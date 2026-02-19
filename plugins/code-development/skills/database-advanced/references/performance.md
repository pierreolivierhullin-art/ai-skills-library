# Performance PostgreSQL — EXPLAIN ANALYZE et Optimisation

## EXPLAIN ANALYZE : lire le plan d'exécution

`EXPLAIN ANALYZE` exécute réellement la requête et retourne le plan avec les statistiques mesurées. C'est la seule source de vérité pour comprendre pourquoi une requête est lente.

```sql
-- Toujours utiliser BUFFERS pour voir les accès disque vs cache
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.id, u.email, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.email
ORDER BY order_count DESC
LIMIT 50;
```

### Déchiffrer les nœuds du plan

**Seq Scan** : parcours séquentiel de toute la table. Acceptable pour les petites tables ou quand la sélectivité est faible (> 10-20% des lignes).

**Index Scan** : utilise un index B-tree pour trouver les lignes, puis va chercher les données dans le heap (table principale). Chaque accès heap = potentiellement un I/O aléatoire.

**Index Only Scan** : toutes les colonnes nécessaires sont dans l'index (`INCLUDE` ou colonnes indexées). Pas d'accès heap → beaucoup plus rapide. Nécessite que le visibility map soit à jour (autovacuum).

**Bitmap Index Scan + Bitmap Heap Scan** : PostgreSQL collecte d'abord tous les pointeurs via l'index (Bitmap Index Scan), puis les trie et accède au heap de façon séquentielle (Bitmap Heap Scan). Plus efficace qu'un Index Scan pur quand de nombreuses lignes correspondent.

**Hash Join** : table la plus petite est chargée en mémoire dans une table de hachage, puis la plus grande est parcourue. Optimal pour les grandes jointures sans index.

**Merge Join** : les deux entrées sont triées (ou déjà triées via un index), puis fusionnées. Très efficace si les données sont déjà ordonnées.

**Nested Loop** : pour chaque ligne de la table extérieure, on cherche les lignes correspondantes dans la table intérieure. Excellent si la table intérieure a un index et que peu de lignes correspondent.

### Interpréter les coûts et les lignes

```
-> Index Scan using idx_orders_user_id on orders  (cost=0.43..8.45 rows=1 width=52)
                                                          ^^^^^^^  ^^^^^^^  ^^^^
                                                          startup  total    estimated rows
   (actual time=0.021..0.024 rows=3 loops=1)
              ^^^^^^^  ^^^^^^^  ^^^^^^  ^^^^^^
              startup  total    actual  how many
              actual   actual   rows    times this node ran
```

- **cost startup** : coût avant de retourner la première ligne (important pour les LIMIT)
- **cost total** : coût estimé pour retourner toutes les lignes
- **rows** estimés vs **rows** actuels : si très différents, les statistiques sont obsolètes → `ANALYZE`
- **loops** : le nœud a été exécuté N fois (dans un Nested Loop, le nœud intérieur tourne une fois par ligne extérieure)

### Buffers : comprendre les accès disque

```
Buffers: shared hit=1243 read=4521
```

- **shared hit** : pages trouvées dans le cache partagé PostgreSQL (shared_buffers) → très rapide
- **read** : pages lues depuis le disque (ou l'OS page cache) → lent
- **written** : pages écrites (dirty) pendant l'exécution

Un ratio `hit / (hit + read)` faible indique que le cache est insuffisant ou que la table est rarement accédée.

---

## pg_stat_statements : identifier les requêtes lentes

```sql
-- Activer l'extension (dans postgresql.conf ou via ALTER SYSTEM)
-- shared_preload_libraries = 'pg_stat_statements'
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 des requêtes par temps total cumulé
SELECT
  LEFT(query, 100)                                        AS query_preview,
  calls,
  ROUND(total_exec_time::NUMERIC / 1000, 2)               AS total_sec,
  ROUND(mean_exec_time::NUMERIC, 2)                       AS mean_ms,
  ROUND(stddev_exec_time::NUMERIC, 2)                     AS stddev_ms,
  ROUND(max_exec_time::NUMERIC, 2)                        AS max_ms,
  rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Top 10 par temps moyen (requêtes unitairement lentes)
SELECT
  LEFT(query, 100) AS query_preview,
  calls,
  ROUND(mean_exec_time::NUMERIC, 2) AS mean_ms,
  ROUND(max_exec_time::NUMERIC, 2)  AS max_ms
FROM pg_stat_statements
WHERE calls > 100  -- Exclure les requêtes rares
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Réinitialiser les statistiques (après une optimisation)
SELECT pg_stat_statements_reset();
```

Les requêtes sont normalisées : les valeurs littérales sont remplacées par `$1`, `$2`, ce qui groupe les requêtes identiques avec des paramètres différents.

---

## Autovacuum tuning

L'autovacuum recycle les lignes mortes (MVCC) et met à jour les statistiques. Une table avec beaucoup d'UPDATE/DELETE accumule du "bloat" si l'autovacuum ne suit pas.

### Paramètres clés

```sql
-- Voir la configuration actuelle par table
SELECT
  relname,
  n_live_tup,
  n_dead_tup,
  ROUND(n_dead_tup::NUMERIC / NULLIF(n_live_tup, 0) * 100, 2) AS dead_pct,
  last_vacuum,
  last_autovacuum,
  last_analyze,
  last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 20;
```

### Tuner l'autovacuum pour les tables haute écriture

Les paramètres globaux (`autovacuum_vacuum_scale_factor = 0.2`) signifient que l'autovacuum se déclenche quand 20% des lignes sont mortes. Sur une table de 10 millions de lignes, il faut donc 2 millions de lignes mortes. C'est trop tardif.

```sql
-- Surcharger les paramètres pour une table spécifique
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.01,    -- Déclencher à 1% (vs 20% global)
  autovacuum_analyze_scale_factor = 0.005,  -- Analyser à 0.5%
  autovacuum_vacuum_cost_delay = 2,         -- Moins de pause entre les pages (défaut: 20ms)
  autovacuum_vacuum_threshold = 100         -- Minimum 100 lignes mortes
);

-- Pour une table de logs très active (écriture intense)
ALTER TABLE event_logs SET (
  autovacuum_vacuum_scale_factor = 0.001,
  autovacuum_vacuum_cost_limit = 800        -- Permettre plus d'I/O (défaut: 200)
);
```

---

## Statistiques et planificateur

### ANALYZE et pg_stats

```sql
-- Forcer la mise à jour des statistiques
ANALYZE products;                    -- Une table
ANALYZE VERBOSE products;            -- Avec détails par colonne
ANALYZE;                             -- Toute la base

-- Inspecter les statistiques collectées
SELECT
  attname       AS colonne,
  n_distinct,   -- Négatif = fraction des lignes distinctes (ex. -0.5 = 50% distinct)
  correlation,  -- Entre -1 et 1 : corrélation avec l'ordre physique (1 = parfait, 0 = aléatoire)
  most_common_vals,
  most_common_freqs
FROM pg_stats
WHERE tablename = 'orders'
  AND schemaname = 'public'
ORDER BY attname;
```

Une `correlation` proche de 1 ou -1 favorise les Index Scans (les pages accédées sont proches physiquement). Une `correlation` proche de 0 favorise les Bitmap Scans ou les Seq Scans.

### Augmenter la cible de statistiques pour les colonnes sélectives

```sql
-- Par défaut, statistics_target = 100 (échantillon de ~300 valeurs)
-- Pour les colonnes avec distribution complexe
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;
ANALYZE orders;
```

---

## Index avancés

### BRIN : Block Range INdex

Extrêmement compact. Stocke uniquement les valeurs min/max par bloc de pages (128 pages par défaut). Idéal pour les tables très grandes où les données sont naturellement corrélées avec l'ordre d'insertion (timestamps, IDs séquentiels, logs).

```sql
-- Créer un BRIN sur une colonne de timestamp (insertion chronologique)
CREATE INDEX idx_events_created_brin ON events USING BRIN (created_at);

-- Configurer la granularité (moins de pages par range = index plus précis mais plus grand)
CREATE INDEX idx_events_created_brin ON events USING BRIN (created_at)
  WITH (pages_per_range = 32);

-- Vérifier la taille comparée à un B-tree
SELECT
  indexname,
  pg_size_pretty(pg_relation_size(indexname::regclass)) AS index_size
FROM pg_indexes
WHERE tablename = 'events';
-- BRIN : ~48 KB vs B-tree : ~450 MB pour 100M lignes
```

### Index covering avec INCLUDE

Permet des Index Only Scans sans dupliquer les colonnes dans la clé d'index.

```sql
-- Requête cible :
-- SELECT user_id, status, total_amount FROM orders WHERE user_id = $1 ORDER BY created_at DESC

-- Index sans INCLUDE → Index Scan + heap access pour total_amount
CREATE INDEX idx_orders_user_created ON orders (user_id, created_at DESC);

-- Index avec INCLUDE → Index Only Scan possible (tout dans l'index)
CREATE INDEX idx_orders_user_created_covering ON orders (user_id, created_at DESC)
  INCLUDE (status, total_amount);
```

### Index partiels avec expression

```sql
-- Uniquement les commandes en attente (petite fraction de la table)
CREATE INDEX idx_orders_pending_user ON orders (user_id, created_at)
  WHERE status = 'EN_ATTENTE';

-- Index sur une expression (insensible à la casse)
CREATE INDEX idx_users_email_lower ON users (LOWER(email));
-- Pour utiliser cet index : WHERE LOWER(email) = LOWER($1)

-- Index partiel unique (emails vérifiés uniquement)
CREATE UNIQUE INDEX idx_users_email_verified ON users (email)
  WHERE email_verified = true;
```

---

## Paramètres du planificateur pour SSD

Sur SSD, le coût des accès aléatoires est beaucoup plus proche du séquentiel que sur HDD. Adapter la configuration :

```sql
-- Pour un serveur avec SSD et 32 GB de RAM
ALTER SYSTEM SET random_page_cost = 1.1;      -- Défaut: 4.0 (pour HDD). SSD ≈ 1.1
ALTER SYSTEM SET effective_cache_size = '24GB'; -- RAM disponible pour le cache OS + shared_buffers
ALTER SYSTEM SET shared_buffers = '8GB';        -- ~25% de la RAM totale
ALTER SYSTEM SET effective_io_concurrency = 200; -- Défaut: 1 pour HDD. SSD ≈ 200

-- Reload sans redémarrage
SELECT pg_reload_conf();
```

### Désactiver temporairement des stratégies (pour diagnostiquer)

```sql
-- Forcer un Seq Scan pour comparer avec un Index Scan
SET enable_indexscan = off;
EXPLAIN ANALYZE SELECT ... ;
RESET enable_indexscan;

-- Forcer un Hash Join à la place d'un Nested Loop
SET enable_nestloop = off;
EXPLAIN ANALYZE SELECT ... ;
RESET enable_nestloop;
```

---

## Parallel query

```sql
-- Vérifier la configuration actuelle
SHOW max_parallel_workers;                  -- Défaut: 8
SHOW max_parallel_workers_per_gather;       -- Défaut: 2
SHOW min_parallel_table_scan_size;          -- Défaut: 8MB

-- Forcer le parallélisme sur une requête spécifique (session)
SET max_parallel_workers_per_gather = 4;

-- Désactiver le parallélisme si nécessaire (requêtes OLTP courtes)
SET max_parallel_workers_per_gather = 0;

-- Indiquer qu'une table est grande (pour encourager le parallélisme)
ALTER TABLE large_events SET (parallel_workers = 4);
```

Le parallélisme bénéficie aux Seq Scans, Hash Joins et agrégations sur de grandes tables. Il est contre-productif pour les requêtes OLTP courtes.

---

## Connection overhead et pooling

Chaque connexion PostgreSQL est un processus OS (fork). Le coût de 1 000 connexions ouvertes est réel même si elles sont idle :

```sql
-- État des connexions
SELECT
  state,
  COUNT(*) AS nb,
  ROUND(AVG(EXTRACT(EPOCH FROM (clock_timestamp() - state_change))), 1) AS avg_age_sec
FROM pg_stat_activity
WHERE pid != pg_backend_pid()
GROUP BY state
ORDER BY nb DESC;

-- Connexions idle depuis plus de 5 minutes (candidats à être tuées)
SELECT pid, usename, application_name, state_change
FROM pg_stat_activity
WHERE state = 'idle'
  AND state_change < clock_timestamp() - INTERVAL '5 minutes';

-- Terminer les connexions idle trop vieilles
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
  AND state_change < clock_timestamp() - INTERVAL '30 minutes'
  AND pid != pg_backend_pid();
```

Recommandation : `max_connections = 100` côté PostgreSQL + PgBouncer en mode transaction pooling devant. Les applications voient 1 000 connexions, PostgreSQL n'en maintient que 20-50 actives réellement.

---

## Write performance

```sql
-- Tuner les buffers WAL (pour les charges write-intensive)
ALTER SYSTEM SET wal_buffers = '64MB';      -- Défaut: -1 (auto ~1/32 de shared_buffers)
ALTER SYSTEM SET checkpoint_completion_target = 0.9; -- Étaler le checkpoint sur 90% de l'intervalle

-- synchronous_commit = off : risque de perdre les dernières ~100ms d'écritures en cas de crash
-- Acceptable pour les logs, analytics, données non-critiques
SET synchronous_commit = off;

-- Bulk inserts avec COPY (bien plus rapide que des INSERT individuels)
COPY measurements (sensor_id, value, recorded_at)
FROM '/tmp/measurements.csv'
WITH (FORMAT csv, HEADER true);
```

---

## Table bloat : VACUUM FULL vs pg_repack

Le MVCC de PostgreSQL ne supprime pas physiquement les anciennes versions de lignes — elles restent dans le heap jusqu'au VACUUM. Si le VACUUM prend du retard, la table "gonfle" (bloat).

```sql
-- Estimer le bloat par table (requête approximative)
SELECT
  tablename,
  pg_size_pretty(pg_total_relation_size(tablename::regclass)) AS total_size,
  n_dead_tup,
  ROUND(n_dead_tup::NUMERIC / NULLIF(n_live_tup + n_dead_tup, 0) * 100, 1) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;
```

### VACUUM FULL vs pg_repack

| | VACUUM FULL | pg_repack |
|---|---|---|
| Lock | AccessExclusiveLock (bloque tout) | Pas de lock prolongé |
| Durée | Long (rebuild complet) | Long mais online |
| Espace récupéré | Total | Total |
| Usage | Maintenance planifiée (avec downtime) | Production active |

```bash
# Installer pg_repack (extension)
# pg_repack recrée la table en arrière-plan et permute atomiquement

pg_repack --host=localhost --dbname=mydb --table=orders --no-superuser-check

# Options utiles
pg_repack --table=orders --jobs=2          # Parallélisme
pg_repack --table=orders --wait-timeout=60 # Timeout pour les locks
```
