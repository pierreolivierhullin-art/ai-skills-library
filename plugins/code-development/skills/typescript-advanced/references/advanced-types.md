# Types Conditionnels Avancés et Récursifs

## Types conditionnels : distributifs vs non-distributifs

Un type conditionnel `T extends U ? X : Y` est **distributif** quand `T` est un type nu (bare type parameter). TypeScript distribue automatiquement l'union sur chaque membre.

```typescript
// Distributif : T est un type nu
type ToArray<T> = T extends unknown ? T[] : never;
type Result = ToArray<string | number>; // string[] | number[]

// Non-distributif : T est enveloppé dans un tuple
type ToArraySafe<T> = [T] extends [unknown] ? T[] : never;
type ResultSafe = ToArraySafe<string | number>; // (string | number)[]
```

Le wrapping en tuple `[T] extends [U]` est le pattern standard pour **bloquer la distribution**. Utile pour `IsUnion<T>` :

```typescript
type IsUnion<T, U = T> = T extends unknown
  ? ([U] extends [T] ? false : true)
  : never;

type A = IsUnion<string | number>; // true
type B = IsUnion<string>;          // false
type C = IsUnion<never>;           // never (cas particulier)

// IsNever fiable grâce au tuple
type IsNever<T> = [T] extends [never] ? true : false;
type D = IsNever<never>; // true
type E = IsNever<string>; // false
```

### Cas pratiques — filtrage de types dans une union

```typescript
// Extraire les types qui ont une propriété donnée
type WithProp<T, K extends PropertyKey, V = unknown> =
  T extends unknown
    ? K extends keyof T
      ? T[K] extends V ? T : never
      : never
    : never;

type Events =
  | { type: "click"; x: number; y: number }
  | { type: "keydown"; key: string }
  | { type: "resize"; width: number; height: number };

type MouseEvents = WithProp<Events, "x">; // { type: "click"; x: number; y: number }

// Supprimer les propriétés dont la valeur est never
type NonNeverProperties<T> = {
  [K in keyof T as T[K] extends never ? never : K]: T[K];
};
```

## `infer` dans des positions complexes

### Inférer les paramètres d'un constructeur

```typescript
type ConstructorArgs<T> =
  T extends new (...args: infer A) => unknown ? A : never;

class HttpClient {
  constructor(
    private baseUrl: string,
    private timeout: number,
    private headers: Record<string, string>
  ) {}
}

type HttpClientArgs = ConstructorArgs<typeof HttpClient>;
// [baseUrl: string, timeout: number, headers: Record<string, string>]

// Récupérer le premier argument uniquement
type FirstArg<T> =
  T extends new (first: infer F, ...rest: any[]) => unknown ? F : never;

type FirstParam = FirstArg<typeof HttpClient>; // string
```

### Inférer les types de valeurs d'un Record

```typescript
type ValueOf<T> = T extends Record<string, infer V> ? V : never;

const config = {
  api: "https://api.example.com",
  timeout: 5000,
  retries: 3,
} as const;

type ConfigValue = ValueOf<typeof config>; // string | number

// Inférer les clés d'un Record dont la valeur match un type
type KeysWithValue<T, V> = {
  [K in keyof T]: T[K] extends V ? K : never;
}[keyof T];

type StringKeys = KeysWithValue<typeof config, string>; // "api"
type NumberKeys = KeysWithValue<typeof config, number>; // "timeout" | "retries"
```

### Inférer des types depuis des tuples

```typescript
// Premier élément d'un tuple
type Head<T extends unknown[]> = T extends [infer H, ...unknown[]] ? H : never;

// Dernier élément d'un tuple
type Last<T extends unknown[]> = T extends [...unknown[], infer L] ? L : never;

// Tout sauf le premier (Tail)
type Tail<T extends unknown[]> = T extends [unknown, ...infer R] ? R : never;

// Longueur d'un tuple
type Length<T extends unknown[]> = T["length"];

type H = Head<[string, number, boolean]>; // string
type L = Last<[string, number, boolean]>; // boolean
type Ta = Tail<[string, number, boolean]>; // [number, boolean]
type Len = Length<[string, number, boolean]>; // 3

// Inférer le type de retour d'une Promise imbriquée
type UnwrapPromise<T> = T extends Promise<infer U> ? UnwrapPromise<U> : T;

type A = UnwrapPromise<Promise<Promise<string>>>; // string
```

## Types récursifs

### DeepPartial et DeepReadonly

```typescript
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

type DeepReadonly<T> = T extends (infer U)[]
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T;

type DeepRequired<T> = T extends object
  ? { [K in keyof T]-?: DeepRequired<T[K]> }
  : T;

// Usage pratique — configuration d'application
interface AppConfig {
  database: {
    host: string;
    port: number;
    credentials: {
      username: string;
      password: string;
    };
  };
  features: {
    darkMode: boolean;
    analytics: boolean;
  };
}

type PartialConfig = DeepPartial<AppConfig>;
// Toutes les propriétés sont optionnelles récursivement

function mergeConfig(
  base: AppConfig,
  overrides: DeepPartial<AppConfig>
): AppConfig {
  return JSON.parse(
    JSON.stringify({ ...base, ...overrides })
  ) as AppConfig;
}
```

### Flatten pour tableaux imbriqués

```typescript
type Flatten<T> = T extends (infer U)[] ? Flatten<U> : T;

type Nested = string[][][];
type Flat = Flatten<Nested>; // string

// Version avec profondeur limitée
type FlattenDepth<T, D extends number, A extends unknown[] = []> =
  A["length"] extends D
    ? T
    : T extends (infer U)[]
    ? FlattenDepth<U, D, [...A, unknown]>
    : T;

type Level2 = FlattenDepth<string[][][], 2>; // string[]
type Level3 = FlattenDepth<string[][][], 3>; // string
```

### DeepPick et DeepOmit

```typescript
// Récupérer un chemin imbriqué
type Get<T, K extends string> =
  K extends `${infer Head}.${infer Tail}`
    ? Head extends keyof T
      ? Get<T[Head], Tail>
      : never
    : K extends keyof T
    ? T[K]
    : never;

interface User {
  profile: {
    address: {
      city: string;
      country: string;
    };
    age: number;
  };
  email: string;
}

type City = Get<User, "profile.address.city">; // string
type Age  = Get<User, "profile.age">;          // number
```

## Variadic Tuple Types (TypeScript 4.0+)

```typescript
// Concat deux tuples
type Concat<T extends unknown[], U extends unknown[]> = [...T, ...U];

type AB = Concat<[string, number], [boolean, null]>;
// [string, number, boolean, null]

// Push un élément à la fin
type Push<T extends unknown[], E> = [...T, E];

// Pop le dernier élément
type Pop<T extends unknown[]> = T extends [...infer R, unknown] ? R : never;

// Prepend un élément au début
type Prepend<T extends unknown[], E> = [E, ...T];

type Pushed  = Push<[string, number], boolean>;  // [string, number, boolean]
type Popped  = Pop<[string, number, boolean]>;   // [string, number]
type Prepended = Prepend<[number, boolean], string>; // [string, number, boolean]
```

### Paramètres rest dans les tuples — fonctions type-safe

```typescript
// Inférer les arguments d'une fonction de façon précise
function call<T extends unknown[], R>(
  fn: (...args: T) => R,
  ...args: T
): R {
  return fn(...args);
}

function add(a: number, b: number): number {
  return a + b;
}

const result = call(add, 1, 2); // TypeScript sait que result: number
// call(add, 1, "2") — Erreur de compilation !

// ZipArgs : zipper deux listes de paramètres
type ZipArgs<T extends unknown[], U extends unknown[]> =
  T extends [infer TH, ...infer TR]
    ? U extends [infer UH, ...infer UR]
      ? [[TH, UH], ...ZipArgs<TR, UR>]
      : []
    : [];

type Zipped = ZipArgs<[string, number], [boolean, null]>;
// [[string, boolean], [number, null]]
```

## Template Literal Types avancés

### Split et Join

```typescript
type Split<S extends string, D extends string> =
  S extends `${infer Head}${D}${infer Tail}`
    ? [Head, ...Split<Tail, D>]
    : [S];

type Join<T extends string[], D extends string> =
  T extends [infer F extends string, ...infer R extends string[]]
    ? R extends []
      ? F
      : `${F}${D}${Join<R, D>}`
    : "";

type Parts = Split<"a.b.c.d", ".">;     // ["a", "b", "c", "d"]
type Joined = Join<["a", "b", "c"], "-">; // "a-b-c"
```

### KebabCase et CamelCase

```typescript
type KebabCase<S extends string> =
  S extends `${infer Head}${infer Tail}`
    ? Head extends Uppercase<Head>
      ? Head extends Lowercase<Head>
        ? `${Head}${KebabCase<Tail>}`
        : `-${Lowercase<Head>}${KebabCase<Tail>}`
      : `${Head}${KebabCase<Tail>}`
    : S;

type CamelCase<S extends string> =
  S extends `${infer Head}-${infer Tail}`
    ? `${Head}${Capitalize<CamelCase<Tail>>}`
    : S;

type K1 = KebabCase<"getUserProfile">;     // "get-user-profile"
type K2 = CamelCase<"get-user-profile">;   // "getUserProfile"
```

### Paths — chemins d'objets imbriqués

```typescript
type Paths<T, Prefix extends string = ""> =
  T extends object
    ? {
        [K in keyof T & string]:
          | `${Prefix}${K}`
          | Paths<T[K], `${Prefix}${K}.`>;
      }[keyof T & string]
    : never;

type UserPaths = Paths<User>;
// "profile" | "profile.address" | "profile.address.city"
// | "profile.address.country" | "profile.age" | "email"

// Utilisation : fonction get type-safe
function getPath<T, P extends Paths<T>>(obj: T, path: P): Get<T, P> {
  return path.split(".").reduce((acc, key) => (acc as any)[key], obj) as Get<T, P>;
}

const user: User = {
  profile: { address: { city: "Paris", country: "France" }, age: 30 },
  email: "alice@example.com",
};

const city = getPath(user, "profile.address.city"); // type: string
```

## Extract, Exclude, NonNullable — implémentations from scratch

```typescript
// Extract<T, U> — garder les membres de T assignables à U
type MyExtract<T, U> = T extends U ? T : never;

// Exclude<T, U> — supprimer les membres de T assignables à U
type MyExclude<T, U> = T extends U ? never : T;

// NonNullable<T> — supprimer null et undefined
type MyNonNullable<T> = T extends null | undefined ? never : T;

type E1 = MyExtract<"a" | "b" | "c", "a" | "c">;   // "a" | "c"
type E2 = MyExclude<"a" | "b" | "c", "a" | "c">;   // "b"
type E3 = MyNonNullable<string | null | undefined>;  // string

// Différence symétrique entre deux unions
type SymDiff<T, U> = MyExclude<T, U> | MyExclude<U, T>;
type SD = SymDiff<"a" | "b" | "c", "b" | "c" | "d">; // "a" | "d"
```

## Utility types de fonctions avancés

```typescript
// Parameters, ConstructorParameters, InstanceType, ReturnType
function createUser(name: string, age: number, role: "admin" | "user") {
  return { name, age, role, createdAt: new Date() };
}

type CreateUserParams  = Parameters<typeof createUser>;
// [name: string, age: number, role: "admin" | "user"]

type CreateUserReturn  = ReturnType<typeof createUser>;
// { name: string; age: number; role: "admin" | "user"; createdAt: Date }

class UserRepository {
  constructor(private db: Database, private logger: Logger) {}
}

type RepoArgs     = ConstructorParameters<typeof UserRepository>;
// [db: Database, logger: Logger]

type RepoInstance = InstanceType<typeof UserRepository>;
// UserRepository

// ThisParameterType — extraire le type de `this`
function greet(this: { name: string }, greeting: string): string {
  return `${greeting}, ${this.name}!`;
}

type ThisType = ThisParameterType<typeof greet>;   // { name: string }
type WithoutThis = OmitThisParameter<typeof greet>; // (greeting: string) => string
```

### Types de fonctions avancés — surcharges et this

```typescript
// Surcharges pour comportements différents selon le type d'entrée
function process(input: string): string[];
function process(input: number): number;
function process(input: string | number): string[] | number {
  if (typeof input === "string") return input.split("");
  return input * 2;
}

const r1 = process("hello"); // string[]
const r2 = process(42);      // number

// Paramètre `this` explicite
interface Collection<T> {
  items: T[];
  add(this: Collection<T>, item: T): this;
  filter(this: Collection<T>, predicate: (item: T) => boolean): Collection<T>;
}
```

## Limites du système de types et contournements

### Récursion trop profonde

TypeScript limite la récursion de types (généralement ~50 niveaux). Contournements :

```typescript
// Approche naïve — peut dépasser la limite
type DeepReadonlyNaive<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonlyNaive<T[K]> : T[K];
};

// Contournement 1 : lazy evaluation avec interface
interface DeepReadonlyArray<T> extends ReadonlyArray<DeepReadonlyObject<T>> {}
type DeepReadonlyObject<T> = {
  readonly [K in keyof T]: T[K] extends (infer U)[]
    ? DeepReadonlyArray<U>
    : T[K] extends object
    ? DeepReadonlyObject<T[K]>
    : T[K];
};

// Contournement 2 : limiter la profondeur explicitement
type Depth = [never, 0, 1, 2, 3, 4, 5];

type DeepPartialLimited<T, D extends number = 5> =
  [D] extends [0]
    ? T
    : T extends object
    ? { [K in keyof T]?: DeepPartialLimited<T[K], Depth[D]> }
    : T;
```

### Types circulaires

```typescript
// Les types circulaires directs ne sont pas autorisés
// type Circular = Circular[]; // Erreur !

// Solution : utiliser une interface
interface TreeNode<T> {
  value: T;
  children: TreeNode<T>[]; // OK avec une interface
}

// JSON type récursif
type JSONValue =
  | string
  | number
  | boolean
  | null
  | JSONValue[]
  | { [key: string]: JSONValue };
```

## Tableau récapitulatif — utility types intrinsèques

| Type utilitaire | Description | Exemple |
|---|---|---|
| `Partial<T>` | Toutes propriétés optionnelles | `Partial<User>` |
| `Required<T>` | Toutes propriétés obligatoires | `Required<Config>` |
| `Readonly<T>` | Toutes propriétés en lecture seule | `Readonly<State>` |
| `Record<K, V>` | Objet avec clés K et valeurs V | `Record<string, number>` |
| `Pick<T, K>` | Sous-ensemble de propriétés | `Pick<User, "id" \| "name">` |
| `Omit<T, K>` | Exclure des propriétés | `Omit<User, "password">` |
| `Exclude<T, U>` | Exclure membres d'une union | `Exclude<A \| B, B>` |
| `Extract<T, U>` | Garder membres d'une union | `Extract<A \| B, B>` |
| `NonNullable<T>` | Supprimer null/undefined | `NonNullable<string \| null>` |
| `Parameters<T>` | Types des paramètres | `Parameters<typeof fn>` |
| `ReturnType<T>` | Type de retour | `ReturnType<typeof fn>` |
| `InstanceType<T>` | Type de l'instance | `InstanceType<typeof Cls>` |
| `Awaited<T>` | Dépliage des Promises | `Awaited<Promise<string>>` |

## Points clés à retenir

- Wrapper dans un tuple `[T]` bloque la distribution des types conditionnels
- `infer` peut apparaître dans n'importe quelle position covariante ou contravariante
- Les types récursifs requièrent une interface intermédiaire pour les types circulaires
- Les Variadic Tuple Types permettent de manipuler les tuples comme des listes de longueur fixe
- Les Template Literal Types permettent un typage fin des chaînes de caractères
- La récursion est limitée : utiliser des compteurs de profondeur ou des interfaces pour contourner
