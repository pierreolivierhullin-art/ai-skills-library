# GraphQL & gRPC — Schema Design, Performance, Subscriptions, Streaming, Migration

## Overview

Ce document de référence couvre GraphQL et gRPC en profondeur : conception de schémas, optimisation des performances, subscriptions temps réel, streaming bidirectionnel, sécurité, et stratégies de migration entre paradigmes. Appliquer ces patterns pour choisir le bon protocole et l'implémenter de manière robuste.

---

## GraphQL Schema Design

### Schema-First vs Code-First

Deux approches pour définir un schéma GraphQL. Choisir en fonction de l'équipe et du workflow :

| Critère | Schema-First | Code-First |
|---|---|---|
| **Définition** | Écrire le `.graphql` manuellement | Générer le schéma depuis le code |
| **Outils** | Apollo Server, GraphQL Yoga | Nexus, Pothos (TypeScript), Strawberry (Python) |
| **Collaboration** | Frontend et backend reviewent le schéma ensemble | Le schéma est un artefact dérivé du code |
| **Typage** | Nécessite un codegen séparé (graphql-codegen) | Types TypeScript/Python générés nativement |
| **Validation** | Linting du schéma (graphql-eslint) | Validation au compile-time |
| **Recommandation** | Équipes multi-langages, API publiques | Équipes full-stack TypeScript, itération rapide |

### Conventions de nommage

Appliquer ces conventions systématiquement sur tout le schéma :

```
Types et interfaces :
+-- PascalCase : User, OrderItem, ShippingAddress
+-- Suffixer les connexions : UserConnection, OrderConnection
+-- Suffixer les edges : UserEdge, OrderEdge
+-- Suffixer les payloads : CreateOrderPayload, DeleteUserPayload

Champs :
+-- camelCase : createdAt, totalAmount, shippingAddress
+-- Booléens en is/has/can : isActive, hasPermission, canEdit

Enums :
+-- SCREAMING_SNAKE_CASE : ORDER_PENDING, PAYMENT_CONFIRMED
+-- Toujours inclure une valeur UNKNOWN ou UNSPECIFIED en premier

Mutations :
+-- verbe + nom : createOrder, cancelOrder, updateShippingAddress
+-- Input type dédié : CreateOrderInput, CancelOrderInput
+-- Payload type dédié : CreateOrderPayload, CancelOrderPayload

Queries :
+-- Singulier pour un élément : user(id: ID!): User
+-- Pluriel pour les listes : users(...): UserConnection!
```

### Nullability Rules

Définir la nullabilité avec intention. Chaque choix de `!` (non-null) est un engagement contractuel :

| Contexte | Règle | Exemple |
|---|---|---|
| **Query par ID** | Retour nullable (le 404 est normal) | `user(id: ID!): User` |
| **Listes** | Toujours non-null, contenu non-null | `users: [User!]!` |
| **Connexions** | Toujours non-null | `orders(...): OrderConnection!` |
| **Champs requis** | Non-null | `name: String!` |
| **Champs optionnels** | Nullable | `middleName: String` |
| **Mutations input** | Champs requis non-null | `email: String!` dans `CreateUserInput` |
| **Mutation payload** | Résultat nullable, errors non-null | `user: User`, `errors: [UserError!]!` |

### Interface et Union Types

Utiliser les interfaces pour les types partageant des champs communs et les unions pour les types sans champs communs :

```graphql
# Interface : champs communs + champs spécifiques
interface Node {
  id: ID!
}

interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}

type User implements Node & Timestamped {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  name: String!
  email: String!
}

type Order implements Node & Timestamped {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  total: Money!
  status: OrderStatus!
}

# Union : types distincts sans champs communs
union SearchResult = User | Order | Product | Article

type Query {
  node(id: ID!): Node
  search(query: String!): [SearchResult!]!
}
```

### Input Types — Bonnes pratiques

```graphql
# Toujours un Input type dédié par mutation
input CreateOrderInput {
  customerId: ID!
  items: [OrderItemInput!]!
  shippingAddress: AddressInput!
  note: String               # Champ optionnel
  idempotencyKey: String!     # Pour les retries sûrs
}

input OrderItemInput {
  productId: ID!
  quantity: Int!
  unitPrice: Money           # Optionnel si le serveur calcule
}

# Séparer les inputs de création et de mise à jour
input UpdateOrderInput {
  shippingAddress: AddressInput  # Tous les champs optionnels
  note: String
}

# Payload unifié avec gestion d'erreur métier
type CreateOrderPayload {
  order: Order                   # Null en cas d'erreur
  errors: [UserError!]!          # Vide en cas de succès
}

type UserError {
  field: [String!]               # Chemin vers le champ en erreur
  message: String!               # Message lisible
  code: ErrorCode!               # Code machine-readable
}

enum ErrorCode {
  VALIDATION_ERROR
  NOT_FOUND
  INSUFFICIENT_STOCK
  PAYMENT_DECLINED
  UNAUTHORIZED
}
```

---

## GraphQL Performance

### Le problème N+1 et DataLoader

Le problème N+1 est le piège de performance le plus courant en GraphQL. Sans DataLoader, une query listant 50 users avec leurs orders génère 1 + 50 requêtes SQL.

```typescript
import DataLoader from 'dataloader';

// Créer les loaders par requête (request-scoped)
function createLoaders(db: Database) {
  return {
    userById: new DataLoader<string, User>(async (ids) => {
      // UNE seule requête SQL : SELECT * FROM users WHERE id IN (...)
      const users = await db.query(
        'SELECT * FROM users WHERE id = ANY($1)',
        [ids]
      );
      const map = new Map(users.map(u => [u.id, u]));
      // Retourner dans l'ordre exact des IDs demandés
      return ids.map(id => map.get(id) ?? new Error(`User ${id} not found`));
    }),

    ordersByUserId: new DataLoader<string, Order[]>(async (userIds) => {
      const orders = await db.query(
        'SELECT * FROM orders WHERE user_id = ANY($1)',
        [userIds]
      );
      const grouped = new Map<string, Order[]>();
      for (const order of orders) {
        const list = grouped.get(order.userId) ?? [];
        list.push(order);
        grouped.set(order.userId, list);
      }
      return userIds.map(id => grouped.get(id) ?? []);
    }),
  };
}
```

Règles critiques pour DataLoader :
- Créer un nouveau DataLoader **par requête HTTP**, jamais global (sinon le cache ne se purge pas).
- Retourner les résultats **dans le même ordre** que les clés en entrée.
- Retourner une `Error` pour les éléments introuvables, pas `null` (permet la détection d'erreurs).
- Utiliser `.prime()` pour pré-peupler le cache après une mutation.

### Query Complexity Analysis

Attribuer un coût à chaque champ pour prévenir les requêtes abusives :

```typescript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

// Matrice de coûts
const complexityConfig = {
  scalarCost: 1,       // Chaque champ scalaire = 1 point
  objectCost: 2,       // Chaque objet imbriqué = 2 points
  listFactor: 10,      // Multiplicateur pour les listes
};

// Budget total par requête
const MAX_COMPLEXITY = 1000;

// Exemple de calcul :
// query { users(first: 50) { edges { node { name orders { totalCount } } } } }
// = 1 (users) + 50 * (1 (edges) + 2 (node) + 1 (name) + 2 (orders) + 1 (totalCount))
// = 1 + 50 * 7 = 351 points — autorisé
```

### Depth Limiting

Limiter la profondeur de nesting pour empêcher les requêtes récursives :

```typescript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  schema,
  validationRules: [
    depthLimit(7),  // Maximum 7 niveaux de profondeur
  ],
});

// Requête rejetée (profondeur > 7) :
// query { user { orders { items { product { category { parent { parent { name } } } } } } } }
```

### Persisted Queries

En production, accepter uniquement les requêtes pré-enregistrées pour éliminer les requêtes arbitraires :

```
Workflow des persisted queries :
+-- Développement : le client envoie la requête complète
+-- Build : extraction des requêtes dans un manifeste (hash → query)
+-- Production : le client envoie uniquement le hash
+-- Serveur : lookup du hash, exécute la requête correspondante
+-- Bénéfices : sécurité (pas de requête arbitraire), performance (payload réduit),
    caching facilité (clé de cache = hash)
```

### Response Caching et Batching

| Stratégie | Mécanisme | Gain typique | Complexité |
|---|---|---|---|
| **DataLoader** | Batching + cache per-request | Élimine N+1 | Faible |
| **Response caching** | Cache la réponse GraphQL entière | 10-100x latence | Moyenne |
| **Partial caching** | Cache par type/champ (cache hints) | 2-10x latence | Élevée |
| **CDN caching** | GET persisted queries + CDN | 100x+ latence | Moyenne |
| **Query batching** | Envoyer plusieurs queries en un seul HTTP POST | Réduit les round-trips | Faible |
| **Automatic batching** | @defer / @stream directives | Progressive loading | Moyenne |

---

## GraphQL Security

### Query Depth Limiting

Configurer une profondeur maximale de 7-10 niveaux. Au-delà, les requêtes sont presque toujours abusives ou mal conçues :

```
Profondeur recommandée par contexte :
+-- API publique : max 5-7 niveaux (surface d'attaque exposée)
+-- API interne : max 7-10 niveaux (consommateurs contrôlés)
+-- API avec persisted queries : illimité (requêtes pré-approuvées)
```

### Complexity Budget

Implémenter un budget de complexité avec des coûts personnalisés par champ :

```graphql
# Directives de coût dans le schéma
type Query {
  users(first: Int = 20): UserConnection! @cost(complexity: 10, multiplier: "first")
  expensiveReport: Report! @cost(complexity: 500)
}

type User {
  name: String!         # coût implicite : 1
  orders: [Order!]!     # coût implicite : 10 (liste)
  analytics: UserAnalytics! @cost(complexity: 50)  # coût élevé
}
```

| Tier | Budget de complexité | Depth max | Rate limit |
|---|---|---|---|
| Public (non authentifié) | 100 | 5 | 10 req/min |
| Free tier | 500 | 7 | 60 req/min |
| Pro tier | 2 000 | 10 | 300 req/min |
| Internal service | 10 000 | 15 | 1 000 req/min |

### Introspection Control

Désactiver l'introspection en production pour les APIs publiques. L'introspection expose la totalité du schéma :

```typescript
const server = new ApolloServer({
  schema,
  introspection: process.env.NODE_ENV !== 'production',
  // Ou : autoriser uniquement pour les requêtes internes
  introspection: (req) => req.headers['x-internal-token'] === INTERNAL_TOKEN,
});
```

### Authentication in Resolvers

Implémenter l'authentification au niveau du contexte GraphQL, pas dans chaque resolver :

```typescript
// Middleware d'authentification dans le contexte
const server = new ApolloServer({
  schema,
  context: async ({ req }) => {
    const token = req.headers.authorization?.replace('Bearer ', '');
    const user = token ? await verifyToken(token) : null;
    return {
      user,
      loaders: createLoaders(db),
    };
  },
});
```

### Field-Level Authorization

Appliquer l'autorisation au niveau du champ pour un contrôle granulaire :

```typescript
// Directive @auth dans le schéma
const typeDefs = gql`
  directive @auth(requires: Role!) on FIELD_DEFINITION

  type User {
    id: ID!
    name: String!
    email: String! @auth(requires: OWNER)
    salary: Float! @auth(requires: ADMIN)
    internalNotes: String @auth(requires: ADMIN)
  }
`;

// Implémentation du transformer de directive
function authDirective(directiveName: string) {
  return {
    authDirectiveTransformer: (schema: GraphQLSchema) =>
      mapSchema(schema, {
        [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
          const authDirective = getDirective(schema, fieldConfig, directiveName);
          if (authDirective) {
            const requiredRole = authDirective[0].requires;
            const originalResolve = fieldConfig.resolve ?? defaultFieldResolver;
            fieldConfig.resolve = (source, args, context, info) => {
              if (!context.user) throw new AuthenticationError('Non authentifié');
              if (!context.user.roles.includes(requiredRole)) {
                throw new ForbiddenError('Accès refusé');
              }
              return originalResolve(source, args, context, info);
            };
          }
          return fieldConfig;
        },
      }),
  };
}
```

### Rate Limiting per Query Complexity

Ne pas appliquer un rate limiting uniforme par requête. Pondérer par complexité :

```typescript
// Une query simple (coût 5) consomme 5 unités du budget
// Une query complexe (coût 500) consomme 500 unités du budget
// Budget : 10 000 unités par minute

async function rateLimitByComplexity(
  complexity: number,
  userId: string,
  windowMs: number = 60_000,
  budget: number = 10_000
): Promise<{ allowed: boolean; remaining: number }> {
  const key = `gql:rate:${userId}`;
  const current = await redis.incrby(key, complexity);
  if (current === complexity) await redis.pexpire(key, windowMs);
  return {
    allowed: current <= budget,
    remaining: Math.max(0, budget - current),
  };
}
```

---

## GraphQL Subscriptions

### WebSocket Transport

Les subscriptions GraphQL utilisent le protocole WebSocket pour la communication temps réel. Deux protocoles disponibles :

| Protocole | Package | Statut | Recommandation |
|---|---|---|---|
| `graphql-ws` | `graphql-ws` | Actif, maintenu | Recommandé (2024-2026) |
| `subscriptions-transport-ws` | `subscriptions-transport-ws` | Déprécié | Ne plus utiliser |

```typescript
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';

const httpServer = createServer(app);
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
});

useServer(
  {
    schema,
    context: async (ctx) => {
      // Authentifier lors du handshake WebSocket
      const token = ctx.connectionParams?.authToken;
      const user = await verifyToken(token as string);
      if (!user) throw new Error('Non authentifié');
      return { user, loaders: createLoaders(db) };
    },
    onSubscribe: (_ctx, msg) => {
      // Valider la complexité de la subscription
      const complexity = calculateComplexity(schema, msg.payload.query);
      if (complexity > MAX_SUBSCRIPTION_COMPLEXITY) {
        return [new GraphQLError('Subscription trop complexe')];
      }
    },
  },
  wsServer
);
```

### Event-Driven Architecture pour les Subscriptions

Connecter les subscriptions à un système de pub/sub pour découpler la publication des événements de leur distribution :

```
Architecture de subscription scalable :
+-- Service métier publie un événement → Redis Pub/Sub ou Kafka
+-- Tous les serveurs GraphQL reçoivent l'événement
+-- Chaque serveur filtre et pousse vers les clients WebSocket concernés
+-- Bénéfice : scaling horizontal des serveurs GraphQL
```

```typescript
import { RedisPubSub } from 'graphql-redis-subscriptions';
import Redis from 'ioredis';

const pubsub = new RedisPubSub({
  publisher: new Redis(REDIS_URL),
  subscriber: new Redis(REDIS_URL),
});

// Côté mutation : publier l'événement
const resolvers = {
  Mutation: {
    updateOrderStatus: async (_, { id, status }, ctx) => {
      const order = await db.updateOrderStatus(id, status);
      await pubsub.publish(`ORDER_STATUS_${id}`, { orderStatusChanged: order });
      return { order, errors: [] };
    },
  },
  Subscription: {
    orderStatusChanged: {
      subscribe: (_, { orderId }) =>
        pubsub.asyncIterator(`ORDER_STATUS_${orderId}`),
    },
  },
};
```

### Scaling Subscriptions

| Stratégie | Mécanisme | Capacité | Complexité |
|---|---|---|---|
| **Single server** | In-memory pub/sub | ~10K connexions | Faible |
| **Redis Pub/Sub** | Tous les serveurs reçoivent tous les messages | ~100K connexions | Moyenne |
| **Redis Streams** | Partitionnement + consumer groups | ~500K connexions | Élevée |
| **Kafka** | Partitionnement par topic | ~1M+ connexions | Élevée |

### Subscription Filtering

Filtrer les événements côté serveur pour ne pousser que les données pertinentes :

```typescript
import { withFilter } from 'graphql-subscriptions';

const resolvers = {
  Subscription: {
    orderStatusChanged: {
      subscribe: withFilter(
        () => pubsub.asyncIterator('ORDER_UPDATES'),
        (payload, variables, context) => {
          // Filtrer par orderId ET par permissions utilisateur
          return (
            payload.orderStatusChanged.id === variables.orderId &&
            payload.orderStatusChanged.customerId === context.user.id
          );
        }
      ),
    },
  },
};
```

### Real-Time Patterns

```
Patterns de temps réel avec GraphQL :
+-- Notifications : subscription globale filtrée par userId
+-- Live queries : polling intelligent avec ETag (pas une vraie subscription)
+-- Collaborative editing : subscriptions + CRDT pour la résolution de conflits
+-- Dashboards : subscriptions avec throttling (max 1 update/seconde)
+-- Chat : subscription par room/channel avec pagination des messages historiques
```

---

## gRPC Fundamentals

### Protocol Buffers (Protobuf)

Protocol Buffers est le format de sérialisation de gRPC. Binaire, compact, versionné et générant du code type-safe dans 10+ langages.

```protobuf
syntax = "proto3";

package ecommerce.order.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/wrappers.proto";

// Convention : un message Request et Response par RPC
service OrderService {
  rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc ListOrders(ListOrdersRequest) returns (ListOrdersResponse);
  rpc WatchOrders(WatchOrdersRequest) returns (stream OrderEvent);
}

message Order {
  string id = 1;
  string customer_id = 2;
  repeated OrderItem items = 3;
  OrderStatus status = 4;
  int64 total_amount_cents = 5;      // Monétaire en centimes (pas de float)
  string currency = 6;               // ISO 4217
  google.protobuf.Timestamp created_at = 7;
  google.protobuf.Timestamp updated_at = 8;

  reserved 9, 10;                    // Champs supprimés — ne jamais réutiliser
  reserved "deprecated_notes";
}

// Toujours commencer les enums par UNSPECIFIED = 0
enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_PENDING = 1;
  ORDER_STATUS_CONFIRMED = 2;
  ORDER_STATUS_SHIPPED = 3;
  ORDER_STATUS_DELIVERED = 4;
  ORDER_STATUS_CANCELLED = 5;
}

message ListOrdersRequest {
  int32 page_size = 1;             // Max 100
  string page_token = 2;           // Cursor opaque
  string filter = 3;               // Expression de filtrage (CEL)
  string order_by = 4;             // "created_at desc"
}

message ListOrdersResponse {
  repeated Order orders = 1;
  string next_page_token = 2;
  int32 total_size = 3;
}
```

Règles d'évolution des Protocol Buffers :

```
Safe (backward + forward compatible) :
+-- Ajouter un champ optionnel avec un nouveau numéro
+-- Ajouter une valeur d'enum (sauf la valeur 0)
+-- Ajouter un RPC à un service
+-- Renommer un champ (le numéro compte, pas le nom)

Breaking (interdit sans nouvelle version) :
+-- Réutiliser un numéro de champ supprimé
+-- Changer le type d'un champ
+-- Changer le numéro d'un champ
+-- Supprimer un champ sans 'reserved'
+-- Changer la valeur 0 d'un enum
```

### 4 Communication Patterns

```protobuf
service OrderService {
  // 1. Unary — requête/réponse simple
  rpc GetOrder(GetOrderRequest) returns (Order);

  // 2. Server streaming — le serveur envoie un flux
  rpc WatchOrderStatus(WatchOrderRequest) returns (stream OrderEvent);

  // 3. Client streaming — le client envoie un flux
  rpc BatchCreateOrders(stream CreateOrderRequest) returns (BatchCreateResponse);

  // 4. Bidirectional streaming — flux dans les deux sens
  rpc OrderChat(stream ChatMessage) returns (stream ChatMessage);
}
```

| Pattern | Direction | Cas d'usage | Analogie HTTP |
|---|---|---|---|
| **Unary** | Client → Serveur → Client | CRUD, lookup | GET / POST |
| **Server streaming** | Client → Serveur →→→ Client | Live feeds, exports | SSE |
| **Client streaming** | Client →→→ Serveur → Client | Upload, batch insert | Chunked upload |
| **Bidirectional** | Client ↔ Serveur | Chat, collaboration | WebSocket |

---

## gRPC Advanced

### Interceptors (Middleware)

Les interceptors gRPC sont l'équivalent des middleware HTTP. Chaîner les interceptors pour l'authentification, le logging, le tracing et le rate limiting :

```typescript
// Interceptor d'authentification (Node.js / @grpc/grpc-js)
function authInterceptor(
  call: grpc.ServerUnaryCall<any, any>,
  callback: grpc.sendUnaryData<any>,
  next: Function
) {
  const metadata = call.metadata.get('authorization');
  const token = metadata[0]?.toString().replace('Bearer ', '');
  if (!token) {
    return callback({
      code: grpc.status.UNAUTHENTICATED,
      message: 'Token manquant',
    });
  }
  try {
    const user = verifyToken(token);
    call.user = user;  // Attacher au contexte
    next();
  } catch {
    callback({
      code: grpc.status.UNAUTHENTICATED,
      message: 'Token invalide',
    });
  }
}
```

### Error Handling

gRPC utilise des codes de statut spécifiques, différents des codes HTTP :

| gRPC Code | HTTP Equivalent | Utilisation |
|---|---|---|
| `OK` (0) | 200 | Succès |
| `CANCELLED` (1) | 499 | Client a annulé |
| `INVALID_ARGUMENT` (3) | 400 | Validation échouée |
| `NOT_FOUND` (5) | 404 | Ressource introuvable |
| `ALREADY_EXISTS` (6) | 409 | Doublon |
| `PERMISSION_DENIED` (7) | 403 | Non autorisé |
| `UNAUTHENTICATED` (16) | 401 | Non authentifié |
| `RESOURCE_EXHAUSTED` (8) | 429 | Rate limit dépassé |
| `INTERNAL` (13) | 500 | Erreur serveur |
| `UNAVAILABLE` (14) | 503 | Service indisponible |
| `DEADLINE_EXCEEDED` (4) | 504 | Timeout |

Enrichir les erreurs avec des détails structurés (google.rpc.Status) :

```typescript
import { status, Metadata } from '@grpc/grpc-js';

function throwGrpcError(code: number, message: string, details?: Record<string, any>) {
  const metadata = new Metadata();
  if (details) {
    metadata.set('error-details-bin', Buffer.from(JSON.stringify(details)));
  }
  const error = {
    code,
    message,
    metadata,
  };
  throw error;
}

// Utilisation
throwGrpcError(status.INVALID_ARGUMENT, 'Quantité invalide', {
  field: 'quantity',
  constraint: 'Doit être entre 1 et 1000',
  provided: -5,
});
```

### Deadlines et Timeouts

Toujours définir un deadline côté client. Sans deadline, un appel peut bloquer indéfiniment :

```typescript
// Client avec deadline de 5 secondes
const deadline = new Date();
deadline.setSeconds(deadline.getSeconds() + 5);

client.getOrder({ id: 'ORD-123' }, { deadline }, (err, response) => {
  if (err?.code === grpc.status.DEADLINE_EXCEEDED) {
    console.error('Appel gRPC timeout après 5 secondes');
  }
});

// Propager le deadline entre services (deadline propagation)
// Le service B hérite du deadline restant du service A
```

### Health Checking et Load Balancing

```protobuf
// Standard gRPC Health Checking Protocol (grpc.health.v1)
service Health {
  rpc Check(HealthCheckRequest) returns (HealthCheckResponse);
  rpc Watch(HealthCheckRequest) returns (stream HealthCheckResponse);
}
```

Stratégies de load balancing :

| Stratégie | Mécanisme | Avantages | Inconvénients |
|---|---|---|---|
| **Proxy LB** (L7) | Envoy, Nginx, Traefik | Simple, centralisé | SPOF potentiel, latence ajoutée |
| **Client-side LB** | Le client résout et choisit | Pas de SPOF, faible latence | Complexité client, service discovery requis |
| **Look-aside LB** | Service dédié (xDS, Lookaside) | Flexible, policies avancées | Composant supplémentaire |

### gRPC-Web et Connect Protocol

```
Exposition de gRPC aux clients web :
+-- gRPC-Web (Envoy proxy)
    +-- Traduit HTTP/1.1 ou HTTP/2 vers gRPC natif
    +-- Supporte : unary, server streaming
    +-- Ne supporte PAS : client streaming, bidirectional
    +-- Nécessite un proxy (Envoy, grpc-web proxy)

+-- Connect Protocol (Buf) — RECOMMANDÉ 2024-2026
    +-- Protocole compatible gRPC natif en HTTP/1.1 et HTTP/2
    +-- Trois formats : gRPC, gRPC-Web, Connect (JSON natif)
    +-- Supporte : unary, server streaming, client streaming, bidirectional (HTTP/2)
    +-- Pas besoin de proxy — fonctionne avec fetch() standard
    +-- curl-friendly : requêtes lisibles en JSON
    +-- Outils : connectrpc.com, buf.build
```

---

## Performance Comparison

### REST vs GraphQL vs gRPC — Benchmark

Mesures sur un scénario e-commerce typique (liste de 50 produits avec détails, catégorie et reviews) :

| Métrique | REST (JSON) | GraphQL (JSON) | gRPC (Protobuf) |
|---|---|---|---|
| **Payload size** | 45 KB | 28 KB (query sélective) | 12 KB (binaire) |
| **Latency (p50)** | 35 ms | 40 ms | 15 ms |
| **Latency (p99)** | 120 ms | 150 ms | 45 ms |
| **Throughput** | 8 000 req/s | 5 500 req/s | 25 000 req/s |
| **CPU usage** | Bas | Moyen (parsing query) | Bas |
| **Sérialisation** | ~2 ms | ~3 ms | ~0.3 ms |
| **Désérialisation** | ~2 ms | ~3 ms | ~0.5 ms |

### When Each Wins

```
gRPC gagne quand :
+-- Communication inter-services à haute fréquence
+-- Latence critique (< 20 ms requis)
+-- Bande passante limitée (payload binaire compact)
+-- Streaming requis (bidirectionnel)
+-- Environnement polyglot (code generation multi-langages)

GraphQL gagne quand :
+-- Clients avec besoins de données variables (mobile vs desktop)
+-- Over-fetching significatif avec REST
+-- Besoin de composition de données multi-sources
+-- Itération rapide frontend sans changer le backend
+-- Subscriptions temps réel natives

REST gagne quand :
+-- API publique grand public (standard universel)
+-- Caching HTTP critique (CDN, ETags natifs)
+-- Simplicité requise (courbe d'apprentissage faible)
+-- Écosystème existant (outils, monitoring, documentation)
+-- Requêtes prévisibles et uniformes
```

### Real-World Measurements

| Entreprise | Paradigme | Résultat mesurable |
|---|---|---|
| **Netflix** | GraphQL Federation | Réduction de 40% des requêtes réseau, latence p99 de 200ms à 80ms |
| **Uber** | gRPC inter-services | Réduction de 60% de la taille des payloads vs JSON REST |
| **Shopify** | GraphQL public API | 70% moins de data transférée vs REST equivalent |
| **Google** | gRPC (microservices) | Latence inter-services < 5ms en datacenter |
| **GitHub** | GraphQL v4 API | 10x moins de requêtes pour les mêmes opérations vs REST v3 |

---

## Migration Strategies

### REST to GraphQL — BFF Pattern

Migrer progressivement en plaçant GraphQL comme Backend-For-Frontend devant les APIs REST existantes :

```
Architecture de migration REST → GraphQL :

Phase 1 — GraphQL comme proxy
+-- Client SPA/Mobile → GraphQL Server (BFF)
+-- GraphQL Server → APIs REST existantes (inchangées)
+-- Bénéfice : le frontend profite de GraphQL sans toucher au backend

Phase 2 — Migration incrémentale des resolvers
+-- Resolver par resolver, remplacer les appels REST par des accès directs à la base
+-- Les APIs REST restent en place pour les autres consommateurs
+-- Monitoring : comparer les performances REST vs accès direct

Phase 3 — Décommission progressive
+-- Quand tous les consommateurs utilisent GraphQL : sunset des endpoints REST
+-- Maintenir les endpoints critiques avec une politique de dépréciation
```

### REST to gRPC — Services internes

```
Migration progressive REST → gRPC pour les services internes :

Phase 1 — Dual protocol
+-- Ajouter les définitions .proto à côté des routes REST
+-- Le même service expose REST et gRPC simultanément
+-- Outils : grpc-gateway (Go), Connect (multi-langages)

Phase 2 — Migration des clients internes
+-- Service par service, migrer les clients vers gRPC
+-- Prioriser les chemins critiques en termes de latence
+-- Garder REST pour les API publiques et les intégrations legacy

Phase 3 — REST sunset interne
+-- Retirer les endpoints REST internes quand tous les clients sont migrés
+-- Maintenir REST uniquement pour les APIs publiques
```

### GraphQL Federation

Composer un supergraph à partir de sous-graphes indépendants, chaque service possédant son domaine :

```graphql
# Sous-graphe Users (service Users)
type User @key(fields: "id") {
  id: ID!
  name: String!
  email: String!
}

# Sous-graphe Orders (service Orders)
type Order @key(fields: "id") {
  id: ID!
  total: Money!
  status: OrderStatus!
  customer: User!      # Référence vers le sous-graphe Users
}

# Extension dans le sous-graphe Orders
extend type User @key(fields: "id") {
  id: ID! @external
  orders: [Order!]!    # Ajout du champ orders sur User
}
```

```
Architecture Apollo Federation v2 :
+-- Apollo Router (ou Gateway)
    +-- Compose les sous-graphes en un supergraph
    +-- Query planning : détermine quels sous-graphes interroger
    +-- Exécution parallèle des sous-requêtes

+-- Sous-graphe A (Users service)
    +-- Possède : User, UserProfile
    +-- Expose : @key(fields: "id") sur User

+-- Sous-graphe B (Orders service)
    +-- Possède : Order, OrderItem
    +-- Référence : User via @key

+-- Sous-graphe C (Products service)
    +-- Possède : Product, Category
    +-- Contribue : recommendations sur User (@requires)
```

### Schema Stitching vs Federation

| Critère | Schema Stitching | Federation |
|---|---|---|
| **Définition** | Merge de schémas au niveau du gateway | Composition déclarative avec directives |
| **Ownership** | Gateway connaît tous les schémas | Chaque service déclare ses entités |
| **Autonomie** | Faible (le gateway orchestre) | Forte (chaque service est indépendant) |
| **Évolution** | Risque de conflits au merge | Composition validée au build |
| **Tooling** | graphql-tools, Mesh | Apollo Federation, Cosmo |
| **Recommandation** | Legacy, cas spécifiques | Standard pour les nouvelles architectures |

---

## State of the Art (2025-2026)

### GraphQL Federation v2

Apollo Federation v2 apporte des améliorations majeures :
- **@shareable** : plusieurs sous-graphes peuvent résoudre le même champ sans conflit.
- **@override** : migrer progressivement la résolution d'un champ d'un sous-graphe à un autre.
- **@inaccessible** : masquer des champs internes du schéma public.
- **@composeDirective** : propager des directives custom à travers la composition.
- **Apollo Router** (Rust) : remplace Apollo Gateway (Node.js) pour des performances 10x supérieures.
- **Cosmo Router** (Go) : alternative open-source à Apollo Router, compatible Federation v2.

### gRPC + Connect Protocol

Le Connect Protocol (Buf) unifie gRPC, gRPC-Web et REST-like JSON en un seul protocole :
- Appels gRPC natifs depuis le navigateur sans proxy.
- Format JSON lisible pour le debugging (curl-friendly).
- Bibliothèques client/serveur en Go, TypeScript, Swift, Kotlin.
- Rétrocompatible avec les services gRPC existants.
- Buf CLI : linting protobuf, breaking change detection, code generation unifiée.

### tRPC et APIs Type-Safe

tRPC élimine la couche de sérialisation entre le client et le serveur TypeScript :
- Zéro code generation : les types TypeScript sont partagés directement.
- Validation avec Zod intégrée dans les procédures.
- React Query / TanStack Query intégrés pour le caching client.
- Adapters : Next.js, Express, Fastify, Hono, AWS Lambda.
- Limitation : réservé aux architectures full-stack TypeScript (pas polyglot).

### GraphQL over HTTP Spec

La spécification GraphQL over HTTP se stabilise (2025) :
- Standardise GET pour les queries (cacheable par CDN).
- Standardise POST pour les mutations et queries complexes.
- Définit les content types : `application/graphql-response+json`.
- Spécifie le multipart pour `@defer` et `@stream` (incremental delivery).
- Adopté par Apollo, Yoga, Grafbase et la majorité des implémentations.

### Relay-Style Patterns

Les patterns Relay deviennent la norme de facto pour les schémas GraphQL matures :
- **Node interface** : `node(id: ID!): Node` pour le fetching universel par ID global.
- **Connection pattern** : pagination cursor-based avec `edges`, `pageInfo`, `totalCount`.
- **Global IDs** : identifiants opaques encodant le type et l'ID (`base64("User:123")`).
- **@defer / @stream** : chargement progressif des données sans requêtes supplémentaires.
- **Relay Compiler** : validation des fragments au build, optimisation automatique des requêtes.

### Tendances émergentes

| Tendance | Description | Maturité |
|---|---|---|
| **WunderGraph Cosmo** | Plateforme open-source de GraphQL Federation | Production-ready |
| **Grafbase** | GraphQL edge-native avec résolution au edge | GA 2025 |
| **Tailcall** | Runtime GraphQL hautes performances en Rust | Émergent |
| **gRPC + xDS** | Configuration dynamique des services gRPC via xDS (Envoy) | Stable |
| **GraphQL Mesh** | Unification de sources hétérogènes (REST, gRPC, SQL) en un seul GraphQL | Stable |
| **Streaming APIs** | @defer/@stream GraphQL, Server-Sent Events, WebTransport | En adoption |
