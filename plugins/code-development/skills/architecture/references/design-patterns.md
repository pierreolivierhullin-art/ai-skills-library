# Design Patterns — Modern Software Design

## Overview

Ce document de référence couvre les design patterns appliqués au développement logiciel moderne. Il traite les patterns GoF réinterprétés pour les architectures actuelles, les principes SOLID, les patterns tactiques du Domain-Driven Design, CQRS et Event Sourcing. Appliquer ces patterns comme des outils de résolution de problèmes récurrents, jamais comme des dogmes.

---

## SOLID Principles — Applied to Modern Development

### Single Responsibility Principle (SRP)
Chaque module, classe ou fonction doit avoir une seule raison de changer. En pratique dans les architectures modernes :

- **Au niveau du module** : un module dans un monolithe modulaire encapsule un seul bounded context.
- **Au niveau du service** : un microservice gère un seul sous-domaine métier.
- **Au niveau de la fonction** : une fonction serverless traite un seul type d'événement.
- **Au niveau du fichier** : un fichier de code contient une seule préoccupation (handler, repository, domain entity).

Indicateur de violation : quand une modification métier dans un domaine nécessite de modifier du code dans un autre domaine, les responsabilités sont mal séparées.

### Open/Closed Principle (OCP)
Les modules doivent être ouverts à l'extension, fermés à la modification. Application moderne :

- **Plugin architecture** : concevoir des points d'extension (hooks, middleware, interceptors) plutôt que de modifier le code existant.
- **Strategy pattern** : injecter les comportements variables plutôt que d'utiliser des conditionnelles.
- **Feature flags** : activer/désactiver des fonctionnalités sans modifier le code déployé.
- **Event-driven** : ajouter des consommateurs d'événements sans modifier le producteur.

```typescript
// Violation OCP — modification nécessaire pour chaque nouveau type
function calculateDiscount(order: Order): number {
  if (order.type === 'premium') return order.total * 0.2;
  if (order.type === 'vip') return order.total * 0.3;
  // Ajouter un nouveau type = modifier cette fonction
}

// Conforme OCP — extension par stratégie
interface DiscountStrategy {
  calculate(order: Order): number;
}

class DiscountCalculator {
  constructor(private strategies: Map<string, DiscountStrategy>) {}

  calculate(order: Order): number {
    const strategy = this.strategies.get(order.type);
    return strategy?.calculate(order) ?? 0;
  }
}
```

### Liskov Substitution Principle (LSP)
Les sous-types doivent être substituables à leurs types de base sans altérer la correctness du programme. Application moderne :

- **Interface segregation dans les APIs** : un consommateur d'API ne doit pas être surpris par le comportement d'une version dérivée.
- **Polymorphisme dans les handlers** : un handler de commande doit respecter le contrat de son interface, quel que soit le type concret.
- **Contravariance/covariance** : respecter la variance des types dans les generics.

Indicateur de violation : un `instanceof` check ou un cast de type dans du code consommateur.

### Interface Segregation Principle (ISP)
Aucun client ne devrait être forcé de dépendre de méthodes qu'il n'utilise pas. Application moderne :

- **APIs granulaires** : concevoir des endpoints spécifiques plutôt qu'un endpoint monolithique qui retourne tout.
- **Ports & Adapters** : définir des interfaces (ports) étroites et spécifiques par cas d'usage.
- **GraphQL** : le field selection natif implémente naturellement ISP côté API.
- **CQRS** : séparer les interfaces de lecture et d'écriture.

```typescript
// Violation ISP — interface trop large
interface UserRepository {
  findById(id: string): User;
  findByEmail(email: string): User;
  save(user: User): void;
  delete(id: string): void;
  generateReport(): Report;
  sendNotification(userId: string): void;
}

// Conforme ISP — interfaces ciblées
interface UserReader {
  findById(id: string): User;
  findByEmail(email: string): User;
}

interface UserWriter {
  save(user: User): void;
  delete(id: string): void;
}
```

### Dependency Inversion Principle (DIP)
Les modules de haut niveau ne doivent pas dépendre des modules de bas niveau. Les deux doivent dépendre d'abstractions. Application moderne :

- **Hexagonal Architecture (Ports & Adapters)** : le domaine définit des ports (interfaces), l'infrastructure fournit des adapters.
- **Dependency Injection** : injecter les dépendances plutôt que les instancier directement.
- **Infrastructure as plugin** : la base de données, le message broker, le file system sont des détails d'implémentation injectés.

```
Domain Layer (abstractions / ports)
     ↑ dépend de
Application Layer (use cases)
     ↑ dépend de
Infrastructure Layer (adapters) → implémente les ports
```

---

## GoF Patterns — Modern Reinterpretation

### Creational Patterns

#### Factory & Abstract Factory
Encapsuler la logique de création d'objets complexes. En développement moderne :

- **Factory functions** : préférer les fonctions factory aux classes factory dans les langages fonctionnels. En TypeScript : `createOrder(data)` plutôt que `new OrderFactory().create(data)`.
- **DI Container** : le container d'injection de dépendances est la factory ultime — il gère la création et le cycle de vie de tous les composants.
- **Configuration-driven factories** : créer des instances basées sur la configuration (feature flags, environment variables).

```typescript
// Factory function moderne avec validation
function createOrder(input: CreateOrderInput): Result<Order, ValidationError> {
  const validatedItems = validateItems(input.items);
  if (validatedItems.isErr()) return validatedItems;

  return Ok(Order.create({
    id: OrderId.generate(),
    customerId: input.customerId,
    items: validatedItems.value,
    status: OrderStatus.PENDING,
    createdAt: Clock.now(),
  }));
}
```

#### Builder
Construire des objets complexes étape par étape. Très utilisé dans les tests :

```typescript
// Test builder — facilite la création d'objets de test
class OrderBuilder {
  private props: Partial<OrderProps> = {
    id: 'ORD-001',
    status: OrderStatus.PENDING,
    items: [defaultItem()],
    createdAt: new Date('2025-01-01'),
  };

  withStatus(status: OrderStatus): this {
    this.props.status = status;
    return this;
  }

  withItems(items: OrderItem[]): this {
    this.props.items = items;
    return this;
  }

  build(): Order {
    return Order.create(this.props as OrderProps);
  }
}

// Usage dans les tests
const pendingOrder = new OrderBuilder().build();
const cancelledOrder = new OrderBuilder()
  .withStatus(OrderStatus.CANCELLED)
  .build();
```

#### Singleton — Use with Caution
Garantir une instance unique d'une classe. En développement moderne :

- **Éviter le Singleton classique** : il introduit un état global, rend les tests difficiles et masque les dépendances.
- **Préférer la DI avec scope singleton** : le container gère le cycle de vie, la testabilité est préservée.
- **Cas légitimes** : connection pools, configuration loaders, loggers (mais toujours via DI).

### Structural Patterns

#### Adapter
Convertir l'interface d'une classe en une interface attendue par le client. Pattern fondamental de l'Hexagonal Architecture :

```typescript
// Port (interface du domaine)
interface PaymentGateway {
  charge(amount: Money, customerId: string): Promise<PaymentResult>;
}

// Adapter pour Stripe
class StripePaymentAdapter implements PaymentGateway {
  constructor(private stripe: Stripe) {}

  async charge(amount: Money, customerId: string): Promise<PaymentResult> {
    const intent = await this.stripe.paymentIntents.create({
      amount: amount.toCents(),
      currency: amount.currency,
      customer: customerId,
    });
    return PaymentResult.fromStripe(intent);
  }
}

// Adapter pour test
class FakePaymentGateway implements PaymentGateway {
  private results = new Map<string, PaymentResult>();

  async charge(amount: Money, customerId: string): Promise<PaymentResult> {
    return this.results.get(customerId) ?? PaymentResult.success();
  }
}
```

#### Decorator
Ajouter des comportements à un objet dynamiquement. Très utilisé dans les middlewares modernes :

```typescript
// Decorator pattern via middleware
class LoggingCommandHandler<T extends Command> implements CommandHandler<T> {
  constructor(
    private inner: CommandHandler<T>,
    private logger: Logger,
  ) {}

  async handle(command: T): Promise<Result> {
    this.logger.info(`Handling ${command.constructor.name}`, { command });
    const startTime = performance.now();

    const result = await this.inner.handle(command);

    const duration = performance.now() - startTime;
    this.logger.info(`Handled ${command.constructor.name}`, { duration, success: result.isOk() });

    return result;
  }
}

// Composition de decorators
const handler = new LoggingCommandHandler(
  new ValidationCommandHandler(
    new RetryCommandHandler(
      new CreateOrderHandler(repository),
      { maxRetries: 3 }
    )
  ),
  logger
);
```

#### Facade
Fournir une interface simplifiée à un sous-système complexe. Application moderne :

- **API Gateway** : facade devant les microservices.
- **BFF (Backend for Frontend)** : facade spécifique par type de client.
- **Module API** : interface publique d'un module dans un monolithe modulaire.

### Behavioral Patterns

#### Strategy
Définir une famille d'algorithmes interchangeables. Pattern le plus utilisé dans le développement moderne :

- **Injection de stratégies** : injecter le comportement via DI.
- **Configuration-driven** : sélectionner la stratégie via la configuration.
- **A/B testing** : alterner les stratégies pour expérimenter.

#### Observer / Event Emitter
Notifier automatiquement les objets abonnés lors d'un changement d'état. Fondation de l'architecture event-driven :

- **Domain Events** : les aggregates émettent des événements de domaine.
- **Event Bus** : distribue les événements aux handlers enregistrés.
- **Reactive Streams** : RxJS, Project Reactor pour le traitement asynchrone.

#### Command
Encapsuler une action en tant qu'objet. Fondation de CQRS :

```typescript
// Command object
class PlaceOrderCommand {
  constructor(
    public readonly customerId: string,
    public readonly items: OrderItemDTO[],
    public readonly shippingAddress: AddressDTO,
  ) {}
}

// Command Handler
class PlaceOrderHandler implements CommandHandler<PlaceOrderCommand> {
  constructor(
    private orderRepository: OrderRepository,
    private eventBus: EventBus,
  ) {}

  async handle(command: PlaceOrderCommand): Promise<Result<OrderId, DomainError>> {
    const order = Order.place(
      command.customerId,
      command.items.map(OrderItem.fromDTO),
      ShippingAddress.fromDTO(command.shippingAddress),
    );

    await this.orderRepository.save(order);
    await this.eventBus.publishAll(order.domainEvents);

    return Ok(order.id);
  }
}
```

#### Mediator
Découpler les objets en les faisant communiquer via un médiateur. Implémenté dans les frameworks modernes via un Command/Query Bus :

```typescript
// Mediator / Dispatcher
class CommandBus {
  private handlers = new Map<string, CommandHandler<any>>();

  register<T extends Command>(commandType: string, handler: CommandHandler<T>): void {
    this.handlers.set(commandType, handler);
  }

  async dispatch<T extends Command>(command: T): Promise<Result> {
    const handler = this.handlers.get(command.constructor.name);
    if (!handler) throw new Error(`No handler for ${command.constructor.name}`);
    return handler.handle(command);
  }
}
```

---

## Domain-Driven Design — Tactical Patterns

### Entities

Les entités sont des objets avec une identité unique qui persiste à travers le temps. L'identité, pas les attributs, détermine l'égalité.

```typescript
class Order extends Entity<OrderId> {
  private _status: OrderStatus;
  private _items: OrderItem[];
  private _totalAmount: Money;

  // Les méthodes expriment le langage du domaine
  cancel(reason: CancellationReason): Result<void, OrderError> {
    if (!this._status.isCancellable()) {
      return Err(OrderError.cannotCancel(this._status));
    }
    this._status = OrderStatus.CANCELLED;
    this.addDomainEvent(new OrderCancelled(this.id, reason, Clock.now()));
    return Ok(undefined);
  }

  addItem(product: Product, quantity: Quantity): Result<void, OrderError> {
    if (this._status !== OrderStatus.DRAFT) {
      return Err(OrderError.cannotModify(this._status));
    }
    const item = OrderItem.create(product, quantity);
    this._items.push(item);
    this._totalAmount = this.recalculateTotal();
    return Ok(undefined);
  }
}
```

### Value Objects

Les value objects sont des objets immutables définis par leurs attributs, pas par une identité. Ils encapsulent la validation et le comportement.

```typescript
class Money {
  private constructor(
    private readonly amount: number,
    private readonly currency: Currency,
  ) {
    if (amount < 0) throw new InvalidMoneyError('Amount cannot be negative');
    if (!Number.isFinite(amount)) throw new InvalidMoneyError('Amount must be finite');
  }

  static of(amount: number, currency: Currency): Money {
    return new Money(Math.round(amount * 100) / 100, currency);
  }

  add(other: Money): Money {
    this.ensureSameCurrency(other);
    return Money.of(this.amount + other.amount, this.currency);
  }

  subtract(other: Money): Money {
    this.ensureSameCurrency(other);
    return Money.of(this.amount - other.amount, this.currency);
  }

  multiply(factor: number): Money {
    return Money.of(this.amount * factor, this.currency);
  }

  isGreaterThan(other: Money): boolean {
    this.ensureSameCurrency(other);
    return this.amount > other.amount;
  }

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }

  toCents(): number {
    return Math.round(this.amount * 100);
  }

  private ensureSameCurrency(other: Money): void {
    if (this.currency !== other.currency) {
      throw new CurrencyMismatchError(this.currency, other.currency);
    }
  }
}

class EmailAddress {
  private constructor(private readonly value: string) {
    if (!EmailAddress.isValid(value)) {
      throw new InvalidEmailError(value);
    }
  }

  static create(value: string): EmailAddress {
    return new EmailAddress(value.toLowerCase().trim());
  }

  static isValid(value: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  equals(other: EmailAddress): boolean {
    return this.value === other.value;
  }

  toString(): string {
    return this.value;
  }
}
```

### Aggregates

Un aggregate est un cluster d'entités et de value objects traité comme une unité de consistance. L'aggregate root est le seul point d'entrée.

#### Règles de conception des aggregates

1. **Protéger les invariants métier** : l'aggregate garantit que ses règles métier sont toujours respectées.
2. **Favoriser les petits aggregates** : préférer les aggregates avec peu d'entités. Un aggregate trop large crée des problèmes de contention.
3. **Référencer les autres aggregates par identité** : ne pas inclure d'autres aggregates par référence directe. Utiliser les IDs.
4. **Une transaction = un aggregate** : ne modifier qu'un seul aggregate par transaction. Utiliser des domain events pour la consistance inter-aggregates.
5. **Eventual consistency entre aggregates** : accepter la consistance éventuelle entre aggregates distincts.

```typescript
// Aggregate Root
class ShoppingCart extends AggregateRoot<CartId> {
  private items: CartItem[] = [];
  private readonly MAX_ITEMS = 50;

  addItem(productId: ProductId, quantity: Quantity, price: Money): Result<void, CartError> {
    if (this.items.length >= this.MAX_ITEMS) {
      return Err(CartError.maxItemsReached(this.MAX_ITEMS));
    }

    const existingItem = this.items.find(i => i.productId.equals(productId));
    if (existingItem) {
      existingItem.increaseQuantity(quantity);
    } else {
      this.items.push(CartItem.create(productId, quantity, price));
    }

    this.addDomainEvent(new ItemAddedToCart(this.id, productId, quantity));
    return Ok(undefined);
  }

  checkout(): Result<CheckoutResult, CartError> {
    if (this.items.length === 0) {
      return Err(CartError.emptyCart());
    }

    const total = this.calculateTotal();
    this.addDomainEvent(new CartCheckedOut(this.id, this.items, total));

    return Ok({ items: [...this.items], total });
  }

  private calculateTotal(): Money {
    return this.items.reduce(
      (sum, item) => sum.add(item.subtotal()),
      Money.of(0, Currency.EUR),
    );
  }
}
```

### Domain Events

Les domain events représentent des faits significatifs qui se sont produits dans le domaine. Ils sont le mécanisme principal de communication entre aggregates et entre bounded contexts.

```typescript
// Domain Event
class OrderPlaced extends DomainEvent {
  constructor(
    public readonly orderId: OrderId,
    public readonly customerId: CustomerId,
    public readonly items: ReadonlyArray<OrderItemSnapshot>,
    public readonly totalAmount: Money,
    public readonly placedAt: Date,
  ) {
    super();
  }
}

// Event Handler (dans un autre bounded context)
class SendOrderConfirmationEmail implements DomainEventHandler<OrderPlaced> {
  constructor(private emailService: EmailService) {}

  async handle(event: OrderPlaced): Promise<void> {
    await this.emailService.send({
      to: event.customerId,
      template: 'order-confirmation',
      data: {
        orderId: event.orderId.value,
        items: event.items,
        total: event.totalAmount.toString(),
      },
    });
  }
}
```

### Repositories

Les repositories fournissent une abstraction de la persistance pour les aggregates. Ils opèrent sur des aggregates entiers.

```typescript
interface OrderRepository {
  findById(id: OrderId): Promise<Order | null>;
  save(order: Order): Promise<void>;
  nextId(): OrderId;
}

// Implémentation PostgreSQL
class PostgresOrderRepository implements OrderRepository {
  constructor(private db: DatabaseClient) {}

  async findById(id: OrderId): Promise<Order | null> {
    const row = await this.db.query(
      'SELECT * FROM orders WHERE id = $1',
      [id.value]
    );
    if (!row) return null;

    const items = await this.db.query(
      'SELECT * FROM order_items WHERE order_id = $1',
      [id.value]
    );

    return OrderMapper.toDomain(row, items);
  }

  async save(order: Order): Promise<void> {
    await this.db.transaction(async (tx) => {
      await tx.query(
        `INSERT INTO orders (id, customer_id, status, total_amount, created_at)
         VALUES ($1, $2, $3, $4, $5)
         ON CONFLICT (id) DO UPDATE SET status = $3, total_amount = $4`,
        [order.id.value, order.customerId.value, order.status, order.totalAmount.toCents(), order.createdAt]
      );

      // Sauvegarder les items...
      // Publier les domain events...
    });
  }

  nextId(): OrderId {
    return OrderId.generate();
  }
}
```

### Bounded Contexts & Context Mapping

#### Context Mapping Patterns

| Pattern | Description | Quand l'utiliser |
|---|---|---|
| **Shared Kernel** | Code partagé entre deux contexts | Équipes très proches, domaine intimement lié |
| **Customer-Supplier** | Un context fournit, l'autre consomme | Dépendance claire, supplier accommode le customer |
| **Conformist** | Le consumer s'adapte au modèle du supplier | Pas de contrôle sur le supplier (API tierce) |
| **Anti-Corruption Layer (ACL)** | Couche de traduction entre contextes | Protéger le modèle de domaine des modèles externes |
| **Open Host Service** | API publique bien définie | Multiples consommateurs, contrat stable |
| **Published Language** | Format d'échange standardisé | Communication inter-contextes avec schéma partagé |

#### Anti-Corruption Layer — Implementation

```typescript
// ACL protège notre domaine du modèle externe
class LegacyOrderACL {
  constructor(private legacyClient: LegacyOrderSystemClient) {}

  async findOrder(orderId: OrderId): Promise<Order | null> {
    // Appel au système legacy
    const legacyOrder = await this.legacyClient.getOrder(orderId.value);
    if (!legacyOrder) return null;

    // Traduction vers notre modèle de domaine
    return this.translateToDomain(legacyOrder);
  }

  private translateToDomain(legacy: LegacyOrderDTO): Order {
    return Order.reconstitute({
      id: OrderId.of(legacy.order_number),
      customerId: CustomerId.of(legacy.client_ref),
      status: this.mapStatus(legacy.state_code),
      items: legacy.line_items.map(this.mapItem),
      totalAmount: Money.of(legacy.grand_total / 100, Currency.EUR),
    });
  }

  private mapStatus(legacyCode: number): OrderStatus {
    const mapping: Record<number, OrderStatus> = {
      0: OrderStatus.DRAFT,
      1: OrderStatus.PENDING,
      2: OrderStatus.CONFIRMED,
      9: OrderStatus.CANCELLED,
    };
    return mapping[legacyCode] ?? OrderStatus.UNKNOWN;
  }
}
```

---

## CQRS — Command Query Responsibility Segregation

### Architecture CQRS

Séparer les modèles de lecture (Query) et d'écriture (Command) en deux stacks indépendantes.

```
[Client]
  ├── Commands → [Command Handler] → [Write Model] → [Event Store / DB]
  │                                                        ↓
  │                                              [Domain Events]
  │                                                        ↓
  │                                              [Projection Engine]
  │                                                        ↓
  └── Queries → [Query Handler] → [Read Model] ← [Optimized Views]
```

### Niveaux de CQRS

1. **CQRS logique (même base)** : séparer les interfaces de lecture et d'écriture dans le code, même base de données. Coût minimal, bénéfice en clarté.
2. **CQRS avec read replicas** : écrire sur le primary, lire sur les replicas. Scalabilité en lecture.
3. **CQRS avec projections dédiées** : écrire dans le write model, projeter vers des stores de lecture optimisés (ElasticSearch, Redis, vues matérialisées). Scalabilité et performance maximales.
4. **CQRS + Event Sourcing** : le write model est un event store, les projections reconstruisent les vues à partir des événements. Puissance maximale mais complexité élevée.

### Projections

```typescript
// Projection qui maintient une vue optimisée pour la lecture
class OrderSummaryProjection implements EventHandler {
  constructor(private readDb: ReadDatabase) {}

  async on(event: DomainEvent): Promise<void> {
    if (event instanceof OrderPlaced) {
      await this.readDb.upsert('order_summaries', {
        id: event.orderId.value,
        customer_name: event.customerName,
        status: 'placed',
        total: event.totalAmount.value,
        item_count: event.items.length,
        placed_at: event.placedAt,
      });
    }

    if (event instanceof OrderShipped) {
      await this.readDb.update('order_summaries', event.orderId.value, {
        status: 'shipped',
        shipped_at: event.shippedAt,
        tracking_number: event.trackingNumber,
      });
    }

    if (event instanceof OrderDelivered) {
      await this.readDb.update('order_summaries', event.orderId.value, {
        status: 'delivered',
        delivered_at: event.deliveredAt,
      });
    }
  }
}
```

### Quand utiliser CQRS

| Critère | CQRS recommandé | CQRS non recommandé |
|---|---|---|
| Ratio lecture/écriture | Très asymétrique (100:1) | Équilibré (1:1) |
| Complexité du domaine | Élevée, règles métier riches | CRUD simple |
| Besoins de performance | Lecture haute performance requise | Performance uniforme suffisante |
| Scalabilité | Scaling indépendant lecture/écriture | Scaling uniforme suffisant |
| Consistance | Éventuelle acceptable pour les lectures | Forte consistance requise partout |

---

## Event Sourcing — Implementation Guide

### Event Store Implementation

```typescript
interface EventStore {
  // Append events to a stream with optimistic concurrency
  append(
    streamId: string,
    events: DomainEvent[],
    expectedVersion: number,
  ): Promise<void>;

  // Read all events for a stream
  readStream(streamId: string): Promise<StoredEvent[]>;

  // Read events from a global position (for projections)
  readAll(fromPosition: number, limit: number): Promise<StoredEvent[]>;

  // Subscribe to new events (for live projections)
  subscribe(handler: (event: StoredEvent) => Promise<void>): Subscription;
}

interface StoredEvent {
  streamId: string;
  eventType: string;
  data: Record<string, unknown>;
  metadata: EventMetadata;
  version: number;        // Position dans le stream
  globalPosition: number; // Position globale
  timestamp: Date;
}
```

### Aggregate Rehydration

```typescript
abstract class EventSourcedAggregate<TId> {
  private _version: number = 0;
  private _uncommittedEvents: DomainEvent[] = [];

  // Reconstruire l'état à partir des événements
  static rehydrate<T extends EventSourcedAggregate<any>>(
    events: DomainEvent[],
  ): T {
    const aggregate = new (this as any)();
    for (const event of events) {
      aggregate.apply(event, false);
    }
    return aggregate;
  }

  // Appliquer un nouvel événement
  protected raise(event: DomainEvent): void {
    this.apply(event, true);
  }

  private apply(event: DomainEvent, isNew: boolean): void {
    this.when(event); // Muter l'état
    this._version++;
    if (isNew) {
      this._uncommittedEvents.push(event);
    }
  }

  // Chaque aggregate implémente le routage des événements
  protected abstract when(event: DomainEvent): void;

  get uncommittedEvents(): ReadonlyArray<DomainEvent> {
    return this._uncommittedEvents;
  }

  get version(): number {
    return this._version;
  }

  clearUncommittedEvents(): void {
    this._uncommittedEvents = [];
  }
}
```

### Snapshotting

Pour éviter de rejouer des milliers d'événements, sauvegarder des snapshots périodiques :

```typescript
class SnapshotStore {
  async save(aggregateId: string, snapshot: AggregateSnapshot): Promise<void> {
    await this.db.upsert('snapshots', {
      aggregate_id: aggregateId,
      version: snapshot.version,
      state: JSON.stringify(snapshot.state),
      created_at: new Date(),
    });
  }

  async load(aggregateId: string): Promise<AggregateSnapshot | null> {
    return this.db.findOne('snapshots', { aggregate_id: aggregateId });
  }
}

// Rehydratation avec snapshot
async function loadAggregate(id: string): Promise<Order> {
  const snapshot = await snapshotStore.load(id);
  const fromVersion = snapshot ? snapshot.version + 1 : 0;
  const events = await eventStore.readStream(id, fromVersion);

  if (snapshot) {
    const order = Order.fromSnapshot(snapshot);
    for (const event of events) {
      order.apply(event, false);
    }
    return order;
  }

  return Order.rehydrate(events);
}
```

Stratégie de snapshotting :
- Créer un snapshot tous les N événements (typiquement 50-100).
- Ou créer un snapshot quand le temps de rehydratation dépasse un seuil.
- Les snapshots sont optionnels et peuvent être recréés à partir des événements.

---

## Architectural Patterns — Hexagonal & Clean Architecture

### Hexagonal Architecture (Ports & Adapters)

```
                    [Driving Adapters]
                    (REST Controller)
                    (CLI Command)
                    (gRPC Handler)
                    (Event Consumer)
                           │
                           ▼
                    ┌─────────────┐
                    │   Ports In  │ (Use Case interfaces)
                    │  ┌────────┐ │
                    │  │ Domain │ │ (Entities, Value Objects, Domain Services)
                    │  └────────┘ │
                    │  Ports Out  │ (Repository interfaces, Gateway interfaces)
                    └─────────────┘
                           │
                           ▼
                    [Driven Adapters]
                    (PostgreSQL Repository)
                    (Redis Cache)
                    (Kafka Publisher)
                    (Stripe Gateway)
```

#### Règle de dépendance
Les dépendances pointent toujours vers l'intérieur. Le domaine ne dépend de rien d'externe. L'infrastructure dépend du domaine, jamais l'inverse.

### Vertical Slice Architecture

Alternative à l'architecture en couches : organiser le code par feature (slice vertical) plutôt que par couche technique.

```
src/
├── features/
│   ├── place-order/
│   │   ├── PlaceOrderCommand.ts
│   │   ├── PlaceOrderHandler.ts
│   │   ├── PlaceOrderValidator.ts
│   │   ├── PlaceOrderEndpoint.ts
│   │   └── PlaceOrder.test.ts
│   ├── cancel-order/
│   │   ├── CancelOrderCommand.ts
│   │   ├── CancelOrderHandler.ts
│   │   └── ...
│   └── get-order-summary/
│       ├── GetOrderSummaryQuery.ts
│       ├── GetOrderSummaryHandler.ts
│       └── ...
├── domain/
│   ├── Order.ts
│   ├── OrderItem.ts
│   └── Money.ts
└── infrastructure/
    ├── database/
    └── messaging/
```

Avantages : haute cohésion par feature, modifications localisées, facilité de suppression de features. Particulièrement adapté au CQRS où chaque slice est un command/query handler.
