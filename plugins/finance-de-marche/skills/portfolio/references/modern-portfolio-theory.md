# Modern Portfolio Theory — Markowitz, CAPM, Factor Models & Risk-Return Optimization

## Overview

Ce document de reference couvre les fondations theoriques de la gestion de portefeuille moderne : la theorie du portefeuille de Markowitz, le CAPM, les ratios de performance ajustee du risque, l'hypothese des marches efficients et les modeles factoriels de Fama-French. Utiliser ce guide comme fondation theorique pour toute decision de construction de portefeuille et d'evaluation de performance.

This reference document covers the theoretical foundations of modern portfolio management: Markowitz portfolio theory, CAPM, risk-adjusted performance ratios, the Efficient Market Hypothesis, and Fama-French factor models. Use this guide as the theoretical foundation for all portfolio construction and performance evaluation decisions.

---

## Markowitz Mean-Variance Optimization (1952)

### Theoretical Foundation

Harry Markowitz a revolutionne la finance en formalisant mathematiquement la relation entre risque et rendement au niveau du portefeuille. Avant Markowitz, la selection de titres se faisait titre par titre. L'innovation fondamentale est que le risque d'un portefeuille depend non seulement du risque de chaque actif mais aussi de la correlation entre les actifs.

Harry Markowitz revolutionized finance by mathematically formalizing the relationship between risk and return at the portfolio level. The fundamental insight is that portfolio risk depends not only on individual asset risk but critically on the correlations between assets.

### Mathematical Framework

#### Rendement attendu du portefeuille / Expected Portfolio Return

Le rendement attendu d'un portefeuille de n actifs est la moyenne ponderee des rendements attendus individuels :

```
E(Rp) = SUM(i=1 to n) wi * E(Ri)
```

ou wi represente le poids de l'actif i dans le portefeuille et E(Ri) son rendement attendu.

#### Variance du portefeuille / Portfolio Variance

La variance du portefeuille capture l'effet de diversification via les covariances :

```
sigma_p^2 = SUM(i=1 to n) SUM(j=1 to n) wi * wj * sigma_i * sigma_j * rho_ij
```

ou sigma_i est l'ecart-type de l'actif i et rho_ij le coefficient de correlation entre les actifs i et j. Quand rho_ij < 1, la variance du portefeuille est inferieure a la moyenne ponderee des variances individuelles : c'est l'effet de diversification.

#### Cas a deux actifs / Two-Asset Case

Pour un portefeuille de deux actifs A et B avec poids wA et wB = (1 - wA) :

```
sigma_p^2 = wA^2 * sigma_A^2 + wB^2 * sigma_B^2 + 2 * wA * wB * sigma_A * sigma_B * rho_AB
```

Le poids de variance minimale est :

```
wA* = (sigma_B^2 - sigma_A * sigma_B * rho_AB) / (sigma_A^2 + sigma_B^2 - 2 * sigma_A * sigma_B * rho_AB)
```

### Efficient Frontier / Frontiere Efficiente

La frontiere efficiente est l'ensemble des portefeuilles qui offrent le rendement maximal pour chaque niveau de risque (ou le risque minimal pour chaque niveau de rendement). Tout portefeuille situe en dessous de la frontiere est sous-optimal : il existe un portefeuille sur la frontiere offrant soit un meilleur rendement pour le meme risque, soit un risque moindre pour le meme rendement.

#### Construction de la frontiere efficiente

1. Definir l'univers d'actifs et estimer les rendements attendus, volatilites et correlations.
2. Pour chaque rendement cible Rc, resoudre le probleme d'optimisation :
   - Minimiser sigma_p^2
   - Sous les contraintes : E(Rp) = Rc, SUM(wi) = 1, wi >= 0 (contrainte de non-negativite si vente a decouvert interdite)
3. Tracer l'ensemble des portefeuilles optimaux dans l'espace (sigma, E(R)).

#### Global Minimum Variance Portfolio (GMV)

Le portefeuille de variance minimale globale est le point le plus a gauche de la frontiere efficiente. Il represente le risque minimal atteignable par diversification dans l'univers d'actifs considere. En pratique, le portefeuille GMV est souvent remarquablement performant car il ne depend pas des estimations de rendements attendus (qui sont notoirement instables).

#### Limites de l'optimisation mean-variance

- **Sensibilite aux inputs** : de petites variations dans les rendements attendus, volatilites ou correlations produisent des allocations tres differentes. L'optimiseur maximise les erreurs d'estimation (error maximization).
- **Instabilite des correlations** : les correlations augmentent significativement en periode de crise (correlation breakdown), exactement quand la diversification est la plus necessaire.
- **Hypothese de normalite** : l'optimisation MV suppose des rendements normalement distribues, ce qui ne capture pas les fat tails, le skewness et le kurtosis observes en realite.
- **Concentration excessive** : sans contraintes additionnelles, l'optimiseur tend a concentrer le portefeuille sur un petit nombre d'actifs avec les rendements attendus les plus eleves.

#### Solutions de robustesse

- **Black-Litterman (1992)** : combiner l'equilibre de marche (CAPM implicite) avec les vues de l'investisseur pour obtenir des rendements attendus plus stables. Partir de l'allocation de marche comme prior et l'ajuster selon les convictions.
- **Resampled Efficient Frontier (Michaud, 1998)** : simuler de multiples frontieres efficientes par bootstrap des parametres et moyenner les allocations. Reduit la sensibilite aux inputs.
- **Minimum Variance constrained** : imposer des contraintes de poids minimum et maximum par actif (ex: 2% <= wi <= 25%) pour eviter la concentration.
- **Shrinkage estimators (Ledoit-Wolf)** : appliquer un retrecissement (shrinkage) a la matrice de covariance vers une matrice structuree pour reduire le bruit d'estimation.
- **Risk budgeting** : definir les poids par contribution au risque plutot que par optimisation mean-variance.

---

## Capital Asset Pricing Model (CAPM)

### Theoretical Foundation

Le CAPM (Sharpe 1964, Lintner 1965, Mossin 1966) est un modele d'equilibre qui definit la relation attendue entre le risque systematique d'un actif et son rendement. Il decoule directement de la theorie de Markowitz en ajoutant un actif sans risque a l'univers d'investissement.

The CAPM is an equilibrium model defining the expected relationship between an asset's systematic risk and its return. It extends Markowitz's framework by introducing a risk-free asset.

### CAPM Equation

```
E(Ri) = Rf + beta_i * [E(Rm) - Rf]
```

- **E(Ri)** : rendement attendu de l'actif i
- **Rf** : taux sans risque (risk-free rate, typiquement T-Bills ou OAT court terme)
- **beta_i** : mesure de sensibilite de l'actif au marche (risque systematique)
- **E(Rm) - Rf** : prime de risque du marche (equity risk premium, historiquement 4-7% selon la periode et le marche)

### Beta — Risque Systematique / Systematic Risk

Le beta mesure la co-variation d'un actif avec le portefeuille de marche :

```
beta_i = Cov(Ri, Rm) / Var(Rm)
```

| Beta | Interpretation | Exemples |
|---|---|---|
| beta = 0 | Aucune correlation avec le marche | Actif sans risque, certains hedge funds |
| 0 < beta < 1 | Moins volatile que le marche | Utilities, consumer staples, obligations HY |
| beta = 1 | Meme volatilite que le marche | Fonds indiciel S&P 500 / MSCI World |
| beta > 1 | Plus volatile que le marche | Tech growth, small caps, financieres cycliques |
| beta < 0 | Mouvement inverse au marche | Or (faiblement negatif), puts, VIX futures |

### Alpha — Rendement Excedentaire / Excess Return

L'alpha (Jensen's alpha) est la difference entre le rendement realise et le rendement predit par le CAPM :

```
alpha_i = Ri - [Rf + beta_i * (Rm - Rf)]
```

Un alpha positif indique une surperformance ajustee du risque. Un alpha negatif indique une sous-performance. La persistance de l'alpha est l'objet central du debat gestion active vs passive. La recherche empirique montre que l'alpha net de frais est negatif pour la majorite des gestionnaires actifs sur la plupart des periodes.

### Security Market Line (SML)

La SML represente graphiquement la relation CAPM dans l'espace (beta, E(R)). Chaque actif devrait se situer sur la SML a l'equilibre. Les actifs au-dessus de la SML sont sous-evalues (alpha positif), ceux en dessous sont sur-evalues (alpha negatif). Ne pas confondre SML et CML (Capital Market Line) : la CML est dans l'espace (sigma, E(R)) et ne s'applique qu'aux portefeuilles efficients.

### Capital Market Line (CML)

La CML relie le taux sans risque au portefeuille de marche (tangent portfolio) dans l'espace risque-rendement :

```
E(Rp) = Rf + [(E(Rm) - Rf) / sigma_m] * sigma_p
```

La pente de la CML est le ratio de Sharpe du portefeuille de marche. Tout portefeuille efficient (combinaison de l'actif sans risque et du portefeuille de marche) se situe sur la CML.

### Limites du CAPM

- **Facteur unique** : le CAPM ne considere qu'un seul facteur de risque (le marche). La recherche empirique montre que d'autres facteurs (size, value, momentum) expliquent une part significative des rendements.
- **Beta instable** : le beta varie dans le temps, notamment en fonction du cycle economique et des conditions de marche.
- **Prime de risque non observable** : la prime de risque du marche attendue est difficile a estimer avec precision (estimations historiques vs implicites).
- **Hypotheses irrealistes** : marches sans friction, investisseurs rationnels homogenes, horizons identiques.

---

## Risk-Adjusted Performance Metrics

### Sharpe Ratio (1966)

Le ratio de Sharpe mesure le rendement excedentaire par unite de risque total (volatilite) :

```
Sharpe = (Rp - Rf) / sigma_p
```

- Interpretation : chaque unite de risque (1% de volatilite) genere Sharpe% de rendement excedentaire.
- Benchmarks : Sharpe < 0.5 = mediocre, 0.5-1.0 = acceptable, 1.0-2.0 = bon, > 2.0 = excellent (rare et souvent non durable).
- Limites : penalise symetriquement la volatilite haussiere et baissiere ; suppose des rendements normalement distribues ; sensible a la frequence de mesure (annualiser avec sqrt(N) uniquement pour des rendements iid).
- Annualisation : multiplier le Sharpe quotidien par sqrt(252), mensuel par sqrt(12).

### Sortino Ratio

Le ratio de Sortino ne penalise que la volatilite baissiere (downside deviation), utilisant un rendement cible minimal (MAR, souvent Rf ou 0) :

```
Sortino = (Rp - MAR) / sigma_downside
```

ou sigma_downside = sqrt(mean(min(Ri - MAR, 0)^2)). Preferer le Sortino au Sharpe pour evaluer les strategies dont la distribution des rendements est asymetrique (options, alternatives, strategies momentum).

### Treynor Ratio (1965)

Le ratio de Treynor mesure le rendement excedentaire par unite de risque systematique (beta) :

```
Treynor = (Rp - Rf) / beta_p
```

Utiliser le Treynor pour comparer des portefeuilles qui font partie d'un portefeuille plus large et bien diversifie (ou le risque idiosyncratique est diversifie). Le Treynor est plus pertinent que le Sharpe pour evaluer un gestionnaire dans le contexte d'une allocation globale.

### Calmar Ratio

Le ratio de Calmar rapporte le rendement annualise (CAGR) au maximum drawdown sur la periode :

```
Calmar = CAGR / |Max Drawdown|
```

Typiquement calcule sur 3 ans. Particulierement pertinent pour les strategies alternatives et les allocations tactiques ou le controle du drawdown est critique. Calmar > 1 indique que le rendement annualise depasse le maximum drawdown. Calmar > 3 est considere excellent.

### Information Ratio

L'Information Ratio mesure le rendement actif (vs benchmark) par unite de risque actif (tracking error) :

```
IR = (Rp - Rb) / TE
```

ou TE (Tracking Error) = sigma(Rp - Rb). Un IR > 0.5 est considere bon, > 1.0 exceptionnel. L'IR est la metrique centrale pour evaluer les gestionnaires actifs car elle capture la constance de la surperformance.

### Omega Ratio

L'Omega ratio capture l'integralite de la distribution des rendements (pas seulement les deux premiers moments) :

```
Omega(r) = integral(r to +inf) [1 - F(x)] dx / integral(-inf to r) F(x) dx
```

ou F(x) est la fonction de distribution cumulative des rendements et r le seuil de rendement minimum. Omega > 1 indique que les gains au-dessus du seuil depassent les pertes en dessous.

---

## Efficient Market Hypothesis (EMH)

### Les trois formes de l'EMH / The Three Forms

Eugene Fama (1970) a formalise l'EMH en trois formes :

| Forme | Information integree dans les prix | Implication | Strategie concernee |
|---|---|---|---|
| **Faible (Weak)** | Prix et volumes historiques | L'analyse technique est inutile | Toutes les strategies basees sur les patterns de prix |
| **Semi-forte (Semi-Strong)** | Toute information publique (rapports, news, donnees macro) | L'analyse fondamentale ne genere pas d'alpha systematique | Stock picking, event-driven |
| **Forte (Strong)** | Toute information, y compris privee | Meme le delit d'initie ne genere pas d'alpha | Insider trading (theorique, car illegal) |

### Evidence empirique / Empirical Evidence

La forme semi-forte est largement supportee par les donnees empiriques pour les marches developpes et liquides :

- **SPIVA Scorecard** : sur 15 ans, plus de 85-90% des fonds actions US a gestion active sous-performent leur benchmark (S&P 500) apres frais. Les resultats sont similaires en Europe et dans les marches developpes.
- **Persistance de la performance** : la performance passee des fonds n'est pas un predicteur fiable de la performance future. Les top-quartile managers d'une periode de 5 ans ont une probabilite quasi aleatoire de rester top-quartile la periode suivante.
- **Anomalies documentees** : certaines anomalies (value premium, momentum, size effect) persistent meme apres publication, ce qui a conduit au developpement des modeles factoriels.

### Implications pratiques / Practical Implications

- **Marches efficients (large caps US, Europe, Japon)** : privilegier l'investissement indiciel passif low-cost. L'alpha net de frais est quasi nul en moyenne.
- **Marches moins efficients (small caps, EM, credit, private markets)** : la gestion active a plus de chances de generer de l'alpha, mais la selection du gestionnaire est critique.
- **Approche pragmatique** : adopter l'hypothese d'efficience comme position par defaut et n'y deroger que sur la base de preuves solides (facteurs documentes, avantages informationnels structurels).

### Behavioral Finance Challenges to EMH

Les travaux de Kahneman, Tversky, Thaler et Shiller documentent des biais systematiques :
- **Overreaction/Underreaction** : les investisseurs surreagissent aux nouvelles dramatiques et sous-reagissent aux tendances lentes. Cela alimente les anomalies de momentum et de mean reversion.
- **Loss Aversion** : la douleur d'une perte est environ 2x le plaisir d'un gain equivalent, conduisant a la disposition effect (vendre les gagnants trop tot, garder les perdants trop longtemps).
- **Herding** : le comportement gregaire amplifie les bulles et les crashes.
- **Overconfidence** : les investisseurs surestiment leur capacite a battre le marche, conduisant a un turnover excessif et des couts eleves.

---

## Fama-French Factor Models

### Three-Factor Model (1993)

Fama et French ont etendu le CAPM en ajoutant deux facteurs qui expliquent une part significative de la variation des rendements cross-sectionnels :

```
E(Ri) - Rf = beta_m * (Rm - Rf) + beta_s * SMB + beta_v * HML
```

| Facteur | Nom complet | Construction | Prime historique (annualisee) |
|---|---|---|---|
| **Market (MKT)** | Market Risk Premium | Rendement du marche - taux sans risque | ~5-7% |
| **SMB** | Small Minus Big | Rendement small caps - large caps | ~2-3% |
| **HML** | High Minus Low | Rendement value stocks (B/M eleve) - growth stocks | ~3-5% |

#### Size Effect (SMB)

Les actions de petite capitalisation tendent a surperformer les grandes capitalisations sur le long terme. Justification : prime de risque pour l'illiquidite, le risque de defaillance et le manque de couverture analytique. Cet effet s'est attenue depuis sa publication (1981 par Banz), notamment pour les micro-caps. Il reste plus prononce en dehors des USA et dans les marches emergents.

#### Value Effect (HML)

Les actions "value" (ratio book-to-market eleve, P/E faible, P/B faible) tendent a surperformer les actions "growth" sur le long terme. Debat sur l'origine : prime de risque rationnelle (entreprises en detresse financiere) vs biais comportemental (extrapolation excessive de la croissance passee). La value premium a connu une longue eclipse (2007-2020) avant un retour notable en 2021-2023, illustrant que les primes factorielles ne sont ni constantes ni garanties.

### Five-Factor Model (2015)

Fama et French ont ajoute deux facteurs additionnels pour mieux capturer les rendements cross-sectionnels :

```
E(Ri) - Rf = beta_m * (Rm - Rf) + beta_s * SMB + beta_v * HML + beta_r * RMW + beta_c * CMA
```

| Facteur | Nom complet | Construction | Interpretation |
|---|---|---|---|
| **RMW** | Robust Minus Weak | Rendement firms haute profitabilite - basse profitabilite | Qualite / Profitabilite |
| **CMA** | Conservative Minus Aggressive | Rendement firms investissement conservateur - agressif | Discipline d'investissement |

L'ajout de RMW et CMA reduit significativement le pouvoir explicatif de HML, suggerant que la value premium est partiellement capturee par la profitabilite et la discipline d'investissement.

### Momentum Factor (Carhart, 1997)

Le facteur momentum (UMD : Up Minus Down, ou WML : Winners Minus Losers) capture la tendance des titres ayant surperforme sur 2-12 mois a continuer de surperformer a court terme, et inversement :

```
MOM = Rendement des titres les plus performants (top decile, 2-12 mois) - Rendement des moins performants (bottom decile)
```

Prime historique : ~6-8% annualise, mais avec des crash risk severes (ex: momentum crash de 2009). Le momentum est le facteur avec la prime historique la plus elevee mais aussi la plus volatile. Implementer avec des stops ou des mecanismes de reduction d'exposition en regime de haute volatilite.

### Quality Factor

Le facteur qualite selectionne les entreprises avec des caracteristiques financieres solides : haute profitabilite (ROE eleve), faible endettement, stabilite des benefices, croissance constante. Partiellement capture par RMW dans le modele a 5 facteurs. Buffett's alpha est largement explique par une exposition aux facteurs quality et low-volatility avec levier.

### Low Volatility / Betting Against Beta (BAB)

Le facteur Low Volatility (Frazzini & Pedersen, 2014) exploite l'anomalie que les actions a faible beta tendent a offrir des rendements ajustes du risque superieurs aux actions a haut beta. Explication : les contraintes de levier poussent les investisseurs vers les actifs a haut beta, les survalorisant. Implementer via des strategies min-vol ou low-beta ETFs.

### Application pratique des facteurs / Practical Factor Implementation

Construire un portefeuille factor-based en utilisant les facteurs comme briques d'allocation :

| Approche | Implementation | Avantages | Risques |
|---|---|---|---|
| **Factor tilts** | Surponderer les facteurs dans un portefeuille indiciel large | Simple, faible tracking error | Exposition factorielle diluee |
| **Factor ETFs dedicates** | ETFs single-factor (iShares Edge, SPDR, Amundi) | Transparence, liquidite, faible cout | Timing des facteurs, turnover |
| **Multi-factor** | Combinaison de 3-5 facteurs dans un seul portefeuille | Diversification factorielle, reduction du drawdown | Complexite, definitions variables |
| **Factor rotation** | Allocation tactique entre facteurs selon le cycle | Potentiel de surperformance | Tres difficile a implementer, risque de timing |

### Factor Timing — Evidence

La rotation factorielle (factor timing) est extremement difficile a implementer avec succes. La recherche montre que :
- Les facteurs ont des cycles longs et imprevisibles (la value premium peut etre negative pendant 5-10 ans).
- Les strategies de timing multi-facteurs n'ont pas demontre d'alpha robuste out-of-sample.
- L'approche recommandee est de maintenir une exposition factorielle diversifiee et stable, avec un rebalancement periodique vers les poids cibles.
- Exception : reduire l'exposition momentum en regime de tres haute volatilite (VIX > 35) est supporte par la recherche.

---

## Risk-Return Optimization — Advanced Techniques

### Black-Litterman Model (1992)

Le modele Black-Litterman resout le probleme de sensibilite de l'optimisation Markowitz en combinant deux sources d'information :

1. **Prior (equilibre)** : les rendements implicites du CAPM (derived from market capitalization weights). Partir de l'allocation de capitalisation de marche comme point de depart.
2. **Views (vues de l'investisseur)** : ajuster les rendements attendus selon les convictions, avec un niveau de confiance associe a chaque vue.

Le resultat est un vecteur de rendements attendus combines qui produit des allocations stables et intuitives. Avantages : reduit la concentration, produit des portefeuilles proches de l'allocation de marche quand les vues sont faibles, et permet d'integrer des vues qualitatives de maniere quantitative.

### Resampled Efficient Frontier (Michaud, 1998)

Approche par simulation Monte Carlo :
1. Generer N ensembles de parametres (rendements, volatilites, correlations) par reechantillonnage.
2. Calculer la frontiere efficiente pour chaque ensemble.
3. Moyenner les allocations optimales a travers toutes les frontieres.

Le portefeuille resample est plus stable et mieux diversifie que le portefeuille Markowitz classique.

### Risk Budgeting

Allouer le risque plutot que le capital. Definir un budget de risque total (ex: 10% de volatilite annualisee) et le repartir entre les sources de risque :

```
Total Risk Budget = SUM(Risk Contribution_i)
Risk Contribution_i = wi * (partial sigma_p / partial wi) = wi * (Sigma * w)_i / sigma_p
```

L'approche risk budgeting est plus robuste que l'optimisation mean-variance car elle ne depend pas des estimations de rendements attendus.

### Hierarchical Risk Parity (HRP, Lopez de Prado, 2016)

Methode moderne qui utilise le clustering hierarchique et la theorie des graphes pour construire un portefeuille diversifie :

1. Calculer la matrice de distances basee sur les correlations.
2. Appliquer un clustering hierarchique (single-linkage) pour construire un dendrogramme.
3. Quasi-diagonaliser la matrice de covariance selon l'ordre du dendrogramme.
4. Allouer le risque de maniere recursive (bisection) en respectant la structure hierarchique.

Avantages vs Markowitz : pas d'inversion de matrice (plus stable numeriquement), robuste aux estimations bruitees, produit des portefeuilles mieux diversifies out-of-sample.

### Robust Optimization

Optimiser sous incertitude sur les parametres en definissant des ensembles d'incertitude (uncertainty sets) :

- **Worst-case optimization** : maximiser le rendement dans le pire scenario de l'ensemble d'incertitude. Conservateur mais robuste.
- **Distributionally robust optimization (DRO)** : optimiser sous un ensemble de distributions possibles des rendements, pas une distribution unique.
- **Regularization** : ajouter des penalites (L1 pour parcimonie, L2 pour stabilite) a la fonction objectif pour reduire la sensibilite.

---

## Practical Considerations

### Estimation des inputs / Input Estimation

| Parametre | Methode recommandee | Piege a eviter |
|---|---|---|
| **Rendements attendus** | Black-Litterman, primes de risque implicites, CMAs (Capital Market Assumptions) | Utiliser les rendements historiques bruts (backward-looking bias) |
| **Volatilites** | EWMA (Exponentially Weighted Moving Average), GARCH | Volatilite historique sur fenetre fixe (ignore les regimes) |
| **Correlations** | DCC-GARCH, correlations en regime de crise (stress correlations) | Correlations historiques stables (ignorent les regimes de crise) |
| **Taux sans risque** | T-Bills 3 mois, OAT court terme, SOFR/ESTER | Taux long terme (inclut la prime de terme) |

### Frequence de reoptimisation / Reoptimization Frequency

Reoptimiser l'allocation strategique annuellement ou lors de changements structurels (nouvelles classes d'actifs, changement de regime economique, evolution des objectifs). Ne pas reoptimiser tactiquement trop frequemment : les couts de transaction et l'instabilite des estimations dominent les gains potentiels.

### Implementation Shortcuts / Raccourcis d'implementation

Pour les portefeuilles de taille moderee (<500K EUR/USD), la complexite des approches avancees (Black-Litterman, HRP) n'est souvent pas justifiee. Utiliser les regles simples :
- **1/N (equal-weight)** : allouer 1/N a chaque classe d'actifs. DeMiguel et al. (2009) montrent que 1/N surperforme la plupart des strategies d'optimisation out-of-sample sur 14 datasets.
- **60/40** : 60% actions globales, 40% obligations. Benchmark classique, simple et historiquement performant.
- **Three-fund portfolio** : actions US (ou monde developpe) + actions internationales + obligations. Approche Bogle simplifiee.
- **Target-date funds** : fonds lifecycle qui ajustent automatiquement l'allocation selon l'horizon.
