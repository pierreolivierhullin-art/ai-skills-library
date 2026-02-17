# Analysis & Synthesis -- De l'Observation a l'Insight Actionnable

## Overview

Ce document de reference couvre les methodes et frameworks d'analyse et de synthese des donnees de recherche utilisateur : affinity mapping, analyse thematique (Braun & Clarke), atomic research (Tomer Sharon), creation de personas data-driven, empathy maps, journey mapping, service blueprinting, conception d'un research repository et communication des insights aux parties prenantes. Appliquer ces methodes systematiquement pour transformer les observations brutes en insights actionnables, eviter les biais de synthese et maximiser l'impact de la recherche sur les decisions produit.

---

## Affinity Mapping -- Du Post-It au Pattern

L'affinity mapping est une methode bottom-up de regroupement des donnees qualitatives. Elle fait emerger des themes et des patterns a partir d'observations individuelles sans imposer de structure prealable. Utiliser cette methode comme premier reflexe apres la collecte de donnees qualitatives.

### Processus en 5 etapes

**Etape 1 -- Externaliser les observations.** Transcrire chaque observation, citation ou comportement sur un post-it individuel. Une idee par post-it. Inclure le contexte : qui, quand, dans quelle situation. Bon : "P4 a cherche le bouton 'Annuler' pendant 15 secondes sans le trouver (ecran paiement)". Mauvais : "Probleme de navigation".

**Etape 2 -- Regrouper en clusters.** Deplacer les post-its pour former des groupes naturels. Ne pas definir les categories a l'avance. Travailler en silence pendant les 20 premieres minutes pour eviter le groupthink. Les post-its qui ne rentrent dans aucun groupe restent isoles.

**Etape 3 -- Nommer les themes.** Attribuer un label descriptif a chaque cluster. Preferer une formulation sous forme d'insight : "Les utilisateurs ne font pas confiance aux calculs automatiques" plutot que "Problemes de calcul".

**Etape 4 -- Identifier les hierarchies.** Regrouper les themes en 3-5 super-themes maximum. Chaque super-theme devient un axe strategique potentiel.

**Etape 5 -- Formuler les insights.** Transformer chaque theme en insight actionnable suivant la structure : Observation + Implication + Direction.

| Outil | Mode | Forces | Limites |
|---|---|---|---|
| **Miro / FigJam** | Collaboratif distant | Temps reel, templates, votes | Necessite formation |
| **Dovetail** | Analyse dediee | Tagging, recherche, repository | Cout (abonnement) |
| **Post-its physiques** | Presentiel | Tactile, rapide, inclusif | Pas de sauvegarde, espace |
| **Notion** | Documentation | Flexible, integrations | Pas optimise pour le clustering visuel |

Bonnes pratiques : impliquer 2-4 personnes dans le clustering. Compter un minimum de 50 notes (3-5 interviews generent 100-200 notes). Prevoir 2-3 heures. Ne pas eliminer les outliers : les observations isolees sont parfois les plus revelateurs.

---

## Thematic Analysis -- Methode de Braun & Clarke

L'analyse thematique (Braun & Clarke, 2006, revisee 2019) est le standard academique de codage et d'identification de patterns dans les donnees qualitatives. Elle se distingue de l'affinity mapping par sa systematicite et sa tracabilite.

### Les 6 phases

**Phase 1 -- Familiarisation.** Relire l'integralite des transcriptions et enregistrements. Prendre des notes initiales sans coder. Temps recommande : 1-2 heures par interview de 45 minutes.

**Phase 2 -- Codage initial.** Attribuer des codes descriptifs a chaque segment pertinent. Coder de maniere exhaustive. Un meme segment peut recevoir plusieurs codes.

| Type de code | Exemple d'extrait | Code |
|---|---|---|
| **Descriptif** | "Je regarde les avis avant d'acheter" | consultation-avis-pre-achat |
| **Interpretatif** | "Je regarde les avis avant d'acheter" | besoin-reassurance-sociale |
| **In vivo** | "C'est la jungle" | jungle-informationnelle |

**Phase 3 -- Generation des themes.** Regrouper les codes en themes potentiels. Un theme capture un pattern significatif en relation avec la question de recherche. Distinguer les themes des categories : un theme a un point de vue, une categorie est un simple classement.

**Phase 4 -- Revue des themes.** Verifier la coherence interne (les extraits partagent-ils un pattern commun ?) et la distinction externe (les themes sont-ils suffisamment differents ?). Fusionner, scinder ou abandonner les themes si necessaire.

**Phase 5 -- Definition et nommage.** Definir precisement ce que chaque theme capture. Choisir des noms evocateurs : "La confiance se construit par la preuve sociale" plutot que "Theme 3".

**Phase 6 -- Rapport.** Presenter chaque theme avec 2-3 citations cles, synthese des implications et recommandations. Le rapport doit convaincre un lecteur externe que les themes sont solidement ancres dans les donnees.

Criteres de qualite : les themes sont des patterns interpretatifs (pas des resumes de surface), les donnees sont codees exhaustivement (pas selectivement), les themes racontent une histoire coherente, l'analyse est transparente et tracable.

---

## Atomic Research -- Modele de Tomer Sharon

L'atomic research decompose les findings en unites atomiques reutilisables connectees dans un graphe de connaissances : `Experiments --> Facts --> Insights --> Recommendations`. Chaque unite est indexable, cherchable et recombinante.

**Niveau 1 -- Experiments** : l'etude (methode, participants, date, objectifs). Source de tracabilite.
**Niveau 2 -- Facts** : donnees brutes (citations verbatim, comportements observes). Objectifs et non interpretes.
**Niveau 3 -- Insights** : patterns identifies a travers plusieurs facts, souvent issus de plusieurs experiments.
**Niveau 4 -- Recommendations** : actions suggerees sur la base des insights, adressees a une equipe specifique.

### Systeme de tagging

| Dimension | Exemples de tags |
|---|---|
| **Persona / Segment** | admin, end-user, manager, nouveau-client, churned |
| **Produit / Feature** | onboarding, checkout, dashboard, search, notifications |
| **Phase du parcours** | decouverte, evaluation, achat, usage, support |
| **Type d'insight** | pain-point, besoin-non-satisfait, workaround, motivation, frein |
| **Criticite** | bloquant, important, mineur, opportunite |
| **Methode source** | interview, usability-test, survey, analytics, diary-study |

Saisir les nuggets dans les 24 heures. Un insight robuste requiert minimum 3 facts de 2 sources differentes. Reviser trimestriellement.

---

## Persona Creation -- Personas Data-Driven

Les personas sont des archetypes construits a partir de donnees reelles. Les personas fictives (inventees sans donnees) renforcent les biais internes au lieu de les corriger.

| Source | Type | Apport |
|---|---|---|
| **Interviews** | Qualitatif | Motivations, frustrations, modeles mentaux |
| **Surveys** | Quantitatif | Segmentation, frequences, preferences |
| **Analytics produit** | Quantitatif | Comportements reels, patterns d'usage |
| **CRM / support** | Mixte | Historique, tickets, raisons de churn |

**Methode de clustering :** (1) Identifier 5-10 variables discriminantes (frequence d'usage, objectif principal, expertise, taille d'organisation). (2) Croiser analyse thematique et donnees quantitatives pour identifier 3-5 groupes distincts. (3) Valider que chaque segment a des besoins suffisamment distincts. (4) Incarner chaque segment en persona narrative.

### Template de persona

```
PERSONA : [Nom] | Segment : [Label]
PROFIL : Role, contexte, expertise technique, frequence d'usage
OBJECTIFS (2-3) : [Objectifs lies au produit]
FRUSTRATIONS (2-3) : [Pain points avec citations verbatim]
COMPORTEMENTS : [Habitudes, outils, criteres de decision]
CITATION : "[Verbatim representatif]"
SCENARIO : [Paragraphe narratif d'usage type]
```

**Anti-patterns :** personas inventees sans donnees, personas purement demographiques (age/genre sans lien comportemental), plus de 5 personas (perte de pouvoir de priorisation), personas statiques jamais mises a jour, personas decoratives affichees au mur mais ignorees dans les decisions.

---

## Empathy Maps

L'empathy map capture l'experience d'un utilisateur selon 4 quadrants :

| Quadrant | Question cle | Sources |
|---|---|---|
| **Says** (Dit) | Quelles phrases emploie-t-il ? | Citations verbatim, feedback support |
| **Thinks** (Pense) | Quelles preoccupations internes ? | Inferences des hesitations, questions |
| **Does** (Fait) | Quels comportements observe-t-on ? | Tests d'utilisabilite, analytics, terrain |
| **Feels** (Ressent) | Quelles emotions ? | Ton de voix, expressions, declarations |

**Remplissage :** (1) Rassembler transcriptions et notes. (2) Extraire les elements par quadrant ("Thinks" et "Feels" sont des inferences : les etiqueter comme telles). (3) Identifier les contradictions Says/Does -- ce sont les insights les plus precieux. (4) Formuler 2-3 implications pour le design.

Utiliser en debut de projet pour aligner l'equipe, apres une serie d'interviews, en complement d'une persona, ou pendant un design sprint.

---

## Journey Mapping -- Cartographier l'Experience Complete

Le journey map visualise l'experience complete a travers toutes les etapes d'interaction. Il revele les points de friction et les opportunites que les analyses feature-par-feature ne capturent pas.

| Composant | Description | Exemple |
|---|---|---|
| **Etapes** | Phases macro du parcours | Decouverte, Evaluation, Achat, Onboarding, Usage, Support |
| **Actions** | Ce que l'utilisateur fait | Recherche Google, compare, cree un compte |
| **Points de contact** | Canaux et interfaces | Site web, email, app mobile, support chat |
| **Pensees** | Ce qu'il se dit | "Est-ce que ca vaut le prix ?" |
| **Emotions** | Etat emotionnel (courbe) | Curiosite, confusion, frustration, satisfaction |
| **Pain points** | Frictions et obstacles | Formulaire long, attente support, doc manquante |
| **Opportunites** | Ameliorations potentielles | Simplifier le formulaire, chat proactif |

**Construction :** (1) Definir le scope et les bornes du parcours. (2) Combiner donnees qualitatives et quantitatives. (3) Identifier 5-8 etapes macro (>10 = illisible). (4) Remplir chaque ligne a partir des donnees. (5) Tracer la courbe emotionnelle : les creux sont les zones prioritaires. (6) Prioriser les opportunites par impact et effort.

Regles : baser sur des donnees reelles, inclure les touchpoints hors-produit, creer un journey map par persona, mettre a jour semestriellement.

---

## Service Blueprinting -- Au-dela du Visible

Le service blueprint etend le journey map en ajoutant les couches internes de l'organisation. Il rend visible les processus, systemes et acteurs qui permettent (ou empechent) la delivrance du service.

```
COUCHE 1 -- Evidence physique (touchpoints visibles)
----------- Ligne d'interaction -----------
COUCHE 2 -- Actions client
----------- Ligne de visibilite -----------
COUCHE 3 -- Actions frontstage (visibles par le client : chat, appel)
----------- Ligne d'interaction interne -----------
COUCHE 4 -- Actions backstage (invisibles : traitement, verification)
COUCHE 5 -- Processus support (CRM, ERP, API, logistique)
```

| Situation | Outil recommande |
|---|---|
| Experience emotionnelle du client | Journey map |
| Pain points du parcours client | Journey map |
| Dysfonctionnements internes | Service blueprint |
| Coordination entre equipes | Service blueprint |
| Conception de nouveau service | Service blueprint |
| Reduction des couts operationnels | Service blueprint |

Commencer par le journey map, approfondir avec le blueprint pour les zones problematiques. Impliquer operations, support et IT. Identifier les "fail points" et les "wait points". Documenter les handoffs entre equipes.

---

## Research Repository Design

Un research repository centralise observations, insights, rapports et enregistrements dans un systeme organise et cherchable. Sans repository, les insights se perdent et l'equipe refait les memes etudes.

| Couche | Contenu | Acces |
|---|---|---|
| **Etudes** | Objectifs, methode, participants, raw data | Equipe research |
| **Observations** | Citations verbatim, comportements | Research + produit |
| **Insights** | Patterns, interpretations, preuves | Toute l'organisation |
| **Recommendations** | Actions, priorite, statut | Produit + leadership |
| **Assets** | Videos, personas, journey maps, rapports | Toute l'organisation |

**Taxonomie :** definir une taxonomie controlee (pas de tags libres). Categories : produit/feature, persona/segment, phase du parcours, methode, statut (nouveau/valide/archive/obsolete), impact (bloquant/significatif/mineur).

**Gouvernance :** designer un Repository Manager. Definir qui contribue (researchers) et qui consulte (tous). Instaurer une revue par les pairs avant publication. Archiver les insights >18 mois non revalides. Integrer la formation au repository dans l'onboarding.

| Outil | Forces | Cible |
|---|---|---|
| **Dovetail** | Analyse qualitative, tagging, highlights video | Equipes research dediees |
| **Notion** | Flexible, bases relationnelles, cout reduit | Equipes produit polyvalentes |
| **EnjoyHQ** | Centralisation multi-sources, full-text search | Forte maturite research |
| **Condens** | Repository structure, synthese assistee | Equipes research mid-size |

---

## Insight Communication -- Du Rapport au Changement

Un insight qui ne change pas une decision est un insight inutile. Adapter le format au public cible.

### Insight Brief Template

```
TITRE : [Pattern identifie]
EVIDENCE : [3 faits avec sources -- verbatim, analytics, survey]
IMPACT : [Qui ? Quelle ampleur ? Consequence si inaction ?]
RECOMMANDATION : [Action suggeree + niveau de confiance]
PROCHAINE ETAPE : [Owner, decision attendue, delai]
```

| Audience | Format | Frequence |
|---|---|---|
| **C-Level** | Executive summary 1 page, video highlights 2 min | Mensuel |
| **Product managers** | Insight briefs, workshops de priorisation | Hebdomadaire |
| **Design** | Empathy maps, journey maps, video clips | Continu |
| **Engineering** | Pain points techniques, scenarios d'usage | Par sprint |
| **Organisation** | Newsletter research, "insight of the week" | Bi-mensuel |

**Video highlights :** creer des compilations de 2-5 minutes des moments cles (frustrations, workarounds). Diffuser en sprint reviews et town halls. Outils : Dovetail, Lookback, Grain.

**Newsletter research :** (1) Insight principal avec contexte, (2) 2-3 findings secondaires en une phrase, (3) citation de la semaine, (4) etudes en cours, (5) appel a participation.

---

## From Insight to Action -- De l'Insight a l'Impact

### Priorisation des insights

| Critere | Score (1-5) |
|---|---|
| **Frequence** | 1 = rare, 5 = universel |
| **Severite** | 1 = mineur, 5 = bloquant |
| **Faisabilite** | 1 = tres complexe, 5 = quick win |
| **Confiance** | 1 = hypothese, 5 = sources convergentes |
| **Alignement strategique** | 1 = hors scope, 5 = priorite #1 |

**Lien backlog :** traduire chaque insight priorise en user story ou opportunity. Tagger les items avec la reference de l'insight source. Presenter les insights en sprint planning. Verifier en retrospective si l'action a produit l'effet attendu.

### Mesurer l'impact de la recherche

| Metrique | Description | Cible |
|---|---|---|
| **Insight-to-action rate** | % insights actiones en 90 jours | > 60% |
| **Time-to-action** | Delai moyen insight --> action | < 30 jours |
| **Research coverage** | % decisions majeures informees par la recherche | > 80% |
| **Stakeholder satisfaction** | Satisfaction PM/designers (survey interne) | > 4/5 |
| **Repository utilisation** | Consultations par non-researchers / mois | En augmentation |

---

## State of the Art (2025-2026)

### AI-Assisted Qualitative Analysis

**Auto-transcription et codage assiste.** Les outils (Otter.ai, Trint, Dovetail AI) atteignent 95%+ de precision. Les LLMs permettent un codage assiste : l'analyste fournit le codebook, le modele propose des codes que l'humain valide. Gain de temps : 40-60% sur la phase de codage.

**Detection automatique de patterns.** Les LLMs analysent un corpus de transcriptions et identifient themes emergents, sentiments et contradictions (Dovetail AI Insights, Notably, Marvin). Limite : tendance a sur-generaliser et produire des themes banals. Le jugement humain reste indispensable.

**Generation de syntheses.** Les LLMs generent des premieres versions de rapports, personas et journey maps. Utiliser comme point de depart, jamais comme resultat final. Verifier attributions, inferences causales et representativite.

### Tendances emergentes

**Continuous research platforms.** Les plateformes (Rally, Great Question, User Interviews) integrent recrutement, conduite, transcription, analyse et repository dans un workflow unique, permettant la recherche comme habitude plutot que comme projet.

**Research democratization at scale.** Les organisations matures passent de "only researchers do research" a "researchers enable everyone to learn from users". Le role du researcher evolue vers : methodologie, formation, qualite, etudes complexes.

**Synthesis repositories avec IA.** Les repositories de nouvelle generation suggerent des connexions entre insights, alertent sur les themes recurrents et generent des meta-analyses transversales.

**Ethical AI in research.** Enjeux emergents : consentement pour l'analyse IA des enregistrements, biais des modeles (sous-representation culturelle/linguistique), propriete des insights generes. Etablir une politique claire et en informer les participants.

---

## Common Pitfalls

**Piege 1 -- Confondre observation et insight.** Une observation est un fait ("5/8 participants n'ont pas trouve le bouton"). Un insight est un pattern interprete avec implication ("Les utilisateurs s'attendent a la recherche dans le header par convention e-commerce").

**Piege 2 -- Biais de confirmation.** Selectionner inconsciemment les donnees confirmantes. Contre-mesure : demander "Quelles donnees contredisent cette conclusion ?" et documenter les counter-evidence.

**Piege 3 -- Insight orphelin.** Insight sans owner ni prochaine etape. Chaque insight doit avoir un destinataire et une action definie avant communication.

**Piege 4 -- Repository fantome.** Outil sophistique que personne ne consulte. La valeur d'un repository est proportionnelle a son usage. Commencer simple, migrer quand le volume le justifie.

**Piege 5 -- Personas decoratives.** Personas encadrees au mur mais jamais invoquees dans les decisions. Integrer dans les rituels : "Pour quelle persona construisons-nous cette feature ?"

**Piege 6 -- Sur-confiance dans l'IA.** Deleguer l'analyse a un LLM sans verification. Les modeles produisent des syntheses fluides mais potentiellement incorrectes. L'IA accelere ; elle ne remplace pas le jugement critique.

---

## References

- Virginia Braun & Victoria Clarke, *Thematic Analysis: A Practical Guide* (2021)
- Tomer Sharon, *Validating Product Ideas Through Lean User Research* (2016)
- Jim Kalbach, *Mapping Experiences* (2nd ed., 2020)
- Nikki Anderson, *User Research in Practice* (2023)
- Erika Hall, *Just Enough Research* (2nd ed., 2019)
- Nielsen Norman Group -- https://www.nngroup.com/articles/affinity-diagram/
- Dovetail Research Repository -- https://dovetail.com
- Atomic Research -- https://blog.prototypr.io/atomic-research
