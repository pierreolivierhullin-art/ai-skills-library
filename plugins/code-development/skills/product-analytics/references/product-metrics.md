# Product Metrics & Measurement / Métriques Produit & Mesure

Référence approfondie sur la North Star Metric, les métriques d'engagement (DAU/WAU/MAU, stickiness), l'analyse de rétention (cohortes, Day-N, courbes), l'analyse de funnels, l'adoption de fonctionnalités, les métriques AARRR/pirate, et les métriques product-led growth.

Deep-dive reference on North Star Metric, engagement metrics (DAU/WAU/MAU, stickiness), retention analysis (cohort, Day-N, curves), funnel analysis & conversion optimization, feature adoption metrics, AARRR/pirate metrics, and product-led growth metrics.

---

## Table of Contents

1. [North Star Metric Framework](#north-star-metric-framework)
2. [Engagement Metrics](#engagement-metrics)
3. [Retention Analysis](#retention-analysis)
4. [Funnel Analysis & Conversion Optimization](#funnel-analysis--conversion-optimization)
5. [Feature Adoption Metrics](#feature-adoption-metrics)
6. [AARRR / Pirate Metrics](#aarrr--pirate-metrics)
7. [Product-Led Growth Metrics](#product-led-growth-metrics)
8. [Metrics Modeling in the Warehouse](#metrics-modeling-in-the-warehouse)
9. [AI-Powered Product Insights](#ai-powered-product-insights)

---

## North Star Metric Framework

### Definition / Définition

The North Star Metric (NSM) is a single metric that captures the core value a product delivers to its customers. It serves as the primary compass for the entire organization: product, engineering, marketing, and sales teams align around it. The NSM must be measurable, actionable, and correlated with long-term business success (revenue, retention).

La North Star Metric (NSM) est une métrique unique capturant la valeur fondamentale qu'un produit délivre à ses clients. Elle sert de boussole pour toute l'organisation. La NSM doit être mesurable, actionnable et corrélée au succès business long terme.

### Choosing a North Star / Choisir une North Star

Apply these criteria when selecting the NSM:

1. **Reflects value delivery**: The metric increases when customers get more value from the product.
2. **Leading indicator**: It predicts future revenue and retention, not just current performance.
3. **Actionable**: Teams can directly influence it through product and engineering work.
4. **Understandable**: Every team member can explain what it means and how to move it.
5. **Not a vanity metric**: Page views, total sign-ups, and downloads are not North Stars — they do not reflect delivered value.

Critères : reflète la valeur délivrée, indicateur avancé, actionnable, compréhensible, pas une vanity metric.

### North Star Examples by Product Type / Exemples par type de produit

| Product Type | North Star Metric | Why |
|---|---|---|
| **SaaS B2B** | Weekly Active Teams using core feature | Measures active engagement with the key value prop |
| **E-commerce** | Weekly Purchases per Active Customer | Captures repeat purchase behavior |
| **Marketplace** | Transactions Completed per Week | Measures liquidity and match quality |
| **Content/Media** | Daily Active Users reading 3+ articles | Measures habitual engagement beyond casual visits |
| **FinTech** | Monthly Transaction Volume | Reflects trust and utility of the financial product |
| **EdTech** | Weekly Lessons Completed | Measures actual learning outcomes, not just logins |
| **Social** | Daily Active Users who post or comment | Measures active contribution, not passive consumption |
| **Developer Tool** | Weekly Deployments via Platform | Measures adoption integrated into the developer workflow |

### Input Metrics / Métriques d'entrée

Decompose the NSM into 3-5 input metrics (levers) that teams can directly influence:

```
North Star: Weekly Active Teams using Core Feature
├── Input 1: New teams activated this week (Activation)
├── Input 2: Returning teams from last week (Retention)
├── Input 3: Features used per team per session (Depth)
├── Input 4: Team members invited per team (Virality)
└── Input 5: Upgrade rate from free to paid (Monetization)
```

Assign each input metric to a specific team or squad. Set quarterly OKRs against input metrics. Review weekly in a product review meeting.

Décomposer la NSM en 3-5 métriques d'entrée (leviers). Assigner chaque levier à une équipe. Fixer des OKR trimestriels sur les métriques d'entrée.

---

## Engagement Metrics

### DAU / WAU / MAU

- **DAU** (Daily Active Users): Unique users who perform a qualifying action on a given day. Define "active" precisely — a page view may not count; a meaningful interaction (e.g., creating content, completing a task) is better.
- **WAU** (Weekly Active Users): Unique users active within a 7-day rolling window.
- **MAU** (Monthly Active Users): Unique users active within a 28-day or 30-day rolling window.

Définir "actif" précisément : une page vue ne compte pas toujours. Préférer une interaction significative. DAU = utilisateurs actifs par jour, WAU = par semaine (7j glissants), MAU = par mois (28-30j).

### Stickiness / Adhérence

**Stickiness = DAU / MAU**

Stickiness measures what fraction of monthly users come back daily. A stickiness of 25% means the average MAU uses the product ~7.5 days per month. Industry benchmarks:

| Category | Stickiness (DAU/MAU) | Interpretation |
|---|---|---|
| Social media (top tier) | 50-65% | Users come daily |
| SaaS productivity tools | 25-40% | Users come several days per week |
| E-commerce | 10-20% | Users come a few times per month |
| B2B SaaS (niche) | 15-25% | Active workday usage |

Track stickiness over time to detect engagement trends. A declining stickiness signals that new features or growth channels are attracting less-engaged users, or that habitual users are churning.

Stickiness = DAU/MAU. Mesure la fraction d'utilisateurs mensuels qui reviennent quotidiennement. Benchmarks : réseaux sociaux 50-65%, SaaS productivité 25-40%, e-commerce 10-20%.

### L7 / L28 Engagement Curves

Plot the distribution of how many days each user was active over a 7-day (L7) or 28-day (L28) period. A healthy product shows a "smile" curve with peaks at both ends: a large group of one-time visitors and a large group of power users. A declining curve with most users at 1 day signals poor retention. Track the shift in this distribution over time.

```
Users
│
│ ████                                        ████
│ ████                                        ████
│ ████ ██                                  ██ ████
│ ████ ████                            ████ ██████
│ ████ ████ ████ ████ ████ ████ ████ ████ ████████
└─────────────────────────────────────────────────
  1d   2d   3d   4d   5d   6d   7d   → Days active in L7
```

Tracer la distribution du nombre de jours actifs par utilisateur sur 7j ou 28j. Un produit sain montre une courbe "sourire" avec des pics aux deux extrémités.

### Sessions per User / Sessions par utilisateur

Track average and median sessions per user per day/week. More revealing than DAU alone because it captures depth of engagement. Combine with session duration and actions per session for a complete engagement picture.

### Intensity Metrics / Métriques d'intensité

- **Actions per session**: Average number of meaningful actions (not page views) per session.
- **Time spent**: Total and average time in the product per session and per week. Be cautious: time spent is not inherently positive (it could signal confusion or friction).
- **Feature breadth**: Number of distinct features used per user per week. Indicates how deeply users explore the product surface.

---

## Retention Analysis

### Why Retention Is the Most Important Metric / Pourquoi la rétention est la métrique la plus importante

Retention is the foundation of sustainable growth. Without retention, acquisition is a leaky bucket. A 5-percentage-point improvement in retention has a compounding effect that far exceeds a 5-percentage-point improvement in acquisition. Retention also directly impacts LTV, which determines how much can be spent on acquisition.

La rétention est le fondement de la croissance durable. Sans rétention, l'acquisition est un seau percé. Une amélioration de 5 points de rétention a un effet composé supérieur à 5 points d'acquisition.

### Cohort-based Retention / Rétention par cohortes

Always analyze retention by cohort (group of users who signed up in the same period), never as a global average. A global retention number hides trends: product improvements affect only newer cohorts, while churned older cohorts drag the average down.

Toujours analyser la rétention par cohorte (groupe d'utilisateurs inscrits sur la même période), jamais en moyenne globale. Un nombre global masque les tendances.

#### Retention Table / Table de rétention

```
Cohort       | Day 0 | Day 1 | Day 7 | Day 14 | Day 30 | Day 60 | Day 90
─────────────┼───────┼───────┼───────┼────────┼────────┼────────┼───────
Jan W1 2025  | 100%  | 45%   | 28%   | 22%    | 18%    | 14%    | 12%
Jan W2 2025  | 100%  | 48%   | 30%   | 25%    | 20%    | 16%    | --
Jan W3 2025  | 100%  | 52%   | 33%   | 27%    | 22%    | --     | --
Feb W1 2025  | 100%  | 55%   | 36%   | 28%    | --     | --     | --
```

Read this table vertically (by Day-N column) to see if newer cohorts retain better — this indicates product improvements are working. Read horizontally to understand the typical decay curve for a cohort.

Lire verticalement (par colonne Day-N) pour voir si les nouvelles cohortes retiennent mieux. Lire horizontalement pour comprendre la courbe de décroissance typique.

### Day-N Retention / Rétention Day-N

- **Day 1 retention**: Percentage of users who return the day after first use. Measures initial value delivery and "aha moment." Target: 40-60% for consumer apps, 70-80% for SaaS.
- **Day 7 retention**: Measures habit formation. Users who survive Day 7 are significantly more likely to become long-term users. Target: 20-30% for consumer, 40-60% for SaaS.
- **Day 30 retention**: Measures product-market fit signal. A Day 30 retention above 20% for consumer or 40% for SaaS indicates strong PMF.

Day 1 = valeur initiale et "aha moment." Day 7 = formation d'habitude. Day 30 = signal de product-market fit.

### Retention Curve Shapes / Formes de courbes de rétention

| Shape | Interpretation | Action |
|---|---|---|
| **Flattening curve** (stabilizes at 15-25%) | Healthy: a core group of retained users exists | Optimize activation to increase the asymptote |
| **Continuously declining** (never flattens) | Critical: no core retained group, leaky bucket | Fix the core product value before investing in growth |
| **Smiling curve** (rises after initial dip) | Excellent: users rediscover value after initial drop | Invest in re-engagement to amplify the rebound |
| **Cliff drop** (sharp drop at Day 1, then flat) | Activation problem: most users do not find value on first use | Redesign onboarding, reduce time-to-value |

### Unbounded vs. Bounded Retention

- **Unbounded (N-day)**: "Did the user come back on Day N or later?" — more forgiving, used for products with infrequent natural usage (e-commerce, travel).
- **Bounded (exact Day N)**: "Did the user come back exactly on Day N?" — stricter, used for habitual products (social, messaging, daily tools).
- **Bracket retention**: "Did the user come back during Week 2 (Day 8-14)?" — compromise approach for weekly-use products.

Choose the retention definition that matches the natural usage cadence of the product.

Choisir la définition de rétention correspondant à la cadence d'usage naturelle du produit.

### SQL Pattern — Cohort Retention / Pattern SQL

```sql
-- Cohort retention analysis (BigQuery/Snowflake compatible)
WITH user_cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC(MIN(event_date), WEEK) AS cohort_week,
    event_date
  FROM events
  WHERE event_name = 'Session Started'
  GROUP BY user_id, event_date
),
retention AS (
  SELECT
    cohort_week,
    DATE_DIFF(event_date, cohort_week, DAY) AS days_since_signup,
    COUNT(DISTINCT user_id) AS active_users
  FROM user_cohorts
  GROUP BY cohort_week, days_since_signup
),
cohort_size AS (
  SELECT cohort_week, COUNT(DISTINCT user_id) AS total_users
  FROM user_cohorts
  WHERE days_since_signup = 0
  GROUP BY cohort_week
)
SELECT
  r.cohort_week,
  r.days_since_signup,
  r.active_users,
  cs.total_users,
  ROUND(r.active_users / cs.total_users * 100, 1) AS retention_pct
FROM retention r
JOIN cohort_size cs ON r.cohort_week = cs.cohort_week
WHERE r.days_since_signup IN (0, 1, 7, 14, 30, 60, 90)
ORDER BY r.cohort_week, r.days_since_signup;
```

---

## Funnel Analysis & Conversion Optimization

### Funnel Design Principles / Principes de conception de funnels

1. **Define the critical path**: Identify the core sequence of steps from entry to conversion. For e-commerce: `Landing → Product Viewed → Added to Cart → Checkout Started → Order Completed`. For SaaS: `Signup → Onboarding Step 1 → Onboarding Complete → First Core Action → Subscription Started`.

2. **Measure step-by-step conversion**: Calculate the conversion rate between each consecutive step. Identify the biggest drop-off ("leaky step") and focus optimization effort there.

3. **Segment funnels**: Analyze funnels by acquisition channel, device type, geography, user plan, and cohort. Global funnels hide important differences.

4. **Set time windows**: Define a reasonable completion window (e.g., funnel must complete within 7 days). Too short a window excludes valid conversions; too long includes noise.

Définir le chemin critique, mesurer la conversion étape par étape, segmenter les funnels, définir des fenêtres temporelles raisonnables.

### Funnel Metrics / Métriques de funnel

| Metric | Formula | Usage |
|---|---|---|
| **Step conversion rate** | Users at Step N+1 / Users at Step N | Identify the leakiest step |
| **Overall conversion rate** | Users who completed / Users who entered | End-to-end funnel efficiency |
| **Time to convert** | Median time from Step 1 to final step | Identify friction and delays |
| **Drop-off rate** | 1 - Step conversion rate | Quantify loss at each step |
| **Conversion by segment** | Conversion rate grouped by channel/device/plan | Find high/low performers |

### Funnel Example / Exemple de funnel

```
Step 1: Landing Page Viewed        10,000 users (100%)
    ↓ 42% conversion
Step 2: Product Viewed              4,200 users (42%)
    ↓ 38% conversion
Step 3: Added to Cart               1,596 users (16%)
    ↓ 55% conversion ← Leaky step identified
Step 4: Checkout Started              878 users (8.8%)
    ↓ 72% conversion
Step 5: Order Completed               632 users (6.3%)

→ Focus optimization on Step 3→4 (55% conversion = biggest absolute loss)
```

### Conversion Optimization Tactics / Tactiques d'optimisation conversion

- **Reduce friction**: Remove unnecessary form fields, add progress indicators, simplify payment flow.
- **Social proof**: Add reviews, testimonials, trust badges at high-drop steps.
- **Urgency/scarcity**: Limited-time offers, stock indicators (use ethically).
- **Personalization**: Show relevant products/plans based on user behavior.
- **A/B test each step**: Do not redesign the entire funnel at once — test one step at a time to isolate impact.

Réduire la friction, ajouter la preuve sociale, tester A/B chaque étape individuellement.

---

## Feature Adoption Metrics

### Feature Adoption Framework / Framework d'adoption de fonctionnalités

Measure feature adoption through four lenses:

1. **Discovery**: What percentage of users discover the feature? (Saw the feature in the UI.)
2. **Activation**: What percentage of discoverers try the feature? (First use.)
3. **Adoption**: What percentage of activators use the feature repeatedly? (Used 3+ times.)
4. **Retention**: What percentage of adopters continue using the feature after 30 days?

Mesurer l'adoption via quatre lentilles : découverte, activation, adoption, rétention.

```
Feature Adoption Funnel:
All Users → Discovery (60%) → Activation (35%) → Adoption (20%) → Retention (12%)
```

### Feature Adoption Metrics / Métriques d'adoption

| Metric | Formula | Benchmark |
|---|---|---|
| **Feature Discovery Rate** | Users who saw feature / Total active users | Depends on feature placement |
| **Feature Activation Rate** | Users who used feature once / Users who discovered it | 30-50% is healthy |
| **Feature Adoption Rate** | Users who used feature 3+ times / Total active users | 15-30% for a good feature |
| **Feature Retention** | Users still using after 30d / Users who adopted | 40-60% target |
| **Feature DAU/MAU** | Daily feature users / Monthly feature users | Same as product stickiness |

### Breadth vs. Depth / Largeur vs. profondeur

- **Breadth**: How many distinct features does the average user use? Low breadth signals that users do not discover or need most features.
- **Depth**: How intensely does the user use each adopted feature? High depth with low breadth indicates a narrow but loyal use case.

Track both. A product with high breadth and high depth has strong product-market fit and expansion potential.

---

## AARRR / Pirate Metrics

### Framework Overview / Vue d'ensemble du framework

The AARRR framework (Dave McClure, 2007) structures product metrics into five stages of the customer lifecycle. Despite its age, it remains the most practical framework for organizing product analytics. Adapt the specific metrics to your product; the stages are universal.

Le framework AARRR structure les métriques produit en cinq étapes du cycle de vie client. Adapter les métriques spécifiques au produit ; les étapes sont universelles.

| Stage | Question | Key Metrics |
|---|---|---|
| **Acquisition** | How do users find us? | Traffic by channel, sign-up rate, CAC, CPL |
| **Activation** | Do users have a great first experience? | Onboarding completion, time to aha moment, Day-1 retention |
| **Retention** | Do users come back? | Day-7/30 retention, DAU/MAU, churn rate |
| **Revenue** | Do users pay? | MRR, ARPU, LTV, conversion to paid, expansion revenue |
| **Referral** | Do users tell others? | Viral coefficient (K), NPS, invite rate, referral conversion |

### AARRR Implementation Checklist / Checklist d'implémentation AARRR

For each stage, implement at least these events and metrics:

**Acquisition:**
- Track `Page Viewed` with `utm_source`, `utm_medium`, `utm_campaign` properties.
- Track `Account Created` with `acquisition_channel` property.
- Calculate CAC (Customer Acquisition Cost) = Marketing Spend / New Customers.

**Activation:**
- Define the "aha moment" (the action that correlates most strongly with long-term retention). Use correlation analysis to find it.
- Track `Onboarding Step Completed` for each step with a `step_number` property.
- Track the aha moment event (e.g., `First Report Created`, `First Team Member Invited`).
- Measure time-to-activation: median time from sign-up to aha moment.

**Retention:**
- Implement cohort retention tables (Day 1, 7, 14, 30, 60, 90).
- Track `Session Started` to measure return frequency.
- Calculate churn rate = (Users lost in period / Users at start of period).

**Revenue:**
- Track `Subscription Started`, `Subscription Upgraded`, `Subscription Cancelled` server-side.
- Calculate MRR = Sum of all monthly recurring revenue.
- Calculate ARPU = Revenue / Active Users.
- Calculate LTV = ARPU / Churn Rate (simplified) or use a cohort-based LTV model.
- Calculate LTV/CAC ratio (target > 3x).

**Referral:**
- Track `Invite Sent`, `Invite Accepted`.
- Calculate viral coefficient K = (Invites per user) x (Invite conversion rate). K > 1 = viral growth.
- Track NPS surveys (Net Promoter Score).

---

## Product-Led Growth Metrics

### PLG-specific Metrics / Métriques spécifiques au PLG

Product-led growth (PLG) relies on the product itself as the primary driver of acquisition, conversion, and expansion. This requires a specific set of metrics beyond traditional AARRR.

Le product-led growth (PLG) repose sur le produit comme moteur principal d'acquisition, conversion et expansion. Cela nécessite des métriques spécifiques au-delà du AARRR traditionnel.

| Metric | Formula | Target |
|---|---|---|
| **Time to Value (TTV)** | Time from sign-up to first value moment | Minimize (< 5 min ideal) |
| **Product Qualified Lead (PQL)** | Users who hit activation criteria in free tier | Define based on correlation with conversion |
| **Free to Paid Conversion** | Paid users / Total free users | 2-5% for freemium, 15-25% for free trial |
| **Natural Rate of Growth (NRG)** | Organic sign-ups / Total sign-ups | > 60% is PLG-driven |
| **Expansion Revenue Rate** | Revenue from upsells/upgrades / Starting MRR | > 120% Net Revenue Retention |
| **PQL to Customer Rate** | Customers / PQLs | 20-40% |
| **Seat Expansion Rate** | New seats added / Starting seats | Indicates organic team adoption |
| **Time to Expand** | Time from first paid to upgrade/expansion | Shorter = stronger value delivery |

### Product Qualified Leads (PQLs) / Leads qualifiés par le produit

Define PQL criteria based on in-product behavior that correlates with conversion to paid. Use a scoring model:

```
PQL Score Components (example for a SaaS tool):
+20 pts: Completed onboarding
+15 pts: Used core feature 3+ times
+10 pts: Invited a team member
+10 pts: Connected an integration
+15 pts: Active on 5+ days in first 14 days
+10 pts: Viewed pricing page
──────
Threshold: PQL if score >= 50
```

Implement PQL scoring in the data warehouse, then sync to CRM (HubSpot, Salesforce) via reverse ETL (Census, Hightouch) to trigger sales outreach at the right moment.

Définir les critères PQL basés sur le comportement in-product corrélé à la conversion. Implémenter un scoring dans le warehouse, synchroniser vers le CRM via reverse ETL.

### Net Revenue Retention (NRR)

**NRR = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR**

NRR above 100% means the product grows revenue from existing customers even without new acquisitions. Top PLG companies achieve NRR of 120-150%. Track monthly, report quarterly.

NRR au-dessus de 100% signifie que le produit augmente le revenu des clients existants sans nouvelles acquisitions. Les meilleures entreprises PLG atteignent 120-150%.

---

## Metrics Modeling in the Warehouse

### dbt Metrics Layer / Couche métriques dbt

Use dbt (data build tool) to model product metrics as SQL transformations in the warehouse. This ensures a single source of truth for metric definitions, version-controlled and testable.

Utiliser dbt pour modeler les métriques produit comme transformations SQL dans le warehouse. Source unique de vérité, versionnée et testable.

```sql
-- models/metrics/daily_active_users.sql
WITH daily_activity AS (
  SELECT
    DATE_TRUNC('day', event_timestamp) AS activity_date,
    user_id,
    COUNT(*) AS event_count
  FROM {{ ref('stg_events') }}
  WHERE event_name IN ('Session Started', 'Feature Used', 'Content Created')
  GROUP BY 1, 2
)
SELECT
  activity_date,
  COUNT(DISTINCT user_id) AS dau,
  SUM(event_count) AS total_events,
  AVG(event_count) AS avg_events_per_user
FROM daily_activity
GROUP BY 1
```

```sql
-- models/metrics/stickiness.sql
WITH dau AS (
  SELECT activity_date, COUNT(DISTINCT user_id) AS dau
  FROM {{ ref('daily_active_users_detail') }}
  GROUP BY 1
),
mau AS (
  SELECT
    activity_date,
    COUNT(DISTINCT user_id) AS mau
  FROM {{ ref('daily_active_users_detail') }}
  WHERE activity_date >= DATEADD('day', -28, CURRENT_DATE)
  GROUP BY 1
)
SELECT
  d.activity_date,
  d.dau,
  m.mau,
  ROUND(d.dau::FLOAT / NULLIF(m.mau, 0) * 100, 1) AS stickiness_pct
FROM dau d
JOIN mau m ON d.activity_date = m.activity_date
```

### Semantic Layer / Couche sémantique

Use a semantic layer (dbt Semantic Layer, Cube, LookML, Metriql) to define metrics with their dimensions, time grains, and business logic once. All downstream tools (dashboards, notebooks, AI agents) query through this layer, ensuring consistent metric definitions.

Utiliser une couche sémantique (dbt Semantic Layer, Cube, LookML) pour définir les métriques avec leurs dimensions, grains temporels et logique métier une seule fois. Tous les outils downstream interrogent cette couche.

---

## AI-Powered Product Insights

### Automated Anomaly Detection / Détection d'anomalies automatisée

Deploy anomaly detection on critical product metrics to surface unexpected changes before they are noticed manually:

- **Volume anomalies**: Sudden drop in DAU, sessions, or events (indicates broken tracking, outage, or external factor).
- **Conversion anomalies**: Unexpected funnel conversion rate changes (indicates UX regression or experiment gone wrong).
- **Retention anomalies**: Cohort retention deviating from historical patterns.

Use tools like PostHog alerts, Amplitude anomaly detection, Metaplane (data quality), or Monte Carlo (data observability).

Déployer la détection d'anomalies sur les métriques critiques : anomalies de volume, de conversion, de rétention. Utiliser PostHog, Amplitude, Metaplane, ou Monte Carlo.

### LLM-Powered Analytics / Analytics alimentées par LLM

The 2024-2026 wave of AI-powered analytics enables natural language queries over product data:

- **PostHog SQL Insights + AI**: Ask questions in natural language, get SQL queries and visualizations.
- **Amplitude Ask Amplitude**: Natural language interface for behavioral analytics.
- **Custom LLM agents**: Build agents (LangChain, Claude) that query the warehouse semantic layer to answer product questions.

Implement guardrails: validate generated SQL, limit query scope (read-only, specific tables), and require human review for business-critical decisions.

Les analytics alimentées par IA permettent des requêtes en langage naturel. PostHog, Amplitude proposent des interfaces IA. Construire des agents LLM custom interrogeant la couche sémantique. Implémenter des garde-fous.

### Correlation and Causal Analysis / Analyse de corrélation et causale

Use AI-assisted analysis to identify:

- **Features correlated with retention**: Which actions in the first 7 days predict 30-day retention? This reveals the "aha moment."
- **Segments with anomalous behavior**: Which user segments retain at dramatically different rates?
- **Experiment heterogeneous effects**: Does the treatment effect vary by user segment?

Tools: Amplitude Experiment Results (heterogeneous treatment effects), custom Python (causal inference with DoWhy, EconML), or Eppo's segment analysis.

Utiliser l'analyse IA pour identifier les fonctionnalités corrélées à la rétention, les segments anomaux, et les effets hétérogènes d'expériences.
