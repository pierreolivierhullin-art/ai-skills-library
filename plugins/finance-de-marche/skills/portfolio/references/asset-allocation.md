# Asset Allocation — Strategic, Tactical, Factor-Based & Advanced Strategies

## Overview

Ce document de reference couvre les strategies d'allocation d'actifs, du strategique au tactique, en passant par les approches avancees (risk parity, endowment model, factor-based). L'allocation d'actifs est le determinant principal de la performance d'un portefeuille a long terme : selon Brinson, Hood & Beebower (1986, 1991), plus de 90% de la variabilite des rendements d'un portefeuille s'explique par l'allocation strategique, non par la selection de titres ou le market timing. Utiliser ce guide pour structurer toute decision d'allocation.

This reference covers asset allocation strategies from strategic to tactical, including advanced approaches (risk parity, endowment model, factor-based). Asset allocation is the primary determinant of long-term portfolio performance. Use this guide to structure all allocation decisions.

---

## Strategic Asset Allocation (SAA)

### Definition et principes / Definition and Principles

L'allocation strategique definit les poids cibles a long terme pour chaque classe d'actifs, basee sur les rendements attendus, les risques et les correlations historiques, l'horizon d'investissement et la tolerance au risque de l'investisseur. La SAA represente le "plan de vol" du portefeuille et ne doit etre modifiee que lors de changements structurels (objectifs, horizon, contraintes).

Strategic allocation defines long-term target weights for each asset class. It represents the portfolio's "flight plan" and should only be modified upon structural changes in objectives, horizon, or constraints.

### Asset Classes — Caracteristiques / Asset Class Characteristics

| Classe d'actifs | Rendement reel historique (annualise) | Volatilite | Role dans le portefeuille |
|---|---|---|---|
| **Actions marches developpes** | 5-7% | 15-20% | Moteur de croissance, prime de risque actions |
| **Actions marches emergents** | 6-9% | 20-30% | Croissance superieure, diversification geographique |
| **Obligations souveraines (investment grade)** | 1-3% | 4-8% | Stabilisateur, couverture deflation, flight to quality |
| **Obligations corporate (IG)** | 2-4% | 6-10% | Rendement superieur aux souveraines, credit spread |
| **Obligations high yield** | 4-6% | 10-15% | Rendement eleve, comportement hybride actions/credit |
| **TIPS / OATi (inflation-linked)** | 1-2% | 5-8% | Couverture inflation |
| **Immobilier (REITs)** | 4-6% | 15-20% | Revenus reguliers, couverture inflation, diversification |
| **Matieres premieres** | 0-2% | 15-25% | Couverture inflation, diversification (faible correlation) |
| **Or** | 0-1% | 15-20% | Valeur refuge, couverture geopolitique, correlation negative en crise |
| **Private Equity** | 8-12% (brut) | 15-25% (lisse) | Prime d'illiquidite, alpha operationnel, horizon > 7 ans |
| **Hedge Funds** | 3-6% | 5-12% | Rendements decoreles, alpha, strategies alternatives |
| **Infrastructure** | 5-8% | 10-15% | Revenus stables, inflation-linked, horizon long |
| **Cash / Money Market** | 0-1% (reel) | < 1% | Liquidite, opportunisme, attente |

### Modeles d'allocation classiques / Classic Allocation Models

#### Conservative (Defensif)
- Actions : 20-30%
- Obligations : 50-60%
- Alternatives/Immobilier : 5-10%
- Cash : 5-10%
- Profil : horizon < 5 ans, faible tolerance au drawdown, besoin de revenus

#### Balanced (Equilibre)
- Actions : 50-60%
- Obligations : 30-40%
- Alternatives/Immobilier : 5-10%
- Cash : 0-5%
- Profil : horizon 5-15 ans, tolerance au drawdown moderee (15-25%)

#### Growth (Croissance)
- Actions : 70-85%
- Obligations : 10-20%
- Alternatives/Immobilier : 5-10%
- Cash : 0-5%
- Profil : horizon > 15 ans, haute tolerance au drawdown (25-40%)

#### Aggressive (Agressif)
- Actions : 85-100%
- Obligations : 0-10%
- Alternatives : 0-10%
- Profil : horizon > 20 ans, tres haute tolerance, capacite financiere a absorber des pertes majeures

### Capital Market Assumptions (CMAs)

Produire ou utiliser des CMAs (previsions a long terme de rendements, volatilites et correlations par classe d'actifs) comme inputs pour l'optimisation. Les grandes maisons de gestion (BlackRock, Vanguard, J.P. Morgan, AQR) publient annuellement leurs CMAs sur un horizon 10-15 ans. Utiliser les CMAs comme point de depart, en les ajustant selon les conditions de marche (CAPE ratio, spreads de credit, taux reels).

Regles pratiques pour ajuster les rendements attendus :
- **Actions** : rendement attendu = 1/CAPE + croissance des benefices attendue (typiquement 1-2% reel). Quand CAPE > 30, reduire les attentes.
- **Obligations** : rendement attendu ~ yield to maturity actuel (le meilleur predicteur pour les obligations investment grade).
- **Credit** : rendement = yield souverain + spread de credit - pertes de credit attendues.
- **Alternatives** : rendement = beta marche + prime d'illiquidite (2-4%) + alpha (incertain).

---

## Tactical Asset Allocation (TAA)

### Definition et principes / Definition and Principles

L'allocation tactique consiste a devier temporairement de l'allocation strategique pour exploiter des opportunites de marche a court-moyen terme (3-18 mois). La TAA suppose une forme d'inefficience de marche exploitable par le gestionnaire.

Tactical allocation involves temporarily deviating from strategic allocation to exploit short-to-medium term market opportunities. It assumes some form of exploitable market inefficiency.

### Signaux pour la TAA / TAA Signals

| Signal | Indicateur | Interpretation |
|---|---|---|
| **Valuation** | CAPE (Shiller P/E), Yield Gap (earnings yield - bond yield) | CAPE > 30 : reduire actions ; CAPE < 15 : surponderer |
| **Momentum** | Moyennes mobiles (10M, 12M), cross-sectional momentum | Prix > MA10 : rester investi ; Prix < MA10 : reduire exposition |
| **Macro** | PMI, yield curve slope, credit spreads, unemployment claims | Inversion yield curve : signal recessionniste (delai 12-18 mois) |
| **Sentiment** | VIX, put/call ratio, AAII survey, fund flows | VIX > 35 : opportunite d'achat contrarian ; VIX < 12 : complaisance |
| **Credit** | Spreads IG/HY, CDS indices (CDX, iTraxx) | Ecartement des spreads : risk-off, tightening : risk-on |
| **Liquidite** | Conditions financieres (FCI), bilan des banques centrales | Conditions accommodantes : favorable aux actifs risques |

### Regles de TAA / TAA Rules

- **Limiter les deviations** : la TAA ne devrait pas devier de plus de +/- 10% de l'allocation strategique par classe d'actifs. Des deviations plus larges transforment la TAA en market timing.
- **Documenter chaque decision** : chaque mouvement tactique doit avoir un signal identifie, une these explicite, un horizon de retour attendu et un stop-loss.
- **Budget de risque TAA** : allouer un budget de tracking error specifique a la TAA (ex: 1-3% de tracking error vs SAA). Cela discipline la prise de risque active.
- **Evaluer systematiquement** : mesurer la contribution de la TAA via l'attribution de performance. Si la TAA ne genere pas d'alpha net de couts sur 3-5 ans, la supprimer.

### Trend-Following as TAA

L'approche momentum/trend-following est l'une des rares strategies TAA avec des preuves empiriques de long terme (200+ ans selon AQR/Moskowitz). Implementer via :
- **Time-series momentum** : comparer le prix actuel a la moyenne mobile 10 ou 12 mois. Si au-dessus, rester investi ; sinon, basculer sur obligations/cash.
- **Dual momentum (Antonacci)** : combiner le momentum absolu (rendement vs cash) et le momentum relatif (rendement vs alternatives). Simple, efficace, faible turnover.
- **Limites** : performant en tendances claires, perd en marches range-bound. Les frais de transaction et le slippage peuvent eroder une part significative de l'alpha.

---

## Core-Satellite Strategy

### Architecture / Architecture

Le modele core-satellite divise le portefeuille en deux composantes complementaires :

**Core (60-80% du portefeuille)** :
- Investissement passif, indiciel, a faible cout (ETFs large cap, world index)
- Objectif : capturer le rendement de marche (beta) avec un minimum de frais
- Rebalancement peu frequent (semestriel ou par bandes)
- Vehicules : ETFs indiciels (MSCI World, S&P 500, Aggregate Bond), fonds indiciels

**Satellite (20-40% du portefeuille)** :
- Investissement actif ou thematique ciblant l'alpha
- Objectif : surperformance vs benchmark, diversification additionnelle, expression de convictions
- Turnover plus eleve, frais plus eleves (justifies par l'alpha attendu)
- Vehicules : ETFs factoriels, fonds actifs specialises, titres individuels, alternatives

### Implementation pratique / Practical Implementation

| Composante | Allocation | Vehicule type | TER moyen | Objectif |
|---|---|---|---|---|
| Core: Actions monde | 40-50% | MSCI World ETF, FTSE All-World ETF | 0.07-0.20% | Beta actions monde |
| Core: Obligations | 15-25% | Global Aggregate Bond ETF | 0.10-0.20% | Stabilisateur, income |
| Satellite: Small Cap Value | 5-10% | Small Cap Value ETF / Fonds actif | 0.20-0.50% | Factor premium (size + value) |
| Satellite: Marches emergents | 5-10% | EM Equity ETF / Fonds actif EM | 0.15-0.60% | Diversification, croissance |
| Satellite: Alternatives | 5-10% | REITs, Gold ETF, Infrastructure | 0.20-0.50% | Diversification, inflation hedge |
| Satellite: Thematique | 0-5% | ETF thematique, titres individuels | 0.30-0.75% | Convictions, innovation |

### Avantages / Advantages
- Controle des couts : le core low-cost ancre les frais globaux
- Flexibilite : les satellites peuvent etre ajustes sans perturber le core
- Discipline : le core empeche le performance chasing sur l'ensemble du portefeuille
- Mesurabilite : l'alpha des satellites est clairement mesurable vs le benchmark core

---

## Risk Parity

### Principes fondamentaux / Fundamental Principles

La risk parity egalise les contributions au risque de chaque classe d'actifs plutot que les allocations en capital. L'idee centrale : dans un portefeuille 60/40 classique, les actions representent ~90% du risque total du portefeuille. La risk parity reequilibre en augmentant l'allocation aux actifs moins risques (obligations) et en utilisant du levier pour atteindre le rendement cible.

Risk parity equalizes risk contributions from each asset class rather than capital allocations. In a classic 60/40 portfolio, equities represent ~90% of total risk. Risk parity rebalances by increasing allocation to lower-risk assets and using leverage to reach target returns.

### Formulation mathematique / Mathematical Formulation

Pour un portefeuille de n actifs, la risk parity cherche les poids wi tels que :

```
RC_i = wi * (Sigma * w)_i / sigma_p = 1/n * sigma_p

soit: wi * (Sigma * w)_i = constante pour tout i
```

ou RC_i est la contribution au risque de l'actif i, Sigma la matrice de covariance et sigma_p la volatilite du portefeuille.

### Bridgewater All Weather — Ray Dalio

Le portefeuille All Weather de Bridgewater est la reference de la risk parity. Il alloue le risque equitablement entre quatre regimes economiques :

| Regime economique | Actifs performants | Allocation approximative |
|---|---|---|
| **Croissance en hausse** | Actions, credit corporate, matieres premieres | 25% du budget de risque |
| **Croissance en baisse** | Obligations souveraines nominales, TIPS | 25% du budget de risque |
| **Inflation en hausse** | TIPS, matieres premieres, or, EM | 25% du budget de risque |
| **Inflation en baisse** | Obligations souveraines nominales, actions growth | 25% du budget de risque |

Allocation approximative en capital (sans levier) : 30% actions, 40% obligations long terme, 15% obligations moyen terme, 7.5% matieres premieres, 7.5% or.

### Avantages et limites / Advantages and Limitations

**Avantages** :
- Robustesse a travers differents regimes economiques (pas de dependance excessive a un seul regime)
- Meilleure diversification effective (Effective N plus eleve)
- Drawdowns historiquement inferieurs a un portefeuille 60/40
- Ne depend pas des estimations de rendements attendus (uniquement covariances)

**Limites** :
- Necessite du levier pour atteindre des rendements comparables a un portefeuille actions (cout du levier, risque de marge)
- Sous-performe en marches haussiers prolonges (bull markets actions)
- Hypothese que les correlations et volatilites sont stables (elles ne le sont pas)
- En regime de hausse de taux simultanee avec baisse des actions (2022), la risk parity souffre car les obligations ne jouent pas leur role de couverture

### Implementation sans levier / Leverage-Free Implementation

Pour les investisseurs individuels ne pouvant pas utiliser de levier, adapter la risk parity en :
- Utilisant des obligations a longue duration (plus volatiles) pour augmenter la contribution au risque des obligations sans levier
- Ajoutant des matieres premieres et de l'or pour diversifier les sources de risque
- Acceptant un rendement attendu inferieur a un portefeuille 100% actions

---

## Factor-Based Allocation

### Philosophie / Philosophy

L'allocation factorielle considere les facteurs de risque (market, value, size, momentum, quality, low vol) comme les briques fondamentales du portefeuille plutot que les classes d'actifs traditionnelles. Deux actifs de classes differentes peuvent avoir des expositions factorielles similaires (ex: actions value et obligations HY sont toutes deux sensibles au facteur de risque economique).

Factor-based allocation considers risk factors as the fundamental building blocks rather than traditional asset classes. Two assets from different classes may share similar factor exposures.

### Implementation strategies

#### Single-Factor Tilts
Surponderer un ou deux facteurs dans un portefeuille indiciel large. Exemple : allouer 70% MSCI World + 30% MSCI World Value pour un tilt value modere. Simple a implementer, faible tracking error, facile a comprendre.

#### Multi-Factor Portfolio
Combiner 3-5 facteurs dans un portefeuille integre. Deux approches :
- **Mixing (portfolio of portfolios)** : combiner des portefeuilles single-factor. Simple mais dilue les expositions factorielles.
- **Integration** : selectionner les titres qui ont des scores eleves sur plusieurs facteurs simultanement. Expositions factorielles plus pures mais plus complexe, moins transparent.

#### Factor Parity
Appliquer le principe de risk parity aux facteurs : egaliser la contribution au risque de chaque facteur. Necessite l'estimation des volatilites et correlations factorielles, qui sont plus stables que les correlations entre actifs.

### Factor Premia — Taille et persistance / Factor Premia — Size and Persistence

| Facteur | Prime historique (annualisee) | Ratio de Sharpe (long/short) | Persistance | Risque principal |
|---|---|---|---|---|
| Market | 5-7% | 0.35-0.45 | Tres haute | Drawdowns profonds (-50%) |
| Value | 3-5% | 0.15-0.30 | Haute (avec periodes creuses longues) | Periodes creuses de 5-15 ans |
| Size | 2-3% | 0.10-0.20 | Moderee (affaiblie post-publication) | Illiquidite, concentration sectorielle |
| Momentum | 6-8% | 0.40-0.60 | Haute | Crash risk severe, correlation negative avec value |
| Quality | 3-5% | 0.30-0.50 | Haute | Cher en entry (valorisations elevees) |
| Low Volatility | 2-4% | 0.40-0.60 | Haute | Sous-performe en bull markets, concentration sectorielle |

---

## Endowment Model (Yale / Swensen)

### Philosophie / Philosophy

David Swensen (Yale Endowment, 1985-2021) a revolutionne la gestion de dotation en allouant massivement aux actifs alternatifs illiquides (PE, venture capital, real assets, hedge funds) au detriment des obligations traditionnelles. L'idee : un horizon d'investissement perpetuel permet de capturer des primes d'illiquidite significatives.

### Allocation type Yale / Typical Yale Allocation

| Classe d'actifs | Allocation | Role |
|---|---|---|
| Venture Capital | 20-25% | Croissance, innovation, alpha operationnel |
| Private Equity (LBO) | 15-20% | Rendement, levier operationnel |
| Absolute Return (Hedge Funds) | 20-25% | Decorrelation, alpha |
| Real Assets (Immobilier, Timber, Infrastructure) | 10-15% | Inflation hedge, revenus |
| Actions cotees (domestic + foreign) | 10-15% | Liquidite, marche public |
| Obligations / Cash | 5-10% | Liquidite, stabilisateur |

### Conditions de succes / Prerequisites for Success

- **Horizon perpetuel** : pas de contrainte de liquidite a court terme
- **Acces aux top-quartile managers** : la dispersion des rendements en PE/VC est enorme (top quartile vs bottom quartile : 10-15% annualise). Sans acces aux meilleurs gestionnaires, le modele perd sa raison d'etre
- **Governance sophistiquee** : comite d'investissement expert, CIO dedie, due diligence rigoureuse
- **Tolerance a l'illiquidite et au J-curve** : les investissements PE/VC ne deviennent profitables qu'apres 3-5 ans
- **Taille critique** : les couts fixes de due diligence et les minimums d'investissement necessitent un portefeuille > 500M USD

### Limites et critique / Limitations and Criticism

- **Survivorship bias** : Yale et quelques dotations d'elite performent, mais la mediane des dotations adoptant ce modele sous-performe un portefeuille 60/40 passif
- **Illiquidite-smoothing** : la volatilite apparemment faible des alternatives est en partie due au lissage des valorisations (mark-to-model vs mark-to-market)
- **Frais eleves** : 2/20 en PE/hedge funds (2% management + 20% performance fee) necessite un alpha brut tres eleve pour justifier les couts nets
- **Complexite operationnelle** : gestion des appels de capitaux, distributions, rapports de valorisation

---

## Lifecycle Allocation (Glide Path)

### Principes / Principles

L'allocation lifecycle reduit progressivement l'exposition aux actifs risques (principalement les actions) a mesure que l'investisseur approche de son objectif (typiquement la retraite). La logique : le capital humain (revenus futurs) diminue avec l'age, donc le capital financier doit devenir plus conservateur pour compenser.

### Glide Path classique / Classic Glide Path

| Age | Actions | Obligations | Alternatives/Cash | Logique |
|---|---|---|---|---|
| 20-30 | 80-100% | 0-15% | 0-5% | Capital humain eleve, horizon long, capacite de recuperation |
| 30-40 | 70-85% | 10-25% | 5-10% | Accumulation, encore long horizon |
| 40-50 | 55-70% | 20-35% | 5-10% | Transition, obligations croissantes |
| 50-60 | 40-55% | 30-45% | 10-15% | Pre-retraite, reduction du risque |
| 60-70 | 30-45% | 40-55% | 10-15% | Retraite, income focus, preservation du capital |
| 70+ | 20-35% | 45-60% | 10-20% | Distribution, liquidite, preservation |

### Glide Path "Through" vs "To"

- **"To" retirement** : l'allocation atteint son point le plus conservateur a la date de retraite. Risque : trop conservateur si la retraite dure 30+ ans.
- **"Through" retirement** : l'allocation continue de s'ajuster apres la retraite, restant relativement agressive les premieres annees pour financer un horizon de distribution long (20-30 ans). Recommande pour la plupart des investisseurs.

### Ajustements modernes / Modern Adjustments

- **Bucket strategy** : diviser le portefeuille en "buckets" temporels (0-5 ans : cash/obligations, 5-15 ans : balanced, 15+ ans : growth). Psychologiquement plus confortable pour les retraites car les depenses immediates sont securisees.
- **Rising equity glide path** : commencer la retraite avec une allocation conservatrice (30% actions) et augmenter progressivement (50-60% actions a 80 ans). La recherche (Kitces, Pfau) montre que cette approche reduit le risque de ruine en retraite car elle evite de cristalliser les pertes au debut de la retraite (sequence of returns risk).
- **Capital humain comme actif** : les salaries d'entreprises stables (fonctionnaires, utilities) ont un capital humain bond-like et peuvent se permettre plus d'actions. Les entrepreneurs/commerciaux ont un capital humain equity-like et doivent diversifier davantage vers les obligations.

---

## Black-Litterman in Practice

### Workflow d'implementation / Implementation Workflow

1. **Calculer les rendements d'equilibre** : utiliser les poids de capitalisation de marche et le CAPM inverse pour deriver les rendements implicites du marche.
2. **Formuler les vues (views)** : exprimer les vues en termes relatifs ou absolus avec un niveau de confiance. Exemple : "Les actions EM surperformeront les actions DM de 2% avec une confiance de 60%."
3. **Combiner equilibre et vues** : appliquer la formule Black-Litterman pour obtenir les rendements combines.
4. **Optimiser** : utiliser les rendements combines comme inputs pour l'optimisation mean-variance.
5. **Verifier la coherence** : les poids resultants doivent etre proches de l'allocation de marche quand les vues sont faibles/incertaines.

### Formule simplifiee / Simplified Formula

```
E(R_combined) = [(tau * Sigma)^(-1) + P' * Omega^(-1) * P]^(-1) * [(tau * Sigma)^(-1) * Pi + P' * Omega^(-1) * Q]
```

ou :
- Pi : vecteur des rendements d'equilibre implicites
- P : matrice des vues (quels actifs sont concernes)
- Q : vecteur des rendements des vues
- Omega : matrice de confiance des vues (diagonale)
- tau : scalaire reflectant l'incertitude sur l'equilibre (typiquement 0.025 a 0.05)
- Sigma : matrice de covariance

### Avantages pratiques / Practical Advantages

- Produit des allocations intuitives et stables (pas de positions extremes)
- Permet d'integrer des vues qualitatives de maniere quantitative
- Le portefeuille converge vers l'allocation de marche en l'absence de vues (comportement safe par defaut)
- Utilise par les plus grandes maisons de gestion (Goldman Sachs, BlackRock, UBS)
