---
name: data-engineering
description: This skill should be used when the user asks about "data pipeline", "ETL", "ELT", "dbt", "data warehouse", "data lake", "data lakehouse", "Airflow", "Dagster", "streaming", "Kafka", "data orchestration", "Snowflake", "BigQuery", "data transformation", "data infrastructure", "pipeline de données", "entrepôt de données", "lac de données", "orchestration de données", "transformation de données", "infrastructure de données", "ingestion de données", "data ingestion", "batch processing", "traitement par lots", "stream processing", "traitement en temps réel", "real-time data", "données temps réel", "Apache Spark", "Flink", "Fivetran", "Airbyte", "Stitch", "CDC", "change data capture", "data partitioning", "data compaction", "Iceberg", "Delta Lake", "Parquet", "Avro", "schema evolution", "idempotency", "backfill", "data freshness", or needs guidance on data engineering, pipeline architecture, and data platform design.
version: 1.2.0
last_updated: 2026-02
---

# Data Engineering — Pipelines, Transformations, Orchestration & Data Infrastructure

## Overview

**FR** — Cette skill couvre les pratiques modernes de data engineering : conception de pipelines de donnees (ETL/ELT), architectures batch et streaming, transformation avec dbt, orchestration avec Airflow/Dagster/Prefect, et infrastructure de donnees (data warehouse, data lake, data lakehouse). L'objectif est de construire des plateformes de donnees fiables, scalables et economiques — de l'ingestion brute a la couche de consommation analytique. Les recommandations sont alignees avec les meilleures pratiques 2024-2026, incluant l'architecture medallion, les formats de table ouverts (Iceberg, Delta Lake), le streaming unifie, et l'observabilite des donnees.

**EN** — This skill covers modern data engineering practices: data pipeline design (ETL/ELT), batch and streaming architectures, transformation with dbt, orchestration with Airflow/Dagster/Prefect, and data infrastructure (data warehouse, data lake, data lakehouse). The goal is to build reliable, scalable, and cost-efficient data platforms — from raw ingestion to the analytical consumption layer. Recommendations are aligned with 2024-2026 best practices, including medallion architecture, open table formats (Iceberg, Delta Lake), unified streaming, and data observability.

---

## When This Skill Applies

Activate this skill when the user:

- Designs or optimizes a data pipeline (ETL, ELT, batch, streaming, hybrid)
- Writes or reviews dbt models, tests, snapshots, or incremental logic
- Chooses or configures a data orchestrator (Airflow, Dagster, Prefect, Mage)
- Selects a data warehouse (BigQuery, Snowflake, Redshift, Databricks SQL)
- Implements a data lake or lakehouse (S3/GCS + Delta Lake, Iceberg, Hudi)
- Builds or evaluates a streaming pipeline (Kafka, Pub/Sub, Kinesis, Flink)
- Sets up data integration tools (Fivetran, Airbyte, Meltano, Sling)
- Implements schema evolution, idempotency, or exactly-once semantics
- Establishes data pipeline testing, CI/CD for data, or data observability
- Needs guidance on data platform cost management and optimization

---

## Core Principles

### 1. Design for Idempotency and Reproducibility
Build every pipeline so that re-running it with the same inputs produces the same outputs without side effects. Use MERGE/upsert patterns, partition-based overwrite, and deterministic transformations. Never assume a pipeline runs exactly once. / Construire chaque pipeline de sorte que la re-execution avec les memes entrees produise les memes sorties sans effets de bord. Utiliser les patrons MERGE/upsert, l'ecrasement par partition, et les transformations deterministes. Ne jamais supposer qu'un pipeline s'execute exactement une fois.

### 2. Separate Ingestion, Transformation, and Serving
Adopt a clear layered architecture. Ingest raw data faithfully (bronze), clean and conform it (silver), then build business-level aggregations (gold). Each layer has its own quality contracts, SLAs, and ownership. / Adopter une architecture en couches claire. Ingerer les donnees brutes fidelement (bronze), les nettoyer et les conformer (silver), puis construire les agregations metier (gold). Chaque couche a ses propres contrats de qualite, SLAs et ownership.

### 3. Schema Is a Contract, Not an Assumption
Treat schema changes as breaking changes. Implement schema validation at ingestion, enforce schema evolution policies (backward-compatible by default), and use schema registries for streaming. / Traiter les changements de schema comme des breaking changes. Implementer la validation de schema a l'ingestion, appliquer des politiques d'evolution de schema (retrocompatibles par defaut), et utiliser des registres de schemas pour le streaming.

### 4. Test Data Pipelines Like Software
Apply unit tests to transformations (ex: tester qu'une fonction de nettoyage retourne le resultat attendu sur 5 cas limites), integration tests to pipeline stages (ex: verifier que le pipeline bout-en-bout produit le bon nombre de lignes sur un jeu de donnees de reference), and data quality tests to outputs (ex: not_null, unique, accepted_values sur chaque modele dbt). Use dbt tests, Great Expectations, or Soda for assertion-based data validation. Never deploy an untested transformation to production.

### 5. Optimize for Cost and Performance Together
Choose the right processing paradigm (batch vs. micro-batch vs. streaming) based on latency requirements, not hype. Partition and cluster tables by the columns most used in WHERE and JOIN clauses. Use incremental processing over full refreshes — for a table de 100M lignes, passer de full refresh a incremental peut reduire les couts de 80-95%. Monitor compute costs per pipeline and set budgets with alerts at 80% consumption.

### 6. Observe Everything, Alert on What Matters
Instrument every pipeline with data quality checks, freshness monitors, and volume anomaly detection. Use data observability tools (Monte Carlo, Elementary, Soda) to detect issues before they reach dashboards. Define data SLAs with des engagements explicites (ex: "table orders_mart rafraichie avant 08h00 UTC, completude > 99.5%, zero doublons sur order_id") and measure adherence weekly.

---

## Key Frameworks & Methods

| Framework / Method | Purpose | FR |
|---|---|---|
| **Medallion Architecture** | Layered data quality (bronze/silver/gold) | Architecture en couches de qualite des donnees |
| **dbt** | SQL-first transformation framework with testing | Framework de transformation SQL-first avec tests |
| **Data Mesh** | Domain-oriented decentralized data ownership | Ownership decentralise des donnees par domaine |
| **Data Vault 2.0** | Auditable, historized enterprise data modeling | Modelisation auditables et historisee des donnees |
| **Kappa Architecture** | Stream-first, single processing layer | Architecture stream-first, couche unique |
| **Lambda Architecture** | Dual batch+streaming layers (legacy pattern) | Double couche batch+streaming (patron legacy) |
| **DataOps** | Agile and lean applied to data pipelines | Agile et lean appliques aux pipelines de donnees |
| **Open Table Formats** | Iceberg, Delta Lake, Hudi for ACID on data lakes | Formats de table ouverts pour ACID sur data lakes |

---

## Decision Guide

### Choosing ETL vs. ELT
- **ETL (Extract-Transform-Load)** — Transform data before loading into the target. Use when the target system has limited compute (e.g., legacy databases), data must be filtered/anonymized before landing, or strict governance requires transformation before persistence.
- **ELT (Extract-Load-Transform)** — Load raw data first, then transform in the target warehouse. Prefer ELT for modern cloud warehouses (BigQuery, Snowflake, Databricks) where compute is elastic and separation of ingestion from transformation is desirable. This is the dominant modern pattern.

### Choosing Batch vs. Streaming
- **Batch** — Use for daily/hourly analytics, historical aggregations, large backfills, cost-sensitive workloads. Simpler to build, test, and debug. Prefer batch unless latency requirements demand otherwise.
- **Micro-batch** — Use for near-real-time needs (1-15 minute latency). Spark Structured Streaming, dbt with incremental models. Good balance of freshness and simplicity.
- **Streaming** — Use for sub-second latency requirements: fraud detection, real-time personalization, operational alerting. Requires Kafka/Pub/Sub, Flink/ksqlDB, and significantly more operational complexity.

### Choosing a Data Warehouse
- **BigQuery** — Best for GCP-native stacks, serverless pricing model, excellent for ad-hoc analytics. Slot-based pricing for predictable costs at scale.
- **Snowflake** — Best for multi-cloud, strong data sharing capabilities, clean separation of compute and storage. Excellent for organizations needing cross-cloud flexibility.
- **Databricks SQL** — Best when combining warehouse and data science workloads. Unity Catalog for governance. Strong for lakehouse architecture.
- **Redshift** — Best for AWS-native stacks with heavy, predictable workloads. Redshift Serverless for variable workloads.

### Choosing a Data Orchestrator
- **Airflow** — Industry standard, massive ecosystem, broad community. Best for established teams comfortable with Python. Managed options: MWAA, Cloud Composer, Astronomer.
- **Dagster** — Software-defined assets, strong typing, built-in data lineage. Best for teams adopting asset-centric data engineering. Excellent developer experience.
- **Prefect** — Pythonic, dynamic workflow generation, strong observability. Best for Python-heavy teams wanting simplicity over configuration.
- **Mage** — Hybrid notebook + pipeline interface. Best for smaller teams or data scientists building pipelines.

---

## Common Patterns & Anti-Patterns

### Patterns (Do)
- **Medallion Architecture (Bronze/Silver/Gold)**: Ingest raw data into bronze (append-only, schema-on-read), clean and deduplicate in silver (typed, tested), aggregate for consumption in gold (business metrics, star schemas)
- **Incremental Processing with Merge**: Process only new or changed records using watermarks, CDC, or partition-based incremental strategies. Use `MERGE INTO` or dbt incremental models to upsert efficiently
- **Schema Registry for Streaming**: Enforce schema contracts between producers and consumers using Confluent Schema Registry or AWS Glue Schema Registry. Require backward-compatible evolution
- **Data Contracts Between Teams**: Define explicit contracts (schema, SLAs, quality expectations) between data producers and consumers. Use tools like Soda or datacontract-cli to enforce them
- **Partition Pruning and Clustering**: Partition tables by date or high-cardinality dimension. Cluster by frequently filtered columns. This is the single biggest cost and performance lever in cloud warehouses
- **CI/CD for dbt**: Run `dbt build` (models + tests) in CI on every PR. Use slim CI (`--select state:modified+`) to test only changed models. Deploy via automated pipelines, never manually

### Anti-Patterns (Avoid)
- **Full Refresh Everything**: Rebuilding entire tables daily when incremental processing would suffice. Wastes compute and increases latency for large datasets
- **Unmonitored Pipelines**: Pipelines that run on schedule without freshness checks, volume assertions, or schema validation. Data issues silently propagate to dashboards
- **SQL in Orchestrator Code**: Embedding complex SQL inside Airflow DAGs or Python scripts. Extract transformations into dbt models for testability, documentation, and lineage
- **One Giant Pipeline**: Monolithic pipelines that ingest, transform, and serve in a single DAG. Break into independent, composable stages with clear interfaces
- **No Backfill Strategy**: Pipelines that cannot re-process historical data. Design every pipeline to accept a date range parameter and produce idempotent results for that range
- **Ignoring Warehouse Costs**: Running unoptimized queries, using on-demand pricing without monitoring, failing to set query timeouts and slot/credit budgets

---

## Implementation Workflow

Follow this workflow when designing or improving a data platform:

1. **Assess Data Requirements** — Identify data sources (lister chaque source avec : type de connecteur, volume estimé, fréquence de mise à jour, sensibilité PII), latency requirements (batch T+1 vs. near-real-time vs. streaming sub-second), data volumes, and consumer needs. Map the current pipeline topology. Classify data by sensitivity (PII, financial, public).

2. **Design the Architecture** — Choose ELT for modern cloud warehouses. Adopt medallion architecture (bronze/silver/gold). Define data contracts between layers with SLAs explicites (ex: bronze -> silver : fraicheur < 2h, completude > 99%). Select batch, micro-batch, or streaming based on actual latency needs documented in step 1.

3. **Set Up Ingestion** — Deploy integration tools (Fivetran, Airbyte, or custom connectors) for source extraction. Land raw data faithfully in the bronze layer. Implement CDC (Change Data Capture) for transactional sources. Use schema detection and evolution at ingestion.

4. **Build the Transformation Layer** — Implement dbt as the transformation framework. Structure models by layer (staging -> intermediate -> marts). Write tests for every model (not_null, unique, relationships, custom). Generate documentation with `dbt docs`. Use incremental models for large tables.

5. **Configure Orchestration** — Deploy Airflow, Dagster, or Prefect. Define DAGs/assets with clear dependencies. Set up retries with exponential backoff (ex: 3 retries, delais 1min/5min/15min). Configure alerting on failure, SLA misses, and anomalies via Slack/PagerDuty. Implement sensors or triggers for event-driven pipelines.

6. **Implement Data Quality** — Add dbt tests at every layer boundary. Deploy data observability (Elementary, Monte Carlo, or Soda). Monitor freshness, volume, schema, and distribution. Define SLAs: "marketing dashboard refreshed by 08:00 UTC daily."

7. **Establish CI/CD for Data** — Run dbt in CI (lint with sqlfluff, build with tests, generate docs). Use slim CI for efficiency. Implement blue-green deployments for warehouse schema changes. Version-control all pipeline code, SQL, and configuration.

8. **Optimize Costs** — Partition and cluster all large tables (> 1 Go). Monitor per-query and per-pipeline costs with un dashboard dédié mis à jour quotidiennement. Set warehouse auto-suspend (ex: 5 min inactivité) and auto-scaling policies. Use reserved capacity for predictable workloads, on-demand for spikes. Review and eliminate unused tables and pipelines quarterly.

9. **Observe and Iterate** — Track data freshness SLAs, pipeline success rates, data quality scores, and cost per pipeline dans un dashboard opérationnel unique. Run blameless post-incident reviews for data outages. Feed learnings back into architecture and process improvements.

---


## Modèle de maturité

### Niveau 1 — Manuel
- Scripts SQL/Python ad-hoc lancés manuellement, pas d'orchestration
- Données en silos sans catalogue ni documentation, logique métier éparpillée
- Pas de tests ni de validation, qualité des données inconnue
- **Indicateurs** : pipeline reliability < 50%, time-to-insight > 1 semaine

### Niveau 2 — Structuré
- ETL basique avec scheduling (cron/Airflow simple), pipelines identifiés
- Quelques tests de données en place, documentation partielle des sources
- Warehouse centralisé mais transformations peu organisées
- **Indicateurs** : pipeline reliability 60-80%, data freshness SLA compliance < 70%

### Niveau 3 — Industrialisé
- ELT moderne (dbt + warehouse cloud), medallion architecture (bronze/silver/gold)
- Data contracts entre producteurs et consommateurs, tests automatisés systématiques
- CI/CD data en place, environnements de développement isolés
- **Indicateurs** : pipeline reliability > 95%, cost per TB processed suivi et optimisé

### Niveau 4 — Optimisé
- Observabilité data complète : SLAs, freshness monitoring, lineage bout-en-bout
- Streaming intégré (Kafka/Flink) pour les cas d'usage temps réel, DataOps mature
- Coûts optimisés par workload (auto-scaling, partitionnement, lifecycle policies)
- **Indicateurs** : data freshness SLA compliance > 99%, time-to-insight < 4 heures

### Niveau 5 — Self-service
- Data mesh opérationnel avec data products autonomes et interopérables
- Gouvernance fédérée : chaque domaine propriétaire de ses données et SLAs
- Provisionnement automatique de pipelines, schéma discovery, accès self-service
- **Indicateurs** : pipeline reliability > 99.5%, time-to-insight < 30 minutes

## Rythme opérationnel

| Cadence | Activité | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Hebdomadaire** | Revue santé des pipelines (échecs, violations SLA) | Data Engineer | Rapport d'incidents et actions correctives |
| **Hebdomadaire** | Triage des alertes qualité de données | Data Engineer | Backlog priorisé des anomalies |
| **Mensuel** | Analyse des coûts et optimisation infrastructure | Data Engineer Lead | Dashboard coûts et plan d'optimisation |
| **Mensuel** | Revue des contrats de données avec les consommateurs | Data Engineer + Data Analyst | Registre des data contracts mis à jour |
| **Trimestriel** | Rightsizing de l'infrastructure (compute, storage) | Data Engineer Lead | Rapport de dimensionnement et recommandations |
| **Trimestriel** | Revue d'architecture data (patterns, technologies) | Data Architect | Diagramme d'architecture actualisé |
| **Annuel** | Actualisation de la roadmap plateforme data | Head of Data | Roadmap annuelle et budget prévisionnel |

## State of the Art (2025-2026)

L'ingénierie de données évolue vers la simplification et le temps réel :

- **Lakehouse architecture** : L'architecture lakehouse (Delta Lake, Apache Iceberg, Hudi) unifie data lake et data warehouse, simplifiant l'infrastructure.
- **Streaming-first** : Apache Flink et Kafka Streams permettent le traitement temps réel comme paradigme par défaut, avec le batch comme cas particulier.
- **dbt dominant** : dbt s'impose comme le standard de transformation, avec un écosystème riche (dbt Cloud, dbt Mesh, semantic layer).
- **AI data pipelines** : Les pipelines spécifiques à l'IA (embeddings, feature stores, vector indexing) deviennent une spécialité de l'ingénierie de données.
- **DataOps mature** : Les pratiques DataOps (CI/CD pour les pipelines, tests de données, monitoring de qualité) se standardisent sur le modèle du DevOps.

## Template actionnable

### Data contract template

| Champ | Valeur |
|---|---|
| **Nom du dataset** | ___ |
| **Owner** | Équipe ___ |
| **Consommateurs** | Équipe(s) ___ |
| **SLA de fraîcheur** | ___ (ex: T+1, temps réel, horaire) |
| **SLA de qualité** | Taux de nulls < ___%, unicité sur ___ |
| **Schéma** | Colonnes: ___, types: ___, contraintes: ___ |
| **Format** | Parquet / JSON / Avro / CSV |
| **Fréquence de mise à jour** | ___ |
| **Rétention** | ___ jours/mois |
| **Point de contact** | ___ (Slack, email) |
| **Changelog** | Toute modification de schéma notifiée ___ jours avant |

## Prompts types

- "Comment concevoir un pipeline ETL robuste avec dbt ?"
- "Aide-moi à choisir entre data warehouse et data lakehouse"
- "Propose une architecture de streaming avec Kafka"
- "Comment orchestrer nos pipelines avec Airflow ou Dagster ?"
- "Aide-moi à optimiser les coûts de notre data warehouse Snowflake"
- "Comment mettre en place du CDC pour la réplication temps réel ?"

## Limites et Red Flags

Ce skill n'est PAS adapté pour :
- ❌ Concevoir des dashboards, choisir un outil BI ou définir des KPIs métier → Utiliser plutôt : `data-bi:decision-reporting-governance`
- ❌ Former des utilisateurs au data storytelling ou à la lecture de graphiques → Utiliser plutôt : `data-bi:data-literacy`
- ❌ Concevoir l'architecture applicative (microservices, API REST, frontend) → Utiliser plutôt : `code-development:architecture`
- ❌ Gérer la sécurité réseau, les certificats SSL ou l'authentification applicative → Utiliser plutôt : `code-development:auth-security`
- ❌ Entraîner ou déployer des modèles de machine learning (feature engineering, model serving, MLOps) → Utiliser plutôt : un skill dédié MLOps ou `ai-governance:prompt-engineering-llmops` pour les pipelines LLM

Signaux d'alerte en cours d'utilisation :
- ⚠️ Un pipeline n'a aucun test de données (ni dbt test, ni assertion de qualité) — il va silencieusement propager des données corrompues aux dashboards
- ⚠️ Toutes les tables sont en full refresh alors que les volumes dépassent 10M lignes — signe de coûts excessifs et de latence évitable
- ⚠️ Les transformations SQL sont écrites directement dans les DAGs Airflow plutôt que dans des modèles dbt — la logique métier sera introuvable, intestable et sans lineage
- ⚠️ Aucun SLA de fraîcheur n'est défini pour les datasets consommés par les dashboards — personne ne saura si les données sont à jour ou périmées

## Skills connexes

| Skill | Lien |
|---|---|
| Backend & DB | `code-development:backend-db` — Bases de données et optimisation SQL |
| Architecture | `code-development:architecture` — Architecture data et systèmes distribués |
| DevOps | `code-development:devops` — Infrastructure et orchestration des pipelines |
| Decision Reporting | `data-bi:decision-reporting-governance` — Qualité des données et gouvernance |
| Prompt Engineering | `ai-governance:prompt-engineering-llmops` — Pipelines RAG et embeddings |

## Glossaire

| Terme | Définition |
|-------|-----------|
| **ETL (Extract, Transform, Load)** | Patron d'intégration où les données sont extraites, transformées puis chargées dans le système cible. Adapté aux systèmes cibles à capacité de calcul limitée. |
| **ELT (Extract, Load, Transform)** | Patron moderne où les données brutes sont chargées d'abord dans le warehouse, puis transformées sur place grâce à la puissance de calcul élastique du cloud. |
| **Medallion Architecture (Bronze/Silver/Gold)** | Architecture en couches de qualité croissante : bronze (données brutes), silver (nettoyées et conformées), gold (agrégations métier prêtes à consommer). |
| **Data Lakehouse** | Architecture hybride combinant le stockage à faible coût d'un data lake avec les capacités transactionnelles (ACID) et la performance d'un data warehouse. |
| **Data Lake** | Réservoir centralisé de données brutes stockées dans leur format natif (structuré, semi-structuré, non structuré), généralement sur du stockage objet (S3, GCS, ADLS). |
| **Data Warehouse** | Entrepôt de données structurées, optimisé pour les requêtes analytiques. Exemples : BigQuery, Snowflake, Redshift, Databricks SQL. |
| **dbt (data build tool)** | Framework open source de transformation SQL-first permettant de modéliser, tester et documenter les transformations de données directement dans le warehouse. |
| **DAG (Directed Acyclic Graph)** | Graphe orienté sans cycle représentant les dépendances entre tâches d'un pipeline. Structure fondamentale des orchestrateurs comme Airflow et Dagster. |
| **Airflow** | Orchestrateur de workflows open source (Apache). Standard de l'industrie pour planifier et surveiller des pipelines de données via des DAGs Python. |
| **Dagster** | Orchestrateur moderne orienté assets (software-defined assets) avec typage fort, lignage natif et excellente expérience développeur. |
| **Idempotence** | Propriété d'une opération qui, exécutée plusieurs fois avec les mêmes entrées, produit toujours le même résultat sans effets de bord. Essentielle pour la fiabilité des pipelines. |
| **Backfill** | Ré-exécution d'un pipeline sur une période historique pour recalculer ou corriger des données passées. Requiert des pipelines idempotents paramétrés par date. |
| **Schema Evolution** | Capacité d'un système à gérer les modifications de schéma (ajout/suppression de colonnes, changement de types) sans casser les pipelines existants. |
| **CDC (Change Data Capture)** | Technique de capture des modifications (insertions, mises à jour, suppressions) dans une base source pour les répliquer de manière incrémentale vers un système cible. |
| **Partitioning** | Technique de découpage physique des tables par clé (date, région, etc.) pour améliorer les performances de requête et réduire les coûts via le partition pruning. |
| **Data Contract** | Accord formel entre producteurs et consommateurs de données définissant le schéma, les SLAs de qualité et de fraîcheur, et les responsabilités de chaque partie. |
| **Data SLA** | Engagement de niveau de service sur les données : fraîcheur maximale, taux de qualité minimal, disponibilité du pipeline. Exemple : « dashboard mis à jour avant 08h00 UTC ». |
| **Dead Letter Queue** | File d'attente où sont redirigés les messages ou enregistrements en erreur lors du traitement, permettant une analyse et un retraitement ultérieurs sans bloquer le pipeline. |
| **Exactly-once Processing** | Garantie sémantique assurant que chaque enregistrement est traité exactement une fois, sans perte ni doublon, même en cas de panne ou de retry. |

## Additional Resources

Consult these reference files for deep dives on each topic area:

- **[Pipeline Design](./references/pipeline-design.md)** — ETL vs ELT patterns, batch vs streaming architecture, medallion architecture deep dive, idempotency and exactly-once processing, error handling and dead letter queues, schema evolution strategies, backfill patterns.

- **[Data Transformation](./references/data-transformation.md)** — dbt deep dive (models, tests, documentation, snapshots, seeds, metrics), SQL transformations at scale, incremental processing patterns, materialized views, sqlfluff linting, data modeling best practices.

- **[Data Orchestration](./references/data-orchestration.md)** — Airflow deep dive (DAGs, operators, sensors, TaskFlow API), Dagster software-defined assets, Prefect flows, scheduling and dependency management, monitoring and alerting, data SLAs and freshness enforcement.

- **[Data Infrastructure](./references/data-infrastructure.md)** — Data warehouse comparison (BigQuery, Snowflake, Redshift, Databricks), data lake and lakehouse (Delta Lake, Iceberg, Hudi), streaming platforms (Kafka, Pub/Sub, Flink), integration tools (Fivetran, Airbyte, Meltano), DataOps practices, CI/CD for data, cost optimization strategies.

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.
