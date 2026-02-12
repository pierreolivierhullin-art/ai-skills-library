# Études de cas — Monitoring & Observability

## Cas 1 : Déploiement d'OpenTelemetry pour une architecture microservices

### Contexte
LogiSoft, éditeur SaaS de logistique (80 personnes, 20 développeurs), opère 18 microservices sur Kubernetes. Chaque service utilise un outil de monitoring différent selon l'époque de sa création : 5 services avec Datadog APM, 4 avec New Relic, 6 avec du logging brut vers CloudWatch, et 3 sans aucune instrumentation. L'équipe SRE (3 personnes) navigue entre 4 dashboards différents pour diagnostiquer un incident.

### Problème
Un incident majeur (perte de commandes pendant 45 minutes) prend 4 heures à diagnostiquer car l'équipe ne peut pas tracer une requête de bout en bout. Le service de routing des commandes appelle le service d'inventaire qui appelle le service de pricing — mais les traces s'arrêtent à chaque frontière de service car les outils ne propagent pas le même context. Le MTTD (Mean Time to Detect) est de 25 minutes et le MTTR de 3.5 heures. Les coûts de monitoring atteignent 8K€/mois avec 3 vendors différents.

### Approche
1. **OpenTelemetry comme couche unique** : Migration vers le SDK OpenTelemetry pour tous les services. Auto-instrumentation pour HTTP, gRPC, PostgreSQL et Redis. Injection de custom spans sur la logique métier critique (traitement de commande, calcul de route, vérification de stock).
2. **OTel Collector en gateway mode** : Déploiement d'un OTel Collector en mode gateway qui reçoit toutes les traces, métriques et logs. Le Collector enrichit les données (ajout de metadata K8s), filtre le bruit, et exporte vers un backend unique (Grafana Cloud : Tempo pour les traces, Mimir pour les métriques, Loki pour les logs).
3. **Tail-based sampling** : Configuration du sampling dans le Collector : 100% des traces avec erreurs sont conservées, 100% des traces lentes (> 2s) sont conservées, 5% des traces normales sont échantillonnées. Réduction de 80% du volume de données tout en conservant 100% du signal.
4. **Correlation IDs systématiques** : Injection d'un `trace_id` et d'un `request_id` dans chaque log line via le contexte OpenTelemetry. Un clic dans Grafana sur un log affiche la trace complète, et vice versa.

### Résultat
- MTTD réduit de 25 min à 3 min (alertes sur les traces d'erreur)
- MTTR réduit de 3.5h à 35 min (trace end-to-end visible en un clic)
- Coûts monitoring réduits de 8K€ à 3.2K€/mois (un seul vendor, sampling intelligent)
- 100% des services instrumentés avec propagation de contexte — zéro trou dans les traces
- Onboarding monitoring d'un nouveau service : 15 minutes (auto-instrumentation OTel)

### Leçons apprises
- OpenTelemetry élimine le vendor lock-in et unifie l'instrumentation — c'est le standard incontournable pour toute nouvelle architecture.
- Le tail-based sampling est crucial pour le rapport coût/signal — sans lui, le volume de données explose et les coûts deviennent prohibitifs.
- La corrélation traces-logs-métriques dans un seul outil transforme le diagnostic d'incident — passer de 3 dashboards à 1 divise le MTTR.

---

## Cas 2 : Implémentation d'une stratégie SLO-driven

### Contexte
BookAPI, plateforme de réservation en ligne (60 personnes), expose une API REST servant 15K requêtes/minute. L'équipe utilise Datadog avec 200+ alertes configurées. Les développeurs sont en astreinte (on-call) par rotation d'une semaine.

### Problème
L'alert fatigue est critique : les on-call reçoivent 30-50 pages par semaine, dont 85% sont des faux positifs ou des alertes non-actionnables. Un développeur senior a démissionné en citant le stress de l'astreinte. Les alertes sont basées sur des seuils statiques (CPU > 80%, memory > 90%, error rate > 1%) qui ne reflètent pas l'impact réel sur les utilisateurs. Paradoxalement, un vrai incident (latence dégradée sur le parcours de réservation) n'a été détecté que par un tweet client — aucune alerte ne l'avait capté.

### Approche
1. **Identification des SLIs critiques** : Atelier avec product et engineering pour identifier les 5 parcours utilisateur critiques (recherche, réservation, paiement, annulation, consultation). Pour chaque parcours : SLI d'availability (% de requêtes réussies en < 3s) et SLI de latency (p95 < 800ms).
2. **Définition des SLOs** : SLOs définis sur des fenêtres glissantes de 30 jours : availability 99.9% (43 min d'erreur tolérées/mois), latency p95 99.5% (< 800ms pour 99.5% des requêtes). Error budgets calculés automatiquement.
3. **Burn rate alerting** : Remplacement de toutes les alertes statiques par des alertes sur le burn rate de l'error budget. Fast burn alert : budget consommé 14.4× plus vite que prévu sur 1h (page immédiate). Slow burn alert : budget consommé 3× plus vite sur 6h (notification Slack).
4. **Error budget policies** : Trois zones définies avec des actions claires — Budget > 50% restant : ship features, optimize → Budget 25-50% : cautious, review changes carefully → Budget < 25% : freeze features, focus 100% on reliability.

### Résultat
- Pages on-call réduites de 35/semaine à 3/semaine (÷12) — 100% actionnables
- MTTD pour les vrais incidents réduit de "aléatoire" à 5 minutes (burn rate détecte les dégradations subtiles)
- Satisfaction on-call (survey interne) passée de 2/10 à 7.5/10
- Disponibilité réelle améliorée de 99.7% à 99.95% — les incidents sont détectés et résolus plus vite
- Dialogue product/engineering objectivé : "il nous reste 40% d'error budget ce mois, on peut shipper cette feature risquée"

### Leçons apprises
- Les SLOs transforment le dialogue entre product et engineering — l'error budget rend la fiabilité tangible et négociable.
- Le burn rate alerting élimine les faux positifs car il mesure l'impact cumulé, pas les pics instantanés — un CPU à 90% pendant 10 secondes ne page plus.
- Les error budget policies doivent être formalisées et acceptées par toute l'organisation — sans engagement du management, elles sont ignorées sous pression business.

---

## Cas 3 : Culture postmortem et amélioration continue

### Contexte
StreamFlow, plateforme de streaming vidéo B2B (45 personnes), subit 2-3 incidents majeurs par mois (perte de service > 15 min). L'équipe traite les incidents en mode pompier — le problème est résolu, un email est envoyé, et on passe à autre chose. Les mêmes types d'incidents se reproduisent cycliquement.

### Problème
Analyse sur 6 mois : 40% des incidents sont des récurrences de problèmes déjà rencontrés. La base de données de cache Redis sature tous les 3-4 semaines (même cause, jamais corrigée durablement). Les migrations de base de données cassent la production une fois par mois (process non standardisé). Il n'existe aucun postmortem documenté, aucune action corrective suivie, et les développeurs en astreinte appliquent les mêmes workarounds manuels à chaque fois.

### Approche
1. **Processus d'incident structuré** : Définition de niveaux de sévérité (SEV1: perte totale, SEV2: dégradation majeure, SEV3: dégradation mineure). Pour chaque SEV1/SEV2 : un incident commander est désigné, un canal Slack dédié est créé, et une timeline d'incident est documentée en temps réel.
2. **Postmortems blameless systématiques** : Postmortem obligatoire pour tout SEV1/SEV2 dans les 48h. Template structuré : timeline, impact, root cause (5 Whys), what went well, what can be improved, action items avec owner et deadline. Revue en réunion d'équipe — focus sur les systèmes, jamais sur les individus.
3. **Action items trackés** : Chaque action item du postmortem est créé comme ticket Jira avec une deadline. Un dashboard "postmortem actions" est revu en weekly engineering meeting. Les actions non complétées après 2 sprints sont escaladées.
4. **Runbooks opérationnels** : Création d'un runbook pour chaque type d'incident récurrent. Le runbook décrit : symptômes, diagnostic, procédure de résolution, et actions préventives. Chaque alerte PagerDuty contient un lien vers le runbook correspondant.

### Résultat
- Incidents récurrents réduits de 40% à 8% des incidents totaux
- MTTR médian réduit de 45 min à 18 min grâce aux runbooks (diagnostic plus rapide)
- 25 postmortems documentés en 6 mois — base de connaissances consultable
- 92% des action items complétés dans les délais (vs 0% avant — pas de tracking)
- Redis : scaling automatique implémenté (action postmortem) — plus de saturation depuis 5 mois
- Migrations : pipeline zero-downtime standardisé (action postmortem) — zéro incident de migration depuis 4 mois

### Leçons apprises
- Le postmortem blameless est le mécanisme d'apprentissage le plus puissant d'une organisation d'ingénierie — sans lui, les erreurs se répètent indéfiniment.
- Tracker les action items est aussi important que les identifier — un postmortem sans suivi est un exercice de documentation inutile.
- Les runbooks transforment le temps de résolution pour les problèmes connus — l'investissement de 2 heures de rédaction économise des heures de diagnostic sur chaque occurrence.
