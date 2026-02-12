# Alerting & Incident Management / Alerting et gestion des incidents

## Introduction

Effective alerting and incident management separate resilient organizations from those drowning in firefighting. This reference covers alert design principles, on-call management, the complete incident response lifecycle, blameless post-mortems, and the tools that support these processes. The goal is sustainable operations: teams that respond effectively to real incidents without burning out from noise.

Un alerting efficace et une gestion d'incidents mature différencient les organisations résilientes de celles submergées par le firefighting. Cette référence couvre les principes de conception d'alertes, la gestion d'astreinte, le cycle complet de réponse aux incidents, les post-mortems sans blâme, et les outils qui supportent ces processus.

---

## 1. Alert Design / Conception des alertes

### The Five Properties of Good Alerts / Les cinq propriétés d'une bonne alerte

Every alert in the system must satisfy all five criteria. If an alert fails any criterion, fix or remove it.

Chaque alerte doit satisfaire les cinq critères. Si une alerte échoue sur un critère, la corriger ou la supprimer.

#### 1. Actionable / Actionnable

The alert requires a human to take a specific action. If the correct response is "wait and see" or "it will auto-resolve," it is not worth paging a human. Automate the response or downgrade to a ticket.

L'alerte nécessite qu'un humain prenne une action spécifique. Si la réponse correcte est « attendre » ou « ça va se résoudre seul », ce n'est pas une alerte digne d'un page.

#### 2. Meaningful / Significative

The alert represents a real impact on users or a genuine risk to the business. Alerting on proxy metrics (CPU > 80%) is only valuable if it correlates with user impact. Prefer SLO-based alerts that directly measure user experience.

L'alerte représente un impact réel sur les utilisateurs ou un risque véritable pour le business.

#### 3. Urgent / Urgente

The alert requires attention within minutes or hours, not days. If it can wait until the next business day, route it to a ticket queue, not to a pager.

L'alerte nécessite une attention dans les minutes ou les heures, pas les jours.

#### 4. Contextualized / Contextualisée

The alert provides enough context for the responder to begin investigation immediately: which service, which environment, current values, thresholds, links to dashboards and runbooks.

L'alerte fournit assez de contexte pour que le répondant commence l'investigation immédiatement.

#### 5. Novel / Nouvelle

The alert is not a duplicate of another alert firing simultaneously. Use alert grouping, deduplication, and correlation to avoid paging the same person for the same root cause via multiple alerts.

L'alerte n'est pas un doublon d'une autre alerte déjà active.

### Alert Template / Template d'alerte

```yaml
# Example Prometheus AlertManager alert
alert: PaymentServiceHighErrorRate
expr: |
  (
    sum(rate(http_requests_total{service="payment-api", status=~"5.."}[5m]))
    /
    sum(rate(http_requests_total{service="payment-api"}[5m]))
  ) > 0.01
for: 3m
labels:
  severity: critical
  team: payments
  slo: payment-availability
annotations:
  summary: "Payment API error rate is {{ $value | humanizePercentage }} (> 1%)"
  description: |
    The payment-api service is returning server errors at a rate of
    {{ $value | humanizePercentage }} over the last 5 minutes.

    This is impacting the payment-availability SLO.
    Current error budget remaining: {{ template "error_budget" . }}

  dashboard_url: "https://grafana.internal/d/payment-overview"
  runbook_url: "https://runbooks.internal/payment-high-error-rate"
  escalation: "If not resolved within 30 minutes, escalate to payments-oncall-secondary"
```

### Alert Routing / Routage des alertes

Configure alert routing based on severity, team ownership, and time of day:

```yaml
# AlertManager routing configuration
route:
  receiver: default-slack
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h

  routes:
    # Critical alerts → PagerDuty (24/7 paging)
    - match:
        severity: critical
      receiver: pagerduty-critical
      repeat_interval: 15m
      continue: true

    # Warning alerts → Slack during business hours, PagerDuty otherwise
    - match:
        severity: warning
      receiver: slack-warnings
      active_time_intervals:
        - business-hours
    - match:
        severity: warning
      receiver: pagerduty-warning
      active_time_intervals:
        - outside-business-hours

    # Info alerts → Slack only, no paging
    - match:
        severity: info
      receiver: slack-info
      repeat_interval: 24h
```

### Alert Hygiene / Hygiène des alertes

Conduct quarterly alert reviews:

1. **Audit every alert**: For each alert that fired in the last quarter, classify as: Actionable (led to a human action), False positive (no real issue), Noise (real but not worth paging).
2. **Calculate alert quality ratio**: `Actionable Alerts / Total Alerts`. Target > 80%.
3. **Remove or fix bad alerts**: Delete alerts with < 50% actionable rate. Tune thresholds. Add deduplication.
4. **Review coverage**: Identify incidents that were NOT detected by alerts. Add missing alerts.
5. **Track metrics**: Alert volume per week, mean time to acknowledge, false positive rate.

Mener des revues d'alertes trimestrielles. Auditer chaque alerte. Calculer le ratio de qualité des alertes. Supprimer ou corriger les mauvaises alertes. Viser > 80% d'alertes actionnables.

### Alert Severity Levels / Niveaux de sévérité des alertes

| Severity | Description | Response Time | Notification |
|---|---|---|---|
| **SEV1 / Critical** | Complete service outage or data loss affecting all users | < 15 min | Page on-call immediately, 24/7 |
| **SEV2 / High** | Major degradation affecting significant portion of users | < 30 min | Page during business hours, Slack 24/7 |
| **SEV3 / Medium** | Partial degradation, workaround available | < 4 hours | Slack notification, ticket created |
| **SEV4 / Low** | Minor issue, cosmetic, or preemptive warning | Next business day | Ticket only |

---

## 2. On-Call Management / Gestion de l'astreinte

### On-Call Rotation Design / Conception des rotations d'astreinte

#### Rotation Structure / Structure de rotation

- **Primary on-call**: First responder for all pages. Rotates weekly.
- **Secondary on-call**: Backup if primary does not acknowledge within SLA (typically 15 minutes). Provides expertise escalation.
- **Specialist on-call** (optional): Domain experts (database, networking, security) available for escalation during complex incidents.

**Rotation length**: Use weekly rotations (Monday 10:00 to Monday 10:00). Avoid daily rotations (too many handoffs) and bi-weekly rotations (too long, leads to burnout). Overlap handoffs by 30 minutes for warm transfer.

**Durée de rotation** : Utiliser des rotations hebdomadaires. Éviter les rotations quotidiennes (trop de handoffs) et bi-hebdomadaires (trop long, mène au burn-out).

#### On-Call Expectations / Attentes d'astreinte

Document clearly for every on-call participant:

1. **Acknowledge pages within 5 minutes** (configurable per org).
2. **Begin investigation within 15 minutes** of acknowledgment.
3. **Laptop and connectivity required** throughout the on-call shift.
4. **No alcohol or substances** that impair judgment during on-call.
5. **Escalate early**: If unsure or unable to resolve within 30 minutes, escalate to secondary or specialist.
6. **Handoff notes**: Write a brief summary at the end of each shift documenting open issues and ongoing investigations.

#### On-Call Compensation / Compensation de l'astreinte

On-call is real work that impacts personal life. Compensate it:

- **Paid on-call stipend**: Fixed amount per on-call shift (common: $200-500/week in US, adapt to local market).
- **Time-off-in-lieu**: Comp time for incidents handled outside business hours.
- **Page load limits**: If an on-call engineer is paged more than N times in a shift, provide additional time off and investigate alert quality.

### On-Call Health Metrics / Métriques de santé d'astreinte

Track and optimize:

| Metric | Target | Why |
|---|---|---|
| Pages per on-call shift | < 5 | Sustainable operations |
| Mean time to acknowledge | < 5 minutes | Rapid response |
| Incidents per shift | < 2 | Manageable workload |
| False positive rate | < 20% | Alert quality |
| After-hours pages | < 2/week | Work-life balance |
| Escalation rate | < 30% | Primary can handle most issues |

---

## 3. Incident Response Process / Processus de réponse aux incidents

### Incident Lifecycle / Cycle de vie d'un incident

```
Detection → Triage → Response → Mitigation → Resolution → Post-Mortem → Improvement
```

### Phase 1: Detection / Détection

Incidents are detected through:
- **Automated alerts** (primary method): SLO burn-rate alerts, threshold alerts, anomaly detection.
- **User reports**: Support tickets, social media mentions, status page reports.
- **Internal discovery**: Engineer notices anomaly during routine work.
- **Synthetic monitoring**: Uptime checks and synthetic transaction failures.

**Target**: Detect 90%+ of incidents through automated alerts before users report them. Track the detection source for every incident.

**Cible** : Détecter 90%+ des incidents via des alertes automatisées avant les signalements utilisateurs.

### Phase 2: Triage / Triage

Within the first 5 minutes:

1. **Assess severity**: Determine SEV level based on user impact scope and business criticality.
2. **Declare the incident**: Create an incident in the incident management tool (Incident.io, PagerDuty, OpsGenie).
3. **Open a communication channel**: Dedicated Slack channel (`#inc-YYYY-MM-DD-short-description`) or video call for SEV1/SEV2.
4. **Assign roles**: Incident Commander (IC), Communications Lead, Technical Lead(s).

### Phase 3: Roles During Incident / Rôles pendant l'incident

#### Incident Commander (IC) / Commandant d'incident

The IC owns the incident process, not the technical resolution:

- Maintain the incident timeline and status
- Coordinate between technical teams
- Make decisions about escalation, communication, and scope
- Ensure the right people are involved
- Drive toward mitigation, then resolution
- Prevent tunnel vision (ensure multiple hypotheses are explored)

Le IC gère le processus d'incident, pas la résolution technique. Coordonner, décider des escalades, et conduire vers la mitigation.

#### Communications Lead / Responsable communication

- Post regular updates to the status page (every 15-30 minutes for SEV1)
- Update internal stakeholders (leadership, support, sales)
- Draft customer communications
- Manage the incident Slack channel (prevent noise, summarize progress)

#### Technical Lead(s) / Lead(s) technique(s)

- Investigate root cause
- Implement mitigation (rollback, failover, scaling, feature flag toggle)
- Coordinate with other teams if cross-service
- Document technical findings in real-time

### Phase 4: Mitigation / Mitigation

The priority is always **mitigate first, debug later**. Restore service before understanding root cause.

La priorité est toujours **mitiger d'abord, débugger ensuite**. Restaurer le service avant de comprendre la cause racine.

Common mitigation strategies:

| Strategy | When to Use | Example |
|---|---|---|
| **Rollback** | Recent deployment caused the issue | `kubectl rollout undo deployment/api` |
| **Feature flag toggle** | New feature causing errors | Disable `new-checkout-flow` flag |
| **Scale up** | Traffic spike overwhelming capacity | Increase replica count or instance size |
| **Failover** | Region or dependency failure | Switch traffic to secondary region |
| **Rate limit** | Abuse or unexpected traffic pattern | Enable emergency rate limits |
| **Circuit breaker** | Cascading failure from dependency | Trip circuit breaker to failing dependency |
| **Cache bypass** | Stale cache causing errors | Invalidate and rebuild cache |

### Phase 5: Resolution / Résolution

After mitigation:

1. Confirm service has recovered (SLIs are back within SLO).
2. Verify no lingering effects (data inconsistencies, stuck queues).
3. Remove any temporary mitigations (replace with permanent fix).
4. Close the incident with a summary.
5. Schedule the post-mortem within 48 hours (for SEV1/SEV2) or 1 week (SEV3).

### Incident Communication Template / Template de communication d'incident

#### Status Page Update (During Incident)

```
[INVESTIGATING] Elevated error rates on Payment API
Posted: 2025-06-15 14:23 UTC

We are investigating elevated error rates affecting payment processing.
Some users may experience failed transactions. Our team is actively
working on resolution.

Next update in 30 minutes or sooner if status changes.
```

#### Status Page Update (Resolved)

```
[RESOLVED] Elevated error rates on Payment API
Posted: 2025-06-15 14:23 UTC | Resolved: 2025-06-15 15:47 UTC

A configuration change to the payment processing service caused elevated
error rates between 14:15 and 15:42 UTC. Approximately 3% of payment
transactions failed during this window. The configuration has been rolled
back and all systems are operating normally.

Affected customers will see failed transactions automatically retried.
No action is required. A full post-mortem will be conducted.
```

---

## 4. Post-Mortem / Blameless Retrospectives / Rétrospectives sans blâme

### Principles / Principes

The post-mortem is the single most important reliability improvement tool. Get it right.

Le post-mortem est l'outil d'amélioration de fiabilité le plus important. Le faire correctement.

1. **Blameless**: Never identify individuals as the "cause." Humans make mistakes; the system should be resilient to human error. Replace "John deployed the bad config" with "The deployment pipeline accepted a configuration that caused errors."

2. **Timely**: Conduct the post-mortem within 48 hours for SEV1/SEV2 (while memory is fresh), within 1 week for SEV3.

3. **Thorough**: Include all relevant context, timeline, and contributing factors. Shallow post-mortems produce shallow improvements.

4. **Action-oriented**: Every post-mortem must produce concrete, assigned, time-bound action items. Track them to completion.

5. **Shared**: Publish post-mortems to the whole organization. Transparency builds trust and enables cross-team learning.

**Sans blâme** : Ne jamais identifier des individus comme « la cause ». Remplacer « Jean a déployé la mauvaise config » par « Le pipeline de déploiement a accepté une configuration causant des erreurs ».

### Post-Mortem Template / Template de post-mortem

```markdown
# Post-Mortem: [Incident Title]

**Date**: 2025-06-15
**Severity**: SEV1
**Duration**: 1h 27m (14:15 - 15:42 UTC)
**Impact**: 3% of payment transactions failed. ~450 users affected.
           Estimated revenue impact: €12,300.
**Author**: [IC Name]
**Reviewers**: [Team leads, stakeholders]

## Summary / Résumé

One paragraph describing what happened, the impact, and how it was resolved.

## Timeline / Chronologie

| Time (UTC) | Event |
|---|---|
| 14:10 | Deployment v2.4.1 rolled out to production via automated pipeline |
| 14:15 | Error rate begins increasing on payment-api |
| 14:18 | SLO burn-rate alert fires (14.4x burn rate detected on 5m window) |
| 14:20 | On-call engineer acknowledges alert, begins investigation |
| 14:25 | Incident declared as SEV1, Slack channel #inc-2025-06-15-payment created |
| 14:28 | IC identifies recent deployment as potential cause |
| 14:32 | Decision to rollback deployment v2.4.1 |
| 14:35 | Rollback initiated via `kubectl rollout undo` |
| 14:42 | Rollback complete, new pods healthy |
| 14:50 | Error rate returns to baseline, SLI recovering |
| 15:42 | SLO burn-rate alert resolves. Incident marked as resolved. |

## Root Cause Analysis / Analyse de cause racine

### What happened / Ce qui s'est passé
Deployment v2.4.1 included a database migration that added an index
concurrently. The migration locked the payments table for ~25 minutes
under high load, causing connection pool exhaustion and cascading timeouts.

### Contributing factors / Facteurs contributifs
1. The migration was not tested under production-level load.
2. Database migrations run during peak traffic hours (no deployment
   window policy).
3. The connection pool timeout was set to 30s, causing requests to queue
   rather than fail fast.

### Five Whys / Cinq pourquoi

1. **Why did payments fail?** → Database connections were exhausted.
2. **Why were connections exhausted?** → A table lock held connections
   for 25 minutes.
3. **Why was the table locked?** → The migration added an index that
   acquired a lock under load.
4. **Why was the migration run under load?** → No policy restricting
   migration timing.
5. **Why was the impact not caught in staging?** → Staging does not
   replicate production traffic volume.

## Action Items / Actions correctives

| ID | Action | Owner | Priority | Due Date | Status |
|---|---|---|---|---|---|
| 1 | Add load-test gate for database migrations in CI/CD | @platform-team | P1 | 2025-06-22 | TODO |
| 2 | Implement deployment window policy (no migrations during peak hours) | @engineering-lead | P1 | 2025-06-22 | TODO |
| 3 | Reduce connection pool timeout to 5s with retry | @payments-team | P2 | 2025-06-29 | TODO |
| 4 | Add connection pool saturation alert | @sre-team | P2 | 2025-06-29 | TODO |
| 5 | Create staging load test environment mirroring production traffic | @platform-team | P3 | 2025-07-15 | TODO |

## Lessons Learned / Leçons tirées

- Database migrations under load are a recurring incident pattern.
  Invest in migration safety tooling.
- Fast rollback capability (< 10 minutes) was critical in limiting impact.
- SLO burn-rate alerting detected the issue 3 minutes after onset —
  faster than threshold alerts would have.

## Error Budget Impact / Impact sur le budget d'erreur

- Error budget consumed by this incident: 8.2% (of 30-day budget)
- Error budget remaining: 67.3%
```

### Post-Mortem Review Meeting / Réunion de revue post-mortem

Conduct the review meeting with all involved parties:

1. **Read the document first** (10 min): Everyone reads the post-mortem silently.
2. **Timeline walkthrough** (10 min): Walk through the timeline, fill gaps.
3. **Contributing factors discussion** (15 min): Discuss systemic factors, not individual actions.
4. **Action items review** (10 min): Agree on actions, owners, and priorities.
5. **Process improvement** (5 min): Discuss what went well and what to improve in the incident response process itself.

---

## 5. Status Pages / Pages de statut

### Public Status Page / Page de statut publique

Maintain a public status page for external customers. This is a trust-building tool and reduces support ticket volume during incidents.

Maintenir une page de statut publique pour les clients externes. C'est un outil de confiance qui réduit le volume de tickets support pendant les incidents.

**Components to display**:
- Individual service/component status (API, Dashboard, Mobile, Payments, etc.)
- Current incidents with updates
- Scheduled maintenance windows
- Historical uptime (30/90 day view)
- Incident history with post-mortem links

**Tools**: Atlassian Statuspage, Instatus, Better Uptime status pages, Cachet (open-source), or build custom with a static site generator.

**Update cadence during incidents**:
- SEV1: Every 15 minutes minimum
- SEV2: Every 30 minutes
- SEV3: At detection, mitigation, and resolution

### Internal Status Dashboard / Dashboard de statut interne

Maintain an internal dashboard with more detail than the public page:
- Real-time SLO compliance for all services
- Active incidents with Slack channel links
- On-call roster (who is currently on-call for each team)
- Recent deployments
- Error budget status

---

## 6. Incident Management Tools / Outils de gestion d'incidents

### PagerDuty

The industry standard for on-call management and incident response.

**Key features**: Multi-channel alerting (push, SMS, phone call, email), escalation policies, on-call scheduling, incident workflows, postmortem integration, AIOps (noise reduction, alert grouping), event orchestration.

**Best for**: Large organizations with complex on-call structures, multi-team routing, compliance requirements.

**Pricing**: Per-user/month. Professional plan ~$29/user/month, Business plan ~$49/user/month.

### OpsGenie (Atlassian)

Strong alternative to PagerDuty with deep Atlassian ecosystem integration.

**Key features**: On-call scheduling, alert routing, escalation policies, Jira integration, Confluence runbooks, Statuspage integration, heartbeat monitoring.

**Best for**: Organizations already using Atlassian products (Jira, Confluence, Bitbucket).

**Pricing**: Essentials ~$9/user/month, Standard ~$19/user/month.

### Incident.io

Modern, Slack-native incident management platform. The fastest-growing tool in this category (2024-2026).

**Key features**: Declare and manage incidents entirely from Slack, automatic timeline generation, role assignment, status page updates from Slack, post-mortem generation, custom workflows, catalog of services and teams, on-call scheduling (added 2024).

**Best for**: Slack-first organizations, teams that want low-friction incident management, modern SaaS companies.

**Pricing**: Per-responder/month. Starter free (up to 5 responders), Pro ~$16/responder/month.

### Rootly

AI-powered incident management with strong automation.

**Key features**: Slack-native incident management, AI-powered retrospective drafts, automated Jira ticket creation, Kubernetes-aware, runbook automation, on-call scheduling.

**Best for**: Engineering-heavy organizations wanting maximum automation.

### Comparison Matrix / Matrice de comparaison

| Feature | PagerDuty | OpsGenie | Incident.io | Rootly |
|---|---|---|---|---|
| On-call scheduling | Excellent | Excellent | Good | Good |
| Alert routing | Excellent | Excellent | Good | Good |
| Slack integration | Good | Good | Excellent | Excellent |
| Post-mortem generation | Good | Good | Excellent | Excellent (AI) |
| Jira integration | Good | Excellent | Good | Good |
| Status page | Via Statuspage | Integrated | Integrated | Via integration |
| AIOps / AI features | Good | Basic | Growing | Excellent |
| Pricing (10 users) | ~$490/mo | ~$190/mo | ~$160/mo | ~$200/mo |
| Best for | Enterprise | Atlassian shops | Slack-first teams | Automation-focused |

---

## Summary Checklist / Checklist récapitulatif

- [ ] Every alert satisfies the 5 criteria: actionable, meaningful, urgent, contextualized, novel
- [ ] Alert routing is configured by severity, team, and time of day
- [ ] Quarterly alert reviews are conducted with quality metrics
- [ ] On-call rotation is weekly with primary + secondary
- [ ] On-call compensation is provided (stipend or comp time)
- [ ] On-call health metrics are tracked (pages per shift < 5)
- [ ] Incident severity levels (SEV1-4) are defined with response time expectations
- [ ] Incident roles are defined: IC, Communications Lead, Technical Lead
- [ ] Mitigation-first culture: restore service before debugging
- [ ] Post-mortems are blameless, timely, thorough, and action-oriented
- [ ] Post-mortem action items are tracked to completion
- [ ] Public status page is maintained and updated during incidents
- [ ] Incident management tool is deployed (PagerDuty, OpsGenie, or Incident.io)
- [ ] Runbooks exist for every critical alert
