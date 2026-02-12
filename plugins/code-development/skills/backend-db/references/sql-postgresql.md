# SQL & PostgreSQL Advanced Reference

> Reference detaillee pour le SQL avance et les fonctionnalites specifiques a PostgreSQL. Couvre les window functions, CTEs, requetes recursives, JSONB, extensions majeures, strategies d'indexation, optimisation de requetes et partitionnement.

---

## Common Table Expressions (CTEs)

### Standard CTEs

Utiliser les CTEs pour decomposer les requetes complexes en etapes lisibles. Chaque CTE agit comme une sous-requete nommee. Depuis PostgreSQL 12, les CTEs non-recursives sont automatiquement inlinees par l'optimiseur (pas de barriere d'optimisation).

```sql
-- Exemple : Calculer le chiffre d'affaires par client avec classement
WITH customer_revenue AS (
    SELECT
        c.id,
        c.name,
        SUM(o.total_amount) AS total_revenue,
        COUNT(o.id) AS order_count
    FROM customers c
    JOIN orders o ON o.customer_id = c.id
    WHERE o.created_at >= NOW() - INTERVAL '12 months'
    GROUP BY c.id, c.name
),
revenue_ranked AS (
    SELECT
        *,
        NTILE(10) OVER (ORDER BY total_revenue DESC) AS decile
    FROM customer_revenue
)
SELECT * FROM revenue_ranked WHERE decile = 1;
```

Forcer la materialisation d'un CTE si necessaire avec `AS MATERIALIZED` :

```sql
WITH MATERIALIZED heavy_computation AS (
    SELECT ... -- requete couteuse qui ne doit s'executer qu'une fois
)
SELECT * FROM heavy_computation WHERE ...
UNION ALL
SELECT * FROM heavy_computation WHERE ...;
```

### Recursive CTEs

Utiliser les CTEs recursives pour parcourir les structures arborescentes (categories, organigrammes, graphes). Toujours inclure une condition de terminaison pour eviter les boucles infinies.

```sql
-- Parcourir un arbre de categories avec la profondeur
WITH RECURSIVE category_tree AS (
    -- Cas de base : racines
    SELECT id, name, parent_id, 0 AS depth, ARRAY[id] AS path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    -- Cas recursif : enfants
    SELECT c.id, c.name, c.parent_id, ct.depth + 1, ct.path || c.id
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
    WHERE ct.depth < 10  -- garde-fou contre les boucles infinies
      AND NOT c.id = ANY(ct.path)  -- detection de cycle
)
SELECT * FROM category_tree ORDER BY path;
```

```sql
-- Parcourir un graphe de dependances avec detection de cycle
WITH RECURSIVE deps AS (
    SELECT target_id, source_id, ARRAY[source_id] AS path, FALSE AS has_cycle
    FROM dependencies
    WHERE source_id = 'module_a'

    UNION ALL

    SELECT d.target_id, d.source_id, deps.path || d.source_id,
           d.source_id = ANY(deps.path) AS has_cycle
    FROM dependencies d
    JOIN deps ON d.source_id = deps.target_id
    WHERE NOT deps.has_cycle
)
SELECT * FROM deps;
```

## Window Functions

Les window functions calculent des valeurs sur un ensemble de lignes liees a la ligne courante, sans reduire le nombre de lignes retournees (contrairement a GROUP BY).

### Fonctions de classement

```sql
-- ROW_NUMBER, RANK, DENSE_RANK : differences
SELECT
    product_id,
    category,
    revenue,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS row_num,
    RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rank,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS dense_rank
FROM product_sales;
-- ROW_NUMBER : toujours unique (1,2,3,4,5)
-- RANK : saute les rangs apres ex-aequo (1,2,2,4,5)
-- DENSE_RANK : ne saute pas (1,2,2,3,4)
```

### Fonctions d'agregation en fenetre

```sql
-- Moyenne glissante sur 7 jours et cumul
SELECT
    date,
    daily_revenue,
    AVG(daily_revenue) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS avg_7_days,
    SUM(daily_revenue) OVER (
        ORDER BY date
        ROWS UNBOUNDED PRECEDING
    ) AS cumulative_revenue
FROM daily_stats;
```

### LAG / LEAD pour comparaisons temporelles

```sql
-- Comparer avec la periode precedente
SELECT
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY month) AS prev_month,
    ROUND(
        (revenue - LAG(revenue, 1) OVER (ORDER BY month))::numeric
        / NULLIF(LAG(revenue, 1) OVER (ORDER BY month), 0) * 100, 2
    ) AS growth_pct
FROM monthly_revenue;
```

### FIRST_VALUE / LAST_VALUE / NTH_VALUE

```sql
-- Premier et dernier achat par client
SELECT DISTINCT
    customer_id,
    FIRST_VALUE(product_name) OVER w AS first_purchase,
    LAST_VALUE(product_name) OVER w AS latest_purchase
FROM orders
WINDOW w AS (
    PARTITION BY customer_id
    ORDER BY created_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
);
```

### Named Windows

Definir des fenetres nommees avec `WINDOW` pour eviter la repetition :

```sql
SELECT
    employee_id,
    department,
    salary,
    AVG(salary) OVER dept_window AS dept_avg,
    MAX(salary) OVER dept_window AS dept_max,
    salary - AVG(salary) OVER dept_window AS diff_from_avg
FROM employees
WINDOW dept_window AS (PARTITION BY department);
```

## LATERAL Joins

Utiliser `LATERAL` pour referencer les colonnes des tables precedentes dans une sous-requete jointe. Equivalent a une "boucle for each" en SQL.

```sql
-- Top 3 commandes par client (pattern frequent)
SELECT c.id, c.name, top_orders.*
FROM customers c
CROSS JOIN LATERAL (
    SELECT o.id AS order_id, o.total_amount, o.created_at
    FROM orders o
    WHERE o.customer_id = c.id
    ORDER BY o.total_amount DESC
    LIMIT 3
) AS top_orders;
```

```sql
-- Derniere activite par utilisateur avec LATERAL
SELECT u.id, u.email, latest.*
FROM users u
LEFT JOIN LATERAL (
    SELECT a.action, a.created_at
    FROM activities a
    WHERE a.user_id = u.id
    ORDER BY a.created_at DESC
    LIMIT 1
) AS latest ON TRUE;
```

## PostgreSQL JSONB

### Operations de base

```sql
-- Creer et interroger du JSONB
CREATE TABLE events (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type TEXT NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Acceder aux valeurs (-> retourne JSON, ->> retourne TEXT)
SELECT
    payload->>'user_id' AS user_id,
    payload->'metadata'->>'source' AS source,
    (payload->>'amount')::numeric AS amount
FROM events
WHERE type = 'purchase';

-- Filtrer avec @> (containment)
SELECT * FROM events
WHERE payload @> '{"status": "completed", "priority": "high"}';

-- Verifier l'existence de cles avec ? et ?|
SELECT * FROM events
WHERE payload ? 'error_code';           -- cle existe
SELECT * FROM events
WHERE payload ?| ARRAY['warning', 'error'];  -- au moins une cle existe
```

### Fonctions JSONB avancees

```sql
-- jsonb_build_object pour construire du JSON proprement
SELECT jsonb_build_object(
    'user', jsonb_build_object('id', u.id, 'name', u.name),
    'orders', jsonb_agg(jsonb_build_object('id', o.id, 'total', o.total_amount))
) AS result
FROM users u
JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name;

-- jsonb_path_query pour SQL/JSON path (PostgreSQL 12+)
SELECT jsonb_path_query(payload, '$.items[*] ? (@.price > 100)') AS expensive_items
FROM orders;

-- Modifier du JSONB avec jsonb_set
UPDATE events
SET payload = jsonb_set(payload, '{status}', '"processed"')
WHERE id = 42;

-- Supprimer une cle avec - operateur
UPDATE events
SET payload = payload - 'temporary_field'
WHERE payload ? 'temporary_field';
```

### Indexation JSONB

```sql
-- Index GIN sur tout le document (supporte @>, ?, ?|, ?&)
CREATE INDEX idx_events_payload ON events USING GIN (payload);

-- Index GIN avec jsonb_path_ops (plus compact, supporte uniquement @>)
CREATE INDEX idx_events_payload_path ON events USING GIN (payload jsonb_path_ops);

-- Index B-tree sur une expression pour un chemin specifique
CREATE INDEX idx_events_user_id ON events ((payload->>'user_id'));

-- Index sur valeur imbriquee avec cast
CREATE INDEX idx_events_amount ON events (((payload->>'amount')::numeric));
```

## PostgreSQL Full-Text Search

```sql
-- Configurer la recherche full-text
ALTER TABLE articles ADD COLUMN search_vector tsvector
    GENERATED ALWAYS AS (
        setweight(to_tsvector('french', coalesce(title, '')), 'A') ||
        setweight(to_tsvector('french', coalesce(body, '')), 'B')
    ) STORED;

CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);

-- Rechercher avec classement par pertinence
SELECT
    id, title,
    ts_rank(search_vector, query) AS rank
FROM articles,
     to_tsquery('french', 'machine & learning | intelligence & artificielle') AS query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;
```

## Extensions PostgreSQL Essentielles

### pgvector : Recherche vectorielle pour l'IA

```sql
-- Installer et configurer pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Table avec colonne vectorielle (1536 dimensions pour OpenAI ada-002, 3072 pour text-embedding-3-large)
CREATE TABLE documents (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL,
    metadata JSONB DEFAULT '{}'
);

-- Index HNSW (recommande pour la plupart des cas, meilleur recall)
CREATE INDEX idx_documents_embedding ON documents
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 200);

-- Index IVFFlat (plus rapide a construire, bon pour les grands datasets)
CREATE INDEX idx_documents_embedding_ivf ON documents
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Recherche par similarite cosinus (top 10 plus proches)
SELECT id, content, 1 - (embedding <=> $1::vector) AS similarity
FROM documents
WHERE metadata @> '{"type": "article"}'
ORDER BY embedding <=> $1::vector
LIMIT 10;

-- Recherche hybride : vectorielle + full-text
WITH semantic AS (
    SELECT id, 1 - (embedding <=> $1::vector) AS score
    FROM documents
    ORDER BY embedding <=> $1::vector
    LIMIT 50
),
fulltext AS (
    SELECT id, ts_rank(search_vector, to_tsquery($2)) AS score
    FROM documents
    WHERE search_vector @@ to_tsquery($2)
    LIMIT 50
)
SELECT
    COALESCE(s.id, f.id) AS id,
    COALESCE(s.score, 0) * 0.7 + COALESCE(f.score, 0) * 0.3 AS combined_score
FROM semantic s
FULL OUTER JOIN fulltext f ON s.id = f.id
ORDER BY combined_score DESC
LIMIT 10;
```

### PostGIS : Donnees geospatiales

```sql
CREATE EXTENSION IF NOT EXISTS postgis;

-- Table avec geometrie
CREATE TABLE places (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    location GEOGRAPHY(Point, 4326) NOT NULL
);

CREATE INDEX idx_places_location ON places USING GIST (location);

-- Trouver les lieux dans un rayon de 5 km
SELECT name, ST_Distance(location, ST_MakePoint(2.3522, 48.8566)::geography) AS distance_m
FROM places
WHERE ST_DWithin(location, ST_MakePoint(2.3522, 48.8566)::geography, 5000)
ORDER BY distance_m;
```

### pg_cron : Planification de taches

```sql
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Rafraichir une vue materialisee toutes les heures
SELECT cron.schedule('refresh-dashboard', '0 * * * *',
    'REFRESH MATERIALIZED VIEW CONCURRENTLY mv_dashboard_stats');

-- Purger les anciennes sessions chaque nuit
SELECT cron.schedule('cleanup-sessions', '0 3 * * *',
    'DELETE FROM sessions WHERE expires_at < NOW()');

-- Vacuum les tables volumineuses le dimanche
SELECT cron.schedule('weekly-vacuum', '0 4 * * 0',
    'VACUUM ANALYZE orders');
```

## Indexing Strategies

### Types d'index et leurs cas d'usage

| Type | Operateurs supportes | Cas d'usage |
|------|---------------------|-------------|
| **B-tree** (defaut) | `=, <, >, <=, >=, BETWEEN, IN, IS NULL` | Egalite, range, tri, la majorite des cas |
| **GIN** | `@>, ?, ?&, ?|, @@` | JSONB, arrays, full-text search, trigram |
| **GiST** | `<<, >>, @>, <@, &&, ~=` | Geospatial, range types, full-text, nearest-neighbor |
| **BRIN** | `=, <, >, <=, >=` | Tres grandes tables avec donnees naturellement ordonnees (timestamps, IDs sequentiels) |
| **Hash** | `=` | Egalite stricte uniquement (rarement superieur a B-tree) |

### Index partiels

Creer des index uniquement sur un sous-ensemble de lignes pour reduire la taille et ameliorer les performances :

```sql
-- Indexer uniquement les commandes actives (90% des requetes)
CREATE INDEX idx_orders_active ON orders (customer_id, created_at)
    WHERE status NOT IN ('cancelled', 'archived');

-- Index partiel sur les lignes non-null
CREATE INDEX idx_users_phone ON users (phone)
    WHERE phone IS NOT NULL;

-- Index unique conditionnel (soft delete)
CREATE UNIQUE INDEX idx_users_email_active ON users (email)
    WHERE deleted_at IS NULL;
```

### Index couvrants (Covering Indexes)

Ajouter des colonnes a un index avec `INCLUDE` pour permettre des index-only scans :

```sql
-- L'index couvre entierement la requete, pas besoin d'acceder a la table
CREATE INDEX idx_orders_covering ON orders (customer_id, created_at DESC)
    INCLUDE (total_amount, status);

-- Cette requete utilise uniquement l'index (Index Only Scan)
SELECT total_amount, status
FROM orders
WHERE customer_id = 42
ORDER BY created_at DESC
LIMIT 10;
```

### Index multicolonnes : ordre des colonnes

Respecter la regle : placer les colonnes d'egalite en premier, puis les colonnes de range/tri.

```sql
-- BON : egalite (status) puis range (created_at)
CREATE INDEX idx_orders_status_date ON orders (status, created_at DESC);

-- Utilise par : WHERE status = 'active' ORDER BY created_at DESC
-- Utilise par : WHERE status = 'active' AND created_at > '2024-01-01'
-- N'utilise PAS efficacement : WHERE created_at > '2024-01-01' (sans status)
```

## Query Optimization

### EXPLAIN ANALYZE : lire un query plan

```sql
-- Toujours utiliser ANALYZE + BUFFERS pour les informations reelles
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.*, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'pending'
  AND o.created_at > NOW() - INTERVAL '7 days'
ORDER BY o.created_at DESC
LIMIT 20;
```

Elements cles a surveiller dans le plan :
- **Seq Scan** sur une grande table : index manquant probable
- **Nested Loop** avec un grand nombre de boucles : possiblement un N+1
- **Sort** avec `external merge` : `work_mem` insuffisant, tri sur disque
- **Buffers shared read** eleve : donnees pas en cache, I/O disque
- **Rows estimated vs actual** tres differents : statistiques obsoletes, lancer `ANALYZE table_name`

### pg_stat_statements : identifier les requetes lentes

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 requetes par temps total
SELECT
    calls,
    ROUND(total_exec_time::numeric, 2) AS total_ms,
    ROUND(mean_exec_time::numeric, 2) AS mean_ms,
    ROUND((100 * total_exec_time / SUM(total_exec_time) OVER ())::numeric, 2) AS pct,
    LEFT(query, 100) AS query_preview
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Requetes avec le pire ratio rows estimes/reels
SELECT
    calls,
    rows,
    ROUND(mean_exec_time::numeric, 2) AS mean_ms,
    LEFT(query, 100) AS query_preview
FROM pg_stat_statements
WHERE calls > 100
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Parametres de performance critiques

```sql
-- work_mem : memoire par operation de tri/hash (defaut 4MB, augmenter pour les requetes analytiques)
SET work_mem = '256MB';  -- pour une session analytique

-- effective_cache_size : indication a l'optimiseur de la memoire disponible
-- Generalement 75% de la RAM totale
ALTER SYSTEM SET effective_cache_size = '12GB';

-- random_page_cost : reduire pour les SSD (defaut 4.0)
ALTER SYSTEM SET random_page_cost = 1.1;

-- Verifier le cache hit ratio (doit etre > 99%)
SELECT
    ROUND(100.0 * SUM(heap_blks_hit) / NULLIF(SUM(heap_blks_hit) + SUM(heap_blks_read), 0), 2) AS cache_hit_ratio
FROM pg_statio_user_tables;
```

## Table Partitioning

### Partitionnement par range (cas le plus courant)

```sql
-- Creer la table partitionnee
CREATE TABLE events (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    event_type TEXT NOT NULL,
    payload JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Creer les partitions
CREATE TABLE events_2024_q1 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
CREATE TABLE events_2024_q2 PARTITION OF events
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');
CREATE TABLE events_2024_q3 PARTITION OF events
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');
CREATE TABLE events_2024_q4 PARTITION OF events
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');

-- Partition par defaut pour les donnees hors range
CREATE TABLE events_default PARTITION OF events DEFAULT;

-- Les index doivent etre crees sur la table parent (propages aux partitions)
CREATE INDEX idx_events_type_created ON events (event_type, created_at DESC);
```

### Partitionnement par liste

```sql
CREATE TABLE orders (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    region TEXT NOT NULL,
    total_amount NUMERIC(12,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY LIST (region);

CREATE TABLE orders_eu PARTITION OF orders FOR VALUES IN ('FR', 'DE', 'ES', 'IT', 'NL');
CREATE TABLE orders_us PARTITION OF orders FOR VALUES IN ('US', 'CA');
CREATE TABLE orders_apac PARTITION OF orders FOR VALUES IN ('JP', 'KR', 'AU', 'SG');
CREATE TABLE orders_other PARTITION OF orders DEFAULT;
```

### Automatiser la creation de partitions

Utiliser `pg_partman` pour automatiser la creation et la maintenance des partitions :

```sql
CREATE EXTENSION IF NOT EXISTS pg_partman;

SELECT partman.create_parent(
    p_parent_table := 'public.events',
    p_control := 'created_at',
    p_type := 'range',
    p_interval := '1 month',
    p_premake := 3  -- creer 3 partitions a l'avance
);

-- Maintenance automatique via pg_cron
SELECT cron.schedule('partition-maintenance', '0 1 * * *',
    'SELECT partman.run_maintenance()');
```

## PostgreSQL 16/17 Notable Features

### PostgreSQL 16
- `any_value()` : fonction d'agregation qui retourne une valeur arbitraire du groupe (remplace le pattern `MIN()` sur une colonne non-groupee)
- Parallelisme ameliore pour `FULL OUTER JOIN` et `RIGHT OUTER JOIN`
- Support de l'authentification RADIUS sur les connexions TLS

### PostgreSQL 17
- Amelioration du `MERGE` avec `RETURNING` clause
- `COPY` ameliore avec support de colonnes generees
- Incremental sort ameliore pour de meilleures performances sur les tris partiels
- Ameliorations du vacuum : plus rapide et moins bloquant
- Meilleur support du JSON avec `JSON_TABLE` (SQL standard)

## Performance Checklist

Appliquer cette checklist avant toute mise en production :

1. Verifier que toutes les cles etrangeres sont indexees
2. Valider le cache hit ratio > 99% avec `pg_statio_user_tables`
3. Auditer les requetes lentes via `pg_stat_statements` (top 10 par temps total)
4. Verifier l'absence de Seq Scan sur les grandes tables dans les requetes frequentes
5. Configurer `random_page_cost = 1.1` pour les disques SSD
6. Ajuster `work_mem` pour les requetes analytiques (session-level, pas global)
7. S'assurer que `effective_cache_size` reflete ~75% de la RAM
8. Mettre en place VACUUM automatique avec des seuils adaptes
9. Activer `log_min_duration_statement` pour logger les requetes lentes
10. Valider que les statistiques sont a jour (`ANALYZE` recent sur les tables critiques)
