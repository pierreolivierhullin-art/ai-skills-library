# Data Observability — Detection des Anomalies et Monitoring

## Vue d'Ensemble

La data observability est la capacite d'une organisation a comprendre l'etat de sante de ses donnees a tout moment. Analogue a l'observabilite des systemes logiciels (APM, distributed tracing), elle repose sur cinq piliers : freshness, volume, distribution, schema et lineage. L'objectif : detecter les problemes de donnees avant que les utilisateurs ne s'en rendent compte, et diagnostiquer rapidement la cause racine.

---

## Les 5 Piliers en Detail

### 1. Freshness (Fraicheur)

Detecte : table non mise a jour, pipeline en retard ou en echec.

**Monitoring de base** :
```sql
-- Verifier la fraicheur d'une table BigQuery
SELECT
    table_name,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(last_modified_time), HOUR) AS hours_since_update
FROM information_schema.PARTITIONS
WHERE table_schema = 'gold'
    AND table_name IN ('orders_daily', 'customer_360', 'revenue_forecast')
GROUP BY 1
ORDER BY hours_since_update DESC;
```

**Alerting** :
```python
# Exemple avec dbt et Elementary
# schema.yml
models:
  - name: orders_daily
    tests:
      - elementary.table_anomalies:
          timestamp_column: order_date
          anomaly_sensitivity: 3  # z-score
      - dbt_utils.recency:
          datepart: hour
          field: loaded_at
          interval: 26  # alerte si plus de 26h sans update
```

**SLO de fraicheur** :
Definir pour chaque data product le delai maximum acceptable entre la donnee source et sa disponibilite downstream. Exemple : orders_daily disponible avant 06h00 CET (J+1) — SLO de fraicheur = 30h.

### 2. Volume

Detecte : absence de donnees (pipeline bloque), donnees dupliquees (double chargement), perte de donnees (filtrage incorrect).

**Detection d'anomalies de volume** :
```python
import pandas as pd
import numpy as np
from scipy import stats

def detect_volume_anomaly(df_history, current_count, threshold_sigma=3):
    """
    Detecte si le volume actuel est anormal par rapport a l'historique
    Utilise un Z-score sur une fenetre glissante de 30 jours
    """
    historical_counts = df_history['row_count'].values

    mean = np.mean(historical_counts)
    std = np.std(historical_counts)

    if std == 0:
        return False, 0.0

    z_score = (current_count - mean) / std

    is_anomaly = abs(z_score) > threshold_sigma

    return is_anomaly, z_score

# Usage
is_anomaly, z = detect_volume_anomaly(history_df, today_count=45200)
if is_anomaly:
    send_alert(f"Volume anomalie : {today_count} rows (z={z:.2f})")
```

**Regles de volume dans dbt** :
```yaml
models:
  - name: orders_daily
    tests:
      - dbt_utils.expression_is_true:
          expression: "count(*) BETWEEN 50000 AND 200000"
          config:
            severity: error
      - elementary.volume_anomalies:
          timestamp_column: order_date
          anomaly_sensitivity: 3.5
```

### 3. Distribution

Detecte : changements dans les statistiques des colonnes (shift de la moyenne, apparition de nouvelles valeurs, proportion de nulls qui explose, outliers).

**Metriques de distribution a surveiller** :

| Metrique | Type de colonne | Seuil d'alerte |
|---|---|---|
| Proportion de NULL | Toutes | > 2x la baseline sur 30j |
| Moyenne | Numerique | Z-score > 3 vs baseline 30j |
| % valeurs negatives | Montants, quantites | > 0.5% (normalement 0) |
| Entropie de Shannon | Categorique | Variation > 20% vs baseline |
| Min / Max | Numerique | En dehors des bornes historiques |

**Implementation avec Great Expectations** :
```python
import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest

context = gx.get_context()

# Batch sur les nouvelles donnees
batch = context.get_validator(
    datasource_name="bigquery_prod",
    data_asset_name="orders_daily",
    batch_request=RuntimeBatchRequest(
        datasource_name="bigquery_prod",
        data_connector_name="default_runtime_data_connector",
        data_asset_name="orders_daily",
        runtime_parameters={"query": "SELECT * FROM gold.orders_daily WHERE order_date = CURRENT_DATE() - 1"},
        batch_identifiers={"default_identifier_name": "today"},
    )
)

# Tests de distribution
batch.expect_column_mean_to_be_between("revenue_eur", min_value=45.0, max_value=120.0)
batch.expect_column_proportion_of_unique_values_to_be_between("customer_id", min_value=0.98)
batch.expect_column_values_to_not_be_null("order_date")
batch.expect_column_values_to_be_between("revenue_eur", min_value=0, max_value=50000)

# Categories valides
batch.expect_column_values_to_be_in_set(
    "status",
    value_set=["completed", "refunded", "pending", "cancelled"]
)

results = batch.validate()
```

**PSI — Population Stability Index** :

Detecte le drift d'une variable numerique ou categorique par rapport a une reference.

```python
def calculate_psi(reference, current, buckets=10):
    """
    PSI < 0.1 : pas de shift significatif
    PSI 0.1-0.2 : shift modere — surveiller
    PSI > 0.2 : shift important — investiguer
    """
    breakpoints = np.linspace(
        min(reference.min(), current.min()),
        max(reference.max(), current.max()),
        buckets + 1
    )

    ref_pct = np.histogram(reference, bins=breakpoints)[0] / len(reference)
    cur_pct = np.histogram(current, bins=breakpoints)[0] / len(current)

    # Eviter la division par zero
    ref_pct = np.where(ref_pct == 0, 0.0001, ref_pct)
    cur_pct = np.where(cur_pct == 0, 0.0001, cur_pct)

    psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
    return psi
```

### 4. Schema

Detecte : colonne supprimee, type de donnee change, nouvelle colonne obligatoire ajoutee sans valeur par defaut.

**Types de changements de schema** :

| Changement | Impact | Severite |
|---|---|---|
| Colonne supprimee | Downstream queries cassees | CRITIQUE |
| Type change (int → string) | Resultats incorrects silencieux | ELEVEE |
| Colonne renommee | Equivalent a suppression + ajout | CRITIQUE |
| Colonne ajoutee | Impact limité si nullable | FAIBLE |
| Precision reduite (DECIMAL(18,4) → DECIMAL(10,2)) | Perte de precision | ELEVEE |

**Detection dans dbt** :
```yaml
# Verifier le type de colonne
models:
  - name: orders_daily
    columns:
      - name: revenue_eur
        data_type: NUMERIC
        tests:
          - not_null
      - name: order_date
        data_type: DATE
        tests:
          - not_null
```

**Schema Evolution — Strategie** :

```python
# Comparaison de schema avant/apres (exemple Python)
def compare_schemas(old_schema: dict, new_schema: dict) -> dict:
    old_cols = set(old_schema.keys())
    new_cols = set(new_schema.keys())

    breaking_changes = []
    warnings = []

    # Colonnes supprimees
    for col in old_cols - new_cols:
        breaking_changes.append(f"BREAKING: Column '{col}' deleted")

    # Colonnes renommees (heuristique : type identique, nom different)
    # ...

    # Changements de type
    for col in old_cols & new_cols:
        if old_schema[col]['type'] != new_schema[col]['type']:
            breaking_changes.append(
                f"BREAKING: Column '{col}' type changed: "
                f"{old_schema[col]['type']} → {new_schema[col]['type']}"
            )

    # Nouvelles colonnes NOT NULL sans defaut
    for col in new_cols - old_cols:
        if new_schema[col].get('nullable') == False and \
           new_schema[col].get('default') is None:
            breaking_changes.append(
                f"BREAKING: New NOT NULL column '{col}' without default"
            )
        else:
            warnings.append(f"INFO: New column '{col}' added")

    return {
        'breaking': breaking_changes,
        'warnings': warnings,
        'is_breaking': len(breaking_changes) > 0
    }
```

### 5. Lineage

Detecte : impact amont/aval d'un changement, root cause analysis lors d'un incident.

**Lineage dans dbt** :

dbt genere automatiquement un graphe de dependances entre les modeles. Accessible via `dbt docs generate` ou dans l'interface de dbt Cloud.

```bash
# Identifier tous les modeles dependant d'une source
dbt ls --select +my_source_table+

# Tester tous les dependants d'un modele
dbt test --select +orders_daily+

# En cas de breaking change sur orders_daily, identifier l'impact
dbt ls --select orders_daily+  # Tous les modeles downstream
```

**Lineage avec Datahub** :
```python
# Push du lineage vers Datahub
from datahub.emitter.mce_builder import make_dataset_urn

dataset_properties = {
    "upstreams": [
        {"dataset": make_dataset_urn("bigquery", "prod.raw.orders"), "type": "TRANSFORMED"},
    ],
    "downstreams": [
        make_dataset_urn("bigquery", "prod.gold.revenue_monthly"),
        make_dataset_urn("bigquery", "prod.gold.customer_ltv"),
    ]
}
```

---

## Outils de Data Observability

### Monte Carlo Data

Outil commercial de reference (Series D, >$235M leve). Approche : ML pour detecter automatiquement les anomalies sans regles manuelles.

**Points forts** :
- Detection automatique (pas besoin de definir les seuils manuellement)
- Lineage automatique par reverse engineering des requetes SQL
- Alertes avec root cause analysis
- Integration native BigQuery, Snowflake, Redshift, dbt

**Points faibles** :
- Cout eleve (~ 30-100k USD/an selon la taille)
- Latence de detection (pas du temps reel)
- Boite noire — peu transparent sur les algorithmes

### Elementary (open source, dbt-native)

Outil open source qui s'integre directement dans le projet dbt. Couvre: anomalies de volume, fraicheur, distribution, schema drift.

```bash
# Installation
pip install elementary-data

# Initialisation dans le projet dbt
dbt run --select elementary

# Rapport d'observabilite
edr report  # Genere un rapport HTML local
edr send-report --slack-webhook YOUR_WEBHOOK  # Envoie sur Slack
```

Avantages : gratuit, open source, s'integre naturellement dans dbt. Limites : moins complet que Monte Carlo sur le lineage et le root cause analysis.

### Soda (open source + commercial)

Framework de tests de qualite de donnees avec un DSL specifique (SodaCL).

```yaml
# checks.yml
checks for orders_daily:
  - freshness(order_date) < 26h
  - row_count between 50000 and 200000:
      warn:
        when not between 60000 and 150000
      fail:
        when not between 50000 and 200000
  - missing_count(customer_id) = 0
  - duplicate_count(customer_id, order_date) = 0
  - invalid_count(status) = 0:
      valid values: [completed, refunded, pending, cancelled]
  - avg(revenue_eur) between 50 and 110
```

```bash
soda scan -d bigquery_prod -c soda_config.yml checks.yml
```

---

## Architecture d'Observabilite Complete

```
Sources (databases, APIs, SaaS)
        |
        ↓ [Ingestion + tests schema]
Bronze Layer
        |
        ↓ [dbt + tests de source (not_null, unique, referential)]
Silver Layer
        |
        ↓ [dbt + tests metier + Great Expectations]
Gold Layer (data products)
        |
        ↓ [Monitoring en continu]
Observabilite Runtime
    ├── Elementary / Monte Carlo / Soda [volume, freshness, distribution]
    ├── Datahub / OpenMetadata [lineage, catalog]
    └── Alerting [Slack, PagerDuty, email]
        |
        ↓
SLO Dashboard (Gold Layer health score)
```

## Incident Response — Data Incident Playbook

```
Alerte detectee (freshness, volume, schema, distribution)
        |
        ↓
Triage (< 15 min)
  - Quelle table / pipeline ?
  - Quel type d'anomalie ?
  - Quels consommateurs impactes ?
        |
        ↓
Evaluation severite
  CRITIQUE : donnees incorrectes utilisees dans des decisions en prod
  ELEVEE   : rapport ou dashboard impacte
  MODEREE  : retard, pas d'incorrection
        |
        ↓ (si CRITIQUE ou ELEVEE)
Communication
  - Notifier les data stewards des tables impactees
  - Notifier les utilisateurs finaux (si rapports publics impactes)
  - Postmortem prevu
        |
        ↓
Root Cause Analysis (lineage)
  - Remonter le lineage upstream
  - Identifier le premier point de defaillance
  - Verifier les logs du pipeline (Airflow, dbt, Fivetran)
        |
        ↓
Resolution
  - Corriger la source si possible
  - Rejouer le pipeline depuis le point de defaillance
  - Valider les SLOs apres resolution
        |
        ↓
Post-mortem (< 48h apres resolution)
  - Timeline de l'incident
  - Root cause
  - Impact (combien d'heures de downtime, combien de tables, combien d'utilisateurs)
  - Actions preventives (nouveau test, monitoring additionnel, data contract)
```
