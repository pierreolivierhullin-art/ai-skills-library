# Etudes de Cas — Finance Quantitative en Pratique

## Vue d'Ensemble

Ces etudes de cas illustrent le developpement et le deploiement de strategies quantitatives dans des contextes reels : developpement d'une strategie momentum, audit d'un backtest biaised, implementation d'un modele de risque, et construction d'un portefeuille multi-strategies.

---

## Cas 1 — Developpement d'une Strategie Momentum (Equites Europeennes)

### Contexte

Un family office (150M EUR d'actifs) souhaite implementer une poche systematique de 20M EUR sur les actions europeennes. Objectif : Sharpe > 0.8 net de frais, drawdown max < -20%, decorrelation avec le portefeuille discret existant (beta marche < 0.5).

### Processus de Developpement

**Etape 1 — Universe selection** :
- Euro Stoxx 600 (600 plus grandes capitalisations europeennes)
- Filtres de liquidite : ADV > 5M EUR/jour, market cap > 500M EUR → 380 valeurs retenues
- Donnees : Refinitiv Eikon (prix ajustes pour dividendes et splits, historique 15 ans), INCLUANT les delistes

**Etape 2 — Definition du signal** :

Signal momentum traditionnel : rendement cumulé sur 2-12 mois (excluant le dernier mois pour la reversion court-terme).

Tests de paramètres :
| Fenêtre | Sharpe brut | Sharpe net | Max DD |
|---|---|---|---|
| 3 mois | 0.62 | 0.31 | -28% |
| 6 mois | 0.78 | 0.52 | -24% |
| 12 mois | 0.89 | 0.67 | -22% |
| 2-12 mois (exclure 1m) | 0.95 | 0.74 | -21% |

**Etape 3 — Walk-Forward Validation** :

WFA sur 2010-2025 avec fenetres de 3 ans train / 1 an test.

| Annee OOS | Rendement | Sharpe OOS |
|---|---|---|
| 2013 | +8.2% | 0.71 |
| 2014 | +12.4% | 1.12 |
| 2015 | -2.1% | -0.19 (momentum crash) |
| 2016 | +6.8% | 0.62 |
| 2017 | +14.2% | 1.34 |
| 2018 | -8.4% | -0.73 (forte rotation sectorielle) |
| 2019 | +11.3% | 1.02 |
| 2020 | -15.2% | -1.28 (COVID crash) |
| 2021 | +18.7% | 1.45 |
| 2022 | -6.8% | -0.61 |
| 2023 | +9.4% | 0.88 |
| 2024 | +7.2% | 0.69 |
| **Annualise** | **+5.8%** | **0.61** |

WFA Efficiency : 0.61 IS Sharpe (0.95) → Ratio 0.64 — acceptable (> 0.5).

**Etape 4 — Ameliorations du signal** :

Le momentum pur sous-performe lors des retournements de marche (2015, 2018, 2020). Ameliorations testees :
- **Filtre de trend** : ne prendre de positions que si le marche global (Stoxx 600) est au-dessus de sa MA 200j. Reduit l'exposition lors des corrections de marche. Impact : max DD de -21% → -14%, Sharpe de 0.61 → 0.72.
- **Sector neutralite** : long/short dans chaque secteur separement (eviter les biais sectoriels). Impact : Sharpe 0.72 → 0.79, reduce la corrélation marché.

**Etape 5 — Holdout Set Validation** :

Holdout set garde depuis le debut : 2022-2024 (jamais touche). Test final de la strategie avec toutes les ameliorations.

Resultat : Sharpe 0.74, rendement +4.8%/an, max DD -12%. Conforme aux objectifs.

**Decision** : Deploiement de la strategie avec 15M EUR (pas les 20M prevus initialement — capacite limitee par le market impact sur les small caps).

### Lecons

- La WFA revele que la strategie sous-performe lors des momentum crashes (retournements brusques) : 2015, 2018, 2020. Cette periode doit etre explicitement discutee avec le client.
- Le filtre de trend de marche est une amelioration robuste (valide sur toutes les annees de test) — pas un overfit.
- Commencer avec 15M EUR et monitorer le market impact pendant 6 mois avant de monter a 20M EUR.

---

## Cas 2 — Audit d'un Backtest Biaised (Consultant en Gestion)

### Contexte

Un gestionnaire de patrimoine presente un backtest d'une "strategie de prediction de rendements" montrant un Sharpe de 4.2 sur 10 ans et un rendement annualisé de 28%. Il propose d'investir 5M EUR dans cette strategie.

### Audit Methodologique

**Red flags identifies immediatement** :
- Sharpe de 4.2 en trading systematique d'actions → exceptionnel, suspect
- 28% de rendement annualisé → impossible a tenir sur 10 ans pour une strategie accessible
- Backtesting code non fourni

**Audit Step 1 — Demande du code et des donnees** :

Le gestionnaire fournit un script Python. Analyse rapide :

```python
# BUG IDENTIFIE dans le code du gestionnaire
# Calcul du signal — LOOKAHEAD BIAS
data['signal'] = data['close'].pct_change(252)  # Rendement sur 12 mois
# Puis le signal est utilisé directement pour trader :
data['returns'] = data['signal'].shift(0) * data['next_day_return']
# PROBLEME : pas de shift(1) → le signal du jour J inclut la cloture du jour J
# La strategie "connait" les rendements futurs
```

**Audit Step 2 — Correction du lookahead bias** :

```python
# Correction : decaler le signal d'un jour
data['signal_corrected'] = data['close'].pct_change(252).shift(1)
data['returns_corrected'] = data['signal_corrected'] * data['next_day_return']

# Comparaison
sharpe_biased = data['returns'].mean() / data['returns'].std() * np.sqrt(252)
sharpe_corrected = data['returns_corrected'].mean() / data['returns_corrected'].std() * np.sqrt(252)

print(f"Sharpe avec lookahead bias: {sharpe_biased:.2f}")   # 4.2 — confirme
print(f"Sharpe corrige: {sharpe_corrected:.2f}")             # 0.58 — plus realiste
```

**Audit Step 3 — Survivorship Bias** :

L'universe utilise : les 100 plus grandes capitalisations europeennes en 2024. En 2014, l'universe devrait inclure les entreprises de l'epoque, dont beaucoup ont fait faillite ou ete delistes depuis.

Estimation de l'impact : +2-3% de rendement surestime par an.

**Conclusion de l'audit** :

Le backtest presente est invalide. Performance reelle estimee (apres correction) : Sharpe ~0.5-0.6, rendement 5-7%/an — correct mais pas exceptionnel. Recommandation : NE PAS investir sur la base de ce backtest. Demander une version corrigee avec methodology review independante.

**Lecon** : Un Sharpe > 2 dans le trading systematique d'equites est tres suspect. Les strategies Sharpe > 1.5 sont rares et generalement le fait d'institutions avec des avantages structurels (donnees alternatives, infrastructure HFT). Pour un gestionnaire de patrimoine retail, Sharpe 0.7-1.2 apres frais est un bon objectif.

---

## Cas 3 — Modele de Risque pour un Portefeuille Multi-Actifs

### Contexte

Un single family office (800M EUR d'actifs) souhaite implementer un systeme de risk management quantitatif. Portefeuille : 60% equites (US + Europe), 25% obligations, 10% alternatifs, 5% cash. Objectif : VaR quotidienne 99% < 1.5% du portefeuille.

### Implementation

**Step 1 — Matrice de covariance** :

```python
# Actifs du portefeuille
assets = {
    'MSCI_USA': 0.35,
    'MSCI_EUROPE': 0.25,
    'MSCI_EM': 0.00,
    'BONDS_EUR_10Y': 0.15,
    'BONDS_US_10Y': 0.10,
    'GOLD': 0.05,
    'PRIVATE_EQUITY': 0.05,  # Illiquide — prix lisse
    'CASH_EUR': 0.05,
}

# Problème : les PE (private equity) ont des prix lissés (autocorrélation)
# Desmoothing des rendements PE avant calcul de la cov matrix
def desmooth_returns(returns: pd.Series, autocorr_coef: float = 0.6) -> pd.Series:
    """Corriger l'autocorrelation des actifs illiquides (Geltner, 1991)"""
    return (returns - autocorr_coef * returns.shift(1)) / (1 - autocorr_coef)
```

**Step 2 — Comparaison des methodes VaR** :

| Methode | VaR 99% 1 jour | VaR 99% 10 jours |
|---|---|---|
| Historique (252j) | -1.28% | -4.05% |
| Parametrique normale | -1.15% | -3.64% |
| Monte Carlo (100k sims) | -1.31% | -4.14% |
| T-Student (v=5) | -1.52% | -4.81% |
| CVaR 99% (historique) | -1.89% | -5.98% |

**Decision** : La VaR historique de 1.28%/jour (99%) respecte l'objectif de 1.5%. Mais le CVaR de 1.89% montre que les queues sont epaisses. En cas de crise, les pertes peuvent depasser significativement la VaR.

**Step 3 — Stress tests scenarios** :

| Scenario | Impact Portefeuille |
|---|---|
| COVID Mars 2020 (March 9-23) | -12.4% |
| Lehman Sept-Nov 2008 | -18.2% |
| Dot-com crash 2000-2002 | -28.1% (sur 2 ans) |
| Hausse taux +200bps | -6.8% |
| Crise geopolitique (Ukraine-like) | -7.2% |

**Step 4 — Alertes et gouvernance** :

| Seuil | Trigger | Action |
|---|---|---|
| VaR > 1.2% (80% du limit) | Alerte email | Review mensuelle des positions |
| VaR > 1.5% (limit) | Alerte urgente | Comite de risque dans les 48h |
| Drawdown > -5% YTD | Alerte mensuelle | Revue de l'allocation |
| Drawdown > -10% YTD | Alerte urgente | Reduction du risque possible |

---

## Cas 4 — Portefeuille Multi-Strategies : Combinaison et Risque

### Contexte

Un hedge fund (450M EUR d'AUM) exploite 4 strategies independantes. L'equipe veut comprendre comment combiner optimalement ces strategies en termes d'allocation de capital.

### Analyse du Portefeuille de Strategies

**Performances individuelles (3 ans OOS)** :

| Strategie | Sharpe | Return | Vol | Max DD | Corr avec Marche |
|---|---|---|---|---|---|
| Momentum Cross-Section | 0.82 | 9.2% | 11.2% | -15.3% | 0.42 |
| Statistical Arbitrage | 1.24 | 6.8% | 5.5% | -7.1% | 0.08 |
| Event-Driven | 0.71 | 8.1% | 11.4% | -18.2% | 0.51 |
| Macro Trend | 0.93 | 7.4% | 7.9% | -11.8% | -0.18 |

**Matrice de correlation entre strategies** :

| | Momentum | Stat Arb | Event | Macro |
|---|---|---|---|---|
| Momentum | 1.00 | 0.12 | 0.38 | -0.15 |
| Stat Arb | 0.12 | 1.00 | 0.09 | 0.02 |
| Event | 0.38 | 0.09 | 1.00 | 0.21 |
| Macro | -0.15 | 0.02 | 0.21 | 1.00 |

**Allocation optimale** (max Sharpe du portefeuille de strategies) :

```python
from pypfopt import EfficientFrontier, expected_returns, risk_models

# Construction du portefeuille de strategies
strategies_returns = pd.DataFrame({
    'Momentum': momentum_returns,
    'StatArb': statarb_returns,
    'EventDriven': event_returns,
    'MacroTrend': macro_returns,
})

mu = strategies_returns.mean() * 252
sigma = strategies_returns.cov() * 252

ef = EfficientFrontier(mu, sigma)
weights = ef.max_sharpe(risk_free_rate=0.04)

print("Poids optimaux:")
for strat, w in weights.items():
    print(f"  {strat}: {w:.2%}")
```

**Poids optimaux** : Momentum 22%, Stat Arb 38%, Event 18%, Macro 22%.

**Performance du portefeuille combine (backtest sur les memes 3 ans)** :
- Sharpe : 1.41 (vs 0.93 pour la meilleure strategie individuelle)
- Rendement annualisé : 8.1%
- Volatilite : 5.8%
- Max Drawdown : -6.8%

**Lecon principale** : La diversification entre strategies decorrelees ameliore le Sharpe plus efficacement qu'ameliorer une strategie individuelle. Le Stat Arb (faible correlation au marche et aux autres strategies) est disproportionnellement valorisé dans l'allocation optimale.
