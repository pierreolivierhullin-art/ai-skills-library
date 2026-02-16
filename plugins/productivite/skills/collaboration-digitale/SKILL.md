---
name: collaboration-digitale
description: This skill should be used when the user asks about "Teams collaboration", "Slack workspace", "digital collaboration", "remote work tools", "hybrid work", "Miro whiteboard", "FigJam", "Loom video", "asynchronous communication", "meeting management", "video conferencing", "screen recording", "digital facilitation", "team communication", "collaboration outils", "travail hybride", "communication asynchrone", "visioconférence", "facilitation digitale", "tableau blanc collaboratif", "travail à distance", "réunions efficaces", "outils de collaboration", "Microsoft Teams avancé", "Slack avancé", discusses digital collaboration tools, remote/hybrid work, or needs guidance on team communication, facilitation, and meeting management.
version: 1.0.0
last_updated: 2026-02
---

# Collaboration Digitale / Digital Collaboration

## Overview

**FR** — Cette skill couvre l'ensemble des pratiques de collaboration digitale moderne : plateformes de messagerie (Microsoft Teams, Slack), outils de collaboration visuelle (Miro, FigJam, Microsoft Whiteboard), communication asynchrone (Loom, video enregistree, documentation), visioconference (Zoom, Teams, Google Meet), facilitation d'ateliers a distance et gestion de reunions efficaces. La maitrise de la collaboration digitale est devenue une competence fondamentale dans le monde post-2020 : le travail hybride est desormais la norme, les equipes sont distribuees geographiquement, et la capacite a collaborer efficacement a travers les outils numeriques determine directement la performance collective. Les recommandations couvrent les configurations avancees des plateformes, les patterns d'architecture de channels, les protocoles de communication asynchrone, les techniques de facilitation a distance, et les innovations 2025-2026 : IA integree dans Teams et Slack, resume automatique de reunions, collaboration spatiale, et assistants IA conversationnels embarques.

**EN** — This skill covers the full spectrum of modern digital collaboration practices: messaging platforms (Microsoft Teams, Slack), visual collaboration tools (Miro, FigJam, Microsoft Whiteboard), asynchronous communication (Loom, recorded video, documentation), video conferencing (Zoom, Teams, Google Meet), remote workshop facilitation, and effective meeting management. Mastering digital collaboration has become a foundational competency in the post-2020 world: hybrid work is now the standard, teams are geographically distributed, and the ability to collaborate effectively through digital tools directly determines collective performance. Recommendations cover advanced platform configurations, channel architecture patterns, asynchronous communication protocols, remote facilitation techniques, and 2025-2026 innovations: AI embedded in Teams and Slack, automatic meeting summaries, spatial collaboration, and embedded conversational AI assistants.

---

## When This Skill Applies

Activer ce skill lorsque l'utilisateur :

- Met en place ou restructure un workspace Teams ou Slack (architecture de channels, gouvernance, conventions de nommage, permissions)
- Facilite des ateliers ou workshops a distance avec des outils visuels (Miro, FigJam, Whiteboard)
- Definit ou ameliore les pratiques de communication asynchrone (Loom, video, documentation, RFC)
- Optimise la gestion de reunions (preparation, facilitation, suivi, reduction du nombre de reunions)
- Organise le travail hybride (regles de presence, outils, rituels, equite entre sites et remote)
- Structure l'onboarding a distance de nouveaux collaborateurs
- Anime des retrospectives, ceremonies agiles ou sessions de brainstorming collaboratif en mode distribue
- Gere les fuseaux horaires et la coordination d'equipes internationales
- Evalue, selectionne ou rationalise les outils de collaboration de l'organisation

---

## Core Principles

### 1. Async by Default, Sync When Needed
Privilegier la communication asynchrone comme mode par defaut. Reserver le synchrone (reunions, appels) aux situations qui l'exigent reellement : decisions complexes impliquant des desaccords, sujets sensibles necessitant de la nuance, brainstorming creatif en groupe, et cohesion d'equipe. Chaque message, chaque mise a jour, chaque partage d'avancement doit d'abord etre envisage en async. La communication synchrone est couteuse : elle interrompt le travail profond, impose une simultaneite souvent artificielle, et exclut les collaborateurs sur d'autres fuseaux horaires. L'async n'est pas de la paresse — c'est du respect pour le temps et l'attention de chacun.

### 2. Right Tool, Right Message
Chaque type de message a un canal optimal. Un message Slack n'est pas un email, un Loom n'est pas une reunion, un document n'est pas un message instantane. Definir une matrice claire : messages operationnels courts dans le chat, decisions structurees dans un document partage, explications complexes en video Loom, alignement strategique en reunion synchrone. Le choix du mauvais outil cree du bruit, de la frustration, et des informations perdues. Former les equipes a cette discipline de choix est un investissement a haut rendement.

### 3. Structured Channels, Not Chaos
L'architecture des channels dans Teams ou Slack est un acte de design organisationnel. Des channels mal structures creent du bruit, de la duplication, et de l'information introuvable. Definir des conventions de nommage strictes, des categories claires, des regles de creation et d'archivage, et des responsables par channel. Un workspace bien structure est un workspace ou chaque collaborateur sait exactement ou poster et ou chercher.

### 4. Documentation Over Memory
Ce qui n'est pas documente n'existe pas. Chaque decision prise en reunion doit etre consignee. Chaque processus explique en chat doit finir dans une documentation durable. Chaque contexte partage en Loom doit etre indexe et retrouvable. La documentation n'est pas une corvee administrative — c'est le systeme nerveux de la collaboration asynchrone. Sans documentation, les equipes distribuees sont condamnees a repeter les memes conversations et a perdre le contexte a chaque nouveau collaborateur.

### 5. Inclusive Collaboration
Les outils et les pratiques de collaboration doivent garantir l'equite entre tous les participants, quel que soit leur lieu de travail (bureau, domicile, autre fuseau horaire), leur style de communication (introvertis, non-natifs de la langue), ou leur accessibilite (handicap visuel, auditif). Les reunions hybrides doivent traiter les participants distants comme des participants de premiere classe. Les ateliers doivent prevoir des modes de contribution ecrits, pas uniquement oraux. Les decisions ne doivent jamais etre prises dans des couloirs auxquels seuls les presents physiques ont acces.

### 6. Meeting Discipline
Chaque reunion doit avoir un objectif clair, un agenda distribue a l'avance, un animateur designe, et un compte-rendu avec actions et responsables. Si l'objectif peut etre atteint par un document, un Loom, ou un message asynchrone, annuler la reunion. Le temps en reunion est le temps le plus cher de l'organisation : il mobilise simultanement plusieurs personnes et interrompt le travail profond de chacune. Proteger le temps de l'equipe, c'est proteger sa capacite de production.

---

## Key Frameworks & Methods

### Communication Mode Selection Matrix

| Critere | Async (message/doc/Loom) | Sync (reunion/appel) |
|---|---|---|
| **Urgence faible** | Prefere | Non necessaire |
| **Urgence haute** | Message + notification | Appel immediat si decision requise |
| **Complexite faible** | Message/chat | Non necessaire |
| **Complexite haute** | Document + Loom pour contexte | Reunion si debat necessaire |
| **Desaccord probable** | Document pour preparer les positions | Reunion pour resoudre |
| **Information unidirectionnelle** | Loom / document / post | Non necessaire |
| **Brainstorming** | Pre-work async (idees ecrites) | Session collaborative (Miro/FigJam) |
| **Decision formelle** | RFC ecrit, vote async possible | Reunion si consensus requis |
| **Cohesion d'equipe** | Non adapte | Prefere (video, informel) |

### Meeting Decision Framework

```
Cette reunion est-elle necessaire ?
├── L'objectif est-il clairement defini ?
│   ├── NON → Ne pas planifier tant que l'objectif est flou
│   └── OUI → Peut-on atteindre cet objectif en async ?
│       ├── OUI (information, mise a jour, partage) → Loom / document / post
│       └── NON → Le sujet necessite-t-il un debat interactif ?
│           ├── NON → Email ou message structure suffit
│           └── OUI → PLANIFIER LA REUNION
│               ├── Definir l'agenda (max 3 points)
│               ├── Identifier les participants essentiels uniquement
│               ├── Fixer la duree minimale necessaire (25 ou 50 min)
│               └── Distribuer le pre-read 24h avant
```

### Channel Architecture Pattern

| Prefixe | Usage | Exemples |
|---|---|---|
| `#announce-` | Communications officielles (lecture seule pour la plupart) | `#announce-general`, `#announce-rh` |
| `#team-` | Espace d'equipe pour la coordination quotidienne | `#team-product`, `#team-engineering` |
| `#project-` | Channels dedies a un projet avec date de fin | `#project-migration-crm`, `#project-launch-v2` |
| `#topic-` | Discussions thematiques transverses | `#topic-design-system`, `#topic-data-privacy` |
| `#help-` | Support et questions | `#help-it`, `#help-rh`, `#help-finance` |
| `#social-` | Conversations informelles et cohesion | `#social-random`, `#social-food`, `#social-sports` |
| `#ext-` | Channels avec des partenaires externes | `#ext-agency-design`, `#ext-client-alpha` |
| `#bot-` ou `#feed-` | Notifications automatisees (CI/CD, alertes, RSS) | `#feed-github`, `#bot-monitoring` |

### RACI for Digital Tools

| Outil | Responsable (admin) | Accountable (sponsor) | Consulted | Informed |
|---|---|---|---|---|
| **Teams/Slack** | IT + Collaboration Lead | CTO/COO | Managers d'equipe | Tous les collaborateurs |
| **Miro/FigJam** | Design Lead ou PMO | Head of Product | Facilitateurs | Participants ateliers |
| **Loom** | Collaboration Lead | VP Engineering | Equipes distribuees | Tous |
| **Zoom/Meet** | IT | CTO | Managers | Tous |
| **Documentation** (Notion/Confluence) | Knowledge Manager | COO | Leads d'equipe | Tous |

### Async Communication Protocol

1. **Structurer** — Chaque message async doit avoir : un titre/sujet clair, le contexte necessaire, la demande precise, la date limite de reponse attendue
2. **Contextualiser** — Fournir tout le contexte dans le message. Le destinataire ne doit pas avoir a poser de questions de clarification pour comprendre
3. **Prioriser** — Indiquer le niveau d'urgence. Utiliser des conventions : `[FYI]` (pas de reponse attendue), `[Input needed by DATE]`, `[Decision required by DATE]`, `[Urgent]`
4. **Centraliser** — Poster dans le bon channel, pas en message prive. L'information doit etre visible par tous ceux qui pourraient en avoir besoin
5. **Boucler** — Toujours fermer la boucle : accuser reception, confirmer la decision, partager le resultat. Un message sans conclusion est un thread mort

---

## Decision Guide

### Choisir le mode de communication

```
Quel type d'information dois-je transmettre ?
├── Mise a jour de statut / avancement → Post async dans le channel d'equipe
├── Question operationnelle rapide → Message dans le thread ou channel dedie
├── Explication complexe necessitant du contexte → Loom video (3-5 min)
├── Decision necessitant des inputs multiples → RFC document + commentaires async
├── Sujet sensible ou emotionnel → Appel 1:1 video ou en personne
├── Brainstorming creatif → Atelier Miro/FigJam (pre-work async + session sync)
└── Alignement strategique d'equipe → Reunion structuree avec agenda
```

### Choisir l'outil de collaboration

```
Quel est le besoin principal ?
├── Communication textuelle rapide
│   ├── Conversation operationnelle d'equipe → Slack / Teams chat
│   ├── Communication officielle → Channel d'annonce
│   └── Discussion structuree longue → Document (Notion, Confluence, Google Docs)
├── Communication video
│   ├── Explication asynchrone → Loom / ScreenPal
│   ├── Reunion interactive → Zoom / Teams / Meet
│   └── Presentation a large audience → Teams Town Hall / Zoom Webinar
├── Collaboration visuelle
│   ├── Atelier / workshop structure → Miro (features avancees, templates)
│   ├── Brainstorming rapide en equipe produit → FigJam (integration Figma)
│   └── Whiteboarding en reunion Teams → Microsoft Whiteboard
└── Documentation durable
    ├── Base de connaissances → Notion / Confluence
    ├── Documents collaboratifs → Google Docs / Microsoft Loop
    └── Decision records → ADR dans le repo ou Notion
```

---

## Common Patterns & Anti-Patterns

### Patterns (Do)

- **Convention de nommage stricte pour les channels** : definir un schema de nommage (`prefixe-domaine-sujet`) et l'appliquer sans exception. Documenter la convention dans un channel `#meta-workspace` ou dans le wiki interne. Auditer regulierement les channels qui ne respectent pas la convention et les renommer ou archiver.
- **Conversations threadees obligatoires** : dans Slack comme dans Teams, imposer l'usage des threads pour les discussions. Les messages dans le channel principal ne doivent contenir que le sujet initial. Tout le debat se passe dans le thread. Cela reduit considerablement le bruit et rend l'historique lisible.
- **Status updates en async** : les mises a jour d'avancement (standup, weekly update) se font en mode asynchrone via un bot (Geekbot, Standuply) ou un post structure dans le channel d'equipe. Reserver le standup synchrone aux impediments qui necessitent une resolution collective immediate.
- **Agenda distribue 24h avant chaque reunion** : pas d'agenda, pas de reunion. L'agenda doit inclure l'objectif de la reunion, les points a traiter (avec le temps alloue), les decisions attendues, et les pre-reads necessaires. L'animateur est responsable de l'agenda.
- **Loom pour le contexte, pas pour la reunion** : utiliser Loom pour partager du contexte (demo, explication technique, revue de document) afin que la reunion synchrone soit consacree au debat et a la decision, pas a la presentation. Un Loom de 5 minutes peut remplacer 30 minutes de reunion.
- **Archivage proactif des channels** : archiver les channels inactifs depuis plus de 90 jours. Les channels de projet se ferment a la fin du projet. Un workspace propre est un workspace utilisable.

### Anti-Patterns (Avoid)

- **Slack comme email** : envoyer de longs messages non structures dans Slack comme on ecrirait un email. Slack est fait pour des echanges courts, structures, et threads. Les contenus longs appartiennent a un document ou un Loom.
- **Reunion pour tout** : planifier une reunion pour chaque question, chaque mise a jour, chaque decision. Le reflexe "on fait un call ?" est le premier destructeur de productivite dans les organisations distribuees. Se poser systematiquement la question : "est-ce que cela peut etre async ?"
- **Pas de gouvernance des channels** : laisser chacun creer des channels librement sans convention de nommage, sans responsable, sans politique d'archivage. En 6 mois, le workspace devient un labyrinthe de channels morts et de doublons.
- **Notification fatigue** : ne pas configurer ses notifications, utiliser `@channel` et `@here` sans discernement, ne pas respecter les horaires de Do Not Disturb. La surnotification detruit l'attention profonde et cree de l'anxiete. Former les equipes a la gestion des notifications.
- **Proliferation d'outils** : utiliser Teams ET Slack ET Discord ET WhatsApp pour des usages similaires. Chaque outil supplementaire fragmente l'information et augmente la charge cognitive. Choisir un outil principal par categorie et s'y tenir.
- **Decisions dans les couloirs** : prendre des decisions lors de conversations informelles au bureau sans les documenter ni les partager avec les collaborateurs distants. C'est le premier facteur d'exclusion dans le travail hybride.

---

## Implementation Workflow

### Phase 1 — Audit & Diagnostic (Semaine 1-2)
Auditer l'ecosysteme de collaboration existant : quels outils sont utilises, par qui, pour quoi, avec quelle satisfaction. Identifier les pain points (trop de reunions, information introuvable, outils redondants, exclusion des remote). Mesurer les metriques de base : nombre de reunions par personne/semaine, nombre de channels actifs, temps moyen en visioconference, satisfaction collaborateur sur la collaboration. Benchmarker avec les pratiques du marche.

### Phase 2 — Design de l'Architecture (Semaine 3-4)
Definir l'architecture cible : choix des outils par categorie (un outil principal, un outil secondaire le cas echeant), conventions de nommage des channels, gouvernance (qui cree, qui archive, qui administre), protocole de communication async, templates de reunions. Produire le "Collaboration Playbook" de l'organisation, document de reference pour tous les collaborateurs.

### Phase 3 — Migration & Setup (Semaine 5-8)
Deployer l'architecture cible : restructurer les channels existants selon les nouvelles conventions, configurer les integrations (bots, workflows, connecteurs), mettre en place les templates (reunions, standups async, retrospectives). Former les administrateurs et les champions de la collaboration (2-3 par equipe). Preparer les guides utilisateurs et les FAQ.

### Phase 4 — Formation & Adoption (Semaine 9-12)
Former l'ensemble des collaborateurs par vagues : sessions de 60 minutes par equipe couvrant les conventions, les outils, et les protocoles. Identifier et traiter les resistances (habitudes email, preference pour le presentiel, peur de la visibilite). Mettre en place les mecanismes de feedback (channel dedie, pulse survey). Lancer un challenge d'adoption (reduire le nombre de reunions de 20%, augmenter l'utilisation des threads de 50%).

### Phase 5 — Optimisation Continue (Mois 4+)
Mesurer les metriques d'adoption et de satisfaction mensuellement. Auditer les channels trimestriellement (archivage, renommage, consolidation). Iterer sur le Collaboration Playbook en fonction des retours. Evaluer les nouvelles fonctionnalites des outils (IA, automatisation) et les integrer. Organiser une retrospective semestrielle sur les pratiques de collaboration.

---

## Modele de maturite

### Niveau 1 — Ad-hoc
- Outils de collaboration non standardises, chaque equipe utilise ce qu'elle veut
- Pas de conventions de nommage, pas de gouvernance des channels
- Reunions par defaut pour toute communication, pas de culture async
- **Indicateurs** : > 20 heures/semaine en reunion par personne, satisfaction collaboration < 40%, information introuvable

### Niveau 2 — Standardise
- Plateforme de messagerie unique choisie (Teams ou Slack), conventions de base en place
- Quelques channels structures, debut de gouvernance (archivage, nommage)
- Visioconference standardisee, debut de sensibilisation a l'async
- **Indicateurs** : 15-20 heures/semaine en reunion, satisfaction 40-55%, channels structures > 50%

### Niveau 3 — Structure
- Architecture de channels mature avec conventions strictes et gouvernance active
- Protocole async en place : standups async, Loom pour le contexte, RFC pour les decisions
- Reunions disciplinees : agenda obligatoire, duree optimisee, compte-rendu systematique
- **Indicateurs** : 10-15 heures/semaine en reunion, satisfaction 55-70%, adoption async > 60%

### Niveau 4 — Optimise
- Culture async-first verifiee dans les pratiques quotidiennes
- Outils de collaboration visuelle integres dans les processus (ateliers Miro, retrospectives FigJam)
- Metriques de collaboration suivies et analysees, amelioration continue en place
- **Indicateurs** : 8-12 heures/semaine en reunion, satisfaction 70-85%, documentation a jour > 80%

### Niveau 5 — Augmente
- IA integree dans la collaboration : resumes automatiques, recherche semantique, assistants
- Collaboration spatiale et persistante (virtual rooms, whiteboards permanents)
- Equipes distribuees aussi performantes que les equipes co-localisees, equite hybride atteinte
- **Indicateurs** : < 8 heures/semaine en reunion, satisfaction > 85%, zero information perdue

---

## Rythme operationnel

| Cadence | Activite | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Quotidien** | Standup async (bot ou post structure dans le channel d'equipe) | Chaque membre d'equipe | Post standup dans le channel |
| **Hebdomadaire** | Revue des channels et threads non resolus | Collaboration Champion | Threads fermes, redirections |
| **Hebdomadaire** | Weekly team sync (25 min max, agenda obligatoire) | Team Lead | Compte-rendu avec actions |
| **Mensuel** | Audit des metriques de collaboration (heures reunion, adoption async) | Collaboration Lead | Dashboard collaboration |
| **Mensuel** | Revue des integrations et bots (fonctionnement, pertinence) | IT / Admin workspace | Liste des integrations actives |
| **Trimestriel** | Audit des channels (archivage inactifs, renommage, consolidation) | Collaboration Lead + IT | Workspace nettoye |
| **Trimestriel** | Retrospective collaboration (ce qui fonctionne, ce qui freine) | Collaboration Lead | Plan d'amelioration |
| **Semestriel** | Mise a jour du Collaboration Playbook | Collaboration Lead | Playbook v.N+1 |
| **Annuel** | Evaluation des outils et benchmark marche | IT + Collaboration Lead | Recommandations strategiques |

---

## State of the Art (2025-2026)

La collaboration digitale entre dans l'ere de l'intelligence augmentee et de l'integration transparente :

- **AI Meeting Summaries & Action Items** : Microsoft Copilot dans Teams, Otter.ai, Fireflies.ai, Granola generent automatiquement des resumes de reunions, identifient les decisions prises et les actions a mener, et les assignent aux participants. Le compte-rendu manuel devient obsolete. L'enjeu est la qualite et la fiabilite de ces resumes automatiques.
- **AI-Powered Search & Knowledge** : la recherche dans les messages, documents et enregistrements video devient semantique grace a l'IA. Microsoft Copilot dans Teams permet de poser des questions en langage naturel sur l'historique des conversations. Slack AI propose des resumes de channels et une recherche contextuelle. Glean et Guru federent la recherche cross-outils.
- **Spatial & Persistent Collaboration** : les outils evoluent vers la collaboration spatiale persistante. Les boards Miro deviennent des espaces de travail permanents (pas seulement pour les ateliers). Microsoft Loop propose des composants collaboratifs portables entre les applications. Notion et Coda combinent documentation et collaboration en temps reel.
- **Persistent Virtual Rooms** : des outils comme Gather, Teamflow et les channels vocaux persistants de Slack (Huddles) ou Discord creent des espaces virtuels ou les collegues peuvent se "retrouver" sans planifier de reunion formelle, recreant la spontaneite du bureau.
- **AI Assistants in Platforms** : les assistants IA embarques dans Teams (Copilot), Slack (Slack AI + integrations GPT), et les outils de collaboration repondent aux questions, suggerent des actions, et automatisent les taches repetitives directement dans le flux de travail. L'assistant IA devient un membre a part entiere de l'equipe digitale.
- **Async Video Intelligence** : Loom integre l'IA pour generer des resumes automatiques, des chapitres, et des transcriptions indexees. Les videos async deviennent cherchables et analysables, transformant la video d'un format ephemere en une base de connaissances durable.

---

## Template actionnable

### Checklist efficacite reunion

| # | Critere | Statut | Commentaire |
|---|---------|--------|-------------|
| 1 | L'objectif de la reunion est clairement defini en une phrase | ☐ | ___ |
| 2 | L'objectif ne peut PAS etre atteint en async (document, Loom, message) | ☐ | ___ |
| 3 | L'agenda est distribue au moins 24h avant avec les points et durees | ☐ | ___ |
| 4 | Le pre-read est fourni et les participants ont eu le temps de le lire | ☐ | ___ |
| 5 | Seuls les participants essentiels sont invites (max 7 pour une decision) | ☐ | ___ |
| 6 | Un animateur est designe et responsable du respect de l'agenda | ☐ | ___ |
| 7 | Un note-taker est designe (ou un outil IA de prise de notes est active) | ☐ | ___ |
| 8 | La duree est de 25 ou 50 minutes (pas 30 ou 60, pour laisser des pauses) | ☐ | ___ |
| 9 | La reunion commence et finit a l'heure | ☐ | ___ |
| 10 | Les decisions sont documentees dans le channel ou le document dedie | ☐ | ___ |
| 11 | Les actions sont assignees avec un responsable et une date limite | ☐ | ___ |
| 12 | Le compte-rendu est partage dans les 2 heures suivant la reunion | ☐ | ___ |
| 13 | Les participants distants ont eu un acces equitable a la parole | ☐ | ___ |
| 14 | La prochaine reunion n'est planifiee que si elle est necessaire | ☐ | ___ |

---

## Prompts types

- "Aide-moi a concevoir l'architecture de channels Slack pour une organisation de 200 personnes avec 8 equipes produit"
- "Propose un protocole de communication asynchrone pour une equipe repartie sur 3 fuseaux horaires"
- "Comment faciliter un atelier de brainstorming sur Miro avec 25 participants distants ?"
- "Redige un Collaboration Playbook pour notre passage en mode hybride (3 jours bureau, 2 jours remote)"
- "Comment reduire le nombre de reunions de 30% sans perdre en alignement d'equipe ?"
- "Propose un format de standup asynchrone efficace avec un bot Slack"
- "Comment structurer une retrospective d'equipe sur FigJam en 45 minutes ?"
- "Aide-moi a configurer Microsoft Teams pour un projet transverse de 6 mois avec 4 equipes"

---

## Limites et Red Flags

Ce skill n'est PAS adapte pour :
- Concevoir une strategie de communication corporate ou de relations presse → Utiliser plutot : `entreprise:communication`
- Gerer des projets complexes (planification, jalons, risques, budget) → Utiliser plutot : `entreprise:gestion-de-projets`
- Construire des workflows d'automatisation metier (Zapier, Make, Power Automate) → Utiliser plutot : `productivite:automatisation-workflows`
- Mettre en place une infrastructure IT ou un digital workplace complet → Utiliser plutot : `entreprise:it-systemes`
- Definir une strategie RH pour le travail hybride (politique, droit du travail, accord collectif) → Utiliser plutot : `entreprise:rh`

Signaux d'alerte en cours d'utilisation :
- Les collaborateurs passent plus de 20 heures par semaine en reunion — le probleme n'est pas l'outil mais la culture de reunion. Intervenir sur les pratiques, pas sur la technologie
- Le workspace contient plus de 50% de channels inactifs — absence de gouvernance, lancer un audit et un archivage massif
- Les equipes utilisent plus de 5 outils de messagerie differents — proliferation d'outils, rationaliser et converger vers un outil principal
- Les collaborateurs distants se plaignent d'etre exclus des decisions — probleme d'equite hybride, revoir le protocole de documentation des decisions
- Le taux d'adoption des conventions async est inferieur a 30% apres 3 mois — resistance au changement, renforcer la formation et l'accompagnement managerial

---

## Skills connexes

| Skill | Lien |
|---|---|
| Communication Corporate | `entreprise:communication` — Communication institutionnelle, relations presse, gestion de crise |
| Gestion de Projets | `entreprise:gestion-de-projets` — Planification, pilotage et livraison de projets |
| Automatisation Workflows | `productivite:automatisation-workflows` — Automatisation des processus metier |
| IT & Systemes | `entreprise:it-systemes` — Infrastructure digitale et digital workplace |
| RH | `entreprise:rh` — Politique de travail hybride, engagement collaborateur |
| Excel & Spreadsheets | `productivite:excel-spreadsheets` — Donnees et tableaux collaboratifs |
| AI Copilots Productivite | `productivite:ai-copilots-productivite` — IA generative pour la productivite |

---

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[Messaging Platforms](./references/messaging-platforms.md)** — Microsoft Teams architecture (teams, channels, tabs, apps), Teams advanced features (breakout rooms, town halls, Loop components), Slack workspace design (channels, sections, workflows, canvas), Slack advanced features (Slack Connect, Huddles, Workflow Builder), comparaison Teams vs Slack, conventions de nommage, gouvernance, notifications, integrations et bots, securite et compliance.

- **[Visual Collaboration](./references/visual-collaboration.md)** — Miro fundamentals (boards, frames, templates), Miro advanced (voting, timer, presentation mode, integrations), FigJam features et workflows, Microsoft Whiteboard, techniques de facilitation digitale, design d'ateliers a distance, ice-breakers, templates de pensee visuelle (affinity diagram, empathy map, business model canvas, retrospective), collaboration visuelle async vs temps reel.

- **[Async & Remote Work](./references/async-remote-work.md)** — Principes de communication asynchrone, Loom pour la video async (enregistrement, partage, reactions, taches), outils de screen recording, standups async, culture documentation-first, gestion des fuseaux horaires, bonnes pratiques du travail a distance, decision-making async (RFC, ADR), confiance a distance, onboarding async, mesure de l'efficacite async.

- **[Meeting & Facilitation](./references/meeting-facilitation.md)** — Types et formats de reunion (standup, review, brainstorm, decision, 1:1), preparation (agenda, pre-read, roles), techniques de facilitation (timeboxing, round robin, silent brainstorm, dot voting), comptes-rendus et suivi des actions, bonnes pratiques de visioconference (Zoom, Teams, Meet), defis des reunions hybrides, assistants IA de reunion (Otter.ai, Fireflies, Granola, Copilot), analytics de reunion, annulation des reunions inutiles.
