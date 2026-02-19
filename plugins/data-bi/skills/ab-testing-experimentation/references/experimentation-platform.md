# Plateforme d'Experimentation — Architecture et Feature Flags

## Introduction

**FR** — Ce guide couvre l'architecture complete d'une plateforme d'experimentation industrielle : du service d'assignation au pipeline d'analyse, en passant par les patterns de feature flags et l'instrumentation requise. Une plateforme robuste permet de lancer des dizaines de tests en parallele sans interference, avec une analyse fiable et une detection automatique des anomalies d'assignation. Le guide inclut des comparaisons detaillees des plateformes du marche et du code TypeScript + SQL de production.

**EN** — This guide covers the complete architecture of an industrial experimentation platform: from assignment service to analysis pipeline, including feature flag patterns and required instrumentation. A robust platform supports running dozens of parallel tests without interference, with reliable analysis and automatic assignment anomaly detection.

---

## 1. Architecture Complete d'une Plateforme d'Experimentation

### Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXPERIMENTATION PLATFORM                     │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │  Config Store│    │  Assignment  │    │  Analysis        │  │
│  │  (experiments│───▶│  Service     │───▶│  Pipeline        │  │
│  │  definitions)│    │  (hashing)   │    │  (stats + viz)   │  │
│  └──────────────┘    └──────┬───────┘    └────────┬─────────┘  │
│                             │                     │            │
│                             ▼                     ▼            │
│                    ┌──────────────┐    ┌──────────────────┐    │
│                    │  Event       │    │  Dashboard       │    │
│                    │  Tracking    │───▶│  (Pulse, Metrics │    │
│                    │  (exposures  │    │  significance)   │    │
│                    │  + conversns)│    └──────────────────┘    │
│                    └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Data Warehouse  │
                    │  (assignments    │
                    │  + events tables)│
                    └──────────────────┘
```

### 1.1 Assignment Service — Logique d'Assignation Deterministe

**FR** — L'assignation doit etre deterministe (meme utilisateur → meme variante) et uniforme (distribution exacte conforme au ratio cible). On utilise un hash consistant de l'identifiant utilisateur et de la cle d'experience.

```typescript
import * as crypto from 'crypto';

interface ExperimentConfig {
  experimentKey: string;
  variants: Array<{ name: string; weight: number }>;  // weights sum to 1
  salt?: string;  // optional salt to decorrelate from other experiments
}

function assignVariant(userId: string, config: ExperimentConfig): string {
  // Hash deterministe : meme userId → meme bucket → meme variante
  const hashInput = `${config.experimentKey}:${config.salt ?? ''}:${userId}`;
  const hash = crypto.createHash('sha256').update(hashInput).digest('hex');

  // Conversion du hash en bucket [0, 1)
  const bucketValue = parseInt(hash.substring(0, 8), 16) / 0xFFFFFFFF;

  // Assignation par tranche de poids cumulatif
  let cumWeight = 0;
  for (const variant of config.variants) {
    cumWeight += variant.weight;
    if (bucketValue < cumWeight) {
      return variant.name;
    }
  }

  return config.variants[config.variants.length - 1].name;
}

// Test : meme userId → meme variante a chaque appel
const config: ExperimentConfig = {
  experimentKey: 'checkout_v2',
  variants: [
    { name: 'control', weight: 0.5 },
    { name: 'variant_a', weight: 0.5 },
  ],
};

const variant1 = assignVariant('user_12345', config);
const variant2 = assignVariant('user_12345', config);
console.assert(variant1 === variant2, 'Assignment must be deterministic');
console.log(`user_12345 → ${variant1}`);
```

### 1.2 Event Tracking — Exposition et Conversion

```typescript
interface ExposureEvent {
  type: 'experiment_exposure';
  userId: string;
  anonymousId?: string;
  experimentKey: string;
  variant: string;
  timestamp: number;
  sessionId: string;
  properties: {
    deviceType: 'mobile' | 'desktop' | 'tablet';
    country: string;
    platform: string;
    appVersion: string;
  };
}

interface ConversionEvent {
  type: string;  // ex: 'checkout_completed', 'signup_completed'
  userId: string;
  timestamp: number;
  properties: Record<string, unknown>;
  revenue?: number;  // Pour les metriques de revenu
}

class ExperimentTracker {
  private analyticsClient: any;
  private exposedExperiments = new Set<string>();

  constructor(analyticsClient: any) {
    this.analyticsClient = analyticsClient;
  }

  trackExposure(
    userId: string,
    experimentKey: string,
    variant: string,
    context: ExposureEvent['properties'],
  ): void {
    // Deduplication : n'envoyer l'exposition qu'une fois par session
    const dedupeKey = `${userId}:${experimentKey}`;
    if (this.exposedExperiments.has(dedupeKey)) {
      return;
    }
    this.exposedExperiments.add(dedupeKey);

    const event: ExposureEvent = {
      type: 'experiment_exposure',
      userId,
      experimentKey,
      variant,
      timestamp: Date.now(),
      sessionId: this.getSessionId(),
      properties: context,
    };

    this.analyticsClient.track(event);
  }

  private getSessionId(): string {
    // Implementation specifique au SDK analytics utilise
    return `session_${Date.now()}`;
  }
}
```

### 1.3 Analysis Pipeline

```
Raw Events (S3/BigQuery)
        │
        ▼
┌───────────────────────────────────────┐
│  1. Assignment Table                  │
│     userId | experimentKey | variant  │
│     assignedAt | ...properties        │
└───────────────────┬───────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Primary  │ │Secondary │ │Guardrail │
│ Metric   │ │ Metrics  │ │ Metrics  │
│(checkout │ │(session, │ │(errors,  │
│ conv.)   │ │ revenue) │ │ churn)   │
└──────────┘ └──────────┘ └──────────┘
        │           │           │
        └───────────┼───────────┘
                    ▼
        ┌───────────────────────┐
        │  Statistical Tests    │
        │  + Multiple Testing   │
        │  Correction           │
        └───────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  Experiment Report    │
        │  (significance, CI,   │
        │   recommendation)     │
        └───────────────────────┘
```

---

## 2. Feature Flags Patterns

### 2.1 Boolean Flag (Kill Switch)

```typescript
// Pattern le plus simple : activer/desactiver une feature
// Use case : rollout progressif avec possibilite de rollback instantane

interface BooleanFlag {
  key: string;
  enabled: boolean;
  targeting?: TargetingRule[];  // Override par segment
}

interface TargetingRule {
  attribute: string;   // ex: 'country', 'plan_type', 'beta_user'
  operator: 'in' | 'not_in' | 'equals' | 'contains';
  values: string[];
}

function evaluateBooleanFlag(
  flag: BooleanFlag,
  userContext: Record<string, string>,
): boolean {
  if (!flag.targeting || flag.targeting.length === 0) {
    return flag.enabled;
  }

  // Evaluer les regles de targeting (premier match gagne)
  for (const rule of flag.targeting) {
    const userValue = userContext[rule.attribute];
    if (!userValue) continue;

    const matches = (() => {
      switch (rule.operator) {
        case 'in': return rule.values.includes(userValue);
        case 'not_in': return !rule.values.includes(userValue);
        case 'equals': return rule.values[0] === userValue;
        case 'contains': return rule.values.some(v => userValue.includes(v));
        default: return false;
      }
    })();

    if (matches) return true;
  }
  return flag.enabled;
}
```

### 2.2 Multivariate Flag

```typescript
// Test A/B/C/D avec plusieurs variantes et distributions configurables

interface MultivariateFlag {
  key: string;
  variants: Array<{
    name: string;
    weight: number;   // Poids relatif (les poids sont normalises en interne)
    payload?: Record<string, unknown>;  // Donnees associees a la variante
  }>;
  defaultVariant: string;
}

function evaluateMultivariateFlag(
  flag: MultivariateFlag,
  userId: string,
): { variant: string; payload?: Record<string, unknown> } {
  const totalWeight = flag.variants.reduce((sum, v) => sum + v.weight, 0);
  const normalizedVariants = flag.variants.map(v => ({
    ...v,
    weight: v.weight / totalWeight,
  }));

  const assignedName = assignVariant(userId, {
    experimentKey: flag.key,
    variants: normalizedVariants,
  });

  const variant = flag.variants.find(v => v.name === assignedName)
    ?? flag.variants.find(v => v.name === flag.defaultVariant)!;

  return { variant: variant.name, payload: variant.payload };
}
```

### 2.3 Gradual Rollout

```typescript
// Rollout progressif : passer de 0% a 100% en plusieurs etapes
// Use case : deploiement prudent avec monitoring continu

interface GradualRolloutConfig {
  flagKey: string;
  rolloutPercentage: number;  // 0 a 100
  rolloutAttribute?: string;  // Optionnel : 'userId' par defaut
}

function isInRollout(
  config: GradualRolloutConfig,
  userId: string,
): boolean {
  if (config.rolloutPercentage <= 0) return false;
  if (config.rolloutPercentage >= 100) return true;

  const hashInput = `${config.flagKey}:rollout:${userId}`;
  const hash = crypto.createHash('sha256').update(hashInput).digest('hex');
  const bucket = (parseInt(hash.substring(0, 8), 16) / 0xFFFFFFFF) * 100;

  return bucket < config.rolloutPercentage;
}

// Schema de rollout recommande (avec monitoring entre chaque etape)
const ROLLOUT_SCHEDULE = [
  { percentage: 5,   duree: '2 jours',   action: 'Valider metriques de garde' },
  { percentage: 20,  duree: '2 jours',   action: 'Valider SRM et metriques primaires' },
  { percentage: 50,  duree: '3 jours',   action: 'Collecte de donnees A/B test officiel' },
  { percentage: 100, duree: 'permanent', action: 'Deploiement complet' },
];
```

---

## 3. Statsig — Deep Dive

### Gates, Experiments, Layers et Holdouts

```typescript
import Statsig from 'statsig-node';

await Statsig.initialize(process.env.STATSIG_SERVER_SECRET!, {
  environment: { tier: process.env.NODE_ENV },
});

// 1. Gate : feature flag avec targeting
const isNewCheckoutEnabled = await Statsig.checkGate(
  { userID: userId, email: userEmail, country: userCountry },
  'new_checkout_flow',  // Nom du gate configure dans la console Statsig
);

// 2. Experiment : test A/B avec metriques Pulse
const experiment = await Statsig.getExperiment(
  { userID: userId, custom: { plan_type: planType } },
  'checkout_cta_experiment',
);

const ctaText = experiment.get('cta_text', 'Finaliser la commande');
const ctaColor = experiment.get('cta_color', '#007AFF');
const showProgressBar = experiment.get('show_progress_bar', false);

// Log exposure automatique lors du getExperiment
// Le dashboard Pulse affiche automatiquement les metriques

// 3. Layer : evite les conflits entre experiments sur la meme surface
const layer = await Statsig.getLayer(
  { userID: userId },
  'checkout_layer',  // Experiments checkout s'excluent mutuellement dans ce layer
);

const variant = layer.get('variant', 'control');

// 4. Log d'evenement de conversion
Statsig.logEvent(
  { userID: userId },
  'checkout_completed',  // Metrique liee a l'experiment dans la console
  1,                     // Valeur (optionnel)
  { revenue: orderTotal.toString(), orderId },
);

await Statsig.shutdown();
```

### Configuration des Metriques dans Statsig

```
Types de metriques dans Statsig :

1. Event Count         : nombre d'occurrences de l'evenement
   → Exemple : nb de clics, nb de pages vues

2. Event User Rate     : % d'utilisateurs exposés ayant declenche l'evenement
   → Exemple : taux de conversion, taux d'abandon

3. Sum                 : somme d'une valeur sur les evenements
   → Exemple : revenu total, nb de produits achetes

4. Mean                : moyenne d'une valeur par utilisateur
   → Exemple : revenu moyen par utilisateur, temps de session moyen

5. Ratio               : rapport entre deux evenements
   → Exemple : revenu par visite, conversions par session

Metriques de garde recommandees pour chaque experiment checkout :
  - taux_erreur_paiement (ne doit pas augmenter)
  - latence_p99_checkout (ne doit pas augmenter)
  - taux_churn_7j (ne doit pas augmenter)
```

---

## 4. LaunchDarkly — Targeting Rules et Gradual Rollout

```typescript
import LaunchDarkly from '@launchdarkly/node-server-sdk';

const ldClient = LaunchDarkly.init(process.env.LAUNCHDARKLY_SDK_KEY!);
await ldClient.waitForInitialization({ timeout: 10 });

// Contexte utilisateur enrichi (LDContext)
const userContext: LaunchDarkly.LDContext = {
  kind: 'user',
  key: userId,
  email: userEmail,
  country: userCountry,
  custom: {
    plan_type: planType,
    account_age_days: accountAgeDays,
    mrr_eur: mrrEur,
    is_beta_tester: isBetaTester,
  },
};

// Evaluation d'un flag multivariate
const variant = await ldClient.variation('onboarding_flow_v3', userContext, 'control');

// Evaluation avec detail (pour logging)
const detail = await ldClient.variationDetail('onboarding_flow_v3', userContext, 'control');
console.log(`Variant: ${detail.value}, raison: ${JSON.stringify(detail.reason)}`);
// reason.kind : 'RULE_MATCH', 'FALLTHROUGH', 'OFF', 'TARGETING_MATCH'

// Track d'evenement de conversion
ldClient.track('checkout_completed', userContext, { revenue: orderTotal });

await ldClient.close();
```

### Targeting Rules LaunchDarkly (Configuration YAML/JSON)

```yaml
# Exemple de regle de targeting pour un rollout progressif
flag:
  key: new_pricing_page
  on: true
  targets: []
  rules:
    - description: "Equipe interne (100%)"
      clauses:
        - attribute: email
          op: endsWith
          values: ["@monentreprise.com"]
      variation: 1  # variante
      trackEvents: true

    - description: "Beta testers (100%)"
      clauses:
        - attribute: is_beta_tester
          op: in
          values: [true]
      variation: 1
      trackEvents: true

    - description: "Clients FR premium (50%)"
      clauses:
        - attribute: country
          op: in
          values: ["FR"]
        - attribute: plan_type
          op: in
          values: ["premium", "enterprise"]
      percentage:
        variation_0: 50000  # 50% controle (en millieme de %)
        variation_1: 50000  # 50% variante
      trackEvents: true

  fallthrough:
    percentage:
      variation_0: 100000  # 100% controle pour le reste
  offVariation: 0
  variations:
    - value: false   # controle
    - value: true    # variante
```

---

## 5. Unleash — Self-Hosted, Strategies et Variants

```typescript
import { UnleashClient, type IVariant } from 'unleash-proxy-client';

const unleash = new UnleashClient({
  url: process.env.UNLEASH_PROXY_URL!,
  clientKey: process.env.UNLEASH_CLIENT_KEY!,
  appName: 'web-frontend',
  refreshInterval: 15,   // Secondes
  metricsInterval: 60,
});

await unleash.start();

// Contexte enrichi pour le targeting
unleash.updateContext({
  userId,
  properties: {
    plan: planType,
    country: userCountry,
    deviceType: deviceType,
  },
});

// Feature toggle avec variante
function getOnboardingVariant(): IVariant {
  const variant = unleash.getVariant('onboarding_experiment');
  return variant.enabled
    ? variant
    : { name: 'control', enabled: false, feature_enabled: false };
}

// Strategies disponibles dans Unleash
const UNLEASH_STRATEGIES = {
  'default':              'Toujours actif si le flag est on',
  'userWithId':           'Liste blanche d\'userId specifiques',
  'gradualRolloutUserId': 'Rollout progressif par hash userId (deterministe)',
  'gradualRolloutRandom': 'Rollout progressif aleatoire (non deterministe, eviter)',
  'remoteAddress':        'Ciblage par IP (utile pour VPN interne)',
  'flexibleRollout':      'Rollout avec stickiness configurable (userId, sessionId, random)',
};
```

---

## 6. Tableau Comparatif des Plateformes

```
┌─────────────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Critere         │ Statsig  │ LaunchDk │ Split.io │Optimizely│ AB Tasty │ Homemade │
├─────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Modele          │ SaaS     │ SaaS     │ SaaS     │ SaaS     │ SaaS     │ Custom   │
│ Self-hosted     │ Non      │ Non      │ Non      │ Non      │ Non      │ Oui      │
│ Open source     │ Non      │ Non      │ Non      │ Non      │ Non      │ Oui      │
├─────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Analyse integ.  │ Excellent│ Basique  │ Bon      │ Bon      │ Bon      │ A faire  │
│ (Pulse, stats)  │          │          │          │          │          │          │
├─────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ SDK             │ 15+ lang │ 20+ lang │ 15+ lang │ 10+ lang │ JS/iOS   │ A faire  │
│ Feature flags   │ Oui      │ Excellent│ Oui      │ Oui      │ Limite   │ A faire  │
│ MAB / Adaptive  │ Non      │ Non      │ Non      │ Non      │ Non      │ Possible │
├─────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Prix (estim.)   │ Freemium │ $300/mo+ │ $400/mo+ │ $1k/mo+  │ $200/mo+ │ DevCost  │
│                 │ / usage  │          │          │          │          │ + Infra  │
├─────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Cas ideal       │ Startups │ Enterprise│ Enterprise│ Marketing│ Marketing│ Equipes  │
│                 │ scale-up │ / DevOps │ data     │ A/B      │ no-code  │ data 5+  │
├─────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Latence SDK     │ <5ms     │ <5ms     │ <5ms     │ <5ms     │ ~50ms    │ Variable │
│ (local eval.)   │          │          │          │          │ (server) │          │
└─────────────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘

Recommandations :
- Startup / scale-up (< 50 engineers) : Statsig (meilleur rapport qualite/prix, Pulse integre)
- Enterprise avec equipes DevOps matures : LaunchDarkly (targeting avance, audit logs)
- Besoin de controle total / RGPD strict : Unleash self-hosted ou solution homemade
- Focus marketing / no-code : AB Tasty (interface visuelle, pas de SDK requis)
```

---

## 7. Instrumentation Requise

### Schema Minimal des Tables

```sql
-- Table d'assignation (une ligne par utilisateur expose par experience)
CREATE TABLE experiment_assignments (
  user_id         VARCHAR(255)  NOT NULL,
  experiment_key  VARCHAR(255)  NOT NULL,
  variant         VARCHAR(100)  NOT NULL,
  assigned_at     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  session_id      VARCHAR(255),
  device_type     VARCHAR(50),   -- 'mobile', 'desktop', 'tablet'
  country         VARCHAR(10),
  platform        VARCHAR(50),   -- 'web', 'ios', 'android'
  app_version     VARCHAR(50),
  PRIMARY KEY (user_id, experiment_key),   -- Une seule assignation par exp.
  INDEX idx_experiment_assigned (experiment_key, assigned_at)
);

-- Table d'evenements de conversion
CREATE TABLE analytics_events (
  event_id        VARCHAR(255)  NOT NULL PRIMARY KEY,
  user_id         VARCHAR(255)  NOT NULL,
  event_type      VARCHAR(255)  NOT NULL,  -- 'checkout_completed', 'signup', etc.
  occurred_at     TIMESTAMP     NOT NULL,
  properties      JSON,                    -- Proprietes specifiques a l'evenement
  revenue         DECIMAL(12,2),           -- Optionnel : pour metriques de revenu
  INDEX idx_user_event (user_id, event_type, occurred_at),
  INDEX idx_event_type_time (event_type, occurred_at)
);
```

---

## 8. Analyse SQL des Experiments

### Intent-to-Treat Analysis (Standard)

```sql
-- Analyse principale : tous les utilisateurs assignes, qu'ils aient converti ou non
-- Intent-to-treat evite le biais de selection (ne pas exclure les non-actifs)

WITH assigned_users AS (
  SELECT
    user_id,
    variant,
    assigned_at,
    device_type,
    country
  FROM experiment_assignments
  WHERE experiment_key = 'checkout_v2'
    AND assigned_at BETWEEN '2024-03-01' AND '2024-03-15'
),
conversion_window AS (
  -- Fenetre de conversion : 7 jours apres l'exposition
  SELECT
    a.user_id,
    a.variant,
    a.assigned_at,
    a.device_type,
    a.country,
    MAX(CASE WHEN e.event_type = 'checkout_completed'
              AND e.occurred_at > a.assigned_at
              AND e.occurred_at <= DATEADD(day, 7, a.assigned_at)
         THEN 1 ELSE 0 END) AS converted,
    SUM(CASE WHEN e.event_type = 'checkout_completed'
              AND e.occurred_at > a.assigned_at
              AND e.occurred_at <= DATEADD(day, 7, a.assigned_at)
         THEN e.revenue ELSE 0 END) AS revenue_generated
  FROM assigned_users a
  LEFT JOIN analytics_events e ON a.user_id = e.user_id
  GROUP BY a.user_id, a.variant, a.assigned_at, a.device_type, a.country
),
summary AS (
  SELECT
    variant,
    COUNT(*)                          AS n_users,
    SUM(converted)                    AS n_conversions,
    AVG(converted)                    AS conversion_rate,
    SUM(revenue_generated)            AS total_revenue,
    AVG(revenue_generated)            AS avg_revenue_per_user,
    STDDEV(revenue_generated)         AS stddev_revenue
  FROM conversion_window
  GROUP BY variant
)
SELECT
  s.*,
  -- Uplift relatif vs controle
  (s.conversion_rate - c.conversion_rate) / c.conversion_rate AS lift_relatif,
  -- Ecart-type de la proportion (pour test statistique)
  SQRT(s.conversion_rate * (1 - s.conversion_rate) / s.n_users) AS se_conversion
FROM summary s
CROSS JOIN (SELECT conversion_rate FROM summary WHERE variant = 'control') c
ORDER BY variant;
```

### SRM Check (Sample Ratio Mismatch)

```sql
-- Verification SRM : le ratio controle/variante est-il conforme au design ?
-- Un SRM indique un probleme d'implementation du feature flag

WITH srm_check AS (
  SELECT
    variant,
    COUNT(*) AS n_assigned,
    SUM(COUNT(*)) OVER () AS n_total
  FROM experiment_assignments
  WHERE experiment_key = 'checkout_v2'
    AND assigned_at BETWEEN '2024-03-01' AND '2024-03-15'
  GROUP BY variant
)
SELECT
  variant,
  n_assigned,
  n_total,
  n_assigned * 1.0 / n_total AS ratio_observe,
  0.5 AS ratio_attendu,
  ABS(n_assigned * 1.0 / n_total - 0.5) AS deviation,
  -- Chi-square simplifie : chi2 = (observe - attendu)^2 / attendu
  -- Un chi2 > 10.83 correspond a p < 0.001 (seuil SRM)
  POWER(n_assigned - n_total * 0.5, 2) / (n_total * 0.5) AS chi2_contribution
FROM srm_check;

-- Si chi2_total = SUM(chi2_contribution) > 10.83 → SRM detecte → STOP
```

### Segmentation par Device

```sql
-- HTE : analyse des effets heterogenes par device_type
-- ATTENTION : appliquer correction Bonferroni (3 segments → alpha = 5%/3 = 1.67%)

SELECT
  device_type,
  variant,
  COUNT(*)                                        AS n_users,
  SUM(converted)                                  AS n_conversions,
  AVG(converted)                                  AS conversion_rate,
  AVG(converted) - LAG(AVG(converted)) OVER (
    PARTITION BY device_type ORDER BY variant
  )                                               AS delta_vs_control,
  -- Intervalle de confiance a 98.33% (Bonferroni pour 3 segments)
  AVG(converted) + 2.394 * SQRT(AVG(converted) * (1-AVG(converted)) / COUNT(*)) AS ic_haut,
  AVG(converted) - 2.394 * SQRT(AVG(converted) * (1-AVG(converted)) / COUNT(*)) AS ic_bas
FROM (
  SELECT a.user_id, a.variant, a.device_type, COALESCE(c.converted, 0) AS converted
  FROM experiment_assignments a
  LEFT JOIN (
    SELECT DISTINCT user_id, 1 AS converted
    FROM analytics_events
    WHERE event_type = 'checkout_completed'
  ) c ON a.user_id = c.user_id
  WHERE a.experiment_key = 'checkout_v2'
) t
GROUP BY device_type, variant
ORDER BY device_type, variant;
```

---

## 9. Network Effects et Interference (SUTVA)

### Violation de SUTVA

**FR** — SUTVA (Stable Unit Treatment Value Assumption) stipule que l'effet du traitement sur un utilisateur ne depend pas du traitement des autres utilisateurs. Les violations les plus courantes :

```
Cas de violation SUTVA :
1. Reseaux sociaux / virality : un utilisateur influence ses contacts
   → Risque : sous-estimation de l'effet (contamination du controle)

2. Marketplaces : plus d'acheteurs → plus de vendeurs → prix modifies
   → Risque : biais si controle et variante partagent le meme inventaire

3. Coupons / promotions : partage de codes promo entre groupes
   → Risque : contamination directe du controle

4. Algorithmes de recommendation : les actions de la variante modifient
   les recommendations vues par les utilisateurs controle
   → Risque : impossible a mesurer si le modele est global
```

### Randomisation par Cluster

```sql
-- Solution pour les marketplaces : randomiser par cluster (ex: par ville/region)
-- Plutot que par utilisateur, pour eviter la contamination inter-groupes

-- Assignation par region (cluster)
INSERT INTO experiment_assignments (user_id, experiment_key, variant, assigned_at)
SELECT
  u.user_id,
  'marketplace_v2' AS experiment_key,
  r.assigned_variant AS variant,
  NOW() AS assigned_at
FROM users u
JOIN (
  -- Assignation deterministe par region
  SELECT
    region_id,
    CASE
      WHEN FARM_FINGERPRINT(CONCAT('marketplace_v2', CAST(region_id AS STRING)))
           % 2 = 0 THEN 'control'
      ELSE 'variant'
    END AS assigned_variant
  FROM regions
  WHERE active = TRUE
) r ON u.region_id = r.region_id
WHERE u.created_at > '2024-01-01';
```

---

## 10. Implementation Complete — Checklist de Lancement

```typescript
// Checklist TypeScript : validation avant lancement d'un experiment

interface ExperimentLaunchChecklist {
  designDocument: {
    hypothese: string;
    metrique_primaire: string;
    metriques_secondaires: string[];
    metriques_de_garde: string[];
    segments_pre_specifies: string[];
    taille_echantillon_calculee: number;
    duree_minimale_jours: number;
    date_lancement: string;
    date_decision: string;
    alpha: number;
    power: number;
    mde_relatif: number;
  };
  validation_technique: {
    srm_check_configure: boolean;
    tracking_exposition_valide: boolean;
    tracking_conversion_valide: boolean;
    metriques_de_garde_alertes: boolean;
    qa_en_staging: boolean;
    rollback_plan: string;
  };
  gouvernance: {
    revue_par_statisticien: boolean;
    approbation_product_owner: boolean;
    document_de_design_partage: boolean;
  };
}

function validerChecklist(checklist: ExperimentLaunchChecklist): string[] {
  const erreurs: string[] = [];

  if (!checklist.designDocument.hypothese) {
    erreurs.push('BLOQUANT : hypothese non definie');
  }
  if (checklist.designDocument.taille_echantillon_calculee < 1000) {
    erreurs.push('ATTENTION : taille echantillon < 1000, test probablement sous-puissant');
  }
  if (checklist.designDocument.duree_minimale_jours < 14) {
    erreurs.push('ATTENTION : duree < 14 jours, risque de novelty effect non capte');
  }
  if (!checklist.validation_technique.srm_check_configure) {
    erreurs.push('BLOQUANT : SRM check non configure, impossible de valider l\'assignation');
  }
  if (!checklist.gouvernance.revue_par_statisticien) {
    erreurs.push('ATTENTION : pas de revue statistique, risque d\'erreurs methodologiques');
  }

  return erreurs;
}
```

---

## References Complementaires

- `references/statistical-foundations.md` — Theorie statistique, calculs de taille d'echantillon
- `references/bayesian-testing.md` — Thompson Sampling integre dans la plateforme
- `references/case-studies.md` — Implementation complete du cas checkout e-commerce
- Documentation Statsig : https://docs.statsig.com/
- Documentation LaunchDarkly : https://docs.launchdarkly.com/
- Documentation Unleash : https://docs.getunleash.io/
- "Experimentation Platform at Netflix" (Netflix Tech Blog) — architecture de reference
