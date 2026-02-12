# The Pillars of Observability / Les piliers de l'observabilité

## Introduction

Modern observability rests on three foundational pillars — logs, metrics, and traces — extended by emerging capabilities: continuous profiling, eBPF-based kernel observability, and wide/structured events. This reference provides expert-level guidance on each pillar, including concrete implementation patterns, tool choices, and state-of-the-art practices for 2024-2026.

L'observabilité moderne repose sur trois piliers fondamentaux — logs, métriques et traces — étendus par des capacités émergentes : profiling continu, observabilité kernel via eBPF, et événements structurés/wide events. Cette référence fournit des conseils de niveau expert sur chaque pilier, incluant des patterns d'implémentation concrets, des choix d'outils et des pratiques état de l'art 2024-2026.

---

## 1. Structured Logging / Logging structuré

### Principles / Principes

Emit every log entry as a structured JSON object. Never use unstructured text logs in production systems. Structure enables machine parsing, filtering, aggregation, and correlation at scale.

Émettre chaque entrée de log sous forme d'objet JSON structuré. Ne jamais utiliser de logs texte non structurés en production. La structure permet le parsing machine, le filtrage, l'agrégation et la corrélation à l'échelle.

### Log Format Standard / Standard de format de log

Adopt a consistent schema across all services. Include these fields in every log entry:

```json
{
  "timestamp": "2025-06-15T14:23:45.123Z",
  "level": "error",
  "service": "payment-api",
  "version": "2.4.1",
  "environment": "production",
  "trace_id": "abc123def456",
  "span_id": "789ghi012",
  "request_id": "req-uuid-here",
  "user_id": "usr_42",
  "message": "Payment processing failed",
  "error": {
    "type": "StripeCardDeclinedError",
    "message": "Card was declined",
    "stack": "..."
  },
  "context": {
    "payment_amount": 4999,
    "currency": "EUR",
    "card_last4": "4242"
  },
  "duration_ms": 342
}
```

### Log Levels / Niveaux de log

Use log levels consistently across all services. Define organizational standards:

| Level | Usage / Utilisation | Example / Exemple |
|-------|---------------------|-------------------|
| **FATAL** | Application cannot continue, immediate shutdown / L'application ne peut pas continuer | `Database connection pool exhausted, shutting down` |
| **ERROR** | Operation failed, requires attention / Opération échouée, nécessite attention | `Payment charge failed: card_declined` |
| **WARN** | Unexpected condition, operation continued / Condition inattendue, opération continuée | `Retry attempt 3/5 for upstream service call` |
| **INFO** | Significant business events / Événements métier significatifs | `Order #1234 completed, total: €49.99` |
| **DEBUG** | Diagnostic information for development / Information diagnostique pour le développement | `Cache miss for key user:42:preferences` |
| **TRACE** | Fine-grained diagnostic, very verbose / Diagnostique fin, très verbeux | `Entering function processPayment with args {...}` |

**Production rule**: Set default level to INFO. Enable DEBUG per-service dynamically via feature flags or environment variables — never hardcode debug logging in production.

**Règle production** : Définir le niveau par défaut à INFO. Activer DEBUG par service dynamiquement via feature flags — ne jamais coder en dur le debug logging en production.

### Correlation IDs / IDs de corrélation

Propagate correlation identifiers through every request path. Generate a `request_id` at the edge (API gateway, load balancer) and pass it through all downstream services via HTTP headers (`X-Request-ID`) or gRPC metadata. Link this to the OpenTelemetry `trace_id` for seamless log-to-trace correlation.

Propager les identifiants de corrélation dans chaque chemin de requête. Générer un `request_id` à la frontière (API gateway) et le propager dans tous les services via headers HTTP ou metadata gRPC. Le lier au `trace_id` OpenTelemetry.

```python
# Python example: Middleware that injects correlation IDs
import uuid
from opentelemetry import trace

class CorrelationMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        span = trace.get_current_span()
        trace_id = format(span.get_span_context().trace_id, '032x')

        # Inject into logger context
        logger = structlog.get_logger()
        logger = logger.bind(
            request_id=request_id,
            trace_id=trace_id,
            user_id=request.user.id if request.user else None,
        )
        return self.app(request)
```

### Log Aggregation Backends / Backends d'agrégation de logs

#### ELK Stack (Elasticsearch, Logstash, Kibana)

Use for full-text search over logs when complex querying patterns are needed. Strengths: powerful query language (KQL/Lucene), mature ecosystem, strong for security/compliance use cases. Weaknesses: high resource cost, operational complexity, expensive at scale.

Utiliser pour la recherche full-text quand des patterns de requêtes complexes sont nécessaires. Forces : langage de requête puissant, écosystème mature. Faiblesses : coût élevé en ressources, complexité opérationnelle.

#### Grafana Loki

Use for cost-effective log aggregation that indexes only labels, not full log content. Loki stores logs as compressed chunks and queries them via LogQL. Ideal when paired with Grafana for unified metrics + logs + traces dashboards. Strengths: low cost (10-50x cheaper than ELK at scale), native Grafana integration, label-based querying. Weaknesses: no full-text index (grep-like queries are slower).

Utiliser pour une agrégation de logs économique qui indexe seulement les labels. Loki stocke les logs comme des chunks compressés. Idéal avec Grafana pour des dashboards unifiés métriques + logs + traces.

#### Datadog Logs

Use for unified APM + Logs + Infrastructure in a single managed platform. Strengths: seamless correlation with traces and metrics, powerful faceted search, log patterns and anomaly detection. Weaknesses: cost scales rapidly with volume, vendor lock-in risk.

Utiliser pour une plateforme unifiée APM + Logs + Infrastructure. Forces : corrélation transparente, recherche facettée. Faiblesses : coût qui scale rapidement.

### Log Retention Strategy / Stratégie de rétention des logs

Define tiered retention based on log criticality and regulatory requirements:

| Tier / Niveau | Retention | Examples / Exemples |
|---|---|---|
| **Hot** (searchable) | 7-30 days | Application errors, security events |
| **Warm** (queryable) | 30-90 days | INFO logs, audit trails |
| **Cold** (archived) | 1-7 years | Compliance data, financial transactions |
| **Dropped** | 0 days | Debug/trace logs in production, health check logs |

Implement log sampling for high-volume, low-value logs (health checks, heartbeats). Drop or sample these at the collector level to reduce storage costs by 40-70%.

Implémenter le sampling de logs pour les logs à haut volume et faible valeur. Supprimer ou échantillonner au niveau du collecteur pour réduire les coûts de stockage de 40-70%.

---

## 2. Metrics / Métriques

### Metric Types / Types de métriques

Understand and use the four fundamental metric types correctly:

#### Counter (Compteur)

A monotonically increasing value. Use for events that only go up: requests served, errors occurred, bytes transferred.

```prometheus
# Total HTTP requests processed
http_requests_total{method="POST", endpoint="/api/orders", status="200"} 15234
```

**Rule**: Never use a counter for values that can decrease. Never reset a counter in application code — let the monitoring system handle resets.

#### Gauge (Jauge)

A value that can go up and down. Use for current state: temperature, queue depth, active connections, memory usage.

```prometheus
# Current number of items in the processing queue
queue_depth{queue="order-processing"} 42
```

#### Histogram (Histogramme)

Samples observations into configurable buckets. Use for measuring distributions of request durations, response sizes. Histograms enable computing percentiles server-side.

```prometheus
# Request duration distribution
http_request_duration_seconds_bucket{endpoint="/api/search", le="0.1"} 8234
http_request_duration_seconds_bucket{endpoint="/api/search", le="0.5"} 9120
http_request_duration_seconds_bucket{endpoint="/api/search", le="1.0"} 9403
http_request_duration_seconds_bucket{endpoint="/api/search", le="+Inf"} 9500
```

**Bucket design**: Choose buckets aligned with your SLOs. If your latency SLO is < 500ms, include buckets at 50ms, 100ms, 200ms, 500ms, 1s, 5s. Use exponential bucketing for wide ranges.

#### Summary

Client-side computed percentiles. Use only when pre-computed quantiles are sufficient and you cannot aggregate across instances. Prefer histograms over summaries in most cases because histograms are aggregatable.

### Percentiles: p50, p95, p99 / Percentiles

- **p50 (median)**: The typical user experience. 50% of requests are faster than this.
- **p95**: The experience of the slowest 5% of users. Use as primary SLI for latency.
- **p99**: The tail latency. Critical for detecting issues affecting a small but significant percentage of users.
- **p99.9**: Use for high-criticality services (payment processing, authentication).

**Rule**: Never use averages for latency. Averages hide tail latency and mask real user suffering. Always report and alert on percentiles.

**Règle** : Ne jamais utiliser de moyennes pour la latence. Les moyennes masquent la latence de queue. Toujours rapporter et alerter sur les percentiles.

### Metric Cardinality Management / Gestion de la cardinalité des métriques

High cardinality (many unique label combinations) is the number-one cost driver in metrics systems. Control it:

- **Never use unbounded values as labels**: user IDs, request IDs, IP addresses, email addresses. These create millions of time series.
- **Use bounded enumerations**: HTTP method, status code category (2xx, 4xx, 5xx), environment, region.
- **Monitor cardinality**: Track `scrape_series_added` in Prometheus or use Datadog's Metrics Summary to identify cardinality explosions.
- **Set recording rules**: Pre-aggregate high-cardinality metrics into lower-cardinality summaries.

Ne jamais utiliser de valeurs non bornées comme labels. Utiliser des énumérations bornées. Surveiller la cardinalité. Pré-agréger via des recording rules.

### The RED Method (Request-Driven Services)

For every microservice endpoint, instrument:
- **R**ate: Requests per second (`http_requests_total`)
- **E**rrors: Failed requests per second (`http_requests_total{status=~"5.."}`)
- **D**uration: Distribution of request latency (`http_request_duration_seconds`)

### The USE Method (Infrastructure Resources)

For every physical or virtual resource, instrument:
- **U**tilization: Percentage of time the resource is busy (CPU %, memory %)
- **S**aturation: Degree to which the resource has extra work queued (run queue length, swap usage)
- **E**rrors: Count of error events (ECC errors, network packet drops)

---

## 3. Distributed Tracing / Tracing distribué

### OpenTelemetry Tracing Architecture / Architecture de tracing OpenTelemetry

OpenTelemetry is the CNCF standard for distributed tracing. Adopt it as the single instrumentation API across all languages and frameworks.

OpenTelemetry est le standard CNCF pour le tracing distribué. L'adopter comme API d'instrumentation unique.

#### Core Concepts / Concepts fondamentaux

- **Trace**: The entire journey of a request through the system, identified by a unique `trace_id`.
- **Span**: A single unit of work within a trace (e.g., an HTTP request, a database query, a function call). Each span has a `span_id`, parent `span_id`, start time, duration, status, and attributes.
- **Context Propagation**: The mechanism that passes trace context (`trace_id`, `span_id`) across process and network boundaries. Use W3C TraceContext headers (`traceparent`, `tracestate`) as the standard propagation format.

#### Instrumentation Strategy / Stratégie d'instrumentation

1. **Auto-instrumentation first**: Use OTel auto-instrumentation agents/libraries to capture HTTP, gRPC, database, and messaging spans automatically. Available for Java, Python, Node.js, .NET, Go, Ruby, PHP.

2. **Enrich with custom spans**: Add business-relevant spans manually for operations that auto-instrumentation cannot capture:

```typescript
// TypeScript/Node.js example
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('order-service');

async function processOrder(order: Order): Promise<OrderResult> {
  return tracer.startActiveSpan('process-order', async (span) => {
    span.setAttribute('order.id', order.id);
    span.setAttribute('order.total', order.totalAmount);
    span.setAttribute('order.item_count', order.items.length);

    try {
      const validated = await validateOrder(order);
      const charged = await chargePayment(order);
      const fulfilled = await fulfillOrder(order);

      span.setStatus({ code: SpanStatusCode.OK });
      return fulfilled;
    } catch (error) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
}
```

3. **Add span attributes generously**: Include business context (user tier, feature flags, A/B test variants) as span attributes. These become the high-cardinality dimensions that enable powerful querying.

#### OTel Collector Architecture / Architecture du OTel Collector

Deploy the OpenTelemetry Collector as the central telemetry pipeline between applications and backends:

```
Application (OTel SDK) → OTel Collector (Agent/Sidecar) → OTel Collector (Gateway) → Backend(s)
```

**Collector pipeline components**:
- **Receivers**: Accept telemetry data (OTLP, Jaeger, Zipkin, Prometheus).
- **Processors**: Transform, filter, batch, sample data. Use `batch` processor always. Use `tail_sampling` for intelligent trace sampling.
- **Exporters**: Send data to backends (OTLP, Datadog, Jaeger, Prometheus, Loki).

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 5s
    send_batch_size: 8192

  tail_sampling:
    decision_wait: 10s
    policies:
      - name: errors-policy
        type: status_code
        status_code: {status_codes: [ERROR]}
      - name: slow-traces
        type: latency
        latency: {threshold_ms: 2000}
      - name: probabilistic-sample
        type: probabilistic
        probabilistic: {sampling_percentage: 10}

  resource:
    attributes:
      - key: environment
        value: production
        action: upsert

exporters:
  otlp/tempo:
    endpoint: tempo.monitoring:4317
    tls:
      insecure: true
  otlp/datadog:
    endpoint: "https://api.datadoghq.eu"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, tail_sampling, resource]
      exporters: [otlp/tempo, otlp/datadog]
```

#### Sampling Strategies / Stratégies de sampling

- **Head-based sampling**: Decide at trace start whether to sample. Simple but may miss interesting traces. Use for very high throughput (> 100k spans/sec).
- **Tail-based sampling** (recommended): Decide after the trace completes. Keep 100% of error and slow traces, sample healthy traces probabilistically. Requires the OTel Collector's `tail_sampling` processor with sufficient memory.
- **Adaptive sampling**: Adjust sampling rates dynamically based on traffic volume. Useful for services with variable load.

**Sampling recommandé** : tail-based sampling. Conserver 100% des traces en erreur et lentes, échantillonner les traces saines. Nécessite le processeur `tail_sampling` du Collector.

---

## 4. Application Performance Monitoring (APM)

### What APM Provides / Ce que fournit l'APM

APM combines traces, metrics, and profiling into a unified service performance view:

- **Service map**: Automatic topology discovery showing service dependencies and health.
- **Endpoint performance**: Latency, throughput, and error rate per endpoint with trace drill-down.
- **Database query analysis**: Slow query identification, N+1 detection, connection pool monitoring.
- **Error tracking**: Grouped error classification with stack traces and frequency analysis.
- **Deployment tracking**: Performance comparison between deployments (before/after regression detection).

### APM Implementation / Implémentation APM

Use OpenTelemetry for instrumentation, then choose an APM backend:
- **Datadog APM**: Full-featured, automatic service map, live search on 100% of traces for 15 minutes.
- **Grafana Tempo + Grafana**: Open-source trace storage with TraceQL query language, integrated with Grafana dashboards.
- **New Relic APM**: Developer-friendly, generous free tier, automatic anomaly detection.
- **Elastic APM**: Part of the Elastic stack, good for orgs already on ELK.

---

## 5. Beyond the Three Pillars / Au-delà des trois piliers

### eBPF-Based Monitoring / Monitoring basé sur eBPF

eBPF (extended Berkeley Packet Filter) enables running sandboxed programs in the Linux kernel, providing observability without code changes or agent installation in application processes.

eBPF permet d'exécuter des programmes sandboxés dans le kernel Linux, fournissant de l'observabilité sans modification de code ni installation d'agent dans les processus applicatifs.

**Key tools / Outils clés**:
- **Grafana Beyla**: Auto-instruments HTTP/gRPC services using eBPF. Zero-code, zero-config observability. Generates RED metrics and distributed traces from kernel-level syscall observation.
- **Pixie (by New Relic)**: Captures full-body HTTP requests, database queries, and service maps using eBPF. Data stays in-cluster by default (privacy advantage).
- **Cilium**: Network observability and security via eBPF. Provides L3/L4/L7 network flow logs, DNS monitoring, and network policy enforcement.
- **bpftrace**: Low-level dynamic tracing tool for custom kernel and userspace probes.

**When to use eBPF**: Use for polyglot environments where installing language-specific agents is impractical, for network-level observability, for monitoring third-party binaries without source access, and for ultra-low-overhead production profiling.

### Continuous Profiling / Profiling continu

Run always-on, low-overhead CPU and memory profiling in production. Continuous profiling answers "which lines of code consume the most resources?" — not just "which service is slow?" but "which function, which line, which allocation."

Exécuter du profiling CPU et mémoire en continu en production, à faible surcoût. Le profiling continu répond à « quelles lignes de code consomment le plus de ressources ? ».

**Tools / Outils**:
- **Grafana Pyroscope**: Open-source continuous profiling, integrated with Grafana for flame graph visualization alongside metrics and traces.
- **Parca**: Open-source, eBPF-based profiling. Zero-instrumentation approach using Linux perf events.
- **Datadog Continuous Profiler**: Integrated with Datadog APM, correlate profiles with traces.
- **Polar Signals Cloud**: Managed Parca with advanced comparison and diff views.

**Implementation pattern**: Enable OTel span profiling to link profiles directly to trace spans. When a slow span is detected, jump directly to the flame graph showing what the code was doing during that span.

### Wide Events / Structured Events / Événements structurés

The wide events model (pioneered by Honeycomb) treats each request as a single, richly-attributed event rather than splitting it across logs, metrics, and traces. A single event contains hundreds of attributes: timing, user context, feature flags, business data, infrastructure metadata.

Le modèle wide events traite chaque requête comme un événement unique richement attributé plutôt que de le répartir entre logs, métriques et traces.

**Advantages / Avantages**:
- Ask arbitrary questions without pre-defining dashboards or metrics
- Group-by any dimension in real time (BubbleUp analysis)
- Debug novel, never-before-seen issues without pre-existing queries
- Reduce the mental overhead of correlating across three separate systems

**Implementation**: Use Honeycomb as a native wide-event backend, or build a similar pattern using OTel traces with rich span attributes exported to a columnar store (ClickHouse, Grafana Tempo with TraceQL).

```go
// Go example: Emitting a wide event via OTel span attributes
span.SetAttributes(
    attribute.String("user.id", user.ID),
    attribute.String("user.plan", user.Plan),
    attribute.String("feature_flag.new_checkout", featureFlags.Get("new_checkout")),
    attribute.Int("cart.item_count", len(cart.Items)),
    attribute.Float64("cart.total_amount", cart.Total),
    attribute.String("payment.provider", "stripe"),
    attribute.String("payment.method", card.Type),
    attribute.Int("db.query_count", queryCounter.Count()),
    attribute.Float64("db.total_duration_ms", queryCounter.TotalDuration().Milliseconds()),
    attribute.String("build.version", buildInfo.Version),
    attribute.String("build.commit", buildInfo.CommitSHA),
    attribute.String("cdn.cache_status", response.Header.Get("X-Cache")),
)
```

### Real User Monitoring (RUM) / Monitoring d'utilisateurs réels

Capture performance data from real user browsers and devices:

- **Core Web Vitals**: LCP (Largest Contentful Paint), INP (Interaction to Next Paint), CLS (Cumulative Layout Shift). These are Google's ranking signals and directly measure user experience.
- **Error tracking**: JavaScript errors with stack traces, source maps, and session replay.
- **Session replay**: Record and replay user sessions to reproduce bugs visually.
- **Resource timing**: Identify slow assets, third-party script impact, CDN performance.

**Tools**: Datadog RUM, Sentry (with session replay), New Relic Browser, Grafana Faro (open-source).

**Implementation**: Deploy the RUM SDK in the frontend, configure source map uploads in CI/CD, connect RUM sessions to backend traces via the `traceparent` header propagated from browser to API.

Déployer le SDK RUM dans le frontend, configurer l'upload des source maps en CI/CD, connecter les sessions RUM aux traces backend via le header `traceparent`.

---

## Summary Checklist / Checklist récapitulatif

- [ ] All logs are structured JSON with `trace_id`, `request_id`, `service`, `level`
- [ ] Log levels are consistent and production default is INFO
- [ ] Metrics use correct types (counter, gauge, histogram) with bounded cardinality
- [ ] Latency is reported as percentiles (p50, p95, p99), never averages
- [ ] RED metrics exist for every request-driven service
- [ ] OpenTelemetry SDK is installed with auto-instrumentation
- [ ] OTel Collector is deployed with batch processing and tail sampling
- [ ] W3C TraceContext propagation is configured across all service boundaries
- [ ] Custom spans include business-relevant attributes
- [ ] Log-to-trace correlation works end-to-end
- [ ] RUM is deployed for frontend performance monitoring
- [ ] Continuous profiling is enabled in production
