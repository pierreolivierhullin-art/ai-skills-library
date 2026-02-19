# Études de Cas — GraphQL en Production

Ces quatre études de cas sont tirées de contextes réels. Elles couvrent les décisions techniques, les compromis, les implémentations concrètes et les métriques mesurées. Chaque cas illustre un problème archétypal rencontré lors du déploiement de GraphQL à l'échelle.

---

## Cas 1 — Migration REST → GraphQL (Marketplace B2C, 50K DAU)

### Contexte

Une marketplace e-commerce avec 50 000 utilisateurs actifs quotidiens. L'API REST existante comptait 80 endpoints distincts. L'équipe mobile constatait des problèmes critiques de performance : **over-fetching** massif (les réponses REST incluaient des dizaines de champs non utilisés par le mobile), et **under-fetching** sur le web (la page produit nécessitait 5 requêtes HTTP en cascade : produit, vendeur, avis, stock, recommandations).

### Problème quantifié

- Mobile : chargement de 3x plus de données que nécessaire (champs non utilisés, images haute résolution inutiles)
- Web : 5 requêtes HTTP séquentielles pour afficher une page produit (TTFB perçu : 900ms sur 3G)
- Aucune possibilité de personnaliser les réponses sans créer de nouveaux endpoints REST
- 80 endpoints REST à maintenir, documentation souvent désynchronisée

### Stratégie : GraphQL comme BFF devant les services REST

L'équipe a choisi une **migration progressive** sans réécriture des services backend. GraphQL agit comme un **Backend For Frontend (BFF)** qui agrège plusieurs services REST existants. Aucun service backend n'est modifié.

```typescript
// Apollo Server avec RESTDataSource — agrégation de 3 services REST
import { RESTDataSource } from "@apollo/datasource-rest";

class ProductService extends RESTDataSource {
  baseURL = "https://api-products.internal/v2/";

  async getProduct(id: string) {
    return this.get(`products/${id}`);
  }

  async getProductReviews(productId: string) {
    return this.get(`products/${productId}/reviews?limit=10`);
  }
}

class SellerService extends RESTDataSource {
  baseURL = "https://api-sellers.internal/v1/";

  async getSeller(id: string) {
    return this.get(`sellers/${id}`);
  }
}

class InventoryService extends RESTDataSource {
  baseURL = "https://api-inventory.internal/v1/";

  async getStock(productId: string, variantId?: string) {
    const path = variantId
      ? `stock/${productId}/variants/${variantId}`
      : `stock/${productId}`;
    return this.get(path);
  }
}
```

```graphql
# Schéma GraphQL unifié — exposé au client
type Product {
  id: ID!
  name: String!
  description: String!
  price: Float!
  currency: String!
  seller: Seller!
  stock: StockInfo!
  reviews(first: Int = 5): ReviewConnection!
  images: [ProductImage!]!
  # Champ calculé : non disponible dans les APIs REST individuelles
  isAvailable: Boolean!
}

type Query {
  # UNE seule query remplace 5 requêtes REST en cascade
  product(id: ID!): Product
}
```

```typescript
// Resolvers : parallélisation avec Promise.all
const resolvers = {
  Query: {
    product: async (_, { id }, ctx) => {
      // Appel principal — séquentiel (nécessaire pour avoir l'ID du seller)
      return ctx.dataSources.productService.getProduct(id);
    },
  },
  Product: {
    // Ces resolvers s'exécutent en parallèle grâce au moteur GraphQL
    seller: async (product, _, ctx) => {
      return ctx.dataSources.sellerService.getSeller(product.sellerId);
    },
    stock: async (product, _, ctx) => {
      return ctx.dataSources.inventoryService.getStock(product.id);
    },
    reviews: async (product, { first }, ctx) => {
      return ctx.dataSources.productService.getProductReviews(product.id);
    },
    // Champ calculé — logique métier centralisée dans le BFF
    isAvailable: (product) => {
      return product.status === "ACTIVE" && product.stock?.quantity > 0;
    },
    // Mobile peut demander uniquement les petites images — filtrage serveur-side
    images: (product, _, __, info) => {
      // Inspecter si le client a demandé le champ 'url' ou 'thumbnailUrl'
      return product.images;
    },
  },
};
```

### Configuration graphql-codegen côté client

```yaml
# codegen.yml
overwrite: true
schema: "http://localhost:4000/graphql"
documents: "src/**/*.graphql"
generates:
  src/generated/graphql.ts:
    plugins:
      - "typescript"
      - "typescript-operations"
      - "typescript-react-apollo"
    config:
      withHooks: true
      withComponent: false
      withResultType: true
      # Fragments colocalisés avec les composants qui les utilisent
      inlineFragmentTypes: "combine"
```

```graphql
# src/pages/ProductPage/ProductPage.graphql
query GetProductPage($id: ID!) {
  product(id: $id) {
    ...ProductHero_product
    ...ProductDetails_product
    seller {
      ...SellerCard_seller
    }
  }
}

# Fragment colocalisé avec le composant ProductHero
fragment ProductHero_product on Product {
  id
  name
  images(first: 1) {
    thumbnailUrl
    alt
  }
  price
  currency
  isAvailable
}
```

### Métriques mesurées

| Métrique | Avant (REST) | Après (GraphQL BFF) | Amélioration |
|---|---|---|---|
| Données transférées (mobile, page produit) | 48 KB | 19 KB | -60% bandwidth |
| Requêtes HTTP (page produit) | 5 requêtes séquentielles | 1 requête | -80% |
| TTFB (Time To First Byte) perçu | 900ms | 700ms | -200ms |
| Endpoints REST à maintenir | 80 | 80 (inchangés) | Migration progressive |
| Types TypeScript générés automatiquement | 0 (manual) | 100% auto-générés | DX améliorée |

### Leçon clé

GraphQL comme BFF devant des APIs REST existantes est la stratégie de migration la moins risquée. Elle n'exige aucune modification des services backend, permet aux équipes frontend de prendre ownership du schéma, et livre de la valeur immédiatement. La génération de code TypeScript depuis le schéma élimine toute dérive entre l'API et le client.

---

## Cas 2 — Résolution du N+1 (SaaS Analytique, 200K Requêtes/Jour)

### Contexte

Une plateforme SaaS d'analytique business avec 200 000 requêtes GraphQL par jour. Le dashboard principal affiche une liste de projets avec leurs membres et les avatars de chaque membre — 3 niveaux de nesting. Une alerte PagerDuty signalait régulièrement une charge DB critique aux heures de pointe.

### Problème quantifié

```graphql
# Cette query innocente causait 420 requêtes DB
query {
  projects(first: 20) {
    edges {
      node {
        id
        name
        members(first: 10) {
          edges {
            node {
              id
              name
              avatarUrl
              role
            }
          }
        }
      }
    }
  }
}
```

Décomposition des requêtes DB générées :
- 1 requête : `SELECT * FROM projects LIMIT 20`
- 20 requêtes : `SELECT * FROM memberships WHERE project_id = ?` (une par projet)
- 400 requêtes : `SELECT * FROM users WHERE id = ?` (une par membre, par projet)

**Total : 421 requêtes DB.** Sur Postgres, un `EXPLAIN ANALYZE` montrait 800ms de temps total avec des index scans répétés sur `users.id`.

### Solution : DataLoader à chaque niveau + inspection des fieldNodes

```typescript
// context.ts — un DataLoader par requête, isolation du cache
export function createLoaders(prisma: PrismaClient) {
  // Loader niveau 1 : projets (non nécessaire ici, mais pour __resolveReference)
  const projectLoader = new DataLoader<string, Project | null>(async (ids) => {
    const projects = await prisma.project.findMany({
      where: { id: { in: [...ids] } },
    });
    const map = new Map(projects.map((p) => [p.id, p]));
    return ids.map((id) => map.get(id) ?? null);
  });

  // Loader niveau 2 : memberships par projectId (one-to-many)
  const membershipsByProjectIdLoader = new DataLoader<string, Membership[]>(
    async (projectIds) => {
      const memberships = await prisma.membership.findMany({
        where: { projectId: { in: [...projectIds] } },
        select: { id: true, projectId: true, userId: true, role: true },
      });
      const grouped = new Map(projectIds.map((id) => [id, [] as Membership[]]));
      memberships.forEach((m) => grouped.get(m.projectId)?.push(m));
      return projectIds.map((id) => grouped.get(id) ?? []);
    }
  );

  // Loader niveau 3 : users par id (many-to-one via memberships)
  const userLoader = new DataLoader<string, User | null>(async (userIds) => {
    const users = await prisma.user.findMany({
      where: { id: { in: [...userIds] } },
      select: { id: true, name: true, email: true, avatarUrl: true },
    });
    const map = new Map(users.map((u) => [u.id, u]));
    // CRITIQUE : retourner dans l'ordre exact des userIds reçus
    return userIds.map((id) => map.get(id) ?? null);
  });

  return { projectLoader, membershipsByProjectIdLoader, userLoader };
}
```

```typescript
// resolvers.ts — inspection des fieldNodes pour skip les relations non demandées
import { GraphQLResolveInfo, FieldNode, SelectionSetNode } from "graphql";

function hasField(info: GraphQLResolveInfo, ...fieldPath: string[]): boolean {
  let selectionSet: SelectionSetNode | undefined =
    info.fieldNodes[0]?.selectionSet;

  for (const fieldName of fieldPath) {
    if (!selectionSet) return false;
    const field = selectionSet.selections.find(
      (s): s is FieldNode => s.kind === "Field" && s.name.value === fieldName
    );
    if (!field) return false;
    selectionSet = field.selectionSet;
  }
  return true;
}

const resolvers = {
  Project: {
    members: async (project: Project, args, ctx, info: GraphQLResolveInfo) => {
      // Skip si le client n'a pas demandé 'members'
      if (!hasField(info, "edges")) {
        return { edges: [], pageInfo: { hasNextPage: false, hasPreviousPage: false } };
      }

      const memberships = await ctx.loaders.membershipsByProjectIdLoader.load(project.id);
      const limited = memberships.slice(0, args.first ?? 10);

      return {
        edges: limited.map((m) => ({
          node: m,
          cursor: Buffer.from(m.id).toString("base64"),
        })),
        pageInfo: {
          hasNextPage: memberships.length > (args.first ?? 10),
          hasPreviousPage: false,
        },
      };
    },
  },

  Membership: {
    // Résolu via DataLoader — batché avec tous les autres membres de la requête
    user: async (membership: Membership, _, ctx) => {
      return ctx.loaders.userLoader.load(membership.userId);
    },
  },
};
```

### Comparaison EXPLAIN ANALYZE avant/après

**Avant (N+1) :**
```sql
-- Exécuté 400 fois :
EXPLAIN ANALYZE SELECT id, name, email, avatar_url
FROM users WHERE id = 'usr_abc123';
-- Execution Time: 0.8ms × 400 = 320ms de queries users seules
-- Planning Time: 0.3ms × 400 = 120ms overhead PostgreSQL
```

**Après (DataLoader batché) :**
```sql
-- Exécuté 1 fois :
EXPLAIN ANALYZE SELECT id, name, email, avatar_url
FROM users WHERE id IN ('usr_1', 'usr_2', ..., 'usr_200');
-- Index Scan on users_pkey: Rows=200, Execution Time: 3.2ms
-- Planning Time: 0.4ms
```

### Métriques mesurées

| Métrique | Avant | Après | Amélioration |
|---|---|---|---|
| Requêtes DB (query dashboard 20 projets) | 421 | 4 | -99% |
| Temps de réponse P50 | 800ms | 45ms | -94% |
| Temps de réponse P99 | 2 400ms | 180ms | -92% |
| CPU PostgreSQL (heures de pointe) | 85% | 8% | -90% |
| Charge DB totale | Saturée | Nominale | -95% |

### Leçon clé

Le DataLoader doit être instancié dans le context GraphQL (une instance par requête), jamais au niveau module. La batch function doit impérativement retourner les résultats dans l'ordre exact des clés d'entrée — un bug dans cet ordering produit des corruptions de données silencieuses. L'inspection des `fieldNodes` permet d'éviter des DataLoader calls pour des relations que le client n'a pas demandées.

---

## Cas 3 — Federation Micro-services (Scale-up, 4 Équipes)

### Contexte

Une scale-up e-commerce avec 4 équipes produit indépendantes : **Users** (authentification, profils), **Products** (catalogue, prix), **Orders** (panier, commandes), **Billing** (facturation, abonnements). L'API GraphQL était un monolithe partagé dans un seul dépôt — tous les resolvers, tous les types, un seul serveur.

### Problème

- **Contention entre équipes :** chaque PR modifiant le schéma bloquait les 3 autres équipes (reviews croisées obligatoires, conflits de merge fréquents)
- **Déploiements couplés :** impossible de déployer une feature Orders sans déployer le monolithe entier
- **On-call partagé :** un bug dans Billing pouvait mettre hors service l'API des Users
- **Temps moyen de time-to-feature :** 3 semaines (revue cross-équipe + coordination déploiement)

### Solution : Apollo Federation v2

Chaque équipe migre son domaine vers un subgraph indépendant. L'Apollo Router remplace le monolithe comme point d'entrée unique.

```graphql
# subgraph-users/schema.graphql
extend schema
  @link(url: "https://specs.apollo.dev/federation/v2.5", import: ["@key", "@shareable"])

type User @key(fields: "id") {
  id: ID!
  email: String!
  name: String!
  createdAt: DateTime!
  # Profil public — @shareable permet à d'autres subgraphs de l'utiliser
  publicProfile: UserPublicProfile! @shareable
}

type UserPublicProfile @shareable {
  displayName: String!
  avatarUrl: URL
}

type Query {
  me: User
  user(id: ID!): User
}

type Mutation {
  updateProfile(input: UpdateProfileInput!): UpdateProfileResult!
}
```

```graphql
# subgraph-orders/schema.graphql
extend schema
  @link(url: "https://specs.apollo.dev/federation/v2.5",
    import: ["@key", "@external", "@requires"])

# Extension de l'entité User depuis le subgraph Users
type User @key(fields: "id") {
  id: ID!
  # Champ défini dans Users, requis pour filtrer les orders par timezone
  timezone: String! @external
  orders(first: Int, status: OrderStatus): OrderConnection!
}

type Order @key(fields: "id") {
  id: ID!
  user: User!
  status: OrderStatus!
  total: Float!
  currency: String!
  items: [OrderItem!]!
  createdAt: DateTime!
  # Ce champ nécessite la timezone de l'utilisateur (définie dans Users)
  localDeliveryDate: String! @requires(fields: "user { timezone }")
}

type Query {
  order(id: ID!): Order
  myOrders(first: Int, status: OrderStatus): OrderConnection!
}
```

```typescript
// subgraph-orders/resolvers.ts
const resolvers = {
  User: {
    orders: async (user: { id: string }, args, ctx) => {
      return ctx.loaders.ordersByUserId.load(user.id);
    },
    __resolveReference: async (ref: { id: string }, ctx) => {
      // Retourner uniquement l'id — les champs @external sont fournis par le Router
      return { id: ref.id };
    },
  },
  Order: {
    localDeliveryDate: (order: Order & { user: { timezone: string } }) => {
      // 'timezone' est disponible car @requires le pré-charge depuis Users
      return formatDateInTimezone(order.deliveryDate, order.user.timezone);
    },
    __resolveReference: async (ref: { id: string }, ctx) => {
      return ctx.loaders.orderLoader.load(ref.id);
    },
  },
};
```

```yaml
# router.yaml — configuration du Router en production
supergraph:
  path: /graphql
  introspection: false

headers:
  all:
    request:
      - propagate:
          named: Authorization
      - propagate:
          named: x-request-id

authentication:
  router:
    jwt:
      jwks:
        - url: https://auth.example.com/.well-known/jwks.json
          poll_interval: 60s

limits:
  max_depth: 10

telemetry:
  tracing:
    otlp:
      endpoint: http://otel-collector:4317
      protocol: grpc
```

### CI Pipeline avec Rover Schema Checks

```yaml
# .github/workflows/subgraph-check.yml
name: Schema Check

on:
  pull_request:
    paths:
      - 'src/**/*.graphql'
      - 'schema.graphql'

jobs:
  schema-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Rover
        run: |
          curl -sSL https://rover.apollo.dev/nix/latest | sh
          echo "$HOME/.rover/bin" >> $GITHUB_PATH

      - name: Validate subgraph schema (composition locale)
        run: |
          rover subgraph check ${{ vars.APOLLO_GRAPH_REF }} \
            --name ${{ vars.SUBGRAPH_NAME }} \
            --schema ./schema.graphql
        env:
          APOLLO_KEY: ${{ secrets.APOLLO_KEY }}

      - name: Comment PR with schema diff
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ Schema check failed. Breaking changes detected. See workflow logs.'
            })
```

### Métriques mesurées

| Métrique | Avant (monolithe) | Après (Federation) | Amélioration |
|---|---|---|---|
| Équipes pouvant déployer indépendamment | 0 | 4 | Indépendance totale |
| Conflits de schema par sprint | 12 | 0 | -100% |
| Time-to-feature moyen | 3 semaines | 1,8 semaine | -40% |
| Incidents cross-équipe causés par deploy | 3/mois | 0/mois | Isolation complète |
| Schema checks en CI | Non | Oui (100% des PRs) | Prévention proactive |

### Leçon clé

La fédération libère les équipes du couplage de déploiement, mais exige une gouvernance formelle du schéma. Sans schema checks automatiques en CI (via `rover subgraph check`), les équipes introduiront inévitablement des breaking changes sans s'en rendre compte. Apollo Studio + schema checks = le filet de sécurité indispensable.

---

## Cas 4 — Client Apollo Optimisé (React SPA, Fintech)

### Contexte

Un dashboard financier React pour une néobanque. Apollo Client gérait l'état de l'application : soldes, transactions, virements. L'équipe frontend signalait un cache incohérent après les mutations (solde affiché non mis à jour), 5 re-renders par mutation observés dans React DevTools, et un polling toutes les 30 secondes pour les mises à jour de solde.

### Problème détaillé

```typescript
// Problème 1 : mutation sans update du cache → solde non mis à jour
const [transfer] = useMutation(TRANSFER_MUTATION);

const handleTransfer = async () => {
  await transfer({
    variables: { from: accountId, to: destinationId, amount: 500 },
    // Pas d'update du cache → le solde affiché reste l'ancien
  });
  // L'utilisateur voit l'ancien solde pendant 30s (jusqu'au prochain poll)
};
```

```typescript
// Problème 2 : re-renders excessifs — query monolithique
const { data } = useQuery(FULL_DASHBOARD_QUERY);
// Une mutation sur n'importe quelle transaction re-render TOUT le dashboard
// Apollo Client invalide l'objet racine → 5 composants re-rendent
```

### Solution 1 : Fragments colocalisés

Chaque composant déclare ses besoins avec un fragment. Apollo Client normalise le cache par `__typename + id`, donc seul le composant affichant la donnée modifiée re-rend.

```typescript
// components/AccountBalance/AccountBalance.tsx
import { gql, useFragment } from "@apollo/client";

// Fragment colocalisé — ce composant "owns" ses champs
export const ACCOUNT_BALANCE_FRAGMENT = gql`
  fragment AccountBalance_account on Account {
    id
    balance
    currency
    lastUpdatedAt
  }
`;

export function AccountBalance({ accountId }: { accountId: string }) {
  // useFragment lit directement depuis le cache normalisé — ultra-performant
  const { data: account, complete } = useFragment({
    fragment: ACCOUNT_BALANCE_FRAGMENT,
    fragmentName: "AccountBalance_account",
    from: { __typename: "Account", id: accountId },
  });

  if (!complete) return <Skeleton />;

  return (
    <div>
      <span>{account.balance}</span>
      <span>{account.currency}</span>
    </div>
  );
}
```

```graphql
# Dashboard query — agrège les fragments des composants enfants
query DashboardQuery($accountId: ID!) {
  account(id: $accountId) {
    ...AccountBalance_account
    ...TransactionList_account
    ...QuickActions_account
  }
}
```

### Solution 2 : update() explicite du cache après mutation

```typescript
// components/TransferForm/TransferForm.tsx
import { gql, useMutation, useApolloClient } from "@apollo/client";

const TRANSFER_MUTATION = gql`
  mutation Transfer($input: TransferInput!) {
    transfer(input: $input) {
      ... on TransferSuccess {
        transaction {
          id
          amount
          status
          createdAt
        }
        fromAccount {
          id
          balance  # Le serveur retourne le NOUVEAU solde
        }
        toAccount {
          id
          balance
        }
      }
      ... on InsufficientFundsError {
        message
        available
        requested
      }
    }
  }
`;

export function TransferForm() {
  const [transfer, { loading }] = useMutation(TRANSFER_MUTATION, {
    // update() est appelé AVANT que React re-rende — mise à jour synchrone du cache
    update(cache, { data }) {
      if (data?.transfer.__typename !== "TransferSuccess") return;

      const { fromAccount, toAccount, transaction } = data.transfer;

      // Mettre à jour le solde du compte source dans le cache
      cache.modify({
        id: cache.identify(fromAccount),
        fields: {
          balance: () => fromAccount.balance,
        },
      });

      // Mettre à jour le solde du compte destination
      cache.modify({
        id: cache.identify(toAccount),
        fields: {
          balance: () => toAccount.balance,
        },
      });

      // Ajouter la nouvelle transaction en tête de liste
      cache.modify({
        id: cache.identify(fromAccount),
        fields: {
          transactions: (existingRefs = [], { toReference }) => {
            const newRef = toReference(transaction);
            return [newRef, ...existingRefs];
          },
        },
      });
    },
  });

  const handleSubmit = async (values: TransferValues) => {
    const result = await transfer({ variables: { input: values } });
    if (result.data?.transfer.__typename === "InsufficientFundsError") {
      // Erreur métier — afficher dans le formulaire
      setError(result.data.transfer.message);
    }
  };

  return <form onSubmit={handleSubmit}>{/* ... */}</form>;
}
```

### Solution 3 : Optimistic UI pour les virements

```typescript
const [transfer] = useMutation(TRANSFER_MUTATION, {
  // optimisticResponse : mis à jour IMMÉDIATEMENT dans le cache avant la réponse serveur
  optimisticResponse: (variables) => ({
    transfer: {
      __typename: "TransferSuccess",
      transaction: {
        __typename: "Transaction",
        id: `temp-${Date.now()}`, // ID temporaire
        amount: variables.input.amount,
        status: "PENDING",
        createdAt: new Date().toISOString(),
      },
      fromAccount: {
        __typename: "Account",
        id: variables.input.fromAccountId,
        // Déduction optimiste du solde (sera corrigé par la réponse serveur)
        balance: currentBalance - variables.input.amount,
      },
      toAccount: {
        __typename: "Account",
        id: variables.input.toAccountId,
        balance: destinationBalance + variables.input.amount,
      },
    },
  }),
  update(cache, { data }) {
    // update() est appelé deux fois : avec l'optimistic response, puis avec la vraie
    // Apollo gère automatiquement le rollback si la mutation échoue
    if (data?.transfer.__typename !== "TransferSuccess") return;
    // ... même code qu'au-dessus
  },
});
```

### Solution 4 : Subscriptions pour les mises à jour temps réel

```typescript
// Remplace le polling toutes les 30 secondes
import { useSubscription } from "@apollo/client";

const ACCOUNT_UPDATED_SUBSCRIPTION = gql`
  subscription AccountUpdated($accountId: ID!) {
    accountUpdated(accountId: $accountId) {
      id
      balance
      currency
      lastUpdatedAt
    }
  }
`;

export function useAccountRealtime(accountId: string) {
  const client = useApolloClient();

  useSubscription(ACCOUNT_UPDATED_SUBSCRIPTION, {
    variables: { accountId },
    onData: ({ data }) => {
      if (!data.data?.accountUpdated) return;
      const updatedAccount = data.data.accountUpdated;

      // Mettre à jour le cache Apollo — tous les composants utilisant ce fragment re-rendent
      client.writeFragment({
        id: client.cache.identify(updatedAccount),
        fragment: ACCOUNT_BALANCE_FRAGMENT,
        data: updatedAccount,
      });
    },
  });
}
```

```typescript
// Configurer Apollo Client avec WebSocket Link pour les subscriptions
import { ApolloClient, InMemoryCache, split } from "@apollo/client";
import { GraphQLWsLink } from "@apollo/client/link/subscriptions";
import { createClient } from "graphql-ws";
import { getMainDefinition } from "@apollo/client/utilities";
import { createHttpLink } from "@apollo/client";

const httpLink = createHttpLink({ uri: "https://api.example.com/graphql" });

const wsLink = new GraphQLWsLink(
  createClient({
    url: "wss://api.example.com/graphql",
    connectionParams: () => ({
      authorization: `Bearer ${getAuthToken()}`,
    }),
  })
);

// Routing : subscriptions → WebSocket, queries/mutations → HTTP
const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === "OperationDefinition" &&
      definition.operation === "subscription"
    );
  },
  wsLink,
  httpLink
);

const client = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache({
    typePolicies: {
      Account: {
        // Cache normalisé par id — chaque Account est une entrée unique
        keyFields: ["id"],
      },
      Query: {
        fields: {
          // Pagination cursor-based : merge des pages au lieu de remplacement
          transactions: {
            keyArgs: ["accountId", "status"],
            merge(existing = { edges: [] }, incoming) {
              return {
                ...incoming,
                edges: [...(existing.edges ?? []), ...(incoming.edges ?? [])],
              };
            },
          },
        },
      },
    },
  }),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: "cache-and-network", // Affiche le cache immédiatement + rafraîchit
      errorPolicy: "partial", // Affiche les données partielles même en cas d'erreur
    },
  },
});
```

### Métriques mesurées

| Métrique | Avant | Après | Amélioration |
|---|---|---|---|
| Re-renders par mutation (React DevTools) | 5 | 1 | -80% |
| Délai d'affichage du nouveau solde | 30 secondes (poll) | < 100ms (optimistic + subscription) | -99% |
| Incohérences de cache signalées | 8/semaine | 0/semaine | -100% |
| Perceptions UX "lenteur" (user surveys) | 62% | 11% | -82% |
| Requêtes polling supprimées | 2 880/jour | 0 | Bandwidth économisée |

### Leçon clé

Les fragments colocalisés avec `useFragment` et la mise à jour explicite du cache via `update()` sont les deux pratiques les plus impactantes pour un client Apollo performant et cohérent. L'optimistic UI avec Apollo gère automatiquement le rollback en cas d'échec serveur — une feature sous-utilisée qui transforme la perception de réactivité de l'application. Les subscriptions WebSocket remplacent avantageusement le polling pour les données financières qui doivent être temps réel.
