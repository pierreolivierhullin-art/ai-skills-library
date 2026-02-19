---
name: graphql
version: 1.0.0
description: >
  GraphQL schema design SDL, resolvers mutations subscriptions, DataLoader N+1 problem,
  Apollo Server Apollo Client, GraphQL Code Generator, schema-first vs code-first,
  Apollo Federation subgraphs supergraph, persisted queries, query complexity limits,
  GraphQL security depth limiting, schema stitching, Relay, urql, type-safe GraphQL TypeScript,
  fragments colocation, optimistic updates, pagination cursor-based
---

# GraphQL — API Flexible et Type-Safe

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu conçois une API consommée par plusieurs clients avec des besoins différents (mobile, web, partenaires)
- Tu as un problème d'over-fetching ou under-fetching avec une API REST
- Tu mets en place une architecture micro-services avec un gateway GraphQL fédéré
- Tu utilises Apollo Client et veux optimiser le cache et les requêtes
- Tu dois résoudre un problème de performance N+1 dans des resolvers imbriqués
- Tu veux générer automatiquement les types TypeScript depuis un schéma GraphQL

---

## Schéma SDL — Design des Types

```graphql
# schema.graphql

scalar DateTime
scalar Upload
scalar JSON

# Types de base
type Utilisateur {
  id: ID!
  email: String!
  nom: String!
  role: RoleUtilisateur!
  créeA: DateTime!
  commandes(
    page: Int = 1
    limite: Int = 10
    statut: StatutCommande
  ): PaginationCommandes!
}

type Commande {
  id: ID!
  référence: String!
  statut: StatutCommande!
  total: Float!
  lignes: [LigneCommande!]!
  utilisateur: Utilisateur!
  créeA: DateTime!
}

type LigneCommande {
  produit: Produit!
  quantité: Int!
  prixUnitaire: Float!
}

type PaginationCommandes {
  données: [Commande!]!
  total: Int!
  page: Int!
  pages: Int!
  curseurSuivant: String
}

enum RoleUtilisateur { ADMIN USER MODERATEUR }
enum StatutCommande { EN_ATTENTE CONFIRMEE EXPEDIEE LIVREE ANNULEE }

# Queries — lecture
type Query {
  moi: Utilisateur!
  utilisateur(id: ID!): Utilisateur
  commandes(
    curseur: String
    limite: Int = 20
    statut: StatutCommande
  ): PaginationCommandes!
}

# Mutations — écriture
type Mutation {
  créerCommande(entrée: EntréeCréerCommande!): MutationCommande!
  mettreÀJourStatutCommande(
    id: ID!
    statut: StatutCommande!
  ): MutationCommande!
}

union MutationCommande = Commande | ErreurValidation | ErreurAuthorisation

type ErreurValidation {
  message: String!
  champs: [ErreurChamp!]!
}

type ErreurAuthorisation {
  message: String!
}

type ErreurChamp {
  champ: String!
  message: String!
}

input EntréeCréerCommande {
  lignes: [EntréeLigneCommande!]!
  adresseLivraison: EntréeAdresse!
}

input EntréeLigneCommande {
  produitId: ID!
  quantité: Int!
}

# Subscriptions — temps réel
type Subscription {
  suivi(commandeId: ID!): MiseÀJourCommande!
}

type MiseÀJourCommande {
  commande: Commande!
  événement: String!
}
```

---

## Apollo Server — Resolvers

```typescript
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import DataLoader from 'dataloader';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Context typé
interface Context {
  utilisateur?: { id: string; role: string };
  loaders: {
    utilisateur: DataLoader<string, Utilisateur | null>;
    commandes: DataLoader<string, Commande[]>;
  };
}

// Créer les DataLoaders dans le context (un nouveau par requête)
function créerLoaders() {
  return {
    utilisateur: new DataLoader<string, Utilisateur | null>(async (ids) => {
      const utilisateurs = await prisma.utilisateur.findMany({
        where: { id: { in: [...ids] } },
      });
      const map = new Map(utilisateurs.map(u => [u.id, u]));
      return ids.map(id => map.get(id) ?? null);
    }),

    commandes: new DataLoader<string, Commande[]>(async (utilisateurIds) => {
      const commandes = await prisma.commande.findMany({
        where: { utilisateurId: { in: [...utilisateurIds] } },
        include: { lignes: { include: { produit: true } } },
      });
      return utilisateurIds.map(id => commandes.filter(c => c.utilisateurId === id));
    }),
  };
}

const resolvers = {
  Query: {
    moi: async (_: unknown, __: unknown, ctx: Context) => {
      if (!ctx.utilisateur) throw new GraphQLError('Non authentifié', {
        extensions: { code: 'UNAUTHENTICATED' },
      });
      return ctx.loaders.utilisateur.load(ctx.utilisateur.id);
    },

    commandes: async (_: unknown, args: PaginationArgs, ctx: Context) => {
      const { curseur, limite = 20, statut } = args;
      const commandes = await prisma.commande.findMany({
        take: limite + 1,  // +1 pour savoir s'il y a une page suivante
        cursor: curseur ? { id: curseur } : undefined,
        skip: curseur ? 1 : 0,
        where: statut ? { statut } : {},
        orderBy: { créeA: 'desc' },
      });

      const aPage = commandes.length > limite;
      const données = aPage ? commandes.slice(0, -1) : commandes;

      return {
        données,
        total: await prisma.commande.count({ where: statut ? { statut } : {} }),
        curseurSuivant: aPage ? données[données.length - 1].id : null,
      };
    },
  },

  Utilisateur: {
    // Resolver qui utilise DataLoader (pas de N+1)
    commandes: (parent: Utilisateur, _: unknown, ctx: Context) =>
      ctx.loaders.commandes.load(parent.id),
  },

  Mutation: {
    créerCommande: async (_: unknown, { entrée }: { entrée: EntréeCommande }, ctx: Context) => {
      if (!ctx.utilisateur) {
        return { __typename: 'ErreurAuthorisation', message: 'Non authentifié' };
      }

      // Validation
      const erreurs = validerEntréeCommande(entrée);
      if (erreurs.length > 0) {
        return { __typename: 'ErreurValidation', message: 'Données invalides', champs: erreurs };
      }

      const commande = await prisma.commande.create({
        data: {
          utilisateurId: ctx.utilisateur.id,
          statut: 'EN_ATTENTE',
          lignes: {
            create: entrée.lignes.map(l => ({
              produitId: l.produitId,
              quantité: l.quantité,
              prixUnitaire: l.prixUnitaire,
            })),
          },
        },
        include: { lignes: { include: { produit: true } } },
      });

      return { __typename: 'Commande', ...commande };
    },
  },

  // Résoudre le union type
  MutationCommande: {
    __resolveType: (obj: { __typename: string }) => obj.__typename,
  },
};

const server = new ApolloServer<Context>({ typeDefs, resolvers });

// Middleware Express avec context
app.use('/graphql', expressMiddleware(server, {
  context: async ({ req }) => ({
    utilisateur: await authFromToken(req.headers.authorization),
    loaders: créerLoaders(),
  }),
}));
```

---

## Problème N+1 et DataLoader

```typescript
// ❌ Sans DataLoader : N+1 requêtes
const resolvers = {
  Commande: {
    utilisateur: async (commande) => {
      // Appelé N fois pour N commandes → N requêtes DB séparées
      return prisma.utilisateur.findUnique({ where: { id: commande.utilisateurId } });
    },
  },
};

// ✅ Avec DataLoader : 1 requête groupée
const userLoader = new DataLoader<string, Utilisateur | null>(async (ids) => {
  console.log(`Chargement de ${ids.length} utilisateurs en 1 requête`);
  const users = await prisma.utilisateur.findMany({
    where: { id: { in: [...ids] } },
  });
  const map = new Map(users.map(u => [u.id, u]));
  // IMPORTANT : retourner dans le MÊME ordre que les ids
  return ids.map(id => map.get(id) ?? null);
});

const resolvers = {
  Commande: {
    utilisateur: (commande, _, ctx) => ctx.loaders.user.load(commande.utilisateurId),
  },
};
```

---

## Sécurité GraphQL

```typescript
import depthLimit from 'graphql-depth-limit';
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(7),                              // Profondeur maximale
    createComplexityLimitRule(1000, {           // Complexité maximale
      scalarCost: 1,
      objectCost: 5,
      listFactor: 10,
    }),
  ],
  introspection: process.env.NODE_ENV !== 'production',  // Désactiver en prod
  includeStacktraceInErrorResponses: process.env.NODE_ENV === 'development',
});

// Persisted Queries : prévenir l'injection de requêtes arbitraires
// Côté client : hash SHA256 de la requête
// Côté serveur : vérifier que le hash est dans la liste autorisée
```

---

## GraphQL Code Generator

```yaml
# codegen.yml
schema: http://localhost:4000/graphql
documents: src/**/*.graphql
generates:
  src/generated/graphql.ts:
    plugins:
      - typescript
      - typescript-operations
      - typescript-react-apollo
    config:
      withHooks: true
      strictScalars: true
      scalars:
        DateTime: string
        Upload: File
```

```typescript
// Fragment colocalisé avec le composant
// components/CarteBadge.graphql
// fragment CarteBadge on Utilisateur {
//   id
//   nom
//   role
// }

// Usage typé automatiquement
import { CarteBadgeFragment, useGetCommandesQuery } from '@/generated/graphql';

function CarteBadge({ utilisateur }: { utilisateur: CarteBadgeFragment }) {
  return <div>{utilisateur.nom} — {utilisateur.role}</div>;
}

function ListeCommandes() {
  const { data, loading, error } = useGetCommandesQuery({
    variables: { limite: 20, statut: StatutCommande.EnAttente },
  });

  if (loading) return <Spinner />;
  if (error) return <Erreur message={error.message} />;

  return data?.commandes.données.map(c => <CartéCommande key={c.id} commande={c} />);
}
```

---

## Apollo Federation — Architecture Micro-Services

```typescript
// service-utilisateurs/schema.ts
import { buildSubgraphSchema } from '@apollo/subgraph';
import gql from 'graphql-tag';

const typeDefs = gql`
  extend schema @link(url: "https://specs.apollo.dev/federation/v2.0", import: ["@key"])

  type Utilisateur @key(fields: "id") {
    id: ID!
    email: String!
    nom: String!
  }

  type Query {
    moi: Utilisateur
  }
`;

const resolvers = {
  Utilisateur: {
    __resolveReference: (ref: { id: string }) =>
      prisma.utilisateur.findUnique({ where: { id: ref.id } }),
  },
};

// service-commandes/schema.ts — Étend Utilisateur depuis un autre service
const typeDefs2 = gql`
  extend schema @link(...)

  extend type Utilisateur @key(fields: "id") {
    id: ID! @external
    commandes: [Commande!]!
  }

  type Commande @key(fields: "id") {
    id: ID!
    total: Float!
    statut: StatutCommande!
  }
`;
```

---

## Références

- `references/schema-design.md` — SDL avancé, unions, interfaces, directives, scalars custom, schema versioning
- `references/performance.md` — DataLoader patterns avancés, query complexity, persisted queries, APQ, caching
- `references/federation.md` — Apollo Federation v2, supergraph, subgraphs, @key, @shareable, gateway config
- `references/case-studies.md` — 4 cas : migration REST→GraphQL, N+1 résolu, federation micro-services, client Apollo cache
