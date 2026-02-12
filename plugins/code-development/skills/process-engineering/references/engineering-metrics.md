# Engineering Metrics — DORA, SPACE, Cycle Time, Developer Productivity & Engineering Intelligence

## Vue d'ensemble / Overview

**FR** — Ce document de reference couvre l'ensemble des metriques d'ingenierie logicielle : metriques DORA (frequence de deploiement, lead time, MTTR, taux d'echec des changements), framework SPACE, cycle time et throughput, debats sur la productivite des developpeurs, OKRs d'ingenierie, burndown et velocite, et plateformes d'intelligence ingenierie (LinearB, Jellyfish, DX, Swarmia). La mesure de la performance d'ingenierie est un sujet sensible et complexe. Bien faite, elle eclaire les decisions, identifie les goulots d'etranglement et motive l'amelioration continue. Mal faite, elle detruit la confiance, incentive le gaming et cree une culture toxique. Ce guide fournit un cadre rigoureux pour mesurer ce qui compte, eviter les pieges classiques, et utiliser les metriques comme outil d'amelioration — jamais comme outil de surveillance.

**EN** — This reference document covers the full landscape of software engineering metrics: DORA metrics (deployment frequency, lead time for changes, MTTR, change failure rate), SPACE framework, cycle time and throughput, developer productivity debates, engineering OKRs, burndown and velocity, and engineering intelligence platforms (LinearB, Jellyfish, DX, Swarmia). Measuring engineering performance is a sensitive and complex topic. Done well, it illuminates decisions, identifies bottlenecks, and motivates continuous improvement. Done poorly, it destroys trust, incentivizes gaming, and creates a toxic culture. This guide provides a rigorous framework for measuring what matters, avoiding classic pitfalls, and using metrics as improvement tools — never as surveillance tools.

---

## DORA Metrics — Deep Dive

### The Four Key Metrics

The DORA (DevOps Research and Assessment) metrics, established by Nicole Forsgren, Jez Humble, and Gene Kim, are the most validated measures of software delivery performance. A decade of research (Accelerate State of DevOps Reports, 2014-2025) demonstrates that these four metrics correlate with organizational performance.

#### 1. Deployment Frequency (DF)

**Definition**: How often the team successfully deploys code to production.

**How to measure**: Count the number of successful deployments to the production environment per time period. Use CI/CD system data (GitHub Actions deployment events, ArgoCD sync events, deployment pipeline completion events).

**Performance levels:**
| Level | Frequency | FR |
|---|---|---|
| **Elite** | On-demand, multiple times per day | A la demande, plusieurs fois par jour |
| **High** | Between once per week and once per month | Entre une fois par semaine et une fois par mois |
| **Medium** | Between once per month and once every six months | Entre une fois par mois et une fois tous les six mois |
| **Low** | Less than once every six months | Moins d'une fois tous les six mois |

**Improvement levers:**
- Adopt trunk-based development with feature flags to decouple deployment from release
- Reduce batch size: smaller deployments are less risky and faster to review
- Automate the deployment pipeline end-to-end (zero manual steps)
- Implement progressive delivery (canary, blue-green) to reduce deployment fear
- Address test suite speed: slow tests discourage frequent deployment

#### 2. Lead Time for Changes (LT)

**Definition**: The time from code commit to code running successfully in production.

**How to measure**: Calculate the median time from the first commit in a PR to that code running in production. Source data from git timestamps and deployment logs.

**Performance levels:**
| Level | Lead Time | FR |
|---|---|---|
| **Elite** | Less than one hour | Moins d'une heure |
| **High** | Between one day and one week | Entre un jour et une semaine |
| **Medium** | Between one month and six months | Entre un mois et six mois |
| **Low** | More than six months | Plus de six mois |

**Common bottlenecks and solutions:**
| Bottleneck | Symptom | Solution | FR |
|---|---|---|---|
| **Slow PR reviews** | PRs wait 24+ hours for review | Set PR review SLA (< 4 hours), use auto-assignment, keep PRs < 400 lines | Definir un SLA de review PR (< 4h) |
| **Slow CI pipeline** | Pipeline takes 30+ minutes | Parallelize tests, use caching, run only affected tests in monorepos | Paralleliser les tests, utiliser le cache |
| **Manual QA gate** | Stories wait days for manual testing | Automate regression tests, shift QA left, use risk-based testing | Automatiser les tests de regression |
| **Manual deployment approval** | Deployments require manager sign-off | Automate approvals for low-risk changes, use progressive delivery for high-risk | Automatiser les approbations pour les changements a faible risque |
| **Environment contention** | Teams queue for shared staging environments | Use ephemeral preview environments per PR | Utiliser des environnements ephemeres par PR |

#### 3. Mean Time to Restore (MTTR)

**Definition**: The time from a production incident being detected to the service being restored.

**How to measure**: Calculate the median time from incident detection (alert firing or customer report) to service restoration (incident resolved in PagerDuty/Opsgenie). Source data from incident management tools.

**Performance levels:**
| Level | MTTR | FR |
|---|---|---|
| **Elite** | Less than one hour | Moins d'une heure |
| **High** | Less than one day | Moins d'un jour |
| **Medium** | Between one day and one week | Entre un jour et une semaine |
| **Low** | More than six months | Plus de six mois |

**Improvement levers:**
- Write runbooks for every known failure mode and link them to alerts
- Implement rollback automation (one-click or automatic rollback on error rate spike)
- Invest in observability: structured logging, distributed tracing, and actionable alerting
- Practice incident response through game days and chaos engineering
- Reduce blast radius through circuit breakers, bulkheads, and feature flags

#### 4. Change Failure Rate (CFR)

**Definition**: The percentage of deployments to production that result in degraded service and require remediation (rollback, hotfix, patch).

**How to measure**: (Number of failed deployments / Total number of deployments) x 100. A "failed deployment" is one that triggers a rollback, hotfix, or incident. Source data from CI/CD and incident management tools.

**Performance levels:**
| Level | Change Failure Rate | FR |
|---|---|---|
| **Elite** | 0-5% | 0-5% |
| **High** | 6-15% | 6-15% |
| **Medium** | 16-30% | 16-30% |
| **Low** | 46-60% | 46-60% |

**Improvement levers:**
- Increase automated test coverage (especially integration and contract tests)
- Implement progressive delivery: canary deployments catch issues with a small user subset
- Add pre-deployment validation: smoke tests, synthetic monitoring, database migration dry-runs
- Improve code review quality: use PR checklists, AI-assisted review, and pair programming for complex changes
- Reduce batch size: smaller changes are easier to review and less likely to fail

**FR** — Les quatre metriques DORA sont les mesures les plus validees de la performance de livraison logicielle. Frequence de deploiement (combien souvent), lead time (combien rapidement), MTTR (combien vite on restaure), taux d'echec des changements (combien de deploiements echouent). Viser le niveau elite : deploiement multiple par jour, lead time < 1h, MTTR < 1h, taux d'echec < 5%.

### DORA — Beyond the Four (2024-2026 Additions)

The 2024 and 2025 State of DevOps reports introduced additional dimensions:

- **Reliability**: goes beyond MTTR to include service-level objectives (SLOs), error budgets, and user-perceived reliability. Measure SLO compliance rate.
- **Documentation quality**: 2024 report highlighted that teams with high-quality documentation have 25% higher delivery performance.
- **AI adoption impact**: 2025 report measures how AI tool adoption correlates with delivery performance. Early findings: AI improves individual throughput but can increase change failure rate if review practices are not adapted.
- **Developer satisfaction**: the latest reports include developer well-being and satisfaction as a predictor of performance. Burnout correlates with lower performance across all four metrics.

---

## The SPACE Framework

### Five Dimensions of Developer Productivity

The SPACE framework (Forsgren, Storey, Maddila, Zimmermann, Houck — ACM Queue, 2021) provides a multidimensional model for understanding developer productivity. No single metric captures productivity — use SPACE to select metrics across multiple dimensions.

#### S — Satisfaction and Well-being

**What it measures**: how fulfilled, happy, and healthy developers feel about their work, team, and tools.

**Why it matters**: satisfied developers stay longer (retention), produce higher-quality work, and contribute to a positive team culture. Burnout is the single biggest threat to engineering performance.

**Example metrics:**
| Metric | How to measure | Target | FR |
|---|---|---|---|
| Developer satisfaction score | Quarterly survey (1-5 scale) | > 4.0 | Score de satisfaction developpeur |
| eNPS (employee Net Promoter Score) | "Would you recommend working here?" | > 30 | "Recommanderiez-vous de travailler ici ?" |
| Burnout indicators | Survey questions on exhaustion, cynicism, reduced efficacy | Trending down | Indicateurs d'epuisement professionnel |
| Tooling satisfaction | Survey on specific tools and processes | > 3.5/5 per tool | Satisfaction vis-a-vis des outils |

#### P — Performance

**What it measures**: the outcomes of developer work — quality, impact, and reliability of the software produced.

**Why it matters**: ultimately, engineering exists to produce valuable, reliable software. Performance metrics connect engineering work to business outcomes.

**Example metrics:**
| Metric | How to measure | Target | FR |
|---|---|---|---|
| Customer impact (features shipped that move business metrics) | Product analytics | Increasing | Impact client des features livrees |
| Reliability (SLO compliance) | Monitoring systems | > 99.9% | Conformite SLO |
| Code quality (defect escape rate) | Bugs found in production per release | Decreasing | Taux de defauts echappes en production |
| Change failure rate (DORA) | CI/CD + incident data | < 5% | Taux d'echec des changements |

#### A — Activity

**What it measures**: the volume of actions and outputs, counted over time.

**Why it matters**: activity metrics provide leading indicators and are easy to collect, but they are the most dangerous dimension to use in isolation. Activity without context rewards busyness over impact.

**Example metrics (use with extreme caution):**
| Metric | How to measure | Caution | FR |
|---|---|---|---|
| Number of PRs merged | Git/GitHub data | More PRs != more value. Tiny PRs inflate count | Plus de PRs != plus de valeur |
| Deployment frequency (DORA) | CI/CD data | Good activity metric because it correlates with outcomes | Bonne metrique d'activite car correlee aux resultats |
| Number of code reviews completed | GitHub data | Incentivizes rubber-stamping if measured alone | Incentive le rubber-stamping si mesure seul |
| Story points completed | Issue tracker | Inflation risk. Never compare across teams | Risque d'inflation. Ne jamais comparer entre equipes |

**Critical rule**: NEVER use activity metrics for individual performance evaluation. Use them only for team-level trend analysis.

#### C — Communication and Collaboration

**What it measures**: how effectively developers communicate, share knowledge, and work together.

**Why it matters**: modern software development is fundamentally collaborative. A highly productive individual who hoards knowledge and creates bottlenecks reduces team throughput.

**Example metrics:**
| Metric | How to measure | Target | FR |
|---|---|---|---|
| PR review turnaround time | GitHub data (time from review request to first review) | < 4 hours during business hours | Temps de reponse des reviews de PR |
| Knowledge distribution (bus factor) | Git analysis: how many developers contribute to each area | > 2 per service/area | Distribution des connaissances |
| Documentation contributions | Git data on doc file changes | Increasing | Contributions a la documentation |
| Cross-team collaboration frequency | PR reviews across team boundaries | Stable or increasing | Frequence de collaboration inter-equipes |

#### E — Efficiency and Flow

**What it measures**: the ability to complete work with minimal friction, delay, and context switching.

**Why it matters**: efficiency captures the developer experience — are processes smooth or frustrating? Is the toolchain helping or hindering?

**Example metrics:**
| Metric | How to measure | Target | FR |
|---|---|---|---|
| Cycle time | Issue tracker (In Progress to Done) | Decreasing over time | Temps de cycle |
| Lead time for changes (DORA) | Git + CI/CD data | < 1 day (high) | Delai de livraison des changements |
| CI build time | CI/CD data | < 10 minutes | Temps de build CI |
| Context switching frequency | Survey or calendar analysis | Decreasing | Frequence de changement de contexte |
| Wait time ratio | Value stream map | < 20% of total lead time | Ratio de temps d'attente |

### How to Use SPACE

1. **Select 3-5 metrics across at least 3 SPACE dimensions**. Never rely on a single dimension.
2. **Combine perceptual and system metrics**: pair surveys (satisfaction, perceived efficiency) with objective data (cycle time, deployment frequency).
3. **Measure at team level, not individual level**. Individual developer metrics destroy trust and encourage gaming.
4. **Review trends, not snapshots**: a single data point means nothing. Track metrics over quarters and look for directional trends.
5. **Discuss metrics in retrospectives**: make metrics a conversation starter, not a judgment tool. Ask "what is this trend telling us?" not "why is this number low?"

**FR** — Le framework SPACE definit cinq dimensions de la productivite developpeur : Satisfaction, Performance, Activite, Communication, Efficience. Selectionner 3-5 metriques couvrant au moins 3 dimensions. Combiner metriques perceptuelles (enquetes) et systeme (donnees CI/CD). Mesurer au niveau equipe, jamais individuel. Analyser les tendances, pas les snapshots.

---

## Cycle Time & Throughput

### Cycle Time Anatomy

Cycle time is the total elapsed time from when work begins on an item to when it is delivered to production. Decompose it to identify bottlenecks:

```
Cycle Time = Coding Time + PR Review Time + CI Time + Deploy Time + Wait Time

Where:
- Coding Time    = first commit to PR opened
- PR Review Time = PR opened to PR approved
- CI Time        = PR merge to CI pipeline completion
- Deploy Time    = CI completion to production deployment
- Wait Time      = all idle time between stages (queues, blocked items)
```

### Measuring and Improving Cycle Time

**Data sources:**
- Git timestamps (commit, PR creation, PR merge)
- CI/CD pipeline timestamps (build start, test completion, deployment)
- Issue tracker timestamps (status transitions)

**Benchmarks (2024-2026 industry data):**
| Metric | Good | Median | Poor | FR |
|---|---|---|---|---|
| Total cycle time | < 2 days | 5-7 days | > 14 days | Temps de cycle total |
| PR review time | < 4 hours | 12-24 hours | > 48 hours | Temps de review PR |
| CI pipeline time | < 10 minutes | 15-30 minutes | > 45 minutes | Temps du pipeline CI |
| Deploy time (after merge) | < 30 minutes | 1-4 hours | > 24 hours | Temps de deploiement |

**Improvement strategies by bottleneck:**
| Bottleneck | Improvement | Expected impact | FR |
|---|---|---|---|
| Long coding time | Better story refinement, pair programming, smaller stories | -30% coding time | Meilleur refinement, pair programming |
| Slow PR reviews | Auto-assignment, review SLA, smaller PRs, AI pre-review | -50% review wait time | Auto-assignation, SLA de review, PRs plus petites |
| Slow CI | Parallelization, caching, affected-only testing, faster hardware | -40-60% CI time | Parallelisation, cache, tests affectes uniquement |
| Manual deploy steps | Full automation, GitOps, one-click deploy | -80% deploy time | Automatisation complete |
| Wait time (queues) | WIP limits, eliminate handoffs, cross-functional teams | -50% wait time | Limites WIP, eliminer les transferts |

### Throughput

**Definition**: the number of work items completed per time period (typically per week or per sprint).

**How to measure**: count items that transition to "Done" per week. Use the issue tracker's cycle time report or build a custom dashboard.

**How to use throughput:**
- Track weekly throughput as a team metric. Plot it on a run chart.
- Use throughput for Monte Carlo forecasting: "Given our historical throughput of 8-12 items per week, we have an 85% probability of completing the remaining 40 items in 4 weeks."
- Never compare throughput across teams (different item sizes, different domains).
- Combine with cycle time: high throughput with high cycle time means large batch sizes. High throughput with low cycle time means healthy flow.

**FR** — Le cycle time mesure le temps total de la prise en charge d'un item a sa livraison en production. Le decomposer en coding time, review time, CI time, deploy time et wait time pour identifier les goulots. Le throughput mesure le nombre d'items livres par periode. Les combiner pour piloter l'amelioration continue.

---

## Developer Productivity Debates (2023-2026)

### The McKinsey Controversy

In August 2023, McKinsey published "Yes, you can measure software developer productivity," proposing to measure individual developer productivity using a combination of DORA metrics, SPACE framework, and a new "talent" dimension including "Developer Velocity Index Benchmark" and individual contribution analysis. The article provoked intense backlash from the engineering community.

**Key criticisms:**
- **Kent Beck and Gergely Orosz** published a rebuttal arguing that measuring individual developer productivity incentivizes gaming, destroys collaboration, and misses the sociotechnical nature of software engineering.
- **Dan North** argued that "developer productivity" is an ill-defined concept and that organizations should focus on outcomes (delivered value) rather than outputs (developer activity).
- **The DORA team** clarified that their metrics are designed for team and organizational level measurement, not individual developer evaluation.

**The consensus position (2024-2026):**
1. **Team-level metrics are valid and useful** (DORA, team cycle time, team throughput).
2. **Individual activity metrics are harmful** (lines of code, commits, PRs per developer).
3. **Perceptual metrics are essential** (developer satisfaction, perceived friction, cognitive load surveys).
4. **Outcomes matter more than outputs** (customer impact, reliability, time-to-market rather than features shipped or velocity).
5. **Context matters enormously** — a developer mentoring three juniors contributes enormous value that zero activity metrics capture.

**FR** — La controverse McKinsey (2023) a cristallise le debat sur la mesure de la productivite developpeur. Le consensus 2024-2026 : les metriques au niveau equipe sont valides (DORA), les metriques d'activite individuelle sont nefastes, les metriques perceptuelles sont essentielles, les resultats comptent plus que les sorties, et le contexte est determinant.

### The Developer Productivity Measurement Principles

Based on the debate and research consensus, adopt these principles:

1. **Never use metrics for individual ranking or performance reviews.** Metrics are for identifying systemic issues and team improvement opportunities.
2. **Always combine quantitative and qualitative data.** Numbers alone miss context. Surveys alone miss blind spots.
3. **Measure the system, not the people.** If a developer is slow, ask "what in our system is making this developer slow?" not "why is this developer underperforming?"
4. **Make metrics transparent.** Share all metrics with the team. Hidden metrics breed suspicion.
5. **Let teams choose their own improvement metrics.** The team decides which 3-5 SPACE metrics they want to focus on for the quarter.
6. **Accept that some valuable work is invisible to metrics.** Mentoring, knowledge sharing, architecture thinking, preventing bad decisions — these do not show up in any dashboard.

---

## Engineering OKRs

### Structuring Engineering OKRs

Engineering OKRs should focus on outcomes (improved capability, reduced friction, better reliability) rather than outputs (features shipped, story points completed).

**Example engineering OKRs:**

**Objective: Accelerate software delivery**
- KR1: Reduce median lead time for changes from 5 days to 2 days
- KR2: Increase deployment frequency from weekly to daily
- KR3: Reduce change failure rate from 12% to < 5%

**Objective: Improve developer experience**
- KR1: Increase developer satisfaction score from 3.2/5 to 4.0/5
- KR2: Reduce time-to-first-commit for new hires from 3 days to < 1 day
- KR3: Reduce CI build time from 25 minutes to < 10 minutes

**Objective: Strengthen engineering quality**
- KR1: Achieve 99.95% SLO compliance across all tier-1 services
- KR2: Reduce escaped defect rate from 5 per release to < 2 per release
- KR3: Increase code coverage of business-critical modules from 65% to 85%

**Objective: Build a self-service platform**
- KR1: 100% of production services registered in the developer portal with up-to-date ownership
- KR2: 80% of new services created using platform templates (golden paths)
- KR3: Reduce infrastructure ticket resolution time from 3 days to < 4 hours (self-service)

### OKR Anti-Patterns to Avoid

| Anti-pattern | Problem | Better alternative | FR |
|---|---|---|---|
| Output-based KRs ("Ship 15 features") | Incentivizes quantity over quality and impact | Outcome-based: "Increase user activation by 10%" | Basé sur les résultats, pas les sorties |
| Velocity as a KR ("Increase velocity by 20%") | Velocity inflation (bigger estimates, easier stories) | Cycle time or lead time reduction | Reduction du cycle time ou lead time |
| Individual developer KRs | Creates competition, discourages collaboration | Team-level KRs only | OKRs au niveau equipe uniquement |
| Too many KRs (> 5 per objective) | Dilutes focus, impossible to track meaningfully | 3-4 KRs per objective, 2-3 objectives per quarter | 3-4 KRs par objectif, 2-3 objectifs par trimestre |

**FR** — Les OKRs d'ingenierie doivent se concentrer sur les resultats (capacite amelioree, friction reduite, meilleure fiabilite) plutot que sur les sorties (features livrees, story points). Eviter les anti-patterns : KRs bases sur les sorties, velocite comme KR, KRs individuels, trop de KRs.

---

## Burndown & Velocity

### Velocity — What It Is and What It Is Not

**What velocity IS**: a planning tool that helps the team estimate how much work it can commit to in a sprint. It is the sum of story points completed in a sprint, averaged over the last 3-5 sprints.

**What velocity IS NOT**: a performance metric, a productivity measure, a basis for comparison between teams, or a KPI for management reporting.

**How to use velocity correctly:**
1. Track velocity over the last 3-5 sprints. Use the average (or range) to plan the next sprint's capacity.
2. If velocity is volatile (> 30% variation sprint over sprint), investigate: are stories poorly sized? Are there regular disruptions? Is the team composition changing?
3. Never commit to "increasing velocity." This leads to story point inflation and destroys the metric's utility.
4. When team composition changes, recalibrate. Velocity is team-specific and not transferable.

### Burndown Charts

**Sprint burndown**: shows remaining work (in story points or count) over the sprint duration. Use it in daily standups to track progress toward the sprint goal.

**Healthy patterns:**
- Gradual decline with daily progress
- Small plateaus (1-2 days) are normal when stories are in progress but not yet done

**Unhealthy patterns:**
- **Cliff pattern**: flat line for most of the sprint, then steep drop at the end. Indicates stories are too large or there is a "done" bottleneck.
- **Scope increase**: line goes up mid-sprint. Indicates scope creep or unplanned work being added.
- **No progress**: flat line. Indicates the team is blocked, stories are too complex, or the team is overcommitted.

### Release Burndown and Burnup

Prefer **burnup charts** over burndown for release tracking:
- Burnup shows both completed work (rising line) and total scope (potentially rising line), making scope changes visible
- Burndown hides scope changes — the chart moves left if scope is added, making it appear that progress is being made when it is not

**FR** — La velocite est un outil de planification, pas une metrique de performance. Ne jamais la comparer entre equipes ni chercher a l'augmenter. Utiliser les burndown charts dans les standups quotidiens. Preferer les burnup charts pour le suivi de release car ils rendent les changements de scope visibles.

---

## Engineering Intelligence Platforms

### Platform Comparison (2024-2026)

| Platform | Focus | Data Sources | Strengths | Weaknesses | FR |
|---|---|---|---|---|---|
| **LinearB** | Engineering metrics, workflow automation | Git, CI/CD, issue trackers | Strong DORA metrics, PR workflow insights, gitStream automation | Can feel surveillance-like if not introduced carefully | Metriques DORA, automatisation de workflow |
| **Jellyfish** | Engineering alignment with business | Git, Jira, HR systems | Maps engineering effort to business initiatives, executive dashboards | Enterprise pricing, heavy implementation | Alignement ingenierie-business |
| **DX (getdx.com)** | Developer experience measurement | Surveys + system metrics | Validated survey instruments (DX Core 4), research-backed, benchmarking | Survey-focused, less system automation | Mesure de l'experience developpeur |
| **Swarmia** | Engineering productivity, investment tracking | Git, CI/CD, Slack, Jira | Working agreements, investment balance (features vs debt vs support), team-level focus | Smaller company, fewer enterprise features | Productivite, suivi de l'investissement |
| **Sleuth** | DORA metrics, deploy tracking | Git, CI/CD, feature flags, incident tools | Focused on DORA, lightweight setup, good deploy visibility | Narrower scope than full platforms | Focus DORA, tracking de deploiement |
| **Pluralsight Flow (ex-GitPrime)** | Engineering analytics | Git | Deep git analytics, code review insights | Acquired by Pluralsight, future uncertain. Prone to individual-level measurement misuse | Analytiques git approfondies |
| **Faros AI** | Open-source engineering intelligence | Configurable connectors to 50+ tools | Open-source core, self-hostable, highly customizable | Requires engineering effort to deploy and maintain | Open-source, auto-hebergeable |

### Implementation Guidance

1. **Start with DORA**: before adopting any platform, manually measure the four DORA metrics using existing CI/CD and git data. If the organization cannot measure DORA manually, it is not ready for a platform.
2. **Add DX surveys**: adopt DX Core 4 or a custom quarterly survey. This provides the perceptual layer that system metrics miss.
3. **Evaluate platforms for team improvement, not management reporting**: the primary user of an engineering intelligence platform should be the engineering team itself, not the VP of Engineering.
4. **Roll out transparently**: announce what is being measured, why, and how it will be used. Commit publicly that metrics will never be used for individual evaluation.
5. **Start with one team**: pilot with a willing team for 2-3 months. Validate that the platform provides actionable insights. Scale only after proven value.

**FR** — Commencer par mesurer DORA manuellement avant d'adopter une plateforme. Ajouter des enquetes DX. Evaluer les plateformes pour l'amelioration d'equipe, pas le reporting management. Deployer de maniere transparente. Piloter avec une equipe volontaire pendant 2-3 mois avant de generaliser.

---

## Building an Engineering Metrics Program

### Step-by-Step Implementation

**Month 1 — Foundations**
1. Form a small working group (2-3 engineers + 1 engineering manager) to design the metrics program.
2. Select 4-6 metrics across at least 3 SPACE dimensions. Include at least 1 perceptual metric (survey) and 3 system metrics.
3. Establish baselines: measure current values for all selected metrics.
4. Create a simple dashboard (Grafana, Looker, or even a spreadsheet for the first iteration).
5. Run the first DX survey to establish a satisfaction baseline.

**Month 2 — Visibility**
1. Share the dashboard with all engineering teams. Explain each metric: what it measures, why it matters, and how to interpret it.
2. Include metrics review in sprint retrospectives. Ask "what does this trend tell us?" not "why is this number bad?"
3. Identify the top 2-3 bottlenecks based on the data (e.g., slow PR reviews, slow CI, long wait times).
4. Define improvement experiments: "We hypothesize that auto-assigning PR reviewers will reduce review time from 24 hours to 4 hours."

**Month 3-6 — Improvement Cycles**
1. Run improvement experiments with clear hypotheses and success criteria.
2. Measure impact: did the experiment improve the target metric? Were there unintended side effects?
3. Share results (successes and failures) with all teams. Create a culture of data-driven improvement.
4. Gradually expand the metrics program: add more teams, refine metrics, evaluate engineering intelligence platforms.

**Ongoing — Sustain and Evolve**
1. Run quarterly DX surveys. Compare results over time.
2. Review and refresh metrics annually. Retire metrics that no longer provide actionable insights.
3. Calibrate targets: as the team improves, raise the bar. An "elite" DORA team should set new challenges.
4. Invest in the tooling: as the metrics program matures, adopt an engineering intelligence platform to automate data collection and visualization.

### Metrics Program Anti-Patterns

| Anti-pattern | Consequence | Prevention | FR |
|---|---|---|---|
| **Measuring everything** | Dashboard overload, no actionable insights | Limit to 4-6 key metrics. Add more only when existing ones are consistently used | Limiter a 4-6 metriques cles |
| **Top-down metric mandates** | Teams game the metrics, lose trust | Let teams participate in metric selection | Laisser les equipes participer a la selection |
| **Ignoring context** | Misinterpretation (e.g., "team X has lower velocity" without knowing they are refactoring) | Always discuss metrics in context during retros | Toujours discuter les metriques en contexte |
| **Metric fixation** | Optimizing for the metric rather than the underlying goal (Goodhart's Law) | Rotate focus metrics quarterly, use multiple dimensions | Alterner les metriques focus, utiliser plusieurs dimensions |
| **No action from data** | Metrics become wallpaper; cynicism grows | Every metrics review must produce at least one improvement experiment | Chaque revue de metriques doit produire un experiment d'amelioration |

**FR** — Construire un programme de metriques en 6 mois : mois 1 — fondations (selectionner 4-6 metriques, etablir les baselines), mois 2 — visibilite (dashboard partage, revue en retro), mois 3-6 — cycles d'amelioration (experiments avec hypotheses et criteres de succes). Eviter les anti-patterns : tout mesurer, mandats top-down, ignorer le contexte, fixation sur les metriques, absence d'action.

---

## References

- Nicole Forsgren, Jez Humble, Gene Kim, *Accelerate: The Science of Lean Software and DevOps* (2018)
- Forsgren, Storey, Maddila, Zimmermann, Houck, *The SPACE of Developer Productivity* (ACM Queue, 2021)
- Abi Noda, Margaret-Anne Storey et al., *DevEx: What Actually Drives Productivity* (ACM Queue, 2023)
- *State of DevOps Report* — DORA / Google Cloud (annual, 2014-2025)
- Kent Beck & Gergely Orosz, *Measuring Developer Productivity: Real-World Examples* (2023)
- Daniel Vacanti, *Actionable Agile Metrics for Predictability* (2015)
- Daniel Vacanti, *When Will It Be Done?* (2020)
- Don Reinertsen, *The Principles of Product Development Flow* (2009)
- DORA — dora.dev
- DX Core 4 — getdx.com
- LinearB — linearb.io
- Jellyfish — jellyfish.co
- Swarmia — swarmia.com
- Sleuth — sleuth.io
- Faros AI — faros.ai (open-source engineering intelligence)
