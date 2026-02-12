# European Financial Market Regulation

Reference complete du cadre reglementaire europeen des marches financiers. Couvre MiFID II/MiFIR, EMIR (Refit), MAR, PRIIPs et SFDR. Ce document est la reference pour toute question portant sur la reglementation des marches financiers dans l'Union europeenne.

Complete reference for the European financial markets regulatory framework. Covers MiFID II/MiFIR, EMIR (Refit), MAR, PRIIPs, and SFDR. Use this document as the authoritative source for any question on EU financial market regulation.

---

## MiFID II / MiFIR — Markets in Financial Instruments

### Architecture reglementaire / Regulatory Architecture

MiFID II (Directive 2014/65/EU) et MiFIR (Regulation 600/2014) constituent le cadre central de la reglementation des marches d'instruments financiers dans l'UE. La directive necessite une transposition nationale ; le reglement est d'application directe.

MiFID II (Directive 2014/65/EU) and MiFIR (Regulation 600/2014) form the central framework for regulating financial instrument markets in the EU. The directive requires national transposition; the regulation is directly applicable.

Champ d'application / Scope :

- Entreprises d'investissement (investment firms) fournissant des services d'investissement
- Marches reglementes (regulated markets), MTF (Multilateral Trading Facilities), OTF (Organised Trading Facilities)
- Systematic Internalisers (SI) executant des ordres clients contre leur propre compte
- Instruments couverts : actions, obligations, derives, ETF, instruments du marche monetaire, emission de carbone

### Autorisation et passeport / Authorisation and Passport

Toute entreprise fournissant des services d'investissement dans l'UE doit obtenir un agrement de l'autorite competente nationale (NCA). L'agrement donne acces au passeport europeen permettant d'operer dans tout l'EEE en libre prestation de services (LPS) ou en libre etablissement (LE).

Any firm providing investment services in the EU must obtain authorisation from the national competent authority (NCA). Authorisation grants access to the European passport allowing operations across the EEA via freedom to provide services or freedom of establishment.

Exigences d'autorisation / Authorisation requirements :
- Capital initial minimum (selon les services : 75 000 EUR, 150 000 EUR, ou 750 000 EUR)
- Dirigeants effectifs competents et honorables (fit & proper assessment)
- Organisation adequate : compliance function, risk management, internal audit
- Plan d'activite detaille et projections financieres
- Procedures de gestion des conflits d'interets et de traitement des reclamations
- Politique de remuneration conforme (pas d'incitation a prendre des risques excessifs)
- Dispositif de continuite d'activite (BCP/DRP)

### Transparence pre- et post-negociation / Pre- and Post-Trade Transparency

**Pre-trade transparency (equity / actions)** : Les operateurs de marche, MTF et SI doivent publier en continu les meilleurs prix a l'achat et a la vente (bid/ask) et la profondeur du carnet d'ordres. Les SI sont soumis a des obligations de cotation pour les instruments liquides pour lesquels ils sont SI.

**Pre-trade transparency (non-equity)** : Obligations etendues par MiFIR aux obligations, produits structures, derives et quotas d'emission. Des waivers pre-trade existent : Large in Scale (LIS), Reference Price, Order Management Facility, Illiquid Instrument.

**Post-trade transparency** : Publication des transactions executees dans les delais prescrits. En temps reel pour les equities (15 minutes), avec possibilite de differe pour les non-equities selon la taille et la liquidite. Les donnees doivent etre publiees via un APA (Approved Publication Arrangement).

Regles a appliquer / Rules to apply :

- Verifier le regime de transparence applicable (equity RTS 1 / non-equity RTS 2)
- Identifier les waivers disponibles et leurs conditions d'application
- Publier via un APA agree par la NCA
- Respecter les delais de publication (real-time ou differe selon le waiver)
- Conserver les preuves de publication pendant 5 ans minimum

### Classification des clients / Client Classification

MiFID II impose une classification tripartite des clients qui determine le niveau de protection applicable :

| Classification | Protection | Obligations de la firme |
|---------------|-----------|------------------------|
| **Retail client** | Maximale | Suitability/appropriateness, KID PRIIPs, information complete sur les couts |
| **Professional client** | Standard | Suitability pour le conseil, appropriateness allege, information sur les couts |
| **Eligible counterparty** | Minimale | Obligations reduites, pas de suitability/appropriateness |

Regles de reclassification / Reclassification rules :
- Un retail peut demander a etre traite comme professionnel (opt-up) sous conditions quantitatives et qualitatives strictes (2 sur 3 : portefeuille > 500 000 EUR, experience professionnelle dans le secteur financier, volume de transactions significatif)
- Un professionnel peut demander a etre traite comme retail (opt-down) pour obtenir une protection accrue
- Documenter toute reclassification et obtenir le consentement ecrit du client

### Product Governance (gouvernance produit)

Le regime de product governance impose des obligations aux manufacturers (concepteurs de produits) et distributors (distributeurs) :

**Manufacturer** : Definir un target market positif et negatif pour chaque produit. Identifier les besoins, objectifs, caracteristiques et profil de risque du marche cible. Realiser un scenario analysis. Selectionner le canal de distribution adapte. Revoir le target market periodiquement.

**Distributor** : Identifier le target market au niveau de sa propre base de clients. Verifier la coherence entre le target market du manufacturer et sa propre evaluation. Ne pas distribuer hors target market sauf cas exceptionnel documente. Reporter au manufacturer les ventes hors target market.

### Inducements (incitations)

MiFID II restreint severement les incitations (commissions, retrocessions) :

- **Conseil independant et gestion de portefeuille** : Interdiction totale de recevoir et conserver des incitations de tiers. Toute incitation recue doit etre integralement retrocedee au client.
- **Autres services** : Incitations autorisees uniquement si elles ameliorent la qualite du service au client et ne portent pas atteinte au devoir d'agir au mieux des interets du client. Transparence totale sur le montant et la nature de l'incitation.
- **Research** : Obligation de dissocier le paiement de la recherche de l'execution (unbundling). Paiement via RPA (Research Payment Account) ou sur les ressources propres de la firme.

### Couts et charges / Costs and Charges Disclosure

Informer le client de maniere exhaustive sur tous les couts et charges, ex ante (avant la transaction) et ex post (apres la transaction, rapport annuel). Inclure les couts du service, les couts du produit, les couts de transaction, les incitations, et l'impact cumule des couts sur le rendement. Presenter les couts en montant absolu et en pourcentage.

---

## EMIR — European Market Infrastructure Regulation

### Cadre general / General Framework

EMIR (Regulation 648/2012), renforce par EMIR Refit (Regulation 2019/834) et EMIR 3.0, etablit le cadre pour les derives OTC : obligation de compensation (clearing), techniques d'attenuation des risques, et obligation de declaration (reporting) aux referentiels centraux (Trade Repositories).

EMIR (Regulation 648/2012), strengthened by EMIR Refit (2019/834) and EMIR 3.0, establishes the framework for OTC derivatives: clearing obligation, risk mitigation techniques, and reporting obligation to Trade Repositories.

### Obligation de clearing / Clearing Obligation

Les derives OTC denommes par ESMA comme soumis a l'obligation de clearing doivent etre compenses via une CCP (Central Counterparty) autorisee ou reconnue dans l'UE.

Classes soumises / Subject classes :
- Interest rate swaps (IRS) en EUR, GBP, USD, JPY, NOK, PLN, SEK
- Credit default swaps (CDS) sur indices iTraxx Europe et iTraxx Crossover
- Dates d'entree en vigueur echelonnees selon la categorie de contrepartie (FC, NFC+, NFC-)

Categories de contreparties / Counterparty categories :
- **FC (Financial Counterparty)** : Entreprises d'investissement, etablissements de credit, fonds d'investissement, assurances. Toujours soumises au clearing pour les classes designees.
- **NFC+ (Non-Financial Counterparty above threshold)** : Entreprises non financieres depassant les seuils de clearing dans au moins une classe d'actifs. Soumises au clearing pour toutes les classes.
- **NFC- (Non-Financial Counterparty below threshold)** : En dessous des seuils. Exemptees du clearing mais soumises au reporting et aux techniques de mitigation.

Seuils de clearing (notionnel brut) / Clearing thresholds :
- Credit derivatives : 1 milliard EUR
- Equity derivatives : 1 milliard EUR
- Interest rate derivatives : 3 milliards EUR
- FX derivatives : 3 milliards EUR
- Commodity and other : 4 milliards EUR (depuis EMIR 3.0)

### Techniques d'attenuation des risques / Risk Mitigation Techniques

Pour les derives OTC non compenses, appliquer les techniques suivantes :

- **Confirmation rapide** : Confirmer les termes du derive des que possible (idealement T+1, obligation legale selon le type)
- **Portfolio reconciliation** : Reconciliation periodique des portefeuilles entre contreparties (quotidienne si > 500 trades, hebdomadaire si 51-500, trimestrielle si <= 50)
- **Portfolio compression** : Evaluer periodiquement la possibilite de comprimer les portefeuilles pour reduire le risque de contrepartie
- **Dispute resolution** : Procedures formelles de resolution des litiges sur la valorisation
- **Margining bilateral** : Echange d'initial margin (IM) et de variation margin (VM) pour les derives OTC non compenses. VM quotidienne obligatoire. IM obligatoire au-dessus de 8 milliards EUR d'encours notionnel (seuil phase-in complet)
- **Mark-to-market quotidien** : Valorisation quotidienne des positions ouvertes

### Obligation de reporting / Reporting Obligation

Toutes les contreparties (FC et NFC, y compris NFC-) doivent reporter chaque transaction sur derives (OTC et ETD) a un referentiel central (TR) agree.

Regles de reporting / Reporting rules :
- Delai : J+1 (jour ouvrable suivant la conclusion, modification ou terminaison)
- Contenu : 129 champs sous le format ISO 20022 XML (depuis EMIR Refit)
- Double-sided reporting : Les deux contreparties doivent reporter (sauf delegation)
- Utilisation obligatoire de l'UTI (Unique Transaction Identifier) et du UPI (Unique Product Identifier)
- LEI (Legal Entity Identifier) obligatoire pour toutes les contreparties
- Conservation des donnees pendant au moins 5 ans apres la terminaison du contrat

### EMIR 3.0 — Evolutions recentes / Recent Evolutions

EMIR 3.0 introduit des ajustements significatifs :
- Obligation d'active account aupres d'une CCP de l'UE pour certains derives systemiquement importants (IRS en EUR, CDS sur indices EU)
- Relevement des seuils de clearing pour les commodity derivatives (4 milliards EUR)
- Simplification des obligations pour les NFC-
- Renforcement du cadre de supervision des CCP de pays tiers (Tier 2 CCPs)

---

## MAR — Market Abuse Regulation

### Cadre general / General Framework

MAR (Regulation 596/2014) etablit un cadre harmonise pour la prevention et la detection des abus de marche dans l'UE. Il s'applique aux instruments financiers admis ou demandes a la negociation sur un marche reglemente, un MTF ou un OTF, ainsi qu'aux instruments dont le prix depend de ces instruments.

MAR (Regulation 596/2014) establishes a harmonised framework for preventing and detecting market abuse in the EU. It applies to financial instruments admitted to or requested for trading on a regulated market, MTF, or OTF.

### Insider Dealing (delit d'initie) — Article 14

Il est interdit a toute personne detenant une information privilegiee (inside information) de :
- Acquerir ou ceder des instruments financiers auxquels l'information se rapporte (insider dealing)
- Recommander a un tiers d'acquerir ou de ceder ces instruments (recommending/inducing)
- Communiquer cette information a un tiers hors du cadre normal de l'exercice professionnel (unlawful disclosure)

**Inside information** (Article 7) : Information precise, non publique, concernant directement ou indirectement un ou plusieurs emetteurs ou instruments financiers, et susceptible, si elle etait rendue publique, d'avoir un effet significatif sur le prix (price-sensitive information).

Test de la personne raisonnable : L'information est price-sensitive si un investisseur raisonnable serait susceptible de l'utiliser comme l'un des fondements de ses decisions d'investissement.

Sanctions : Les sanctions administratives MAR peuvent atteindre 5 millions EUR pour les personnes physiques et 15 millions EUR ou 15% du chiffre d'affaires pour les personnes morales. Les sanctions penales relevent du droit national (en France, jusqu'a 100 millions EUR d'amende et 5 ans d'emprisonnement).

### Market Manipulation (manipulation de marche) — Article 15

MAR interdit toute forme de manipulation de marche, incluant :

- **Transactions fictives ou trompeuses** : Ordres ou transactions donnant des indications fausses ou trompeuses sur l'offre, la demande ou le prix (wash trading, painting the tape)
- **Price positioning** : Fixer le prix a un niveau artificiel (marking the close, ramping)
- **Emploi de procedes fictifs ou artificiels** : Spoofing (ordres sans intention d'execution), layering (couches d'ordres pour influencer le carnet), stuffing (surcharge du carnet)
- **Dissemination d'informations fausses** : Diffusion de fausses informations ou rumeurs via les medias, internet ou tout autre canal

Indicateurs de manipulation (non exhaustifs) / Manipulation indicators :
- Proportion anormalement elevee d'ordres annules par rapport aux ordres executes
- Ordres places a des moments critiques (ouverture, cloture, fixings)
- Ordres places pres du bid/ask qui sont retires avant execution
- Concentration de transactions entre un nombre restreint de contreparties
- Negociations sur des volumes anormalement faibles ou eleves sans justification economique

### PDMR — Persons Discharging Managerial Responsibilities (Article 19)

Les PDMR (dirigeants, administrateurs, membres du conseil de surveillance) et les personnes qui leur sont etroitement liees (closely associated persons) doivent :

- Notifier a l'emetteur et a la NCA toute transaction sur les instruments de l'emetteur dans un delai de 3 jours ouvrables
- Seuil de notification : 5 000 EUR de transactions cumulees sur l'annee civile (certaines NCAs ont releve ce seuil a 20 000 EUR)
- Respecter les periodes de fermeture (closed periods) : interdiction de negocier pendant les 30 jours calendaires precedant la publication des resultats annuels ou semestriels
- L'emetteur doit publier la notification dans un delai de 3 jours ouvrables

### Insider Lists (listes d'inities) — Article 18

Tout emetteur ou toute personne agissant pour son compte doit etablir et tenir a jour une liste de toutes les personnes ayant acces a des informations privilegiees.

Exigences de la liste / List requirements :
- Identite de la personne (nom, prenom, date de naissance, numero d'identification national)
- Raison de l'inscription sur la liste
- Date et heure d'obtention de l'acces a l'information privilegiee
- Date de mise a jour de la liste
- Conservation pendant 5 ans apres l'etablissement ou la derniere mise a jour
- Format electronique conforme aux ITS (Implementing Technical Standards)

### STORs — Suspicious Transaction and Order Reports (Article 16)

Les operateurs de marche, les entreprises d'investissement et toute personne qui organise ou execute professionnellement des transactions doivent declarer sans delai a la NCA tout ordre ou transaction suspecte. Le STOR doit etre soumis des qu'il y a un soupcon raisonnable, meme si la transaction n'a pas ete executee (suspicious orders inclus).

---

## PRIIPs — Packaged Retail and Insurance-based Investment Products

### Key Information Document (KID) — Regulation 1286/2014

Tout manufacturer ou distributeur d'un PRIIP doit fournir au client retail un KID avant la conclusion de la transaction.

Le KID doit contenir / The KID must contain :
- Identite du manufacturer et de l'autorite competente
- Description du produit, son fonctionnement et ses objectifs
- Profil de risque : indicateur synthetique de risque (SRI) de 1 a 7
- Scenarios de performance : favorable, modere, defavorable, stress
- Couts totaux (RIY — Reduction in Yield methodology)
- Duree de detention recommandee et conditions de sortie anticipee
- Procedures de reclamation

Produits concernes / Products in scope : OPCVM (depuis janvier 2023), fonds structures, notes structurees, produits d'assurance-investissement, derives accessibles aux retail.

Regles imperatives / Mandatory rules :
- Maximum 3 pages A4
- Langage clair et non technique
- Mise a jour au moins annuelle ou en cas de changement significatif
- Fourniture sur support durable avant la transaction (papier ou electronique)

---

## SFDR — Sustainable Finance Disclosure Regulation

### Cadre general / General Framework

SFDR (Regulation 2019/2088) impose des obligations de transparence en matiere de durabilite aux participants des marches financiers (asset managers, conseillers en investissement, fonds de pension).

### Classification des produits / Product Classification

| Article | Classification | Exigences |
|---------|---------------|-----------|
| **Article 6** | Pas de promotion ESG | Disclosure de l'integration des risques de durabilite dans le processus d'investissement |
| **Article 8** | Promotion de caracteristiques E/S (light green) | Disclosure des caracteristiques promues, proportion d'investissements durables (si applicable), methodologie |
| **Article 9** | Objectif d'investissement durable (dark green) | Designation d'un indice de reference durable ou explication de la methodologie pour atteindre l'objectif |

### Principal Adverse Impacts (PAI)

Les participants des marches financiers doivent declarer s'ils prennent en compte les principales incidences negatives (PAI) de leurs decisions d'investissement sur les facteurs de durabilite.

PAI obligatoires (mandatory indicators) :
- Emissions de GES (Scope 1, 2, 3, intensite carbone, empreinte carbone)
- Exposition aux combustibles fossiles
- Part d'energie non renouvelable
- Intensite de consommation d'energie
- Biodiversite (sites sensibles)
- Emissions dans l'eau
- Ratio de dechets dangereux
- Violations du Pacte mondial des Nations Unies et des principes directeurs de l'OCDE
- Ecart de remuneration femmes-hommes
- Diversite au sein des conseils d'administration
- Exposition aux armes controversees

### Obligations de disclosure / Disclosure Obligations

- **Entity level** : Publication sur le site web de la politique d'integration des risques de durabilite, de la politique de remuneration relative a la durabilite, et de la declaration PAI (comply or explain)
- **Product level** : Information precontractuelle (annexes SFDR aux prospectus), reporting periodique (rapport annuel), site web
- **Format** : Templates RTS obligatoires (Delegated Regulation 2022/1288) avec des tableaux standardises
- **Taxonomie EU** : Pour les produits Article 8 avec investissements durables et Article 9, discloser la proportion d'activites alignees avec la Taxonomie EU (Regulation 2020/852)
