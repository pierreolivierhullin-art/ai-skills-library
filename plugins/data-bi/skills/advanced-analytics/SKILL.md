---
name: advanced-analytics
description: This skill should be used when the user asks about "predictive analytics", "machine learning business", "churn prediction", "customer lifetime value", "demand forecasting", "customer segmentation", "RFM analysis", "clustering", "AutoML", "A/B testing", "statistical significance", "uplift modeling", "propensity scoring", "lead scoring", "fraud detection ML", "recommendation engine", "next best action", "causal inference", "analytique predictive", "machine learning metier", "prediction de churn", "valeur vie client", "prevision de demande", "segmentation client", "analyse RFM", "clustering", "AutoML", "test A/B", "significance statistique", "modelisation d'uplift", "scoring de propension", "scoring de leads", "detection de fraude ML", "moteur de recommandation", "prochaine meilleure action", "inference causale", "modele predictif", "ML applique", "science des donnees metier", "business data science", or needs guidance on applying machine learning and statistics to business problems for prediction, segmentation, and experimentation.
version: 1.2.0
last_updated: 2026-02
---

# Advanced Analytics — Predictive ML, Segmentation & Business Experimentation

## Overview

**FR** — Ce skill couvre l'application du machine learning et des methodes statistiques aux problemes metier concrets : prediction (churn, LTV, demande), segmentation (RFM, clustering, personas), scoring (leads, propension, fraude), et experimentation (A/B testing, inference causale, uplift modeling). L'objectif n'est pas le ML de recherche ni le deep learning academique, mais le ML applique operationnel — les modeles qui tournent en production, genèrent de la valeur mesurable et peuvent etre compriss et actiones par les equipes metier. Chaque recommandation privilegia la simplicite et l'interpretabilite sur la complexite, la valeur metier sur la performance technique, et la rigueur statistique sur les intuitions.

**EN** — This skill covers the application of machine learning and statistical methods to concrete business problems: prediction (churn, LTV, demand), segmentation (RFM, clustering, personas), scoring (leads, propensity, fraud), and experimentation (A/B testing, causal inference, uplift modeling). The goal is not research ML or academic deep learning, but operational applied ML — models that run in production, generate measurable value, and can be understood and acted upon by business teams.

---

## When This Skill Applies

Activate this skill when the user:

- Veut construire un modele predictif metier (churn, LTV, demande, scoring de leads)
- Veut segmenter sa base client ou ses produits (RFM, k-means, clustering hierarchique)
- Analyse les resultats d'un A/B test ou veut en concevoir un
- Cherche a mesurer l'impact causal d'une action (uplift modeling, DiD, regression discontinuite)
- Veut automatiser la selection et l'optimisation de modeles (AutoML)
- Construit un systeme de recommandation ou de next-best-action
- Applique des techniques statistiques aux donnees metier (regression, classification, time series)
- A besoin de rendre des modeles ML interpretables et actionnables pour les equipes metier

---

## Core Principles

### 1. Start Simple, Add Complexity Only If Needed
Commencer toujours par le modele le plus simple qui pourrait marcher : regression logistique, decision tree, modele de gradient boosting simple. La complexite ne se justifie que si elle apporte un gain de performance mesurable sur les metriques metier. Un modele interpretable a 85% d'AUC est preferable a un modele black-box a 87% si les equipes metier doivent comprendre et agir sur ses sorties. / Always start with the simplest model that could work. Complexity is only justified by measurable business metric improvement.

### 2. Business Metric First, Model Metric Second
L'AUC, le RMSE ou l'accuracy ne sont pas des KPIs metier. Definir d'abord le KPI metier impacte (taux de churn reduit, revenus additionnels, couts evites), puis choisir les metriques de modele alignees avec cet objectif. Un modele de churn avec un recall de 80% sur les churners est meilleur qu'un modele avec une accuracy de 95% si l'accuracy est tirée par la majorite des non-churners. / Business KPI first, model metrics second. Align model metrics with the business objective.

### 3. Understand Your Data Before Modeling
Consacrer au moins 30% du temps d'un projet ML a l'analyse exploratoire et la comprehension des donnees. Detecter les outliers, les valeurs manquantes, les biais de selection, les fuites de donnees (features qui "connaissent" la cible). Un modele entraine sur des donnees biaisees ou avec du data leakage donnera des resultats trompeurs en production. / Spend at minimum 30% of project time on EDA and data understanding before modeling.

### 4. Validate Out-of-Time, Not Just Out-of-Sample
Pour les modeles sur donnees temporelles, utiliser une validation temporelle (out-of-time) plutot qu'un split aleatoire. Diviser les donnees par periode : entrainement sur T-24 a T-6 mois, validation sur T-6 a T-3 mois, test sur T-3 mois a aujourd'hui. Un split aleatoire sur des donnees temporelles cree du leakage temporel et surestime les performances. / For time-series data, always use out-of-time validation, never random splits.

### 5. Make Models Actionable
Un modele predictif n'a de valeur que s'il genere des actions. Pour chaque modele, definir : quelles actions sont declenchees par les predictions (ex: une propension d'achat > 0.7 declenche un email de retargeting), qui prend ces actions (equipes marketing, commercial, support), et comment mesurer l'impact de ces actions. Presenter les resultats en termes metier : "parmi les 1000 clients a haut risque de churn, contacter les 200 avec le plus fort LTV attendu". / Every model must map to specific actions. Define who acts, on what trigger, and how impact is measured.

### 6. Experiment Rigorously
Mesurer l'impact incremental des modeles par experimentation controlee. Un A/B test bien concu est la seule methode rigoureuse pour mesurer la causalite. Definir la taille d'echantillon, la duree et les metriques avant de lancer l'experience. Ne pas arreter l'experience prematuremment au premier resultat significatif (peeking problem). Utiliser des methodes bayesiennes si la rapidite de decision prime sur la rigueur frequentiste. / Use randomized controlled experiments to measure incremental impact. Pre-register hypotheses and sample sizes.

---

## Key Frameworks & Methods

| Framework / Method | Purpose | FR |
|---|---|---|
| **XGBoost / LightGBM** | Gradient boosting for tabular data | Gradient boosting pour donnees tabulaires |
| **scikit-learn** | General-purpose ML library | Bibliotheque ML generaliste |
| **Prophet / NeuralProphet** | Time series forecasting | Prevision de series temporelles |
| **RFM Analysis** | Customer segmentation by behavior | Segmentation client par comportement |
| **k-means / DBSCAN** | Unsupervised clustering | Clustering non supervise |
| **SHAP** | Model explainability | Explicabilite des modeles |
| **H2O AutoML / AutoGluon** | Automated model selection | Selection automatique de modeles |
| **CausalML / DoWhy** | Causal inference and uplift modeling | Inference causale et modelisation d'uplift |
| **Lifetimes (BG/NBD)** | Customer LTV and churn probability | LTV client et probabilite de churn |
| **statsmodels** | Statistical modeling and testing | Modelisation statistique et tests |

---

## Decision Guide

### Choisir le type de modele selon le probleme

```
Quel est le type de probleme metier ?
+-- Predire un evenement binaire (churn, fraude, conversion)
|   +-- Classe desequilibree (< 10% de positifs) -> XGBoost + resampling (SMOTE)
|   +-- Classes equilibrees -> Regression logistique (base) + XGBoost (prod)
+-- Predire une valeur continue (LTV, revenu, prix)
|   +-- Donnees tabulaires -> XGBoost Regressor, LightGBM
|   +-- Series temporelles -> Prophet, ARIMA, XGBoost avec features temporelles
+-- Segmenter sans variable cible (clustering)
|   +-- Nombre de segments connu -> k-means
|   +-- Nombre de segments inconnu -> DBSCAN, clustering hierarchique
|   +-- Segmentation metier immediate -> RFM (Recency, Frequency, Monetary)
+-- Mesurer l'impact causal d'une intervention
|   +-- Randomisation possible -> A/B test classique
|   +-- Randomisation impossible -> DiD, regression discontinuite, PSM
|   +-- Mesurer l'impact par segment -> Uplift modeling (meta-learner T/S/X)
+-- Recommander des items ou actions
|   +-- Collaborative filtering -> ALS (implicit feedback), SVD
|   +-- Contenu -> Embeddings + similarite cosinus
|   +-- Hybrid -> Deux tours (retrieval + ranking)
```

### Choisir entre frequentiste et bayesien pour l'A/B testing

| Critere | Frequentiste | Bayesien |
|---|---|---|
| **Principe** | p-value < 0.05 = significatif | Probabilite que A > B |
| **Decision** | Binaire (go/no-go) | Continue (probabilite) |
| **Duree de test** | Fixe, pre-determinee | Peut etre arrete plus tot |
| **Interpretation** | "Probabilite d'observer ces resultats si H0 vraie" | "Probabilite que B soit meilleur que A" |
| **Avantage** | Standard, bien compris | Stoppage anticipé, intuition |
| **Recommande pour** | Tests formels, conformite, decisions irreversibles | Tests rapides, iterations frequentes |

### Metriques par type de modele

| Type de modele | Metrique principale | Metriques secondaires |
|---|---|---|
| **Classification** | AUC-ROC | Precision, Recall, F1 par seuil |
| **Classification desequilibree** | AUC-PR (Precision-Recall) | Recall@K (top K %), F1 |
| **Regression** | RMSE | MAE, MAPE, R² |
| **Ranking/Recommendation** | NDCG@K | MRR, Recall@K, Coverage |
| **Clustering** | Silhouette score | Davies-Bouldin, cohesion metier |
| **Time Series** | MAPE | RMSE, SMAPE, backtest accuracy |

---

## Common Patterns & Anti-Patterns

### Patterns (Do)
- **RFM comme Point de Depart de la Segmentation** : Calculer Recency (derniere transaction), Frequency (nombre de transactions), Monetary (valeur totale) sur la base client. Scorer chaque dimension de 1 a 5, combiner pour obtenir un score RFM. Simple, interpretable, directement actionnable par les equipes marketing et CRM.
- **Validation Temporelle Stricte** : Pour tout modele sur donnees temporelles, creer un split par periode (train/validation/test sur periodes consecutives), jamais aleatoire. Simuler les conditions reelles de prediction : le modele ne peut utiliser que les donnees disponibles au moment de la prediction.
- **SHAP pour l'Explicabilite** : Utiliser SHAP (SHapley Additive exPlanations) pour expliquer les predictions individuelles et l'importance globale des features. Presenter les explications en termes metier (ex: "la propension d'achat est elevee car le client a visite la page produit 3 fois cette semaine").
- **Calibration du Modele** : Verifier et calibrer les probabilites sortant du modele (Platt scaling ou isotonic regression). Un modele de churn qui predit 70% de probabilite doit effectivement choisir 70% du temps. La calibration est essentielle pour le scoring et la prise de decision.
- **Baseline Simple Obligatoire** : Toujours comparer le modele ML a une baseline simple (moyenne historique, derniere valeur observee, regle metier existante). Si le modele ne bat pas la baseline, c'est un signal d'alerte sur la qualite des donnees ou la formulation du probleme.
- **Feature Engineering Metier** : Investir dans la creation de features a partir de la connaissance metier : ratios, lags temporels, agregations sur differentes fenetres, interactions entre variables. Les features bien construites ont souvent plus d'impact que le choix du modele.

### Anti-Patterns (Avoid)
- **Data Leakage** : Inclure dans les features d'entrainement des informations non disponibles au moment de la prediction (ex: inclure le statut de churn futur dans les features d'un modele de churn). Le data leakage produit des metriques excellentes en training mais une performance catastrophique en production.
- **Classe Desequilibree Ignoree** : Sur un probleme de fraude (0.1% de positifs), un modele qui predit toujours "non fraude" a 99.9% d'accuracy. Utiliser AUC-PR, F1, ou les metriques de recall sur les positifs. Appliquer des techniques de reequilibrage (SMOTE, class weighting).
- **Overfitting au Jeu de Validation** : Optimiser les hyperparametres en regardant les resultats du jeu de test (cherry-picking), puis annoncer les resultats du test comme non biaises. Le jeu de test doit etre touche exactement une fois, a la fin.
- **Ignorer la Distribution de Production** : Entrainer sur des donnees historiques sans verifier que la distribution correspond aux donnees de production actuelles. Les changements de comportement utilisateur, les modifications de produit ou les biais de selection peuvent rendre le modele obsolete immediatement.
- **A/B Test Premature** : Arreter un A/B test des qu'il montre une significativite statistique, avant d'avoir atteint la taille d'echantillon pre-calculee. Le peeking problem gonfle le taux de faux positifs a plus de 25% pour des tests surveilles quotidiennement.
- **Complexite Injustifiee** : Deployer un deep learning ou un ensemble complexe pour un probleme ou une regression logistique obtient 83% d'AUC contre 85% pour le modele complexe. La difference de 2 points ne justifie pas la complexite additionnelle de maintenance, d'interpretation et de monitoring.

---

## Implementation Workflow

Follow this workflow when building a predictive or segmentation analytics project:

1. **Definir le Probleme Metier** — Identifier precisement la variable cible, l'horizon de prediction, les donnees disponibles, et le KPI metier qui sera impacte. Ecrire une definition du succes measurable avant tout code.

2. **Audit des Donnees (EDA)** — Analyser la distribution de la variable cible (desequilibre ?), les valeurs manquantes, les outliers, la qualite temporelle, les correlations entre variables. Detecter les signaux de data leakage potentiel.

3. **Feature Engineering** — Construire les features a partir de la connaissance metier : agregations temporelles (somme, moyenne, max sur 7/30/90 jours), ratios, lags, interactions. Documenter chaque feature avec son interpretation metier.

4. **Modele Baseline** — Implémenter la baseline la plus simple : regle metier existante, moyenne historique, ou modele de regression logistique. Etablir les metriques de reference a battre.

5. **Modelisation** — Experimenter avec XGBoost, LightGBM ou Random Forest. Utiliser une validation croisee temporelle. Loguer tous les experiments dans MLflow ou W&B. Optimiser les hyperparametres avec Optuna ou HyperOpt.

6. **Evaluation et Validation** — Evaluer sur le jeu de test temporel (jamais touche pendant le developpement). Verifier la calibration des probabilites. Conduire les analyses SHAP pour l'explicabilite. Valider avec les experts metier.

7. **Segmentation (si applicable)** — Executer RFM pour la segmentation rapide. Pour le clustering, determiner le nombre optimal de clusters (methode du coude, silhouette score), entrainer k-means, valider la coherence metier de chaque segment.

8. **Action Design** — Pour chaque segment ou decile de prediction, definir les actions associees (email, offre, appel), les equipes responsables, et les metriques de suivi. Presenter les resultats en termes metier (ex: "top 10% des clients a risque de churn = 1,200 clients, LTV moyen de 450 euros").

9. **Experimentation** — Concevoir un A/B test pour mesurer l'impact incremental du modele. Calculer la taille d'echantillon requise. Definir la duree et les metriques primaires et secondaires. Ne pas lancer sans pre-enregistrement des hypotheses.

10. **Monitoring et Iteration** — Monitorer les distributions des features et des predictions en production. Definir la politique de retraining. Analyser les erreurs (faux positifs, faux negatifs) pour identifier les opportunites d'amelioration.

---

## Modele de maturite

### Niveau 1 — Descriptif
- Reporting historique et dashboards, pas de prediction
- Excel et SQL pour l'analyse, pas de ML
- Decisions basees sur l'intuition et les metriques passees
- **Indicateurs** : zero modeles en production, pas de culture de l'experimentation

### Niveau 2 — Premiers Modeles
- Premiers modeles de scoring ou segmentation en place (RFM, scoring simple)
- Utilisation d'outils BI avec quelques fonctions predictives (Google Analytics, Salesforce Einstein)
- A/B testing ad hoc sans processus rigoureux
- **Indicateurs** : 1-3 modeles en production, experimentation peu rigoureuse

### Niveau 3 — ML Operationnel
- Pipeline ML en production : churn, LTV, scoring de leads
- A/B testing rigoureux avec calcul de taille d'echantillon et suivi de significativite
- Segmentation data-driven avec actions associees
- **Indicateurs** : 5-15 modeles en production, experimentation systematique

### Niveau 4 — ML Avance
- Uplift modeling pour mesurer l'impact incremental
- AutoML pour l'exploration rapide de nouveaux cas d'usage
- Recommandation personnalisee en temps reel
- **Indicateurs** : 15-50 modeles en production, ROI mesure par modele

### Niveau 5 — Decision Automatisee
- Next-Best-Action en temps reel sur tous les canaux
- Experimentation adaptative (bandits multi-bras)
- Causal inference integree aux decisions metier
- **Indicateurs** : ML dans chaque decision client critique, >90% des hypotheses testees experimentalement

## Rythme operationnel

| Cadence | Activite | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Hebdomadaire** | Revue des performances des modeles en production | Data Scientist | Rapport de performance et alertes de derive |
| **Hebdomadaire** | Analyse des resultats des experiences en cours | Analytics Engineer | Synthese experiences et recommandations |
| **Mensuel** | Revue des segmentations client (stabilite, coherence) | Data Scientist + Marketing | Rapport de stabilite et mise a jour des segments |
| **Mensuel** | Backlog de nouveaux cas d'usage ML | Analytics Lead + Product | Backlog priorise avec ROI estime |
| **Trimestriel** | Revue ROI du portefeuille de modeles predictifs | Analytics Lead + Business | Scorecard ROI et decisions de priorisation |
| **Trimestriel** | Mise a jour des modeles critiques (retraining) | Data Scientist | Changelog des modeles mis a jour |
| **Annuel** | Audit de la stack analytics et selection des outils | Analytics Lead | Rapport d'audit et roadmap outillage |

## State of the Art (2025-2026)

Le ML applique au business evolue rapidement :

- **AutoML democratise** : H2O, AutoGluon et DataRobot permettent aux equipes moins techniques de construire des modeles competitifs, liberant les data scientists pour les cas d'usage complexes.
- **Causal ML** : L'inference causale (Double ML, CausalML) devient accessible pour mesurer les effets incrementaux sans A/B test randomise, via les donnees observationnelles.
- **LLM pour la feature engineering** : Les grands modeles de langage permettent de generer des features semantiques a partir de textes non structures (reviews, emails, CRM notes) et de les integrer dans des pipelines ML classiques.
- **Experimentation sequentielle** : Les methodes d'experimentation adaptative (bandits contextuels, tests sequentiels) remplacent progressivement les A/B tests classiques pour les decisions frequentes.
- **Explicabilite reglementaire** : L'EU AI Act et les regulations sectorielle imposent l'explicabilite des modeles de scoring dans des domaines comme le credit, l'emploi et l'assurance.

## Template actionnable

### Canvas de projet ML metier

| Champ | Valeur |
|---|---|
| **Probleme metier** | ___ |
| **Variable cible** | ___ (binaire / continue / categorielle) |
| **Horizon de prediction** | ___ (J+7, J+30, etc.) |
| **Donnees disponibles** | Sources: ___, periode: ___, volume: ___ |
| **KPI metier impacte** | ___ (ex: taux de churn, taux de conversion) |
| **Valeur attendue** | ___ (ex: reduire le churn de 5%, +200k EUR/an) |
| **Metrique modele principale** | ___ (AUC, RMSE, F1@seuil) |
| **Seuil de succes** | ___ (ex: AUC > 0.80, MAPE < 15%) |
| **Action associee** | ___ (qui fait quoi quand le modele predit quoi) |
| **Baseline de comparaison** | ___ (regle metier existante, modele actuel) |
| **Strategie de validation** | ___ (out-of-time, date de coupure: ___) |
| **Plan d'experimentation** | A/B test : n=___, duree=___, metrique=___ |

## Prompts types

- "Comment construire un modele de prediction du churn ?"
- "Aide-moi a segmenter ma base client avec l'analyse RFM"
- "Comment calculer le Customer Lifetime Value de mes clients ?"
- "Explique-moi comment concevoir un A/B test rigoureux"
- "Quelle est la difference entre uplift modeling et A/B testing ?"
- "Comment utiliser AutoML pour explorer rapidement des cas d'usage ?"

## Limites et Red Flags

Ce skill n'est PAS adapte pour :
- ❌ Deep learning, vision par ordinateur, NLP de recherche → Utiliser plutot un skill IA specialise
- ❌ Pipelines de donnees, ETL, data warehouse → Utiliser plutot : `data-bi:data-engineering`
- ❌ Dashboards, KPIs, reporting BI → Utiliser plutot : `data-bi:decision-reporting-governance`
- ❌ Deploiement et monitoring de modeles en production → Utiliser plutot : `ai-governance:ai-implementation`
- ❌ Prompts LLM, RAG, agents IA → Utiliser plutot : `ai-governance:prompt-engineering-llmops`

Signaux d'alerte en cours d'utilisation :
- ⚠️ Le modele est evalue uniquement sur l'accuracy alors que les classes sont desequilibrees — l'AUC-PR ou le recall sur les positifs doivent etre les metriques principales
- ⚠️ La validation est faite avec un split aleatoire sur des donnees temporelles — risque de data leakage temporel et d'overestimation des performances
- ⚠️ L'A/B test est arrete des qu'une significativite est observee sans avoir atteint la taille d'echantillon pre-calculee — peeking problem, taux de faux positifs gonfle
- ⚠️ Le modele n'est associe a aucune action metier concrete — un modele qui predit sans generer d'action n'a aucune valeur operationnelle

## Skills connexes

| Skill | Lien |
|---|---|
| Data Engineering | `data-bi:data-engineering` — Pipelines et infrastructure pour les donnees ML |
| Decision Reporting | `data-bi:decision-reporting-governance` — BI, KPIs et dashboards |
| Data Literacy | `data-bi:data-literacy` — Visualisation et communication des resultats |
| AI Implementation | `ai-governance:ai-implementation` — Deploiement et monitoring des modeles en prod |
| AI Ethics | `ai-governance:ai-ethics` — Biais et equite dans les modeles predictifs |

## Glossaire

| Terme | Definition |
|-------|-----------|
| **AUC-ROC** | Area Under the ROC Curve — mesure de la capacite discriminante d'un classifieur, independante du seuil de decision. Va de 0.5 (aleatoire) a 1.0 (parfait). |
| **AUC-PR** | Area Under the Precision-Recall Curve — preferable a AUC-ROC pour les classes fortement desequilibrees (ex: fraude, rare evenement). |
| **Churn** | Attrition client : comportement de desabonnement ou d'arret d'utilisation d'un produit. Un modele de churn predit la probabilite de churn d'un client sur un horizon donne. |
| **LTV / CLV** | Customer Lifetime Value / Customer Lifetime Value — valeur totale qu'un client genere sur toute la duree de la relation commerciale. |
| **RFM** | Recency (date de dernier achat), Frequency (nombre d'achats), Monetary (valeur totale des achats) — methode de segmentation client par comportement transactionnel. |
| **k-means** | Algorithme de clustering partitionnel qui divise N observations en k clusters en minimisant la distance intra-cluster. Requiert de specifier k a l'avance. |
| **SHAP** | SHapley Additive exPlanations — methode d'explicabilite des modeles ML basee sur la theorie des jeux, qui attribue a chaque feature sa contribution a chaque prediction. |
| **Data Leakage** | Inclusion dans les donnees d'entrainement d'informations qui ne seraient pas disponibles au moment de la prediction reelle, causant une surestime des performances. |
| **Out-of-Time Validation** | Evaluation d'un modele sur une periode temporelle posterieure a la periode d'entrainement, simulant les conditions reelles de prediction future. |
| **Uplift Modeling** | Modelisation de l'effet incremental (uplift) d'une action sur une sous-population, mesurant qui beneficie le plus d'une intervention par rapport au groupe de controle. |
| **AutoML** | Machine Learning automatise — ensemble de techniques automatisant le pipeline ML : selection de features, choix du modele, optimisation des hyperparametres. |
| **Calibration** | Alignement des probabilites predites par un modele avec les frequences observees. Un modele bien calibre qui predit 70% de probabilite observe 70% de cas positifs. |
| **Prophet** | Bibliotheque de prevision de series temporelles developpee par Meta, adaptee aux donnees avec saisonnalite et jours feries, avec decomposition additive automatique. |
| **XGBoost / LightGBM** | Algorithmes de gradient boosting sur arbres de decision, references pour les donnees tabulaires en ML applique. LightGBM est plus rapide sur les gros volumes. |

## Additional Resources

Consult these reference files for deep dives on each topic area:

- **[Predictive Analytics](./references/predictive-analytics.md)** — Churn prediction, Customer Lifetime Value, demand forecasting, lead scoring, fraud detection. Modeles, metriques, validation et mise en production.

- **[Segmentation & Clustering](./references/segmentation-clustering.md)** — Analyse RFM, k-means, clustering hierarchique, DBSCAN, personas data-driven, interpretation et activation des segments.

- **[AutoML Tools](./references/automl-tools.md)** — H2O AutoML, AutoGluon, DataRobot, Google AutoML. Feature engineering automatise, selection de modeles, limites et bonnes pratiques.

- **[Experimentation & Statistics](./references/experimentation-stats.md)** — A/B testing rigoureux, calcul de taille d'echantillon, tests de significativite, methodes bayesiennes, uplift modeling, inference causale.

- **[Etudes de cas](./references/case-studies.md)** — Cas pratiques detailles illustrant l'application du ML avance a des problemes metier reels.
