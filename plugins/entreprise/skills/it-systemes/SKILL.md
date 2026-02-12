---
name: it-systemes
description: This skill should be used when the user asks about "IT governance", "ITIL framework", "cloud strategy", "ERP implementation", "cybersecurity governance", "gouvernance IT", "gouvernance informatique", "stratégie cloud", "migration cloud", "implémentation ERP", "SAP", "Salesforce", "IT service management", "ITSM", "COBIT", "infrastructure informatique", "IT infrastructure", "vendor management", "gestion des fournisseurs IT", "digital workplace", "environnement de travail numérique", "shadow IT", "IT asset management", "CMDB", "incident management", "gestion des incidents", "disaster recovery", "PRA", "PCA", "SLA", "helpdesk", "ticketing", "TOGAF", "architecture d'entreprise", discusses IT service management, COBIT, or needs guidance on IT infrastructure, vendor management, or digital workplace.
version: 1.0.0
---

# IT / Data / Systemes — Gouvernance IT, Infrastructure, Cybersecurite & Applications Metier

## Overview

**FR** — Cette skill couvre l'ensemble des disciplines de la DSI (Direction des Systemes d'Information) : gouvernance IT et strategie numerique, infrastructure et cloud, cybersecurite (gouvernance), applications metier (ERP/CRM/RPA) et gestion des services IT (ITSM). L'objectif est de fournir des recommandations actionnables et alignees avec les meilleures pratiques 2024-2026, incluant les evolutions majeures : adoption du FinOps et du GreenOps, strategies multi-cloud matures, conformite NIS2 et DORA, migration SAP S/4HANA, convergence ITSM/ESM pilotee par l'IA, et montee en puissance du platform engineering cote infrastructure. Ce skill adopte la perspective du DSI/CIO et de ses equipes. Le volet analytics/data est couvert dans "Data & BI", et l'implementation technique/code dans "Code Development".

**EN** — This skill covers the full scope of CIO-level disciplines: IT governance and digital strategy, infrastructure and cloud, cybersecurity governance, business applications (ERP/CRM/RPA), and IT service management (ITSM). The goal is to provide actionable recommendations aligned with 2024-2026 best practices, including major evolutions: FinOps and GreenOps adoption, mature multi-cloud strategies, NIS2 and DORA compliance, SAP S/4HANA migration, AI-driven ITSM/ESM convergence, and the rise of platform engineering for infrastructure. This skill adopts the CIO perspective. Data analytics is covered in "Data & BI", and technical implementation in "Code Development".

---

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Gouvernance IT et strategie numerique** : elaboration ou revue du SDSI (Schema Directeur des Systemes d'Information), alignement IT/business, mise en oeuvre d'ITIL 4 ou COBIT 2019, pilotage du budget IT et du TCO, gestion du portefeuille applicatif, gouvernance du shadow IT.
- **Infrastructure et cloud** : definition de la strategie cloud (IaaS/PaaS/SaaS), choix et migration entre cloud providers (AWS, GCP, Azure, OVH/Scaleway), architecture reseau, virtualisation et conteneurisation, plan de reprise d'activite (PRA/PCA), edge computing, FinOps et optimisation des couts cloud.
- **Cybersecurite (gouvernance)** : mise en place ou amelioration d'un SMSI (ISO 27001/27701), analyse de risques (EBIOS RM, ISO 27005), politiques de securite (PSSI), sensibilisation, reponse aux incidents, conformite reglementaire (RGPD, NIS2, DORA, SOC 2, HDS).
- **Applications metier** : selection, implementation ou optimisation d'un ERP (SAP S/4HANA, Oracle, Dynamics 365, Odoo), administration CRM, deploiement RPA/low-code/no-code, integration via iPaaS (MuleSoft, Workato, Boomi), gestion du cycle de vie applicatif (ALM).
- **Gestion des services IT (ITSM)** : organisation du service desk (L1/L2/L3), gestion des changements IT (CAB), CMDB et gestion de la configuration, problem management, knowledge management, gestion des actifs IT (ITAM), evolution vers l'ESM (Enterprise Service Management).

---

## Core Principles

### Principle 1 — Aligner le SI sur la strategie metier

Le systeme d'information n'est pas une fonction support : c'est un levier strategique. Chaque investissement IT doit se justifier par sa contribution a un objectif metier mesurable. Construire le SDSI comme une traduction operationnelle de la strategie d'entreprise, pas comme un catalogue de projets techniques. Evaluer chaque initiative IT sur trois axes : valeur metier, risque, et faisabilite technique. Refuser les projets purement technologiques sans sponsor metier identifie.

### Principle 2 — Industrialiser par les frameworks, pas par l'improvisation

Adopter des referentiels eprouves (ITIL 4, COBIT 2019, ISO 27001, TOGAF) comme fondations, puis les adapter au contexte de l'organisation. Ne jamais implementer un framework a 100% par dogmatisme : selectionner les pratiques qui generent le plus de valeur pour le niveau de maturite actuel. Un processus documete, mesure et ameliore en continu vaut mieux qu'une certification sans pratique reelle.

### Principle 3 — Securiser par conception, pas en reaction

Integrer la securite des la phase de conception de tout projet IT (Security by Design). La cybersecurite n'est pas un sujet technique reserve au RSSI : c'est un enjeu de gouvernance porte par la direction. Appliquer le principe de defense en profondeur : aucune couche unique de securite ne suffit. La conformite reglementaire (NIS2, DORA, RGPD) est un minimum, pas un objectif.

### Principle 4 — Privilegier le cloud-smart au cloud-first

Ne pas migrer vers le cloud par dogme, mais par analyse rigoureuse du rapport cout/benefice/risque pour chaque workload. Adopter une approche cloud-smart : certains workloads justifient le cloud public, d'autres le cloud prive ou l'on-premise. Maitriser le FinOps pour eviter l'explosion des couts. Anticiper la reversibilite et le vendor lock-in des la conception.

### Principle 5 — Mesurer pour piloter

Ce qui ne se mesure pas ne se pilote pas. Definir des KPIs clairs pour chaque domaine IT : disponibilite des services, temps de resolution des incidents, couts par service, taux de conformite, dette technique, satisfaction utilisateur. Utiliser les tableaux de bord IT comme outils de dialogue avec la direction, pas comme exercices de reporting.

### Principle 6 — Automatiser les operations, humaniser les decisions

Automatiser les taches repetitives et a faible valeur ajoutee (provisioning, patching, incidents L1, deploiements). Liberer les equipes IT pour les activites a forte valeur : architecture, securite, innovation, accompagnement des metiers. L'IA generative transforme l'ITSM : l'exploiter pour la resolution automatisee, la base de connaissances et l'analyse predictive, tout en maintenant la supervision humaine sur les decisions critiques.

---

## Key Frameworks & Methods

| Framework / Method | Purpose | FR |
|---|---|---|
| **ITIL 4** | Service management lifecycle and value system | Systeme de valeur pour la gestion des services IT |
| **COBIT 2019** | IT governance and management objectives | Objectifs de gouvernance et de management IT |
| **TOGAF / Urbanisme SI** | Enterprise architecture framework | Cadre d'architecture d'entreprise |
| **ISO 27001 / 27701** | Information security / Privacy management system | Systeme de management de la securite / Vie privee |
| **EBIOS RM** | Cyber risk assessment (ANSSI method) | Analyse de risques cyber (methode ANSSI) |
| **ISO 20000** | IT service management standard | Norme de gestion des services IT |
| **FinOps (FOCUS)** | Cloud financial management | Gestion financiere du cloud |
| **NIST CSF** | Cybersecurity framework (Identify, Protect, Detect, Respond, Recover) | Cadre de cybersecurite |
| **SAFe / Agile IT** | Scaled agile for IT portfolio management | Agilite a l'echelle pour le portefeuille IT |

---

## Decision Guide

### Strategie cloud : quel modele pour quel workload ?

```
1. Le workload est-il critique metier ?
   +-- Oui -> exigences de SLA elevees
   |   +-- Donnees sensibles / reglementees ?
   |   |   +-- Oui -> Cloud prive ou cloud souverain (OVH, Scaleway, S3NS)
   |   |   +-- Non -> Cloud public avec architecture HA multi-AZ
   |   +-- Latence critique (< 10ms) ?
   |       +-- Oui -> Edge computing ou on-premise
   |       +-- Non -> Cloud public
   +-- Non -> Cloud public standard, optimiser les couts

2. Quel modele de service ?
   +-- Besoin de controle total sur l'OS/runtime ?
   |   +-- Oui -> IaaS (EC2, Compute Engine, VMs)
   |   +-- Non -> PaaS (App Engine, Azure App Service, Heroku)
   +-- Application standard ?
       +-- Oui -> SaaS (O365, Salesforce, ServiceNow)
       +-- Non -> PaaS ou containers (EKS, GKE, AKS)

3. Multi-cloud ou single-cloud ?
   +-- Risque vendor lock-in inacceptable ? -> Multi-cloud avec abstraction
   +-- Equipe < 20 personnes IT ? -> Single-cloud (reduire la complexite)
   +-- Contraintes reglementaires multi-juridiction ? -> Multi-cloud
```

### Choix d'un ERP

| Critere | SAP S/4HANA | Oracle Cloud ERP | Dynamics 365 | Odoo |
|---|---|---|---|---|
| **Taille entreprise** | Grande / ETI | Grande / ETI | ETI / PME | PME / Startup |
| **Complexite metier** | Tres elevee | Elevee | Moyenne-Elevee | Moyenne |
| **Ecosysteme Microsoft** | Independant | Independant | Integration native | Independant |
| **Cout de mise en oeuvre** | 500k-50M EUR | 300k-30M EUR | 100k-10M EUR | 20k-2M EUR |
| **Time to deploy** | 12-36 mois | 9-24 mois | 6-18 mois | 3-12 mois |
| **Open source** | Non | Non | Non | Oui (core) |

### Selection d'un referentiel de securite

- **ISO 27001** : incontournable pour toute organisation souhaitant structurer sa securite. Prerequis pour les certifications sectorielles (HDS, SOC 2). Privilegier si l'objectif est la certification formelle.
- **NIST CSF** : plus flexible, ideal pour un premier cadrage ou pour des organisations internationales. Complementaire a ISO 27001.
- **EBIOS RM** : methode de reference francaise (ANSSI) pour l'analyse de risques. Obligatoire pour les OIV/OSE. A utiliser pour les analyses de risques approfondies sur les systemes critiques.
- **SOC 2** : indispensable pour les editeurs SaaS et les fournisseurs de services. Type II prefere au Type I pour la credibilite.

---

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **IT Portfolio Management** : classifier chaque application (invest, maintain, migrate, retire) et calculer le TCO reel (licences + infra + support + dette technique).
- **Cloud Landing Zone** : preparer l'environnement cloud avant migration (VPC, IAM, tagging, FinOps, guardrails). Utiliser les blueprints natifs (AWS Control Tower, Azure Landing Zones, GCP Foundation Toolkit).
- **Shift-Left Security** : integrer les controles de securite dans le pipeline CI/CD (SAST/DAST, scan de vulnerabilites, conformite des configurations).
- **ITSM-to-ESM Expansion** : etendre les pratiques ITSM a l'ensemble de l'entreprise (RH, finance, juridique, facilities).
- **Infrastructure as Code (IaC)** : coder l'infrastructure (Terraform, Pulumi). Versionner et tester comme du code applicatif.
- **Zero Trust Architecture** : "never trust, always verify" — micro-segmentation, MFA generalisee, ZTNA.

### Anti-patterns critiques

- **Shadow IT non gouverne** : repondre par un processus d'onboarding SaaS rapide (< 5 jours), pas par l'interdiction.
- **Migration cloud "lift & shift" brute** : evaluer chaque application avec les 6R (Retain, Retire, Rehost, Replatform, Refactor, Repurchase) avant migration.
- **Cybersecurite par la peur** : privilegier une culture positive de la securite basee sur la responsabilisation.
- **ITIL comme bureaucratie** : ITIL 4 est un systeme de valeur, pas un ensemble de formulaires. Adapter au contexte.
- **ERP Big Bang sans change management** : deployer par vagues avec un programme de conduite du changement structure (15-20% du budget).
- **CMDB fantome** : automatiser la decouverte (ServiceNow Discovery, Device42). Une CMDB non fiable est pire que pas de CMDB.

---

## Implementation Workflow

### Phase 1 — Diagnostic & Vision (Semaines 1-6)

1. Realiser un audit de maturite IT sur 5 domaines (gouvernance, infrastructure, securite, applications, ITSM) avec un modele CMM (niveaux 1 a 5).
2. Cartographier le portefeuille applicatif : criticite, dette technique, couts.
3. Evaluer la posture de securite (gap analysis ISO 27001) et la performance ITSM.
4. Analyser les couts IT (run vs build vs transform), le ratio IT/CA, les benchmarks sectoriels.
5. Definir la vision IT cible a 3 ans alignee sur la strategie d'entreprise.

### Phase 2 — Schema Directeur SI (Semaines 7-14)

6. Elaborer le SDSI : trajectoire de transformation sur 3 ans, structure en vagues.
7. Definir l'architecture cible (cloud strategy, plateformes, patterns d'integration) et prioriser les chantiers.
8. Construire le business case consolide et valider avec la direction generale.

### Phase 3 — Fondations & Quick Wins (Mois 4-9)

9. Deployer les cloud landing zones, renforcer le SMSI (ISO 27001), moderniser le service desk.
10. Lancer la rationalisation applicative et les premieres automatisations (IaC, RPA).

### Phase 4 — Transformation & Scaling (Mois 9-24)

11. Executer les migrations cloud par vagues et deployer/migrer l'ERP.
12. Implementer la conformite reglementaire (NIS2, DORA) et industrialiser l'ITSM (CMDB, ITAM, FinOps).

### Phase 5 — Optimisation & Innovation (Mois 24+)

13. Etendre l'ESM, integrer l'IA dans les operations IT (AIOps, chatbot ITSM).
14. Evoluer vers Zero Trust complet, FinOps mature, GreenOps et piloter le SI comme un produit.

---

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[IT Governance & Strategy](./references/it-governance-strategy.md)** — SDSI (elaboration, structure, pilotage), ITIL 4 (Service Value System, pratiques cles), COBIT 2019 (objectifs de gouvernance et de management), budget IT et TCO, gestion des fournisseurs IT, gouvernance du shadow IT, portefeuille applicatif.

- **[Infrastructure & Cloud](./references/infrastructure-cloud.md)** — Strategie cloud (IaaS/PaaS/SaaS), comparatif AWS/GCP/Azure/OVH, multi-cloud et cloud souverain, architecture reseau, virtualisation et conteneurisation, PRA/PCA et DR, edge computing, FinOps/FOCUS, GreenOps, platform engineering.

- **[Cybersecurity Governance](./references/cybersecurity-governance.md)** — ISO 27001/27701 (SMSI, implementation), EBIOS RM et ISO 27005 (analyse de risques), politiques de securite (PSSI), sensibilisation, reponse aux incidents (CSIRT), conformite reglementaire (RGPD, NIS2, DORA, SOC 2, HDS), Zero Trust.

- **[ERP & ITSM](./references/erp-itsm.md)** — ERP (SAP S/4HANA, Oracle, Dynamics 365, Odoo), CRM administration, RPA/low-code/no-code, integration et iPaaS (MuleSoft, Workato, Boomi), service desk (L1/L2/L3), change management IT (CAB), CMDB, problem management, knowledge management, ITAM, ESM.
