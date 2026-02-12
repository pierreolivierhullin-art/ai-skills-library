# Portfolio Management — Rebalancing, Tax Optimization, Performance Attribution & Risk Control

## Overview

Ce document de reference couvre les aspects operationnels de la gestion de portefeuille : strategies de rebalancement, optimisation fiscale (tax-loss harvesting, asset location), attribution de performance (Brinson-Fachler), selection de benchmarks, gestion du drawdown et stress testing. Utiliser ce guide pour structurer la maintenance operationnelle et le monitoring continu de tout portefeuille.

This reference covers the operational aspects of portfolio management: rebalancing strategies, tax optimization, performance attribution, benchmark selection, drawdown management, and stress testing. Use this guide to structure the operational maintenance and continuous monitoring of any portfolio.

---

## Rebalancing Strategies

### Pourquoi rebalancer / Why Rebalance

Le rebalancement ramene le portefeuille vers son allocation cible apres les mouvements de marche. Sans rebalancement, un portefeuille tend a deriver vers une allocation dominee par les actifs les plus performants (et souvent les plus risques), augmentant le risque au-dela du niveau cible. Le rebalancement est une forme systematique de "buy low, sell high" qui capture la mean reversion.

Rebalancing brings the portfolio back to target allocation after market movements. Without rebalancing, a portfolio drifts toward the best-performing (often riskiest) assets, increasing risk beyond target levels.

### Calendar Rebalancing (Rebalancement calendaire)

Rebalancer a intervalles fixes (mensuel, trimestriel, semestriel, annuel).

| Frequence | Avantages | Inconvenients | Recommandation |
|---|---|---|---|
| **Mensuel** | Controle strict du risque | Couts de transaction eleves, impact fiscal | Non recommande sauf pour portefeuilles institutionnels sans contraintes fiscales |
| **Trimestriel** | Bon compromis cout/controle | Peut manquer des deviations intenses en marche volatile | Recommande pour portefeuilles > 1M avec gestion active |
| **Semestriel** | Couts faibles | Deviations potentiellement larges | Convient aux portefeuilles passifs equilibres |
| **Annuel** | Couts minimaux | Deviations potentiellement tres larges | Acceptable pour portefeuilles tres long terme, full passive |

### Threshold Rebalancing (Rebalancement par bandes)

Rebalancer uniquement quand une classe d'actifs devie au-dela d'un seuil predetermine. Approche plus efficiente que le calendaire car elle rebalance quand c'est necessaire, pas quand c'est prevu.

#### Calibration des bandes / Band Calibration

| Classe d'actifs | Bande recommandee (deviation absolue) | Bande relative | Justification |
|---|---|---|---|
| **Actions domestiques** | +/- 5% | +/- 10% | Haute volatilite, deviation frequente |
| **Actions internationales** | +/- 5% | +/- 10% | Haute volatilite |
| **Obligations investment grade** | +/- 3% | +/- 10% | Volatilite moderee |
| **Alternatives / REIT** | +/- 2% | +/- 20% | Poids faible, seuil relatif large |
| **Matieres premieres / Or** | +/- 2% | +/- 20% | Poids faible |
| **Cash** | +/- 2% | +/- 50% | Poids minimal |

#### Methodologie

1. Verifier quotidiennement (ou hebdomadairement) si les poids reels sont dans les bandes cibles.
2. Si un actif sort de sa bande, evaluer le cout de rebalancement (frais, taxes, spread) vs le benefice en reduction de risque.
3. Rebalancer vers le milieu de la bande (et non exactement vers le poids cible) pour reduire la frequence de declenchement.
4. Combiner avec un calendrier (ex: threshold + check trimestriel obligatoire).

### Cash Flow Rebalancing

Utiliser les flux entrants (epargne reguliere, dividendes, coupons) pour acheter les classes d'actifs sous-ponderees plutot que de vendre les sur-ponderees. Avantages : zero cout de transaction additionnel, zero impact fiscal. Limite : ne fonctionne que si les flux sont suffisamment importants par rapport au portefeuille.

### Tax-Aware Rebalancing

Integrer les consequences fiscales dans chaque decision de rebalancement :

1. **Privilegier les ventes de lots en perte** : realiser les pertes (tax-loss harvesting) en priorite pour rebalancer.
2. **Utiliser les comptes defiscalises** : rebalancer dans les comptes PEA, IRA, ISA ou l'enveloppe assurance-vie ou il n'y a pas d'impact fiscal.
3. **Reporter les ventes en gain court terme** : si possible, attendre que les plus-values passent en long terme (1 an aux USA, 2 ans pour le PEA en France) pour beneficier d'un taux d'imposition reduit.
4. **Lot selection (LIFO, FIFO, specific identification)** : choisir les lots a vendre pour minimiser l'impact fiscal. L'identification specifique (specific share identification) est optimale mais plus complexe operationnellement.

---

## Tax-Loss Harvesting (TLH)

### Principes / Principles

Le tax-loss harvesting consiste a realiser les pertes latentes dans un portefeuille pour generer des deductions fiscales, tout en maintenant une exposition de marche similaire en remplacant l'actif vendu par un actif similaire mais non identique.

Tax-loss harvesting involves realizing latent losses to generate tax deductions while maintaining similar market exposure by replacing the sold asset with a similar but non-identical substitute.

### Workflow systematique / Systematic Workflow

1. **Scanner** : identifier quotidiennement ou hebdomadairement les positions avec des pertes latentes significatives (seuil : perte > 2-3% de la position ou > 500 EUR/USD en valeur absolue).
2. **Evaluer** : calculer l'economie fiscale nette (perte * taux marginal d'imposition - couts de transaction - spread bid-ask).
3. **Executer** : vendre l'actif en perte et acheter immediatement un substitut pour maintenir l'exposition.
4. **Documenter** : enregistrer la date de vente, le substitut utilise et la date de wash sale (30 jours aux USA).
5. **Reverser** : apres la periode de wash sale, revenir a l'actif original si desire (optionnel).

### Regles de wash sale / Wash Sale Rules

**USA** : interdiction de racheter un actif "substantiellement identique" dans les 30 jours avant ou apres la vente en perte. Violation : la perte est reportee sur le cout de base du nouvel actif (pas perdue, mais differee). Les ETFs du meme indice mais de fournisseurs differents (ex: VTI vs ITOT) sont generalement consideres comme non substantiellement identiques.

**France** : pas de regle de wash sale formelle, mais l'abus de droit (article L64 du LPF) peut s'appliquer si l'administration fiscale demontre que la transaction n'a pas de substance economique hors avantage fiscal. En pratique, le risque est faible pour les substitutions d'ETFs avec un delai raisonnable.

**UK** : "bed and breakfasting" rule — regle des 30 jours similaire aux USA pour les actions et parts de fonds. Les substituts doivent etre suffisamment differents.

### Substitution pairs (exemples) / Substitution Pairs

| Actif vendu | Substitut | Correlation | Commentaire |
|---|---|---|---|
| ETF S&P 500 (VOO/SPY) | ETF Russell 1000 (IWB) ou MSCI USA (EUSA) | > 0.99 | Meme univers, indice different |
| ETF MSCI World (IWDA) | ETF FTSE All-World (VWCE) | > 0.98 | Indices similaires, fournisseurs differents |
| ETF MSCI EM (EEM) | ETF FTSE EM (VWO) | > 0.97 | Differences : Coree du Sud classifiee differemment |
| ETF Aggregate Bond (AGG) | ETF Core Bond (BND) | > 0.99 | Barclays Agg vs Bloomberg Agg |
| ETF Small Cap Value (VBR) | ETF S&P 600 Value (IJS) | > 0.95 | Univers similaire, methodologie differente |

### Direct Indexing

Le direct indexing represente l'evolution ultime du tax-loss harvesting : detenir les composantes individuelles d'un indice (ex: les 500 actions du S&P 500) plutot qu'un ETF. Cela permet un TLH au niveau de chaque titre individuel, multipliant les opportunites de harvesting.

**Avantages** :
- TLH granulaire : chaque titre peut etre harveste individuellement (vs un seul lot pour un ETF)
- Personnalisation : exclure certains titres (ESG, conflits d'interets) tout en maintenant les caracteristiques d'indice
- Estimation de l'alpha fiscal : 1-2% annualise les premieres annees, declinant progressivement (les lots s'apprecient)

**Inconvenients** :
- Complexite operationnelle : gerer 500+ positions, corporate actions, dividendes
- Cout : les plateformes de direct indexing (Wealthfront, Parametric, Aperio) prelevent 0.20-0.40%
- Diminishing returns : l'alpha fiscal decline avec le temps car les lots gagnants dominent
- Seuil de taille : generalement viable a partir de 100K-250K USD par compte

### Asset Location (Localisation d'actifs)

Optimiser la repartition des classes d'actifs entre les differents types de comptes pour minimiser l'impot total :

| Type d'actif | Placement optimal | Raison |
|---|---|---|
| **Obligations imposables (coupons)** | Compte defiscalise (IRA, PEA-PME, assurance-vie) | Coupons taxes comme revenu ordinaire (taux marginal eleve) |
| **REITs** | Compte defiscalise | Dividendes taxes comme revenu ordinaire |
| **Actions internationales** | Compte fiscalise (CTO) | Credit d'impot etranger non recupable en IRA/PEA |
| **Actions croissance (faibles dividendes)** | Compte fiscalise (CTO) | Plus-values taxees a taux preferentiel (long terme) |
| **ETFs indiciels (faible distribution)** | Compte fiscalise (CTO) | Efficience fiscale naturelle des ETFs |
| **Strategies a turnover eleve (momentum, tactique)** | Compte defiscalise | Le turnover genere des plus-values court terme taxees lourdement |

---

## Performance Attribution (Brinson-Fachler)

### Modele Brinson-Fachler / Brinson-Fachler Model

L'attribution de performance decompose le rendement actif (portefeuille vs benchmark) en trois effets :

```
Rendement actif = Effet Allocation + Effet Selection + Effet Interaction

Rp - Rb = SUM(i) [(wp_i - wb_i) * (Rb_i - Rb)]     --> Allocation
         + SUM(i) [wb_i * (Rp_i - Rb_i)]              --> Selection
         + SUM(i) [(wp_i - wb_i) * (Rp_i - Rb_i)]     --> Interaction
```

| Effet | Formule | Interpretation |
|---|---|---|
| **Allocation** | (wp_i - wb_i) * (Rb_i - Rb) | Surperformance due au choix de surponderer/sous-ponderer certains segments |
| **Selection** | wb_i * (Rp_i - Rb_i) | Surperformance due au choix de titres au sein de chaque segment |
| **Interaction** | (wp_i - wb_i) * (Rp_i - Rb_i) | Effet combine allocation x selection |

### Application pratique / Practical Application

1. **Definir les segments** : decomposer le portefeuille et le benchmark en segments identiques (par classe d'actifs, secteur, geographie, ou facteur).
2. **Calculer les rendements par segment** : pour le portefeuille (Rp_i) et le benchmark (Rb_i).
3. **Calculer les poids par segment** : pour le portefeuille (wp_i) et le benchmark (wb_i).
4. **Appliquer la decomposition** : calculer les trois effets pour chaque segment et les sommer.
5. **Interpreter** : un effet allocation positif signifie que les decisions de surponderation/sous-ponderation ont ajoute de la valeur. Un effet selection positif signifie que les titres selectionnes dans chaque segment ont surperforme.

### Multi-Period Attribution

L'attribution Brinson-Fachler sur une seule periode est additive. Pour les attributions multi-periodes, utiliser les methodes :
- **Linking geometrique (Carino, 1999)** : ajuster les effets pour que la somme corresponde au rendement actif geometrique.
- **Methode de Menchero (2004)** : decomposition additive sur plusieurs periodes avec ajustement de liaison.
- **Methode de Frongello** : approche plus simple mais moins precise.

### Factor-Based Attribution

Decomposer le rendement actif en contributions factorielles plutot que par segment :

```
alpha = Rp - [Rf + beta_m*(Rm-Rf) + beta_s*SMB + beta_v*HML + beta_r*RMW + beta_c*CMA + beta_mom*MOM]
```

L'alpha residuel apres controle de tous les facteurs represente le vrai alpha idiosyncratique (skill du gestionnaire). Si l'alpha est explique par les facteurs, le gestionnaire ne fait que prendre des paris factoriels (ce qui peut etre replique a moindre cout via des ETFs factoriels).

---

## Benchmark Selection

### Criteres de selection / Selection Criteria

Un benchmark valide doit etre :

| Critere | Description | Exemple |
|---|---|---|
| **Representatif** | Refleter l'univers d'investissement et le style du portefeuille | MSCI World pour un portefeuille actions mondiales |
| **Investissable** | Composable de titres reellement achetables | Pas un indice theorique non replicable |
| **Mesurable** | Rendements et composition calculables de maniere fiable | Indices publies par des fournisseurs reconnus |
| **Non ambigu** | Composition et regles clairement definies | Methodologie d'indice transparente |
| **Specifie a l'avance** | Defini avant la periode d'evaluation | Pas de benchmark changing post facto |
| **Appropriate** | Coherent avec le mandat et les contraintes du portefeuille | Pas d'utiliser le S&P 500 pour un portefeuille global |

### Benchmarks courants / Common Benchmarks

| Classe d'actifs | Benchmark | Usage |
|---|---|---|
| Actions monde | MSCI ACWI, FTSE All-World | Portefeuille actions global |
| Actions monde developpe | MSCI World, FTSE Developed | Actions DM |
| Actions US | S&P 500, Russell 3000 | Actions US large/broad |
| Actions Europe | STOXX Europe 600, MSCI Europe | Actions EU |
| Actions EM | MSCI Emerging Markets, FTSE EM | Actions marches emergents |
| Obligations monde | Bloomberg Global Aggregate | Obligations mondiales |
| Obligations US | Bloomberg US Aggregate | Obligations US |
| Obligations Euro | Bloomberg Euro Aggregate, iBoxx Euro | Obligations EUR |
| Multi-asset balanced | 60% MSCI ACWI + 40% Bloomberg Global Agg | Benchmark composite |
| HY Credit | ICE BofA US High Yield | Credit a haut rendement |
| Real Estate | FTSE EPRA/NAREIT | Immobilier cote |

### Custom Benchmarks

Pour les portefeuilles multi-asset ou les mandats specifiques, construire un benchmark composite :
- Definir les poids de chaque sous-benchmark (ex: 50% MSCI World + 20% Bloomberg Agg + 15% MSCI EM + 10% FTSE EPRA/NAREIT + 5% Bloomberg Commodity).
- Rebalancer le benchmark compositellon la meme frequence que le portefeuille.
- Documenter la composition dans l'IPS.

---

## Drawdown Management

### Mesures de drawdown / Drawdown Metrics

| Metrique | Definition | Seuils d'alerte |
|---|---|---|
| **Maximum Drawdown** | Perte maximale du pic au creux sur la periode | > 20% pour portefeuille balanced, > 35% pour growth |
| **Drawdown Duration** | Temps passe en dessous du pic precedent | > 24 mois pour un portefeuille balanced |
| **Recovery Time** | Temps pour revenir au pic precedent apres le creux | > 36 mois necessitant une revue de strategie |
| **Ulcer Index** | Racine de la moyenne des drawdowns au carre | Capture la severite et la duree des drawdowns |
| **Pain Index** | Moyenne des drawdowns sur la periode | Mesure l'experience de l'investisseur |

### Drawdowns historiques de reference / Historical Reference Drawdowns

| Evenement | Dates | S&P 500 Drawdown | Portefeuille 60/40 | Recovery time (S&P 500) |
|---|---|---|---|---|
| Dot-com crash | 2000-2002 | -49% | -22% | 7 ans |
| Global Financial Crisis | 2007-2009 | -57% | -31% | 5.5 ans |
| COVID crash | Feb-Mar 2020 | -34% | -18% | 5 mois |
| 2022 Rate shock | Jan-Oct 2022 | -25% | -22% | ~2 ans |

### Strategies de gestion du drawdown / Drawdown Management Strategies

- **Pre-emptive (avant le drawdown)** : diversifier adequatement, calibrer le niveau de risque selon la tolerance, utiliser des strategies de tail hedging (puts OTM, VIX calls) si le budget le permet.
- **During drawdown** : resister a la tentation de vendre en panic. Rebalancer systematiquement (acheter les actifs en baisse, vendre ceux qui tiennent). Utiliser le cash flow rebalancing.
- **Post-drawdown** : evaluer si le drawdown a depasse les limites de l'IPS. Si oui, revoir l'allocation strategique, pas en reaction mais apres analyse reflechie. Documenter les lessons learned.
- **Tail risk hedging** : allouer 1-3% du portefeuille a des strategies de couverture du tail risk. Options : puts OTM sur indice (couteux, drag en marche haussier), strategies trend-following (CTA/managed futures), allocation or/tresorerie.

---

## Stress Testing

### Approches de stress testing / Stress Testing Approaches

#### Historical Scenario Analysis
Appliquer les rendements historiques de periodes de crise au portefeuille actuel :

| Scenario | Periode | Choc principal | Impact type sur portefeuille balanced |
|---|---|---|---|
| **GFC 2008** | Sep 2008 - Mar 2009 | Credit crunch, bank failures | Actions -45%, Obligations +10%, Credit -15% |
| **Taper Tantrum** | Mai-Juin 2013 | Hausse soudaine des taux | Obligations -5%, EM -15%, Actions DM -5% |
| **COVID** | Feb-Mar 2020 | Shutdown economique mondial | Actions -30%, Obligations +5%, Credit -10% |
| **2022 Rate Shock** | Jan-Oct 2022 | Hausse de taux +400bps, inflation | Actions -20%, Obligations -15%, 60/40 echec diversification |
| **Crise souveraine EUR** | 2011-2012 | Risque de defaut EUR peripherie | Actions EUR -25%, Obligations PIGS -30% |

#### Hypothetical Scenario Analysis
Construire des scenarios hypothetiques pour evaluer les vulnerabilites :

| Scenario | Parametres | Ce qu'il teste |
|---|---|---|
| **Rate shock +300bps** | Taux souverains +300bps sur 6 mois | Sensibilite aux taux, duration du portefeuille |
| **Recession severe** | PIB -5%, earnings -30%, spreads +500bps | Risque de credit, cyclicite du portefeuille |
| **Inflation surprise** | Inflation +5% vs attentes | Couverture inflation, actifs reels |
| **Correlation 1** | Toutes les correlations convergent vers 1 | Diversification effective en stress |
| **Liquidite** | Spreads x3, volumes /3, pas d'acces aux marches de credit | Risque de liquidite du portefeuille |
| **Choc geopolitique** | Conflit majeur, sanctions, disruption supply chain | Concentration geographique, exposition sectorielle |

#### Sensitivity Analysis
Varier un parametre a la fois pour comprendre les sensibilites du portefeuille :
- **Duration** : impact d'un mouvement de 1bp sur la valeur obligataire (DV01)
- **Beta** : impact d'un mouvement de 1% du marche sur le portefeuille
- **Credit spread** : impact d'un ecartement de 100bps sur le credit corporate
- **Change** : impact d'une variation de 10% du taux de change

### Frequence et gouvernance / Frequency and Governance

- Realiser un stress test complet (historical + hypothetical) au minimum trimestriellement.
- Presenter les resultats au comite d'investissement ou documenter dans le journal de bord du portefeuille.
- Si un scenario produit un drawdown depassant la tolerance definie dans l'IPS, prendre des mesures correctives : reduire l'exposition, ajouter des couvertures, ou reviser l'allocation.
- Mettre a jour les scenarios hypothetiques annuellement pour reflet les risques contemporains.

---

## Investment Policy Statement (IPS)

### Structure recommandee / Recommended Structure

Rediger un IPS formel pour chaque portefeuille, couvrant :

1. **Objectifs de rendement** : rendement cible nominal/reel, net de frais et d'impots. Distinguer objectifs de croissance et objectifs de revenu.
2. **Contraintes de risque** : volatilite maximale, drawdown maximal tolere, VaR limit, tracking error budget.
3. **Horizon temporel** : duree d'investissement, dates de liquidite obligatoire, staged withdrawal schedule.
4. **Besoins de liquidite** : flux de tresorerie attendus (entrees/sorties), reserve de liquidite minimale.
5. **Contraintes legales et reglementaires** : restrictions reglementaires (UCITS, ERISA), restrictions fiscales, ratios prudentiels.
6. **Considerations fiscales** : type de comptes, taux marginal d'imposition, strategies d'optimisation.
7. **Preferences uniques** : exclusions ESG, restrictions sectorielles/geographiques, actifs illiquides.
8. **Allocation strategique cible** : poids par classe d'actifs, bandes de rebalancement, vehicules selectionnes.
9. **Calendrier de revue** : frequence des revues (trimestrielle), declencheurs de revue exceptionnelle.
10. **Gouvernance** : autorite de decision, processus d'approbation, delegation.

### Revue et mise a jour / Review and Update

Reviser l'IPS :
- **Annuellement** : revue de routine, ajustement des CMAs, verification de la coherence avec la situation de l'investisseur.
- **Lors d'evenements declencheurs** : changement de situation personnelle (mariage, divorce, naissance, deces, heritage, retraite), changement reglementaire significatif, changement de regime de marche fondamental.
- **Ne jamais modifier l'IPS en reaction a un drawdown** : les modifications emotionnelles detruisent la discipline. Attendre au moins 3 mois apres un choc pour reviser calmement.
