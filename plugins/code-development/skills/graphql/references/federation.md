# Apollo Federation v2 — Architecture Distribuée

Apollo Federation permet de composer plusieurs APIs GraphQL indépendantes en un supergraph unifié. Chaque équipe owne son subgraph, déploie indépendamment, et l'Apollo Router assemble les réponses de manière transparente pour le client. Ce guide couvre l'architecture complète de Federation v2, des directives fondamentales aux patterns de migration.

---

## Architecture Federation — Vue d'Ensemble

```
                        ┌─────────────────────────────────┐
Client GraphQL ────────▶│       Apollo Router              │
                        │  (Supergraph Query Planner)      │
                        └──────────┬──────────┬────────────┘
                                   │          │
                     ┌─────────────┘          └──────────────┐
                     ▼                                        ▼
            ┌────────────────┐                    ┌────────────────────┐
            │ Subgraph Users │                    │ Subgraph Products  │
            │  (Node.js)     │                    │  (Go / Python)     │
            └────────┬───────┘                    └─────────┬──────────┘
                     │                                      │
            ┌────────▼───────┐                    ┌─────────▼──────────┐
            │   PostgreSQL   │                    │     PostgreSQL      │
            └────────────────┘                    └────────────────────┘
```

- **Subgraph :** API GraphQL autonome avec son propre schéma et sa propre base de données.
- **Supergraph :** schéma unifié composé par la CLI `rover` à partir de tous les subgraphs.
- **Apollo Router :** reverse proxy qui planifie et exécute les query plans distribués. Plus performant que l'ancien `@apollo/gateway` (Rust, multithreaded).

---

## Directives Federation v2 Fondamentales

### @key — Entités et Clés d'Identification

La directive `@key` déclare qu'un type est une **entité** — un objet avec une identité globale qui peut être référencé et étendu par d'autres subgraphs.

```graphql
# Subgraph Users
type User @key(fields: "id") {
  id: ID!
  email: String!
  name: String!
  createdAt: DateTime!
}
```

```graphql
# Clé composée (plusieurs champs identifient l'entité)
type Product @key(fields: "sku variantId") {
  sku: String!
  variantId: String!
  name: String!
  price: Float!
}
```

```typescript
// Resolver __resolveReference : appelé quand un autre subgraph demande cette entité
const resolvers = {
  User: {
    __resolveReference: async (reference: { id: string }, ctx) => {
      // reference contient uniquement les champs de la @key
      return ctx.loaders.user.load(reference.id);
    },
  },
};
```

### @key avec resolvable: false

Déclarer qu'un type d'un autre subgraph est référencé sans avoir besoin de le résoudre localement.

```graphql
# Subgraph Orders — référence User sans le résoudre
type User @key(fields: "id", resolvable: false) {
  id: ID!
}

type Order {
  id: ID!
  user: User!    # Le Router récupère les détails de User depuis le subgraph Users
  total: Float!
  items: [OrderItem!]!
}
```

### @external et @requires — Accès aux Champs d'Autres Subgraphs

`@external` marque un champ défini dans un autre subgraph. `@requires` déclare qu'un champ local a besoin de champs externes pour être résolu.

```graphql
# Subgraph Shipping
type User @key(fields: "id") {
  id: ID!
  # Champ défini dans le subgraph Users, requis pour le calcul de livraison
  address: String! @external
  # Ce champ nécessite 'address' (défini ailleurs) pour être calculé
  shippingOptions: [ShippingOption!]! @requires(fields: "address")
}
```

```typescript
const resolvers = {
  User: {
    shippingOptions: async (user: { id: string; address: string }, _, ctx) => {
      // 'address' est disponible car @requires garantit que le Router le pré-charge
      return ctx.shippingService.getOptions(user.address);
    },
    __resolveReference: async (ref: { id: string }, ctx) => {
      return { id: ref.id };
    },
  },
};
```

### @provides — Optimisation des Query Plans

`@provides` indique au Router que ce subgraph peut fournir certains champs d'une entité liée, évitant un aller-retour supplémentaire.

```graphql
# Subgraph Orders — peut fournir name des Products directement
type Order {
  id: ID!
  items: [OrderItem!]! @provides(fields: "product { name }")
}

type OrderItem {
  quantity: Int!
  product: Product!
}

type Product @key(fields: "id", resolvable: false) {
  id: ID!
  name: String! @external
}
```

---

## @shareable — Types Partagés

Par défaut, un type dans Federation v2 appartient à un seul subgraph (ownership exclusif). `@shareable` permet à plusieurs subgraphs de définir et résoudre le même type.

```graphql
# Subgraph Users
type Location @shareable {
  lat: Float!
  lng: Float!
  address: String!
}

type User {
  id: ID!
  homeLocation: Location
}
```

```graphql
# Subgraph Delivery — peut aussi retourner Location
type Location @shareable {
  lat: Float!
  lng: Float!
  address: String!
}

type DeliveryStop {
  id: ID!
  location: Location!
}
```

**Règle :** utiliser `@shareable` uniquement pour les types valeur (Value Objects) sans ownership sémantique. Les entités avec identité restent `@key` dans un seul subgraph owning.

---

## @inaccessible — Champs Internes

`@inaccessible` masque un champ dans le supergraph tout en le gardant accessible en interne pour les query plans (notamment avec `@requires`).

```graphql
# Subgraph Products
type Product @key(fields: "id") {
  id: ID!
  name: String!
  # ID interne du fournisseur — jamais exposé au client
  internalSupplierId: String! @inaccessible
  price: Float!
}
```

---

## @override — Migration Progressive de Champs

`@override` transfère la résolution d'un champ d'un subgraph à un autre, avec support d'un pourcentage de migration progressif.

```graphql
# Subgraph Users — l'ancien owner de 'preferences'
type User @key(fields: "id") {
  id: ID!
  # @override: ce subgraph prend ownership de 'preferences' depuis 'settings-subgraph'
  preferences: UserPreferences! @override(from: "settings-subgraph")
}
```

```graphql
# Migration progressive avec pourcentage (Federation v2.7+)
type User @key(fields: "id") {
  id: ID!
  # 20% des requêtes résolues par le nouveau subgraph, 80% par l'ancien
  preferences: UserPreferences! @override(from: "settings-subgraph", label: "percent(20)")
}
```

---

## @interfaceObject — Extensions d'Interfaces Cross-Subgraph

Disponible depuis Federation v2.3, `@interfaceObject` permet d'étendre une interface définie dans un autre subgraph.

```graphql
# Subgraph Media — définit l'interface
interface Media @key(fields: "id") {
  id: ID!
  title: String!
  duration: Int!
}

type Video implements Media @key(fields: "id") {
  id: ID!
  title: String!
  duration: Int!
  resolution: String!
}

type Podcast implements Media @key(fields: "id") {
  id: ID!
  title: String!
  duration: Int!
  episodeNumber: Int!
}
```

```graphql
# Subgraph Analytics — ajoute un champ à TOUS les types Media sans les connaître
type Media @interfaceObject @key(fields: "id") {
  id: ID!
  # Ce champ sera disponible sur Video ET Podcast
  viewCount: Int!
  likeCount: Int!
}
```

---

## Composition du Supergraph avec Rover

```bash
# Installer Rover CLI
curl -sSL https://rover.apollo.dev/nix/latest | sh

# rover.yaml — configuration des subgraphs
```

```yaml
# supergraph.yaml
federation_version: =2.5.0

subgraphs:
  users:
    routing_url: http://users-service:4001/graphql
    schema:
      file: ./subgraphs/users/schema.graphql
  products:
    routing_url: http://products-service:4002/graphql
    schema:
      file: ./subgraphs/products/schema.graphql
  orders:
    routing_url: http://orders-service:4003/graphql
    schema:
      file: ./subgraphs/orders/schema.graphql
```

```bash
# Composer le supergraph localement
rover supergraph compose --config supergraph.yaml > supergraph.graphql

# Vérifier les breaking changes contre le schema en production
rover graph check my-graph@production \
  --schema ./subgraphs/users/schema.graphql \
  --name users

# Publier un subgraph sur Apollo Studio
rover subgraph publish my-graph@production \
  --name users \
  --schema ./subgraphs/users/schema.graphql \
  --routing-url https://users.internal.example.com/graphql
```

---

## Apollo Router — Configuration

```yaml
# router.yaml
supergraph:
  path: /graphql
  introspection: false  # Désactivé en production

cors:
  origins:
    - https://app.example.com
  methods:
    - GET
    - POST
  headers:
    - Content-Type
    - Authorization

headers:
  all:
    request:
      # Forwarder le header Authorization à tous les subgraphs
      - propagate:
          named: Authorization
      # Ajouter un header interne d'identification du Router
      - insert:
          name: x-gateway-version
          value: "2.0"

authentication:
  router:
    jwt:
      jwks:
        - url: https://auth.example.com/.well-known/jwks.json

limits:
  max_depth: 12
  max_height: 200
  max_aliases: 30
  max_root_fields: 20

traffic_shaping:
  all:
    timeout: 30s
    rate_limit:
      capacity: 1000
      interval: 1s

telemetry:
  tracing:
    otlp:
      endpoint: http://otel-collector:4317
  metrics:
    otlp:
      endpoint: http://otel-collector:4317
```

### Coprocessors — Logique Custom dans le Router

```yaml
# router.yaml — activer un coprocesseur externe
coprocessor:
  url: http://auth-coprocessor:8080/check
  router:
    request:
      headers: true
      body: false
```

```typescript
// Coprocesseur Express — validation JWT avancée
import express from "express";

const app = express();
app.post("/check", express.json(), async (req, res) => {
  const { headers, stage } = req.body;
  const authHeader = headers?.Authorization ?? headers?.authorization;

  if (!authHeader?.startsWith("Bearer ")) {
    return res.json({ control: "Break", http: { status: 401 } });
  }

  try {
    const payload = await verifyJWT(authHeader.slice(7));
    // Injecter userId dans les headers pour les subgraphs
    return res.json({
      control: "Continue",
      headers: { "x-user-id": payload.sub, "x-user-roles": payload.roles.join(",") },
    });
  } catch {
    return res.json({ control: "Break", http: { status: 403 } });
  }
});
```

---

## Testing des Subgraphs

### Test unitaire avec buildSubgraphSchema

```typescript
import { buildSubgraphSchema } from "@apollo/subgraph";
import { ApolloServer } from "@apollo/server";

// Tester un subgraph isolément
describe("Users subgraph", () => {
  let server: ApolloServer;

  beforeAll(async () => {
    server = new ApolloServer({
      schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
    });
    await server.start();
  });

  it("résout __resolveReference", async () => {
    const response = await server.executeOperation({
      query: `
        query ($representations: [_Any!]!) {
          _entities(representations: $representations) {
            ... on User {
              id
              email
            }
          }
        }
      `,
      variables: {
        representations: [{ __typename: "User", id: "user-1" }],
      },
    });
    expect(response.body.kind).toBe("single");
    const data = (response.body as { singleResult: { data: unknown } }).singleResult.data as { _entities: { id: string; email: string }[] };
    expect(data._entities[0].email).toBe("alice@example.com");
  });
});
```

### Test d'intégration Federation avec `@apollo/federation-integration-test-utils`

```typescript
import { LocalFederatedServer } from "@apollo/server-integration-testing";

// Démarrer un supergraph complet en mémoire pour les tests e2e
const gateway = new LocalFederatedServer({
  subgraphs: [
    { name: "users", url: "http://localhost:4001/graphql" },
    { name: "products", url: "http://localhost:4002/graphql" },
  ],
});
```

---

## Observabilité en Fédération

### Tracing distribué cross-subgraphs

Le Router Apollo propage automatiquement les trace IDs OpenTelemetry vers les subgraphs (via le header `traceparent` W3C). Chaque subgraph crée des spans enfants du span Router.

```typescript
// Subgraph — utiliser le trace ID propagé
import { context, trace } from "@opentelemetry/api";

const resolvers = {
  Query: {
    user: async (_, { id }, ctx) => {
      const span = trace.getActiveSpan();
      span?.setAttribute("user.id", id);
      const user = await ctx.loaders.user.load(id);
      span?.setAttribute("user.found", !!user);
      return user;
    },
  },
};
```

### Métriques par Subgraph

```yaml
# router.yaml — métriques détaillées par subgraph
telemetry:
  metrics:
    common:
      attributes:
        subgraph.request:
          subgraph_name: true
          http.response.status_code: true
    otlp:
      endpoint: http://otel-collector:4317
```

---

## Migration REST → Federation — Step by Step

### Étape 1 : Identifier les entités

Analyser les APIs REST existantes et identifier les entités cross-services (User, Product, Order qui apparaissent dans plusieurs services).

### Étape 2 : Démarrer avec un subgraph unique (strangler fig)

```typescript
// Phase 1 : un seul subgraph qui appelle les APIs REST existantes
import { RESTDataSource } from "@apollo/datasource-rest";

class UserService extends RESTDataSource {
  baseURL = "https://api.legacy.example.com/v2/";

  async getUser(id: string) {
    return this.get(`users/${id}`);
  }
}

// Le Router Federation est en place, mais avec un seul subgraph
// Les équipes peuvent progressivement créer leurs subgraphs indépendants
```

### Étape 3 : Extraire les subgraphs progressivement

```graphql
# Avant : monolithe GraphQL
type Query {
  user(id: ID!): User
  products(first: Int): [Product!]!
  order(id: ID!): Order
}
```

```graphql
# Après : 3 subgraphs indépendants
# subgraph-users/schema.graphql
type User @key(fields: "id") {
  id: ID!
  email: String!
}

type Query {
  user(id: ID!): User
  me: User
}
```

```graphql
# subgraph-orders/schema.graphql
type Order @key(fields: "id") {
  id: ID!
  user: User!
  total: Float!
}

# Référence User depuis le subgraph Users
type User @key(fields: "id", resolvable: false) {
  id: ID!
}

type Query {
  order(id: ID!): Order
  myOrders: [Order!]!
}
```

### CI Pipeline avec Schema Checks

```yaml
# .github/workflows/schema-check.yml
name: GraphQL Schema Check

on: [pull_request]

jobs:
  schema-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Rover
        run: curl -sSL https://rover.apollo.dev/nix/latest | sh
      - name: Check schema
        run: |
          ~/.rover/bin/rover subgraph check my-graph@production \
            --name ${{ env.SUBGRAPH_NAME }} \
            --schema ./schema.graphql \
            --background false
        env:
          APOLLO_KEY: ${{ secrets.APOLLO_KEY }}
          SUBGRAPH_NAME: users
```

---

## Récapitulatif des Directives Federation v2

| Directive | Emplacement | Usage |
|---|---|---|
| `@key(fields: "id")` | Type | Déclare une entité avec sa clé d'identification |
| `@key(resolvable: false)` | Type | Référence une entité d'un autre subgraph sans la résoudre |
| `@external` | Champ | Champ défini dans un autre subgraph |
| `@requires(fields: "x")` | Champ | Nécessite des champs `@external` pour être résolu |
| `@provides(fields: "x")` | Champ | Ce subgraph peut fournir ces champs sans appel externe |
| `@shareable` | Type / Champ | Plusieurs subgraphs peuvent résoudre ce type |
| `@inaccessible` | Type / Champ | Masqué dans le supergraph, utilisable en interne |
| `@override(from: "sg")` | Champ | Reprend l'ownership d'un champ depuis un autre subgraph |
| `@interfaceObject` | Type | Étend une interface depuis un autre subgraph |
| `@composeDirective` | Schema | Importe une directive custom dans la composition |
