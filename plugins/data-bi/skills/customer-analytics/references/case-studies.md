# Etudes de Cas — Customer Analytics en Production

## Vue d'ensemble

Quatre cas concrets d'implementation de customer analytics dans des environnements de production. Chaque cas documente le contexte initial, les choix techniques, les resultats mesures et les leçons applicables.

---

## Cas 1 — E-commerce Mode : Segmentation RFM → +23% Revenue par Email

### Contexte Initial

E-commerce de pret-a-porter feminin, 250 000 clients actifs dans la base, present depuis 7 ans. Pratique historique : un email blast hebdomadaire envoye a toute la base (meme message, meme offre, meme visuel).

Metriques initiales :
- Open rate moyen : 18%
- Click-through rate : 2.1%
- Conversion email → achat : 0.8%
- Revenue attribuable aux emails : 12% du CA total
- Taux de desinscription : 0.8% par envoi

**Probleme identifie :** les clients VIP (Champions, 8% de la base, 35% du CA) recevaient les memes emails promotionnels que les clients inactifs. Les clients inactifs recevaient des offres sans pertinence et se desinscrivaient massivement. La pression email non ciblee degradait la deliverabilite globale.

### Implementation RFM

**Etape 1 — Calcul RFM** sur 18 mois d'historique de transactions (PostgreSQL).

```sql
-- Scoring RFM sur 12 mois glissants
WITH rfm_base AS (
  SELECT
    customer_email,
    customer_id,
    DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY)   AS recency_days,
    COUNT(DISTINCT order_id)                           AS frequency,
    SUM(order_amount_net)                              AS monetary
  FROM orders
  WHERE
    order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
    AND order_status = 'completed'
  GROUP BY customer_email, customer_id
)
-- Scoring + segmentation (voir reference rfm-segmentation.md pour le detail complet)
SELECT
  customer_id,
  customer_email,
  NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
  NTILE(5) OVER (ORDER BY frequency ASC)    AS f_score,
  NTILE(5) OVER (ORDER BY monetary ASC)     AS m_score
FROM rfm_base;
```

**Etape 2 — Reduction a 8 groupes actionables** (les 11 segments classiques fusionnes selon les capacites de production creative) :

| Groupe CRM | Segments RFM | Taille | % CA |
|-----------|-------------|--------|------|
| VIP | Champions | 8% | 35% |
| Fideles | Loyal Customers | 12% | 25% |
| A developper | Potential Loyalists + New Customers | 15% | 10% |
| Attention requise | Need Attention + Promising | 18% | 12% |
| Retention urgente | At Risk + "Can't Lose Them" | 10% | 10% |
| Re-engagement | About to Sleep | 12% | 5% |
| Inactifs | Hibernating + Lost | 25% | 3% |

**Etape 3 — Production creative par segment.** Plutot que de personnaliser individuellement, produire 8 versions de chaque campagne avec :
- Message principal adapte au comportement (recompense VIP vs. retention At Risk vs. surprise New Customer)
- Selection produits basee sur l'historique de categorie du segment
- Promotion differenciee : pas de remise pour les VIP (ils achetent au prix plein), remise 20% pour At Risk

**Etape 4 — Test A/B pre-lancement.** Chaque groupe splitte en deux : 50% reçoit le message segmente, 50% reçoit le blast classique. Duree du test : 4 semaines.

### Resultats du Test

| Groupe | Open Rate (blast) | Open Rate (segmente) | Conversion (blast) | Conversion (segmente) |
|--------|------------------|---------------------|-------------------|--------------------|
| VIP | 24% | 41% | 1.2% | 2.8% |
| Fideles | 21% | 35% | 1.0% | 2.1% |
| At Risk | 16% | 28% | 0.6% | 1.4% |
| Re-engagement | 12% | 22% | 0.3% | 0.9% |
| **Moyenne** | **18%** | **31%** | **0.8%** | **1.9%** |

**Resultats apres generalisation (6 mois) :**
- Open rate moyen : 18% → 31% (+72%)
- Revenue email : +23% a volume d'envoi constant
- Taux de desinscription : 0.8% → 0.48% par envoi (-40%)
- Deliverabilite (reputation domaine) : amelioration mesurable (bounce rate -15%)

**Resultats financiers :** revenue email annuel passe de 2.4M EUR a 2.95M EUR. Cout d'implementation (8 jours de travail data + adaptation creative) : 12K EUR. ROI immediat : 45x.

### Lesson Principale

La personnalisation par comportement (RFM) surpasse systematiquement la personnalisation par donnees demographiques (age, genre, localisation). Les clients VIP qui recoivent une communication traitant leur statut de facon adequide ont un taux de reachat superieur de 40% vs. ceux qui reçoivent une offre promotionnelle generique. Ne pas offrir une remise a ses meilleurs clients — c'est une erreur qui detruit la valeur perçue du produit.

---

## Cas 2 — SaaS B2B : CLV Prediction pour Priorisation Sales

### Contexte Initial

SaaS RH (gestion des recrutements), 800 comptes en freemium actifs, produit freemium gratuit jusqu'a 3 offres d'emploi actives. Equipe commerciale de 3 personnes pour convertir freemium → payant.

Probleme initial : les sales priorisaient leurs relances manuellement (taille de l'entreprise visible sur LinkedIn, feeling, timing). Taux de conversion freemium → payant : 8%. ACV moyen sur les conversions : 4 200 EUR.

**Hypothese testee :** en predisant le CLV potentiel de chaque compte freemium et en concentrant les efforts sales sur les 20% a plus fort CLV predit, on peut augmenter le taux de conversion ET l'ACV moyen.

### Construction du Modele CLV Predictif

**Features disponibles sur les comptes freemium :**

```python
# Features extraites pour chaque compte freemium
freemium_features = {
    # Usage produit (signal fort)
    'active_job_postings':     'nb offres actives (cap: 3 en freemium)',
    'logins_last_30d':         'connexions au produit sur 30 jours',
    'candidate_profiles_viewed': 'profils candidats consultes',
    'collaborators_invited':   'collegues invites dans le produit',
    'time_to_first_posting':   'delai inscription → premiere offre (jours)',

    # Profil entreprise (proxies de valeur potentielle)
    'company_headcount':       'taille enterprise (LinkedIn)',
    'industry':                'secteur (one-hot encode)',
    'nb_open_roles_linkedin':  'nb postes ouverts sur LinkedIn (scraping)',
    'funding_stage':           'stade de financement (Crunchbase)',
    'country':                 'pays (one-hot encode)',

    # Engagement marketing
    'emails_opened_30d':       'emails ouverts sur 30 jours',
    'webinar_attended':        'participation aux webinars (binaire)',
    'requested_demo':          'a demande une demo (binaire)',
}
```

**Modele : XGBoost regression sur CLV 24 mois.**

Le CLV 24 mois est calcule sur les comptes PAYANTS existants (ground truth), puis le modele apprend a predire ce CLV depuis les features disponibles au stade freemium. La prediction s'applique ensuite aux 800 comptes freemium actuels.

```python
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
import numpy as np

# Donnees d'entrainement : comptes devenus payants il y a plus de 24 mois
paying_accounts = pd.read_csv('paying_accounts_with_freemium_features.csv')
paying_accounts['clv_24m'] = paying_accounts['revenue_24m_post_conversion']

# Split chronologique
split_date   = paying_accounts['conversion_date'].quantile(0.8)
train        = paying_accounts[paying_accounts['conversion_date'] < split_date]
test         = paying_accounts[paying_accounts['conversion_date'] >= split_date]

FEATURES = [col for col in paying_accounts.columns
            if col not in ['account_id', 'clv_24m', 'conversion_date']]

model = XGBRegressor(
    n_estimators   = 300,
    max_depth      = 4,
    learning_rate  = 0.05,
    subsample      = 0.8,
    random_state   = 42
)
model.fit(train[FEATURES], train['clv_24m'])

# Evaluation
y_pred = model.predict(test[FEATURES])
mae    = mean_absolute_error(test['clv_24m'], y_pred)
r2     = r2_score(test['clv_24m'], y_pred)
print(f"MAE : {mae:.0f} EUR | R² : {r2:.3f}")
# MAE : 1 840 EUR | R² : 0.61

# Prediction sur les 800 comptes freemium
freemium = pd.read_csv('current_freemium_accounts.csv')
freemium['predicted_clv_24m'] = model.predict(freemium[FEATURES])
freemium['sales_priority']    = pd.qcut(
    freemium['predicted_clv_24m'],
    q=[0, 0.5, 0.8, 1.0],
    labels=['Low', 'Medium', 'High']
)
```

**Top features predictives (SHAP) :**
1. `nb_open_roles_linkedin` : le signal le plus fort — une entreprise qui recrute a besoin d'un ATS
2. `collaborators_invited` : signe de viralite interne, l'outil se repand dans l'equipe
3. `company_headcount` : taille = willingness to pay et expansion potential
4. `logins_last_30d` : engagement direct
5. `funding_stage` : les Scale-ups ont des budgets et des besoins de recrutement forts

### Priorisation Sales et Resultats

Les 800 comptes freemium classes : 160 en "High CLV predit" (20% top), 240 en "Medium", 400 en "Low".

Les 3 sales concentrent leurs relances sur les 160 comptes High CLV. Les comptes Medium reçoivent une sequence email automatisee. Les comptes Low : nurture automatique sans intervention humaine.

**Resultats apres 6 mois :**

| Segment | Nb comptes | Taux conversion | ACV moyen |
|---------|-----------|----------------|-----------|
| High CLV predit | 160 | 23% (+187%) | 5 880 EUR (+40%) |
| Medium CLV predit | 240 | 9% (+12%) | 4 100 EUR (-2%) |
| Low CLV predit | 400 | 4% (-50%) | 2 900 EUR (-31%) |
| **Avant priorisation (baseline)** | **800** | **8%** | **4 200 EUR** |

Revenue additionnel genere vs. baseline (sur 6 mois) :
- High : 160 x 23% x 5 880 = 216 384 EUR
- Medium : 240 x 9% x 4 100 = 88 560 EUR
- Avant : 800 x 8% x 4 200 = 268 800 EUR (base annualisee / 2)
- **Net additionnel : +36 144 EUR sur 6 mois sans recrutement sales**

### Lesson Principale

Le CLV predictif est le meilleur signal de priorisation sales pour un SaaS freemium. La taille d'entreprise seule est insuffisante (une grande entreprise peu engagee dans le produit a un faible CLV potentiel). La combinaison usage produit + profil entreprise + signaux d'intention (ouvertures de postes) produit un signal 3x plus predictif que la qualification manuelle.

---

## Cas 3 — SaaS Project Management : Health Score qui Reduit le Churn de 35%

### Contexte Initial

SaaS de gestion de projets, segment PME (5-50 employes), 1 200 clients payants, MRR 280K EUR. Churn annuel : 12% (benchmark secteur : 8-10%). Equipe CS : 2 personnes pour 1 200 comptes.

**Probleme structurel :** approche reactive. L'equipe CS n'intervenait qu'apres qu'un client avait contacte le support ou, pire, apres reception de la notification de resiliation. Aucune visibilite sur l'etat de sante des comptes en temps reel.

Estimation du cout du churn : 12% de 280K EUR MRR = 33 600 EUR MRR perdu par an = 403 200 EUR ARR.

### Construction du Health Score

**Phase 1 — Determination des poids par analyse de correlation.**

Calculer la correlation de Spearman entre chaque metrique et le churn observe sur 24 mois d'historique. Les correlations determinent les poids de chaque composante.

```python
import pandas as pd
from scipy.stats import spearmanr

# Correlations metriques → churn (valeur absolue)
correlations = {}
metrics = ['active_days_30d', 'features_used_pct', 'logins_week',
           'nps_score', 'support_tickets_open', 'payment_failures',
           'onboarding_completion', 'days_since_last_login']

for metric in metrics:
    corr, pval = spearmanr(df[metric], df['churned_90d'])
    correlations[metric] = abs(corr)
    print(f"{metric:35s} : {corr:+.3f} (p={pval:.4f})")
```

**Resultats de l'analyse de correlation :**

| Metrique | Correlation avec churn | Sens |
|---------|----------------------|------|
| days_since_last_login | 0.68 | + = risque |
| features_used_pct | -0.61 | - = risque |
| nps_score | -0.54 | - = risque |
| onboarding_completion | -0.51 | - = risque |
| support_tickets_open | +0.43 | + = risque |
| active_days_30d | -0.41 | - = risque |
| payment_failures | +0.38 | + = risque |

**Phase 2 — Architecture du score final :**

```python
def saas_pm_health_score(df: pd.DataFrame) -> pd.DataFrame:
    """Health Score pour SaaS Project Management — 5 dimensions."""
    d = df.copy()

    # USAGE (35 pts) : activite et recence
    d['score_usage'] = (
        (1 - (d['days_since_last_login'].clip(0, 30) / 30)) * 0.5 +
        (d['active_days_30d'].clip(0, 20) / 20)             * 0.3 +
        (d['logins_week'].clip(0, 10) / 10)                 * 0.2
    ) * 35

    # ADOPTION (25 pts) : profondeur d'utilisation du produit
    d['score_adoption'] = (
        (d['features_used_pct'].clip(0, 1))                          * 0.6 +
        (d['onboarding_completion'].clip(0, 1))                       * 0.4
    ) * 25

    # ENGAGEMENT (20 pts) : NPS + engagement marketing
    d['score_engagement'] = (
        ((d['nps_score'].clip(-100, 100) + 100) / 200)               * 0.7 +
        (d['email_open_rate_30d'].clip(0, 1))                         * 0.3
    ) * 20

    # FINANCIER (10 pts)
    d['score_financial'] = (
        (1 - d['had_payment_failure'].clip(0, 1))                     * 0.6 +
        (1 - d['had_downgrade'].clip(0, 1))                           * 0.4
    ) * 10

    # SENTIMENT (10 pts)
    d['score_sentiment'] = (
        (1 - (d['open_tickets_critical'].clip(0, 3) / 3))            * 0.7 +
        (1 - d['had_escalation_30d'].clip(0, 1))                     * 0.3
    ) * 10

    d['health_score'] = (
        d['score_usage'] + d['score_adoption'] + d['score_engagement'] +
        d['score_financial'] + d['score_sentiment']
    ).clip(0, 100).round(1)

    d['health_color'] = pd.cut(
        d['health_score'],
        bins=[-1, 40, 70, 101],
        labels=['Rouge', 'Jaune', 'Vert']
    )
    return d
```

### Alerting et Playbook CS

**Alerting Slack automatise :** chaque nuit, un job calcule les health scores. Si un compte passe de Vert ou Jaune vers Rouge, alerte Slack immediate au CS responsable.

**Playbook par segment :**

- **Rouge (< 40) :** appel dans les 48h. Agenda de "compte sauve" ouvert dans le CRM. Revue interne avec le product manager si le probleme est lie a une feature manquante.
- **Jaune (40-70) :** email personnalise automatique J+1 avec ressource ciblee (video tutoriel sur la feature peu utilisee, invitation webinar). Suivi CS J+14 si pas d'amelioration.
- **Vert en degradation** (score en baisse 3 semaines consecutives) : proactivite, QBR anticipee.

### Resultats Apres 6 Mois

| Metrique | Avant | Apres (6 mois) |
|----------|-------|----------------|
| Churn annuel | 12% | 7.8% |
| NRR | 96% | 104% |
| Delai detection risque | Post-resiliation | 45 jours avant |
| Comptes sauves / mois | 0 (pas de tracking) | 8-12 / mois |
| CS contacts proactifs / mois | 15 | 65 |

**ROI calcule :**
- Reduction churn MRR : 12% → 7.8% sur 280K MRR = 11 760 EUR MRR sauve mensuel
- ARR retenu additionnel : 141 120 EUR
- Cout de mise en oeuvre (developpement pipeline + 1 trimestre CS manager) : 35 000 EUR
- Payback : 3 mois. ROI annuel : 4x.

**Effet secondaire inattendu :** le NRR est passe de 96% a 104% en 6 mois. Les CS, desormais moins en mode extincteur, ont pu identifier 23 comptes Vert avec fort potentiel d'expansion (upsell seats additionels). 9 expansions conclues = 18 200 EUR MRR additionnel.

### Lesson Principale

La detection precoce transforme le CS d'un role reactif (pompier) en role proactif (medecin preventif). Le health score ne predit pas le churn avec une precision parfaite — il permet d'intervenir suffisamment tot pour changer le trajectory. Un mois de prodrome est suffisant si l'equipe a un playbook clair. L'investissement dans les alertes automatisees est recupere en moins d'un trimestre.

---

## Cas 4 — Fintech / Neobanque : Churn Prediction Model en Production

### Contexte Initial

Neobanque B2C, 500 000 clients actifs, produit gratuit avec options premium payantes (carte Metal, assurances, facilites de paiement). Churn tres difficile a predire : pas de contrat formel, le client "disparait" progressivement — ses transactions ralentissent, puis il ouvre un compte chez un concurrent.

Definition operationnelle du churn : aucune transaction sur 90 jours consecutifs apres avoir ete actif pendant au moins 60 jours. Cette definition est validee par l'equipe Risk et Finance.

Churn mensuel observe : 1.8% (annualise : ~20%). Cout : 500 000 x 20% = 100 000 clients perdus/an. Revenue moyen perdu par client churned : 65 EUR/an (interchange, premium, interets). Impact : 6.5M EUR/an.

### Feature Engineering

```python
# Features calculees sur fenetre glissante 90 jours avant snapshot
CHURN_FEATURES = {
    # Volume transactionnel (signal le plus fort)
    'transactions_count_90d':      'nb transactions totales',
    'transactions_count_trend':    'ratio nb tx (45 derniers j / 45 premiers j)',
    'unique_merchants_90d':        'nb marchands distincts',
    'avg_transaction_amount':      'montant moyen par transaction',
    'monthly_spend_vs_3m_avg':     'depenses dernier mois vs moyenne 3 mois',

    # Produits actives
    'nb_products_active':          'nb produits utilises (carte, epargne, assurance...)',
    'has_premium_subscription':    'abonne au plan premium (binaire)',
    'uses_savings':                'utilise le produit epargne (binaire)',
    'uses_payments':               'virement/paiement recurrent (binaire)',

    # Engagement applicatif
    'app_opens_30d':               'ouvertures app sur 30 jours',
    'app_opens_trend':             'tendance ouvertures app (dernier mois vs precedent)',
    'days_since_last_app_open':    'jours depuis derniere ouverture',
    'push_notif_opt_in':           'notifications push activees (binaire)',

    # Financier
    'avg_balance_90d':             'solde moyen compte principal',
    'min_balance_30d':             'solde minimum (signal de detresse)',
    'overdraft_incidents_90d':     'nb incidents de decouvert',
    'salary_credited':             'salaire credit regulier (binaire)',
}
```

### Training du Modele

```python
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_recall_curve
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Chargement donnees historiques labellisees
df = pd.read_parquet('churn_training_dataset.parquet')

# Split chronologique strict
CUTOFF_DATE = '2023-09-01'
train = df[df['snapshot_date'] <  CUTOFF_DATE]
test  = df[df['snapshot_date'] >= CUTOFF_DATE]

X_train = train[list(CHURN_FEATURES.keys())].fillna(-1)
y_train = train['churned_90d']
X_test  = test[list(CHURN_FEATURES.keys())].fillna(-1)
y_test  = test['churned_90d']

# Gestion du desequilibre de classes (churn = 1.8% mensuel → rare)
# scale_pos_weight : ratio negatifs/positifs
pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

model = GradientBoostingClassifier(
    n_estimators    = 500,
    max_depth       = 4,
    learning_rate   = 0.05,
    subsample       = 0.8,
    min_samples_leaf = 50,
    random_state    = 42
)
model.fit(X_train, y_train, sample_weight=np.where(y_train == 1, pos_weight, 1))

# Evaluation
y_proba = model.predict_proba(X_test)[:, 1]
auc     = roc_auc_score(y_test, y_proba)
print(f"AUC-ROC : {auc:.3f}")  # → 0.84

# Courbe precision-recall pour choisir le seuil optimal
precision, recall, thresholds = precision_recall_curve(y_test, y_proba)
f1_scores = 2 * precision * recall / (precision + recall + 1e-9)
best_idx   = np.argmax(f1_scores)
best_threshold = thresholds[best_idx]
print(f"Seuil optimal (F1 max) : {best_threshold:.3f}")
print(f"  Precision : {precision[best_idx]:.1%}")
print(f"  Recall    : {recall[best_idx]:.1%}")
# Precision : 65% | Recall : 71%
```

### Choix du Seuil — Precision vs Recall

Le choix du seuil est une decision metier, pas uniquement statistique. Pour cette neobanque :

**Cout d'un faux positif (client non-churned identifie comme churned) :** sur-contact du client avec une offre retention. Cout unitaire : ~3 EUR (SMS + offre cashback). Risque : agacer un client satisfait.

**Cout d'un faux negatif (churned non detecte) :** perte du client. Revenue annuel perdu : 65 EUR. Plus difficile et couteux a recuperer.

Avec un ratio cout(FN) / cout(FP) = 65 / 3 = 21.7, il est rationnel d'abaisser le seuil pour maximiser le recall (detecter plus de churns, au prix de plus de faux positifs).

```python
# Analyse de sensibilite au seuil
results = []
for threshold in np.arange(0.1, 0.9, 0.05):
    y_pred = (y_proba >= threshold).astype(int)
    TP = ((y_pred == 1) & (y_test == 1)).sum()
    FP = ((y_pred == 1) & (y_test == 0)).sum()
    FN = ((y_pred == 0) & (y_test == 1)).sum()

    cost_fp = FP * 3    # EUR par faux positif
    saved   = TP * 65   # EUR par vrai positif (revenue sauve)
    net_roi = saved - cost_fp

    results.append({
        'threshold': threshold,
        'recall':    TP / (TP + FN + 1e-9),
        'precision': TP / (TP + FP + 1e-9),
        'net_roi':   net_roi
    })

results_df = pd.DataFrame(results)
optimal = results_df.loc[results_df['net_roi'].idxmax()]
print(f"Seuil optimal ROI : {optimal['threshold']:.2f}")
print(f"  Recall    : {optimal['recall']:.1%}")
print(f"  Precision : {optimal['precision']:.1%}")
print(f"  Net ROI   : {optimal['net_roi']:,.0f} EUR")
```

**Seuil retenu : 0.35** (recall 71%, precision 65%). A ce seuil, sur 500 000 clients :
- Vrais positifs identifies (churns detectes) : ~6 400 / mois
- Faux positifs (sur-contacts) : ~3 500 / mois
- Faux negatifs (churns non detectes) : ~2 600 / mois

### Deploy en Production — Scoring Batch Hebdomadaire

```python
# Pipeline de scoring batch (execute chaque lundi matin)
import pandas as pd
import joblib
from datetime import datetime

def weekly_churn_scoring():
    """
    Calcule les scores de churn pour tous les clients actifs.
    Publie les resultats dans le CRM et Snowflake.
    """
    snapshot_date = datetime.today().strftime('%Y-%m-%d')

    # 1. Extraction des features (depuis Snowflake via SQLAlchemy)
    features = extract_churn_features(snapshot_date=snapshot_date)

    # 2. Chargement du modele depuis le registre (MLflow)
    model = joblib.load('churn_model_v3.pkl')

    # 3. Scoring
    X = features[list(CHURN_FEATURES.keys())].fillna(-1)
    features['churn_score']      = model.predict_proba(X)[:, 1].round(4)
    features['churn_risk_label'] = pd.cut(
        features['churn_score'],
        bins   = [0, 0.2, 0.4, 1.01],
        labels = ['Low', 'Medium', 'High']
    )

    # 4. Top 10% risque → campagne retention
    top_risk = features.nlargest(int(len(features) * 0.10), 'churn_score')

    # 5. Ecriture dans Snowflake (table churn_scores)
    features.to_sql('churn_scores', con=db_engine, if_exists='replace', index=False)

    # 6. Push des segments dans le CRM via API
    push_segments_to_crm(top_risk, segment_name='Churn_Risk_High')

    print(f"[{snapshot_date}] Scoring termine : {len(features):,} clients scored")
    print(f"  High Risk (top 10%) : {len(top_risk):,} clients")
    return features

weekly_churn_scoring()
```

### Campagnes Retention Ciblees

**Top 10% risque churn (High Risk) :** sequence de 3 touchpoints sur 2 semaines.
- J0 : push notification personnalisee avec avantage concret ("Debloquez 3 mois de Metal offerts")
- J7 : email avec recapitulatif des benefices utilises et de ceux non encore actives
- J14 : SMS si toujours inactif ("Votre compte est pret pour votre prochaine utilisation")

Pas de contact pour Medium et Low Risk — contenu standard dans l'application.

### Resultats Apres 12 Mois en Production

| Metrique | Avant | Apres 12 mois |
|----------|-------|---------------|
| Churn mensuel | 1.8% | 1.53% (-15%) |
| Retention rate | 78.4% | 81.6% (+4.2pts) |
| Cout campagnes retention | 180K EUR/an (blast) | 147K EUR/an (-18%) |
| Revenue predit sauve | - | 6.5M EUR/an |
| Clients re-engages / mois | non mesure | 4 200 en moyenne |

**ROI du projet :**
- Cout developpement + infrastructure (12 mois) : 280 000 EUR
- Revenue additionnel retenu : 6 500 000 EUR/an
- ROI : 23x sur la premiere annee

### Lesson Principale

Le seuil optimal entre precision et recall n'est pas 0.5 — il est determine par le ratio des couts metier. Pour cette neobanque, un faux positif coute 3 EUR et un faux negatif coute 65 EUR : le seuil rationnel est donc bien en dessous de 0.5. Systematiser cette analyse de sensibilite au seuil avec les equipes metier avant le deploiement. Un modele AUC 0.84 deploye avec le bon seuil surpasse un modele AUC 0.90 deploye avec le seuil par defaut de 0.5.

La securite du deploiement passe par le monitoring continu : tracker le data drift (evolution de la distribution des features) et l'AUC en production chaque semaine. Un retrainement mensuel est necessaire pour conserver la performance dans un contexte client qui evolue.
