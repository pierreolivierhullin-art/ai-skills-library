# Études de Cas — Caching en Production

Ces quatre études de cas illustrent des problèmes réels résolus avec des stratégies de cache adaptées. Chaque cas présente le contexte initial, le diagnostic du problème, la solution implémentée avec le code complet, et les métriques mesurées en production.

## Cas 1 — API REST 800ms → 8ms (SaaS analytique)

### Contexte

Une plateforme SaaS d'analytique B2B propose 50 endpoints d'API pour alimenter des dashboards clients. Chaque appel déclenchait 5 à 10 queries PostgreSQL agrégées (GROUP BY, COUNT DISTINCT, SUM sur des tables de 50M+ lignes). L'équipe avait 12 ingénieurs, 800 clients actifs, et une croissance de 20% par mois du volume de données.

### Problème

Les dashboards s'affichaient en 2 à 3 secondes en heures de pointe. PostgreSQL atteignait 80% de CPU entre 9h et 11h, rendant l'ensemble de la plateforme instable. L'autoscaling de la DB coûtait 4 000$ de plus par mois sans résoudre le problème de fond : les mêmes données étaient recalculées des centaines de fois par heure pour des résultats quasi-identiques.

### Diagnostic

```bash
# EXPLAIN ANALYZE sur la query la plus lourde (stat global dashboard)
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT
  date_trunc('day', created_at) AS day,
  COUNT(DISTINCT user_id) AS unique_users,
  SUM(amount) AS revenue
FROM events
WHERE tenant_id = $1 AND created_at >= NOW() - INTERVAL '30 days'
GROUP BY 1
ORDER BY 1;

# Résultat : Planning Time: 2.3ms, Execution Time: 847ms
# Seq Scan sur 48M lignes — index partiel insuffisant
# Shared hits: 12847 blocks (100MB de buffer pool consommé par requête)
```

### Solution

Cache-aside Redis avec TTL adaptatif par type de données. La clé d'insight : les statistiques globales changent très rarement (toutes les heures quand un batch ETL tourne), mais les statistiques par utilisateur changent à chaque action.

```typescript
// cache-config.ts — TTL différencié par type de données
export const CACHE_TTL = {
  // Stats globales de la plateforme : batch ETL toutes les heures
  globalStats: 3600,       // 1h — correspond au cycle ETL

  // Stats par tenant : recalculées toutes les 5 min par un worker
  tenantStats: 300,        // 5min — fraîcheur acceptable pour les dashboards

  // Stats par utilisateur : plus volatiles
  userStats: 60,           // 1min — acceptable pour l'UX

  // Données temps réel (webhooks, events en direct)
  realtimeEvents: 30,      // 30s — compromis entre fraîcheur et charge DB

  // Métadonnées de configuration (rarement modifiées)
  tenantConfig: 86400,     // 24h — changement exceptionnel

  // Résultats de recherche/filtres
  filteredReports: 120,    // 2min — tolérance à la stale data
} as const;

// analytics-cache.service.ts
import { Redis } from 'ioredis';
import type { Database } from './database';

type CacheKey = keyof typeof CACHE_TTL;

class AnalyticsCacheService {
  constructor(
    private readonly redis: Redis,
    private readonly db: Database,
  ) {}

  // Wrapper générique avec TTL configurable
  async getCached<T>(
    key: string,
    cacheType: CacheKey,
    loader: () => Promise<T>,
  ): Promise<T> {
    const cached = await this.redis.get(key);
    if (cached) {
      metrics.increment('analytics.cache.hit', { type: cacheType });
      return JSON.parse(cached) as T;
    }

    metrics.increment('analytics.cache.miss', { type: cacheType });
    const value = await loader();

    await this.redis.set(
      key,
      JSON.stringify(value),
      'EX',
      CACHE_TTL[cacheType],
    );

    return value;
  }

  // Statistiques de dashboard avec clé composite
  async getDashboardStats(tenantId: string, period: '7d' | '30d' | '90d') {
    const key = `tenant:${tenantId}:stats:${period}`;
    return this.getCached(key, 'tenantStats', () =>
      this.db.query(`
        SELECT
          date_trunc('day', created_at) AS day,
          COUNT(DISTINCT user_id) AS unique_users,
          SUM(amount) AS revenue,
          COUNT(*) AS events
        FROM events
        WHERE tenant_id = $1
          AND created_at >= NOW() - INTERVAL '${period}'
        GROUP BY 1
        ORDER BY 1
      `, [tenantId])
    );
  }
}
```

```typescript
// cache-warmer.ts — Pré-peupler le cache au démarrage de l'application
export async function warmAnalyticsCache(
  redis: Redis,
  db: Database,
): Promise<void> {
  console.log('[CacheWarmer] Début du réchauffement du cache analytique...');
  const t0 = Date.now();

  // Récupérer les 50 tenants les plus actifs (80% du trafic)
  const topTenants = await db.query<{ id: string }[]>(
    `SELECT id FROM tenants ORDER BY monthly_requests DESC LIMIT 50`
  );

  const pipeline = redis.pipeline();
  let count = 0;

  for (const { id } of topTenants) {
    for (const period of ['7d', '30d', '90d'] as const) {
      const stats = await db.query(/* ... query analytique ... */, [id]);
      pipeline.set(
        `tenant:${id}:stats:${period}`,
        JSON.stringify(stats),
        'EX',
        CACHE_TTL.tenantStats,
      );
      count++;
    }
  }

  await pipeline.exec();
  console.log(`[CacheWarmer] ${count} clés réchauffées en ${Date.now() - t0}ms`);
}

// Appel dans le bootstrap de l'application
await warmAnalyticsCache(redis, db);
await app.listen(3000);
// Le pod répond au trafic seulement APRÈS le warming
```

```typescript
// cache-monitor.ts — Monitoring du hit rate en continu
setInterval(async () => {
  const info = await redis.info('stats');
  const hits = parseInt(info.match(/keyspace_hits:(\d+)/)?.[1] || '0');
  const misses = parseInt(info.match(/keyspace_misses:(\d+)/)?.[1] || '0');
  const total = hits + misses;
  const hitRate = total > 0 ? hits / total : 0;

  metrics.gauge('cache.hit_rate', hitRate);

  if (hitRate < 0.85) {
    alerting.send('warning', `Hit rate cache < 85% (${(hitRate * 100).toFixed(1)}%)`);
  }
}, 60_000);
```

### Résultats mesurés

| Métrique                    | Avant      | Après      | Amélioration |
|-----------------------------|------------|------------|--------------|
| Latence P50                 | 800 ms     | 8 ms       | -99%         |
| Latence P99                 | 3 200 ms   | 45 ms      | -98.6%       |
| CPU PostgreSQL (heure de pointe) | 80%   | 15%        | -81%         |
| Coût infrastructure mensuel | 100%       | 60%        | -40%         |
| Hit rate cache              | —          | 94%        | —            |

### Leçon clé

Ne jamais appliquer un TTL universel. La durée de vie d'une donnée analytique varie de 30 secondes (événements temps réel) à 24 heures (configuration). Categoriser les données par fréquence de changement avant de définir les TTLs est la première étape obligatoire de toute implémentation de cache.

---

## Cas 2 — Leaderboard gaming 10M joueurs (jeu mobile)

### Contexte

Un jeu mobile multijoueur avec 10 millions de joueurs enregistrés et 2 millions actifs quotidiennement. Chaque partie terminée met à jour le score du joueur. En heure de pointe : 500 000 mises à jour de score par heure. Le classement mondial est affiché dans le jeu après chaque partie et dans un écran dédié.

### Problème

Le calcul du classement depuis PostgreSQL était impossible à tenir en charge réelle :

```sql
-- Query "rang d'un joueur" — 450ms sur 10M lignes
SELECT COUNT(*) + 1 AS rank
FROM leaderboard
WHERE score > (SELECT score FROM leaderboard WHERE player_id = $1);

-- Query "top 100" — 2200ms
SELECT player_id, pseudo, score,
       RANK() OVER (ORDER BY score DESC) AS rank
FROM leaderboard
ORDER BY score DESC
LIMIT 100;
```

Ces deux queries représentaient 70% de la charge CPU de la base de données. Avec 500 000 parties par heure, les résultats étaient également périmés dès qu'ils étaient calculés.

### Solution

Redis Sorted Set comme source de vérité pour le classement. Le Sorted Set maintient les éléments triés par score en O(log N) et répond aux queries de rang en O(log N) également. Write-through : écriture simultanée en DB (persistance) et Redis (classement temps réel).

```typescript
// leaderboard.service.ts
import { Redis } from 'ioredis';

const LEADERBOARD_KEY = 'leaderboard:global';
const DAILY_LEADERBOARD_KEY = (date: string) => `leaderboard:daily:${date}`;

class LeaderboardService {
  constructor(
    private readonly redis: Redis,
    private readonly db: Database,
  ) {}

  // Mise à jour du score après une partie — write-through
  async updateScore(playerId: string, newScore: number): Promise<void> {
    const pipeline = this.redis.pipeline();

    // Classement global (all-time)
    pipeline.zadd(LEADERBOARD_KEY, newScore.toString(), `player:${playerId}`);

    // Classement du jour (pour les tournois quotidiens)
    const today = new Date().toISOString().split('T')[0];
    pipeline.zadd(DAILY_LEADERBOARD_KEY(today), newScore.toString(), `player:${playerId}`);
    pipeline.expire(DAILY_LEADERBOARD_KEY(today), 86400 * 2); // Garder 2 jours

    await pipeline.exec();

    // Persistance asynchrone en DB (ne pas attendre pour répondre au joueur)
    this.db.query(
      `INSERT INTO leaderboard (player_id, score, updated_at)
       VALUES ($1, $2, NOW())
       ON CONFLICT (player_id) DO UPDATE SET score = GREATEST(score, $2), updated_at = NOW()`,
      [playerId, newScore]
    ).catch(err => console.error('DB write failed for leaderboard', err));
  }

  // Rang personnel du joueur — O(log N) Redis
  async getPlayerRank(playerId: string): Promise<{ rank: number; score: number } | null> {
    const [rank, score] = await Promise.all([
      this.redis.zrevrank(LEADERBOARD_KEY, `player:${playerId}`),
      this.redis.zscore(LEADERBOARD_KEY, `player:${playerId}`),
    ]);

    if (rank === null || score === null) return null;
    return { rank: rank + 1, score: parseFloat(score) }; // rank est 0-indexé
  }

  // Top 100 mondial — O(log N + 100) Redis
  async getTop100(): Promise<Array<{ playerId: string; score: number; rank: number }>> {
    const results = await this.redis.zrevrange(
      LEADERBOARD_KEY,
      0,
      99,
      'WITHSCORES',
    );

    // zrevrange avec WITHSCORES retourne [member, score, member, score, ...]
    const top100 = [];
    for (let i = 0; i < results.length; i += 2) {
      const playerId = results[i].replace('player:', '');
      const score = parseFloat(results[i + 1]);
      top100.push({ playerId, score, rank: top100.length + 1 });
    }
    return top100;
  }

  // Classement contextuel : 5 joueurs autour du joueur courant
  async getContextualRanking(
    playerId: string,
    radius: number = 2
  ): Promise<Array<{ playerId: string; score: number; rank: number }>> {
    const rank = await this.redis.zrevrank(LEADERBOARD_KEY, `player:${playerId}`);
    if (rank === null) return [];

    const from = Math.max(0, rank - radius);
    const to = rank + radius;

    const results = await this.redis.zrevrange(
      LEADERBOARD_KEY,
      from,
      to,
      'WITHSCORES',
    );

    const contextual = [];
    for (let i = 0; i < results.length; i += 2) {
      contextual.push({
        playerId: results[i].replace('player:', ''),
        score: parseFloat(results[i + 1]),
        rank: from + contextual.length + 1,
      });
    }
    return contextual;
  }

  // Joueurs dans une plage de scores (pour les tournois par niveau)
  async getPlayersInScoreRange(minScore: number, maxScore: number): Promise<string[]> {
    return this.redis.zrangebyscore(
      LEADERBOARD_KEY,
      minScore.toString(),
      maxScore.toString(),
    );
  }
}
```

```typescript
// daily-active-users.service.ts — HyperLogLog pour les DAU
class DauService {
  async recordActivePlayer(playerId: string): Promise<void> {
    const today = new Date().toISOString().split('T')[0];
    // PFADD est idempotent — appeler plusieurs fois avec le même ID = 1 unique
    await this.redis.pfadd(`dau:${today}`, playerId);
    // Expirer après 30 jours pour les analyses mensuelles
    await this.redis.expire(`dau:${today}`, 86400 * 30);
  }

  async getDau(date: string): Promise<number> {
    return this.redis.pfcount(`dau:${date}`); // ±0.81% de précision
  }

  async getMau(): Promise<number> {
    // Fusionner les 30 derniers jours
    const keys = Array.from({ length: 30 }, (_, i) => {
      const d = new Date();
      d.setDate(d.getDate() - i);
      return `dau:${d.toISOString().split('T')[0]}`;
    });
    await this.redis.pfmerge('mau:current', ...keys);
    return this.redis.pfcount('mau:current');
  }
}
```

### Résultats mesurés

| Métrique                    | PostgreSQL | Redis Sorted Set | Amélioration |
|-----------------------------|------------|-----------------|--------------|
| Lookup rang personnel       | 450 ms     | 0.3 ms          | -99.9%       |
| Top 100 mondial             | 2 200 ms   | 0.8 ms          | -99.96%      |
| Mémoire pour 10M joueurs    | ~4 GB (DB) | 512 MB Redis    | -87.5%       |
| CPU DB en heure de pointe   | 70%        | 8%              | -89%         |
| Requêtes supportées/seconde | ~200       | ~50 000         | +250x        |

### Leçon clé

Les Sorted Sets Redis sont la solution canonique pour tout système de classement. Ne jamais implémenter un leaderboard avec une query `ORDER BY + RANK()` en SQL sur des tables volumineuses — c'est architecturalement incorrect dès 100 000 entrées. Le Sorted Set maintient l'ordre automatiquement à chaque `ZADD` en O(log N).

---

## Cas 3 — Session management distribué (SaaS multi-instance, Kubernetes)

### Contexte

Application Node.js/Express déployée sur Kubernetes avec 8 pods en autoscaling. Les sessions utilisateur contenaient des données volumineuses : préférences UI, panier d'achat, contexte de navigation (50-200 KB par session). L'application traitait 50 000 sessions actives simultanées.

### Problème

Trois problèmes interdépendants :
1. **Sticky sessions Kubernetes** peu fiables : les pods étaient recréés fréquemment (mises à jour, autoscaling), perdant les sessions locales
2. **Mémoire process gonflée** : chaque pod stockait jusqu'à 2 GB de données de session en mémoire
3. **Pertes de session** lors des déploiements rolling update : les utilisateurs étaient déconnectés à mi-session

### Solution

Redis comme session store centralisé avec `express-session` et `connect-redis`. Sessions JSON avec TTL glissant, compression pour les grandes sessions, et dégradation gracieuse si Redis est indisponible.

```typescript
// session.config.ts
import session from 'express-session';
import RedisStore from 'connect-redis';
import { Redis } from 'ioredis';
import { compress, decompress } from 'snappy'; // Compression rapide

const redis = new Redis({
  host: process.env.REDIS_HOST,
  password: process.env.REDIS_PASSWORD,
  tls: process.env.NODE_ENV === 'production' ? {} : undefined,
  // Retry sur déconnexion avec backoff exponentiel
  retryStrategy: (times) => Math.min(times * 50, 2000),
  enableOfflineQueue: false, // Ne pas empiler les commandes si Redis est down
});

// Sérialiser avec compression pour les grandes sessions
const sessionSerializer = {
  async stringify(session: object): Promise<string> {
    const json = JSON.stringify(session);
    if (json.length < 1024) return json; // Pas de compression pour les petites sessions
    const compressed = await compress(Buffer.from(json));
    return `compressed:${compressed.toString('base64')}`;
  },

  async parse(raw: string): Promise<object> {
    if (!raw.startsWith('compressed:')) return JSON.parse(raw);
    const compressed = Buffer.from(raw.replace('compressed:', ''), 'base64');
    const decompressed = await decompress(compressed);
    return JSON.parse(decompressed.toString());
  },
};

// Configuration du store Redis avec TTL glissant
const store = new RedisStore({
  client: redis,
  prefix: 'sess:',
  ttl: 86400,              // 24h de TTL initial
  disableTouch: false,     // Rafraîchir le TTL à chaque requête (sliding TTL)
  serializer: sessionSerializer,
});

export const sessionMiddleware = session({
  store,
  secret: process.env.SESSION_SECRET!,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    sameSite: 'lax',
    maxAge: 24 * 60 * 60 * 1000, // 24h
  },
  // Générer des IDs de session non-séquentiels (sécurité)
  genid: () => crypto.randomUUID(),
});
```

```typescript
// session-resilience.middleware.ts
// Dégradation gracieuse : si Redis est indisponible, continuer sans session persistante
export function sessionWithFallback(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  const redisAvailable = redis.status === 'ready';

  if (!redisAvailable) {
    // Mode dégradé : session en mémoire locale (non partagée entre pods)
    console.warn('[Session] Redis indisponible — mode dégradé activé');
    metrics.increment('session.degraded_mode');

    // Permettre aux requêtes non-authentifiées de continuer
    if (!req.path.startsWith('/api/protected')) {
      return next();
    }

    // Bloquer les endpoints qui nécessitent absolument la session
    return res.status(503).json({
      error: 'Service temporairement indisponible',
      retryAfter: 30,
    });
  }

  next();
}

// session-cleanup.ts — Nettoyage des sessions orphelines
async function cleanOrphanedSessions(): Promise<void> {
  // Redis gère automatiquement l'expiration via TTL — pas de cleanup manuel nécessaire
  // Mais on peut monitorer le nombre de sessions actives
  const sessionCount = await redis.dbsize(); // Approximatif (toutes les clés)
  const actualSessions = (await redis.keys('sess:*')).length;
  metrics.gauge('sessions.active', actualSessions);
  console.log(`Sessions actives : ${actualSessions}`);
}
```

```typescript
// sliding-ttl.middleware.ts — Renouvellement automatique du TTL de session
export function refreshSessionTTL(
  req: Request,
  _res: Response,
  next: NextFunction
): void {
  if (req.session && req.sessionID) {
    // connect-redis avec disableTouch: false s'en charge automatiquement
    // Mais on peut être explicite pour les sessions "remember me"
    if (req.session.rememberMe) {
      req.session.cookie.maxAge = 30 * 24 * 60 * 60 * 1000; // 30 jours
    }
    req.session.lastActivity = Date.now();
  }
  next();
}
```

### Résultats mesurés

| Métrique                         | Avant         | Après        | Amélioration      |
|----------------------------------|---------------|--------------|-------------------|
| Pertes de session (déploiement)  | ~5% des sessions | 0%        | -100%             |
| Mémoire process par pod          | ~2 GB         | ~200 MB      | -90%              |
| Latence ajoutée par Redis        | —             | < 2ms P99    | (overhead minimal)|
| Sessions perdues / redémarrage   | 100%          | 0%           | -100%             |
| Temps de déploiement rolling     | 8 min (prudent) | 3 min      | -62%              |

### Leçon clé

Externaliser les sessions dans un store Redis dès le premier déploiement multi-instances. Implémenter la dégradation gracieuse dès le départ : si Redis tombe, l'application doit rester partiellement fonctionnelle. Le pattern "Redis down = mode dégradé contrôlé" est préférable au crash total.

---

## Cas 4 — Cache CDN + invalidation événementielle (e-commerce, 500K produits)

### Contexte

Plateforme e-commerce avec 500 000 produits actifs, servies par Next.js avec ISR (Incremental Static Regeneration). Les pages produit sont générées statiquement et servies par Cloudflare CDN. Le catalogue est alimenté par un PIM (Product Information Management) qui gère les mises à jour de prix, de stock et de descriptions.

### Problème

ISR configuré avec `revalidate: 3600` (1 heure) : les mises à jour de prix et de stock étaient visibles avec jusqu'à 1 heure de retard. Inacceptable pour un e-commerce où les prix changent fréquemment (promotions flash, repricing dynamique).

La solution naïve — réduire le revalidate à 60 secondes — aurait généré 500 000 revalidations par heure, saturant l'infrastructure de rendu Next.js et annulant les bénéfices de l'ISR.

### Solution

Tag-based cache invalidation : chaque page produit est taguée avec ses identifiants sémantiques. Quand le PIM met à jour un produit, un webhook déclenche la revalidation ciblée uniquement de ce produit, via `revalidateTag` Next.js et les Cache Tags Cloudflare.

```typescript
// app/products/[id]/page.tsx
import { revalidateTag } from 'next/cache';
import { unstable_cache } from 'next/cache';

// Fetch avec tags — Next.js Data Cache + CDN Cache Tags
async function getProduct(id: string): Promise<Product> {
  const res = await fetch(`${process.env.PIM_API_URL}/products/${id}`, {
    next: {
      revalidate: false,            // Pas de revalidation périodique — on utilise les tags
      tags: [
        `product:${id}`,            // Tag spécifique au produit
        `category:${await getCategoryId(id)}`, // Tag de catégorie
        'catalog',                  // Tag global du catalogue
        `brand:${await getBrandId(id)}`,       // Tag de marque
      ],
    },
    headers: {
      // Transmettre les Cache Tags à Cloudflare
      'Cache-Tag': `product-${id},catalog`,
    },
  });

  if (!res.ok) throw new Error(`Produit ${id} non trouvé`);
  return res.json();
}

// Page produit : statique par défaut, revalidée à la demande
export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);

  return (
    <main>
      <h1>{product.name}</h1>
      <PriceDisplay price={product.price} originalPrice={product.originalPrice} />
      <StockBadge stock={product.stock} />
      <ProductDescription content={product.description} />
    </main>
  );
}

// Métadonnées pour le SEO — elles utilisent aussi le cache taguée
export async function generateMetadata({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id); // Retourne depuis le cache
  return {
    title: product.name,
    description: product.metaDescription,
  };
}
```

```typescript
// app/api/webhooks/pim/route.ts — Webhook déclenché par le PIM
import { revalidateTag } from 'next/cache';
import { headers } from 'next/headers';
import crypto from 'crypto';

// Payload envoyé par le PIM lors d'une mise à jour
interface PimWebhookPayload {
  event: 'product.updated' | 'product.created' | 'product.deleted' | 'category.updated';
  productId?: string;
  categoryId?: string;
  changedFields?: string[];
  timestamp: number;
}

export async function POST(request: Request): Promise<Response> {
  // Vérifier la signature du webhook (sécurité)
  const signature = headers().get('X-PIM-Signature');
  const body = await request.text();

  const expectedSignature = crypto
    .createHmac('sha256', process.env.PIM_WEBHOOK_SECRET!)
    .update(body)
    .digest('hex');

  if (signature !== `sha256=${expectedSignature}`) {
    return new Response('Signature invalide', { status: 401 });
  }

  const payload = JSON.parse(body) as PimWebhookPayload;
  const invalidatedTags: string[] = [];

  switch (payload.event) {
    case 'product.updated':
      if (!payload.productId) break;

      // Toujours invalider le produit lui-même
      revalidateTag(`product:${payload.productId}`);
      invalidatedTags.push(`product:${payload.productId}`);

      // Invalider les listes de la catégorie si la catégorie a changé
      if (payload.changedFields?.includes('category_id')) {
        revalidateTag(`category:${payload.categoryId}`);
        invalidatedTags.push(`category:${payload.categoryId}`);
      }

      // Invalider les résultats de recherche si le nom ou le prix a changé
      if (payload.changedFields?.some(f => ['name', 'price', 'tags'].includes(f))) {
        revalidateTag('search-results');
        invalidatedTags.push('search-results');
      }

      // Purger Cloudflare CDN par Cache-Tag
      await purgeCloudflareByTag([`product-${payload.productId}`]);

      break;

    case 'category.updated':
      revalidateTag(`category:${payload.categoryId}`);
      revalidateTag('catalog');
      invalidatedTags.push(`category:${payload.categoryId}`, 'catalog');
      await purgeCloudflareByTag([`category-${payload.categoryId}`]);
      break;
  }

  console.log(`[Webhook PIM] Tags invalidés :`, invalidatedTags);

  return Response.json({
    revalidated: true,
    tags: invalidatedTags,
    timestamp: Date.now(),
  });
}

// Purge Cloudflare par Cache-Tag (plan Business+ requis)
async function purgeCloudflareByTag(tags: string[]): Promise<void> {
  const response = await fetch(
    `https://api.cloudflare.com/client/v4/zones/${process.env.CF_ZONE_ID}/cache/purge`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.CF_API_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tags }),
    }
  );

  if (!response.ok) {
    console.error('[Cloudflare] Purge échouée :', await response.text());
  }
}
```

```typescript
// next.config.ts — Configuration complète du cache CDN
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  async headers() {
    return [
      // Pages produit : CDN cache long avec Cache-Tag pour invalidation ciblée
      {
        source: '/products/:path*',
        headers: [
          {
            key: 'Cache-Control',
            // s-maxage=86400 : CDN garde 24h
            // stale-while-revalidate=600 : servir stale 10min pendant revalidation
            // stale-if-error=86400 : servir stale 24h si l'origine répond en erreur
            value: 'public, s-maxage=86400, stale-while-revalidate=600, stale-if-error=86400',
          },
          {
            key: 'Surrogate-Control', // Pour les CDN qui supportent Surrogate-Control (Fastly)
            value: 'max-age=86400',
          },
        ],
      },
      // Assets statiques : immutables
      {
        source: '/_next/static/:path*',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' },
        ],
      },
    ];
  },

  // Configuration du Data Cache Next.js
  experimental: {
    staleTimes: {
      dynamic: 0,    // Pages dynamiques : pas de cache par défaut
      static: 3600,  // Pages statiques sans revalidate : 1h
    },
  },
};

export default nextConfig;
```

```typescript
// scripts/cache-warming-deployment.ts
// Exécuter AVANT la mise en production lors d'un déploiement blue-green
// Pré-générer les 1000 pages produit les plus visitées

async function warmTopProducts(): Promise<void> {
  console.log('[Deployment] Préchauffage des pages produit les plus visitées...');

  const topProducts = await db.query<{ id: string }[]>(
    `SELECT product_id AS id, COUNT(*) AS views
     FROM page_views
     WHERE created_at >= NOW() - INTERVAL '7 days'
     GROUP BY product_id
     ORDER BY views DESC
     LIMIT 1000`
  );

  // Générer les pages en parallèle (4 à la fois pour ne pas surcharger le rendu)
  const BATCH_SIZE = 4;
  for (let i = 0; i < topProducts.length; i += BATCH_SIZE) {
    const batch = topProducts.slice(i, i + BATCH_SIZE);
    await Promise.all(
      batch.map(({ id }) =>
        fetch(`${process.env.NEXT_BASE_URL}/products/${id}`, {
          headers: { 'X-Cache-Warm': 'true' },
        }).catch(err => console.warn(`Warm failed for product ${id}:`, err.message))
      )
    );
    console.log(`[Deployment] ${Math.min(i + BATCH_SIZE, topProducts.length)}/${topProducts.length} pages préchauffées`);
  }
}
```

### Résultats mesurés

| Métrique                               | ISR 60min   | ISR + Tags ciblés | Amélioration   |
|----------------------------------------|-------------|-------------------|----------------|
| Délai de mise à jour visible           | ~60 min     | < 30 s            | -98%           |
| Revalidations/heure (charge serveur)   | 500 000     | ~200 (modifications réelles) | -99.96% |
| Pages statiques non touchées (500K prod) | 0%        | 499 800/500 000   | 99.96% servis depuis CDN |
| Faux positifs (revalidations inutiles) | 0           | 0                 | Revalidation ciblée |
| Coût rendu Next.js (CPU)               | Très élevé  | Minimal           | -95%           |

### Leçon clé

Le tag-based cache invalidation est le compromis parfait entre fraîcheur et performance pour les catalogues larges. La revalidation globale (`revalidateTag('catalog')`) est un antipattern à éviter sauf en cas de refonte complète. La granularité des tags doit correspondre à la granularité des mises à jour : `product:${id}` pour une mise à jour produit, `category:${id}` pour une mise à jour de catégorie.

---

## Synthèse — Choisir sa stratégie selon le contexte

| Contexte                        | Pattern recommandé             | Structure Redis       |
|---------------------------------|--------------------------------|-----------------------|
| API dashboard analytique        | Cache-aside + TTL adaptatif    | String (JSON)         |
| Classement temps réel           | Write-through + Sorted Set     | Sorted Set            |
| Sessions multi-instances        | Session store externalisé      | String avec TTL       |
| Catalogue e-commerce            | Tag-based ISR + CDN            | Next.js Data Cache    |
| Comptage d'utilisateurs uniques | HyperLogLog                    | HyperLogLog           |
| File de tâches fiable           | Consumer groups                | Streams               |
| Rate limiting                   | Lua script atomique            | String (compteur)     |
| Verrou distribué                | Redlock                        | String (NX + EX)      |
| Invalidation cross-pods (L1)    | Pub/Sub                        | Pub/Sub channel       |

La règle universelle : mesurer avant d'optimiser, et toujours prévoir la dégradation gracieuse quand le cache est indisponible.
