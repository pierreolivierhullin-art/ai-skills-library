# Design Thinking — Methodologie et Application Metier

## Vue d'Ensemble

Le design thinking est une methodologie de resolution de problemes centree sur l'humain, developpee a Stanford et popularisee par IDEO. Elle repose sur l'alternance systematique entre phases de divergence (generer des possibilites) et de convergence (selectionner les meilleures). Sa valeur differenciante : l'investissement en amont sur la comprehension profonde du probleme avant de chercher des solutions.

---

## Phase 1 — Empathize : Comprendre l'Utilisateur

### Methodes de recherche

**Interviews contextuelles** :
L'interview contextuelle se deroule dans l'environnement naturel de l'utilisateur (son bureau, son domicile, son magasin), pas dans une salle de reunion. Duree : 45-90 minutes. Ratio ideale : 80% d'ecoute, 20% de questions.

**Guide d'interview JTBD (Jobs-to-be-Done)** :
```
Partie 1 — Contexte (10 min)
- Decrivez votre journee type dans ce role
- A quel moment utilisez-vous [produit/service] ?
- Quel etait votre workflow avant ?

Partie 2 — Comportements (20 min)
- Montrez-moi comment vous faites ca en ce moment
- Qu'est-ce qui vous prend le plus de temps ?
- Quand ca bloque, que faites-vous ?

Partie 3 — Frustrations et desirs (15 min)
- Qu'est-ce qui vous agace le plus dans ce processus ?
- Si vous aviez une baguette magique, que changeriez-vous ?
- Qu'est-ce que vous trouvez le plus satisfaisant ?

Cloture (5 min)
- Y a-t-il quelque chose qu'on n'a pas aborde et qui vous semble important ?
- Pouvez-vous nous suggerer quelqu'un d'autre a interviewer ?
```

**5 Why's (5 Pourquoi)** :
Technique pour atteindre la cause racine. Chaque reponse devient la question suivante.
```
Probleme : "Les commerciaux n'utilisent pas le CRM"
Pourquoi 1 : "C'est trop long a remplir"
Pourquoi 2 : "Les champs obligatoires sont nombreux et peu pertinents"
Pourquoi 3 : "Le CRM a ete configure par la DSI sans impliquer les commerciaux"
Pourquoi 4 : "Le projet CRM n'avait pas de sponsor commercial"
Pourquoi 5 : "La direction ne considerait pas l'adoption comme un risque projet"
Cause racine : absence de gouvernance utilisateur dans les projets IT
```

**Observation silencieuse (Shadowing)** :
Suivre un utilisateur pendant sa journee sans intervenir. Relever : temps passe sur chaque activite, moments de frustration (soupirs, hésitations), workarounds (quand ils contournent le processus officiel), interactions avec collègues. Duree minimum : 2h.

**Cultural Probes** :
Kit d'outils laisses avec l'utilisateur pendant 1 semaine : journal de bord, appareil photo, post-its pour noter les moments importants. Permet de capturer le quotidien sans observateur. Tres utile pour les comportements difficiles a observer (vie privee, comportements nocturnes).

### Outils de synthese

**Empathy Map** :
```
         CE QU'IL DIT      CE QU'IL PENSE
              |                  |
VOIT ─────── UTILISATEUR ─────── ENTEND
              |                  |
         CE QU'IL FAIT      CE QU'IL RESSENT
              |
    FRUSTRATIONS  |  BESOINS
```

Remplir en equipe apres les interviews. Identifier les tensions (ce qu'il dit vs ce qu'il fait). Les tensions sont des opportunites d'innovation.

**Persona** (1 page max) :
```
[Photo]  Marie, 38 ans — Responsable Operations, ETI industrielle

Citation : "Je passe ma vie dans des reunions plutot que sur le terrain"

Contexte : 15 ans d'experience, manages 12 personnes, responsable de 3 sites
           Outils : Excel (intensif), Teams, SAP (reluctant)

Objectifs             Frustrations
- Prevenir les        - Donnees dispersees
  pannes              - Alertes trop tardives
- Optimiser les       - Reporting manuel
  tournees            - 40% du temps en admin

Comportements
- Checke les KPIs chaque matin sur son mobile
- Prefere les resumes visuels aux tableaux
- Formee a Six Sigma, pense en processus
```

---

## Phase 2 — Define : Formuler le Probleme

### Point of View (POV)

Structure : **[UTILISATEUR]** a besoin de **[BESOIN]** parce que **[INSIGHT]**

Exemples :
- Mauvais : "Marie a besoin d'un meilleur tableau de bord"
- Bon : "Marie, responsable operations sur 3 sites, a besoin de voir l'etat de ses equipements en temps reel parce que les alertes actuelles arrivent apres la panne, pas avant"

### How Might We (HMW)

Transformer les insights en questions creatives. Formulation : "Comment pourrions-nous... ?"

```
Insight : "Marie ne peut pas agir sur les alertes parce qu'elles arrivent trop tard"

HMW (trop large) : "Comment pourrions-nous ameliorer la maintenance ?"
HMW (trop etroit) : "Comment pourrions-nous envoyer les alertes plus vite ?"
HMW (juste) : "Comment pourrions-nous permettre a Marie d'anticiper les pannes
               avant qu'elles ne se produisent ?"

Autres angles HMW :
- "Comment pourrions-nous rendre les informations terrain disponibles
   sans que Marie soit physiquement presente ?"
- "Comment pourrions-nous reduire les taches administratives de Marie
   de 50% pour qu'elle passe plus de temps sur le terrain ?"
```

### Journey Map

Visualiser l'experience complete de l'utilisateur sur un processus :

```
Etapes :  Detecte  Evalue   Decide  Agit   Verifie
          probleme  urgence  action  dessus  resultat
             |        |       |       |        |
Pensees : "Encore   "Est-ce  "Qui    "Encore  "Enfin,
           une       grave ? j'appelle?" un     mais
           alerte"           ?         ticket" pourquoi
                                              si tard"
             |        |       |       |        |
Emotions :  😐       😰      😤      😓       😤
             |        |       |       |        |
Canaux :   Email    Appel   Teams   GMAO     Email
           SAP
             |        |       |       |        |
Opportunites : [!] Alertes predictives | [!] Dashboard | [!] Workflow automatise
```

---

## Phase 3 — Ideate : Generer des Solutions

### Regles du Brainstorming (IDEO)

1. **Differer le jugement** : aucune critique pendant la generation
2. **Quantite avant qualite** : viser 100 idees en 30 minutes
3. **S'appuyer sur les idees des autres** : "Oui, et..." au lieu de "Oui, mais..."
4. **Encourager les idees folles** : les idees irrealisables inspirent les idees realisables
5. **Rester visuel** : dessiner plutot qu'expliquer
6. **Une conversation a la fois** : eviter les discussions en parallele
7. **Rester focalise sur le sujet** : afficher le HMW visible de tous

### Crazy 8's

Technique de sketching intensif : plier une feuille A4 en 8 rectangles. Dessiner 8 idees differentes en 8 minutes (1 min/idee). Contrainte de temps force la generation sans censure. A faire individuellement d'abord, puis partage.

### SCAMPER

Technique de transformation d'une solution existante :
- **S**ubstituer : remplacer un element par un autre
- **C**ombiner : fusionner avec un autre produit/service
- **A**dapter : adapter depuis un autre domaine
- **M**odifier/Magnifier/Minifier : changer une dimension
- **P**roposer d'autres usages
- **E**liminer : supprimer des elements
- **R**eorganiser/Renverser : inverser l'ordre ou la logique

---

## Phase 4 — Prototype : Rendre Tangible

### La resolution croissante du prototype

**Niveau 1 — Papier (2-4h)** :
Screens dessinés sur post-its ou papier A4. Suffisant pour tester la navigation et le concept. Le plus rapide et le moins coûteux — donc le plus utile.

**Niveau 2 — Maquette cliquable (1-2 jours)** :
Figma, Marvel ou Invision. Photos des prototypes papier linkees entre elles, ou wireframes basse fidelite. Permet des tests plus realistes sans coder.

**Niveau 3 — Prototype haute fidelite (3-5 jours)** :
Figma avec design complet. Indiscernable d'une vraie application. Utiliser si le test necessite que l'utilisateur se "projette" dans le produit final.

**Niveau 4 — Wizard of Oz** :
L'utilisateur croit interagir avec un systeme automatise, mais c'est un humain qui repond dans les coulisses. Permet de tester des experiences IA/ML sans les developper. Ex : test d'un chatbot avec un agent humain.

**Niveau 5 — Concierge MVP** :
Fournir le service manuellement a un petit groupe de clients reels avant de l'automatiser. Ex : avant de construire un algorithme de recommandation, faire les recommandations manuellement par email.

---

## Phase 5 — Test : Apprendre

### Protocole de test utilisateur

**Regles** :
- Ne jamais aider l'utilisateur : observer sans intervenir
- Ecouter les "je pense a voix haute" (demander au debut : "please think aloud")
- Prendre des notes sur : ce qui fonctionne, ce qui bloque, les questions posees, les comportements inattendus
- 5 utilisateurs suffisent pour detecter 85% des problemes majeurs (Nielsen 1993)

**Script de session (60 minutes)** :
```
Introduction (5 min)
- "Merci de participer. Vous testez un prototype, pas vos competences."
- "Il n'y a pas de bonne ou mauvaise reponse — c'est le prototype qu'on teste."
- "Pensez a voix haute en utilisant le prototype."

Taches (40 min)
Donner des scenarios realistes, pas des instructions :
[MAL] "Cliquez sur le bouton 'Ajouter une alerte'"
[BIEN] "Vous venez de recevoir un appel d'un technicien signalant un bruit
        suspect sur la pompe P3. Que faites-vous ?"

Debriefing (15 min)
- "Qu'est-ce qui vous a semble le plus utile ?"
- "Qu'est-ce qui vous a derouté ou frustré ?"
- "Comment cela s'integrerat-il dans votre travail quotidien ?"
```

### Synthese des resultats — Matrice d'Apprentissage

| Ce qu'on a observe | Interpretation | Prochaine action |
|---|---|---|
| 3/5 utilisateurs ont cherche le bouton "Sauvegarder" en haut | Le pattern habituel est barre d'outils superieure | Deplacer le bouton en haut |
| 2/5 ont confondu "Alerte" et "Notification" | Terminologie ambigue | Tester "Maintenance preventive" comme alternative |
| Tous les utilisateurs ont aime la carte interactive | Forte desirabilite validee | Conserver et developper |

---

## Design Sprint — Format Google (Jake Knapp)

Le Design Sprint compresse les 5 phases en 5 jours pour des equipes de 5-7 personnes.

**Prerequis** :
- 1 "Decider" (pouvoir de decision finale)
- 1 Facilitateur dedie (idealement externe)
- Salle disponible 5 jours, materiels (post-its, markers, tableau)
- Acces a 5 utilisateurs pour les tests du vendredi

**Resultats attendus** :
- 1 prototype haute fidelite
- Donnees qualitatives de 5 interviews utilisateurs
- Decision documentee : Go / Pivot / No-Go

**Quand l'utiliser** :
- Lancement d'une nouvelle fonctionnalite majeure
- Probleme persistant non resolu malgre plusieurs tentatives
- Decision strategique avec grande incertitude

**Quand ne pas l'utiliser** :
- Probleme de performance (bug, lenteur) — pas besoin de design sprint
- Fonctionnalite bien definie — aller directement en developpement
- Manque de temps utilisateurs pour le vendredi — reporter

---

## Outils Recommandes

| Besoin | Outil | Gratuit ? |
|---|---|---|
| Prototypage basse fidelite | Balsamiq, Whimsical | Oui (limites) |
| Prototypage haute fidelite | Figma | Oui (plan gratuit) |
| Workshops collaboratifs | Miro, FigJam | Oui (limites) |
| Tests utilisateurs a distance | Maze, Hotjar | Oui (limites) |
| Enregistrement de sessions | Loom | Oui |
| Synthesis d'interviews | Dovetail, Atlas.ti | Non |
| Gestion des insights | Notion, Airtable | Oui (limites) |
