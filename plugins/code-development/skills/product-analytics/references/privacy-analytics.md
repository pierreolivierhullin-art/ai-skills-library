# Privacy & Analytics / Vie Privée & Analytics

Référence approfondie sur la gestion du consentement (CMP), le tracking server-side pour la vie privée, l'anonymisation et la pseudonymisation, le tracking sans cookies, l'analytique conforme RGPD (exemption CNIL first-party), et les alternatives à GA4.

Deep-dive reference on consent management (CMP), server-side tracking for privacy, anonymization & pseudonymization, cookie-less tracking, RGPD/GDPR-compliant analytics (CNIL first-party exemption), and GA4 alternatives.

---

## Table of Contents

1. [RGPD/GDPR Framework for Analytics](#rgpdgdpr-framework-for-analytics)
2. [Consent Management Platforms (CMP)](#consent-management-platforms-cmp)
3. [Implementation of Consent-gated Tracking](#implementation-of-consent-gated-tracking)
4. [Server-side Tracking for Privacy](#server-side-tracking-for-privacy)
5. [Anonymization & Pseudonymization](#anonymization--pseudonymization)
6. [Cookie-less Tracking Approaches](#cookie-less-tracking-approaches)
7. [CNIL Exemption for First-party Analytics](#cnil-exemption-for-first-party-analytics)
8. [GA4 Alternatives — Privacy-first Analytics](#ga4-alternatives--privacy-first-analytics)
9. [Data Retention & Deletion](#data-retention--deletion)
10. [Privacy-by-Design Architecture](#privacy-by-design-architecture)

---

## RGPD/GDPR Framework for Analytics

### Key Principles / Principes clés

The RGPD (Règlement Général sur la Protection des Données) / GDPR imposes strict rules on processing personal data, which includes most analytics data. Understand these core principles for analytics:

Le RGPD impose des règles strictes sur le traitement des données personnelles, ce qui inclut la plupart des données analytics. Principes fondamentaux :

1. **Lawfulness (Licéité)**: Analytics processing requires a legal basis. For most analytics, this is either **consent** (Article 6.1.a) or **legitimate interest** (Article 6.1.f). In practice, EU regulators (especially CNIL, AEPD, BfDI) have ruled that analytics cookies require explicit opt-in consent, not just legitimate interest.

2. **Purpose limitation (Limitation des finalités)**: Collect data only for specified, explicit, and legitimate purposes. "Analytics" is a valid purpose, but it must be declared in the privacy policy.

3. **Data minimization (Minimisation des données)**: Collect only the data strictly necessary for the declared analytics purpose. Do not collect full IP addresses, precise geolocation, or device fingerprints unless specifically justified.

4. **Storage limitation (Limitation de conservation)**: Define and enforce a maximum retention period. CNIL recommends a maximum of 25 months for analytics cookies and 13 months for the consent cookie itself.

5. **Integrity and confidentiality (Intégrité et confidentialité)**: Protect analytics data with appropriate security measures. Encrypt in transit (HTTPS) and at rest.

Licéité (consentement ou intérêt légitime), limitation des finalités, minimisation des données, limitation de conservation (25 mois max recommandé par la CNIL), intégrité et confidentialité.

### What Constitutes Personal Data in Analytics / Ce qui constitue des données personnelles en analytics

| Data Point | Personal Data? | Notes |
|---|---|---|
| Full IP address | Yes | Can identify an individual, especially with ISP data |
| Truncated IP (last octet zeroed) | Debatable | CNIL considers it pseudonymized, not anonymous |
| Cookie ID / Device ID | Yes | Unique identifiers are personal data under RGPD |
| User ID (internal) | Yes | Indirectly identifies a person |
| User Agent string | Potentially | Combined with other data, can create a fingerprint |
| Page URL with PII in query params | Yes | e.g., `?email=user@example.com` |
| Aggregate statistics (no user-level) | No | True aggregation without re-identification risk is not personal data |

### Legal Basis Decision Tree / Arbre de décision base légale

```
Is the analytics tool strictly first-party and configured for
CNIL-exempt purpose (audience measurement only)?
├── YES → No consent required (CNIL exemption, see below)
│         Tools: Matomo (exempt config), AT Internet/Piano Analytics,
│         Plausible*, Fathom*
│         (*if configured without cross-site tracking)
│
└── NO → Consent required (opt-in before any tracking fires)
          ├── Third-party cookies? → Consent required (always)
          ├── Cross-site tracking? → Consent required (always)
          ├── Google Analytics (GA4)? → Consent required
          │   (data transfer to US, cross-site, third-party context)
          ├── Amplitude, Mixpanel, PostHog Cloud? → Consent required
          │   (user-level tracking, potential cross-site)
          └── Self-hosted PostHog, Matomo (standard)? → Consent required
              (user-level tracking, but can argue legitimate interest
               if strictly first-party and anonymized — risky, prefer consent)
```

---

## Consent Management Platforms (CMP)

### Overview / Vue d'ensemble

A Consent Management Platform (CMP) collects, stores, and enforces user consent choices for cookies and tracking technologies. In the EU, a CMP is required for any non-exempt analytics. The CMP must comply with the IAB Transparency & Consent Framework (TCF) v2.2 for advertising, and with CNIL/RGPD requirements for analytics.

Un CMP collecte, stocke et applique les choix de consentement des utilisateurs. Requis en UE pour tout analytics non-exempté. Doit être conforme au TCF v2.2 de l'IAB et aux exigences CNIL/RGPD.

### CMP Comparison / Comparaison des CMP

| CMP | Origin | Pricing | Strengths | Best For |
|---|---|---|---|---|
| **Didomi** | France | From free to enterprise | TCF v2.2, CNIL-recommended, API-first, multi-regulation (RGPD, CCPA, LGPD) | European companies, multi-market compliance |
| **Axeptio** | France | From free tier | Beautiful UX, gamified consent, high acceptance rates, CNIL-compliant | French companies wanting high opt-in rates |
| **OneTrust** | US (global) | Enterprise pricing | Comprehensive privacy management (consent + DSAR + privacy impact), TCF v2.2 | Large enterprises, multi-regulation |
| **Cookiebot (Usercentrics)** | Denmark/Germany | From free tier | Automatic cookie scanning, TCF v2.2, easy setup | SMBs, quick compliance |
| **TarteAuCitron** | France | Open-source (free) | Lightweight, open-source, CNIL-recommended | Developers, budget-conscious |
| **Osano** | US | From free tier | Simple UI, automatic blocking, compliance monitoring | US/EU companies |
| **Consentmanager** | Germany | From free tier | TCF v2.2, fast loading, multi-language | European publishers |

### CNIL Requirements for CMP / Exigences CNIL pour les CMP

The CNIL requires that consent banners:

1. **Offer equal choices**: The "Accept" and "Refuse" buttons must be equally prominent (same size, same position, same visual weight). No dark patterns.
2. **Be specific**: List the purposes (analytics, advertising, social media) and allow granular consent per purpose.
3. **Not use pre-checked boxes**: All checkboxes must be unchecked by default.
4. **Allow easy withdrawal**: Users must be able to withdraw consent as easily as they gave it (persistent widget or settings page).
5. **Not use cookie walls**: Blocking access to the site until consent is given is prohibited (with limited exceptions for paid alternatives).
6. **Store consent proof**: Keep a record of when and how consent was obtained, for audit purposes.
7. **Renew consent**: Ask for consent renewal at most every 13 months.

La CNIL exige : choix égaux (Accept/Refuse même importance), consentement spécifique par finalité, pas de cases pré-cochées, retrait facile, pas de cookie wall, preuve de consentement, renouvellement tous les 13 mois max.

---

## Implementation of Consent-gated Tracking

### Architecture Pattern / Pattern d'architecture

```
┌──────────────────────────────────────────────────────────────┐
│                         User visits page                      │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    CMP Banner displayed                        │
│                    (no tracking fires yet)                     │
└───────────┬──────────────────────────────────┬───────────────┘
            │                                  │
     User accepts                       User refuses
            │                                  │
            ▼                                  ▼
┌───────────────────────┐      ┌───────────────────────────────┐
│ Initialize analytics  │      │ Do NOT initialize analytics   │
│ SDK (Segment/PostHog) │      │ Only exempt tools fire        │
│ Flush buffered events │      │ (e.g., CNIL-exempt Matomo)    │
│ Set consent cookie    │      │ Set refusal cookie            │
└───────────────────────┘      └───────────────────────────────┘
```

### Implementation — Didomi + Segment / Implémentation Didomi + Segment

```typescript
// consent-manager.ts
import { AnalyticsBrowser } from '@segment/analytics-next';

let analyticsInstance: AnalyticsBrowser | null = null;
const eventBuffer: Array<{ method: string; args: any[] }> = [];

// Initialize Didomi
window.didomiConfig = {
  app: { apiKey: 'YOUR_DIDOMI_API_KEY' },
  notice: {
    position: 'bottom',
    // Equal-weight buttons as required by CNIL
    denyButton: { enabled: true },
    learnMoreButton: { enabled: true },
  },
};

// Buffer events before consent
export function track(event: string, properties: Record<string, unknown>): void {
  if (analyticsInstance) {
    analyticsInstance.track(event, properties);
  } else {
    eventBuffer.push({ method: 'track', args: [event, properties] });
  }
}

// Listen for Didomi consent events
window.didomiOnReady = window.didomiOnReady || [];
window.didomiOnReady.push(function (Didomi: any) {
  // Check if user has already consented (returning visitor)
  if (Didomi.getUserConsentStatusForPurpose('analytics')) {
    initializeAnalytics();
  }

  // Listen for consent changes
  Didomi.on('consent.changed', function () {
    if (Didomi.getUserConsentStatusForPurpose('analytics')) {
      initializeAnalytics();
    } else {
      teardownAnalytics();
    }
  });
});

function initializeAnalytics(): void {
  if (analyticsInstance) return; // Already initialized

  analyticsInstance = AnalyticsBrowser.load({
    writeKey: process.env.NEXT_PUBLIC_SEGMENT_WRITE_KEY!,
  });

  // Flush buffered events
  for (const { method, args } of eventBuffer) {
    (analyticsInstance as any)[method](...args);
  }
  eventBuffer.length = 0;
}

function teardownAnalytics(): void {
  // If user withdraws consent, stop tracking and clear local data
  if (analyticsInstance) {
    analyticsInstance.reset(); // Clear anonymous ID and traits
    analyticsInstance = null;
  }
  eventBuffer.length = 0;
}
```

### Implementation — Axeptio + PostHog / Implémentation Axeptio + PostHog

```typescript
// consent-axeptio-posthog.ts
import posthog from 'posthog-js';

let posthogInitialized = false;

// Axeptio callback when consent choices are made
window._axcb = window._axcb || [];
window._axcb.push(function (axeptio: any) {
  axeptio.on('cookies:complete', function (choices: Record<string, boolean>) {
    if (choices.analytics) {
      initPostHog();
    } else {
      stopPostHog();
    }
  });
});

function initPostHog(): void {
  if (posthogInitialized) return;

  posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
    api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://eu.posthog.com',
    persistence: 'localStorage+cookie',
    capture_pageview: true,
    autocapture: true,
    // Privacy settings
    ip: false,                    // Do not capture IP address
    mask_all_text: false,         // Session replay text masking
    mask_all_element_attributes: false,
  });
  posthogInitialized = true;
}

function stopPostHog(): void {
  if (posthogInitialized) {
    posthog.opt_out_capturing();
    posthog.reset();
    posthogInitialized = false;
  }
}
```

### Server-side Consent Checking / Vérification du consentement côté serveur

For server-side tracking, verify consent status before sending events:

```typescript
// server/analytics-with-consent.ts
import { PostHog } from 'posthog-node';

const posthog = new PostHog(process.env.POSTHOG_API_KEY!, {
  host: 'https://eu.posthog.com',
});

interface ConsentStatus {
  analytics: boolean;
  advertising: boolean;
  updated_at: string;
}

async function getConsentStatus(userId: string): Promise<ConsentStatus> {
  // Query your consent database / CMP API
  const consent = await db.consents.findByUserId(userId);
  return consent ?? { analytics: false, advertising: false, updated_at: '' };
}

export async function trackWithConsent(
  userId: string,
  event: string,
  properties: Record<string, unknown>
): Promise<void> {
  const consent = await getConsentStatus(userId);

  if (!consent.analytics) {
    // User has not consented to analytics — do not track
    return;
  }

  posthog.capture({
    distinctId: userId,
    event,
    properties: {
      ...properties,
      consent_status: 'granted',
      consent_updated_at: consent.updated_at,
    },
  });
}
```

Pour le tracking server-side, vérifier le statut de consentement avant d'envoyer les événements. Interroger la base de consentement ou l'API du CMP.

---

## Server-side Tracking for Privacy

### Why Server-side Tracking Is Privacy-friendly / Pourquoi le tracking server-side est privacy-friendly

Server-side tracking offers significant privacy advantages over client-side tracking:

1. **No third-party cookies**: Events are sent from your server to the analytics provider's API. No cookies are set in the user's browser by third-party domains.

2. **First-party by definition**: Data flows from your server (first party) to the analytics backend. No browser-side scripts from third-party analytics vendors.

3. **Ad blocker immune**: Server-to-server API calls cannot be blocked by browser extensions or ad blockers.

4. **Data control**: You control exactly what data is sent. You can strip PII (email, IP, name) before forwarding to analytics.

5. **Reduced attack surface**: No client-side JavaScript that could be tampered with, injected, or intercepted.

Le tracking server-side n'utilise pas de cookies tiers, est first-party par définition, résiste aux ad blockers, permet le contrôle des données (suppression de PII avant envoi), et réduit la surface d'attaque.

### Server-side Tracking Architecture / Architecture de tracking server-side

```
┌──────────────────────────────────────────────────────────────┐
│  Client (Browser)                                             │
│  → Sends actions to YOUR API (e.g., POST /api/checkout)      │
│  → No analytics SDK loaded (or minimal first-party only)     │
└──────────────────────────────┬───────────────────────────────┘
                               │ HTTPS (first-party)
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  Your Server / API                                            │
│  1. Process business logic                                    │
│  2. Strip PII (email, IP, full name)                         │
│  3. Send sanitized event to analytics                         │
│     via server-side SDK (Segment-node, PostHog-node)         │
└──────────────────────────────┬───────────────────────────────┘
                               │ Server-to-server API call
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  Analytics Backend (PostHog, Amplitude, Segment)              │
│  → Receives sanitized, first-party data                       │
│  → No direct user browser access                              │
└──────────────────────────────────────────────────────────────┘
```

### Google Tag Manager Server-side (sGTM) / GTM Server-side

Google Tag Manager Server-side (sGTM) runs a Tag Manager container on your own server (Cloud Run, App Engine). Client-side hits are sent to your first-party domain, then the server container routes data to Google Analytics, Facebook, and other providers. This provides:

- **First-party context**: Cookies are set by your domain, not google.com.
- **Data filtering**: Strip or redact data before forwarding to third parties.
- **Ad blocker resistance**: Client hits go to your domain, not blocked third-party endpoints.

**Caution / Attention**: sGTM does not exempt you from consent requirements. If the data is ultimately forwarded to Google or Facebook, consent is still needed under RGPD.

GTM Server-side fournit un contexte first-party et le filtrage des données, mais ne vous exempte pas du consentement si les données sont envoyées à Google ou Facebook.

---

## Anonymization & Pseudonymization

### Definitions / Définitions

- **Anonymization (Anonymisation)**: Irreversible transformation of personal data so that the individual can never be re-identified, even by the data controller. Truly anonymous data is not subject to RGPD. However, true anonymization is extremely difficult to achieve — most techniques that claim anonymization are actually pseudonymization.

- **Pseudonymization (Pseudonymisation)**: Replacing direct identifiers with artificial identifiers (pseudonyms) while keeping the mapping in a separate, secured system. Pseudonymized data is still personal data under RGPD, but benefits from reduced risk and is encouraged by the regulation.

Anonymisation : transformation irréversible, l'individu ne peut jamais être ré-identifié. Données anonymes hors champ RGPD. Pseudonymisation : remplacement des identifiants directs par des pseudonymes, le mapping est conservé séparément. Données pseudonymisées restent des données personnelles.

### Techniques for Analytics / Techniques pour l'analytics

| Technique | Type | Description | Example |
|---|---|---|---|
| **IP truncation** | Pseudonymization | Zero the last octet of IPv4 (or last 80 bits of IPv6) | `192.168.1.123` → `192.168.1.0` |
| **Hashing user IDs** | Pseudonymization | SHA-256 hash of user identifier | `user_42` → `a1b2c3d4...` |
| **Salted hashing** | Stronger pseudo. | Hash with a secret salt, rotated periodically | `SHA256(salt + user_42)` |
| **k-anonymity** | Anonymization | Ensure each record is indistinguishable from k-1 others | Group by age range + city instead of exact age + address |
| **Differential privacy** | Anonymization | Add calibrated noise to aggregates | True count = 1,247, reported = 1,247 + noise(epsilon) |
| **Aggregation** | Anonymization | Report only aggregates, never user-level data | "500 users visited page X" instead of individual events |
| **Data suppression** | Anonymization | Remove small groups (< k users) from reports | Do not report cohorts with < 5 users |

### Implementation — PII Stripping Middleware / Middleware de suppression de PII

```typescript
// middleware/strip-pii.ts
interface AnalyticsEvent {
  userId: string;
  event: string;
  properties: Record<string, unknown>;
  context?: Record<string, unknown>;
}

function stripPII(event: AnalyticsEvent): AnalyticsEvent {
  const sanitized = { ...event };

  // Hash user ID for pseudonymization
  sanitized.userId = hashUserId(event.userId);

  // Remove PII from properties
  const piiFields = ['email', 'name', 'first_name', 'last_name', 'phone', 'address', 'ip'];
  for (const field of piiFields) {
    delete sanitized.properties[field];
  }

  // Truncate IP in context
  if (sanitized.context?.ip) {
    sanitized.context.ip = truncateIP(sanitized.context.ip as string);
  }

  // Remove URLs with PII in query params
  if (typeof sanitized.properties.page_url === 'string') {
    sanitized.properties.page_url = stripQueryPII(sanitized.properties.page_url);
  }

  return sanitized;
}

function hashUserId(userId: string): string {
  const crypto = require('crypto');
  const salt = process.env.ANALYTICS_HASH_SALT!;
  return crypto.createHash('sha256').update(salt + userId).digest('hex').substring(0, 16);
}

function truncateIP(ip: string): string {
  // IPv4: zero last octet
  if (ip.includes('.')) {
    const parts = ip.split('.');
    parts[3] = '0';
    return parts.join('.');
  }
  // IPv6: zero last 5 groups
  const parts = ip.split(':');
  return parts.slice(0, 3).join(':') + ':0:0:0:0:0';
}

function stripQueryPII(url: string): string {
  try {
    const parsed = new URL(url);
    const piiParams = ['email', 'token', 'password', 'secret', 'key'];
    for (const param of piiParams) {
      parsed.searchParams.delete(param);
    }
    return parsed.toString();
  } catch {
    return url;
  }
}
```

---

## Cookie-less Tracking Approaches

### Why Cookie-less / Pourquoi sans cookies

The cookie-less movement is driven by three forces:

1. **Regulatory pressure**: RGPD/ePrivacy require consent for non-essential cookies. Consent rates in France average 55-65%, meaning 35-45% of traffic is untracked.
2. **Browser restrictions**: Safari ITP (Intelligent Tracking Prevention) limits first-party cookies to 7 days, third-party cookies are fully blocked. Firefox ETP blocks third-party cookies. Chrome has announced (and delayed, then partially implemented) the deprecation of third-party cookies.
3. **User expectations**: Privacy-conscious users increasingly use ad blockers (30-40% on desktop) and expect privacy by default.

Pression réglementaire (55-65% de taux de consentement en France), restrictions navigateurs (Safari ITP, Firefox ETP, Chrome), attentes utilisateurs (30-40% d'ad blockers).

### Cookie-less Approaches / Approches sans cookies

| Approach | How It Works | Privacy Level | Analytics Quality |
|---|---|---|---|
| **Aggregate-only analytics** | Count page views, sessions, and referrers without any user-level identification | Very high | Basic (no funnels, no retention, no user paths) |
| **Fingerprint-free session detection** | Use server-side session tokens (short-lived, per-visit) | High | Medium (per-session analysis, no cross-session) |
| **First-party, short-lived cookies** | First-party cookie with 24h-7d expiry, no cross-site | Medium-high | Good (multi-page sessions, limited retention) |
| **Server-side session stitching** | Stitch sessions server-side using authenticated user ID | Medium | Full (for logged-in users only) |
| **Privacy sandbox (Chrome Topics API)** | Browser-provided interest categories, no individual tracking | Medium | Low (coarse-grained, advertising-focused) |

### Implementation — Cookie-less Aggregate Analytics

```typescript
// Minimal cookie-less page analytics (no user identification)
// Sends aggregate page view data to your own endpoint

async function trackPageView(): Promise<void> {
  const data = {
    url: window.location.pathname, // No query params (may contain PII)
    referrer: document.referrer ? new URL(document.referrer).hostname : null,
    viewport: `${window.innerWidth}x${window.innerHeight}`,
    locale: navigator.language,
    timestamp: new Date().toISOString(),
    // NO: user ID, device ID, cookie ID, IP, user agent
  };

  // Send to your own first-party endpoint
  navigator.sendBeacon('/api/pageview', JSON.stringify(data));
}

// Fire on page load (no consent needed — no personal data collected)
trackPageView();
```

---

## CNIL Exemption for First-party Analytics

### What Is the CNIL Exemption / Qu'est-ce que l'exemption CNIL

The CNIL (French data protection authority) provides an exemption from cookie consent requirements for analytics tools that are configured to be strictly limited to audience measurement. This means certain analytics tools can track visitors without a consent banner, as long as they meet specific conditions.

La CNIL accorde une exemption de consentement pour les outils analytics configurés de manière strictement limitée à la mesure d'audience. Certains outils peuvent tracker sans bandeau de consentement.

### Exemption Conditions / Conditions d'exemption

To qualify for the CNIL exemption, the analytics tool must:

1. **Serve only audience measurement**: The data must be used exclusively to produce anonymous statistics. It must not be used for profiling, cross-site tracking, data enrichment, or targeted advertising.

2. **Be first-party only**: No data sharing with third parties. The analytics provider must not use the data for their own purposes.

3. **Limited scope of data**: Collect only data necessary for audience measurement (page views, referrers, basic device info). No precise geolocation, no detailed device fingerprinting.

4. **IP anonymization**: IP addresses must be anonymized (truncated) before storage.

5. **Limited cookie lifetime**: Cookies used for visitor recognition must not exceed 13 months. The collected data must not be retained for more than 25 months.

6. **No cross-site tracking**: The tool must not track users across different websites or services.

7. **Users must be informed**: Even though consent is not required, users must still be informed that analytics are used (in the privacy policy). An opt-out mechanism should be provided.

Conditions : mesure d'audience uniquement, first-party uniquement, données limitées, IP anonymisé, cookies max 13 mois, conservation max 25 mois, pas de tracking cross-site, information de l'utilisateur.

### CNIL-exempt Tools / Outils exemptés CNIL

The CNIL maintains a list of tools that can be configured for exemption:

| Tool | Configuration for Exemption | Notes |
|---|---|---|
| **Matomo** (self-hosted) | Disable cross-site tracking, enable IP anonymization, set cookie lifetime to 13 months, disable user-id tracking | Most popular exempt option |
| **AT Internet / Piano Analytics** | Use "exempt" configuration, first-party cookies only | French company, widely used in France |
| **Plausible** | Default configuration is already privacy-first (no cookies, no personal data) | Qualifies for exemption if self-hosted or EU cloud |
| **Fathom** | No cookies mode, EU-isolated data | Check current CNIL guidance for official status |
| **Abla Analytics** | Designed for CNIL exemption by default | French company |
| **Beyondanalytics** | CNIL-exempt by design | French company |

**Important / Important**: Google Analytics (GA4) does NOT qualify for the CNIL exemption. GA4 transfers data to the US (Schrems II concerns), uses cross-site tracking capabilities, and Google may use the data for its own purposes. The CNIL has explicitly ruled that GA4 is not exempt.

Google Analytics (GA4) ne qualifie PAS pour l'exemption CNIL. Le CNIL a explicitement statué que GA4 n'est pas exempté (transfert de données US, tracking cross-site, utilisation par Google).

### Matomo Exempt Configuration / Configuration Matomo exemptée

```php
// Matomo configuration for CNIL exemption
// In Matomo admin panel or config.ini.php:

// 1. Anonymize IP addresses (at least 2 bytes for IPv4)
[Tracker]
trust_visitors_cookies = 0

// 2. Set cookie lifetime to max 13 months (396 days)
[Tracker]
cookie_expire = 34214400  ; 396 days in seconds

// 3. Disable User ID tracking
// Do NOT use setUserId() in the tracking code

// 4. Disable cross-domain tracking
// Do NOT use setCookieDomain() with a wildcard

// 5. Respect Do-Not-Track header
[PrivacyManager]
doNotTrackEnabled = 1

// 6. Configure data retention to max 25 months
// Admin > Privacy > Data Retention > Delete old raw data after 25 months
```

```html
<!-- Matomo tracking code for CNIL-exempt configuration -->
<script>
  var _paq = window._paq = window._paq || [];
  // NO cookies for cross-site; first-party only
  _paq.push(['disableCookies']); // OR use the limited cookie config above
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="https://matomo.yourdomain.com/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '1']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
```

---

## GA4 Alternatives — Privacy-first Analytics

### Why Replace GA4 / Pourquoi remplacer GA4

Multiple factors drive the move away from Google Analytics 4:

1. **RGPD compliance risk**: CNIL, Austrian DSB, and Italian Garante have all ruled that GA (Universal/GA4) violates RGPD due to data transfers to the US and Google's data processing. The EU-US Data Privacy Framework (2023) provides some relief, but its long-term stability is uncertain.

2. **Consent dependency**: GA4 requires explicit opt-in consent in the EU. With consent rates of 55-65%, you lose 35-45% of traffic data.

3. **Data ownership**: GA4 data lives in Google's infrastructure. Export is limited (BigQuery Linking helps but adds cost and complexity).

4. **Sampling**: GA4 samples data for large datasets, introducing inaccuracy in high-volume sites.

5. **Complexity**: GA4's event-based model is powerful but significantly more complex than Universal Analytics for basic reporting.

Risque RGPD (décisions CNIL, DSB, Garante), dépendance au consentement (35-45% de données perdues), propriété des données, échantillonnage, complexité.

### Alternative Comparison / Comparaison des alternatives

| Tool | Type | Hosting | Cookies | CNIL Exempt | Pricing | Best For |
|---|---|---|---|---|---|---|
| **PostHog** | Product analytics + more | Cloud (EU) or self-hosted | Optional | No (user-level tracking) | Free tier, then usage-based | Full product analytics suite |
| **Plausible** | Web analytics | Cloud (EU) or self-hosted | No cookies | Yes (by design) | From $9/mo | Simple, privacy-first web analytics |
| **Fathom** | Web analytics | Cloud (EU data) | No cookies | Check guidance | From $14/mo | Simple analytics, premium support |
| **Matomo** | Web analytics + product | Self-hosted or cloud | Configurable | Yes (exempt config) | Free (self-hosted), from $19/mo (cloud) | Full GA4 replacement, CNIL exempt |
| **Umami** | Web analytics | Self-hosted | No cookies | Yes (by design) | Free (self-hosted) | Developers, open-source, minimal |
| **Pirsch** | Web analytics | Cloud (Germany) | No cookies | Check guidance | From $4/mo | Simple, German-hosted |
| **Piwik PRO** | Analytics suite | Cloud (EU) or on-premises | Configurable | Configurable | Free tier, enterprise | Enterprise GA4 replacement in EU |
| **Piano Analytics** (AT Internet) | Analytics suite | Cloud (France) | Configurable | Yes (exempt config) | Enterprise | French enterprises, publishing |

### Migration Strategy GA4 to Privacy-first / Stratégie de migration GA4 vers privacy-first

1. **Assess requirements**: List the GA4 reports and features currently used. Distinguish between "nice to have" and "must have."
2. **Choose replacement(s)**: Often a dual approach works: Plausible/Fathom for CNIL-exempt web analytics (all visitors, no consent needed) + PostHog/Amplitude for deep product analytics (consented users only).
3. **Run in parallel**: Deploy the new tool alongside GA4 for 2-4 weeks. Compare data to identify gaps.
4. **Migrate dashboards**: Rebuild critical dashboards in the new tool. Accept that some GA4-specific features (audience building for Google Ads) may require different approaches.
5. **Remove GA4**: Once validated, remove GA4 scripts. Update the consent banner if analytics consent is no longer needed for the exempt tool.
6. **Update privacy policy**: Reflect the new analytics setup in the privacy policy and cookie policy.

Stratégie : évaluer les besoins, choisir les remplacements (souvent double approche), faire tourner en parallèle, migrer les dashboards, retirer GA4, mettre à jour la politique de confidentialité.

---

## Data Retention & Deletion

### Retention Policies / Politiques de conservation

| Data Category | CNIL Recommendation | Implementation |
|---|---|---|
| **Consent cookie** | 13 months maximum | Set `max-age` or `expires` on the consent cookie |
| **Analytics cookies** | 13 months maximum | Configure in analytics tool settings |
| **Raw event data** | 25 months maximum | Set TTL in warehouse/analytics tool, automate deletion |
| **Aggregated reports** | No limit (anonymous) | Keep indefinitely if truly aggregated |
| **User profiles** | 25 months from last activity | Automated cleanup job |

### Right to Erasure (DSAR) / Droit à l'effacement

Under RGPD Article 17, users can request deletion of their personal data. For analytics:

1. Implement a mechanism to delete all analytics data for a given user ID.
2. If using Segment, use the Segment Deletion API.
3. If using PostHog, use the person deletion API or admin interface.
4. Delete data in the warehouse: run a targeted DELETE on all tables containing the user ID.
5. Note: Truly anonymized/aggregated data does not need to be deleted (it is not personal data).

Implémenter un mécanisme de suppression de toutes les données analytics pour un user ID donné. Les données véritablement anonymisées n'ont pas besoin d'être supprimées.

---

## Privacy-by-Design Architecture

### Architecture Decision Record / Décision d'architecture

When designing a privacy-first analytics architecture, follow this decision framework:

```
1. Do we need user-level analytics (funnels, retention, cohorts)?
   ├── NO → Use cookie-less, aggregate-only tool (Plausible, Fathom, Umami)
   │        → No consent needed (CNIL exempt)
   │        → Deploy and done
   │
   └── YES → Continue to step 2

2. Can we limit user-level tracking to authenticated (logged-in) users?
   ├── YES → Use server-side tracking only (no client-side cookies)
   │        → Track via backend API calls (Segment-node, PostHog-node)
   │        → User ID = internal identifier (hashed)
   │        → Still need consent (user-level data is personal data)
   │        → But higher consent rates (logged-in users are more engaged)
   │
   └── NO → Need to track anonymous visitors too → Continue to step 3

3. Implement full consent-gated tracking
   → Deploy CMP (Didomi, Axeptio)
   → Initialize analytics SDK only after consent
   → Accept 35-45% data loss from non-consenting visitors
   → Complement with CNIL-exempt tool for 100% aggregate data
   → Use server-side tracking for critical business events
```

### Recommended Dual-stack Architecture / Architecture double-stack recommandée

For European products, the recommended approach is a dual-stack:

| Layer | Tool | Consent Required | Coverage | Use For |
|---|---|---|---|---|
| **Layer 1: Aggregate** | Plausible or Matomo (exempt config) | No (CNIL exempt) | 100% of visitors | Traffic, referrers, top pages, trends |
| **Layer 2: Product** | PostHog or Amplitude (consent-gated) | Yes (opt-in) | 55-65% of visitors | Funnels, retention, cohorts, experiments |

This dual-stack ensures you always have 100% traffic visibility (Layer 1) while still enabling deep product analytics for consented users (Layer 2).

Pour les produits européens, l'approche recommandée est un double-stack : couche agrégée (Plausible/Matomo exempt, 100% des visiteurs, sans consentement) + couche produit (PostHog/Amplitude, 55-65% des visiteurs, avec consentement). Cela garantit une visibilité trafic complète tout en permettant l'analytique produit approfondie.
