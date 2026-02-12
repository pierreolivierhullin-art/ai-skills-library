---
name: backend-db
description: This skill should be used when the user asks about "database design", "SQL optimization", "PostgreSQL", "Supabase", "ORM", "Prisma", "Drizzle", "API development", "REST API", "GraphQL", "database migrations", "indexing", "query optimization", "NoSQL", "Redis", "vector databases", "conception de base de données", "optimisation SQL", "développement API", "migrations de base de données", "optimisation de requêtes", "bases de données vectorielles", "MySQL", "MongoDB", "DynamoDB", "Elasticsearch", "database schema", "schéma de base de données", "normalization", "normalisation", "denormalization", "N+1 query", "connection pooling", "database replication", "réplication", "sharding", "partitioning", "stored procedures", "triggers", "materialized views", "tRPC", "Hono", "Express", "Fastify", "NestJS", "serverless functions", or needs guidance on backend development and database management.
version: 1.0.0
---

# Backend Development & Database Management

## Overview

Cette skill couvre l'ensemble du spectre backend moderne : conception de bases de donnees, optimisation SQL avancee, developpement d'API, et integration de stacks modernes comme Supabase. Elle fournit des guidelines de niveau expert pour construire des systemes backend performants, securises et maintenables, en incorporant les meilleures pratiques de 2024-2026 incluant les bases vectorielles pour l'IA, les edge functions, le database branching, et les ORM type-safe de nouvelle generation.

## When This Skill Applies

Activer cette skill lorsque l'utilisateur :
- Concoive un schema de base de donnees ou demande des conseils sur la normalisation/denormalisation
- Ecrit ou optimise des requetes SQL (PostgreSQL, MySQL, SQLite)
- Configure ou utilise un ORM (Prisma, Drizzle, TypeORM, Kysely)
- Developpe des API REST, GraphQL ou gRPC
- Travaille avec Supabase (Auth, Storage, Realtime, Edge Functions, RLS)
- Gere des migrations de base de donnees
- Implemente du caching avec Redis ou Memcached
- Travaille avec des bases NoSQL (MongoDB, DynamoDB, Firestore)
- Implemente des recherches vectorielles avec pgvector ou des bases vectorielles dediees
- Optimise les performances de requetes (indexation, EXPLAIN ANALYZE, query plans)
- Met en place du connection pooling (PgBouncer, Supavisor)
- Gere la pagination, le filtrage ou le tri cote serveur

## Core Principles

### 1. Type Safety End-to-End
Privilegier les ORM et outils qui propagent les types de la base de donnees jusqu'au frontend. Drizzle ORM et Prisma offrent cette garantie. Ne jamais construire de requetes par concatenation de chaines. Utiliser des query builders type-safe ou des requetes parametrees systematiquement.

### 2. Defense in Depth pour les Donnees
Appliquer la securite a chaque couche : Row Level Security (RLS) au niveau PostgreSQL, validation au niveau API, sanitization des inputs. Ne jamais se reposer sur une seule couche de securite. Considerer la base de donnees comme la derniere ligne de defense, pas la premiere.

### 3. Performance by Design
Concevoir le schema et les index en fonction des patterns d'acces (access patterns), pas uniquement du modele de donnees. Mesurer avant d'optimiser avec EXPLAIN ANALYZE. Privilegier les index couvrants (covering indexes) pour les requetes critiques. Anticiper la volumetrie des la conception.

### 4. Migrations Reproductibles et Reversibles
Chaque migration doit etre idempotente, versionee, et accompagnee d'un plan de rollback. Utiliser des outils de migration declaratifs (Drizzle Kit, Prisma Migrate) et tester les migrations sur des copies de production. Adopter le database branching pour les environnements de preview.

### 5. API Contract First
Definir le contrat d'API avant l'implementation. Utiliser OpenAPI/Swagger pour REST, le schema SDL pour GraphQL. Versionner les API et maintenir la retrocompatibilite. Documenter les codes d'erreur, les limites de rate, et les formats de pagination.

## Key Frameworks & Methods

### ORM & Query Builders (Tier moderne)

| Outil | Forces | Cas d'usage ideal |
|-------|--------|-------------------|
| **Drizzle ORM** | Type-safe, SQL-like, leger, migrations declaratives, support edge runtime | Projets greenfield, serverless, edge computing |
| **Prisma** | DX excellente, schema declaratif, introspection, Prisma Accelerate pour le caching | Projets d'equipe, prototypage rapide, stacks fullstack |
| **Kysely** | Query builder type-safe pur, sans generation de code | Requetes complexes, migration depuis du SQL brut |
| **TypeORM** | Patterns Active Record/Data Mapper, decorateurs | Projets NestJS existants (eviter pour les nouveaux projets) |

### Bases de Donnees

| Type | Technologie | Quand l'utiliser |
|------|-------------|-----------------|
| **Relationnelle** | PostgreSQL 16/17 | Donnees structurees, transactions ACID, cas general |
| **Document** | MongoDB 7+ | Schemas tres variables, prototypage rapide, donnees semi-structurees |
| **Cle-valeur** | Redis 7+ / Valkey | Cache, sessions, queues, rate limiting, leaderboards |
| **Vectorielle** | pgvector / Pinecone / Qdrant | Recherche semantique, RAG, recommandations IA |
| **Time-series** | TimescaleDB / InfluxDB | IoT, metriques, logs, donnees temporelles |
| **Graphe** | Neo4j / Apache AGE | Relations complexes, reseaux sociaux, graphes de connaissances |

### Stack Supabase

Supabase est le BaaS open-source de reference pour PostgreSQL. Utiliser ses composants :
- **Auth** : Authentification multi-provider avec integration RLS native
- **PostgREST** : API REST auto-generee depuis le schema PostgreSQL
- **Realtime** : Broadcast, Presence, et ecoute des changements Postgres via WebSockets
- **Storage** : Stockage objets avec policies RLS et transformations d'images
- **Edge Functions** : Functions serverless Deno deployees au edge (< 50ms cold start)
- **Supavisor** : Connection pooler natif remplacant PgBouncer

## Decision Guide

### Choisir sa base de donnees

```
Donnees structurees avec relations ?
  OUI --> PostgreSQL (defaut) ou MySQL
    Besoin de recherche vectorielle ?
      OUI --> PostgreSQL + pgvector
    Besoin de donnees geospatiales ?
      OUI --> PostgreSQL + PostGIS
    Besoin de time-series ?
      OUI --> TimescaleDB (extension PostgreSQL)

  NON --> Schema tres variable ?
    OUI --> MongoDB ou Firestore
    NON --> Acces cle-valeur rapide ?
      OUI --> Redis / Valkey
      NON --> Relations complexes (graphe) ?
        OUI --> Neo4j ou Apache AGE (extension PostgreSQL)
```

### Choisir son ORM

```
Projet TypeScript/JavaScript ?
  OUI --> Environnement edge/serverless ?
    OUI --> Drizzle ORM (leger, compatible edge)
    NON --> Equipe junior ou prototypage ?
      OUI --> Prisma (meilleure DX, documentation)
      NON --> Requetes SQL complexes ?
        OUI --> Drizzle ORM ou Kysely
        NON --> Prisma ou Drizzle
  NON --> Python ?
    OUI --> SQLAlchemy 2.0+ (async support)
  NON --> Go ?
    OUI --> sqlc (generation de code depuis SQL) ou GORM
```

### Choisir son style d'API

```
API publique avec documentation ?
  OUI --> REST + OpenAPI
API avec des donnees tres connectees ou des besoins flexibles ?
  OUI --> GraphQL
Communication inter-services haute performance ?
  OUI --> gRPC
Temps reel bidirectionnel ?
  OUI --> WebSockets (ou Supabase Realtime)
Flux de donnees unidirectionnel serveur -> client ?
  OUI --> Server-Sent Events (SSE)
```

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Repository Pattern** : Abstraire l'acces aux donnees derriere une interface. Faciliter les tests et le changement d'ORM.
- **Unit of Work** : Grouper les operations de base de donnees dans une transaction unique. Garantir la coherence.
- **CQRS simplifie** : Separer les modeles de lecture (vues optimisees, index dedies) des modeles d'ecriture (schema normalise). Appliquer uniquement quand la complexite le justifie.
- **Database-per-service** : En microservices, chaque service possede sa base. Communiquer par events, jamais par jointures cross-service.
- **Pagination par curseur** : Privilegier la pagination par curseur (cursor-based) sur la pagination par offset pour les grands datasets. Plus performante et stable.
- **Materialized Views** : Utiliser des vues materialisees pour les dashboards et rapports. Rafraichir periodiquement avec `REFRESH MATERIALIZED VIEW CONCURRENTLY`.
- **Connection Pooling** : Toujours utiliser un pooler (PgBouncer, Supavisor, Prisma Accelerate) en production. Ne jamais exposer la base directement.

### Anti-patterns a eviter

- **N+1 Queries** : Charger une liste puis faire une requete par element. Utiliser les jointures, `include` (Prisma), ou `with` (Drizzle) pour le eager loading.
- **SELECT \*** : Ne jamais selectionner toutes les colonnes. Specifier les colonnes necessaires pour reduire le transfert et exploiter les index couvrants.
- **Indexes sur tout** : Chaque index a un cout en ecriture et en stockage. Indexer uniquement les colonnes utilisees dans les WHERE, JOIN, ORDER BY des requetes frequentes.
- **Stocker des fichiers en base** : Utiliser un object storage (S3, Supabase Storage, R2) et stocker uniquement l'URL ou la reference en base.
- **Ignorer les transactions** : Toute operation multi-tables doit etre dans une transaction. Utiliser `$transaction` (Prisma) ou `db.transaction()` (Drizzle).
- **RLS desactive en production** : Ne jamais desactiver Row Level Security sur les tables accessibles depuis le client. Toujours definir des policies explicites.
- **Migrations manuelles** : Ne jamais modifier le schema de production manuellement. Toujours passer par des fichiers de migration versiones.

## Implementation Workflow

### Phase 1 : Conception

1. Definir les entites, relations et access patterns avec un diagramme ERD.
2. Choisir la base de donnees adaptee au cas d'usage (voir Decision Guide).
3. Concevoir le schema en 3NF puis denormaliser intentionnellement si les patterns d'acces le necessitent.
4. Definir les index initiaux sur les cles etrangeres et les colonnes de filtrage frequentes.
5. Rediger le contrat d'API (OpenAPI spec ou schema GraphQL SDL).

### Phase 2 : Implementation

1. Configurer l'ORM et generer le schema initial (Drizzle `schema.ts` ou Prisma `schema.prisma`).
2. Creer la premiere migration et l'appliquer en local.
3. Implementer la couche repository/service avec les requetes type-safe.
4. Mettre en place les Row Level Security policies si utilisation de Supabase ou acces client direct.
5. Implementer les endpoints API avec validation des inputs (Zod, Valibot).
6. Ajouter la pagination par curseur sur les endpoints de liste.

### Phase 3 : Optimisation

1. Analyser les requetes lentes avec `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)`.
2. Ajouter des index cibles sur les colonnes identifiees (voir sql-postgresql.md pour les strategies).
3. Implementer le caching Redis pour les donnees frequemment accedees et rarement modifiees.
4. Configurer le connection pooling (PgBouncer/Supavisor) avec des limites appropriees.
5. Mettre en place le monitoring des requetes avec `pg_stat_statements`.

### Phase 4 : Production & Maintenance

1. Activer les backups automatiques (Point-in-Time Recovery).
2. Configurer les alertes sur les metriques cles (connections actives, cache hit ratio, slow queries).
3. Mettre en place le database branching pour les environnements de preview (Neon, Supabase Branching).
4. Planifier les maintenances (VACUUM, REINDEX, rafraichissement des vues materialisees).
5. Documenter les runbooks pour les operations courantes (rollback migration, scaling, failover).

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[SQL & PostgreSQL Avance](./references/sql-postgresql.md)** : Window functions, CTEs, requetes recursives, JSONB, extensions (pgvector, PostGIS, pg_cron), strategies d'indexation avancees (B-tree, GIN, GiST, BRIN, partial, covering), optimisation de requetes avec EXPLAIN ANALYZE, partitionnement.

- **[Conception de Base de Donnees](./references/database-design.md)** : Normalisation (3NF, BCNF), denormalisation intentionnelle, patterns de schema design, modelisation par cas d'usage, choix de la bonne base de donnees (relationnelle vs document vs cle-valeur vs graphe vs vecteur vs time-series), gestion des migrations.

- **[Developpement d'API](./references/api-development.md)** : REST API design (nommage des ressources, versioning, pagination, filtrage, gestion d'erreurs), GraphQL (schema design, resolvers, DataLoader, federation), gRPC, WebSockets & SSE, rate limiting, documentation OpenAPI/Swagger.

- **[Stack Supabase](./references/supabase-stack.md)** : Supabase Auth (providers, integration RLS), Supabase Storage (policies, transformations), Supabase Realtime (broadcast, presence, postgres changes), Edge Functions (Deno), PostgREST, CLI & developpement local, webhooks & triggers.
