# Cache Distribué et Multi-Niveaux — CDN, Browser et L1/L2

Un système de cache performant n'est pas monolithique. C'est une architecture en couches où chaque niveau complète le suivant : de la mémoire process ultra-rapide jusqu'au CDN global. Maîtriser cette architecture multi-niveaux, les headers HTTP et l'intégration CDN est ce qui permet d'atteindre des latences sub-milliseconde pour les utilisateurs du monde entier.

## Architecture multi-niveaux complète

```
Requête utilisateur
       ↓
  [L0] Browser Cache      ← 0ms — mémoire locale du navigateur
       ↓ (miss)
  [L1] CDN (Cloudflare)   ← 1-5ms — edge le plus proche géographiquement
       ↓ (miss)
  [L2] L1 Process Cache   ← 0.1ms — LRU en mémoire du pod Node.js
       ↓ (miss)
  [L3] Redis (L2 partagé) ← 1-5ms — partagé entre tous les pods
       ↓ (miss)
  [L4] Base de données    ← 10-100ms — source de vérité
```

### L1 — Cache mémoire process (In-Process LRU)

```typescript
import LRU from 'lru-cache';

const l1Cache = new LRU<string, unknown>({
  max: 500,                    // Maximum 500 entrées (protège la mémoire du pod)
  ttl: 1000 * 30,             // 30 secondes — court pour éviter le stale excessif
  allowStale: false,           // Ne pas servir les entrées expirées
  updateAgeOnGet: false,       // Ne pas réinitialiser le TTL à chaque lecture
  sizeCalculation: (value) => JSON.stringify(value).length, // Taille en octets
  maxSize: 50 * 1024 * 1024,  // 50 MB max de mémoire
});

// Wrapper multi-niveaux L1 + L2 (Redis)
async function get<T>(key: string, loader: () => Promise<T>, ttl: number): Promise<T> {
  // L1 : cache mémoire local — ultra-rapide
  const l1Value = l1Cache.get(key) as T | undefined;
  if (l1Value !== undefined) {
    metrics.increment('cache.l1.hit');
    return l1Value;
  }

  // L2 : Redis — partagé entre pods
  const l2Value = await redis.get(key);
  if (l2Value) {
    const parsed = JSON.parse(l2Value) as T;
    l1Cache.set(key, parsed); // Peupler le L1 depuis le L2
    metrics.increment('cache.l2.hit');
    return parsed;
  }

  // L3 : source de données
  metrics.increment('cache.miss');
  const value = await loader();
  await redis.set(key, JSON.stringify(value), 'EX', ttl);
  l1Cache.set(key, value);
  return value;
}
```

**Caractéristiques du L1** : sub-milliseconde, limité à la taille du pod, local (chaque instance a son propre L1), pas partagé entre pods.

**Problème du L1** : quand Redis invalide une clé, les autres pods conservent leur copie L1 jusqu'à expiration. Solution : pub/sub pour invalider le L1 cross-instances.

### Invalidation cohérente du L1 via Pub/Sub

```typescript
class MultiLevelCache {
  private readonly INVALIDATION_CHANNEL = 'cache:invalidate';

  constructor(
    private redis: Redis,
    private subscriber: Redis, // Connexion dédiée au subscribe
    private l1: LRU<string, unknown>,
  ) {
    this.setupInvalidationListener();
  }

  private setupInvalidationListener(): void {
    this.subscriber.subscribe(this.INVALIDATION_CHANNEL);
    this.subscriber.on('message', (_, message) => {
      const { keys } = JSON.parse(message) as { keys: string[] };
      // Invalider le L1 local quand un autre pod invalide Redis
      keys.forEach(key => this.l1.delete(key));
    });
  }

  async invalidate(keys: string[]): Promise<void> {
    // Supprimer de Redis (L2)
    if (keys.length) await this.redis.del(...keys);
    // Invalider le L1 local immédiatement
    keys.forEach(key => this.l1.delete(key));
    // Notifier tous les autres pods d'invalider leur L1
    await this.redis.publish(
      this.INVALIDATION_CHANNEL,
      JSON.stringify({ keys })
    );
  }
}
```

## HTTP Cache-Control — Guide complet des directives

Le header `Cache-Control` est le levier le plus puissant pour contrôler le comportement des caches intermédiaires (CDN, proxy) et du navigateur.

```typescript
// Configurations typiques selon le type de ressource
const CACHE_POLICIES = {
  // Assets statiques avec fingerprint dans le nom (bundle.a1b2c3.js)
  // Immutables pour toujours — le CDN peut les garder indéfiniment
  staticAssets: 'public, max-age=31536000, immutable',

  // Pages HTML — fraîches 5 minutes, stale acceptable pendant 1h de revalidation
  htmlPages: 'public, max-age=300, stale-while-revalidate=3600',

  // Données API publiques — fresh 60s, stale-if-error pour la résilience
  publicApi: 'public, max-age=60, stale-while-revalidate=120, stale-if-error=86400',

  // Données API privées (authentifiées) — jamais mis en cache par les CDN
  privateApi: 'private, no-cache',

  // Pages de paiement, formulaires sensibles — aucun cache nulle part
  sensitive: 'no-store',
};

// Middleware Express avec politique par route
app.use('/api/products', (req, res, next) => {
  res.set('Cache-Control', CACHE_POLICIES.publicApi);
  next();
});

app.use('/api/account', requireAuth, (req, res, next) => {
  res.set('Cache-Control', CACHE_POLICIES.privateApi);
  next();
});

app.use('/assets', express.static('public', {
  setHeaders: (res) => {
    res.set('Cache-Control', CACHE_POLICIES.staticAssets);
  },
}));
```

### Tableau des directives Cache-Control

| Directive                  | Qui est affecté        | Signification                                          |
|----------------------------|------------------------|--------------------------------------------------------|
| `max-age=N`                | Browser + CDN          | Valide pendant N secondes                              |
| `s-maxage=N`               | CDN uniquement         | Remplace max-age pour les caches partagés              |
| `public`                   | CDN                    | Peut être mis en cache par les caches partagés         |
| `private`                  | Browser uniquement     | Ne pas mettre en cache dans les caches partagés        |
| `no-cache`                 | Browser + CDN          | Toujours revalider (peut servir stale si revalidation OK) |
| `no-store`                 | Partout                | N'écrire la réponse nulle part (RGPD, données sensibles) |
| `immutable`                | Browser                | Ne jamais revalider même si max-age expiré (F5 inclus) |
| `stale-while-revalidate=N` | Browser + CDN (si supporté) | Servir stale pendant N secondes pendant revalidation |
| `stale-if-error=N`         | Browser + CDN          | Servir stale si la source répond avec une erreur       |
| `must-revalidate`          | Partout                | Ne jamais servir stale même en cas d'erreur réseau     |
| `vary: Accept-Language`    | CDN                    | Cacher des copies différentes selon le header Vary     |

## CDN — Configuration Cloudflare et Fastly

### Cloudflare Cache Rules (nouvelle interface)

```typescript
// cloudflare-cache-rules.ts — Générer des règles Cloudflare via l'API
const rules = [
  {
    description: 'Cache les assets statiques 1 an',
    expression: '(http.request.uri.path matches "^/assets/.*\\.[a-f0-9]{8}\\.")',
    action: 'set_cache_settings',
    action_parameters: {
      cache: true,
      edge_ttl: { mode: 'override', value: 31536000 },
      browser_ttl: { mode: 'override', value: 31536000 },
    },
  },
  {
    description: 'Bypasser le cache pour les API authentifiées',
    expression: '(http.request.uri.path matches "^/api/") and (http.request.headers["authorization"] exists)',
    action: 'bypass_cache',
  },
  {
    description: 'Cache les pages produit 10 minutes',
    expression: '(http.request.uri.path matches "^/products/")',
    action: 'set_cache_settings',
    action_parameters: {
      cache: true,
      edge_ttl: { mode: 'override', value: 600 },
      cache_key: {
        custom_key: {
          header: { include: ['accept-language'] }, // Vary par langue
        },
      },
    },
  },
];

// Purge par Cache-Tag (nécessite plan Cloudflare Business ou Enterprise)
async function purgeByTag(tags: string[]): Promise<void> {
  await fetch(`https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/cache/purge`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${CF_API_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ tags }),
  });
}
```

### Fastly VCL (Varnish Configuration Language)

```vcl
// fastly_recv.vcl
sub vcl_recv {
  // Ne pas cacher les requêtes authentifiées
  if (req.http.Authorization) {
    return(pass);
  }

  // Ne pas cacher les méthodes non-idempotentes
  if (req.method != "GET" && req.method != "HEAD") {
    return(pass);
  }

  // Normaliser les URLs (supprimer les paramètres de tracking)
  set req.url = querystring.regsuball(req.url, "utm_[^&]+&?", "");
  set req.url = querystring.regsuball(req.url, "[&?]$", "");

  #FASTLY recv
  return(hash);
}

// fastly_backend_response.vcl
sub vcl_backend_response {
  // Override TTL pour les ressources statiques
  if (beresp.http.Content-Type ~ "^(text/css|application/javascript|image/)") {
    set beresp.ttl = 365d;
    set beresp.http.Cache-Control = "public, max-age=31536000, immutable";
  }

  // Grace mode : servir stale pendant la revalidation (comme stale-while-revalidate)
  set beresp.grace = 1h;

  #FASTLY beresp
  return(deliver);
}
```

## Vary Header — Cache par variante

Le header `Vary` indique aux caches de stocker des copies séparées selon certains headers de requête. À utiliser avec précaution : un `Vary: *` vide complètement l'efficacité du cache.

```typescript
// API multilingue : cacher une version par langue
app.get('/api/products', (req, res) => {
  const lang = req.headers['accept-language']?.split(',')[0] || 'fr';
  res.set({
    'Content-Type': 'application/json',
    'Vary': 'Accept-Language',            // CDN cacherait une copie par langue
    'Cache-Control': 'public, max-age=600',
    'Content-Language': lang,
  });
  res.json(getProducts(lang));
});

// Eviter Vary: Cookie (annule le cache CDN pour tous les utilisateurs connectés)
// Eviter Vary: User-Agent (crée trop de variantes)
// Préférer : Vary: Accept-Language, Accept-Encoding uniquement
```

## Edge Caching avec Next.js

Next.js 13+ intègre le cache CDN nativement via les Server Components et le Data Cache.

```typescript
// app/products/[id]/page.tsx
// Fetch avec tags de cache — invalider par tag depuis n'importe quel endpoint
async function getProduct(id: string): Promise<Product> {
  const res = await fetch(`${API_URL}/products/${id}`, {
    next: {
      revalidate: 600,                           // ISR : revalider toutes les 10min
      tags: [`product:${id}`, 'catalog'],        // Tags pour invalidation ciblée
    },
  });
  return res.json();
}

// app/api/webhooks/pim/route.ts — Webhook déclenché par le PIM lors d'une mise à jour
import { revalidateTag, revalidatePath } from 'next/cache';

export async function POST(request: Request): Promise<Response> {
  const { productId, type } = await request.json();

  if (type === 'product.updated') {
    // Invalider seulement les caches de ce produit — pas tout le catalogue
    revalidateTag(`product:${productId}`);
    console.log(`Cache invalidé pour product:${productId}`);
  }

  if (type === 'catalog.rebuilt') {
    // Invalider tout le catalogue
    revalidateTag('catalog');
  }

  return Response.json({ revalidated: true });
}

// next.config.ts — Configurer les headers CDN globaux
const nextConfig = {
  async headers() {
    return [
      {
        source: '/_next/static/:path*',
        headers: [{ key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }],
      },
      {
        source: '/products/:path*',
        headers: [{ key: 'Cache-Control', value: 'public, s-maxage=600, stale-while-revalidate=86400' }],
      },
    ];
  },
};
```

## Varnish VCL — Cache serveur hautes performances

Varnish est un reverse proxy cache que l'on place devant l'application. Il offre un contrôle très fin via son langage VCL.

```vcl
vcl 4.1;

backend default {
  .host = "app";
  .port = "3000";
  .connect_timeout = 2s;
  .first_byte_timeout = 30s;
}

sub vcl_recv {
  // Supprimer les cookies pour les ressources statiques
  if (req.url ~ "\.(css|js|png|jpg|svg|woff2)(\?.*)?$") {
    unset req.http.Cookie;
  }

  // Clé de cache personnalisée : inclure le tenant depuis le sous-domaine
  set req.http.X-Tenant = regsub(req.http.Host, "^([^.]+)\..*$", "\1");
}

sub vcl_backend_response {
  // Grace mode : servir stale jusqu'à 1h pendant la revalidation du backend
  set beresp.grace = 1h;

  // Allonger le TTL des ressources statiques hashées
  if (bereq.url ~ "\.[a-f0-9]{8}\.(css|js)") {
    set beresp.ttl = 365d;
    unset beresp.http.Set-Cookie;
  }
}

sub vcl_deliver {
  // Ajouter des headers de debug en développement
  if (req.http.X-Debug == "true") {
    if (obj.hits > 0) {
      set resp.http.X-Cache = "HIT";
      set resp.http.X-Cache-Hits = obj.hits;
    } else {
      set resp.http.X-Cache = "MISS";
    }
    set resp.http.X-Cache-TTL = obj.ttl;
  }
}
```

## Browser Cache — ServiceWorker Workbox

Les ServiceWorkers permettent un contrôle granulaire du cache navigateur, au-delà de ce que les headers HTTP autorisent.

```typescript
// service-worker.ts (avec Workbox)
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';

// Assets statiques hashés : CacheFirst (ils ne changeront jamais)
registerRoute(
  ({ url }) => url.pathname.startsWith('/assets/'),
  new CacheFirst({
    cacheName: 'static-assets-v1',
    plugins: [
      new CacheableResponsePlugin({ statuses: [200] }),
      new ExpirationPlugin({ maxEntries: 100, maxAgeSeconds: 365 * 24 * 60 * 60 }),
    ],
  })
);

// Pages HTML : NetworkFirst (fraîcheur prioritaire) avec fallback offline
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({
    cacheName: 'pages-cache',
    plugins: [
      new CacheableResponsePlugin({ statuses: [200] }),
      new ExpirationPlugin({ maxEntries: 50, maxAgeSeconds: 24 * 60 * 60 }),
    ],
    networkTimeoutSeconds: 3, // Fallback sur le cache si le réseau est lent
  })
);

// API data : StaleWhileRevalidate (équilibre fraîcheur/performance)
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/products'),
  new StaleWhileRevalidate({
    cacheName: 'api-products',
    plugins: [
      new CacheableResponsePlugin({ statuses: [200] }),
      new ExpirationPlugin({ maxEntries: 200, maxAgeSeconds: 10 * 60 }),
    ],
  })
);
```

### ETag et Last-Modified — Revalidation conditionnelle

```typescript
// Middleware de revalidation conditionnelle avec ETag
app.get('/api/products/:id', async (req, res) => {
  const product = await getProduct(req.params.id);
  const etag = `"${hashObject(product)}"`;          // Hash déterministe
  const lastModified = product.updatedAt.toUTCString();

  // Vérifier si le client a déjà la bonne version
  if (req.headers['if-none-match'] === etag) {
    return res.status(304).end(); // Not Modified — pas de corps, économie de bande passante
  }

  res.set({
    'ETag': etag,
    'Last-Modified': lastModified,
    'Cache-Control': 'public, max-age=60, must-revalidate',
  });

  res.json(product);
});
```

## Consistent Hashing — Distribution des clés

Dans un cache distribué multi-nœuds, le consistent hashing garantit que l'ajout ou la suppression d'un nœud ne remplace qu'une fraction minimale des clés (1/N en moyenne, contre 100% avec un modulo simple).

```typescript
import ConsistentHashing from 'consistent-hashring';

// Virtual nodes (vnodes) : augmenter la dispersion pour éviter les hotspots
const ring = new ConsistentHashing({
  vnodesCount: 150, // 150 positions virtuelles par nœud réel
});

// Ajouter les nœuds Redis
const nodes = ['redis-1:6379', 'redis-2:6379', 'redis-3:6379'];
nodes.forEach(node => ring.add(node));

// Résoudre quel nœud héberge une clé donnée
function getNodeForKey(key: string): string {
  return ring.get(key);
}

// Ajouter un nœud (seul 1/4 des clés migre — pas toutes)
ring.add('redis-4:6379');

// Supprimer un nœud gracieusement
ring.remove('redis-3:6379');
// → Les clés qui étaient sur redis-3 se redistribuent sur redis-1 et redis-2
```

**Importance pour le cache** : sans consistent hashing, l'ajout d'un nœud invalide tout le cache (remapping de toutes les clés). Avec consistent hashing, seulement les clés migrées génèrent des misses temporaires.

## Cache Cohérence vs Disponibilité — CAP theorem appliqué

```
          C (Cohérence)
         / \
        /   \
       / CP  \
      /-------\
     /    CA   \
    /           \
   A-------------P
(Disponibilité) (Tolérance partition)
```

**Le cache est AP par nature** : on choisit la disponibilité et la tolérance aux partitions au détriment de la cohérence stricte. La cohérence est éventuelle, pas immédiate.

```typescript
// Graceful degradation : si Redis est down, continuer à fonctionner
async function getWithFallback<T>(
  key: string,
  loader: () => Promise<T>,
  ttl: number
): Promise<T> {
  try {
    const cached = await redis.get(key);
    if (cached) return JSON.parse(cached);

    const value = await loader();
    await redis.set(key, JSON.stringify(value), 'EX', ttl).catch(() => {
      // Ignorer les erreurs d'écriture dans le cache — ne pas faire échouer la requête
      console.warn('Cache write failed — continuing without cache');
    });
    return value;
  } catch (error) {
    if (error instanceof RedisConnectionError) {
      // Cache complètement indisponible : fallback direct sur la source
      console.error('Redis indisponible — fallback sur la DB');
      return loader(); // Dégradation gracieuse : plus lent mais fonctionnel
    }
    throw error;
  }
}
```

## Analyse de coûts — Redis vs Cloudflare KV vs Memcached

| Solution              | Coût (10GB, 10M req/mois) | Latence        | Limite taille valeur | Structures      |
|-----------------------|--------------------------|----------------|----------------------|-----------------|
| Redis Cloud (Upstash) | ~50$/mois (pay-per-req)  | 1-5ms          | 512 MB               | Toutes          |
| Redis Enterprise      | ~200$/mois (managed)     | < 1ms (même DC)| 512 MB               | Toutes          |
| Cloudflare KV         | ~5$/mois + usage         | < 25ms (global)| 25 MB                | Clé-valeur seul |
| Memcached (EC2)       | ~80$/mois (instance)     | < 1ms          | 1 MB                 | String uniquement|
| Upstash Redis         | ~30$/mois (serverless)   | 1-10ms         | 100 MB               | Toutes          |

**Règle de calcul du ROI** :

```
Coût DB query évitée = (temps_moyen_query_ms / 1000) × coût_CPU_par_seconde
                     + (taux_requêtes/heure × coût_instance_DB)

ROI cache = (requêtes_évitées_par_heure × coût_DB_query_évitée) - coût_cache_par_heure

Exemple :
- Query PostgreSQL moyenne : 50ms, 1000 requêtes/heure
- Instance RDS db.t3.medium : 0.068$/heure
- Redis ElastiCache cache.t3.micro : 0.017$/heure
- ROI = 1000 × (50ms × CPU_cost) + (réduction charge DB × $0.068) - $0.017
```

**Cas général** : le cache Redis est rentable dès 100 requêtes/heure pour une query DB supérieure à 20ms, avec un ROI typiquement de 5x à 20x le coût du cache.
