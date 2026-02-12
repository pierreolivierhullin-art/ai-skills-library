# Investment Vehicles — ETFs, Index Investing, Options Overlay, Alternatives & Modern Instruments

## Overview

Ce document de reference couvre les vehicules d'investissement disponibles pour implementer une allocation de portefeuille : ETFs vs fonds communs, investissement indiciel (philosophie Bogle), strategies d'options overlay, investissements alternatifs (REITs, private equity, hedge funds), produits structures, fractional shares et investissement thematique. Utiliser ce guide pour selectionner les vehicules optimaux pour chaque composante du portefeuille.

This reference covers investment vehicles for portfolio implementation: ETFs vs mutual funds, index investing (Bogle philosophy), options overlay strategies, alternative investments (REITs, PE, hedge funds), structured products, fractional shares, and thematic investing. Use this guide to select optimal vehicles for each portfolio component.

---

## ETFs vs Mutual Funds (Fonds Communs)

### Exchange-Traded Funds (ETFs)

#### Structure et mecanique / Structure and Mechanics

Les ETFs sont des fonds negocies en bourse qui repliquent generalement un indice. Ils utilisent un mecanisme de creation/rachat en nature (in-kind creation/redemption) via des Authorized Participants (APs) qui maintient le prix de marche proche de la NAV.

**Replication physique** : detenir les titres composant l'indice (complete replication) ou un echantillon representatif (sampling/optimized replication). Methode preferee pour les indices liquides (S&P 500, MSCI World).

**Replication synthetique (swap-based)** : utiliser des contrats de swap avec une contrepartie pour repliquer le rendement de l'indice. Avantages : tracking error plus faible, acces a des marches difficiles (matieres premieres, marches frontieres). Risques : risque de contrepartie (limite a 10% de la NAV en UCITS), complexite, moindre transparence.

#### Avantages des ETFs / ETF Advantages

| Avantage | Detail |
|---|---|
| **Couts faibles** | TER de 0.03% a 0.50% pour les ETFs indiciels large cap. Leader : SPDR Portfolio S&P 500 (SPLG) a 0.02%, Vanguard FTSE All-World (VWCE) a 0.22% |
| **Liquidite intraday** | Negociables en continu pendant les heures de marche, possibilite d'ordres limites |
| **Transparence** | Composition publiee quotidiennement (daily holdings disclosure) |
| **Efficience fiscale** | Le mecanisme in-kind creation/redemption minimise les distributions de plus-values (specifique aux USA — pas applicable en Europe UCITS) |
| **Diversification instantanee** | Un seul ETF peut offrir une exposition a 3,000+ titres (MSCI ACWI) |
| **Flexibilite** | Large gamme : indices larges, sectoriels, factoriels, obligataires, matieres premieres, thematiques |

#### Criteres de selection d'un ETF / ETF Selection Criteria

Evaluer chaque ETF selon les criteres suivants :

| Critere | Metrique | Seuil recommande |
|---|---|---|
| **TER (Total Expense Ratio)** | Frais annuels en % | < 0.20% pour les indices larges, < 0.50% pour les niches |
| **Tracking Difference** | Ecart entre le rendement du fonds et celui de l'indice sur 1 an | < 0.10% pour les large caps, < 0.30% pour les EM/small caps |
| **AUM (Actifs sous gestion)** | Taille du fonds | > 100M EUR/USD (risque de fermeture si trop petit) |
| **Spread bid-ask** | Ecart entre prix d'achat et de vente | < 0.10% pour les ETFs liquides |
| **Methode de replication** | Physique vs synthetique | Physique preferee sauf cas specifiques |
| **Domiciliation** | Pays d'immatriculation (Irlande, Luxembourg pour UCITS) | Irlande pour l'optimisation de la retenue a la source US (15% vs 30%) |
| **Politique de distribution** | Distribution vs capitalisation (Acc vs Dist) | Capitalisation preferee pour la croissance et l'efficience fiscale (sauf besoin de revenus) |

### Mutual Funds (Fonds Communs / OPCVM)

#### Avantages specifiques / Specific Advantages

- **Investissement programme (DCA)** : pas de spread bid-ask, achat exact au montant souhaite (pas de nombre entier de parts). Ideal pour les plans d'epargne mensuels.
- **Certains indices exclusifs** : certains fonds offrent acces a des strategies non disponibles en ETF.
- **Plans d'epargne entreprise (PEE, PERCO)** : souvent uniquement disponibles en format fonds commun.

#### Inconvenients vs ETFs / Disadvantages vs ETFs

- Prix determine une fois par jour (NAV de cloture), pas de trading intraday
- Frais generalement plus eleves (meme pour les fonds indiciels)
- Moins transparents (composition trimestrielle, pas quotidienne)
- Droits d'entree/sortie possibles (surtout en Europe)

### Quand choisir quoi / When to Choose What

| Situation | Vehicule recommande | Raison |
|---|---|---|
| Investissement lump sum > 5,000 | ETF | Couts plus faibles, execution immediate |
| Investissement programme mensuel < 500 | Fonds indiciel | Pas de spread, montant exact |
| Compte taxable, recherche efficience fiscale | ETF (surtout aux USA) | In-kind creation/redemption |
| Plan d'epargne entreprise (PEE) | Fonds commun | Seul vehicule disponible |
| PEA (France) | ETF UCITS eligible PEA | Large choix, faibles couts |
| Exposition matieres premieres | ETF synthetique (ETC) | Replique les futures sans roulement manuel |

---

## Index Investing — La philosophie Bogle / The Bogle Philosophy

### Principes fondamentaux / Core Principles

John C. Bogle (fondateur de Vanguard, 1975) a etabli les principes de l'investissement indiciel :

1. **Le marche agrege est un jeu a somme nulle** : avant frais, le rendement moyen des investisseurs actifs egale le rendement du marche. Apres frais, il est inferieur. Donc la majorite des investisseurs actifs sous-performent l'indice.

2. **Les couts sont le meilleur predicteur de performance** : les fonds avec les frais les plus bas surperforment systematiquement ceux avec les frais les plus eleves sur le long terme. Correlation negative robuste entre TER et rendement net.

3. **La simplicite gagne** : un portefeuille de 3 fonds indiciels (actions US, actions internationales, obligations) suffit pour capturer la prime de risque de marche avec une diversification adequate.

4. **Stay the course** : la discipline d'investissement (rester investi, rebalancer systematiquement) est plus importante que la selection de titres ou le timing de marche.

### Evidence empirique / Empirical Evidence

Les donnees SPIVA (S&P Indices Versus Active) confirment systematiquement la these de Bogle :

| Categorie | % de fonds actifs sous-performant l'indice sur 15 ans | Indice de reference |
|---|---|---|
| Actions US Large Cap | 87-92% | S&P 500 |
| Actions US Mid Cap | 85-90% | S&P MidCap 400 |
| Actions US Small Cap | 80-88% | S&P SmallCap 600 |
| Actions Europe | 85-90% | S&P Europe 350 |
| Obligations US | 90-95% | Bloomberg US Aggregate |
| Actions EM | 75-85% | S&P/IFCI Composite |

La categorie des actions EM et des small caps montrent un taux de sous-performance legerement plus faible, suggerant que ces marches sont moins efficients et offrent plus d'opportunites pour la gestion active.

### Portefeuilles modeles indiciel / Model Index Portfolios

#### Three-Fund Portfolio (Bogle)
- 60% : Total US Stock Market Index (VTI / VTSAX)
- 30% : Total International Stock Market Index (VXUS / VTIAX)
- 10% : Total Bond Market Index (BND / VBTLX)

#### Four-Fund Portfolio (Global)
- 40% : US Total Market (VTI)
- 20% : International Developed (VEA)
- 10% : Emerging Markets (VWO)
- 30% : Total Bond Market (BND)

#### European Equivalent (UCITS, PEA-compatible)
- 50% : MSCI World ETF (CW8 / IWDA)
- 10% : MSCI Emerging Markets ETF (PAEEM / EIMI)
- 30% : Euro Government Bond ETF (VGEA / AGGH EUR-hedged)
- 10% : Euro Inflation-Linked Bond ETF

#### Single-Fund Solutions
- Vanguard LifeStrategy (UK/EU) : allocation automatique actions/obligations selon profil
- iShares Target Date Funds : allocation lifecycle automatique
- Vanguard Target Retirement Funds (USA) : glide path automatique

### Smart Beta / Factor-Enhanced Indexing

Le smart beta (ou strategic beta) utilise des regles systematiques non basees sur la capitalisation pour construire des indices alternatifs :

| Strategie | Construction | Prime ciblee | Exemples ETFs |
|---|---|---|---|
| **Equal Weight** | Meme poids pour chaque composant | Anti-concentration, small cap tilt | RSP (Invesco S&P 500 Equal Weight) |
| **Minimum Variance** | Minimiser la volatilite du portefeuille | Low volatility anomaly | USMV (iShares MSCI USA Min Vol) |
| **Fundamental Index** | Ponderation par metriques fondamentales (revenus, dividendes, book value) | Value tilt | PRF (Invesco FTSE RAFI US 1000) |
| **Quality** | Filtrer par ROE, stabilite, faible endettement | Quality premium | QUAL (iShares MSCI USA Quality) |
| **Momentum** | Surponderer les titres avec momentum positif sur 6-12 mois | Momentum premium | MTUM (iShares MSCI USA Momentum) |
| **Multi-Factor** | Combiner 3-5 facteurs dans un seul indice | Diversification factorielle | GSLC (Goldman Sachs ActiveBeta) |

---

## Options Overlay Strategies

### Principes / Principles

Les strategies d'options overlay utilisent des options sur les positions existantes du portefeuille pour modifier le profil de rendement/risque. Elles ne sont pas des strategies autonomes mais des surcouches (overlay) sur l'allocation sous-jacente.

Options overlay strategies use options on existing portfolio positions to modify the return/risk profile. They are not standalone strategies but overlays on the underlying allocation.

### Covered Call Writing (Vente de calls couverts)

Vendre des options d'achat (calls) sur les positions actions du portefeuille pour generer un revenu additionnel (prime d'option) en echange d'un plafonnement du potentiel de hausse.

**Mecanique** :
- Detenir 100 actions de l'actif sous-jacent (ou equivalent en ETF)
- Vendre 1 call OTM (Out of The Money, strike 3-7% au-dessus du prix actuel)
- Echeance : 30-45 jours (decroissance theta optimale)
- Renouveler (roll) a l'expiration ou avant si le call est ITM

**Profil de rendement** :
- Rendement additionnel : 3-8% annualise selon la volatilite et le delta choisi
- Plafond de gain : le gain maximal est le strike - prix actuel + prime recue
- Pas de protection baissiere (la prime recue amortit faiblement les pertes)

**ETFs BuyWrite / Covered Call** : XYLD (S&P 500 BuyWrite), QYLD (Nasdaq 100 BuyWrite), JEPI (JPMorgan Equity Premium Income). Ces ETFs implementent automatiquement la strategie.

### Protective Put (Put protecteur)

Acheter des options de vente (puts) sur les positions actions pour creer un plancher de perte (floor).

**Mecanique** :
- Detenir les actions sous-jacentes
- Acheter des puts OTM (strike 5-10% en dessous du prix actuel)
- Echeance : 3-6 mois (compromis cout/protection)

**Cout** : 2-5% annualise (le "cout de l'assurance"). Ce drag sur la performance rend la strategie couteuse en permanence. Utiliser tactiquement, pas structurellement.

### Collar (Tunnel)

Combiner un covered call et un protective put pour creer une fourchette de rendement borned.

**Mecanique** :
- Detenir les actions sous-jacentes
- Acheter un put OTM (strike -5% a -10%)
- Vendre un call OTM (strike +5% a +10%)
- Le premium du call finance partiellement ou totalement le put (zero-cost collar si les strikes sont calibres)

**Usage** : protection a cout reduit (voire nul) pour les positions concentrees que l'investisseur ne peut pas vendre (restrictions, raisons fiscales, lock-up).

### Put Spread Hedge (Bear Put Spread)

Acheter un put a un strike proche (ATM ou legerement OTM) et vendre un put a un strike plus bas (deep OTM) pour reduire le cout de la couverture.

**Usage** : protection partielle contre les drawdowns moderees (-5% a -20%) a cout reduit vs un put simple. Ne protege pas contre les crashes extremes (la protection s'arrete au strike du put vendu).

### Tail Risk Hedging

Allouer 1-3% du portefeuille a des couvertures contre les evenements extremes :
- **Deep OTM puts** (strike -20% a -30%, echeance 6-12 mois) : protection contre les crashes, tres couteux en carry
- **VIX calls** : beneficient de la convexite du VIX en crise. Risque : le VIX futures est en contango permanent, donc les calls perdent de la valeur en marche calme
- **CDS indices (CDX, iTraxx)** : protection contre le risque de credit systematique
- **Managed futures / CTA funds** : strategies trend-following qui tendent a profiter des dislocations majeures. Correlation historiquement negative avec les actions en crise

---

## Alternative Investments (Investissements Alternatifs)

### REITs (Real Estate Investment Trusts)

#### Structure et caracteristiques / Structure and Characteristics

Les REITs sont des societes foncieres cotees qui detiennent et gerent des biens immobiliers generant des revenus. Ils doivent distribuer au minimum 90% de leur revenu imposable sous forme de dividendes (aux USA ; regles similaires pour les SIIC en France).

| Type de REIT | Sous-jacent | Rendement dividende | Sensibilite |
|---|---|---|---|
| **Residential** | Immobilier residentiel, multifamily | 2-4% | Demographie, emploi local |
| **Office** | Bureaux | 4-7% | Teletravail, cycle economique |
| **Retail** | Centres commerciaux, retail parks | 4-8% | E-commerce, consommation |
| **Industrial/Logistics** | Entrepots, logistique | 2-4% | E-commerce (beneficiaire), supply chain |
| **Healthcare** | Hopitaux, EHPAD, laboratoires | 4-6% | Vieillissement demographique |
| **Data Centers** | Centres de donnees | 2-3% | Cloud computing, IA |
| **Infrastructure** | Tours telecom, fiber, renewables | 2-4% | 5G, transition energetique |
| **Specialty** | Self-storage, timberland, farmland | 3-5% | Niche, faible correlation |

#### Role dans le portefeuille / Portfolio Role
- Rendement : dividendes superieurs aux actions (3-5% vs 1.5-2%)
- Inflation hedge partiel : les baux sont indexes sur l'inflation (avec delai)
- Diversification : correlation intermediaire avec les actions (~0.6-0.7) et faible avec les obligations (~0.1-0.3)
- Poids recommande : 5-15% de l'allocation totale

### Private Equity (Capital Investissement)

#### Strategies principales / Main Strategies

| Strategie | Phase entreprise | Rendement cible (net) | Horizon | Risque |
|---|---|---|---|---|
| **Venture Capital** | Early-stage, growth | 15-25% IRR | 7-12 ans | Tres eleve (majorite des investissements echouent) |
| **Growth Equity** | Expansion | 12-20% IRR | 5-7 ans | Eleve |
| **Buyout / LBO** | Mature, restructuration | 10-18% IRR | 4-7 ans | Modere-eleve |
| **Distressed / Special Situations** | Crise, restructuration | 12-20% IRR | 3-5 ans | Eleve |
| **Secondaries** | Rachat de parts existantes | 10-15% IRR | 3-5 ans | Modere (J-curve reduit) |

#### Acces pour les investisseurs individuels / Retail Access

Historiquement reserve aux institutionnels (minimum 250K-1M par fonds), le PE s'ouvre progressivement :
- **Listed PE** : societes de PE cotees (Blackstone, KKR, Apollo, EQT). Correlation elevee avec les marches actions.
- **PE ETFs** : PSP (Invesco Global Listed PE), IPRV (iShares Listed PE). Liquidite quotidienne mais ne repliquent pas les vrais rendements PE (absence de prime d'illiquidite).
- **Feeder funds / ELTIF** : fonds semi-ouverts offrant acces a des strategies PE/VC avec des minimums reduits (10K-50K EUR). Cadre ELTIF 2.0 en Europe depuis 2024.
- **Plateformes de co-investissement** : Moonfare, iCapital, AngelList. Minimums 50K-100K.

### Hedge Funds (Fonds Alternatifs)

#### Strategies principales / Main Strategies

| Strategie | Description | Rendement cible | Volatilite | Correlation marche |
|---|---|---|---|---|
| **Long/Short Equity** | Positions longues et courtes en actions | 6-10% | 8-12% | 0.5-0.7 |
| **Market Neutral** | Beta de marche proche de zero | 3-6% | 3-6% | ~0 |
| **Global Macro** | Paris directionnels sur devises, taux, matieres premieres | 5-10% | 8-15% | Variable |
| **Event-Driven (Merger Arb)** | Exploitation des spreads de M&A, restructurations | 4-8% | 4-8% | 0.3-0.5 |
| **Systematic CTA / Managed Futures** | Trend-following systematique sur futures | 3-8% | 10-15% | Negative en crise (~-0.3) |
| **Relative Value / Fixed Income Arb** | Arbitrage de spreads obligataires | 3-6% | 3-6% | Faible |
| **Multi-Strategy** | Combinaison de plusieurs strategies | 5-8% | 5-8% | 0.2-0.4 |

#### Frais et structure / Fees and Structure

Structure classique : 2% management fee + 20% performance fee (2/20). Tendance a la compression : 1.5/15 ou 1/10 pour les grands allocataires. High-water mark : la performance fee ne s'applique que sur les rendements depassant le pic precedent.

**Impact des frais** : un hedge fund brut a 8% avec 2/20 delivre ~4.8% net [(8% - 2%) * 0.8 = 4.8%]. Justifier que cet alpha net depasse un portefeuille passif faiblement correle.

#### Liquid Alternatives (UCITS Alternatives)

Fonds alternatifs au format UCITS offrant liquidite quotidienne et transparence reglementaire. Compromis : les contraintes UCITS (levier limite, liquidite, diversification) limitent l'univers de strategies et reduisent le potentiel de rendement par rapport aux hedge funds "full".

### Structured Products (Produits Structures)

#### Types principaux / Main Types

| Produit | Mecanique | Rendement | Risque | Usage |
|---|---|---|---|---|
| **Capital Protected Notes** | Zero-coupon bond + call option | Participe a la hausse avec protection du capital (partielle ou totale) | Risque emetteur (credit), cout d'opportunite | Investisseur averse au risque voulant participation actions |
| **Autocallable** | Remboursement anticipe si le sous-jacent > barrier | Coupon fixe (6-10%) si conditions remplies | Barriere de protection (si sous-jacent < -30/40%, perte en capital) | Recherche de rendement en marche range-bound |
| **Reverse Convertible** | Bond + short put | Coupon eleve (8-15%) | Risque de perte si sous-jacent < strike du put | Income en echange de risque de downside |
| **Participation Notes** | Exposition leveraged a un indice | Amplifie les gains et les pertes | Levier, risque emetteur | Vue directionnelle avec levier |

#### Avertissements / Warnings

- Les produits structures ont des frais implicites significatifs (2-5% embedded dans le prix d'emission) rarement transparents
- Le risque emetteur (credit de la banque emettrice) est souvent sous-estime
- La liquidite secondaire est generalement faible (spread large, pas de market maker)
- Les conditions de remboursement sont complexes et souvent defavorables dans les scenarios de stress
- Regle generale : si le mecanisme ne peut pas etre explique en 2 minutes, ne pas investir

---

## Fractional Shares (Actions Fractionnees)

### Principes / Principles

Les fractional shares permettent d'acheter une fraction d'action ou d'ETF plutot qu'une part entiere. Cela democratise l'acces a des titres a prix unitaire eleve (Berkshire Hathaway, Amazon, LVMH) et permet une diversification precise meme avec de petits montants.

### Plateformes proposant le fractional investing / Platforms

| Plateforme | Region | Fractional shares | Commentaire |
|---|---|---|---|
| **Interactive Brokers** | Global | Oui (actions US et ETFs) | Broker institutionnel, frais tres faibles |
| **Trade Republic** | Europe | Oui (plans d'epargne) | Plans d'epargne automatiques, gratuit |
| **Scalable Capital** | Europe | Oui (via ETF savings plans) | Plateforme de gestion d'investissement |
| **Fidelity** | USA | Oui (Fidelity Stocks by the Slice) | Grand broker traditionnel |
| **Charles Schwab** | USA | Oui (Schwab Stock Slices) | S&P 500 components |
| **Revolut / eToro** | Global | Oui | Neobrokers, verifier la structure de propriete (nominee vs direct) |

### Usage optimal / Optimal Usage

- **DCA sur titres chers** : investir 100 EUR/mois dans un ETF a 400 EUR/part avec precision
- **Direct indexing a petite echelle** : repliquer un indice titre par titre avec des montants modestes
- **Rebalancement precis** : ajuster les poids au pourcentage pres sans contrainte de lot minimum
- **Attention** : verifier la structure de propriete (certains courtiers detiennent les fractional shares en nominee, pas en propriete directe)

---

## Thematic Investing (Investissement Thematique)

### Definition et approche / Definition and Approach

L'investissement thematique cible des tendances structurelles de long terme (megatrends) plutot que des secteurs ou geographies traditionnels. Les themes traversent les secteurs classiques (ex: la cybersecurite inclut tech, defense, finance).

### Themes principaux et ETFs / Major Themes and ETFs

| Theme | Tendance sous-jacente | Exemples ETFs | Risque specifique |
|---|---|---|---|
| **Intelligence Artificielle / AI** | Adoption IA generative, automatisation | BOTZ, AIQ, WTAI | Concentration sur quelques mega-caps, valorisations elevees |
| **Cybersecurite** | Croissance des menaces cyber, reglementation | HACK, BUG, CIBR | Dependance aux budgets IT corporate |
| **Energie propre / Clean Energy** | Transition energetique, reglementation climat | ICLN, QCLN, TAN | Risque reglementaire, competition chinoise |
| **Vieillissement demographique** | Augmentation de l'esperance de vie | AGED, HEAL | Risque reglementaire sante |
| **Economie spatiale / Space** | Commercialisation de l'espace, satellites | UFO, ARKX | Speculative, peu de revenus |
| **Blockchain / Digital Assets** | Adoption crypto, tokenization | BLOK, BKCH | Haute volatilite, risque reglementaire |
| **Eau / Water** | Rarefaction des ressources en eau | PHO, CGW, FIW | Faible croissance, defensive |
| **Robotique et automatisation** | Automation industrielle, Industry 4.0 | ROBO, IRBO | Cyclique, sensible au capex industriel |

### Regles d'integration thematique dans le portefeuille / Thematic Integration Rules

1. **Limiter l'allocation thematique a 5-15% du portefeuille total** (satellite, jamais core).
2. **Diversifier entre 2-4 themes non correles** pour eviter la concentration.
3. **Verifier la construction de l'indice** : certains ETFs thematiques ont une concentration excessive (top 10 holdings > 50% du fonds) ou incluent des societes tangentiellement liees au theme.
4. **Evaluer les frais** : les ETFs thematiques sont generalement plus chers (TER 0.40-0.75%) que les ETFs indiciels larges. Justifier le surcout par une these d'investissement solide.
5. **Horizon long** : les themes structurels se deployent sur 5-15 ans. Ne pas investir thematiquement avec un horizon < 5 ans.
6. **Eviter le hype cycle** : les themes recents (IA, espace) sont souvent deja prices in. Preferer les themes matures avec des fondamentaux solides (eau, cybersecurite, vieillissement) aux themes speculatifs.

---

## Cryptocurrencies & Digital Assets in Portfolio Context

### Role dans le portefeuille / Portfolio Role

Les crypto-actifs (Bitcoin, Ethereum principalement) sont consideres comme une classe d'actifs emergente avec des caracteristiques specifiques :

| Caracteristique | Detail |
|---|---|
| **Volatilite** | 60-80% annualisee (vs 15-20% pour les actions) |
| **Correlation** | Variable : faible en 2019-2020, elevee en 2022 (correlation avec tech/risk-on), redevenue moderee |
| **Rendement historique** | Exceptionnellement eleve (mais sur une courte historique, survivorship bias massif) |
| **Regulatory risk** | Elevee : cadre reglementaire en evolution (MiCA en Europe, SEC aux USA) |
| **Custody risk** | Risque specifique lie a la conservation (hacks, fraude d'exchange — FTX) |

### Allocation recommandee / Recommended Allocation

- **Sceptique/Conservateur** : 0% (pas de track record suffisant, volatilite excessive)
- **Pragmatique** : 1-3% du portefeuille total via des vehicules regules (Bitcoin/Ethereum spot ETFs : IBIT, FBTC, ETHA). Impact limite en cas de perte totale (-1 a -3% du portefeuille), contribution positive en cas de hausse
- **Convaincu** : 3-5% maximum, diversifie entre Bitcoin (store of value thesis) et Ethereum (smart contract platform thesis). Rebalancer strictement via les bandes

### Vehicules d'acces / Access Vehicles

- **Spot ETFs (USA)** : IBIT (BlackRock), FBTC (Fidelity), GBTC (Grayscale) pour Bitcoin. Approuves par la SEC en janvier 2024.
- **Spot ETFs (Europe)** : ETPs Bitcoin/Ethereum disponibles sur les bourses europeennes (21Shares, CoinShares, VanEck).
- **Crypto-tracking ETFs** : fonds investissant dans des societes liees a la crypto (mining, exchanges, infrastructure). Correlation elevee mais sans exposition directe.
- **Detenir directement** : via des exchanges regules (Coinbase, Kraken, Bitstamp) avec cold storage. Plus complexe mais pas de frais de gestion.

---

## Commodities (Matieres Premieres)

### Role dans le portefeuille / Portfolio Role

Les matieres premieres offrent une diversification unique car elles sont drivees par des fondamentaux d'offre/demande physiques plutot que par les earnings d'entreprises. Elles constituent une couverture contre l'inflation et les chocs d'offre.

### Vehicules d'exposition / Exposure Vehicles

| Vehicule | Mecanique | Avantages | Inconvenients |
|---|---|---|---|
| **Commodity ETFs (futures-based)** | Roulement de contrats futures | Liquidite, diversification | Roll yield negatif (contango), tracking error |
| **Physical Gold ETFs** | Adosse a de l'or physique | Couverture pure, pas de roll | Frais de stockage/assurance (TER 0.12-0.25%) |
| **Commodity producers equities** | Actions de societes minieres, petrolieres | Dividendes, leverage operationnel | Correlation avec actions, risque corporate |
| **Agricultural / Energy ETFs** | Futures sur matieres premieres specifiques | Exposition ciblee | Contango severe sur certaines matieres premieres |

### Allocation recommandee / Recommended Allocation

- Or : 3-10% du portefeuille (couverture geopolitique, deflation, perte de confiance monetaire)
- Broad commodities : 0-5% (diversification inflation, mais drag en marche normal a cause du contango)
- Ne pas surponderer les matieres premieres : rendement reel de long terme proche de zero (elles ne generent ni dividendes, ni coupons, ni croissance des benefices)
