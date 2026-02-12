# Reporting Obligations — Transaction, Position, Tax & Cross-Border

Reference complete des obligations de reporting sur les marches financiers. Couvre le transaction reporting (MiFIR, FINRA), le position reporting, les declarations de participation (13F, 13D, 13G), la fiscalite des operations de marche (plus-values, IFU, Schedule D, Form 8949), et les obligations d'echange automatique d'informations (FATCA, CRS).

Complete reference for financial market reporting obligations. Covers transaction reporting (MiFIR, FINRA), position reporting, beneficial ownership filings (13F, 13D, 13G), tax reporting (capital gains, IFU, Schedule D, Form 8949), and automatic exchange of information (FATCA, CRS).

---

## Transaction Reporting — European Union

### MiFIR Article 26 — Transaction Reporting

Toute entreprise d'investissement qui execute des transactions sur des instruments financiers doit reporter chaque transaction a son autorite competente nationale (NCA) au plus tard a la fin du jour ouvrable suivant l'execution (T+1).

Every investment firm executing transactions in financial instruments must report each transaction to its NCA no later than the end of the business day following execution (T+1).

### Champ d'application / Scope

Instruments couverts :
- Instruments financiers admis a la negociation ou negocies sur un trading venue (RM, MTF, OTF)
- Instruments dont le sous-jacent est un instrument negocie sur un trading venue
- Instruments dont le sous-jacent est un indice ou un panier compose d'instruments negocies sur un trading venue
- CDS sur entites europeennes
- Quotas d'emission

### Contenu du report / Report Content

Le report contient 65 champs organises en categories :

**Identification des parties** :
- LEI (Legal Entity Identifier) de la firme executante et de la contrepartie
- Identifiant national du client personne physique (numero de passeport, identifiant fiscal national)
- Identification du decision maker au sein de la firme (si algorithme, identifiant de l'algo)
- Identification du short selling flag (position short nette, execution en principal)

**Identification de l'instrument et de la transaction** :
- ISIN de l'instrument ou identifiant CFI si pas d'ISIN
- Identifiant de l'ordre et de la transaction (unique)
- Venue d'execution (MIC code) ou "XOFF" pour les transactions OTC
- Date et heure d'execution (precision a la microseconde)
- Quantite et prix

**Champs relatifs au trading** :
- Type de transaction (achat, vente, autre)
- Transmission flag (si la firme a transmis l'ordre pour execution)
- Waiver indicators (Large in Scale, Reference Price, etc.)
- Indicateurs de vente a decouvert

### Canaux de reporting / Reporting Channels

- Reporting direct a la NCA
- Via un ARM (Approved Reporting Mechanism) agree
- Via le trading venue ou la plateforme d'execution (si l'accord est en place)
- La delegation du reporting est autorisee mais la firme executante reste responsable de l'exactitude et de la completude

### EMIR Trade Reporting

Distinct du transaction reporting MiFIR, le reporting EMIR concerne specifiquement les derives (OTC et ETD). Depuis EMIR Refit (avril 2024) :

- Format ISO 20022 XML obligatoire
- 129 champs de donnees (augmentation significative par rapport au format precedent)
- UTI (Unique Transaction Identifier) : genere selon la hierarchie definie (CCP > clearing member > sell-side > buy-side)
- UPI (Unique Product Identifier) : code ISDA CFI pour l'identification du type de derive
- Reporting aux Trade Repositories agrees par ESMA (DTCC, Regis-TR, UnaVista, KDPW)
- Double-sided : les deux contreparties doivent reporter (delegation possible)
- Reconciliation obligatoire entre les deux reports (matching des champs cles)

---

## Transaction Reporting — United States

### FINRA Trade Reporting

Les broker-dealers FINRA doivent reporter les transactions en temps reel ou quasi temps reel aux Trade Reporting Facilities (TRF) pour les equities NMS.

Facilities de reporting / Reporting facilities :
- **TRF (Trade Reporting Facility)** : Pour les transactions OTC en NMS stocks (NYSE TRF, NASDAQ TRF)
- **ORF (OTC Reporting Facility)** : Pour les transactions en OTC equity securities (non-NMS)
- **ADF (Alternative Display Facility)** : Pour l'affichage et la comparaison des cotations et transactions
- **TRACE (Trade Reporting and Compliance Engine)** : Pour les obligations (corporate bonds, agency bonds, ABS, MBS)

Delais de reporting / Reporting deadlines :
- NMS stocks (equities) : Dans les 10 secondes suivant l'execution pendant les heures de marche
- OTC equities : Dans les 10 secondes pendant les heures de marche
- TRACE (obligations) : 15 minutes pour les corporate bonds, temps reel pour les treasuries (depuis 2023)
- Options : Reporting automatique par les exchanges (pas d'obligation directe pour le broker)

### Rule 605 — Execution Quality Statistics

Les market centers (exchanges, market makers, ECNs) doivent publier mensuellement des statistiques d'execution pour les ordres couverts (covered orders) incluant :
- Effective spread / quoted spread ratio
- Taux d'execution (fill rate) et vitesse d'execution
- Price improvement (amelioration de prix) et disimprovement
- Taille effective vs taille quotee

### Rule 606 — Order Routing Disclosure

Les broker-dealers doivent publier trimestriellement des rapports sur le routage des ordres clients non diriges (non-directed orders) incluant :
- Top 10 venues par type d'ordre (market, limit, marketable limit)
- Payment for Order Flow (PFOF) recu par venue
- Profit sharing arrangements
- Depuis 2020 : rapports supplementaires pour les ordres institutionnels (> 10 000 USD notionnel)

---

## Position Reporting & Beneficial Ownership Disclosure

### MiFID II Position Reporting — Article 57/58

Obligations de position reporting pour les commodity derivatives :

- **Position limits** (Art. 57) : Les NCAs fixent des limites de position sur les commodity derivatives negocies sur les trading venues. Distinction entre position spot month et position other months.
- **Position reporting** (Art. 58) : Les operateurs de trading venues doivent publier hebdomadairement un rapport de positions (Commitment of Traders report europeen) et reporter les positions individuelles depassant les seuils a la NCA.
- **Position management** (Art. 57) : Les operateurs de trading venues doivent disposer de pouvoirs de position management (reduction ordonnee, limite individuelle).

### SEC — 13F Filing (Institutional Investment Managers)

Tout institutional investment manager exercant une discretion d'investissement sur au moins 100 millions USD d'instruments eligibles (Section 13(f) securities : actions cotees US, options sur actions, warrants, certains convertibles) doit deposer un Form 13F trimestriel aupres de la SEC.

Regles du 13F / 13F rules :
- Depot dans les 45 jours suivant la fin du trimestre calendaire
- Contenu : Chaque position de 10 000 actions ou plus OU d'une valeur de marche de 200 000 USD ou plus
- Voting authority : Declarer l'autorite de vote (sole, shared, none) pour chaque position
- Confidential treatment : Possibilite de demander un traitement confidentiel temporaire pour certaines positions (acquisition en cours, strategie proprietary)
- Le 13F ne couvre pas : les positions short, les obligations, les instruments non cotes, les commodity futures, les devises

### SEC — 13D/13G (Beneficial Ownership > 5%)

Toute personne ou groupe acquierant plus de 5% du beneficial ownership d'une classe d'equity securities enregistree sous le Securities Exchange Act doit deposer :

**Schedule 13D** (long form) :
- Depot dans les 5 jours ouvrables suivant le franchissement du seuil de 5%
- Disclosure complete : identite, source de financement, objectif de l'acquisition (passif, activiste, M&A), plans futurs
- Amendment dans les 2 jours ouvrables pour tout changement materiel (> 1% de variation)
- Exige pour les investisseurs actifs (activist investors) ayant l'intention d'influencer le controle ou la gestion

**Schedule 13G** (short form) :
- Disponible pour les investisseurs passifs (Qualified Institutional Investors, passive investors)
- Conditions : pas d'intention d'influencer le controle de l'emetteur
- Depot annuel (dans les 45 jours apres la fin de l'annee civile) + amendments si > 10% ou variation > 5%
- QII (Qualified Institutional Investors) : banques, assurances, broker-dealers, fonds enregistres. Depot annuel + amendment dans les 10 jours si > 10%
- Passage obligatoire au 13D si l'intention change de passive a active

### Section 16 Reporting (Officers, Directors, 10% Owners)

- **Form 3** : Initial statement of beneficial ownership. Depot dans les 10 jours suivant le statut d'insider.
- **Form 4** : Statement of changes. Depot dans les 2 jours ouvrables suivant tout changement (achat, vente, option exercise, gift).
- **Form 5** : Annual statement. Depot dans les 45 jours apres la fin de l'exercice fiscal pour les transactions exemptees non reportees sur Form 4.

---

## Tax Reporting — France

### Plus-values mobilieres / Capital Gains on Securities

**Regime du Prelevement Forfaitaire Unique (PFU) — Flat Tax** :

Le PFU s'applique par defaut aux plus-values de cession de valeurs mobilieres au taux global de 30% :
- 12.8% d'impot sur le revenu
- 17.2% de prelevements sociaux (CSG 9.2%, CRDS 0.5%, prelevement de solidarite 7.5%)

**Option pour le bareme progressif** :
- Le contribuable peut opter pour l'imposition au bareme progressif de l'IR (option globale pour tous les revenus de capitaux mobiliers et plus-values de l'annee)
- En cas d'option, benefice de l'abattement pour duree de detention pour les titres acquis avant le 1er janvier 2018 (50% entre 2 et 8 ans, 65% au-dela de 8 ans — abattement de droit commun)
- CSG deductible a hauteur de 6.8% (uniquement si option bareme progressif)

### IFU — Imprime Fiscal Unique

L'IFU (formulaire 2561) est le document fiscal que le courtier ou l'etablissement financier est tenu de transmettre au contribuable et a l'administration fiscale avant le 15 fevrier de chaque annee.

Contenu de l'IFU :
- Montant total des cessions (prix de cession brut)
- Plus-values et moins-values realisees
- Dividendes percus (montant brut, credits d'impot, retenues a la source)
- Interets percus
- Prelevements forfaitaires deja operes a la source (acompte IR de 12.8%)

### Formulaire 2074 — Declaration des plus-values complexes

Le formulaire 2074 est requis pour les situations qui ne sont pas couvertes par la declaration pre-remplie :
- Plus-values sur cessions de titres acquis a des dates differentes (lots multiples)
- Cessions de titres issus d'operations sur titres (OPT) : splits, fusions, apports
- Plus-values sur operations de SRD (Service de Reglement Differe)
- Plus-values sur options et warrants
- Report d'imposition (sursis, report d'imposition en cas d'apport-cession)
- Calcul des abattements pour duree de detention
- Moins-values reportables (imputables sur les plus-values des 10 annees suivantes)

### Declaration des comptes a l'etranger — Formulaire 3916

Tout resident fiscal francais detenant un compte a l'etranger (compte bancaire, compte-titres, compte de trading) doit le declarer chaque annee sur le formulaire 3916 / 3916-bis. Le defaut de declaration est sanctionne d'une amende de 1 500 EUR par compte non declare (10 000 EUR si le compte est dans un Etat non cooperatif).

---

## Tax Reporting — United States

### Schedule D — Capital Gains and Losses

Le Schedule D (Form 1040) recapitule les gains et pertes en capital de l'annee :

**Short-term capital gains (holding period <= 1 year)** : Taxes au taux ordinaire (jusqu'a 37% federal + state taxes).

**Long-term capital gains (holding period > 1 year)** : Taux preferentiels :
- 0% : Single filers jusqu'a 47 025 USD de taxable income (2024)
- 15% : Single filers de 47 026 a 518 900 USD
- 20% : Single filers au-dessus de 518 900 USD
- 3.8% Net Investment Income Tax (NIIT) additionnel pour les AGI > 200 000 USD (single) / 250 000 USD (married filing jointly)

### Form 8949 — Sales and Other Dispositions of Capital Assets

Le Form 8949 detaille chaque transaction individuelle. Il est organise en deux parties :
- **Part I** : Short-term (holding period <= 1 year)
- **Part II** : Long-term (holding period > 1 year)

Pour chaque transaction :
- Description of property (ticker symbol, nombre d'actions)
- Date acquired and date sold
- Proceeds (prix de vente)
- Cost or other basis (prix d'achat + commissions)
- Adjustment codes : W (wash sale), B (basis reported to IRS), D (market discount), etc.
- Gain or loss

Categories de reporting (basis reported vs not) :
- **Box A** : Short-term, basis reported to IRS on Form 1099-B
- **Box B** : Short-term, basis NOT reported to IRS
- **Box C** : Short-term, Form 1099-B not received
- **Box D** : Long-term, basis reported to IRS
- **Box E** : Long-term, basis NOT reported to IRS
- **Box F** : Long-term, Form 1099-B not received

### Cost Basis Methods

- **FIFO (First In, First Out)** : Methode par defaut si aucune election. Les premiers titres achetes sont reputes les premiers vendus.
- **Specific Identification** : Le contribuable identifie precisement les lots vendus (necessite une instruction ecrite au broker avant la vente). Permet l'optimisation fiscale (tax-lot harvesting).
- **Average Cost** : Uniquement disponible pour les mutual funds et les DRIP plans. Cout moyen pondere de toutes les parts.
- **LIFO (Last In, First Out)** : Non standard pour les titres mais applicable a certaines situations. Tend a maximiser les short-term gains.

### Section 475(f) Mark-to-Market Election

Pour les traders qualifies (trader tax status), l'election 475(f) offre des avantages significatifs :
- Toutes les positions sont marked-to-market au 31 decembre (gain/perte fictif)
- Tous les gains/pertes sont traites comme ordinary income/loss
- Pas de limitation des pertes a 3 000 USD net capital loss
- Elimination de la wash sale rule
- Les pertes sont pleinement deductibles sans report

Conditions pour le trader tax status (jurisprudence) :
- Trading frequent, regulier et continu (pas de critere fixe, mais plusieurs centaines de trades par an)
- Intention de profit a court terme (pas de buy-and-hold)
- Activite substantielle en termes de temps consacre
- Le contribuable cherche a tirer profit des fluctuations de prix quotidiennes

---

## FATCA — Foreign Account Tax Compliance Act

### Cadre general / General Framework

FATCA (2010, entree en vigueur 2014) impose aux institutions financieres etrangeres (FFI) de reporter aux autorites fiscales americaines (IRS) les comptes detenus par des US persons.

FATCA (2010, effective 2014) requires Foreign Financial Institutions (FFIs) to report to the IRS accounts held by US persons.

### Obligations des FFI / FFI Obligations

Les FFI doivent :
- S'enregistrer aupres de l'IRS et obtenir un GIIN (Global Intermediary Identification Number)
- Identifier les US persons parmi leurs clients (US indicia : nationalite, lieu de naissance, adresse, numero de telephone US, instructions de transfert vers un compte US)
- Reporter annuellement les informations sur les comptes des US persons : nom, adresse, TIN (Tax Identification Number), solde du compte, revenus (interets, dividendes, produits de cession)
- Appliquer une retenue a la source (withholding) de 30% sur les paiements de source americaine aux FFI non participantes et aux titulaires de comptes recalcitrants

### Formulaires FATCA / FATCA Forms

- **W-9** : Fourni par les US persons aux institutions financieres pour certifier leur statut fiscal US (nom, adresse, TIN)
- **W-8BEN** : Fourni par les personnes physiques non-US pour certifier leur statut de non-US person et reclamer les benefices conventionnels (treaty benefits)
- **W-8BEN-E** : Equivalent du W-8BEN pour les entites (societes, trusts, fonds)
- **W-8IMY** : Pour les intermediaires financiers (FFIs agissant comme agents)

### IGA — Intergovernmental Agreements

La plupart des pays ont signe des IGA avec les US pour faciliter l'implementation de FATCA :
- **Model 1 IGA** : Les FFI reportent a leur autorite fiscale nationale, qui transmet les informations a l'IRS (exemple : France, Royaume-Uni, Allemagne)
- **Model 2 IGA** : Les FFI reportent directement a l'IRS avec le consentement du gouvernement local (exemple : Suisse, Japon)

---

## CRS — Common Reporting Standard

### Cadre general / General Framework

Le CRS (OCDE, 2014) est le standard mondial d'echange automatique d'informations fiscales. Il s'inspire directement de FATCA et impose aux institutions financieres de reporter les comptes detenus par des non-residents fiscaux a leur autorite fiscale, qui transmet ensuite les informations aux autorites fiscales des pays de residence des titulaires.

CRS (OECD, 2014) is the global standard for automatic exchange of tax information. Modeled on FATCA, it requires financial institutions to report accounts held by non-tax residents to their local tax authority, which then transmits the information to the tax authorities of the account holders' countries of residence.

### Differences avec FATCA / Differences from FATCA

| Aspect | FATCA | CRS |
|--------|-------|-----|
| Initiateur | USA (IRS) | OCDE (multilateral) |
| Personnes cibles | US persons uniquement | Tous les non-residents fiscaux |
| Critere de declaration | US indicia (nationalite, naissance) | Residence fiscale (auto-certification) |
| Retenue a la source | 30% withholding sur les non-conformes | Pas de retenue a la source |
| Nombre de juridictions | Bilateral (US + chaque pays) | > 100 juridictions signataires |
| Seuils de minimis | Certains seuils (comptes < 50 000 USD pre-existing individual) | Pas de seuil pour les nouveaux comptes (seuil 250 000 USD pour les comptes pre-existants d'entites) |

### Obligations des institutions financieres / Financial Institution Obligations

- Obtenir l'auto-certification de residence fiscale de chaque titulaire de compte (formulaire CRS)
- Appliquer des procedures de due diligence pour identifier la residence fiscale reelle
- Reporter annuellement a l'autorite fiscale locale : nom, adresse, TIN, date de naissance, juridiction de residence, numero de compte, solde, revenus (interets, dividendes, produits de cession, autres)
- Conserver les documents de due diligence pendant au moins 5 ans

### Implications pour les traders / Implications for Traders

- Tout compte de trading ouvert dans une juridiction differente de la residence fiscale sera automatiquement reporte
- Les courtiers en ligne operant dans des juridictions CRS (la quasi-totalite des pays europeens) reporteront les soldes et les revenus aux autorites fiscales du pays de residence
- Declarer proactivement les comptes etrangers (formulaire 3916 en France) pour eviter les penalites
- L'opacite fiscale est devenue quasiment impossible dans les juridictions CRS/FATCA participantes

---

## Beneficial Ownership Disclosure — Corporate Transparency Act (US)

Depuis janvier 2024, le Corporate Transparency Act (CTA) impose a la plupart des entites americaines (corporations, LLCs) et des entites etrangeres enregistrees aux US de declarer leurs beneficial owners a FinCEN (Financial Crimes Enforcement Network).

Beneficial owner : Toute personne physique qui, directement ou indirectement, (1) exerce un controle substantiel sur l'entite, ou (2) detient ou controle 25% ou plus des ownership interests.

Informations a declarer : Nom complet, date de naissance, adresse, numero d'identification (passeport, permis de conduire) et image du document d'identite.

Exemptions : Les grandes societes (> 20 employes, > 5 millions USD de chiffre d'affaires, presence physique aux US), les entites reglementees (banques, broker-dealers, fonds enregistres), et d'autres categories specifiques sont exemptees.
