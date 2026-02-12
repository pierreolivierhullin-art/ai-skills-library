# Data Culture — Democratization, Champions & Organizational Maturity

## Overview

Ce document de reference couvre la dimension organisationnelle de la data literacy : comment construire, mesurer et faire evoluer une culture data-driven a l'echelle d'une organisation entiere. La technologie et les competences individuelles sont necessaires mais insuffisantes — sans une culture qui valorise les donnees, qui soutient leur utilisation et qui tolere l'experimentation, les investissements data restent sous-exploites. Utiliser ce guide pour concevoir et piloter des programmes de transformation data culture, du diagnostic initial a la mesure de maturite en passant par les mecanismes de changement.

This reference covers the organizational dimension of data literacy: how to build, measure, and evolve a data-driven culture across an entire organization. Technology and individual skills are necessary but insufficient — without a culture that values data, supports its use, and tolerates experimentation, data investments remain underutilized. Use this guide to design and run data culture transformation programs.

---

## Data Democratization Programs

### Principes fondamentaux de la democratisation

**Definition operationnelle** : la data democratization est le processus qui rend les donnees accessibles, comprehensibles et utilisables par tous les collaborateurs habilites, sans dependre systematiquement d'une equipe data centrale pour chaque question. L'objectif n'est pas de rendre tout le monde data scientist, mais de reduire le temps entre une question business et une reponse fondee sur les donnees.

**Les trois piliers de la democratisation** :

1. **Acces** : les bonnes personnes ont acces aux bonnes donnees au bon moment. Cela implique :
   - Un catalogue de donnees navigable et maintenu (data catalog) avec descriptions metier, pas seulement techniques.
   - Des niveaux d'acces granulaires bases sur les roles et les besoins (RBAC — Role-Based Access Control).
   - Des donnees disponibles dans des outils accessibles (BI tools, spreadsheets, APIs) et pas seulement dans des bases techniques.
   - Une latence de mise a disposition acceptable : les donnees disponibles a J+1 pour les analyses strategiques, en temps reel pour les operations.

2. **Comprehension** : les donnees sont comprehensibles sans expertise technique. Cela implique :
   - Un glossaire metier (business glossary) definissant chaque metrique, dimension et KPI en langage courant.
   - Des semantic layers qui traduisent les tables techniques en concepts metier (ex : "Revenue" au lieu de "sum(line_items.amount * line_items.quantity) WHERE status != 'cancelled'").
   - Des metadata enrichies : description, owner, fraicheur, qualite, lignage (lineage).
   - Une documentation des calculs et definitions accessible depuis les outils BI (infobulle, lien vers le glossaire).

3. **Confiance** : les utilisateurs font confiance aux donnees qu'ils consultent. Cela implique :
   - Des indicateurs de qualite visibles (data quality scores, freshness indicators).
   - Un processus de certification des datasets et des rapports (certified vs non-certified).
   - Une gestion proactive des incidents de qualite de donnees (data quality alerts, SLAs sur la fraicheur).
   - Un canal de signalement des anomalies accessible a tous les utilisateurs.

### Anti-patterns de la democratisation

- **Open Bar sans gouvernance** : rendre toutes les donnees accessibles a tous sans controle produit confusion, interpretations erronees, et risques de confidentialite. La democratisation n'est pas l'absence de regles.
- **Data Swamp** : un data lake sans catalogage, sans documentation, sans qualite. Les utilisateurs trouvent des donnees mais ne leur font pas confiance et ne comprennent pas leur signification.
- **Shadow Analytics** : quand le self-service est mal gouverne, des analystes non-formes creent des rapports incorrects qui prennent une vie propre dans l'organisation. Ces "sources alternatives de verite" sont destructrices.
- **Training-then-Forget** : former les utilisateurs une fois et ne jamais assurer le suivi. Sans pratique continue, support et reinforcement, les competences acquises disparaissent en quelques mois.

---

## Self-Service Analytics Enablement

### Architecture du self-service

**Le modele a 3 couches** :

Couche 1 — Governed Data Layer (equipe data) :
- Sources de donnees integrees, nettoyees, documentees.
- Modele de donnees semantique (semantic layer / metrics layer).
- Definitions de metriques certifiees et versionnees.
- Rafraichissement automatise avec monitoring de qualite.
- Responsabilite : equipe data engineering / analytics engineering.

Couche 2 — Curated Content Layer (analystes data + equipe data) :
- Dashboards certifies de reference (golden dashboards).
- Rapports periodiques automatises.
- Templates de visualisation conformes aux standards.
- Datasets precomputes pour les cas d'usage recurrents (data marts, cubes OLAP).
- Responsabilite : analystes data embedes dans les equipes metier.

Couche 3 — Self-Service Exploration Layer (utilisateurs metier) :
- Exploration ad hoc sur les datasets gouvernes.
- Dashboards personnels non certifies (clairement marques comme tels).
- Export de donnees pour analyse dans des spreadsheets.
- Requetes en langage naturel (NLQ — Natural Language Query) avec les nouveaux outils IA.
- Responsabilite : utilisateurs metier formes, avec support disponible.

### La semantic layer — pilier technique du self-service

La semantic layer est la couche d'abstraction qui traduit les tables techniques en concepts metier. Elle est le pilier technique indispensable du self-service reussi :

**Fonctions de la semantic layer** :
- **Definitions uniques** : chaque metrique est definie une seule fois (single source of truth). "Revenue" est calculee de la meme maniere partout.
- **Gouvernance centralisee** : les modifications de definitions sont versionees, approuvees et tracees.
- **Accessibilite** : les utilisateurs explorent des concepts metier ("Revenue par segment par mois") sans ecrire de SQL.
- **Performance** : les aggregations sont pre-calculees ou optimisees par la couche semantique.

**Outils de semantic layer modernes** :
- **dbt Metrics / MetricFlow** : definitions de metriques dans le code (metrics-as-code), integre avec dbt.
- **Cube.dev** : semantic layer headless, API-first, supporte plusieurs BI tools en frontend.
- **Looker (LookML)** : semantic layer native dans Looker, tres mature.
- **AtScale** : semantic layer enterprise, compatible avec les outils BI existants (Tableau, Power BI, Excel).
- **Power BI Datasets / Tabular Models** : semantic layer native dans l'ecosysteme Microsoft (DAX + relationships).

### Gouvernance du self-service

Equilibrer liberte et controle avec ces mecanismes :

- **Certification des contenus** : distinguer les dashboards et datasets certifies (gouvernes, valides) des contenus self-service (personnels, non garantis). Utiliser un badge visuel clair (ex : badge "Certified" dans Tableau, "Endorsed" dans Power BI).
- **Usage analytics** : monitorer l'utilisation des contenus. Identifier les dashboards les plus consultes (a certifier en priorite), les contenus abandonnes (a archiver), et les signaux de shadow analytics.
- **Review process** : quand un dashboard self-service devient largement utilise, le soumettre a une revue (viz review) et le promouvoir en contenu certifie ou le corriger.
- **Guardrails techniques** : limiter l'acces aux donnees brutes sensibles, restreindre les exports de donnees personnelles, mettre des quotas sur les requetes lourdes.
- **Feedback loop** : un canal (Slack, formulaire, JIRA) pour que les utilisateurs signalent des problemes de donnees, demandent de nouvelles metriques, ou proposent des ameliorations.

---

## Data Champions & Ambassadors

### Le role du Data Champion

Un data champion est un collaborateur ancre dans une equipe metier (pas dans l'equipe data) qui sert de pont entre les experts data et les utilisateurs metier. C'est le role le plus important et le plus sous-estime de la transformation data.

**Mission du data champion** :
- **Traduire** : convertir les besoins metier en questions data et les insights data en recommandations metier.
- **Former** : animer des sessions de formation et de mentorat pour son equipe.
- **Promouvoir** : evangeliser l'utilisation des donnees et des outils self-service.
- **Faire remonter** : signaler les problemes de qualite, les besoins non couverts, les frictions des outils.
- **Standardiser** : veiller au respect des conventions de visualisation et de communication data.

**Profil ideal** :
- Expertise metier forte (credibilite aupres de ses pairs).
- Curiosite pour les donnees et aisance avec les outils BI.
- Competences de communication et de pedagogie.
- Influence informelle dans son equipe (pas necessairement un manager).
- Volonte de consacrer 10-20% de son temps a ce role.

### Programme Data Champions — Mise en oeuvre

**Phase 1 — Identification (Semaines 1-4)**
- Envoyer un appel a volontaires (ne pas designer — les volontaires sont plus efficaces).
- Identifier les "super-utilisateurs" naturels des outils data (les personnes que les collegues consultent deja informellement).
- Viser 1 champion pour 20-50 collaborateurs dans chaque departement.
- Valider le soutien du management de chaque champion (allocation de 10-20% du temps).

**Phase 2 — Formation avancee (Semaines 5-12)**
- Formation intensive aux outils de self-service analytics (au-dela du niveau utilisateur standard).
- Formation a la pensee statistique et aux biais courants.
- Formation au data storytelling et a la communication d'insights.
- Ateliers pratiques sur les cas d'usage de leur departement.
- Introduction au data governance framework de l'organisation.

**Phase 3 — Activation (Mois 3-6)**
- Chaque champion cree ou ameliore un dashboard de reference pour son equipe.
- Animation d'une premiere "data clinic" dans son departement.
- Participation aux revues de visualisation inter-departements.
- Contribution au glossaire metier pour les termes de son domaine.
- Buddy system : chaque champion est en binome avec un analyste data pour le support.

**Phase 4 — Communaute et perennisation (Mois 6+)**
- Meetups mensuels de la communaute de champions (partage de bonnes pratiques, retours d'experience).
- Channel Slack dedie avec l'equipe data pour le support rapide.
- Reconnaissance formelle : integration dans les objectifs individuels, mention lors des town halls, certification interne.
- Rotation : encourager le renouvellement (certains champions evoluent vers des roles data, d'autres passent le relais).
- Mesure d'impact : chaque champion documente les cas d'usage resolus et les gains obtenus.

### Roles complementaires dans l'ecosysteme data

| Role | Positionnement | Responsabilite principale |
|---|---|---|
| **Data Champion** | Dans l'equipe metier | Pont entre data et metier, formation locale, adoption |
| **Embedded Analyst** | Dans l'equipe metier, reporte a la data team | Analyses complexes, dashboards certifies, support technique |
| **Analytics Engineer** | Dans l'equipe data | Modelisation de donnees, semantic layer, qualite |
| **Data Steward** | Dans l'equipe metier ou data governance | Qualite des donnees, definitions metier, conformite |
| **Data Product Owner** | Dans l'equipe data | Priorisation des produits data, roadmap, satisfaction utilisateurs |

---

## Training Programs & Upskilling

### Architecture du programme de formation

**Niveau 1 — Data Foundations (tout l'effectif)**
- Duree : 4 heures (2 sessions de 2h ou e-learning)
- Contenu :
  - Pourquoi les donnees comptent (exemples concrets dans l'industrie de l'organisation).
  - Lire un dashboard : axes, echelles, filtres, drill-down.
  - Les pieges courants : correlation vs causalite, biais du survivant, axes tronques.
  - Naviguer dans les outils de l'organisation (ou trouver quoi, a qui demander).
  - Exercice pratique : interpreter 3 graphiques reels de l'organisation.
- Evaluation : quiz de 10 questions + exercice d'interpretation.
- Cible : 100% des collaborateurs dans les 12 premiers mois.

**Niveau 2 — Data Communication (managers et fonctions analytiques)**
- Duree : 8 heures (2 jours demi-journees ou e-learning)
- Contenu :
  - Choisir le bon type de graphique (matrice de selection).
  - Principes de design visuel (Tufte, Few, Knaflic).
  - Structurer une communication data (arc narratif, Big Idea, SCQA).
  - Construire un dashboard simple dans l'outil de l'organisation.
  - Exercice pratique : transformer une analyse brute en executive summary.
- Evaluation : projet — creer un dashboard et le presenter a un jury.
- Cible : tous les managers et fonctions analytiques dans les 18 premiers mois.

**Niveau 3 — Data Analysis (analystes metier et futurs champions)**
- Duree : 24 heures (6 demi-journees sur 3 mois)
- Contenu :
  - SQL fondamental pour l'exploration de donnees.
  - Pensee statistique avancee (tests d'hypotheses, intervalles de confiance, taille d'echantillon).
  - Analyse exploratoire de donnees (EDA) avec les outils de l'organisation.
  - Data storytelling avance (narratif complexe, multi-audience).
  - Introduction a l'A/B testing et a la prise de decision experimentale.
  - Projet fil rouge : analyse complete d'un cas d'usage reel de bout en bout.
- Evaluation : soutenance du projet devant un jury data + metier.
- Cible : 2-5 personnes par departement, candidats data champions.

**Niveau 4 — Data Leadership (data champions et sponsors executifs)**
- Duree : 16 heures (4 demi-journees sur 2 mois)
- Contenu :
  - Gouvernance des donnees : principes, roles, outils.
  - Evangelisation et conduite du changement.
  - Mesure de la data culture et ROI des initiatives data.
  - Ethique des donnees et communication responsable.
  - Facilitation de data clinics et de revues de visualisation.
  - Strategie self-service : quand centraliser, quand democratiser.
- Evaluation : plan d'action de data culture pour son departement.
- Cible : data champions, directeurs, VP.

### Formats pedagogiques recommandes

| Format | Efficacite | Scalabilite | Cout | Quand l'utiliser |
|---|---|---|---|---|
| **Formation en presentiel** | Tres haute | Faible | Eleve | Niveaux 3-4, ateliers pratiques |
| **E-learning asynchrone** | Moyenne | Tres haute | Moyen (creation) | Niveau 1, fondamentaux |
| **Data clinics (sessions ouvertes)** | Haute | Moyenne | Faible | Post-formation, renforcement |
| **Mentorat 1:1 (champion-collegue)** | Tres haute | Faible | Faible | Accompagnement personnalise |
| **Lunch & Learn** | Moyenne | Moyenne | Faible | Sensibilisation, inspiration |
| **Hackathons data** | Haute (engagement) | Faible | Moyen | Stimulation, innovation, team-building |
| **Communaute de pratique** | Haute (long terme) | Haute | Faible | Perennisation, partage continu |

### Mesure de l'efficacite de la formation

Appliquer le modele de Kirkpatrick a 4 niveaux :
1. **Reaction** : satisfaction des participants (survey post-formation). Cible : > 4/5.
2. **Apprentissage** : acquisition de connaissances (quiz, exercices). Cible : > 80% de reussite.
3. **Comportement** : application en situation reelle. Mesurer via l'usage des outils (logins, dashboards crees, requetes executees) a 1, 3 et 6 mois post-formation.
4. **Resultats** : impact business. Mesurer la reduction du temps de decision, l'augmentation du nombre de decisions documentees par les donnees, l'amelioration des KPIs lies aux initiatives data-driven.

---

## Measuring Data Culture Maturity

### Modele de maturite Data Culture en 5 niveaux

**Niveau 1 — Ad Hoc (Data-Resistant)**
- Les decisions sont prises sur la base de l'intuition, de la hierarchie, ou de l'experience.
- Les donnees sont utilisees retrospectivement pour justifier des decisions deja prises.
- Pas de standards de visualisation, pas de glossaire, pas de self-service.
- Les equipes data sont percues comme un centre de cout.
- Score typique : < 20% des decisions sont documentees par les donnees.

**Niveau 2 — Emerging (Data-Aware)**
- Certaines equipes utilisent les donnees regulierement, d'autres non.
- Des dashboards existent mais sont peu consultes ou mal compris.
- L'equipe data repond aux demandes ad hoc mais est debordee.
- Pas de data champions formalises.
- Score typique : 20-40% des decisions documentees par les donnees.

**Niveau 3 — Established (Data-Literate)**
- La majorite des equipes utilise les donnees pour les decisions operationnelles.
- Des dashboards certifies existent avec un refresh regulier.
- Un programme de data champions est en place.
- Le self-service analytics couvre les cas d'usage les plus courants.
- Un glossaire metier est maintenu et accessible.
- Score typique : 40-60% des decisions documentees par les donnees.

**Niveau 4 — Advanced (Data-Driven)**
- Les donnees sont integrees dans la quasi-totalite des processus de decision.
- L'experimentation (A/B testing) est une pratique courante.
- Les data champions sont actifs et reconnus dans chaque departement.
- La qualite des donnees est monitoree avec des SLAs.
- Le self-service couvre 80%+ des besoins courants.
- Score typique : 60-80% des decisions documentees par les donnees.

**Niveau 5 — Leading (Data-Native)**
- Les donnees sont dans l'ADN de l'organisation — chaque reunoin, chaque proposal, chaque revue est etayee par des donnees.
- L'IA et le machine learning sont integres dans les processus operationnels.
- L'organisation partage des donnees avec son ecosysteme (partenaires, clients).
- L'innovation data est un avantage concurrentiel reconnu.
- La data literacy est un critere de recrutement et d'evaluation a tous les niveaux.
- Score typique : > 80% des decisions documentees par les donnees.

### Scorecard de maturite — Dimensions d'evaluation

| Dimension | Indicateurs mesurables |
|---|---|
| **Leadership & Vision** | Le comex a-t-il une strategie data formalisee ? Un CDO ou equivalent est-il en place ? Les OKR de l'organisation incluent-ils des objectifs data ? |
| **Competences & Formation** | Quel % des collaborateurs a suivi une formation data ? Combien de data champions actifs ? Quel est le niveau moyen au Data Literacy Assessment ? |
| **Outils & Infrastructure** | Un outil de self-service est-il deploye ? Quel est le taux d'adoption (MAU/effectif) ? La semantic layer est-elle en place ? |
| **Gouvernance & Qualite** | Un data catalog existe-t-il ? Quel % des metriques critiques a une definition formelle ? Quel est le data quality score moyen ? |
| **Processus & Pratiques** | Les decisions sont-elles documentees par les donnees ? Des revues de dashboards regulieres existent-elles ? L'A/B testing est-il pratique ? |
| **Culture & Comportement** | Les donnees sont-elles citees dans les reunions ? Les echecs d'analyses sont-ils partages ouvertement ? L'experimentation est-elle encouragee ? |

### KPIs de suivi de la data culture

**Metriques d'adoption** :
- Nombre d'utilisateurs actifs mensuels (MAU) des outils self-service / effectif total.
- Nombre de dashboards consultes par semaine (total et par departement).
- Nombre de requetes self-service executees par mois.
- Temps moyen entre une question data et une reponse (data-to-insight latency).
- Ratio contenus certifies / contenus non-certifies.

**Metriques de qualite** :
- Data quality score moyen des datasets critiques.
- Nombre d'incidents de qualite de donnees par mois.
- Temps moyen de resolution des incidents de qualite.
- Couverture du data catalog (% de tables documentees).
- Couverture du glossaire metier (% de metriques definies).

**Metriques d'impact** :
- % de decisions strategiques documentees par les donnees (audit trimestriel).
- Nombre d'A/B tests lances par trimestre.
- Reduction du temps de production de rapports recurrents.
- Satisfaction des utilisateurs data (survey semestriel, NPS interne).
- ROI des initiatives data-driven (revenus generes, couts evites, risques reduits).

---

## Organizational Change for Data Adoption

### Le modele ADKAR applique a la data culture

Le modele ADKAR (Prosci) est un framework de conduite du changement applicable a la transformation data :

**A — Awareness (Prise de conscience)**
Les collaborateurs comprennent pourquoi le changement est necessaire.
- Actions : town halls avec des exemples concrets de decisions ameliorees par les donnees, partage d'echecs causes par le manque de donnees, benchmarks concurrentiels.
- Piege : supposer que les gens sont deja convaincus. La majorite est soit indifferente soit sceptique.

**D — Desire (Envie)**
Les collaborateurs veulent participer au changement.
- Actions : montrer le "what's in it for me" (reduction de taches repetitives, meilleures decisions, reconnaissance), impliquer les leaders d'opinion, creer des early wins visibles.
- Piege : imposer le changement par la hierarchie sans susciter l'adhesion. Le compliance sans conviction est fragile.

**K — Knowledge (Connaissance)**
Les collaborateurs savent comment changer.
- Actions : programme de formation par niveaux, documentation accessible, tutoriels video, data champions comme relais locaux.
- Piege : former trop tot (avant l'Awareness et le Desire) ou trop tard (apres le deploiement des outils).

**A — Ability (Capacite)**
Les collaborateurs sont capables d'appliquer le changement au quotidien.
- Actions : outils deployes et fonctionnels, support disponible (helpdesk data, champions, office hours), temps alloue pour la pratique.
- Piege : deployer des outils complexes sans accompagnement, ou attendre une maitrise parfaite avant de commencer.

**R — Reinforcement (Renforcement)**
Le changement est ancre dans les habitudes et les processus.
- Actions : celebrations des succes data, integration dans les revues de performance, communautes de pratique, evolution continue du programme.
- Piege : arreter l'effort apres le deploiement initial. Sans renforcement, les comportements reviennent a l'etat anterieur en 6-12 mois.

### Resistance au changement — Patterns et reponses

| Pattern de resistance | Signe observable | Reponse recommandee |
|---|---|---|
| **"On a toujours fait comme ca"** | Refus d'utiliser les nouveaux outils | Montrer un cas concret ou l'ancienne methode a echoue et la nouvelle a reussi |
| **"Je n'ai pas le temps"** | Non-participation aux formations | Integrer la data dans les processus existants plutot que d'ajouter une couche |
| **"Les donnees mentent"** | Rejet systematique des conclusions data | Impliquer la personne dans la methodologie, transparence totale sur les limites |
| **"C'est le job de l'equipe data"** | Delegation systematique | Celebrer les succes des non-data people, montrer que chacun peut contribuer |
| **"Mes donnees sont differentes"** | Creation de rapports paralleles | Integrer les specificites dans le systeme officiel, pas les ignorer |
| **"L'IA va remplacer tout ca"** | Attentisme | Montrer que l'IA amplifie la data literacy, ne la remplace pas. L'IA necessite des utilisateurs capables de challenger ses resultats |

### Coalition de soutien

Construire une coalition a trois niveaux pour porter le changement :

**Sponsor executif (1-2 personnes)** :
- Membre du comex, idealement CDO, CFO ou COO.
- Role : debloquer les budgets, porter le message au plus haut niveau, arbitrer les conflits.
- Engagement minimum : revue trimestrielle du programme, mention reguliere dans les communications internes.

**Champions de direction (5-10 personnes)** :
- Directeurs ou VP qui integrent les donnees dans le pilotage de leur departement.
- Role : modele de comportement, allocation de temps pour les champions, integration dans les objectifs d'equipe.
- Engagement minimum : participation aux data clinics mensuelles, revue des dashboards departementaux.

**Data champions (1 pour 20-50 collaborateurs)** :
- Volontaires ancres dans chaque equipe operationnelle.
- Role : formation locale, support de proximite, remontee des besoins et frictions.
- Engagement minimum : 10-20% du temps, participation aux meetups mensuels de la communaute.

### Timeline type d'une transformation data culture

| Phase | Duree | Objectifs cles | Indicateurs de succes |
|---|---|---|---|
| **Diagnostic** | Mois 1-2 | Evaluer la maturite actuelle, identifier les quick wins | Scorecard de maturite complete, roadmap validee |
| **Quick Wins** | Mois 2-4 | Livrer 3-5 cas d'usage a forte valeur visible | Dashboards utilises, temoignages positifs |
| **Foundation** | Mois 3-8 | Deployer la plateforme, former les champions, lancer le Niveau 1 | 80% de l'effectif forme au Niveau 1, champions actifs |
| **Acceleration** | Mois 6-12 | Etendre le self-service, lancer les Niveaux 2-3, mesurer l'adoption | MAU > 40% de l'effectif, > 50% des decisions documentees |
| **Ancrage** | Mois 12-24 | Industrialiser, integrer dans les processus RH, mesurer l'impact business | ROI mesurable, maturite Niveau 3-4, programme auto-entretenu |
| **Excellence** | Mois 24+ | Innovation data, experimentation generalisee, partage externe | Maturite Niveau 4-5, avantage concurrentiel data reconnu |

### Budget indicatif

| Poste | Fourchette | Notes |
|---|---|---|
| **Outils BI (licences)** | 10-50 EUR/utilisateur/mois | Selon l'outil et le tier choisi |
| **Formation (creation de contenu)** | 30-80K EUR | Creation initiale des 4 niveaux |
| **Formation (deploiement)** | 500-2,000 EUR/personne | Selon le niveau et le format |
| **Data champions (temps alloue)** | 10-20% d'un ETP par champion | Cout indirect — pas de budget direct |
| **Accompagnement conduite du changement** | 50-150K EUR | Consultant specialise sur 12-18 mois |
| **Infrastructure semantic layer** | 20-100K EUR/an | Selon la complexite et l'outil |

Le ROI typique d'un programme de data culture mature est estime entre 3x et 10x sur 3 ans, principalement via la reduction du temps de production de rapports, l'amelioration de la qualite des decisions, et l'identification d'opportunites et de risques manques auparavant.
