# Data Transformation — dbt Deep Dive, SQL at Scale & Incremental Processing

## Introduction

**FR** — Ce guide de reference couvre la transformation de donnees moderne : dbt en profondeur (modeles, tests, documentation, snapshots, seeds, metriques), les transformations SQL a grande echelle, le traitement incremental, les vues materialisees, et les bonnes pratiques de modelisation. La transformation est le coeur de la plateforme de donnees — c'est la qu'on passe des donnees brutes aux insights metier.

**EN** — This reference guide covers modern data transformation: dbt in depth (models, tests, documentation, snapshots, seeds, metrics), SQL transformations at scale, incremental processing, materialized views, and modeling best practices. Transformation is the heart of the data platform — it is where raw data becomes business insight.

---

## 1. dbt Fundamentals

### What dbt Is (and Is Not)

**EN** — dbt (data build tool) is a SQL-first transformation framework that brings software engineering practices to analytics code. It compiles SQL models, manages dependencies, runs tests, and generates documentation. dbt does NOT extract or load data — it is the "T" in ELT.

**FR** — dbt (data build tool) est un framework de transformation SQL-first qui apporte les pratiques d'ingenierie logicielle au code analytique. Il compile les modeles SQL, gere les dependances, execute les tests, et genere la documentation. dbt ne fait PAS l'extraction ou le chargement — c'est le "T" dans ELT.

### Project Structure

Adopt a layered structure that mirrors the medallion architecture:

```
dbt_project/
  models/
    staging/           # 1:1 with source tables (bronze -> silver entry)
      _staging.yml     # Source definitions and tests
      stg_crm__contacts.sql
      stg_crm__orders.sql
      stg_payments__transactions.sql
    intermediate/      # Business logic, joins, complex transforms
      int_orders__enriched.sql
      int_contacts__deduplicated.sql
    marts/             # Gold layer — consumption-ready models
      marketing/
        mrt_marketing__daily_metrics.sql
        mrt_marketing__campaign_performance.sql
      finance/
        mrt_finance__monthly_revenue.sql
        _finance__models.yml
  tests/
    generic/
      test_positive_values.sql
    singular/
      assert_revenue_balance.sql
  macros/
    generate_schema_name.sql
    cents_to_dollars.sql
  seeds/
    country_codes.csv
    currency_exchange_rates.csv
  snapshots/
    snp_crm__contacts.sql
  analyses/
    ad_hoc_revenue_investigation.sql
```

### Naming Conventions

**EN** — Adopt consistent naming conventions to make models self-documenting. Prefix models by layer and source system.

| Layer | Prefix | Example | Description |
|---|---|---|---|
| Staging | `stg_` | `stg_crm__contacts` | 1:1 source mapping, minimal transforms |
| Intermediate | `int_` | `int_orders__enriched` | Business joins and logic |
| Marts | `mrt_` | `mrt_finance__revenue` | Consumption-ready aggregations |
| Snapshots | `snp_` | `snp_crm__contacts` | SCD Type 2 historical tracking |

**FR** — Adopter des conventions de nommage coherentes pour rendre les modeles auto-documentants. Prefixer les modeles par couche et systeme source. Utiliser le double underscore `__` pour separer le systeme source de l'entite.

---

## 2. dbt Models in Depth

### Staging Models

**EN** — Staging models are the entry point from raw sources. Perform only: renaming, type casting, basic filtering (remove test/internal records), and adding computed columns for downstream use. One staging model per source table.

```sql
-- models/staging/stg_crm__contacts.sql
WITH source AS (
    SELECT * FROM {{ source('crm', 'raw_contacts') }}
),

renamed AS (
    SELECT
        id                          AS contact_id,
        LOWER(TRIM(email))          AS email,
        first_name || ' ' || last_name AS full_name,
        UPPER(country_code)         AS country_code,
        CAST(created_at AS TIMESTAMP) AS created_at,
        CAST(updated_at AS TIMESTAMP) AS updated_at,
        CASE WHEN is_deleted = 'true' THEN TRUE ELSE FALSE END AS is_deleted
    FROM source
    WHERE id IS NOT NULL  -- Filter corrupt records
)

SELECT * FROM renamed
```

### Intermediate Models

**EN** — Intermediate models encode business logic: joins between staging models, deduplication, enrichment, and complex calculations. Keep them modular — each intermediate model should solve one specific problem.

**FR** — Les modeles intermediaires encodent la logique metier : jointures entre modeles staging, deduplication, enrichissement, et calculs complexes. Les garder modulaires — chaque modele intermediaire doit resoudre un probleme specifique.

```sql
-- models/intermediate/int_orders__enriched.sql
WITH orders AS (
    SELECT * FROM {{ ref('stg_shopify__orders') }}
),

contacts AS (
    SELECT * FROM {{ ref('stg_crm__contacts') }}
),

exchange_rates AS (
    SELECT * FROM {{ ref('stg_finance__exchange_rates') }}
)

SELECT
    o.order_id,
    o.contact_id,
    c.email,
    c.country_code,
    o.order_date,
    o.currency,
    o.amount_local,
    o.amount_local * COALESCE(er.rate_to_usd, 1.0) AS amount_usd,
    o.status
FROM orders o
LEFT JOIN contacts c ON o.contact_id = c.contact_id
LEFT JOIN exchange_rates er
    ON o.currency = er.source_currency
    AND o.order_date = er.rate_date
```

### Mart Models

**EN** — Mart models are the gold layer: pre-aggregated, denormalized, and optimized for consumption. Each mart serves a specific business domain or use case. Use `materialized='table'` for frequently queried marts with stable data.

```sql
-- models/marts/finance/mrt_finance__monthly_revenue.sql
{{
    config(
        materialized='table',
        partition_by={'field': 'revenue_month', 'data_type': 'date'},
        cluster_by=['country_code', 'product_category']
    )
}}

SELECT
    DATE_TRUNC(order_date, MONTH) AS revenue_month,
    country_code,
    product_category,
    COUNT(DISTINCT order_id)      AS order_count,
    COUNT(DISTINCT contact_id)    AS unique_customers,
    SUM(amount_usd)               AS total_revenue_usd,
    AVG(amount_usd)               AS avg_order_value_usd
FROM {{ ref('int_orders__enriched') }}
WHERE status = 'completed'
GROUP BY 1, 2, 3
```

---

## 3. dbt Testing

### Built-in Generic Tests

**EN** — Apply generic tests to every model. These are non-negotiable for production models.

```yaml
# models/staging/_staging.yml
version: 2

models:
  - name: stg_crm__contacts
    description: "Cleaned CRM contacts — one row per contact"
    columns:
      - name: contact_id
        description: "Primary key"
        tests:
          - unique
          - not_null
      - name: email
        description: "Contact email, lowercased and trimmed"
        tests:
          - not_null
          - unique
      - name: country_code
        description: "ISO 3166-1 alpha-2 country code"
        tests:
          - not_null
          - accepted_values:
              values: ['US', 'GB', 'FR', 'DE', 'CA', 'AU', 'JP']
              config:
                severity: warn  # Warn, don't fail, for unexpected countries
```

### Custom Generic Tests

```sql
-- tests/generic/test_positive_values.sql
{% test positive_values(model, column_name) %}
SELECT {{ column_name }}
FROM {{ model }}
WHERE {{ column_name }} < 0
{% endtest %}
```

Usage in YAML:
```yaml
- name: amount_usd
  tests:
    - positive_values
```

### Singular Tests

**EN** — Singular tests validate business rules that span multiple models or complex conditions.

**FR** — Les tests singuliers valident des regles metier qui traversent plusieurs modeles ou des conditions complexes.

```sql
-- tests/singular/assert_revenue_balance.sql
-- Verify that gold revenue matches silver order totals
WITH gold AS (
    SELECT SUM(total_revenue_usd) AS gold_total
    FROM {{ ref('mrt_finance__monthly_revenue') }}
    WHERE revenue_month = '2025-01-01'
),
silver AS (
    SELECT SUM(amount_usd) AS silver_total
    FROM {{ ref('int_orders__enriched') }}
    WHERE DATE_TRUNC(order_date, MONTH) = '2025-01-01'
    AND status = 'completed'
)
SELECT *
FROM gold
CROSS JOIN silver
WHERE ABS(gold_total - silver_total) > 0.01  -- Tolerance for rounding
```

### Data Quality with dbt-expectations

**EN** — Use the `dbt-expectations` package for advanced data quality tests inspired by Great Expectations:

```yaml
- name: amount_usd
  tests:
    - dbt_expectations.expect_column_values_to_be_between:
        min_value: 0
        max_value: 1000000
        row_condition: "status = 'completed'"
    - dbt_expectations.expect_column_mean_to_be_between:
        min_value: 10
        max_value: 500
```

---

## 4. dbt Documentation

### Model Documentation

**EN** — Document every model and column in YAML files. Use `dbt docs generate` and `dbt docs serve` to produce an interactive documentation site with a DAG visualization. Documentation is not optional — it is the primary way new team members understand the data platform.

**FR** — Documenter chaque modele et colonne dans les fichiers YAML. Utiliser `dbt docs generate` et `dbt docs serve` pour produire un site de documentation interactif avec une visualisation DAG. La documentation n'est pas optionnelle — c'est le moyen principal pour les nouveaux membres de comprendre la plateforme.

```yaml
models:
  - name: mrt_finance__monthly_revenue
    description: >
      Monthly revenue aggregation by country and product category.
      Source of truth for the finance team's monthly reporting.
      Refreshed daily. SLA: available by 08:00 UTC.
    meta:
      owner: data-engineering
      sla: "08:00 UTC daily"
      pii: false
    columns:
      - name: revenue_month
        description: "First day of the month (DATE)"
      - name: total_revenue_usd
        description: "Sum of completed order revenue in USD, converted at daily exchange rates"
```

### Doc Blocks for Reusable Descriptions

```markdown
{# docs/column_descriptions.md #}

{% docs contact_id %}
Unique identifier for a contact in the CRM system.
Sourced from the `id` field in the raw CRM export.
Format: UUID v4.
{% enddocs %}
```

Reference in YAML: `description: '{{ doc("contact_id") }}'`

---

## 5. dbt Snapshots (SCD Type 2)

**EN** — Snapshots track how records change over time using Slowly Changing Dimension Type 2 (SCD2). Use snapshots to capture the history of mutable source data (customer status changes, pricing updates, employee records).

**FR** — Les snapshots suivent comment les enregistrements changent au fil du temps via Slowly Changing Dimension Type 2 (SCD2). Utiliser les snapshots pour capturer l'historique des donnees sources mutables (changements de statut client, mises a jour de prix, dossiers employes).

```sql
-- snapshots/snp_crm__contacts.sql
{% snapshot snp_crm__contacts %}

{{
    config(
        target_schema='snapshots',
        unique_key='contact_id',
        strategy='timestamp',
        updated_at='updated_at',
        invalidate_hard_deletes=True
    )
}}

SELECT * FROM {{ source('crm', 'raw_contacts') }}

{% endsnapshot %}
```

**Result:** Each row gets `dbt_valid_from` and `dbt_valid_to` columns. Current records have `dbt_valid_to = NULL`. Historical records have the full validity range.

### Querying Snapshots

```sql
-- Current state
SELECT * FROM {{ ref('snp_crm__contacts') }}
WHERE dbt_valid_to IS NULL;

-- State at a specific point in time
SELECT * FROM {{ ref('snp_crm__contacts') }}
WHERE '2025-06-15' BETWEEN dbt_valid_from AND COALESCE(dbt_valid_to, '9999-12-31');
```

---

## 6. dbt Seeds and Metrics

### Seeds

**EN** — Seeds are CSV files version-controlled in the dbt project. Use seeds for small, static reference data: country codes, currency mappings, manual category overrides. Never use seeds for large or frequently changing data.

```csv
# seeds/country_codes.csv
code,name,region
US,United States,North America
GB,United Kingdom,Europe
FR,France,Europe
DE,Germany,Europe
```

```bash
dbt seed  # Loads CSVs into the warehouse
```

### dbt Metrics (Semantic Layer)

**EN** — Define business metrics as code using the dbt Semantic Layer (MetricFlow). This ensures a single source of truth for metric definitions across all consumption tools (BI, notebooks, APIs).

**FR** — Definir les metriques metier en tant que code via le Semantic Layer dbt (MetricFlow). Cela garantit une source unique de verite pour les definitions de metriques a travers tous les outils de consommation (BI, notebooks, APIs).

```yaml
# models/marts/finance/_finance__semantic.yml
semantic_models:
  - name: orders
    defaults:
      agg_time_dimension: order_date
    model: ref('int_orders__enriched')
    entities:
      - name: order_id
        type: primary
      - name: contact_id
        type: foreign
    dimensions:
      - name: country_code
        type: categorical
      - name: order_date
        type: time
        type_params:
          time_granularity: day
    measures:
      - name: total_revenue
        agg: sum
        expr: amount_usd
      - name: order_count
        agg: count_distinct
        expr: order_id

metrics:
  - name: monthly_revenue
    type: simple
    label: "Monthly Revenue (USD)"
    description: "Total completed order revenue in USD"
    type_params:
      measure: total_revenue
    filter: |
      {{ Dimension('order__status') }} = 'completed'
```

---

## 7. Incremental Processing

### Why Incremental

**EN** — Full table refreshes reprocess all historical data on every run. For large tables (millions+ rows), this wastes compute, costs money, and increases pipeline latency. Incremental models process only new or changed records.

**FR** — Les rafraichissements complets retraitent toutes les donnees historiques a chaque execution. Pour les grandes tables (millions+ de lignes), cela gaspille du compute, coute de l'argent et augmente la latence du pipeline. Les modeles incrementaux traitent uniquement les enregistrements nouveaux ou modifies.

### dbt Incremental Strategies

| Strategy | How It Works | Best For | Warehouse |
|---|---|---|---|
| `append` | INSERT new rows only | Immutable event streams | All |
| `delete+insert` | DELETE matching partition, then INSERT | Partition-based updates | BigQuery, Redshift |
| `merge` | MERGE/upsert by unique key | Mutable dimension tables | Snowflake, BigQuery, Databricks |
| `insert_overwrite` | Overwrite entire partitions | Large partitioned fact tables | BigQuery, Spark |

### Incremental Model Example

```sql
{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='event_id',
        partition_by={'field': 'event_date', 'data_type': 'date'},
        cluster_by=['event_type'],
        on_schema_change='append_new_columns'
    )
}}

SELECT
    event_id,
    event_type,
    user_id,
    event_properties,
    DATE(event_timestamp) AS event_date,
    event_timestamp,
    _ingested_at
FROM {{ source('bronze', 'raw_events') }}

{% if is_incremental() %}
WHERE _ingested_at > (
    SELECT MAX(_ingested_at) FROM {{ this }}
)
{% endif %}
```

### Incremental Pitfalls and Solutions

| Pitfall | Impact | Solution |
|---|---|---|
| Late-arriving data | Missed records | Use a lookback window: `_ingested_at > MAX(_ingested_at) - INTERVAL 3 HOUR` |
| Non-unique merge key | Cartesian explosion on MERGE | Ensure unique key is truly unique; deduplicate in a CTE before merge |
| Schema changes | Pipeline failure | Set `on_schema_change='append_new_columns'` or `'sync_all_columns'` |
| Accumulated drift | Gradual data quality degradation | Schedule periodic full refresh (`dbt run --full-refresh -s model`) weekly/monthly |

---

## 8. SQL Transformations at Scale

### Window Functions for Analytics

```sql
-- Running total and moving average
SELECT
    order_date,
    daily_revenue,
    SUM(daily_revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_revenue,
    AVG(daily_revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS revenue_7d_moving_avg
FROM {{ ref('mrt_finance__daily_revenue') }}
```

### Efficient Joins at Scale

**EN** — In cloud warehouses, join performance depends on data distribution and clustering. Follow these rules:

- Always filter before joining (push predicates down)
- Join on clustered/partitioned columns when possible
- Use `LEFT JOIN` over `FULL OUTER JOIN` unless truly needed
- Avoid joining large tables to large tables without partition pruning
- Use semi-joins (`WHERE EXISTS`) instead of `INNER JOIN` when only filtering

**FR** — Dans les entrepots cloud, la performance des jointures depend de la distribution et du clustering des donnees. Filtrer avant de joindre, joindre sur les colonnes clusterees/partitionnees, et utiliser des semi-jointures quand on filtre seulement.

### Materialized Views

**EN** — Materialized views pre-compute query results and refresh automatically (or on schedule). Use them for frequently queried aggregations that do not need the full flexibility of dbt models.

```sql
-- BigQuery materialized view
CREATE MATERIALIZED VIEW gold.mv_daily_revenue
PARTITION BY revenue_date
CLUSTER BY country_code
AS
SELECT
    DATE(order_date) AS revenue_date,
    country_code,
    SUM(amount_usd) AS total_revenue,
    COUNT(*) AS order_count
FROM silver.orders
WHERE status = 'completed'
GROUP BY 1, 2;
```

**Snowflake:**
```sql
CREATE MATERIALIZED VIEW gold.mv_daily_revenue AS
SELECT
    DATE_TRUNC('day', order_date) AS revenue_date,
    country_code,
    SUM(amount_usd) AS total_revenue,
    COUNT(*) AS order_count
FROM silver.orders
WHERE status = 'completed'
GROUP BY 1, 2;
```

---

## 9. SQL Linting with sqlfluff

**EN** — Enforce consistent SQL style across the team with sqlfluff. Run it in CI to prevent style drift.

**FR** — Appliquer un style SQL coherent dans toute l'equipe avec sqlfluff. L'executer en CI pour prevenir la derive stylistique.

```yaml
# .sqlfluff
[sqlfluff]
dialect = bigquery
templater = dbt
max_line_length = 120

[sqlfluff:rules:capitalisation.keywords]
capitalisation_policy = upper

[sqlfluff:rules:capitalisation.functions]
capitalisation_policy = upper

[sqlfluff:rules:layout.long_lines]
ignore_comment_lines = True
```

```bash
# Lint all models
sqlfluff lint models/

# Fix auto-fixable issues
sqlfluff fix models/

# CI command — fail on any violation
sqlfluff lint models/ --fail-on-violation
```

---

## 10. Data Modeling Best Practices

### Star Schema vs One Big Table (OBT)

| Approach | Pros | Cons | Best For |
|---|---|---|---|
| **Star Schema** | Normalized, efficient storage, clear relationships | Requires joins at query time | Complex analytics, multiple consumption patterns |
| **One Big Table** | No joins needed, simple queries, fast for BI tools | Redundant data, larger storage | Single-purpose dashboards, self-serve analytics |

**EN** — In modern cloud warehouses, favor OBT for mart-level models when the primary consumer is a BI tool. Use star schemas when the same dimensions serve multiple fact tables or when storage costs are a concern.

**FR** — Dans les entrepots cloud modernes, privilegier l'OBT pour les modeles de type mart quand le consommateur principal est un outil BI. Utiliser les schemas en etoile quand les memes dimensions servent plusieurs tables de faits ou quand les couts de stockage sont une preoccupation.

### Surrogate Keys

**EN** — Generate deterministic surrogate keys from natural keys using hashing. This ensures idempotency and avoids sequence-based keys that differ across environments.

```sql
-- Using dbt_utils
SELECT
    {{ dbt_utils.generate_surrogate_key(['source_system', 'source_id']) }} AS sk_customer,
    source_system,
    source_id,
    customer_name
FROM {{ ref('stg_crm__customers') }}
```

### Slowly Changing Dimensions

| SCD Type | Description | Implementation |
|---|---|---|
| **Type 1** | Overwrite current value | dbt incremental with `merge` |
| **Type 2** | Track full history with valid_from/valid_to | dbt `snapshot` |
| **Type 3** | Track current and previous value only | Add `previous_*` columns |

**FR** — Le Type 2 (via dbt snapshots) est le plus courant pour l'audit et l'analyse historique. Le Type 1 suffit quand l'historique n'a pas de valeur metier.
