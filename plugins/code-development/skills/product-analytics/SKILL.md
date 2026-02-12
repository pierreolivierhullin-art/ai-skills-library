---
name: product-analytics
description: This skill should be used when the user asks about "product analytics", "event tracking", "A/B testing", "experimentation", "product metrics", "funnel analysis", "retention analysis", "cohort analysis", "tracking plan", "Amplitude", "Mixpanel", "PostHog", "Segment", "analytique produit", "suivi d'événements", "tests A/B", "expérimentation", "métriques produit", "analyse de funnel", "analyse de rétention", "analyse de cohortes", "plan de tracking", "AARRR", "pirate metrics", "activation", "engagement", "conversion rate", "taux de conversion", "DAU", "MAU", "WAU", "feature adoption", "adoption fonctionnalité", "user segmentation", "segmentation utilisateurs", "heat maps", "session replay", "Hotjar", "FullStory", "Google Analytics", "GA4", "attribution", "privacy-compliant analytics", "CNIL", or needs guidance on product instrumentation, data-driven decisions, and privacy-compliant analytics.
version: 1.1.0
last_updated: 2026-02
---

# Product Analytics & Instrumentation / Analytique Produit & Instrumentation

## Overview / Vue d'ensemble

This skill covers the full spectrum of modern product analytics engineering: tracking plan design, event instrumentation, product metrics frameworks, experimentation platforms, and privacy-compliant analytics. It integrates state-of-the-art practices from 2024-2026 including warehouse-native analytics, PostHog as the open-source standard, privacy-first tracking, AI-powered insights, product-led growth metrics, and server-side instrumentation for a cookie-less world.

Cette skill couvre l'ensemble de l'ingénierie analytique produit moderne : conception de tracking plans, instrumentation d'événements, frameworks de métriques produit, plateformes d'expérimentation, et analytique conforme vie privée. Elle intègre les pratiques état de l'art 2024-2026 incluant l'analytique warehouse-native, PostHog comme standard open-source, le tracking privacy-first, les insights alimentés par l'IA, les métriques product-led growth, et l'instrumentation server-side pour un monde sans cookies.

## When This Skill Applies / Quand cette skill s'applique

Apply this skill when the user needs to:
- Design a tracking plan or event taxonomy for a product
- Implement client-side or server-side event tracking
- Define and measure product metrics (North Star, engagement, retention)
- Build funnel analysis or cohort-based retention analysis
- Design and run A/B tests or feature experiments
- Choose analytics tools (Amplitude, Mixpanel, PostHog, Segment)
- Implement GDPR/RGPD-compliant analytics and consent management
- Migrate to warehouse-native or privacy-first analytics
- Instrument product-led growth (PLG) funnels
- Evaluate statistical significance of experiments

Appliquer cette skill quand l'utilisateur a besoin de : concevoir un tracking plan, implémenter du tracking événementiel, définir des métriques produit, construire des analyses de funnels ou cohortes de rétention, concevoir des A/B tests, choisir des outils analytics, implémenter une analytique conforme RGPD, migrer vers de l'analytique warehouse-native, instrumenter des funnels PLG, ou évaluer la significativité statistique d'expériences.

## Core Principles / Principes fondamentaux

### 1. Tracking Plan First / Le tracking plan d'abord

Never instrument ad hoc. Design a structured tracking plan before writing any tracking code. Use the object-action naming convention (e.g., `Order Completed`, `Article Viewed`, `Subscription Started`). Define every event with its properties, types, expected values, and owner. Store the tracking plan in a versioned, shared document (Avo, Amplitude Data, or a Git-tracked YAML/JSON schema). Treat the tracking plan as a contract between product, engineering, and data teams.

Ne jamais instrumenter ad hoc. Concevoir un tracking plan structuré avant d'écrire du code de tracking. Utiliser la convention object-action (ex : `Order Completed`, `Article Viewed`). Définir chaque événement avec ses propriétés, types, valeurs attendues et propriétaire. Stocker le tracking plan dans un document versionné et partagé. Traiter le tracking plan comme un contrat entre les équipes produit, engineering et data.

### 2. Measure What Matters / Mesurer ce qui compte

Identify a single North Star Metric that captures the core value your product delivers. Align all teams around this metric. Decompose it into input metrics (levers) that teams can directly influence. Use the AARRR framework (Acquisition, Activation, Retention, Revenue, Referral) to ensure full-funnel coverage. Avoid vanity metrics -- prefer actionable metrics that drive decisions.

Identifier une North Star Metric unique capturant la valeur fondamentale du produit. Aligner toutes les équipes. Décomposer en métriques d'entrée (leviers). Utiliser le framework AARRR pour une couverture full-funnel. Éviter les vanity metrics au profit de métriques actionnables.

### 3. Experiment Rigorously / Expérimenter rigoureusement

Define a clear hypothesis before every experiment: "If we [change], then [metric] will [improve] by [amount] because [rationale]." Calculate the required sample size before starting based on Minimum Detectable Effect (MDE), baseline conversion, and desired statistical power (80%+). Never peek at results early without proper sequential testing corrections. Use guardrail metrics to ensure experiments do not degrade critical business metrics.

Définir une hypothèse claire avant chaque expérience. Calculer la taille d'échantillon requise avant de démarrer. Ne jamais consulter les résultats en avance sans correction de test séquentiel. Utiliser des guardrail metrics pour protéger les métriques métier critiques.

### 4. Privacy by Design / Privacy dès la conception

Embed consent management from day one. Implement server-side tracking to reduce dependency on browser cookies and ad blockers. Prefer first-party data collection over third-party scripts. Anonymize or pseudonymize personal data at the collection layer. Respect RGPD/GDPR consent signals: do not fire analytics events before explicit consent is granted (unless exempt under CNIL first-party analytics exemption). Evaluate cookie-less analytics alternatives (Matomo, Plausible, Fathom) for use cases that do not require user-level identification.

Intégrer la gestion du consentement dès le premier jour. Implémenter le tracking server-side. Privilégier la collecte first-party. Anonymiser ou pseudonymiser les données personnelles à la collecte. Respecter les signaux de consentement RGPD. Évaluer les alternatives cookie-less pour les cas ne nécessitant pas d'identification utilisateur.

### 5. Warehouse-Native Analytics / Analytique warehouse-native

Adopt a warehouse-native approach where the data warehouse (BigQuery, Snowflake, Databricks) is the single source of truth. Use reverse ETL tools (Census, Hightouch) to activate warehouse data in product tools. Consider warehouse-native analytics platforms (Mitzu, Hashboard, Lightdash) that query the warehouse directly instead of duplicating data. This architecture eliminates data silos, reduces vendor lock-in, and ensures analytics and ML models use the same data.

Adopter une approche warehouse-native où l'entrepôt de données est la source unique de vérité. Utiliser le reverse ETL pour activer les données dans les outils produit. Considérer les plateformes analytiques warehouse-native qui interrogent directement l'entrepôt. Cette architecture élimine les silos, réduit le vendor lock-in, et assure la cohérence données analytics/ML.

## Key Frameworks & Methods / Frameworks et méthodes clés

### Event Taxonomy — Object-Action Convention

Adopt a consistent, human-readable naming convention. Use `Object Action` format in Title Case:

| Event / Événement | Properties / Propriétés |
|---|---|
| `Page Viewed` | `page_name`, `page_url`, `referrer` |
| `Button Clicked` | `button_id`, `button_text`, `page_name` |
| `Order Completed` | `order_id`, `total`, `currency`, `items_count` |
| `Experiment Viewed` | `experiment_id`, `variant_id` |
| `Subscription Started` | `plan_id`, `plan_name`, `billing_cycle` |

### Metrics Hierarchy / Hiérarchie de métriques

```
North Star Metric (ex: Weekly Active Learners)
├── Acquisition: Sign-ups, Activation Rate
├── Activation: Aha Moment completion (Day-1 retention)
├── Engagement: DAU/MAU (stickiness), Sessions/User, Feature Usage
├── Retention: Day-1, Day-7, Day-30 cohort retention
├── Revenue: MRR, ARPU, LTV/CAC ratio
└── Referral: Viral coefficient, NPS, Invite rate
```

### Experimentation Maturity Model / Modèle de maturité expérimentation

| Level / Niveau | Description | Practices / Pratiques |
|---|---|---|
| **L1 — Ad hoc** | Occasional A/B tests, no process | Manual analysis, no sample size calculation |
| **L2 — Emerging** | Regular testing cadence, basic tooling | Fixed-horizon tests, frequentist p-values |
| **L3 — Scaling** | Feature flags everywhere, experiment platform | Sequential testing, guardrail metrics, MDE planning |
| **L4 — Mature** | All launches behind experiments, review board | Bayesian analysis, multi-armed bandits, CUPED variance reduction |
| **L5 — Excellence** | Experimentation culture, self-serve | Automated decisions, causal inference, interleaving, long-term holdouts |

## Decision Guide / Guide de décision

### Choosing an Analytics Stack / Choisir une stack analytics

```
START
├── Need open-source, self-hosted? → PostHog (analytics + experiments + feature flags + session replay)
├── Enterprise, large scale? → Amplitude or Mixpanel
│   ├── Deep behavioral analytics? → Amplitude
│   └── Simplicity, fast setup? → Mixpanel
├── Warehouse-native, no data duplication? → Mitzu, Hashboard, or Cube + custom
├── Privacy-first, no cookies, simple? → Plausible, Fathom, or Matomo
├── Need a CDP (Customer Data Platform)? → Segment or RudderStack (open-source)
│   └── Budget-conscious? → RudderStack or Jitsu (open-source)
├── Experimentation platform? → Statsig, Eppo, LaunchDarkly, or Optimizely
│   ├── Warehouse-native experiments? → Eppo or Statsig
│   └── Feature flags primary? → LaunchDarkly
└── GA4 replacement (web analytics)? → PostHog, Plausible, or Matomo
```

### Client-side vs. Server-side Tracking / Tracking client-side vs. server-side

| Criterion / Critère | Client-side | Server-side |
|---|---|---|
| **Ease of setup** | Simple (JS snippet) | Requires backend work |
| **Ad blocker resistance** | Low (blocked 30-40%) | High (not blockable) |
| **Data accuracy** | Lower (blockers, consent) | Higher (complete data) |
| **Privacy compliance** | Harder (cookies, 3P scripts) | Easier (first-party, server-controlled) |
| **Real-time UX events** | Native (clicks, scrolls) | Requires event forwarding |
| **Recommended for** | UX/behavior events | Conversions, revenue, critical business events |

**Best practice / Bonne pratique**: Use a hybrid approach. Track UX interactions client-side. Track business-critical events (purchases, subscriptions, activations) server-side. Forward server events to analytics via Segment/RudderStack server-side SDKs.

## Common Patterns & Anti-Patterns / Patterns et anti-patterns

### Patterns (Do This / Faire)

- **Tracking plan as code**: Store event schemas in a Git repository (JSON Schema, Avo, or Amplitude Data). Validate events at ingestion time. Fail CI if a tracked event violates the schema.
- **Server-side for critical events**: Track all revenue events, account creation, and subscription changes server-side to guarantee accuracy.
- **Cohort-based retention analysis**: Always analyze retention by cohort (sign-up week/month), never as a global average that hides trends.
- **Pre-experiment power analysis**: Calculate required sample size before launching any experiment. Avoid stopping early.
- **Guardrail metrics**: Define metrics that must not degrade (e.g., page load time, crash rate, revenue) alongside the primary experiment metric.
- **Feature flags for progressive rollout**: Roll out behind flags, measure impact on the target metric, then decide to ship or rollback.

### Anti-Patterns (Avoid / Éviter)

- **Tracking everything**: Instrumenting hundreds of events with no plan leads to data swamps, governance nightmares, and analytics distrust.
- **Vanity metrics obsession**: Celebrating page views, total registered users, or downloads instead of measuring active engagement and retention.
- **Peeking at experiments**: Checking results daily and stopping when p < 0.05 inflates false positive rate dramatically (up to 30%+).
- **No consent enforcement**: Firing analytics before consent is granted violates RGPD and risks fines up to 4% of global revenue.
- **Siloed analytics data**: Each team using a different tool with no shared taxonomy creates conflicting metrics and broken trust in data.
- **Ignoring sampling bias**: Not accounting for novelty effect, selection bias, or survivorship bias in experiment analysis.

## Implementation Workflow / Workflow d'implémentation

### Phase 1: Foundation (Week 1-2) / Phase 1 : Fondations

1. Define the product's North Star Metric and 3-5 input metrics.
2. Design the tracking plan: list core events (10-30), their properties, types, and owners.
3. Set up the analytics stack: PostHog (self-hosted or cloud) or Segment + Amplitude/Mixpanel.
4. Implement the Segment/RudderStack SDK (or PostHog SDK) in the frontend and backend.
5. Implement consent management (Axeptio, Didomi, or custom CMP) before any tracking fires.
6. Validate events: check payloads in the debugger, verify data types, run automated schema tests.

### Phase 2: Metrics & Dashboards (Week 3-4) / Phase 2 : Métriques et dashboards

1. Build the core product dashboard: North Star, DAU/WAU/MAU, activation rate, retention curves.
2. Implement funnel analysis for the primary user journey (sign-up to activation to conversion).
3. Set up cohort-based retention analysis (Day-1, Day-7, Day-30).
4. Create feature adoption dashboards for newly launched features.
5. Configure weekly automated reports (Slack/email) for the product team.

### Phase 3: Experimentation (Month 2-3) / Phase 3 : Expérimentation

1. Deploy a feature flag system (PostHog feature flags, LaunchDarkly, or Statsig).
2. Run the first A/B test with proper hypothesis, sample size calculation, and guardrail metrics.
3. Establish an experiment review process (design doc, peer review, results review).
4. Implement server-side experiment assignment for consistency and performance.
5. Build an experiment results dashboard with confidence intervals and statistical significance.

### Phase 4: Maturity (Ongoing) / Phase 4 : Maturité

1. Migrate to warehouse-native analytics: stream events to BigQuery/Snowflake, use dbt for metrics modeling.
2. Implement AI-powered anomaly detection on key product metrics (unexpected drops/spikes).
3. Adopt Bayesian experimentation or sequential testing for faster decisions.
4. Build self-serve analytics for PMs (Metabase, Lightdash, or PostHog SQL insights).
5. Run quarterly tracking plan audits: remove dead events, update schemas, validate data quality.
6. Implement long-term holdouts and causal inference for measuring cumulative experiment impact.



## State of the Art (2025-2026)

L'analytics produit se sophistique et se responsabilise :

- **Warehouse-native analytics** : Les outils d'analytics s'appuient directement sur le data warehouse (reverse ETL, warehouse-native CDPs) plutôt que sur des silos propriétaires.
- **Privacy-first analytics** : Post-RGPD, les solutions cookieless et server-side (Plausible, Fathom, PostHog self-hosted) gagnent du terrain.
- **AI-powered insights** : Les outils détectent automatiquement les anomalies, les corrélations et génèrent des insights actionnables via des LLM.
- **Experimentation avancée** : Le bayesian A/B testing, les bandits multi-bras et l'experimentation continue remplacent les tests classiques.
- **Product-Led Analytics** : L'analytics s'intègre directement dans le produit (in-app dashboards, behavioral nudges) plutôt que dans des outils séparés.

## Template actionnable

### Tracking plan

| Événement | Catégorie | Propriétés | Déclencheur | Priorité |
|---|---|---|---|---|
| `page_viewed` | Navigation | page_name, referrer | Chargement de page | P1 |
| `signup_started` | Activation | source, plan_type | Clic sur "S'inscrire" | P1 |
| `signup_completed` | Activation | method, plan_type | Compte créé | P1 |
| `feature_used` | Engagement | feature_name, context | Utilisation feature | P1 |
| `upgrade_started` | Monétisation | current_plan, target_plan | Clic sur upgrade | P1 |
| `payment_completed` | Monétisation | plan, amount, currency | Paiement réussi | P1 |
| `error_occurred` | Technique | error_type, page, stack | Erreur runtime | P2 |

## Prompts types

- "Aide-moi à créer un tracking plan pour mon application"
- "Comment mettre en place des tests A/B avec PostHog ?"
- "Propose des métriques AARRR adaptées à notre produit"
- "Comment analyser la rétention de nos utilisateurs par cohorte ?"
- "Aide-moi à implémenter un event tracking conforme au RGPD"
- "Quels outils choisir entre Amplitude, Mixpanel et PostHog ?"

## Skills connexes

| Skill | Lien |
|---|---|
| Marketing | `entreprise:marketing` — Métriques d'acquisition et attribution |
| UI/UX | `code-development:ui-ux` — Recherche utilisateur et tests d'usabilité |
| Data Engineering | `data-bi:data-engineering` — Infrastructure de tracking et pipelines |
| Data Literacy | `data-bi:data-literacy` — Visualisation et storytelling des métriques |
| Stratégie IA | `ai-governance:strategie-ia` — Analytics augmentés par l'IA |

## Additional Resources / Ressources complémentaires

Consult the following reference files for deep-dive guidance on each domain:

- **[Event Tracking](./references/event-tracking.md)** -- Tracking plan design, event naming conventions & taxonomy (object-action), client-side vs server-side instrumentation, SDKs (Segment, RudderStack, Jitsu), data validation & QA, schema validation, tracking governance.
- **[Product Metrics](./references/product-metrics.md)** -- North Star Metric, engagement metrics (DAU/WAU/MAU, stickiness), retention analysis (cohort, Day-N, curves), funnel analysis & conversion optimization, feature adoption metrics, AARRR/pirate metrics, product-led growth metrics.
- **[Experimentation](./references/experimentation.md)** -- Experiment design (hypothesis, variants, sample size calculator), statistical significance & power analysis (MDE, p-value, confidence interval), Bayesian vs frequentist, multi-armed bandits, platforms (Optimizely, LaunchDarkly, Statsig, Eppo), guardrail metrics.
- **[Privacy & Analytics](./references/privacy-analytics.md)** -- Consent management (CMP -- Didomi, Axeptio, OneTrust), server-side tracking for privacy, anonymization & pseudonymization, cookie-less tracking, RGPD-compliant analytics (CNIL exemption for first-party), GA4 alternatives.

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.
### External References / Références externes

- Amplitude Analytics Playbook: https://amplitude.com/blog/analytics-playbook
- PostHog Documentation: https://posthog.com/docs
- Segment Tracking Plan Guide: https://segment.com/academy/collecting-data/
- Evan Miller Sample Size Calculator: https://www.evanmiller.org/ab-testing/sample-size.html
- Eppo Experimentation Guide: https://www.geteppo.com/blog
- CNIL Analytics Exemption: https://www.cnil.fr/fr/cookies-et-autres-traceurs/regles/cookies-solutions-pour-les-outils-de-mesure-daudience
