---
name: devops
description: This skill should be used when the user asks about "CI/CD", "continuous integration", "continuous deployment", "Docker", "Kubernetes", "Infrastructure as Code", "Terraform", "Pulumi", "feature flags", "GitOps", "GitHub Actions", "deployment strategy", "blue-green", "canary", "release management", or needs guidance on DevOps practices, pipeline design, and release engineering.
version: 1.0.0
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

## Additional Resources

Consult these reference files for deep dives on each topic area:

- **[CI/CD Pipelines](./references/ci-cd-pipelines.md)** — Pipeline design patterns, GitHub Actions deep dive, GitLab CI, automated testing in CI, artifact management, pipeline optimization and caching, monorepo CI (Nx, Turborepo), supply chain security (SLSA, Sigstore, SBOM).

- **[Infrastructure as Code](./references/infrastructure-as-code.md)** — Terraform (HCL, modules, state management, workspaces), Pulumi (programmatic IaC), AWS CDK, Ansible, GitOps (ArgoCD, Flux), IaC testing (Terratest, Checkov), drift detection, state management best practices.

- **[Containerization](./references/containerization.md)** — Docker best practices (multi-stage builds, layer caching, security scanning), Docker Compose, Kubernetes (pods, services, deployments, ingress, HPA, ConfigMaps, Secrets), Helm charts, Kustomize, container security (Trivy, Snyk Container).

- **[Deployment Strategies](./references/deployment-strategies.md)** — Blue-green, canary, rolling updates, feature flags and progressive delivery, zero-downtime deployments, database migrations in deployment, rollback strategies, environment management, preview environments.
