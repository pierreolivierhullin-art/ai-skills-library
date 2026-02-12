# Containerization — Docker, Kubernetes & Container Security

## Introduction

**FR** — Ce guide de reference couvre la conteneurisation moderne : Docker (bonnes pratiques Dockerfile, multi-stage builds, optimisation du cache de layers, scanning de securite), Docker Compose, Kubernetes (pods, services, deployments, ingress, HPA, ConfigMaps, Secrets), Helm charts, Kustomize et securite des conteneurs. Maitriser la conteneurisation est essentiel pour des deploiements reproductibles, scalables et securises.

**EN** — This reference guide covers modern containerization: Docker (Dockerfile best practices, multi-stage builds, layer caching, security scanning), Docker Compose, Kubernetes (pods, services, deployments, ingress, HPA, ConfigMaps, Secrets), Helm charts, Kustomize, and container security. Mastering containerization is essential for reproducible, scalable, and secure deployments.

---

## 1. Docker — Dockerfile Best Practices

### The Optimal Dockerfile Structure

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Dependencies
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile --prod

# Stage 2: Build
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

# Stage 3: Production
FROM gcr.io/distroless/nodejs22-debian12 AS production
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist

# Run as non-root
USER nonroot:nonroot

EXPOSE 3000
CMD ["dist/server.js"]
```

**FR** — Structure optimale : separer les dependances, le build et la production en stages distincts. Utiliser distroless ou Alpine pour l'image finale. Toujours executer en tant qu'utilisateur non-root.

### Key Dockerfile Rules

1. **Use multi-stage builds**: Separate build dependencies from runtime. The final image should contain only what is needed to run the application.
2. **Order layers by change frequency**: Place rarely changing layers first (base image, system packages), frequently changing layers last (application code).
3. **Use `.dockerignore`**: Exclude `node_modules`, `.git`, `*.md`, test files, and local configuration from the build context.
4. **Pin base image versions**: Use `node:22.11-alpine` instead of `node:latest` or `node:22`. Pin to a specific patch version for reproducibility.
5. **Minimize layer count**: Combine related RUN commands with `&&`. Each RUN creates a layer.
6. **Use COPY, not ADD**: `ADD` has extra features (tar extraction, URL fetching) that introduce unpredictability. Use `COPY` for simple file operations.
7. **Set USER to non-root**: Always run the final stage as a non-root user. Use distroless images which default to non-root.
8. **Add health checks**: Include a HEALTHCHECK instruction or configure health checks in the orchestrator.

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["/app/healthcheck"]
```

### Multi-Stage Build for Go

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.23-alpine AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server ./cmd/server

FROM gcr.io/distroless/static-debian12
COPY --from=build /app/server /server
USER nonroot:nonroot
ENTRYPOINT ["/server"]
```

**EN** — Go produces static binaries, enabling use of the minimal `distroless/static` base image (< 2MB). This drastically reduces the attack surface.

### Multi-Stage Build for Python

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt -o requirements.txt --without-hashes
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

**FR** — Pour Python, exporter les dependances via Poetry en requirements.txt, installer avec `--prefix`, puis copier uniquement les packages installes dans l'image finale.

### Layer Caching Optimization

```dockerfile
# BAD — Cache invalidated on any source change
COPY . .
RUN npm install && npm run build

# GOOD — Dependencies cached separately from source
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build
```

**EN** — Dependency installation is the most expensive step. By copying only the lock file first, Docker can cache the `npm ci` layer as long as dependencies haven't changed. Source code changes only invalidate the COPY and build layers.

### BuildKit Advanced Features

```dockerfile
# syntax=docker/dockerfile:1

# Cache mount — Persists cache between builds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Secret mount — Exposes secrets only during build (not in layer)
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci

# Bind mount — Avoids copying files into a layer
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=pnpm-lock.yaml,target=pnpm-lock.yaml \
    pnpm install --frozen-lockfile
```

**FR** — BuildKit offre des fonctionnalites avancees : `--mount=type=cache` pour persister le cache entre les builds, `--mount=type=secret` pour les secrets de build (non stockes dans les layers), et `--mount=type=bind` pour eviter des COPY inutiles.

---

## 2. Docker Compose

### Production-Grade Compose File

```yaml
# docker-compose.yml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  pgdata:
```

**EN** — Use health checks on all services. Use `depends_on` with `condition: service_healthy` to enforce startup order. Set resource limits. Use named volumes for persistent data.

**FR** — Utiliser des health checks sur tous les services. Utiliser `depends_on` avec `condition: service_healthy` pour imposer l'ordre de demarrage. Definir des limites de ressources.

### Compose for Development vs. Production

```yaml
# docker-compose.override.yml (development overrides, auto-loaded)
services:
  api:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules  # Anonymous volume to preserve container's node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=app:*
    command: ["pnpm", "dev"]
```

**EN** — Use `docker-compose.override.yml` for development-specific settings (volume mounts for hot reload, debug flags). The base `docker-compose.yml` should represent a production-like configuration.

---

## 3. Kubernetes Fundamentals

### Pod Specification — Best Practices

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  labels:
    app: api
    version: v2.3.1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
        version: v2.3.1
    spec:
      serviceAccountName: api  # Dedicated service account
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: api
          image: ghcr.io/org/api:a1b2c3d  # Pinned to commit SHA
          ports:
            - containerPort: 3000
              protocol: TCP
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 15
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          startupProbe:
            httpGet:
              path: /healthz
              port: 3000
            failureThreshold: 30
            periodSeconds: 2
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: database-url
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: api-config
                  key: log-level
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: api
```

**FR** — Points cles de cette specification : contexte de securite (non-root, seccomp), trois types de probes (liveness, readiness, startup), requests et limits de ressources, spread across zones, secrets via secretKeyRef, et image pinned au commit SHA.

### Services

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  type: ClusterIP
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 3000
      protocol: TCP
```

**EN** — Use `ClusterIP` for internal services, `LoadBalancer` for direct external access (cloud-specific), and `Ingress` for HTTP routing. Prefer Ingress over LoadBalancer for HTTP services to consolidate load balancers and save cost.

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 80
```

**FR** — Utiliser cert-manager pour la gestion automatique des certificats TLS. Ajouter des annotations pour le rate limiting, les timeouts et les configurations specifiques au controller d'Ingress.

### Horizontal Pod Autoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
```

**EN** — Configure HPA with both CPU and memory metrics. Set `scaleDown.stabilizationWindowSeconds` to 300 (5 minutes) to prevent flapping. Scale up aggressively (50% per minute), scale down conservatively (10% per minute).

### ConfigMaps and Secrets

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
data:
  log-level: "info"
  feature-flags-endpoint: "https://flags.example.com/api"
  max-connections: "100"

---
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
type: Opaque
data:
  database-url: cG9zdGdyZXM6Ly91c2VyOnBhc3NAZGIvYXBw  # base64 encoded
```

**EN** — Never store secrets in plain text in Git. Use sealed-secrets, external-secrets-operator (with AWS Secrets Manager, HashiCorp Vault, or GCP Secret Manager), or SOPS for encrypting secrets at rest in Git.

**FR** — Ne jamais stocker de secrets en clair dans Git. Utiliser sealed-secrets, external-secrets-operator ou SOPS pour chiffrer les secrets au repos dans Git.

### External Secrets Operator

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: api-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: api-secrets
  data:
    - secretKey: database-url
      remoteRef:
        key: production/api/database-url
```

**EN** — External Secrets Operator syncs secrets from external providers (AWS Secrets Manager, Vault, GCP SM) into Kubernetes Secrets. This is the recommended approach for production — it provides automatic rotation and a single source of truth for secrets.

---

## 4. Helm Charts

### Chart Structure

```
charts/api/
  Chart.yaml
  values.yaml
  values-staging.yaml
  values-production.yaml
  templates/
    deployment.yaml
    service.yaml
    ingress.yaml
    hpa.yaml
    configmap.yaml
    _helpers.tpl
```

### values.yaml

```yaml
replicaCount: 3

image:
  repository: ghcr.io/org/api
  tag: ""  # Overridden at deploy time
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilization: 70

ingress:
  enabled: true
  hostname: api.example.com
  tls: true

env:
  LOG_LEVEL: info
```

### Deployment Template

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "api.fullname" . }}
  labels:
    {{- include "api.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "api.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "api.selectorLabels" . | nindent 8 }}
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: 3000
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

**FR** — Le `checksum/config` dans les annotations force un rolling restart quand la ConfigMap change. Utiliser `_helpers.tpl` pour les labels et noms standards. Toujours tester les charts avec `helm template` et `helm lint` avant le deploiement.

**EN** — Always run `helm lint` and `helm template` in CI. Use `helm diff` plugin to preview changes before applying. Store charts in an OCI registry (GHCR, ECR) alongside container images.

---

## 5. Kustomize

### Kustomize Structure

```
k8s/
  base/
    deployment.yaml
    service.yaml
    kustomization.yaml
  overlays/
    dev/
      kustomization.yaml
      replica-patch.yaml
    staging/
      kustomization.yaml
    production/
      kustomization.yaml
      replica-patch.yaml
      hpa.yaml
```

### Base Kustomization

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
commonLabels:
  app: api
```

### Production Overlay

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
  - hpa.yaml
patches:
  - path: replica-patch.yaml
images:
  - name: ghcr.io/org/api
    newTag: a1b2c3d  # Updated by CI pipeline
namespace: api-production
```

**EN** — Use Kustomize when Helm templating feels like overkill. Kustomize works with plain YAML and uses patches for customization. Ideal for GitOps workflows — ArgoCD and Flux support Kustomize natively.

**FR** — Utiliser Kustomize quand le templating Helm est excessif. Kustomize fonctionne avec du YAML brut et utilise des patches pour la personnalisation. Ideal pour les workflows GitOps.

### Helm vs. Kustomize Decision

| Criteria | Helm | Kustomize |
|---|---|---|
| Templating | Full Go templating | Patch-based (Strategic Merge, JSON Patch) |
| Packaging | Chart as distributable package | Directory-based, not packaged |
| Complexity | Higher (templating syntax) | Lower (plain YAML + patches) |
| Ecosystem | Vast chart repository | Built into kubectl |
| Best for | Distributing to external users | Internal deployment customization |

---

## 6. Container Security

### Image Scanning with Trivy

```yaml
# GitHub Actions — Trivy scan
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/org/api:${{ github.sha }}
    format: sarif
    output: trivy-results.sarif
    severity: CRITICAL,HIGH
    exit-code: 1  # Fail pipeline on HIGH/CRITICAL

- name: Upload Trivy SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: trivy-results.sarif
```

**EN** — Scan every image in CI before pushing to registry. Upload results in SARIF format to GitHub Security tab. Also run nightly scans to catch newly disclosed CVEs in existing images.

### Container Security Hardening Checklist

1. **Use minimal base images**: distroless, Alpine, or scratch (for Go). Fewer packages = smaller attack surface.
2. **Run as non-root**: Set `USER nonroot` in Dockerfile and `runAsNonRoot: true` in Kubernetes securityContext.
3. **Read-only filesystem**: Set `readOnlyRootFilesystem: true` in securityContext. Mount writable volumes only where needed (/tmp).
4. **Drop all capabilities**: `securityContext.capabilities.drop: ["ALL"]`. Add back only specific capabilities if required.
5. **Use Seccomp profiles**: Set `seccompProfile.type: RuntimeDefault` to restrict system calls.
6. **No privilege escalation**: Set `allowPrivilegeEscalation: false`.
7. **Network policies**: Restrict pod-to-pod communication with Kubernetes NetworkPolicies. Default deny, explicitly allow.
8. **Image pull policy**: Use `IfNotPresent` with immutable tags (SHA-based) or `Always` with mutable tags.

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
  seccompProfile:
    type: RuntimeDefault
```

**FR** — Appliquer systematiquement ce securityContext a tous les conteneurs en production. Utiliser OPA Gatekeeper ou Kyverno pour imposer ces politiques au niveau du cluster.

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
  namespace: api
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - port: 3000
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: database
      ports:
        - port: 5432
    - to:  # Allow DNS
        - namespaceSelector: {}
      ports:
        - port: 53
          protocol: UDP
        - port: 53
          protocol: TCP
```

**EN** — Implement default-deny network policies, then explicitly allow required traffic. Always allow DNS egress (port 53). This limits the blast radius of a compromised pod.

### Admission Control with Kyverno

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-non-root
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-non-root
      match:
        any:
          - resources:
              kinds: ["Pod"]
      validate:
        message: "Containers must run as non-root"
        pattern:
          spec:
            containers:
              - securityContext:
                  runAsNonRoot: true
```

**FR** — Utiliser Kyverno ou OPA Gatekeeper pour imposer des politiques au niveau du cluster : images depuis des registres approuves uniquement, non-root obligatoire, labels requis, limites de ressources obligatoires.

**EN** — Enforce cluster-wide policies: approved registries only, non-root required, mandatory labels, mandatory resource limits. Use `Enforce` mode in production, `Audit` mode during rollout.

---

## 7. Container Image Optimization

### Image Size Comparison

| Base Image | Size | Use Case |
|---|---|---|
| `ubuntu:24.04` | ~78MB | Avoid for production |
| `node:22` | ~1.1GB | Build stage only |
| `node:22-alpine` | ~130MB | Good for Node.js apps |
| `node:22-slim` | ~200MB | When Alpine causes issues (musl vs glibc) |
| `gcr.io/distroless/nodejs22` | ~130MB | Best for Node.js production |
| `gcr.io/distroless/static` | ~2MB | Best for Go static binaries |
| `scratch` | 0MB | Absolute minimum (no shell, no debug tools) |

**EN** — Target the smallest image that works. Use distroless for production (no shell = harder to exploit). Use Alpine or slim for build stages. Reserve full images for development only.

### .dockerignore

```
.git
.github
node_modules
*.md
tests/
coverage/
.env*
docker-compose*.yml
.vscode/
.idea/
```

**FR** — Un `.dockerignore` bien configure reduit la taille du contexte de build et evite de copier des fichiers sensibles ou inutiles dans l'image. Toujours exclure `.git`, `node_modules`, et les fichiers `.env`.
