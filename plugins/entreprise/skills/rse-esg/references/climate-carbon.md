# Climate & Carbon -- GHG Protocol, Bilan Carbone, SBTi, Net Zero, Carbon Markets, LCA

Reference complete sur la comptabilite carbone, les strategies climat, les trajectoires Net Zero, les marches carbone et l'analyse du cycle de vie. Ce document couvre les methodologies de reference (GHG Protocol, Bilan Carbone ADEME), la definition d'objectifs science-based (SBTi), les mecanismes de compensation et contribution carbone, et l'ACV. Utiliser ce document comme guide operationnel pour tout projet de strategie climat et de decarbonation.

---

## Comptabilite GES — GHG Protocol

### Architecture du GHG Protocol

Le GHG Protocol (Greenhouse Gas Protocol) est le standard international de reference pour la comptabilite des emissions de gaz a effet de serre. Developpe par le WRI (World Resources Institute) et le WBCSD (World Business Council for Sustainable Development), il comprend plusieurs guides :

- **Corporate Accounting and Reporting Standard** (revised edition) : standard principal pour la comptabilite GES au niveau de l'entreprise
- **Corporate Value Chain (Scope 3) Standard** : guide detaille pour la comptabilite du scope 3
- **GHG Protocol Land Sector and Removals Guidance** (2022) : guide pour la comptabilite des absorptions et du secteur des terres

### Les trois scopes d'emissions

#### Scope 1 — Emissions directes

Emissions de GES provenant de sources detenues ou controlees par l'entreprise :

- **Combustion fixe** : chaudieres, fours, turbines, generateurs alimentes par des combustibles fossiles (gaz naturel, fioul, charbon). Calcul : consommation de combustible (en kWh PCI ou en litres/tonnes) x facteur d'emission du combustible.
- **Combustion mobile** : vehicules detenus ou controles par l'entreprise (flotte automobile, camions, engins). Calcul : litres de carburant consommes x facteur d'emission du carburant, ou km parcourus x facteur d'emission par km selon le type de vehicule.
- **Emissions de procede** : emissions liees aux procedes industriels (cimenterie : calcination du calcaire ; chimie : reactions chimiques ; metallurgie : reduction des minerais). Calcul specifique par procede.
- **Emissions fugitives** : fuites de gaz refrigerants (climatisation, froid commercial/industriel), fuites de gaz naturel, emissions de SF6 (equipements electriques). Calcul : quantite de gaz recharge x potentiel de rechauffement global (PRG/GWP) du gaz.

#### Scope 2 — Emissions indirectes liees a l'energie

Emissions liees a la production de l'electricite, de la chaleur, de la vapeur ou du refroidissement achetes et consommes par l'entreprise :

**Methode location-based** : Applique le facteur d'emission moyen du reseau electrique de la zone geographique ou l'electricite est consommee. Reflete la realite physique du mix electrique local. Utiliser les facteurs d'emission par pays publies par l'IEA, l'ADEME (Base Carbone), ou les operateurs de reseau nationaux.

**Methode market-based** : Utilise le facteur d'emission specifique au fournisseur d'electricite ou au contrat d'achat. Reflete les choix contractuels de l'entreprise (achat d'electricite verte, PPA — Power Purchase Agreement). Utiliser les garanties d'origine (GO), les PPA, les certificats d'energie renouvelable (RECs), ou a defaut le residual mix du pays.

Le GHG Protocol exige la publication des deux methodes. Le scope 2 market-based peut etre nul si l'entreprise achete 100% d'electricite renouvelable avec des GO correspondantes. Le scope 2 location-based reste inchange car il reflete le mix physique.

#### Scope 3 — Autres emissions indirectes

Le scope 3 couvre l'ensemble des emissions indirectes de la chaine de valeur, en amont et en aval. Il represente typiquement 70-90% des emissions totales d'une entreprise. Le GHG Protocol definit 15 categories :

**Amont (Upstream)** :
1. Achats de biens et services : emissions liees a la production des biens et services achetes. Methode preferee : donnees specifiques fournisseurs (supplier-specific). A defaut : methodes hybrides (facteurs d'emission par categorie de produit) ou methode monetaire (spend-based : EUR depenses x facteur d'emission par EUR).
2. Biens d'equipement (capital goods) : emissions liees a la fabrication des biens d'equipement acquis (machines, batiments, vehicules, IT).
3. Combustibles et energie (non inclus dans les scopes 1 et 2) : emissions amont de la production et du transport des combustibles et de l'electricite consommes (extraction, raffinage, transport, pertes en ligne).
4. Transport et distribution amont : emissions liees au transport des intrants vers les sites de l'entreprise par des prestataires tiers.
5. Dechets generes par les operations : emissions liees au traitement et a l'elimination des dechets generes par l'entreprise (mise en decharge, incineration, recyclage).
6. Deplacements professionnels : emissions liees aux voyages d'affaires des salaries (avion, train, taxi, hotel).
7. Trajets domicile-travail : emissions liees aux deplacements quotidiens des salaries.
8. Actifs loues en amont : emissions liees aux actifs loues par l'entreprise (batiments, vehicules) non inclus dans les scopes 1 et 2.

**Aval (Downstream)** :
9. Transport et distribution aval : emissions liees au transport des produits vers les clients par des prestataires tiers.
10. Transformation des produits vendus : emissions liees a la transformation des produits intermediaires vendus par l'entreprise.
11. Utilisation des produits vendus : emissions liees a l'utilisation des produits par les clients (consommation d'energie, emission de gaz). Categorie majeure pour les secteurs automobile, electronique, energie.
12. Fin de vie des produits vendus : emissions liees au traitement en fin de vie des produits vendus (mise en decharge, recyclage, incineration).
13. Actifs loues en aval : emissions liees aux actifs detenus par l'entreprise et loues a des tiers.
14. Franchises : emissions des franchises.
15. Investissements : emissions liees aux investissements financiers de l'entreprise (applicable aux institutions financieres, methodologie PCAF).

### Bilan Carbone (methode ADEME)

Le Bilan Carbone est la methode francaise de reference, developpee par l'ADEME (Agence de la Transition Ecologique) et geree par l'Association Bilan Carbone (ABC). Elle est compatible avec le GHG Protocol mais presente des specificites :

**Differences avec le GHG Protocol** :
- Le Bilan Carbone couvre les 6 GES du Protocole de Kyoto (CO2, CH4, N2O, HFC, PFC, SF6) plus le NF3
- La categorisation des postes d'emission est differente (regroupement par thematique : energie, intrants, fret, deplacements, dechets, immobilisations, utilisation, fin de vie)
- Les facteurs d'emission de reference sont ceux de la Base Carbone ADEME (base francaise, europeenne et internationale)
- Le Bilan Carbone est obligatoire en France pour les entreprises de plus de 500 salaries (250 en outre-mer) et les collectivites de plus de 50 000 habitants (article L229-25 du Code de l'environnement)

**Base Carbone ADEME** : Base de donnees publique de facteurs d'emission geres par l'ADEME. Couvre plus de 3 000 facteurs d'emission pour la France et l'international. Mise a jour reguliere. Accessible gratuitement. Utiliser en priorite les facteurs Base Carbone pour les operations en France.

### Facteurs de conversion et unites

Toutes les emissions sont exprimees en tonnes de CO2 equivalent (tCO2e), en utilisant les potentiels de rechauffement global (PRG/GWP) du GIEC/IPCC :

| Gaz | Formule | PRG 100 ans (AR6) |
|---|---|---|
| CO2 | Dioxyde de carbone | 1 |
| CH4 | Methane | 27.9 (fossile : 29.8) |
| N2O | Protoxyde d'azote | 273 |
| HFC | Hydrofluorocarbures | 4 a 14 800 selon le gaz |
| PFC | Perfluorocarbures | 6 500 a 11 100 |
| SF6 | Hexafluorure de soufre | 25 200 |
| NF3 | Trifluorure d'azote | 17 400 |

Utiliser les PRG du dernier rapport du GIEC (AR6, 2021) sauf exigence reglementaire specifique imposant les PRG d'un rapport anterieur.

---

## SBTi — Science Based Targets initiative

### Presentation et principes

Le SBTi (Science Based Targets initiative) est un partenariat entre le CDP, le UN Global Compact, le WRI et le WWF qui permet aux entreprises de definir des objectifs de reduction des emissions de GES alignes sur la science climatique (accords de Paris : limiter le rechauffement a 1.5 degre C ou bien en dessous de 2 degres C).

### Near-term targets (objectifs a court terme)

**Definition** : Objectifs de reduction a horizon 5-10 ans a partir de l'annee de base. Doivent couvrir les scopes 1, 2 et, si le scope 3 represente plus de 40% des emissions totales, le scope 3 (au moins 2/3 des emissions scope 3 en termes de couverture des categories).

**Criteres de validation SBTi** :
- Scopes 1+2 : reduction minimale de 4.2% par an en valeur absolue (trajectoire 1.5 degre C) ou via une methode sectorielle (SDA — Sectoral Decarbonization Approach) quand disponible
- Scope 3 : reduction minimale de 2.5% par an (trajectoire well-below 2 degre C) en couvrant au moins 67% des emissions scope 3
- Annee de base : maximum 5 ans avant la date de soumission (recalculs autorises)
- Horizon cible : entre 5 et 10 ans a partir de l'annee de soumission
- Pas d'utilisation de credits carbone pour atteindre les objectifs near-term

**Processus d'engagement** :
1. Lettre d'engagement (commitment letter) : engagement public a definir un objectif SBTi dans les 24 mois
2. Definition de l'objectif : calcul de la trajectoire avec les outils SBTi (Target Validation Protocol)
3. Soumission : dossier de validation au SBTi (formulaire, donnees d'emission, calcul de trajectoire)
4. Validation : revue par le SBTi (delai de 2-6 mois selon la file d'attente). Validation publique.
5. Communication annuelle : reporting annuel des emissions et des progres vers l'objectif

### Net Zero Standard (objectifs long terme)

**Definition** : Le SBTi Corporate Net-Zero Standard (publie en octobre 2021, revise en 2024) definit les exigences pour atteindre le net zero :

**Structure de l'engagement Net Zero** :
- **Near-term target** (obligatoire) : reduction de 50% minimum des emissions scopes 1+2+3 d'ici 2030 (trajectoire 1.5 degre C)
- **Long-term target** (obligatoire) : reduction de 90% minimum des emissions scopes 1+2+3 avant 2050
- **Neutralisation des emissions residuelles** (obligatoire) : les 10% residuels doivent etre neutralises par des removals permanents (capture et stockage du carbone, reforestation, etc.)
- **Beyond value chain mitigation** (recommande) : investissements dans des projets de reduction ou de retrait de GES hors de la chaine de valeur (contribution climatique)

**Points d'attention critiques** :
- Le net zero n'est PAS la carbon neutrality. La carbon neutrality permet de compenser 100% des emissions par des credits carbone. Le net zero SBTi exige d'abord de reduire 90% des emissions, puis de neutraliser les 10% residuels par des removals.
- Les credits de compensation (avoidance credits) ne peuvent PAS etre utilises pour atteindre les objectifs SBTi.
- Le SBTi encourage les actions de beyond value chain mitigation (BVCM) en complement de la reduction, mais elles ne comptent pas dans l'atteinte de l'objectif.

### Methodologies sectorielles SBTi

Le SBTi developpe des methodologies specifiques pour les secteurs les plus emetteurs :

| Secteur | Methodologie | Specificite |
|---|---|---|
| **Power** | SDA + absolute contraction | Intensite carbone par kWh |
| **Transport** | SDA | Intensite carbone par tkm ou pkm |
| **Buildings** | SDA | Intensite carbone par m2 |
| **Cement** | SDA | Intensite carbone par tonne de ciment |
| **Steel** | SDA | Intensite carbone par tonne d'acier |
| **Forest, Land & Agriculture (FLAG)** | FLAG Guidance | Emissions et absorptions du secteur terres |
| **Financial Institutions** | FI Guidance | Emissions financees (PCAF) |
| **Oil & Gas** | En preparation | Scope 3 categorie 11 critique |

---

## Marches Carbone — Compensation et Contribution

### Marche reglemente du carbone (ETS)

**EU ETS (European Union Emissions Trading System)** : Le plus grand marche carbone reglemente au monde. Mecanisme de cap and trade : un plafond d'emissions decroissant est fixe, et les entreprises soumises doivent detenir des quotas (EUAs — EU Allowances) correspondant a leurs emissions.

**Perimetre actuel** :
- Secteurs couverts : production d'electricite, industrie lourde (ciment, acier, chimie, raffinage, verre, papier), aviation intra-EEE
- EU ETS 2 (a partir de 2027) : extension au transport routier et aux batiments (chauffage)
- CBAM (Carbon Border Adjustment Mechanism) : taxe carbone aux frontieres applicable progressivement (phase transitoire 2023-2025, pleine application 2026) pour les importations de ciment, fer/acier, aluminium, engrais, electricite, hydrogene

**Prix du carbone EU ETS** : Le prix du quota EU ETS a fluctue entre 50 et 100 EUR/tCO2e sur la periode 2023-2025. La tendance structurelle est haussiere en raison de la reduction du plafond et de la reserve de stabilite de marche (MSR).

**Prix interne du carbone** : Independamment de l'EU ETS, de nombreuses entreprises utilisent un prix interne du carbone (internal carbon price) pour guider les decisions d'investissement. Fourchettes observees : 50-150 EUR/tCO2e pour les decisions courantes, 100-300 EUR/tCO2e pour les investissements long terme. L'ESRS E1 exige la disclosure du prix interne du carbone utilise.

### Marche volontaire du carbone

**Principes** : Le marche volontaire permet aux entreprises et individus d'acheter des credits carbone pour financer des projets de reduction ou de retrait des GES hors de leur chaine de valeur. Un credit carbone = 1 tCO2e evitee ou retiree.

**Types de credits** :
- **Avoidance credits (credits d'evitement)** : emissions evitees par rapport a un scenario de reference (ex : projet d'energies renouvelables evitant une centrale a charbon, protection de forets evitant la deforestation — REDD+)
- **Removal credits (credits de retrait)** : CO2 effectivement retire de l'atmosphere (ex : reforestation/afforestation, biochar, direct air capture and storage — DACS, enhanced weathering)

**Standards de certification** :
| Standard | Type | Rigueur | Couverture |
|---|---|---|---|
| **Verra (VCS)** | Multi-type | Moyenne-elevee | Le plus utilise mondialement (1 milliard+ credits emis) |
| **Gold Standard** | Multi-type + co-benefices | Elevee | Focus co-benefices ODD |
| **ACR (American Carbon Registry)** | Multi-type | Elevee | Ameriques |
| **CAR (Climate Action Reserve)** | Multi-type | Elevee | Amerique du Nord |
| **Puro.earth** | Removals uniquement | Elevee | Biochar, CCU, mineralization |
| **ICVCM (Integrity Council for VCM)** | Meta-standard (CCP label) | Tres elevee | Label qualite transversal |

**Core Carbon Principles (CCP) — ICVCM** : L'ICVCM a publie en 2023 les Core Carbon Principles, un cadre de qualite pour les credits carbone volontaires. Les credits labellises CCP doivent satisfaire des criteres stricts : additionnalite demontree, baseline conservative, permanence, robustesse de la quantification, co-benefices, absence de double comptage. Le label CCP est progressivement adopte comme reference qualite par les acheteurs corporate.

**VCMI (Voluntary Carbon Markets Integrity Initiative)** : Le VCMI a publie le Claims Code of Practice, qui definit comment les entreprises peuvent communiquer sur l'utilisation de credits carbone. Le VCMI distingue trois niveaux : Silver (achat de credits couvrant le scope 3), Gold (scopes 1+2+3 partiellement couverts), Platinum (scopes 1+2+3 entierement couverts). Prerequis : avoir un objectif SBTi valide et etre en bonne voie de l'atteindre.

### Contribution climatique vs compensation

**Cadre conceptuel recommande** : Abandonner le terme "compensation carbone" (qui implique une annulation des emissions) au profit de "contribution climatique" (qui reconnait le financement de projets clima positifs sans pretendre a la neutralite). Cette approche est alignee avec le Net Zero Initiative (Carbone 4) :

**Pilier A — Reduction des emissions** : Reduire les emissions de la chaine de valeur (scopes 1, 2, 3). C'est la priorite absolue.
**Pilier B — Evitement des emissions hors chaine de valeur** : Financer des projets qui evitent des emissions ailleurs (avoidance credits). Ne compte pas dans l'objectif SBTi.
**Pilier C — Retrait de carbone** : Financer des puits de carbone (removal credits). Obligatoire pour le residuel SBTi Net Zero.

---

## Analyse du Cycle de Vie (ACV / LCA)

### Presentation et normes de reference

L'ACV (Analyse du Cycle de Vie) ou LCA (Life Cycle Assessment) est une methode systematique d'evaluation des impacts environnementaux d'un produit, service ou procede tout au long de son cycle de vie ("du berceau a la tombe" ou "du berceau au berceau").

**Normes de reference** :
- ISO 14040:2006 — Principes et cadre
- ISO 14044:2006 — Exigences et lignes directrices
- ISO 14067:2018 — Empreinte carbone des produits (specifique GES)
- PEF (Product Environmental Footprint) — methode europeenne

### Les 4 phases de l'ACV (ISO 14040)

#### Phase 1 — Definition des objectifs et du champ de l'etude

**Elements a definir** :
- Objectif de l'etude : pourquoi realiser l'ACV (ecoconception, communication, reporting, comparaison de produits)
- Unite fonctionnelle : quantifier la fonction rendue par le produit (exemple : "fournir 1 000 litres d'eau potable pendant 10 ans" plutot que "une bouteille d'eau")
- Frontieres du systeme : quels processus inclure et exclure (cradle-to-gate, cradle-to-grave, cradle-to-cradle)
- Categories d'impact evaluees : changement climatique, epuisement des ressources, acidification, eutrophisation, etc.
- Hypotheses et limitations

**Types de frontieres** :
- **Cradle-to-gate** : de l'extraction des matieres premieres a la sortie d'usine. Utile pour les produits intermediaires.
- **Cradle-to-grave** : de l'extraction a la fin de vie (mise en decharge, recyclage, incineration). Approche la plus complete pour les produits finis.
- **Cradle-to-cradle** : integre la circularite (les materiaux en fin de vie deviennent des matieres premieres pour un nouveau cycle).

#### Phase 2 — Inventaire du cycle de vie (ICV / LCI)

Collecter les donnees quantitatives sur tous les flux entrants (matieres premieres, energie, eau) et sortants (emissions dans l'air, l'eau, le sol, dechets) pour chaque processus du cycle de vie.

**Sources de donnees** :
- Donnees primaires : mesures directes sur les sites de production, donnees operationnelles
- Bases de donnees generiques : ecoinvent (la plus utilisee internationalement, 20 000+ datasets), GaBi (Sphera), Base IMPACTS ADEME (France), Agribalyse (alimentaire France)
- Donnees fournisseurs : Environmental Product Declarations (EPD), fiches produit

**Regles d'allocation** : Quand un processus produit plusieurs co-produits, repartir les impacts entre les co-produits par allocation physique (masse, volume, contenu energetique) ou economique (valeur de marche). La norme ISO 14044 recommande d'eviter l'allocation quand c'est possible (expansion du systeme).

#### Phase 3 — Evaluation de l'impact (LCIA)

Convertir les donnees d'inventaire en impacts environnementaux. Les methodes d'evaluation les plus utilisees :

**Methodes midpoint (point milieu)** :
- CML-IA : methode de reference, 11 categories d'impact
- ReCiPe Midpoint : 18 categories d'impact, tres complete
- EF (Environmental Footprint) : methode europeenne, 16 categories d'impact, recommandee pour le PEF

**Categories d'impact principales** :
| Categorie | Indicateur | Unite |
|---|---|---|
| Changement climatique | GWP (Global Warming Potential) | kg CO2e |
| Epuisement de la couche d'ozone | ODP | kg CFC-11e |
| Acidification | AP | mol H+e |
| Eutrophisation aquatique | EP | kg PO4e |
| Formation d'ozone photochimique | POCP | kg NMVOCe |
| Epuisement des ressources minerales | ADP | kg Sbe |
| Consommation d'eau | Water use | m3 |
| Utilisation des sols | Land use | Dimensionless (pt) |
| Ecotoxicite | CTUe | CTUe |
| Toxicite humaine | CTUh | CTUh |

#### Phase 4 — Interpretation

Analyser les resultats, identifier les contributeurs principaux (hotspots), tester la sensibilite aux hypotheses, et formuler des conclusions et recommandations.

**Analyse de contribution** : Identifier quelles etapes du cycle de vie et quels processus contribuent le plus a chaque categorie d'impact. Generalement : 20% des processus contribuent a 80% des impacts.

**Analyse de sensibilite** : Tester la robustesse des conclusions en faisant varier les hypotheses cles (duree de vie, taux de recyclage, source d'electricite, facteurs d'emission). Les conclusions doivent etre stables face a des variations raisonnables des hypotheses.

**Revue critique** : Pour les etudes comparatives destinees a la communication publique, une revue critique par un panel d'experts independants est obligatoire (ISO 14044 clause 6.1).

### Outils ACV

| Outil | Type | Usage |
|---|---|---|
| **SimaPro** | Logiciel professionnel | ACV detaillee, recherche, consultants |
| **GaBi (Sphera)** | Logiciel professionnel | ACV industrielle, grandes entreprises |
| **OpenLCA** | Open source | ACV accessible, PME, recherche |
| **Ecochain Helix** | SaaS cloud | ACV simplifiee, ecoconception |
| **One Click LCA** | SaaS specialise batiment | ACV batiment, EPD, certifications |

---

## State of the Art (2024-2026)

### Evolution du GHG Protocol

Le GHG Protocol est en cours de revision pour la premiere fois depuis 2004 (Corporate Standard) et 2011 (Scope 3 Standard) :
- Mise a jour des guidelines scope 2 : clarification des regles pour les PPA, les garanties d'origine, et la comptabilisation de l'electricite renouvelable dans un contexte de marche evolue
- Mise a jour du scope 3 : amelioration des methodes de calcul, hierarchie des donnees (primaires vs secondaires), guidelines specifiques pour les secteurs financiers (alignement PCAF), et clarification du scope 3 downstream
- Le Land Sector and Removals Guidance (publie 2022) clarifie la comptabilisation des removals et du secteur des terres (FLAG), devenu obligatoire pour les objectifs SBTi dans les secteurs FLAG

### Evolution du SBTi

- Le SBTi a revise son Corporate Net-Zero Standard en 2024, renforçant les exigences sur le scope 3 et clarifiant les criteres de neutralisation des emissions residuelles
- Debat majeur sur les Environmental Attribute Certificates (EACs) et les credits carbone dans les objectifs scope 3 : le SBTi a initie une consultation en 2024, avec des positions divergentes entre les ONG (contre) et les entreprises (pour un usage encadre)
- Extension des methodologies sectorielles : le SBTi a publie la guidance FLAG (Forest, Land and Agriculture) obligeant les entreprises des secteurs alimentaire, forestier et agricole a inclure les emissions FLAG dans leurs objectifs
- Le Financial Institutions SBTi Guidance est de plus en plus adopte par les banques et asset managers pour definir des objectifs sur les emissions financees

### Marches carbone en mutation

- L'Article 6 de l'Accord de Paris (marches carbone internationaux) est entre en phase operationnelle. L'Article 6.2 (transferts bilateraux entre pays) genere les premiers ITMOs (Internationally Transferred Mitigation Outcomes). L'Article 6.4 (mecanisme centralise supervise par l'ONU, successeur du MDP) est operationnel.
- Le CBAM (Carbon Border Adjustment Mechanism) europeen est en phase transitoire (reporting obligatoire des emissions embodied dans les importations). La phase definitive (achat de certificats CBAM) demarre en 2026.
- Le prix du carbone EU ETS a oscille entre 50 et 100 EUR/tCO2 sur 2023-2025. Les analystes anticipent une hausse progressive vers 100-150 EUR/tCO2 d'ici 2030 en raison du resserrement du cap.
- Sur le marche volontaire, les prix des credits carbone ont connu une forte volatilite. Les credits removal (biochar, DACS) se negocient a 100-1 000+ EUR/tCO2, tandis que les credits avoidance de qualite variable se negocient entre 5 et 50 EUR/tCO2. La tendance est a la premiumisation des credits haute qualite.

### Technologies de decarbonation emergentes

| Technologie | TRL | Potentiel | Cout actuel |
|---|---|---|---|
| **Green hydrogen** | 7-8 | Industrie, transport lourd, stockage | 4-8 EUR/kg H2 |
| **Direct Air Capture (DAC)** | 6-7 | Removal permanent | 400-1 000 EUR/tCO2 |
| **CCUS (Carbon Capture, Utilization and Storage)** | 7-9 | Industrie lourde (ciment, acier) | 50-120 EUR/tCO2 |
| **Enhanced weathering** | 5-6 | Removal distribue, agriculture | 50-200 EUR/tCO2 |
| **Biochar** | 8-9 | Removal, amendement sols | 100-300 EUR/tCO2 |
| **SAF (Sustainable Aviation Fuel)** | 8-9 | Aviation | 2-5x cout du kerosene |
| **E-fuels** | 6-7 | Aviation, maritime | 3-6x cout des fossiles |
| **Batteries etat solide** | 5-6 | Vehicules electriques, stockage | En developpement |

### Scope 3 : le defi de la donnee fournisseur

Le scope 3 reste le principal defi de la comptabilite carbone :
- Les methodes spend-based (estimation des emissions a partir des depenses en EUR) restent dominantes mais peu precises (incertitude de 30-50%)
- L'emergence de plateformes de collecte de donnees fournisseurs (CDP Supply Chain, EcoVadis Carbon, Trazable, Emitwise) ameliore progressivement la qualite des donnees
- Le PACT (Partnership for Carbon Transparency, ex-WBCSD Pathfinder Framework) standardise l'echange de donnees carbone produit entre entreprises (Product Carbon Footprint — PCF) via des APIs interoperables
- La Digital Product Passport (DPP) europeenne, obligatoire pour les batteries (2027) et progressivement pour d'autres produits, inclura des donnees d'empreinte carbone standardisees

### ACV et numerique

- Les outils d'ACV integrent de plus en plus l'IA pour automatiser la collecte de donnees et l'identification des hotspots
- Le PEF (Product Environmental Footprint) europeen avance vers des PEFCR (Product Environmental Footprint Category Rules) harmonisees, facilitant la comparabilite
- L'affichage environnemental obligatoire se deploie (France : Eco-Score alimentaire, Ecoscore textile), s'appuyant sur des ACV simplifiees et des bases de donnees sectorielles (Agribalyse, Base IMPACTS)
- Les EPD (Environmental Product Declarations) numeriques se generalisent dans le batiment (RE2020 en France) et l'industrie
