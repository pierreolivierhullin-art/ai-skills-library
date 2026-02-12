# Database Design Reference

> Reference detaillee pour la conception de bases de donnees. Couvre la normalisation, la denormalisation intentionnelle, les patterns de schema design, la modelisation par cas d'usage, le choix de la bonne technologie de base de donnees, et la gestion des migrations.

---

## Normalization

### Les formes normales essentielles

Appliquer la normalisation pour eliminer la redondance et garantir l'integrite des donnees. Comprendre les formes normales pour savoir quand et comment les appliquer ou les transgresser.

#### Premiere Forme Normale (1NF)
- Chaque colonne contient une valeur atomique (pas de listes, pas de groupes repetitifs)
- Chaque ligne est identifiable de maniere unique (cle primaire)

```sql
-- VIOLATION 1NF : tags sous forme de chaine separee par des virgules
CREATE TABLE articles_bad (
    id SERIAL PRIMARY KEY,
    title TEXT,
    tags TEXT  -- "javascript,react,frontend" -> NON
);

-- CORRECT 1NF : table de liaison ou ARRAY/JSONB typee
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL
);
CREATE TABLE article_tags (
    article_id INT REFERENCES articles(id),
    tag TEXT NOT NULL,
    PRIMARY KEY (article_id, tag)
);

-- Alternative moderne avec PostgreSQL ARRAY (acceptable si requetes simples)
CREATE TABLE articles_v2 (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    tags TEXT[] NOT NULL DEFAULT '{}'
);
CREATE INDEX idx_articles_tags ON articles_v2 USING GIN (tags);
```

#### Deuxieme Forme Normale (2NF)
- Respecter 1NF
- Chaque attribut non-cle depend de la totalite de la cle primaire (pas de dependance partielle)

```sql
-- VIOLATION 2NF : student_name depend uniquement de student_id, pas du couple (student_id, course_id)
CREATE TABLE enrollments_bad (
    student_id INT,
    course_id INT,
    student_name TEXT,     -- depend seulement de student_id
    grade CHAR(1),
    PRIMARY KEY (student_id, course_id)
);

-- CORRECT 2NF : extraire dans une table separee
CREATE TABLE students (
    id INT PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE enrollments (
    student_id INT REFERENCES students(id),
    course_id INT REFERENCES courses(id),
    grade CHAR(1),
    PRIMARY KEY (student_id, course_id)
);
```

#### Troisieme Forme Normale (3NF)
- Respecter 2NF
- Aucun attribut non-cle ne depend transitivement d'un autre attribut non-cle

```sql
-- VIOLATION 3NF : city et country dependent de zip_code (dependance transitive)
CREATE TABLE customers_bad (
    id SERIAL PRIMARY KEY,
    name TEXT,
    zip_code TEXT,
    city TEXT,      -- depend de zip_code, pas de id directement
    country TEXT    -- idem
);

-- CORRECT 3NF
CREATE TABLE locations (
    zip_code TEXT PRIMARY KEY,
    city TEXT NOT NULL,
    country TEXT NOT NULL
);
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    zip_code TEXT REFERENCES locations(zip_code)
);
```

#### Boyce-Codd Normal Form (BCNF)
- Version plus stricte de 3NF
- Chaque determinant est une cle candidate
- S'applique lorsqu'il y a des cles candidates multiples qui se chevauchent

```sql
-- Violation BCNF : un professeur enseigne un seul sujet,
-- mais un sujet peut avoir plusieurs professeurs
-- (professor -> subject, mais professor n'est pas une cle candidate)
CREATE TABLE teachings_bad (
    student_id INT,
    subject TEXT,
    professor TEXT,  -- professor determine subject, mais n'est pas cle
    PRIMARY KEY (student_id, subject)
);

-- CORRECT BCNF : decomposer
CREATE TABLE professor_subjects (
    professor TEXT PRIMARY KEY,
    subject TEXT NOT NULL
);
CREATE TABLE student_professors (
    student_id INT,
    professor TEXT REFERENCES professor_subjects(professor),
    PRIMARY KEY (student_id, professor)
);
```

### Denormalisation Intentionnelle

Denormaliser consciemment pour la performance, jamais par negligence. Toujours documenter la raison et mettre en place des mecanismes de coherence.

#### Quand denormaliser

| Situation | Technique | Mecanisme de coherence |
|-----------|-----------|----------------------|
| Requetes de lecture critiques avec jointures couteuses | Colonnes redondantes | Trigger ou application-level sync |
| Compteurs d'agregation frequemment lus | Compteur materialise | Trigger `ON INSERT/DELETE` |
| Donnees historiques immuables | Snapshot denormalise | Ecriture unique, pas de mise a jour |
| Recherche full-text sur donnees jointes | Colonne `tsvector` composite | Trigger de mise a jour |
| Cache de valeurs calculees | Vue materialisee ou colonne calculee | Rafraichissement periodique |

```sql
-- Pattern : compteur denormalise avec trigger
ALTER TABLE posts ADD COLUMN comment_count INT NOT NULL DEFAULT 0;

CREATE OR REPLACE FUNCTION update_comment_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE posts SET comment_count = comment_count + 1 WHERE id = NEW.post_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE posts SET comment_count = comment_count - 1 WHERE id = OLD.post_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_comment_count
    AFTER INSERT OR DELETE ON comments
    FOR EACH ROW EXECUTE FUNCTION update_comment_count();
```

```sql
-- Pattern : snapshot denormalise pour les factures (donnees historiques immuables)
CREATE TABLE invoices (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT REFERENCES customers(id),
    -- Snapshot : copie des donnees client au moment de la facturation
    customer_name TEXT NOT NULL,
    customer_address TEXT NOT NULL,
    customer_vat_number TEXT,
    -- Donnees de facturation
    total_amount NUMERIC(12,2) NOT NULL,
    issued_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- Justification : le nom/adresse du client peut changer, mais la facture doit refleter
-- les informations au moment de l'emission.
```

## Schema Design Patterns

### Soft Delete

Privilegier le soft delete pour les donnees reglementairement sensibles ou les cas ou l'annulation doit etre possible.

```sql
CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    deleted_at TIMESTAMPTZ,  -- NULL = actif, timestamp = supprime
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index unique qui ne s'applique qu'aux utilisateurs actifs
CREATE UNIQUE INDEX idx_users_email_active ON users (email) WHERE deleted_at IS NULL;

-- Index partiel pour exclure les supprimes des requetes courantes
CREATE INDEX idx_users_active ON users (created_at DESC) WHERE deleted_at IS NULL;

-- Vue pour simplifier les requetes
CREATE VIEW active_users AS SELECT * FROM users WHERE deleted_at IS NULL;
```

### Polymorphisme en base de donnees

#### Pattern : Single Table Inheritance (STI)

```sql
-- Toutes les notifications dans une seule table avec un discriminateur
CREATE TABLE notifications (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type TEXT NOT NULL CHECK (type IN ('email', 'sms', 'push', 'in_app')),
    recipient_id BIGINT NOT NULL REFERENCES users(id),
    title TEXT NOT NULL,
    body TEXT,
    -- Champs specifiques par type (nullable)
    email_address TEXT,         -- pour type = 'email'
    phone_number TEXT,          -- pour type = 'sms'
    device_token TEXT,          -- pour type = 'push'
    -- Ou mieux : utiliser JSONB pour les champs specifiques
    metadata JSONB NOT NULL DEFAULT '{}',
    sent_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

#### Pattern : Table par type avec table de base

```sql
-- Table de base commune
CREATE TABLE payments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type TEXT NOT NULL CHECK (type IN ('card', 'bank_transfer', 'crypto')),
    amount NUMERIC(12,2) NOT NULL,
    currency TEXT NOT NULL DEFAULT 'EUR',
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tables specifiques
CREATE TABLE card_payments (
    payment_id BIGINT PRIMARY KEY REFERENCES payments(id),
    last_four TEXT NOT NULL,
    brand TEXT NOT NULL,
    stripe_payment_intent_id TEXT
);

CREATE TABLE bank_transfer_payments (
    payment_id BIGINT PRIMARY KEY REFERENCES payments(id),
    iban TEXT NOT NULL,
    bic TEXT,
    reference TEXT
);
```

### Multi-Tenancy

#### Schema-per-tenant (isolation forte)

```sql
-- Creer un schema par tenant
CREATE SCHEMA tenant_acme;
CREATE TABLE tenant_acme.users (...);
CREATE TABLE tenant_acme.orders (...);

-- Definir le search_path par connexion
SET search_path TO tenant_acme, public;
```

#### Row-Level Security (recommande avec Supabase)

```sql
-- Colonne tenant_id sur chaque table
CREATE TABLE orders (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    ...
);

-- RLS policy
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- Ou avec Supabase Auth
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = (auth.jwt() ->> 'tenant_id')::uuid);
```

### Audit Trail

```sql
-- Table d'audit generique
CREATE TABLE audit_log (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    table_name TEXT NOT NULL,
    record_id TEXT NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_data JSONB,
    new_data JSONB,
    changed_by UUID,
    changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Trigger d'audit generique
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, record_id, action, old_data, new_data, changed_by)
    VALUES (
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id)::text,
        TG_OP,
        CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN to_jsonb(OLD) END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN to_jsonb(NEW) END,
        current_setting('app.user_id', true)::uuid
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Appliquer sur les tables sensibles
CREATE TRIGGER audit_orders
    AFTER INSERT OR UPDATE OR DELETE ON orders
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
```

### Temporal Data (Slowly Changing Dimensions)

```sql
-- Type 2 : historique complet avec periodes de validite
CREATE TABLE product_prices (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES products(id),
    price NUMERIC(10,2) NOT NULL,
    valid_from TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_to TIMESTAMPTZ, -- NULL = prix actuel
    EXCLUDE USING gist (
        product_id WITH =,
        tstzrange(valid_from, valid_to) WITH &&
    ) -- Empeche les chevauchements de periodes pour un meme produit
);

-- Obtenir le prix actuel
SELECT price FROM product_prices
WHERE product_id = 42 AND valid_to IS NULL;

-- Obtenir le prix a une date donnee
SELECT price FROM product_prices
WHERE product_id = 42
  AND valid_from <= '2024-06-15'::timestamptz
  AND (valid_to IS NULL OR valid_to > '2024-06-15'::timestamptz);
```

## Choosing the Right Database

### Matrice de decision detaillee

| Critere | PostgreSQL | MongoDB | Redis | pgvector | TimescaleDB | Neo4j |
|---------|-----------|---------|-------|----------|-------------|-------|
| **Transactions ACID** | Oui (complet) | Oui (depuis 4.0) | Non | Oui (via PG) | Oui (via PG) | Oui |
| **Schema flexible** | JSONB | Natif | N/A | N/A | Non | Natif |
| **Scalabilite ecriture** | Verticale + replicas | Horizontale (sharding) | Horizontale | Verticale | Verticale + chunks | Verticale |
| **Latence lecture** | ~1-10ms | ~1-10ms | ~0.1ms | ~5-50ms | ~1-10ms | ~1-50ms |
| **Recherche vectorielle** | Extension | Atlas Search | Non | Natif | Non | Non |
| **Cout operationnel** | Moyen | Moyen-Eleve | Faible | Moyen | Moyen | Eleve |
| **Ecosysteme cloud** | Excellent | Excellent | Excellent | Via PG | Via PG | Moyen |

### PostgreSQL comme choix par defaut

Privilegier PostgreSQL comme base de donnees par defaut pour ces raisons :
- Extensions riches : pgvector (IA), PostGIS (geo), TimescaleDB (time-series), pg_cron (scheduling)
- JSONB performant pour les donnees semi-structurees
- Full-text search integre avec support multilingue
- Mature, fiable, excellent support communautaire
- Ajouter des bases specialisees uniquement quand PostgreSQL atteint ses limites

### Quand NE PAS utiliser PostgreSQL

- **Cache haute performance (< 1ms)** : utiliser Redis / Valkey
- **Sharding horizontal massif (> 10TB, ecriture distribuee)** : evaluer MongoDB, CockroachDB, ou YugabyteDB
- **Donnees de graphe avec traversals profonds (> 3 niveaux)** : evaluer Neo4j (Apache AGE convient pour les cas simples)
- **Streaming / event log** : utiliser Apache Kafka ou Redpanda
- **Stockage objet / fichiers** : utiliser S3, R2, ou Supabase Storage

## Migration Management

### Principes fondamentaux

1. **Immutabilite** : Ne jamais modifier une migration deja executee en production. Creer une nouvelle migration corrective.
2. **Idempotence** : Utiliser `IF NOT EXISTS`, `IF EXISTS` pour rendre les migrations re-executables sans erreur.
3. **Backward compatibility** : Chaque migration doit etre compatible avec la version N-1 du code (deploiement zero-downtime).
4. **Reversibilite** : Chaque migration doit avoir un plan de rollback documente (meme si le down est rarement utilise).

### Zero-Downtime Migration Patterns

#### Ajouter une colonne

```sql
-- SAFE : Ajouter une colonne nullable (ne bloque pas)
ALTER TABLE users ADD COLUMN phone TEXT;

-- SAFE : Ajouter une colonne avec DEFAULT (PostgreSQL 11+, ne reecrit pas la table)
ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'active';

-- UNSAFE : Ajouter une contrainte NOT NULL sans default sur une table existante
-- ALTER TABLE users ADD COLUMN phone TEXT NOT NULL;  -- BLOQUE ET ECHOUE
```

#### Renommer une colonne (zero-downtime)

Proceder en 4 etapes deployees separement :

```sql
-- Migration 1 : Ajouter la nouvelle colonne
ALTER TABLE users ADD COLUMN full_name TEXT;

-- Migration 2 : Backfill (en batches pour les grandes tables)
UPDATE users SET full_name = name WHERE full_name IS NULL;
-- Ajouter un trigger pour synchroniser pendant la transition
CREATE OR REPLACE FUNCTION sync_name_columns()
RETURNS TRIGGER AS $$
BEGIN
    NEW.full_name := NEW.name;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER sync_names BEFORE INSERT OR UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION sync_name_columns();

-- Migration 3 : Le code utilise maintenant full_name, supprimer le trigger
DROP TRIGGER sync_names ON users;

-- Migration 4 : Supprimer l'ancienne colonne
ALTER TABLE users DROP COLUMN name;
```

#### Ajouter un index sans bloquer

```sql
-- TOUJOURS utiliser CONCURRENTLY pour les index en production
CREATE INDEX CONCURRENTLY idx_orders_customer ON orders (customer_id);

-- Note : CREATE INDEX CONCURRENTLY ne peut pas s'executer dans une transaction
-- Configurer l'outil de migration pour executer hors transaction
```

### Outils de migration recommandes

| Outil | Approche | Ecosysteme |
|-------|----------|------------|
| **Drizzle Kit** | Declaratif (diff du schema TypeScript) | TypeScript, edge-compatible |
| **Prisma Migrate** | Declaratif (diff du schema Prisma) | TypeScript, fullstack |
| **golang-migrate** | Imperatif (fichiers SQL up/down) | Go, polyglotte |
| **Flyway** | Imperatif (fichiers SQL versiones) | JVM, entreprise |
| **Atlas** | Declaratif (HCL ou SQL) | Polyglotte, moderne |
| **sqitch** | Imperatif (SQL avec dependances) | Polyglotte, avance |

### Database Branching

Le database branching permet de creer des copies isolees de la base pour les environnements de preview, comme des branches Git.

#### Avec Neon

```bash
# Creer une branche depuis main pour une PR
neon branches create --name pr-123 --parent main

# Obtenir la connection string de la branche
neon connection-string pr-123

# Supprimer apres merge
neon branches delete pr-123
```

#### Avec Supabase Branching

Configurer dans `supabase/config.toml` et utiliser via les GitHub Actions. Chaque PR obtient un environnement Supabase complet (base + auth + storage) isole.

### Migration Checklist

Appliquer avant chaque migration en production :

1. Tester la migration sur une copie de production (dump recent)
2. Verifier la retrocompatibilite avec le code en cours d'execution
3. Estimer le temps d'execution sur le volume reel de donnees
4. Preparer le script de rollback
5. Planifier l'execution pendant les heures creuses si migration lourde
6. Verifier que `CREATE INDEX` utilise `CONCURRENTLY`
7. Verifier l'absence de `LOCK TABLE` ou d'`ALTER TABLE` bloquants sur les grandes tables
8. Monitorer les connexions actives et les locks pendant l'execution
9. Valider le resultat immediatement apres (count, sample queries)
10. Communiquer au sein de l'equipe avant et apres l'execution
