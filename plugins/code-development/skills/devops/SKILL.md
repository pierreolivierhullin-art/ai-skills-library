---
name: devops
description: This skill should be used when the user asks about "CI/CD", "continuous integration", "continuous deployment", "Docker", "Kubernetes", "Infrastructure as Code", "Terraform", "Pulumi", "feature flags", "GitOps", "GitHub Actions", "deployment strategy", "blue-green", "canary", "release management", "intégration continue", "déploiement continu", "infrastructure as code", "IaC", "stratégie de déploiement", "gestion des releases", "containerization", "conteneurisation", "Docker Compose", "Helm", "ArgoCD", "Flux", "Jenkins", "CircleCI", "GitLab CI", "Vercel", "Netlify", "AWS", "GCP", "Azure", "serverless", "rolling update", "rollback", "secrets management", "environment management", "staging", "production", "immutable infrastructure", "12-factor app", or needs guidance on DevOps practices, pipeline design, and release engineering.
version: 1.2.0
last_updated: 2026-02
---

# DevOps — CI/CD, Infrastructure as Code, Containers & Release Management

## Overview

**FR** — Cette skill couvre l'ensemble des pratiques DevOps modernes : conception de pipelines CI/CD, Infrastructure as Code, conteneurisation, orchestration, stratégies de déploiement et gestion des releases. Adopter une approche DevOps mature, c'est construire un système de livraison logicielle rapide, fiable et sécurisé — du commit au monitoring en production. L'objectif est de fournir des recommandations actionnables et alignées avec les meilleures pratiques 2024-2026, incluant le platform engineering, les environnements éphémères, la sécurité de la supply chain logicielle et l'intégration de l'IA dans les pipelines.

**EN** — This skill covers the full spectrum of modern DevOps practices: CI/CD pipeline design, Infrastructure as Code, containerization, orchestration, deployment strategies, and release management. Adopting a mature DevOps approach means building a fast, reliable, and secure software delivery system — from commit to production monitoring. The goal is to provide actionable recommendations aligned with 2024-2026 best practices, including platform engineering, ephemeral environments, software supply chain security, and AI integration in pipelines.

---

## When This Skill Applies

Activate this skill when the user:

- Designs or optimizes a CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins, CircleCI, Dagger)
- Writes or reviews Infrastructure as Code (Terraform, Pulumi, AWS CDK, Ansible)
- Builds, secures, or optimizes Docker images and Kubernetes deployments
- Chooses a deployment strategy (blue-green, canary, rolling, progressive delivery)
- Implements GitOps workflows (ArgoCD, Flux)
- Sets up feature flags or progressive delivery (LaunchDarkly, Unleash, Flagsmith)
- Manages environments (dev, staging, preview, production) or monorepo CI
- Addresses supply chain security (SLSA, Sigstore, SBOM generation)
- Builds an Internal Developer Platform (Backstage, Port, Kratix)
- Needs guidance on semantic versioning, changelog automation, or release engineering

---

## Core Principles

### 1. Automate Everything, Trust Nothing Manually
Treat every manual step as a defect. Automate builds, tests, security scans, deployments, and rollbacks. Use policy-as-code to enforce guardrails. / Traiter chaque etape manuelle comme un defaut. Automatiser builds, tests, scans de securite, deploiements et rollbacks. Utiliser le policy-as-code pour imposer des garde-fous.

### 2. Shift Left Security and Quality
Integrate SAST, DAST, dependency scanning, container scanning, and IaC validation at the earliest pipeline stages. Generate SBOMs and enforce SLSA provenance. / Integrer SAST, DAST, analyse de dependances, scan de conteneurs et validation IaC des les premieres etapes du pipeline. Generer des SBOMs et appliquer la provenance SLSA.

### 3. Infrastructure Is Code, Code Is Reviewed
Apply the same rigor to infrastructure code as to application code: version control, code review, testing, and automated deployment. Never make ad-hoc changes to infrastructure. / Appliquer la meme rigueur au code d'infrastructure qu'au code applicatif : versioning, code review, tests et deploiement automatise. Ne jamais faire de changements ad-hoc a l'infrastructure.

### 4. Deploy Small, Deploy Often
Optimize for small, frequent, reversible deployments. Use feature flags to decouple deploy from release. Aim for DORA elite metrics: deployment frequency multiple times per day, lead time under one hour, change failure rate under 5%, MTTR under one hour. / Optimiser pour des deploiements petits, frequents et reversibles. Utiliser les feature flags pour decoupler le deploy du release. Viser les metriques DORA elite.

### 5. Embrace Platform Engineering
Build golden paths and self-service capabilities for developers. Reduce cognitive load through Internal Developer Platforms. Provide standardized templates, not gatekeeping. / Construire des golden paths et des capacites self-service pour les developpeurs. Reduire la charge cognitive via des plateformes developpeurs internes. Fournir des templates standardises, pas du gatekeeping.

### 6. Observe and Feedback Continuously
Close the feedback loop from production back to development. Integrate deployment events with observability tools. Use deployment markers in APM, correlate deploys with error rates. / Fermer la boucle de feedback de la production vers le developpement. Integrer les evenements de deploiement avec les outils d'observabilite.

---

## Key Frameworks & Methods

| Framework / Method | Purpose | FR |
|---|---|---|
| **DORA Metrics** | Measure delivery performance (DF, LT, CFR, MTTR) | Mesurer la performance de livraison |
| **SLSA Framework** | Supply chain security levels (L1-L4) | Niveaux de securite de la supply chain |
| **GitOps** | Git as single source of truth for infrastructure | Git comme source unique de verite pour l'infra |
| **Progressive Delivery** | Gradual rollout with observability gates | Deploiement progressif avec portes d'observabilite |
| **Platform Engineering** | Self-service developer platforms (IDP) | Plateformes developpeurs self-service |
| **Twelve-Factor App** | Cloud-native application methodology | Methodologie d'applications cloud-native |
| **SemVer** | Semantic Versioning for release management | Versionnage semantique pour la gestion des releases |
| **Immutable Infrastructure** | Replace, never patch running infrastructure | Remplacer, jamais patcher l'infrastructure en cours |

---

## Decision Guide

### Choosing a CI/CD Platform
- **GitHub Actions** — Best for GitHub-native projects, excellent marketplace, matrix strategies, OIDC for cloud auth. Prefer for most teams.
- **GitLab CI** — Best when using GitLab; built-in registry, security scanning, and environment management. Strong for regulated industries.
- **Dagger** — Best for portable, testable pipelines written in real programming languages. Use when pipeline logic is complex or multi-platform.
- **Jenkins** — Legacy choice. Migrate away unless deeply embedded. Use Jenkins pipelines with JCasC if stuck.

### Choosing an IaC Tool
- **Terraform** — Industry standard, vast provider ecosystem, mature state management. Use for multi-cloud or established teams.
- **Pulumi** — Use real programming languages (TypeScript, Python, Go). Best for teams that prefer code over HCL configuration.
- **AWS CDK / CDKTF** — Best for AWS-heavy stacks or when combining Terraform providers with programming language constructs.
- **Ansible** — Best for configuration management and ad-hoc tasks. Complement, do not replace, declarative IaC.

### Choosing a Deployment Strategy
- **Rolling Update** — Default for most workloads. Gradual pod replacement in Kubernetes. Simple but limited rollback speed.
- **Blue-Green** — Instant cutover, easy rollback. Higher cost (double infrastructure). Best for critical services.
- **Canary** — Progressive traffic shifting (1% -> 5% -> 25% -> 100%). Best with observability gates. Use with Flagger, Argo Rollouts.
- **Feature Flags** — Decouple deployment from release entirely. Best for trunk-based development. Use LaunchDarkly, Unleash, or Flagsmith.

---

## Common Patterns & Anti-Patterns

### Patterns (Do)
- **Trunk-Based Development + Feature Flags**: Keep branches short-lived (< 1 day), deploy from main, toggle features via flags
- **Immutable Artifacts**: Build once, promote the same artifact through environments. Tag images with commit SHA, not `latest`
- **Ephemeral Preview Environments**: Spin up a full environment per PR. Tear down on merge. Use Vercel, Netlify, or Kubernetes namespaces
- **Pipeline-as-Code with Reusable Workflows**: Centralize CI logic in shared workflow repositories. Version them with tags
- **OIDC for Cloud Authentication**: Never store long-lived cloud credentials in CI. Use GitHub OIDC -> AWS/GCP/Azure identity federation
- **Signed Artifacts and SLSA Provenance**: Sign container images with Sigstore/cosign. Generate and attest SLSA provenance at L2+

### Anti-Patterns (Avoid)
- **Snowflake Environments**: Manually configured servers that drift from desired state. Always use IaC
- **Long-Running Feature Branches**: Branches alive for weeks cause painful merges and integration bugs. Keep branches under 24 hours
- **Secrets in Code or CI Variables Without Rotation**: Use a secrets manager (Vault, AWS Secrets Manager) with automatic rotation
- **Monolithic Pipelines Without Caching**: Pipelines that rebuild everything on every commit. Use dependency caching, affected-only builds in monorepos
- **Deploy on Friday Without Feature Flags**: If you cannot toggle off a feature instantly, do not deploy before a period of low staffing

---

## Implementation Workflow

Follow this workflow when designing or improving a DevOps setup:

1. **Assess Current State** — Map the current delivery pipeline end-to-end. Measure DORA metrics (deployment frequency, lead time, change failure rate, MTTR). Identify bottlenecks.

2. **Design the Pipeline** — Define stages: lint -> test (unit, integration) -> build -> security scan (SAST, SCA, container scan) -> artifact publish -> deploy staging -> smoke test -> deploy production. Add approval gates only where compliance requires them.

3. **Implement Infrastructure as Code** — Choose Terraform or Pulumi. Structure code in modules. Set up remote state with locking. Implement CI for infrastructure (plan on PR, apply on merge to main).

4. **Containerize Applications** — Write multi-stage Dockerfiles. Minimize image size (distroless or Alpine base). Scan images with Trivy. Push to a private registry with immutable tags.

5. **Set Up GitOps** — Deploy ArgoCD or Flux. Define the desired state in a Git repository. Let the GitOps operator reconcile cluster state automatically. Use ApplicationSets for multi-cluster.

6. **Implement Deployment Strategies** — Start with rolling updates. Graduate to canary with Argo Rollouts or Flagger when observability is mature. Add feature flags for business-critical features.

7. **Harden the Supply Chain** — Enable SLSA L2+ provenance. Sign artifacts with cosign. Generate SBOMs with Syft. Enforce admission policies with Kyverno or OPA Gatekeeper.

8. **Build the Platform Layer** — Adopt Backstage or Port as an IDP. Create software templates for new services. Expose golden paths that embed all the above practices by default.

9. **Observe and Iterate** — Track DORA metrics continuously. Run blameless post-incident reviews. Feed learnings back into pipeline and platform improvements.

---



## Modèle de maturité

### Niveau 1 — Ad-hoc
- Déploiements manuels via SSH ou copie de fichiers, sans procédure standardisée
- Pas de CI : tests lancés localement, scripts individuels non versionnés
- Rollbacks paniqués en production, pas de stratégie de retour arrière
- **Indicateurs** : deployment frequency < 1/mois, MTTR > 1 semaine

### Niveau 2 — Reproductible
- CI basique en place (lint + tests unitaires + build automatisé)
- Infrastructure partiellement versionnée, environnements documentés
- Déploiements suivant un runbook documenté, reproductibles mais manuels
- **Indicateurs** : deployment frequency 1-2/mois, lead time for changes 1-2 semaines

### Niveau 3 — Standardisé
- CI/CD complet avec déploiements automatisés en staging et production
- IaC systématique (Terraform/Pulumi), environnements éphémères disponibles
- Métriques DORA suivies et revues régulièrement par l'équipe
- **Indicateurs** : deployment frequency 1-2/semaine, change failure rate < 15%

### Niveau 4 — Optimisé
- Déploiements canary/blue-green avec rollback automatique sur anomalie
- GitOps avec réconciliation automatique (ArgoCD/Flux), Internal Developer Platform
- DORA au niveau élite, feature flags pour découplage deploy/release
- **Indicateurs** : deployment frequency quotidienne, lead time < 1 jour, change failure rate < 5%

### Niveau 5 — Autonome
- Optimisation IA des pipelines (parallélisation, cache, sélection de tests)
- Auto-remédiation sur incidents courants, chaos engineering continu en production
- Developer experience mesurée (DX surveys, cognitive load, time-to-productivity)
- **Indicateurs** : deployment frequency on-demand (multiple/jour), MTTR < 1 heure

## Rythme opérationnel

| Cadence | Activité | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Hebdomadaire** | Revue des déploiements (succès, rollbacks, incidents) | Tech Lead | Rapport hebdo déploiements |
| **Hebdomadaire** | Rétro incidents et post-mortems | SRE / DevOps Engineer | Action items priorisés |
| **Mensuel** | Revue des métriques DORA (DF, LT, CFR, MTTR) | Engineering Manager | Dashboard DORA commenté |
| **Mensuel** | Optimisation des pipelines CI/CD (temps, coûts, fiabilité) | DevOps Engineer | Backlog d'améliorations pipeline |
| **Trimestriel** | Audit d'infrastructure (sécurité, coûts, scalabilité) | SRE / Cloud Architect | Rapport d'audit + plan de remédiation |
| **Trimestriel** | Test de disaster recovery (failover, restore, RTO/RPO) | SRE | Compte-rendu DR + checklist validée |
| **Annuel** | Revue tech radar et outillage DevOps | Engineering Manager | Tech radar mis à jour + roadmap outillage |

## State of the Art (2025-2026)

Le DevOps évolue vers le platform engineering et l'IA :

- **Platform engineering** : Les équipes plateforme construisent des Internal Developer Platforms (IDP) avec Backstage, Humanitec ou Port pour standardiser le self-service.
- **GitOps mature** : ArgoCD et Flux deviennent les standards de déploiement Kubernetes, avec des pratiques de progressive delivery intégrées.
- **AI-assisted DevOps** : L'IA optimise les pipelines (détection de tests flaky, root cause analysis automatisée, auto-remediation).
- **Shift-left security (DevSecOps)** : La sécurité s'intègre dès le pipeline CI avec des scans automatisés (SAST, DAST, SCA, SBOM).
- **Ephemeral environments** : Les environnements de preview par PR (Vercel, Railway, Namespace) deviennent le standard pour tester en isolation.

## Template actionnable

### Checklist de déploiement en production

| Phase | Action | Vérifié |
|---|---|---|
| **Pré-deploy** | Tests CI passent (unit, integration, E2E) | ☐ |
| **Pré-deploy** | Code review approuvé | ☐ |
| **Pré-deploy** | Changelog / release notes rédigées | ☐ |
| **Pré-deploy** | Variables d'environnement vérifiées | ☐ |
| **Pré-deploy** | Migrations DB testées sur staging | ☐ |
| **Deploy** | Déploiement progressif (canary / blue-green) | ☐ |
| **Deploy** | Vérification health checks | ☐ |
| **Post-deploy** | Smoke tests en production | ☐ |
| **Post-deploy** | Monitoring et alertes vérifiés | ☐ |
| **Rollback** | Procédure de rollback prête | ☐ |

## Prompts types

- "Comment mettre en place un pipeline CI/CD avec GitHub Actions ?"
- "Aide-moi à containeriser mon application avec Docker"
- "Propose une stratégie de déploiement blue-green pour notre API"
- "Comment gérer les feature flags en production ?"
- "Terraform vs Pulumi : lequel choisir pour notre infra ?"
- "Aide-moi à configurer un environnement de staging automatisé"

## Limites et Red Flags

Ce skill n'est PAS adapté pour :
- ❌ Décisions d'architecture applicative (monolithe vs microservices, DDD, CQRS) → Utiliser plutôt : `code-development:architecture`
- ❌ Écriture de tests unitaires, TDD, stratégie de test ou refactoring de code → Utiliser plutôt : `code-development:code-excellence` ou `code-development:quality-reliability`
- ❌ Monitoring, alerting, SLOs ou gestion d'incidents en production → Utiliser plutôt : `code-development:monitoring`
- ❌ Sécurité applicative (OAuth, OWASP, gestion des secrets applicatifs) → Utiliser plutôt : `code-development:auth-security`
- ❌ Gouvernance IT d'entreprise, stratégie cloud au niveau direction → Utiliser plutôt : `entreprise:it-systemes`

Signaux d'alerte en cours d'utilisation :
- ⚠️ Le pipeline CI prend plus de 30 minutes → découper en stages parallèles, activer le caching des dépendances et limiter les tests e2e au smoke testing
- ⚠️ Les déploiements en production sont manuels ou nécessitent un accès SSH → automatiser via CI/CD avec des approval gates uniquement où la compliance l'exige
- ⚠️ Les images Docker sont taguées `latest` en production → taguer avec le commit SHA pour garantir la traçabilité et la reproductibilité
- ⚠️ L'infrastructure est modifiée manuellement sans passer par l'IaC → tout changement doit être versionné dans Terraform/Pulumi et appliqué via pipeline

## Skills connexes

| Skill | Lien |
|---|---|
| Architecture | `code-development:architecture` — Infrastructure et architecture cloud |
| Monitoring | `code-development:monitoring` — Observabilité et alerting en production |
| Quality Reliability | `code-development:quality-reliability` — CI/CD et tests automatisés |
| Backend & DB | `code-development:backend-db` — Déploiement de bases de données et migrations |
| IT Systèmes | `entreprise:it-systemes` — Gouvernance infrastructure et cloud strategy |

## Glossaire

| Terme | Définition |
|-------|-----------|
| **CI/CD** | Intégration Continue / Déploiement Continu — pratiques automatisant la compilation, les tests et le déploiement du code à chaque changement pour livrer plus vite et plus fiablement. |
| **GitOps** | Pratique utilisant Git comme source unique de vérité pour l'infrastructure et les déploiements, avec réconciliation automatique de l'état réel vers l'état déclaré. |
| **Infrastructure as Code (IaC)** | Gestion de l'infrastructure via des fichiers de configuration déclaratifs versionnés, plutôt que par des manipulations manuelles. |
| **Terraform** | Outil IaC de HashiCorp utilisant le langage HCL pour provisionner et gérer l'infrastructure multi-cloud de manière déclarative avec gestion d'état. |
| **Pulumi** | Outil IaC permettant de définir l'infrastructure avec de vrais langages de programmation (TypeScript, Python, Go) plutôt qu'un DSL. |
| **Blue-Green Deployment** | Stratégie de déploiement maintenant deux environnements identiques (blue/green), basculant le trafic instantanément vers le nouveau pour un rollback rapide. |
| **Canary Release** | Stratégie déployant progressivement une nouvelle version à un sous-ensemble croissant d'utilisateurs (1% -> 5% -> 25% -> 100%) avec des portes d'observabilité. |
| **Feature Flag** | Mécanisme permettant d'activer ou désactiver une fonctionnalité en production sans redéploiement, découplant le déploiement du release. |
| **ArgoCD** | Outil GitOps pour Kubernetes réconciliant automatiquement l'état du cluster avec les manifestes déclarés dans un dépôt Git. |
| **Helm** | Gestionnaire de packages pour Kubernetes utilisant des charts (templates paramétrables) pour déployer et versionner des applications. |
| **Container Registry** | Service de stockage et de distribution d'images de conteneurs (Docker Hub, GitHub Container Registry, ECR, GCR). |
| **Namespace (K8s)** | Partitionnement logique d'un cluster Kubernetes isolant les ressources (pods, services, secrets) par environnement ou par équipe. |
| **Rolling Update** | Stratégie de déploiement par défaut dans Kubernetes, remplaçant progressivement les anciens pods par les nouveaux sans interruption de service. |
| **Immutable Infrastructure** | Principe selon lequel l'infrastructure déployée n'est jamais modifiée en place : toute mise à jour consiste à remplacer les instances par de nouvelles. |
| **Drift Detection** | Détection des écarts entre l'état réel de l'infrastructure et l'état déclaré dans le code IaC, signalant les modifications manuelles non autorisées. |
| **Pipeline as Code** | Définition du pipeline CI/CD dans des fichiers versionnés dans le dépôt (ex. `.github/workflows/`, `.gitlab-ci.yml`) plutôt que via une interface graphique. |
| **Artifact** | Produit de build (image Docker, binaire, archive) généré par le pipeline CI et promu à travers les environnements sans recompilation. |
| **DORA Metrics** | Quatre métriques clés mesurant la performance DevOps : fréquence de déploiement, lead time, taux d'échec des changements, temps de restauration (MTTR). |
| **SemVer** | Versionnage sémantique (MAJOR.MINOR.PATCH) communiquant la nature des changements : breaking change, nouvelle fonctionnalité, ou correction de bug. |

## Additional Resources

Consult these reference files for deep dives on each topic area:

- **[CI/CD Pipelines](./references/ci-cd-pipelines.md)** — Pipeline design patterns, GitHub Actions deep dive, GitLab CI, automated testing in CI, artifact management, pipeline optimization and caching, monorepo CI (Nx, Turborepo), supply chain security (SLSA, Sigstore, SBOM).

- **[Infrastructure as Code](./references/infrastructure-as-code.md)** — Terraform (HCL, modules, state management, workspaces), Pulumi (programmatic IaC), AWS CDK, Ansible, GitOps (ArgoCD, Flux), IaC testing (Terratest, Checkov), drift detection, state management best practices.

- **[Containerization](./references/containerization.md)** — Docker best practices (multi-stage builds, layer caching, security scanning), Docker Compose, Kubernetes (pods, services, deployments, ingress, HPA, ConfigMaps, Secrets), Helm charts, Kustomize, container security (Trivy, Snyk Container).

- **[Deployment Strategies](./references/deployment-strategies.md)** — Blue-green, canary, rolling updates, feature flags and progressive delivery, zero-downtime deployments, database migrations in deployment, rollback strategies, environment management, preview environments.

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.