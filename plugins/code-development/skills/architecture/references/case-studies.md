# Études de cas — Software Architecture & System Design

## Cas 1 : Migration Strangler Fig d'un monolithe e-commerce

### Contexte
ShopNova, plateforme e-commerce B2C de 85 personnes, traite 2M de commandes/an sur un monolithe Ruby on Rails de 8 ans (400K lignes de code). L'entreprise occupe la troisième position sur le marché français du prêt-à-porter en ligne, derrière deux acteurs historiques disposant d'architectures modernes. La base PostgreSQL unique gère tout : catalogue, commandes, paiements, utilisateurs, stock. L'application est déployée sur un seul cluster de 3 serveurs bare-metal avec un load balancer HAProxy, sans autoscaling. L'équipe technique se compose de 12 développeurs full-stack, 2 SREs et un architecte à temps partiel partagé avec un autre projet.

### Problème
Le monolithe atteint ses limites opérationnelles et business : les déploiements prennent 45 minutes avec 20% de taux d'échec, chaque modification du moteur de pricing casse régulièrement le module de stock via des dépendances implicites non documentées, et les pics de trafic (Black Friday, soldes) saturent toute la plateforme alors que seul le catalogue est sollicité. L'équipe de 12 développeurs se bloque mutuellement sur les merge conflicts — en moyenne 3 heures perdues par développeur par semaine. Le CTO doit présenter un plan de modernisation au board sous 6 semaines, avec un premier résultat tangible sous 3 mois. La concurrence a déjà migré vers des architectures événementielles, et deux clients grands comptes menacent de partir si la stabilité ne s'améliore pas avant la prochaine saison de soldes.

### Approche
1. **Event Storming** : 3 jours d'atelier intensif avec les 12 développeurs, le product manager et 4 experts métier (achat, logistique, finance, marketing) pour cartographier l'ensemble du domaine. L'exercice a révélé des dépendances cachées entre le pricing et l'inventaire que personne n'avait documentées. Identification de 5 bounded contexts clairs : Catalog, Order, Payment, Inventory, Customer. Le coût de l'atelier (15 jours-homme) a été amorti dès le premier mois par la réduction des erreurs de découpage.
2. **Architecture Decision Records** : Rédaction de 8 ADR couvrant les décisions structurantes — choix du monolithe modulaire comme étape intermédiaire (rejet de la migration directe vers des microservices jugée trop risquée), communication asynchrone via RabbitMQ (préféré à Kafka pour la simplicité opérationnelle à cette échelle), base de données par service avec PostgreSQL, pattern Strangler Fig pour la migration progressive. Chaque ADR a été revu en pair par au moins 2 développeurs seniors et validé par le CTO en comité architecture.
3. **Strangler Fig progressif** : Extraction du service Catalog en premier (le plus découplé, identifié lors de l'Event Storming), avec un API Gateway (Kong) routant le trafic entre le monolithe et le nouveau service. Migration base par base avec dual-write temporaire et reconciliation par batch nocturne. Le service Catalog a été réécrit en Go pour bénéficier de meilleures performances sur les lectures intensives. La phase de dual-write a duré 6 semaines — plus longue que prévu mais contenue grâce à un monitoring dédié des écarts de données.
4. **Fitness functions** : Définition de métriques architecturales automatisées exécutées à chaque build dans le pipeline CI/CD — couplage afférent < 5 par service (mesuré par un script d'analyse statique custom), latence p99 < 200ms (validée par des tests de charge Gatling hebdomadaires), disponibilité 99.95% mesurée par des synthetic checks Datadog, temps de déploiement < 10 min par service. Les violations de fitness functions bloquent le merge des PRs, garantissant que la dette architecturale ne se réintroduit pas progressivement.

### Résultat
- Temps de déploiement passé de 45 min à 8 min par service (x5.6), permettant des déploiements quotidiens au lieu d'hebdomadaires
- Taux d'échec de déploiement réduit de 20% à 3%, éliminant presque totalement les rollbacks d'urgence
- Le service Catalog scale indépendamment : 10x plus de requêtes pendant le Black Friday sans impacter les commandes — premier Black Friday sans incident en 4 ans
- Merge conflicts réduits de 70% grâce aux équipes alignées sur les bounded contexts, libérant environ 25 jours-développeur par mois
- 3 services extraits en 9 mois (Catalog, Payment, Inventory), 2 restants planifiés pour le semestre suivant
- ROI estimé à 450K EUR sur la première année (gain de productivité + réduction des incidents + rétention des clients grands comptes)

### Leçons apprises
- L'Event Storming est indispensable avant toute décision de découpage — les frontières techniques ne correspondent pas toujours aux frontières métier. Dans le cas de ShopNova, le pricing semblait appartenir au Catalog alors qu'il dépendait fortement de l'Inventory.
- Le Strangler Fig évite le big-bang rewrite, mais le dual-write temporaire génère une complexité sous-estimée — limiter sa durée à 2-3 sprints par service et monitorer les écarts de données quotidiennement. Au-delà, le risque d'incohérence croît exponentiellement.
- Les ADR documentés dès le départ évitent les débats répétitifs et accélèrent l'onboarding des nouveaux développeurs — chez ShopNova, le temps de compréhension des choix architecturaux pour un nouvel arrivant est passé de 2 semaines à 2 jours.
- Les fitness functions sont le garde-fou invisible qui empêche la dérive architecturale — sans elles, les bonnes intentions s'érodent sous la pression des deadlines en quelques mois.

---

## Cas 2 : Architecture event-driven pour une fintech de paiements

### Contexte
PayStream, fintech de 40 personnes spécialisée dans les paiements multi-devises, propose une API de paiements pour les marketplaces européennes opérant dans au moins 3 pays. L'architecture initiale est un monolithe Node.js (Express) avec une base PostgreSQL, traitant 50K transactions/jour. L'entreprise vient de lever 15M EUR en Série A avec pour objectif d'atteindre 500K transactions/jour sous 18 mois et d'obtenir la licence d'établissement de paiement auprès de l'ACPR. L'équipe technique se compose de 12 développeurs, 2 SREs, et un responsable conformité. Le stack technologique inclut Node.js 18, PostgreSQL 15, Redis pour le caching, et un déploiement sur AWS ECS Fargate.

### Problème
L'architecture synchrone (REST point-to-point) crée des cascades de défaillances critiques : quand le service de détection de fraude ralentit (latence > 5s lors des pics), tout le pipeline de paiement est bloqué car chaque étape attend la réponse de la précédente. Les timeouts en cascade provoquent des transactions en état indéterminé — 150 à 200 par jour — nécessitant une réconciliation manuelle quotidienne mobilisant un développeur pendant 2 heures. Le temps de traitement moyen d'une transaction est passé de 800ms à 3.2s en 6 mois, avec des pics à 12s pendant les heures d'affluence. La conformité PSD2 impose un audit trail complet que l'architecture actuelle ne supporte pas : l'ACPR exige la capacité de reconstruire l'état exact de chaque transaction à tout moment, et le délai de mise en conformité est de 6 mois sous peine de refus de licence.

### Approche
1. **Domain-Driven Design stratégique** : Identification de 4 sous-domaines en atelier collaboratif de 2 jours avec les développeurs et le responsable conformité — Payment Processing (core domain, avantage compétitif), Fraud Detection (supporting, logique complexe mais pas différenciant), Compliance/Audit (supporting, contraint par la réglementation), Settlement (generic, processus standard bancaire). Context mapping avec des Anti-Corruption Layers entre les bounded contexts pour éviter que les modèles de données de la fraude contaminent le core domain. Ce travail a pris 3 semaines et a impliqué toute l'équipe technique.
2. **Event Sourcing pour le core domain** : Implémentation d'event sourcing sur le Payment Processing avec EventStoreDB, choisi après évaluation d'Apache Kafka Streams et Axon Framework. Chaque transaction est une séquence d'événements immuables (PaymentInitiated, FraudCheckCompleted, PaymentAuthorized, PaymentSettled, PaymentFailed). Reconstruction temporelle pour l'audit PSD2 — n'importe quel auditeur peut rejouer l'historique complet d'une transaction et voir son état exact à n'importe quel instant. La migration des données historiques a nécessité un script de "event uplift" qui a converti 18 mois de transactions existantes en événements.
3. **CQRS pour les lectures** : Séparation des modèles de lecture avec des projections matérialisées dans PostgreSQL pour les dashboards et rapports temps réel, alimentées par les événements via un consumer dédié. Le modèle d'écriture (EventStoreDB) optimisé pour l'append-only, le modèle de lecture optimisé pour les requêtes analytiques avec des index couvrants. Les projections sont reconstruites from scratch en cas d'erreur, garantissant la cohérence. Le temps de reconstruction complète est de 45 minutes pour 18 mois de données.
4. **Communication asynchrone** : Remplacement des appels REST synchrones par Apache Kafka (3 brokers, réplication 3) pour la communication inter-services. Le Fraud Detection consomme les événements PaymentInitiated et publie FraudCheckCompleted — le pipeline ne bloque plus même si la fraude met 30 secondes à répondre. Un mécanisme de timeout avec fallback a été implémenté : si aucune réponse de la fraude en 60 secondes, le paiement est accepté avec un flag "pending_fraud_review" pour revue manuelle. Chaque consumer utilise un consumer group avec exactement-once semantics via les transactions Kafka.

### Résultat
- Latence médiane de transaction réduite de 3.2s à 450ms (p99 < 1.2s), supportant les pics de trafic sans dégradation
- Zéro transaction en état indéterminé grâce à l'event sourcing — la réconciliation manuelle quotidienne de 2h est entièrement éliminée
- Audit PSD2 passé avec succès : l'auditeur a pu reconstruire l'historique complet de chaque transaction sur demande, point spécifiquement salué dans le rapport
- Capacité de traitement passée à 300K transactions/jour sans scaling supplémentaire, avec une projection à 800K après optimisation des projections CQRS
- Tolérance aux pannes : le service de fraude peut être down 10 min sans impact sur les paiements (traitement asynchrone avec timeout et fallback)
- Licence d'établissement de paiement obtenue auprès de l'ACPR — l'architecture event-sourced a été un argument déterminant pour la traçabilité

### Leçons apprises
- L'event sourcing est puissant pour les domaines nécessitant un audit trail complet, mais la complexité opérationnelle est significative (schema evolution, compaction, replay) — ne l'appliquer qu'au core domain et utiliser du CRUD classique partout ailleurs.
- CQRS sans event sourcing est souvent suffisant — séparer la décision d'adopter les deux patterns. Chez PayStream, le Settlement domain utilise CQRS sans event sourcing avec succès.
- Kafka introduit une complexité opérationnelle majeure — investir dans le monitoring des consumer lags et la gestion des offsets dès le début. Un consumer lag non détecté pendant 24h a provoqué un retard de reporting qui a nécessité 8 heures de correction.
- Le fallback en cas de timeout du service de fraude doit être soigneusement calibré avec le métier — un seuil trop bas augmente le risque de fraude, trop haut dégrade l'expérience utilisateur. Impliquer le responsable risque dans cette décision.

---

## Cas 3 : Architecture cloud-native pour un SaaS multi-tenant B2B

### Contexte
DataPilot, éditeur SaaS B2B d'analytics, sert 200 clients (PME et ETI) depuis une architecture monolithique Python/Django déployée sur AWS EC2. L'équipe de 25 développeurs gère un codebase unique avec une base PostgreSQL partagée. La société, positionnée sur le marché de la business intelligence self-service en Europe francophone, vient de signer un contrat avec un grand groupe bancaire (top 5 français) qui exige une isolation stricte des données, une résidence des données en Europe (régions AWS eu-west-1 et eu-central-1 uniquement), et une disponibilité de 99.99%. Le stack technique inclut Django 4.2, PostgreSQL 15, Redis, Celery pour les tâches asynchrones, et un déploiement EC2 avec Auto Scaling Groups.

### Problème
L'architecture mono-tenant sur infrastructure partagée ne répond pas aux exigences d'isolation du client bancaire, qui a mandaté un audit de sécurité externe (cabinet Big 4) pour valider l'architecture. La base partagée sans Row-Level Security expose des risques de fuite de données cross-tenant — un test de pénétration a démontré qu'un utilisateur authentifié pouvait accéder aux données d'un autre tenant en manipulant les paramètres d'URL. Le SLA actuel est de 99.5% (40h de downtime autorisé/an) contre 99.99% requis (52 min/an), soit un écart de deux ordres de grandeur. L'absence de cell isolation signifie qu'un bug ou une surcharge d'un client impacte tous les autres — un incident récent causé par un client générant 50x le volume normal de requêtes a dégradé la plateforme pour les 199 autres clients pendant 4 heures. Le contrat bancaire représente 800K EUR d'ARR, soit 25% du chiffre d'affaires projeté de l'année suivante.

### Approche
1. **Cell-based architecture** : Conception d'une architecture cellulaire où chaque "cellule" est une instance autonome de l'application avec sa propre base de données, déployée dans un namespace Kubernetes dédié sur un cluster EKS multi-AZ. Les petits clients partagent des cellules (pool tenant, 20-30 clients par cellule), le client bancaire a une cellule dédiée (single tenant) avec des ressources garanties et une politique de scaling indépendante. La conception a nécessité 6 semaines d'architecture avec un consultant external spécialisé en multi-tenancy, incluant un proof of concept validé par l'équipe sécurité du groupe bancaire.
2. **Monolithe modulaire comme étape** : Refactoring du monolithe Django en modules découplés (analytics-engine, data-ingestion, user-management, reporting) avec des interfaces bien définies via des abstract base classes et un bus d'événements interne (Django signals remplacés par un broker Redis Streams). Cette étape intermédiaire a pris 3 mois et a permis de valider les frontières de modules sans la complexité opérationnelle des microservices. L'équipe a maintenu le delivery de features pendant la migration grâce à un "strangler" progressif module par module.
3. **Infrastructure as Code multi-cellule** : Terraform modules réutilisables pour provisionner une cellule complète (namespace K8s, base PostgreSQL dédiée via RDS, Redis ElastiCache, stockage S3 isolé avec des bucket policies) en < 30 minutes. GitOps avec ArgoCD pour le déploiement — chaque cellule est décrite dans un ApplicationSet ArgoCD qui génère automatiquement les manifestes K8s à partir d'un template. Les secrets sont gérés via AWS Secrets Manager avec rotation automatique toutes les 72h. Un module Terraform de "cell factory" permet à un SRE de créer une nouvelle cellule en remplissant un fichier YAML de configuration.
4. **Global routing layer** : API Gateway centralisé (Kong) qui route chaque requête vers la cellule appropriée basée sur le tenant ID extrait du JWT. Health checks par cellule avec failover automatique — si une cellule dédiée est en panne, les requêtes sont redirigées vers une cellule de failover en lecture seule (mode dégradé). Le routage utilise un cache Redis avec un TTL de 5 minutes pour la résolution tenant → cellule, évitant un lookup en base à chaque requête. Le temps de routage ajouté est de < 5ms au p99.

### Résultat
- Isolation complète des données : chaque cellule a sa propre base PostgreSQL — l'audit de sécurité du cabinet Big 4 mandaté par la banque a été passé sans réserve majeure
- Disponibilité mesurée à 99.97% sur les cellules dédiées (proche de l'objectif 99.99%), avec un plan d'amélioration identifié pour les 0.02% restants (failover DNS plus rapide)
- Blast radius réduit : un incident sur une cellule n'impacte que ses tenants — les autres cellules restent opérationnelles, validé par des chaos experiments trimestriels
- Provisionnement d'une nouvelle cellule en 25 minutes (vs 2 jours manuellement), permettant un onboarding client enterprise en moins d'une journée
- Contrat bancaire signé (800K EUR ARR) — le plus gros client de l'entreprise, ayant déclenché 3 autres opportunités enterprise grâce à l'architecture certifiée
- Coût d'infrastructure augmenté de 35% mais couvert par la marge des clients enterprise dont le pricing reflète l'isolation dédiée

### Leçons apprises
- L'architecture cell-based est le meilleur compromis pour le multi-tenant B2B avec des exigences d'isolation variables — mais la complexité opérationnelle est élevée. Prévoir au minimum 2 SREs dédiés à la gestion des cellules et un tooling d'observabilité multi-cellule dès le départ.
- Le monolithe modulaire est une étape intermédiaire pragmatique qui apporte 80% des bénéfices des microservices avec 30% de la complexité. DataPilot n'a pas eu besoin de passer aux microservices pour satisfaire les exigences du client bancaire.
- Le coût d'infrastructure augmente significativement avec les cellules dédiées — implémenter un modèle de pricing qui reflète ce coût pour les clients enterprise. Chez DataPilot, le tier "Dedicated" est facturé 3x le prix du tier "Shared" pour couvrir le surcoût d'infrastructure et de maintenance.
- Le routage global est un SPOF (Single Point of Failure) qu'il faut traiter avec le plus grand soin — chez DataPilot, Kong est déployé en multi-AZ avec un fallback sur un routage DNS-based en cas de panne complète du gateway.
