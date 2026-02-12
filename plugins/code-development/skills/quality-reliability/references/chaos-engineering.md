# Chaos Engineering / Ingenierie du chaos

Reference approfondie sur les principes du chaos engineering, l'injection de pannes, les game days, la gestion du blast radius et les patterns de resilience.

Deep-dive reference on chaos engineering principles, failure injection, game days, blast radius management, and resilience patterns.

---

## Table of Contents

1. [Chaos Engineering Principles](#chaos-engineering-principles)
2. [Failure Injection Tools](#failure-injection-tools)
3. [Game Days & Experiments](#game-days--experiments)
4. [Steady-State Hypothesis](#steady-state-hypothesis)
5. [Blast Radius Management](#blast-radius-management)
6. [Chaos in CI/CD](#chaos-in-cicd)
7. [Resilience Patterns](#resilience-patterns)

---

## Chaos Engineering Principles

### Fondation / Foundation

Le chaos engineering est la discipline consistant a experimenter sur un systeme en production pour etablir la confiance dans sa capacite a resister aux conditions turbulentes. Formalise par Netflix avec le manifeste "Principles of Chaos Engineering", il part d'un constat simple : les systemes distribues complexes echouent de facons imprevisibles, et la seule maniere de les comprendre est de les provoquer de maniere controlee.

Chaos engineering is the discipline of experimenting on a production system to build confidence in its ability to withstand turbulent conditions. Formalized by Netflix with the "Principles of Chaos Engineering" manifesto, it starts from a simple observation: complex distributed systems fail in unpredictable ways, and the only way to understand them is to provoke failures in a controlled manner.

### Les 5 principes du chaos engineering / The 5 Principles of Chaos Engineering

1. **Definir un "steady state" mesurable** — Identifier les metriques qui representent le comportement normal du systeme (throughput, latence, taux d'erreur). Le steady state est la baseline de reference. / Define a measurable "steady state" — Identify metrics representing normal system behavior. The steady state is the reference baseline.

2. **Hypothetiser que le steady state sera maintenu** — Formuler une hypothese : "meme sous cette perturbation, les metriques resteront dans les limites acceptables". L'experience doit tenter de refuter cette hypothese. / Hypothesize that the steady state will be maintained — The experiment must attempt to disprove this hypothesis.

3. **Varier les evenements du monde reel** — Injecter des perturbations realistes : crash de serveur, latence reseau, perte de connexion DB, saturation CPU, corruption de donnees, expiration de certificats, perte d'une availability zone. / Vary real-world events — Inject realistic disruptions.

4. **Executer les experiences en production** — Les environnements de staging ne reproduisent pas fidelement les conditions de production (trafic reel, donnees reelles, integrations tierces). Executer en production avec des garde-fous stricts. / Run experiments in production — Staging environments do not faithfully reproduce production conditions. Run in production with strict safeguards.

5. **Automatiser les experiences en continu** — Le chaos engineering n'est pas un evenement ponctuel. Automatiser les experiences dans le pipeline CI/CD et les executer continuellement pour detecter les regressions de resilience. / Automate experiments continuously — Chaos engineering is not a one-time event.

### Maturite du chaos engineering / Chaos Engineering Maturity Model

```
Niveau 0 — Ad hoc
  Pas d'experimentation de resilience. Les pannes sont decouvertes en production de maniere non planifiee.

Niveau 1 — Game Days manuels
  Exercices ponctuels (trimestriels) avec injection manuelle de pannes. Runbooks documentes.

Niveau 2 — Experiences automatisees
  Outils de chaos engineering deployes (Litmus, Gremlin). Experiences executees regulierement
  avec steady-state monitoring automatise.

Niveau 3 — Chaos continu
  Experiences integrees dans le pipeline CI/CD. Chaque deploy est valide par des chaos tests.
  Blast radius automatiquement limite.

Niveau 4 — Chaos autonome
  Systeme autonome qui identifie et execute les experiences pertinentes en fonction
  des changements du systeme. Self-healing valide automatiquement.
```

---

## Failure Injection Tools

### Chaos Monkey (Netflix)

L'outil pionnier du chaos engineering. Chaos Monkey termine aleatoirement des instances de VM ou des conteneurs en production pour forcer les equipes a concevoir des services resilients aux pannes d'instance.

The pioneering chaos engineering tool. Chaos Monkey randomly terminates VM instances or containers in production to force teams to design services resilient to instance failures.

**Cas d'usage / Use case:** Validation de base que les services survivent a la perte d'une instance.
**Limites / Limitations:** Scope limite (instance termination uniquement). Utiliser des outils plus complets pour une strategie de chaos mature.

### Gremlin

Gremlin est la plateforme SaaS leader pour le chaos engineering entreprise. Elle offre une interface graphique, des experiences predefinies et des controles de securite avances.

**Capacites / Capabilities:**
- **Infrastructure attacks** : CPU stress, memory pressure, disk I/O, shutdown.
- **Network attacks** : latence, perte de paquets, DNS failure, blackhole.
- **State attacks** : process kill, time travel (desynchronisation horloge), disk fill.
- **Application-level attacks** : injection d'erreurs HTTP, latence de requetes specifiques.

**Forces / Strengths:**
- Interface graphique accessible pour les equipes non-SRE.
- Controles de securite : halt button, blast radius limits, rollback automatique.
- Scenarios predefinis avec guides de remediation.
- Reporting et compliance pour les audits.

**Limites / Limitations:** Solution SaaS payante. Moins de flexibilite que les outils open-source pour des scenarios custom.

### Litmus (CNCF)

Litmus est le projet CNCF de reference pour le chaos engineering sur Kubernetes. Open-source, il offre un framework declaratif pour definir et executer des experiences de chaos.

Litmus is the reference CNCF project for chaos engineering on Kubernetes. Open-source, it offers a declarative framework for defining and running chaos experiments.

**Architecture Litmus:**

```yaml
# litmus-experiment.yaml — Pod kill experiment
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: checkout-chaos
  namespace: production
spec:
  appinfo:
    appns: production
    applabel: app=checkout-api
    appkind: deployment
  engineState: active
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '60'          # duree: 60 secondes
            - name: CHAOS_INTERVAL
              value: '10'          # supprimer un pod toutes les 10s
            - name: FORCE
              value: 'false'       # graceful shutdown
            - name: PODS_AFFECTED_PERC
              value: '50'          # affecter 50% des pods max
        probe:
          - name: checkout-health
            type: httpProbe
            httpProbe/inputs:
              url: http://checkout-api.production/health
              method:
                get:
                  criteria: ==
                  responseCode: '200'
            mode: Continuous
            runProperties:
              probeTimeout: 5s
              interval: 5s
              retry: 3
```

**Experiences Litmus disponibles / Available Litmus experiments:**
- **Pod-level** : pod-delete, container-kill, pod-cpu-hog, pod-memory-hog, pod-network-latency, pod-network-loss, pod-dns-error.
- **Node-level** : node-drain, node-taint, node-cpu-hog, node-memory-hog, node-io-stress.
- **Network** : pod-network-partition, pod-network-duplication, pod-network-corruption.
- **Application-specific** : spring-boot-faults, generic-http-chaos, kafka-broker-kill.

### Chaos Mesh (CNCF)

Alternative a Litmus, Chaos Mesh offre une plateforme de chaos engineering pour Kubernetes avec un dashboard web et un support de scenarios complexes via des workflows.

### Autres outils / Other Tools

| Outil / Tool | Type | Plateforme | Cas d'usage |
|---|---|---|---|
| **Toxiproxy** (Shopify) | Proxy TCP | Toutes | Injection de latence et erreurs reseau en dev/test |
| **Chaos Toolkit** | Framework | Toutes | Experiences declaratives multi-plateforme |
| **AWS Fault Injection Simulator** | SaaS | AWS | Chaos engineering natif AWS (EC2, ECS, EKS, RDS) |
| **Azure Chaos Studio** | SaaS | Azure | Chaos engineering natif Azure |
| **Pumba** | CLI | Docker | Chaos pour conteneurs Docker (kill, netem, stress) |
| **tc/netem** | Kernel | Linux | Injection de latence/perte reseau au niveau kernel |

---

## Game Days & Experiments

### Structure d'un Game Day

Un Game Day est un exercice planifie ou l'equipe execute des experiences de chaos engineering de maniere coordonnee. Il combine l'aspect technique (injection de pannes) et organisationnel (reponse d'equipe).

A Game Day is a planned exercise where the team executes chaos engineering experiments in a coordinated manner. It combines the technical aspect (failure injection) and the organizational aspect (team response).

### Preparation (1-2 semaines avant / 1-2 weeks before)

1. **Definir l'objectif** : quelle hypothese de resilience tester ? (ex: "le service checkout survit a la perte de la zone eu-west-1a").
2. **Identifier les participants** : SRE, on-call engineers, product owner, communication lead.
3. **Preparer les runbooks** : documenter les procedures de recovery pour chaque scenario.
4. **Valider les observability** : s'assurer que les dashboards et alertes couvrent les metriques impactees.
5. **Definir le blast radius** : limiter l'impact (un seul service, une seule zone, un pourcentage de trafic).
6. **Preparer le rollback** : avoir un bouton d'arret immediat (kill switch) pour chaque experience.
7. **Communiquer** : informer les equipes dependantes, le support client, le management.

### Execution (jour J)

```
09:00 — Briefing : rappel des objectifs, des scenarios et des criteres d'arret
09:15 — Pre-check : verification des metriques baseline, confirmation du steady state
09:30 — Experiment 1 : injection de la premiere perturbation
        → Observer les metriques, la reaction du systeme, les alertes declenchees
        → Documenter en temps reel : ce qui se passe, ce qui est attendu, les ecarts
10:00 — Debrief Experiment 1 : constats immediats
10:15 — Experiment 2 : scenario suivant (plus intense ou different)
        → Repeter observation et documentation
11:00 — Debrief Experiment 2
11:15 — Recovery : verifier le retour au steady state apres arret des perturbations
11:30 — Hot debrief : constats a chaud, surprises, points positifs, vulnerabilites decouvertes
```

### Post-Game Day (1 semaine apres)

1. **Rediger le rapport** : documenter chaque experience, resultats, ecarts avec les hypotheses.
2. **Identifier les action items** : vulnerabilites decouvertes, ameliorations necessaires.
3. **Prioriser les corrections** : integrer les action items dans le backlog avec une priorite proportionnelle au risque.
4. **Partager les apprentissages** : presentation a l'equipe elargie, mise a jour des runbooks.
5. **Planifier le prochain Game Day** : integrer les corrections et tester les memes scenarios + nouveaux.

---

## Steady-State Hypothesis

### Definition et formulation / Definition and Formulation

L'hypothese de steady state est l'affirmation centrale de chaque experience de chaos : "sous cette perturbation specifique, les metriques du systeme resteront dans les bornes de fonctionnement normal".

The steady-state hypothesis is the central assertion of each chaos experiment: "under this specific perturbation, system metrics will remain within normal operating bounds."

### Formulation structuree / Structured Formulation

```
GIVEN   : le systeme est dans son etat normal de fonctionnement
         [metriques baseline : latence p95 < 200ms, error rate < 0.1%, throughput > 500 req/s]

WHEN    : [perturbation specifique]
         ex: 50% des pods du service checkout sont termines brutalement

THEN    : [criteres de succes]
         - La latence p95 ne depasse pas 500ms (2.5x baseline)
         - Le taux d'erreur ne depasse pas 1% (10x baseline mais reste acceptable)
         - Le throughput ne descend pas sous 400 req/s (80% de la baseline)
         - Le service se retablit completement en moins de 2 minutes
         - Aucune perte de donnees (0 transactions perdues)
```

### Criteres d'arret / Abort Criteria

Definir des criteres d'arret immediat pour chaque experience :

- **Taux d'erreur > 5%** pendant plus de 30 secondes.
- **Latence p99 > 10s** (experience de degradation, pas d'interruption complete).
- **Perte de donnees detectee** : arret immediat.
- **Impact utilisateur reel signale** : arret immediat.
- **Le systeme ne montre aucun signe de recovery** apres 3 minutes.
- **Cascade vers des services non inclus** dans le perimetre de l'experience.

---

## Blast Radius Management

### Principes / Principles

Le blast radius est la portee de l'impact d'une experience de chaos. Commencer avec le plus petit blast radius possible et l'elargir progressivement une fois la confiance etablie.

The blast radius is the scope of impact of a chaos experiment. Start with the smallest possible blast radius and expand progressively once confidence is established.

### Strategies de limitation / Limitation Strategies

```
Progression recommandee du blast radius :
1. Environnement de dev/staging → valider les mecanismes et les outils
2. Canary en production (1-5% du trafic) → premier test production a risque minimal
3. Un service en production (hors heures de pointe) → valider la resilience du service
4. Zone de disponibilite (AZ) → valider le multi-AZ failover
5. Region entiere → valider le multi-region failover (annuel)
```

### Controles de securite / Safety Controls

1. **Kill switch** : bouton d'arret immediat accessible a tout participant du Game Day.
2. **Timeout automatique** : chaque experience a une duree maximale apres laquelle elle s'arrete automatiquement.
3. **Health probes** : monitoring continu du steady state pendant l'experience. Arret automatique si les criteres d'arret sont atteints.
4. **Traffic draining** : possibilite de drainer le trafic vers des instances saines instantanement.
5. **Scope limitation** : limiter l'experience a un pourcentage de pods/instances/trafic.
6. **Time-of-day restriction** : executer les experiences pendant les heures de faible trafic ou les heures ouvrables (pour avoir l'equipe disponible).

```yaml
# Litmus ChaosEngine - blast radius controls
spec:
  annotationCheck: 'true'    # only affect pods with chaos annotation
  engineState: active
  terminationGracePeriodSeconds: 30
  experiments:
    - name: pod-network-latency
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '120'         # max 2 minutes
            - name: NETWORK_LATENCY
              value: '200'         # 200ms added latency
            - name: PODS_AFFECTED_PERC
              value: '25'          # only 25% of pods affected
            - name: TARGET_PODS
              value: 'checkout-api-canary'  # only canary pods
```

---

## Chaos in CI/CD

### Principe / Principle

Integrer les experiences de chaos dans le pipeline CI/CD pour valider automatiquement la resilience a chaque deploy. Chaque changement de code ou de configuration doit prouver qu'il ne degrade pas la resilience du systeme.

Integrate chaos experiments into the CI/CD pipeline to automatically validate resilience on every deploy.

### Pipeline avec chaos testing / Pipeline with Chaos Testing

```yaml
# GitHub Actions - Chaos validation pipeline
name: Deploy with Chaos Validation
on:
  push:
    branches: [main]

jobs:
  deploy-canary:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy canary (10% traffic)
        run: kubectl apply -f k8s/canary-deployment.yaml
      - name: Wait for stable canary
        run: kubectl rollout status deployment/checkout-canary --timeout=120s

  chaos-validation:
    needs: deploy-canary
    runs-on: ubuntu-latest
    steps:
      - name: Run pod-kill experiment
        run: |
          kubectl apply -f chaos/pod-kill-experiment.yaml
          # Wait for experiment completion
          kubectl wait --for=condition=Complete chaosengine/checkout-chaos --timeout=300s
      - name: Validate steady state
        run: |
          # Check that error rate stayed below threshold during experiment
          python scripts/validate-steady-state.py \
            --service checkout-api \
            --metric error_rate --threshold 0.02 \
            --metric p95_latency --threshold 500 \
            --window 5m
      - name: Run network-latency experiment
        run: kubectl apply -f chaos/network-latency-experiment.yaml

  promote-or-rollback:
    needs: chaos-validation
    runs-on: ubuntu-latest
    steps:
      - name: Promote canary to full deployment
        if: success()
        run: kubectl apply -f k8s/full-deployment.yaml
      - name: Rollback canary
        if: failure()
        run: kubectl rollout undo deployment/checkout-canary
```

### Chaos en environnement de staging

Pour les equipes qui ne sont pas encore pretes pour le chaos en production, commencer par l'integrer dans le staging :

1. Deployer en staging avec une replique du trafic production (traffic mirroring).
2. Executer les experiences de chaos sur le staging.
3. Valider les metriques et les comportements de resilience.
4. Graduellement migrer les experiences vers la production (canary d'abord).

---

## Resilience Patterns

### Circuit Breaker

Le circuit breaker empeche un service de continuer a appeler un service dependant defaillant. Il evite la cascade de pannes et permet au service dependant de se retablir.

The circuit breaker prevents a service from continuing to call a failing dependent service. It avoids cascading failures and allows the dependent service to recover.

```
Etats du circuit breaker :
CLOSED (normal)   → Les requetes passent normalement. Le circuit breaker compte les erreurs.
OPEN (protection) → Le circuit est ouvert : toutes les requetes echouent immediatement
                    (fail fast) sans appeler le service dependant. Duree configurable.
HALF-OPEN (test)  → Un nombre limite de requetes est autorise pour tester la recovery.
                    Succes → retour a CLOSED. Echec → retour a OPEN.
```

```typescript
// Circuit breaker avec resilience4j (concept applicable en tout langage)
const circuitBreaker = new CircuitBreaker({
  failureRateThreshold: 50,      // ouvrir a 50% d'echecs
  slowCallRateThreshold: 80,     // ouvrir a 80% d'appels lents
  slowCallDurationThreshold: 2000, // "lent" = > 2s
  waitDurationInOpenState: 30000,  // rester ouvert 30s avant half-open
  permittedNumberOfCallsInHalfOpenState: 5, // 5 appels test en half-open
  slidingWindowSize: 20,         // fenetre de 20 appels
  minimumNumberOfCalls: 10,      // evaluer apres 10 appels min
});

// Usage avec fallback
async function getProductPrice(productId: string): Promise<Money> {
  try {
    return await circuitBreaker.execute(() =>
      pricingService.getPrice(productId)
    );
  } catch (error) {
    if (error instanceof CircuitBreakerOpenError) {
      // Fallback: utiliser le prix cache
      return cachedPricingService.getPrice(productId);
    }
    throw error;
  }
}
```

### Bulkhead (Cloison)

Le pattern bulkhead isole les composants pour qu'une defaillance dans un compartiment ne se propage pas aux autres. Inspire des cloisons etanches des navires.

The bulkhead pattern isolates components so that a failure in one compartment does not spread to others. Inspired by ship bulkheads.

**Implementations:**
- **Thread pool bulkhead** : chaque service dependant a son propre pool de threads. Si un service ralentit, seul son pool est sature.
- **Connection pool bulkhead** : pools de connexions separes par service dependant.
- **Pod-level bulkhead** (Kubernetes) : deployer les services critiques sur des node pools dedies pour isoler les ressources.

```yaml
# Kubernetes: bulkhead via resource limits et node affinity
apiVersion: apps/v1
kind: Deployment
metadata:
  name: checkout-api
spec:
  template:
    spec:
      containers:
        - name: checkout
          resources:
            requests:
              cpu: "500m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: tier
                    operator: In
                    values: ["critical"]
```

### Retry with Exponential Backoff and Jitter

Implementer les retries avec backoff exponentiel et jitter pour eviter les "thundering herd" (tempete de requetes synchronisees apres une panne).

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries: number;
    baseDelay: number;      // ms
    maxDelay: number;        // ms
    jitterFactor: number;    // 0-1
    retryableErrors?: (error: Error) => boolean;
  }
): Promise<T> {
  for (let attempt = 0; attempt <= options.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === options.maxRetries) throw error;
      if (options.retryableErrors && !options.retryableErrors(error)) throw error;

      const exponentialDelay = Math.min(
        options.baseDelay * Math.pow(2, attempt),
        options.maxDelay
      );
      const jitter = exponentialDelay * options.jitterFactor * Math.random();
      const delay = exponentialDelay + jitter;

      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  throw new Error('Unreachable');
}

// Usage
const result = await retryWithBackoff(
  () => paymentGateway.charge(amount),
  {
    maxRetries: 3,
    baseDelay: 200,
    maxDelay: 5000,
    jitterFactor: 0.5,
    retryableErrors: (e) => e instanceof TransientError,
  }
);
```

### Timeout

Definir des timeouts explicites sur chaque appel distant. Ne jamais utiliser les timeouts par defaut (souvent trop longs ou infinis).

```
Regle des timeouts :
- Timeout connect : 1-3 secondes (si l'hote ne repond pas, il est down)
- Timeout read : 2-10 secondes (selon la complexite de l'operation)
- Timeout total : toujours inferieur au timeout du client (cascade)
- Timeout du circuit breaker : slowCallDurationThreshold doit etre coherent
```

### Rate Limiting (Cote serveur)

Proteger les services contre la surcharge via le rate limiting. Implementer a l'API gateway et/ou au niveau service.

- **Token bucket** : autorise les bursts courts tout en limitant le debit moyen.
- **Leaky bucket** : lisse le trafic a un debit constant.
- **Fixed window** : compte les requetes par fenetre de temps fixe.
- **Sliding window** : compte les requetes sur une fenetre glissante (plus precis).

### Queue-Based Load Leveling

Utiliser une file d'attente pour absorber les pics de charge et lisser le traitement. Les producteurs enqueent les requetes, les consommateurs les traitent a un rythme stable.

```
[Clients] → [API Gateway] → [Message Queue (SQS/RabbitMQ/Kafka)]
                                        ↓
                              [Worker Pool (auto-scaled)]
                                        ↓
                              [Processing + DB Write]
```

### Fallback & Graceful Degradation

Implementer des fallbacks pour chaque dependance externe. Un service degrade est preferable a un service en erreur :

| Dependance en panne | Fallback | Impact utilisateur |
|---|---|---|
| Service de recommandations | Afficher les produits populaires (cache) | Minimal |
| Service de recherche | Proposer la navigation par categories | Modere |
| Service de paiement | Afficher un message "reessayer dans 5 min" | Visible mais clair |
| CDN d'images | Afficher des placeholders | Cosmetique |
| Service de notifications | Enqueuer et envoyer plus tard | Invisible |

---

## Summary Checklist / Checklist de synthese

- [ ] Les 5 principes du chaos engineering sont compris et acceptes par l'equipe
- [ ] Un outil de chaos engineering est deploye (Litmus, Gremlin, ou Chaos Mesh)
- [ ] Au moins un Game Day est conduit par trimestre avec documentation complete
- [ ] Chaque experience a une hypothese de steady state clairement formulee
- [ ] Les criteres d'arret (abort criteria) sont definis et automatises pour chaque experience
- [ ] Le blast radius est limite et progresse graduellement (staging → canary → production)
- [ ] Le chaos testing est integre dans le pipeline CI/CD (au minimum en staging)
- [ ] Les patterns de resilience sont implementes : circuit breaker, retry with backoff, timeout, bulkhead
- [ ] Les fallbacks sont definis et testes pour chaque dependance externe critique
- [ ] Les resultats des experiences sont documentes et les corrections sont traquees jusqu'a completion
