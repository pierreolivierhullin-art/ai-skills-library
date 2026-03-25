# UX Research -- Methods, Frameworks & Design Sprints

Reference complete pour la recherche utilisateur : methodes qualitatives et quantitatives, frameworks de decision, personas, journey mapping et design sprints. Complete reference for user research: qualitative and quantitative methods, decision frameworks, personas, journey mapping, and design sprints.

---

## 1. User Research Methods

### Vue d'ensemble / Overview

La recherche utilisateur est le fondement de toute decision de design informee. Distinguer deux axes : le moment de la recherche (discovery vs validation) et le type de donnees (qualitatif vs quantitatif). Ne jamais designer sans avoir au minimum conduit 5 interviews utilisateur.

User research is the foundation of every informed design decision. Distinguish two axes: the timing of research (discovery vs validation) and the type of data (qualitative vs quantitative). Never design without having conducted at minimum 5 user interviews.

### User Interviews

**Objectif / Goal:** Comprendre les besoins, motivations, frustrations et modeles mentaux des utilisateurs en profondeur.

**Protocole / Protocol:**
1. **Preparation** : definir 3-5 objectifs de recherche. Rediger un guide d'entretien avec des questions ouvertes. Eviter les questions orientees ("N'aimez-vous pas cette fonctionnalite ?").
2. **Recrutement** : recruter 5-8 participants representatifs du segment cible. Utiliser un screener questionnaire pour filtrer. Prevoir une compensation (carte cadeau, remuneration).
3. **Conduite** : sessions de 45-60 minutes. Un interviewer + un preneur de notes. Enregistrer (audio/video) avec consentement. Suivre le guide mais laisser les tangentes enrichissantes se developper.
4. **Analyse** : transcrire les points cles. Utiliser la methode d'affinite (affinity diagramming) pour regrouper les insights en themes.
5. **Synthese** : produire un rapport avec insights cles, citations verbatim, et recommandations actionnables.

**Questions types / Sample Questions:**
- "Decrivez-moi la derniere fois que vous avez [tache cible]. Qu'avez-vous fait etape par etape ?"
- "Qu'est-ce qui etait le plus frustrant dans cette experience ?"
- "Si vous pouviez changer une chose, ce serait quoi ?"
- "Comment faisiez-vous avant d'utiliser [solution actuelle] ?"
- "Montrez-moi comment vous feriez [tache] sur votre ecran maintenant."

### Usability Testing

**Objectif / Goal:** Evaluer l'utilisabilite d'un produit ou prototype en observant des utilisateurs reels accomplir des taches specifiques.

**Types de tests / Test Types:**

| Type | Fidelite | Participants | Quand |
|---|---|---|---|
| **Guerilla testing** | Paper/low-fi | 3-5 | Early discovery |
| **Moderated remote** | Mid-fi to hi-fi | 5-8 | Prototype validation |
| **Unmoderated remote** | Hi-fi / production | 10-20+ | Post-launch optimization |
| **Lab testing** | Any | 5-8 | Complex interactions, a11y |

**Protocole de test modere / Moderated Test Protocol:**
1. **Scenarios de tache** : rediger 5-7 scenarios realistes ("Vous souhaitez acheter un billet de train Paris-Lyon pour vendredi prochain").
2. **Think-aloud** : demander aux participants de verbaliser leurs pensees pendant qu'ils executent les taches.
3. **Metriques** : mesurer le taux de completion, le temps de tache, le nombre d'erreurs, la satisfaction (SEQ - Single Ease Question, echelle 1-7).
4. **Observation** : noter les hesitations, les erreurs, les retours en arriere, les expressions faciales.
5. **Debriefing** : poser des questions ouvertes apres chaque tache et a la fin de la session.

**Regle des 5 utilisateurs / 5-User Rule:**
5 participants detectent ~85% des problemes d'utilisabilite majeurs (Nielsen/Landauer). Conduire des cycles de 5 tests iteratifs plutot qu'un grand test de 20 participants.

### Surveys / Questionnaires

**Objectif / Goal:** Collecter des donnees quantitatives a grande echelle pour valider des hypotheses ou mesurer la satisfaction.

**Types de questionnaires standardises / Standardized Questionnaire Types:**

| Survey | Purpose | Scale | Benchmark |
|---|---|---|---|
| **SUS** (System Usability Scale) | Usabilite globale | 0-100 | > 68 = above average |
| **NPS** (Net Promoter Score) | Recommandation | -100 to 100 | > 50 = excellent |
| **CSAT** (Customer Satisfaction) | Satisfaction | 1-5 | > 4 = bon |
| **CES** (Customer Effort Score) | Effort percu | 1-7 | < 3 = faible effort |
| **SEQ** (Single Ease Question) | Facilite de tache | 1-7 | > 5.5 = facile |
| **UEQ** (User Experience Questionnaire) | Experience complete | -3 to 3 | > 0.8 = bon |

**Bonnes pratiques / Best Practices:**
- Limiter a 10-15 questions maximum. Chaque question supplementaire reduit le taux de completion.
- Melanger questions fermees (echelles) et questions ouvertes (pourquoi).
- Eviter les questions a double negation et les questions orientees.
- Tester le questionnaire avec 3 personnes avant le deploiement.
- Viser un minimum de 30 reponses pour des resultats significatifs (100+ pour des analyses par segment).

### Diary Studies

**Objectif / Goal:** Capturer les comportements et experiences des utilisateurs dans leur contexte naturel sur une periode prolongee (1-4 semaines).

**Protocole / Protocol:**
1. **Setup** : definir la duree (1-4 semaines), la frequence des entrees (quotidienne ou par evenement), et le format (texte, photo, video).
2. **Outil** : utiliser une application mobile (dscout, Indeemo) ou un simple formulaire (Google Forms, Typeform).
3. **Prompts** : envoyer des rappels quotidiens avec des questions contextuelles : "Qu'avez-vous fait aujourd'hui avec [produit] ?" "Quel moment a ete le plus frustrant ?"
4. **Analyse** : analyser les entrees chronologiquement et thematiquement. Identifier les patterns recurrents et les moments critiques.

**Use cases ideaux / Ideal Use Cases:**
- Comprendre les routines quotidiennes et les workflows reel.
- Identifier les pain points qui n'emergent pas en session de test unique.
- Etudier l'adoption et l'apprentissage d'un nouveau produit dans le temps.
- Capturer le contexte d'usage (lieu, moment, appareil, etat emotionnel).

### Card Sorting

**Objectif / Goal:** Comprendre les modeles mentaux des utilisateurs pour structurer l'architecture de l'information.

**Types / Types:**
- **Open card sort** : les participants groupent les cartes et nomment les categories eux-memes. Utiliser en phase de discovery.
- **Closed card sort** : les categories sont predefinies, les participants classent les cartes. Utiliser pour valider une structure existante.
- **Hybrid card sort** : categories predefinies mais les participants peuvent en creer de nouvelles.

**Protocole / Protocol:**
1. Preparer 30-60 cartes representant les contenus/fonctionnalites a organiser.
2. Recruter 15-20 participants (minimum) pour des resultats fiables.
3. Utiliser un outil en ligne (Optimal Workshop, UserZoom) ou des cartes physiques.
4. Analyser avec une matrice de similarite et un dendrogramme pour identifier les groupements naturels.

### Contextual Inquiry

**Objectif / Goal:** Observer et interroger les utilisateurs dans leur environnement de travail reel pour comprendre les pratiques actuelles.

**Les 4 principes / The 4 Principles (Beyer & Holtzblatt):**
1. **Context** : observer dans l'environnement reel, pas en laboratoire.
2. **Partnership** : etablir une relation maitre-apprenti ou l'utilisateur enseigne au chercheur.
3. **Interpretation** : partager les interpretations en temps reel avec l'utilisateur pour les valider.
4. **Focus** : garder le focus sur les aspects pertinents pour le projet de design.

**Quand utiliser / When to Use:**
- Redesign d'un outil professionnel complexe.
- Comprehension de workflows impliquant plusieurs outils et personnes.
- Migration d'un outil existant vers une nouvelle plateforme.
- Identification de besoins non exprimes (latent needs).

---

## 2. Personas & User Journeys

### Personas basees sur les donnees / Data-Driven Personas

Construire des personas a partir de donnees reelles (interviews, analytics, surveys), jamais a partir de suppositions.

**Structure d'une persona / Persona Structure:**
- **Nom et photo** : humaniser la persona (utiliser des noms credibles, pas de cliches).
- **Demographics** : age, profession, expertise technique, situation de handicap eventuelle.
- **Goals** : 2-3 objectifs principaux que la persona cherche a accomplir.
- **Frustrations / Pain points** : 2-3 obstacles majeurs rencontres actuellement.
- **Behaviors** : habitudes, outils utilises, frequence d'usage, contexte d'usage.
- **Quotes** : 1-2 citations verbatim des interviews qui capturent l'essence de la persona.
- **Scenario d'usage** : un scenario narratif decrivant un usage typique.

**Regles / Rules:**
- Limiter a 3-5 personas maximum. Au-dela, elles perdent leur utilite de priorisation.
- Distinguer la persona primaire (cible principale) des personas secondaires.
- Mettre a jour les personas annuellement avec de nouvelles donnees de recherche.
- Ne jamais utiliser les personas comme substitut a la recherche continue.

### User Journey Maps

Cartographier l'experience complete de l'utilisateur a travers les points de contact avec le produit/service.

**Structure d'une journey map / Journey Map Structure:**

| Phase | Actions | Thoughts | Emotions | Pain Points | Opportunities |
|---|---|---|---|---|---|
| Awareness | Decouvre le produit | "Ca pourrait m'aider" | Curiosite | Pas d'info claire | Landing page claire |
| Onboarding | Cree un compte | "C'est long..." | Frustration | Formulaire complexe | Simplifier, SSO |
| First Use | Explore les features | "Ou est X ?" | Confusion | Navigation confuse | Guided tour |
| Regular Use | Utilise quotidiennement | "C'est pratique" | Satisfaction | Tache repetitive | Shortcuts |
| Advocacy | Recommande | "Tu devrais essayer" | Enthousiasme | Pas de partage facile | Referral program |

**Regles / Rules:**
- Baser la journey map sur les donnees de recherche (interviews, analytics), pas sur des hypotheses internes.
- Inclure les points de contact hors produit (email, support, documentation).
- Identifier les "moments de verite" (moments critiques ou l'experience est faite ou defaite).
- Mettre a jour regulierement en fonction des changements de produit et des nouvelles donnees.

### Jobs-to-be-Done (JTBD)

Utiliser le framework JTBD pour comprendre les motivations profondes des utilisateurs au-dela des fonctionnalites.

**Formulation d'un Job / Job Statement Format:**
"Quand [situation], je veux [motivation], pour que [resultat attendu]."

**Exemples / Examples:**
- "Quand je planifie un voyage en equipe, je veux voir les disponibilites de chacun, pour que je puisse trouver une date qui convient a tous."
- "Quand je recois une notification d'erreur, je veux comprendre immediatement ce qui s'est passe, pour que je puisse corriger le probleme rapidement."

**Job Map / Job Map:**
1. **Define** : le client definit ce qu'il veut accomplir.
2. **Locate** : il rassemble les elements necessaires.
3. **Prepare** : il se prepare a executer le job.
4. **Confirm** : il valide que tout est pret.
5. **Execute** : il execute le job.
6. **Monitor** : il surveille le deroulement.
7. **Modify** : il ajuste si necessaire.
8. **Conclude** : il termine et evalue le resultat.

---

## 3. Heuristic Evaluation -- Nielsen's 10 Heuristics

### Les 10 heuristiques de Nielsen / Nielsen's 10 Heuristics

Utiliser ces heuristiques comme cadre d'evaluation rapide de l'utilisabilite. Conduire l'evaluation avec 3-5 evaluateurs experts independants, puis consolider les findings.

**1. Visibility of System Status**
Le systeme doit informer l'utilisateur de ce qui se passe en temps reel. Exemples : indicateurs de chargement, barres de progression, confirmations d'actions, etats de sauvegarde.

**2. Match Between System and Real World**
Utiliser un langage et des concepts familiers a l'utilisateur. Organiser l'information selon les conventions du domaine, pas selon la structure technique interne.

**3. User Control and Freedom**
Fournir des "sorties de secours" claires : undo/redo, boutons annuler, retour arriere. Les utilisateurs font des erreurs ; leur permettre de les corriger facilement.

**4. Consistency and Standards**
Suivre les conventions de la plateforme et les patterns etablis. Un meme element doit se comporter de la meme maniere partout dans l'application.

**5. Error Prevention**
Prevenir les erreurs plutot que les signaler. Utiliser des confirmations pour les actions destructives, des contraintes de saisie (datepickers plutot que saisie libre), et des valeurs par defaut intelligentes.

**6. Recognition Rather Than Recall**
Minimiser la charge cognitive en rendant les options visibles. Utiliser des menus, des suggestions, des historiques plutot que de demander a l'utilisateur de se souvenir.

**7. Flexibility and Efficiency of Use**
Offrir des raccourcis pour les utilisateurs experts (keyboard shortcuts, commandes, favoris) sans compliquer l'interface pour les novices.

**8. Aesthetic and Minimalist Design**
Chaque element supplementaire est en competition avec le contenu pertinent. Supprimer tout ce qui n'est pas strictement necessaire. Privilegier la hierarchie visuelle claire.

**9. Help Users Recognize, Diagnose, and Recover from Errors**
Les messages d'erreur doivent etre en langage clair (pas de codes techniques), indiquer le probleme et suggerer une solution concrete.

**10. Help and Documentation**
Fournir une aide contextuelle accessible depuis l'interface. La meilleure documentation est celle que l'utilisateur n'a pas besoin de consulter grace a un design intuitif.

### Methode d'evaluation / Evaluation Method

1. Chaque evaluateur examine l'interface independamment.
2. Pour chaque probleme identifie, associer l'heuristique violee.
3. Evaluer la severite (1-4) : cosmetic, minor, major, catastrophe.
4. Consolider les findings : regrouper les problemes identiques, prioriser par severite et frequence.
5. Produire un rapport avec recommandations actionnables classees par priorite.

---

## 4. Design Thinking & Design Sprint

### Design Thinking Process (IDEO / Stanford d.school)

Appliquer le processus en 5 etapes comme cadre iteratif pour la resolution de problemes centres utilisateur.

**Etape 1 -- Empathize (Comprendre)**
Conduire des recherches terrain pour comprendre les besoins reels. Utiliser les interviews, l'observation contextuelle et les diary studies. Construire une empathy map (Says, Thinks, Does, Feels).

**Etape 2 -- Define (Definir)**
Synthetiser les insights de recherche en un point de vue (POV) actionnable. Formuler un "How Might We" (HMW) statement : "Comment pourrions-nous [objectif] pour [persona] afin de [resultat] ?"

**Etape 3 -- Ideate (Generer)**
Generer un maximum d'idees sans jugement. Utiliser le brainstorming structure (Crazy 8s, brainwriting, SCAMPER). Converger en votant (dot voting) sur les idees les plus prometteuses.

**Etape 4 -- Prototype**
Construire des prototypes rapides pour tester les idees. Commencer par le plus faible niveau de fidelite necessaire : paper prototypes, wireframes clickables (Figma, Balsamiq), prototypes coded (HTML/CSS rapide).

**Etape 5 -- Test**
Tester les prototypes avec des utilisateurs reels. Utiliser les usability tests moderes. Iterer en fonction des resultats : revenir a n'importe quelle etape precedente si necessaire.

### Google Ventures Design Sprint (5 jours)

Le Design Sprint est un processus structure de 5 jours pour passer d'un probleme a une solution testee.

**Lundi -- Map & Target**
- Definir l'objectif a long terme du sprint.
- Cartographier le parcours utilisateur (journey map simplifiee).
- Interviewer les experts internes (stakeholders, support, ventes).
- Choisir un segment cible du parcours a traiter.

**Mardi -- Sketch**
- Lightning demos : chaque participant presente des inspirations (solutions existantes, competitors).
- Ideation individuelle : chaque participant dessine des solutions (Crazy 8s, solution sketch detaille).
- Pas de groupthink : le travail individuel produit plus de diversite.

**Mercredi -- Decide**
- Presentation silencieuse des sketches (art museum).
- Vote par dots (heat map voting).
- Decision finale par le "Decider" (decision maker designee).
- Storyboard : creer un storyboard detaille de la solution retenue (8-12 frames).

**Jeudi -- Prototype**
- Construire un prototype realiste en une journee.
- Utiliser Figma ou Keynote pour un prototype haute fidelite.
- Division du travail : makers (designers), stitcher (integre), writer (contenu), asset collector.
- Le prototype doit etre "just enough" pour tester les hypotheses.

**Vendredi -- Test**
- 5 interviews utilisateur de 60 minutes chacune.
- Un interviewer + des observateurs dans une piece separee (ou remote).
- Observer les patterns : si 3/5 participants butent sur le meme point, c'est un signal fort.
- Debrief collectif immediat : patterns observes, insights, decisions pour la suite.

### Quand utiliser un Design Sprint / When to Use a Design Sprint

| Situation | Design Sprint ? | Alternative |
|---|---|---|
| Nouvelle fonctionnalite majeure | Oui | - |
| Pivot strategique | Oui | - |
| Redesign complet | Oui | - |
| Amelioration incrementale | Non | Usability testing direct |
| Bug fix UX | Non | Quick research + fix |
| Exploration (pas de probleme clair) | Non | Discovery research |

---

## 5. Research Operations (ResearchOps)

### Industrialiser la recherche / Scaling Research

Pour les organisations conduisant de la recherche regulierement, mettre en place une infrastructure de ResearchOps.

**Repository de recherche / Research Repository:**
- Centraliser tous les findings dans un outil searchable (Dovetail, EnjoyHQ, Notion).
- Tagger les insights par theme, produit, persona, methode.
- Rendre les insights accessibles a toute l'organisation (pas seulement l'equipe UX).
- Mettre a jour et archiver les insights perimes.

**Panel de participants / Participant Panel:**
- Maintenir une base de participants volontaires pour accelerer le recrutement.
- Segmenter par persona, usage, expertise.
- Respecter la frequence de sollicitation (pas plus d'une fois par trimestre par participant).
- Gerer le consentement RGPD et la compensation.

**Templates et processus / Templates and Processes:**
- Templates standardises pour les guides d'entretien, les rapports d'insights, les journey maps.
- Processus de review par les pairs pour les syntheses de recherche.
- Cadence reguliere : sprint research (biweekly), deep research (quarterly).

---

## 6. Mesurer l'Impact UX / Measuring UX Impact

### Metriques UX essentielles / Essential UX Metrics

| Metric | Type | Measurement | Target |
|---|---|---|---|
| **Task Success Rate** | Effectiveness | % of completed tasks | > 90% |
| **Time on Task** | Efficiency | Time to complete task | Decreasing |
| **Error Rate** | Effectiveness | Errors per task | < 5% |
| **SUS Score** | Satisfaction | Standardized survey | > 68 |
| **NPS** | Loyalty | Survey (-100 to 100) | > 50 |
| **CSAT** | Satisfaction | Survey (1-5) | > 4.0 |
| **CES** | Effort | Survey (1-7) | < 3.0 |
| **Conversion Rate** | Business | % completing goal | Increasing |
| **Bounce Rate** | Engagement | % leaving immediately | Decreasing |
| **Feature Adoption** | Engagement | % using new feature | > 60% after 30 days |

### Lier UX et impact business / Linking UX to Business Impact

Toujours connecter les metriques UX aux metriques business pour demontrer la valeur de la recherche :
- Reduction du taux d'erreur -> reduction des tickets support -> economie de couts.
- Amelioration du taux de completion -> augmentation de la conversion -> augmentation du revenu.
- Amelioration du SUS -> augmentation de la retention -> augmentation de la LTV.
- Amelioration de l'accessibilite -> augmentation de l'audience adressable -> augmentation du marche.

---

## References

- Steve Krug, *Don't Make Me Think* (3rd ed., 2014)
- Jakob Nielsen, *Usability Engineering* (1993)
- Jake Knapp, *Sprint: How to Solve Big Problems in Just Five Days* (2016)
- Erika Hall, *Just Enough Research* (2nd ed., 2019)
- Indi Young, *Mental Models* (2008)
- Alan Cooper, *About Face: The Essentials of Interaction Design* (4th ed., 2014)
- Clayton Christensen, *Competing Against Luck* (JTBD framework, 2016)
- Nielsen Norman Group -- https://www.nngroup.com
- Beyer & Holtzblatt, *Contextual Design* (2nd ed., 2017)
