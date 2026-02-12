# SRE Practices / Pratiques SRE

Reference approfondie sur les principes SRE (Google SRE Book), la gestion du risque, les SLOs, l'elimination du toil, le capacity planning, la reprise apres sinistre et les error budgets.

Deep-dive reference on SRE principles (Google SRE Book), risk management, SLOs, toil elimination, capacity planning, disaster recovery, and error budgets.

---

## Table of Contents

1. [SRE Principles (Google SRE Book)](#sre-principles-google-sre-book)
2. [Embracing Risk](#embracing-risk)
3. [Service Level Objectives (SLOs)](#service-level-objectives-slos)
4. [Toil Measurement & Automation](#toil-measurement--automation)
5. [Capacity Planning](#capacity-planning)
6. [Disaster Recovery Testing](#disaster-recovery-testing)
7. [Error Budgets in Practice](#error-budgets-in-practice)
8. [SRE vs DevOps](#sre-vs-devops)
9. [Platform Reliability Engineering](#platform-reliability-engineering)

---

## SRE Principles (Google SRE Book)

### Fondation / Foundation

Le Site Reliability Engineering, formalise par Google, est une discipline qui applique les principes d'ingenierie logicielle a l'exploitation des systemes. Les SRE traitent l'exploitation comme un probleme logiciel : automatiser tout ce qui peut l'etre, mesurer tout ce qui compte, et utiliser les donnees pour prendre des decisions.

Site Reliability Engineering, formalized by Google, is a discipline that applies software engineering principles to systems operations. SREs treat operations as a software problem: automate everything automatable, measure everything that matters, and use data to drive decisions.

### Les 7 principes fondamentaux / The 7 Core Principles

1. **Embracing Risk** — Accepter un niveau de risque calcule plutot que de viser la perfection. La fiabilite a 100% n'est ni realiste ni souhaitable. / Accept a calculated level of risk rather than aiming for perfection. 100% reliability is neither realistic nor desirable.

2. **Service Level Objectives** — Definir des cibles de fiabilite mesurables (SLOs) basees sur l'experience utilisateur. Les SLOs guident toutes les decisions d'ingenierie de fiabilite. / Define measurable reliability targets (SLOs) based on user experience. SLOs guide all reliability engineering decisions.

3. **Eliminating Toil** — Reduire le travail manuel repetitif (toil) qui n'apporte pas de valeur durable. Viser un ratio maximum de 50% de toil dans le travail SRE. / Reduce repetitive manual work (toil) that provides no lasting value. Target a maximum ratio of 50% toil in SRE work.

4. **Monitoring** — Observer les systemes avec les quatre signaux dores (latence, trafic, erreurs, saturation). Alerter sur les symptomes, pas sur les causes. / Observe systems with the four golden signals (latency, traffic, errors, saturation). Alert on symptoms, not causes.

5. **Automation** — Automatiser les taches operationnelles pour reduire les erreurs humaines, augmenter la vitesse et garantir la reproductibilite. / Automate operational tasks to reduce human errors, increase speed, and ensure reproducibility.

6. **Release Engineering** — Integrer la fiabilite dans le processus de release : deploys progressifs, canary analysis, rollback automatise. / Integrate reliability into the release process: progressive deploys, canary analysis, automated rollback.

7. **Simplicity** — La simplicite est un prerequis de la fiabilite. Chaque composant supplementaire est une source potentielle de defaillance. / Simplicity is a prerequisite for reliability. Every additional component is a potential source of failure.

---

## Embracing Risk

### Le paradoxe de la fiabilite / The Reliability Paradox

Augmenter la fiabilite au-dela d'un certain seuil coute exponentiellement plus cher et ralentit l'innovation. La difference entre 99.9% et 99.99% de disponibilite represente 52 minutes de downtime annuel transformees en 5 minutes — un investissement massif pour un gain perceptible uniquement par les utilisateurs les plus exigeants.

Increasing reliability beyond a certain threshold costs exponentially more and slows innovation. The difference between 99.9% and 99.99% availability represents 52 minutes of annual downtime reduced to 5 minutes — a massive investment for a gain perceptible only to the most demanding users.

### Tableau de disponibilite / Availability Table

| Disponibilite | Downtime/an | Downtime/mois | Downtime/semaine | Cas d'usage typique |
|---|---|---|---|---|
| 99% (deux 9) | 3.65 jours | 7.3 heures | 1.68 heures | Outils internes, batch processing |
| 99.9% (trois 9) | 8.76 heures | 43.8 minutes | 10.1 minutes | SaaS standard, API B2B |
| 99.95% | 4.38 heures | 21.9 minutes | 5 minutes | E-commerce, services financiers |
| 99.99% (quatre 9) | 52.6 minutes | 4.38 minutes | 1 minute | Paiement, infrastructure critique |
| 99.999% (cinq 9) | 5.26 minutes | 26.3 secondes | 6 secondes | Telephonie, systemes vitaux |

### Decision de niveau de fiabilite / Reliability Level Decision

Choisir le niveau de fiabilite en fonction du coût d'un incident versus le coût de la prevention :

```
Cout du downtime (par heure) > Cout d'amelioration (annualise) ?
  -> OUI : investir dans la fiabilite superieure
  -> NON : conserver le niveau actuel, investir dans les features
```

Facteurs de decision :
- Impact revenue (transactions perdues, SLA penalties)
- Impact reputation (couverture medias, churn utilisateurs)
- Impact cascade (services dependants affectes)
- Exigences reglementaires (finance, sante, transport)

---

## Service Level Objectives (SLOs)

### Hierarchie SLI / SLO / SLA

| Concept | Definition | Responsable |
|---|---|---|
| **SLI** (Service Level Indicator) | Mesure quantitative de la fiabilite d'un aspect du service | Engineering |
| **SLO** (Service Level Objective) | Cible interne de fiabilite basee sur les SLIs | Engineering + Product |
| **SLA** (Service Level Agreement) | Engagement contractuel envers les clients, avec penalites | Business + Legal |

**Regle fondamentale / Fundamental rule:** Le SLO doit etre strictement plus exigeant que le SLA. Le SLA est la ligne rouge contractuelle ; le SLO est le seuil interne qui declenche l'action avant d'atteindre le SLA.

### Definir des SLIs pertinents / Defining Relevant SLIs

Choisir les SLIs en fonction du type de service :

**Services de type requete (APIs, web apps) :**
- **Disponibilite** : proportion de requetes reussies (status < 500) / total requetes.
- **Latence** : proportion de requetes completees en moins de X ms (p50, p95, p99).
- **Qualite** : proportion de requetes renvoyant des donnees completes et correctes.

**Services de type pipeline (batch, ETL, data processing) :**
- **Fraicheur** : age des donnees les plus recentes dans le systeme cible.
- **Completude** : proportion de records traites avec succes.
- **Exactitude** : proportion de resultats corrects valides par des checks automatises.

**Services de type stockage :**
- **Durabilite** : proportion de donnees recoverables sans perte.
- **Disponibilite en lecture/ecriture** : proportion d'operations reussies.
- **Latence d'acces** : temps de reponse pour les operations de lecture et ecriture.

### Implementation concrete / Concrete Implementation

```yaml
# slo-definitions.yaml
service: checkout-api
slos:
  - name: availability
    description: "Proportion of successful checkout requests"
    sli:
      type: request-based
      good_events: "http_status < 500"
      total_events: "all http requests to /api/checkout"
    target: 99.95
    window: 30d
    burn_rate_alerts:
      - severity: critical
        long_window: 1h
        short_window: 5m
        burn_rate: 14.4    # exhaust budget in ~5 days
      - severity: warning
        long_window: 6h
        short_window: 30m
        burn_rate: 6        # exhaust budget in ~5 days

  - name: latency
    description: "Proportion of checkout requests under 500ms"
    sli:
      type: request-based
      good_events: "response_time < 500ms"
      total_events: "all successful http requests to /api/checkout"
    target: 99.0
    window: 30d

  - name: correctness
    description: "Proportion of checkout results matching expected state"
    sli:
      type: request-based
      good_events: "order_state == expected after checkout"
      total_events: "all completed checkouts"
    target: 99.99
    window: 30d
```

### SLO Tooling

- **Sloth** : generateur de recording rules Prometheus et alertes burn-rate a partir de definitions YAML.
- **OpenSLO** : specification ouverte pour definir les SLOs de maniere portable.
- **Nobl9** : plateforme SaaS pour la gestion des SLOs multi-source.
- **Google Cloud Service Monitoring** : SLOs natifs dans GCP.
- **Datadog SLOs** : integration native avec l'ecosysteme Datadog.

---

## Toil Measurement & Automation

### Definition du toil

Le toil est un travail qui possede ces caracteristiques :
- **Manuel** : une personne doit executer l'action.
- **Repetitif** : effectue encore et encore, pas une action unique.
- **Automatisable** : un script ou un systeme pourrait le faire.
- **Tactique** : reactif et interruptif, pas strategique.
- **Sans valeur durable** : ne fait pas progresser le service de facon permanente.
- **Croissant** : la quantite augmente lineairement avec la taille du service.

Toil is work that has these characteristics: manual, repetitive, automatable, tactical, without lasting value, and scaling linearly with service growth.

### Mesure du toil / Toil Measurement

Mesurer le toil systematiquement pour justifier les investissements d'automatisation :

```
Toil ratio = Temps passe en toil / Temps total de travail SRE

Objectif Google SRE: toil ratio < 50%
Objectif excellence: toil ratio < 30%
```

**Methode de mesure / Measurement method:**
1. Categoriser chaque tache SRE : ingenierie (projets, automation) vs operations (toil).
2. Tracker le temps passe sur chaque categorie pendant 2-4 semaines.
3. Identifier les 5 taches de toil les plus chronophages.
4. Calculer le ROI d'automatisation pour chaque tache : `temps economise par an / temps d'automatisation`.
5. Automatiser en priorite les taches avec le ROI le plus eleve.

### Exemples de toil et automatisation / Toil Examples and Automation

| Toil | Automatisation |
|---|---|
| Rotation manuelle des certificats | cert-manager + Let's Encrypt |
| Nettoyage de logs/disques | CronJob + retention policies |
| Scaling manuel des replicas | HPA / KEDA avec metriques custom |
| Restarting de pods/services crashant | Kubernetes liveness probes + PDB |
| Provisioning d'environnements | Terraform modules + self-service portal |
| Onboarding de nouveaux services | Templates Backstage + golden paths |
| Rapport hebdomadaire de metriques | Dashboard automatise + envoi Slack planifie |
| Rotation d'astreinte manuelle | PagerDuty / OpsGenie rotations automatiques |

### Hierarchy of Automation (Google SRE)

```
Niveau 0 : Aucune automatisation — action manuelle a chaque occurrence
Niveau 1 : Documentation — runbook decrivant les etapes manuelles
Niveau 2 : Script — script executant l'action mais lance manuellement
Niveau 3 : Semi-automatique — script lance automatiquement, humain valide
Niveau 4 : Automatique avec override — action automatique, humain peut intervenir
Niveau 5 : Autonome — action entierement automatique, pas d'intervention humaine
```

Viser le niveau 4-5 pour les operations critiques repetitives. Accepter le niveau 2-3 pour les operations rares ou a haut risque.

---

## Capacity Planning

### Processus de capacity planning / Capacity Planning Process

1. **Demand forecasting** : projeter la demande future en combinant :
   - Croissance organique (tendances historiques, saisonnalite).
   - Croissance inorganique (lancements produit, campagnes marketing, acquisitions).
   - Evenements planifies (Black Friday, fin de trimestre, evenements sportifs).

2. **Resource modeling** : traduire la demande en besoins de ressources :
   - CPU, memoire, stockage, bande passante par unite de charge.
   - Dependencies de scaling (si le service A double, le service B et la DB doivent tripler).
   - Bottleneck analysis : identifier le composant qui sature en premier.

3. **Provisioning strategy** : choisir la strategie d'approvisionnement :
   - **Reserved capacity** : instances reservees pour la baseline (economie de 30-60%).
   - **Auto-scaling** : scaling automatique pour les variations (HPA, KEDA, cloud auto-scaling).
   - **Burst capacity** : capacite on-demand pour les pics imprevisibles.

4. **Validation** : valider le plan via des load tests simulant la charge projetee + 50% de marge.

5. **Review cadence** : reviser le capacity plan trimestriellement et apres chaque incident de capacite.

### Auto-Scaling Best Practices

```yaml
# Kubernetes HPA - Configuration recommandee
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: checkout-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: checkout-api
  minReplicas: 3
  maxReplicas: 50
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 100          # doubler les pods max
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300  # attendre 5 min avant scale-down
      policies:
        - type: Percent
          value: 25            # reduire de 25% max par palier
          periodSeconds: 60
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60   # scale a 60% CPU, pas 80%
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "100"
```

---

## Disaster Recovery Testing

### Classification des sinistres / Disaster Classification

| Niveau | Description | Exemples | RTO cible | RPO cible |
|---|---|---|---|---|
| **Tier 1** | Panne totale du service primaire | Region cloud down, corruption DB | < 1h | < 5 min |
| **Tier 2** | Panne partielle majeure | AZ down, service critique indisponible | < 30 min | < 1 min |
| **Tier 3** | Degradation significative | Pod crashloop, cache invalide, latence elevee | < 15 min | 0 (pas de perte) |
| **Tier 4** | Incident mineur | Feature degradee, erreurs intermittentes | < 1h | 0 |

**RTO** = Recovery Time Objective (temps maximal acceptable pour restaurer le service).
**RPO** = Recovery Point Objective (perte de donnees maximale acceptable).

### Strategies de DR / DR Strategies

| Strategie | RTO | Cout | Complexite | Cas d'usage |
|---|---|---|---|---|
| **Backup & Restore** | Heures | Faible | Faible | Donnees non-critiques |
| **Pilot Light** | 30-60 min | Moyen | Moyenne | Services importants |
| **Warm Standby** | 5-15 min | Eleve | Elevee | Services critiques |
| **Multi-Active (Active-Active)** | < 1 min | Tres eleve | Tres elevee | Services mission-critical |

### Testing de DR / DR Testing

Tester le plan de reprise regulierement — un plan non teste est un plan qui ne fonctionne pas :

1. **Tabletop exercise** (trimestriel) : simulation verbale d'un scenario de sinistre avec l'equipe. Reviser le plan et les runbooks.
2. **Walkthrough test** (trimestriel) : parcourir les etapes de recovery pas a pas sans execution reelle.
3. **Functional test** (semestriel) : executer le failover vers l'environnement de DR avec du trafic synthetique.
4. **Full-scale DR test** (annuel) : executer le failover complet avec un sous-ensemble du trafic production reel.
5. **Chaos engineering** (continu) : injecter des pannes en production pour valider la resilience.

---

## Error Budgets in Practice

### Calcul du budget d'erreur / Error Budget Calculation

```
Error budget = 1 - SLO target

Exemple pour un SLO de 99.95% sur 30 jours :
  Error budget = 0.05% = 0.0005
  Budget en minutes = 30 * 24 * 60 * 0.0005 = 21.6 minutes de downtime
  Budget en requetes = 0.05% des requetes totales peuvent echouer
```

### Error Budget Policies

Definir des politiques claires basees sur la consommation du budget d'erreur :

| Consommation du budget | Action | FR |
|---|---|---|
| < 50% consomme | Normal — deploy features a volonte | Deployer les features normalement |
| 50-75% consomme | Prudence — renforcer les tests, canary deploys | Renforcer les tests avant deploy |
| 75-90% consomme | Alerte — deployer uniquement avec rollback automatique | Uniquement deploys avec rollback auto |
| 90-100% consomme | Gel — uniquement bug fixes et fiabilite | Gel des features, focus fiabilite |
| Budget epuise | Freeze total — aucun deploy non-fiabilite | Aucun deploy sauf corrections de fiabilite |

### Processus de revue / Review Process

Conduire une revue hebdomadaire du budget d'erreur avec :
- Etat actuel de chaque SLO et budget restant.
- Incidents ayant consomme du budget (avec root cause).
- Projection : a ce rythme de consommation, quand le budget sera-t-il epuise ?
- Decisions : ajuster la politique de deploy en consequence.
- Action items : projets de fiabilite a prioriser.

---

## SRE vs DevOps

### Comparaison / Comparison

| Aspect | SRE | DevOps |
|---|---|---|
| **Origine** | Google (2003) | Communaute (2008) |
| **Nature** | Discipline prescriptive avec pratiques concretes | Mouvement culturel avec principes directeurs |
| **Focus** | Fiabilite et performance des systemes en production | Flux de livraison logicielle de bout en bout |
| **Metriques** | SLOs, error budgets, toil ratio | DORA metrics (DF, LT, CFR, MTTR) |
| **Equipe** | Equipe SRE dediee (ou embedded) | Culture partagee, pas d'equipe distincte necessaire |
| **Automatisation** | Automatiser les operations pour reduire le toil | Automatiser le pipeline de livraison |
| **Relation** | "Class SRE implements interface DevOps" | Framework culturel que SRE implemente |

### Quand adopter quel modele / When to Adopt Which Model

- **Startup (< 50 devs)** : adopter les principes DevOps avec des pratiques SRE legeres (SLOs, on-call rotation, post-mortems). Pas d'equipe SRE dediee necessaire.
- **Scale-up (50-200 devs)** : creer une equipe SRE embryonnaire (2-3 personnes) ou un modele "embedded SRE" avec des SREs integres dans les equipes produit.
- **Enterprise (200+ devs)** : equipe SRE centrale + SREs embarques dans les equipes critiques. Platform engineering team pour les outils et l'automatisation.

---

## Platform Reliability Engineering

### Evolution du SRE (2024-2026) / SRE Evolution (2024-2026)

Le Platform Reliability Engineering represente l'evolution du SRE traditionnel vers une approche plateforme. Les SRE ne gerent plus des services individuels mais construisent des plateformes qui rendent la fiabilite accessible a toutes les equipes de developpement.

Platform Reliability Engineering represents the evolution of traditional SRE toward a platform approach. SREs no longer manage individual services but build platforms that make reliability accessible to all development teams.

### Principes du Platform Reliability / Platform Reliability Principles

1. **Golden paths** : fournir des chemins standardises (templates, starters) qui integrent la fiabilite par defaut (health checks, metrics, tracing, alerting).
2. **Self-service reliability** : permettre aux equipes de definir leurs SLOs, configurer leurs alertes, et executer leurs chaos experiments via des interfaces self-service.
3. **Reliability as code** : definir les SLOs, les alertes, les dashboards et les runbooks en code, versionne et revise comme le code applicatif.
4. **Guardrails, not gates** : fournir des garde-fous automatises (quality gates, deployment policies) plutot que des approbations manuelles.
5. **Paved roads** : rendre le chemin facile le chemin fiable. Si la solution fiable est plus simple a utiliser que le contournement, les equipes l'adopteront naturellement.

### Implementation

```
Plateforme de fiabilite / Reliability Platform:
├── Service templates (Backstage) — incluent health checks, OTel, SLO config
├── SLO-as-Code (Sloth/OpenSLO) — definitions YAML, CI pour validation
├── Alert-as-Code — Terraform/Pulumi pour les alertes
├── Chaos platform (Litmus/Gremlin) — self-service chaos experiments
├── Incident platform (Incident.io/Rootly) — workflow automatise
├── Dashboard templates — Grafana dashboards standardises par type de service
└── On-call tooling (PagerDuty) — rotation automatique, escalation
```

---

## Summary Checklist / Checklist de synthese

- [ ] Les SLOs sont definis pour chaque service critique, bases sur l'experience utilisateur reelle
- [ ] Les error budgets sont calcules, suivis et revises chaque semaine
- [ ] Les politiques d'error budget definissent les actions en fonction de la consommation
- [ ] Le toil ratio est mesure et maintenu sous 50% (cible : < 30%)
- [ ] Les 5 principales sources de toil sont identifiees avec un plan d'automatisation
- [ ] Le capacity planning est realise trimestriellement avec une marge de 30-50%
- [ ] L'auto-scaling est configure et valide par des tests de charge
- [ ] Les plans de DR sont testes semestriellement (failover fonctionnel) et annuellement (full-scale)
- [ ] Les post-mortems sont conduits sans blame et les actions sont suivies jusqu'a completion
- [ ] La plateforme de fiabilite offre des golden paths et un self-service aux equipes de dev
