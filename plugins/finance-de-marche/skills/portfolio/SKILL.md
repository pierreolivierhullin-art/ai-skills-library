---
name: portfolio
description: This skill should be used when the user asks about "portfolio construction", "asset allocation", "modern portfolio theory", "MPT", "diversification", "rebalancing", "risk-adjusted returns", "Sharpe ratio", "CAPM", "factor investing", "ETF", "tax-loss harvesting", "efficient frontier", "construction de portefeuille", "allocation d'actifs", "théorie moderne du portefeuille", "rééquilibrage", "rendements ajustés au risque", "ratio de Sharpe", "investissement factoriel", "frontière efficiente", "Sortino ratio", "Treynor ratio", "alpha", "beta", "correlation", "corrélation", "volatility", "volatilité", "drawdown", "max drawdown", "value at risk", "VaR", "CVaR", "Monte Carlo simulation", "backtesting", "benchmark", "indice de référence", "S&P 500", "MSCI", "bonds", "obligations", "commodities", "matières premières", "REIT", "alternative investments", "investissements alternatifs", "dollar-cost averaging", "DCA", "strategic allocation", "tactical allocation", or needs guidance on portfolio management, investment strategy, and allocation optimization.
version: 1.1.0
last_updated: 2026-02
---

# Portfolio Construction, Asset Allocation & Investment Management

## Overview

Ce skill couvre l'ensemble des disciplines liées a la construction de portefeuilles, l'allocation d'actifs et la gestion d'investissements. Il fournit un cadre de decision structure pour concevoir, optimiser et maintenir des portefeuilles robustes alignes avec les objectifs de rendement, les contraintes de risque et l'horizon temporel de l'investisseur. La gestion de portefeuille ne se limite pas a la selection de titres : elle englobe la theorie financiere moderne, les strategies d'allocation, la diversification multi-dimensionnelle, le rebalancement tactique, l'optimisation fiscale et l'attribution de performance. Appliquer systematiquement les principes decrits ici pour guider chaque decision d'investissement, en privilegiant la rigueur quantitative, la diversification et la discipline systematique.

This skill covers portfolio construction, asset allocation, and investment management comprehensively. It provides a structured decision framework for designing, optimizing, and maintaining robust portfolios aligned with return objectives, risk constraints, and investment horizons. Apply these principles systematically to guide every investment decision.

## When This Skill Applies

Activer ce skill dans les situations suivantes / Activate this skill in the following situations:

- **Construction de portefeuille initiale** : definition de l'allocation strategique, selection des classes d'actifs, choix des vehicules d'investissement (ETFs, fonds, titres individuels), calibration du niveau de risque.
- **Optimisation de portefeuille existant** : analyse mean-variance, identification des inefficiences, amelioration du ratio rendement/risque, reduction des correlations excessives.
- **Strategies d'allocation d'actifs** : allocation strategique vs tactique, core-satellite, risk parity, factor-based allocation, modele de dotation (endowment model).
- **Gestion du risque de portefeuille** : stress testing, analyse de drawdown, mesure de VaR/CVaR, analyse de correlation en regime de crise, hedging via options overlay.
- **Rebalancement et maintenance** : strategies de rebalancement (calendaire, par bandes, tactique), tax-loss harvesting, gestion des flux entrants/sortants.
- **Attribution de performance** : decomposition Brinson-Fachler, analyse alpha/beta, selection de benchmarks, evaluation des couts.
- **Conseil en investissement** : allocation lifecycle, profil de risque investisseur, integration ESG, planification retraite.

## Core Principles

### Principle 1 — Diversification Is the Only Free Lunch

Appliquer la diversification sur toutes les dimensions disponibles : classes d'actifs (actions, obligations, matieres premieres, immobilier, alternatives), geographies (marches developpes, emergents, frontieres), secteurs, styles (value, growth, momentum, quality), et horizons temporels (DCA, echelonnement). La diversification reduit le risque idiosyncratique sans reduire le rendement attendu. Mesurer la diversification effective via la matrice de correlation et le nombre effectif d'actifs (Effective N).

Diversification is the only established mechanism for reducing portfolio risk without proportionally reducing expected return. Apply it across all available dimensions: asset classes, geographies, sectors, styles, and time horizons.

### Principle 2 — Risk First, Returns Follow

Definir le budget de risque avant de chercher le rendement. Utiliser des metriques quantitatives : volatilite annualisee, VaR (Value at Risk) a 95%/99%, CVaR (Conditional VaR), maximum drawdown, Ulcer Index. Construire le portefeuille en partant de la contrainte de risque maximale acceptable et optimiser le rendement attendu sous cette contrainte. Ne jamais poursuivre le rendement sans quantifier le risque associe.

### Principle 3 — Cost Minimization Compounds

Minimiser les couts frictionnels : frais de gestion (TER), spreads bid-ask, couts de transaction, taxes, impact de marche. Un ecart de 50 bps de frais annuels represente une difference de ~12% sur 20 ans (compounding effect). Privilegier les vehicules a faible cout (ETFs indiciels, fonds passifs) pour les allocations core. Reserver les strategies actives (alpha) pour les allocations satellite ou les classes d'actifs moins efficientes.

### Principle 4 — Evidence-Based Investing over Narratives

Fonder chaque decision d'investissement sur des preuves empiriques, pas sur des narratifs de marche. La recherche academique (Fama-French, Sharpe, Markowitz, Shiller) fournit un cadre robuste. L'hypothese des marches efficients (EMH) dans sa forme semi-forte implique que la majorite des gestionnaires actifs sous-performent leur benchmark apres frais. Utiliser les facteurs de risque documentes (market, size, value, profitability, investment, momentum) comme briques de construction.

### Principle 5 — Systematic Process over Discretionary Impulse

Etablir un Investment Policy Statement (IPS) formel definissant : objectifs de rendement, contraintes de risque, horizon temporel, besoins de liquidite, contraintes fiscales, preferences ESG. Suivre un processus systematique de rebalancement et de revue. Eliminer les biais comportementaux (loss aversion, recency bias, overconfidence) par l'automatisation et la discipline.

### Principle 6 — Tax Awareness as Alpha Source

Traiter l'optimisation fiscale comme une source d'alpha apres impots. Appliquer systematiquement : localisation d'actifs (asset location) entre comptes fiscalises et defiscalises, tax-loss harvesting, gestion des plus-values court terme vs long terme, utilisation strategique des enveloppes fiscales (PEA, assurance-vie, ISA, 401k/IRA).

## Key Frameworks & Methods

### Modern Portfolio Theory (MPT) — Markowitz Framework

L'optimisation mean-variance de Markowitz (1952) reste le fondement de la construction de portefeuille. Identifier la frontiere efficiente : l'ensemble des portefeuilles offrant le rendement maximal pour chaque niveau de risque. Le portefeuille optimal se situe au point de tangence entre la frontiere efficiente et la Capital Market Line (CML).

| Composante | Formule / Concept | Application |
|---|---|---|
| **Rendement attendu** | E(Rp) = sum(wi * E(Ri)) | Moyenne ponderee des rendements attendus |
| **Variance du portefeuille** | sigma_p^2 = sum_i sum_j wi*wj*cov(Ri,Rj) | Effet de diversification via covariances |
| **Frontiere efficiente** | Ensemble des portefeuilles min-variance pour chaque cible de rendement | Contrainte : sum(wi) = 1, wi >= 0 (sans vente a decouvert) |
| **Ratio de Sharpe** | (Rp - Rf) / sigma_p | Rendement excedentaire par unite de risque total |

### Capital Asset Pricing Model (CAPM)

Le CAPM (Sharpe 1964, Lintner 1965) definit la relation d'equilibre entre risque et rendement : E(Ri) = Rf + beta_i * (E(Rm) - Rf). Le beta mesure la sensibilite au risque de marche (risque systematique). L'alpha represente le rendement excedentaire par rapport a la prediction du CAPM. La Security Market Line (SML) represente graphiquement cette relation.

### Risk-Adjusted Performance Metrics

| Ratio | Formule | Utilisation |
|---|---|---|
| **Sharpe** | (Rp - Rf) / sigma_p | Rendement excedentaire par unite de risque total |
| **Sortino** | (Rp - Rf) / sigma_downside | Penalise uniquement la volatilite baissiere |
| **Treynor** | (Rp - Rf) / beta_p | Rendement excedentaire par unite de risque systematique |
| **Calmar** | CAGR / Max Drawdown | Rendement par unite de drawdown maximal |
| **Information Ratio** | (Rp - Rb) / Tracking Error | Alpha par unite de risque actif vs benchmark |

### Fama-French Factor Models

Le modele a 3 facteurs (1993) ajoute size (SMB) et value (HML) au facteur marche. Le modele a 5 facteurs (2015) ajoute profitability (RMW) et investment (CMA). Utiliser ces facteurs comme briques d'allocation pour capturer les primes de risque documentees. Le facteur momentum (Carhart 1997) est souvent ajoute en complement.

### Allocation Strategies Decision Matrix

| Strategie | Philosophie | Complexite | Profil cible |
|---|---|---|---|
| **Strategic (Buy & Hold)** | Allocation fixe long terme basee sur les rendements attendus | Faible | Investisseur passif, horizon long |
| **Tactical (TAA)** | Deviations temporaires de l'allocation strategique selon les conditions de marche | Elevee | Gestionnaire actif, capacite de timing |
| **Core-Satellite** | Coeur passif (60-80%) + satellites actifs (20-40%) | Moyenne | Compromis cout/alpha |
| **Risk Parity** | Egalisation des contributions au risque par classe d'actifs | Elevee | Sensibilite aux regimes de risque |
| **Factor-Based** | Allocation par facteurs de risque (value, momentum, quality) | Elevee | Investisseur quantitatif |
| **Endowment Model** | Large allocation aux alternatives (PE, hedge funds, real assets) | Tres elevee | Dotations, family offices, horizon > 10 ans |

## Decision Guide

### Arbre de decision de construction de portefeuille / Portfolio Construction Decision Tree

```
1. Quel est l'horizon d'investissement ?
   |-- < 2 ans --> Obligations court terme, money market, pas d'actions
   |-- 2-5 ans --> Allocation conservatrice (30-50% actions, 50-70% obligations)
   |-- 5-10 ans --> Allocation equilibree (50-70% actions, 20-40% obligations, 10% alternatives)
   +-- > 10 ans --> Allocation aggressive (70-90% actions, 5-15% obligations, 5-15% alternatives)

2. Quelle est la tolerance au risque (max drawdown acceptable) ?
   |-- < 10% --> Risk parity, allocation defensive, hedging via options
   |-- 10-25% --> Allocation equilibree standard, diversification large
   |-- 25-40% --> Allocation actions dominante, facteurs agressifs
   +-- > 40% --> Concentration sectorielle/thematique, levier possible

3. Quelles sont les contraintes fiscales ?
   |-- Compte fiscalise --> Asset location optimale, tax-loss harvesting actif
   |-- Compte defiscalise (PEA, IRA, ISA) --> Maximiser les actifs a haut rendement/turnover
   +-- Mix des deux --> Strategie de localisation par classe d'actifs

4. Quel est le budget de frais acceptable ?
   |-- < 20 bps --> ETFs indiciels uniquement, portefeuille 100% passif
   |-- 20-50 bps --> Core-satellite (core passif + satellites factoriels)
   |-- 50-100 bps --> Fonds actifs selectionnes + ETFs
   +-- > 100 bps --> Gestion alternative, PE, hedge funds (justifier l'alpha net)
```

### Selection des vehicules d'investissement

| Vehicule | Avantages | Inconvenients | Cas d'usage |
|---|---|---|---|
| **ETFs indiciels** | Faible cout, liquidite, transparence, efficience fiscale | Pas d'alpha, tracking error | Core allocation, marches efficients |
| **Fonds indiciels** | Faible cout, pas de spread bid-ask | Moins liquides que les ETFs, NAV une fois/jour | Plans d'epargne reguliers, petits montants |
| **Fonds actifs** | Potentiel d'alpha, expertise sectorielle | Frais eleves, majorite sous-performe | Marches inefficients (small cap, EM, credit) |
| **Titres individuels** | Controle total, tax-loss harvesting granulaire | Risque idiosyncratique, couts de recherche | Direct indexing, convictions fortes |
| **Options overlay** | Couverture, generation de revenus (covered calls) | Complexite, risque de mauvais timing | Hedging tactique, income enhancement |
| **Alternatives (PE, HF, REIT)** | Diversification, primes d'illiquidite | Illiquidite, frais eleves, complexite | Endowment model, horizon tres long |

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Dollar-Cost Averaging (DCA)** : investir des montants fixes a intervalles reguliers pour lisser le prix d'entree et eliminer le risque de timing. Particulierement efficace pour les investisseurs individuels avec des revenus reguliers.
- **Rebalancement par bandes (Threshold Rebalancing)** : rebalancer uniquement quand une classe d'actifs devie de plus de 5% (relatif) ou 3% (absolu) de l'allocation cible. Plus efficient que le rebalancement calendaire car il capture la mean reversion tout en minimisant les transactions.
- **Tax-Loss Harvesting systematique** : realiser les pertes latentes pour compenser les gains, en respectant les regles de wash sale (30 jours aux USA). Remplacer immediatement par un actif similaire mais non identique pour maintenir l'exposition.
- **Core-Satellite** : allouer 70-80% du portefeuille a des vehicules passifs low-cost (core) et 20-30% a des strategies actives ou thematiques (satellites). Le core assure la performance de marche, les satellites visent l'alpha.
- **Glide Path (Lifecycle)** : reduire progressivement l'exposition actions en approchant de la date cible (retraite). Regle heuristique : % actions = 110 - age (a ajuster selon la tolerance au risque et les sources de revenus).

### Anti-patterns critiques

- **Home Bias** : surponderer les actifs domestiques. Un investisseur francais ne devrait pas avoir 80% de son portefeuille en actions francaises (la France represente ~3% de la capitalisation mondiale). Diversifier globalement.
- **Performance Chasing (Return Chasing)** : acheter les actifs qui ont le plus performe recemment. La mean reversion est documentee : les top performers d'une periode sous-performent souvent la suivante. Rebalancer contre-cycliquement.
- **Over-Diversification (Diworsification)** : ajouter des actifs au-dela du point ou la diversification marginale est negligeable. Au-dela de 30-40 titres dans une classe d'actifs, le benefice de diversification est minimal. Surveiller les correlations effectives.
- **Neglecting Costs** : ignorer l'impact compose des frais. Un fonds a 1.5% de TER doit generer 1.5% d'alpha annuel juste pour egaliser un ETF a 0.07%. Sur 30 ans, cette difference represente ~35% du capital final.
- **Market Timing** : tenter de predire les mouvements de marche a court terme. La recherche montre que manquer les 10 meilleurs jours de bourse sur 20 ans reduit le rendement de plus de 50%. Rester investi systematiquement.
- **Concentration non compensee** : prendre un risque idiosyncratique sans prime de risque correspondante. Le risque specifique a un titre n'est pas remunere car il est diversifiable. Concentrer uniquement avec une these d'investissement documentee et un sizing rigoureux.

## Implementation Workflow

### Phase 1 — Profilage et Objectifs / Profiling & Objectives
1. Definir l'Investment Policy Statement (IPS) : objectifs de rendement (nominal/reel), horizon temporel, besoins de liquidite, contraintes legales/reglementaires.
2. Evaluer la tolerance au risque (questionnaire + analyse de la capacite financiere a absorber les pertes).
3. Identifier les contraintes fiscales : type de comptes, taux marginal d'imposition, enveloppes disponibles (PEA, assurance-vie, CTO, IRA, 401k).
4. Documenter les preferences : exclusions ESG, restrictions sectorielles, besoins de revenus reguliers.

### Phase 2 — Allocation Strategique / Strategic Allocation
5. Definir l'univers d'investissement : classes d'actifs eligibles (actions, obligations, immobilier, matieres premieres, alternatives).
6. Estimer les rendements attendus, volatilites et correlations pour chaque classe d'actifs (utiliser les primes de risque historiques ajustees des conditions actuelles).
7. Optimiser l'allocation via mean-variance (Markowitz) ou risk parity selon le profil. Appliquer des contraintes de robustesse (Black-Litterman, resampled efficient frontier).
8. Definir les bandes de rebalancement pour chaque classe d'actifs.

### Phase 3 — Implementation / Implementation
9. Selectionner les vehicules d'investissement pour chaque classe d'actifs (ETFs, fonds, titres directs) en minimisant les couts totaux.
10. Optimiser la localisation d'actifs (asset location) entre comptes fiscalises et defiscalises.
11. Executer l'allocation initiale (en une fois ou via DCA selon la taille et les conditions de marche).
12. Mettre en place les alertes de rebalancement et le calendrier de revue.

### Phase 4 — Monitoring et Maintenance / Monitoring & Maintenance
13. Surveiller les deviations d'allocation et declencher le rebalancement selon les bandes definies.
14. Executer le tax-loss harvesting de maniere opportuniste (pertes latentes > seuil minimum).
15. Analyser la performance via attribution Brinson-Fachler : decomposer entre effet allocation, effet selection et effet interaction.
16. Realiser un stress test trimestriel (scenarios historiques : 2008, 2020, 2022 ; scenarios hypothetiques : hausse de taux +300bps, recession, choc geopolitique).
17. Reviser l'IPS annuellement ou lors de changements de situation (mariage, retraite, heritage).

## Template actionnable

### Grille d'allocation d'actifs

| Classe d'actifs | Allocation cible | Allocation réelle | Écart | Action |
|---|---|---|---|---|
| **Actions US** | ___% | ___% | ___% | ___ |
| **Actions Europe** | ___% | ___% | ___% | ___ |
| **Actions Émergents** | ___% | ___% | ___% | ___ |
| **Obligations souveraines** | ___% | ___% | ___% | ___ |
| **Obligations corporate** | ___% | ___% | ___% | ___ |
| **Immobilier (REITs)** | ___% | ___% | ___% | ___ |
| **Matières premières** | ___% | ___% | ___% | ___ |
| **Cash / Monétaire** | ___% | ___% | ___% | ___ |
| **Total** | 100% | 100% | — | — |

> Rééquilibrer quand l'écart dépasse ±5% de l'allocation cible.

## Prompts types

- "Comment construire un portefeuille diversifié avec des ETF ?"
- "Aide-moi à rééquilibrer mon allocation d'actifs"
- "Calcule le ratio de Sharpe de mon portefeuille"
- "Propose une allocation factorielle pour un profil modéré"
- "Comment mettre en place le tax-loss harvesting ?"
- "Analyse la corrélation entre mes positions et propose des améliorations"

## Skills connexes

| Skill | Lien |
|---|---|
| Options Risk | `finance-de-marche:options-risk` — Couverture et stratégies d'options |
| Behavioral Finance | `finance-de-marche:behavioral-finance` — Biais d'investissement et discipline |
| Regulatory | `finance-de-marche:regulatory` — Conformité et fiscalité du portefeuille |
| Finance | `entreprise:finance` — Modélisation financière et valorisation |
| Decision Reporting | `data-bi:decision-reporting-governance` — Dashboards et suivi de performance |

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[Modern Portfolio Theory](./references/modern-portfolio-theory.md)** : Markowitz mean-variance optimization, frontiere efficiente, CAPM (beta, alpha, SML), ratios de Sharpe/Sortino/Treynor/Calmar, hypothese des marches efficients (EMH), modeles factoriels Fama-French 3 et 5 facteurs, optimisation rendement-risque.
- **[Asset Allocation](./references/asset-allocation.md)** : allocation strategique vs tactique, core-satellite, risk parity (All-Weather), factor-based allocation, modele de dotation (Yale/Swensen), allocation lifecycle, Black-Litterman.
- **[Portfolio Management](./references/portfolio-management.md)** : strategies de rebalancement, tax-loss harvesting, attribution de performance (Brinson-Fachler), selection de benchmarks, gestion du drawdown, stress testing, Investment Policy Statement.
- **[Investment Vehicles](./references/investment-vehicles.md)** : ETFs vs fonds communs, investissement indiciel (Bogle), strategies d'options overlay, investissements alternatifs (REITs, PE, hedge funds), produits structures, fractional shares, investissement thematique.
