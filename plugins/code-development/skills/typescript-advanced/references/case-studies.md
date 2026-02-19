# Études de Cas — TypeScript Avancé en Production

## Cas 1 — Migration strict mode dans une fintech (80 000 lignes)

### Contexte

Application React/Node.js développée pendant 4 ans dans une fintech de taille moyenne. TypeScript 3.x configuré avec `strict: false`, accumulation de technical debt : environ 847 utilisations de `any` comptabilisées, des `as unknown as X` à chaque coin du code, et `// @ts-ignore` disséminés partout. L'équipe hésitait à refactoriser les modules critiques faute de confiance dans les types.

### Problème

Trois bugs en production consécutifs causés par des `undefined` non gérés :

- Un montant affiché comme `NaN` dans un récapitulatif de transaction (`undefined + 100`)
- Un crash silencieux sur une propriété d'utilisateur optionnelle lue sans vérification
- Une liste de paiements rendue vide car une propriété `items` retournait `undefined` au lieu de `[]`

Le refactoring était considéré comme dangereux : personne n'osait toucher les modules centraux car les types ne reflétaient pas la réalité.

### Solution — migration progressive

La stratégie adoptée : activer `strict` par fichier grâce à `@ts-strict-ignore`, puis réduire progressivement les `any` sur 6 semaines.

**Étape 1 — outillage de mesure**

```typescript
// scripts/count-any.ts — compter les any dans la codebase
import { Project } from "ts-morph";

const project = new Project({ tsConfigFilePath: "./tsconfig.json" });

let totalAny = 0;
const byFile: Record<string, number> = {};

project.getSourceFiles().forEach((file) => {
  const count = file.getDescendantsOfKind(
    SyntaxKind.AnyKeyword
  ).length;
  if (count > 0) {
    byFile[file.getFilePath()] = count;
    totalAny += count;
  }
});

console.log(`Total any : ${totalAny}`);
console.table(
  Object.entries(byFile)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 20)
    .map(([file, count]) => ({ file: file.split("/src/")[1], count }))
);
```

**Étape 2 — marquer les anciens fichiers avec @ts-strict-ignore**

```bash
# Installer ts-strict-ignore
npm install -D ts-strict-ignore

# Ajouter automatiquement le commentaire sur tous les fichiers existants
npx ts-strict-ignore --path ./src
```

```typescript
// src/services/payment.service.ts (avant migration — marqué automatiquement)
// @ts-strict-ignore
export class PaymentService {
  processPayment(amount: any, userId: any): any {
    // ...
  }
}

// src/services/user.service.ts (nouveau fichier — strict dès le début)
// Pas de @ts-strict-ignore ici
export class UserService {
  async findById(id: number): Promise<User | null> {
    const result = await this.db.query<User>(
      "SELECT * FROM users WHERE id = $1",
      [id]
    );
    return result.rows[0] ?? null; // undefined géré explicitement
  }
}
```

**Étape 3 — activation de strict dans tsconfig**

```json
{
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": true,
    "noImplicitAny": true,
    "plugins": [{ "name": "ts-strict-ignore" }]
  }
}
```

**Étape 4 — migration des fichiers critiques un par un**

```typescript
// Avant — PaymentService avec any
// @ts-strict-ignore
class PaymentServiceLegacy {
  async charge(data: any): any {
    const amount = data.amount; // Peut être undefined — bug #1
    return this.stripe.charge(amount * 100);
  }
}

// Après — types précis
interface ChargeInput {
  amount: number;
  currency: "EUR" | "USD" | "GBP";
  customerId: string;
  description?: string;
}

interface ChargeResult {
  chargeId: string;
  status: "succeeded" | "pending" | "failed";
  processedAt: Date;
}

class PaymentService {
  async charge(data: ChargeInput): Promise<ChargeResult> {
    // TypeScript garantit que data.amount est un number
    const amountInCents = Math.round(data.amount * 100);
    const charge = await this.stripe.charge({
      amount: amountInCents,
      currency: data.currency,
      customer: data.customerId,
    });
    return {
      chargeId: charge.id,
      status: charge.status,
      processedAt: new Date(),
    };
  }
}
```

**Étape 5 — activer noUncheckedIndexedAccess en dernier**

```typescript
// noUncheckedIndexedAccess : les accès par index renvoient T | undefined
// Migration des accès tableau

// Avant
const firstTransaction = transactions[0];
const amount = firstTransaction.amount; // Crash si tableau vide !

// Après
const firstTransaction = transactions[0];
if (firstTransaction === undefined) {
  return { total: 0, transactions: [] };
}
const amount = firstTransaction.amount; // Sûr

// Pattern helper
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

function firstOrThrow<T>(arr: T[], context: string): T {
  const item = arr[0];
  if (item === undefined) throw new Error(`Tableau vide : ${context}`);
  return item;
}
```

### Métriques

| Métrique | Avant | Après | Évolution |
|---|---|---|---|
| Occurrences de `any` | 847 | 12 | -98.6% |
| Bugs undefined en prod | 3 en 6 mois | 0 en 6 mois | -100% |
| `@ts-ignore` / `@ts-expect-error` | 43 | 5 | -88% |
| Couverture de types (estimée) | ~60% | ~97% | +37pp |
| Durée de migration | — | 6 semaines | — |

### Leçon clé

Activer `strict` directement sur 80 000 lignes de code est impossible — des milliers d'erreurs paralysent l'équipe. La stratégie `@ts-strict-ignore` sur les anciens fichiers et `strict` sur les nouveaux permet une migration incrémentale sans bloquer le développement. Activer `noUncheckedIndexedAccess` en tout dernier, une fois que le reste est stabilisé.

---

## Cas 2 — API type-safe avec Zod + tRPC dans un SaaS B2B

### Contexte

SaaS B2B avec 5 développeurs (2 backend, 2 frontend, 1 fullstack). Architecture REST classique : Express côté serveur, React Query côté client. Les types étaient définis deux fois : une fois en Zod pour la validation backend, une fois en interface TypeScript côté frontend.

### Problème

Les types backend et frontend dérivaient. Un champ `createdAt` retourné comme `string` (sérialisation JSON) était typé comme `Date` côté frontend — cause de crashes intermittents. Un champ optionnel ajouté en backend n'était pas mis à jour dans les 3 interfaces frontend correspondantes. Deux développeurs avaient introduit des bugs de validation en ajoutant un champ côté client sans mettre à jour la validation Zod backend.

```typescript
// Backend — avant tRPC
// routes/users.ts
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
  role: z.enum(["admin", "member"]),
});

app.post("/users", validateBody(createUserSchema), async (req, res) => {
  const user = await userService.create(req.body);
  res.json(user);
});

// Frontend — types dupliqués et divergents
// types/user.ts
interface CreateUserInput {
  email: string;
  name: string;
  role: "admin" | "member" | "owner"; // "owner" ajouté ici mais pas dans le schema !
}

interface User {
  id: number;
  email: string;
  name: string;
  role: "admin" | "member";
  createdAt: Date; // Erreur — JSON serialise en string, pas Date
}
```

### Solution — tRPC avec Zod comme source de vérité unique

```typescript
// packages/api/src/schemas/user.schema.ts — source de vérité unique
import { z } from "zod";

export const CreateUserSchema = z.object({
  email: z.string().email("Email invalide"),
  name: z.string().min(2, "Nom trop court").max(100),
  role: z.enum(["admin", "member"]),
});

export const UpdateUserSchema = CreateUserSchema.partial().omit({ email: true });

export const UserSchema = z.object({
  id: z.number().int().positive(),
  email: z.string().email(),
  name: z.string(),
  role: z.enum(["admin", "member"]),
  createdAt: z.string().datetime(), // string ISO — honnête sur la sérialisation JSON
  updatedAt: z.string().datetime(),
});

// Types inférés automatiquement depuis le schema
export type CreateUserInput = z.infer<typeof CreateUserSchema>;
export type UpdateUserInput = z.infer<typeof UpdateUserSchema>;
export type User = z.infer<typeof UserSchema>;
```

```typescript
// packages/api/src/router/user.router.ts — tRPC router
import { router, protectedProcedure, publicProcedure } from "../trpc";
import { CreateUserSchema, UpdateUserSchema, UserSchema } from "../schemas/user.schema";
import { z } from "zod";

export const userRouter = router({
  // Lister les utilisateurs — pagination type-safe
  list: protectedProcedure
    .input(
      z.object({
        page: z.number().int().min(1).default(1),
        perPage: z.number().int().min(1).max(100).default(20),
        search: z.string().optional(),
      })
    )
    .output(
      z.object({
        users: UserSchema.array(),
        total: z.number(),
        hasNextPage: z.boolean(),
      })
    )
    .query(async ({ input, ctx }) => {
      const { page, perPage, search } = input;
      const offset = (page - 1) * perPage;

      const [users, total] = await Promise.all([
        ctx.db.user.findMany({
          skip: offset,
          take: perPage,
          where: search ? { OR: [
            { name: { contains: search } },
            { email: { contains: search } },
          ]} : undefined,
        }),
        ctx.db.user.count(),
      ]);

      return {
        users,
        total,
        hasNextPage: offset + perPage < total,
      };
    }),

  // Créer un utilisateur
  create: protectedProcedure
    .input(CreateUserSchema)
    .output(UserSchema)
    .mutation(async ({ input, ctx }) => {
      const user = await ctx.db.user.create({ data: input });
      return user;
    }),

  // Mettre à jour
  update: protectedProcedure
    .input(z.object({ id: z.number(), data: UpdateUserSchema }))
    .output(UserSchema)
    .mutation(async ({ input, ctx }) => {
      const user = await ctx.db.user.update({
        where: { id: input.id },
        data: input.data,
      });
      return user;
    }),
});
```

```typescript
// apps/web/src/hooks/useUsers.ts — côté frontend, types inférés automatiquement
import { trpc } from "../lib/trpc";

export function useUsers(page: number, search?: string) {
  const query = trpc.user.list.useQuery(
    { page, perPage: 20, search },
    { keepPreviousData: true }
  );

  // query.data est automatiquement typé :
  // { users: User[]; total: number; hasNextPage: boolean } | undefined
  return {
    users: query.data?.users ?? [],
    total: query.data?.total ?? 0,
    isLoading: query.isLoading,
  };
}

// Plus aucun type manuel côté frontend — tout vient du schema Zod
```

### Métriques

| Métrique | Avant | Après | Évolution |
|---|---|---|---|
| Fichiers de types dupliqués | 23 | 0 | -100% |
| Erreurs runtime liées aux types | 8 en 3 mois | 0 en 3 mois | -100% |
| Lignes de code de validation | ~1 200 | ~720 | -40% |
| Temps d'onboarding d'un dev | 2 semaines | 1 semaine | -50% |
| Bugs détectés avant PR merge | 12 | 31 | +158% |

### Leçon clé

Zod + tRPC crée une **source de vérité unique** pour les types et la validation runtime. Le schema Zod est définitif : plus aucun écart possible entre ce que le backend valide et ce que le frontend attend. `z.infer<typeof schema>` génère les types TypeScript sans duplication — ajouter un champ dans le schema le propage automatiquement aux deux côtés.

---

## Cas 3 — ORM type-safe et Branded IDs dans un e-commerce

### Contexte

Application e-commerce avec Prisma comme ORM. Les IDs de toutes les entités (User, Product, Order, Cart, Address) étaient des `number` simples. Les fonctions prenaient des `number` en paramètre sans distinction d'entité.

### Problème

Bug en production : une fonction de recommandation passait un `productId` là où un `userId` était attendu. Les données affichées dans les recommandations étaient incohérentes pendant 48 heures avant détection. Le bug était invisible à la compilation — les deux étaient des `number`.

```typescript
// Avant — IDs non typés, confusion possible
async function getRecommendations(userId: number): Promise<Product[]> {
  const orders = await getOrdersByUser(userId);
  return computeRecommendations(orders);
}

// Bug : productId passé à la place de userId — aucune erreur TypeScript
const recommendations = await getRecommendations(product.id); // Silencieux !
```

### Solution — Branded IDs générés depuis Prisma

```typescript
// packages/types/src/branded.ts — définition des brands
declare const __brand: unique symbol;
type Brand<T, B extends string> = T & { readonly [__brand]: B };

// IDs brandés pour chaque entité
export type UserId    = Brand<number, "UserId">;
export type ProductId = Brand<number, "ProductId">;
export type OrderId   = Brand<number, "OrderId">;
export type CartId    = Brand<number, "CartId">;
export type AddressId = Brand<number, "AddressId">;

// Constructeurs — le seul moyen de créer un ID brandé
export const UserId    = (n: number): UserId    => n as UserId;
export const ProductId = (n: number): ProductId => n as ProductId;
export const OrderId   = (n: number): OrderId   => n as OrderId;
export const CartId    = (n: number): CartId    => n as CartId;
export const AddressId = (n: number): AddressId => n as AddressId;

// Utility type générique
type BrandedId<Entity extends string> = Brand<number, Entity>;
```

```typescript
// Extension Prisma — retourner des IDs brandés automatiquement
// lib/prisma-extension.ts
import { Prisma } from "@prisma/client";
import { UserId, ProductId, OrderId } from "@app/types";

export const brandedIdsExtension = Prisma.defineExtension({
  result: {
    user: {
      id: {
        needs: { id: true },
        compute(user) { return UserId(user.id); },
      },
    },
    product: {
      id: {
        needs: { id: true },
        compute(product) { return ProductId(product.id); },
      },
    },
    order: {
      id: {
        needs: { id: true },
        compute(order) { return OrderId(order.id); },
      },
    },
  },
});

export const prisma = new PrismaClient().$extends(brandedIdsExtension);
```

```typescript
// services/recommendation.service.ts — après migration
import { UserId, ProductId } from "@app/types";

// Signature précise — impossible de passer le mauvais ID
async function getOrdersByUser(userId: UserId): Promise<Order[]> {
  return prisma.order.findMany({
    where: { userId }, // prisma accepte UserId car l'extension le retourne
  });
}

async function getProductById(productId: ProductId): Promise<Product | null> {
  return prisma.product.findUnique({ where: { id: productId } });
}

async function getRecommendations(userId: UserId): Promise<Product[]> {
  const orders = await getOrdersByUser(userId);
  return computeRecommendations(orders);
}

// Maintenant le bug est détecté à la compilation :
const product = await getProductById(ProductId(42));
// getRecommendations(product.id); // Erreur ! ProductId !== UserId
getRecommendations(UserId(1));      // OK
```

```typescript
// Script de migration — mettre à jour 50+ signatures de fonctions
// scripts/migrate-ids.ts
import { Project, SyntaxKind } from "ts-morph";

const project = new Project({ tsConfigFilePath: "./tsconfig.json" });

// Patterns à migrer : (userId: number) → (userId: UserId)
const patterns: Array<{ param: RegExp; newType: string }> = [
  { param: /userId/,    newType: "UserId" },
  { param: /productId/, newType: "ProductId" },
  { param: /orderId/,   newType: "OrderId" },
  { param: /cartId/,    newType: "CartId" },
  { param: /addressId/, newType: "AddressId" },
];

project.getSourceFiles("src/**/*.ts").forEach((file) => {
  file.getFunctions().forEach((fn) => {
    fn.getParameters().forEach((param) => {
      const name = param.getName();
      const typeNode = param.getTypeNode();

      if (typeNode?.getText() !== "number") return;

      for (const pattern of patterns) {
        if (pattern.param.test(name)) {
          param.setType(pattern.newType);
          // Ajouter l'import si nécessaire
          const importDecl = file.getImportDeclaration("@app/types");
          if (!importDecl) {
            file.addImportDeclaration({
              moduleSpecifier: "@app/types",
              namedImports: [pattern.newType],
            });
          }
          break;
        }
      }
    });
  });
});

project.saveSync();
console.log("Migration terminée.");
```

### Métriques

| Métrique | Avant | Après | Évolution |
|---|---|---|---|
| Bugs de confusion d'IDs en prod | 3 en 6 mois | 0 | -100% |
| Détection de confusion d'IDs | Runtime | Compilation | Immédiat |
| Durée de migration | — | 3 jours | — |
| Fonctions migrées | — | 67 | — |
| Temps moyen de PR review | 45 min | 32 min | -30% |

### Leçon clé

Les branded types sur les IDs d'entités offrent le **ROI TypeScript le plus élevé** pour tout projet avec plusieurs entités. Un seul bug d'ID en production peut coûter des heures de debugging. La migration est quasi-automatisable avec ts-morph et l'extension Prisma intègre les brands sans modifier le code métier. Le coût : 3 jours de migration pour une protection permanente.

---

## Cas 4 — Types partagés dans un monorepo (startup 8 développeurs)

### Contexte

Startup en croissance avec 3 applications : une web app React, une app mobile React Native, et une API Node.js. Architecture monorepo Turborepo avec 8 développeurs. Le projet avait 2 ans et n'avait jamais formalisé les types partagés.

### Problème

Audit de la codebase avant un recrutement technique :

- 12 définitions différentes du type `User` dans le codebase (parfois avec des champs contradictoires)
- Les `Date` sérialisées en JSON côté API arrivaient comme `string` côté client — typées `Date` par convention mais jamais vérifiées
- Les montants financiers : certains modules utilisaient des centimes (entiers), d'autres des euros (flottants) — source de bugs d'affichage et de calcul
- Un développeur mobile avait un `User` avec `fullName`, le développeur web utilisait `firstName + lastName`

### Solution — packages de types canoniques

```
packages/
├── @app/types/          # Types TypeScript canoniques
│   ├── src/
│   │   ├── entities/    # User, Product, Order
│   │   ├── money/       # Types monétaires
│   │   └── index.ts
│   └── package.json
├── @app/schemas/        # Schemas Zod (source de vérité + types)
│   ├── src/
│   │   ├── user.schema.ts
│   │   ├── product.schema.ts
│   │   └── index.ts
│   └── package.json
└── @app/config/         # Configuration partagée avec satisfies
    ├── src/
    │   └── index.ts
    └── package.json
```

```typescript
// packages/@app/types/src/entities/user.ts — type User canonique
// Utilisation de z.infer pour garantir la cohérence avec le schema Zod
import type { z } from "zod";
import type { UserSchema, UserRoleSchema } from "@app/schemas";

// Types dérivés du schema Zod — source de vérité unique
export type User = z.infer<typeof UserSchema>;
export type UserRole = z.infer<typeof UserRoleSchema>;

// Sous-types utiles
export type PublicUser = Omit<User, "passwordHash" | "internalNotes">;
export type UserSummary = Pick<User, "id" | "firstName" | "lastName" | "email" | "role">;
```

```typescript
// packages/@app/schemas/src/user.schema.ts — schema Zod canonique
import { z } from "zod";

export const UserRoleSchema = z.enum(["admin", "member", "viewer"]);

export const UserSchema = z.object({
  id: z.number().int().positive(),
  email: z.string().email(),
  firstName: z.string().min(1).max(100),   // Décision : firstName + lastName, pas fullName
  lastName: z.string().min(1).max(100),
  role: UserRoleSchema,
  // Dates : string ISO pour être honnête sur la sérialisation JSON
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
});

// Helpers pour transformer les données à la frontière
export function parseUser(raw: unknown): User {
  return UserSchema.parse(raw);
}

export function safeParseUser(raw: unknown) {
  return UserSchema.safeParse(raw);
}
```

```typescript
// packages/@app/types/src/money/index.ts — types monétaires précis
declare const __brand: unique symbol;
type Brand<T, B extends string> = T & { readonly [__brand]: B };

// Deux representations distinctes — jamais interchangeables
export type EuroAmount  = Brand<number, "EuroAmount">;   // 12.50 — affichage
export type CentAmount  = Brand<number, "CentAmount">;   // 1250  — calcul/stockage

// Constructeurs
export const euro  = (n: number): EuroAmount => n as EuroAmount;
export const cents = (n: number): CentAmount => n as CentAmount;

// Conversions explicites
export function eurosToCents(e: EuroAmount): CentAmount {
  return Math.round(e * 100) as CentAmount;
}

export function centsToEuros(c: CentAmount): EuroAmount {
  return (c / 100) as EuroAmount;
}

// Opérations sur les cents (pour les calculs financiers)
export function addCents(a: CentAmount, b: CentAmount): CentAmount {
  return (a + b) as CentAmount;
}

export function subtractCents(a: CentAmount, b: CentAmount): CentAmount {
  return (a - b) as CentAmount;
}

// Formatage — prend toujours EuroAmount
export function formatPrice(
  amount: EuroAmount,
  locale = "fr-FR",
  currency = "EUR"
): string {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
  }).format(amount);
}
```

```typescript
// packages/@app/types/src/index.ts — barrel export
export type { User, PublicUser, UserSummary, UserRole } from "./entities/user";
export type { Product, ProductSummary } from "./entities/product";
export type { Order, OrderStatus } from "./entities/order";
export type { EuroAmount, CentAmount } from "./money";
export { euro, cents, eurosToCents, centsToEuros, addCents, formatPrice } from "./money";
```

```typescript
// packages/@app/config/src/index.ts — configuration partagée avec satisfies
import type { AppEnvironment } from "@app/types";

// satisfies valide la config sans perdre le type littéral
const appConfig = {
  environments: {
    development: {
      apiUrl: "http://localhost:3000",
      featureFlags: { darkMode: true, betaFeatures: true },
    },
    staging: {
      apiUrl: "https://staging-api.app.com",
      featureFlags: { darkMode: true, betaFeatures: false },
    },
    production: {
      apiUrl: "https://api.app.com",
      featureFlags: { darkMode: false, betaFeatures: false },
    },
  },
} satisfies Record<string, Record<string, AppEnvironment>>;

// TypeScript connaît le type exact (pas juste Record<string, AppEnvironment>)
type Envs = keyof typeof appConfig.environments;
// "development" | "staging" | "production" — type littéral préservé par satisfies
```

```typescript
// Exemple d'usage cohérent dans les 3 apps
// apps/web/src/components/UserCard.tsx
import type { PublicUser } from "@app/types";
import { formatPrice } from "@app/types";

interface UserCardProps {
  user: PublicUser; // Type canonique — toujours firstName + lastName
  balance: CentAmount; // Toujours en centimes côté données
}

export function UserCard({ user, balance }: UserCardProps) {
  const displayBalance = centsToEuros(balance); // Conversion explicite pour l'affichage
  return (
    <div>
      <h2>{user.firstName} {user.lastName}</h2>
      <p>{formatPrice(displayBalance)}</p>
    </div>
  );
}
```

### Métriques

| Métrique | Avant | Après | Évolution |
|---|---|---|---|
| Définitions du type `User` | 12 | 1 | -92% |
| Bugs de sérialisation Date | 4 en 6 mois | 0 en 8 mois | -100% |
| Bugs montants (€ vs centimes) | 2 en 6 mois | 0 en 8 mois | -100% |
| Temps d'onboarding | 3 semaines | 1.5 semaine | -50% |
| Lignes de types dupliquées | ~2 400 | ~800 | -67% |
| Confiance au refactoring (score équipe) | 3/10 | 8/10 | +167% |

### Leçon clé

Investir dans les types partagés **dès la phase de croissance** (pas au démarrage, mais avant que la duplication devienne incontrôlable) économise des semaines de débogage. Les points d'attention : être honnête sur la sérialisation JSON (ne pas typer `Date` ce qui est `string`), utiliser `satisfies` pour préserver les types littéraux dans les configs, et encoder les distinctions métier (euros vs centimes) dans le système de types plutôt que dans la documentation.

---

## Synthèse — patterns récurrents dans les 4 cas

| Pattern | Cas 1 | Cas 2 | Cas 3 | Cas 4 | ROI |
|---|:---:|:---:|:---:|:---:|---|
| Migration progressive strict | X | | | | Élevé — risque maîtrisé |
| Zod comme source de vérité | | X | | X | Très élevé — fin de la duplication |
| Branded types sur primitives | | | X | X | Très élevé — bugs éliminés à la compilation |
| `satisfies` pour les configs | | | | X | Moyen — DX améliorée |
| ts-morph pour la migration | X | | X | | Élevé — automation des migrations |
| Monorepo avec packages partagés | | X | | X | Très élevé — cohérence garantie |

Les 4 cas partagent un fil directeur : **faire confiance au compilateur plutôt qu'à la discipline humaine**. Quand TypeScript peut détecter un bug à la compilation, il le détectera toujours. Quand on compte sur les développeurs pour ne pas mélanger des IDs, ils finissent par le faire.
