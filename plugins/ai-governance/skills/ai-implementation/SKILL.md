---
name: ai-implementation
description: This skill should be used when the user asks about "AI implementation", "AI deployment", "PoC to production", "MLOps pipeline", "model deployment", "AI project execution", "machine learning in production", "AI ROI measurement", "feature store", "model monitoring", "ML CI/CD", "model serving", "AI operationalization", "implementation IA", "deploiement IA", "mise en production IA", "PoC vers production", "pipeline MLOps", "deploiement de modele", "execution projet IA", "machine learning en production", "mesure ROI IA", "feature store", "monitoring de modele", "CI/CD pour modeles", "serving de modele", "operationnalisation IA", "modele en production", "model registry", "model validation", "A/B testing modele", "shadow deployment", "canary model", "batch inference", "online inference", "real-time prediction", "prediction temps reel", "model drift", "data drift", "concept drift", or needs guidance on concretely implementing AI projects from proof-of-concept to production systems.
version: 1.2.0
last_updated: 2026-02
---

# AI Implementation — PoC to Production, MLOps & ROI

## Overview

Ce skill couvre l'execution concrete des projets IA : comment passer d'un proof-of-concept a un systeme en production fiable, comment structurer les pipelines MLOps, comment deployer et monitorer les modeles, et comment mesurer rigoureusement le retour sur investissement des initiatives IA. Il se distingue de ai-governance:strategie-ia (vision, roadmap, organisation) en se concentrant sur l'EXECUTION operationnelle — les choix techniques, les criteres de validation, les patterns de deploiement et les metriques de performance. Appliquer systematiquement les principes decrits ici pour chaque projet IA, depuis la conception du PoC jusqu'au decommissionnement du modele, en privilegiant la fiabilite, la reproductibilite et la valeur metier mesurable.

## When This Skill Applies

Activate this skill when the user:

- Veut faire passer un PoC IA vers la production (criteres de go/no-go, checklist)
- Conçoit ou ameliore un pipeline MLOps (CI/CD pour modeles, feature store, model registry)
- Choisit une strategie de deploiement de modele (batch, online, edge, canary, shadow)
- Veut monitorer un modele en production (data drift, concept drift, performance decay)
- Construit un business case IA chiffre ou mesure le ROI d'une initiative IA
- Configure des outils MLOps (MLflow, Weights & Biases, Kubeflow, Vertex AI, SageMaker)
- Gere le cycle de vie complet d'un modele (entrainement, validation, deploiement, retraining, decommissionnement)
- Rencontre des problemes de qualite de donnees, de regression de modele ou de derive en production

## Core Principles

### Principle 1 — PoC is Not a Product

Un PoC valide une hypothese metier et prouve la faisabilite technique, pas plus. Avant de se lancer dans le developpement production, conduire une evaluation formelle sur trois axes : qualite des donnees (disponibilite, fraicheur, completude), performance du modele (metriques suffisantes pour le cas d'usage, pas seulement l'accuracy), et feasibilite de l'integration (API existantes, contraintes de latence, securite). Le code d'un PoC (notebooks, scripts ad-hoc) doit etre refactore avant toute mise en production — ne jamais deployer directement depuis un notebook Jupyter. Un PoC qui ne passe pas en production dans les 6 mois doit etre raevalue ou abandonne.

### Principle 2 — Reproducibility First

Chaque experiment doit etre reproductible : meme donnees + meme code + meme configuration = memes resultats. Utiliser un framework de tracking des experiments (MLflow, W&B, Neptune) pour logguer systematiquement les hyperparametres, les metriques, les versions de donnees et les artefacts de modele. Versionner les donnees d'entrainement avec DVC, LakeFS ou le systeme de stockage du cloud. Un modele dont les resultats ne sont pas reproductibles est un modele non auditables et non deployable.

### Principle 3 — Test Before You Ship

Appliquer les memes standards de qualite au code ML qu'au code applicatif : tests unitaires pour les fonctions de preprocessing et feature engineering, tests d'integration pour les pipelines end-to-end, tests de regression pour valider que les nouvelles versions n'ont pas de regression de performance. Ajouter des tests specifiques au ML : validation de la distribution des features, detection de data leakage, tests de robustesse (comportement sur des inputs hors distribution), tests d'equite (disparite de performance par sous-groupe). Refuser de deployer sans une suite de tests automatises passant en CI.

### Principle 4 — Deploy Incrementally

Ne jamais basculer 100% du trafic vers un nouveau modele sans validation incrementale. Utiliser systematiquement le shadow deployment (le nouveau modele tourne en parallele sans impacter la production, ses predictions sont loggees et comparees) puis le canary release (exposition progressive : 1%, 5%, 20%, 50%, 100%) avec des metriques de rollback automatique. Definir avant le deploiement les seuils d'alerte qui declenchent un rollback (ex: AUC < 0.75, latence P99 > 200ms, taux d'erreur > 1%). Maintenir toujours la capacite de rollback vers le modele precedent en moins de 5 minutes.

### Principle 5 — Monitor Continuously, Retrain Proactively

Un modele en production se degrade dans le temps : les distributions de donnees changent (data drift), les relations entre features et cible evoluent (concept drift), la performance reelle diverge de la performance offline (train-serve skew). Mettre en place un monitoring en trois couches : monitoring des donnees (distribution des features, volume, qualite), monitoring du modele (predictions, scores de confiance, distribution des outputs), monitoring metier (KPIs business impactes par le modele). Definir et automatiser la politique de retraining : trigger sur alerte de drift, sur degradation de performance, ou sur calendrier fixe (ex: retraining hebdomadaire).

### Principle 6 — Measure Business Value, Not Just Model Metrics

L'AUC ou le RMSE ne sont pas des KPIs metier. Chaque modele en production doit avoir au moins un KPI metier directement lie a ses predictions : taux de churn reduit, conversion augmentee, cout de fraude diminue, delai de traitement reduit. Construire un dashboard de suivi du ROI IA avec : valeur generee (mesure incrementale via A/B test ou comparaison pre/post), couts operationnels (compute, stockage, equipe), et ROI net. Revue trimestrielle obligatoire : tout modele avec ROI < 1x sur 6 mois doit etre optimise ou decommissionne.

## Key Frameworks & Methods

| Framework / Method | Purpose | FR |
|---|---|---|
| **MLflow** | Experiment tracking, model registry, model serving | Suivi d'experiments, registre et serving de modeles |
| **Weights & Biases** | Experiment tracking, hyperparameter tuning, model monitoring | Tracking, tuning et monitoring de modeles |
| **DVC** | Data versioning and pipeline reproducibility | Versionnage des donnees et reproductibilite des pipelines |
| **Kubeflow** | ML orchestration on Kubernetes | Orchestration ML sur Kubernetes |
| **Vertex AI / SageMaker / AzureML** | Managed MLOps platforms | Plateformes MLOps managees |
| **Feature Store (Feast, Tecton, Hopsworks)** | Centralized feature management for ML | Gestion centralisee des features ML |
| **Evidently AI** | Data and model drift monitoring | Monitoring de drift donnees et modele |
| **SHAP / LIME** | Model explainability (feature importance) | Explicabilite des modeles (importance des features) |
| **Great Expectations** | Data validation and quality testing | Validation et test de qualite des donnees |
| **Argo Workflows / Airflow** | ML pipeline orchestration | Orchestration de pipelines ML |

## Decision Guide

### PoC → Production : Criteres de Go / No-Go

Evaluer systematiquement ces criteres avant de valider le passage en production :

| Critere | Go | No-Go | Condition |
|---|---|---|---|
| **Performance modele** | Metriques > seuil defini pre-PoC | Metriques < seuil ou instables | AUC, F1, RMSE selon le type |
| **Qualite des donnees** | Completude > 95%, fraicheur OK | Donnees manquantes > 10% ou perimees | Audit qualite complet |
| **Reproductibilite** | Results stables sur 3 runs independants | Variance significative entre runs | Tests de reproductibilite |
| **Latence** | Inference < SLA defini | Latence > SLA (ex: > 200ms pour online) | Benchmark sur donnees prod |
| **Integration** | API ou batch interface validee | Blocage technique d'integration | Test sur env staging |
| **Equite** | Pas de biais significatif par sous-groupe | Disparite de performance > 10% | Tests de fairness |
| **Securite** | Audit securite passe | Vulnerabilites non corrigees | Pentest ou security review |
| **Rollback** | Procedure de rollback testee | Pas de strategie de retour arriere | Drill de rollback execute |

### Choisir la strategie de deploiement

```
Le modele necessite des predictions en temps reel ?
+-- Oui (latence < 1s)
|   +-- Volume < 1000 req/s -> REST API (FastAPI, Flask, TorchServe)
|   +-- Volume > 1000 req/s -> gRPC + load balancer + cache semantique
|   +-- Contraintes edge/IoT -> Modele embarque (TFLite, ONNX Runtime, CoreML)
+-- Non (latence acceptable > 1 minute)
    +-- Volume < 1M predictions/jour -> Batch inference (Spark, dbt + ML)
    +-- Volume > 1M predictions/jour -> Batch distribue (Spark MLlib, Ray)
    +-- Trigger evenementiel -> Streaming inference (Kafka + modele en consumer)
```

### Choisir l'outil MLOps

| Critere | MLflow | W&B | Vertex AI | SageMaker | AzureML |
|---|---|---|---|---|---|
| **Cloud** | Self-hosted ou cloud-agnostic | Self-hosted ou W&B cloud | GCP | AWS | Azure |
| **Cout** | Open source (infra seule) | Freemium / usage-based | Pay-per-use | Pay-per-use | Pay-per-use |
| **Facilite de prise en main** | Moyen | Facile | Moyen | Complexe | Moyen |
| **Feature Store integre** | Non | Non | Oui (Vertex Feature Store) | Oui (SageMaker Feature Store) | Oui |
| **Model Serving integre** | MLflow Serving | Non natif | Vertex AI Endpoints | SageMaker Endpoints | AzureML Endpoints |
| **Adapte pour** | Equipes cherchant open source | Startups et recherche | Stacks GCP | Stacks AWS | Stacks Azure |

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Two-Tower Architecture pour les Recommandations** : Separer retrieval (modele leger, millions de candidats) et ranking (modele lourd, top-K candidats). Permet de scaler independamment les deux etapes.
- **Feature Store Centralisee** : Partager les features entre entrainement et inference via un feature store (Feast, Tecton, Hopsworks). Elimine le train-serve skew et la duplication de logique de calcul de features.
- **Model Registry avec Etapes de Validation** : Chaque modele passe par les etapes : Staging -> QA -> Production. Aucun modele ne peut aller en production sans validation explicite via le registry.
- **Shadow Deployment** : Faire tourner le nouveau modele en parallele de l'ancien pendant 1-2 semaines avant tout basculement de trafic. Comparer les predictions, detecter les anomalies, valider la performance offline vs online.
- **Champion / Challenger Pattern** : En production, maintenir le modele champion (100% ou 90% du trafic) et le challenger (10% ou moins). Comparer les KPIs metier sur la meme periode. Basculer quand le challenger surpasse le champion.
- **Data Validation au Point d'Entree** : Valider le schema, les types, les plages de valeurs et les distributions des donnees d'inference avant de passer au modele. Rejeter ou flaguer les inputs aberrants plutot que de servir des predictions non fiables.

### Anti-patterns critiques

- **Notebook en Production** : Deployer directement un notebook Jupyter en production sans refactoring. Le code de notebook est difficile a tester, a versionner et a maintenir. Toujours refactorer en modules Python avec tests avant le deploiement.
- **Train-Serve Skew** : Calculer les features differemment entre l'entrainement et l'inference. Les features doivent etre calculees par le meme code (feature store ou fonction partagee). Le train-serve skew est la cause numero 1 de degradation silencieuse des modeles.
- **Pas de Monitoring** : Deployer un modele sans monitoring de drift ni alertes. La degradation est inevitable et silencieuse sans monitoring. Un modele sans monitoring est un modele qui va casser sans qu'on le sache.
- **Retraining Panic** : Retrainer en urgence apres une alerte de drift sans comprendre la cause racine. Le drift peut venir des donnees, du concept, ou d'un bug dans le pipeline. Diagnostiquer avant de retrainer.
- **One-Size-Fits-All Threshold** : Utiliser un seuil de classification fixe (ex: 0.5) pour tous les segments. Optimiser le seuil par segment ou par objectif metier (maximiser le recall pour la fraude, optimiser le F1 pour la satisfaction client).
- **Ignorer la Latence d'Inference** : Developper un modele avec d'excellentes metriques offline sans mesurer la latence en conditions reelles. La latence P99 en production peut etre 10x superieure a la latence moyenne en benchmark.

## Implementation Workflow

### Phase 1 — PoC Rigoureux (Semaines 1-4)

1. Definir le probleme metier avec precision : variable cible, contraintes de performance (latence, recall minimum), donnees disponibles, definition du succes. Ne pas commencer le PoC sans ces elements.
2. Conduire un audit de qualite des donnees (completude, fraicheur, biais, distribution). Si les donnees sont insuffisantes, stopper et investiguer avant de continuer.
3. Developper le modele baseline (modele le plus simple qui pourrait marcher) et le modele cible. Loguer tous les experiments dans MLflow ou W&B.
4. Evaluer la faisabilite de deploiement : latence sur donnees de taille production, integration avec les systemes existants, contraintes securite.
5. Conduire l'evaluation Go/No-Go (voir Decision Guide) et documenter la decision avec les metriques.

### Phase 2 — Preparation Production (Semaines 4-8)

6. Refactorer le code du PoC en modules Python testables : preprocessing, feature engineering, inference. Ecrire les tests unitaires et d'integration.
7. Configurer le pipeline MLOps : tracking des experiments, versionnage des donnees (DVC), model registry (MLflow Registry ou cloud-native).
8. Mettre en place le feature store si plusieurs modeles partagent des features ou si le volume de donnees est significatif.
9. Configurer l'infrastructure de deploiement : endpoint REST API, batch job, ou streaming consumer selon la strategie choisie.
10. Implementer la validation des donnees d'entree (Great Expectations ou schema Pydantic) et la gestion des erreurs d'inference.

### Phase 3 — Deploiement Incremental (Semaines 8-10)

11. Deployer en shadow mode : le nouveau modele tourne en production sans impacter les utilisateurs. Loguer toutes ses predictions et les comparer au modele actuel.
12. Analyser les divergences de predictions entre l'ancien et le nouveau modele. Investiguer les cas ou les deux modeles different significativement.
13. Lancer le canary release : 1% du trafic, monitorer les metriques metier et techniques pendant 48 heures minimum.
14. Escalader progressivement : 5% -> 25% -> 50% -> 100%, avec monitoring continu et seuils de rollback automatique definis.
15. Documenter le deploiement dans le model registry : version, date, metriques de validation, configuration de monitoring.

### Phase 4 — Monitoring et Maintenance (Continu)

16. Activer le monitoring en trois couches : donnees (distribution des features), modele (distribution des predictions, scores de confiance), metier (KPIs impactes).
17. Configurer les alertes de drift avec Evidently AI, WhyLabs ou solution custom. Definir les seuils d'alerte et d'action.
18. Etablir la politique de retraining : trigger sur alerte de drift, sur degradation de performance, ou calendrier (ex: hebdomadaire pour les modeles sur donnees volatiles).
19. Revue mensuelle de performance : comparer les metriques online vs offline, analyser les cas d'erreur, identifier les opportunities d'amelioration.
20. Revue trimestrielle de ROI : valeur generee vs cout operationnel. Decider de l'optimisation ou du decommissionnement.

## Modele de maturite

### Niveau 1 — Ad Hoc
- Modeles en notebooks, deploiement manuel ou inexistant
- Pas de tracking d'experiments, pas de versionnage des modeles
- Pas de monitoring en production, decouverte des problemes par les utilisateurs
- **Indicateurs** : taux PoC-to-production < 10%, MTTR incidents modele > 1 semaine

### Niveau 2 — Structure
- Premier pipeline de deploiement, modeles en production mais peu monitores
- Tracking des experiments partiel (quelques metriques loggees)
- Rollback manuel, detection des problemes par monitoring applicatif basique
- **Indicateurs** : taux PoC-to-production 10-30%, MTTR incidents modele 2-5 jours

### Niveau 3 — Industrialise
- Pipeline MLOps complet : tracking, registry, CI/CD pour modeles, deployment automatise
- Monitoring de drift en place avec alertes, politique de retraining definie
- Shadow deployment et canary release utilises systematiquement
- **Indicateurs** : taux PoC-to-production 30-60%, MTTR incidents modele < 4 heures

### Niveau 4 — Optimise
- Feature store centralise, train-serve skew elimine
- Retraining automatique sur alerte de drift, champion/challenger systematique
- ROI mesure par modele, revue trimestrielle de portefeuille
- **Indicateurs** : taux PoC-to-production > 60%, MTTR incidents modele < 1 heure

### Niveau 5 — Autonome
- AutoML pour la selection de modeles et le tuning d'hyperparametres
- Self-healing pipelines avec rollback automatique sur degradation
- Modeles de nouvelle generation (LLM, agents) avec governance specifique
- **Indicateurs** : taux PoC-to-production > 80%, zero downtime pour les modeles critiques

## Rythme operationnel

| Cadence | Activite | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Quotidien** | Revue des alertes de monitoring (drift, performance, erreurs) | ML Engineer | Log d'alertes et actions correctives |
| **Hebdomadaire** | Revue de performance des modeles en production | Data Scientist + ML Engineer | Rapport de performance hebdo |
| **Hebdomadaire** | Validation des retrainings executes dans la semaine | ML Engineer | Registre des retrainings avec delta de performance |
| **Mensuel** | Revue de qualite des donnees d'inference (distribution, completude) | Data Engineer + ML Engineer | Rapport qualite donnees d'inference |
| **Mensuel** | Post-mortem des incidents modele du mois | ML Lead | Compte-rendu post-mortem et plan d'action |
| **Trimestriel** | Revue ROI du portefeuille de modeles | AI Lead + Product | Scorecard ROI et decisions go/no-go |
| **Annuel** | Audit technique de la plateforme MLOps | AI Architect | Rapport d'audit et roadmap MLOps |

## State of the Art (2025-2026)

L'implementation IA entre dans une phase de maturite industrielle :

- **LLMOps** : Les pipelines pour les LLM (evaluation, red teaming, guardrails, fine-tuning) necessitent des outils specifiques (Langfuse, Phoenix, Ragas) distincts des pipelines ML classiques.
- **AI agents en production** : Le deploiement d'agents autonomes (tool use, multi-step reasoning) requiert des patterns specifiques : sandbox d'execution, monitoring de chaque action, budget d'API plafonne, whitelist d'outils autorises.
- **Feature stores matures** : Tecton, Hopsworks et Feast sont maintenant des standards pour eliminer le train-serve skew a grande echelle, avec support du temps reel et de l'historique point-in-time.
- **Drift detection avancee** : Les outils de monitoring (Evidently, Arize, WhyLabs) integrent des capacites de root cause analysis automatique pour identifier la source du drift.
- **ML Testing mature** : Des frameworks comme Deepchecks et Giskard standardisent les tests de regression, de biais et de robustesse pour les modeles ML.

## Template actionnable

### Checklist PoC → Production

| Phase | Critere | Status | Notes |
|---|---|---|---|
| **Modele** | Metriques > seuil pre-PoC | ☐ | AUC: ___, seuil: ___ |
| **Modele** | Reproductibilite validee (3 runs) | ☐ | |
| **Modele** | Biais / equite testes par sous-groupe | ☐ | |
| **Donnees** | Qualite validee (completude > 95%) | ☐ | |
| **Donnees** | Versionnage des donnees d'entrainement | ☐ | DVC tag: ___ |
| **Code** | Refactoring notebook → modules | ☐ | |
| **Code** | Tests unitaires ecrits et passants | ☐ | Couverture: ___% |
| **Integration** | Latence benchmark sur donnees prod | ☐ | P50: ___ms, P99: ___ms |
| **Integration** | Validation schema des inputs | ☐ | |
| **Deploiement** | Shadow deployment valide | ☐ | Duree: ___ jours |
| **Deploiement** | Monitoring configure (3 couches) | ☐ | |
| **Deploiement** | Procedure de rollback testee | ☐ | |
| **Business** | KPI metier defini et mesurable | ☐ | KPI: ___, baseline: ___ |
| **Business** | ROI projete documente | ☐ | ROI projete: ___ |

## Prompts types

- "Comment faire passer notre modele de churn de PoC a production ?"
- "Aide-moi a configurer un pipeline MLOps avec MLflow"
- "Quels sont les criteres de go/no-go avant de deployer un modele ?"
- "Comment detecter et gerer le data drift en production ?"
- "Propose une strategie de retraining pour notre modele de recommandation"
- "Comment mesurer le ROI de notre modele de scoring credit ?"

## Limites et Red Flags

Ce skill n'est PAS adapte pour :
- Conception de la strategie IA, roadmap ou organisation IA → Utiliser plutot : `ai-governance:strategie-ia`
- Ethique IA, biais algorithmiques, conformite reglementaire → Utiliser plutot : `ai-governance:ai-ethics` ou `ai-governance:ai-risk`
- Architecture de pipelines de donnees, ETL, data warehouse → Utiliser plutot : `data-bi:data-engineering`
- Infrastructure cloud, Kubernetes, CI/CD applicatif → Utiliser plutot : `code-development:devops` ou `code-development:cloud-infrastructure`
- Conception et optimisation de prompts LLM → Utiliser plutot : `ai-governance:prompt-engineering-llmops`

Signaux d'alerte en cours d'utilisation :
- ⚠️ Le modele est deploye directement depuis un notebook sans refactoring ni tests — risque d'instabilite, de manque de reproductibilite et d'impossibilite de maintenance
- ⚠️ Il n'y a aucun monitoring en production — la degradation du modele sera decouverte par les utilisateurs finaux, pas par l'equipe technique
- ⚠️ Le taux de PoC-to-production est inferieur a 20% — symptome d'un manque de rigueur dans la qualification des PoC ou d'obstacles a l'integration en production
- ⚠️ Le ROI IA n'est mesure qu'en termes de metriques techniques (AUC, RMSE) sans KPI metier associe — impossible de justifier les investissements ou de prioriser les modeles

## Skills connexes

| Skill | Lien |
|---|---|
| Strategie IA | `ai-governance:strategie-ia` — Vision, roadmap, organisation et gouvernance IA |
| Prompt Engineering | `ai-governance:prompt-engineering-llmops` — Pipelines LLM et agents IA |
| AI Ethics | `ai-governance:ai-ethics` — Biais, equite et IA responsable |
| AI Risk | `ai-governance:ai-risk` — Risques IA, red teaming, incidents |
| Data Engineering | `data-bi:data-engineering` — Pipelines de donnees pour l'IA |
| DevOps | `code-development:devops` — CI/CD et infrastructure de deploiement |

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[PoC to Production](./references/poc-to-production.md)** : criteres de qualification des PoC, evaluation go/no-go, checklist de validation, passage a l'echelle, gestion des obstacles a la mise en production.
- **[MLOps Implementation](./references/mlops-implementation.md)** : configuration de MLflow et W&B, versionnage des donnees avec DVC, feature store (Feast, Tecton), CI/CD pour modeles ML, Kubeflow et Vertex AI.
- **[ROI Measurement](./references/roi-measurement.md)** : KPIs metier par type de modele, methodologies de mesure du ROI, A/B testing pour les modeles, construction du business case IA, dashboard de suivi ROI.
- **[Deployment Patterns](./references/deployment-patterns.md)** : REST API inference, batch inference, streaming inference, shadow deployment, canary release, champion/challenger, edge deployment, modeles embarques.
- **[Etudes de cas](./references/case-studies.md)** : cas pratiques detailles illustrant l'implementation IA dans differents contextes metier.
