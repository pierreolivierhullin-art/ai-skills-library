# Product Discovery -- Methodes, Frameworks & Experimentation

## Overview

Ce document de reference couvre les methodes et frameworks essentiels de product discovery : Opportunity Solution Trees, assumption mapping, prototypage multi-fidelite, techniques d'experimentation rapide, et Dual-Track Agile. Il fournit les outils pratiques pour reduire l'incertitude avant d'investir en developpement, valider les hypotheses critiques et maintenir une cadence de discovery continue. Appliquer ces methodes systematiquement pour maximiser la probabilite de construire des produits qui creent de la valeur pour les utilisateurs et pour le business.

---

## Opportunity Solution Trees (OST)

### Principes Fondamentaux — Methode Teresa Torres

L'Opportunity Solution Tree est un framework visuel de decision produit developpe par Teresa Torres. Il structure le raisonnement depuis l'objectif business jusqu'aux experimentations terrain. Utiliser l'OST comme artefact central du product trio (PM, designer, engineer) pour aligner les decisions de discovery.

### Structure de l'Arbre

```
                    [Outcome]
                       |
          +------------+------------+
          |            |            |
    [Opportunity]  [Opportunity]  [Opportunity]
          |            |
     +----+----+    +--+--+
     |         |    |     |
 [Solution] [Sol]  [Sol] [Sol]
     |
  +--+--+
  |     |
[Exp] [Exp]
```

**Niveau 1 — Outcome (Resultat mesurable)**
Definir un outcome produit lie a un objectif business. L'outcome doit etre mesurable, influencable par l'equipe produit, et formule en comportement utilisateur observable. Ne pas confondre outcome et output (fonctionnalite livree).

| Critere | Bon Outcome | Mauvais Outcome |
|---|---|---|
| Mesurable | "Augmenter le taux de completion du onboarding de 40% a 60%" | "Ameliorer l'experience utilisateur" |
| Influencable | "Reduire le time-to-first-value a < 5 min" | "Augmenter le chiffre d'affaires de 20%" |
| Oriente comportement | "Augmenter le nombre d'utilisateurs qui invitent un collegue dans les 7 premiers jours" | "Lancer la feature X avant le Q3" |

**Niveau 2 — Opportunities (Besoins, douleurs, desirs)**
Les opportunities sont les besoins utilisateurs, pain points et desirs non satisfaits identifies par la recherche continue. Extraire les opportunities des interviews utilisateurs (minimum 1 interview/semaine par product trio). Structurer les opportunities en arbre hierarchique : les opportunities parentes sont larges, les enfants sont specifiques et actionnables. Formuler du point de vue de l'utilisateur, utiliser le verbatim des interviews, prioriser selon la frequence, l'intensite et le potentiel d'impact sur l'outcome.

**Niveau 3 — Solutions**
Generer au minimum 3 solutions par opportunity selectionnee. Ne jamais s'engager sur la premiere idee. Utiliser des techniques de divergence (Crazy 8s, How Might We, analogies inter-industries) pour elargir l'espace des solutions.

**Niveau 4 — Experiments (Assumption Tests)**
Chaque solution porte des hypotheses. Identifier l'hypothese la plus risquee et concevoir l'experience la plus petite possible pour la tester. L'objectif est d'apprendre, pas de prouver qu'on a raison.

### Erreurs Frequentes avec les OST

| Erreur | Diagnostic | Correction |
|---|---|---|
| Outcome = output | L'equipe definit "lancer la feature X" comme outcome | Reformuler en comportement utilisateur mesurable |
| Opportunities inventees | Pas de lien avec la recherche utilisateur | Ancrer chaque opportunity dans un verbatim d'interview |
| Une seule solution par opportunity | Biais de confirmation, attachement a la premiere idee | Imposer le "rule of three" : 3 solutions minimum |
| Experiments trop gros | L'experiment ressemble a un MVP complet | Reduire au plus petit test validant l'hypothese la plus risquee |
| Arbre statique | L'OST n'evolue pas avec les apprentissages | Mettre a jour l'OST chaque semaine lors du weekly discovery |

---

## Assumption Mapping

### Les Quatre Dimensions du Risque Produit

Tout produit ou fonctionnalite porte quatre types de risques. Mapper les assumptions sur ces quatre dimensions avant d'investir en developpement.

| Dimension | Question Cle | Methodes de Validation |
|---|---|---|
| **Desirability** (Desirabilite) | Les utilisateurs veulent-ils cette solution ? | Interviews, surveys, fake door tests, landing pages |
| **Viability** (Viabilite business) | Cette solution fonctionne-t-elle pour notre business ? | Business model canvas, unit economics, pricing tests |
| **Feasibility** (Faisabilite technique) | Pouvons-nous construire cette solution ? | Spike technique, PoC, architecture review |
| **Usability** (Utilisabilite) | Les utilisateurs savent-ils utiliser la solution ? | Tests d'utilisabilite, prototypes clickables, first-click tests |

### Matrice de Priorisation des Assumptions

Classer chaque assumption selon deux axes : le niveau de risque (probabilite que l'assumption soit fausse) et le niveau d'impact (consequence si l'assumption est fausse).

```
          IMPACT ELEVE
               |
    TESTER     |    TESTER
    EN PRIORITE|    RAPIDEMENT
    (critique) |    (important)
               |
  -------------+-------------
               |
    SURVEILLER |    IGNORER
    (mineur)   |    (negligeable)
               |
          IMPACT FAIBLE

  RISQUE ELEVE          RISQUE FAIBLE
```

### Template d'Assumption Map

| # | Assumption | Dimension | Risque (1-5) | Impact (1-5) | Score | Methode de Test | Critere de Succes |
|---|---|---|---|---|---|---|---|
| A1 | Les PME ont besoin de rapports automatises | Desirability | 4 | 5 | 20 | Fake door test | > 5% CTR sur CTA |
| A2 | Les utilisateurs comprennent le dashboard | Usability | 3 | 4 | 12 | Test utilisabilite 5 users | > 80% task completion |
| A3 | L'API partenaire supporte le volume | Feasibility | 2 | 5 | 10 | Spike technique 2 jours | < 200ms latence p95 |
| A4 | Le pricing a 49 EUR/mois est acceptable | Viability | 3 | 3 | 9 | Van Westendorp survey | Range 35-65 EUR |

Tester les assumptions dans l'ordre decroissant du score (Risque x Impact). Commencer par les assumptions de desirabilite : si les utilisateurs ne veulent pas de la solution, la faisabilite et l'utilisabilite sont sans objet.

---

## Methodes de Prototypage

### Spectre de Fidelite

Choisir le niveau de fidelite en fonction de ce que l'on cherche a valider. Monter en fidelite uniquement quand le niveau inferieur ne suffit plus.

| Niveau | Temps de Creation | Ce qu'on Valide | Outils |
|---|---|---|---|
| **Paper prototype** (croquis, post-its) | 15-60 min | Flux, architecture d'information, retours conceptuels | Papier, marqueurs |
| **Wireframe statique** (basse fidelite, niveaux de gris) | 2-4 h | Structure, hierarchie de l'information, navigation | Balsamiq, Whimsical |
| **Prototype clickable** (haute fidelite, interactions) | 1-3 jours | Utilisabilite, comprehension des parcours, desirabilite | Figma, Framer, ProtoPie |
| **Prototype code** (version fonctionnelle) | 3-10 jours | Faisabilite technique, performance, usage reel | React, Swift, Storybook |

### Arbre de Decision du Prototypage

```
Que cherche-t-on a valider ?
|
+-- Concept / proposition de valeur
|   +-- Audience interne --> Paper prototype
|   +-- Utilisateurs finaux --> Wireframe + interview
|
+-- Parcours utilisateur / navigation
|   +-- Flux simple (< 5 ecrans) --> Wireframe statique
|   +-- Flux complexe / conditionnel --> Prototype clickable
|
+-- Utilisabilite / interactions detaillees
|   +-- Patterns standards (formulaire, liste) --> Wireframe annote
|   +-- Interactions nouvelles --> Prototype clickable haute fidelite
|
+-- Faisabilite technique / performance
    +-- Question d'architecture --> Spike technique (pas de prototype UI)
    +-- UX dependant de la performance --> Prototype code
```

### Bonnes Pratiques de Prototypage

- Ne jamais prototyper sans question de recherche explicite. Definir ce qu'on teste avant de construire.
- Privilegier la vitesse sur la perfection. Un prototype est jetable par nature.
- Inclure des donnees realistes dans les prototypes haute fidelite : les utilisateurs reagissent differemment face a "Lorem ipsum" versus des donnees contextuelles.
- Tester chaque prototype avec 5 utilisateurs (regle Nielsen-Norman : 5 tests detectent ~85% des problemes d'utilisabilite).

---

## Techniques d'Experimentation

### Panorama des Methodes

| Technique | Principe | Effort | Delai | Meilleur Usage |
|---|---|---|---|---|
| **Fake Door Test** | CTA ou feature visible mais non fonctionnelle | Faible | 1-3 jours | Valider la desirabilite d'une feature |
| **Painted Door Test** | Bouton ou lien dans le produit existant | Tres faible | < 1 jour | Mesurer l'interet in-product |
| **Wizard of Oz** | Service semble automatise, opere manuellement en coulisse | Moyen | 1-2 sem. | Valider un service complexe (IA, matching) |
| **Concierge** | Service delivre manuellement, de maniere transparente | Moyen | 2-4 sem. | Comprendre le besoin en profondeur |
| **Smoke Test** | Landing page + formulaire d'inscription | Faible | 2-5 jours | Valider desirabilite d'un nouveau produit |
| **A/B Test** | Deux variantes en parallele, mesure statistique | Moyen-eleve | 1-4 sem. | Optimiser une experience existante |
| **Pre-commande** | Proposer l'achat avant que le produit existe | Faible | 3-7 jours | Valider le willingness-to-pay |

### Exemples Detailles

**Fake Door Test — SaaS B2B** : ajouter un bouton "Exporter en PDF" dans l'interface. Au clic, afficher "Cette fonctionnalite arrive bientot. Souhaitez-vous etre notifie ?". Seuil de decision : > 3% des utilisateurs actifs cliquent en 2 semaines.

**Wizard of Oz — Marketplace** : valider un algorithme de matching en realisant le matching manuellement. Les utilisateurs croient interagir avec un algorithme. Mesurer le NPS des matchs (> 50) et le taux de conversion (> 25%).

**Concierge — Fintech** : offrir un service de conseil financier manuellement a 20 clients pilotes. Documenter chaque interaction pour specifier l'algorithme d'automatisation futur.

**Smoke Test — Nouveau Produit** : creer une landing page avec CTA "Rejoindre la liste d'attente". Budget : 500-1000 EUR en acquisition. Seuil : > 10% conversion B2C, > 5% B2B.

### Arbre de Decision Experimentation

```
Que cherche-t-on a valider ?
|
+-- Desirabilite (les gens veulent-ils ca ?)
|   +-- Nouveau produit --> Smoke test (landing page)
|   +-- Nouvelle feature, simple a comprendre --> Fake door in-product
|   +-- Nouvelle feature, complexe --> Prototype clickable + interviews
|
+-- Viabilite (le business model fonctionne ?)
|   +-- Pricing --> Pre-commande ou Van Westendorp survey
|   +-- Unit economics --> Concierge (mesurer le cout reel)
|
+-- Faisabilite (peut-on le construire ?)
|   +-- Technologie connue --> Spike technique (1-2 jours)
|   +-- Technologie inconnue --> PoC technique (1-2 semaines)
|
+-- Utilisabilite (les gens comprennent ?)
    +-- Flux nouveau --> Test utilisabilite sur prototype (5 users)
    +-- Optimisation existante --> A/B test (si trafic suffisant)
```

---

## Dual-Track Agile

### Principe Fondamental

Le Dual-Track Agile separe deux flux de travail alimentant le meme backlog :
- **Discovery Track** : explorer le probleme, tester des solutions, reduire l'incertitude. Resultat : backlog d'items valides avec preuves d'impact.
- **Delivery Track** : construire et livrer les solutions validees. Resultat : increment produit fonctionnel et mesurable.

### Implementation Detaillee

| Aspect | Discovery Track | Delivery Track |
|---|---|---|
| **Objectif** | Reduire l'incertitude | Construire et livrer |
| **Equipe** | Product trio (PM + Designer + Tech Lead) | Equipe de developpement complete |
| **Cadence** | Continue (pas de sprints) | Sprints de 2 semaines ou flux continu |
| **Artefacts** | OST, assumption maps, resultats d'experiments | User stories, code, tests |
| **Ceremonies** | Weekly discovery sync, interviews hebdo | Sprint planning, daily, review, retro |
| **Metriques** | Experiments/semaine, taux de validation | Velocity, cycle time, defect rate |

### Handoff Discovery vers Delivery

1. **Discovery Brief** : le product trio redige un document contenant le probleme (avec preuves), la solution recommandee, les hypotheses testees, les risques residuels et les criteres de succes.
2. **Review croisee** : l'equipe delivery challenge le brief (faisabilite, estimation, edge cases).
3. **Story Mapping** : decouper la solution en user stories livrables, definir le MVP de la feature.
4. **Prioritisation** : integrer dans le backlog delivery selon impact, effort et dependances.

### Anti-Patterns du Dual-Track

| Anti-Pattern | Symptome | Remediation |
|---|---|---|
| Discovery en silo | Le PM fait la discovery seul | Imposer le product trio sur chaque interview et decision |
| Discovery trop en avance | 3+ mois de discovery non livree | Limiter le WIP discovery a 2-3 opportunities |
| Delivery sans discovery | Pas de preuve de valeur dans le backlog | Validation minimale obligatoire avant tout sprint |
| Pas de mesure post-delivery | On livre sans verifier l'impact | Success metrics avant dev, mesure a J+28 |

---

## Discovery Cadence — Rythme Hebdomadaire

### Planning du Product Trio

| Jour | Activite | Duree | Output |
|---|---|---|---|
| **Lundi** | Weekly Discovery Sync : revue des apprentissages, MAJ de l'OST, plan des experiments | 60 min | OST mis a jour, plan semaine |
| **Mardi** | Interviews utilisateurs (2 sessions) | 2 x 30 min | Notes, nouveaux verbatims |
| **Mercredi** | Prototypage et preparation des experiments | Async | Prototypes, materiaux de test |
| **Jeudi** | Tests d'utilisabilite ou execution des experiments | 2-3 h | Resultats, insights |
| **Vendredi** | Synthese, documentation, communication stakeholders | 45 min | Synthese hebdo, brief stakeholders |

### Regles de Cadence

- Minimum 1 interview utilisateur par semaine par product trio. Non negociable.
- Minimum 1 experiment par semaine. Aucune hypothese validee/invalidee en une semaine = rythme insuffisant.
- Mettre a jour l'OST chaque semaine. Un OST statique pendant 2 semaines signale un probleme.
- Timeboxer les experiments : duree maximale et critere de decision fixes avant le lancement.

---

## Stakeholder Management en Discovery

### Matrice d'Implication

| Role | Implication | Frequence | Format |
|---|---|---|---|
| **C-level / Sponsor** | Informe des outcomes et decisions majeures | Mensuel | Discovery report 1 page |
| **Head of Product** | Aligne sur les outcomes, challenge les priorites | Hebdomadaire | Weekly 1:1, acces OST |
| **Product trio** | Co-decisionnaire | Quotidien | Rituels discovery, Slack dedie |
| **Equipe delivery** | Implique au handoff et story mapping | A chaque handoff | Discovery briefs |
| **Sales / CS / Support** | Source d'insights | Bi-mensuel | Feedback loop meeting |

### Principes de Communication

- Ne jamais communiquer un experiment comme une "feature a venir". Vocabulaire : "nous explorons", "nous testons l'hypothese que".
- Partager les invalidations autant que les validations. Formuler : "Nous avons appris que X ne repond pas au besoin, ce qui nous concentre sur Y".
- Adapter le detail au public : donnees brutes pour le trio, synthese pour le management, impact business pour les C-level.
- Maintenir un "Discovery Log" accessible : registre de toutes les hypotheses testees, resultats et decisions.

---

## Pieges Courants de la Discovery

### Top 10 des Erreurs et Diagnostics

| # | Piege | Symptome | Remediation |
|---|---|---|---|
| 1 | **Solution-first thinking** | L'equipe commence par la solution et cherche un probleme | Revenir aux interviews, reformuler les opportunities en besoins |
| 2 | **Discovery theatre** | Interviews sans changement de direction | Imposer une decision apres chaque experiment : pivoter, perseverer ou arreter |
| 3 | **Analysis paralysis** | Aucun experiment en cours depuis 3+ semaines | Timeboxer, lancer un experiment imparfait |
| 4 | **Confirmation bias** | Les interviews ne contiennent jamais de surprises | Former aux techniques d'interview non biaisees |
| 5 | **Feature factory** | Backlog = liste de demandes stakeholders | Instaurer un processus de validation obligatoire |
| 6 | **Discovery en chambre** | Insights exclusivement de la data, pas d'utilisateurs reels | Imposer "1 interview/semaine minimum" |
| 7 | **Prototype trop fidele** | Ratio creation/test > 3:1 | Baisser la fidelite au minimum necessaire |
| 8 | **Pas de critere de succes** | Resultats toujours interpretes positivement | Definir seuil et critere AVANT l'experiment |
| 9 | **Discovery solo** | Seul le PM fait la discovery | Constituer le product trio, impliquer les 3 roles |
| 10 | **Ignorer les signaux faibles** | Disruptions venant de besoins non detectes | Reserver 20% du temps a l'exploration non dirigee |

---

## Etat de l'Art 2025-2026

### Intelligence Artificielle dans la Discovery

**Analyse automatisee des interviews** — Les outils (Dovetail, Grain) transcrivent en temps reel, taguent les themes et identifient des patterns sur des dizaines d'interviews. Reduction de 60-70% du temps d'analyse. Utiliser l'IA pour l'extraction, garder l'equipe pour la synthese et les decisions.

**Synthese d'insights a grande echelle** — Les LLM agregent des volumes massifs de feedback (tickets support, avis, NPS verbatims) pour identifier les opportunities emergentes. Attention : ne pas se fier exclusivement aux syntheses IA sans echantillonnage de validation.

**Prototypage assiste par IA** — Les outils (Figma AI, Galileo AI, v0 by Vercel) accelerent la creation de prototypes. Un PM peut generer un wireframe en minutes. Le designer reste essentiel pour la finition et les tests d'utilisabilite.

**Simulation d'utilisateurs** — Des LLM simulent des reponses utilisateurs pour pre-filtrer les concepts faibles. Traiter comme un outil de tri, pas comme une validation.

### Evolution des Outils

| Categorie | Outils de Reference | Tendance 2025-2026 |
|---|---|---|
| **Research Repository** | Dovetail, EnjoyHQ, Condens | Repositories centralises alimentes par IA |
| **Prototypage** | Figma, Framer, ProtoPie | Generation IA, prototypes conversationnels |
| **Experimentation** | LaunchDarkly, Optimizely, Statsig | Feature flagging democratise, analyses bayesiennes |
| **Product Analytics** | Amplitude, Mixpanel, PostHog | Convergence analytics + session replay + flags |
| **OST / Strategy** | Productboard, Vistaly, Miro | Outils OST integres aux repositories d'insights |
| **Interview / Testing** | UserTesting, Maze, Lyssna | Tests asynchrones, recrutement automatise |

### Tendances Emergentes

- **Continuous discovery as a service** : plateformes integrees proposant un workflow end-to-end de la recherche a la priorisation.
- **Democratisation de la discovery** : outils low-barrier (Loom, Tally, Maze) permettant aux equipes sans chercheur UX dedie de maintenir une cadence.
- **Quantified discovery** : metriques dediees — interviews/semaine, hypotheses testees/sprint, ratio validation/invalidation, time-to-insight.
- **Discovery ops** : emergence du role Research Ops gerant l'infrastructure (panels, templates, repository) pour liberer les product trios.

---

## Templates Pratiques

### Discovery Brief (Handoff vers Delivery)

```
DISCOVERY BRIEF — [Nom de l'initiative]
Date : [JJ/MM/AAAA] | Product Trio : [PM, Designer, Tech Lead]

1. PROBLEME UTILISATEUR
   Description : [2-3 phrases, avec citation verbatim]
   Frequence : [% d'utilisateurs] | Intensite : [1-5] | Source : [interviews, analytics, support]

2. SOLUTION RECOMMANDEE
   Description : [3-5 phrases] | Prototype : [lien]
   Alternatives evaluees : [2+ alternatives et raisons du rejet]

3. HYPOTHESES TESTEES
   | Hypothese | Methode | Resultat | Statut (Validee/Invalidee) |

4. RISQUES RESIDUELS
   [Risque] : [mitigation prevue]

5. CRITERES DE SUCCES EN PRODUCTION
   Primaire : [metrique] de [baseline] a [cible] en [delai]
   Garde-fou : [metrique qui ne doit pas se degrader]
```

### Experiment Report

```
EXPERIMENT REPORT — [Nom]
Hypothese : Si nous faisons X, alors Y, mesure par Z
Methode : [fake door / wizard of oz / prototype test / etc.]
Duree : [jours] | Echantillon : [nombre de participants]

RESULTATS
Critere de succes : [seuil] | Resultat : [donnees] | Statut : VALIDE / INVALIDE / NON CONCLUANT

APPRENTISSAGES CLES
1. [Apprentissage 1]  2. [Apprentissage 2]  3. [Apprentissage 3]

DECISION
[ ] Delivery  [ ] Iterer  [ ] Pivoter  [ ] Arreter
PROCHAINE ETAPE : [action + responsable + date]
```
