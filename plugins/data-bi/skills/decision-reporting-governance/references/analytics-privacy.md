# Analytics & Privacy — Descriptive to Prescriptive Analytics, Statistical Analysis & RGPD Compliance

## Overview

Ce document de reference couvre le spectre complet de l'analytics (descriptive, diagnostique, predictive, prescriptive), les methodes d'analyse statistique appliquees au BI, ainsi que la conformite RGPD/GDPR : cartographie des traitements, classification des donnees, techniques d'anonymisation et politiques de retention. Utiliser ce guide pour choisir les bonnes methodes analytiques et garantir la conformite reglementaire des systemes de donnees.

This reference document covers the full analytics spectrum (descriptive, diagnostic, predictive, prescriptive), statistical analysis methods applied to BI, and RGPD/GDPR compliance: processing mapping, data classification, anonymization techniques, and retention policies. Use this guide to select the right analytical methods and ensure regulatory compliance of data systems.

---

## The Four Types of Analytics

### Descriptive Analytics — "Que s'est-il passe ?" / "What happened?"

L'analytics descriptive resume les donnees historiques pour comprendre les evenements passes. C'est la fondation de toute demarche analytique.

#### Methodes et livrables / Methods and Deliverables

- **Dashboards de suivi** : KPIs avec tendances, comparaisons temporelles (MoM, YoY), decompositions par dimension.
- **Rapports standard** : rapports periodiques (quotidien, hebdomadaire, mensuel) avec les metriques cles.
- **Aggregations et distributions** : moyennes, medianes, percentiles, frequences, histogrammes.
- **Segmentations** : repartition par cohorte, par segment, par canal, par region.

#### Statistiques descriptives essentielles / Essential Descriptive Statistics

| Mesure | Formule / Methode | Usage |
|---|---|---|
| **Moyenne (Mean)** | Sum / Count | Tendance centrale, sensible aux outliers |
| **Mediane** | Valeur centrale ordonnee | Tendance centrale robuste aux outliers |
| **Mode** | Valeur la plus frequente | Categorie dominante |
| **Ecart-type (Std Dev)** | sqrt(variance) | Dispersion autour de la moyenne |
| **Percentiles (P50, P90, P99)** | Valeur en dessous de laquelle tombe X% des observations | Performance (latency p99), revenus |
| **IQR (Interquartile Range)** | Q3 - Q1 | Detection d'outliers (< Q1-1.5*IQR ou > Q3+1.5*IQR) |
| **Coefficient de variation** | Std Dev / Mean | Comparaison de dispersion entre metriques differentes |

#### Exemples d'implementation SQL / SQL Implementation Examples

```sql
-- Statistiques descriptives pour les commandes
SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value,
    MEDIAN(total_amount) AS median_order_value,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY total_amount) AS p90_order_value,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY total_amount) AS p99_order_value,
    STDDEV(total_amount) AS stddev_order_value,
    MIN(total_amount) AS min_order_value,
    MAX(total_amount) AS max_order_value
FROM fct_orders
WHERE order_date >= DATEADD('month', -12, CURRENT_DATE)
GROUP BY 1
ORDER BY 1;

-- Analyse de cohorte (retention)
WITH cohort AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) AS cohort_month
    FROM fct_orders
    GROUP BY 1
),
activity AS (
    SELECT
        c.cohort_month,
        DATEDIFF('month', c.cohort_month, DATE_TRUNC('month', o.order_date)) AS months_since_first,
        COUNT(DISTINCT o.customer_id) AS active_customers
    FROM fct_orders o
    JOIN cohort c ON o.customer_id = c.customer_id
    GROUP BY 1, 2
)
SELECT
    cohort_month,
    months_since_first,
    active_customers,
    active_customers * 100.0 / FIRST_VALUE(active_customers) OVER (
        PARTITION BY cohort_month ORDER BY months_since_first
    ) AS retention_rate
FROM activity
ORDER BY 1, 2;
```

### Diagnostic Analytics — "Pourquoi ?" / "Why did it happen?"

L'analytics diagnostique va au-dela de la description pour comprendre les causes. Elle repond a "pourquoi le chiffre d'affaires a-t-il baisse de 15% ?" plutot que simplement constater la baisse.

#### Methodes / Methods

- **Drill-down analysis** : descendre dans la hierarchie dimensionnelle (region -> pays -> ville -> magasin) pour localiser l'anomalie.
- **Contribution analysis** : identifier quelle dimension ou quel segment explique le plus la variation. Decomposer le delta en contributions par segment.
- **Correlation analysis** : mesurer la relation lineaire entre deux metriques (coefficient de Pearson, Spearman). Attention : correlation n'est pas causalite.
- **Root cause analysis** : technique structuree (5 Whys, Ishikawa/fishbone diagram) pour remonter a la cause racine d'un probleme.
- **Anomaly detection** : identifier les points de donnees qui deviennent significativement hors norme (z-score > 3, IQR outliers, algorithmes ML comme Isolation Forest).

#### Contribution Analysis — Implementation

```sql
-- Decomposition de la variation du CA par segment
WITH current_period AS (
    SELECT segment, SUM(total_amount) AS revenue
    FROM fct_orders o
    JOIN dim_customer c ON o.customer_key = c.customer_key AND c.is_current
    WHERE order_date BETWEEN '2026-01-01' AND '2026-01-31'
    GROUP BY 1
),
prior_period AS (
    SELECT segment, SUM(total_amount) AS revenue
    FROM fct_orders o
    JOIN dim_customer c ON o.customer_key = c.customer_key AND c.is_current
    WHERE order_date BETWEEN '2025-01-01' AND '2025-01-31'
    GROUP BY 1
)
SELECT
    COALESCE(c.segment, p.segment) AS segment,
    COALESCE(p.revenue, 0) AS prior_revenue,
    COALESCE(c.revenue, 0) AS current_revenue,
    COALESCE(c.revenue, 0) - COALESCE(p.revenue, 0) AS absolute_change,
    ROUND((COALESCE(c.revenue, 0) - COALESCE(p.revenue, 0)) * 100.0
        / NULLIF(SUM(COALESCE(p.revenue, 0)) OVER (), 0), 2) AS contribution_to_total_change_pct
FROM current_period c
FULL OUTER JOIN prior_period p ON c.segment = p.segment
ORDER BY ABS(COALESCE(c.revenue, 0) - COALESCE(p.revenue, 0)) DESC;
```

### Predictive Analytics — "Que va-t-il se passer ?" / "What will happen?"

L'analytics predictive utilise les donnees historiques et des modeles statistiques ou de machine learning pour anticiper les evenements futurs.

#### Methodes de prevision / Forecasting Methods

| Methode | Description | Complexite | Cas d'usage |
|---|---|---|---|
| **Moving averages** | Moyenne mobile simple ou ponderee | Faible | Lissage de tendance, baseline rapide |
| **Exponential smoothing** | Modeles de lissage exponentiel (Holt-Winters) | Moyenne | Series temporelles avec saisonnalite |
| **ARIMA/SARIMA** | Modeles auto-regressifs integres | Moyenne | Series temporelles stationnaires |
| **Prophet (Meta)** | Modele additif avec saisonnalite + tendance + vacances | Moyenne | Forecasting business, facile a configurer |
| **XGBoost / LightGBM** | Gradient boosting sur features temporelles | Elevee | Prevision avec features externes |
| **Deep Learning (LSTM, Transformer)** | Reseaux de neurones pour series temporelles | Tres elevee | Tres grands volumes, patterns complexes |

#### Cas d'usage predictif en BI / Predictive BI Use Cases

- **Revenue forecasting** : projeter le chiffre d'affaires sur les 3-12 prochains mois. Integrer dans les dashboards financiers avec intervalles de confiance.
- **Churn prediction** : identifier les clients a risque de depart. Combiner avec des actions de retention (offres, outreach).
- **Demand forecasting** : prevoir la demande produit pour optimiser les stocks et la logistique.
- **Anomaly forecasting** : detecter les deviations par rapport aux previsions (depense anormalement elevee, trafic inhabituel).

#### Integration du predictif dans les dashboards / Integrating Predictions into Dashboards

```python
# Exemple de prevision avec Prophet pour integration dans dbt/BI
from prophet import Prophet
import pandas as pd

# Preparer les donnees au format Prophet
df = pd.read_sql("""
    SELECT
        DATE_TRUNC('day', order_date) AS ds,
        SUM(total_amount) AS y
    FROM analytics.fct_orders
    WHERE order_date >= DATEADD('year', -2, CURRENT_DATE)
    GROUP BY 1
    ORDER BY 1
""", connection)

# Entrainer le modele
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    changepoint_prior_scale=0.05,  # Regularisation
    interval_width=0.95             # Intervalle de confiance a 95%
)
model.fit(df)

# Generer les previsions sur 90 jours
future = model.make_future_dataframe(periods=90)
forecast = model.predict(future)

# Colonnes cles : ds, yhat (prediction), yhat_lower, yhat_upper (intervalles)
# Ecrire dans le data warehouse pour consommation BI
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_sql(
    'fct_revenue_forecast', engine, schema='analytics', if_exists='replace'
)
```

### Prescriptive Analytics — "Que faire ?" / "What should we do?"

L'analytics prescriptive recommande des actions concretes basees sur les donnees et les modeles predictifs. C'est le niveau le plus avance de maturite analytique.

#### Methodes / Methods

- **Optimization** : optimisation lineaire, programmation lineaire en nombres entiers pour les decisions d'allocation (budget, inventaire, planning).
- **Simulation (Monte Carlo)** : simuler des milliers de scenarios pour evaluer les distributions de resultats possibles et quantifier les risques.
- **A/B testing & experimentation** : tester des hypotheses avec des experiences controlees. Calculer la significativite statistique (p-value < 0.05, puissance > 0.8).
- **Recommender systems** : recommander des produits, des contenus ou des actions basees sur les comportements passes et les similarites.
- **Decision automation** : automatiser les decisions operationnelles basees sur des regles et des modeles (pricing dynamique, allocation automatique de leads, ajustement de stock).

#### Evaluation de la significativite statistique / Statistical Significance Evaluation

```python
# Test de significativite pour un A/B test
from scipy import stats
import numpy as np

# Donnees du test A/B
control_conversions = 120
control_total = 5000
variant_conversions = 145
variant_total = 5000

# Taux de conversion
control_rate = control_conversions / control_total  # 2.4%
variant_rate = variant_conversions / variant_total    # 2.9%

# Test chi-carre
contingency_table = np.array([
    [control_conversions, control_total - control_conversions],
    [variant_conversions, variant_total - variant_conversions]
])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)

# Interpretation
lift = (variant_rate - control_rate) / control_rate * 100
print(f"Lift: {lift:.1f}%")           # +20.8%
print(f"p-value: {p_value:.4f}")       # < 0.05 = significatif
print(f"Significant: {p_value < 0.05}")

# Calcul de la taille d'echantillon necessaire (power analysis)
from statsmodels.stats.power import NormalIndPower
analysis = NormalIndPower()
sample_size = analysis.solve_power(
    effect_size=0.1,   # Effet minimum detectable
    power=0.8,         # Puissance souhaitee (80%)
    alpha=0.05,        # Seuil de significativite (5%)
    ratio=1            # Ratio control/variant
)
print(f"Required sample size per group: {int(sample_size)}")
```

---

## Statistical Analysis for BI

### Tests statistiques essentiels / Essential Statistical Tests

| Test | Quand l'utiliser | Hypotheses |
|---|---|---|
| **t-test (Student)** | Comparer les moyennes de 2 groupes | Distribution normale, variances similaires |
| **Welch's t-test** | Comparer les moyennes de 2 groupes, variances inegales | Distribution normale |
| **Mann-Whitney U** | Comparer 2 groupes (non parametrique) | Pas de normalite requise |
| **ANOVA** | Comparer les moyennes de 3+ groupes | Distribution normale, homoscedasticite |
| **Chi-carre** | Tester l'independance de variables categoriques | Effectifs attendus > 5 |
| **Correlation de Pearson** | Mesurer la relation lineaire entre 2 variables continues | Linearite, normalite |
| **Correlation de Spearman** | Mesurer la relation monotone (non lineaire) | Pas de normalite requise |
| **Regression lineaire** | Modeliser la relation entre une variable dependante et des predicteurs | Linearite, independance, normalite des residus |

### Pieges statistiques en BI / Statistical Pitfalls in BI

- **Simpson's Paradox** : une tendance presente dans plusieurs groupes peut s'inverser quand les groupes sont combines. Toujours verifier les analyses a differents niveaux d'agregation.
- **Survivorship Bias** : analyser uniquement les entites qui ont "survecu" (clients actifs, produits en vente) et ignorer celles qui ont disparu. Inclure les entites disparues dans les analyses.
- **Cherry-picking de periodes** : choisir une periode de reference qui valide un recit predetermine. Toujours utiliser des periodes de reference consistantes et documentees.
- **Confondre correlation et causalite** : une correlation forte entre deux variables n'implique pas une relation causale. Utiliser des methodes experimentales (A/B tests) ou des techniques causales (diff-in-diff, regression discontinuity) pour etablir la causalite.
- **Multiple comparisons problem** : tester plusieurs hypotheses augmente le risque de faux positifs. Appliquer la correction de Bonferroni ou le FDR (False Discovery Rate) quand on effectue des tests multiples.
- **Sample size insuffisant** : tirer des conclusions a partir d'echantillons trop petits. Toujours effectuer un power analysis avant de lancer un test.

---

## RGPD / GDPR — Data Privacy & Compliance

### Principes fondamentaux du RGPD / Core GDPR Principles

Le RGPD (Reglement General sur la Protection des Donnees) s'applique a tout traitement de donnees personnelles de residents de l'UE. Ses 7 principes fondamentaux :

1. **Licite, loyal et transparent** : chaque traitement doit reposer sur une base legale (consentement, contrat, interet legitime, obligation legale, mission d'interet public, interets vitaux) et etre communique de maniere transparente.
2. **Limitation des finalites** : les donnees sont collectees pour des finalites determinees, explicites et legitimes.
3. **Minimisation** : ne collecter que les donnees strictement necessaires a la finalite.
4. **Exactitude** : maintenir les donnees a jour et rectifier les inexactitudes.
5. **Limitation de la conservation** : ne pas conserver les donnees au-dela de ce qui est necessaire.
6. **Integrite et confidentialite** : proteger les donnees contre les acces non autorises, la perte et la destruction.
7. **Responsabilite (Accountability)** : le responsable du traitement doit pouvoir demontrer sa conformite.

### Cartographie des traitements (Article 30) / Processing Mapping

Maintenir un registre des traitements documentant pour chaque traitement :

| Champ | Description | Exemple |
|---|---|---|
| **Nom du traitement** | Description du traitement | Analyse des ventes par segment client |
| **Finalite** | Objectif du traitement | Optimisation de la strategie commerciale |
| **Base legale** | Fondement juridique | Interet legitime (analyse interne) |
| **Categories de donnees** | Types de donnees traitees | Nom, email, historique d'achat, segment |
| **Categories de personnes** | Personnes concernees | Clients B2C et B2B |
| **Destinataires** | Qui accede aux donnees | Equipe commerciale, equipe data |
| **Transferts hors UE** | Transferts internationaux | AWS us-east-1 (Clauses Contractuelles Types) |
| **Duree de conservation** | Duree de retention | 3 ans apres la derniere transaction |
| **Mesures de securite** | Protections appliquees | Chiffrement, RLS, anonymisation dans les rapports |

### Data Classification

Classifier chaque champ de donnees selon son niveau de sensibilite. Cette classification guide les regles d'acces, de chiffrement et d'anonymisation.

| Niveau | Description | Exemples | Mesures requises |
|---|---|---|---|
| **Public** | Aucune restriction | Nom de l'entreprise, catalogue produit | Aucune mesure speciale |
| **Internal** | Usage interne uniquement | CA global, nombre d'employes | Acces restreint aux employes |
| **Confidential** | Acces limite aux personnes autorisees | Donnees clients (nom, email), salaires | Chiffrement, RLS, audit trail |
| **Restricted** | Acces strictement controle | Donnees de sante, numero de securite sociale, carte bancaire | Chiffrement fort, masking, acces nominatif, audit obligatoire |

#### Implementation de la classification dans le catalogue / Catalog Classification Implementation

```yaml
# DataHub / OpenMetadata tag taxonomy
classification:
  - name: public
    description: "No restriction on access or usage"
    color: green
  - name: internal
    description: "Internal use only, not for external sharing"
    color: blue
  - name: confidential
    description: "Limited access, contains PII or business-sensitive data"
    color: orange
    requires:
      - encryption_at_rest
      - row_level_security
      - audit_logging
  - name: restricted
    description: "Strictly controlled access, highly sensitive data"
    color: red
    requires:
      - encryption_at_rest
      - encryption_in_transit
      - column_masking
      - nominative_access
      - mandatory_audit
      - dpia_required
```

### PII Detection and Tagging

Automatiser la detection de donnees personnelles dans les pipelines :

```python
# Patterns de detection PII (pour integration dans Great Expectations ou custom scanner)
PII_PATTERNS = {
    'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    'phone_fr': r'(?:\+33|0)[1-9](?:[\s.-]?\d{2}){4}',
    'phone_international': r'\+\d{1,3}[\s.-]?\d{4,14}',
    'iban': r'[A-Z]{2}\d{2}[\s]?[\dA-Z]{4}[\s]?(?:[\dA-Z]{4}[\s]?){2,7}[\dA-Z]{1,4}',
    'ssn_fr': r'[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}',
    'credit_card': r'\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}',
    'ip_address': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
    'date_of_birth': r'\d{2}/\d{2}/\d{4}',
}

# Colonnes heuristiquement suspectes (par nom)
PII_COLUMN_NAMES = [
    'email', 'mail', 'courriel',
    'phone', 'telephone', 'tel', 'mobile',
    'name', 'nom', 'prenom', 'first_name', 'last_name',
    'address', 'adresse', 'street', 'rue',
    'ssn', 'nir', 'social_security',
    'date_of_birth', 'dob', 'date_naissance',
    'ip_address', 'ip',
    'credit_card', 'card_number', 'carte',
    'iban', 'account_number',
    'passport', 'id_card', 'carte_identite',
]
```

---

## Anonymization & Pseudonymization Techniques

### Distinction anonymisation vs pseudonymisation / Anonymization vs Pseudonymization

| Critere | Anonymisation | Pseudonymisation |
|---|---|---|
| **Reversibilite** | Irreversible | Reversible (avec la cle) |
| **Statut RGPD** | Donnees non personnelles (hors scope RGPD) | Donnees personnelles (dans le scope RGPD) |
| **Utilite analytique** | Reduite (perte d'information) | Elevee (analyses possibles avec la cle) |
| **Cas d'usage** | Publication, open data, environnements de test | Analytics internes, data warehouse, data science |

### Techniques d'anonymisation / Anonymization Techniques

| Technique | Description | Utilite preservee | Risque de reidentification |
|---|---|---|---|
| **Suppression** | Supprimer le champ | Nulle pour ce champ | Nul |
| **Generalisation** | Reduire la precision (age exact -> tranche d'age, CP -> departement) | Analyses par groupe | Faible si k-anonymite respectee |
| **Agregation** | Remplacer par des statistiques (moyenne, somme, count) | Tendances uniquement | Tres faible |
| **Noise addition** | Ajouter du bruit statistique aux valeurs | Distributions preservees | Faible |
| **Data swapping** | Permuter les valeurs entre records | Relations inter-champs rompues | Moyen |
| **k-anonymite** | Chaque combinaison de quasi-identifiants apparait au moins k fois | Analyses cross-dimensionnelles | Controle (k >= 5 recommande) |
| **l-diversite** | Chaque classe d'equivalence contient au moins l valeurs distinctes pour l'attribut sensible | Attributs sensibles proteges | Controle |
| **Differential privacy** | Ajout de bruit calibre garantissant qu'un individu n'impacte pas significativement le resultat | Statistiques agregees | Tres faible (garanti mathematiquement) |

### Pseudonymisation — Implementation

```sql
-- Pseudonymisation par hashing (SHA-256 + salt)
-- Attention : le hash seul sans salt est vulnerable aux rainbow tables

-- Dans dbt, creer un macro de pseudonymisation
{% macro pseudonymize(column_name, salt) %}
    SHA2(CONCAT({{ column_name }}, '{{ salt }}'), 256)
{% endmacro %}

-- Usage dans un modele
SELECT
    {{ pseudonymize('email', env_var('PSEUDONYMIZATION_SALT')) }} AS email_pseudo,
    {{ pseudonymize('customer_id', env_var('PSEUDONYMIZATION_SALT')) }} AS customer_pseudo,
    -- Champs non PII en clair
    order_date,
    order_amount,
    product_category,
    region
FROM {{ ref('stg_orders') }}
```

### Techniques de masking dynamique / Dynamic Data Masking

```sql
-- Snowflake : masking policy
CREATE OR REPLACE MASKING POLICY email_mask AS (val STRING)
RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('DATA_ENGINEER', 'DATA_STEWARD')
            THEN val
        WHEN CURRENT_ROLE() IN ('ANALYST')
            THEN REGEXP_REPLACE(val, '.+@', '***@')   -- ***@domain.com
        ELSE '***MASKED***'
    END;

ALTER TABLE dim_customer MODIFY COLUMN email SET MASKING POLICY email_mask;

-- BigQuery : column-level access control
-- Utiliser les policy tags pour restreindre l'acces aux colonnes PII
-- Les policy tags sont geres dans Data Catalog et appliques aux colonnes

-- Redshift : dynamic data masking (preview 2025+)
CREATE MASKING POLICY partial_email
    WITH (email VARCHAR)
    USING (
        CASE
            WHEN HAS_ROLE('full_access') THEN email
            ELSE CONCAT('***@', SPLIT_PART(email, '@', 2))
        END
    );
```

---

## Retention Policies

### Definition des politiques de retention / Retention Policy Definition

Definir pour chaque categorie de donnees une duree de conservation maximale et un processus de suppression ou d'archivage.

| Categorie de donnees | Duree de retention | Base legale | Action a expiration |
|---|---|---|---|
| **Donnees transactionnelles** | 10 ans (obligation comptable) | Obligation legale (Code de commerce) | Archivage froid |
| **Donnees clients actifs** | Duree de la relation + 3 ans | Execution du contrat + interet legitime | Anonymisation ou suppression |
| **Donnees prospects** | 3 ans apres dernier contact | Interet legitime | Suppression |
| **Logs applicatifs (avec PII)** | 12 mois | Interet legitime (securite) | Suppression |
| **Logs anonymises** | 5 ans | Interet legitime (analytics) | Archivage ou suppression |
| **Donnees de navigation (cookies)** | 13 mois (CNIL) | Consentement | Suppression |
| **Donnees de paie** | 5 ans (Code du travail) | Obligation legale | Archivage froid |
| **Donnees de sante** | 20 ans | Obligation legale | Archivage securise |

### Implementation technique / Technical Implementation

```sql
-- Processus de retention automatise dans dbt + Airflow

-- 1. Vue de detection des donnees a expiration
CREATE VIEW data_retention.expired_records AS
SELECT
    'dim_customer' AS table_name,
    customer_id,
    'Prospect sans contact depuis 3 ans' AS reason,
    last_contact_date
FROM analytics.dim_customer
WHERE customer_type = 'prospect'
  AND last_contact_date < DATEADD('year', -3, CURRENT_DATE)

UNION ALL

SELECT
    'stg_app_logs' AS table_name,
    log_id AS record_id,
    'Logs applicatifs de plus de 12 mois' AS reason,
    log_timestamp AS relevant_date
FROM raw.stg_app_logs
WHERE log_timestamp < DATEADD('month', -12, CURRENT_DATE);

-- 2. Processus de suppression (execute par Airflow avec approbation)
-- Ne jamais supprimer sans log d'audit
INSERT INTO data_retention.deletion_audit
    (table_name, record_count, deletion_reason, deleted_by, deleted_at)
SELECT
    table_name,
    COUNT(*) AS record_count,
    reason AS deletion_reason,
    CURRENT_USER() AS deleted_by,
    CURRENT_TIMESTAMP() AS deleted_at
FROM data_retention.expired_records
GROUP BY table_name, reason;

-- 3. Suppression effective
DELETE FROM analytics.dim_customer
WHERE customer_id IN (
    SELECT customer_id FROM data_retention.expired_records
    WHERE table_name = 'dim_customer'
);
```

### Droit a l'effacement (Article 17) / Right to Erasure

Implementer le processus de traitement des demandes de suppression (droit a l'oubli) :

1. **Reception** : recevoir la demande via le DPO ou un formulaire dedie. Verifier l'identite du demandeur.
2. **Cartographie** : identifier toutes les tables et systemes contenant les donnees de la personne. Utiliser la lineage du data catalog pour tracer les propagations.
3. **Evaluation** : verifier si une obligation legale empeche la suppression (obligation comptable, litige en cours). Documenter la decision.
4. **Execution** : supprimer ou anonymiser les donnees dans tous les systemes (source, data warehouse, backups, caches, BI tools). Propager la suppression via les pipelines.
5. **Confirmation** : confirmer au demandeur dans le delai de 30 jours. Logger l'action dans le registre d'audit.
6. **Verification** : verifier que les donnees ont ete effectivement supprimees dans tous les systemes.

### DPIA (Data Protection Impact Assessment)

Realiser une DPIA avant tout traitement presentant un risque eleve pour les droits et libertes des personnes. Les cas necessitant une DPIA incluent :

- Evaluation systematique et extensive de personnes (scoring, profiling).
- Traitement a grande echelle de donnees sensibles (sante, biometrie, opinions politiques).
- Surveillance systematique a grande echelle de zones publiques.
- Croisement de jeux de donnees (data matching, entity resolution).
- Utilisation de nouvelles technologies (IA, biometrie, IoT).

Structure de la DPIA :

1. **Description du traitement** : nature, finalite, portee, contexte.
2. **Evaluation de la necessite et de la proportionnalite** : le traitement est-il necessaire ? Les donnees sont-elles minimisees ?
3. **Evaluation des risques** : identifier les risques pour les droits des personnes (discrimination, atteinte a la vie privee, perte financiere).
4. **Mesures d'attenuation** : definir les mesures techniques et organisationnelles pour reduire les risques (anonymisation, masking, RLS, formation, audits).
5. **Consultation du DPO** : obtenir l'avis du DPO avant de lancer le traitement.
6. **Consultation de la CNIL** : si les risques residuels restent eleves malgre les mesures d'attenuation, consulter l'autorite de controle.
