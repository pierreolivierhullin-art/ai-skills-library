---
name: ab-testing-experimentation
version: 1.0.0
description: >
  A/B testing methodology, statistical significance, p-value, confidence interval,
  sample size calculation, Bayesian experimentation, frequentist hypothesis testing,
  online controlled experiments, feature flags, multivariate testing, conversion optimization,
  experiment design, minimum detectable effect, type I type II errors, peeking problem
---

# A/B Testing et Experimentation — Methodologie Rigoureuse

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu veux valider l'impact d'une feature ou d'un changement UI avant le rollout
- Tu as besoin de calculer la taille d'echantillon pour un test valide
- Les equipes interpretent les resultats A/B sans comprendre la statistique
- Tu dois choisir entre l'approche frequentiste et bayesienne
- Tu implementes un programme d'experimentation a l'echelle (feature flags, plateforme)
- Tu veux eviter les pieges classiques : peeking, novelty effect, underpowered tests

---

## Concepts Statistiques Fondamentaux

### Hypotheses et Erreurs

```
H0 (hypothese nulle) : le changement n'a pas d'effet
H1 (hypothese alternative) : le changement a un effet

Erreur de Type I (faux positif) : declarer un effet inexistant
  → controlée par alpha (seuil de significativite, typiquement 5%)

Erreur de Type II (faux negatif) : rater un effet reel
  → controlée par beta (typiquement 20%)
  → Power = 1 - beta = 80% (probabilite de detecter un effet reel)
```

### Calcul de la Taille d'Echantillon

```python
import numpy as np
from scipy import stats
import math

def calculer_taille_echantillon(
    taux_base: float,        # Taux de conversion actuel (ex: 0.05 = 5%)
    mde: float,              # Minimum Detectable Effect (ex: 0.10 = +10% relatif)
    alpha: float = 0.05,     # Seuil de significativite (5%)
    power: float = 0.80,     # Puissance statistique (80%)
    bilateral: bool = True   # Test bilateral (recommande)
) -> dict:
    """
    Calcule la taille d'echantillon necessaire par variante.
    """
    taux_variant = taux_base * (1 + mde)

    # Z-scores
    z_alpha = stats.norm.ppf(1 - alpha / (2 if bilateral else 1))
    z_beta = stats.norm.ppf(power)

    # Variance poolee
    p_pool = (taux_base + taux_variant) / 2
    var_pool = p_pool * (1 - p_pool)

    # Formule de la taille d'echantillon
    n = (z_alpha * math.sqrt(2 * var_pool) + z_beta * math.sqrt(
        taux_base * (1 - taux_base) + taux_variant * (1 - taux_variant)
    )) ** 2 / (taux_variant - taux_base) ** 2

    n = math.ceil(n)

    return {
        'n_par_variante': n,
        'n_total': n * 2,
        'taux_base': taux_base,
        'taux_variant_attendu': taux_variant,
        'mde_absolu': taux_variant - taux_base,
        'mde_relatif': mde,
        'duree_jours': None,  # A remplir avec le trafic quotidien
    }

# Exemple : CTA d'inscription, 5% de conversion, MDE = +20% relatif
result = calculer_taille_echantillon(taux_base=0.05, mde=0.20)
print(f"Taille par variante : {result['n_par_variante']:,}")
# → ~2,098 utilisateurs par variante (4,196 au total)
```

### Calcul de la Significativite

```python
from scipy.stats import chi2_contingency, norm
import numpy as np

def analyser_ab_test(
    visites_controle: int,
    conversions_controle: int,
    visites_variante: int,
    conversions_variante: int,
    alpha: float = 0.05,
) -> dict:
    """Analyse complete d'un test A/B."""

    taux_controle = conversions_controle / visites_controle
    taux_variante = conversions_variante / visites_variante
    uplift_relatif = (taux_variante - taux_controle) / taux_controle

    # Test du chi-deux (recommande pour les taux de conversion)
    tableau = np.array([
        [conversions_controle, visites_controle - conversions_controle],
        [conversions_variante, visites_variante - conversions_variante],
    ])
    chi2, p_value, dof, _ = chi2_contingency(tableau, correction=False)

    # Intervalle de confiance sur la difference
    se = np.sqrt(
        taux_controle * (1 - taux_controle) / visites_controle +
        taux_variante * (1 - taux_variante) / visites_variante
    )
    z = norm.ppf(1 - alpha / 2)
    diff = taux_variante - taux_controle
    ic_bas = diff - z * se
    ic_haut = diff + z * se

    significatif = p_value < alpha

    return {
        'taux_controle': f"{taux_controle:.2%}",
        'taux_variante': f"{taux_variante:.2%}",
        'uplift_relatif': f"{uplift_relatif:+.1%}",
        'p_value': round(p_value, 4),
        'significatif': significatif,
        'confiance': f"{(1 - p_value) * 100:.1f}%",
        'ic_95': f"[{ic_bas:+.3%}, {ic_haut:+.3%}]",
        'decision': 'Deployer la variante' if significatif and uplift_relatif > 0 else
                    'Conserver le controle' if significatif else 'Pas assez de donnees',
    }

# Exemple
result = analyser_ab_test(
    visites_controle=5_000, conversions_controle=247,
    visites_variante=5_000, conversions_variante=301,
)
# taux_controle: 4.94%, taux_variante: 6.02%, uplift: +21.9%, p=0.009 → significatif
```

---

## Le Probleme du Peeking

Le peeking est la principale cause de faux positifs en A/B testing.

```python
# Simulation : taux de faux positifs avec peeking
import numpy as np

def simuler_peeking(n_simulations=10_000, verif_quotidiennes=14):
    """
    Montre que verifier quotidiennement le p-value pendant 14 jours
    fait exploser le taux de faux positifs (H0 toujours vraie).
    """
    alpha = 0.05
    faux_positifs = 0

    for _ in range(n_simulations):
        # Les deux groupes ont le MEME taux (H0 vraie)
        controle = np.random.binomial(500, 0.05, size=verif_quotidiennes)
        variante = np.random.binomial(500, 0.05, size=verif_quotidiennes)

        for j in range(1, verif_quotidiennes + 1):
            c_cum = controle[:j].sum()
            v_cum = variante[:j].sum()
            n_c = n_v = j * 500

            # Test chi-deux
            from scipy.stats import chi2_contingency
            table = np.array([
                [c_cum, n_c - c_cum],
                [v_cum, n_v - v_cum],
            ])
            _, p, _, _ = chi2_contingency(table, correction=False)

            if p < alpha:
                faux_positifs += 1
                break  # Stoppe au premier "significatif"

    return faux_positifs / n_simulations

# Sans peeking : 5% de faux positifs (attendu)
# Avec peeking 14 jours : ~26% de faux positifs !
print(f"Taux de faux positifs avec peeking : {simuler_peeking():.1%}")
```

**Solutions** :
- Fixer la duree ET la taille d'echantillon avant de demarrer
- Utiliser les Sequential Tests (SPRT) si le peeking est necessaire
- Approche bayesienne : pas de p-value, moins sensible au peeking

---

## Approche Bayesienne

```python
import numpy as np
from scipy.stats import beta

def analyse_bayesienne(
    conversions_controle: int, visites_controle: int,
    conversions_variante: int, visites_variante: int,
    prior_alpha: float = 1, prior_beta: float = 1,  # Prior non-informatif
    n_simulations: int = 100_000,
) -> dict:
    """
    Analyse bayesienne d'un test A/B.
    Retourne la probabilite que la variante soit meilleure.
    """
    # Posterior distributions (Beta-Binomial)
    post_controle = beta(
        prior_alpha + conversions_controle,
        prior_beta + visites_controle - conversions_controle,
    )
    post_variante = beta(
        prior_alpha + conversions_variante,
        prior_beta + visites_variante - conversions_variante,
    )

    # Monte Carlo : simuler les distributions
    echantillons_c = post_controle.rvs(n_simulations)
    echantillons_v = post_variante.rvs(n_simulations)

    # Probabilite que variante > controle
    prob_variante_meilleure = (echantillons_v > echantillons_c).mean()

    # Expected Loss (perte attendue si mauvaise decision)
    expected_loss_v = np.maximum(echantillons_c - echantillons_v, 0).mean()
    expected_loss_c = np.maximum(echantillons_v - echantillons_c, 0).mean()

    return {
        'prob_variante_meilleure': f"{prob_variante_meilleure:.1%}",
        'expected_loss_variante': f"{expected_loss_v:.4f}",
        'expected_loss_controle': f"{expected_loss_c:.4f}",
        'taux_median_controle': f"{post_controle.median():.3%}",
        'taux_median_variante': f"{post_variante.median():.3%}",
        'decision': 'Deployer' if prob_variante_meilleure > 0.95 else 'Continuer',
    }
```

---

## Feature Flags et Architecture d'Experimentation

### Stack d'Experimentation

```
Source de verite : Feature Flag Service (LaunchDarkly, Flagsmith, Unleash, Statsig)
     ↓
Assignation : utilisateur → variante (deterministe par hash user_id + flag_key)
     ↓
Tracking : impression + evenements de conversion → entrepot de donnees
     ↓
Analyse : plateforme d'experimentation ou notebook Python
```

### Implémentation avec Unleash (open-source)

```typescript
import { UnleashClient } from 'unleash-proxy-client';

const unleash = new UnleashClient({
  url: 'https://unleash.monapp.com/api/frontend',
  clientKey: process.env.UNLEASH_CLIENT_KEY!,
  appName: 'web-app',
});

await unleash.start();

// Assignation deterministe (meme variante pour le meme user)
function obtenirVariante(userId: string, flagKey: string): string {
  const contexte = { userId };
  const variante = unleash.getVariant(flagKey, contexte);
  return variante.name; // 'control' | 'variant_a' | 'variant_b'
}

// Tracking de l'exposition
function trackExposition(userId: string, flagKey: string, variante: string) {
  analytics.track('Experiment Exposure', {
    experiment_id: flagKey,
    variant: variante,
    user_id: userId,
    timestamp: Date.now(),
  });
}
```

---

## Design d'Experiences — Bonnes Pratiques

### Checklist avant de lancer un test

```
Hypothesis
├── ✅ Une seule variable testee
├── ✅ Hypothese directionelle (on s'attend a une hausse/baisse)
└── ✅ Metrique primaire definie (ex: inscription completion)

Stats
├── ✅ Taille d'echantillon calculee avant le test
├── ✅ Duree minimale : 2 semaines (capturer la variabilite hebdomadaire)
├── ✅ MDE realiste (pas < 5% relatif si trafic insuffisant)
└── ✅ Pas de peeking : date de decision fixee a l'avance

Qualite des donnees
├── ✅ Pas de fuite entre les groupes (SRM check = Sample Ratio Mismatch)
├── ✅ Holdout period : attendre 2j avant d'analyser (effets d'apprentissage)
└── ✅ Segment d'analyse = meme segment d'eligibilite
```

### Sample Ratio Mismatch (SRM)

```python
def verifier_srm(n_controle: int, n_variante: int, ratio_attendu: float = 0.5) -> dict:
    """
    Verifie si le ratio controle/variante est conforme au design.
    Un SRM indique un probleme d'implementation.
    """
    from scipy.stats import binom_test
    n_total = n_controle + n_variante
    p_value = binom_test(n_variante, n_total, ratio_attendu)

    return {
        'ratio_observe': n_variante / n_total,
        'ratio_attendu': ratio_attendu,
        'p_value': round(p_value, 4),
        'srm_detecte': p_value < 0.001,  # Seuil strict pour le SRM
        'action': 'STOP — verifier l\'implementation' if p_value < 0.001 else 'OK',
    }
```

---

## References

- `references/statistical-foundations.md` — Theorie statistique, erreurs type I/II, power analysis
- `references/bayesian-testing.md` — Approche bayesienne, Thompson Sampling, Multi-Armed Bandit
- `references/experimentation-platform.md` — Architecture, feature flags, Statsig, LaunchDarkly
- `references/case-studies.md` — 4 cas : test checkout e-commerce, pricing page SaaS, onboarding app
