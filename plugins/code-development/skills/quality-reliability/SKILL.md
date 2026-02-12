---
name: quality-reliability
description: This skill should be used when the user asks about "QA automation", "test automation", "SRE", "site reliability engineering", "chaos engineering", "performance testing", "load testing", "reliability", "incident management", "quality gates", "visual regression", "Playwright", "Cypress", "automatisation QA", "automatisation de tests", "ingénierie de fiabilité", "tests de performance", "tests de charge", "fiabilité", "gestion des incidents", "portes qualité", "régression visuelle", "Jest", "Vitest", "Testing Library", "Selenium", "k6", "Artillery", "Gatling", "JMeter", "stress testing", "soak testing", "end-to-end testing", "E2E", "smoke testing", "canary testing", "feature flags testing", "contract testing", "Pact", "error budget", "SLO", "toil reduction", "chaos monkey", "game days", or needs guidance on software quality assurance and site reliability engineering.
version: 1.1.0
last_updated: 2026-02
---

# Quality & Reliability — QA Automation, SRE, Chaos Engineering & Performance Testing

## Overview

**FR** — Cette skill couvre les pratiques modernes de qualite logicielle et de fiabilite des systemes : automatisation des tests, strategie risk-based, regression visuelle, tests de performance, principes SRE (Google SRE Book), chaos engineering et processus qualite. L'objectif est de construire un systeme ou la confiance dans chaque release repose sur des preuves automatisees, ou la resilience est validee par des experiences controlees, et ou la fiabilite est pilotee par des metriques centrees sur l'utilisateur. Recommandations alignees avec les pratiques 2024-2026 : Playwright comme standard e2e, shift-left testing, AI-powered testing, platform reliability engineering, chaos engineering comme pratique standard.

**EN** — This skill covers modern software quality and system reliability: test automation, risk-based test strategy, visual regression, performance testing, SRE principles (Google SRE Book), chaos engineering, and quality processes. The goal is to build a system where release confidence is based on automated evidence, resilience is validated through controlled experiments, and reliability is driven by user-centric metrics. Aligned with 2024-2026 best practices: Playwright as e2e standard, shift-left testing, AI-powered testing, platform reliability engineering, chaos engineering as standard practice.

---

## When This Skill Applies

Activate this skill when the user / Activer cette skill quand l'utilisateur :

- Designs or implements a test automation strategy (Playwright, Cypress, Selenium)
- Defines a test strategy, test pyramid, or risk-based testing approach
- Sets up visual regression testing (Percy, Chromatic, Argos, Playwright screenshots)
- Implements API testing or contract testing (Pact, REST Assured, k6)
- Plans or executes load testing, stress testing, or performance benchmarking (k6, JMeter, Gatling, Locust)
- Optimizes frontend performance (Lighthouse, Core Web Vitals, SpeedCurve) or defines performance budgets
- Applies SRE principles: SLOs, error budgets, toil reduction, capacity planning
- Implements chaos engineering (Chaos Monkey, Gremlin, Litmus) or plans Game Days
- Designs quality processes: bug triage, quality gates, release readiness reviews
- Measures quality metrics: defect density, escape rate, test coverage, flaky test rate
- Implements resilience patterns: circuit breaker, bulkhead, retry with backoff

---

## Core Principles

### 1. Shift-Left Everything / Tout decaler a gauche

Integrer la qualite le plus tot possible dans le cycle de developpement. Chaque PR doit executer automatiquement : analyse statique, tests unitaires, integration, regression visuelle et smoke tests e2e. Detecter les defauts au stade le moins couteux. Investir dans les quality gates automatises plutot que la validation manuelle pre-release. / Integrate quality as early as possible. Every PR must automatically run static analysis, unit tests, integration tests, visual regression, and e2e smoke tests. Invest in automated quality gates over manual pre-release validation.

### 2. Playwright as the E2E Standard / Playwright comme standard E2E

Adopter Playwright comme framework par defaut pour tout nouveau projet e2e. Son auto-waiting natif elimine la flakiness, son support multi-navigateurs (Chromium, Firefox, WebKit) couvre le spectre complet, et ses contextes de navigateur garantissent l'isolation. L'utiliser pour le testing UI, API, composants et regression visuelle. / Adopt Playwright as the default e2e framework. Its auto-waiting eliminates flakiness, multi-browser support covers the full spectrum, and browser contexts guarantee isolation.

### 3. SLO-Driven Reliability / Fiabilite pilotee par les SLOs

Definir des SLOs bases sur l'experience utilisateur reelle, pas sur les metriques d'infrastructure. Deriver des error budgets. Quand le budget est sain, deployer des features ; quand il est sous pression, prioriser la fiabilite. Alerter sur le burn rate, pas sur des seuils statiques. / Define SLOs based on real user experience. Derive error budgets. When the budget is healthy, ship features; under pressure, prioritize reliability. Alert on burn rate, not static thresholds.

### 4. Chaos Engineering as Standard Practice / Chaos engineering comme pratique standard

Traiter le chaos engineering comme une pratique continue integree dans le pipeline de delivery. Commencer par des Game Days trimestriels, puis automatiser dans la CI/CD. Toute hypothese de fiabilite non testee est une dette de fiabilite. / Treat chaos engineering as a continuous practice in the delivery pipeline. Start with quarterly Game Days, then automate in CI/CD. Every untested reliability hypothesis is reliability debt.

### 5. Measure What Matters / Mesurer ce qui compte

Piloter la qualite par les metriques : densite de defauts, taux d'echappement, taux de flakiness, mutation score, Core Web Vitals, consommation du budget d'erreur. Rendre ces metriques visibles et les reviser regulierement. / Drive quality by metrics: defect density, escape rate, flaky rate, mutation score, Core Web Vitals, error budget consumption. Make visible and review regularly.

### 6. AI-Augmented Testing / Testing augmente par l'IA

Utiliser l'IA comme accelerateur : generation de tests, detection de regressions visuelles, analyse d'impact, self-healing des selecteurs. Ne jamais substituer l'IA a la strategie de test humaine. / Use AI as an accelerator: test generation, visual regression detection, impact analysis, selector self-healing. Never substitute AI for human test strategy.

---

## Key Frameworks & Methods

### Test Automation Stack (2024-2026)

| Layer / Couche | Recommended / Recommande | Alternatives |
|---|---|---|
| E2E Testing | **Playwright** | Cypress, Selenium |
| Visual Regression | **Playwright + Percy** | Chromatic, Argos |
| API Testing | **k6 + Pact** | REST Assured, Postman |
| Load Testing | **k6** | Gatling, JMeter, Locust |
| Frontend Performance | **Lighthouse CI + Web Vitals** | SpeedCurve, WebPageTest |
| Mobile Testing | **Detox / Maestro** | Appium, XCUITest, Espresso |
| Chaos Engineering | **Litmus (CNCF)** | Gremlin, Chaos Mesh |
| Mutation Testing | **Stryker** | PITest (Java) |

### Quality Metrics Dashboard / Tableau de bord qualite

| Metric / Metrique | Target / Cible |
|---|---|
| **Defect Density** (defauts / KLOC) | < 1 |
| **Escape Rate** (defauts prod / total) | < 5% |
| **Flaky Test Rate** | < 1% |
| **Mutation Score** | > 80% |
| **Test Coverage** (critical business logic) | > 90% |
| **CI Feedback Time** | < 10 min |
| **LCP / INP / CLS** (Core Web Vitals) | Good (green) |
| **Error Budget Remaining** | > 25% |

---

## Decision Guide

### Choosing a Test Framework / Choisir un framework

```
Nouveau projet JS/TS ? → Playwright (standard par defaut)
Suite Cypress existante et mature ? → Conserver, migrer si cout maintenance eleve
Equipe Java/.NET ? → Playwright bindings ou Selenium WebDriver 4
Mobile React Native ? → Detox ou Maestro
Mobile natif ? → XCUITest (iOS) / Espresso (Android)
Cross-platform mobile ? → Appium ou Maestro
```

### Choosing a Load Testing Tool / Choisir un outil de load testing

```
Equipe JavaScript ? → k6 (standard recommande)
QA non-developpeur ? → JMeter (GUI)
Equipe JVM ? → Gatling
Equipe Python ? → Locust
```

### Choosing a Chaos Engineering Approach / Approche chaos engineering

```
Kubernetes ? → Litmus (CNCF) ou Chaos Mesh
Solution entreprise managee ? → Gremlin (SaaS)
AWS natif ? → AWS Fault Injection Simulator
Premiere experience ? → Toxiproxy en staging → Game Day manuel → Litmus en CI
```

---

## Common Patterns & Anti-Patterns

### Patterns (Do / Faire)

- **Test pyramid with solid base** : 70% unit, 20% integration, 10% e2e. Ne pas inverser (ice cream cone anti-pattern).
- **Risk-based test prioritization** : effort de test proportionnel au risque metier. Paiement et auth meritent plus de tests que la page "A propos".
- **Contract testing** (Pact) pour valider les contrats inter-services sans deploiement integre.
- **Performance budgets automatises** : JS < 200KB gzip, LCP < 2.5s, Lighthouse > 90. Enforcer en CI.
- **Error budget policies** : actions claires en fonction de la consommation (normal / prudence / gel).
- **Chaos experiments continus** : integrer dans la CI/CD, pas uniquement lors des Game Days.
- **Flaky test quarantine** : identifier, isoler, corriger sous 1 sprint. Flaky = confiance zero.
- **Observability-driven testing** : instrumenter les tests avec traces et metriques.

### Anti-Patterns (Avoid / Eviter)

- **Ice cream cone** : majorite e2e, peu d'unitaires. Lent, fragile, couteux.
- **Coverage cosmetique** : 100% coverage sans assertions valides. Utiliser le mutation testing.
- **Manual pre-release testing** comme strategie principale. Automatiser dans le pipeline.
- **Pas de SLOs** : sans objectifs mesurables, impossible de prioriser fiabilite vs. features.
- **Chaos sans steady-state** : injecter des pannes sans hypothese = sabotage, pas chaos engineering.
- **Perf testing en fin de cycle** : integrer les benchmarks dans le CI quotidien.
- **Ignorer les tests flaky** : erode la confiance, les vrais bugs passent inapercus.

---

## Implementation Workflow

### Phase 1 — Test Automation Foundation (Semaines 1-2)

1. Deployer Playwright avec multi-navigateurs (Chromium, Firefox, WebKit) et reporters HTML/JUnit.
2. Structurer la pyramide : unitaires (Jest/Vitest), integration (Testcontainers), e2e (Playwright).
3. Integrer dans la CI : lint, typecheck, unitaires, integration, smoke e2e sur chaque PR.
4. Quality gates : couverture min 80% (logique metier), zero flaky, complexite cyclomatique < 10.
5. Regression visuelle (Playwright screenshots ou Percy) pour les composants UI critiques.

### Phase 2 — Performance & Quality Metrics (Semaines 3-4)

1. Deployer k6 pour le load testing des parcours critiques (checkout, login, search).
2. Lighthouse CI dans le pipeline (LCP < 2.5s, score > 90).
3. Performance budgets (taille bundles, timing, scores) enforces en CI.
4. Dashboard qualite : defect density, escape rate, flaky rate, mutation score.
5. Contract testing (Pact) pour les interactions inter-services.

### Phase 3 — SRE & Reliability (Mois 2)

1. Definir SLIs et SLOs pour les services critiques (disponibilite, latence, qualite).
2. Calculer les error budgets et alertes burn-rate.
3. Error budget policies (actions en fonction de la consommation).
4. Mesurer le toil ratio, identifier les 5 sources principales, planifier l'automatisation.
5. Capacity planning et disaster recovery documentation.

### Phase 4 — Chaos Engineering & Continuous Improvement (Mois 3+)

1. Deployer Litmus/Gremlin. Commencer en staging.
2. Premier Game Day : pod-kill, network-latency, AZ failure.
3. Hypotheses de steady state et criteres d'arret pour chaque experience.
4. Automatiser les chaos experiments dans la CI/CD (validation post-deploy).
5. Patterns de resilience : circuit breaker, retry with backoff, bulkhead, graceful degradation.
6. Revue hebdomadaire : SLO status, error budget, metriques qualite, resultats chaos.
7. Game Days trimestriels avec augmentation progressive du blast radius.

---



## State of the Art (2025-2026)

La qualité et la fiabilité intègrent l'IA et l'automatisation avancée :

- **AI-generated tests** : Les LLM génèrent des tests unitaires, d'intégration et E2E à partir du code source, accélérant la couverture.
- **Playwright domine** : Playwright s'impose comme le framework E2E de référence, surpassant Cypress grâce au multi-navigateur natif et aux traces.
- **Chaos engineering mainstream** : Les pratiques de chaos engineering (Litmus, Chaos Mesh, game days) se démocratisent au-delà des GAFAM.
- **SLO-driven development** : Les SLOs pilotent les décisions d'ingénierie, avec des error budgets qui déterminent le rythme de déploiement.
- **Shift-left testing** : Les tests de sécurité, performance et accessibilité s'exécutent dès le développement local, pas seulement en CI.

## Template actionnable

### Matrice de stratégie de tests

| Type de test | Scope | Outils | Fréquence | Couverture cible |
|---|---|---|---|---|
| **Unit** | Fonctions, modules | Jest, Vitest | Chaque commit | > 80% |
| **Integration** | APIs, services | Supertest, MSW | Chaque PR | Endpoints critiques |
| **E2E** | Parcours utilisateur | Playwright, Cypress | Nightly + pre-deploy | Happy paths |
| **Visual** | UI, composants | Chromatic, Percy | Chaque PR UI | Composants partagés |
| **Performance** | Charge, latence | k6, Artillery | Hebdomadaire | SLOs définis |
| **Contract** | APIs inter-services | Pact | Chaque PR API | Contrats publiés |
| **Security** | Vulnérabilités | Snyk, OWASP ZAP | Quotidien | OWASP Top 10 |

## Prompts types

- "Comment mettre en place des tests E2E avec Playwright ?"
- "Aide-moi à concevoir une stratégie de tests automatisés complète"
- "Comment implémenter du chaos engineering dans notre environnement ?"
- "Propose des quality gates pour notre pipeline CI/CD"
- "Comment faire du load testing avec k6 pour notre API ?"
- "Aide-moi à définir un error budget et des SLOs réalistes"

## Skills connexes

| Skill | Lien |
|---|---|
| Code Excellence | `code-development:code-excellence` — Stratégie de tests et TDD |
| DevOps | `code-development:devops` — CI/CD et déploiement continu |
| Monitoring | `code-development:monitoring` — SRE, SLOs et incident management |
| Process Engineering | `code-development:process-engineering` — Quality gates et métriques DORA |
| Opérations | `entreprise:operations` — Excellence opérationnelle et amélioration continue |

## Additional Resources

Consult the reference files for deep-dive guidance / Consulter les references pour un approfondissement :

- **[Test Automation](./references/test-automation.md)** — Comparatif Cypress vs Playwright vs Selenium, strategie de test risk-based, regression visuelle (Percy, Chromatic, Argos), API testing (Pact, REST Assured, k6), mobile testing (Appium, Detox, Maestro), AI-powered testing.

- **[Performance Testing](./references/performance-testing.md)** — Load testing (k6, JMeter, Gatling, Locust), stress testing, capacity testing, benchmarking, frontend performance (Lighthouse, Core Web Vitals, SpeedCurve), database performance, performance budgets.

- **[SRE Practices](./references/sre-practices.md)** — Principes SRE (Google SRE Book : embracing risk, SLOs, eliminating toil), toil measurement & automation, capacity planning, disaster recovery testing, error budgets, SRE vs DevOps, platform reliability engineering.

- **[Chaos Engineering](./references/chaos-engineering.md)** — Principes Netflix, injection de pannes (Chaos Monkey, Gremlin, Litmus), Game Days, steady-state hypothesis, blast radius management, chaos in CI/CD, resilience patterns (circuit breaker, bulkhead, retry with backoff).

### Foundational References / References fondamentales

- Betsy Beyer et al., *Site Reliability Engineering* (Google SRE Book, 2016) — https://sre.google/sre-book/table-of-contents/
- Betsy Beyer et al., *The Site Reliability Workbook* (2018) — https://sre.google/workbook/table-of-contents/
- Casey Rosenthal & Nora Jones, *Chaos Engineering: System Resiliency in Practice* (O'Reilly, 2020)
- Principles of Chaos Engineering — https://principlesofchaos.org/
- k6 Documentation — https://grafana.com/docs/k6/
- Playwright Documentation — https://playwright.dev/
- Dave Farley, *Modern Software Engineering* (2021)
