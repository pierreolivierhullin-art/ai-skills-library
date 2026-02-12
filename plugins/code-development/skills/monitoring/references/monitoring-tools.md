# Monitoring Tools / Outils de monitoring

## Introduction

Choosing the right monitoring and observability tools is one of the highest-leverage decisions for an engineering organization. This reference provides expert-level analysis of the major tools in the observability ecosystem: commercial platforms (Datadog, New Relic), open-source stacks (Grafana + Prometheus), error tracking (Sentry), uptime and synthetic monitoring, Real User Monitoring (RUM), and cloud cost monitoring (FinOps observability). It concludes with a comprehensive comparison matrix and selection guide.

Choisir les bons outils de monitoring et d'observabilité est l'une des décisions à plus fort effet de levier pour une organisation d'ingénierie. Cette référence fournit une analyse experte des outils majeurs de l'écosystème d'observabilité.

---

## 1. Datadog

### Overview / Vue d'ensemble

Datadog is the leading commercial observability platform, offering a unified experience across infrastructure monitoring, APM, logs, RUM, synthetic monitoring, security, and CI/CD visibility. It is the default choice for organizations that want a single-vendor, fully managed observability platform and can afford the cost.

Datadog est la plateforme d'observabilité commerciale leader, offrant une expérience unifiée. C'est le choix par défaut pour les organisations qui veulent un single-vendor managé et peuvent en assumer le coût.

### Key Products / Produits clés

| Product | Description | Pricing Model |
|---|---|---|
| **Infrastructure Monitoring** | Host, container, serverless, network monitoring | Per host/month ($15-23) |
| **APM & Distributed Tracing** | Service map, trace search, flame graphs, profiling | Per host/month ($31-40) |
| **Log Management** | Ingest, index, archive, rehydrate logs | Per GB ingested ($0.10) + indexed ($1.70/million events) |
| **RUM** | Browser & mobile performance, session replay | Per 1K sessions ($1.50-2.20) |
| **Synthetic Monitoring** | API tests, browser tests, multistep | Per 10K test runs ($5-12) |
| **Database Monitoring** | Query performance, explain plans, wait events | Per host/month ($70) |
| **Continuous Profiler** | Always-on CPU, memory, I/O profiling | Per host/month ($12-19) |
| **Security (SIEM/CSM)** | Cloud Security Posture Management, threat detection | Per host/GB |
| **CI Visibility** | Pipeline and test performance monitoring | Per committer/month |

### Strengths / Forces

- **Unified platform**: Seamlessly correlate metrics, traces, logs, and profiles in a single UI. Click from a slow trace to the relevant logs to the flame graph in seconds.
- **Auto-discovery**: Automatic service mapping and dependency detection via agent instrumentation.
- **Powerful query language**: Metrics, logs, and traces all queryable with rich filtering, grouping, and visualization.
- **Integrations**: 750+ out-of-the-box integrations (AWS, GCP, Azure, Kubernetes, databases, message queues, CDNs).
- **AI features (Watchdog)**: Automatic anomaly detection, root cause analysis, and alert correlation. LLM-powered incident investigation (Bits AI, launched 2024).
- **Notebooks**: Collaborative investigation documents combining queries, graphs, and commentary.

### Weaknesses / Faiblesses

- **Cost**: Datadog is expensive and costs scale rapidly with data volume. A mid-size company (50 hosts, moderate log volume) easily reaches $10-30k/month. Log management is the primary cost driver.
- **Vendor lock-in**: Despite OTel support, the full Datadog experience requires the Datadog agent and vendor-specific features.
- **Complex pricing**: Multiple SKUs with different pricing models makes cost prediction difficult. Spikes in log volume or custom metrics create surprise bills.
- **Custom metrics cost**: Custom metrics are billed per unique time series. Cardinality explosions can cause significant unexpected costs.

### Best Practices / Bonnes pratiques

1. **Use the OTel Collector as a proxy**: Route telemetry through the OTel Collector, then export to Datadog. This preserves vendor portability.
2. **Implement log pipelines**: Use Datadog's log pipelines to parse, filter, and route logs. Drop debug/trace logs before indexing. Use exclusion filters to reduce indexed volume by 50-80%.
3. **Control custom metric cardinality**: Audit custom metrics monthly. Use Datadog's Metrics Summary to identify high-cardinality offenders.
4. **Use Metrics without Limits**: Configure tags-to-keep lists to query only on necessary dimensions, reducing metric cost.
5. **Set budget alerts**: Configure cost anomaly alerts in Datadog's Usage & Billing to catch volume spikes early.

### When to Choose Datadog / Quand choisir Datadog

Choose Datadog when: the organization values time-to-value over cost, when a single platform for all observability is required, when the team lacks the expertise to manage open-source infrastructure, or when enterprise features (compliance, SSO, RBAC) are non-negotiable.

Choisir Datadog quand l'organisation valorise le time-to-value sur le coût, quand une plateforme unique est nécessaire, ou quand l'équipe manque d'expertise pour gérer de l'open-source.

---

## 2. Grafana + Prometheus Stack (LGTM) / Stack Grafana + Prometheus

### Overview / Vue d'ensemble

The Grafana LGTM stack (Loki, Grafana, Tempo, Mimir) is the leading open-source observability platform. Prometheus (or its scalable successor Mimir) handles metrics, Loki handles logs, Tempo handles traces, and Grafana provides the unified visualization layer. This stack offers full observability at a fraction of the cost of commercial platforms.

La stack LGTM (Loki, Grafana, Tempo, Mimir) est la plateforme d'observabilité open-source leader. Prometheus/Mimir pour les métriques, Loki pour les logs, Tempo pour les traces, et Grafana pour la visualisation.

### Components / Composants

#### Prometheus / Mimir (Metrics)

- **Prometheus**: Pull-based metrics collection with a powerful query language (PromQL). The de facto standard for Kubernetes metrics. Single-node, not natively horizontally scalable.
- **Grafana Mimir**: Horizontally scalable, multi-tenant, long-term storage for Prometheus metrics. Use when Prometheus single-node limits are reached (typically > 10M active series).
- **Thanos**: Alternative to Mimir for multi-cluster Prometheus with long-term storage. Sidecar or receive architecture.

#### Loki (Logs)

Log aggregation system that indexes only metadata (labels), not the full log content. 10-50x cheaper than Elasticsearch for log storage at scale. Query with LogQL (similar to PromQL). Native integration with Grafana for log-to-metric-to-trace correlation.

Système d'agrégation de logs qui indexe uniquement les métadonnées (labels). 10-50x moins cher qu'Elasticsearch à l'échelle.

#### Tempo (Traces)

Distributed tracing backend that requires only object storage (S3, GCS). No indexing infrastructure needed — uses trace IDs for lookup and TraceQL for querying. Lowest-cost trace storage option.

Backend de tracing distribué nécessitant uniquement du stockage objet. Coût de stockage de traces le plus bas.

#### Grafana (Visualization)

The universal observability dashboard. Connects to 100+ data sources. Rich visualization library, alerting engine, and exploration tools. Grafana Explore allows ad-hoc querying across metrics, logs, and traces.

#### Grafana Alloy (Agent / OTel Collector)

Grafana's observability agent (successor to Grafana Agent), built on the OTel Collector. Collects metrics, logs, traces, and profiles. Deploys as a DaemonSet, sidecar, or standalone.

#### Grafana Pyroscope (Continuous Profiling)

Continuous profiling backend integrated into Grafana. View flame graphs alongside metrics, logs, and traces. Link profiles to trace spans.

#### Grafana Beyla (eBPF Auto-instrumentation)

eBPF-based auto-instrumentation that generates RED metrics and distributed traces without any code changes. Deploy as a sidecar or DaemonSet.

### Self-Hosted vs. Grafana Cloud / Auto-hébergé vs. Grafana Cloud

| Aspect | Self-Hosted | Grafana Cloud |
|---|---|---|
| **Cost** | Infrastructure + operations cost | Per-usage pricing, generous free tier |
| **Operations** | You manage upgrades, scaling, storage | Fully managed by Grafana Labs |
| **Free tier** | Always free (open source) | 10K metrics, 50GB logs, 50GB traces free |
| **Customization** | Full control | Managed, some limitations |
| **Best for** | Teams with K8s expertise, cost-sensitive at scale | Teams wanting managed service, small-to-mid scale |

### Strengths / Forces

- **Cost**: 5-20x cheaper than Datadog at scale, especially for logs (Loki) and traces (Tempo).
- **No vendor lock-in**: Fully open source. Data is in your control. Use OTel for instrumentation.
- **PromQL**: The most powerful and widely-adopted metrics query language in the industry.
- **Community**: Massive ecosystem of dashboards, exporters, and integrations. Thousands of pre-built Grafana dashboards.
- **Kubernetes-native**: Prometheus is the default monitoring for Kubernetes. Best-in-class K8s observability.

### Weaknesses / Faiblesses

- **Operational complexity** (self-hosted): Running Prometheus, Loki, Tempo, and Mimir at scale requires significant Kubernetes expertise.
- **No unified search** (logs): Loki's label-based querying is less powerful than full-text search (Elasticsearch, Datadog).
- **Alerting**: Grafana Alerting has improved significantly but remains less polished than Datadog's.
- **APM experience**: No native APM view comparable to Datadog's service catalog and dependency map (though Grafana's Application Observability feature is closing the gap).

### When to Choose Grafana Stack / Quand choisir la stack Grafana

Choose when: cost is a primary concern, the team has Kubernetes expertise, open-source and data ownership are important, or the organization is already using Prometheus. Use Grafana Cloud for managed convenience.

Choisir quand le coût est une préoccupation primaire, l'équipe a une expertise Kubernetes, ou l'open-source et la propriété des données sont importants.

---

## 3. New Relic

### Overview / Vue d'ensemble

New Relic is a full-stack observability platform with a developer-friendly approach and a differentiated pricing model (per-user + data ingestion, rather than per-host + per-feature). It offers APM, infrastructure, logs, browser monitoring, mobile, synthetics, and AI monitoring.

New Relic est une plateforme d'observabilité full-stack avec une approche developer-friendly et un modèle de pricing différencié (par utilisateur + ingestion de données).

### Key Differentiators / Différenciateurs clés

- **Pricing model**: All features included in one plan. Pay per full-platform user ($49-549/user/month depending on tier) + data ingestion ($0.35-0.55/GB). 100GB/month free for all accounts.
- **NRQL**: New Relic Query Language is SQL-like, making it approachable for developers familiar with SQL.
- **AI Monitoring**: Native monitoring for AI/ML models, including LLM observability (token usage, latency, hallucination detection).
- **Vulnerability management**: Built-in security vulnerability scanning integrated with APM.
- **Change tracking**: Automatic deployment markers with performance comparison.

### Strengths / Forces

- **Simple pricing**: One price per user includes everything. Predictable costs.
- **Generous free tier**: 100GB/month free, 1 free full-platform user.
- **Developer experience**: Clean UI, fast query execution, good onboarding.
- **AI/LLM monitoring**: First major platform to offer dedicated AI observability.
- **Pixie integration**: eBPF-based Kubernetes observability via acquired Pixie technology.

### Weaknesses / Faiblesses

- **User-based pricing penalizes large teams**: As the number of full-platform users grows, costs increase significantly.
- **Smaller ecosystem**: Fewer integrations and community dashboards compared to Datadog or Grafana.
- **Enterprise features**: Less mature RBAC, SSO, and compliance features compared to Datadog.

### When to Choose New Relic / Quand choisir New Relic

Choose when: the team wants predictable per-user pricing, the free tier covers initial needs, AI/LLM monitoring is a priority, or the team prefers SQL-like querying.

---

## 4. Sentry (Error Tracking) / Sentry (suivi d'erreurs)

### Overview / Vue d'ensemble

Sentry is the leading error tracking and performance monitoring platform, focused on helping developers find and fix errors in their code. It captures exceptions with full stack traces, source maps, breadcrumbs, and context, grouped by root cause.

Sentry est la plateforme leader de suivi d'erreurs et monitoring de performance, focalisée sur l'aide aux développeurs pour trouver et corriger les erreurs.

### Key Features / Fonctionnalités clés

- **Error grouping**: Automatically groups similar errors into "issues" using fingerprinting algorithms. Reduces thousands of errors into actionable issues.
- **Stack traces with source context**: Full stack traces with source code context, source map support for minified JavaScript, and deobfuscation for mobile.
- **Breadcrumbs**: Automatic capture of events leading up to the error (console logs, HTTP requests, user interactions, navigation).
- **Release tracking**: Correlate errors with specific releases. Identify regressions introduced by a deployment.
- **Session replay**: Record and replay user sessions that led to errors. See exactly what the user experienced.
- **Performance monitoring**: Transaction-based performance tracking with distributed tracing.
- **Cron monitoring**: Monitor scheduled jobs — detect if cron jobs fail, run late, or take too long.
- **Profiling**: Continuous profiling integrated with error and performance data.

### Integration Pattern / Pattern d'intégration

Sentry complements (does not replace) full observability platforms. Use Sentry for error tracking and developer workflow, use Datadog/Grafana for metrics, infrastructure monitoring, and SLO management.

Sentry complète (ne remplace pas) les plateformes d'observabilité complètes. Utiliser Sentry pour le suivi d'erreurs et le workflow développeur.

```
Application → Sentry SDK (errors, performance)
           → OTel SDK (metrics, traces, logs) → OTel Collector → Datadog/Grafana
```

### Best Practices / Bonnes pratiques

1. **Configure source maps in CI/CD**: Upload source maps during build process for readable stack traces in production.
2. **Set up release tracking**: Tag Sentry events with the release version. Use `sentry-cli` in CI/CD to create releases and associate commits.
3. **Configure alert rules**: Alert on new issues (first-seen errors), regressions (resolved errors that reappear), and volume spikes.
4. **Assign ownership**: Use Sentry's code owners feature to automatically assign errors to the team that owns the code.
5. **Integrate with issue tracker**: Connect Sentry to Jira or Linear for automatic ticket creation on new error types.
6. **Use environments**: Separate errors by environment (production, staging, development) to focus on production issues.

### Pricing / Tarification

- **Developer (free)**: 5K errors/month, 10K transactions, 1 user.
- **Team**: $26/month per user, 50K errors, 100K transactions.
- **Business**: $80/month per user, 100K+ errors, advanced features.
- **Enterprise**: Custom pricing with SLA, SSO, custom retention.

### When to Choose Sentry / Quand choisir Sentry

Always include Sentry (or equivalent) in the stack. Error tracking is a distinct concern from general observability. Sentry's developer workflow (assign, track, resolve) is unmatched by general-purpose platforms. Use it alongside, not instead of, a metrics/tracing platform.

Toujours inclure Sentry dans la stack. Le suivi d'erreurs est une préoccupation distincte de l'observabilité générale.

---

## 5. Uptime Monitoring / Monitoring de disponibilité

### Purpose / Objectif

Uptime monitoring validates that services are reachable and responding correctly from external locations. It is the simplest and most critical form of monitoring — if the service is down, nothing else matters.

Le monitoring de disponibilité valide que les services sont accessibles et répondent correctement depuis des localisations externes. C'est la forme de monitoring la plus simple et la plus critique.

### Key Tools / Outils clés

#### Better Uptime (now Better Stack)

Modern uptime monitoring with integrated status pages and incident management.
- **Features**: HTTP, TCP, DNS, ping, cron monitoring. Multi-location checks (every 30s). Screenshot on failure. Integrated status page and on-call scheduling.
- **Pricing**: Free tier (10 monitors, 3-min interval), Starter $29/mo, Plus $79/mo.
- **Best for**: Teams wanting uptime + status page + on-call in one tool.

#### UptimeRobot

Simple, cost-effective uptime monitoring.
- **Features**: HTTP, keyword, ping, port, heartbeat monitors. 5-min intervals (free), 1-min (paid). Multi-location.
- **Pricing**: Free (50 monitors, 5-min), Pro $7/mo (50 monitors, 1-min).
- **Best for**: Budget-conscious teams needing basic uptime alerting.

#### Pingdom (SolarWinds)

Established uptime monitoring with transaction monitoring.
- **Features**: Uptime, transaction monitoring, page speed, RUM.
- **Pricing**: Starts at $15/month for 10 uptime monitors.

### Uptime Check Best Practices / Bonnes pratiques de vérification de disponibilité

1. **Monitor from multiple regions**: Check from at least 3 geographic locations. Confirm an outage from 2+ regions before alerting (avoids false positives from regional network issues).
2. **Check critical paths, not just `/health`**: Monitor the login page, checkout flow, API authentication endpoint — not just a health check that may succeed even when the application is broken.
3. **Include content validation**: Verify the response contains expected content (keyword checks), not just HTTP 200 status.
4. **Set appropriate intervals**: 1-minute checks for critical services, 5-minute for secondary. Sub-minute for payment/financial.
5. **Configure meaningful alerting**: Alert to Slack for 1 failure, page to PagerDuty for 2+ consecutive failures from multiple regions.

---

## 6. Synthetic Monitoring / Monitoring synthétique

### Purpose / Objectif

Synthetic monitoring executes scripted user flows (transactions) at regular intervals from external locations. It validates that multi-step user journeys work correctly, proactively detecting issues before real users encounter them.

Le monitoring synthétique exécute des flows utilisateur scriptés à intervalles réguliers depuis des localisations externes. Il valide que les parcours utilisateur multi-étapes fonctionnent correctement.

### Key Tools / Outils clés

- **Datadog Synthetic Monitoring**: API tests, browser tests (using headless Chrome), multistep API tests. Integrated with Datadog APM for backend trace correlation.
- **Grafana Synthetic Monitoring** (k6): Uses k6 browser for scripted browser tests. Open-source engine, managed checks via Grafana Cloud.
- **Checkly**: Developer-focused synthetic monitoring using Playwright scripts. Monitoring as Code (checks defined in code, version controlled). Excellent for API and browser testing.
- **New Relic Synthetics**: Scripted browser and API monitoring integrated with New Relic platform.

### What to Monitor Synthetically / Que monitorer synthétiquement

Prioritize critical user journeys:

| Journey | Check Type | Frequency |
|---|---|---|
| User login (SSO, email/password) | Browser test | Every 5 min |
| Checkout / payment flow | Browser test | Every 5 min |
| API authentication (token exchange) | API test | Every 1 min |
| Search functionality | API test | Every 5 min |
| Webhook endpoints | API test | Every 1 min |
| Third-party integrations (Stripe, Auth0) | API test | Every 5 min |
| Critical API endpoints | Multistep API test | Every 1 min |

### Monitoring as Code (MaC) / Monitoring as Code

Define synthetic checks as code alongside application code. Use Checkly or Datadog's Terraform provider to version-control monitoring configuration.

Définir les checks synthétiques comme du code. Utiliser Checkly ou le provider Terraform de Datadog pour versionner la configuration de monitoring.

```typescript
// Checkly - Playwright-based synthetic monitoring
import { test, expect } from '@playwright/test';

test('checkout flow completes successfully', async ({ page }) => {
  await page.goto('https://shop.example.com');

  // Add item to cart
  await page.click('[data-testid="product-card-1"]');
  await page.click('[data-testid="add-to-cart"]');

  // Navigate to checkout
  await page.click('[data-testid="cart-icon"]');
  await page.click('[data-testid="checkout-button"]');

  // Fill payment details (test card)
  await page.fill('[data-testid="card-number"]', '4242424242424242');
  await page.fill('[data-testid="card-expiry"]', '12/26');
  await page.fill('[data-testid="card-cvc"]', '123');

  // Complete purchase
  await page.click('[data-testid="pay-button"]');

  // Verify success
  await expect(page.locator('[data-testid="order-confirmation"]'))
    .toBeVisible({ timeout: 10000 });
});
```

---

## 7. Real User Monitoring (RUM) / Monitoring d'utilisateurs réels

### Purpose / Objectif

RUM captures performance and error data from real user browsers and devices. Unlike synthetic monitoring (controlled, scripted), RUM reflects the actual user experience across diverse devices, networks, and geographies.

Le RUM capture les données de performance et d'erreur depuis les navigateurs et appareils des vrais utilisateurs. Contrairement au monitoring synthétique, le RUM reflète l'expérience utilisateur réelle.

### Core Metrics: Core Web Vitals / Métriques fondamentales

| Metric | What It Measures | Good Threshold |
|---|---|---|
| **LCP** (Largest Contentful Paint) | Loading performance: time to render main content | < 2.5s |
| **INP** (Interaction to Next Paint) | Interactivity: response time to user input | < 200ms |
| **CLS** (Cumulative Layout Shift) | Visual stability: unexpected layout shifts | < 0.1 |
| **TTFB** (Time to First Byte) | Server response time | < 800ms |
| **FCP** (First Contentful Paint) | Time to first visual content | < 1.8s |

### Key Tools / Outils clés

- **Datadog RUM**: Full RUM with session replay, error tracking, and backend trace connection. Generous feature set, premium pricing.
- **Sentry Performance**: Transaction-based RUM with error context, session replay, and Web Vitals. Good for error-first monitoring.
- **New Relic Browser**: RUM with AJAX monitoring, JS error tracking, and distributed traces.
- **Grafana Faro**: Open-source RUM SDK by Grafana Labs. Sends data to Loki (logs) and Tempo (traces). Youngest product in this category but rapidly maturing.
- **Vercel Analytics** / **Netlify Analytics**: Platform-specific RUM for Vercel/Netlify deployments. Simple, automatic, limited customization.

### RUM Implementation / Implémentation RUM

1. Install the RUM SDK in the frontend application (script tag or npm package).
2. Configure source map uploads in CI/CD for readable stack traces.
3. Set up trace propagation: inject `traceparent` header in API calls from the browser to connect frontend sessions to backend traces.
4. Define custom user actions and business events (e.g., "add to cart," "complete purchase").
5. Create dashboards for Core Web Vitals segmented by page, device type, geography, and user cohort.

---

## 8. Cloud Cost Monitoring (FinOps Observability) / Monitoring des coûts cloud

### Purpose / Objectif

Monitor and optimize cloud infrastructure costs as a first-class observability signal. Unexpected cost spikes are incidents too. FinOps observability integrates cost data into the same dashboards and alerting workflows as performance data.

Monitorer et optimiser les coûts d'infrastructure cloud comme un signal d'observabilité de première classe. Les pics de coûts inattendus sont aussi des incidents.

### Key Tools / Outils clés

#### Dedicated FinOps Tools / Outils FinOps dédiés

- **Kubecost**: Kubernetes-specific cost monitoring. Per-namespace, per-deployment, per-pod cost allocation. Integrates with Grafana for dashboards.
- **Infracost**: Shift-left cloud cost estimation. Shows cost impact of Terraform changes in pull requests before they are applied.
- **Vantage**: Multi-cloud cost management with rich reporting, cost anomaly detection, and budgeting.
- **CloudZero**: Engineering-focused cost intelligence. Allocates costs to features, teams, and customers.

#### Cloud-Native Tools / Outils natifs cloud

- **AWS Cost Explorer + Budgets**: Native AWS cost monitoring with alerts on budget thresholds.
- **GCP Billing Reports + Budgets**: Native GCP cost monitoring.
- **Azure Cost Management**: Native Azure cost analysis and alerting.

#### Observability Platform Integration / Intégration plateforme d'observabilité

- **Datadog Cloud Cost Management**: Correlate cloud costs with infrastructure metrics. View cost per service, per environment, per team. Alert on cost anomalies.
- **Grafana + Kubecost**: Export Kubecost metrics to Prometheus, visualize in Grafana alongside performance metrics.

### Cost Monitoring Best Practices / Bonnes pratiques

1. **Alert on cost anomalies**: Set daily and weekly cost anomaly alerts (> 20% increase triggers investigation).
2. **Tag everything**: Apply cost allocation tags to all cloud resources (team, service, environment, cost center).
3. **Show cost in dashboards**: Add a cost panel to service dashboards so teams see the cost of their decisions.
4. **Review in PR**: Use Infracost to show cost impact of infrastructure changes in pull requests.
5. **Set budgets**: Define monthly budgets per team/service. Alert at 80% and 100% consumption.
6. **Monitor observability tool costs**: The monitoring tools themselves can be a significant cost center. Track Datadog, New Relic, or cloud logging costs as a percentage of total infrastructure spend. Target < 5-10% of total cloud spend.

---

## 9. Tool Selection Guide & Comparison Matrix / Guide de sélection et matrice de comparaison

### Decision Framework / Framework de décision

```
What is your primary constraint?

├── BUDGET (minimize cost)
│   ├── < $100/month → Grafana Cloud Free + Sentry Free + UptimeRobot Free
│   ├── $100-1000/month → Grafana Cloud + Sentry Team + Better Uptime
│   └── $1000-5000/month → Self-hosted Grafana LGTM + Sentry + Checkly
│
├── TIME-TO-VALUE (minimize setup effort)
│   ├── Small team (< 10 eng) → New Relic (free tier) + Sentry
│   ├── Mid team (10-50 eng) → Datadog + Sentry
│   └── Large team (50+ eng) → Datadog Enterprise
│
├── CONTROL (maximize data ownership)
│   ├── Self-hosted everything → Grafana LGTM + Sentry Self-Hosted + PagerDuty
│   └── Managed but open → Grafana Cloud + Sentry SaaS
│
└── SPECIALIZATION (specific use case)
    ├── Error tracking focus → Sentry
    ├── Kubernetes-native → Grafana + Prometheus + Beyla
    ├── AI/LLM monitoring → New Relic or Datadog LLM Observability
    └── FinOps → Kubecost + Infracost + Vantage
```

### Comprehensive Comparison Matrix / Matrice de comparaison complète

| Capability | Datadog | Grafana Stack | New Relic | Sentry |
|---|---|---|---|---|
| **Infrastructure monitoring** | Excellent | Excellent (Prometheus) | Good | N/A |
| **APM / Distributed tracing** | Excellent | Good (Tempo) | Excellent | Basic |
| **Log management** | Excellent | Good (Loki) | Good | N/A |
| **Error tracking** | Good | Basic | Good | Excellent |
| **RUM / Browser** | Excellent | Growing (Faro) | Good | Good |
| **Synthetic monitoring** | Excellent | Good (k6) | Good | N/A |
| **Continuous profiling** | Excellent | Good (Pyroscope) | Good | Good |
| **eBPF monitoring** | Basic | Excellent (Beyla) | Good (Pixie) | N/A |
| **AI/LLM monitoring** | Good | Basic | Excellent | Basic |
| **Kubernetes native** | Good | Excellent | Good | N/A |
| **Session replay** | Excellent | N/A | N/A | Excellent |
| **On-call / incident mgmt** | Basic (Incident Management) | Via PagerDuty/OpsGenie | Basic | N/A |
| **Cost monitoring (FinOps)** | Good | Via Kubecost | Basic | N/A |
| **OTel native support** | Good | Excellent | Good | Good |
| **Open source** | No | Yes | No | Yes (self-hosted) |
| **Free tier** | 14-day trial | Yes (generous) | Yes (100GB/mo) | Yes (5K errors) |
| **Approx. cost (50 hosts)** | $8-25k/mo | $0-3k/mo | $5-15k/mo | $500-2k/mo |
| **Best for** | Enterprises, all-in-one | Cost-conscious, K8s | Dev-friendly, AI | Error tracking |

### Recommended Stacks by Company Size / Stacks recommandées par taille d'entreprise

#### Startup (1-10 engineers) / Startup (1-10 ingénieurs)

```
Observability: Grafana Cloud (free tier) or New Relic (free tier)
Error tracking: Sentry (free tier)
Uptime: UptimeRobot (free)
Incidents: PagerDuty (free tier for up to 5 users) or Incident.io (free)
Cost: ~$0-100/month
```

#### Scale-up (10-50 engineers) / Scale-up

```
Observability: Grafana Cloud (paid) or Datadog
Error tracking: Sentry (Team)
Uptime + Synthetics: Better Uptime or Checkly
Incidents: PagerDuty or Incident.io
Cost: ~$1,000-10,000/month
```

#### Enterprise (50+ engineers) / Entreprise

```
Observability: Datadog or Grafana Enterprise Stack
Error tracking: Sentry (Business/Enterprise)
Uptime + Synthetics: Datadog Synthetics or Checkly
RUM: Datadog RUM or Sentry
Incidents: PagerDuty or Incident.io
FinOps: Kubecost + Infracost + Datadog Cloud Cost Management
Cost: ~$10,000-100,000+/month
```

---

## 10. Migration Strategy / Stratégie de migration

### Migrating Between Observability Platforms / Migrer entre plateformes

When migrating from one platform to another (e.g., Datadog to Grafana, or New Relic to Datadog):

1. **Instrument with OpenTelemetry first**: Before migrating, switch application instrumentation from vendor-specific SDKs to OpenTelemetry. This decouples instrumentation from the backend and makes the migration a backend-only change.

2. **Run dual-write during transition**: Configure the OTel Collector to export to both the old and new backend simultaneously. Run both for 2-4 weeks to validate parity.

3. **Migrate dashboards incrementally**: Recreate critical dashboards on the new platform first. Use Grafana's Terraform provider or Datadog's Terraform provider for infrastructure-as-code dashboard management.

4. **Migrate alerts last**: Once dashboards are validated and the team is comfortable with the new platform, migrate alerting rules. Do not migrate alerts and decommission the old platform simultaneously.

5. **Decommission the old platform**: After 4-8 weeks of dual-write with no issues, decommission the old backend. Remove old SDKs and agents from applications.

**Instrumenter avec OpenTelemetry d'abord** : Découpler l'instrumentation du backend rend la migration un changement backend-only. Exécuter en dual-write pendant 2-4 semaines pour valider la parité.

---

## Summary Checklist / Checklist récapitulatif

- [ ] Primary observability platform selected based on budget, team size, and requirements
- [ ] Error tracking (Sentry or equivalent) deployed for all services
- [ ] Uptime monitoring configured for all critical endpoints from multiple regions
- [ ] Synthetic monitoring covers critical user journeys (login, checkout, key APIs)
- [ ] RUM deployed for frontend performance with Core Web Vitals tracking
- [ ] Cloud cost monitoring configured with anomaly alerts
- [ ] All instrumentation uses OpenTelemetry (vendor-portable)
- [ ] OTel Collector deployed as the telemetry gateway
- [ ] Cost of observability tools is tracked and optimized (< 5-10% of cloud spend)
- [ ] Tool migration plan prepared using OTel + dual-write strategy
