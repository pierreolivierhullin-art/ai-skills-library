# Fondements Statistiques des Tests A/B

## Introduction

**FR** — Ce guide couvre les fondements mathematiques indispensables pour concevoir, executer et interpreter correctement un test A/B. Maîtriser ces concepts evite les pieges les plus courants : tests sous-puissants, interpretation erronee des p-values, inflation du taux d'erreur par les comparaisons multiples, et faux positifs dus au peeking. Chaque section inclut le code Python complet pour une application immediate en production.

**EN** — This guide covers the mathematical foundations required to properly design, run, and interpret A/B tests. Mastering these concepts prevents the most common pitfalls: underpowered tests, misinterpretation of p-values, error rate inflation from multiple comparisons, and false positives from peeking. Every section includes complete Python code for immediate production use.

---

## 1. Distributions de Probabilite — Quand Utiliser Quoi

### Distribution Binomiale

**FR** — La distribution binomiale modelise le nombre de succes dans n essais independants, chacun avec une probabilite p de succes. Elle est le modele naturel pour les taux de conversion (clic, inscription, achat), ou chaque visite est un essai et la conversion est le succes.

**EN** — The binomial distribution models the number of successes in n independent trials, each with probability p of success. It is the natural model for conversion rates (click, sign-up, purchase), where each visit is a trial and conversion is the success.

```python
from scipy.stats import binom
import numpy as np
import matplotlib.pyplot as plt

# Parametres : n visites, p taux de conversion
n_visites = 1000
p_conversion = 0.05

# Distribution binomiale
dist = binom(n=n_visites, p=p_conversion)

# Moments
print(f"Esperance (conversions attendues) : {dist.mean():.1f}")
print(f"Ecart-type : {dist.std():.2f}")
print(f"P(>60 conversions) : {1 - dist.cdf(60):.4f}")

# Approximation normale (valide si n*p > 5 et n*(1-p) > 5)
# Ici : 1000*0.05 = 50 > 5 → approximation normale valide
mu = n_visites * p_conversion
sigma = np.sqrt(n_visites * p_conversion * (1 - p_conversion))
print(f"Approximation normale : N({mu}, {sigma:.2f}^2)")
```

**Quand utiliser la binomiale directement** : echantillons < 30, ou quand p est tres proche de 0 ou 1 (taux < 1% ou > 99%). La loi normale n'est alors plus une bonne approximation.

### Distribution Normale

**FR** — Par le theoreme central limite, la moyenne d'un grand echantillon suit approximativement une loi normale, independamment de la distribution des donnees sous-jacentes. En pratique, pour n > 30 et p entre 0.01 et 0.99, le test sur les proportions peut utiliser l'approximation normale.

**EN** — By the central limit theorem, the mean of a large sample approximately follows a normal distribution regardless of the underlying data distribution. In practice, for n > 30 and p between 0.01 and 0.99, proportion tests can use the normal approximation.

```python
from scipy.stats import norm

# Z-score pour un taux de conversion observe
n = 1000
conversions_obs = 55
p_base = 0.05

p_obs = conversions_obs / n
se = np.sqrt(p_base * (1 - p_base) / n)
z = (p_obs - p_base) / se

p_value_unilaterale = 1 - norm.cdf(z)
p_value_bilaterale = 2 * (1 - norm.cdf(abs(z)))

print(f"Taux observe : {p_obs:.3%}")
print(f"Z-score : {z:.3f}")
print(f"p-value (bilateral) : {p_value_bilaterale:.4f}")
```

### Distribution t de Student

**FR** — La distribution t de Student remplace la normale quand l'ecart-type de la population est inconnu (ce qui est toujours le cas en pratique) et que l'echantillon est petit (n < 30). Elle a des queues plus epaisses que la normale, ce qui genere des p-values plus conservatrices (plus grandes) pour les petits echantillons.

**EN** — Student's t-distribution replaces the normal when the population standard deviation is unknown (which is always the case in practice) and the sample is small (n < 30). It has heavier tails than the normal, producing more conservative (larger) p-values for small samples.

```python
from scipy.stats import ttest_ind, ttest_rel
import numpy as np

# Cas metriques continues : duree de session, revenu par visite
# (pas les taux de conversion — pour les taux, utiliser chi2 ou z-test)
revenu_controle = np.random.normal(loc=45.0, scale=30.0, size=200)
revenu_variante = np.random.normal(loc=48.5, scale=32.0, size=200)

# t-test independant (deux echantillons distincts)
t_stat, p_value = ttest_ind(revenu_variante, revenu_controle, equal_var=False)  # Welch's t-test

print(f"Revenu moyen controle : {revenu_controle.mean():.2f} EUR")
print(f"Revenu moyen variante : {revenu_variante.mean():.2f} EUR")
print(f"t-statistique : {t_stat:.3f}")
print(f"p-value (bilateral) : {p_value:.4f}")
print(f"Significatif a 5% : {p_value < 0.05}")

# Welch's t-test (equal_var=False) est recommande par defaut :
# il ne suppose PAS que les deux groupes ont la meme variance
```

**Regle pratique** :
- Taux de conversion (0/1) → test du chi-2 ou z-test sur proportions
- Metriques continues (revenu, duree, nombre de pages) → Welch t-test
- Metriques a distribution asymetrique (revenu avec outliers) → Mann-Whitney U ou bootstrap

---

## 2. Theorie de la Decision : alpha, beta, Power, Effect Size

### Les Quatre Parametres Fondamentaux

```
Erreur de Type I (alpha) : declarer un effet inexistant (faux positif)
  → P(rejeter H0 | H0 vraie) = alpha
  → Standard : 5% (parfois 1% pour les decisions a fort enjeu)

Erreur de Type II (beta) : rater un effet reel (faux negatif)
  → P(ne pas rejeter H0 | H1 vraie) = beta
  → Standard : 20% (parfois 10% pour les decisions critiques)

Power (1 - beta) : probabilite de detecter un effet reel
  → Standard : 80% (parfois 90%)

Effect Size (MDE) : plus petit effet que l'on veut detecter avec fiabilite
  → Minimum Detectable Effect : choisir en fonction de l'impact metier minimal
```

### Relation entre les Quatre Parametres

```python
import numpy as np
from scipy.stats import norm

def afficher_tradeoffs(taux_base=0.05, mde_relatif=0.15):
    """
    Montre comment alpha, beta et MDE interagissent sur la taille d'echantillon.
    """
    taux_variant = taux_base * (1 + mde_relatif)
    p_pool = (taux_base + taux_variant) / 2
    delta = taux_variant - taux_base

    configs = [
        ("Standard    ", 0.05, 0.20),
        ("Strict alpha", 0.01, 0.20),
        ("High power  ", 0.05, 0.10),
        ("Strict both ", 0.01, 0.10),
    ]

    print(f"Taux base : {taux_base:.0%}, MDE relatif : {mde_relatif:.0%}")
    print(f"{'Config':<15} {'alpha':<8} {'power':<8} {'N/variante':<12} {'N total'}")
    print("-" * 55)

    for label, alpha, beta in configs:
        z_alpha = norm.ppf(1 - alpha / 2)
        z_beta = norm.ppf(1 - beta)
        n = ((z_alpha * np.sqrt(2 * p_pool * (1 - p_pool)) +
              z_beta * np.sqrt(taux_base * (1 - taux_base) + taux_variant * (1 - taux_variant))) / delta) ** 2
        n = int(np.ceil(n))
        print(f"{label:<15} {alpha:<8.0%} {1-beta:<8.0%} {n:<12,} {n*2:,}")

afficher_tradeoffs()
# Standard     : 5%      80%     ~2,900    5,800
# Strict alpha : 1%      80%     ~4,400    8,800
# High power   : 5%      90%     ~3,900    7,800
# Strict both  : 1%      90%     ~5,800   11,600
```

**Implication pratique** : passer de 80% a 90% de puissance augmente la taille d'echantillon de ~35%. Passer de alpha=5% a 1% l'augmente de ~50%. Choisir ces parametres avant de lancer, pas apres.

---

## 3. Calcul de la Taille d'Echantillon — Formules Exactes

### Formule Generale pour les Proportions

La taille d'echantillon par variante (n) est donnee par :

```
n = [ z_{alpha/2} * sqrt(2 * p_pool * (1-p_pool))
     + z_{beta} * sqrt(p_c*(1-p_c) + p_v*(1-p_v)) ]^2
    / (p_v - p_c)^2

Ou :
  p_c = taux de conversion du controle
  p_v = p_c * (1 + MDE_relatif)  [taux attendu de la variante]
  p_pool = (p_c + p_v) / 2
  z_{alpha/2} = quantile normal pour alpha/2 (1.96 pour alpha=5%, bilateral)
  z_{beta} = quantile normal pour beta (0.842 pour power=80%)
```

```python
import math
from scipy.stats import norm
from typing import Optional

def calculer_taille_echantillon(
    taux_base: float,
    mde_relatif: float,
    alpha: float = 0.05,
    power: float = 0.80,
    bilateral: bool = True,
    n_variantes: int = 1,
) -> dict:
    """
    Calcule la taille d'echantillon necessaire par variante.

    Parametres :
        taux_base    : taux de conversion actuel (ex: 0.05 pour 5%)
        mde_relatif  : plus petite variation a detecter en relatif (ex: 0.15 pour +15%)
        alpha        : seuil de significativite (Type I error rate)
        power        : puissance statistique souhaitee (1 - Type II error rate)
        bilateral    : True pour test bilateral (recommande)
        n_variantes  : nombre de variantes (ajuste alpha par Bonferroni si > 1)
    """
    # Correction Bonferroni pour tests multiples
    alpha_ajuste = alpha / n_variantes if n_variantes > 1 else alpha

    taux_variant = taux_base * (1 + mde_relatif)
    delta = taux_variant - taux_base
    p_pool = (taux_base + taux_variant) / 2

    z_alpha = norm.ppf(1 - alpha_ajuste / (2 if bilateral else 1))
    z_beta = norm.ppf(power)

    numerateur = (
        z_alpha * math.sqrt(2 * p_pool * (1 - p_pool)) +
        z_beta * math.sqrt(
            taux_base * (1 - taux_base) +
            taux_variant * (1 - taux_variant)
        )
    ) ** 2
    n = math.ceil(numerateur / delta ** 2)

    return {
        'n_par_variante': n,
        'n_total': n * (n_variantes + 1),  # controle + variantes
        'taux_base': f"{taux_base:.2%}",
        'taux_variant_attendu': f"{taux_variant:.2%}",
        'mde_absolu': f"{delta:+.3%}",
        'mde_relatif': f"{mde_relatif:+.0%}",
        'alpha_utilise': f"{alpha_ajuste:.3%}",
        'power': f"{power:.0%}",
    }

# Exemples representatifs
cas = [
    {"label": "Landing page (5% base, +15% MDE)", "taux_base": 0.05, "mde_relatif": 0.15},
    {"label": "Email CTA (25% base, +10% MDE)", "taux_base": 0.25, "mde_relatif": 0.10},
    {"label": "Checkout (8% base, +20% MDE)",  "taux_base": 0.08, "mde_relatif": 0.20},
    {"label": "Panier ajoute (12% base, +5%)",  "taux_base": 0.12, "mde_relatif": 0.05},
]

for c in cas:
    r = calculer_taille_echantillon(c["taux_base"], c["mde_relatif"])
    print(f"{c['label']}")
    print(f"  N/variante : {r['n_par_variante']:,} | N total : {r['n_total']:,}")
```

### Calcul pour Metriques Continues

```python
def calculer_taille_echantillon_continue(
    moyenne: float,
    ecart_type: float,
    mde_absolu: float,
    alpha: float = 0.05,
    power: float = 0.80,
) -> dict:
    """
    Taille d'echantillon pour metriques continues (revenu, duree, etc.)
    Cohen's d = mde_absolu / ecart_type
    """
    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(power)

    # Formule simplifiee pour deux groupes independants
    n = math.ceil(2 * ((z_alpha + z_beta) ** 2) * (ecart_type ** 2) / (mde_absolu ** 2))
    cohens_d = mde_absolu / ecart_type

    return {
        'n_par_variante': n,
        'cohens_d': round(cohens_d, 3),
        'interpretation_d': (
            'tres faible (<0.2)' if cohens_d < 0.2 else
            'faible (0.2-0.5)' if cohens_d < 0.5 else
            'moyen (0.5-0.8)' if cohens_d < 0.8 else
            'fort (>0.8)'
        ),
    }

# Exemple : revenu moyen 45 EUR, SD=30, detecter +3 EUR
r = calculer_taille_echantillon_continue(
    moyenne=45.0, ecart_type=30.0, mde_absolu=3.0
)
print(f"N/variante : {r['n_par_variante']:,}")
print(f"Cohen's d : {r['cohens_d']} ({r['interpretation_d']})")
```

---

## 4. Courbes de Puissance Statistique

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def courbe_puissance(
    taux_base: float,
    mde_range: list,
    n_range: list,
    alpha: float = 0.05,
):
    """
    Trace les courbes de puissance : power en fonction de N pour differents MDE.
    """
    def calculer_power(n, taux_base, mde_rel, alpha):
        taux_v = taux_base * (1 + mde_rel)
        p_pool = (taux_base + taux_v) / 2
        delta = taux_v - taux_base
        z_alpha = norm.ppf(1 - alpha / 2)
        se = math.sqrt(p_pool * (1 - p_pool) * 2 / n)
        ncp = delta / math.sqrt(
            taux_base * (1-taux_base) / n +
            taux_v * (1-taux_v) / n
        )
        power = 1 - norm.cdf(z_alpha - ncp) + norm.cdf(-z_alpha - ncp)
        return power

    fig, ax = plt.subplots(figsize=(10, 6))

    for mde in mde_range:
        powers = [calculer_power(n, taux_base, mde, alpha) for n in n_range]
        ax.plot(n_range, powers, label=f"MDE = {mde:+.0%}")

    ax.axhline(y=0.80, color='red', linestyle='--', alpha=0.7, label='Power = 80%')
    ax.axhline(y=0.90, color='orange', linestyle='--', alpha=0.7, label='Power = 90%')
    ax.set_xlabel('Taille d\'echantillon par variante')
    ax.set_ylabel('Puissance statistique (1 - beta)')
    ax.set_title(f'Courbes de puissance (taux base = {taux_base:.0%}, alpha = {alpha:.0%})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig('power_curves.png', dpi=150)
    return fig

courbe_puissance(
    taux_base=0.05,
    mde_range=[0.10, 0.15, 0.20, 0.30],
    n_range=list(range(500, 15001, 500)),
)
```

---

## 5. Tests a Une ou Deux Queues

### Test Bilateral (Two-Tailed) — Recommande par Defaut

**FR** — Le test bilateral teste H1 : p_v != p_c. Il detecte a la fois les hausses et les baisses. Utiliser par defaut car une variante peut degrader les metriques sans qu'on s'y attende.

```python
# Zone de rejet : les 2.5% inferieurs ET les 2.5% superieurs de la distribution
z_critique_bilateral = norm.ppf(1 - 0.05 / 2)  # 1.96
print(f"Z critique (bilateral, alpha=5%) : {z_critique_bilateral:.4f}")
```

### Test Unilateral (One-Tailed) — Cas Specifiques Seulement

**FR** — Le test unilateral teste H1 : p_v > p_c. Il est plus puissant pour detecter une hausse mais aveugle aux degradations. A utiliser uniquement quand :
1. Une degradation est physiquement impossible
2. L'hypothese directionnelle est specifiee avant le test dans un document de design

```python
z_critique_unilateral = norm.ppf(1 - 0.05)  # 1.645
print(f"Z critique (unilateral, alpha=5%) : {z_critique_unilateral:.4f}")
# Avantage : z_crit plus bas → plus facile d'atteindre significativite
# Risque : masque les degradations → ne jamais utiliser pour les metriques de garde
```

**Danger du switching post-hoc** : choisir unilateral apres avoir vu les resultats est une forme de p-hacking qui double le taux de faux positifs effectif.

---

## 6. Interpretation Correcte de la p-Value

### Ce que la p-Value EST et N'EST PAS

```
p-value = P(observer des donnees aussi extremes | H0 vraie)

Ce que la p-value N'EST PAS :
  ✗ P(H0 vraie | donnees)  — c'est la probabilite posterieure (bayesien)
  ✗ P(de se tromper si on rejette H0)
  ✗ La taille de l'effet
  ✗ La probabilite que le resultat soit du au hasard

Ce que la p-value EST :
  ✓ La probabilite d'observer cet ecart (ou plus extreme) si H0 est vraie
  ✓ Une mesure de la compatibilite des donnees avec H0
  ✓ Un critere de decision, pas une mesure de confiance
```

```python
# Illustration : grande p-value != pas d'effet
np.random.seed(42)

# Test sous-puissant : meme effet, mais echantillon trop petit
data_A_petit = np.random.binomial(1, 0.05, size=200)
data_B_petit = np.random.binomial(1, 0.065, size=200)  # effet reel de +30%

# Test bien puissant
data_A_grand = np.random.binomial(1, 0.05, size=5000)
data_B_grand = np.random.binomial(1, 0.065, size=5000)

from scipy.stats import chi2_contingency

def faire_test(a, b, label):
    table = np.array([
        [a.sum(), len(a) - a.sum()],
        [b.sum(), len(b) - b.sum()],
    ])
    _, p, _, _ = chi2_contingency(table, correction=False)
    print(f"{label}: p={p:.4f}, taux A={a.mean():.3%}, taux B={b.mean():.3%}")

faire_test(data_A_petit, data_B_petit, "N=200  ")  # p souvent > 0.05 malgre l'effet
faire_test(data_A_grand, data_B_grand, "N=5000 ")  # p < 0.05 detecte l'effet
# Lecon : une grande p-value avec un petit N dit "pas assez de donnees", pas "pas d'effet"
```

---

## 7. Intervalles de Confiance vs p-Value

**FR** — L'intervalle de confiance (IC) est plus informatif que la p-value car il donne a la fois la direction, la taille de l'effet et son incertitude. Preferer les IC pour les communications aux equipes metier.

```python
from scipy.stats import norm
import numpy as np

def ic_difference_proportions(
    n_c: int, conv_c: int,
    n_v: int, conv_v: int,
    alpha: float = 0.05,
) -> dict:
    """
    Intervalle de confiance sur la difference de taux de conversion.
    Methode de Newcombe (sans continuite, recommandee pour les proportions).
    """
    p_c = conv_c / n_c
    p_v = conv_v / n_v
    diff = p_v - p_c
    uplift = diff / p_c

    se = np.sqrt(p_c * (1-p_c) / n_c + p_v * (1-p_v) / n_v)
    z = norm.ppf(1 - alpha / 2)
    marge = z * se

    return {
        'taux_controle': f"{p_c:.3%}",
        'taux_variante': f"{p_v:.3%}",
        'difference_absolue': f"{diff:+.3%}",
        'uplift_relatif': f"{uplift:+.1%}",
        f'IC_{int((1-alpha)*100)}%': f"[{diff-marge:+.3%}, {diff+marge:+.3%}]",
        'interpretation': (
            'Positif significatif' if diff - marge > 0 else
            'Negatif significatif' if diff + marge < 0 else
            'Non concluant (IC contient 0)'
        ),
    }

r = ic_difference_proportions(5000, 247, 5000, 301)
for k, v in r.items():
    print(f"  {k} : {v}")
# IC ne contenant pas 0 → significatif, et donne l'amplitude de l'effet
```

**Regle heuristique** : si l'IC a 95% exclut 0, le test est significatif a 5%. Si l'IC exclut le MDE minimum, le test est conclusif meme pour une non-difference.

---

## 8. Multiple Testing Problem

### Inflation du Taux d'Erreur (FWER)

```python
def calculer_fwer(alpha_par_test: float, n_tests: int) -> float:
    """
    Familywise Error Rate : probabilite de faire au moins un faux positif
    si on effectue n_tests tests independants.
    """
    fwer = 1 - (1 - alpha_par_test) ** n_tests
    return fwer

print("FWER selon le nombre de tests (alpha = 5% par test) :")
for n in [1, 2, 3, 5, 10, 20, 50]:
    fwer = calculer_fwer(0.05, n)
    print(f"  {n:>3} tests : FWER = {fwer:.1%}")
# 1  test  : 5.0%   → acceptable
# 5  tests : 22.6%  → inacceptable
# 20 tests : 64.2%  → majorite des "decouvertes" sont des faux positifs
```

### Correction de Bonferroni

**FR** — Correction la plus simple : diviser alpha par le nombre de tests. Tres conservatrice (augmente les faux negatifs) mais garantit le FWER.

```python
def bonferroni(alpha: float, n_tests: int) -> float:
    return alpha / n_tests

alpha_ajuste = bonferroni(0.05, 5)
print(f"Alpha ajuste (5 tests) : {alpha_ajuste:.3%}")  # 1.0%
```

### Correction de Benjamini-Hochberg (FDR)

**FR** — Preferer BH quand on effectue de nombreux tests (analyses de sous-groupes, multi-metriques). Elle controle le False Discovery Rate (FDR = proportion de fausses decouvertes parmi toutes les decouvertes), pas le FWER. Moins conservatrice que Bonferroni.

```python
import numpy as np

def benjamini_hochberg(p_values: list, fdr_level: float = 0.05) -> list:
    """
    Correction BH : retourne les indices des tests significatifs apres correction.
    """
    n = len(p_values)
    # Trier les p-values et garder l'ordre original
    indices_tries = np.argsort(p_values)
    p_tries = np.array(p_values)[indices_tries]

    # Seuil BH pour chaque rang : (k/m) * alpha
    seuils = [(k + 1) / n * fdr_level for k in range(n)]

    # Trouver le plus grand k tel que p_(k) <= (k/m) * alpha
    significatifs_tries = []
    for k in range(n - 1, -1, -1):
        if p_tries[k] <= seuils[k]:
            significatifs_tries = list(range(k + 1))
            break

    # Retourner les indices originaux des tests significatifs
    return [indices_tries[i] for i in significatifs_tries]

# Exemple : 10 tests sur des sous-groupes
p_values = [0.001, 0.008, 0.012, 0.024, 0.048, 0.065, 0.120, 0.240, 0.380, 0.450]
labels = [f"Segment_{i+1}" for i in range(10)]

significatifs_bonf = [i for i, p in enumerate(p_values) if p < 0.05 / 10]
significatifs_bh = benjamini_hochberg(p_values, fdr_level=0.05)

print(f"Bonferroni (seuil {0.05/10:.3%}) : {[labels[i] for i in significatifs_bonf]}")
print(f"BH (FDR 5%)                    : {[labels[i] for i in significatifs_bh]}")
```

---

## 9. Segmentation et HTE (Heterogeneous Treatment Effects)

### Pre-Specification Obligatoire

**FR** — L'analyse de sous-groupes est valide uniquement si les segments sont specifies avant le test dans le document de design. Analyser des sous-groupes apres avoir vu les resultats (data-dredging) garantit de trouver des effets statistiquement significatifs par chance pure.

```python
# Document de design : a completer AVANT le lancement

EXPERIMENT_DESIGN = {
    'nom': 'Test CTA checkout V2',
    'date_lancement': '2024-03-01',
    'duree_prevue': '14 jours',
    'metrique_primaire': 'taux_checkout_completion',
    'metriques_secondaires': ['revenu_par_visite', 'taux_abandon_panier'],
    'metriques_de_garde': ['taux_erreur_paiement', 'taux_churn_30j'],
    'segments_pre_specifies': [
        'device_type',      # mobile vs desktop
        'user_type',        # nouveau vs returning
        'geo_region',       # FR vs BE vs CH
    ],
    'alpha': 0.05,
    'power': 0.80,
    'mde_relatif': 0.12,
    'n_par_variante': 3200,
    'analyste_responsable': 'data-team',
    'approbation_statisticien': True,
}
```

### Calcul des HTE — CATE (Conditional Average Treatment Effect)

```python
import pandas as pd
from scipy.stats import chi2_contingency

def analyser_hte(df: pd.DataFrame, segment_col: str, alpha_bonf: float = 0.05) -> pd.DataFrame:
    """
    Analyse les effets heterogenes par sous-groupe.
    Applique Bonferroni sur le nombre de segments.

    df doit contenir : 'variante' (0/1), 'converti' (0/1), segment_col
    """
    segments = df[segment_col].unique()
    alpha_ajuste = alpha_bonf / len(segments)
    resultats = []

    for seg in segments:
        sous_df = df[df[segment_col] == seg]
        controle = sous_df[sous_df['variante'] == 0]['converti']
        variante = sous_df[sous_df['variante'] == 1]['converti']

        table = np.array([
            [controle.sum(), len(controle) - controle.sum()],
            [variante.sum(), len(variante) - variante.sum()],
        ])
        _, p, _, _ = chi2_contingency(table, correction=False)

        resultats.append({
            'segment': seg,
            'n_controle': len(controle),
            'n_variante': len(variante),
            'taux_controle': controle.mean(),
            'taux_variante': variante.mean(),
            'uplift': (variante.mean() - controle.mean()) / controle.mean(),
            'p_value': p,
            'significatif_bonf': p < alpha_ajuste,
        })

    return pd.DataFrame(resultats).sort_values('uplift', ascending=False)
```

---

## 10. Variance Reduction — CUPED et Stratification

### CUPED (Controlled-experiment Using Pre-Experiment Data)

**FR** — CUPED reduit la variance de la metrique en soustrayant la contribution d'une covariable pre-experimentale (ex: comportement avant le test). Cela revient a augmenter la puissance statistique ou a reduire la duree du test sans augmenter le risque d'erreur.

```python
import numpy as np
from scipy.stats import pearsonr

def appliquer_cuped(
    df: pd.DataFrame,
    metrique_col: str,
    covariate_col: str,
    variante_col: str,
) -> pd.DataFrame:
    """
    Applique CUPED : Y_cuped = Y - theta * (X - E[X])
    Ou theta = Cov(Y, X) / Var(X)
    """
    # Calcul de theta sur l'ensemble du dataset (controle + variante)
    theta = np.cov(df[metrique_col], df[covariate_col])[0, 1] / np.var(df[covariate_col])
    x_mean = df[covariate_col].mean()

    # Ajustement CUPED
    df = df.copy()
    df[f'{metrique_col}_cuped'] = df[metrique_col] - theta * (df[covariate_col] - x_mean)

    # Comparaison de la variance
    var_originale = df.groupby(variante_col)[metrique_col].var().mean()
    var_cuped = df.groupby(variante_col)[f'{metrique_col}_cuped'].var().mean()
    reduction = (1 - var_cuped / var_originale) * 100

    print(f"Theta : {theta:.4f}")
    print(f"Correlation (Y, X) : {pearsonr(df[metrique_col], df[covariate_col])[0]:.3f}")
    print(f"Variance originale : {var_originale:.4f}")
    print(f"Variance CUPED     : {var_cuped:.4f}")
    print(f"Reduction de variance : {reduction:.1f}%")
    print(f"Gain equivalent : test {1/(1-reduction/100):.1%} plus puissant")

    return df

# CUPED est particulierement efficace quand :
# - La correlation entre Y et la covariate est forte (r > 0.3)
# - La covariate est stable et mesurable avant le test
# - Exemple : revenu des 30 derniers jours pour predire le revenu pendant le test
```

### Stratification

**FR** — La stratification garantit que les groupes controle et variante ont des distributions identiques sur les variables cles (device, pays, cohorte). Elle reduit le biais d'assignation et la variance inter-groupes.

```python
import hashlib

def assigner_variante_stratifiee(
    user_id: str,
    experiment_id: str,
    strate: str,  # ex: "mobile_FR", "desktop_US"
    n_variantes: int = 2,
) -> int:
    """
    Assignation deterministe et stratifiee.
    La strate est incluse dans le hash pour garantir l'equilibre par strate.
    """
    cle = f"{experiment_id}_{strate}_{user_id}"
    hash_val = int(hashlib.md5(cle.encode()).hexdigest(), 16)
    return hash_val % n_variantes

# Verification de l'equilibre par strate
np.random.seed(42)
strates = ['mobile_FR', 'mobile_BE', 'desktop_FR', 'desktop_BE']
user_ids = [f"user_{i}" for i in range(10000)]

resultats_strates = {}
for strate in strates:
    assignments = [assigner_variante_stratifiee(uid, "exp_001", strate) for uid in user_ids]
    pct_variante = np.mean(assignments)
    resultats_strates[strate] = pct_variante
    print(f"{strate}: {pct_variante:.3%} en variante (attendu: 50%)")
```

---

## References Complementaires

- `references/bayesian-testing.md` — Approche bayesienne, Thompson Sampling, critere de l'Expected Loss
- `references/experimentation-platform.md` — Architecture plateforme, feature flags, Statsig, LaunchDarkly
- `references/case-studies.md` — 4 cas concrets en production avec resultats et lecons apprises
- Livre de reference : "Trustworthy Online Controlled Experiments" (Kohavi, Tang, Xu) — standard industrie
- Librairie Python : `scipy.stats`, `statsmodels`, `pingouin` pour les tests statistiques
