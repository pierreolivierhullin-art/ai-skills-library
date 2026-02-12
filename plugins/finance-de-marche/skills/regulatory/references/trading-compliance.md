# Trading Compliance — Best Execution, Order Handling, AML/KYC & Conduct

Reference complete des obligations de conformite operationnelle pour les activites de trading. Couvre les obligations de best execution, le traitement des ordres et la transparence, les conflits d'interets, la suitability et l'appropriateness, le record keeping, le personal account dealing (PAD), et les obligations AML/KYC pour les comptes de trading.

Complete reference for operational compliance obligations in trading activities. Covers best execution obligations, order handling and transparency, conflicts of interest, suitability and appropriateness, record keeping, personal account dealing (PAD), and AML/KYC for trading accounts.

---

## Best Execution Obligations

### MiFID II Best Execution — Article 27

L'obligation de best execution sous MiFID II impose aux entreprises d'investissement de prendre toutes les mesures suffisantes pour obtenir le meilleur resultat possible pour leurs clients lors de l'execution des ordres, en tenant compte des facteurs de best execution.

The best execution obligation under MiFID II requires investment firms to take all sufficient steps to obtain the best possible result for their clients when executing orders, considering the best execution factors.

### Facteurs de best execution / Best Execution Factors

Prendre en compte l'ensemble des facteurs suivants pour chaque execution :

- **Prix** : Le prix d'execution est le facteur predominant pour les clients retail. Pour les professionnels, il peut etre pondere differemment selon le contexte.
- **Couts** : Tous les couts lies a l'execution (commissions, frais de venue, frais de compensation, frais de reglement, spread).
- **Rapidite** : Le delai entre la reception de l'ordre et son execution.
- **Probabilite d'execution et de reglement** : La vraisemblance que l'ordre soit integralement execute et regle.
- **Taille** : La capacite du venue a absorber l'ordre sans impact significatif sur le prix.
- **Nature de l'ordre** : Caracteristiques specifiques (ordre a cours limite, ordre au marche, iceberg, VWAP, etc.).
- **Tout autre facteur pertinent** : Liquidite du marche, volatilite, conditions exceptionnelles.

### Politique de best execution / Best Execution Policy

Rediger et maintenir a jour une politique de best execution ecrite couvrant :

1. **Selection des venues d'execution** : Lister les venues utilises pour chaque classe d'instruments. Justifier la selection par des criteres objectifs (liquidite, couts, fiabilite, qualite d'execution). Inclure les Systematic Internalisers et les market makers si utilises.

2. **Hierarchie des facteurs** : Etablir la ponderation relative des facteurs de best execution par classe d'instruments et par type de client (retail vs professionnel). Pour les clients retail, le prix total (prix + couts) prime sauf circonstances exceptionnelles.

3. **Monitoring et revue** : Conduire un monitoring continu de la qualite d'execution. Comparer les executions obtenues avec les donnees de marche disponibles. Produire un rapport annuel de qualite d'execution (RTS 28 report) detaillant les 5 principaux venues par classe d'instruments et les mesures de qualite d'execution.

4. **Information au client** : Informer le client de la politique de best execution avant la fourniture du service. Obtenir le consentement prealable si l'execution a lieu en dehors d'un trading venue (OTC).

5. **Revue periodique** : Revoir la politique au moins annuellement ou en cas de changement significatif (nouveau venue, changement de structure de marche, degradation de la qualite d'execution).

### FINRA Rule 5310 — Best Execution (US)

Les broker-dealers FINRA doivent utiliser une diligence raisonnable (reasonable diligence) pour s'assurer que le meilleur marche est identifie pour le titre, et acheter ou vendre dans ce marche de maniere a obtenir le prix le plus favorable possible dans les circonstances prevalentes.

Exigences pratiques / Practical requirements :
- Conduire des reviews regulieres (au minimum trimestrielles) de la qualite d'execution
- Evaluer les venues alternatifs pour chaque type d'ordre
- Considerer les facteurs : prix, volatilite, liquidite relative, taille, timing, conditions de marche
- Documenter l'analyse et les decisions
- Evaluer l'impact du Payment for Order Flow (PFOF) sur la qualite d'execution
- Publier les rapports Rule 605 (market centers) et Rule 606 (order routing)

---

## Order Handling & Transparency

### Regles de traitement des ordres / Order Handling Rules

**Ordre de priorite / Order Priority** :

Traiter les ordres clients avec diligence et dans le meilleur interet du client. Respecter la priorite temporelle (time priority) et la priorite prix (price priority). Ne pas retarder l'execution d'un ordre client pour beneficier d'un mouvement de prix favorable au detriment du client.

- Ne jamais front-runner un ordre client (executer un ordre proprietary avant un ordre client au meme prix ou a un meilleur prix)
- Ne pas cherry-picker les ordres (executer les ordres rentables et retarder les ordres non rentables)
- Respecter la regle d'aggregation et d'allocation equitable si plusieurs ordres sont aggreges pour execution

**Aggregation et allocation / Aggregation and Allocation** :

L'aggregation d'ordres de plusieurs clients (ou d'ordres clients avec des ordres proprietary) est autorisee si :
- L'aggregation ne desavantage pas les clients individuels
- La politique d'allocation est definie ex ante et documentee
- L'allocation est effectuee equitablement, en general au prorata (pro rata)
- Si l'ordre aggregate est partiellement execute, aucun client ne doit etre systematiquement desavantage
- Les ordres proprietary ne doivent recevoir une allocation que si tous les ordres clients sont satisfaits, sauf si l'ordre proprietary avait ete place en premier et dans de meilleures conditions

**Limites d'ordres clients / Client Limit Orders** :

Sous MiFID II, si un ordre client a cours limite n'est pas immediatement executable et que le client ne donne pas d'instructions specifiques contraires, l'entreprise doit rendre l'ordre public en le transmettant a un trading venue afin de faciliter son execution. Une exception existe pour les ordres de grande taille (Large in Scale).

### Pre-Trade and Post-Trade Transparency

**Pre-trade (equities)** :
- Publication continue du meilleur prix achat/vente (BBO) et de la profondeur du carnet
- Waivers disponibles : Reference Price, Negotiated Trade, Large in Scale, Order Management Facility

**Pre-trade (non-equities — bonds, derivatives, SFPs, emission allowances)** :
- Publication des prix et interets indicatifs (indicative quotes)
- Waivers plus larges que pour les equities (illiquid instruments, size specific to the instrument, large in scale)

**Post-trade** :
- Publication des transactions executees : prix, volume, heure, venue
- Delai de publication : temps reel pour les equities (15 min max), deffered publication possible pour les non-equities (48h a 4 semaines selon la taille et la liquidite)
- Publication via un APA (Approved Publication Arrangement) pour les transactions OTC

---

## Conflicts of Interest

### Cadre MiFID II / MiFID II Framework

Les entreprises d'investissement doivent identifier, prevenir ou gerer les conflits d'interets entre la firme (y compris ses dirigeants, employes, agents lies) et ses clients, ou entre clients.

Investment firms must identify, prevent, or manage conflicts of interest between the firm (including its managers, employees, tied agents) and its clients, or between clients.

### Types de conflits a identifier / Conflict Types to Identify

- **Interets financiers divergents** : La firme gagne au detriment du client (execution a un prix defavorable, commissions excessives, incitations de tiers)
- **Conflits entre clients** : Allocation d'une IPO limitee, execution d'ordres opposes pour deux clients
- **Conflits lies a la recherche** : La recherche est influencee par les interets de l'activite de banque d'investissement ou de trading
- **Conflits lies aux remunerations** : La remuneration des employes incite a recommander des produits plus rentables pour la firme
- **Conflits lies aux informations** : Des informations confidentielles detenues dans une partie de la firme pourraient beneficier a une autre partie (Chinese Walls)

### Mesures de gestion / Management Measures

Appliquer les mesures suivantes de maniere proportionnee :

1. **Information barriers (Chinese Walls)** : Separer physiquement et logiquement les activites generant des conflits (recherche vs trading, banque d'investissement vs asset management). Restreindre l'acces aux informations confidentielles au strict necessaire (need-to-know basis). Implementer des controles d'acces logiques sur les systemes d'information.

2. **Politique de remuneration** : Eliminer les incentives directs qui creent des conflits (bonus lies au volume de commissions sur un produit specifique). Aligner la remuneration sur les interets des clients et sur la qualite du service.

3. **Politique d'inducements** : Appliquer les regles MiFID II sur les incitations (interdiction totale pour le conseil independant et la gestion de portefeuille, qualite de service pour les autres). Documenter chaque incitement recu ou verse.

4. **Politique d'allocation** : Definir une politique d'allocation ex ante pour les IPO, les placements et l'execution d'ordres aggreges. S'assurer de l'equite et de la transparence de l'allocation.

5. **Disclosure** : Si les mesures organisationnelles ne suffisent pas a prevenir le conflit, informer le client de la nature et de la source du conflit avant de proceder a la transaction. La disclosure est un dernier recours, pas une premiere ligne de defense.

6. **Registre des conflits** : Maintenir un registre actualise de tous les conflits d'interets identifies, des mesures prises et de leur efficacite.

---

## Suitability & Appropriateness

### Suitability (Adequation) — Conseil en investissement et gestion de portefeuille

Lorsqu'une entreprise fournit un conseil en investissement ou un service de gestion de portefeuille, elle doit obtenir les informations necessaires pour evaluer l'adequation de la recommandation au profil du client :

**Informations a collecter / Information to collect** :
- Connaissances et experience du client en matiere d'investissement (types d'instruments, frequence, education financiere)
- Situation financiere (revenus, patrimoine, engagements financiers, capacite a absorber des pertes)
- Objectifs d'investissement (horizon de placement, profil de risque, preferences de liquidite, objectifs ESG depuis MiFID II delegated acts)
- Capacite a absorber des pertes (total ou partiel du montant investi)
- Tolerance au risque (niveau de risque que le client est pret a accepter)

**Evaluation de l'adequation / Suitability Assessment** :
- Verifier que la recommandation correspond aux objectifs du client
- Verifier que le client peut supporter financierement les risques associes
- Verifier que le client possede les connaissances et l'experience necessaires pour comprendre les risques
- Documenter l'evaluation et la justification de la recommandation (suitability report)
- Fournir la declaration d'adequation au client retail avant l'execution

### Appropriateness (Caractere Approprie) — Execution avec conseil minimal

Pour les services d'execution sans conseil (execution-only) portant sur des instruments complexes, l'entreprise doit evaluer si l'instrument est appropriate pour le client en fonction de ses connaissances et de son experience :

- Evaluer la comprehension du client des risques associes a l'instrument
- Si l'instrument n'est pas appropriate, avertir le client (warning)
- Si le client ne fournit pas les informations, avertir le client qu'il n'est pas possible d'evaluer le caractere appropriate
- Documenter l'evaluation et l'avertissement eventuel

**Execution-only exemption** : Pour les instruments non complexes (actions cotees, obligations simples, OPCVM non structures, instruments du marche monetaire), le service d'execution peut etre fourni sans evaluation d'appropriateness si le service est fourni a l'initiative du client.

### Reg BI Obligations (US)

Regulation Best Interest impose aux broker-dealers un standard plus eleve que la suitability classique pour les recommendations aux retail customers :

- La recommandation doit etre dans le meilleur interet du client au moment ou elle est faite
- Le broker-dealer ne doit pas placer ses interets financiers ou autres avant ceux du client
- Identifier et attenuer les conflits d'interets lies a la recommandation
- Evaluer les alternatives raisonnablement disponibles
- Considerer les couts, les risques, les recompenses potentielles et la complexite du produit
- Ne pas faire de recommendations excessives (no excessive trading/churning)

---

## Record Keeping

### Obligations MiFID II / MiFID II Requirements

Conserver les enregistrements suivants pendant au minimum 5 ans :

- **Enregistrement des ordres** : Tous les ordres recus et transmis (date, heure, instrument, sens, quantite, prix, client, decision maker)
- **Enregistrement des transactions** : Toutes les transactions executees (memes champs + venue, contrepartie, frais)
- **Enregistrement des communications** : Toutes les communications relatives aux ordres et transactions, incluant les conversations telephoniques et les communications electroniques (emails, chats, messages instantanes)
- **Suitability et appropriateness** : Toutes les evaluations, les declarations d'adequation, les avertissements
- **Politique et procedures** : Toutes les versions des politiques internes (best execution, conflits d'interets, etc.)
- **Registre des reclamations** : Toutes les reclamations clients et leur traitement

**Telephone recording** : Obligation d'enregistrer les conversations telephoniques et les communications electroniques relatives aux ordres clients et aux transactions pour compte propre, y compris les communications internes relatives aux decisions d'investissement. Informer les clients et les employes de l'enregistrement.

### Obligations FINRA / FINRA Requirements

FINRA Rule 4511 impose la conservation des livres et registres conformement aux regles SEC (Rule 17a-3, 17a-4) :

- **6 ans** pour la plupart des enregistrements de comptes clients, des blotters, des ledgers
- **3 ans** pour les communications, les memoranda, les rapports
- **Lifetime of the firm + 3 years** pour les partnership agreements, articles of incorporation
- Format WORM (Write Once, Read Many) obligatoire pour les enregistrements electroniques
- Les electronic communications (emails, texts, social media) doivent etre conservees et supervisees

### Obligations specifiques de retention / Specific Retention Obligations

| Type d'enregistrement | MiFID II | FINRA/SEC |
|----------------------|----------|-----------|
| Ordres et transactions | 5 ans | 6 ans |
| Communications (tel, email) | 5 ans | 3 ans (communications), 6 ans (blotters) |
| Comptes clients | 5 ans | 6 ans apres fermeture |
| Suitability assessments | 5 ans | 6 ans |
| Reclamations | 5 ans | 4 ans |
| Politiques internes | Duree de validite + 5 ans | 3 ans apres cessation |

---

## Personal Account Dealing (PAD)

### Cadre MiFID II / MiFID II Framework

Les entreprises d'investissement doivent etablir des regles adequates pour empecher les operations personnelles (personal transactions) de leurs employes qui pourraient creer un conflit d'interets ou constituer un abus de marche.

Investment firms must establish adequate rules to prevent personal transactions by their employees that could create conflicts of interest or constitute market abuse.

### Regles a implementer / Rules to Implement

1. **Pre-clearance** : Exiger une autorisation prealable (pre-clearance) avant toute transaction personnelle sur des instruments couverts par la politique PAD. Le compliance officer ou un systeme automatise doit valider que la transaction ne genere pas de conflit avec les activites de la firme ou les ordres clients.

2. **Holding period** : Imposer une duree minimale de detention (holding period) pour les transactions personnelles (typiquement 30 jours, parametre selon le type d'instrument et la fonction de l'employe). Interdire le day trading personnel sur les instruments couverts.

3. **Restricted lists** : Maintenir une liste d'instruments restreints (restricted list) sur lesquels les transactions personnelles sont interdites (instruments sur lesquels la firme detient une information privilegiee, instruments faisant l'objet d'un mandat client, instruments en phase d'IPO/placement). Verifier automatiquement chaque pre-clearance contre la restricted list.

4. **Reporting periodique** : Exiger un reporting trimestriel (ou plus frequent) de toutes les transactions personnelles et des positions detenues. Comparer avec les pre-clearances accordees pour detecter les transactions non autorisees.

5. **Scope** : La politique doit couvrir les transactions de l'employe, de son conjoint, de ses enfants a charge et de toute personne etroitement liee (closely associated person). Inclure les comptes detenus aupres de courtiers tiers.

6. **Sanctions** : Definir un regime de sanctions internes pour les violations de la politique PAD (avertissement, amende, suspension, licenciement selon la gravite).

---

## AML/KYC for Trading Accounts

### Cadre reglementaire / Regulatory Framework

Les obligations AML/KYC (Anti-Money Laundering / Know Your Customer) pour les comptes de trading decoulent de :
- **EU** : 4eme et 5eme Directives Anti-blanchiment (AMLD4/AMLD5), Reglement de transfert de fonds, AMLR (nouveau reglement unifie en cours de transposition)
- **US** : Bank Secrecy Act (BSA), USA PATRIOT Act, FinCEN Customer Due Diligence (CDD) Rule
- **International** : Recommandations du GAFI/FATF (40 recommandations)

### Customer Due Diligence (CDD)

**Standard CDD** — A appliquer pour chaque ouverture de compte de trading :

1. **Identification du client** : Obtenir et verifier l'identite du client (personne physique : nom, date de naissance, adresse, document d'identite officiel ; personne morale : denomination, forme juridique, siege social, numero d'immatriculation, documents constitutifs)

2. **Identification du beneficial owner** : Identifier toute personne physique qui detient ou controle, directement ou indirectement, 25% ou plus des parts ou des droits de vote de l'entite cliente (seuil UE et US). Verifier l'identite du beneficial owner.

3. **Objet et nature de la relation d'affaires** : Comprendre et documenter l'objet du compte (investissement personnel, trading professionnel, hedging), les sources de revenus et de patrimoine, le volume et la frequence attendus des transactions.

4. **Monitoring continu** : Surveiller les transactions et les mouvements de fonds tout au long de la relation. Detecter les transactions inhabituelles ou incoherentes avec le profil declare du client.

**Enhanced Due Diligence (EDD)** — Appliquer des mesures renforcees dans les cas suivants :

- Client identifie comme PEP (Politically Exposed Person) ou personne etroitement liee a un PEP
- Client residant dans un pays a risque eleve (liste GAFI, liste de l'UE des pays tiers a haut risque)
- Relation d'affaires non presentielle (remote onboarding)
- Transaction complexe, inhabituellement importante ou sans objet economique apparent
- Structures opaques (societes ecran, trusts, nominees, bearer shares)

Mesures EDD / EDD measures :
- Approbation de la relation par un membre de la direction (senior management approval)
- Verification renforcee de la source des fonds et du patrimoine
- Monitoring renforce de la relation (revue plus frequente, seuils d'alerte plus bas)
- Documentation renforcee de l'analyse de risque

### Screening et listes de sanctions / Sanctions Screening

Appliquer un screening systematique contre :

- **Listes de sanctions** : UE (listes de mesures restrictives), OFAC (SDN List, Sectoral Sanctions), UN sanctions lists, HM Treasury (UK)
- **PEP lists** : Listes de personnes politiquement exposees (bases de donnees commerciales : World-Check, Dow Jones, LexisNexis)
- **Adverse media** : Surveillance des medias pour les informations negatives associees aux clients existants

Frequence / Frequency :
- A l'ouverture du compte (onboarding)
- A chaque modification des donnees client
- Screening batch periodique (quotidien ou hebdomadaire selon le risque)
- A chaque mise a jour des listes de sanctions
- Screening des transactions en temps reel pour les transferts de fonds

### Suspicious Activity Reporting

**Declaration de soupcon (SAR/STR)** :
- **France** : Declaration a TRACFIN (Traitement du Renseignement et Action contre les Circuits Financiers Clandestins) via le portail ERMES
- **US** : SAR (Suspicious Activity Report) aupres de FinCEN via le BSA E-Filing System. Depot dans les 30 jours suivant la detection de l'activite suspecte. Seuil de 5 000 USD pour les broker-dealers.
- **UK** : SAR aupres de la NCA (National Crime Agency) via le SAR Online system

Red flags specifiques au trading / Trading-specific red flags :
- Ouverture et fermeture rapide de comptes sans activite substantielle
- Virements importants immediatement suivis de retraits sans activite de trading
- Trading excessif sans profit apparent (potential wash trading for AML purposes)
- Utilisation de comptes multiples sans justification economique
- Transactions sur des instruments illiquides a des prix anormaux
- Depot de fonds de source non identifiee ou incoherente avec le profil du client
- Refus de fournir les informations KYC ou fourniture d'informations incoherentes
- Transactions impliquant des juridictions a risque eleve
- Changements soudains et inexpliques dans le pattern de trading du client

### Obligations de formation / Training Obligations

Former l'ensemble du personnel en contact avec les clients aux obligations AML/KYC :
- Formation initiale lors de l'embauche
- Formation de rappel annuelle (au minimum)
- Formations specifiques pour les fonctions a risque (front office, onboarding, compliance)
- Documentation des formations suivies et des tests de connaissance
- Sensibilisation aux typologies de blanchiment specifiques aux marches financiers (layering via le trading, integration via les produits d'investissement)
