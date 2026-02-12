---
name: monitoring
description: This skill should be used when the user asks about "monitoring", "observability", "logging", "metrics", "tracing", "alerting", "SLO", "SLI", "SLA", "incident management", "OpenTelemetry", "Datadog", "Grafana", "Sentry", "APM", "observabilité", "journalisation", "métriques", "traçabilité", "alertes", "gestion des incidents", "supervision", "distributed tracing", "traces distribuées", "log aggregation", "agrégation de logs", "Prometheus", "Loki", "ELK", "Elasticsearch", "Kibana", "PagerDuty", "OpsGenie", "New Relic", "error tracking", "suivi d'erreurs", "uptime monitoring", "health checks", "dashboards opérationnels", "on-call", "astreinte", "postmortem", "root cause analysis", "RCA", "error budget", or needs guidance on system observability, reliability monitoring, and incident response.
version: 1.1.0
last_updated: 2026-02
---

# Monitoring & Observability / Monitoring & Observabilité

## Overview / Vue d'ensemble

This skill covers the full spectrum of modern observability engineering: the three pillars (logs, metrics, traces), structured logging, distributed tracing with OpenTelemetry, SLO/SLI/SLA management, error budgets, alerting design, incident management, and post-mortem culture. It integrates state-of-the-art practices from 2024-2026 including OpenTelemetry as the universal standard, eBPF-based kernel-level monitoring, continuous profiling, AI-powered anomaly detection, and observability-driven development (ODD).

Cette skill couvre l'ensemble de l'ingénierie d'observabilité moderne : les trois piliers (logs, métriques, traces), le logging structuré, le tracing distribué avec OpenTelemetry, la gestion SLO/SLI/SLA, les budgets d'erreur, la conception d'alertes, la gestion d'incidents et la culture post-mortem. Elle intègre les pratiques état de l'art 2024-2026 incluant OpenTelemetry comme standard universel, le monitoring kernel via eBPF, le profiling continu, la détection d'anomalies par IA, et l'observability-driven development (ODD).

## When This Skill Applies / Quand cette skill s'applique

Apply this skill when the user needs to:
- Instrument an application with logs, metrics, or traces
- Set up or improve monitoring infrastructure
- Define SLOs, SLIs, or manage error budgets
- Design an alerting strategy or reduce alert fatigue
- Respond to or learn from production incidents
- Choose between observability tools (Datadog, Grafana, Sentry, etc.)
- Implement distributed tracing across microservices
- Optimize monitoring costs (FinOps for observability)
- Adopt OpenTelemetry or migrate from proprietary agents
- Build dashboards, runbooks, or status pages

Appliquer cette skill quand l'utilisateur a besoin de : instrumenter une application, configurer une infrastructure de monitoring, définir des SLOs, concevoir une stratégie d'alerting, gérer des incidents de production, choisir des outils d'observabilité, implémenter du tracing distribué, optimiser les coûts de monitoring, adopter OpenTelemetry, ou construire des dashboards et runbooks.

## Core Principles / Principes fondamentaux

### 1. Observe, Don't Just Monitor / Observer, ne pas juste monitorer

Distinguish monitoring (known-unknowns: "is the CPU high?") from observability (unknown-unknowns: "why is this request slow for this user?"). Design systems that allow asking arbitrary questions about internal state from external outputs. Prioritize high-cardinality, high-dimensionality data that enables exploration over pre-defined dashboards.

Distinguer le monitoring (known-unknowns) de l'observabilité (unknown-unknowns). Concevoir des systèmes permettant de poser des questions arbitraires sur l'état interne à partir des sorties externes. Privilégier les données à haute cardinalité et haute dimensionalité.

### 2. OpenTelemetry as the Universal Standard / OpenTelemetry comme standard universel

Adopt OpenTelemetry (OTel) as the single instrumentation layer. Use the OTel SDK for traces, metrics, and logs. Deploy the OTel Collector as the central telemetry pipeline — it decouples instrumentation from backend choice. Never lock instrumentation to a vendor; always use OTel-native APIs first. Leverage auto-instrumentation where available, then enrich with custom spans and attributes.

Adopter OpenTelemetry comme couche d'instrumentation unique. Utiliser le SDK OTel pour traces, métriques et logs. Déployer l'OTel Collector comme pipeline central de télémétrie. Ne jamais verrouiller l'instrumentation à un vendor.

### 3. SLO-Driven Reliability / Fiabilité pilotée par les SLOs

Define Service Level Indicators (SLIs) that reflect real user experience: availability, latency (p50, p95, p99), error rate, throughput. Set Service Level Objectives (SLOs) as targets over rolling windows (e.g., 99.9% availability over 30 days). Derive error budgets from SLOs. Alert on burn rate, not raw thresholds. Use error budget policies to balance feature velocity and reliability investment.

Définir des SLIs reflétant l'expérience utilisateur réelle. Fixer des SLOs comme objectifs sur des fenêtres glissantes. Dériver des budgets d'erreur des SLOs. Alerter sur le burn rate, pas sur des seuils bruts.

### 4. Signal, Not Noise / Du signal, pas du bruit

Design every alert to be actionable, meaningful, and requiring human judgment. Eliminate duplicate, stale, and low-value alerts ruthlessly. Implement alert routing based on severity (SEV1-4), time-of-day, and team ownership. Measure alert quality: ratio of actionable alerts vs. total pages. Target < 5 pages per on-call shift for sustainable operations.

Concevoir chaque alerte pour qu'elle soit actionnable, significative et nécessitant un jugement humain. Éliminer les alertes redondantes, obsolètes et à faible valeur. Cibler < 5 pages par rotation d'astreinte.

### 5. Blameless Continuous Improvement / Amélioration continue sans blâme

Conduct blameless post-mortems for every significant incident. Focus on systemic causes, not individual errors. Track action items to completion. Share post-mortems across the organization. Measure MTTR (Mean Time to Recovery), MTTD (Mean Time to Detection), and MTTR trends over time.

Mener des post-mortems sans blâme pour chaque incident significatif. Se concentrer sur les causes systémiques. Suivre les actions correctives jusqu'à completion.

## Key Frameworks & Methods / Frameworks et méthodes clés

### The Three Pillars of Observability / Les trois piliers de l'observabilité

| Pillar / Pilier | Purpose / Objectif | Key Tools / Outils |
|---|---|---|
| **Logs** | Discrete events, debugging context / Événements discrets, contexte de debug | ELK, Loki, Datadog Logs |
| **Metrics** | Aggregated numerical time-series / Séries temporelles numériques agrégées | Prometheus, Datadog, CloudWatch |
| **Traces** | Request flow across services / Flux de requêtes inter-services | Jaeger, Tempo, Datadog APM |

### Beyond the Three Pillars / Au-delà des trois piliers

- **Continuous Profiling**: Use Parca, Pyroscope, or Datadog Continuous Profiler to understand CPU, memory, and I/O at the code-level in production.
- **eBPF-based monitoring**: Leverage Cilium, Pixie, or Grafana Beyla for kernel-level network, security, and performance observability without code changes.
- **Wide Events / Structured Events**: Emit rich, high-cardinality events (Honeycomb-style) that combine trace, log, and metric data in a single event.
- **Real User Monitoring (RUM)**: Capture frontend performance from real browsers (Core Web Vitals, errors, session replay).

### The RED and USE Methods / Les méthodes RED et USE

- **RED** (for request-driven services): Rate, Errors, Duration per endpoint.
- **USE** (for infrastructure resources): Utilization, Saturation, Errors per resource (CPU, memory, disk, network).
- **The Four Golden Signals** (Google SRE): Latency, Traffic, Errors, Saturation.

### Observability-Driven Development (ODD)

Write observability instrumentation alongside feature code — not after. Include trace spans, custom metrics, and structured log lines in every pull request. Review instrumentation in code reviews. Consider observability a first-class feature, not an afterthought.

Écrire l'instrumentation d'observabilité en même temps que le code fonctionnel. Inclure spans, métriques custom et logs structurés dans chaque pull request. L'observabilité est une fonctionnalité de première classe.

## Decision Guide / Guide de décision

### Choosing an Observability Stack / Choisir une stack d'observabilité

```
START
├── Budget > $10k/month and want managed? → Datadog or New Relic
│   ├── Need APM + Logs + Infra in one? → Datadog
│   └── Developer-first, simple pricing? → New Relic
├── Budget-conscious, open-source preference? → Grafana Stack
│   ├── Metrics: Prometheus + Grafana
│   ├── Logs: Loki + Grafana
│   ├── Traces: Tempo + Grafana
│   └── All-in-one managed: Grafana Cloud
├── Error tracking primary need? → Sentry
├── Startup / early stage? → Grafana Cloud Free + Sentry Free
└── Enterprise, multi-cloud, compliance? → Datadog or Splunk
```

### Alerting Strategy Selection / Sélection de stratégie d'alerting

- **Threshold-based**: Use for infrastructure metrics with known bounds (disk > 90%, CPU > 95% sustained).
- **SLO burn-rate**: Use for service-level reliability (error budget consumed 10x faster than planned over 1h window).
- **Anomaly detection (AI/ML)**: Use for seasonal patterns, traffic shifts, or metrics where static thresholds fail.
- **Composite alerts**: Combine multiple signals to reduce false positives (e.g., high latency AND high error rate AND traffic above baseline).

## Common Patterns & Anti-Patterns / Patterns et anti-patterns courants

### Patterns (Do This / Faire)

- **Structured JSON logging** with correlation IDs, request IDs, user IDs, and trace IDs in every log line.
- **OTel Collector as gateway**: Route all telemetry through the Collector for filtering, sampling, enrichment before export.
- **Tail-based sampling**: Sample 100% of errored/slow traces, downsample healthy traces to control costs.
- **Dashboard hierarchy**: Start with a service-level overview, drill into per-endpoint, then per-instance.
- **Runbooks linked to alerts**: Every alert has a runbook URL explaining what it means and how to investigate.
- **Error budget review**: Weekly review of SLO status and error budget remaining with engineering leadership.

### Anti-Patterns (Avoid / Éviter)

- **Log-and-pray**: Logging everything to stdout with no structure, no correlation, no retention policy.
- **Dashboard-only monitoring**: Building dashboards nobody watches instead of proactive alerts.
- **Alert fatigue**: Hundreds of alerts, most ignored, causing real incidents to be missed.
- **Vendor lock-in instrumentation**: Using vendor-specific SDKs throughout application code instead of OTel.
- **Monitoring without SLOs**: No defined reliability targets means no way to prioritize reliability work.
- **Blame culture in post-mortems**: Focusing on "who" instead of "what" and "why" kills trust and learning.
- **Ignoring costs**: Unbounded log ingestion and metric cardinality explosion leading to $50k+ monthly bills.

## Implementation Workflow / Workflow d'implémentation

### Phase 1: Foundation (Week 1-2) / Phase 1 : Fondations

1. Deploy the OpenTelemetry Collector in your infrastructure (sidecar or gateway mode).
2. Add OTel SDK auto-instrumentation to all services (HTTP, gRPC, database clients).
3. Implement structured JSON logging with correlation IDs across all services.
4. Choose and configure a backend: Datadog, Grafana Cloud, or self-hosted Grafana stack.
5. Set up basic health checks and uptime monitoring for all critical endpoints.

### Phase 2: SLOs & Alerting (Week 3-4) / Phase 2 : SLOs et alerting

1. Identify 3-5 critical user journeys (e.g., login, checkout, search).
2. Define SLIs for each journey (availability and latency at minimum).
3. Set SLO targets based on business requirements and historical data.
4. Implement burn-rate alerts (fast burn: 14.4x over 1h, slow burn: 1x over 3 days).
5. Create on-call rotation with escalation policies.
6. Write runbooks for every alert.

### Phase 3: Maturity (Month 2-3) / Phase 3 : Maturité

1. Add custom business metrics (conversion rate, revenue per minute, queue depth).
2. Implement distributed tracing across all service boundaries.
3. Deploy continuous profiling in production.
4. Set up error budget policies and weekly review cadence.
5. Conduct the first post-mortem and establish the retrospective template.
6. Build a public or internal status page.

### Phase 4: Excellence (Ongoing) / Phase 4 : Excellence

1. Implement tail-based sampling to optimize costs while retaining signal.
2. Adopt eBPF-based monitoring for network and kernel observability.
3. Deploy AI/ML anomaly detection on key metrics.
4. Integrate observability into CI/CD (deployment markers, automated canary analysis).
5. Measure and report on MTTR, MTTD, alert quality, and SLO compliance monthly.
6. Practice chaos engineering with observability validation (GameDays).



## Template actionnable

### Template de postmortem

| Section | Contenu |
|---|---|
| **Titre** | Incident du ___ — ___ |
| **Sévérité** | P1 / P2 / P3 |
| **Durée** | Début: ___ — Fin: ___ — Durée totale: ___ |
| **Impact** | ___ utilisateurs affectés, ___ revenus perdus |
| **Timeline** | HH:MM — Événement 1 / HH:MM — Événement 2 / ... |
| **Root cause** | Cause racine identifiée : ___ |
| **Détection** | Comment l'incident a été détecté : ___ |
| **Résolution** | Actions prises pour résoudre : ___ |
| **Ce qui a fonctionné** | ___ |
| **Ce qui peut être amélioré** | ___ |
| **Action items** | 1. ___ (owner, deadline) / 2. ___ / 3. ___ |

## Prompts types

- "Comment mettre en place une stack d'observabilité complète ?"
- "Aide-moi à définir des SLOs pertinents pour notre API"
- "Propose une stratégie d'alerting qui évite l'alert fatigue"
- "Comment implémenter le distributed tracing avec OpenTelemetry ?"
- "Aide-moi à structurer nos logs pour faciliter le debugging"
- "Comment rédiger un bon postmortem après un incident ?"

## Skills connexes

| Skill | Lien |
|---|---|
| DevOps | `code-development:devops` — Infrastructure et pipeline de déploiement |
| Quality Reliability | `code-development:quality-reliability` — SRE et ingénierie de fiabilité |
| Architecture | `code-development:architecture` — Design d'observabilité dans l'architecture |
| Process Engineering | `code-development:process-engineering` — Processus d'incident et postmortem |
| Risk Management | `entreprise:risk-management` — Continuité d'activité et gestion de crise |

## Additional Resources / Ressources complémentaires

Consult the following reference files for deep-dive guidance on each domain:

- **[Observability Pillars](./references/observability-pillars.md)** — Structured logging, metrics types, distributed tracing, APM, log aggregation, eBPF, continuous profiling, wide events.
- **[SLO/SLI Management](./references/slo-sli-management.md)** — SLI definition, SLO targets, error budgets, burn rate alerts, SLA management, toil reduction. Based on Google SRE Book principles.
- **[Alerting & Incidents](./references/alerting-incidents.md)** — Alert design, on-call management, incident response process, post-mortem / blameless retrospectives, status pages, PagerDuty/OpsGenie/Incident.io.
- **[Monitoring Tools](./references/monitoring-tools.md)** — Datadog, Grafana+Prometheus, New Relic, Sentry, uptime monitoring, synthetic monitoring, RUM, cloud cost monitoring (FinOps), tool comparison matrix.

### External References / Références externes

- Google SRE Book: https://sre.google/sre-book/table-of-contents/
- OpenTelemetry Documentation: https://opentelemetry.io/docs/
- Charity Majors on Observability: https://charity.wtf/
- Honeycomb Observability Guide: https://www.honeycomb.io/what-is-observability
- Grafana LGTM Stack: https://grafana.com/oss/
