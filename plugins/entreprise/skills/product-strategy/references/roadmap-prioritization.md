# Roadmap & Prioritization -- Frameworks, Formats & Communication

## Overview

Ce document de reference couvre les frameworks de priorisation produit (RICE, ICE, Kano, Opportunity Score, WSJF, Weighted Scoring), les formats de roadmap (Now/Next/Later, outcome-based, theme-based, timeline-based, Shape Up), les strategies de communication selon les audiences (board, stakeholders, equipe, clients) et les anti-patterns courants. Utiliser ce guide pour structurer les decisions de priorisation, construire des roadmaps actionnables et communiquer la strategie produit de maniere adaptee a chaque interlocuteur.

---

## RICE Framework

Le framework RICE, developpe par Intercom, evalue chaque initiative sur 4 dimensions. **Formule** : RICE = (Reach x Impact x Confidence) / Effort

| Composante | Definition | Unite | Calibration |
|---|---|---|---|
| **Reach** | Utilisateurs/clients impactes par periode | Utilisateurs/trimestre | Donnees analytics, cohortes |
| **Impact** | Contribution a l'objectif vise | Score 0.25 a 3 | 3=massif, 2=fort, 1=moyen, 0.5=faible, 0.25=minimal |
| **Confidence** | Certitude des estimations | Pourcentage | 100%=donnees solides, 80%=intuition forte, 50%=pari, 20%=speculation |
| **Effort** | Travail en personne-mois | Personne-mois | Engineering + design + QA |

#### Tables de calibration

| Impact | Description | Exemple |
|---|---|---|
| 3 (massif) | Transforme l'experience, impact sur la North Star metric | Refonte onboarding reduisant le time-to-value de 70% |
| 2 (fort) | Amelioration significative d'un workflow cle | Mode collaboratif temps reel |
| 1 (moyen) | Amelioration notable mais non transformatrice | Filtres avances dans la recherche |
| 0.5 (faible) | Nice-to-have | Amelioration design d'une page secondaire |
| 0.25 (minimal) | Changement a peine perceptible | Correction d'un label textuel |

| Confidence | Bases de l'estimation |
|---|---|
| 100% (haute) | Donnees quantitatives solides (A/B tests, analytics, interviews n>30) |
| 80% (bonne) | Donnees qualitatives convergentes (interviews n>10, feedback support) |
| 50% (moyenne) | Intuition informee, quelques signaux sans validation rigoureuse |
| 20% (basse) | Speculation pure, hypothese non testee |

#### Exemple de scoring RICE

```
Feature A : Onboarding personnalise par IA
  Reach       = 5 000 utilisateurs/trimestre
  Impact      = 2 (fort)
  Confidence  = 80%
  Effort      = 3 personne-mois
  RICE Score  = (5000 x 2 x 0.8) / 3 = 2 667

Feature B : Export CSV avance
  Reach       = 800 utilisateurs/trimestre
  Impact      = 1 (moyen)
  Confidence  = 100%
  Effort      = 0.5 personne-mois
  RICE Score  = (800 x 1 x 1.0) / 0.5 = 1 600

Feature C : Integration Salesforce native
  Reach       = 2 000 utilisateurs/trimestre
  Impact      = 3 (massif)
  Confidence  = 50%
  Effort      = 4 personne-mois
  RICE Score  = (2000 x 3 x 0.5) / 4 = 750

Priorite : A > B > C
```

**Limites** : le Reach biaise vers les fonctionnalites grand public au detriment du strategique enterprise ; l'Impact reste subjectif malgre la calibration ; ne capture pas les dependances techniques ni les couts d'opportunite ; necessite une discipline de recalibration trimestrielle pour eviter la derive des scores.

---

## ICE Framework

Le framework ICE simplifie le RICE en 3 dimensions scorees de 1 a 10. **Formule** : ICE = Impact x Confidence x Ease

| Composante | Definition | Echelle |
|---|---|---|
| **Impact** | Effet sur l'objectif cible | 1 (negligeable) a 10 (transformateur) |
| **Confidence** | Certitude de l'estimation | 1 (speculation) a 10 (certitude) |
| **Ease** | Facilite d'implementation (inverse de l'effort) | 1 (tres difficile) a 10 (trivial) |

```
RICE vs ICE -- Arbre de decision
+-- Donnees de Reach fiables (analytics, cohortes) ?
|   +-- OUI : RICE (le Reach apporte la rigueur quantitative)
|   +-- NON : Plus de 20 items a trier ?
|       +-- OUI : ICE (scoring rapide, suffisant pour un premier tri)
|       +-- NON : RICE avec estimations de Reach qualitatives
+-- Aligner des stakeholders non-techniques ?
    +-- OUI : ICE (plus simple a expliquer)
    +-- NON : RICE (plus rigoureux)
```

---

## Kano Model

Le modele Kano classe les fonctionnalites selon leur impact sur la satisfaction client.

| Categorie | Effet si absent | Effet si present | Strategie |
|---|---|---|---|
| **Must-be** (indispensable) | Forte insatisfaction | Pas de satisfaction supplementaire | Couvrir systematiquement, cout d'entree du marche |
| **Performance** (proportionnel) | Insatisfaction proportionnelle | Satisfaction proportionnelle | Investir selon le positionnement concurrentiel |
| **Attractive** (delighter) | Aucune insatisfaction | Forte satisfaction, effet wow | Investir pour la differenciation |
| **Indifferent** | Aucun effet | Aucun effet | Eliminer du backlog |
| **Reverse** (inverse) | Satisfaction (prefere l'absence) | Insatisfaction (la presence gene) | Eviter ou rendre desactivable |

#### Methode de survey Kano

Pour chaque fonctionnalite, poser deux questions : (1) Question fonctionnelle : "Si cette fonctionnalite est presente, que ressentez-vous ?" et (2) Question dysfonctionnelle : "Si absente, que ressentez-vous ?". Reponses : J'aime / Je m'y attends / Neutre / Je tolere / Ca me deplait.

| | Dysf: J'aime | Dysf: Attends | Dysf: Neutre | Dysf: Tolere | Dysf: Deplait |
|---|---|---|---|---|---|
| **Fonc: J'aime** | Questionnable | Attractive | Attractive | Attractive | Performance |
| **Fonc: Attends** | Reverse | Indifferent | Indifferent | Indifferent | Must-be |
| **Fonc: Neutre** | Reverse | Indifferent | Indifferent | Indifferent | Must-be |
| **Fonc: Tolere** | Reverse | Indifferent | Indifferent | Indifferent | Must-be |
| **Fonc: Deplait** | Reverse | Reverse | Reverse | Reverse | Questionnable |

**Analyse** : collecter minimum 30-50 repondants par segment. Calculer le coefficient de satisfaction CS+ = (Attractive+Performance)/(A+P+M+I) et le coefficient d'insatisfaction CS- = (Must-be+Performance)/(A+P+M+I) x (-1). Les categories evoluent dans le temps (Attractive --> Performance --> Must-be). Refaire l'analyse annuellement.

---

## Opportunity Score

Developpe par Anthony Ulwick (Outcome-Driven Innovation). Identifie les fonctionnalites ou l'ecart importance/satisfaction est maximal.

**Formule** : Opportunity Score = Importance + max(Importance - Satisfaction, 0)

Collecter aupres des utilisateurs l'importance (1-10) et la satisfaction actuelle (1-10) pour chaque outcome formule en job-to-be-done.

| Zone | Importance | Satisfaction | Score | Action |
|---|---|---|---|---|
| **Sur-opportunite** | >7 | <5 | >12 | Investir prioritairement |
| **Bien servie** | >7 | >7 | 7-10 | Maintenir, pas de sur-investissement |
| **Sur-servie** | <5 | >7 | <5 | Reduire l'investissement |
| **Indifferente** | <5 | <5 | 5-7 | Ignorer |

---

## WSJF / Cost of Delay (contexte SAFe)

Le Weighted Shortest Job First est le framework de priorisation SAFe. **Formule** : WSJF = Cost of Delay / Job Size

Le Cost of Delay se decompose en 3 elements scores de 1 a 21 (Fibonacci : 1, 2, 3, 5, 8, 13, 21) :

| Composante | Definition | Questions cles |
|---|---|---|
| **User-Business Value** | Valeur pour les utilisateurs ou le business | Quel revenu/economie ? Quel impact retention ? |
| **Time Criticality** | Urgence, fenetre d'opportunite | Deadline reglementaire ? La valeur diminue-t-elle avec le temps ? |
| **Risk Reduction** | Reduction de risque ou deblocage d'opportunites | Risque technique/business reduit ? Autres initiatives debloquees ? |

#### Exemple de calcul WSJF

```
Feature X : Module de conformite DORA
  User-Business Value   = 13  (obligation reglementaire, risque de sanction)
  Time Criticality      = 21  (deadline reglementaire en Q2)
  Risk Reduction        = 8   (debloque l'entree sur le marche bancaire)
  Cost of Delay         = 42
  Job Size              = 8
  WSJF                  = 42 / 8 = 5.25

Feature Y : Dashboard analytics v2
  User-Business Value   = 8   (demande forte des enterprise clients)
  Time Criticality      = 3   (pas de deadline, valeur stable dans le temps)
  Risk Reduction        = 2   (pas de risque associe)
  Cost of Delay         = 13
  Job Size              = 5
  WSJF                  = 13 / 5 = 2.6

Priorite : Feature X (WSJF 5.25) avant Feature Y (WSJF 2.6)
```

**Pieges** : scorer en relatif (comparer les features entre elles) ; forcer la differenciation des scores ; recalculer a chaque PI Planning car la Time Criticality evolue.

---

## Weighted Scoring Model

Criteres de priorisation personnalises avec ponderation refletant les priorites strategiques.

1. Definir 4-7 criteres alignes sur la strategie (valeur client, revenu, alignement strategique, effort, risque).
2. Ponderer chaque critere (total = 100%), valider avec les stakeholders.
3. Scorer chaque initiative de 1 a 5 par critere.
4. Score pondere = somme (score x poids).

| Critere | Poids | Feature A | Feature B | Feature C |
|---|---|---|---|---|
| Valeur client | 30% | 4 (1.2) | 5 (1.5) | 3 (0.9) |
| Revenu potentiel | 25% | 3 (0.75) | 4 (1.0) | 5 (1.25) |
| Alignement strategique | 20% | 5 (1.0) | 3 (0.6) | 4 (0.8) |
| Facilite technique | 15% | 2 (0.3) | 4 (0.6) | 3 (0.45) |
| Reduction de risque | 10% | 4 (0.4) | 2 (0.2) | 3 (0.3) |
| **Score total** | **100%** | **3.65** | **3.90** | **3.70** |

```
Choix du framework de priorisation -- Arbre de decision
+-- Contexte SAFe / organisation a l'echelle ?
|   +-- OUI : WSJF (standard SAFe, Cost of Delay natif)
|   +-- NON
|       +-- Donnees quantitatives de Reach disponibles ?
|       |   +-- OUI : RICE
|       |   +-- NON
|       |       +-- Plus de 20 items a trier rapidement ?
|       |           +-- OUI : ICE (scoring rapide)
|       |           +-- NON : Weighted Scoring (personnalisation maximale)
+-- Besoin de comprendre la satisfaction client ?
    +-- OUI : Coupler avec Kano ou Opportunity Score
    +-- NON : Le framework principal suffit
```

---

## Formats de Roadmap

| Format | Horizon | Audience | Force | Faiblesse |
|---|---|---|---|---|
| **Now/Next/Later** | 3-12 mois | Equipe, stakeholders | Flexibilite, pas d'engagement dates | Manque de precision temporelle |
| **Outcome-based** | 6-18 mois | Board, leadership | Aligne sur la valeur | Difficulte de lien avec les travaux concrets |
| **Theme-based** | 6-12 mois | Stakeholders, clients enterprise | Lisibilite strategique | Risque de themes trop vagues |
| **Timeline-based** | 3-12 mois | Engineering, PMO | Precision, engagement visible | Rigidite, faux sentiment de certitude |
| **Shape Up** | 6 semaines | Equipe produit/engineering | Focus intense, pas de backlog | Rupture culturelle |

**Now/Next/Later** : Now (0-6 sem, initiatives commitees, haute confiance, 3-5 max), Next (6-12 sem, validees en preparation, confiance moyenne), Later (3-12 mois, opportunites non engagees, faible confiance). Reviser mensuellement les mouvements entre colonnes. Le Later est un reservoir d'opportunites, pas un backlog exhaustif.

**Outcome-based** : organise autour des resultats a atteindre plutot que des features a livrer. Structure : Objectif strategique --> Outcome mesurable --> Initiatives candidates.

```
Objectif : Accelerer l'adoption produit
+-- Outcome 1 : Reduire le time-to-value de 14j a 3j
|   +-- Initiative : Onboarding personnalise par IA
|   +-- Initiative : Templates pre-configures par secteur
+-- Outcome 2 : Augmenter le taux d'activation de 35% a 55%
|   +-- Initiative : Checklist interactive de prise en main
|   +-- Initiative : Notifications contextuelles in-app
+-- Outcome 3 : Reduire le churn M3 de 12% a 7%
    +-- Initiative : Programme customer success proactif
    +-- Initiative : Feature discovery assistant
```

**Theme-based** : regroupe par axe strategique sur 2-4 trimestres. 3-5 themes max par semestre. Chaque theme a un sponsor, un budget et des metriques de succes. Les themes derivent directement de la strategie produit.

**Timeline-based** : uniquement quand les dates sont contractuellement necessaires (engagements enterprise, obligations reglementaires, lancement marketing coordonne). Toujours representer l'incertitude : barres de confiance, zones grises pour les horizons lointains.

---

## Shape Up Method

Methode Basecamp (Ryan Singer), alternative a Scrum : cycles de 6 semaines + 2 semaines de cooldown.

| Phase | Duree | Activite | Participants |
|---|---|---|---|
| **Shaping** | Continu (hors cycle) | Definir probleme, concevoir solution au bon niveau d'abstraction | Senior PM/designer/engineer |
| **Betting Table** | 1-2h (entre cycles) | Selectionner les pitches pour le prochain cycle | Leadership produit, CTO |
| **Building** | 6 semaines | Implementation autonome | Equipes de 2-3 (designer + dev) |
| **Cooldown** | 2 semaines | Bugs, projets personnels, exploration | Toute l'equipe |

**Appetit** : budget de temps maximum qu'on est pret a investir. L'inverse de l'estimation : au lieu de "combien de temps faut-il ?", on demande "combien de temps est-ce que ca vaut ?". Small Batch (1-2 sem) ou Big Batch (6 sem). Si le probleme ne rentre pas dans l'appetit, reduire le scope.

**Le Pitch** : document soumis a la betting table. Structure : Problem (quel probleme, pour qui, evidence), Appetite (small ou big batch), Solution (fat marker sketches, breadboarding), Rabbit Holes (risques identifies), No-Gos (exclusions explicites).

**Betting Table** : pas de backlog (pitches non retenus abandonnes), decision binaire (accepte ou rejete), engagement ferme (6 semaines d'autonomie sans interruption).

---

## Roadmap Communication

| Audience | Veut savoir | Format | Frequence | Piege |
|---|---|---|---|---|
| **Board** | Impact business, ROI, risques | Outcome-based, 3-5 themes | Trimestrielle | Trop de details techniques |
| **Stakeholders** | Quand leurs demandes arrivent, dependencies | Theme-based ou Now/Next/Later | Mensuelle | Promettre des dates fermes |
| **Equipe** | Quoi, pourquoi, ordre, contraintes | Now/Next/Later detaille | Hebdomadaire | Imposer des solutions sans le pourquoi |
| **Clients** | Direction du produit, fonctionnalites cles | Roadmap publique par themes | Trimestrielle | Engagements de dates |

**Regles** : (1) distinguer engagement ("nous travaillons sur X") et intention ("nous explorons Y") ; (2) communiquer le pourquoi avant le quoi ; (3) dates uniquement pour le Now, horizons ("T2 2026") pour Next/Later ; (4) documenter les renoncements explicitement ; (5) maintenir un changelog de la roadmap.

**Roadmap publique** : outil dedie (Productboard, Canny, GitHub Discussions), organiser par themes/outcomes, permettre le vote, mise a jour trimestrielle, jamais de dates de livraison.

---

## Roadmap Anti-Patterns

### Anti-pattern 1 -- La roadmap feature-factory

**Symptome** : la roadmap est une liste de features sans lien avec les outcomes business. L'equipe produit devient une usine a fonctionnalites pilotee par les demandes stakeholders. Pas de mesure d'impact, pas de validation des hypotheses, accumulation de complexite produit.

**Remede** : reformuler chaque feature en outcome mesurable. Remplacer "Ajouter un export PDF" par "Permettre aux utilisateurs de partager leurs rapports avec des non-utilisateurs (metrique : taux de partage >15%)".

### Anti-pattern 2 -- La roadmap calendar-driven

**Symptome** : diagramme de Gantt avec dates fixes imposees par le management ou les commerciaux. Les dates sont annoncees aux clients avant meme que l'equipe ait estime le travail. Qualite sacrifiee pour tenir les dates, burnout.

**Remede** : adopter un format Now/Next/Later ou outcome-based. Si des dates sont necessaires (contrainte reglementaire, evenement marche), fixer la date et rendre le scope variable.

### Anti-pattern 3 -- Le stakeholder-driven backlog

**Symptome** : le backlog est une concatenation des demandes de chaque stakeholder interne. Le Product Owner ne priorise pas, il arbitre politiquement. Roadmap incoherente, fonctionnalites disparates.

**Remede** : mettre en place un framework de priorisation transparent (RICE, WSJF). Publier les criteres et les scores. Organiser des sessions de priorisation collaborative ou les stakeholders voient le processus.

### Anti-pattern 4 -- La roadmap confidentielle

**Symptome** : partagee uniquement avec le COMEX. L'equipe engineering ne connait pas la vision a 6 mois. Decisions techniques a courte vue, alignement impossible.

**Remede** : publier en interne (tous les collaborateurs) et en externe (version adaptee clients). La transparence cree l'alignement et la confiance.

### Anti-pattern 5 -- L'absence de renoncement

**Symptome** : tout est prioritaire. Le backlog croit indefiniment, jamais de suppressions ni de reports explicites. Equipes dispersees sur trop de sujets.

**Remede** : pour chaque initiative ajoutee, une initiative retiree ou reportee. Documenter explicitement les renoncements et les communiquer.

---

## State of the Art (2025-2026)

### AI-Assisted Prioritization

- **Scoring automatique** : Productboard, Aha!, Airfocus integrent des modeles IA analysant feedback client, tickets support et entretiens pour generer des scores suggestifs. Le PM reste decisionnaire.
- **Clustering de feedback** : les LLMs regroupent les retours clients en themes, identifiant les patterns que l'analyse manuelle manquerait (Productboard AI, Dovetail).
- **Predictive impact modeling** : modeles entraines sur les donnees historiques (adoption, retention, engagement) pour predire l'impact d'une fonctionnalite avant developpement.
- **Opportunity detection** : analyse croisee donnees produit, tendances marche et signaux concurrentiels.

**Limites** : l'IA ne remplace pas la vision strategique ; les modeles reproduisent les biais des donnees (sur-representation des utilisateurs vocaux) ; la priorisation reste un jugement humain.

### Continuous Roadmapping

- **Dual-track continu** (Teresa Torres) : discovery et delivery en parallele permanent, insights alimentant la roadmap en temps reel.
- **Roadmap-as-code** : versioning Git, pull requests pour les changements, tracabilite et debat structure.
- **Real-time stakeholder sync** : suivi d'avancement en temps reel reduisant les presentations formelles.

### Outils de roadmapping

| Outil | Forces | Ideal pour |
|---|---|---|
| **Productboard** | IA clustering feedback, portail client | B2B SaaS data-driven |
| **Aha!** | Strategie-to-delivery, reporting enterprise | Grandes organisations, PMO |
| **Airfocus** | Scoring modulaire (RICE, WSJF, custom) | Equipes cherchant la flexibilite |
| **Linear** | Rapidite, roadmap integree au backlog | Startups et scale-ups tech |
| **Jira Product Discovery** | Integration native Jira, scoring | Ecosysteme Atlassian |

### Tendances emergentes

- **Outcome-based funding** : financement lie aux outcomes mesures, pas au nombre de features. Points Go/No-Go a mi-parcours.
- **Product Operations** : industrialisation des processus de priorisation, standardisation des frameworks, coherence des donnees cross-equipes.
- **Strategy deployment via OKR** : alignement strategie-OKR-roadmap comme standard. OKR trimestriels alimentant directement les decisions de priorisation.
- **Carbon-aware roadmapping** : impact environnemental comme critere de priorisation pour les entreprises soumises a la CSRD.
