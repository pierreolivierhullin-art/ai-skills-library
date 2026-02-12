# Greeks & Strategies

Référence approfondie sur les Greeks de premier et second ordre, les stratégies d'options par catégorie, la Wheel Strategy, le rolling et les ajustements.

---

## Table of Contents

1. [First-Order Greeks](#first-order-greeks)
2. [Second-Order Greeks](#second-order-greeks)
3. [Income Strategies](#income-strategies)
4. [Directional Strategies](#directional-strategies)
5. [Volatility Strategies](#volatility-strategies)
6. [Hedging Strategies](#hedging-strategies)
7. [The Wheel Strategy](#the-wheel-strategy)
8. [Rolling & Adjustments](#rolling--adjustments)

---

## First-Order Greeks

Les Greeks mesurent la sensibilité du prix d'une option aux variations des paramètres du marché. Ils sont les instruments de bord essentiels du trader d'options.

### Delta (sensibilité au prix du sous-jacent)

```
Delta = dC/dS (pour un call)  |  Delta = dP/dS (pour un put)

Call delta : 0 à +1.00  |  Put delta : -1.00 à 0
```

**Interprétation multiple** :
1. **Sensibilité directionnelle** : un delta de +0.50 signifie que pour chaque hausse de 1$ du sous-jacent, le prix de l'option augmente d'environ 0.50$.
2. **Probabilité approximative** : un call avec delta 0.30 a environ 30% de probabilité d'expirer ITM (approximation, pas exact mathématiquement).
3. **Hedge ratio** : pour couvrir 100 calls avec delta 0.50, acheter 50 actions du sous-jacent (50 calls x 0.50 delta = 25 contrats x 100 actions x 0.50 = 2500 deltas = 2500 actions).
4. **Equivalent share exposure** : une position de 10 calls avec delta 0.60 est équivalente directionnellement à 600 actions (10 x 100 x 0.60).

**Comportement du delta selon le moneyness** :

| Moneyness | Call Delta | Put Delta | Évolution avec le temps |
|---|---|---|---|
| Deep ITM | ~0.90-1.00 | ~-0.90 à -1.00 | Converge vers 1.00/-1.00 |
| ITM | 0.55-0.85 | -0.55 à -0.85 | Augmente/diminue lentement |
| ATM | ~0.50 | ~-0.50 | Stable (maximum de gamma) |
| OTM | 0.15-0.45 | -0.15 à -0.45 | Diminue/augmente lentement |
| Deep OTM | ~0.00-0.10 | ~-0.00 à -0.10 | Converge vers 0 |

**Delta à expiration** : devient un step function (0 ou 1 pour les calls, 0 ou -1 pour les puts). La transition est brutale au voisinage du strike ATM.

### Gamma (taux de variation du delta)

```
Gamma = d(Delta)/dS = d2C/dS2

Toujours positif pour les options longues (calls et puts)
Toujours négatif pour les options courtes (vendeuses)
```

**Interprétation** : le gamma mesure la convexité de la position. Un gamma positif signifie que le delta évolue en faveur du trader : le delta augmente quand le sous-jacent monte et diminue quand il baisse. Un gamma négatif (position courte) signifie le contraire -- c'est le risque principal des vendeurs d'options.

**Propriétés clés** :
- **Maximum ATM** : le gamma est le plus élevé pour les options ATM.
- **Accélération à l'expiration** : le gamma des options ATM augmente dramatiquement dans les derniers jours avant expiration, créant le "gamma risk" des vendeurs.
- **Inversement proportionnel au DTE** : gamma(ATM) est approximativement proportionnel à 1/sqrt(T).

```
Gamma risk scenario :
  Short ATM put à 1 DTE, gamma = 0.15
  Le sous-jacent baisse de 5$ : delta passe de -0.50 à -0.50 - (0.15 * 5) = -1.25
  La perte accélère : c'est le "gamma squeeze" des vendeurs.
```

**Règle de gestion** : ne jamais maintenir de positions short-gamma ATM dans les 7 derniers jours avant expiration. Clôturer ou roller avant que le gamma n'explose.

### Theta (érosion temporelle)

```
Theta = dC/dt (pour un call)  |  Theta = dP/dt (pour un put)

Typiquement exprimé en dollars par jour
Négatif pour les positions longues (time decay)
Positif pour les positions courtes (time income)
```

**Interprétation** : le theta représente le montant de valeur temporelle que l'option perd chaque jour, toutes choses égales par ailleurs. Pour un vendeur d'options, le theta est un revenu quotidien ; pour un acheteur, c'est un coût quotidien.

**Propriétés clés** :
- **Maximum ATM** : les options ATM ont le theta le plus élevé en valeur absolue.
- **Non-linéaire** : le theta s'accélère dans les 30-45 derniers jours, avec une accélération dramatique dans les 7-14 derniers jours.
- **Proportionnel à l'IV** : une IV plus élevée implique plus de valeur temporelle à perdre, donc un theta plus élevé.

```
Approximation du theta decay pour une option ATM :

Theta ≈ -(S * sigma * N'(d1)) / (2 * sqrt(T))  - r * K * e^(-rT) * N(d2)

Où N'(d1) est la densité de la loi normale (bell curve)

Règle du pouce : une option ATM à 30 DTE perd environ
  1/30ème de sa valeur chaque jour,
  mais à 7 DTE, elle perd environ 1/7ème par jour.
```

**Sweet spot du theta selling** : ouvrir les positions vendeuses de premium à 30-45 DTE pour capturer la zone d'accélération du theta tout en conservant suffisamment de temps pour les ajustements si nécessaire.

### Vega (sensibilité à la volatilité implicite)

```
Vega = dC/d(sigma) = dP/d(sigma)

Exprimé en dollars pour un changement de 1% (1 point) de l'IV
Toujours positif pour les options longues
Toujours négatif pour les options courtes
```

**Interprétation** : le vega mesure combien le prix de l'option change pour chaque point de variation de la volatilité implicite. Un vega de 0.15 signifie que si l'IV augmente de 1%, le prix de l'option augmente de 0.15$.

**Propriétés clés** :
- **Maximum ATM** : comme gamma et theta, le vega est maximum pour les options ATM.
- **Proportionnel au temps** : contrairement au gamma, le vega AUGMENTE avec le temps restant. Les LEAPS ont un vega beaucoup plus élevé que les options à court terme.
- **Relationship vega-theta** : les positions longues vega sont courtes theta (et vice versa). C'est le trade-off fondamental du trading de volatilité.

```
Vega approx = S * sqrt(T) * N'(d1)

Exemple : AAPL at 180$, call ATM à 45 DTE, IV = 30%, vega = 0.25
  Si l'IV passe de 30% à 32% (+2 points) :
    Gain = 2 * 0.25 = 0.50$ par action = 50$ par contrat

  Si l'IV passe de 30% à 25% (-5 points, ex: IV crush post-earnings) :
    Perte = 5 * 0.25 = 1.25$ par action = 125$ par contrat
```

### Rho (sensibilité aux taux d'intérêt)

```
Rho = dC/dr  (call rho positif)  |  Rho = dP/dr  (put rho négatif)

Exprimé en dollars pour un changement de 1% du taux sans risque
```

**Interprétation** : le rho est généralement le Greek le moins significatif pour les options à court terme. Cependant, il devient important :
- Pour les **LEAPS** (options à long terme, > 6 mois) : un changement de 100 bps du taux sans risque peut modifier le prix d'un LEAPS de 2-5%.
- En environnement de **taux élevés** : le rho est plus significatif pour tous les horizons.
- Pour les **options sur futures** : le rho interagit avec le coût de portage (cost of carry).

---

## Second-Order Greeks

Les Greeks de second ordre mesurent la sensibilité des Greeks de premier ordre aux variations des paramètres. Essentiels pour le risk management avancé et le delta-hedging dynamique.

### Charm (Delta Decay / DdeltaDtime)

```
Charm = d(Delta)/dt = d(Theta)/dS

Mesure la vitesse à laquelle le delta change avec le passage du temps
```

**Interprétation** : le charm quantifie combien le delta d'une position change chaque jour. C'est critique pour le delta-hedging dynamique :
- **OTM options** : le delta diminue avec le temps (l'option devient de moins en moins sensible au mouvement du sous-jacent). Charm négatif pour les calls OTM.
- **ITM options** : le delta augmente avec le temps (converge vers 1.00 ou -1.00). Charm positif pour les calls ITM.
- **Impact pratique** : un hedger qui re-balance son delta quotidiennement doit anticiper le charm pour éviter d'être systématiquement en retard.

### Vanna (Cross-Greek : Delta-Vol / DdeltaDvol)

```
Vanna = d(Delta)/d(sigma) = d(Vega)/dS

Mesure la sensibilité du delta à la volatilité (et vice versa)
```

**Interprétation** : le vanna explique pourquoi les market makers ajustent leurs hedges quand la volatilité change :
- Quand l'IV augmente, le delta des options OTM augmente (elles deviennent plus "sensibles" au mouvement du sous-jacent).
- Le vanna est positif pour les calls OTM et les puts ITM, négatif pour les calls ITM et les puts OTM.
- **Vanna flow** : les ajustements de hedging des dealers liés au vanna peuvent amplifier les mouvements de marché. Quand la volatilité baisse, les dealers qui hedgent des positions short-vanna doivent acheter le sous-jacent, créant un "vanna rally".

### Volga (Vomma / DvegaDvol)

```
Volga = d(Vega)/d(sigma) = d2C/d(sigma)2

Mesure la convexité du prix par rapport à la volatilité
```

**Interprétation** : le volga mesure combien le vega change quand la volatilité change :
- **Positif pour les options OTM et ITM** : le vega augmente quand la volatilité augmente (convexité positive en volatilité).
- **Proche de zéro ATM** : les options ATM ont un vega relativement stable par rapport aux changements de vol.
- **Pricing du skew** : le volga est un facteur clé dans le pricing de la volatility smile. Les options avec un volga élevé (wings) commandent une prime supplémentaire car elles bénéficient des mouvements de volatilité.

### Tableau récapitulatif des Greeks

| Greek | Formule | Signe Long Call | Signe Long Put | Ce que ça mesure |
|---|---|---|---|---|
| Delta | dC/dS | + (0 à 1) | - (-1 à 0) | Direction |
| Gamma | d2C/dS2 | + | + | Convexité / Accélération |
| Theta | dC/dt | - | - | Érosion temporelle |
| Vega | dC/dsigma | + | + | Sensibilité à l'IV |
| Rho | dC/dr | + | - | Sensibilité aux taux |
| Charm | dDelta/dt | Variable | Variable | Delta decay |
| Vanna | dDelta/dsigma | Variable | Variable | Cross delta-vol |
| Volga | dVega/dsigma | Variable | Variable | Convexité de vol |

---

## Income Strategies

Stratégies conçues pour générer un revenu régulier à partir de la vente de premium (time decay). Idéales quand l'IV Rank est élevé (> 50%).

### Covered Call (Call couvert)

**Construction** : long 100 actions + short 1 call OTM.

```
Position = +100 shares @ S + short 1 call @ strike K (K > S)

Max profit  = (K - S + premium reçu) x 100
Max loss    = (S - premium reçu) x 100 (si le sous-jacent tombe à 0)
Breakeven   = S - premium reçu (coût de base réduit)
```

**Sélection du strike** :
- **Delta 0.30 (70% POP)** : rendement modéré, bonne protection à la baisse, conserve le potentiel haussier.
- **Delta 0.40-0.50** : premium plus élevé, mais cap plus bas sur le profit des actions.
- **Au-dessus d'une résistance technique** : aligner le strike avec un niveau technique où une correction est probable.

**Gestion** :
- Clôturer à 50-75% du profit maximum.
- Si le sous-jacent approche le short strike, évaluer : laisser assigner (si le prix est acceptable) ou roll up and out.
- Ne jamais rouler à perte nette (le crédit du roll doit toujours être positif).

### Cash-Secured Put

**Construction** : short 1 put OTM + cash réservé pour l'achat potentiel de 100 actions.

```
Cash requis = strike x 100
Max profit  = premium reçu
Max loss    = (strike - premium reçu) x 100
Breakeven   = strike - premium reçu
```

**Sélection du strike** :
- Choisir un strike correspondant à un prix d'achat acceptable pour le sous-jacent (support technique, valorisation GARP attractive).
- Delta 0.25-0.35 typiquement.
- Le premium reçu abaisse le coût de base effectif en cas d'assignation.

### Iron Condor

**Construction** : bull put spread + bear call spread sur le même sous-jacent et la même expiration.

```
Jambes : long put (K1) + short put (K2) + short call (K3) + long call (K4)
Où K1 < K2 < prix actuel < K3 < K4

Max profit  = Net credit reçu
Max loss    = max(K2-K1, K4-K3) - Net credit (largeur du spread le plus large - crédit)
Breakeven inf = K2 - Net credit
Breakeven sup = K3 + Net credit
POP         ≈ 1 - (Net credit / largeur du spread)
```

**Paramétrage optimal** :
- Short strikes à delta 0.16-0.30 (70-84% POP par jambe).
- Largeur des wings (K2-K1 et K4-K3) : 1$ à 5$ selon le prix du sous-jacent et le risque souhaité.
- Expiration 30-45 DTE.
- IV Rank > 50% (condition indispensable).

**Gestion** :
- Clôturer à 50% du profit maximum (règle fondamentale des stratégies premium-selling).
- Si le sous-jacent approche un short strike, envisager de clôturer la jambe gagnante et de rouler la jambe menacée.
- Max loss rule : clôturer si la perte atteint 2x le crédit reçu.

### Iron Butterfly

**Construction** : identique à l'iron condor mais avec les short strikes au même niveau (ATM).

```
Jambes : long put (K1) + short put (K2=ATM) + short call (K3=ATM) + long call (K4)
Où K1 < K2 = K3 < K4

Max profit  = Net credit reçu (plus élevé que l'iron condor car short strikes ATM)
Max loss    = largeur du spread - Net credit
Breakeven inf = K2 - Net credit
Breakeven sup = K3 + Net credit
```

**Usage** : version plus agressive de l'iron condor, avec un credit plus élevé mais une zone de profit plus étroite. Préférer quand on anticipe une faible amplitude de mouvement et une IV élevée.

---

## Directional Strategies

### Vertical Spreads (Bull Call / Bear Put)

**Bull Call Spread** (debit spread haussier) :

```
Long 1 call @ K1 (ATM ou légèrement ITM) + Short 1 call @ K2 (OTM)
K1 < K2

Max profit = (K2 - K1 - net debit) x 100
Max loss   = net debit x 100
Breakeven  = K1 + net debit
```

**Bear Put Spread** (debit spread baissier) :

```
Long 1 put @ K1 (ATM ou légèrement ITM) + Short 1 put @ K2 (OTM)
K1 > K2

Max profit = (K1 - K2 - net debit) x 100
Max loss   = net debit x 100
Breakeven  = K1 - net debit
```

**Sélection** :
- En environnement d'IV basse (IV Rank < 30%), préférer les debit spreads aux credit spreads (acheter du premium bon marché).
- Largeur du spread : déterminer en fonction du ratio risque/rendement souhaité (spread étroit = risque faible mais profit limité).

### LEAPS (Long-Term Equity Anticipation Securities)

Options à long terme (expiration > 1 an, typiquement 12-24 mois). Utilisées comme substitut d'action avec levier contrôlé.

**LEAPS Call comme substitut d'action** :
- Acheter un call deep ITM (delta 0.80+) à 12-24 mois d'expiration.
- Coût = fraction du prix de l'action (typiquement 60-75%).
- Levier implicite de 1.3x-1.7x.
- Le theta decay est très lent pour les LEAPS (la courbe de decay est plate loin de l'expiration).
- Le vega est élevé : sensibilité importante aux changements de l'IV.

**Poor Man's Covered Call (PMCC)** :
- Long 1 LEAPS call (deep ITM, delta 0.75+) + short 1 call OTM à court terme (30-45 DTE).
- Simule un covered call avec moins de capital engagé.
- Le premium du short call réduit le coût de base du LEAPS.

---

## Volatility Strategies

### Long Straddle

```
Long 1 call ATM + Long 1 put ATM (même strike, même expiration)

Max profit = illimité (dans les deux directions)
Max loss   = total premium payé (call premium + put premium)
Breakeven sup = strike + total premium
Breakeven inf = strike - total premium
```

**Quand utiliser** :
- Anticipation d'un mouvement important du sous-jacent, direction incertaine.
- IV Rank bas (< 30%) : le premium acheté est relativement bon marché.
- Avant un événement binaire (earnings, FDA, procès) MAIS seulement si l'IV n'a pas déjà intégré l'événement.

**Règle de breakeven** : le sous-jacent doit bouger d'au moins le total du premium payé dans une direction pour atteindre le breakeven. Typiquement, l'expected move implicite est supérieur au breakeven, ce qui rend le straddle structurellement perdant en moyenne (le vendeur de straddle est payé pour le risque).

### Long Strangle

```
Long 1 call OTM (K2) + Long 1 put OTM (K1) (K1 < K2, même expiration)

Max profit = illimité
Max loss   = total premium payé
Breakeven sup = K2 + total premium
Breakeven inf = K1 - total premium
```

Moins cher que le straddle mais nécessite un mouvement plus important pour être profitable. Plus adapté aux situations où un événement extrême est anticipé.

### Long Butterfly

```
Long 1 call @ K1 + Short 2 calls @ K2 + Long 1 call @ K3
Où K1 < K2 < K3 et K2 - K1 = K3 - K2 (strikes équidistants)

Max profit = (K2 - K1 - net debit) x 100  (atteint si S = K2 à expiration)
Max loss   = net debit x 100
```

**Usage** : pari sur un mouvement limité autour d'un strike cible. Coût faible, profit potentiel élevé si le sous-jacent expire précisément au strike central. Utilisée comme alternative à faible coût pour parier sur une plage de prix étroite.

### Calendar Spread (Time Spread)

```
Short 1 call/put @ K (expiration courte T1) + Long 1 call/put @ K (expiration longue T2)
Même strike, expirations différentes (T1 < T2)

Max profit = atteint si S = K à expiration de la jambe courte
Max loss   = net debit payé (limité)
```

**Mécanique** : profite de la différence de theta decay entre les deux expirations. La jambe courte décaye plus vite que la jambe longue, augmentant la valeur nette de la position.

**Vega exposure** : la position est longue vega (bénéficie d'une hausse de l'IV). Si l'IV augmente, la jambe longue (plus sensible au vega) gagne plus que la jambe courte.

**Usage optimal** :
- Environnement d'IV basse (la position bénéficie d'une hausse de l'IV).
- Backwardation de la term structure (IV courte > IV longue) : acheter l'expiration longue à IV basse, vendre l'expiration courte à IV haute.

### Diagonal Spread

```
Short 1 call/put @ K1 (expiration courte T1) + Long 1 call/put @ K2 (expiration longue T2)
Strikes différents ET expirations différentes

Combinaison d'un calendar spread et d'un vertical spread
```

**Usage** : plus flexible que le calendar pur. Permet d'exprimer une vue directionnelle ET temporelle. Le PMCC (Poor Man's Covered Call) est un type de diagonal spread.

---

## Hedging Strategies

### Protective Put (Married Put)

```
Long 100 shares + Long 1 put OTM

Max profit = illimité (à la hausse)
Max loss   = (S - strike + premium) x 100
Breakeven  = S + premium
```

**Coût vs protection** :
- Put delta -0.20 (80% OTM) : protection "catastrophe", premium faible.
- Put delta -0.30 (70% OTM) : protection modérée, premium modéré.
- Put delta -0.50 (ATM) : protection complète, premium élevé (réduit significativement le rendement).

### Collar (Collier)

```
Long 100 shares + Long 1 put OTM + Short 1 call OTM

Coût net = put premium - call premium (souvent proche de zéro = "zero-cost collar")
Max profit = (call strike - S + net credit/debit) x 100
Max loss   = (S - put strike + net credit/debit) x 100
```

**Usage** : protection gratuite (ou quasi-gratuite) en échange d'un plafonnement du gain. Idéale pour protéger un gain latent important sans déclencher un événement fiscal.

### Put Spread Collar

```
Long 100 shares + Long 1 put OTM @ K1 + Short 1 put far OTM @ K2 + Short 1 call OTM @ K3
(K2 < K1 < S < K3)
```

Version améliorée du collar : le short put (K2) finance partiellement le long put (K1), réduisant le coût. La protection n'est pas complète en cas de crash extrême (en dessous de K2), mais le coût est significativement réduit.

---

## The Wheel Strategy

### Principe Fondamental

La Wheel Strategy est un cycle systématique de vente de premium conçu pour générer un revenu régulier sur des sous-jacents de qualité, avec l'acceptation de détenir les actions si assigné.

### Cycle Complet

```
Phase 1 : Cash-Secured Put
  └─> Option expire OTM → Collecter premium → Recommencer Phase 1
  └─> Option assignée → Acheter 100 actions au strike → Phase 2

Phase 2 : Covered Call
  └─> Option expire OTM → Collecter premium → Recommencer Phase 2
  └─> Option assignée → Vendre 100 actions au strike → Phase 1

Yield annualisé = somme des premiums collectés / capital déployé x (365/jours)
```

### Critères de Sélection du Sous-Jacent

Appliquer impérativement un filtre de qualité (voir GARP Analysis) :
- Actions que l'on accepte de détenir à long terme (fondamentaux solides).
- Prix d'action entre 20$ et 200$ (taille de lot de 100 actions gérable).
- Liquidité élevée sur les options (bid-ask spread étroit).
- Pas de earnings imminent ou d'événement binaire dans les 30 jours.
- IV Rank > 30% (premium suffisant pour justifier la vente).
- Secteur diversifié par rapport aux autres positions Wheel.

### Gestion des Scénarios Adverses

**Le sous-jacent chute significativement après assignation** :
- Ne PAS paniquer et vendre les actions à perte.
- Évaluer si la thèse fondamentale reste intacte.
- Vendre des covered calls au-dessus du coût de base ajusté (prix d'assignation - premium total collecté).
- Si nécessaire, patience : continuer à vendre des calls OTM pour réduire le coût de base progressivement.
- Si les fondamentaux se sont dégradés : couper la perte et recommencer sur un autre sous-jacent.

**Le sous-jacent monte fortement et les covered calls sont assignés prématurément** :
- Accepter l'assignation : le profit est plafonné mais réel (gain sur actions + premium).
- Recommencer le cycle avec un cash-secured put, potentiellement sur le même sous-jacent si la valorisation reste acceptable.

---

## Rolling & Adjustments

### Rolling : Principes Généraux

Le rolling consiste à clôturer une position existante et à en ouvrir une nouvelle simultanément, ajustant le strike, l'expiration, ou les deux.

**Types de roll** :

| Type | Action | Quand |
|---|---|---|
| Roll out | Même strike, expiration ultérieure | Le sous-jacent n'a pas atteint le short strike mais plus de temps est nécessaire |
| Roll up (call) | Strike supérieur, même ou nouvelle expiration | Le sous-jacent a monté au-delà du short call strike |
| Roll down (put) | Strike inférieur, même ou nouvelle expiration | Le sous-jacent a baissé au-delà du short put strike |
| Roll up and out | Strike supérieur + expiration ultérieure | Ajustement agressif à la hausse |
| Roll down and out | Strike inférieur + expiration ultérieure | Ajustement agressif à la baisse |

### Règle du Crédit Net

**Ne jamais rouler pour un débit net** (sauf exception stratégique documentée). Le roll doit toujours collecter un crédit supplémentaire, ce qui :
- Abaisse le breakeven.
- Augmente le profit potentiel total.
- Compense le risque additionnel du temps supplémentaire.

```
Exemple : Iron Condor sur SPY
  Position initiale : Bear call 580/585 pour 1.20$ de crédit
  SPY monte à 578, le short call 580 est menacé.

  Roll :
  - Buy to close : bear call 580/585 @ 3.00$ (perte de 1.80$ sur cette jambe)
  - Sell to open : bear call 585/590 à 45 DTE @ 2.50$ (nouveau crédit)
  - Net du roll : -3.00 + 2.50 = -0.50$ de débit -> NON ACCEPTABLE

  Alternative : roll up AND out
  - Buy to close : bear call 580/585 @ 3.00$
  - Sell to open : bear call 590/595 à 60 DTE @ 1.30$ -> encore un débit

  Décision : si aucun roll n'est possible pour un crédit net, CLÔTURER la position.
```

### Adjustment Decision Framework

```
1. Le sous-jacent approche le short strike ?
   ├─ Oui : Évaluer le roll (crédit net possible ?)
   │   ├─ Crédit net possible → Roll
   │   └─ Crédit net impossible → Clôturer
   └─ Non : Maintenir la position

2. Le profit atteint 50-75% du max ?
   └─ Oui → Clôturer et réinitialiser

3. La perte atteint 2x le crédit reçu ?
   └─ Oui → Clôturer (couper les pertes)

4. Les fondamentaux du sous-jacent se sont dégradés ?
   └─ Oui → Clôturer immédiatement

5. Un earnings/événement approche dans les 7 jours ?
   └─ Oui → Clôturer ou rouler post-événement
```

### Repair Strategy pour les Actions en Perte

Quand on détient des actions en perte significative (typiquement après assignation d'un put) :

```
Repair Strategy :
  Long 100 actions @ coût de base C (actuellement à S, S < C)
  + Long 1 call @ K1 (ATM, strike ≈ S)
  + Short 2 calls @ K2 (OTM, strike = (C + S) / 2 approximativement)

  Résultat : crée un bull call spread gratuit (ou presque) financé par le short call supplémentaire.
  Le breakeven descend de C à K2.
  Le max profit est capé à K2 mais le recovery est accéléré.
```

---

## Summary Checklist

### Pour chaque trade d'options :

- [ ] Les Greeks de position sont calculés et compris (delta, gamma, theta, vega)
- [ ] Le profil risque/rendement est quantifié (max profit, max loss, breakeven, POP)
- [ ] La stratégie est alignée avec l'IV environment (IV Rank, vente vs achat de premium)
- [ ] Les règles de management sont définies AVANT l'entrée (target profit, max loss, adjustment triggers)
- [ ] Le sizing respecte les limites (< 5% du capital en risque par trade)
- [ ] L'expiration est adaptée à la stratégie (30-45 DTE income, 60-90 DTE directional, >180 DTE LEAPS)
- [ ] Aucun earnings/événement n'est dans la fenêtre de risque
- [ ] La liquidité est vérifiée (bid-ask spread, volume, OI)

### Pour la gestion du portefeuille d'options :

- [ ] Les Greeks agrégés sont surveillés quotidiennement (delta net, gamma net, theta net, vega net)
- [ ] Les corrélations entre positions sont évaluées
- [ ] Les expirations sont diversifiées (pas de concentration sur une seule date)
- [ ] Le capital utilisé (buying power reduction) est < 50% du capital total
- [ ] Le journal de trading est tenu à jour
