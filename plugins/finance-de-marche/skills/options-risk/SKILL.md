---
name: options-risk
description: This skill should be used when the user asks about "options trading", "Greeks", "delta", "gamma", "theta", "vega", "implied volatility", "options strategies", "risk management", "position sizing", "GARP screening", "covered call", "iron condor", "straddle", "Black-Scholes", "trading d'options", "grecques", "volatilité implicite", "stratégies d'options", "gestion du risque", "dimensionnement de position", "call couvert", "vente de put", "put spread", "call spread", "butterfly", "calendar spread", "strangle", "collar", "risk/reward", "ratio risque/rendement", "IV rank", "IV percentile", "options chain", "chaîne d'options", "expiration", "échéance", "strike price", "prix d'exercice", "in the money", "ITM", "OTM", "ATM", "open interest", "volume", "bid-ask spread", "assignment", "exercise", or needs guidance on options trading, market risk management, and fundamental analysis.
version: 1.0.0
---

# Options Risk

Expertise complète en trading d'options, Greeks, volatilité, stratégies, analyse fondamentale GARP et gestion du risque de portefeuille.

## Overview

Maîtriser l'ensemble de la chaîne de valeur du trading d'options : de la mécanique fondamentale des contrats Call/Put aux stratégies multi-jambes sophistiquées, en passant par le pricing quantitatif (Black-Scholes, binomial, Monte Carlo), l'analyse de la volatilité implicite, la gestion des Greeks de portefeuille et la méthodologie GARP pour la sélection de sous-jacents de qualité. Cette skill intègre les pratiques institutionnelles modernes (2024-2026) incluant l'analyse de flow, les surfaces de volatilité, le delta-hedging dynamique et les frameworks de risk management quantitatif (VaR, Expected Shortfall, stress testing).

Le trading d'options n'est pas de la spéculation aveugle : c'est de l'ingénierie du risque. Chaque position est un ensemble de paris sur la direction, la volatilité, le temps et les taux -- quantifiés par les Greeks. Comprendre ces dimensions et les gérer activement transforme les options d'un instrument dangereux en un outil précis de construction de profils de rendement asymétriques et de couverture de portefeuille.

## When This Skill Applies

Activer cette skill dans les situations suivantes :

- **Analyse d'une position options** : évaluer le prix théorique, les Greeks, le breakeven, le max profit/loss et le profil risque/rendement d'une position simple ou complexe.
- **Construction de stratégie** : sélectionner et structurer une stratégie d'options (income, directionnelle, volatilité, hedging) adaptée à une thèse de marché, un objectif de rendement et une tolérance au risque.
- **Analyse de volatilité** : interpréter la volatilité implicite, l'IV Rank/Percentile, le skew, la term structure, et identifier les opportunités de mispricing.
- **Sélection de sous-jacent (GARP)** : appliquer la méthodologie Growth At a Reasonable Price pour identifier des actions de qualité à prix raisonnable comme sous-jacents pour des stratégies d'options.
- **Gestion du risque** : dimensionner les positions (Kelly, fixed fractional), calculer les pertes maximales, gérer les Greeks au niveau du portefeuille, et surveiller les métriques de risque (VaR, Expected Shortfall).
- **Wheel strategy** : exécuter et optimiser le cycle complet cash-secured put / assignment / covered call pour la génération de revenus.
- **Ajustements et rolling** : décider quand et comment ajuster une position existante (roll up/down/out, conversion, repair strategy).
- **Analyse de marché** : combiner analyse technique, sentiment, options flow (unusual activity, put/call ratio, max pain) pour affiner le timing et la sélection de strikes.

## Core Principles

### La Volatilité est le Sous-Jacent Réel

Ne jamais oublier que le trader d'options trade la volatilité autant (sinon plus) que la direction. Le prix d'une option reflète une volatilité implicite (IV) qui représente l'anticipation du marché sur la volatilité future. Comparer systématiquement l'IV à la volatilité historique réalisée (HV) pour identifier les situations de sur- ou sous-évaluation. Un IV Rank > 50% indique une volatilité élevée par rapport à son historique -- favoriser les stratégies vendeuses de premium (iron condors, credit spreads). Un IV Rank < 30% favorise les stratégies acheteuses de volatilité (straddles, calendars).

### Probabilité vs Rendement : le Spectre Risque/Récompense

Chaque stratégie d'options se positionne sur un spectre probabilité/rendement. Les stratégies à haute probabilité de profit (iron condors, credit spreads OTM) offrent un rendement limité avec un risque potentiellement élevé. Les stratégies directionnelles (long calls/puts, debit spreads) offrent un rendement élevé avec une probabilité de profit plus faible. Aligner systématiquement le profil de la stratégie avec l'objectif d'investissement et la tolérance au risque.

### Le Temps est l'Ennemi de l'Acheteur, l'Allié du Vendeur

Le theta decay (érosion temporelle) est une force constante et non linéaire. L'érosion s'accélère exponentiellement dans les 30-45 derniers jours avant expiration. Les vendeurs de premium exploitent cette asymétrie en ouvrant des positions à 30-45 DTE et en les clôturant à 50-75% du profit maximum. Les acheteurs doivent compenser le theta par un mouvement suffisant du sous-jacent (delta) ou une augmentation de la volatilité (vega).

### Le Greeks Management est Non-Négociable

Gérer un portefeuille d'options sans surveiller les Greeks agrégés revient à piloter un avion sans instruments. Maintenir une conscience permanente du delta net (exposition directionnelle), du gamma (risque de gap), du theta (flux quotidien), du vega (exposition à la volatilité) et des corrélations entre positions. Définir des limites de Greeks par position et au niveau du portefeuille.

### GARP : Qualité du Sous-Jacent Avant Tout

Une stratégie d'options brillante sur un sous-jacent de mauvaise qualité reste une mauvaise position. Appliquer la méthodologie GARP (Growth At a Reasonable Price) pour sélectionner des sous-jacents présentant une croissance des bénéfices supérieure à la moyenne, une valorisation raisonnable (PEG < 1.5), un bilan solide et des catalyseurs identifiables. La qualité fondamentale du sous-jacent est le premier facteur de succès à long terme.

## Key Frameworks & Methods

### Options Pricing : la Triade Quantitative

Maîtriser trois modèles complémentaires de pricing :
- **Black-Scholes-Merton** : modèle analytique de référence pour les options européennes. Fournit des Greeks en forme fermée. Limitations : pas de dividendes discrets natifs, pas d'exercice anticipé, hypothèse de volatilité constante.
- **Modèle binomial (Cox-Ross-Rubinstein)** : arbre de prix discret permettant de pricer les options américaines, d'intégrer les dividendes discrets, et de visualiser la décision d'exercice anticipé.
- **Monte Carlo** : simulation stochastique indispensable pour les options exotiques, path-dependent, ou multi-sous-jacents. Flexible mais computationally intensive.

### Analyse de la Volatilité Implicite

Construire une discipline d'analyse de la volatilité en couches :
- **IV absolue** : le niveau brut de volatilité implicite de l'option.
- **IV Rank** : position de l'IV actuelle par rapport au range des 52 dernières semaines. IV Rank = (IV actuelle - IV min) / (IV max - IV min).
- **IV Percentile** : pourcentage de jours de trading sur les 252 derniers jours où l'IV a été inférieure à l'IV actuelle.
- **Volatility skew** : différentiel d'IV entre strikes OTM puts et OTM calls. Un skew prononcé indique une demande de protection (puts) ou une anticipation de chute.
- **Term structure** : comparaison de l'IV entre différentes expirations. Backwardation (IV court terme > long terme) signale un événement imminent.

### Stratégies par Objectif

Classifier et sélectionner les stratégies selon quatre objectifs :

**Revenus (Income)** : covered call, cash-secured put, iron condor, iron butterfly, jade lizard. Profiter du theta decay et de la mean-reversion de la volatilité. Appliquer à IV Rank élevé.

**Directionnelles** : vertical spreads (bull call, bear put), LEAPS, synthetic positions, risk reversal. Exprimer une vue directionnelle avec un risque défini et un levier contrôlé.

**Volatilité** : long straddle, long strangle, butterfly, calendar spread, diagonal spread, ratio spread. Parier sur une expansion ou contraction de la volatilité indépendamment de la direction.

**Hedging** : protective put (married put), collar, put spread collar, tail risk hedging. Protéger un portefeuille d'actions contre les baisses tout en conservant le potentiel haussier.

### Wheel Strategy

Exécuter le cycle complet de la Wheel Strategy pour la génération de revenus sur des sous-jacents de qualité (filtrés par GARP) :
1. Vendre un cash-secured put à un strike correspondant à un prix d'achat acceptable (support technique, valorisation GARP attractive).
2. Si assigné, détenir les actions et vendre immédiatement un covered call au-dessus du coût de base ajusté (prix d'achat - premium reçu).
3. Si le covered call est assigné, réaliser le profit et recommencer au step 1.
4. Réinvestir le premium collecté pour améliorer le yield annualisé.

### GARP Methodology

Appliquer le screening GARP en 6 étapes pour identifier les sous-jacents de qualité :
1. **PEG Ratio < 1.5** : Price/Earnings divisé par le taux de croissance des bénéfices. Un PEG < 1 indique une sous-valorisation relative à la croissance.
2. **Croissance des revenus** : chiffre d'affaires en croissance > 10% annualisé sur 3 ans avec accélération récente.
3. **Qualité des bénéfices** : marge opérationnelle stable ou en expansion, conversion élevée des bénéfices en free cash flow (FCF/Net Income > 80%).
4. **Solidité du bilan** : ratio dette nette/EBITDA < 2.5, current ratio > 1.5, couverture des intérêts > 5x.
5. **Positionnement sectoriel** : avantage compétitif identifiable (moat), positionnement dans un secteur en croissance structurelle.
6. **Catalyseurs** : identification d'événements pouvant déclencher une revalorisation (nouveau produit, expansion géographique, amélioration des marges, buyback).

## Decision Guide

### Sélection de Stratégie selon l'Environnement de Marché

| Environnement | IV Rank | Biais directionnel | Stratégie recommandée |
|---|---|---|---|
| Haussier, IV élevée | > 50% | Bullish | Bull put spread, short put |
| Haussier, IV basse | < 30% | Bullish | Bull call spread, LEAPS call |
| Baissier, IV élevée | > 50% | Bearish | Bear call spread, short call |
| Baissier, IV basse | < 30% | Bearish | Bear put spread, long put |
| Neutre, IV élevée | > 50% | Neutral | Iron condor, iron butterfly, strangle court |
| Neutre, IV basse | < 30% | Neutral | Calendar spread, butterfly longue |
| Événement imminent | Toute | Incertain | Long straddle/strangle, iron butterfly (selon IV) |
| Forte tendance | Toute | Fort | Vertical spread ITM, synthetic |

### Position Sizing : arbre de décision

1. Calculer le **max loss** de la position (premium payé pour les achats, différence de strikes - premium pour les spreads, potentiellement illimité pour les ventes nues).
2. Appliquer la règle de base : **ne jamais risquer plus de 1-5% du capital sur une seule position**.
3. Pour le Kelly Criterion : f* = (bp - q) / b, où b = ratio gain/perte moyen, p = probabilité de gain, q = 1 - p. Utiliser un **demi-Kelly** (f*/2) en pratique pour réduire la variance.
4. Vérifier que le **total des positions** ne concentre pas plus de 25-30% du capital dans un seul secteur ou thème.
5. Surveiller le **buying power reduction** (BPR) pour maintenir une marge de sécurité suffisante (utiliser < 50% du BPR disponible).

### Ajustement vs Clôture

| Signal | Action recommandée |
|---|---|
| Profit atteint 50-75% du max | Clôturer et réinitialiser |
| Sous-jacent approche le short strike | Roll out (même strike, expiration ultérieure) |
| Sous-jacent dépasse le short strike | Roll out + down/up pour collecter un crédit net |
| IV crush après événement | Clôturer (le theta/vega restant est réduit) |
| Perte atteint 2x le premium collecté | Clôturer (couper les pertes) |
| Fondamentaux du sous-jacent se dégradent | Clôturer immédiatement (la Wheel n'est plus valide) |

## Common Patterns & Anti-Patterns

### Patterns vertueux
- **Mechanical management** : définir les règles de gestion (entry, exit, adjustment) AVANT d'entrer en position. Automatiser les ordres de clôture à 50% de profit.
- **Diversification temporelle** : étaler les expirations sur 3-4 semaines différentes pour lisser le theta et réduire le risque de concentration.
- **Correlation awareness** : vérifier la corrélation entre les sous-jacents du portefeuille. 5 iron condors sur des tech stocks n'est PAS de la diversification.
- **Earnings avoidance** : ne jamais maintenir une position income (iron condor, covered call) à travers un earnings report. L'IV crush post-earnings est imprévisible en direction.
- **Premium reinvestment** : traiter le premium collecté comme un réducteur de coût de base, pas comme un profit réalisé.

### Anti-patterns critiques
- **Selling naked options without risk budget** : ne jamais vendre d'options nues (short call/put) sans un budget de perte maximum strict et un plan d'ajustement. Le risque est théoriquement illimité.
- **Ignoring assignment risk** : les options américaines peuvent être exercées à tout moment. Surveiller les short calls ITM proches de l'ex-dividend et les deep ITM puts proches de l'expiration.
- **Averaging down on losing option positions** : ajouter à une position perdante d'options multiplie le risque sans améliorer les probabilités. Préférer l'ajustement (roll) à l'ajout.
- **Ignoring IV environment** : acheter des straddles quand l'IV Rank est à 90% ou vendre des iron condors quand l'IV Rank est à 10% est structurellement perdant.
- **Over-leveraging with cheap OTM options** : acheter des options très OTM parce qu'elles sont "bon marché" est un piège. La probabilité de profit est extrêmement faible et le theta decay est rapide.
- **Neglecting the underlying** : trader des options sur un sous-jacent sans comprendre ses fondamentaux, son secteur et ses catalyseurs.

## Implementation Workflow

### Phase 1 -- Screening et Sélection (pré-trade)
1. Appliquer le screening GARP pour constituer une watchlist de 15-20 sous-jacents de qualité.
2. Analyser l'environnement de volatilité : IV Rank, skew, term structure pour chaque sous-jacent.
3. Vérifier le calendrier des événements : earnings, dividendes, événements macro.
4. Identifier les niveaux techniques clés (support, résistance, moyennes mobiles) pour le placement des strikes.
5. Consulter le flow d'options (unusual activity, put/call ratio, Open Interest) pour détecter le sentiment institutionnel.

### Phase 2 -- Construction et Sizing (entry)
1. Sélectionner la stratégie alignée avec la thèse, l'IV environment et l'objectif.
2. Choisir l'expiration : 30-45 DTE pour les stratégies income, 60-90 DTE pour les stratégies directionnelles, > 180 DTE pour les LEAPS.
3. Placer les strikes en utilisant les deltas comme guide : 0.30 delta pour les short strikes (70% POP), 0.16 delta pour les wings (84% POP).
4. Calculer le max loss, le breakeven, le ratio risque/rendement et le rendement annualisé.
5. Appliquer le position sizing (max 1-5% du capital en risque par trade).
6. Entrer l'ordre avec un limit price au mid-point du bid-ask spread (ajuster de 0.01-0.02 si nécessaire).

### Phase 3 -- Management Actif (during trade)
1. Surveiller quotidiennement les Greeks de position et les Greeks agrégés du portefeuille.
2. Clôturer les gagnants à 50-75% du profit maximum.
3. Appliquer les règles d'ajustement prédéfinies si le sous-jacent approche un short strike.
4. Couper les pertes si la perte atteint 2x le premium collecté (pour les stratégies crédit).
5. Monitorer le VaR quotidien et le stress test du portefeuille.

### Phase 4 -- Analyse Post-Trade et Amélioration
1. Journaliser chaque trade : setup, thèse, entry, management, exit, P&L, leçons.
2. Calculer les métriques de performance : win rate, average winner/loser, profit factor, R-multiple moyen.
3. Analyser les trades perdants pour identifier les patterns récurrents.
4. Recalibrer les paramètres de sizing et de management en fonction des résultats.

## Skills connexes

| Skill | Lien |
|---|---|
| Portfolio | `finance-de-marche:portfolio` — Gestion de portefeuille et allocation |
| Behavioral Finance | `finance-de-marche:behavioral-finance` — Psychologie du trading et biais |
| Regulatory | `finance-de-marche:regulatory` — Réglementation des produits dérivés |
| Risk Management | `entreprise:risk-management` — Cadre de gestion des risques |
| Data Literacy | `data-bi:data-literacy` — Visualisation des Greeks et P&L |

## Additional Resources

Consulter les fichiers de référence suivants pour un approfondissement détaillé :

- [Options Fundamentals](./references/options-fundamentals.md) -- Mécanique des Call/Put, diagrammes de payoff, modèles de pricing (Black-Scholes, binomial, Monte Carlo), volatilité implicite, IV Rank/Percentile, volatility smile/skew, analyse de la chaîne d'options, Open Interest et volume.

- [Greeks & Strategies](./references/greeks-strategies.md) -- Tous les Greeks en profondeur (delta, gamma, theta, vega, rho, et Greeks de second ordre : charm, vanna, volga), stratégies income (covered call, cash-secured put, iron condor, iron butterfly), directionnelles (vertical spreads, LEAPS), volatilité (straddle, strangle, butterfly, calendar), hedging, Wheel Strategy, rolling et ajustements.

- [GARP Analysis](./references/garp-analysis.md) -- Méthodologie GARP complète (Peter Lynch, Jim Slater), PEG ratio, croissance des revenus et qualité des bénéfices, analyse du bilan, free cash flow, positionnement sectoriel, marge de sécurité, identification des catalyseurs.

- [Risk Management](./references/risk-management.md) -- Position sizing (Kelly criterion, fixed fractional), calculs de perte maximale, R-multiples, corrélation et diversification, stratégies de stop-loss, gestion des Greeks de portefeuille (delta-neutral, vega-neutral), VaR et Expected Shortfall, analyse technique, sentiment, options flow.

### Ouvrages et références fondamentaux
- Sheldon Natenberg, *Option Volatility and Pricing* (2nd ed., 2014) -- La bible du pricing et de la volatilité
- Lawrence McMillan, *Options as a Strategic Investment* (5th ed., 2012) -- Référence encyclopédique des stratégies
- Nassim Taleb, *Dynamic Hedging* (1997) -- Risk management avancé pour les professionnels
- John Hull, *Options, Futures, and Other Derivatives* (11th ed., 2022) -- Fondations quantitatives
- Euan Sinclair, *Volatility Trading* (2nd ed., 2013) -- Approche systématique du trading de volatilité
- Peter Lynch, *One Up on Wall Street* (1989) -- Fondements de l'approche GARP
- Jim Slater, *The Zulu Principle* (1992) -- PEG ratio et croissance à prix raisonnable
- Ralph Vince, *The Mathematics of Money Management* (1992) -- Position sizing et Kelly Criterion
- Aaron Brown, *Red-Blooded Risk* (2011) -- Framework de risk management
