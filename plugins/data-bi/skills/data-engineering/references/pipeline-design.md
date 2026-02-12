# Pipeline Design — ETL vs ELT, Batch vs Streaming, Medallion Architecture & Resilience Patterns

## Introduction

**FR** — Ce guide de reference couvre la conception de pipelines de donnees modernes : les paradigmes ETL vs ELT, les architectures batch et streaming, l'architecture medallion (bronze/silver/gold), l'idempotence, le traitement exactly-once, la gestion des erreurs, les dead letter queues, et les strategies d'evolution de schema. Chaque pipeline doit etre concu comme un systeme resilient : idempotent, observable, et capable de se remettre gracieusement des pannes.

**EN** — This reference guide covers modern data pipeline design: ETL vs ELT paradigms, batch and streaming architectures, medallion architecture (bronze/silver/gold), idempotency, exactly-once processing, error handling, dead letter queues, and schema evolution strategies. Design every pipeline as a resilient system: idempotent, observable, and capable of graceful failure recovery.

---

## 1. ETL vs ELT — Paradigm Selection

### ETL (Extract-Transform-Load)

**EN** — In ETL, data is transformed in a staging area or processing engine before loading into the target system. This was the dominant pattern when warehouses had limited compute.

**FR** — Dans l'ETL, les donnees sont transformees dans une zone de staging ou un moteur de traitement avant le chargement dans le systeme cible. C'etait le patron dominant quand les entrepots avaient un compute limite.

**When to use ETL:**
- The target system has limited processing capability (OLTP databases, legacy warehouses)
- Data must be filtered, anonymized, or redacted before persisting (GDPR, PII compliance)
- Bandwidth between source and target is expensive or limited
- Transformations are complex and require a dedicated compute engine (Spark, Beam)

```
Source -> [Extract] -> Staging Area -> [Transform (Spark/Python)] -> [Load] -> Target DB
```

### ELT (Extract-Load-Transform)

**EN** — In ELT, raw data is loaded directly into the target warehouse, then transformed using the warehouse's compute engine. This is the dominant modern pattern for cloud analytics.

**FR** — Dans l'ELT, les donnees brutes sont chargees directement dans l'entrepot cible, puis transformees avec le moteur de calcul de l'entrepot. C'est le patron moderne dominant pour l'analytique cloud.

**When to use ELT (default choice for modern stacks):**
- The target is a modern cloud warehouse (BigQuery, Snowflake, Databricks, Redshift)
- Compute is elastic and billed per query or per second
- Raw data must be preserved for auditability and reprocessing
- Transformations are primarily SQL-based (dbt)
- Teams want to decouple ingestion from transformation (different owners, different cadences)

```
Source -> [Extract + Load (Fivetran/Airbyte)] -> Raw Layer (Bronze) -> [Transform (dbt/SQL)] -> Clean Layer (Silver) -> [Aggregate] -> Mart Layer (Gold)
```

### Hybrid Patterns

**EN** — In practice, most modern data platforms use a hybrid approach: ELT for the core analytical pipeline, with ETL components for specific use cases (PII redaction at ingestion, real-time feature engineering, data export to operational systems).

**FR** — En pratique, la plupart des plateformes de donnees modernes utilisent une approche hybride : ELT pour le pipeline analytique principal, avec des composants ETL pour des cas specifiques (redaction PII a l'ingestion, feature engineering temps reel, export de donnees vers des systemes operationnels).

---

## 2. Batch vs Streaming Architecture

### Batch Processing

**EN** — Batch processing handles data in discrete, bounded chunks on a schedule (hourly, daily). It is simpler to build, test, debug, and reason about. Prefer batch unless latency requirements genuinely demand otherwise.

**FR** — Le traitement batch traite les donnees en lots discrets et bornes selon un calendrier (horaire, quotidien). Il est plus simple a construire, tester, deboguer et raisonner. Privilegier le batch sauf si les exigences de latence demandent reellement autre chose.

| Characteristic | Batch | Streaming |
|---|---|---|
| Latency | Minutes to hours | Milliseconds to seconds |
| Complexity | Low to medium | High |
| Cost | Predictable, lower | Variable, higher |
| Error handling | Retry full batch | DLQ, offset management |
| Testing | Straightforward | Requires event simulation |
| State management | Simple (stateless or table-based) | Complex (windowing, watermarks) |
| Best for | Analytics, reporting, ML training | Fraud detection, real-time alerts, CDC |

### Micro-Batch: The Middle Ground

**EN** — Micro-batch processes small batches at high frequency (every 1-15 minutes). It achieves near-real-time latency with batch-like simplicity. Spark Structured Streaming, dbt incremental models on short schedules, and trigger-based pipelines all implement micro-batch patterns.

**FR** — Le micro-batch traite de petits lots a haute frequence (toutes les 1 a 15 minutes). Il atteint une latence quasi temps reel avec la simplicite du batch. Spark Structured Streaming, les modeles incrementaux dbt sur des schedules courts, et les pipelines trigger-based implementent tous des patrons micro-batch.

```python
# Spark Structured Streaming — micro-batch example
df = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "events")
    .load())

transformed = (df
    .selectExpr("CAST(value AS STRING) as json_str")
    .select(from_json("json_str", schema).alias("data"))
    .select("data.*")
    .withWatermark("event_time", "10 minutes"))

(transformed.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/checkpoints/events")
    .trigger(processingTime="5 minutes")  # Micro-batch every 5 min
    .start("/data/bronze/events"))
```

### True Streaming Architecture

**EN** — Use true streaming only when sub-second latency is a hard requirement. Streaming requires Kafka/Pub/Sub as the backbone, a stream processor (Flink, ksqlDB, Spark Streaming), and careful attention to state management, watermarks, and exactly-once semantics.

**FR** — Utiliser le vrai streaming uniquement quand la latence sub-seconde est une exigence dure. Le streaming necessite Kafka/Pub/Sub comme backbone, un processeur de flux (Flink, ksqlDB, Spark Streaming), et une attention soigneuse a la gestion d'etat, aux watermarks, et a la semantique exactly-once.

### Lambda vs Kappa Architecture

**Lambda (legacy — avoid for new systems):**
- Two parallel paths: batch layer (complete, accurate) + speed layer (approximate, real-time)
- Merge results at query time
- Problem: maintaining two codebases for the same logic

**Kappa (preferred for streaming-first):**
- Single processing path using a stream processor
- Replay from the event log (Kafka) for reprocessing
- Simpler, but requires a mature streaming infrastructure

**EN** — For most analytics use cases, prefer a batch-first approach with micro-batch for near-real-time needs. Reserve true Kappa architecture for platforms where streaming is the primary consumption pattern.

---

## 3. Medallion Architecture (Bronze / Silver / Gold)

### Overview

**EN** — The medallion architecture organizes data into three layers of increasing quality and business value. Each layer has clear responsibilities, ownership, and quality expectations. This is the standard for modern ELT-based data platforms.

**FR** — L'architecture medallion organise les donnees en trois couches de qualite et de valeur metier croissantes. Chaque couche a des responsabilites, un ownership et des attentes de qualite clairs. C'est le standard pour les plateformes de donnees modernes basees sur ELT.

### Bronze Layer (Raw / Landing)

**Purpose:** Faithful copy of source data. No transformations, no filtering, no deduplication.

**FR** — Copie fidele des donnees sources. Aucune transformation, aucun filtrage, aucune deduplication.

**Characteristics:**
- Append-only ingestion (never update or delete raw records)
- Schema-on-read (store as-is, even if messy)
- Add metadata columns: `_ingested_at`, `_source_system`, `_batch_id`, `_file_name`
- Retain for compliance and reprocessing (typically 90 days to 7 years depending on regulations)
- Partitioned by ingestion date for efficient backfills

```sql
-- Bronze table structure example (BigQuery)
CREATE TABLE bronze.crm_contacts (
    _raw_json       STRING,           -- Full source payload
    _ingested_at    TIMESTAMP,        -- Ingestion timestamp
    _source_system  STRING,           -- Source identifier
    _batch_id       STRING,           -- Batch run identifier
    _file_name      STRING            -- Source file name if applicable
)
PARTITION BY DATE(_ingested_at)
OPTIONS (
    description = 'Raw CRM contacts — append-only, no transformations'
);
```

### Silver Layer (Cleaned / Conformed)

**Purpose:** Cleaned, typed, deduplicated, and conformed data. Business entities are identifiable. Quality is tested.

**FR** — Donnees nettoyees, typees, dedupliquees et conformees. Les entites metier sont identifiables. La qualite est testee.

**Characteristics:**
- Strong typing (cast strings to dates, integers, etc.)
- Deduplication (identify and resolve duplicate records)
- Null handling (fill defaults, flag missing values)
- Standardization (normalize country codes, currency, timestamps to UTC)
- PII tagging or masking
- dbt tests at this layer: `not_null`, `unique`, `accepted_values`, `relationships`

```sql
-- Silver model example (dbt)
-- models/silver/crm/silver_crm_contacts.sql

{{
    config(
        materialized='incremental',
        unique_key='contact_id',
        partition_by={'field': 'updated_at', 'data_type': 'date'},
        cluster_by=['country_code']
    )
}}

WITH source AS (
    SELECT
        JSON_EXTRACT_SCALAR(_raw_json, '$.id') AS contact_id,
        JSON_EXTRACT_SCALAR(_raw_json, '$.email') AS email,
        UPPER(JSON_EXTRACT_SCALAR(_raw_json, '$.country')) AS country_code,
        PARSE_TIMESTAMP(
            '%Y-%m-%dT%H:%M:%S',
            JSON_EXTRACT_SCALAR(_raw_json, '$.updated_at')
        ) AS updated_at,
        _ingested_at
    FROM {{ source('bronze', 'crm_contacts') }}
    {% if is_incremental() %}
    WHERE _ingested_at > (SELECT MAX(_ingested_at) FROM {{ this }})
    {% endif %}
),

deduplicated AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY contact_id
            ORDER BY updated_at DESC
        ) AS _row_num
    FROM source
)

SELECT * EXCEPT(_row_num)
FROM deduplicated
WHERE _row_num = 1
```

### Gold Layer (Business / Consumption)

**Purpose:** Business-level aggregations, star schemas, metrics, and entities ready for direct consumption by analysts, dashboards, and ML features.

**FR** — Agregations metier, schemas en etoile, metriques et entites pretes pour la consommation directe par les analystes, les dashboards et les features ML.

**Characteristics:**
- Star schema or One Big Table (OBT) patterns
- Pre-computed aggregations (daily revenue, monthly active users)
- Business terminology (not technical source names)
- Denormalized for query performance
- Documented with business descriptions

```sql
-- Gold model example (dbt)
-- models/gold/marketing/gold_marketing_daily_metrics.sql

{{
    config(
        materialized='table',
        partition_by={'field': 'metric_date', 'data_type': 'date'},
        cluster_by=['channel']
    )
}}

SELECT
    DATE(c.created_at)          AS metric_date,
    c.acquisition_channel       AS channel,
    COUNT(DISTINCT c.contact_id) AS new_contacts,
    COUNT(DISTINCT o.order_id)   AS conversions,
    SUM(o.revenue_usd)           AS total_revenue,
    SAFE_DIVIDE(
        COUNT(DISTINCT o.order_id),
        COUNT(DISTINCT c.contact_id)
    ) AS conversion_rate
FROM {{ ref('silver_crm_contacts') }} c
LEFT JOIN {{ ref('silver_orders') }} o
    ON c.contact_id = o.contact_id
    AND DATE(o.order_date) = DATE(c.created_at)
GROUP BY 1, 2
```

---

## 4. Idempotency and Exactly-Once Processing

### Why Idempotency Matters

**EN** — Pipelines fail. Orchestrators retry. Duplicate events arrive. An idempotent pipeline produces the same result regardless of how many times it runs for the same input. Without idempotency, retries cause duplicated or corrupted data.

**FR** — Les pipelines echouent. Les orchestrateurs relancent. Des evenements dupliques arrivent. Un pipeline idempotent produit le meme resultat quel que soit le nombre de fois qu'il s'execute pour la meme entree. Sans idempotence, les relances causent des donnees dupliquees ou corrompues.

### Idempotency Patterns

**Pattern 1 — Partition overwrite:**
```sql
-- Delete and replace an entire partition
DELETE FROM silver.events WHERE event_date = '2025-01-15';
INSERT INTO silver.events SELECT * FROM staging.events WHERE event_date = '2025-01-15';
```

**Pattern 2 — MERGE / upsert:**
```sql
MERGE INTO silver.customers AS target
USING staging.customers_delta AS source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN UPDATE SET
    target.email = source.email,
    target.updated_at = source.updated_at
WHEN NOT MATCHED THEN INSERT (customer_id, email, updated_at)
VALUES (source.customer_id, source.email, source.updated_at);
```

**Pattern 3 — Deduplication at read time:**
```sql
-- Use ROW_NUMBER to pick the latest version of each record
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY event_id ORDER BY event_timestamp DESC
    ) AS rn
    FROM bronze.events
)
SELECT * EXCEPT(rn) FROM ranked WHERE rn = 1;
```

### Exactly-Once Semantics in Streaming

**EN** — True exactly-once delivery is impossible in distributed systems (Two Generals Problem). Instead, aim for effectively-once by combining at-least-once delivery with idempotent consumers.

**FR** — La livraison exactement-une-fois est impossible dans les systemes distribus (probleme des deux generaux). Viser plutot l'effectively-once en combinant livraison at-least-once avec des consommateurs idempotents.

**Implementation:**
- Kafka: Enable `enable.idempotence=true` on producers, use transactional consumers with `isolation.level=read_committed`
- Flink: Use checkpointing with exactly-once sinks (Kafka, filesystem, Iceberg)
- Spark Structured Streaming: Use checkpoints and idempotent sinks (Delta Lake, Iceberg)

---

## 5. Error Handling and Dead Letter Queues

### Error Classification

| Error Type | Example | Strategy |
|---|---|---|
| **Transient** | Network timeout, rate limit | Retry with exponential backoff |
| **Data quality** | Invalid JSON, type mismatch | Route to dead letter queue (DLQ) |
| **Schema** | Missing required column | Halt pipeline, alert on-call |
| **Infrastructure** | Out of memory, disk full | Halt pipeline, alert infrastructure team |
| **Business logic** | Negative revenue, future dates | Route to quarantine table, alert data team |

### Dead Letter Queue Pattern

**EN** — A dead letter queue (DLQ) captures records that cannot be processed. Isolate bad records instead of failing the entire pipeline. Periodically review, fix, and replay DLQ records.

**FR** — Une dead letter queue (DLQ) capture les enregistrements qui ne peuvent pas etre traites. Isoler les mauvais enregistrements au lieu de faire echouer tout le pipeline. Periodiquement revoir, corriger et rejouer les enregistrements de la DLQ.

```python
# DLQ pattern in Python
from datetime import datetime

def process_record(record, dlq_table):
    try:
        validated = validate_schema(record)
        transformed = apply_transformations(validated)
        write_to_silver(transformed)
    except ValidationError as e:
        write_to_dlq(dlq_table, record, error=str(e), timestamp=datetime.utcnow())
    except TransientError as e:
        raise  # Let the orchestrator retry the whole task
```

```sql
-- DLQ table structure
CREATE TABLE dlq.failed_records (
    original_payload    STRING,
    error_message       STRING,
    error_type          STRING,
    source_table        STRING,
    pipeline_run_id     STRING,
    failed_at           TIMESTAMP,
    reprocessed         BOOLEAN DEFAULT FALSE,
    reprocessed_at      TIMESTAMP
)
PARTITION BY DATE(failed_at);
```

### Retry Strategies

- **Exponential backoff**: Wait 1s, 2s, 4s, 8s, ... up to a maximum (e.g., 5 minutes). Add jitter to avoid thundering herd.
- **Circuit breaker**: After N consecutive failures, stop retrying and alert. Prevents wasting resources on a persistently failing upstream.
- **Maximum retry count**: Set a hard limit (e.g., 3 retries). After exhaustion, route to DLQ and move on.

---

## 6. Schema Evolution Strategies

### The Problem

**EN** — Source systems change schemas without warning: columns are added, renamed, removed, or retyped. Without a schema evolution strategy, these changes break pipelines silently or loudly.

**FR** — Les systemes sources changent de schema sans prevenir : des colonnes sont ajoutees, renommees, supprimees ou retypees. Sans strategie d'evolution de schema, ces changements cassent les pipelines silencieusement ou bruyamment.

### Evolution Policies

| Policy | Description | When to Use |
|---|---|---|
| **Backward compatible** | New schema can read old data | Default for most systems |
| **Forward compatible** | Old schema can read new data | When consumers upgrade slowly |
| **Full compatible** | Both backward and forward | Critical shared schemas |
| **Breaking change** | Requires coordinated migration | Major redesigns only |

### Implementation by Layer

**Bronze:** Accept any schema. Store raw payloads (JSON, Avro, Parquet). Add new columns automatically. Never reject data at ingestion due to schema changes.

**Silver:** Detect schema changes. For additive changes (new columns), add them automatically with NULL defaults. For breaking changes (removed/renamed columns), halt the pipeline and alert. Use dbt `schema_tests` to validate expectations.

**Streaming (Schema Registry):**
```
# Confluent Schema Registry — enforce backward compatibility
curl -X PUT \
  http://schema-registry:8081/config/events-value \
  -H 'Content-Type: application/vnd.schemaregistry.v1+json' \
  -d '{"compatibility": "BACKWARD"}'
```

### Schema Detection Automation

**EN** — Implement automated schema change detection in the ingestion layer. Compare incoming schema against the registered schema. Classify changes as safe (additive), warning (type widening), or breaking (removal, rename, type narrowing). Route alerts accordingly.

**FR** — Implementer la detection automatisee des changements de schema dans la couche d'ingestion. Comparer le schema entrant au schema enregistre. Classer les changements en sans risque (additif), avertissement (elargissement de type), ou cassant (suppression, renommage, retrecissement de type). Router les alertes en consequence.

---

## 7. Backfill Patterns

### Design for Backfill from Day One

**EN** — Every pipeline must support re-processing historical data. Backfills happen regularly: schema changes require reprocessing, bugs need fixing, new transformations need historical data. A pipeline that cannot backfill is a pipeline that accumulates technical debt.

**FR** — Chaque pipeline doit supporter le retraitement de donnees historiques. Les backfills sont frequents : les changements de schema necessitent un retraitement, les bugs necessitent des corrections, les nouvelles transformations necessitent des donnees historiques. Un pipeline qui ne peut pas faire de backfill est un pipeline qui accumule de la dette technique.

### Backfill Strategies

**Partition-based backfill (preferred):**
```python
# Airflow — parameterized backfill
@task
def transform_partition(execution_date: str):
    """Process a single partition. Idempotent by design."""
    run_dbt_model(
        model="silver_events",
        vars={"partition_date": execution_date}
    )

# Trigger backfill for a date range
# airflow dags backfill -s 2025-01-01 -e 2025-01-31 my_dag
```

**Full re-materialization:**
```sql
-- When the transformation logic changes fundamentally
-- Rebuild the entire table from bronze
{{
    config(
        materialized='table',  -- Full refresh
        full_refresh=true
    )
}}
SELECT ... FROM {{ source('bronze', 'events') }}
```

**Blue-green backfill:**
- Build the backfilled table in a shadow schema (`silver_v2.events`)
- Validate data quality and row counts against the current table
- Swap the table atomically (rename or view redirect)
- Keep the old table for 7 days as a safety net

### Backfill Guardrails

- Always test backfill logic on a small date range before running the full range
- Set warehouse concurrency limits to prevent backfills from starving production queries
- Monitor costs during backfill — large historical reprocessing can generate unexpected bills
- Log backfill runs separately from regular runs for observability

---

## 8. Pipeline Design Checklist

Use this checklist when designing or reviewing a data pipeline:

- [ ] Is the pipeline idempotent? Can it be re-run safely?
- [ ] Does it follow the medallion architecture (bronze -> silver -> gold)?
- [ ] Is schema evolution handled? What happens if a source column is added or removed?
- [ ] Are errors classified (transient vs. data quality vs. infrastructure)?
- [ ] Is there a dead letter queue for unprocessable records?
- [ ] Does the pipeline support backfill for arbitrary date ranges?
- [ ] Are data quality tests defined at each layer boundary?
- [ ] Is freshness monitored? Is there an SLA?
- [ ] Are costs estimated and budgeted?
- [ ] Is the pipeline documented (data lineage, business context, owner)?

**FR** — Utiliser cette checklist lors de la conception ou de la revue d'un pipeline de donnees. Chaque point non coche represente un risque operationnel.

**EN** — Every unchecked item represents an operational risk. Address them before deploying to production.
