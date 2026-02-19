---
name: customer-analytics
version: 1.0.0
description: >
  Use this skill when the user asks about "customer analytics", "analyse client", "LTV", "CLV", "customer lifetime value", "RFM", "segmentation client", "cohort analysis", "churn prediction", "churn rate", "retention analysis", "customer 360", "customer health score", "NPS analyse", "customer segmentation", "ARPU", "CAC LTV ratio", "churn modeling", "customer journey analytics", "behavioral segmentation", discusses measuring customer behavior, predicting churn, calculating lifetime value, or needs guidance on customer data analysis and retention strategy.
---

# Customer Analytics

## Vue d'Ensemble

La customer analytics transforme les donnees clients en decisions de retention, croissance et monetisation. Trois questions fondamentales : qui sont nos meilleurs clients (segmentation) ? Pourquoi et quand les clients partent (churn) ? Quelle est la valeur a long terme de chaque client (LTV) ?

Ces analyses sont critiques pour tout business avec des clients recurrents — SaaS, e-commerce, subscription, marketplaces.

---

## Customer 360 — Le Modele de Donnees

### Architecture

Le Customer 360 consolide toutes les donnees clients dans un profil unifie.

```sql
-- Table clients unifiee (exemple e-commerce / SaaS)
CREATE TABLE customer_360 AS
SELECT
    c.customer_id,
    c.email,
    c.acquisition_date,
    c.acquisition_channel,
    c.plan_type,
    -- Metriques comportementales
    o.total_orders,
    o.total_revenue,
    o.avg_order_value,
    o.days_since_last_order,
    -- Metriques produit
    p.sessions_last_30d,
    p.features_used,
    p.last_login_date,
    -- Sante client
    s.nps_score,
    s.support_tickets_open,
    s.health_score
FROM customers c
LEFT JOIN (
    SELECT
        customer_id,
        COUNT(*) as total_orders,
        SUM(amount) as total_revenue,
        AVG(amount) as avg_order_value,
        DATE_DIFF('day', MAX(created_at), CURRENT_DATE) as days_since_last_order
    FROM orders
    GROUP BY customer_id
) o USING (customer_id)
LEFT JOIN product_usage p USING (customer_id)
LEFT JOIN customer_scores s USING (customer_id);
```

---

## RFM — Segmentation par Valeur Client

### Definition

**Recency (R)** : depuis combien de temps le client a ete actif/achete ? Plus recent = meilleur score.
**Frequency (F)** : combien de fois le client a achete / utilise le produit ? Plus frequent = meilleur score.
**Monetary (M)** : combien le client a depense ? Plus elevé = meilleur score.

### Implementation SQL

```sql
WITH rfm_raw AS (
    SELECT
        customer_id,
        MAX(order_date) as last_order_date,
        COUNT(DISTINCT order_id) as frequency,
        SUM(amount) as monetary,
        DATE_DIFF('day', MAX(order_date), CURRENT_DATE) as recency_days
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '2 years'
    GROUP BY customer_id
),

rfm_scores AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary,
        -- Score 1-5 par quintile (5 = meilleur)
        NTILE(5) OVER (ORDER BY recency_days ASC) as r_score,   -- Moins de jours = meilleur
        NTILE(5) OVER (ORDER BY frequency DESC) as f_score,
        NTILE(5) OVER (ORDER BY monetary DESC) as m_score
    FROM rfm_raw
),

rfm_segments AS (
    SELECT
        *,
        CONCAT(r_score, f_score, m_score) as rfm_code,
        (r_score + f_score + m_score) as rfm_total
    FROM rfm_scores
)

SELECT
    customer_id,
    rfm_code,
    rfm_total,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'Recent Customers'
        WHEN r_score >= 3 AND f_score <= 3 AND m_score >= 3 THEN 'Potential Loyalist'
        WHEN r_score >= 4 AND f_score >= 2 AND m_score >= 2 THEN 'Promising'
        WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score >= 4 AND m_score >= 4 THEN 'Cant Lose Them'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
        ELSE 'Need Attention'
    END as segment
FROM rfm_segments;
```

### Segments et Actions Marketing

| Segment | Caracteristique | Action recommandee |
|---|---|---|
| **Champions** | Achete recemment, souvent, beaucoup | Demander des temoignages, early access nouveautes |
| **Loyal Customers** | Achete souvent, fidele | Programme de fidelite, upsell |
| **At Risk** | Bon historique mais inactif | Campagne re-engagement, offre de retour |
| **Cant Lose Them** | Tres gros clients qui deviennent inactifs | Contact direct commercial, offre personnalisee |
| **Lost** | Anciens clients, plus actifs | Campagne winback ou desengagement |
| **Recent Customers** | Nouveau, peu d'historique | Onboarding optimise, education produit |

---

## Cohort Analysis

### Definition

Une cohort = un groupe de clients partageant une caracteristique commune (en general : la date d'acquisition). L'analyse de cohortes compare la retention de chaque cohorte au fil du temps.

### Implementation SQL

```sql
WITH cohorts AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', first_order_date) as cohort_month
    FROM (
        SELECT
            customer_id,
            MIN(order_date) as first_order_date
        FROM orders
        GROUP BY customer_id
    ) first_orders
),

cohort_activity AS (
    SELECT
        c.customer_id,
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) as activity_month,
        DATE_DIFF('month', c.cohort_month, DATE_TRUNC('month', o.order_date)) as month_number
    FROM cohorts c
    JOIN orders o USING (customer_id)
),

cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) as cohort_customers
    FROM cohorts
    GROUP BY cohort_month
),

retention AS (
    SELECT
        a.cohort_month,
        a.month_number,
        COUNT(DISTINCT a.customer_id) as retained_customers
    FROM cohort_activity a
    GROUP BY a.cohort_month, a.month_number
)

SELECT
    r.cohort_month,
    r.month_number,
    r.retained_customers,
    s.cohort_customers,
    ROUND(100.0 * r.retained_customers / s.cohort_customers, 1) as retention_rate
FROM retention r
JOIN cohort_size s USING (cohort_month)
ORDER BY r.cohort_month, r.month_number;
```

### Lecture du Tableau de Cohortes

```
Cohort     M0     M1     M2     M3     M6     M12
Jan 2024   100%   45%    32%    28%    22%    18%
Feb 2024   100%   47%    35%    30%    —      —
Mar 2024   100%   52%    38%    —      —      —

Lecture : la cohorte de Jan 2024 avait 100 clients.
- Au mois 1 : 45% sont encore actifs
- Au mois 3 : 28% sont encore actifs
- Au mois 12 : 18% sont encore actifs (retention annuelle)
```

**Signaux d'alerte** : chute brutale entre M0 et M1 → probleme d'onboarding. Chute entre M3 et M6 → probleme de valeur a moyen terme.

---

## Customer Lifetime Value (CLV)

### CLV Historique (Simple)

Pour les clients avec suffisamment d'historique.

```python
import pandas as pd
import numpy as np

def calculate_historical_clv(
    orders: pd.DataFrame,
    discount_rate: float = 0.1  # 10% taux d'actualisation annuel
) -> pd.DataFrame:
    """
    Calculer le CLV historique par client.
    orders : DataFrame avec columns [customer_id, order_date, amount]
    """
    # Revenue par client et date
    customer_revenue = orders.groupby(['customer_id', 'order_date'])['amount'].sum().reset_index()

    # Calculer le CLV actualisé
    results = []
    for customer_id, group in customer_revenue.groupby('customer_id'):
        group = group.sort_values('order_date')
        first_date = group['order_date'].min()

        total_clv = 0
        for _, row in group.iterrows():
            # Periode en annees depuis le premier achat
            years = (row['order_date'] - first_date).days / 365
            # Valeur actualisee
            discounted_value = row['amount'] / (1 + discount_rate) ** years
            total_clv += discounted_value

        results.append({
            'customer_id': customer_id,
            'historical_clv': total_clv,
            'orders_count': len(group),
            'avg_order_value': group['amount'].mean(),
            'first_order': first_date,
            'last_order': group['order_date'].max(),
        })

    return pd.DataFrame(results)
```

### CLV Predictif — Modele BG/NBD (Pareto/NBD)

Le modele BG/NBD (Fader, Hardie, Lee 2005) est le standard academique pour predire le comportement futur des clients non-contractuels (e-commerce, retail).

```python
from lifetimes import BetaGeoFitter, GammaGammaFitter

# Preparer les donnees au format RFM
rfm = summary_data_from_transaction_data(
    transactions=orders,
    customer_id_col='customer_id',
    datetime_col='order_date',
    monetary_value_col='amount',
    observation_period_end='2025-01-01',
)

# Ajuster le modele BG/NBD (frequence et recence)
bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(rfm['frequency'], rfm['recency'], rfm['T'])

# Predire les transactions futures sur 12 mois
rfm['predicted_purchases_12m'] = bgf.conditional_expected_number_of_purchases_up_to_time(
    t=12 * 4.33,  # 12 mois en semaines
    frequency=rfm['frequency'],
    recency=rfm['recency'],
    T=rfm['T'],
)

# Ajuster le Gamma-Gamma pour le monetary value
ggf = GammaGammaFitter(penalizer_coef=0.001)
ggf.fit(rfm[rfm['frequency'] > 0]['frequency'],
        rfm[rfm['frequency'] > 0]['monetary_value'])

# CLV predictif sur 12 mois
rfm['clv_12m'] = ggf.customer_lifetime_value(
    bgf,
    rfm['frequency'],
    rfm['recency'],
    rfm['T'],
    rfm['monetary_value'],
    time=12,  # mois
    discount_rate=0.01,  # 1% mensuel
)
```

### CLV SaaS (MRR-Based)

Pour les modeles d'abonnement, le CLV est plus simple :

```python
def saas_clv(mrr: float, gross_margin: float, churn_rate: float) -> float:
    """
    CLV SaaS simplifie
    mrr : Monthly Recurring Revenue moyen par client
    gross_margin : ex 0.80 pour 80%
    churn_rate : taux de churn mensuel, ex 0.02 pour 2%
    """
    avg_lifetime_months = 1 / churn_rate
    return mrr * gross_margin * avg_lifetime_months

# Exemple
clv = saas_clv(mrr=200, gross_margin=0.75, churn_rate=0.02)
print(f"CLV = {clv:.0f} EUR")  # CLV = 7500 EUR
```

---

## Churn Prediction

### Features Predicteurs du Churn

**Signaux comportementaux (les plus predictifs)** :
- Frequence de connexion (login frequency) — declin brutal = alerte
- Nombre de features actives utilisees — reduction = risque
- Volume de donnees/transactions traites — baisse anormale
- Temps passe dans l'application — en baisse depuis N semaines

**Signaux relationnels** :
- Nombre de tickets support ouverts/non resolus
- Score NPS bas ou absence de reponse au NPS
- Contacts commerciaux recents (negociation prix = risque)

**Signaux externes** :
- Levee de fonds recente du client (peut changer de stack)
- Mouvement de personnel cle (champion interne parti)

### Modele de Churn — Implementation

```python
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.preprocessing import StandardScaler

# Features engineering
def build_churn_features(customers: pd.DataFrame) -> pd.DataFrame:
    """Construire les features pour le modele de churn."""
    features = pd.DataFrame()

    features['days_since_login'] = customers['days_since_last_login']
    features['login_frequency_30d'] = customers['logins_last_30d']
    features['login_trend'] = (
        customers['logins_last_30d'] - customers['logins_prev_30d']
    )  # Negatif = declin
    features['features_used'] = customers['features_used_count']
    features['support_tickets_open'] = customers['open_tickets']
    features['days_since_nps'] = customers['days_since_last_nps']
    features['nps_score'] = customers['nps_score'].fillna(5)  # Imputer la mediane
    features['contract_months_remaining'] = customers['contract_months_remaining']
    features['plan_age_months'] = customers['plan_age_months']
    features['mrr'] = customers['mrr']

    return features

# Entrainement
X = build_churn_features(training_customers)
y = training_customers['churned_next_90d']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GradientBoostingClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    min_samples_leaf=20,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluation
y_pred_proba = model.predict_proba(X_test)[:, 1]
print(f"AUC-ROC: {roc_auc_score(y_test, y_pred_proba):.3f}")

# Scoring en production
def get_churn_risk_score(customer: dict) -> dict:
    """Obtenir le score de risque de churn pour un client."""
    features = build_churn_features(pd.DataFrame([customer]))
    churn_prob = model.predict_proba(features)[0, 1]

    risk_level = (
        'HIGH' if churn_prob > 0.7
        else 'MEDIUM' if churn_prob > 0.4
        else 'LOW'
    )

    return {
        'churn_probability': round(churn_prob, 3),
        'risk_level': risk_level,
        'top_risk_factors': get_top_features(features, model),
    }
```

### Actions par Niveau de Risque

| Risque | Score | Action |
|---|---|---|
| **Tres eleve** | > 80% | Contact direct CS dans les 24h, offre personnalisee |
| **Eleve** | 60-80% | Email automatique du CSM, audit de sante |
| **Moyen** | 40-60% | Campagne email produit, invitation webinar |
| **Faible** | < 40% | Monitoring standard, NPS trimestriel |

---

## Customer Health Score

Scoring composite sur 0-100 qui agrege les signaux cles en un indicateur actionnable.

```python
def calculate_health_score(customer: dict) -> int:
    """
    Score de sante client — 0 (critique) a 100 (excellent)
    """
    score = 0

    # Engagement produit (40 points max)
    login_score = min(40, customer['logins_last_30d'] * 2)
    score += login_score

    # Utilisation features (20 points max)
    feature_score = min(20, customer['features_used'] * 4)
    score += feature_score

    # Support (20 points max — soustraction)
    if customer['open_tickets'] == 0:
        score += 20
    elif customer['open_tickets'] == 1:
        score += 10
    else:
        score += 0

    # NPS (20 points max)
    if customer.get('nps_score') is not None:
        nps_normalized = (customer['nps_score'] + 100) / 2  # -100 a +100 → 0 a 100
        score += min(20, nps_normalized * 0.2)

    return min(100, max(0, int(score)))
```

---

## Maturity Model — Customer Analytics

| Niveau | Caracteristique |
|---|---|
| **1 — Basique** | Churn calcule manuellement, pas de segmentation |
| **2 — RFM** | Segmentation RFM, actions marketing par segment |
| **3 — Cohortes** | Analyse de retention par cohorte, CLV historique |
| **4 — Predictif** | Modele de churn en production, CLV predictif |
| **5 — Real-Time** | Health score temps reel, intervention automatique, CLV comme KPI nord |
