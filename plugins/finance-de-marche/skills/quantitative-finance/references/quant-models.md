# Modeles Quantitatifs — Valorisation et Risque

## Vue d'Ensemble

Les modeles quantitatifs sont les fondations mathematiques de la finance de marche moderne. Ils couvrent deux grands domaines : la **valorisation** (quel est le prix theorique d'un actif ?) et la **gestion du risque** (quelle est l'exposition potentielle aux pertes ?). Ce document couvre les modeles fondamentaux utilises par les praticiens, avec leur implementation Python.

---

## Modeles de Valorisation

### 1. Capital Asset Pricing Model (CAPM)

**Formule** : E(Ri) = Rf + βi × (E(Rm) - Rf)

- E(Ri) : rendement attendu de l'actif i
- Rf : taux sans risque (taux OAT 10 ans, actuellement ~3.2% en 2025)
- βi : exposition systematique au marche (beta)
- E(Rm) - Rf : prime de risque marche (historiquement 5-7% en Europe)

```python
import numpy as np
import pandas as pd
import yfinance as yf
from scipy import stats

def calculate_beta(asset_returns: pd.Series, market_returns: pd.Series) -> dict:
    """
    Calcule le beta d'un actif par regression sur les rendements du marche
    """
    # Regression OLS
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        market_returns.dropna(),
        asset_returns.dropna()
    )

    return {
        'beta': slope,
        'alpha_annualized': intercept * 252,  # Jensen's alpha
        'r_squared': r_value**2,
        'p_value': p_value,
        'std_error': std_err,
    }

def capm_expected_return(beta: float, rf: float = 0.032, market_premium: float = 0.055) -> float:
    """
    Rendement attendu CAPM
    rf : taux sans risque (OAT 10 ans France 2025)
    market_premium : prime de risque marche (5.5% Europe)
    """
    return rf + beta * market_premium

# Exemple
data = yf.download(['MC.PA', '^FCHI'], period='3y', auto_adjust=True)['Close']
returns = data.pct_change().dropna()

result = calculate_beta(returns['MC.PA'], returns['^FCHI'])
print(f"Beta LVMH: {result['beta']:.3f}")
print(f"Alpha Jensen: {result['alpha_annualized']:.2%}/an")
print(f"R2: {result['r_squared']:.3f}")
expected = capm_expected_return(result['beta'])
print(f"Rendement attendu CAPM: {expected:.2%}")
```

**Limites du CAPM** : hypothese de marche efficient, beta unique, pas de representation des tail risks. En pratique, complementer avec les modeles multi-facteurs.

### 2. Modeles Multi-Facteurs (Fama-French)

**Extension a 3 facteurs** :
E(Ri) - Rf = αi + bi × (Rm - Rf) + si × SMB + hi × HML

```python
import statsmodels.api as sm
import pandas_datareader as pdr

def fama_french_regression(returns: pd.Series, start: str = '2020-01', end: str = '2025-01') -> dict:
    """
    Regression sur les facteurs Fama-French 5
    Donnees disponibles gratuitement sur le site de Kenneth French
    """
    # Telecharger les facteurs Fama-French
    ff_data = pdr.get_data_famafrench('F-F_Research_Data_5_Factors_2x3', start=start, end=end)[0]
    ff_data = ff_data / 100  # Convertir de % en decimal

    # Aligner les donnees
    aligned = pd.concat([returns, ff_data], axis=1).dropna()
    excess_returns = aligned.iloc[:, 0] - aligned['RF']

    factors = aligned[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']]
    X = sm.add_constant(factors)

    model = sm.OLS(excess_returns, X).fit()

    return {
        'alpha_annualized': model.params['const'] * 12,  # Mensuel → annuel
        'market_beta': model.params['Mkt-RF'],
        'size_factor': model.params['SMB'],     # Positif = preference small cap
        'value_factor': model.params['HML'],    # Positif = preference value
        'profitability': model.params['RMW'],   # Positif = preference qualite
        'investment': model.params['CMA'],      # Positif = preference conservateur
        'r_squared': model.rsquared,
        'information_ratio': model.params['const'] / model.bse['const'] * np.sqrt(12),
    }
```

### 3. Black-Scholes (Valorisation d'Options)

**Pour la valorisation d'options europeennes** (voir skill options-risk pour le detail complet) :

```python
from scipy.stats import norm
import numpy as np

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    S : prix actuel du sous-jacent
    K : prix d'exercice (strike)
    T : temps jusqu'a l'echeance en annees
    r : taux sans risque (continu)
    sigma : volatilite implicite ou historique
    """
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    if option_type == 'call':
        price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    else:
        price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

    # Greeks
    delta = norm.cdf(d1) if option_type == 'call' else -norm.cdf(-d1)
    gamma = norm.pdf(d1) / (S*sigma*np.sqrt(T))
    theta = (-(S*norm.pdf(d1)*sigma)/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(d2)) / 365
    vega = S*norm.pdf(d1)*np.sqrt(T) / 100  # Par 1% de vol

    return {'price': price, 'delta': delta, 'gamma': gamma, 'theta': theta, 'vega': vega}
```

---

## Modeles de Risque

### Value at Risk (VaR) — Methodes Comparées

```python
import numpy as np
import pandas as pd
from scipy.stats import norm, t
import yfinance as yf

class PortfolioVaR:

    def __init__(self, returns: pd.Series):
        self.returns = returns

    def historical_var(self, confidence: float = 0.95, horizon: int = 1) -> float:
        """VaR historique — pas d'hypothese distributionnelle"""
        return np.percentile(self.returns, (1 - confidence) * 100) * np.sqrt(horizon)

    def parametric_var(self, confidence: float = 0.95, horizon: int = 1) -> float:
        """VaR parametrique — hypothese de normalite"""
        mu = self.returns.mean()
        sigma = self.returns.std()
        z = norm.ppf(1 - confidence)
        return (mu * horizon + z * sigma * np.sqrt(horizon))

    def monte_carlo_var(self, confidence: float = 0.95, horizon: int = 10,
                        n_simulations: int = 100000) -> float:
        """VaR Monte Carlo — utile pour les portefeuilles non-lineaires"""
        mu = self.returns.mean()
        sigma = self.returns.std()

        simulated = np.random.normal(
            mu * horizon,
            sigma * np.sqrt(horizon),
            n_simulations
        )

        return np.percentile(simulated, (1 - confidence) * 100)

    def cvar(self, confidence: float = 0.95) -> float:
        """CVaR / Expected Shortfall — moyenne des pertes au-dela du VaR"""
        var = self.historical_var(confidence)
        return self.returns[self.returns <= var].mean()

    def var_t_student(self, confidence: float = 0.95, horizon: int = 1,
                      nu: int = 5) -> float:
        """VaR avec distribution t de Student (mieux pour les queues epaisses)"""
        from scipy.stats import t as t_dist
        mu = self.returns.mean()
        sigma = self.returns.std() * np.sqrt((nu - 2) / nu)  # Correction variance
        z = t_dist.ppf(1 - confidence, df=nu)
        return (mu * horizon + z * sigma * np.sqrt(horizon))

    def compare_methods(self, confidence: float = 0.95) -> pd.DataFrame:
        """Comparer les differentes methodes"""
        return pd.DataFrame({
            'Method': ['Historical', 'Parametric (Normal)', 'Monte Carlo', 'CVaR', 'T-Student (v=5)'],
            'VaR_1day': [
                self.historical_var(confidence),
                self.parametric_var(confidence),
                self.monte_carlo_var(confidence),
                self.cvar(confidence),
                self.var_t_student(confidence),
            ]
        })
```

### Maximum Drawdown et Calmar Ratio

```python
def calculate_drawdown_metrics(returns: pd.Series) -> dict:
    """
    Calcule les metriques de drawdown pour evaluer le risque de perte cumulee
    """
    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.expanding().max()
    drawdown = cumulative / rolling_max - 1

    # Sequence de drawdown
    max_dd = drawdown.min()
    dd_start = drawdown.idxmin()

    # Trouver le debut du max drawdown
    peak_date = rolling_max[:dd_start].idxmax()

    # Trouver la fin de la recuperation (si recuperee)
    recovery = cumulative[dd_start:] >= rolling_max[dd_start]
    recovery_date = recovery[recovery].index[0] if recovery.any() else None

    annual_return = returns.mean() * 252
    calmar = annual_return / abs(max_dd) if max_dd != 0 else float('inf')

    return {
        'max_drawdown': max_dd,
        'peak_date': peak_date,
        'trough_date': dd_start,
        'recovery_date': recovery_date,
        'drawdown_duration_days': (dd_start - peak_date).days,
        'recovery_duration_days': (recovery_date - dd_start).days if recovery_date else None,
        'calmar_ratio': calmar,
        'average_drawdown': drawdown[drawdown < 0].mean(),
    }
```

---

## Optimisation de Portefeuille

### Frontiere Efficiente (Markowitz)

```python
import numpy as np
from scipy.optimize import minimize

def markowitz_optimization(returns: pd.DataFrame, rf: float = 0.032) -> dict:
    """
    Optimisation Markowitz — Minimisation de la variance pour un rendement cible
    Retourne les poids optimaux pour differents points de la frontiere efficiente
    """
    n_assets = len(returns.columns)
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252

    def portfolio_stats(weights):
        ret = np.dot(weights, mean_returns)
        vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe = (ret - rf) / vol
        return ret, vol, sharpe

    # Contraintes
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(n_assets))  # Long-only
    x0 = np.array([1/n_assets] * n_assets)

    # Portefeuille Sharpe Maximum
    def neg_sharpe(weights):
        ret, vol, sharpe = portfolio_stats(weights)
        return -sharpe

    msrp = minimize(neg_sharpe, x0, method='SLSQP', bounds=bounds, constraints=constraints)

    # Portefeuille Minimum Variance
    def portfolio_vol(weights):
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

    mvp = minimize(portfolio_vol, x0, method='SLSQP', bounds=bounds, constraints=constraints)

    return {
        'max_sharpe_weights': dict(zip(returns.columns, msrp.x)),
        'max_sharpe_stats': portfolio_stats(msrp.x),
        'min_var_weights': dict(zip(returns.columns, mvp.x)),
        'min_var_stats': portfolio_stats(mvp.x),
    }
```

### Hierarchical Risk Parity (HRP)

Approche robuste pour l'allocation de portefeuille, sans inverser la matrice de covariance (probleme numerique avec Markowitz).

```python
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform

def hierarchical_risk_parity(returns: pd.DataFrame) -> dict:
    """
    HRP (Lopez de Prado, 2016) — Allocation basee sur la hierarchie de correlation
    Plus robuste que Markowitz, pas besoin d'estimer le vecteur de rendements
    """
    corr = returns.corr()
    cov = returns.cov()

    # Distance correlation
    dist = np.sqrt(0.5 * (1 - corr))

    # Clustering hierarchique (Ward linkage)
    link = linkage(squareform(dist), method='ward')

    # Quasi-diagonalisation (reordonner les actifs par cluster)
    # ... (implementation complete dans PyPortfolioOpt)

    # Utiliser PyPortfolioOpt pour HRP
    from pypfopt import HRPOpt
    hrp = HRPOpt(returns)
    weights = hrp.optimize()

    return {
        'weights': weights,
        'performance': hrp.portfolio_performance(risk_free_rate=0.032, verbose=True)
    }
```

---

## Volatilite et GARCH

### GARCH(1,1) — Modelisation de la Volatilite Dynamique

Les modeles GARCH capturent le "volatility clustering" : les periodes de forte volatilite tendent a etre suivies de periodes de forte volatilite.

```python
from arch import arch_model

def fit_garch(returns: pd.Series) -> dict:
    """
    GARCH(1,1) — modele standard pour la volatilite dynamique
    """
    # Conversion en pourcentage (convention arch library)
    returns_pct = returns * 100

    # Specification du modele
    model = arch_model(
        returns_pct,
        vol='Garch',
        p=1, q=1,
        mean='Constant',
        dist='Normal'  # ou 't' pour Student (fat tails)
    )

    result = model.fit(disp='off')

    # Prevision de la volatilite sur 10 jours
    forecasts = result.forecast(horizon=10, reindex=False)
    vol_forecast = np.sqrt(forecasts.variance.values[-1]) / 100  # En decimal

    return {
        'omega': result.params['omega'],
        'alpha': result.params['alpha[1]'],     # Choc court terme
        'beta': result.params['beta[1]'],       # Persistance
        'persistence': result.params['alpha[1]'] + result.params['beta[1]'],
        'long_run_vol': np.sqrt(result.params['omega'] / (1 - result.params['alpha[1]'] - result.params['beta[1]'])) / 100,
        'vol_forecast_10d': vol_forecast,
        'aic': result.aic,
    }

# Interpretation :
# persistence ~ 0.95 → la volatilite est tres persistante (chocs durent longtemps)
# persistence > 1 → non-stationnaire (probleme)
```

---

## Stress Testing et Scenarios

```python
def scenario_analysis(portfolio_weights: dict, returns: pd.DataFrame) -> pd.DataFrame:
    """
    Analyse de scenarios historiques et hypothetiques
    """
    scenarios = {
        # Scenarios historiques
        'COVID Crash (feb-mar 2020)': ('2020-02-19', '2020-03-23'),
        'Tech Selloff (Q1 2022)': ('2022-01-03', '2022-03-14'),
        'Crise Lehman (sep-oct 2008)': ('2008-09-01', '2008-11-30'),
        'Black Monday 1987': ('1987-10-14', '1987-10-21'),
    }

    results = []

    for scenario_name, (start, end) in scenarios.items():
        try:
            scenario_returns = returns.loc[start:end]
            scenario_portfolio_return = sum(
                portfolio_weights.get(asset, 0) * scenario_returns[asset].sum()
                for asset in returns.columns
                if asset in portfolio_weights
            )
            results.append({
                'Scenario': scenario_name,
                'Start': start,
                'End': end,
                'Portfolio Return': f"{scenario_portfolio_return:.2%}",
            })
        except KeyError:
            pass  # Donnee non disponible pour ce scenario

    # Scenarios hypothetiques
    hypothetical = [
        ('Taux +200bps', {'bonds': -0.15, 'equities': -0.10, 'commodities': 0.02}),
        ('Recession severe', {'bonds': 0.05, 'equities': -0.35, 'commodities': -0.20}),
        ('Crise geopolitique', {'bonds': 0.08, 'equities': -0.20, 'commodities': 0.30}),
    ]

    return pd.DataFrame(results)
```
