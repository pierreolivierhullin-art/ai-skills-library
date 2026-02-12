# CI/CD Pipelines — Design, Optimization & Supply Chain Security

## Introduction

**FR** — Ce guide de reference couvre la conception de pipelines CI/CD modernes, de l'architecture fondamentale aux pratiques avancees telles que l'optimisation du cache, la CI monorepo et la securite de la supply chain logicielle. Chaque pipeline doit etre traite comme un produit : fiable, rapide, maintenable et securise. Ce document fournit des patrons concrets et des exemples directement applicables.

**EN** — This reference guide covers modern CI/CD pipeline design, from foundational architecture to advanced practices such as cache optimization, monorepo CI, and software supply chain security. Treat every pipeline as a product: reliable, fast, maintainable, and secure. This document provides concrete patterns and directly applicable examples.

---

## 1. Pipeline Architecture Fundamentals

### The Standard Pipeline Model

Design every pipeline with these ordered stages. Each stage must be independently cacheable and fail-fast:

```
Trigger -> Checkout -> Install -> Lint -> Unit Test -> Build -> Integration Test -> Security Scan -> Artifact Publish -> Deploy Staging -> Smoke Test -> Deploy Production
```

**FR** — Concevoir chaque pipeline avec ces etapes ordonnees. Chaque etape doit etre independamment cacheable et echouer rapidement (fail-fast).

**EN** — Order stages by speed and cost: fast, cheap checks first (lint, unit tests), expensive checks later (integration tests, security scans). This minimizes wasted compute on obviously broken commits.

### Guiding Principles

- **Fail fast**: Place the fastest checks first. A lint error caught in 10 seconds saves a 15-minute integration test run.
- **Parallelize aggressively**: Run independent jobs concurrently. Unit tests, lint, and type checking have no dependencies on each other.
- **Make pipelines deterministic**: Pin dependency versions, use lock files, pin action versions by SHA (not tags).
- **Keep pipelines under 10 minutes**: If a pipeline exceeds 10 minutes for a standard PR, treat it as a performance bug. DORA research shows elite teams have lead times under 1 hour, which requires fast CI.

---

## 2. GitHub Actions Deep Dive

### Workflow Structure Best Practices

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Cancel in-progress runs for the same PR/branch
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read
  # Principle of least privilege — declare only needed permissions

jobs:
  lint-and-typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm test --shard=${{ matrix.shard }}/4

  build:
    needs: [lint-and-typecheck, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm build
      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
          retention-days: 7
```

**FR** — Points cles : utiliser `concurrency` pour annuler les runs obsoletes, `permissions` pour le principe du moindre privilege, `matrix` pour le sharding des tests, et `actions/upload-artifact` pour la promotion d'artefacts.

### Reusable Workflows

Centralize shared CI logic in a dedicated repository and call it from consumer repos:

```yaml
# In .github/workflows/ci.yml of your app repo
jobs:
  ci:
    uses: your-org/shared-workflows/.github/workflows/node-ci.yml@v2.1.0
    with:
      node-version: 22
      package-manager: pnpm
    secrets: inherit
```

**EN** — Version reusable workflows with Git tags (v2.1.0). Never reference `@main` in production workflows — a breaking change in the shared workflow would cascade to all consumers.

**FR** — Versionner les workflows reutilisables avec des tags Git (v2.1.0). Ne jamais referencer `@main` dans les workflows de production.

### OIDC Authentication for Cloud Providers

Eliminate long-lived secrets by using GitHub's OIDC token:

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789:role/github-actions-deploy
      aws-region: eu-west-1
```

**EN** — Configure the cloud provider to trust GitHub's OIDC issuer. Scope the IAM role to the specific repository and branch. Never store AWS_ACCESS_KEY_ID in GitHub secrets.

### GitHub Actions Advanced Patterns

- **Path filters**: Trigger workflows only when relevant files change. Use `paths` and `paths-ignore` to avoid running backend tests when only docs change.
- **Environment protection rules**: Require manual approval for production deployments. Use GitHub Environments with required reviewers and wait timers.
- **Composite actions**: Extract repeated step sequences into composite actions within your repo or a shared actions repo.
- **Self-hosted runners**: Use for workloads requiring GPU, specific OS, or private network access. Deploy with actions-runner-controller (ARC) on Kubernetes for auto-scaling.

---

## 3. GitLab CI

### Pipeline Configuration

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - test
  - build
  - security
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  key:
    files:
      - requirements.txt
  paths:
    - .cache/pip
    - venv/

lint:
  stage: validate
  script:
    - ruff check .
    - mypy src/

test:
  stage: test
  parallel: 4
  script:
    - pytest --splits 4 --group $CI_NODE_INDEX

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main

container_scan:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy_staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
```

**FR** — GitLab CI offre des fonctionnalites integrees puissantes : registre de conteneurs, environnements avec URLs de review, et scanning de securite natif. Utiliser `parallel` pour le sharding des tests et `cache:key:files` pour un cache base sur les fichiers de lock.

**EN** — GitLab CI excels at integrated DevSecOps. Use its built-in container registry, SAST/DAST templates, and environment tracking. Leverage `rules:` over `only/except` for modern pipeline control.

---

## 4. Automated Testing in CI

### Test Pyramid in CI

Structure tests by execution speed and blast radius:

| Layer | Duration Target | CI Stage | Parallelism |
|---|---|---|---|
| Static analysis (lint, type check) | < 30s | validate | Low (single job) |
| Unit tests | < 2 min | test | High (sharded) |
| Integration tests | < 5 min | test | Medium (sharded) |
| E2E tests | < 10 min | test (post-build) | High (sharded by spec) |
| Performance tests | Variable | Nightly / on-demand | Dedicated |

### Test Sharding and Parallelism

**EN** — Shard test suites to keep CI under 10 minutes. Use test timing data to balance shards evenly.

```yaml
# GitHub Actions — Playwright sharding
test-e2e:
  strategy:
    matrix:
      shard: [1/4, 2/4, 3/4, 4/4]
  steps:
    - run: npx playwright test --shard=${{ matrix.shard }}
```

### Flaky Test Management

- Track flakiness rates per test. Quarantine tests exceeding a 2% flake rate.
- Use retry logic (`retries: 2` in Playwright, `--reruns` in pytest) but treat retries as a diagnostic signal, not a solution.
- Never let flaky tests block the main branch. Move them to a quarantine suite and fix within 48 hours.

**FR** — Suivre les taux de flakiness par test. Mettre en quarantaine les tests depassant 2% de flakiness. Ne jamais laisser des tests instables bloquer la branche principale.

---

## 5. Artifact Management

### Container Image Strategy

- Tag images with the commit SHA: `myapp:a1b2c3d`. Never use `latest` as a deployment target.
- Store images in a private registry (ECR, GCR, GHCR, Harbor).
- Set retention policies: keep the last 50 tags, delete untagged manifests after 7 days.
- Scan every image before push and on a nightly schedule for newly discovered CVEs.

### Build Artifact Promotion

Implement the "build once, promote everywhere" pattern:

```
Build artifact (commit SHA tag)
  -> Deploy to staging (automatic)
  -> Run smoke tests
  -> Promote to production (manual approval or automated gate)
```

**EN** — Never rebuild for production. The artifact deployed to staging must be byte-identical to what reaches production. Change only configuration (environment variables, secrets) between environments.

**FR** — Ne jamais reconstruire pour la production. L'artefact deploye en staging doit etre identique octet par octet a celui qui atteint la production. Changer uniquement la configuration entre les environnements.

---

## 6. Pipeline Optimization & Caching

### Caching Strategies

| Strategy | Tool | Example |
|---|---|---|
| Dependency cache | actions/cache, GitLab cache | Cache `node_modules`, `~/.m2`, `.cache/pip` by lockfile hash |
| Build cache | Docker BuildKit, Turborepo | Layer caching, remote build cache |
| Test result cache | Nx, Turborepo | Skip unchanged tests in monorepos |
| Artifact cache | actions/upload-artifact | Promote built artifacts between jobs |

### Docker Build Optimization in CI

```yaml
- uses: docker/setup-buildx-action@v3
- uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: ghcr.io/org/app:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**EN** — Use BuildKit's GitHub Actions cache backend (`type=gha`) to share Docker layer cache across CI runs. This typically cuts Docker build times by 60-80%.

### Reducing CI Time — Checklist

1. Enable dependency caching by lockfile hash
2. Run independent jobs in parallel
3. Shard large test suites (aim for < 3 min per shard)
4. Use path filters to skip irrelevant jobs
5. Cache Docker layers with BuildKit
6. Use `concurrency` to cancel stale runs
7. Consider self-hosted runners for compute-intensive workloads
8. Use remote build caches (Turborepo, Nx Cloud, Gradle Build Cache)

**FR** — Objectif : chaque pipeline PR doit completer en moins de 10 minutes. Chaque minute au-dela de 10 est une taxe sur la productivite des developpeurs.

---

## 7. Monorepo CI

### The Challenge

In a monorepo, running all tests and builds for every commit is wasteful. Only execute pipelines for packages affected by the change.

### Affected-Only Execution with Nx

```yaml
# GitHub Actions with Nx
steps:
  - uses: actions/checkout@v4
    with:
      fetch-depth: 0  # Required for Nx affected detection
  - uses: nrwl/nx-set-shas@v4
  - run: npx nx affected -t lint test build --parallel=3
```

**EN** — Nx computes the dependency graph and determines which projects are affected by the current changeset. Only those projects run lint, test, and build. This reduces CI time from O(n) to O(affected).

### Turborepo in CI

```yaml
steps:
  - run: npx turbo run lint test build --filter=...[origin/main]
    env:
      TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
      TURBO_TEAM: my-team
```

**FR** — Turborepo utilise un cache distant pour partager les resultats de build entre les developpeurs et la CI. Combiner avec `--filter` pour n'executer que les packages affectes.

### Monorepo CI Architecture Patterns

- **Per-package pipelines**: Each package has its own CI workflow, triggered by path filters. Simple but limited.
- **Affected-only with shared cache**: Use Nx or Turborepo to compute affected packages. Best for most teams.
- **Merge queue**: Use GitHub merge queue or GitLab merge trains to batch and test multiple PRs together, reducing redundant CI runs.

---

## 8. Supply Chain Security

### SLSA Framework (Supply-chain Levels for Software Artifacts)

| Level | Requirement | Practical Implementation |
|---|---|---|
| SLSA L1 | Build process is documented | Pipeline-as-code in version control |
| SLSA L2 | Signed provenance, hosted build | GitHub Actions with OIDC + attestation |
| SLSA L3 | Hardened build platform, non-falsifiable provenance | Isolated build environments, verified builders |
| SLSA L4 | Two-person review, hermetic builds | Full reproducibility, auditable supply chain |

### Implementing SLSA L2+ with GitHub Actions

```yaml
jobs:
  build:
    permissions:
      id-token: write
      contents: read
      attestations: write
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: actions/attest-build-provenance@v1
        with:
          subject-path: dist/
```

**EN** — GitHub's built-in attestation support generates SLSA L2 provenance automatically. Verify attestations with `gh attestation verify`.

### Sigstore and Cosign

Sign container images without managing private keys:

```bash
# Sign an image with keyless signing (Sigstore/Fulcio)
cosign sign ghcr.io/org/app:v1.2.3

# Verify the signature
cosign verify ghcr.io/org/app:v1.2.3 \
  --certificate-identity=https://github.com/org/repo/.github/workflows/release.yml@refs/heads/main \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com
```

**FR** — Sigstore permet la signature sans cle (keyless) en utilisant des certificats ephemeres lies a l'identite OIDC du workflow CI. Aucune cle privee a gerer.

### SBOM Generation

Generate Software Bill of Materials for every release:

```yaml
steps:
  - uses: anchore/sbom-action@v0
    with:
      image: ghcr.io/org/app:${{ github.sha }}
      format: spdx-json
      output-file: sbom.spdx.json
  - uses: actions/upload-artifact@v4
    with:
      name: sbom
      path: sbom.spdx.json
```

**EN** — Attach SBOMs to releases. Use `syft` (by Anchore) or `trivy sbom` to generate SBOMs. Combine with `grype` for vulnerability scanning against the SBOM.

**FR** — Attacher les SBOMs aux releases. Utiliser `syft` ou `trivy sbom` pour generer les SBOMs. Combiner avec `grype` pour l'analyse de vulnerabilites.

### Dependency Management Security

- Enable Dependabot or Renovate for automated dependency updates. Group minor/patch updates to reduce PR noise.
- Pin GitHub Actions by commit SHA, not by tag: `uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11` (the SHA for v4.1.1).
- Use `npm audit`, `pip audit`, or `cargo audit` in CI. Fail the pipeline on critical vulnerabilities.
- Implement a dependency review step for PRs that checks for license compliance and known vulnerabilities.

---

## 9. AI-Augmented CI/CD (2025-2026 Emerging Practices)

### AI in Pipeline Design

- **Intelligent test selection**: Use ML models to predict which tests are likely to fail based on the changeset. Tools: Launchable, Codecov's ATS.
- **Auto-fix in CI**: Run AI-powered linters that suggest fixes (e.g., AI-assisted code review bots in PRs).
- **Pipeline performance prediction**: Predict CI duration based on changeset size and historical data. Alert when predicted time exceeds threshold.
- **Anomaly detection**: Detect unusual build times, test failures, or resource consumption patterns in CI.

**FR** — L'IA dans la CI/CD est une tendance emergente en 2025-2026. Utiliser la selection intelligente de tests pour reduire les temps de CI, et la detection d'anomalies pour identifier les problemes de pipeline proactivement.

**EN** — Adopt AI-augmented CI incrementally. Start with intelligent test selection (highest ROI), then add anomaly detection. Avoid over-automating — keep humans in the loop for deployment decisions to production.

---

## 10. Pipeline Anti-Patterns to Eliminate

| Anti-Pattern | Impact | Fix |
|---|---|---|
| No caching | Slow pipelines, wasted compute | Cache dependencies, Docker layers, build outputs |
| `latest` tag for deployments | Non-reproducible deployments | Use commit SHA or SemVer tags |
| Secrets in environment variables without rotation | Security risk | Use OIDC, Vault, or cloud secrets managers |
| Running all tests in monorepo | O(n) CI time | Use Nx/Turborepo affected-only detection |
| Manual deployment steps | Error-prone, slow | Automate with GitOps or pipeline deployment |
| No concurrency control | Wasted resources | Use `concurrency.cancel-in-progress` |
| Unrestricted `permissions` | Excessive token scope | Declare minimal permissions per job |
| Actions pinned by tag only | Vulnerable to tag mutation | Pin actions by full commit SHA |

**FR** — Eliminer ces anti-patrons systematiquement. Chacun represente un risque de securite, de fiabilite ou de performance.

**EN** — Treat each anti-pattern as a tech debt item. Prioritize by risk (security issues first) and impact (slowest pipeline stages first).
