---
name: cloud-infrastructure
description: This skill should be used when the user asks about "cloud infrastructure", "AWS", "GCP", "Google Cloud", "Azure", "cloud provider", "cloud architecture", "Terraform", "Pulumi", "Infrastructure as Code", "IaC", "serverless", "Lambda", "Cloud Functions", "Azure Functions", "Kubernetes managed", "EKS", "GKE", "AKS", "FinOps", "cloud cost optimization", "VPC", "cloud networking", "cloud security", "IAM", "cloud-native", "multi-cloud", "hybrid cloud", "cloud migration", "lift and shift", "cloud design patterns", "infrastructure cloud", "architecture cloud", "fournisseur cloud", "IaC avancé", "infrastructure serverless", "optimisation des coûts cloud", "réseau cloud", "sécurité cloud", "migration cloud", "patterns d'architecture cloud", "reserved instances", "spot instances", "auto-scaling", "cloud storage", "S3", "GCS", "blob storage", "cloud database", "RDS", "Cloud SQL", "Cosmos DB", "CDN", "load balancer", "WAF", "cloud firewall", or needs guidance on cloud infrastructure design, multi-cloud strategy, Infrastructure as Code, or serverless architectures.
version: 1.2.0
last_updated: 2026-02
---

# Cloud Infrastructure — AWS/GCP/Azure, IaC & Cloud-Native Architecture

## Overview

**FR** — Ce skill couvre la conception, le déploiement et la gestion d'infrastructures cloud modernes : choix du fournisseur cloud (AWS, GCP, Azure), Infrastructure as Code avec Terraform et Pulumi, architectures serverless et cloud-native, réseaux et sécurité cloud, et optimisation des coûts (FinOps). L'objectif est de construire des infrastructures fiables, sécurisées, scalables et économiquement efficientes — en partant des fondamentaux du cloud jusqu'aux patterns d'architecture avancés. Les recommandations sont alignées avec les meilleures pratiques 2024-2026, incluant le FinOps, la sécurité by design, et les architectures événementielles serverless.

**EN** — This skill covers the design, deployment, and management of modern cloud infrastructures: cloud provider selection (AWS, GCP, Azure), Infrastructure as Code with Terraform and Pulumi, serverless and cloud-native architectures, cloud networking and security, and cost optimization (FinOps). The goal is to build reliable, secure, scalable, and cost-efficient infrastructures — from cloud fundamentals to advanced architecture patterns.

---

## When This Skill Applies

Activate this skill when the user:

- Choisit un fournisseur cloud ou compare AWS, GCP et Azure
- Conçoit une architecture cloud (VPC, subnets, load balancing, haute disponibilité)
- Écrit ou revoit du code Terraform ou Pulumi (modules, state, workspaces, testing)
- Conçoit une architecture serverless (Lambda, Cloud Functions, event-driven)
- Migre une application vers le cloud (lift-and-shift, re-platforming, re-architecture)
- Optimise les coûts cloud (rightsizing, reserved instances, FinOps)
- Conçoit la sécurité cloud (IAM, least privilege, VPC design, WAF, encryption)
- Gère une infrastructure multi-cloud ou hybride
- Configure des services managés cloud (RDS, Cloud SQL, EKS, GKE, AKS)
- Troubleshoot des problèmes d'infrastructure cloud (latence, disponibilité, coûts)

---

## Core Principles

### 1. Infrastructure as Code, Always
Ne jamais créer ou modifier des ressources cloud manuellement via la console. Chaque ressource doit être définie dans du code versionné (Terraform, Pulumi), revu par des pairs, et déployé via un pipeline CI/CD. La console cloud est un outil de lecture et d'exploration, pas de modification. Les changements manuels créent du drift et des environnements non reproductibles. / Never create or modify cloud resources manually. Every resource must be defined in versioned code, peer-reviewed, and deployed via CI/CD.

### 2. Least Privilege by Default
Chaque ressource cloud, service et utilisateur doit avoir exactement les permissions nécessaires à son fonctionnement, ni plus. Commencer par zéro permissions et ajouter uniquement ce qui est nécessaire. Utiliser des rôles IAM dédiés par service, des policies scoped au minimum, et des service accounts distincts. Auditer régulièrement les permissions inutilisées avec IAM Access Analyzer (AWS), Policy Analyzer (GCP), ou Access Review (Azure). / Every resource, service, and user gets only the permissions needed. Start from zero, add only what is necessary.

### 3. Design for Failure
L'infrastructure cloud doit être conçue en assumant que des composants vont tomber. Déployer dans plusieurs zones de disponibilité (multi-AZ minimum, multi-région pour les services critiques). Utiliser des load balancers, des health checks, des auto-scaling groups, des circuit breakers. Tester régulièrement la résilience avec des exercises de chaos engineering. L'objectif est de rendre les pannes tolérables et automatiquement récupérables, pas de les prévenir toutes. / Design assuming components will fail. Deploy multi-AZ, use health checks, auto-scaling, and circuit breakers.

### 4. Immutable Infrastructure
Une fois déployée, l'infrastructure ne doit pas être modifiée en place. Toute mise à jour consiste à créer une nouvelle instance avec la configuration souhaitée et à remplacer l'ancienne. Ce principe s'applique aux instances EC2 (AMIs immuables), aux containers (images versionnées par SHA), et aux configurations (pas de SSH en production, tout via IaC). L'infrastructure immuable est reproductible, auditables, et élimine le configuration drift. / Update by replacing, never by patching in place. Immutable infrastructure eliminates drift.

### 5. FinOps — Cost is a Feature
Le coût cloud est une métrique de performance au même titre que la latence ou la disponibilité. Taguer toutes les ressources par équipe, environnement et projet pour allouer les coûts. Configurer des budgets avec alertes à 50%, 80% et 100%. Utiliser des reserved instances ou committed use pour les workloads prévisibles (économie de 40-70%). Arrêter les ressources non-production en dehors des heures de travail. Revoir les coûts mensuellement avec toutes les équipes. / Cloud cost is a performance metric. Tag everything, set budgets, use reservations for predictable workloads.

### 6. Security by Design, Not by Afterthought
Intégrer la sécurité dès la conception de l'architecture, pas en couche ajoutée après. Utiliser des VPC avec subnets privés pour les données et les services backend. Chiffrer les données au repos (KMS, Cloud KMS, Azure Key Vault) et en transit (TLS 1.2+ minimum). Ne jamais exposer des buckets S3 ou GCS publiquement sauf besoin explicite. Activer les logs d'audit (CloudTrail, Cloud Audit Logs, Azure Activity Log) et centraliser dans un SIEM. Faire des reviews de sécurité pour chaque nouveau composant cloud. / Integrate security from day one: private subnets for data, encryption everywhere, audit logs always on.

---

## Key Frameworks & Methods

| Framework / Method | Purpose | FR |
|---|---|---|
| **Terraform** | IaC declarative multi-cloud (HCL) | IaC déclarative multi-cloud |
| **Pulumi** | IaC avec vrais langages de programmation | IaC avec TypeScript, Python, Go |
| **AWS CDK / CDKTF** | IaC AWS-native ou Terraform en code | IaC AWS ou Terraform en langage de programmation |
| **Terratest** | Tests d'intégration pour Terraform | Tests automatisés pour le code IaC |
| **tfsec / Checkov** | Analyse de sécurité du code IaC | Scan de sécurité statique du code IaC |
| **AWS Well-Architected Framework** | 6 piliers d'architecture cloud AWS | Cadre d'architecture cloud AWS |
| **Google Cloud Architecture Framework** | Bonnes pratiques cloud GCP | Cadre d'architecture cloud GCP |
| **Cloud Adoption Framework (CAF)** | Migration et adoption cloud | Cadre de migration cloud |
| **FinOps Framework** | Gouvernance et optimisation des coûts cloud | Gestion des coûts cloud |
| **Zero Trust Network Architecture** | Sécurité réseau sans périmètre de confiance | Architecture sécurité sans frontière de confiance |

---

## Decision Guide

### Choisir son fournisseur cloud

| Critère | AWS | GCP | Azure |
|---|---|---|---|
| **Market share** | Leader (32%) | 3ème (11%) | 2ème (22%) |
| **Ecosystème** | Le plus large | Fort en data/ML | Fort en entreprise |
| **Kubernetes** | EKS (complexe) | GKE (le meilleur) | AKS (bon) |
| **Base de données** | RDS, Aurora, DynamoDB | Cloud SQL, Spanner, BigTable | Azure SQL, Cosmos DB |
| **Serverless** | Lambda (référence) | Cloud Functions, Cloud Run | Azure Functions |
| **Data / ML** | SageMaker, Redshift | BigQuery, Vertex AI | Azure ML, Synapse |
| **Réseau** | VPC, Transit Gateway | VPC, Cloud Interconnect | VNet, ExpressRoute |
| **Stack Microsoft** | Moyen | Faible | Excellent (AD, Office 365) |
| **Recommandé pour** | Stacks polyvalentes, startups | Data/ML, orgs Google | Entreprises Microsoft |

### Choisir entre Terraform et Pulumi

| Critère | Terraform | Pulumi |
|---|---|---|
| **Langage** | HCL (DSL déclaratif) | TypeScript, Python, Go, C#, Java |
| **Courbe d'apprentissage** | Modérée | Plus élevée (langage de programmation) |
| **Ecosystème de providers** | Le plus large (3000+ providers) | Compatible Terraform providers |
| **Logique conditionnelle** | Limitée (count, for_each) | Complète (boucles, conditions, fonctions) |
| **Tests** | Terratest (Go) | Tests unitaires natifs du langage |
| **State management** | Remote state (S3, GCS, Terraform Cloud) | Pulumi Cloud ou self-hosted |
| **Adapté pour** | Infrastructure complexe, équipes ops | Équipes dev, logique complexe, tests |

### Choisir la stratégie compute

```
Quel est le pattern de charge de travail ?
+-- Tâches courtes et événementielles (< 15 min, triggers HTTP/event)
|   -> Serverless Functions (Lambda, Cloud Functions, Azure Functions)
+-- Applications conteneurisées sans gestion d'infra
|   -> Serverless containers (Cloud Run, AWS App Runner, Azure Container Apps)
+-- Applications web avec trafic variable et managé
|   -> PaaS (App Engine, Elastic Beanstalk, Azure App Service)
+-- Microservices avec orchestration complexe
|   -> Kubernetes managé (GKE, EKS, AKS) + Helm
+-- VMs avec contrôle total sur l'OS
|   -> EC2, GCE, Azure VMs (auto-scaling groups)
+-- Charges très prévisibles et continues
|   -> Reserved Instances ou Committed Use Discounts (économie 40-70%)
```

### Architecture VPC / réseau

| Pattern | Usage | Configuration |
|---|---|---|
| **Single VPC** | Applications simples, petites équipes | 1 VPC, subnets public/private/data |
| **Multi-VPC Hub & Spoke** | Organisations avec plusieurs comptes/projets | VPC central (shared services) + VPCs spoke |
| **Multi-region active-active** | Applications à haute disponibilité globale | VPCs par région, routing global (Route 53, Cloud DNS) |
| **Hybrid (VPN/Direct Connect)** | Connexion on-premise + cloud | VPN IPSec ou Direct Connect/Cloud Interconnect |

---

## Common Patterns & Anti-Patterns

### Patterns (Do)
- **Module Terraform Réutilisable** : Encapsuler les composants récurrents (VPC, ECS service, RDS instance) en modules Terraform versionnés. Versionner les modules avec des tags Git. Utiliser un registry de modules (Terraform Registry ou registry privé). Chaque équipe consomme les modules standard plutôt que de recréer l'infrastructure from scratch.
- **Remote State avec Locking** : Stocker le state Terraform dans un backend remote (S3 + DynamoDB pour AWS, GCS pour GCP) avec locking pour éviter les modifications concurrentes. Ne jamais committer le fichier `terraform.tfstate` dans Git.
- **Workspaces pour Multi-Environnement** : Utiliser les workspaces Terraform pour gérer dev/staging/production avec le même code mais des configurations différentes. Combiner avec des fichiers `terraform.tfvars` par environnement.
- **Tagging Systématique** : Définir une convention de tags obligatoires pour toutes les ressources cloud : `environment`, `team`, `project`, `cost-center`, `managed-by`. Automatiser la validation des tags avec des policies (SCP, Organization Policy, Azure Policy).
- **Plan Before Apply in CI** : Dans le pipeline CI/CD, toujours exécuter `terraform plan` sur les PRs pour visualiser les changements. N'exécuter `terraform apply` qu'après approval humain sur les environnements critiques (staging, production).
- **Security Groups Minimal** : Créer des security groups dédiés par service avec uniquement les ports nécessaires. Interdire les règles `0.0.0.0/0` en ingress sauf pour les load balancers publics sur les ports 80/443.

### Anti-Patterns (Avoid)
- **ClickOps** : Créer ou modifier des ressources cloud manuellement via la console. Crée du drift entre l'état réel et l'IaC, rend l'infrastructure non reproductible et non auditables.
- **Monorepo IaC Unique** : Mettre toute l'infrastructure d'une organisation dans un seul repo Terraform sans modularisation. Un `terraform apply` global devient dangereux et lent. Décomposer en stacks indépendantes avec des backends de state séparés.
- **Credentials Hardcodées** : Inclure des AWS access keys, GCP service account keys ou tokens dans le code IaC ou les scripts. Utiliser des instance profiles, workload identity federation, ou OIDC pour l'authentification sans credentials.
- **Ressources Orphelines** : Créer des ressources cloud sans les gérer dans l'IaC (créées manuellement ou via des scripts). Ces ressources génèrent des coûts invisibles et des risques de sécurité. Importer toutes les ressources existantes dans Terraform.
- **Sur-Allocation par Défaut** : Choisir des types d'instances oversizées "pour être tranquille" sans mesure de l'utilisation réelle. Commencer par des instances modestes, monitorer l'utilisation CPU/mémoire, et rightsizer après 2-4 semaines de données.
- **Single AZ** : Déployer des services critiques dans une seule zone de disponibilité. Une panne AZ (rare mais réel) met hors service l'application entière. Déployer minimum 2 AZ pour la production, 3 AZ pour les services critiques.

---

## Implementation Workflow

Follow this workflow when designing or provisioning cloud infrastructure:

1. **Définir les Requirements** — Identifier les exigences de disponibilité (SLA), de performance (latence, throughput), de sécurité (compliance, données sensibles), et de coût (budget mensuel). Ces contraintes guident toutes les décisions d'architecture.

2. **Choisir le Fournisseur Cloud et la Région** — Sélectionner le cloud provider selon les critères (stack existante, compétences, services requis). Choisir la région principale selon la latence avec les utilisateurs et les exigences de souveraineté des données.

3. **Concevoir le Réseau** — Définir la structure VPC : CIDR block, subnets publics/privés/data, routage, NAT gateways, security groups. Documenter l'architecture réseau avec un diagramme. Valider la conception avec un security review.

4. **Structurer le Projet IaC** — Organiser le code Terraform en modules réutilisables et en stacks indépendantes (réseau, compute, database, monitoring). Configurer le remote state avec locking. Définir les conventions de nommage et de tagging.

5. **Provisionner les Fondations** — Déployer les ressources fondamentales : VPC, subnets, route tables, security groups, IAM roles, S3 buckets pour les logs et le state. Valider avec `terraform plan` avant chaque `apply`.

6. **Déployer les Services** — Provisionner les services applicatifs : instances compute, bases de données, load balancers, caches. Utiliser des services managés (RDS, ElastiCache, Cloud SQL) plutôt que de gérer les services soi-même.

7. **Configurer la Sécurité** — Activer les logs d'audit (CloudTrail, Cloud Audit Logs). Configurer WAF pour les endpoints publics. Activer le chiffrement au repos et en transit. Scanner le code IaC avec tfsec ou Checkov. Conduire un security review de l'architecture.

8. **Implémenter le Monitoring et les Alertes** — Configurer les métriques cloud natives (CloudWatch, Cloud Monitoring, Azure Monitor). Définir des alertes sur les métriques critiques (CPU, mémoire, erreurs, latence, coûts). Intégrer avec l'outil d'observabilité de l'équipe.

9. **Optimiser les Coûts (FinOps)** — Configurer les budgets avec alertes. Identifier les ressources sous-utilisées. Acheter des reserved instances pour les workloads stables. Programmer l'arrêt des environnements non-production en dehors des heures de bureau.

10. **Tester et Documenter** — Écrire des tests Terratest pour les modules critiques. Documenter l'architecture avec des diagrammes (C4, architecture diagrams). Créer un runbook pour les opérations courantes (scaling, rotation des credentials, DR).

---

## Modèle de maturité

### Niveau 1 — Manuel
- Ressources créées manuellement via la console, configurations non documentées
- Pas de gestion des coûts, facturation surprise mensuelle
- Sécurité basique, credentials partagés, pas d'audit logs
- **Indicateurs** : 0% IaC coverage, coûts non alloués par équipe, incidents de sécurité non détectés

### Niveau 2 — Scripts
- Premiers scripts de provisioning (CloudFormation, scripts bash), reproductibilité partielle
- Tagging partiel, quelques alertes de coût configurées
- IAM basique en place, quelques security groups définis
- **Indicateurs** : 20-50% IaC coverage, alertes de coût configurées

### Niveau 3 — IaC Systématique
- Terraform ou Pulumi pour toute l'infrastructure, remote state avec locking
- Budgets par équipe, rightsizing mensuel, reserved instances pour les workloads stables
- VPC design sécurisé, least privilege IAM, audit logs activés
- **Indicateurs** : > 80% IaC coverage, drift < 5%, coûts alloués par équipe

### Niveau 4 — Platform Engineering
- Modules IaC réutilisables, CI/CD pour l'infrastructure, plan/apply automatisé
- FinOps mature : coûts par service, spot instances, auto-scaling optimisé
- Security by design : policy-as-code (SCP, OPA), vulnerability scanning, zero trust
- **Indicateurs** : 100% IaC coverage, coût cloud / revenu en amélioration continue

### Niveau 5 — Cloud Native
- Self-service infrastructure via IDP (Backstage, Port), golden paths
- FinOps automatisé : rightsizing automatique, spot instance fallback, waste elimination
- Multi-cloud actif avec gestion unifiée, chaos engineering, DR automatisé
- **Indicateurs** : time-to-infrastructure < 30 min, coût cloud optimisé en continu

## Rythme opérationnel

| Cadence | Activité | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Quotidien** | Revue des alertes de coût et de sécurité | Cloud Engineer | Log des alertes et actions correctives |
| **Hebdomadaire** | Revue des ressources orphelines et du drift IaC | Cloud Engineer | Rapport de drift et cleanup |
| **Mensuel** | FinOps review : coûts par équipe et par service | Cloud Engineer + FinOps | Dashboard coûts et plan d'optimisation |
| **Mensuel** | Security review : IAM, security groups, vulnérabilités | Cloud Security Engineer | Rapport de sécurité et actions |
| **Trimestriel** | Rightsizing : analyse de l'utilisation et redimensionnement | Cloud Architect | Plan de rightsizing et économies estimées |
| **Trimestriel** | Revue des reserved instances (renouvellement, ajustements) | FinOps Engineer | Rapport RI et recommandations |
| **Annuel** | Audit d'architecture cloud et roadmap infrastructure | Cloud Architect | Rapport d'audit et roadmap annuelle |

## State of the Art (2025-2026)

L'infrastructure cloud évolue vers plus d'abstraction et d'automatisation :

- **Platform Engineering** : Les Internal Developer Platforms (Backstage, Port, Kratix) permettent le self-service infrastructure avec des golden paths, réduisant la charge cognitive des développeurs.
- **FinOps mature** : Le Framework FinOps s'impose comme standard de gouvernance des coûts cloud, avec des outils comme CloudCost, Infracost, et OpenCost pour la visibilité en temps réel.
- **IaC nouvelle génération** : Pulumi et les CDKs gagnent du terrain face à Terraform (licence BSL), avec des capacités de testing et de réutilisation supérieures.
- **Edge computing** : AWS Outposts, Google Distributed Cloud et Azure Arc permettent d'étendre le cloud vers l'edge et les datacenters on-premise.
- **Confidential computing** : AMD SEV, Intel TDX et les enclaves sécurisées (AWS Nitro Enclaves) permettent le traitement de données sensibles dans le cloud avec isolation cryptographique.
- **Sustainability** : Les fournisseurs cloud publient des métriques d'empreinte carbone par service, intégrées dans les outils FinOps pour optimiser la durabilité.

## Template actionnable

### Checklist de sécurité cloud

| Domaine | Contrôle | Status | Notes |
|---|---|---|---|
| **IAM** | Least privilege sur tous les rôles | ☐ | |
| **IAM** | MFA obligatoire pour les comptes humans | ☐ | |
| **IAM** | Pas de credentials AWS root utilisées | ☐ | |
| **Réseau** | Subnets privés pour data et services backend | ☐ | |
| **Réseau** | Pas de règle 0.0.0.0/0 en ingress (sauf LB 80/443) | ☐ | |
| **Chiffrement** | Chiffrement au repos activé (KMS) | ☐ | |
| **Chiffrement** | TLS 1.2+ minimum en transit | ☐ | |
| **Logs** | CloudTrail / Audit Logs activés sur tous les comptes | ☐ | |
| **Logs** | Logs centralisés dans un SIEM | ☐ | |
| **Stockage** | Aucun bucket S3/GCS public non intentionnel | ☐ | |
| **IaC** | Code IaC scanné avec tfsec ou Checkov | ☐ | |
| **Coûts** | Budgets avec alertes à 80% configurés | ☐ | |

## Prompts types

- "Comment concevoir un VPC AWS sécurisé pour mon application web ?"
- "Aide-moi à structurer un projet Terraform en modules réutilisables"
- "Quand utiliser serverless (Lambda) vs containers (ECS/GKE) ?"
- "Comment optimiser les coûts de notre infrastructure AWS ?"
- "Compare AWS vs GCP pour notre stack data"
- "Comment migrer notre infrastructure vers Pulumi depuis Terraform ?"

## Limites et Red Flags

Ce skill n'est PAS adapté pour :
- ❌ CI/CD pipelines, déploiement d'applications, GitOps → Utiliser plutôt : `code-development:devops`
- ❌ Monitoring, alerting, SLOs, incident management → Utiliser plutôt : `code-development:monitoring`
- ❌ Sécurité applicative (OAuth, OWASP, JWT, secrets applicatifs) → Utiliser plutôt : `code-development:auth-security`
- ❌ Architecture logicielle (microservices, DDD, API design) → Utiliser plutôt : `code-development:architecture`
- ❌ Gouvernance IT, stratégie cloud niveau direction → Utiliser plutôt : `entreprise:it-systemes`

Signaux d'alerte en cours d'utilisation :
- ⚠️ Des ressources cloud sont créées ou modifiées manuellement via la console sans mise à jour de l'IaC — création de drift, infrastructure non reproductible
- ⚠️ Les coûts cloud augmentent sans budget ni alertes configurés — risque de facture surprise significative
- ⚠️ Des credentials AWS/GCP hardcodées apparaissent dans le code ou les variables d'environnement — risque de fuite de credentials, remplacer par des rôles IAM et workload identity
- ⚠️ L'application est déployée dans une seule zone de disponibilité en production — résilience insuffisante, panne AZ = downtime total

## Skills connexes

| Skill | Lien |
|---|---|
| DevOps | `code-development:devops` — CI/CD, déploiement et GitOps |
| Architecture | `code-development:architecture` — Architecture logicielle et patterns distribués |
| Monitoring | `code-development:monitoring` — Observabilité et alerting en production |
| Auth Security | `code-development:auth-security` — Sécurité applicative et IAM |
| IT Systèmes | `entreprise:it-systemes` — Gouvernance IT et stratégie cloud |

## Glossaire

| Terme | Définition |
|-------|-----------|
| **IaC (Infrastructure as Code)** | Gestion de l'infrastructure via des fichiers de configuration déclaratifs versionnés plutôt que par des manipulations manuelles. Terraform, Pulumi, CloudFormation. |
| **VPC (Virtual Private Cloud)** | Réseau virtuel isolé dans le cloud, dans lequel sont déployées les ressources. Divisé en subnets publics (accessibles depuis internet) et privés (isolés). |
| **Subnet** | Subdivision d'un VPC avec un bloc CIDR propre. Les subnets publics ont un accès direct à internet via une Internet Gateway ; les privés utilisent un NAT Gateway. |
| **IAM (Identity and Access Management)** | Service de gestion des identités et des permissions cloud. Permet de définir qui peut faire quoi sur quelles ressources (users, roles, policies). |
| **Least Privilege** | Principe de sécurité donnant à chaque entité (utilisateur, service) uniquement les permissions strictement nécessaires à son fonctionnement. |
| **Terraform** | Outil IaC de HashiCorp utilisant le langage HCL pour provisionner et gérer l'infrastructure multi-cloud de manière déclarative avec gestion d'état. |
| **Pulumi** | Outil IaC permettant de définir l'infrastructure avec de vrais langages de programmation (TypeScript, Python, Go) avec les mêmes capacités que Terraform. |
| **Remote State** | Stockage du fichier d'état Terraform dans un backend partagé (S3, GCS) avec locking pour éviter les modifications concurrentes entre membres de l'équipe. |
| **Terraform Module** | Ensemble réutilisable de ressources Terraform encapsulées avec des inputs et outputs définis, permettant la réutilisation et la standardisation. |
| **Reserved Instances / Committed Use** | Engagement d'utilisation sur 1 ou 3 ans en échange d'une réduction tarifaire de 40 à 70% par rapport au prix on-demand. |
| **Spot Instances / Preemptible VMs** | Instances disponibles à prix réduit (60-90%) pouvant être interrompues par le cloud provider. Adapté aux workloads tolérantes aux interruptions. |
| **Auto Scaling Group** | Groupe d'instances EC2 (ou équivalent GCP/Azure) qui s'ajuste automatiquement selon des métriques (CPU, latence, custom) entre un min et un max définis. |
| **NAT Gateway** | Passerelle permettant aux ressources dans des subnets privés d'accéder à internet en sortie sans exposer d'adresse IP publique en entrée. |
| **Security Group** | Pare-feu virtuel au niveau instance contrôlant le trafic entrant et sortant. Stateful : une règle d'entrée autorise automatiquement la réponse en sortie. |
| **WAF (Web Application Firewall)** | Pare-feu applicatif filtrant le trafic HTTP/HTTPS pour protéger contre les attaques OWASP Top 10 (injection SQL, XSS, etc.). |
| **KMS (Key Management Service)** | Service managé de gestion de clés de chiffrement. Utilisé pour chiffrer les données au repos dans les bases de données, buckets S3, et disques. |
| **CloudTrail / Cloud Audit Logs** | Services d'audit cloud enregistrant toutes les appels API effectués dans un compte (qui a fait quoi, quand, depuis quelle IP). Essentiel pour la conformité et la forensique. |
| **FinOps** | Discipline combinant finance, technologie et métier pour optimiser les coûts cloud : visibilité, allocation, benchmarking et optimisation continue. |
| **Multi-AZ** | Déploiement d'une application ou base de données dans plusieurs zones de disponibilité (datacenters physiquement séparés) pour la haute disponibilité. |
| **EKS / GKE / AKS** | Services Kubernetes managés d'AWS, GCP et Azure. Gèrent le control plane Kubernetes, laissant l'équipe gérer uniquement les workloads (nodes et pods). |
| **Serverless** | Modèle d'exécution où le cloud provider gère automatiquement l'infrastructure (provisionnement, scaling, maintenance). Facturation à l'usage (ex: Lambda par invocation). |
| **CDN (Content Delivery Network)** | Réseau de serveurs distribués géographiquement servant le contenu statique depuis le point le plus proche de l'utilisateur (CloudFront, Cloud CDN, Azure CDN). |

## Additional Resources

Consult these reference files for deep dives on each topic area:

- **[AWS, GCP & Azure](./references/aws-gcp-azure.md)** — Comparaison détaillée des services cloud par catégorie (compute, storage, database, networking, ML), patterns d'usage, services clés, et guide de sélection.

- **[Terraform & Pulumi](./references/terraform-pulumi.md)** — Terraform avancé (modules, workspaces, state, testing avec Terratest, drift detection), Pulumi (programmatic IaC, testing natif, stacks), et IaC best practices.

- **[Serverless & Cloud-Native](./references/serverless-cloud-native.md)** — Lambda, Cloud Functions, Azure Functions, Cloud Run, architectures événementielles, cold start optimization, serverless patterns, containers managés.

- **[Cloud Architecture](./references/cloud-architecture.md)** — Patterns d'architecture cloud (multi-tier, microservices cloud-native, event-driven), VPC design, haute disponibilité, disaster recovery, FinOps avancé, sécurité cloud by design.

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant la conception et l'implémentation d'architectures cloud dans différents contextes.
