# Cloud Architecture — Modern Cloud-Native Patterns

## Overview

Ce document de référence couvre les stratégies et patterns d'architecture cloud modernes, incluant les approches multi-cloud, serverless, container orchestration, edge computing et FinOps. Appliquer ces patterns en alignement avec les Well-Architected Frameworks et les principes de cloud-native design. Concevoir pour l'élasticité, la résilience et l'optimisation des coûts dès le premier jour.

---

## Well-Architected Frameworks — Unified View

### Les Six Piliers (synthèse AWS, Azure, GCP)

Les trois principaux cloud providers ont convergé vers des frameworks similaires. Utiliser cette synthèse comme grille d'évaluation universelle :

#### 1. Operational Excellence
- Automatiser toutes les opérations (Infrastructure as Code, GitOps, CI/CD).
- Implémenter l'observabilité complète (métriques, logs, traces) avec OpenTelemetry.
- Documenter les runbooks et pratiquer le game day (simulation d'incidents).
- Adopter le "everything as code" : infrastructure, configuration, policies, monitoring.

#### 2. Security
- Appliquer le Zero Trust : ne jamais faire confiance, toujours vérifier. Chaque requête est authentifiée et autorisée.
- Chiffrer les données at rest (AES-256) et in transit (TLS 1.3, mTLS).
- Implémenter le least privilege avec des politiques IAM granulaires. Préférer les rôles temporaires (assume role, workload identity).
- Automatiser la détection des menaces (GuardDuty, Defender, Security Command Center).
- Rotation automatique des secrets (Vault, AWS Secrets Manager).

#### 3. Reliability
- Concevoir pour la défaillance : chaque composant peut tomber.
- Implémenter les patterns de résilience : circuit breaker, bulkhead, retry, timeout.
- Multi-AZ minimum, multi-region pour les workloads critiques.
- Tester la résilience avec le chaos engineering (Chaos Monkey, Litmus, Gremlin).
- Définir des RTO (Recovery Time Objective) et RPO (Recovery Point Objective) par service.

#### 4. Performance Efficiency
- Dimensionner correctement les ressources (right-sizing) : éviter le sur-provisionnement.
- Utiliser le caching à chaque niveau : CDN, application, base de données.
- Adopter les architectures serverless pour les workloads intermittents.
- Benchmark et profiler régulièrement. Mesurer la latence p50, p95, p99.
- Utiliser les global accelerators et le CDN pour réduire la latence réseau.

#### 5. Cost Optimization (FinOps)
- Implementer le tagging obligatoire : chaque ressource identifiée par service, équipe, environnement, cost center.
- Utiliser les reserved instances / savings plans pour les workloads stables (jusqu'à 72% d'économie).
- Activer l'auto-scaling agressif : scale to zero quand possible.
- Monitorer les coûts en temps réel avec des alertes de budget.
- Pratiquer le FinOps : collaboration entre engineering, finance et business pour optimiser le rapport valeur/coût.

#### 6. Sustainability
- Minimiser l'empreinte carbone : choisir les régions avec l'énergie la plus propre.
- Optimiser l'utilisation des ressources pour réduire le gaspillage.
- Utiliser les instances ARM (Graviton, Ampere) pour un meilleur rapport performance/watt.
- Mesurer et rapporter l'impact carbone (Carbon Footprint Dashboard).

---

## Container Orchestration

### Kubernetes — When and How

#### Quand utiliser Kubernetes
- Plus de 10-15 microservices en production.
- Besoin de scaling horizontal automatique fin.
- Équipe avec expertise DevOps/Platform Engineering.
- Workloads complexes nécessitant des stratégies de déploiement avancées.

#### Quand NE PAS utiliser Kubernetes
- Moins de 5 services : un PaaS (Railway, Render, Fly.io) ou des containers managés (ECS, Cloud Run) suffisent.
- Équipe sans expertise Kubernetes : la complexité opérationnelle peut submerger l'équipe.
- Workloads purement serverless : les plateformes serverless sont plus appropriées.

#### Managed Kubernetes Options (2024-2026)

| Service | Provider | Particularité |
|---|---|---|
| **EKS** | AWS | Intégration profonde AWS, EKS Anywhere pour hybrid |
| **GKE** | GCP | Autopilot mode (fully managed nodes), meilleur UX |
| **AKS** | Azure | Intégration Azure AD, KEDA natif pour scaling |
| **DOKS** | DigitalOcean | Simple, économique, bon pour les petites équipes |

#### Kubernetes Best Practices

**Resource Management** :
- Toujours définir les requests et limits pour CPU et mémoire.
- Utiliser le Vertical Pod Autoscaler (VPA) pour le right-sizing automatique.
- Utiliser le Horizontal Pod Autoscaler (HPA) avec des métriques custom (pas seulement CPU).
- Implémenter les Pod Disruption Budgets (PDB) pour garantir la disponibilité pendant les maintenances.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      containers:
      - name: order-service
        image: order-service:v1.2.3
        resources:
          requests:
            cpu: "250m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 15
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
        startupProbe:
          httpGet:
            path: /health/startup
            port: 8080
          failureThreshold: 30
          periodSeconds: 5
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
```

**Networking** :
- Utiliser les NetworkPolicies pour le micro-segmentation (deny all par défaut, allow list explicite).
- Implémenter un Ingress Controller (nginx, Traefik, Istio Gateway) pour le routage externe.
- Utiliser le Gateway API (successeur d'Ingress) pour le routage avancé.

**Security** :
- Activer le Pod Security Standards (Restricted profile).
- Ne jamais exécuter les containers en root. Utiliser des non-root users.
- Scanner les images avec Trivy, Snyk, ou Grype dans la CI.
- Utiliser les Sealed Secrets ou External Secrets Operator pour la gestion des secrets.
- Implémenter les OPA/Gatekeeper policies pour l'enforcement automatique.

### GitOps — Declarative Infrastructure

#### Principes GitOps
1. **Declarative** : toute l'infrastructure et la configuration décrites de manière déclarative.
2. **Versioned** : Git comme single source of truth. Chaque changement est un commit.
3. **Automated** : réconciliation automatique entre l'état désiré (Git) et l'état réel (cluster).
4. **Auditable** : historique complet des changements via l'historique Git.

#### Outils GitOps (2024-2026)
- **ArgoCD** : le standard de facto pour le GitOps Kubernetes. Interface web riche, multi-cluster, SSO.
- **Flux** : léger, composable, CNCF graduated. Bon pour les équipes préférant la CLI.
- **Crossplane** : GitOps étendu aux ressources cloud (bases de données, queues, etc.). Gère l'infrastructure cloud comme des ressources Kubernetes.

#### Structure de repository GitOps

```
gitops-repo/
├── apps/
│   ├── base/
│   │   ├── order-service/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   ├── hpa.yaml
│   │   │   └── kustomization.yaml
│   │   └── payment-service/
│   │       └── ...
│   ├── staging/
│   │   ├── kustomization.yaml    # Overlays staging
│   │   └── patches/
│   └── production/
│       ├── kustomization.yaml    # Overlays production
│       └── patches/
├── infrastructure/
│   ├── cert-manager/
│   ├── ingress-nginx/
│   ├── monitoring/
│   └── sealed-secrets/
└── clusters/
    ├── staging/
    │   └── kustomization.yaml
    └── production/
        └── kustomization.yaml
```

---

## Serverless Architecture

### Quand le serverless est approprié
- **Event-driven workloads** : traitement de webhooks, notifications, transformations de données.
- **Trafic imprévisible** : de 0 à des milliers de requêtes par seconde.
- **APIs légères** : endpoints REST/GraphQL sans état.
- **Background jobs** : cron jobs, batch processing, ETL.
- **Prototypage rapide** : time-to-market minimal.

### Quand éviter le serverless
- **Workloads longue durée** : traitements > 15 minutes (limites de timeout).
- **Applications stateful** : besoin de connexions persistantes (WebSocket), sessions serveur.
- **Latence ultra-faible requise** : le cold start (100ms-2s) est inacceptable.
- **Coûts prévisibles requis** : le modèle pay-per-invocation peut exploser avec un trafic élevé constant.

### Serverless Patterns

#### Event Processing Pipeline

```
[Source: S3/API/IoT] → [Event Bridge / SNS] → [Lambda / Cloud Function]
                                                       ↓
                                              [Processing Logic]
                                                       ↓
                                            [DynamoDB / RDS / S3]
                                                       ↓
                                              [Notification / Next Step]
```

#### Fan-out / Fan-in

```
[Trigger Event]
      ↓
[Dispatcher Lambda]
      ├── [Worker Lambda 1] ──┐
      ├── [Worker Lambda 2] ──┤
      ├── [Worker Lambda 3] ──┼── [Aggregator Lambda] → [Result]
      └── [Worker Lambda N] ──┘
```

Utiliser AWS Step Functions, Azure Durable Functions, ou GCP Workflows pour orchestrer les flux complexes avec gestion d'état, retry et compensation.

#### Serverless API

```
[Client] → [API Gateway] → [Lambda] → [DynamoDB]
                ↓
        [Authorization]
        [Rate Limiting]
        [Caching]
        [Request Validation]
```

### Cold Start Optimization
- **Provisioned concurrency** (AWS) / **minimum instances** (GCP) : maintenir des instances chaudes pour les endpoints critiques.
- **Réduire la taille du package** : tree-shaking, lazy imports, layer pour les dépendances communes.
- **Choisir un runtime rapide** : Rust, Go, ou .NET AOT pour les cold starts < 100ms. Node.js et Python sont acceptables. Java/JVM à éviter sans GraalVM native.
- **SnapStart** (AWS Lambda, Java) : snapshot de l'initialisation JVM pour réduire le cold start.
- **Initialisation paresseuse** : déplacer les connexions DB et SDK init hors du handler critique.

### Serverless Databases
- **DynamoDB** (AWS) : NoSQL serverless, pay-per-request, auto-scaling. Idéal pour les patterns d'accès prévisibles par clé.
- **Aurora Serverless v2** (AWS) : PostgreSQL/MySQL serverless avec auto-scaling fin. Bon compromis entre relationnel et serverless.
- **Neon** : PostgreSQL serverless avec branching. Excellente DX, scale to zero. Recommandé pour les startups (2024-2026).
- **PlanetScale** : MySQL serverless avec branching et schema migrations non-bloquantes.
- **Turso** : SQLite distribué sur edge (libSQL). Ultra-faible latence. Émergent en 2024-2025.

---

## Edge Computing

### Edge Computing Patterns

#### Edge Functions / Workers
Exécuter du code au plus proche des utilisateurs sur le réseau CDN mondial :
- **Cloudflare Workers** : V8 isolates, cold start < 5ms, 300+ PoP. Support Wasm.
- **Vercel Edge Functions** : intégrées avec Next.js, streaming SSR.
- **Deno Deploy** : runtime Deno natif, compatible Web Standards.
- **AWS CloudFront Functions / Lambda@Edge** : intégrés avec CloudFront CDN.

#### Cas d'usage des edge functions
- **A/B testing** : routage basé sur des headers/cookies sans latence additionnelle.
- **Personnalisation géographique** : contenu adapté par région.
- **Authentication** : validation des tokens JWT au edge.
- **Rate limiting** : contrôle du trafic au plus proche de la source.
- **Transformation de réponse** : modification des headers, réécriture d'URL.
- **Feature flags** : évaluation des flags au edge pour un rendering instantané.

#### Edge Data

Rapprocher les données des utilisateurs :
- **Turso / libSQL** : SQLite répliqué sur edge, lecture locale ultra-rapide.
- **Cloudflare D1** : SQLite serverless sur le réseau Cloudflare.
- **Cloudflare KV / Durable Objects** : stockage clé-valeur et objets stateful au edge.
- **Upstash Redis** : Redis serverless avec réplication globale.

#### Architecture Edge-First

```
[Client] → [Edge PoP (nearest)]
              ├── Edge Function (auth, routing, A/B)
              ├── Edge Cache (KV, Redis)
              ├── Edge DB (Turso replica)
              └── [Origin] (si cache miss)
                    ├── API Server
                    ├── Primary Database
                    └── Background Workers
```

Avantage : latence p50 < 50ms pour la majorité des requêtes, résilience aux pannes d'une région.

---

## Multi-Cloud & Hybrid Strategies

### Quand adopter le multi-cloud

| Motivation | Valide ? | Commentaire |
|---|---|---|
| Éviter le vendor lock-in | Partiellement | Le coût d'abstraction est souvent supérieur au risque réel |
| Conformité réglementaire | Oui | Certaines régulations exigent la diversification |
| Best-of-breed services | Oui | Utiliser GCP pour l'IA, AWS pour l'infra, Azure pour l'entreprise |
| Résilience inter-provider | Rarement | La complexité opérationnelle est immense |
| Négociation commerciale | Oui | Le leverage pricing est un bénéfice réel |

### Stratégies multi-cloud pragmatiques

#### Polycloud (recommandé)
Utiliser différents clouds pour différents workloads, sans chercher la portabilité :
- AWS pour l'infrastructure principale.
- GCP pour le machine learning (Vertex AI, BigQuery).
- Cloudflare pour le edge et le CDN.
- Pas d'abstraction multi-cloud — chaque workload utilise les services natifs du cloud choisi.

#### Cloud-Agnostic Layer (si nécessaire)
Si la portabilité est requise, abstraire uniquement les couches nécessaires :
- **Containers + Kubernetes** : portables entre clouds.
- **Terraform** : provisioning multi-cloud avec le même outil.
- **CNCF ecosystem** : Prometheus, Grafana, ArgoCD, Istio fonctionnent partout.
- **Éviter d'abstraire** les bases de données managées, le messaging, l'IAM — le coût d'abstraction est trop élevé.

### Hybrid Cloud

#### Cas d'usage légitimes
- **Données sensibles** : garder certaines données on-premise (régulation, souveraineté).
- **Latence** : traitement au plus proche des sources de données (usine, edge IoT).
- **Migration progressive** : migrer vers le cloud par phases.

#### Technologies hybrid (2024-2026)
- **AWS Outposts / EKS Anywhere** : services AWS on-premise.
- **Azure Arc** : gestion unifiée des ressources multi-cloud et on-premise.
- **GCP Anthos** : Kubernetes multi-cloud et hybrid.

---

## FinOps — Cloud Financial Management

### Principes FinOps

1. **Teams need to collaborate** : engineering, finance et business travaillent ensemble sur l'optimisation des coûts.
2. **Everyone takes ownership** : chaque équipe est responsable de ses coûts cloud.
3. **A centralized team drives FinOps** : une équipe FinOps fournit les outils, métriques et bonnes pratiques.
4. **Reports should be accessible** : les coûts doivent être visibles en temps réel par tous.
5. **Decisions are driven by business value** : optimiser le rapport valeur/coût, pas uniquement réduire les coûts.

### Cost Optimization Strategies

#### Right-Sizing
- Analyser l'utilisation réelle des ressources (CPU, mémoire) sur 14+ jours.
- Réduire les instances sur-provisionnées (typiquement 30-50% des instances sont sur-dimensionnées).
- Utiliser les recommandations automatiques (AWS Compute Optimizer, Azure Advisor, GCP Recommender).
- Implémenter le Vertical Pod Autoscaler en Kubernetes pour l'ajustement automatique.

#### Reserved Capacity
- **Reserved Instances / Savings Plans** : engagement 1-3 ans pour 30-72% d'économie.
- Analyser la baseline stable pour déterminer le volume à réserver.
- Utiliser les Savings Plans (AWS) plutôt que les RI pour plus de flexibilité.
- Réserver par famille d'instances, pas par type spécifique.

#### Spot / Preemptible Instances
- Utiliser pour les workloads tolérants aux interruptions : batch processing, CI/CD, training ML.
- Économie de 60-90% par rapport aux on-demand.
- Implémenter la gestion d'interruption : checkpointing, graceful shutdown, redistribution automatique.
- Diversifier les types d'instances pour réduire le risque d'interruption.

#### Architectural Cost Optimization
- **Scale to zero** : serverless, Knative, KEDA pour les workloads intermittents.
- **Data tiering** : déplacer les données froides vers le stockage moins cher (S3 Glacier, Archive).
- **Caching** : réduire les appels aux services coûteux (bases de données, APIs tierces, LLMs).
- **Compression** : réduire les coûts de transfert et de stockage.
- **Region selection** : les prix varient de 10-30% entre régions. Choisir les régions les moins chères quand la latence le permet.

### Cost Monitoring & Alerting

```
[Cloud Billing API]
       ↓
[Cost Allocation Engine]
  ├── Par service (tags)
  ├── Par équipe (tags)
  ├── Par environnement
  └── Par feature
       ↓
[Dashboard FinOps]
  ├── Coût actuel vs budget
  ├── Trend et forecast
  ├── Cost per transaction
  └── Unit economics
       ↓
[Alerting]
  ├── Budget threshold (80%, 100%, 120%)
  ├── Anomaly detection
  └── Unused resource detection
```

Outils FinOps : Infracost (coût de la PR avant merge), Kubecost (Kubernetes), CloudHealth, Spot.io, OpenCost (CNCF).

---

## Infrastructure as Code (IaC)

### Terraform Best Practices

#### Structure de projet

```
infrastructure/
├── modules/                    # Modules réutilisables
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── database/
│   └── compute/
├── environments/
│   ├── staging/
│   │   ├── main.tf            # Composition des modules
│   │   ├── terraform.tfvars   # Variables staging
│   │   └── backend.tf         # State backend
│   └── production/
│       ├── main.tf
│       ├── terraform.tfvars
│       └── backend.tf
└── global/                    # Ressources globales (IAM, DNS)
    ├── main.tf
    └── backend.tf
```

#### Règles essentielles
- **State remote et verrouillé** : utiliser un backend remote (S3, GCS, Azure Blob) avec state locking (DynamoDB, GCS).
- **State séparé par environnement** : ne jamais partager le state entre staging et production.
- **Modules versionnés** : publier les modules avec des tags semver. Référencer les modules par version, pas par branche.
- **Plan before apply** : toujours exécuter `terraform plan` et le reviewer avant `apply`. Intégrer dans la CI.
- **Drift detection** : détecter les modifications manuelles via des checks périodiques.

### Alternatives à Terraform (2024-2026)
- **OpenTofu** : fork open source de Terraform (après le changement de licence HashiCorp). Compatible à 100%.
- **Pulumi** : IaC en langages de programmation (TypeScript, Python, Go). Bon pour les équipes de développeurs.
- **CDK (AWS)** : constructs de haut niveau en TypeScript/Python pour les services AWS.
- **SST** : framework serverless moderne basé sur CDK. Excellente DX pour les applications serverless sur AWS.
- **Wing** : langage dédié au cloud qui compile vers Terraform/CDK. Émergent.

---

## Observability Stack

### The Three Pillars + Beyond

#### Métriques
- **Types** : counters, gauges, histograms, summaries.
- **RED method** (pour les services) : Rate, Errors, Duration.
- **USE method** (pour les ressources) : Utilization, Saturation, Errors.
- **Métriques métier** : taux de conversion, revenu par seconde, nombre de commandes actives.
- **Outils** : Prometheus + Grafana (standard), Datadog, New Relic.

#### Logs
- **Structured logging** obligatoire : JSON format avec correlation IDs.
- **Niveaux** : ERROR (action requise), WARN (dégradation), INFO (événements métier), DEBUG (diagnostic).
- **Ne pas logger** : données personnelles (PII), secrets, tokens.
- **Outils** : Loki + Grafana, ELK Stack, Datadog Logs.

```json
{
  "timestamp": "2025-01-15T10:30:00.123Z",
  "level": "INFO",
  "service": "order-service",
  "traceId": "abc-123",
  "spanId": "def-456",
  "message": "Order placed successfully",
  "orderId": "ORD-789",
  "customerId": "CUST-012",
  "totalAmount": 149.99,
  "itemCount": 3,
  "durationMs": 234
}
```

#### Traces
- **Distributed tracing** avec OpenTelemetry (standard ouvert, vendor-agnostic).
- **Auto-instrumentation** : instrumenter automatiquement les frameworks HTTP, clients DB, message brokers.
- **Context propagation** : propager le trace context (W3C Trace Context) à travers tous les services.
- **Sampling** : échantillonner intelligemment (tail-based sampling) pour réduire les coûts tout en capturant les requêtes intéressantes (erreurs, haute latence).
- **Outils** : Jaeger, Tempo + Grafana, Honeycomb, Datadog APM.

#### Profiling Continu
Quatrième pilier émergent. Profiler les applications en production en continu :
- **CPU profiling** : identifier les hotspots de code.
- **Memory profiling** : détecter les fuites et les allocations excessives.
- **Outils** : Pyroscope, Grafana Phlare, Datadog Continuous Profiler.

### SLO / SLI / SLA

- **SLI (Service Level Indicator)** : métrique mesurée (latence p99, taux d'erreur, disponibilité).
- **SLO (Service Level Objective)** : cible interne pour le SLI (latence p99 < 200ms, disponibilité 99.95%).
- **SLA (Service Level Agreement)** : engagement contractuel envers les clients (généralement moins ambitieux que le SLO).
- **Error Budget** : le budget d'erreur = 1 - SLO. Si le SLO est 99.9%, le budget est 0.1% (43.8 minutes/mois). Consommer le budget pour livrer des features, le préserver quand il est épuisé.

Utiliser les SLOs pour piloter les décisions de fiabilité : si le budget est dépassé, arrêter les déploiements de features et investir dans la fiabilité.

---

## Modern Cloud Patterns 2024-2026

### Platform Engineering & Internal Developer Platforms

Construire une plateforme interne qui abstrait la complexité cloud pour les développeurs :

```
[Developer] → [IDP Portal (Backstage)]
                    ↓
              [Self-Service APIs]
              ├── Provision Database
              ├── Create Service
              ├── Setup CI/CD
              ├── Configure Monitoring
              └── Manage Secrets
                    ↓
              [Platform Orchestration (Crossplane, Terraform)]
                    ↓
              [Cloud Infrastructure (AWS/GCP/Azure)]
```

**Principes** :
- Fournir des "golden paths" : chemins pré-configurés et optimisés pour les cas d'usage courants.
- Offrir du self-service : les développeurs provisionnent sans tickets, mais avec des guardrails.
- Abstraire, ne pas cacher : les développeurs peuvent voir et comprendre l'infrastructure sous-jacente.
- Mesurer l'adoption et la satisfaction développeur (Developer Experience metrics).

### AI Infrastructure Patterns

Architecture pour les applications intégrant l'IA :

```
[Client] → [API Gateway]
              ├── [Application Services]
              │     ├── Business Logic
              │     └── AI Orchestration
              ├── [AI Gateway]
              │     ├── LLM Routing (OpenAI, Anthropic, self-hosted)
              │     ├── Prompt Management
              │     ├── Response Caching (semantic)
              │     ├── Rate Limiting / Cost Control
              │     └── Observability (token usage, latency, quality)
              ├── [Vector Database]
              │     ├── Pinecone / Weaviate / pgvector
              │     └── Embedding Pipeline
              └── [Evaluation Pipeline]
                    ├── Quality Metrics
                    ├── Safety Checks
                    └── A/B Testing
```

**Considérations** :
- Implémenter un AI Gateway (Portkey, LiteLLM, custom) pour centraliser la gestion des LLMs.
- Cacher les réponses par similarité sémantique pour réduire les coûts (GPTCache, custom).
- Monitorer les tokens consommés, la latence et la qualité des réponses.
- Implémenter des fallback chains : si le modèle principal échoue, basculer vers un modèle alternatif.
- Séparer les pipelines d'indexation (offline) des pipelines de query (online) dans les architectures RAG.

### Sustainable Cloud Architecture

- Choisir les régions avec le plus faible impact carbone (AWS : Irlande, Oregon ; GCP : Finlande, Iowa).
- Utiliser les instances ARM (Graviton sur AWS, Ampere sur GCP/Azure) : 40% plus efficientes énergétiquement.
- Optimiser le code pour réduire le temps de calcul (profiling, algorithmes efficaces).
- Scale to zero pour les workloads non essentiels en dehors des heures de bureau.
- Utiliser le CDN et le caching pour réduire les round-trips vers l'origin.
- Mesurer l'empreinte carbone avec les outils natifs (AWS Customer Carbon Footprint, GCP Carbon Footprint).
