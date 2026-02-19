# Performance GraphQL — DataLoader, Cache et Sécurité

La performance d'une API GraphQL repose sur trois axes distincts : l'élimination du problème N+1 au niveau des resolvers, la mise en cache intelligente des réponses, et la protection contre les requêtes abusives. Ignorer ces axes conduit inévitablement à une API qui dégrade la base de données sous charge et expose des vecteurs d'attaque critiques.

---

## Le Problème N+1 — Anatomie Complète

### Exemple concret : users → orders → products

Considérons cette query apparemment simple :

```graphql
query {
  users(first: 20) {
    edges {
      node {
        id
        email
        orders(first: 5) {
          edges {
            node {
              id
              total
              items {
                product {
                  id
                  name
                  price
                }
              }
            }
          }
        }
      }
    }
  }
}
```

Sans optimisation, cette query génère :
- **1** requête pour charger 20 utilisateurs
- **20** requêtes pour charger les orders de chaque utilisateur
- **100** requêtes (20 × 5) pour charger les items de chaque order
- **500** requêtes (100 × 5 items) pour charger chaque produit

**Total : 621 requêtes DB** pour 20 utilisateurs. Avec DataLoader correctement implémenté : **4 requêtes**.

### Pourquoi GraphQL amplifie le problème

Contrairement à REST où le développeur contrôle le SQL, GraphQL délègue la résolution à des fonctions indépendantes. Chaque resolver ignore ce que font ses voisins, ce qui rend le batching impossible sans mécanisme dédié.

---

## DataLoader — Implémentation en Profondeur

### Principe fondamental

DataLoader collecte les appels pendant le tick JavaScript courant (micro-queue), puis exécute une seule requête batch. La clé est l'**ordering garanti** : le tableau retourné par la batch function DOIT correspondre exactement à l'ordre du tableau d'entrée `keys`.

```typescript
import DataLoader from "dataloader";
import { PrismaClient, User } from "@prisma/client";

// CRITIQUE : la batch function DOIT retourner les résultats dans le même
// ordre que les keys reçues. Un résultat null pour une clé manquante.
function createUserLoader(prisma: PrismaClient) {
  return new DataLoader<string, User | null>(async (ids) => {
    const users = await prisma.user.findMany({
      where: { id: { in: [...ids] } },
    });

    // Construire une Map pour la recherche O(1)
    const userMap = new Map(users.map((user) => [user.id, user]));

    // OBLIGATOIRE : retourner dans l'ordre exact des ids reçus
    return ids.map((id) => userMap.get(id) ?? null);
  });
}
```

### DataLoader dans le context — Un par requête GraphQL

**Erreur critique commune :** créer le DataLoader au niveau module (global). Cela partage le cache entre toutes les requêtes GraphQL, causant des fuites de données entre utilisateurs.

```typescript
// server.ts — Apollo Server avec contexte
import { ApolloServer } from "@apollo/server";

const server = new ApolloServer({
  typeDefs,
  resolvers,
  // contextFunction est appelée à chaque requête HTTP
  // Chaque requête obtient ses propres DataLoaders (cache isolé)
});

export interface Context {
  prisma: PrismaClient;
  userId: string | null;
  loaders: {
    user: DataLoader<string, User | null>;
    ordersByUserId: DataLoader<string, Order[]>;
    productsByOrderId: DataLoader<string, Product[]>;
  };
}

// Express middleware
app.use("/graphql", expressMiddleware(server, {
  context: async ({ req }): Promise<Context> => ({
    prisma,
    userId: extractUserId(req),
    loaders: {
      // Nouveau DataLoader par requête = cache isolé + batch par requête
      user: createUserLoader(prisma),
      ordersByUserId: createOrdersByUserIdLoader(prisma),
      productsByOrderId: createProductsByOrderIdLoader(prisma),
    },
  }),
}));
```

### DataLoader pour relations Many-to-Many — Pattern groupBy

Les relations one-to-many (un utilisateur → plusieurs orders) nécessitent un pattern différent : retourner un tableau pour chaque parent.

```typescript
function createOrdersByUserIdLoader(prisma: PrismaClient) {
  return new DataLoader<string, Order[]>(async (userIds) => {
    const orders = await prisma.order.findMany({
      where: { userId: { in: [...userIds] } },
      orderBy: { createdAt: "desc" },
    });

    // Grouper par userId : Map<userId, Order[]>
    const ordersByUserId = new Map<string, Order[]>();

    // Initialiser chaque clé avec un tableau vide (CRITIQUE pour l'ordering)
    userIds.forEach((id) => ordersByUserId.set(id, []));

    // Remplir les groupes
    orders.forEach((order) => {
      const group = ordersByUserId.get(order.userId)!;
      group.push(order);
    });

    // Retourner dans l'ordre des userIds reçus
    return userIds.map((id) => ordersByUserId.get(id) ?? []);
  });
}
```

```typescript
// Resolver utilisant le DataLoader
const resolvers = {
  User: {
    orders: async (user, args, ctx) => {
      const orders = await ctx.loaders.ordersByUserId.load(user.id);
      return {
        edges: orders.slice(0, args.first ?? 10).map((order) => ({
          node: order,
          cursor: Buffer.from(order.id).toString("base64"),
        })),
        pageInfo: {
          hasNextPage: orders.length > (args.first ?? 10),
          hasPreviousPage: false,
        },
      };
    },
  },
};
```

### DataLoader avec Prisma — Optimisation des queries imbriquées

```typescript
// Anti-pattern : query Prisma imbriquée dans un resolver (N+1 avec Prisma)
const resolvers_BAD = {
  User: {
    orders: async (user, _, ctx) => {
      // PROBLÈME : appelé N fois, génère N queries
      return ctx.prisma.order.findMany({
        where: { userId: user.id },
        include: { items: { include: { product: true } } },
      });
    },
  },
};

// Pattern correct : DataLoader avec findMany + groupBy
function createOrdersWithItemsLoader(prisma: PrismaClient) {
  return new DataLoader<string, (Order & { items: (OrderItem & { product: Product })[] })[]>(
    async (userIds) => {
      // UNE SEULE requête pour tous les utilisateurs
      const orders = await prisma.order.findMany({
        where: { userId: { in: [...userIds] } },
        include: {
          items: {
            include: { product: true },
          },
        },
      });

      const grouped = new Map(userIds.map((id) => [id, [] as typeof orders]));
      orders.forEach((order) => grouped.get(order.userId)?.push(order));
      return userIds.map((id) => grouped.get(id) ?? []);
    }
  );
}
```

### clear() et prime() — Gestion manuelle du cache

```typescript
// prime() : pré-charger le cache avec des données déjà chargées
const user = await prisma.user.findUnique({ where: { id } });
if (user) {
  ctx.loaders.user.prime(user.id, user); // évite un futur DataLoader.load()
}

// clear() : invalider après mutation
await prisma.user.update({ where: { id }, data: { email: newEmail } });
ctx.loaders.user.clear(id); // forcer un rechargement à la prochaine demande

// clearAll() : vider tout le cache (rare, utile après bulk operations)
ctx.loaders.user.clearAll();
```

---

## Query Complexity

La complexité permet de rejeter les requêtes trop lourdes avant exécution.

```typescript
import { createComplexityRule } from "graphql-query-complexity";
import { simpleEstimator, fieldExtensionsEstimator } from "graphql-query-complexity";

const complexityRule = createComplexityRule({
  maximumComplexity: 1000,
  variables: {},
  onComplete: (complexity) => {
    console.log("Query complexity:", complexity);
  },
  estimators: [
    // Utiliser les extensions de champ pour les coûts personnalisés
    fieldExtensionsEstimator(),
    // Fallback : scalaire = 1, objet = 1, liste multiplie par le count
    simpleEstimator({ defaultComplexity: 1 }),
  ],
});

// Dans Apollo Server
const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [complexityRule],
});
```

```graphql
# Annoter les champs coûteux dans le schéma (avec @pothos ou extensions)
type Query {
  # Complexité : 10 + (first ?? 10) * complexité_User
  users(first: Int): UserConnection!
  # Complexité fixe de 100 (opération lourde)
  exportUsersCsv: String!
}
```

**Règle pratique :** commencer avec un maximum de 1000, monitorer en production, ajuster. Les queries de production complexes se situent généralement entre 50 et 300.

---

## Depth Limiting

Limite la profondeur d'imbrication pour prévenir les requêtes récursives ou les attaques par déni de service.

```typescript
import depthLimit from "graphql-depth-limit";

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(10), // Maximum 10 niveaux d'imbrication
  ],
});
```

```graphql
# Cette requête serait rejetée avec depth limit de 5
{
  users {
    edges {
      node {               # niveau 3
        orders {
          edges {
            node {         # niveau 6 — REJETÉE
              items { product { category { parent { name } } } }
            }
          }
        }
      }
    }
  }
}
```

**Recommandation :** 7–12 niveaux couvrent 99% des cas d'usage légitimes. Combiner avec la query complexity pour une protection complète.

---

## Persisted Queries (APQ)

Les Automatic Persisted Queries réduisent la bande passante et permettent la mise en cache CDN des requêtes GET.

### Fonctionnement

1. Client calcule le hash SHA256 de la query
2. Envoie uniquement le hash (première tentative)
3. Si le serveur ne connaît pas le hash : retourne `PERSISTED_QUERY_NOT_FOUND`
4. Client renvoie hash + query complète
5. Serveur stocke l'association hash → query
6. Requêtes suivantes : hash uniquement (GET request CDN-cacheable)

```typescript
// Côté client — Apollo Client
import { ApolloClient, createHttpLink, InMemoryCache } from "@apollo/client";
import { createPersistedQueryLink } from "@apollo/client/link/persisted-queries";
import { sha256 } from "crypto-hash";

const persistedQueriesLink = createPersistedQueryLink({
  sha256,
  useGETForHashedQueries: true, // Active les GET requests pour CDN cache
});

const client = new ApolloClient({
  link: persistedQueriesLink.concat(
    createHttpLink({ uri: "https://api.example.com/graphql" })
  ),
  cache: new InMemoryCache(),
});
```

```typescript
// Côté serveur — Apollo Server avec cache Redis
import { ApolloServer } from "@apollo/server";
import { KeyValueCache } from "@apollo/utils.keyvaluecache";
import RedisCache from "@apollo/server-plugin-redis";

const server = new ApolloServer({
  typeDefs,
  resolvers,
  cache: new RedisCache({
    host: process.env.REDIS_HOST,
    port: 6379,
  }),
  plugins: [ApolloServerPluginCacheControl({ defaultMaxAge: 300 })],
});
```

**Sécurité renforcée :** en production, combiner APQ avec une allow-list des queries connues (seules les queries hashées connues sont acceptées, rejet des queries ad-hoc).

---

## Response Caching

### @cacheControl Directive

```graphql
type Query {
  # Public, cacheable 5 minutes
  products(first: Int): ProductConnection! @cacheControl(maxAge: 300, scope: PUBLIC)
  # Privé par utilisateur, 60 secondes
  myProfile: User! @cacheControl(maxAge: 60, scope: PRIVATE)
  # Jamais caché
  currentTime: DateTime! @cacheControl(maxAge: 0)
}

type Product {
  id: ID!
  name: String!
  price: Float! @cacheControl(maxAge: 60) # Override au niveau du champ
}
```

```typescript
// Apollo Server — Configuration du cache
import { InMemoryLRUCache } from "@apollo/utils.keyvaluecache";
import responseCachePlugin from "@apollo/server-plugin-response-cache";

const server = new ApolloServer({
  typeDefs,
  resolvers,
  cache: new InMemoryLRUCache({
    maxSize: Math.pow(2, 20) * 100, // 100 MB
    ttl: 300, // 5 minutes par défaut
  }),
  plugins: [
    responseCachePlugin({
      // Clé de cache personnalisée par utilisateur pour scope PRIVATE
      generateCacheKey: async (requestContext) => {
        const userId = requestContext.contextValue.userId;
        return userId ? `user:${userId}:${requestContext.request.http?.url}` : null;
      },
    }),
  ],
});
```

### CDN Cache avec APQ

Avec APQ activé et `useGETForHashedQueries: true`, les requêtes publiques deviennent des GET requests cacheable par Cloudflare, Fastly ou CloudFront. Configurer le TTL CDN en accord avec `maxAge`.

---

## Query Batching Côté Client

```typescript
import { ApolloClient, InMemoryCache } from "@apollo/client";
import { BatchHttpLink } from "@apollo/client/link/batch-http";

const client = new ApolloClient({
  // BatchHttpLink regroupe les queries émises dans le même tick
  link: new BatchHttpLink({
    uri: "/graphql",
    batchMax: 10,    // Maximum 10 queries par batch
    batchInterval: 20, // Attendre 20ms pour collecter les queries
  }),
  cache: new InMemoryCache(),
});
```

Apollo Client déduplique également automatiquement les queries identiques en cours d'exécution (`fetchPolicy: "cache-first"` par défaut).

---

## Tracing et Monitoring

### OpenTelemetry pour GraphQL

```typescript
import { ApolloServer } from "@apollo/server";
import { ApolloOpenTelemetry } from "apollo-opentelemetry";
import { NodeTracerProvider } from "@opentelemetry/node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http";

const provider = new NodeTracerProvider();
provider.addSpanProcessor(
  new SimpleSpanProcessor(new OTLPTraceExporter({ url: process.env.OTEL_ENDPOINT }))
);
provider.register();

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    // Trace chaque resolver comme un span OpenTelemetry
    ApolloOpenTelemetry({
      includeDocument: true,
      includeVariables: true,
      includeResult: false, // Ne pas tracer les résultats (données sensibles)
    }),
  ],
});
```

### Plugin custom pour slow query detection

```typescript
const slowQueryPlugin = {
  requestDidStart: async () => ({
    executionDidStart: async () => ({
      willResolveField: ({ info }) => {
        const start = Date.now();
        return () => {
          const duration = Date.now() - start;
          if (duration > 100) {
            // Alerte si un resolver prend plus de 100ms
            console.warn(`Slow resolver: ${info.parentType.name}.${info.fieldName} — ${duration}ms`);
          }
        };
      },
    }),
    willSendResponse: async ({ request, response }) => {
      const duration = Date.now() - (request.http?.headers?.get("x-start-time") as unknown as number ?? 0);
      if (duration > 500) {
        console.error(`Slow GraphQL query: ${duration}ms`, {
          operationName: request.operationName,
          query: request.query?.substring(0, 200),
        });
      }
    },
  }),
};
```

---

## Introspection en Production

L'introspection expose la totalité du schéma — types, champs, descriptions — à quiconque peut exécuter une requête. En production, la désactiver ou la restreindre.

```typescript
import { ApolloServer } from "@apollo/server";
import {
  ApolloServerPluginInlineTraceDisabled,
  ApolloServerPluginLandingPageDisabled,
} from "@apollo/server/plugin/disabled";

const isProduction = process.env.NODE_ENV === "production";

const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: !isProduction, // Désactivé en production
  plugins: [
    ...(isProduction
      ? [
          ApolloServerPluginLandingPageDisabled(), // Désactive GraphQL Playground
          ApolloServerPluginInlineTraceDisabled(),
        ]
      : []),
  ],
});
```

**Alternative :** activer l'introspection uniquement pour les IPs du réseau interne ou pour les tokens d'API internes (pour les équipes de développement). Ne jamais exposer publiquement en production sans contrôle d'accès.

---

## Récapitulatif — Checklist Performance

| Optimisation | Impact | Effort | Priorité |
|---|---|---|---|
| DataLoader pour chaque relation | Élimine N+1 | Moyen | Critique |
| DataLoader créé dans le context | Isolation du cache | Faible | Critique |
| Query complexity limit | Protection DDoS | Faible | Haute |
| Depth limit | Protection DDoS | Très faible | Haute |
| Désactiver introspection en prod | Sécurité | Très faible | Haute |
| APQ + GET requests | Cache CDN | Moyen | Moyenne |
| @cacheControl sur les queries publiques | Cache réponse | Faible | Moyenne |
| Tracing OpenTelemetry | Observabilité | Moyen | Moyenne |
| Query batching client | Réseau | Faible | Basse |
