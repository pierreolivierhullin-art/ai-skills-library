---
name: user-research
description: This skill should be used when the user asks about "user research", "user interviews", "usability testing", "UX research", "personas", "user personas", "jobs to be done", "JTBD", "customer discovery", "user journey mapping", "card sorting", "tree testing", "survey design", "A/B testing qualitative", "diary study", "ethnographic research", "contextual inquiry", "focus group", "design sprint research", "recherche utilisateur", "entretiens utilisateurs", "tests d'utilisabilité", "parcours utilisateur", "carte d'empathie", "empathy map", "découverte client", "besoin utilisateur", "user needs", "voice of customer", "VoC", "unmoderated testing", "moderated testing", "prototype testing", "assumption testing", "research repository", "insight management", "research ops", discusses user research methods and analysis, or needs guidance on understanding users, validating assumptions, or testing product concepts.
version: 1.0.0
last_updated: 2026-02
---

# User Research & Product Discovery

## Overview

Ce skill couvre l'ensemble des methodes de recherche utilisateur et de decouverte produit, de la planification d'une etude a la synthese des insights et a leur activation dans les decisions produit. Il integre les approches qualitatives (interviews, tests d'utilisabilite, observations) et quantitatives (surveys, analytics, A/B tests) dans un cadre rigoureux et actionnable. Appliquer systematiquement les principes decrits ici pour structurer chaque initiative de recherche, en privilegiant la rigueur methodologique (chaque etude a un objectif et un protocole), l'objectivite (separer observation et interpretation), et l'impact (un insight sans action est un insight inutile). La recherche utilisateur n'est pas une validation de ce qu'on veut construire : c'est un outil de reduction de l'incertitude qui doit rester ouvert a la decouverte de verites inconfortables.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Planification d'une etude de recherche** : definition des objectifs, choix de la methode, recrutement des participants, redaction du protocole, dimensionnement de l'echantillon.
- **Entretiens utilisateurs** : entretiens exploratoires, entretiens de decouverte (discovery interviews), entretiens de validation, entretiens de switch (pourquoi les utilisateurs changent de solution), scripts et techniques d'interview.
- **Tests d'utilisabilite** : tests moderes et non-moderes, protocoles think-aloud, tests de premier clic, tests de 5 secondes, evaluation heuristique, tests de prototypes.
- **Methodes d'observation** : etude ethnographique, contextual inquiry, diary studies, shadowing, observation terrain.
- **Methodes quantitatives** : conception de surveys (questionnaires), analyse statistique des reponses, card sorting, tree testing, NPS/CSAT/CES, benchmarking UX.
- **Synthese et activation des insights** : analyse thematique, affinity mapping, creation de personas data-driven, journey mapping, construction du research repository, communication des insights.
- **Research Ops** : gouvernance de la recherche, tooling, recrutement de participants, ethique et consentement, democratisation de la recherche dans l'organisation.

## Core Principles

### Principle 1 -- Research is Not Validation

La recherche utilisateur n'est pas un exercice de confirmation de ce qu'on croit deja savoir. Son objectif est de reduire l'incertitude et de decouvrir ce qu'on ne sait pas encore. Formuler les objectifs de recherche sous forme de questions ouvertes ("Comment les utilisateurs gerent-ils X ?") et non de questions fermees ("Est-ce que les utilisateurs aiment notre feature Y ?"). Si la conclusion de chaque etude confirme les hypotheses de depart, c'est un signal de biais de confirmation, pas de bonne research.

### Principle 2 -- Behavioral Over Declarative

Ce que les gens disent qu'ils font est different de ce qu'ils font reellement. Privilegier l'observation du comportement reel (tests d'utilisabilite, analytics, diary studies) aux declarations d'intention (sondages, focus groups). Quand des donnees declaratives sont necessaires (surveys), les croiser avec des donnees comportementales. La hierarchie de fiabilite : donnees comportementales observees > donnees comportementales auto-reportees > intentions declarees > opinions.

### Principle 3 -- Right Method for the Right Question

Chaque methode de recherche repond a des types de questions specifiques. Ne pas utiliser des interviews pour des questions quantitatives, ni des surveys pour des questions exploratoires. Choisir la methode en fonction de : (1) le type de question (exploratoire, evaluative, generative), (2) la phase produit (discovery, design, delivery, post-launch), (3) les contraintes (temps, budget, acces aux utilisateurs). Combiner au minimum une methode qualitative et une methode quantitative par cycle de recherche (triangulation).

### Principle 4 -- Continuous Over Episodic

Integrer la recherche dans le rythme continu de l'equipe produit, pas comme une phase ponctuelle avant un gros projet. Viser 2-3 entretiens utilisateurs par semaine par product trio. Maintenir un panel de participants recrutables en permanence. La recherche continue permet de detecter les problemes tot et de valider les solutions incrementalement, plutot que de decouvrir des problemes majeurs en fin de cycle.

### Principle 5 -- Separate Observation from Interpretation

Pendant les sessions de recherche, distinguer rigoureusement les observations factuelles ("L'utilisateur a clique 3 fois sur le bouton sans resultat") des interpretations ("L'utilisateur est frustre par l'interface"). Les observations sont des faits ; les interpretations sont des hypotheses qui doivent etre etayees par des patterns recurrents. Documenter les observations brutes d'abord, puis synthetiser les interpretations dans un second temps.

### Principle 6 -- Democratize Without Diluting

Rendre les insights accessibles a toute l'organisation (research repository, highlights videos, insight briefs) sans diluer la rigueur methodologique. Encourager les non-chercheurs a observer des sessions utilisateurs, mais former les equipes aux biais courants (biais de confirmation, biais de desirabilite sociale, leading questions). La democratisation de la recherche ne signifie pas que tout le monde fait de la research : elle signifie que tout le monde a acces aux insights et comprend comment ils ont ete produits.

## Key Frameworks & Methods

### Research Method Selection Matrix

| Methode | Type | Quand l'utiliser | Participants | Duree | Fidelite des insights |
|---|---|---|---|---|---|
| **Interview exploratoire** | Qualitatif, generatif | Discovery, comprendre le contexte | 5-8 | 45-60 min | Elevee (profondeur) |
| **Interview de validation** | Qualitatif, evaluatif | Tester des hypotheses specifiques | 5-8 | 30-45 min | Moyenne-elevee |
| **Test d'utilisabilite modere** | Qualitatif, evaluatif | Evaluer un prototype ou un produit | 5-8 | 30-60 min | Elevee (comportement) |
| **Test non-modere** | Qualitatif, evaluatif | Tests a grande echelle, benchmarking | 20-50 | 10-20 min | Moyenne (pas de probing) |
| **Diary Study** | Qualitatif, generatif | Comprendre l'usage dans la duree | 10-15 | 1-4 semaines | Elevee (contexte reel) |
| **Contextual Inquiry** | Qualitatif, generatif | Observer l'usage en contexte reel | 5-8 | 60-120 min | Tres elevee |
| **Survey** | Quantitatif, evaluatif | Mesurer attitudes, satisfaction, segmenter | 100-500+ | 5-10 min | Moyenne (declaratif) |
| **Card Sorting** | Quanti-quali, generatif | Structurer l'architecture d'information | 15-30 | 15-30 min | Elevee pour l'IA |
| **Tree Testing** | Quantitatif, evaluatif | Valider une architecture d'information | 30-50 | 10-15 min | Elevee pour la navigation |
| **A/B Testing** | Quantitatif, evaluatif | Comparer 2 variantes en production | 1000+* | Continue | Tres elevee (comportement reel) |

*Taille d'echantillon dependante de l'effet detecte et de la significativite souhaitee.

### Interview Script Structure

```
1. Introduction (5 min)
   +-- Presentation du contexte (sans reveler les hypotheses)
   +-- Consentement et permission d'enregistrer
   +-- "Il n'y a pas de bonne ou mauvaise reponse"
   +-- "Je n'ai pas concu ce produit, votre honnêteté m'aide"

2. Echauffement (5 min)
   +-- Questions sur le contexte personnel/professionnel
   +-- Etablir le rapport et mettre a l'aise

3. Corps de l'interview (30-40 min)
   +-- Questions ouvertes, du general au specifique
   +-- "Racontez-moi la derniere fois que..."
   +-- "Comment faites-vous aujourd'hui pour... ?"
   +-- "Qu'est-ce qui est le plus frustrant dans... ?"
   +-- Follow-up : "Pourquoi ?", "Pouvez-vous me montrer ?", "Que s'est-il passe ensuite ?"
   +-- Eviter : questions fermees, questions orientees, doubles questions

4. Wrap-up (5 min)
   +-- "Y a-t-il quelque chose que je n'ai pas demande et que vous aimeriez partager ?"
   +-- Remerciements et explication des prochaines etapes
```

### Assumption Mapping

| Quadrant | Risque | Evidence | Action |
|---|---|---|---|
| **Haut risque + Peu d'evidence** | Elevé | Faible | Tester en priorite (experiments, interviews) |
| **Haut risque + Beaucoup d'evidence** | Elevé | Forte | Monitorer (les conditions peuvent changer) |
| **Faible risque + Peu d'evidence** | Faible | Faible | Backlog (tester si le temps le permet) |
| **Faible risque + Beaucoup d'evidence** | Faible | Forte | Ignorer (risque maitre) |

Types d'hypotheses a cartographier :
- **Desirabilite** : les utilisateurs veulent-ils cette solution ?
- **Viabilite** : le business model fonctionne-t-il ?
- **Faisabilite** : pouvons-nous le construire avec les ressources disponibles ?
- **Utilisabilite** : les utilisateurs peuvent-ils l'utiliser sans difficulte ?

### Jobs To Be Done (JTBD) Framework

```
Structure d'un Job Statement :
"Quand [situation/contexte], je veux [motivation/objectif],
 pour que [resultat attendu/benefice]"

Exemple :
"Quand je dois preparer une presentation pour le COMEX en 2h,
 je veux transformer mes donnees brutes en un recit visuel convaincant,
 pour que le board approuve mon budget sans poser de questions bloquantes."

Niveaux d'analyse :
1. Core Functional Job : la tache a accomplir
2. Related Jobs : les taches adjacentes dans le meme workflow
3. Emotional Jobs : comment l'utilisateur veut se sentir
4. Social Jobs : comment l'utilisateur veut etre percu

Forces du Switch (pourquoi les utilisateurs changent de solution) :
+-- Push : frustration avec la solution actuelle
+-- Pull : attraction de la nouvelle solution
+-- Anxiety : peur liee au changement
+-- Habit : inertie et confort de la solution actuelle
```

### Research Quality Checklist

| Critere | Question de verification | Seuil minimum |
|---|---|---|
| **Objectif clair** | L'objectif de recherche est-il formule en question ? | Oui |
| **Methode appropriee** | La methode repond-elle au type de question ? | Oui |
| **Echantillon suffisant** | Le nombre de participants est-il adequat ? | 5+ (quali), 100+ (quanti) |
| **Protocole documente** | Le script/protocole est-il ecrit avant la premiere session ? | Oui |
| **Biais mitiges** | Les questions sont-elles non-orientees ? | Revue par un pair |
| **Consentement** | Les participants ont-ils donne leur accord ecrit ? | Oui (obligatoire) |
| **Triangulation** | Les insights sont-ils croises avec d'autres sources ? | 2+ sources |
| **Actionnable** | Chaque insight est-il lie a une recommandation ? | Oui |

## Decision Guide

### Choix de la methode de recherche

```
1. Quel type de question vous posez-vous ?
   +-- "Quoi / Combien ?" (mesurer, quantifier) --> Methodes quantitatives (survey, analytics, A/B test)
   +-- "Pourquoi / Comment ?" (comprendre, explorer) --> Methodes qualitatives (interviews, observation)
   +-- "Est-ce utilisable ?" (evaluer) --> Tests d'utilisabilite (moderes ou non-moderes)

2. Quelle phase produit ?
   +-- Pre-discovery (comprendre le marche) --> Interviews exploratoires, contextual inquiry
   +-- Discovery (identifier les opportunites) --> Interviews JTBD, diary studies, observations
   +-- Design (tester les solutions) --> Tests d'utilisabilite, prototype testing, A/B tests
   +-- Post-launch (mesurer l'impact) --> Surveys (NPS/CSAT), analytics, interviews de suivi

3. Quelles contraintes ?
   +-- Budget < 500 EUR --> Interviews informelles, guerrilla testing, survey gratuit
   +-- Temps < 1 semaine --> Tests non-moderes (Maze, UserTesting), survey rapide
   +-- Pas d'acces direct aux utilisateurs --> Analytics, support ticket analysis, review mining
```

### Dimensionnement de l'echantillon

```
Methodes qualitatives :
+-- Interviews exploratoires : 5-8 participants (saturation thematique)
+-- Tests d'utilisabilite : 5 participants (detectent 85% des problemes)
+-- Diary studies : 10-15 participants
+-- Card sorting : 15-30 participants (ouvert), 30-50 (ferme)

Methodes quantitatives :
+-- Surveys : 100-500 repondants minimum (marge d'erreur < 5%)
+-- A/B tests : calculer via sample size calculator
   +-- Inputs : baseline conversion, MDE (minimum detectable effect), puissance (80%), significativite (95%)
+-- NPS : 200+ repondants pour un score fiable
```

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Research Repository** : centraliser tous les insights dans un systeme structuré et cherchable (Dovetail, Notion, EnjoyHQ). Chaque insight est tague par theme, segment, date et methode. Le repository evite de refaire des etudes deja menees et permet de detecter des patterns cross-etudes.
- **Atomic Research** : decomposer les resultats en atomes : Experiment (la session) → Observation (fait brut) → Insight (pattern recurrent) → Recommendation (action). Cette granularite permet de reutiliser les insights dans differents contextes.
- **Research Sprints** : concentrer la recherche en sprints courts (1-2 semaines) avec un objectif precis, plutot que des etudes longues. Chaque sprint produit un deliverable actionnable (insight brief, personas mis a jour, journey map revisee).
- **Participant Panel** : maintenir un panel pre-recrute de participants volontaires, segmentes par profil. Permet de lancer une etude en 48h au lieu de 2 semaines. Renouveler le panel regulierement pour eviter le biais de familiarite.

### Anti-patterns critiques

- **Confirmation Bias Research** : concevoir les etudes pour confirmer ce qu'on veut entendre. Diagnostiquer via : "Les questions de mon script pourraient-elles orienter les reponses dans une direction ?" Faire relire le protocole par un pair.
- **Insight Graveyard** : conduire des etudes dont les resultats ne sont jamais actionnes. Exiger qu'un owner et une action soient definis pour chaque insight majeur avant de cloturer l'etude.
- **Leading Questions** : poser des questions qui suggerent la reponse ("Ne trouvez-vous pas que cette interface est confuse ?"). Utiliser des formulations neutres ("Decrivez-moi votre experience avec cette interface").
- **Survey Abuse** : envoyer des surveys pour des questions qui necessitent des interviews (le "pourquoi" profond). Les surveys mesurent le "quoi" et le "combien", pas le "pourquoi".
- **N=1 Decisions** : generaliser a partir d'un seul entretien ou d'un seul feedback. Attendre de voir un pattern recurrer sur 3-5 participants avant de conclure.

## Implementation Workflow

### Phase 1 -- Fondations Research Ops

1. Definir la charte de recherche : objectifs, methodes autorisees, ethique, consentement, RGPD.
2. Choisir et deployer les outils de research (enregistrement, analyse, repository).
3. Constituer le panel de participants initial (recruter 50-100 volontaires segmentes).
4. Former les product trios aux techniques d'interview et aux biais cognitifs (atelier de 2h).
5. Creer les templates standard : plan de recherche, script d'interview, grille d'observation, rapport d'insight.

### Phase 2 -- Premiere etude pilote

6. Choisir un sujet de recherche prioritaire aligne sur les objectifs produit actuels.
7. Rediger le plan de recherche : objectif, methode, participants, protocole, timeline.
8. Conduire 5-8 entretiens ou sessions avec le protocole defini.
9. Synthetiser les resultats via affinity mapping (regrouper les observations en themes).
10. Produire un insight brief actionnable et le presenter a l'equipe produit.

### Phase 3 -- Cadence continue

11. Etablir la cadence de recherche : 2-3 entretiens par semaine par product trio.
12. Mettre en place le research repository et commencer a indexer les insights.
13. Integrer la recherche dans le dual-track agile (discovery track).
14. Former des "research champions" dans chaque equipe pour demultiplier la capacite.
15. Conduire des surveys trimestriels (NPS, CSAT) pour completer les donnees qualitatives.

### Phase 4 -- Maturite et impact

16. Mesurer l'impact de la recherche : combien de decisions produit s'appuient sur des insights ?
17. Construire des personas et journey maps data-driven, mis a jour trimestriellement.
18. Mettre en place des etudes longitudinales (diary studies, cohortes) pour les questions complexes.
19. Automatiser ce qui peut l'etre : recrutement, transcription, analyse thematique assistee par IA.
20. Partager les insights a l'echelle de l'organisation (newsletter insights, video highlights, all-hands).

## Modele de maturite

### Niveau 1 -- Ad-hoc
- La recherche utilisateur est ponctuelle et non structuree
- Les decisions produit reposent sur l'intuition ou les remontees du support client
- Pas de methode, pas de protocole, pas de documentation des insights
- **Indicateurs** : < 1 entretien utilisateur par mois, pas de research repository

### Niveau 2 -- Reactif
- La recherche est declenchee avant les gros projets (refonte, nouveau produit)
- Des interviews et des tests d'utilisabilite sont conduits mais de maniere irreguliere
- Les insights sont documentes mais peu partages au-dela de l'equipe produit
- **Indicateurs** : 2-4 etudes par an, insights dans des documents isoles

### Niveau 3 -- Continu
- La recherche fait partie du rythme quotidien de l'equipe produit (2+ interviews/semaine)
- Un research repository est en place et utilise par les PMs et designers
- Les methodes sont variees (quali + quanti) et adaptees aux questions
- **Indicateurs** : > 50 entretiens/an, research repository actif, 50%+ des decisions appuyees par des insights

### Niveau 4 -- Strategique
- La recherche influence les decisions strategiques, pas seulement tactiques
- Les personas et journey maps sont data-driven et mis a jour regulierement
- La recherche est democratisee : les non-chercheurs observent des sessions et consultent le repository
- **Indicateurs** : > 100 entretiens/an, insights accessibles a toute l'organisation, NPS research interne > 50

### Niveau 5 -- Predictif
- L'IA assiste l'analyse (transcription auto, clustering thematique, detection de patterns)
- La recherche est integree dans les processus de decision a tous les niveaux de l'organisation
- Des etudes longitudinales permettent de predire les evolutions des besoins utilisateurs
- **Indicateurs** : temps d'analyse reduit de 50%+, > 80% des initiatives produit appuyees par la research, research ROI mesure

## Rythme operationnel

| Cadence | Activite | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Hebdomadaire** | 2-3 entretiens utilisateurs par product trio | Product Trio | Notes d'interview + observations |
| **Hebdomadaire** | Debrief research — partage des observations de la semaine | UX Researcher + PMs | Insights de la semaine |
| **Bi-mensuel** | Synthese et mise a jour du research repository | UX Researcher | Insights indexes et tagges |
| **Mensuel** | Research review — quels insights, quelles actions | Head of Research + Head of Product | Rapport d'impact research |
| **Trimestriel** | Survey NPS/CSAT et analyse des tendances | UX Researcher | Rapport quantitatif + trends |
| **Trimestriel** | Mise a jour des personas et journey maps | UX Researcher + Product Trio | Personas et journey maps actualises |
| **Annuel** | Audit research ops — outils, processus, competences | Head of Research | Plan d'amelioration research ops |

## State of the Art (2025-2026)

La recherche utilisateur connait une transformation profonde portee par l'IA et la democratisation des outils :

- **AI-Powered Analysis** : Les outils comme Dovetail, Marvin et Notably utilisent l'IA pour transcrire, coder et clusteriser automatiquement les insights. Le temps d'analyse est reduit de 60-80%, permettant aux chercheurs de se concentrer sur l'interpretation et la strategie.
- **Synthetic Users & AI Personas** : L'emergence d'utilisateurs synthetiques (bases sur des donnees reelles) pour des pre-tests rapides. Ne remplace pas la vraie research mais accelere les iterations de prototypage.
- **Democratisation & Research Ops** : Le role de Research Ops se generalise pour industrialiser la recherche (recrutement, outils, gouvernance). Les plateformes self-serve (Maze, UserTesting) permettent a tout PM de lancer un test non-modere en 24h.
- **Mixed Methods par defaut** : La combinaison systematique de methodes qualitatives et quantitatives devient la norme, pas l'exception. Les outils facilitent le croisement (ex : segments analytics + interviews ciblees).
- **Ethical Research & Privacy** : Avec le RGPD et les regulations sur l'IA, la gestion du consentement, de l'anonymisation et de la retention des donnees de recherche devient un enjeu critique.

## Template actionnable

### Plan de recherche

| Element | Description | Votre reponse |
|---|---|---|
| **Objectif** | Quelle question de recherche ? | ___ |
| **Contexte** | Pourquoi cette recherche maintenant ? | ___ |
| **Methode** | Quelle methode et pourquoi ? | ___ |
| **Participants** | Combien, quels criteres de recrutement ? | ___ |
| **Protocole** | Script ou grille d'observation (lien) | ___ |
| **Timeline** | Dates de recrutement, sessions, analyse | ___ |
| **Livrables** | Quels outputs attendus ? | ___ |
| **Owner** | Qui conduit et qui observe ? | ___ |
| **Decision** | Quelle decision sera eclairee par cette recherche ? | ___ |

## Prompts types

- "Aide-moi a planifier une etude de recherche utilisateur pour comprendre pourquoi nos utilisateurs churnernt"
- "Redige un script d'interview pour de la discovery sur le workflow de nos utilisateurs"
- "Comment recruter des participants pour des tests d'utilisabilite ?"
- "Synthetise ces notes d'interview en insights actionnables"
- "Construis des personas data-driven a partir de ces donnees"
- "Quelle methode de recherche utiliser pour valider cette hypothese produit ?"
- "Aide-moi a concevoir un survey NPS/CSAT efficace"
- "Comment mettre en place un research repository ?"

## Limites et Red Flags

Ce skill n'est PAS adapte pour :
- ❌ **Strategie produit et roadmap** (vision, priorisation, OKR produit) → Utiliser plutot : `entreprise:product-strategy`
- ❌ **Design d'interface et prototypage** (wireframes, mockups, design system) → Utiliser plutot : `code-development:ui-ux`
- ❌ **Analytics et tracking produit** (event tracking, funnels, A/B testing quantitatif a grande echelle) → Utiliser plutot : `code-development:product-analytics`
- ❌ **Etude de marche et analyse concurrentielle** (taille de marche, benchmarks sectoriels) → Utiliser plutot : `entreprise:marketing`
- ❌ **Compliance RGPD et protection des donnees** (aspects juridiques de la collecte de donnees) → Utiliser plutot : `entreprise:juridique`

Signaux d'alerte en cours d'utilisation :
- ⚠️ Toutes les etudes confirment les hypotheses de l'equipe — biais de confirmation probable, revoir le protocole
- ⚠️ Les insights ne sont pas actionnes depuis plus d'un mois — risque d'insight graveyard, revoir le processus d'activation
- ⚠️ Les interviews contiennent des questions orientees ("Aimez-vous cette feature ?") — biais methodologique
- ⚠️ Les decisions sont prises sur la base d'un seul entretien — risque de N=1 generalization

## Skills connexes

| Skill | Lien |
|---|---|
| Product Strategy | `entreprise:product-strategy` — Vision, roadmap et priorisation produit |
| Marketing | `entreprise:marketing` — Etudes de marche, buyer personas marketing |
| UI/UX | `code-development:ui-ux` — Design d'interface base sur la research |
| Product Analytics | `code-development:product-analytics` — Donnees quantitatives produit |
| Support Client | `entreprise:support-client` — Voice of Customer et feedbacks terrain |
| AI Ethics | `ai-governance:ai-ethics` — Ethique de la recherche avec participants humains |

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[Research Methods](./references/research-methods.md)** : guide detaille de chaque methode (interviews, usability tests, surveys, diary studies, card sorting), protocoles, scripts types, dimensionnement des echantillons, state of the art 2025-2026.
- **[Analysis & Synthesis](./references/analysis-synthesis.md)** : techniques d'analyse (affinity mapping, thematic analysis, atomic research), creation de personas, journey mapping, communication des insights, state of the art 2025-2026.
- **[UX Metrics & Testing](./references/ux-metrics-testing.md)** : metriques UX (SUS, NPS, CSAT, CES, task success rate), benchmarks, tests d'utilisabilite avances, evaluation heuristique, accessibility testing, state of the art 2025-2026.
- **[Etudes de cas](./references/case-studies.md)** — Cas pratiques detailles illustrant les concepts cles du skill.
