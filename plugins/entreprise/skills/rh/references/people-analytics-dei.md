# People Analytics & DEI — HR Analytics, Engagement, Diversity Strategy, Pay Equity

## Overview

Ce document de reference couvre les disciplines analytiques et strategiques de la fonction RH : le people analytics (collecte, analyse et exploitation des donnees RH pour eclairer les decisions) et la strategie DEI (Diversite, Equite, Inclusion). Ces deux domaines sont intimement lies : le people analytics fournit les donnees objectives necessaires pour mesurer les progres en DEI, et la strategie DEI oriente les analyses vers les questions d'equite et de representation. Utiliser ce guide pour deployer une fonction analytics RH mature et une strategie DEI fondee sur les preuves.

---

## People Analytics — KPIs et Metriques RH

### Framework de Metriques RH

Organiser les metriques RH en 5 categories, de l'operationnel au strategique :

#### 1. Metriques de Recrutement

| Metrique | Definition | Benchmark | Calcul |
|---|---|---|---|
| **Time-to-hire** | Jours entre l'ouverture du poste et l'acceptation de l'offre | 25-40 jours (tech), 30-60 jours (management) | Date acceptation - Date ouverture |
| **Time-to-fill** | Jours entre l'ouverture du poste et le debut effectif | 40-60 jours (tech), 50-80 jours (management) | Date debut - Date ouverture |
| **Cost-per-hire** | Cout total moyen d'un recrutement | 3 000-8 000 EUR (France, profil qualifie) | (Couts internes + externes) / Nombre d'embauches |
| **Quality of hire** | Performance et retention des nouvelles recrues | Score performance > 3/5 a 12 mois, retention > 85% a 1 an | Combinaison performance + retention + feedback manager |
| **Source effectiveness** | Taux de conversion et qualite par canal de sourcing | Variable selon canal | Embauches par source / Candidatures par source |
| **Offer acceptance rate** | Pourcentage d'offres acceptees | 85-95% | Offres acceptees / Offres emises |
| **Candidate experience score** | Satisfaction des candidats sur le processus | > 4/5 | Enquete post-processus |

#### 2. Metriques d'Engagement et Retention

| Metrique | Definition | Benchmark | Calcul |
|---|---|---|---|
| **eNPS (Employee Net Promoter Score)** | Probabilite de recommander l'entreprise comme employeur | > 20 (bon), > 40 (excellent) | % Promoteurs (9-10) - % Detracteurs (0-6) |
| **Turnover volontaire** | Taux de departs volontaires | 8-15% annuel (France, hors tech). Tech : 15-25% | Departs volontaires / Effectif moyen x 100 |
| **Turnover regrettable** | Departs des collaborateurs que l'entreprise aurait voulu retenir | < 5% | Departs regrettables / Effectif moyen x 100 |
| **Retention rate** | Pourcentage de collaborateurs restes sur la periode | > 85% a 1 an | (Effectif debut - Departs) / Effectif debut x 100 |
| **Absenteisme** | Taux d'absences non planifiees | 4-6% (France, secteur prive) | Jours absence / Jours theoriques x 100 |
| **Anciennete moyenne** | Duree moyenne de presence | Variable selon secteur et stade entreprise | Somme des anciennetes / Effectif |

#### 3. Metriques de Performance et Developpement

| Metrique | Definition | Benchmark |
|---|---|---|
| **Taux de completion des reviews** | Pourcentage de reviews realisees dans les delais | > 95% |
| **Distribution des ratings** | Repartition des evaluations de performance | Pas de concentration > 70% sur un seul rating |
| **Mobilite interne** | Pourcentage de postes pourvus en interne | 20-40% (bon), > 40% (excellent) |
| **Taux de completion formation** | Pourcentage de formations achevees | > 80% |
| **Heures de formation par collaborateur** | Investissement formation par tete | 20-40h/an (France, obligation legale 1% masse salariale) |
| **ROI formation** | Retour sur investissement des actions de formation | Difficile a mesurer directement. Proxies : performance post-formation, retention des formes |

#### 4. Metriques de Compensation

| Metrique | Definition | Benchmark |
|---|---|---|
| **Compa-ratio** | Salaire reel / Midpoint de la bande salariale | 0.90 - 1.10 |
| **Range penetration** | Position du salaire dans la bande (0% = min, 100% = max) | 40-60% pour collaborateurs pleinement performants |
| **Pay equity ratio** | Ecart de remuneration a poste et experience equivalents (par genre, age, etc.) | < 3% d'ecart inexplique |
| **Total compensation competitiveness** | Position du package total vs marche | Aligne sur le percentile cible (P50, P75, etc.) |
| **Cout de la masse salariale / CA** | Part de la masse salariale dans le chiffre d'affaires | Variable par secteur (20-40% services, 10-20% industrie) |

#### 5. Metriques Organisationnelles

| Metrique | Definition | Benchmark |
|---|---|---|
| **Span of control** | Nombre moyen de reports directs par manager | 5-8 (optimal). > 12 : surcharge manageriale |
| **Management ratio** | Ratio managers / contributeurs individuels | 1:6 a 1:10 (selon la maturite des equipes) |
| **Workforce composition** | Repartition par type de contrat (CDI, CDD, interim, freelance) | Variable selon strategie |
| **Diversity metrics** | Representation par genre, age, handicap a chaque niveau hierarchique | cf. section DEI |

### Enquetes d'Engagement

#### Types d'enquetes

| Type | Frequence | Nombre de questions | Objectif |
|---|---|---|---|
| **Enquete annuelle** | 1x/an | 40-80 questions | Diagnostic complet de l'engagement et de la satisfaction |
| **Enquete pulse** | Mensuel ou trimestriel | 5-15 questions | Suivi de l'evolution des indicateurs cles et detection rapide des tendances |
| **Enquete thematique** | Ad hoc | 10-20 questions | Exploration d'un sujet specifique (teletravail, management, bien-etre) |
| **eNPS** | Trimestriel | 1 question + commentaire libre | Indicateur flash de l'engagement global |
| **Onboarding survey** | J30, J60, J90 | 10-15 questions | Mesure de la qualite de l'integration |
| **Exit survey** | Au depart | 15-25 questions | Comprehension des raisons de depart |

#### Outils d'enquetes d'engagement

| Outil | Forces | Taille cible |
|---|---|---|
| **Culture Amp** | Analytics avances, benchmarks, action planning integre | 100-10 000+ |
| **Officevibe (Workleap)** | Interface intuitive, pulse surveys, feedback anonyme | 50-1 000 |
| **Peakon (Workday)** | IA predictive, integration Workday native | 500-50 000+ |
| **Leapsome** | Combine engagement, performance et apprentissage | 100-5 000 |
| **Supermood** | Outil francais, conformite RGPD native | 50-5 000 |
| **Bleexo** | Outil francais, focus QVT et bien-etre | 50-2 000 |

#### Bonnes pratiques des enquetes d'engagement
- **Anonymat garanti** : ne jamais permettre l'identification des repondants dans les groupes de moins de 5 personnes. Communiquer clairement sur les garanties d'anonymat.
- **Taux de participation** : viser > 75% pour une representativite fiable. Un taux faible est en soi un signal (desengagement, defiance).
- **Action planning** : chaque enquete doit aboutir a des actions concretes communiquees aux collaborateurs. Publier les resultats sous 2 semaines et les plans d'action sous 4 semaines. Le pire pour l'engagement est de faire des enquetes sans jamais agir.
- **Longitudinal tracking** : suivre l'evolution des scores dans le temps plutot que de se focaliser sur les valeurs absolues. Un eNPS de 15 en progression constante est plus sain qu'un eNPS de 30 en baisse.
- **Segmentation** : analyser les resultats par equipe, departement, anciennete, niveau hierarchique, localisation. Les moyennes globales masquent les disparites.

### Workforce Planning

#### Processus de Workforce Planning

1. **Analyse de la situation actuelle** : cartographier les effectifs par famille de metiers, niveau, localisation, type de contrat. Identifier les pyramides des ages et les risques demographiques (departs en retraite, concentration de competences critiques).
2. **Projection des besoins** : a partir du plan strategique et des projections business (croissance, nouveaux marches, nouvelles offres), estimer les besoins en effectifs et en competences a 12-36 mois. Utiliser des scenarios (optimiste, central, pessimiste).
3. **Gap analysis** : comparer les effectifs projetes avec les effectifs actuels ajustes du turnover prevu. Identifier les gaps par famille de metiers et par competence.
4. **Plan d'action** : definir les leviers pour combler les gaps :
   - **Build** : formation et montee en competences des collaborateurs existants.
   - **Buy** : recrutement externe de nouveaux talents.
   - **Borrow** : recours a des freelances, consultants ou interim pour les besoins temporaires ou les competences emergentes.
   - **Bot** : automatisation de certaines taches par la technologie (IA, RPA).
5. **Budgetisation** : chiffrer le plan (masse salariale, couts de recrutement, budgets de formation, couts de prestation externe).
6. **Suivi et ajustement** : revoir le plan trimestriellement. Ajuster en fonction de l'evolution du business, du turnover reel et des recrutements realises.

#### Modelisation de l'Attrition
Construire un modele predictif de l'attrition pour anticiper les departs et agir en amont :

**Variables predictives typiques** :
- Anciennete dans le poste (risque eleve a 18-24 mois sans evolution).
- Historique d'augmentations (pas d'augmentation depuis > 18 mois).
- Resultat de la derniere enquete d'engagement (score en baisse).
- Changement de manager recent (risque eleve dans les 6 mois suivants).
- Ecart de remuneration vs marche (compa-ratio < 0.85).
- Distance domicile-travail.
- Evenements de vie (retour de conge parental, fin de formation).

**Approche** :
- Utiliser un modele de survie (Cox proportional hazards) ou un modele de classification (random forest, gradient boosting) entraine sur les donnees historiques de departs.
- Evaluer le modele par AUC-ROC (objectif > 0.75) et calibration.
- Fournir un score de risque par collaborateur aux managers et HR Business Partners.
- **Important** : ne jamais utiliser le score de risque pour penaliser un collaborateur. L'objectif est la retention proactive (discussion, ajustement, developpement).

---

## DEI — Diversite, Equite & Inclusion

### Strategie DEI — Framework

#### Definitions operationnelles
- **Diversite** : la presence de differences au sein de l'organisation (genre, age, origine, handicap, orientation sexuelle, neurodiversite, parcours socio-economique, parcours academique). La diversite est un fait mesurable.
- **Equite** : l'assurance que les processus et les resultats sont justes pour tous, en tenant compte des barrieres structurelles que certains groupes rencontrent. L'equite n'est pas l'egalite : elle implique des actions differenciees pour compenser des desavantages structurels.
- **Inclusion** : le sentiment d'appartenance et la capacite de chaque individu a contribuer pleinement, independamment de ses differences. L'inclusion est une experience vecue, mesurable par des enquetes.

#### Modele de maturite DEI

| Niveau | Description | Caracteristiques |
|---|---|---|
| **1 — Compliance** | La DEI est traitee comme une obligation legale | Respect des quotas, reporting minimum, pas de strategie proactive |
| **2 — Programmatic** | Des programmes DEI existent mais restent peripheriques | Formations biais inconscients, celebrations, ERGs, pas d'integration dans les processus RH |
| **3 — Embedded** | La DEI est integree dans les processus RH et business | Recrutement inclusif, audits d'equite salariale, analytics DEI, objectifs DEI dans les OKR |
| **4 — Systemic** | La DEI est un levier strategique et culturel | DEI integree dans la strategie d'entreprise, le design produit, les relations fournisseurs, la culture quotidienne |

Viser au minimum le niveau 3 (Embedded) pour un impact reel et mesurable.

### Recrutement Inclusif

#### Redaction d'offres d'emploi inclusives
- **Langage non genre** : utiliser l'ecriture inclusive ou des formulations neutres. Eviter les termes codes masculins (ex : "ninja", "rockstar", "agressif") qui decouragent les candidatures feminines.
- **Exigences realistes** : les etudes montrent que les femmes postulent quand elles remplissent 100% des criteres, les hommes a 60%. Distinguer clairement "requis" et "souhaite". Limiter les criteres requis a ce qui est reellement eliminatoire.
- **Formulations inclusives** : mentionner explicitement l'engagement DEI de l'entreprise. Preciser les amenagements possibles pour les personnes en situation de handicap. Eviter les references inutiles a l'age ou a la localisation.
- **Outils de verification** : Textio, Gender Decoder, Witty Works analysent les biais linguistiques des offres d'emploi.

#### Processus de selection inclusif
- **CV anonymise** : masquer le nom, l'adresse, la photo, l'age et les informations personnelles identifiantes lors du premier tri. Des etudes (Behaghel et al., 2015) montrent un effet positif sur la diversite du shortlisting.
- **Panel d'entretien diversifie** : s'assurer que le panel d'evaluateurs est representatif en termes de genre, anciennete et background.
- **Questions standardisees** : les memes questions pour tous les candidats, avec une scorecard predéfinie. Eliminer les questions potentiellement discriminatoires (situation familiale, projets d'enfants, origine).
- **Evaluation des competences, pas du fit culturel** : remplacer la notion de "culture fit" (qui favorise la reproduction a l'identique) par "culture add" (ce que le candidat apporte de nouveau a la culture).

### Formation aux Biais Inconscients (Unconscious Bias Training)

#### Types de biais a couvrir
- **Biais d'affinite** : preference pour les personnes qui nous ressemblent (meme ecole, meme parcours, memes hobbies).
- **Biais de confirmation** : tendance a chercher les informations qui confirment notre premiere impression.
- **Effet de halo** : une qualite positive influence positivement l'evaluation de toutes les autres qualites.
- **Biais d'ancrage** : la premiere information recue (ex : salaire precedent) influence disproportionnellement le jugement.
- **Biais de recence** : accorder plus de poids aux evenements recents qu'aux evenements passes.
- **Biais de genre** : les memes comportements sont percus differemment selon le genre (ex : "leader" vs "autoritaire").
- **Biais d'age** : presupposes sur les competences ou l'adaptabilite lies a l'age.

#### Efficacite des formations
La recherche est nuancee sur l'efficacite des formations aux biais inconscients :
- Les formations de sensibilisation seules (awareness) ont un impact limite et de courte duree (Paluck et al., 2021).
- Les formations combinees a des changements structurels (processus, outils, metriques) sont significativement plus efficaces.
- Privilegier des formations courtes et repetees (micro-learning, nudges) plutot qu'une session unique annuelle.
- Integrer les biais dans les moments de decision (rappels avant un entretien, checklist avant une evaluation) plutot que dans des sessions decontextualisees.

### ERGs (Employee Resource Groups)

Les ERGs sont des groupes de collaborateurs reunis autour d'une identite ou d'une experience partagee :
- **Exemples** : Women@Company, Pride Network, Parents Network, Disability Network, Network des collaborateurs issus de la diversite, Network des seniors.
- **Mission** : soutien mutuel, networking, sensibilisation, recommandations aupres de la direction sur les politiques RH.
- **Organisation** : budget dedie (typiquement 2 000-10 000 EUR/an par ERG), sponsor executif, leader(s) ERG avec du temps dedie, programme d'evenements.
- **Impact mesurable** : les entreprises avec des ERGs actifs rapportent un eNPS +15 points pour les membres des ERGs et un taux de retention +10% (McKinsey).

### Pay Equity — Equite Salariale

#### Methodologie d'audit d'equite salariale

1. **Collecte des donnees** : rassembler les donnees de remuneration (fixe, variable, equity), les donnees demographiques (genre, age, anciennete) et les donnees de poste (famille de metiers, niveau, localisation, performance).
2. **Analyse descriptive** : calculer les ecarts bruts de remuneration par genre (et autres axes proteges) a chaque niveau et dans chaque famille de metiers. Les ecarts bruts incluent les differences de representation (ex : moins de femmes a des niveaux seniors).
3. **Analyse multivariee** : realiser une regression multivariee pour isoler l'ecart "inexplique" :

```
Remuneration = f(poste, niveau, anciennete, performance, localisation, ...) + ecart_genre + residuel

L'ecart_genre apres controle des variables legitimes represente la part
"inexpliquee" de l'ecart salarial. C'est cet ecart qu'il faut corriger.

Variables legitimes : poste, niveau de responsabilite, anciennete, performance,
localisation, competences specifiques certifiees.

Variables NON legitimes : genre, age, origine, situation familiale, temps partiel
(si non lie a la performance), ecole d'origine.
```

4. **Identification des outliers** : identifier les collaborateurs dont le salaire est significativement en-dessous de la prediction du modele apres controle des variables legitimes.
5. **Plan de remediation** : budgetiser et planifier les ajustements salariaux pour les outliers identifies. Typiquement, un budget de 0.5-2% de la masse salariale est necessaire lors du premier audit.
6. **Suivi continu** : integrer l'analyse d'equite dans le processus annuel de revue salariale. Prevenir les nouveaux ecarts en controlant l'equite a l'embauche et a chaque augmentation.

#### Index Egalite Professionnelle (Index Penicaud)

**Obligation legale en France** pour les entreprises de 50+ salaries. Publication annuelle d'un score sur 100 points :

| Indicateur | Points | Mesure |
|---|---|---|
| Ecart de remuneration F/H | 40 points | Par tranche d'age et categorie professionnelle |
| Ecart de taux d'augmentations individuelles | 20 points | Hors promotions (entreprises > 250) |
| Ecart de taux de promotions | 15 points | Entreprises > 250 salaries |
| Augmentations au retour de conge maternite | 15 points | 100% des salariees augmentees si augmentations dans la periode |
| Representation dans les 10 plus hautes remunerations | 10 points | Au moins 4 personnes du sexe sous-represente |

- **Score minimum** : 75/100. En dessous, obligation de negocier des mesures correctives.
- **Publication** : sur le site de l'entreprise et sur la plateforme Egapro.
- **Tendances** : le score moyen en France est de 88/100 (2024), mais les progres stagnent sur les indicateurs de haute remuneration et de promotion.

### DEI Analytics — Metriques et Reporting

#### Metriques DEI essentielles

| Dimension | Metriques | Objectif |
|---|---|---|
| **Representation** | % de femmes, personnes en situation de handicap, seniors par niveau hierarchique | Pipeline diversifie a tous les niveaux |
| **Recrutement** | Diversite du pipeline de candidatures, taux de conversion par groupe, diversite des embauches | Eliminer les biais du funnel de recrutement |
| **Retention** | Turnover par groupe demographique, ecarts d'anciennete | Pas de turnover disproportionne pour un groupe |
| **Promotion** | Taux de promotion par groupe, delai moyen entre promotions | Pas de glass ceiling mesurable |
| **Engagement** | eNPS par groupe, score d'inclusion | Pas d'ecart d'engagement significatif entre groupes |
| **Remuneration** | Ecart salarial ajuste par groupe, compa-ratio par groupe | Equite salariale demontree |
| **Formation** | Acces a la formation par groupe, heures de formation par groupe | Acces equitable au developpement |

#### Dashboard DEI
Construire un dashboard DEI visible par la direction avec les metriques clees, les tendances, et les actions en cours. Mettre a jour mensuellement ou trimestriellement. Inclure des comparaisons avec les benchmarks sectoriels et les objectifs fixes.

---

## State of the Art (2024-2026)

### AI-Powered People Analytics
L'IA transforme les capacites analytiques des equipes RH :
- **Predictive analytics** : des plateformes comme Visier, One Model et Workday Prism Analytics utilisent le machine learning pour predire l'attrition, identifier les hauts potentiels, optimiser le workforce planning et modeliser l'impact des decisions RH. Les modeles deviennent plus precis grace a l'integration de donnees multi-sources (SIRH, enquetes, feedback, activite collaboration).
- **NLP sur les donnees qualitatives** : l'IA analyse automatiquement les commentaires des enquetes d'engagement, les exit interviews et les feedbacks pour identifier les themes emergents, le sentiment et les signaux faibles. Des outils comme Culture Amp et Qualtrics integrent ces capacites nativement.
- **Organizational Network Analysis (ONA)** : l'analyse des flux de communication (emails, messages, reunions — avec le consentement des collaborateurs et dans le respect du RGPD) revele les reseaux informels, les silos, les bottlenecks de collaboration et les leaders d'influence non reconnus. Outils : Microsoft Viva Insights (ex-Workplace Analytics), Polinode, Humanyze.
- **Skills intelligence** : l'IA cartographie les competences de l'organisation en temps reel a partir de multiples signaux (profils, projets, formations, certifications). Permet un workforce planning base sur les competences plutot que sur les postes. Outils : Eightfold AI, Beamery, Lightcast.

### Ethical AI in HR
L'utilisation de l'IA dans les decisions RH souleve des questions ethiques majeures :
- **EU AI Act (2024)** : les systemes IA utilises pour le recrutement, l'evaluation des performances et les decisions d'emploi sont classes "haut risque". Obligations : transparence vis-a-vis des personnes concernees, documentation technique, evaluation de conformite, supervision humaine obligatoire.
- **Bias auditing** : obligation d'auditer regulierement les algorithmes RH pour les biais discriminatoires. Des frameworks comme le NIST AI Risk Management Framework et l'ISO 42001 fournissent des guidelines. Des entreprises comme Pymetrics et HireVue publient des rapports d'audit de biais.
- **Right to explanation** : en vertu du RGPD (Article 22), les personnes soumises a une decision automatisee significative ont le droit d'obtenir une explication et de contester la decision. Assurer que chaque decision assistee par IA peut etre expliquee en termes comprehensibles.
- **Human-in-the-loop** : maintenir systematiquement un decision-maker humain pour toutes les decisions RH significatives (embauche, promotion, augmentation, sanction). L'IA recommande, l'humain decide.

### DEI Evolution 2024-2026
Le paysage DEI evolue rapidement sous l'effet de la reglementation, des attentes societales et des pressions contradictoires :
- **Directive europeenne transparence salariale** : transposition d'ici 2026, imposant la publication des ecarts salariaux et le droit pour les candidats de connaitre la fourchette salariale. Les entreprises europeennes doivent se preparer a une transparence accrue.
- **Corporate Sustainability Reporting Directive (CSRD)** : les entreprises europeennes de 250+ salaries doivent reporter sur les metriques sociales et DEI dans le cadre de la CSRD (premiers reportings en 2025 pour les donnees 2024). Les indicateurs couvrent l'egalite de remuneration, la representation, les conditions de travail et le dialogue social.
- **Intersectionalite** : l'analyse DEI evolue d'une approche monocritere (genre OU age OU handicap) vers une approche intersectionnelle (genre ET age ET origine). Les outils analytics s'adaptent pour fournir des analyses multi-dimensionnelles.
- **Neurodiversite** : reconnaissance croissante de la neurodiversite (autisme, TDAH, dyslexie, haut potentiel) comme dimension de la diversite. Adaptation des processus de recrutement (entretiens structures, accommodations), de l'environnement de travail (espaces calmes, flexibilite) et des methodes de management.
- **Accessibilite numerique** : la Directive europeenne sur l'accessibilite (European Accessibility Act, application 2025) impose l'accessibilite des produits et services numeriques, y compris les outils RH internes (SIRH, LMS, portails collaborateurs). Auditer et mettre en conformite les outils RH pour les personnes en situation de handicap.
- **DEI analytics avances** : au-dela du comptage (representation), les entreprises leaders analysent l'equite des processus (qui est promu, qui a acces a quelles opportunites, qui recoit quel feedback) et l'inclusion vecue (sentiment d'appartenance, securite psychologique par groupe).

### Engagement in a Hybrid World
L'engagement des collaborateurs est repense pour le monde hybride :
- **Digital employee experience (DEX)** : l'experience numerique du collaborateur (qualite des outils, fluidite des processus digitaux, acces a l'information) est devenue un driver majeur de l'engagement. Des outils comme Nexthink, Lakeside et 1E mesurent et optimisent la DEX.
- **Hybrid-adapted surveys** : les enquetes d'engagement integrent des questions specifiques au travail hybride (qualite de la collaboration a distance, sentiment d'isolation, equite de traitement tele/presentiel, qualite de l'equipement).
- **Wellbeing analytics** : integration de metriques de bien-etre (stress, charge mentale, equilibre vie pro/perso) dans les dashboards d'engagement. Des outils comme Microsoft Viva Insights detectent les signaux de surcharge (reunions excessives, emails hors horaires, absence de focus time) et emettent des nudges aux managers.
- **Continuous listening** : evolution d'un modele d'enquetes periodiques vers un modele d'ecoute continue combinant enquetes pulse, analyse de sentiment sur les canaux internes, feedback en temps reel et signaux comportementaux (anonymises et consentis). L'objectif est de detecter les signaux faibles avant qu'ils ne deviennent des crises.
- **Manager effectiveness** : reconnaissance que le manager est le facteur #1 d'engagement (Gallup). Investissement dans des programmes de formation et de coaching managerial, combines a des feedbacks ascendants (enquetes 360 pour les managers) et des metriques d'engagement par equipe.
