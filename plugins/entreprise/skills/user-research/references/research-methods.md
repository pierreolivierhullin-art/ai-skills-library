# Research Methods -- Guide Complet des Methodes de Recherche Utilisateur

Guide de reference exhaustif des methodes de recherche utilisateur. Couvre les interviews exploratoires et de validation, les tests d'utilisabilite moderes et non-moderes, les diary studies, la contextual inquiry, la conception de surveys, le card sorting, le tree testing, le guerrilla testing, le recrutement de participants et l'etat de l'art 2025-2026 avec les outils IA.

---

## Interviews Exploratoires

Utiliser les interviews exploratoires en phase de discovery, quand l'objectif est de comprendre un espace probleme, un contexte d'usage ou un workflow avant de formuler des hypotheses. L'interview exploratoire ne cherche pas a valider une idee : elle cherche a decouvrir ce qu'on ne sait pas encore.

**Dimensionnement** : 5-8 participants par segment pour atteindre la saturation thematique (Nielsen/Landauer). Pour un sujet multi-segments (ex : 3 personas), prevoir 5 par segment = 15 total. Pour un sujet complexe ou un nouveau marche, viser 8-12 participants.

### Script d'interview exploratoire -- Template

```
Phase 1 -- Introduction (5 min)
   +-- Presenter le contexte sans orienter ("On cherche a comprendre comment...")
   +-- Obtenir le consentement ecrit, demander la permission d'enregistrer
   +-- "Il n'y a pas de bonne ou mauvaise reponse"
Phase 2 -- Echauffement (5 min)
   +-- "Pouvez-vous me decrire votre role et vos responsabilites ?"
   +-- "A quoi ressemble une journee type pour vous ?"
Phase 3 -- Exploration du probleme (30-40 min)
   +-- "Racontez-moi la derniere fois que vous avez du faire [activite cible]"
   +-- "Comment faites-vous aujourd'hui pour [tache cible] ?"
   +-- "Qu'est-ce qui est le plus frustrant ou difficile ?"
   +-- Suivre le recit du participant, ne pas imposer un ordre rigide
Phase 4 -- Approfondissement (10 min)
   +-- "Pouvez-vous me montrer comment vous faites concretement ?"
   +-- "Que se passe-t-il quand [scenario limite] ?"
Phase 5 -- Cloture (5 min)
   +-- "Y a-t-il quelque chose que je n'ai pas demande et que vous aimeriez partager ?"
   +-- Remercier et expliquer les prochaines etapes
```

### Techniques de probing

| Technique | Formulation | Quand l'utiliser |
|---|---|---|
| **Echo** | Repeter le dernier mot du participant | Developper sans orienter |
| **Silence** | 5-7 secondes de silence apres une reponse | Le participant hesite a aller plus loin |
| **Pourquoi x5** | "Pourquoi ?" repete pour aller a la cause racine | Reponse en surface |
| **Contraste** | "Qu'est-ce qui serait different si... ?" | Explorer des scenarios alternatifs |
| **Concretisation** | "Pouvez-vous me donner un exemple precis ?" | Reponse trop abstraite |
| **Show me** | "Pouvez-vous me montrer sur votre ecran ?" | Observer le comportement reel vs declaratif |

### Erreurs frequentes

- **Questions fermees** : "Est-ce que c'est difficile ?" au lieu de "Decrivez-moi comment ca se passe"
- **Questions orientees** : "Ne trouvez-vous pas que X est un probleme ?" oriente la reponse
- **Solution trop tot** : reveler le produit ou l'idee avant d'avoir explore le probleme
- **Doubles questions** : "Comment faites-vous X et qu'est-ce qui est frustrant ?" — une question a la fois
- **Accepter les generalisations** : quand le participant dit "en general", demander un exemple specifique recent
- **Remplir les silences** : laisser le participant reflechir, ne pas reformuler immediatement

---

## Interviews de Validation

### Difference avec les interviews exploratoires

| Dimension | Exploratoire | Validation |
|---|---|---|
| **Objectif** | Decouvrir l'espace probleme | Tester une hypothese specifique |
| **Questions** | Ouvertes, non-directives | Semi-structurees, orientees hypothese |
| **Analyse** | Emergence de themes | Confirmation ou infirmation |
| **Livrable** | Carte du probleme | Decision go/no-go sur l'hypothese |

### Approche hypothesis-testing

```
Hypothese testable :
"Nous croyons que [segment] rencontre [probleme]
 quand [contexte] et que [solution] resoudrait ce probleme"

Criteres de validation pre-definis :
+-- Seuil : X participants sur Y confirment le probleme (ex : 4/5)
+-- Signaux forts : participant propose spontanement la meme solution
+-- Signaux faibles : participant reconnait le probleme mais le contourne
+-- Invalidation : le probleme n'est pas mentionne sans probing
```

**Protocole en 3 etapes** : (1) tester le probleme d'abord ("Racontez-moi la derniere fois que..."), (2) presenter le concept (prototype, storyboard), observer la reaction spontanee, (3) evaluer la traction ("Si cette solution existait, comment reagiriez-vous ?") en cherchant des signaux d'engagement.

---

## Tests d'Utilisabilite Moderes

### Setup et protocole Think-Aloud

```
Checklist de preparation :
+-- Definir 3-5 taches representant les parcours critiques
+-- Rediger les scenarios (contexte + objectif, sans indiquer le chemin)
+-- Tester le setup complet avec un participant pilote
+-- Configurer l'enregistrement (ecran + webcam + audio)
+-- Preparer la grille d'observation pour les observateurs
```

**Think-Aloud** — instruction au participant : "Pensez a voix haute. Dites-moi ce que vous voyez, ce que vous pensez, ce que vous cherchez." Deux variantes : concurrent (verbalise en temps reel, acces direct aux pensees, peut modifier le comportement) et retrospectif (commente l'enregistrement apres, comportement naturel preserve, risque de rationalisation).

**Conception des taches** : contextualiser avec un scenario realiste, indiquer l'objectif pas le chemin, definir le critere de succes mesurable, prioriser les taches critiques en premier.

### Echelle de severite des problemes

| Niveau | Severite | Description | Action |
|---|---|---|---|
| **0** | Non-probleme | Hesitation mais correction spontanee | Documenter |
| **1** | Cosmetique | Gene legere, n'empeche pas la completion | Si le temps le permet |
| **2** | Mineur | Ralentissement, contournement trouve | Prochain sprint |
| **3** | Majeur | Difficulte importante, besoin d'aide | Avant mise en production |
| **4** | Bloquant | Tache impossible meme avec aide | Corriger immediatement |

### Reporting

```
Structure du rapport :
+-- Contexte : objectif, methode, participants
+-- Resume executif : 3-5 findings cles
+-- Resultats par tache : taux de succes, temps, problemes par severite, verbatims
+-- Problemes consolides : description, severite, frequence, recommandation
+-- Video highlights : montage 3-5 min des moments cles
```

---

## Tests d'Utilisabilite Non-Moderes

| Dimension | Modere | Non-modere |
|---|---|---|
| **Chercheur** | Present, peut probing | Absent, pre-configure |
| **Volume** | 5-8 participants | 20-50+ participants |
| **Cout** | Eleve (temps chercheur) | Faible (automatise) |
| **Richesse** | Tres elevee (dialogue) | Moyenne (comportement) |

### Outils (2025-2026)

| Outil | Points forts | Prix indicatif |
|---|---|---|
| **Maze** | Integration Figma, analyse automatisee, heatmaps | 99 EUR/mois |
| **UserTesting** | Panel 2M+ testeurs, video webcam | 15 000 EUR/an |
| **Lookback** | Sessions live et non-moderees, annotations collaboratives | 99 USD/mois |
| **Lyssna (ex-UsabilityHub)** | Tests rapides (5-sec, first click), panel integre | 75 USD/mois |

```
Arbre de decision : modere ou non-modere ?
+-- Comprendre le "pourquoi" en profondeur --> MODERE
+-- Mesurer le "quoi" a grande echelle
|   +-- Taches simples et autonomes --> NON-MODERE
|   +-- Taches necessitant du contexte --> MODERE
+-- Benchmarker avant/apres redesign --> NON-MODERE
+-- Budget ou temps tres limite --> NON-MODERE
```

**Bonnes pratiques** : 3-5 taches max (10-15 min total), instructions claires et non ambigues, tache de calibration en premier, questions post-tache (SEQ 1-7), filtrer les resultats aberrants (temps < 30 sec ou > 5x mediane).

**Metriques** : taux de succes direct/indirect, misclick rate (heatmap), temps de completion, score SEQ, taux d'abandon.

---

## Diary Studies

La diary study capture les comportements qui se deploient dans le temps (adoption, evolution d'un workflow, usage en contexte naturel). Duree : 1-4 semaines. Participants : 10-15 (prevoir 20% d'attrition). Cadence des entrees : event-driven ("a chaque fois que...") ou time-driven ("chaque jour a 18h"). Outils : dscout, Indeemo, ou canal leger (WhatsApp, email).

**Instructions aux participants** : "Documentez [comportement cible] a chaque occurence : (1) contexte, (2) ce qui s'est passe, (3) ce qui a fonctionne ou frustre, (4) photo/capture si possible. 2-5 minutes par entree."

| Moment | Action | Objectif |
|---|---|---|
| **Jour 1** | Onboarding individuel (15 min) | Verifier la comprehension |
| **Jour 3** | Rappel + feedback sur les premieres entrees | Corriger la profondeur |
| **Mi-parcours** | Check-in rapide (10 min) | Maintenir l'engagement |
| **Jour final** | Interview de debriefing (30-45 min) | Approfondir les themes |

**Analyse** : codage chronologique par participant/date/theme, analyse intra-participant (evolution), analyse inter-participants (patterns communs), timeline mapping des moments cles, extraction des triggers contextuels.

---

## Contextual Inquiry

### Les 4 principes (Beyer & Holtzblatt)

| Principe | Application concrete |
|---|---|
| **Partenariat** | Alterner observation et questions : "Je vois que vous avez fait X, pourquoi ?" |
| **Focus** | Definir 2-3 themes a observer avant la session |
| **Interpretation** | Partager les interpretations en temps reel : "Il me semble que... est-ce correct ?" |
| **Modele de contexte** | Documenter l'espace, les outils, les interruptions, les interactions |

```
Protocole (90-120 min) :
+-- Phase 1 (10 min) : introduction et contexte general
+-- Phase 2 (60-90 min) : observation du travail reel
|   +-- Le participant travaille normalement, le chercheur observe
|   +-- Interruptions ponctuelles pour questions contextuelles
|   +-- Photographier l'environnement (avec autorisation)
+-- Phase 3 (15 min) : debriefing et validation des observations
+-- Post-session : retranscrire dans les 24h, construire les modeles de contexte
```

---

## Survey Design

### Types de questions

| Type | Cas d'usage | Attention |
|---|---|---|
| **Choix unique** | Categorisation, segmentation | Options exclusives + "Autre" |
| **Choix multiple** | Inventaire de comportements | 7-10 options max |
| **Likert (1-5 ou 1-7)** | Attitudes, satisfaction | Ancres verbales, echelle impaire |
| **NPS (0-10)** | Satisfaction globale, benchmark | Analyser les verbatims, pas seulement le score |
| **Classement** | Priorisation | 5 items max |
| **Ouverte** | Exploration, verbatims | En fin de survey, 2-3 max |

### Biais a eviter

| Biais | Contre-mesure |
|---|---|
| **Acquiescence** (tendance au "oui") | Alterner formulations positives et negatives |
| **Ordre** (premiere option sur-selectionnee) | Randomiser l'ordre des options |
| **Desirabilite sociale** | Formulations non-jugeantes, anonymiser |
| **Question double** ("Simple et rapide ?") | Une seule idee par question |
| **Fatigue** | Limiter a 5-10 min (15-25 questions max) |

### Taille d'echantillon

```
Formule : n = (Z^2 * p * (1-p)) / e^2
+-- Z = 1.96 (confiance 95%), p = 0.5 (cas conservateur), e = marge d'erreur

| Population | 95% / Marge 5% | 95% / Marge 3% | 99% / Marge 5% |
|------------|----------------|----------------|----------------|
| 500        | 217            | 340            | 285            |
| 1 000      | 278            | 516            | 399            |
| 10 000     | 370            | 964            | 622            |
| 100 000+   | 384            | 1 067          | 663            |
```

**Taux de reponse par canal** : email 10-30% (clients existants), in-app 15-40%, post-interaction 20-50%, panel externe 50-80%. Prevoir un echantillon initial 3-5x superieur a la cible.

---

## Card Sorting

| Type | Principe | Quand |
|---|---|---|
| **Open sort** | Participants creent les categories | Phase exploratoire |
| **Closed sort** | Categories pre-definies | Phase evaluative |
| **Hybrid** | Categories pre-definies + creation libre | Compromis |

**Outils** : OptimalSort (Optimal Workshop, 107 USD/mois, dendrogramme + matrice), Maze (inclus), UserZoom (enterprise), post-it physiques (gratuit).

**Analyse** : matrice de similarite (> 70% = regroupement fort, < 30% = pas de lien) et dendrogramme (representation hierarchique, couper a differents niveaux pour identifier les groupes naturels).

```
Dendrogramme simplifie :
               +--------+--------+
               |                 |
          +----+----+       +----+----+
       +--+--+   Carte E   Carte F   +--+--+
    Carte A Carte B                Carte G Carte H
       (85%)                          (72%)
```

**Dimensionnement** : 30-60 cartes (open), 60-100 (closed). 15-30 participants (open), 30-50 (closed). 15-30 min par session.

---

## Tree Testing

Le tree testing valide la trouvabilite des contenus dans une structure de navigation. Formuler des taches realistes en langage utilisateur, eviter les mots-indices presents dans l'arborescence, 8-12 taches par test.

| Metrique | Seuil acceptable |
|---|---|
| **Task success rate** | > 70% |
| **Directness** (sans backtracking) | > 50% |
| **First click correctness** | > 60% (correle a > 80% de succes) |

**Outils** : Treejack (Optimal Workshop), UserZoom, Maze.

---

## Guerrilla Testing

```
Arbre de decision :
Sujet sensible ou confidentiel ?
+-- Oui --> NE PAS faire de guerrilla testing
+-- Non --> Prototype auto-porteur ?
    +-- Non --> NE PAS faire de guerrilla testing
    +-- Oui --> Besoin de participants specifiques ?
        +-- Oui --> NE PAS faire de guerrilla testing
        +-- Non --> Budget < 500 EUR ? --> GUERRILLA TESTING ADAPTE
```

**Setup** : cafes, coworking, conferences. Laptop/tablette avec prototype. 5-10 min par participant, 5-8 personnes. Incentive : un cafe (5-10 EUR). **Limites** : pas de controle du profil, environnement bruyant, pas de consentement formel (probleme RGPD), insights superficiels, non-adapte aux sujets complexes.

---

## Recrutement de Participants

### Screener

```
Structure :
+-- Qualification (criteres d'inclusion)
|   +-- Comportement, role, experience
+-- Disqualification (criteres d'exclusion)
|   +-- Professionnels UX/design, participation recente
+-- Diversite (variete de profils)
+-- Regles : ne pas reveler les "bonnes reponses", choix multiples, 8-12 questions max
```

### Incentives

| Etude | Duree | B2C | B2B |
|---|---|---|---|
| Survey | 5-10 min | 5-10 EUR | 10-20 EUR |
| Test non-modere | 10-15 min | 10-20 EUR | 20-40 EUR |
| Interview | 45-60 min | 30-80 EUR | 75-200 EUR |
| Diary study | 1-4 semaines | 100-250 EUR | 200-500 EUR |
| Contextual inquiry | 90-120 min | 80-150 EUR | 150-300 EUR |

### Panel et biais

**Gestion de panel** : viser 200-500 panelistes actifs, tagger par profil, rotation trimestrielle, suppression des inactifs, conformite RGPD (consentement explicite, droit de retrait, anonymisation).

| Biais | Contre-mesure |
|---|---|
| **Volontariat** (plus engages que la moyenne) | Comparer au profil de la base totale |
| **Familiarite** (deviennent "experts") | Max 2-3 etudes/an par participant |
| **Representativite** | Quotas par segment |
| **No-show** (15-25%) | Sur-recruter de 25-30%, rappels |

---

## State of the Art 2025-2026

### Outils IA

**Transcription et analyse automatisee** : Dovetail, Marvin, Notably et Condens integrent la transcription IA (precision > 95% FR/EN) et le codage thematique assiste, reduisant le temps d'analyse de 60-80%. Le chercheur passe du codage manuel a la curation des themes proposes par l'IA.

**Synthetic Users** : outils de simulation (Synthetic Users, User Evaluation) bases sur des LLM. Usage legitime : pre-tester un script, identifier les angles morts d'un protocole. Usage illegitime : remplacer les vrais participants. Les LLM ne reproduisent pas les comportements reels, les biais et les contextes individuels.

**Research Repository intelligent** : recherche semantique dans l'ensemble des insights (Dovetail, EnjoyHQ), detection automatique des patterns cross-etudes, synthese en langage naturel des insights existants.

### Maturation de la recherche a distance

| Dimension | Evolution 2025-2026 |
|---|---|
| **Outils** | Zoom/Teams (modere), Maze/UserTesting (non-modere) |
| **Qualite** | Equivalente au presentiel pour 80% des cas |
| **Limites** | Contexte physique, objets physiques, participants peu techno |
| **Hybrid** | Presentiel (contextual inquiry) + remote (interviews, tests) comme norme |
| **Global reach** | Recrutement international sans deplacement |

### Tendances emergentes

- **Recherche continue automatisee** : micro-surveys in-app declenchees par des evenements specifiques (abandon, premiere utilisation) remplacent les surveys ponctuels.
- **Analyse multimodale** : croisement automatique des donnees comportementales, declaratives et qualitatives dans un meme dashboard.
- **Research Ops** : role de Research Operations Manager generalise (recrutement, outils, gouvernance, RGPD, democratisation).
- **Ethique renforcee** : EU AI Act et RGPD imposent un processus de consentement, anonymisation et retention auditable et documente.
