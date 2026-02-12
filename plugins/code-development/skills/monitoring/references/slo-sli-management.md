# SLO/SLI Management / Gestion des SLO/SLI

## Introduction

Service Level Objectives (SLOs) are the cornerstone of modern reliability engineering. They quantify "reliable enough" in terms users care about, provide a shared language between engineering, product, and business, and enable data-driven decisions about where to invest engineering effort. This reference covers SLI definition, SLO target setting, error budgets, burn rate alerting, SLA management, and toil reduction — grounded in Google SRE Book principles and extended with 2024-2026 industry practices.

Les Service Level Objectives (SLOs) sont la pierre angulaire de l'ingénierie de fiabilité moderne. Ils quantifient « suffisamment fiable » en termes qui importent aux utilisateurs, fournissent un langage commun entre ingénierie, produit et business, et permettent des décisions data-driven sur l'allocation de l'effort d'ingénierie.

---

## 1. Service Level Indicators (SLIs) / Indicateurs de niveau de service

### Definition / Définition

An SLI is a quantitative measure of some aspect of the service level provided to users. Define SLIs as ratios: the number of "good" events divided by the total number of events, expressed as a percentage.

Un SLI est une mesure quantitative d'un aspect du niveau de service fourni aux utilisateurs. Définir les SLIs comme des ratios : nombre d'événements « bons » divisé par le nombre total d'événements.

```
SLI = (Good Events / Total Events) × 100%
```

### Core SLI Categories / Catégories de SLI fondamentales

#### Availability / Disponibilité

Measure the proportion of requests that are served successfully (non-error responses).

```
Availability SLI = (Total requests - Server errors) / Total requests × 100%
```

**What counts as "good"**: HTTP 2xx and 3xx responses, plus expected 4xx (e.g., 404 for genuinely missing resources). Exclude 5xx responses and timeouts. Be explicit about what error codes indicate server failure vs. client error.

**Ce qui compte comme « bon »** : réponses HTTP 2xx et 3xx, plus les 4xx attendus. Exclure les 5xx et les timeouts. Être explicite sur la distinction erreur serveur vs. erreur client.

#### Latency / Latence

Measure the proportion of requests served faster than a threshold.

```
Latency SLI = (Requests completed in < Xms) / Total requests × 100%
```

**Best practice**: Define multiple latency SLIs at different thresholds:
- p50 latency SLI: "99% of requests complete in < 200ms" (median experience)
- p95 latency SLI: "95% of requests complete in < 500ms" (tail experience)
- p99 latency SLI: "99% of requests complete in < 2000ms" (worst-case experience)

**Measurement point**: Measure latency as close to the user as possible — at the load balancer or API gateway, not at the application server. This captures network latency, queue wait time, and processing time.

**Point de mesure** : Mesurer la latence au plus près de l'utilisateur — au niveau du load balancer ou API gateway, pas au niveau du serveur applicatif.

#### Throughput / Débit

Measure the system's ability to handle load.

```
Throughput SLI = (Requests processed successfully per second) / Expected baseline
```

Use throughput SLIs for batch processing, data pipelines, or systems where "keeping up" matters more than individual request latency.

#### Freshness / Fraîcheur

Measure how recent the data is, for systems that serve cached or replicated data.

```
Freshness SLI = (Queries returning data updated within X seconds) / Total queries × 100%
```

Use for search indexes, analytics dashboards, CDN-served content, read replicas.

#### Correctness / Exactitude

Measure the proportion of responses that return the correct result.

```
Correctness SLI = (Correct responses) / Total responses × 100%
```

Use for calculation engines, ML inference services, financial systems. Often measured via canary/golden dataset validation.

### SLI Implementation / Implémentation des SLIs

#### Where to Measure / Où mesurer

Choose the SLI measurement point strategically:

| Measurement Point | Pros | Cons |
|---|---|---|
| **Load balancer / CDN** | Closest to user, captures full stack | May lack application-level context |
| **API Gateway** | Good user proximity, rich request metadata | Misses network issues before gateway |
| **Application code** | Full business context, custom logic | Misses infrastructure failures |
| **Synthetic monitoring** | Controlled, consistent, proactive | Doesn't reflect real user distribution |
| **Client-side (RUM)** | Truest user experience | Noisy, device/network variability |

**Recommendation**: Use load balancer metrics as primary SLI source for availability and latency. Supplement with application-level metrics for business-specific SLIs. Use synthetic monitoring as a canary, not as the primary SLI.

**Recommandation** : Utiliser les métriques du load balancer comme source primaire de SLI. Compléter avec des métriques applicatives pour les SLIs métier.

#### Prometheus SLI Recording Rules / Règles d'enregistrement Prometheus

```yaml
# prometheus-rules.yaml
groups:
  - name: sli-recording-rules
    interval: 30s
    rules:
      # Availability SLI: proportion of non-5xx responses
      - record: sli:availability:ratio_rate5m
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))

      # Latency SLI: proportion of requests under 500ms
      - record: sli:latency:ratio_rate5m
        expr: |
          sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m]))
          /
          sum(rate(http_request_duration_seconds_count[5m]))

      # Error budget remaining (30-day rolling window)
      - record: sli:error_budget:remaining
        expr: |
          1 - (
            (1 - sli:availability:ratio_rate30d)
            /
            (1 - 0.999)
          )
```

---

## 2. Service Level Objectives (SLOs) / Objectifs de niveau de service

### Definition / Définition

An SLO is a target value or range for an SLI, measured over a time window. It represents the reliability commitment that the team aspires to maintain.

Un SLO est une valeur cible pour un SLI, mesurée sur une fenêtre de temps. Il représente l'engagement de fiabilité que l'équipe aspire à maintenir.

```
SLO: 99.9% of requests should return a non-error response over a 30-day rolling window.
```

### Setting SLO Targets / Définition des cibles SLO

#### Step 1: Measure current performance / Mesurer la performance actuelle

Before setting an SLO, collect at least 30 days of historical SLI data. Understand the baseline: if your service currently achieves 99.95% availability, do not set a 99.99% SLO without significant investment.

Avant de fixer un SLO, collecter au moins 30 jours de données historiques. Comprendre la baseline : si le service atteint actuellement 99.95%, ne pas fixer un SLO à 99.99% sans investissement significatif.

#### Step 2: Align with user expectations / Aligner avec les attentes utilisateurs

Ask: "At what point do users start noticing and complaining?" This is the user happiness threshold. Set the SLO slightly above this threshold.

| Service Type | Typical Availability SLO | Error Budget (30 days) |
|---|---|---|
| Internal tools | 99.0% | 7h 18m downtime |
| SaaS product (standard) | 99.9% | 43m 49s downtime |
| Payment/financial | 99.95% | 21m 55s downtime |
| Infrastructure/platform | 99.99% | 4m 23s downtime |

#### Step 3: Consider dependencies / Considérer les dépendances

A service cannot be more reliable than its least reliable critical dependency. If your database provides 99.95% availability, your API service cannot achieve 99.99%. Map dependency reliability and set SLOs accordingly.

Un service ne peut pas être plus fiable que sa dépendance critique la moins fiable. Cartographier la fiabilité des dépendances et fixer les SLOs en conséquence.

#### Step 4: Start conservative, tighten over time / Commencer conservateur, resserrer avec le temps

Set initial SLOs at or slightly below current performance. Tighten them as the team builds confidence and invests in reliability. A too-aggressive SLO creates constant firefighting; a too-loose SLO provides no signal.

### Rolling Windows vs. Calendar Windows / Fenêtres glissantes vs. calendaires

- **Rolling window (recommended)**: Evaluate the SLO over the last N days continuously. A 30-day rolling window updates every minute and always reflects the most recent 30 days. More responsive to recent changes.
- **Calendar window**: Evaluate over fixed periods (monthly, quarterly). Simpler for reporting but creates "budget reset" gaming behavior at the start of each period.

**Recommendation**: Use 30-day rolling windows for operational alerting. Use calendar quarters for executive reporting and SLA compliance.

---

## 3. Error Budgets / Budgets d'erreur

### Definition / Définition

The error budget is the allowed amount of unreliability: `Error Budget = 1 - SLO`. If the SLO is 99.9% availability, the error budget is 0.1% — meaning the service can fail for 0.1% of requests or time within the window.

Le budget d'erreur est la quantité d'indisponibilité autorisée : `Budget d'erreur = 1 - SLO`. Si le SLO est 99.9%, le budget d'erreur est 0.1%.

### Error Budget Calculation / Calcul du budget d'erreur

```
30-day error budget for 99.9% availability SLO:
- Total minutes in 30 days: 43,200 minutes
- Error budget: 43,200 × 0.001 = 43.2 minutes of downtime allowed
- Or: 0.1% of requests can fail

Current consumption:
- If 20 minutes of downtime have occurred: 46.3% of budget consumed
- Remaining: 23.2 minutes (53.7% remaining)
```

### Error Budget Policies / Politiques de budget d'erreur

Define organizational policies that trigger when error budgets are consumed:

| Budget Remaining | Policy / Politique | Action |
|---|---|---|
| **> 50%** | Normal operations | Ship features, experiment freely |
| **25-50%** | Caution | Prioritize reliability fixes alongside features |
| **10-25%** | Reliability focus | Halt non-critical feature work, focus on reliability |
| **< 10%** | Freeze | Feature freeze. All effort on reliability recovery. |
| **0% (exhausted)** | Full freeze | No changes except reliability improvements. Conduct review with leadership. |

Implement error budget review meetings weekly with engineering leads, product managers, and SRE/platform team. Display error budget status prominently on team dashboards.

Organiser des revues de budget d'erreur hebdomadaires avec les leads engineering, product managers et l'équipe SRE/plateforme.

### Burn Rate / Taux de consommation

Burn rate measures how fast the error budget is being consumed relative to the steady-state rate. A burn rate of 1x means the budget will be exactly exhausted at the end of the window. Higher burn rates indicate accelerated consumption.

Le burn rate mesure la vitesse de consommation du budget d'erreur par rapport au taux nominal. Un burn rate de 1x signifie que le budget sera exactement épuisé à la fin de la fenêtre.

```
Burn Rate = (Error rate observed) / (Error rate allowed by SLO)

Example:
- SLO: 99.9% over 30 days → allowed error rate = 0.1%
- Current error rate: 1% over the last hour
- Burn rate = 1% / 0.1% = 10x

At 10x burn rate, the 30-day budget will be exhausted in 3 days.
```

---

## 4. Burn Rate Alerting / Alerting par burn rate

### Why Burn Rate Beats Threshold Alerting / Pourquoi le burn rate surpasse l'alerting par seuil

Traditional threshold alerts (e.g., "error rate > 1%") are disconnected from business impact. They fire at arbitrary thresholds that may or may not matter. Burn rate alerts are directly tied to SLO compliance: they fire when reliability is degrading fast enough to exhaust the error budget within a meaningful timeframe.

Les alertes par seuil traditionnelles sont déconnectées de l'impact métier. Les alertes par burn rate sont directement liées à la conformité SLO.

### Multi-Window, Multi-Burn-Rate Alerting / Alerting multi-fenêtre, multi-burn-rate

Implement the Google SRE recommended multi-window approach:

| Alert Level | Burn Rate | Long Window | Short Window | Budget Consumed | Action |
|---|---|---|---|---|---|
| **Page (SEV1)** | 14.4x | 1 hour | 5 minutes | 2% in 1h | Wake someone up |
| **Page (SEV2)** | 6x | 6 hours | 30 minutes | 5% in 6h | Urgent during business hours |
| **Ticket (SEV3)** | 1x | 3 days | 6 hours | 10% in 3d | Create a ticket, fix within days |

**Multi-window logic**: Both the long window AND short window must be in violation simultaneously. The long window provides confidence (not a blip), while the short window confirms the issue is still ongoing (not already recovered).

**Logique multi-fenêtre** : Les deux fenêtres (longue ET courte) doivent être en violation simultanément. La fenêtre longue donne la confiance, la courte confirme que le problème est en cours.

#### Prometheus Alert Rules / Règles d'alerte Prometheus

```yaml
groups:
  - name: slo-burn-rate-alerts
    rules:
      # Fast burn: 14.4x over 1h AND 5m (pages immediately)
      - alert: HighErrorBudgetBurn_Critical
        expr: |
          (
            sli:availability:ratio_rate1h < (1 - 14.4 * (1 - 0.999))
          )
          and
          (
            sli:availability:ratio_rate5m < (1 - 14.4 * (1 - 0.999))
          )
        for: 2m
        labels:
          severity: critical
          slo: availability
        annotations:
          summary: "High error budget burn rate (14.4x)"
          description: >
            Service availability SLI is {{ $value | humanizePercentage }}.
            At this rate, the 30-day error budget will be exhausted in ~50 hours.
          runbook_url: "https://runbooks.internal/slo-availability-critical"

      # Slow burn: 6x over 6h AND 30m
      - alert: HighErrorBudgetBurn_Warning
        expr: |
          (
            sli:availability:ratio_rate6h < (1 - 6 * (1 - 0.999))
          )
          and
          (
            sli:availability:ratio_rate30m < (1 - 6 * (1 - 0.999))
          )
        for: 5m
        labels:
          severity: warning
          slo: availability
        annotations:
          summary: "Elevated error budget burn rate (6x)"
          description: >
            Service availability SLI is {{ $value | humanizePercentage }} over 6h.
          runbook_url: "https://runbooks.internal/slo-availability-warning"

      # Slow leak: 1x over 3d AND 6h
      - alert: ErrorBudgetSlowLeak
        expr: |
          (
            sli:availability:ratio_rate3d < (1 - 1 * (1 - 0.999))
          )
          and
          (
            sli:availability:ratio_rate6h < (1 - 1 * (1 - 0.999))
          )
        for: 30m
        labels:
          severity: info
          slo: availability
        annotations:
          summary: "Error budget slow leak detected"
          runbook_url: "https://runbooks.internal/slo-availability-slowleak"
```

### SLO Monitoring Dashboards / Dashboards de monitoring SLO

Build a central SLO dashboard showing for each critical service:

1. **Current SLI value** (e.g., 99.94% over last 30 days)
2. **SLO target line** (e.g., 99.9%)
3. **Error budget remaining** as percentage and absolute time
4. **Error budget burn rate** over multiple windows (1h, 6h, 3d)
5. **Budget consumption timeline** showing how budget was consumed over the window
6. **Incident markers** overlaid on the timeline

---

## 5. SLA Management / Gestion des SLA

### SLA vs. SLO Distinction / Distinction SLA vs. SLO

- **SLO** (Service Level Objective): Internal target. No contractual consequences for missing it. Set aggressively to drive improvement.
- **SLA** (Service Level Agreement): External contractual commitment to customers. Has financial consequences (credits, penalties) if breached.

**Golden rule**: Always set the SLO stricter than the SLA. If the SLA promises 99.9%, set the internal SLO to 99.95% or 99.99%. This creates a safety buffer: the team will react to SLO violations long before the SLA is breached.

**Règle d'or** : Toujours fixer le SLO plus strict que le SLA. Si le SLA promet 99.9%, fixer le SLO interne à 99.95%. Cela crée une marge de sécurité.

### SLA Reporting / Reporting SLA

Automate SLA compliance reporting:
- Generate monthly/quarterly reports showing SLA compliance for each customer tier.
- Track SLA credits owed automatically.
- Alert the account management team before SLA breaches occur (when SLO alerts fire, the SLA buffer provides time to act).

---

## 6. Toil Measurement & Reduction / Mesure et réduction du toil

### Definition / Définition

Toil is the kind of work tied to running a production service that tends to be manual, repetitive, automatable, tactical, without enduring value, and that scales linearly with service growth (Google SRE definition).

Le toil est le travail lié à l'exploitation d'un service de production qui est manuel, répétitif, automatisable, tactique, sans valeur durable, et qui scale linéairement avec la croissance.

### Measuring Toil / Mesurer le toil

Track time spent on toil activities weekly:

| Toil Category | Examples / Exemples | Target |
|---|---|---|
| **Manual incident response** | Restarting pods, clearing queues, scaling | < 2h/week |
| **Manual deployments** | Steps requiring human intervention | 0 (fully automated) |
| **Alert triage** | Investigating non-actionable alerts | < 1h/week |
| **Capacity management** | Manual scaling, resource requests | < 1h/week |
| **Configuration changes** | Manual config updates across envs | 0 (GitOps automated) |
| **Data management** | Manual database operations, migrations | < 1h/week |

**Google SRE target**: No team should spend more than 50% of their time on toil. Target 30% or less. Track toil percentage as a team-level metric and report it alongside SLO compliance.

**Cible Google SRE** : Aucune équipe ne doit passer plus de 50% de son temps en toil. Viser 30% ou moins.

### Toil Reduction Strategies / Stratégies de réduction du toil

1. **Automate incident remediation**: Create runbook automation for common incidents (auto-scale, auto-restart, auto-rollback).
2. **Eliminate noisy alerts**: Every non-actionable alert is toil. Remove or fix them.
3. **Self-healing systems**: Implement health check-based auto-recovery (Kubernetes liveness/readiness probes, circuit breakers with automatic reset).
4. **GitOps for configuration**: All configuration changes through version-controlled pull requests, automatically applied.
5. **Capacity auto-scaling**: Horizontal Pod Autoscaler, KEDA event-driven autoscaling, cloud auto-scaling groups.
6. **Invest in developer self-service**: Platform teams provide self-service tools so application teams manage their own SLOs, alerts, and dashboards.

---

## 7. Practical SLO Adoption Playbook / Guide pratique d'adoption des SLOs

### Step-by-Step / Étape par étape

1. **Identify critical user journeys**: Start with 3-5 journeys that most impact business outcomes (e.g., user login, search, checkout, data export).

2. **Define SLIs for each journey**: At minimum, availability and latency. Add throughput and freshness where relevant.

3. **Collect baseline data**: Run SLI recording rules for 2-4 weeks before setting SLO targets.

4. **Set initial SLOs**: Set at or slightly below current performance. Get buy-in from product and engineering leadership.

5. **Implement error budget tracking**: Dashboard showing real-time error budget for each SLO.

6. **Configure burn-rate alerts**: Start with fast-burn (14.4x/1h) and slow-burn (6x/6h). Add slow-leak (1x/3d) once the team is comfortable.

7. **Establish error budget policies**: Define what happens at each budget threshold. Get agreement from product and engineering.

8. **Conduct weekly SLO reviews**: 15-minute weekly meeting reviewing all SLOs, budget status, and action items.

9. **Iterate**: Tighten or loosen SLOs based on 3 months of data. Add SLOs for more services. Refine SLI definitions.

10. **Connect to SLAs**: Once internal SLOs are mature and consistently met, use them to inform external SLA commitments with appropriate safety margins.

---

## Summary Checklist / Checklist récapitulatif

- [ ] SLIs are defined as ratios (good events / total events) for all critical journeys
- [ ] SLIs measure at the closest point to the user (load balancer or API gateway)
- [ ] Latency SLIs use percentiles, not averages
- [ ] SLO targets are set based on historical data and user expectations
- [ ] 30-day rolling windows are used for operational SLOs
- [ ] Error budgets are calculated and displayed on dashboards
- [ ] Multi-window burn-rate alerts are configured (14.4x/1h, 6x/6h, 1x/3d)
- [ ] Error budget policies define actions at each consumption threshold
- [ ] SLOs are stricter than SLAs with a safety buffer
- [ ] Weekly SLO review meetings are established
- [ ] Toil is measured and targeted for reduction below 30%
- [ ] SLO compliance is reported to engineering leadership monthly
