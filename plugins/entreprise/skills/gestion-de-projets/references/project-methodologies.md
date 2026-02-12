# Project Methodologies — Waterfall, Agile, SAFe, PRINCE2, Hybrid & Tools

## Overview

Ce document de reference couvre les methodologies de gestion de projet dans leur profondeur : Waterfall traditionnel, approches agiles (Scrum, Kanban, Scrumban), frameworks a l'echelle (SAFe), PRINCE2, approches hybrides, ainsi que les techniques de planification (WBS, Gantt), de gestion des risques (risk register) et de suivi de la valeur acquise (EVM). Utiliser ce guide pour selectionner, configurer et deployer la methodologie la plus adaptee au contexte de chaque projet, en s'appuyant sur les outils modernes de gestion de projet (Jira, Asana, Monday, Linear, MS Project).

---

## Waterfall — Approche Sequentielle

### Principes fondamentaux

Le modele Waterfall (cascade) organise le projet en phases sequentielles ou chaque phase doit etre completee avant de passer a la suivante. Chaque phase produit des livrables formels qui servent d'entree a la phase suivante.

### Les 6 phases du Waterfall

| Phase | Livrables | Gate de sortie |
|---|---|---|
| **1. Requirements** | Cahier des charges (SRS), specification fonctionnelle | Signature du sponsor |
| **2. Design** | Architecture technique, design detaille, plan de tests | Revue de design approuvee |
| **3. Implementation** | Code source, composants developpes, documentation technique | Code complet, revue de code |
| **4. Testing** | Rapports de tests (unitaires, integration, systeme, UAT) | Criteres d'acceptation valides |
| **5. Deployment** | Systeme deploye en production, documentation operationnelle | Go-live confirme |
| **6. Maintenance** | Correctifs, evolutions mineures, support | SLA respectes |

### Quand utiliser Waterfall

Utiliser Waterfall lorsque :
- Les exigences sont stables, completes et bien documentees avant le debut du developpement.
- Le projet est reglemente ou contractuel avec des livrables formels obligatoires (defense, construction, medical devices).
- Les dependances techniques imposent un sequencement strict (infrastructure physique, hardware).
- Le client exige un prix fixe et un perimetre defini (contrat forfaitaire).
- L'equipe est distribuee et la communication asynchrone domine.

### Limites connues

- Decouverte tardive des problemes (le test arrive en fin de cycle).
- Cout du changement eleve : une modification des exigences en phase de test peut couter 10-100x plus cher qu'en phase de design.
- Absence de feedback utilisateur avant le deploiement.
- Effet tunnel : le sponsor ne voit rien pendant des mois.

---

## PRINCE2 — PRojects IN Controlled Environments

### Principes fondamentaux

PRINCE2 est un framework de gestion de projet structure, base sur 7 principes, 7 themes et 7 processus. Il est largement adopte au Royaume-Uni, en Europe et dans les organisations gouvernementales.

### Les 7 principes PRINCE2

1. **Continued Business Justification** : le projet doit rester justifie tout au long de son cycle de vie. Si le business case n'est plus viable, arreter le projet.
2. **Learn from Experience** : capitaliser sur les lecons apprises des projets precedents et du projet en cours.
3. **Defined Roles and Responsibilities** : chaque partie prenante a un role clair (Project Board, Project Manager, Team Manager, Project Assurance).
4. **Manage by Stages** : decouper le projet en stages de gestion, chaque stage etant approuve separement.
5. **Manage by Exception** : definir des tolerances (temps, cout, qualite, perimetre, risque, benefices) et n'escalader que si les tolerances sont depassees.
6. **Focus on Products** : se concentrer sur les livrables (products) plutot que sur les activites.
7. **Tailor to Suit the Project** : adapter le framework a la taille et a la complexite du projet.

### Les 7 themes PRINCE2

| Theme | Description | Artefact cle |
|---|---|---|
| **Business Case** | Justification continue du projet | Business Case document |
| **Organization** | Structure de gouvernance et roles | Organization chart, role descriptions |
| **Quality** | Criteres de qualite et methode de controle | Quality Management Strategy |
| **Plans** | Planification a 3 niveaux (projet, stage, equipe) | Project Plan, Stage Plans |
| **Risk** | Identification et gestion des risques | Risk Register |
| **Change** | Controle des changements et des issues | Issue Register, Change Control |
| **Progress** | Suivi de l'avancement et reporting | Highlight Reports, End Stage Reports |

### PRINCE2 Agile

PRINCE2 Agile combine la gouvernance PRINCE2 avec les pratiques de delivery agile. C'est une approche hybride ou :
- La **gouvernance** (business case, stages, tolerances, reporting) suit PRINCE2.
- Le **delivery** (au sein de chaque stage) utilise Scrum, Kanban ou une autre methode agile.
- Les **tolerances** sont configurees pour permettre la flexibilite agile : le perimetre est la variable d'ajustement principale (les Must sont proteges, les Should et Could sont flexibles via MoSCoW).

---

## Scrum — Framework Agile Iteratif

### Les 3 piliers de Scrum

1. **Transparence** : tous les aspects significatifs du processus doivent etre visibles pour ceux qui sont responsables du resultat.
2. **Inspection** : les artefacts Scrum et la progression vers les objectifs doivent etre inspectes frequemment.
3. **Adaptation** : si un aspect du processus devie au-dela des limites acceptables, l'ajustement doit etre fait au plus vite.

### Roles Scrum

| Role | Responsabilites | Anti-patterns |
|---|---|---|
| **Product Owner** | Maximiser la valeur du produit, gerer le Product Backlog, definir les priorites, representer les stakeholders | PO absent ou indisponible, PO proxy sans pouvoir de decision, backlog non priorise |
| **Scrum Master** | Faciliter les evenements Scrum, coacher l'equipe, eliminer les impediments, proteger l'equipe | SM qui fait du micro-management, SM qui devient chef de projet, SM a temps partiel sur 5 equipes |
| **Developers** | Auto-organisation pour livrer l'increment, competences cross-fonctionnelles, engagement sur le Sprint Goal | Equipe de specialistes (pas cross-fonctionnel), equipe trop grande (>9), absence de responsabilite collective |

### Evenements Scrum

| Evenement | Duree (sprint 2 sem.) | Objectif | Participants |
|---|---|---|---|
| **Sprint Planning** | 4h max | Definir le Sprint Goal et selectionner les items du backlog | Scrum Team |
| **Daily Scrum** | 15 min | Inspecter la progression vers le Sprint Goal, adapter le plan | Developers |
| **Sprint Review** | 2h max | Inspecter l'increment, collecter le feedback, adapter le backlog | Scrum Team + stakeholders |
| **Sprint Retrospective** | 1h30 max | Inspecter le processus, identifier les ameliorations, planifier les actions | Scrum Team |

### Artefacts Scrum

- **Product Backlog** : liste ordonnee de tout ce qui est necessaire pour le produit. Le PO en est responsable. Raffiner continuellement (refinement = ~10% du temps du sprint).
- **Sprint Backlog** : ensemble des items du Product Backlog selectionnes pour le sprint, plus le plan pour les livrer. Propriete des Developers.
- **Increment** : somme de tous les items du Product Backlog completes pendant le sprint et les sprints precedents. Doit respecter la Definition of Done.
- **Definition of Done (DoD)** : accord commun sur les criteres qu'un item doit satisfaire pour etre considere comme termine. Inclut typiquement : code revise, tests unitaires passes, tests d'integration passes, documentation mise a jour, deploye en environnement de staging.

### Metriques Scrum

| Metrique | Definition | Usage | Piege a eviter |
|---|---|---|---|
| **Velocity** | Nombre de story points completes par sprint | Prevision de capacite (pas de performance !) | Utiliser la velocity comme KPI de performance |
| **Sprint Burndown** | Travail restant dans le sprint par jour | Visibilite sur la progression intra-sprint | Obseder sur la forme de la courbe |
| **Release Burnup** | Story points cumulees livrees vs. scope total | Prevision de date de release | Ignorer les variations de scope |

---

## Kanban — Systeme de Flux Continu

### Les 6 pratiques fondamentales de Kanban

1. **Visualiser le flux de travail** : rendre visible chaque etape du processus sur un board.
2. **Limiter le travail en cours (WIP)** : plafonner le nombre d'items par etape pour eviter la surcharge et accelerer le flux.
3. **Gerer le flux** : mesurer et optimiser le temps de traversee (lead time), le debit (throughput) et l'age des items.
4. **Expliciter les regles de processus** : definir les criteres d'entree, de sortie et de tirage (pull) pour chaque colonne.
5. **Implementer des boucles de feedback** : cadences regulieres de revue (daily standup, replenishment, delivery planning, service delivery review).
6. **S'ameliorer collaborativement, evoluer experimentalement** : utiliser des modeles et la methode scientifique pour proposer et evaluer des ameliorations.

### Metriques de flux Kanban

| Metrique | Definition | Cible typique |
|---|---|---|
| **Lead Time** | Temps entre l'entree d'un item dans le systeme et sa completion | Reduire continuellement |
| **Cycle Time** | Temps entre le debut du travail actif et la completion | < Lead Time |
| **Throughput** | Nombre d'items completes par unite de temps | Stabiliser et augmenter |
| **WIP** | Nombre d'items en cours a un instant T | Limiter (loi de Little : Lead Time = WIP / Throughput) |
| **WIP Age** | Temps depuis lequel un item est en cours | Alerter si > 85e percentile du Cycle Time |
| **Flow Efficiency** | Ratio temps actif / temps total (actif + attente) | > 40% (excellence > 60%) |

### Scrumban — Hybride Scrum + Kanban

Scrumban combine les elements de Scrum et de Kanban pour les equipes qui veulent la cadence Scrum avec la flexibilite Kanban :
- **De Scrum** : iterations (sprints optionnels), sprint planning, retrospective, roles (optionnels).
- **De Kanban** : limites WIP, gestion du flux, metriques de flux, tirage (pull) au lieu de l'engagement par sprint.
- **Cas d'usage** : equipes de maintenance/support ou la charge est imprevisible, equipes en transition de Scrum vers Kanban, equipes produit avec un mix de feature work et d'operations.

---

## WBS, Gantt & Planification

### Work Breakdown Structure (WBS)

La WBS decompose le projet en livrables de plus en plus fins, selon une structure hierarchique :

```
Projet
+-- Phase 1 : Cadrage
|   +-- 1.1 Etude de faisabilite
|   +-- 1.2 Business case
|   +-- 1.3 Charte de projet
+-- Phase 2 : Conception
|   +-- 2.1 Architecture fonctionnelle
|   +-- 2.2 Architecture technique
|   +-- 2.3 Plan de tests
+-- Phase 3 : Realisation
|   +-- 3.1 Module A
|   |   +-- 3.1.1 Developpement
|   |   +-- 3.1.2 Tests unitaires
|   +-- 3.2 Module B
|       +-- 3.2.1 Developpement
|       +-- 3.2.2 Tests unitaires
+-- Phase 4 : Tests & Deploiement
    +-- 4.1 Tests d'integration
    +-- 4.2 UAT
    +-- 4.3 Deploiement production
```

Regles de construction :
- **Regle des 100%** : la WBS doit capturer 100% du travail du projet, ni plus, ni moins.
- **Regle du 8/80** : chaque work package au niveau le plus fin represente entre 8 heures et 80 heures de travail.
- **Livrables, pas activites** : decomposer par livrable (nom = substantif), pas par activite (nom = verbe).
- **Mutuellement exclusif** : pas de chevauchement entre les elements d'un meme niveau.

### Diagramme de Gantt

Le Gantt traduit la WBS en planning temporel avec :
- **Taches** : chaque work package de la WBS avec une duree, une date de debut et de fin.
- **Dependances** : liens entre les taches (Finish-to-Start, Start-to-Start, Finish-to-Finish, Start-to-Finish).
- **Chemin critique** : la sequence de taches la plus longue determinant la duree minimale du projet. Toute tache du chemin critique en retard retarde le projet.
- **Marge (float)** : temps disponible pour retarder une tache sans impacter la date de fin du projet. Les taches du chemin critique ont une marge de zero.
- **Jalons (milestones)** : points de controle sans duree marquant la fin d'une phase ou un livrable cle.

---

## Risk Register — Gestion des Risques Projet

### Structure du risk register

| Champ | Description |
|---|---|
| **ID** | Identifiant unique du risque (R-001, R-002...) |
| **Description** | Description claire du risque (evenement + impact) |
| **Categorie** | Technique, organisationnel, externe, financier, legal |
| **Probabilite** | Estimation de la probabilite (1-5 ou %) |
| **Impact** | Estimation de l'impact (1-5 ou EUR) |
| **Score** | Probabilite x Impact |
| **Strategie** | Eviter, Transferer, Attenuer, Accepter (ETAA) |
| **Actions** | Actions de mitigation planifiees |
| **Owner** | Responsable du suivi du risque |
| **Statut** | Ouvert, En cours, Ferme |

### Exemple de risk register

| ID | Risque | Prob | Impact | Score | Strategie | Action |
|---|---|---|---|---|---|---|
| R-001 | Depart d'un developpeur senior en cours de projet | 3 | 4 | 12 | Attenuer | Documenter le code, binomage, plan de succession |
| R-002 | Changement reglementaire impactant le perimetre | 2 | 5 | 10 | Accepter | Veille reglementaire, marge de 15% dans le planning |
| R-003 | Performance insuffisante de l'API tierce | 4 | 3 | 12 | Attenuer | PoC technique en sprint 1, plan B avec API alternative |
| R-004 | Resistance des utilisateurs finaux au nouvel outil | 4 | 4 | 16 | Attenuer | Programme de change management, pilote utilisateurs |

### Cadences de revue des risques

- **Hebdomadaire** : mise a jour des risques actifs dans le standup projet.
- **Bi-mensuelle** : revue complete du risk register par le chef de projet et le sponsor.
- **A chaque gate/milestone** : revue formelle par le comite de pilotage.

---

## Earned Value Management (EVM)

### Les 3 mesures fondamentales de l'EVM

| Mesure | Definition | Source |
|---|---|---|
| **Planned Value (PV)** | Budget autorise pour le travail planifie a date | Planning de reference (baseline) |
| **Earned Value (EV)** | Budget autorise pour le travail reellement accompli a date | Avancement reel x budget |
| **Actual Cost (AC)** | Cout reel depense a date | Comptabilite projet |

### Indicateurs de performance EVM

| Indicateur | Formule | Interpretation |
|---|---|---|
| **Schedule Variance (SV)** | EV - PV | > 0 : en avance / < 0 : en retard |
| **Cost Variance (CV)** | EV - AC | > 0 : sous le budget / < 0 : depassement |
| **Schedule Performance Index (SPI)** | EV / PV | > 1 : en avance / < 1 : en retard |
| **Cost Performance Index (CPI)** | EV / AC | > 1 : sous le budget / < 1 : depassement |
| **Estimate at Completion (EAC)** | BAC / CPI | Projection du cout total a la fin |
| **Estimate to Complete (ETC)** | EAC - AC | Budget restant necessaire |
| **Variance at Completion (VAC)** | BAC - EAC | Ecart projete budget final vs. initial |

### Exemple pratique EVM

```
Projet de 12 mois, budget total (BAC) = 1 200 000 EUR
A la fin du mois 6 :

PV = 600 000 EUR (50% du budget devait etre consomme)
EV = 480 000 EUR (40% du travail est reellement accompli)
AC = 540 000 EUR (on a depense 540 000 EUR)

SV = 480 000 - 600 000 = -120 000 EUR -> en retard
CV = 480 000 - 540 000 = -60 000 EUR -> depassement de budget
SPI = 480 000 / 600 000 = 0.80 -> 20% en retard sur le planning
CPI = 480 000 / 540 000 = 0.89 -> chaque euro depense ne produit que 0.89 EUR de valeur
EAC = 1 200 000 / 0.89 = 1 348 315 EUR -> projection de depassement de 148k EUR
```

**Decisions a prendre** : quand SPI < 0.8 ou CPI < 0.8, escalader immediatement au sponsor. Envisager un rebaseline, une reduction de perimetre, ou un renfort de capacite.

---

## Outils de Gestion de Projet — Guide de Selection et Configuration

### Jira (Atlassian)

**Positionnement** : outil de reference pour les equipes tech/engineering, natif agile.

Configuration recommandee pour Scrum :
- Creer un project de type "Scrum board" avec les colonnes : Backlog, To Do, In Progress, In Review, Done.
- Configurer les types d'issues : Epic > Story > Sub-task, Bug, Spike.
- Parametrer les story points sur le champ "Story Points".
- Activer le sprint board et les velocity charts.
- Configurer les workflows avec transitions claires et conditions (ex : un item ne peut passer "In Review" que si un reviewer est assigne).
- Utiliser les Jira Automations pour les taches repetitives (deplacer en Done quand la PR est mergee, notification au PO quand un bug est cree).

Integration avec l'ecosysteme :
- **Confluence** : documentation, comptes rendus de sprint review, ADR.
- **Bitbucket/GitHub** : lien automatique entre les commits/PR et les issues Jira.
- **Slack/Teams** : notifications sur les changements de statut.
- **API REST** : `https://your-instance.atlassian.net/rest/api/3/` pour l'automatisation et le reporting custom. Cle API : `JIRA_API_TOKEN=FAKE-xxxx-1234-abcd-fake-token-000`.

### Asana

**Positionnement** : collaboration cross-fonctionnelle, excellent pour les equipes non-tech.

Configuration recommandee :
- Utiliser les Portfolios pour la vue portefeuille multi-projets.
- Creer des projets en mode Board (Kanban) ou List selon la preference de l'equipe.
- Exploiter les Custom Fields pour le scoring de priorisation (Impact, Effort, RICE score).
- Configurer les Rules (automatisations) pour les workflows recurrents.
- Utiliser les Goals pour lier les projets aux objectifs strategiques.

### Monday.com

**Positionnement** : polyvalent, excellent reporting, ideal pour les PMO et les equipes operations.

Configuration recommandee :
- Utiliser les Workspaces pour separer les departements.
- Creer des Dashboards agrégeant les donnees de plusieurs boards pour le reporting PMO.
- Exploiter les formules pour les calculs automatiques (RICE score, EVM simplifie).
- Configurer les integrations natives (Slack, email, calendar).
- Utiliser les automations pour le suivi des deadlines et les notifications d'escalade.

### Linear

**Positionnement** : rapidite et experience developpeur, ideal pour les startups et scale-ups tech.

Configuration recommandee :
- Utiliser les Cycles (equivalent des sprints) de 1-2 semaines.
- Exploiter les Projects pour regrouper les issues par initiative strategique.
- Configurer le Triage flow pour le traitement rapide des bugs et demandes.
- Utiliser les Roadmaps pour la visibilite multi-projets.
- Integration native avec GitHub/GitLab pour le suivi automatique du code.

---

## Approches Hybrides

### Principes de l'hybridation

L'approche hybride combine les elements de plusieurs methodologies pour s'adapter au contexte. Elle est pertinente quand :
- Le projet a un perimetre macro stable mais des details emergents (planification Waterfall au niveau programme, delivery agile au niveau equipe).
- Les parties prenantes exigent des livrables formels et un planning global (PRINCE2) mais l'equipe technique fonctionne en Scrum.
- L'organisation est en transition vers l'agilite et ne peut pas adopter un framework pur d'emblee.

### Pattern hybride classique : "Water-Scrum-Fall"

```
[Phase 1: Requirements]  ->  [Phase 2: Sprints de delivery]  ->  [Phase 3: Release]
  (Waterfall)                    (Scrum / Kanban)                  (Waterfall)
  - Business case                - Sprint Planning                 - UAT formelle
  - Spec. fonctionnelle          - Daily Scrum                     - Formation
  - Architecture macro           - Sprint Review                   - Deploiement
  - Plan projet global           - Retrospective                   - Hypercare
  Duree : 4-8 sem.              Duree : 8-16 sem.                 Duree : 2-4 sem.
```

### Pattern hybride avance : PRINCE2 Agile

La gouvernance PRINCE2 encapsule le delivery agile :
- **Initiation Stage** (PRINCE2) : business case, PID, definition des tolerances MoSCoW.
- **Delivery Stages** (Agile) : chaque stage PRINCE2 contient N sprints. Le Scrum Team livre les increments. Le perimetre "Could" et "Won't" sert de variable d'ajustement.
- **End Stage Assessment** (PRINCE2) : revue formelle, decision de continuer/arreter, mise a jour du business case.
- **Closing** (PRINCE2) : revue post-implementation, lecons apprises, transfert en operations.

---

## State of the Art (2024-2026)

### AI-Augmented Project Management

L'intelligence artificielle transforme la gestion de projet sur plusieurs axes :
- **Predictive scheduling** : les outils modernes (Jira, Monday, Asana) integrent des modeles predictifs qui estiment les dates de livraison basees sur les donnees historiques de velocity et de cycle time, plutot que sur les estimations manuelles.
- **Risk prediction** : identification automatique des risques emergents a partir de l'analyse des patterns de retard, de la charge de travail et des dependances. Des outils comme Forecast.app et Screenful utilisent le ML pour anticiper les deviations.
- **Intelligent triage** : classification automatique des bugs et demandes, assignation suggeree, estimation de l'effort par analyse du texte et des donnees historiques.
- **Meeting intelligence** : transcription et synthese automatique des ceremonies agiles (sprint review, retrospective), extraction des decisions et des actions, suivi automatique.
- **Natural language queries** : interrogation du portefeuille de projets en langage naturel ("quels projets sont en retard de plus de 2 semaines ?") via les assistants IA integres aux outils.

### Evolution des outils

- **Linear** a connu une croissance significative depuis 2023, s'imposant comme l'outil de reference pour les equipes engineering des startups et scale-ups, grace a sa rapidite et son experience utilisateur soignee.
- **Jira** a deploye Atlassian Intelligence (IA generative) pour la creation automatique de stories, la suggestion de priorites et l'analyse des retrospectives.
- **Monday.com** et **Asana** ont renforce leurs capacites de portfolio management et de resource management, ciblant directement le segment PMO.
- **GitHub Projects** et **GitLab** etendent leurs capacites de project management natif, permettant aux equipes dev de rester dans leur ecosysteme sans outil tiers.
- **Notion** et **Coda** gagnent du terrain comme outils de documentation projet integree, remplacant Confluence pour certaines equipes.

### Tendances methodologiques

- **Continuous Discovery** (Teresa Torres) : integration permanente de la decouverte produit dans le cycle de delivery, au-dela du dual track classique. Les Opportunity Solution Trees deviennent un outil standard.
- **Shape Up** (Basecamp) : alternative a Scrum avec des cycles de 6 semaines ("bets"), sans backlog permanent, avec un accent sur l'appetit (budget de temps) plutot que sur l'estimation. Adoption croissante dans les startups produit.
- **Team Topologies** (Skelton & Pais) : organisation des equipes en 4 types (Stream-aligned, Enabling, Platform, Complicated-subsystem) avec 3 modes d'interaction (Collaboration, X-as-a-Service, Facilitating). Devient le standard de reference pour structurer les equipes tech.
- **Flow metrics over velocity** : les metriques de flux (lead time, cycle time, throughput, WIP) remplacent progressivement la velocity comme metriques primaires de performance, meme dans les equipes Scrum.
- **Evidence-Based Management (EBM)** de Scrum.org : framework de metriques organisationnelles en 4 dimensions (Current Value, Unrealized Value, Time-to-Market, Ability to Innovate) pour piloter l'agilite au niveau strategique.
- **OKR + Agile alignment** : l'alignement des OKR (Objectives & Key Results) avec le delivery agile se generalise, avec des cadences OKR trimestrielles synchronisees avec les PI Planning ou les quarterly planning agiles.
