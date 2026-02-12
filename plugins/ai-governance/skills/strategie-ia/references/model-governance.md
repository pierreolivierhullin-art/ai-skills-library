# Model Governance — MLOps Lifecycle, Model Registry, Monitoring & LLM Governance

## Overview

Ce document de reference couvre la gouvernance operationnelle des modeles IA : le cycle de vie MLOps complet, les registres de modeles, la validation et l'approbation, le monitoring en production (data drift, concept drift, performance decay), le decommissionnement, et la gouvernance specifique aux LLM et modeles generatifs. Utiliser ce guide pour etablir et operer un cadre de gouvernance des modeles proportionnel aux risques et a la maturite de l'organisation.

---

## MLOps Lifecycle — Vue d'ensemble

### Les 7 phases du cycle de vie d'un modele

Le cycle de vie d'un modele IA en entreprise couvre sept phases, de la decouverte du cas d'usage au decommissionnement :

```
[1. Problem    [2. Data      [3. Model       [4. Model       [5. Deploy-   [6. Moni-    [7. Decom-
 Framing]  -->  Preparation]  Development] -->  Validation] --> ment]    -->  toring] -->  missioning]
    ^                                                                           |
    |___________________________________________________________________________|
                              Feedback Loop (re-entrainement)
```

#### Phase 1 — Problem Framing

- Definir le probleme metier de maniere precise et mesurable.
- Identifier les KPIs metier et les metriques techniques cibles.
- Evaluer la faisabilite (donnees disponibles, complexite, contraintes).
- Documenter les biais potentiels et les risques ethiques.
- Classifier le niveau de risque (EU AI Act : minimal, limite, haut, inacceptable).
- **Livrable** : AI Project Charter (probleme, KPI, donnees, risques, classification).

#### Phase 2 — Data Preparation

- Collecter et integrer les donnees depuis les sources identifiees.
- Evaluer et ameliorer la qualite des donnees (completude, exactitude, coherence, fraicheur).
- Documenter le lignage des donnees (provenance, transformations, responsable).
- Detecter et traiter les biais dans les donnees d'entrainement.
- Creer les splits train/validation/test avec une strategie de separation rigoureuse (temporelle pour les time series, stratifiee pour les classifications).
- Mettre en place le versioning des datasets (DVC, LakeFS, Delta Lake).
- **Livrable** : Dataset versionne avec documentation (data card), analyse de biais, data quality report.

#### Phase 3 — Model Development

- Selectionner les approches de modelisation (ML classique, deep learning, LLM, ensemble).
- Entrainer et optimiser les hyperparametres (grid search, bayesian optimization, Optuna).
- Tracker les experimentations (MLflow Tracking, Weights & Biases, Neptune).
- Evaluer les metriques sur le jeu de test (accuracy, precision, recall, F1, AUC-ROC, RMSE selon le type de probleme).
- Analyser l'interpretabilite (SHAP, LIME, attention maps).
- Documenter les choix de modelisation et les compromis.
- **Livrable** : Modele candidat avec metriques, experiment tracking, analyse d'interpretabilite.

#### Phase 4 — Model Validation

- Revue par les pairs (code review, architecture review).
- Validation des metriques techniques contre les seuils definis.
- Validation metier : le modele repond-il au besoin formule en Phase 1 ?
- Tests de robustesse : performance sur des sous-populations, edge cases, donnees adversariales.
- Tests d'equite et de biais (demographic parity, equalized odds, fairness metrics).
- Pour les modeles a haut risque : validation par un comite independant (Model Review Board).
- **Livrable** : Model Card complete, rapport de validation, approbation formelle.

#### Phase 5 — Deployment

- Packager le modele (containerisation Docker, format ONNX/TorchServe/Triton).
- Deployer via le pipeline CI/CD (staging -> production avec gates de validation).
- Configurer l'infrastructure de serving (batch, real-time, streaming).
- Mettre en place les strategies de deploiement (canary, blue-green, shadow mode).
- Configurer le rate limiting, le scaling automatique et les fallbacks.
- Documenter les dependances (versions de librairies, modeles de base, config).
- **Livrable** : Modele en production avec pipeline CI/CD, documentation de deploiement.

#### Phase 6 — Monitoring

- Monitorer les metriques techniques en continu (latence, throughput, erreurs, disponibilite).
- Monitorer les metriques de performance du modele (accuracy, drift, degradation).
- Monitorer les metriques metier (impact sur les KPIs cibles).
- Detecter les drifts (data drift, concept drift, prediction drift).
- Configurer les alertes et les seuils d'escalade.
- Planifier les re-entrainements (schedules ou triggered par drift).
- **Livrable** : Dashboard de monitoring, alertes configurees, plan de re-entrainement.

#### Phase 7 — Decommissioning

- Identifier les modeles candidats au decommissionnement (performance degradee, cas d'usage obsolete, remplace par un nouveau modele).
- Planifier la migration des dependances (applications, pipelines, equipes).
- Archiver le modele, les donnees et la documentation (conformite reglementaire : conservation 5-10 ans selon le secteur).
- Communiquer le decommissionnement aux parties prenantes.
- Mettre a jour le registre de modeles.
- **Livrable** : Plan de decommissionnement, archive, confirmation de suppression.

---

## Model Registry — Registre de Modeles

### Role du registre de modeles

Le registre de modeles est le referentiel central qui inventorie tous les modeles IA de l'organisation. Il assure la tracabilite, la gouvernance et la reproductibilite. Chaque modele en production doit etre enregistre.

### Information a capturer par modele

| Categorie | Informations |
|---|---|
| **Identite** | Nom, version, owner, equipe, date de creation, statut (dev/staging/prod/archive) |
| **Technique** | Framework, architecture, hyperparametres, taille, format, dependances |
| **Donnees** | Datasets utilises (versions), features, preprocessing, data card |
| **Performance** | Metriques d'entrainement, validation, test, benchmarks |
| **Gouvernance** | Classification de risque, approbations, audits, Model Card |
| **Lineage** | Pipeline d'entrainement, experiment tracking, artefacts |
| **Deploiement** | Endpoint(s), infrastructure, config de serving, SLA |
| **Monitoring** | Metriques en production, drift detecte, re-entrainements |

### Outils de Model Registry (2024-2026)

#### MLflow Model Registry

MLflow est la solution open-source la plus adoptee pour le tracking d'experimentations et le registre de modeles.

Fonctionnalites cles :
- **Experiment Tracking** : log des parametres, metriques, artefacts pour chaque run.
- **Model Registry** : enregistrement, versioning, staging (None -> Staging -> Production -> Archived).
- **Model Serving** : deploiement en tant que REST API ou batch scoring.
- **Model Lineage** : tracabilite complete de l'experimentation au deploiement.

Exemple de workflow MLflow :

```python
import mlflow

# Configuration du tracking (utiliser un serveur centralise, pas de fichiers locaux)
mlflow.set_tracking_uri("https://mlflow.internal.example.com")
mlflow.set_experiment("churn-prediction-v2")

with mlflow.start_run(run_name="xgboost-optimized"):
    # Log des parametres
    mlflow.log_params({
        "model_type": "xgboost",
        "max_depth": 6,
        "learning_rate": 0.1,
        "n_estimators": 200
    })

    # Entrainement (pseudo-code)
    # model = train_model(X_train, y_train, params)
    # metrics = evaluate_model(model, X_test, y_test)

    # Log des metriques
    mlflow.log_metrics({
        "accuracy": 0.89,
        "precision": 0.85,
        "recall": 0.82,
        "f1_score": 0.83,
        "auc_roc": 0.92
    })

    # Log du modele dans le registry
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="churn-prediction"
    )

# Transition du modele vers Production (apres validation)
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="churn-prediction",
    version=3,
    stage="Production"
)
```

#### Weights & Biases (W&B)

W&B est une plateforme SaaS de ML experiment tracking, model registry et monitoring, particulierement adoptee pour le deep learning et les LLM.

Fonctionnalites cles :
- **Experiment Tracking** : visualisation interactive des metriques, comparaison de runs.
- **Artifacts** : versioning des datasets, modeles, et artefacts avec lignage automatique.
- **Model Registry** : gestion du cycle de vie avec linking vers les artefacts.
- **Tables** : exploration interactive des donnees et des predictions.
- **Sweeps** : hyperparameter optimization integree.
- **Launch** : orchestration de jobs d'entrainement sur le cloud.

#### Autres solutions notables

- **Vertex AI Model Registry** (GCP) : integre nativement dans l'ecosysteme Google Cloud, gestion du cycle de vie, deploiement en un clic.
- **SageMaker Model Registry** (AWS) : integre dans SageMaker, approbation de modeles, CI/CD natif.
- **Azure ML Model Registry** : integre dans Azure ML, connexion avec Azure DevOps.
- **DVC (Data Version Control)** : open source, versioning de donnees et modeles avec Git, leger et flexible.
- **Neptune.ai** : SaaS specialise dans le tracking d'experimentations, particulierement pour la recherche.

---

## Model Validation & Approval

### Model Card

Chaque modele deploye en production doit avoir une Model Card complete. La Model Card est le document de reference qui decrit le modele, ses performances, ses limites et ses risques.

Structure recommandee (inspiree de Google Model Cards, 2019) :

```markdown
# Model Card — [Nom du modele]

## Model Details
- **Nom** : churn-prediction-v2
- **Version** : 2.3.1
- **Owner** : equipe Data Science Marketing
- **Date de creation** : 2025-03-15
- **Framework** : XGBoost 2.0
- **Type** : Classification binaire

## Intended Use
- **Usage prevu** : predire le churn des clients B2B dans les 90 jours
- **Utilisateurs prevus** : equipe CRM, managers commerciaux
- **Usage non prevu** : ne pas utiliser pour des decisions RH ou de credit

## Training Data
- **Source** : base CRM interne (3 ans d'historique)
- **Taille** : 150k exemples (85% non-churn, 15% churn)
- **Features** : 45 features (usage produit, interactions support, profil client)
- **Biais connus** : sous-representation des PME (< 10% du dataset)

## Performance Metrics
| Metrique | Global | Segment Grands Comptes | Segment PME |
|---|---|---|---|
| Accuracy | 0.89 | 0.91 | 0.83 |
| Precision | 0.85 | 0.88 | 0.79 |
| Recall | 0.82 | 0.85 | 0.74 |
| AUC-ROC | 0.92 | 0.94 | 0.86 |

## Limitations & Risks
- Performance reduite sur le segment PME (manque de donnees)
- Ne capte pas les evenements macro-economiques
- Feature "nb_tickets_support" peut etre biaisee par la qualite du support

## Ethical Considerations
- Pas de variables sensibles directes (genre, age, origine)
- Risque de proxy discrimination via la variable "secteur d'activite"
- Impact : score utilise pour prioriser les actions de retention, pas de decision automatique

## Risk Classification
- **EU AI Act** : risque minimal (outil d'aide a la decision, pas de decision automatisee)
- **Tier interne** : Tier 2 (important mais pas business-critical)
```

### Model Review Board

Pour les modeles a haut risque (Tier 1 ou EU AI Act haut risque), mettre en place un comite de validation (Model Review Board) :

**Composition** :
- Head of AI / Chief AI Officer (president)
- Data Science lead (expertise technique)
- Business owner (validation metier)
- Risk / Compliance (evaluation des risques)
- Legal (conformite reglementaire)
- Ethics representative (biais, equite)

**Processus de revue** :
1. Soumission du dossier par l'equipe data (Model Card + rapport de validation + code review).
2. Revue technique (24-48h) : metriques, robustesse, interpretabilite.
3. Revue metier et risque (24-48h) : adequation au besoin, risques, impacts.
4. Decision : approuve / approuve avec reserves / rejete (avec feedback).
5. Frequence : bimensuelle pour les soumissions regulieres, ad hoc pour les urgences.

---

## Model Monitoring — Deep Dive

### Types de drift

#### Data Drift (Covariate Shift)

La distribution des features d'entree change par rapport aux donnees d'entrainement, sans que la relation feature-cible ne change.

**Causes** : evolution des comportements clients, changement saisonnier, modification d'un processus en amont, bug dans un pipeline de donnees.

**Detection** :
- **Tests statistiques** : Kolmogorov-Smirnov (numeriques), Chi-square (categoriques), Population Stability Index (PSI).
- **Seuils** : PSI < 0.1 (pas de drift), 0.1-0.2 (drift modere, investiguer), > 0.2 (drift significatif, agir).
- **Frequence** : quotidienne pour les modeles temps reel, hebdomadaire pour les modeles batch.

#### Concept Drift

La relation entre les features et la cible change (le "concept" appris par le modele evolue).

**Causes** : changement de marche, nouvelle reglementation, evolution des preferences, evenement inattendu (pandemie, crise).

**Types de concept drift** :
- **Sudden** : changement brutal (ex : nouvelle reglementation). Detection : chute soudaine des metriques.
- **Gradual** : changement progressif (ex : evolution des gouts). Detection : degradation lente des metriques sur plusieurs semaines.
- **Recurring** : patterns cycliques (ex : saisonnalite). Detection : correlation avec le calendrier.
- **Incremental** : micro-changements cumulatifs. Detection : comparaison des metriques sur des fenetres glissantes.

**Detection** :
- Monitorer les metriques de performance (accuracy, precision, recall) sur des fenetres temporelles glissantes.
- Comparer les distributions de predictions (prediction drift) : un changement dans la distribution des predictions peut indiquer un concept drift.
- Pour les modeles supervises avec ground truth disponible : comparer les predictions aux vrais labels avec un lag.

#### Performance Decay

Degradation progressive des performances du modele, souvent causee par une combinaison de data drift et concept drift.

**Metriques a surveiller** :
- Metriques de classification : accuracy, precision, recall, F1, AUC-ROC.
- Metriques de regression : RMSE, MAE, MAPE.
- Metriques de ranking : NDCG, MAP, MRR.
- Metriques operationnelles : latence p50/p95/p99, taux d'erreur, throughput.

**Seuils et alertes** :

| Niveau | Condition | Action |
|---|---|---|
| **Info** | Degradation < 5% relative | Log, monitorer |
| **Warning** | Degradation 5-10% relative | Investigation, analyse de drift |
| **Critical** | Degradation > 10% relative | Re-entrainement urgent, fallback |
| **Emergency** | Modele non fonctionnel | Rollback vers version precedente |

### Infrastructure de monitoring

Architecture recommandee pour le monitoring de modeles :

```
[Model in Production]
        |
        v
[Prediction Logger]  --> [Data Store (time-series)]
        |
        v
[Drift Detector]     --> [Alert Manager (PagerDuty, Slack)]
        |
        v
[Performance Tracker] --> [Dashboard (Grafana, custom)]
        |
        v
[Re-training Trigger] --> [Training Pipeline (scheduled or triggered)]
```

### Outils de monitoring (2024-2026)

| Outil | Type | Forces |
|---|---|---|
| **Evidently AI** | Open source | Drift detection, data quality, model performance. Excellent pour commencer. |
| **WhyLabs / WhyLogs** | Open source + SaaS | Profiling de donnees, drift detection, monitoring leger. |
| **Arize AI** | SaaS | Monitoring complet, troubleshooting, embeddings. |
| **Fiddler AI** | SaaS | Explainability + monitoring, biais, conformite. |
| **NannyML** | Open source | Detection de drift sans ground truth (performance estimation). |
| **Prometheus + Grafana** | Open source | Metriques operationnelles (latence, throughput, erreurs). |
| **Great Expectations** | Open source | Data quality monitoring (validation des donnees en entree). |

### Strategie de re-entrainement

Trois approches, non mutuellement exclusives :

1. **Scheduled re-training** : re-entrainement periodique (quotidien, hebdomadaire, mensuel). Simple a implementer, mais peut etre insuffisant en cas de drift soudain ou trop frequent si le modele est stable.

2. **Triggered re-training** : re-entrainement declenche par une alerte de drift ou de degradation de performance. Plus reactif, mais necessite un monitoring fiable et des seuils bien calibres.

3. **Continuous training** : re-entrainement continu sur les nouvelles donnees (online learning, incremental learning). Optimal pour les modeles a haute frequence mais complexe a implementer et a valider.

**Recommandation** : combiner scheduled (mensuel) et triggered (sur alerte de drift) pour la majorite des cas. Reserver le continuous training aux cas d'usage avec des flux de donnees massifs et une ground truth disponible en temps reel.

---

## LLM-Specific Governance (2024-2026)

### Specificites de la gouvernance LLM

Les Large Language Models (LLM) presentent des defis de gouvernance specifiques par rapport au ML classique :

| Dimension | ML classique | LLM |
|---|---|---|
| **Entrainement** | Modele entraine sur des donnees internes | Foundation model pre-entraine, fine-tuning optionnel |
| **Donnees** | Dataset controle | Donnees d'entrainement du foundation model inconnues/opaques |
| **Evaluation** | Metriques quantitatives claires | Evaluation multidimensionnelle (qualite, factualite, securite, biais) |
| **Comportement** | Deterministe (meme entree -> meme sortie) | Stochastique, sensible au prompt |
| **Risques** | Drift, biais connus | Hallucinations, prompt injections, fuite de donnees, biais amplifies |
| **Versioning** | Version du modele | Version du modele + version du prompt + version des guardrails |

### Cadre de gouvernance LLM

#### 1. Politique d'usage LLM

Definir une politique d'usage claire couvrant :

- **Donnees autorisees** : quelles donnees peuvent etre envoyees au LLM ? Distinguer : donnees publiques (OK), donnees internes non-sensibles (OK avec API privee), donnees sensibles/personnelles (interdit ou avec anonymisation).
- **Cas d'usage autorises** : categoriser les usages (approuve, conditionnel, interdit). Exemple : redaction email (approuve), scoring credit automatique (interdit), synthese de documents internes (conditionnel).
- **Validation humaine** : pour quels cas d'usage un humain doit-il valider la sortie du LLM avant utilisation ?
- **Attribution** : les contenus generes par IA doivent-ils etre marques comme tels ?

#### 2. Architecture de securite LLM

```
[Utilisateur]
     |
     v
[Input Guardrails]
  - PII detection & masking (presidio, regex)
  - Prompt injection detection
  - Topic/content filtering
  - Rate limiting per user
     |
     v
[LLM Gateway]
  - Auth & authorization
  - Model routing (cost/quality optimization)
  - Request/response logging (avec masking PII)
  - Cost tracking per team/project
     |
     v
[LLM Provider / Self-hosted]
     |
     v
[Output Guardrails]
  - Hallucination detection (grounding check)
  - Content safety (toxicity, bias)
  - PII detection in output
  - Format validation (JSON schema, etc.)
     |
     v
[Utilisateur]
```

#### 3. Evaluation des LLM

L'evaluation des LLM est un domaine en evolution rapide. Cadre d'evaluation recommande :

| Dimension | Metriques | Outils |
|---|---|---|
| **Qualite** | Coherence, relevance, completeness, style | LLM-as-judge, human evaluation |
| **Factualite** | Groundedness, citation accuracy, hallucination rate | RAG evaluation (RAGAS), fact-checking |
| **Securite** | Prompt injection resistance, jailbreak resistance | Red teaming, adversarial testing, Garak |
| **Biais** | Demographic bias, stereotypes, fairness | Bias benchmarks, human audit |
| **Performance** | Latence, throughput, cost per query | Load testing, monitoring |
| **Conformite** | RGPD, EU AI Act, politique d'usage | Compliance audit, automated checks |

Evaluer sur un benchmark interne representatif des cas d'usage reels. Ne pas se fier uniquement aux benchmarks publics (MMLU, HumanEval) qui ne refletent pas le contexte specifique.

#### 4. Prompt Management

Gerer les prompts comme du code :

- **Versioning** : versionner les prompts dans un repository Git dedie (ou colocated avec le code applicatif).
- **Testing** : tester les prompts sur un jeu d'evaluation avant deploiement (regression testing).
- **Review** : revue par les pairs pour les prompts en production (comme le code review).
- **Monitoring** : tracker les versions de prompts deployees, les metriques de qualite par version.
- **Separation** : separer les prompts systeme (geres par l'equipe IA) des prompts utilisateur (variables).

#### 5. RAG Governance

Pour les systemes Retrieval-Augmented Generation (RAG) :

- **Source management** : inventorier et qualifier les sources de donnees indexees (fraicheur, fiabilite, droits).
- **Chunk strategy** : documenter la strategie de chunking (taille, overlap, methode) et son impact sur la qualite.
- **Embedding versioning** : versionner les modeles d'embedding et re-indexer quand necessaire.
- **Retrieval evaluation** : mesurer la qualite du retrieval (precision@k, recall@k, MRR) separement de la generation.
- **Attribution** : chaque reponse RAG doit citer ses sources pour permettre la verification.
- **Access control** : le RAG doit respecter les permissions d'acces aux documents sources (RBAC sur les chunks).

---

## Model Tiering & Proportionate Governance

### Systeme de classification par tiers

Appliquer une gouvernance proportionnee au risque et a l'impact du modele :

| | Tier 1 — Critical | Tier 2 — Important | Tier 3 — Standard | Tier 4 — Experimental |
|---|---|---|---|---|
| **Impact** | Decision automatisee, risque financier/reputationnel eleve | Decision assistee, impact metier significatif | Optimisation, aide operationnelle | PoC, experimentation interne |
| **Exemples** | Scoring credit, detection fraude, pricing automatique | Churn prediction, recommandation produit, forecasting | Classification de tickets, extraction de donnees | Prototypes, analyses exploratoires |
| **Model Card** | Complete + audit externe | Complete | Simplifiee | Non requise |
| **Validation** | Model Review Board | Peer review + business owner | Peer review | Self-review |
| **Monitoring** | Temps reel, alertes critiques | Quotidien, alertes warning | Hebdomadaire | Mensuel |
| **Re-entrainement** | Triggered + scheduled (hebdomadaire) | Scheduled (mensuel) | Scheduled (trimestriel) | Ad hoc |
| **Audit trail** | Complet (5+ ans) | Complet (3 ans) | Partiel (1 an) | Non requis |
| **EU AI Act** | Haut risque | Risque limite | Risque minimal | N/A |

### Processus de classification

1. Evaluer l'impact de la decision du modele (financier, operationnel, reputationnel, humain).
2. Evaluer le niveau d'automatisation (informatif, assistif, decisif, autonome).
3. Verifier la classification EU AI Act si applicable.
4. Croiser les criteres pour determiner le tier.
5. Documenter la classification et la justification dans le registre de modeles.
6. Revoir la classification annuellement ou lors de changements significatifs.

---

## Model Decommissioning

### Criteres de decommissionnement

Declencher le processus de decommissionnement quand :

- Le modele a ete **remplace** par une version plus performante (et la migration est complete).
- Le **cas d'usage** n'existe plus (produit arrete, processus modifie).
- Les **performances** sont degradees de maniere irreversible et le re-entrainement n'est pas viable.
- Le **cout de maintenance** depasse la valeur generee.
- Le modele est **non conforme** a une nouvelle reglementation et ne peut pas etre adapte.

### Processus de decommissionnement

1. **Annonce** : notifier les parties prenantes 30-60 jours avant le decommissionnement.
2. **Migration** : verifier que toutes les applications dependantes ont migre vers le remplacement ou un fallback.
3. **Archive** : archiver le modele, les donnees d'entrainement, la documentation et les logs de monitoring (duree de retention selon le tier et la reglementation).
4. **Nettoyage** : supprimer l'infrastructure de serving, les endpoints, les pipelines associes.
5. **Registre** : mettre a jour le statut dans le registre de modeles (Archived/Decommissioned).
6. **Post-mortem** : documenter les lessons learned (performance, couts, adoption, raisons du decommissionnement).
