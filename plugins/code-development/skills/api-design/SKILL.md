---
name: api-design
description: This skill should be used when the user asks about "API design", "REST API", "RESTful", "GraphQL", "gRPC", "API versioning", "API documentation", "OpenAPI", "Swagger", "API gateway", "rate limiting", "API authentication", "OAuth2 API", "API pagination", "API error handling", "API testing", "contract testing", "API-first design", "API lifecycle", "conception d'API", "design d'API", "HATEOAS", "hypermedia API", "API backward compatibility", "breaking changes", "API deprecation", "webhook design", "event-driven API", "API security", "API performance", "API caching", "ETag", "idempotency", "idempotent API", "API monitoring", "API analytics", "developer experience", "DX", "SDK design", "API marketplace", discusses API architecture decisions, or needs guidance on designing, securing, documenting, or evolving APIs.
version: 1.0.0
last_updated: 2026-02
---

# API Design — REST, GraphQL, gRPC & Developer Experience

## Overview

Ce skill couvre l'ensemble de la conception d'APIs, de l'architecture initiale jusqu'à la gestion du cycle de vie et l'expérience développeur. Il intègre les trois paradigmes majeurs (REST, GraphQL, gRPC) et les pratiques transversales (sécurité, documentation, versioning, testing, monitoring). Appliquer systématiquement les principes décrits ici pour concevoir des APIs qui sont prévisibles (les développeurs devinent le comportement correct), évolutives (les changements ne cassent pas les clients existants), sécurisées (defense in depth dès le design) et bien documentées (la documentation est le produit). Une API est un contrat : chaque décision de design impacte tous les consommateurs actuels et futurs.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Conception d'une nouvelle API** : choix du paradigme (REST, GraphQL, gRPC), modélisation des ressources, design des endpoints, conventions de nommage, gestion des erreurs.
- **Versioning et évolution** : stratégies de versioning (URL, header, query param), gestion des breaking changes, politique de dépréciation, migration des clients.
- **Sécurité des APIs** : authentification (OAuth2, API keys, JWT, mTLS), autorisation (RBAC, ABAC, scopes), rate limiting, input validation, protection contre les abus.
- **Documentation et DX** : OpenAPI/Swagger, portails développeur, SDKs, exemples, sandbox, changelogs.
- **Performance et scalabilité** : pagination, filtering, caching (ETags, Cache-Control), compression, batching, connection pooling.
- **Testing et qualité** : contract testing (Pact), integration testing, load testing, mocking, API linting (Spectral).
- **Monitoring et observabilité** : métriques d'usage, latence par endpoint, error rates, alerting, API analytics.

## Core Principles

### Principle 1 — API-First Design

Concevoir l'API avant d'écrire le code d'implémentation. Rédiger la spécification OpenAPI/protobuf comme premier livrable, la faire reviewer par les consommateurs, puis implémenter. L'API-first élimine les incohérences entre ce que le backend offre et ce que le frontend/client attend. Utiliser des outils de mock (Prism, WireMock) pour permettre le développement parallèle.

### Principle 2 — Consistency Over Cleverness

Une API prévisible vaut mieux qu'une API élégante. Appliquer des conventions uniformes sur toute l'API : nommage (snake_case ou camelCase, pas les deux), format de date (ISO 8601), structure d'erreur (toujours le même format), pagination (même mécanisme partout). Les développeurs apprennent les conventions une fois et les appliquent partout. Utiliser un linter (Spectral) pour garantir la cohérence automatiquement.

### Principle 3 — Design for Failure

Chaque appel API peut échouer. Concevoir l'API pour que les échecs soient gérables : codes d'erreur précis et documentés, messages d'erreur actionnables (pas "Internal Server Error" mais "The field 'email' is required and must be a valid email address"), idempotency keys pour les opérations de mutation, retry-after headers pour le rate limiting.

### Principle 4 — Backward Compatibility as Default

Ne jamais casser un client existant sans processus de migration explicite. Chaque changement d'API doit être évalué : additive change (nouveau champ optionnel → safe), breaking change (suppression de champ, changement de type → migration requise). Appliquer le principe de Robustness (Postel's Law) : être strict dans ce qu'on envoie, tolérant dans ce qu'on accepte.

### Principle 5 — Least Privilege & Defense in Depth

Chaque consommateur d'API ne doit accéder qu'aux ressources et actions nécessaires. Implémenter l'autorisation granulaire (scopes OAuth2, RBAC), le rate limiting par consommateur, la validation stricte des entrées (schema validation, size limits), et le logging de chaque accès. Ne jamais exposer des données internes (IDs séquentiels, stack traces, chemins de fichiers) dans les réponses.

### Principle 6 — Documentation is the Product

Pour une API, la documentation est l'interface utilisateur. Une API mal documentée est une API inutilisable, quelle que soit la qualité de l'implémentation. Documenter chaque endpoint avec : description, paramètres, exemples de requête et réponse, codes d'erreur possibles, et cas d'usage. Maintenir la documentation synchronisée avec le code (génération depuis OpenAPI spec).

## Key Frameworks & Methods

### API Paradigm Comparison

| Critère | REST | GraphQL | gRPC |
|---|---|---|---|
| **Protocol** | HTTP/1.1 ou 2 | HTTP/1.1 ou 2 | HTTP/2 (obligatoire) |
| **Format** | JSON (typique) | JSON | Protocol Buffers (binaire) |
| **Schéma** | OpenAPI (optionnel) | Schema (obligatoire) | Protobuf (obligatoire) |
| **Over-fetching** | Fréquent | Résolu (query sélective) | Résolu (messages typés) |
| **Under-fetching** | Fréquent (N+1) | Résolu (query imbriquée) | Résolu (streaming) |
| **Caching** | Natif HTTP (ETags, CDN) | Complexe (POST-based) | Limité |
| **Real-time** | SSE, WebSocket (ajout) | Subscriptions (natif) | Streaming bidirectionnel (natif) |
| **Tooling** | Mature, universel | Bon, écosystème riche | Bon, code generation |
| **Courbe d'apprentissage** | Faible | Moyenne | Élevée |
| **Idéal pour** | APIs publiques, CRUD, microservices | Apps mobiles/SPA, BFF | Inter-services, haute performance |

### REST Resource Design

```
Conventions de nommage :
+-- Noms de ressources au pluriel : /users, /orders, /products
+-- Noms en kebab-case pour multi-mots : /order-items, /user-profiles
+-- Hiérarchie via nesting (max 2 niveaux) : /users/{id}/orders
+-- Au-delà de 2 niveaux : utiliser des query params ou des liens

Méthodes HTTP :
+-- GET    /resources          → Liste (200)
+-- GET    /resources/{id}     → Détail (200, 404)
+-- POST   /resources          → Création (201, 400, 409)
+-- PUT    /resources/{id}     → Remplacement complet (200, 404)
+-- PATCH  /resources/{id}     → Mise à jour partielle (200, 404)
+-- DELETE /resources/{id}     → Suppression (204, 404)

Actions non-CRUD :
+-- POST /orders/{id}/cancel   → Action sur ressource
+-- POST /reports/generate     → Opération longue (202 + Location header)
```

### Pagination Patterns

| Pattern | Mécanisme | Forces | Faiblesses | Quand l'utiliser |
|---|---|---|---|---|
| **Offset** | `?offset=20&limit=10` | Simple, saut possible | Lent sur gros datasets, drift | CRUD simple, < 100K items |
| **Cursor** | `?cursor=abc123&limit=10` | Performant, stable | Pas de saut, opaque | Feeds, datasets larges, temps réel |
| **Keyset** | `?after_id=123&limit=10` | Très performant | Tri sur colonne indexée requis | Haute performance, tri fixe |
| **Page** | `?page=3&per_page=10` | Intuitif pour l'UI | Mêmes limites qu'offset | APIs grand public, UI paginée |

### Error Response Standard

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request body contains invalid fields.",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address."
      },
      {
        "field": "age",
        "code": "OUT_OF_RANGE",
        "message": "Must be between 18 and 120."
      }
    ],
    "request_id": "req_abc123",
    "documentation_url": "https://api.example.com/docs/errors#VALIDATION_ERROR"
  }
}
```

Principes : toujours le même format (erreur simple ou multiple), code machine-readable + message human-readable, request_id pour le debugging, lien vers la documentation.

### Versioning Strategies

| Stratégie | Exemple | Forces | Faiblesses | Quand l'utiliser |
|---|---|---|---|---|
| **URL path** | `/v1/users` | Explicite, simple | Duplication de routes | APIs publiques, breaking changes rares |
| **Header** | `API-Version: 2` | URL propre | Moins visible, tooling limité | APIs internes, évolution fine |
| **Query param** | `?version=2` | Simple à tester | Pollue l'URL | Transition, testing |
| **Content negotiation** | `Accept: application/vnd.api+json;v=2` | Standard HTTP | Complexe | APIs avancées, hypermedia |
| **Date-based** | `Stripe-Version: 2025-02-15` | Granulaire, progressif | Complexité de gestion | APIs avec évolution continue (Stripe) |

## Decision Guide

### Choix du paradigme API

```
1. Qui sont les consommateurs ?
   +-- Grand public / développeurs tiers → REST (standard, bien compris)
   +-- Frontend interne (SPA/mobile) → GraphQL (flexibilité des queries)
   +-- Microservices internes → gRPC (performance, contrat fort)

2. Quels patterns de données ?
   +-- CRUD simple → REST
   +-- Requêtes complexes, données imbriquées → GraphQL
   +-- Streaming, haute fréquence → gRPC

3. Quelles contraintes ?
   +-- Caching HTTP critique → REST (caching natif)
   +-- Bande passante limitée (mobile) → GraphQL ou gRPC
   +-- Latence ultra-faible requise → gRPC
```

### Breaking change ou non ?

```
Safe (non-breaking) :
+-- Ajouter un champ optionnel en response
+-- Ajouter un endpoint
+-- Ajouter un query parameter optionnel
+-- Ajouter une valeur à un enum (côté réponse)
+-- Augmenter une limite de rate

Breaking :
+-- Supprimer ou renommer un champ
+-- Changer le type d'un champ
+-- Ajouter un champ required en request
+-- Changer un code de statut HTTP
+-- Modifier la sémantique d'un endpoint existant
+-- Réduire une limite de rate
```

## Common Patterns & Anti-Patterns

### Patterns recommandés

- **Idempotency Keys** : pour toutes les opérations POST/PATCH, accepter un header `Idempotency-Key` fourni par le client. Stocker le résultat de la première exécution et le retourner pour les requêtes dupliquées. Élimine les problèmes de double-soumission et de retry.
- **Health Check & Status** : exposer `GET /health` (liveness), `GET /ready` (readiness) et `GET /status` (informations de version et dépendances). Essentiel pour le monitoring et l'orchestration (Kubernetes).
- **Request ID Propagation** : générer un `X-Request-ID` unique par requête (UUID v7), le propager à travers tous les services, le retourner dans la réponse. Permet le tracing distribué et le debugging.
- **Webhook Design** : pour les notifications asynchrones, implémenter des webhooks avec : signature HMAC pour l'authenticité, retry avec backoff exponentiel, endpoint de vérification, logs d'envoi consultables.

### Anti-patterns critiques

- **Chatty API** : forcer le client à faire 10 appels pour afficher une page. Concevoir des endpoints qui retournent les données nécessaires en 1-2 appels (BFF pattern, sparse fieldsets, ou GraphQL).
- **God Endpoint** : un seul endpoint `/api/data` qui accepte un JSON avec une "action" et retourne n'importe quoi. Utiliser des ressources et méthodes HTTP explicites.
- **Leaky Abstraction** : exposer la structure interne de la base de données dans l'API (noms de colonnes, IDs auto-incrémentés, relations internes). L'API est un contrat public, pas un miroir de la BDD.
- **Versioning Avoidance** : ne jamais versionner et casser les clients sans préavis. Implémenter un processus de dépréciation (sunset header, timeline, migration guide).
- **Inconsistent Errors** : retourner un format d'erreur différent selon l'endpoint ou le type d'erreur. Standardiser le format d'erreur sur toute l'API.

## Implementation Workflow

### Phase 1 — Design & Contract

1. Identifier les consommateurs et leurs besoins (frontend, mobile, tiers, services internes).
2. Choisir le paradigme (REST, GraphQL, gRPC) selon le Decision Guide.
3. Modéliser les ressources et leurs relations (ERD → Resource model).
4. Rédiger la spécification OpenAPI / schema GraphQL / protobuf.
5. Review de la spec par les consommateurs. Itérer jusqu'à consensus.

### Phase 2 — Implémentation

6. Générer les stubs serveur et les SDKs client depuis la spec.
7. Implémenter les endpoints avec validation stricte des entrées (schema validation).
8. Implémenter l'authentification, l'autorisation et le rate limiting.
9. Configurer la pagination, le filtering et le sorting selon les conventions choisies.
10. Implémenter la gestion d'erreurs standardisée et l'idempotency.

### Phase 3 — Documentation & Testing

11. Générer la documentation depuis la spec OpenAPI (Redoc, Stoplight).
12. Ajouter des exemples de requête/réponse pour chaque endpoint.
13. Écrire les contract tests (Pact) pour chaque consommateur.
14. Écrire les integration tests et les load tests (k6, Artillery).
15. Configurer le linting de la spec (Spectral) dans le CI/CD.

### Phase 4 — Production & Évolution

16. Déployer avec monitoring : latence par endpoint, error rate, usage par consommateur.
17. Configurer les alertes : latence p99, error rate, rate limit hits.
18. Publier le changelog et le portail développeur.
19. Mettre en place le processus de dépréciation (Sunset header, timeline, communication).
20. Collecter les feedbacks développeurs et itérer sur la DX.

## Modèle de maturité

### Niveau 1 — Ad-hoc
- Les APIs sont conçues au fil de l'eau sans conventions ni documentation
- Pas de versioning, les breaking changes cassent les clients sans préavis
- Authentification basique ou absente, pas de rate limiting
- **Indicateurs** : pas de spec OpenAPI, pas de convention de nommage, erreurs non standardisées

### Niveau 2 — Standardisé
- Des conventions existent (nommage, format d'erreur, pagination) et sont documentées
- La spec OpenAPI est maintenue et la documentation est générée
- L'authentification OAuth2/API key est en place avec rate limiting basique
- **Indicateurs** : spec OpenAPI à jour, conventions documentées, auth + rate limiting actifs

### Niveau 3 — Contract-Driven
- L'API est conçue API-first : spec avant implémentation
- Les contract tests valident la compatibilité avec chaque consommateur
- Le versioning et la politique de dépréciation sont formalisés
- **Indicateurs** : contract tests dans le CI, changelog publié, zero breaking changes non-annoncés

### Niveau 4 — Optimisé
- Le portail développeur offre une DX excellente (sandbox, SDKs, exemples)
- Le monitoring avancé (usage analytics, latence par endpoint, coût par consommateur)
- L'API linting automatique bloque les violations de conventions en CI
- **Indicateurs** : developer NPS > 50, TTFHW (time to first hello world) < 15 min, 100% des endpoints documentés

### Niveau 5 — Platform
- L'API est un produit avec sa propre roadmap, ses métriques et son product owner
- L'API marketplace interne permet la découverte et la composition de services
- L'évolution est pilotée par les métriques d'usage et les feedbacks développeurs
- **Indicateurs** : API-as-a-product, > 80% de réutilisation, governance automatisée

## Rythme opérationnel

| Cadence | Activité | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Continue** | Monitoring latence, erreurs, usage par endpoint | Backend team | Dashboard temps réel |
| **Hebdomadaire** | Review des feedbacks développeurs et des tickets API | API Owner | Actions priorisées |
| **Bi-mensuel** | Revue des conventions et linting rules | API Guild | Standards mis à jour |
| **Mensuel** | Revue des métriques d'usage (endpoints populaires, abandonnés) | API Owner | Rapport d'usage + décisions |
| **Trimestriel** | Revue de la politique de versioning et dépréciation | API Guild + Tech Lead | Roadmap API + sunset plan |
| **Annuel** | Audit de sécurité API (OWASP API Top 10) | Security team | Rapport d'audit + remédiations |

## State of the Art (2025-2026)

Le design d'API évolue vers plus d'automatisation et une meilleure DX :

- **API-First Toolchains** : les outils comme Stoplight, Bump.sh et Speakeasy permettent de concevoir, documenter, générer des SDKs et tester depuis une seule spec OpenAPI. Le workflow design→mock→implement→document est entièrement automatisé.
- **AI-Assisted API Design** : les LLMs assistent la conception (génération de specs depuis des descriptions en langage naturel), le review (détection d'incohérences, suggestions de conventions) et la documentation (exemples générés automatiquement).
- **Type-Safe SDKs** : la génération de SDKs type-safe dans tous les langages majeurs depuis OpenAPI ou protobuf devient standard (Speakeasy, openapi-typescript, connectrpc).
- **API Observability Platforms** : les plateformes comme Moesif, Akita et Optic analysent le trafic API réel pour détecter les breaking changes, les patterns d'usage anormaux et les opportunités d'optimisation.
- **Event-Driven APIs** : les webhooks et AsyncAPI se standardisent pour les notifications asynchrones. CloudEvents émerge comme format commun pour les événements inter-services.

## Template actionnable

### API Design Checklist

| Élément | Question de vérification | Status |
|---|---|---|
| **Ressources** | Les noms de ressources sont-ils des noms au pluriel ? | ___ |
| **Méthodes** | Chaque endpoint utilise-t-il la méthode HTTP appropriée ? | ___ |
| **Erreurs** | Le format d'erreur est-il standardisé sur toute l'API ? | ___ |
| **Pagination** | Toutes les listes sont-elles paginées ? | ___ |
| **Versioning** | La stratégie de versioning est-elle définie ? | ___ |
| **Auth** | L'authentification et l'autorisation sont-elles en place ? | ___ |
| **Rate limiting** | Le rate limiting est-il configuré par consommateur ? | ___ |
| **Idempotency** | Les mutations supportent-elles l'idempotency ? | ___ |
| **Documentation** | Chaque endpoint a-t-il des exemples req/res ? | ___ |
| **Contract tests** | Les contrats sont-ils validés en CI ? | ___ |

## Prompts types

- "Conçois une API REST pour un système de gestion de commandes"
- "Comment versionner mon API sans casser les clients existants ?"
- "Aide-moi à choisir entre REST, GraphQL et gRPC pour mon use case"
- "Review ma spec OpenAPI et identifie les incohérences"
- "Comment implémenter le rate limiting et la pagination cursor-based ?"
- "Conçois un système de webhooks robuste avec retry et signature"
- "Comment migrer mon API de v1 à v2 sans downtime ?"
- "Aide-moi à standardiser le format d'erreur de mon API"

## Limites et Red Flags

Ce skill n'est PAS adapté pour :
- ❌ **Architecture système globale** (microservices, event-driven, DDD) → Utiliser plutôt : `code-development:architecture`
- ❌ **Sécurité applicative générale** (auth flows, OWASP web, encryption) → Utiliser plutôt : `code-development:auth-security`
- ❌ **Backend et bases de données** (schema design, queries, ORM) → Utiliser plutôt : `code-development:backend-db`
- ❌ **DevOps et infrastructure** (CI/CD, déploiement, scaling) → Utiliser plutôt : `code-development:devops`
- ❌ **Product analytics et tracking** (event tracking, funnels) → Utiliser plutôt : `code-development:product-analytics`

Signaux d'alerte en cours d'utilisation :
- ⚠️ Pas de spec OpenAPI/protobuf — l'API n'a pas de contrat, les changements sont risqués
- ⚠️ Les erreurs retournent des formats différents selon les endpoints — incohérence critique
- ⚠️ Pas de versioning et des breaking changes en production — les clients vont casser
- ⚠️ La documentation est désynchronisée du code — les développeurs n'ont pas confiance

## Skills connexes

| Skill | Lien |
|---|---|
| Architecture | `code-development:architecture` — Design système et bounded contexts |
| Auth & Security | `code-development:auth-security` — Sécurité des APIs (OAuth2, JWT) |
| Backend & DB | `code-development:backend-db` — Implémentation backend des APIs |
| DevOps | `code-development:devops` — Déploiement et scaling des APIs |
| Monitoring | `code-development:monitoring` — Observabilité des APIs en production |
| Quality & Reliability | `code-development:quality-reliability` — Testing et fiabilité |

## Additional Resources

Consulter les fichiers de référence suivants pour des guides détaillés :

- **[REST Design Patterns](./references/rest-design-patterns.md)** : principes REST détaillés, resource modeling, HTTP methods, status codes, HATEOAS, pagination avancée, filtering, sorting, partial responses, bulk operations, state of the art 2025-2026.
- **[GraphQL & gRPC](./references/graphql-grpc.md)** : schema design GraphQL, resolvers, subscriptions, DataLoader, gRPC/protobuf, streaming, comparaison de performance, migration entre paradigmes, state of the art 2025-2026.
- **[API Security & Operations](./references/api-security-operations.md)** : authentification (OAuth2 flows, API keys, mTLS), rate limiting, documentation (OpenAPI), testing (contract, integration, load), monitoring, OWASP API Top 10, state of the art 2025-2026.
- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.
