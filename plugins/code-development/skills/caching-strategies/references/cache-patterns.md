# Patterns de Cache — Stratégies d'Invalidation et Cohérence

L'invalidation de cache est l'un des deux problèmes difficiles de l'informatique. Choisir la mauvaise stratégie entraîne soit des données périmées visibles par les utilisateurs, soit une surcharge de la base de données qui annule les bénéfices du cache. Ce guide couvre les patterns fondamentaux et leur implémentation concrète.

## Les 4 stratégies fondamentales — Tableau comparatif

| Stratégie       | Cohérence lecture | Latence écriture | Complexité | Risque de stale data |
|-----------------|-------------------|------------------|------------|----------------------|
| Cache-Aside     | Éventuelle        | Faible (DB seule) | Faible     | Oui (miss au premier appel) |
| Read-Through    | Éventuelle        | Faible (DB seule) | Moyenne    | Oui (géré par le cache) |
| Write-Through   | Forte             | Haute (DB + cache) | Moyenne   | Non                  |
| Write-Behind    | Éventuelle        | Très faible (cache seul) | Haute | Risque de perte de données |

### Cache-Aside (Lazy Loading)

C'est le pattern le plus répandu. L'application est responsable du cache : elle le consulte, gère les misses et le peuple elle-même.

```typescript
class UserRepository {
  constructor(
    private readonly redis: Redis,
    private readonly db: Database,
  ) {}

  async findById(userId: string): Promise<User | null> {
    const cacheKey = `user:${userId}:profile`;

    // 1. Consulter le cache
    const cached = await this.redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached) as User;
    }

    // 2. Cache miss → aller en base
    const user = await this.db.query<User>(
      'SELECT * FROM users WHERE id = $1', [userId]
    );

    // 3. Peupler le cache pour les prochaines requêtes
    if (user) {
      await this.redis.set(cacheKey, JSON.stringify(user), 'EX', 3600);
    }

    return user;
  }

  async update(userId: string, data: Partial<User>): Promise<User> {
    const user = await this.db.update<User>('users', userId, data);
    // Invalider le cache après écriture
    await this.redis.del(`user:${userId}:profile`);
    return user;
  }
}
```

**Avantage** : seules les données réellement demandées entrent en cache (pas de chargement inutile).
**Inconvénient** : le premier appel après un miss (ou après invalidation) frappe toujours la base.

### Read-Through Cache

La différence avec cache-aside est subtile mais importante : c'est le cache lui-même (ou une couche d'abstraction) qui appelle la DB, pas l'application. L'application ne connaît que le cache.

```typescript
class CacheLayer<T> {
  private loaders = new Map<string, () => Promise<T>>();

  register(pattern: string, loader: (key: string) => Promise<T>): void {
    this.loaders.set(pattern, loader as () => Promise<T>);
  }

  async get(key: string): Promise<T | null> {
    const cached = await this.redis.get(key);
    if (cached) return JSON.parse(cached);

    // Le cache appelle lui-même le loader enregistré
    const loader = this.findLoader(key);
    if (!loader) return null;

    const value = await loader(key);
    if (value) await this.redis.set(key, JSON.stringify(value), 'EX', 3600);
    return value;
  }
}

// L'application ne connaît que la couche cache
const cache = new CacheLayer<User>();
cache.register('user:*:profile', async (key) => {
  const userId = key.split(':')[1];
  return db.findUser(userId);
});

// Appel simplifié depuis l'application
const user = await cache.get('user:42:profile'); // La DB n'est jamais appelée directement
```

### Write-Through

Chaque écriture est faite simultanément en base et dans le cache. Le cache est toujours cohérent avec la DB.

```typescript
async function updateUserProfile(userId: string, data: Partial<User>): Promise<User> {
  // Écriture en DB (source de vérité)
  const user = await db.update<User>('users', userId, data);

  // Mise à jour immédiate du cache (write-through)
  await redis.set(`user:${userId}:profile`, JSON.stringify(user), 'EX', 3600);

  return user;
}
```

**Quand choisir write-through** : données lues très fréquemment après écriture (profil utilisateur mis à jour puis immédiatement rechargé), ou quand les misses post-invalidation sont inacceptables.

### Write-Behind (Write-Back)

L'écriture est faite dans le cache immédiatement, la persistance en base est asynchrone et différée. Extrêmement performant pour les écritures fréquentes, mais risqué si le cache tombe avant la persistance.

```typescript
class WriteBehindCache {
  private writeQueue = new Map<string, { data: unknown; timestamp: number }>();
  private flushInterval: NodeJS.Timer;

  constructor(private redis: Redis, private db: Database) {
    // Flush vers la DB toutes les 5 secondes
    this.flushInterval = setInterval(() => this.flush(), 5000);
  }

  async write(key: string, data: unknown): Promise<void> {
    // Écriture immédiate dans le cache (réponse instantanée)
    await this.redis.set(key, JSON.stringify(data));
    // Mise en queue pour persistance asynchrone
    this.writeQueue.set(key, { data, timestamp: Date.now() });
  }

  private async flush(): Promise<void> {
    const entries = Array.from(this.writeQueue.entries());
    this.writeQueue.clear();

    await Promise.allSettled(
      entries.map(([key, { data }]) => this.persistToDb(key, data))
    );
  }
}
```

**Cas d'usage appropriés** : compteurs d'événements (vues, likes), métriques temps réel, données où une perte partielle est acceptable.

## Refresh-Ahead et Stale-While-Revalidate

Le refresh-ahead anticipe l'expiration du cache pour éviter les misses : quand une clé approche de son TTL, elle est rafraîchie en arrière-plan avant d'expirer.

```typescript
class RefreshAheadCache {
  // Rafraîchir si on est dans les 20% de temps restant avant expiration
  private readonly REFRESH_THRESHOLD = 0.2;

  async get<T>(key: string, loader: () => Promise<T>, ttl: number): Promise<T | null> {
    const [value, remainingTtl] = await Promise.all([
      this.redis.get(key),
      this.redis.ttl(key),
    ]);

    if (!value) return this.loadAndCache(key, loader, ttl);

    const parsed = JSON.parse(value) as T;

    // Rafraîchissement proactif en arrière-plan
    const shouldRefresh = remainingTtl > 0 && remainingTtl < ttl * this.REFRESH_THRESHOLD;
    if (shouldRefresh) {
      // Ne pas attendre — l'utilisateur reçoit la valeur stale immédiatement
      this.loadAndCache(key, loader, ttl).catch(console.error);
    }

    return parsed;
  }

  private async loadAndCache<T>(key: string, loader: () => Promise<T>, ttl: number): Promise<T> {
    const value = await loader();
    await this.redis.set(key, JSON.stringify(value), 'EX', ttl);
    return value;
  }
}
```

**HTTP stale-while-revalidate** : l'équivalent au niveau du protocole HTTP. Le navigateur/CDN sert la réponse stale immédiatement et la revalide en arrière-plan.

```typescript
// Express — header stale-while-revalidate
res.set('Cache-Control', 'public, max-age=60, stale-while-revalidate=300');
// max-age=60 : frais pendant 60s
// stale-while-revalidate=300 : servir stale pendant encore 5min si la revalidation est en cours
```

## Stratégies d'invalidation

### TTL simple — Calcul du TTL optimal

Le TTL est le mécanisme le plus simple, mais choisir la bonne valeur est un art. La règle générale :

```
TTL optimal = durée_de_vie_donnée × (1 - tolérance_au_stale)

Exemples :
- Prix e-commerce (change toutes les heures) × tolérance 10% = 360s ≈ 5 min
- Profil utilisateur (change rarement) × tolérance 50% = plusieurs heures
- Météo (change toutes les 10min) × tolérance 20% = 2 min
- Données temps réel de trading : pas de cache, ou TTL 1-5s max
```

```typescript
// TTL adaptatif selon le type de données
const TTL_CONFIG = {
  'user:profile': 3600,          // 1h — change rarement
  'user:preferences': 1800,      // 30min — change occasionnellement
  'product:detail': 600,         // 10min — prix peuvent changer
  'product:stock': 60,           // 1min — stock très volatile
  'analytics:dashboard': 300,    // 5min — tolérance à la stale data
  'session:data': 86400,         // 24h — géré par sliding TTL
} as const;
```

### Tag-based invalidation

Associer des tags sémantiques aux clés de cache permet d'invalider des groupes entiers de clés liées à une entité, sans connaître toutes les clés individuellement.

```typescript
class TaggedCache {
  private redis: Redis;

  async set(key: string, value: unknown, ttl: number, tags: string[]): Promise<void> {
    const pipeline = this.redis.pipeline();
    pipeline.set(key, JSON.stringify(value), 'EX', ttl);

    // Enregistrer la clé sous chaque tag (Set Redis)
    for (const tag of tags) {
      pipeline.sadd(`tag:${tag}`, key);
      pipeline.expire(`tag:${tag}`, ttl + 60); // Garder le tag légèrement plus longtemps
    }

    await pipeline.exec();
  }

  async invalidateTag(tag: string): Promise<number> {
    const keys = await this.redis.smembers(`tag:${tag}`);
    if (!keys.length) return 0;

    const pipeline = this.redis.pipeline();
    for (const key of keys) pipeline.del(key);
    pipeline.del(`tag:${tag}`);
    await pipeline.exec();

    return keys.length;
  }
}

// Usage : associer les caches liés à un produit
await cache.set('product:42:detail', productData, 600, ['product:42', 'catalog']);
await cache.set('product:42:pricing', pricingData, 60, ['product:42', 'pricing']);
await cache.set('search:laptops:page1', searchResults, 300, ['catalog', 'search']);

// Quand le produit 42 est modifié : invalider tout ce qui le concerne
const invalidated = await cache.invalidateTag('product:42');
// → invalide 'product:42:detail' et 'product:42:pricing' en une opération
```

### Event-driven invalidation

Le cache est invalidé en réaction aux événements métier, découplant la logique d'invalidation de la logique d'écriture.

```typescript
// Producteur : publier un événement lors de la mise à jour
async function updateProduct(productId: string, data: Partial<Product>): Promise<Product> {
  const product = await db.update('products', productId, data);

  // Publier l'événement d'invalidation
  await eventBus.publish('product.updated', {
    productId,
    updatedFields: Object.keys(data),
    timestamp: Date.now(),
  });

  return product;
}

// Consommateur : invalider le cache en réaction à l'événement
eventBus.subscribe('product.updated', async ({ productId, updatedFields }) => {
  const tagsToInvalidate = ['product:' + productId];

  if (updatedFields.includes('price')) tagsToInvalidate.push('pricing');
  if (updatedFields.includes('stock')) tagsToInvalidate.push('availability');

  await Promise.all(tagsToInvalidate.map(tag => cache.invalidateTag(tag)));
  console.log(`Cache invalidé pour product:${productId}`, tagsToInvalidate);
});
```

## Cache Stampede (Thundering Herd)

Le cache stampede se produit quand une clé populaire expire et que des centaines de requêtes simultanées essaient de la recalculer toutes en même temps, submergeant la base de données.

### Détection

```typescript
// Identifier le stampede : spike soudain de misses sur une clé
// Si keyspace_misses augmente brutalement → suspicion de stampede
// Vérifier avec MONITOR (très brièvement) pour confirmer
```

### Solution 1 — Mutex Redis

```typescript
async function getWithMutex<T>(
  key: string,
  loader: () => Promise<T>,
  ttl: number
): Promise<T> {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  const lockKey = `lock:${key}`;
  const lockToken = randomUUID();

  // Tenter d'acquérir le verrou (NX = seulement si absent)
  const acquired = await redis.set(lockKey, lockToken, 'EX', 10, 'NX');

  if (acquired) {
    // On a le verrou : calculer et cacher la valeur
    try {
      const value = await loader();
      await redis.set(key, JSON.stringify(value), 'EX', ttl);
      return value;
    } finally {
      // Libérer le verrou (Lua script atomique)
      await redis.eval(
        `if redis.call('get',KEYS[1])==ARGV[1] then return redis.call('del',KEYS[1]) else return 0 end`,
        1, lockKey, lockToken
      );
    }
  } else {
    // Un autre worker calcule la valeur : attendre et réessayer
    await new Promise(resolve => setTimeout(resolve, 100 + Math.random() * 100));
    return getWithMutex(key, loader, ttl); // Retry récursif
  }
}
```

### Solution 2 — Probabilistic Early Expiration (XFetch)

XFetch est l'approche la plus élégante : chaque requête a une probabilité croissante de déclencher le rafraîchissement à l'approche de l'expiration, sans verrou.

```typescript
// Algorithme XFetch — Optimal Probabilistic Cache Stampede Prevention (Vattani et al., 2015)
async function getXFetch<T>(
  key: string,
  loader: () => Promise<T>,
  ttl: number,
  beta: number = 1.0 // beta > 1 = rafraîchissement plus agressif
): Promise<T> {
  const raw = await redis.get(`xfetch:${key}`);

  if (raw) {
    const { value, delta, expiry } = JSON.parse(raw);
    // P(refresh) augmente exponentiellement à l'approche de l'expiration
    const now = Date.now() / 1000;
    if (expiry - now > beta * delta * Math.log(Math.random())) {
      return value; // Pas encore le moment de rafraîchir
    }
  }

  // Rafraîchir (soit first load, soit early refresh probabiliste)
  const start = Date.now();
  const value = await loader();
  const delta = (Date.now() - start) / 1000; // Temps de calcul en secondes
  const expiry = Date.now() / 1000 + ttl;

  await redis.set(`xfetch:${key}`, JSON.stringify({ value, delta, expiry }), 'EX', ttl + 60);
  return value;
}
```

## Cache Warming

Le warming consiste à pré-peupler le cache avant que le trafic arrive, évitant les misses massives au démarrage.

```typescript
// warming.ts — À exécuter au démarrage de l'application
async function warmCache(): Promise<void> {
  console.log('Début du cache warming...');
  const start = Date.now();

  // Pré-charger les données les plus consultées
  const [topProducts, topCategories, globalConfig] = await Promise.all([
    db.query<Product[]>('SELECT * FROM products ORDER BY views DESC LIMIT 1000'),
    db.query<Category[]>('SELECT * FROM categories WHERE active = true'),
    db.query<Config>('SELECT * FROM config WHERE scope = \'global\''),
  ]);

  // Peupler le cache en pipeline pour la performance
  const pipeline = redis.pipeline();

  topProducts.forEach(p => {
    pipeline.set(`product:${p.id}:detail`, JSON.stringify(p), 'EX', 600);
  });

  topCategories.forEach(c => {
    pipeline.set(`category:${c.id}`, JSON.stringify(c), 'EX', 3600);
  });

  pipeline.set('config:global', JSON.stringify(globalConfig), 'EX', 86400);

  await pipeline.exec();

  const duration = Date.now() - start;
  console.log(`Cache warming terminé en ${duration}ms — ${topProducts.length} produits chargés`);
}

// Warm pendant un blue-green deployment AVANT de basculer le trafic
// Cela garantit que le nouveau pod ne sert pas de misses au démarrage
```

## Negative Caching

Mettre en cache les résultats "not found" est essentiel pour éviter les attaques par énumération et les requêtes répétées sur des ressources inexistantes.

```typescript
const NEGATIVE_CACHE_SENTINEL = '__NOT_FOUND__';

async function findProduct(productId: string): Promise<Product | null> {
  const cached = await redis.get(`product:${productId}:detail`);

  if (cached === NEGATIVE_CACHE_SENTINEL) {
    return null; // Negative cache hit — pas de requête DB
  }

  if (cached) {
    return JSON.parse(cached);
  }

  const product = await db.findById('products', productId);

  if (product) {
    await redis.set(`product:${productId}:detail`, JSON.stringify(product), 'EX', 600);
  } else {
    // Cacher le "not found" avec un TTL court
    await redis.set(`product:${productId}:detail`, NEGATIVE_CACHE_SENTINEL, 'EX', 60);
  }

  return product;
}
```

**TTL recommandé pour le negative cache** : 30-120 secondes. Assez long pour absorber les requêtes répétées, assez court pour que la création de la ressource soit visible rapidement.

## Conventions de nommage des clés

```typescript
// Pattern recommandé : {entité}:{id}:{attribut}
// Exemples :
const CACHE_KEYS = {
  userProfile:    (id: string)   => `user:${id}:profile`,
  userPrefs:      (id: string)   => `user:${id}:prefs`,
  productDetail:  (id: string)   => `product:${id}:detail`,
  productStock:   (id: string)   => `product:${id}:stock`,
  searchResults:  (query: string, page: number) =>
                   `search:${hashKey(query)}:page:${page}`,
  tenantConfig:   (tenantId: string) => `tenant:${tenantId}:config`,
};

// Hashage pour les clés longues (URL, requêtes SQL, etc.)
import { createHash } from 'crypto';
function hashKey(input: string): string {
  return createHash('sha256').update(input).digest('hex').substring(0, 16);
}

// Namespacing par tenant dans un contexte multi-tenant
function tenantKey(tenantId: string, key: string): string {
  return `{tenant:${tenantId}}:${key}`;
  // Les {} assurent que toutes les clés du même tenant vont sur le même slot Redis Cluster
}
```

## Cache Partitioning

```typescript
// Séparer les caches par type pour isoler les impacts
const caches = {
  // Cache "hot" : données très fréquentes, TTL court, éviction agressive
  hot: new Redis({ host: 'redis-hot', maxmemory: '512mb', policy: 'allkeys-lfu' }),

  // Cache "warm" : données moyennement accédées, TTL plus long
  warm: new Redis({ host: 'redis-warm', maxmemory: '2gb', policy: 'allkeys-lru' }),

  // Cache "sessions" : isolé pour garantir la disponibilité des sessions
  sessions: new Redis({ host: 'redis-sessions', maxmemory: '1gb', policy: 'noeviction' }),
};

// Choisir le cache selon le type de donnée
function getCache(dataType: 'product' | 'user' | 'session' | 'search'): Redis {
  if (dataType === 'session') return caches.sessions;
  if (dataType === 'product' || dataType === 'search') return caches.hot;
  return caches.warm;
}
```

## Monitoring de l'efficacité du cache

```typescript
// Métriques clés à suivre en production
interface CacheMetrics {
  hitRate: number;          // Cible : > 85-95% selon le cas d'usage
  missRate: number;         // = 1 - hitRate
  evictionRate: number;     // Si > 0 régulièrement : augmenter maxmemory
  latencyP50: number;       // Devrait être < 1ms pour Redis
  latencyP99: number;       // Devrait être < 5ms pour Redis
}

class InstrumentedCache {
  private hits = 0;
  private misses = 0;

  async get<T>(key: string): Promise<T | null> {
    const start = process.hrtime.bigint();
    const value = await this.redis.get(key);
    const latencyMs = Number(process.hrtime.bigint() - start) / 1_000_000;

    if (value) {
      this.hits++;
      metrics.histogram('cache.get.latency', latencyMs, { result: 'hit' });
    } else {
      this.misses++;
      metrics.histogram('cache.get.latency', latencyMs, { result: 'miss' });
    }

    metrics.gauge('cache.hit_rate', this.hits / (this.hits + this.misses));
    return value ? JSON.parse(value) : null;
  }
}
```

## Testing du cache

```typescript
// Test unitaire : mocker le cache pour isoler la logique métier
describe('UserRepository', () => {
  it('retourne la valeur du cache sans appeler la DB', async () => {
    const mockRedis = { get: jest.fn().mockResolvedValue(JSON.stringify(mockUser)) };
    const repo = new UserRepository(mockRedis as any, mockDb);

    const user = await repo.findById('42');

    expect(mockDb.query).not.toHaveBeenCalled(); // DB non consultée
    expect(user).toEqual(mockUser);
  });
});

// Test d'intégration avec Redis réel (testcontainers)
import { GenericContainer } from 'testcontainers';

describe('Cache intégration', () => {
  let redisContainer: StartedTestContainer;

  beforeAll(async () => {
    redisContainer = await new GenericContainer('redis:7-alpine')
      .withExposedPorts(6379)
      .start();
  });

  afterAll(() => redisContainer.stop());

  it('survit à un FLUSHALL (chaos test)', async () => {
    await cache.set('key', 'value', 60);
    await redis.flushall(); // Simuler une perte totale du cache
    const result = await cache.get('key'); // Doit fallback sur la DB sans erreur
    expect(result).not.toBeNull(); // La donnée est récupérée depuis la DB
  });
});
```
