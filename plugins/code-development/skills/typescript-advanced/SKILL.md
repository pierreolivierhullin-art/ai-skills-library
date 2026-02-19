---
name: typescript-advanced
version: 1.0.0
description: >
  Advanced TypeScript, conditional types, mapped types, template literal types,
  infer keyword, branded types, type narrowing, discriminated unions, variance,
  generic constraints, declaration merging, module augmentation, utility types,
  TypeScript compiler API, strict mode configuration, tsconfig optimization,
  type-safe APIs, type guards, assertion functions, satisfies operator
---

# TypeScript Avancé — Système de Types Maîtrisé

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu modélises des domaines complexes avec des types précis et sûrs
- Tu écris des types génériques réutilisables ou des utilitaires de types
- Tu intègres des APIs externes en créant des types sûrs à partir de réponses JSON
- Tu as des erreurs TypeScript cryptiques ou des `any` implicites à éliminer
- Tu construis des librairies ou des frameworks internes avec des APIs bien typées
- Tu veux tirer parti du compilateur TypeScript pour détecter des bugs à la compilation

---

## Types Conditionnels

Les types conditionnels permettent une logique de branchement au niveau du système de types.

```typescript
// Syntaxe : T extends U ? X : Y
type IsString<T> = T extends string ? true : false;

type A = IsString<"hello">;  // true
type B = IsString<number>;   // false

// Cas d'usage : extraire le type de retour d'une fonction
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type Fn = () => { id: number; nom: string };
type Result = ReturnType<Fn>;  // { id: number; nom: string }

// Infer dans des positions complexes
type ElementType<T> = T extends (infer E)[] ? E : never;
type Num = ElementType<number[]>;  // number

// Unpromise : extraire le type résolu d'une Promise
type Awaited<T> = T extends Promise<infer R> ? Awaited<R> : T;
type Data = Awaited<Promise<Promise<string>>>;  // string
```

### Types Conditionnels Distributifs

```typescript
// Sur un union type, le conditionnel est appliqué à chaque membre
type ToArray<T> = T extends any ? T[] : never;

type StringOrNumber = ToArray<string | number>;
// = string[] | number[]  (pas (string | number)[])

// Éviter la distribution : envelopper dans un tuple
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;
type Both = ToArrayNonDist<string | number>;
// = (string | number)[]

// Utilitaire : exclure null et undefined
type NonNullable<T> = T extends null | undefined ? never : T;
type Safe = NonNullable<string | null | undefined>;  // string
```

---

## Mapped Types

```typescript
// Transformer toutes les propriétés d'un type
type Readonly<T> = { readonly [K in keyof T]: T[K] };
type Partial<T> = { [K in keyof T]?: T[K] };
type Required<T> = { [K in keyof T]-?: T[K] };  // -? retire l'optionnalité

// Record : créer un type avec des clés spécifiques
type Record<K extends keyof any, V> = { [P in K]: V };
type Permissions = Record<'lecture' | 'écriture' | 'suppression', boolean>;

// Remapper les clés avec as
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type Personne = { nom: string; age: number };
type GettersPersonne = Getters<Personne>;
// { getNom: () => string; getAge: () => number }

// Filtrer les propriétés par type
type PickByType<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K];
};

type MonObjet = { id: number; nom: string; actif: boolean; score: number };
type JustStrings = PickByType<MonObjet, string>;  // { nom: string }
type Numerics = PickByType<MonObjet, number>;     // { id: number; score: number }
```

---

## Template Literal Types

```typescript
// Combiner des types string littéraux
type Couleur = 'rouge' | 'vert' | 'bleu';
type Taille = 'petit' | 'moyen' | 'grand';

type Variante = `${Taille}-${Couleur}`;
// = "petit-rouge" | "petit-vert" | ... (9 combinaisons)

// Typer des clés d'événements
type EventName = 'clic' | 'survol' | 'soumission';
type Handlers = {
  [K in EventName as `on${Capitalize<K>}`]: (event: Event) => void;
};
// { onClic: ...; onSurvol: ...; onSoumission: ... }

// Parser des chaînes de route
type ExtractParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<`/${Rest}`>
    : T extends `${string}:${infer Param}`
    ? Param
    : never;

type Params = ExtractParams<'/users/:userId/posts/:postId'>;
// = "userId" | "postId"

// Typer une fonction de route sûre
function createRoute<Path extends string>(
  path: Path,
  handler: (params: Record<ExtractParams<Path>, string>) => void,
) { /* ... */ }

createRoute('/users/:id/posts/:slug', ({ id, slug }) => {
  // id et slug sont typés string, les autres clés sont des erreurs
});
```

---

## Branded Types (Types Nominaux)

TypeScript est structurellement typé : deux types avec la même structure sont interchangeables. Les branded types imposent une distinction nominale.

```typescript
// Pattern : brander un type primitif
declare const __brand: unique symbol;
type Brand<T, B> = T & { readonly [__brand]: B };

// Créer des types distincts à partir de string/number
type UserId = Brand<string, 'UserId'>;
type ProductId = Brand<string, 'ProductId'>;
type Euro = Brand<number, 'Euro'>;

// Fonctions de construction avec validation
function createUserId(id: string): UserId {
  if (!id.startsWith('usr_')) throw new Error('UserId invalide');
  return id as UserId;
}

function createProductId(id: string): ProductId {
  if (!id.startsWith('prd_')) throw new Error('ProductId invalide');
  return id as ProductId;
}

// Usage : les erreurs sont détectées à la compilation
function getUser(id: UserId): Promise<User> { /* ... */ }

const userId = createUserId('usr_123');
const productId = createProductId('prd_456');

getUser(userId);     // ✅
getUser(productId);  // ❌ Argument of type 'ProductId' is not assignable to 'UserId'

// Brand pour les montants financiers
function calculerTVA(montant: Euro): Euro {
  return (montant * 1.2) as Euro;
}

const prix = 100 as Euro;
calculerTVA(prix);  // ✅
calculerTVA(100);   // ❌ Type 'number' is not assignable to type 'Euro'
```

---

## Discriminated Unions et Narrowing

```typescript
// Union discriminée : un champ commun 'type' permet le narrowing
type EvenementPaiement =
  | { type: 'INITIE'; montant: number; devise: string }
  | { type: 'CONFIRME'; transactionId: string; montant: number }
  | { type: 'ECHEC'; raison: string; codeErreur: number }
  | { type: 'REMBOURSE'; transactionId: string; montantRembourse: number };

function traiterEvenement(evt: EvenementPaiement) {
  switch (evt.type) {
    case 'INITIE':
      console.log(`Paiement de ${evt.montant} ${evt.devise} initié`);
      break;
    case 'CONFIRME':
      console.log(`Transaction ${evt.transactionId} confirmée`);
      break;
    case 'ECHEC':
      console.error(`Échec ${evt.codeErreur}: ${evt.raison}`);
      break;
    case 'REMBOURSE':
      // evt.montantRembourse est available ici uniquement
      break;
    default:
      // Vérification d'exhaustivité
      const _exhaustif: never = evt;
  }
}

// Type Guards personnalisés
function estConfirme(evt: EvenementPaiement): evt is Extract<EvenementPaiement, { type: 'CONFIRME' }> {
  return evt.type === 'CONFIRME';
}

// Assertion function (TypeScript 3.7+)
function assertEvenementConfirme(
  evt: EvenementPaiement
): asserts evt is Extract<EvenementPaiement, { type: 'CONFIRME' }> {
  if (evt.type !== 'CONFIRME') {
    throw new Error(`Attendu CONFIRME, reçu ${evt.type}`);
  }
}
```

---

## Generics Avancés

### Contraintes et Inférence

```typescript
// Contraindre un generic à avoir certaines propriétés
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Generic avec valeur par défaut
type Container<T = string> = { valeur: T; timestamp: Date };

// Inférer depuis un tableau de clés
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  return keys.reduce((acc, key) => {
    acc[key] = obj[key];
    return acc;
  }, {} as Pick<T, K>);
}

const user = { id: 1, nom: 'Alice', email: 'alice@ex.com', role: 'admin' };
const publicUser = pick(user, ['id', 'nom']);  // { id: number; nom: string }

// Builder pattern type-safe
class QueryBuilder<T extends Record<string, unknown>> {
  private filters: Partial<T> = {};

  where<K extends keyof T>(key: K, value: T[K]): this {
    this.filters[key] = value;
    return this;
  }

  build(): Partial<T> {
    return this.filters;
  }
}

type UserQuery = QueryBuilder<{ id: number; email: string; actif: boolean }>;
const q = new QueryBuilder<typeof user>()
  .where('actif', true)
  // .where('actif', 'oui')  // ❌ Type 'string' is not assignable to 'boolean'
  .build();
```

---

## L'opérateur `satisfies`

Disponible depuis TypeScript 4.9, `satisfies` valide un type sans widening.

```typescript
type Palette = Record<string, string | [number, number, number]>;

// ❌ Avant satisfies : TypeScript élargit le type
const palette: Palette = {
  rouge: [255, 0, 0],
  vert: '#00ff00',
};
palette.rouge.toUpperCase();  // Erreur : T[K] est string | [number, number, number]

// ✅ Avec satisfies : le type exact est préservé
const paletteV2 = {
  rouge: [255, 0, 0],
  vert: '#00ff00',
} satisfies Palette;

paletteV2.rouge.map(v => v * 2);  // ✅ TypeScript sait que rouge est un tableau
paletteV2.vert.toUpperCase();     // ✅ TypeScript sait que vert est une string

// Cas d'usage : configuration validée
type Config = {
  port: number;
  host: string;
  debug: boolean;
};

export const config = {
  port: 3000,
  host: 'localhost',
  debug: process.env.NODE_ENV !== 'production',
} satisfies Config;
// config.port est number (pas number | string | boolean)
```

---

## Déclaration Merging et Module Augmentation

```typescript
// Augmenter un module existant (ex: Express Request)
// fichier : types/express.d.ts
declare global {
  namespace Express {
    interface Request {
      utilisateur?: {
        id: string;
        email: string;
        role: 'admin' | 'user';
      };
      requestId: string;
    }
  }
}

// Augmenter un module tiers
// fichier : types/environment.d.ts
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      NODE_ENV: 'development' | 'test' | 'production';
      DATABASE_URL: string;
      JWT_SECRET: string;
      PORT?: string;
    }
  }
}

// Usage : accès typé aux variables d'environnement
const port = parseInt(process.env.PORT ?? '3000', 10);
// process.env.DATABASE_URL est string (pas string | undefined)
```

---

## Configuration TypeScript Optimale

```json
// tsconfig.json
{
  "compilerOptions": {
    // Strictness maximale
    "strict": true,           // Active toutes les vérifications strictes
    "noUncheckedIndexedAccess": true,  // arr[0] est T | undefined (pas T)
    "exactOptionalPropertyTypes": true, // { a?: string } ≠ { a: string | undefined }
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,

    // Modules
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "esModuleInterop": true,

    // Émission
    "target": "ES2022",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,

    // Chemins
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src", "tests"],
  "exclude": ["node_modules", "dist"]
}
```

---

## Références

- `references/advanced-types.md` — Conditional types profonds, infer avancé, recursive types, variadic tuples
- `references/generics-patterns.md` — Builder pattern, Factory, variance covariant/contravariant, higher-kinded types
- `references/typescript-config.md` — tsconfig par environnement, project references, declaration files, compiler API
- `references/case-studies.md` — 4 cas : migration strict mode, API type-safe Zod, ORM type-safe, monorepo types partagés
