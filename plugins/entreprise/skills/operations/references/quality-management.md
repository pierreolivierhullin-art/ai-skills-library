# Quality Management — ISO 9001, TQM, Analyse de Causes Racines et SPC

## Overview

Ce document de reference couvre les systemes de management de la qualite, les methodologies d'amelioration continue, les techniques d'analyse de causes racines et la maitrise statistique des procedes. Il fournit les cadres normatifs, les outils pratiques et les approches de deploiement necessaires pour integrer la qualite dans chaque dimension de l'organisation. Utiliser ce guide pour structurer un systeme qualite robuste, de la conformite reglementaire a l'excellence operationnelle.

---

## ISO 9001:2015 — Systeme de Management de la Qualite

### Structure de la norme (High Level Structure — HLS)

La norme ISO 9001:2015 suit la structure HLS commune a toutes les normes ISO de systemes de management, facilitant l'integration avec ISO 14001 (environnement), ISO 45001 (sante-securite) et ISO 27001 (securite de l'information).

| Clause | Titre | Contenu cle |
|---|---|---|
| **4** | Contexte de l'organisation | Comprehension des enjeux internes/externes, parties interessees, perimetre du QMS |
| **5** | Leadership | Engagement de la direction, politique qualite, roles et responsabilites |
| **6** | Planification | Actions face aux risques et opportunites, objectifs qualite, planification des changements |
| **7** | Support | Ressources, competences, sensibilisation, communication, informations documentees |
| **8** | Realisation des activites operationnelles | Planification, exigences produit/service, conception, maitrise des prestataires externes, production, liberation, maitrise des elements non conformes |
| **9** | Evaluation des performances | Surveillance et mesure, satisfaction client, audit interne, revue de direction |
| **10** | Amelioration | Non-conformites et actions correctives, amelioration continue |

### Approche par les risques (Risk-Based Thinking)

L'edition 2015 de l'ISO 9001 introduit la pensee basee sur le risque comme principe fondamental (remplacement de l'ancien concept d'actions preventives) :

- **Identifier les risques et opportunites** (clause 6.1) a chaque niveau du QMS. Utiliser des outils comme l'AMDEC (FMEA), la matrice de risques ou l'analyse SWOT.
- **Integrer les actions dans les processus** : les actions face aux risques ne sont pas un processus separe mais sont integrees dans les processus operationnels.
- **Proportionnalite** : l'effort de gestion des risques est proportionne a l'impact potentiel. Pas d'obligation de processus formel de management des risques (contrairement a l'ISO 14971 pour le medical par exemple).

### Approche processus

Modeliser l'organisation comme un reseau de processus interconnectes. Chaque processus est decrit par :

- **Entrees** : ce dont le processus a besoin pour fonctionner.
- **Sorties** : ce que le processus produit (pour le processus suivant ou le client final).
- **Responsable de processus (Process Owner)** : la personne accountable de la performance du processus.
- **Indicateurs de performance** : KPI mesurant l'efficacite (atteinte des resultats) et l'efficience (ressources utilisees).
- **Risques et opportunites** : identifies et traites.

#### Typologie des processus

- **Processus de realisation (operationnels)** : creent directement la valeur pour le client (production, livraison, service).
- **Processus de management** : orientent et pilotent l'organisation (planification strategique, revue de direction, communication interne).
- **Processus de support** : fournissent les ressources necessaires aux processus de realisation (RH, maintenance, IT, achats).

### Audit interne (clause 9.2)

L'audit interne est un outil de verification et d'amelioration du QMS :

#### Planification des audits

- **Programme d'audit** : planifier les audits sur l'annee en couvrant tous les processus du QMS. Ajuster la frequence selon les risques, les performances passees et les changements recents.
- **Independance de l'auditeur** : l'auditeur ne doit pas auditer son propre travail. Dans les petites organisations, utiliser des audits croises entre departements.
- **Competence de l'auditeur** : formation aux techniques d'audit (ISO 19011), connaissance de la norme et du domaine audite.

#### Conduite de l'audit

1. **Reunion d'ouverture** : confirmer le scope, le planning et les criteres.
2. **Collecte de preuves** : entretiens, observation, revue de documents et d'enregistrements. La methode est factuelle : "Montrez-moi", "Comment savez-vous que...".
3. **Constats** : classer les ecarts en non-conformites majeures (systeme defaillant), mineures (ecart ponctuel) et opportunites d'amelioration.
4. **Reunion de cloture** : presenter les constats, s'assurer de leur comprehension.
5. **Suivi** : les actions correctives doivent traiter la cause racine, pas seulement le symptome. Verifier l'efficacite des actions.

---

## Total Quality Management (TQM)

### Principes fondamentaux du TQM

Le TQM est une philosophie de management globale qui integre la qualite dans toutes les fonctions et a tous les niveaux de l'organisation. Les 8 principes :

1. **Orientation client** : comprendre les besoins actuels et futurs du client, satisfaire ses exigences et s'efforcer d'aller au-dela de ses attentes.
2. **Leadership** : la direction cree un environnement dans lequel les personnes s'impliquent dans l'atteinte des objectifs qualite.
3. **Implication du personnel** : les personnes a tous les niveaux sont l'essence de l'organisation. Leur implication permet d'utiliser pleinement leurs competences.
4. **Approche processus** : gerer les activites comme des processus interconnectes.
5. **Amelioration continue** : l'amelioration continue est un objectif permanent.
6. **Prise de decision fondee sur des preuves** : les decisions efficaces sont basees sur l'analyse de donnees et d'informations.
7. **Management des relations** : gerer les relations avec les parties interessees (fournisseurs, partenaires) pour optimiser la performance globale.
8. **Approche systemique** : identifier, comprendre et gerer des processus correles comme un systeme.

### Cost of Quality (CoQ)

Le cout de la qualite est un levier puissant pour justifier les investissements qualite :

| Categorie | Description | Exemples | % typique du CA |
|---|---|---|---|
| **Prevention** | Investissements pour empecher les defauts | Formation, design review, FMEA, Poka-Yoke, process validation | 1-5% |
| **Detection (Evaluation)** | Couts de verification et de controle | Inspection, tests, audit, calibration, controle qualite entrant | 2-5% |
| **Defaillances internes** | Couts des defauts detectes avant livraison | Rebut, retouche, re-test, tri, temps d'arret | 5-15% |
| **Defaillances externes** | Couts des defauts detectes par le client | Retours, garantie, rappels, reclamations, litiges, perte de reputation | 5-20% |

**Regle empirique** : le cout de detection d'un defaut est multiplie par 10 a chaque etape de la chaine de valeur (regle du 1-10-100). Investir dans la prevention est toujours plus rentable que detecter ou corriger.

---

## Amelioration Continue — PDCA, A3, 8D

### Cycle PDCA (Roue de Deming)

Le PDCA est le cycle fondamental de l'amelioration continue :

#### Plan (Planifier)
- Identifier le probleme ou l'opportunite d'amelioration.
- Analyser la situation actuelle (donnees, observation).
- Identifier les causes racines.
- Definir l'objectif d'amelioration (SMART).
- Concevoir les solutions et le plan de mise en oeuvre.

#### Do (Realiser)
- Mettre en oeuvre les solutions a petite echelle (pilote).
- Collecter les donnees de performance pendant le pilote.
- Documenter les ecarts et les observations.

#### Check (Verifier)
- Comparer les resultats du pilote avec l'objectif.
- Analyser les ecarts (positifs et negatifs).
- Identifier les ajustements necessaires.

#### Act (Agir)
- Si les resultats sont positifs : standardiser la solution, la deployer a plus grande echelle.
- Si les resultats sont insuffisants : ajuster la solution et relancer un cycle PDCA.
- Documenter les apprentissages.
- Identifier le prochain sujet d'amelioration.

### Methode 8D (Eight Disciplines)

La methode 8D est une approche structuree de resolution de problemes, particulierement utilisee dans l'industrie automobile (origine Ford) :

| Discipline | Action | Livrable |
|---|---|---|
| **D0 — Preparation** | Evaluer la necessite d'un 8D (severite, recurrence). Collecter les donnees initiales. | Decision Go/No-Go, donnees de base |
| **D1 — Constituer l'equipe** | Former une equipe pluridisciplinaire avec les competences necessaires. | Equipe nommee, champion designe |
| **D2 — Decrire le probleme** | Decrire le probleme de maniere precise et factuelle (IS / IS NOT). | Description 5W2H du probleme |
| **D3 — Actions de confinement** | Mettre en place des actions immediates pour proteger le client. Trier, isoler, controler 100%. | Actions de confinement deployes, client protege |
| **D4 — Identifier les causes racines** | Utiliser Ishikawa, 5 Whys, arbre de defaillance. Verifier chaque cause potentielle avec des donnees. | Causes racines verifiees |
| **D5 — Choisir les actions correctives** | Selectionner les actions permanentes qui eliminent les causes racines. Verifier qu'elles n'ont pas d'effets secondaires. | Actions correctives validees |
| **D6 — Implementer et valider** | Deployer les actions correctives permanentes. Retirer les actions de confinement. Valider l'efficacite. | Actions deployees, efficacite confirmee |
| **D7 — Prevenir la recurrence** | Mettre a jour les standards, FMEA, control plans. Transversaliser les apprentissages. | Standards mis a jour, actions transversalisees |
| **D8 — Feliciter l'equipe** | Reconnaitre le travail de l'equipe. Capitaliser les apprentissages. | Cloture formelle, retour d'experience |

### QRQC (Quick Response Quality Control)

Le QRQC est une methode de resolution rapide de problemes qualite, structuree en 3 niveaux :

- **Niveau 1 — Ligne/Terrain** : traitement quotidien des problemes sur le poste de travail. San Gen Shugi ("les 3 reels") : aller sur le lieu reel (Gemba), regarder l'objet reel (Genbutsu), se baser sur les faits reels (Genjitsu).
- **Niveau 2 — Atelier/Service** : escalade des problemes non resolus au niveau 1. Analyse 8D simplifiee, actions correctives sous 5 jours.
- **Niveau 3 — Usine/Direction** : problemes recurrents ou a fort impact. 8D complet, analyse systemique.

---

## Root Cause Analysis — Outils d'Analyse de Causes Racines

### Diagramme d'Ishikawa (Fishbone / Cause-and-Effect)

#### Methode de construction

1. Placer l'effet (le probleme) a droite du diagramme.
2. Tracer les aretes principales par categorie. Utiliser les 6M pour les processus industriels ou les 5P pour les services :

**6M (Industrie)** :
- **Matiere** : matieres premieres, composants, consommables.
- **Machine** : equipements, outils, logiciels.
- **Main-d'oeuvre** : competences, formation, effectifs.
- **Methode** : procedures, instructions, standards.
- **Milieu** : environnement, temperature, humidite, proprete.
- **Mesure** : instruments, methodes de mesure, calibration.

**5P (Services)** :
- **People** : competences, motivation, staffing.
- **Process** : workflow, procedures, systemes.
- **Place** : lieu, environnement physique ou digital.
- **Provisions** : fournitures, outils, donnees.
- **Patrons** : management, politiques, culture.

3. Brainstormer les causes potentielles par categorie.
4. Pour chaque cause potentielle, demander "Pourquoi ?" pour approfondir.
5. Verifier chaque cause avec des donnees avant de conclure.

### Analyse 5 Whys (5 Pourquoi)

#### Regles pour un 5 Whys efficace

1. **Partir du fait observe** : ne pas partir d'une interpretation mais d'un fait verifiable.
2. **Verifier chaque "Pourquoi" avec des donnees** : ne pas accepter de reponse non verifiee.
3. **Ne pas s'arreter au premier "Pourquoi"** : la premiere reponse est rarement la cause racine.
4. **Eviter les boucles** : si une reponse ramene a une precedente, la chaine logique est brisee.
5. **Accepter les branches multiples** : un probleme peut avoir plusieurs causes racines. Suivre chaque branche.
6. **La cause racine est actionnable** : si on ne peut rien faire pour eliminer la cause identifiee, ce n'est pas la bonne cause racine (ou pas le bon niveau).

#### Exemple structure

```
Probleme : Le client a recu une commande incomplete.

Pourquoi 1 : Un article manquait dans le colis.
  --> Verification : controle du colis expedie (photo pre-expedition) confirme l'absence.

Pourquoi 2 : Le preparateur n'a pas mis l'article dans le colis.
  --> Verification : interview du preparateur, revue de la checklist de preparation.

Pourquoi 3 : L'article n'etait pas dans la zone de picking a ce moment-la.
  --> Verification : historique WMS, ecart de stock confirme sur cet emplacement.

Pourquoi 4 : Le reapprovisionnement de la zone de picking n'a pas ete declenche a temps.
  --> Verification : parametres du systeme de reapprovisionnement, seuil trop bas.

Pourquoi 5 : Le seuil de reapprovisionnement n'avait pas ete ajuste apres le changement de packaging (taille de contenant modifiee).
  --> Cause racine : processus de mise a jour des parametres WMS apres changement de packaging inexistant.
  --> Action corrective : creer une checklist de mise a jour des parametres WMS lors de tout changement de packaging. Integrer cette verification dans le processus de changement.
```

### Analyse de Pareto

L'analyse de Pareto (regle 80/20) permet de concentrer les efforts sur les causes ayant le plus d'impact :

1. Lister toutes les categories de defauts/problemes.
2. Compter la frequence (ou le cout) de chaque categorie.
3. Classer par ordre decroissant.
4. Calculer le pourcentage cumule.
5. Tracer le diagramme (barres + courbe cumulee).
6. Identifier le seuil 80% : les categories a gauche de ce seuil sont les priorites.

**Attention** : ne pas appliquer Pareto de maniere aveugle. Une cause rare mais a impact catastrophique (securite, legal) peut meriter la priorite meme si elle ne fait pas partie du "80%".

### Arbre de defaillance (Fault Tree Analysis — FTA)

L'arbre de defaillance est une analyse deductive (du sommet vers les causes) :

- **Evenement sommet** : le defaut ou l'incident a analyser.
- **Portes logiques** : AND (toutes les causes doivent etre presentes) et OR (une seule cause suffit).
- **Evenements de base** : les causes elementaires actionnables.

Utiliser le FTA pour les analyses de securite et de fiabilite, quand les interactions entre causes sont complexes.

---

## Statistical Process Control (SPC)

### Concepts fondamentaux

Le SPC utilise des outils statistiques pour surveiller et controler les processus en temps reel. L'objectif est de distinguer :

- **Causes communes (Common causes)** : variabilite inherente au processus, aleatoire et previsible. Agir sur les causes communes necessite un changement du processus lui-meme (design, equipement, methode).
- **Causes speciales (Special causes)** : variabilite exceptionnelle, identifiable et attribuable a un evenement specifique (panne, erreur operateur, lot de matiere non conforme). Eliminer les causes speciales par des actions correctives immediates.

### Cartes de controle

#### Types de cartes de controle

| Type | Donnees | Usage |
|---|---|---|
| **X-bar / R** | Continues, sous-groupes de 2-10 | Suivi de la moyenne et de l'etendue. Le plus courant en production. |
| **X-bar / S** | Continues, sous-groupes > 10 | Suivi de la moyenne et de l'ecart-type. Plus precis pour grands echantillons. |
| **I-MR (Individual / Moving Range)** | Continues, mesures individuelles | Quand chaque piece est unique ou le cout de mesure est eleve. |
| **p** | Attributs (proportion de defectueux) | Taux de defauts sur echantillons de taille variable. |
| **np** | Attributs (nombre de defectueux) | Nombre de defauts sur echantillons de taille constante. |
| **c** | Attributs (nombre de defauts) | Nombre de defauts par unite (taille constante). |
| **u** | Attributs (defauts par unite) | Nombre de defauts par unite (taille variable). |

#### Construction d'une carte de controle

1. **Collecter les donnees** : minimum 25 sous-groupes pour etablir les limites de controle.
2. **Calculer les limites** :
   - **Ligne centrale (CL)** : moyenne du processus.
   - **Limite de controle superieure (UCL)** : CL + 3 * sigma.
   - **Limite de controle inferieure (LCL)** : CL - 3 * sigma.
   - Les limites a +/- 3 sigma donnent une probabilite de 99.73% qu'un point soit a l'interieur si le processus est sous controle.
3. **Distinguer limites de controle et limites de specification** : les limites de controle sont la voix du processus (ce qu'il fait). Les limites de specification sont la voix du client (ce qu'il veut). Ne jamais utiliser les specifications comme limites de controle.

#### Regles de detection des causes speciales (Western Electric / Nelson)

Un processus est declare hors controle si :

- **Regle 1** : un point au-dela des limites de controle (> 3 sigma).
- **Regle 2** : 9 points consecutifs du meme cote de la ligne centrale (shift).
- **Regle 3** : 6 points consecutifs en progression croissante ou decroissante (trend).
- **Regle 4** : 14 points consecutifs alternant haut-bas (oscillation excessive).
- **Regle 5** : 2 points sur 3 consecutifs au-dela de 2 sigma (meme cote).
- **Regle 6** : 4 points sur 5 consecutifs au-dela de 1 sigma (meme cote).

### Process Capability (Capabilite du processus)

#### Indices de capabilite

- **Cp** = (USL - LSL) / (6 * sigma) : le processus est-il capable de respecter les specifications si il est centre ?
- **Cpk** = min((USL - X_bar) / (3 * sigma), (X_bar - LSL) / (3 * sigma)) : le processus respecte-t-il reellement les specifications (compte tenu du decentrage) ?
- **Pp / Ppk** : memes formules que Cp/Cpk mais calculees sur la totalite des donnees (performance globale vs capabilite court terme).

#### Interpretation

| Cpk | Interpretation | Action |
|---|---|---|
| < 1.0 | Processus non capable. Defauts > 2700 DPMO. | Action urgente : reduire la variabilite ou recentrer. |
| 1.0 - 1.33 | Processus marginalement capable. | Surveillance rapprochee, plan d'amelioration. |
| 1.33 - 1.67 | Processus capable. Standard acceptable. | Maintenir le controle, amelioration continue. |
| 1.67 - 2.0 | Processus tres capable. | Envisager de reduire la frequence de controle. |
| > 2.0 | Processus excellent. Six Sigma. | Benchmark, possibilite d'elargir les tolerances si besoin. |

### FMEA (Failure Mode and Effects Analysis)

#### Types de FMEA

- **DFMEA (Design FMEA)** : analyse des modes de defaillance lors de la conception du produit. Quand : pendant la phase de design, avant la production.
- **PFMEA (Process FMEA)** : analyse des modes de defaillance du processus de fabrication/service. Quand : avant le lancement en production, ou lors de la modification d'un processus.

#### Methode FMEA (version AIAG-VDA 2019)

La methode FMEA a ete mise a jour par le referentiel AIAG-VDA en 2019. Le RPN (Risk Priority Number) traditionnel est remplace par l'AP (Action Priority) :

1. **Structure Analysis** : decomposer le systeme/processus en elements.
2. **Function Analysis** : definir les fonctions de chaque element.
3. **Failure Analysis** : identifier les modes de defaillance, effets et causes.
4. **Risk Analysis** : evaluer la Severite (S), l'Occurrence (O) et la Detection (D) sur des echelles de 1 a 10.
5. **Optimization** : determiner l'Action Priority (High, Medium, Low) selon la matrice SOD et definir les actions d'amelioration.
6. **Results Documentation** : documenter les actions, responsables et resultats.

---

## State of the Art (2024-2026)

### Quality 4.0

Quality 4.0 est la convergence entre le management de la qualite et les technologies de l'Industrie 4.0 :

- **Predictive Quality** : utiliser le machine learning pour predire les defauts avant qu'ils ne surviennent, a partir des donnees processus temps reel (parametres machine, conditions environnementales, donnees matieres). Passer du SPC reactif au controle predictif.
- **AI-Driven Visual Inspection** : la vision par ordinateur (deep learning / computer vision) remplace l'inspection visuelle humaine pour les controles d'aspect, de dimensions et de conformite. Les modeles atteignent des taux de detection superieurs a l'inspection humaine (> 99.5% vs 80-90%) avec une repetabilite parfaite.
- **Connected Quality** : les donnees qualite (mesures, controles, non-conformites) sont integrees en temps reel dans un ecosysteme digital (QMS digital, MES, ERP, IoT), permettant une boucle de retour instantanee entre le controle et la production.
- **Digital Quality Management Systems** : les QMS papier ou bureautiques sont remplaces par des plateformes digitales (MasterControl, ETQ, Veeva QMS, Greenlight Guru) offrant workflows automatises, signatures electroniques, analyse de tendances et conformite reglementaire integree.

### Augmented Root Cause Analysis

L'analyse de causes racines est transformee par l'IA :

- **Automated Ishikawa Generation** : les systemes d'IA analysent les donnees historiques de non-conformite pour generer automatiquement des diagrammes d'Ishikawa avec les causes les plus probables classees par frequence et correlation.
- **Natural Language Processing (NLP) for Complaints** : les algorithmes NLP analysent les reclamations clients (texte libre) pour identifier les patterns, classer automatiquement les types de problemes et detecter les tendances emergentes.
- **Causal AI** : au-dela de la correlation, les algorithmes de causalite (do-calculus, DAGs) identifient les vraies relations de cause a effet dans les donnees de processus, evitant le piege de la correlation spurieuse.
- **Digital 8D** : les plateformes digitales guident les equipes a travers le processus 8D avec des templates intelligents, des suggestions basees sur les 8D precedents, et un suivi automatise des delais et de l'efficacite.

### Regulatory Evolution

L'environnement reglementaire evolue significativement :

- **ISO 9001 revision attendue** : la prochaine revision de l'ISO 9001 (prevue pour 2025-2026) devrait integrer des elements lies au changement climatique, a la diversite, a l'equite et a la transformation digitale, en alignement avec la Declaration de Londres de l'ISO.
- **EU AI Act et qualite** : l'AI Act europeen impose des exigences de qualite specifiques pour les systemes d'IA a haut risque (management des donnees, transparence, supervision humaine), creant de nouvelles exigences pour les QMS des organisations utilisant l'IA.
- **FDA CDER/CBER modernization** : la FDA americaine accelere l'adoption de la continuous manufacturing et du real-time release testing dans le pharma, s'appuyant sur des technologies PAT (Process Analytical Technology) et le controle statistique avance.

### Zero-Defect Manufacturing

L'approche zero defaut evolue d'un objectif aspirationnel vers une realite technologique :

- **In-Line 100% Inspection** : les capteurs et la vision par ordinateur permettent de controler 100% de la production en temps reel, eliminant le besoin d'echantillonnage statistique pour de nombreuses applications.
- **Closed-Loop Quality Control** : les donnees de controle alimentent directement les parametres de production en temps reel (feedback loop automatique). Si une derive est detectee, les parametres sont ajustes automatiquement avant que le defaut ne se produise.
- **Digital Thread** : la tracabilite numerique complete (de la matiere premiere au produit livre) permet de remonter instantanement a la source de tout probleme qualite et d'identifier tous les produits potentiellement affectes.

### Sustainability and Quality Integration

- **Environmental Quality Metrics** : integrer des indicateurs environnementaux dans le QMS (taux de dechets, consommation energetique par unite, emissions CO2 par produit).
- **Quality for Sustainability** : la reduction des defauts et des gaspillages est inheremment durable. Chaque defaut genere des dechets, consomme de l'energie et des matieres inutilement.
- **Circular Quality** : concevoir la qualite pour la durabilite, la reparabilite et la recyclabilite des produits (lien avec l'eco-conception et la reglementation europeenne sur la durabilite des produits).

### Exemples de KPI qualite modernes

```
Performance qualite :
- First Pass Yield (FPY) : cible > 99% (production), > 95% (services)
- Cost of Quality (CoQ) / Revenue : cible < 5% (benchmark world-class < 2%)
- DPMO (Defects Per Million Opportunities) : cible < 233 (5 sigma)
- Customer Complaint Rate : reduction YoY de 15%
- Return Rate : cible < 1%

Systeme qualite :
- Non-Conformite Closure Rate (sous 30 jours) : cible > 90%
- CAPA Effectiveness Rate : cible > 85%
- Audit Finding Close-Out : cible 100% dans les delais
- Supplier Quality Rating : cible > 95% des fournisseurs strategiques

SPC :
- % de processus sous controle statistique : cible > 90%
- Cpk moyen des processus critiques : cible > 1.33
- Taux de detection des causes speciales : cible > 95%

Quality 4.0 :
- % de controles automatises (vision, capteurs) : augmentation YoY
- Temps moyen de detection d'un defaut : reduction de 50%
- Taux de prediction correcte (predictive quality) : cible > 90%
- Digital maturity score du QMS : progression annuelle
```

### Ressources cles

- **ISO 9001:2015** : norme internationale pour les systemes de management de la qualite.
- **ISO 19011:2018** : lignes directrices pour l'audit des systemes de management.
- **AIAG-VDA FMEA Handbook** : reference pour la methode FMEA (edition 2019).
- **"Out of the Crisis"** (W. Edwards Deming) : les 14 points du management qualite.
- **"Quality Is Free"** (Philip Crosby) : la qualite comme investissement, pas comme cout.
- **ASQ Body of Knowledge** : reference pour les certifications qualite (CQE, CQA, CMQ/OE).
- **IATF 16949** : referentiel qualite specifique a l'industrie automobile.
