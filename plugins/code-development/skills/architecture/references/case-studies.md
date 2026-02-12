# Études de cas — Software Architecture & System Design

## Cas 1 : Migration Strangler Fig d'un monolithe e-commerce

### Contexte
ShopNova, plateforme e-commerce B2C de 85 personnes, traite 2M de commandes/an sur un monolithe Ruby on Rails de 8 ans (400K lignes de code). La base PostgreSQL unique gère tout : catalogue, commandes, paiements, utilisateurs, stock. L'application est déployée sur un seul cluster de 3 serveurs avec un load balancer.

### Problème
Le monolithe atteint ses limites : les déploiements prennent 45 minutes avec 20% de taux d'échec, chaque modification du moteur de pricing casse régulièrement le module de stock, et les pics de trafic (Black Friday, soldes) saturent toute la plateforme alors que seul le catalogue est sollicité. L'équipe de 12 développeurs se bloque mutuellement sur les merge conflicts. Le CTO doit présenter un plan de modernisation au board sous 6 semaines.

### Approche
1. **Event Storming** : 3 jours d'atelier avec les développeurs et les experts métier pour cartographier le domaine. Identification de 5 bounded contexts clairs : Catalog, Order, Payment, Inventory, Customer.
2. **Architecture Decision Records** : Rédaction de 8 ADR couvrant les décisions structurantes — choix du monolithe modulaire comme étape intermédiaire, communication asynchrone via RabbitMQ, base de données par service, pattern Strangler Fig pour la migration.
3. **Strangler Fig progressif** : Extraction du service Catalog en premier (le plus découplé), avec un API Gateway (Kong) routant le trafic entre le monolithe et le nouveau service. Migration base par base avec dual-write temporaire et reconciliation.
4. **Fitness functions** : Définition de métriques architecturales automatisées — couplage afférent < 5 par service, latence p99 < 200ms, disponibilité 99.95%, temps de déploiement < 10 min.

### Résultat
- Temps de déploiement passé de 45 min à 8 min par service (×5.6)
- Taux d'échec de déploiement réduit de 20% à 3%
- Le service Catalog scale indépendamment : 10× plus de requêtes pendant le Black Friday sans impacter les commandes
- Merge conflicts réduits de 70% grâce aux équipes alignées sur les bounded contexts
- 3 services extraits en 9 mois (Catalog, Payment, Inventory), 2 restants planifiés

### Leçons apprises
- L'Event Storming est indispensable avant toute décision de découpage — les frontières techniques ne correspondent pas toujours aux frontières métier.
- Le Strangler Fig évite le big-bang rewrite, mais le dual-write temporaire génère une complexité sous-estimée — limiter sa durée à 2-3 sprints par service.
- Les ADR documentés dès le départ évitent les débats répétitifs et accélèrent l'onboarding des nouveaux développeurs.

---

## Cas 2 : Architecture event-driven pour une fintech de paiements

### Contexte
PayStream, fintech de 40 personnes, propose une API de paiements multi-devises pour les marketplaces européennes. L'architecture initiale est un monolithe Node.js avec une base PostgreSQL, traitant 50K transactions/jour. L'entreprise vient de lever 15M€ en Série A et prévoit d'atteindre 500K transactions/jour sous 18 mois.

### Problème
L'architecture synchrone (REST point-to-point) crée des cascades de défaillances : quand le service de détection de fraude ralentit, tout le pipeline de paiement est bloqué. Les timeouts en cascade provoquent des transactions en état indéterminé, nécessitant une réconciliation manuelle quotidienne. Le temps de traitement moyen d'une transaction est passé de 800ms à 3.2s en 6 mois. La conformité PSD2 impose un audit trail complet que l'architecture actuelle ne supporte pas.

### Approche
1. **Domain-Driven Design stratégique** : Identification de 4 sous-domaines — Payment Processing (core), Fraud Detection (supporting), Compliance/Audit (supporting), Settlement (generic). Context mapping avec des Anti-Corruption Layers entre les bounded contexts.
2. **Event Sourcing pour le core domain** : Implémentation d'event sourcing sur le Payment Processing avec EventStoreDB. Chaque transaction est une séquence d'événements (PaymentInitiated, FraudCheckCompleted, PaymentAuthorized, PaymentSettled). Reconstruction temporelle pour l'audit PSD2.
3. **CQRS pour les lectures** : Séparation des modèles de lecture avec des projections matérialisées dans PostgreSQL pour les dashboards et rapports, alimentées par les événements.
4. **Communication asynchrone** : Remplacement des appels REST synchrones par Apache Kafka pour la communication inter-services. Le Fraud Detection consomme les événements PaymentInitiated et publie FraudCheckCompleted — le pipeline ne bloque plus.

### Résultat
- Latence médiane de transaction réduite de 3.2s à 450ms (p99 < 1.2s)
- Zéro transaction en état indéterminé grâce à l'event sourcing — réconciliation manuelle éliminée
- Audit PSD2 passé avec succès : reconstruction complète de l'historique de chaque transaction
- Capacité de traitement passée à 300K transactions/jour sans scaling supplémentaire
- Tolérance aux pannes : le service de fraude peut être down 10 min sans impact sur les paiements (traitement asynchrone avec timeout et fallback)

### Leçons apprises
- L'event sourcing est puissant pour les domaines nécessitant un audit trail complet, mais la complexité opérationnelle est significative — ne l'appliquer qu'au core domain.
- CQRS sans event sourcing est souvent suffisant — séparer la décision d'adopter les deux patterns.
- Kafka introduit une complexité opérationnelle majeure — investir dans le monitoring des consumer lags et la gestion des offsets dès le début.

---

## Cas 3 : Architecture cloud-native pour un SaaS multi-tenant B2B

### Contexte
DataPilot, éditeur SaaS B2B d'analytics, sert 200 clients (PME et ETI) depuis une architecture monolithique Python/Django déployée sur AWS EC2. L'équipe de 25 développeurs gère un codebase unique avec une base PostgreSQL partagée. La société vient de signer un contrat avec un grand groupe bancaire qui exige une isolation stricte des données, une résidence des données en Europe, et une disponibilité de 99.99%.

### Problème
L'architecture mono-tenant sur infrastructure partagée ne répond pas aux exigences d'isolation du client bancaire. La base partagée sans Row-Level Security expose des risques de fuite de données cross-tenant. Le SLA actuel est de 99.5% (40h de downtime autorisé/an) contre 99.99% requis (52 min/an). L'absence de cell isolation signifie qu'un bug ou une surcharge d'un client impacte tous les autres.

### Approche
1. **Cell-based architecture** : Conception d'une architecture cellulaire où chaque "cellule" est une instance autonome de l'application avec sa propre base de données, déployée dans un namespace Kubernetes dédié. Les petits clients partagent des cellules (pool tenant), le client bancaire a une cellule dédiée (single tenant).
2. **Monolithe modulaire comme étape** : Refactoring du monolithe Django en modules découplés (analytics-engine, data-ingestion, user-management, reporting) avec des interfaces bien définies, sans passer directement aux microservices.
3. **Infrastructure as Code multi-cellule** : Terraform modules réutilisables pour provisionner une cellule complète (namespace K8s, base PostgreSQL dédiée, Redis, stockage S3 isolé) en < 30 minutes. GitOps avec ArgoCD pour le déploiement.
4. **Global routing layer** : API Gateway centralisé (Kong) qui route chaque requête vers la cellule appropriée basée sur le tenant ID. Health checks par cellule avec failover automatique.

### Résultat
- Isolation complète des données : chaque cellule a sa propre base PostgreSQL — audit de sécurité bancaire passé
- Disponibilité mesurée à 99.97% sur les cellules dédiées (proche de l'objectif 99.99%)
- Blast radius réduit : un incident sur une cellule n'impacte que ses tenants — les autres cellules restent opérationnelles
- Provisionnement d'une nouvelle cellule en 25 minutes (vs 2 jours manuellement)
- Contrat bancaire signé (800K€ ARR) — le plus gros client de l'entreprise

### Leçons apprises
- L'architecture cell-based est le meilleur compromis pour le multi-tenant B2B avec des exigences d'isolation variables — mais la complexité opérationnelle est élevée.
- Le monolithe modulaire est une étape intermédiaire pragmatique qui apporte 80% des bénéfices des microservices avec 30% de la complexité.
- Le coût d'infrastructure augmente significativement avec les cellules dédiées — implémenter un modèle de pricing qui reflète ce coût pour les clients enterprise.
