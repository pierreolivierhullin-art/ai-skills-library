# Études de Cas — Database Advanced en Production

## Cas 1 — Migration zero-downtime : 10M lignes sur un site e-commerce 24/7

### Contexte

Table `products` contenant 10 millions de lignes sur un site e-commerce opérant 24h/24, 7j/7. L'objectif est de migrer la colonne `name TEXT` vers `name VARCHAR(500) NOT NULL` et d'ajouter une colonne `slug TEXT NOT NULL` dérivée du nom (utilisée pour les URLs SEO).

Contrainte absolue : aucune interruption de service. Le site génère 50 000 € de revenu par heure et une fenêtre de maintenance n'est pas envisageable.

### Problème

Une migration directe prendrait 35 à 45 minutes avec un verrou exclusif qui bloquerait toutes les requêtes :

```sql
-- Migration naïve (NE JAMAIS FAIRE en production sur une table de cette taille)
ALTER TABLE products
  ALTER COLUMN name TYPE VARCHAR(500),
  ALTER COLUMN name SET NOT NULL;

-- Résultat : AccessExclusiveLock pendant ~40 minutes
-- Toutes les requêtes SELECT et INSERT/UPDATE attendent → downtime complet
```

### Solution : Expand/Contract en 3 phases

**Phase 1 — Expand : ajouter les nouvelles structures sans casser l'existant**

```sql
-- Ajouter la colonne slug (nullable, pas de lock prolongé)
ALTER TABLE products ADD COLUMN IF NOT EXISTS slug TEXT;

-- Ajouter la colonne name_v2 pour la migration du type (nullable)
ALTER TABLE products ADD COLUMN IF NOT EXISTS name_v2 VARCHAR(500);

-- Durée : < 1 seconde (métadonnées uniquement)
-- Impact : zéro, le code existant ignore ces nouvelles colonnes
```

Déployer une version du code applicatif qui écrit dans les deux colonnes simultanément :

```typescript
// Version de transition : écriture dans les deux colonnes
async function createProduct(data: CreateProductInput) {
  const slug = generateSlug(data.name);
  return prisma.products.create({
    data: {
      name: data.name,          // Ancienne colonne (backward compat)
      name_v2: data.name,       // Nouvelle colonne
      slug: slug,               // Nouvelle colonne slug
      price: data.price,
    }
  });
}

function generateSlug(name: string): string {
  return name
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Supprimer les accents
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}
```

**Phase 2 — Backfill : remplir les lignes existantes**

```sql
-- Script de backfill par batches de 5000 lignes
DO $$
DECLARE
  batch_size     INT := 5000;
  rows_updated   INT;
  total_updated  INT := 0;
  start_time     TIMESTAMPTZ := clock_timestamp();
  estimated_total INT;
BEGIN
  SELECT COUNT(*) INTO estimated_total
  FROM products
  WHERE slug IS NULL OR name_v2 IS NULL;

  RAISE NOTICE 'Début du backfill : % produits à traiter', estimated_total;

  LOOP
    -- Backfill par batch avec une sous-requête pour éviter les locks longs
    WITH batch AS (
      SELECT id FROM products
      WHERE slug IS NULL OR name_v2 IS NULL
      ORDER BY id
      LIMIT batch_size
      FOR UPDATE SKIP LOCKED  -- Ignorer les lignes verrouillées par d'autres transactions
    )
    UPDATE products p
    SET
      slug    = lower(regexp_replace(
                  unaccent(p.name),
                  '[^a-z0-9]+', '-', 'g'
                )),
      name_v2 = p.name
    FROM batch
    WHERE p.id = batch.id;

    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;

    total_updated := total_updated + rows_updated;

    RAISE NOTICE 'Progression : %/% (%.1f%%) — durée : %',
      total_updated,
      estimated_total,
      (total_updated::FLOAT / NULLIF(estimated_total, 0) * 100),
      clock_timestamp() - start_time;

    -- Pause de 200ms pour ne pas saturer les I/O
    PERFORM pg_sleep(0.2);
  END LOOP;

  RAISE NOTICE 'Backfill terminé : % lignes traitées en %',
    total_updated, clock_timestamp() - start_time;
END $$;
```

Monitoring en temps réel depuis une autre session :

```sql
-- Surveiller la progression du backfill toutes les 30 secondes
SELECT
  COUNT(*)                                            AS total,
  COUNT(*) FILTER (WHERE slug IS NOT NULL)            AS slug_done,
  COUNT(*) FILTER (WHERE slug IS NULL)                AS slug_remaining,
  ROUND(
    COUNT(*) FILTER (WHERE slug IS NOT NULL)::NUMERIC
    / COUNT(*) * 100, 2
  )                                                   AS pct_complete
FROM products;
```

**Phase 3 — Contract : poser les contraintes et supprimer l'ancienne structure**

```sql
-- Vérifier qu'aucune ligne ne manque avant de poser les contraintes
SELECT COUNT(*) FROM products WHERE slug IS NULL;    -- Doit être 0
SELECT COUNT(*) FROM products WHERE name_v2 IS NULL; -- Doit être 0

-- Contrainte NOT VALID (instantanée, ne vérifie pas les lignes existantes)
ALTER TABLE products
  ADD CONSTRAINT chk_slug_not_null    CHECK (slug IS NOT NULL)    NOT VALID,
  ADD CONSTRAINT chk_name_v2_not_null CHECK (name_v2 IS NOT NULL) NOT VALID;

-- Validation (ShareUpdateExclusiveLock — compatible lectures/écritures)
ALTER TABLE products VALIDATE CONSTRAINT chk_slug_not_null;
ALTER TABLE products VALIDATE CONSTRAINT chk_name_v2_not_null;

-- Index unique sur slug (CONCURRENTLY = sans lock de table)
CREATE UNIQUE INDEX CONCURRENTLY idx_products_slug ON products (slug);

-- Transformer l'index en contrainte (utilise l'index existant, instantané)
ALTER TABLE products ADD CONSTRAINT uq_products_slug UNIQUE USING INDEX idx_products_slug;

-- Supprimer l'ancienne colonne name (après déploiement du code final sans compatibilité)
ALTER TABLE products DROP COLUMN IF EXISTS name;
ALTER TABLE products RENAME COLUMN name_v2 TO name;
```

### Plan de rollback

```sql
-- Rollback instantané : supprimer les nouvelles colonnes si problème en Phase 1
ALTER TABLE products DROP COLUMN IF EXISTS slug;
ALTER TABLE products DROP COLUMN IF EXISTS name_v2;

-- Rollback en Phase 3 : supprimer les contraintes
ALTER TABLE products DROP CONSTRAINT IF EXISTS chk_slug_not_null;
ALTER TABLE products DROP CONSTRAINT IF EXISTS chk_name_v2_not_null;
DROP INDEX CONCURRENTLY IF EXISTS idx_products_slug;
```

### Résultats mesurés

| Métrique | Avant | Après |
|---|---|---|
| Downtime | Migration impossible sans downtime | 0 seconde de downtime |
| Durée totale de la migration | — | 6 heures (backfill en arrière-plan) |
| Erreurs de contrainte | — | 0 |
| Impact sur la latence applicative | — | Négligeable (< 1ms) |

**Leçon clé** : toute migration DDL sur une table dépassant 100 000 lignes doit passer par le pattern Expand/Contract. Un `ALTER TABLE` direct en production, même pour un changement apparemment mineur, est un risque d'incident majeur.

---

## Cas 2 — Query lente résolue : -95% de latence dans une fintech

### Contexte

Application de gestion financière personnelle. La page principale affiche les transactions de l'utilisateur, filtrées par plage de dates et statut, triées par montant décroissant. Chaque utilisateur actif possède en moyenne 30 000 transactions, certains utilisateurs premium en ont jusqu'à 200 000.

### Problème

La page de reporting met 4 500ms à charger pour les utilisateurs avec beaucoup de transactions. Le monitoring Datadog montre 15% des requêtes dépassant 8 000ms (P99).

```sql
-- Requête applicative (générée par Prisma)
SELECT id, amount, description, category, status, transaction_date
FROM transactions
WHERE user_id = $1
  AND transaction_date BETWEEN $2 AND $3
  AND status = $4
ORDER BY amount DESC
LIMIT 50 OFFSET $5;
```

**EXPLAIN ANALYZE avant optimisation :**

```
Limit  (cost=12834.21..12834.34 rows=50 width=89) (actual time=4482.341..4482.356 rows=50 loops=1)
  ->  Sort  (cost=12834.21..12864.02 rows=11921 width=89) (actual time=4482.337..4482.340 rows=50 loops=1)
        Sort Key: amount DESC
        Sort Method: external merge  Disk: 2304kB
        ->  Seq Scan on transactions  (cost=0.00..12542.18 rows=11921 width=89) (actual time=0.041..4471.234 rows=48230 loops=1)
              Filter: ((user_id = 12345) AND (status = 'COMPLETED') AND (transaction_date >= '2024-01-01') AND (transaction_date <= '2024-03-31'))
              Rows Removed by Filter: 1951770
              Buffers: shared hit=234 read=12450
Planning Time: 0.821 ms
Execution Time: 4482.891 ms
```

Diagnostic : Seq Scan sur 2 000 000 de lignes, 12 450 pages lues depuis le disque, tri sur disque (external merge). Il n'existe qu'un index sur `user_id` mais le planificateur ne l'utilise pas car les statistiques sont obsolètes (dernier ANALYZE : 6 mois).

### Solution

**Étape 1 : Mettre à jour les statistiques**

```sql
ANALYZE transactions;
-- Les statistiques montrent maintenant que 85% des transactions sont COMPLETED
-- et que la corrélation de transaction_date est 0.98 (insertion chronologique)
```

**Étape 2 : Créer l'index composite partiel optimal**

```sql
-- Index composite sur les colonnes de la clause WHERE + ORDER BY,
-- partiel pour exclure les statuts rares (PENDING, FAILED représentent 3%)
CREATE INDEX CONCURRENTLY idx_transactions_user_date_amount
  ON transactions (user_id, transaction_date DESC, amount DESC)
  INCLUDE (description, category, status)  -- Index covering pour éviter l'accès heap
  WHERE status IN ('COMPLETED', 'CANCELLED');

-- Surveiller la création de l'index
SELECT phase, blocks_done, blocks_total,
  ROUND(blocks_done::NUMERIC / NULLIF(blocks_total, 0) * 100, 1) AS pct
FROM pg_stat_progress_create_index
WHERE relid = 'transactions'::regclass;
```

**Étape 3 : Réécrire la requête pour forcer l'utilisation de l'index**

```sql
-- Requête optimisée : ORDER BY doit correspondre à l'ordre de l'index
-- ou utiliser l'index covering pour éviter le tri sur disque
SELECT id, amount, description, category, status, transaction_date
FROM transactions
WHERE user_id = $1
  AND transaction_date BETWEEN $2 AND $3
  AND status = $4
ORDER BY transaction_date DESC, amount DESC  -- Correspond à l'ordre de l'index
LIMIT 50 OFFSET $5;
```

**EXPLAIN ANALYZE après optimisation :**

```
Limit  (cost=0.57..84.23 rows=50 width=89) (actual time=0.312..0.421 rows=50 loops=1)
  ->  Index Only Scan using idx_transactions_user_date_amount on transactions
        (cost=0.57..10234.12 rows=6102 width=89) (actual time=0.309..0.398 rows=50 loops=1)
        Index Cond: ((user_id = 12345) AND (transaction_date >= '2024-01-01') AND (transaction_date <= '2024-03-31'))
        Filter: (status = 'COMPLETED')
        Heap Fetches: 0
        Buffers: shared hit=12 read=0
Planning Time: 0.234 ms
Execution Time: 0.489 ms
```

Index Only Scan : 12 pages en cache, 0 lecture disque, 0 accès heap. Le tri disparaît car les données sont déjà ordonnées dans l'index.

**Vérification de l'utilisation de l'index en production :**

```sql
SELECT
  indexrelname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE relname = 'transactions'
ORDER BY idx_scan DESC;
```

### Résultats mesurés

| Métrique | Avant | Après | Amélioration |
|---|---|---|---|
| Latence P50 | 4 500ms | 45ms | -99% |
| Latence P99 | 8 000ms | 180ms | -97.75% |
| CPU PostgreSQL (cette query) | 65% | 3% | -95% |
| Pages disque lues | 12 450 | 0 | -100% |

**Leçon clé** : `EXPLAIN (ANALYZE, BUFFERS)` est la seule source de vérité pour les problèmes de performance. Ne jamais optimiser sans mesurer d'abord. Les statistiques obsolètes sont la première cause de plans sous-optimaux — intégrer `ANALYZE` dans le pipeline de déploiement.

---

## Cas 3 — Multi-tenant avec RLS : SaaS B2B, 500 organisations

### Contexte

SaaS de gestion RH utilisé par 500 organisations clientes. Toutes les données sont stockées dans les mêmes tables PostgreSQL, isolées uniquement par une colonne `organisation_id`. Le produit gère des données RH sensibles (salaires, évaluations, données personnelles).

### Problème

Un audit de code révèle un bug critique dans l'endpoint `GET /api/employees` : un développeur a oublié le filtre `WHERE organisation_id = :currentOrg` dans une requête complexe avec plusieurs JOINs. Un client a pu accéder aux données d'un autre client pendant 72 heures avant détection.

```typescript
// Bug : la requête oublie le filtre sur organisation_id
async function getEmployeesWithManager(departmentId: string) {
  // Requête avec JOIN complexe — filtre organisation_id oublié sur la sous-requête
  return prisma.$queryRaw`
    SELECT e.*, m.name as manager_name
    FROM employees e
    LEFT JOIN employees m ON e.manager_id = m.id
    WHERE e.department_id = ${departmentId}
    -- MANQUE : AND e.organisation_id = ${currentOrgId}
  `;
}
```

### Solution : Row-Level Security comme dernière ligne de défense

**Étape 1 : Activer RLS sur toutes les tables sensibles**

```sql
-- Activer RLS sur les 5 tables principales
ALTER TABLE employees         ENABLE ROW LEVEL SECURITY;
ALTER TABLE employees         FORCE ROW LEVEL SECURITY;

ALTER TABLE departments       ENABLE ROW LEVEL SECURITY;
ALTER TABLE departments       FORCE ROW LEVEL SECURITY;

ALTER TABLE payroll_records   ENABLE ROW LEVEL SECURITY;
ALTER TABLE payroll_records   FORCE ROW LEVEL SECURITY;

ALTER TABLE performance_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE performance_reviews FORCE ROW LEVEL SECURITY;

ALTER TABLE time_off_requests  ENABLE ROW LEVEL SECURITY;
ALTER TABLE time_off_requests  FORCE ROW LEVEL SECURITY;

-- FORCE RLS s'applique même au propriétaire de la table (rôle superuser exclus)
-- Créer un rôle applicatif non-superuser pour l'application
CREATE ROLE app_user LOGIN PASSWORD 'secret';
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
```

**Étape 2 : Créer les policies RLS**

```sql
-- Policy universelle : lire/écrire uniquement les données de son organisation
CREATE POLICY tenant_isolation ON employees
  USING (organisation_id = current_setting('app.organisation_id', true)::BIGINT)
  WITH CHECK (organisation_id = current_setting('app.organisation_id', true)::BIGINT);

-- Idem pour toutes les autres tables
CREATE POLICY tenant_isolation ON departments
  USING (organisation_id = current_setting('app.organisation_id', true)::BIGINT)
  WITH CHECK (organisation_id = current_setting('app.organisation_id', true)::BIGINT);

CREATE POLICY tenant_isolation ON payroll_records
  USING (organisation_id = current_setting('app.organisation_id', true)::BIGINT)
  WITH CHECK (organisation_id = current_setting('app.organisation_id', true)::BIGINT);

-- Policy spécifique pour les super-admins (contournement pour support/debug)
CREATE POLICY super_admin_bypass ON employees
  USING (current_setting('app.role', true) = 'SUPER_ADMIN');
```

**Étape 3 : Middleware Prisma pour setter le contexte**

```typescript
import { PrismaClient, Prisma } from '@prisma/client';

// Extension Prisma qui injecte app.organisation_id dans chaque transaction
function createTenantPrismaClient(organisationId: number): PrismaClient {
  return new PrismaClient().$extends({
    query: {
      $allModels: {
        async $allOperations({ args, query }) {
          // Toutes les opérations sont enveloppées dans une transaction
          // qui définit d'abord le context RLS
          const [, result] = await prismaBase.$transaction([
            prismaBase.$executeRaw`
              SELECT set_config('app.organisation_id', ${organisationId.toString()}, true)
            `,
            query(args),
          ]);
          return result;
        },
      },
    },
  });
}

// Utilisation dans les handlers HTTP
async function handler(req: Request, res: Response) {
  const { organisationId } = req.user; // Extrait du JWT
  const db = createTenantPrismaClient(organisationId);

  // Même si on oublie un filtre WHERE, RLS bloque les données des autres organisations
  const employees = await db.employees.findMany({
    where: { departmentId: req.params.departmentId }
    // Pas besoin de WHERE organisation_id = ... : RLS le fait automatiquement
  });

  res.json(employees);
}
```

**Étape 4 : Tests d'isolation automatisés**

```typescript
describe('RLS tenant isolation', () => {
  let orgA: TestOrganisation;
  let orgB: TestOrganisation;

  beforeAll(async () => {
    orgA = await createTestOrganisation('Org A');
    orgB = await createTestOrganisation('Org B');

    // Créer des employés dans chaque organisation
    await seedEmployees(orgA.id, 5);
    await seedEmployees(orgB.id, 5);
  });

  it('Organisation A ne peut pas voir les employés de Organisation B', async () => {
    const dbA = createTenantPrismaClient(orgA.id);

    // Requête sans filtre explicite sur organisation_id
    const employees = await dbA.employees.findMany();

    // RLS doit garantir que seuls les employés de orgA sont retournés
    expect(employees).toHaveLength(5);
    expect(employees.every(e => e.organisationId === orgA.id)).toBe(true);
  });

  it('Une requête raw SQL est aussi protégée par RLS', async () => {
    const dbA = createTenantPrismaClient(orgA.id);

    // Même une requête raw tente de contourner les filtres applicatifs
    const result = await dbA.$queryRaw<Array<{ id: number }>>`
      SELECT id FROM employees
    `;

    // RLS filtre malgré l'absence de WHERE
    expect(result.every(r => orgAEmployeeIds.includes(r.id))).toBe(true);
  });

  it('Accès cross-tenant via id direct est bloqué', async () => {
    const dbA = createTenantPrismaClient(orgA.id);
    const orgBEmployeeId = (await getOrgBEmployees())[0].id;

    // Tentative de lecture directe par ID d'un employé de orgB
    const employee = await dbA.employees.findUnique({
      where: { id: orgBEmployeeId }
    });

    // RLS retourne null (pas d'erreur, juste aucun résultat)
    expect(employee).toBeNull();
  });
});
```

### Résultats mesurés

| Métrique | Avant RLS | Après RLS |
|---|---|---|
| Fuites de données | 1 incident détecté | 0 en 18 mois |
| Audit de sécurité externe | Échoué (isolation insuffisante) | Validé (SOC 2 Type II) |
| Overhead de performance RLS | — | < 2ms par requête |
| Complexité du code applicatif | Filtre manuel partout | Simplifié (RLS gère l'isolation) |

**Leçon clé** : RLS est la dernière ligne de défense, pas la première. Le code applicatif peut avoir des bugs, les développeurs peuvent oublier des filtres, des bibliothèques tierces peuvent contourner les filtres ORM. La base de données doit garantir l'isolation même quand tout le reste échoue.

---

## Cas 4 — TimescaleDB pour l'IoT : startup énergie, 50M mesures/jour

### Contexte

Startup développant une plateforme de monitoring énergétique pour les bâtiments industriels. 10 000 capteurs (énergie électrique, température, humidité) envoient une mesure toutes les 2 secondes. Cela représente 5 000 mesures/seconde, soit 432 millions de mesures/jour.

Infrastructure initiale : PostgreSQL 15 classique sur une instance AWS RDS `db.r6g.2xlarge` (8 vCPU, 64 GB RAM).

### Problème

Après 18 mois de production, la table `measurements` atteint 2 milliards de lignes et 1,2 TB de stockage.

```sql
-- Table originale
CREATE TABLE measurements (
  id          BIGSERIAL PRIMARY KEY,
  sensor_id   INT           NOT NULL,
  value       DOUBLE PRECISION NOT NULL,
  unit        VARCHAR(20)   NOT NULL,
  recorded_at TIMESTAMPTZ   NOT NULL
);
CREATE INDEX idx_measurements_sensor_time ON measurements (sensor_id, recorded_at DESC);
```

Symptômes :
- Requête d'agrégation horaire sur 30 jours : **28 à 35 secondes** (inacceptable pour le dashboard)
- VACUUM autovacuum constamment en retard : `n_dead_tup` dépasse 500 millions
- Taille des WAL : 40 GB/jour (backups coûteux)
- RDS atteint les limites de CPU lors des pics d'ingestion

### Solution : migration vers TimescaleDB

**Étape 1 : Installer l'extension et convertir la table**

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Convertir la table existante en hypertable
-- chunk_time_interval = 1 jour : chaque chunk couvre 24h de données
-- (à 432M mesures/jour, chaque chunk pèse environ 600 MB)
SELECT create_hypertable(
  'measurements',
  'recorded_at',
  chunk_time_interval => INTERVAL '1 day',
  migrate_data => true  -- Migrer les données existantes (long, faire en maintenance)
);

-- TimescaleDB recréé automatiquement les partitions (chunks)
-- Vérification des chunks créés
SELECT
  chunk_name,
  range_start,
  range_end,
  pg_size_pretty(total_bytes) AS size
FROM timescaledb_information.chunks
WHERE hypertable_name = 'measurements'
ORDER BY range_start DESC
LIMIT 10;
```

**Étape 2 : Activer la compression automatique**

```sql
-- Configurer la compression par capteur (segmentby = tri des données dans le chunk compressé)
ALTER TABLE measurements SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'sensor_id',
  timescaledb.compress_orderby   = 'recorded_at DESC'
);

-- Compresser automatiquement les chunks de plus de 7 jours
SELECT add_compression_policy('measurements', INTERVAL '7 days');

-- Forcer la compression des chunks historiques existants
SELECT compress_chunk(c.chunk_name)
FROM timescaledb_information.chunks c
WHERE c.hypertable_name = 'measurements'
  AND c.range_end < NOW() - INTERVAL '7 days'
  AND NOT c.is_compressed;

-- Résultat de la compression
SELECT
  chunk_name,
  pg_size_pretty(before_compression_total_bytes) AS avant,
  pg_size_pretty(after_compression_total_bytes)  AS apres,
  ROUND((1 - after_compression_total_bytes::NUMERIC
             / before_compression_total_bytes) * 100, 1) AS reduction_pct
FROM chunk_compression_stats('measurements')
ORDER BY chunk_name DESC
LIMIT 5;
-- Résultat typique : réduction de 75-85% (1.2 TB → 280 GB)
```

**Étape 3 : Continuous Aggregates pour les dashboards**

```sql
-- Agrégat par minute (pour les graphiques haute résolution, 24h)
CREATE MATERIALIZED VIEW measurements_1min
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 minute', recorded_at) AS bucket,
  sensor_id,
  AVG(value)  AS avg_value,
  MAX(value)  AS max_value,
  MIN(value)  AS min_value,
  COUNT(*)    AS nb_samples
FROM measurements
GROUP BY bucket, sensor_id
WITH NO DATA;

SELECT add_continuous_aggregate_policy('measurements_1min',
  start_offset      => INTERVAL '2 hours',
  end_offset        => INTERVAL '1 minute',
  schedule_interval => INTERVAL '1 minute'
);

-- Agrégat par heure (pour les graphiques 30 jours, 1 an)
CREATE MATERIALIZED VIEW measurements_1hour
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', bucket) AS bucket,
  sensor_id,
  AVG(avg_value)  AS avg_value,
  MAX(max_value)  AS max_value,
  MIN(min_value)  AS min_value,
  SUM(nb_samples) AS nb_samples
FROM measurements_1min  -- Aggregat sur aggregat : plus efficace
GROUP BY time_bucket('1 hour', bucket), sensor_id
WITH NO DATA;

SELECT add_continuous_aggregate_policy('measurements_1hour',
  start_offset      => INTERVAL '3 hours',
  end_offset        => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour'
);
```

**Étape 4 : Retention policy**

```sql
-- Conserver les données brutes pendant 2 ans
SELECT add_retention_policy('measurements', INTERVAL '2 years');

-- Les continuous aggregates ont leur propre retention
SELECT add_retention_policy('measurements_1min',  INTERVAL '90 days');
SELECT add_retention_policy('measurements_1hour', INTERVAL '5 years');
```

**Requêtes optimisées sur les continuous aggregates :**

```sql
-- Dashboard : énergie horaire pour un bâtiment sur 30 jours
-- Requête sur le continuous aggregate (données pré-agrégées)
SELECT
  bucket,
  SUM(avg_value) AS total_kwh,
  MAX(max_value) AS peak_power
FROM measurements_1hour
WHERE bucket BETWEEN NOW() - INTERVAL '30 days' AND NOW()
  AND sensor_id = ANY(
    SELECT id FROM sensors WHERE building_id = $1 AND type = 'ENERGY'
  )
GROUP BY bucket
ORDER BY bucket ASC;
-- Durée : 0.28s (vs 32s avant sur les données brutes)

-- Alerte temps réel : capteurs hors-seuil dans la dernière heure
-- Requête sur les données brutes récentes (< 1 jour, chunk non compressé)
SELECT
  sensor_id,
  time_bucket('5 minutes', recorded_at) AS bucket,
  AVG(value) AS avg_value
FROM measurements
WHERE recorded_at > NOW() - INTERVAL '1 hour'
  AND sensor_id = ANY(SELECT id FROM sensors WHERE type = 'TEMPERATURE')
GROUP BY sensor_id, bucket
HAVING AVG(value) > 35.0  -- Seuil d'alerte
ORDER BY bucket DESC;
```

### Résultats mesurés

| Métrique | PostgreSQL classique | TimescaleDB | Amélioration |
|---|---|---|---|
| Requête agrégation 30 jours | 28-35 secondes | 0.28 secondes | -99% |
| Stockage total (1.2 TB) | 1 200 GB | 290 GB | -76% |
| Ingestion (mesures/sec) | 3 200 max | 8 500 max | +165% |
| VACUUM retard | Permanent | Automatique par chunk | Résolu |
| Coût RDS mensuel | 2 800 $/mois | 1 100 $/mois | -61% |

**Leçon clé** : TimescaleDB est PostgreSQL pour les time-series — même SQL, mêmes drivers, même ORM, migration transparente. La réécriture de l'application est quasi-nulle (seule la couche de création de table change). Pour tout projet gérant des données temporelles volumineuses, évaluer TimescaleDB avant d'envisager InfluxDB ou Cassandra qui imposent un changement complet de stack.
