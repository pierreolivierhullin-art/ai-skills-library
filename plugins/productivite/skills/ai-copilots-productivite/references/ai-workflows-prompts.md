# Workflows IA & Prompts Bureautiques — Patterns, Templates, Chaines & Automatisation

## Introduction

**FR** — Ce guide de reference couvre l'ensemble des techniques de prompting et de construction de workflows IA pour la productivite bureautique : patterns de prompt engineering (role, contexte, format, exemples, contraintes), templates de prompts par cas d'usage (redaction d'emails, resume de documents, analyse de donnees, preparation de reunions, brainstorming), chaines de prompts pour les taches complexes, IA pour la redaction (articles, rapports, propositions), IA pour l'analyse de donnees (langage naturel vers insights), IA pour la communication (ajustement de ton, traduction, simplification), construction d'une bibliotheque de prompts personnelle et organisationnelle, automatisation de workflows IA avec N8N, Make (Integromat), Power Automate, et la creation de Custom GPTs et Claude Projects pour les taches recurrentes. Ce document fournit des exemples concrets et actionnables pour chaque cas d'usage. Il reflete l'etat de l'art 2025-2026.

**EN** — This reference guide covers prompt engineering techniques and AI workflow construction for office productivity: prompt patterns (role, context, format, examples, constraints), prompt templates by use case (email drafting, document summarization, data analysis, meeting prep, brainstorming), chained prompts for complex tasks, AI for writing, data analysis, communication, building prompt libraries, and automating AI workflows with N8N, Make, Power Automate, Custom GPTs, and Claude Projects. This document provides concrete, actionable examples for each use case.

---

## 1. Prompt Engineering Patterns for Productivity

### Pattern 1 — Role + Task + Format (RTF)

Le pattern fondamental de tout prompt efficace. Definir qui l'IA doit etre (role), ce qu'elle doit faire (tache), et comment elle doit presenter le resultat (format).

**Structure** :
```
Tu es [ROLE].
[TACHE a accomplir avec contexte].
[FORMAT de sortie attendu].
```

**Exemple concret** :
```
Tu es un directeur financier experimente.
Analyse les resultats trimestriels suivants et identifie les 3 risques
principaux et les 3 opportunites majeures pour le trimestre a venir.
[Coller les donnees]
Presente les resultats dans un tableau a 2 colonnes (Risques | Opportunites)
avec une recommandation d'action pour chaque point. Maximum 1 page.
```

**Pourquoi ca fonctionne** : Le role calibre le niveau d'expertise et le vocabulaire. La tache definit l'objectif. Le format elimine l'ambiguite sur la structure attendue. Sans format, l'IA choisit un format generique qui necessite un reformatage.

### Pattern 2 — Context Injection

Fournir des donnees, documents, ou informations de reference dans le prompt pour que l'IA travaille sur un contexte precis plutot que sur ses connaissances generales.

**Structure** :
```
Voici [TYPE DE DOCUMENT] :
---
[CONTENU DU DOCUMENT]
---
A partir de ce document, [TACHE].
[FORMAT de sortie].
```

**Exemple concret** :
```
Voici le compte-rendu brut de la reunion du 15 janvier 2026 :
---
Participants : Marie (CEO), Jean (CTO), Sophie (CFO)
Discussion budget IT 2026 : Jean propose +20% pour la migration cloud.
Sophie alerte sur la tresorerie Q1, suggere report de 3 mois.
Marie tranche : budget valide a +15% avec demarrage en avril.
Action : Jean prepare le plan de migration pour le 1er fevrier.
Action : Sophie negocie le paiement echelonne avec le fournisseur cloud.
Prochaine reunion : 5 fevrier 2026.
---
A partir de ces notes, redige un compte-rendu de reunion professionnel
avec les sections : Contexte, Decisions, Actions (tableau), Prochaines etapes.
```

### Pattern 3 — Iterative Refinement (Multi-turn)

Ne pas essayer d'obtenir le resultat parfait en un seul prompt. Commencer large, puis affiner en plusieurs echanges.

**Workflow** :
1. **Prompt initial** : "Redige un email de proposition commerciale pour un service de conseil en IA"
2. **Affinement 1** : "Rends le ton plus formel et ajoute des chiffres de ROI"
3. **Affinement 2** : "Raccourcis a 8 lignes et ajoute un call-to-action clair"
4. **Affinement 3** : "Remplace 'intelligence artificielle' par 'IA' partout et ajoute une formule de politesse professionnelle"

**Pourquoi ca fonctionne** : Chaque iteration est simple et precise. L'IA conserve le contexte de la conversation et applique les modifications incrementalement. 3-4 iterations produisent un resultat significativement meilleur qu'un seul prompt complexe.

### Pattern 4 — Constraint Setting

Imposer des contraintes explicites pour cadrer la reponse et eviter les sorties generiques ou trop longues.

**Contraintes courantes** :
- Longueur : "Maximum 200 mots", "En 5 bullet points", "1 page maximum"
- Ton : "Professionnel", "Formel", "Decontracte", "Diplomatique", "Direct"
- Audience : "Pour un public de dirigeants non techniques", "Pour des ingenieurs"
- Format : "Tableau", "Liste numerotee", "Paragraphes structures", "JSON"
- Langue : "En francais", "Bilingue FR/EN", "Sans jargon technique"
- Exclusions : "Ne mentionne pas [sujet]", "Pas de jargon", "Pas d'emojis"

**Exemple concret** :
```
Resume ce rapport en exactement 5 bullet points.
Chaque bullet point doit faire 1-2 phrases maximum.
Ton : factuel et direct, pas de langage marketing.
Audience : conseil d'administration.
Ne mentionne pas les details techniques de l'implementation.
Mets en evidence les chiffres cles (CA, marge, croissance).
```

### Pattern 5 — Few-Shot Examples

Fournir 2-3 exemples du resultat attendu pour calibrer le style, le format, et le niveau de detail.

**Structure** :
```
Je veux que tu rediges [TYPE DE CONTENU] dans le style suivant.

Exemple 1 :
[Exemple de sortie attendue]

Exemple 2 :
[Autre exemple]

Maintenant, redige le meme type de contenu pour : [NOUVEAU SUJET].
```

**Exemple concret** :
```
Je veux que tu rediges des descriptions de produit pour notre site web
dans le style suivant :

Exemple 1 : "Plateforme Analytics Pro — Transformez vos donnees en decisions.
Connectez vos sources en 5 minutes, explorez avec des dashboards interactifs,
et partagez des insights en temps reel. A partir de 49 EUR/mois."

Exemple 2 : "Suite Collaboration — Travaillez ensemble, ou que vous soyez.
Documents partages, visioconference HD, et messagerie unifiee dans une seule
application. A partir de 12 EUR/utilisateur/mois."

Maintenant, redige une description pour notre nouveau produit :
"AI Assistant for Sales" — un assistant IA qui aide les commerciaux
a preparer leurs rendez-vous, qualifier les leads, et rediger les propositions.
Prix : 29 EUR/utilisateur/mois.
```

### Pattern 6 — Chain of Thought (CoT)

Demander a l'IA de raisonner etape par etape avant de conclure. Essentiel pour les taches d'analyse, de decision, ou de resolution de problemes.

**Structure** :
```
Analyse [SITUATION] etape par etape :
1. Identifie les faits cles
2. Identifie les hypotheses et les inconnues
3. Evalue les options possibles
4. Pondere les avantages et inconvenients de chaque option
5. Formule une recommandation argumentee
```

**Exemple concret** :
```
Notre entreprise (SaaS B2B, 50 employes, 5M EUR ARR) doit choisir entre :
A) Recruter 3 commerciaux supplementaires
B) Investir dans un outil d'outbound automatise + 1 commercial
C) Augmenter le budget marketing inbound de 50%

Analyse etape par etape :
1. Quel est le cout de chaque option sur 12 mois ?
2. Quel est le revenu additionnel attendu pour chaque option ?
3. Quel est le delai avant de voir les premiers resultats ?
4. Quels sont les risques de chaque option ?
5. Quelle option recommandes-tu et pourquoi ?
```

---

## 2. Templates de Prompts par Cas d'Usage

### 2.1 Redaction d'Emails

**Email professionnel generique** :
```
Redige un email professionnel avec les parametres suivants :
- Destinataire : [NOM, ROLE]
- Objet : [SUJET]
- Objectif : [ce que je veux obtenir]
- Ton : [formel / professionnel / amical / direct]
- Contexte : [relation avec le destinataire, historique]
- Longueur : maximum [N] lignes
- Call-to-action : [ce que le destinataire doit faire]
```

**Email de relance** :
```
Redige un email de relance pour [NOM] qui n'a pas repondu depuis [DUREE].
Contexte initial : [rappeler l'objet de l'email precedent].
Ton : professionnel et persistant sans etre agressif.
Ajoute une valeur supplementaire (information, proposition, deadline).
Maximum 6 lignes. Termine par une question ouverte ou une proposition
de creneau.
```

**Email de refus diplomate** :
```
Redige un email pour decliner poliment [PROPOSITION/DEMANDE].
Raison du refus : [RAISON] (a formuler de maniere diplomate).
Ton : respectueux, appreciatif, et ouvert pour l'avenir.
Structure : remerciement, explication, alternative si possible, ouverture.
Maximum 8 lignes.
```

**Email d'annonce interne** :
```
Redige un email d'annonce interne pour communiquer [NOUVELLE/CHANGEMENT].
Audience : [toute l'entreprise / equipe specifique].
Ton : [enthousiaste / informatif / rassurant].
Structure : accroche, annonce principale, contexte/raisons, impact concret,
prochaines etapes, qui contacter pour les questions.
Maximum 15 lignes.
```

### 2.2 Resume de Documents

**Resume executif** :
```
Resume ce document en un executive summary de [N] lignes pour [AUDIENCE].
Structure : contexte (2 lignes), points cles (3-5 bullet points),
implications/recommandations (2-3 lignes).
Mets en evidence les chiffres cles et les decisions a prendre.
[COLLER LE DOCUMENT]
```

**Resume de rapport long** :
```
Resume ce rapport de [N] pages en une synthese de 1 page.
Pour chaque section du rapport, extrais :
- Le point cle (1 phrase)
- Le chiffre ou la donnee la plus importante
- L'implication pour notre organisation
Termine par les 3 actions prioritaires recommandees.
[COLLER LE RAPPORT]
```

**Resume de fil de discussion** :
```
Resume ce fil de [N] messages en identifiant :
1. Le sujet principal et le contexte
2. Les positions des differents participants
3. Les decisions prises (avec qui a decide)
4. Les points de desaccord non resolus
5. Les actions a suivre (qui, quoi, quand)
6. La tonalite generale (consensus, tension, blocage)
[COLLER LE FIL DE DISCUSSION]
```

### 2.3 Analyse de Donnees

**Analyse exploratoire** :
```
Analyse le tableau de donnees suivant et identifie :
1. Les 5 tendances principales
2. Les anomalies ou valeurs aberrantes
3. Les correlations entre les variables
4. 3 hypotheses explicatives pour les tendances observees
5. 3 recommandations actionnables basees sur l'analyse
Presente les resultats dans un format structure avec des tableaux resumes.
[COLLER LES DONNEES]
```

**Comparaison** :
```
Compare les deux ensembles de donnees suivants et identifie :
1. Les differences significatives
2. Les points communs
3. L'evolution entre les deux periodes
4. Les elements qui necessitent une attention particuliere
Presente la comparaison dans un tableau avant/apres avec variation en %.
[COLLER LES DEUX ENSEMBLES]
```

### 2.4 Preparation de Reunions

**Briefing pre-reunion** :
```
Prepare un briefing pour la reunion suivante :
- Sujet : [SUJET]
- Participants : [LISTE]
- Objectif : [DECISIONS A PRENDRE / INFORMATIONS A PARTAGER]
- Documents de reference : [LISTE DES DOCUMENTS]

Produis :
1. Contexte et enjeux (5 lignes)
2. Points cles a discuter (liste)
3. Questions a poser (par participant si pertinent)
4. Objections ou risques anticipes
5. Proposition de decision / conclusion souhaitee
```

**Ordre du jour structure** :
```
Cree un ordre du jour structure pour une reunion de [DUREE] sur [SUJET].
Participants : [LISTE avec roles].
Objectifs : [3 objectifs de la reunion].
Structure : introduction (5min), [sujets avec durees], next steps (5min).
Pour chaque sujet : titre, objectif, presentateur, duree, decision attendue.
```

### 2.5 Brainstorming

**Brainstorming structure** :
```
Je travaille sur [PROBLEME/OPPORTUNITE]. Aide-moi a brainstormer
en suivant cette structure :
1. Reformule le probleme de 3 manieres differentes
2. Propose 10 idees (du conventionnel au radical)
3. Pour les 3 meilleures idees, developpe :
   - Description detaillee (3 lignes)
   - Avantages et risques
   - Effort de mise en oeuvre (faible/moyen/eleve)
   - Premier pas concret pour tester l'idee
```

**Challenge d'idee** :
```
Voici mon idee / ma proposition : [DESCRIPTION].
Joue le role de l'avocat du diable et :
1. Identifie les 5 principales faiblesses de cette idee
2. Pour chaque faiblesse, propose une solution ou une mitigation
3. Identifie les 3 risques que je n'ai probablement pas anticipes
4. Donne un score de viabilite de 1 a 10 avec justification
5. Reformule l'idee en la renforceant avec tes suggestions
```

---

## 3. Chaines de Prompts pour Taches Complexes

### Principe

Les taches complexes ne peuvent pas etre realisees en un seul prompt. La technique des chaines de prompts (prompt chaining) consiste a decomposer une tache en etapes sequentielles, ou la sortie d'un prompt alimente le prompt suivant.

### Chaine : Redaction de rapport complet

**Etape 1 — Structure** :
```
Je dois rediger un rapport sur [SUJET] pour [AUDIENCE].
Propose un plan detaille en 5-7 sections avec les sous-sections,
les points cles a couvrir dans chaque section, et les donnees
a inclure. Format : plan hierarchique (1., 1.1, 1.2, 2., etc.)
```

**Etape 2 — Recherche et contenu** :
```
A partir du plan ci-dessus, redige la section [N] en detail.
Inclus des donnees chiffrees, des exemples concrets, et des
references. Longueur : [N] mots. Ton : [TON].
```
(Repeter pour chaque section)

**Etape 3 — Synthese** :
```
Voici les sections redigees du rapport [coller].
Redige maintenant l'introduction (accroche, contexte, objectif du rapport)
et la conclusion (synthese, recommandations cles, prochaines etapes).
Assure la coherence de ton et de style entre toutes les sections.
```

**Etape 4 — Relecture et amelioration** :
```
Relis le rapport complet et :
1. Verifie la coherence des chiffres et des donnees
2. Identifie les repetitions a supprimer
3. Ameliore les transitions entre sections
4. Ajoute un executive summary de 10 lignes au debut
5. Propose un titre percutant
```

### Chaine : Analyse strategique complete

**Etape 1** : "Fais une analyse PESTEL du marche [X] en 2026"
**Etape 2** : "A partir de l'analyse PESTEL, identifie les 5 forces de Porter pour notre position"
**Etape 3** : "Avec PESTEL + Porter, realise un SWOT de notre entreprise sur ce marche"
**Etape 4** : "A partir du SWOT, propose 3 options strategiques avec avantages/risques/investissement"
**Etape 5** : "Recommande l'option optimale et propose un plan d'implementation en 5 phases"

### Chaine : Preparation d'une presentation importante

**Etape 1** : "Voici le contexte [coller]. Identifie les 5 messages cles que je dois transmettre"
**Etape 2** : "Pour chaque message cle, propose un slide avec titre, 3 bullet points, et un visuel"
**Etape 3** : "Redige les speaker notes pour chaque slide (ce que je dois dire, pas ce qui est ecrit)"
**Etape 4** : "Anticipe les 10 questions les plus probables de l'audience et prepare les reponses"
**Etape 5** : "Resume le pitch en 2 minutes pour le cas ou je dois raccourcir"

---

## 4. IA pour la Redaction

### Blog posts et articles

```
Redige un article de blog de [N] mots sur [SUJET].
Audience : [AUDIENCE].
Objectif : [informer / persuader / eduquer / divertir].
Structure : titre accrocheur, introduction (hook + contexte), [N] sections
avec sous-titres, conclusion avec call-to-action.
Ton : [expert mais accessible / conversationnel / formel].
SEO : integre naturellement les mots-cles [LISTE].
Inclus [N] exemples concrets et [N] donnees chiffrees.
```

### Rapports professionnels

```
Redige un rapport professionnel sur [SUJET] pour [AUDIENCE].
Donnees source : [COLLER ou REFERENCER].
Structure standard :
1. Page de garde (titre, auteur, date, version)
2. Executive summary (10 lignes)
3. Introduction et contexte
4. Methodologie (si applicable)
5. Analyse et resultats
6. Recommandations (tableau : action, priorite, responsable, deadline)
7. Annexes (si necessaire)
Ton : objectif, base sur les donnees, oriente decision.
Longueur : [N] pages.
```

### Propositions commerciales

```
Redige une proposition commerciale pour [CLIENT] sur [SERVICE/PRODUIT].
Contexte client : [SITUATION, BESOIN, ENJEUX].
Notre proposition : [DESCRIPTION DU SERVICE/PRODUIT].
Structure :
1. Comprendre votre enjeu (reformulation du besoin client)
2. Notre approche (methodologie, differenciateurs)
3. Livrables et planning (tableau)
4. Equipe mobilisee (profils et expertises)
5. Investissement (tarification, conditions)
6. References similaires (2-3 cas clients)
7. Prochaines etapes
Ton : professionnel, client-centrique, sans survente.
```

---

## 5. IA pour l'Analyse de Donnees

### Analyse en langage naturel

La puissance de l'IA pour l'analyse de donnees reside dans sa capacite a transformer des questions en langage naturel en insights actionnables. Il n'est plus necessaire de maitriser SQL, Python, ou les formules avancees pour explorer des donnees.

**Questions types pour l'analyse** :
```
Voici un tableau de donnees [COLLER].

Reponds aux questions suivantes :
1. Quelles sont les 3 tendances les plus significatives ?
2. Y a-t-il des correlations entre [VARIABLE A] et [VARIABLE B] ?
3. Quels sont les outliers et comment les expliquer ?
4. Si la tendance actuelle continue, quelle est la projection pour les 6 prochains mois ?
5. Quelles actions recommandes-tu basees sur ces donnees ?

Presente les reponses avec des tableaux et des recommandations concretes.
Indique le niveau de confiance de chaque conclusion (eleve, moyen, faible).
```

### Nettoyage et preparation de donnees

```
Voici un jeu de donnees brut [COLLER].
Nettoie les donnees :
1. Identifie et signale les valeurs manquantes
2. Detecte les doublons
3. Standardise les formats (dates, noms, montants)
4. Signale les incoherences (ex: age negatif, montant aberrant)
5. Propose un schema de donnees nettoyees
Presente un rapport de nettoyage avec les actions effectuees.
```

### Visualisation et reporting

```
A partir des donnees suivantes [COLLER], recommande :
1. Les 3 visualisations les plus pertinentes (type de graphique + variables)
2. Le message cle de chaque visualisation (ce que le lecteur doit retenir)
3. La mise en page optimale pour un dashboard d'une page
4. Les KPIs a mettre en evidence (avec valeurs actuelles et cibles)
Decris chaque visualisation en detail (axes, couleurs, legende, titre).
```

---

## 6. IA pour la Communication

### Ajustement de ton

L'IA excelle pour adapter le ton d'un message a differentes audiences et contextes :

```
Voici un message [COLLER].
Reecris ce message en 4 versions :
1. Version formelle (pour le conseil d'administration)
2. Version accessible (pour toute l'entreprise)
3. Version technique (pour l'equipe d'ingenieurs)
4. Version client (pour une communication externe)
Pour chaque version, conserve le message de fond mais adapte le vocabulaire,
le ton, et le niveau de detail.
```

### Traduction contextuelle

```
Traduis le texte suivant de [LANGUE SOURCE] vers [LANGUE CIBLE].
Contexte : [TYPE DE DOCUMENT / AUDIENCE / SECTEUR].
Consignes :
- Conserve le ton [formel / technique / conversationnel]
- Adapte les expressions idiomatiques (ne pas traduire literalement)
- Conserve les termes techniques en anglais si c'est la convention du secteur
- Signale les passages ou plusieurs traductions sont possibles
[COLLER LE TEXTE]
```

### Simplification

```
Simplifie le texte suivant pour un public [NON TECHNIQUE / GRAND PUBLIC / DEBUTANT].
Regles :
- Remplace le jargon par des termes courants
- Utilise des phrases courtes (max 20 mots)
- Ajoute une analogie ou un exemple pour chaque concept complexe
- Niveau de lecture cible : [college / lycee / universite]
- Longueur : [meme longueur / plus court / plus detaille]
[COLLER LE TEXTE]
```

---

## 7. Construction d'une Bibliotheque de Prompts

### Architecture de la bibliotheque

Une bibliotheque de prompts efficace est organisee par categorie et par metier :

```
📁 Bibliotheque de Prompts
├── 📁 Communication
│   ├── Email — reponse formelle
│   ├── Email — relance commerciale
│   ├── Email — annonce interne
│   ├── Email — refus diplomatique
│   └── Email — felicitations
├── 📁 Redaction
│   ├── Rapport — executive summary
│   ├── Rapport — complet
│   ├── Compte-rendu de reunion
│   ├── Article de blog
│   └── Proposition commerciale
├── 📁 Analyse
│   ├── Analyse de donnees exploratoire
│   ├── Comparaison avant/apres
│   ├── SWOT
│   └── Analyse de risques
├── 📁 Reunion
│   ├── Briefing pre-reunion
│   ├── Ordre du jour
│   ├── Compte-rendu
│   └── Suivi post-reunion
├── 📁 Brainstorming
│   ├── Generation d'idees
│   ├── Challenge d'idee
│   └── Decision multi-criteres
└── 📁 Metier-specifique
    ├── [Prompts specifiques au metier]
    └── [Prompts specifiques au secteur]
```

### Bonnes pratiques de gestion

- **Stockage** : Google Doc partage, Notion, ou Custom GPT / Claude Project dedie
- **Naming convention** : [Categorie] — [Action] — [Precision] (ex: "Email — Relance — Client inactif")
- **Parametrisation** : Utiliser des placeholders [VARIABLE] pour rendre les prompts reutilisables
- **Versioning** : Dater chaque prompt et noter les ameliorations (v1, v2, v3)
- **Feedback** : Annoter les prompts avec leur efficacite (note 1-5) et les contextes ou ils fonctionnent le mieux
- **Partage** : Publier les meilleurs prompts dans un canal dedie (Teams, Slack) pour capitalisation organisationnelle

### Maintenance

| Cadence | Action |
|---------|--------|
| **Hebdomadaire** | Ajouter les nouveaux prompts utilises dans la semaine |
| **Mensuel** | Revoir et ameliorer les 5 prompts les plus utilises |
| **Trimestriel** | Archiver les prompts obsoletes, tester les prompts avec les nouveaux modeles |
| **Annuel** | Restructurer la bibliotheque, former les nouveaux employes |

---

## 8. Automatisation de Workflows IA

### N8N + IA

N8N est une plateforme d'automatisation open-source qui s'integre nativement avec les APIs d'IA (OpenAI, Anthropic, Google AI).

**Workflow type : Veille concurrentielle automatisee**
1. **Trigger** : Cron (tous les lundis 8h)
2. **Scraping** : Collecter les articles de presse et posts LinkedIn des concurrents (via RSS, scraping, ou Google Alerts API)
3. **IA** : Envoyer le contenu collecte a Claude/GPT pour synthese ("Resume les 5 actualites concurrentielles les plus importantes de la semaine avec implications pour notre strategie")
4. **Formatage** : Formatter le resume en HTML/Markdown
5. **Distribution** : Envoyer par email ou poster dans un canal Slack/Teams

**Workflow type : Traitement automatique de feedback client**
1. **Trigger** : Nouveau feedback recu (formulaire, NPS, avis Google)
2. **IA** : Classifier le sentiment (positif, neutre, negatif) et extraire les themes
3. **Routing** : Acheminer les feedbacks negatifs au support, les positifs au marketing
4. **IA** : Generer une reponse personnalisee pour les feedbacks negatifs
5. **Notification** : Alerter le manager si le sentiment moyen baisse sous le seuil

**Workflow type : Generation de rapports hebdomadaires**
1. **Trigger** : Cron (vendredi 17h)
2. **Data** : Collecter les donnees de la semaine (CRM, Google Analytics, base de donnees)
3. **IA** : Generer l'analyse et les insights ("Analyse ces donnees hebdomadaires et identifie les 3 faits marquants, les 2 risques, et les 2 opportunites")
4. **Formatage** : Creer un rapport structure (HTML ou Google Docs)
5. **Distribution** : Envoyer au COMEX et archiver dans Google Drive

### Make (ex-Integromat) + IA

Make offre une interface visuelle pour construire des workflows complexes avec des modules IA :

**Cas d'usage courants** :
- Transcription automatique d'enregistrements audio → resume IA → email aux participants
- Nouveau lead CRM → enrichissement IA (analyse du profil, scoring, email personalise)
- Ticket support → classification IA → reponse pre-redigee → assignation agent
- Nouvelle publication blog → adaptation IA pour chaque reseau social → publication automatique

### Power Automate + IA (Microsoft)

Power Automate s'integre nativement avec M365 Copilot et les AI Builder de Microsoft :

**Workflows M365 + IA** :
- Nouvel email avec piece jointe → extraction IA des informations cles → mise a jour Dataverse
- Nouvelle reunion Teams terminee → resume Copilot → email de suivi automatique aux participants
- Nouveau document SharePoint → classification IA (type, sensibilite, departement) → routing
- Formulaire soumis → analyse IA du contenu → assignation automatique → notification

### Comparaison des plateformes d'automatisation

| Critere | N8N | Make | Power Automate |
|---------|-----|------|----------------|
| **Open source** | Oui | Non | Non |
| **Self-hosted** | Oui | Non | Non (cloud Microsoft) |
| **Integration IA** | API directe (OpenAI, Anthropic, etc.) | Modules IA pre-integres | AI Builder + Copilot natif |
| **Ecosysteme** | Universel (APIs, webhooks) | Universel (1000+ apps) | Microsoft 365 native |
| **Complexite** | Moyenne-elevee (technique) | Faible-moyenne (visuel) | Faible (pour M365) |
| **Cout** | Gratuit (self-hosted) ou cloud abordable | Freemium, plans a partir de 9 EUR/mois | Inclus dans certaines licences M365 |
| **Ideal pour** | Developpeurs, workflows complexes, on-premise | PME, workflows multi-apps, marketing | Organisations Microsoft, workflows Office |

---

## 9. Custom GPTs et Claude Projects

### Custom GPTs (OpenAI)

Les Custom GPTs permettent de creer des assistants specialises avec des instructions systeme, des fichiers de reference, et des actions (appels API).

**Architecture d'un Custom GPT** :
- **Instructions** : Le prompt systeme qui definit le comportement, le role, les contraintes, et le format de reponse
- **Knowledge** : Les fichiers uploades que le GPT peut consulter (manuels, templates, donnees de reference)
- **Actions** : Les APIs externes que le GPT peut appeler (CRM, base de donnees, outils internes)
- **Conversation starters** : Les exemples de questions pour guider l'utilisateur

**Exemples de Custom GPTs productivite** :
- **Redacteur de comptes-rendus** : Instructions sur le format de CR de l'entreprise, templates en knowledge, style guide
- **Analyste de donnees** : Instructions sur les KPIs de l'entreprise, definitions metier, templates de rapports
- **Coach de presentation** : Instructions sur les bonnes pratiques de presentation, style guide, exemples de slides
- **FAQ interne** : Tous les documents de politique interne en knowledge, instructions pour repondre de maniere precise et citee

### Claude Projects (Anthropic)

Claude Projects offre une approche similaire avec des specificites :

**Architecture d'un Claude Project** :
- **Custom Instructions** : Instructions systeme persistantes qui s'appliquent a chaque conversation dans le projet
- **Knowledge Base** : Fichiers uploades qui servent de contexte permanent (PDFs, documents, code, donnees)
- **Conversations** : Chaque conversation dans le projet herite des instructions et de la knowledge base

**Avantages de Claude Projects** :
- Fenetre de contexte tres large (200K+ tokens dans Claude 3.5/4)
- Instructions custom detaillees et respectees avec precision
- Knowledge base consultable en contexte (pas un simple RAG — le modele peut raisonner sur les documents)
- Pas de limite de fichiers (dans les limites du plan)
- MCP (Model Context Protocol) pour connecter Claude a des outils externes

**Exemples de Claude Projects productivite** :
- **Strategie d'entreprise** : Business plan, rapports annuels, analyses marche en knowledge, instructions pour raisonner de maniere strategique
- **Redaction technique** : Style guide, glossaire, templates en knowledge, instructions pour respecter les conventions
- **Analyse juridique** : Contrats, textes de loi, jurisprudence en knowledge, instructions pour analyser avec precision et citer les sources
- **Assistant de projet** : Plan de projet, RACI, documents de specification en knowledge, instructions pour suivre l'avancement et identifier les risques

### Custom GPT vs Claude Project — Comparaison

| Critere | Custom GPT | Claude Project |
|---------|-----------|----------------|
| **Instructions systeme** | 8 000 caracteres max | Plus flexibles, pas de limite stricte |
| **Knowledge base** | 20 fichiers max, taille limitee | Genereux, fichiers volumineux supportes |
| **Actions / Tool use** | Actions (appels API, OpenAPI) | MCP (Model Context Protocol) |
| **Partage** | Publique, lien, ou GPT Store | Partage au sein d'un workspace |
| **Precision des instructions** | Bonne | Excellente (Claude suit les instructions avec precision) |
| **Cas d'usage ideal** | Assistants publics, workflows simples | Assistants internes, analyse approfondie |

---

## 10. Bonnes Pratiques Transversales

### Les 10 regles d'or du prompting productif

1. **Commencer par le resultat souhaite** : Decrire d'abord le format de sortie, puis le contenu. "Produis un tableau avec 3 colonnes : risque, probabilite, impact" avant de decrire les donnees
2. **Etre specifique** : "Resume en 5 bullet points de 2 lignes" est 10x meilleur que "Resume"
3. **Fournir du contexte** : Plus l'IA comprend la situation, meilleur est le resultat
4. **Utiliser des exemples** : Un exemple vaut mille mots de description
5. **Iterer** : Ne jamais accepter le premier resultat sans affinage
6. **Decomposer** : Les taches complexes doivent etre decomposees en etapes
7. **Definir les contraintes** : Longueur, ton, audience, exclusions, format
8. **Verifier** : Toujours verifier les faits, les chiffres, et la logique
9. **Capitaliser** : Sauvegarder les bons prompts pour reutilisation
10. **Experimenter** : Tester differentes formulations pour le meme besoin

### Erreurs courantes a eviter

- Ecrire des prompts de 1 ligne et s'attendre a des resultats exceptionnels
- Ne pas preciser l'audience ni le format de sortie
- Copier-coller la sortie IA sans la relire ni la personnaliser
- Utiliser le meme prompt pour des audiences et des contextes differents
- Ne pas sauvegarder les prompts efficaces pour reutilisation
- Oublier de mentionner ce que l'IA ne doit PAS faire (exclusions)
- Faire confiance aux chiffres et aux sources generees par l'IA sans verification
- Utiliser l'IA pour des taches qu'elle ne fait pas bien (jugement ethique, decisions critiques, creativite pure)

---

## 11. Mesure d'Efficacite des Prompts

### Framework d'evaluation

| Critere | Description | Score (1-5) |
|---------|-------------|-------------|
| **Pertinence** | Le resultat repond-il a la question posee ? | ___ |
| **Precision** | Les faits, chiffres et details sont-ils corrects ? | ___ |
| **Completude** | Tous les aspects demandes sont-ils couverts ? | ___ |
| **Format** | Le format de sortie est-il conforme a la demande ? | ___ |
| **Utilisabilite** | Le resultat est-il directement utilisable sans modification majeure ? | ___ |
| **Efficacite** | Le temps total (prompting + revision) est-il inferieur au temps manuel ? | ___ |

### Metriques d'efficacite

- **Temps de premier brouillon** : Temps pour obtenir un premier brouillon utilisable (prompt + generation)
- **Taux d'acceptation** : % du contenu IA utilise tel quel (sans modification)
- **Nombre d'iterations** : Combien de cycles prompt-revision avant le resultat final
- **Temps total** : Temps prompt + generation + revision vs temps de production manuelle
- **Gain net** : Temps manuel - temps avec IA = gain net en minutes

### Objectifs par niveau

| Niveau | Taux d'acceptation | Iterations | Gain net |
|--------|-------------------|------------|----------|
| **Debutant** | 20-30% | 4-6 | 10-20% |
| **Intermediaire** | 40-60% | 2-4 | 30-50% |
| **Avance** | 60-80% | 1-2 | 50-70% |
| **Expert** | 80-95% | 1 | 70-90% |
