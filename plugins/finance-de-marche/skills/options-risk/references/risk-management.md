# Risk Management

Référence approfondie sur le position sizing, la gestion des pertes, les Greeks de portefeuille, la VaR, l'analyse technique, le sentiment et l'options flow.

---

## Table of Contents

1. [Position Sizing](#position-sizing)
2. [Max Loss Calculations](#max-loss-calculations)
3. [R-Multiples & Trade Expectancy](#r-multiples--trade-expectancy)
4. [Correlation & Diversification](#correlation--diversification)
5. [Stop-Loss Strategies for Options](#stop-loss-strategies-for-options)
6. [Portfolio Greeks Management](#portfolio-greeks-management)
7. [VaR & Expected Shortfall](#var--expected-shortfall)
8. [Technical Analysis for Options](#technical-analysis-for-options)
9. [Sentiment Analysis](#sentiment-analysis)
10. [Options Flow Analysis](#options-flow-analysis)

---

## Position Sizing

### Le Position Sizing Détermine le Résultat

Le position sizing est le facteur le plus important de la performance à long terme. Un edge modeste (slight positive expectancy) combiné avec un sizing discipliné génère des résultats supérieurs à un edge important avec un sizing erratique. Ne jamais déterminer la taille d'une position sans un calcul explicite du risque.

### Fixed Fractional Method (Risque fixe par trade)

La méthode la plus simple et la plus robuste pour les particuliers et les gestionnaires non-systématiques :

```
Nombre de contrats = (Capital x % de risque par trade) / Max loss par contrat

Exemple :
  Capital = 100,000$
  Risque par trade = 2%
  Budget de risque = 100,000 x 0.02 = 2,000$
  Iron condor avec max loss = 400$ par contrat
  Nombre de contrats = 2,000 / 400 = 5 contrats
```

**Paramètres recommandés** :

| Profil de risque | % par trade | % total du portefeuille | Positions simultanées max |
|---|---|---|---|
| Conservateur | 1-2% | 15-25% | 10-15 |
| Modéré | 2-3% | 25-40% | 8-12 |
| Agressif | 3-5% | 40-60% | 5-8 |

**Règle absolue** : ne jamais dépasser 5% du capital en risque sur une seule position, quelle que soit la conviction.

### Kelly Criterion

Le Kelly Criterion détermine la fraction optimale du capital à risquer pour maximiser la croissance géométrique du portefeuille.

```
f* = (b * p - q) / b

Où :
  f* = fraction optimale du capital à risquer
  b  = ratio gain moyen / perte moyenne (ex : si gain moyen = 200$ et perte moyenne = 400$, b = 0.5)
  p  = probabilité de gain
  q  = probabilité de perte = 1 - p

Exemple pour un iron condor :
  Probabilité de profit (POP) = 70% → p = 0.70, q = 0.30
  Gain moyen quand profitable = 150$ (50% du crédit max de 300$)
  Perte moyenne quand perdant = 500$ (max loss 600$ avec stop à 2x)
  b = 150 / 500 = 0.30

  f* = (0.30 x 0.70 - 0.30) / 0.30 = (0.21 - 0.30) / 0.30 = -0.30

  Kelly négatif → cette stratégie avec ces paramètres n'a pas d'edge positif !
  Ne pas trader sans un edge positif vérifié.
```

**Recalcul avec un vrai edge** :

```
Probabilité de profit = 75%, gain moyen = 200$, perte moyenne = 400$
b = 200/400 = 0.5
f* = (0.5 x 0.75 - 0.25) / 0.5 = (0.375 - 0.25) / 0.5 = 0.25 = 25%

ATTENTION : le Kelly plein (25%) est TROP AGRESSIF en pratique.
La volatilité du portefeuille serait insoutenable.

Utiliser le DEMI-KELLY : f*/2 = 12.5%
Ou le QUART-KELLY : f*/4 = 6.25% pour un confort maximal.
```

**Pourquoi le demi-Kelly** : le Kelly Criterion suppose une connaissance parfaite des probabilités et des paramètres de gain/perte, ce qui n'est jamais le cas en pratique. L'erreur d'estimation rend le Kelly plein excessivement risqué. Le demi-Kelly :
- Réduit le drawdown maximum de ~50%.
- Sacrifie seulement ~25% du taux de croissance optimal.
- Offre un meilleur profil risque/rendement dans un monde d'incertitude.

### Buying Power Utilization

Au-delà du risque par trade, surveiller l'utilisation globale du Buying Power (BP) :

```
BP Utilization = Buying Power Used / Total Buying Power

Seuils :
  < 30% : Conservateur (beaucoup de marge pour les ajustements)
  30-50% : Modéré (position manageable)
  50-70% : Agressif (risque de margin call en cas de mouvement adverse)
  > 70% : Danger (margin call probable, réduire les positions immédiatement)
```

**Règle** : maintenir le BP Utilization < 50% en conditions normales et < 30% avant un événement macro majeur (FOMC, NFP, CPI).

---

## Max Loss Calculations

### Par Type de Stratégie

Calculer le max loss AVANT d'entrer chaque position :

| Stratégie | Max Loss | Formule |
|---|---|---|
| Long call / Long put | Premium payé | Premium x 100 |
| Short (naked) call | Théoriquement illimité | (S_final - Strike - Premium) x 100 |
| Short (naked) put | (Strike - Premium) x 100 | Si S -> 0 |
| Cash-secured put | (Strike - Premium) x 100 | Si S -> 0 |
| Covered call | (Prix d'achat - Premium) x 100 | Si S -> 0 |
| Bull call spread | Net debit x 100 | Debit payé |
| Bear put spread | Net debit x 100 | Debit payé |
| Bull put spread (credit) | (K_short - K_long - Credit) x 100 | Largeur - Crédit |
| Bear call spread (credit) | (K_long - K_short - Credit) x 100 | Largeur - Crédit |
| Iron condor | max(put spread width, call spread width) - Credit | Pire jambe - Crédit |
| Iron butterfly | Wing width - Credit | Largeur wing - Crédit |
| Straddle (long) | Total premium payé | Somme des premiums |
| Strangle (long) | Total premium payé | Somme des premiums |
| Calendar spread | Net debit payé (approx.) | Debit initial |

### Scénario d'Analyse de Max Loss

Pour chaque trade, remplir cette matrice :

```
┌──────────────────────────────────────────────────────────────┐
│ TRADE ANALYSIS CARD                                          │
├──────────────────────────────────────────────────────────────┤
│ Sous-jacent : ________    Prix actuel : ________             │
│ Stratégie : ________      Expiration : ________              │
│                                                              │
│ Max Profit : ________ $   (si S à expiration = ________)     │
│ Max Loss   : ________ $   (si S à expiration = ________)     │
│ Breakeven  : ________ $   (sup: ________ / inf: ________)    │
│                                                              │
│ Ratio Risque/Rendement : ________ : 1                        │
│ POP (Probability of Profit) : ________%                      │
│ Rendement annualisé (si max profit) : ________%              │
│                                                              │
│ Capital à risque : ________ $ = ________% du portefeuille    │
│ Position size (contrats) : ________                          │
│                                                              │
│ Règles de management :                                       │
│   Close at ________% profit                                  │
│   Close at ________$ loss                                    │
│   Roll si S atteint ________                                 │
│   Close si earnings dans ________ jours                      │
└──────────────────────────────────────────────────────────────┘
```

---

## R-Multiples & Trade Expectancy

### R-Multiple Framework (Van Tharp)

Le R-multiple normalise chaque trade par rapport au risque initial, permettant de comparer des trades de tailles différentes.

```
R = Risque initial par trade (max loss défini à l'entrée)

R-Multiple du trade = P&L réel / R

Exemples :
  Trade 1 : risque = 500$, profit = 750$ → R-multiple = +1.5R
  Trade 2 : risque = 300$, perte = 300$ → R-multiple = -1.0R
  Trade 3 : risque = 400$, profit = 200$ → R-multiple = +0.5R
  Trade 4 : risque = 500$, perte = 750$ (stop raté) → R-multiple = -1.5R
```

### Expectancy (Espérance mathématique)

```
Expectancy = (Win% x Average Win in R) + (Loss% x Average Loss in R)

Ou de manière équivalente :
Expectancy = (Win% x Avg Winner) - (Loss% x Avg Loser)

Exemple pour un portefeuille d'iron condors :
  Win rate = 72%
  Average winner = +0.5R (closing at 50% profit)
  Average loser = -1.5R (stop at 2x credit)

  Expectancy = (0.72 x 0.5) + (0.28 x -1.5) = 0.36 - 0.42 = -0.06R

  Edge négatif ! Malgré un win rate de 72%, l'asymétrie des gains/pertes
  rend la stratégie perdante. Solutions :
  a) Améliorer le stop-loss (limiter les pertes à -1.0R → Expectancy = +0.08R)
  b) Améliorer le win rate (à 80% → Expectancy = +0.10R)
  c) Les deux.
```

### Profit Factor

```
Profit Factor = Somme des gains / Somme des pertes

> 2.0 : Excellent
1.5-2.0 : Bon
1.0-1.5 : Marginal (attention aux frais et slippage)
< 1.0 : Perdant
```

### System Quality Number (SQN) -- Van Tharp

```
SQN = sqrt(N) x Expectancy / StdDev(R-multiples)

Où N = nombre de trades, minimum 30 pour significativité

Interprétation :
  < 1.6 : Système médiocre
  1.6-2.0 : Système moyen
  2.0-3.0 : Bon système
  3.0-5.0 : Excellent système
  > 5.0 : Système exceptionnel (vérifier l'overfitting)
```

---

## Correlation & Diversification

### Risque de Corrélation dans un Portefeuille d'Options

Le piège majeur des portefeuilles d'options income (iron condors, strangles courts) est la corrélation latente :

**Scénario typique** :
```
Portefeuille : 5 iron condors sur AAPL, MSFT, GOOGL, AMZN, META
  → Apparence de diversification (5 sous-jacents)
  → Réalité : corrélation de ~0.70 entre ces 5 tech stocks
  → En cas de sell-off tech, les 5 positions perdent simultanément
  → Le risque réel est ~3x le risque perçu
```

### Mesure de la Corrélation

```
Corrélation (Pearson) entre les rendements de deux actifs :

ρ(A,B) = Cov(R_A, R_B) / (σ_A x σ_B)

  ρ = +1.0 : corrélation parfaite (pas de diversification)
  ρ = 0.0 : indépendance (diversification maximale)
  ρ = -1.0 : corrélation inverse (hedging parfait)
```

### Rules of Diversification pour les Options

| Règle | Seuil | Raison |
|---|---|---|
| Max par sous-jacent | 5% du capital en risque | Limiter le single-name risk |
| Max par secteur | 25% du capital en risque | Les actions du même secteur sont fortement corrélées |
| Max par expiration | 30% du capital en risque | Éviter le risque de concentration temporelle |
| Diversification temporelle | Minimum 3 expirations | Lisser le theta et le gamma risk |
| Corrélation max entre positions | Vérifier ρ < 0.60 | Maintenir une vraie diversification |
| Positions delta-neutral | < 20% du portefeuille en delta net | Limiter l'exposition directionnelle non intentionnelle |

### Beta-Weighted Portfolio Analysis

Convertir toutes les positions en "SPY-equivalent" pour évaluer l'exposition directionnelle globale :

```
Beta-Weighted Delta = Position Delta x Beta du sous-jacent vs SPY

Exemple :
  Position 1 : Long 10 AAPL calls, delta = 0.50 par contrat, AAPL beta = 1.20
    BW Delta = 10 x 100 x 0.50 x 1.20 = +600 SPY-equivalent shares

  Position 2 : Short 5 XLU puts, delta = -0.30 par contrat, XLU beta = 0.40
    BW Delta = 5 x 100 x (-0.30) x 0.40 = -60 SPY-equivalent shares

  Portfolio BW Delta = +600 - 60 = +540 SPY-equivalent shares
  → Le portefeuille est long de l'équivalent de 540 actions SPY
```

---

## Stop-Loss Strategies for Options

### Pourquoi les Stop-Loss Standards ne Fonctionnent Pas pour les Options

Les stop-loss sur le prix de l'option sont problématiques :
- L'option peut perdre de la valeur due au theta (sans mouvement du sous-jacent) et déclencher un stop.
- Les spreads bid-ask larges pendant les heures de faible liquidité peuvent déclencher des stops erronés.
- Un gap overnight peut sauter le stop entièrement.

### Approches Alternatives

**Stop basé sur le sous-jacent** (recommandé) :

```
Pour un iron condor :
  Stop si le sous-jacent atteint le short strike → clôturer la jambe menacée

Pour un vertical spread credit :
  Stop si le sous-jacent dépasse le short strike de X%

Pour un covered call / CSP :
  Stop si le sous-jacent casse un support technique majeur
```

**Stop basé sur la perte en dollars** :

```
Pour les stratégies crédit :
  Stop si la perte = 2x le crédit reçu

  Exemple : iron condor ouvert pour 1.50$ de crédit
  Stop quand le coût de clôture atteint 4.50$ (perte de 3.00$ = 2x le crédit)
```

**Stop basé sur le delta** :

```
Pour les positions courtes (short options) :
  Stop si le delta du short strike dépasse 0.50 (ATM)

  Exemple : short put ouvert à delta -0.25
  Si le sous-jacent baisse et que le delta atteint -0.50, clôturer ou roller
```

**Stop basé sur le temps** :

```
Pour les stratégies income :
  Si le profit n'est pas atteint à 21 DTE (ouvert à 45 DTE), clôturer
  La zone 21-0 DTE est la zone de gamma risk maximum
```

---

## Portfolio Greeks Management

### Delta Management

Le delta net du portefeuille mesure l'exposition directionnelle totale.

```
Portfolio Delta = SUM(position_i.delta x quantity_i x multiplier_i)

Objectifs :
  Trading directionnel : delta net aligné avec la vue (positif = bullish)
  Trading de volatilité : delta-neutral (delta net ≈ 0)
  Income strategies : léger biais (typiquement légèrement delta-positif)
```

**Delta-Neutral Hedging** :
- Ajuster le delta net en achetant/vendant des actions du sous-jacent ou de l'ETF de référence (SPY).
- Fréquence de rebalancement : quotidien pour les traders actifs, hebdomadaire pour les positions income.
- Coût du rebalancement : chaque ajustement génère des frais de transaction. Le rebalancement optimal est un trade-off entre le risque de delta drift et le coût.

### Gamma Management

```
Portfolio Gamma = SUM(position_i.gamma x quantity_i x multiplier_i)

Gamma positif : la position s'auto-ajuste favorablement (acheteur d'options)
Gamma négatif : la position se dégrade en cas de mouvement (vendeur d'options)
```

**Stress test gamma** : calculer l'impact d'un mouvement de +/- 1, 2 et 3 écarts-types du sous-jacent sur le P&L du portefeuille.

```
P&L approximatif pour un mouvement ΔS :
  ΔP&L ≈ Delta * ΔS + 0.5 * Gamma * (ΔS)^2

Pour un portefeuille short gamma (iron condors, strangles courts) :
  Un mouvement de 2σ (environ 2%) du S&P 500 ≈ une perte de :
  ΔP&L = Delta * (2%*S) + 0.5 * Gamma * (2%*S)^2
```

### Theta Management

```
Portfolio Theta = SUM(position_i.theta x quantity_i x multiplier_i)

Objectif : theta positif pour les stratégies income
  → Le portefeuille gagne de la valeur chaque jour (si le sous-jacent ne bouge pas)

Theta comme "salaire quotidien" du vendeur de premium :
  Portfolio theta de +150$/jour = le portefeuille gagne ~150$/jour en valeur temporelle
  Sur 30 jours = ~4,500$ de theta income (avant tout mouvement du sous-jacent)
```

**Ratio Theta/BPR** : mesure de l'efficacité du capital pour les stratégies income.

```
Theta/BPR = (Portfolio Theta x 365) / Buying Power Used

Objectif : > 10% annualisé après frais

Exemple :
  Theta quotidien = +200$
  BPR utilisé = 500,000$
  Theta/BPR = (200 x 365) / 500,000 = 14.6% annualisé
```

### Vega Management

```
Portfolio Vega = SUM(position_i.vega x quantity_i x multiplier_i)

Vega positif : le portefeuille profite d'une hausse de la volatilité
Vega négatif : le portefeuille profite d'une baisse de la volatilité
```

**Vega-neutral strategies** : pour les traders de volatilité qui veulent isoler le gamma du vega, ou pour les income traders qui veulent réduire leur exposition à un spike de vol.

```
Exemple de hedging vega :
  Portefeuille d'iron condors : vega net = -500 (short 500$ de vega)
  Si le VIX augmente de 5 points → perte ≈ 500 x 5 = 2,500$

  Hedging : acheter des options sur le VIX ou des calls sur VXX/UVXY
  pour compenser le vega négatif du portefeuille principal.
```

### Dashboard de Greeks Agrégés

Maintenir un tableau de bord quotidien :

```
┌────────────────────────────────────────────────┐
│ PORTFOLIO GREEKS DASHBOARD                     │
├────────────────────────────────────────────────┤
│ Net Delta (beta-weighted SPY) : +350 shares    │
│ Net Gamma :                    -45             │
│ Net Theta :                    +185 $/day      │
│ Net Vega :                     -620            │
│                                                │
│ BP Utilization :               38%             │
│ Max position % :               4.2% (AAPL)    │
│ Sector concentration :         22% (Tech)      │
│ Expirations : 3 (Mar 21, Apr 18, May 16)      │
│                                                │
│ Stress test -5% SPY :         -3,200$          │
│ Stress test +5% SPY :         -1,100$          │
│ Stress test VIX +10 pts :     -6,200$          │
└────────────────────────────────────────────────┘
```

---

## VaR & Expected Shortfall

### Value at Risk (VaR)

La VaR mesure la perte maximale attendue sur un horizon donné avec un niveau de confiance spécifié.

```
VaR(α, T) = perte telle que P(Loss > VaR) = 1 - α

Exemple : VaR(95%, 1 jour) = 5,000$
  → Il y a 95% de probabilité que la perte journalière ne dépasse pas 5,000$
  → Ou : la perte dépassera 5,000$ environ 1 jour sur 20 (5% du temps)
```

**Méthodes de calcul** :

**VaR paramétrique (variance-covariance)** :

```
VaR = Portefeuille_Value x σ_portfolio x Z_α x sqrt(T)

Où :
  σ_portfolio = volatilité du portefeuille (annualisée)
  Z_α = quantile de la loi normale (1.645 pour 95%, 2.326 pour 99%)
  T = horizon en fraction d'année (1/252 pour un jour)

Exemple :
  Portefeuille = 500,000$
  σ = 15% annualisée
  VaR 95% 1-jour = 500,000 x 0.15 x 1.645 x sqrt(1/252) = 500,000 x 0.15 x 1.645 x 0.063 = 7,773$
```

**VaR historique** :
- Prendre les 252 derniers rendements quotidiens du portefeuille.
- Trier par ordre croissant.
- Le 5ème percentile (ou le 13ème rendement le plus faible sur 252) est la VaR 95%.
- Plus robuste car ne suppose pas de distribution normale.

**VaR Monte Carlo** :
- Simuler 10,000+ trajectoires de prix pour le portefeuille.
- Calculer le P&L sur l'horizon T pour chaque trajectoire.
- Le 5ème percentile des P&L est la VaR 95%.
- La plus flexible pour les portefeuilles d'options (capture le gamma risk).

### Expected Shortfall (CVaR / Conditional VaR)

La VaR ne dit rien sur l'ampleur des pertes au-delà du seuil. L'Expected Shortfall (ES) comble cette lacune.

```
ES(α) = E[Loss | Loss > VaR(α)]

C'est la perte moyenne dans les (1-α)% des pires scénarios.

Exemple :
  VaR 95% 1-jour = 5,000$
  ES 95% 1-jour = 8,200$
  → Dans les 5% des pires jours, la perte moyenne est de 8,200$ (pas juste 5,000$)
```

**Pourquoi l'ES est supérieur à la VaR** :
- La VaR n'est pas subadditive (VaR du portefeuille peut > somme des VaR individuelles).
- La VaR ignore les queues de distribution (fat tails).
- L'ES est cohérent (subadditif) et capture le risque de queue.
- Bâle III/IV recommandent l'ES comme mesure de risque de marché.

### Application aux Portefeuilles d'Options

La VaR paramétrique est INADÉQUATE pour les portefeuilles d'options car :
- Le profil de P&L est non-linéaire (gamma, vega).
- Les rendements ne sont pas normalement distribués.
- Les corrélations changent en période de stress (correlation breakdown).

**Approche recommandée** : VaR Monte Carlo avec :
- Processus stochastique multi-facteurs (prix, volatilité, taux).
- Chocs corrélés entre sous-jacents.
- Réévaluation complète des options à chaque pas de la simulation (full repricing).

---

## Technical Analysis for Options

### Niveaux Techniques pour le Placement des Strikes

L'analyse technique n'est pas utilisée pour prédire la direction du marché mais pour **identifier des niveaux de prix significatifs** pour le placement optimal des strikes.

### Support et Résistance

```
Identifier les niveaux clés :
  - Previous highs/lows (52-week, all-time)
  - Round numbers psychologiques (100, 200, 500...)
  - Zones de volume élevé (Volume Profile / VPOC)
  - Gaps non comblés
  - Niveaux de Fibonacci (38.2%, 50%, 61.8% de retracement)
```

**Application aux options** :
- **Short put strike** : placer en dessous d'un support majeur identifié.
- **Short call strike** : placer au-dessus d'une résistance majeure.
- **Wings de l'iron condor** : placer au-delà des supports/résistances secondaires.

### Moyennes Mobiles

```
SMA (Simple Moving Average) : moyenne arithmétique des N derniers prix de clôture
EMA (Exponential Moving Average) : pondérée exponentiellement (plus de poids aux données récentes)

MM clés : SMA 20, SMA 50, SMA 200
  - Prix > SMA 200 : tendance haussière long terme (favorable pour CSP/covered call)
  - Prix < SMA 200 : tendance baissière long terme (prudence pour la Wheel)
  - Golden Cross (SMA 50 > SMA 200) : signal haussier
  - Death Cross (SMA 50 < SMA 200) : signal baissier
```

### Expected Move (EM)

Calculer le mouvement attendu implicite pour une période donnée :

```
Expected Move = Prix x IV x sqrt(DTE/365)

Ou approximation à partir du prix du straddle ATM :
EM ≈ Straddle Price x 0.85  (ajustement pour la distribution log-normale)

Exemple :
  AAPL à 180$, IV = 25%, expiration dans 30 jours
  EM = 180 x 0.25 x sqrt(30/365) = 180 x 0.25 x 0.287 = 12.90$
  Range attendu = [167.10, 192.90] à ~68% de probabilité (1 écart-type)
  Range 2σ = [154.20, 205.80] à ~95% de probabilité
```

**Usage** : les short strikes d'un iron condor devraient être positionnés au-delà de l'expected move pour avoir une POP > 50%.

### Bollinger Bands

```
Upper Band = SMA(20) + 2 x σ(20)
Lower Band = SMA(20) - 2 x σ(20)

Application options :
  Prix touchant la bande inférieure : zone favorable pour vendre un CSP
  Prix touchant la bande supérieure : zone favorable pour vendre un covered call
  Squeeze de Bollinger (bandes contractées) : anticipation d'un mouvement, favorable pour un long straddle
```

---

## Sentiment Analysis

### Indicateurs de Sentiment Marché

Intégrer le sentiment comme filtre contrarian pour le timing des positions d'options.

### VIX (CBOE Volatility Index)

```
VIX = "Fear Gauge" du marché
  Mesure l'IV à 30 jours des options SPX (S&P 500)

Niveaux de référence :
  VIX < 15 : Complaisance / faible volatilité (acheter des protections bon marché)
  VIX 15-20 : Zone normale
  VIX 20-30 : Anxiété élevée (vendre du premium)
  VIX 30-40 : Peur significative (premium très élevé, opportunité de vente)
  VIX > 40 : Panique (extrême, timing délicat pour les ventes)
```

**VIX Term Structure** :
- Contango (VIX spot < VIX futures) : état normal, pas de panique.
- Backwardation (VIX spot > VIX futures) : peur immédiate, marché stressé.
- La normalisation du VIX (retour de backwardation vers contango) est un signal d'accalmie.

### AAII Sentiment Survey

```
AAII (American Association of Individual Investors) Sentiment Survey :
  % Bullish, % Bearish, % Neutral (publié chaque jeudi)

Signal contrarian :
  Bullish > 50% : Excès d'optimisme → potentiellement bearish
  Bearish > 50% : Excès de pessimisme → potentiellement bullish
  Bull-Bear spread < -20% : Signal contrarian bullish fort
  Bull-Bear spread > +30% : Signal contrarian bearish fort
```

### Fear & Greed Index (CNN)

Composite de 7 indicateurs de sentiment :
- VIX, Put/Call ratio, Market momentum, Junk bond demand, Stock price breadth, Market volatility, Safe haven demand.
- Score de 0 (peur extrême) à 100 (avidité extrême).
- Utiliser comme filtre contrarian pour le timing.

### Intégration du Sentiment dans les Décisions d'Options

| Sentiment | VIX | Action options |
|---|---|---|
| Peur extrême | > 35 | Vendre du premium agressivement (iron condors larges, CSP) |
| Peur modérée | 25-35 | Vendre du premium avec prudence (taille réduite) |
| Neutre | 15-25 | Stratégies standard, sizing normal |
| Complaisance | < 15 | Acheter des protections (puts OTM bon marché), réduire les ventes de premium |
| Avidité extrême | < 12 | Réduire l'exposition, acheter des hedges, potentiel de correction élevé |

---

## Options Flow Analysis

### Qu'est-ce que l'Options Flow ?

L'analyse du flow d'options consiste à surveiller les transactions d'options en temps réel pour détecter le positionnement des institutionnels et des "smart money".

### Détection de l'Unusual Activity

**Critères** :
- Volume du jour > 3x-5x le volume moyen sur 20 jours.
- Transactions exécutées au ask (achat agressif) ou au bid (vente agressive).
- Transactions de grande taille (> 500-1,000 contrats en un seul lot).
- Activité sur des expirations inhabituelles (pas les expirations mensuelles standards).
- Ratio volume/OI > 2 (beaucoup de nouvelles positions ouvertes).

### Classification des Trades

| Type | Description | Signal |
|---|---|---|
| Sweep | Ordre exécuté sur plusieurs exchanges simultanément pour obtenir un fill rapide | Urgence / conviction élevée |
| Block | Transaction unique de grande taille (> 500 contrats) | Institutionnel |
| Split | Ordre divisé en plusieurs tranches sur plusieurs minutes | Tentative de discrétion |

### Interprétation des Flows

```
Achats agressifs de calls (au ask) :
  → Conviction haussière forte
  → Si combiné avec volume > 5x moyenne : potentiel "smart money" information

Achats agressifs de puts (au ask) :
  → Conviction baissière OU hedging de portefeuille
  → Distinguer : hedging = puts OTM loin, spéculation = puts ATM/légèrement OTM

Ventes de puts (au bid) :
  → Conviction haussière (vendeur est long le sous-jacent implicitement)
  → Si sur des strikes bas (OTM) : confidence que le prix ne descendra pas

Spreads complexes :
  → Généralement institutionnels
  → Analyser la structure pour comprendre la thèse
```

### Dark Pool & Block Trades

Surveiller les transactions hors marché (dark pools) pour les actions sous-jacentes :
- Les gros blocs d'actions tradés hors marché peuvent signaler un positionnement institutionnel.
- Combiner avec l'options flow : si des achats d'actions en dark pool sont accompagnés d'achats de calls, le signal est renforcé.

### GEX (Gamma Exposure) et DEX (Delta Exposure)

**GEX (Gamma Exposure)** :
```
GEX total = SUM(OI * Gamma * 100 * S) pour tous les contrats

GEX positif (dealers sont long gamma) :
  → Les dealers achètent quand ça baisse, vendent quand ça monte
  → Effet stabilisant, volatilité comprimée
  → Favorable pour les stratégies income (iron condors)

GEX négatif (dealers sont short gamma) :
  → Les dealers vendent quand ça baisse, achètent quand ça monte
  → Effet amplificateur, volatilité élevée
  → Risqué pour les stratégies income, favorable pour les achats de volatilité
```

### Outils et Sources de Données

**Sources de flow en temps réel** (exemples, pas exhaustif) :
- CBOE (données officielles de volume et OI)
- Plateformes de courtage avancées (thinkorswim, IBKR, Tastyworks)
- Services spécialisés options flow (accès aux données agrégées et filtrées)
- Dark pool data (FINRA ATS data, publiée avec délai)

---

## Summary Checklist

### Position sizing (avant chaque trade) :

- [ ] Max loss calculé en dollars
- [ ] Risque par trade < 5% du capital (idéalement 1-3%)
- [ ] Kelly Criterion évalué (demi-Kelly appliqué)
- [ ] BP Utilization < 50% après ouverture
- [ ] Corrélation avec les positions existantes vérifiée
- [ ] Diversification sectorielle et temporelle maintenue

### Risk management continu (quotidien) :

- [ ] Portfolio Greeks dashboard mis à jour
- [ ] Delta net beta-weighted calculé
- [ ] Stress test SPY +/-5% et VIX +10pts effectué
- [ ] Stop-loss et targets vérifiés pour chaque position
- [ ] Calendrier des événements vérifié (earnings, FOMC, CPI)
- [ ] VIX et VIX term structure analysés
- [ ] Options flow inhabituel surveillé

### Post-trade analysis (après chaque clôture) :

- [ ] R-multiple du trade calculé et journalisé
- [ ] Expectancy du système mise à jour (running average)
- [ ] Profit factor recalculé
- [ ] Erreurs de management identifiées et documentées
- [ ] Leçons extraites pour calibrer les paramètres futurs
