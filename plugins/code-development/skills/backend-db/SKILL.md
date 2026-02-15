---
name: backend-db
description: This skill should be used when the user asks about "database design", "SQL optimization", "PostgreSQL", "Supabase", "ORM", "Prisma", "Drizzle", "API development", "REST API", "GraphQL", "database migrations", "indexing", "query optimization", "NoSQL", "Redis", "vector databases", "conception de base de données", "optimisation SQL", "développement API", "migrations de base de données", "optimisation de requêtes", "bases de données vectorielles", "MySQL", "MongoDB", "DynamoDB", "Elasticsearch", "database schema", "schéma de base de données", "normalization", "normalisation", "denormalization", "N+1 query", "connection pooling", "database replication", "réplication", "sharding", "partitioning", "stored procedures", "triggers", "materialized views", "tRPC", "Hono", "Express", "Fastify", "NestJS", "serverless functions", or needs guidance on backend development and database management.
version: 1.2.0
last_updated: 2026-02
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
4. Configurer le connection pooling (PgBouncer/Supavisor) : pool_size = nb_cores * 2 + nb_disks pour PostgreSQL, max 100 connexions par pool, mode transaction pour les workloads web.
5. Mettre en place le monitoring des requetes avec `pg_stat_statements`.

### Phase 4 : Production & Maintenance

1. Activer les backups automatiques (Point-in-Time Recovery).
2. Configurer les alertes sur les metriques cles (connections actives, cache hit ratio, slow queries).
3. Mettre en place le database branching pour les environnements de preview (Neon, Supabase Branching).
4. Planifier les maintenances (VACUUM, REINDEX, rafraichissement des vues materialisees).
5. Documenter les runbooks pour les operations courantes (rollback migration, scaling, failover).



## Modèle de maturité

### Niveau 1 — Ad-hoc
- Schéma de base de données conçu sans modélisation préalable, pas de conventions de nommage
- Requêtes SQL écrites en concaténation de chaînes, pas d'ORM ni de query builder type-safe
- Migrations manuelles en production, pas de versionning du schéma
- **Indicateurs** : query p95 latency > 1s, migration success rate < 80%

### Niveau 2 — Structuré
- Schéma normalisé (3NF) avec diagramme ERD documenté, conventions de nommage établies
- ORM type-safe configuré (Prisma ou Drizzle), requêtes paramétrées systématiques
- Migrations versionnées et appliquées via CI/CD, backups automatiques quotidiens
- **Indicateurs** : query p95 latency < 500ms, migration success rate > 95%, index coverage > 50%

### Niveau 3 — Optimisé
- Index stratégiques basés sur EXPLAIN ANALYZE, vues matérialisées pour les dashboards
- Connection pooling configuré (PgBouncer/Supavisor), caching Redis pour les données chaudes
- RLS actif sur les tables multi-tenant, tests de migration sur copies de production
- **Indicateurs** : query p95 latency < 200ms, migration success rate > 99%, connection pool utilization < 80%

### Niveau 4 — Scalable
- Partitionnement et read replicas déployés, monitoring pg_stat_statements actif
- CQRS appliqué sur les cas justifiés, pagination par curseur généralisée
- Database branching pour les environnements de preview, observabilité des requêtes intégrée
- **Indicateurs** : query p95 latency < 100ms, index coverage > 80%, zero downtime migrations

### Niveau 5 — Cloud-native
- Architecture multi-base adaptée aux cas d'usage (relationnelle, vectorielle, cache, time-series)
- Auto-scaling serverless (Neon, Supabase), edge databases pour la latence minimale
- Chaos testing sur la couche données, capacity planning automatisé, DR testé trimestriellement
- **Indicateurs** : query p95 latency < 50ms, migration success rate 100%, connection pool utilization optimisée dynamiquement

## Rythme opérationnel

| Cadence | Activité | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Hebdomadaire** | Revue des slow queries (pg_stat_statements, EXPLAIN ANALYZE) | DBA / Tech Lead | Top 10 requêtes lentes + plan d'optimisation |
| **Hebdomadaire** | Vérification des backups et tests de restauration aléatoires | DBA / SRE | Rapport backup + test restore validé |
| **Mensuel** | Optimisation des index (index inutilisés, index manquants, bloat) | DBA / Backend Engineer | Rapport indexation + actions correctives |
| **Mensuel** | Revue des métriques de performance (connection pool, cache hit ratio, latence) | DBA / Tech Lead | Dashboard performance à jour |
| **Trimestriel** | Revue du schéma (normalisation, cohérence, évolutions nécessaires) | Architecte / DBA | Schema review documenté + migrations planifiées |
| **Trimestriel** | Test de disaster recovery (failover, restauration point-in-time) | SRE / DBA | Rapport DR + temps de restauration mesuré |
| **Annuel** | Revue de l'architecture base de données (choix technologiques, scaling, coûts) | Architecte / Engineering Manager | Plan d'évolution architecture données |

## State of the Art (2025-2026)

Le backend et les bases de données évoluent vers l'IA et la simplification :

- **Vector databases** : Pinecone, Weaviate, pgvector deviennent essentiels pour les applications IA (RAG, semantic search, recommendations).
- **Serverless databases** : Neon, PlanetScale, Supabase offrent du PostgreSQL serverless avec scaling automatique et branching de schéma.
- **Edge databases** : Turso (libSQL), Cloudflare D1 et DynamoDB Global Tables rapprochent les données des utilisateurs.
- **TypeScript-first ORMs** : Drizzle ORM et Prisma dominent l'écosystème TypeScript avec des requêtes type-safe et des migrations déclaratives.
- **Realtime-first** : Les architectures intègrent nativement le temps réel (Supabase Realtime, Convex, Electric SQL) plutôt que de l'ajouter après coup.

## Template actionnable

### Checklist de migration de base de données

| Étape | Action | Vérifié |
|---|---|---|
| **Pré-migration** | Backup complet de la base | ☐ |
| **Pré-migration** | Tester la migration sur staging | ☐ |
| **Pré-migration** | Vérifier la rétrocompatibilité du schéma | ☐ |
| **Pré-migration** | Estimer le downtime si applicable | ☐ |
| **Migration** | Exécuter la migration | ☐ |
| **Migration** | Vérifier l'intégrité des données | ☐ |
| **Post-migration** | Valider les index et contraintes | ☐ |
| **Post-migration** | Tester les requêtes critiques | ☐ |
| **Post-migration** | Monitorer les performances | ☐ |
| **Rollback** | Plan de rollback documenté et testé | ☐ |

## Prompts types

- "Comment concevoir un schéma PostgreSQL pour une app multi-tenant ?"
- "Aide-moi à optimiser cette requête SQL lente"
- "Prisma vs Drizzle : lequel choisir pour mon projet ?"
- "Comment structurer mes migrations de base de données ?"
- "Propose une stratégie d'indexation pour améliorer les performances"
- "Comment implémenter une API GraphQL avec des relations complexes ?"
- "Aide-moi à configurer Supabase avec Row Level Security"

## Limites et Red Flags

Ce skill n'est PAS adapté pour :
- ❌ Décisions d'architecture système (monolithe vs microservices, event-driven design) → Utiliser plutôt : `code-development:architecture`
- ❌ Pipelines de données ETL/ELT, data warehousing ou orchestration dbt → Utiliser plutôt : `data-bi:data-engineering`
- ❌ Authentification utilisateur, OAuth, gestion de sessions ou RBAC applicatif → Utiliser plutôt : `code-development:auth-security`
- ❌ Design d'interface frontend, formulaires ou composants UI → Utiliser plutôt : `code-development:ui-ux`
- ❌ Intégration de paiements Stripe, webhooks de facturation ou conformité PCI → Utiliser plutôt : `code-development:payment-stripe`

Signaux d'alerte en cours d'utilisation :
- ⚠️ Des requêtes SELECT * sont présentes dans le code de production → spécifier les colonnes nécessaires pour réduire le transfert et exploiter les index couvrants
- ⚠️ Les migrations sont appliquées manuellement en production sans fichier versionné → toujours passer par des fichiers de migration versionnés et testés sur staging
- ⚠️ Le schema est en 1NF avec des colonnes JSON fourre-tout → normaliser en 3NF d'abord, puis dénormaliser intentionnellement selon les access patterns mesurés
- ⚠️ Pas de connection pooler en production → chaque connexion directe coûte ~5MB de RAM PostgreSQL ; utiliser PgBouncer ou Supavisor systématiquement

## Skills connexes

| Skill | Lien |
|---|---|
| Architecture | `code-development:architecture` — Design système et choix d'architecture |
| DevOps | `code-development:devops` — Déploiement et migrations en production |
| Data Engineering | `data-bi:data-engineering` — Pipelines de données et intégration |
| Auth Security | `code-development:auth-security` — Sécurité des données et accès |
| Payment Stripe | `code-development:payment-stripe` — APIs de paiement et webhooks |

## Glossaire

| Terme | Définition |
|-------|-----------|
| **ORM (Object-Relational Mapping)** | Couche d'abstraction mappant les tables de base de données vers des objets du langage de programmation, simplifiant l'accès aux données (ex. Prisma, Drizzle). |
| **N+1 Query** | Anti-pattern où une requête initiale charge une liste, puis une requête supplémentaire est exécutée pour chaque élément, causant une explosion du nombre de requêtes. |
| **ACID (Atomicity, Consistency, Isolation, Durability)** | Ensemble de propriétés garantissant la fiabilité des transactions de base de données : atomicité, cohérence, isolation et durabilité. |
| **CAP Theorem** | Théorème stipulant qu'un système distribué ne peut garantir simultanément que deux des trois propriétés : Cohérence, Disponibilité, Tolérance au partitionnement. |
| **Index (B-tree, GIN, GiST)** | Structure de données accélérant les recherches en base. B-tree pour les comparaisons classiques, GIN pour le full-text/JSONB, GiST pour les données spatiales. |
| **Migration** | Fichier versionné décrivant une modification de schéma de base de données (ajout de table, colonne, index), appliqué de manière reproductible et réversible. |
| **Row-Level Security (RLS)** | Mécanisme PostgreSQL appliquant des politiques de sécurité au niveau de chaque ligne, filtrant automatiquement les données selon l'utilisateur connecté. |
| **Connection Pooling** | Technique maintenant un pool de connexions réutilisables vers la base de données pour éviter le coût d'établissement de nouvelles connexions à chaque requête. |
| **Materialized View** | Vue dont les résultats sont stockés physiquement et rafraîchis périodiquement, optimisant les requêtes coûteuses fréquemment exécutées (dashboards, rapports). |
| **CTE (Common Table Expression)** | Sous-requête nommée définie avec `WITH`, améliorant la lisibilité des requêtes complexes et permettant des requêtes récursives. |
| **Deadlock** | Situation où deux transactions se bloquent mutuellement en attendant chacune la libération d'un verrou détenu par l'autre, nécessitant l'annulation d'une des deux. |
| **Sharding** | Technique de partitionnement horizontal distribuant les données sur plusieurs instances de base de données selon une clé de partition pour gérer la montée en charge. |
| **Read Replica** | Copie en lecture seule de la base de données principale, permettant de répartir la charge des requêtes de lecture et d'améliorer les performances. |
| **Prisma** | ORM TypeScript moderne avec un schéma déclaratif, une excellente DX, la génération de types automatique et des migrations intégrées. |
| **Drizzle** | ORM TypeScript léger, type-safe et proche du SQL, compatible avec les runtimes edge et serverless, avec des migrations déclaratives. |
| **Edge Function** | Fonction serverless exécutée au plus proche de l'utilisateur (edge network), offrant des latences très faibles (< 50ms cold start). |
| **Vector Database** | Base de données spécialisée dans le stockage et la recherche de vecteurs d'embeddings pour la recherche sémantique, le RAG et les recommandations IA. |

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[SQL & PostgreSQL Avance](./references/sql-postgresql.md)** : Window functions, CTEs, requetes recursives, JSONB, extensions (pgvector, PostGIS, pg_cron), strategies d'indexation avancees (B-tree, GIN, GiST, BRIN, partial, covering), optimisation de requetes avec EXPLAIN ANALYZE, partitionnement.

- **[Conception de Base de Donnees](./references/database-design.md)** : Normalisation (3NF, BCNF), denormalisation intentionnelle, patterns de schema design, modelisation par cas d'usage, choix de la bonne base de donnees (relationnelle vs document vs cle-valeur vs graphe vs vecteur vs time-series), gestion des migrations.

- **[Developpement d'API](./references/api-development.md)** : REST API design (nommage des ressources, versioning, pagination, filtrage, gestion d'erreurs), GraphQL (schema design, resolvers, DataLoader, federation), gRPC, WebSockets & SSE, rate limiting, documentation OpenAPI/Swagger.

- **[Stack Supabase](./references/supabase-stack.md)** : Supabase Auth (providers, integration RLS), Supabase Storage (policies, transformations), Supabase Realtime (broadcast, presence, postgres changes), Edge Functions (Deno), PostgREST, CLI & developpement local, webhooks & triggers.

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.