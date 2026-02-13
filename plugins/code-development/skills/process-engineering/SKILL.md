---
name: process-engineering
description: This skill should be used when the user asks about "development workflow", "developer experience", "DX", "agile process", "sprint planning", "estimation", "technical documentation", "engineering metrics", "DORA metrics", "SPACE framework", "coding standards", "linting", "workflow de développement", "expérience développeur", "processus agile", "planification de sprint", "estimation", "documentation technique", "métriques d'ingénierie", "standards de code", "velocity", "story points", "retrospective", "daily standup", "code review process", "PR review", "pull request", "git workflow", "branching strategy", "trunk-based development", "feature branching", "monorepo", "RFC", "design doc", "ADR", "technical RFC", "team topologies", "engineering culture", or needs guidance on engineering processes, team productivity, and development standards.
version: 1.1.0
last_updated: 2026-02
---

# Process Engineering — Development Workflows, Developer Experience, Documentation & Engineering Metrics

## Overview

**FR** — Cette skill couvre l'ingenierie des processus de developpement logiciel dans sa globalite : conception de workflows agiles, experience developpeur (DX), documentation technique, metriques d'ingenierie et gouvernance technologique. Un processus de developpement mature ne se limite pas a choisir un framework agile — il s'agit de concevoir un systeme sociotechnique ou chaque developpeur peut produire son meilleur travail avec un minimum de friction. L'objectif est de fournir des recommandations actionnables et alignees avec les meilleures pratiques 2024-2026, incluant le platform engineering, le developpement augmente par l'IA, la mesure de la productivite developpeur et les plateformes d'intelligence ingenierie.

**EN** — This skill covers the full scope of software development process engineering: agile workflow design, developer experience (DX), technical documentation, engineering metrics, and technology governance. A mature development process goes far beyond picking an agile framework — it is about designing a sociotechnical system where every developer can produce their best work with minimal friction. The goal is to provide actionable recommendations aligned with 2024-2026 best practices, including platform engineering, AI-augmented development, developer productivity measurement, and engineering intelligence platforms.

---

## When This Skill Applies

Activate this skill when the user:

- Plans or improves sprint planning, estimation, and backlog management workflows
- Designs a developer onboarding process or improves time-to-first-commit
- Sets up local development environments (devcontainers, Docker Compose, Nix)
- Evaluates or deploys internal developer portals (Backstage, Port, Cortex, OpsLevel)
- Writes or structures API documentation (OpenAPI, AsyncAPI), architecture docs (C4, arc42), or runbooks
- Measures engineering performance with DORA metrics, SPACE framework, or other productivity models
- Defines coding standards, linting rules, or technology governance policies
- Builds documentation-as-code pipelines or knowledge base maintenance workflows
- Evaluates or integrates AI-augmented development tools into team workflows
- Sets up engineering OKRs, cycle time tracking, or engineering intelligence platforms (LinearB, Jellyfish, DX)

---

## Core Principles

### 1. Optimize for Developer Flow State
Treat developer focus time as the most precious resource. Minimize context switching, reduce toil, and eliminate unnecessary approval gates. Every process should be evaluated by its impact on uninterrupted deep work time. / Traiter le temps de concentration des developpeurs comme la ressource la plus precieuse. Minimiser les changements de contexte, reduire le travail repetitif et eliminer les portes d'approbation inutiles.

### 2. Measure Outcomes, Not Activity
Never measure lines of code, number of commits, or hours logged. Focus on outcomes: cycle time, deployment frequency, customer impact, and developer satisfaction. Use the SPACE framework to capture multiple dimensions of productivity. / Ne jamais mesurer les lignes de code, le nombre de commits ou les heures travaillees. Se concentrer sur les resultats : cycle time, frequence de deploiement, impact client et satisfaction des developpeurs.

### 3. Document as You Build, Not After
Embed documentation into the development workflow. Use documentation-as-code (Markdown in repos, OpenAPI specs, ADRs). Treat stale documentation as a bug. Automate documentation generation wherever possible. / Integrer la documentation dans le workflow de developpement. Utiliser la documentation-as-code. Traiter la documentation obsolete comme un bug.

### 4. Standardize the Golden Path, Not Every Path
Provide opinionated, well-supported default workflows (golden paths) while allowing teams to deviate when justified. The platform team builds paved roads; product teams are free to go off-road if they accept the maintenance cost. / Fournir des workflows par defaut opiniatres et bien supportes (golden paths) tout en permettant aux equipes de devier quand c'est justifie.

### 5. Treat Process as Product
Apply product thinking to internal processes: gather feedback, iterate, measure adoption, and deprecate processes that no longer serve their purpose. A process without a clear owner and regular review cadence will decay. / Appliquer la pensee produit aux processus internes : collecter du feedback, iterer, mesurer l'adoption, et deprecier les processus qui ne servent plus.

### 6. Embrace AI as a Collaborator, Not a Replacement
Integrate AI tools (Copilot, Claude, Cursor, Cody) as force multipliers for documentation, code review, test generation, and workflow automation. Establish clear governance for AI-generated artifacts. Measure AI impact on DX rather than assuming benefit. / Integrer les outils IA comme multiplicateurs de force pour la documentation, la revue de code, la generation de tests et l'automatisation des workflows. Etablir une gouvernance claire pour les artefacts generes par l'IA.

---

## Key Frameworks & Methods

| Framework / Method | Purpose | FR |
|---|---|---|
| **DORA Metrics** | Measure software delivery performance (DF, LT, CFR, MTTR) | Mesurer la performance de livraison logicielle |
| **SPACE Framework** | Multidimensional developer productivity (Satisfaction, Performance, Activity, Communication, Efficiency) | Productivite multidimensionnelle des developpeurs |
| **Story Mapping** | Visualize user journey for backlog prioritization | Visualiser le parcours utilisateur pour prioriser le backlog |
| **Definition of Done / Ready** | Quality gates for work items entering and exiting sprints | Portes de qualite pour les items entrant et sortant du sprint |
| **C4 Model** | Hierarchical architecture documentation (Context, Container, Component, Code) | Documentation d'architecture hierarchique |
| **OpenAPI / AsyncAPI** | Machine-readable API contracts | Contrats API lisibles par les machines |
| **ADR (Architecture Decision Records)** | Document architectural decisions with context and consequences | Documenter les decisions architecturales avec contexte et consequences |
| **Platform Engineering** | Self-service golden paths for developers via Internal Developer Platforms | Golden paths self-service via des plateformes internes |
| **DevEx (DX) Framework** | Three dimensions of DX: flow state, feedback loops, cognitive load | Trois dimensions de la DX : etat de flow, boucles de feedback, charge cognitive |
| **Engineering Intelligence** | Data-driven insights into engineering processes (LinearB, Jellyfish, DX) | Insights data-driven sur les processus d'ingenierie |

---

## Decision Guide

### Choosing an Estimation Approach

| Approach | When to Use | FR |
|---|---|---|
| **Story Points (Fibonacci)** | Teams needing relative sizing, shared understanding of complexity | Equipes ayant besoin d'un dimensionnement relatif |
| **T-Shirt Sizing (S/M/L/XL)** | Early-stage estimation, roadmap planning, less mature teams | Estimation macro, planification roadmap |
| **No Estimates** | High-trust teams with small, well-defined work items and continuous flow | Equipes matures en flux continu avec items bien decoupes |
| **Cycle Time Forecasting** | Data-driven estimation using Monte Carlo simulations on historical data | Estimation data-driven par simulations Monte Carlo |
| **Ideal Days** | When stakeholders struggle with abstract units; keep calibrated | Quand les parties prenantes ont du mal avec les unites abstraites |

### Choosing a Documentation Strategy

- **OpenAPI + Redoc/Swagger UI** — REST APIs with strong contract-first approach. Generate client SDKs automatically.
- **AsyncAPI** — Event-driven architectures (Kafka, RabbitMQ, WebSocket). Document message schemas and channels.
- **C4 Model + Structurizr** — System architecture at multiple zoom levels. Best for evolving architectures.
- **arc42** — Comprehensive architecture documentation template. Best for regulated industries or large systems.
- **Diátaxis framework** — Structure docs into tutorials, how-to guides, explanations, and references. Apply to developer portals.

### Choosing an Internal Developer Portal

- **Backstage (Spotify)** — Open-source, extensible, large plugin ecosystem. Best for organizations wanting full control and customization. Requires dedicated platform team to operate.
- **Port** — SaaS-first, lower operational overhead, strong RBAC. Best for mid-size organizations wanting quick time-to-value.
- **Cortex** — Focus on service maturity scorecards and operational readiness. Best for SRE-oriented organizations.
- **OpsLevel** — Service ownership and maturity tracking. Best for organizations focused on service catalog and standards enforcement.

---

## Common Patterns & Anti-Patterns

### Patterns (Do)
- **Sprint Goal-Driven Planning**: Define a single sprint goal; select stories that contribute to it. Reject work that does not align. This creates focus and enables meaningful sprint reviews.
- **Definition of Ready as a Contract**: Require stories to meet DoR criteria (acceptance criteria defined, dependencies identified, estimated, UX specs attached) before sprint planning. Reject unready items.
- **Documentation-as-Code**: Keep docs in the same repository as code. Use Markdown, Mermaid diagrams, and CI pipelines to build and publish. Docs are reviewed in PRs alongside code changes.
- **Devcontainers for Onboarding**: Provide a `.devcontainer` configuration that gives every developer a fully working environment in under 10 minutes. Include all dependencies, services, seed data, and IDE extensions.
- **Engineering Metrics Dashboards**: Display DORA metrics, cycle time, and PR review time on team dashboards. Review trends weekly. Never use metrics for individual performance evaluation.
- **AI-Augmented Documentation**: Use LLMs to generate first drafts of runbooks, API docs, and ADRs. Human review remains mandatory. Track documentation freshness automatically.

### Anti-Patterns (Avoid)
- **Estimation Theater**: Spending hours debating whether a story is 5 or 8 points. Time-box estimation. If debate exceeds 2 minutes, split the story or use the higher estimate.
- **Vanity Metrics**: Tracking velocity as a performance metric or comparing velocity across teams. Velocity is a planning tool, not a productivity measure.
- **Documentation Graveyards**: Writing comprehensive docs once and never updating them. Prefer lightweight, living docs with automated freshness checks.
- **Tool Fetishism**: Adopting every new productivity tool without measuring impact. Each tool adds cognitive load. Evaluate tools with a 30-day trial and measurable success criteria.
- **Process Cargo Culting**: Copying another company's process without understanding the context. Spotify Model, SAFe, and other frameworks require adaptation, not blind adoption.
- **Surveillance Disguised as Metrics**: Using commit frequency, keystrokes, or screen time as developer productivity proxies. This destroys trust and incentivizes gaming rather than outcomes.

---

## Implementation Workflow

Follow this workflow when designing or improving engineering processes:

### Phase 1 — Assess Current State (1 week)

1. **Map the value stream** from idea to production. Identify each step, handoff, queue, and wait time. Measure the total lead time and the ratio of active work to waiting.
2. **Survey developers** using a DX survey (DX by Abi Noda, or custom). Measure satisfaction, perceived friction points, and tooling pain. Target a minimum 70% response rate for validity.
3. **Collect baseline metrics**: deployment frequency, lead time for changes, change failure rate, MTTR. Use existing CI/CD data, git history, and incident logs.
4. **Audit documentation**: inventory existing docs, measure staleness (last updated date vs. last code change), and identify critical gaps (missing runbooks, outdated architecture diagrams).

### Phase 2 — Design Target State (1-2 weeks)

1. **Define engineering principles** the team agrees to uphold. Write them down. Make them specific and falsifiable (e.g., "every production service has a runbook" not "we value documentation").
2. **Design the sprint workflow**: cadence (1 or 2 weeks), ceremonies (planning, daily standup, review, retro), artifact standards (DoR, DoD, story format).
3. **Select and configure tooling**: issue tracker, documentation platform, developer portal, metrics dashboard. Prefer tools that integrate with existing workflows rather than requiring new ones.
4. **Define coding standards**: linting rules, formatting (Prettier, Black, gofmt), commit message conventions (Conventional Commits), branch naming, PR size limits.

### Phase 3 — Implement Incrementally (2-4 weeks per initiative)

1. **Start with quick wins**: devcontainer setup, linter configuration, PR template, Definition of Done checklist. These deliver immediate value and build momentum.
2. **Roll out documentation standards**: API documentation (OpenAPI spec per service), README template, ADR process, runbook template. Assign documentation owners per service.
3. **Deploy metrics visibility**: set up a DORA metrics dashboard (from CI/CD data). Share it publicly with the team. Discuss trends in retrospectives. Never use it for individual evaluation.
4. **Launch the developer portal**: start with a service catalog (Backstage or Port). Add software templates for new services. Gradually integrate documentation, API specs, and scorecards.

### Phase 4 — Sustain and Evolve (Ongoing)

1. **Run quarterly DX surveys** to track developer satisfaction and identify emerging friction. Compare results over time.
2. **Review processes in retrospectives**: every process has a shelf life. Regularly ask "does this still serve us?" and be willing to deprecate.
3. **Iterate on standards**: coding standards, DoD, and templates evolve. Version them. Communicate changes clearly. Provide migration guides when standards change.
4. **Invest in AI augmentation**: continuously evaluate new AI tools for documentation generation, code review, test creation, and workflow automation. Measure their impact on cycle time and developer satisfaction.

---



## Rythme opérationnel

| Cadence | Activité | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Hebdomadaire** | Revue des métriques sprint (vélocité, cycle time) | Engineering Manager | Dashboard sprint et tendances |
| **Hebdomadaire** | Log des blocages et frictions de processus | Tech Lead | Backlog frictions priorisé |
| **Mensuel** | Revue des métriques DORA/SPACE | Engineering Manager + VP Engineering | Rapport DORA/SPACE commenté |
| **Mensuel** | Audit de fraîcheur de la documentation | Tech Lead | Checklist documentation et mises à jour requises |
| **Trimestriel** | Rétrospective des processus d'ingénierie | Engineering Manager + Équipe | Plan d'amélioration des processus |
| **Trimestriel** | Enquête expérience développeur (DX) | VP Engineering | Rapport DX et actions prioritaires |
| **Annuel** | Actualisation du handbook et des standards engineering | VP Engineering + Tech Leads | Handbook engineering et normes actualisés |

## State of the Art (2025-2026)

Les processus d'ingénierie s'adaptent à l'ère de l'IA :

- **AI-augmented development** : L'intégration d'assistants IA dans le workflow (coding, review, documentation, testing) transforme les processus et les métriques de productivité.
- **DORA metrics standardisées** : Les quatre métriques DORA (deployment frequency, lead time, MTTR, change failure rate) sont adoptées comme standard de mesure.
- **Developer Experience (DX)** : Le DX devient une priorité avec des équipes dédiées, des surveys internes (DX surveys) et des outils de mesure (SPACE framework).
- **Inner source** : Les pratiques open source appliquées en interne (inner source) favorisent la réutilisation et la collaboration inter-équipes.
- **Documentation-as-Code** : La documentation technique vit dans le repo (Markdown, MDX, Astro), versionnée et déployée automatiquement avec le code.

## Template actionnable

### Template de RFC / Design Doc

| Section | Contenu |
|---|---|
| **Titre** | RFC-___: ___ |
| **Auteur** | ___ |
| **Date** | ___ |
| **Statut** | Brouillon / En revue / Approuvé / Implémenté |
| **Résumé** | En 2-3 phrases, quel problème et quelle solution ? |
| **Contexte** | Pourquoi maintenant ? Quel est le problème ? |
| **Proposition** | Description détaillée de la solution |
| **Alternatives** | Options écartées et pourquoi |
| **Impact** | Équipes impactées, migration, breaking changes |
| **Plan d'implémentation** | Étapes, estimation, dépendances |
| **Questions ouvertes** | Points à résoudre avant approbation |

## Prompts types

- "Comment améliorer les métriques DORA de notre équipe ?"
- "Aide-moi à mettre en place un processus de PR review efficace"
- "Propose une convention de branching pour notre monorepo"
- "Comment estimer les story points de manière fiable ?"
- "Aide-moi à rédiger un RFC/design doc pour une nouvelle feature"
- "Quels standards de code adopter pour notre équipe TypeScript ?"

## Skills connexes

| Skill | Lien |
|---|---|
| Gestion de projets | `entreprise:gestion-de-projets` — Méthodologies agile et pilotage de projet |
| Code Excellence | `code-development:code-excellence` — Standards de code et bonnes pratiques |
| DevOps | `code-development:devops` — CI/CD et automatisation du workflow |
| Quality Reliability | `code-development:quality-reliability` — Quality gates et métriques qualité |
| Monitoring | `code-development:monitoring` — Métriques DORA et performance engineering |

## Additional Resources

Consult these reference files for deep dives on each topic area:

- **[Agile Workflows](./references/agile-workflows.md)** — Sprint planning, estimation techniques (story points, t-shirt sizing, no estimates, Monte Carlo), story mapping, backlog grooming, Definition of Done and Definition of Ready, workflow automation, issue tracking tools comparison (Jira, Linear, Shortcut, GitHub Projects), agile at scale (SAFe, LeSS, Nexus), and continuous flow with Kanban.

- **[Developer Experience](./references/developer-experience.md)** — Developer onboarding programs, local dev setup (devcontainers, Docker Compose, Nix), developer tooling and productivity measurement, internal developer portals (Backstage, Port, Cortex, OpsLevel), documentation-as-code, AI-augmented development workflows, platform engineering, and the DevEx framework (flow state, feedback loops, cognitive load).

- **[Technical Documentation](./references/technical-documentation.md)** — API documentation (OpenAPI/Swagger, AsyncAPI), architecture documentation (C4 model, arc42, Structurizr), Architecture Decision Records (ADR), runbooks and playbooks, README standards, knowledge base maintenance, diagramming tools (Mermaid, PlantUML, D2), and the Diataxis documentation framework.

- **[Engineering Metrics](./references/engineering-metrics.md)** — DORA metrics deep dive (deployment frequency, lead time for changes, MTTR, change failure rate), SPACE framework, cycle time and throughput analysis, developer productivity debates and pitfalls, engineering OKRs, burndown and velocity, engineering intelligence platforms (LinearB, Jellyfish, DX, Swarmia), and the McKinsey developer productivity controversy.

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.
### Foundational References
- Nicole Forsgren, Jez Humble, Gene Kim, *Accelerate* (2018)
- Team Topologies — Matthew Skelton & Manuel Pais (2019)
- Abi Noda, Margaret-Anne Storey et al., *DevEx: What Actually Drives Productivity* (ACM Queue, 2023)
- Forsgren, Storey, Maddila et al., *The SPACE of Developer Productivity* (ACM Queue, 2021)
- Jeff Patton, *User Story Mapping* (2014)
- Gregor Hohpe, *The Software Architect Elevator* (2020)
- Simon Brown, *The C4 Model for Visualising Software Architecture* (c4model.com)
- Luca Mezzalira, *Building Micro-Frontends* (2021) — for platform engineering patterns
- *State of DevOps Report* — DORA / Google Cloud (annual)
- *DX Core 4* — DX (getdx.com) developer experience measurement framework
