# System Design — Distributed Systems & Architecture Styles

## Overview

Ce document de référence couvre les fondamentaux du design de systèmes distribués et les styles architecturaux modernes. Il fournit les bases théoriques et les patterns pratiques nécessaires pour concevoir des systèmes résilients, scalables et performants. Utiliser ce guide comme fondation pour toute décision de design système.

---

## Distributed Systems Fundamentals

### The Fallacies of Distributed Computing

Garder en permanence à l'esprit les 8 erreurs classiques des systèmes distribués (Peter Deutsch, 1994) — elles restent pleinement d'actualité :

1. **Le réseau est fiable** — Non. Concevoir pour les partitions réseau, timeouts et pertes de paquets. Implémenter des retries avec exponential backoff et jitter.
2. **La latence est nulle** — Non. Chaque appel réseau ajoute de la latence. Minimiser les round-trips, batchers les requêtes, utiliser du caching local.
3. **La bande passante est infinie** — Non. Concevoir des payloads compacts, utiliser la compression, paginer les résultats.
4. **Le réseau est sécurisé** — Non. Chiffrer les communications (mTLS), valider les inputs, appliquer le principe de Zero Trust.
5. **La topologie ne change pas** — Si. Concevoir pour la découverte dynamique de services (service discovery).
6. **Il y a un seul administrateur** — Non. Automatiser les opérations, utiliser l'Infrastructure as Code.
7. **Le coût de transport est nul** — Non. Chaque appel a un coût en sérialisation, désérialisation, overhead réseau.
8. **Le réseau est homogène** — Non. Gérer les différences de protocoles, versions, formats.

### CAP Theorem — Understanding the Trade-offs

Le théorème CAP (Brewer, 2000) établit qu'un système distribué ne peut garantir simultanément que deux des trois propriétés suivantes :

- **Consistency (C)** : chaque lecture retourne la dernière écriture ou une erreur.
- **Availability (A)** : chaque requête reçoit une réponse (pas nécessairement la plus récente).
- **Partition tolerance (P)** : le système continue de fonctionner malgré des partitions réseau.

En pratique, les partitions réseau sont inévitables dans un système distribué, donc le choix réel se fait entre **CP** et **AP** :

| Choix | Comportement | Cas d'usage |
|---|---|---|
| **CP** | Refuse les requêtes si la consistance ne peut être garantie | Systèmes financiers, inventaire, réservations |
| **AP** | Retourne des données potentiellement obsolètes | Catalogues produits, timelines sociales, analytics |

**Important** : le théorème CAP est souvent mal compris. Il s'applique par opération et par partition, pas globalement au système. Un même système peut être CP pour certaines opérations et AP pour d'autres. Le modèle PACELC (Abadi, 2012) est plus nuancé : en cas de Partition, choisir entre Availability et Consistency ; sinon (Else), choisir entre Latency et Consistency.

### Consistency Patterns

#### Strong Consistency
Toutes les lectures reflètent la dernière écriture. Implémenter via :
- **Consensus distribué** : Raft (etcd, CockroachDB), Paxos
- **Transactions distribuées** : 2PC (Two-Phase Commit) — à utiliser avec parcimonie car bloquant
- **Linearizability** : la garantie la plus forte, chaque opération semble instantanée

#### Eventual Consistency
Les réplicas convergent vers le même état à terme. Stratégies de résolution de conflits :
- **Last-Writer-Wins (LWW)** : simple mais peut perdre des données
- **CRDTs (Conflict-free Replicated Data Types)** : convergence automatique sans coordination. Utiliser pour les compteurs, ensembles, registres distribués
- **Vector Clocks** : détection de conflits avec résolution applicative

#### Causal Consistency
Préserver l'ordre causal des opérations sans exiger la consistance totale. Bon compromis entre forte consistance et consistance éventuelle. Implémenter via des timestamps logiques (Lamport clocks, vector clocks).

---

## Architecture Styles — In-Depth Comparison

### Monolith

#### Quand le choisir
- Phase MVP ou prototype, quand le domaine n'est pas encore bien compris.
- Équipe petite (< 5 développeurs) partageant le même code.
- Domaine simple sans besoin de scaling indépendant par composant.

#### Bonnes pratiques pour un monolithe sain
- Structurer le code en modules avec des frontières claires (packages, namespaces).
- Appliquer le principe de séparation des préoccupations au sein du monolithe.
- Utiliser des interfaces internes entre modules pour préparer une future extraction.
- Tester unitairement chaque module indépendamment.
- Déployer sur un PaaS (Railway, Render, Fly.io) pour simplifier les opérations.

#### Limites
- Scaling uniquement vertical (ou horizontal identique).
- Un déploiement = tout le système. Risque de blast radius élevé.
- Difficulté de scaling organisationnel au-delà d'une certaine taille d'équipe.

### Modular Monolith — The Modern Default

Le monolithe modulaire est le style architectural recommandé par défaut en 2024-2026. Il combine la simplicité opérationnelle du monolithe avec la modularité des microservices.

#### Principes fondamentaux
- **Module = Bounded Context** : chaque module correspond à un bounded context DDD avec son propre modèle de données, ses APIs internes et ses invariants métier.
- **Communication inter-modules via interfaces explicites** : pas d'accès direct aux tables d'un autre module. Utiliser des APIs internes (méthodes, interfaces) ou des événements in-process.
- **Base de données logiquement séparée** : chaque module possède son propre schéma (schema-per-module) même dans la même base physique. Interdire les JOINs cross-modules.
- **Déploiement unique** : un seul artefact déployable, simplifiant les opérations.

#### Pattern d'implémentation

```
src/
├── modules/
│   ├── orders/
│   │   ├── api/           # Interface publique du module
│   │   ├── domain/        # Entities, Value Objects, Aggregates
│   │   ├── application/   # Use cases, command/query handlers
│   │   ├── infrastructure/# Repositories, adapters
│   │   └── events/        # Domain events émis
│   ├── inventory/
│   │   ├── api/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── events/
│   └── shipping/
│       └── ...
├── shared/
│   ├── kernel/            # Types partagés (très limité)
│   └── infrastructure/    # Cross-cutting concerns
└── main.ts                # Composition root
```

#### Enforcement des frontières
Utiliser des outils d'analyse de dépendances pour vérifier les frontières :
- **ArchUnit** (Java/Kotlin) : tests d'architecture automatisés
- **Dependency Cruiser** (JavaScript/TypeScript) : vérification des imports
- **Go** : packages et modules natifs avec visibilité explicite
- **Règles de lint custom** : interdire les imports directs entre modules

#### Chemin d'extraction vers microservices
Quand un module doit être extrait en service indépendant :
1. Remplacer les appels in-process par des appels réseau (HTTP/gRPC).
2. Migrer les événements in-process vers un broker (Kafka, RabbitMQ).
3. Séparer la base de données physiquement.
4. Mettre en place le monitoring et tracing distribué.
5. Configurer le déploiement indépendant.

### Microservices

#### Prérequis organisationnels et techniques
Ne pas adopter les microservices sans ces capacités :
- **CI/CD mature** : déploiement automatisé par service.
- **Observabilité distribuée** : tracing, logging centralisé, métriques par service.
- **Infrastructure as Code** : provisioning automatisé.
- **Équipes autonomes** : chaque équipe possède un ou plusieurs services end-to-end.
- **Culture DevOps** : "you build it, you run it".

#### Sizing des services
Ne pas créer des nano-services. Un bon microservice :
- Correspond à un bounded context ou un sous-domaine.
- Peut être compris entièrement par une seule équipe (Two-Pizza Team Rule).
- Possède ses propres données et peut être déployé indépendamment.
- A une raison de scaler indépendamment des autres.

#### Communication Patterns

**Synchrone** :
- **REST over HTTP** : standard, universellement supporté, idéal pour les CRUD et les APIs publiques.
- **gRPC** : haute performance, typage fort via Protocol Buffers, idéal pour la communication interne entre services.
- **GraphQL** : flexible pour les clients, idéal comme BFF (Backend for Frontend).

**Asynchrone** :
- **Event-driven (publish/subscribe)** : découplage maximal, chaque service publie des événements sans connaître les consommateurs. Utiliser Apache Kafka, AWS EventBridge, ou NATS.
- **Message queues (point-to-point)** : garantie de livraison, ordonnancement. Utiliser RabbitMQ, AWS SQS, ou Redis Streams.
- **Event streaming** : Kafka ou Redpanda pour le traitement de flux d'événements en temps réel avec persistance et replay.

### Cell-Based Architecture

Architecture émergente (2023-2026) conçue pour la haute disponibilité et l'isolation de défaillance à grande échelle, popularisée par AWS et les géants du web.

#### Concept fondamental
Une **cellule** est une unité autonome et indépendante qui contient toutes les couches nécessaires pour servir un sous-ensemble de trafic : compute, storage, cache, messaging. Chaque cellule est identique en structure mais sert un segment différent d'utilisateurs ou de requêtes.

#### Caractéristiques clés
- **Isolation de défaillance (blast radius)** : une panne dans une cellule n'affecte que les utilisateurs de cette cellule (typiquement < 5% du trafic total).
- **Scaling horizontal par cellule** : ajouter de nouvelles cellules pour gérer plus de trafic, plutôt que de scaler chaque composant individuellement.
- **Déploiement canary par cellule** : déployer les nouvelles versions cellule par cellule pour limiter les risques.
- **Routage au niveau du cell router** : un routeur global dirige les requêtes vers la bonne cellule (par user ID, tenant ID, region).

#### Quand adopter le Cell-Based
- Systèmes servant > 100K requêtes/seconde.
- Exigences de disponibilité > 99.99%.
- Besoin d'isolation stricte entre tenants (multi-tenancy).
- Budget et équipe capables de gérer la complexité opérationnelle.

#### Pattern de cell routing

```
[Client] → [Cell Router / Global Load Balancer]
              ├── Cell A (users 0-25%)
              │   ├── API Gateway
              │   ├── Services
              │   ├── Database (replica)
              │   └── Cache
              ├── Cell B (users 25-50%)
              │   └── ... (même structure)
              ├── Cell C (users 50-75%)
              │   └── ...
              └── Cell D (users 75-100%)
                  └── ...
```

---

## Service Mesh

### Quand utiliser un service mesh
Adopter un service mesh quand le nombre de microservices dépasse 15-20 et que la gestion des préoccupations transverses (mTLS, retry, circuit breaking, observabilité) devient un fardeau pour les équipes de développement.

### Options modernes (2024-2026)
- **Istio** : le plus complet, basé sur Envoy proxy. Lourd mais très configurable. Convient aux grandes organisations.
- **Linkerd** : léger, simple, performant. Écrit en Rust (data plane). Recommandé pour les équipes cherchant la simplicité.
- **Cilium Service Mesh** : basé sur eBPF, élimine le besoin de sidecars. Très performant car opère au niveau du kernel Linux. Tendance forte en 2024-2026.
- **Ambient Mesh (Istio)** : mode sans sidecar d'Istio, utilisant des ztunnels et waypoint proxies. Réduit l'overhead mémoire et CPU.

### Fonctionnalités clés d'un service mesh
- **mTLS automatique** : chiffrement de toutes les communications inter-services sans modification du code applicatif.
- **Traffic management** : canary deployments, blue-green, traffic mirroring, header-based routing.
- **Observabilité** : métriques L7 automatiques (latence, taux d'erreur, throughput) par service et par route.
- **Resilience** : circuit breaking, retry, timeout, rate limiting configurés de manière centralisée.

---

## Scalability Patterns

### Horizontal Scaling Strategies

#### Stateless Services
Concevoir les services applicatifs comme stateless. Externaliser l'état dans des stores dédiés (bases de données, caches, object stores). Cela permet un scaling horizontal trivial via ajout d'instances.

#### Database Scaling
- **Read Replicas** : rediriger les lectures vers des réplicas pour décharger le primary. Accepter un léger délai de réplication.
- **Sharding** : partitionner les données par clé (user ID, tenant ID, region). Stratégies de sharding :
  - **Range-based** : simple mais risque de hotspots.
  - **Hash-based** : distribution uniforme mais rend les range queries difficiles.
  - **Directory-based** : flexible mais le directory est un SPOF.
- **CQRS** : séparer physiquement les bases de lecture et d'écriture. Utiliser des projections optimisées pour la lecture (vues matérialisées, ElasticSearch, bases de données colonne).

#### Caching Strategy
Appliquer le caching en couches :
1. **CDN** : contenu statique, réponses API cachéables (Cache-Control headers).
2. **Application cache** : Redis ou Memcached pour les données fréquemment accédées.
3. **Local cache** : in-memory cache (LRU) pour les données de référence peu changeantes.
4. **Database cache** : query cache, buffer pool tuning.

Patterns de caching :
- **Cache-Aside** : l'application gère le cache explicitement (read-through, write-through).
- **Write-Behind** : écrire dans le cache puis propager en asynchrone vers la base. Risque de perte si le cache tombe.
- **Refresh-Ahead** : pré-charger le cache avant expiration pour éviter les cache misses.

### Resilience Patterns

#### Circuit Breaker
Implémenter le pattern circuit breaker pour éviter les cascades de pannes. Trois états :
- **Closed** : requêtes passent normalement, compteur d'erreurs actif.
- **Open** : requêtes rejetées immédiatement (fail-fast), durée configurable.
- **Half-Open** : quelques requêtes autorisées pour tester la reprise du service.

Configurer les seuils : taux d'erreur > 50% sur les 10 dernières secondes -> ouverture. Timeout de 30 secondes avant half-open.

#### Bulkhead
Isoler les ressources par type de requête ou par dépendance pour empêcher un composant saturé de consommer toutes les ressources. Implémenter via des thread pools dédiés, des connection pools séparés, ou des containers avec limites de ressources.

#### Retry with Exponential Backoff
Réessayer les opérations idempotentes en cas d'échec transitoire. Formule : `delay = min(base * 2^attempt + random_jitter, max_delay)`. Ne jamais retry les erreurs non-transitoires (4xx). Toujours ajouter du jitter pour éviter les thundering herds.

#### Rate Limiting
Protéger les services contre la surcharge. Algorithmes :
- **Token Bucket** : flexible, permet les bursts. Recommandé pour la plupart des cas.
- **Sliding Window** : précis, bonne distribution temporelle.
- **Leaky Bucket** : lissage du trafic, pas de bursts.

---

## Event-Driven Architecture

### Core Concepts

#### Domain Events
Un domain event représente un fait qui s'est produit dans le domaine métier. Nommer les événements au passé (OrderPlaced, PaymentReceived, ShipmentDelivered). Chaque événement est immuable et contient les données nécessaires à sa compréhension sans requête supplémentaire.

#### Event Schema Design
Concevoir des événements avec un schéma clair et versionné :

```json
{
  "eventId": "uuid-v7",
  "eventType": "order.placed",
  "eventVersion": "1.2",
  "timestamp": "2025-01-15T10:30:00Z",
  "source": "order-service",
  "correlationId": "uuid-request",
  "causationId": "uuid-previous-event",
  "data": {
    "orderId": "ORD-12345",
    "customerId": "CUST-789",
    "totalAmount": 149.99,
    "currency": "EUR",
    "items": [...]
  },
  "metadata": {
    "userId": "USR-456",
    "traceId": "trace-abc"
  }
}
```

#### Event Versioning
Gérer l'évolution des schémas d'événements :
- **Backward compatible changes** : ajouter des champs optionnels (recommandé).
- **Schema Registry** : utiliser un schema registry (Confluent, AWS Glue) pour versionner et valider les schémas.
- **Upcasting** : transformer les anciens événements vers le nouveau format à la lecture.
- **Event wrapper** : encapsuler les événements dans une enveloppe avec métadonnées de version.

### Event Sourcing Deep Dive

#### Principes
- Stocker chaque changement d'état comme un événement immuable dans un event store.
- L'état courant est reconstruit en rejouant les événements (rehydratation).
- Le journal d'événements constitue la source de vérité unique (single source of truth).

#### Event Store Requirements
- **Append-only** : écriture uniquement en ajout, jamais de modification ou suppression.
- **Ordonnancement garanti** : par aggregate, pas nécessairement global.
- **Optimistic concurrency** : vérifier la version attendue lors de l'écriture pour détecter les conflits.
- **Snapshotting** : sauvegarder périodiquement l'état pour éviter de rejouer trop d'événements.

#### Quand utiliser Event Sourcing
- Domaines avec besoin d'audit trail complet (finance, santé, légal).
- Besoin de "time travel" (reconstruire l'état à un instant T).
- Domaines avec des règles métier complexes qui bénéficient de la modélisation par événements.
- Quand les patterns de lecture et d'écriture sont très différents (combiner avec CQRS).

#### Quand NE PAS utiliser Event Sourcing
- Applications CRUD simples sans besoin d'historique.
- Domaines avec beaucoup de mises à jour sur les mêmes entités (performance de rehydratation).
- Équipes sans expérience des systèmes event-driven (courbe d'apprentissage significative).

---

## Data Management in Distributed Systems

### Database-per-Service Pattern
Chaque service possède sa propre base de données. Avantages : indépendance technologique, isolation, scalabilité indépendante. Inconvénients : requêtes cross-services complexes, consistance éventuelle.

### Saga Pattern — Transactions Distribuées

#### Choreography-based Saga
Chaque service écoute les événements des autres et réagit. Avantages : découplage fort, pas de point central de coordination. Inconvénients : logique dispersée, difficulté à visualiser le flux complet, risque de cycles.

```
OrderService → [OrderCreated] → PaymentService → [PaymentConfirmed] → InventoryService → [StockReserved] → ShippingService
                                                   [PaymentFailed] → OrderService (compensation: cancel order)
```

#### Orchestration-based Saga
Un orchestrateur central coordonne les étapes. Avantages : logique centralisée, facile à comprendre et à monitorer. Inconvénients : l'orchestrateur est un point de couplage et potentiellement un SPOF.

```
OrderSaga (Orchestrator):
  1. CreateOrder → OrderService
  2. ProcessPayment → PaymentService
  3. ReserveStock → InventoryService
  4. ArrangeShipping → ShippingService
  Compensation: reverse steps in order
```

Préférer la chorégraphie pour les flux simples (3-4 étapes) et l'orchestration pour les flux complexes (> 4 étapes) ou quand la visibilité du flux est critique.

### Change Data Capture (CDC)

Capturer les modifications de la base de données en temps réel et les propager comme événements. Outils :
- **Debezium** : open source, basé sur Kafka Connect, supporte PostgreSQL, MySQL, MongoDB, SQL Server.
- **AWS DMS** : managed service pour la capture de changements sur AWS.

Utiliser CDC pour synchroniser les données entre services sans modifier le code applicatif existant. Particulièrement utile dans les stratégies de migration (Strangler Fig pattern).

---

## Modern Patterns 2024-2026

### Platform Engineering
L'émergence des Internal Developer Platforms (IDP) comme abstraction au-dessus de l'infrastructure. Fournir aux développeurs des self-service capabilities pour le provisioning, le déploiement et l'observabilité. Outils : Backstage (Spotify), Port, Humanitec, Kratix.

### AI-Augmented Architecture
Intégrer l'IA comme composant architectural de premier ordre :
- **AI Gateway** : routage, rate limiting et observabilité spécifiques aux appels LLM.
- **Semantic Caching** : cacher les réponses LLM par similarité sémantique plutôt que par correspondance exacte.
- **RAG Architecture** : Retrieval-Augmented Generation comme pattern architectural pour les applications IA, avec vector databases (Pinecone, Weaviate, pgvector) et embedding pipelines.
- **AI Sidecar** : enrichir les services existants avec des capacités IA via un sidecar pattern.

### WebAssembly (Wasm) at the Edge
Utiliser WebAssembly comme runtime pour le edge computing et les plugins :
- Exécution ultra-rapide (cold start < 1ms vs > 100ms pour les containers).
- Isolation forte (sandboxing natif).
- Portabilité (WASI — WebAssembly System Interface).
- Cas d'usage : edge functions, plugin systems, serverless lightweight.

### Composable Architecture
Construire des systèmes à partir de composants interchangeables (Packaged Business Capabilities — PBCs) :
- Chaque PBC fournit une capacité métier complète avec API, UI et données.
- Composition dynamique via un orchestration layer.
- Aligné avec les principes MACH (Microservices, API-first, Cloud-native, Headless).
