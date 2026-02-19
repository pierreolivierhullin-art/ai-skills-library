# Backtesting Rigoureux — Methodologie et Pieges

## Vue d'Ensemble

Le backtesting est le processus de validation d'une strategie de trading sur des donnees historiques. C'est l'etape la plus critique et la plus facilement manipulee du developpement de strategies quantitatives. Un backtest biaised peut transformer n'importe quelle strategie perdante en strategie "gagnante" sur papier. Ce document presente la methodologie rigoureuse pour eviter les pieges classiques et produire des backtests credibles.

---

## Les Biais a Eliminer — Taxonomie Complete

### 1. Lookahead Bias (Biais Futur)

**Definition** : Utiliser des informations qui n'etaient pas disponibles au moment de la decision de trading.

**Sources courantes** :

```python
# MAUVAIS : Le signal du jour J utilise la cloture du jour J
prices = pd.DataFrame({'close': [100, 101, 102, 100, 103]})
signal_BAD = prices['close'].rolling(3).mean()  # rolling mean inclut prices[J]

# CORRECT : Decaler d'un jour pour n'utiliser que les donnees de J-1
signal_GOOD = prices['close'].rolling(3).mean().shift(1)  # Disponible pour trading a l'ouverture J+1
```

**Autres sources de lookahead bias** :
- Normalisation sur l'ensemble du dataset avant le split train/test
- Imputation de valeurs manquantes avec des statistiques futures
- Etiquetage des trades avec le P&L realise (qui depend de l'avenir)
- Calcul du beta sur l'ensemble de la periode

**Detection** : Tester la strategie sur des donnees aleatoires. Si elle performe, il y a un biais.

### 2. Survivorship Bias (Biais de Survie)

**Definition** : Tester uniquement sur des actifs qui existent aujourd'hui, ignorant ceux qui ont fait faillite, ete acquis ou delistes.

**Impact** : Un backtest sur le S&P 500 actuel teste sur les 500 meilleures entreprises d'aujourd'hui — pas celles qui existaient il y a 20 ans. Le biais surestime les performances d'environ 1-3% par an.

**Solution** : Utiliser des donnees "point-in-time" incluant les actifs delistes.

Sources de donnees sans survivorship bias :
- **CRSP** (Center for Research in Security Prices) — reference academique
- **Compustat** — fundamental data incluant les delistes
- **Sharadar** (via Nasdaq Data Link) — accessible, inclut les delistes
- **Quandl SHARADAR** — base de donnees actions US avec historique complet

```python
# Simuler l'impact du survivorship bias (illustration)
# Universe avec survivorship bias (ce qu'on a souvent)
survivorship_returns = pd.Series([0.10, 0.08, 0.12, 0.09, 0.11])  # Que les survivors

# Universe sans survivorship bias (avec les delistes)
full_universe_returns = pd.concat([
    survivorship_returns,
    pd.Series([-0.80, -0.95, -0.70])  # Les delistes (pertes totales)
])

print(f"Biais de survie: {survivorship_returns.mean() - full_universe_returns.mean():.2%} par an")
```

### 3. Data Snooping / Multiple Testing

**Definition** : Tester de nombreuses combinaisons de parametres et selectionner la meilleure. La probabilite de trouver une "bonne" performance par chance est elevee.

**Calcul du risque** :

Si on teste N strategies independantes avec un niveau de significativite α :
P(au moins 1 faux positif) = 1 - (1-α)^N

Pour N=100 strategies et α=0.05 : P = 99.4% de trouver au moins 1 "strategie" significative par chance !

**Solutions** :

**Correction de Bonferroni** :
```python
def bonferroni_correction(p_values: list, alpha: float = 0.05) -> list:
    """
    Ajuster le seuil de significativite pour les tests multiples
    Bonferroni : chaque test doit avoir p < alpha/N
    """
    n = len(p_values)
    threshold = alpha / n
    return [(p, p < threshold) for p in p_values]
```

**Haircut de Sharpe** (Harvey, Liu & Zhu, 2016) :
Le Sharpe minimum requis pour valider une strategie augmente avec le nombre de strategies testees.

```python
def minimum_required_sharpe(n_strategies_tested: int, years: int = 3) -> float:
    """
    Haircut du Sharpe pour le multiple testing
    Basé sur Harvey, Liu & Zhu (2016) — 'Harvey ratio'
    """
    # Approximation : Sharpe minimum augmente avec sqrt(ln(n))
    import math
    sharpe_min = math.sqrt(2 * math.log(n_strategies_tested) / (years * 252))
    return sharpe_min

print(f"Sharpe min pour 10 strategies: {minimum_required_sharpe(10):.3f}")
print(f"Sharpe min pour 100 strategies: {minimum_required_sharpe(100):.3f}")
print(f"Sharpe min pour 1000 strategies: {minimum_required_sharpe(1000):.3f}")
```

**Solution pratique** : Garder un holdout set (20% des donnees) jamais touche pendant le developpement. Tester la strategie finale sur ce holdout une seule fois.

### 4. Overfitting

**Definition** : Parametres sur-optimises sur le dataset historique mais qui ne generalisent pas.

**Symptomes** :
- Tres haute performance in-sample, beaucoup plus basse out-of-sample
- Performances tres sensibles a de petites variations des parametres
- Trop de parametres par rapport au nombre d'observations

**Tests de robustesse** :

```python
import numpy as np
import pandas as pd

def robustness_test(strategy_fn, data: pd.DataFrame, params_grid: dict,
                     optimal_params: dict) -> pd.DataFrame:
    """
    Tester la sensibilite des performances aux parametres
    Une strategie robuste performe bien sur une plage large de parametres
    """
    results = []

    for param_name, param_values in params_grid.items():
        for value in param_values:
            test_params = {**optimal_params, param_name: value}
            returns = strategy_fn(data, **test_params)
            sharpe = returns.mean() / returns.std() * np.sqrt(252)
            results.append({
                'param_name': param_name,
                'param_value': value,
                'sharpe': sharpe,
                'is_optimal': value == optimal_params[param_name]
            })

    return pd.DataFrame(results)

# Si la performance est stable sur toute la plage → robuste
# Si elle s'effondre en dehors du parametre optimal → overfit
```

**Regularisation dans les modeles ML** :

```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.model_selection import TimeSeriesSplit, cross_val_score

def cross_validate_timeseries(model, X, y, n_splits=5):
    """
    Validation croisee adaptee aux series temporelles
    NEVER utiliser KFold standard (fuite d'information future)
    """
    tscv = TimeSeriesSplit(n_splits=n_splits)

    scores = cross_val_score(
        model, X, y,
        cv=tscv,
        scoring='neg_mean_squared_error'
    )

    return {
        'mean_score': scores.mean(),
        'std_score': scores.std(),
        'all_scores': scores,
    }

# Preferer ElasticNet pour les signaux alpha (combinaison Ridge + Lasso)
model = ElasticNet(alpha=0.1, l1_ratio=0.5)
```

### 5. Couts de Transaction Sous-estimes

**Composantes des couts reels** :

```python
def realistic_transaction_costs(
    trade_value: float,
    asset_type: str = 'equity',
    holding_period_days: int = 20,
    market_cap: str = 'large',
) -> dict:
    """
    Estimation des couts de transaction realistes
    """
    costs = {}

    if asset_type == 'equity':
        # Commission broker
        costs['commission_bps'] = 2.0  # ~2 bps (IB, algo)

        # Spread bid-ask
        spread_by_cap = {'large': 1.0, 'mid': 3.0, 'small': 10.0, 'micro': 25.0}
        costs['spread_bps'] = spread_by_cap.get(market_cap, 5.0)

        # Slippage (market impact)
        # Regle empirique : pour une position < 0.5% de l'ADV, impact ~ 0.5 x spread
        costs['slippage_bps'] = costs['spread_bps'] * 0.5

        # Borrow cost si short
        costs['borrow_bps'] = 50.0 if holding_period_days > 0 else 0  # 50 bps/an

    total_one_way_bps = (
        costs['commission_bps'] +
        costs['spread_bps'] / 2 +  # Moitie du spread en entree
        costs['slippage_bps']
    )

    # Aller-retour (entree + sortie)
    costs['total_roundtrip_bps'] = total_one_way_bps * 2

    # Si position longue, borrow cost
    if holding_period_days > 0:
        annual_borrow = costs.get('borrow_bps', 0) * holding_period_days / 252
        costs['total_roundtrip_bps'] += annual_borrow

    costs['total_roundtrip_pct'] = costs['total_roundtrip_bps'] / 10000

    return costs

# Exemple : combien de rendement brut pour etre rentable ?
costs = realistic_transaction_costs(100000, 'equity', 20, 'mid')
print(f"Couts roundtrip: {costs['total_roundtrip_bps']:.1f} bps")
print(f"Rendement minimum par trade pour etre profitable: {costs['total_roundtrip_pct']:.3%}")
```

---

## Walk-Forward Optimization — Implementation Complète

```python
import numpy as np
import pandas as pd
from typing import Callable, Dict, Any

def walk_forward_analysis(
    prices: pd.DataFrame,
    strategy_fn: Callable,
    params_grid: Dict[str, list],
    train_size: int = 504,    # 2 ans de trading
    test_size: int = 126,     # 6 mois
    step_size: int = 63,      # Reoptimise tous les 3 mois
    objective: str = 'sharpe',
) -> Dict[str, Any]:
    """
    Walk-Forward Analysis : train sur N jours, test sur M jours, avance de S jours
    Reproduit fidelement le processus de developpement reel d'une strategie
    """
    results = []
    n = len(prices)

    for start in range(0, n - train_size - test_size, step_size):
        train_end = start + train_size
        test_end = train_end + test_size

        train_data = prices.iloc[start:train_end]
        test_data = prices.iloc[train_end:test_end]

        # Optimisation sur le train set (grid search avec cross-validation)
        best_params = None
        best_score = float('-inf')

        # Inner walk-forward pour l'optimisation (evite l'overfitting sur le train set)
        inner_tscv_size = train_size // 5  # 5 splits internes
        inner_scores = {}

        for params_combo in _generate_combinations(params_grid):
            inner_returns = []

            for inner_start in range(0, train_size - inner_tscv_size * 2, inner_tscv_size):
                inner_train = train_data.iloc[inner_start:inner_start + inner_tscv_size]
                inner_test = train_data.iloc[inner_start + inner_tscv_size:inner_start + inner_tscv_size * 2]

                try:
                    strategy_returns = strategy_fn(inner_test, **params_combo)
                    inner_returns.append(_compute_objective(strategy_returns, objective))
                except:
                    inner_returns.append(float('-inf'))

            avg_score = np.mean(inner_returns)
            if avg_score > best_score:
                best_score = avg_score
                best_params = params_combo

        # Appliquer les meilleurs parametres sur le test set (hors-echantillon)
        test_returns = strategy_fn(test_data, **best_params)
        test_score = _compute_objective(test_returns, objective)

        results.append({
            'train_start': prices.index[start],
            'train_end': prices.index[train_end - 1],
            'test_start': prices.index[train_end],
            'test_end': prices.index[test_end - 1],
            'best_params': best_params,
            'in_sample_score': best_score,
            'out_of_sample_score': test_score,
            'out_of_sample_returns': test_returns,
        })

    # Concatener tous les rendements hors-echantillon
    all_oos_returns = pd.concat([r['out_of_sample_returns'] for r in results])

    # Efficience WFA : ratio IS/OOS Sharpe (> 0.5 = acceptable)
    is_scores = [r['in_sample_score'] for r in results]
    oos_scores = [r['out_of_sample_score'] for r in results]
    wfa_efficiency = np.mean(oos_scores) / np.mean(is_scores) if np.mean(is_scores) > 0 else 0

    return {
        'oos_returns': all_oos_returns,
        'oos_sharpe': all_oos_returns.mean() / all_oos_returns.std() * np.sqrt(252),
        'wfa_efficiency': wfa_efficiency,
        'n_windows': len(results),
        'detail': results,
    }

def _compute_objective(returns: pd.Series, objective: str) -> float:
    if objective == 'sharpe':
        return returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
    elif objective == 'calmar':
        drawdown = returns.cumsum().sub(returns.cumsum().cummax())
        return returns.sum() * 252 / abs(drawdown.min()) if drawdown.min() < 0 else 0

def _generate_combinations(params_grid: dict):
    """Genere toutes les combinaisons de parametres"""
    import itertools
    keys = params_grid.keys()
    for combo in itertools.product(*params_grid.values()):
        yield dict(zip(keys, combo))
```

---

## Rapport de Backtest Standard

```python
def generate_backtest_report(returns: pd.Series, benchmark_returns: pd.Series = None,
                               rf: float = 0.04) -> pd.DataFrame:
    """
    Rapport complet de backtest
    """
    annual_return = returns.mean() * 252
    annual_vol = returns.std() * np.sqrt(252)

    cum_returns = (1 + returns).cumprod()
    rolling_max = cum_returns.expanding().max()
    drawdown = cum_returns / rolling_max - 1
    max_dd = drawdown.min()

    sharpe = (annual_return - rf) / annual_vol

    downside_returns = returns[returns < 0]
    downside_vol = downside_returns.std() * np.sqrt(252)
    sortino = (annual_return - rf) / downside_vol

    calmar = annual_return / abs(max_dd)

    # Ratios de victoire
    win_rate = (returns > 0).mean()
    avg_win = returns[returns > 0].mean()
    avg_loss = returns[returns < 0].mean()
    profit_factor = abs(avg_win * win_rate / (avg_loss * (1 - win_rate))) if avg_loss != 0 else float('inf')

    report = {
        'Annual Return': f"{annual_return:.2%}",
        'Annual Volatility': f"{annual_vol:.2%}",
        'Sharpe Ratio': f"{sharpe:.3f}",
        'Sortino Ratio': f"{sortino:.3f}",
        'Calmar Ratio': f"{calmar:.3f}",
        'Max Drawdown': f"{max_dd:.2%}",
        'Win Rate': f"{win_rate:.2%}",
        'Avg Win / Avg Loss': f"{abs(avg_win/avg_loss):.3f}",
        'Profit Factor': f"{profit_factor:.3f}",
        'Total Return': f"{cum_returns.iloc[-1] - 1:.2%}",
        'N Days': len(returns),
    }

    if benchmark_returns is not None:
        corr = returns.corr(benchmark_returns)
        bench_annual = benchmark_returns.mean() * 252
        bench_vol = benchmark_returns.std() * np.sqrt(252)
        bench_sharpe = (bench_annual - rf) / bench_vol
        active_return = annual_return - bench_annual
        tracking_error = (returns - benchmark_returns).std() * np.sqrt(252)
        information_ratio = active_return / tracking_error

        report.update({
            'Benchmark Sharpe': f"{bench_sharpe:.3f}",
            'Active Return': f"{active_return:.2%}",
            'Information Ratio': f"{information_ratio:.3f}",
            'Correlation (Benchmark)': f"{corr:.3f}",
            'Beta': f"{returns.cov(benchmark_returns) / benchmark_returns.var():.3f}",
        })

    return pd.Series(report, name='Backtest Report')
```

---

## Checklist de Validation d'un Backtest

### Pre-Backtest
- [ ] Donnees point-in-time verifiees (pas de survivorship bias)
- [ ] Holdout set separe (20% minimum) jamais touche
- [ ] Logique de signal documentee et simple a comprendre

### Pendant le Backtest
- [ ] Zero lookahead bias (shift(1) systematique sur tous les signaux)
- [ ] Couts de transaction inclus (spread + commission + slippage)
- [ ] Rebalancement realiste (pas en fin de journee a des prix impossibles)

### Post-Backtest
- [ ] Walk-forward analysis realisee (pas uniquement IS backtest)
- [ ] Efficience WFA > 0.5 (OOS/IS ratio de Sharpe)
- [ ] Test sur le holdout set (une seule fois — sacre)
- [ ] Tests de robustesse sur les parametres
- [ ] Performance stable si couts × 2 (test de sensibilite aux couts)
- [ ] Sharpe hors-echantillon > 0.7 (minimum pour consideration live)
- [ ] Max drawdown acceptable en live (pas seulement en backtest)
