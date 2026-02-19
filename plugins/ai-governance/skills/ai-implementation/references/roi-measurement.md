# ROI Measurement — KPIs IA, Calcul du ROI & Business Case

## Overview

Ce guide couvre la methodologie de mesure du retour sur investissement des initiatives IA : comment definir des KPIs metier alignes sur les modeles, comment mesurer l'impact incremental via l'experimentation, comment construire un business case IA rigoureux, et comment mettre en place un dashboard de suivi ROI. L'objectif est de passer d'une evaluation uniquement technique (AUC, RMSE) a une demonstration de valeur metier mesurable et defensable.

---

## Pourquoi la Mesure du ROI IA est Difficile

### Problemes Frequents

**Attribution causale** : Quand le churn baisse de 5% apres le deploiement d'un modele de retention, quelle fraction est due au modele ? D'autres initiatives ont peut-etre change en meme temps (amelioration produit, equipe support renforcee). Sans experimentation rigoureuse, l'attribution est impossible.

**Metriques proxy vs valeur reelle** : L'AUC de 0.85 est une metrique de modele, pas de valeur metier. Un modele avec AUC 0.82 qui est utilise par les equipes ventes et declenche des actions est plus precieux qu'un modele avec AUC 0.91 qui n'est pas adopte.

**Couts caches** : Le cout d'un modele IA inclut : compute d'entrainement et d'inference, stockage, equipe de maintenance, monitoring, retraining, documentation, formation des utilisateurs. Sous-estimer les couts conduit a des business cases trop optimistes.

**Horizon de mesure** : Certains benefices de l'IA se manifestent a 6-12 mois (ex: fidélisation client). Mesurer uniquement a 30 jours peut underestimer la valeur reelle.

**Baseline ambigue** : Comparer a quoi ? La situation sans IA (mais avec d'autres initiatives en cours) ? La situation N-1 (mais le marche a change) ? La baseline doit etre definie avant le deploiement.

---

## Framework de ROI IA

### Structure du ROI

```
ROI IA = (Valeur Generee - Couts Totaux) / Couts Totaux x 100

Valeur Generee = Benefices Directs + Benefices Indirects

Benefices Directs :
- Revenus additionnels (conversion, upsell, retention)
- Couts evites (fraude evitee, erreurs reduites, automatisation)
- Gains de productivite (temps economise x cout horaire)

Benefices Indirects :
- Amelioration de la satisfaction client (NPS -> retention -> revenus futurs)
- Reduction des risques (moins d'incidents, meilleure conformite)
- Avantage competitif (time-to-market reduit)

Couts Totaux = Couts One-Time + Couts Recurrents

Couts One-Time :
- Developpement du modele (salaires data scientists, ML engineers)
- Infrastructure initiale (compute d'entrainement, storage)
- Integration technique (developpement de l'API, modifications systeme)
- Formation des utilisateurs

Couts Recurrents (annuels) :
- Compute d'inference (proportionnel au volume de predictions)
- Stockage des donnees d'entrainement et de production
- Maintenance et monitoring (30-40% du cout initial de developpement)
- Retraining periodique
- Licences outils (MLflow Cloud, W&B, Vertex AI, SageMaker)
```

### KPIs par Type de Modele

| Type de modele | KPI metier principal | KPI secondaires | Methode de mesure |
|---|---|---|---|
| **Churn prediction** | Taux de retention ameliore (%) | Revenus sauvegardes (EUR), LTV moyen des clients retenus | A/B test sur la population de churners identifies |
| **Recommandation** | Taux de conversion incremental (%) | Panier moyen, CTR, Revenue Per User | A/B test (groupe expose vs controle) |
| **Scoring de leads** | Taux de conversion MQL→SQL (%) | Duree du cycle de vente, Revenue per Sales Rep | Comparaison pre/post, A/B test |
| **Fraud detection** | Montant de fraude evite (EUR) | Taux de faux positifs (friction), recall | Analyse des cas detectes vs non detectes |
| **Demand forecasting** | Reduction des ruptures et surstocks (%) | Couts de stockage, ventes perdues | Comparaison historique, simulation |
| **NLP / extraction** | Heures economisees par semaine | Taux d'erreur, satisfaction equipes | Chronometrage avant/apres, sondage |
| **Maintenance predictive** | Reduction des pannes non planifiees (%) | Couts de maintenance, uptime | Comparaison pre/post sur equipements monitores |

---

## Mesure de l'Impact Incremental

### A/B Testing des Modeles

L'A/B test est la methode la plus rigoureuse pour mesurer l'impact incremental d'un modele. La cle est de randomiser au niveau de l'individu (client, transaction) et non au niveau agrege.

**Design type — Modele de churn**

```
Population : Clients identifies comme a risque de churn (score > 0.6)

Groupe A (Controle) : 50% des clients a risque
- Pas d'action specifique declenchee par le modele
- La relation se deroule normalement (meme qualite de produit/support)

Groupe B (Traitement) : 50% des clients a risque
- Action de retention declenchee : email personnalise + offre (si score > 0.75)
- Action legere : email d'engagement (si 0.6 < score < 0.75)

Metriques primaires :
- Taux de churn a 30, 60, 90 jours dans chaque groupe
- Difference de taux de churn (effet incremental du modele)

Metriques secondaires :
- Revenue sauvegarde (nb clients retenus x LTV moyen)
- Taux d'engagement sur les actions (ouverture email, clic, conversion)
- Cout par client retenu

Duree minimale : 60 jours (pour observer le churn et minimiser les effets temporaires)
Taille d'echantillon : calculee a priori (voir section calcul de sample size)
```

```python
# Calcul de la taille d'echantillon pour l'A/B test

from scipy import stats
import numpy as np

def sample_size_ab_test(baseline_rate, expected_lift, alpha=0.05, power=0.80):
    """
    Calcule la taille d'echantillon pour un A/B test.

    Args:
        baseline_rate: Taux dans le groupe controle (ex: 0.15 pour 15% de churn)
        expected_lift: Amelioration attendue (ex: 0.03 pour -3% de churn)
        alpha: Niveau de signification (defaut: 0.05 = 5%)
        power: Puissance statistique (defaut: 0.80 = 80%)
    """
    treatment_rate = baseline_rate - expected_lift  # Pour une reduction du churn

    # Calcul de l'effet et de la taille d'echantillon
    pooled_rate = (baseline_rate + treatment_rate) / 2
    effect_size = abs(baseline_rate - treatment_rate) / np.sqrt(pooled_rate * (1 - pooled_rate))

    analysis = TTestIndPower()
    n = analysis.solve_power(
        effect_size=effect_size,
        power=power,
        alpha=alpha
    )

    return int(np.ceil(n))

# Exemple : taux de churn de base = 15%, amelioration attendue = 3 points
n_per_group = sample_size_ab_test(baseline_rate=0.15, expected_lift=0.03)
print(f"Taille d'echantillon requise par groupe : {n_per_group}")
print(f"Taille totale : {n_per_group * 2}")
```

### Methodes Alternatives si l'A/B Test est Impossible

**Difference-en-Differences (DiD)** : Comparer l'evolution du KPI entre un groupe traite et un groupe de controle sur deux periodes (avant et apres le deploiement). Requiert que les deux groupes aient des tendances paralleles avant le deploiement.

**Propensity Score Matching (PSM)** : Apparier des individus traites et non traites ayant des caracteristiques similaires, pour creer un groupe de controle "synthétique". Reduit le biais de selection.

**Regression Discontinuite** : Si le modele est applique a partir d'un seuil (ex: score > 0.7), comparer les individus juste en dessous et juste au-dessus du seuil. L'effet pres du seuil est comparable a un RCT.

**Analyse Pre/Post** : Comparer le KPI avant et apres le deploiement. Methode fragile (confusion avec d'autres evenements) mais rapide. A utiliser uniquement quand les autres methodes sont impossibles et avec des tests de robustesse.

---

## Construction du Business Case IA

### Template de Business Case

```
BUSINESS CASE — [Nom du Projet IA]
Date : ___
Auteur : ___
Version : ___

1. RESUME EXECUTIF
   Probleme metier : ___
   Solution IA proposee : ___
   ROI projete sur 3 ans : ___x
   Investissement initial : ___ EUR
   Payback period : ___ mois

2. PROBLEME METIER
   Situation actuelle : [description avec metriques]
   Impact du probleme : [couts, risques, opportunites ratees]
   Objectif : [amelioration cible chiffree]

3. SOLUTION PROPOSEE
   Type de modele : ___
   Donnees necessaires : ___
   Integration systeme : ___
   Equipe requise : ___

4. ESTIMATION DES BENEFICES
   Metrique cible : ___
   Valeur actuelle : ___
   Valeur cible (an 1) : ___
   Hypotheses : [liste des hypotheses]
   Valeur annuelle estimee : ___ EUR

   [Tableau de calcul de la valeur]
   | Benefice | Calcul | Valeur annuelle |
   |---|---|---|
   | Retention amelioree | [X clients retenus x LTV EUR] | ___ EUR |
   | Automatisation | [Y heures economisees x cout horaire EUR] | ___ EUR |
   | Fraude evitee | [Z EUR de fraude detectee] | ___ EUR |
   | TOTAL | | ___ EUR |

5. ESTIMATION DES COUTS
   [Tableau de couts]
   | Cout | One-Time | Recurrent / an |
   |---|---|---|
   | Developpement (X sprints x Y EUR) | ___ EUR | - |
   | Compute d'entrainement | ___ EUR | - |
   | Infrastructure d'inference | - | ___ EUR |
   | Maintenance et monitoring | - | ___ EUR |
   | Licences outils | - | ___ EUR |
   | TOTAL | ___ EUR | ___ EUR |

6. ROI PAR ANNEE
   | Annee | Benefices | Couts | Cash Flow | ROI Cumule |
   |---|---|---|---|---|
   | An 0 | 0 | ___ (investissement) | -___ | -100% |
   | An 1 | ___ | ___ | ___ | ___% |
   | An 2 | ___ | ___ | ___ | ___% |
   | An 3 | ___ | ___ | ___ | ___% |

7. RISQUES ET MITIGATION
   | Risque | Probabilite | Impact | Mitigation |
   |---|---|---|---|
   | Qualite des donnees insuffisante | Moyen | Eleve | Audit qualite pre-projet |
   | Performance modele insuffisante | Faible | Eleve | Critere de Go/No-Go pre-defini |
   | Adoption faible par les equipes | Moyen | Moyen | Plan de change management |

8. PLAN D'IMPLEMENTATION
   Phase 1 (M1-M2) : PoC et qualification
   Phase 2 (M3-M4) : Developpement production
   Phase 3 (M5) : Deploiement et test A/B
   Phase 4 (M6+) : Mesure du ROI et optimisation

9. DECISION REQUISE
   Budget demande : ___ EUR
   Decision requise de : ___
   Date limite : ___
```

---

## Dashboard de Suivi ROI

### Structure du Dashboard

**Vue Executive (mensuelle)**

| Metrique | Valeur actuelle | Valeur cible | Delta vs cible | Trend |
|---|---|---|---|---|
| Valeur generee totale (EUR) | ___ | ___ | ___% | ↑ ↓ → |
| Couts operationnels IA (EUR) | ___ | ___ | ___% | |
| ROI net (%) | ___% | ___% | | |
| Nb modeles en production | ___ | ___ | | |
| Nb modeles ROI > 1x | ___ | ___ | | |

**Vue Portefeuille de Modeles**

| Modele | KPI metier | Valeur an | Cout an | ROI | Statut |
|---|---|---|---|---|---|
| Churn predictor | Taux retention +3% | 450k EUR | 60k EUR | 6.5x | En production |
| Lead scoring | Conversion MQL +15% | 200k EUR | 30k EUR | 5.7x | En production |
| Demand forecast | Stocks -8% | 120k EUR | 20k EUR | 5.0x | En production |
| Recommandation | Upsell +5% | 300k EUR | 80k EUR | 2.75x | En production |
| Fraude detection | Fraude evitee | 180k EUR | 50k EUR | 2.6x | En production |
| Credit scoring | En cours de PoC | TBD | 40k EUR (invest) | TBD | PoC |

**Vue Operationnelle (hebdomadaire)**

| Modele | Volume de predictions / semaine | Latence P99 | Couts compute / semaine | Alertes drift |
|---|---|---|---|---|
| Churn predictor | 150k | 45ms | 85 EUR | 0 |
| Lead scoring | 5k | 12ms | 8 EUR | 0 |
| Demand forecast | 50k | 120ms | 30 EUR | 1 (feature X) |

### Automatisation du Calcul du ROI

```python
# roi_tracker.py — Calcul automatique du ROI mensuel

class ModelROITracker:
    """
    Suit le ROI d'un modele ML en production.
    """

    def __init__(self, model_name, kpi_metric, baseline_value,
                 unit_value_eur, monthly_cost_eur):
        self.model_name = model_name
        self.kpi_metric = kpi_metric
        self.baseline = baseline_value
        self.unit_value = unit_value_eur  # Valeur d'une unite d'amelioration du KPI
        self.monthly_cost = monthly_cost_eur

    def calculate_monthly_roi(self, current_kpi_value, control_kpi_value=None):
        """
        Calcule le ROI mensuel du modele.

        Si control_kpi_value est fourni, utilise le lift vs controle (A/B test).
        Sinon, utilise le lift vs baseline historique.
        """
        if control_kpi_value is not None:
            # Methode A/B test : mesure l'impact incremental
            lift = current_kpi_value - control_kpi_value
        else:
            # Methode baseline : attention aux facteurs confondants
            lift = current_kpi_value - self.baseline

        monthly_value_eur = lift * self.unit_value
        monthly_roi = (monthly_value_eur - self.monthly_cost) / self.monthly_cost * 100

        return {
            "model": self.model_name,
            "kpi_lift": lift,
            "monthly_value_eur": monthly_value_eur,
            "monthly_cost_eur": self.monthly_cost,
            "monthly_roi_pct": monthly_roi,
            "is_profitable": monthly_value_eur > self.monthly_cost
        }

# Exemple d'utilisation
churn_tracker = ModelROITracker(
    model_name="churn-prediction-v3",
    kpi_metric="retention_rate",
    baseline_value=0.82,       # 82% de retention sans le modele
    unit_value_eur=150_000,    # 1 point de retention = 150k EUR/mois (LTV moyen x nb clients)
    monthly_cost_eur=5_000     # Couts mensuels : compute + maintenance
)

# Avec A/B test
roi_report = churn_tracker.calculate_monthly_roi(
    current_kpi_value=0.853,   # 85.3% de retention dans le groupe traitement
    control_kpi_value=0.820    # 82.0% de retention dans le groupe controle
)
# Lift = 3.3 points de retention
# Valeur mensuelle = 3.3% x 150k = 4,950 EUR...
# -> modele à la limite du ROI positif, a reevaluer
```

---

## Gouvernance du ROI IA

### Revue Trimestrielle du Portefeuille

Processus de revue trimestrielle :

1. **Presentation du ROI par modele** : data scientist ou ML engineer responsable presente le ROI observe vs projete.

2. **Classification en 3 categories** :
   - ✅ **ROI > 3x** : maintenir en production, optimiser si possible
   - ⚠️ **1x < ROI < 3x** : analyser les opportunites d'optimisation (meilleur modele, meilleures donnees, meilleure adoption)
   - ❌ **ROI < 1x** : plan d'amelioration avec deadline ou decommissionnement

3. **Decisions de priorisation** : Allouer les ressources de l'equipe ML en fonction du ROI potentiel de chaque initiative dans le backlog.

### Criteres de Decommissionnement

Un modele doit etre decommissionne lorsque :
- Son ROI est inferieur a 1x depuis plus de 2 trimestres consecutifs
- Son ROI < 1x depuis 6 mois malgre un plan d'optimisation execute
- Une solution de remplacement (nouveau modele, SaaS) offre un ROI superieur avec le meme investissement
- Le cas d'usage metier n'est plus pertinent (changement de strategie, deprecation du produit)

```python
# Checklist de decommissionnement
decommission_checklist = {
    "notification_equipes": False,      # Prevenir les equipes consommatrices
    "suppression_endpoint": False,      # Retirer l'API ou le job batch
    "archivage_artefacts": False,       # Archiver modele, code, donnees pendant N mois
    "mlflow_archive": False,            # Archiver dans le model registry
    "documentation_retour_exp": False,  # Documenter les lecons apprises
    "communication_officielle": False,  # Newsletter IA interne
    "suppression_monitoring": False,    # Supprimer les alertes et dashboards
    "audit_couts_residuels": False,     # Verifier qu'aucun cout de compute ne subsiste
}
```
