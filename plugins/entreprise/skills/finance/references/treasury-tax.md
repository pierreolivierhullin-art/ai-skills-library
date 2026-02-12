# Treasury & Tax — Cash Management, Couverture de Change, Fiscalite & Prix de Transfert

## Overview

Ce document de reference couvre la gestion de tresorerie et la strategie fiscale d'entreprise : previsions de tresorerie, financement du BFR, couverture de change (FX hedging), cash pooling, optimisation de l'IS et de la TVA, credits d'impot (CIR/CII), prix de transfert et integration fiscale. Utiliser ce guide comme fondation pour structurer la tresorerie, securiser la liquidite et optimiser la charge fiscale dans le respect des obligations legales.

---

## Cash Management — Previsions et Pilotage de la Tresorerie

### Prevision de Tresorerie a 13 Semaines (13-Week Cash Flow Forecast)

Le cash flow forecast a 13 semaines est l'outil central de la gestion de tresorerie operationnelle. Il couvre un horizon de 3 mois glissants avec une granulite hebdomadaire, permettant d'anticiper les besoins de financement et les excedents a placer.

#### Structure du forecast 13 semaines

```
Solde d'ouverture (semaine N)

ENCAISSEMENTS
  + Encaissements clients (factures echues + previsions d'encaissement)
  + Subventions et aides (CIR, aides publiques)
  + Produits financiers (interets, dividendes recus)
  + Autres encaissements (cessions d'actifs, apports en capital)
= Total encaissements

DECAISSEMENTS
  - Fournisseurs (factures echues + engagements a venir)
  - Salaires et charges sociales (dates de virement paie)
  - TVA (dates d'echeance des declarations)
  - IS (acomptes trimestriels : 15/03, 15/06, 15/09, 15/12)
  - Loyers et charges locatives
  - Remboursements d'emprunts (echeances contractuelles)
  - CAPEX (investissements planifies)
  - Autres decaissements
= Total decaissements

Flux net de la semaine = Encaissements - Decaissements
Solde de cloture = Solde d'ouverture + Flux net

Ligne de credit disponible (RCF non tiree)
Position de tresorerie totale = Solde de cloture + Ligne disponible
```

#### Bonnes pratiques du forecast 13 semaines

- **Mise a jour hebdomadaire** : chaque lundi, mettre a jour le forecast avec le reel de la semaine ecoulee et reviser les previsions des semaines suivantes.
- **Reconciliation** : comparer systematiquement le forecast de la semaine precedente avec le reel. Un ecart recurrent indique un biais dans les previsions.
- **Sources directes** : les donnees d'encaissement doivent provenir du systeme de facturation (balance agee), pas d'estimations approximatives. Les decaissements doivent refleter les echeances contractuelles reelles.
- **Scenarios de stress** : calculer en permanence un scenario de stress (encaissements -20%, decaissements +10%) pour dimensionner le matelas de securite.
- **Seuils d'alerte** : definir un solde minimum de tresorerie en dessous duquel une action est requise (ex: 2 mois de charges fixes). Alerter automatiquement le DAF si le forecast passe sous ce seuil.

### Indicateurs de Tresorerie

| Indicateur | Formule | Cible indicative |
|---|---|---|
| **Cash Runway** | Tresorerie / Cash burn mensuel | > 12 mois (startup), > 6 mois (PME) |
| **Quick Ratio (Acid Test)** | (Actifs circulants - Stocks) / Passifs circulants | > 1.0 |
| **Current Ratio** | Actifs circulants / Passifs circulants | 1.2 - 2.0 |
| **Cash Conversion Cycle (CCC)** | DSO + DIO - DPO | Le plus bas possible, negatif = ideal |
| **FCF Yield** | FCF / Valeur d'entreprise | > 5% considere attractif |
| **Debt Service Coverage Ratio (DSCR)** | EBITDA / (Interets + Remboursement principal) | > 1.5x (covenant bancaire typique) |

---

## Besoin en Fonds de Roulement (BFR) — Working Capital

### Composantes du BFR

```
BFR = Actif circulant d'exploitation - Passif circulant d'exploitation
    = (Stocks + Creances clients + Autres creances d'exploitation)
      - (Dettes fournisseurs + Dettes fiscales et sociales + Autres dettes d'exploitation)

En jours de CA :
BFR en jours = DSO + DIO - DPO

ou :
DSO (Days Sales Outstanding) = (Creances clients / CA TTC) x 365
DIO (Days Inventory Outstanding) = (Stocks / COGS) x 365
DPO (Days Payable Outstanding) = (Dettes fournisseurs / Achats TTC) x 365
```

### Leviers d'Optimisation du BFR

#### Reduction du DSO (poste clients)

- **Facturation immediate** : emettre la facture le jour de la livraison/prestation, pas en fin de mois.
- **Conditions de paiement** : negocier des delais courts (30 jours fin de mois). En France, le delai legal maximum est de 60 jours a compter de la date d'emission (ou 45 jours fin de mois).
- **Relance systematique** : mettre en place un processus de relance automatise (J-5 avant echeance, J+1, J+7, J+15, J+30 puis mise en demeure).
- **Escompte pour paiement anticipe** : proposer 1-2% d'escompte pour paiement a 10 jours au lieu de 60 jours. Le cout pour l'entreprise (environ 7-12% annualise) peut etre inferieur au cout du financement alternatif.
- **Scoring credit client** : evaluer la solvabilite des clients avant d'accorder des conditions de paiement (Coface, Ellisphere, donnees publiques). Plafonner l'encours par client.

#### Reduction du DIO (stocks)

- **Juste a temps (JIT)** : reduire les stocks de securite en ameliorant la fiabilite de la chaine d'approvisionnement.
- **ABC classification** : classer les stocks par valeur (A = 80% de la valeur en 20% des references) et ajuster les niveaux de stock en consequence.
- **Obsolescence** : identifier et provisionner les stocks a rotation lente (>6 mois sans mouvement). Liquider les stocks obsoletes plutot que de les conserver au bilan.

#### Augmentation du DPO (poste fournisseurs)

- **Negociation des delais** : allonger les delais de paiement dans le respect de la loi (60 jours max en France, Loi de Modernisation de l'Economie). Attention : les penalites pour retard de paiement sont juridiquement exigibles.
- **Centralisation des achats** : consolider les volumes pour negocier de meilleures conditions.
- **Reverse factoring (Supply Chain Finance)** : proposer aux fournisseurs un paiement anticipe par un tiers financeur en echange d'un escompte. Le fournisseur est paye plus vite, l'entreprise allonge son DPO.

### Instruments de Financement du BFR

#### Affacturage (Factoring)

L'affacturage consiste a ceder les creances clients a un factor (societe financiere specialisee) en echange d'un financement immediat (80-95% de la valeur faciale).

| Type | Caracteristique | Cout indicatif |
|---|---|---|
| **Affacturage avec recours** | Le cedant reste garant en cas d'impayes | Commission d'affacturage 0.3-1.0% + financement Euribor +1-2% |
| **Affacturage sans recours** | Le factor assume le risque d'insolvabilite | Commission 0.5-2.0% + financement Euribor +1-3% |
| **Affacturage confidentiel** | Le debiteur n'est pas informe de la cession | Prime supplementaire 0.1-0.3% |
| **Affacturage reverse** | Initie par l'acheteur au benefice de ses fournisseurs | Cout pour le fournisseur, generalement inferieur a son cout de financement |

#### Cession Dailly

La cession Dailly (loi du 2 janvier 1981) est un mecanisme de cession de creances professionnelles a une banque. Plus simple et moins couteux que l'affacturage mais sans les services associes (gestion du poste clients, assurance credit).

- **Fonctionnement** : l'entreprise cede un lot de creances a sa banque via un bordereau Dailly. La banque avance les fonds (80-100% selon la qualite des creances).
- **Cout** : taux de financement = Euribor + spread (1-3%) + commission de traitement.
- **Avantage** : rapidite (pas besoin de notification au debiteur en cas de cession a titre de garantie).
- **Limite** : pas de gestion du poste clients ni d'assurance credit, contrairement a l'affacturage.

---

## FX Hedging — Couverture du Risque de Change

### Identification de l'Exposition de Change

#### Types d'exposition

| Type | Definition | Horizon | Couverture |
|---|---|---|---|
| **Transaction exposure** | Impact des fluctuations de change sur les flux futurs libelles en devise etrangere | Court-moyen terme | Forwards, options |
| **Translation exposure** | Impact de la conversion des etats financiers des filiales etrangeres | Cloture comptable | Hedging de l'investissement net |
| **Economic exposure** | Impact structurel des variations de change sur la competitivite | Long terme | Diversification geographique, pricing |

### Instruments de Couverture

#### Contrat a terme (Forward)

Le forward fixe un taux de change pour une transaction future a une date determinee. C'est l'instrument le plus utilise pour couvrir le risque de change (>80% des couvertures corporate).

- **Avantage** : simplicite, cout nul a la souscription (pas de prime), taux fixe.
- **Inconvenient** : obligation de livrer a l'echeance (pas de participation a une evolution favorable du change).
- **Comptabilite** : en IFRS 9, le forward peut etre designe comme instrument de couverture (hedge accounting) pour eviter la volatilite en P&L.

#### Option de change

L'option donne le droit (mais pas l'obligation) d'acheter ou vendre une devise a un taux fixe (strike) a une date future.

- **Call** : droit d'acheter la devise (couverture d'un flux payable en devise).
- **Put** : droit de vendre la devise (couverture d'un flux recevable en devise).
- **Avantage** : protection contre l'evolution defavorable + participation a l'evolution favorable.
- **Inconvenient** : cout de la prime (1-3% du nominal selon la volatilite et la duree).

#### Strategies combinees

| Strategie | Construction | Cout | Profil |
|---|---|---|---|
| **Tunnel (collar)** | Achat d'une option + vente d'une option de sens inverse | Reduit ou nul (zero-cost collar) | Protection avec participation plafonnee |
| **Participating forward** | Forward + option | Prime reduite | Couverture partielle avec participation |
| **Accumulator** | Series de forwards conditionnes | Complexe | Accumulation progressive a taux favorable. Risque : knock-in en cas de mouvement adverse important |

### Politique de Couverture

Definir une politique de couverture formelle validee par le board :

```
Politique de couverture type :
1. Expositions certaines (contrats signes) : couverture 80-100% par forwards
2. Expositions probables (forecast a 3-6 mois) : couverture 50-80% par forwards ou options
3. Expositions possibles (forecast a 6-12 mois) : couverture 0-30% par options
4. Seuil minimum de couverture : ne pas couvrir les expositions < 50K EUR
5. Contreparties : diversifier entre 2-3 banques minimum
6. Reporting : position de couverture reportee mensuellement au DAF
7. Interdiction de speculation : pas de prise de position speculatives sur le change
```

---

## Cash Pooling

### Principes du Cash Pooling

Le cash pooling centralise la gestion de tresorerie des entites d'un groupe pour optimiser les soldes bancaires et reduire le cout de financement.

#### Cash pooling physique (Zero Balancing)

Les soldes des comptes des filiales sont transferes quotidiennement vers un compte centralisateur (compte pivot ou master account) :
- Les filiales en position creditrice pretent a la holding.
- Les filiales en position debitrice empruntent a la holding.
- Le solde net du groupe determine le besoin/excedent global.
- Reduction du cout de financement : le groupe finance son besoin net plutot que chaque filiale individuellement.

#### Cash pooling notionnel

Les soldes des comptes sont maintenus en place mais la banque calcule les interets sur le solde net consolide :
- Pas de transfert physique de fonds (avantage juridique et fiscal).
- La banque remunere/debite chaque filiale a un taux preferentiel base sur le solde net groupe.
- Plus simple a mettre en oeuvre dans un contexte multi-pays.
- Restrictions : certains pays interdisent ou limitent le cash pooling notionnel (Bresil, Inde, Chine).

### Considerations Fiscales du Cash Pooling

- **Prix de transfert** : les taux d'interet appliques aux prets intragroupe doivent etre conformes au principe de pleine concurrence (arm's length). Utiliser des taux de reference marche (Euribor, SOFR) + spread adapte au profil de risque.
- **Sous-capitalisation** : en France, les interets verses a des entreprises liees sont deductibles dans la limite d'un plafond (30% de l'EBITDA fiscal, avec un plancher de 3M EUR d'interets nets — article 212 bis du CGI).
- **Withholding tax** : les interets verses a des entites etrangeres peuvent etre soumis a retenue a la source. Verifier les conventions fiscales bilaterales.

---

## Strategie Fiscale — Optimisation dans le Respect des Regles

### Impot sur les Societes (IS)

#### Taux d'IS en France (2024-2026)

Le taux normal d'IS est de 25% depuis 2022. Les PME beneficient d'un taux reduit de 15% sur les 42 500 premiers euros de resultat fiscal (conditions : CA < 10M EUR, capital entierement libere, detenu a 75% par des personnes physiques).

#### Optimisation de la base imposable

- **Amortissements** : choisir entre amortissement lineaire et degressif selon l'impact fiscal souhaite. Le degressif accelere la deduction fiscale dans les premieres annees.
- **Provisions** : constituer toutes les provisions justifiees (depreciations de stocks, creances douteuses, litiges). Une provision deductible fiscalement reduit la base imposable.
- **Charges deductibles** : verifier que toutes les charges engagees dans l'interet de l'entreprise sont deduites (article 39-1 du CGI). Les charges somptuaires, les penalites et les amendes ne sont pas deductibles.
- **Reports deficitaires** : les deficits fiscaux sont reportables en avant sans limitation de duree, mais avec un plafond d'imputation de 1M EUR + 50% du benefice excedant 1M EUR (carry forward). Le report en arriere (carry back) est limite a 1M EUR sur l'exercice precedent.

### TVA — Optimisation et Gestion

#### Mecanisme de la TVA

```
TVA a payer = TVA collectee (sur les ventes) - TVA deductible (sur les achats)

Si TVA deductible > TVA collectee -> Credit de TVA
-> Possibilite de demander un remboursement (mensuel si regime reel normal avec option)
   ou imputation sur les declarations suivantes
```

#### Points de vigilance TVA

- **TVA intracommunautaire** : les acquisitions intracommunautaires sont soumises a autoliquidation. Verifier les numeros de TVA intracom via le systeme VIES.
- **TVA a l'importation** : depuis 2022, autoliquidation obligatoire de la TVA a l'importation (suppression du paiement a la douane).
- **TVA sur les acomptes** : en matiere de prestations de services, la TVA est exigible sur les encaissements (sauf option pour les debits). Les acomptes recus declenchent l'exigibilite.
- **Credits de TVA** : surveiller les credits de TVA non rembourses. Un credit de TVA superieur a 150 EUR est remboursable mensuellement (regime reel normal avec option mensuelle). Ne pas laisser dormir du cash chez l'administration.

### Credits d'Impot — CIR et CII

#### Credit d'Impot Recherche (CIR)

Le CIR est le dispositif fiscal le plus genereux pour les entreprises innovantes en France :

- **Taux** : 30% des depenses de R&D eligibles jusqu'a 100M EUR, puis 5% au-dela.
- **Depenses eligibles** : salaires et charges des chercheurs/ingenieurs de R&D, amortissements du materiel de recherche, frais de fonctionnement (50% des depenses de personnel, forfaitairement), sous-traitance aupres d'organismes agrees (plafonnee).
- **Condition** : les travaux doivent relever de la recherche fondamentale, de la recherche appliquee ou du developpement experimental (definition du Manuel de Frascati).
- **Securisation** : documenter rigoureusement les travaux de R&D (cahiers de laboratoire, rapports techniques, fiches projets). Le rescrit fiscal aupres de l'administration permet de securiser l'eligibilite en amont.

#### Credit d'Impot Innovation (CII)

Le CII complete le CIR pour les PME (au sens europeen : <250 salaries, CA <50M EUR ou bilan <43M EUR) :

- **Taux** : 30% des depenses d'innovation eligibles, plafonnees a 400K EUR par an.
- **Depenses eligibles** : conception de prototypes, installations pilotes de produits nouveaux (superieurs a l'etat de l'art sur le marche).
- **Distinction CIR/CII** : le CIR couvre la R&D (creation de connaissances nouvelles), le CII couvre l'innovation (amelioration superieure a l'existant).

### Prix de Transfert (Transfer Pricing)

#### Principe de pleine concurrence (Arm's Length)

Les transactions intragroupe (ventes de biens, prestations de services, redevances, financements) doivent etre valorisees au prix qui aurait ete convenu entre des parties independantes dans des conditions comparables. Ce principe est pose par l'article 57 du CGI et les Guidelines de l'OCDE.

#### Methodes de determination des prix de transfert

| Methode | Principe | Cas d'usage |
|---|---|---|
| **Prix comparable sur le marche libre (CUP)** | Comparaison avec des transactions comparables entre parties independantes | Marchandises cotees, services standardises |
| **Prix de revente moins (Resale Minus)** | Prix de vente au client final moins une marge de distribution | Distribution, revente sans transformation significative |
| **Cout majore (Cost Plus)** | Cout de production + marge | Prestations de services intragroupe, fabrication sous contrat |
| **Methode transactionnelle de la marge nette (TNMM)** | Comparaison de la marge nette operationnelle avec celle d'entreprises comparables | Methode la plus utilisee, applicable largement |
| **Methode de partage des benefices (Profit Split)** | Repartition du profit combine selon les contributions relatives | Transactions complexes, actifs incorporels uniques |

#### Documentation obligatoire

En France, les entreprises repondant a certains criteres (CA ou actif brut > 400M EUR, ou membre d'un groupe depassant ces seuils) doivent preparer une documentation de prix de transfert comprenant :
- **Master file** : description du groupe, de son activite, de sa politique de prix de transfert.
- **Local file** : description des transactions intragroupe de l'entite francaise, analyses de comparabilite, methode retenue.
- **Reporting pays par pays (CbCR)** : repartition du CA, des benefices, des impots payes et du nombre d'employes par juridiction (groupes >750M EUR de CA consolide).

### Integration Fiscale

L'integration fiscale permet de consolider les resultats fiscaux des societes d'un meme groupe pour n'acquitter qu'un seul IS sur le resultat d'ensemble.

#### Conditions

- La societe mere doit detenir directement ou indirectement au moins 95% du capital des filiales integrees.
- Les societes doivent avoir des exercices comptables coincidents.
- Option valable 5 ans, renouvelable.

#### Avantages

- **Compensation des benefices et des deficits** : le deficit d'une filiale vient en deduction du benefice d'une autre, reduisant la charge IS globale.
- **Neutralisation des operations intragroupe** : les dividendes intragroupe, les provisions sur titres de filiales integrees et certaines plus/moins-values intragroupe sont neutralises.
- **Economie de tresorerie** : le groupe ne paie qu'un IS sur le resultat net d'ensemble, reduisant les decaissements intermediaires.

---

## State of the Art (2024-2026)

### Treasury as a Service (TaaS) et API Banking

La tresorerie d'entreprise se transforme sous l'impulsion de la digitalisation bancaire :

- **Open banking / API bancaires** : les APIs PSD2 (Payment Services Directive 2) et au-dela permettent de connecter directement les systemes de tresorerie (Kyriba, GTreasury, Coupa Treasury) aux banques pour des operations en temps reel (soldes, virements, previsions). L'initiative SEPA API Access Scheme standardise les APIs bancaires en Europe.
- **Virtual accounts** : les banques proposent des comptes virtuels (sous-comptes logiques d'un compte physique) pour segmenter les flux par entite, par projet ou par client sans multiplier les comptes bancaires. Reduction des frais bancaires et simplification de la reconciliation.
- **Payment factories** : centralisation de l'emission des paiements groupe dans un hub unique (in-house bank ou via un outil de tresorerie centralise). Reduction des couts de traitement, controle renforce, standardisation des formats (ISO 20022).
- **Real-time payments** : les virements SEPA Instant (SCT Inst, <10 secondes, 24/7/365, plafond en hausse vers 100K+ EUR) transforment la gestion de tresorerie quotidienne. Les previsions de tresorerie deviennent plus precises quand les flux sont immediats.

### Embedded Finance et BaaS pour les Tresoriers

- **Banking-as-a-Service (BaaS)** : les entreprises integrent des services financiers (paiements, comptes, reconciliation) directement dans leurs systemes via des plateformes BaaS (Swan, Solarisbank, Treezor). Reduction de la dependance aux banques traditionnelles.
- **Auto-reconciliation** : les algorithmes de matching automatise reconcilent les mouvements bancaires avec les factures et les ecritures comptables en temps reel (>95% de matching automatique sur les flux recurrents).
- **Dynamic discounting** : les plateformes de supply chain finance (C2FO, Taulia, Kyriba) permettent aux fournisseurs de proposer des escomptes dynamiques en fonction de leur besoin de cash et du cout du capital de l'acheteur.

### Pillar Two — Impot Minimum Mondial (GloBE Rules)

La reforme fiscale internationale la plus significative depuis des decennies :

- **Principe** : un taux d'imposition effectif minimum de 15% (ETR) pour les groupes multinationaux dont le CA consolide depasse 750M EUR.
- **Mecanisme IIR (Income Inclusion Rule)** : la societe mere paie un complement d'impot si une filiale etrangere est imposee a moins de 15%.
- **Mecanisme UTPR (Undertaxed Profits Rule)** : si l'IIR n'est pas appliquee, les autres juridictions peuvent imposer les benefices sous-taxes.
- **Impact** : les strategies d'optimisation basees sur la localisation de profits dans des juridictions a faible fiscalite deviennent moins efficaces. Les groupes doivent recalculer l'ETR juridiction par juridiction et provisionner le complement d'impot (Top-Up Tax).
- **Implementation** : directive UE transposee en droit francais (article 33 de la LFI 2024). Application aux exercices ouverts a compter du 31 decembre 2023 pour l'IIR et du 31 decembre 2024 pour l'UTPR.

### IA et Automatisation en Fiscalite

- **Tax engines** : les moteurs de calcul fiscal (Vertex, Thomson Reuters ONESOURCE, Avalara) automatisent le calcul de la TVA, des taxes indirectes et de l'IS dans un contexte multi-juridictionnel.
- **Transfer pricing automation** : les outils TP (KPMG TP Catalyst, PwC TP Smart, Deloitte TP Studio) automatisent les benchmarks, la documentation et le monitoring des prix de transfert. Les modeles de ML identifient les transactions a risque.
- **Tax provision automation** : automatisation du calcul de la charge d'impot provisoire (tax provision) pour les clotures trimestrielles, incluant les impots differes et l'impact Pillar Two.
- **GenAI pour la veille fiscale** : les modeles de langage analysent les publications de l'administration fiscale, les jurisprudences et les textes legislatifs pour alerter sur les changements impactant l'entreprise.

### Crypto-actifs et Enjeux Fiscaux

L'emergence des crypto-actifs dans la tresorerie d'entreprise pose de nouveaux enjeux :

- **Qualification fiscale** : en France, les crypto-actifs sont des actifs incorporels. Les plus-values de cession sont imposees au taux d'IS pour les entreprises.
- **TVA** : les operations d'echange de crypto-monnaies contre des devises classiques sont exonerees de TVA (CJUE, Hedqvist, 2015). Les services lies aux crypto-actifs (staking-as-a-service, mining) posent des questions de TVA non encore pleinement resolues.
- **MiCA (Markets in Crypto-Assets)** : le reglement europeen MiCA (applicable progressivement 2024-2025) impose un cadre reglementaire aux prestataires de services sur actifs numeriques. Impact sur les tresoriers : les placements de tresorerie en stablecoins deviennent reglementairement encadres.
- **Comptabilisation** : en IFRS, les crypto-actifs sont generalement comptabilises en IAS 38 (intangible assets) au cout historique, avec test d'impairment. Le FASB americain a adopte en 2023 la juste valeur (fair value) pour les crypto-actifs repondant a certains criteres.

### ESG et Tresorerie Verte

- **Green bonds / obligations vertes** : financement dedie a des projets a impact environnemental positif. Le marche des green bonds a depasse 500 Md USD d'emissions cumulees. Les ETI et grands groupes accentuent leurs emissions vertes.
- **Sustainability-linked loans** : prets dont le taux d'interet est lie a l'atteinte d'objectifs ESG (reduction des emissions GHG, part d'energie renouvelable, KPIs sociaux). Mecanisme de bonus/malus sur le spread (+/- 5-15 bps).
- **Taxonomie europeenne** : la taxonomie UE definit les activites economiques "vertes" eligibles. Impact sur l'acces aux financements verts et sur le reporting extra-financier.
- **Carbon pricing interne** : de plus en plus de tresoriers integrent un prix interne du carbone dans les decisions d'investissement (prix ombre de 50-100 EUR/tonne CO2e) pour anticiper l'evolution de la reglementation.
