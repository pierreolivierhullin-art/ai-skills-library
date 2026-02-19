# Pub/Sub et Scaling — Redis, NATS et Socket.io Adapters

## Redis Pub/Sub : Commandes et Limitations

Redis Pub/Sub est un mécanisme de messagerie feu-et-oubli (fire-and-forget) : les messages publiés ne sont jamais persistés, et si aucun subscriber n'écoute au moment de la publication, le message est définitivement perdu.

### Commandes fondamentales

```bash
# S'abonner à un canal exact
SUBSCRIBE room:equipe-dev

# S'abonner à plusieurs canaux avec un pattern glob
PSUBSCRIBE room:*
PSUBSCRIBE user:*.notifications

# Lister les canaux actifs (au moins 1 subscriber)
PUBSUB CHANNELS
PUBSUB CHANNELS room:*

# Nombre de subscribers sur un canal
PUBSUB NUMSUB room:equipe-dev room:general

# Publier un message
PUBLISH room:equipe-dev '{"type":"MESSAGE","userId":"alice","content":"Bonjour"}'
```

### Utilisation avec Node.js (`ioredis`)

```typescript
import Redis from 'ioredis';

// Deux clients séparés : un subscriber est en mode bloquant
const publisher = new Redis(process.env.REDIS_URL!);
const subscriber = new Redis(process.env.REDIS_URL!);

// Abonnement exact à plusieurs canaux
await subscriber.subscribe('room:equipe-dev', 'room:general');

subscriber.on('message', (channel: string, message: string) => {
  console.log(`[${channel}] ${message}`);
  const data = JSON.parse(message);
  // Diffuser aux clients WebSocket de cette instance connectés à ce canal
  broadcastToLocalClients(channel, data);
});

// Abonnement par pattern (PSUBSCRIBE)
await subscriber.psubscribe('user:*');

subscriber.on('pmessage', (pattern: string, channel: string, message: string) => {
  // pattern = 'user:*', channel = 'user:alice', message = '...'
  const userId = channel.split(':')[1];
  sendToUser(userId, JSON.parse(message));
});

// Publier depuis n'importe où dans l'application
async function publishToChannel(channel: string, event: object): Promise<number> {
  const subscriberCount = await publisher.publish(channel, JSON.stringify(event));
  return subscriberCount;  // Nombre de subscribers qui ont reçu le message
}

function broadcastToLocalClients(_channel: string, _data: unknown): void { /* implémentation locale */ }
function sendToUser(_userId: string, _data: unknown): void { /* implémentation locale */ }
```

### Limitations de Redis Pub/Sub

| Limitation | Impact | Solution |
|------------|--------|----------|
| Pas de persistence | Messages perdus si aucun subscriber actif | Utiliser Redis Streams |
| Pas d'ACK | Impossible de savoir si le message a été traité | Redis Streams + consumer groups |
| Pas de replay | Impossible de rejouer les messages manqués | Redis Streams avec `XREAD` |
| At-most-once delivery | Un message peut ne jamais arriver | Redis Streams pour at-least-once |
| Pas de filtrage côté serveur | Le subscriber reçoit tout | PSUBSCRIBE ou filtrer côté applicatif |

---

## Redis Streams vs Pub/Sub : Quand Utiliser Quoi

Redis Streams (introduits en Redis 5.0) adressent toutes les limitations du Pub/Sub en ajoutant persistence, consumer groups et replay.

```typescript
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL!);

// === REDIS STREAMS ===

// Ajouter un message au stream
async function appendToStream(streamKey: string, data: Record<string, string>): Promise<string> {
  // XADD mystream * field1 value1 field2 value2
  // '*' = ID auto-généré par Redis (timestamp-sequence)
  const messageId = await redis.xadd(streamKey, '*', ...Object.entries(data).flat());
  return messageId!;
}

// Créer un consumer group (once at startup)
async function setupConsumerGroup(streamKey: string, groupName: string): Promise<void> {
  try {
    // '$' = commencer à partir des nouveaux messages seulement
    // '0' = rejouer depuis le début du stream
    await redis.xgroup('CREATE', streamKey, groupName, '$', 'MKSTREAM');
  } catch (err: unknown) {
    // Ignorer si le groupe existe déjà
    if (!(err as Error).message.includes('BUSYGROUP')) throw err;
  }
}

// Lire les messages en tant que consumer dans un groupe
async function consumeMessages(
  streamKey: string,
  groupName: string,
  consumerName: string,
): Promise<void> {
  while (true) {
    // XREADGROUP GROUP mygroup consumer1 COUNT 10 BLOCK 5000 STREAMS mystream >
    // '>' = seulement les messages non délivrés à ce groupe
    const results = await redis.xreadgroup(
      'GROUP', groupName, consumerName,
      'COUNT', '10',
      'BLOCK', '5000',
      'STREAMS', streamKey, '>',
    ) as Array<[string, Array<[string, string[]]>]> | null;

    if (!results) continue;  // Timeout — aucun message

    for (const [_stream, messages] of results) {
      for (const [id, fields] of messages) {
        const data = Object.fromEntries(
          fields.reduce<Array<[string, string]>>((acc, _, i, arr) =>
            i % 2 === 0 ? [...acc, [arr[i], arr[i + 1]]] : acc, []
          )
        );

        try {
          await processMessage(data);
          // Acquitter le message après traitement réussi
          await redis.xack(streamKey, groupName, id);
        } catch (err) {
          console.error(`Échec du traitement du message ${id}:`, err);
          // Ne pas ACK → le message reste en "pending" pour retry
        }
      }
    }
  }
}

async function processMessage(_data: Record<string, string>): Promise<void> { /* logique */ }

// Tableau de décision
// Utiliser Redis Pub/Sub quand :
//   - La perte de messages est acceptable (métriques non critiques, curseurs de présence)
//   - Latence ultra-faible requise (<1ms vs ~5ms pour Streams)
//   - Pas besoin de replay
//
// Utiliser Redis Streams quand :
//   - Les messages doivent être garantis (commandes, paiements, notifications)
//   - Plusieurs consumers doivent traiter chaque message (fan-out garanti)
//   - Besoin de replay historique (nouveaux consumers qui rattrapent le retard)
//   - At-least-once delivery nécessaire
```

---

## NATS : Publish-Subscribe, Queue Groups et JetStream

NATS est un broker de messagerie haute performance (Go), conçu pour la faible latence et le haut débit. Il supporte nativement le clustering et la géo-distribution.

```typescript
import { connect, StringCodec, NatsConnection } from 'nats';

const nc: NatsConnection = await connect({ servers: process.env.NATS_URL ?? 'nats://localhost:4222' });
const sc = StringCodec();

// === PUBLISH-SUBSCRIBE SIMPLE ===
const sub = nc.subscribe('room.equipe-dev');

(async () => {
  for await (const msg of sub) {
    const data = JSON.parse(sc.decode(msg.data));
    console.log('Reçu :', data);
  }
})();

await nc.publish('room.equipe-dev', sc.encode(JSON.stringify({ content: 'Bonjour' })));

// === QUEUE GROUPS (load balancing) ===
// Plusieurs workers s'abonnent au même subject avec le même groupe
// Un seul worker parmi le groupe reçoit chaque message
const worker1 = nc.subscribe('tasks.process', { queue: 'workers' });
const worker2 = nc.subscribe('tasks.process', { queue: 'workers' });

// Seul worker1 OU worker2 recevra chaque message publié sur 'tasks.process'
await nc.publish('tasks.process', sc.encode(JSON.stringify({ taskId: 'abc123' })));

// === REQUEST-REPLY ===
// Pattern requête-réponse natif dans NATS
const sub2 = nc.subscribe('service.ping');
(async () => {
  for await (const msg of sub2) {
    // Répondre directement à l'expediteur
    msg.respond(sc.encode(JSON.stringify({ status: 'ok', ts: Date.now() })));
  }
})();

const response = await nc.request('service.ping', sc.encode('{}'), { timeout: 5_000 });
console.log('Réponse :', JSON.parse(sc.decode(response.data)));
```

### JetStream pour la Persistence

```typescript
import { connect, AckPolicy, RetentionPolicy } from 'nats';

const nc = await connect({ servers: 'nats://localhost:4222' });
const js = nc.jetstream();
const jsm = await nc.jetstreamManager();

// Créer un stream persistant
await jsm.streams.add({
  name: 'EVENTS',
  subjects: ['events.*'],
  retention: RetentionPolicy.Limits,
  max_msgs: 100_000,
  max_age: 7 * 24 * 60 * 60 * 1e9,  // 7 jours en nanosecondes
});

// Publier avec garantie de persistence
const pubAck = await js.publish('events.order', new TextEncoder().encode(
  JSON.stringify({ orderId: 'ORD-001', amount: 99.90 })
));
console.log(`Message persisté, séquence : ${pubAck.seq}`);

// Consumer durable (reprend là où il s'est arrêté après restart)
await jsm.consumers.add('EVENTS', {
  durable_name: 'order-processor',
  ack_policy: AckPolicy.Explicit,
  filter_subject: 'events.order',
});

const consumer = await js.consumers.get('EVENTS', 'order-processor');
const messages = await consumer.consume();

for await (const msg of messages) {
  const order = JSON.parse(new TextDecoder().decode(msg.data));
  await processOrder(order);
  msg.ack();  // Acquittement explicite
}

async function processOrder(_order: unknown): Promise<void> { /* logique */ }
```

---

## Socket.io Adapters : Redis, Streams et Cluster

### `@socket.io/redis-adapter` (Pub/Sub)

```typescript
import { createServer } from 'http';
import { Server } from 'socket.io';
import { createClient } from 'redis';
import { createAdapter } from '@socket.io/redis-adapter';

const httpServer = createServer();
const io = new Server(httpServer, {
  cors: { origin: process.env.CLIENT_URL },
});

const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);

// Comment ça fonctionne :
// - Chaque room Socket.io correspond à un canal Redis
// - Quand io.to('room-1').emit() est appelé sur l'instance A,
//   l'adapter publie sur le canal Redis 'socket.io#room-1'
// - Toutes les instances abonnées à ce canal reçoivent le message
//   et le diffusent à leurs clients locaux dans 'room-1'
io.adapter(createAdapter(pubClient, subClient));

io.on('connection', (socket) => {
  socket.on('join', (roomId: string) => socket.join(roomId));

  // Cet emit traverse Redis — atteint TOUS les clients dans la room
  // sur TOUTES les instances du cluster
  socket.on('broadcast', ({ roomId, event }: { roomId: string; event: string }) => {
    io.to(roomId).emit('update', { event, from: socket.id });
  });
});
```

### `@socket.io/redis-streams-adapter` (Streams — persisté)

```typescript
import { createAdapter } from '@socket.io/redis-streams-adapter';
import { createClient } from 'redis';

const redisClient = createClient({ url: process.env.REDIS_URL });
await redisClient.connect();

// Avantage vs pub/sub : les messages sont persistés dans Redis Streams
// Si une instance redémarre, elle peut rejouer les messages manqués
io.adapter(createAdapter(redisClient, {
  streamName: 'socket.io',
  maxLen: 10_000,           // Conserver les 10 000 derniers messages
  readCount: 100,            // Lire 100 messages à la fois
  sessionKeyPrefix: 'sio:',
  heartbeatInterval: 5_000,
  heartbeatTimeout: 10_000,
}));
```

---

## Architecture Multi-Instance : 4 Pods Kubernetes

```
                    ┌──────────────────────────────────────────────┐
                    │              Nginx / Ingress                  │
                    │         (Load Balancer L7, round-robin)       │
                    └───┬──────────┬──────────┬──────────┬─────────┘
                        │          │          │          │
                   Pod 1      Pod 2      Pod 3      Pod 4
               Fastify+SIO Fastify+SIO Fastify+SIO Fastify+SIO
                    │          │          │          │
                    └──────────┴────┬─────┴──────────┘
                                    │
                             Redis Cluster
                        (Pub/Sub message bus)
                                    │
                             PostgreSQL
                        (Persistence des messages)
```

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: realtime-server
spec:
  replicas: 4
  selector:
    matchLabels:
      app: realtime-server
  template:
    spec:
      containers:
        - name: server
          image: myregistry/realtime-server:latest
          env:
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: redis-secret
                  key: url
            - name: PORT
              value: "3000"
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: realtime-service
spec:
  # ClusterIP ou NodePort — pas besoin de sticky sessions avec Redis adapter
  type: ClusterIP
  ports:
    - port: 3000
      targetPort: 3000
```

---

## Kafka pour le Temps Réel : Quand et Pourquoi

Kafka est pertinent quand Redis Pub/Sub ne suffit plus. La décision dépend principalement du volume, de la durée de rétention et du nombre de consumers.

| Critère | Redis Pub/Sub | Redis Streams | Apache Kafka |
|---------|--------------|---------------|--------------|
| Débit max | ~100K msg/s | ~200K msg/s | ~1M+ msg/s par partition |
| Rétention | Aucune | Configurable (ex : 7j) | Configurable (ex : 30j, illimité) |
| Replay | Non | Oui | Oui |
| Consumer groups | Non | Oui | Oui (offset management) |
| Ordering | Par canal | Par stream | Par partition |
| Complexité ops | Très faible | Faible | Élevée (ZooKeeper/KRaft) |
| Cas d'usage | Présence, curseurs | Notifications garanties | Event sourcing, analytics, audit log |

```typescript
import { Kafka, Producer, Consumer } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'realtime-app',
  brokers: (process.env.KAFKA_BROKERS ?? 'localhost:9092').split(','),
});

// Producer — envoyer des événements
const producer: Producer = kafka.producer({
  idempotent: true,           // Garantit exactly-once à l'écriture
  transactionTimeout: 30_000,
});
await producer.connect();

async function publishEvent(topic: string, key: string, value: object): Promise<void> {
  await producer.send({
    topic,
    messages: [
      {
        key,
        value: JSON.stringify(value),
        headers: { source: 'realtime-server', ts: Date.now().toString() },
      },
    ],
  });
}

// Consumer — traiter les événements avec exactly-once
const consumer: Consumer = kafka.consumer({ groupId: 'notification-processor' });
await consumer.connect();
await consumer.subscribe({ topics: ['user.events', 'order.events'], fromBeginning: false });

await consumer.run({
  partitionsConsumedConcurrently: 3,
  eachMessage: async ({ topic, partition, message }) => {
    const key = message.key?.toString();
    const value = JSON.parse(message.value!.toString());

    console.log(`[${topic}][${partition}][offset:${message.offset}] ${key}:`, value);

    await handleEvent(topic, value);
    // Offset commité automatiquement après eachMessage
  },
});

async function handleEvent(_topic: string, _value: unknown): Promise<void> { /* logique */ }
```

---

## Fan-Out : Broadcasting Efficace à N Utilisateurs

### Problème du fan-out naïf

Envoyer N messages individuels à N utilisateurs est O(N) en appels Redis. Le fan-out via un canal partagé est O(1) côté publisher.

```typescript
// MAUVAIS : N appels Redis pour N utilisateurs
async function notifyUsersNaive(userIds: string[], event: object): Promise<void> {
  for (const userId of userIds) {
    await publisher.publish(`user:${userId}`, JSON.stringify(event));  // N appels Redis
  }
}

// BON : 1 publication sur un canal de groupe, le filtre est côté subscriber
async function notifyRoom(roomId: string, event: object): Promise<void> {
  await publisher.publish(`room:${roomId}`, JSON.stringify(event));  // 1 appel Redis
}

// OPTIMISÉ pour les notifications à grande échelle : batching + fan-out via pipeline
async function notifyUsersOptimized(userIds: string[], event: object): Promise<void> {
  const BATCH_SIZE = 500;
  const payload = JSON.stringify(event);

  for (let i = 0; i < userIds.length; i += BATCH_SIZE) {
    const batch = userIds.slice(i, i + BATCH_SIZE);

    // Pipeline Redis : grouper les commandes en un seul round-trip réseau
    const pipeline = publisher.pipeline();
    for (const userId of batch) {
      pipeline.publish(`user:${userId}`, payload);
    }
    await pipeline.exec();
  }
}
```

---

## Rate Limiting des Messages WebSocket

```typescript
// Token bucket par userId — limite le débit de messages
class TokenBucket {
  private tokens: number;
  private lastRefill: number;

  constructor(
    private readonly capacity: number,      // Tokens maximum
    private readonly refillRate: number,     // Tokens par milliseconde
  ) {
    this.tokens = capacity;
    this.lastRefill = Date.now();
  }

  consume(count = 1): boolean {
    this.refill();
    if (this.tokens >= count) {
      this.tokens -= count;
      return true;  // Autorisé
    }
    return false;   // Rate limited
  }

  private refill(): void {
    const now = Date.now();
    const elapsed = now - this.lastRefill;
    this.tokens = Math.min(this.capacity, this.tokens + elapsed * this.refillRate);
    this.lastRefill = now;
  }
}

// Appliquer le rate limiting sur les messages WebSocket entrants
const rateLimiters = new Map<string, TokenBucket>();

function getRateLimiter(userId: string): TokenBucket {
  if (!rateLimiters.has(userId)) {
    // 10 messages par seconde, burst de 30
    rateLimiters.set(userId, new TokenBucket(30, 10 / 1000));
  }
  return rateLimiters.get(userId)!;
}

io.on('connection', (socket) => {
  const userId = socket.data.userId as string;

  socket.use(([event, ..._args], next) => {
    const limiter = getRateLimiter(userId);
    if (!limiter.consume()) {
      socket.emit('ERROR', { code: 'RATE_LIMITED', message: 'Trop de messages. Ralentissez.' });
      return;  // Ne pas appeler next() = bloquer le message
    }
    next();
  });

  // Nettoyer le rate limiter à la déconnexion
  socket.on('disconnect', () => {
    rateLimiters.delete(userId);
  });
});
```

---

## Métriques et Monitoring des Connexions Temps Réel

```typescript
import { register, Gauge, Counter, Histogram } from 'prom-client';

// Métriques Prometheus pour les WebSockets
const activeConnections = new Gauge({
  name: 'websocket_active_connections',
  help: 'Nombre de connexions WebSocket actives',
  labelNames: ['namespace'],
});

const messagesTotal = new Counter({
  name: 'websocket_messages_total',
  help: 'Nombre total de messages WebSocket traités',
  labelNames: ['direction', 'type'],
});

const messageLatency = new Histogram({
  name: 'websocket_message_latency_ms',
  help: 'Latence de traitement des messages WebSocket en millisecondes',
  buckets: [1, 5, 10, 25, 50, 100, 250, 500, 1000],
});

const disconnectionRate = new Counter({
  name: 'websocket_disconnections_total',
  help: 'Nombre total de déconnexions WebSocket',
  labelNames: ['reason'],
});

// Instrumenter Socket.io
io.on('connection', (socket) => {
  activeConnections.labels('default').inc();

  socket.onAny((event: string) => {
    messagesTotal.labels('inbound', event).inc();
  });

  socket.onAnyOutgoing((event: string) => {
    messagesTotal.labels('outbound', event).inc();
  });

  socket.on('disconnect', (reason: string) => {
    activeConnections.labels('default').dec();
    disconnectionRate.labels(reason).inc();

    // Alerter si trop de déconnexions en rafale (signe de problème réseau)
  });
});

// Endpoint Prometheus
app.get('/metrics', async (_req, res) => {
  res.set('Content-Type', register.contentType);
  res.send(await register.metrics());
});
```

---

## Circuit Breaker pour les Publishers Redis

```typescript
enum CircuitState {
  CLOSED = 'CLOSED',     // Normal — les requêtes passent
  OPEN = 'OPEN',         // Dégradé — les requêtes sont bloquées
  HALF_OPEN = 'HALF_OPEN',  // Récupération — une requête test passe
}

class RedisPublisherCircuitBreaker {
  private state = CircuitState.CLOSED;
  private failureCount = 0;
  private lastFailureTime = 0;
  private readonly FAILURE_THRESHOLD = 5;
  private readonly TIMEOUT = 30_000;

  constructor(private readonly redis: Redis) {}

  async publish(channel: string, message: string): Promise<boolean> {
    if (this.state === CircuitState.OPEN) {
      const elapsed = Date.now() - this.lastFailureTime;
      if (elapsed < this.TIMEOUT) {
        // Circuit ouvert — logger et continuer sans Redis
        console.warn(`Circuit ouvert : message vers ${channel} abandonné`);
        return false;
      }
      this.state = CircuitState.HALF_OPEN;
    }

    try {
      await this.redis.publish(channel, message);
      this.onSuccess();
      return true;
    } catch (err) {
      this.onFailure();
      throw err;
    }
  }

  private onSuccess(): void {
    this.failureCount = 0;
    this.state = CircuitState.CLOSED;
  }

  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    if (this.failureCount >= this.FAILURE_THRESHOLD) {
      this.state = CircuitState.OPEN;
      console.error(`Circuit ouvert après ${this.failureCount} échecs Redis`);
    }
  }
}
```

---

## Multi-Région : Latence Géographique et Redis Global

```typescript
// Stratégie de routing intelligent multi-région
// Utiliser Upstash Redis Global pour la réplication automatique entre régions

import { Redis } from '@upstash/redis';

// Upstash Redis Global réplique automatiquement vers la région la plus proche
const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

// Dans un déploiement multi-région (ex : Vercel Edge, Cloudflare Workers)
// chaque région lit depuis le replica le plus proche (latence ~5ms)
// mais écrit vers le primaire (latence ~50-100ms cross-région)

async function publishGlobal(channel: string, event: object): Promise<void> {
  // Les écritures vont au primaire, les lectures viennent du replica local
  await redis.publish(channel, JSON.stringify(event));
}

// Routing basé sur la géolocalisation (Next.js Middleware / Vercel Edge)
// middleware.ts
export function middleware(request: Request): Response {
  const country = request.headers.get('x-vercel-ip-country') ?? 'US';

  const regionMap: Record<string, string> = {
    FR: 'https://eu-west-api.monapp.com',
    DE: 'https://eu-central-api.monapp.com',
    US: 'https://us-east-api.monapp.com',
    JP: 'https://ap-northeast-api.monapp.com',
  };

  const targetRegion = regionMap[country] ?? regionMap['US'];
  return Response.redirect(`${targetRegion}${new URL(request.url).pathname}`);
}
```

---

## Résumé des Choix Technologiques

| Scénario | Solution recommandée |
|----------|---------------------|
| Diffusion multi-instance Socket.io | `@socket.io/redis-adapter` (Pub/Sub) |
| Diffusion multi-instance avec replay | `@socket.io/redis-streams-adapter` |
| Notifications garanties | Redis Streams + consumer groups |
| Events analytics / audit log | Apache Kafka |
| Microservices request-reply | NATS |
| Fan-out massif (millions d'utilisateurs) | NATS JetStream ou Kafka + SSE côté client |
| Déploiement simple (1-4 instances) | Redis Pub/Sub — simple et suffisant |
| Multi-région faible latence | Upstash Redis Global |
