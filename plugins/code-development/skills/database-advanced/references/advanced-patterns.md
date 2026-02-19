# Patterns Avancés — Partitioning, TimescaleDB et Neo4j

## Partitioning PostgreSQL avancé

Le partitioning divise une grande table en sous-tables (partitions) tout en maintenant une interface unifiée. Les requêtes filtrant sur la clé de partition ne lisent que les partitions concernées (partition pruning).

### Range partitioning (par date)

```sql
-- Table de base partitionnée par mois
CREATE TABLE orders (
  id          BIGSERIAL,
  user_id     BIGINT       NOT NULL,
  total       NUMERIC(12,2) NOT NULL,
  created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  PRIMARY KEY (id, created_at)  -- La clé de partition doit faire partie de la PK
) PARTITION BY RANGE (created_at);

-- Créer les partitions manuellement
CREATE TABLE orders_2024_01 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Partition "default" pour les valeurs hors range (évite les erreurs d'insertion)
CREATE TABLE orders_default PARTITION OF orders DEFAULT;
```

### Hash partitioning (distribution uniforme)

Idéal pour répartir uniformément une table sans critère temporel naturel :

```sql
CREATE TABLE user_sessions (
  id         UUID          NOT NULL DEFAULT gen_random_uuid(),
  user_id    BIGINT        NOT NULL,
  data       JSONB,
  expires_at TIMESTAMPTZ   NOT NULL,
  PRIMARY KEY (id, user_id)
) PARTITION BY HASH (user_id);

-- 8 partitions de taille égale
CREATE TABLE user_sessions_p0 PARTITION OF user_sessions
  FOR VALUES WITH (MODULUS 8, REMAINDER 0);
CREATE TABLE user_sessions_p1 PARTITION OF user_sessions
  FOR VALUES WITH (MODULUS 8, REMAINDER 1);
-- ... p2 à p7
```

### List partitioning (valeurs discrètes)

```sql
CREATE TABLE products (
  id     BIGSERIAL,
  name   TEXT    NOT NULL,
  region VARCHAR(20) NOT NULL,
  status VARCHAR(20) NOT NULL
) PARTITION BY LIST (region);

CREATE TABLE products_europe  PARTITION OF products FOR VALUES IN ('FR', 'DE', 'ES', 'IT');
CREATE TABLE products_america PARTITION OF products FOR VALUES IN ('US', 'CA', 'BR', 'MX');
CREATE TABLE products_asia    PARTITION OF products FOR VALUES IN ('JP', 'CN', 'IN', 'SG');
CREATE TABLE products_other   PARTITION OF products DEFAULT;
```

### Sous-partitioning (range + hash)

```sql
-- Partitionné par année, sous-partitionné par hash sur l'ID (distribution uniforme dans chaque année)
CREATE TABLE events (
  id         BIGSERIAL,
  type       VARCHAR(50) NOT NULL,
  payload    JSONB,
  created_at TIMESTAMPTZ NOT NULL,
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2024 PARTITION OF events
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01')
  PARTITION BY HASH (id);

CREATE TABLE events_2024_p0 PARTITION OF events_2024 FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE events_2024_p1 PARTITION OF events_2024 FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE events_2024_p2 PARTITION OF events_2024 FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE events_2024_p3 PARTITION OF events_2024 FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

### Vérifier le partition pruning

```sql
-- EXPLAIN doit montrer "Partitions selected" et pruner les partitions non concernées
EXPLAIN (ANALYZE, PARTITIONS)
SELECT * FROM orders
WHERE created_at BETWEEN '2024-01-01' AND '2024-01-31';
-- → "Partitions selected: orders_2024_01 (1 out of 24)"

-- Activer/désactiver le pruning (pour diagnostiquer)
SET enable_partition_pruning = on;  -- Défaut: on
```

### Maintenance des partitions avec pg_partman

```sql
-- pg_partman automatise la création et la suppression des partitions
CREATE EXTENSION pg_partman;

-- Configurer la gestion automatique
SELECT partman.create_parent(
  p_parent_table   => 'public.orders',
  p_control        => 'created_at',
  p_interval       => '1 month',
  p_premake        => 3  -- Créer 3 partitions en avance
);

-- Archiver et supprimer les vieilles partitions (garder 24 mois)
SELECT partman.run_maintenance(p_parent_table => 'public.orders');

-- Détacher une partition pour l'archiver (sans la supprimer)
ALTER TABLE orders DETACH PARTITION orders_2022_01;
-- La partition devient une table indépendante → backup → DROP
```

---

## Sharding avec Citus

Citus est une extension PostgreSQL qui transforme une instance en cluster distribué. Les données sont réparties sur plusieurs nœuds workers.

```sql
-- Sur le nœud coordinateur
CREATE EXTENSION citus;

-- Ajouter des nœuds workers
SELECT citus_add_node('worker-1', 5432);
SELECT citus_add_node('worker-2', 5432);

-- Distribuer une table (shardée sur user_id, 32 shards)
SELECT create_distributed_table('orders', 'user_id', shard_count => 32);

-- Table de référence (répliquée sur tous les workers)
SELECT create_reference_table('countries');
SELECT create_reference_table('product_categories');

-- Les requêtes incluant la shard key sont routées vers le bon worker
SELECT * FROM orders WHERE user_id = 12345;  -- Routage direct

-- Les requêtes sans shard key sont broadcastées (à éviter)
SELECT COUNT(*) FROM orders;  -- Query sur tous les workers
```

---

## TimescaleDB

TimescaleDB est une extension PostgreSQL optimisée pour les données time-series. Elle divise automatiquement les hypertables en chunks par intervalle de temps.

### Hypertables

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Créer la table normale
CREATE TABLE measurements (
  time        TIMESTAMPTZ      NOT NULL,
  sensor_id   INT              NOT NULL,
  temperature DOUBLE PRECISION,
  humidity    DOUBLE PRECISION,
  value       DOUBLE PRECISION NOT NULL
);

-- Convertir en hypertable (chunks de 1 jour par défaut)
SELECT create_hypertable('measurements', 'time', chunk_time_interval => INTERVAL '1 day');

-- Vérifier les chunks créés
SELECT chunk_schema, chunk_name, range_start, range_end
FROM timescaledb_information.chunks
WHERE hypertable_name = 'measurements'
ORDER BY range_start DESC
LIMIT 10;
```

### Compression automatique

```sql
-- Activer la compression après 7 jours
ALTER TABLE measurements SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'sensor_id',  -- Grouper par capteur dans le chunk compressé
  timescaledb.compress_orderby   = 'time DESC'
);

SELECT add_compression_policy('measurements', INTERVAL '7 days');

-- Vérifier le taux de compression
SELECT
  chunk_name,
  before_compression_total_bytes / 1024 / 1024 AS size_mb_before,
  after_compression_total_bytes / 1024 / 1024  AS size_mb_after,
  ROUND((1 - after_compression_total_bytes::NUMERIC / before_compression_total_bytes) * 100, 1) AS compression_pct
FROM chunk_compression_stats('measurements')
ORDER BY chunk_name DESC;
```

### Continuous Aggregates

Les continuous aggregates sont des vues matérialisées rafraîchies automatiquement, beaucoup plus rapides pour les agrégations sur de grandes plages de temps.

```sql
-- Agrégat par heure
CREATE MATERIALIZED VIEW measurements_hourly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time) AS bucket,
  sensor_id,
  AVG(temperature)  AS avg_temperature,
  MAX(temperature)  AS max_temperature,
  MIN(temperature)  AS min_temperature,
  AVG(humidity)     AS avg_humidity,
  COUNT(*)          AS nb_measurements
FROM measurements
GROUP BY bucket, sensor_id
WITH NO DATA;

-- Politique de rafraîchissement automatique (toutes les heures, lag de 1h)
SELECT add_continuous_aggregate_policy('measurements_hourly',
  start_offset => INTERVAL '3 hours',
  end_offset   => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour'
);

-- Rafraîchissement manuel (pour les données historiques)
CALL refresh_continuous_aggregate('measurements_hourly',
  '2024-01-01'::TIMESTAMPTZ,
  '2024-02-01'::TIMESTAMPTZ
);
```

### Retention policy

```sql
-- Supprimer les données brutes après 2 ans
SELECT add_retention_policy('measurements', INTERVAL '2 years');

-- Conserver les agrégats horaires 5 ans, journaliers indéfiniment
SELECT add_retention_policy('measurements_hourly', INTERVAL '5 years');
```

### Requêtes time-series

```sql
-- time_bucket : regrouper par intervalle arbitraire
SELECT
  time_bucket('15 minutes', time) AS bucket,
  sensor_id,
  AVG(value)    AS avg_value,
  first(value, time) AS first_value,  -- Première valeur dans le bucket
  last(value, time)  AS last_value    -- Dernière valeur dans le bucket
FROM measurements
WHERE time > NOW() - INTERVAL '24 hours'
  AND sensor_id IN (1, 2, 3)
GROUP BY bucket, sensor_id
ORDER BY bucket DESC;

-- histogram : distribution des valeurs
SELECT
  sensor_id,
  histogram(temperature, 0, 50, 10) AS temp_distribution
FROM measurements
WHERE time > NOW() - INTERVAL '7 days'
GROUP BY sensor_id;
-- Retourne : {count_below, count_1, count_2, ..., count_above} par bucket
```

---

## Neo4j et Cypher : bases de données graphes

### Quand choisir une DB graphe ?

| Cas d'usage | PostgreSQL suffit ? | Neo4j recommandé ? |
|---|---|---|
| Relations à 1-2 niveaux de profondeur | Oui (JOINs) | Non nécessaire |
| Réseau social (amis d'amis d'amis) | Difficile (JOINs récursifs) | Oui |
| Recommandations collaboratives | Difficile | Oui |
| Détection de fraude (cycles, patterns) | Très difficile | Oui |
| Hiérarchies peu profondes (catégories) | Oui (LTREE) | Non nécessaire |
| Hiérarchies profondes (org charts, BOM) | Difficile | Oui |
| Shortest path, PageRank | Très difficile | Oui |

### Modélisation graphe

```cypher
// Créer des nœuds
CREATE (alice:Person {name: 'Alice', email: 'alice@example.com', age: 30})
CREATE (bob:Person {name: 'Bob', email: 'bob@example.com', age: 25})
CREATE (product:Product {id: 'P001', name: 'Laptop Pro', price: 1299.99})
CREATE (category:Category {name: 'Electronics'})

// Créer des relations
MATCH (alice:Person {email: 'alice@example.com'})
MATCH (bob:Person {email: 'bob@example.com'})
CREATE (alice)-[:KNOWS {since: date('2020-01-15')}]->(bob)

MATCH (alice:Person {email: 'alice@example.com'})
MATCH (product:Product {id: 'P001'})
CREATE (alice)-[:PURCHASED {date: date('2024-03-10'), quantity: 1}]->(product)

// MERGE : créer si n'existe pas, sinon retourner l'existant
MERGE (person:Person {email: 'charlie@example.com'})
ON CREATE SET person.name = 'Charlie', person.created_at = datetime()
ON MATCH SET person.last_seen = datetime()
```

### Requêtes Cypher fondamentales

```cypher
// Trouver les amis d'amis d'Alice (2 niveaux)
MATCH (alice:Person {name: 'Alice'})-[:KNOWS*2]->(fof:Person)
WHERE NOT (alice)-[:KNOWS]->(fof) AND fof <> alice
RETURN fof.name, fof.email

// Path variable length (1 à 5 niveaux)
MATCH path = (start:Person {name: 'Alice'})-[:KNOWS*1..5]->(end:Person {name: 'Eve'})
RETURN path, length(path) AS hops
ORDER BY hops ASC
LIMIT 1

// Recommandation : produits achetés par les personnes qui me ressemblent
MATCH (me:Person {email: 'alice@example.com'})-[:PURCHASED]->(p:Product)
      <-[:PURCHASED]-(similar:Person)-[:PURCHASED]->(rec:Product)
WHERE NOT (me)-[:PURCHASED]->(rec)
RETURN rec.name, COUNT(similar) AS score
ORDER BY score DESC
LIMIT 10

// Détection de fraude : cycles d'achats suspects
MATCH cycle = (account:Account)-[:TRANSFER*3..6]->(account)
WHERE ALL(r IN relationships(cycle) WHERE r.amount > 1000)
RETURN account.id, length(cycle) AS cycle_length
```

### Graph algorithms (GDS library)

```cypher
// Charger le graphe en mémoire
CALL gds.graph.project(
  'social-network',
  'Person',
  {KNOWS: {orientation: 'UNDIRECTED'}}
)

// PageRank : identifier les personnes les plus influentes
CALL gds.pageRank.stream('social-network')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS person, score
ORDER BY score DESC LIMIT 10

// Shortest path (Dijkstra avec poids)
MATCH (source:Person {name: 'Alice'}), (target:Person {name: 'Eve'})
CALL gds.shortestPath.dijkstra.stream('social-network', {
  sourceNode: source,
  targetNode: target,
  relationshipWeightProperty: 'strength'
})
YIELD path
RETURN [node IN nodes(path) | node.name] AS path_names

// Community detection (Louvain)
CALL gds.louvain.stream('social-network')
YIELD nodeId, communityId
RETURN communityId, COLLECT(gds.util.asNode(nodeId).name) AS members
ORDER BY SIZE(members) DESC LIMIT 5
```

### Index Neo4j

```cypher
// Index sur une propriété de nœud
CREATE INDEX person_email FOR (p:Person) ON (p.email)

// Index composite
CREATE INDEX order_date_status FOR (o:Order) ON (o.date, o.status)

// Index full-text (pour CONTAINS, STARTS WITH)
CREATE FULLTEXT INDEX product_search FOR (p:Product) ON EACH [p.name, p.description]

// Utiliser le full-text index
CALL db.index.fulltext.queryNodes('product_search', 'laptop pro')
YIELD node, score
RETURN node.name, score
```

---

## Full-text search : PostgreSQL vs Elasticsearch

### Full-text search natif PostgreSQL

```sql
-- tsvector + tsquery : suffisant pour 80% des cas
ALTER TABLE articles ADD COLUMN search_vector TSVECTOR
  GENERATED ALWAYS AS (
    setweight(to_tsvector('french', COALESCE(title, '')), 'A') ||
    setweight(to_tsvector('french', COALESCE(body, '')),  'B')
  ) STORED;

CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);

-- Requête full-text
SELECT title, ts_rank(search_vector, query) AS rank
FROM articles, to_tsquery('french', 'base & données & performance') query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;

-- pg_trgm : recherche par similarité (typos, partiel)
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_products_name_trgm ON products USING GIN (name gin_trgm_ops);

SELECT name, similarity(name, 'laptoo pro') AS sim
FROM products
WHERE name % 'laptoo pro'  -- Opérateur de similarité
ORDER BY sim DESC;
```

### Quand passer à Elasticsearch ?

| Critère | PostgreSQL FTS | Elasticsearch |
|---|---|---|
| Volume < 10M documents | Très bien | Overkill |
| Relevance scoring avancé | Basique (ts_rank) | Très sophistiqué (BM25) |
| Facettes/agrégations | Possible mais lent | Natif et rapide |
| Suggestions / autocomplete | Difficile | Natif |
| Synonymes, stemming personnalisé | Limité | Très configurable |
| Maintenance opérationnelle | Nulle (PostgreSQL déjà là) | Cluster à gérer |

---

## Multi-tenant avancé : comparaison des stratégies

### Schema-per-tenant

```sql
-- Créer un schéma par organisation
CREATE SCHEMA tenant_org_001;
CREATE TABLE tenant_org_001.orders ( ... );
-- Avantage : isolation totale, backup par tenant facile
-- Inconvénient : migration = N fois le même ALTER TABLE, cross-tenant queries impossibles
```

### Row-Level Security (RLS)

```sql
-- Toutes les données dans les mêmes tables, isolation par policy
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;  -- Même pour le propriétaire de la table

-- Policy : chaque transaction doit définir app.organisation_id
CREATE POLICY orders_tenant_isolation ON orders
  USING (organisation_id = current_setting('app.organisation_id')::BIGINT);

-- Policy différenciée lecture/écriture
CREATE POLICY orders_read  ON orders FOR SELECT
  USING (organisation_id = current_setting('app.organisation_id')::BIGINT);

CREATE POLICY orders_write ON orders FOR INSERT
  WITH CHECK (organisation_id = current_setting('app.organisation_id')::BIGINT);

-- Prisma middleware pour setter le context à chaque transaction
-- (voir cas d'étude case-studies.md)
```

### Separate databases

```typescript
// Connection pool par tenant (PgBouncer)
const tenantPools = new Map<string, Pool>();

function getPoolForTenant(tenantId: string): Pool {
  if (!tenantPools.has(tenantId)) {
    tenantPools.set(tenantId, new Pool({
      connectionString: `postgresql://user:pass@host/tenant_${tenantId}`
    }));
  }
  return tenantPools.get(tenantId)!;
}
// Avantage : isolation maximale, no RLS overhead
// Inconvénient : N bases à maintenir, migrations complexes, coût infrastructure élevé
```

### Tableau comparatif

| Critère | Schema-per-tenant | RLS (même tables) | Separate DBs |
|---|---|---|---|
| Isolation | Bonne | Bonne (si bien configuré) | Maximale |
| Migrations | Complexe (N schémas) | Simple (une seule table) | Très complexe |
| Cross-tenant queries | Difficile | Facile (superuser) | Impossible |
| Performance | Bonne | Très bonne (< 2ms overhead) | Excellente |
| Coût infra | Moyen | Faible | Élevé |
| Recommandé pour | < 1000 tenants, isolation forte | 1-100K tenants, SaaS standard | Réglementaire, haute isolation |
