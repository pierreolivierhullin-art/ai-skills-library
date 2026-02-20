# Options Trading Platform — Design Document

**Date** : 2026-02-20
**Statut** : Validé
**Scope** : MVP usage personnel (solo)

---

## Vision

Plateforme web d'aide à la décision pour le trading d'options sur le marché américain. L'objectif est de concentrer l'intelligence trading — analyse fondamentale GARP, signaux techniques, dynamique de la volatilité implicite — en une interface qui produit des recommandations actionnables : quelle stratégie, sur quel sous-jacent, avec quel sizing, et surtout : **acheter ou vendre la volatilité**.

---

## Architecture globale

### Stack technique

| Couche | Technologie | Rôle |
|--------|-------------|------|
| Frontend | Next.js App Router (TypeScript) | Interface utilisateur |
| UI | shadcn/ui + Recharts | Composants + visualisations |
| Backend | FastAPI (Python) | Calculs quant, Signal Engine |
| Database | Supabase (PostgreSQL) | Journal, watchlist, cache |
| Market data | Polygon.io ($29/mois) | Options chain, IV, Greeks, flow |
| Déploiement frontend | Vercel | Hosting Next.js |
| Déploiement backend | Railway | Hosting FastAPI |

### Schéma d'architecture

```
┌────────────────────────────────────────────────────────┐
│                   FRONTEND (Next.js)                   │
│  Screener │ Analyzer │ Portfolio │ Trade Journal       │
│  shadcn/ui · React Query · Recharts                    │
└──────────────────────┬─────────────────────────────────┘
                       │ REST + WebSocket
┌──────────────────────▼─────────────────────────────────┐
│              BACKEND (FastAPI / Python)                │
│  signal_engine │ screener │ portfolio │ garp_filter    │
│  Black-Scholes · Monte Carlo · Greeks · IV Surface     │
└──────────┬───────────────────────────┬─────────────────┘
           │                           │
┌──────────▼──────────┐   ┌────────────▼────────────────┐
│   Polygon.io API    │   │    Supabase (PostgreSQL)     │
│ Chain · IV · Flow   │   │ Journal · Watchlist · Cache  │
│ Greeks · Snapshots  │   │ Positions · Settings         │
└─────────────────────┘   └─────────────────────────────┘
```

---

## Modules fonctionnels

### Module 1 — Screener

Identifier les meilleures opportunités du jour sans parcourir 6 000 tickers.

**Universe** : S&P 500 + Nasdaq 100 + watchlist personnelle

**Pipeline de filtrage (FastAPI) :**

```
[Filtre 1] GARP Fundamentals
  → PEG < 1.5
  → Croissance CA > 10%/an sur 3 ans
  → FCF/Net Income > 80%
  → Dette nette/EBITDA < 2.5

[Filtre 2] Options Liquidity
  → Open Interest > 500
  → Bid-ask spread < 5%
  → Volume journalier > 100 contracts

[Filtre 3] Volatilité implicite
  → IV Rank calculé sur 252 jours
  → IV Percentile

[Filtre 4] Signaux techniques
  → Tendance MAs (EMA 20/50/200)
  → RSI 14 (pas en zone extrême contraire à la thèse)
  → Volume > moyenne 20j (confirmation)

→ Score composite → Ranking des opportunités
```

**Output pour chaque ticker retenu :**
- Score global (0-100)
- IV Rank + signal buy/sell volatility
- Biais directionnel (haussier / baissier / neutre) + conviction (1-5)
- Stratégie recommandée par le Signal Engine
- P&L max / max loss / POP estimé

**Cadence :** Refresh pre-market (9h00 EST) + toutes les 30 min pendant les heures de marché.

**Flow detection (Polygon.io WebSocket) :** Alertes en temps réel sur les options avec volume >> Open Interest (signal institutionnel potentiel).

---

### Module 2 — Signal Engine (Buy vs Sell)

Le cerveau différenciant de la plateforme. Traduit le process de trading en algorithme reproductible.

**Ordre d'analyse :**

```
1. GARP screening        → sous-jacent de qualité
2. VIX regime            → < 15 calme / 15-25 normal / > 25 stress
3. Tendance              → EMA 20/50/200 + MACD
4. Momentum              → RSI 14
5. Volatilité prix       → Bollinger Bands (expansion / contraction)
6. Volume                → Confirmation du mouvement (vs moyenne 20j)
7. Niveaux clés          → Support / résistance → placement des strikes
8. IV Rank               → Décision ACHETER ou VENDRE la volatilité
                           ↓
                   RECOMMANDATION finale
```

**Matrice de décision Buy vs Sell :**

| | IV Rank > 50% (IV chère) | IV Rank < 30% (IV bon marché) |
|---|---|---|
| Biais haussier | Vendre Bull Put Spread | Acheter Bull Call Spread / LEAPS |
| Biais baissier | Vendre Bear Call Spread | Acheter Bear Put Spread / Long Put |
| Neutre / range | Vendre Iron Condor | Acheter Calendar / Straddle |
| Événement imminent | Vendre Iron Butterfly | Acheter Straddle / Strangle |

**Output Signal Engine (exemple NVDA) :**

```
NVDA — Signal Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fondamentaux  : GARP ✓ (PEG 1.1, FCF/NI 92%)
VIX regime    : Normal (VIX 18.2)
Tendance      : Haussier (EMA 20 > 50 > 200)
MACD          : Bullish crossover confirmé
RSI           : 58 (neutre-haussier)
Bollinger     : Prix au-dessus de la bande médiane
Volume        : +34% vs moyenne 20j (confirmation)
Support clé   : $820 (strike short recommandé : $830)
IV Rank       : 68% → VENDRE la volatilité

→ Bull Put Spread 35 DTE
  Short put : 830 (Δ -0.28)  Long put : 810 (Δ -0.14)
  Crédit    : $1.85   Risque max : $18.15   POP : 73%
```

---

### Module 3 — Analyzer

Analyse approfondie d'un trade spécifique avant d'ouvrir la position.

**Fonctionnalités :**

- **Options chain** : strikes × expirations avec IV, delta, gamma, theta, vega, OI, volume, bid/ask
- **Strategy Builder** : sélection de 1-4 legs → calcul automatique du profil complet
- **Pricing Black-Scholes** : prix théorique vs prix de marché → détection du mispricing
- **Greeks de position** : delta, gamma, theta, vega, rho
- **Breakeven(s)** exact(s) calculés
- **POP** (probabilité de profit) via distribution log-normale
- **Expected Value** sur 1 000 simulations Monte Carlo
- **IV Surface** : heat map (skew + term structure)

**Visualisations :**
- Payoff diagram : P&L à expiration par niveau de prix du sous-jacent
- P&L live : valeur de la position aujourd'hui vs dans N jours (theta decay animé)
- Scenario analysis : "Si le sous-jacent +5% dans 10 jours avec IV -20% → P&L ?"

**Checklist pré-trade intégrée** (9 critères du skill options-risk) :
La checklist se complète automatiquement à partir des données calculées. Le bouton "Enregistrer dans le journal" n'est actif qu'une fois les 9 critères validés.

---

### Module 4 — Portfolio Tracker

Suivi en temps réel des positions ouvertes et gestion active du risque.

**Dashboard Greeks agrégés :**

```
┌─────────────────────────────────────────────────────────┐
│ Δ Net: +0.23  Γ: 0.04  Θ: -$47/day  V: +$180/%IV      │
│ P&L Today: +$342  P&L Total: +$1,847  Max Risk: $4,200  │
└─────────────────────────────────────────────────────────┘
```

**Alertes automatiques (règles mécaniques) :**
- Profit atteint 50% → notification "Clôturer ?"
- Profit atteint 75% → notification "Clôturer maintenant"
- Perte atteint 2× premium → alerte rouge "Couper"
- DTE < 21 → rappel de review
- Short strike approché (Δ > 0.50) → alerte ajustement / roll

**Stress Test hebdomadaire :**
Simulation Monte Carlo sur le portefeuille entier. Scénarios : -10%, -20%, VIX spike +50%.

---

### Module 5 — Trade Journal

Base de données de toutes les positions (ouvertes et fermées). Fondation de la crédibilité trader.

**Par trade enregistré :**
- Setup : ticker, stratégie, thèse directionnelle
- Entry : date, prix, Greeks à l'ouverture, IV Rank
- Management : ajustements effectués
- Exit : date, prix, raison (TP / SL / expiration / roll)
- P&L réel (en dollars et en % du risque)
- Leçon / note post-trade

**Dashboard de performance :**
- Win rate global et par stratégie
- Profit factor (gain moyen / perte moyenne)
- R-multiple moyen
- Max drawdown
- Top 5 stratégies par P&L
- Historique équité

---

## Données de marché — Polygon.io

**Endpoints utilisés :**
- `/v3/snapshot/options/{underlyingAsset}` — Options chain complète avec Greeks et IV
- `/v2/aggs/ticker/{stocksTicker}/range/...` — OHLCV pour indicateurs techniques
- `/v2/snapshot/locale/us/markets/options/...` — Unusual activity / flow
- WebSocket `options.*` — Updates temps réel prix et Greeks

**Calculs backend (Python, non délégués à Polygon) :**
- IV Rank sur 252 jours (Polygon fournit l'IV brute, le Rank est calculé côté FastAPI)
- Signal Engine complet
- Tous les Greeks de stratégie multi-legs
- Monte Carlo et Expected Value

---

## Indicateurs techniques (Signal Engine)

| Indicateur | Usage |
|---|---|
| EMA 20 / 50 / 200 | Définition de la tendance (haussier si EMA 20 > 50 > 200) |
| MACD (12/26/9) | Momentum et changements de tendance (crossover signal) |
| RSI 14 | Surachat (> 70) / survente (< 30) pour timing d'entrée |
| Bollinger Bands (20, 2σ) | Régime : expansion (breakout) vs contraction (range) |
| VIX | Régime macro : < 15 / 15-25 / > 25 |
| Volume vs MA 20j | Confirmation : mouvement validé si volume > moyenne |
| Support / Résistance | Pivot points + swing highs/lows pour placement des strikes |
| IV Rank (252j) | Décision buy vs sell volatility |

---

## Périmètre MVP (usage personnel)

**Inclus :**
- Screener + Signal Engine + Analyzer + Portfolio Tracker + Trade Journal
- Authentification simple (session locale, pas de multi-users)
- Polygon.io intégration complète
- Calculs Black-Scholes, Monte Carlo, Greeks
- Tous les indicateurs techniques listés

**Hors périmètre MVP :**
- Multi-utilisateurs / communauté
- Exécution d'ordres (connexion broker)
- Mobile app
- Backtesting automatisé

---

## Déploiement et coûts

| Service | Plan | Coût mensuel |
|---|---|---|
| Vercel | Hobby | $0 |
| Railway | Starter | $5 |
| Supabase | Free tier | $0 |
| Polygon.io | Options Starter | $29 |
| **Total** | | **~$34/mois** |
