# Supplier Management — Selection, Evaluation, SRM, Performance & Development

Reference complete du management des fournisseurs. Couvre la selection et l'evaluation multicritere, les scorecards de performance, le Supplier Relationship Management (SRM), le developpement fournisseurs, les audits et certifications.

---

## Supplier Selection — Processus structure

### Identification et pre-qualification

#### Sources d'identification de fournisseurs
- **Bases de donnees e-procurement** : Ariba Discovery, Coupa Supplier Network, ThomasNet, Kompass, Europages.
- **Salons professionnels et federations sectorielles** : source privilegiee pour l'innovation et les fournisseurs de niche.
- **Recommandations internes** : prescripteurs, R&D, operations. Structurer la remontee d'informations.
- **Intelligence artificielle** : outils de supplier discovery bases sur le NLP qui scannent les sites web, brevets, publications pour identifier des fournisseurs potentiels par competence.
- **Benchmarks sectoriels** : etudes Gartner, Forrester, cabinets specialises achats (Kepler, Efficio, Procurement Leaders).

#### Criteres de pre-qualification (shortlisting)

Appliquer un filtre de pre-qualification avant d'investir du temps dans une evaluation detaillee :

```
Criteres eliminatoires (go/no-go) :
- Capacite de production suffisante pour les volumes requis
- Certifications obligatoires (ISO 9001, ISO 14001, sectorielles)
- Sante financiere minimale (score Altares/Coface > seuil defini)
- Conformite reglementaire (pas de sanctions, pas de liste noire)
- Couverture geographique compatible
- Conformite RSE minimale (EcoVadis > 25/100 ou equivalent)

Criteres de differentiation (scoring) :
- Competences techniques et references clients
- Capacite d'innovation et R&D
- Flexibilite et reactivite
- Competitivite prix (estimation TCO)
- Engagement RSE et trajectoire carbone
```

### Evaluation multicritere detaillee — Methode AHP simplifiee

#### Grille d'evaluation standard

Pour une evaluation structuree des fournisseurs shortlistes, utiliser une grille multicritere ponderee. Adapter les poids selon la categorie (Kraljic) :

| Critere | Poids Levier | Poids Strategique | Poids Goulet | Methode d'evaluation |
|---|---|---|---|---|
| **Prix / TCO** | 35% | 20% | 15% | Analyse TCO, cost breakdown |
| **Qualite** | 20% | 25% | 20% | Audit, echantillons, certifications |
| **Delai / Fiabilite** | 15% | 15% | 30% | Historique OTD, capacite declaree |
| **Innovation / Tech** | 5% | 20% | 10% | Roadmap R&D, brevets, references |
| **Solidite financiere** | 10% | 10% | 15% | Score credit, bilan, ratios |
| **RSE / ESG** | 10% | 10% | 5% | EcoVadis, audits, certifications |
| **Flexibilite** | 5% | 0% | 5% | Capacite de montee en charge |

#### Processus d'evaluation

1. **Analyse documentaire** : etude du dossier fournisseur (questionnaire, documents qualite, bilans financiers, rapports RSE).
2. **Visite de site / Audit** : evaluation in situ des capacites de production, des processus qualite, des conditions de travail. Obligatoire pour les fournisseurs strategiques et les nouveaux fournisseurs de production.
3. **Evaluation technique** : tests sur echantillons, essais en conditions reelles, validation par les prescripteurs.
4. **Analyse financiere** : scoring financier (Altares, Coface, D&B) complete d'une analyse de bilan pour les fournisseurs strategiques.
5. **Due diligence RSE** : verification de la conformite sociale et environnementale (voir reference contract-risk.md pour le detail KYS).
6. **Scoring consolide** : notation ponderee sur la grille multicritere, comparaison des fournisseurs, recommandation d'attribution.

---

## Supplier Performance Scorecard — QCDRSE

### Architecture du scorecard

#### Quality (Qualite)

| KPI | Definition | Cible typique | Frequence |
|---|---|---|---|
| **PPM (Parts Per Million)** | Nombre de pieces defectueuses par million livrees | < 50 PPM (industrie auto), < 500 PPM (general) | Mensuel |
| **Taux de non-conformite reception** | % de lots rejetes ou mis en quarantaine a la reception | < 1% | Mensuel |
| **Taux de retour client imputable** | % de retours clients traces a un defaut fournisseur | < 0.1% | Trimestriel |
| **Score audit qualite** | Note de l'audit processus fournisseur (checklist standardisee) | > 80/100 | Annuel |
| **Certifications** | Maintien des certifications obligatoires (ISO, sectorielles) | 100% a jour | Annuel |

#### Cost (Cout)

| KPI | Definition | Cible typique | Frequence |
|---|---|---|---|
| **Competitivite prix** | Position prix vs benchmark marche ou panel | Top quartile | Annuel |
| **Respect conditions tarifaires** | % de factures conformes aux conditions contractuelles | > 98% | Mensuel |
| **Productivite annuelle** | Reduction de prix annuelle contractuelle ou obtenue | 2-5% par an | Annuel |
| **Cout total des litiges** | Montant des avoirs et penalites factures | < 0.5% du CA | Trimestriel |

#### Delivery (Livraison)

| KPI | Definition | Cible typique | Frequence |
|---|---|---|---|
| **OTD (On-Time Delivery)** | % de livraisons dans la fenetre de livraison promise | > 95% | Mensuel |
| **OTIF (On-Time In-Full)** | % de livraisons a l'heure ET en quantite complete | > 92% | Mensuel |
| **Lead time moyen** | Delai moyen commande-livraison | Selon contrat | Mensuel |
| **Lead time fiabilite** | Ecart-type du lead time (variabilite) | < 15% du LT moyen | Trimestriel |
| **Taux de rupture** | Nombre de ruptures d'approvisionnement par periode | 0 (cible) | Mensuel |

#### Responsiveness (Reactivite)

| KPI | Definition | Cible typique | Frequence |
|---|---|---|---|
| **Delai de reponse aux demandes** | Temps moyen de reponse aux sollicitations acheteur | < 24h | Mensuel |
| **Gestion des urgences** | Capacite a repondre aux commandes urgentes | Evaluation qualitative | Trimestriel |
| **Flexibilite volume** | Capacite a absorber des variations de volume (up et down) | +/- 20% sans preavis | Trimestriel |
| **Contribution a la resolution de problemes** | Proactivite dans l'analyse des causes racines et les actions correctives | Evaluation qualitative | Trimestriel |

#### Sustainability / CSR (RSE)

| KPI | Definition | Cible typique | Frequence |
|---|---|---|---|
| **Score EcoVadis** | Note EcoVadis du fournisseur (ou equivalent) | > 45/100 (Silver) | Annuel |
| **Emissions carbone** | Emissions CO2 par unite de produit livre (scope 1+2) | Trajectoire de reduction | Annuel |
| **Conformite sociale** | Respect des normes ILO, pas de travail force/enfants | 100% conformite | Annuel (audit) |
| **Diversite fournisseur** | % du panel issu de PME, ESS, entreprises inclusives | > 20% | Annuel |
| **Economie circulaire** | % de matieres recyclees, recyclabilite, emballages reemployables | Croissant | Annuel |

### Processus de revue de performance

#### Monthly Performance Review (categories critiques)
- Suivi automatise des KPIs Q, C, D via les donnees du systeme (ERP, WMS, QMS).
- Alerte automatique si un KPI passe en zone rouge (seuil predetermine).
- Action corrective demandee au fournisseur sous 48h pour tout incident critique.

#### Quarterly Business Review (QBR) — Fournisseurs strategiques
- Revue approfondie de tous les KPIs QCDRSE.
- Presentation par le fournisseur de ses plans d'action sur les axes d'amelioration.
- Discussion sur les opportunites d'innovation et de creation de valeur.
- Alignement des forecasts et des plans de capacite.
- Documentation formelle des decisions et des engagements mutuels.

#### Annual Business Review (ABR) — Fournisseurs strategiques
- Bilan annuel complet de la performance et de la relation.
- Revue de la strategie de sourcing pour la categorie.
- Partage des roadmaps strategiques (acheteur et fournisseur).
- Definition des objectifs de progres pour l'annee suivante.
- Decision de maintien, developpement, mise sous surveillance ou sortie du panel.

---

## Supplier Relationship Management (SRM)

### Segmentation des relations fournisseurs

Toutes les relations fournisseurs ne meritent pas le meme niveau d'investissement. Segmenter le panel fournisseur en 4 niveaux :

```
Niveau 1 — Partenaires strategiques (5-10% du panel, 40-50% des depenses)
   Relation : co-developpement, innovation conjointe, integration des systemes
   Gouvernance : Executive Sponsor, QBR + ABR, comites de pilotage conjoints
   Investissement SRM : eleve (ressources dediees)

Niveau 2 — Fournisseurs preferes (10-15% du panel, 30-35% des depenses)
   Relation : contrats-cadres pluriannuels, scorecards, plans de progres
   Gouvernance : Category Manager referent, QBR
   Investissement SRM : moyen

Niveau 3 — Fournisseurs approuves (20-30% du panel, 15-20% des depenses)
   Relation : contrats standards, evaluation periodique
   Gouvernance : suivi des KPIs automatise, revue annuelle
   Investissement SRM : faible

Niveau 4 — Fournisseurs ponctuels / Tail spend (50-60% du panel, 5-10% des depenses)
   Relation : commandes ponctuelles, catalogues, marketplaces
   Gouvernance : minimale, automatisee
   Investissement SRM : aucun (automatiser ou eliminer)
```

### Programme SRM — Composantes

#### 1. Governance Framework
- Definir les roles et responsabilites : Executive Sponsor (C-level), Relationship Owner (Category Manager), Operational Contact (acheteur operationnel).
- Formaliser les rituels de gouvernance par niveau de relation (calendrier des revues, format, participants, livrables).
- Etablir un escalation path clair en cas de probleme non resolu au niveau operationnel.

#### 2. Performance Management
- Deployer les scorecards par niveau de relation (voir section precedente).
- Automatiser la collecte des KPIs via integration systemes (ERP, WMS, QMS).
- Mettre en place un systeme d'alertes proactives.
- Definir les consequences de la performance : reward (volume additionnel, long terme) et remedy (plan d'action, penalites, desengagement).

#### 3. Collaboration & Innovation
- Organiser des Innovation Days avec les fournisseurs partenaires (presenter les challenges, recevoir des propositions).
- Mettre en place des programmes de co-developpement structure (gate process, IP sharing, partage des couts et benefices).
- Creer des cercles de partage de bonnes pratiques entre fournisseurs non concurrents.
- Integrer les fournisseurs partenaires dans les phases amont des projets (design-to-cost, design-to-value).

#### 4. Risk & Compliance (voir reference contract-risk.md)

---

## Supplier Development

### Quand developper un fournisseur

Le developpement fournisseur est un investissement significatif. Le justifier dans ces cas :

- Fournisseur strategique avec un potentiel sous-exploite (bon produit, processus ameliorables).
- Aucune alternative credible sur le marche (goulet d'etranglement).
- Volonte de creer un fournisseur local pour des raisons de proximite, RSE ou securite d'approvisionnement.
- Fournisseur innovant (startup, PME) necessitant un accompagnement pour scaler.

### Programme de developpement — Structure

#### Phase 1 — Diagnostic (4-6 semaines)
- Audit approfondi des processus du fournisseur (production, qualite, logistique, management).
- Identification des ecarts par rapport aux exigences et aux meilleures pratiques.
- Quantification des gains potentiels (qualite, cout, delai).
- Validation de l'engagement du fournisseur (direction generale impliquee).

#### Phase 2 — Plan d'action (co-construit)
- Definir les chantiers prioritaires avec des objectifs SMART.
- Allouer les ressources (experts techniques de l'acheteur, consultants, budget).
- Definir les jalons et les indicateurs de progres.
- Formaliser les engagements mutuels (ressources de l'acheteur vs investissements du fournisseur).

#### Phase 3 — Execution et accompagnement (6-18 mois)
- Deployer les experts sur site (resident engineers, kaizen workshops).
- Transferer les methodologies (Lean manufacturing, SPC, SMED, 5S, TPM).
- Organiser des revues de progres regulieres (mensuel minimum).
- Adapter le plan en fonction des resultats intermediaires.

#### Phase 4 — Perennisation et autonomie
- Verifier l'ancrage des ameliorations via un audit de cloture.
- Transferer la gouvernance au management du fournisseur.
- Definir les KPIs de suivi post-developpement.
- Capitaliser les enseignements pour les futurs programmes.

### Outils de developpement fournisseur

- **Lean Manufacturing** : 5S, VSM (Value Stream Mapping), SMED, Kanban, TPM.
- **Qualite** : SPC (Statistical Process Control), FMEA (Failure Mode and Effects Analysis), 8D, poka-yoke.
- **Logistique** : VMI (Vendor Managed Inventory), EDI, forecasting collaboratif.
- **Management** : coaching direction, aide a la structuration (ERP, QMS).

---

## Audits & Certifications

### Types d'audits fournisseurs

#### Audit de qualification initiale
- Objectif : valider la capacite du fournisseur a repondre aux exigences AVANT la premiere commande.
- Contenu : visite de site, revue des processus qualite et production, verification des capacites, evaluation des risques.
- Decision : qualifie, qualifie sous conditions (avec plan d'action), non qualifie.
- Frequence : une fois, avant le referencement.

#### Audit de suivi (surveillance)
- Objectif : verifier le maintien des conditions initiales de qualification.
- Contenu : revue des KPIs, verification des actions correctives, controle des certifications.
- Frequence : annuelle pour les fournisseurs strategiques, tous les 2-3 ans pour les autres.

#### Audit de processus
- Objectif : evaluation detaillee d'un processus specifique (production, logistique, qualite).
- Contenu : observation sur site, analyse des donnees, entretiens avec les operateurs.
- Methodologies : VDA 6.3 (automobile), HACCP (agroalimentaire), audit interne ISO 19011.
- Frequence : selon les besoins, souvent declenche par un probleme qualite.

#### Audit flash (non programme)
- Objectif : verification sans preavis, souvent declenchee par un incident ou un signal d'alerte.
- Contenu : cible (un aspect specifique), court (1/2 journee).
- Prevoir la possibilite contractuellement (clause d'audit).

#### Audit RSE / Social
- Objectif : verifier la conformite aux engagements sociaux et environnementaux.
- Referentiels : SA8000, SMETA (Sedex), BSCI (amfori), ISO 26000, checklist devoir de vigilance.
- Contenu : conditions de travail, sante-securite, environnement, ethique, sous-traitance.
- Frequence : annuelle pour les fournisseurs a risque RSE (pays a risque, secteurs sensibles).

### Certifications fournisseurs — Reference

#### Certifications qualite
- **ISO 9001** : systeme de management de la qualite. Exigence minimale universelle.
- **IATF 16949** : qualite automobile (integration ISO 9001 + exigences sectorielles).
- **AS 9100** : qualite aeronautique et defense.
- **ISO 13485** : qualite dispositifs medicaux.
- **ISO 22000 / FSSC 22000** : securite alimentaire.

#### Certifications environnementales
- **ISO 14001** : systeme de management environnemental.
- **ISO 50001** : management de l'energie.
- **EMAS** : eco-management and audit scheme (europeen, plus exigeant qu'ISO 14001).
- **Cradle to Cradle** : conception pour l'economie circulaire.

#### Certifications RSE
- **EcoVadis** : evaluation RSE en ligne (environnement, social, ethique, achats responsables). De facto standard en Europe.
- **B Corp** : certification d'entreprise a impact positif.
- **SA8000** : norme sociale basee sur les conventions ILO.
- **SBTi** : engagement de reduction carbone base sur la science.

#### Certifications securite de l'information
- **ISO 27001** : management de la securite de l'information. Indispensable pour les fournisseurs IT et services digitaux.
- **SOC 2** : controles de securite, disponibilite, confidentialite (standard americain, reconnu globalement).

---

## State of the Art (2024-2026)

### IA et Supplier Performance Prediction
L'intelligence artificielle permet de passer du suivi de performance reactif au predictif. Des algorithmes de machine learning analysent les donnees historiques de performance (qualite, delais, incidents), les donnees financieres (bilan, tresorerie, notation credit), les signaux faibles (actualites, reseaux sociaux, brevets) et les donnees macro-economiques pour predire les risques de degradation de performance AVANT qu'ils ne se materialisent. Les plateformes comme Resilinc, Prewave et Everstream Analytics offrent ces capacites. Integration dans les scorecards sous forme de "risk-adjusted performance score".

### Supplier Collaboration Platforms
Evolution des portails fournisseurs vers de veritables plateformes de collaboration temps reel. Au-dela du partage de commandes et factures, ces plateformes integrent le forecasting collaboratif, le partage de capacite, la gestion de projet conjointe, le co-design et le suivi qualite en temps reel. Les solutions comme Ivalua, SAP Business Network, et Coupa Supply Chain Design renforcent la transparence et la collaboration end-to-end.

### ESG-Integrated Supplier Management
La notation RSE des fournisseurs passe de "nice to have" a obligation reglementaire avec la directive CSRD (Corporate Sustainability Reporting Directive) en Europe et le devoir de vigilance (loi francaise 2017, directive CS3D europeenne en cours). Les entreprises doivent documenter leur processus d'evaluation RSE fournisseur, etablir des plans de progres et demontrer l'amelioration continue. EcoVadis atteint plus de 130 000 entreprises evaluees dans plus de 180 pays. Integration des criteres ESG dans les scorecards avec un poids croissant (objectif 20-25% d'ici 2026).

### Supplier Diversity & Inclusive Procurement
Les programmes de diversite fournisseur (achats aupres de PME, entreprises du secteur social et solidaire, entreprises dirigees par des minorites ou des femmes) se structurent en Europe apres avoir ete historiquement plus developpes aux USA. Les grands donneurs d'ordre definissent des objectifs chiffres de diversite dans leur panel fournisseur. Des plateformes comme ConnXus, Supplier.io et TealBook facilitent l'identification et le suivi des fournisseurs diversifies.

### Continuous Supplier Monitoring
Fin du modele d'evaluation periodique (annuelle) au profit d'un monitoring continu. Les plateformes SRM modernes integrent des flux de donnees en temps reel : alertes financieres (Altares, Coface, CreditSafe), actualites et reputation (Prewave, Dataminr), conformite reglementaire (sanctions lists, PEP databases), cybersecurite (SecurityScorecard, BitSight). Les scores de risque sont recalcules quotidiennement et les alertes sont routees automatiquement aux category managers concernes.

### Digital Twins of Supply Chain
Certaines grandes entreprises commencent a creer des jumeaux numeriques de leur chaine d'approvisionnement, incluant la modelisation des capacites, des flux et des risques fournisseurs. Ces modeles permettent de simuler l'impact d'une perturbation (defaillance fournisseur, catastrophe naturelle, crise logistique) et d'optimiser les decisions de sourcing en temps reel. Technologies : simulation discrete, optimization, graph analytics.

### Supplier Onboarding Automation
Les processus d'onboarding fournisseur (referencement, collecte de documents, verification de conformite) sont de plus en plus automatises. Les plateformes combinent RPA (Robotic Process Automation) pour la collecte de donnees, OCR et NLP pour l'analyse de documents, API pour la verification automatique (registres legaux, listes de sanctions, scores de credit). Un onboarding qui prenait 4-6 semaines peut etre reduit a 3-5 jours pour les cas standards.
