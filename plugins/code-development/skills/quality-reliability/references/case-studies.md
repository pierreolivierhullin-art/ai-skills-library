# Études de cas — Quality & Reliability

## Cas 1 : Transformation de la stratégie de tests avec Playwright

### Contexte
InvoiceCloud, SaaS de facturation B2B (55 personnes, 14 développeurs), gère 200K factures/mois. L'application est développée en React/Next.js avec un backend Node.js. La suite de tests E2E utilise Cypress (150 tests) exécutée nightly sur Jenkins. L'équipe QA (2 personnes) effectue des tests manuels de régression de 3 jours avant chaque release.

### Problème
Les tests Cypress sont instables : le taux de flakiness atteint 18% (27 tests flaky sur 150). Les développeurs ignorent les résultats car "c'est probablement flaky" — un vrai bug de régression passe en production en moyenne une fois par mois. Les tests manuels de 3 jours rallongent le cycle de release et bloquent les déploiements. Le temps d'exécution de la suite Cypress est de 45 minutes (exécution séquentielle, pas de parallélisme). Le coût total de la QA (tests manuels + correction des bugs de régression) est estimé à 30% du budget engineering.

### Approche
1. **Migration Cypress → Playwright** : Réécriture progressive des 150 tests en Playwright. L'auto-waiting natif élimine 80% de la flakiness (plus de `cy.wait()` arbitraires). Les browser contexts garantissent l'isolation entre tests. Exécution multi-navigateurs (Chromium, Firefox, WebKit) et parallélisée.
2. **Test pyramid rebalancing** : La suite existante est "ice cream cone" inversée (150 E2E, 200 unitaires, 30 intégration). Migration vers une pyramide saine : extraction de la logique métier testable en unitaire (calcul de taxes, proration, échéances), ajout de 120 tests d'intégration API (Supertest), réduction des E2E à 80 scénarios critiques (happy paths uniquement).
3. **Visual regression en CI** : Intégration de Playwright screenshot comparison pour les 15 pages critiques (facture, dashboard, checkout). Quality gate : zéro diff visuelle non approuvée. Les changements visuels intentionnels sont approuvés via un workflow de review.
4. **Flaky test quarantine** : Processus automatisé : un test qui échoue 2× sur les 10 dernières exécutions est automatiquement mis en quarantaine (exécuté mais non-bloquant). Un ticket Jira est créé automatiquement. SLA : correction ou suppression sous 1 sprint.

### Résultat
- Taux de flakiness passé de 18% à 0.5% (1 test flaky résiduel sur 200)
- Temps d'exécution de la suite E2E réduit de 45 min à 8 min (parallélisme Playwright + réduction du nombre de tests E2E)
- Tests manuels de régression éliminés — les QA se concentrent sur les tests exploratoires et la validation UX
- Bugs de régression en production réduits de 1/mois à 1/trimestre
- Cycle de release passé de 8 jours (avec testing manuel) à 1 jour (CI automatisé)
- Couverture multi-navigateurs : 100% des tests exécutés sur Chromium, Firefox et WebKit

### Leçons apprises
- Playwright élimine mécaniquement la majorité de la flakiness grâce à l'auto-waiting — c'est le choix par défaut pour tout nouveau projet E2E.
- La pyramide des tests n'est pas un dogme mais un guide — trop de tests E2E est un anti-pattern coûteux. Extraire la logique en unitaire et réserver l'E2E aux happy paths.
- Le quarantine automatique des tests flaky est essentiel — un test flaky non traité érode la confiance de toute la suite.

---

## Cas 2 : Chaos engineering et Game Days pour la résilience

### Contexte
StreamPay, fintech de paiement par streaming (70 personnes), traite 500K micro-paiements/jour via une architecture microservices sur Kubernetes (GKE). Les services communiquent via gRPC et Kafka. L'infrastructure est multi-AZ mais n'a jamais été testée en conditions de panne réelle.

### Problème
Un incident majeur : la perte d'une Availability Zone GCP pendant 35 minutes provoque une cascade de défaillances. Le service de paiement tente de reconnecter à la base PostgreSQL (single-AZ), sature son pool de connexions, et bloque tous les paiements pendant 2h15. Le circuit breaker n'est pas configuré, les retries sont infinies (sans backoff), et le failover DNS prend 20 minutes. L'incident coûte 180K€ en transactions perdues et 15 points de NPS.

### Approche
1. **Steady-state hypothesis** : Définition de l'état normal du système sous forme de SLIs mesurables : latence p99 < 500ms, error rate < 0.1%, throughput > 100 tx/sec. Toute expérience de chaos est évaluée par rapport à ces SLIs.
2. **Resilience patterns** : Implémentation des patterns de résilience avant les chaos experiments — circuit breaker (Resilience4j) sur chaque appel inter-service, retry with exponential backoff + jitter, bulkhead pattern (pools de connexions séparés par service consommé), graceful degradation (mode dégradé qui accepte les paiements en queue si le service de vérification est down).
3. **Chaos experiments progressifs** : Déploiement de Litmus (CNCF) en staging puis en production. Progression : pod kill (service individuel) → network latency injection (200ms entre services) → AZ failure simulation (drain d'un node pool) → Kafka broker loss → PostgreSQL failover.
4. **Game Days trimestriels** : Organisation de Game Days de 4 heures avec toute l'équipe engineering. Scénario secret préparé par le SRE lead. L'équipe on-call doit détecter, diagnostiquer et résoudre l'incident en temps réel. Debriefing structuré avec timeline, what went well, et action items.

### Résultat
- Circuit breaker activé sur 100% des appels inter-services — cascade de défaillances éliminée
- AZ failover testé et validé : le système survit à la perte d'une AZ avec < 30 secondes de dégradation (vs 2h15 avant)
- MTTR réduit de 2h15 à 12 minutes pour les incidents d'infrastructure
- 15 vulnérabilités de résilience découvertes et corrigées grâce aux chaos experiments (connexions non-poolées, timeouts manquants, retries infinies)
- Graceful degradation : le mode dégradé a été activé 3 fois en production, traitant 95% des transactions au lieu de 0%
- Confiance de l'équipe en astreinte : 90% se sentent "prêts" pour un incident majeur (vs 30% avant)

### Leçons apprises
- Les resilience patterns (circuit breaker, retry, bulkhead) doivent être implémentés AVANT les chaos experiments — injecter des pannes dans un système sans protection est du sabotage, pas du chaos engineering.
- Les Game Days sont l'investissement le plus rentable en résilience — ils révèlent les failles que les tests automatisés ne trouvent pas (procédures manquantes, runbooks incomplets, communication défaillante).
- Le graceful degradation est la différence entre une panne totale et une dégradation acceptable — il doit être designé et testé pour chaque service critique.

---

## Cas 3 : Implémentation d'error budgets et SLO-driven development

### Contexte
HealthAPI, plateforme d'API de données de santé (45 personnes), expose des APIs REST consommées par 80 applications tierces (hôpitaux, pharmacies, assurances). L'infrastructure tourne sur AWS ECS avec PostgreSQL RDS et Redis ElastiCache. Le SLA contractuel est de 99.9% de disponibilité.

### Problème
L'entreprise est prise dans un cercle vicieux : l'équipe produit pousse pour des features, l'équipe SRE freine pour la fiabilité, et le CTO arbitre au cas par cas sans données objectives. Les développeurs déploient sans considérer l'impact sur la fiabilité, et les SRE bloquent des releases "par précaution". Résultat : le SLA de 99.9% est respecté (99.92% mesuré) mais 3 clients majeurs ont renouvelé avec une pénalité pour les incidents passés. L'équipe SRE (2 personnes) est en burnout, traitant 25 pages/semaine dont la majorité sont des faux positifs.

### Approche
1. **SLIs centrés utilisateur** : Définition de 4 SLIs basés sur l'expérience utilisateur réelle (pas sur l'infrastructure) : availability (% requêtes 2xx/3xx en < 3s), latency (p95 < 500ms), correctness (% de réponses avec données valides), freshness (données < 5 min de retard par rapport à la source).
2. **SLOs et error budgets** : SLO de 99.95% sur une fenêtre glissante de 30 jours pour chaque SLI. Error budget calculé : 0.05% × 30 jours = 21.6 minutes d'erreur autorisées/mois. Dashboard error budget visible par tous (product, engineering, management).
3. **Error budget policies** : Politique formalisée et signée par le CTO, VP Product et VP Engineering : Budget > 50% → ship features normalement ; Budget 25-50% → review supplémentaire des releases, pas de changements risqués ; Budget < 25% → feature freeze, 100% reliability focus ; Budget épuisé → postmortem obligatoire + plan de remédiation avant toute nouvelle feature.
4. **Burn rate alerting** : Remplacement des 200+ alertes statiques par 8 alertes burn rate (2 par SLI : fast burn 14.4×/1h et slow burn 3×/6h). Runbook associé à chaque alerte. Suppression de 192 alertes non-actionnables.

### Résultat
- Pages on-call réduites de 25/semaine à 4/semaine — 100% actionnables
- Disponibilité mesurée passée de 99.92% à 99.97% — l'error budget crée un cadre de priorisation clair
- Feature velocity augmentée de 20% — les releases ne sont plus bloquées "par précaution" mais par des données objectives
- Dialogue product/engineering objectivé : "il reste 65% d'error budget, on peut prendre le risque de cette migration"
- Zéro pénalité SLA sur les 12 derniers mois (vs 3 pénalités l'année précédente)
- Burnout SRE résolu : satisfaction de l'équipe SRE passée de 3/10 à 8/10

### Leçons apprises
- L'error budget est l'outil le plus puissant pour aligner product et engineering — il transforme la fiabilité d'un sujet de conflit en un sujet de données.
- Le burn rate alerting élimine la fatigue d'alerte tout en améliorant la détection — moins d'alertes, mais chaque alerte compte.
- L'error budget policy doit être formalisée et signée par le management — sans engagement exécutif, elle est ignorée sous pression business.
