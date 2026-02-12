# API Design — Modern API-First Patterns

## Overview

Ce document de référence couvre les principes et bonnes pratiques de conception d'APIs modernes. Il traite REST, GraphQL, gRPC, WebSockets et les patterns émergents de 2024-2026. Appliquer une approche API-first : concevoir le contrat d'API avant l'implémentation, traiter l'API comme un produit à part entière.

---

## API-First Design Philosophy

### Principes fondamentaux

1. **Contract-First** : définir le contrat d'API (OpenAPI, GraphQL schema, Protocol Buffers) avant d'écrire une ligne de code. Le contrat est la spécification, le code est l'implémentation.
2. **API as a Product** : traiter l'API comme un produit avec des utilisateurs (consommateurs), une documentation, un versioning, un support et un cycle de vie.
3. **Consumer-Driven** : concevoir l'API du point de vue du consommateur. Pratiquer le Consumer-Driven Contract Testing (Pact) pour garantir que l'API répond aux besoins réels.
4. **Consistency** : appliquer les mêmes conventions (nommage, pagination, erreurs, authentification) sur toutes les APIs. Établir un API Style Guide partagé.

### API Style Guide — Éléments essentiels

Définir et documenter les conventions suivantes dans un API Style Guide d'organisation :
- Conventions de nommage (camelCase, snake_case, kebab-case).
- Format des URLs et structure des ressources.
- Codes HTTP standards et format d'erreur unifié.
- Mécanisme d'authentification et d'autorisation.
- Patterns de pagination et de filtrage.
- Stratégie de versioning.
- Rate limiting et quotas.
- Format des timestamps (ISO 8601, toujours UTC).

---

## REST API Design

### Resource Design

#### Conventions de nommage
- Utiliser des noms pluriels pour les collections : `/orders`, `/users`, `/products`.
- Utiliser des identifiants uniques dans les URLs : `/orders/{orderId}`.
- Nester les ressources pour exprimer les relations : `/users/{userId}/orders`.
- Limiter le nesting à 2 niveaux maximum. Au-delà, utiliser des query parameters ou des liens HATEOAS.
- Utiliser des noms, pas des verbes : `/orders` (correct) vs `/getOrders` (incorrect).

#### Méthodes HTTP et sémantique

| Méthode | Sémantique | Idempotent | Safe | Exemple |
|---|---|---|---|---|
| **GET** | Lecture | Oui | Oui | `GET /orders/123` |
| **POST** | Création | Non | Non | `POST /orders` |
| **PUT** | Remplacement complet | Oui | Non | `PUT /orders/123` |
| **PATCH** | Modification partielle | Idéalement oui | Non | `PATCH /orders/123` |
| **DELETE** | Suppression | Oui | Non | `DELETE /orders/123` |

#### Actions non-CRUD
Pour les actions qui ne correspondent pas au modèle CRUD, utiliser des sous-ressources verbales :
- `POST /orders/123/cancel` — annuler une commande
- `POST /orders/123/refund` — rembourser une commande
- `POST /users/456/activate` — activer un utilisateur

Alternatif : utiliser des ressources qui représentent le processus :
- `POST /order-cancellations` avec `{ "orderId": "123" }`

### HTTP Status Codes

#### Codes de succès
- **200 OK** : requête réussie avec body de réponse.
- **201 Created** : ressource créée, inclure le header `Location` avec l'URL de la nouvelle ressource.
- **202 Accepted** : requête acceptée pour traitement asynchrone. Retourner un lien vers le statut de l'opération.
- **204 No Content** : succès sans body (typiquement pour DELETE ou PUT).

#### Codes d'erreur client
- **400 Bad Request** : payload invalide, validation échouée.
- **401 Unauthorized** : authentification requise ou invalide.
- **403 Forbidden** : authentifié mais non autorisé.
- **404 Not Found** : ressource inexistante.
- **409 Conflict** : conflit avec l'état actuel (violation de contrainte, version conflict).
- **422 Unprocessable Entity** : syntaxe correcte mais sémantiquement invalide.
- **429 Too Many Requests** : rate limit dépassé. Inclure le header `Retry-After`.

#### Codes d'erreur serveur
- **500 Internal Server Error** : erreur inattendue. Ne jamais exposer les stack traces en production.
- **502 Bad Gateway** : erreur du service upstream.
- **503 Service Unavailable** : service temporairement indisponible. Inclure `Retry-After`.
- **504 Gateway Timeout** : timeout du service upstream.

### Error Response Format

Adopter un format d'erreur unifié et structuré conforme à RFC 9457 (Problem Details for HTTP APIs) :

```json
{
  "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient Funds",
  "status": 422,
  "detail": "Account balance (50.00 EUR) is insufficient for the requested transfer (150.00 EUR).",
  "instance": "/transfers/txn-789",
  "errors": [
    {
      "field": "amount",
      "message": "Amount exceeds available balance",
      "code": "INSUFFICIENT_BALANCE"
    }
  ],
  "traceId": "abc-123-def"
}
```

### Pagination

#### Cursor-Based Pagination (recommandé)
Préférer la pagination par curseur pour les jeux de données dynamiques et les grandes collections. Plus performante et cohérente que l'offset-based pagination.

```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTAwfQ==",
    "previous_cursor": "eyJpZCI6NTB9",
    "has_more": true,
    "limit": 25
  }
}
```

Requête : `GET /orders?cursor=eyJpZCI6MTAwfQ==&limit=25`

Avantages : pas de problème de décalage lors d'insertions/suppressions, performance constante (pas d'OFFSET SQL).

#### Offset-Based Pagination
Acceptable pour les petites collections statiques ou les interfaces administrateur avec numérotation de pages.

```
GET /orders?page=3&per_page=25
```

Retourner les métadonnées : `total_count`, `total_pages`, `current_page`.

#### Keyset Pagination
Variante du cursor-based utilisant les valeurs des colonnes triées :

```
GET /orders?created_after=2025-01-15T10:00:00Z&limit=25
```

Très performant avec un index sur la colonne de tri. Recommandé pour les APIs internes à haute performance.

### Filtering, Sorting & Field Selection

#### Filtering
```
GET /orders?status=pending&created_after=2025-01-01&customer_id=CUST-789
GET /products?price_min=10&price_max=100&category=electronics
```

Pour des filtres complexes, considérer un query parameter dédié :
```
GET /orders?filter=status eq 'pending' and total gt 100
```

#### Sorting
```
GET /orders?sort=-created_at,+total_amount
```

Convention : `+` pour ascendant (défaut), `-` pour descendant. Supporter le tri multi-colonnes.

#### Field Selection (Sparse Fieldsets)
Permettre aux clients de sélectionner les champs retournés pour réduire la taille des payloads :
```
GET /orders?fields=id,status,total_amount,customer.name
```

### HATEOAS — Hypermedia as the Engine of Application State

Inclure des liens hypermedia dans les réponses pour guider les clients à travers les états possibles :

```json
{
  "id": "ORD-123",
  "status": "pending",
  "total": 149.99,
  "_links": {
    "self": { "href": "/orders/ORD-123" },
    "cancel": { "href": "/orders/ORD-123/cancel", "method": "POST" },
    "payment": { "href": "/orders/ORD-123/payment", "method": "POST" },
    "customer": { "href": "/customers/CUST-789" }
  }
}
```

Appliquer HATEOAS quand l'API a des workflows complexes avec des transitions d'état. Ne pas l'appliquer systématiquement pour des APIs CRUD simples.

### API Versioning

#### Stratégies

| Stratégie | Mécanisme | Avantages | Inconvénients |
|---|---|---|---|
| **URL path** | `/v1/orders`, `/v2/orders` | Simple, explicite, cacheable | Duplique les routes, URL change |
| **Header** | `Accept: application/vnd.api+json;version=2` | URL stable | Moins visible, pas cacheable par CDN |
| **Query param** | `/orders?version=2` | Simple | Pollue les query params |

**Recommandation** : utiliser le versioning par URL path pour les APIs publiques (simplicité et clarté). Utiliser le header versioning pour les APIs internes quand la stabilité des URLs est importante.

#### Règles d'évolution
- **Non-breaking changes** (pas de nouvelle version) : ajouter des champs optionnels, ajouter de nouveaux endpoints, ajouter des valeurs à une enum (si le client est tolérant).
- **Breaking changes** (nouvelle version) : supprimer un champ, renommer un champ, changer le type d'un champ, modifier la sémantique d'un endpoint.
- **Deprecation policy** : annoncer la dépréciation au moins 6 mois avant le retrait. Utiliser les headers `Deprecation` et `Sunset` (RFC 8594).

---

## GraphQL Schema Design

### Quand choisir GraphQL
- Clients avec des besoins de données très variables (mobile vs desktop).
- Over-fetching ou under-fetching significatif avec REST.
- Besoin de composition de données provenant de plusieurs sources.
- Équipe frontend demandant plus d'autonomie sur les données.

### Quand NE PAS choisir GraphQL
- API simple avec des patterns d'accès prévisibles.
- API publique avec des consommateurs non contrôlés (risque de requêtes abusives).
- Besoin de caching HTTP simple (GraphQL utilise POST, donc pas de cache CDN par défaut).
- Équipe sans expérience GraphQL (courbe d'apprentissage non triviale).

### Schema Design Principles

#### Nommage
- Types en PascalCase : `Order`, `Customer`, `ProductVariant`.
- Champs en camelCase : `createdAt`, `totalAmount`, `shippingAddress`.
- Enums en SCREAMING_SNAKE_CASE : `ORDER_STATUS`, `PAYMENT_METHOD`.
- Mutations en verbe + nom : `createOrder`, `cancelOrder`, `updateShippingAddress`.

#### Design des Queries

```graphql
type Query {
  # Récupération par ID — retourner nullable pour gérer le 404
  order(id: ID!): Order

  # Liste avec pagination, filtrage et tri
  orders(
    first: Int
    after: String
    filter: OrderFilter
    orderBy: OrderSortInput
  ): OrderConnection!
}

# Relay-style pagination (recommandé)
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

#### Design des Mutations

```graphql
# Input type dédié par mutation
input CreateOrderInput {
  customerId: ID!
  items: [OrderItemInput!]!
  shippingAddress: AddressInput!
}

# Payload de retour unifié
type CreateOrderPayload {
  order: Order
  errors: [UserError!]!
}

type UserError {
  field: [String!]
  message: String!
  code: ErrorCode!
}

type Mutation {
  createOrder(input: CreateOrderInput!): CreateOrderPayload!
  cancelOrder(input: CancelOrderInput!): CancelOrderPayload!
}
```

#### Subscriptions pour le temps réel

```graphql
type Subscription {
  orderStatusChanged(orderId: ID!): OrderStatusEvent!
  newOrderPlaced(restaurantId: ID!): Order!
}
```

### Performance & Security

#### Query Complexity Analysis
Limiter la complexité des requêtes pour prévenir les abus :
- **Depth limiting** : limiter la profondeur de nesting (max 7-10 niveaux).
- **Cost analysis** : attribuer un coût à chaque champ et rejeter les requêtes dépassant un budget.
- **Persisted queries** : en production, n'accepter que les requêtes pré-enregistrées (whitelisting). Élimine les requêtes arbitraires.

#### DataLoader Pattern
Utiliser le DataLoader pattern pour résoudre le problème N+1 :
- Batcher les requêtes à la base de données par type de ressource.
- Cacher les résultats dans le scope de la requête (request-scoped cache).
- Implémenter avec la bibliothèque DataLoader (JavaScript), ou équivalents dans d'autres langages.

#### Federation (GraphQL Federation v2)
Pour les architectures microservices, utiliser Apollo Federation v2 pour composer un supergraph à partir de sous-graphes indépendants :
- Chaque service possède son sous-graphe (subgraph).
- Le router (Apollo Router) compose les sous-graphes en un schéma unifié.
- Utiliser les directives `@key`, `@shareable`, `@external` pour définir les entités partagées.

---

## gRPC — High-Performance Communication

### Quand choisir gRPC
- Communication interne entre microservices (service-to-service).
- Besoin de haute performance et faible latence.
- APIs avec contrats stricts et évolution contrôlée.
- Streaming bidirectionnel (real-time data feeds, chat).
- Environnements polyglots (Protocol Buffers génèrent du code dans 10+ langages).

### Protocol Buffers Best Practices

```protobuf
syntax = "proto3";

package order.v1;

// Utiliser des messages dédiés pour les requêtes et réponses
service OrderService {
  rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc ListOrders(ListOrdersRequest) returns (ListOrdersResponse);
  rpc StreamOrderUpdates(StreamOrderUpdatesRequest) returns (stream OrderUpdate);
}

message CreateOrderRequest {
  string customer_id = 1;
  repeated OrderItem items = 2;
  Address shipping_address = 3;

  // Réserver les numéros de champs supprimés
  reserved 4, 5;
  reserved "deprecated_field";
}

message CreateOrderResponse {
  Order order = 1;
}

message ListOrdersRequest {
  int32 page_size = 1;
  string page_token = 2;  // Cursor-based pagination
  string filter = 3;       // CEL expression
  string order_by = 4;     // e.g., "created_at desc"
}

message ListOrdersResponse {
  repeated Order orders = 1;
  string next_page_token = 2;
  int32 total_size = 3;
}
```

#### Règles d'évolution des Protocol Buffers
- **Ne jamais** réutiliser un numéro de champ supprimé (utiliser `reserved`).
- **Ne jamais** changer le type d'un champ existant.
- Ajouter des champs optionnels est toujours safe (backward et forward compatible).
- Utiliser `oneof` pour les champs mutuellement exclusifs.
- Préfixer les packages avec le domaine et la version : `company.service.v1`.

### gRPC Communication Patterns

| Pattern | Description | Cas d'usage |
|---|---|---|
| **Unary** | Requête/réponse simple | CRUD standard |
| **Server streaming** | Le serveur envoie un flux | Feeds de données, exports volumineux |
| **Client streaming** | Le client envoie un flux | Upload de fichiers, ingestion batch |
| **Bidirectional streaming** | Flux dans les deux sens | Chat, collaboration temps réel |

### gRPC-Web & Connect
Pour exposer gRPC aux clients web :
- **gRPC-Web** : proxy (Envoy) pour traduire gRPC vers HTTP/1.1. Support limité (unary et server streaming).
- **Connect Protocol (Buf)** : protocole moderne compatible gRPC qui fonctionne nativement en HTTP/1.1 et HTTP/2. Supporte les appels gRPC, gRPC-Web et un format JSON natif. Recommandé pour les nouveaux projets (2024-2026).

---

## WebSockets & Real-Time

### Quand utiliser WebSockets
- Notifications en temps réel (dashboards, alertes).
- Applications collaboratives (édition simultanée, whiteboard).
- Chat et messagerie.
- Live data feeds (cours boursiers, scores sportifs).

### Alternatives à considérer
- **Server-Sent Events (SSE)** : plus simple que WebSockets pour le streaming serveur vers client uniquement. Supporte la reconnexion automatique. Recommandé quand le flux est unidirectionnel.
- **HTTP/2 Server Push** : déprécié par les navigateurs. Ne plus utiliser.
- **HTTP Streaming (chunked transfer)** : pour le streaming de réponses longues (LLM responses, fichiers volumineux).
- **WebTransport** : standard émergent basé sur HTTP/3 et QUIC. Supporte le streaming multiplexé et la communication non fiable (datagrams). À surveiller pour 2025-2026.

### WebSocket Design Patterns

#### Message Format
Adopter un format de message unifié :

```json
{
  "type": "order.status_changed",
  "id": "msg-uuid",
  "timestamp": "2025-01-15T10:30:00Z",
  "payload": {
    "orderId": "ORD-123",
    "previousStatus": "pending",
    "newStatus": "confirmed"
  }
}
```

#### Connection Management
- Implémenter le heartbeat/ping-pong pour détecter les connexions mortes.
- Gérer la reconnexion avec exponential backoff côté client.
- Utiliser des rooms/channels pour le multicast ciblé.
- Authentifier lors du handshake (token dans le query param ou le premier message).
- Limiter le nombre de connexions par utilisateur.

---

## API Security

### Authentication Patterns

#### OAuth 2.0 + OpenID Connect
Standard pour l'authentification et l'autorisation des APIs. Flux recommandés :
- **Authorization Code + PKCE** : applications web et mobile (flow le plus sécurisé pour les clients publics).
- **Client Credentials** : communication service-to-service (machine-to-machine).
- **Device Authorization** : IoT et smart TV.

#### API Keys
Pour les APIs publiques avec besoin de tracking simple. Ne pas utiliser comme seul mécanisme d'authentification — combiner avec OAuth pour les opérations sensibles.

#### JWT Best Practices
- Garder les tokens courts (expiration 15 minutes pour les access tokens).
- Utiliser les refresh tokens (rotation et détection de réutilisation).
- Ne stocker que le minimum dans le payload JWT (sub, roles, permissions).
- Valider systématiquement : signature, expiration, issuer, audience.
- Utiliser RS256 ou EdDSA plutôt que HS256 pour les systèmes distribués.

### Rate Limiting Headers

Inclure systématiquement les headers de rate limiting :
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 742
X-RateLimit-Reset: 1705312800
Retry-After: 30
```

### API Gateway Patterns

Utiliser un API Gateway comme point d'entrée unique :
- **Authentification centralisée** : valider les tokens une seule fois.
- **Rate limiting** : protéger les services backend.
- **Request/response transformation** : adapter les formats.
- **Caching** : cacher les réponses fréquentes.
- **Observabilité** : centraliser les métriques et le logging.

Options modernes : Kong, Tyk, AWS API Gateway, Cloudflare API Shield, Envoy Gateway.

---

## API Documentation & Developer Experience

### OpenAPI Specification (OAS 3.1)
Utiliser OpenAPI 3.1 (aligné avec JSON Schema 2020-12) pour documenter les APIs REST :
- Documenter chaque endpoint, paramètre, schéma de requête/réponse et code d'erreur.
- Inclure des exemples concrets pour chaque opération.
- Générer la documentation interactive avec Scalar, Stoplight, ou Redoc.
- Valider le spec automatiquement dans la CI (Spectral).

### AsyncAPI
Utiliser AsyncAPI pour documenter les APIs event-driven :
- Décrire les channels (topics/queues), les messages et les schémas.
- Documenter les protocoles (Kafka, AMQP, WebSocket, MQTT).
- Générer la documentation et le code client/serveur.

### Developer Portal
Pour les APIs publiques ou les plateformes internes, mettre en place un developer portal incluant :
- Documentation interactive (try-it-out).
- Guides de démarrage rapide (Getting Started en < 5 minutes).
- SDK et exemples de code dans les langages principaux.
- Changelog et migration guides.
- Status page et métriques de performance de l'API.

---

## Modern API Patterns 2024-2026

### API Mesh / API Composition
Composer des APIs provenant de multiples sources via un mesh layer :
- **GraphQL Federation** : composer des sous-graphes en un supergraph.
- **API Gateway composition** : agréger les réponses de multiples services en une seule réponse.
- **BFF (Backend for Frontend)** : couche de composition dédiée par type de client.

### AI-Friendly APIs
Concevoir des APIs consommables par les agents IA :
- Fournir des descriptions sémantiques riches (descriptions détaillées dans OpenAPI).
- Supporter les tool-use formats (function calling, MCP — Model Context Protocol).
- Implémenter les APIs comme des "outils" découvrables par les LLMs.
- Documenter les side effects et les pré-conditions de manière explicite.

### Idempotency Keys
Pour les APIs de mutation, supporter les clés d'idempotence pour permettre les retries sûrs :

```
POST /orders
Idempotency-Key: unique-client-generated-uuid
```

Stocker la clé et le résultat pendant 24-48h. Retourner le même résultat si la même clé est rejouée. Indispensable pour les opérations financières et les APIs à haute fiabilité.
