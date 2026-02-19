# Patterns de Résilience — Circuit Breaker, Retry et Bulkhead

Les systèmes distribués tombent. Pas si, mais quand. La résilience ne consiste pas à éviter les pannes, mais à en limiter l'impact, à se rétablir automatiquement, et à dégrader gracieusement plutôt que d'effondrer l'ensemble du système. Ce guide couvre les patterns fondamentaux de résilience avec des implémentations TypeScript prêtes pour la production.

---

## Retry avec Exponential Backoff et Jitter

### Pourquoi le jitter est indispensable

Sans jitter, tous les clients en échec retentatent simultanément après le même délai — ce qui provoque un "thundering herd" qui peut aggraver la panne. Le jitter introduit une perturbation aléatoire qui étale les retries dans le temps.

**Formule de calcul :**
```
délai(tentative) = min(cap, base * 2^tentative) + random(0, jitter_max)

Exemple avec base=100ms, cap=30s, jitter_max=1s :
- Tentative 0 : 100ms + random(0, 1000ms)
- Tentative 1 : 200ms + random(0, 1000ms)
- Tentative 2 : 400ms + random(0, 1000ms)
- Tentative 5 : 3200ms + random(0, 1000ms)
- Tentative 8 : 25600ms + random(0, 1000ms)
- Tentative 9+ : 30000ms (cap) + random(0, 1000ms)
```

### Implémentation TypeScript

```typescript
interface RetryOptions {
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
  jitterMs: number;
  retryOn?: (err: Error) => boolean;
  onRetry?: (err: Error, attempt: number, delayMs: number) => void;
}

async function withRetry<T>(
  fn: () => Promise<T>,
  opts: RetryOptions
): Promise<T> {
  const {
    maxRetries,
    baseDelayMs,
    maxDelayMs,
    jitterMs,
    retryOn = () => true,
    onRetry,
  } = opts;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      const error = err as Error;

      if (attempt === maxRetries || !retryOn(error)) {
        throw error;
      }

      const exponential = Math.min(maxDelayMs, baseDelayMs * Math.pow(2, attempt));
      const jitter = Math.random() * jitterMs;
      const delay = Math.floor(exponential + jitter);

      onRetry?.(error, attempt + 1, delay);
      await sleep(delay);
    }
  }

  throw new Error('Unreachable'); // TypeScript safety
}

// Usage
const result = await withRetry(
  () => fetchOrderFromExternalAPI(orderId),
  {
    maxRetries: 5,
    baseDelayMs: 100,
    maxDelayMs: 30000,
    jitterMs: 1000,
    retryOn: (err) => isTransientError(err), // ne pas retenter sur 4xx
    onRetry: (err, attempt, delay) =>
      logger.warn({ err, attempt, delay }, 'Retrying request'),
  }
);

function isTransientError(err: Error): boolean {
  const transientCodes = [408, 429, 500, 502, 503, 504];
  const statusCode = (err as { statusCode?: number }).statusCode;
  return statusCode === undefined || transientCodes.includes(statusCode);
}

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));
```

### Utilisation de `p-retry`

```typescript
import pRetry, { AbortError } from 'p-retry';

const result = await pRetry(
  async (attemptNumber) => {
    const res = await fetch(`https://api.example.com/orders/${orderId}`);

    if (res.status === 404) {
      throw new AbortError('Order not found — no retry');
    }
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    return res.json();
  },
  {
    retries: 5,
    minTimeout: 100,
    maxTimeout: 30000,
    randomize: true, // active le jitter
    onFailedAttempt: ({ message, attemptNumber, retriesLeft }) => {
      logger.warn({ message, attemptNumber, retriesLeft }, 'Attempt failed');
    },
  }
);
```

---

## Idempotency Keys — Requêtes HTTP

### Schéma complet

L'idempotency key permet à un client de retenter une requête en toute sécurité : si la requête a déjà été traitée, le serveur renvoie la même réponse sans réexécuter l'opération.

```typescript
import { Redis } from 'ioredis';
import { Request, Response, NextFunction } from 'express';
import crypto from 'crypto';

const redis = new Redis();
const IDEMPOTENCY_TTL = 86400; // 24h

interface CachedResponse {
  statusCode: number;
  body: unknown;
  headers: Record<string, string>;
}

async function idempotencyMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  // Uniquement pour les mutations
  if (!['POST', 'PUT', 'PATCH', 'DELETE'].includes(req.method)) {
    return next();
  }

  const idempotencyKey = req.headers['idempotency-key'] as string | undefined;
  if (!idempotencyKey) {
    return next();
  }

  // Scoping de la clé : user + opération + clé fournie
  const userId = (req as { user?: { id: string } }).user?.id ?? 'anonymous';
  const scopedKey = `idempotency:${userId}:${req.path}:${idempotencyKey}`;

  // Vérifier si la réponse est en cache
  const cached = await redis.get(scopedKey);
  if (cached) {
    const { statusCode, body, headers }: CachedResponse = JSON.parse(cached);

    // Replay de la réponse originale
    res.set(headers);
    res.set('X-Idempotency-Replayed', 'true');
    res.status(statusCode).json(body);
    return;
  }

  // Intercept la réponse pour la mettre en cache
  const originalJson = res.json.bind(res);
  res.json = (body: unknown) => {
    const responseToCache: CachedResponse = {
      statusCode: res.statusCode,
      body,
      headers: {
        'content-type': res.getHeader('content-type') as string ?? 'application/json',
      },
    };

    // Sauvegarder en background (ne pas bloquer la réponse)
    redis
      .set(scopedKey, JSON.stringify(responseToCache), 'EX', IDEMPOTENCY_TTL)
      .catch((err) => logger.error({ err }, 'Failed to cache idempotency response'));

    return originalJson(body);
  };

  next();
}
```

---

## Circuit Breaker — Implémentation Complète

### Machine d'états

```
CLOSED ──(N échecs en T secondes)──→ OPEN
  ↑                                    |
  └── (M succès en HALF-OPEN) ──← HALF-OPEN ←── (timeout écoulé)
```

### Implémentation avec état persisté dans Redis (multi-instances)

```typescript
import { Redis } from 'ioredis';

type CircuitState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

interface CircuitBreakerConfig {
  name: string;
  failureThreshold: number;   // nb échecs pour passer OPEN
  successThreshold: number;   // nb succès en HALF_OPEN pour revenir CLOSED
  timeout: number;            // ms avant de passer OPEN → HALF_OPEN
  windowMs: number;           // fenêtre glissante pour compter les échecs
  redis: Redis;
}

class DistributedCircuitBreaker {
  private config: CircuitBreakerConfig;

  constructor(config: CircuitBreakerConfig) {
    this.config = config;
  }

  private key(suffix: string): string {
    return `circuit:${this.config.name}:${suffix}`;
  }

  async getState(): Promise<CircuitState> {
    const state = await this.config.redis.get(this.key('state'));
    return (state as CircuitState | null) ?? 'CLOSED';
  }

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    const state = await this.getState();

    if (state === 'OPEN') {
      // Vérifier si le timeout est écoulé → passer en HALF_OPEN
      const openedAt = await this.config.redis.get(this.key('opened_at'));
      if (openedAt && Date.now() - parseInt(openedAt) > this.config.timeout) {
        await this.transitionTo('HALF_OPEN');
      } else {
        throw new CircuitOpenError(`Circuit breaker ${this.config.name} is OPEN`);
      }
    }

    try {
      const result = await fn();
      await this.recordSuccess();
      return result;
    } catch (err) {
      await this.recordFailure();
      throw err;
    }
  }

  private async recordSuccess(): Promise<void> {
    const state = await this.getState();

    if (state === 'HALF_OPEN') {
      const successes = await this.config.redis.incr(this.key('half_open_successes'));
      if (successes >= this.config.successThreshold) {
        await this.transitionTo('CLOSED');
        await this.config.redis.del(
          this.key('failures'),
          this.key('half_open_successes')
        );
      }
    }
  }

  private async recordFailure(): Promise<void> {
    const state = await this.getState();

    if (state === 'HALF_OPEN') {
      // Un seul échec en HALF_OPEN → retour OPEN immédiat
      await this.transitionTo('OPEN');
      return;
    }

    // Compteur d'échecs avec expiration sur la fenêtre glissante
    const pipeline = this.config.redis.pipeline();
    pipeline.incr(this.key('failures'));
    pipeline.expire(this.key('failures'), Math.ceil(this.config.windowMs / 1000));
    const results = await pipeline.exec();

    const failures = (results?.[0]?.[1] as number) ?? 0;
    if (failures >= this.config.failureThreshold) {
      await this.transitionTo('OPEN');
    }
  }

  private async transitionTo(state: CircuitState): Promise<void> {
    const pipeline = this.config.redis.pipeline();
    pipeline.set(this.key('state'), state);

    if (state === 'OPEN') {
      pipeline.set(this.key('opened_at'), Date.now().toString());
    }

    await pipeline.exec();
    logger.info({ circuit: this.config.name, state }, 'Circuit state transition');
  }
}

class CircuitOpenError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'CircuitOpenError';
  }
}

// Usage
const circuitBreaker = new DistributedCircuitBreaker({
  name: 'payment-service',
  failureThreshold: 5,
  successThreshold: 2,
  timeout: 60000,     // 1 minute en OPEN avant de tenter HALF_OPEN
  windowMs: 30000,    // 5 échecs en 30 secondes → OPEN
  redis,
});

const result = await circuitBreaker.execute(() => callPaymentService(order));
```

---

## Bulkhead Pattern — Isolation des Ressources

Le Bulkhead isole les pools de ressources entre les différents services appelés. Si le service Rapports consomme toutes les connexions HTTP disponibles, les autres services continuent de fonctionner normalement.

```typescript
import pLimit from 'p-limit';

// Un semaphore par service — isolation stricte
const limiters = {
  paymentService:  pLimit(10), // max 10 appels concurrents
  inventoryService: pLimit(20),
  reportingService: pLimit(2), // le service lent est strictement limité
  notificationService: pLimit(50),
};

type ServiceName = keyof typeof limiters;

async function callService<T>(
  serviceName: ServiceName,
  fn: () => Promise<T>
): Promise<T> {
  const limiter = limiters[serviceName];

  if (limiter.pendingCount > 50) {
    // Queue trop longue → fail fast plutôt que d'accumuler
    throw new BulkheadRejectedError(`Bulkhead full for ${serviceName}`);
  }

  return limiter(fn);
}

// Usage
const [payment, inventory] = await Promise.all([
  callService('paymentService', () => processPayment(order)),
  callService('inventoryService', () => reserveStock(order.items)),
]);
```

---

## Timeout Patterns et Deadline Propagation

### Timeout avec AbortController

```typescript
async function withTimeout<T>(
  fn: (signal: AbortSignal) => Promise<T>,
  timeoutMs: number,
  timeoutMessage = 'Operation timed out'
): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fn(controller.signal);
  } catch (err) {
    if (controller.signal.aborted) {
      throw new TimeoutError(timeoutMessage);
    }
    throw err;
  } finally {
    clearTimeout(timer);
  }
}

// Deadline propagation : réduire le timeout à chaque appel descendant
interface RequestContext {
  deadlineMs: number;
  correlationId: string;
}

async function callWithDeadline<T>(
  ctx: RequestContext,
  fn: (signal: AbortSignal) => Promise<T>
): Promise<T> {
  const remaining = ctx.deadlineMs - Date.now();

  if (remaining <= 0) {
    throw new TimeoutError('Deadline already exceeded');
  }

  return withTimeout(fn, remaining);
}
```

---

## Health Checks — Liveness vs Readiness

### Distinction fondamentale

- **Liveness** (`/health/live`) : le service est-il en vie ? Si non, Kubernetes redémarre le pod. Ne jamais inclure les dépendances — un service doit se redémarrer uniquement si lui-même est cassé, pas si sa DB est lente.
- **Readiness** (`/health/ready`) : le service est-il prêt à recevoir du trafic ? Si non, Kubernetes retire le pod des endpoints du Service. Inclure les dépendances critiques.

```typescript
import express from 'express';
import { Pool } from 'pg';
import { Redis } from 'ioredis';

const app = express();

// Liveness : simple et rapide
app.get('/health/live', (_req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Readiness : vérifie les dépendances critiques
app.get('/health/ready', async (_req, res) => {
  const checks = await Promise.allSettled([
    checkDatabase(pool),
    checkRedis(redis),
  ]);

  const results = {
    database: checks[0].status === 'fulfilled',
    redis: checks[1].status === 'fulfilled',
  };

  const isReady = Object.values(results).every(Boolean);

  res.status(isReady ? 200 : 503).json({
    status: isReady ? 'ready' : 'not_ready',
    checks: results,
  });
});

async function checkDatabase(pool: Pool): Promise<void> {
  const client = await pool.connect();
  try {
    await client.query('SELECT 1');
  } finally {
    client.release();
  }
}

async function checkRedis(redis: Redis): Promise<void> {
  await redis.ping();
}
```

---

## Rate Limiting Distribué

### Token Bucket en Lua Redis

```typescript
const TOKEN_BUCKET_SCRIPT = `
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])  -- tokens par seconde
local requested = tonumber(ARGV[3])
local now = tonumber(ARGV[4])

local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
local tokens = tonumber(bucket[1]) or capacity
local last_refill = tonumber(bucket[2]) or now

-- Recalculer les tokens disponibles depuis le dernier refill
local elapsed = (now - last_refill) / 1000  -- en secondes
local new_tokens = math.min(capacity, tokens + elapsed * refill_rate)

if new_tokens >= requested then
  redis.call('HMSET', key, 'tokens', new_tokens - requested, 'last_refill', now)
  redis.call('EXPIRE', key, 3600)
  return 1  -- autorisé
else
  redis.call('HMSET', key, 'tokens', new_tokens, 'last_refill', now)
  redis.call('EXPIRE', key, 3600)
  return 0  -- rejeté
end
`;

async function checkRateLimit(
  redis: Redis,
  userId: string,
  endpoint: string,
  capacity: number,
  refillRatePerSecond: number
): Promise<boolean> {
  const key = `rate_limit:${userId}:${endpoint}`;
  const result = await redis.eval(
    TOKEN_BUCKET_SCRIPT,
    1,
    key,
    capacity.toString(),
    refillRatePerSecond.toString(),
    '1',
    Date.now().toString()
  );
  return result === 1;
}

// Middleware Express
function rateLimitMiddleware(capacity: number, refillRate: number) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const userId = (req as { user?: { id: string } }).user?.id ?? req.ip ?? 'anonymous';
    const allowed = await checkRateLimit(redis, userId, req.path, capacity, refillRate);

    if (!allowed) {
      res.status(429).json({
        error: 'Too Many Requests',
        retryAfter: Math.ceil(1 / refillRate),
      });
      return;
    }

    next();
  };
}
```

---

## Chaos Engineering

### Principes fondamentaux

1. **Définir l'état stable.** Choisir une métrique de santé (taux d'erreur < 0.1%, p99 latence < 500ms, SLO 99.9%). L'hypothèse est que le système maintient cet état stable face à une perturbation.
2. **Formuler l'hypothèse.** "Si le service Inventaire perd 20% de ses requêtes, le taux d'erreur global reste < 0.1%."
3. **Injecter le chaos en production (avec blast radius minimal).** Commencer par les environnements de staging, puis production avec canary (5% du trafic).
4. **Observer.** Comparer le groupe de contrôle et le groupe expérimental sur la métrique d'état stable.
5. **Automatiser.** Les tests de chaos en CI préviennent les régressions de résilience.

### Tests de chaos automatisés avec `chaos-mesh` (Kubernetes)

```yaml
# pod-failure.yaml — tuer 30% des pods du service inventory aléatoirement
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: inventory-pod-failure
  namespace: chaos-testing
spec:
  action: pod-failure
  mode: fixed-percent
  value: "30"
  duration: "5m"
  selector:
    namespaces:
      - production
    labelSelectors:
      app: inventory-service
  scheduler:
    cron: "@every 1h"
```

```yaml
# network-delay.yaml — ajouter 200ms de latence réseau sur le service Rapports
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: reporting-network-delay
spec:
  action: delay
  mode: all
  selector:
    labelSelectors:
      app: reporting-service
  delay:
    latency: "200ms"
    correlation: "25"
    jitter: "50ms"
  duration: "10m"
```

---

## Distributed Tracing — Propagation du Contexte

### W3C TraceContext et Correlation ID dans Kafka

```typescript
import { trace, context, propagation } from '@opentelemetry/api';
import { W3CTraceContextPropagator } from '@opentelemetry/core';

const propagator = new W3CTraceContextPropagator();

// Injecter le contexte de trace dans les headers Kafka
function injectTraceContext(): Record<string, string> {
  const carrier: Record<string, string> = {};
  propagator.inject(context.active(), carrier, {
    set: (carrier, key, value) => { carrier[key] = value; },
  });
  return carrier;
}

// Extraire et restaurer le contexte de trace depuis les headers Kafka
function extractTraceContext(headers: Record<string, Buffer | string>): ReturnType<typeof context.active> {
  const carrier: Record<string, string> = {};
  for (const [key, value] of Object.entries(headers)) {
    carrier[key] = value.toString();
  }
  return propagator.extract(context.active(), carrier, {
    get: (carrier, key) => carrier[key],
    keys: (carrier) => Object.keys(carrier),
  });
}

// Dans le consumer Kafka
await consumer.run({
  eachMessage: async ({ message }) => {
    const headers = message.headers as Record<string, Buffer>;
    const parentContext = extractTraceContext(headers);

    await context.with(parentContext, async () => {
      const span = trace.getTracer('order-processor').startSpan('process-order');
      try {
        await processOrder(JSON.parse(message.value!.toString()));
        span.setStatus({ code: SpanStatusCode.OK });
      } catch (err) {
        span.recordException(err as Error);
        span.setStatus({ code: SpanStatusCode.ERROR });
        throw err;
      } finally {
        span.end();
      }
    });
  },
});
```

---

## SLO et Error Budget

### Définir les SLOs pour un système distribué

| SLI | SLO | Fenêtre |
|---|---|---|
| Disponibilité (requêtes réussies / total) | ≥ 99.9% | 30 jours glissants |
| Latence p99 | ≤ 500ms | 1h |
| Taux d'erreur (5xx) | ≤ 0.1% | 1h |
| Fraîcheur des données (lag max Kafka) | ≤ 30s | 5min |

### Alerte sur la burn rate de l'error budget

```yaml
# prometheus-rules.yaml
groups:
  - name: error_budget
    rules:
      - alert: ErrorBudgetBurnRateCritical
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[1h]))
            /
            sum(rate(http_requests_total[1h]))
          ) > 14.4 * 0.001
        # 14.4x burn rate = budget épuisé en 2h si ça continue
        for: 5m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "Error budget burn rate critique"
          description: |
            Le budget d'erreur est consommé 14.4x plus vite que prévu.
            À ce rythme, le budget du mois sera épuisé en 2 heures.
```

L'alerte multi-fenêtre (1h + 6h) est recommandée pour éviter les faux positifs sur des pics courts : la fenêtre courte détecte les incidents sévères rapidement, la fenêtre longue détecte les dégradations progressives.
