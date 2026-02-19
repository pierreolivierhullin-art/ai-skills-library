# Architecture File d'Attente — BullMQ, Rate Limiting et Gestion des Erreurs

> Référence complète pour architecturer l'envoi d'emails en mode asynchrone. Couvre BullMQ en configuration avancée, le rate limiting par destinataire, la dead-letter queue, le dashboard Bull Board, les stratégies de retry, la gestion des bounces et suppressions, le batching, le monitoring et le pattern Outbox.

---

## BullMQ — Configuration Avancée

### Connexion Redis et pool de connexions

```typescript
// lib/redis.ts — Configuration Redis pour BullMQ
import { Redis } from 'ioredis';

// BullMQ nécessite une connexion Redis dédiée avec maxRetriesPerRequest: null
export const redisConnection = new Redis({
  host: process.env.REDIS_HOST ?? 'localhost',
  port: parseInt(process.env.REDIS_PORT ?? '6379'),
  password: process.env.REDIS_PASSWORD,
  tls: process.env.REDIS_TLS === 'true' ? {} : undefined,
  maxRetriesPerRequest: null,  // Obligatoire pour BullMQ
  enableReadyCheck: false,
  retryStrategy: (times: number) => Math.min(times * 50, 2000),
  lazyConnect: true,
});

// Connexion séparée pour les operations non-BullMQ
export const redis = new Redis({
  host: process.env.REDIS_HOST ?? 'localhost',
  port: parseInt(process.env.REDIS_PORT ?? '6379'),
  password: process.env.REDIS_PASSWORD,
  tls: process.env.REDIS_TLS === 'true' ? {} : undefined,
});
```

### Définition complète des queues

```typescript
// queues/definitions.ts
import { Queue, QueueOptions } from 'bullmq';
import { redisConnection } from '../lib/redis';

const defaultQueueOptions: QueueOptions = {
  connection: redisConnection,
  defaultJobOptions: {
    removeOnComplete: {
      age: 24 * 60 * 60,    // Garder les jobs réussis pendant 24h
      count: 1000,          // Maximum 1000 jobs réussis en queue
    },
    removeOnFail: {
      age: 7 * 24 * 60 * 60, // Garder les échecs pendant 7 jours
      count: 5000,
    },
  },
};

// Queue emails transactionnels (confirmations, réinitialisations, factures)
export const transactionalQueue = new Queue('email:transactional', {
  ...defaultQueueOptions,
  defaultJobOptions: {
    ...defaultQueueOptions.defaultJobOptions,
    attempts: 5,
    backoff: { type: 'exponential', delay: 5000 },
    priority: 1,  // Priorité haute (1 = max)
  },
});

// Queue emails marketing (newsletters, campagnes)
export const marketingQueue = new Queue('email:marketing', {
  ...defaultQueueOptions,
  defaultJobOptions: {
    ...defaultQueueOptions.defaultJobOptions,
    attempts: 3,
    backoff: { type: 'exponential', delay: 30000 },
    priority: 10, // Priorité basse
  },
});

// Queue emails systèmes (alertes, rapports internes)
export const systemQueue = new Queue('email:system', {
  ...defaultQueueOptions,
  defaultJobOptions: {
    ...defaultQueueOptions.defaultJobOptions,
    attempts: 3,
    backoff: { type: 'fixed', delay: 10000 },
    priority: 5,
  },
});

// Dead-letter queue pour les jobs définitivement échoués
export const dlqQueue = new Queue('email:dlq', {
  ...defaultQueueOptions,
  defaultJobOptions: {
    removeOnComplete: false,  // Garder indéfiniment pour audit
    removeOnFail: false,
  },
});
```

### Jobs planifiés et récurrents

```typescript
// Envoi différé d'un email
await transactionalQueue.add(
  'email:relance-panier',
  { userId: 'usr_123', panier: cartData },
  {
    delay: 60 * 60 * 1000,  // Dans 1 heure
    jobId: `relance-panier:usr_123:${Date.now()}`, // ID unique pour éviter les doublons
  }
);

// Email récurrent avec cron (digest quotidien à 9h)
await marketingQueue.add(
  'digest:quotidien',
  { type: 'digest' },
  {
    repeat: {
      pattern: '0 9 * * 1-5',  // Lundi–vendredi à 9h00
      tz: 'Europe/Paris',
    },
    jobId: 'digest:quotidien:recurring',
  }
);

// Job avec dépendances (Flow) — email de facture après confirmation de paiement
import { FlowProducer } from 'bullmq';

const flow = new FlowProducer({ connection: redisConnection });

await flow.add({
  name: 'envoyer-facture',
  queueName: 'email:transactional',
  data: { userId: 'usr_123', montant: 99.90 },
  children: [
    {
      name: 'générer-pdf-facture',
      queueName: 'documents:generation',
      data: { type: 'facture', userId: 'usr_123' },
    },
  ],
});
```

---

## Rate Limiting par Destinataire

### Sliding window avec RateLimiterRedis

```typescript
// lib/rate-limiter.ts
import { RateLimiterRedis } from 'rate-limiter-flexible';
import { redis } from './redis';

// Limiter à 3 emails par utilisateur par heure (prévenir le spam accidentel)
export const rateLimiterParUtilisateur = new RateLimiterRedis({
  storeClient: redis,
  keyPrefix: 'ratelimit:email:user',
  points: 3,        // 3 emails
  duration: 3600,   // par heure
  blockDuration: 0, // ne pas bloquer, juste refuser
});

// Limiter par domaine destinataire (respecter les limites des ESPs)
export const rateLimiterParDomaine = new RateLimiterRedis({
  storeClient: redis,
  keyPrefix: 'ratelimit:email:domain',
  points: 100,      // 100 emails
  duration: 60,     // par minute
  blockDuration: 0,
});

// Limiter le débit global vers l'ESP (Resend : 100 req/s)
export const rateLimiterESP = new RateLimiterRedis({
  storeClient: redis,
  keyPrefix: 'ratelimit:esp:resend',
  points: 100,
  duration: 1,      // 100 par seconde
  blockDuration: 10, // Bloquer 10s si dépassement
});
```

### Limites spécifiques par domaine

```typescript
// Limites connues des principaux domaines (emails/jour)
const LIMITES_DOMAINE: Record<string, number> = {
  'gmail.com': 2000,
  'googlemail.com': 2000,
  'yahoo.com': 500,
  'yahoo.fr': 500,
  'hotmail.com': 500,
  'outlook.com': 500,
  'live.com': 500,
  'icloud.com': 200,
};

async function vérifierLimiteDomaine(email: string): Promise<boolean> {
  const domaine = email.split('@')[1].toLowerCase();
  const limite = LIMITES_DOMAINE[domaine] ?? 10000; // Défaut libéral pour domaines inconnus

  const limiterDomaine = new RateLimiterRedis({
    storeClient: redis,
    keyPrefix: 'ratelimit:domain',
    points: limite,
    duration: 86400, // 24 heures
  });

  try {
    await limiterDomaine.consume(domaine);
    return true; // Autorisé
  } catch {
    return false; // Limite atteinte
  }
}
```

### Token bucket vs sliding window

```
Sliding window (RateLimiterRedis par défaut) :
  ✓ Plus précis — compte les requêtes dans une fenêtre glissante
  ✓ Pas de "burst" en début de fenêtre
  ✗ Plus coûteux en mémoire Redis

Token bucket :
  ✓ Permet les micro-bursts (ex: 10 emails en 1s puis attendre)
  ✓ Meilleur pour les systèmes qui "rechargent" les tokens
  ✗ Fenêtre fixe peut permettre 2x le débit à la jonction

Recommandation : sliding window pour les limites par utilisateur,
token bucket pour le rate limiting vers l'ESP (où les bursts sont naturels).
```

---

## Dead-Letter Queue (DLQ)

### Déplacer les jobs définitivement échoués

```typescript
// workers/email.worker.ts — Gestion des échecs définitifs
import { Worker, Job } from 'bullmq';
import { dlqQueue } from '../queues/definitions';

const emailWorker = new Worker(
  'email:transactional',
  async (job: Job) => {
    // ... logique d'envoi
  },
  {
    connection: redisConnection,
    concurrency: 20,
  }
);

emailWorker.on('failed', async (job: Job | undefined, error: Error) => {
  if (!job) return;

  const maxAttempts = job.opts.attempts ?? 3;
  const estDéfinitif = job.attemptsMade >= maxAttempts;

  if (estDéfinitif) {
    // Déplacer vers la DLQ pour audit et replay manuel
    await dlqQueue.add(
      'échec-définitif',
      {
        jobId: job.id,
        queue: job.queueName,
        données: job.data,
        erreur: {
          message: error.message,
          stack: error.stack,
          code: (error as NodeJS.ErrnoException).code,
        },
        tentatives: job.attemptsMade,
        échouéÀ: new Date().toISOString(),
      },
      {
        jobId: `dlq:${job.id}:${Date.now()}`,
      }
    );

    // Alerter l'équipe
    await envoyerAlerteSlack({
      canal: '#alertes-email',
      message: `Email définitivement échoué après ${job.attemptsMade} tentatives`,
      détails: { jobId: job.id, destinataire: job.data.to, erreur: error.message },
    });

    // Enregistrer dans la base pour audit
    await db.emailÉchecs.créer({
      jobId: job.id!,
      destinataire: job.data.to,
      type: job.data.type,
      erreur: error.message,
      tentatives: job.attemptsMade,
    });
  }
});
```

### Replay manuel des jobs DLQ

```typescript
// scripts/replay-dlq.ts — Rejouer les jobs échoués après correction
async function rejouerDLQ(filtres: {
  depuis?: Date;
  type?: string;
  limite?: number;
}): Promise<void> {
  const jobs = await dlqQueue.getJobs(['waiting', 'failed'], 0, filtres.limite ?? 100);

  let rejoués = 0;
  let ignorés = 0;

  for (const job of jobs) {
    // Filtrer par date si spécifié
    if (filtres.depuis && new Date(job.data.échouéÀ) < filtres.depuis) {
      ignorés++;
      continue;
    }

    // Filtrer par type d'email
    if (filtres.type && job.data.données.type !== filtres.type) {
      ignorés++;
      continue;
    }

    // Remettre dans la queue originale
    const queueCible = job.data.queue === 'email:transactional'
      ? transactionalQueue
      : marketingQueue;

    await queueCible.add(
      job.data.données.type ?? 'replay',
      job.data.données,
      {
        jobId: `replay:${job.data.jobId}:${Date.now()}`,
        priority: 2, // Légèrement prioritaire
      }
    );

    // Supprimer de la DLQ après replay
    await job.remove();
    rejoués++;
  }

  console.log(`DLQ replay terminé : ${rejoués} rejoués, ${ignorés} ignorés`);
}
```

---

## Bull Board — Dashboard UI

### Intégration avec Next.js App Router

```typescript
// app/api/queues/route.ts (Next.js App Router)
import { createBullBoard } from '@bull-board/api';
import { BullMQAdapter } from '@bull-board/api/bullMQAdapter';
import { NextAdapter } from '@bull-board/next';
import { transactionalQueue, marketingQueue, systemQueue, dlqQueue } from '../../../../queues/definitions';

const serverAdapter = new NextAdapter();
serverAdapter.setBasePath('/api/queues');

createBullBoard({
  queues: [
    new BullMQAdapter(transactionalQueue, { readOnlyMode: false }),
    new BullMQAdapter(marketingQueue, { readOnlyMode: false }),
    new BullMQAdapter(systemQueue, { readOnlyMode: false }),
    new BullMQAdapter(dlqQueue, { readOnlyMode: false, description: 'Dead-Letter Queue' }),
  ],
  serverAdapter,
  options: {
    uiConfig: {
      boardTitle: 'Email Queue Dashboard',
      boardLogo: { path: '/logo.png', width: 100 },
    },
  },
});

export const { GET, POST } = serverAdapter.registerHandlers();
```

### Authentification du dashboard

```typescript
// middleware.ts — Protéger l'accès à Bull Board
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith('/api/queues')) {
    // Vérifier l'authentification admin
    const authHeader = request.headers.get('authorization');

    if (!authHeader || !vérifierTokenAdmin(authHeader)) {
      return new NextResponse('Non autorisé', {
        status: 401,
        headers: { 'WWW-Authenticate': 'Basic realm="Queue Dashboard"' },
      });
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/api/queues/:path*'],
};
```

---

## Retry Strategies

### Exponential backoff avec jitter

```typescript
// Éviter le "thundering herd" : ajouter du jitter (délai aléatoire)
// Sans jitter : tous les jobs échoués reessaient en même temps
// Avec jitter : dispersion temporelle des retries

function calculerDélaiAvecJitter(tentative: number, délaiBase: number = 5000): number {
  const délaiExponentiel = délaiBase * Math.pow(2, tentative - 1);
  const délaiMax = délaiBase * Math.pow(2, 5); // Cap à 32x le délai de base

  // Full jitter : délai aléatoire entre 0 et le délai exponentiel
  const délaiAvecJitter = Math.random() * Math.min(délaiExponentiel, délaiMax);

  return Math.floor(délaiAvecJitter);
}

// Configuration BullMQ avec backoff personnalisé
await transactionalQueue.add('email', données, {
  attempts: 5,
  backoff: {
    type: 'custom',
    // BullMQ ne supporte pas le jitter natif — utiliser un wrapper
  },
});

// Alternative : utiliser un backoff dans le worker lui-même
emailWorker.on('failed', async (job, error) => {
  if (job && job.attemptsMade < (job.opts.attempts ?? 5)) {
    const délai = calculerDélaiAvecJitter(job.attemptsMade);
    await job.retry({ delay: délai });
  }
});
```

### Stratégie de retry par type d'email

```typescript
const stratégiesRetry: Record<string, { attempts: number; backoff: object }> = {
  // Critique — confirmation, réinitialisation : retry agressif
  CONFIRMATION: { attempts: 7, backoff: { type: 'exponential', delay: 2000 } },
  RÉINITIALISATION: { attempts: 7, backoff: { type: 'exponential', delay: 2000 } },

  // Important — facture : retry modéré
  FACTURE: { attempts: 5, backoff: { type: 'exponential', delay: 10000 } },

  // Non critique — newsletter : retry limité
  NEWSLETTER: { attempts: 2, backoff: { type: 'fixed', delay: 60000 } },

  // Notification : retry minimal
  NOTIFICATION: { attempts: 3, backoff: { type: 'exponential', delay: 5000 } },
};
```

---

## Gestion des Bounces et Suppressions

### Schéma de suppression PostgreSQL

```sql
-- Table de suppression des emails (respect RGPD + bounces)
CREATE TABLE email_suppressions (
  id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email      TEXT NOT NULL,
  raison     TEXT NOT NULL CHECK (raison IN (
               'HARD_BOUNCE', 'SOFT_BOUNCE_PERSISTANT',
               'PLAINTE_SPAM', 'PLAINTE_FBL', 'DÉSABONNEMENT',
               'RGPD_SUPPRESSION', 'FRAUDE', 'ADMIN'
             )),
  source     TEXT,             -- 'resend_webhook', 'yahoo_fbl', 'utilisateur', etc.
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMPTZ,      -- NULL = permanent
  metadata   JSONB DEFAULT '{}'
);

-- Index pour lookup rapide avant envoi
CREATE UNIQUE INDEX idx_suppressions_email ON email_suppressions (email)
  WHERE expires_at IS NULL OR expires_at > NOW();

CREATE INDEX idx_suppressions_email_actif ON email_suppressions (email, created_at DESC)
  WHERE expires_at IS NULL OR expires_at > NOW();
```

### Vérification avant envoi

```typescript
// lib/suppression.ts
async function estSupprimé(email: string): Promise<boolean> {
  const résultat = await db.query<{ count: number }>(
    `SELECT COUNT(*) as count
     FROM email_suppressions
     WHERE email = $1
       AND (expires_at IS NULL OR expires_at > NOW())`,
    [email.toLowerCase()]
  );

  return résultat.rows[0].count > 0;
}

// Dans le worker — vérifier AVANT d'envoyer
async function processerJob(job: Job): Promise<void> {
  const { to, type, données } = job.data;

  // Vérification suppression
  if (await estSupprimé(to)) {
    logger.info({ email: to, jobId: job.id }, 'Email ignoré (liste de suppression)');
    return; // Terminer normalement — ne pas rejeter (évite le retry)
  }

  // Envoi
  await resend.emails.send({ to, ...données });
}
```

### Traitement RGPD — Droit à l'oubli

```typescript
// Lors d'une demande de suppression RGPD
async function exécuterDroitÀLOubli(userId: string): Promise<void> {
  const utilisateur = await db.users.findById(userId);
  if (!utilisateur) return;

  // 1. Ajouter à la liste de suppression permanente
  await db.emailSuppressions.créer({
    email: utilisateur.email,
    raison: 'RGPD_SUPPRESSION',
    source: 'rgpd_request',
    metadata: { userId, requestedAt: new Date() },
  });

  // 2. Annuler tous les jobs en attente
  const jobsEnAttente = await transactionalQueue.getJobs(['waiting', 'delayed']);
  for (const job of jobsEnAttente) {
    if (job.data.to === utilisateur.email) {
      await job.remove();
    }
  }

  // 3. Anonymiser les logs d'envoi
  await db.emailLogs.anonymiser(utilisateur.email);

  logger.info({ userId, email: utilisateur.email }, 'RGPD suppression traitée');
}
```

---

## Email Batching

### Diviser les bulk sends en batches

```typescript
// services/bulk-email.service.ts
interface BulkEmailOptions {
  template: string;
  données: Array<{ email: string; variables: Record<string, unknown> }>;
  délaiEntreEnvois?: number; // ms entre chaque email
}

async function envoyerBulkEmail(options: BulkEmailOptions): Promise<void> {
  const TAILLE_BATCH = 100; // 100 jobs ajoutés à la queue par lot
  const { données, template } = options;

  // Filtrer les suppressions en batch (une seule requête DB)
  const emailsSupprimés = await db.emailSuppressions.trouverParmis(
    données.map(d => d.email)
  );
  const donnéesFiltérées = données.filter(d => !emailsSupprimés.has(d.email));

  // Diviser en batches
  for (let i = 0; i < donnéesFiltérées.length; i += TAILLE_BATCH) {
    const batch = donnéesFiltérées.slice(i, i + TAILLE_BATCH);

    // Ajouter le batch à la queue avec un délai progressif
    const jobsBatch = batch.map((destinataire, indexLot) => ({
      name: `bulk:${template}`,
      data: { to: destinataire.email, template, variables: destinataire.variables },
      opts: {
        delay: i * 10 + indexLot * 50,  // Étaler les envois dans le temps
        attempts: 2,
        jobId: `bulk:${template}:${destinataire.email}:${Date.now()}`,
      },
    }));

    await marketingQueue.addBulk(jobsBatch);
    logger.info(`Batch ${Math.floor(i / TAILLE_BATCH) + 1} ajouté : ${batch.length} emails`);
  }
}
```

### Adaptive throttling

```typescript
// Circuit breaker pour ralentir si l'ESP signale des erreurs
class EmailCircuitBreaker {
  private erreurs = 0;
  private readonly seuilOuverture = 10;  // Ouvrir si 10 erreurs en 60s
  private readonly fenêtreTemps = 60000;  // 60 secondes
  private ouvert = false;
  private minuteurFermeture?: NodeJS.Timeout;

  async exécuter<T>(fn: () => Promise<T>): Promise<T> {
    if (this.ouvert) {
      throw new Error('Circuit breaker ouvert — ESP indisponible, retry dans 30s');
    }

    try {
      const résultat = await fn();
      this.erreurs = Math.max(0, this.erreurs - 1); // Décroissance graduelle
      return résultat;
    } catch (error) {
      this.erreurs++;
      if (this.erreurs >= this.seuilOuverture) {
        this.ouvrir();
      }
      throw error;
    }
  }

  private ouvrir(): void {
    this.ouvert = true;
    this.erreurs = 0;
    logger.error('Circuit breaker OUVERT — pause des envois email 30s');

    this.minuteurFermeture = setTimeout(() => {
      this.ouvert = false;
      logger.info('Circuit breaker FERMÉ — reprise des envois');
    }, 30000);
  }
}

export const emailCircuitBreaker = new EmailCircuitBreaker();
```

---

## Monitoring des Queues

### Métriques Datadog / Grafana

```typescript
// lib/queue-metrics.ts — Exporter les métriques des queues
import StatsD from 'hot-shots';

const statsd = new StatsD({ prefix: 'email.queue.' });

async function exporterMétriquesQueue(queue: Queue): Promise<void> {
  const [waiting, active, completed, failed, delayed] = await Promise.all([
    queue.getWaitingCount(),
    queue.getActiveCount(),
    queue.getCompletedCount(),
    queue.getFailedCount(),
    queue.getDelayedCount(),
  ]);

  const queueNom = queue.name.replace(':', '_');

  statsd.gauge(`${queueNom}.waiting`, waiting);
  statsd.gauge(`${queueNom}.active`, active);
  statsd.gauge(`${queueNom}.completed`, completed);
  statsd.gauge(`${queueNom}.failed`, failed);
  statsd.gauge(`${queueNom}.delayed`, delayed);

  // Alerte si trop de jobs en attente
  if (waiting > 10000) {
    logger.warn({ queue: queue.name, waiting }, 'Queue saturée');
    await envoyerAlerteSlack({ canal: '#alertes-email', message: `Queue ${queue.name} saturée (${waiting} en attente)` });
  }
}

// Surveiller toutes les queues toutes les 30 secondes
setInterval(async () => {
  await Promise.all([
    exporterMétriquesQueue(transactionalQueue),
    exporterMétriquesQueue(marketingQueue),
    exporterMétriquesQueue(dlqQueue),
  ]);
}, 30000);
```

### Détection des stalled jobs

```typescript
// Les "stalled jobs" sont des jobs actifs dont le worker a crashé sans signaler la fin
// BullMQ les détecte automatiquement et les replace en waiting

const emailWorker = new Worker(
  'email:transactional',
  processerJob,
  {
    connection: redisConnection,
    stalledInterval: 30000,    // Vérifier les stalled jobs toutes les 30s
    maxStalledCount: 2,        // Retry 2x avant de marquer comme échoué
    lockDuration: 60000,       // Durée du lock job (doit être > temps max de traitement)
  }
);

emailWorker.on('stalled', (jobId: string) => {
  logger.warn({ jobId }, 'Job stalled détecté — sera réessayé automatiquement');
});
```

---

## Outbox Pattern — Garantie d'Envoi Transactionnel

### Problème : email envoyé mais transaction annulée (ou vice-versa)

```typescript
// PROBLÈME : race condition entre DB et envoi email
async function créerUtilisateur(données: CreateUserData): Promise<User> {
  const user = await db.users.créer(données);
  // Si le processus crash ici → utilisateur créé sans email de bienvenue
  await resend.emails.send({ to: user.email, ... });
  return user;
  // Si l'envoi échoue → utilisateur créé sans email reçu
}
```

### Solution : pattern Outbox avec garantie at-least-once

```typescript
// SOLUTION : Outbox pattern — l'email est enregistré dans la même transaction DB
// puis envoyé de façon asynchrone par un worker séparé

// 1. Créer la table outbox
// CREATE TABLE email_outbox (
//   id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
//   type         TEXT NOT NULL,
//   payload      JSONB NOT NULL,
//   created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
//   scheduled_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
//   sent_at      TIMESTAMPTZ,
//   error        TEXT,
//   attempts     INT NOT NULL DEFAULT 0
// );

// 2. Écrire dans l'outbox dans la même transaction que la création
async function créerUtilisateurAvecOutbox(données: CreateUserData): Promise<User> {
  return await db.transaction(async (tx) => {
    // Créer l'utilisateur
    const user = await tx.users.créer(données);

    // Enregistrer l'email à envoyer dans la même transaction
    await tx.emailOutbox.créer({
      type: 'BIENVENUE',
      payload: {
        destinataire: user.email,
        prénom: user.prénom,
        userId: user.id,
      },
    });

    return user;
    // Si la transaction échoue → ni l'utilisateur ni l'outbox ne sont créés ✓
    // Si la transaction réussit → les deux sont créés atomiquement ✓
  });
}

// 3. Worker qui lit l'outbox et envoie les emails
async function processerOutbox(): Promise<void> {
  // Sélectionner et verrouiller les emails à envoyer (FOR UPDATE SKIP LOCKED)
  const emails = await db.query(
    `SELECT * FROM email_outbox
     WHERE sent_at IS NULL
       AND attempts < 5
       AND scheduled_at <= NOW()
     ORDER BY scheduled_at ASC
     LIMIT 50
     FOR UPDATE SKIP LOCKED`
  );

  for (const email of emails.rows) {
    try {
      await envoyerEmailParType(email.type, email.payload);

      // Marquer comme envoyé
      await db.query(
        `UPDATE email_outbox SET sent_at = NOW() WHERE id = $1`,
        [email.id]
      );
    } catch (error) {
      // Enregistrer l'erreur et planifier le retry
      const délaiRetry = Math.pow(2, email.attempts) * 60; // Minutes
      await db.query(
        `UPDATE email_outbox
         SET attempts = attempts + 1,
             error = $2,
             scheduled_at = NOW() + ($3 || ' minutes')::interval
         WHERE id = $1`,
        [email.id, (error as Error).message, délaiRetry]
      );
    }
  }
}

// Exécuter le worker outbox toutes les 30 secondes
setInterval(processerOutbox, 30000);
```

---

## Testing des Workers

### Vitest avec BullMQ mocks

```typescript
// tests/workers/email.worker.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Job } from 'bullmq';

// Mock de la connexion Redis et de l'ESP
vi.mock('../../lib/redis', () => ({
  redisConnection: { options: {} },
}));

vi.mock('../../lib/resend', () => ({
  resend: {
    emails: {
      send: vi.fn().mockResolvedValue({ id: 'msg_test_123' }),
    },
  },
}));

vi.mock('../../lib/suppression', () => ({
  estSupprimé: vi.fn().mockResolvedValue(false),
}));

describe('Email Worker', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('envoie un email de bienvenue correctement', async () => {
    const { processerJob } = await import('../../workers/email.worker');
    const { resend } = await import('../../lib/resend');

    const mockJob = {
      id: 'job_1',
      data: { to: 'alice@exemple.fr', type: 'BIENVENUE', variables: { prénom: 'Alice' } },
      attemptsMade: 0,
    } as Job;

    await processerJob(mockJob);

    expect(resend.emails.send).toHaveBeenCalledWith(
      expect.objectContaining({
        to: ['alice@exemple.fr'],
      })
    );
  });

  it('ignore les emails dans la liste de suppression', async () => {
    const { estSupprimé } = await import('../../lib/suppression');
    const { resend } = await import('../../lib/resend');
    vi.mocked(estSupprimé).mockResolvedValue(true);

    const { processerJob } = await import('../../workers/email.worker');
    const mockJob = {
      id: 'job_2',
      data: { to: 'supprimé@exemple.fr', type: 'BIENVENUE', variables: {} },
      attemptsMade: 0,
    } as Job;

    await processerJob(mockJob);

    expect(resend.emails.send).not.toHaveBeenCalled();
  });
});
```

### Tests d'intégration avec Testcontainers

```typescript
// tests/integration/queue.integration.test.ts
import { GenericContainer, StartedTestContainer } from 'testcontainers';
import { Queue, Worker } from 'bullmq';
import { Redis } from 'ioredis';

describe('Email Queue Integration', () => {
  let redisContainer: StartedTestContainer;
  let redis: Redis;
  let queue: Queue;

  beforeAll(async () => {
    // Démarrer un Redis réel dans Docker
    redisContainer = await new GenericContainer('redis:7-alpine')
      .withExposedPorts(6379)
      .start();

    redis = new Redis({
      host: redisContainer.getHost(),
      port: redisContainer.getMappedPort(6379),
      maxRetriesPerRequest: null,
    });

    queue = new Queue('email:test', { connection: redis });
  }, 30000);

  afterAll(async () => {
    await queue.close();
    await redis.quit();
    await redisContainer.stop();
  });

  it('traite un job et appelle l\'ESP', async () => {
    const mockEnvoi = vi.fn().mockResolvedValue({ id: 'msg_1' });

    const worker = new Worker('email:test', async (job) => {
      await mockEnvoi(job.data);
    }, { connection: redis });

    await queue.add('test', { to: 'test@exemple.fr', type: 'TEST' });

    // Attendre que le job soit traité
    await new Promise<void>(resolve => {
      worker.on('completed', () => resolve());
    });

    expect(mockEnvoi).toHaveBeenCalledWith(
      expect.objectContaining({ to: 'test@exemple.fr' })
    );

    await worker.close();
  });
});
```
