# Migrations Zero-Downtime — Expand/Contract et Outils

## Le pattern Expand/Contract : principe fondamental

Toute migration directe sur une table en production (`ALTER TABLE ... ALTER COLUMN`, `ALTER TABLE ... RENAME COLUMN`) pose un verrou exclusif (`AccessExclusiveLock`) qui bloque toutes les lectures et écritures pendant sa durée. Sur une table de 10 millions de lignes, cette durée peut être de 5 à 45 minutes. Le pattern Expand/Contract découpe chaque migration en trois phases déployées indépendamment, sans aucun verrou prolongé.

**Règle absolue** : toute modification de schéma sur une table dépassant 100 000 lignes doit passer par ce pattern.

### Phase 1 — Expand (ajouter sans casser)

L'objectif est d'ajouter les nouvelles colonnes ou structures en les rendant optionnelles, sans toucher aux colonnes existantes. Le code existant continue de fonctionner sans modification.

```sql
-- Exemple : renommer une colonne "name" en "product_name"
-- Phase Expand : ajouter la nouvelle colonne nullable
ALTER TABLE products ADD COLUMN product_name TEXT;

-- Exemple : split d'une colonne "full_name" en "first_name" + "last_name"
ALTER TABLE users ADD COLUMN first_name TEXT;
ALTER TABLE users ADD COLUMN last_name TEXT;

-- Exemple : ajouter une colonne NOT NULL avec défaut (safe car défaut est évalué immédiatement en PG 11+)
ALTER TABLE orders ADD COLUMN currency VARCHAR(3) NOT NULL DEFAULT 'EUR';
-- En PG 11+, ceci est instantané si le défaut est immutable (pas de verrou prolongé)
```

### Phase 2 — Backfill (remplir les données)

Le backfill remplit les nouvelles colonnes par batches pour éviter de monopoliser les I/O et de provoquer une contention de locks.

```sql
-- Backfill de la colonne "product_name" depuis "name"
-- Traitement par batches de 1000 lignes avec pause entre chaque batch
DO $$
DECLARE
  batch_size INT := 1000;
  offset_val INT := 0;
  rows_updated INT;
  total_updated INT := 0;
  start_time TIMESTAMPTZ := clock_timestamp();
  estimated_total INT;
BEGIN
  SELECT COUNT(*) INTO estimated_total FROM products WHERE product_name IS NULL;
  RAISE NOTICE 'Backfill à effectuer : % lignes', estimated_total;

  LOOP
    UPDATE products
    SET product_name = name
    WHERE id IN (
      SELECT id FROM products
      WHERE product_name IS NULL
      ORDER BY id
      LIMIT batch_size
    );

    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;

    total_updated := total_updated + rows_updated;

    -- Estimer le temps restant
    DECLARE
      elapsed INTERVAL := clock_timestamp() - start_time;
      rate FLOAT := total_updated / EXTRACT(EPOCH FROM elapsed);
      remaining FLOAT := (estimated_total - total_updated) / NULLIF(rate, 0);
    BEGIN
      RAISE NOTICE 'Progression : %/% lignes (%.1f%%), ~% secondes restantes',
        total_updated, estimated_total,
        (total_updated::FLOAT / estimated_total * 100),
        remaining::INT;
    END;

    -- Pause pour laisser respirer le système (100ms)
    PERFORM pg_sleep(0.1);
  END LOOP;

  RAISE NOTICE 'Backfill terminé : % lignes en %', total_updated, clock_timestamp() - start_time;
END $$;
```

Pour le monitoring du backfill en temps réel depuis une autre session :

```sql
-- Surveiller la progression du backfill
SELECT
  COUNT(*) FILTER (WHERE product_name IS NOT NULL) AS migrated,
  COUNT(*) FILTER (WHERE product_name IS NULL)     AS remaining,
  ROUND(
    COUNT(*) FILTER (WHERE product_name IS NOT NULL)::NUMERIC / COUNT(*) * 100, 2
  ) AS pct_done
FROM products;
```

### Phase 3 — Contract (supprimer l'ancienne structure)

Une fois que tout le code applicatif utilise la nouvelle colonne et que le backfill est complet, on supprime l'ancienne structure.

```sql
-- Avant de supprimer, vérifier qu'il n'y a plus de données manquantes
SELECT COUNT(*) FROM products WHERE product_name IS NULL;
-- Doit retourner 0

-- Poser la contrainte NOT NULL (voir section dédiée plus bas)
ALTER TABLE products ALTER COLUMN product_name SET NOT NULL;

-- Supprimer l'ancienne colonne
ALTER TABLE products DROP COLUMN name;
```

---

## Cas courants d'Expand/Contract

### Changer le type d'une colonne (ex. INT → BIGINT)

```sql
-- Phase Expand
ALTER TABLE events ADD COLUMN id_new BIGINT;

-- Phase Backfill
UPDATE events SET id_new = id::BIGINT WHERE id_new IS NULL;
-- (en batches, voir ci-dessus)

-- Phase Contract
ALTER TABLE events ALTER COLUMN id_new SET NOT NULL;
ALTER TABLE events DROP COLUMN id;
ALTER TABLE events RENAME COLUMN id_new TO id;
-- Note : RENAME est instantané (pas de lock prolongé, juste un AccessExclusiveLock très bref)
```

### Ajouter une contrainte UNIQUE sur une colonne existante

```sql
-- Phase Expand : créer l'index CONCURRENTLY (sans lock de table)
CREATE UNIQUE INDEX CONCURRENTLY idx_users_email_unique ON users (email);

-- Phase Contract : transformer l'index en contrainte (instantané, utilise l'index existant)
ALTER TABLE users ADD CONSTRAINT uq_users_email UNIQUE USING INDEX idx_users_email_unique;
```

### Ajouter une contrainte NOT NULL sur une colonne existante

```sql
-- Phase Expand : contrainte avec NOT VALID (ne vérifie pas les lignes existantes)
ALTER TABLE products ADD CONSTRAINT chk_product_name_not_null
  CHECK (product_name IS NOT NULL) NOT VALID;
-- Cette instruction est quasi-instantanée

-- Phase Backfill : corriger les valeurs NULL existantes
UPDATE products SET product_name = 'Sans nom' WHERE product_name IS NULL;

-- Phase Contract : valider la contrainte (scan sans lock d'écriture)
ALTER TABLE products VALIDATE CONSTRAINT chk_product_name_not_null;
-- VALIDATE acquiert uniquement un ShareUpdateExclusiveLock (compatible avec les lectures/écritures)
```

---

## Contraintes sans lock : NOT VALID + VALIDATE

Le mécanisme `NOT VALID` est l'un des outils les plus puissants pour les migrations sans downtime.

Quand on ajoute une contrainte avec `NOT VALID` :
1. PostgreSQL pose un `ShareRowExclusiveLock` très bref pour enregistrer la contrainte dans le catalogue
2. Les nouvelles lignes insérées ou mises à jour sont vérifiées immédiatement
3. Les lignes existantes ne sont PAS vérifiées

`VALIDATE CONSTRAINT` scanne ensuite toutes les lignes existantes avec uniquement un `ShareUpdateExclusiveLock`, compatible avec les INSERT/UPDATE/DELETE concurrents.

```sql
-- Pattern complet pour une clé étrangère sur une table active
-- (ADD FOREIGN KEY classique poserait un verrou sur les deux tables)
ALTER TABLE orders ADD CONSTRAINT fk_orders_customer_id
  FOREIGN KEY (customer_id) REFERENCES customers(id)
  NOT VALID;

-- Plus tard (après vérification des données), en dehors des heures de pointe
ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_customer_id;
```

---

## Ajout d'index sans lock : CREATE INDEX CONCURRENTLY

`CREATE INDEX CONCURRENTLY` construit l'index en plusieurs passes sans jamais bloquer les lectures ou écritures. La contrepartie est une durée plus longue (environ 2-3× plus long qu'un `CREATE INDEX` classique).

```sql
-- Création d'un index sans lock de table
CREATE INDEX CONCURRENTLY idx_orders_user_created
  ON orders (user_id, created_at DESC)
  WHERE status != 'CANCELLED';

-- Surveiller la progression
SELECT
  phase,
  blocks_done,
  blocks_total,
  ROUND(blocks_done::NUMERIC / NULLIF(blocks_total, 0) * 100, 1) AS pct_done,
  tuples_done,
  tuples_total
FROM pg_stat_progress_create_index
WHERE relid = 'orders'::regclass;
```

### Que faire si CREATE INDEX CONCURRENTLY échoue à mi-chemin ?

En cas d'échec, PostgreSQL laisse un index "invalide" (`pg_index.indisvalid = false`). Cet index ne sert pas aux requêtes mais consomme des ressources en écriture.

```sql
-- Détecter les index invalides
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE NOT EXISTS (
  SELECT 1 FROM pg_index pi
  JOIN pg_class pc ON pc.oid = pi.indexrelid
  WHERE pc.relname = pg_indexes.indexname
  AND pi.indisvalid
);

-- Supprimer l'index invalide (DROP INDEX CONCURRENTLY pour éviter le lock)
DROP INDEX CONCURRENTLY idx_orders_user_created;

-- Recréer
CREATE INDEX CONCURRENTLY idx_orders_user_created ON orders (user_id, created_at DESC);
```

---

## Prisma Migrate en production

### prisma migrate dev vs prisma migrate deploy

| Commande | Environnement | Comportement |
|---|---|---|
| `prisma migrate dev` | Développement local | Crée une shadow DB, génère une migration, applique sur la DB locale |
| `prisma migrate deploy` | Production / CI | Applique uniquement les migrations pending, pas de shadow DB |

```bash
# En production (CI/CD pipeline)
npx prisma migrate deploy

# Vérifier l'état des migrations sans appliquer
npx prisma migrate status

# Si une migration a été appliquée manuellement et qu'on veut la marquer comme appliquée
npx prisma migrate resolve --applied "20240115_add_slug_column"
```

### Shadow database

La shadow database est une base temporaire créée et détruite par `prisma migrate dev` pour valider les migrations. En production, elle n'est pas utilisée. Dans les environnements cloud (PlanetScale, Supabase), elle peut nécessiter une configuration explicite :

```
# .env
DATABASE_URL="postgresql://user:pass@host/mydb"
SHADOW_DATABASE_URL="postgresql://user:pass@host/mydb_shadow"
```

### Résoudre les conflits de migrations en équipe

Quand deux développeurs créent des migrations simultanément :

```bash
# Développeur A a créé 20240115_add_slug, développeur B a créé 20240115_add_tags
# Les deux ont été mergés — historique divergent

# Vérifier l'état
npx prisma migrate status
# Affiche : "Found failed migration 20240115_add_tags"

# Option 1 : marquer la migration comme appliquée (si elle l'a été manuellement)
npx prisma migrate resolve --applied "20240115_add_tags"

# Option 2 : réinitialiser en développement (JAMAIS en production)
npx prisma migrate reset --skip-seed
```

---

## Flyway vs Liquibase : comparaison

| Critère | Flyway | Liquibase |
|---|---|---|
| Format des migrations | SQL pur (recommandé) ou Java | SQL, XML, YAML, JSON |
| Convention de nommage | `V1__description.sql` | Fichier changelog XML/YAML |
| Undo migrations | Flyway Teams (payant) | Natif (rollback tag) |
| Dry-run | Flyway Teams | `--dry-run` en ligne de commande |
| Intégration CI | Simple (jar ou plugin Maven/Gradle) | Idem |
| Répéatable | `R__description.sql` (s'applique si le contenu change) | `runOnChange: true` |

```sql
-- Flyway : fichier V3__add_slug_to_products.sql
-- Conventions : V{version}__{description}.sql (double underscore)
ALTER TABLE products ADD COLUMN slug TEXT;
CREATE INDEX CONCURRENTLY idx_products_slug ON products (slug);
```

```yaml
# Liquibase : fichier changelog.yaml
databaseChangeLog:
  - changeSet:
      id: 3
      author: pierre
      changes:
        - addColumn:
            tableName: products
            columns:
              - column:
                  name: slug
                  type: text
        - createIndex:
            tableName: products
            indexName: idx_products_slug
            columns:
              - column:
                  name: slug
```

---

## Multi-step deploy workflow

Ce workflow garantit qu'à aucun moment le code en production et le schéma de base de données ne sont incompatibles.

```
Phase 1 : Déploiement DB (Expand)
  - Appliquer la migration d'expand (nouvelles colonnes nullable)
  - L'ancien code en production fonctionne (ignore les nouvelles colonnes)

Phase 2 : Déploiement application
  - Le nouveau code écrit dans les deux colonnes (ancienne et nouvelle)
  - Le nouveau code lit depuis la nouvelle colonne si elle est non-null, sinon l'ancienne

Phase 3 : Backfill
  - Script de backfill comble les lignes non migrées
  - Surveillance de la progression

Phase 4 : Déploiement DB (Contract)
  - Ajouter les contraintes (NOT VALID puis VALIDATE)
  - Supprimer les anciennes colonnes

Phase 5 : Déploiement application cleanup
  - Supprimer le code de compatibilité (lecture de l'ancienne colonne)
```

---

## Testing des migrations

### Test avec Testcontainers (TypeScript)

```typescript
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { execSync } from 'child_process';

describe('Migration: add_slug_to_products', () => {
  let container: StartedPostgreSqlContainer;
  let connectionString: string;

  beforeAll(async () => {
    container = await new PostgreSqlContainer('postgres:16')
      .withDatabase('testdb')
      .withUsername('testuser')
      .withPassword('testpass')
      .start();

    connectionString = container.getConnectionUri();

    // Appliquer toutes les migrations jusqu'à la précédente
    process.env.DATABASE_URL = connectionString;
    execSync('npx prisma migrate deploy', { env: process.env });
  }, 60_000);

  afterAll(async () => {
    await container.stop();
  });

  it('la migration est réversible', async () => {
    // Vérifier que la colonne slug existe
    const result = await db.query(`
      SELECT column_name FROM information_schema.columns
      WHERE table_name = 'products' AND column_name = 'slug'
    `);
    expect(result.rows).toHaveLength(1);
  });

  it('le backfill ne laisse aucune valeur NULL', async () => {
    // Insérer des données de test
    await db.query(`INSERT INTO products (name) VALUES ('Test Product')`);
    // Exécuter le backfill
    await runBackfillScript();
    // Vérifier
    const nullCount = await db.query(
      `SELECT COUNT(*) FROM products WHERE slug IS NULL`
    );
    expect(parseInt(nullCount.rows[0].count)).toBe(0);
  });
});
```

---

## Monitoring pendant une migration

```sql
-- Sessions actives et leur état de lock
SELECT
  pid,
  state,
  wait_event_type,
  wait_event,
  ROUND(EXTRACT(EPOCH FROM (clock_timestamp() - query_start))::NUMERIC, 2) AS duration_sec,
  LEFT(query, 80) AS query_preview
FROM pg_stat_activity
WHERE state != 'idle'
  AND query_start < clock_timestamp() - INTERVAL '5 seconds'
ORDER BY duration_sec DESC;

-- Détecter les locks bloquants
SELECT
  blocked.pid          AS blocked_pid,
  blocked.query        AS blocked_query,
  blocking.pid         AS blocking_pid,
  blocking.query       AS blocking_query,
  ROUND(EXTRACT(EPOCH FROM (clock_timestamp() - blocked.query_start))::NUMERIC, 2) AS wait_sec
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked
  ON blocked.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
  ON blocking_locks.locktype = blocked_locks.locktype
  AND blocking_locks.relation = blocked_locks.relation
  AND blocking_locks.pid != blocked_locks.pid
  AND blocking_locks.granted
JOIN pg_catalog.pg_stat_activity blocking
  ON blocking.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

---

## Rollback strategies

### Guard clauses IF EXISTS

```sql
-- Migration forward
ALTER TABLE products ADD COLUMN IF NOT EXISTS slug TEXT;

-- Migration de rollback (compensation)
ALTER TABLE products DROP COLUMN IF EXISTS slug;
```

### PITR (Point In Time Recovery)

Avant toute migration risquée, déclencher un snapshot manuel dans votre cloud provider, puis noter le LSN (Log Sequence Number) exact :

```sql
-- Noter le LSN avant la migration
SELECT pg_current_wal_lsn();
-- Résultat : 0/1A3F2B8

-- En cas de besoin de retour arrière, restaurer jusqu'à ce LSN
-- (via pg_basebackup + WAL replay, ou via la console AWS RDS / GCP CloudSQL)
```

La stratégie de rollback doit être choisie avant de commencer la migration :
- **Compensation** (recommandée) : script SQL inverse, applicable en quelques secondes
- **Snapshot restore** : accepter X minutes de perte de données entre le snapshot et le moment du problème
- **PITR** : restauration sans perte de données, mais peut prendre 30-60 minutes selon la taille
