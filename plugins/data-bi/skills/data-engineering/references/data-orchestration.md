# Data Orchestration — Airflow, Dagster, Prefect, Scheduling & Data SLAs

## Introduction

**FR** — Ce guide de reference couvre l'orchestration des pipelines de donnees modernes : Airflow en profondeur (DAGs, operateurs, sensors, TaskFlow API), Dagster (software-defined assets), Prefect (flows dynamiques), Mage, la gestion des dependances, le scheduling, le monitoring, les alertes, et les SLAs de donnees. L'orchestrateur est le systeme nerveux de la plateforme de donnees — il coordonne l'execution, gere les pannes, et garantit la fraicheur des donnees.

**EN** — This reference guide covers modern data pipeline orchestration: Airflow in depth (DAGs, operators, sensors, TaskFlow API), Dagster (software-defined assets), Prefect (dynamic flows), Mage, dependency management, scheduling, monitoring, alerting, and data SLAs. The orchestrator is the nervous system of the data platform — it coordinates execution, manages failures, and guarantees data freshness.

---

## 1. Apache Airflow Deep Dive

### Architecture Overview

**EN** — Airflow is the industry-standard orchestrator for data pipelines. It defines workflows as Directed Acyclic Graphs (DAGs) of tasks, with a scheduler, executor, metadata database, and web UI.

**FR** — Airflow est l'orchestrateur standard de l'industrie pour les pipelines de donnees. Il definit les workflows comme des graphes acycliques diriges (DAGs) de taches, avec un scheduler, un executeur, une base de metadonnees et une interface web.

**Core components:**
- **Scheduler**: Monitors DAGs, triggers task instances based on schedule and dependencies
- **Executor**: Runs tasks (LocalExecutor for dev, CeleryExecutor/KubernetesExecutor for production)
- **Metadata DB**: PostgreSQL storing DAG state, task history, variables, connections
- **Web Server**: UI for monitoring, triggering, and debugging DAGs
- **Workers**: Processes that execute task instances (in CeleryExecutor or KubernetesExecutor)

### DAG Design Best Practices

```python
# dags/elt_crm_pipeline.py
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator

default_args = {
    'owner': 'data-engineering',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
    'execution_timeout': timedelta(hours=2),
    'on_failure_callback': alert_on_failure,  # Slack/PagerDuty alert
    'sla': timedelta(hours=3),               # SLA: complete within 3 hours
}

@dag(
    dag_id='elt_crm_pipeline',
    schedule='0 6 * * *',          # Daily at 06:00 UTC
    start_date=datetime(2025, 1, 1),
    catchup=False,                  # Don't backfill on deploy
    max_active_runs=1,              # Prevent overlapping runs
    tags=['elt', 'crm', 'daily'],
    default_args=default_args,
    doc_md="""
    ## ELT CRM Pipeline
    Extracts CRM data via Fivetran, transforms with dbt, validates quality.
    **SLA:** Dashboard ready by 09:00 UTC.
    **Owner:** data-engineering@company.com
    """
)
def elt_crm_pipeline():
    # Task definitions here
    pass

elt_crm_pipeline()
```

### TaskFlow API (Modern Python Syntax)

**EN** — The TaskFlow API (Airflow 2.x+) uses Python decorators for cleaner DAG definitions. Prefer TaskFlow over classic operator instantiation for Python-based tasks.

**FR** — L'API TaskFlow (Airflow 2.x+) utilise les decorateurs Python pour des definitions de DAG plus propres. Privilegier TaskFlow par rapport a l'instanciation classique d'operateurs pour les taches basees sur Python.

```python
@dag(
    dag_id='elt_crm_pipeline_v2',
    schedule='0 6 * * *',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['elt', 'crm'],
    default_args=default_args,
)
def elt_crm_pipeline_v2():

    @task
    def check_source_freshness():
        """Verify source data has been updated in the last 24 hours."""
        from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
        hook = BigQueryHook()
        result = hook.get_first(
            "SELECT MAX(_ingested_at) FROM bronze.crm_contacts"
        )
        max_ingested = result[0]
        if (datetime.utcnow() - max_ingested).total_seconds() > 86400:
            raise ValueError(f"Source data is stale: last ingested at {max_ingested}")
        return str(max_ingested)

    @task
    def trigger_fivetran_sync():
        """Trigger Fivetran connector sync and wait for completion."""
        from airflow.providers.fivetran.operators.fivetran import FivetranOperator
        # Fivetran sync logic
        return "sync_completed"

    @task
    def run_dbt_staging():
        """Run dbt staging models for CRM sources."""
        import subprocess
        result = subprocess.run(
            ['dbt', 'run', '--select', 'staging.crm'],
            capture_output=True, text=True, check=True
        )
        return result.stdout

    @task
    def run_dbt_marts():
        """Run dbt mart models that depend on CRM staging."""
        import subprocess
        result = subprocess.run(
            ['dbt', 'run', '--select', 'marts.marketing'],
            capture_output=True, text=True, check=True
        )
        return result.stdout

    @task
    def run_dbt_tests():
        """Run dbt tests on all modified models."""
        import subprocess
        result = subprocess.run(
            ['dbt', 'test', '--select', 'staging.crm marts.marketing'],
            capture_output=True, text=True, check=True
        )
        return result.stdout

    @task
    def notify_success(test_results: str):
        """Notify Slack channel on successful completion."""
        # Slack notification logic
        pass

    # Define dependencies
    freshness = check_source_freshness()
    sync = trigger_fivetran_sync()
    staging = run_dbt_staging()
    marts = run_dbt_marts()
    tests = run_dbt_tests()
    notify = notify_success(tests)

    freshness >> sync >> staging >> marts >> tests >> notify

elt_crm_pipeline_v2()
```

### Key Operators

| Operator | Purpose | Example Use Case |
|---|---|---|
| `BashOperator` | Run shell commands | Trigger dbt CLI, run scripts |
| `PythonOperator` / `@task` | Run Python functions | Custom transformations, API calls |
| `BigQueryInsertJobOperator` | Execute BigQuery SQL | Run SQL transformations |
| `SnowflakeOperator` | Execute Snowflake SQL | Run warehouse queries |
| `DbtCloudRunJobOperator` | Trigger dbt Cloud job | Managed dbt execution |
| `FivetranOperator` | Trigger Fivetran sync | Source extraction |
| `S3ToGCSOperator` | Transfer files between clouds | Cross-cloud data movement |
| `KubernetesPodOperator` | Run any container | Isolated, resource-controlled tasks |

### Sensors

**EN** — Sensors wait for an external condition to be met before proceeding. Use `mode='reschedule'` to free worker slots during waiting (instead of `mode='poke'` which holds a worker slot).

**FR** — Les sensors attendent qu'une condition externe soit remplie avant de continuer. Utiliser `mode='reschedule'` pour liberer les slots de worker pendant l'attente.

```python
from airflow.providers.google.cloud.sensors.bigquery import BigQueryTableExistenceSensor
from airflow.sensors.external_task import ExternalTaskSensor

# Wait for an upstream DAG to complete
wait_for_ingestion = ExternalTaskSensor(
    task_id='wait_for_ingestion',
    external_dag_id='ingest_crm_data',
    external_task_id=None,        # Wait for entire DAG
    mode='reschedule',            # Don't block a worker slot
    timeout=7200,                 # Timeout after 2 hours
    poke_interval=300,            # Check every 5 minutes
    allowed_states=['success'],
)

# Wait for a table partition to exist
wait_for_partition = BigQueryTableExistenceSensor(
    task_id='wait_for_partition',
    project_id='my-project',
    dataset_id='bronze',
    table_id='events$20250115',   # Specific partition
    mode='reschedule',
    timeout=3600,
)
```

### Managed Airflow Options

| Service | Cloud | Key Features |
|---|---|---|
| **MWAA** | AWS | Managed Airflow on AWS, integrated with S3, Redshift, Glue |
| **Cloud Composer** | GCP | Managed Airflow on GCP, integrated with BigQuery, GCS |
| **Astronomer** | Multi-cloud | Enterprise Airflow platform, Astro CLI for local dev |

**EN** — Prefer managed Airflow over self-hosted unless the organization has strong Kubernetes expertise and specific customization needs. Managed services handle upgrades, scaling, and high availability.

**FR** — Privilegier Airflow manage plutot que self-hosted sauf si l'organisation a une forte expertise Kubernetes et des besoins de personnalisation specifiques.

---

## 2. Dagster — Software-Defined Assets

### Paradigm Shift: Assets Over Tasks

**EN** — Dagster inverts the orchestration model: instead of defining tasks that produce side effects, define assets (data products) and let Dagster determine how to build them. This is the "asset-centric" approach — each asset knows its dependencies, materialization logic, and metadata.

**FR** — Dagster inverse le modele d'orchestration : au lieu de definir des taches qui produisent des effets de bord, definir des assets (produits de donnees) et laisser Dagster determiner comment les construire. C'est l'approche "asset-centric" — chaque asset connait ses dependances, sa logique de materialisation et ses metadonnees.

```python
# assets/crm_pipeline.py
from dagster import asset, AssetIn, MaterializeResult, MetadataValue
from dagster_dbt import DbtCliResource, dbt_assets

@asset(
    group_name="ingestion",
    description="Raw CRM contacts loaded from Fivetran",
    metadata={"owner": "data-engineering", "sla": "06:00 UTC"},
    compute_kind="fivetran",
)
def raw_crm_contacts(fivetran: FivetranResource) -> MaterializeResult:
    """Trigger Fivetran sync and return sync metadata."""
    sync_result = fivetran.sync_and_poll(connector_id="crm_connector")
    return MaterializeResult(
        metadata={
            "rows_synced": MetadataValue.int(sync_result.rows_synced),
            "sync_duration_seconds": MetadataValue.float(sync_result.duration),
        }
    )

@asset(
    group_name="transformation",
    description="Cleaned and deduplicated CRM contacts",
    ins={"raw_contacts": AssetIn("raw_crm_contacts")},
    compute_kind="dbt",
)
def silver_crm_contacts(dbt: DbtCliResource, raw_contacts):
    """Run dbt model for silver CRM contacts."""
    dbt_result = dbt.cli(["run", "--select", "stg_crm__contacts"]).wait()
    return MaterializeResult(
        metadata={
            "row_count": MetadataValue.int(get_row_count("silver.crm_contacts")),
        }
    )
```

### Dagster Advantages

| Feature | Benefit |
|---|---|---|
| **Software-defined assets** | Declare what data should exist, not how to orchestrate tasks |
| **Built-in lineage** | Automatic dependency graph from asset definitions |
| **Type system** | Strong typing for inputs/outputs, catches errors early |
| **Partitions** | First-class support for time-partitioned and key-partitioned assets |
| **Freshness policies** | Declarative SLAs: "this asset should never be more than 6 hours old" |
| **Dagster+ (Cloud)** | Managed service with branch deployments and insights |

### Dagster Partitions

```python
from dagster import asset, DailyPartitionsDefinition

daily_partitions = DailyPartitionsDefinition(start_date="2025-01-01")

@asset(
    partitions_def=daily_partitions,
    group_name="transformation",
)
def daily_events(context):
    """Process events for a single day partition."""
    partition_date = context.partition_key  # "2025-01-15"
    df = read_events_for_date(partition_date)
    transformed = transform_events(df)
    write_to_silver(transformed, partition_date)

    return MaterializeResult(
        metadata={"row_count": MetadataValue.int(len(transformed))}
    )
```

### Dagster Freshness Policies

```python
from dagster import asset, FreshnessPolicy

@asset(
    freshness_policy=FreshnessPolicy(
        maximum_lag_minutes=360,       # Must be refreshed within 6 hours
        cron_schedule="0 8 * * *",     # Expected refresh by 08:00 UTC
    ),
    auto_materialize_policy=AutoMaterializePolicy.eager(),
)
def gold_marketing_metrics():
    """Marketing metrics with a 6-hour freshness SLA."""
    pass
```

---

## 3. Prefect

### Flow Design

**EN** — Prefect uses Python-native flows and tasks with minimal boilerplate. Flows are regular Python functions decorated with `@flow`. Prefect excels at dynamic workflows where the task graph is determined at runtime.

**FR** — Prefect utilise des flows et taches natifs Python avec un minimum de boilerplate. Les flows sont des fonctions Python regulieres decorees avec `@flow`. Prefect excelle dans les workflows dynamiques ou le graphe de taches est determine a l'execution.

```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(
    retries=3,
    retry_delay_seconds=[60, 300, 900],  # 1min, 5min, 15min
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=1),
    tags=["ingestion", "crm"],
)
def extract_crm_data(date: str) -> dict:
    """Extract CRM data for a given date."""
    # Extraction logic
    return {"rows": 1500, "date": date}

@task(retries=2, tags=["transformation"])
def transform_contacts(raw_data: dict) -> dict:
    """Clean and transform CRM contacts."""
    # Transformation logic
    return {"rows_cleaned": 1480}

@task(tags=["loading"])
def load_to_warehouse(transformed_data: dict) -> None:
    """Load transformed data to the warehouse."""
    # Loading logic
    pass

@flow(
    name="ELT CRM Pipeline",
    description="Daily CRM data pipeline",
    retries=1,
    log_prints=True,
)
def elt_crm_pipeline(date: str):
    raw = extract_crm_data(date)
    transformed = transform_contacts(raw)
    load_to_warehouse(transformed)
    print(f"Pipeline completed for {date}")

# Dynamic flow — process multiple sources in parallel
@flow(name="Multi-Source Ingestion")
def multi_source_pipeline(date: str, sources: list[str]):
    futures = []
    for source in sources:
        future = extract_crm_data.submit(date)  # Run in parallel
        futures.append(future)

    results = [f.result() for f in futures]
    # Continue with merged results
```

### Prefect vs Airflow Comparison

| Feature | Airflow | Prefect |
|---|---|---|
| **DAG definition** | Static (parsed at import time) | Dynamic (built at runtime) |
| **Configuration** | Airflow Variables, Connections | Prefect Blocks, Variables |
| **Scheduling** | Cron, timetables | Cron, intervals, RRULE |
| **Retry logic** | Per-task, basic backoff | Per-task, custom delay sequences |
| **Caching** | Custom via XCom | Built-in result caching |
| **UI** | Mature, complex | Clean, modern |
| **Community** | Massive, battle-tested | Growing, Python-native |

---

## 4. Scheduling and Dependency Management

### Scheduling Strategies

| Strategy | Use Case | Implementation |
|---|---|---|
| **Cron-based** | Regular intervals (daily, hourly) | `schedule='0 6 * * *'` |
| **Event-driven** | React to data arrival | Sensors (Airflow), triggers (Dagster/Prefect) |
| **Data-aware** | Run when upstream data is ready | `ExternalTaskSensor`, Dagster asset deps |
| **Manual trigger** | Ad-hoc runs, backfills | API trigger, UI button |

### Cross-DAG Dependencies

**EN** — When pipelines depend on other pipelines, use explicit dependency mechanisms rather than timing assumptions. Never rely on "DAG A finishes at 6 AM so DAG B starts at 7 AM."

**FR** — Quand des pipelines dependent d'autres pipelines, utiliser des mecanismes de dependance explicites plutot que des hypotheses de timing. Ne jamais compter sur "le DAG A finit a 6h donc le DAG B demarre a 7h."

**Airflow approaches:**
```python
# Option 1: ExternalTaskSensor (pull-based)
wait_for_ingestion = ExternalTaskSensor(
    task_id='wait_for_ingestion',
    external_dag_id='ingest_pipeline',
    mode='reschedule',
    timeout=3600,
)

# Option 2: TriggerDagRunOperator (push-based)
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

trigger_transform = TriggerDagRunOperator(
    task_id='trigger_transform',
    trigger_dag_id='transform_pipeline',
    wait_for_completion=True,
    poke_interval=60,
)

# Option 3: Dataset-aware scheduling (Airflow 2.4+)
from airflow.datasets import Dataset

crm_dataset = Dataset("bigquery://project/bronze/crm_contacts")

# Producer DAG: declare that it produces this dataset
@dag(schedule='0 6 * * *')
def ingest_crm():
    @task(outlets=[crm_dataset])
    def load_crm():
        pass

# Consumer DAG: runs when dataset is updated
@dag(schedule=[crm_dataset])
def transform_crm():
    @task
    def process():
        pass
```

---

## 5. Monitoring and Alerting

### What to Monitor

| Metric | Why | Alert Threshold |
|---|---|---|
| **Pipeline success rate** | Detect systemic failures | < 95% over 24 hours |
| **Task duration** | Detect performance degradation | > 2x historical average |
| **SLA misses** | Data freshness violations | Any SLA miss |
| **Queue depth** | Scheduler/worker saturation | > 50 queued tasks for > 15 min |
| **Data volume** | Detect missing or duplicate data | > 30% deviation from average |
| **Schema changes** | Detect upstream breaking changes | Any detected change |

### Alerting Implementation

```python
# Airflow — SLA and failure callbacks
def alert_on_failure(context):
    """Send Slack alert on task failure."""
    task_instance = context['task_instance']
    dag_id = context['dag'].dag_id
    message = (
        f"*Pipeline Failure*\n"
        f"DAG: `{dag_id}`\n"
        f"Task: `{task_instance.task_id}`\n"
        f"Execution Date: {context['execution_date']}\n"
        f"Log URL: {task_instance.log_url}"
    )
    send_slack_alert(channel="#data-alerts", message=message)

def alert_on_sla_miss(dag, task_list, blocking_task_list, slas, blocking_tis):
    """Send alert when SLA is missed."""
    message = f"*SLA Miss* for DAG `{dag.dag_id}` — tasks: {[t.task_id for t in task_list]}"
    send_slack_alert(channel="#data-alerts-critical", message=message)
    send_pagerduty_alert(service="data-platform", message=message)
```

### Observability Stack for Data Orchestration

**EN** — Combine orchestrator-native monitoring with external observability:

- **Orchestrator UI**: DAG status, task duration, failure rates (built into Airflow/Dagster/Prefect)
- **Data observability**: Monte Carlo, Elementary, Soda for data quality downstream of pipelines
- **Infrastructure monitoring**: Datadog, Grafana for compute utilization, costs
- **Log aggregation**: Centralize pipeline logs in ELK, Loki, or CloudWatch for debugging
- **Incident management**: Route critical alerts to PagerDuty/Opsgenie with clear runbooks

**FR** — Combiner le monitoring natif de l'orchestrateur avec l'observabilite externe. Les alertes critiques doivent etre routees vers PagerDuty/Opsgenie avec des runbooks clairs.

---

## 6. Data SLAs and Freshness

### Defining Data SLAs

**EN** — A data SLA defines when data must be available and at what quality level. Every gold-layer model and critical dashboard should have a documented SLA. Treat SLA breaches as incidents.

**FR** — Un SLA de donnees definit quand les donnees doivent etre disponibles et a quel niveau de qualite. Chaque modele gold et chaque dashboard critique doit avoir un SLA documente. Traiter les violations de SLA comme des incidents.

### SLA Framework

```yaml
# data_slas.yml — Version-controlled SLA definitions
slas:
  - name: marketing_daily_dashboard
    description: "Marketing team's daily performance dashboard"
    freshness_target: "08:00 UTC daily"
    max_staleness_hours: 4
    quality_requirements:
      - "All tests pass (dbt test)"
      - "Row count within 20% of 7-day average"
      - "No null values in revenue columns"
    owner: data-engineering
    stakeholders: [marketing-team, cmo]
    escalation:
      - delay_minutes: 30
        action: slack_alert
        channel: "#data-alerts"
      - delay_minutes: 60
        action: pagerduty
        service: data-platform
      - delay_minutes: 120
        action: email_stakeholders
```

### Freshness Monitoring

**EN** — Implement freshness checks at multiple levels:

1. **Source freshness** (dbt `source freshness`):
```yaml
# models/staging/_staging.yml
sources:
  - name: crm
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    loaded_at_field: _ingested_at
    tables:
      - name: raw_contacts
      - name: raw_orders
```

2. **Pipeline freshness** (orchestrator SLAs): Monitor that pipelines complete within their expected window.

3. **Asset freshness** (Dagster FreshnessPolicy, Elementary, Monte Carlo): Monitor that downstream tables are refreshed on schedule.

---

## 7. Orchestrator Selection Guide

### Decision Matrix

| Criterion | Airflow | Dagster | Prefect | Mage |
|---|---|---|---|---|
| **Maturity** | Very high | High | Medium-high | Medium |
| **Community size** | Massive | Growing fast | Growing | Small |
| **Learning curve** | Medium-high | Medium | Low | Low |
| **Dynamic workflows** | Limited | Good | Excellent | Good |
| **Asset-centric** | No (task-centric) | Yes (native) | No (task-centric) | Partial |
| **Built-in data lineage** | No (requires plugins) | Yes | No | Yes |
| **Managed offering** | MWAA, Composer, Astronomer | Dagster+ | Prefect Cloud | Mage Pro |
| **Best for** | Large teams, complex DAGs | Modern data teams | Python-heavy teams | Small teams, prototypes |

**EN** — For new data platforms in 2025-2026, evaluate Dagster seriously — its asset-centric model aligns naturally with modern data engineering. For teams with existing Airflow investment, upgrade to Airflow 2.x+ and adopt the TaskFlow API and Dataset-aware scheduling.

**FR** — Pour les nouvelles plateformes de donnees en 2025-2026, evaluer Dagster serieusement — son modele asset-centric s'aligne naturellement avec l'ingenierie des donnees moderne. Pour les equipes avec un investissement Airflow existant, upgrader vers Airflow 2.x+ et adopter le TaskFlow API et le scheduling Dataset-aware.
