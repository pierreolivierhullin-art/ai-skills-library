# AI Regulatory Frameworks — EU AI Act, NIST AI RMF, ISO 42001 & International Landscape

## Overview

Ce document de reference couvre les principaux cadres reglementaires et normatifs de l'IA : le reglement europeen sur l'intelligence artificielle (EU AI Act), le NIST AI Risk Management Framework, la norme ISO/IEC 42001, les reglementations sectorielles et le paysage international de la gouvernance IA. Utiliser ce guide pour comprendre les obligations legales, concevoir un programme de conformite proportionnee et anticiper les evolutions reglementaires. Ce document reflete l'etat du paysage reglementaire jusqu'en debut 2026.

---

## EU AI Act — Reglement Europeen sur l'IA

### Contexte et calendrier

Le reglement europeen sur l'intelligence artificielle (EU AI Act, Reglement (UE) 2024/1689) est le premier cadre juridique complet au monde regulant l'IA. Adopte en mars 2024, entre en vigueur le 1er aout 2024, il s'applique progressivement :

| Date | Etape |
|---|---|
| **1er aout 2024** | Entree en vigueur |
| **2 fevrier 2025** | Interdictions (pratiques IA inacceptables) applicables |
| **2 aout 2025** | Obligations pour les modeles a usage general (GPAI) applicables ; designation des autorites nationales |
| **2 aout 2026** | Obligations pour les systemes a haut risque (Annexe III) applicables |
| **2 aout 2027** | Obligations pour les systemes a haut risque integres dans des produits reglementes (Annexe I) applicables |

### Classification des risques

Le EU AI Act adopte une approche fondee sur les risques avec quatre niveaux :

#### Niveau 1 — Risque inacceptable (INTERDIT)

Systemes IA dont l'utilisation est interdite dans l'UE :

- **Manipulation subliminale** : systemes utilisant des techniques subliminales pour alterer le comportement d'une personne de maniere prejudiciable.
- **Exploitation de vulnerabilites** : systemes exploitant les vulnerabilites liees a l'age, au handicap ou a la situation sociale.
- **Social scoring** : systemes d'evaluation sociale par les autorites publiques conduisant a un traitement defavorable injustifie.
- **Identification biometrique en temps reel** dans les espaces publics a des fins repressives (avec des exceptions strictement encadrees pour les forces de l'ordre).
- **Categorisation biometrique** basee sur des donnees sensibles (race, opinions politiques, orientation sexuelle, croyances).
- **Scraping non cible d'images faciales** pour constituer des bases de reconnaissance faciale.
- **Inference d'emotions** sur le lieu de travail et dans les etablissements d'enseignement (avec exceptions limitees).
- **Policing predictif** base uniquement sur le profilage d'une personne.

#### Niveau 2 — Haut risque

Systemes IA soumis a des obligations renforcees avant mise sur le marche et tout au long de leur cycle de vie. Deux categories :

**Annexe I** — Systemes IA integres dans des produits reglementes :
- Dispositifs medicaux, machines, jouets, equipements radio, aviation civile, vehicules, ascenseurs, equipements sous pression.
- Soumis aux legislations d'harmonisation existantes + exigences supplementaires du AI Act.

**Annexe III** — Systemes IA autonomes a haut risque :
1. **Identification biometrique** (a distance, non en temps reel).
2. **Gestion d'infrastructures critiques** (eau, gaz, electricite, transport, numerique).
3. **Education et formation** (acces, evaluation, detection de triche).
4. **Emploi et gestion du personnel** (recrutement, evaluation, promotion, licenciement).
5. **Acces aux services essentiels** (credit, assurance, services publics, secours).
6. **Repression** (evaluation de risque, detection de crimes, profilage dans le cadre d'enquetes).
7. **Gestion de la migration et controle aux frontieres** (evaluation de risque, authentification de documents).
8. **Administration de la justice** (recherche juridique, application de la loi aux faits).

**Obligations pour les systemes a haut risque** :

| Obligation | Description |
|---|---|
| **Systeme de gestion des risques** | Evaluation continue des risques, mesures d'attenuation, documentation |
| **Gouvernance des donnees** | Qualite, representativite, biais, pertinence des donnees d'entrainement |
| **Documentation technique** | Description detaillee du systeme, de ses performances et de ses limites |
| **Tenue de registres (logging)** | Tracabilite automatique des operations du systeme |
| **Transparence** | Instructions d'utilisation claires pour les deployers |
| **Controle humain** | Capacite d'intervention humaine, arret d'urgence |
| **Exactitude, robustesse, securite** | Metriques de performance, resilience aux erreurs et aux attaques |
| **Evaluation de conformite** | Auto-evaluation ou evaluation par un tiers (selon le domaine) |
| **Enregistrement dans la base de donnees UE** | Enregistrement avant la mise sur le marche |
| **Monitoring post-marche** | Surveillance continue apres le deploiement |

#### Niveau 3 — Risque limite

Systemes IA soumis a des obligations de transparence specifiques :

- **Chatbots / systemes conversationnels** : informer l'utilisateur qu'il interagit avec un systeme IA.
- **Deepfakes / contenu genere par IA** : marquer le contenu comme genere artificiellement.
- **Systemes de reconnaissance d'emotions** : informer les personnes concernees.
- **Systemes de categorisation biometrique** : informer les personnes concernees.

#### Niveau 4 — Risque minimal

Tous les autres systemes IA. Pas d'obligations specifiques au-dela du droit commun. Encouragement a adopter volontairement des codes de conduite.

### General-Purpose AI Models (GPAI) — Modeles a usage general

Le EU AI Act introduit des obligations specifiques pour les **fournisseurs** de modeles a usage general (foundation models, LLM) :

#### Obligations pour tous les modeles GPAI

- **Documentation technique** : description du modele, capacites, limites, processus d'entrainement.
- **Politique de respect du droit d'auteur** : conformite a la directive copyright, transparence sur les donnees d'entrainement.
- **Mise a disposition d'un resume des donnees d'entrainement** : suffisamment detaille pour comprendre la provenance.
- **Cooperation avec les autorites** : repondre aux demandes d'information.

#### Obligations supplementaires pour les modeles GPAI a risque systemique

Un modele GPAI est considere a risque systemique si sa puissance de calcul d'entrainement depasse 10^25 FLOPS (seuil ajustable) ou si la Commission le designe comme tel.

Obligations supplementaires :
- **Evaluation du modele** : evaluations standardisees incluant le red teaming adversarial.
- **Evaluation et attenuation des risques systemiques** : identification proactive et attenuation.
- **Signalement d'incidents graves** : notification a la Commission et aux autorites nationales.
- **Cybersecurite** : protection adequate du modele et de son infrastructure.

### Mise en conformite — Guide pratique

#### Etape 1 : Inventaire des systemes IA

Realiser un inventaire exhaustif de tous les systemes IA deployes ou en developpement dans l'organisation. Pour chaque systeme :
- Description fonctionnelle et technique.
- Donnees utilisees (entrainement et inference).
- Cas d'usage et contexte de deploiement.
- Classification de risque (inacceptable, haut, limite, minimal).

#### Etape 2 : Classification des risques

Pour chaque systeme, determiner le niveau de risque :
1. Verifier si le systeme tombe dans les categories interdites (risque inacceptable).
2. Verifier si le systeme est couvert par l'Annexe I ou l'Annexe III (haut risque).
3. Verifier si des obligations de transparence s'appliquent (risque limite).
4. Par defaut, le systeme est a risque minimal.

**Attention** : la classification depend du **cas d'usage** et du **contexte de deploiement**, pas uniquement de la technologie. Un meme modele ML peut etre a risque minimal dans un contexte et a haut risque dans un autre.

#### Etape 3 : Plan de conformite

Pour les systemes a haut risque, etablir un plan de conformite couvrant les 10 obligations. Prioriser :
1. Systeme de gestion des risques (fondation de la conformite).
2. Documentation technique (base de la transparence).
3. Gouvernance des donnees (qualite et biais).
4. Logging et tracabilite (prerequis pour le monitoring).
5. Controle humain (mecanismes d'intervention).

#### Etape 4 : Implementation et monitoring

- Integrer les exigences dans le pipeline MLOps (model cards, logging, monitoring, drift detection).
- Automatiser autant que possible les controles de conformite.
- Mettre en place un monitoring post-marche continu.
- Preparer les dossiers d'evaluation de conformite.

### Sanctions

| Type de violation | Amende maximale |
|---|---|
| Systemes IA interdits | 35M EUR ou 7% du CA mondial |
| Non-conformite des systemes a haut risque | 15M EUR ou 3% du CA mondial |
| Information incorrecte aux autorites | 7.5M EUR ou 1.5% du CA mondial |

Pour les PME et startups, les amendes sont calculees proportionnellement (le montant le plus bas s'applique).

---

## NIST AI Risk Management Framework (AI RMF)

### Presentation

Le NIST AI Risk Management Framework (AI RMF 1.0, janvier 2023, avec des mises a jour continues) est un cadre volontaire developpe par le National Institute of Standards and Technology (USA) pour aider les organisations a gerer les risques lies a l'IA. Bien que non contraignant legalement, il est devenu une reference internationale et est souvent exige dans les marches publics americains.

### Les 4 fonctions du AI RMF

Le framework est structure autour de quatre fonctions complementaires :

#### GOVERN — Gouverner

Etablir et maintenir les structures organisationnelles, les politiques et les processus de gouvernance de l'IA.

**Activites cles** :
- Definir la politique IA de l'organisation (principes, limites, responsabilites).
- Etablir les roles et responsabilites de la gouvernance IA.
- Aligner la gouvernance IA sur le risk management global de l'organisation.
- Definir les processus de decision et d'escalade.
- Integrer la culture de gestion des risques IA a tous les niveaux.

**Categories** :
- GOVERN 1 : Politiques, processus, procedures et pratiques.
- GOVERN 2 : Accountability structures.
- GOVERN 3 : Workforce diversity, equity, inclusion.
- GOVERN 4 : Organizational culture.
- GOVERN 5 : AI system engagement with communities.
- GOVERN 6 : Risk management policies and procedures.

#### MAP — Cartographier

Identifier et comprendre le contexte d'utilisation du systeme IA et les risques associes.

**Activites cles** :
- Definir le contexte d'utilisation (qui, pourquoi, comment, ou).
- Identifier les parties prenantes impactees (directement et indirectement).
- Evaluer les benefices attendus et les risques potentiels.
- Documenter les limites connues du systeme.
- Evaluer les biais potentiels dans les donnees et le modele.

**Categories** :
- MAP 1 : Context is established and understood.
- MAP 2 : Categorization of the AI system.
- MAP 3 : AI risks and benefits are identified.
- MAP 4 : Risks are prioritized.
- MAP 5 : Impacts to individuals, communities, organizations are characterized.

#### MEASURE — Mesurer

Quantifier les risques identifies, evaluer les performances et les impacts du systeme IA.

**Activites cles** :
- Definir les metriques d'evaluation (performance, equite, robustesse, securite).
- Evaluer les biais et l'equite (demographic parity, equalized odds).
- Tester la robustesse (adversarial testing, edge cases).
- Mesurer la transparence et l'explicabilite.
- Evaluer la securite et la resilience.
- Documenter les resultats et les comparer aux seuils definis.

**Categories** :
- MEASURE 1 : Appropriate methods and metrics are identified and applied.
- MEASURE 2 : AI systems are evaluated for trustworthy characteristics.
- MEASURE 3 : Mechanisms for tracking identified AI risks over time.
- MEASURE 4 : Feedback about efficacy of measurement.

#### MANAGE — Gerer

Traiter les risques identifies en deployant des mesures d'attenuation, de monitoring et de reponse.

**Activites cles** :
- Prioriser les risques selon leur severite et probabilite.
- Deployer les mesures d'attenuation (techniques, organisationnelles, contractuelles).
- Mettre en place le monitoring continu des risques.
- Definir les plans de reponse aux incidents IA.
- Communiquer les risques residuels aux parties prenantes.

**Categories** :
- MANAGE 1 : AI risks based on assessments are prioritized, responded to, and managed.
- MANAGE 2 : Plans for maximizing benefits and minimizing negative impacts.
- MANAGE 3 : AI risks are managed and monitored post-deployment.
- MANAGE 4 : Risk treatments and residual risks are communicated.

### AI RMF Profiles

Le NIST a publie des profils specifiques pour guider l'implementation du AI RMF dans des contextes particuliers :

- **Generative AI Profile (NIST AI 600-1, 2024)** : profil specifique pour les risques des systemes d'IA generative, couvrant 12 risques cles (CBRN, confabulation/hallucination, data privacy, environmental, information integrity, information security, intellectual property, obscene/abusive content, value chain risks, etc.).
- **AI RMF Playbook** : guide pratique avec des actions suggerees pour chaque sous-categorie du framework.
- **Crosswalks** : correspondances entre le AI RMF et d'autres standards (ISO 42001, EU AI Act, OECD AI Principles).

### Utilisation pratique du AI RMF

Le AI RMF est un cadre flexible, pas une checklist. Approche recommandee :

1. **Evaluation du contexte** (MAP) : commencer par comprendre le systeme, ses utilisateurs et ses impacts.
2. **Definition de la gouvernance** (GOVERN) : etablir les structures et les politiques avant de deployer.
3. **Mesure des risques** (MEASURE) : evaluer quantitativement les risques identifies.
4. **Gestion des risques** (MANAGE) : deployer les mesures d'attenuation et le monitoring.
5. **Iteration continue** : les quatre fonctions s'executent en continu, pas sequentiellement.

---

## ISO/IEC 42001 — Systeme de Management de l'IA

### Presentation

ISO/IEC 42001:2023 est la premiere norme internationale pour les systemes de management de l'intelligence artificielle (AIMS — Artificial Intelligence Management System). Publiee en decembre 2023, elle fournit un cadre pour les organisations qui developpent, fournissent ou utilisent des systemes IA.

### Structure (basee sur le cadre HLS — High Level Structure)

Comme les autres normes de management ISO (ISO 27001, ISO 9001), ISO 42001 suit la structure de haut niveau (HLS) :

| Clause | Titre | Contenu |
|---|---|---|
| **4** | Contexte de l'organisation | Comprendre l'organisation, les parties interessees, le perimetre du AIMS |
| **5** | Leadership | Engagement de la direction, politique IA, roles et responsabilites |
| **6** | Planification | Identification des risques et opportunites, objectifs IA, planification des actions |
| **7** | Support | Ressources, competences, sensibilisation, communication, documentation |
| **8** | Operations | Planification operationnelle, evaluation d'impact IA, gestion du cycle de vie |
| **9** | Evaluation de la performance | Monitoring, mesure, analyse, evaluation, audit interne, revue de direction |
| **10** | Amelioration | Non-conformites, actions correctives, amelioration continue |

### Annexe A — Controles de reference

L'Annexe A de ISO 42001 definit 38 controles repartis en themes :

| Theme | Exemples de controles |
|---|---|
| **Politiques IA** | Politique d'utilisation de l'IA, politique de donnees |
| **Organisation interne** | Roles et responsabilites, separation des taches |
| **Ressources** | Competences, sensibilisation, formation |
| **Evaluation d'impact** | Evaluation d'impact IA, evaluation des risques, equite |
| **Cycle de vie du systeme IA** | Specification, design, verification, validation, deploiement, monitoring |
| **Donnees** | Qualite, provenance, biais, consentement, protection |
| **Transparence et explicabilite** | Documentation, information des parties prenantes, explicabilite |
| **Fournisseurs et tiers** | Due diligence, contrats, monitoring des fournisseurs |

### Certification ISO 42001

La certification ISO 42001 est delivree par des organismes de certification accredites. Processus :

1. **Gap analysis** : evaluation de l'ecart entre les pratiques actuelles et les exigences de la norme.
2. **Implementation** : mise en place du AIMS (politiques, processus, controles, documentation).
3. **Audit interne** : verification interne de la conformite.
4. **Audit de certification** :
   - Stage 1 : revue documentaire (politique, perimetre, documentation).
   - Stage 2 : audit sur site (verification de l'implementation effective).
5. **Certification** : delivrance du certificat (valide 3 ans).
6. **Audits de surveillance** : audits annuels de suivi.
7. **Re-certification** : tous les 3 ans.

### Benefices de ISO 42001

- **Confiance** : signal de confiance pour les clients, partenaires et regulateurs.
- **Structure** : cadre systematique pour la gestion de l'IA.
- **Conformite** : preparation a la conformite EU AI Act (les systemes de management ISO 42001 peuvent servir de base pour satisfaire les exigences du AI Act).
- **Amelioration continue** : le cycle PDCA (Plan-Do-Check-Act) assure une amelioration continue.
- **Interoperabilite** : integrable avec d'autres systemes de management (ISO 27001 pour la securite, ISO 9001 pour la qualite).

---

## Reglementations sectorielles

### Finance et banque

| Reglementation | Juridiction | Impact IA |
|---|---|---|
| **SR 11-7 (OCC/Fed)** | USA | Gouvernance des modeles (model risk management), validation, monitoring |
| **SS1/23 (PRA)** | UK | Model risk management pour les banques, exigences de gouvernance |
| **EBA Guidelines on ML for IRB** | EU | Encadrement de l'utilisation du ML pour le calcul du risque de credit |
| **DORA** | EU | Resilience numerique, incluant les systemes IA dans le perimetre |
| **MiFID II** | EU | Transparence algorithmique pour le trading algorithmique |

**Implications** : dans le secteur financier, chaque modele (y compris ML) est soumis a des exigences de validation independante, de documentation, de monitoring et d'audit. Le SR 11-7 (USA) et son equivalent europeen exigent un inventaire complet des modeles, une validation avant deploiement et un monitoring continu.

### Sante et pharma

| Reglementation | Juridiction | Impact IA |
|---|---|---|
| **MDR / IVDR** | EU | Dispositifs medicaux IA (SaMD), evaluation clinique, marquage CE |
| **FDA AI/ML SaMD Framework** | USA | Cadre pour les logiciels medicaux utilisant l'IA, pre-determined change control plan |
| **HIPAA** | USA | Protection des donnees de sante, impacte les donnees d'entrainement et d'inference |

**Implications** : les systemes IA utilises dans un contexte medical (diagnostic, aide a la prescription, imagerie) sont classifies comme dispositifs medicaux et soumis a des processus d'evaluation clinique rigoureux. Le concept de "predetermined change control plan" (FDA) permet des mises a jour de modeles pre-approuvees sous conditions strictes.

### Assurance

| Reglementation | Juridiction | Impact IA |
|---|---|---|
| **Solvency II** | EU | Gouvernance des modeles actuariels et de tarification |
| **Colorado AI Act** | USA (Colorado) | Obligations pour les deployers de systemes IA a haut risque en assurance |
| **EIOPA Guidelines** | EU | Principes d'ethique pour l'IA en assurance |

### Protection des donnees (transversal)

| Reglementation | Juridiction | Impact IA |
|---|---|---|
| **RGPD / GDPR** | EU | Base legale pour le traitement, PIA, droits des personnes, transferts |
| **CCPA / CPRA** | USA (Californie) | Droits des consommateurs, opt-out du profilage automatise |
| **PIPL** | Chine | Protection des donnees personnelles, consentement, localisation |

**Implications RGPD pour l'IA** :
- **Base legale** : consentement, interet legitime, execution d'un contrat ou obligation legale pour l'entrainement de modeles sur des donnees personnelles.
- **Article 22** : droit de ne pas faire l'objet d'une decision fondee exclusivement sur un traitement automatise (avec exceptions). Si un modele IA prend des decisions automatisees impactant des individus, des garde-fous sont obligatoires.
- **PIA (Privacy Impact Assessment)** : obligatoire pour les traitements a risque eleve (profilage, surveillance, donnees sensibles).
- **Droit a l'explication** : bien que non explicitement formule, derive de la combinaison des articles 13-15 (information), 22 (decision automatisee) et du principe de transparence.
- **Minimisation des donnees** : ne collecter et traiter que les donnees strictement necessaires a la finalite.

---

## Paysage international de la gouvernance IA

### Comparaison des approches regulatoires

| Region/Pays | Approche | Instrument principal | Caractéristiques |
|---|---|---|---|
| **Union Europeenne** | Reglementaire contraignante | EU AI Act (2024) | Approche par les risques, obligations strictes, amendes |
| **Etats-Unis** | Sectorielle + executive orders | Executive Order 14110 (2023), NIST AI RMF | Pas de loi federale unifiee, approche par agence sectorielle |
| **Royaume-Uni** | Pro-innovation | AI Regulation White Paper (2023) | Regulation par les regulateurs sectoriels existants, principes-based |
| **Chine** | Reglementaire ciblee | Regulations on GenAI (2023), Deep Synthesis (2023) | Reglementation specifique par technologie, controle du contenu |
| **Canada** | Legislative en cours | AIDA (Artificial Intelligence and Data Act) | Loi en discussion, approche par les risques |
| **Japon** | Soft law | AI Guidelines for Business (2024) | Approche volontaire, orientee innovation |
| **Singapour** | Governance framework | AI Verify, Model AI Governance Framework | Outil de test de gouvernance, framework volontaire |
| **Bresil** | Legislative en cours | AI Bill (en discussion) | Approche par les risques, inspiree du EU AI Act |

### Initiatives internationales

| Initiative | Organisation | Description |
|---|---|---|
| **OECD AI Principles** | OECD (2019, mis a jour 2024) | 5 principes pour une IA de confiance, adoptes par 46 pays |
| **G7 Hiroshima Process** | G7 (2023-2024) | Code de conduite pour les developeurs d'IA avancee, guiding principles |
| **UN AI Advisory Body** | ONU (2023-2024) | Recommandations pour la gouvernance internationale de l'IA |
| **Global Partnership on AI (GPAI)** | 29 pays | Recherche et collaboration sur l'IA responsable |
| **AI Safety Summit** | UK puis international | Sommets internationaux sur la securite de l'IA (Bletchley, Seoul, Paris) |
| **AI Seoul Declaration** | 28 pays + EU (2024) | Engagements sur la securite et la gouvernance de l'IA de frontiere |

### Tendances reglementaires 2025-2026

1. **Convergence vers l'approche par les risques** : la plupart des juridictions adoptent ou convergent vers une classification basee sur les risques, inspiree du EU AI Act.
2. **Focus sur la GenAI** : les regulateurs mondiaux publient des guidelines specifiques aux modeles generatifs et aux LLM (transparence, droits d'auteur, deepfakes).
3. **Obligations de transparence renforcees** : marquage du contenu genere par IA (watermarking, labels), explicabilite pour les decisions automatisees.
4. **Responsabilite et liability** : evolution vers une responsabilite produit pour les systemes IA (AI Liability Directive en discussion dans l'UE).
5. **Interoperabilite des frameworks** : efforts pour creer des correspondances (crosswalks) entre EU AI Act, NIST AI RMF, ISO 42001, et les frameworks nationaux.
6. **Regulation des agents IA autonomes** : premiers cadres pour reguler les systemes IA capables d'agir de maniere autonome (planification, execution, iteration).
7. **IA et durabilite** : emergence d'exigences de reporting sur l'impact environnemental de l'IA (empreinte carbone de l'entrainement et de l'inference).

---

## Guide pratique de conformite multi-frameworks

### Cartographie des correspondances

Les trois principaux frameworks (EU AI Act, NIST AI RMF, ISO 42001) sont complementaires. Voici les correspondances principales :

| EU AI Act (Haut risque) | NIST AI RMF | ISO 42001 |
|---|---|---|
| Systeme de gestion des risques | GOVERN + MAP | 6.1 (Actions pour traiter les risques) |
| Gouvernance des donnees | MAP 1-3, MEASURE 2 | 8.4 (Data for AI systems) |
| Documentation technique | MAP 1, MEASURE 1-2 | 7.5 (Documented information) |
| Tenue de registres (logging) | MANAGE 3 | 9.1 (Monitoring, measurement, analysis) |
| Transparence | GOVERN 1, MAP 5 | Annexe A.8 (Transparency) |
| Controle humain | MANAGE 2-4 | Annexe A.6 (Human oversight) |
| Exactitude, robustesse, securite | MEASURE 2, MANAGE 1 | 8.2-8.4 (Operational control) |
| Monitoring post-marche | MANAGE 3 | 9.1, 10 (Performance evaluation, Improvement) |

### Programme de conformite integre

Pour une organisation devant se conformer aux trois frameworks, l'approche recommandee est :

1. **ISO 42001 comme fondation** : implementer le systeme de management IA (AIMS) selon ISO 42001. Cela fournit la structure organisationnelle de base.
2. **NIST AI RMF comme methode** : utiliser les fonctions GOVERN/MAP/MEASURE/MANAGE du NIST AI RMF pour operationnaliser la gestion des risques IA au sein du AIMS.
3. **EU AI Act comme exigence legale** : mapper les obligations specifiques du AI Act sur les controles ISO 42001 et les activites NIST AI RMF pour assurer la conformite legale.

### Outillage de conformite (2024-2026)

| Outil | Type | Fonctionnalites |
|---|---|---|
| **Credo AI** | SaaS | Governance platform, policy packs (EU AI Act, NIST), model risk management |
| **Holistic AI** | SaaS | Compliance mapping, bias auditing, risk assessment |
| **IBM OpenPages** | Enterprise | GRC integre avec module IA, conformite multi-frameworks |
| **Monitaur** | SaaS | Model documentation, monitoring, audit trail |
| **AIVerify (Singapour)** | Open source | Testing toolkit pour la gouvernance IA, transparent |
| **Fiddler AI** | SaaS | Explainability, fairness, monitoring, compliance |
| **Arthur AI** | SaaS | Performance monitoring, bias detection, explainability |

### Checklist de conformite rapide

Pour chaque systeme IA deploye, verifier :

- [ ] Classification de risque EU AI Act determinee et documentee.
- [ ] Model Card complete (pour les systemes a haut risque et Tier 1-2).
- [ ] Donnees d'entrainement documentees (provenance, qualite, biais).
- [ ] Metriques de performance evaluees et documentees (y compris par sous-population).
- [ ] Mecanisme de controle humain en place (si requis).
- [ ] Logging et tracabilite actifs (predictions, donnees d'entree, versions).
- [ ] Monitoring en production configure (drift, performance, equite).
- [ ] Plan de re-entrainement ou de decommissionnement defini.
- [ ] Evaluation RGPD/PIA realisee (si donnees personnelles).
- [ ] Documentation technique a jour et accessible.
- [ ] Owner du modele identifie et responsable.
- [ ] Revue de conformite planifiee (frequence selon le tier).
