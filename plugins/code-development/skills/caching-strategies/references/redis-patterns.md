# Redis Patterns Avancés — Structures, Lua et Cluster

Redis est bien plus qu'un simple cache clé-valeur. La maîtrise de ses structures de données natives, de son modèle d'exécution atomique et de ses topologies distribuées est ce qui distingue une implémentation naïve d'une architecture de cache robuste et performante en production.

## Structures de données Redis — Choisir la bonne structure

Redis propose 8 structures de données distinctes. Utiliser la mauvaise structure est la source la plus fréquente de problèmes de performance et de mémoire.

### Tableau de sélection des structures

| Structure       | Cas d'usage principal                                  | Complexité lookup | Mémoire     |
|-----------------|--------------------------------------------------------|-------------------|-------------|
| String          | Cache simple, compteurs, verrous distribués            | O(1)              | Faible      |
| Hash            | Objets avec champs multiples (profil utilisateur)      | O(1) par champ    | Très faible |
| List            | File de tâches (queue), historique ordonné             | O(1) tête/queue   | Moyenne     |
| Set             | Tags, relations M:N, unicité                           | O(1)              | Moyenne     |
| Sorted Set      | Classements, files de priorité, range queries         | O(log N)          | Haute       |
| HyperLogLog     | Comptage d'éléments uniques approximatif              | O(1)              | 12 KB fixe  |
| Bitmap          | Tracking booléen par position (activité par jour)     | O(1)              | Très faible |
| Stream          | Journal d'événements persistant, consumer groups      | O(1) ajout        | Variable    |

### String — Le couteau suisse

```typescript
// Cache simple avec TTL
await redis.set('user:42:profile', JSON.stringify(user), 'EX', 3600);
const cached = await redis.get('user:42:profile');

// Compteur atomique
await redis.incr('api:calls:2024-01-15');
await redis.incrby('stats:page_views', 5);

// Valeur avec expiration conditionnelle (SET NX = set if not exists)
const acquired = await redis.set('lock:resource:42', 'owner-uuid', 'EX', 30, 'NX');
if (!acquired) throw new Error('Ressource déjà verrouillée');
```

### Hash — Objets efficaces en mémoire

Les Hash consomment significativement moins de mémoire que des JSON sérialisés pour les objets avec de nombreux champs, grâce à l'encodage `ziplist` automatique de Redis pour les petits hashes.

```typescript
// Stocker un objet utilisateur champ par champ
await redis.hset('user:42', {
  nom: 'Dupont',
  email: 'dupont@example.com',
  plan: 'pro',
  derniere_connexion: Date.now().toString(),
});

// Lire un seul champ sans désérialiser l'objet entier
const plan = await redis.hget('user:42', 'plan');

// Incrémenter un champ numérique directement
await redis.hincrby('user:42', 'login_count', 1);

// Lire tous les champs
const user = await redis.hgetall('user:42');
```

### Sorted Set — Classements et range queries

```typescript
// Ajouter/mettre à jour un score
await redis.zadd('leaderboard:global', score, `user:${userId}`);

// Rang du joueur (0-indexé, du plus grand score)
const rank = await redis.zrevrank('leaderboard:global', `user:${userId}`);

// Top 100 avec leurs scores
const top100 = await redis.zrevrange('leaderboard:global', 0, 99, 'WITHSCORES');

// Tous les éléments dans une plage de scores
const actifs = await redis.zrangebyscore('sessions:actives', Date.now() - 3600000, '+inf');
```

## HyperLogLog — Comptage approximatif à mémoire constante

HyperLogLog résout un problème précis : compter des éléments uniques dans un flux massif sans stocker chaque élément individuellement. L'algorithme utilise des fonctions de hachage probabilistes pour estimer la cardinalité avec une précision de ±0.81% en utilisant seulement 12 KB de mémoire, quelle que soit la taille de l'ensemble.

**Cas d'usage typiques** : DAU (Daily Active Users), visiteurs uniques, IPs uniques, requêtes distinctes.

```typescript
// Enregistrer une visite unique (idempotent)
const dateKey = new Date().toISOString().split('T')[0]; // '2024-01-15'
await redis.pfadd(`dau:${dateKey}`, userId.toString());

// Compter les utilisateurs uniques du jour
const dauToday = await redis.pfcount(`dau:${dateKey}`);
console.log(`DAU aujourd'hui : ~${dauToday} utilisateurs`);

// Fusionner plusieurs périodes pour un total semaine
const semaine = ['2024-01-09', '2024-01-10', '2024-01-11', '2024-01-12',
                  '2024-01-13', '2024-01-14', '2024-01-15'];
const keys = semaine.map(d => `dau:${d}`);
await redis.pfmerge('dau:semaine:2024-W02', ...keys);
const wau = await redis.pfcount('dau:semaine:2024-W02');
```

Important : HyperLogLog ne permet pas de vérifier si un élément spécifique est présent (pas de lookup), et ne supporte pas la suppression d'éléments. Pour ces besoins, utiliser un Bloom Filter.

## Bitmap — Tracking d'activité en O(1)

Les Bitmaps permettent de représenter l'activité d'un utilisateur sur N jours avec N bits. Pour 365 jours, chaque utilisateur n'occupe que 46 octets — c'est la structure la plus économe en mémoire pour le tracking binaire.

```typescript
// Marquer l'utilisateur 42 comme actif aujourd'hui
const dayOfYear = getDayOfYear(new Date()); // 0-365
await redis.setbit(`active:2024`, dayOfYear, 1);

// Vérifier si l'utilisateur était actif un jour donné
const wasActive = await redis.getbit(`active:2024`, dayOfYear);

// Compter les jours actifs sur toute l'année
const activeDays = await redis.bitcount(`active:2024`);

// Compter les utilisateurs actifs sur un mois (BITOP AND entre les jours du mois)
// Tous les utilisateurs actifs TOUS les jours de janvier
await redis.bitop('AND', 'active:jan:all_days', ...january_daily_keys);
const retained = await redis.bitcount('active:jan:all_days');

// BITPOS : trouver le premier jour inactif
const firstInactiveDay = await redis.bitpos(`active:2024`, 0);
```

## Scripts Lua — Atomicité garantie

Les scripts Lua s'exécutent de manière atomique dans Redis : aucune autre commande ne peut s'intercaler pendant l'exécution. C'est essentiel pour les opérations qui doivent être atomiques mais ne peuvent pas être exprimées avec `MULTI/EXEC`.

### Rate limiting avec Lua

```lua
-- rate_limit.lua
-- KEYS[1] = clé du compteur (ex: "ratelimit:user:42:minute:2024-01-15T10:30")
-- ARGV[1] = limite (ex: "100")
-- ARGV[2] = fenêtre en secondes (ex: "60")
-- Retourne: {current_count, is_allowed}

local current = redis.call('GET', KEYS[1])
if current == false then
  redis.call('SET', KEYS[1], 1, 'EX', ARGV[2])
  return {1, 1}
end
current = tonumber(current)
if current >= tonumber(ARGV[1]) then
  return {current, 0}
end
return {redis.call('INCR', KEYS[1]), 1}
```

```typescript
// Chargement du script (SHA pour EVALSHA)
const script = fs.readFileSync('./rate_limit.lua', 'utf-8');
const sha = await redis.script('LOAD', script);

// Utilisation avec EVALSHA (plus performant qu'EVAL — pas de retransmission du script)
const windowKey = `ratelimit:user:${userId}:${getMinuteKey()}`;
const [count, allowed] = await redis.evalsha(sha, 1, windowKey, '100', '60') as [number, number];

if (!allowed) {
  throw new TooManyRequestsError(`Limite atteinte : ${count}/100 requêtes/minute`);
}
```

### Distributed Lock avec Lua (Redlock)

```lua
-- unlock.lua : libérer le verrou seulement si on est le propriétaire
-- Opération atomique GET + DEL indispensable
if redis.call('GET', KEYS[1]) == ARGV[1] then
  return redis.call('DEL', KEYS[1])
else
  return 0
end
```

```typescript
import Redlock from 'ioredis-redlock';

// Redlock nécessite plusieurs instances Redis indépendantes pour la tolérance aux pannes
const redlock = new Redlock([redis1, redis2, redis3], {
  driftFactor: 0.01,    // Dérive d'horloge tolérée (1%)
  retryCount: 3,
  retryDelay: 200,      // ms entre les tentatives
  retryJitter: 100,     // Jitter aléatoire pour éviter les thundering herds
});

async function withLock<T>(resource: string, ttl: number, fn: () => Promise<T>): Promise<T> {
  const lock = await redlock.acquire([`lock:${resource}`], ttl);
  try {
    return await fn();
  } finally {
    await lock.release();
  }
}

// Usage
await withLock('invoice:generate:order-789', 30000, async () => {
  // Section critique — un seul pod l'exécute à la fois
  await generateInvoice(orderId);
});
```

**Principe du Redlock** : pour acquérir le verrou, le client tente de l'acquérir sur N/2+1 noeuds minimum (quorum). Si le temps total d'acquisition dépasse le TTL, le verrou est considéré invalide et libéré automatiquement.

## Redis Cluster — Distribution horizontale

Redis Cluster distribue les données sur 16 384 hash slots répartis entre les nœuds. Chaque clé est assignée à un slot via `CRC16(key) % 16384`.

### Hash Tags pour les opérations multi-clés

```typescript
// PROBLÈME : ces clés peuvent être sur des slots différents
// MULTI/EXEC échoue si les clés sont sur des nœuds différents
await redis.mget('user:42:cart', 'user:42:wishlist'); // ❌ Potentiel CROSSSLOT error

// SOLUTION : hash tags {} — seule la partie entre {} détermine le slot
// Toutes ces clés seront sur le même slot (hash de "42")
await redis.mget('{user:42}:cart', '{user:42}:wishlist', '{user:42}:orders'); // ✅

// En TypeScript, préfixer systématiquement avec le hash tag
function userKey(userId: string, suffix: string): string {
  return `{user:${userId}}:${suffix}`;
}
const keys = ['cart', 'wishlist', 'orders'].map(s => userKey('42', s));
const values = await redis.mget(...keys);
```

### Resharding et failover

```bash
# Vérifier la distribution des slots
redis-cli --cluster info redis-node-1:6379

# Déplacer 1000 slots du nœud 1 vers le nœud 4 (resharding)
redis-cli --cluster reshard redis-node-1:6379 \
  --cluster-from <node1-id> \
  --cluster-to <node4-id> \
  --cluster-slots 1000 \
  --cluster-yes

# Vérifier l'état du cluster
redis-cli -h redis-node-1 cluster info
redis-cli -h redis-node-1 cluster nodes
```

Le failover automatique se déclenche quand un nœud master est inaccessible depuis les autres nœuds pendant `cluster-node-timeout` ms (défaut : 15s). Un nœud replica est promu master automatiquement.

## Redis Sentinel — Haute disponibilité sans Cluster

Sentinel convient pour les déploiements sans sharding mais avec besoin de haute disponibilité. Il monitore le master, détecte les pannes (quorum de Sentinels requis) et déclenche le failover.

```typescript
import { Redis } from 'ioredis';

const redis = new Redis({
  sentinels: [
    { host: 'sentinel-1', port: 26379 },
    { host: 'sentinel-2', port: 26379 },
    { host: 'sentinel-3', port: 26379 },
  ],
  name: 'mymaster',          // Nom du groupe défini dans sentinel.conf
  role: 'master',            // 'master' pour les écritures, 'slave' pour les lectures
  sentinelRetryStrategy: (times) => Math.min(times * 100, 3000),
});

// Connexion de lecture sur les replicas (load balancing)
const redisRead = new Redis({
  sentinels: [...],
  name: 'mymaster',
  role: 'slave',
  preferredSlaves: [{ ip: 'replica-1', port: '6379', prio: 1 }],
});
```

## Pub/Sub vs Streams

| Critère              | Pub/Sub                           | Streams                                   |
|----------------------|-----------------------------------|-------------------------------------------|
| Persistance          | Aucune (fire-and-forget)          | Oui (comme un log Kafka)                  |
| Consommateurs        | Tous reçoivent tous les messages  | Consumer groups (chaque message = 1 fois) |
| Replay               | Impossible                        | Possible (via ID de message)              |
| Garantie de livraison| At-most-once                      | At-least-once avec ACK                    |
| Cas d'usage          | Invalidation de cache, live chat  | Event sourcing, audit log, tâches async   |

```typescript
// Pub/Sub : invalidation de cache L1 cross-instances
await publisher.publish('cache:invalidate', JSON.stringify({ key: 'user:42:profile' }));

subscriber.on('message', (channel, message) => {
  const { key } = JSON.parse(message);
  localCache.delete(key); // Invalider le cache mémoire local
});
await subscriber.subscribe('cache:invalidate');

// Streams : queue de tâches fiable avec Consumer Groups
await redis.xadd('tasks:emails', '*', 'to', 'user@example.com', 'template', 'welcome');
await redis.xgroup('CREATE', 'tasks:emails', 'email-workers', '$', 'MKSTREAM');

// Consommateur
const messages = await redis.xreadgroup(
  'GROUP', 'email-workers', 'worker-1',
  'COUNT', 10, 'BLOCK', 2000, 'STREAMS', 'tasks:emails', '>'
);
// Après traitement, acquitter
await redis.xack('tasks:emails', 'email-workers', messageId);
```

## Pipeline et Transactions

```typescript
// Pipeline : envoyer plusieurs commandes en un seul round-trip réseau
// Pas atomique — les commandes peuvent être interleaved avec d'autres clients
const pipeline = redis.pipeline();
pipeline.set('key1', 'val1');
pipeline.set('key2', 'val2');
pipeline.get('key1');
const results = await pipeline.exec(); // [[null, 'OK'], [null, 'OK'], [null, 'val1']]

// MULTI/EXEC : atomique, mais pas de logique conditionnelle
const multi = redis.multi();
multi.incr('counter');
multi.expire('counter', 3600);
await multi.exec();

// WATCH + MULTI/EXEC : transaction optimiste
// Si 'balance' change entre WATCH et EXEC, la transaction échoue (retourne null)
async function transfert(from: string, to: string, amount: number): Promise<boolean> {
  return new Promise((resolve) => {
    redis.watch(from, async (err) => {
      const balance = parseInt(await redis.get(from) || '0');
      if (balance < amount) { await redis.unwatch(); return resolve(false); }
      const result = await redis.multi()
        .decrby(from, amount)
        .incrby(to, amount)
        .exec();
      resolve(result !== null); // null = conflit détecté, retry nécessaire
    });
  });
}
```

## Memory Optimization et Politiques d'éviction

```bash
# Configuration maxmemory et politique d'éviction dans redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lfu  # LFU : évicte les moins fréquemment utilisés

# Politiques disponibles :
# noeviction        : erreur si mémoire pleine (pour DB, pas cache)
# allkeys-lru       : LRU sur toutes les clés (bon défaut pour cache)
# allkeys-lfu       : LFU — meilleur pour les workloads Zipf (quelques clés très hot)
# volatile-lru      : LRU uniquement sur clés avec TTL
# volatile-lfu      : LFU uniquement sur clés avec TTL
# allkeys-random    : éviction aléatoire
# volatile-ttl      : évicte en priorité les clés qui expirent bientôt
```

```bash
# Inspecter l'encodage mémoire d'une clé
OBJECT ENCODING user:42           # → "ziplist" (compact) ou "hashtable" (large)
OBJECT IDLETIME user:42           # Secondes depuis le dernier accès
OBJECT FREQ user:42               # Fréquence d'accès (LFU)

# Taille mémoire d'une clé (octets)
MEMORY USAGE user:42

# Rapport mémoire global
INFO memory
```

Les Hashes avec moins de 128 champs et des valeurs inférieures à 64 octets utilisent l'encodage `ziplist` (compact linéaire). Au-delà, Redis bascule automatiquement en `hashtable`. Configurer `hash-max-ziplist-entries` et `hash-max-ziplist-value` pour contrôler ce seuil.

## Monitoring Redis en production

```bash
# Métriques globales — la commande la plus importante
INFO all
INFO replication  # État master/replica
INFO stats        # keyspace_hits, keyspace_misses, evicted_keys
INFO memory       # used_memory, mem_fragmentation_ratio

# Commandes lentes (toutes les commandes > 10ms dans les 128 dernières)
SLOWLOG GET 10
SLOWLOG LEN    # Nombre de commandes lentes enregistrées
SLOWLOG RESET

# Latence par événement
LATENCY HISTORY event
LATENCY LATEST     # Dernière latence mesurée par type d'événement
LATENCY RESET

# MONITOR : affiche toutes les commandes en temps réel
# DANGER EN PRODUCTION : peut diviser par 2 les performances
# Utiliser uniquement en debug et couper immédiatement après
MONITOR

# Calculer le hit rate depuis les statistiques
# hit_rate = keyspace_hits / (keyspace_hits + keyspace_misses)
```

```yaml
# prometheus redis_exporter — docker-compose snippet
redis-exporter:
  image: oliver006/redis_exporter:latest
  environment:
    REDIS_ADDR: "redis:6379"
    REDIS_PASSWORD: "${REDIS_PASSWORD}"
  ports:
    - "9121:9121"
```

```yaml
# Alertes Prometheus recommandées
groups:
  - name: redis
    rules:
      - alert: RedisHighMemoryUsage
        expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.85
        for: 5m
        annotations:
          summary: "Redis utilise plus de 85% de sa mémoire allouée"

      - alert: RedisLowHitRate
        expr: |
          redis_keyspace_hits_total /
          (redis_keyspace_hits_total + redis_keyspace_misses_total) < 0.80
        for: 10m
        annotations:
          summary: "Hit rate Redis < 80% — vérifier la configuration du cache"

      - alert: RedisEvictingKeys
        expr: rate(redis_evicted_keys_total[5m]) > 100
        for: 2m
        annotations:
          summary: "Redis évicte des clés — augmenter maxmemory ou réduire le TTL"
```

## Checklist de production Redis

- Configurer `maxmemory` et `maxmemory-policy` explicitement (jamais laisser par défaut)
- Activer la persistance RDB ou AOF selon le besoin de durabilité
- Utiliser `requirepass` et TLS en production (Redis 6+)
- Désactiver les commandes dangereuses : `RENAME-COMMAND FLUSHALL ""` dans redis.conf
- Monitorer `mem_fragmentation_ratio` — si > 1.5, considérer un `MEMORY PURGE`
- Tester la procédure de failover Sentinel/Cluster en pré-production
- Documenter les conventions de nommage des clés dans le wiki de l'équipe
