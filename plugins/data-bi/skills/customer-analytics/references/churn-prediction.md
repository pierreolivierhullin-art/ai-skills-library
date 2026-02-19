# Prediction du Churn — ML et Health Score

## Definition et Typologies du Churn

**Churn volontaire :** le client choisit deliberement de partir — resiliation d'abonnement, non-renouvellement de contrat, arret d'utilisation du service. C'est le plus frequent et le plus predictible.

**Churn involontaire :** echec de paiement, carte expiree, probleme technique. Represent 20-30% du churn total dans le SaaS. Se traite avec des processus de dunning automatises, pas des modeles ML.

**Leading indicators (signaux precurseurs) :** metriques qui evoluent AVANT le churn. Diminution des logins, baisse du volume traite, chute de l'engagement email, ouverture de tickets support, inactivite sur des features cles. Ces signaux apparaissent en general 30 a 90 jours avant le depart.

**Lagging indicators (indicateurs retardes) :** taux de churn mensuel, NRR, revenue perdu. Mesurent le churn apres qu'il s'est produit. Indispensables pour mesurer les resultats, inutiles pour l'anticiper.

L'objectif du modele de churn prediction est de transformer des leading indicators en score d'action — permettre a l'equipe Customer Success d'intervenir avant que le churn soit consomme.

---

## Feature Engineering pour le Churn

Construire des features riches est la partie la plus critique du pipeline. Un modele simple avec de bonnes features surpasse un modele complexe avec de mauvaises features.

### Metriques d'Usage Produit

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def compute_usage_features(events_df, accounts_df, snapshot_date, lookback_days=90):
    """
    Calcule les features d'usage produit sur la fenetre de lookback.
    events_df : table evenements (account_id, event_date, event_type, feature_name)
    """
    cutoff = pd.Timestamp(snapshot_date)
    start  = cutoff - timedelta(days=lookback_days)

    events = events_df[
        (events_df['event_date'] >= start) &
        (events_df['event_date'] <  cutoff)
    ].copy()

    usage = events.groupby('account_id').agg(
        # Volume d'usage global
        total_events         = ('event_type',   'count'),
        active_days          = ('event_date',   lambda x: x.dt.date.nunique()),
        # Features actives (diversite d'usage)
        unique_features_used = ('feature_name', 'nunique'),
        # Sessions
        total_sessions       = ('session_id',   'nunique'),
        # Recence (jours depuis derniere activite)
        days_since_last_use  = ('event_date',   lambda x: (cutoff - x.max()).days),
    ).reset_index()

    # Tendance : comparer fenetre recente vs fenetre precedente
    mid = cutoff - timedelta(days=lookback_days // 2)
    recent = events[events['event_date'] >= mid].groupby('account_id')['event_type'].count().rename('events_recent_half')
    early  = events[events['event_date'] <  mid].groupby('account_id')['event_type'].count().rename('events_early_half')

    usage = usage.merge(recent, on='account_id', how='left').merge(early, on='account_id', how='left')
    # Ratio de tendance : < 1 = usage en baisse (signal churn)
    usage['usage_trend_ratio'] = (
        usage['events_recent_half'] / (usage['events_early_half'] + 1)
    ).round(3)

    return usage
```

### Metriques d'Engagement

```python
def compute_engagement_features(email_df, support_df, nps_df, account_id_col='account_id'):
    """Features d'engagement multi-canal."""

    # Email
    email_feat = email_df.groupby(account_id_col).agg(
        emails_sent          = ('email_id',  'count'),
        emails_opened        = ('opened',    'sum'),
        emails_clicked       = ('clicked',   'sum'),
    ).reset_index()
    email_feat['open_rate']  = (email_feat['emails_opened']  / email_feat['emails_sent'].clip(lower=1)).round(3)
    email_feat['click_rate'] = (email_feat['emails_clicked'] / email_feat['emails_sent'].clip(lower=1)).round(3)

    # Support
    support_feat = support_df.groupby(account_id_col).agg(
        nb_tickets          = ('ticket_id',      'count'),
        avg_resolution_days = ('resolution_days', 'mean'),
        nb_escalations      = ('escalated',       'sum'),
        pct_negative        = ('sentiment',       lambda x: (x == 'negative').mean()),
    ).reset_index()

    # NPS
    nps_feat = nps_df.groupby(account_id_col).agg(
        latest_nps         = ('nps_score', 'last'),
        nps_trend          = ('nps_score', lambda x: x.iloc[-1] - x.iloc[0] if len(x) > 1 else 0),
    ).reset_index()

    return email_feat.merge(support_feat, on=account_id_col, how='outer').merge(nps_feat, on=account_id_col, how='outer')
```

### Metriques Financieres

```python
def compute_financial_features(billing_df, contracts_df):
    """Features financieres et contractuelles."""

    billing_feat = billing_df.groupby('account_id').agg(
        mrr                 = ('mrr',                'last'),
        mrr_3m_growth       = ('mrr',                lambda x: (x.iloc[-1] / x.iloc[-4] - 1) if len(x) >= 4 else 0),
        nb_payment_failures = ('payment_status',     lambda x: (x == 'failed').sum()),
        days_overdue_max    = ('days_overdue',        'max'),
        had_downgrade       = ('plan_change',         lambda x: (x == 'downgrade').any().astype(int)),
        had_upgrade         = ('plan_change',         lambda x: (x == 'upgrade').any().astype(int)),
    ).reset_index()

    contract_feat = contracts_df[['account_id', 'contract_type', 'contract_end_date',
                                  'days_until_renewal', 'nb_seats', 'annual_contract_value']].copy()

    return billing_feat.merge(contract_feat, on='account_id', how='left')
```

### Metriques Relationnelles et Contrat

```python
def compute_relationship_features(contacts_df, accounts_df):
    """Features sur la relation client et le profil du compte."""

    contact_feat = contacts_df.groupby('account_id').agg(
        nb_contacts_known   = ('contact_id',   'count'),
        has_champion        = ('is_champion',  'max'),
        has_economic_buyer  = ('role',         lambda x: (x == 'economic_buyer').any().astype(int)),
        nb_active_contacts  = ('last_login',   lambda x: (x >= pd.Timestamp.now() - pd.Timedelta(days=30)).sum()),
    ).reset_index()

    account_feat = accounts_df[['account_id', 'industry', 'company_size',
                                 'country', 'months_as_customer', 'onboarding_score']].copy()

    return contact_feat.merge(account_feat, on='account_id', how='left')
```

---

## Pipeline de Training Complet — Scikit-Learn

### Preparation des Donnees et Labelisation

```python
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score, classification_report, RocCurveDisplay
import shap

def create_churn_labels(accounts_df, churn_events_df, snapshot_date, prediction_window_days=90):
    """
    Labelise les comptes : churne=1 si desabonnement dans les 90 prochains jours.
    IMPORTANT : utiliser la date de snapshot pour separer features et label.
    """
    snapshot    = pd.Timestamp(snapshot_date)
    window_end  = snapshot + timedelta(days=prediction_window_days)

    # Comptes actifs au moment du snapshot
    active = accounts_df[
        accounts_df['subscription_start'] < snapshot
    ].copy()

    # Comptes qui ont churne dans la fenetre de prediction
    churned = churn_events_df[
        (churn_events_df['churn_date'] >= snapshot) &
        (churn_events_df['churn_date'] <  window_end)
    ]['account_id'].unique()

    active['churned_90d'] = active['account_id'].isin(churned).astype(int)

    print(f"Base de modelisation : {len(active):,} comptes")
    print(f"  - Churnes (label=1) : {active['churned_90d'].sum():,} ({active['churned_90d'].mean():.1%})")
    print(f"  - Actifs  (label=0) : {(active['churned_90d']==0).sum():,}")

    return active
```

### Pourquoi le Split Chronologique

Ne jamais utiliser un split aleatoire pour un modele de churn. Un split random permettrait au modele d'observer le comportement d'un compte en janvier pour predire son churn en decembre de l'annee precedente — ce qui est impossible en production. Le split chronologique reproduit fidelement les conditions de deploiement.

```python
def chronological_train_test_split(df, date_col='snapshot_date', test_ratio=0.2):
    """Split chronologique : les donnees les plus recentes servent de test."""
    df = df.sort_values(date_col)
    split_idx = int(len(df) * (1 - test_ratio))
    split_date = df.iloc[split_idx][date_col]

    train = df[df[date_col] <  split_date].copy()
    test  = df[df[date_col] >= split_date].copy()

    print(f"Train : {len(train):,} observations (jusqu'a {split_date.date()})")
    print(f"Test  : {len(test):,}  observations (depuis {split_date.date()})")
    return train, test
```

### Training du Modele GradientBoosting

```python
# --- Features et target ---
FEATURE_COLS = [
    'total_events', 'active_days', 'unique_features_used', 'days_since_last_use',
    'usage_trend_ratio', 'open_rate', 'click_rate', 'nb_tickets',
    'pct_negative', 'latest_nps', 'mrr', 'mrr_3m_growth',
    'nb_payment_failures', 'days_overdue_max', 'had_downgrade',
    'days_until_renewal', 'nb_contacts_known', 'has_champion',
    'months_as_customer', 'onboarding_score'
]

TARGET_COL = 'churned_90d'

X_train = train[FEATURE_COLS].fillna(0)
y_train = train[TARGET_COL]
X_test  = test[FEATURE_COLS].fillna(0)
y_test  = test[TARGET_COL]

# --- Hyperparameter tuning par TimeSeriesSplit ---
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators':      [100, 200, 300],
    'max_depth':         [3, 4, 5],
    'learning_rate':     [0.05, 0.1, 0.15],
    'subsample':         [0.8, 1.0],
    'min_samples_leaf':  [20, 50]
}

tscv  = TimeSeriesSplit(n_splits=5)
model = GradientBoostingClassifier(random_state=42)

grid_search = GridSearchCV(
    model, param_grid,
    cv=tscv, scoring='roc_auc',
    n_jobs=-1, verbose=1
)
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
print(f"Meilleurs hyperparametres : {grid_search.best_params_}")
```

### Evaluation du Modele

```python
# --- Predictions ---
y_pred_proba = best_model.predict_proba(X_test)[:, 1]
y_pred_class = (y_pred_proba >= 0.5).astype(int)

# --- Metriques ---
auc = roc_auc_score(y_test, y_pred_proba)
print(f"\nAUC-ROC : {auc:.3f}")
print("\nRapport de classification :")
print(classification_report(y_test, y_pred_class))

# --- Courbe precision-recall ---
from sklearn.metrics import PrecisionRecallDisplay
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ROC
RocCurveDisplay.from_predictions(y_test, y_pred_proba, ax=axes[0])
axes[0].set_title(f'Courbe ROC (AUC = {auc:.3f})')
axes[0].plot([0, 1], [0, 1], 'k--', label='Random')

# Precision-Recall
PrecisionRecallDisplay.from_predictions(y_test, y_pred_proba, ax=axes[1])
axes[1].set_title('Courbe Precision-Recall')

plt.tight_layout()
plt.savefig('churn_model_evaluation.png', dpi=150)
```

### Feature Importance avec SHAP Values

```python
# --- SHAP Values ---
# pip install shap
import shap

explainer   = shap.TreeExplainer(best_model)
shap_values = explainer.shap_values(X_test)

# Importance globale
shap.summary_plot(shap_values, X_test, feature_names=FEATURE_COLS,
                  plot_type='bar', max_display=15, show=False)
plt.title('Feature Importance (SHAP values)')
plt.tight_layout()
plt.savefig('shap_importance.png', dpi=150)
plt.close()

# Dependence plot : effet de l'usage_trend_ratio sur le churn
shap.dependence_plot('usage_trend_ratio', shap_values, X_test, show=False)
plt.tight_layout()
plt.savefig('shap_usage_trend.png', dpi=150)
plt.close()

# Explication individuelle d'un compte specifique
account_idx = 42  # index dans X_test
shap.waterfall_plot(shap.Explanation(
    values        = shap_values[account_idx],
    base_values   = explainer.expected_value,
    data          = X_test.iloc[account_idx],
    feature_names = FEATURE_COLS
))
```

---

## Customer Health Score

### Architecture : Score Composite Pondere 0-100

Le health score aggregate plusieurs dimensions de sante du compte en un score unique, actionnable par les equipes Customer Success. Chaque dimension est notee de 0 a 100, puis les scores sont combines avec des poids determines par leur correlation avec le churn.

**5 categories et poids recommandes :**

| Categorie | Poids | Exemples de signals |
|-----------|-------|---------------------|
| Usage | 35% | Logins/semaine, features actives, volume traite |
| Adoption | 25% | % features utilisees, progression onboarding |
| Engagement | 20% | NPS, emails ouverts, reponse CS |
| Financier | 10% | Paiements a jour, pas de downgrade |
| Sentiment | 10% | Qualite tickets support, escalations |

### Code Python — Calcul du Health Score

```python
def compute_health_score(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule le Customer Health Score sur 100 points.
    Toutes les features doivent etre normalisees entre 0 et 1.
    """
    df = features_df.copy()

    # --- Normalisation des composantes (0-1) ---
    def normalize(series, higher_is_better=True, cap=None):
        s = series.clip(upper=cap) if cap else series
        normalized = (s - s.min()) / (s.max() - s.min() + 1e-9)
        return normalized if higher_is_better else 1 - normalized

    # USAGE (35 pts max)
    df['usage_component'] = (
        normalize(df['active_days'],          higher_is_better=True)  * 0.4 +
        normalize(df['unique_features_used'], higher_is_better=True)  * 0.3 +
        normalize(df['usage_trend_ratio'],    higher_is_better=True)  * 0.2 +
        normalize(df['days_since_last_use'],  higher_is_better=False) * 0.1
    ) * 35

    # ADOPTION (25 pts max)
    df['adoption_component'] = (
        normalize(df['feature_adoption_pct'],  higher_is_better=True) * 0.6 +
        normalize(df['onboarding_score'],      higher_is_better=True) * 0.4
    ) * 25

    # ENGAGEMENT (20 pts max)
    df['engagement_component'] = (
        normalize(df['latest_nps'],            higher_is_better=True) * 0.5 +
        normalize(df['open_rate'],             higher_is_better=True) * 0.3 +
        normalize(df['nb_escalations'],        higher_is_better=False) * 0.2
    ) * 20

    # FINANCIER (10 pts max)
    df['financial_component'] = (
        (1 - df['had_downgrade'])                                       * 0.5 +
        normalize(df['nb_payment_failures'],   higher_is_better=False) * 0.3 +
        (1 - (df['days_overdue_max'] > 0).astype(float))               * 0.2
    ) * 10

    # SENTIMENT (10 pts max)
    df['sentiment_component'] = (
        normalize(df['pct_negative'],          higher_is_better=False) * 0.6 +
        normalize(df['avg_resolution_days'],   higher_is_better=False) * 0.4
    ) * 10

    # SCORE TOTAL
    df['health_score'] = (
        df['usage_component']     +
        df['adoption_component']  +
        df['engagement_component']+
        df['financial_component'] +
        df['sentiment_component']
    ).clip(0, 100).round(1)

    # STATUT
    df['health_status'] = pd.cut(
        df['health_score'],
        bins   = [-1, 40, 70, 101],
        labels = ['Rouge', 'Jaune', 'Vert']
    )

    return df
```

### Thresholds et Interpretation

| Score | Statut | Signification | Action |
|-------|--------|--------------|--------|
| > 70 | Vert | Client sain, engagement fort | Monitoring standard, opportunite upsell |
| 40-70 | Jaune | Signaux de faiblesse, risque modere | Outreach CS proactif dans 7 jours |
| < 40 | Rouge | Risque churn eleve, intervention urgente | Alerte immediate CS, action sous 48h |

### Alerting — Workflow CS via Slack

```python
import requests
import json

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

def send_churn_alert(account: dict, previous_score: float, current_score: float):
    """Envoie une alerte Slack quand un compte passe en zone rouge."""

    if current_score >= 40 or previous_score < 40:
        return  # Pas d'alerte si deja rouge ou pas de degradation vers rouge

    score_change = current_score - previous_score
    emoji = "🔴" if current_score < 40 else "🟡"

    message = {
        "text": f"{emoji} *Alerte Churn — {account['account_name']}*",
        "attachments": [{
            "color": "danger" if current_score < 40 else "warning",
            "fields": [
                {"title": "Health Score",    "value": f"{previous_score} → {current_score} ({score_change:+.0f})", "short": True},
                {"title": "MRR",             "value": f"{account['mrr']:,} EUR", "short": True},
                {"title": "CS Responsable",  "value": account['cs_owner'],        "short": True},
                {"title": "Derniere activite","value": f"il y a {account['days_since_last_use']} jours", "short": True},
            ],
            "footer": f"Action requise sous 48h — Voir fiche CRM : {account['crm_url']}"
        }]
    }

    requests.post(SLACK_WEBHOOK_URL, data=json.dumps(message))
```

---

## Playbook de Retention par Segment de Risque

### Risque Eleve — Score < 40 (Zone Rouge)

**Action humaine immediate sous 48 heures.**
1. Appel du CS Manager responsable du compte (pas un email)
2. Audit interne : revue du log d'usage, tickets recents, historique NPS
3. Agenda partage avec l'equipe client : diagnostic conjoint des blocages
4. Plan d'action ecrit avec dates et responsables (des deux cotes)
5. Suivi hebdomadaire pendant 60 jours minimum

**Messages a eviter :** les emails generiques "Nous n'avons pas de vos nouvelles..." — ils signalent que l'entreprise n'a pas analyse la situation reelle du compte.

### Risque Moyen — Score 40-70 (Zone Jaune)

**Sequence email automatique + ressources.**
- J+0 : email personnalise base sur l'usage reel (feature peu utilisee = lien vers tutoriel)
- J+7 : invitation webinar "best practices" ou session Q&A
- J+14 : check-in CS par email (pas d'appel a ce stade)
- J+21 : envoi case study pertinent pour l'industrie du client
- J+30 : appel CS si le score n'a pas remonte au-dessus de 55

### Risque Faible — Score > 70 (Zone Verte)

**Programme nurture et expansion.**
- Newsletter mensuelle avec nouveautes produit et contenu educatif
- Invitation evenements clients (summit, webinars exclusifs)
- Revue QBR (Quarterly Business Review) si MRR > seuil defini
- Proposition expansion : nouveaux seats, nouvelles features, modules additionels

---

## Metriques du Programme de Retention

Mesurer l'efficacite du programme de retention avec des KPIs clairs et attribuables.

```python
def compute_retention_program_metrics(before_df, after_df, intervention_df):
    """
    before_df  : comptes en risque avant intervention (snapshot T)
    after_df   : statut des memes comptes 90 jours apres (snapshot T+90)
    intervention_df : comptes ayant recu une action CS
    """

    # Taux de churn sauve
    at_risk  = before_df[before_df['health_status'] == 'Rouge']
    saved    = at_risk.merge(after_df, on='account_id', suffixes=('_before', '_after'))
    saved    = saved[saved['churned_90d'] == 0]

    churn_saved_rate   = len(saved) / len(at_risk) if len(at_risk) > 0 else 0
    revenue_saved      = saved['mrr'].sum() * 12  # ARR

    # ROI CS
    cs_team_cost_annual  = 180000  # cout total equipe CS (salaires + charges)
    revenue_retained     = revenue_saved
    roi_multiple         = revenue_retained / cs_team_cost_annual

    print("=== METRIQUES PROGRAMME RETENTION ===")
    print(f"Comptes en zone rouge (T)      : {len(at_risk):,}")
    print(f"Comptes sauves (non-churned)   : {len(saved):,}")
    print(f"Taux de churn sauve            : {churn_saved_rate:.1%}")
    print(f"Revenue annuel retenu          : {revenue_saved:,.0f} EUR")
    print(f"ROI equipe CS                  : {roi_multiple:.1f}x")

    return {
        'churn_rate_saved': churn_saved_rate,
        'revenue_saved_eur': revenue_saved,
        'roi_cs': roi_multiple
    }
```

**Benchmarks programme retention :**
| Metrique | Bon | Excellent |
|----------|-----|-----------|
| Taux churn sauve (zone rouge) | 30-40% | > 50% |
| Delai intervention (rouge) | < 72h | < 24h |
| NRR post-programme | > 100% | > 110% |
| ROI equipe CS | > 3x | > 6x |
