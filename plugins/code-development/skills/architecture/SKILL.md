---
name: architecture
description: This skill should be used when the user asks about "software architecture", "system design", "microservices", "API design", "design patterns", "DDD", "event-driven architecture", "scalability", "cloud architecture", "technical strategy", "architecture logicielle", "conception système", "architecture cloud", "stratégie technique", "monolith vs microservices", "hexagonal architecture", "clean architecture", "CQRS", "event sourcing", "domain-driven design", "bounded context", "service mesh", "API gateway", "load balancing", "distributed systems", "systèmes distribués", "high availability", "haute disponibilité", "fault tolerance", "tolérance aux pannes", "tech stack", "choix technologiques", "architecture decision record", "ADR", or needs guidance on technical architecture decisions and system design.
version: 1.1.0
last_updated: 2026-02
---

# Software Architecture & System Design

## Overview

Ce skill couvre l'ensemble des disciplines liées à l'architecture logicielle et au design de systèmes. Il fournit un cadre de décision structuré pour concevoir des systèmes robustes, scalables et maintenables. L'architecture logicielle ne se limite pas au choix de technologies : elle englobe la structuration des composants, la gestion des flux de données, les stratégies de déploiement et l'alignement entre contraintes techniques et objectifs métier. Appliquer systématiquement les principes décrits ici pour guider chaque décision architecturale, en privilégiant la simplicité, l'évolutivité et la résilience.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Conception initiale d'un système** : choix de l'architecture globale (monolithe, monolithe modulaire, microservices, serverless), définition des bounded contexts, design des APIs.
- **Revue d'architecture existante** : évaluation de la dette technique architecturale, identification des bottlenecks de scalabilité, audit de résilience.
- **Migration ou modernisation** : transition monolithe vers microservices, migration cloud, adoption de patterns event-driven.
- **Décisions techniques structurantes** : choix de bases de données, stratégies de caching, design de pipelines de données, choix de protocoles de communication.
- **Rédaction d'ADR (Architecture Decision Records)** : documentation formelle des décisions architecturales et de leurs justifications.
- **Scalabilité et performance** : conception pour la montée en charge, stratégies de sharding, patterns de résilience (circuit breaker, bulkhead, retry).
- **Design d'APIs** : conception REST, GraphQL, gRPC, stratégies de versioning, pagination, gestion des erreurs.

## Core Principles

### Principle 1 — Fitness Functions over Gut Feeling
Définir des fitness functions architecturales mesurables pour chaque attribut qualité (latence p99 < 200ms, disponibilité 99.9%, couplage afférent < 5). Utiliser ces métriques pour valider objectivement chaque décision. Ne jamais se fier uniquement à l'intuition.

### Principle 2 — Evolutionary Architecture
Concevoir pour le changement, pas pour la perfection. Appliquer le principe de la "dernière décision responsable" (Last Responsible Moment) : retarder les choix irréversibles, rendre les choix réversibles quand c'est possible. Favoriser les architectures qui permettent l'expérimentation et le pivotement rapide.

### Principle 3 — Domain-Driven Boundaries
Aligner les frontières techniques sur les frontières métier. Utiliser le Domain-Driven Design pour identifier les bounded contexts et les ubiquitous languages. Chaque service ou module doit correspondre à un sous-domaine métier clairement identifié.

### Principle 4 — Appropriate Coupling
Ne pas viser le découplage maximal mais le couplage approprié. Distinguer couplage afférent (incoming) et efférent (outgoing). Accepter un couplage fort au sein d'un bounded context et exiger un couplage lâche entre bounded contexts. Utiliser des contrats (API contracts, event schemas) pour formaliser les interfaces.

### Principle 5 — Observability by Design
Intégrer l'observabilité dès la conception : structured logging, distributed tracing (OpenTelemetry), métriques métier et techniques. Un système non observable est un système non opérable.

### Principle 6 — Security as Architecture
Traiter la sécurité comme une contrainte architecturale de premier ordre, pas comme une couche ajoutée a posteriori. Appliquer les principes de Zero Trust, least privilege, defense in depth dès le design initial.

## Key Frameworks & Methods

### Architecture Styles Decision Matrix

| Style | Quand l'utiliser | Complexité Ops | Coût initial | Scalabilité |
|---|---|---|---|---|
| **Monolithe** | MVP, équipe < 5, domaine simple | Faible | Faible | Verticale |
| **Monolithe modulaire** | Domaine complexe, équipe < 20, besoin d'évolution | Faible | Moyen | Verticale + préparation horizontale |
| **Microservices** | Équipes autonomes, scaling indépendant, domaine mature | Élevée | Élevé | Horizontale fine |
| **Serverless** | Workloads event-driven, trafic imprévisible | Moyenne | Faible | Automatique |
| **Cell-based** | Très haute disponibilité, isolation de défaillance | Très élevée | Très élevé | Horizontale par cellule |

### Domain-Driven Design (DDD)

Appliquer la démarche DDD en deux phases :
1. **Strategic Design** : identifier les domaines, sous-domaines (core, supporting, generic), bounded contexts, et context mapping (ACL, Open Host, Shared Kernel).
2. **Tactical Design** : implémenter les aggregates, entities, value objects, domain events, repositories et domain services à l'intérieur de chaque bounded context.

### Architecture Decision Records (ADR)

Documenter chaque décision architecturale significative selon le format :
- **Titre** : description concise de la décision
- **Contexte** : forces en présence, contraintes, hypothèses
- **Décision** : choix retenu avec justification
- **Conséquences** : impacts positifs, négatifs, risques résiduels
- **Statut** : proposé, accepté, déprécié, remplacé

### Event Storming

Utiliser l'Event Storming comme technique de découverte collaborative pour identifier les domain events, commands, aggregates et bounded contexts. Privilégier cette approche pour aligner développeurs et experts métier avant toute décision architecturale.

## Decision Guide

### Arbre de décision architectural

```
1. Quelle est la taille de l'équipe et sa maturité DevOps ?
   ├── < 5 développeurs, DevOps débutant → Monolithe ou Monolithe modulaire
   ├── 5-20 développeurs, DevOps intermédiaire → Monolithe modulaire
   └── > 20 développeurs, DevOps mature → Microservices ou Cell-based

2. Quel est le profil de charge ?
   ├── Trafic prévisible et stable → Containers (ECS/Kubernetes)
   ├── Trafic imprévisible avec pics → Serverless ou auto-scaling agressif
   └── Trafic très élevé avec besoin d'isolation → Cell-based architecture

3. Quelles sont les contraintes de consistance ?
   ├── Consistance forte requise → Base relationnelle, transactions ACID
   ├── Consistance éventuelle acceptable → Event sourcing, CQRS
   └── Mix des deux → Saga pattern avec compensations

4. Quel est le budget opérationnel ?
   ├── Budget limité → Monolithe sur PaaS, serverless
   ├── Budget moyen → Containers managés, services managés
   └── Budget important → Infrastructure dédiée, multi-region
```

### Critères de choix de communication inter-services

| Critère | Synchrone (REST/gRPC) | Asynchrone (Events/Messages) |
|---|---|---|
| Besoin de réponse immédiate | Oui | Non |
| Tolérance aux pannes | Faible | Élevée |
| Couplage temporel | Fort | Faible |
| Complexité de debug | Faible | Élevée |
| Throughput | Moyen | Élevé |

## Common Patterns & Anti-Patterns

### Patterns recommandés

- **Strangler Fig** : migrer un monolithe progressivement en routant le trafic vers les nouveaux services via un proxy. Ne jamais tenter un big-bang rewrite.
- **CQRS** : séparer les modèles de lecture et d'écriture quand les patterns d'accès divergent significativement. Ne pas appliquer CQRS par défaut — uniquement quand la complexité est justifiée.
- **Event Sourcing** : stocker les événements plutôt que l'état final pour les domaines nécessitant un audit trail complet ou la reconstruction temporelle. Combiner avec CQRS pour les projections de lecture.
- **Saga Pattern** : orchestrer les transactions distribuées via des séquences de transactions locales avec compensations. Préférer les sagas chorégraphiées pour le découplage, les sagas orchestrées pour la visibilité.
- **Sidecar / Ambassador** : externaliser les préoccupations transverses (logging, auth, retry) dans des sidecars pour éviter la contamination du code métier.
- **Backend for Frontend (BFF)** : créer une couche API dédiée par type de client (mobile, web, IoT) pour optimiser les payloads et les interactions.

### Anti-patterns critiques

- **Distributed Monolith** : des microservices couplés temporellement et déployés ensemble. Résultat : la complexité des microservices sans les bénéfices. Diagnostiquer via le test : "Puis-je déployer ce service indépendamment ?"
- **Golden Hammer** : appliquer la même architecture à tous les problèmes. Chaque sous-domaine peut justifier un style différent.
- **Premature Decomposition** : découper en microservices avant de comprendre les frontières du domaine. Commencer par un monolithe modulaire et extraire les services quand les frontières sont stabilisées.
- **Shared Database** : partager une base de données entre services détruit l'encapsulation et crée un couplage invisible. Chaque service doit posséder ses données.
- **Chatty Services** : des services qui s'appellent en cascade pour chaque requête. Regrouper les données nécessaires ou utiliser des événements.

## Implementation Workflow

### Phase 1 — Discovery & Analysis
1. Conduire un Event Storming avec les experts métier pour cartographier le domaine.
2. Identifier les bounded contexts et établir le context map.
3. Classifier les sous-domaines (core, supporting, generic).
4. Documenter les attributs qualité prioritaires (latence, disponibilité, consistance, sécurité).
5. Analyser les contraintes existantes (équipe, budget, timeline, legacy).

### Phase 2 — Architecture Decision
6. Évaluer les styles architecturaux candidats avec la matrice de décision.
7. Rédiger un ADR pour chaque décision structurante.
8. Définir les fitness functions pour valider les attributs qualité.
9. Concevoir le modèle de communication (sync/async, protocols, formats).
10. Définir la stratégie de données (ownership, consistance, partitioning).

### Phase 3 — Design & Prototyping
11. Designer les APIs publiques (contracts-first approach) avec OpenAPI/AsyncAPI.
12. Modéliser les aggregates, entities et value objects (tactical DDD).
13. Concevoir les schémas d'événements (event catalog) avec versioning.
14. Prototyper le chemin critique (walking skeleton) pour valider les choix.
15. Établir les conventions d'observabilité (traces, métriques, logs).

### Phase 4 — Validation & Evolution
16. Valider les fitness functions sur le prototype.
17. Réaliser des chaos engineering tests pour vérifier la résilience.
18. Mettre en place des architectural fitness tests automatisés (ArchUnit, dependency checks).
19. Planifier les revues d'architecture périodiques (Architecture Review Board léger).
20. Maintenir les ADR à jour et documenter les évolutions.



## State of the Art (2025-2026)

L'architecture logicielle évolue vers plus de modularité et d'intelligence :

- **AI-native architectures** : Les applications intègrent nativement des composants IA (LLM, embeddings, agents), nécessitant de nouvelles patterns (RAG, tool use, orchestration d'agents).
- **Edge computing et serverless** : Le déploiement se rapproche des utilisateurs avec des architectures edge-first et des fonctions serverless comme primitives de base.
- **Platform engineering** : Les Internal Developer Platforms (IDP) standardisent l'infrastructure et accélèrent le time-to-market en proposant des abstractions self-service.
- **CQRS et event sourcing mainstreams** : Ces patterns se démocratisent grâce aux outils matures (EventStoreDB, Kafka, Axon) et aux besoins d'auditabilité.
- **WebAssembly (Wasm)** : Wasm émerge comme runtime universel pour les plugins, les edge functions et les applications portables multi-plateformes.

## Template actionnable

### Architecture Decision Record (ADR)

| Champ | Contenu |
|---|---|
| **Titre** | ADR-___: ___ |
| **Date** | ___ |
| **Statut** | Proposé / Accepté / Rejeté / Remplacé |
| **Contexte** | Quel problème résolvons-nous ? |
| **Options envisagées** | Option A: ___ / Option B: ___ / Option C: ___ |
| **Décision** | Nous choisissons l'option ___ parce que ___ |
| **Conséquences** | Positif: ___ / Négatif: ___ / Risques: ___ |
| **Participants** | Qui a participé à la décision ? |

## Prompts types

- "Comment migrer un monolithe vers une architecture microservices ?"
- "Propose une architecture pour une app Next.js à forte charge"
- "CQRS vs architecture classique : quand utiliser quoi ?"
- "Aide-moi à concevoir un système event-driven avec Kafka"
- "Comment structurer une API REST scalable ?"
- "Fais une revue d'architecture de mon projet et identifie les risques"

## Skills connexes

| Skill | Lien |
|---|---|
| Backend & DB | `code-development:backend-db` — Architecture de données et design de schéma |
| DevOps | `code-development:devops` — Infrastructure et déploiement de l'architecture |
| Auth Security | `code-development:auth-security` — Sécurité dans la conception système |
| Code Excellence | `code-development:code-excellence` — Design patterns et principes SOLID |
| IT Systèmes | `entreprise:it-systemes` — Gouvernance IT et architecture d'entreprise |

## Glossaire

| Terme | Définition |
|-------|-----------|
| **DDD (Domain-Driven Design)** | Approche de conception logicielle qui aligne le code sur le domaine métier en utilisant un langage ubiquitaire partagé entre développeurs et experts métier. |
| **Bounded Context** | Frontière explicite à l'intérieur de laquelle un modèle de domaine est défini et applicable. Chaque bounded context possède son propre langage ubiquitaire. |
| **CQRS (Command Query Responsibility Segregation)** | Pattern séparant les modèles de lecture (queries) et d'écriture (commands) pour optimiser indépendamment chaque chemin d'accès aux données. |
| **Event Sourcing** | Pattern de persistance stockant l'historique complet des événements plutôt que l'état final, permettant la reconstruction temporelle et l'audit trail. |
| **ADR (Architecture Decision Record)** | Document formel enregistrant une décision architecturale, son contexte, les options envisagées, la justification et les conséquences. |
| **Strangler Fig** | Pattern de migration progressive d'un monolithe vers de nouveaux services en redirigeant le trafic route par route, sans big-bang rewrite. |
| **API Gateway** | Point d'entrée unique pour les clients qui route les requêtes vers les services backend, gérant authentification, rate limiting et agrégation. |
| **Service Mesh** | Couche d'infrastructure (ex. Istio, Linkerd) gérant la communication inter-services de manière transparente : mTLS, retry, circuit breaking, observabilité. |
| **Monolithe Modulaire** | Architecture monolithique structurée en modules fortement découplés avec des frontières claires, préparant une extraction future en microservices si nécessaire. |
| **Clean Architecture** | Architecture en couches concentriques où les dépendances pointent vers l'intérieur, isolant la logique métier des détails techniques (frameworks, BDD, UI). |
| **Architecture Hexagonale** | Variante de Clean Architecture organisant le code autour de ports (interfaces) et d'adaptateurs (implémentations), séparant le domaine de l'infrastructure. |
| **Fitness Function** | Métrique ou test automatisé évaluant objectivement si l'architecture respecte un attribut qualité donné (latence, couplage, disponibilité). |
| **Cell-based Architecture** | Architecture découpant le système en cellules autonomes et isolées, chacune capable de fonctionner indépendamment pour maximiser la résilience. |
| **Event Storming** | Atelier collaboratif de découverte du domaine où développeurs et experts métier identifient les événements, commandes, agrégats et bounded contexts. |
| **Saga Pattern** | Pattern de gestion des transactions distribuées via une séquence de transactions locales avec des actions de compensation en cas d'échec. |
| **Circuit Breaker** | Pattern de résilience coupant temporairement les appels vers un service défaillant pour éviter la propagation de pannes en cascade. |
| **Sidecar Pattern** | Pattern déployant un conteneur auxiliaire aux côtés du service principal pour gérer des préoccupations transverses (logging, proxy, auth) sans modifier le code métier. |
| **Anti-Corruption Layer** | Couche de traduction isolant un bounded context des modèles externes (legacy, services tiers) pour préserver l'intégrité du modèle de domaine interne. |

## Additional Resources

Consulter les fichiers de référence suivants pour des guides détaillés :

- **[System Design](./references/system-design.md)** : fondamentaux des systèmes distribués, théorème CAP, patterns de consistance, comparaison monolithe / monolithe modulaire / microservices, service mesh, cell-based architecture, patterns modernes 2024-2026.
- **[API Design](./references/api-design.md)** : bonnes pratiques REST, conception de schémas GraphQL, gRPC et protocoles binaires, WebSockets, versioning d'API, pagination, HATEOAS, design API-first moderne.
- **[Design Patterns](./references/design-patterns.md)** : patterns GoF appliqués au développement moderne, principes SOLID, patterns tactiques DDD (aggregates, bounded contexts, domain events), CQRS, event sourcing.
- **[Cloud Architecture](./references/cloud-architecture.md)** : stratégies multi-cloud, serverless, orchestration de containers, edge computing, FinOps, Well-Architected Frameworks (AWS, Azure, GCP), patterns cloud-native modernes.

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.