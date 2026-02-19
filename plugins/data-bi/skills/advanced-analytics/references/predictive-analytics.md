# Predictive Analytics — Churn, LTV, Demand Forecasting & Scoring

## Overview

Ce guide couvre les principaux use cases de machine learning predictif applique au metier : prediction du churn client, calcul du customer lifetime value, prevision de la demande, scoring de leads, et detection de fraude. Pour chaque use case, le guide detaille les donnees necessaires, les approches de modelisation recommandees, les metriques d'evaluation, les pieges courants, et les actions metier a associer aux predictions.

---

## Churn Prediction

### Definition et enjeux

Le churn (attrition) designe l'arret ou la non-renouvellement d'une relation commerciale par un client. Selon le secteur, la definition varie :
- **Churn voluntaire** : resiliation active (abonnement annule)
- **Churn involontaire** : non-renouvellement passif (carte de credit expiree, paiement echoue)
- **Churn comportemental** : reduction de l'usage sans resiliation formelle (souvent precurseur du churn voluntaire)

L'horizon de prediction est crucial : predire "qui va churner dans les 30 prochains jours" est different de "qui va churner dans les 6 prochains mois". L'horizon determine les features utilisables (pas de leakage temporel) et les actions possibles (les actions de retention necessitent un delai de 2-4 semaines pour produire leur effet).

### Donnees necessaires

**Features comportementales (les plus predictives)**
- Frequence d'utilisation du produit (quotidienne, hebdomadaire, mensuelle)
- Tendance d'utilisation : en baisse sur les 4 dernieres semaines ?
- Engagement avec les features cles du produit
- Frequence et nature des contacts support (nombre de tickets, NPS, CSAT)

**Features relationnelles**
- Anciennete client
- Historique de facturation (retards, litiges, credits)
- Historique d'abonnements (upgrades, downgrades, pauses)

**Features de contexte**
- Date d'echeance du contrat / abonnement
- Evenements recents (changement de tarif, panne de service)
- Segment client (taille, secteur)

**Features socio-economiques (avec RGPD)**
- Localisation geographique
- Secteur d'activite

### Approche de modelisation

**Baseline** : Regle metier simple — "les clients qui n'ont pas utilise le produit depuis 14 jours sont a risque de churn". Mesurer le recall et la precision de cette regle avant tout ML.

**Modele recommande** : XGBoost ou LightGBM en classification binaire. Ces modeles sont robustes sur les donnees tabulaires, gèrent bien les valeurs manquantes, et sont suffisamment interpretables avec SHAP.

```python
# Pipeline type pour le churn
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

pipeline = Pipeline([
    ('preprocessor', preprocessor),  # encodage categoriel, imputation
    ('classifier', XGBClassifier(
        scale_pos_weight=neg_count/pos_count,  # gestion du desequilibre
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='aucpr',  # AUC-PR pour classes desequilibrees
        early_stopping_rounds=50
    ))
])
```

**Gestion du desequilibre de classes** : Le churn est typiquement une classe minoritaire (2-15%). Utiliser :
- `scale_pos_weight` dans XGBoost (ratio negatifs/positifs)
- SMOTE pour l'oversampling de la classe minoritaire (appliquer uniquement sur le jeu d'entrainement, jamais sur le test)
- Metriques adaptees : AUC-PR, Recall@K, F1 au seuil optimal

**Validation temporelle** : Diviser les donnees par periode, jamais aleatoirement. Exemple :
- Entrainement : clients observes entre T-24 et T-6 mois
- Validation : clients observes entre T-6 et T-3 mois
- Test : clients observes entre T-3 mois et aujourd'hui
- Prediction cible : churn dans les 30 jours suivant la date d'observation

### Metriques d'evaluation

| Metrique | Formule | Interpretation |
|---|---|---|
| **AUC-ROC** | Aire sous la courbe ROC | Capacite discriminante generale |
| **AUC-PR** | Aire sous la courbe Precision-Recall | Plus adapte aux classes desequilibrees |
| **Recall@top10%** | Recall sur les 10% avec le score le plus eleve | % de vrais churners detectes dans le top scoring |
| **Lift@top10%** | Taux de churners dans le top 10% / taux moyen | Combien de fois mieux que le hasard |
| **F1@seuil optimal** | F1 au seuil maximisant F1 sur la validation | Performance globale au seuil d'action |

**Seuil de decision** : Le seuil de 0.5 n'est pas le bon seuil par defaut. Optimiser le seuil selon l'objectif :
- Maximiser le recall (detecter le plus de churners possible) : seuil bas (ex: 0.3)
- Maximiser la precision (contacter uniquement les churners certains, ressources limitees) : seuil haut (ex: 0.7)
- Maximiser le F1 : seuil au point de maximisation du F1 sur la courbe Precision-Recall

### Actions metier

Le modele de churn n'a de valeur que s'il declenche des actions :

| Score de churn | Action recommandee | Equipe responsable | Delai d'action |
|---|---|---|---|
| > 0.8 (tres haut risque) | Appel direct d'un conseiller commercial | Commercial / Customer Success | < 48 heures |
| 0.6 - 0.8 (haut risque) | Email personnalise + offre de retention | Marketing | < 1 semaine |
| 0.4 - 0.6 (risque modere) | Sequence d'email d'engagement | Marketing automation | < 2 semaines |
| < 0.4 (faible risque) | Pas d'action proactive | - | - |

**Ciblage par valeur** : Combiner le score de churn avec le LTV client pour prioriser les actions. Un client avec un score de churn de 0.7 et un LTV de 50 000 EUR merite plus d'attention qu'un client avec un score de 0.9 et un LTV de 200 EUR.

---

## Customer Lifetime Value (LTV/CLV)

### Definition et types de LTV

Le Customer Lifetime Value est la valeur totale qu'un client genèrera sur toute la duree de la relation commerciale, actualisee au present.

**LTV historique** : somme des revenus passe d'un client. Utile pour l'analyse de portefeuille, pas pour la prediction.

**LTV previsionnel** : valeur attendue des revenus futurs d'un client. Necessite un modele predictif.

**LTV previsionnel = P(actif sur la periode) x Revenus attendus si actif**

### Approches de modelisation

**Approche 1 : Modele BG/NBD (Non-Contractual)**

Le modele Beta-Geometric / Negative Binomial Distribution (BG/NBD) combine :
- Un modele de comportement transactionnel (frequence d'achat : loi de Poisson)
- Un modele de churn (probabilite de "deceder" : processus geometrique)

```python
from lifetimes import BetaGeoFitter, GammaGammaFitter

# Modele de frequence et de retention
bgf = BetaGeoFitter(penalizer_coef=0.0)
bgf.fit(rfm_df['frequency'], rfm_df['recency'], rfm_df['T'])

# Prediction du nombre de transactions dans les prochains 90 jours
rfm_df['predicted_purchases_90'] = bgf.conditional_expected_number_of_purchases_up_to_time(
    90, rfm_df['frequency'], rfm_df['recency'], rfm_df['T']
)

# Modele de valeur monetaire
ggf = GammaGammaFitter(penalizer_coef=0.0)
ggf.fit(rfm_df[rfm_df['frequency'] > 0]['frequency'],
        rfm_df[rfm_df['frequency'] > 0]['monetary_value'])

# LTV sur 1 an
rfm_df['ltv_12m'] = ggf.customer_lifetime_value(
    bgf, rfm_df['frequency'], rfm_df['recency'], rfm_df['T'],
    rfm_df['monetary_value'], time=12, freq='W'
)
```

Adapte pour : e-commerce, retail, B2C avec transactions recurrentes non contractuelles.

**Approche 2 : Regression ML (Contractuel)**

Pour les business contractuels (abonnements SaaS, telco) :
- Variable cible : MRR (Monthly Recurring Revenue) ou ARR dans N mois
- Features : historique de paiement, usage du produit, churn score, tier d'abonnement
- Modele : XGBoost Regressor ou Random Forest Regressor

**Approche 3 : Cohortes Simples**

Pour une estimation rapide sans ML :
- Grouper les clients par cohorte d'acquisition (mois, canal, segment)
- Calculer la retention et les revenus par cohorte sur les periodes suivantes
- Projeter les courbes de retention et de revenus pour les nouvelles cohortes

---

## Demand Forecasting

### Enjeux et caracteristiques

La prevision de la demande est l'un des cas d'usage les plus impactants du ML metier, avec des applications en :
- Gestion des stocks (eviter les ruptures et les surstocks)
- Planification de la capacite de production
- Optimisation des prix dynamiques
- Allocation des ressources RH

Caracteristiques des series temporelles de demande :
- **Saisonnalite** : hebdomadaire, mensuelle, annuelle
- **Tendance** : croissance ou declin structurel
- **Evenements speciaux** : jours feries, promotions, evenements externes
- **Hierarchie** : demande nationale > regionale > locale > par SKU

### Choix du modele selon l'horizon

| Horizon | Modele recommande | Avantages |
|---|---|---|
| < 1 semaine | Modeles de lissage exponentiel (ETS) | Tres rapides, adaptent aux recentes tendances |
| 1-4 semaines | Prophet | Gere la saisonnalite multiple et les jours feries |
| 1-3 mois | XGBoost avec features temporelles | Capture les effets non lineaires et les interactions |
| > 3 mois | Ensemble (Prophet + XGBoost) | Combine capacite de saisonnalite et flexibilite ML |
| Hierarchique | Reconciliation (bottom-up, top-down) | Coherence entre niveaux de la hierarchie |

### Features temporelles pour XGBoost

```python
def create_time_features(df, date_col):
    df = df.copy()
    dt = df[date_col].dt

    # Caracteristiques du calendrier
    df['day_of_week'] = dt.dayofweek
    df['day_of_month'] = dt.day
    df['week_of_year'] = dt.isocalendar().week
    df['month'] = dt.month
    df['quarter'] = dt.quarter
    df['year'] = dt.year
    df['is_weekend'] = dt.dayofweek >= 5
    df['is_month_end'] = dt.is_month_end
    df['is_month_start'] = dt.is_month_start

    # Lags de la variable cible (utiliser uniquement des lags disponibles au moment de la prediction)
    for lag in [7, 14, 21, 28, 364]:
        df[f'demand_lag_{lag}'] = df['demand'].shift(lag)

    # Moyennes mobiles
    for window in [7, 14, 28]:
        df[f'demand_rolling_mean_{window}'] = df['demand'].shift(1).rolling(window).mean()
        df[f'demand_rolling_std_{window}'] = df['demand'].shift(1).rolling(window).std()

    return df
```

### Metriques d'evaluation pour la prevision

| Metrique | Formule | Quand l'utiliser |
|---|---|---|
| **MAPE** | mean(|actual - pred| / actual) * 100 | Cas d'usage general, interpretable |
| **SMAPE** | mean(|actual - pred| / ((actual + pred)/2)) * 100 | Quand actual peut etre proche de 0 |
| **RMSE** | sqrt(mean((actual - pred)²)) | Penalise les grandes erreurs, meme unite que la cible |
| **MAE** | mean(|actual - pred|) | Plus robuste aux outliers que RMSE |
| **Bias** | mean(pred - actual) | Detecter le sur-estimage ou sous-estimage systematique |

---

## Lead Scoring

### Objectif et definition

Le lead scoring attribue un score a chaque prospect commercial pour prioriser les efforts de l'equipe de vente. Un bon lead scoring permet :
- D'augmenter le taux de conversion en concentrant les efforts sur les prospects les plus qualifies
- De reduire le delai de conversion en contactant les prospects au bon moment
- De personnaliser l'approche commerciale selon le profil du prospect

### Types de scores

**Score de fit (profil)** : probabilite que le prospect soit adapte au produit/service selon des criteres demographiques et firmographiques (secteur, taille, technologie utilisee).

**Score d'intention (comportement)** : probabilite que le prospect soit en phase d'achat, basee sur ses actions (pages visitees, contenus telecharges, emails ouverts, demos demandees).

**Score combine** : combinaison du score de fit et du score d'intention en une matrice 2x2.

### Features pour le lead scoring

**Features firmographiques (B2B)**
- Taille de l'entreprise (effectif, chiffre d'affaires)
- Secteur d'activite
- Maturite technologique (tech stack identifiable via BuiltWith, LinkedIn)
- Localisation geographique
- Financement (levee de fonds recente ?)

**Features comportementales**
- Nombre de visites sur le site web (total et recentes)
- Pages visitees (page de tarification = signal fort)
- Contenus telecharges (livres blancs, etudes de cas)
- Emails : taux d'ouverture, clics, engagement
- Demos demandees ou essais gratuits

**Features de timing**
- Temps depuis le premier contact
- Trend d'engagement : en hausse ou en baisse ?
- Saisonnalite sectorielle (budgets en fin d'annee fiscale)

### Modelisation et calibration

```python
# XGBoost pour le lead scoring avec calibration
from sklearn.calibration import CalibratedClassifierCV

# Entrainement du modele de base
xgb = XGBClassifier(...)
xgb.fit(X_train, y_train)

# Calibration des probabilites (Platt scaling)
calibrated_model = CalibratedClassifierCV(xgb, method='sigmoid', cv='prefit')
calibrated_model.fit(X_val, y_val)

# Les probabilites sortantes sont maintenant bien calibrees
proba = calibrated_model.predict_proba(X_prod)[:, 1]
```

**Matrice de prioritisation des leads**

| Score d'intention | Score de fit | Action commerciale |
|---|---|---|
| Eleve (> 70) | Eleve (> 70) | Contact immediat par commercial senior |
| Eleve (> 70) | Moyen (40-70) | Contact rapide + qualification approfondie |
| Moyen (40-70) | Eleve (> 70) | Nurturing intensif (contenu personnalise) |
| Moyen (40-70) | Moyen (40-70) | Nurturing standard |
| < 40 | < 40 | Pas d'action proactive |

---

## Fraud Detection

### Specificites du cas d'usage fraude

La detection de fraude est un des cas d'usage ML les plus critiques et les plus contraignants :
- **Classe ultra-desequilibree** : fraude < 0.1-1% des transactions
- **Adversarial** : les fraudeurs s'adaptent aux systemes de detection
- **Couts asymetriques** : le cout d'un faux negatif (fraude non detectee) est bien superieur au cout d'un faux positif (transaction legitime bloquee)
- **Latence critique** : la decision doit etre prise en < 100ms pour le paiement en ligne

### Approche recommandee

**Ensemble de modeles** :
- Modele de regle metier (vitesse pure, capture la fraude connue et les patterns simples)
- XGBoost / LightGBM (performance generale sur features structurees)
- Isolation Forest ou Autoencoder (detection d'anomalies, capture la fraude nouvelle)
- Modele sequentiel (LSTM ou Transformer sur l'historique des transactions)

**Features critiques pour la fraude financiere** :
- Montant de la transaction (vs. historique du compte)
- Geolocalisation (distance avec la derniere transaction, pays inhabituel)
- Appareil utilise (device fingerprinting, IP, cookie)
- Heure de la transaction (transactions nocturnes suspectes)
- Velocite : nombre de transactions dans les 1, 5, 15 dernieres minutes
- Features de comportement : categorie de marchand, canal de paiement

**Seuils differencies par contexte** :
- Transaction de faible montant : seuil plus eleve (moins de friction)
- Transaction de montant eleve ou inhabituel : seuil plus bas (plus de controle)
- Nouveau compte : seuil plus bas (historique insuffisant)

### Metriques adaptees a la fraude

| Metrique | Formule | Cible typique |
|---|---|---|
| **Recall (Sensitivity)** | TP / (TP + FN) | > 85% (detecter la majorite des fraudes) |
| **Precision** | TP / (TP + FP) | > 50% (la moitie des alertes sont vraies fraudes) |
| **FPR (False Positive Rate)** | FP / (FP + TN) | < 0.1% (ne pas bloquer les transactions legitimes) |
| **AUC-PR** | Aire sous Precision-Recall curve | > 0.75 |
| **Dollar Saved** | Montant de fraudes detectees evitees | KPI metier direct |

---

## Glossaire des Metriques Predictives

| Terme | Definition |
|-------|-----------|
| **Precision** | Parmi les cas predits positifs, quelle fraction l'est vraiment. TP / (TP + FP). |
| **Recall (Sensibilite)** | Parmi tous les cas reellement positifs, quelle fraction est detectee. TP / (TP + FN). |
| **F1 Score** | Moyenne harmonique de la precision et du recall. 2 * (Prec * Rec) / (Prec + Rec). |
| **AUC-ROC** | Area Under the ROC Curve. Probabilite que le modele classe correctement une paire positif/negatif. |
| **AUC-PR** | Area Under the Precision-Recall Curve. Plus informatif que AUC-ROC pour les classes desequilibrees. |
| **MAPE** | Mean Absolute Percentage Error. Erreur de prevision en pourcentage. |
| **Lift** | Rapport entre le taux de positifs dans le top-K% score et le taux moyen. Mesure l'efficacite du ciblage. |
| **Calibration** | Alignement entre les probabilites predites et les frequences observees. |
| **Data Leakage** | Inclusion de features contenant de l'information sur la cible qui ne serait pas disponible au moment de la prediction. |
| **Out-of-Time Validation** | Evaluation du modele sur une periode posterieure a l'entrainement, simulant les conditions reelles. |
