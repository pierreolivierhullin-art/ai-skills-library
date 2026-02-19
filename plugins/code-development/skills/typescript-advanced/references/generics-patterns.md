# Generics Avancés — Patterns et Variance

## Variance en TypeScript : covariant, contravariant, invariant, bivariant

La variance décrit comment les relations de sous-typage se propagent à travers les types génériques. Comprendre la variance évite des erreurs subtiles au runtime.

### Positions covariantes — les retours de fonctions

Une position est **covariante** si `A extends B` implique `F<A> extends F<B>`. Les types de retour et les propriétés en lecture seule sont covariants.

```typescript
// Covariant : () => T
type Producer<T> = () => T;

// Si Dog extends Animal, alors Producer<Dog> extends Producer<Animal>
interface Animal { name: string }
interface Dog extends Animal { breed: string }

const dogProducer: Producer<Dog> = () => ({ name: "Rex", breed: "Labrador" });
const animalProducer: Producer<Animal> = dogProducer; // OK — covariant

// ReadonlyArray est covariant
const dogs: ReadonlyArray<Dog> = [{ name: "Rex", breed: "Labrador" }];
const animals: ReadonlyArray<Animal> = dogs; // OK — covariant
```

### Positions contravariantes — les paramètres de fonctions

Une position est **contravariante** si `A extends B` implique `F<B> extends F<A>`. Les paramètres de fonctions sont contravariants.

```typescript
// Contravariant : (x: T) => void
type Consumer<T> = (item: T) => void;

// Si Dog extends Animal, alors Consumer<Animal> extends Consumer<Dog>
const animalConsumer: Consumer<Animal> = (a) => console.log(a.name);
const dogConsumer: Consumer<Dog> = animalConsumer; // OK — contravariant

// L'inverse échoue correctement
const specificDogConsumer: Consumer<Dog> = (d) => console.log(d.breed);
// const willFail: Consumer<Animal> = specificDogConsumer; // Erreur TypeScript !
```

### Positions invariantes — Array mutable

Une position est **invariante** si ni covariant ni contravariant ne s'applique. Les tableaux mutables sont invariants car on peut lire ET écrire.

```typescript
// Array<T> est invariant
const dogArray: Array<Dog> = [];
// const animalArray: Array<Animal> = dogArray; // Erreur !
// Sinon on pourrait faire : animalArray.push({ name: "Cat" }) — corrompt dogArray

// Invariance explicite avec -/+ variance annotations (TypeScript 4.7+)
type InvariantBox<T> = {
  get(): T;    // covariant
  set(v: T): void; // contravariant
};
// Combiné → invariant
```

### strictFunctionTypes et son impact

```typescript
// Avec strictFunctionTypes: true (défaut dans strict)
// Les méthodes RESTENT bivariantes (compatibilité avec ES2015 classes)
// Les types de fonctions fléchées sont contravariants sur les paramètres

interface Processor {
  process(item: Animal): void;     // méthode — bivariant (risqué)
  processArrow: (item: Animal) => void; // propriété flèche — contravariant (sûr)
}

class DogProcessor implements Processor {
  process(item: Dog): void { // Accepté (bivariant sur méthodes)
    console.log(item.breed);
  }
  processArrow = (item: Dog): void => { // Erreur avec strict ! (contravariant)
    console.log(item.breed);
  };
}
```

## Higher-Kinded Types (HKT) — simulation en TypeScript

TypeScript ne supporte pas nativement les HKT (types paramétrés par d'autres types). Le pattern HKT simule cette fonctionnalité via l'augmentation d'interface.

```typescript
// Registre global des HKTs — à augmenter par chaque type
interface HKTRegistry {
  readonly _A: unknown;
}

// Type d'application : applique un HKT à un argument
type Apply<F extends keyof HKTRegistry, A> =
  (HKTRegistry & { readonly _A: A })[F];

// Exemple : Maybe (Option type)
interface MaybeHKT extends HKTRegistry {
  readonly MaybeHKT: Maybe<this["_A"]>;
}

type Maybe<T> = { kind: "just"; value: T } | { kind: "nothing" };

// Déclarer Maybe dans le registre
declare module "./hkt" {
  interface HKTRegistry {
    MaybeHKT: Maybe<this["_A"]>;
  }
}

// Functor générique utilisant les HKTs
interface Functor<F extends keyof HKTRegistry> {
  map<A, B>(fa: Apply<F, A>, f: (a: A) => B): Apply<F, B>;
}

// Implémentation concrète
const MaybeFunctor: Functor<"MaybeHKT"> = {
  map(fa, f) {
    if (fa.kind === "nothing") return { kind: "nothing" };
    return { kind: "just", value: f(fa.value) };
  },
};
```

## Builder pattern entièrement type-safe avec type state machines

Le Builder Pattern encode l'état de construction dans le système de types. Certaines méthodes ne sont disponibles que dans certains états.

```typescript
// Marqueurs d'état — phantom types
declare const _hasUrl: unique symbol;
declare const _hasMethod: unique symbol;
declare const _hasBody: unique symbol;

type RequestState = {
  hasUrl: boolean;
  hasMethod: boolean;
  hasBody: boolean;
};

type InitialState = { hasUrl: false; hasMethod: false; hasBody: false };

class RequestBuilder<S extends RequestState> {
  private config: Record<string, unknown> = {};

  // setUrl est disponible seulement si hasUrl est false
  setUrl<This extends RequestBuilder<S & { hasUrl: false }>>(
    this: This,
    url: string
  ): RequestBuilder<Omit<S, "hasUrl"> & { hasUrl: true }> {
    this.config.url = url;
    return this as any;
  }

  setMethod<This extends RequestBuilder<S & { hasMethod: false }>>(
    this: This,
    method: "GET" | "POST" | "PUT" | "DELETE"
  ): RequestBuilder<Omit<S, "hasMethod"> & { hasMethod: true }> {
    this.config.method = method;
    return this as any;
  }

  setBody<This extends RequestBuilder<S & { hasBody: false; hasMethod: true }>>(
    this: This,
    body: unknown
  ): RequestBuilder<Omit<S, "hasBody"> & { hasBody: true }> {
    this.config.body = JSON.stringify(body);
    return this as any;
  }

  // build() seulement si URL et méthode sont définis
  build<This extends RequestBuilder<S & { hasUrl: true; hasMethod: true }>>(
    this: This
  ): Request {
    return new Request(this.config.url as string, this.config as RequestInit);
  }
}

// Usage — les erreurs sont détectées à la compilation
const request = new RequestBuilder<InitialState>()
  .setUrl("https://api.example.com/users")
  .setMethod("POST")
  .setBody({ name: "Alice" })
  .build();

// Erreur : build() non disponible sans setUrl()
// new RequestBuilder<InitialState>().setMethod("GET").build(); // Erreur !
```

## Factory pattern générique

```typescript
interface BaseService {
  initialize(): Promise<void>;
  destroy(): Promise<void>;
}

// Factory qui préserve le type concret
function createService<T extends BaseService>(
  Class: new (...args: any[]) => T,
  ...args: ConstructorParameters<typeof Class>
): T {
  return new Class(...args);
}

class UserService extends BaseService {
  constructor(private db: Database, private cache: Cache) {
    super();
  }
  async initialize() { await this.db.connect(); }
  async destroy()    { await this.db.disconnect(); }
  async findById(id: number) { /* ... */ }
}

// TypeScript infère UserService, pas BaseService
const userService = createService(UserService, db, cache);
userService.findById(1); // Disponible — type est UserService, pas BaseService

// Factory avec registre
type ServiceRegistry = {
  user: typeof UserService;
  order: typeof OrderService;
};

function createFromRegistry<K extends keyof ServiceRegistry>(
  key: K,
  ...args: ConstructorParameters<ServiceRegistry[K]>
): InstanceType<ServiceRegistry[K]> {
  const registry: ServiceRegistry = { user: UserService, order: OrderService };
  return new registry[key](...args) as InstanceType<ServiceRegistry[K]>;
}
```

## Generic constraints avancées

```typescript
// Contrainte sur keyof — accès type-safe aux propriétés
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Contrainte extends object — exclure primitives
function mergeObjects<T extends object, U extends object>(
  base: T,
  override: Partial<U>
): T & U {
  return { ...base, ...override } as T & U;
}

// Inférence depuis des contraintes — le type est déduit
function firstKey<T extends Record<string, unknown>>(obj: T): keyof T {
  return Object.keys(obj)[0] as keyof T;
}

// Contrainte avec union — accepter plusieurs formes
type Serializable = string | number | boolean | null | Serializable[] | { [k: string]: Serializable };

function serialize<T extends Serializable>(value: T): string {
  return JSON.stringify(value);
}

// Mapper les valeurs d'un objet en préservant les clés
function mapValues<T extends object, U>(
  obj: T,
  fn: <K extends keyof T>(value: T[K], key: K) => U
): { [K in keyof T]: U } {
  const result = {} as { [K in keyof T]: U };
  for (const key in obj) {
    result[key] = fn(obj[key], key);
  }
  return result;
}
```

## Currying type-safe

```typescript
// Curry simple — 2 arguments
function curry<A, B, C>(fn: (a: A, b: B) => C): (a: A) => (b: B) => C {
  return (a) => (b) => fn(a, b);
}

const add = curry((a: number, b: number) => a + b);
const add5 = add(5);   // type: (b: number) => number
const result = add5(3); // type: number — 8

// Curry générique à N arguments via overloads
function curryN<A, B>(fn: (a: A) => B): (a: A) => B;
function curryN<A, B, C>(fn: (a: A, b: B) => C): (a: A) => (b: B) => C;
function curryN<A, B, C, D>(fn: (a: A, b: B, c: C) => D): (a: A) => (b: B) => (c: C) => D;
function curryN(fn: (...args: any[]) => any) {
  return function curried(...args: any[]) {
    if (args.length >= fn.length) return fn(...args);
    return (...more: any[]) => curried(...args, ...more);
  };
}

const multiply = curryN((a: number, b: number, c: number) => a * b * c);
const double = multiply(2);        // (b: number) => (c: number) => number
const sixTimes = double(3);        // (c: number) => number
const result2 = sixTimes(4);       // number — 24
```

## Pipe type-safe

```typescript
// Pipe avec surcharges jusqu'à 5 étapes
function pipe<A>(value: A): A;
function pipe<A, B>(value: A, fn1: (a: A) => B): B;
function pipe<A, B, C>(value: A, fn1: (a: A) => B, fn2: (b: B) => C): C;
function pipe<A, B, C, D>(
  value: A,
  fn1: (a: A) => B,
  fn2: (b: B) => C,
  fn3: (c: C) => D
): D;
function pipe<A, B, C, D, E>(
  value: A,
  fn1: (a: A) => B,
  fn2: (b: B) => C,
  fn3: (c: C) => D,
  fn4: (d: D) => E
): E;
function pipe(value: unknown, ...fns: Array<(x: unknown) => unknown>): unknown {
  return fns.reduce((acc, fn) => fn(acc), value);
}

// Usage type-safe
const processUser = (id: string) =>
  pipe(
    id,
    (s) => parseInt(s, 10),    // string → number
    (n) => ({ id: n }),         // number → { id: number }
    (obj) => JSON.stringify(obj) // { id: number } → string
  );

// processUser("42") renvoie string — vérifié à la compilation

// compose (ordre inversé)
function compose<A, B, C>(fn2: (b: B) => C, fn1: (a: A) => B): (a: A) => C {
  return (a) => fn2(fn1(a));
}
```

## Design patterns OOP avec TypeScript strict

### Decorator pattern — type-safe

```typescript
interface TextProcessor {
  process(text: string): string;
}

class BaseProcessor implements TextProcessor {
  process(text: string): string {
    return text;
  }
}

abstract class TextDecorator implements TextProcessor {
  constructor(protected wrapped: TextProcessor) {}
  process(text: string): string {
    return this.wrapped.process(text);
  }
}

class UpperCaseDecorator extends TextDecorator {
  process(text: string): string {
    return super.process(text).toUpperCase();
  }
}

class TrimDecorator extends TextDecorator {
  process(text: string): string {
    return super.process(text).trim();
  }
}

// Composition fluide avec les types préservés
const processor: TextProcessor = new UpperCaseDecorator(
  new TrimDecorator(new BaseProcessor())
);
```

### Strategy pattern avec generics

```typescript
interface SortStrategy<T> {
  sort(items: T[]): T[];
  compare(a: T, b: T): number;
}

class Sorter<T> {
  constructor(private strategy: SortStrategy<T>) {}

  setStrategy(strategy: SortStrategy<T>): this {
    this.strategy = strategy;
    return this;
  }

  execute(items: T[]): T[] {
    return this.strategy.sort([...items]);
  }
}

const numberSorter = new Sorter<number>({
  sort: (items) => items.sort((a, b) => a - b),
  compare: (a, b) => a - b,
});
```

### Observer avec types précis

```typescript
type EventMap = {
  "user:created": { id: number; name: string };
  "user:deleted": { id: number };
  "order:placed": { orderId: string; amount: number };
};

class TypedEventEmitter<Events extends Record<string, unknown>> {
  private listeners = new Map<keyof Events, Set<(payload: unknown) => void>>();

  on<K extends keyof Events>(
    event: K,
    listener: (payload: Events[K]) => void
  ): () => void {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    const set = this.listeners.get(event)!;
    set.add(listener as (payload: unknown) => void);
    return () => set.delete(listener as (payload: unknown) => void);
  }

  emit<K extends keyof Events>(event: K, payload: Events[K]): void {
    this.listeners.get(event)?.forEach((listener) => listener(payload));
  }
}

const emitter = new TypedEventEmitter<EventMap>();

// Types inférés automatiquement
emitter.on("user:created", ({ id, name }) => {
  console.log(`Utilisateur créé : ${name} (${id})`);
});

emitter.emit("user:created", { id: 1, name: "Alice" }); // OK
// emitter.emit("user:created", { id: 1 }); // Erreur — name manquant !
```

## Branded types — sécurité des types primitifs

```typescript
// Déclaration d'un brand
declare const brand: unique symbol;
type Brand<T, B> = T & { readonly [brand]: B };

// Types physiques — impossibles à mélanger
type Metres = Brand<number, "Metres">;
type Kilograms = Brand<number, "Kilograms">;
type Seconds = Brand<number, "Seconds">;

// Constructeurs type-safe
const metres = (n: number): Metres => n as Metres;
const kilograms = (n: number): Kilograms => n as Kilograms;

function calculateSpeed(distance: Metres, time: Seconds): Brand<number, "MetresPerSecond"> {
  return (distance / time) as Brand<number, "MetresPerSecond">;
}

const distance = metres(100);
const time = 10 as Seconds;
const speed = calculateSpeed(distance, time); // OK

// calculateSpeed(kilograms(50), time); // Erreur — Kilograms !== Metres !

// Branded IDs pour entités
type UserId    = Brand<number, "UserId">;
type ProductId = Brand<number, "ProductId">;
type OrderId   = Brand<number, "OrderId">;

const userId    = (n: number): UserId    => n as UserId;
const productId = (n: number): ProductId => n as ProductId;

function getUserById(id: UserId): Promise<User> { /* ... */ return Promise.resolve(null!); }
function getProductById(id: ProductId): Promise<Product> { /* ... */ return Promise.resolve(null!); }

const uid = userId(1);
const pid = productId(42);

getUserById(uid);    // OK
// getUserById(pid); // Erreur — ProductId !== UserId !
// getUserById(1);   // Erreur — number brut non accepté !
```

## Tableau récapitulatif — variance par position

| Position | Variance | Exemple | `A extends B` implique |
|---|---|---|---|
| Type de retour | Covariant | `() => T` | `F<A> extends F<B>` |
| Paramètre de fonction | Contravariant | `(x: T) => void` | `F<B> extends F<A>` |
| Array mutable | Invariant | `Array<T>` | Ni l'un ni l'autre |
| Propriété en lecture seule | Covariant | `{ readonly x: T }` | `F<A> extends F<B>` |
| Méthode de classe | Bivariant | `{ m(x: T): void }` | Les deux (dangereux) |

## Points clés à retenir

- Utiliser des propriétés fléchées plutôt que des méthodes pour obtenir la contravariante sur les paramètres
- Le Builder pattern type-safe encode les étapes de construction dans les types — impossible d'oublier une étape
- Les branded types éliminent toute une classe de bugs liés à la confusion d'entités du même type primitif
- Les HKT permettent d'écrire des abstractions fonctionnelles génériques (Functor, Monad) même sans support natif
- Le pipe type-safe avec surcharges couvre 95% des cas d'usage avec une inférence parfaite
