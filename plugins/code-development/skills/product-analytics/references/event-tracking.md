# Event Tracking & Instrumentation / Tracking événementiel & Instrumentation

Référence approfondie sur la conception de tracking plans, les conventions de nommage d'événements, l'instrumentation client-side et server-side, les SDKs analytics, la validation de données et la gouvernance du tracking.

Deep-dive reference on tracking plan design, event naming conventions, client-side and server-side instrumentation, analytics SDKs, data validation, and tracking governance.

---

## Table of Contents

1. [Tracking Plan Design](#tracking-plan-design)
2. [Event Naming Conventions & Taxonomy](#event-naming-conventions--taxonomy)
3. [Client-side Instrumentation](#client-side-instrumentation)
4. [Server-side Instrumentation](#server-side-instrumentation)
5. [Hybrid Tracking Architecture](#hybrid-tracking-architecture)
6. [SDKs & Customer Data Platforms](#sdks--customer-data-platforms)
7. [Data Validation & QA](#data-validation--qa)
8. [Schema Validation & Tracking as Code](#schema-validation--tracking-as-code)
9. [Tracking Governance](#tracking-governance)

---

## Tracking Plan Design

### What Is a Tracking Plan / Qu'est-ce qu'un tracking plan

A tracking plan is the single source of truth for all analytics data collected in a product. It documents every event, its properties, data types, expected values, and the team or person responsible for its implementation. Treat it as an API contract between product managers (who define what to measure), engineers (who implement the instrumentation), and data analysts (who query and interpret the data).

Un tracking plan est la source unique de vérité pour toutes les données analytics collectées. Il documente chaque événement, ses propriétés, types de données, valeurs attendues et le responsable. Le traiter comme un contrat API entre product managers, ingénieurs et analystes data.

### Structure of a Tracking Plan / Structure d'un tracking plan

Organize the tracking plan into these sections:

| Column / Colonne | Description | Example / Exemple |
|---|---|---|
| **Event Name** | Object-Action format, Title Case | `Order Completed` |
| **Category** | Functional grouping | `E-commerce`, `Onboarding` |
| **Trigger** | When exactly the event fires | "When user clicks 'Confirm Purchase' and payment succeeds" |
| **Properties** | Key-value pairs sent with the event | `order_id`, `total`, `currency` |
| **Property Type** | Data type for each property | `string`, `number`, `boolean`, `array` |
| **Required** | Whether the property is mandatory | `true` / `false` |
| **Example Value** | Sample value for documentation | `"ord_12345"`, `49.99`, `"EUR"` |
| **Owner** | Team or person responsible | `@checkout-team` |
| **Platform** | Where the event is tracked | `Web`, `iOS`, `Android`, `Server` |
| **Status** | Implementation status | `Planned`, `Implemented`, `Deprecated` |

### Design Principles / Principes de conception

1. **Start with questions, not events.** List the business questions to answer ("What is our activation rate?", "Where do users drop in the onboarding funnel?"), then derive the minimal set of events needed.

2. **Keep it lean.** 15-40 core events is sufficient for most products. Avoid tracking every micro-interaction. Each event must serve at least one defined business question.

3. **Version the plan.** Use semantic versioning (v1.2.0). Log breaking changes (renamed events, removed properties) in a changelog. Communicate changes to all stakeholders before implementation.

4. **Use a shared, editable format.** Options include: Avo (purpose-built tracking plan tool with CI integration), Amplitude Data (Amplitude's governance layer), a Google Sheet with strict access controls, or a YAML/JSON file in the Git repository.

Commencer par les questions business, pas les événements. Garder le plan lean (15-40 événements). Versionner le plan. Utiliser un format partagé et éditable (Avo, Amplitude Data, Google Sheet ou fichier Git).

### Tracking Plan Template (YAML) / Template de tracking plan

```yaml
# tracking-plan.yaml
version: "1.3.0"
last_updated: "2025-11-15"

events:
  - name: "Page Viewed"
    category: "Core"
    description: "Fired when a user views any page in the application."
    trigger: "On page load (SPA: on route change)"
    platforms: ["web", "mobile"]
    properties:
      - name: "page_name"
        type: "string"
        required: true
        description: "Human-readable name of the page"
        example: "Homepage"
      - name: "page_url"
        type: "string"
        required: true
        description: "Full URL of the page"
        example: "https://app.example.com/dashboard"
      - name: "referrer"
        type: "string"
        required: false
        description: "URL of the referring page"
        example: "https://google.com"

  - name: "Order Completed"
    category: "E-commerce"
    description: "Fired when a purchase is successfully processed."
    trigger: "Server-side, after payment confirmation from Stripe/provider"
    platforms: ["server"]
    properties:
      - name: "order_id"
        type: "string"
        required: true
        description: "Unique order identifier"
        example: "ord_abc123"
      - name: "total"
        type: "number"
        required: true
        description: "Order total in minor units (cents)"
        example: 4999
      - name: "currency"
        type: "string"
        required: true
        description: "ISO 4217 currency code"
        enum: ["EUR", "USD", "GBP"]
        example: "EUR"
      - name: "items_count"
        type: "integer"
        required: true
        description: "Number of items in the order"
        example: 3
      - name: "payment_method"
        type: "string"
        required: true
        description: "Payment method used"
        enum: ["card", "paypal", "apple_pay", "google_pay"]
        example: "card"
```

---

## Event Naming Conventions & Taxonomy

### The Object-Action Convention / La convention objet-action

Adopt the `Object Action` naming format consistently across all events. The object is the entity being acted upon; the action is the past-tense verb describing what happened. Use Title Case. This convention, popularized by Segment, provides readability, sortability, and consistency.

Adopter le format `Objet Action` de manière cohérente. L'objet est l'entité concernée, l'action est le verbe au passé décrivant ce qui s'est passé. Utiliser le Title Case. Cette convention, popularisée par Segment, garantit lisibilité, triabilité et cohérence.

**Correct examples / Exemples corrects:**

| Object / Objet | Action | Full Event / Événement complet |
|---|---|---|
| Account | Created | `Account Created` |
| Article | Viewed | `Article Viewed` |
| Cart | Updated | `Cart Updated` |
| Checkout | Started | `Checkout Started` |
| Experiment | Viewed | `Experiment Viewed` |
| Feature | Activated | `Feature Activated` |
| Invite | Sent | `Invite Sent` |
| Order | Completed | `Order Completed` |
| Search | Performed | `Search Performed` |
| Subscription | Cancelled | `Subscription Cancelled` |

**Incorrect examples / Exemples incorrects:**

| Bad Name | Problem | Corrected |
|---|---|---|
| `click_buy_button` | snake_case, imperative, too specific | `Order Started` |
| `pageview` | No object-action separation | `Page Viewed` |
| `user_signup_complete` | snake_case, redundant "user" | `Account Created` |
| `trackPurchase` | camelCase, imperative verb | `Order Completed` |
| `homepage.hero.cta.clicked` | Dotted path, too granular | `Button Clicked` (with `button_id` property) |

### Property Naming Conventions / Conventions de nommage des propriétés

Use `snake_case` for all property names. Be specific and consistent. Prefix with the object when there could be ambiguity.

```
GOOD: order_id, total_amount, currency_code, created_at, user_id
BAD:  OrderId, totalAmount, currencyCode, CreatedAt, userId
```

Utiliser `snake_case` pour toutes les propriétés. Etre spécifique et cohérent. Préfixer avec l'objet quand il y a ambiguïté.

### Reserved Properties / Propriétés réservées

Define a set of global properties (also called "super properties" or "context") that are automatically attached to every event:

| Property | Type | Description |
|---|---|---|
| `user_id` | string | Authenticated user identifier (not PII) |
| `anonymous_id` | string | Device/session identifier for unauthenticated users |
| `session_id` | string | Session identifier |
| `timestamp` | ISO 8601 | Event timestamp (client or server) |
| `platform` | string | `web`, `ios`, `android`, `server` |
| `app_version` | string | Application version |
| `locale` | string | User locale (e.g., `fr-FR`, `en-US`) |
| `environment` | string | `production`, `staging`, `development` |

### Grouping and Namespacing / Regroupement et espaces de noms

For large products with multiple domains, consider prefixing events with a namespace to avoid collisions: `Onboarding: Step Completed`, `Checkout: Payment Failed`. Alternatively, use a `category` property on every event. Do not use deep dot notation (`checkout.payment.card.declined`) as it degrades readability in analytics tools.

Pour les produits complexes, envisager un préfixe namespace (`Onboarding: Step Completed`) ou une propriété `category`. Éviter la dot notation profonde.

---

## Client-side Instrumentation

### When to Track Client-side / Quand tracker côté client

Track client-side when the event is intrinsically tied to user interface behavior that is not observable from the server:

- **Page views and navigation** (route changes in SPAs)
- **UI interactions** (clicks, scrolls, hovers, form field focus)
- **Frontend performance** (Core Web Vitals, time to interactive)
- **Session replay triggers** (rage clicks, error screens)
- **Experiment exposure** (when a variant is rendered to the user)

Tracker côté client quand l'événement est intrinsèquement lié au comportement UI non observable côté serveur : vues de pages, interactions UI, performance frontend, session replay, exposition aux expériences.

### Implementation Pattern — Web (JavaScript/TypeScript)

```typescript
// analytics.ts — Centralized analytics wrapper
import { AnalyticsBrowser } from '@segment/analytics-next';
// OR: import posthog from 'posthog-js';

const analytics = AnalyticsBrowser.load({
  writeKey: process.env.NEXT_PUBLIC_SEGMENT_WRITE_KEY!,
});

// Type-safe event tracking with the tracking plan
type TrackingEvents = {
  'Page Viewed': { page_name: string; page_url: string; referrer?: string };
  'Button Clicked': { button_id: string; button_text: string; page_name: string };
  'Feature Activated': { feature_id: string; feature_name: string };
  'Experiment Viewed': { experiment_id: string; variant_id: string };
};

export function track<E extends keyof TrackingEvents>(
  event: E,
  properties: TrackingEvents[E]
): void {
  // Check consent before firing
  if (!hasAnalyticsConsent()) {
    return;
  }
  analytics.track(event, {
    ...properties,
    timestamp: new Date().toISOString(),
    platform: 'web',
    app_version: APP_VERSION,
  });
}

export function identify(userId: string, traits: Record<string, unknown>): void {
  if (!hasAnalyticsConsent()) return;
  analytics.identify(userId, traits);
}

export function page(name: string, properties?: Record<string, unknown>): void {
  if (!hasAnalyticsConsent()) return;
  analytics.page(name, properties);
}
```

```typescript
// Usage in a React component
import { track } from '@/lib/analytics';

function CheckoutButton({ orderId }: { orderId: string }) {
  const handleClick = () => {
    track('Button Clicked', {
      button_id: 'checkout_confirm',
      button_text: 'Confirm Purchase',
      page_name: 'Checkout',
    });
    // proceed with checkout...
  };

  return <button onClick={handleClick}>Confirm Purchase</button>;
}
```

### Implementation Pattern — Mobile (React Native)

```typescript
import { createClient } from '@segment/analytics-react-native';

const segmentClient = createClient({
  writeKey: SEGMENT_WRITE_KEY,
  trackAppLifecycleEvents: true,
  collectDeviceId: false, // Privacy: do not collect device ID
});

export function trackMobile(event: string, properties: Record<string, unknown>) {
  if (!hasConsent()) return;
  segmentClient.track(event, properties);
}
```

### Pitfalls of Client-side Tracking / Pièges du tracking client-side

- **Ad blockers** block 30-40% of analytics requests on desktop web. Expect significant data loss for client-side-only tracking.
- **Consent delays**: If using a CMP, the analytics SDK must wait for consent before initializing. Implement a queue that buffers events until consent is granted, then flushes or discards.
- **SPA double-counting**: In single-page applications, ensure page view events fire on route change, not on full page load only.
- **Performance impact**: Load analytics SDKs asynchronously. Use `requestIdleCallback` or defer initialization to avoid impacting Core Web Vitals (LCP, INP).
- **Clock skew**: Client timestamps may be inaccurate. Use server-side ingestion timestamps as the canonical time when precision matters.

Les ad blockers bloquent 30-40% des requêtes analytics. Les délais de consentement nécessitent un buffer d'événements. Attention au double-comptage SPA, à l'impact performance, et au décalage d'horloge client.

---

## Server-side Instrumentation

### When to Track Server-side / Quand tracker côté serveur

Track server-side for events that represent business-critical state changes where data accuracy is non-negotiable:

- **Revenue events**: `Order Completed`, `Payment Failed`, `Refund Issued`
- **Account lifecycle**: `Account Created`, `Account Deleted`, `Subscription Started`, `Subscription Cancelled`
- **Backend actions**: `Email Sent`, `Webhook Delivered`, `Export Generated`
- **Security events**: `Login Succeeded`, `Login Failed`, `Password Changed`
- **Experiment assignment**: Server-side randomization for consistent assignment

Tracker côté serveur pour les événements business-critiques où la précision est non-négociable : revenus, cycle de vie compte, actions backend, événements sécurité, assignation d'expériences.

### Implementation Pattern — Node.js (Server-side)

```typescript
// server/analytics.ts
import Analytics from '@segment/analytics-node';
// OR: import { PostHog } from 'posthog-node';

const analytics = new Analytics({
  writeKey: process.env.SEGMENT_SERVER_WRITE_KEY!,
  flushAt: 20,      // Batch size before flush
  flushInterval: 10000, // Flush every 10 seconds
});

export function serverTrack(
  userId: string,
  event: string,
  properties: Record<string, unknown>
): void {
  analytics.track({
    userId,
    event,
    properties: {
      ...properties,
      platform: 'server',
      environment: process.env.NODE_ENV,
    },
    timestamp: new Date(),
  });
}

// Usage in an API route / webhook handler
async function handlePaymentSuccess(payment: PaymentEvent) {
  // Business logic first
  const order = await orderService.confirm(payment.orderId);

  // Then track — server-side, so no ad blocker, no consent delay
  serverTrack(order.userId, 'Order Completed', {
    order_id: order.id,
    total: order.totalCents,
    currency: order.currency,
    items_count: order.items.length,
    payment_method: payment.method,
  });
}
```

### Implementation Pattern — Python (Server-side)

```python
import analytics  # segment-analytics-python
# OR: from posthog import Posthog

analytics.write_key = os.environ["SEGMENT_SERVER_WRITE_KEY"]

def track_server(user_id: str, event: str, properties: dict) -> None:
    analytics.track(
        user_id=user_id,
        event=event,
        properties={
            **properties,
            "platform": "server",
            "environment": os.environ.get("ENV", "production"),
        },
    )

# Usage in Django/FastAPI
def complete_subscription(user_id: str, plan: Plan) -> Subscription:
    subscription = subscription_service.create(user_id, plan)

    track_server(user_id, "Subscription Started", {
        "plan_id": plan.id,
        "plan_name": plan.name,
        "billing_cycle": plan.billing_cycle,
        "mrr_cents": plan.price_cents,
    })

    return subscription
```

### Server-side Advantages / Avantages du server-side

- **100% data capture**: Not affected by ad blockers, browser extensions, or network issues.
- **Single source of truth**: Revenue events from the server match the database — no discrepancy between analytics and billing.
- **Privacy-friendly**: No client-side cookies or JavaScript execution needed. First-party by definition.
- **Consistent experiment assignment**: Assign users to variants server-side for deterministic, repeatable assignment.
- **Real-time pipeline**: Server events can feed real-time data pipelines (Kafka, Kinesis) for operational analytics.

Capture à 100% sans ad blockers. Source unique de vérité pour les revenus. Privacy-friendly sans cookies. Assignation d'expériences consistante. Pipeline temps réel possible.

---

## Hybrid Tracking Architecture

### Recommended Architecture / Architecture recommandée

```
┌─────────────────────────────────────────────────────────────┐
│                     Client (Browser/Mobile)                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Analytics SDK (Segment/PostHog/RudderStack)        │    │
│  │  → Page Viewed, Button Clicked, Feature Activated   │    │
│  │  → Consent-gated: only fires after CMP approval     │    │
│  └──────────────────────┬──────────────────────────────┘    │
└─────────────────────────┼───────────────────────────────────┘
                          │ HTTPS
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              First-party Proxy (optional)                     │
│  e.g., /api/analytics → Segment/PostHog endpoint             │
│  Avoids ad blockers, keeps data first-party                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              CDP / Analytics Backend                          │
│  (Segment, RudderStack, PostHog, Jitsu)                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐    │
│  │ Amplitude   │  │ BigQuery   │  │ Braze/Customer.io  │    │
│  │ Mixpanel    │  │ Snowflake  │  │ (activation)       │    │
│  │ PostHog     │  │ Redshift   │  │                    │    │
│  └────────────┘  └────────────┘  └────────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       ▲
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                     Server (API/Backend)                      │
│  Server-side SDK (Segment-node/PostHog-node)                │
│  → Order Completed, Subscription Started, Account Created   │
│  → No consent gating needed (first-party, no cookies)       │
└─────────────────────────────────────────────────────────────┘
```

### First-party Proxy Pattern / Pattern proxy first-party

Route client-side analytics requests through your own domain to avoid ad blockers and keep data first-party. Set up a reverse proxy at a path like `/api/t` or `/api/analytics` that forwards to Segment, PostHog, or RudderStack.

Router les requêtes analytics client-side via votre propre domaine pour éviter les ad blockers et garder les données first-party.

```typescript
// Next.js API route: /api/analytics/route.ts
export async function POST(request: Request) {
  const body = await request.json();

  // Forward to Segment/PostHog with server-side auth
  await fetch('https://api.segment.io/v1/track', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Basic ${btoa(SEGMENT_WRITE_KEY + ':')}`,
    },
    body: JSON.stringify(body),
  });

  return new Response(null, { status: 204 });
}
```

---

## SDKs & Customer Data Platforms

### Segment

The industry-standard CDP. Collect once, route to 400+ destinations. Pricing scales with Monthly Tracked Users (MTUs), which can become expensive at scale. Best for teams that need multi-tool integration without maintaining multiple SDKs.

Le CDP standard de l'industrie. Collecter une fois, router vers 400+ destinations. Tarification par MTU. Idéal pour les équipes nécessitant une intégration multi-outils.

- **Protocols**: Schema enforcement, event blocking, property validation
- **Functions**: Custom server-side transformations in JavaScript
- **Unify**: Identity resolution across devices and channels

### RudderStack (Open-source Alternative)

Open-source CDP with a Segment-compatible API. Self-hostable or cloud-managed. Warehouse-first architecture: data is always written to your warehouse. Lower cost at scale. Growing integration catalog.

CDP open-source avec API compatible Segment. Self-hostable ou cloud. Architecture warehouse-first. Coût inférieur à l'échelle.

### Jitsu (Open-source, Lightweight)

Lightweight open-source alternative for teams that need event collection and warehouse streaming without a full CDP. Simple deployment (Docker), built-in schema inference, direct warehouse connectors. Ideal for startups and small teams.

Alternative open-source légère pour la collecte d'événements et le streaming vers un warehouse. Déploiement simple, inférence de schéma intégrée. Idéal pour startups.

### PostHog (All-in-one Open-source)

PostHog combines product analytics, session replay, feature flags, A/B testing, and surveys in a single platform. Self-hostable (Docker/Kubernetes) or cloud. ClickHouse-powered for fast queries on large event volumes. The most comprehensive open-source alternative to the Amplitude + LaunchDarkly + Hotjar stack.

PostHog combine analytique produit, session replay, feature flags, A/B testing et enquêtes dans une seule plateforme. Self-hostable ou cloud. Propulsé par ClickHouse. L'alternative open-source la plus complète.

### SDK Comparison / Comparaison des SDKs

| Feature | Segment | RudderStack | Jitsu | PostHog |
|---|---|---|---|---|
| Open-source | No | Yes | Yes | Yes |
| Self-hostable | No | Yes | Yes | Yes |
| JS SDK size | ~35KB | ~40KB | ~15KB | ~45KB |
| Server-side SDKs | Node, Python, Go, Ruby, Java, PHP | Node, Python, Go, Ruby, Java | Node, Python | Node, Python, Go, Ruby, PHP |
| Warehouse-native | Via destinations | First-class | First-class | Built-in (ClickHouse) |
| Identity resolution | Yes (Unify) | Yes | Basic | Yes |
| Schema validation | Yes (Protocols) | Yes (Data Governance) | Auto-infer | Yes |

---

## Data Validation & QA

### Validation Layers / Couches de validation

Implement validation at three layers to catch tracking issues before they reach production dashboards:

1. **Development-time**: TypeScript types or Avo codegen ensure events match the tracking plan at compile time. Linters flag unknown events.

2. **Ingestion-time**: The CDP (Segment Protocols, RudderStack Data Governance) validates event schemas on ingestion. Block or quarantine non-conforming events.

3. **Pipeline-time**: dbt tests or Great Expectations validate data quality in the warehouse. Check for nulls, unexpected values, volume anomalies.

Implémenter la validation à trois niveaux : développement (types TypeScript, Avo), ingestion (Segment Protocols, RudderStack), pipeline (dbt tests, Great Expectations).

### QA Checklist / Checklist QA

Before releasing any tracking change to production, verify:

- [ ] Event name matches the tracking plan exactly (case-sensitive)
- [ ] All required properties are present and correctly typed
- [ ] Properties have valid values (enums respected, numbers in expected range)
- [ ] Event fires at the correct trigger moment (not too early, not duplicated)
- [ ] Event does not fire before consent is granted
- [ ] Server-side events include the correct `user_id`
- [ ] Events appear in the analytics tool's live debugger/event stream
- [ ] No PII (email, name, IP) is sent in event properties unless explicitly intended

### Automated Testing / Tests automatisés

```typescript
// __tests__/analytics.test.ts
import { track } from '@/lib/analytics';

describe('Analytics tracking', () => {
  it('should track Order Completed with required properties', () => {
    const spy = jest.spyOn(analytics, 'track');

    track('Order Completed', {
      order_id: 'ord_123',
      total: 4999,
      currency: 'EUR',
      items_count: 2,
      payment_method: 'card',
    });

    expect(spy).toHaveBeenCalledWith('Order Completed', expect.objectContaining({
      order_id: expect.any(String),
      total: expect.any(Number),
      currency: expect.stringMatching(/^(EUR|USD|GBP)$/),
      items_count: expect.any(Number),
      payment_method: expect.stringMatching(/^(card|paypal|apple_pay|google_pay)$/),
    }));
  });

  it('should not track when consent is not granted', () => {
    mockConsentDenied();
    const spy = jest.spyOn(analytics, 'track');

    track('Page Viewed', { page_name: 'Home', page_url: '/' });

    expect(spy).not.toHaveBeenCalled();
  });
});
```

---

## Schema Validation & Tracking as Code

### JSON Schema for Event Validation / JSON Schema pour validation d'événements

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Order Completed",
  "type": "object",
  "required": ["order_id", "total", "currency", "items_count", "payment_method"],
  "properties": {
    "order_id": {
      "type": "string",
      "pattern": "^ord_[a-zA-Z0-9]+$",
      "description": "Unique order identifier"
    },
    "total": {
      "type": "integer",
      "minimum": 0,
      "description": "Total in minor units (cents)"
    },
    "currency": {
      "type": "string",
      "enum": ["EUR", "USD", "GBP"]
    },
    "items_count": {
      "type": "integer",
      "minimum": 1
    },
    "payment_method": {
      "type": "string",
      "enum": ["card", "paypal", "apple_pay", "google_pay"]
    }
  },
  "additionalProperties": false
}
```

### Avo — Tracking Plan as Code

Avo is a purpose-built platform that turns the tracking plan into a type-safe, auto-generated SDK. Define events in the Avo web interface or CLI, then generate TypeScript/Swift/Kotlin functions that enforce correct usage at compile time. Integrate Avo's CI check into pull requests to block merges that violate the tracking plan.

Avo est une plateforme dédiée qui transforme le tracking plan en SDK type-safe auto-généré. Définir les événements dans l'interface Avo, puis générer des fonctions TypeScript/Swift/Kotlin. Intégrer le check CI d'Avo dans les pull requests.

### CI Pipeline Integration / Intégration pipeline CI

```yaml
# .github/workflows/tracking-validation.yml
name: Tracking Plan Validation
on: [pull_request]

jobs:
  validate-tracking:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate event schemas
        run: |
          npx ajv validate -s tracking-plan/schemas/*.json -d tracking-plan/examples/*.json
      - name: Avo pull request check (if using Avo)
        run: npx avo pull --branch ${{ github.head_ref }}
      - name: Check for tracking plan coverage
        run: |
          # Ensure every tracked event in code exists in the tracking plan
          node scripts/check-tracking-coverage.js
```

---

## Tracking Governance

### Governance Model / Modèle de gouvernance

Establish a tracking governance process to prevent tracking plan drift, data quality degradation, and analytics distrust:

1. **Tracking Plan Owner**: Assign a single owner (typically a data/analytics lead) who approves all additions and changes to the tracking plan.

2. **Change Request Process**: Require a lightweight RFC for new events or property changes. Include: business question served, event name, properties, expected volume, and implementation platform.

3. **PR Review Gate**: No tracking code ships without a review from the tracking plan owner or a designated analytics engineer.

4. **Quarterly Audit**: Review all tracked events quarterly. Deprecate events that are no longer queried. Identify gaps in coverage. Clean up stale properties.

5. **Data Quality Alerts**: Set up automated alerts for tracking anomalies: sudden volume drops (broken tracking), unexpected null rates, new unknown events.

Établir un processus de gouvernance : propriétaire du tracking plan, processus de changement (RFC léger), gate de review PR, audit trimestriel, alertes qualité de données.

### Deprecation Process / Processus de dépréciation

When deprecating an event:

1. Mark the event as `deprecated` in the tracking plan with a target removal date.
2. Add a deprecation warning in the tracking SDK wrapper (log a warning when the deprecated event is called).
3. Verify no active dashboards, alerts, or queries depend on the event.
4. Remove the event from the SDK and tracking plan after the grace period.
5. Optionally keep the event in the warehouse for historical analysis.

Quand un événement est déprécié : le marquer dans le plan, ajouter un warning dans le SDK, vérifier qu'aucun dashboard ne dépend de l'événement, le retirer après la période de grâce, conserver dans le warehouse pour l'historique.

### Ownership Matrix / Matrice de responsabilité

| Role | Responsibility |
|---|---|
| **Product Manager** | Defines business questions, requests new events, validates event triggers |
| **Analytics Engineer** | Owns tracking plan, reviews schemas, monitors data quality |
| **Frontend Engineer** | Implements client-side tracking, ensures consent gating |
| **Backend Engineer** | Implements server-side tracking, ensures accurate business events |
| **Data Analyst** | Consumes events, reports tracking gaps, validates data accuracy |
| **Privacy/Legal** | Reviews PII exposure, validates consent implementation |
