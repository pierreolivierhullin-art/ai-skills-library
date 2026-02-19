# AWS, GCP & Azure — Comparaison, Services Clés & Guide de Sélection

## Overview

Ce guide compare les trois principaux fournisseurs de cloud public — Amazon Web Services (AWS), Google Cloud Platform (GCP) et Microsoft Azure — en détaillant leurs services clés par catégorie, leurs forces et faiblesses, et les critères pour choisir le bon provider selon le contexte. L'objectif est de fournir une grille de décision objective basée sur les cas d'usage réels, pas sur le marketing.

---

## Vue d'Ensemble des Fournisseurs

### Parts de Marché et Positionnement (2025-2026)

| Indicateur | AWS | GCP | Azure |
|---|---|---|---|
| **Part de marché** | ~32% | ~11% | ~22% |
| **Revenus annuels (cloud)** | ~100 Mds USD | ~40 Mds USD | ~75 Mds USD |
| **Nombre de régions** | 34+ | 42+ | 60+ |
| **Zones de disponibilité** | 108+ | 127+ | 3 par région |
| **Certifications compliance** | 300+ | 150+ | 100+ |
| **Positionnement** | Leader généraliste | Leader data/ML | Leader entreprise |

### Forces distinctives

**AWS** : L'écosystème le plus large avec 200+ services, la meilleure maturité des services, la communauté la plus grande. Idéal pour les startups qui démarrent sur le cloud et les organisations cherchant la polyvalence maximale.

**GCP** : Supériorité sur les services de données et d'IA (BigQuery, Vertex AI, Cloud Run), réseau premium mondial, Kubernetes nativement (créateur de Kubernetes). Idéal pour les workloads data-intensive et les organisations avec des besoins ML avancés.

**Azure** : Intégration native avec l'écosystème Microsoft (Active Directory, Office 365, Windows Server), support hybride avec Azure Arc, présence enterprise forte. Idéal pour les entreprises utilisant déjà massivement Microsoft.

---

## Comparaison par Catégorie de Service

### Compute

| Service | AWS | GCP | Azure |
|---|---|---|---|
| **Machines virtuelles** | EC2 (le plus de types) | Compute Engine | Azure VMs |
| **Conteneurs managés** | ECS, EKS | GKE (le meilleur K8s) | AKS |
| **Serverless functions** | Lambda (référence) | Cloud Functions / Cloud Run | Azure Functions |
| **Serverless containers** | AWS App Runner, Fargate | Cloud Run (excellent) | Azure Container Apps |
| **PaaS applicatif** | Elastic Beanstalk | App Engine | Azure App Service |
| **Batch computing** | AWS Batch | Cloud Batch | Azure Batch |

**Recommandation** :
- Pour Kubernetes : GKE offre la meilleure expérience avec autopilot et les mises à jour automatiques.
- Pour serverless sans gestion de serveurs : Cloud Run (GCP) est le plus flexible (containers, pas de timeout de 15 min comme Lambda).
- Pour la variété des types d'instances EC2 : AWS gagne largement (instances GPU, FPGA, instances optimisées mémoire).

### Base de Données

| Type | AWS | GCP | Azure |
|---|---|---|---|
| **Relationnelle managée** | RDS (PostgreSQL, MySQL, Oracle) | Cloud SQL | Azure Database |
| **Relationnelle haute perf** | Aurora (MySQL/PostgreSQL compatible) | Cloud Spanner (distributed) | Azure SQL Hyperscale |
| **NoSQL document** | DynamoDB | Firestore, Cloud Bigtable | Cosmos DB |
| **Data Warehouse** | Redshift | BigQuery (le meilleur) | Azure Synapse |
| **Cache** | ElastiCache (Redis/Memcached) | Memorystore (Redis) | Azure Cache for Redis |
| **Vector database** | OpenSearch, pgvector via RDS | AlloyDB (pgvector) | Azure Cosmos DB |

**Recommandation** :
- Pour le data warehouse : BigQuery est le standard incontesté — serverless, séparation compute/storage, SQL standard, excellent pour l'analyse ad-hoc.
- Pour les bases relationnelles managées : Aurora PostgreSQL est supérieur à RDS PostgreSQL standard en termes de performance (3x Aurora vs RDS).
- Pour les workloads globaux distribués : Cloud Spanner (GCP) offre la cohérence forte globale unique sur le marché.

### Stockage

| Type | AWS | GCP | Azure |
|---|---|---|---|
| **Object storage** | S3 (référence mondiale) | Cloud Storage | Azure Blob Storage |
| **Block storage** | EBS | Persistent Disk | Azure Disk Storage |
| **File storage** | EFS, FSx | Filestore | Azure Files |
| **Archive** | S3 Glacier | Cloud Archive | Azure Archive Storage |

**Recommandation** : Les trois sont équivalents pour le stockage objet. Choisir selon le provider cloud principal. S3 a le plus large écosystème d'outils compatibles.

### Réseau

| Service | AWS | GCP | Azure |
|---|---|---|---|
| **Virtual Network** | VPC | VPC | Virtual Network (VNet) |
| **Load Balancer** | ALB, NLB, CLB | Cloud Load Balancing | Azure Load Balancer, App Gateway |
| **CDN** | CloudFront | Cloud CDN | Azure CDN |
| **DNS** | Route 53 | Cloud DNS | Azure DNS |
| **Interconnect** | Direct Connect | Cloud Interconnect | ExpressRoute |
| **VPN** | AWS VPN | Cloud VPN | Azure VPN Gateway |
| **Service Mesh** | AWS App Mesh | Traffic Director | Azure Service Fabric Mesh |

**Réseau GCP** : Le réseau privé mondial de Google (qui est aussi le réseau de YouTube et Google Search) est souvent meilleur en termes de latence et de throughput pour les communications inter-régions.

### Sécurité et IAM

| Service | AWS | GCP | Azure |
|---|---|---|---|
| **IAM** | AWS IAM | Cloud IAM | Azure Active Directory |
| **Gestion des secrets** | Secrets Manager, Parameter Store | Secret Manager | Azure Key Vault |
| **Chiffrement** | KMS | Cloud KMS | Azure Key Vault |
| **WAF** | AWS WAF | Cloud Armor | Azure WAF |
| **Audit logs** | CloudTrail | Cloud Audit Logs | Azure Activity Log |
| **Security posture** | Security Hub, GuardDuty | Security Command Center | Microsoft Defender for Cloud |
| **Compliance** | AWS Artifact | Google Compliance | Microsoft Compliance Manager |

**Différence clé IAM** : AWS utilise des policies JSON attachées aux entités. GCP utilise des bindings IAM sur les ressources. Azure AD est nettement plus complexe mais offre la meilleure intégration avec les environnements Microsoft existants.

### IA et Machine Learning

| Service | AWS | GCP | Azure |
|---|---|---|---|
| **Plateforme ML managée** | SageMaker | Vertex AI | Azure ML |
| **Data Warehouse + ML** | Redshift ML | BigQuery ML | Azure Synapse ML |
| **LLM / Foundation Models** | Amazon Bedrock | Vertex AI (Gemini) | Azure OpenAI Service |
| **Vision** | Rekognition | Vision AI | Azure Computer Vision |
| **NLP** | Comprehend | Natural Language API | Azure Language |
| **Speech** | Transcribe, Polly | Speech-to-Text, Text-to-Speech | Azure Speech |
| **Recommandations** | Personalize | Recommendations AI | Azure Personalizer |
| **Feature Store** | SageMaker Feature Store | Vertex Feature Store | Azure ML Feature Store |

**Recommandation** :
- Pour l'accès aux modèles OpenAI en production : Azure OpenAI Service est le seul à offrir GPT-4 avec SLAs enterprise.
- Pour le ML end-to-end : Vertex AI (GCP) est actuellement le plus intégré (pipelines, feature store, model registry, monitoring) dans un seul service.
- Pour SageMaker : puissant mais complexe, courbe d'apprentissage élevée.

### DevOps et CI/CD

| Service | AWS | GCP | Azure |
|---|---|---|---|
| **Registry de containers** | ECR | Artifact Registry | Azure Container Registry |
| **CI/CD** | CodePipeline, CodeBuild | Cloud Build | Azure DevOps, GitHub Actions |
| **Infrastructure as Code** | CloudFormation, AWS CDK | Terraform (compatible), Deployment Manager | ARM Templates, Bicep |
| **Secrets en CI** | AWS Secrets Manager + OIDC | Secret Manager + Workload Identity | Azure Key Vault + Managed Identity |

---

## Pricing Model et FinOps

### Structure de Pricing

**Modèles de facturation communs**

| Modèle | AWS | GCP | Azure |
|---|---|---|---|
| **On-demand** | Oui (tarif plein) | Oui (tarif plein) | Oui (tarif plein) |
| **Réservation 1 an** | Reserved Instances (40% off) | Committed Use Discounts (37% off) | Reserved VM Instances (36% off) |
| **Réservation 3 ans** | Reserved Instances (60% off) | Committed Use Discounts (55% off) | Reserved VM Instances (55% off) |
| **Spot / Preemptible** | Spot Instances (60-90% off) | Spot VMs (60-91% off) | Spot VMs (60-90% off) |
| **Réductions automatiques** | Non | Sustained Use Discounts (jusqu'à 30%) | Non |

**Sustained Use Discounts (GCP uniquement)** : GCP applique automatiquement des réductions allant jusqu'à 30% pour les VMs utilisées plus de 25% du mois — sans engagement ni configuration. Un avantage distinctif de GCP.

### Outils de FinOps par Provider

| Outil | AWS | GCP | Azure |
|---|---|---|---|
| **Visualisation des coûts** | Cost Explorer | Cloud Billing | Azure Cost Management |
| **Budget et alertes** | AWS Budgets | Cloud Billing Budgets | Azure Budgets |
| **Recommandations** | Trusted Advisor, Compute Optimizer | Recommender | Azure Advisor |
| **Tags pour allocation** | AWS Tags | Labels | Azure Tags |

### Stratégie FinOps Multi-Cloud

**Outils tiers recommandés pour la visibilité unifiée** :
- **CloudCost** : Dashboard multi-cloud open source
- **Infracost** : Estimation du coût lors du développement IaC
- **OpenCost** : Attribution des coûts Kubernetes par workload

**Règles FinOps universelles** :
1. Tagger toutes les ressources dès la création (environment, team, project, cost-center)
2. Configurer des budgets avec alertes à 50%, 80%, 100%
3. Acheter des réservations pour les workloads stables (économie 40-70%)
4. Utiliser des Spot/Preemptible pour les workloads tolérantes aux interruptions
5. Arrêter les environnements non-production en dehors des heures de bureau (économie ~65%)
6. Revoir le rightsizing mensuellement avec les outils de recommandation natifs

---

## Cas d'Usage et Recommandations par Profil

### Startup SaaS B2B

**Recommandation : AWS**
- Écosystème le plus large pour les intégrations tierces
- Aurora PostgreSQL pour la base de données relationnelle
- Lambda + API Gateway pour le backend serverless
- S3 pour le stockage, CloudFront pour le CDN
- GitHub Actions pour le CI/CD
- Coût initial : EC2 t3.medium (~30 USD/mois), Aurora Serverless (pay-per-request)

### Organisation Enterprise avec Stack Microsoft

**Recommandation : Azure**
- Azure Active Directory pour l'authentification (SSO avec Office 365)
- Azure SQL pour les bases relationnelles, Cosmos DB pour le NoSQL
- Azure DevOps ou GitHub Enterprise (Microsoft) pour le CI/CD
- Azure OpenAI Service pour l'intégration des LLM
- ExpressRoute pour la connectivité hybride avec le datacenter on-premise

### Équipe Data-First (Data Engineering + ML)

**Recommandation : GCP**
- BigQuery pour le data warehouse (serverless, SQL, ML intégré)
- Cloud Storage pour le data lake
- Dataflow (Apache Beam) ou Dataproc (Spark) pour les pipelines
- Vertex AI pour le ML platform
- Cloud Run pour les APIs de serving de modèles
- Artifact Registry + Cloud Build pour le CI/CD

### Application Globale à Faible Latence

**Recommandation : GCP ou AWS**
- GCP : réseau privé mondial, anycast CDN, Cloud CDN avec edge nodes dans 160+ villes
- AWS : CloudFront (450+ points of presence), Global Accelerator pour les applications TCP/UDP
- Azure : Azure CDN avec Verizon ou Akamai en option

### Workloads GPU / HPC

**Recommandation : AWS ou GCP**
- AWS : p4d.24xlarge (8x A100), p3.16xlarge (8x V100), Trainium/Inferentia pour les LLM
- GCP : TPU v4 (Google exclusif pour le ML), A100/H100 disponibles
- Azure : ND96asr_v4 (8x A100), NDm A100 v4

---

## Migration Cloud

### Stratégies de Migration (les 6 R)

| Stratégie | Description | Délai | Risque | Cas d'usage |
|---|---|---|---|---|
| **Rehost (Lift & Shift)** | Migration sans changement de l'application | Rapide | Faible | Legacy apps, migration d'urgence |
| **Replatform** | Migration avec optimisations mineures (ex: RDS au lieu de MySQL self-hosted) | Moyen | Faible | Réduire les coûts OPS sans refactoring |
| **Repurchase** | Passer à un SaaS (ex: Salesforce au lieu d'un CRM on-prem) | Moyen | Moyen | Remplacement d'applications standard |
| **Refactor / Re-architect** | Réécriture en cloud-native (microservices, serverless) | Long | Élevé | Applications critiques avec fort ROI |
| **Retain** | Garder on-premise (trop complexe ou non éligible) | N/A | N/A | Applications dépendantes du matériel |
| **Retire** | Décommissionner l'application | Rapide | Faible | Applications obsolètes ou doublons |

### Checklist de Migration

```
Avant la migration
[ ] Inventaire complet des applications et leurs dépendances
[ ] Évaluation du modèle de migration pour chaque application (6 R)
[ ] Évaluation des contraintes de conformité et de souveraineté des données
[ ] Calcul du TCO cloud vs on-premise sur 3 ans
[ ] Plan de formation des équipes

Pendant la migration
[ ] Architecture de migration documentée et validée
[ ] Environnement cloud de landing zone (réseau, IAM, sécurité) provisionné via IaC
[ ] Tests de performance et de charge en cloud staging
[ ] Plan de rollback documenté et testé
[ ] Monitoring configuré avant le basculement

Après la migration
[ ] Validation des performances en production cloud
[ ] Audit des coûts et rightsizing initial
[ ] Décommissionnement progressif des ressources on-premise
[ ] Optimisation continue (FinOps, réservations)
```

---

## Compliance et Certifications

### Certifications communes

| Certification | AWS | GCP | Azure |
|---|---|---|---|
| **ISO 27001** | Oui | Oui | Oui |
| **SOC 2 Type II** | Oui | Oui | Oui |
| **PCI DSS Level 1** | Oui | Oui | Oui |
| **HIPAA** | Oui (BAA disponible) | Oui (BAA disponible) | Oui (BAA disponible) |
| **RGPD** | Conformant | Conformant | Conformant |
| **HDS (France)** | Oui | Oui | Oui |
| **SecNumCloud (France)** | En cours | En cours | Non |
| **FedRAMP (US Gov)** | High | High | High |

### Souveraineté des Données

**Enjeux de souveraineté** : Pour les données sensibles (personnelles, financières, de santé), s'assurer que les données ne quittent pas le territoire européen.

**Solutions** :
- **AWS EU Data Boundary** : Engagement contractuel que les données des clients UE restent dans les régions UE
- **GCP Data Residency** : Restriction de la localisation des données avec policies organisationnelles
- **Azure EU Data Boundary** : Programme dédié pour les données UE (Schengen)
- **Alternatives souveraines** : OVHcloud (SecNumCloud qualifié), Outscale (filiale Dassault), S3NS (Thales + GCP)

---

## Ressources et Outils de Comparaison

### Outils officiels de calcul des coûts

- **AWS Pricing Calculator** : calculator.aws.amazon.com
- **GCP Pricing Calculator** : cloud.google.com/products/calculator
- **Azure Pricing Calculator** : azure.microsoft.com/pricing/calculator

### Outils de veille et comparaison

- **CloudPrices.net** : Comparaison des prix des instances en temps réel
- **ec2instances.info** : Comparaison détaillée des types d'instances EC2
- **CNCF Landscape** : cloudnativelandscape.cncf.io — écosystème cloud native

### Benchmarks de Performance

- **CloudHarmony** : benchmarks de performance des VMs par provider
- **PerformanceLand** : benchmarks réseau et storage

---

## Glossaire Cloud Providers

| Terme | AWS | GCP | Azure |
|-------|-----|-----|-------|
| Instance virtuelle | EC2 | Compute Engine (GCE) | Azure VM |
| Stockage objet | S3 | Cloud Storage (GCS) | Azure Blob |
| Base de données managée | RDS | Cloud SQL | Azure Database |
| Kubernetes managé | EKS | GKE | AKS |
| Serverless functions | Lambda | Cloud Functions | Azure Functions |
| Load balancer | ALB / NLB | Cloud Load Balancing | Azure Load Balancer |
| Réseau privé | VPC | VPC | VNet |
| CDN | CloudFront | Cloud CDN | Azure CDN |
| IAM | AWS IAM | Cloud IAM | Azure AD |
| Audit logs | CloudTrail | Cloud Audit Logs | Azure Activity Log |
| Data warehouse | Redshift | BigQuery | Azure Synapse |
| ML Platform | SageMaker | Vertex AI | Azure ML |
| Container registry | ECR | Artifact Registry | ACR |
| Secrets | Secrets Manager | Secret Manager | Azure Key Vault |
| DNS | Route 53 | Cloud DNS | Azure DNS |
