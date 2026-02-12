# US Financial Market Regulation

Reference complete du cadre reglementaire americain des marches financiers. Couvre le Securities Exchange Act, Reg NMS, Pattern Day Trader (PDT), Regulation T (margin), wash sale rules, insider trading (Section 10b-5), et les regles FINRA. Ce document est la reference pour toute question portant sur la reglementation des marches financiers aux Etats-Unis.

Complete reference for the US financial markets regulatory framework. Covers the Securities Exchange Act, Reg NMS, Pattern Day Trader (PDT) rules, Regulation T (margin), wash sale rules, insider trading (Section 10b-5), and FINRA rules. Use this document as the authoritative source for any question on US financial market regulation.

---

## Securities Exchange Act of 1934

### Architecture reglementaire / Regulatory Architecture

Le Securities Exchange Act de 1934 constitue le fondement de la reglementation des marches secondaires aux Etats-Unis. Il cree la SEC (Securities and Exchange Commission) et etablit le cadre pour l'enregistrement des bourses, des broker-dealers, et des transfer agents. Il contient les dispositions fondamentales anti-fraude et anti-manipulation.

The Securities Exchange Act of 1934 is the foundation of US secondary market regulation. It created the SEC and established the framework for registration of exchanges, broker-dealers, and transfer agents. It contains the fundamental anti-fraud and anti-manipulation provisions.

Key sections a connaitre / Key sections :
- **Section 9** : Interdiction de la manipulation du prix des titres enregistres (wash sales, matched orders, manipulation of price)
- **Section 10(b)** : Clause generale anti-fraude, base de la Rule 10b-5 (insider trading, fraud in connection with securities)
- **Section 13** : Obligations de reporting periodique (10-K, 10-Q, 8-K) et beneficial ownership (13D, 13G, 13F)
- **Section 15** : Enregistrement des broker-dealers aupres de la SEC
- **Section 16** : Restrictions sur les short-swing profits des insiders (beneficial owners > 10%, officers, directors)

### Rule 10b-5 — Anti-Fraud Provision

La Rule 10b-5 est la disposition anti-fraude la plus importante du droit americain des marches financiers. Elle interdit, en relation avec l'achat ou la vente de tout titre :

- Employer tout stratageme, schema ou artifice tendant a la fraude (scheme to defraud)
- Faire une declaration inexacte d'un fait important ou omettre de declarer un fait important rendant les declarations faites non trompeuses (material misstatement or omission)
- Se livrer a tout acte, pratique ou mode operatoire qui constitue ou constituerait une fraude ou une tromperie (fraudulent act or practice)

Elements d'une action 10b-5 / Elements of a 10b-5 claim :
1. Material misrepresentation or omission (ou scheme to defraud)
2. Scienter (intention de tromper, manipuler ou frauder)
3. In connection with the purchase or sale of a security
4. Reliance (le plaintiff s'est appuye sur la declaration)
5. Economic loss
6. Loss causation (lien de causalite entre la fraude et la perte)

---

## Reg NMS — Regulation National Market System

### Cadre general / General Framework

Reg NMS (2005, amende periodiquement) modernise la structure du marche national des titres de participation (NMS securities). Il comprend quatre regles principales :

### Rule 611 — Order Protection Rule (Trade-Through Rule)

Interdire l'execution d'un trade a un prix inferieur a la meilleure cotation protegee disponible (protected quotation) sur un autre trading venue. Chaque trading center doit etablir des politiques et procedures pour prevenir les trade-throughs.

Protected quotation : Cotation automatiquement accessible et immediatement executable (automated quotation) affichee par un trading center NMS.

Exceptions au trade-through / Trade-through exceptions :
- Intermarket sweep orders (ISO) : Ordres envoyes simultanement a tous les venues affichant de meilleurs prix
- Flickering quotations : Cotations qui changent avant que l'ordre puisse etre route
- Self-help : Quand un trading center de destination ne repond pas dans des delais raisonnables
- Stopped orders, benchmark trades, qualified contingent trades

### Rule 610 — Access Rule

Garantir un acces equitable et non discriminatoire aux cotations protegees. Plafonner les frais d'acces (access fees) a 0.0030 USD par action pour les cotations protegees (30 mils). Interdire le "locked" et "crossed" markets (meilleure offre egale ou superieure a la meilleure demande).

### Rule 612 — Sub-Penny Rule

Interdire l'affichage, le classement ou l'acceptation d'un ordre a un increment de prix inferieur a 0.01 USD pour les titres cotes a 1.00 USD ou plus. Pour les titres cotes en dessous de 1.00 USD, l'increment minimum est de 0.0001 USD.

Note : La SEC a propose en 2022-2023 des reformes significatives a Reg NMS (tick size reform, order competition rule, best execution standard). Verifier le statut de ces propositions lors de l'application.

### Regulation SHO — Short Selling

Reg SHO encadre les ventes a decouvert :
- **Locate requirement** : Avant toute vente a decouvert, le broker-dealer doit avoir des raisons de croire que le titre peut etre emprunte (locate)
- **Close-out requirement** : Si une position short n'est pas livree a T+2, le broker-dealer doit acheter ou emprunter le titre pour effectuer la livraison (close-out)
- **Threshold securities list** : Titres avec des fails-to-deliver importants, soumis a des obligations renforcees
- **Circuit breaker (alternative uptick rule)** : Si le prix d'un titre baisse de 10% ou plus par rapport a la cloture de la veille, les short sales ne peuvent etre executees qu'a un prix superieur au meilleur national bid (restriction valable jusqu'a la fin du jour de bourse suivant)

---

## Pattern Day Trader (PDT) Rule

### Definition et regles / Definition and Rules

Un Pattern Day Trader est un client margin qui execute 4 day trades ou plus sur une periode de 5 jours ouvrables, a condition que le nombre de day trades represente plus de 6% de l'activite totale de trading du compte sur cette periode.

A Pattern Day Trader is a margin client who executes 4 or more day trades within 5 business days, provided the number of day trades represents more than 6% of total trading activity in the account during that period.

**Day trade** : Ouverture et fermeture de la meme position sur le meme titre dans le meme jour de bourse (achat puis vente, ou vente short puis rachat).

### Exigences / Requirements

- **Minimum equity** : Le compte doit maintenir une equity minimum de 25 000 USD a tout moment. Ce seuil s'applique en valeurs de marche incluant cash, actions et options.
- **Margin call** : Si l'equity tombe en dessous de 25 000 USD, le compte est soumis a un day trading margin call. Le trader doit deposer les fonds necessaires pour restaurer le seuil. Jusqu'au depot, le compte est restreint au trading dans un rapport de 2:1 (cash available).
- **Buying power** : Un PDT dispose d'un day trading buying power de 4 fois l'exces de maintenance margin (4x leverage intraday). Le buying power overnight reste a 2x (standard Reg T).
- **Account restriction** : En cas de non-depot du margin call sous 5 jours ouvrables, le compte est restreint a un trading cash-only pendant 90 jours.

### Strategies pour les traders sous le seuil / Strategies for traders below threshold

- Utiliser un cash account (pas de margin) : Pas de PDT rule applicable, mais obligation de respecter les regles de free-riding (attendre le settlement T+2 avant de reutiliser le produit d'une vente)
- Limiter les day trades a 3 sur une periode de 5 jours
- Utiliser plusieurs comptes chez differents broker-dealers (attention : chaque compte est evalue independamment, mais la consolidation peut etre appliquee par certains brokers)
- Trader des instruments non soumis au PDT : futures, forex spot (non-securities), crypto (traitement variable selon le broker)

---

## Regulation T — Margin Requirements

### Cadre general / General Framework

Reg T (Federal Reserve Board) fixe les exigences de marge initiale pour l'achat de titres sur marge. Les exigences de marge de maintenance sont fixees par les SROs (FINRA, exchanges).

Reg T (Federal Reserve Board) sets initial margin requirements for purchasing securities on margin. Maintenance margin requirements are set by SROs (FINRA, exchanges).

### Exigences de marge / Margin Requirements

| Type | Taux | Description |
|------|------|-------------|
| **Initial margin (Reg T)** | 50% | Deposit minimum de 50% de la valeur d'achat |
| **Maintenance margin (FINRA 4210)** | 25% | Equity minimum de 25% de la valeur de marche des titres long |
| **Short sale initial** | 150% | 50% margin requirement + 100% produit de la vente short |
| **Short sale maintenance** | 30% | Equity minimum de 30% de la valeur de marche des titres short |
| **Day trading (PDT)** | 25% intraday | Buying power = 4x maintenance excess (25% de la valeur des positions) |

Regles pratiques / Practical rules :
- Les broker-dealers peuvent imposer des exigences superieures a Reg T et FINRA (house requirements)
- Les concentrated positions peuvent etre soumises a des exigences de marge plus elevees
- Les options, warrants et titres speculates sont soumis a des regles de marge specifiques (Reg T Section 220.12, FINRA 4210)
- Les fonds Reg T sont disponibles a T+2 (settlement standard). Le free-riding (utilisation de fonds non regles) est interdit.

### Margin Accounts vs Cash Accounts

**Margin account** : Permet d'emprunter des fonds au broker-dealer pour acheter des titres. Soumis a Reg T et aux regles FINRA de maintenance margin. Le broker peut liquider des positions sans preavis si la maintenance margin n'est pas respectee (margin call liquidation).

**Cash account** : Pas d'emprunt. L'integralite du prix d'achat doit etre deposee. Pas de PDT rule applicable. Soumis aux regles de free-riding et good faith violations. Un cash account peut etre restreint pendant 90 jours apres une free-riding violation.

---

## Wash Sale Rule — Section 1091 IRC

### Definition et mecanisme / Definition and Mechanism

La wash sale rule interdit la deduction d'une perte realisee sur la vente d'un titre si un titre "substantiellement identique" (substantially identical security) est acquis dans une fenetre de 61 jours (30 jours avant la vente + le jour de la vente + 30 jours apres la vente).

The wash sale rule disallows the deduction of a loss realized on the sale of a security if a "substantially identical security" is acquired within a 61-day window (30 days before the sale + the day of the sale + 30 days after the sale).

### Mecanisme de report / Deferral Mechanism

La perte non deductible n'est pas perdue definitivement. Elle est ajoutee au cout de base (cost basis) du titre de remplacement et la periode de detention du titre vendu est ajoutee a celle du titre de remplacement :

```
Exemple / Example :
- Achat de 100 actions XYZ a 50 USD le 1er mars (cost basis = 5 000 USD)
- Vente de 100 actions XYZ a 40 USD le 15 juin (perte realisee = 1 000 USD)
- Rachat de 100 actions XYZ a 42 USD le 1er juillet (dans la fenetre de 30 jours)

Resultat / Result :
- La perte de 1 000 USD est non deductible (wash sale)
- Cost basis du nouveau lot = 42 USD + 10 USD (perte reportee) = 52 USD par action
- Holding period : la periode de detention du premier lot est ajoutee au second
```

### Substantially Identical Securities

Le concept de "substantially identical" n'est pas defini avec precision par l'IRS. Regles generales / General rules :
- Les memes actions de la meme societe sont toujours substantially identical
- Les options et les actions de la meme societe peuvent etre substantially identical
- Les ETF trackant le meme indice sont generalement considered substantially identical (ex : SPY et IVV trackers du S&P 500 — zone grise, prudence)
- Les obligations du meme emetteur avec des termes similaires peuvent etre substantially identical
- Les actions de societes differentes dans le meme secteur ne sont PAS substantially identical
- Un ETF broad market (S&P 500) et un ETF sectoriel (Technology) ne sont PAS substantially identical

### Pieges courants / Common Pitfalls

- La wash sale rule s'applique entre comptes (IRA, 401(k), compte taxable, compte du conjoint dans certains cas)
- Les dividendes reinvestis automatiquement (DRIP) dans la fenetre de 30 jours declenchent une wash sale
- Les options exercees ou assignees peuvent declencher une wash sale
- Un achat partiel dans la fenetre peut declencher une wash sale partielle
- Les short sales sont egalement soumises a la wash sale rule

### Election Mark-to-Market — Section 475(f) IRC

Les traders actifs qualifies (trader tax status) peuvent elire le traitement mark-to-market sous Section 475(f). Cette election :
- Elimine la wash sale rule (toutes les positions sont marked-to-market au 31 decembre)
- Convertit tous les gains/pertes en ordinary income/loss (pas de capital gains preferentiels)
- Permet de deduire les pertes de trading sans limitation (pas de cap de 3 000 USD)
- L'election doit etre faite avant le 15 avril de l'annee fiscale concernee (irrevocable)
- Ne s'applique pas aux titres detenus a des fins d'investissement (segregation requise)

---

## Insider Trading — US Framework

### Base legale / Legal Basis

L'insider trading aux US repose principalement sur la Rule 10b-5 et sur deux theories juridiques complementaires :

**Classical theory** : Un insider corporatif (officer, director, employee) qui trade sur la base d'informations materielles non publiques (MNPI) viole son duty of trust and confidence envers la societe et ses actionnaires.

**Misappropriation theory** (United States v. O'Hagan, 1997) : Toute personne qui detourne des MNPI en violation d'un devoir de confiance envers la source de l'information commet une fraude. Cette theorie etend l'interdiction au-dela des insiders corporatifs.

### Tipper/Tippee Liability

**Tipper** : L'insider qui communique des MNPI a un tiers (tippee) engage sa responsabilite si : (1) il a communique l'information en violation d'un devoir fiduciaire, et (2) il a recu un benefice personnel (personal benefit) de la communication (ce benefice peut etre reputationnel, reciproque, ou un cadeau a un proche).

**Tippee** : Le destinataire de l'information engage sa responsabilite s'il savait ou aurait du savoir que le tipper violait un devoir fiduciaire et qu'il trade sur la base de cette information.

Critere du personal benefit (Dirks v. SEC, 1983 ; Salman v. United States, 2016) : Un cadeau d'information a un trading relative ou friend constitue un personal benefit suffisant. Il n'est pas necessaire de prouver un benefice pecuniaire direct pour le tipper.

### Section 16 — Short-Swing Profits

Les insiders statutaires (officers, directors, beneficial owners > 10%) sont soumis a :

- **Form 3** : Declaration initiale de beneficial ownership (dans les 10 jours suivant le statut d'insider)
- **Form 4** : Declaration de tout changement de beneficial ownership (dans les 2 jours ouvrables)
- **Form 5** : Declaration annuelle des transactions exemptees (dans les 45 jours apres la fin de l'exercice fiscal)
- **Section 16(b) disgorgement** : Tout profit realise sur un achat et une vente (ou vente et achat) dans une periode de 6 mois est restituable a la societe (strict liability, pas besoin de prouver l'utilisation de MNPI)

### Regulation FD — Fair Disclosure

Reg FD (2000) interdit la divulgation selective d'informations materielles non publiques par un emetteur a certains destinataires privilegies (analystes, investisseurs institutionnels, hedge funds). Si une divulgation selective se produit :
- Si intentionnelle : divulgation publique simultanee requise
- Si non intentionnelle : divulgation publique dans les meilleurs delais (promptly, en pratique 24 heures ou avant l'ouverture du marche suivant)
- Modes de divulgation publique : press release, filing SEC (8-K), webcast accessible au public

---

## FINRA Rules

### Architecture de FINRA / FINRA Architecture

FINRA (Financial Industry Regulatory Authority) est le Self-Regulatory Organization (SRO) supervisant les broker-dealers aux Etats-Unis. Tout broker-dealer doit s'enregistrer aupres de FINRA pour operer. FINRA administre les examens de qualification (Series 7, 63, 65, 66, etc.) et conduit les examinations et les enforcement actions.

### Rule 2111 — Suitability (remplacee par Reg BI pour les recommendations retail)

FINRA Rule 2111 impose une obligation de suitability pour les recommendations faites aux clients. Trois composantes :

- **Reasonable-basis suitability** : La firme doit avoir une base raisonnable pour croire que la recommandation est adaptee a au moins certains clients
- **Customer-specific suitability** : La recommandation doit etre adaptee au profil specifique du client (objectifs, situation financiere, tolerance au risque, besoins, experience)
- **Quantitative suitability** : Le volume de transactions recommandees ne doit pas etre excessif (excessive trading/churning) au regard du profil du client

### Regulation Best Interest (Reg BI) — SEC Rule

Reg BI (2020) remplace FINRA 2111 pour les recommendations aux retail customers. Standard plus eleve que la suitability classique :

- **Disclosure obligation** : Fournir le Form CRS (Customer Relationship Summary) et les disclosures sur les conflits d'interets
- **Care obligation** : Exercer un soin raisonnable dans la recommandation, comprendre les risques et les couts, ne pas placer ses interets avant ceux du client
- **Conflict of interest obligation** : Identifier et eliminer ou attenuer les conflits d'interets (sales contests, quotas, compensation differentiee)
- **Compliance obligation** : Etablir des politiques et procedures ecrites pour se conformer a Reg BI

### Rule 5310 — Best Execution

Les broker-dealers doivent executer les ordres clients au meilleur prix raisonnablement disponible (best execution). Evaluer regulierement la qualite d'execution obtenue aupres des differents venues. Considerer : le prix, la vitesse d'execution, la probabilite d'execution, la taille de l'ordre, les couts de transaction.

Conduire des reviews regulieres (au moins trimestrielles) de la qualite d'execution par type d'ordre et par venue. Documenter les resultats et les actions prises. Publier les rapports Rule 605 (execution quality) et Rule 606 (order routing).

### Rule 4210 — Margin Requirements

FINRA 4210 fixe les exigences de maintenance margin :
- **Long equity** : 25% minimum de la valeur de marche
- **Short equity** : 30% minimum de la valeur de marche
- **Concentrated positions** : Exigences superieures possibles (up to 100% pour les penny stocks)
- **Day trading** : 25 000 USD minimum equity pour les PDT, 4x buying power intraday
- **Portfolio margin** : Alternative pour les comptes sophistiques, basee sur le risque du portefeuille (stress tests), equity minimum de 100 000 USD

### FINRA Examination and Qualification

| Examen | Designation | Activites autorisees |
|--------|-------------|---------------------|
| **Series 7** | General Securities Representative | Toutes les valeurs mobilieres (actions, obligations, options, fonds) |
| **Series 63** | Uniform Securities Agent | Enregistrement au niveau de l'Etat (state registration) |
| **Series 65** | Uniform Investment Adviser Law | Conseiller en investissement (investment adviser representative) |
| **Series 66** | Uniform Combined State Law | Combine Series 63 + 65 |
| **Series 24** | General Securities Principal | Supervision des activites de broker-dealer |
| **Series 57** | Securities Trader | Activites de proprietary trading |
| **SIE** | Securities Industry Essentials | Prerequis pour les Series 6, 7, 57, etc. |
