# AutoML Tools — H2O, AutoGluon, DataRobot & Feature Engineering Automatisé

## Overview

Ce guide couvre les outils d'AutoML (Automated Machine Learning) pour le ML applique au metier : H2O AutoML, AutoGluon d'Amazon, DataRobot, et les plateformes cloud AutoML. Pour chaque outil, le guide presente les capacites, les limites, les bonnes pratiques d'utilisation, et les pieges a eviter. L'objectif est de savoir quand et comment utiliser l'AutoML pour accelerer le developpement de modeles sans sacrifier la rigueur ni creer des systemes non maintenables.

---

## Qu'est-ce que l'AutoML et Quand l'Utiliser ?

### Definition

L'AutoML automatise une partie ou la totalite du pipeline ML :
- **Feature engineering automatise** : generation de features, encodage, imputation
- **Selection de modeles** : tester plusieurs algorithmes et architectures
- **Optimisation des hyperparametres** : grid search, random search, optimisation bayesienne
- **Ensembling** : combiner plusieurs modeles pour ameliorer la performance
- **Interpretation** : importance des features, explications locales (SHAP)

### Quand Utiliser l'AutoML ?

**Cas d'usage ideal pour l'AutoML** :
- Exploration rapide de nouveaux use cases (evaluer la faisabilite en quelques heures)
- Datasets de taille moyenne (10k - 1M lignes, < 100 features)
- Equipes moins experimentees en ML qui veulent des resultats rapides
- Benchmarking : comparer les performances AutoML avec un modele custom
- PoC a livrer rapidement avant une decision d'investissement

**Cas ou l'AutoML est insuffisant** :
- Contraintes de latence d'inference tres strictes (AutoML peut produire des ensembles lourds)
- Donnees non tabulaires (images, textes, sequences temporelles longues)
- Besoin d'interpretabilite metier fine (explicabilite "globale" vs "locale")
- Production haute frequence avec monitoring fin du modele
- Donnees tres specifiques avec connaissance metier forte a integrer dans les features

### AutoML ne remplace pas le Data Scientist

L'AutoML accelere le travail mais ne remplace pas :
- La definition du probleme (quelle variable cible, quel horizon, quelle metrique)
- L'audit de qualite des donnees (data leakage, drift, biais)
- La validation metier des resultats (est-ce que le modele est coherent avec la logique metier ?)
- Le feature engineering specifique (connaissance metier qui ne s'automatise pas)
- Le monitoring en production et le plan de retraining

---

## H2O AutoML

### Presentation et Positionnement

H2O AutoML est l'une des solutions AutoML open source les plus puissantes. Il entraine systematiquement un ensemble de modeles (XGBoost, GBM, GLM, Deep Learning, Stacked Ensembles) et les classe selon la metrique choisie.

**Forces** :
- Entierement open source et gratuit (H2O 3)
- Interface Python, R et web UI (Flow)
- Stacked Ensemble systematique (combine les meilleurs modeles)
- Rapide sur les donnees tabulaires
- Export des modeles en Java (POJO) pour l'inference a faible latence

**Limites** :
- Gestion des series temporelles limitee (pas de validation temporelle automatique)
- Pas de support natif pour le texte brut ou les images
- Peut produire des ensembles complexes difficiles a interpreter

### Utilisation Pratique

```python
import h2o
from h2o.automl import H2OAutoML

# Demarrer H2O
h2o.init(nthreads=-1, max_mem_size="8G")  # Utilise tous les CPU, 8GB RAM

# Charger les donnees
train = h2o.import_file("data/train.csv")
test = h2o.import_file("data/test.csv")

# Definir la cible et les features
target = "churn"
features = train.columns
features.remove(target)
features.remove("customer_id")  # Retirer les identifiants

# Convertir la cible en facteur pour la classification
train[target] = train[target].asfactor()
test[target] = test[target].asfactor()

# Lancer l'AutoML
aml = H2OAutoML(
    max_models=20,             # Tester 20 modeles maximum
    max_runtime_secs=3600,     # 1 heure maximum
    seed=42,
    sort_metric="AUC",         # Ou "AUCPR" pour les classes desequilibrees
    stopping_metric="AUC",
    exclude_algos=["DeepLearning"],  # Optionnel : exclure des algos
    include_algos=None,        # None = inclure tous
    nfolds=5,                  # Validation croisee
    balance_classes=True       # Pour les classes desequilibrees (churn)
)

aml.train(x=features, y=target, training_frame=train, leaderboard_frame=test)

# Voir le classement des modeles
print(aml.leaderboard.head(10))

# Meilleur modele
best_model = aml.leader
print(f"Meilleur modele : {best_model.model_id}")
print(f"AUC sur le test : {best_model.auc(xval=True):.4f}")

# Importance des features (SHAP pour les tree-based models)
best_model.shap_explain_row_plot(test, row_index=0)

# Prediction
predictions = best_model.predict(test)
print(predictions.head())

# Sauvegarder le modele
model_path = h2o.save_model(model=best_model, path="models/", force=True)
print(f"Modele sauvegarde : {model_path}")
```

### Validation Temporelle avec H2O

```python
# H2O n'a pas de validation temporelle native — la configurer manuellement
cutoff_date = "2024-06-30"

train_period = df[df['date'] <= cutoff_date]
test_period = df[df['date'] > cutoff_date]

train_h2o = h2o.H2OFrame(train_period)
test_h2o = h2o.H2OFrame(test_period)

# Lancer l'AutoML avec un leaderboard sur la periode test
aml = H2OAutoML(max_models=20, max_runtime_secs=1800, seed=42,
                sort_metric="AUCPR")
aml.train(x=features, y=target,
          training_frame=train_h2o,
          leaderboard_frame=test_h2o)  # Evaluer sur le test temporel
```

---

## AutoGluon (Amazon)

### Presentation et Positionnement

AutoGluon est une librairie AutoML d'Amazon particulierement performante sur les benchmarks de donnees tabulaires. Elle se distingue par son approche multi-layer stacking tres agressive.

**Forces** :
- Performance souvent superieure a H2O sur les donnees tabulaires (benchmarks AMLB 2023)
- Support natif des textes, images, et series temporelles (en plus des tableaux)
- Tres facile a utiliser (interface de 3 lignes de code)
- Gestion automatique du desequilibre de classes
- Evaluation multi-metriques

**Limites** :
- Peut etre tres lent sur les grands datasets (stacking agressif)
- Ensembles tres complexes, difficiles a interpreter et a deployer
- Moins adapte aux contraintes de latence (les ensembles sont lourds)

```python
from autogluon.tabular import TabularPredictor
import pandas as pd

# Charger les donnees
train = pd.read_csv("data/train.csv")
test = pd.read_csv("data/test.csv")

# AutoGluon en 3 lignes
predictor = TabularPredictor(
    label='churn',                   # Variable cible
    eval_metric='roc_auc',           # Metrique d'optimisation
    path='models/autogluon-churn/'   # Dossier de sauvegarde
).fit(
    train,
    time_limit=3600,                 # 1 heure maximum
    presets='best_quality',          # 'medium_quality', 'good_quality', 'best_quality'
    ag_args_fit={'num_gpus': 0}      # Pas de GPU (adapte pour le ML tabulaire)
)

# Evaluation
leaderboard = predictor.leaderboard(test, silent=True)
print(leaderboard[['model', 'score_test', 'score_val', 'pred_time_test']].head(10))

# Prediction
proba = predictor.predict_proba(test)
print(f"AUC : {roc_auc_score(test['churn'], proba[1]):.4f}")

# Importance des features
feature_importance = predictor.feature_importance(test)
print(feature_importance.head(20))
```

### Presets AutoGluon

| Preset | Duree | Performance | Complexite du modele | Usage |
|---|---|---|---|---|
| `medium_quality` | 10 min | Bonne | Moderate | Exploration rapide |
| `good_quality` | 1 heure | Tres bonne | Elevee | PoC et prototypes |
| `best_quality` | 4+ heures | Maximale | Tres elevee | Competition, meilleure perf |
| `optimize_for_deployment` | Variable | Bonne | Faible (modele simple) | Production avec contrainte de latence |

---

## DataRobot

### Presentation et Positionnement

DataRobot est une plateforme AutoML enterprise avec interface graphique et APIs. Elle est particulierement adaptee aux organisations qui veulent donner acces au ML a des equipes non techniques (citizen data scientists).

**Forces** :
- Interface graphique intuitive (pas de code necessaire)
- Data prep integree, detection de biais, compliance
- Deployment et monitoring integres (DataRobot MLOps)
- Gouvernance et audit trail complet
- Support fort (customer success, formations)

**Limites** :
- Cout eleve (licences enterprise)
- Moins de flexibilite que les solutions open source
- Lock-in vendor fort
- Moins performant que AutoGluon sur les benchmarks purs

### Quand Choisir DataRobot ?

DataRobot est pertinent quand :
- L'organisation veut donner acces au ML a des analystes metier sans expertise technique
- La gouvernance et l'audit trail sont des exigences reglementaires
- Le MLOps integre dans une seule plateforme est une priorite
- Le budget ne contraint pas le choix de l'outil

---

## Cloud AutoML

### Google Cloud AutoML / Vertex AI AutoML

```python
from google.cloud import aiplatform

aiplatform.init(project="mon-projet", location="europe-west1")

# Creer un dataset dans Vertex AI
dataset = aiplatform.TabularDataset.create(
    display_name="churn-dataset",
    gcs_source="gs://mon-bucket/churn_data.csv"
)

# Lancer l'AutoML
job = aiplatform.AutoMLTabularTrainingJob(
    display_name="churn-automl",
    optimization_prediction_type="classification",
    optimization_objective="maximize-au-prc",  # AUC-PR pour classes desequilibrees
    column_specs={
        "customer_id": "categorical",
        "age": "numeric",
        "nb_transactions_30d": "numeric",
        # ...
    }
)

model = job.run(
    dataset=dataset,
    target_column="churn",
    budget_milli_node_hours=1000,  # 1 heure de compute
    model_display_name="churn-automl-model"
)

# Deploiement automatique
endpoint = model.deploy(
    machine_type="n1-standard-4",
    min_replica_count=1,
    max_replica_count=3
)
```

### AWS SageMaker AutoPilot

```python
import boto3

sm = boto3.client('sagemaker', region_name='eu-west-1')

# Lancer un job AutoPilot
response = sm.create_auto_ml_job(
    AutoMLJobName='churn-autopilot',
    InputDataConfig=[{
        'DataSource': {
            'S3DataSource': {
                'S3DataType': 'S3Prefix',
                'S3Uri': 's3://mon-bucket/churn_train/'
            }
        },
        'TargetAttributeName': 'churn',
        'ContentType': 'text/csv'
    }],
    OutputDataConfig={'S3OutputPath': 's3://mon-bucket/autopilot-output/'},
    AutoMLJobConfig={
        'CompletionCriteria': {
            'MaxCandidates': 20,
            'MaxRuntimePerTrainingJobInSeconds': 3600
        }
    },
    AutoMLJobObjective={'MetricName': 'AUC'}
)
```

---

## Feature Engineering Automatise

### Featuretools — Deep Feature Synthesis

Featuretools permet de generer automatiquement des features a partir de tables relationnelles en appliquant des operations d'agregation (DFS : Deep Feature Synthesis).

```python
import featuretools as ft

# Definir les entites (tables)
es = ft.EntitySet(id="transactions")

es = es.add_dataframe(
    dataframe_name="customers",
    dataframe=customers_df,
    index="customer_id"
)

es = es.add_dataframe(
    dataframe_name="transactions",
    dataframe=transactions_df,
    index="transaction_id",
    time_index="transaction_date"
)

# Definir les relations entre tables
es = es.add_relationship("customers", "customer_id", "transactions", "customer_id")

# Generer les features automatiquement (DFS)
feature_matrix, feature_defs = ft.dfs(
    entityset=es,
    target_dataframe_name="customers",
    agg_primitives=[
        "count", "sum", "mean", "max", "min", "std",
        "num_unique", "last", "trend"
    ],
    trans_primitives=["month", "day_of_week", "is_weekend"],
    max_depth=2,     # Profondeur des features composees
    cutoff_time=cutoff_df  # Eviter le leakage temporel
)

print(f"Features generees : {len(feature_defs)}")
print(f"Exemples de features :")
print(feature_matrix.head())
```

### Sélection de Features

Apres la generation automatique de features, selectionner les plus pertinentes pour eviter la malediction de la dimensionnalite :

```python
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Selectionner les features importantes avec un RandomForest
selector = SelectFromModel(
    RandomForestClassifier(n_estimators=100, random_state=42),
    threshold="mean"  # Garder les features au-dessus de l'importance moyenne
)
selector.fit(X_train, y_train)

selected_features = X_train.columns[selector.get_support()].tolist()
print(f"Features retenues : {len(selected_features)} / {len(X_train.columns)}")

# Ou avec SHAP pour l'interpretabilite
import shap
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_val)
feature_importance = np.abs(shap_values).mean(0)

top_features = pd.DataFrame({
    'feature': X_val.columns,
    'shap_importance': feature_importance
}).sort_values('shap_importance', ascending=False).head(30)
```

---

## Comparaison des Outils AutoML

| Critere | H2O AutoML | AutoGluon | DataRobot | Vertex AI AutoML | SageMaker Autopilot |
|---|---|---|---|---|---|
| **Open source** | Oui | Oui | Non (payant) | Non (payant) | Non (payant) |
| **Facilite** | Moyenne | Elevee | Tres elevee | Elevee | Elevee |
| **Performance** | Tres bonne | Excellente | Tres bonne | Bonne | Bonne |
| **Series temporelles** | Basique | Native (TimeSeriesPredictor) | Oui | Oui | Non natif |
| **Texte / images** | Non | Oui | Oui | Oui | Partiellement |
| **Deploiement integre** | H2O Wave (partiel) | Non natif | Oui (DataRobot MLOps) | Oui (Vertex AI) | Oui (SageMaker) |
| **Monitoring** | Non | Non | Oui | Oui | Oui |
| **Cout** | Gratuit | Gratuit | 50k-200k EUR/an | A l'usage | A l'usage |
| **Adapte pour** | PoC, performance | Benchmarks, PoC | Equipes non techniques, enterprise | Stack GCP | Stack AWS |

---

## Bonnes Pratiques AutoML

### Avant de Lancer l'AutoML

```
[ ] L'audit de qualite des donnees a ete conduit (completude, outliers, drift)
[ ] La variable cible est bien definie et sans leakage temporel
[ ] Les features "futures" (disponibles apres la cible) ont ete retirees
[ ] Les identifiants (customer_id, session_id) ont ete retires des features
[ ] Un split temporel a ete defini (pas un split aleatoire pour les donnees temporelles)
[ ] La metrique d'optimisation correspond a l'objectif metier
[ ] Une baseline simple (logistic regression ou regle metier) est prete pour comparaison
```

### Interpreter les Resultats AutoML

```
[ ] Verifier que le meilleur modele sur le leaderboard bat la baseline simple
[ ] Analyser l'importance des features : les features importantes font-elles sens metier ?
[ ] Verifier la calibration des probabilites (si le modele sort des proba)
[ ] Evaluer la performance sur des sous-groupes critiques (equite)
[ ] Tester la robustesse : le modele performe-t-il si on retire la feature la plus importante ?
[ ] Estimer la latence d'inference avec le modele choisi (ensembles = latence elevee)
```

### Pieges a Eviter

| Piege | Description | Prevention |
|---|---|---|
| **Data leakage** | AutoML inclut des features "futures" dans le modele | Retirer manuellement toutes les features post-date-cible |
| **Split aleatoire** | AutoML fait un split aleatoire sur des donnees temporelles | Configurer explicitement un split temporel |
| **Ensemble impossible a deployer** | Le meilleur modele AutoML est un stacked ensemble de 20 modeles | Utiliser `optimize_for_deployment` ou choisir le 2e modele si plus simple |
| **Monitoring ignore** | Deployer le modele AutoML sans plan de monitoring | Exiger un plan de monitoring avant tout deploiement |
| **Interpretabilite oubliee** | Le modele est un black-box non explicable | Exiger des SHAP values avant tout deploiement en contexte regulatoire |
