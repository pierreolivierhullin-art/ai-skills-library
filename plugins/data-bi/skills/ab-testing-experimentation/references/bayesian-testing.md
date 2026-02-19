# Tests Bayesiens et Multi-Armed Bandit

## Introduction

**FR** — Ce guide couvre l'approche bayesienne pour l'experimentation et les algorithmes d'optimisation adaptative. Contrairement au cadre frequentiste, l'inference bayesienne produit des distributions de probabilite sur les parametres inconnus plutot que des p-values. Cette difference philosophique a des implications pratiques majeures : meilleure tolerabilite au peeking, communication naturelle de l'incertitude, et possibilite d'implementer des bandits multi-bras pour l'optimisation continue. Le code Python complet couvre PyMC, scipy et des implementations from-scratch.

**EN** — This guide covers the Bayesian approach to experimentation and adaptive optimization algorithms. Unlike the frequentist framework, Bayesian inference produces probability distributions over unknown parameters rather than p-values. This philosophical difference has major practical implications: better tolerance to peeking, natural uncertainty communication, and the ability to implement multi-armed bandits for continuous optimization.

---

## 1. Paradigme Bayesien vs Frequentiste

### Philosophie et Implications Pratiques

```
FREQUENTISTE                          | BAYESIEN
--------------------------------------|---------------------------------------
Question : P(donnees | H0)            | Question : P(theta | donnees)
→ "Si H0 vraie, quelle proba         | → "Apres avoir vu les donnees,
  d'observer ces donnees ?"           |   que croit-on sur le parametre ?"
                                      |
Parametre : fixe, inconnu             | Parametre : variable aleatoire
Prior : aucun (H0 comme reference)    | Prior : distribution sur theta
Sortie : p-value, IC frequentiste     | Sortie : distribution posterieure
Decision : rejeter/ne pas rejeter H0  | Decision : action basee sur loss function
                                      |
Peeking : invalide (gonfle alpha)     | Peeking : valide (le posterior s'update)
Taille echantillon : fixe a l'avance  | Taille : peut s'arreter sur critere metier
Interpretation : delicate (voir §6)   | Interpretation : intuitive
Outils Python : scipy.stats           | Outils : PyMC, arviz, bambi, scipy.stats.beta
```

### Quand Choisir Bayesien vs Frequentiste

```python
# Arbre de decision : approche recommandee

def choisir_approche(
    taille_echantillon_disponible: str,  # "petite", "moyenne", "grande"
    tolerance_peeking: bool,
    contrainte_reglementaire: bool,
    equipe_familiere_bayesien: bool,
) -> str:
    """
    Recommandation d'approche statistique selon le contexte.
    """
    if contrainte_reglementaire:
        return "frequentiste (norme industrie pour les soumissions reglementaires)"
    if taille_echantillon_disponible == "petite":
        return "bayesien (meilleure utilisation de l'information prior)"
    if tolerance_peeking:
        return "bayesien (ou SPRT frequentiste si contrainte de rapport)"
    if equipe_familiere_bayesien:
        return "bayesien (communication plus intuitive)"
    return "frequentiste (plus simple, bien etabli, outillage abondant)"
```

---

## 2. Modele Beta-Binomial Conjugue

### Le Prior Beta

**FR** — Pour les taux de conversion (variables binaires), la distribution Beta est le prior conjugue de la vraisemblance binomiale. "Conjugue" signifie que le posterior a la meme forme que le prior, ce qui permet un calcul analytique (sans simulation).

```python
from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt

# Distribution Beta(alpha, beta)
# alpha = nombre de succes + 1
# beta  = nombre d'echecs + 1
# E[theta] = alpha / (alpha + beta)
# Variance = alpha*beta / [(alpha+beta)^2 * (alpha+beta+1)]

# Priors courants pour un taux de conversion
priors = {
    'Uniforme (non informatif)': beta(1, 1),
    'Faiblement informatif (5% attendu)': beta(5, 95),
    'Informatif (historique 3 mois)': beta(150, 2850),  # 150 conv sur 3000
}

x = np.linspace(0, 0.15, 1000)
fig, ax = plt.subplots(figsize=(10, 5))

for label, dist in priors.items():
    ax.plot(x, dist.pdf(x), label=f"{label} (E={dist.mean():.2%})")

ax.set_xlabel('Taux de conversion theta')
ax.set_ylabel('Densite a posteriori')
ax.set_title('Comparaison des priors Beta pour un taux de conversion')
ax.legend()
plt.savefig('beta_priors.png', dpi=150)
```

### Update Bayesien — Step by Step

```python
def update_bayesien(
    alpha_prior: float,
    beta_prior: float,
    conversions: int,
    visites: int,
) -> tuple:
    """
    Update bayesien pour un taux de conversion.

    Posterior = Beta(alpha_prior + conversions, beta_prior + non_conversions)

    Propriete conjuguee : si Prior ~ Beta(a, b) et Vraisemblance ~ Binomial(n, theta)
    alors Posterior ~ Beta(a + conversions, b + non_conversions)
    """
    non_conversions = visites - conversions
    alpha_post = alpha_prior + conversions
    beta_post = beta_prior + non_conversions
    return alpha_post, beta_post

# Simulation d'accumulation de donnees
np.random.seed(42)
true_rate = 0.063
n_jours = 14
visites_par_jour = 200

alpha_prior, beta_prior = 1, 1  # Prior uniforme

print(f"{'Jour':<6} {'Visites':<10} {'Convs':<8} {'E[theta]':<12} {'IC 95%':<25} {'Mode'}")
print("-" * 70)

alpha, beta_p = alpha_prior, beta_prior
total_visites = 0
total_convs = 0

for jour in range(1, n_jours + 1):
    nouvelles_convs = np.random.binomial(visites_par_jour, true_rate)
    total_visites += visites_par_jour
    total_convs += nouvelles_convs

    alpha, beta_p = update_bayesien(alpha_prior, beta_prior, total_convs, total_visites)
    dist_post = beta(alpha, beta_p)

    ic_bas, ic_haut = dist_post.ppf([0.025, 0.975])
    mode = (alpha - 1) / (alpha + beta_p - 2) if alpha > 1 else 0

    print(f"{jour:<6} {total_visites:<10} {total_convs:<8} {dist_post.mean():.4%}    "
          f"[{ic_bas:.4%}, {ic_haut:.4%}]    {mode:.4%}")
```

---

## 3. Probabilite d'Etre Meilleur — Monte Carlo

### Calcul Analytique et Monte Carlo

```python
from scipy.stats import beta
import numpy as np

def probabilite_variante_meilleure(
    alpha_c: float, beta_c: float,  # Posterior controle
    alpha_v: float, beta_v: float,  # Posterior variante
    n_simulations: int = 200_000,
) -> dict:
    """
    Calcule P(theta_variante > theta_controle) par simulation Monte Carlo.

    Pour deux distributions Beta, il existe une formule analytique fermee,
    mais Monte Carlo est plus flexible et s'etend aux cas non-conjugues.
    """
    dist_c = beta(alpha_c, beta_c)
    dist_v = beta(alpha_v, beta_v)

    # Simulation Monte Carlo
    echant_c = dist_c.rvs(n_simulations)
    echant_v = dist_v.rvs(n_simulations)

    prob_v_meilleure = (echant_v > echant_c).mean()

    # Lift distribue : distribution de (theta_v - theta_c) / theta_c
    lift = (echant_v - echant_c) / echant_c
    lift_median = np.median(lift)
    lift_ic_bas, lift_ic_haut = np.percentile(lift, [2.5, 97.5])

    return {
        'prob_variante_meilleure': prob_v_meilleure,
        'prob_controle_meilleure': 1 - prob_v_meilleure,
        'lift_median': lift_median,
        'lift_ic_95': (lift_ic_bas, lift_ic_haut),
        'taux_median_controle': dist_c.median(),
        'taux_median_variante': dist_v.median(),
    }

# Exemple : test avec 5000 visites par groupe
# Controle : 247 conversions / 5000 → Prior Beta(1,1) + data = Beta(248, 4754)
# Variante  : 301 conversions / 5000 → Beta(302, 4700)
r = probabilite_variante_meilleure(248, 4754, 302, 4700)
print(f"P(variante meilleure) : {r['prob_variante_meilleure']:.2%}")
print(f"Lift median           : {r['lift_median']:+.1%}")
print(f"IC 95% du lift        : [{r['lift_ic_95'][0]:+.1%}, {r['lift_ic_95'][1]:+.1%}]")
```

---

## 4. Expected Loss — Critere de Decision

### Definition et Calcul

**FR** — L'Expected Loss (perte attendue) est le critere de decision bayesien le plus rigoureux. Elle mesure la perte esperee si on prend la mauvaise decision. Le seuil standard de 1% (0.01 en absolu sur le taux) est recommande par VWO et la litterature bayesienne.

```python
def expected_loss(
    alpha_c: float, beta_c: float,
    alpha_v: float, beta_v: float,
    n_simulations: int = 200_000,
) -> dict:
    """
    Calcule l'Expected Loss pour chaque decision possible.

    EL(choisir variante) = E[max(theta_c - theta_v, 0)]
      = perte attendue si on choisit la variante alors qu'elle est en realite pire

    EL(choisir controle) = E[max(theta_v - theta_c, 0)]
      = perte attendue si on garde le controle alors que la variante est meilleure
    """
    echant_c = beta(alpha_c, beta_c).rvs(n_simulations)
    echant_v = beta(alpha_v, beta_v).rvs(n_simulations)

    el_variante = np.maximum(echant_c - echant_v, 0).mean()  # Regretter d'avoir choisi V
    el_controle = np.maximum(echant_v - echant_c, 0).mean()  # Regretter d'avoir garde C

    seuil_decision = 0.001  # 0.1 point de % de taux de conversion
    decision = (
        'Deployer la variante' if el_variante < seuil_decision else
        'Conserver le controle' if el_controle < seuil_decision else
        'Continuer le test (incertitude trop elevee)'
    )

    return {
        'expected_loss_si_variante': el_variante,
        'expected_loss_si_controle': el_controle,
        'seuil_utilise': seuil_decision,
        'decision': decision,
    }

r = expected_loss(248, 4754, 302, 4700)
print(f"EL si on deploie variante  : {r['expected_loss_si_variante']:.5f}")
print(f"EL si on garde controle    : {r['expected_loss_si_controle']:.5f}")
print(f"Decision                   : {r['decision']}")
```

---

## 5. HDI vs IC Frequentiste

### Highest Density Interval (HDI)

**FR** — Le HDI bayesien est l'intervalle le plus court contenant X% de la masse de probabilite posterieure. Il s'interprete directement : "Il y a 95% de probabilite que le taux de conversion soit dans cet intervalle." L'IC frequentiste a 95% ne peut pas etre interprete ainsi.

```python
import numpy as np
from scipy.stats import beta

def calculer_hdi(distribution, credible_mass: float = 0.95, n_points: int = 10000) -> tuple:
    """
    Calcule le Highest Density Interval (HDI) pour une distribution Beta.
    """
    # Methode : trouver l'intervalle le plus court parmi tous les intervalles
    # de la meme largeur de probabilite
    x = np.linspace(distribution.ppf(0.001), distribution.ppf(0.999), n_points)
    dx = x[1] - x[0]
    pdf = distribution.pdf(x)

    # Trier par densite decroissante et accumuler jusqu'a credible_mass
    indices_tries = np.argsort(pdf)[::-1]
    cumul = 0
    dans_hdi = np.zeros(n_points, dtype=bool)

    for i in indices_tries:
        cumul += pdf[i] * dx
        dans_hdi[i] = True
        if cumul >= credible_mass:
            break

    # Extraire les bornes
    indices_hdi = np.where(dans_hdi)[0]
    return x[indices_hdi[0]], x[indices_hdi[-1]]

# Comparaison HDI vs IC frequentiste
alpha_post, beta_post = 302, 4700  # Posterior variante
dist = beta(alpha_post, beta_post)

hdi_bas, hdi_haut = calculer_hdi(dist, 0.95)
ic_bas, ic_haut = dist.ppf([0.025, 0.975])  # Intervalle de credibilite (equal-tailed)

print(f"HDI 95%   : [{hdi_bas:.4%}, {hdi_haut:.4%}] (intervalle le plus court)")
print(f"IC 95%    : [{ic_bas:.4%}, {ic_haut:.4%}] (equal-tailed)")
print(f"Largeur HDI : {(hdi_haut - hdi_bas):.4%}")
print(f"Largeur IC  : {(ic_haut - ic_bas):.4%}")
print()
print("Interpretation correcte du HDI :")
print(f"  'Il y a 95% de probabilite que le taux reel soit entre {hdi_bas:.3%} et {hdi_haut:.3%}'")
print()
print("Interpretation INCORRECTE de l'IC frequentiste :")
print("  'Il y a 95% de probabilite que le vrai taux soit dans l'IC' — FAUX")
print("  Correct : '95% des IC construits de cette facon contiennent le vrai parametre'")
```

---

## 6. Thompson Sampling — Exploration-Exploitation

### Principe et Implementation

**FR** — Thompson Sampling est un algorithme bayesien pour le probleme exploration-exploitation. A chaque iteration, on tire un echantillon de chaque distribution posterieure et on alloue le trafic a l'option avec l'echantillon le plus eleve. Naturellement, les options prometteuses recoivent plus de trafic et convergent plus vite.

```python
import numpy as np
from scipy.stats import beta
from typing import List
import matplotlib.pyplot as plt

class ThompsonSampling:
    """
    Thompson Sampling pour des taux de conversion (distribution Beta).
    Compatible avec un test A/B classique (2 variantes) ou multi-bras.
    """

    def __init__(self, n_bras: int, prior_alpha: float = 1.0, prior_beta: float = 1.0):
        self.n_bras = n_bras
        self.alphas = np.full(n_bras, prior_alpha, dtype=float)
        self.betas = np.full(n_bras, prior_beta, dtype=float)
        self.historique = {'n_tirages': np.zeros(n_bras), 'n_succes': np.zeros(n_bras)}

    def choisir_bras(self) -> int:
        """
        Tire un echantillon de chaque posterior et choisit l'argmax.
        """
        echantillons = [beta(a, b).rvs() for a, b in zip(self.alphas, self.betas)]
        return int(np.argmax(echantillons))

    def update(self, bras: int, succes: int, essais: int = 1):
        """
        Met a jour le posterior apres observation.
        succes : nombre de conversions
        essais : nombre de visites
        """
        echecs = essais - succes
        self.alphas[bras] += succes
        self.betas[bras] += echecs
        self.historique['n_tirages'][bras] += essais
        self.historique['n_succes'][bras] += succes

    @property
    def taux_observe(self) -> np.ndarray:
        n = self.historique['n_tirages']
        s = self.historique['n_succes']
        return np.where(n > 0, s / n, 0.0)

    @property
    def esperance_posterieure(self) -> np.ndarray:
        return self.alphas / (self.alphas + self.betas)

    def rapport(self) -> dict:
        return {
            f'bras_{i}': {
                'n_tirages': int(self.historique['n_tirages'][i]),
                'n_succes': int(self.historique['n_succes'][i]),
                'taux_observe': f"{self.taux_observe[i]:.3%}",
                'E[theta_posterieur]': f"{self.esperance_posterieure[i]:.3%}",
                'IC_95': beta(self.alphas[i], self.betas[i]).ppf([0.025, 0.975]),
            }
            for i in range(self.n_bras)
        }

# Simulation : 3 variantes, taux reels inconnus de l'algorithme
np.random.seed(42)
vrais_taux = [0.050, 0.065, 0.058]  # Variante B est la meilleure
ts = ThompsonSampling(n_bras=3)

n_iterations = 10_000
allocation_hist = np.zeros((n_iterations, 3))

for t in range(n_iterations):
    bras = ts.choisir_bras()
    succes = int(np.random.binomial(1, vrais_taux[bras]))
    ts.update(bras, succes)
    allocation_hist[t] = ts.historique['n_tirages']

print("Rapport final Thompson Sampling :")
for bras, info in ts.rapport().items():
    print(f"\n{bras} (vrai taux: {vrais_taux[int(bras.split('_')[1])]:.1%}):")
    for k, v in info.items():
        print(f"  {k}: {v}")

# Verification : le meilleur bras (B, indice 1) a recu le plus de trafic
allocation_finale = ts.historique['n_tirages'] / ts.historique['n_tirages'].sum()
print(f"\nAllocation finale : {allocation_finale}")
```

---

## 7. Multi-Armed Bandit — Comparaison des Algorithmes

### UCB1, Epsilon-Greedy et Thompson Sampling

```python
import numpy as np

class BanditEnvironment:
    """Environnement de simulation pour les algorithmes de bandit."""

    def __init__(self, vrais_taux: List[float]):
        self.vrais_taux = np.array(vrais_taux)
        self.n_bras = len(vrais_taux)
        self.meilleur_bras = np.argmax(vrais_taux)
        self.meilleur_taux = vrais_taux[self.meilleur_bras]

    def tirer(self, bras: int) -> int:
        return int(np.random.binomial(1, self.vrais_taux[bras]))

class UCB1:
    """Upper Confidence Bound 1 — garantie theorique de regret logarithmique."""

    def __init__(self, n_bras: int):
        self.n_bras = n_bras
        self.n_tirages = np.zeros(n_bras)
        self.recompenses = np.zeros(n_bras)
        self.t = 0

    def choisir_bras(self) -> int:
        self.t += 1
        # Au debut, tirer chaque bras une fois
        bras_non_tires = np.where(self.n_tirages == 0)[0]
        if len(bras_non_tires) > 0:
            return bras_non_tires[0]

        moyennes = self.recompenses / self.n_tirages
        bonus = np.sqrt(2 * np.log(self.t) / self.n_tirages)
        return int(np.argmax(moyennes + bonus))

    def update(self, bras: int, recompense: float):
        self.n_tirages[bras] += 1
        self.recompenses[bras] += recompense

class EpsilonGreedy:
    """Epsilon-Greedy — simple mais sous-optimal sur le long terme."""

    def __init__(self, n_bras: int, epsilon: float = 0.1):
        self.n_bras = n_bras
        self.epsilon = epsilon
        self.n_tirages = np.zeros(n_bras)
        self.recompenses = np.zeros(n_bras)

    def choisir_bras(self) -> int:
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_bras)  # Exploration
        moyennes = np.where(
            self.n_tirages > 0,
            self.recompenses / self.n_tirages,
            0
        )
        return int(np.argmax(moyennes))  # Exploitation

    def update(self, bras: int, recompense: float):
        self.n_tirages[bras] += 1
        self.recompenses[bras] += recompense

def comparer_algorithmes(vrais_taux: List[float], n_iterations: int = 20_000) -> dict:
    """Compare UCB1, Epsilon-Greedy et Thompson Sampling sur le meme environnement."""
    env = BanditEnvironment(vrais_taux)
    algos = {
        'Thompson Sampling': ThompsonSampling(len(vrais_taux)),
        'UCB1': UCB1(len(vrais_taux)),
        'Epsilon-Greedy (0.1)': EpsilonGreedy(len(vrais_taux), epsilon=0.1),
    }

    resultats = {nom: {'regret_cumule': [], 'recompenses': 0} for nom in algos}

    for nom, algo in algos.items():
        regret_cumule = 0
        for _ in range(n_iterations):
            bras = algo.choisir_bras()
            recompense = env.tirer(bras)
            algo.update(bras, recompense)
            regret_cumule += env.meilleur_taux - vrais_taux[bras]
            resultats[nom]['regret_cumule'].append(regret_cumule)
        resultats[nom]['regret_final'] = regret_cumule

    return resultats

vrais_taux = [0.05, 0.065, 0.058, 0.052, 0.049]
resultats = comparer_algorithmes(vrais_taux, n_iterations=15_000)

print(f"Regret cumule apres 15,000 iterations :")
for algo, r in sorted(resultats.items(), key=lambda x: x[1]['regret_final']):
    print(f"  {algo:<30}: {r['regret_final']:.1f}")
```

---

## 8. MAB vs A/B Classique — Quand Choisir

```
                    A/B CLASSIQUE              MULTI-ARMED BANDIT
--------------------------------------------------------------------
Objectif           Valider une hypothese       Maximiser la recompense
                   (inference)                 pendant le test (optimisation)

Allocations        Fixes (50/50 ou N-aire)     Adaptatives (favorise le meilleur)

Stabilite          Requiert un environnement   Peut s'adapter a la non-stationnarite
requise            stable                      (drift, saisonnalite)

Risque pendant     Accepte le cout de          Minimise les regrets pendant le test
le test            l'apprentissage

Interpretabilite  Facile : IC, p-value        Plus complexe : regret, allocation
des resultats

Cas d'usage        Decisions strategiques,     Optimisation continue, personnalisation,
ideaux             feature deployment,         pricing, contenu editorial, push notifs
                   UI/UX testing

Duree              Predeterminee               Peut tourner en continu

Biais d'adaptation Non (les deux groupes       Oui : les premiers utilisateurs sont
                   sont equivalents)           sous-representes dans les bons bras
```

---

## 9. Frameworks Python Bayesiens

### PyMC — Modelisation Probabiliste Complete

```python
import pymc as pm
import numpy as np
import arviz as az

# Modele A/B test bayesien avec PyMC
def ab_test_pymc(
    n_controle: int, conv_controle: int,
    n_variante: int, conv_variante: int,
    draws: int = 4000, chains: int = 2,
) -> az.InferenceData:

    with pm.Model() as model:
        # Priors non-informatifs sur les taux de conversion
        theta_c = pm.Beta('theta_controle', alpha=1, beta=1)
        theta_v = pm.Beta('theta_variante', alpha=1, beta=1)

        # Vraisemblances
        obs_c = pm.Binomial('obs_controle', n=n_controle, p=theta_c, observed=conv_controle)
        obs_v = pm.Binomial('obs_variante', n=n_variante, p=theta_v, observed=conv_variante)

        # Quantites derivees
        delta_abs = pm.Deterministic('delta_absolu', theta_v - theta_c)
        delta_rel = pm.Deterministic('delta_relatif', (theta_v - theta_c) / theta_c)
        variante_meilleure = pm.Deterministic('prob_variante_meilleure',
                                               pm.math.gt(theta_v, theta_c).astype(float))

        # Echantillonnage MCMC (NUTS par defaut)
        trace = pm.sample(draws=draws, chains=chains, progressbar=False,
                          return_inferencedata=True, random_seed=42)

    return trace, model

# Analyse du trace
trace, model = ab_test_pymc(5000, 247, 5000, 301)

print(az.summary(trace, var_names=['theta_controle', 'theta_variante', 'delta_absolu', 'delta_relatif']))
print(f"\nP(variante meilleure) : {trace.posterior['prob_variante_meilleure'].values.mean():.2%}")
```

### ArviZ — Visualisation et Diagnostics

```python
import arviz as az
import matplotlib.pyplot as plt

# Diagnostics de convergence MCMC
print("Diagnostics MCMC :")
print(f"  R-hat max : {az.rhat(trace).max().values:.4f}  (doit etre < 1.01)")
print(f"  ESS bulk min : {az.ess(trace, method='bulk').min().values:.0f}  (doit etre > 400)")

# Visualisations
az.plot_posterior(trace, var_names=['delta_relatif'], ref_val=0,
                  hdi_prob=0.95, figsize=(8, 4))
plt.title('Distribution posterieure du lift relatif')
plt.savefig('posterior_lift.png', dpi=150)

az.plot_forest(trace, var_names=['theta_controle', 'theta_variante'],
               combined=True, hdi_prob=0.95, figsize=(8, 4))
plt.title('HDI 95% des taux de conversion')
plt.savefig('forest_plot.png', dpi=150)
```

---

## 10. Cas d'Usage — Pricing Dynamique, Personnalisation, Recommandations

### Cas 1 : Optimisation du Timing des Push Notifications

```python
import numpy as np
from typing import Dict

class NotificationBandit:
    """
    MAB pour optimiser l'heure d'envoi des push notifications.
    5 bras : 8h, 10h, 12h, 18h, 20h
    """

    def __init__(self, heures: List[int]):
        self.heures = heures
        self.ts = ThompsonSampling(n_bras=len(heures))

    def choisir_heure(self, user_id: str) -> int:
        """Choisit l'heure optimale pour un utilisateur donne."""
        bras = self.ts.choisir_bras()
        return self.heures[bras], bras

    def enregistrer_resultat(self, bras: int, clique: bool):
        self.ts.update(bras, succes=int(clique))

    def rapport_par_heure(self) -> Dict:
        rapport = {}
        for i, heure in enumerate(self.heures):
            alpha = self.ts.alphas[i]
            b = self.ts.betas[i]
            n = int(self.ts.historique['n_tirages'][i])
            rapport[f"{heure}h"] = {
                'envois': n,
                'taux_clic_posterieur': f"{alpha/(alpha+b):.2%}",
                'pct_allocation': f"{n / max(self.ts.historique['n_tirages'].sum(), 1):.1%}",
            }
        return rapport

# Simulation sur 30 jours, 500 notifications/jour
np.random.seed(42)
heures = [8, 10, 12, 18, 20]
vrais_taux_clic = [0.04, 0.07, 0.05, 0.12, 0.09]  # 18h est le meilleur
bandit = NotificationBandit(heures)

for _ in range(30 * 500):
    heure, bras = bandit.choisir_heure(f"user_{np.random.randint(10000)}")
    clique = bool(np.random.binomial(1, vrais_taux_clic[bras]))
    bandit.enregistrer_resultat(bras, clique)

print("Rapport MAB - Optimisation timing notifications :")
for heure, stats in bandit.rapport_par_heure().items():
    print(f"  {heure} : {stats}")
```

### Cas 2 : Personnalisation du Prix d'Appel

```python
# Attention : les tests de prix sont soumis a des contraintes legales et ethiques
# Voir references/case-studies.md pour l'analyse complete

class PricingBandit:
    """
    MAB contextuel pour optimiser le prix d'appel par segment.
    IMPORTANT : completer une analyse legale avant toute implementation.
    """

    def __init__(self, prix: List[float], segments: List[str]):
        self.prix = prix
        self.segments = segments
        # Un modele separé par segment (contextuel)
        self.bandits = {
            seg: ThompsonSampling(n_bras=len(prix))
            for seg in segments
        }

    def recommander_prix(self, segment: str) -> float:
        if segment not in self.bandits:
            return self.prix[0]  # Prix par defaut
        bras = self.bandits[segment].choisir_bras()
        return self.prix[bras], bras

    def enregistrer_conversion(self, segment: str, bras: int, converti: bool):
        self.bandits[segment].update(bras, succes=int(converti))
```

---

## References Complementaires

- `references/statistical-foundations.md` — Fondements frequentistes, calcul de taille d'echantillon
- `references/experimentation-platform.md` — Integration MAB dans une plateforme feature flags
- `references/case-studies.md` — Cas 4 : MAB pour les notifications (Thompson Sampling en production)
- Documentation PyMC : https://www.pymc.io/
- Documentation ArviZ : https://python.arviz.org/
- Librairie Bambi : https://bambinos.github.io/bambi/ (interface haut niveau sur PyMC)
- "Bayesian Methods for Hackers" (Cameron Davidson-Pilon) — reference pratique bayesienne
