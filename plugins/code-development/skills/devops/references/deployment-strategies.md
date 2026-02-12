# Deployment Strategies — Progressive Delivery, Feature Flags & Release Management

## Introduction

**FR** — Ce guide de reference couvre les strategies de deploiement modernes : blue-green, canary, rolling updates, feature flags et progressive delivery, deploiements zero-downtime, migrations de base de donnees en deploiement, strategies de rollback, gestion des environnements et environnements de preview. L'objectif : deployer avec confiance, a haute frequence, avec la capacite de reverter instantanement en cas de probleme.

**EN** — This reference guide covers modern deployment strategies: blue-green, canary, rolling updates, feature flags and progressive delivery, zero-downtime deployments, database migrations in deployment, rollback strategies, environment management, and preview environments. The goal: deploy with confidence, at high frequency, with the ability to revert instantly when problems arise.

---

## 1. Rolling Updates

### How Rolling Updates Work

A rolling update gradually replaces instances of the old version with the new version. At any point during the rollout, both old and new versions are running simultaneously.

```yaml
# Kubernetes Deployment with rolling update strategy
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # Allow 2 extra pods during rollout
      maxUnavailable: 1  # At most 1 pod unavailable
  template:
    spec:
      containers:
        - name: api
          image: ghcr.io/org/api:v2.4.0
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            periodSeconds: 5
            failureThreshold: 3
```

**EN** — The readiness probe is critical: Kubernetes only routes traffic to pods that pass the readiness check. Set `maxSurge` to control how many extra pods can run during the update. Set `maxUnavailable` to control the minimum available capacity.

**FR** — La readiness probe est critique : Kubernetes ne route le trafic que vers les pods qui passent le readiness check. Configurer `maxSurge` et `maxUnavailable` pour controler la capacite pendant la mise a jour.

### Rolling Update Considerations

- **Backward compatibility**: Both old and new versions run simultaneously. The new version must handle requests that the old version initiated (e.g., shared session formats, compatible API contracts).
- **Database compatibility**: Database schema must be compatible with both versions during the rollout window. See the database migration section below.
- **Rollback**: Use `kubectl rollout undo deployment/api` for instant rollback to the previous revision. Kubernetes keeps a revision history.

---

## 2. Blue-Green Deployments

### Architecture

```
                    ┌─────────────┐
                    │   Router    │
                    │ (LB/Ingress)│
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │                         │
        ┌─────▼─────┐           ┌──────▼─────┐
        │   Blue     │           │   Green    │
        │ (current)  │           │  (new)     │
        │  v2.3.0    │           │  v2.4.0    │
        └───────────┘           └────────────┘
```

### Implementation with Kubernetes

```yaml
# Blue deployment (currently live)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-blue
  labels:
    app: api
    slot: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
      slot: blue
  template:
    metadata:
      labels:
        app: api
        slot: blue
    spec:
      containers:
        - name: api
          image: ghcr.io/org/api:v2.3.0

---
# Service pointing to blue
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
    slot: blue  # Switch to "green" for cutover
  ports:
    - port: 80
      targetPort: 3000
```

**EN** — To perform the cutover, deploy the green deployment with the new version, verify it passes health checks, then update the Service selector from `slot: blue` to `slot: green`. Rollback is instant: switch the selector back to `slot: blue`.

**FR** — Pour effectuer le basculement : deployer le deployment green avec la nouvelle version, verifier les health checks, puis mettre a jour le selecteur du Service de `slot: blue` a `slot: green`. Le rollback est instantane.

### Blue-Green Tradeoffs

| Advantage | Disadvantage |
|---|---|
| Instant cutover | Double infrastructure cost during deployment |
| Instant rollback | Database must be compatible with both versions |
| Full environment testing before switch | Complexity in managing two parallel deployments |
| Zero downtime | Long-running connections may be dropped during switch |

**EN** — Blue-green is best for critical services where instant rollback is non-negotiable. Mitigate the cost issue by tearing down the old (blue) environment after a stability window (e.g., 1 hour post-deploy).

---

## 3. Canary Deployments

### Progressive Traffic Shifting

```
Phase 1:  ████████████████████░  (5% canary, 95% stable)
Phase 2:  ███████████████░░░░░░  (25% canary, 75% stable)
Phase 3:  ██████████░░░░░░░░░░░  (50% canary, 50% stable)
Phase 4:  ░░░░░░░░░░░░░░░░░░░░░  (100% canary → new stable)
```

### Argo Rollouts — Canary with Analysis

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: api
spec:
  replicas: 10
  strategy:
    canary:
      canaryService: api-canary
      stableService: api-stable
      trafficRouting:
        nginx:
          stableIngress: api-ingress
      steps:
        - setWeight: 5
        - pause: { duration: 5m }
        - analysis:
            templates:
              - templateName: success-rate
            args:
              - name: service-name
                value: api-canary
        - setWeight: 25
        - pause: { duration: 10m }
        - analysis:
            templates:
              - templateName: success-rate
        - setWeight: 50
        - pause: { duration: 10m }
        - analysis:
            templates:
              - templateName: success-rate
        - setWeight: 100

---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: result[0] >= 0.99
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service-name}}",status=~"2.."}[5m]))
            /
            sum(rate(http_requests_total{service="{{args.service-name}}"}[5m]))
```

**FR** — Argo Rollouts automatise le deploiement canary avec des portes d'analyse. A chaque etape, une requete Prometheus verifie que le taux de succes reste superieur a 99%. Si l'analyse echoue 3 fois, le rollout est automatiquement annule (rollback).

**EN** — Each canary step includes an analysis gate that queries Prometheus. If the success rate drops below 99%, the rollout automatically aborts and rolls back to the stable version. This is progressive delivery: automated, observable, and self-healing.

### Flagger — Alternative to Argo Rollouts

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: api
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  service:
    port: 80
    targetPort: 3000
  analysis:
    interval: 1m
    threshold: 5     # Max failed checks before rollback
    maxWeight: 50    # Max canary traffic percentage
    stepWeight: 10   # Increase by 10% each interval
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500  # ms
        interval: 1m
    webhooks:
      - name: load-test
        url: http://flagger-loadtester.test/
        metadata:
          cmd: "hey -z 1m -q 10 -c 2 http://api-canary.production/"
```

**EN** — Flagger works with any service mesh or ingress controller (Istio, Linkerd, NGINX, Contour). It creates canary and primary deployments automatically from a standard Deployment resource.

---

## 4. Feature Flags & Progressive Delivery

### Feature Flags Architecture

```
┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
│  Application │─────▶│ Feature Flag     │◀─────│  Dashboard   │
│  (SDK)       │      │ Service          │      │  (UI)        │
│              │◀─────│ (LaunchDarkly/   │      │              │
│              │      │  Unleash)        │      │              │
└──────────────┘      └─────────────────┘      └──────────────┘
```

### Feature Flag Implementation Patterns

```typescript
// LaunchDarkly SDK example
import * as ld from '@launchdarkly/node-server-sdk';

const client = ld.init(process.env.LAUNCHDARKLY_SDK_KEY!);

// Boolean flag — simple toggle
async function handleRequest(req: Request) {
  const user = {
    key: req.userId,
    email: req.userEmail,
    custom: { plan: req.userPlan, region: req.userRegion },
  };

  const newCheckoutEnabled = await client.variation('new-checkout-flow', user, false);

  if (newCheckoutEnabled) {
    return renderNewCheckout(req);
  }
  return renderLegacyCheckout(req);
}

// Percentage rollout — progressive delivery
// Configured in LaunchDarkly dashboard:
// - 5% of users see new feature (day 1)
// - 25% of users (day 2)
// - 100% of users (day 5)
```

### Unleash — Self-Hosted Feature Flags

```typescript
import { initialize, isEnabled } from 'unleash-client';

const unleash = initialize({
  url: 'https://unleash.example.com/api',
  appName: 'api',
  customHeaders: { Authorization: process.env.UNLEASH_API_TOKEN },
});

// Gradual rollout strategy
const isNewFeatureEnabled = isEnabled('new-feature', {
  userId: req.userId,
  properties: { region: req.userRegion },
});
```

**FR** — Les feature flags permettent de decoupler le deploiement du code du release de fonctionnalites. Deployer du code cache derriere un flag a 0%, puis augmenter progressivement le pourcentage. En cas de probleme, desactiver le flag instantanement — pas besoin de rollback de deploiement.

### Feature Flag Best Practices

1. **Name flags descriptively**: `enable-new-checkout-v2`, not `flag-123` or `test`.
2. **Set expiration dates**: Every flag should have an owner and a planned removal date. Stale flags are tech debt.
3. **Limit flag scope**: A flag should control one feature. Avoid compound flags that control multiple behaviors.
4. **Use server-side evaluation**: Evaluate flags server-side for security-sensitive features. Client-side evaluation exposes flag configuration.
5. **Test all flag states**: Unit tests must cover both the enabled and disabled paths. Use flag overrides in tests.
6. **Remove flags after rollout**: Once a feature is fully rolled out, remove the flag from code and the flag service. Aim to remove within 2 weeks of 100% rollout.
7. **Use kill switches for critical paths**: Keep permanent flags for circuit-breaker patterns on external dependencies.

**EN** — Treat feature flags as first-class code. A codebase with 500 unmanaged flags is worse than one with no flags at all. Implement a flag lifecycle: create -> rollout -> verify -> remove.

---

## 5. Zero-Downtime Deployments

### Requirements for Zero Downtime

1. **Graceful shutdown**: Applications must handle SIGTERM, finish in-flight requests, and shut down cleanly within the termination grace period.
2. **Readiness probes**: New pods must not receive traffic until they are ready.
3. **Connection draining**: Load balancers must drain existing connections before removing old pods.
4. **Backward-compatible changes**: Both old and new versions must coexist during the transition window.

### Graceful Shutdown in Node.js

```typescript
const server = app.listen(3000);

process.on('SIGTERM', () => {
  console.log('SIGTERM received. Starting graceful shutdown...');

  // Stop accepting new connections
  server.close(() => {
    console.log('HTTP server closed. Cleaning up...');

    // Close database connections
    db.end().then(() => {
      console.log('Database connections closed. Exiting.');
      process.exit(0);
    });
  });

  // Force exit after timeout
  setTimeout(() => {
    console.error('Graceful shutdown timed out. Forcing exit.');
    process.exit(1);
  }, 25000); // Must be less than terminationGracePeriodSeconds (default 30s)
});
```

### Kubernetes Lifecycle Hooks

```yaml
spec:
  terminationGracePeriodSeconds: 60
  containers:
    - name: api
      lifecycle:
        preStop:
          exec:
            command: ["sh", "-c", "sleep 5"]  # Allow time for endpoint removal
```

**FR** — Le `preStop` hook avec un `sleep 5` est essentiel : il donne le temps au kube-proxy et aux ingress controllers de retirer le pod de la rotation AVANT que le pod ne commence a refuser les connexions. Sans ce delai, des requetes en vol peuvent etre perdues pendant le deploiement.

**EN** — The 5-second preStop sleep is critical. When a pod is terminated, Kubernetes sends SIGTERM and simultaneously begins removing the pod from endpoints. The endpoint update takes time to propagate. Without the sleep, the pod may stop accepting connections before all routers have been updated, causing brief errors.

---

## 6. Database Migrations in Deployment

### The Expand-Contract Pattern

Never make breaking schema changes in a single deployment. Use the expand-contract (also called parallel change) pattern:

**Phase 1 — Expand** (deploy v2.1): Add the new column/table alongside the old one. Both versions of the application work.
```sql
ALTER TABLE users ADD COLUMN email_verified boolean DEFAULT false;
```

**Phase 2 — Migrate** (deploy v2.2): Application writes to both old and new columns. Backfill existing data.
```sql
UPDATE users SET email_verified = (email_verification_date IS NOT NULL);
```

**Phase 3 — Contract** (deploy v2.3): Remove the old column after confirming all reads use the new column.
```sql
ALTER TABLE users DROP COLUMN email_verification_date;
```

**FR** — Le pattern expand-contract garantit la compatibilite arriere a chaque etape. Chaque migration est deployable independamment. Si une etape pose probleme, les precedentes restent compatibles.

### Migration Execution Strategies

| Strategy | Pros | Cons | Use When |
|---|---|---|---|
| **Init container** | Runs before app starts | Blocks deployment | Small, fast migrations |
| **Separate migration job** | Independent lifecycle | Timing coordination needed | Large data migrations |
| **Application startup** | Simple | Concurrent migration risk | Single-instance apps |
| **Background worker** | Non-blocking | Complex to monitor | Large data backfills |

### Kubernetes Migration Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: api-migration-v2.4.0
  annotations:
    argocd.argoproj.io/hook: PreSync  # Run before main deployment
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: ghcr.io/org/api:v2.4.0
          command: ["npx", "prisma", "migrate", "deploy"]
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: database-url
      restartPolicy: Never
  backoffLimit: 3
```

**EN** — Use ArgoCD PreSync hooks to run migrations before the application deployment. The deployment only proceeds if the migration job succeeds. This guarantees schema compatibility.

### Migration Safety Rules

1. **Never drop columns in the same deploy that stops reading them**. Wait at least one deploy cycle.
2. **Never rename columns**. Add new, copy data, remove old.
3. **Always add columns as nullable or with defaults**. Non-nullable columns without defaults will fail on existing rows.
4. **Test migrations against a production-size dataset**. A migration that works on 1,000 rows may lock a table with 10 million rows.
5. **Use online DDL tools** (pt-online-schema-change, gh-ost) for large MySQL tables. PostgreSQL handles most ALTER TABLE operations without full table locks.

---

## 7. Rollback Strategies

### Layered Rollback Approach

| Layer | Speed | Action |
|---|---|---|
| **Feature flag** | Instant (seconds) | Disable the flag — no deployment needed |
| **Traffic shift** | Fast (seconds) | Shift canary back to 0% or switch blue-green |
| **Kubernetes rollback** | Fast (minutes) | `kubectl rollout undo deployment/api` |
| **Revert commit + redeploy** | Slow (minutes-hours) | Git revert, push, wait for CI/CD pipeline |
| **Database rollback** | Slowest (depends) | Run reverse migration — often not feasible |

**EN** — Always plan rollback before deploying. The ideal rollback does not involve a deployment at all — feature flags and traffic shifting provide instant rollback without touching the pipeline.

**FR** — Toujours planifier le rollback avant de deployer. Le rollback ideal n'implique aucun deploiement — les feature flags et le traffic shifting fournissent un rollback instantane sans toucher au pipeline.

### Automated Rollback with Observability Gates

```yaml
# Argo Rollouts — automatic rollback on metrics degradation
spec:
  strategy:
    canary:
      steps:
        - setWeight: 10
        - pause: { duration: 5m }
        - analysis:
            templates:
              - templateName: error-rate-check
      # If any analysis fails, rollout automatically aborts
      # and reverts to the previous stable version
```

**EN** — Configure automated rollback triggers based on error rate, latency P99, and saturation metrics. The deployment should self-heal: if the new version degrades metrics beyond thresholds, it automatically rolls back without human intervention.

---

## 8. Environment Management

### Environment Hierarchy

```
┌──────────────────────────────────────────────────────────┐
│  Production                                              │
│  - Full scale, real traffic, real data                   │
│  - Deployment: canary with analysis gates                │
│  - Access: restricted, audit-logged                      │
├──────────────────────────────────────────────────────────┤
│  Staging                                                 │
│  - Production-like configuration, synthetic data         │
│  - Deployment: automatic on merge to main                │
│  - Purpose: final validation before production           │
├──────────────────────────────────────────────────────────┤
│  Preview (per-PR)                                        │
│  - Ephemeral, created on PR open, destroyed on merge     │
│  - Purpose: review and test changes in isolation         │
├──────────────────────────────────────────────────────────┤
│  Development (local)                                     │
│  - Docker Compose or local Kubernetes (kind, minikube)   │
│  - Purpose: fast iteration                               │
└──────────────────────────────────────────────────────────┘
```

### Environment Parity

**EN** — Minimize differences between environments. Use the same Docker images, the same Kubernetes manifests (with Kustomize overlays for environment-specific values), and the same database engine version. Differences between environments are the root cause of "works in staging, fails in production" incidents.

**FR** — Minimiser les differences entre les environnements. Utiliser les memes images Docker, les memes manifests Kubernetes (avec des overlays Kustomize), et la meme version du moteur de base de donnees. Les differences entre environnements sont la cause principale des incidents "ca marche en staging, ca plante en production".

### Configuration Management Across Environments

```yaml
# Use environment-specific ConfigMaps, NOT code-level if/else
# base/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
data:
  LOG_LEVEL: info
  FEATURE_FLAGS_URL: https://flags.example.com

# overlays/production/configmap-patch.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
data:
  LOG_LEVEL: warn
  CACHE_TTL: "3600"
```

**EN** — Externalize all configuration. The application binary should be identical across environments. Only configuration (environment variables, ConfigMaps, Secrets) should differ.

---

## 9. Preview Environments

### Ephemeral Environments per Pull Request

**EN** — Preview environments provide a fully functional copy of the application for every PR. Reviewers can interact with the feature before merging, QA can test in isolation, and stakeholders can provide feedback on actual running software.

### Kubernetes-Based Preview Environments

```yaml
# GitHub Actions — Deploy preview environment
name: Preview
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  deploy-preview:
    runs-on: ubuntu-latest
    environment:
      name: preview-pr-${{ github.event.pull_request.number }}
      url: https://pr-${{ github.event.pull_request.number }}.preview.example.com
    steps:
      - uses: actions/checkout@v4
      - run: |
          docker build -t ghcr.io/org/api:pr-${{ github.event.pull_request.number }} .
          docker push ghcr.io/org/api:pr-${{ github.event.pull_request.number }}

      - uses: azure/k8s-set-context@v4
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG }}

      - run: |
          NAMESPACE="preview-pr-${{ github.event.pull_request.number }}"
          kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

          # Deploy with Kustomize, overriding image and namespace
          cd k8s/overlays/preview
          kustomize edit set image ghcr.io/org/api=ghcr.io/org/api:pr-${{ github.event.pull_request.number }}
          kustomize edit set namespace $NAMESPACE
          kustomize build | kubectl apply -f -

      - uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '🚀 Preview deployed: https://pr-${{ github.event.pull_request.number }}.preview.example.com'
            })

  # Cleanup on PR close
  cleanup-preview:
    if: github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - run: kubectl delete namespace preview-pr-${{ github.event.pull_request.number }}
```

**FR** — Creer un namespace Kubernetes par PR. Deployer l'application avec la meme configuration que staging. Detruire le namespace a la fermeture de la PR. Poster l'URL de preview en commentaire sur la PR.

### Vercel / Netlify Preview Deployments

```json
// vercel.json
{
  "git": {
    "deploymentEnabled": {
      "main": true,
      "preview": true
    }
  }
}
```

**EN** — For frontend applications, Vercel and Netlify provide zero-configuration preview deployments. Every PR gets a unique URL automatically. This is the gold standard for frontend preview environments — no infrastructure management required.

### Preview Environment Best Practices

1. **Use seeded test data**: Never connect preview environments to production databases. Use a seed script or database snapshot.
2. **Set resource limits**: Preview environments should use minimal resources (1 replica, small resource limits) to control cloud costs.
3. **Auto-cleanup with TTL**: Delete preview environments after 48 hours of inactivity or on PR merge/close. Use a CronJob or GitHub Actions to enforce.
4. **Mock external services**: Use service stubs or sandbox endpoints for third-party APIs in preview environments.
5. **Share the URL in the PR**: Always post the preview URL as a PR comment for easy access.

---

## 10. Semantic Versioning & Release Management

### SemVer Rules

```
MAJOR.MINOR.PATCH
  │      │     └── Bug fixes, no API changes
  │      └──────── New features, backward compatible
  └─────────────── Breaking changes
```

### Automated Releases with Semantic Release

```yaml
# GitHub Actions — Automated release
name: Release
on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      packages: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

```json
// .releaserc.json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    "@semantic-release/github",
    ["@semantic-release/git", {
      "assets": ["CHANGELOG.md", "package.json"],
      "message": "chore(release): ${nextRelease.version} [skip ci]"
    }]
  ]
}
```

**FR** — Utiliser Conventional Commits (`feat:`, `fix:`, `BREAKING CHANGE:`) pour que semantic-release determine automatiquement le prochain numero de version, genere le changelog, et publie la release. Aucune intervention humaine necessaire.

**EN** — semantic-release reads commit messages following Conventional Commits, determines the next version number (major/minor/patch), generates release notes, creates a Git tag, publishes to npm/registry, and creates a GitHub release — all automatically. Combine with Commitlint to enforce commit message format.

### Release Checklist

1. Use Conventional Commits for all commit messages
2. Configure semantic-release or release-please for automated versioning
3. Generate CHANGELOG.md automatically
4. Tag container images with both the SemVer tag and the commit SHA
5. Create GitHub Releases with release notes
6. Sign release artifacts with cosign/Sigstore
7. Attach SBOM to the release
8. Notify stakeholders via Slack/Teams webhook

**FR** — Un processus de release entierement automatise reduit les erreurs humaines, accelere la livraison et fournit un audit trail complet. Chaque release est tracable depuis le commit jusqu'a l'artefact deploye.

**EN** — A fully automated release process reduces human error, accelerates delivery, and provides a complete audit trail. Every release is traceable from commit to deployed artifact. Never rely on a human remembering to bump a version number or write release notes manually.
