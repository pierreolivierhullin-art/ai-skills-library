# Analyse Cohorte et Customer Lifetime Value

## Definition et Fondements de l'Analyse de Cohorte

Une cohorte est un groupe de clients partageant une caracteristique commune, definie a un moment precis. L'analyse de cohorte consiste a suivre ce groupe dans le temps pour observer son comportement et son evolution.

**Pourquoi c'est fondamental.** Les metriques agregees peuvent masquer des tendances critiques. Un taux de retention global de 75% peut cacher une retention de 90% pour les cohortes recentes et de 50% pour les anciennes — signe que le produit s'ameliore, ou inverse. Sans analyse de cohorte, il est impossible de distinguer une amelioration reelle d'un effet de mix (croissance qui noie le signal).

**Le probleme des metriques agregees :** si une entreprise acquiert 1000 nouveaux clients par mois avec 60% de retention, le nombre total de clients actifs augmente continuellement — alors que la qualite de retention pour chaque cohorte peut se degrader. Le paradoxe de la croissance masque la deterioration.

---

## Types de Cohortes

**Cohorte d'acquisition :** definie par la date d'acquisition du client (premier achat, inscription, activation). La plus courante. Permet de mesurer la retention et la valeur generee par chaque vague d'acquisition.

**Cohorte de comportement :** definie par une action specifique (premier achat d'une categorie, utilisation d'une feature premium, abonnement a un plan superieur). Permet de mesurer l'impact d'un comportement specifique sur la retention future.

**Cohorte de produit :** definie par la version du produit utilisee au moment de l'acquisition. Permet de comparer la retention selon les iterations produit.

---

## SQL — Cohorte d'Acquisition (Retention Mensuelle)

### Structure : CTE pour la Cohorte d'Origine

```sql
-- Etape 1 : identifier le mois de premiere commande par client
WITH cohort_base AS (
  SELECT
    customer_id,
    DATE_TRUNC('month', MIN(order_date)) AS cohort_month
  FROM orders
  WHERE order_status NOT IN ('cancelled', 'refunded')
  GROUP BY customer_id
),

-- Etape 2 : tous les mois d'activite de chaque client
customer_activity AS (
  SELECT
    o.customer_id,
    DATE_TRUNC('month', o.order_date) AS activity_month
  FROM orders o
  WHERE order_status NOT IN ('cancelled', 'refunded')
  GROUP BY o.customer_id, DATE_TRUNC('month', o.order_date)
),

-- Etape 3 : jointure pour calculer le mois relatif (0, 1, 2, 3...)
cohort_joined AS (
  SELECT
    cb.cohort_month,
    ca.activity_month,
    cb.customer_id,
    -- Mois depuis acquisition (0 = mois d'acquisition)
    DATE_DIFF(ca.activity_month, cb.cohort_month, MONTH) AS months_since_acquisition
  FROM cohort_base cb
  JOIN customer_activity ca USING (customer_id)
),

-- Etape 4 : taille de chaque cohorte (nb clients acquis)
cohort_size AS (
  SELECT
    cohort_month,
    COUNT(DISTINCT customer_id) AS cohort_customers
  FROM cohort_base
  GROUP BY cohort_month
),

-- Etape 5 : clients actifs par cohorte et par mois relatif
cohort_retention AS (
  SELECT
    cohort_month,
    months_since_acquisition,
    COUNT(DISTINCT customer_id) AS active_customers
  FROM cohort_joined
  GROUP BY cohort_month, months_since_acquisition
)

-- Etape 6 : calcul du taux de retention
SELECT
  cr.cohort_month,
  cr.months_since_acquisition,
  cr.active_customers,
  cs.cohort_customers,
  ROUND(100.0 * cr.active_customers / cs.cohort_customers, 1) AS retention_rate_pct
FROM cohort_retention cr
JOIN cohort_size cs USING (cohort_month)
ORDER BY cr.cohort_month, cr.months_since_acquisition;
```

### Format Triangulaire — Pivot en SQL (BigQuery)

```sql
-- Pivotage pour obtenir le tableau triangulaire standard
SELECT
  cohort_month,
  MAX(CASE WHEN months_since_acquisition = 0  THEN retention_rate_pct END) AS m0,
  MAX(CASE WHEN months_since_acquisition = 1  THEN retention_rate_pct END) AS m1,
  MAX(CASE WHEN months_since_acquisition = 2  THEN retention_rate_pct END) AS m2,
  MAX(CASE WHEN months_since_acquisition = 3  THEN retention_rate_pct END) AS m3,
  MAX(CASE WHEN months_since_acquisition = 6  THEN retention_rate_pct END) AS m6,
  MAX(CASE WHEN months_since_acquisition = 12 THEN retention_rate_pct END) AS m12
FROM (
  -- requete precedente ici
)
GROUP BY cohort_month
ORDER BY cohort_month;
```

---

## Visualisation Heat Map Cohorte en Python

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# --- Chargement des donnees ---
df = pd.read_csv('orders.csv', parse_dates=['order_date'])
df = df[~df['order_status'].isin(['cancelled', 'refunded'])]

# --- Cohorte d'acquisition ---
df['cohort_month'] = df.groupby('customer_id')['order_date'].transform('min').dt.to_period('M')
df['order_month']  = df['order_date'].dt.to_period('M')
df['months_since'] = (df['order_month'] - df['cohort_month']).apply(lambda x: x.n)

# --- Tableau de retention ---
cohort_size = df[df['months_since'] == 0].groupby('cohort_month')['customer_id'].nunique()
cohort_data = df.groupby(['cohort_month', 'months_since'])['customer_id'].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index='cohort_month', columns='months_since', values='customer_id')

# Taux de retention en pourcentage
retention_matrix = cohort_pivot.divide(cohort_size, axis=0).round(3) * 100

# --- Visualisation ---
fig, ax = plt.subplots(figsize=(16, 8))

sns.heatmap(
    retention_matrix,
    annot=True,
    fmt='.0f',
    cmap='YlOrRd_r',
    linewidths=0.5,
    ax=ax,
    vmin=0, vmax=100,
    cbar_kws={'label': 'Taux de retention (%)'}
)

ax.set_title('Analyse de Cohorte — Retention Mensuelle (%)', fontsize=16, pad=15)
ax.set_xlabel('Mois depuis acquisition', fontsize=12)
ax.set_ylabel('Cohorte (mois d\'acquisition)', fontsize=12)
plt.tight_layout()
plt.savefig('cohort_heatmap.png', dpi=150)
plt.show()
```

---

## Interpretation de la Heat Map

**Identifier le "retention floor" :** c'est le taux de retention qui se stabilise apres les premiers mois. Si les cohortes se stabilisent a 30% au mois 6 et restent a ce niveau jusqu'au mois 18, le retention floor est a 30%. Ce plancher represente les clients "vrais fideles" — ceux qui ne partiront probablement pas.

**Lire les colonnes verticalement :** une colonne M3 en deterioration sur les cohortes recentes signale un probleme apparu dans le produit ou l'onboarding au cours des derniers mois.

**Lire les lignes horizontalement :** une cohorte specifique avec une retention anormalement basse indique un probleme lie a cette vague d'acquisition (mauvaise qualite de lead, campagne mal ciblee, bug produit en production ce mois).

**Temps de stabilisation :** dans le SaaS, la retention se stabilise generalement entre M3 et M6. Dans l'e-commerce, entre M6 et M12. Au-dela, les clients qui restent ont un churn residuel tres faible.

---

## Customer Lifetime Value — Methodes de Calcul

### CLV Historique Simple

```python
# CLV historique = somme des revenues passes par client
clv_historical = df.groupby('customer_id').agg(
    total_revenue  = ('order_amount', 'sum'),
    nb_orders      = ('order_id',     'nunique'),
    first_order    = ('order_date',   'min'),
    last_order     = ('order_date',   'max'),
    customer_age_days = ('order_date', lambda x: (x.max() - x.min()).days + 1)
).reset_index()

# Revenue mensuel moyen par client
clv_historical['monthly_revenue'] = (
    clv_historical['total_revenue'] /
    (clv_historical['customer_age_days'] / 30)
).round(2)
```

**Limite :** le CLV historique ne predit pas la valeur future. Un client qui a achete massivement pendant 2 ans mais a arrete peut avoir un CLV historique eleve mais un CLV futur nul.

### CLV Predictif — Modele BG/NBD + Gamma-Gamma

Le modele BG/NBD (Buy-Till-You-Die) modelise deux processus simultanement :
1. **Processus d'achat :** le client effectue des achats selon un processus de Poisson (frequence individuelle variable)
2. **Processus de churn :** le client peut "mourir" (churner) apres chaque transaction avec une probabilite p

Le modele Gamma-Gamma predit la valeur monetaire esperee par transaction, conditionnellement au nombre de transactions.

```python
# Installation : pip install lifetimes
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# --- Preparation des donnees ---
df = pd.read_csv('transactions.csv', parse_dates=['order_date'])
df = df[df['order_status'].isin(['completed', 'shipped'])]

# Format requis par lifetimes : summary par client
summary = summary_data_from_transaction_data(
    df,
    customer_id_col    = 'customer_id',
    datetime_col       = 'order_date',
    monetary_value_col = 'order_amount',
    observation_period_end = '2024-01-01',
    freq               = 'D'
)

# Filtrer les clients avec au moins 1 transaction repetee (requis BG/NBD)
summary_repeat = summary[summary['frequency'] > 0]

print(f"Clients avec repeat purchase : {len(summary_repeat):,}")
print(summary_repeat.describe().round(2))
```

### Fit du Modele BG/NBD

```python
# --- Modele BG/NBD ---
bgf = BetaGeoFitter(penalizer_coef=0.01)
bgf.fit(
    summary_repeat['frequency'],
    summary_repeat['recency'],
    summary_repeat['T']
)

print("Parametres BG/NBD :")
print(f"  r (heterogeneite frequence) : {bgf.params_['r']:.3f}")
print(f"  alpha (frequence moy)       : {bgf.params_['alpha']:.3f}")
print(f"  a (heterogeneite churn)     : {bgf.params_['a']:.3f}")
print(f"  b (prob churn par defaut)   : {bgf.params_['b']:.3f}")

# Prediction du nombre de transactions sur les 12 prochains mois
summary_repeat['predicted_purchases_12m'] = bgf.conditional_expected_number_of_purchases_up_to_time(
    t           = 365,
    frequency   = summary_repeat['frequency'],
    recency     = summary_repeat['recency'],
    T           = summary_repeat['T']
).round(2)

# Probabilite d'etre encore actif (vivant)
summary_repeat['prob_alive'] = bgf.conditional_probability_alive(
    frequency = summary_repeat['frequency'],
    recency   = summary_repeat['recency'],
    T         = summary_repeat['T']
).round(3)
```

**Interpretation des parametres BG/NBD :**
- `r` et `alpha` : parametres de la distribution Gamma sur la frequence d'achat individuelle. Un `r` faible signifie une grande heterogeneite entre clients.
- `a` et `b` : parametres de la distribution Beta sur la probabilite de churn. Un ratio `a/b` eleve signifie une probabilite de churn moyenne elevee dans la base.

### Fit du Modele Gamma-Gamma

```python
# --- Modele Gamma-Gamma (valeur monetaire) ---
# Prerequis : frequence >= 1 ET valeur monetaire > 0
summary_gg = summary_repeat[
    (summary_repeat['frequency'] > 0) &
    (summary_repeat['monetary_value'] > 0)
].copy()

ggf = GammaGammaFitter(penalizer_coef=0.001)
ggf.fit(
    summary_gg['frequency'],
    summary_gg['monetary_value']
)

print(f"\nParametres Gamma-Gamma :")
print(f"  p : {ggf.params_['p']:.3f}")
print(f"  q : {ggf.params_['q']:.3f}")
print(f"  v : {ggf.params_['v']:.3f}")

# Valeur monetaire esperee par transaction
summary_gg['expected_avg_revenue'] = ggf.conditional_expected_average_profit(
    summary_gg['frequency'],
    summary_gg['monetary_value']
).round(2)
```

### Calcul du CLV Predictif 12 Mois

```python
# --- CLV predictif 12 mois ---
# Discount rate : taux mensuel (ex: 10% annuel -> 0.80% mensuel)
monthly_discount_rate = 0.01  # 12% annuel

clv_12m = ggf.customer_lifetime_value(
    bgf,
    summary_gg['frequency'],
    summary_gg['recency'],
    summary_gg['T'],
    summary_gg['monetary_value'],
    time           = 12,   # mois
    discount_rate  = monthly_discount_rate,
    freq           = 'D'
).reset_index()

clv_12m.columns = ['customer_id', 'clv_12m']

# --- Segmentation par CLV predit ---
clv_12m['clv_segment'] = pd.qcut(
    clv_12m['clv_12m'],
    q     = [0, 0.5, 0.8, 1.0],
    labels = ['Low Value', 'Medium Value', 'High Value']
)

print("\nDistribution CLV 12 mois :")
print(clv_12m.groupby('clv_segment')['clv_12m'].describe().round(0))
```

---

## LTV / CAC Ratio — Calcul et Benchmarks

```python
# --- Calcul LTV/CAC ---
# CAC = cout total acquisition / nb nouveaux clients
cac_data = pd.DataFrame({
    'month':        pd.period_range('2023-01', '2023-12', freq='M'),
    'marketing_spend': [45000, 52000, 48000, 61000, 58000, 55000,
                         49000, 67000, 72000, 68000, 75000, 90000],
    'new_customers':   [120, 135, 125, 158, 148, 140,
                         128, 170, 185, 172, 190, 225]
})

cac_data['cac'] = (cac_data['marketing_spend'] / cac_data['new_customers']).round(0)
avg_cac = cac_data['cac'].mean()

# LTV = CLV moyen (historique ou predict sur horizon client moyen)
avg_ltv = clv_12m['clv_12m'].mean() * 3  # extrapolation 36 mois simplifiee

ltv_cac_ratio = avg_ltv / avg_cac
print(f"CAC moyen   : {avg_cac:.0f} EUR")
print(f"LTV moyen   : {avg_ltv:.0f} EUR")
print(f"LTV/CAC     : {ltv_cac_ratio:.1f}x")
```

**Benchmarks LTV/CAC :**
| Ratio | Interpretation | Action |
|-------|---------------|--------|
| < 1:1 | Destruction de valeur | Revoir le modele economique en urgence |
| 1:1 - 3:1 | Sous-optimal | Reduire le CAC ou augmenter la retention |
| > 3:1 | Sain | Continuer, monitorer l'evolution |
| > 5:1 | Excellent | Envisager d'accelerer les investissements d'acquisition |

---

## Payback Period — Calcul et Benchmark

Le payback period est le nombre de mois necessaires pour recuperer le cout d'acquisition d'un client.

```python
# --- Payback Period ---
# Revenue mensuel moyen par client (gross margin incluse)
avg_monthly_revenue  = df.groupby('customer_id')['order_amount'].sum().mean() / 12
gross_margin_rate    = 0.65  # 65% de marge brute
avg_monthly_margin   = avg_monthly_revenue * gross_margin_rate

payback_months = avg_cac / avg_monthly_margin
print(f"Revenue mensuel moyen/client : {avg_monthly_revenue:.0f} EUR")
print(f"Marge mensuelle moy/client   : {avg_monthly_margin:.0f} EUR")
print(f"Payback period               : {payback_months:.1f} mois")
```

**Benchmarks Payback Period par Modele :**
| Modele | Payback sain | Payback acceptable | Alerte |
|--------|-------------|-------------------|--------|
| SaaS SMB | < 12 mois | 12-18 mois | > 24 mois |
| SaaS Enterprise | < 18 mois | 18-30 mois | > 36 mois |
| E-commerce | < 6 mois | 6-12 mois | > 18 mois |
| Fintech/Neobanque | < 9 mois | 9-18 mois | > 24 mois |

---

## Pipeline Complet — Cohort + CLV depuis Donnees Brutes

```python
import pandas as pd
import numpy as np
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data
import seaborn as sns
import matplotlib.pyplot as plt

# ============================================================
# PIPELINE COMPLET : COHORT ANALYSIS + CLV PREDICTIF
# ============================================================

def run_cohort_clv_pipeline(transactions_path: str, observation_end: str):

    # 1. Chargement
    df = pd.read_csv(transactions_path, parse_dates=['order_date'])
    df = df[df['order_status'].isin(['completed', 'shipped'])]
    df['order_amount'] = df['order_amount'].clip(lower=0)

    # 2. Analyse de cohorte
    df['cohort_month'] = df.groupby('customer_id')['order_date'].transform('min').dt.to_period('M')
    df['order_period']  = df['order_date'].dt.to_period('M')
    df['months_since']  = (df['order_period'] - df['cohort_month']).apply(lambda x: x.n)

    cohort_size   = df[df['months_since'] == 0].groupby('cohort_month')['customer_id'].nunique()
    cohort_matrix = df.groupby(['cohort_month', 'months_since'])['customer_id'].nunique().unstack()
    retention     = cohort_matrix.divide(cohort_size, axis=0).round(3) * 100

    # 3. Heatmap
    plt.figure(figsize=(14, 7))
    sns.heatmap(retention, annot=True, fmt='.0f', cmap='Blues', vmin=0, vmax=100)
    plt.title('Retention par Cohorte (%)')
    plt.tight_layout()
    plt.savefig('cohort_retention.png', dpi=150)
    plt.close()

    # 4. CLV predictif
    summary = summary_data_from_transaction_data(
        df, customer_id_col='customer_id', datetime_col='order_date',
        monetary_value_col='order_amount', observation_period_end=observation_end, freq='D'
    )
    summary = summary[(summary['frequency'] > 0) & (summary['monetary_value'] > 0)]

    bgf = BetaGeoFitter(penalizer_coef=0.01)
    bgf.fit(summary['frequency'], summary['recency'], summary['T'])

    ggf = GammaGammaFitter(penalizer_coef=0.001)
    ggf.fit(summary['frequency'], summary['monetary_value'])

    clv = ggf.customer_lifetime_value(
        bgf, summary['frequency'], summary['recency'],
        summary['T'], summary['monetary_value'], time=12, discount_rate=0.01, freq='D'
    ).reset_index()
    clv.columns = ['customer_id', 'clv_12m']

    # 5. Rapport
    print("\n=== RAPPORT CLV PREDICTIF 12 MOIS ===")
    print(clv['clv_12m'].describe().round(0))
    print(f"\nCLV total predit (12m) : {clv['clv_12m'].sum():,.0f} EUR")

    return retention, clv

# Execution
retention, clv = run_cohort_clv_pipeline('transactions.csv', '2024-01-01')
```
