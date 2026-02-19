# Event Sourcing — Événements comme Source de Vérité

L'Event Sourcing renverse le paradigme de persistance classique : au lieu de stocker l'état courant d'une entité, on stocke la séquence complète des événements qui ont conduit à cet état. L'état actuel est une projection calculée à partir de ces événements. Ce modèle apporte un audit trail inaltérable, le time-travel debugging, et une scalabilité horizontale des projections.

---

## Pourquoi Event Sourcing

### Avantages structurels

**Audit trail complet et inaltérable.** Chaque changement d'état est un événement immuable avec timestamp, auteur, et contexte. Aucune donnée n'est jamais écrasée. C'est la réponse native aux exigences légales (conformité RGPD, audit financier, retail POS).

**Time-travel debugging.** Il est possible de reconstituer l'état exact d'un agrégat à n'importe quel instant passé en rejouant les événements jusqu'à ce timestamp. Les bugs de production deviennent reproductibles.

**Scalabilité des projections.** Une projection est une vue matérialisée calculée depuis les événements. On peut créer autant de projections que nécessaire sans modifier le modèle de données source — un avantage décisif pour les équipes qui font évoluer leurs besoins d'analyse.

**Découplage fort.** Les événements sont des faits passés (nommés au passé : `OrderPlaced`, `PaymentReceived`). Les consommateurs s'abonnent aux événements qui les concernent sans couplage avec le producteur.

### Cas d'usage appropriés

- Systèmes financiers (transactions, comptabilité en partie double)
- Logiciels de caisse (obligation légale d'audit inaltérable)
- Workflow engines (chaque transition est un événement)
- Collaborative editing (CRDT + event sourcing)

### Cas où l'Event Sourcing est sur-dimensionné

Un CRUD simple sans exigence d'audit ou de projections multiples ne justifie pas la complexité de l'Event Sourcing. Le seuil de rentabilité est atteint quand le besoin d'historique ou de projections découplées est avéré.

---

## Event Store — Implémentation PostgreSQL

### Schéma de la table `events`

```sql
CREATE TABLE events (
  seq          BIGSERIAL       PRIMARY KEY,          -- séquence globale monotone
  aggregate_id UUID            NOT NULL,
  aggregate_type VARCHAR(100)  NOT NULL,
  type         VARCHAR(200)    NOT NULL,
  version      INT             NOT NULL,             -- version locale à l'agrégat
  payload      JSONB           NOT NULL,
  metadata     JSONB           NOT NULL DEFAULT '{}',
  created_at   TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Index pour charger les événements d'un agrégat en ordre
CREATE INDEX idx_events_aggregate
  ON events (aggregate_id, version);

-- Index pour les projections qui consomment depuis un checkpoint
CREATE INDEX idx_events_seq
  ON events (seq);

-- Unicité de la version par agrégat — garantit l'optimistic concurrency
ALTER TABLE events
  ADD CONSTRAINT uq_aggregate_version
  UNIQUE (aggregate_id, version);
```

La colonne `seq` est la séquence globale de l'event store. Elle garantit l'ordre total pour les projections qui consomment tous les événements. La colonne `version` est locale à chaque agrégat et permet la détection de conflits de concurrence optimiste.

### Append atomique avec vérification de version

```typescript
import { Pool } from 'pg';

interface DomainEvent {
  type: string;
  payload: Record<string, unknown>;
  metadata?: Record<string, unknown>;
}

interface AppendOptions {
  aggregateId: string;
  aggregateType: string;
  events: DomainEvent[];
  expectedVersion: number; // -1 si l'agrégat n'existe pas encore
}

async function appendEvents(pool: Pool, opts: AppendOptions): Promise<void> {
  const { aggregateId, aggregateType, events, expectedVersion } = opts;
  const client = await pool.connect();

  try {
    await client.query('BEGIN');

    // Vérification de la version courante (optimistic concurrency)
    const { rows } = await client.query<{ max_version: number }>(
      `SELECT COALESCE(MAX(version), -1) AS max_version
       FROM events
       WHERE aggregate_id = $1`,
      [aggregateId]
    );

    const currentVersion = rows[0].max_version;
    if (currentVersion !== expectedVersion) {
      throw new ConcurrencyError(
        `Version conflict on ${aggregateId}: expected ${expectedVersion}, got ${currentVersion}`
      );
    }

    // Insertion des événements en une seule transaction
    for (let i = 0; i < events.length; i++) {
      const newVersion = expectedVersion + 1 + i;
      await client.query(
        `INSERT INTO events (aggregate_id, aggregate_type, type, version, payload, metadata)
         VALUES ($1, $2, $3, $4, $5, $6)`,
        [
          aggregateId,
          aggregateType,
          events[i].type,
          newVersion,
          JSON.stringify(events[i].payload),
          JSON.stringify(events[i].metadata ?? {}),
        ]
      );
    }

    await client.query('COMMIT');
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}

class ConcurrencyError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ConcurrencyError';
  }
}
```

### Retry sur conflit de concurrence

```typescript
async function appendWithRetry(
  pool: Pool,
  opts: Omit<AppendOptions, 'expectedVersion'>,
  loadAggregate: () => Promise<{ version: number }>,
  maxRetries = 3
): Promise<void> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const { version } = await loadAggregate();
    try {
      await appendEvents(pool, { ...opts, expectedVersion: version });
      return;
    } catch (err) {
      if (err instanceof ConcurrencyError && attempt < maxRetries - 1) {
        // Attente exponentielle avant retry
        await sleep(50 * Math.pow(2, attempt));
        continue;
      }
      throw err;
    }
  }
}

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));
```

---

## Snapshots

### Quand créer un snapshot

Sans snapshots, charger un agrégat avec 10 000 événements est coûteux. La règle pratique : créer un snapshot tous les N événements (N = 50 à 200 selon la fréquence des événements et la taille des payloads).

```sql
CREATE TABLE snapshots (
  aggregate_id   UUID         NOT NULL,
  aggregate_type VARCHAR(100) NOT NULL,
  version        INT          NOT NULL,  -- version de l'événement le plus récent inclus
  state          JSONB        NOT NULL,
  created_at     TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  PRIMARY KEY (aggregate_id, version)
);
```

### Chargement avec snapshot

```typescript
async function loadAggregate<TState>(
  pool: Pool,
  aggregateId: string,
  applyEvent: (state: TState, event: DomainEvent) => TState,
  initialState: TState
): Promise<{ state: TState; version: number }> {
  // 1. Charger le snapshot le plus récent
  const snapshotResult = await pool.query<{ version: number; state: TState }>(
    `SELECT version, state FROM snapshots
     WHERE aggregate_id = $1
     ORDER BY version DESC
     LIMIT 1`,
    [aggregateId]
  );

  let state = initialState;
  let fromVersion = -1;

  if (snapshotResult.rows.length > 0) {
    const snap = snapshotResult.rows[0];
    state = snap.state;
    fromVersion = snap.version;
  }

  // 2. Charger uniquement les événements postérieurs au snapshot
  const eventsResult = await pool.query<{
    type: string;
    payload: Record<string, unknown>;
    version: number;
  }>(
    `SELECT type, payload, version FROM events
     WHERE aggregate_id = $1 AND version > $2
     ORDER BY version ASC`,
    [aggregateId, fromVersion]
  );

  let currentVersion = fromVersion;
  for (const row of eventsResult.rows) {
    state = applyEvent(state, { type: row.type, payload: row.payload });
    currentVersion = row.version;
  }

  return { state, version: currentVersion };
}
```

### Création automatique de snapshot

```typescript
const SNAPSHOT_THRESHOLD = 100;

async function appendAndMaybeSnapshot<TState>(
  pool: Pool,
  aggregateId: string,
  aggregateType: string,
  events: DomainEvent[],
  currentState: TState,
  currentVersion: number
): Promise<void> {
  await appendEvents(pool, {
    aggregateId,
    aggregateType,
    events,
    expectedVersion: currentVersion,
  });

  const newVersion = currentVersion + events.length;

  if (newVersion % SNAPSHOT_THRESHOLD === 0) {
    await pool.query(
      `INSERT INTO snapshots (aggregate_id, aggregate_type, version, state)
       VALUES ($1, $2, $3, $4)
       ON CONFLICT (aggregate_id, version) DO NOTHING`,
      [aggregateId, aggregateType, newVersion, JSON.stringify(currentState)]
    );
  }
}
```

---

## Projections

### Projection synchrone vs asynchrone

| Caractéristique | Synchrone | Asynchrone |
|---|---|---|
| Cohérence | Forte (même transaction) | Éventuelle |
| Complexité | Faible | Élevée |
| Scalabilité | Limitée | Horizontale |
| Cas d'usage | Vue simple, usage interne | Reporting, recherche, multi-consumers |

### Projection asynchrone avec checkpoint

```typescript
interface ProjectionCheckpoint {
  projectionName: string;
  lastSeq: number;
}

// Table de checkpoint pour reprendre après redémarrage
// CREATE TABLE projection_checkpoints (
//   projection_name VARCHAR(100) PRIMARY KEY,
//   last_seq BIGINT NOT NULL DEFAULT 0
// );

async function runProjection(
  pool: Pool,
  projectionName: string,
  handler: (event: { type: string; payload: unknown; seq: number }) => Promise<void>,
  batchSize = 100
): Promise<void> {
  // Charger le dernier checkpoint
  const cpResult = await pool.query<{ last_seq: number }>(
    `SELECT last_seq FROM projection_checkpoints WHERE projection_name = $1`,
    [projectionName]
  );
  let lastSeq = cpResult.rows[0]?.last_seq ?? 0;

  while (true) {
    const { rows } = await pool.query<{
      seq: number;
      type: string;
      payload: unknown;
    }>(
      `SELECT seq, type, payload FROM events
       WHERE seq > $1
       ORDER BY seq ASC
       LIMIT $2`,
      [lastSeq, batchSize]
    );

    if (rows.length === 0) {
      await sleep(500); // Polling interval
      continue;
    }

    for (const row of rows) {
      await handler(row);
      lastSeq = row.seq;
    }

    // Sauvegarder le checkpoint après chaque batch
    await pool.query(
      `INSERT INTO projection_checkpoints (projection_name, last_seq)
       VALUES ($1, $2)
       ON CONFLICT (projection_name) DO UPDATE SET last_seq = EXCLUDED.last_seq`,
      [projectionName, lastSeq]
    );
  }
}
```

### Rebuild d'une projection

Le rebuild consiste à remettre le checkpoint à 0 et à rejouer tous les événements depuis le début. Il faut d'abord vider la table cible, puis relancer la projection.

```typescript
async function rebuildProjection(
  pool: Pool,
  projectionName: string,
  truncateTarget: () => Promise<void>,
  handler: (event: { type: string; payload: unknown; seq: number }) => Promise<void>
): Promise<void> {
  await truncateTarget();
  await pool.query(
    `UPDATE projection_checkpoints SET last_seq = 0 WHERE projection_name = $1`,
    [projectionName]
  );
  await runProjection(pool, projectionName, handler);
}
```

---

## Upcasting — Évolution du Format des Événements

Quand le format d'un événement change (renommage de champ, ajout de données obligatoires, restructuration), les anciens événements stockés doivent toujours pouvoir être lus. L'upcasting transforme un événement d'une ancienne version vers la version courante au moment de la lecture, sans jamais modifier l'event store.

```typescript
type EventUpcaster = (payload: Record<string, unknown>) => Record<string, unknown>;

const upcasters: Record<string, Record<number, EventUpcaster>> = {
  OrderPlaced: {
    1: (payload) => ({
      // v1 → v2 : `customer_id` renommé en `customerId`, `total` ajouté
      ...payload,
      customerId: payload['customer_id'],
      total: payload['amount'],
    }),
    2: (payload) => ({
      // v2 → v3 : `currency` ajouté avec valeur par défaut
      ...payload,
      currency: payload['currency'] ?? 'EUR',
    }),
  },
};

function upcast(
  eventType: string,
  payload: Record<string, unknown>,
  fromVersion: number,
  toVersion: number
): Record<string, unknown> {
  let current = payload;
  const typeUpcasters = upcasters[eventType] ?? {};

  for (let v = fromVersion; v < toVersion; v++) {
    const fn = typeUpcasters[v];
    if (fn) current = fn(current);
  }
  return current;
}
```

La version de l'événement est stockée dans les métadonnées (`metadata.schemaVersion`). Lors du chargement, l'upcaster est appliqué automatiquement avant de passer le payload à la fonction `applyEvent`.

---

## EventStoreDB — Fonctionnalités Spécifiques

EventStoreDB est une base de données optimisée pour l'Event Sourcing avec des fonctionnalités natives que PostgreSQL ne peut pas reproduire nativement.

### Persistent Subscriptions et Competing Consumers

```typescript
import { EventStoreDBClient, jsonEvent, FORWARDS, START } from '@eventstore/db-client';

const client = EventStoreDBClient.connectionString(
  'esdb://localhost:2113?tls=false'
);

// Créer une persistent subscription (competing consumers)
await client.createPersistentSubscriptionToStream('orders', 'payment-processor', {
  startFrom: START,
  resolveLinkTos: false,
  extraStatistics: true,
  maxRetryCount: 5,
  checkPointAfter: 1000, // ms
  liveBufferSize: 500,
  readBatchSize: 20,
  historyBufferSize: 500,
});

// Consommateur
const subscription = client.subscribeToPersistentSubscriptionToStream(
  'orders',
  'payment-processor'
);

for await (const resolvedEvent of subscription) {
  try {
    await processPayment(resolvedEvent.event);
    await subscription.ack(resolvedEvent);
  } catch (err) {
    // Nack → retry ou dead-letter selon la config
    await subscription.nack('retry', 'Processing failed', resolvedEvent);
  }
}
```

Les persistent subscriptions avec competing consumers permettent à plusieurs instances d'un service de consommer le même stream en parallèle avec distribution automatique des événements — un équivalent des consumer groups Kafka natif à EventStoreDB.

---

## Design des Agrégats

### Règles fondamentales

**Un agrégat = une transaction.** L'append d'événements pour un agrégat est atomique. Deux agrégats ne peuvent pas être modifiés dans la même transaction — si c'est nécessaire, c'est un signal que les bounded contexts sont mal découpés.

**Petits agrégats = moins de conflits.** Un agrégat qui accumule beaucoup d'événements par seconde génère beaucoup de conflits de concurrence optimiste. Découper en agrégats plus petits réduit la contention.

**Nommer les événements au passé.** `OrderPlaced`, `ItemAdded`, `PaymentReceived` — ce sont des faits immuables.

---

## Tests d'Agrégats Event-Sourced

Le pattern `given/when/then` est idiomatique pour tester des agrégats event-sourced : on définit l'historique initial, on exécute une commande, et on vérifie les événements produits.

```typescript
describe('Order aggregate', () => {
  it('should add an item to an existing order', () => {
    // Given : événements passés qui reconstituent l'état initial
    const givenEvents: DomainEvent[] = [
      { type: 'OrderCreated', payload: { orderId: '123', customerId: 'cust-1' } },
    ];

    // When : commande à exécuter
    const state = givenEvents.reduce(applyOrderEvent, initialOrderState);
    const newEvents = handleAddItem(state, {
      type: 'AddItem',
      payload: { productId: 'prod-42', quantity: 2, unitPrice: 19.99 },
    });

    // Then : événements produits (pas l'état final)
    expect(newEvents).toHaveLength(1);
    expect(newEvents[0].type).toBe('ItemAdded');
    expect(newEvents[0].payload).toMatchObject({
      productId: 'prod-42',
      quantity: 2,
      lineTotal: 39.98,
    });
  });
});
```

Tester les événements produits plutôt que l'état final est une distinction importante : cela valide le contrat de l'agrégat avec ses consommateurs externes.

---

## Problèmes Courants

### Événements trop volumineux

Un événement ne devrait pas dépasser quelques kilooctets. Les données volumineuses (fichiers, images) sont stockées en dehors de l'event store avec une référence dans le payload (`{ "fileKey": "s3://bucket/file.pdf" }`).

### Ordering garanti par agrégat, pas global

La séquence globale (`seq BIGSERIAL`) garantit l'ordre de l'event store côté PostgreSQL, mais deux agrégats écrits en parallèle peuvent avoir leurs événements entrelacés dans la séquence. Les projections qui dépendent de l'ordre global entre différents agrégats doivent gérer cette situation explicitement (lamport timestamps ou vector clocks).

### ACID dans l'event store

L'event store est append-only par contrat. Aucun événement ne doit jamais être modifié ou supprimé. Si une donnée personnelle doit être supprimée (RGPD), on utilise le pattern "crypto-shredding" : chiffrer les données personnelles avec une clé per-utilisateur, puis supprimer la clé pour rendre les données illisibles sans toucher aux événements.

| Propriété | Event Store |
|---|---|
| Append | Autorisé (seule opération) |
| Update | Interdit |
| Delete | Interdit |
| Read | Autorisé (par aggregate_id, par seq range) |

### Événements manquants

Un bug peut faire en sorte qu'un événement ne soit pas persisté. La défense principale est le test unitaire `given/when/then` et l'idempotence de l'append. En production, un monitoring sur les gaps de `version` par agrégat permet de détecter les incohérences.
