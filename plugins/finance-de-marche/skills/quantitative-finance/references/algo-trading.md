# Strategies de Trading Algorithmique

## Vue d'Ensemble

Le trading algorithmique est l'execution de strategies d'investissement systematiques via des regles pre-programmees, sans intervention humaine dans la prise de decision. Il couvre un large spectre de frequences (intraday a long terme) et de strategies (momentum, mean reversion, stat arb, market making). Ce document se concentre sur les strategies de frequence medium (holding de quelques heures a quelques semaines), implementables avec des ressources raisonnables.

---

## Architecture d'un Systeme de Trading Algorithmique

```
Donnees de marche
├── Temps reel (WebSocket, FIX) : prix, volumes, order book
├── EOD (End of Day) : OHLCV historique, dividendes, splits
└── Donnees alternatives : news, sentiment, earnings

        |
        ↓
Signal Generation
├── Feature engineering (indicateurs techniques, facteurs)
├── Modele de prediction (statistique ou ML)
└── Signal aggregation (multi-modele)

        |
        ↓
Portfolio Construction
├── Sizing des positions (Kelly, risk parity, fixed fraction)
├── Gestion des contraintes (concentration, levier, secteur)
└── Rebalancing logic

        |
        ↓
Execution
├── Order management (marche, limite, TWAP, VWAP)
├── Slippage minimisation
└── Couts de transaction

        |
        ↓
Risk Management
├── Stop-loss par position
├── Drawdown limit au niveau portefeuille
├── VaR limite
└── Circuit breakers

        |
        ↓
Monitoring & Reporting
├── P&L temps reel
├── Performance metriques
└── Alertes
```

---

## Strategies Systematiques — Implementation

### 1. Momentum Cross-Sectionnel (Equities)

**Principe** : Acheter les actions qui ont le plus monte sur les 12 derniers mois (en excluant le dernier mois — reversion a court terme) et vendre les actions qui ont le plus baisse.

```python
import pandas as pd
import numpy as np
import yfinance as yf

class CrossSectionalMomentum:

    def __init__(self, universe: list, lookback: int = 252, skip: int = 21,
                 top_pct: float = 0.20, rebalance_freq: str = 'M'):
        self.universe = universe
        self.lookback = lookback
        self.skip = skip
        self.top_pct = top_pct
        self.rebalance_freq = rebalance_freq

    def calculate_signal(self, prices: pd.DataFrame) -> pd.DataFrame:
        """Signal momentum : rendement sur lookback - skip derniers jours"""
        returns_full = prices.pct_change(self.lookback)
        returns_recent = prices.pct_change(self.skip)

        # Momentum ajuste (excluant le court terme)
        momentum = ((1 + returns_full) / (1 + returns_recent) - 1)

        # Rank cross-sectionnel (0 = pire, 1 = meilleur)
        return momentum.rank(axis=1, pct=True)

    def construct_portfolio(self, signal: pd.Series) -> pd.Series:
        """Long top 20%, short bottom 20%, equal-weighted"""
        n_assets = len(signal)
        n_positions = int(n_assets * self.top_pct)

        weights = pd.Series(0.0, index=signal.index)

        # Top performers (long)
        top = signal.nlargest(n_positions).index
        weights[top] = 1 / n_positions

        # Bottom performers (short)
        bottom = signal.nsmallest(n_positions).index
        weights[bottom] = -1 / n_positions

        return weights

    def backtest(self, prices: pd.DataFrame) -> pd.Series:
        """Backtest avec rebalancement mensuel"""
        signals = self.calculate_signal(prices)
        daily_returns = prices.pct_change()

        portfolio_returns = []
        rebalance_dates = pd.date_range(
            prices.index[self.lookback],
            prices.index[-1],
            freq=self.rebalance_freq
        )

        current_weights = None

        for date in prices.index[self.lookback:]:
            if current_weights is None or date in rebalance_dates:
                if date in signals.index:
                    current_weights = self.construct_portfolio(signals.loc[date])

            if current_weights is not None and date in daily_returns.index:
                daily_pnl = (current_weights * daily_returns.loc[date]).sum()
                portfolio_returns.append((date, daily_pnl))

        return pd.Series(
            [r[1] for r in portfolio_returns],
            index=[r[0] for r in portfolio_returns],
            name='momentum_returns'
        )
```

### 2. Mean Reversion — Pairs Trading (Cointegration)

```python
from statsmodels.tsa.stattools import coint, adfuller
from statsmodels.regression.linear_model import OLS
import statsmodels.api as sm

class PairsTrading:

    def __init__(self, ticker1: str, ticker2: str, window: int = 30,
                 entry_zscore: float = 2.0, exit_zscore: float = 0.0):
        self.ticker1 = ticker1
        self.ticker2 = ticker2
        self.window = window
        self.entry_zscore = entry_zscore
        self.exit_zscore = exit_zscore

    def check_cointegration(self, prices1: pd.Series, prices2: pd.Series) -> dict:
        """Test de cointegration (Engle-Granger)"""
        score, p_value, critical_values = coint(prices1, prices2)

        # Regression pour obtenir le hedge ratio
        X = sm.add_constant(prices2)
        model = OLS(prices1, X).fit()
        hedge_ratio = model.params[prices2.name]

        return {
            'cointegrated': p_value < 0.05,
            'p_value': p_value,
            'hedge_ratio': hedge_ratio,
            'r_squared': model.rsquared,
        }

    def calculate_spread(self, prices1: pd.Series, prices2: pd.Series,
                          hedge_ratio: float) -> pd.Series:
        """Calculer le spread entre les deux actifs"""
        return prices1 - hedge_ratio * prices2

    def generate_signals(self, spread: pd.Series) -> pd.Series:
        """
        Generer les signaux de trading sur le z-score du spread
        1 = long spread (long A, short B)
        -1 = short spread (short A, long B)
        0 = neutre
        """
        mean = spread.rolling(self.window).mean()
        std = spread.rolling(self.window).std()
        zscore = (spread - mean) / std

        signals = pd.Series(0, index=spread.index)

        # Positions
        signals[zscore > self.entry_zscore] = -1   # Short spread (spread trop large)
        signals[zscore < -self.entry_zscore] = 1   # Long spread (spread trop serré)
        signals[abs(zscore) < self.exit_zscore] = 0  # Exit

        # Propager la derniere position (hold)
        signals = signals.replace(0, np.nan).ffill().fillna(0)

        return signals, zscore

    def backtest(self, prices1: pd.Series, prices2: pd.Series, hedge_ratio: float) -> dict:
        """Backtest simple de la strategie pairs trading"""
        spread = self.calculate_spread(prices1, prices2, hedge_ratio)
        signals, zscore = self.generate_signals(spread)

        # P&L : long spread = long A, short B
        returns1 = prices1.pct_change()
        returns2 = prices2.pct_change()

        spread_returns = signals.shift(1) * (returns1 - hedge_ratio * returns2)

        return {
            'returns': spread_returns.dropna(),
            'sharpe': spread_returns.mean() / spread_returns.std() * np.sqrt(252),
            'max_drawdown': (spread_returns + 1).cumprod().div((spread_returns + 1).cumprod().cummax()) - 1,
            'n_trades': (signals.diff() != 0).sum(),
        }
```

### 3. Breakout Strategy (Donchian Channels)

```python
class DonchianBreakout:
    """
    Strategie de breakout sur les plus hauts/bas de N jours
    Trend-following simple et robuste
    """

    def __init__(self, entry_period: int = 20, exit_period: int = 10):
        self.entry_period = entry_period
        self.exit_period = exit_period

    def generate_signals(self, ohlcv: pd.DataFrame) -> pd.Series:
        """
        Entry : breakout du high ou low sur entry_period jours
        Exit : breakout du high ou low sur exit_period jours (inverse)
        """
        high_entry = ohlcv['High'].rolling(self.entry_period).max()
        low_entry = ohlcv['Low'].rolling(self.entry_period).min()
        high_exit = ohlcv['High'].rolling(self.exit_period).max()
        low_exit = ohlcv['Low'].rolling(self.exit_period).min()

        signals = pd.Series(0, index=ohlcv.index)

        position = 0
        for i in range(self.entry_period, len(ohlcv)):
            date = ohlcv.index[i]
            price = ohlcv['Close'].iloc[i]

            if position == 0:
                if price >= high_entry.iloc[i]:
                    position = 1   # Long breakout
                elif price <= low_entry.iloc[i]:
                    position = -1  # Short breakout
            elif position == 1:
                if price <= low_exit.iloc[i]:
                    position = 0   # Exit long
            elif position == -1:
                if price >= high_exit.iloc[i]:
                    position = 0   # Exit short

            signals.iloc[i] = position

        return signals
```

---

## Gestion des Positions et Sizing

### Kelly Criterion

```python
def kelly_fraction(win_rate: float, avg_win: float, avg_loss: float,
                   kelly_fraction: float = 0.5) -> float:
    """
    Fraction de Kelly = W - (1-W)/R
    W = win_rate, R = avg_win/avg_loss (payoff ratio)

    kelly_fraction = 0.5 → Half-Kelly (recommande en pratique)
    Kelly plein est trop agressif pour les strategies avec estimation incertaine
    """
    payoff_ratio = avg_win / abs(avg_loss)
    full_kelly = win_rate - (1 - win_rate) / payoff_ratio
    return max(0, full_kelly * kelly_fraction)

# Position sizing avec Kelly
def calculate_position_size(capital: float, price: float, win_rate: float,
                              avg_win_pct: float, avg_loss_pct: float,
                              max_position_pct: float = 0.10) -> dict:
    """
    Calculer la taille de position en nombre d'actions
    """
    kelly = kelly_fraction(win_rate, avg_win_pct, avg_loss_pct)
    kelly_capped = min(kelly, max_position_pct)  # Plafond de position

    capital_to_deploy = capital * kelly_capped
    shares = int(capital_to_deploy / price)

    return {
        'kelly_raw': kelly,
        'kelly_capped': kelly_capped,
        'capital_deployed': capital_to_deploy,
        'shares': shares,
        'position_value': shares * price,
    }
```

### ATR-Based Position Sizing

```python
def atr_position_size(capital: float, price: float, atr: float,
                       risk_per_trade_pct: float = 0.01,
                       atr_multiplier: float = 2.0) -> dict:
    """
    Taille de position basee sur l'ATR (Average True Range)
    risk_per_trade_pct : % du capital a risquer par trade
    atr_multiplier : distance du stop en multiple d'ATR
    """
    risk_amount = capital * risk_per_trade_pct
    stop_distance = atr * atr_multiplier

    shares = int(risk_amount / stop_distance)
    stop_price = price - stop_distance  # Pour une position longue

    return {
        'shares': shares,
        'stop_price': stop_price,
        'risk_amount': risk_amount,
        'position_value': shares * price,
        'position_pct': (shares * price) / capital,
    }
```

---

## Frameworks de Backtesting

### VectorBT — Backtesting Rapide

```python
import vectorbt as vbt
import pandas as pd
import numpy as np

# Telecharger les donnees
data = vbt.YFData.download('AAPL', start='2020-01-01', end='2025-01-01')
close = data.get('Close')

# Signaux de momentum simple (croisement de moyennes mobiles)
fast_ma = vbt.MA.run(close, window=20)
slow_ma = vbt.MA.run(close, window=50)

entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# Backtest en une ligne
portfolio = vbt.Portfolio.from_signals(
    close,
    entries=entries.values,
    exits=exits.values,
    freq='D',
    fees=0.001,        # 10 bps de frais
    slippage=0.0005,   # 5 bps de slippage
)

# Metriques
print(portfolio.stats())
print(f"Sharpe: {portfolio.sharpe_ratio():.3f}")
print(f"Max DD: {portfolio.max_drawdown():.2%}")
print(f"Total Return: {portfolio.total_return():.2%}")

# Visualisation
portfolio.plot().show()
```

### Backtrader — Event-Driven (plus realiste)

```python
import backtrader as bt

class MomentumStrategy(bt.Strategy):
    params = (
        ('lookback', 252),
        ('skip', 21),
        ('top_pct', 0.2),
    )

    def __init__(self):
        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}')
            else:
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}')

    def next(self):
        # Logique de trading ici
        pass

# Setup du backtest
cerebro = bt.Cerebro()
cerebro.addstrategy(MomentumStrategy)

# Donnees
data = bt.feeds.YahooFinanceData(
    dataname='AAPL',
    fromdate=datetime(2020, 1, 1),
    todate=datetime(2025, 1, 1),
)
cerebro.adddata(data)

# Capital initial et commission
cerebro.broker.setcash(100000)
cerebro.broker.setcommission(commission=0.001)

# Analyse
cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.04)
cerebro.addanalyzer(bt.analyzers.DrawDown)
cerebro.addanalyzer(bt.analyzers.Returns)

results = cerebro.run()
print(f"Final Portfolio: {cerebro.broker.getvalue():.2f}")
```

---

## Execution et Couts de Transaction

### Impact des Couts sur les Strategies

Les couts de transaction (spreads, commissions, slippage, market impact) peuvent transformer une strategie profitable en strategie perdante.

```python
def net_sharpe_after_costs(gross_sharpe: float, annual_turnover: float,
                            avg_cost_per_trade_bps: float = 20) -> float:
    """
    Estimation du Sharpe net apres couts de transaction
    annual_turnover : % du portefeuille trade par an (ex: 200% = portefeuille x2 par an)
    avg_cost_per_trade_bps : spread + commission + slippage en bps
    """
    annual_cost_drag = annual_turnover * avg_cost_per_trade_bps / 10000

    # Approximation : le Sharpe perd annual_cost_drag / vol_annualisee
    vol_annualisee = 0.15  # Hypothese
    sharpe_drag = annual_cost_drag / vol_annualisee

    return gross_sharpe - sharpe_drag

# Exemple :
# Strategie momentum avec turnover de 100%/an, 20 bps de couts
net = net_sharpe_after_costs(gross_sharpe=1.2, annual_turnover=1.0, avg_cost_per_trade_bps=20)
print(f"Sharpe net estimé: {net:.3f}")
```

### Algorithmes d'Execution

| Algorithme | Description | Usage |
|---|---|---|
| **Market Order** | Execution immediate au prix du marche | Liquidite elevee, urgence |
| **Limit Order** | Execution si le prix atteint un seuil | Eviter le slippage, moins de certitude |
| **TWAP** | Time-Weighted Average Price — decoupe sur le temps | Minimiser impact sur le prix |
| **VWAP** | Volume-Weighted Average Price — suit le volume | Reference standard institutionnel |
| **POV** | Participation On Volume — % du volume | Limiter l'impact de marche |

Pour les stratégies non-HFT avec des positions de taille raisonnable : l'ordre limite place a mi-spread est souvent l'approche la plus efficace.
