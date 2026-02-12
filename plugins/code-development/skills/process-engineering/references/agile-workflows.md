# Agile Workflows — Sprint Planning, Estimation, Story Mapping & Backlog Management

## Vue d'ensemble / Overview

**FR** — Ce document de reference couvre l'ensemble des pratiques agiles modernes pour la gestion du flux de travail : planification de sprint, techniques d'estimation, story mapping, gestion du backlog, Definition of Done et Definition of Ready, automatisation des workflows et comparaison des outils de suivi. Il integre les approches recentes (2024-2026) incluant l'estimation probabiliste, le no-estimates, les workflows IA-augmentes et les methodes hybrides combinant Scrum et Kanban. L'objectif est de fournir un guide actionnable pour construire des workflows agiles matures, adaptes au contexte de l'equipe, et qui maximisent le flux de valeur vers l'utilisateur final.

**EN** — This reference document covers the full spectrum of modern agile workflow practices: sprint planning, estimation techniques, story mapping, backlog management, Definition of Done and Definition of Ready, workflow automation, and issue tracking tool comparison. It incorporates recent approaches (2024-2026) including probabilistic estimation, no-estimates, AI-augmented workflows, and hybrid methods combining Scrum and Kanban. The goal is to provide an actionable guide for building mature agile workflows, adapted to the team's context, that maximize the flow of value to the end user.

---

## Sprint Planning

### The Sprint Planning Ceremony

Structure sprint planning as a two-part ceremony to maximize focus and minimize waste:

**Part 1 — What (30-60 minutes)**
1. Review the sprint goal proposed by the Product Owner. Ensure it aligns with the current product roadmap and OKRs.
2. Walk through the top of the prioritized backlog. The PO explains the "why" behind each candidate story.
3. The team selects stories that contribute to the sprint goal. Reject work that does not align — this is the hardest and most important discipline.
4. Validate that all selected stories meet the Definition of Ready. Return unready items to the backlog for refinement.

**Part 2 — How (30-60 minutes)**
1. Break selected stories into technical tasks. Identify implementation approaches, dependencies, and risks.
2. Assign initial owners (or let team members self-select in pull-based models).
3. Validate sprint capacity: account for vacations, on-call rotations, planned meetings, and maintenance work. Never plan at 100% capacity — 70-80% is sustainable.
4. Confirm the sprint commitment as a team. The sprint backlog belongs to the team, not the PO.

**FR** — Structurer la planification de sprint en deux parties : le "quoi" (selection alignee sur l'objectif du sprint) et le "comment" (decomposition technique). Ne jamais planifier a 100% de capacite — viser 70-80% pour absorber les imprevus et la maintenance.

### Sprint Cadence Selection

| Cadence | When to use | FR |
|---|---|---|
| **1 week** | Fast-moving products, high uncertainty, need for rapid feedback. Requires mature CI/CD. | Produits rapides, forte incertitude, besoin de feedback rapide |
| **2 weeks** | Most common default. Balances planning overhead with delivery rhythm. | Defaut le plus courant. Equilibre entre overhead de planification et rythme de livraison |
| **3 weeks** | Complex domains (embedded, hardware-software). Rarely recommended for pure software. | Domaines complexes. Rarement recommande pour du logiciel pur |
| **Continuous flow (Kanban)** | Maintenance teams, ops teams, mature teams with small well-defined items. No fixed sprint boundary. | Equipes maintenance/ops, equipes matures avec items bien definis |

### Sprint Goal Best Practices

- Write the sprint goal as a single sentence that answers "what value will we deliver to users this sprint?"
- Make it measurable: "Users can complete checkout with Apple Pay" not "Work on payments"
- Display it visibly on the team board. Reference it in daily standups.
- If mid-sprint changes invalidate the sprint goal, the PO and team renegotiate — never silently replace the goal.

---

## Estimation Techniques

### Story Points (Fibonacci Scale)

Use the modified Fibonacci sequence (1, 2, 3, 5, 8, 13, 21) for relative estimation. Story points measure complexity, uncertainty, and effort — not time.

**How to run Planning Poker:**
1. PO reads the story and acceptance criteria. Team asks clarifying questions.
2. Each team member privately selects a card (use apps like Planit Poker, Pointing Poker, or native tool integrations).
3. All cards are revealed simultaneously. If consensus exists (all within 1 step), accept the estimate.
4. If divergence exists, the highest and lowest estimators explain their reasoning. Discuss for maximum 2 minutes.
5. Re-vote once. Accept the majority. If still divergent after 2 rounds, take the higher estimate and move on.
6. Any story estimated at 13+ should be split. Stories at 21 are epics in disguise.

**FR** — Utiliser l'echelle de Fibonacci modifiee pour l'estimation relative. Les story points mesurent la complexite, l'incertitude et l'effort — pas le temps. Time-boxer le debat a 2 minutes par story. Toute story a 13+ doit etre decoupee.

**Calibration**: maintain a reference story sheet with 2-3 example stories for each point value. Review and update it quarterly. New team members study this sheet before their first planning poker.

### T-Shirt Sizing (S, M, L, XL)

Use t-shirt sizing for high-level roadmap estimation and early-stage backlog grooming where precision is not needed.

| Size | Relative effort | Typical conversion | FR |
|---|---|---|---|
| **S** | Trivial, well-understood, < 1 day | 1-2 story points | Trivial, bien compris |
| **M** | Moderate complexity, 2-3 days | 3-5 story points | Complexite moderee |
| **L** | Significant work, multiple components | 8-13 story points | Travail significatif, plusieurs composants |
| **XL** | Too large — must be split before commitment | 13+ — split required | Trop gros — decoupage obligatoire |

**When to use**: roadmap planning sessions with stakeholders, epic-level estimation, portfolio prioritization. Never use t-shirt sizes for sprint commitment — convert to story points or use no-estimates.

### No Estimates (#NoEstimates)

The no-estimates approach works for mature teams operating in continuous flow. Instead of estimating individual stories, rely on:

1. **Right-sizing stories**: enforce that every story is small enough to complete within 1-2 days. If it is larger, split it.
2. **Throughput-based forecasting**: track how many stories the team completes per week. Use this throughput rate for planning.
3. **Monte Carlo simulation**: use historical throughput data to generate probabilistic forecasts. "We have an 85% probability of completing these 30 items in 6 weeks."

**Prerequisites for no-estimates to work:**
- Team has 3+ months of consistent throughput data
- Stories are consistently right-sized (low variance in cycle time)
- High trust between team and stakeholders
- Continuous flow or very short sprints (1 week)

**FR** — L'approche no-estimates fonctionne pour les equipes matures en flux continu. Au lieu d'estimer individuellement chaque story, imposer un decoupage fin (1-2 jours par story) et utiliser le debit historique pour des previsions probabilistes (simulation Monte Carlo).

### Cycle Time Forecasting with Monte Carlo

Monte Carlo simulation is the most rigorous estimation approach available. Use it for release planning and stakeholder commitments.

**How to implement:**
1. Collect historical cycle time data for the past 3-6 months (time from "In Progress" to "Done" for each work item).
2. Run 10,000 simulations: for each remaining item, randomly sample a cycle time from the historical distribution.
3. Sum the simulated cycle times to get a total project duration.
4. Plot the cumulative probability: "50% chance of finishing by March 15, 85% chance by March 29, 95% chance by April 5."

**Tools**: ActionableAgile (from Kanban University), Jira plugins (Portfolio, Advanced Roadmaps), custom Python scripts with NumPy, or dedicated forecasting tools like Nave.

---

## Story Mapping

### Jeff Patton's User Story Mapping

Use story mapping to visualize the user journey and prioritize the backlog based on user value rather than arbitrary ordering.

**How to run a story mapping workshop (2-4 hours):**

1. **Frame the narrative** — Define the target persona and their primary goal. Write it at the top of the map: "As a [persona], I want to [goal] so that [benefit]."

2. **Map the backbone (activities)** — Identify the major activities the user performs, left to right in chronological order. These become the horizontal backbone of the map. Example: Browse -> Search -> Select -> Purchase -> Receive.

3. **Add user tasks under each activity** — Break each activity into specific tasks the user performs. These go vertically under each activity, roughly ordered from essential (top) to nice-to-have (bottom).

4. **Draw release slices** — Draw horizontal lines across the map to define release boundaries:
   - **Release 1 (MVP)**: the minimum set of tasks that delivers a usable end-to-end experience. Walk the map left-to-right — every activity must have at least one task in Release 1.
   - **Release 2**: enhanced experience, additional task completions.
   - **Release 3+**: full feature set, edge cases, optimizations.

5. **Convert to backlog items** — Each task on the map becomes a user story. The vertical position within a release slice determines priority.

**FR** — Utiliser le story mapping pour visualiser le parcours utilisateur et prioriser le backlog par la valeur. Mapper le backbone (activites utilisateur de gauche a droite), ajouter les taches sous chaque activite, puis tracer des lignes horizontales pour definir les tranches de release. Chaque activite doit avoir au moins une tache dans le MVP.

### Story Splitting Techniques

When a story is too large (> 8 points or > 3 days), split it using these patterns:

| Pattern | Description | Example | FR |
|---|---|---|---|
| **Workflow steps** | Split by steps in the user flow | "Add to cart" vs "Apply coupon" vs "Checkout" | Decouper par etapes du flux utilisateur |
| **Business rules** | Split by rule variations | "Calculate tax for domestic" vs "Calculate tax for international" | Decouper par regles metier |
| **Data variations** | Split by input types | "Import CSV" vs "Import Excel" vs "Import JSON" | Decouper par types de donnees |
| **Happy path / edge cases** | Deliver the main scenario first | "Login with email" (happy) vs "Login with expired password" (edge) | Scenario principal d'abord, cas limites ensuite |
| **Operations (CRUD)** | Split by operation type | "View orders" vs "Cancel order" vs "Reorder" | Decouper par type d'operation |
| **Platform / interface** | Split by platform | "Mobile checkout" vs "Desktop checkout" | Decouper par plateforme |
| **Spike + implementation** | Research first, build second | "Spike: evaluate payment providers" then "Implement Stripe integration" | Recherche d'abord, implementation ensuite |

---

## Backlog Grooming (Refinement)

### Refinement Best Practices

Hold backlog refinement sessions regularly (1-2 times per week, 30-60 minutes each). This is the most valuable ceremony for sprint predictability.

1. **Prepare before the session**: the PO selects 5-10 items from the top of the backlog. Write preliminary acceptance criteria. Attach mockups or specs if available.
2. **Walk through each item**: PO explains the business context and desired outcome. Team asks questions until they understand the "what" and "why."
3. **Write acceptance criteria collaboratively**: use the Given/When/Then format for clarity. Each story should have 3-7 acceptance criteria.
4. **Estimate if the team uses story points**: run quick planning poker (1 minute per item max if well-refined).
5. **Check the Definition of Ready**: verify that each refined item meets all DoR criteria. If not, identify the missing pieces and assign owners to complete them before the next planning session.
6. **Split stories that are too large**: apply the splitting techniques above. Target stories completable in 1-3 days.

**FR** — Tenir des sessions de refinement 1 a 2 fois par semaine (30-60 min). Preparer les items en amont, ecrire les criteres d'acceptation en Given/When/Then, estimer rapidement, verifier la Definition of Ready, et decouper les stories trop grosses.

### Backlog Prioritization Frameworks

| Framework | Method | Best for | FR |
|---|---|---|---|
| **MoSCoW** | Must/Should/Could/Won't | Release scoping with stakeholders | Cadrage de release avec les parties prenantes |
| **WSJF (Weighted Shortest Job First)** | Value / Duration. Prioritize high-value, low-effort items first | SAFe environments, economic prioritization | Environnements SAFe, priorisation economique |
| **RICE** | Reach x Impact x Confidence / Effort | Product-led growth, data-driven prioritization | Croissance produit, priorisation data-driven |
| **Cost of Delay** | Quantify the economic cost of not delivering a feature now | When features have time-sensitive value (regulatory, seasonal) | Quand les features ont une valeur sensible au temps |
| **Value vs. Effort Matrix** | 2x2 quadrant: quick wins, strategic bets, fill-ins, avoid | Simple visual prioritization for team workshops | Priorisation visuelle simple pour ateliers d'equipe |

---

## Definition of Done (DoD) & Definition of Ready (DoR)

### Definition of Ready (DoR) — Entry Criteria

A story is "ready" for sprint planning when it meets ALL of the following criteria. Adapt this template to the team's context:

- [ ] User story follows the standard format: "As a [role], I want [action] so that [benefit]"
- [ ] Acceptance criteria are written in Given/When/Then format (3-7 criteria per story)
- [ ] UX designs or mockups are attached and approved (if UI-related)
- [ ] Technical dependencies are identified and resolved (or explicitly flagged)
- [ ] The story is estimated (story points or t-shirt size)
- [ ] The story is small enough to complete within the sprint (< 8 points or < 3 days)
- [ ] Edge cases and error scenarios are documented
- [ ] API contracts are defined (if applicable)
- [ ] Test scenarios are outlined (manual or automated)

**FR** — La Definition of Ready definit les criteres d'entree dans le sprint. Une story n'est jamais prise en sprint si elle ne respecte pas tous les criteres. Adapter ce template au contexte de l'equipe.

### Definition of Done (DoD) — Exit Criteria

A story is "done" when it meets ALL of the following criteria:

- [ ] Code is written, reviewed (PR approved by at least 1 peer), and merged to main
- [ ] All acceptance criteria pass (automated or manual verification)
- [ ] Unit tests written and passing (coverage target met for new code)
- [ ] Integration tests written for new API endpoints or service interactions
- [ ] No critical or high-severity static analysis warnings introduced
- [ ] API documentation updated (OpenAPI spec if applicable)
- [ ] Feature is deployable to production (behind feature flag if needed)
- [ ] Monitoring and alerting are configured for new functionality
- [ ] Runbook updated if operational impact exists
- [ ] Product Owner has accepted the story in a demo or review

**FR** — La Definition of Done definit les criteres de sortie du sprint. Aucune story n'est consideree terminee tant que tous les criteres ne sont pas remplis. Inclure les tests, la revue de code, la documentation et la validite operationnelle.

---

## Workflow Automation

### Automating Agile Ceremonies and Processes

Reduce toil and improve consistency by automating repetitive workflow steps:

| Automation | Tool / Approach | Impact | FR |
|---|---|---|---|
| **PR-to-story linking** | GitHub Actions, Linear Git integrations, Jira Smart Commits | Auto-move stories when PRs are opened/merged | Lier automatiquement les PRs aux stories |
| **Sprint reports** | Jira Dashboards, Linear Cycles, custom Slack bots | Auto-generate velocity, burndown, and completion reports | Generer automatiquement les rapports de sprint |
| **Stale item detection** | Scheduled scripts, Jira automation rules | Flag items untouched for 2+ sprints | Detecter les items inactifs depuis 2+ sprints |
| **DoR validation** | GitHub issue templates, Linear templates, custom bots | Enforce required fields before an item can enter "Ready" | Valider la Definition of Ready automatiquement |
| **Release notes** | Conventional Commits + auto-changelog (release-please, semantic-release) | Auto-generate changelogs from commit messages | Generer automatiquement les release notes |
| **Retrospective facilitation** | EasyRetro, Retrium, Parabol, or Slack-based retro bots | Collect feedback asynchronously, facilitate voting | Faciliter les retrospectives de maniere asynchrone |
| **Sprint kickoff notifications** | Slack/Teams integrations | Auto-post sprint goal, team capacity, and key stories at sprint start | Notifier automatiquement le lancement du sprint |

### AI-Augmented Workflow Automation (2024-2026)

- **Automated story writing**: use LLMs to generate draft user stories from product briefs or feature requests. Human refinement remains mandatory.
- **Acceptance criteria suggestions**: AI tools can suggest Given/When/Then criteria based on story descriptions and historical patterns.
- **Dependency detection**: AI-powered tools can analyze story descriptions and code repositories to identify potential technical dependencies.
- **Effort prediction**: machine learning models trained on historical team data can predict cycle time for new stories based on text similarity.
- **Retro theme extraction**: use NLP to cluster retrospective feedback into themes and track recurring issues across sprints.

**FR** — Les outils d'IA augmentent les workflows agiles en 2024-2026 : generation de stories a partir de briefs produit, suggestion de criteres d'acceptation, detection de dependances, prediction d'effort, et extraction de themes de retrospective. La validation humaine reste obligatoire.

---

## Issue Tracking Tools Comparison

### 2024-2026 Landscape

| Tool | Strengths | Weaknesses | Best for | FR — Ideal pour |
|---|---|---|---|---|
| **Linear** | Blazing fast UI, keyboard-first, opinionated workflow, excellent cycles feature, Git integration | Limited custom fields, less flexible reporting, smaller ecosystem | Startups, product teams valuing speed and simplicity | Startups, equipes produit privilegiant la rapidite |
| **Jira** | Extremely configurable, massive ecosystem, advanced reporting (JQL), compliance features, SAFe support | Slow UI, configuration complexity, over-customization leads to chaos | Enterprise, regulated industries, scaled agile (SAFe) | Entreprises, industries reglementees, agile a echelle |
| **Shortcut (ex-Clubhouse)** | Good balance of simplicity and power, strong API, milestones feature | Smaller ecosystem, less mature than Jira | Mid-size product teams wanting balance | Equipes produit mid-size |
| **GitHub Projects** | Native GitHub integration, free for public repos, table/board/roadmap views | Limited ceremony support, basic reporting, not for non-engineering stakeholders | Open-source projects, small teams already on GitHub | Projets open-source, petites equipes sur GitHub |
| **Azure DevOps** | Deep Microsoft/Azure integration, full ALM suite, strong for .NET teams | Dated UI, Microsoft-centric, complex configuration | Enterprise Microsoft shops | Entreprises Microsoft |
| **Notion** | Flexible databases, combines docs and project tracking, good for cross-functional teams | Not purpose-built for agile, lacks burndown/velocity natively | Cross-functional teams, early-stage companies | Equipes cross-fonctionnelles, startups early-stage |
| **Plane** | Open-source Jira/Linear alternative, self-hostable, modern UI | Young project, smaller community, fewer integrations | Teams wanting open-source with modern UX | Equipes voulant de l'open-source avec UX moderne |

### Migration Guidance

When migrating between issue trackers:
1. Export historical data (stories, epics, sprints) before migration. Preserve velocity history.
2. Map custom fields and workflows between tools before starting.
3. Run both tools in parallel for 1-2 sprints to validate the new setup.
4. Clean up old tool access after migration is confirmed successful.
5. Update all automation integrations (CI/CD links, Slack notifications, dashboards).

---

## Agile at Scale

### Framework Comparison

| Framework | Team size | Philosophy | Complexity | FR |
|---|---|---|---|---|
| **Scrum of Scrums** | 2-5 teams | Lightweight coordination across Scrum teams | Low | Coordination legere entre equipes Scrum |
| **LeSS (Large-Scale Scrum)** | 2-8 teams | Scrum with minimal additions; one product backlog, one PO | Medium | Scrum avec ajouts minimaux |
| **Nexus** | 3-9 teams | Scrum.org scaling framework; Nexus integration team | Medium | Framework de scaling Scrum.org |
| **SAFe** | 50-125+ people | Comprehensive; ARTs, PI Planning, solution trains | High | Comprehensif; pour grandes organisations |
| **Spotify Model** | Varies | Squads, tribes, chapters, guilds (cultural model, not a framework) | Medium | Modele culturel, pas un framework |
| **Flight Levels** | Varies | Focus on coordination levels (operational, coordination, strategic) | Low-Medium | Focus sur les niveaux de coordination |

**Recommendation**: start with the simplest approach (Scrum of Scrums or LeSS) and add complexity only when proven necessary. SAFe is warranted only for very large organizations with strong compliance needs. Never adopt the Spotify Model as a framework — it was a description of Spotify's culture at a point in time, not a prescriptive methodology.

**FR** — Commencer par l'approche la plus simple (Scrum of Scrums ou LeSS) et n'ajouter de la complexite que si c'est prouve necessaire. SAFe n'est justifie que pour de tres grandes organisations. Ne jamais adopter le modele Spotify comme un framework — c'etait une description culturelle, pas une methodologie prescriptive.

---

## Continuous Flow with Kanban

### When to Use Kanban Over Scrum

Adopt Kanban (or Scrumban hybrid) when:
- The team handles a mix of planned work and unplanned requests (support, bugs, ops)
- Work items are small and relatively uniform in size
- The team is mature enough to self-manage without sprint boundaries
- Stakeholders accept "continuous delivery" rather than sprint-based commitments

### Kanban Core Practices

1. **Visualize the workflow**: map each state a work item passes through (Backlog -> Ready -> In Progress -> Review -> Testing -> Done).
2. **Limit Work in Progress (WIP)**: set explicit WIP limits per column. Start with the formula: WIP limit = number of team members x 1.5, rounded down. Adjust based on experience.
3. **Manage flow**: focus on reducing cycle time and increasing throughput. Use cumulative flow diagrams to identify bottlenecks.
4. **Make policies explicit**: write column entry/exit criteria. Display them on the board.
5. **Implement feedback loops**: daily standup (walk the board right-to-left), weekly replenishment meeting, monthly service delivery review.
6. **Improve collaboratively, evolve experimentally**: use data (cycle time, throughput, WIP age) to drive improvement experiments.

**FR** — Adopter Kanban quand l'equipe gere un mix de travail planifie et non planifie, que les items sont petits et uniformes, et que l'equipe est suffisamment mature pour s'autogerir sans frontieres de sprint. Limiter le WIP, visualiser le flux, et utiliser les donnees (cycle time, throughput) pour piloter l'amelioration.

---

## References

- Jeff Patton, *User Story Mapping* (2014)
- Mike Cohn, *Agile Estimating and Planning* (2005)
- Daniel Vacanti, *Actionable Agile Metrics for Predictability* (2015)
- Daniel Vacanti, *When Will It Be Done?* (2020) — Monte Carlo forecasting
- David Anderson, *Kanban: Successful Evolutionary Change* (2010)
- Henrik Kniberg, *Scrum and XP from the Trenches* (2007, 2015)
- Vasco Duarte, *No Estimates* (2016)
- SAFe Framework — scaledagileframework.com
- LeSS Framework — less.works
- Kanban University — kanban.university
