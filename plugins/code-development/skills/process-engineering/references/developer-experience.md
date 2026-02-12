# Developer Experience — Onboarding, Tooling, Portals, Platform Engineering & AI-Augmented Development

## Vue d'ensemble / Overview

**FR** — Ce document de reference couvre l'experience developpeur (DX) dans toutes ses dimensions : onboarding des nouveaux developpeurs, configuration des environnements de developpement locaux, outillage et productivite, portails developpeurs internes, documentation-as-code, workflows de developpement augmente par l'IA, platform engineering et le framework DevEx. L'experience developpeur est devenue un domaine d'investissement strategique en 2024-2026, portee par la penurie de talents, la complexite croissante des systemes distribues et l'avenement des outils de developpement IA. Un DX mature reduit le time-to-productivity, diminue la charge cognitive et augmente la retention des developpeurs.

**EN** — This reference document covers developer experience (DX) across all its dimensions: developer onboarding, local development environment setup, tooling and productivity, internal developer portals, documentation-as-code, AI-augmented development workflows, platform engineering, and the DevEx framework. Developer experience has become a strategic investment area in 2024-2026, driven by talent scarcity, growing complexity of distributed systems, and the advent of AI development tools. A mature DX reduces time-to-productivity, lowers cognitive load, and increases developer retention.

---

## Developer Onboarding

### Measuring Onboarding Success

Define and track these onboarding KPIs:

| Metric | Target | How to measure | FR |
|---|---|---|---|
| **Time to first commit** | < 1 day | Git log: time from account creation to first merged PR | Temps entre creation du compte et premier commit merge |
| **Time to first production deploy** | < 2 weeks | Deployment logs: time from start date to first production deployment | Temps entre la date de debut et le premier deploiement en prod |
| **Time to full productivity** | < 3 months | Manager assessment + self-assessment survey at 30/60/90 days | Evaluation manager + auto-evaluation a 30/60/90 jours |
| **Onboarding NPS** | > 8/10 | Survey at 30 days and 90 days | Enquete a 30 et 90 jours |
| **Documentation completeness** | > 80% tasks documented | Audit of onboarding checklist vs. actual steps required | Audit du checklist d'onboarding vs etapes reelles |

### The 30-60-90 Day Onboarding Plan

**Week 1 — Environment and Context**
1. Grant all required access (repos, CI/CD, cloud accounts, issue tracker, communication tools) on day 0, before the developer arrives. Automate access provisioning with SCIM or Terraform.
2. Provide a working development environment: devcontainer, Docker Compose, or Nix flake that gives a fully functional local setup in under 10 minutes.
3. Assign an onboarding buddy (not the manager) — a peer who answers questions and pair-programs.
4. Walk through the architecture overview (C4 context and container diagrams). Provide links to ADRs for key decisions.
5. Complete the first "hello world" task: fix a small bug or add a minor feature. The goal is a merged PR by end of day 2.

**Days 8-30 — Contribution**
1. Assign progressively complex stories. Start with well-defined items, then move to items requiring cross-team coordination.
2. Pair-program on at least 3 tasks with different team members to transfer context.
3. Encourage the new developer to update documentation when they find gaps — "if you had to figure it out, document it."
4. Review the onboarding experience in a 30-day feedback session. Update the onboarding checklist based on findings.

**Days 31-60 — Ownership**
1. Assign ownership of a small service or feature area.
2. Include the developer in on-call rotation (with a shadow period first).
3. Have the developer present their work in a sprint review or tech talk.

**Days 61-90 — Autonomy**
1. The developer should be able to independently deliver medium-complexity stories.
2. Conduct a 90-day feedback session with the manager, buddy, and the developer themselves.
3. Transition from onboarding buddy to regular team collaboration.

**FR** — Structurer l'onboarding en 30-60-90 jours. Semaine 1 : environnement fonctionnel et premier PR merge en J2. Jours 8-30 : contributions progressives et pair programming. Jours 31-60 : prise de responsabilite. Jours 61-90 : autonomie complete. Mesurer le time-to-first-commit (< 1 jour) et le time-to-productivity (< 3 mois).

---

## Local Development Environments

### Devcontainers (VS Code / GitHub Codespaces)

Devcontainers provide a fully reproducible development environment defined in code. Use them as the primary onboarding mechanism.

**Structure a `.devcontainer/` directory:**

```
.devcontainer/
  devcontainer.json      # Main configuration
  docker-compose.yml     # Multi-service setup (app + db + cache + queue)
  Dockerfile             # Custom dev image (if base image needs extensions)
  post-create.sh         # Run after container creation (seed data, install tools)
```

**Best practices for devcontainer.json:**
- Start from a well-maintained base image (`mcr.microsoft.com/devcontainers/` or custom).
- Define all required VS Code extensions in `customizations.vscode.extensions`. Include linters, formatters, language servers, and debugging tools.
- Use `forwardPorts` to expose service ports (database, API, frontend).
- Configure `postCreateCommand` to run database migrations, seed data, and install project dependencies automatically.
- Use `features` to add common tools (Docker-in-Docker, Node.js, Python, AWS CLI) without bloating the Dockerfile.
- Set environment variables via `containerEnv` or `.env` files (never commit secrets — use placeholder values with comments).

**FR** — Les devcontainers fournissent un environnement de developpement reproductible defini dans le code. Les utiliser comme mecanisme d'onboarding principal. Definir les extensions VS Code, les ports forwards, les commandes post-creation (migrations, seed data) et les variables d'environnement.

### Docker Compose for Development

For teams not using devcontainers, Docker Compose provides a multi-service development environment.

**Best practices:**
- Create a `docker-compose.dev.yml` separate from production compose files.
- Use volume mounts for source code to enable hot-reloading.
- Include all dependencies (database, cache, message queue, mock services) so developers never need to install anything natively.
- Add a `Makefile` or `Taskfile` with common commands: `make up`, `make down`, `make seed`, `make test`, `make logs`.
- Use healthchecks and `depends_on` with conditions to ensure proper startup order.
- Provide a `.env.example` file with all required environment variables and sane defaults.

### Nix for Reproducible Environments

Nix is the most rigorous approach to reproducible development environments. Use it when teams need exact binary-level reproducibility across macOS and Linux.

**When to adopt Nix:**
- Multi-language projects where tool version management is complex (Python + Node + Go + Rust)
- Teams experiencing "works on my machine" issues despite Docker
- Projects requiring specific system-level dependencies that containers handle poorly (GPU drivers, specific kernel modules)

**How to implement:**
- Define a `flake.nix` in the project root with `devShells` for each environment.
- Use `direnv` with `nix-direnv` for automatic environment activation on `cd`.
- Pin all dependencies via `flake.lock` — commit the lock file to ensure reproducibility.
- Combine with devcontainers for the best of both worlds: Nix inside a devcontainer for maximum portability.

**FR** — Nix offre la reproductibilite la plus rigoureuse pour les environnements de dev. L'utiliser pour les projets multi-langages ou les problemes de "works on my machine" persistent malgre Docker. Definir un `flake.nix` avec `devShells` et utiliser `direnv` pour l'activation automatique.

---

## Developer Tooling & Productivity

### Essential Developer Tooling Stack (2024-2026)

| Category | Tool(s) | Purpose | FR |
|---|---|---|---|
| **Editor / IDE** | VS Code, JetBrains (IntelliJ, WebStorm), Cursor, Zed | Code editing, debugging, refactoring | Edition, debogage, refactoring |
| **AI Code Assistant** | GitHub Copilot, Claude (via Claude Code, Cursor, Cody), Amazon Q Developer | Code completion, generation, explanation, refactoring | Completion, generation, explication de code |
| **Terminal** | Warp, iTerm2, Alacritty, Windows Terminal | Modern terminal with AI features, split panes, history | Terminal moderne |
| **Git GUI** | GitKraken, Lazygit, Fork, built-in IDE Git | Visual branch management, conflict resolution | Gestion visuelle des branches |
| **API Client** | Bruno, Insomnia, Postman, httpie | API testing and documentation | Test et documentation d'API |
| **Task Runner** | Make, Taskfile, Just, npm scripts | Standardized command interface | Interface de commandes standardisee |
| **Linter / Formatter** | ESLint, Prettier, Biome, Black, Ruff, gofmt, clippy | Code quality enforcement | Application des standards de qualite |
| **Pre-commit hooks** | Husky + lint-staged, pre-commit (Python), lefthook | Gate quality before commit | Verifier la qualite avant le commit |
| **Secrets scanner** | Gitleaks, TruffleHog, git-secrets | Prevent secrets in code | Empecher les secrets dans le code |
| **Documentation** | Mintlify, Docusaurus, Starlight, VitePress | Developer documentation sites | Sites de documentation developpeur |

### Measuring Developer Tooling Impact

Do not adopt tools based on hype. Measure impact using:
1. **Time saved per developer per week**: estimate before and after adoption. Require > 30 minutes saved per week to justify the cognitive load of a new tool.
2. **Adoption rate**: track active usage (not just installations). A tool with < 60% weekly active usage after 90 days should be reconsidered.
3. **Developer satisfaction survey**: include tooling questions in quarterly DX surveys. Track sentiment over time.
4. **Cycle time impact**: measure whether new tools correlate with reduced cycle time or deployment frequency improvements.

**FR** — Ne pas adopter d'outils sur la base du hype. Mesurer l'impact : temps gagne par developpeur par semaine (> 30 min minimum), taux d'adoption (> 60% d'utilisation hebdomadaire active apres 90 jours), satisfaction dans les enquetes DX, et impact sur le cycle time.

---

## Internal Developer Portals (IDP)

### Backstage (Spotify) — Deep Dive

Backstage is the leading open-source Internal Developer Portal. Use it to centralize service catalogs, documentation, API specs, and developer workflows.

**Core components:**
1. **Software Catalog**: register every service, library, website, and infrastructure component. Use `catalog-info.yaml` files in each repository for registration.
2. **Software Templates (Scaffolder)**: provide golden-path templates for creating new services, libraries, or infrastructure. Include CI/CD, monitoring, documentation, and security by default.
3. **TechDocs**: documentation-as-code rendered from Markdown files in each repository. Automatically published alongside the service catalog.
4. **Plugins**: extend Backstage with 200+ community plugins (Kubernetes, PagerDuty, ArgoCD, SonarQube, GitHub Actions, etc.).

**Implementation roadmap:**
1. **Phase 1 (4-6 weeks)**: Deploy Backstage, populate the software catalog with all services, set up basic TechDocs.
2. **Phase 2 (6-8 weeks)**: Create 2-3 software templates for common service patterns. Integrate CI/CD status and deployment info.
3. **Phase 3 (ongoing)**: Add plugins for monitoring, incident management, and API docs. Build custom plugins for organization-specific workflows.

**Operational requirements**: Backstage requires a dedicated platform team (minimum 1-2 engineers) for maintenance, plugin updates, and custom development. Budget for this before adopting.

### Port — SaaS Alternative

Port is a SaaS-based Internal Developer Portal that offers faster time-to-value than Backstage.

**Differentiators:**
- No infrastructure to manage — fully hosted SaaS
- Strong RBAC and permissions model out of the box
- Self-service actions with approval workflows
- Scorecards for service maturity tracking
- Native integrations with major cloud providers and DevOps tools

**When to choose Port over Backstage**: when the organization does not have a dedicated platform team, needs faster time-to-value (weeks instead of months), or prioritizes enterprise features (RBAC, audit logs, SSO) out of the box.

**FR** — Backstage est le portail developpeur open-source de reference. Il centralise le catalogue de services, les templates, la documentation et les plugins. Port est l'alternative SaaS pour les organisations sans equipe plateforme dediee. Choisir Backstage pour le controle et la personnalisation, Port pour la rapidite de mise en oeuvre.

---

## Documentation-as-Code

### Principles

1. **Store docs alongside code**: documentation lives in the same repository as the code it describes. Changes to code and docs happen in the same PR.
2. **Write in Markdown**: use Markdown (or MDX for React-based docs) as the universal documentation format. Avoid proprietary formats.
3. **Render automatically**: use CI pipelines to build and publish docs on every merge to main. Tools: Docusaurus, Starlight, VitePress, Mintlify, MkDocs.
4. **Review docs in PRs**: apply the same code review process to documentation changes. Require review from both a technical writer (if available) and a domain expert.
5. **Test documentation**: use link checkers (markdown-link-check), spell checkers (cspell), and linters (markdownlint) in CI. For API docs, validate OpenAPI specs with spectral.
6. **Track freshness**: tag each document with a `last-reviewed` date. Set up automated alerts when docs have not been reviewed in 90 days.

### Diátaxis Documentation Framework

Structure all developer documentation using the Diátaxis framework (by Daniele Procida):

| Type | Purpose | Structure | Example | FR |
|---|---|---|---|---|
| **Tutorial** | Learning-oriented: guide the learner through a series of steps to complete a project | Step-by-step, sequential | "Build your first API with our framework" | Guide d'apprentissage pas-a-pas |
| **How-to Guide** | Task-oriented: provide steps to solve a specific problem | Numbered steps, assumes knowledge | "How to add authentication to a service" | Guide pratique pour resoudre un probleme |
| **Explanation** | Understanding-oriented: clarify concepts, provide context and reasoning | Discursive, can include diagrams | "How our event-driven architecture works" | Explication de concepts et architecture |
| **Reference** | Information-oriented: technical description of the system | Structured, comprehensive, no narrative | "API endpoint reference", "Configuration options" | Reference technique exhaustive |

**FR** — Utiliser le framework Diataxis pour structurer toute la documentation developpeur en quatre types : tutoriels (apprentissage), guides pratiques (taches), explications (comprehension), references (information). Stocker la doc dans le meme repository que le code, ecrire en Markdown, construire automatiquement en CI.

---

## AI-Augmented Development Workflows (2024-2026)

### The AI-Augmented Developer Toolkit

| Capability | Tool(s) | Maturity | Impact | FR |
|---|---|---|---|---|
| **Code completion** | GitHub Copilot, Claude (Cursor, Cody, Claude Code), Amazon Q | Mature | 20-40% faster code writing for routine tasks | 20-40% plus rapide pour les taches routinieres |
| **Code generation from spec** | Claude, GPT-4, Gemini via IDE integration | Mature | Generate boilerplate, tests, migrations from specs | Generation de boilerplate depuis les specs |
| **Code review assistance** | CodeRabbit, Copilot Code Review, PR-Agent, Ellipsis | Growing | First-pass review catching style, bugs, security issues | Revue de premier niveau |
| **Documentation generation** | Claude, Mintlify AI, Swim | Growing | Draft API docs, READMEs, ADRs, runbooks | Brouillons de documentation |
| **Test generation** | Copilot, Claude, Diffblue Cover (Java), CodiumAI | Growing | Generate unit/integration tests from existing code | Generation de tests |
| **Bug diagnosis** | Claude Code, Cursor, Sentry AI | Emerging | Explain errors, suggest fixes from stack traces | Diagnostic de bugs et suggestion de correctifs |
| **Codebase Q&A** | Claude Code, Sourcegraph Cody, Cursor | Mature | Answer questions about any codebase via embedding search | Repondre aux questions sur n'importe quel codebase |

### Governance for AI-Generated Code

Establish clear policies for AI-generated code:

1. **Review requirement**: all AI-generated code must pass the same code review process as human-written code. No exceptions.
2. **Test requirement**: AI-generated code must have tests. AI is excellent at generating tests — use it for that too.
3. **License compliance**: verify that AI tools do not introduce license-incompatible code. Use tools like FOSSA or Snyk for license scanning.
4. **Attribution**: determine the team's policy on AI attribution (some organizations require `// AI-assisted` comments, others do not).
5. **Security review**: AI-generated code is especially prone to subtle security issues (SQL injection in generated queries, insecure defaults). Apply extra scrutiny.
6. **Measurement**: track AI tool adoption, developer satisfaction with AI tools, and impact on cycle time. Do not assume benefit — measure it.

**FR** — Etablir une gouvernance claire pour le code genere par l'IA : revue humaine obligatoire, tests obligatoires, conformite des licences, politique d'attribution, revue de securite renforcee, et mesure de l'impact. Ne jamais presumer du benefice — le mesurer.

---

## Platform Engineering

### What Is Platform Engineering

Platform engineering is the discipline of building and operating self-service internal developer platforms (IDPs) that enable product teams to deliver software with minimal friction. It applies product management principles to internal tools and infrastructure.

**Core concepts:**
- **Golden paths**: opinionated, well-supported default workflows that cover 80% of use cases. Teams can deviate but accept the maintenance burden.
- **Self-service**: developers provision infrastructure, create services, and configure deployments without filing tickets or waiting for a platform team.
- **Abstraction layers**: hide infrastructure complexity behind simple interfaces (Backstage templates, Terraform modules, Kubernetes operators).
- **Thinnest viable platform (TVP)**: start with the minimum platform that adds value. A TVP might be just a set of Terraform modules and a CI/CD template — not a full Backstage deployment.

### Platform Team Topology

Follow Team Topologies (Skelton & Pais) for platform team design:

- **Platform team**: builds and maintains the IDP. Operates as a product team with its own backlog, user research (developer surveys), and roadmap.
- **Enabling team**: helps stream-aligned teams adopt platform capabilities. Provides training, documentation, and hands-on support during migration.
- **Stream-aligned teams**: consume platform capabilities to deliver product features. They are the "customers" of the platform team.

**Sizing**: start with 2-3 engineers for a platform team serving 20-50 developers. Scale to 5-8 engineers for 50-200 developers. Above 200 developers, consider multiple specialized platform teams (CI/CD platform, infrastructure platform, developer portal team).

**FR** — Le platform engineering construit des plateformes internes self-service pour les developpeurs. Appliquer la pensee produit aux outils internes. Commencer par la plateforme viable la plus fine (TVP). Structurer l'equipe plateforme selon Team Topologies : equipe plateforme (construit l'IDP), equipe habilitante (aide a l'adoption), equipes alignees sur les flux (consomment la plateforme).

---

## The DevEx Framework

### Three Dimensions of Developer Experience

The DevEx framework (Noda, Storey et al., ACM Queue 2023) identifies three core dimensions that drive developer productivity:

**1. Flow State**
- The ability to enter and maintain a state of deep, focused work
- Measured by: frequency of interruptions, length of uninterrupted coding sessions, perceived ease of focus
- Improve by: reducing meetings, batching notifications, protecting "maker schedules," minimizing context switching between codebases or tools

**2. Feedback Loops**
- The speed and quality of feedback developers receive about their work
- Measured by: CI build time, PR review turnaround, time from code change to production, quality of error messages
- Improve by: faster CI (< 10 minutes), same-day PR reviews, preview environments per PR, better error messages and observability

**3. Cognitive Load**
- The mental effort required to complete tasks beyond the core problem-solving
- Measured by: number of tools to learn, complexity of local setup, documentation quality, number of manual steps in workflows
- Improve by: devcontainers, golden paths, automation, better documentation, reducing the number of tools

### Measuring DevEx

Run quarterly DX surveys using validated instruments:
- **DX Core 4** (getdx.com): standardized survey covering the three DevEx dimensions plus overall satisfaction. Enables benchmarking against industry data.
- **Custom surveys**: include questions about specific tooling, processes, and pain points. Use a mix of Likert scales (1-5) and open-ended questions.
- **System metrics**: complement surveys with objective data (CI build times, PR review times, environment setup time, deployment frequency).
- **Qualitative interviews**: conduct 30-minute 1:1 interviews with a representative sample of developers each quarter. Surface insights that surveys miss.

**FR** — Le framework DevEx identifie trois dimensions de l'experience developpeur : etat de flow (concentration), boucles de feedback (rapidite des retours), et charge cognitive (effort mental superflu). Mesurer avec des enquetes trimestrielles (DX Core 4), des metriques systeme (temps de CI, temps de review), et des entretiens qualitatifs.

---

## References

- Abi Noda, Margaret-Anne Storey et al., *DevEx: What Actually Drives Productivity* (ACM Queue, 2023)
- Matthew Skelton & Manuel Pais, *Team Topologies* (2019)
- Luca Mezzalira, *Building Micro-Frontends* (2021)
- Gregor Hohpe, *The Software Architect Elevator* (2020)
- Backstage documentation — backstage.io/docs
- Port documentation — docs.getport.io
- Dev Containers specification — containers.dev
- Nix documentation — nix.dev
- Diátaxis documentation framework — diataxis.fr
- DX (getdx.com) — Developer Experience measurement platform
- *State of Developer Experience Report* — DX (annual)
- Gergely Orosz, *The Pragmatic Engineer* — platform engineering and DX articles
