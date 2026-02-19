# MLOps Implementation — MLflow, CI/CD, Feature Store & Model Registry

## Overview

Ce guide couvre l'implementation concrete des practices MLOps : configuration de MLflow et Weights & Biases pour le tracking des experiments, versionnage des donnees avec DVC, mise en place d'un feature store, CI/CD pour les modeles ML, et deploiement sur les plateformes cloud managees (Vertex AI, SageMaker). L'objectif est de passer d'un ML artisanal (notebooks, scripts ad-hoc) a un ML industrialise avec des pipelines reproductibles et monitores.

---

## MLflow — Tracking, Registry & Serving

### Configuration et Structure du Projet

```python
# Installation
pip install mlflow[extras] scikit-learn xgboost

# Structure recommandee d'un projet avec MLflow
projet_ml/
├── mlflow/
│   └── mlruns/          # Local (dev) — en production, utiliser un serveur MLflow distant
├── src/
│   ├── train.py         # Script d'entrainement avec MLflow tracking
│   ├── predict.py       # Script d'inference
│   └── evaluate.py      # Evaluation des modeles
├── configs/
│   └── config.yaml      # Hyperparametres et configuration
└── MLproject            # Definition du projet MLflow
```

### Tracking des Experiments

```python
import mlflow
import mlflow.xgboost
from mlflow.models.signature import infer_signature

# Configurer le serveur MLflow (distant en production)
mlflow.set_tracking_uri("https://mlflow.votre-organisation.com")
# OU pour le backend cloud :
# mlflow.set_tracking_uri("databricks")  # Databricks MLflow
# mlflow.set_tracking_uri("s3://votre-bucket/mlruns")  # S3 backend

# Creer ou selectionner un experiment
mlflow.set_experiment("churn-prediction-v2")

with mlflow.start_run(run_name="xgboost-balanced-v1") as run:
    # Logger les parametres
    mlflow.log_params({
        "n_estimators": 500,
        "max_depth": 6,
        "learning_rate": 0.05,
        "scale_pos_weight": neg_count / pos_count,
        "validation_strategy": "out_of_time",
        "train_period": "2023-01-01_to_2024-06-30",
        "test_period": "2024-07-01_to_2024-12-31"
    })

    # Entrainement
    model = XGBClassifier(**params)
    model.fit(X_train, y_train,
              eval_set=[(X_val, y_val)],
              early_stopping_rounds=50)

    # Logger les metriques
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    mlflow.log_metrics({
        "auc_roc": roc_auc_score(y_test, y_pred_proba),
        "auc_pr": average_precision_score(y_test, y_pred_proba),
        "f1_optimal": f1_at_optimal_threshold(y_test, y_pred_proba),
        "recall_top10pct": recall_at_top_k(y_test, y_pred_proba, k=0.10)
    })

    # Logger le modele avec sa signature
    signature = infer_signature(X_test, y_pred_proba)
    mlflow.xgboost.log_model(
        model,
        artifact_path="model",
        signature=signature,
        registered_model_name="churn-prediction"  # Enregistrement automatique dans le registry
    )

    # Logger des artefacts supplementaires
    mlflow.log_artifact("reports/feature_importance.png")
    mlflow.log_artifact("reports/calibration_curve.png")

    print(f"Run ID : {run.info.run_id}")
```

### Model Registry — Workflow de Validation

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Transition d'un modele de None vers Staging
client.transition_model_version_stage(
    name="churn-prediction",
    version=3,
    stage="Staging",
    archive_existing_versions=False  # Garder les versions precedentes
)

# Apres validation en staging, passer en Production
client.transition_model_version_stage(
    name="churn-prediction",
    version=3,
    stage="Production",
    archive_existing_versions=True  # Archiver automatiquement l'ancienne version Production
)

# Charger le modele de production dans le code d'inference
production_model = mlflow.pyfunc.load_model("models:/churn-prediction/Production")
predictions = production_model.predict(X_inference)
```

### Etapes du Model Registry

| Etape | Description | Conditions de passage |
|---|---|---|
| **None** | Modele enregistre, pas encore classe | Experiment termine |
| **Staging** | En cours de validation | Metriques > seuil minimum |
| **Production** | Deploye et actif | Validation par l'equipe ML et le business |
| **Archived** | Remplace par une version plus recente | Automatique apres promotion en Production |

---

## Weights & Biases (W&B)

### Cas d'usage et differences avec MLflow

W&B excelle pour :
- La visualisation en temps reel des experiments (courbes d'entrainement interactives)
- Le hyperparameter tuning automatise (Sweeps)
- La collaboration en equipe sur les experiments
- Le tracking des modeles de deep learning et LLM

```python
import wandb

# Initialisation du run
wandb.init(
    project="churn-prediction",
    name="xgboost-balanced-v1",
    config={
        "n_estimators": 500,
        "max_depth": 6,
        "learning_rate": 0.05
    }
)

# Log au cours de l'entrainement (chaque epoch ou iteration)
for epoch in range(n_epochs):
    wandb.log({
        "train_loss": train_loss,
        "val_loss": val_loss,
        "auc_pr": auc_pr,
        "epoch": epoch
    })

# Log du modele
wandb.log_model(path="model.pkl", name="churn-xgb-v1")

# Finaliser le run
wandb.finish()
```

### W&B Sweeps — Hyperparameter Tuning Automatise

```yaml
# sweep_config.yaml
method: bayes  # bayesian optimization (recommande), grid, random
metric:
  name: auc_pr
  goal: maximize
parameters:
  n_estimators:
    values: [200, 500, 1000]
  max_depth:
    distribution: int_uniform
    min: 4
    max: 10
  learning_rate:
    distribution: log_uniform_values
    min: 0.01
    max: 0.3
  subsample:
    distribution: uniform
    min: 0.6
    max: 1.0
  scale_pos_weight:
    value: 10.0  # Fixe selon le ratio de classes
```

```python
# Lancement du sweep
sweep_id = wandb.sweep(sweep_config, project="churn-prediction")
wandb.agent(sweep_id, function=train_with_params, count=50)
```

---

## DVC — Versionnage des Donnees

### Installation et Configuration

```bash
pip install dvc dvc-s3  # ou dvc-gcs, dvc-azure selon le provider

# Initialiser DVC dans le repo git
dvc init
git commit -m "Initialize DVC"

# Configurer le remote storage (S3 recommande pour la production)
dvc remote add -d myremote s3://mon-bucket-ml/dvc-store
dvc remote modify myremote region eu-west-1

# Activer l'encryption cote serveur
dvc remote modify myremote sse aws:kms
```

### Versionner les Donnees

```bash
# Tracker un fichier de donnees avec DVC
dvc add data/raw/transactions_2024.parquet

# Cela cree un fichier .dvc (leger, suivi par git)
git add data/raw/transactions_2024.parquet.dvc
git commit -m "Add transactions dataset 2024-Q4"

# Pousser les donnees vers le remote
dvc push

# Tag la version des donnees avec git
git tag -a "data-v1.2.0" -m "Dataset with 2024 transactions, churn labels recalculated"
git push origin data-v1.2.0
```

### Pipelines DVC

```yaml
# dvc.yaml — Definition du pipeline reproductible
stages:
  preprocess:
    cmd: python src/preprocess.py --input data/raw/transactions.parquet --output data/processed/
    deps:
      - src/preprocess.py
      - data/raw/transactions.parquet
    outs:
      - data/processed/features.parquet
      - data/processed/labels.parquet

  train:
    cmd: python src/train.py
    deps:
      - src/train.py
      - data/processed/features.parquet
      - data/processed/labels.parquet
      - configs/model_config.yaml
    outs:
      - models/xgb_churn.pkl
    metrics:
      - metrics/train_metrics.json:
          cache: false

  evaluate:
    cmd: python src/evaluate.py
    deps:
      - src/evaluate.py
      - models/xgb_churn.pkl
      - data/processed/features.parquet
    metrics:
      - metrics/eval_metrics.json:
          cache: false
```

```bash
# Executer le pipeline (ne rejoue que les stages modifies)
dvc repro

# Comparer les metriques entre versions
dvc metrics diff HEAD~1

# Voir l'arbre des dependances du pipeline
dvc dag
```

---

## Feature Store

### Pourquoi un Feature Store ?

Le feature store resout trois problemes critiques :
1. **Train-serve skew** : les features sont calculees differemment entre l'entrainement et l'inference
2. **Duplication** : plusieurs equipes recalculent les memes features (ex: "nombre d'achats dans les 30 derniers jours")
3. **Point-in-time correctness** : en entrainement, utiliser les features telles qu'elles etaient au moment de l'evenement (eviter le leakage temporel)

### Feast — Open Source Feature Store

```python
# definitions des features (feature_repo/feature_views.py)
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from datetime import timedelta

# Entity
customer = Entity(
    name="customer_id",
    value_type=ValueType.INT64,
    description="Identifiant unique du client"
)

# Source de donnees
customer_stats_source = FileSource(
    path="s3://mon-bucket/features/customer_stats/*.parquet",
    event_timestamp_column="event_timestamp",
    created_timestamp_column="created_timestamp"
)

# Feature View
customer_activity_fv = FeatureView(
    name="customer_activity",
    entities=["customer_id"],
    ttl=timedelta(days=90),  # Duree de vie des features
    features=[
        Feature(name="nb_transactions_7d", dtype=ValueType.INT32),
        Feature(name="nb_transactions_30d", dtype=ValueType.INT32),
        Feature(name="total_amount_30d", dtype=ValueType.FLOAT),
        Feature(name="days_since_last_transaction", dtype=ValueType.INT32),
        Feature(name="avg_transaction_amount", dtype=ValueType.FLOAT),
        Feature(name="support_tickets_90d", dtype=ValueType.INT32),
    ],
    batch_source=customer_stats_source,
)
```

```python
# Recuperation des features pour l'entrainement (historique, point-in-time correct)
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo/")

# Dataset d'entrainement : features au moment de l'observation
training_df = store.get_historical_features(
    entity_df=entity_df_with_timestamps,  # DataFrame avec customer_id et event_timestamp
    features=[
        "customer_activity:nb_transactions_7d",
        "customer_activity:nb_transactions_30d",
        "customer_activity:total_amount_30d",
        "customer_activity:days_since_last_transaction",
    ]
).to_df()

# Recuperation des features pour l'inference (temps reel)
feature_vector = store.get_online_features(
    features=["customer_activity:nb_transactions_7d", ...],
    entity_rows=[{"customer_id": 12345}]
).to_dict()
```

---

## CI/CD pour les Modeles ML

### Pipeline GitHub Actions — ML

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Training & Validation Pipeline

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'configs/**'
      - 'data/**/*.dvc'  # Declenchement sur changement de donnees
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Lint (ruff)
        run: ruff check src/

      - name: Type check (mypy)
        run: mypy src/

      - name: Unit tests
        run: pytest tests/unit/ -v --cov=src --cov-report=xml

      - name: Data validation tests
        run: pytest tests/data/ -v

  train-and-evaluate:
    needs: lint-and-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'  # Entrainement uniquement sur main
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/ml-pipeline-role
          aws-region: eu-west-1

      - name: Pull DVC data
        run: dvc pull

      - name: Run training pipeline
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
          WANDB_API_KEY: ${{ secrets.WANDB_API_KEY }}
        run: dvc repro

      - name: Evaluate model performance
        run: python src/evaluate.py --compare-to-production

      - name: Gate check — performance threshold
        run: |
          AUC_PR=$(cat metrics/eval_metrics.json | jq '.auc_pr')
          if (( $(echo "$AUC_PR < 0.72" | bc -l) )); then
            echo "FAIL: AUC-PR $AUC_PR is below minimum threshold 0.72"
            exit 1
          fi
          echo "PASS: AUC-PR $AUC_PR meets threshold"

      - name: Promote model to Staging (if performance gate passes)
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
        run: python scripts/promote_to_staging.py

  integration-tests:
    needs: train-and-evaluate
    runs-on: ubuntu-latest
    steps:
      - name: Run inference integration tests
        run: pytest tests/integration/ -v

  deploy-to-production:
    needs: integration-tests
    runs-on: ubuntu-latest
    environment: production  # Requiert une approbation manuelle dans GitHub
    steps:
      - name: Promote model to Production
        run: python scripts/promote_to_production.py

      - name: Deploy model endpoint
        run: python scripts/deploy_endpoint.py

      - name: Smoke test production endpoint
        run: python scripts/smoke_test.py
```

---

## Deploiement sur Plateformes Managees

### Vertex AI (GCP)

```python
from google.cloud import aiplatform

aiplatform.init(project="mon-projet-gcp", location="europe-west1")

# Uploader le modele
model = aiplatform.Model.upload(
    display_name="churn-prediction-v3",
    artifact_uri="gs://mon-bucket/models/churn/v3/",
    serving_container_image_uri="europe-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-3:latest",
    serving_container_environment_variables={
        "MODEL_NAME": "churn-prediction",
        "VERSION": "3"
    }
)

# Creer un endpoint
endpoint = aiplatform.Endpoint.create(display_name="churn-prediction-endpoint")

# Deployer le modele
model.deploy(
    endpoint=endpoint,
    deployed_model_display_name="churn-v3",
    machine_type="n1-standard-4",
    min_replica_count=2,
    max_replica_count=10,
    traffic_split={"0": 100}  # 100% du trafic sur la version 0 (la nouvelle)
)
```

### SageMaker (AWS)

```python
import sagemaker
from sagemaker.sklearn.model import SKLearnModel

sagemaker_session = sagemaker.Session()
role = "arn:aws:iam::123456789:role/SageMakerRole"

# Uploader les artefacts du modele
model_uri = sagemaker_session.upload_data(
    path="model.tar.gz",
    bucket="mon-bucket-ml",
    key_prefix="models/churn/v3"
)

# Creer le modele
sklearn_model = SKLearnModel(
    model_data=model_uri,
    role=role,
    entry_point="inference.py",
    framework_version="1.2-1",
    py_version="py3"
)

# Deployer sur un endpoint
predictor = sklearn_model.deploy(
    initial_instance_count=2,
    instance_type="ml.t3.large",
    endpoint_name="churn-prediction-v3"
)

# Prediction
result = predictor.predict([[features]])
```

---

## Monitoring de la Performance en Production

### Metriques a Monitorer par Couche

**Couche 1 — Donnees d'inference**

| Metrique | Description | Outil | Seuil d'alerte |
|---|---|---|---|
| Volume de requetes | Nombre de predictions/heure | Prometheus, CloudWatch | < 50% ou > 200% vs semaine precedente |
| Taux de valeurs manquantes | % de features nulles | Evidently, WhyLabs | > 2x le baseline training |
| Distribution des features | Deviation statistique (PSI, KL divergence) | Evidently | PSI > 0.2 sur feature critique |
| Plage des valeurs | Min/max des features numeriques | Evidently | Feature hors plage training + 3 sigma |

**Couche 2 — Modele**

| Metrique | Description | Outil | Seuil d'alerte |
|---|---|---|---|
| Distribution des predictions | Histogramme des scores | Evidently, Arize | KL divergence > 0.1 vs baseline |
| Taux de predictions par bucket | % predictions haute/basse probabilite | Custom | > 20% deviation vs baseline |
| Latence d'inference | P50, P95, P99 en ms | Prometheus, Datadog | P99 > SLA definie |
| Taux d'erreur | % de requetes en erreur | Prometheus | > 0.1% |

**Couche 3 — Business**

| Metrique | Description | Outil | Seuil d'alerte |
|---|---|---|---|
| KPI metier | Taux de churn reel, conversion, etc. | BI dashboard | Deviation > 10% vs baseline |
| Precision@K observe | Fraction des cas etiquetes positifs parmi les top-K | Custom | < seuil defini post-deployment |
| A/B test performance | Performance champion vs challenger | Custom | Challenger significativement inferieur |

### Evidently AI — Configuration du Monitoring

```python
from evidently.metric_preset import DataDriftPreset, ClassificationPreset
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.tests import TestNumberOfMissingValues, TestShareOfMissingValues

# Rapport de drift des donnees
data_drift_report = Report(metrics=[DataDriftPreset()])
data_drift_report.run(
    reference_data=training_data[feature_columns],
    current_data=production_data[feature_columns]
)
data_drift_report.save_html("reports/data_drift_report.html")

# Test suite pour l'integrer dans le pipeline CI/CD
test_suite = TestSuite(tests=[
    TestNumberOfMissingValues(),
    TestShareOfMissingValues(lte=0.05),  # Max 5% de valeurs manquantes
])
test_suite.run(
    reference_data=training_data,
    current_data=production_data
)
if not test_suite.as_dict()["summary"]["all_passed"]:
    raise ValueError("Data quality tests failed — check drift report")
```

---

## Cadences de Retraining

### Politique de Retraining par Type de Modele

| Type de modele | Trigger principal | Frequence minimale | Trigger supplementaire |
|---|---|---|---|
| **Churn prediction** | Drift des features comportementales | Mensuel | Changement produit majeur |
| **Demande forecasting** | Performance offline (MAPE > seuil) | Hebdomadaire | Saisonnalite annuelle |
| **Scoring credit** | Concept drift (evolution economique) | Trimestriel | Changement reglementaire |
| **Recommandation** | Nouveaux items (item cold start) | Quotidien / temps reel | Evenements marketing majeurs |
| **Fraude** | Nouveau pattern de fraude detecte | Quotidien | En continu (online learning) |

### Retraining Automatique avec Alertes

```python
# monitoring/retrain_trigger.py
import mlflow
from evidently.metrics import DataDriftTable

def check_and_trigger_retraining(reference_data, current_data, threshold_psi=0.2):
    """
    Verifie si un retraining est necessaire et declenche le pipeline si oui.
    """
    # Calcul du Population Stability Index (PSI)
    report = Report(metrics=[DataDriftTable()])
    report.run(reference_data=reference_data, current_data=current_data)

    drifted_features = [
        f for f in report.as_dict()["metrics"][0]["result"]["drift_by_columns"]
        if report.as_dict()["metrics"][0]["result"]["drift_by_columns"][f]["drift_score"] > threshold_psi
    ]

    if len(drifted_features) > 0:
        # Envoyer une alerte (Slack, PagerDuty, email)
        send_drift_alert(drifted_features, threshold_psi)

        # Declencher le pipeline de retraining (ex: GitHub Actions workflow_dispatch)
        trigger_retraining_pipeline(
            reason=f"Drift detecte sur {len(drifted_features)} features : {drifted_features}",
            severity="high" if len(drifted_features) > 3 else "medium"
        )

    return drifted_features
```
