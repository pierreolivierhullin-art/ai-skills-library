# IT Governance & Strategy — SDSI, ITIL 4, COBIT, Budget IT & Vendor Management

## Overview

Ce document de reference couvre les fondamentaux de la gouvernance et de la strategie IT : elaboration et pilotage du Schema Directeur des Systemes d'Information (SDSI), mise en oeuvre des referentiels ITIL 4 et COBIT 2019, gestion du budget IT et du TCO, management des fournisseurs IT, gouvernance du shadow IT et gestion du portefeuille applicatif. Utiliser ce guide comme fondation pour toute initiative de gouvernance IT, en l'adaptant au contexte specifique de l'organisation (secteur, taille, maturite, contraintes reglementaires).

---

## Schema Directeur des Systemes d'Information (SDSI)

### Definition et finalite

Le SDSI est le document strategique qui definit la trajectoire de transformation du systeme d'information sur 3 a 5 ans. Il traduit la strategie d'entreprise en initiatives IT concretes, priorisees et budgetees. Ce n'est ni un catalogue technique ni une liste de projets : c'est une feuille de route strategique portee conjointement par la DSI et les directions metier.

### Structure type d'un SDSI

Un SDSI complet comporte sept parties :

#### 1. Vision et ambitions

Formuler la vision IT en lien direct avec la strategie d'entreprise. Exemples :
- "Devenir une entreprise cloud-native d'ici 3 ans pour accelerer le time-to-market."
- "Rationaliser le portefeuille applicatif de 200 a 80 applications pour reduire les couts de maintenance de 40%."
- "Atteindre la conformite NIS2 et deployer une architecture Zero Trust en 24 mois."

Chaque ambition doit etre assortie d'un KPI mesurable et d'un horizon temporel.

#### 2. Diagnostic de l'existant

Realiser un etat des lieux factuel couvrant :
- **Portefeuille applicatif** : nombre d'applications, age moyen, criticite, dette technique, couts de maintenance. Utiliser une cartographie applicative (LeanIX, Ardoq, ou un simple tableur structure).
- **Infrastructure** : taux de virtualisation, repartition on-premise / cloud, age du parc serveur, capacite reseau.
- **Securite** : niveau de maturite (gap analysis ISO 27001), vulnerabilites identifiees, incidents des 12 derniers mois.
- **ITSM** : volumes d'incidents/demandes, temps moyen de resolution, taux de satisfaction utilisateur, couverture CMDB.
- **Couts** : repartition run/build/transform, ratio IT/CA (benchmarks : 3-5% industrie, 5-8% services, 7-12% finance), cout par poste de travail.
- **Organisation** : effectifs IT, repartition des competences, taux de sous-traitance, niveau de maturite agile.

#### 3. Architecture cible

Definir l'architecture SI cible a l'horizon du SDSI :
- **Architecture applicative** : urbanisation (decoupage en blocs fonctionnels), patterns d'integration (API-first, event-driven), choix des plateformes cles (ERP, CRM, ITSM).
- **Architecture technique** : strategie cloud, choix des providers, modele d'hebergement par workload, architecture reseau cible.
- **Architecture de securite** : modele Zero Trust, segmentation, gestion des identites (IAM/IGA).
- **Architecture de donnees** : data platform, gouvernance des donnees, flux de donnees entre systemes.

Utiliser les cadres TOGAF (pour les grandes organisations) ou une approche d'urbanisme SI simplifiee (pour les ETI/PME).

#### 4. Portefeuille de chantiers

Decliner la trajectoire en chantiers concrets, organises en vagues :

| Vague | Horizon | Focus | Exemples de chantiers |
|---|---|---|---|
| **Wave 1** | 0-12 mois | Fondations & Quick Wins | Cloud landing zones, SMSI, modernisation service desk, premiers retrait d'applications obsoletes |
| **Wave 2** | 12-24 mois | Transformation | Migration cloud, deploiement ERP, CMDB automatisee, conformite NIS2 |
| **Wave 3** | 24-36 mois | Innovation & Optimisation | ESM, AIOps, Zero Trust complet, FinOps mature |

#### 5. Modele de financement

Structurer le budget du SDSI en distinguant :
- **Run** (maintien en condition operationnelle) : viser une reduction progressive (typiquement de 70% a 55% du budget IT).
- **Build** (projets de transformation) : viser une augmentation (typiquement de 20% a 30%).
- **Transform** (innovation, R&D IT) : allouer 5-15% pour l'exploration et la modernisation.

#### 6. Gouvernance du SDSI

Mettre en place une gouvernance de pilotage :
- **Comite strategique IT** (trimestriel) : DSI + DG + sponsors metier. Arbitrage des priorites, validation des investissements.
- **Comite de pilotage SDSI** (mensuel) : DSI + responsables de domaines IT. Suivi de l'avancement, gestion des risques et des dependances.
- **Revue annuelle** : actualisation du SDSI en fonction des evolutions strategiques, technologiques et reglementaires.

#### 7. KPIs de pilotage du SDSI

| KPI | Cible | Frequence |
|---|---|---|
| Taux d'avancement des chantiers | > 80% on-time | Mensuel |
| Ratio run/build/transform | 55/30/15 | Trimestriel |
| Satisfaction utilisateurs IT | > 4/5 (NPS > 30) | Semestriel |
| Nombre d'applications actives | Reduction de 30% en 3 ans | Annuel |
| Cout IT / CA | Dans la cible sectorielle | Annuel |
| Dette technique (scoring) | Reduction progressive | Semestriel |

---

## ITIL 4 — Service Value System

### Evolution ITIL v3 vers ITIL 4

ITIL 4 (publie en 2019, derniere mise a jour 2023) marque un changement de paradigme par rapport a ITIL v3 :
- **De processus a pratiques** : ITIL 4 parle de 34 pratiques (et non plus de processus) pour souligner la flexibilite d'adaptation.
- **De cycle de vie a chaine de valeur** : la Service Value Chain remplace le cycle de vie rigide (Strategy -> Design -> Transition -> Operation -> Improvement).
- **Integration Agile/DevOps** : ITIL 4 integre explicitement les approches Agile, Lean et DevOps dans sa philosophie.
- **Co-creation de valeur** : la valeur n'est pas delivree unilaeralement par l'IT mais co-creee avec les parties prenantes.

### Le Service Value System (SVS)

Le SVS est le coeur d'ITIL 4. Il decrit comment tous les composants interagissent pour creer de la valeur :

```
[Opportunite / Demande]
        |
  [Principes directeurs]
        |
  [Gouvernance]
        |
  [Service Value Chain]  <-- Plan, Improve, Engage, Design & Transition, Obtain/Build, Deliver & Support
        |
  [Pratiques]  <-- 34 pratiques (general, service, technical)
        |
  [Amelioration continue]
        |
  [Valeur]
```

### Les 7 principes directeurs d'ITIL 4

1. **Focus on value** : toute action doit creer de la valeur pour les parties prenantes.
2. **Start where you are** : ne pas repartir de zero, evaluer et exploiter l'existant.
3. **Progress iteratively with feedback** : avancer par iterations courtes avec des boucles de feedback.
4. **Collaborate and promote visibility** : travailler en transparence et en collaboration.
5. **Think and work holistically** : considerer le systeme dans son ensemble, pas les silos.
6. **Keep it simple and practical** : eviter la complexite inutile, chercher la solution la plus simple.
7. **Optimize and automate** : optimiser les processus avant de les automatiser.

### Les 34 pratiques ITIL 4

Classees en trois categories :

**Pratiques de management general (14)** : strategy management, portfolio management, architecture management, service financial management, workforce and talent management, continual improvement, measurement and reporting, risk management, information security management, knowledge management, organizational change management, project management, relationship management, supplier management.

**Pratiques de gestion des services (17)** : business analysis, service catalogue management, service design, service level management, availability management, capacity and performance management, service continuity management, monitoring and event management, service desk, incident management, service request management, problem management, release management, change enablement, service validation and testing, service configuration management, IT asset management.

**Pratiques de gestion technique (3)** : deployment management, infrastructure and platform management, software development and management.

### Pratiques prioritaires selon la maturite

| Maturite | Pratiques a deployer en priorite |
|---|---|
| **Niveau 1** (Initial) | Incident management, service desk, service request management |
| **Niveau 2** (Repeatable) | Change enablement, problem management, service level management |
| **Niveau 3** (Defined) | Service configuration management (CMDB), knowledge management, continual improvement |
| **Niveau 4** (Managed) | IT asset management, capacity management, service continuity |
| **Niveau 5** (Optimized) | Toutes les pratiques integrees, automatisees et ameliorees en continu |

---

## COBIT 2019 — Governance & Management

### Structure de COBIT 2019

COBIT 2019 (Control Objectives for Information and Related Technologies) est le referentiel de reference pour la gouvernance IT. Il distingue :

- **Gouvernance** (5 objectifs) : EDM01 a EDM05 — Evaluer, Diriger et Surveiller. Responsabilite du conseil d'administration et de la direction.
- **Management** (35 objectifs) : APO (Aligner, Planifier, Organiser), BAI (Batir, Acquerir, Implementer), DSS (Delivrer, Servir, Supporter), MEA (Monitorer, Evaluer, Apprecier).

### Les 5 objectifs de gouvernance (EDM)

| Objectif | Intitule | Description |
|---|---|---|
| **EDM01** | Governance Framework | Definir et maintenir le cadre de gouvernance IT |
| **EDM02** | Benefits Delivery | S'assurer que les investissements IT generent la valeur attendue |
| **EDM03** | Risk Optimization | S'assurer que les risques IT sont identifies et geres |
| **EDM04** | Resource Optimization | S'assurer que les ressources IT sont utilisees efficacement |
| **EDM05** | Stakeholder Transparency | Garantir la transparence envers les parties prenantes |

### Utilisation pratique de COBIT

COBIT est particulierement utile pour :
- **Audit IT** : COBIT est le referentiel de facto pour les auditeurs IT (ISACA). Chaque objectif est assorti de metriques, d'activites et de roles.
- **Alignement IT/business** : le cascade model de COBIT lie les objectifs d'entreprise aux objectifs IT.
- **Conformite** : COBIT integre des mappings avec ISO 27001, ITIL, NIST, RGPD, facilitant la demonstration de conformite.
- **Benchmarking** : les niveaux de capacite (0 a 5 par processus) permettent de se comparer et de fixer des cibles.

### COBIT vs ITIL : complementarite

| Dimension | COBIT 2019 | ITIL 4 |
|---|---|---|
| **Focus** | Gouvernance (quoi et pourquoi) | Management des services (comment) |
| **Audience** | Direction, audit, compliance | Equipes IT operationnelles |
| **Granularite** | Objectifs et metriques | Pratiques et processus |
| **Complementarite** | Definit les objectifs de gouvernance | Fournit les pratiques pour atteindre les objectifs |

Recommandation : utiliser COBIT pour le cadre de gouvernance et le reporting a la direction, ITIL 4 pour l'operationnalisation des services IT. Les deux se completent naturellement.

---

## Budget IT & TCO

### Structure du budget IT

Decomposer le budget IT en trois enveloppes :

| Enveloppe | Description | Cible (% du budget IT) |
|---|---|---|
| **Run** | Maintien en condition operationnelle (infra, licences, support, salaires ops) | 50-60% |
| **Build** | Projets de transformation (nouveaux systemes, migrations, integrations) | 25-35% |
| **Transform** | Innovation et modernisation (PoC, R&D IT, veille techno) | 5-15% |

### Benchmarks du ratio IT/CA par secteur

| Secteur | Ratio IT/CA moyen | Leaders |
|---|---|---|
| Banque / Finance | 7-12% | 10-15% |
| Assurance | 5-8% | 8-12% |
| Tech / Digital | 10-20% | 15-25% |
| Industrie / Manufacturing | 2-4% | 4-6% |
| Retail / Distribution | 2-4% | 4-7% |
| Sante | 3-6% | 5-8% |
| Services | 4-7% | 6-10% |
| Secteur public | 3-6% | 5-8% |

### Calcul du TCO (Total Cost of Ownership)

Le TCO d'une application ou d'un service IT comprend :

```
TCO = Couts d'acquisition + Couts d'implementation + Couts operationnels annuels x duree + Couts de sortie

Couts d'acquisition :
  - Licences logicielles ou abonnements SaaS
  - Materiel / infrastructure initiale
  - Couts de conseil et d'integration

Couts d'implementation :
  - Configuration et personnalisation
  - Migration de donnees
  - Tests et recette
  - Formation initiale
  - Conduite du changement

Couts operationnels annuels :
  - Maintenance et support (editeur + interne)
  - Infrastructure (hebergement, reseau, stockage)
  - Licences recurrentes
  - Personnel dedie (administration, support L2/L3)
  - Evolution et correctifs
  - Formation continue

Couts de sortie :
  - Migration vers une solution de remplacement
  - Export et conversion des donnees
  - Decommissionnement
  - Penalites contractuelles eventuelles
```

### FinOps et pilotage des couts cloud

Le FinOps (Financial Operations) est la discipline de gestion financiere du cloud. Les principes cles :

1. **Visibilite** : taguer systematiquement toutes les ressources cloud (par equipe, projet, environnement, centre de cout). Sans tagging, pas de FinOps.
2. **Optimisation** : rightsizing (ajuster la taille des instances), reserved instances / savings plans (engagement 1-3 ans pour 30-60% de reduction), spot instances (workloads tolerants aux interruptions).
3. **Gouvernance** : alertes de budget, politiques d'auto-shutdown (environnements de dev/test), revues mensuelles des couts par equipe.
4. **Culture** : responsabiliser les equipes sur leurs couts cloud. Rendre les couts visibles et attribuables.

Outils recommandes : AWS Cost Explorer / Budgets, Azure Cost Management, GCP Billing, Apptio Cloudability, CAST AI, Kubecost (pour Kubernetes).

---

## Vendor Management (Gestion des fournisseurs IT)

### Framework de gestion des fournisseurs

Classifier les fournisseurs selon leur criticite et leur impact strategique :

| Categorie | Criticite | Relation | Exemples |
|---|---|---|---|
| **Strategique** | Tres elevee, remplacement couteux | Partenariat long terme | ERP (SAP), cloud provider principal, ITSM platform |
| **Tactique** | Elevee, impact operationnel | Contrat structure | Integrators, cybersecurite, telecom |
| **Operationnel** | Moyenne, remplacable | Gestion standard | Bureautique, peripheriques, cablage |
| **Commodite** | Faible, facilement substituable | Appel d'offre | Fournitures, petit materiel |

### Bonnes pratiques de vendor management

- **Contrat-cadre** : negocier des contrats pluriannuels avec SLA, penalites et clauses de reversibilite pour les fournisseurs strategiques et tactiques.
- **Revue de performance** : revue trimestrielle des SLA, de la satisfaction et de la qualite de service pour les fournisseurs strategiques.
- **Plan de sortie** : pour chaque fournisseur strategique, documenter un plan de sortie (reversibilite) avec estimation de cout et de delai. Le tester periodiquement.
- **Diversification** : eviter la dependance a un seul fournisseur pour un domaine critique. Avoir au minimum un plan B evalue.
- **Gouvernance des contrats** : maintenir un registre centralise des contrats IT (echeances, montants, responsables, clauses cles).

### Multi-sourcing et vendor lock-in

Le multi-sourcing permet de repartir les risques mais augmente la complexite de gestion. Recommandations :
- **Cloud** : privilegier un cloud principal (70-80% des workloads) + un cloud secondaire pour les workloads specifiques ou la resilience. Le vrai multi-cloud a 50/50 est rarement justifie.
- **ERP** : un seul ERP coeur, eviter la multiplication des solutions. Les integrations sont plus couteuses que les licences.
- **Services manages** : utiliser les services natifs du cloud provider pour la productivite, mais abstraire les couches critiques (bases de donnees, messaging) si la portabilite est un enjeu.

---

## Gouvernance du Shadow IT

### Definition et ampleur

Le shadow IT designe l'ensemble des solutions technologiques (applications SaaS, outils, scripts, bases de donnees) utilisees par les collaborateurs sans validation ni visibilite de la DSI. Selon les etudes (Gartner, Everest Group), 30 a 50% des depenses IT d'une organisation sont du shadow IT.

### Risques du shadow IT non gouverne

- **Securite** : donnees sensibles dans des applications non securisees, pas de chiffrement, pas de gestion des acces.
- **Conformite** : violations RGPD (donnees personnelles dans des SaaS non conformes), non-respect des politiques internes.
- **Doublons** : plusieurs equipes paient pour des outils equivalents sans le savoir.
- **Integration** : silos de donnees, pas d'interoperabilite avec le SI officiel.
- **Continuite** : dependance a des outils non maintenus, pas de backup, depart du "key user".

### Strategie de gouvernance du shadow IT

Ne pas interdire le shadow IT (c'est inefficace et contre-productif). Adopter une strategie en quatre axes :

1. **Decouvrir** : utiliser un outil de CASB (Cloud Access Security Broker) ou de SaaS management (Productiv, Zylo, Torii) pour identifier les applications SaaS utilisees. Analyser les flux DNS et les depenses par carte bancaire.
2. **Evaluer** : classifier chaque application decouverte (risque securitaire, conformite RGPD, valeur metier, alternatives dans le SI officiel).
3. **Integrer ou retirer** : pour les applications a forte valeur, les integrer dans le SI officiel (SSO, provisioning, backup). Pour les doublons ou les risques eleves, proposer une alternative officielle et accompagner la migration.
4. **Faciliter** : mettre en place un processus d'onboarding SaaS rapide (< 5 jours ouvrables) pour que les metiers puissent obtenir de nouveaux outils sans contourner la DSI. Creer un catalogue de services SaaS pre-approuves.

---

## Portefeuille Applicatif (Application Portfolio Management)

### Cartographie du portefeuille

Maintenir un inventaire structure de toutes les applications :

| Champ | Description |
|---|---|
| Nom de l'application | Identifiant unique |
| Editeur / Type | Commercial, open source, developpement interne |
| Fonction metier | Domaine fonctionnel couvert |
| Criticite (T1/T2/T3) | Impact en cas d'indisponibilite |
| Nombre d'utilisateurs | Actifs sur les 90 derniers jours |
| Cout annuel (TCO) | Licences + infra + support + personnel |
| Age / Version | Date de mise en service, version actuelle |
| Score de dette technique | Evaluation 1-5 de l'obsolescence |
| Statut de vie | Invest / Maintain / Migrate / Retire |
| Responsable metier | Product owner ou sponsor metier |
| Responsable IT | Administrateur ou equipe support |

### Matrice TIME (Tolerate, Invest, Migrate, Eliminate)

Classifier chaque application selon sa valeur metier et sa qualite technique :

```
        Qualite technique elevee
              |
   INVEST     |  TOLERATE
   (evoluer,  |  (maintenir,
    enrichir) |   faible priorite)
              |
--------------+---------------
   MIGRATE    |  ELIMINATE
   (remplacer |  (retirer,
    par mieux) |  decommissionner)
              |
        Valeur metier elevee
```

- **Invest** : application strategique en bon etat technique. Continuer a investir et a enrichir.
- **Tolerate** : application correcte techniquement mais a faible valeur metier. Maintenir a moindre cout.
- **Migrate** : application a forte valeur metier mais en mauvais etat technique. Planifier la migration ou la refonte.
- **Eliminate** : application obsolete a faible valeur. Decommissionner et migrer les donnees.

### Rationalisation du portefeuille

Objectif type : reduire le nombre d'applications de 20 a 40% sur 3 ans. Strategies :
- **Consolidation fonctionnelle** : remplacer plusieurs outils faisant la meme chose par un seul (ex : 5 outils de gestion de projet -> 1 plateforme).
- **Modernisation** : migrer les applications legacy critiques vers des plateformes modernes (cloud-native, API-first).
- **Decommissionnement** : retirer les applications sans utilisateur actif ou avec < 10 utilisateurs (sauf obligations reglementaires).
- **SaaS-ification** : remplacer les applications on-premise non critiques par des equivalents SaaS (moins de maintenance, mises a jour automatiques).

---

## State of the Art (2024-2026)

### Tendances majeures en gouvernance IT

1. **Platform Engineering et Internal Developer Platforms (IDP)** : la DSI evolue d'un role de fournisseur de services vers un role de fournisseur de plateforme. Les IDP (Backstage, Port, Kratix) permettent aux equipes de developper, deployer et operer leurs applications en self-service sur des rails pre-configures. Cela reduit le time-to-market tout en maintenant la gouvernance.

2. **FinOps mature et GreenOps** : le FinOps n'est plus optionnel pour les organisations cloud. La discipline se structure autour du standard FOCUS (FinOps Open Cost and Usage Specification) pour normaliser les donnees de couts multi-cloud. Le GreenOps ajoute la dimension environnementale : mesurer et reduire l'empreinte carbone du SI (scope 1-2-3 IT), optimiser la consommation energetique des datacenters et du cloud.

3. **ITIL 4 + AI-driven ITSM** : ITIL 4 integre progressivement les capacites IA dans ses pratiques. Les plateformes ITSM (ServiceNow, BMC, Ivanti) deploient des assistants IA generative pour la categorisation automatique des tickets, la resolution guidee, la generation de knowledge articles et la prediction d'incidents. La convergence ITSM/ESM s'accelere : les pratiques IT s'etendent a toute l'entreprise.

4. **Composable Enterprise Architecture** : l'architecture d'entreprise evolue vers une approche composable : les systemes monolithiques sont remplaces par des assemblages de composants modulaires (microservices, API, event-driven) qui peuvent etre recombines rapidement pour repondre aux evolutions metier. Les architectures MACH (Microservices, API-first, Cloud-native, Headless) se generalisent dans le commerce et le contenu.

5. **Souverainete numerique et cloud souverain** : en Europe, la pression reglementaire (RGPD, NIS2, DORA, Data Act) et geopolitique pousse a l'adoption de solutions souveraines. Les offres de cloud souverain (OVHcloud, Scaleway, S3NS [GCP], Bleu [Azure/Orange/Capgemini]) se structurent pour les secteurs regules et le secteur public. Le label SecNumCloud de l'ANSSI devient un critere de selection incontournable.

6. **IT as a Product** : la DSI adopte le product management pour gerer ses services IT. Chaque service IT majeur a un product owner, une roadmap, des metriques d'usage et de satisfaction, un backlog priorise. L'IT ne "delivre pas des projets", il "evolue des produits". Ce changement de posture transforme la relation IT/metiers.

7. **Automation-First Operations** : l'automatisation n'est plus une optimisation, c'est le mode par defaut. Infrastructure as Code (Terraform, Pulumi), GitOps (ArgoCD, Flux), policy-as-code (OPA, Kyverno), configuration management automatise. Les equipes IT qui ne codifient pas leurs operations accusent un retard croissant en termes de fiabilite, de securite et de vitesse.

8. **Observability-Driven IT** : les tableaux de bord IT evoluent de la supervision classique (up/down) vers l'observabilite (metriques, logs, traces) avec des plateformes comme Datadog, Grafana, Dynatrace. L'AIOps (Moogsoft, BigPanda, ServiceNow ITOM AI) permet la correlation automatique d'alertes, la detection d'anomalies et la remediation assistee.

### Evolution des roles IT

| Role emergent | Description |
|---|---|
| **Platform Engineer** | Construit et maintient les plateformes self-service internes |
| **FinOps Practitioner** | Optimise les couts cloud et instille la culture FinOps |
| **Cloud Security Architect** | Concoit la securite des architectures cloud et multi-cloud |
| **SRE (Site Reliability Engineer)** | Garantit la fiabilite des services via l'ingenierie |
| **AI/ML Engineer (IT Ops)** | Deploie l'IA dans les operations IT (AIOps, chatbot ITSM) |
| **Digital Workplace Manager** | Pilote l'experience collaborateur numerique (poste de travail, outils collaboratifs) |
