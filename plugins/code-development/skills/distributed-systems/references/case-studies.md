# Études de Cas — Systèmes Distribués en Production

Ces quatre études de cas couvrent les scénarios les plus fréquents en architecture distribuée : décomposition de monolithe, saga e-commerce, event sourcing pour l'audit réglementaire, et résilience d'API gateway. Chaque cas présente le contexte réel, la solution technique détaillée avec le code de production, et les métriques mesurées.

---

## Cas 1 — Décomposition Monolithe → Micro-services (Marketplace, 10M Commandes/An)

### Contexte

Marketplace B2C de 8 ans d'âge, stack Ruby on Rails, base PostgreSQL de 400 Go, 15 développeurs. Chaque déploiement requiert 2 heures de gel de fonctionnalités (migrations DB bloquantes) et est planifié toutes les 2 semaines. Le catalogue (3M articles, 500K requêtes/heure en pic) et les commandes (10M/an, écritures intensives) partagent la même base et les mêmes processus applicatifs.

### Problème

Il est impossible de scaler indépendamment le catalogue (haute lecture, cache-friendly) et les commandes (haute écriture, transactions complexes). Un pic de trafic sur le catalogue ralentit les commandes en cours, et inversement. Les migrations de schéma pour les commandes bloquent l'affichage du catalogue pendant des heures.

### Solution — Strangler Fig Pattern

Le Strangler Fig Pattern consiste à extraire les fonctionnalités du monolithe progressivement, en redirigeant le trafic vers les nouveaux services sans Big Bang. L'extraction se fait en trois phases :

**Phase 1 — Extraction du service Catalogue (lecture seule).**
Le catalogue est extrait en premier car il est le plus simple : lecture seule, cache-friendly, pas de transactions complexes. Le monolithe continue d'écrire dans sa DB ; le service Catalogue lit depuis une réplique PostgreSQL dédiée et ajoute un cache Redis avec TTL de 5 minutes.

```typescript
// nginx.conf — router progressivement le trafic catalogue vers le nouveau service
upstream catalogue_service {
  server catalogue-svc:3000 weight=100;  // augmenter progressivement
  server rails-monolith:8080 weight=0;
}

upstream orders_monolith {
  server rails-monolith:8080 weight=100;  // commandes restent dans le monolithe
}

location /api/v1/products {
  proxy_pass http://catalogue_service;
}

location /api/v1/orders {
  proxy_pass http://orders_monolith;
}
```

**Phase 2 — Extraction du service Commandes avec Outbox Pattern.**
Les commandes sont extraites avec un service Node.js + PostgreSQL dédié. L'Outbox Pattern garantit qu'aucune commande n'est perdue lors des appels vers les services externes (paiement, stock).

```sql
-- Base dédiée du service Commandes
CREATE TABLE orders (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id  UUID NOT NULL,
  status       VARCHAR(50) NOT NULL DEFAULT 'pending',
  total_cents  INT NOT NULL,
  currency     VARCHAR(3) NOT NULL DEFAULT 'EUR',
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id   UUID NOT NULL REFERENCES orders(id),
  product_id UUID NOT NULL,
  quantity   INT NOT NULL,
  unit_price_cents INT NOT NULL
);

CREATE TABLE outbox (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  aggregate_id UUID NOT NULL,
  event_type   VARCHAR(200) NOT NULL,
  payload      JSONB NOT NULL,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  published_at TIMESTAMPTZ
);

CREATE INDEX idx_outbox_pending ON outbox (created_at) WHERE published_at IS NULL;
```

```typescript
// Création de commande — order + outbox dans la même transaction
async function createOrder(
  pool: Pool,
  command: CreateOrderCommand
): Promise<string> {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    const orderId = crypto.randomUUID();

    await client.query(
      `INSERT INTO orders (id, customer_id, total_cents, currency)
       VALUES ($1, $2, $3, $4)`,
      [orderId, command.customerId, command.totalCents, command.currency]
    );

    for (const item of command.items) {
      await client.query(
        `INSERT INTO order_items (order_id, product_id, quantity, unit_price_cents)
         VALUES ($1, $2, $3, $4)`,
        [orderId, item.productId, item.quantity, item.unitPriceCents]
      );
    }

    // Outbox : garantit la publication de l'événement même si Kafka est down
    await client.query(
      `INSERT INTO outbox (aggregate_id, event_type, payload)
       VALUES ($1, 'OrderCreated', $2)`,
      [orderId, JSON.stringify({ orderId, ...command })]
    );

    await client.query('COMMIT');
    return orderId;
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}
```

**Phase 3 — Saga pour les paiements.**
Le paiement implique le service Commandes, le service Paiement (Stripe), et le service Inventaire. Une saga orchestrée coordonne les trois avec compensation automatique.

### Architecture avant/après

```
AVANT
┌─────────────────────────────────────┐
│          Rails Monolith             │
│  Catalogue │ Commandes │ Paiements  │
│  [PostgreSQL 400Go partagé]         │
└─────────────────────────────────────┘

APRÈS
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Catalogue   │   │  Commandes   │   │  Paiements   │
│  Service     │   │  Service     │   │  Service     │
│  Node.js     │   │  Node.js     │   │  Node.js     │
│  Redis cache │   │  PG dédié    │   │  PG dédié    │
│  PG replica  │   │  + Outbox    │   │  Stripe API  │
└──────────────┘   └──────────────┘   └──────────────┘
         └──────────────┴──────────────┘
                      Kafka
```

### Métriques

| Métrique | Avant | Après |
|---|---|---|
| Fréquence de déploiement | 1 par 2 semaines | Indépendant par service |
| Latence catalogue p99 | 450ms | 35ms (cache Redis) |
| Perte de commandes | ~0.02% (race conditions) | 0% (outbox) |
| Durée pic catalogue → impact commandes | Corrélé | Aucun impact |

**Leçon clé.** Commencer par extraire le service avec le ratio read/write le plus élevé — le moins risqué. Le catalogue en lecture seule est une extraction "sans filet" : si le nouveau service a un bug, le monolithe reprend le relais immédiatement.

---

## Cas 2 — Saga E-commerce avec 3 Services (Fintech)

### Contexte

Plateforme fintech de paiements en ligne. La création d'une commande implique trois services avec leurs propres bases de données : **Inventaire** (réservation du stock), **Paiement** (débit Stripe), et **Livraison** (création d'une expédition). Chaque service est déployé indépendamment et possède sa propre DB PostgreSQL.

### Problème

Sans coordination, les scénarios de défaillance partiels créent des états incohérents catastrophiques :
- Le paiement réussit mais la réservation stock échoue → client débité sans livraison
- La livraison est créée mais le paiement échoue → expédition envoyée sans encaissement
- Toute panne réseau mid-saga laisse les données dans un état indéterminé

### Solution — Saga Orchestrée avec Compensations

```sql
-- Table de suivi des sagas
CREATE TABLE sagas (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type         VARCHAR(100) NOT NULL,
  status       VARCHAR(50) NOT NULL DEFAULT 'STARTED',
  payload      JSONB NOT NULL,
  current_step VARCHAR(100),
  error        TEXT,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE saga_steps (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  saga_id    UUID NOT NULL REFERENCES sagas(id),
  step_name  VARCHAR(100) NOT NULL,
  status     VARCHAR(50) NOT NULL, -- PENDING | COMPLETED | COMPENSATING | COMPENSATED | FAILED
  result     JSONB,
  executed_at TIMESTAMPTZ,
  compensated_at TIMESTAMPTZ
);
```

```typescript
interface SagaStep<TInput, TOutput> {
  name: string;
  execute: (input: TInput) => Promise<TOutput>;
  compensate: (output: TOutput) => Promise<void>;
}

interface CreateOrderSagaPayload {
  orderId: string;
  customerId: string;
  items: Array<{ productId: string; quantity: number; unitPrice: number }>;
  totalCents: number;
}

interface SagaContext {
  stockReservationId?: string;
  paymentIntentId?: string;
  shipmentId?: string;
}

class CreateOrderSaga {
  private steps: SagaStep<unknown, unknown>[] = [];
  private completedSteps: Array<{ name: string; output: unknown }> = [];

  constructor(
    private pool: Pool,
    private sagaId: string,
    private payload: CreateOrderSagaPayload
  ) {
    this.steps = [
      {
        name: 'RESERVE_STOCK',
        execute: async (input: CreateOrderSagaPayload) => {
          const reservationId = await inventoryClient.reserve({
            items: input.items,
            orderId: input.orderId,
          });
          return { reservationId };
        },
        compensate: async (output: { reservationId: string }) => {
          await inventoryClient.cancelReservation(output.reservationId);
        },
      },
      {
        name: 'PROCESS_PAYMENT',
        execute: async (input: CreateOrderSagaPayload) => {
          const paymentIntentId = await paymentClient.charge({
            customerId: input.customerId,
            amountCents: input.totalCents,
            orderId: input.orderId,
            idempotencyKey: `order-${input.orderId}`,
          });
          return { paymentIntentId };
        },
        compensate: async (output: { paymentIntentId: string }) => {
          await paymentClient.refund(output.paymentIntentId);
        },
      },
      {
        name: 'CREATE_SHIPMENT',
        execute: async (input: CreateOrderSagaPayload) => {
          const shipmentId = await shippingClient.create({
            orderId: input.orderId,
            customerId: input.customerId,
            items: input.items,
          });
          return { shipmentId };
        },
        compensate: async (output: { shipmentId: string }) => {
          await shippingClient.cancel(output.shipmentId);
        },
      },
    ];
  }

  async execute(): Promise<void> {
    await this.updateSagaStatus('IN_PROGRESS');

    for (const step of this.steps) {
      await this.updateCurrentStep(step.name);

      try {
        const output = await (step.execute as (input: unknown) => Promise<unknown>)(
          this.payload
        );
        this.completedSteps.push({ name: step.name, output });
        await this.persistStepResult(step.name, 'COMPLETED', output);
      } catch (err) {
        await this.persistStepResult(step.name, 'FAILED', null, (err as Error).message);
        await this.compensate();
        throw err;
      }
    }

    await this.updateSagaStatus('COMPLETED');
  }

  private async compensate(): Promise<void> {
    await this.updateSagaStatus('COMPENSATING');

    // Compenser dans l'ordre inverse
    for (const completed of [...this.completedSteps].reverse()) {
      const step = this.steps.find(s => s.name === completed.name)!;

      try {
        await (step.compensate as (output: unknown) => Promise<void>)(completed.output);
        await this.persistStepResult(completed.name, 'COMPENSATED');
      } catch (err) {
        // Échec de compensation → alerte humaine requise
        logger.error(
          { sagaId: this.sagaId, step: completed.name, err },
          'CRITICAL: Compensation failed — manual intervention required'
        );
        await this.updateSagaStatus('COMPENSATION_FAILED');
        throw err;
      }
    }

    await this.updateSagaStatus('COMPENSATED');
  }

  private async updateSagaStatus(status: string): Promise<void> {
    await this.pool.query(
      `UPDATE sagas SET status = $1, updated_at = NOW() WHERE id = $2`,
      [status, this.sagaId]
    );
  }

  private async updateCurrentStep(stepName: string): Promise<void> {
    await this.pool.query(
      `UPDATE sagas SET current_step = $1, updated_at = NOW() WHERE id = $2`,
      [stepName, this.sagaId]
    );
  }

  private async persistStepResult(
    stepName: string,
    status: string,
    result: unknown = null,
    error?: string
  ): Promise<void> {
    await this.pool.query(
      `INSERT INTO saga_steps (saga_id, step_name, status, result)
       VALUES ($1, $2, $3, $4)
       ON CONFLICT (saga_id, step_name)
       DO UPDATE SET status = EXCLUDED.status, result = EXCLUDED.result`,
      [this.sagaId, stepName, status, JSON.stringify(result)]
    );
  }
}
```

### Process de recovery pour les sagas bloquées

```typescript
// Worker de recovery — relance les sagas bloquées depuis plus de 10 minutes
async function recoverStuckSagas(pool: Pool): Promise<void> {
  const { rows } = await pool.query<{ id: string; payload: unknown }>(
    `SELECT id, payload FROM sagas
     WHERE status IN ('STARTED', 'IN_PROGRESS')
       AND updated_at < NOW() - INTERVAL '10 minutes'
     LIMIT 10
     FOR UPDATE SKIP LOCKED`
  );

  for (const saga of rows) {
    logger.warn({ sagaId: saga.id }, 'Recovering stuck saga');

    const orchestrator = new CreateOrderSaga(
      pool,
      saga.id,
      saga.payload as CreateOrderSagaPayload
    );

    try {
      await orchestrator.execute();
    } catch (err) {
      logger.error({ sagaId: saga.id, err }, 'Recovery failed');
    }
  }
}
```

### Métriques

| Métrique | Valeur |
|---|---|
| Paiements sans livraison | 0 sur 12 mois |
| Commandes complétées avec succès | 99.97% |
| Commandes compensées automatiquement | 0.03% |
| Sagas bloquées nécessitant intervention humaine | < 5 par trimestre |
| Temps moyen de compensation automatique | 3.2 secondes |

**Leçon clé.** Stocker l'état de la saga en DB dès le premier appel, avant d'exécuter la première étape. Le process de recovery pour les sagas bloquées est aussi critique que la saga elle-même — sans lui, les pannes réseau créent des sagas orphelines indéfiniment.

---

## Cas 3 — Event Sourcing Caisse Enregistreuse (Retail, 500 Caisses)

### Contexte

Éditeur de logiciel de caisse pour la grande distribution. 500 caisses réparties dans 80 magasins. Obligation légale d'audit complet et inaltérable de chaque transaction (norme NF 525 en France). Les caisses doivent fonctionner en mode offline-first (les pannes réseau ne doivent pas interrompre les ventes).

### Problème

Le système précédent stockait l'état courant du ticket en base relationnelle (SQLite local). Les modifications de transactions après coup étaient techniquement possibles (problème légal). La synchronisation vers le serveur central lors du retour en ligne créait des conflits non résolus (dernière écriture gagne → perte de données).

### Solution — Event Sourcing Local + Vector Clocks

**Événements métier du domaine Ticket :**

```typescript
type TicketEvent =
  | { type: 'TICKET_OUVERT'; payload: { ticketId: string; caissierIdId: string; caisseId: string } }
  | { type: 'ARTICLE_AJOUTE'; payload: { codeEan: string; libelle: string; quantite: number; prixUnitaire: number } }
  | { type: 'ARTICLE_RETIRE'; payload: { codeEan: string; quantite: number } }
  | { type: 'REMISE_APPLIQUEE'; payload: { type: 'POURCENTAGE' | 'MONTANT'; valeur: number; motif: string } }
  | { type: 'PAIEMENT_RECU'; payload: { mode: 'CB' | 'ESPECES' | 'TITRE_RESTAURANT'; montant: number } }
  | { type: 'TICKET_CLOS'; payload: { montantTotal: number; montantTVA: number; ticketNumber: string } };

// Agrégat Ticket — état calculé depuis les événements
interface TicketState {
  id: string;
  status: 'OUVERT' | 'CLOS' | 'ANNULE';
  lignes: Array<{ codeEan: string; libelle: string; quantite: number; prixUnitaire: number }>;
  remises: Array<{ type: string; valeur: number }>;
  paiements: Array<{ mode: string; montant: number }>;
  total: number;
}

function applyTicketEvent(state: TicketState, event: TicketEvent): TicketState {
  switch (event.type) {
    case 'TICKET_OUVERT':
      return { ...state, id: event.payload.ticketId, status: 'OUVERT' };

    case 'ARTICLE_AJOUTE':
      return {
        ...state,
        lignes: [...state.lignes, {
          codeEan: event.payload.codeEan,
          libelle: event.payload.libelle,
          quantite: event.payload.quantite,
          prixUnitaire: event.payload.prixUnitaire,
        }],
        total: state.total + event.payload.quantite * event.payload.prixUnitaire,
      };

    case 'REMISE_APPLIQUEE':
      const remiseAmount = event.payload.type === 'POURCENTAGE'
        ? state.total * event.payload.valeur / 100
        : event.payload.valeur;
      return {
        ...state,
        remises: [...state.remises, event.payload],
        total: state.total - remiseAmount,
      };

    case 'PAIEMENT_RECU':
      return {
        ...state,
        paiements: [...state.paiements, event.payload],
      };

    case 'TICKET_CLOS':
      return { ...state, status: 'CLOS' };

    default:
      return state;
  }
}
```

**Event store local SQLite (sur la caisse) :**

```sql
CREATE TABLE ticket_events (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  ticket_id    TEXT NOT NULL,
  type         TEXT NOT NULL,
  payload      TEXT NOT NULL,  -- JSON
  version      INTEGER NOT NULL,
  caisse_id    TEXT NOT NULL,
  created_at   TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
  synced_at    TEXT,           -- NULL = non synchronisé
  vector_clock TEXT NOT NULL   -- JSON: {"caisse_001": 42, "caisse_002": 0}
);

CREATE UNIQUE INDEX idx_ticket_version ON ticket_events (ticket_id, version);
CREATE INDEX idx_unsynced ON ticket_events (created_at) WHERE synced_at IS NULL;
```

**Vector clocks pour la synchronisation sans conflit :**

```typescript
type VectorClock = Record<string, number>;

function incrementClock(clock: VectorClock, nodeId: string): VectorClock {
  return { ...clock, [nodeId]: (clock[nodeId] ?? 0) + 1 };
}

function mergeClock(a: VectorClock, b: VectorClock): VectorClock {
  const merged: VectorClock = { ...a };
  for (const [node, time] of Object.entries(b)) {
    merged[node] = Math.max(merged[node] ?? 0, time);
  }
  return merged;
}

function happensBefore(a: VectorClock, b: VectorClock): boolean {
  // a → b si tous les composants de a sont ≤ b et au moins un est strictement <
  const allNodes = new Set([...Object.keys(a), ...Object.keys(b)]);
  let strictlyLess = false;
  for (const node of allNodes) {
    const timeA = a[node] ?? 0;
    const timeB = b[node] ?? 0;
    if (timeA > timeB) return false;
    if (timeA < timeB) strictlyLess = true;
  }
  return strictlyLess;
}

// Synchronisation : les événements sont ajoutés dans l'event store central
// dans l'ordre causal déterminé par les vector clocks — pas de conflits
async function syncCaisseEvents(
  caisseId: string,
  events: Array<{ ticketId: string; type: string; payload: unknown; vectorClock: VectorClock }>
): Promise<void> {
  for (const event of events) {
    await appendToEventStoreDB(event);
  }
  // Pas de résolution de conflits nécessaire : les événements sont des faits immuables
  // L'order causal est préservé grâce aux vector clocks
}
```

**Projection ChiffreAffaires (serveur central) :**

```typescript
interface ChiffreAffairesEntry {
  date: string;
  magasinId: string;
  totalHT: number;
  totalTVA: number;
  nombreTickets: number;
}

async function handleChiffreAffairesProjection(
  event: { type: string; payload: unknown; metadata: { caisseId: string; createdAt: string } }
): Promise<void> {
  if (event.type !== 'TICKET_CLOS') return;

  const payload = event.payload as { montantTotal: number; montantTVA: number };
  const date = event.metadata.createdAt.substring(0, 10); // YYYY-MM-DD
  const magasinId = event.metadata.caisseId.split('_')[0]; // "magasin001_caisse01" → "magasin001"

  await pool.query(
    `INSERT INTO chiffre_affaires (date, magasin_id, total_ht, total_tva, nombre_tickets)
     VALUES ($1, $2, $3, $4, 1)
     ON CONFLICT (date, magasin_id) DO UPDATE SET
       total_ht = chiffre_affaires.total_ht + EXCLUDED.total_ht,
       total_tva = chiffre_affaires.total_tva + EXCLUDED.total_tva,
       nombre_tickets = chiffre_affaires.nombre_tickets + 1`,
    [date, magasinId, payload.montantTotal - payload.montantTVA, payload.montantTVA]
  );
}
```

### Métriques

| Métrique | Résultat |
|---|---|
| Audit légal NF 525 | Certifié — aucun événement modifiable |
| Conflits à la synchronisation offline-online | 0 (vector clocks) |
| Rapports CA en temps réel | Latence < 5s après synchronisation |
| Disponibilité caisse (panne réseau) | 100% — mode offline-first natif |
| Perte de données lors des synchronisations | 0 |

**Leçon clé.** Event sourcing + vector clocks est la solution canonique pour l'offline-first avec synchronisation. L'immutabilité des événements rend les conflits structurellement impossibles : il n'y a rien à "écraser" — seulement des événements à fusionner dans l'ordre causal.

---

## Cas 4 — Résilience API Gateway (SaaS, 99.9% SLO)

### Contexte

Plateforme SaaS B2B avec un API gateway Express devant 6 micro-services. SLO de disponibilité de 99.9% stipulé dans les contrats clients (soit 8.7 heures de downtime autorisé par an). Le service Rapports exécute des requêtes analytiques lourdes sur des datasets de plusieurs centaines de Mo et peut prendre jusqu'à 30 secondes pour répondre.

### Problème

Le service Rapports lent provoque des cascades de timeouts : les threads Express s'accumulent en attente, la mémoire du gateway augmente, les timeouts se propagent aux autres routes. La disponibilité effective est de 98.7% — le SLO contractuel de 99.9% n'est pas atteint. Le MTTR (Mean Time To Recovery) est de 3 heures (détection manuelle + redémarrage).

### Solution — Circuit Breaker par Service + Bulkhead + Fallback Cache

**Circuit Breaker avec Opossum :**

```typescript
import CircuitBreaker from 'opossum';
import { Router } from 'express';
import { Counter, Gauge } from 'prom-client';

// Métriques Prometheus pour le circuit state
const circuitStateGauge = new Gauge({
  name: 'circuit_breaker_state',
  help: 'Circuit breaker state (0=CLOSED, 1=OPEN, 2=HALF_OPEN)',
  labelNames: ['service'],
});

const circuitCallCounter = new Counter({
  name: 'circuit_breaker_calls_total',
  help: 'Total circuit breaker calls',
  labelNames: ['service', 'outcome'], // success | failure | rejected | timeout | fallback
});

function createServiceCircuitBreaker(
  serviceName: string,
  serviceCall: (...args: unknown[]) => Promise<unknown>
): CircuitBreaker {
  const breaker = new CircuitBreaker(serviceCall, {
    timeout: serviceName === 'reporting' ? 15000 : 3000, // timeout adapté par service
    errorThresholdPercentage: 50,  // 50% d'erreurs → OPEN
    resetTimeout: 30000,           // 30s en OPEN avant HALF_OPEN
    volumeThreshold: 10,           // minimum 10 appels avant d'évaluer le seuil
    rollingCountTimeout: 10000,    // fenêtre glissante de 10s
    rollingCountBuckets: 10,
    name: serviceName,
  });

  // Mise à jour des métriques Prometheus sur chaque transition d'état
  breaker.on('open', () => {
    circuitStateGauge.set({ service: serviceName }, 1);
    logger.warn({ service: serviceName }, 'Circuit OPENED');
  });
  breaker.on('halfOpen', () => {
    circuitStateGauge.set({ service: serviceName }, 2);
    logger.info({ service: serviceName }, 'Circuit HALF-OPEN');
  });
  breaker.on('close', () => {
    circuitStateGauge.set({ service: serviceName }, 0);
    logger.info({ service: serviceName }, 'Circuit CLOSED');
  });
  breaker.on('success', () =>
    circuitCallCounter.inc({ service: serviceName, outcome: 'success' })
  );
  breaker.on('failure', () =>
    circuitCallCounter.inc({ service: serviceName, outcome: 'failure' })
  );
  breaker.on('reject', () =>
    circuitCallCounter.inc({ service: serviceName, outcome: 'rejected' })
  );
  breaker.on('timeout', () =>
    circuitCallCounter.inc({ service: serviceName, outcome: 'timeout' })
  );
  breaker.on('fallback', () =>
    circuitCallCounter.inc({ service: serviceName, outcome: 'fallback' })
  );

  return breaker;
}
```

**Bulkhead avec p-limit — isolation du service Rapports :**

```typescript
import pLimit from 'p-limit';
import { Redis } from 'ioredis';

const redis = new Redis();

// Semaphores par service — le service Rapports ne peut monopoliser le gateway
const bulkheads = {
  analytics:     pLimit(5),   // service analytique léger
  users:         pLimit(30),
  orders:        pLimit(20),
  inventory:     pLimit(20),
  notifications: pLimit(50),
  reporting:     pLimit(3),   // strictement limité — service lent isolé
};

type ServiceKey = keyof typeof bulkheads;

// Fallback : renvoyer les données du cache Redis si le circuit est ouvert
async function callServiceWithFallback<T>(
  service: ServiceKey,
  breaker: CircuitBreaker,
  cacheKey: string,
  fn: () => Promise<T>
): Promise<{ data: T; degraded: boolean }> {
  try {
    const data = await bulkheads[service](() => breaker.fire(fn));
    // Mettre en cache la réponse fraîche
    await redis.set(cacheKey, JSON.stringify(data), 'EX', 300); // TTL 5min
    return { data, degraded: false };
  } catch (err) {
    // Circuit ouvert ou bulkhead saturé → tenter le cache stale
    const cached = await redis.get(cacheKey);
    if (cached) {
      logger.warn({ service, cacheKey }, 'Serving stale cache — service degraded');
      return { data: JSON.parse(cached) as T, degraded: true };
    }
    throw err;
  }
}
```

**Middleware Express — assemblage :**

```typescript
const reportingBreaker = createServiceCircuitBreaker(
  'reporting',
  (req: Request) => reportingServiceClient.get(req.path, { timeout: 15000 })
);

// Fallback : mode dégradé avec message explicite si pas de cache
reportingBreaker.fallback(async (req: Request, err: Error) => {
  logger.warn({ err: err.message }, 'Reporting fallback triggered');
  return {
    degraded: true,
    message: 'Le service de rapports est temporairement indisponible. Les données affichées peuvent ne pas être à jour.',
    data: null,
  };
});

const router = Router();

router.get('/reports/:reportId', async (req, res) => {
  const cacheKey = `report:${req.params.reportId}:${req.query.from}:${req.query.to}`;

  const { data, degraded } = await callServiceWithFallback(
    'reporting',
    reportingBreaker,
    cacheKey,
    () => reportingServiceClient.getReport(req.params.reportId, req.query)
  );

  if (degraded) {
    res.set('X-Degraded-Mode', 'true');
  }

  res.json(data);
});
```

**Dashboard Grafana — visualisation des circuit states :**

```json
{
  "panels": [
    {
      "title": "Circuit Breaker States",
      "type": "stat",
      "targets": [
        {
          "expr": "circuit_breaker_state",
          "legendFormat": "{{service}}"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "mappings": [
            { "value": 0, "text": "CLOSED", "color": "green" },
            { "value": 1, "text": "OPEN",   "color": "red" },
            { "value": 2, "text": "HALF-OPEN", "color": "orange" }
          ]
        }
      }
    },
    {
      "title": "Circuit Breaker — Appels par outcome (5m)",
      "type": "timeseries",
      "targets": [
        {
          "expr": "sum by (service, outcome) (rate(circuit_breaker_calls_total[5m]))",
          "legendFormat": "{{service}} / {{outcome}}"
        }
      ]
    },
    {
      "title": "SLO — Disponibilité 30j glissants",
      "type": "gauge",
      "targets": [
        {
          "expr": "1 - (sum(increase(http_requests_total{status=~'5..'}[30d])) / sum(increase(http_requests_total[30d])))",
          "legendFormat": "Availability"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "steps": [
              { "value": 0,     "color": "red" },
              { "value": 0.999, "color": "green" }
            ]
          }
        }
      }
    }
  ]
}
```

### Métriques

| Métrique | Avant | Après |
|---|---|---|
| Disponibilité (30 jours) | 98.7% | 99.92% (SLO atteint) |
| Impact panne service Rapports sur les autres services | Total | Aucun (bulkhead) |
| MTTR (Mean Time To Recovery) | 3h (manuel) | 2 minutes (auto-recovery circuit) |
| Alertes PagerDuty sur incident Rapports | 8/mois | 0 (circuit absorbe les pannes) |
| Réponses servies depuis cache dégradé | N/A | 0.08% des requêtes |

**Leçon clé.** Le circuit breaker par service + bulkhead est le minimum non-négociable pour tout API gateway en production. Sans isolation, un seul service lent peut saturer l'ensemble du gateway — une défaillance d'un micro-service devient une défaillance de toute la plateforme. La combinaison circuit breaker + cache stale permet un mode dégradé transparent pour l'utilisateur : il voit des données légèrement obsolètes plutôt qu'une page d'erreur.
