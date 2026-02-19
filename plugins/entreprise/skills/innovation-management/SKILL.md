---
name: innovation-management
version: 1.0.0
description: >
  Use this skill when the user asks about "innovation management", "design thinking", "intrapreneuriat", "open innovation", "innovation lab", "corporate innovation", "stage-gate process", "lean startup methodology", "jobs-to-be-done", "hackathon organisation", "startup collaboration", "innovation culture", "ideation workshop", "prototype validation", discusses accelerators, venture building, or needs guidance on innovation governance, idea management, and building internal innovation capabilities.
---

# Innovation Management — Design Thinking, Intrapreneuriat & Open Innovation

## Overview

L'innovation managee est la discipline qui transforme la creativite en valeur economique mesurable. Elle couvre trois dimensions complementaires : les methodes de decouverte (design thinking, Jobs-to-be-Done), les modeles organisationnels (intrapreneuriat, labs, spin-off) et les ecosystemes exterieurs (open innovation, partenariats startups, corporate venture).

La distinction critique : **l'innovation accidentelle vs l'innovation systematique**. La premiere depend des individus exceptionnels ; la seconde construit des processus, des competences et une culture qui produisent de l'innovation de maniere previsible.

**Trois types d'innovation a piloter separement** :
- **Innovation incrementale** (horizon 1) : amelioration des produits et process existants — 70% des ressources
- **Innovation adjacente** (horizon 2) : extension vers de nouveaux marches ou segments — 20% des ressources
- **Innovation de rupture** (horizon 3) : exploration de business models radicalement nouveaux — 10% des ressources

## Core Principles

**1. Empathie avant solution.** La majorite des innovations echouent non par manque de technologie mais par mauvaise comprehension du probleme. Passer 50% du temps sur la phase de decouverte : interviews, observations terrain, shadowing. Une heure d'interview utilisateur economise dix heures de dev inutile.

**2. Hypotheses explicites et testables.** Toute initiative d'innovation repose sur des hypotheses (sur le probleme, l'utilisateur, la solution, le modele economique). Les rendre explicites, les prioriser par niveau de risque, les tester dans le bon ordre. Ne jamais coder avant d'avoir valide la desirabilite.

**3. Prototype avant investissement.** Un prototype papier en 2h revele 80% des problemes qu'un MVP en 3 mois aurait aussi detectes. L'objectif du prototype n'est pas de construire mais d'apprendre. Resolution croissante : sketch → wireframe → prototype cliquable → MVP → pilote → lancement.

**4. Separation de la phase de generation et de la phase d'evaluation.** Les idees sont tuees trop tot par le jugement premature. Brainstorming (sans critique), puis evaluation (sans biais de premiere idee). Les deux phases ne peuvent pas coexister dans la meme reunion.

**5. Metriques d'apprentissage, pas de performance.** En phase d'exploration, les KPIs sont : nombre d'hypotheses testees, vitesse d'iteration, qualite des insights. Les metriques de performance (CA, marge) arrivent en phase d'exploitation. Confondre les deux tue l'innovation.

**6. Portefeuille, pas projet unique.** Une innovation sur dix aboutit. Gerer un portefeuille d'initiatives avec des regles explicites de financement par etape (stage-gating), de pivot et d'arret. L'echec d'une initiative est une donnee, pas un probleme — l'absence d'apprentissage est le vrai probleme.

## Key Frameworks

### Double Diamond (Design Council)
Quatre phases : **Discover** (comprendre le probleme), **Define** (synthetiser les insights en problematique claire), **Develop** (generer et prototyper des solutions), **Deliver** (tester et lancer). Deux moments de divergence (toutes les idees sont bienvenues) et deux moments de convergence (selectionner la meilleure piste). Applicable a tout projet de 1 semaine a 6 mois.

### Design Thinking (IDEO/Stanford d.school)
Cinq etapes : **Empathize** → **Define** → **Ideate** → **Prototype** → **Test**. Non-lineaire : on peut revenir en arriere a tout moment. Point fort : l'empathie profonde avec l'utilisateur final. Adapte aux problemes complexes dont la nature n'est pas encore claire.

### Jobs-to-be-Done (Clayton Christensen)
Les utilisateurs "embauchent" des produits pour accomplir des "jobs" fonctionnels, emotionnels et sociaux. Exemple : les gens n'achetent pas une perceuse, ils achetent un trou dans le mur. Identifier le job dominant permet de decouvrir des concurrents non-evidents et des opportunites d'innovation. Outil : l'interview JTBD avec la chronologie d'achat.

### Lean Startup (Eric Ries)
Cycle Build-Measure-Learn : construire le MVP minimal, mesurer une metrique actionnable, apprendre et decider de perseverer ou pivoter. Anti-pattern a eviter : le "Fake Lean Startup" — construire trop avant de mesurer. MVP = l'experience la plus simple qui permet de valider (ou invalider) l'hypothese la plus risquee.

### Stage-Gate (Robert Cooper)
Processus en entonnoir avec des phases (ideation → concept → business case → developpement → lancement) separees par des "gates" (comites de decision Go/No-Go/Hold). Adapte aux innovations complexes avec investissements lourds (industrie, pharma, hardware). Critiques : peut ralentir l'iteration ; a combiner avec des sprints agiles dans les phases de dev.

### Open Innovation (Henry Chesbrough)
Principe : les meilleures idees ne sont pas toutes dans l'entreprise. Deux flux : **inbound** (startups, labo de recherche, crowdsourcing, API ouverte) et **outbound** (licensing de brevets, spin-off, JV). Outils : partenariats startups, corporate accelerators, API economy, challenges d'innovation avec partenaires.

## Decision Guide — Quelle Methode pour Quel Contexte

| Contexte | Methode recommandee | Duree typique |
|---|---|---|
| Probleme mal defini, utilisateur connu | Design Thinking | 1-4 semaines |
| Marche a creer, besoin latent | Jobs-to-be-Done | 2-6 semaines (recherche) |
| Prototype digital a valider vite | Lean Startup / Sprint | 1-5 jours (Design Sprint) |
| Innovation complexe, investissement > 500k | Stage-Gate | 3-18 mois |
| Acces a des technologies ou marches exterieurs | Open Innovation | 3-12 mois |
| Liberer les initiatives internes | Intrapreneuriat | Programme 6-12 mois |

**Regles de selection** :
- Probleme connu + solution inconnue → Design Thinking
- Probleme inconnu + solution inconnue → JTBD + ethnographie
- Hypothese business a tester → Lean Startup
- Projet industriel lourd → Stage-Gate
- Manque de ressources internes → Open Innovation

## Architecture d'un Programme d'Innovation

### Structure organisationnelle
```
CEO / COMEX
    |
Chief Innovation Officer (CIO)
    |
    ├── Innovation Lab (exploration H3)
    │     ├── Design Researchers
    │     ├── Prototypeurs / Makers
    │     └── Business Designers
    │
    ├── Accelerateur interne (H2)
    │     ├── Equipes intrapreneurs
    │     └── Mentors business
    │
    └── Innovation par BU (H1)
          └── Innovation Champions dans chaque BU
```

### Gouvernance du portefeuille
- **Comite d'ideation** (mensuel) : selection des idees a passer en qualification (horizon 3)
- **Comite de scaling** (trimestriel) : decisions de pivot, perseverer ou tuer (horizon 2)
- **Business review** (trimestriel) : suivi KPIs des innovations en cours de commercialisation (horizon 1)

## Operational Workflow — Design Sprint Google (5 Jours)

**Lundi — Map** : Definir le defi, cartographier le parcours utilisateur, interviewer les experts. Choisir la cible prioritaire.

**Mardi — Sketch** : Revue des solutions existantes (inspirations), puis sketching individuel (4 etapes : notes → idees folles → crazy-8 → solution sketch).

**Mercredi — Decide** : Vote silencieux (dot voting), critique structuree, decision par le "Decider". Storyboard de la solution retenue.

**Jeudi — Prototype** : Construire un prototype realiste (Figma, Keynote, ou physique) en 1 jour. Objectif : faire illusion, pas construire.

**Vendredi — Test** : Interviews avec 5 utilisateurs cibles. 5 interviews revelent 85% des problemes majeurs. Synthese des apprentissages et decision.

## Maturity Model — Innovation Management

| Niveau | Caracteristique | Indicateurs |
|---|---|---|
| **1 — Ad Hoc** | Innovation dependant des individus | Pas de processus, pas de budget dedie |
| **2 — Experimenter** | Quelques initiatives isolees, pas de cadre | Budget projets ponctuels, quelques champions |
| **3 — Structure** | Processus d'ideation et de selection definis | Lab, budget H3, stage-gate operationnel |
| **4 — Systematique** | Portefeuille gere, metriques d'apprentissage | Pipeline mesure, partenariats ecosysteme |
| **5 — Ambidextre** | Exploitation et exploration en equilibre | 70/20/10, culture d'experimentation repandue |

## Obstacles Frequents et Solutions

**"L'idee est tuee en comite"** : Separer la session de generation (100% de bienveillance) de la session d'evaluation. Utiliser des criteres explicites pre-etablis. Eviter les comites > 7 personnes en phase d'ideation.

**"Pas de temps pour innover"** : L'innovation requiert du temps protege. Minimum : 10% du temps des equipes + budget dedie. Sans cela, l'urgence opérationnelle ecrase toujours l'exploration.

**"On a plein d'idees mais rien ne sort"** : Probleme d'execution, pas de generation. Implementer le stage-gate avec des ressources dediees a chaque phase. La plupart des entreprises ont trop d'idees et pas assez de capacite d'execution focalisee.

**"L'innovation lab est deconnecte du business"** : Le lab doit avoir des sponsors dans les BU. Chaque initiative doit avoir un "sponsor business" qui s'engage a deployer la solution si elle est validee. Eviter les labs trophy.

## Templates Operationnels

### Innovation Canvas (1 page)
```
PROBLEME                    SOLUTION
Quel probleme on resout ?   Quelle est notre proposition ?
Pour qui ?                  Differenciateur cle ?

HYPOTHESES CRITIQUES        EXPERIENCE
A valider en priorite ?     Comment on va tester ?
Quelle est la + risquee ?   En combien de temps ?

SUCCES = ...                RESSOURCES NECESSAIRES
Metrique de validation      Budget / Equipe / Acces
```

### Pitch d'Idee (5 minutes, structure)
1. **Probleme** (1 min) : Pour qui, quelle frustration, quelle frequence
2. **Solution** (1 min) : Notre approche, en quoi elle est differente
3. **Validation** (1 min) : Ce qu'on a deja teste, ce qu'on a appris
4. **Marche** (30s) : Taille du marche addressable, potentiel
5. **Demande** (30s) : Ressources demandees, prochaine etape

## State of the Art (2024-2026)

- **AI-augmented ideation** : LLMs pour generer des variations d'idees, simuler des personas utilisateurs, accelerer la synthese d'interviews (ex : notebooks Claude avec transcriptions d'entretiens)
- **Remote Design Sprints** : Outillage (Miro, FigJam, Butter) mature, sprints asynchrones possibles sur 2 semaines
- **Innovation accounting** (Ries) : metriques d'apprentissage standardisees — Innovation Options (valeur d'information d'un test), DACI pour la gouvernance
- **Venture clienting** vs corporate venturing : acheter des solutions startups (client direct) vs investir — le venture clienting monte car plus rapide et moins risque financierement

## Limites et Pieges

- Le design thinking n'est pas une baguette magique : il necessite une vraie recherche utilisateur, pas des assumptions en salle de reunion
- L'innovation de rupture (H3) ne peut pas etre geree avec les memes outils que l'innovation incrementale (H1)
- Les programmes d'intrapreneuriat echouent souvent par manque de protection organisationnelle : l'intrapreneur doit etre libere de ses objectifs habituels pendant la duree du programme
- Open Innovation : la propriete intellectuelle doit etre clarifiee avant toute collaboration externe (NDA, accords de co-developpement)
- Ne pas confondre "innovation" et "R&D" : la R&D produit des technologies, l'innovation produit de la valeur client
