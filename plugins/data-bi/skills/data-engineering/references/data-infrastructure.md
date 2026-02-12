# Data Infrastructure — Warehouses, Lakehouses, Streaming, Integration & DataOps

## Introduction

**FR** — Ce guide de reference couvre l'infrastructure de donnees moderne : comparaison des data warehouses (BigQuery, Snowflake, Redshift, Databricks), data lake et lakehouse (Delta Lake, Iceberg, Hudi), plateformes de streaming (Kafka, Pub/Sub, Flink), outils d'integration (Fivetran, Airbyte, Meltano), pratiques DataOps, CI/CD pour les donnees, et optimisation des couts. Choisir la bonne infrastructure est la decision architecturale la plus consequente d'une plateforme de donnees — elle conditionne les performances, les couts et l'agilite pour des annees.

**EN** — This reference guide covers modern data infrastructure: data warehouse comparison (BigQuery, Snowflake, Redshift, Databricks), data lake and lakehouse (Delta Lake, Iceberg, Hudi), streaming platforms (Kafka, Pub/Sub, Flink), integration tools (Fivetran, Airbyte, Meltano), DataOps practices, CI/CD for data, and cost optimization. Choosing the right infrastructure is the most consequential architectural decision for a data platform — it determines performance, cost, and agility for years.

---

## 1. Data Warehouse Comparison

### BigQuery (Google Cloud)

**Architecture:** Serverless, columnar storage with Dremel query engine. Separation of storage and compute. No cluster management required.

**FR** — BigQuery est entierement serverless : aucun cluster a gerer, aucune capacite a provisionner pour les requetes ad-hoc. Le modele de tarification par requete est ideal pour les charges de travail variables.

**Key characteristics:**
- Serverless: No infrastructure to manage, auto-scales to petabytes
- Pricing: On-demand ($7.50/TB scanned) or slot-based ($0.06/slot-hour for editions)
- Partitioning: By date, integer range, or ingestion time
- Clustering: Up to 4 columns per table, auto-reclustered
- Nested/repeated fields (STRUCT, ARRAY): First-class support, reduces joins
- BigQuery ML: Train ML models directly in SQL
- BI Engine: In-memory acceleration for dashboards
- Materialized views: Auto-refreshed, query optimizer routes to them automatically

**Best practices:**
```sql
-- Always partition and cluster large tables
CREATE TABLE project.silver.events (
    event_id        STRING,
    event_type      STRING,
    user_id         STRING,
    event_timestamp TIMESTAMP,
    properties      JSON,
    event_date      DATE
)
PARTITION BY event_date
CLUSTER BY event_type, user_id
OPTIONS (
    partition_expiration_days = 365,  -- Auto-delete old partitions
    require_partition_filter = TRUE    -- Force partition pruning
);

-- Use INFORMATION_SCHEMA for cost monitoring
SELECT
    user_email,
    SUM(total_bytes_processed) / POW(1024, 4) AS tb_scanned,
    SUM(total_bytes_processed) / POW(1024, 4) * 7.50 AS estimated_cost_usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY user_email
ORDER BY tb_scanned DESC;
```

### Snowflake

**Architecture:** Multi-cluster shared data. Separation of storage (S3/GCS/Azure Blob), compute (virtual warehouses), and cloud services. Each warehouse scales independently.

**FR** — Snowflake offre une separation complete du stockage et du compute. Chaque virtual warehouse est un cluster de compute independant, permettant d'isoler les charges de travail analytiques, d'ingestion et de transformation.

**Key characteristics:**
- Virtual warehouses: Independent compute clusters (XS to 6XL), auto-suspend/resume
- Multi-cloud: Available on AWS, GCP, and Azure with cross-cloud data sharing
- Data sharing: Secure, zero-copy sharing between Snowflake accounts
- Time travel: Query data as it existed up to 90 days ago
- Snowpark: DataFrame API for Python, Java, Scala transformations
- Dynamic tables: Declarative pipelines inside Snowflake (dbt alternative for simple transforms)
- Cortex: Built-in LLM functions for text processing
- Iceberg tables: Native support for Apache Iceberg format

**Best practices:**
```sql
-- Configure warehouse auto-suspend and auto-resume
ALTER WAREHOUSE transform_wh SET
    AUTO_SUSPEND = 60          -- Suspend after 60 seconds idle
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 3      -- Auto-scale up to 3 clusters
    SCALING_POLICY = 'ECONOMY';-- Queue queries before scaling up

-- Resource monitors for cost control
CREATE RESOURCE MONITOR monthly_budget
    WITH CREDIT_QUOTA = 1000
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS
        ON 75 PERCENT DO NOTIFY
        ON 90 PERCENT DO NOTIFY
        ON 100 PERCENT DO SUSPEND;

ALTER WAREHOUSE transform_wh SET RESOURCE_MONITOR = monthly_budget;

-- Query tagging for cost attribution
ALTER SESSION SET QUERY_TAG = 'pipeline:elt_crm|team:data-engineering';
```

### Amazon Redshift

**Architecture:** Columnar, massively parallel processing (MPP). Available as provisioned clusters or Redshift Serverless. Tight AWS integration.

**FR** — Redshift est le data warehouse natif AWS. Redshift Serverless simplifie l'exploitation en eliminant la gestion de clusters. Les performances sont excellentes pour les charges de travail previsibles et lourdes.

**Key characteristics:**
- Redshift Serverless: Pay-per-query, auto-scaling (recommended for new workloads)
- Provisioned: RA3 nodes with managed storage on S3
- Spectrum: Query data directly in S3 without loading
- AQUA: Hardware-accelerated cache for push-down processing
- Data sharing: Cross-cluster and cross-account data sharing
- Federated query: Query RDS, Aurora, S3 directly from Redshift

### Databricks SQL

**Architecture:** Lakehouse platform combining data lake storage with warehouse SQL capabilities. Built on Delta Lake and Apache Spark. Unity Catalog for governance.

**FR** — Databricks SQL est la couche warehouse d'une plateforme lakehouse. Il combine le stockage open (Delta Lake) avec un moteur SQL performant et un catalogue de gouvernance unifie (Unity Catalog). Ideal quand les equipes ont des besoins analytiques ET de data science sur les memes donnees.

**Key characteristics:**
- SQL Warehouses: Serverless or classic, with auto-scaling
- Delta Lake: ACID transactions, time travel, schema enforcement on data lake storage
- Unity Catalog: Unified governance for tables, ML models, files, and notebooks
- Photon engine: Vectorized query execution, significant performance boost
- Workflows: Built-in orchestration for notebooks and jobs
- Multi-language: SQL, Python, Scala, R in the same platform

### Warehouse Comparison Matrix

| Feature | BigQuery | Snowflake | Redshift | Databricks SQL |
|---|---|---|---|---|
| **Pricing model** | Per-TB or slots | Per-credit (compute time) | Per-RPU or nodes | Per-DBU (compute time) |
| **Serverless** | Yes (native) | Yes (warehouses) | Yes (Serverless) | Yes (SQL Warehouses) |
| **Storage format** | Capacitor (proprietary) | Proprietary (micro-partitions) | Columnar (proprietary) | Delta Lake (open) |
| **Multi-cloud** | GCP only | AWS, GCP, Azure | AWS only | AWS, GCP, Azure |
| **Data lake query** | External tables, BigLake | External tables, Iceberg | Spectrum | Native (Delta Lake) |
| **ML integration** | BigQuery ML | Snowpark ML | SageMaker | MLflow, Mosaic AI |
| **Best for** | GCP shops, ad-hoc analytics | Multi-cloud, data sharing | AWS shops, stable workloads | Lakehouse, ML + analytics |

---

## 2. Data Lake and Lakehouse

### Data Lake Fundamentals

**EN** — A data lake stores raw data in its native format on cheap object storage (S3, GCS, ADLS). The key innovation of the lakehouse is adding ACID transactions, schema enforcement, and time travel to data lake storage using open table formats.

**FR** — Un data lake stocke les donnees brutes dans leur format natif sur du stockage objet economique (S3, GCS, ADLS). L'innovation cle du lakehouse est d'ajouter les transactions ACID, l'enforcement de schema et le time travel au stockage data lake via des formats de table ouverts.

### Open Table Formats Comparison

| Feature | Delta Lake | Apache Iceberg | Apache Hudi |
|---|---|---|---|
| **Origin** | Databricks | Netflix/Apple | Uber |
| **ACID transactions** | Yes | Yes | Yes |
| **Time travel** | Yes | Yes | Yes |
| **Schema evolution** | Yes | Yes (strong) | Yes |
| **Partition evolution** | Limited | Yes (hidden partitions) | Limited |
| **Engine support** | Spark, Flink, Trino, DuckDB | Spark, Flink, Trino, Dremio, Snowflake, BigQuery | Spark, Flink, Trino |
| **Adoption (2025)** | High (Databricks ecosystem) | Very high (multi-engine standard) | Medium |
| **UniForm support** | Yes (Delta UniForm reads Iceberg) | N/A | N/A |

### Apache Iceberg Deep Dive

**EN** — Iceberg is emerging as the industry standard for open table formats. It provides true partition evolution (change partitioning without rewriting data), hidden partitioning (users do not need to know the partition scheme), and broad engine support. Snowflake, BigQuery, Databricks, and Trino all support Iceberg tables.

**FR** — Iceberg emerge comme le standard industriel pour les formats de table ouverts. Il fournit une vraie evolution de partitionnement (changer le partitionnement sans recrire les donnees), le partitionnement cache (les utilisateurs n'ont pas besoin de connaitre le schema de partition), et un large support de moteurs.

```python
# Creating an Iceberg table with PyIceberg
from pyiceberg.catalog import load_catalog

catalog = load_catalog("my_catalog", **{
    "type": "glue",
    "s3.region": "us-east-1",
})

from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType, TimestampType, LongType

schema = Schema(
    NestedField(1, "event_id", StringType(), required=True),
    NestedField(2, "event_type", StringType(), required=True),
    NestedField(3, "user_id", StringType()),
    NestedField(4, "event_timestamp", TimestampType()),
    NestedField(5, "properties", StringType()),
)

from pyiceberg.partitioning import PartitionSpec, PartitionField
from pyiceberg.transforms import DayTransform

partition_spec = PartitionSpec(
    PartitionField(
        source_id=4, field_id=1000,
        transform=DayTransform(), name="event_day"
    )
)

catalog.create_table(
    identifier="bronze.events",
    schema=schema,
    partition_spec=partition_spec,
    location="s3://data-lake/bronze/events/",
)
```

### Delta Lake Deep Dive

```sql
-- Delta Lake operations in Databricks / Spark SQL

-- Create a Delta table
CREATE TABLE silver.events (
    event_id        STRING,
    event_type      STRING,
    user_id         STRING,
    event_timestamp TIMESTAMP,
    event_date      DATE GENERATED ALWAYS AS (CAST(event_timestamp AS DATE))
)
USING DELTA
PARTITIONED BY (event_date)
TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true',
    'delta.logRetentionDuration' = 'interval 30 days',
    'delta.deletedFileRetentionDuration' = 'interval 7 days'
);

-- Upsert with MERGE
MERGE INTO silver.events AS target
USING bronze.events_staging AS source
ON target.event_id = source.event_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- Time travel
SELECT * FROM silver.events VERSION AS OF 42;    -- By version number
SELECT * FROM silver.events TIMESTAMP AS OF '2025-01-15T10:00:00'; -- By timestamp

-- Optimize (compaction + Z-ordering)
OPTIMIZE silver.events ZORDER BY (user_id, event_type);

-- Vacuum (remove old files)
VACUUM silver.events RETAIN 168 HOURS;  -- Keep 7 days of history
```

### Lakehouse Architecture Pattern

```
Source Systems
    |
    v
[Ingestion Layer] -- Fivetran / Airbyte / Kafka Connect / Custom
    |
    v
[Bronze Layer] -- S3/GCS + Delta/Iceberg -- Raw, append-only
    |
    v
[Silver Layer] -- S3/GCS + Delta/Iceberg -- Cleaned, typed, tested
    |                                          (dbt transformations)
    v
[Gold Layer] -- S3/GCS + Delta/Iceberg -- Business metrics, star schemas
    |
    +---> [SQL Warehouse] -- Snowflake / Databricks SQL / Trino -- BI & Analytics
    +---> [ML Platform] -- Databricks ML / SageMaker / Vertex AI -- Data Science
    +---> [Reverse ETL] -- Census / Hightouch -- Push to operational systems
```

---

## 3. Streaming Platforms

### Apache Kafka

**EN** — Kafka is the de facto standard for event streaming. It provides a durable, distributed, append-only log. Use Kafka for event-driven architectures, CDC (Change Data Capture), real-time pipelines, and as the backbone of a Kappa architecture.

**FR** — Kafka est le standard de facto pour le streaming d'evenements. Il fournit un log durable, distribue et append-only. Utiliser Kafka pour les architectures event-driven, le CDC, les pipelines temps reel, et comme backbone d'une architecture Kappa.

**Key components:**
- **Topics**: Named streams of events, partitioned for parallelism
- **Producers**: Applications that publish events to topics
- **Consumers**: Applications that read events from topics (consumer groups for load balancing)
- **Connect**: Framework for source/sink connectors (Debezium for CDC, S3 sink, BigQuery sink)
- **Schema Registry**: Schema management and evolution enforcement

```python
# Kafka producer example (Python, confluent-kafka)
from confluent_kafka import Producer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.avro import AvroSerializer

producer_config = {
    'bootstrap.servers': 'broker1:9092,broker2:9092',
    'enable.idempotence': True,         # Exactly-once producer
    'acks': 'all',                      # Wait for all replicas
    'compression.type': 'zstd',         # Compress messages
    'linger.ms': 50,                    # Batch for 50ms before sending
    'batch.size': 65536,                # 64KB batch size
}

producer = Producer(producer_config)

def produce_event(topic: str, key: str, value: dict):
    serialized_value = avro_serializer(
        value,
        SerializationContext(topic, MessageField.VALUE)
    )
    producer.produce(
        topic=topic,
        key=key,
        value=serialized_value,
        on_delivery=delivery_callback,
    )
    producer.flush()
```

### Kafka Connect for Data Integration

```json
{
    "name": "postgres-cdc-source",
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "database.hostname": "db-host",
        "database.port": "5432",
        "database.user": "replication_user",
        "database.dbname": "app_db",
        "database.server.name": "app_db",
        "table.include.list": "public.orders,public.customers",
        "plugin.name": "pgoutput",
        "slot.name": "debezium_slot",
        "publication.name": "debezium_pub",
        "topic.prefix": "cdc.app_db",
        "transforms": "route",
        "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
        "transforms.route.regex": "cdc\\.app_db\\.public\\.(.*)",
        "transforms.route.replacement": "bronze.$1"
    }
}
```

### Google Cloud Pub/Sub

**EN** — Pub/Sub is Google's fully managed messaging service. Serverless, auto-scaling, and deeply integrated with GCP. Use Pub/Sub when building on GCP and when operational simplicity outweighs the need for Kafka's advanced features (compacted topics, exactly-once, Kafka Streams).

**FR** — Pub/Sub est le service de messagerie entierement manage de Google. Serverless, auto-scaling, et profondement integre avec GCP. Utiliser Pub/Sub quand on construit sur GCP et quand la simplicite operationnelle l'emporte sur le besoin des fonctionnalites avancees de Kafka.

### Apache Flink for Stream Processing

**EN** — Flink is the leading stream processing engine. Use Flink for complex event processing, windowed aggregations, pattern detection, and streaming SQL. Flink processes events with exactly-once semantics and supports both bounded (batch) and unbounded (streaming) data.

```sql
-- Flink SQL — real-time aggregation
CREATE TABLE events (
    event_id    STRING,
    event_type  STRING,
    user_id     STRING,
    amount      DECIMAL(10, 2),
    event_time  TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '10' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'events',
    'properties.bootstrap.servers' = 'broker:9092',
    'format' = 'avro-confluent',
    'avro-confluent.url' = 'http://schema-registry:8081'
);

-- Tumbling window aggregation
SELECT
    TUMBLE_START(event_time, INTERVAL '5' MINUTE) AS window_start,
    event_type,
    COUNT(*) AS event_count,
    SUM(amount) AS total_amount
FROM events
GROUP BY
    TUMBLE(event_time, INTERVAL '5' MINUTE),
    event_type;

-- Pattern detection (Complex Event Processing)
SELECT *
FROM events
MATCH_RECOGNIZE (
    PARTITION BY user_id
    ORDER BY event_time
    MEASURES
        A.event_time AS start_time,
        C.event_time AS end_time,
        C.amount AS fraud_amount
    ONE ROW PER MATCH
    PATTERN (A B C)
    DEFINE
        A AS A.event_type = 'login_failed',
        B AS B.event_type = 'login_failed',
        C AS C.event_type = 'large_transaction' AND C.amount > 10000
) AS fraud_pattern;
```

### Streaming Platform Comparison

| Feature | Kafka | Pub/Sub | Kinesis | Redpanda |
|---|---|---|---|---|
| **Managed** | Confluent Cloud, MSK | Fully managed | Fully managed | Redpanda Cloud |
| **Ordering** | Per-partition | Per-key (ordering keys) | Per-shard | Per-partition |
| **Retention** | Configurable (unlimited) | 31 days max | 365 days max | Configurable |
| **Exactly-once** | Yes (transactional) | At-least-once | At-least-once | Yes |
| **Schema registry** | Confluent Schema Registry | N/A (use external) | Glue Schema Registry | Built-in |
| **Best for** | Event-driven architectures | GCP-native streaming | AWS-native streaming | Kafka-compatible, simpler ops |

---

## 4. Data Integration Tools

### Fivetran

**EN** — Fivetran is the leading managed EL (Extract-Load) platform. It provides 500+ pre-built connectors, automatic schema detection, incremental syncing, and data normalization. Use Fivetran for reliable, low-maintenance source extraction.

**FR** — Fivetran est la principale plateforme EL (Extract-Load) managee. Il fournit 500+ connecteurs pre-construits, la detection automatique de schema, la synchronisation incrementale, et la normalisation des donnees. Utiliser Fivetran pour une extraction source fiable et a faible maintenance.

**Best for:** Teams that want turnkey ingestion without maintaining custom connectors. Premium pricing justified by reliability and speed of implementation.

### Airbyte

**EN** — Airbyte is the leading open-source EL platform. Self-hosted or cloud-managed. 400+ connectors (community + certified). Use Airbyte when budget is constrained, custom connectors are needed, or self-hosting is preferred for data sovereignty.

**FR** — Airbyte est la principale plateforme EL open-source. Self-hosted ou manage en cloud. 400+ connecteurs (communautaires + certifies). Utiliser Airbyte quand le budget est contraint, des connecteurs custom sont necessaires, ou le self-hosting est prefere pour la souverainete des donnees.

```yaml
# Airbyte connection configuration (YAML for Octavia CLI)
connections:
  - name: postgres_to_bigquery
    source:
      name: postgres_source
      type: source-postgres
      configuration:
        host: db.example.com
        port: 5432
        database: app_db
        username: "${POSTGRES_USER}"
        password: "${POSTGRES_PASSWORD}"
        replication_method:
          method: CDC
          plugin: pgoutput
          replication_slot: airbyte_slot
          publication: airbyte_pub
    destination:
      name: bigquery_destination
      type: destination-bigquery
      configuration:
        project_id: my-project
        dataset_id: bronze
        loading_method:
          method: GCS Staging
          gcs_bucket_name: airbyte-staging
    schedule:
      schedule_type: cron
      cron_expression: "0 */6 * * *"  # Every 6 hours
    sync_mode: incremental_deduped
```

### Meltano

**EN** — Meltano is an open-source DataOps platform built on Singer taps and targets. It provides a CLI-first experience for managing EL pipelines as code. Best for teams that want full control over their EL configuration in version control.

### Sling

**EN** — Sling is a lightweight CLI tool for data movement between databases, data warehouses, and file systems. Excellent for simple database-to-warehouse replication without the overhead of a full EL platform.

### Integration Tool Comparison

| Feature | Fivetran | Airbyte | Meltano | Sling |
|---|---|---|---|---|
| **Deployment** | SaaS only | Self-hosted or Cloud | Self-hosted | CLI / Self-hosted |
| **Connectors** | 500+ (certified) | 400+ (mixed quality) | 600+ (Singer) | 30+ (database-focused) |
| **CDC support** | Yes (built-in) | Yes (Debezium) | Limited | Limited |
| **Schema detection** | Automatic | Automatic | Manual | Automatic |
| **Pricing** | Per-row or MAR | Free (OSS) / Cloud pricing | Free (OSS) | Free (OSS) |
| **Best for** | Enterprise, turnkey | Budget-conscious, custom | DataOps purists | Simple DB replication |

---

## 5. DataOps Practices

### What Is DataOps

**EN** — DataOps applies DevOps and Agile principles to data engineering. It emphasizes automation, version control, testing, monitoring, and continuous delivery for data pipelines. DataOps is not a tool — it is a set of practices.

**FR** — DataOps applique les principes DevOps et Agile a l'ingenierie des donnees. Il met l'accent sur l'automatisation, le controle de version, les tests, le monitoring, et la livraison continue pour les pipelines de donnees. DataOps n'est pas un outil — c'est un ensemble de pratiques.

### DataOps Pillars

| Pillar | Practice | Tools |
|---|---|---|
| **Version control** | All pipeline code, SQL, config in Git | GitHub, GitLab |
| **Automated testing** | Unit tests, integration tests, data quality tests | dbt tests, Great Expectations, Soda |
| **CI/CD** | Automated build, test, deploy for data pipelines | GitHub Actions, GitLab CI, dbt Cloud |
| **Monitoring** | Pipeline health, data quality, freshness, costs | Elementary, Monte Carlo, Datadog |
| **Collaboration** | Data contracts, documentation, catalogs | dbt docs, DataHub, Atlan, Select Star |
| **Incident management** | Alerting, runbooks, post-incident reviews | PagerDuty, Opsgenie, Slack |

---

## 6. CI/CD for Data Pipelines

### dbt CI/CD Pipeline

```yaml
# .github/workflows/dbt-ci.yml
name: dbt CI
on:
  pull_request:
    branches: [main]
    paths:
      - 'dbt_project/**'

concurrency:
  group: dbt-ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  dbt-ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - run: pip install dbt-bigquery sqlfluff dbt-checkpoint

      - name: SQL Linting
        run: sqlfluff lint dbt_project/models/ --fail-on-violation

      - name: dbt deps
        run: dbt deps --project-dir dbt_project

      - name: dbt compile
        run: dbt compile --project-dir dbt_project

      # Slim CI — only build and test modified models
      - name: dbt build (modified models only)
        run: |
          dbt build \
            --project-dir dbt_project \
            --select state:modified+ \
            --defer \
            --state ./prod-manifest/ \
            --target ci
        env:
          DBT_PROFILES_DIR: ./dbt_project/profiles

      - name: Generate docs
        run: dbt docs generate --project-dir dbt_project

      - name: Upload docs artifact
        uses: actions/upload-artifact@v4
        with:
          name: dbt-docs
          path: dbt_project/target/
```

### Slim CI Explained

**EN** — Slim CI compares the current PR against the production manifest (state of models in production). Only modified models and their downstream dependents (`state:modified+`) are built and tested. This dramatically reduces CI time for large dbt projects.

**FR** — Le Slim CI compare la PR actuelle contre le manifeste de production (etat des modeles en production). Seuls les modeles modifies et leurs dependants en aval (`state:modified+`) sont construits et testes. Cela reduit considerablement le temps de CI pour les grands projets dbt.

### Database Schema Migration CI/CD

**EN** — For warehouse schema changes beyond dbt (stored procedures, access policies, external tables), use migration tools:

```python
# Using sqlalchemy-migrate or Flyway-style migrations
# migrations/V001__create_bronze_schema.sql
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

GRANT USAGE ON SCHEMA bronze TO ROLE ingestion_role;
GRANT USAGE ON SCHEMA silver TO ROLE transformation_role;
GRANT USAGE ON SCHEMA gold TO ROLE analytics_role;
```

---

## 7. Data Observability

### The Five Pillars of Data Observability

| Pillar | What to Monitor | Example |
|---|---|---|
| **Freshness** | Is data arriving on time? | "orders table last updated 26 hours ago" |
| **Volume** | Is the expected amount of data present? | "Today's partition has 80% fewer rows than average" |
| **Schema** | Has the structure changed? | "Column `phone` was removed from source" |
| **Distribution** | Are values within expected ranges? | "avg(order_amount) spiked 300% today" |
| **Lineage** | Where does data come from and flow to? | "This dashboard depends on 12 upstream models" |

### Tools

| Tool | Type | Strength |
|---|---|---|
| **Elementary** | Open-source, dbt-native | Embedded in dbt, dashboards from dbt artifacts |
| **Monte Carlo** | Commercial SaaS | ML-powered anomaly detection, broad integrations |
| **Soda** | Open-source + Cloud | Data contracts, check-based validation |
| **Great Expectations** | Open-source | Programmable expectations, rich documentation |
| **Datafold** | Commercial | Data diff (compare datasets), CI integration |

### Elementary Setup (dbt-Native Observability)

```yaml
# packages.yml
packages:
  - package: elementary-data/elementary
    version: "0.16.0"

# Add to dbt_project.yml
models:
  elementary:
    +schema: elementary  # Store Elementary models in dedicated schema
```

```yaml
# Add anomaly detection tests to models
models:
  - name: mrt_finance__daily_revenue
    tests:
      - elementary.volume_anomalies:
          timestamp_column: revenue_date
          backfill_days: 30
      - elementary.freshness_anomalies:
          timestamp_column: revenue_date
          where: "revenue_date >= current_date - 7"
    columns:
      - name: total_revenue_usd
        tests:
          - elementary.column_anomalies:
              timestamp_column: revenue_date
              column_anomalies:
                - zero_count
                - zero_percent
                - average
                - standard_deviation
```

---

## 8. Cost Optimization

### Cost Optimization Strategies by Warehouse

**BigQuery:**
- Use slot-based pricing (editions) for predictable workloads over $500/month
- Require partition filters on large tables (`require_partition_filter = TRUE`)
- Set custom cost controls per project/user with quotas
- Use BI Engine for frequently accessed dashboards (reduces slot consumption)
- Monitor with `INFORMATION_SCHEMA.JOBS` and set up Cloud Billing alerts

**Snowflake:**
- Set `AUTO_SUSPEND = 60` on all warehouses (suspend after 1 minute idle)
- Use multi-cluster warehouses with `ECONOMY` scaling policy
- Create resource monitors with credit budgets per team/pipeline
- Use `QUERY_TAG` for cost attribution to teams and pipelines
- Review query history for expensive, recurring queries

**Databricks:**
- Use serverless SQL Warehouses (auto-stop, pay-per-query)
- Optimize Delta Lake files regularly (`OPTIMIZE`, `VACUUM`)
- Use spot instances for non-critical jobs (up to 90% savings)
- Monitor DBU consumption per workspace and cluster

### General Cost Optimization Checklist

- [ ] Partition all tables over 1 GB by the most common filter column (usually date)
- [ ] Cluster tables by the most frequently filtered columns
- [ ] Use incremental processing instead of full refresh where possible
- [ ] Set query timeouts to prevent runaway queries (e.g., 30 minutes max)
- [ ] Implement warehouse auto-suspend (Snowflake) or use serverless (BigQuery, Redshift)
- [ ] Monitor and alert on cost anomalies weekly
- [ ] Review and drop unused tables and pipelines quarterly
- [ ] Use reserved capacity or committed use discounts for predictable base load
- [ ] Implement column pruning: `SELECT *` is the enemy of cost-efficient warehousing
- [ ] Compress data at rest (Parquet, ORC, or warehouse-native columnar formats)

**FR** — L'optimisation des couts est un processus continu, pas un projet ponctuel. Mettre en place des alertes de budget, des revues mensuelles des couts par pipeline, et une culture d'efficacite des requetes dans l'equipe.

**EN** — Cost optimization is a continuous process, not a one-time project. Establish budget alerts, monthly cost reviews per pipeline, and a culture of query efficiency across the team. The best cost optimization is not running unnecessary queries in the first place.

---

## 9. Architecture Decision Records (ADR) for Data Infrastructure

**EN** — Document major infrastructure decisions using Architecture Decision Records. These records explain the context, options considered, decision made, and consequences. They prevent re-litigating decisions and onboard new team members.

```markdown
# ADR-003: Adopt Apache Iceberg as the Open Table Format

## Status
Accepted (2025-03-15)

## Context
We need an open table format for our data lakehouse to provide ACID transactions,
time travel, and schema evolution on S3 storage. Our query engines include Spark,
Trino, and Snowflake.

## Decision
Adopt Apache Iceberg as the standard open table format.

## Rationale
- Broadest engine support (Spark, Flink, Trino, Snowflake, BigQuery, Databricks)
- Superior partition evolution (no data rewrite needed)
- Hidden partitioning reduces user errors
- Delta Lake UniForm provides Iceberg read compatibility as a fallback

## Consequences
- All new bronze/silver tables will use Iceberg format
- Existing Delta tables will be migrated over 6 months
- Team training on Iceberg maintenance operations (compaction, snapshot expiry)
```

**FR** — Documenter les decisions d'infrastructure majeures avec des ADRs. Ces documents expliquent le contexte, les options evaluees, la decision prise, et les consequences. Ils empechent de remettre en question les decisions et facilitent l'onboarding des nouveaux membres.
