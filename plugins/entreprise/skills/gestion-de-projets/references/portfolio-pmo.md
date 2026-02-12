# Portfolio & PMO — Governance, Prioritization, Capacity Planning & PMO Models

## Overview

Ce document de reference couvre la gestion de portefeuille de projets et la mise en place d'un PMO (Project Management Office) performant. Il detaille les frameworks de priorisation (RICE, MoSCoW, Weighted Scoring, Cost of Delay, WSJF), la gouvernance de portefeuille, le capacity planning, les modeles de PMO (delivery, strategic, value delivery office) et les metriques de performance du portefeuille. Utiliser ce guide pour structurer la gestion du portefeuille de projets, optimiser l'allocation des ressources et maximiser la valeur delivree a l'echelle de l'organisation.

---

## Portfolio Governance — Principes et Structure

### Objectif de la gouvernance de portefeuille

La gouvernance de portefeuille a pour objectif de s'assurer que l'organisation investit dans les bons projets, au bon moment, avec les bonnes ressources. Elle repond a trois questions cles :
1. **Faisons-nous les bons projets ?** (alignement strategique)
2. **Faisons-nous les projets correctement ?** (execution et delivery)
3. **Generons-nous la valeur attendue ?** (benefits realization)

### Structure de gouvernance type

```
[Comite de Direction / ExCom]
    |
    |-- Decisions strategiques, arbitrages majeurs
    |-- Cadence : trimestrielle
    |
[Portfolio Board / Comite de Portefeuille]
    |
    |-- Priorisation, arbitrage des ressources, go/no-go
    |-- Membres : CFO, CIO, COO, CDO, heads of BU
    |-- Cadence : mensuelle
    |
[PMO / Value Delivery Office]
    |
    |-- Execution, suivi, reporting, standards
    |-- Cadence : hebdomadaire (operationnel)
    |
[Project/Program Managers]
    |
    |-- Delivery des projets individuels
    |-- Reporting au PMO et au Portfolio Board
```

### Processus de gouvernance du portefeuille

#### 1. Intake & Qualification

Tout nouveau projet doit passer par un processus d'intake structure :
- **Soumission** : le sponsor remplit un formulaire d'intake standardise (objectif, perimetre, budget estime, benefices attendus, ressources necessaires, urgence).
- **Qualification** : le PMO verifie la completude et la coherence de la demande.
- **Scoring initial** : application du framework de priorisation (RICE, Weighted Scoring) pour positionner le projet dans le pipeline.
- **Decision** : le Portfolio Board decide du go/no-go et de la priorite relative.

#### 2. Priorisation & Sequencement

La priorisation du portefeuille s'effectue selon un processus structure :
- **Scoring multicritere** : chaque projet est score selon le framework defini (voir section dediee).
- **Contraintes de capacite** : les projets sont sequences en fonction de la capacite disponible (personnes, budget, infrastructure).
- **Dependances** : les dependances inter-projets sont identifiees et gerees (predecesseur, bloqueur).
- **Arbitrage** : le Portfolio Board tranche les conflits de ressources et les priorites ex aequo.

#### 3. Execution & Monitoring

- **Reporting standardise** : chaque projet remonte un rapport mensuel (avancement, risques, budget, benefices).
- **Stage gates** : revue formelle a chaque etape cle du projet (phase gate, PI boundary).
- **Health check** : indicateur de sante global du portefeuille (vert/orange/rouge) base sur les metriques de chaque projet.
- **Rebalancing** : revue trimestrielle du portefeuille pour reallouer les ressources, arreter les projets sans valeur, accelerer les priorites.

#### 4. Closure & Benefits Review

- **Post-implementation review** : 3-6 mois apres le go-live, revue formelle des benefices realises vs. prevus.
- **Lessons learned** : capitalisation des lecons apprises et integration dans les processus PMO.
- **Portfolio optimization** : mise a jour du scoring et resequencement du portefeuille en fonction des apprentissages.

---

## Frameworks de Priorisation — Deep Dive

### RICE Score

**Usage** : priorisation de features produit, backlog produit, initiatives a perimetre comparable.

| Composante | Definition | Echelle |
|---|---|---|
| **Reach** | Nombre d'utilisateurs/clients impactes par periode | Nombre reel (ex : 10 000 users/trimestre) |
| **Impact** | Contribution a l'objectif cible par utilisateur touche | 3 = massif, 2 = eleve, 1 = moyen, 0.5 = faible, 0.25 = minimal |
| **Confidence** | Niveau de confiance dans les estimations | 100% = eleve, 80% = moyen, 50% = faible |
| **Effort** | Charge de travail en person-months | Nombre reel (ex : 3 person-months) |

**Formule** : RICE = (Reach x Impact x Confidence) / Effort

**Exemple** :
```
Feature A : Reach=5000, Impact=2, Confidence=80%, Effort=4 person-months
RICE = (5000 x 2 x 0.8) / 4 = 2000

Feature B : Reach=20000, Impact=1, Confidence=50%, Effort=6 person-months
RICE = (20000 x 1 x 0.5) / 6 = 1667

-> Prioriser Feature A (RICE = 2000 > 1667)
```

**Limites** : RICE suppose une mesurabilite du Reach et de l'Impact, ce qui n'est pas toujours possible pour les projets infrastructure ou les initiatives non-produit.

### MoSCoW

**Usage** : definition du perimetre d'une release ou d'un sprint, arbitrage dans les projets a perimetre contraint.

| Categorie | Definition | Regle |
|---|---|---|
| **Must** | Indispensable, le projet echoue sans | Maximum 60% du budget/capacite |
| **Should** | Important, contournement difficile | 20% du budget/capacite |
| **Could** | Souhaitable, facile a reporter | 20% du budget/capacite |
| **Won't** | Exclu de cette iteration, peut-etre plus tard | Documente pour tracabilite |

**Regles d'application** :
- Ne jamais avoir plus de 60% de Must dans un scope : cela ne laisse aucune marge de manoeuvre.
- Les Should et Could servent de variable d'ajustement en cas de retard ou de contrainte de capacite.
- Les Won't ne sont pas rejetes, ils sont explicitement reportes a une iteration future.
- Valider la classification MoSCoW avec le sponsor et les parties prenantes cles.

### Weighted Scoring

**Usage** : priorisation de portefeuille strategique, comparaison de projets heterogenes (differents types, tailles, domaines).

Construire la matrice de scoring en 5 etapes :

**Etape 1** — Definir les criteres (5-8 maximum) :

| Critere | Poids | Description |
|---|---|---|
| Alignement strategique | 25% | Contribution aux objectifs strategiques |
| Valeur financiere (NPV/ROI) | 20% | Retour sur investissement projete |
| Risque (inverse) | 15% | Niveau de risque du projet (score inverse : risque faible = score eleve) |
| Urgence | 15% | Impact du delai sur la valeur (Cost of Delay) |
| Faisabilite | 15% | Disponibilite des competences, donnees, infrastructure |
| Innovation | 10% | Potentiel de disruption ou d'apprentissage |

**Etape 2** — Definir l'echelle de scoring (1-5) avec des ancres descriptives pour eviter la subjectivite.

**Etape 3** — Scorer chaque projet independamment (idealement par un panel de 3-5 evaluateurs).

**Etape 4** — Calculer le score pondere : Score = somme(score_critere x poids_critere).

**Etape 5** — Classer et trancher :
- Score > 4.0 : lancer en priorite
- Score 3.0-4.0 : planifier en vague suivante
- Score 2.0-3.0 : mettre en attente, re-evaluer trimestriellement
- Score < 2.0 : rejeter

### Cost of Delay (CoD)

**Usage** : priorisation basee sur la valeur economique du temps, ideal pour les environnements de flux (Kanban).

Le Cost of Delay mesure la perte de valeur economique causee par chaque semaine de retard dans la livraison d'un projet.

**Types de profils CoD** :

| Profil | Comportement | Exemple |
|---|---|---|
| **Standard** | Valeur constante perdue par semaine de retard | Feature produit classique |
| **Urgent / Fixed Date** | Valeur qui s'effondre a une date precise | Conformite reglementaire, evenement saisonnier |
| **Intangible** | Valeur qui augmente progressivement avec le temps | Competence, infrastructure, dette technique |
| **Exponentiel** | Cout qui s'accelere avec le temps | Faille de securite, probleme de performance |

**Calcul du CoD** :
```
CoD = Valeur annuelle du projet / 52 semaines

Exemple :
Projet A : valeur annuelle = 520 000 EUR -> CoD = 10 000 EUR/semaine
Projet B : valeur annuelle = 260 000 EUR -> CoD = 5 000 EUR/semaine
```

### WSJF — Weighted Shortest Job First

**Usage** : priorisation dans SAFe (PI Planning), combine la valeur et la duree.

**Formule** : WSJF = Cost of Delay / Job Duration

Le Cost of Delay dans SAFe est la somme de 3 composantes (echelle de Fibonacci relative : 1, 2, 3, 5, 8, 13, 20) :
- **User/Business Value** : valeur pour l'utilisateur ou le metier.
- **Time Criticality** : urgence, fenetre d'opportunite.
- **Risk Reduction / Opportunity Enablement** : reduction de risque ou ouverture de nouvelles opportunites.

**Exemple de priorisation WSJF** :

| Feature | Business Value | Time Criticality | RR/OE | CoD | Job Size | WSJF |
|---|---|---|---|---|---|---|
| A | 8 | 13 | 5 | 26 | 5 | 5.2 |
| B | 13 | 5 | 8 | 26 | 13 | 2.0 |
| C | 5 | 8 | 3 | 16 | 3 | 5.3 |

**Sequencement** : C (5.3) > A (5.2) > B (2.0). La feature C, malgre un CoD inferieur, passe en premier car sa duree courte maximise le flux de valeur.

---

## Capacity Planning

### Principes du capacity planning

Le capacity planning aligne la demande (portefeuille de projets) avec la capacite (ressources disponibles). Trois niveaux de planification :

| Niveau | Horizon | Granularite | Responsable |
|---|---|---|---|
| **Strategique** | 12-18 mois | Equipes, budgets, grandes initiatives | Portfolio Board |
| **Tactique** | 3-6 mois | Personnes par equipe, allocation par projet | PMO, Resource Managers |
| **Operationnel** | 1-4 semaines | Taches par personne, sprint planning | Scrum Master, Tech Lead |

### Methode de capacity planning tactique

**Etape 1** — Inventorier la capacite brute :
```
Capacite brute = Nombre de personnes x Jours ouvrables par periode
Exemple : 10 personnes x 65 jours/trimestre = 650 person-days
```

**Etape 2** — Calculer la capacite nette (deduire les indisponibilites) :
```
Capacite nette = Capacite brute x Facteur de disponibilite
Facteur typique : 70-80% (conges, formations, reunions, support, ceremoniels agiles)
Exemple : 650 x 0.75 = 487 person-days disponibles pour les projets
```

**Etape 3** — Allouer la capacite par categorie :
```
Repartition recommandee :
- 60-70% : projets strategiques et de croissance (Run the Business / Change the Business)
- 15-25% : maintenance, support, dette technique (Keep the Lights On)
- 10-15% : innovation, experimentations, montee en competences
```

**Etape 4** — Confronter la demande a la capacite :
- Si demande > capacite : prioriser avec le framework choisi, reporter ou arreter les projets de faible priorite.
- Si capacite > demande : accelerer les projets en cours, reduire le multi-tasking, investir dans l'innovation.

### Anti-patterns du capacity planning

- **Allocation a 100%** : ne jamais planifier les personnes a 100% de leur capacite. Viser 75-80% pour absorber les aleas et maintenir la qualite.
- **Fractionnement excessif** : eviter d'affecter une personne a plus de 2 projets simultanement. Le cout du context switching est de 20-40% de la productivite par projet additionnel.
- **Planification person-by-person** : a l'echelle strategique, planifier par equipe, pas par individu. Le micro-management des allocations individuelles ne passe pas a l'echelle.

---

## Models de PMO

### PMO de Type 1 — Delivery PMO (Supportive)

**Mission** : fournir du support, des templates et de la methodologie aux chefs de projet.

**Caracteristiques** :
- Faible autorite : le PMO conseille mais ne decide pas.
- Fournit les outils, templates, methodologies et formations.
- Centralise le reporting et les lessons learned.
- Convient aux organisations avec des chefs de projet experimentes et une culture d'autonomie.

**Equipe type** : 2-5 personnes (PMO Manager, PMO Analyst, Coordinateur).

**Metriques** :
- Taux d'utilisation des templates et standards PMO.
- Satisfaction des chefs de projet envers le support PMO.
- Qualite et ponctualite du reporting consolide.

### PMO de Type 2 — Controlling PMO (Directive)

**Mission** : garantir la conformite methodologique et controler la performance du portefeuille.

**Caracteristiques** :
- Autorite moyenne : le PMO definit les standards et verifie leur application.
- Gate reviews obligatoires a chaque phase.
- Controle du budget et du planning avec escalade sur les deviations.
- Audit regulier des projets.
- Convient aux organisations en maturite croissante qui ont besoin de standardisation.

**Equipe type** : 5-15 personnes (PMO Director, Portfolio Analysts, Project Auditors, Resource Planners).

**Metriques** :
- Taux de conformite aux gates et standards.
- Performance du portefeuille (on time, on budget, on scope).
- Taux de succes des projets (benefices realises vs. prevus).

### PMO de Type 3 — Strategic PMO / Value Delivery Office (VDO)

**Mission** : maximiser la valeur delivree par le portefeuille, aligner les projets sur la strategie, piloter les benefices.

**Caracteristiques** :
- Autorite elevee : le PMO participe aux decisions de portefeuille, conseille la direction.
- Pilotage des benefices (benefits realization management).
- Capacity planning strategique et allocation des ressources.
- Gestion des dependances inter-programmes.
- Veille methodologique et innovation (introduction de l'agilite, lean, IA).
- Convient aux organisations matures avec un portefeuille important.

**Equipe type** : 10-30 personnes (Chief Project Officer, Portfolio Managers, Benefits Managers, Agile Coaches, Resource Planners, PMO Analysts).

**Metriques** :
- ROI du portefeuille (benefices realises / investissements).
- Alignement strategique (% de projets alignes sur les objectifs strategiques).
- Time-to-value (delai moyen entre le lancement et la premiere creation de valeur).
- Health of portfolio (% de projets en vert/orange/rouge).
- Customer/stakeholder satisfaction.

### Evolution du PMO

Le PMO doit evoluer avec la maturite de l'organisation :

```
Maturite faible : Delivery PMO (supportive)
     |
     v (12-18 mois)
Maturite moyenne : Controlling PMO (directive)
     |
     v (12-18 mois)
Maturite elevee : Strategic PMO / Value Delivery Office
     |
     v (continu)
Transformation : Lean-Agile Center of Excellence (LACE)
```

Le passage d'un type a l'autre necessite un mandat clair de la direction, un renforcement des competences de l'equipe PMO et un changement de posture : du controle vers le service, du reporting vers la valeur.

---

## Benefits Realization Management

### Cycle de vie des benefices

Le benefits realization management (BRM) est le processus de s'assurer que les benefices attendus d'un projet sont effectivement realises. Il couvre 5 etapes :

#### 1. Benefits Identification

Identifier les benefices des le business case :
- **Benefices tangibles** : quantifiables en EUR (reduction de couts, augmentation de revenus, gain de productivite).
- **Benefices intangibles** : qualitatifs mais mesurables (satisfaction client, engagement employes, reputation).
- **Dis-benefits** : effets negatifs attendus du changement (ex : baisse temporaire de productivite pendant la transition).

#### 2. Benefits Quantification

Pour chaque benefice, definir :
- **Metrique** : l'indicateur mesurable (ex : temps de traitement d'une commande).
- **Baseline** : la valeur actuelle avant le projet (ex : 45 minutes).
- **Target** : la valeur cible apres le projet (ex : 15 minutes).
- **Valeur financiere** : traduction en EUR si possible (ex : gain de 30 min x 10 000 commandes/an x 50 EUR/heure = 250 000 EUR/an).
- **Owner** : la personne responsable de la realisation du benefice (generalement un manager metier, pas le chef de projet).

#### 3. Benefits Planning

Planifier la realisation des benefices :
- **Timing** : quand le benefice commencera a se materialiser (souvent 3-6 mois apres le go-live, pas immediatement).
- **Pre-requis** : conditions necessaires a la realisation (formation des utilisateurs, migration des donnees, changement de processus).
- **Dependances** : autres projets ou changements necessaires.
- **Risques** : facteurs pouvant empecher la realisation (adoption insuffisante, resistance, conditions de marche).

#### 4. Benefits Tracking

Suivre la realisation des benefices en continu :
- **Benefits Register** : document central de suivi de tous les benefices identifies.
- **Cadence de suivi** : mensuelle pour les benefices operationnels, trimestrielle pour les benefices strategiques.
- **Reporting** : dashboard de benefices integre au reporting du portefeuille.
- **Escalade** : si la realisation d'un benefice devie significativement de la cible, escalader au Portfolio Board.

#### 5. Post-Implementation Review (PIR)

Revue formelle 6-12 mois apres le go-live :
- Comparer les benefices realises vs. prevus pour chaque metrique.
- Analyser les ecarts (pourquoi certains benefices n'ont pas ete realises, pourquoi d'autres ont depasse les previsions).
- Documenter les lecons apprises pour le benefice des projets futurs.
- Decider des actions correctives si des benefices ne sont pas au rendez-vous.

### Exemple de Benefits Register

| ID | Benefice | Type | Metrique | Baseline | Target | Realise | Owner | Statut |
|---|---|---|---|---|---|---|---|---|
| B-001 | Reduction du temps de traitement des commandes | Tangible | Temps moyen/commande | 45 min | 15 min | 20 min | Dir. Operations | En cours |
| B-002 | Amelioration de la satisfaction client | Intangible | NPS | 32 | 50 | 45 | Dir. Service Client | En cours |
| B-003 | Reduction des erreurs de saisie | Tangible | Taux d'erreur | 5% | 1% | 1.5% | Dir. Qualite | En cours |
| B-004 | Baisse temporaire de productivite | Dis-benefit | Productivite equipe | 100% | -15% pendant 3 mois | -20% pendant 4 mois | Dir. Operations | Clos |

---

## Metriques de Performance du Portefeuille

### Dashboard portefeuille type

Un dashboard de portefeuille efficace couvre 4 dimensions :

#### 1. Health — Sante du portefeuille

| Metrique | Definition | Cible |
|---|---|---|
| % projets en vert | Projets dans les tolerances (cout, delai, perimetre) | > 70% |
| % projets en rouge | Projets en deviation critique | < 10% |
| Nombre de projets actifs | Charge du portefeuille | Aligne avec la capacite |
| Age moyen des projets | Duree moyenne des projets en cours | En diminution |

#### 2. Value — Valeur delivree

| Metrique | Definition | Cible |
|---|---|---|
| ROI du portefeuille | Benefices realises / Investissements | > 150% a 3 ans |
| Time-to-value | Delai moyen lancement -> premiere valeur | < 6 mois |
| Benefits realization rate | Benefices realises / Benefices prevus | > 80% |
| % projets avec benefices mesures | Projets ayant fait l'objet d'une PIR | 100% des projets >100k EUR |

#### 3. Flow — Flux du portefeuille

| Metrique | Definition | Cible |
|---|---|---|
| Throughput | Nombre de projets completes par trimestre | Stable ou en augmentation |
| Lead time portefeuille | Delai intake -> go-live | En diminution |
| WIP | Nombre de projets en cours | Limite (capacite disponible) |
| Taux d'abandon | % de projets arretes avant completion | < 15% (mais > 0% : savoir arreter) |

#### 4. Alignment — Alignement strategique

| Metrique | Definition | Cible |
|---|---|---|
| % budget aligne sur les priorites strategiques | Investissement projet dans les axes strategiques | > 80% |
| Couverture des objectifs strategiques | Objectifs strategiques couverts par au moins un projet | 100% |
| Balance du portefeuille | Repartition Run/Grow/Transform | Selon la strategie (ex : 50/30/20) |

---

## State of the Art (2024-2026)

### Lean Portfolio Management (LPM)

Le Lean Portfolio Management, promu par SAFe mais applicable independamment, remplace la gouvernance de portefeuille traditionnelle par une approche plus legere et adaptative :
- **Strategy & Investment Funding** : allocation budgetaire par value stream plutot que par projet. Chaque value stream recoit un budget annuel qu'il gere en autonomie, sans avoir a faire approuver chaque projet individuellement.
- **Agile Portfolio Operations** : gestion du flux de valeur avec un Portfolio Kanban, des limites WIP au niveau portefeuille, et des cadences legeres (Portfolio Sync mensuel au lieu de comites de pilotage lourds).
- **Lean Governance** : garde-fous legers mais efficaces — guardrails budgetaires, epics avec Lean Business Case (pas de business case de 50 pages), decision rapide (Participatory Budgeting).

### Product Operating Model

L'evolution majeure 2024-2026 est le passage du "project model" au "product operating model" :
- Les organisations passent du **financement par projet** (budget alloue a un projet temporaire) au **financement par produit** (budget alloue a une equipe produit persistante).
- Les equipes sont **stables et persistantes**, pas assemblees et dissoutes a chaque projet.
- Le PMO evolue vers un **Value Delivery Office** qui pilote les outcomes plutot que les livrables.
- Les metriques evoluent : de "on time, on budget" vers "time-to-value, customer satisfaction, business impact".

### AI-Powered Portfolio Management

L'IA transforme la gestion de portefeuille :
- **Predictive portfolio analytics** : prevision de la performance du portefeuille basee sur les donnees historiques et les tendances actuelles. Identification precoce des projets a risque avant que les indicateurs classiques ne virent au rouge.
- **Automated scoring** : scoring automatique des demandes de projet basee sur l'analyse du texte, les donnees historiques de projets similaires, et les patterns de succes/echec.
- **Resource optimization** : allocation optimisee des ressources par algorithmes, prenant en compte les competences, la disponibilite, les preferences et les contraintes multi-projets.
- **Scenario simulation** : simulation de l'impact de differents scenarios de priorisation (what-if analysis) sur la valeur totale du portefeuille, le risque agrege et la capacite.

### OKR-Driven Portfolio

L'alignement OKR-portefeuille se generalise :
- Les **Objectives** definissent les priorites strategiques de l'organisation.
- Les **Key Results** mesurent le succes et alimentent les criteres de priorisation du portefeuille.
- Chaque projet du portefeuille est explicitement lie a un ou plusieurs Key Results.
- La revue OKR trimestrielle et la revue de portefeuille sont synchronisees.
- Les outils integrent cette vision : Jira Align, Targetprocess, Aha!, Productboard.

### Continuous Funding Models

Le modele traditionnel de financement par projet (budget alloue en debut d'annee, immobilise jusqu'a la fin) cede la place a des modeles plus fluides :
- **Incremental funding** : budget alloue par increment (trimestriel), avec revue et reallocation a chaque iteration.
- **VC-style funding** : les initiatives sont financees comme des investissements (seed, series A, series B) avec des gates de financement basees sur les resultats demontres.
- **Participatory budgeting** : les parties prenantes participent a l'allocation budgetaire de maniere collaborative plutot que hierarchique.
- **Zero-based portfolio** : chaque cycle budgetaire, tous les projets doivent re-justifier leur existence plutot que de reconduire automatiquement le budget precedent.
