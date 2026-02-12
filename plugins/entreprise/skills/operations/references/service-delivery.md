# Service Delivery & Workplace Management — SLA, Incidents, CSI et Facilities

## Overview

Ce document de reference couvre la gestion des services (design de SLA/SLO/SLI, gestion des incidents, capacity management, Continual Service Improvement), le facilities management et la gestion du workplace. Il fournit les cadres, les processus et les indicateurs necessaires pour delivrer des services de qualite, gerer les environnements de travail et assurer l'amelioration continue. Utiliser ce guide pour structurer la delivery de services internes et externes, concevoir des engagements de niveau de service et piloter la performance operationnelle.

---

## SLA Design — Engagements de Niveau de Service

### Hierarchie SLI / SLO / SLA

Comprendre la distinction fondamentale entre ces trois concepts :

| Concept | Definition | Exemple | Audience |
|---|---|---|---|
| **SLI (Service Level Indicator)** | Metrique technique mesurable qui quantifie un aspect du service | Temps de reponse p99, taux de disponibilite, taux d'erreur | Equipes techniques |
| **SLO (Service Level Objective)** | Cible interne pour un SLI donne | Disponibilite >= 99.9%, latence p99 < 200ms | Equipes produit/operations |
| **SLA (Service Level Agreement)** | Contrat formel avec le client incluant les engagements de service et les penalites | Disponibilite mensuelle >= 99.5% avec credit de 10% si non atteint | Clients, direction |

**Regle fondamentale** : le SLO doit etre plus strict que le SLA pour creer un "error budget" (marge de manoeuvre). Exemple : SLA a 99.5%, SLO interne a 99.9%. L'ecart (0.4%) est le budget d'erreur consommable pour les deployments, maintenances et incidents.

### Conception d'un SLA efficace

#### Elements constitutifs d'un SLA

1. **Description du service** : perimetre exact du service couvert, exclusions explicites.
2. **Heures de service** : plages horaires de disponibilite (24/7, heures ouvrables, astreinte).
3. **Indicateurs de performance et cibles** :
   - Disponibilite (availability) : % de temps ou le service est operationnel.
   - Temps de reponse : delai pour accuser reception d'une demande/incident.
   - Temps de resolution : delai pour resoudre un incident selon sa criticite.
   - Throughput/capacite : nombre de transactions/requetes supportees.
4. **Methode de mesure** : comment les indicateurs sont mesures, outils utilises, frequence de reporting.
5. **Exclusions** : maintenances planifiees, force majeure, actions du client.
6. **Penalites et compensations** : credits de service, penalites financieres, clauses de resiliation.
7. **Processus d'escalade** : contacts, niveaux d'escalade, delais.
8. **Revue periodique** : frequence de revue du SLA, processus de modification.

#### Matrice de severite des incidents

| Severite | Definition | Temps de reponse | Temps de resolution | Exemple |
|---|---|---|---|---|
| **P1 — Critique** | Service completement indisponible ou degradation majeure impactant tous les utilisateurs | < 15 min | < 4h | Plateforme indisponible, perte de donnees |
| **P2 — Haute** | Degradation significative impactant un groupe d'utilisateurs ou une fonctionnalite majeure | < 30 min | < 8h | Fonctionnalite cle degradee, performance tres reduite |
| **P3 — Moyenne** | Impact limite sur un sous-ensemble d'utilisateurs ou fonctionnalite secondaire | < 2h | < 24h | Bug sur une fonctionnalite non critique |
| **P4 — Basse** | Impact mineur, workaround disponible | < 8h | < 5 jours ouvrables | Defaut cosmetique, amelioration mineure |

#### Error Budget Policy

L'error budget est la quantite acceptable de non-fiabilite sur une periode donnee :

```
Error Budget = 1 - SLO

Exemple avec un SLO de 99.9% de disponibilite mensuelle :
- Error budget = 0.1% d'un mois = 43.2 minutes d'indisponibilite autorisees
- Si le budget est consomme : geler les deployments de nouvelles fonctionnalites
  et concentrer les efforts sur la fiabilite

Politique d'error budget typique :
- Budget > 50% restant : deploiement normal, innovation priorisee
- Budget entre 25-50% : deploiements avec revue supplementaire
- Budget < 25% : seuls les deploiements de fiabilite sont autorises
- Budget epuise : gel complet des changements, focus 100% fiabilite
```

### Niveaux de disponibilite et impact

| Disponibilite | Indisponibilite/an | Indisponibilite/mois | Cout typique | Usage |
|---|---|---|---|---|
| 99% ("deux neuf") | 3.65 jours | 7.3 heures | Faible | Services internes non critiques |
| 99.9% ("trois neuf") | 8.76 heures | 43.8 minutes | Moyen | Applications business standard |
| 99.95% | 4.38 heures | 21.9 minutes | Eleve | Applications business critiques |
| 99.99% ("quatre neuf") | 52.6 minutes | 4.4 minutes | Tres eleve | Infrastructure critique, paiements |
| 99.999% ("cinq neuf") | 5.26 minutes | 26.3 secondes | Extreme | Systemes vitaux, telecom |

**Regle** : chaque "neuf" supplementaire coute environ 10x plus cher en infrastructure et en operations. Ne pas sur-specifier le SLA — aligner le niveau de service sur la criticite metier reelle et le budget disponible.

---

## Incident Management — Gestion des Incidents

### Processus de gestion des incidents

#### Cycle de vie d'un incident

```
Detection --> Classification --> Escalade --> Diagnostic --> Resolution --> Cloture --> Revue
    |             |                |              |              |            |          |
    v             v                v              v              v            v          v
 Monitoring   Severite P1-P4   L1->L2->L3    Root Cause    Fix/Workaround  PIR      CAPA
 Alerting     Impact/Urgence   On-call        Analysis      Deployment     Rapport   Prevention
 User report  Assignation      Management     Testing       Validation     Metrics   Standards
```

#### Niveaux de support

| Niveau | Role | Competences | Delai de prise en charge |
|---|---|---|---|
| **L0 — Self-Service** | Utilisateur autonome | Base de connaissance, FAQ, chatbot | Immediat |
| **L1 — Service Desk** | Premiere ligne de support | Scripts de diagnostic, resolution des incidents connus, escalade | < 15 min (P1), < 1h (P2) |
| **L2 — Support specialise** | Equipes techniques specialisees | Expertise domaine, analyse avancee, resolution complexe | < 30 min (P1), < 2h (P2) |
| **L3 — Expertise** | Ingenieurs, developpeurs, editeurs | Analyse code/infrastructure, patch, resolution definitive | < 1h (P1), < 4h (P2) |

#### Post-Incident Review (PIR) / Blameless Postmortem

Conduire une revue post-incident pour tout incident P1/P2. La revue est blameless (sans blame) — l'objectif est d'ameliorer le systeme, pas de trouver un coupable.

Structure d'un postmortem :

1. **Resume de l'incident** : quoi, quand, combien de temps, quel impact (utilisateurs affectes, revenue perdu).
2. **Timeline detaillee** : chronologie minute par minute des evenements, decisions et actions.
3. **Root cause analysis** : causes racines techniques et organisationnelles (utiliser les 5 Whys).
4. **What went well** : ce qui a bien fonctionne dans la reponse a l'incident (detection, communication, resolution).
5. **What went wrong** : ce qui n'a pas fonctionne (detection tardive, documentation manquante, processus de communication).
6. **Action items** : actions correctives et preventives avec responsable et date. Distinguer :
   - Actions immediates (< 1 semaine) : mitigation, monitoring supplementaire.
   - Actions moyen terme (< 1 mois) : amelioration du systeme, automatisation.
   - Actions structurelles (< 1 trimestre) : changement d'architecture, formation.
7. **Lessons learned** : apprentissages a partager avec l'organisation.

### On-Call Management

#### Principes d'une astreinte saine

- **Rotation equilibree** : repartir equitablement la charge d'astreinte entre les membres de l'equipe. Rotation hebdomadaire recommandee.
- **Compensation** : remunerer l'astreinte equitablement (prime fixe + intervention).
- **Runbooks** : documenter les procedures de diagnostic et de resolution pour les incidents courants. Chaque alerte doit avoir un runbook associe.
- **Escalade claire** : definir qui appeler quand L1 ne peut pas resoudre, avec des delais explicites.
- **Toil budget** : limiter le travail operationnel manuel (toil) a < 50% du temps de l'equipe. Automatiser les taches repetitives.
- **Bilan mensuel** : analyser le nombre d'alertes, les false positives, le temps de resolution moyen, et ajuster les seuils d'alerte.

---

## Capacity & Availability Management

### Capacity Planning

#### Processus de planification de capacite

1. **Analyser la demande actuelle** : volumetrie, patterns d'utilisation (heures de pointe, saisonnalite), tendances de croissance.
2. **Modeliser la capacite** : identifier la capacite maximale de chaque composant du systeme (serveurs, bases de donnees, reseau, equipes).
3. **Identifier les goulots** : quel composant atteindra sa limite en premier ?
4. **Prevoir la demande future** : projeter la croissance sur 6-18 mois avec des scenarios (nominal, optimiste, pic).
5. **Planifier les actions** : scaling horizontal/vertical, migration, optimisation, recrutement.
6. **Valider par des tests** : load testing, stress testing, chaos engineering.

#### Metriques de capacite

- **Utilization** : pourcentage de la capacite utilisee. Cible : < 70% en regime normal pour absorber les pics.
- **Saturation** : mesure de la surcharge (files d'attente, latence excessive). Objectif : zero saturation en regime normal.
- **Headroom** : marge de capacite disponible avant saturation. Maintenir > 30% de headroom sur les composants critiques.

### Availability Management

#### Calcul de la disponibilite composite

Pour un systeme compose de plusieurs composants :

```
Composants en serie (tous necessaires) :
  A_total = A1 x A2 x A3 x ... x An
  Exemple : 3 composants a 99.9% en serie = 99.9% x 99.9% x 99.9% = 99.7%

Composants en parallele (redondance) :
  A_total = 1 - (1-A1) x (1-A2) x ... x (1-An)
  Exemple : 2 composants a 99.9% en parallele = 1 - (0.001)^2 = 99.9999%
```

**Implication cle** : la disponibilite d'un systeme en serie est toujours inferieure a celle de son composant le plus faible. Pour augmenter la disponibilite, ajouter de la redondance sur les composants critiques.

#### Strategies de haute disponibilite

| Strategie | Description | Disponibilite typique | Cout |
|---|---|---|---|
| **Single instance** | Pas de redondance | 99-99.5% | Faible |
| **Active-Passive** | Instance secondaire en standby | 99.9% | Moyen |
| **Active-Active** | Plusieurs instances actives simultanement | 99.95-99.99% | Eleve |
| **Multi-region Active-Active** | Instances actives dans plusieurs regions | 99.99-99.999% | Tres eleve |
| **Cell-based** | Architecture cellulaire isolant les defaillances | 99.999%+ | Extreme |

---

## Continual Service Improvement (CSI)

### Le modele CSI (ITIL)

Le Continual Service Improvement assure l'alignement permanent des services IT avec les besoins metier changeants. Cycle en 7 etapes :

1. **Identifier la strategie d'amelioration** : qu'est-ce qui est important pour le business ?
2. **Definir ce que l'on va mesurer** : quels sont les indicateurs pertinents ?
3. **Collecter les donnees** : mettre en place la collecte automatisee.
4. **Traiter les donnees** : agreger, normaliser, contextualiser.
5. **Analyser les donnees** : identifier les tendances, les ecarts, les opportunites.
6. **Presenter et utiliser l'information** : communiquer aux parties prenantes avec des recommandations actionnables.
7. **Implementer les ameliorations** : prioriser et mettre en oeuvre les actions d'amelioration.

### CSI Register

Le CSI Register est le registre centralise de toutes les opportunites d'amelioration identifiees :

| Champ | Description |
|---|---|
| ID | Identifiant unique |
| Date de creation | Quand l'opportunite a ete identifiee |
| Source | D'ou vient l'idee (audit, incident, feedback, metriques) |
| Description | Description de l'amelioration proposee |
| Benefice attendu | Impact en termes de qualite, cout, satisfaction |
| Effort estime | T-shirt sizing (S/M/L/XL) |
| Priorite | Basee sur benefice/effort (matrice impact-effort) |
| Responsable | Qui porte l'initiative |
| Statut | Propose, Approuve, En cours, Complete, Rejete |
| Date cible | Echeance prevue |
| Resultat reel | Mesure du benefice realise |

### Service Review Meeting

Tenir des revues de service regulieres (mensuelles pour les services critiques, trimestrielles pour les autres) :

**Agenda type** :
1. Revue des SLA/SLO : performance vs cibles, tendances.
2. Incidents majeurs du mois : resume, root cause, actions.
3. Capacity review : utilisation, previsions, actions planifiees.
4. Change review : changements realises, impact, incidents lies.
5. Satisfaction client : NPS, CSAT, feedback qualitatif.
6. CSI update : etat d'avancement des initiatives d'amelioration.
7. Risques et problemes : risques identifies, actions de mitigation.
8. Actions et decisions.

---

## ITIL 4 — Cadre de Reference pour la Gestion des Services

### Les 4 dimensions de la gestion des services

ITIL 4 (2019) propose une approche holistique structuree autour de 4 dimensions :

1. **Organizations and People** : culture, competences, roles, communication, gestion du changement organisationnel.
2. **Information and Technology** : systemes d'information, outils, donnees, automatisation.
3. **Partners and Suppliers** : relations avec les fournisseurs, integration, contrats.
4. **Value Streams and Processes** : flux de valeur, processus, procedures, workflows.

### Service Value System (SVS)

Le SVS est le modele central d'ITIL 4 :

- **Guiding Principles** : 7 principes directeurs (Focus on value, Start where you are, Progress iteratively, Collaborate, Think holistically, Keep it simple, Optimize and automate).
- **Governance** : evaluation, direction et surveillance.
- **Service Value Chain** : 6 activites (Plan, Improve, Engage, Design & Transition, Obtain/Build, Deliver & Support).
- **Practices** : 34 pratiques organisees en 3 categories (general management, service management, technical management).
- **Continual Improvement** : boucle d'amelioration permanente a tous les niveaux.

### Pratiques ITIL 4 cles pour les operations

| Pratique | Objectif | KPI cles |
|---|---|---|
| **Incident Management** | Restaurer le service normal le plus rapidement possible | MTTR, First Call Resolution, incidents/mois |
| **Problem Management** | Eliminer les causes racines des incidents recurrents | Known errors identifies, problemes resolus/mois |
| **Change Enablement** | Maximiser les changements reussis tout en gerant les risques | Change success rate, emergency changes % |
| **Service Level Management** | Definir, mesurer et gerer les niveaux de service | SLA compliance, customer satisfaction |
| **Monitoring & Event Management** | Detecter et reagir aux evenements significatifs | Alertes traitees, faux positifs, MTTD |
| **Service Request Management** | Gerer les demandes de service standard | Temps de traitement, satisfaction, automatisation % |

---

## Facilities & Workplace Management

### Workplace Design

#### Principes de conception des espaces de travail

- **Activity-Based Working (ABW)** : concevoir des espaces adaptes aux differents types d'activites (concentration, collaboration, reunion, socialisation) plutot qu'attribuer un poste fixe a chaque personne.
- **Ratio d'occupation** : en mode hybride, un ratio de 0.6-0.8 postes par employe est typique (base sur un taux de presence de 60-80%).
- **Zonage acoustique** : creer des zones de silence, de collaboration et de socialisation avec un traitement acoustique adapte.
- **Biophilic Design** : integrer des elements naturels (plantes, lumiere naturelle, materiaux naturels) pour ameliorer le bien-etre et la productivite.
- **Accessibilite** : concevoir pour l'accessibilite universelle (PMR, malvoyants, malentendants) conformement a la reglementation (ERP en France).

### Hybrid Workplace Management

#### Modeles de travail hybride

| Modele | Description | Avantages | Defis |
|---|---|---|---|
| **Fixed hybrid** | Jours fixes au bureau/a distance (ex: lundi-mercredi bureau, jeudi-vendredi remote) | Previsible, planification facile | Rigide, ne convient pas a tous les roles |
| **Flexible hybrid** | L'employe choisit ses jours de presence | Autonomie, satisfaction | Difficile a planifier, risque de bureaux vides/surcharges |
| **Team-based hybrid** | L'equipe definit ses jours de presence ensemble | Collaboration preservee | Coordination inter-equipes complexe |
| **Remote-first** | Le remote est la norme, le bureau est un lieu de rassemblement ponctuel | Acces aux talents global, couts reduits | Isolement, culture d'entreprise |

#### Outils de gestion du workplace hybride

- **Reservation de postes (desk booking)** : applications permettant de reserver un poste ou une salle (Robin, Envoy, Deskbird, Officely).
- **Occupancy analytics** : capteurs et donnees d'acces pour mesurer l'utilisation reelle des espaces et ajuster le dimensionnement.
- **Collaboration tools** : equipement des salles de reunion pour la visioconference (equity d'experience entre presentiel et distant).
- **Communication asynchrone** : prioriser la documentation et la communication asynchrone (Notion, Confluence, Loom) pour les equipes distribuees.

### HSE (Hygiene, Securite, Environnement)

#### Cadre reglementaire (France)

- **Document Unique d'Evaluation des Risques Professionnels (DUERP)** : obligatoire pour tout employeur, mis a jour au minimum annuellement ou lors de tout changement significatif.
- **Plan de Prevention** : obligatoire pour les interventions d'entreprises exterieures.
- **Registre de securite** : suivi des verifications periodiques (installations electriques, ascenseurs, extincteurs, systemes de desenfumage).
- **Formation securite** : formations obligatoires (incendie, premiers secours, habilitations electriques, CACES pour les engins).

#### Systeme de management HSE

Structurer la demarche HSE selon l'ISO 45001:2018 :

1. **Identification des dangers** : lister tous les dangers sur chaque poste de travail (physiques, chimiques, biologiques, ergonomiques, psychosociaux).
2. **Evaluation des risques** : probabilite x gravite pour chaque danger. Prioriser les actions.
3. **Hierarchie des mesures de prevention** :
   - **Eliminer** le danger (suppression de la source).
   - **Substituer** par un danger moindre (remplacement d'un produit chimique).
   - **Isoler** le danger (protections collectives, barrages).
   - **Controles administratifs** (procedures, formation, signalisation).
   - **EPI** (equipements de protection individuelle) en dernier recours.
4. **Indicateurs** :
   - **TF1 (Taux de Frequence)** = (accidents avec arret x 1 000 000) / heures travaillees.
   - **TG (Taux de Gravite)** = (jours d'arret x 1 000) / heures travaillees.
   - **Presqu'accidents reportes** : indicateur avance (leading indicator) de la culture securite.

### Sustainability in Operations

#### Gestion energetique des batiments

- **Certification HQE/BREEAM/LEED** : certifier les batiments selon les referentiels de construction durable.
- **Building Management System (BMS)** : pilotage automatise du chauffage, de la climatisation, de l'eclairage et de la ventilation selon l'occupation reelle.
- **Decret Tertiaire (France)** : obligation de reduction de la consommation energetique des batiments tertiaires de 40% d'ici 2030, 50% d'ici 2040, 60% d'ici 2050 (reference 2010).
- **RE2020** : reglementation environnementale 2020 pour les batiments neufs (performance energetique, empreinte carbone, confort d'ete).

#### Operations durables

- **Politique zero papier** : numeriser les processus, eliminer les impressions inutiles.
- **Gestion des dechets** : tri selectif, reduction a la source, economie circulaire (mobilier reconditionne, materiel IT en seconde vie).
- **Mobilite durable** : plan de mobilite employeur, forfait mobilite durable, bornes de recharge electrique, flottes de vehicules electriques.
- **Achats responsables** : criteres RSE dans les cahiers des charges, labels et certifications fournisseurs.

---

## State of the Art (2024-2026)

### Experience Level Agreements (XLA)

L'evolution majeure en 2024-2026 est le passage des SLA (metriques techniques) aux XLA (experience utilisateur) :

- **Definition** : un XLA mesure la qualite de l'experience vecue par l'utilisateur plutot que la performance technique du service. Exemple : au lieu de "disponibilite 99.9%", mesurer "% d'utilisateurs satisfaits de leur capacite a travailler efficacement".
- **Metriques XLA typiques** :
  - **DEX Score (Digital Employee Experience)** : score composite mesurant la qualite de l'experience numerique de l'employe.
  - **Sentiment Analysis** : analyse des retours utilisateurs (tickets, surveys, commentaires) par NLP.
  - **Productivity Impact** : temps perdu par les utilisateurs du a des problemes IT.
  - **Employee Net Promoter Score (eNPS)** pour l'IT.
- **Outils** : Nexthink, Lakeside Software (SysTrack), 1E, Controlup — plateformes de Digital Experience Management (DEM) qui collectent des donnees endpoint pour mesurer l'experience reelle.
- **Shift culturel** : passer d'une culture "le SLA est vert donc tout va bien" a "les utilisateurs sont-ils reellement satisfaits et productifs ?".

### AIOps et Observabilite Avancee

L'intelligence artificielle transforme la gestion des operations IT :

- **AIOps (Artificial Intelligence for IT Operations)** : utiliser le ML pour analyser les volumes massifs de logs, metriques et traces, detecter les anomalies, correler les evenements et predire les incidents avant qu'ils n'impactent les utilisateurs.
- **Predictive Incident Management** : les algorithmes detectent les patterns precurseurs d'incidents (degradation progressive, anomalie de metriques) et declenchent des actions preventives automatiques.
- **Automated Remediation** : resolution automatique des incidents connus sans intervention humaine (auto-scaling, restart, failover, rollback). Objectif : 80% des incidents de routine resolus automatiquement.
- **Observability 2.0** : au-dela du monitoring (dashboards statiques), l'observabilite moderne (Datadog, Grafana, Dynatrace, New Relic, Honeycomb) permet l'exploration ad hoc des donnees pour diagnostiquer des problemes inedits. Le concept de "high cardinality" et "wide events" permet des analyses plus riches.

### Platform Engineering et Developer Experience

- **Internal Developer Platform (IDP)** : fournir aux equipes de developpement un portail self-service pour provisionner des environnements, deployer des services et acceder aux outils. Backstage (Spotify), Port, Humanitec.
- **Developer Experience (DevEx)** : mesurer et optimiser l'experience developpeur comme on mesure l'experience client. Les metriques SPACE (Satisfaction, Performance, Activity, Communication, Efficiency) proposees par Microsoft Research fournissent un cadre.
- **Platform as a Product** : traiter la plateforme interne comme un produit avec ses utilisateurs (les developpeurs), son product manager, sa roadmap et ses metriques de satisfaction.

### Smart Buildings et IoT Workplace

La gestion des batiments est transformee par l'IoT et l'IA :

- **Jumeaux numeriques de batiments** : modelisation 3D du batiment connectee en temps reel aux capteurs (temperature, occupation, consommation energetique, qualite de l'air) pour optimiser la gestion.
- **Occupancy Intelligence** : capteurs de presence et donnees d'acces pour comprendre comment les espaces sont reellement utilises et ajuster le dimensionnement. Reduction typique de 20-30% de la surface de bureau.
- **Indoor Environmental Quality (IEQ)** : surveillance en temps reel de la qualite de l'air (CO2, particules fines, COV), de la temperature, de l'humidite et du bruit pour garantir le confort et la sante des occupants.
- **Energy Optimization AI** : algorithmes d'IA qui pilotent le BMS (Building Management System) pour optimiser la consommation energetique en fonction de l'occupation prevue, de la meteo et des tarifs energetiques. Economies typiques de 15-30%.
- **Space-as-a-Service** : les entreprises consomment des espaces de travail en mode flexible (coworking, bureaux operes comme WeWork, IWG, Morning) plutot que de signer des baux longs.

### ITIL 4 et ESM (Enterprise Service Management)

- **Enterprise Service Management** : etendre les bonnes pratiques ITSM au-dela de l'IT vers les autres fonctions de l'entreprise (RH, Finance, Juridique, Facilities). Les plateformes ServiceNow, Jira Service Management, Freshworks s'etendent vers l'ESM.
- **Value Stream Mapping pour les services IT** : appliquer les principes Lean de VSM pour cartographier et optimiser les flux de valeur de delivery IT (du besoin utilisateur a la mise en production).
- **SRE (Site Reliability Engineering) + ITIL** : la convergence entre les pratiques SRE (Google) et ITIL 4 s'accelere. Les concepts d'error budget, de toil reduction et d'automation sont integres dans les pratiques ITIL.

### Exemples de KPI service delivery et workplace modernes

```
Service Delivery :
- SLA Compliance Rate : cible > 98%
- MTTR (Mean Time To Resolve) : P1 < 2h, P2 < 8h
- MTTD (Mean Time To Detect) : cible < 5 min
- Incident Volume Trend : reduction YoY de 10%
- Change Success Rate : cible > 95%
- First Contact Resolution : cible > 70%
- Customer Satisfaction (CSAT) : cible > 4.2/5
- Error Budget Consumption : cible < 80%/mois

Experience (XLA) :
- DEX Score : cible > 8/10
- IT Employee NPS : cible > 30
- Time Lost to IT Issues (heures/employe/mois) : cible < 2h
- Self-Service Adoption Rate : cible > 60%

Workplace :
- Occupancy Rate : cible 60-80%
- Space Cost per Employee : tracking et optimisation YoY
- Energy Use Intensity (kWh/m2/an) : reduction YoY de 5%
- Indoor Air Quality (CO2 ppm) : cible < 800 ppm
- Employee Workplace Satisfaction : cible > 4/5
- TF1 (Taux de Frequence accidents) : cible < 5

Sustainability :
- Carbon Footprint per Workspace (kgCO2/poste/an) : reduction YoY
- Waste Diversion Rate : cible > 80%
- Green Building Certification Score : progression continue
- Renewable Energy Share : cible > 50%
```

### Ressources cles

- **ITIL 4 Foundation** (Axelos) : cadre de reference pour la gestion des services IT.
- **"Site Reliability Engineering"** (Google / Betsy Beyer et al.) : pratiques SRE, error budgets, toil.
- **"The Phoenix Project"** (Gene Kim) : roman illustrant les principes DevOps et ITIL.
- **ISO/IEC 20000** : norme internationale pour les systemes de management des services IT.
- **ISO 41001** : norme internationale pour le facilities management.
- **ISO 45001** : norme internationale pour les systemes de management de la sante et de la securite au travail.
- **WELL Building Standard** : referentiel de conception des batiments centres sur la sante et le bien-etre des occupants.
- **Nexthink / Lakeside** : plateformes de Digital Experience Management pour la mesure XLA.
