# Options Fundamentals

Référence approfondie sur la mécanique des options, les modèles de pricing, la volatilité implicite et l'analyse de la chaîne d'options.

---

## Table of Contents

1. [Call/Put Mechanics](#callput-mechanics)
2. [Intrinsic Value & Time Value](#intrinsic-value--time-value)
3. [Payoff Diagrams](#payoff-diagrams)
4. [Options Pricing Models](#options-pricing-models)
5. [Implied Volatility](#implied-volatility)
6. [IV Rank & IV Percentile](#iv-rank--iv-percentile)
7. [Volatility Smile & Skew](#volatility-smile--skew)
8. [Options Chain Analysis](#options-chain-analysis)
9. [Open Interest & Volume](#open-interest--volume)

---

## Call/Put Mechanics

### Call Option (Option d'achat)

Un contrat call confère à l'acheteur le **droit, sans obligation**, d'acheter 100 actions du sous-jacent au prix d'exercice (strike price) jusqu'à la date d'expiration (option américaine) ou à la date d'expiration uniquement (option européenne).

**Acheteur du call (long call)** :
- Paie le premium (prix de l'option) au vendeur.
- Profit potentiel illimité si le sous-jacent monte au-dessus du strike + premium payé.
- Perte maximale limitée au premium payé.
- Breakeven = strike + premium payé.

**Vendeur du call (short call / call writer)** :
- Reçoit le premium immédiatement.
- Obligation de vendre 100 actions au strike si l'acheteur exerce.
- Profit maximum = premium reçu.
- Perte potentielle illimitée (si le sous-jacent monte indéfiniment). Ce risque est couvert si le vendeur détient déjà les actions (covered call).

### Put Option (Option de vente)

Un contrat put confère à l'acheteur le **droit, sans obligation**, de vendre 100 actions du sous-jacent au prix d'exercice jusqu'à ou à la date d'expiration.

**Acheteur du put (long put)** :
- Paie le premium au vendeur.
- Profit maximum = (strike - premium) x 100 (si le sous-jacent tombe à zéro).
- Perte maximale = premium payé.
- Breakeven = strike - premium payé.

**Vendeur du put (short put / put writer)** :
- Reçoit le premium immédiatement.
- Obligation d'acheter 100 actions au strike si l'acheteur exerce.
- Profit maximum = premium reçu.
- Perte maximale = (strike - premium) x 100 (si le sous-jacent tombe à zéro). Ce risque est atténué si le vendeur maintient le cash nécessaire en compte (cash-secured put).

### Options américaines vs européennes

| Caractéristique | Américaine | Européenne |
|---|---|---|
| Exercice | À tout moment avant expiration | Uniquement à expiration |
| Marché principal | Actions individuelles US | Indices (SPX, NDX), options sur futures |
| Prime d'exercice anticipé | Oui (intégrée dans le prix) | Non |
| Settlement | Physical delivery (livraison d'actions) | Souvent cash-settled |

**Exercice anticipé** : surveiller les situations d'exercice anticipé optimal :
- **Short call ITM** : risque d'exercice juste avant l'ex-dividend si la valeur temporelle restante < dividende attendu.
- **Deep ITM put** : exercice possible quand la valeur temporelle est quasi nulle et le taux d'intérêt fait préférer le cash immédiat.

---

## Intrinsic Value & Time Value

Toute prime d'option se décompose en deux composantes :

```
Premium = Intrinsic Value + Time Value (Extrinsic Value)
```

### Intrinsic Value (Valeur intrinsèque)

La valeur intrinsèque est le profit immédiat si l'option était exercée à l'instant T :
- **Call** : max(0, Prix du sous-jacent - Strike)
- **Put** : max(0, Strike - Prix du sous-jacent)

Une option avec une valeur intrinsèque > 0 est dite **In-The-Money (ITM)**.
Une option avec une valeur intrinsèque = 0 est dite **Out-of-The-Money (OTM)** ou **At-The-Money (ATM)** si strike = prix du sous-jacent.

### Time Value (Valeur temporelle / Valeur extrinsèque)

La valeur temporelle représente la prime que le marché accorde pour la possibilité que l'option devienne (plus) profitable avant expiration. Elle intègre :
- **Le temps restant** : plus l'expiration est lointaine, plus la valeur temporelle est élevée.
- **La volatilité implicite** : plus l'IV est élevée, plus la valeur temporelle est élevée.
- **La proximité du strike par rapport au prix** : la valeur temporelle est maximale ATM et diminue pour les options deep ITM ou deep OTM.

| Moneyness | Valeur intrinsèque | Valeur temporelle | Delta approximatif (call) |
|---|---|---|---|
| Deep ITM | Élevée | Faible | 0.80 - 1.00 |
| ITM | Présente | Modérée | 0.55 - 0.80 |
| ATM | Nulle ou minime | Maximale | ~0.50 |
| OTM | Nulle | Modérée | 0.20 - 0.45 |
| Deep OTM | Nulle | Faible | 0.00 - 0.20 |

**Règle fondamentale** : à l'expiration, la valeur temporelle est toujours zéro. Le prix de l'option = valeur intrinsèque uniquement. C'est le fondement du theta decay.

---

## Payoff Diagrams

Les diagrammes de payoff (profit/loss à expiration) sont l'outil fondamental pour visualiser le profil risque/rendement d'une position.

### Long Call
```
P&L
 ^
 |                          /
 |                        /
 |                      /
 |--------------------/----------> Prix du sous-jacent
 |   -Premium       Strike+P
 |                  (Breakeven)
```
- Max profit : illimité (S -> infini)
- Max loss : premium payé
- Breakeven : Strike + Premium

### Long Put
```
P&L
 ^
 |  \
 |    \
 |      \
 |--------\----------------------> Prix du sous-jacent
 |   Strike-P    -Premium
 |  (Breakeven)
```
- Max profit : (Strike - Premium) x 100
- Max loss : premium payé
- Breakeven : Strike - Premium

### Short Call (Covered ou Naked)
```
P&L
 ^
 |   +Premium
 |--------------------\
 |                     \----------> Prix du sous-jacent
 |                  Strike+P
 |                 (Breakeven)
```

### Short Put (Cash-Secured)
```
P&L
 ^
 |                    +Premium
 |--------/----------------------> Prix du sous-jacent
 |      /  Strike-P
 |    /   (Breakeven)
 |  /
```

### Bull Call Spread (Debit)
```
P&L
 ^                _______________
 | Max profit    |
 |              /
 |-------------/-----|----------> Prix du sous-jacent
 | -Net Debit  K1    K2
 |______________|
```
- Max profit : (K2 - K1 - Net Debit) x 100
- Max loss : Net Debit x 100
- Breakeven : K1 + Net Debit

### Iron Condor (Credit)
```
P&L
 ^
 |         +Net Credit
 |    ____/____________\____
 |   /  K1  K2      K3  K4  \
 |--/---|------|------|----\---> Prix du sous-jacent
 | /                        \
 |/ -Max Loss          -Max Loss
```
- Max profit : Net Credit reçu
- Max loss : largeur du spread le plus large - Net Credit
- Breakeven inférieur : K2 - Net Credit
- Breakeven supérieur : K3 + Net Credit

---

## Options Pricing Models

### Black-Scholes-Merton (BSM)

Le modèle fondateur de l'évaluation des options européennes, publié par Fischer Black, Myron Scholes et Robert Merton en 1973.

**Formule pour un call européen** :

```
C = S * N(d1) - K * e^(-rT) * N(d2)

Où :
  d1 = [ln(S/K) + (r + sigma^2 / 2) * T] / (sigma * sqrt(T))
  d2 = d1 - sigma * sqrt(T)

  S     = prix actuel du sous-jacent
  K     = prix d'exercice (strike)
  r     = taux sans risque annualisé
  T     = temps jusqu'à expiration (en années)
  sigma = volatilité annualisée du sous-jacent
  N(x)  = fonction de répartition de la loi normale standard
  e     = base du logarithme naturel (2.71828...)
```

**Formule pour un put européen** (via put-call parity) :

```
P = K * e^(-rT) * N(-d2) - S * N(-d1)

Put-Call Parity : C - P = S - K * e^(-rT)
```

**Hypothèses du modèle BSM** :
1. Le prix du sous-jacent suit un mouvement brownien géométrique (GBM) avec volatilité constante.
2. Pas de dividendes pendant la durée de vie de l'option (extension : modèle de Merton avec dividende continu q).
3. Marché efficient sans frais de transaction ni taxes.
4. Taux sans risque constant.
5. Distribution log-normale des rendements (pas de sauts, pas de queues épaisses).
6. Trading continu possible.

**Limitations pratiques** :
- La volatilité n'est PAS constante (smile/skew).
- Les rendements ont des queues épaisses (fat tails) -- sous-estimation des événements extrêmes.
- Le modèle suppose un hedging continu, impossible en pratique (hedging discret = gamma risk).
- Ne gère pas les dividendes discrets ni l'exercice anticipé (options américaines).

**Extension de Merton** pour dividende continu (yield q) :

```
C = S * e^(-qT) * N(d1) - K * e^(-rT) * N(d2)

d1 = [ln(S/K) + (r - q + sigma^2 / 2) * T] / (sigma * sqrt(T))
```

### Modèle Binomial (Cox-Ross-Rubinstein, 1979)

Le modèle binomial construit un arbre de prix discret où, à chaque pas de temps, le sous-jacent monte d'un facteur u ou descend d'un facteur d.

**Paramètres de l'arbre CRR** :

```
u = e^(sigma * sqrt(dt))     (facteur de hausse)
d = 1/u = e^(-sigma * sqrt(dt))  (facteur de baisse)
p = (e^(r * dt) - d) / (u - d)   (probabilité risque-neutre de hausse)
dt = T / N                        (pas de temps, N = nombre de périodes)
```

**Algorithme** :
1. Construire l'arbre des prix du sous-jacent forward (de t=0 à t=T).
2. À chaque noeud terminal (t=T), calculer le payoff : max(S-K, 0) pour un call, max(K-S, 0) pour un put.
3. Backward induction : à chaque noeud, le prix de l'option = max(valeur d'exercice immédiat, valeur de continuation actualisée).
4. Valeur de continuation = e^(-r*dt) * [p * C_up + (1-p) * C_down].

**Avantages** :
- Gère les options américaines (exercice anticipé à chaque noeud).
- Intègre les dividendes discrets (ajustement du prix du sous-jacent au noeud ex-dividend).
- Converge vers Black-Scholes quand N -> infini.
- Intuitif et pédagogique.

**Inconvénients** :
- Computationally plus lourd que BSM pour les options vanilles européennes.
- Nécessite N > 100 pas pour une précision acceptable.
- Difficulté d'extension aux multi-sous-jacents.

### Simulation Monte Carlo

La méthode Monte Carlo estime le prix d'une option en simulant un grand nombre de trajectoires possibles du sous-jacent et en moyennant les payoffs actualisés.

**Processus GBM (Geometric Brownian Motion)** :

```
S(t+dt) = S(t) * exp[(r - q - sigma^2/2) * dt + sigma * sqrt(dt) * Z]

Où Z ~ N(0,1) est un tirage aléatoire standard
```

**Algorithme** :
1. Générer M trajectoires de prix du sous-jacent (M = 10,000 à 1,000,000).
2. Pour chaque trajectoire, calculer le payoff à expiration (ou path-dependent).
3. Moyenne des payoffs actualisés : C = e^(-rT) * (1/M) * SUM(payoff_i).
4. Estimer l'erreur standard : SE = std(payoffs) / sqrt(M).

**Avantages** :
- Extrêmement flexible : options exotiques, path-dependent (asiatiques, barrières, lookback), multi-sous-jacents (basket options, rainbow options).
- Extension facile à des processus stochastiques complexes (Heston, SABR, jump-diffusion).
- Parallélisable massivement (GPU computing).

**Techniques d'accélération** :
- **Antithetic variates** : pour chaque Z, simuler aussi -Z. Réduit la variance de moitié.
- **Control variates** : utiliser le prix BSM comme variable de contrôle.
- **Importance sampling** : biaiser les trajectoires vers les régions de payoff non nul.
- **Quasi-Monte Carlo** : utiliser des séquences de Sobol ou Halton au lieu de nombres pseudo-aléatoires.

**Inconvénients** :
- Lent pour les options simples (BSM est quasi instantané).
- Difficulté native pour les options américaines (nécessite Longstaff-Schwartz / LSM).
- Convergence en O(1/sqrt(M)) : doubler la précision nécessite 4x plus de simulations.

### Comparaison des Modèles

| Critère | Black-Scholes | Binomial | Monte Carlo |
|---|---|---|---|
| Options européennes | Excellent (forme fermée) | Bon | Bon (mais lent) |
| Options américaines | Non natif | Excellent | Difficile (LSM) |
| Greeks | Forme fermée | Différences finies | Différences finies ou pathwise |
| Dividendes discrets | Extension nécessaire | Natif | Natif |
| Options exotiques | Limité | Limité | Excellent |
| Multi-sous-jacents | Non | Difficile | Excellent |
| Vitesse | Instantané | Rapide (N<500) | Lent (M>10000) |
| Modèles de vol complexes | Non natif | Possible | Excellent |

---

## Implied Volatility

### Définition et Interprétation

La volatilité implicite (IV) est la volatilité que le marché "implique" dans le prix observé d'une option. C'est la valeur de sigma qui, injectée dans le modèle BSM, reproduit le prix de marché de l'option.

```
Prix de marché observé = BSM(S, K, r, T, sigma = IV)

Résolution numérique : trouver IV tel que BSM(IV) = Prix de marché
Méthodes : Newton-Raphson (convergence rapide via vega), bisection, Brent
```

**Interprétation** : l'IV représente l'anticipation consensuelle du marché sur la volatilité future du sous-jacent pendant la durée de vie de l'option. Ce n'est PAS une prévision exacte, mais le prix du risque de volatilité.

### Implied vs Historical (Realized) Volatility

| Métrique | Volatilité implicite (IV) | Volatilité historique (HV) |
|---|---|---|
| Direction temporelle | Forward-looking | Backward-looking |
| Source | Prix des options | Prix historiques du sous-jacent |
| Calcul | Inversion du modèle BSM | Écart-type des rendements log sur N jours |
| Usage | Pricing, évaluation du premium | Benchmark pour comparer l'IV |

**Formule de la volatilité historique** :

```
HV = sqrt(252) * std(ln(S_t / S_{t-1}))  pour des rendements quotidiens

Où 252 = nombre de jours de trading par an (annualisation)
```

**Volatilité réalisée (RV) vs HV** : la RV est calculée sur une fenêtre glissante (typiquement 20 ou 30 jours de trading) et comparée à l'IV au moment de l'ouverture de la position. La différence IV - RV est le "variance risk premium" (VRP), historiquement positif (l'IV surestime la RV en moyenne, ce qui rémunère les vendeurs de volatilité).

**Règle pratique** :
- IV > HV(20) significativement : les options sont "chères" -- favoriser les stratégies vendeuses de premium.
- IV < HV(20) significativement : les options sont "bon marché" -- favoriser les stratégies acheteuses de volatilité.

---

## IV Rank & IV Percentile

### IV Rank

L'IV Rank positionne l'IV actuelle par rapport à son range (min-max) sur une période de référence (généralement 52 semaines / 1 an).

```
IV Rank = (IV actuelle - IV min_52w) / (IV max_52w - IV min_52w) * 100

Exemple :
  IV actuelle = 35%
  IV min 52 semaines = 20%
  IV max 52 semaines = 60%
  IV Rank = (35 - 20) / (60 - 20) * 100 = 37.5%
```

**Interprétation** :
- IV Rank > 50% : la volatilité est dans la moitié haute de son range annuel. Environnement favorable à la vente de premium (iron condors, credit spreads, strangles courts).
- IV Rank < 30% : la volatilité est basse. Environnement favorable aux stratégies acheteuses de volatilité (calendars, long straddles, diagonales).

**Limitation** : l'IV Rank est sensible aux extremes. Un seul spike d'IV (ex : crash) peut comprimer le Rank pendant des mois même si l'IV actuelle est raisonnablement élevée.

### IV Percentile

L'IV Percentile mesure le pourcentage de jours de trading sur la période de référence (252 jours) où l'IV a été INFÉRIEURE à l'IV actuelle.

```
IV Percentile = (Nombre de jours où IV < IV actuelle) / 252 * 100

Exemple :
  Si l'IV actuelle de 35% est supérieure à l'IV de 200 des 252 derniers jours :
  IV Percentile = 200/252 * 100 = 79.4%
```

**Interprétation** : plus robuste que l'IV Rank car non sensible aux extremes. Un IV Percentile de 80% signifie que l'IV actuelle est plus élevée que 80% des observations récentes -- c'est un signal fort pour la vente de premium.

**Règle de trading combinée** :

| IV Rank | IV Percentile | Signal |
|---|---|---|
| > 50% | > 50% | Forte conviction pour vente de premium |
| > 50% | < 50% | Signal mixte (extreme passé distord le Rank) |
| < 30% | < 30% | Forte conviction pour achat de volatilité |
| < 30% | > 30% | Signal mixte (IV basse mais pas historiquement rare) |

---

## Volatility Smile & Skew

### Le Smile de Volatilité

En théorie BSM, l'IV devrait être identique pour tous les strikes d'une même expiration (volatilité constante). En pratique, l'IV varie selon le strike, formant un "smile" ou un "skew".

### Equity Skew (Skew action)

Pour les actions et indices, l'IV est typiquement plus élevée pour les puts OTM (strikes bas) que pour les calls OTM (strikes hauts). Ce pattern est appelé **volatility skew** ou **smirk**.

```
IV
 ^
 |  \
 |    \
 |      \____
 |            \_____
 |                   \___
 |-----|-----|-----|-------> Strike / Moneyness
   Deep OTM   ATM   OTM
   puts              calls
```

**Raisons du skew** :
1. **Demande de protection** : les investisseurs institutionnels achètent massivement des puts OTM pour protéger leurs portefeuilles, poussant les prix (et donc l'IV) de ces puts à la hausse.
2. **Crash fear premium** : après le crash de 1987, le marché intègre une prime pour le risque de chute brutale.
3. **Leverage effect** : quand le marché baisse, la volatilité augmente (ratio dette/equity augmente, incertitude croissante).
4. **Rendements asymétriques** : les distributions de rendement des actions ont un skew négatif (queues gauches plus épaisses).

### Mesure du Skew

**Skew 25-delta** : différence d'IV entre le put 25-delta et le call 25-delta pour une même expiration.

```
Skew = IV(25-delta put) - IV(25-delta call)

Skew positif (typique pour les actions) : puts OTM plus chers que les calls OTM
Skew négatif (rare, possible sur les commodities) : calls OTM plus chers
```

**Risk Reversal (RR)** : indicateur de sentiment basé sur le skew.

```
RR = IV(25-delta call) - IV(25-delta put)

RR négatif (normal pour les actions) : demande de protection élevée
RR se normalisant (skew s'aplatit) : réduction de la peur
```

### Term Structure de la Volatilité

Comparer l'IV entre différentes expirations pour un même strike (ou delta).

**Contango (normal)** : IV court terme < IV long terme. La structure reflète l'incertitude croissante avec le temps.

**Backwardation (inversée)** : IV court terme > IV long terme. Signale un événement imminent (earnings, FDA decision, élection) qui gonfle l'IV de court terme.

```
IV
 ^
 |              ______ Contango (normal)
 |            /
 |          /
 |        /
 |  ____/
 |/______________ Backwardation (événement imminent)
 |                \____
 |-----|-----|---------|-------> Expiration
   1m    3m     6m      12m
```

**Application pratique** :
- **Calendar spread** : acheter l'expiration longue (IV plus basse en backwardation) et vendre l'expiration courte (IV plus haute). Profiter de la normalisation post-événement.
- **Placement des expirations** : en contango normal, les vendeurs de premium préfèrent les expirations 30-45 DTE (sweet spot du theta decay).

---

## Options Chain Analysis

### Lecture de la Chaîne d'Options

La chaîne d'options (option chain) est le tableau de tous les contrats disponibles pour un sous-jacent donné, organisé par expiration et par strike.

**Colonnes clés** :

| Colonne | Description | Usage |
|---|---|---|
| Bid / Ask | Prix d'achat / vente actuels | Liquidité (spread étroit = liquide) |
| Last | Dernier prix tradé | Peut être périmé si volume faible |
| Volume | Nombre de contrats échangés aujourd'hui | Activité du jour |
| Open Interest (OI) | Nombre de contrats ouverts (non clôturés) | Positions existantes |
| IV | Volatilité implicite du strike | Coût relatif de l'option |
| Delta | Sensibilité au mouvement du sous-jacent | Probabilité approximative d'expirer ITM |
| Bid-Ask Spread | Différence entre bid et ask | Coût de transaction implicite |

### Critères de Liquidité

Toujours vérifier la liquidité avant d'entrer une position :
- **Bid-ask spread** < 10% du mid-price pour les options ATM.
- **Volume quotidien** > 100 contrats pour le strike visé.
- **Open Interest** > 500 contrats pour le strike visé.
- **Sous-jacent** avec volume d'actions > 1M/jour.
- **Penny-wide spreads** (spreads de 0.01) sur les options les plus liquides (SPY, QQQ, AAPL, etc.).

### Strike Selection par Delta

Utiliser le delta comme guide pour le placement des strikes :

| Delta | Moneyness | Probabilité OTM (approx.) | Usage typique |
|---|---|---|---|
| 0.80-0.90 | Deep ITM | 10-20% | LEAPS directionnels, substitut d'action |
| 0.50-0.60 | ATM | 40-50% | Maximum de premium, balanced risk |
| 0.30-0.35 | OTM | 65-70% | Short strikes des spreads (sweet spot POP) |
| 0.15-0.20 | Far OTM | 80-85% | Wings des iron condors, high probability |
| 0.05-0.10 | Deep OTM | 90-95% | Tail protection, lottery tickets |

---

## Open Interest & Volume

### Open Interest (OI)

L'Open Interest représente le nombre total de contrats d'options ouverts (non encore clôturés, exercés ou expirés) pour un strike et une expiration donnés. Il est mis à jour quotidiennement après la clôture.

**Interprétation de l'OI** :
- **OI élevé sur un strike** : "mur" potentiel de support/résistance (les market makers qui ont vendu ces options hedgent dynamiquement, créant un effet d'attraction du prix vers ce strike -- concept de "max pain").
- **OI croissant + prix croissant** : nouvelles positions ouvertes dans le sens de la tendance (signal de continuation).
- **OI décroissant + prix croissant** : positions short se clôturent (short covering) -- signal potentiel d'épuisement.

### Max Pain Theory

Le "max pain" est le strike auquel le plus grand nombre de contrats d'options (calls + puts) expireraient sans valeur, causant la perte maximale pour les acheteurs d'options (et le profit maximum pour les vendeurs/market makers).

```
Max Pain = Strike qui minimise la valeur totale des options ITM à expiration

Calcul :
  Pour chaque strike K :
    Pain = SUM(call OI * max(S-K, 0)) + SUM(put OI * max(K-S, 0))
  Max Pain = K qui minimise Pain
```

**Usage** : le sous-jacent a tendance (pas toujours) à graviter vers le max pain à l'approche de l'expiration. Utile comme check supplémentaire, pas comme signal primaire.

### Put/Call Ratio

```
P/C Ratio = Volume puts / Volume calls   (ou OI puts / OI calls)
```

| P/C Ratio | Interprétation | Signal contrarian |
|---|---|---|
| < 0.7 | Excès d'optimisme (beaucoup de calls) | Potentiellement bearish |
| 0.7 - 1.0 | Zone neutre | Pas de signal |
| > 1.0 | Excès de pessimisme (beaucoup de puts) | Potentiellement bullish |
| > 1.5 | Peur extrême | Fort signal contrarian bullish |

**Nuance** : distinguer le hedging institutionnel (achats de puts structurels) de la spéculation directionnelle. Le signal contrarian est plus fiable sur les indices (SPY, QQQ) que sur les actions individuelles.

### Unusual Options Activity (UOA)

Surveiller les anomalies de volume qui peuvent signaler un positionnement institutionnel informé :

**Critères de détection** :
- Volume du jour > 5x le volume moyen sur 20 jours pour un strike donné.
- Transactions uniques de grande taille (block trades > 500 contrats).
- Transactions exécutées au ask (achat agressif) ou au bid (vente agressive).
- Activité concentrée sur des expirations inhabituelles (pas les expirations mensuelles standards).

**Interprétation** :
- Des achats massifs de calls OTM à court terme sur une small/mid-cap avant un événement peuvent signaler une anticipation d'annonce positive.
- Des achats massifs de puts ITM peuvent indiquer un hedging institutionnel anticipant un risque de baisse.
- Toujours croiser avec le contexte fondamental et technique avant de suivre l'UOA.

---

## Summary Checklist

Vérifier ces points avant chaque trade d'options :

- [ ] La liquidité est suffisante (bid-ask spread, volume, OI)
- [ ] L'IV environment est identifié (IV Rank, IV Percentile, comparaison IV vs HV)
- [ ] Le skew est analysé (normal, accentué, inversé)
- [ ] La term structure est vérifiée (contango vs backwardation, événements calendaires)
- [ ] Le max pain et les zones de forte concentration d'OI sont identifiés
- [ ] Le P/C ratio et l'UOA sont consultés pour le sentiment
- [ ] Le modèle de pricing approprié est utilisé (BSM pour européennes, binomial pour américaines avec dividendes)
- [ ] La valeur intrinsèque et la valeur temporelle sont comprises et acceptées
- [ ] Le payoff diagram est tracé mentalement ou numériquement
- [ ] Les hypothèses du modèle et leurs limitations sont comprises
