# API Development Reference

> Reference detaillee pour le developpement d'API. Couvre le design REST, GraphQL, gRPC, WebSockets, Server-Sent Events, le rate limiting, la documentation OpenAPI/Swagger, et les patterns de pagination, filtrage et gestion d'erreurs.

---

## REST API Design

### Resource Naming Conventions

Appliquer ces regles de nommage systematiquement pour garantir la coherence de l'API :

```
# Utiliser des noms pluriels pour les collections
GET    /api/v1/users              # lister les utilisateurs
POST   /api/v1/users              # creer un utilisateur
GET    /api/v1/users/:id          # obtenir un utilisateur
PATCH  /api/v1/users/:id          # mettre a jour partiellement
PUT    /api/v1/users/:id          # remplacer completement
DELETE /api/v1/users/:id          # supprimer

# Relations imbriquees (max 2 niveaux)
GET    /api/v1/users/:id/orders              # commandes d'un utilisateur
GET    /api/v1/users/:id/orders/:orderId     # une commande specifique
POST   /api/v1/users/:id/orders              # creer une commande

# EVITER l'imbrication profonde (> 2 niveaux)
# NON : /api/v1/users/:id/orders/:orderId/items/:itemId/reviews
# OUI : /api/v1/order-items/:itemId/reviews

# Actions non-CRUD : utiliser des verbes en sous-ressource
POST   /api/v1/orders/:id/cancel             # annuler une commande
POST   /api/v1/users/:id/verify-email        # action specifique
POST   /api/v1/reports/generate              # generer un rapport

# Cas kebab pour les ressources multi-mots
GET    /api/v1/order-items                   # OUI
GET    /api/v1/orderItems                    # NON
GET    /api/v1/order_items                   # NON
```

### HTTP Methods & Status Codes

#### Methodes HTTP

| Methode | Semantique | Idempotent | Corps requete | Corps reponse |
|---------|-----------|------------|---------------|---------------|
| `GET` | Lire | Oui | Non | Oui |
| `POST` | Creer | Non | Oui | Oui |
| `PUT` | Remplacer entierement | Oui | Oui | Oui |
| `PATCH` | Modifier partiellement | Non* | Oui | Oui |
| `DELETE` | Supprimer | Oui | Non (optionnel) | Optionnel |

*PATCH peut etre rendu idempotent avec des operations JSON Merge Patch.

#### Status Codes essentiels

```
2xx - Succes
  200 OK                 # GET, PUT, PATCH reussis
  201 Created            # POST reussi (avec header Location)
  204 No Content         # DELETE reussi (pas de corps)

3xx - Redirection
  301 Moved Permanently  # Ressource deplacee definitivement
  304 Not Modified       # Cache valide (ETag/If-None-Match)

4xx - Erreur client
  400 Bad Request        # Validation echouee, body malformed
  401 Unauthorized       # Non authentifie (manque de token)
  403 Forbidden          # Authentifie mais non autorise
  404 Not Found          # Ressource inexistante
  409 Conflict           # Conflit (doublon, version conflict)
  422 Unprocessable Entity  # Validation metier echouee
  429 Too Many Requests  # Rate limit depasse

5xx - Erreur serveur
  500 Internal Server Error  # Erreur non prevue
  502 Bad Gateway           # Service upstream defaillant
  503 Service Unavailable   # Maintenance ou surcharge
  504 Gateway Timeout       # Timeout upstream
```

### API Versioning

Privilegier le versioning par URL prefix pour la clarte et la facilite de routage :

```
# Recommande : prefix URL
GET /api/v1/users
GET /api/v2/users

# Acceptable : header custom
GET /api/users
Header: X-API-Version: 2

# Acceptable : content negotiation
GET /api/users
Header: Accept: application/vnd.myapp.v2+json
```

Strategie de deprecation :
1. Annoncer la deprecation via un header `Deprecation` et `Sunset` (RFC 8594)
2. Maintenir la version N-1 pendant au minimum 6 mois apres la sortie de N
3. Logger les appels aux versions deprecees pour suivre l'adoption
4. Retourner le header `Sunset: Sat, 01 Mar 2025 00:00:00 GMT` sur les endpoints depreces

### Error Handling

Adopter un format d'erreur standard et coherent sur toute l'API :

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
        "message": "Must be between 0 and 150."
      }
    ],
    "request_id": "req_abc123xyz",
    "documentation_url": "https://api.example.com/docs/errors#VALIDATION_ERROR"
  }
}
```

Implementation avec Zod (TypeScript) :

```typescript
import { z } from 'zod';

// Schema de validation
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  role: z.enum(['admin', 'member', 'viewer']).default('member'),
});

// Middleware de validation (Express/Hono)
function validate<T extends z.ZodSchema>(schema: T) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(422).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid request body.',
          details: result.error.issues.map(issue => ({
            field: issue.path.join('.'),
            code: issue.code,
            message: issue.message,
          })),
          request_id: req.id,
        },
      });
    }
    req.validated = result.data;
    next();
  };
}
```

### Pagination

#### Cursor-based Pagination (recommandee)

Utiliser la pagination par curseur pour les datasets volumineux. Plus performante et stable que l'offset.

```typescript
// Endpoint
// GET /api/v1/orders?limit=20&cursor=eyJpZCI6MTAwfQ==

// Implementation
async function listOrders(cursor?: string, limit: number = 20) {
  const decodedCursor = cursor
    ? JSON.parse(Buffer.from(cursor, 'base64url').toString())
    : null;

  const orders = await db
    .select()
    .from(ordersTable)
    .where(decodedCursor ? gt(ordersTable.id, decodedCursor.id) : undefined)
    .orderBy(asc(ordersTable.id))
    .limit(limit + 1); // +1 pour detecter s'il y a une page suivante

  const hasMore = orders.length > limit;
  const data = hasMore ? orders.slice(0, -1) : orders;
  const nextCursor = hasMore
    ? Buffer.from(JSON.stringify({ id: data[data.length - 1].id })).toString('base64url')
    : null;

  return {
    data,
    pagination: {
      has_more: hasMore,
      next_cursor: nextCursor,
    },
  };
}
```

Reponse :

```json
{
  "data": [...],
  "pagination": {
    "has_more": true,
    "next_cursor": "eyJpZCI6MTIwfQ"
  }
}
```

#### Offset-based Pagination (cas simples)

Acceptable pour les petits datasets (< 10 000 lignes) ou quand l'utilisateur a besoin de naviguer a une page specifique.

```json
{
  "data": [...],
  "pagination": {
    "page": 3,
    "per_page": 20,
    "total_count": 1542,
    "total_pages": 78
  }
}
```

### Filtering & Sorting

```
# Filtrage par champs
GET /api/v1/orders?status=pending&customer_id=42

# Filtrage avec operateurs (convention LHS brackets)
GET /api/v1/orders?created_at[gte]=2024-01-01&created_at[lt]=2024-07-01
GET /api/v1/products?price[lte]=100&category[in]=electronics,books

# Tri
GET /api/v1/orders?sort=-created_at,+total_amount
# - prefix = DESC, + prefix (ou pas de prefix) = ASC

# Selection de champs (sparse fieldsets)
GET /api/v1/users?fields=id,name,email

# Recherche
GET /api/v1/products?search=wireless+headphones
```

Implementation type-safe du filtrage avec Drizzle :

```typescript
import { and, eq, gte, lte, inArray, like, desc, asc } from 'drizzle-orm';

type FilterOperator = 'eq' | 'gte' | 'lte' | 'gt' | 'lt' | 'in' | 'like';

function buildFilters(table: any, params: Record<string, any>) {
  const conditions = [];

  for (const [key, value] of Object.entries(params)) {
    const match = key.match(/^(\w+)\[(\w+)\]$/);
    if (match) {
      const [, field, op] = match;
      const column = table[field];
      if (!column) continue;

      switch (op as FilterOperator) {
        case 'gte': conditions.push(gte(column, value)); break;
        case 'lte': conditions.push(lte(column, value)); break;
        case 'in': conditions.push(inArray(column, value.split(','))); break;
        case 'like': conditions.push(like(column, `%${value}%`)); break;
        default: conditions.push(eq(column, value));
      }
    } else if (table[key]) {
      conditions.push(eq(table[key], value));
    }
  }

  return conditions.length > 0 ? and(...conditions) : undefined;
}
```

### Rate Limiting

Implementer le rate limiting a plusieurs niveaux :

```
# Headers de rate limiting standards (draft IETF)
RateLimit-Limit: 100
RateLimit-Remaining: 95
RateLimit-Reset: 1625478000

# Reponse 429 Too Many Requests
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please retry after 30 seconds.",
    "retry_after": 30
  }
}
```

Implementation avec Redis (algorithme sliding window) :

```typescript
import { Redis } from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

interface RateLimitConfig {
  windowMs: number;   // fenetre en millisecondes
  maxRequests: number; // nombre max de requetes par fenetre
}

async function checkRateLimit(
  key: string,
  config: RateLimitConfig
): Promise<{ allowed: boolean; remaining: number; resetAt: number }> {
  const now = Date.now();
  const windowStart = now - config.windowMs;

  const pipeline = redis.pipeline();
  // Supprimer les entrees hors fenetre
  pipeline.zremrangebyscore(key, 0, windowStart);
  // Ajouter la requete courante
  pipeline.zadd(key, now.toString(), `${now}-${Math.random()}`);
  // Compter les requetes dans la fenetre
  pipeline.zcard(key);
  // Definir l'expiration
  pipeline.pexpire(key, config.windowMs);

  const results = await pipeline.exec();
  const requestCount = results![2][1] as number;

  return {
    allowed: requestCount <= config.maxRequests,
    remaining: Math.max(0, config.maxRequests - requestCount),
    resetAt: now + config.windowMs,
  };
}
```

Strategies de rate limiting par tier :

| Tier | Limite | Fenetre | Identification |
|------|--------|---------|---------------|
| Non authentifie | 60 req | 1 minute | IP |
| Authentifie (free) | 1 000 req | 1 heure | API key / user ID |
| Authentifie (pro) | 10 000 req | 1 heure | API key / user ID |
| Webhook/service | 100 000 req | 1 heure | Service account |

## GraphQL

### Schema Design

Concevoir le schema GraphQL comme un contrat d'API, pas comme un miroir de la base de donnees. Penser en termes de graphe de domaine.

```graphql
# schema.graphql
type Query {
  """Obtenir un utilisateur par son ID"""
  user(id: ID!): User
  """Lister les utilisateurs avec filtres et pagination"""
  users(filter: UserFilter, first: Int = 20, after: String): UserConnection!
  """Rechercher des produits"""
  searchProducts(query: String!, first: Int = 20): ProductSearchResult!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!
}

type Subscription {
  """Ecouter les nouvelles commandes en temps reel"""
  orderCreated(userId: ID): Order!
}

# Pagination Relay-style
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Input types
input CreateUserInput {
  email: String!
  name: String!
  role: UserRole = MEMBER
}

# Payload types (toujours wrapper le resultat)
type CreateUserPayload {
  user: User
  errors: [UserError!]
}

type UserError {
  field: String
  code: String!
  message: String!
}

# Filtres
input UserFilter {
  status: UserStatus
  role: UserRole
  search: String
  createdAfter: DateTime
}

enum UserRole { ADMIN MEMBER VIEWER }
enum UserStatus { ACTIVE INACTIVE SUSPENDED }
```

### DataLoader Pattern

Utiliser DataLoader pour resoudre le probleme N+1 dans les resolvers GraphQL. DataLoader batch et deduplique les requetes au sein d'un tick d'execution.

```typescript
import DataLoader from 'dataloader';

// Creer les DataLoaders par requete (pas globaux)
function createLoaders(db: Database) {
  return {
    userById: new DataLoader<string, User>(async (ids) => {
      const users = await db
        .select()
        .from(usersTable)
        .where(inArray(usersTable.id, [...ids]));
      // IMPORTANT : retourner dans le meme ordre que les ids d'entree
      const userMap = new Map(users.map(u => [u.id, u]));
      return ids.map(id => userMap.get(id) ?? new Error(`User ${id} not found`));
    }),

    ordersByUserId: new DataLoader<string, Order[]>(async (userIds) => {
      const orders = await db
        .select()
        .from(ordersTable)
        .where(inArray(ordersTable.userId, [...userIds]));
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

// Resolvers
const resolvers = {
  User: {
    orders: (parent: User, _args: any, ctx: Context) =>
      ctx.loaders.ordersByUserId.load(parent.id),
  },
  Order: {
    customer: (parent: Order, _args: any, ctx: Context) =>
      ctx.loaders.userById.load(parent.customerId),
  },
};
```

### Query Complexity & Depth Limiting

Proteger le serveur GraphQL contre les requetes abusives :

```typescript
import { createComplexityLimitRule } from 'graphql-validation-complexity';
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  schema,
  validationRules: [
    depthLimit(7), // profondeur max de 7 niveaux
    createComplexityLimitRule(1000, {
      // chaque champ scalar = 1, chaque connexion = 10
      scalarCost: 1,
      objectCost: 2,
      listFactor: 10,
    }),
  ],
});
```

### GraphQL Federation (Microservices)

Utiliser Apollo Federation pour composer un supergraph a partir de sous-graphes independants :

```graphql
# Sous-graphe Users
type User @key(fields: "id") {
  id: ID!
  name: String!
  email: String!
}

# Sous-graphe Orders (reference User du sous-graphe Users)
type Order @key(fields: "id") {
  id: ID!
  total: Float!
  customer: User!
}

extend type User @key(fields: "id") {
  id: ID! @external
  orders: [Order!]!
}
```

## gRPC

Utiliser gRPC pour la communication inter-services haute performance (serialisation binaire Protobuf, streaming bidirectionnel, generation de code type-safe).

```protobuf
// order_service.proto
syntax = "proto3";
package orderservice;

service OrderService {
  // Unary RPC
  rpc GetOrder(GetOrderRequest) returns (Order);
  // Server streaming
  rpc WatchOrderStatus(WatchOrderRequest) returns (stream OrderStatusUpdate);
  // Client streaming
  rpc BatchCreateOrders(stream CreateOrderRequest) returns (BatchCreateResponse);
}

message Order {
  string id = 1;
  string customer_id = 2;
  repeated OrderItem items = 3;
  OrderStatus status = 4;
  google.protobuf.Timestamp created_at = 5;
}

enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_PENDING = 1;
  ORDER_STATUS_CONFIRMED = 2;
  ORDER_STATUS_SHIPPED = 3;
  ORDER_STATUS_DELIVERED = 4;
  ORDER_STATUS_CANCELLED = 5;
}
```

Quand utiliser gRPC vs REST :
- **gRPC** : communication inter-services, latence critique, streaming, generation de clients type-safe
- **REST** : API publiques, navigateur (sans proxy gRPC-web), ecosysteme existant, simplicite

## WebSockets & Server-Sent Events

### WebSockets

Utiliser pour la communication bidirectionnelle temps reel (chat, jeux, collaboration).

```typescript
// Serveur WebSocket avec heartbeat
import { WebSocketServer } from 'ws';

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (ws) => {
  ws.isAlive = true;

  ws.on('pong', () => { ws.isAlive = true; });

  ws.on('message', (data) => {
    const message = JSON.parse(data.toString());
    // Router par type de message
    switch (message.type) {
      case 'subscribe':
        subscribeToChannel(ws, message.channel);
        break;
      case 'message':
        broadcastToChannel(message.channel, message.payload);
        break;
    }
  });
});

// Heartbeat toutes les 30 secondes
setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!ws.isAlive) return ws.terminate();
    ws.isAlive = false;
    ws.ping();
  });
}, 30_000);
```

### Server-Sent Events (SSE)

Utiliser pour le streaming unidirectionnel serveur vers client (notifications, progress, AI streaming).

```typescript
// Endpoint SSE (compatible avec tous les navigateurs modernes)
app.get('/api/v1/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Envoyer un heartbeat toutes les 15 secondes
  const heartbeat = setInterval(() => {
    res.write(':heartbeat\n\n');
  }, 15_000);

  // Envoyer des events
  function sendEvent(event: string, data: any, id?: string) {
    if (id) res.write(`id: ${id}\n`);
    res.write(`event: ${event}\n`);
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  }

  // Ecouter les changements
  const unsubscribe = eventBus.subscribe((event) => {
    sendEvent(event.type, event.payload, event.id);
  });

  req.on('close', () => {
    clearInterval(heartbeat);
    unsubscribe();
  });
});

// Cote client
const eventSource = new EventSource('/api/v1/events');
eventSource.addEventListener('order_updated', (event) => {
  const data = JSON.parse(event.data);
  console.log('Order updated:', data);
});
```

### Quand utiliser quoi

| Technologie | Direction | Reconnexion auto | Use cases |
|-------------|-----------|-------------------|-----------|
| **WebSocket** | Bidirectionnel | Non (a implementer) | Chat, jeux, collaboration |
| **SSE** | Serveur -> Client | Oui (native) | Notifications, streaming AI, dashboards |
| **Long Polling** | Simule bidirectionnel | Oui (par design) | Fallback, compatibilite anciens systemes |
| **Supabase Realtime** | Bidirectionnel | Oui | Apps Supabase, broadcast, presence |

## OpenAPI / Swagger Documentation

Generer la documentation automatiquement depuis le code ou le schema :

```yaml
# openapi.yaml (extrait)
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
  description: API de gestion des commandes

paths:
  /api/v1/orders:
    get:
      summary: Lister les commandes
      operationId: listOrders
      tags: [Orders]
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, confirmed, shipped, delivered, cancelled]
        - name: cursor
          in: query
          schema:
            type: string
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Liste paginee des commandes
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderListResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/TooManyRequests'

components:
  schemas:
    Order:
      type: object
      required: [id, status, total_amount, created_at]
      properties:
        id:
          type: string
          format: uuid
        status:
          type: string
          enum: [pending, confirmed, shipped, delivered, cancelled]
        total_amount:
          type: number
          format: decimal
        created_at:
          type: string
          format: date-time
```

Outils recommandes pour la generation automatique :

| Outil | Ecosysteme | Approche |
|-------|-----------|----------|
| **Hono + Zod OpenAPI** | TypeScript (Hono) | Code-first, generation depuis les schemas Zod |
| **tRPC + trpc-openapi** | TypeScript (tRPC) | Code-first, export OpenAPI depuis les procedures |
| **FastAPI** | Python | Code-first, generation automatique depuis les type hints |
| **Scalar** | Universel | UI de documentation moderne (remplacant Swagger UI) |
| **Redocly** | Universel | Documentation et linting de specs OpenAPI |

## API Security Checklist

Appliquer ces verifications sur chaque API en production :

1. Authentifier chaque requete (JWT, API key, session) sauf les endpoints publics explicites
2. Valider et sanitizer tous les inputs (Zod, Valibot, class-validator)
3. Implementer le rate limiting par tier d'utilisateur
4. Utiliser HTTPS exclusivement (rediriger HTTP vers HTTPS)
5. Configurer les headers CORS restrictifs (pas de wildcard en production)
6. Ne jamais exposer les IDs internes ou les stack traces dans les erreurs
7. Logger chaque requete avec un request_id pour la tracabilite
8. Implementer l'idempotency key pour les mutations critiques (paiements)
9. Definir des timeouts explicites sur toutes les operations externes
10. Mettre en place un WAF (Web Application Firewall) devant l'API publique
