---
name: data-engineering
description: This skill should be used when the user asks about "data pipeline", "ETL", "ELT", "dbt", "data warehouse", "data lake", "data lakehouse", "Airflow", "Dagster", "streaming", "Kafka", "data orchestration", "Snowflake", "BigQuery", "data transformation", "data infrastructure", "pipeline de données", "entrepôt de données", "lac de données", "orchestration de données", "transformation de données", "infrastructure de données", "ingestion de données", "data ingestion", "batch processing", "traitement par lots", "stream processing", "traitement en temps réel", "real-time data", "données temps réel", "Apache Spark", "Flink", "Fivetran", "Airbyte", "Stitch", "CDC", "change data capture", "data partitioning", "data compaction", "Iceberg", "Delta Lake", "Parquet", "Avro", "schema evolution", "idempotency", "backfill", "data freshness", or needs guidance on data engineering, pipeline architecture, and data platform design.
version: 1.0.0
---

# Data Engineering — Pipelines, Transformations, Orchestration & Data Infrastructure

## Overview

**FR** — Cette skill couvre l'ensemble des pratiques modernes de data engineering : conception de pipelines de donnees (ETL/ELT), architectures batch et streaming, transformation avec dbt, orchestration avec Airflow/Dagster/Prefect, et infrastructure de donnees (data warehouse, data lake, data lakehouse). L'objectif est de construire des plateformes de donnees fiables, scalables et economiques — de l'ingestion brute a la couche de consommation analytique. Les recommandations sont alignees avec les meilleures pratiques 2024-2026, incluant l'architecture medallion, les formats de table ouverts (Iceberg, Delta Lake), le streaming unifie, et l'observabilite des donnees.

**EN** — This skill covers the full spectrum of modern data engineering practices: data pipeline design (ETL/ELT), batch and streaming architectures, transformation with dbt, orchestration with Airflow/Dagster/Prefect, and data infrastructure (data warehouse, data lake, data lakehouse). The goal is to build reliable, scalable, and cost-efficient data platforms — from raw ingestion to the analytical consumption layer. Recommendations are aligned with 2024-2026 best practices, including medallion architecture, open table formats (Iceberg, Delta Lake), unified streaming, and data observability.

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
Apply unit tests to transformations, integration tests to pipeline stages, and data quality tests to outputs. Use dbt tests, Great Expectations, or Soda for assertion-based data validation. Never deploy an untested transformation to production. / Appliquer des tests unitaires aux transformations, des tests d'integration aux etapes du pipeline, et des tests de qualite aux sorties. Utiliser les tests dbt, Great Expectations, ou Soda pour la validation des donnees par assertions. Ne jamais deployer une transformation non testee en production.

### 5. Optimize for Cost and Performance Together
Choose the right processing paradigm (batch vs. micro-batch vs. streaming) based on latency requirements, not hype. Partition and cluster tables. Use incremental processing over full refreshes. Monitor compute costs per pipeline and set budgets. / Choisir le bon paradigme de traitement (batch vs. micro-batch vs. streaming) en fonction des exigences de latence, pas de la mode. Partitionner et clusterer les tables. Privilegier le traitement incremental aux rafraichissements complets. Surveiller les couts de calcul par pipeline et fixer des budgets.

### 6. Observe Everything, Alert on What Matters
Instrument every pipeline with data quality checks, freshness monitors, and volume anomaly detection. Use data observability tools (Monte Carlo, Elementary, Soda) to detect issues before they reach dashboards. Define data SLAs and measure adherence. / Instrumenter chaque pipeline avec des controles de qualite, des moniteurs de fraicheur, et la detection d'anomalies de volume. Utiliser des outils d'observabilite des donnees (Monte Carlo, Elementary, Soda) pour detecter les problemes avant qu'ils n'atteignent les dashboards. Definir des SLAs de donnees et mesurer leur respect.

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

1. **Assess Data Requirements** — Identify data sources, latency requirements, data volumes, and consumer needs. Map the current pipeline topology. Classify data by sensitivity (PII, financial, public).

2. **Design the Architecture** — Choose ELT for modern cloud warehouses. Adopt medallion architecture (bronze/silver/gold). Define data contracts between layers. Select batch, micro-batch, or streaming based on actual latency needs.

3. **Set Up Ingestion** — Deploy integration tools (Fivetran, Airbyte, or custom connectors) for source extraction. Land raw data faithfully in the bronze layer. Implement CDC (Change Data Capture) for transactional sources. Use schema detection and evolution at ingestion.

4. **Build the Transformation Layer** — Implement dbt as the transformation framework. Structure models by layer (staging -> intermediate -> marts). Write tests for every model (not_null, unique, relationships, custom). Generate documentation with `dbt docs`. Use incremental models for large tables.

5. **Configure Orchestration** — Deploy Airflow, Dagster, or Prefect. Define DAGs/assets with clear dependencies. Set up retries with exponential backoff. Configure alerting on failure, SLA misses, and anomalies. Implement sensors or triggers for event-driven pipelines.

6. **Implement Data Quality** — Add dbt tests at every layer boundary. Deploy data observability (Elementary, Monte Carlo, or Soda). Monitor freshness, volume, schema, and distribution. Define SLAs: "marketing dashboard refreshed by 08:00 UTC daily."

7. **Establish CI/CD for Data** — Run dbt in CI (lint with sqlfluff, build with tests, generate docs). Use slim CI for efficiency. Implement blue-green deployments for warehouse schema changes. Version-control all pipeline code, SQL, and configuration.

8. **Optimize Costs** — Partition and cluster all large tables. Monitor per-query and per-pipeline costs. Set warehouse auto-suspend and auto-scaling policies. Use reserved capacity for predictable workloads, on-demand for spikes. Review and eliminate unused tables and pipelines quarterly.

9. **Observe and Iterate** — Track data freshness SLAs, pipeline success rates, data quality scores, and cost per pipeline. Run blameless post-incident reviews for data outages. Feed learnings back into architecture and process improvements.

---


## Prompts types

- "Comment concevoir un pipeline ETL robuste avec dbt ?"
- "Aide-moi à choisir entre data warehouse et data lakehouse"
- "Propose une architecture de streaming avec Kafka"
- "Comment orchestrer nos pipelines avec Airflow ou Dagster ?"
- "Aide-moi à optimiser les coûts de notre data warehouse Snowflake"
- "Comment mettre en place du CDC pour la réplication temps réel ?"

## Skills connexes

| Skill | Lien |
|---|---|
| Backend & DB | `code-development:backend-db` — Bases de données et optimisation SQL |
| Architecture | `code-development:architecture` — Architecture data et systèmes distribués |
| DevOps | `code-development:devops` — Infrastructure et orchestration des pipelines |
| Decision Reporting | `data-bi:decision-reporting-governance` — Qualité des données et gouvernance |
| Prompt Engineering | `ai-governance:prompt-engineering-llmops` — Pipelines RAG et embeddings |

## Additional Resources

Consult these reference files for deep dives on each topic area:

- **[Pipeline Design](./references/pipeline-design.md)** — ETL vs ELT patterns, batch vs streaming architecture, medallion architecture deep dive, idempotency and exactly-once processing, error handling and dead letter queues, schema evolution strategies, backfill patterns.

- **[Data Transformation](./references/data-transformation.md)** — dbt deep dive (models, tests, documentation, snapshots, seeds, metrics), SQL transformations at scale, incremental processing patterns, materialized views, sqlfluff linting, data modeling best practices.

- **[Data Orchestration](./references/data-orchestration.md)** — Airflow deep dive (DAGs, operators, sensors, TaskFlow API), Dagster software-defined assets, Prefect flows, scheduling and dependency management, monitoring and alerting, data SLAs and freshness enforcement.

- **[Data Infrastructure](./references/data-infrastructure.md)** — Data warehouse comparison (BigQuery, Snowflake, Redshift, Databricks), data lake and lakehouse (Delta Lake, Iceberg, Hudi), streaming platforms (Kafka, Pub/Sub, Flink), integration tools (Fivetran, Airbyte, Meltano), DataOps practices, CI/CD for data, cost optimization strategies.
