# Model Cards & Documentation des Systemes IA

## Vue d'Ensemble

Les model cards (Mitchell et al., 2019, Google) sont des documents standardises accompagnant chaque modele IA deploye. Initialement volontaires, elles deviennent une obligation de fait pour les IA a risque eleve sous l'EU AI Act (Article 11 — documentation technique) et une pratique attendue pour tout systeme IA impactant des personnes. Leur complement, les Datasheets for Datasets (Gebru et al., 2021), documente les donnees d'entrainement.

---

## Model Cards — Structure et Contenu

### Section 1 — Informations Generales

```markdown
## Informations Generales du Modele

| Champ | Valeur |
|---|---|
| **Nom** | CustomerChurn-LightGBM-v2.3 |
| **Version** | 2.3.0 |
| **Date de creation** | 2025-03-15 |
| **Date de derniere mise a jour** | 2025-09-01 |
| **Type de modele** | Classification binaire (gradient boosting) |
| **Architecture** | LightGBM 4.3.0, 500 estimateurs, profondeur max 7 |
| **Framework** | Python 3.11, scikit-learn 1.4, LightGBM 4.3 |
| **Taille** | 12.3 MB (modele serialise) |
| **Licence** | Proprietary — usage interne uniquement |
| **Contact** | ml-team@company.com |
| **DPO contact** | dpo@company.com |
```

### Section 2 — Utilisation Prevue et Limitations

```markdown
## Utilisation Prevue

**Cas d'usage principal** :
Prediction du risque de churn des clients B2B dans les 30 prochains jours.
Le score est utilise par l'equipe Customer Success pour prioriser les appels proactifs.

**Utilisateurs prevus** :
- Equipe Customer Success (interpretation des scores via le CRM)
- Data Scientists (maintenance et retrainement)
- Managers CS (dashboard strategique)

**Modalites d'utilisation recommandees** :
- Score > 0.7 : contact proactif prioritaire
- Score 0.4-0.7 : contact a discreation du CS manager
- Score < 0.4 : pas d'action specifique necessaire

**Utilisations NON prevues (Out of Scope)** :
- Ne pas utiliser pour des decisions de resiliation unilaterale
- Ne pas utiliser comme seul critere pour des decisions commerciales importantes
- Ne pas utiliser pour des clients avec < 3 mois d'historique (performance degradee)
- Ne pas utiliser pour la facturation ou des decisions financieres
- Ne pas utiliser en dehors du perimetre clients B2B (non valide sur B2C)
```

### Section 3 — Donnees d'Entrainement

```markdown
## Donnees d'Entrainement

**Source** : CRM interne (Salesforce) + logs d'utilisation produit (Mixpanel)
**Perimetre temporel** : Janvier 2022 — Decembre 2024 (36 mois)
**Volume** : 145 234 observations (clients x periodes)
**Label** : Churn defini comme non-renouvellement dans les 30 jours suivants

**Repartition classes** :
- Classe 0 (pas de churn) : 94.2% (136 951 obs.)
- Classe 1 (churn) : 5.8% (8 283 obs.)
- Technique d'equilibrage : SMOTE applique sur le train set uniquement

**Biais connus et limitations** :
- Sur-representation des entreprises > 50 salaries (68% du dataset vs 45% du portefeuille)
  → Impact : performance legèrement reduite sur les TPE
- Periode COVID (mars-juin 2020) exclue du training (comportements atypiques)
- Pays hors France representant < 3% des donnees — ne pas utiliser pour des clients majoritairement etrangers
- Donnees de satisfaction (CSAT) manquantes pour 23% des observations

**Donnees personnelles utilisees** :
- Identifiant client (pseudonymise — UUID interne, sans donnee directement identifiable)
- Variables comportementales agregees (pas de donnees individuelles de sessions)
- Variables financieres agregees (MRR, pas de donnees de transaction individuelles)

**Note RGPD** : Le modele est entraine sur des donnees pseudonymisees. La table de correspondance UUID → client_id est stockee dans un systeme separe (acces restreint DPO + Tech Lead uniquement).
```

### Section 4 — Performances du Modele

```markdown
## Performances

**Methodologie de validation** :
- Split temporel (out-of-time) : training sur jan 2022 - aout 2024, test sur sep-dec 2024
- Pas de data leakage verifie par revue de code (audit independant realise le 2025-02-10)

**Metriques globales (test set out-of-time)** :

| Metrique | Valeur | Interpretation |
|---|---|---|
| AUC-ROC | 0.847 | Excellent pouvoir discriminant |
| AUC-PR | 0.724 | Bonne precision en classe positive (desequilibree) |
| Precision @threshold 0.5 | 0.68 | 68% des alertes sont de vrais churners |
| Recall @threshold 0.5 | 0.71 | 71% des churners sont detectes |
| F1 @threshold 0.5 | 0.695 | Equilibre precision/recall |
| Recall @top 20% | 0.64 | 64% des churners dans le top quintile |

**Seuil de decision recommande** : 0.65 (optimise sur le critere metier : maximiser
les churners detectes tout en limitant les faux positifs a < 40%)

**Performances par segment** :

| Segment | AUC | N obs. | Note |
|---|---|---|---|
| PME (< 50 sal.) | 0.791 | 28 431 | Performance reduite (moins de data) |
| ETI (50-500 sal.) | 0.863 | 89 245 | Performance nominale |
| Grandes entreprises (> 500 sal.) | 0.901 | 27 558 | Meilleure performance |
| Clients < 6 mois | 0.712 | 8 432 | Utiliser avec precaution |
| Clients > 3 ans | 0.878 | 67 891 | Tres fiable |

**Stabilite temporelle** :
- PSI (Population Stability Index) mensuel, seuil d'alerte : > 0.2
- AUC-PR suivie mensuellement sur echantillon labelle avec 30j de recul
```

### Section 5 — Evaluation Ethique et Biais

```markdown
## Evaluation Ethique

**Variables sensibles exclues du modele** :
- Taille d'entreprise (proxy potentiel de type d'industrie) → INCLUSE apres test de biais
- Localisation geographique → EXCLUE (proxy potentiel de region)
- Secteur d'activite → INCLUS sous forme d'un ensemble de categories validees

**Tests de biais realises (Fairlearn, 2025-02-15)** :

Tests effectues sur les dimensions : taille entreprise, secteur, anciennete.

| Dimension | Metrique | Valeur max ecart | Seuil alerte | Statut |
|---|---|---|---|---|
| Taille entreprise | Equal Opportunity (TPR) | 7.2% (PME vs ETI) | 10% | OK |
| Secteur d'activite | Demographic Parity | 4.1% (tech vs manufacturing) | 10% | OK |
| Anciennete client | Predictive Parity | 3.8% (< 1an vs > 3 ans) | 10% | OK |

**Interpretation** : Aucun ecart significatif detecte au-dela des seuils d'alerte.
L'ecart TPR PME/ETI est attribue a la sous-representation des PME dans les donnees
d'entrainement, pas a une discrimination algorithmique.

**Re-audit prevu** : Trimestriel (prochain : 2025-12-15)

**Limites de l'evaluation** :
- Les tests de biais couvrent uniquement les biais mesurables sur les donnees disponibles
- Des biais non observes (ex: lien avec le secteur geographique non capture) peuvent exister
- L'equite formelle (metriques statistiques) ne garantit pas l'equite substantielle
```

### Section 6 — Facteurs de Risque et Limitations

```markdown
## Facteurs de Risque et Limitations

**Conditions de degradation de performance** :
- Historique client < 3 mois : AUC significativement plus bas (0.71)
- Clients ayant subi une fusion/acquisition recente : patterns non representatifs
- Periodes de disruption marche (crise, changement reglementaire sectoriel) : drift possible

**Risques d'utilisation incorrecte** :
- Utiliser le score comme seul critere pour une decision commerciale importante
- Ignorer les scores pour des clients connus comme "a risque" par le CS manager
- Comparer les scores entre segments differents (PME vs grandes entreprises)

**Ne pas utiliser si** :
- Le client a des caracteristiques tres differentes de la distribution d'entrainement
  (verifier : anciennete < 2 mois, secteur non represente dans le dataset)
- L'objectif est de predire le churn sur plus de 60 jours (fenetre cible = 30 jours)

**Comportement sur les cas limites** :
- Score = NULL si features critiques manquantes (> 5 features manquantes)
- Score = 0.5 (neutre) si le client est dans l'extreme des distributions
```

### Section 7 — Surveillance et Maintenance

```markdown
## Surveillance en Production

**Monitoring automatique (hebdomadaire)** :
- Distribution des scores (PSI vs distribution de reference du mois de mise en prod)
- Volume de predictions (alerte si < 13 000 ou > 17 000 clients scores)
- Proportion de scores NULL (alerte si > 5%)

**Monitoring de performance (mensuel sur echantillon labelle)** :
- AUC-PR sur les 500 clients les plus recents dont le statut est connu (30j de recul)
- Alerte si AUC-PR < 0.65

**Retrainement** :
- Frequence : mensuel (premier lundi du mois)
- Declencheurs de retrainement urgent : AUC-PR < 0.60, PSI > 0.30, changement
  majeur dans la definition du produit
- Approbation du retrainement : ML Lead + Head of Customer Success

**Responsables** :
- Owner technique : [Nom ML Engineer]
- Owner metier : [Nom Head of CS]
- DPO notification : si changement majeur des donnees utilisees

**Historique des versions** :
| Version | Date | Changements | Raison |
|---|---|---|---|
| 1.0 | 2023-01 | Premiere mise en production | Nouveau modele |
| 2.0 | 2024-03 | Feature engineering majeur, LightGBM | Amelioration performances |
| 2.3 | 2025-03 | Ajout features product usage | Drift detecte |
```

---

## Datasheets for Datasets

### Structure (Gebru et al., 2021)

```markdown
# Datasheet — CustomerChurn-Training-Dataset-v3

## Motivation
- **Pourquoi ce dataset existe** : support du modele de churn prediction
- **Qui l'a cree et finance** : equipe Data, budget centre de cout Data Science
- **Processus de creation** : extraction automatique depuis CRM + product analytics,
  pipeline dbt hebdomadaire

## Composition
- **Contenu** : 145 234 observations client x periode mensuelle
- **Types de donnees** : numerique (MRR, nb connexions), categorique (plan, secteur)
- **Valeurs manquantes** : CSAT manquant pour 23% des obs. (methodologie d'imputation documentee)
- **Sensibilite** : donnees pseudonymisees — pas de donnee personnelle directement identifiable

## Collecte et Preprocessing
- **Source** : CRM Salesforce (contrats) + Mixpanel (usage produit) + Zendesk (support)
- **Periode** : janvier 2022 - decembre 2024
- **Exclusions** : periode COVID mars-juin 2020, clients < 1 mois d'anciennete
- **Preprocessing** : normalisation, traitement des outliers (winsorization a 99e percentile),
  encodage des variables categoriques, SMOTE sur train set

## Utilisations Recommandees
- Entrainement et evaluation de modeles de churn prediction B2B SaaS
- Analyse exploratoire des facteurs de retention client

## Utilisations Deconseillees
- Ne pas utiliser pour entrainer des modeles de credit scoring ou de notation financiere
- Ne pas utiliser pour des populations significativement differentes (ex: B2C, autre secteur)
- Ne pas croiser avec des donnees externes sans validation RGPD

## Distribution
- Acces : equipe Data uniquement (acces controle dans le data catalog)
- Pas de partage externe sans validation DPO
- Licence : proprietary, usage interne

## Maintenance
- Mise a jour : mensuelle (pipeline automatique)
- Versioning : gere via DVC (Data Version Control)
- Contact : [ml-team@company.com]
```

---

## Outils de Documentation Automatisee

### Mlflow + Model Card Generator

```python
import mlflow
from mlflow.models import ModelSignature
from mlflow.types.schema import Schema, ColSpec

# Enregistrement automatique des metriques dans MLflow
with mlflow.start_run(run_name="CustomerChurn-v2.3"):
    # Log des metriques de performance
    mlflow.log_metrics({
        "auc_roc": 0.847,
        "auc_pr": 0.724,
        "precision_at_0_5": 0.68,
        "recall_at_0_5": 0.71,
        "recall_top20pct": 0.64,
    })

    # Log des parametres du modele
    mlflow.log_params({
        "algorithm": "LightGBM",
        "n_estimators": 500,
        "max_depth": 7,
        "training_period": "2022-01 to 2024-12",
        "validation_method": "out_of_time",
    })

    # Log des tags de gouvernance
    mlflow.set_tags({
        "risk_level": "medium",
        "eu_ai_act_classification": "not_high_risk",
        "bias_audit_date": "2025-02-15",
        "bias_audit_status": "passed",
        "dpo_approved": "yes",
        "approved_by": "ml-lead",
    })

    # Signature du modele
    signature = ModelSignature(
        inputs=Schema([
            ColSpec("long", "days_since_last_login"),
            ColSpec("double", "mrr"),
            ColSpec("long", "support_tickets_30d"),
        ]),
        outputs=Schema([ColSpec("double", "churn_probability")])
    )

    mlflow.lightgbm.log_model(
        model,
        "model",
        signature=signature,
        registered_model_name="CustomerChurn"
    )
```

### Template de Registre des Modeles en Production

```yaml
# model-registry.yaml
models:
  - id: customer-churn-v2-3
    name: "Customer Churn Prediction"
    version: "2.3.0"
    status: "production"
    deployed_at: "2025-03-15"
    eu_ai_act:
      classification: "not_high_risk"
      human_oversight: "required"
    data_governance:
      personal_data: "pseudonymized"
      dpa_reference: "DPA-2025-007"
      dpo_approval_date: "2025-03-10"
    monitoring:
      psi_alert_threshold: 0.20
      performance_alert_threshold: 0.65
      review_frequency: "monthly"
    ownership:
      technical_owner: "ml-engineer@company.com"
      business_owner: "cs-head@company.com"
      escalation: "cto@company.com"
```
