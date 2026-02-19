---
name: caching-strategies
version: 1.0.0
description: >
  Redis advanced patterns caching, cache-aside pattern, write-through write-behind cache,
  cache invalidation strategies, cache stampede dog-pile prevention, TTL strategies,
  Redis data structures sorted sets hashes lists streams, Redis pub/sub,
  distributed cache, multi-level caching L1 L2, CDN edge cache, browser caching,
  stale-while-revalidate, cache warming, session storage, rate limiting Redis
---

# Caching Strategies — Cache Multi-Niveaux et Redis Avancé

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Les requêtes DB sont trop lentes ou génèrent trop de charge sur la base de données
- Tu dois gérer des sessions, des tokens, ou des états temporaires
- Tu implémente du rate limiting ou du throttling sur une API
- Tu veux implémenter un leaderboard, un compteur temps réel, ou un feed d'activité
- Tu as des problèmes de cache stampede (effet thundering herd)
- Tu conçois une stratégie de cache multi-niveaux (L1 mémoire + L2 Redis + L3 CDN)

---

## Stratégies de Cache

### Cache-Aside (Lazy Loading) — La plus courante

```typescript
import { createClient } from 'redis';
import { prisma } from '@/lib/prisma';

const redis = createClient({ url: process.env.REDIS_URL });
await redis.connect();

async function getProduit(id: string): Promise<Produit | null> {
  const cacheKey = `produit:${id}`;

  // 1. Vérifier le cache
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // 2. Cache miss → charger depuis la DB
  const produit = await prisma.produit.findUnique({
    where: { id },
    include: { categorie: true, images: true },
  });

  // 3. Stocker en cache
  if (produit) {
    await redis.set(cacheKey, JSON.stringify(produit), { EX: 3600 });  // 1h TTL
  }

  return produit;
}

// Invalider le cache à la mise à jour
async function updateProduit(id: string, données: Partial<Produit>): Promise<Produit> {
  const produit = await prisma.produit.update({ where: { id }, data: données });
  await redis.del(`produit:${id}`);  // Invalider
  return produit;
}
```

### Write-Through — Cohérence garantie

```typescript
// Écrire simultanément en DB et en cache
async function saveProduit(produit: Produit): Promise<void> {
  await Promise.all([
    prisma.produit.upsert({ where: { id: produit.id }, update: produit, create: produit }),
    redis.set(`produit:${produit.id}`, JSON.stringify(produit), { EX: 3600 }),
  ]);
}
```

### Write-Behind (Write-Back) — Performance maximale

```typescript
// Écrire immédiatement en cache, puis en DB de façon asynchrone
async function incrementerVues(produitId: string): Promise<void> {
  const key = `produit:vues:${produitId}`;
  const newVues = await redis.incr(key);

  // Flush vers DB tous les 100 vues ou toutes les 5 minutes
  if (newVues % 100 === 0) {
    await syncVuesVersDB(produitId, newVues);
  }
}

// Worker cron pour flush périodique
setInterval(async () => {
  const keys = await redis.keys('produit:vues:*');
  for (const key of keys) {
    const produitId = key.split(':')[2];
    const vues = parseInt(await redis.get(key) ?? '0', 10);
    if (vues > 0) {
      await prisma.produit.update({ where: { id: produitId }, data: { vues } });
    }
  }
}, 5 * 60 * 1000);
```

---

## Prévenir le Cache Stampede

Quand le cache expire, toutes les requêtes simultanées frappent la DB en même temps.

```typescript
// Solution : verrou distribué avec Redis
async function getProduitAvecVerrou(id: string): Promise<Produit | null> {
  const cacheKey = `produit:${id}`;
  const verrouilleKey = `verrou:${cacheKey}`;

  // 1. Lire le cache
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // 2. Acquérir le verrou (NX = seulement si inexistant)
  const verrou = await redis.set(verrouilleKey, '1', { NX: true, EX: 5 });

  if (verrou) {
    // 3. On a le verrou → charger depuis DB
    const produit = await prisma.produit.findUnique({ where: { id } });
    if (produit) {
      await redis.set(cacheKey, JSON.stringify(produit), { EX: 3600 });
    }
    await redis.del(verrouilleKey);
    return produit;
  } else {
    // 4. Quelqu'un d'autre charge → attendre et réessayer
    await sleep(100);
    return getProduitAvecVerrou(id);  // Récursion (avec limite)
  }
}

// Solution alternative : probabilistic early expiration
async function getProduitProbabiliste(id: string, beta = 1): Promise<Produit | null> {
  const cacheKey = `produit:${id}`;
  const metaKey = `${cacheKey}:meta`;

  const [cached, meta] = await Promise.all([
    redis.get(cacheKey),
    redis.hGetAll(metaKey),
  ]);

  if (cached && meta.expires) {
    const ttlRestant = parseInt(meta.expires, 10) - Date.now();
    const delta = parseFloat(meta.delta ?? '1');

    // Recompute early avec probabilité croissante quand le TTL est faible
    const shouldRecompute = -delta * beta * Math.log(Math.random()) > ttlRestant;

    if (!shouldRecompute) return JSON.parse(cached);
  }

  // Recompute
  const début = Date.now();
  const produit = await prisma.produit.findUnique({ where: { id } });
  const delta = Date.now() - début;

  if (produit) {
    const ttl = 3600;
    await Promise.all([
      redis.set(cacheKey, JSON.stringify(produit), { EX: ttl }),
      redis.hSet(metaKey, { expires: String(Date.now() + ttl * 1000), delta: String(delta) }),
    ]);
  }

  return produit;
}
```

---

## Structures de Données Redis Avancées

### Sorted Sets — Leaderboard

```typescript
const LEADERBOARD_KEY = 'jeu:scores';

// Ajouter/mettre à jour le score
async function updateScore(joueurId: string, score: number): Promise<void> {
  await redis.zAdd(LEADERBOARD_KEY, { score, value: joueurId });
}

// Top 10
async function getTop10(): Promise<Array<{ joueur: string; score: number }>> {
  const membres = await redis.zRangeWithScores(LEADERBOARD_KEY, 0, 9, { REV: true });
  return membres.map(m => ({ joueur: m.value, score: m.score }));
}

// Rang d'un joueur (0-indexed)
async function getRang(joueurId: string): Promise<number | null> {
  return redis.zRevRank(LEADERBOARD_KEY, joueurId);
}

// Joueurs dans une plage de score
async function getJoueursAvecScore(min: number, max: number) {
  return redis.zRangeByScore(LEADERBOARD_KEY, min, max);
}
```

### Hashes — Sessions et Objets Partiels

```typescript
// Mettre à jour des champs spécifiques sans charger tout l'objet
async function updateUserSession(userId: string, updates: Partial<SessionData>): Promise<void> {
  const key = `session:${userId}`;
  await redis.hSet(key, updates as Record<string, string>);
  await redis.expire(key, 86400);  // 24h
}

async function getSessionField(userId: string, field: keyof SessionData): Promise<string | null> {
  return redis.hGet(`session:${userId}`, field);
}
```

### Streams — File de Messages

```typescript
// Producteur
async function publierEvenement(stream: string, event: object): Promise<string> {
  return redis.xAdd(stream, '*', {
    type: event.type,
    payload: JSON.stringify(event),
    ts: String(Date.now()),
  });
}

// Consommateur avec consumer group
async function consommerEvenements(stream: string, group: string, consumer: string): Promise<void> {
  // Créer le groupe si inexistant
  try {
    await redis.xGroupCreate(stream, group, '0', { MKSTREAM: true });
  } catch { /* Déjà créé */ }

  while (true) {
    const messages = await redis.xReadGroup(group, consumer, [
      { key: stream, id: '>' },  // '>' = nouveaux messages non traités
    ], { COUNT: 10, BLOCK: 2000 });

    if (!messages) continue;

    for (const { messages: msgs } of messages) {
      for (const { id, message } of msgs) {
        try {
          await traiterMessage(message);
          await redis.xAck(stream, group, id);  // ACK = confirmé traité
        } catch (e) {
          console.error(`Échec traitement ${id}:`, e);
          // Laisser dans le pending pour retraitement
        }
      }
    }
  }
}
```

---

## Rate Limiting avec Redis

```typescript
// Algorithme Token Bucket distribué
async function checkRateLimit(
  identifier: string,
  limit: number,
  windowSeconds: number,
): Promise<{ allowed: boolean; remaining: number; resetAt: Date }> {
  const key = `ratelimit:${identifier}`;
  const now = Date.now();
  const windowMs = windowSeconds * 1000;

  // Lua script pour l'atomicité
  const script = `
    local key = KEYS[1]
    local limit = tonumber(ARGV[1])
    local now = tonumber(ARGV[2])
    local window = tonumber(ARGV[3])

    -- Supprimer les requêtes hors fenêtre
    redis.call('ZREMRANGEBYSCORE', key, 0, now - window)

    local count = redis.call('ZCARD', key)

    if count < limit then
      redis.call('ZADD', key, now, now)
      redis.call('EXPIRE', key, math.ceil(window / 1000))
      return {1, limit - count - 1}
    else
      return {0, 0}
    end
  `;

  const result = await redis.eval(script, {
    keys: [key],
    arguments: [String(limit), String(now), String(windowMs)],
  }) as [number, number];

  const oldest = await redis.zRange(key, 0, 0, { BY: 'SCORE' });
  const resetAt = oldest.length > 0
    ? new Date(parseInt(oldest[0], 10) + windowMs)
    : new Date(now + windowMs);

  return {
    allowed: result[0] === 1,
    remaining: result[1],
    resetAt,
  };
}
```

---

## Cache Multi-Niveaux

```typescript
// L1 : Mémoire process (ultra-rapide, limité)
import LRUCache from 'lru-cache';

const l1Cache = new LRUCache<string, unknown>({
  max: 500,
  ttl: 60_000,  // 1 minute
});

// L2 : Redis (rapide, partagé entre instances)
// L3 : DB (source de vérité)

async function getData<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
  // L1
  const l1 = l1Cache.get(key);
  if (l1) return l1 as T;

  // L2
  const l2 = await redis.get(key);
  if (l2) {
    const data = JSON.parse(l2) as T;
    l1Cache.set(key, data);
    return data;
  }

  // L3 → fetcher
  const data = await fetcher();
  await redis.set(key, JSON.stringify(data), { EX: 3600 });
  l1Cache.set(key, data);
  return data;
}
```

---

## Références

- `references/redis-patterns.md` — Redis Cluster, Sentinel, Lua scripts, Pub/Sub avancé, HyperLogLog, Bloom filters
- `references/cache-patterns.md` — Cache warming, invalidation patterns, consistent hashing, cache eviction policies
- `references/distributed-cache.md` — Multi-niveau avancé, CDN (Cloudflare, Fastly), Varnish, browser cache, stale-while-revalidate
- `references/case-studies.md` — 4 cas : API 100ms→5ms avec cache, leaderboard gaming, sessions distribuées, rate limiting API
