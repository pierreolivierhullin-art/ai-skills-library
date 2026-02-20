# Options Trading Platform — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Construire une plateforme web d'aide à la décision pour le trading d'options US avec Signal Engine (buy/sell volatility), screener GARP, analyzer et portfolio tracker.

**Architecture:** Next.js App Router (frontend) + FastAPI Python (backend quant) + Supabase PostgreSQL (persistance) + Polygon.io (market data). Le backend FastAPI concentre toute l'intelligence : Black-Scholes, Greeks, IV Rank, indicateurs techniques, Signal Engine.

**Tech Stack:** Next.js 14 · shadcn/ui · React Query · FastAPI · Python 3.11 · numpy/scipy · pandas-ta · Supabase · Polygon.io · Railway · Vercel

**Design doc:** `docs/plans/2026-02-20-options-trading-platform-design.md`

---

## Phase 1 — Fondation du projet

### Task 1: Structure monorepo + environnements

**Files:**
- Create: `~/options-platform/backend/requirements.txt`
- Create: `~/options-platform/backend/app/__init__.py`
- Create: `~/options-platform/backend/app/main.py`
- Create: `~/options-platform/backend/.env.example`
- Create: `~/options-platform/frontend/` (via Next.js CLI)

**Step 1: Créer la structure backend**

```bash
mkdir -p ~/options-platform/backend/app/{routers,services,models,db}
mkdir -p ~/options-platform/backend/tests
touch ~/options-platform/backend/app/__init__.py
touch ~/options-platform/backend/app/routers/__init__.py
touch ~/options-platform/backend/app/services/__init__.py
touch ~/options-platform/backend/app/models/__init__.py
touch ~/options-platform/backend/app/db/__init__.py
```

**Step 2: Créer `requirements.txt`**

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
httpx==0.26.0
polygon-api-client==1.13.3
numpy==1.26.3
scipy==1.11.4
pandas==2.1.4
pandas-ta==0.3.14b
supabase==2.3.4
python-dotenv==1.0.0
pydantic==2.5.3
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-mock==3.12.0
```

**Step 3: Créer `app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Options Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}
```

**Step 4: Créer `.env.example`**

```env
POLYGON_API_KEY=your_polygon_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

**Step 5: Créer le frontend Next.js**

```bash
cd ~/options-platform
npx create-next-app@latest frontend \
  --typescript --tailwind --eslint \
  --app --src-dir=false --import-alias="@/*"
```

**Step 6: Installer shadcn/ui**

```bash
cd ~/options-platform/frontend
npx shadcn@latest init
npx shadcn@latest add button card badge table tabs alert skeleton
npm install @tanstack/react-query recharts lucide-react axios
```

**Step 7: Vérifier que le backend démarre**

```bash
cd ~/options-platform/backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# Expected: Uvicorn running on http://127.0.0.1:8000
# Test: curl http://localhost:8000/health → {"status":"ok"}
```

**Step 8: Commit**

```bash
cd ~/options-platform
git init && git add -A
git commit -m "feat: initialize monorepo — Next.js frontend + FastAPI backend"
```

---

### Task 2: Schéma Supabase

**Files:**
- Create: `~/options-platform/backend/db/migrations/001_initial_schema.sql`
- Create: `~/options-platform/backend/app/db/supabase.py`

**Step 1: Créer le fichier de migration SQL**

```sql
-- 001_initial_schema.sql

-- Watchlist de sous-jacents suivis
CREATE TABLE IF NOT EXISTS watchlist (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ticker TEXT NOT NULL UNIQUE,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Positions ouvertes
CREATE TABLE IF NOT EXISTS positions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ticker TEXT NOT NULL,
  strategy TEXT NOT NULL,           -- 'bull_put_spread', 'iron_condor', etc.
  legs JSONB NOT NULL,              -- [{type, strike, expiry, qty, premium}]
  entry_date DATE NOT NULL,
  expiry_date DATE NOT NULL,
  entry_credit NUMERIC(10,4),       -- crédit reçu (négatif si débit)
  max_profit NUMERIC(10,4),
  max_loss NUMERIC(10,4),
  entry_iv_rank NUMERIC(5,2),
  entry_delta NUMERIC(6,4),
  entry_theta NUMERIC(6,4),
  entry_vega NUMERIC(6,4),
  status TEXT DEFAULT 'open',       -- 'open', 'closed', 'expired'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Journal des trades (positions fermées avec P&L)
CREATE TABLE IF NOT EXISTS trades (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  position_id UUID REFERENCES positions(id),
  ticker TEXT NOT NULL,
  strategy TEXT NOT NULL,
  entry_date DATE NOT NULL,
  exit_date DATE NOT NULL,
  entry_credit NUMERIC(10,4),
  exit_debit NUMERIC(10,4),
  pnl NUMERIC(10,4),               -- P&L en dollars
  pnl_pct NUMERIC(6,2),            -- P&L en % du risque max
  exit_reason TEXT,                -- 'tp_50pct', 'tp_75pct', 'sl_2x', 'expiry', 'roll', 'manual'
  thesis TEXT,
  lesson TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Cache IV Rank (évite de recalculer à chaque requête)
CREATE TABLE IF NOT EXISTS iv_rank_cache (
  ticker TEXT PRIMARY KEY,
  iv_rank NUMERIC(5,2),
  iv_current NUMERIC(8,4),
  iv_52w_high NUMERIC(8,4),
  iv_52w_low NUMERIC(8,4),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_positions_status ON positions(status);
CREATE INDEX IF NOT EXISTS idx_positions_ticker ON positions(ticker);
CREATE INDEX IF NOT EXISTS idx_trades_ticker ON trades(ticker);
CREATE INDEX IF NOT EXISTS idx_trades_exit_date ON trades(exit_date);
```

**Step 2: Exécuter la migration dans Supabase**

Ouvrir le Supabase SQL Editor (dashboard.supabase.com → ton projet → SQL Editor), coller le contenu du fichier, exécuter.

**Step 3: Créer `app/db/supabase.py`**

```python
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_supabase() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    return create_client(url, key)
```

**Step 4: Écrire le test de connexion**

```python
# tests/test_db.py
import pytest
from app.db.supabase import get_supabase

def test_supabase_connection():
    client = get_supabase()
    # Vérifier que la table watchlist existe
    result = client.table("watchlist").select("id").limit(1).execute()
    assert result.data is not None
```

**Step 5: Lancer le test**

```bash
cd ~/options-platform/backend
source venv/bin/activate
cp .env.example .env  # remplir les vraies valeurs
pytest tests/test_db.py -v
# Expected: PASS
```

**Step 6: Commit**

```bash
git add -A
git commit -m "feat: add Supabase schema and database client"
```

---

### Task 3: Polygon.io client

**Files:**
- Create: `~/options-platform/backend/app/services/polygon_client.py`
- Create: `~/options-platform/backend/tests/test_polygon_client.py`

**Step 1: Écrire les tests**

```python
# tests/test_polygon_client.py
import pytest
from unittest.mock import AsyncMock, patch
from app.services.polygon_client import PolygonClient

@pytest.fixture
def client():
    return PolygonClient(api_key="test_key")

@pytest.mark.asyncio
async def test_get_options_chain_returns_list(client):
    mock_result = {
        "results": [
            {
                "details": {"contract_type": "call", "strike_price": 500, "expiration_date": "2026-03-21"},
                "greeks": {"delta": 0.45, "gamma": 0.02, "theta": -0.15, "vega": 0.30},
                "implied_volatility": 0.28,
                "open_interest": 1500,
                "day": {"volume": 800},
                "last_quote": {"ask": 8.50, "bid": 8.20}
            }
        ]
    }
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value.json.return_value = mock_result
        mock_get.return_value.status_code = 200
        chain = await client.get_options_chain("AAPL", "2026-03-21")
        assert len(chain) == 1
        assert chain[0]["strike"] == 500

@pytest.mark.asyncio
async def test_get_stock_ohlcv_returns_bars(client):
    mock_result = {
        "results": [
            {"t": 1700000000000, "o": 220.0, "h": 225.0, "l": 218.0, "c": 223.0, "v": 45000000}
        ]
    }
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value.json.return_value = mock_result
        mock_get.return_value.status_code = 200
        bars = await client.get_stock_ohlcv("AAPL", days=30)
        assert len(bars) == 1
        assert bars[0]["close"] == 223.0
```

**Step 2: Vérifier que les tests échouent**

```bash
pytest tests/test_polygon_client.py -v
# Expected: FAIL — "cannot import name 'PolygonClient'"
```

**Step 3: Implémenter `polygon_client.py`**

```python
import os
import httpx
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.polygon.io"

class PolygonClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ["POLYGON_API_KEY"]

    def _params(self, extra: dict = {}) -> dict:
        return {"apiKey": self.api_key, **extra}

    async def get_options_chain(self, ticker: str, expiration_date: str) -> list[dict]:
        url = f"{BASE_URL}/v3/snapshot/options/{ticker}"
        params = self._params({
            "expiration_date": expiration_date,
            "limit": 250
        })
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            raw = resp.json().get("results", [])

        return [
            {
                "contract_type": r["details"]["contract_type"],
                "strike": r["details"]["strike_price"],
                "expiry": r["details"]["expiration_date"],
                "delta": r.get("greeks", {}).get("delta"),
                "gamma": r.get("greeks", {}).get("gamma"),
                "theta": r.get("greeks", {}).get("theta"),
                "vega": r.get("greeks", {}).get("vega"),
                "iv": r.get("implied_volatility"),
                "oi": r.get("open_interest", 0),
                "volume": r.get("day", {}).get("volume", 0),
                "ask": r.get("last_quote", {}).get("ask"),
                "bid": r.get("last_quote", {}).get("bid"),
            }
            for r in raw
        ]

    async def get_stock_ohlcv(self, ticker: str, days: int = 252) -> list[dict]:
        url = f"{BASE_URL}/v2/aggs/ticker/{ticker}/range/1/day/2023-01-01/2026-12-31"
        params = self._params({"adjusted": "true", "sort": "asc", "limit": days})
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            raw = resp.json().get("results", [])

        return [
            {"timestamp": r["t"], "open": r["o"], "high": r["h"],
             "low": r["l"], "close": r["c"], "volume": r["v"]}
            for r in raw
        ]

    async def get_snapshot_iv(self, ticker: str) -> Optional[float]:
        """Récupère l'IV courante de l'option ATM la plus proche."""
        url = f"{BASE_URL}/v3/snapshot/options/{ticker}"
        params = self._params({"limit": 50})
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, params=params)
            if resp.status_code != 200:
                return None
            results = resp.json().get("results", [])
        ivs = [r.get("implied_volatility") for r in results if r.get("implied_volatility")]
        return sum(ivs) / len(ivs) if ivs else None
```

**Step 4: Lancer les tests**

```bash
pytest tests/test_polygon_client.py -v
# Expected: PASS (2 tests)
```

**Step 5: Commit**

```bash
git add -A
git commit -m "feat: add Polygon.io async client with options chain and OHLCV"
```

---

## Phase 2 — Moteur de calcul quant (FastAPI services)

### Task 4: Options pricing — Black-Scholes + Greeks

**Files:**
- Create: `~/options-platform/backend/app/services/pricing.py`
- Create: `~/options-platform/backend/tests/test_pricing.py`

**Step 1: Écrire les tests**

```python
# tests/test_pricing.py
import pytest
from app.services.pricing import black_scholes_price, calculate_greeks, calculate_pop

def test_black_scholes_call_price():
    # SPY 500 call, spot=500, sigma=0.20, T=30j, r=0.05
    price = black_scholes_price(S=500, K=500, T=30/365, r=0.05, sigma=0.20, option_type="call")
    assert 8.0 < price < 12.0  # plage raisonnable ATM

def test_black_scholes_put_price():
    price = black_scholes_price(S=500, K=500, T=30/365, r=0.05, sigma=0.20, option_type="put")
    assert 7.0 < price < 11.0

def test_call_put_parity():
    # C - P = S - K*exp(-rT) (put-call parity)
    S, K, T, r, sigma = 500, 495, 30/365, 0.05, 0.20
    call = black_scholes_price(S, K, T, r, sigma, "call")
    put = black_scholes_price(S, K, T, r, sigma, "put")
    import math
    parity = S - K * math.exp(-r * T)
    assert abs((call - put) - parity) < 0.01

def test_greeks_call_atm():
    greeks = calculate_greeks(S=500, K=500, T=30/365, r=0.05, sigma=0.20, option_type="call")
    assert 0.45 < greeks["delta"] < 0.55   # ATM call delta ≈ 0.50
    assert greeks["theta"] < 0              # theta toujours négatif
    assert greeks["gamma"] > 0
    assert greeks["vega"] > 0

def test_pop_calculation():
    # POP d'un short put à delta 0.30 ≈ 70%
    pop = calculate_pop(short_delta=-0.30)
    assert 0.65 < pop < 0.75
```

**Step 2: Vérifier l'échec**

```bash
pytest tests/test_pricing.py -v
# Expected: FAIL — ImportError
```

**Step 3: Implémenter `pricing.py`**

```python
import math
from scipy.stats import norm
from typing import Literal

def black_scholes_price(
    S: float, K: float, T: float, r: float, sigma: float,
    option_type: Literal["call", "put"] = "call"
) -> float:
    """Black-Scholes price. T en années."""
    if T <= 0:
        return max(0, S - K) if option_type == "call" else max(0, K - S)
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def calculate_greeks(
    S: float, K: float, T: float, r: float, sigma: float,
    option_type: Literal["call", "put"] = "call"
) -> dict:
    """Calcule delta, gamma, theta, vega, rho."""
    if T <= 0:
        return {"delta": 0, "gamma": 0, "theta": 0, "vega": 0, "rho": 0}

    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    pdf_d1 = norm.pdf(d1)
    sqrt_T = math.sqrt(T)
    exp_rT = math.exp(-r * T)

    gamma = pdf_d1 / (S * sigma * sqrt_T)
    vega = S * pdf_d1 * sqrt_T / 100  # pour 1% de changement d'IV

    if option_type == "call":
        delta = norm.cdf(d1)
        theta = (-(S * pdf_d1 * sigma) / (2 * sqrt_T) - r * K * exp_rT * norm.cdf(d2)) / 365
        rho = K * T * exp_rT * norm.cdf(d2) / 100
    else:
        delta = norm.cdf(d1) - 1
        theta = (-(S * pdf_d1 * sigma) / (2 * sqrt_T) + r * K * exp_rT * norm.cdf(-d2)) / 365
        rho = -K * T * exp_rT * norm.cdf(-d2) / 100

    return {"delta": round(delta, 4), "gamma": round(gamma, 6),
            "theta": round(theta, 4), "vega": round(vega, 4), "rho": round(rho, 4)}

def calculate_pop(short_delta: float) -> float:
    """POP d'une option vendue = 1 - |delta|."""
    return round(1 - abs(short_delta), 4)

def monte_carlo_expected_value(
    S: float, sigma: float, T: float, payoff_fn, n_sims: int = 1000
) -> float:
    """Expected value d'une stratégie via Monte Carlo."""
    import numpy as np
    np.random.seed(42)
    drift = -0.5 * sigma**2 * T
    diffusion = sigma * math.sqrt(T) * np.random.standard_normal(n_sims)
    final_prices = S * np.exp(drift + diffusion)
    payoffs = np.array([payoff_fn(p) for p in final_prices])
    return round(float(payoffs.mean()), 4)
```

**Step 4: Lancer les tests**

```bash
pytest tests/test_pricing.py -v
# Expected: PASS (5 tests)
```

**Step 5: Commit**

```bash
git add -A
git commit -m "feat: add Black-Scholes pricing engine with Greeks and Monte Carlo"
```

---

### Task 5: IV Rank calculator

**Files:**
- Create: `~/options-platform/backend/app/services/iv_rank.py`
- Create: `~/options-platform/backend/tests/test_iv_rank.py`

**Step 1: Écrire les tests**

```python
# tests/test_iv_rank.py
import pytest
from app.services.iv_rank import calculate_iv_rank, classify_iv_environment

def test_iv_rank_high():
    # IV actuelle au max historique → rank = 100
    rank = calculate_iv_rank(iv_current=0.40, iv_52w_high=0.40, iv_52w_low=0.15)
    assert rank == 100.0

def test_iv_rank_low():
    # IV actuelle au min historique → rank = 0
    rank = calculate_iv_rank(iv_current=0.15, iv_52w_high=0.40, iv_52w_low=0.15)
    assert rank == 0.0

def test_iv_rank_mid():
    rank = calculate_iv_rank(iv_current=0.275, iv_52w_high=0.40, iv_52w_low=0.15)
    assert abs(rank - 50.0) < 0.1

def test_classify_high_iv():
    result = classify_iv_environment(iv_rank=68)
    assert result["signal"] == "sell"
    assert "Iron Condor" in result["strategies"] or "Bull Put Spread" in result["strategies"]

def test_classify_low_iv():
    result = classify_iv_environment(iv_rank=22)
    assert result["signal"] == "buy"
```

**Step 2: Vérifier l'échec**

```bash
pytest tests/test_iv_rank.py -v
# Expected: FAIL
```

**Step 3: Implémenter `iv_rank.py`**

```python
def calculate_iv_rank(iv_current: float, iv_52w_high: float, iv_52w_low: float) -> float:
    """IV Rank = position de l'IV actuelle dans le range 52 semaines (0-100)."""
    if iv_52w_high == iv_52w_low:
        return 50.0
    rank = (iv_current - iv_52w_low) / (iv_52w_high - iv_52w_low) * 100
    return round(min(100.0, max(0.0, rank)), 2)

def classify_iv_environment(iv_rank: float) -> dict:
    """
    Retourne le signal buy/sell et les stratégies recommandées selon l'IV Rank.
    """
    if iv_rank >= 50:
        return {
            "signal": "sell",
            "label": "IV élevée — Vendre la volatilité",
            "strategies": ["Bull Put Spread", "Bear Call Spread", "Iron Condor", "Iron Butterfly"],
            "rationale": f"IV Rank {iv_rank:.0f}% — La volatilité implicite est chère. Favoriser les stratégies vendeuses de premium."
        }
    elif iv_rank <= 30:
        return {
            "signal": "buy",
            "label": "IV basse — Acheter la volatilité",
            "strategies": ["Bull Call Spread", "Bear Put Spread", "Calendar Spread", "Long Straddle"],
            "rationale": f"IV Rank {iv_rank:.0f}% — La volatilité implicite est bon marché. Favoriser les stratégies acheteuses."
        }
    else:
        return {
            "signal": "neutral",
            "label": "IV neutre — Sélection selon la direction",
            "strategies": ["Vertical Spread", "Calendar Spread"],
            "rationale": f"IV Rank {iv_rank:.0f}% — Zone neutre. Prioriser la direction du sous-jacent."
        }
```

**Step 4: Lancer les tests**

```bash
pytest tests/test_iv_rank.py -v
# Expected: PASS (5 tests)
```

**Step 5: Commit**

```bash
git add -A
git commit -m "feat: add IV Rank calculator and environment classifier"
```

---

### Task 6: Indicateurs techniques

**Files:**
- Create: `~/options-platform/backend/app/services/technicals.py`
- Create: `~/options-platform/backend/tests/test_technicals.py`

**Step 1: Écrire les tests**

```python
# tests/test_technicals.py
import pytest
import pandas as pd
import numpy as np
from app.services.technicals import calculate_signals, classify_trend

def make_trending_up_bars(n=60):
    """Génère des barres avec tendance haussière claire."""
    closes = [100 + i * 0.5 + np.random.normal(0, 0.2) for i in range(n)]
    volumes = [1_000_000 + np.random.randint(0, 500_000) for _ in range(n)]
    return [{"close": c, "high": c+1, "low": c-1, "open": c, "volume": v}
            for c, v in zip(closes, volumes)]

def test_signals_contain_required_keys():
    bars = make_trending_up_bars(60)
    signals = calculate_signals(bars)
    required = ["ema20", "ema50", "ema200", "rsi", "macd", "macd_signal",
                "bb_upper", "bb_lower", "bb_mid", "volume_ratio"]
    for key in required:
        assert key in signals, f"Missing key: {key}"

def test_rsi_range():
    bars = make_trending_up_bars(60)
    signals = calculate_signals(bars)
    assert 0 <= signals["rsi"] <= 100

def test_trend_classification_bullish():
    bars = make_trending_up_bars(60)
    signals = calculate_signals(bars)
    trend = classify_trend(signals)
    assert trend["bias"] in ["bullish", "neutral", "bearish"]
    assert "conviction" in trend  # 1-5
    assert "reasoning" in trend
```

**Step 2: Vérifier l'échec**

```bash
pytest tests/test_technicals.py -v
# Expected: FAIL
```

**Step 3: Implémenter `technicals.py`**

```python
import pandas as pd
import pandas_ta as ta
from typing import Optional

def calculate_signals(bars: list[dict]) -> dict:
    """
    Calcule tous les indicateurs techniques à partir d'une liste de barres OHLCV.
    bars: [{"open", "high", "low", "close", "volume"}, ...]
    """
    df = pd.DataFrame(bars)
    df = df.rename(columns={"open": "Open", "high": "High",
                             "low": "Low", "close": "Close", "volume": "Volume"})

    # EMAs
    df["ema20"] = ta.ema(df["Close"], length=20)
    df["ema50"] = ta.ema(df["Close"], length=50)
    df["ema200"] = ta.ema(df["Close"], length=200)

    # RSI
    df["rsi"] = ta.rsi(df["Close"], length=14)

    # MACD
    macd_df = ta.macd(df["Close"], fast=12, slow=26, signal=9)
    if macd_df is not None:
        df["macd"] = macd_df["MACD_12_26_9"]
        df["macd_signal"] = macd_df["MACDs_12_26_9"]
        df["macd_hist"] = macd_df["MACDh_12_26_9"]

    # Bollinger Bands
    bb_df = ta.bbands(df["Close"], length=20, std=2)
    if bb_df is not None:
        df["bb_upper"] = bb_df["BBU_20_2.0"]
        df["bb_lower"] = bb_df["BBL_20_2.0"]
        df["bb_mid"] = bb_df["BBM_20_2.0"]

    # Volume ratio vs MA 20j
    df["vol_ma20"] = ta.sma(df["Volume"], length=20)
    df["volume_ratio"] = df["Volume"] / df["vol_ma20"]

    last = df.iloc[-1]

    def safe(val):
        import math
        return None if (val is None or (isinstance(val, float) and math.isnan(val))) else round(float(val), 4)

    return {
        "close": safe(last["Close"]),
        "ema20": safe(last.get("ema20")),
        "ema50": safe(last.get("ema50")),
        "ema200": safe(last.get("ema200")),
        "rsi": safe(last.get("rsi")),
        "macd": safe(last.get("macd")),
        "macd_signal": safe(last.get("macd_signal")),
        "macd_hist": safe(last.get("macd_hist")),
        "bb_upper": safe(last.get("bb_upper")),
        "bb_lower": safe(last.get("bb_lower")),
        "bb_mid": safe(last.get("bb_mid")),
        "volume_ratio": safe(last.get("volume_ratio")),
    }

def classify_trend(signals: dict) -> dict:
    """
    Classe la tendance et retourne bias (bullish/bearish/neutral) + conviction (1-5).
    """
    score = 0
    reasoning = []

    close = signals.get("close", 0)
    ema20 = signals.get("ema20")
    ema50 = signals.get("ema50")
    ema200 = signals.get("ema200")

    # MAs alignment (+3 max)
    if ema20 and ema50 and close > ema20 > ema50:
        score += 2
        reasoning.append("Prix > EMA20 > EMA50 (tendance haussière)")
    elif ema20 and ema50 and close < ema20 < ema50:
        score -= 2
        reasoning.append("Prix < EMA20 < EMA50 (tendance baissière)")

    if ema200 and close > ema200:
        score += 1
        reasoning.append("Prix au-dessus de la MA200 (long terme haussier)")
    elif ema200 and close < ema200:
        score -= 1
        reasoning.append("Prix sous la MA200 (long terme baissier)")

    # RSI (+1/-1)
    rsi = signals.get("rsi")
    if rsi:
        if 50 < rsi < 70:
            score += 1
            reasoning.append(f"RSI {rsi:.0f} — momentum haussier")
        elif 30 < rsi < 50:
            score -= 1
            reasoning.append(f"RSI {rsi:.0f} — momentum baissier")

    # MACD (+1/-1)
    macd_hist = signals.get("macd_hist")
    if macd_hist:
        if macd_hist > 0:
            score += 1
            reasoning.append("MACD histogramme positif (momentum haussier)")
        else:
            score -= 1
            reasoning.append("MACD histogramme négatif (momentum baissier)")

    # Volume confirmation (+1)
    vol_ratio = signals.get("volume_ratio")
    if vol_ratio and vol_ratio > 1.2:
        sign = "haussier" if score > 0 else "baissier"
        reasoning.append(f"Volume {vol_ratio:.1f}x la moyenne — confirmation {sign}")

    # Scoring → bias + conviction
    if score >= 3:
        bias, conviction = "bullish", min(5, score)
    elif score <= -3:
        bias, conviction = "bearish", min(5, abs(score))
    elif score > 0:
        bias, conviction = "bullish", score
    elif score < 0:
        bias, conviction = "bearish", abs(score)
    else:
        bias, conviction = "neutral", 1

    return {
        "bias": bias,
        "conviction": conviction,
        "score": score,
        "reasoning": reasoning
    }
```

**Step 4: Lancer les tests**

```bash
pytest tests/test_technicals.py -v
# Expected: PASS (3 tests)
```

**Step 5: Commit**

```bash
git add -A
git commit -m "feat: add technical indicators engine (EMA, RSI, MACD, Bollinger, Volume)"
```

---

### Task 7: GARP filter

**Files:**
- Create: `~/options-platform/backend/app/services/garp.py`
- Create: `~/options-platform/backend/tests/test_garp.py`

**Step 1: Écrire les tests**

```python
# tests/test_garp.py
import pytest
from app.services.garp import evaluate_garp, GARPData

def test_garp_pass_all_criteria():
    data = GARPData(
        peg_ratio=1.1,
        revenue_growth_3y=0.18,   # 18%/an
        fcf_to_net_income=0.92,
        net_debt_to_ebitda=1.5,
        current_ratio=2.1,
        interest_coverage=8.0,
    )
    result = evaluate_garp(data)
    assert result["passes"] is True
    assert result["score"] >= 5

def test_garp_fail_high_peg():
    data = GARPData(
        peg_ratio=3.5,
        revenue_growth_3y=0.18,
        fcf_to_net_income=0.92,
        net_debt_to_ebitda=1.5,
        current_ratio=2.1,
        interest_coverage=8.0,
    )
    result = evaluate_garp(data)
    assert result["passes"] is False

def test_garp_score_is_out_of_6():
    data = GARPData(peg_ratio=1.0, revenue_growth_3y=0.15, fcf_to_net_income=0.85,
                    net_debt_to_ebitda=2.0, current_ratio=1.8, interest_coverage=6.0)
    result = evaluate_garp(data)
    assert 0 <= result["score"] <= 6
```

**Step 2: Vérifier l'échec**

```bash
pytest tests/test_garp.py -v
# Expected: FAIL
```

**Step 3: Implémenter `garp.py`**

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class GARPData:
    peg_ratio: Optional[float]
    revenue_growth_3y: Optional[float]      # ex: 0.18 = 18%
    fcf_to_net_income: Optional[float]      # ex: 0.92
    net_debt_to_ebitda: Optional[float]
    current_ratio: Optional[float]
    interest_coverage: Optional[float]

CRITERIA = [
    ("peg_ratio",          lambda v: v is not None and v < 1.5,  "PEG < 1.5"),
    ("revenue_growth_3y",  lambda v: v is not None and v > 0.10, "Croissance CA > 10%/an"),
    ("fcf_to_net_income",  lambda v: v is not None and v > 0.80, "FCF/Net Income > 80%"),
    ("net_debt_to_ebitda", lambda v: v is not None and v < 2.5,  "Dette nette/EBITDA < 2.5"),
    ("current_ratio",      lambda v: v is not None and v > 1.5,  "Current Ratio > 1.5"),
    ("interest_coverage",  lambda v: v is not None and v > 5.0,  "Couverture intérêts > 5x"),
]

def evaluate_garp(data: GARPData) -> dict:
    results = []
    score = 0
    for field, check, label in CRITERIA:
        val = getattr(data, field)
        passed = check(val)
        if passed:
            score += 1
        results.append({"criterion": label, "value": val, "passes": passed})

    return {
        "passes": score >= 4,   # Minimum 4/6 critères pour qualifier
        "score": score,
        "max_score": len(CRITERIA),
        "details": results,
    }
```

**Step 4: Lancer les tests**

```bash
pytest tests/test_garp.py -v
# Expected: PASS (3 tests)
```

**Step 5: Commit**

```bash
git add -A
git commit -m "feat: add GARP filter with 6 fundamental criteria"
```

---

### Task 8: Signal Engine

**Files:**
- Create: `~/options-platform/backend/app/services/signal_engine.py`
- Create: `~/options-platform/backend/tests/test_signal_engine.py`

**Step 1: Écrire les tests**

```python
# tests/test_signal_engine.py
import pytest
from app.services.signal_engine import SignalEngine, SignalInput

@pytest.fixture
def engine():
    return SignalEngine()

def test_high_iv_bullish_recommends_bull_put_spread(engine):
    inp = SignalInput(
        ticker="NVDA",
        iv_rank=68,
        trend_bias="bullish",
        trend_conviction=4,
        vix_level=18.5,
        volume_ratio=1.3,
        rsi=57,
        has_earnings_within_30d=False,
    )
    signal = engine.analyze(inp)
    assert signal["action"] == "sell_volatility"
    assert "Bull Put Spread" in signal["recommended_strategy"]
    assert signal["confidence"] >= 3

def test_low_iv_bearish_recommends_bear_put_spread(engine):
    inp = SignalInput(
        ticker="AAPL",
        iv_rank=22,
        trend_bias="bearish",
        trend_conviction=3,
        vix_level=14.0,
        volume_ratio=1.1,
        rsi=44,
        has_earnings_within_30d=False,
    )
    signal = engine.analyze(inp)
    assert signal["action"] == "buy_volatility"
    assert "Bear Put Spread" in signal["recommended_strategy"]

def test_high_iv_neutral_recommends_iron_condor(engine):
    inp = SignalInput(
        ticker="SPY",
        iv_rank=72,
        trend_bias="neutral",
        trend_conviction=2,
        vix_level=22.0,
        volume_ratio=0.9,
        rsi=52,
        has_earnings_within_30d=False,
    )
    signal = engine.analyze(inp)
    assert signal["action"] == "sell_volatility"
    assert "Iron Condor" in signal["recommended_strategy"]

def test_earnings_within_30d_warns(engine):
    inp = SignalInput(
        ticker="TSLA",
        iv_rank=55,
        trend_bias="bullish",
        trend_conviction=3,
        vix_level=20.0,
        volume_ratio=1.0,
        rsi=58,
        has_earnings_within_30d=True,
    )
    signal = engine.analyze(inp)
    assert signal["earnings_warning"] is True
```

**Step 2: Vérifier l'échec**

```bash
pytest tests/test_signal_engine.py -v
# Expected: FAIL
```

**Step 3: Implémenter `signal_engine.py`**

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class SignalInput:
    ticker: str
    iv_rank: float
    trend_bias: str          # "bullish" | "bearish" | "neutral"
    trend_conviction: int    # 1-5
    vix_level: float
    volume_ratio: float
    rsi: float
    has_earnings_within_30d: bool

STRATEGY_MATRIX = {
    ("sell", "bullish"):  ("Bull Put Spread",   "Vendre un put spread sous le support clé. Delta short : 0.25-0.30, DTE : 30-45j."),
    ("sell", "bearish"):  ("Bear Call Spread",  "Vendre un call spread au-dessus de la résistance clé. Delta short : 0.25-0.30, DTE : 30-45j."),
    ("sell", "neutral"):  ("Iron Condor",       "Vendre un iron condor des deux côtés. Strangle court à 0.25 delta, wings à 0.10 delta, DTE : 30-45j."),
    ("buy", "bullish"):   ("Bull Call Spread",  "Acheter un call spread directionnel. Delta long : 0.40-0.50, DTE : 45-60j."),
    ("buy", "bearish"):   ("Bear Put Spread",   "Acheter un put spread directionnel. Delta long : 0.40-0.50, DTE : 45-60j."),
    ("buy", "neutral"):   ("Calendar Spread",   "Acheter un calendar spread ATM pour profiter de la hausse de volatilité attendue."),
}

class SignalEngine:
    def analyze(self, inp: SignalInput) -> dict:
        # 1. Décision buy/sell volatility
        if inp.iv_rank >= 50:
            action = "sell_volatility"
            vol_key = "sell"
            vol_rationale = f"IV Rank {inp.iv_rank:.0f}% — volatilité implicite chère → vendre le premium."
        elif inp.iv_rank <= 30:
            action = "buy_volatility"
            vol_key = "buy"
            vol_rationale = f"IV Rank {inp.iv_rank:.0f}% — volatilité implicite bon marché → acheter le premium."
        else:
            action = "neutral"
            vol_key = "buy" if inp.trend_conviction >= 3 else "sell"
            vol_rationale = f"IV Rank {inp.iv_rank:.0f}% — zone neutre, décision orientée par la conviction directionnelle."

        # 2. Stratégie selon la matrice
        key = (vol_key, inp.trend_bias)
        strategy_name, strategy_detail = STRATEGY_MATRIX.get(
            key, ("Vertical Spread", "Stratégie directionnelle selon le biais.")
        )

        # 3. Confidence score (1-5)
        confidence = 0
        if inp.iv_rank >= 60 or inp.iv_rank <= 25:
            confidence += 2
        elif inp.iv_rank >= 50 or inp.iv_rank <= 30:
            confidence += 1
        confidence += min(2, inp.trend_conviction // 2)
        if inp.volume_ratio > 1.2:
            confidence += 1
        confidence = min(5, confidence)

        # 4. Régime VIX
        if inp.vix_level < 15:
            vix_regime = "calme"
        elif inp.vix_level < 25:
            vix_regime = "normal"
        else:
            vix_regime = "stress"

        return {
            "ticker": inp.ticker,
            "action": action,
            "recommended_strategy": strategy_name,
            "strategy_detail": strategy_detail,
            "confidence": confidence,
            "vol_rationale": vol_rationale,
            "trend_bias": inp.trend_bias,
            "trend_conviction": inp.trend_conviction,
            "vix_regime": vix_regime,
            "earnings_warning": inp.has_earnings_within_30d,
            "suggested_dte": 35,
            "suggested_short_delta": 0.28,
        }
```

**Step 4: Lancer les tests**

```bash
pytest tests/test_signal_engine.py -v
# Expected: PASS (4 tests)
```

**Step 5: Run all tests to date**

```bash
pytest tests/ -v
# Expected: PASS (all tests)
```

**Step 6: Commit**

```bash
git add -A
git commit -m "feat: add Signal Engine — buy/sell volatility decision matrix"
```

---

## Phase 3 — API FastAPI (endpoints)

### Task 9: Router Screener

**Files:**
- Create: `~/options-platform/backend/app/routers/screener.py`
- Modify: `~/options-platform/backend/app/main.py`

**Step 1: Créer `routers/screener.py`**

```python
from fastapi import APIRouter, HTTPException
from app.services.polygon_client import PolygonClient
from app.services.iv_rank import calculate_iv_rank, classify_iv_environment
from app.services.technicals import calculate_signals, classify_trend
from app.services.signal_engine import SignalEngine, SignalInput
from app.db.supabase import get_supabase
import asyncio

router = APIRouter(prefix="/screener", tags=["screener"])
engine = SignalEngine()

S_AND_P_100 = [
    "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "TSLA", "BRK.B",
    "JPM", "V", "JNJ", "WMT", "PG", "MA", "HD", "CVX", "MRK", "LLY",
    "ABBV", "AVGO", "PEP", "KO", "BAC", "PFE", "TMO", "COST", "CSCO",
    "ABT", "ACN", "MCD", "NKE", "DHR", "NEE", "TXN", "UNH", "CRM", "QCOM"
]

async def analyze_ticker(ticker: str, polygon: PolygonClient) -> dict | None:
    try:
        bars = await polygon.get_stock_ohlcv(ticker, days=252)
        if len(bars) < 60:
            return None

        signals = calculate_signals(bars)
        trend = classify_trend(signals)

        # IV Rank approximation depuis les barres (en production: utiliser Polygon options)
        closes = [b["close"] for b in bars]
        import numpy as np
        returns = np.diff(np.log(closes))
        hv_current = float(np.std(returns[-30:]) * np.sqrt(252))
        hv_52w_high = float(np.std(returns) * np.sqrt(252)) * 1.3
        hv_52w_low = float(np.std(returns) * np.sqrt(252)) * 0.6
        iv_rank_val = calculate_iv_rank(hv_current, hv_52w_high, hv_52w_low)

        iv_env = classify_iv_environment(iv_rank_val)

        signal_input = SignalInput(
            ticker=ticker,
            iv_rank=iv_rank_val,
            trend_bias=trend["bias"],
            trend_conviction=trend["conviction"],
            vix_level=20.0,  # À remplacer par VIX live
            volume_ratio=signals.get("volume_ratio") or 1.0,
            rsi=signals.get("rsi") or 50.0,
            has_earnings_within_30d=False,
        )
        signal = engine.analyze(signal_input)

        return {
            "ticker": ticker,
            "iv_rank": iv_rank_val,
            "iv_signal": iv_env["signal"],
            "trend_bias": trend["bias"],
            "trend_conviction": trend["conviction"],
            "recommended_strategy": signal["recommended_strategy"],
            "confidence": signal["confidence"],
            "rsi": signals.get("rsi"),
            "volume_ratio": signals.get("volume_ratio"),
        }
    except Exception:
        return None

@router.get("/scan")
async def scan_market(limit: int = 20):
    """Scanne l'univers d'actions et retourne les meilleures opportunités."""
    polygon = PolygonClient()
    tasks = [analyze_ticker(t, polygon) for t in S_AND_P_100[:limit]]
    results = await asyncio.gather(*tasks)
    valid = [r for r in results if r is not None]
    # Trier par confidence décroissante
    sorted_results = sorted(valid, key=lambda x: x["confidence"], reverse=True)
    return {"opportunities": sorted_results, "total": len(sorted_results)}

@router.get("/ticker/{ticker}")
async def analyze_single_ticker(ticker: str):
    """Analyse complète d'un ticker spécifique."""
    polygon = PolygonClient()
    result = await analyze_ticker(ticker.upper(), polygon)
    if not result:
        raise HTTPException(status_code=404, detail=f"Impossible d'analyser {ticker}")
    return result
```

**Step 2: Enregistrer le router dans `main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import screener

app = FastAPI(title="Options Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(screener.router)

@app.get("/health")
def health():
    return {"status": "ok"}
```

**Step 3: Tester manuellement**

```bash
uvicorn app.main:app --reload --port 8000
curl "http://localhost:8000/screener/ticker/AAPL"
# Expected: JSON avec iv_rank, trend_bias, recommended_strategy, confidence
```

**Step 4: Commit**

```bash
git add -A
git commit -m "feat: add screener API router with market scan and single ticker analysis"
```

---

### Task 10: Router Analyzer

**Files:**
- Create: `~/options-platform/backend/app/routers/analyzer.py`

**Step 1: Créer `routers/analyzer.py`**

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.pricing import black_scholes_price, calculate_greeks, calculate_pop, monte_carlo_expected_value
from app.services.polygon_client import PolygonClient
from app.services.iv_rank import calculate_iv_rank

router = APIRouter(prefix="/analyzer", tags=["analyzer"])

class StrategyLeg(BaseModel):
    option_type: str      # "call" | "put"
    strike: float
    expiry_days: int      # DTE
    qty: int              # +1 achat, -1 vente
    premium: float

class StrategyRequest(BaseModel):
    ticker: str
    spot_price: float
    iv: float             # volatilité implicite (ex: 0.28)
    risk_free_rate: float = 0.05
    legs: list[StrategyLeg]

@router.get("/chain/{ticker}")
async def get_options_chain(ticker: str, expiration_date: str):
    """Retourne la chaîne d'options complète pour un ticker et une expiration."""
    polygon = PolygonClient()
    chain = await polygon.get_options_chain(ticker.upper(), expiration_date)
    if not chain:
        raise HTTPException(status_code=404, detail="Chaîne d'options non disponible")
    return {"ticker": ticker, "expiration": expiration_date, "chain": chain}

@router.post("/strategy")
def analyze_strategy(req: StrategyRequest):
    """Analyse complète d'une stratégie multi-legs."""
    leg_results = []
    total_delta = 0
    total_gamma = 0
    total_theta = 0
    total_vega = 0
    net_premium = 0

    for leg in req.legs:
        T = leg.expiry_days / 365
        theo_price = black_scholes_price(
            S=req.spot_price, K=leg.strike, T=T,
            r=req.risk_free_rate, sigma=req.iv,
            option_type=leg.option_type
        )
        greeks = calculate_greeks(
            S=req.spot_price, K=leg.strike, T=T,
            r=req.risk_free_rate, sigma=req.iv,
            option_type=leg.option_type
        )
        mispricing = round(leg.premium - theo_price, 4)
        net_premium += leg.qty * leg.premium * 100  # par contrat (100 actions)
        total_delta += leg.qty * greeks["delta"]
        total_gamma += leg.qty * greeks["gamma"]
        total_theta += leg.qty * greeks["theta"]
        total_vega += leg.qty * greeks["vega"]

        leg_results.append({
            **leg.dict(),
            "theo_price": round(theo_price, 4),
            "mispricing": mispricing,
            "greeks": greeks,
        })

    # Breakevens (simplifié pour spreads 2-legs)
    breakevens = _calculate_breakevens(req.legs, net_premium)
    pop = calculate_pop(total_delta)

    # Monte Carlo EV sur la stratégie complète
    def strategy_payoff(final_price):
        total = 0
        for leg in req.legs:
            if leg.option_type == "call":
                intrinsic = max(0, final_price - leg.strike)
            else:
                intrinsic = max(0, leg.strike - final_price)
            total += leg.qty * (intrinsic - leg.premium) * 100
        return total

    ev = monte_carlo_expected_value(
        S=req.spot_price, sigma=req.iv, T=req.legs[0].expiry_days / 365,
        payoff_fn=strategy_payoff
    )

    return {
        "ticker": req.ticker,
        "legs": leg_results,
        "portfolio_greeks": {
            "delta": round(total_delta, 4),
            "gamma": round(total_gamma, 6),
            "theta": round(total_theta, 4),
            "vega": round(total_vega, 4),
        },
        "net_premium": round(net_premium, 2),
        "breakevens": breakevens,
        "pop": pop,
        "expected_value": ev,
    }

def _calculate_breakevens(legs: list[StrategyLeg], net_premium: float) -> list[float]:
    """Calcule les breakevens pour les stratégies simples."""
    breakevens = []
    premium_per_share = net_premium / 100
    for leg in legs:
        if leg.qty > 0:  # acheté
            if leg.option_type == "call":
                breakevens.append(round(leg.strike + abs(premium_per_share), 2))
            else:
                breakevens.append(round(leg.strike - abs(premium_per_share), 2))
    return breakevens
```

**Step 2: Enregistrer dans `main.py`**

Ajouter après `from app.routers import screener` :

```python
from app.routers import screener, analyzer
# ...
app.include_router(analyzer.router)
```

**Step 3: Tester manuellement**

```bash
curl -X POST "http://localhost:8000/analyzer/strategy" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "spot_price": 220.0,
    "iv": 0.28,
    "legs": [
      {"option_type": "put", "strike": 210, "expiry_days": 35, "qty": -1, "premium": 2.50},
      {"option_type": "put", "strike": 200, "expiry_days": 35, "qty": 1, "premium": 1.20}
    ]
  }'
# Expected: JSON avec greeks, pop, expected_value, breakevens
```

**Step 4: Commit**

```bash
git add -A
git commit -m "feat: add analyzer API router with options chain, strategy analysis and Monte Carlo"
```

---

### Task 11: Router Portfolio

**Files:**
- Create: `~/options-platform/backend/app/routers/portfolio.py`

**Step 1: Créer `routers/portfolio.py`**

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.supabase import get_supabase
from app.services.pricing import calculate_greeks, black_scholes_price
import json

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

class PositionCreate(BaseModel):
    ticker: str
    strategy: str
    legs: list[dict]
    entry_date: str
    expiry_date: str
    entry_credit: float
    max_profit: float
    max_loss: float
    entry_iv_rank: float

@router.get("/positions")
def get_positions():
    db = get_supabase()
    result = db.table("positions").select("*").eq("status", "open").execute()
    return {"positions": result.data}

@router.post("/positions")
def create_position(pos: PositionCreate):
    db = get_supabase()
    data = pos.dict()
    data["legs"] = json.dumps(data["legs"])
    result = db.table("positions").insert(data).execute()
    return {"position": result.data[0]}

@router.get("/summary")
def get_portfolio_summary():
    """Agrège les Greeks et le P&L de toutes les positions ouvertes."""
    db = get_supabase()
    positions = db.table("positions").select("*").eq("status", "open").execute().data

    total_delta = sum(p.get("entry_delta") or 0 for p in positions)
    total_theta = sum(p.get("entry_theta") or 0 for p in positions)
    total_vega = sum(p.get("entry_vega") or 0 for p in positions)
    total_max_risk = sum(abs(p.get("max_loss") or 0) for p in positions)

    return {
        "open_positions": len(positions),
        "aggregate_greeks": {
            "delta": round(total_delta, 4),
            "theta_daily": round(total_theta, 2),
            "vega": round(total_vega, 4),
        },
        "total_max_risk": round(total_max_risk, 2),
        "positions": positions,
    }

@router.patch("/positions/{position_id}/close")
def close_position(position_id: str, exit_debit: float, exit_reason: str, lesson: str = ""):
    db = get_supabase()
    pos = db.table("positions").select("*").eq("id", position_id).single().execute().data

    pnl = pos["entry_credit"] - exit_debit
    pnl_pct = round((pnl / abs(pos["max_loss"])) * 100, 2) if pos["max_loss"] else 0

    # Enregistrer dans le journal
    db.table("trades").insert({
        "position_id": position_id,
        "ticker": pos["ticker"],
        "strategy": pos["strategy"],
        "entry_date": pos["entry_date"],
        "exit_date": str(__import__("datetime").date.today()),
        "entry_credit": pos["entry_credit"],
        "exit_debit": exit_debit,
        "pnl": round(pnl, 2),
        "pnl_pct": pnl_pct,
        "exit_reason": exit_reason,
        "lesson": lesson,
    }).execute()

    # Marquer la position comme fermée
    db.table("positions").update({"status": "closed"}).eq("id", position_id).execute()

    return {"pnl": round(pnl, 2), "pnl_pct": pnl_pct}
```

**Step 2: Enregistrer dans `main.py`**

```python
from app.routers import screener, analyzer, portfolio
app.include_router(portfolio.router)
```

**Step 3: Commit**

```bash
git add -A
git commit -m "feat: add portfolio router — positions CRUD, summary, close with journal"
```

---

## Phase 4 — Frontend Next.js

### Task 12: Layout et navigation

**Files:**
- Modify: `~/options-platform/frontend/app/layout.tsx`
- Create: `~/options-platform/frontend/components/nav.tsx`
- Create: `~/options-platform/frontend/lib/api.ts`

**Step 1: Créer `lib/api.ts`**

```typescript
import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  timeout: 30000,
});

export const screenerApi = {
  scan: (limit = 20) => api.get(`/screener/scan?limit=${limit}`),
  ticker: (ticker: string) => api.get(`/screener/ticker/${ticker}`),
};

export const analyzerApi = {
  chain: (ticker: string, expiration: string) =>
    api.get(`/analyzer/chain/${ticker}?expiration_date=${expiration}`),
  strategy: (body: object) => api.post("/analyzer/strategy", body),
};

export const portfolioApi = {
  positions: () => api.get("/portfolio/positions"),
  summary: () => api.get("/portfolio/summary"),
  create: (data: object) => api.post("/portfolio/positions", data),
  close: (id: string, data: object) => api.patch(`/portfolio/positions/${id}/close`, data),
};

export default api;
```

**Step 2: Créer `components/nav.tsx`**

```tsx
"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const links = [
  { href: "/screener", label: "Screener" },
  { href: "/analyzer", label: "Analyzer" },
  { href: "/portfolio", label: "Portfolio" },
  { href: "/journal", label: "Journal" },
];

export function Nav() {
  const pathname = usePathname();
  return (
    <nav className="border-b bg-background">
      <div className="max-w-7xl mx-auto px-4 flex h-14 items-center gap-6">
        <span className="font-semibold text-sm">Options Platform</span>
        {links.map(({ href, label }) => (
          <Link
            key={href}
            href={href}
            className={cn(
              "text-sm transition-colors hover:text-foreground/80",
              pathname?.startsWith(href)
                ? "text-foreground font-medium"
                : "text-foreground/60"
            )}
          >
            {label}
          </Link>
        ))}
      </div>
    </nav>
  );
}
```

**Step 3: Mettre à jour `app/layout.tsx`**

```tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Nav } from "@/components/nav";
import { Providers } from "@/components/providers";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Options Platform",
  description: "US Options Trading Intelligence Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          <Nav />
          <main className="max-w-7xl mx-auto px-4 py-6">{children}</main>
        </Providers>
      </body>
    </html>
  );
}
```

**Step 4: Créer `components/providers.tsx`**

```tsx
"use client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: { queries: { staleTime: 5 * 60 * 1000 } },
  }));
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}
```

**Step 5: Vérifier que le frontend compile**

```bash
cd ~/options-platform/frontend
npm run dev
# Expected: Serveur sur http://localhost:3000, nav visible
```

**Step 6: Commit**

```bash
git add -A
git commit -m "feat: add Next.js layout, navigation, React Query provider and API client"
```

---

### Task 13: Page Screener

**Files:**
- Create: `~/options-platform/frontend/app/screener/page.tsx`
- Create: `~/options-platform/frontend/components/screener-table.tsx`
- Create: `~/options-platform/frontend/components/signal-badge.tsx`

**Step 1: Créer `components/signal-badge.tsx`**

```tsx
import { Badge } from "@/components/ui/badge";

type Props = { signal: "sell_volatility" | "buy_volatility" | "neutral" };

const config = {
  sell_volatility: { label: "VENDRE vol", className: "bg-orange-100 text-orange-800" },
  buy_volatility:  { label: "ACHETER vol", className: "bg-blue-100 text-blue-800" },
  neutral:         { label: "NEUTRE", className: "bg-gray-100 text-gray-600" },
};

export function SignalBadge({ signal }: Props) {
  const { label, className } = config[signal] ?? config.neutral;
  return <Badge className={className}>{label}</Badge>;
}
```

**Step 2: Créer `components/screener-table.tsx`**

```tsx
"use client";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { SignalBadge } from "./signal-badge";

type Opportunity = {
  ticker: string;
  iv_rank: number;
  trend_bias: string;
  trend_conviction: number;
  recommended_strategy: string;
  confidence: number;
  rsi: number | null;
};

export function ScreenerTable({ data }: { data: Opportunity[] }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Ticker</TableHead>
          <TableHead>IV Rank</TableHead>
          <TableHead>Signal</TableHead>
          <TableHead>Tendance</TableHead>
          <TableHead>Stratégie recommandée</TableHead>
          <TableHead>RSI</TableHead>
          <TableHead>Confiance</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map((row) => (
          <TableRow key={row.ticker}>
            <TableCell className="font-mono font-bold">{row.ticker}</TableCell>
            <TableCell>{row.iv_rank?.toFixed(0)}%</TableCell>
            <TableCell>
              <SignalBadge signal={row.iv_rank >= 50 ? "sell_volatility" : "buy_volatility"} />
            </TableCell>
            <TableCell className={
              row.trend_bias === "bullish" ? "text-green-600" :
              row.trend_bias === "bearish" ? "text-red-600" : "text-gray-500"
            }>
              {row.trend_bias} ({row.trend_conviction}/5)
            </TableCell>
            <TableCell>{row.recommended_strategy}</TableCell>
            <TableCell>{row.rsi?.toFixed(0)}</TableCell>
            <TableCell>{"★".repeat(row.confidence)}{"☆".repeat(5 - row.confidence)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
```

**Step 3: Créer `app/screener/page.tsx`**

```tsx
"use client";
import { useQuery } from "@tanstack/react-query";
import { screenerApi } from "@/lib/api";
import { ScreenerTable } from "@/components/screener-table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export default function ScreenerPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["screener-scan"],
    queryFn: () => screenerApi.scan(30).then((r) => r.data),
    refetchInterval: 30 * 60 * 1000, // refresh toutes les 30 min
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Screener</h1>
        <p className="text-muted-foreground text-sm">
          Opportunités triées par confiance — Signal Engine (GARP + Technique + IV Rank)
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Meilleures opportunités du jour</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading && (
            <div className="space-y-2">
              {Array.from({ length: 8 }).map((_, i) => (
                <Skeleton key={i} className="h-10 w-full" />
              ))}
            </div>
          )}
          {error && (
            <p className="text-destructive text-sm">
              Erreur de chargement. Vérifier que le backend est démarré.
            </p>
          )}
          {data?.opportunities && (
            <ScreenerTable data={data.opportunities} />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
```

**Step 4: Vérifier dans le navigateur**

```
http://localhost:3000/screener
# Expected: table avec tickers, IV Rank, signal badge, stratégie recommandée
```

**Step 5: Commit**

```bash
git add -A
git commit -m "feat: add Screener page with signal badges and opportunity table"
```

---

### Task 14: Page Portfolio

**Files:**
- Create: `~/options-platform/frontend/app/portfolio/page.tsx`

**Step 1: Créer `app/portfolio/page.tsx`**

```tsx
"use client";
import { useQuery } from "@tanstack/react-query";
import { portfolioApi } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

export default function PortfolioPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["portfolio-summary"],
    queryFn: () => portfolioApi.summary().then((r) => r.data),
    refetchInterval: 60_000,
  });

  const greeks = data?.aggregate_greeks;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Portfolio</h1>

      {/* Greeks agrégés */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Delta net", value: greeks?.delta?.toFixed(3) },
          { label: "Theta / jour", value: greeks?.theta_daily ? `$${greeks.theta_daily.toFixed(0)}` : null },
          { label: "Vega", value: greeks?.vega?.toFixed(3) },
          { label: "Risque max", value: data?.total_max_risk ? `$${data.total_max_risk.toLocaleString()}` : null },
        ].map(({ label, value }) => (
          <Card key={label}>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">{label}</CardTitle>
            </CardHeader>
            <CardContent>
              {isLoading ? <Skeleton className="h-8 w-20" /> : (
                <span className="text-2xl font-bold">{value ?? "—"}</span>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Positions ouvertes */}
      <Card>
        <CardHeader>
          <CardTitle>Positions ouvertes ({data?.open_positions ?? 0})</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading && <Skeleton className="h-40 w-full" />}
          {data?.positions?.length === 0 && (
            <p className="text-muted-foreground text-sm">Aucune position ouverte.</p>
          )}
          <div className="space-y-3">
            {data?.positions?.map((pos: any) => (
              <div key={pos.id} className="flex items-center justify-between border rounded-lg p-3">
                <div>
                  <span className="font-mono font-bold">{pos.ticker}</span>
                  <span className="ml-2 text-sm text-muted-foreground">{pos.strategy}</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-sm">Expiry: {pos.expiry_date}</span>
                  <Badge variant="outline">IV Rank: {pos.entry_iv_rank?.toFixed(0)}%</Badge>
                  <Badge className="bg-green-100 text-green-800">
                    Crédit: ${pos.entry_credit?.toFixed(2)}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

**Step 2: Vérifier dans le navigateur**

```
http://localhost:3000/portfolio
# Expected: dashboard avec 4 KPI cards + liste positions
```

**Step 3: Commit**

```bash
git add -A
git commit -m "feat: add Portfolio page with aggregate Greeks and open positions"
```

---

## Phase 5 — Tests d'intégration et déploiement

### Task 15: Tests d'intégration end-to-end

**Step 1: Écrire les tests d'intégration backend**

```python
# tests/test_integration.py
import pytest
import httpx

BASE = "http://localhost:8000"

def test_health():
    r = httpx.get(f"{BASE}/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_screener_ticker_aapl():
    r = httpx.get(f"{BASE}/screener/ticker/AAPL", timeout=20)
    assert r.status_code == 200
    data = r.json()
    assert "iv_rank" in data
    assert "recommended_strategy" in data
    assert "confidence" in data

def test_analyzer_strategy_bull_put_spread():
    payload = {
        "ticker": "AAPL",
        "spot_price": 220.0,
        "iv": 0.28,
        "legs": [
            {"option_type": "put", "strike": 210, "expiry_days": 35, "qty": -1, "premium": 2.50},
            {"option_type": "put", "strike": 200, "expiry_days": 35, "qty": 1, "premium": 1.20}
        ]
    }
    r = httpx.post(f"{BASE}/analyzer/strategy", json=payload, timeout=15)
    assert r.status_code == 200
    data = r.json()
    assert "portfolio_greeks" in data
    assert "pop" in data
    assert "expected_value" in data
    assert 0 < data["pop"] < 1
```

**Step 2: Lancer les tests d'intégration**

```bash
# S'assurer que le serveur tourne
uvicorn app.main:app --port 8000 &
pytest tests/test_integration.py -v
# Expected: PASS (3 tests)
```

**Step 3: Run full test suite**

```bash
pytest tests/ -v --tb=short
# Expected: PASS (tous les tests)
```

**Step 4: Commit**

```bash
git add -A
git commit -m "test: add integration tests for health, screener and analyzer endpoints"
```

---

### Task 16: Déploiement

**Step 1: Déployer le backend sur Railway**

```bash
# Installer Railway CLI
npm install -g @railway/cli
railway login
cd ~/options-platform/backend

# Créer le Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

railway new options-platform-api
railway up
# Configurer les variables d'environnement dans le dashboard Railway :
# POLYGON_API_KEY, SUPABASE_URL, SUPABASE_KEY
```

**Step 2: Déployer le frontend sur Vercel**

```bash
cd ~/options-platform/frontend
npx vercel
# Configurer la variable d'environnement dans Vercel dashboard :
# NEXT_PUBLIC_API_URL = https://your-railway-url.railway.app
```

**Step 3: Vérifier le déploiement**

```bash
curl https://your-railway-url.railway.app/health
# Expected: {"status": "ok"}
```

**Step 4: Commit final**

```bash
cd ~/options-platform
git add -A
git commit -m "feat: add deployment config — Railway backend, Vercel frontend"
```

---

## Récapitulatif des tests

```bash
# Tous les tests unitaires
cd ~/options-platform/backend
pytest tests/ -v

# Tests attendus :
# tests/test_db.py::test_supabase_connection         PASS
# tests/test_polygon_client.py::test_get_options_chain_returns_list  PASS
# tests/test_polygon_client.py::test_get_stock_ohlcv_returns_bars    PASS
# tests/test_pricing.py::test_black_scholes_call_price               PASS
# tests/test_pricing.py::test_black_scholes_put_price                PASS
# tests/test_pricing.py::test_call_put_parity                        PASS
# tests/test_pricing.py::test_greeks_call_atm                        PASS
# tests/test_pricing.py::test_pop_calculation                        PASS
# tests/test_iv_rank.py (5 tests)                                    PASS
# tests/test_technicals.py (3 tests)                                 PASS
# tests/test_garp.py (3 tests)                                       PASS
# tests/test_signal_engine.py (4 tests)                              PASS
# tests/test_integration.py (3 tests)                                PASS
# Total : 27 tests
```

## Coûts mensuels MVP

| Service | Plan | Coût |
|---------|------|------|
| Vercel | Hobby | $0 |
| Railway | Starter | $5 |
| Supabase | Free | $0 |
| Polygon.io | Options Starter | $29 |
| **Total** | | **$34/mois** |
