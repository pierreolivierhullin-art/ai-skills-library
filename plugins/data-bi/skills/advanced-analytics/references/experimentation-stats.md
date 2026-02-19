# Experimentation & Statistics — A/B Testing, Causal Inference & Uplift Modeling

## Overview

Ce guide couvre la rigueur statistique pour l'experimentation en entreprise : design et execution des A/B tests, calcul de la taille d'echantillon, interpretation des resultats, tests bayesiens, inference causale sans randomisation, et uplift modeling pour mesurer l'impact incremental. L'objectif est d'etablir une culture de l'experimentation rigoureuse qui distingue la correlation de la causalite et protege contre les biais courants.

---

## Fondamentaux de l'Experimentation

### Pourquoi Experimenter ?

La correlation n'est pas la causalite. Des exemples courants d'intuitions incorrectes sans experimentation :

- "Nos utilisateurs qui utilisent la feature X ont un taux de retention 40% plus eleve" → Peut-etre que les utilisateurs les plus engages sont a la fois plus enclins a utiliser X ET a rester (selection bias).
- "Les clients contacts par le modele de churn ont churne moins apres le deploiement" → Peut-etre que le marche s'est ameliore en meme temps, ou que d'autres initiatives de retention ont ete lancees.
- "Le panier moyen a augmente depuis le lancement de la recommandation" → Peut-etre une saisonnalite ou une campagne marketing en parallele.

L'experimentation controlee (A/B test randomise) est le seul moyen de mesurer l'impact causal d'une intervention.

### Terminologie Essentielle

| Terme | Definition |
|-------|-----------|
| **Hypothese nulle (H0)** | Il n'y a pas d'effet de l'intervention (A = B) |
| **Hypothese alternative (H1)** | Il y a un effet de l'intervention (A ≠ B) |
| **Erreur de type I (α)** | Rejeter H0 alors qu'elle est vraie (faux positif). Standard : α = 5% |
| **Erreur de type II (β)** | Ne pas rejeter H0 alors qu'elle est fausse (faux negatif) |
| **Puissance statistique (1-β)** | Probabilite de detecter un vrai effet. Standard : 80% |
| **p-value** | Probabilite d'observer un resultat aussi extreme si H0 est vraie |
| **Effet minimum detectable (MDE)** | La plus petite difference que l'on veut pouvoir detecter |
| **Niveau de confiance** | 1 - α = 95% (standard) — probabilite que l'intervalle de confiance contient le vrai parametre |

---

## Design de l'A/B Test

### Etapes Pre-Test Obligatoires

**Etape 1 : Formuler l'hypothese**

L'hypothese doit etre definie AVANT de voir les donnees, pas apres (risque de HARKing : Hypothesizing After Results are Known).

```
Mauvaise hypothese : "Voyons si la nouvelle feature ameliore quelque chose"
Bonne hypothese    : "La personnalisation du message d'onboarding augmente
                      le taux de completion de l'onboarding de 5 points
                      dans les 7 premiers jours apres l'inscription"

Format recommande : "[Intervention] augmentera/reduira [metrique] de [magnitude]
                    parmi [population] sur [horizon de mesure]"
```

**Etape 2 : Choisir la metrique principale**

Ne definir qu'une seule metrique principale par experience. Les metriques multiples multiplient les faux positifs (probleme de comparaisons multiples).

| Critere | Recommandation |
|---|---|
| **Sensitive** | Varie significativement entre variantes si l'effet est reel |
| **Robuste** | Pas sensible aux outliers (outliers un utilisateur peut distordre la moyenne) |
| **Mesurable rapidement** | Observable dans la duree du test |
| **Alignee sur l'objectif metier** | Pas une metrique proxy sans lien avec le revenu |

**Etape 3 : Definir la taille d'echantillon**

```python
from scipy.stats import norm, chi2_contingency
import numpy as np

def sample_size_proportion(baseline_rate, mde, alpha=0.05, power=0.80):
    """
    Calcule la taille d'echantillon pour une metrique de proportion (taux de conversion, churn).

    Args:
        baseline_rate: Taux dans le groupe controle (ex: 0.15 pour 15% de churn)
        mde: Minimum Detectable Effect en valeur absolue (ex: 0.03 pour 3 points)
        alpha: Niveau de signification (5%)
        power: Puissance statistique (80%)

    Returns:
        Taille d'echantillon par groupe
    """
    treatment_rate = baseline_rate + mde

    z_alpha = norm.ppf(1 - alpha / 2)  # 1.96 pour alpha = 0.05 (test bilateral)
    z_beta = norm.ppf(power)            # 0.842 pour power = 0.80

    pooled_p = (baseline_rate + treatment_rate) / 2
    n = (z_alpha * np.sqrt(2 * pooled_p * (1 - pooled_p)) +
         z_beta * np.sqrt(baseline_rate * (1 - baseline_rate) +
                          treatment_rate * (1 - treatment_rate)))**2 / mde**2

    return int(np.ceil(n))

# Exemple : taux de churn de base 15%, vouloir detecter -3 points de reduction
n = sample_size_proportion(baseline_rate=0.15, mde=-0.03)
print(f"Taille requise par groupe : {n}")
print(f"Taille totale : {n * 2}")
print(f"Avec 1000 clients/jour eligibles : duree minimale = {n * 2 / 1000:.0f} jours")
```

```python
def sample_size_continuous(baseline_mean, baseline_std, mde, alpha=0.05, power=0.80):
    """
    Calcule la taille d'echantillon pour une metrique continue (revenus, panier moyen).

    Args:
        baseline_mean: Moyenne dans le groupe controle (ex: 50.0 EUR de panier moyen)
        baseline_std: Ecart-type dans le groupe controle
        mde: Minimum Detectable Effect en valeur absolue (ex: 5.0 EUR)
    """
    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(power)
    effect_size = mde / baseline_std  # Cohen's d

    n = ((z_alpha + z_beta) / effect_size) ** 2

    return int(np.ceil(n))

# Exemple : panier moyen de 50 EUR, ecart-type 30 EUR, detecter +5 EUR
n = sample_size_continuous(baseline_mean=50.0, baseline_std=30.0, mde=5.0)
print(f"Taille requise par groupe : {n}")
```

---

## Execution et Analyse du Test

### Checklist de Lancement

```
Pre-lancement
[ ] Hypothese formalisee et enregistree (pre-registration)
[ ] Metrique principale definie (une seule)
[ ] Metriques secondaires et guardrails definis (max 5)
[ ] Taille d'echantillon calculee et validee
[ ] Duree du test definie et respectee
[ ] Methode de randomisation definie (par user_id, session_id, entreprise)
[ ] Checks de SRM (Sample Ratio Mismatch) configures

Pendant le test
[ ] PAS de regard sur les resultats avant la fin (peeking problem)
[ ] Exception : monitoring des guardrails (taux d'erreur, crashs)
[ ] Documenter tout incident ou changement pendant la periode de test

Post-lancement
[ ] Verifier le SRM avant d'analyser les resultats
[ ] Analyser la metrique principale
[ ] Analyser les metriques secondaires et guardrails
[ ] Segmenter les resultats par sous-groupes predetermines
[ ] Documenter la decision et les apprentissages
```

### Sample Ratio Mismatch (SRM)

Le SRM est un probleme d'implementation ou la proportion reelle d'utilisateurs dans chaque groupe differe de la proportion theorique. C'est le signal d'une erreur dans la randomisation.

```python
from scipy.stats import chi2_contingency

def check_srm(n_control: int, n_treatment: int, expected_split: float = 0.5,
              alpha: float = 0.01) -> dict:
    """
    Verifie si la distribution entre les groupes correspond a la repartition attendue.

    Un p-value < alpha indique un SRM — NE PAS analyser les resultats si SRM detecte.
    """
    total = n_control + n_treatment
    expected_control = total * expected_split
    expected_treatment = total * (1 - expected_split)

    chi2, p_value, _, _ = chi2_contingency([
        [n_control, n_treatment],
        [expected_control, expected_treatment]
    ])

    has_srm = p_value < alpha

    return {
        "n_control": n_control,
        "n_treatment": n_treatment,
        "split_observed": n_treatment / total,
        "split_expected": 1 - expected_split,
        "chi2": chi2,
        "p_value": p_value,
        "has_srm": has_srm,
        "message": "SRM DETECTE - NE PAS ANALYSER" if has_srm else "Distribution OK"
    }

# Verifier avant toute analyse
srm_result = check_srm(n_control=4850, n_treatment=5150)
print(srm_result)
```

### Analyse des Resultats

```python
from scipy import stats
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

def analyze_ab_test_proportion(control_conversions, control_n,
                                treatment_conversions, treatment_n,
                                alpha=0.05):
    """
    Analyse un A/B test sur une metrique de proportion (taux de conversion, churn).
    """
    control_rate = control_conversions / control_n
    treatment_rate = treatment_conversions / treatment_n
    absolute_lift = treatment_rate - control_rate
    relative_lift = absolute_lift / control_rate

    # Test de proportion bilateral
    count = np.array([treatment_conversions, control_conversions])
    nobs = np.array([treatment_n, control_n])
    z_stat, p_value = proportions_ztest(count, nobs, alternative='two-sided')

    # Intervalle de confiance a 95% sur le lift absolu
    se = np.sqrt(control_rate * (1 - control_rate) / control_n +
                  treatment_rate * (1 - treatment_rate) / treatment_n)
    ci_lower = absolute_lift - 1.96 * se
    ci_upper = absolute_lift + 1.96 * se

    is_significant = p_value < alpha

    print(f"\n{'='*50}")
    print(f"RESULTAT A/B TEST")
    print(f"{'='*50}")
    print(f"Groupe controle  : {control_conversions}/{control_n} = {control_rate:.3%}")
    print(f"Groupe traitement: {treatment_conversions}/{treatment_n} = {treatment_rate:.3%}")
    print(f"\nLift absolu  : {absolute_lift:+.3%} ({ci_lower:+.3%} ; {ci_upper:+.3%})")
    print(f"Lift relatif : {relative_lift:+.1%}")
    print(f"\np-value : {p_value:.4f}")
    print(f"Significatif a alpha={alpha} : {'OUI ✓' if is_significant else 'NON ✗'}")

    return {
        "control_rate": control_rate, "treatment_rate": treatment_rate,
        "absolute_lift": absolute_lift, "relative_lift": relative_lift,
        "ci_lower": ci_lower, "ci_upper": ci_upper,
        "p_value": p_value, "is_significant": is_significant
    }
```

---

## Tests Bayesiens

### Avantages et Quand Utiliser

L'approche bayesienne repond a la question : "Quelle est la probabilite que le traitement soit meilleur que le controle ?" plutot que "Est-ce que je rejette H0 ?".

**Avantages** :
- Peut etre arrete plus tot (si la probabilite est tres elevee)
- Interpretation plus intuitive
- Permet de calculer l'expected loss (cout de la mauvaise decision)

**Limites** :
- Necessite de choisir un prior (connaissance a priori)
- Moins standard, peut etre difficile a communiquer aux parties prenantes

```python
import numpy as np
from scipy import stats

def bayesian_ab_test(control_conversions, control_n,
                      treatment_conversions, treatment_n,
                      prior_alpha=1, prior_beta=1,
                      n_samples=100_000):
    """
    Test bayesien pour une metrique de proportion avec prior Beta.

    Returns:
        probability_B_wins: Probabilite que le traitement (B) est superieur au controle (A)
        expected_lift: Lift attendu si on choisit le traitement
        expected_loss: Perte attendue si on choisit le traitement alors qu'il est inferieur
    """
    # Distribution posterieure = Beta(alpha + conversions, beta + non-conversions)
    alpha_control = prior_alpha + control_conversions
    beta_control = prior_beta + (control_n - control_conversions)

    alpha_treatment = prior_alpha + treatment_conversions
    beta_treatment = prior_beta + (treatment_n - treatment_conversions)

    # Echantillonner les posterieures
    samples_control = np.random.beta(alpha_control, beta_control, n_samples)
    samples_treatment = np.random.beta(alpha_treatment, beta_treatment, n_samples)

    # Probabilite que le traitement est superieur au controle
    prob_B_wins = np.mean(samples_treatment > samples_control)

    # Lift attendu
    expected_lift = np.mean(samples_treatment - samples_control)

    # Expected loss si on choisit le traitement
    losses = np.maximum(samples_control - samples_treatment, 0)
    expected_loss = np.mean(losses)

    print(f"\n{'='*50}")
    print(f"RESULTAT BAYESIEN A/B TEST")
    print(f"{'='*50}")
    print(f"P(traitement > controle) : {prob_B_wins:.1%}")
    print(f"Lift attendu             : {expected_lift:+.3%}")
    print(f"Expected loss            : {expected_loss:.4%}")

    if prob_B_wins > 0.95:
        recommendation = "DECLARER TRAITEMENT GAGNANT"
    elif prob_B_wins < 0.05:
        recommendation = "DECLARER CONTROLE GAGNANT"
    else:
        recommendation = "CONTINUER LE TEST"

    print(f"Recommandation           : {recommendation}")

    return {
        "prob_treatment_wins": prob_B_wins,
        "expected_lift": expected_lift,
        "expected_loss": expected_loss
    }
```

---

## Problemes Courants et Biais

### Le Peeking Problem

Le peeking problem est l'erreur la plus frequente en A/B testing : regarder les resultats avant la fin du test et arreter des qu'on voit une significativite.

**Pourquoi c'est un probleme** : Si on regarde les resultats chaque jour pendant 30 jours et qu'on arrete des qu'on voit p < 0.05, le taux reel de faux positifs monte a 26% (au lieu des 5% attendus).

**Solutions** :
- Calculer la taille d'echantillon avant de lancer et ne regarder les resultats QU'UNE FOIS apres.
- Utiliser des methodes de testing sequentiel qui controlent le taux de faux positifs sur plusieurs regards (SPRT, always-valid p-values).
- Utiliser les tests bayesiens (probabilite de gain > 95% comme critere d'arret).

### Novelty Effect

Les utilisateurs peuvent reagir differemment a une nouvelle feature simplement parce qu'elle est nouvelle, et non parce qu'elle est meilleure. L'effet peut disparaitre apres quelques semaines.

**Mitigation** : Pour les tests sur des fonctionnalites visibles, conduire le test pendant au moins 2 semaines et analyser la tendance (le lift est-il stable ou en decroissance ?).

### Network Effects (Interference)

Si les utilisateurs interagissent entre eux (reseau social, marketplace), l'effet de l'une des variantes peut "contaminer" l'autre groupe.

**Mitigation** : Utiliser une randomisation par clusters (ex: randomiser par entreprise plutot que par individu dans un contexte B2B).

---

## Inference Causale

### Difference-en-Differences (DiD)

Le DiD compare l'evolution d'un groupe traite avant/apres une intervention a l'evolution d'un groupe controle sur la meme periode.

```python
import pandas as pd
import statsmodels.formula.api as smf

def difference_in_differences(df, outcome_col, treatment_col, time_col,
                                pre_period, post_period):
    """
    Calcule l'estimateur DiD.

    df: DataFrame avec colonnes outcome, treatment (0/1), time (0=pre, 1=post)
    """
    # Verifier les tendances paralleles (assumption clef du DiD)
    pre_data = df[df[time_col] == 0]
    treated_pre = pre_data[pre_data[treatment_col] == 1][outcome_col].mean()
    control_pre = pre_data[pre_data[treatment_col] == 0][outcome_col].mean()

    post_data = df[df[time_col] == 1]
    treated_post = post_data[post_data[treatment_col] == 1][outcome_col].mean()
    control_post = post_data[post_data[treatment_col] == 0][outcome_col].mean()

    # Estimateur DiD
    did = (treated_post - treated_pre) - (control_post - control_pre)

    # Regression DiD avec variables de controle
    df['interaction'] = df[treatment_col] * df[time_col]
    model = smf.ols(
        f"{outcome_col} ~ {treatment_col} + {time_col} + interaction",
        data=df
    ).fit()

    print(f"Estimateur DiD: {did:.4f}")
    print(f"p-value (interaction): {model.pvalues['interaction']:.4f}")

    return did, model

```

---

## Uplift Modeling

### Principe et Cas d'Usage

L'uplift modeling mesure l'effet incremental d'une action sur des individus, permettant de cibler uniquement les individus qui "repondront" positivement a l'action (Persuadables) et d'eviter ceux qui auraient agi sans intervention (Sure Things) ou ceux sur qui l'action a un effet negatif (Sleeping Dogs).

```
Quatre types d'individus :
- Persuadables   : convertissent avec l'action, pas sans → CIBLER
- Sure Things    : convertissent de toute facon → pas la peine de cibler (gaspillage)
- Lost Causes    : ne convertissent pas quelle que soit l'action → ignorer
- Sleeping Dogs  : convertissent sans l'action mais pas avec → EVITER DE CIBLER
```

```python
from causalml.inference.meta import BaseXLearner
from sklearn.ensemble import GradientBoostingClassifier

# X-Learner : un des meilleurs meta-learners pour l'uplift

# Apres un A/B test, utiliser les donnees pour entrainer un modele d'uplift
# y : variable cible (ex: churn = 1)
# w : indicateur de traitement (1 = contact, 0 = controle)
# X : features des individus

learner = BaseXLearner(
    learner=GradientBoostingClassifier(n_estimators=100, random_state=42)
)

learner.fit(X_train, treatment=w_train, y=y_train)

# Predire l'uplift (effet causal individuel)
# Positif = l'action augmente la probabilite de l'evenement cible
# Negatif = l'action reduit la probabilite (Sleeping Dog)
uplift = learner.predict(X_test)

# Trier les individus par uplift decroissant pour cibler les Persuadables
results = pd.DataFrame({
    'customer_id': test_ids,
    'uplift_score': uplift.flatten(),
    'features': X_test.tolist()
}).sort_values('uplift_score', ascending=False)

# Cibler uniquement les N premiers avec le plus fort uplift positif
n_to_target = int(len(results) * 0.30)  # Top 30%
persuadables = results[results['uplift_score'] > 0].head(n_to_target)
```

### Evaluation de l'Uplift Modeling

```python
def qini_coefficient(y_true, uplift, treatment):
    """
    Calcule le Qini Coefficient — metrique principale pour l'uplift modeling.
    Un Qini > 0 indique que le modele est meilleur que le ciblage aleatoire.
    """
    from causalml.metrics import qini_score
    return qini_score(y_true, uplift, treatment)

# Courbe d'uplift cumulative
def plot_uplift_curve(y_true, uplift, treatment):
    """
    Visualise la courbe d'uplift cumulatif.
    La courbe ideale monte steeply puis se stabilise.
    """
    from causalml.metrics import plot_qini
    plot_qini(y_true, uplift, treatment)
```

---

## Glossaire de l'Experimentation

| Terme | Definition |
|-------|-----------|
| **A/B Test (RCT)** | Randomized Controlled Trial — experience ou les individus sont assignes aleatoirement au groupe controle ou traitement. |
| **p-value** | Probabilite d'observer un resultat aussi extreme si l'hypothese nulle (pas d'effet) est vraie. Pas la probabilite que l'effet soit reel. |
| **Niveau de confiance** | 1 - alpha. Un IC a 95% contient le vrai parametre dans 95% des cas si on repete l'experience. |
| **Puissance statistique** | Probabilite de detecter un vrai effet. 80% = on manque 20% des vrais effets. |
| **MDE** | Minimum Detectable Effect — la plus petite difference qu'on peut detecter avec une puissance donnee. |
| **Peeking Problem** | Biais introduit en regardant les resultats avant la fin du test et en arretant quand on voit p < 0.05. |
| **SRM** | Sample Ratio Mismatch — les groupes ne sont pas dans la proportion attendue, signal d'un probleme d'implementation. |
| **DiD** | Difference-in-Differences — methode causale comparant l'evolution de groupes traites et controles avant/apres. |
| **Uplift Modeling** | Prediction de l'effet causal individuel d'une action, pour cibler uniquement les Persuadables. |
| **Novelty Effect** | Biais d'un test provenant de la reponse positive des utilisateurs a la nouveaute, qui disparait avec le temps. |
| **CUPED** | Controlled-Experiment using Pre-Experiment Data — technique reduisant la variance en utilisant des covariates pre-test. |
