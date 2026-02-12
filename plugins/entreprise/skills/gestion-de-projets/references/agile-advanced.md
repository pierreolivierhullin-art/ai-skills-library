# Advanced Agile — Scaled Agile, Kanban Maturity, Design Thinking, Lean & Kaizen

## Overview

Ce document de reference couvre les pratiques agiles avancees et les approches d'agilite a l'echelle. Il detaille les frameworks scaled agile (Scrum@Scale, LeSS, Nexus, SAFe portfolio), le Kanban avance (flight levels, Kanban Maturity Model), le Design Thinking et le Design Sprint, ainsi que les methodes Lean (Kaizen, A3 Problem Solving, Value Stream Mapping). Utiliser ce guide pour deployer l'agilite au-dela d'une equipe unique et integrer les approches de decouverte et d'amelioration continue dans la culture organisationnelle.

---

## Scaled Agile Frameworks — Vue d'ensemble comparative

### Matrice de comparaison

| Critere | Scrum@Scale | LeSS | Nexus | SAFe |
|---|---|---|---|---|
| **Createur** | Jeff Sutherland | Craig Larman, Bas Vodde | Ken Schwaber | Dean Leffingwell |
| **Philosophie** | Scrum etendu via des cycles de coordination | Scrum minimaliste a l'echelle | Extension officielle de Scrum (Scrum.org) | Framework prescriptif et complet |
| **Equipes** | 2-2000+ | 2-8 (LeSS), 8+ (LeSS Huge) | 3-9 equipes Scrum | 50-500+ personnes |
| **Prescription** | Faible | Faible (anti-framework) | Moyenne | Elevee |
| **Roles ajoutes** | Scrum of Scrums Master, Chief PO | Minimal (pas de roles ajoutes au-dela de Scrum) | Integration Team, Nexus Integration Team | RTE, Solution Architect, Epic Owner, System Architect... |
| **Ceremonies ajoutees** | Scrum of Scrums, MetaScrum | Overall Sprint Planning, Overall Sprint Review | Nexus Sprint Planning, Nexus Sprint Retrospective | PI Planning, Inspect & Adapt, System Demo |
| **Courbe d'apprentissage** | Moderee | Faible (si Scrum maitrise) | Moderee | Elevee |
| **Adoption dans l'industrie** | Moderee | Faible a moderee | Faible | Tres elevee (60%+ des grandes entreprises) |

---

## Scrum@Scale

### Architecture de Scrum@Scale

Scrum@Scale repose sur deux cycles qui operent en parallele :

#### Cycle Scrum Master (How)

Le cycle SM coordonne le "comment" — l'execution et l'elimination des impediments :

```
[Equipe Scrum 1] --> [Scrum of Scrums (SoS)]
[Equipe Scrum 2] --> [Scrum of Scrums (SoS)]
[Equipe Scrum 3] --> [Scrum of Scrums (SoS)]
                            |
                     [SoS of SoS (SoSoS)] --> si necessaire
                            |
                 [Executive Action Team (EAT)]
```

- **Scrum of Scrums (SoS)** : reunion quotidienne de 15 min ou chaque equipe envoie un representant (souvent le SM). Objectif : identifier les dependances inter-equipes et les impediments.
- **Scrum of Scrums Master (SoSM)** : responsable de la facilitation du SoS et de la resolution des impediments inter-equipes.
- **Executive Action Team (EAT)** : equipe de direction responsable de la transformation agile et de la resolution des impediments organisationnels.

#### Cycle Product Owner (What)

Le cycle PO coordonne le "quoi" — la priorisation et l'alignement de la vision produit :

```
[PO Equipe 1] --> [MetaScrum]
[PO Equipe 2] --> [MetaScrum]
[PO Equipe 3] --> [MetaScrum]
                      |
               [Chief Product Owner (CPO)]
                      |
              [Executive MetaScrum (EMS)]
```

- **MetaScrum** : reunion hebdomadaire des PO pour aligner les priorites du backlog, gerer les dependances et arbitrer les conflits.
- **Chief Product Owner (CPO)** : responsable de la vision produit unifiee et de la priorisation inter-equipes.
- **Executive MetaScrum (EMS)** : aligne la vision produit avec la strategie d'entreprise.

### Principes de scaling Scrum@Scale

1. **Scale-free architecture** : les memes patterns Scrum s'appliquent a toutes les echelles (equipe, SoS, SoSoS). Pas de nouvelles regles, juste une recursion fractale.
2. **Minimum viable bureaucracy** : ajouter le strict minimum de coordination. Si un SoS suffit, ne pas creer un SoSoS.
3. **Continuous improvement** : chaque niveau de scaling a sa propre retrospective pour identifier et eliminer les frictions.

---

## LeSS — Large-Scale Scrum

### Principes LeSS

LeSS (Large-Scale Scrum) est une approche minimaliste du scaling, basee sur la philosophie "more with less" :

1. **Scrum reste Scrum** : ne pas ajouter de roles, artefacts ou ceremonies au-dela du strict necessaire. LeSS est du Scrum standard applique a plusieurs equipes travaillant sur un seul produit.
2. **Empirisme** : les pratiques emergent de l'experimentation, pas de la prescription. Chaque organisation doit trouver son propre equilibre.
3. **Transparence** : tout le monde voit le meme Product Backlog, le meme Definition of Done, le meme Sprint Review.
4. **Focus client** : chaque equipe interagit directement avec les clients/utilisateurs, pas via un intermediaire.

### LeSS Basic (2-8 equipes)

| Element | Description |
|---|---|
| **Roles** | 1 Product Owner pour tout le produit, des equipes Scrum standard (pas de SM additionnel) |
| **Product Backlog** | Un seul backlog pour toutes les equipes, priorise par le PO |
| **Sprint Planning Part 1** | Toutes les equipes ensemble avec le PO pour selectionner les items |
| **Sprint Planning Part 2** | Chaque equipe separement pour planifier le travail detaille. Coordination inter-equipes si dependances |
| **Daily Scrum** | Par equipe (standard), avec des representants invites aux dailies des autres equipes si besoin |
| **Sprint Review** | Un seul Sprint Review commun avec toutes les equipes et les parties prenantes (style "bazaar" avec des stations) |
| **Retrospective** | Par equipe + Overall Retrospective avec des representants de chaque equipe |

### LeSS Huge (8+ equipes)

Pour les organisations tres larges, LeSS Huge ajoute une couche :
- **Requirement Areas** : le produit est decoupe en "zones de requirements" (domaines fonctionnels). Chaque zone a un Area Product Owner.
- **Area Product Owner** : responsable de la priorisation dans sa zone, coordonne avec le Product Owner global.
- Les equipes sont assignees a une zone mais peuvent changer de zone entre les sprints.

---

## Nexus

### Structure de Nexus

Nexus est le framework officiel de Scrum.org pour 3-9 equipes Scrum travaillant sur un seul produit.

**Element central** : la **Nexus Integration Team** (NIT), composee de :
- Le **Product Owner** (partage avec les equipes Scrum).
- Le **Scrum Master** (dedie au Nexus, peut aussi etre SM d'une equipe).
- Des **membres des equipes Scrum** (1-2 par equipe, tournants) responsables de l'integration technique.

### Evenements Nexus

| Evenement | Participants | Objectif | Duree |
|---|---|---|---|
| **Nexus Sprint Planning** | NIT + representants de chaque equipe | Identifier les dependances, repartir les items, definir le Nexus Sprint Goal | 4h (sprint 2 sem.) |
| **Nexus Daily Scrum** | NIT + representants | Identifier les problemes d'integration, coordonner les dependances | 15 min |
| **Nexus Sprint Review** | Toutes les equipes + stakeholders | Inspecter l'increment integre, recueillir le feedback | 2h |
| **Nexus Sprint Retrospective** | 3 phases : representants ensemble, equipes separement, representants ensemble | Identifier les problemes cross-equipes, definir les ameliorations | 3h |

### Artefacts Nexus

- **Nexus Sprint Backlog** : rend visible les dependances inter-equipes et les elements d'integration. Ce n'est pas un backlog separe : c'est une vue composite des Sprint Backlogs des equipes, montrant les items inter-dependants.
- **Integrated Increment** : l'increment combine de toutes les equipes, integre et conforme au Definition of Done commun. L'integration doit etre continue (pas de "sprint d'integration").

---

## SAFe — Scaled Agile Framework (Portfolio Level)

### Les 4 configurations SAFe

| Configuration | Equipes | Description |
|---|---|---|
| **Essential SAFe** | 5-12 equipes (1 ART) | Le minimum pour operer SAFe : un Agile Release Train avec PI Planning |
| **Large Solution SAFe** | 12-50+ equipes | Plusieurs ARTs coordonnes via un Solution Train |
| **Portfolio SAFe** | 50-500+ personnes | Lean Portfolio Management, Strategy & Investment Funding |
| **Full SAFe** | Configuration complete | Toutes les couches integrees |

### SAFe Portfolio Level — Deep Dive

Le SAFe Portfolio Level gere le flux de valeur strategique :

#### Lean Portfolio Management (LPM)

3 dimensions :
1. **Strategy & Investment Funding** : allocation du budget par value stream (pas par projet). Le portfolio definit les guardrails budgetaires et les value streams les gèrent en autonomie.
2. **Agile Portfolio Operations** : gestion du flux d'epics via le Portfolio Kanban.
3. **Lean Governance** : conformite, metriques, audit adaptes a l'agilite.

#### Portfolio Kanban

Le Portfolio Kanban gere le flux des epics (initiatives strategiques) :

```
[Funnel] -> [Reviewing] -> [Analyzing] -> [Portfolio Backlog] -> [Implementing] -> [Done]
  WIP: -      WIP: 5       WIP: 3         WIP: 10               WIP: 5          WIP: -
```

- **Funnel** : capture de toutes les idees d'epics, sans filtre.
- **Reviewing** : premier tri : alignement strategique, pertinence, non-duplication.
- **Analyzing** : Lean Business Case, analyse de faisabilite, estimation (T-shirt sizing).
- **Portfolio Backlog** : epics pretes pour implementation, priorisees par WSJF.
- **Implementing** : epics en cours de realisation dans les ARTs/Solution Trains.
- **Done** : epic livree, benefices en cours de realisation.

#### Lean Business Case

Chaque epic necessite un Lean Business Case (1-2 pages, pas un document de 50 pages) :

| Section | Contenu |
|---|---|
| **Epic hypothesis** | "Nous croyons que [cette epic] delivrera [ce benefice] pour [ces utilisateurs]" |
| **Business outcome** | KPI(s) cibles et valeur attendue |
| **Leading indicators** | Metriques precoces confirmant que l'epic est sur la bonne voie |
| **NFRs** | Contraintes non-fonctionnelles (performance, securite, conformite) |
| **Cost estimate** | Estimation en T-shirt (S/M/L/XL) ou en PI-days |
| **Go/No-go recommendation** | Recommandation du Lean Portfolio Manager |

### PI Planning — Deep Dive

Le PI Planning est l'evenement central de SAFe, reunissant toutes les equipes d'un ART pour planifier le prochain Program Increment (8-12 semaines, typiquement 5 sprints).

**Agenda type (2 jours)** :

**Jour 1** :
- Business context (1h) : vision, objectifs strategiques, priorites du PI.
- Product/Solution vision (1h) : backlog des features, priorites produit.
- Architecture vision (30 min) : enablers techniques, decisions d'architecture.
- Team breakouts #1 (3h) : chaque equipe draft son plan de PI (features, dependances, risques).
- Draft plan review (1h) : chaque equipe presente son plan draft, identification des conflits.

**Jour 2** :
- Management review & problem solving (1h) : resolution des conflits et problemes identifies.
- Team breakouts #2 (2h) : ajustement des plans apres resolution des dependances.
- Final plan review & confidence vote (2h) : chaque equipe presente son plan final et vote sa confiance (fist of five).
- PI planning retrospective (30 min) : amelioration du processus de PI Planning.

**Confidence vote** : si la moyenne est < 3/5, le plan doit etre revu. Identifier les risques qui reduisent la confiance et les adresser.

**PI Objectives** : chaque equipe definit 5-10 PI Objectives dont certains sont "committed" (engagement ferme) et d'autres "uncommitted" (stretch goals). Les PI Objectives sont formules en termes de valeur metier, pas en termes techniques.

---

## Kanban Avance

### Flight Levels (Klaus Leopold)

Les Flight Levels modelisent les 3 niveaux d'optimisation du flux dans une organisation :

#### Flight Level 1 — Operational (Equipe)

- **Focus** : optimisation du flux de travail d'une equipe.
- **Board** : Kanban board de l'equipe (To Do / In Progress / Done).
- **Metriques** : cycle time, throughput, WIP de l'equipe.
- **Risque** : optimisation locale sans impact global (chaque equipe s'optimise mais l'organisation reste lente).

#### Flight Level 2 — Coordination (Inter-equipes)

- **Focus** : coordination du flux entre les equipes, gestion des dependances.
- **Board** : Kanban board de coordination montrant les initiatives qui traversent plusieurs equipes.
- **Metriques** : lead time end-to-end, dependances identifiees et resolues, flow efficiency inter-equipes.
- **Cle** : rendre visibles les hand-offs, les files d'attente et les blocages entre equipes.

#### Flight Level 3 — Strategic (Portefeuille)

- **Focus** : alignement du flux de valeur avec la strategie de l'organisation.
- **Board** : Portfolio Kanban montrant les initiatives strategiques et leur progression.
- **Metriques** : time-to-market des initiatives, alignement strategique, ROI du portefeuille.
- **Cle** : limiter le WIP strategique pour eviter le saupoudrage et accelerer les initiatives prioritaires.

**Principe fondamental** : commencer l'amelioration au Flight Level 3, pas au Flight Level 1. Optimiser le flux strategique d'abord, puis descendre aux niveaux inferieurs. L'optimisation locale (FL1) sans alignement strategique (FL3) est un gaspillage.

### Kanban Maturity Model (KMM)

Le KMM (David J. Anderson) definit 7 niveaux de maturite Kanban :

| Niveau | Nom | Description | Pratiques cles |
|---|---|---|---|
| **0** | Oblivious | Pas de conscience du flux, travail ad hoc | Aucune pratique structuree |
| **1** | Team-Focused | Equipes individuelles commencent a visualiser leur travail | Board basique, limites WIP initiales |
| **2** | Customer-Driven | Focus sur la livraison de valeur au client | Classes de service, SLA par classe, lead time tracking |
| **3** | Fit for Purpose | Organisation optimisee pour delivrer ce que le client attend | Metriques de fitness (lead time par classe), cadences formalisees, feedback loops |
| **4** | Risk-Hedged | Gestion proactive du risque via le flux | Risk profiles, cost of delay, portfolio balancing |
| **5** | Market Leader | Agilite strategique, adaptation rapide au marche | Innovation systemique, experimentation continue |
| **6** | Built for Survival | Organisation antifragile, capacite d'adaptation maximale | Meta-agilite, transformation continue |

### Classes de service Kanban

Les classes de service differantient le traitement des items selon leur urgence et leur profil de Cost of Delay :

| Classe | Profil CoD | Politique | % du WIP |
|---|---|---|---|
| **Expedite** | Immediat, critique | Bypass les limites WIP, traitement prioritaire, SLA < 24h | < 5% |
| **Fixed Date** | Augmente jusqu'a la date butoir | Planifie en amont, buffer avant la deadline | 10-20% |
| **Standard** | Lineaire, constant | FIFO ou priorisation par WSJF, SLA standard | 60-70% |
| **Intangible** | Progressif, long terme | Capacite dediee constante (ex : dette technique, amelioration continue) | 10-20% |

---

## Design Thinking

### Le processus Design Thinking (5 phases)

Le Design Thinking est une approche centree sur l'humain pour resoudre des problemes complexes et concevoir des solutions innovantes :

#### Phase 1 — Empathize (Comprendre)

**Objectif** : comprendre les besoins reels des utilisateurs au-dela de ce qu'ils expriment.

**Techniques** :
- **Interviews utilisateurs** : entretiens semi-directifs de 45-60 min, questions ouvertes, ecoute active. Minimum 5-8 utilisateurs par segment.
- **Observation terrain** : observer les utilisateurs dans leur contexte reel d'utilisation (shadowing, contextual inquiry).
- **Empathy map** : synthetiser ce que l'utilisateur dit, pense, fait et ressent.
- **Journey map** : cartographier le parcours de l'utilisateur etape par etape, avec les emotions, les pain points et les opportunites.

#### Phase 2 — Define (Definir)

**Objectif** : synthetiser les insights et formuler le probleme a resoudre.

**Techniques** :
- **Point of View (POV)** : "L'utilisateur [persona] a besoin de [besoin] parce que [insight]".
- **How Might We (HMW)** : reformuler le probleme en question ouverte et actionnable. "Comment pourrions-nous [action] pour [persona] afin de [benefice] ?"
- **Affinity diagram** : regrouper les observations et insights par themes pour identifier les patterns.

#### Phase 3 — Ideate (Generer des idees)

**Objectif** : generer un maximum d'idees de solutions sans jugement.

**Techniques** :
- **Brainstorming** : 15-30 min, rules (defer judgment, build on ideas, go for quantity, encourage wild ideas).
- **Brainwriting** : chaque participant ecrit ses idees silencieusement puis les partage (6-3-5 method).
- **Crazy 8s** : 8 idees en 8 minutes, favorise la pensee divergente.
- **SCAMPER** : Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse.

#### Phase 4 — Prototype (Prototyper)

**Objectif** : creer des representations tangibles et testables des solutions.

**Niveaux de fidelite** :
- **Basse fidelite** : sketches papier, wireframes simples, storyboards (quelques heures).
- **Moyenne fidelite** : wireframes interactifs (Figma, Balsamiq), mockups cliquables (1-3 jours).
- **Haute fidelite** : prototype fonctionnel avec donnees reelles (1-2 semaines).

Regle cle : le prototype doit etre suffisamment realiste pour generer du feedback actionnable, mais suffisamment rapide a creer pour etre jetable.

#### Phase 5 — Test (Tester)

**Objectif** : confronter le prototype aux utilisateurs et apprendre.

**Methode** :
- Tester avec 5-8 utilisateurs (seuil de saturation pour identifier 80% des problemes).
- Observer le comportement plus qu'ecouter les opinions.
- Poser des questions ouvertes : "Parle-moi de ce que tu fais" plutot que "Est-ce que tu aimes ?".
- Iterer : revenir a la phase appropriee (Empathize, Define, Ideate ou Prototype) en fonction des apprentissages.

---

## Design Sprint (Google Ventures)

### Format du Design Sprint (5 jours)

Le Design Sprint condense le processus de design thinking en 5 jours structures :

| Jour | Activite | Objectif | Livrable |
|---|---|---|---|
| **Lundi — Map** | Cartographier le probleme, choisir un focus | Comprendre le challenge et definir le perimetre | Map du challenge, target user, focus choisi |
| **Mardi — Sketch** | Explorer les solutions individuellement | Generer des solutions concretes | Sketches de solutions individuelles (solution sketch) |
| **Mercredi — Decide** | Choisir la meilleure solution et planifier le prototype | Converger vers une solution testable | Storyboard du prototype a construire |
| **Jeudi — Prototype** | Construire un prototype realiste | Creer un artefact testable en 1 journee | Prototype interactif haute-fidelite |
| **Vendredi — Test** | Tester avec 5 utilisateurs cibles | Valider ou invalider l'hypothese | Resultats des 5 tests, decisions go/no-go/iterate |

### Quand utiliser un Design Sprint

- Lancement d'un nouveau produit ou d'une nouvelle feature strategique.
- Probleme complexe avec de l'incertitude sur la solution.
- Besoin de rapprocher des equipes (business, design, tech) autour d'une vision commune.
- Deblocage d'un sujet en impasse depuis des semaines/mois.

### Adaptations du format

- **Mini Design Sprint (3 jours)** : Map+Sketch lundi, Decide+Prototype mardi, Test mercredi. Pour les problemes mieux definis.
- **Design Sprint remote** : fonctionne bien avec Miro/FigJam pour la collaboration et Zoom pour les sessions. Preferer des sessions de 4h/jour plutot que 8h pour eviter la fatigue Zoom.
- **Lightning Decision Jam (LDJ)** : format de 60 min pour les decisions rapides, combinant vote silencieux et priorisation.

---

## Lean Management — Kaizen, A3 & Value Stream Mapping

### Kaizen — Amelioration Continue

**Principes** :
- **Petites ameliorations continues** plutot que des changements radicaux.
- **Gemba** : aller sur le terrain (la ou la valeur est creee) pour observer et comprendre.
- **Respect des personnes** : les personnes qui font le travail sont les mieux placees pour l'ameliorer.
- **Standardiser avant d'ameliorer** : un processus non standardise ne peut pas etre ameliore de maniere fiable.

**Kaizen Event (Kaizen Blitz)** :
- Evenement structure de 3-5 jours concentrant une equipe cross-fonctionnelle sur l'amelioration d'un processus specifique.
- Jour 1 : observation du processus actuel (gemba walk), identification des gaspillages (muda).
- Jour 2-3 : conception et test des ameliorations.
- Jour 4 : mise en oeuvre des ameliorations.
- Jour 5 : standardisation et plan de suivi.

### Les 8 gaspillages (Muda) adaptes au travail de connaissance

| Gaspillage original (manufacturing) | Equivalent en travail de connaissance | Exemple |
|---|---|---|
| **Surproduction** | Travail fait trop tot ou en exces | Features jamais utilisees, rapports non lus |
| **Attente** | Temps d'attente entre les etapes | Attente de validation, attente de deploiement |
| **Transport** | Transferts inutiles entre equipes | Hand-offs multiples, escalades evitables |
| **Sur-traitement** | Complexite inutile | Sur-engineering, gold plating, documentation excessive |
| **Stock** | Travail en cours non termine | Backlog plethore, stories commencees non finies |
| **Mouvements** | Context switching, interruptions | Multi-projet, meetings excessifs, outils fragmentes |
| **Defauts** | Bugs, erreurs, re-travail | Bugs en production, specifications ambigues |
| **Potentiel humain** | Sous-utilisation des competences | Experts faisant du travail routinier, suggestions ignorees |

### A3 Problem Solving

Le A3 est un format structure de resolution de probleme sur une seule feuille A3, force la synthese et la rigueur :

```
+--------------------------------------+--------------------------------------+
| COTE GAUCHE (Comprendre)             | COTE DROIT (Resoudre)                |
|                                      |                                      |
| 1. CONTEXTE                          | 5. CONTRE-MESURES                    |
| Pourquoi ce probleme est important   | Actions specifiques pour atteindre   |
| maintenant ?                         | l'etat cible                         |
|                                      |                                      |
| 2. ETAT ACTUEL                       | 6. PLAN D'ACTION                     |
| Description factuelle du probleme    | Qui, Quoi, Quand, Ou                 |
| (donnees, metriques, observations)   |                                      |
|                                      |                                      |
| 3. OBJECTIF / ETAT CIBLE            | 7. SUIVI                             |
| Ou voulons-nous arriver ?            | Metriques de suivi, cadence de revue |
| (quantifie, date)                    |                                      |
|                                      |                                      |
| 4. ANALYSE DES CAUSES               | 8. RESULTATS & APPRENTISSAGES        |
| Root cause analysis                  | Resultats obtenus, lecons apprises   |
| (5 Why, Ishikawa, Pareto)           |                                      |
+--------------------------------------+--------------------------------------+
```

### Value Stream Mapping (VSM)

La VSM cartographie le flux de valeur de bout en bout pour identifier les gaspillages et les opportunites d'amelioration :

**Etapes de realisation** :

**1. Definir le perimetre** : choisir un flux de valeur specifique (ex : du ticket client a la resolution, de l'idee au deploiement en production).

**2. Cartographier l'etat actuel** :
```
[Demande]  -->  [Analyse]  -->  [Developpement]  -->  [Test]  -->  [Deploiement]  -->  [Done]
  PT: 0.5j      PT: 2j          PT: 5j               PT: 2j      PT: 0.5j
  WT: 3j        WT: 2j          WT: 1j               WT: 5j      WT: 2j

PT = Processing Time (temps de travail actif)
WT = Waiting Time (temps d'attente)
Lead Time total = 23 jours
Process Time total = 10 jours
Flow Efficiency = 10/23 = 43%
```

**3. Identifier les gaspillages** :
- Les temps d'attente (WT) les plus longs sont les goulots d'etranglement prioritaires.
- Dans l'exemple : l'attente avant le test (5j) est le principal goulot.

**4. Concevoir l'etat futur** :
- Eliminer ou reduire les temps d'attente les plus longs.
- Automatiser les hand-offs manuels.
- Paralleliser les activites independantes.
- Reduire les tailles de lot pour accelerer le flux.

**5. Plan d'amelioration** :
- Definir les actions concretes pour passer de l'etat actuel a l'etat futur.
- Prioriser par impact/effort.
- Implementer par petites iterations (kaizen).

---

## State of the Art (2024-2026)

### SAFe 6.0 et l'evolution du framework

SAFe 6.0 a introduit plusieurs evolutions significatives :
- **AI-Augmented SAFe** : integration de l'IA dans les pratiques SAFe — estimation assistee par IA, detection automatique des dependances lors du PI Planning, prediction de la capacite et des risques de PI.
- **Business Agility** : SAFe 6.0 etend le scope au-dela de l'IT/engineering pour couvrir l'agilite metier (marketing, finance, RH, legal). Le concept de "Business Agility Value Stream" formalise l'application de l'agilite a l'ensemble de l'entreprise.
- **Measure and Grow** : renforcement des metriques avec un framework structure pour mesurer l'agilite a tous les niveaux (team, ART, Solution Train, Portfolio) via les flow metrics et les outcome-based metrics.
- **Lean-Agile Procurement** : nouveau guide pour l'agilite dans les processus d'achat et de contractualisation, eliminant les contrats waterfall rigides au profit de contrats agiles collaboratifs.
- **OKR Integration** : alignement formel des OKR avec les PI Objectives et les metriques de flux SAFe.

### Team Topologies et l'organisation agile

L'approche Team Topologies (Matthew Skelton & Manuel Pais) redefinit la facon dont les equipes agiles sont organisees :

| Type d'equipe | Mission | Interaction avec les autres |
|---|---|---|
| **Stream-aligned** | Delivrer de la valeur sur un flux metier specifique | Consomme des services des equipes Platform et Complicated-Subsystem |
| **Enabling** | Aider les stream-aligned teams a acquerir de nouvelles competences | Mode collaboration temporaire (semaines/mois) |
| **Platform** | Fournir des services self-service qui accelerent les stream-aligned teams | Mode X-as-a-Service |
| **Complicated-Subsystem** | Gerer un sous-systeme techniquement complexe necessitant une expertise specialisee | Mode X-as-a-Service ou Collaboration |

**Principle cle** : minimiser la charge cognitive par equipe. Chaque equipe ne doit gerer qu'un perimetre compatible avec sa capacite cognitive (regle : si l'equipe ne peut pas comprendre tout son domaine, le perimetre est trop large).

### Flow Engineering

Le Flow Engineering (Steve Pereira & Andrew Davis) combine le Value Stream Mapping avec des techniques modernes :
- **Value Stream Discovery** : cartographie collaborative du flux de valeur en atelier de 2-4 heures.
- **Flow Roadmap** : roadmap d'amelioration basee sur les goulots identifies par la VSM.
- **Dependency Mapping** : visualisation et gestion des dependances inter-equipes comme un systeme de flux.
- L'approche s'integre avec les Flight Levels de Klaus Leopold pour optimiser le flux a tous les niveaux.

### Unfix Model

L'Unfix Model (Jurgen Appelo) propose une alternative aux structures organisationnelles figees :
- Les equipes ne sont pas permanentes mais se recomposent en fonction des besoins (Base, Crew, Forum, Squad patterns).
- L'organisation est vue comme un reseau dynamique plutot qu'un organigramme statique.
- Adapte aux environnements ou les priorites changent rapidement et ou la polyvalence est valorisee.

### Outcome-Driven Development

Le passage des outputs aux outcomes s'accelere :
- Les equipes ne sont plus mesurees sur le volume de stories livrees mais sur l'impact genere pour les utilisateurs.
- Les **Opportunity Solution Trees** (Teresa Torres) deviennent l'outil standard pour relier les outcomes desires aux solutions testables.
- Le **Dual Track Agile** mature integre la discovery continue comme une activite permanente de l'equipe, pas un phase separee.
- Les metriques evoluent : de la velocity (output) vers les DORA metrics (DevOps Research and Assessment) pour le flux technique, et les product metrics (retention, activation, revenue) pour l'impact metier.
- Le concept de **North Star Metric** (une metrique unique capturant la valeur fondamentale du produit) se generalise pour aligner toutes les equipes sur un objectif commun.

### Kanban for Knowledge Work (post-Lean Kanban)

Le Kanban pour le travail de connaissance continue d'evoluer :
- **Actionable Agile Metrics** (Daniel Vacanti) : utilisation des metriques probabilistes (percentiles de cycle time, scatter plots, Monte Carlo simulations) plutot que des moyennes pour la prevision et le SLA.
- **Kanban Guide for Scrum Teams** (Scrum.org + Kanban University) : integration officielle des pratiques Kanban dans Scrum, validant l'approche Scrumban.
- **Flow metrics universelles** : l'adoption des 4 flow metrics (throughput, WIP, cycle time, work item age) se generalise au-dela des equipes Kanban, y compris dans les equipes Scrum et SAFe.
- **Monte Carlo simulations** : les simulations Monte Carlo remplacent progressivement les estimations manuelles pour la prevision de dates de livraison et la planification de releases, offrant des predictions basees sur les donnees historiques reelles plutot que sur des estimations subjectives.
