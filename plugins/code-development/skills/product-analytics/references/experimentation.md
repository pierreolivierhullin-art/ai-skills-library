# Experimentation & A/B Testing / Expérimentation & A/B Testing

Référence approfondie sur la conception d'expériences, le calcul de taille d'échantillon, la significativité statistique, l'analyse bayésienne vs fréquentiste, les bandits multi-bras, les plateformes d'expérimentation, et les guardrail metrics.

Deep-dive reference on experiment design, sample size calculation, statistical significance & power analysis, Bayesian vs frequentist analysis, multi-armed bandits, experimentation platforms, and guardrail metrics.

---

## Table of Contents

1. [Experiment Design Fundamentals](#experiment-design-fundamentals)
2. [Statistical Foundations](#statistical-foundations)
3. [Sample Size Calculation](#sample-size-calculation)
4. [Bayesian vs Frequentist Approaches](#bayesian-vs-frequentist-approaches)
5. [Sequential Testing & Peeking](#sequential-testing--peeking)
6. [Multi-Armed Bandits](#multi-armed-bandits)
7. [Advanced Techniques](#advanced-techniques)
8. [Experimentation Platforms](#experimentation-platforms)
9. [Guardrail Metrics](#guardrail-metrics)
10. [Experiment Lifecycle & Governance](#experiment-lifecycle--governance)

---

## Experiment Design Fundamentals

### The Hypothesis / L'hypothèse

Every experiment begins with a written hypothesis. Use this template:

**"If we [change], then [metric] will [direction] by [minimum expected effect] because [rationale]."**

Examples:
- "If we add social proof badges to the product page, then add-to-cart rate will increase by 5% because users will feel more confident in their purchase decision."
- "If we simplify the onboarding flow from 5 steps to 3, then Day-7 retention will increase by 3 percentage points because users will reach the aha moment faster."

Chaque expérience commence par une hypothèse écrite. Template : "Si nous [changement], alors [métrique] va [direction] de [effet minimum attendu] parce que [justification]."

### Experiment Components / Composants d'une expérience

| Component | Description | Example |
|---|---|---|
| **Hypothesis** | What you believe will happen and why | "Simplified checkout increases conversion by 8%" |
| **Primary metric** | The metric the experiment is designed to move | Checkout conversion rate |
| **Secondary metrics** | Additional metrics to monitor for full picture | Revenue per visitor, average order value |
| **Guardrail metrics** | Metrics that must not degrade | Page load time, error rate, overall revenue |
| **Variants** | Control (A) and treatment(s) (B, C, ...) | A = current 5-step checkout, B = 3-step checkout |
| **Randomization unit** | The entity being randomized | User ID (most common), session, device |
| **Traffic allocation** | Percentage of traffic per variant | 50/50, 80/10/10 for multi-variant |
| **Sample size** | Required participants per variant | 12,500 per variant (from power analysis) |
| **Duration** | Expected runtime to reach sample size | 14 days (must cover full business cycles) |
| **Targeting** | Who is included in the experiment | New users only, US market, mobile web |

### Randomization / Randomisation

Assign users to variants using a deterministic hash-based randomization:

```python
import hashlib

def get_variant(user_id: str, experiment_id: str, num_variants: int = 2) -> int:
    """Deterministic variant assignment using hash.
    Returns variant index (0 = control, 1+ = treatment)."""
    hash_input = f"{experiment_id}:{user_id}".encode('utf-8')
    hash_value = int(hashlib.sha256(hash_input).hexdigest(), 16)
    return hash_value % num_variants
```

Benefits of hash-based assignment:
- **Deterministic**: Same user always gets the same variant (no flickering).
- **Server-side**: Assignment happens server-side, not client-side (no FOOC — Flash of Original Content).
- **Stateless**: No database lookup needed; can be computed on any request.

Utiliser une randomisation déterministe basée sur le hash. Avantages : déterministe (pas de flickering), server-side (pas de FOOC), stateless (pas de lookup BDD).

### What to Test / Quoi tester

Prioritize experiments using the ICE framework:

- **Impact**: How much will this move the primary metric if it wins?
- **Confidence**: How confident are we that this will work (based on research, qualitative data)?
- **Ease**: How easy is it to implement and run this experiment?

Score each from 1-10. Prioritize by ICE score = (Impact + Confidence + Ease) / 3.

Prioriser les expériences avec le framework ICE : Impact, Confidence, Ease. Score de 1 à 10 chacun.

---

## Statistical Foundations

### Frequentist Framework / Framework fréquentiste

The traditional approach to A/B testing. In the frequentist framework:

- **Null hypothesis (H0)**: There is no difference between control and treatment.
- **Alternative hypothesis (H1)**: There is a difference (typically: treatment > control).
- **p-value**: The probability of observing the measured effect (or more extreme) if H0 is true. A low p-value (< 0.05) means the result is unlikely under H0, so we reject H0.
- **Significance level (alpha)**: The threshold for the p-value, typically 0.05 (5% false positive rate).
- **Statistical power (1 - beta)**: The probability of correctly detecting a true effect. Typically set at 0.80 (80%) or 0.90 (90%).
- **Confidence interval**: The range within which the true effect likely falls (e.g., "conversion increased by 3.2%, 95% CI [1.1%, 5.3%]").

Framework fréquentiste : H0 (pas de différence), H1 (il y a une différence). p-value < 0.05 pour rejeter H0. Puissance statistique typiquement 80%. Intervalle de confiance pour encadrer l'effet réel.

### Key Concepts / Concepts clés

**Type I Error (False Positive / Faux positif)**: Concluding there is an effect when there is none. Controlled by alpha (significance level). At alpha = 0.05, you accept a 5% chance of false positives.

**Type II Error (False Negative / Faux négatif)**: Missing a real effect. Controlled by power (1 - beta). At power = 0.80, you accept a 20% chance of missing a real effect.

**Minimum Detectable Effect (MDE)**: The smallest effect size you want to reliably detect. Smaller MDE requires larger sample sizes. Choose MDE based on business impact: what is the smallest improvement worth detecting?

**Multiple Testing Problem**: Running 20 tests at alpha = 0.05 means you expect 1 false positive by chance. Apply Bonferroni correction (alpha / number_of_tests) or use False Discovery Rate (FDR) control when analyzing multiple metrics or segments.

MDE = plus petit effet à détecter de façon fiable. Un MDE plus petit nécessite plus de participants. Problème de tests multiples : appliquer la correction de Bonferroni ou le contrôle FDR.

---

## Sample Size Calculation

### Formula / Formule

For a two-proportion z-test (comparing two conversion rates):

```
n = (Z_alpha/2 + Z_beta)^2 * (p1*(1-p1) + p2*(1-p2)) / (p2 - p1)^2

Where:
- n = sample size per variant
- Z_alpha/2 = z-score for significance level (1.96 for alpha=0.05 two-sided)
- Z_beta = z-score for power (0.84 for 80% power, 1.28 for 90%)
- p1 = baseline conversion rate (control)
- p2 = expected conversion rate (treatment) = p1 * (1 + MDE_relative)
```

### Practical Examples / Exemples pratiques

| Baseline Rate | Relative MDE | Absolute MDE | Power | Sample per Variant | Total Sample |
|---|---|---|---|---|---|
| 5% | 10% | 0.5pp | 80% | 31,234 | 62,468 |
| 5% | 20% | 1.0pp | 80% | 8,118 | 16,236 |
| 10% | 5% | 0.5pp | 80% | 69,464 | 138,928 |
| 10% | 10% | 1.0pp | 80% | 17,574 | 35,148 |
| 20% | 5% | 1.0pp | 80% | 38,416 | 76,832 |
| 30% | 5% | 1.5pp | 80% | 26,668 | 53,336 |

### Duration Estimation / Estimation de durée

```
Duration (days) = Total Sample Size / (Daily Traffic * Percentage Allocated to Experiment)

Example:
- Need 62,468 total users
- 5,000 users/day visit the relevant page
- 100% allocated to experiment
→ Duration = 62,468 / 5,000 = ~13 days

Round up to cover at least 1-2 full business cycles (weekdays + weekends).
```

**Rule of thumb / Règle empirique**: Always run experiments for at least 7 days (1 full week cycle) even if sample size is reached earlier. This accounts for day-of-week effects.

Toujours faire tourner les expériences au moins 7 jours (1 cycle semaine complet) même si la taille d'échantillon est atteinte avant.

### Sample Size Calculator (Python) / Calculateur de taille d'échantillon

```python
from scipy import stats
import math

def sample_size_two_proportions(
    baseline_rate: float,
    mde_relative: float,
    alpha: float = 0.05,
    power: float = 0.80,
    two_sided: bool = True,
) -> int:
    """Calculate required sample size per variant for a two-proportion z-test.

    Args:
        baseline_rate: Current conversion rate (e.g., 0.05 for 5%)
        mde_relative: Minimum detectable effect as relative change (e.g., 0.10 for 10% relative lift)
        alpha: Significance level (default 0.05)
        power: Statistical power (default 0.80)
        two_sided: Whether the test is two-sided (default True)

    Returns:
        Required sample size per variant (integer, rounded up)
    """
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde_relative)

    if two_sided:
        z_alpha = stats.norm.ppf(1 - alpha / 2)
    else:
        z_alpha = stats.norm.ppf(1 - alpha)

    z_beta = stats.norm.ppf(power)

    numerator = (z_alpha + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))
    denominator = (p2 - p1) ** 2

    n = math.ceil(numerator / denominator)
    return n

# Example usage
n = sample_size_two_proportions(baseline_rate=0.05, mde_relative=0.10)
print(f"Required sample per variant: {n:,}")  # ~31,234
print(f"Total sample needed: {n * 2:,}")      # ~62,468
```

---

## Bayesian vs Frequentist Approaches

### Frequentist Recap / Résumé fréquentiste

- Answers: "What is the probability of seeing this data if there is no effect?"
- Outputs a p-value and confidence interval.
- Requires pre-determined sample size; stopping early inflates false positives.
- Binary decision: "significant" or "not significant."
- Pros: Well-understood, widely accepted, reproducible.
- Cons: Unintuitive (p-value is not "probability of hypothesis being true"), rigid fixed-horizon requirement.

Répond à "Quelle est la probabilité d'observer ces données s'il n'y a pas d'effet?" Sortie : p-value et IC. Nécessite une taille d'échantillon pré-déterminée.

### Bayesian Approach / Approche bayésienne

- Answers: "What is the probability that variant B is better than variant A, given the observed data?"
- Outputs a posterior probability distribution and credible intervals.
- Naturally handles "peeking" — the posterior updates continuously without inflation.
- Provides business-friendly outputs: "There is a 94% probability that B is better than A, with an expected lift of 3.2% [1.1%, 5.8%]."
- Requires specifying a prior distribution (can be uninformative).
- Pros: Intuitive interpretation, allows continuous monitoring, quantifies probability of each variant winning.
- Cons: Prior selection can influence results, computationally heavier, less standardized.

Répond à "Quelle est la probabilité que B soit meilleur que A, étant donné les données observées?" Distribution postérieure et intervalles crédibles. Gère naturellement le peeking. Résultats business-friendly.

### When to Use Which / Quand utiliser lequel

| Situation | Recommended Approach |
|---|---|
| Regulated industry, need to justify to auditors | Frequentist (gold standard) |
| Fast iteration, need quick directional signal | Bayesian |
| Large sample, can wait for fixed horizon | Frequentist |
| Small sample, want to peek without penalty | Bayesian |
| Multiple variants (A/B/C/D) | Bayesian (natural handling) |
| Team is non-technical, needs intuitive results | Bayesian (probability statements) |
| Academic publication, peer review | Frequentist |
| Platform default (Statsig, Eppo) | Often frequentist with sequential testing |
| Platform default (VWO, Dynamic Yield) | Often Bayesian |

### Bayesian A/B Test (Python) / Test A/B bayésien

```python
import numpy as np
from scipy import stats

def bayesian_ab_test(
    visitors_a: int, conversions_a: int,
    visitors_b: int, conversions_b: int,
    prior_alpha: float = 1.0, prior_beta: float = 1.0,
    num_simulations: int = 100_000,
) -> dict:
    """Run a Bayesian A/B test using Beta-Binomial conjugate model.

    Args:
        visitors_a, conversions_a: Control group data
        visitors_b, conversions_b: Treatment group data
        prior_alpha, prior_beta: Beta prior parameters (1,1 = uniform prior)
        num_simulations: Number of Monte Carlo samples

    Returns:
        Dictionary with probability of B > A, expected lift, and credible interval
    """
    # Posterior distributions (Beta-Binomial conjugate)
    posterior_a = stats.beta(
        prior_alpha + conversions_a,
        prior_beta + visitors_a - conversions_a
    )
    posterior_b = stats.beta(
        prior_alpha + conversions_b,
        prior_beta + visitors_b - conversions_b
    )

    # Monte Carlo simulation
    samples_a = posterior_a.rvs(num_simulations)
    samples_b = posterior_b.rvs(num_simulations)

    # Probability that B > A
    prob_b_wins = (samples_b > samples_a).mean()

    # Expected lift
    lift_samples = (samples_b - samples_a) / samples_a
    expected_lift = lift_samples.mean()

    # 95% credible interval for lift
    ci_lower = np.percentile(lift_samples, 2.5)
    ci_upper = np.percentile(lift_samples, 97.5)

    return {
        "prob_b_wins": prob_b_wins,
        "expected_lift": expected_lift,
        "ci_95_lower": ci_lower,
        "ci_95_upper": ci_upper,
        "rate_a": conversions_a / visitors_a,
        "rate_b": conversions_b / visitors_b,
    }

# Example usage
result = bayesian_ab_test(
    visitors_a=10000, conversions_a=500,   # 5.0% conversion
    visitors_b=10000, conversions_b=540,   # 5.4% conversion
)
print(f"P(B > A) = {result['prob_b_wins']:.1%}")
print(f"Expected lift = {result['expected_lift']:.1%}")
print(f"95% CI = [{result['ci_95_lower']:.1%}, {result['ci_95_upper']:.1%}]")
# P(B > A) = 93.2%
# Expected lift = 8.1%
# 95% CI = [-0.8%, 17.5%]
```

---

## Sequential Testing & Peeking

### The Peeking Problem / Le problème du peeking

Checking experiment results before the pre-determined sample size is reached (and stopping when p < 0.05) dramatically inflates the false positive rate. A test designed for alpha = 0.05 can have an effective alpha of 30%+ with frequent peeking. This is the single most common mistake in A/B testing.

Vérifier les résultats avant la taille d'échantillon prédéterminée et arrêter quand p < 0.05 gonfle dramatiquement le taux de faux positifs. Erreur la plus courante en A/B testing.

### Solutions / Solutions

**1. Always Valid p-values (mSPRT / mixture Sequential Probability Ratio Test)**:
Use a sequential testing framework that produces p-values valid at any stopping time. The p-value is adjusted for peeking. Used by Optimizely and Statsig.

**2. Group Sequential Design**:
Pre-define a limited number of "looks" (e.g., 5 interim analyses) with adjusted significance boundaries (O'Brien-Fleming or Pocock spending functions). Stop early only if the effect crosses the adjusted boundary.

**3. Bayesian Continuous Monitoring**:
In the Bayesian framework, the posterior is always valid regardless of when you look. Define a decision rule: "Ship if P(B > A) > 95% and expected loss < 0.1%." Check as often as needed.

**4. CUPED (Controlled-experiment Using Pre-Experiment Data)**:
Use pre-experiment data as a covariate to reduce variance. With lower variance, experiments reach significance faster (sometimes 50% faster). Implemented by Microsoft, Statsig, Eppo.

p-values toujours valides (mSPRT), plans séquentiels de groupe, monitoring bayésien continu, CUPED pour réduire la variance.

---

## Multi-Armed Bandits

### Concept / Concept

Multi-armed bandits (MAB) dynamically allocate more traffic to winning variants, optimizing cumulative reward during the experiment. Unlike A/B tests where traffic is split evenly for the entire duration, bandits adapt the allocation as data comes in.

Les bandits multi-bras allouent dynamiquement plus de trafic aux variantes gagnantes, optimisant la récompense cumulative pendant l'expérience.

### Algorithms / Algorithmes

| Algorithm | Description | Pros | Cons |
|---|---|---|---|
| **Epsilon-Greedy** | Exploit best variant (1-epsilon)% of the time, explore randomly epsilon% | Simple to implement | Fixed exploration rate, not optimal |
| **Thompson Sampling** | Sample from posterior distribution, play the variant with highest sample | Bayesian, adaptive, strong theoretical guarantees | Requires probabilistic modeling |
| **Upper Confidence Bound (UCB)** | Play the variant with highest upper confidence bound | No parameters to tune, optimistic exploration | Frequentist, less intuitive |
| **Contextual Bandits** | Consider user features (context) when selecting variants | Personalized optimization | Complex, requires feature engineering |

### When to Use Bandits vs A/B Tests / Quand utiliser bandits vs A/B tests

| Criterion | A/B Test | Multi-Armed Bandit |
|---|---|---|
| **Goal** | Learn the truth (causal inference) | Maximize cumulative conversions |
| **Statistical rigor** | High (unbiased estimates) | Lower (biased toward early winners) |
| **Duration** | Fixed, pre-determined | Adaptive, can run indefinitely |
| **Best for** | Feature launches, major product decisions | Headlines, recommendations, UI copy |
| **Regret** | Higher (equal traffic to losing variant) | Lower (shifts traffic away from losers) |
| **Interpretability** | Easy to explain and report | Harder to explain to non-technical stakeholders |

**Recommendation / Recommandation**: Use A/B tests for strategic product decisions where you need unbiased causal estimates. Use bandits for optimization tasks where cumulative reward matters more than inference (e.g., headline testing, ad copy, recommendation algorithms).

Utiliser les A/B tests pour les décisions stratégiques nécessitant des estimations causales non biaisées. Utiliser les bandits pour l'optimisation où la récompense cumulative compte plus que l'inférence.

---

## Advanced Techniques

### CUPED Variance Reduction

CUPED (Controlled-experiment Using Pre-Experiment Data) uses pre-experiment metrics as covariates to reduce variance in the treatment effect estimate. This can reduce the required sample size by 30-50%.

```python
# Simplified CUPED implementation
import numpy as np

def cuped_adjustment(
    metric_values: np.ndarray,       # Y: metric during experiment
    pre_experiment_values: np.ndarray, # X: same metric before experiment
) -> np.ndarray:
    """Apply CUPED variance reduction.
    Returns adjusted metric values with lower variance."""
    theta = np.cov(metric_values, pre_experiment_values)[0, 1] / np.var(pre_experiment_values)
    adjusted = metric_values - theta * (pre_experiment_values - np.mean(pre_experiment_values))
    return adjusted
```

CUPED utilise les métriques pré-expérience comme covariables pour réduire la variance. Peut réduire la taille d'échantillon requise de 30-50%.

### Interleaving Experiments

For ranking and recommendation systems, interleaving merges results from two algorithms into a single ranked list and measures which algorithm's results the user prefers (based on clicks, engagement). Much more sensitive than A/B tests for ranking changes — requires 10-100x fewer samples.

Pour les systèmes de ranking et recommandation, l'interleaving fusionne les résultats de deux algorithmes en une seule liste et mesure la préférence utilisateur. 10-100x plus sensible que les A/B tests pour les changements de ranking.

### Long-term Holdouts

Reserve a small percentage (1-5%) of users who never see any experiment treatment (permanent control). Compare their metrics against the general population quarterly to measure the cumulative impact of all shipped experiments. This answers: "Is our experimentation program actually improving the product over time?"

Réserver 1-5% d'utilisateurs qui ne voient jamais de traitement expérimental (contrôle permanent). Comparer trimestriellement pour mesurer l'impact cumulé de toutes les expériences.

### Heterogeneous Treatment Effects (HTE)

Not all users respond the same way to a treatment. Use causal forest, meta-learners (T-learner, S-learner, X-learner), or subgroup analysis to identify which user segments benefit most (or are harmed) by the change. Eppo and Statsig offer built-in HTE analysis.

Tous les utilisateurs ne réagissent pas de la même façon. Utiliser causal forest, meta-learners, ou analyse de sous-groupes pour identifier les segments qui bénéficient le plus du changement.

### Switchback Experiments

For marketplace or supply-constrained experiments where user-level randomization creates interference (e.g., a pricing change affects both buyers and sellers), use switchback experiments: alternate between treatment and control over time periods (e.g., hours or days) within geographic regions.

Pour les expériences marketplace où la randomisation utilisateur crée des interférences, utiliser des expériences switchback : alterner entre traitement et contrôle sur des périodes temporelles dans des régions géographiques.

---

## Experimentation Platforms

### Platform Comparison / Comparaison des plateformes

| Platform | Type | Strengths | Best For |
|---|---|---|---|
| **Statsig** | Cloud, warehouse-native | Pulse metrics system, CUPED, automated analysis, warehouse-native experiments | High-velocity teams, data-driven companies |
| **Eppo** | Cloud, warehouse-native | Warehouse-native (computes on your data), CUPED, HTE, rigorous stats | Teams with mature data warehouses |
| **LaunchDarkly** | Cloud | Best-in-class feature flags, SDKs for every language, targeting rules | Feature flag-first teams, progressive rollouts |
| **Optimizely** | Cloud | Full stack + Web, visual editor, Stats Engine (sequential testing) | Marketing teams, client-side experiments |
| **PostHog** | Cloud/Self-hosted | Open-source, integrated with analytics + feature flags + session replay | Startups, privacy-conscious, all-in-one |
| **GrowthBook** | Open-source | Free, Bayesian engine, warehouse-native, Segment integration | Budget-conscious, self-hosted |
| **VWO** | Cloud | Visual editor, Bayesian stats, heatmaps | Marketing-led experimentation |
| **Split.io** | Cloud | Feature flags + experimentation, attribution | Enterprise feature delivery |
| **Flagship.io** | Cloud (FR-based) | RGPD-compliant by design, server-side focus | European companies, RGPD-sensitive contexts |

### Architecture Patterns / Patterns d'architecture

**Client-side experiment assignment**:
- Variant assigned in the browser/app via JavaScript SDK.
- Faster to set up but subject to FOOC (Flash of Original Content).
- Suitable for UI-only changes (copy, colors, layout).

**Server-side experiment assignment**:
- Variant assigned on the server before rendering.
- No FOOC, consistent experience, works for backend logic changes.
- Recommended for critical experiments (pricing, algorithms, features).

**Warehouse-native experiments (Eppo, Statsig)**:
- Experiment assignment logged as events; analysis runs directly on the warehouse.
- No data leaves the warehouse; full SQL access to experiment data.
- Best for teams with strong data engineering and a mature warehouse.

Assignment client-side pour les changements UI simples. Assignment server-side pour les expériences critiques (pas de FOOC). Warehouse-native pour les équipes avec un warehouse mature.

---

## Guardrail Metrics

### Definition / Définition

Guardrail metrics are metrics that an experiment must not degrade, regardless of whether the primary metric improves. They protect against unintended negative consequences. Always define guardrails before starting an experiment.

Les guardrail metrics sont des métriques qu'une expérience ne doit pas dégrader. Elles protègent contre les conséquences négatives non intentionnelles. Toujours les définir avant de démarrer.

### Common Guardrail Metrics / Guardrails courants

| Category | Guardrail Metric | Threshold |
|---|---|---|
| **Performance** | Page load time (p95) | Must not increase by > 100ms |
| **Stability** | Client-side error rate | Must not increase by > 0.5pp |
| **Engagement** | Session length | Must not decrease by > 5% |
| **Revenue** | Revenue per user (RPU) | Must not decrease (any amount) |
| **Retention** | Day-7 retention | Must not decrease by > 1pp |
| **Trust** | Support ticket rate | Must not increase by > 10% |
| **Compliance** | Data collection errors | Must remain at 0 |

### Guardrail Decision Framework / Framework de décision guardrails

```
Experiment results:
├── Primary metric UP, Guardrails OK → SHIP ✓
├── Primary metric UP, Guardrail DEGRADED → INVESTIGATE
│   ├── Guardrail degradation within tolerance? → Ship with monitoring
│   └── Guardrail degradation significant? → DO NOT SHIP, iterate
├── Primary metric FLAT, Guardrails OK → DO NOT SHIP (no value)
└── Primary metric DOWN → DO NOT SHIP, learn from failure
```

---

## Experiment Lifecycle & Governance

### Experiment Lifecycle / Cycle de vie d'une expérience

1. **Ideation**: Identify opportunity from data analysis, user research, or qualitative feedback. Score with ICE framework.

2. **Design**: Write hypothesis, define primary/secondary/guardrail metrics, calculate sample size, determine duration, document in an experiment brief.

3. **Review**: Peer review the experiment design. Check: Is the hypothesis falsifiable? Is the sample size adequate? Are guardrails defined? Is the randomization correct?

4. **Implementation**: Implement the variant behind a feature flag. QA the variant in staging. Verify tracking fires correctly.

5. **Launch**: Ramp traffic gradually (1% → 10% → 50%). Monitor guardrails during ramp-up. Full deployment once guardrails are stable.

6. **Analysis**: Wait for the pre-determined sample size/duration. Analyze primary, secondary, and guardrail metrics. Check for segment-level effects.

7. **Decision**: Ship, iterate, or kill based on results and guardrails. Document the decision and rationale.

8. **Cleanup**: Remove the losing variant code and feature flag. Update documentation. Share learnings with the organization.

Cycle de vie : idéation, conception, review, implémentation, lancement (rampe graduelle), analyse, décision, nettoyage.

### Experiment Brief Template / Template de brief d'expérience

```markdown
# Experiment: [Name]

## Hypothesis
If we [change], then [metric] will [direction] by [MDE] because [rationale].

## Metrics
- **Primary**: [metric name] (baseline: X%, MDE: Y%)
- **Secondary**: [metric 1], [metric 2]
- **Guardrails**: [metric 1] must not degrade by > Z%

## Design
- **Variants**: Control (current), Treatment (description of change)
- **Randomization unit**: User ID
- **Traffic allocation**: 50/50
- **Sample size**: N per variant (power analysis link)
- **Duration**: X days (minimum 7 days)
- **Targeting**: [All users / specific segment]

## Implementation
- Feature flag: `experiment_simplified_checkout`
- Tracking events: [list events]
- PR: [link]

## Results
[To be filled after analysis]
- Primary metric: X% → Y% (p=Z, 95% CI [a, b])
- Guardrails: All passed / [details]

## Decision
[Ship / Iterate / Kill] — [rationale]
```

### Experiment Review Board / Comité de revue d'expériences

For organizations running 10+ experiments simultaneously, establish an experiment review board that meets weekly to:
- Review new experiment proposals (hypothesis, design, sample size).
- Check for interaction effects between concurrent experiments.
- Review completed experiment results and approve ship/kill decisions.
- Track the overall experiment velocity and win rate.
- Maintain an experiment log with learnings for institutional knowledge.

Pour les organisations avec 10+ expériences simultanées, établir un comité de revue hebdomadaire : revue des propositions, vérification des interactions entre expériences, revue des résultats, suivi de la vélocité et du taux de victoire.
