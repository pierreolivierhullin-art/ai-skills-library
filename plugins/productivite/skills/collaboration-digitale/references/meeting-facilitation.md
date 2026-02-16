# Reunions & Facilitation — Formats, Preparation, Animation, Suivi & Outils

## Overview

Ce document de reference couvre l'ensemble des pratiques de gestion de reunions et de facilitation : types et formats de reunions (standup, review, brainstorm, decision, 1:1), preparation (agenda, pre-read, roles), techniques de facilitation (timeboxing, round robin, silent brainstorm, dot voting), comptes-rendus et suivi des actions, bonnes pratiques de visioconference (Zoom, Teams, Meet), defis specifiques des reunions hybrides, assistants IA de reunion (Otter.ai, Fireflies, Granola, Copilot), analytics de reunions et reduction du nombre de reunions. La reunion est l'outil de collaboration le plus utilise et le plus mal utilise dans les organisations. Ce guide vise a transformer chaque reunion en un moment de decision et d'alignement productif, et a eliminer celles qui ne le sont pas.

---

## PARTIE 1 — Types et Formats de Reunions

### Taxonomie des Reunions

Chaque reunion doit avoir un type clairement identifie qui determine son format, sa duree, et ses regles. Melanger les types dans une meme reunion (informer ET decider ET brainstormer) est le premier anti-pattern a eliminer.

#### 1. Standup / Daily Sync
- **Objectif** : synchroniser l'equipe sur l'avancement quotidien, identifier les blocages.
- **Format** : chaque participant repond a 3 questions (Hier, Aujourd'hui, Blocages). Pas de discussion — les sujets qui necessitent un debat sont notes et traites apres le standup.
- **Duree** : 15 minutes maximum. Si l'equipe depasse regulierement 15 minutes, elle est trop grande ou le format est mal respecte.
- **Participants** : equipe operationnelle (5-9 personnes ideal). Au-dela de 12, passer au standup async.
- **Frequence** : quotidien (ou 3x/semaine si l'equipe est mature en async).
- **Recommandation async** : pour les equipes distribuees, le standup async (bot ou post structure) est systematiquement plus efficace que le standup synchrone.

#### 2. Weekly Team Meeting
- **Objectif** : aligner l'equipe sur la semaine a venir, partager les informations importantes, traiter les sujets transverses.
- **Format** : agenda fixe avec des sections recurrentes (actualites, revue des metriques, sujets de la semaine, actions). Le manager anime, un note-taker documente.
- **Duree** : 25 ou 50 minutes. Jamais 60 minutes — laisser une pause de 5-10 minutes avant le prochain meeting.
- **Participants** : l'equipe complete (max 10-12 personnes).
- **Frequence** : hebdomadaire, meme jour et meme heure chaque semaine.
- **Recommandation** : consacrer 50% du temps aux sujets de decision, pas aux mises a jour de statut (qui doivent etre async).

#### 3. Brainstorming / Ideation
- **Objectif** : generer un maximum d'idees sur un sujet, explorer des solutions, penser de maniere creative.
- **Format** : facilite par un animateur. Commence par une divergence (generation d'idees sans jugement) puis converge (regroupement, priorisation, selection).
- **Duree** : 45-90 minutes selon la complexite. Inclure des pauses si > 60 minutes.
- **Participants** : 4-8 personnes. Diversite de profils essentielle (pas uniquement des experts du domaine).
- **Frequence** : ponctuel, selon les besoins.
- **Recommandation** : utiliser un outil de collaboration visuelle (Miro, FigJam) et des techniques de contribution ecrite (silent brainstorm) pour eviter la domination des extrovertis.

#### 4. Decision Meeting
- **Objectif** : prendre une decision specifique sur un sujet prepare a l'avance. Une reunion de decision produit une decision — pas un "on y reflechit".
- **Format** : pre-read distribue 48h avant avec le contexte, les options, et les analyses. La reunion commence par 5 minutes de relecture silencieuse (pour ceux qui n'ont pas lu), puis discussion structuree des options, puis decision.
- **Duree** : 25-50 minutes. Si la decision ne peut pas etre prise en 50 minutes, c'est que le sujet n'est pas assez prepare.
- **Participants** : le decision maker + les 3-5 personnes dont l'input est essentiel. Pas de spectateurs. Appliquer la regle de Jeff Bezos : "two-pizza team" (max 6-8 personnes).
- **Frequence** : ponctuel.
- **Recommandation** : documenter la decision dans le channel ou le document dedie IMMEDIATEMENT apres la reunion. Un delai de documentation est un risque de perte de decision.

#### 5. Review / Demo
- **Objectif** : presenter le travail accompli a des parties prenantes pour recueillir du feedback.
- **Format** : presentation ou demonstration suivie d'une session de Q&A et de feedback. Le presentateur montre le travail, pas des slides sur le travail.
- **Duree** : 25-50 minutes (dont 50% pour le feedback).
- **Participants** : l'equipe qui a fait le travail + les parties prenantes qui vont donner du feedback (manager, client interne, utilisateurs).
- **Frequence** : a chaque jalon, fin de sprint, ou fin de phase.
- **Recommandation** : enregistrer la demo pour les absents. Envoyer un Loom si le public est large et que le feedback peut etre async.

#### 6. One-on-One (1:1)
- **Objectif** : maintenir la relation manager-collaborateur, discuter du developpement, des preoccupations, et du feedback.
- **Format** : conversation ouverte guidee par un agenda collaboratif (le collaborateur et le manager ajoutent des points). Ce n'est PAS une reunion de reporting (les mises a jour de statut sont async).
- **Duree** : 25-50 minutes.
- **Participants** : 2 personnes (manager + collaborateur).
- **Frequence** : hebdomadaire (non negociable pour les equipes distantes). Bimensuel acceptable pour les equipes co-localisees matures.
- **Recommandation** : ne jamais annuler un 1:1 sauf urgence absolue. C'est le signal le plus fort qu'un manager envoie sur l'importance qu'il accorde a la relation. Le 1:1 appartient au collaborateur — c'est son temps pour aborder les sujets qui comptent pour lui.

#### 7. Retrospective
- **Objectif** : analyser collectivement ce qui a bien fonctionne et ce qui peut etre ameliore.
- **Format** : facilite, utilisant un framework structure (Start/Stop/Continue, 4L, Sailboat, etc.). Contribution individuelle ecrite puis discussion en groupe.
- **Duree** : 45-60 minutes.
- **Participants** : l'equipe (5-10 personnes).
- **Frequence** : toutes les 2 semaines (fin de sprint) ou mensuel.
- **Recommandation** : varier les formats de retrospective pour eviter la lassitude. Assigner un responsable pour chaque action decidee en retro. Revoir les actions de la retro precedente au debut de chaque retro.

#### 8. All-Hands / Town Hall
- **Objectif** : communiquer les informations strategiques a l'ensemble de l'organisation, creer un sentiment d'unite.
- **Format** : presentation de la direction (20-30 min) suivie d'un Q&A ouvert (15-20 min). Le Q&A est essentiel — un all-hands sans Q&A est un webinaire.
- **Duree** : 45-60 minutes.
- **Participants** : toute l'organisation (ou une division).
- **Frequence** : mensuel ou trimestriel.
- **Recommandation** : collecter les questions a l'avance via un formulaire anonyme. Enregistrer et partager pour les absents. Utiliser le Q&A structure de Teams Town Hall ou de Slido pour gerer les questions en temps reel.

---

## PARTIE 2 — Preparation des Reunions

### L'Agenda : Non Negociable

Pas d'agenda, pas de reunion. Cette regle est absolue et non negociable. Un agenda distribue a l'avance est le premier indicateur d'une reunion professionnelle.

#### Structure d'un Agenda Efficace

```
REUNION : [Titre descriptif]
Date : [Date] | Heure : [Heure] (avec fuseau horaire)
Duree : [25 ou 50 min]
Animateur : [Nom]
Note-taker : [Nom]
Objectif : [Pourquoi cette reunion existe — en une phrase]

AGENDA :
1. [Sujet 1] — [Duree] — [Objectif : Information / Discussion / Decision]
   Owner : [Nom]
2. [Sujet 2] — [Duree] — [Objectif]
   Owner : [Nom]
3. [Sujet 3] — [Duree] — [Objectif]
   Owner : [Nom]
4. Prochaines etapes et actions — 5 min

PRE-READ :
- [Lien vers le document / Loom / donnees a lire AVANT la reunion]
- Temps de lecture estime : [X minutes]

DECISION ATTENDUE :
- [Quelle decision sera prise dans cette reunion]
```

#### Recommandations

- **Maximum 3 sujets par reunion** : au-dela, les sujets sont survoles ou la reunion deborde. Prioriser les 3 sujets les plus importants, reporter les autres.
- **Chaque sujet a un objectif** : "Information" (pas de debat, juste du partage), "Discussion" (exploration, pas de decision attendue), ou "Decision" (une decision sera prise). Indiquer l'objectif dans l'agenda pour que les participants sachent ce qu'on attend d'eux.
- **Chaque sujet a un owner** : la personne qui presente le sujet et anime la discussion. Ce n'est pas toujours l'animateur de la reunion.
- **Le pre-read est obligatoire** : distribuer les documents de contexte au moins 24h avant. Si le pre-read n'est pas pret 24h avant, reporter la reunion.
- **La duree est respectee** : 25 minutes (pour les sujets simples) ou 50 minutes (pour les sujets complexes). Pas 30 ni 60 — les 5-10 minutes de battement permettent de souffler entre les reunions.

### Roles en Reunion

| Role | Responsabilites | Qui |
|---|---|---|
| **Animateur** | Introduit la reunion, gere l'agenda, distribue la parole, respecte le timing, synthetise | Designee a l'avance (souvent le manager ou le chef de projet) |
| **Note-taker** | Documente les decisions, les actions (qui/quoi/quand), et les points importants | Designee a l'avance (tourner le role chaque semaine) |
| **Time-keeper** | Surveille le temps et alerte l'animateur quand un sujet deborde | Designee a l'avance (peut etre le note-taker) |
| **Participants** | Contribuent au debat, partagent leurs perspectives, prennent des engagements | Tous les invites |
| **Decision maker** | Tranche en cas de desaccord (reunions de decision) | Designe dans l'agenda |

---

## PARTIE 3 — Techniques de Facilitation

### Timeboxing

Le timeboxing consiste a allouer un temps fixe a chaque activite et a le respecter strictement. C'est la technique la plus fondamentale du facilitateur.

#### Mise en oeuvre
- Annoncer le temps alloue AVANT de commencer l'activite : "Vous avez 5 minutes pour ecrire vos idees."
- Utiliser un timer visible (timer Miro, timer Teams, ou un simple chronometre partage a l'ecran).
- Alerter a mi-parcours et 1 minute avant la fin : "Il vous reste 2 minutes", "Derniere minute, finalisez votre derniere idee."
- Quand le temps est ecoule, passer a l'activite suivante. Ne pas etendre le temps sauf cas exceptionnel (et dans ce cas, reduire le temps d'une activite ulterieure pour compenser).

#### Durees Recommandees par Activite

| Activite | Duree recommandee |
|---|---|
| **Ice-breaker** | 3-5 min |
| **Brainstorming silencieux (sticky notes)** | 5-10 min |
| **Partage de sticky notes (1 par personne)** | 1-2 min par personne |
| **Regroupement / affinity diagram** | 10-15 min |
| **Discussion de groupe** | 10-15 min par sujet |
| **Dot voting** | 2-3 min |
| **Definition des actions** | 5-10 min |
| **Cloture / feedback** | 5 min |

### Round Robin

Le round robin garantit que chaque participant prend la parole au moins une fois. C'est la technique anti-domination par excellence.

#### Mise en oeuvre
- L'animateur donne la parole a chaque participant tour a tour, dans un ordre predefini (ordre alphabetique, ou dans l'ordre d'apparition a l'ecran en visio).
- Chaque participant a un temps identique (1-2 minutes selon le nombre de participants).
- "Passer" est autorise si le participant n'a rien a ajouter, mais l'animateur revient vers lui a la fin pour verifier.
- Utiliser le round robin pour les sujets sensibles ou les introvertis risquent de se taire et les extrovertis de dominer.

### Silent Brainstorm (Brainwriting)

Le silent brainstorm est la technique la plus puissante pour generer des idees de qualite en evitant les biais de groupe (conformisme, ancrage, domination).

#### Mise en oeuvre
1. L'animateur pose la question de brainstorming clairement (ecrite sur le board ou a l'ecran).
2. Chaque participant ecrit ses idees INDIVIDUELLEMENT et EN SILENCE sur des sticky notes (physiques ou digitaux). 1 idee = 1 sticky note.
3. Pas de discussion pendant cette phase. Pas de partage. Chacun reflechit seul.
4. Duree : 5-10 minutes (adapter selon la complexite du sujet).
5. Apres le temps ecoule, les participants partagent leurs idees (soit en les lisant tour a tour, soit en les postant tous simultanement sur le board).
6. La discussion ne commence qu'apres que TOUTES les idees ont ete partagees.

#### Pourquoi c'est superieur au brainstorming oral
- Les introvertis contribuent autant que les extrovertis.
- Les non-natifs de la langue ont le temps de formuler leurs idees.
- Pas d'effet d'ancrage (la premiere idee enoncee oralement influence toutes les suivantes).
- Plus d'idees generees (chaque participant produit ses propres idees sans etre interrompu).
- Les idees sont evaluees sur leur merite, pas sur la confiance en soi de leur auteur.

### Dot Voting

Le dot voting est une technique de priorisation rapide et democratique. Chaque participant dispose d'un nombre fixe de votes qu'il distribue sur les options proposees.

#### Mise en oeuvre
1. Presenter toutes les options (idees, propositions, sujets) clairement.
2. Attribuer un nombre de votes par participant : regle generale = nombre d'options / 3, arrondi a l'entier superieur. Exemples : 10 options → 3-4 votes, 20 options → 6-7 votes.
3. Les participants votent simultanement (pas l'un apres l'autre, pour eviter l'influence).
4. Un participant peut mettre plusieurs votes sur la meme option s'il la considere prioritaire.
5. Compter les votes. Presenter le classement.
6. Discuter uniquement les 3-5 options les plus votees (pas toutes).

#### Variantes
- **Vote anonyme** : dans Miro ou FigJam, configurer le vote en mode anonyme pour eviter l'influence sociale.
- **Vote pondere** : certains participants ont plus de votes que d'autres (ex : le product owner a 5 votes, les developpeurs en ont 3).
- **Vote MoSCoW** : au lieu de dots, classer chaque option en Must, Should, Could, Won't.

### Fishbowl

Technique pour les discussions de groupe ou le nombre de participants est trop eleve pour une discussion libre.

#### Mise en oeuvre
1. Definir un "cercle interieur" de 4-5 chaises (virtuellement : 4-5 personnes avec le micro ouvert).
2. Les participants du cercle interieur discutent du sujet.
3. Les participants du cercle exterieur observent et ecoutent (micro coupe, pas de participation directe).
4. Quand un participant du cercle exterieur veut intervenir, il "prend la chaise vide" (dans un fishbowl ouvert) ou est invite par l'animateur (dans un fishbowl ferme).
5. Quand quelqu'un entre, quelqu'un doit sortir pour garder le nombre constant.

### ROTI (Return on Time Invested)

Technique rapide de feedback en fin de reunion pour evaluer si le temps a ete bien investi.

#### Mise en oeuvre
1. A la fin de la reunion, demander a chaque participant de noter la reunion de 1 a 5 :
   - 1 = temps completement perdu
   - 2 = peu de valeur, j'aurais pu ne pas etre la
   - 3 = correct, valeur egale au temps investi
   - 4 = bonne reunion, j'ai appris ou contribue utilement
   - 5 = excellente reunion, indispensable
2. Vote simultane (chacun leve le nombre de doigts correspondant, ou vote via un sondage).
3. Si la moyenne est inferieure a 3, discuter brievement de ce qui pourrait etre ameliore.
4. Tracker les scores ROTI au fil du temps pour mesurer l'evolution de la qualite des reunions.

---

## PARTIE 4 — Comptes-Rendus et Suivi des Actions

### Structure d'un Compte-Rendu

```
COMPTE-RENDU — [Titre de la reunion]
Date : [Date] | Duree effective : [XX min]
Participants : [Liste]
Absents excuses : [Liste]
Note-taker : [Nom]

DECISIONS PRISES :
1. [Decision 1] — Decidee par [Nom]
2. [Decision 2] — Decidee par [Nom]

ACTIONS :
| # | Action | Responsable | Echeance | Statut |
|---|--------|-------------|----------|--------|
| 1 | [Description de l'action] | [Nom] | [Date] | A faire |
| 2 | [Description de l'action] | [Nom] | [Date] | A faire |

POINTS DE DISCUSSION :
- [Resume du sujet 1 : positions exprimees, arguments cles]
- [Resume du sujet 2]

SUJETS REPORTES :
- [Sujet reporte a la prochaine reunion avec raison]
```

### Regles du Compte-Rendu

1. **Publie dans les 2 heures** : si le compte-rendu est partage 3 jours apres, la moitie de l'information est perdue et personne ne le lit.
2. **Decisions en gras** : les decisions doivent etre immediatement identifiables dans le compte-rendu. Ne pas les noyer dans le texte.
3. **Actions avec responsable ET echeance** : une action sans responsable ne sera pas faite. Une action sans echeance sera repoussee indefiniment.
4. **Poste dans le channel dedie** : le compte-rendu est partage dans le channel Teams/Slack de l'equipe ou du projet, pas envoye par email a chaque participant.
5. **Lie au document source** : si un pre-read ou un document a ete discute, lier le compte-rendu au document pour le contexte.

### Suivi des Actions

Le suivi des actions est le maillon faible de la plupart des reunions. Les actions sont decidees mais jamais suivies.

#### Systeme de Suivi Recommande

| Methode | Description | Ideal pour |
|---|---|---|
| **Liste dans le channel** | Poster les actions comme messages avec un emoji de statut (a faire / en cours / fait) | Equipes petites (3-6 personnes) |
| **Tableau dans Notion/Confluence** | Table structuree avec colonnes Action/Responsable/Echeance/Statut | Equipes moyennes (6-15 personnes) |
| **Outil de project management** | Creer des taches dans Jira, Asana, Linear, Trello | Equipes avec un workflow de taches existant |
| **Bot de suivi** | Bot Slack/Teams qui rappelle les actions non fermees | Equipes qui oublient les actions |

#### Revue des Actions

- Chaque reunion recurrente commence par une revue de 5 minutes des actions de la reunion precedente.
- Chaque action est revue : "Fait", "En cours (nouvelle echeance)", ou "Annule (avec justification)".
- Les actions non fermees depuis plus de 2 reunions sont un signal d'alerte : soit elles ne sont pas prioritaires (les annuler), soit il y a un blocage (le traiter).

---

## PARTIE 5 — Visioconference : Bonnes Pratiques

### Comparaison des Plateformes

| Critere | Zoom | Microsoft Teams | Google Meet |
|---|---|---|---|
| **Qualite video** | Excellente | Tres bonne (New Teams) | Bonne |
| **Qualite audio** | Excellente, noise suppression | Tres bonne, noise suppression | Bonne |
| **Breakout rooms** | Oui (robuste, jusqu'a 50 rooms) | Oui (jusqu'a 50 rooms) | Oui (basique) |
| **Enregistrement** | Cloud et local | Cloud (OneDrive/SharePoint) | Cloud (Google Drive) |
| **Transcription live** | Oui (multi-langues) | Oui (Copilot-powered) | Oui (anglais surtout) |
| **Virtual backgrounds** | Oui (vaste bibliotheque) | Oui | Oui (limite) |
| **Whiteboard integre** | Oui (Zoom Whiteboard) | Oui (Microsoft Whiteboard) | Oui (Jam) |
| **Capacite maximale** | 1 000 (meeting), 50 000 (webinar) | 1 000 (meeting), 20 000 (town hall) | 500 (meeting) |
| **Integration** | Standalone, integrations API | Microsoft 365 natif | Google Workspace natif |
| **IA** | Zoom AI Companion | Copilot | Gemini (2025) |
| **Prix** | Payant (plans Business) | Inclus dans Microsoft 365 | Inclus dans Google Workspace |

### Recommandations Techniques

#### Video
- **Camera allumee par defaut** : la video est essentielle pour la communication non-verbale et l'engagement. Encourager (pas imposer) les cameras allumees, surtout pour les reunions de moins de 10 personnes.
- **Cadrage** : visage centre dans le cadre, a hauteur des yeux. Pas de plongee (laptop sur les genoux) ni de contre-plongee (camera au plafond).
- **Arriere-plan** : arriere-plan reel neutre ou arriere-plan virtuel professionnel. Eviter les arriere-plans fantaisie en contexte professionnel.
- **Eclairage** : source de lumiere face au visage (fenetre ou lampe), jamais derriere (contre-jour).
- **Regard camera** : regarder la camera (pas l'ecran) quand on parle pour simuler le contact visuel. La webcam est "les yeux" de l'interlocuteur.

#### Audio
- **Casque avec micro** : toujours utiliser un casque avec micro integre ou un micro externe. Les hauts-parleurs du laptop creent de l'echo et captent le bruit ambiant.
- **Mute par defaut** : se mettre en mute quand on ne parle pas, surtout dans les reunions de plus de 5 personnes.
- **Environnement calme** : eviter les lieux bruyants (cafe, open space, rue). Si ce n'est pas possible, utiliser la suppression de bruit (Krisp, NVIDIA Broadcast, ou les filtres natifs de Zoom/Teams).
- **Test avant la reunion** : verifier le micro et les hauts-parleurs 2 minutes avant chaque reunion importante.

#### Etiquette
- **Ponctualite** : se connecter 1-2 minutes avant l'heure. Une reunion qui commence 5 minutes en retard parce que les participants arrivent au fil de l'eau est un manque de respect collectif.
- **Participation active** : eteindre les notifications, fermer les emails, ne pas travailler sur autre chose pendant la reunion. Si la reunion ne merite pas votre attention complete, vous ne devriez pas y etre.
- **Chat de la reunion** : utiliser le chat pour partager des liens, poser des questions non urgentes, et reagir sans interrompre. L'animateur doit surveiller le chat et integrer les questions.
- **Lever la main** : utiliser la fonctionnalite "lever la main" (raise hand) pour demander la parole sans interrompre. L'animateur gere la file d'attente.

---

## PARTIE 6 — Reunions Hybrides

### Le Defi Specifique des Reunions Hybrides

Les reunions hybrides (certains participants en salle, d'autres a distance) sont le format le plus difficile a reussir. Elles creent naturellement une asymetrie d'experience : les personnes en salle se voient, se parlent facilement, partagent le meme ecran — tandis que les participants distants sont reduits a une mosaique de visages sur un ecran mural, avec un micro de salle qui capte mal, et une camera qui montre l'ensemble de la salle sans distinction.

### Principes d'Equite Hybride

#### 1. Remote-First Meeting Design
Designer la reunion comme si tout le monde etait remote, meme si certains sont en salle. Cela signifie :
- Chaque participant en salle utilise aussi son laptop avec camera et micro individuels (pas seulement la camera de salle).
- Le chat de la reunion est le channel de communication parallele (pas les apartees en salle).
- Les documents sont partages a l'ecran, pas projetes sur un mur que les distants ne voient pas.

#### 2. Un Ecran, Un Visage
Dans la salle de reunion, chaque participant distant devrait etre visible individuellement (pas une vue en galerie minuscule). Si possible, utiliser un ecran dedie pour les participants distants, a hauteur des yeux des participants en salle, pour creer un semblant de contact visuel.

#### 3. Animateur Hybride
L'animateur a la responsabilite explicite d'inclure les participants distants :
- Solliciter les participants distants EN PREMIER sur chaque sujet (avant la discussion en salle).
- Verifier regulierement : "Est-ce que les participants en remote ont des questions ou des commentaires ?"
- Ne pas laisser les discussions de salle se derouler sans verifier que les distants entendent et comprennent.

#### 4. Equipement de Salle Adequat
L'equipement technique de la salle de reunion est critique :
- **Camera** : camera grand angle ou camera intelligente avec cadrage automatique (Owl Labs Meeting Owl, Poly Studio, Jabra Panacast) qui centre le cadrage sur la personne qui parle.
- **Microphone** : micro de table omni-directionnel de qualite (Jabra Speak, Poly Sync) ou microphones de plafond pour les grandes salles. Le micro du laptop ne suffit JAMAIS pour une salle.
- **Ecran** : ecran de grande taille (55" minimum) place a hauteur des yeux pour que les participants distants soient visibles.
- **Whiteboard capture** : si un tableau blanc physique est utilise, utiliser une camera dediee ou prendre des photos et les partager immediatement dans le chat.

### Anti-Patterns Hybrides

- **Conversation de salle non captee** : les participants en salle discutent entre eux a voix basse, les distants n'entendent rien et se sentent exclus.
- **Decision dans le couloir** : apres la reunion hybride, les participants en salle poursuivent la discussion dans le couloir et prennent des decisions que les distants decouvrent plus tard.
- **Partage d'ecran uniquement en salle** : projeter un document sur le mur de la salle sans le partager a l'ecran de la visio. Les distants voient une image floue d'un ecran filme par la camera de salle.
- **"Tu peux repeter ?"** : si les distants doivent regulierement demander de repeter, l'equipement audio est inadequat. Investir dans un micro de qualite AVANT la prochaine reunion.

---

## PARTIE 7 — Assistants IA de Reunion

### Panorama des Outils (2025-2026)

Les assistants IA de reunion transforment la gestion des reunions en automatisant la prise de notes, la generation de resumes, et l'identification des actions.

| Outil | Fonctionnalites principales | Integration | Prix |
|---|---|---|---|
| **Microsoft Copilot (Teams)** | Resume en temps reel, rattrapage intelligent, actions auto-identifiees, Q&A post-reunion | Microsoft Teams natif | Inclus dans Microsoft 365 Copilot (add-on) |
| **Otter.ai** | Transcription en temps reel, resume IA, identification des speakers, recherche dans les transcriptions | Zoom, Teams, Meet, standalone | Freemium / Plans payants |
| **Fireflies.ai** | Transcription, resume, topics auto-detectes, action items, analytics de reunions | Zoom, Teams, Meet, Webex | Freemium / Plans payants |
| **Granola** | Notes augmentees (combine notes manuelles et transcription IA pour generer un CR complet) | macOS, supporte Zoom/Teams/Meet | Freemium / Plans payants |
| **Fathom** | Resume et highlights, clips video des moments cles, integration CRM | Zoom, Teams, Meet | Gratuit (base), payant (avance) |
| **tl;dv** | Enregistrement, transcription, timestamps, clips partageables, resume IA | Zoom, Meet | Gratuit (base), payant (avance) |
| **Zoom AI Companion** | Resume, prochaines etapes, messages composes par IA dans le chat | Zoom natif | Inclus dans les plans payants |

### Comment Choisir un Assistant IA

```
L'organisation utilise-t-elle Microsoft Teams ?
├── OUI → Microsoft Copilot est le choix naturel (integration native)
│   └── Budget Copilot disponible ?
│       ├── OUI → Deployer Copilot dans Teams
│       └── NON → Evaluer Otter.ai ou Fireflies.ai (integrations Teams)
├── NON → L'organisation utilise-t-elle Zoom ?
│   ├── OUI → Zoom AI Companion (natif) ou Otter.ai / Fireflies.ai
│   └── NON → Google Meet ?
│       ├── OUI → Otter.ai, Fireflies.ai, ou tl;dv
│       └── NON → Evaluer les outils standalone (Otter.ai, Granola)
```

### Recommandations d'Usage

- **Transparence** : informer TOUS les participants que la reunion est enregistree et transcrite par un assistant IA. Obtenir le consentement explicite. Verifier la conformite RGPD.
- **Revue humaine** : ne pas publier les resumes IA sans revue humaine. L'IA peut se tromper sur les noms, les decisions, et les nuances. Le note-taker valide le resume avant publication.
- **Confidentialite** : verifier ou les donnees sont stockees (cloud du fournisseur, region de stockage). Certaines organisations interdisent les outils tiers pour les reunions confidentielles.
- **Ne pas tout enregistrer** : les 1:1 sensibles, les discussions disciplinaires, et les sujets confidentiels ne doivent PAS etre enregistres par un assistant IA, sauf accord explicite de toutes les parties.

---

## PARTIE 8 — Analytics de Reunions

### Pourquoi Mesurer les Reunions

Ce qui n'est pas mesure ne s'ameliore pas. Les metriques de reunion permettent d'identifier les problemes (trop de reunions, reunions trop longues, participants non pertinents) et de mesurer l'impact des ameliorations.

### Metriques Cles

| Metrique | Source | Cible | Signal d'alerte |
|---|---|---|---|
| **Heures en reunion par personne/semaine** | Analytics calendrier | < 10h | > 15h |
| **Nombre de reunions par jour** | Analytics calendrier | < 4 | > 6 |
| **% de reunions avec agenda** | Audit manuel ou outil | > 90% | < 50% |
| **Duree moyenne effective** | Outil IA ou suivi manuel | 80% du temps prevu | Reunions qui depassent systematiquement |
| **Taux de no-show** | Outil de visio (attendance report) | < 10% | > 20% |
| **Score ROTI moyen** | Sondage en fin de reunion | > 3.5/5 | < 3/5 |
| **% de reunions avec compte-rendu** | Audit dans le channel | > 80% | < 40% |
| **% d'actions fermees dans les delais** | Suivi des actions | > 70% | < 40% |
| **Blocs de deep work** (plages de 2h+ sans reunion) | Analytics calendrier | > 3 blocs/semaine | < 1 bloc/semaine |

### Outils d'Analytics

- **Clockwise** : analyse du calendrier, optimisation automatique des horaires, creation de blocs de focus time.
- **Reclaim.ai** : IA qui gere le calendrier, protege le deep work, et optimise les horaires de reunion.
- **Microsoft Viva Insights** : analytics de collaboration Microsoft 365 (temps en reunion, temps de focus, heures hors travail).
- **Google Workspace Insights** : rapports d'utilisation des outils Google (Meet, Calendar, Chat).

---

## PARTIE 9 — Annuler les Reunions Inutiles

### La Reunion la Plus Productive est Celle Qui n'a Pas Lieu

La reduction du nombre de reunions est l'un des leviers de productivite les plus puissants et les plus sous-exploites. Chaque reunion annulee libere du temps pour le travail profond, la reflexion, et la communication asynchrone de qualite.

### Criteres pour Annuler une Reunion

La reunion peut etre annulee si :
- **L'objectif peut etre atteint en async** : une mise a jour de statut, un partage d'information, un feedback sur un document — tout cela peut etre fait par un message, un Loom, ou un commentaire.
- **Le pre-read n'est pas pret** : si le document de preparation n'est pas disponible 24h avant, reporter. Une reunion sans preparation est une reunion improvisee, donc improductive.
- **Plus de 30% des participants essentiels sont absents** : reporter plutot que de reprendre les sujets une deuxieme fois pour les absents.
- **La decision a deja ete prise** : si le sujet de la reunion a ete resolu en async entre-temps, annuler et communiquer la decision par message.
- **Il n'y a pas de decision a prendre** : si la reunion est purement informative, un Loom ou un message structure est systematiquement plus efficace.

### Methodes de Reduction

#### Meeting Audit
1. Lister toutes les reunions recurrentes du calendrier de chaque equipe.
2. Pour chaque reunion, demander : "Si cette reunion etait supprimee demain, que se passerait-il ?"
3. Classer les reunions en 3 categories : Essentielle (garder), Optimisable (raccourcir ou passer en async), Inutile (supprimer).
4. Supprimer les reunions inutiles immediatement. Optimiser les autres dans les 2 semaines.
5. Refaire cet audit tous les trimestres.

#### No-Meeting Days
Instaurer 1-2 jours sans reunion par semaine pour toute l'equipe :
- Recommandation : mardi et jeudi sans reunion, lundi/mercredi/vendredi pour les reunions.
- Les no-meeting days sont sacres — pas d'exceptions sauf urgence reelle.
- Bloquer les journees dans le calendrier pour que personne ne puisse planifier de reunion.
- Mesurer l'impact sur la productivite et la satisfaction apres 1 mois.

#### Speedy Meetings
Raccourcir toutes les reunions par defaut :
- Les reunions de 30 minutes deviennent 25 minutes.
- Les reunions de 60 minutes deviennent 50 minutes.
- Configurer les parametres de calendrier (Google Calendar et Outlook le permettent) pour que les reunions soient automatiquement plus courtes.
- Les 5-10 minutes liberees permettent de souffler, de se deplacer, et d'arriver a l'heure a la reunion suivante.

#### Meeting Cost Calculator
Calculer le cout reel d'une reunion pour sensibiliser les organisateurs :
- Cout = (nombre de participants) x (duree en heures) x (cout horaire moyen charge).
- Exemple : une reunion de 60 min avec 8 participants dont le cout horaire moyen est de 80 EUR = 640 EUR.
- Afficher ce cout dans l'invitation de la reunion pour inciter a reduire les participants et la duree.
- Un standup quotidien de 30 minutes avec 10 personnes a 80 EUR/h = 200 000 EUR/an. Si le standup peut etre async, c'est 200 000 EUR de travail profond recupere.

---

## PARTIE 10 — Checklist Reunion Efficace

### Avant la Reunion

| # | Action | Responsable | Fait |
|---|--------|-------------|------|
| 1 | Verifier que la reunion est necessaire (pas remplacable par async) | Organisateur | ☐ |
| 2 | Definir l'objectif en une phrase | Organisateur | ☐ |
| 3 | Rediger et distribuer l'agenda 24h avant | Organisateur | ☐ |
| 4 | Preparer et distribuer le pre-read 24h avant | Owner du sujet | ☐ |
| 5 | Inviter uniquement les participants essentiels (max 7 pour une decision) | Organisateur | ☐ |
| 6 | Fixer la duree a 25 ou 50 minutes | Organisateur | ☐ |
| 7 | Designe un note-taker et un time-keeper | Organisateur | ☐ |

### Pendant la Reunion

| # | Action | Responsable | Fait |
|---|--------|-------------|------|
| 8 | Commencer a l'heure (pas d'attente des retardataires) | Animateur | ☐ |
| 9 | Rappeler l'objectif et l'agenda en 1 minute | Animateur | ☐ |
| 10 | Respecter le timing de chaque sujet | Time-keeper | ☐ |
| 11 | Solliciter les participants distants explicitement | Animateur | ☐ |
| 12 | Documenter les decisions et actions en temps reel | Note-taker | ☐ |
| 13 | Terminer 5 minutes avant la fin pour le recap et les actions | Animateur | ☐ |
| 14 | Finir a l'heure | Animateur | ☐ |

### Apres la Reunion

| # | Action | Responsable | Fait |
|---|--------|-------------|------|
| 15 | Publier le compte-rendu dans le channel dans les 2 heures | Note-taker | ☐ |
| 16 | Assigner les actions avec responsable et echeance | Animateur | ☐ |
| 17 | Partager l'enregistrement pour les absents (si applicable) | Organisateur | ☐ |
| 18 | Collecter le ROTI (optionnel mais recommande) | Animateur | ☐ |
| 19 | Reviser si la prochaine occurrence de la reunion est necessaire | Organisateur | ☐ |
