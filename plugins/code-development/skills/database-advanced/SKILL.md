---
name: database-advanced
version: 1.0.0
description: >
  Zero-downtime database migrations, expand-contract pattern, Prisma migrate,
  Flyway Liquibase, query optimization EXPLAIN ANALYZE, database indexing strategies,
  table partitioning, sharding, read replicas, connection pooling PgBouncer,
  CQRS read models materialized views, time-series databases TimescaleDB,
  graph databases Neo4j, multi-tenant databases row-level security,
  PostgreSQL advanced features, database performance tuning
---

# Database Advanced — Migrations, Performance et Patterns Avancés

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu dois faire évoluer le schéma d'une base de données sans downtime en production
- Les queries deviennent lentes et tu dois analyser et optimiser les plans d'exécution
- Tu dois scaler une base de données (partitioning, read replicas, sharding)
- Tu as des besoins multi-tenant et dois isoler les données entre clients
- Tu veux utiliser des vues matérialisées ou des tables de lecture CQRS
- Tu considères une base de données spécialisée (time-series, graphe)

---

## Migrations Zéro Downtime — Expand/Contract

Le pattern expand-contract permet de modifier le schéma sans interrompre le service.

```
Étape 1 — EXPAND : ajouter sans supprimer
Déployer la migration + déployer le code qui écrit DANS LES DEUX colonnes

Étape 2 — MIGRATE : backfill des données existantes
Script de migration des données (traitement par batch)

Étape 3 — CONTRACT : supprimer l'ancienne structure
Déployer le code qui ne lit plus l'ancienne colonne, puis supprimer
```

### Exemple : Renommer une colonne

```sql
-- ❌ Rename direct → downtime immédiat
ALTER TABLE utilisateurs RENAME COLUMN nom TO nom_complet;

-- ✅ Expand/Contract

-- Déploiement 1 : EXPAND — ajouter la nouvelle colonne
ALTER TABLE utilisateurs ADD COLUMN nom_complet TEXT;

-- Déploiement 1 : code qui écrit dans les deux colonnes
-- UPDATE users SET nom_complet = nom WHERE nom_complet IS NULL;
-- Dans l'appli :
-- await prisma.utilisateur.update({ data: { nom, nom_complet: nom } });

-- Script de backfill (par batch pour éviter les locks)
DO $$
DECLARE batch_size INT := 1000;
DECLARE last_id BIGINT := 0;
BEGIN
  LOOP
    WITH batch AS (
      SELECT id FROM utilisateurs
      WHERE id > last_id AND nom_complet IS NULL
      ORDER BY id LIMIT batch_size
    )
    UPDATE utilisateurs u
    SET nom_complet = u.nom
    FROM batch
    WHERE u.id = batch.id;

    GET DIAGNOSTICS last_id = ROW_COUNT;
    EXIT WHEN last_id = 0;
    PERFORM pg_sleep(0.1);  -- Laisser respirer
  END LOOP;
END $$;

-- Déploiement 2 : CONTRACT — après que tout lit nom_complet
ALTER TABLE utilisateurs DROP COLUMN nom;
ALTER TABLE utilisateurs ALTER COLUMN nom_complet SET NOT NULL;
```

### Ajouter une contrainte NOT NULL sans lock

```sql
-- ❌ Bloque la table entière
ALTER TABLE commandes ALTER COLUMN référence SET NOT NULL;

-- ✅ Zéro downtime avec une contrainte validée progressivement
-- Étape 1 : contrainte NOT VALID (vérification rapide, n'inspecte pas les données existantes)
ALTER TABLE commandes
ADD CONSTRAINT commandes_reference_not_null
CHECK (référence IS NOT NULL) NOT VALID;

-- Étape 2 : validation progressive (n'acquiert pas de lock exclusif)
ALTER TABLE commandes VALIDATE CONSTRAINT commandes_reference_not_null;
```

---

## EXPLAIN ANALYZE — Diagnostiquer les Requêtes Lentes

```sql
-- Toujours utiliser EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT
  c.id, c.référence, c.total,
  u.email,
  COUNT(lc.id) AS nb_lignes
FROM commandes c
JOIN utilisateurs u ON u.id = c.utilisateur_id
LEFT JOIN lignes_commande lc ON lc.commande_id = c.id
WHERE c.statut = 'EN_ATTENTE'
  AND c.créee_a >= NOW() - INTERVAL '30 days'
GROUP BY c.id, u.email
ORDER BY c.créee_a DESC
LIMIT 50;
```

### Lire un plan d'exécution

```
Gather Merge  (cost=... actual time=1205..1312 rows=50 loops=1)
  ->  Sort  (cost=... actual time=... rows=...)
        Sort Key: c.créee_a DESC
        Sort Method: quicksort  Memory: 5kB
        ->  Hash Join  (cost=... actual time=... rows=...)       ← JOIN hash = bon
              Hash Cond: (lc.commande_id = c.id)
              ->  Seq Scan on lignes_commande lc               ← ❌ Full scan = problème
              ->  Hash  (cost=... actual time=...)
                    ->  Index Scan on commandes c               ← ✅ Index utilisé
                          Index Cond: (statut = 'EN_ATTENTE')
                          Filter: (créee_a >= ...)
Buffers: shared hit=847 read=12450                             ← 12450 blocs lus du disque
```

**Signaux d'alarme :**
- `Seq Scan` sur une grande table → manque d'index
- `Buffers: read=...` élevé → données pas en cache
- `Hash Join` sur millions de lignes → envisager un index sur la clé de jointure

---

## Stratégies d'Indexation

```sql
-- Index composite : l'ordre des colonnes compte (leftmost prefix rule)
-- Optimal pour : WHERE statut = ? AND créee_a >= ?
CREATE INDEX idx_commandes_statut_date
ON commandes (statut, créee_a DESC)
WHERE statut != 'LIVREE';  -- Index partiel (moins volumineux)

-- Index pour les recherches full-text
ALTER TABLE produits ADD COLUMN recherche_ts tsvector
  GENERATED ALWAYS AS (
    to_tsvector('french', coalesce(nom, '') || ' ' || coalesce(description, ''))
  ) STORED;

CREATE INDEX idx_produits_recherche ON produits USING GIN(recherche_ts);

-- Requête full-text
SELECT * FROM produits
WHERE recherche_ts @@ plainto_tsquery('french', 'smartphone 5G')
ORDER BY ts_rank(recherche_ts, plainto_tsquery('french', 'smartphone 5G')) DESC;

-- Index pour JSONB
CREATE INDEX idx_metadonnees_type
ON produits USING GIN (metadonnees jsonb_path_ops);

-- Requête JSONB optimisée
SELECT * FROM produits WHERE metadonnees @> '{"categorie": "electronique"}';

-- Créer un index sans bloquer les écritures
CREATE INDEX CONCURRENTLY idx_utilisateurs_email ON utilisateurs (email);
```

---

## Partitioning — Gérer les Grandes Tables

```sql
-- Partitioning par plage de dates (commandes)
CREATE TABLE commandes_partitioned (
  id BIGINT NOT NULL,
  référence TEXT NOT NULL,
  statut TEXT NOT NULL,
  total NUMERIC NOT NULL,
  créee_a TIMESTAMPTZ NOT NULL,
  PRIMARY KEY (id, créee_a)
) PARTITION BY RANGE (créee_a);

-- Créer les partitions automatiquement
CREATE TABLE commandes_2024_01 PARTITION OF commandes_partitioned
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Automatiser avec pg_partman
SELECT partman.create_parent(
  p_parent_table := 'public.commandes_partitioned',
  p_control := 'créee_a',
  p_type := 'range',
  p_interval := '1 month',
  p_premake := 3  -- Créer 3 partitions à l'avance
);

-- Avantage : PostgreSQL ne scanne que la partition concernée
EXPLAIN SELECT * FROM commandes_partitioned
WHERE créee_a BETWEEN '2024-01-01' AND '2024-01-31';
-- → Seq Scan on commandes_2024_01 (seulement la partition de janvier)
```

---

## Row-Level Security (RLS) — Multi-Tenant

```sql
-- Activer RLS sur la table
ALTER TABLE projets ENABLE ROW LEVEL SECURITY;

-- Politique : chaque utilisateur ne voit que ses projets
CREATE POLICY projets_isolation ON projets
  FOR ALL
  USING (organisation_id = current_setting('app.organisation_id')::UUID);

-- Politique admin
CREATE POLICY projets_admin ON projets
  FOR ALL
  TO admin_role
  USING (true);  -- Les admins voient tout
```

```typescript
// Prisma avec RLS : fixer le context par requête
async function getPrismaClient(organisationId: string): Promise<PrismaClient> {
  const client = new PrismaClient();

  await client.$executeRaw`
    SET LOCAL app.organisation_id = ${organisationId}
  `;

  return client;
}

// Ou via middleware Prisma
const prisma = new PrismaClient().$extends({
  query: {
    $allOperations: async ({ args, query }) => {
      // Le context est déjà défini par le middleware Express
      return query(args);
    },
  },
});
```

---

## Connection Pooling avec PgBouncer

```ini
; pgbouncer.ini
[databases]
production = host=db.prod.svc pool_size=20 max_db_connections=100

[pgbouncer]
pool_mode = transaction      ; transaction | session | statement
max_client_conn = 1000       ; Connexions clients maximum
default_pool_size = 20       ; Connexions vers PostgreSQL par DB
min_pool_size = 5
server_idle_timeout = 600
```

```typescript
// Prisma avec PgBouncer
// DATABASE_URL=postgresql://user:pass@pgbouncer:6432/db?pgbouncer=true
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
  // Désactiver les advisory locks (incompatibles avec pgbouncer transaction mode)
});
```

---

## Vues Matérialisées — Read Models CQRS

```sql
-- Vue matérialisée pour le tableau de bord (recalculée toutes les heures)
CREATE MATERIALIZED VIEW dashboard_stats AS
SELECT
  DATE_TRUNC('day', c.créee_a) AS jour,
  COUNT(DISTINCT c.id) AS nb_commandes,
  COUNT(DISTINCT c.utilisateur_id) AS clients_actifs,
  SUM(c.total) AS ca,
  AVG(c.total) AS panier_moyen,
  COUNT(DISTINCT c.id) FILTER (WHERE c.statut = 'ANNULEE') AS annulations
FROM commandes c
WHERE c.créee_a >= NOW() - INTERVAL '90 days'
GROUP BY DATE_TRUNC('day', c.créee_a)
ORDER BY jour DESC;

CREATE UNIQUE INDEX ON dashboard_stats (jour);

-- Rafraîchir sans bloquer les lectures
REFRESH MATERIALIZED VIEW CONCURRENTLY dashboard_stats;

-- Scheduler: pg_cron
SELECT cron.schedule('rafraichir-dashboard', '0 * * * *',
  'REFRESH MATERIALIZED VIEW CONCURRENTLY dashboard_stats');
```

---

## Références

- `references/migrations.md` — Expand-contract patterns avancés, Prisma migrate, Flyway, migration de données massives, blue-green DB
- `references/performance.md` — EXPLAIN ANALYZE en profondeur, index avancés (BRIN, SP-GiST), autovacuum, pg_stat_statements
- `references/advanced-patterns.md` — Partitioning avancé, sharding avec Citus, TimescaleDB, Neo4j Cypher, full-text search
- `references/case-studies.md` — 4 cas : migration zéro downtime 10M lignes, lenteur résolue par index, RLS multi-tenant, TimescaleDB IoT
