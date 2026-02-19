# Design du Schéma GraphQL — SDL et Bonnes Pratiques

Un schéma GraphQL bien conçu est la fondation de toute API durable. Il contractualise l'interface entre le client et le serveur, rend explicites les capacités de l'API, et conditionne directement la performance des resolvers, la maintenabilité du code, et l'expérience développeur. Ce guide couvre les décisions de design critiques, des scalaires custom aux patterns de pagination, en passant par la gouvernance de schéma en équipe.

---

## Schema-first vs Code-first

### Schema-first (SDL natif)

L'approche **schema-first** consiste à écrire le schéma en SDL (Schema Definition Language) directement, puis à implémenter les resolvers qui correspondent à ce contrat.

```graphql
# schema.graphql
type User {
  id: ID!
  email: EmailAddress!
  createdAt: DateTime!
  orders(first: Int, after: String): OrderConnection!
}

type Query {
  user(id: ID!): User
  users(first: Int, after: String, filter: UserFilter): UserConnection!
}
```

**Avantages :** lisibilité maximale, SDL est le standard de l'industrie, facilite la review de schéma par des non-développeurs, outillage mature (`graphql-codegen`, GraphQL Inspector).

**Inconvénients :** synchronisation manuelle entre SDL et les types TypeScript, risque de dérive si la génération n'est pas automatisée en CI.

### Code-first avec Pothos (Type-Safe Schema Builder)

**Pothos** (anciennement GiraphQL) est l'approche code-first la plus sûre en TypeScript. Le schéma SDL est généré automatiquement à partir du code TypeScript, garantissant la cohérence des types sans génération de code supplémentaire.

```typescript
import SchemaBuilder from "@pothos/core";
import PrismaPlugin from "@pothos/plugin-prisma";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

const builder = new SchemaBuilder<{
  PrismaTypes: PrismaTypes;
  Context: { userId: string; prisma: PrismaClient };
  Scalars: {
    DateTime: { Input: Date; Output: Date };
    EmailAddress: { Input: string; Output: string };
  };
}>({
  plugins: [PrismaPlugin],
  prisma: { client: prisma },
});

builder.prismaObject("User", {
  fields: (t) => ({
    id: t.exposeID("id"),
    email: t.exposeString("email"),
    createdAt: t.expose("createdAt", { type: "DateTime" }),
    orders: t.relation("orders", {
      args: { first: t.arg.int(), after: t.arg.string() },
    }),
  }),
});
```

**Avantages :** sécurité de type bout en bout sans génération de code, refactoring facilité (renommer un champ TypeScript renomme le champ GraphQL), intégration Prisma native avec `@pothos/plugin-prisma`.

**Inconvénients :** courbe d'apprentissage, moins lisible pour les non-TypeScript developers, SDL exporté moins prioritaire.

### Code-first avec Nexus

Nexus est une alternative plus ancienne, aujourd'hui moins maintenue mais encore présente dans de nombreuses codebases.

```typescript
import { objectType, queryField, makeSchema } from "nexus";

const User = objectType({
  name: "User",
  definition(t) {
    t.nonNull.id("id");
    t.nonNull.string("email");
    t.nonNull.field("createdAt", { type: "DateTime" });
  },
});
```

**Recommandation pragmatique :** préférer **Pothos** pour les nouveaux projets TypeScript, **schema-first + graphql-codegen** pour les équipes polyglotes ou quand l'outillage SDL est critique.

---

## Scalaires Custom

Les scalaires custom renforcent la sémantique du schéma et déplacent la validation au niveau de la couche GraphQL. La librairie `graphql-scalars` fournit des implémentations robustes.

```bash
npm install graphql-scalars
```

```typescript
import {
  DateTimeResolver,
  EmailAddressResolver,
  URLResolver,
  UUIDResolver,
  JSONResolver,
} from "graphql-scalars";
import GraphQLUpload from "graphql-upload/GraphQLUpload.mjs";

const resolvers = {
  DateTime: DateTimeResolver,       // ISO 8601, sérialisé en string
  EmailAddress: EmailAddressResolver, // validé côté serveur
  URL: URLResolver,
  UUID: UUIDResolver,
  JSON: JSONResolver,               // type escape-hatch pour données dynamiques
  Upload: GraphQLUpload,            // multipart upload (RFC)
};
```

```graphql
scalar DateTime
scalar EmailAddress
scalar URL
scalar UUID
scalar JSON
scalar Upload

type User {
  id: UUID!
  email: EmailAddress!
  website: URL
  createdAt: DateTime!
  metadata: JSON
}

type Mutation {
  uploadAvatar(file: Upload!): User!
}
```

**Scalaire `Upload` :** nécessite `graphql-upload` et un middleware multipart côté serveur. À désactiver si on utilise un service de stockage avec upload direct (S3 presigned URLs = meilleure approche en production).

---

## Interfaces et Unions

### Interfaces

Les **interfaces** définissent un contrat commun entre types. Elles conviennent quand les types partagent des champs structurels identiques.

```graphql
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
  email: EmailAddress!
}

type Product implements Node & Timestamped {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  name: String!
  price: Float!
}
```

```typescript
// Resolver __resolveType obligatoire pour les interfaces
const resolvers = {
  Node: {
    __resolveType(obj: { __typename?: string }) {
      return obj.__typename ?? null;
    },
  },
};
```

### Unions

Les **unions** regroupent des types sans champ commun. Idéales pour les résultats polymorphes.

```graphql
union SearchResult = User | Product | Article

type Query {
  search(query: String!): [SearchResult!]!
}
```

```graphql
# Côté client, on utilise des inline fragments
query Search($q: String!) {
  search(query: $q) {
    ... on User {
      id
      email
    }
    ... on Product {
      id
      name
      price
    }
    ... on Article {
      id
      title
      slug
    }
  }
}
```

### Pattern Result Union (Success | Error)

Ce pattern remplace les erreurs dans le tableau `errors` GraphQL par des types de retour explicites, rendant les erreurs métier visibles dans le schéma.

```graphql
type CreateUserSuccess {
  user: User!
}

type ValidationError {
  field: String!
  message: String!
}

type EmailAlreadyTakenError {
  email: EmailAddress!
  message: String!
}

union CreateUserResult = CreateUserSuccess | ValidationError | EmailAlreadyTakenError

type Mutation {
  createUser(input: CreateUserInput!): CreateUserResult!
}
```

```typescript
const resolvers = {
  Mutation: {
    createUser: async (_, { input }, ctx) => {
      if (!isValidEmail(input.email)) {
        return { __typename: "ValidationError", field: "email", message: "Email invalide" };
      }
      const existing = await ctx.prisma.user.findUnique({ where: { email: input.email } });
      if (existing) {
        return { __typename: "EmailAlreadyTakenError", email: input.email, message: "Email déjà utilisé" };
      }
      const user = await ctx.prisma.user.create({ data: input });
      return { __typename: "CreateUserSuccess", user };
    },
  },
  CreateUserResult: {
    __resolveType: (obj: { __typename: string }) => obj.__typename,
  },
};
```

---

## Modélisation de la Pagination

### Relay Connection Spec

La **Relay Connection spec** est le standard de facto pour la pagination cursor-based. Elle permet une implémentation côté client générique et prévisible.

```graphql
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

type Query {
  users(
    first: Int
    after: String
    last: Int
    before: String
    filter: UserFilter
    orderBy: UserOrderBy
  ): UserConnection!
}
```

```typescript
// Implémentation avec Prisma
async function usersResolver(_, args, ctx) {
  const { first = 20, after, filter, orderBy } = args;

  // Décoder le cursor (base64 d'un ID)
  const cursor = after
    ? { id: Buffer.from(after, "base64").toString("utf-8") }
    : undefined;

  const users = await ctx.prisma.user.findMany({
    take: first + 1, // on prend un de plus pour savoir s'il y a une page suivante
    skip: cursor ? 1 : 0,
    cursor,
    where: buildUserFilter(filter),
    orderBy: buildUserOrderBy(orderBy),
  });

  const hasNextPage = users.length > first;
  const nodes = hasNextPage ? users.slice(0, -1) : users;

  return {
    edges: nodes.map((user) => ({
      node: user,
      cursor: Buffer.from(user.id).toString("base64"),
    })),
    pageInfo: {
      hasNextPage,
      hasPreviousPage: !!cursor,
      startCursor: nodes[0] ? Buffer.from(nodes[0].id).toString("base64") : null,
      endCursor: nodes.at(-1) ? Buffer.from(nodes.at(-1)!.id).toString("base64") : null,
    },
    totalCount: await ctx.prisma.user.count({ where: buildUserFilter(filter) }),
  };
}
```

### Offset vs Cursor — Choix pragmatique

| Critère | Offset (`skip/limit`) | Cursor |
|---|---|---|
| Simplicité | Très simple | Modéré |
| Stabilité (items ajoutés/supprimés) | Instable | Stable |
| Performance sur grandes tables | Dégradée (`OFFSET` coûteux) | Constante |
| Navigation arbitraire (aller à la page 5) | Oui | Non |
| Usage recommandé | Admin, petits datasets | Feed, listes utilisateurs |

---

## Nullabilité et Philosophie de Design

### Nullable par défaut (convention GraphQL)

Par défaut, tous les champs GraphQL sont nullable. C'est une décision intentionnelle : si un resolver échoue, le champ retourne `null` sans invalider toute la réponse (partial data).

```graphql
type User {
  id: ID!          # Non-null : TOUJOURS présent ou l'objet n'existe pas
  email: String!   # Non-null : garanti par la DB (contrainte unique)
  bio: String      # Nullable : peut légitimement être absent
  avatar: URL      # Nullable : upload optionnel
}
```

**Règle pratique :** marquer non-null (`!`) uniquement quand l'absence de valeur est impossible ou représente une erreur système. Ne jamais forcer non-null sur un champ qui peut légitimement être vide.

### Impact côté client

Un champ non-null qui échoue propage l'erreur à son parent nullable le plus proche. Si un champ `ID!` échoue sur un type racine, toute la query retourne `null`. C'est pourquoi il faut être conservateur avec `!` sur les types racines.

---

## Conventions pour les Mutations

### Nommage : verbe + substantif

```graphql
type Mutation {
  # Pattern : action + entité (+ contexte si nécessaire)
  createUser(input: CreateUserInput!): CreateUserResult!
  updateUserProfile(id: ID!, input: UpdateUserProfileInput!): UpdateUserProfileResult!
  deleteUser(id: ID!): DeleteUserResult!
  sendPasswordResetEmail(email: EmailAddress!): SendPasswordResetEmailResult!
}
```

### Input Types séparés

Toujours utiliser un `input type` dédié plutôt que des arguments individuels. Cela facilite l'évolution du schéma (ajout de champs sans casser les clients existants).

```graphql
input CreateUserInput {
  email: EmailAddress!
  firstName: String!
  lastName: String!
  role: UserRole = MEMBER
}

input UpdateUserProfileInput {
  firstName: String
  lastName: String
  bio: String
  website: URL
}
```

---

## Subscriptions

### Quand utiliser vs polling

| Situation | Recommendation |
|---|---|
| Updates fréquents (< 5s), utilisateurs actifs | Subscription (WebSocket) |
| Updates peu fréquents, contexte mobile | Polling (`pollInterval`) |
| Données critiques temps réel (trading, chat) | Subscription |
| Contexte serverless/CDN | Polling ou webhooks |

```typescript
import { PubSub, withFilter } from "graphql-subscriptions";

const pubsub = new PubSub();

const resolvers = {
  Subscription: {
    orderStatusChanged: {
      subscribe: withFilter(
        () => pubsub.asyncIterator(["ORDER_STATUS_CHANGED"]),
        (payload, variables, context) => {
          // Filtrer : uniquement les orders de l'utilisateur connecté
          return (
            payload.orderStatusChanged.userId === context.userId &&
            payload.orderStatusChanged.orderId === variables.orderId
          );
        }
      ),
    },
  },
  Mutation: {
    updateOrderStatus: async (_, { id, status }, ctx) => {
      const order = await ctx.prisma.order.update({
        where: { id },
        data: { status },
      });
      // Publier l'événement
      await pubsub.publish("ORDER_STATUS_CHANGED", {
        orderStatusChanged: { ...order, userId: order.userId },
      });
      return { __typename: "UpdateOrderStatusSuccess", order };
    },
  },
};
```

**Authentification dans les subscriptions :** valider le token JWT lors du handshake WebSocket (dans `onConnect`), pas à chaque message. Stocker `userId` dans le context de la subscription.

---

## Directives

### Directives Built-in

```graphql
type User {
  id: ID!
  email: String!
  legacyId: Int @deprecated(reason: "Utiliser 'id' (UUID). Sera supprimé en v3.0")
}

query GetUser($id: ID!, $includeOrders: Boolean!, $skipBilling: Boolean!) {
  user(id: $id) {
    id
    orders @include(if: $includeOrders) {
      id
      total
    }
    billingInfo @skip(if: $skipBilling) {
      cardLast4
    }
  }
}
```

### Directives Custom

```typescript
import { MapperKind, mapSchema, getDirective } from "@graphql-tools/utils";
import { defaultFieldResolver, GraphQLSchema } from "graphql";

// @auth directive : protège un champ ou un type
function authDirectiveTransformer(schema: GraphQLSchema, directiveName: string) {
  return mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
      const directive = getDirective(schema, fieldConfig, directiveName)?.[0];
      if (directive) {
        const { requires } = directive;
        const { resolve = defaultFieldResolver } = fieldConfig;
        fieldConfig.resolve = async (source, args, context, info) => {
          if (!context.user) throw new Error("Non authentifié");
          if (requires && !context.user.roles.includes(requires)) {
            throw new Error(`Rôle requis : ${requires}`);
          }
          return resolve(source, args, context, info);
        };
      }
      return fieldConfig;
    },
  });
}
```

```graphql
directive @auth(requires: Role = USER) on FIELD_DEFINITION | OBJECT

enum Role { ADMIN MANAGER USER }

type Query {
  adminDashboard: Dashboard @auth(requires: ADMIN)
  myProfile: User @auth
}
```

---

## Design Évolutif et Gouvernance

### Dépréciation propre

```graphql
type Product {
  id: ID!
  name: String!
  # Ancien champ : price en cents entiers
  priceInCents: Int @deprecated(reason: "Utiliser 'price' (Float en euros). Suppression prévue 2025-Q1")
  # Nouveau champ : price en Float avec devise
  price: Float!
  currency: CurrencyCode!
}
```

### Ajout de champs sans casser

Les ajouts de champs sont rétrocompatibles. Les **modifications** et **suppressions** de champs sont des breaking changes.

| Opération | Breaking ? | Procédure |
|---|---|---|
| Ajouter un champ nullable | Non | Direct |
| Ajouter un champ non-null | Oui | Ajouter nullable d'abord, migrer, passer non-null |
| Renommer un champ | Oui | Ajouter le nouveau, déprécier l'ancien |
| Supprimer un champ | Oui | Déprécier, attendre (min. 2 releases), supprimer |
| Changer le type d'un champ | Oui | Toujours breaking |

### Schema Registry et Linting

```bash
# Apollo Studio — vérifier les breaking changes avant merge
rover graph check my-graph@current --schema ./schema.graphql

# GraphQL Inspector en CI
npx graphql-inspector diff old-schema.graphql new-schema.graphql

# @graphql-eslint pour les règles de style
npm install @graphql-eslint/eslint-plugin
```

```json
// .eslintrc.json
{
  "overrides": [
    {
      "files": ["**/*.graphql"],
      "parser": "@graphql-eslint/eslint-plugin",
      "plugins": ["@graphql-eslint"],
      "rules": {
        "@graphql-eslint/naming-convention": ["error", {
          "FieldDefinition": "camelCase",
          "TypeDefinition": "PascalCase",
          "EnumValueDefinition": "UPPER_CASE"
        }],
        "@graphql-eslint/no-deprecated": "warn",
        "@graphql-eslint/require-description": ["warn", { "types": true }]
      }
    }
  ]
}
```

---

## Erreurs GraphQL

### Deux niveaux d'erreurs

GraphQL distingue les **erreurs techniques** (dans le tableau `errors`, interruption partielle) et les **erreurs métier** (dans le résultat de la mutation via union types).

```json
// Réponse avec erreur technique + partial data
{
  "data": {
    "user": {
      "id": "123",
      "email": "alice@example.com",
      "orders": null
    }
  },
  "errors": [
    {
      "message": "Erreur lors de la récupération des commandes",
      "path": ["user", "orders"],
      "extensions": {
        "code": "INTERNAL_SERVER_ERROR",
        "timestamp": "2024-01-15T10:30:00Z"
      }
    }
  ]
}
```

```typescript
import { GraphQLError } from "graphql";

// Erreur technique avec code standardisé
throw new GraphQLError("Ressource non trouvée", {
  extensions: {
    code: "NOT_FOUND",
    resourceType: "User",
    resourceId: id,
  },
});

// Codes standard : UNAUTHENTICATED, FORBIDDEN, NOT_FOUND,
// BAD_USER_INPUT, INTERNAL_SERVER_ERROR, RATE_LIMITED
```

**Règle :** les erreurs métier prévisibles (validation, not found, conflit) doivent être des **union types dans le schéma**. Les erreurs système inattendues vont dans le tableau `errors`. Ne jamais exposer les stack traces en production — filtrer dans le `formatError` d'Apollo Server.
