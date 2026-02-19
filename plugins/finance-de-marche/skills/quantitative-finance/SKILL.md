---
name: quantitative-finance
version: 1.0.0
description: >
  Use this skill when the user asks about "quantitative finance", "quant models", "algorithmic trading", "algo trading", "backtesting", "systematic trading", "factor models", "alpha generation", "statistical arbitrage", "momentum strategy", "mean reversion", "pairs trading", "risk models", "VaR", "CVaR", "Sharpe ratio optimization", "strategy development", "backtesting pitfalls", "walk-forward optimization", discusses quantitative investment strategies, systematic approaches to trading, or needs guidance on building, testing, and deploying quantitative trading strategies.
---

# Quantitative Finance — Modeles Quant, Algo Trading & Backtesting

## Overview

La finance quantitative applique des methodes mathematiques, statistiques et informatiques a la prise de decision d'investissement. A la frontiere entre research academique et trading operationnel, elle recouvre trois domaines principaux : les **modeles de risque et de valorisation** (VaR, modele de Black-Scholes, facteurs de risque), les **strategies de trading systematique** (momentum, mean reversion, arbitrage statistique) et la **methodologie de backtesting** (validation rigoureuse des strategies sur donnees historiques).

**Ce n'est pas du HFT** : La finance quantitative couverte ici cible les strategies de frequence medium (holding de quelques heures a quelques semaines), accessibles avec des ressources raisonnables. Le High-Frequency Trading (< 1 seconde de holding) requiert une infrastructure specialisee (colocation, FPGA) hors scope.

**Pourquoi la rigueur methodologique est critique** : Le backtesting est facile a manipuler — intentionnellement ou non. Les biais de survie, le data snooping, le lookahead bias, l'overfitting et les couts de transaction sous-estimes peuvent tous transformer une strategie perdante en strategie "gagnante" sur papier. La methodologie rigoureuse est la competence differenciatrice du quant.

**Perimetre** :
- Modeles de valorisation et de risque
- Taxonomie des strategies systematiques
- Methodologie de backtesting rigoureuse
- Implementation Python (Pandas, NumPy, Zipline/Backtrader/Vectorbt)
- Risk management des strategies en live

## Core Principles

**1. La rigueur avant la performance.** Un backtest avec des biais qui montre un Sharpe de 2.5 vaut moins qu'un backtest propre avec un Sharpe de 0.8. Valider systematiquement l'absence de lookahead bias, de survivorship bias et d'overfitting avant de s'enthousiasmer pour un resultat.

**2. Le risque d'abord, le rendement ensuite.** Toute strategie se definit d'abord par son profil de risque (drawdown max, VaR, volatilite). Le rendement est une consequence. Une strategie avec un drawdown inacceptable sera abandonnee en live avant de delivrer son espérance.

**3. Robustesse vs optimisation.** Une strategie robuste fonctionne sur des plages de parametres larges. Une strategie over-optimisee ne fonctionne que sur les parametres exacts du backtest. Preferer la robustesse : tester la sensibilite aux parametres, pas la performance maximale.

**4. Couts de transaction realistes.** Les spreads bid-ask, les commissions, le market impact et le slippage transforment des strategies rentables en strategies perdantes. Modeliser les couts de facon conservative, surtout pour les strategies a fort turnover.

**5. La diversification des signaux.** Un signal qui marche 60% du temps est excellent. Combiner plusieurs signaux decorreles ameliore le ratio rendement/risque mieux qu'un signal parfait (qui n'existe pas). Construire un ensemble de signaux orthogonaux.

**6. Le live est different du backtest — toujours.** L'execution relle diverge du backtest : donnees differentes, latence, erreurs d'execution, market impact. Anticiper un slippage de 20-50% sur les performances backtestees pour les strategies de court terme.

## Modeles de Risque

### Value at Risk (VaR)

**Definition** : Perte maximale qu'un portefeuille peut subir avec une probabilite donnee (confidence level) sur un horizon temporel.

Exemple : VaR 95% a 1 jour = 50 000 EUR signifie qu'on a 5% de chances de perdre plus de 50 000 EUR demain.

**Methodes de calcul** :

```python
import numpy as np
import pandas as pd

def var_historique(returns, confidence=0.95, horizon=1):
    """VaR historique non-parametrique"""
    return np.percentile(returns, (1 - confidence) * 100) * np.sqrt(horizon)

def var_parametrique(returns, confidence=0.95, horizon=1):
    """VaR parametrique (hypothese normalite)"""
    mu = returns.mean()
    sigma = returns.std()
    z = norm.ppf(1 - confidence)
    return (mu + z * sigma) * np.sqrt(horizon)

def cvar(returns, confidence=0.95):
    """Expected Shortfall / CVaR — moyenne des pertes au-dela du VaR"""
    var = var_historique(returns, confidence)
    return returns[returns <= var].mean()
```

**Limites du VaR** : ne capture pas les queues de distribution (fat tails), ne mesure pas l'ampleur des pertes au-dela du seuil. Completer avec le CVaR (Expected Shortfall) et les stress tests.

### Modeles Factoriels

**Fama-French 5 facteurs** :
- Market (Beta) : exposition au marche general
- Size (SMB) : Small minus Big — prime des small caps
- Value (HML) : High minus Low — prime de valeur (P/B ratio)
- Profitability (RMW) : Robust minus Weak — prime de rentabilite
- Investment (CMA) : Conservative minus Aggressive — prime d'investissement conservateur

```python
# Attribution de performance par facteur
import statsmodels.api as sm

def factor_attribution(returns_portfolio, factor_returns):
    """Regression sur les facteurs Fama-French"""
    X = sm.add_constant(factor_returns)
    model = sm.OLS(returns_portfolio, X).fit()

    print(f"Alpha annualise: {model.params['const'] * 252:.2%}")
    print(f"Beta marche: {model.params['Mkt-RF']:.3f}")
    print(f"R2: {model.rsquared:.3f}")
    return model
```

## Taxonomie des Strategies Systematiques

### 1. Momentum (Tendance Suiveur)

**Principe** : Les actifs qui ont surperforme le passe recent continuent a surperformer (inertie de marche). Horizon typique : 3-12 mois.

**Implementation** :
```python
def momentum_signal(prices, lookback=252, skip_recent=21):
    """
    Signal momentum standard : rendement sur lookback jours
    en excluant les skip_recent derniers jours (reversion court-terme)
    """
    returns_full = prices.pct_change(lookback)
    returns_recent = prices.pct_change(skip_recent)
    momentum = (1 + returns_full) / (1 + returns_recent) - 1

    # Cross-sectionnel : rank relatif
    signal = momentum.rank(axis=1, pct=True)
    return signal

# Construction du portefeuille : long top 20%, short bottom 20%
def momentum_portfolio(signal, top_pct=0.20):
    long_mask = signal > (1 - top_pct)
    short_mask = signal < top_pct
    weights = long_mask.astype(float) / long_mask.sum(axis=1, keepdims=True)
    weights -= short_mask.astype(float) / short_mask.sum(axis=1, keepdims=True)
    return weights
```

**Risques** : momentum crashes (inversion rapide lors des retournements de marche comme mars 2020), fort drawdown en regimes de transition.

### 2. Mean Reversion

**Principe** : Les prix ont tendance a revenir vers une moyenne. Fonctionne mieux sur des actifs co-integres (paires d'actions du meme secteur, ETF et ses composants).

**Pairs Trading (Ornstein-Uhlenbeck)** :
```python
from statsmodels.tsa.stattools import coint

def find_cointegrated_pairs(prices, pvalue_threshold=0.05):
    """Identifier les paires co-integrees"""
    n = prices.shape[1]
    pairs = []

    for i in range(n):
        for j in range(i+1, n):
            _, pvalue, _ = coint(prices.iloc[:, i], prices.iloc[:, j])
            if pvalue < pvalue_threshold:
                pairs.append((prices.columns[i], prices.columns[j], pvalue))

    return sorted(pairs, key=lambda x: x[2])

def zscore_signal(spread, window=30):
    """Signal z-score sur le spread"""
    mean = spread.rolling(window).mean()
    std = spread.rolling(window).std()
    return (spread - mean) / std

# Long si z-score < -2, short si z-score > +2, exit si abs(z) < 0.5
```

### 3. Statistical Arbitrage

**Principe** : Exploiter des inefficiences statistiques a court terme entre actifs lies. Inclut le pairs trading mais aussi les strategies intraday sur microstructure.

**Machine Learning applique au stat arb** :
- Features : micro-structure (bid-ask spread, order book imbalance), returns sur multiples horizons, volatilite, volume
- Modeles : Ridge/Lasso pour la linearite, XGBoost pour les non-linearites, LSTM pour les series temporelles
- Attention : le overfitting est particulierement dangereux en stat arb — utiliser l'out-of-sample testing

### 4. Strategies Factorielles (Smart Beta)

Construire un portefeuille avec une exposition systematique a des facteurs de risque primes :
- **Low Volatility** : actions faible volatilite — prime empirique contre-intuitive
- **Quality** : entreprises profitables, faible levier, stable — prime de qualite
- **Carry** : emprunter a bas taux, preter a haut taux (forex, obligataire)
- **Defensive** : beta marche < 1, secteurs defensifs

## Methodologie de Backtesting Rigoureuse

### Les Biais a Eliminer

**1. Lookahead Bias** : utiliser des donnees futures dans le signal. Erreur classique : calculer une moyenne mobile sur les donnees du jour J en incluant la cloture du jour J.
```python
# MAUVAIS : utilise la cloture du jour J pour le signal du jour J
signal = prices.rolling(20).mean()  # signal[J] inclut prices[J]

# CORRECT : decaler le signal d'un jour
signal = prices.rolling(20).mean().shift(1)  # signal[J] utilise prices jusqu'a J-1
```

**2. Survivorship Bias** : tester uniquement sur les actifs qui existent aujourd'hui, ignorant ceux qui ont fait faillite. Utiliser des donnees "point-in-time" incluant les actifs delistes.

**3. Data Snooping / Multiple Testing** : tester 100 parametres et garder le meilleur. La probabilite de trouver un "bon" parametre par chance est elevee. Utiliser des corrections (Bonferroni, Benjamini-Hochberg) ou reserver un holdout set jamais touche.

**4. Overfitting** : parametre sur-optimise sur l'historique. Solution : Walk-Forward Optimization.

### Walk-Forward Optimization

```python
def walk_forward_backtest(prices, strategy_fn, params_grid,
                          train_size=504, test_size=126, step=63):
    """
    Walk-forward : train sur N jours, test sur M jours, avancer de step jours
    """
    results = []

    for start in range(0, len(prices) - train_size - test_size, step):
        # Train period
        train = prices.iloc[start:start + train_size]

        # Optimisation sur train (cross-validation interne)
        best_params = optimize_params(train, strategy_fn, params_grid)

        # Test sur la periode hors-echantillon
        test = prices.iloc[start + train_size:start + train_size + test_size]
        test_returns = strategy_fn(test, **best_params)

        results.append({
            'period': prices.index[start + train_size],
            'returns': test_returns,
            'params': best_params
        })

    return pd.DataFrame(results)
```

### Metriques de Performance

```python
def strategy_metrics(returns, risk_free_rate=0.04):
    """Calcul des metriques de performance"""
    annual_return = returns.mean() * 252
    annual_vol = returns.std() * np.sqrt(252)
    sharpe = (annual_return - risk_free_rate) / annual_vol

    # Maximum Drawdown
    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.expanding().max()
    drawdown = cumulative / rolling_max - 1
    max_dd = drawdown.min()

    # Calmar Ratio
    calmar = annual_return / abs(max_dd)

    # Sortino Ratio (volatilite a la baisse uniquement)
    downside_returns = returns[returns < 0]
    downside_vol = downside_returns.std() * np.sqrt(252)
    sortino = (annual_return - risk_free_rate) / downside_vol

    return {
        'Annual Return': f"{annual_return:.2%}",
        'Annual Volatility': f"{annual_vol:.2%}",
        'Sharpe Ratio': f"{sharpe:.3f}",
        'Max Drawdown': f"{max_dd:.2%}",
        'Calmar Ratio': f"{calmar:.3f}",
        'Sortino Ratio': f"{sortino:.3f}"
    }
```

### Seuils de Validite

| Metrique | Minimum acceptable | Bon | Excellent |
|---|---|---|---|
| Sharpe Ratio | > 0.5 | > 1.0 | > 1.5 |
| Max Drawdown | < -30% | < -15% | < -10% |
| Calmar Ratio | > 0.5 | > 1.0 | > 2.0 |
| Correlation avec benchmark | < 0.8 | < 0.6 | < 0.4 |

## Frameworks de Libraries Python

| Besoin | Librairie | Commentaire |
|---|---|---|
| Backtesting vectorise (rapide) | **VectorBT** | 100-1000x plus rapide que Backtrader |
| Backtesting event-driven | **Backtrader**, **Zipline Reloaded** | Plus realiste, plus lent |
| Donnees financieres | **yfinance**, **OpenBB** | Gratuit, convient pour la recherche |
| Donnees professionnelles | **Bloomberg API**, **Refinitiv** | Payant, donnees haute qualite |
| Optimisation de portefeuille | **PyPortfolioOpt**, **Riskfolio-Lib** | MVO, HRP, Risk Parity |
| Modeles de risque | **QuantLib**, **Statsmodels** | VaR, options pricing |

## Maturity Model — Quant Finance

| Niveau | Caracteristique |
|---|---|
| **1 — Intuitif** | Decisions discretionnaires, backtests Excel sans rigueur |
| **2 — Systematise** | Regles explicites, backtest Python basique, metriques standard |
| **3 — Rigoureux** | Walk-forward, couts realistes, biais elimines, documentation |
| **4 — Avance** | ML signals, optimisation de portefeuille, execution algorithmique |
| **5 — Institutionnel** | Infrastructure professionnelle, risk management quantitatif, alpha recherche continue |

## Limites et Points de Vigilance

- Le backtest n'est pas un predicateur du futur : les conditions de marche changent (regimes), les inefficiences disparaissent quand elles sont exploitees
- La plupart des strategies ne survivent pas 3 ans en live : le decay de l'alpha est la regle, pas l'exception
- L'acces aux donnees de qualite est un avantage competitif majeur : les donnees gratuites (yfinance) ont des imprecisions qui biais les backtests
- La capacite de la strategie (AUM max) est inversement proportionnelle aux rendements : une strategie stat arb avec 10% de Sharpe sur 50k EUR ne fonctionnera pas sur 50M EUR (market impact)
- La conformite reglementaire : toute strategie algorithmique sur marches regules requiert une conformite MiFID II (algo trading) et potentiellement une notification a l'AMF
