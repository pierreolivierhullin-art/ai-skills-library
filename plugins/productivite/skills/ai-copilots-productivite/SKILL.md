---
name: ai-copilots-productivite
description: This skill should be used when the user asks about "Microsoft 365 Copilot", "Copilot in Word", "Copilot in Excel", "Copilot in PowerPoint", "Copilot in Teams", "Copilot in Outlook", "Google Gemini Workspace", "Gemini in Docs", "Gemini in Sheets", "AI productivity tools", "ChatGPT for work", "Claude for productivity", "AI writing assistant", "AI meeting summary", "AI email drafting", "GitHub Copilot", "AI agents personal", "copilotes IA", "productivité augmentée", "IA bureautique", "assistant IA", "automatisation IA", "prompts bureautiques", "agents IA personnels", "IA dans Office", "IA dans Google Workspace", discusses AI copilots for productivity, AI-powered office tools, or needs guidance on leveraging AI assistants in daily work, Microsoft 365 Copilot, Google Gemini, and personal AI workflows.
version: 1.0.0
last_updated: 2026-02
---

# AI Copilots & Productivite Augmentee / AI Copilots & Augmented Productivity

## Overview

**FR** — Cette skill couvre l'ensemble des copilotes IA integres aux outils de productivite : Microsoft 365 Copilot (Word, Excel, PowerPoint, Outlook, Teams), Google Gemini Workspace (Docs, Sheets, Slides, Gmail, Meet), ChatGPT (via interface web, API et Custom GPTs), Claude (Projects, Code, MCP), GitHub Copilot pour le developpement, et les assistants IA de reunion (Otter, Fireflies, Granola). Elle couvre egalement les agents IA personnels — workflows automatises qui executent des taches de maniere autonome avec supervision humaine. Les copilotes IA representent le bond de productivite le plus important depuis le smartphone. En 2026, les maitriser n'est plus optionnel : c'est un avantage competitif individuel et organisationnel. La productivite augmentee par l'IA ne consiste pas a remplacer le travail humain, mais a amplifier les capacites cognitives — redaction, analyse, synthese, communication, decision — par une collaboration intelligente avec l'IA. Les recommandations couvrent le deploiement, l'adoption, le prompt engineering specifique a chaque outil, la securite des donnees, et la construction de workflows IA personnels.

**EN** — This skill covers all AI copilots integrated into productivity tools: Microsoft 365 Copilot (Word, Excel, PowerPoint, Outlook, Teams), Google Gemini Workspace (Docs, Sheets, Slides, Gmail, Meet), ChatGPT (via web interface, API, and Custom GPTs), Claude (Projects, Code, MCP), GitHub Copilot for development, and AI meeting assistants (Otter, Fireflies, Granola). It also covers personal AI agents — automated workflows that execute tasks autonomously with human oversight. AI copilots represent the single biggest productivity leap since the smartphone. In 2026, mastering them is no longer optional: it is an individual and organizational competitive advantage. AI-augmented productivity is not about replacing human work, but amplifying cognitive capabilities — writing, analysis, synthesis, communication, decision-making — through intelligent collaboration with AI. Recommendations cover deployment, adoption, tool-specific prompt engineering, data security, and building personal AI workflows.

---

## When This Skill Applies

Activate this skill when the user:

- Deploie ou administre Microsoft 365 Copilot dans une organisation (licences, securite, adoption)
- Utilise Gemini dans Google Workspace (Docs, Sheets, Slides, Gmail, Meet) pour accelerer son travail
- Redige des documents, emails, rapports ou presentations assistes par IA (premier brouillon, reecriture, reformulation)
- Analyse des donnees a l'aide d'un copilote IA (Excel Copilot, Gemini in Sheets, ChatGPT Advanced Data Analysis)
- Cherche a generer des resumes de reunions IA (Teams Copilot, Gemini in Meet, Otter, Fireflies, Granola)
- Souhaite automatiser la redaction d'emails avec l'IA (Outlook Copilot, Gemini in Gmail, ChatGPT)
- Construit des workflows IA personnels combinant plusieurs outils (Custom GPTs, Claude Projects, MCP, N8N + IA)
- Deploie ou evalue des agents IA autonomes pour des taches recurrentes (triage email, recherche, creation de contenu)
- Selectionne le bon outil IA pour un cas d'usage specifique (M365 Copilot vs Gemini vs ChatGPT vs Claude)
- Forme des equipes a l'utilisation des copilotes IA et au prompt engineering bureautique

---

## Core Principles

### 1. Human in the Loop Always
L'IA genere, l'humain decide. Aucune sortie d'IA ne doit etre publiee, envoyee ou utilisee sans relecture humaine. Le copilote produit un brouillon — l'humain le valide, l'enrichit et l'approuve. L'IA n'a pas de jugement contextuel : elle ne connait pas la politique interne, les sensibilites relationnelles, ni les implications strategiques. La responsabilite reste humaine a 100%. Cela ne ralentit pas — cela securise. / AI generates, humans decide. No AI output should be published, sent, or used without human review. The copilot produces a draft — the human validates, enriches, and approves. AI lacks contextual judgment: it does not know internal politics, relational sensitivities, or strategic implications. Responsibility remains 100% human.

### 2. Prompt Quality Determines Output Quality
La qualite de la sortie IA est directement proportionnelle a la qualite du prompt. Un prompt vague produit un resultat generique. Un prompt precis — avec contexte, role, format, exemples et contraintes — produit un resultat exploitable. Investir 2 minutes dans la formulation du prompt fait gagner 20 minutes de corrections. Le prompt engineering n'est pas une competence technique — c'est une competence de communication avec la machine. / Output quality is directly proportional to prompt quality. A vague prompt produces generic results. A precise prompt — with context, role, format, examples, and constraints — produces actionable results. Investing 2 minutes in prompt formulation saves 20 minutes of corrections.

### 3. Context is King
Plus le copilote dispose de contexte, meilleur est le resultat. Fournir les documents de reference, le ton souhaite, l'audience cible, les contraintes specifiques, les exemples de resultats anterieurs. Dans M365 Copilot, le contexte inclut les fichiers SharePoint, les emails Outlook, les conversations Teams — via Microsoft Graph. Dans Claude Projects, le contexte provient des fichiers uploades et des instructions custom. Sans contexte, l'IA improvise. Avec contexte, l'IA performe. / The more context the copilot has, the better the result. Provide reference documents, desired tone, target audience, specific constraints, and examples of previous outputs. Without context, AI improvises. With context, AI performs.

### 4. Verify Before Trusting
L'IA produit des contenus plausibles, pas necessairement corrects. Les hallucinations sont reelles — chiffres inventes, sources inexistantes, logique apparente mais fausse. Toujours verifier : les donnees chiffrees contre la source, les citations contre l'original, les analyses contre le bon sens metier. Ne jamais faire confiance a un calcul IA sans le recalculer. Ne jamais envoyer un email IA sans le relire. La confiance se construit usage par usage, pas par defaut. / AI produces plausible content, not necessarily correct content. Hallucinations are real — invented numbers, non-existent sources, apparent but false logic. Always verify: numerical data against sources, quotes against originals, analyses against business common sense.

### 5. Compound Gains Through Consistency
Le gain de productivite IA est cumulatif. Utiliser un copilote une fois par semaine produit un gain marginal. L'utiliser systematiquement — pour chaque email, chaque resume, chaque analyse, chaque brouillon — produit un gain compose de 30-60 minutes par jour. La cle est la consistance : construire des habitudes d'utilisation, une bibliotheque de prompts, des templates reutilisables, et des workflows automatises. Le ROI de l'IA se mesure en habitudes, pas en exploits ponctuels. / AI productivity gains are cumulative. Using a copilot once a week produces marginal benefit. Using it systematically — for every email, summary, analysis, draft — produces compound gains of 30-60 minutes per day. The key is consistency.

### 6. Privacy and Data Awareness
Chaque outil IA a des politiques de donnees differentes. M365 Copilot traite les donnees dans le tenant Microsoft (residentes). ChatGPT gratuit utilise les donnees pour l'entrainement. Claude Pro ne s'entraine pas sur les donnees utilisateur. Connaitre les frontieres : ne jamais partager de donnees confidentielles, personnelles, ou strategiques dans un outil dont la politique de donnees ne le permet pas. Classifier les donnees avant de les soumettre a l'IA : publiques, internes, confidentielles, restreintes. Les donnees confidentielles et restreintes exigent des outils conformes (M365 Copilot, Claude Enterprise, Azure OpenAI). / Every AI tool has different data policies. Know the boundaries: never share confidential, personal, or strategic data in a tool whose data policy does not allow it. Classify data before submitting to AI: public, internal, confidential, restricted.

---

## Key Frameworks & Methods

### AI Copilot Maturity Model

| Niveau | Description | Caracteristiques |
|--------|-------------|-----------------|
| **1 — Experimentation** | Usage ad-hoc, curiosite individuelle | Quelques utilisateurs testent ChatGPT/Gemini, pas de cadre, pas de politique |
| **2 — Adoption guidee** | Pilotes structures, formation initiale | Licences M365 Copilot deployees, prompts de base, quick wins identifies |
| **3 — Integration** | IA integree aux processus quotidiens | Bibliotheque de prompts, templates, usage systematique, metriques d'adoption |
| **4 — Optimisation** | Workflows IA avances, gains mesures | Custom GPTs, Claude Projects, chaines de prompts, ROI quantifie |
| **5 — Agents & Autonomie** | Agents IA autonomes, orchestration | Agents MCP, copilot orchestration, IA proactive, apprentissage continu |

### Prompt Pattern Catalog for Productivity

| Pattern | Description | Exemple |
|---------|-------------|---------|
| **Role + Task + Format** | Definir un role, une tache, et un format de sortie | "Tu es un redacteur executif. Redige un email de 5 lignes pour..." |
| **Context Injection** | Fournir des documents ou donnees de reference | "Voici le rapport Q3 [coller]. Resume les 5 points cles..." |
| **Iterative Refinement** | Demander puis affiner en plusieurs echanges | "Reecris avec un ton plus formel" / "Ajoute des chiffres" |
| **Template Fill** | Fournir un template a completer par l'IA | "Remplis ce template de compte-rendu avec les notes suivantes..." |
| **Chain of Thought** | Demander un raisonnement etape par etape | "Analyse ce tableau de donnees etape par etape avant de conclure" |
| **Constraint Setting** | Imposer des contraintes explicites | "Maximum 200 mots, ton professionnel, pas de jargon technique" |

### AI Task Suitability Matrix

| Type de tache | Aptitude IA | Revue humaine | Exemples |
|---------------|-------------|---------------|----------|
| **Brouillon de texte** | Tres elevee | Relecture obligatoire | Emails, rapports, presentations |
| **Resume / synthese** | Tres elevee | Verification des points cles | Reunions, documents, fils de discussion |
| **Analyse de donnees** | Elevee | Validation des conclusions | Tendances, anomalies, correlations |
| **Recherche / exploration** | Elevee | Verification des sources | Veille, benchmarks, etat de l'art |
| **Traduction / reformulation** | Elevee | Relecture legere | Emails, documents, contenu marketing |
| **Generation de code** | Elevee | Code review obligatoire | Scripts, formules, automatisations |
| **Decision strategique** | Faible | Decision humaine integrale | Budget, recrutement, strategie |
| **Jugement ethique** | Tres faible | Decision humaine integrale | Conformite, ethique, discipline |

### AI Tool Selection Guide

| Critere | M365 Copilot | Google Gemini | ChatGPT Plus | Claude Pro |
|---------|-------------|---------------|-------------|------------|
| **Ecosysteme** | Microsoft 365 | Google Workspace | Standalone + API | Standalone + API |
| **Integration native** | Word, Excel, PPT, Teams, Outlook | Docs, Sheets, Slides, Gmail, Meet | Web, mobile, plugins | Web, mobile, Projects |
| **Donnees d'entreprise** | Microsoft Graph, SharePoint, OneDrive | Google Drive, BigQuery | Upload, browsing | Upload, Projects, MCP |
| **Securite donnees** | Tenant-resident, Purview | Google Cloud, DLP | OpenAI policies | Pas d'entrainement user data |
| **Custom agents** | Copilot Studio | Google AI Studio | Custom GPTs, Assistants API | Claude Projects, MCP |
| **Cout/utilisateur/mois** | ~30 EUR (E3+Copilot) | ~20 EUR (Business+AI) | ~20 EUR (Plus) | ~20 EUR (Pro) |
| **Ideal pour** | Organisations full Microsoft | Organisations full Google | Polyvalence, usage personnel | Analyse longue, code, precision |

### ROI Calculation for AI Copilots

| Facteur | Formule | Exemple |
|---------|---------|---------|
| **Temps gagne / jour / utilisateur** | (minutes gagnees par tache) x (frequence quotidienne) | 5 min x 8 taches = 40 min/jour |
| **Equivalent salaire** | (temps gagne annuel) x (cout horaire moyen) | 160h x 50 EUR/h = 8 000 EUR/an/utilisateur |
| **Cout licence** | (prix licence IA) x (nombre utilisateurs) x 12 | 30 EUR x 100 x 12 = 36 000 EUR/an |
| **ROI** | (valeur temps gagne - cout licence - cout formation) / cout total | (800K - 36K - 20K) / 56K = 1 328% |
| **Payback period** | cout total / (valeur temps gagne mensuelle) | 56K / 66K = 0.85 mois |

---

## Decision Guide

### Choosing the Right AI Tool for a Task

```
Quel est le type de tache ?
├── Redaction/email/presentation dans Microsoft 365 ?
│   └── M365 COPILOT (integration native, contexte Graph)
├── Redaction/email/presentation dans Google Workspace ?
│   └── GEMINI WORKSPACE (integration native, contexte Drive)
├── Analyse de donnees complexe (Excel) ?
│   ├── Donnees dans un classeur Excel → M365 COPILOT IN EXCEL
│   └── Donnees a uploader / analyser librement → CHATGPT ADA ou CLAUDE
├── Redaction longue, analyse approfondie, recherche ?
│   ├── Besoin de precision et nuance → CLAUDE
│   └── Besoin de browsing web et plugins → CHATGPT PLUS
├── Code / developpement ?
│   ├── IDE (VS Code, JetBrains) → GITHUB COPILOT
│   └── Terminal / projets complexes → CLAUDE CODE
├── Resume de reunion ?
│   ├── Microsoft Teams → COPILOT IN TEAMS
│   ├── Google Meet → GEMINI IN MEET
│   └── Multi-plateforme → OTTER / FIREFLIES / GRANOLA
└── Agent autonome / workflow automatise ?
    ├── Ecosysteme Microsoft → COPILOT STUDIO
    ├── Custom tool use / MCP → CLAUDE + MCP
    └── No-code automation → N8N + IA / MAKE + IA
```

### When to Use AI vs Manual

```
La tache est-elle repetitive et structuree ?
├── OUI → L'IA peut la realiser ?
│   ├── OUI → UTILISER L'IA (avec relecture)
│   └── NON → AUTOMATISER sans IA (macro, script, workflow)
└── NON → La tache requiert du jugement contextuel ?
    ├── OUI → FAIRE MANUELLEMENT (IA en support pour brouillons/recherche)
    └── NON → La tache est-elle creative ?
        ├── OUI → IA pour brainstorming et premier brouillon, humain pour finalisation
        └── NON → Evaluer au cas par cas
```

---

## Common Patterns & Anti-Patterns

### Patterns (Do)

- **Prompt Templates reutilisables** : Creer une bibliotheque de prompts par cas d'usage (email formel, resume de reunion, analyse de donnees, brainstorming). Stocker les templates dans un document partage, un Custom GPT, ou un Claude Project. Un bon prompt template est parametrable : [CONTEXTE], [AUDIENCE], [TON], [LONGUEUR]. Reutiliser plutot que reinventer a chaque fois.
- **Iterative Refinement** : Ne jamais accepter le premier resultat. Utiliser des prompts de suivi : "Rends le ton plus formel", "Reduis a 3 paragraphes", "Ajoute des donnees chiffrees", "Reformule pour un public non technique". L'IA s'ameliore significativement avec chaque iteration. 2-3 iterations produisent un resultat 3x meilleur que la premiere reponse.
- **AI for First Drafts** : Utiliser systematiquement l'IA pour le premier brouillon de tout document : email, rapport, presentation, proposition. L'humain passe de createur a editeur — un role plus rapide et plus strategique. Cela elimine le syndrome de la page blanche et reduit le temps de production de 40-60%.
- **AI for Data Analysis** : Pour toute analyse de donnees exploratoire, commencer par l'IA. "Analyse ce tableau et identifie les 5 tendances principales", "Quelles anomalies vois-tu dans ces donnees ?", "Propose 3 visualisations pertinentes". L'IA detecte des patterns que l'humain ne voit pas dans les gros volumes de donnees.
- **AI for Meeting Prep** : Avant chaque reunion importante, demander a l'IA de synthetiser les documents de reference, preparer les questions cles, et anticiper les objections. "Voici l'ordre du jour et les documents. Prepare un briefing de 5 points avec les questions a poser." Gain : 15-20 min de preparation par reunion.

### Anti-Patterns (Avoid)

- **Blind Trust (confiance aveugle)** : Copier-coller la sortie IA sans la lire. Les hallucinations sont frequentes : chiffres inventes, dates incorrectes, conclusions non supportees par les donnees. Chaque sortie IA doit etre traitee comme un brouillon a valider, pas comme un produit fini.
- **No Proofreading** : Envoyer un email redige par l'IA sans relecture. L'IA produit souvent un ton generique, des formulations maladroites, ou des erreurs de contexte (nom du destinataire, reference au mauvais projet). 30 secondes de relecture evitent des erreurs embarrassantes.
- **Sharing Confidential Data** : Copier des donnees RH, financieres, clients, ou strategiques dans ChatGPT gratuit ou un outil dont la politique de donnees ne garantit pas la confidentialite. Verifier la politique de donnees AVANT d'utiliser l'outil. Regles : donnees publiques partout, donnees internes dans les outils approuves, donnees confidentielles uniquement dans M365 Copilot ou outils tenant-resident.
- **AI for Critical Decisions Without Validation** : Utiliser la recommandation IA comme base de decision strategique sans validation par un expert humain. L'IA n'a pas acces au contexte complet (politique interne, historique des relations, contraintes non documentees). Les decisions critiques (recrutement, budget, strategie, conformite) exigent un jugement humain informe par l'IA, pas dicte par elle.
- **Prompt Laziness** : Ecrire des prompts vagues et se plaindre de resultats mediocres. "Resume ce texte" vs "Resume ce texte en 5 bullet points, en francais, pour un public de dirigeants, avec les chiffres cles." Le deuxieme prompt produit un resultat 10x plus utilisable. La qualite du prompt est la variable principale de la qualite du resultat.

---

## Implementation Workflow

### Phase 1 — Assessment & Quick Wins (Semaines 1-2)
Auditer les usages actuels de l'IA dans l'organisation (qui utilise quoi, comment, pour quelles taches). Identifier les 5-10 taches les plus chronophages et repetitives par role (redaction emails, resumes de reunions, rapports hebdomadaires, analyse de donnees). Deployer des outils IA gratuits ou existants pour ces taches (ChatGPT gratuit, Gemini gratuit). Mesurer le temps gagne sur les quick wins. Documenter les premiers resultats pour construire le business case.

### Phase 2 — Pilot Deployment (Semaines 3-6)
Selectionner l'outil IA principal (M365 Copilot ou Gemini Workspace selon l'ecosysteme). Deployer sur un groupe pilote de 20-50 utilisateurs motives. Former le groupe pilote au prompt engineering de base (role, contexte, format, contraintes). Mesurer l'adoption (frequence, taches couvertes) et la satisfaction. Collecter les retours pour affiner la strategie.

### Phase 3 — Prompt Library & Training (Semaines 7-10)
Construire une bibliotheque de prompts par metier et cas d'usage (templates parametrables). Creer un programme de formation en 3 niveaux (debutant, intermediaire, avance). Former les managers en priorite — ils sont le levier d'adoption. Publier un guide de bonnes pratiques et de securite des donnees. Mettre en place un canal de partage de prompts et de retours d'experience.

### Phase 4 — Full Rollout (Semaines 11-16)
Deployer les licences IA a l'ensemble de l'organisation. Activer les fonctionnalites avancees (Copilot in Teams, Copilot in Excel, Gemini in Meet). Integrer l'IA dans les processus standards (chaque compte-rendu de reunion passe par Copilot, chaque rapport hebdomadaire commence par un brouillon IA). Mesurer le ROI reel (temps gagne, qualite percue, adoption). Communiquer les resultats.

### Phase 5 — Advanced Workflows & Agents (Semaines 17+)
Construire des workflows IA avances : chaines de prompts, Custom GPTs specialises, Claude Projects avec instructions custom. Deployer des agents IA pour les taches recurrentes (triage email, veille concurrentielle, generation de rapports automatises). Explorer Copilot Studio et MCP pour des copilotes personnalises. Mettre en place un centre d'excellence IA pour capitaliser sur les apprentissages. Evaluer en continu et iterer.

---

## Modele de maturite

### Niveau 1 — Decouverte
- Usage individuel et sporadique de ChatGPT ou Gemini gratuit
- Pas de politique d'usage, pas de formation, pas de cadre
- Risques de securite des donnees non maitrises (donnees confidentielles partagees)
- **Indicateurs** : < 10% des employes utilisent l'IA, gain de productivite non mesurable

### Niveau 2 — Pilote
- Outils IA deployes sur un groupe pilote, formation de base
- Politique d'usage des donnees definie et communiquee
- Quick wins identifies et documentes (emails, resumes, brouillons)
- **Indicateurs** : 10-30% d'adoption dans le pilote, 15-20 min gagnes/jour/utilisateur actif

### Niveau 3 — Integration
- IA integree dans les processus quotidiens (reunions, emails, rapports, analyses)
- Bibliotheque de prompts partagee, templates par metier
- Formation systematique de tous les employes, champions IA identifies
- **Indicateurs** : 50-70% d'adoption, 30-45 min gagnes/jour, satisfaction > 7/10

### Niveau 4 — Optimisation
- Custom GPTs, Claude Projects, workflows IA avances en place
- ROI mesure et communique, gains de productivite quantifies
- Centre d'excellence IA qui capitalise et diffuse les bonnes pratiques
- **Indicateurs** : > 80% d'adoption, 45-60 min gagnes/jour, ROI > 500%

### Niveau 5 — Agents & Autonomie
- Agents IA autonomes deployees pour les taches recurrentes
- Copilot orchestration : plusieurs copilotes coordonnes dans des chaines
- IA proactive qui anticipe les besoins et propose des actions
- **Indicateurs** : > 90% d'adoption, > 60 min gagnes/jour, agents IA en production

---

## Rythme operationnel

| Cadence | Activite | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Quotidien** | Utilisation systematique du copilote IA pour emails, resumes, brouillons | Chaque collaborateur | Taches accelerees, premier brouillon IA |
| **Hebdomadaire** | Revue des prompts efficaces, partage de bonnes pratiques dans le canal IA | Champions IA | Prompts partages, tips de la semaine |
| **Hebdomadaire** | Verification de la qualite des sorties IA (spot-check sur 5-10 sorties) | Manager | Rapport qualite, corrections identifiees |
| **Mensuel** | Mesure d'adoption et de gains de productivite (usage, temps gagne, satisfaction) | Responsable IA | Dashboard d'adoption, metriques ROI |
| **Mensuel** | Mise a jour de la bibliotheque de prompts et des templates | Centre d'excellence IA | Bibliotheque enrichie, nouveaux templates |
| **Trimestriel** | Formation continue (nouvelles fonctionnalites, nouveaux outils, cas avances) | Formateur / Centre IA | Sessions de formation, certification |
| **Trimestriel** | Evaluation des nouveaux outils IA et fonctionnalites (veille technologique) | Responsable IA | Note d'evaluation, recommandations |
| **Annuel** | Revue strategique IA productivite (ROI global, roadmap, budget, evolution) | Direction / DSI | Bilan annuel, roadmap N+1 |

---

## State of the Art (2025-2026)

La productivite augmentee par l'IA evolue a un rythme sans precedent :

- **Agents IA autonomes** : Les copilotes passent de l'assistance reactive (l'utilisateur demande, l'IA repond) a l'autonomie proactive (l'IA detecte un besoin et agit). Exemples : agent de triage email qui classe, resume et pre-redige les reponses ; agent de veille qui collecte, filtre et synthetise l'information quotidiennement. OpenAI Operator, Claude Computer Use, Google Project Mariner. L'agent planifie, execute plusieurs etapes, utilise des outils, et livre le resultat — avec supervision humaine.

- **Copilotes multi-modaux** : Les copilotes comprennent et generent texte, images, audio, video et code dans la meme conversation. Analyser un graphique en image, generer une presentation avec des visuels, transcrire et resumer un enregistrement audio. GPT-4o, Gemini 2, Claude 4 sont nativement multi-modaux. L'interface devient naturelle — parler, montrer, ecrire, tout dans le meme flux de travail.

- **Copilot orchestration** : Plusieurs copilotes coordonnes dans des chaines automatisees. Exemple : Copilot Teams resume la reunion → Copilot Word genere le compte-rendu → Copilot Outlook envoie le suivi → Copilot Planner cree les taches. Copilot Studio (Microsoft) et Vertex AI (Google) permettent de construire ces chaines. L'orchestration transforme des assistants individuels en systemes de productivite integres.

- **IA dans chaque application** : Chaque SaaS integre desormais un copilote IA natif — Notion AI, Slack AI, Figma AI, Canva AI, Miro AI, Salesforce Einstein, HubSpot AI, Asana AI. Le copilote n'est plus un outil separe, mais une couche intelligente integree dans chaque application. Le defi passe de "comment utiliser l'IA" a "comment coordonner 15 copilotes IA differents".

- **IA personnelle qui apprend les preferences** : Les copilotes memorisent le style d'ecriture, les preferences de format, les contacts frequents, les projets en cours. Claude Projects et Custom GPTs permettent de creer des assistants specialises avec memoire persistante. La prochaine etape : un copilote personnel unique qui s'adapte a l'utilisateur au fil du temps, quel que soit l'outil.

---

## Template actionnable

### Checklist audit productivite IA

| # | Critere | Statut | Commentaire |
|---|---------|--------|-------------|
| 1 | Inventaire des outils IA utilises dans l'organisation (officiels et shadow AI) | ☐ | ___ |
| 2 | Politique d'usage des donnees avec l'IA definie et communiquee | ☐ | ___ |
| 3 | Classification des donnees (publiques, internes, confidentielles, restreintes) appliquee | ☐ | ___ |
| 4 | Licences IA deployees (M365 Copilot, Gemini, ChatGPT Team, Claude) | ☐ | ___ |
| 5 | Top 10 taches chronophages identifiees par role | ☐ | ___ |
| 6 | Quick wins IA documentes et mesures (temps gagne) | ☐ | ___ |
| 7 | Bibliotheque de prompts creee et partagee | ☐ | ___ |
| 8 | Formation prompt engineering de base dispensee (> 80% des equipes) | ☐ | ___ |
| 9 | Champions IA identifies dans chaque equipe | ☐ | ___ |
| 10 | Canal de partage de bonnes pratiques IA actif | ☐ | ___ |
| 11 | Metriques d'adoption mesurees (% utilisateurs actifs, frequence, taches) | ☐ | ___ |
| 12 | ROI calcule et communique a la direction | ☐ | ___ |
| 13 | Custom GPTs / Claude Projects crees pour les cas d'usage recurrents | ☐ | ___ |
| 14 | Workflows IA avances en place (chaines de prompts, agents) | ☐ | ___ |
| 15 | Revue trimestrielle des outils et fonctionnalites IA planifiee | ☐ | ___ |

---

## Prompts types

- "Aide-moi a deployer Microsoft 365 Copilot dans mon organisation de 200 personnes — strategie, phases, formation, metriques"
- "Propose une bibliotheque de 20 prompts pour les cas d'usage bureautiques les plus courants (email, resume, rapport, analyse)"
- "Compare M365 Copilot et Google Gemini Workspace pour une PME de 50 personnes sur Google Workspace — avantages, couts, migration"
- "Redige un email professionnel de reponse a cette demande client [coller l'email] avec un ton formel et empathique"
- "Analyse ce tableau de donnees [coller] et identifie les 5 tendances principales avec des recommandations actionnables"
- "Resume cette reunion de 45 minutes [coller la transcription] en 5 points cles avec les decisions et actions a suivre"
- "Aide-moi a creer un Custom GPT specialise pour la redaction de comptes-rendus de reunion dans mon entreprise"
- "Propose un workflow IA complet pour automatiser la veille concurrentielle hebdomadaire avec Claude + MCP + N8N"

---

## Limites et Red Flags

Ce skill n'est PAS adapte pour :
- Concevoir une strategie IA d'entreprise globale (gouvernance, roadmap, organisation) → Utiliser plutot : `ai-governance:strategie-ia`
- Gerer les risques ethiques et de conformite de l'IA → Utiliser plutot : `ai-governance:ai-ethics` ou `ai-governance:ai-risk`
- Construire des prompts systeme avances pour des applications IA en production → Utiliser plutot : `ai-governance:prompt-engineering-llmops`
- Developper des applications IA custom (RAG, fine-tuning, LLMOps) → Utiliser plutot : `ai-governance:prompt-engineering-llmops`
- Automatiser des processus metier complexes sans IA (workflows, BPM) → Utiliser plutot : `productivite:automatisation-workflows`

Signaux d'alerte en cours d'utilisation :
- Des employes partagent des donnees confidentielles (RH, finance, clients) dans ChatGPT gratuit — risque de fuite de donnees immediat
- L'adoption de Copilot est < 20% apres 3 mois — revoir la formation, les use cases, et le support managerial
- Les sorties IA sont publiees sans relecture — risque de qualite et de reputation
- Un seul "power user" concentre toute l'expertise IA — risque de personne cle, diffuser la competence
- L'organisation investit dans les licences IA sans mesurer le ROI — risque de gaspillage budgetaire
- Les agents IA autonomes sont deployes sans supervision humaine — risque d'erreurs en chaine non detectees

---

## Skills connexes

| Skill | Lien |
|---|---|
| Strategie IA | `ai-governance:strategie-ia` — Strategie IA d'entreprise, roadmap, gouvernance |
| AI Ethics | `ai-governance:ai-ethics` — Ethique IA, biais, transparence, impact |
| Prompt Engineering & LLMOps | `ai-governance:prompt-engineering-llmops` — Prompts avances, RAG, evaluation LLM |
| AI Risk | `ai-governance:ai-risk` — Risques IA, securite, robustesse |
| Excel & Spreadsheets | `productivite:excel-spreadsheets` — Tableurs avances, formules, Power Query |
| Automatisation Workflows | `productivite:automatisation-workflows` — Automatisation des processus metier |
| NoCode Apps | `productivite:nocode-apps` — Applications metier sans code |
| Decision Reporting & Governance | `data-bi:decision-reporting-governance` — Dashboards BI, KPIs, gouvernance |

---

## Additional Resources

Consult these reference files for deep dives on each topic area:

- **[Microsoft 365 Copilot](./references/microsoft-copilot.md)** — Architecture et licensing M365 Copilot, Copilot in Word (redaction, reecriture, mise en forme), Copilot in Excel (analyse, formules, graphiques, Python), Copilot in PowerPoint (generation de slides, design, notes), Copilot in Outlook (emails, resumes de fils), Copilot in Teams (resumes de reunions, actions), Copilot Studio, Microsoft Graph, prompt engineering M365, deploiement et adoption, securite et conformite (Purview, data residency).

- **[Google Gemini Workspace](./references/google-gemini-workspace.md)** — Gemini in Google Docs (Help me write, resume, reecriture), Gemini in Sheets (formules, analyse, organisation), Gemini in Slides (creation de slides, images), Gemini in Gmail (reponses, resumes), Gemini in Meet (notes, traduction), Gemini Advanced, Google AI Studio, NotebookLM, comparaison avec M365 Copilot, prompt engineering Gemini, pricing et deploiement.

- **[Workflows IA & Prompts Bureautiques](./references/ai-workflows-prompts.md)** — Patterns de prompt engineering pour la productivite (role, contexte, format, exemples), templates de prompts par cas d'usage (email, resume, analyse, brainstorming), chaines de prompts pour taches complexes, IA pour la redaction, l'analyse de donnees, la communication, construction d'une bibliotheque de prompts, automatisation IA avec N8N, Make, Power Automate, Custom GPTs et Claude Projects.

- **[Agents IA Personnels](./references/ai-agents-personal.md)** — Concept et architecture des agents IA personnels, Claude Code et MCP (Model Context Protocol), Custom GPTs (OpenAI), Claude Projects et instructions custom, agents pour le triage email, la recherche, le scheduling, la creation de contenu, workflows multi-etapes, tool use et function calling, securite et privacy, tendances 2026, build vs buy, evaluation et monitoring.
