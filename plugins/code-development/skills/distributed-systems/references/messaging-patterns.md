# Patterns de Messagerie — Kafka, RabbitMQ et Outbox

La messagerie asynchrone est le tissu conjonctif des architectures distribuées. Elle découple les services dans le temps et l'espace, absorbe les pics de charge, et permet la résilience face aux pannes de services aval. Ce guide couvre Kafka et RabbitMQ en profondeur, le pattern Outbox pour la cohérence transactionnelle, et les outils de déduplication et de documentation.

---

## Architecture Kafka

### Concepts fondamentaux

Kafka est un log distribué et persistant. Les messages sont appelés "records" et sont organisés en **topics**. Chaque topic est divisé en **partitions** — l'unité de parallélisme et d'ordering. L'ordering est garanti au sein d'une partition, pas entre partitions.

```
Topic "orders"
├── Partition 0: [offset 0] [offset 1] [offset 2] ... [offset N]
├── Partition 1: [offset 0] [offset 1] ...
└── Partition 2: [offset 0] [offset 1] ...
```

**Replication factor.** Chaque partition est répliquée sur N brokers. Avec `replication.factor=3`, une partition a 1 leader et 2 replicas. Le leader gère toutes les lectures et écritures ; les replicas suivent de manière synchrone (ISR — In-Sync Replicas).

**Consumer groups.** Plusieurs consommateurs dans le même groupe se partagent les partitions d'un topic (chaque partition est assignée à un seul consommateur du groupe). Des groupes différents consomment le même topic indépendamment avec leurs propres offsets.

### Garanties de livraison selon la configuration producer

| Config `acks` | Garantie | Latence | Risque |
|---|---|---|---|
| `acks=0` | Fire and forget | Minimale | Perte de messages possible |
| `acks=1` | Leader a accusé réception | Basse | Perte si leader tombe avant réplication |
| `acks=all` (ou `-1`) | Tous les ISR ont accusé réception | Plus haute | Aucune perte dans les cas normaux |

---

## Kafka Producer — Exactly-Once Semantics

### Configuration idempotente et transactionnelle

```typescript
import { Kafka, CompressionTypes } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'order-service',
  brokers: ['kafka-1:9092', 'kafka-2:9092', 'kafka-3:9092'],
});

// Producer idempotent : élimine les doublons dus aux retries réseau
const idempotentProducer = kafka.producer({
  idempotent: true,         // active le mode idempotent (acks=all implicite)
  maxInFlightRequests: 5,   // max 5 requêtes en vol pour l'idempotence
  retry: {
    retries: 10,
    initialRetryTime: 100,
    factor: 2,
  },
});

// Producer transactionnel : exactly-once sur plusieurs partitions/topics
const transactionalProducer = kafka.producer({
  transactionalId: 'order-service-tx-1', // unique par instance producer
  idempotent: true,
  maxInFlightRequests: 1, // obligatoire pour les transactions
});

await transactionalProducer.connect();

// Envoi transactionnel
await transactionalProducer.transaction(async (tx) => {
  await tx.send({
    topic: 'orders',
    compression: CompressionTypes.GZIP,
    messages: [
      {
        key: order.id,             // clé = routing vers une partition stable
        value: JSON.stringify(order),
        headers: {
          'event-type': 'OrderPlaced',
          'schema-version': '3',
          'correlation-id': correlationId,
        },
      },
    ],
  });
  // Si cette ligne n'est pas atteinte (exception), la transaction est annulée
});
```

### Partitionnement et ordering

La clé de message détermine la partition cible. Pour garantir que tous les événements d'une même commande sont dans la même partition (et donc ordonnés), utiliser `order.customerId` comme clé — tous les événements d'un client vont sur la même partition.

---

## Kafka Consumer — Stratégies de Commit

### Auto-commit vs commit manuel

```typescript
const consumer = kafka.consumer({
  groupId: 'payment-processor',
  sessionTimeout: 30000,
  heartbeatInterval: 3000,
});

await consumer.connect();
await consumer.subscribe({ topic: 'orders', fromBeginning: false });

// Mode eachMessage : commit offset après chaque message
await consumer.run({
  autoCommit: false, // commit manuel pour contrôler exactement ce qui est commité
  eachMessage: async ({ topic, partition, message, heartbeat }) => {
    try {
      await processPayment(JSON.parse(message.value!.toString()));

      // Commit offset uniquement après traitement réussi
      await consumer.commitOffsets([
        { topic, partition, offset: (BigInt(message.offset) + 1n).toString() },
      ]);
    } catch (err) {
      // Ne pas committer → le message sera re-livré après rebalancing ou redémarrage
      throw err;
    }
  },
});
```

### Traitement par batch

```typescript
await consumer.run({
  autoCommit: false,
  eachBatch: async ({ batch, resolveOffset, heartbeat, commitOffsetsIfNecessary }) => {
    const messages = batch.messages;

    // Traitement bulk pour la performance
    const orders = messages.map(m => JSON.parse(m.value!.toString()));
    await bulkInsertOrders(orders);

    // Marquer chaque offset comme résolu
    for (const message of messages) {
      resolveOffset(message.offset);
      await heartbeat(); // prévenir le timeout de session sur les gros batches
    }

    // Commit du batch entier
    await commitOffsetsIfNecessary();
  },
});
```

### Rebalancing et partition assignment

Lors d'un rebalancing (ajout/suppression d'un consommateur dans le groupe), les partitions sont redistribuées. Les offsets non commités sont perdus sur la partition qui change de consommateur. Stratégie : toujours committer avant de terminer le traitement du message courant, ou accepter l'at-least-once delivery et rendre les handlers idempotents.

---

## Schema Registry — Contrat de Données

Le Schema Registry (Confluent ou compatible) centralise les schémas Avro/JSON Schema/Protobuf et applique les règles de compatibilité.

### Modes de compatibilité

| Mode | Description | Usage |
|---|---|---|
| `BACKWARD` | Le nouveau schéma peut lire les messages de l'ancien | Ajout de champs optionnels |
| `FORWARD` | L'ancien schéma peut lire les messages du nouveau | Suppression de champs optionnels |
| `FULL` | BACKWARD + FORWARD simultanément | Contrainte maximale |
| `NONE` | Pas de vérification | Développement uniquement |

```typescript
import { SchemaRegistry, SchemaType } from '@kafkajs/confluent-schema-registry';

const registry = new SchemaRegistry({ host: 'http://schema-registry:8081' });

// Enregistrer un schéma Avro
const { id: schemaId } = await registry.register(
  {
    type: SchemaType.AVRO,
    schema: JSON.stringify({
      type: 'record',
      name: 'OrderPlaced',
      namespace: 'com.example.orders',
      fields: [
        { name: 'orderId', type: 'string' },
        { name: 'customerId', type: 'string' },
        { name: 'total', type: 'double' },
        { name: 'currency', type: 'string', default: 'EUR' },
      ],
    }),
  },
  { subject: 'orders-value' }
);

// Encodage Avro + schéma ID dans le message
const encodedValue = await registry.encode(schemaId, {
  orderId: order.id,
  customerId: order.customerId,
  total: order.total,
  currency: order.currency,
});

// Décodage côté consommateur (le schéma ID est dans les premiers octets)
const decoded = await registry.decode(message.value!);
```

---

## RabbitMQ — Exchanges et Routing

### Types d'exchanges

```typescript
import amqplib from 'amqplib';

const connection = await amqplib.connect('amqp://localhost');
const channel = await connection.createChannel();

// Direct exchange : routing par routing key exacte
await channel.assertExchange('orders.direct', 'direct', { durable: true });
await channel.assertQueue('payment-queue', { durable: true });
await channel.bindQueue('payment-queue', 'orders.direct', 'order.placed');

// Fanout exchange : broadcast à toutes les queues liées
await channel.assertExchange('orders.events', 'fanout', { durable: true });
// Toutes les queues liées reçoivent tous les messages, sans routing key

// Topic exchange : routing par pattern (*, #)
await channel.assertExchange('orders.topic', 'topic', { durable: true });
await channel.bindQueue('audit-queue', 'orders.topic', 'orders.#');      // tous les événements orders
await channel.bindQueue('payment-queue', 'orders.topic', 'orders.*.placed'); // orders.eu.placed, orders.us.placed
```

### Quand utiliser quel exchange

| Exchange | Cas d'usage |
|---|---|
| `direct` | Routage simple par type d'événement, worker queues |
| `fanout` | Broadcast (notifications, invalidation de cache) |
| `topic` | Routage hiérarchique multi-critères |
| `headers` | Routage par attributs de message (rare, complexe) |

---

## RabbitMQ — Dead Letter Exchange

### Configuration DLX

```typescript
// Dead Letter Exchange pour les messages qui échouent
await channel.assertExchange('dlx', 'direct', { durable: true });
await channel.assertQueue('dead-letter-queue', { durable: true });
await channel.bindQueue('dead-letter-queue', 'dlx', 'payment-queue');

// Queue principale avec DLX configuré
await channel.assertQueue('payment-queue', {
  durable: true,
  arguments: {
    'x-dead-letter-exchange': 'dlx',
    'x-dead-letter-routing-key': 'payment-queue',
    'x-message-ttl': 300000,  // 5 minutes avant DLX si pas consommé
    'x-max-retries': 3,       // extension RabbitMQ — nécessite plugin
  },
});

// Consommateur avec gestion des retries manuels
await channel.consume('payment-queue', async (msg) => {
  if (!msg) return;

  const retryCount = parseInt(
    (msg.properties.headers?.['x-retry-count'] ?? '0').toString()
  );

  try {
    await processPayment(JSON.parse(msg.content.toString()));
    channel.ack(msg);
  } catch (err) {
    if (retryCount < 3) {
      // Re-publier avec compteur de retry incrémenté
      channel.publish(
        'orders.direct',
        'order.placed',
        msg.content,
        {
          ...msg.properties,
          headers: { ...msg.properties.headers, 'x-retry-count': retryCount + 1 },
          expiration: String(1000 * Math.pow(2, retryCount)), // backoff
        }
      );
      channel.ack(msg); // ack le message original
    } else {
      // Poison message → dead-letter (nack sans requeue)
      channel.nack(msg, false, false);
    }
  }
});
```

---

## Outbox Pattern — Cohérence Transactionnelle

### Problème

Sans l'Outbox Pattern, le service écrit en base de données et publie dans Kafka en deux opérations séparées. Si la publication Kafka échoue après le commit en base, le message est perdu. Si la base échoue après la publication Kafka, le message est publié mais la donnée n'est pas persistée.

### Solution : table outbox transactionnelle

```sql
CREATE TABLE outbox (
  id           UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  aggregate_id UUID         NOT NULL,
  event_type   VARCHAR(200) NOT NULL,
  payload      JSONB        NOT NULL,
  created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  published_at TIMESTAMPTZ,          -- NULL = non publié
  retry_count  INT          NOT NULL DEFAULT 0
);

CREATE INDEX idx_outbox_unpublished
  ON outbox (created_at)
  WHERE published_at IS NULL;
```

```typescript
// Écriture transactionnelle : order + outbox dans la même transaction
async function placeOrder(pool: Pool, order: Order): Promise<void> {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    // 1. Écriture métier
    await client.query(
      'INSERT INTO orders (id, customer_id, total) VALUES ($1, $2, $3)',
      [order.id, order.customerId, order.total]
    );

    // 2. Message dans l'outbox (même transaction)
    await client.query(
      `INSERT INTO outbox (aggregate_id, event_type, payload)
       VALUES ($1, $2, $3)`,
      [order.id, 'OrderPlaced', JSON.stringify(order)]
    );

    await client.query('COMMIT');
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}
```

### Outbox Worker — Polling

```typescript
async function outboxWorker(pool: Pool, producer: Producer): Promise<void> {
  while (true) {
    const { rows } = await pool.query<{
      id: string;
      aggregate_id: string;
      event_type: string;
      payload: unknown;
    }>(
      `SELECT id, aggregate_id, event_type, payload
       FROM outbox
       WHERE published_at IS NULL
       ORDER BY created_at ASC
       LIMIT 100
       FOR UPDATE SKIP LOCKED` // évite les conflits entre workers en parallèle
    );

    for (const row of rows) {
      try {
        await producer.send({
          topic: 'orders',
          messages: [{ key: row.aggregate_id, value: JSON.stringify(row.payload) }],
        });

        await pool.query(
          'UPDATE outbox SET published_at = NOW() WHERE id = $1',
          [row.id]
        );
      } catch (err) {
        await pool.query(
          'UPDATE outbox SET retry_count = retry_count + 1 WHERE id = $1',
          [row.id]
        );
      }
    }

    await sleep(500);
  }
}
```

### Outbox avec Debezium (CDC)

Au lieu du polling, Debezium lit le write-ahead log (WAL) de PostgreSQL et publie les changements directement dans Kafka. Latence plus faible, pas de polling, pas de `FOR UPDATE SKIP LOCKED`.

```json
{
  "name": "orders-outbox-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "dbz",
    "database.dbname": "orders_db",
    "slot.name": "debezium_slot",
    "publication.name": "debezium_pub",
    "table.include.list": "public.outbox",
    "transforms": "outbox",
    "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter",
    "transforms.outbox.route.by.field": "event_type",
    "transforms.outbox.table.field.event.key": "aggregate_id"
  }
}
```

---

## Déduplication des Messages

### Idempotency keys avec Redis

```typescript
import { Redis } from 'ioredis';

const redis = new Redis();
const DEDUP_TTL = 86400; // 24h

async function processMessageIdempotently(
  messageId: string,
  handler: () => Promise<void>
): Promise<void> {
  const key = `dedup:processed:${messageId}`;

  // SET NX : n'écrit que si la clé n'existe pas encore
  const isNew = await redis.set(key, '1', 'EX', DEDUP_TTL, 'NX');

  if (!isNew) {
    // Message déjà traité — idempotent, on ignore
    return;
  }

  try {
    await handler();
  } catch (err) {
    // En cas d'échec, supprimer la clé pour permettre le retry
    await redis.del(key);
    throw err;
  }
}
```

### Bloom Filter pour la déduplication à grande échelle

Pour des volumes très élevés (milliards de messages), un Bloom filter Redis réduit la mémoire consommée au prix d'un taux de faux positifs configurable.

```typescript
// Nécessite le module RedisBloom
await redis.call('BF.RESERVE', 'dedup:bloom', '0.001', '10000000');
// 0.1% de faux positifs, 10M d'éléments

async function isAlreadyProcessed(messageId: string): Promise<boolean> {
  const result = await redis.call('BF.EXISTS', 'dedup:bloom', messageId);
  return result === 1;
}

async function markAsProcessed(messageId: string): Promise<void> {
  await redis.call('BF.ADD', 'dedup:bloom', messageId);
}
```

---

## Choreography vs Orchestration

| Dimension | Choreography | Orchestration |
|---|---|---|
| Couplage | Faible (événements) | Fort (orchestrateur connaît tout) |
| Visibilité du flux | Difficile | Centralisée |
| Debugging | Complexe (distribué) | Simple (état centralisé) |
| Résilience | Décentralisée | Point de défaillance unique |
| Complexité accrue avec | Beaucoup d'acteurs | Peu d'acteurs |
| Cas idéal | Notifications, propagation d'événements | Saga avec compensations, workflow métier |

La choreography convient aux flux simples où chaque service réagit aux événements d'un autre sans logique conditionnelle complexe. L'orchestration s'impose dès qu'il y a des compensations, des branches conditionnelles ou un état de workflow à maintenir.

---

## AsyncAPI — Documentation des Topics

AsyncAPI 2.x est le standard de documentation pour les APIs asynchrones, équivalent à OpenAPI pour les APIs REST.

```yaml
asyncapi: '2.6.0'
info:
  title: Orders Service
  version: '1.0.0'

servers:
  production:
    url: kafka://kafka-prod:9092
    protocol: kafka

channels:
  orders:
    description: Événements du cycle de vie des commandes
    bindings:
      kafka:
        partitions: 12
        replicas: 3
    publish:
      message:
        $ref: '#/components/messages/OrderPlaced'
    subscribe:
      message:
        $ref: '#/components/messages/PaymentProcessed'

components:
  messages:
    OrderPlaced:
      name: OrderPlaced
      title: Commande passée
      contentType: application/avro
      headers:
        type: object
        properties:
          schema-version:
            type: string
            description: Version du schéma Avro
      payload:
        type: object
        required: [orderId, customerId, total]
        properties:
          orderId:
            type: string
            format: uuid
          customerId:
            type: string
          total:
            type: number
            format: double
          currency:
            type: string
            default: EUR
```

AsyncAPI permet de générer automatiquement la documentation, les SDKs clients, et les mocks pour les tests d'intégration. L'outil `asyncapi generate` produit des stubs TypeScript à partir du schéma.
