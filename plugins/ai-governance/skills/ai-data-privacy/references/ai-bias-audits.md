# Audits de Biais IA — Methodologie et Outils

## Vue d'Ensemble

Un audit de biais est une evaluation systematique d'un systeme IA pour detecter les discriminations injustes dans ses predictions ou decisions. Il couvre trois dimensions : les biais dans les donnees d'entrainement, les biais dans le modele lui-meme, et les biais dans le contexte de deploiement. L'audit est a la fois une pratique ethique, une obligation reglementaire emergente (EU AI Act, Article 10), et une protection legale pour l'organisation.

---

## Taxonomie des Biais IA

### Biais dans les Donnees

**Biais historique** : Les donnees refletent des discriminations passees. Ex : les modeles de credit entrained sur des historiques ou les femmes avaient moins acces au credit reproduisent cette inegalite.

**Biais de representation** : Certains groupes sont sous-representes. Ex : un modele de reconnaissance faciale entraine principalement sur des visages blancs caucasiens performera moins bien sur des visages d'autres origines ethniques.

**Biais de mesure** : Les proxies utilises comme variables ne mesurent pas ce qu'on croit. Ex : le code postal comme variable independante — en realite, proxy de l'origine ethnique ou du statut socio-economique.

**Biais de survie** : Les donnees disponibles ne representent que les cas "survivants". Ex : entrainer un modele de selection de CV uniquement sur les profils d'employes actuels — qui ne sont pas representatifs de tous les candidats possibles.

**Biais d'etiquetage** : Les labels eux-memes sont biaises. Ex : un modele de detection de "comportement suspect" entraine sur des decisions de police elles-memes biaisees reproduira ces biais.

### Biais dans le Modele

**Biais d'agregation** : Le modele apprend un pattern moyen qui ne represente aucun sous-groupe correctement.

**Biais d'echantillonnage** : La division train/test n'est pas representive. Un sous-groupe rare dans le test set ne permet pas une evaluation robuste.

**Biais de proximite** : Les variables proches geographiquement ou socialement induisent des correlations spurieuses.

### Biais dans le Deploiement

**Feedback loops** : Les decisions du modele influencent les donnees futures, amplifiant les biais initiaux. Ex : un modele de police predictive qui cible plus certains quartiers → plus d'arrestations dans ces quartiers → confirme la prediction → davantage de surveillance.

**Automation bias** : Les utilisateurs font confiance au modele meme quand il a tort, sans exercer de jugement critique.

**Contexte de deploiement different** : Le modele est deploye dans un contexte demographique different du contexte d'entrainement.

---

## Metriques d'Equite (Fairness Metrics)

### Definitions Formelles

Soit :
- Y : label reel (0 = negatif, 1 = positif)
- Ŷ : prediction du modele
- A : attribut protege (genre, origine ethnique, age...)
- TP, FP, TN, FN : True/False Positives/Negatives

**Demographic Parity (Statistical Parity)** :
P(Ŷ=1 | A=0) = P(Ŷ=1 | A=1)

Le taux de predictions positives doit etre egal entre les groupes. Ex : taux d'approbation de credit identique entre hommes et femmes.

**Equal Opportunity** :
P(Ŷ=1 | Y=1, A=0) = P(Ŷ=1 | Y=1, A=1)

Le True Positive Rate (recall) doit etre egal. Ex : meme probabilite qu'un bon emprunteur soit approuve, quel que soit son genre.

**Equalized Odds** :
P(Ŷ=1 | Y=1, A=0) = P(Ŷ=1 | Y=1, A=1) ET P(Ŷ=1 | Y=0, A=0) = P(Ŷ=1 | Y=0, A=1)

A la fois le TPR et le FPR doivent etre egaux. Plus strict que Equal Opportunity.

**Predictive Parity (Calibration)** :
P(Y=1 | Ŷ=p, A=0) = P(Y=1 | Ŷ=p, A=1)

Un score de 0.7 doit correspondre a 70% de cas positifs reels dans chaque groupe. Le meme score signifie la meme chose dans tous les groupes.

**Individual Fairness** :
Pour des individus similaires (d(x,x') < ε), les predictions doivent etre similaires (d(f(x), f(x')) < δ). Plus difficile a implementer — necessite une metrique de similarite.

### Incompatibilite des Metriques (Theoreme de Chouldechova)

**Resultat fondamental** : Il est mathematiquement impossible de satisfaire simultanement Demographic Parity, Equal Opportunity et Predictive Parity, sauf si les taux de prevalence sont egaux entre les groupes (ce qui est rarement le cas en pratique).

Implication pratique : choisir la metrique d'equite en fonction du contexte metier et ethique, et justifier ce choix explicitement.

**Guide de choix** :

| Contexte | Metrique prioritaire | Justification |
|---|---|---|
| Credit, emploi, logement (decisions affectant un droit) | Equalized Odds | Limiter a la fois les faux positifs et faux negatifs par groupe |
| Screening medical (ne pas manquer un cas grave) | Equal Opportunity | Priorite au recall — mieux vaut un faux positif qu'un faux negatif |
| Allocation de ressources rares | Demographic Parity | Representation proportionnelle dans les beneficiaires |
| Systeme de recommandation | Predictive Parity | La signification du score doit etre stable |

---

## Outils d'Audit de Biais

### Fairlearn (Microsoft)

```python
from fairlearn.metrics import (
    MetricFrame,
    selection_rate,
    true_positive_rate,
    false_positive_rate,
    demographic_parity_difference,
    equalized_odds_difference,
)
import pandas as pd

# Donnees : y_true, y_pred, sensitive_features
sensitive = X_test['gender']  # ou age_group, ethnicity, etc.

# Calcul des metriques par groupe
metric_frame = MetricFrame(
    metrics={
        'accuracy': accuracy_score,
        'selection_rate': selection_rate,
        'tpr': true_positive_rate,
        'fpr': false_positive_rate,
    },
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sensitive
)

# Vue par groupe
print("Metriques par groupe:")
print(metric_frame.by_group)

# Differences d'equite globales
print(f"\nDemographic Parity Difference: {demographic_parity_difference(y_test, y_pred, sensitive_features=sensitive):.4f}")
print(f"Equalized Odds Difference: {equalized_odds_difference(y_test, y_pred, sensitive_features=sensitive):.4f}")

# Visualisation
metric_frame.by_group.plot.bar(subplots=True, layout=(2, 2), figsize=(14, 10))
```

### IBM AI Fairness 360 (AIF360)

```python
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
from aif360.algorithms.preprocessing import Reweighing

# Creer un dataset AIF360
dataset = BinaryLabelDataset(
    df=df_train,
    label_names=['churn'],
    protected_attribute_names=['gender'],
    privileged_protected_attributes=[[1]],  # 1 = masculin (groupe privilégie)
    unprivileged_protected_attributes=[[0]], # 0 = feminin (groupe defavorise)
)

# Metriques sur les donnees d'entrainement
metric_data = BinaryLabelDatasetMetric(
    dataset,
    unprivileged_groups=[{'gender': 0}],
    privileged_groups=[{'gender': 1}],
)
print(f"Disparate Impact: {metric_data.disparate_impact():.3f}")
# Seuil : < 0.8 ou > 1.25 signale un biais significant (regle des 80%)

# Mitigation pre-processing : Reweighing
rw = Reweighing(
    unprivileged_groups=[{'gender': 0}],
    privileged_groups=[{'gender': 1}],
)
dataset_reweighed = rw.fit_transform(dataset)

# Les poids peuvent ensuite etre passes a l'entrainement du modele
```

### Aequitas (Centre for Data Science and Public Policy)

Specifiquement concu pour les systemes de justice predictive et les politiques publiques.

```python
from aequitas.group import Group
from aequitas.bias import Bias
from aequitas.fairness import Fairness
from aequitas.plotting import Plot

# Preparer les donnees
aq_df = test_df[['score', 'label_value', 'race', 'sex', 'age_cat']].copy()

# Calcul des disparites par groupe
g = Group()
xtab, _ = g.get_crosstabs(aq_df)

# Calcul des metriques de biais
b = Bias()
bdf = b.get_disparity_predefined_groups(
    xtab,
    original_df=aq_df,
    ref_groups_dict={'race': 'White', 'sex': 'Male', 'age_cat': '25-45'},
    alpha=0.05,
)

# Rapport de fairness
f = Fairness()
fdf = f.get_group_value_fairness(bdf)
```

---

## Methodologie d'Audit Complet

### Phase 1 — Preparation (1-2 semaines)

**1.1 Perimetre de l'audit** :
- Quel modele ? Quelle version en production ?
- Quels groupes proteges analyser ? (conformite legale + enjeux metier)
- Quelles metriques d'equite ? Justification du choix
- Quels seuils d'alerte ? (ex: ecart > 10 points = alerte, > 20 points = bloquant)

**1.2 Collecte des donnees** :
- Dataset de test avec labels reels et attributs proteges
- Taille minimum recommandee par groupe : 500 observations (en dessous, les metriques ne sont pas statistiquement robustes)
- Verifier que les attributs proteges ne sont pas des proxies trop directs les uns des autres

**1.3 Tests statistiques de significativite** :
Avant de conclure qu'un ecart est un biais, tester sa significativite statistique. Un ecart de 3% sur 50 observations n'est pas significatif.

```python
from scipy.stats import chi2_contingency, fisher_exact

# Test chi2 pour la Demographic Parity
def test_demographic_parity(y_pred, sensitive, alpha=0.05):
    groups = sensitive.unique()
    contingency = pd.crosstab(sensitive, y_pred)
    chi2, p_value, dof, expected = chi2_contingency(contingency)

    print(f"Chi2 = {chi2:.4f}, p-value = {p_value:.4f}")
    if p_value < alpha:
        print(f"Ecart SIGNIFICATIF au seuil {alpha}")
    else:
        print(f"Ecart non significatif — peut etre du au hasard")
    return p_value
```

### Phase 2 — Analyse (2-4 semaines)

**2.1 Analyse exploratoire des donnees** :
- Distribution des attributs proteges dans le dataset
- Taux de labels positifs par groupe (base rate)
- Corrélations entre attributs proteges et features du modele

**2.2 Calcul des metriques par groupe** :
- Toutes les metriques definies en Phase 1
- Par groupe et par sous-groupe (intersectionnalite : femme + senior)

**2.3 Analyse des erreurs** :
- Quels types d'erreurs (FP vs FN) affectent quels groupes ?
- Un faux positif et un faux negatif ont-ils le meme cout pour tous les groupes ?

**2.4 Analyse causale (si possible)** :
Est-ce que les ecarts sont dus a des differences reelles dans les outcomes, ou a des discriminations algorithmiques ? Utiliser des methodes causales (DAG, counterfactual analysis) si la donnee le permet.

### Phase 3 — Mitigation

**Pre-processing** :
```python
# Reequilibrage du dataset par sur-echantillonnage
from imblearn.over_sampling import SMOTENC

# SMOTENC respecte les variables categoriques
smote = SMOTENC(categorical_features=[3, 4], random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
```

**In-processing (contrainte dans la fonction de perte)** :
```python
# Fairlearn Reduction — Equalized Odds Constraint
from fairlearn.reductions import ExponentiatedGradient, EqualizedOdds

estimator = LGBMClassifier()
mitigator = ExponentiatedGradient(
    estimator,
    constraints=EqualizedOdds(),
    eps=0.02,  # tolerance sur la violation de la contrainte
)
mitigator.fit(X_train, y_train, sensitive_features=A_train)
y_pred_mitigated = mitigator.predict(X_test)
```

**Post-processing (seuils differencies)** :
```python
from fairlearn.postprocessing import ThresholdOptimizer

postprocessor = ThresholdOptimizer(
    estimator=model,
    constraints="equalized_odds",
    predict_method="predict_proba",
    objective="balanced_accuracy_score",
)
postprocessor.fit(X_cal, y_cal, sensitive_features=A_cal)
y_pred_post = postprocessor.predict(X_test, sensitive_features=A_test)
```

### Phase 4 — Documentation et Rapport

```markdown
# Rapport d'Audit de Biais — [Nom du Modele] — [Date]

## 1. Perimetre et Methodologie
- Modele audite : [Nom, Version]
- Date du test set : [Periode]
- Groupes proteges analyses : [Liste]
- Metriques d'equite choisies : [Liste avec justification]
- Seuils d'alerte : [Valeurs]

## 2. Resultats par Groupe

| Groupe | N | Taux selection | TPR | FPR | Ecart max (ref.) | Statut |
|---|---|---|---|---|---|---|
| Groupe A (reference) | 12 400 | 24.3% | 0.71 | 0.12 | - | - |
| Groupe B | 3 200 | 21.8% | 0.68 | 0.14 | 2.5% | OK |
| Groupe C | 890 | 18.1% | 0.61 | 0.17 | 10.2% | ALERTE |

## 3. Tests de Significativite
- Ecart Groupe C significant (p < 0.05, n = 890)
- Ecart Groupe B non significant (p = 0.23)

## 4. Analyse Causale
L'ecart du Groupe C est partiellement explique par [cause metier legitimee].
La part non expliquee (3.1 points) est attribuee a [biais algorithmique / data].

## 5. Mesures de Mitigation Recommandees
- Court terme : ajustement du seuil de decision pour le Groupe C
- Moyen terme : enrichissement du dataset (collecte donnees Groupe C)
- Long terme : contrainte d'equite dans le retrainement

## 6. Risque Residuel et Acceptation
Apres mitigation, ecart residuel Groupe C : 2.1%
Decision : ACCEPTABLE (en dessous du seuil de 5% post-mitigation)
Signataires : [DPO] [ML Lead] [Business Owner]

## 7. Prochaine Revue
Date : [Trimestre suivant]
Criteres de re-audit urgent : [Conditions]
```

---

## Conformite Reglementaire et Audit Externe

### EU AI Act et Audits de Biais

Pour les IA a risque eleve (Annexe III), l'Article 10 impose une gouvernance des donnees incluant l'identification et la correction des biais. L'audit de biais n'est pas nomme explicitement mais est de facto obligatoire pour documenter la conformite.

Les Notified Bodies (organismes de certification tiers) verifieront les pratiques d'audit de biais dans leurs evaluations de conformite pour les systemes a risque eleve soumis a evaluation tierce.

### Standards Emergents

- **ISO/IEC TR 24027:2021** : Biais dans les systemes IA et prise de decision
- **NIST AI 100-1** : Trustworthy and Responsible AI — section fairness
- **IEEE P7003** : Standard for Algorithmic Bias Considerations (en cours)
- **Aequitas Toolkit** (University of Chicago) : Reference pratique pour les systemes de justice

### Audit Externe Independant

Pour les systemes a fort impact (recrutement, credit, justice), un audit externe independant par un tiers specialise (ex: Credo AI, Holistic AI, Eticas) peut etre necessaire pour :
- Conformite reglementaire (EU AI Act, obligations sectorielles)
- Confiance des parties prenantes
- Protection legale en cas de litige
- Certification ou labellisation (ex: label AFNOR, ISO 42001)
