# Clean Code & Design Principles

Référence approfondie sur les principes de code propre, les design patterns modernes et la gestion de la complexité.

---

## Table of Contents

1. [SOLID Principles in Depth](#solid-principles-in-depth)
2. [DRY, KISS, YAGNI -- Applied](#dry-kiss-yagni--applied)
3. [Naming Conventions](#naming-conventions)
4. [Complexity Management](#complexity-management)
5. [Code Readability](#code-readability)
6. [Design Patterns for Modern Development](#design-patterns-for-modern-development)

---

## SOLID Principles in Depth

### Single Responsibility Principle (SRP)

Concevoir chaque module pour qu'il n'ait qu'une seule raison de changer. La "raison de changer" correspond à un acteur métier unique. Ne pas confondre SRP avec "faire une seule chose" -- il s'agit de n'avoir qu'un seul axe de changement.

**Diagnostic** : si la description d'une classe nécessite le mot "et", elle viole probablement SRP.

```typescript
// VIOLATION : cette classe mélange logique métier et persistance
class OrderService {
  calculateTotal(order: Order): number { /* logique de calcul */ }
  applyDiscount(order: Order, code: string): void { /* règles promo */ }
  saveToDatabase(order: Order): void { /* accès BDD */ }
  sendConfirmationEmail(order: Order): void { /* notification */ }
}

// CORRECT : séparation par responsabilité/acteur
class OrderPricingService {
  calculateTotal(order: Order): Money { /* ... */ }
  applyDiscount(order: Order, discountCode: DiscountCode): Money { /* ... */ }
}

class OrderRepository {
  save(order: Order): Promise<void> { /* ... */ }
  findById(id: OrderId): Promise<Order | null> { /* ... */ }
}

class OrderNotificationService {
  sendConfirmation(order: Order): Promise<void> { /* ... */ }
}
```

### Open/Closed Principle (OCP)

Concevoir les modules pour qu'ils soient extensibles sans modification du code existant. Utiliser le polymorphisme, les stratégies et les plugins plutôt que les conditions en cascade.

```typescript
// VIOLATION : chaque nouveau type de paiement nécessite de modifier cette fonction
function processPayment(type: string, amount: number): void {
  if (type === 'credit_card') { /* ... */ }
  else if (type === 'paypal') { /* ... */ }
  else if (type === 'crypto') { /* ... */ } // ajout = modification
}

// CORRECT : extension par ajout d'une nouvelle implémentation
interface PaymentProcessor {
  supports(method: PaymentMethod): boolean;
  process(payment: Payment): Promise<PaymentResult>;
}

class CreditCardProcessor implements PaymentProcessor {
  supports(method: PaymentMethod): boolean { return method === 'credit_card'; }
  process(payment: Payment): Promise<PaymentResult> { /* ... */ }
}

class PaymentService {
  constructor(private processors: PaymentProcessor[]) {}

  async process(payment: Payment): Promise<PaymentResult> {
    const processor = this.processors.find(p => p.supports(payment.method));
    if (!processor) throw new UnsupportedPaymentMethodError(payment.method);
    return processor.process(payment);
  }
}
```

### Liskov Substitution Principle (LSP)

Garantir que toute sous-classe peut être utilisée à la place de sa classe parente sans surprises. Les préconditions ne doivent pas être renforcées, les postconditions ne doivent pas être affaiblies.

```typescript
// VIOLATION classique : le carré n'est pas un rectangle au sens de LSP
class Rectangle {
  constructor(protected width: number, protected height: number) {}
  setWidth(w: number): void { this.width = w; }
  setHeight(h: number): void { this.height = h; }
  area(): number { return this.width * this.height; }
}

class Square extends Rectangle {
  setWidth(w: number): void { this.width = w; this.height = w; } // surprise !
  setHeight(h: number): void { this.width = h; this.height = h; }
}

// Un test qui passe pour Rectangle échoue pour Square :
// rect.setWidth(5); rect.setHeight(3); expect(rect.area()).toBe(15); // FAIL pour Square

// CORRECT : modéliser comme des types distincts partageant une interface
interface Shape {
  area(): number;
}

class Rectangle implements Shape {
  constructor(readonly width: number, readonly height: number) {}
  area(): number { return this.width * this.height; }
}

class Square implements Shape {
  constructor(readonly side: number) {}
  area(): number { return this.side * this.side; }
}
```

### Interface Segregation Principle (ISP)

Ne pas forcer un client à dépendre de méthodes qu'il n'utilise pas. Préférer plusieurs interfaces fines et cohésives à une interface "fat".

```typescript
// VIOLATION : interface trop large
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
  attendMeeting(): void;
}

// CORRECT : interfaces ségréguées
interface Workable { work(): void; }
interface Feedable { eat(): void; }
interface Restable { sleep(): void; }
interface MeetingAttendee { attendMeeting(): void; }

// Un robot n'a pas besoin de manger ni dormir
class RobotWorker implements Workable {
  work(): void { /* ... */ }
}

// Un humain implémente les interfaces pertinentes
class HumanWorker implements Workable, Feedable, Restable, MeetingAttendee {
  work(): void { /* ... */ }
  eat(): void { /* ... */ }
  sleep(): void { /* ... */ }
  attendMeeting(): void { /* ... */ }
}
```

### Dependency Inversion Principle (DIP)

Les modules de haut niveau ne doivent pas dépendre de modules de bas niveau. Les deux doivent dépendre d'abstractions. Les abstractions ne doivent pas dépendre des détails.

```typescript
// VIOLATION : couplage direct à une implémentation concrète
class UserService {
  private db = new PostgresDatabase(); // dépendance concrète
  private mailer = new SendGridMailer(); // dépendance concrète

  async createUser(data: UserData): Promise<User> {
    const user = User.create(data);
    await this.db.insert('users', user);
    await this.mailer.send(user.email, 'Welcome!');
    return user;
  }
}

// CORRECT : injection de dépendances via abstractions
interface UserRepository {
  save(user: User): Promise<void>;
}

interface EmailService {
  send(to: Email, subject: string, body: string): Promise<void>;
}

class UserService {
  constructor(
    private readonly userRepo: UserRepository,
    private readonly emailService: EmailService
  ) {}

  async createUser(data: UserData): Promise<User> {
    const user = User.create(data);
    await this.userRepo.save(user);
    await this.emailService.send(user.email, 'Welcome!', welcomeBody(user));
    return user;
  }
}
```

---

## DRY, KISS, YAGNI -- Applied

### DRY : Éliminer la duplication de logique

Distinguer trois types de duplication :

1. **Duplication de code** (la plus visible) : deux blocs de code identiques. Extraire dans une fonction.
2. **Duplication de logique** (la plus dangereuse) : deux implémentations différentes de la même règle métier. Centraliser dans un module unique.
3. **Duplication accidentelle** (piège à éviter) : deux blocs de code similaires mais appartenant à des contextes métier différents. Ne PAS factoriser -- leur évolution sera divergente.

```typescript
// Duplication accidentelle : ne PAS factoriser
// Le calcul de la remise employé et le calcul de la remise client
// peuvent sembler identiques aujourd'hui mais évolueront différemment
function calculateEmployeeDiscount(price: Money): Money {
  return price.multiply(0.15); // politique RH
}

function calculateLoyaltyDiscount(price: Money): Money {
  return price.multiply(0.15); // politique commerciale
}
// Garder séparés : demain, la politique RH pourrait passer à 20%
// sans affecter la remise fidélité
```

### KISS : La simplicité comme force

Évaluer chaque solution en se demandant : "Un développeur junior peut-il comprendre ce code en 30 secondes ?"

Signes de complexité inutile :
- Abstraction prématurée (créer une interface pour une seule implémentation qui n'a pas de raison d'en avoir plusieurs).
- Pattern utilisé par anticipation ("on aura sûrement besoin d'un Observer ici un jour").
- Generics/templates inutiles sur du code qui ne gère qu'un seul type en pratique.

### YAGNI : Coder pour aujourd'hui, concevoir pour demain

Ne jamais implémenter une fonctionnalité sur la base d'un besoin futur hypothétique. Cela ne signifie pas ignorer l'architecture -- concevoir le code de manière à ce qu'il soit facile à étendre, mais n'implémenter que ce qui est requis maintenant.

**Règle pratique** : si personne n'a demandé cette fonctionnalité dans un ticket ou une spécification, ne pas la coder.

---

## Naming Conventions

### Principes fondamentaux du nommage

Appliquer ces règles systématiquement :

1. **Révéler l'intention** : le nom doit répondre à "pourquoi ça existe, que fait-il, comment l'utiliser" sans lire l'implémentation.
2. **Éviter la désinformation** : ne pas utiliser `list` dans un nom si ce n'est pas une liste. Ne pas utiliser `Manager`/`Handler`/`Processor` comme suffixes fourre-tout.
3. **Faire des distinctions significatives** : `productInfo` vs `productData` ne transmet aucune distinction. Préférer `productSummary` vs `productDetails`.
4. **Utiliser des noms prononçables et cherchables** : `genYMDHMS` est incompréhensible, `generatedTimestamp` est clair.

### Conventions par type d'élément

```
Variables/propriétés : nom ou groupe nominal décrivant le contenu
  - activeUsers, unpaidInvoiceCount, lastLoginDate

Fonctions/méthodes : verbe + complément décrivant l'action
  - calculateShippingCost(), sendWelcomeEmail(), findUserByEmail()

Booléens : question avec is/has/can/should
  - isActive, hasPermission, canRetry, shouldNotify

Classes : nom singulier décrivant la responsabilité
  - InvoiceCalculator, UserRepository, PaymentGateway

Interfaces : capacité ou contrat (éviter le préfixe I en TS/Java moderne)
  - Serializable, PaymentProcessor, EventListener

Constantes : UPPER_SNAKE_CASE avec contexte
  - MAX_RETRY_ATTEMPTS, DEFAULT_PAGE_SIZE, API_BASE_URL

Enums : singulier pour le type, valeurs descriptives
  - enum OrderStatus { Pending, Confirmed, Shipped, Delivered, Cancelled }
```

### Longueur des noms

Adapter la longueur à la portée :
- **Variable de boucle** (portée 3 lignes) : `i`, `item` acceptable.
- **Variable locale** (portée 20 lignes) : `filteredOrders`, `remainingAttempts`.
- **Champ de classe** (portée 200 lignes) : `maximumConcurrentConnections`, `unpaidInvoiceRepository`.
- **Fonction publique** (portée globale) : nom complet et non ambigu `calculateAnnualRevenueByRegion()`.

---

## Complexity Management

### Complexité cyclomatique

Mesurer le nombre de chemins indépendants dans le code. Chaque `if`, `else`, `case`, `&&`, `||`, `catch`, boucle ajoute un chemin.

| Complexité cyclomatique | Interprétation | Action |
|---|---|---|
| 1-5 | Simple, facile à tester | Maintenir |
| 6-10 | Modérément complexe | Surveiller |
| 11-20 | Complexe, difficile à tester | Refactorer |
| 21+ | Très risqué, non testable | Refactorer immédiatement |

**Règle** : maintenir chaque fonction sous une complexité cyclomatique de 10. Configurer un quality gate dans le CI.

### Complexité cognitive (SonarQube)

Plus pertinente que la complexité cyclomatique car elle mesure la difficulté de compréhension humaine. Elle pénalise :
- L'imbrication (chaque niveau d'indentation augmente le coût cognitif).
- Les ruptures de flux linéaire (sauts, `break`, `continue`).
- Les structures récursives.

```typescript
// Complexité cognitive ÉLEVÉE (imbrication profonde)
function processOrder(order: Order): Result {
  if (order.items.length > 0) {                     // +1
    if (order.customer.isVerified) {                 // +2 (imbriqué)
      for (const item of order.items) {              // +3 (imbriqué x2)
        if (item.stock > 0) {                        // +4 (imbriqué x3)
          if (item.price > 0) {                      // +5 (imbriqué x4)
            // traitement
          }
        }
      }
    }
  }
  return result;
}
// Total : 15 -- trop élevé

// Complexité cognitive RÉDUITE (early returns, extraction)
function processOrder(order: Order): Result {
  if (order.items.length === 0) return Result.empty();      // +1
  if (!order.customer.isVerified) return Result.denied();   // +1

  const validItems = order.items.filter(isAvailableAndPriced); // +0
  return processValidItems(validItems);                        // +0
}
// Total : 2 -- excellent
```

### Stratégies de réduction de la complexité

1. **Guard clauses (early return)** : traiter les cas d'erreur en premier et retourner immédiatement. Réduire l'imbrication.
2. **Extract method** : isoler chaque bloc logique dans une méthode nommée selon son intention.
3. **Replace conditional with polymorphism** : remplacer les switch/if-else en cascade par des stratégies polymorphiques.
4. **Replace nested conditional with pipeline** : utiliser `map`, `filter`, `reduce` pour linéariser le flux de données.
5. **Introduce parameter object** : regrouper les paramètres liés dans un objet dédié quand une fonction a plus de 3 paramètres.

---

## Code Readability

### Structurer le code comme un article

Organiser le code dans un fichier selon le principe du "journal" (Newspaper Rule de Clean Code) :
1. **En haut** : les déclarations publiques, le contrat, le "quoi".
2. **Au milieu** : les méthodes intermédiaires, l'orchestration.
3. **En bas** : les détails d'implémentation privés, le "comment".

Un lecteur doit pouvoir comprendre le "quoi" en lisant le haut du fichier sans descendre dans les détails.

### Limites de taille recommandées

| Élément | Maximum recommandé | Seuil d'alerte |
|---|---|---|
| Fonction/méthode | 20 lignes | 30 lignes |
| Classe/module | 200 lignes | 300 lignes |
| Fichier | 300 lignes | 500 lignes |
| Paramètres de fonction | 3 | 4+ |
| Niveaux d'imbrication | 2 | 3+ |

### Les commentaires comme signal d'alerte

Un commentaire n'est nécessaire que dans ces cas :
- **Explication du "pourquoi"** : contexte métier, contrainte réglementaire, workaround pour un bug externe.
- **Documentation d'API publique** : JSDoc/docstring pour les interfaces consommées par d'autres équipes.
- **TODO/FIXME avec ticket** : `// TODO(JIRA-1234): migrer vers le nouveau calcul de TVA`.

Supprimer systématiquement :
- Les commentaires qui paraphrasent le code (`// incrémente le compteur` avant `counter++`).
- Le code commenté (utiliser git pour l'historique).
- Les commentaires de section (`// --- GETTERS ---`) qui compensent un fichier trop long.

---

## Design Patterns for Modern Development

### Patterns fréquemment utiles

#### Strategy Pattern
Remplacer les conditions en cascade par des stratégies interchangeables. C'est le pattern le plus utilisé dans le code moderne, souvent via l'injection de dépendances.

```typescript
interface PricingStrategy {
  calculate(basePrice: Money, context: PricingContext): Money;
}

class StandardPricing implements PricingStrategy {
  calculate(basePrice: Money, context: PricingContext): Money {
    return basePrice;
  }
}

class PremiumPricing implements PricingStrategy {
  calculate(basePrice: Money, context: PricingContext): Money {
    return basePrice.multiply(0.85); // 15% discount
  }
}

class SeasonalPricing implements PricingStrategy {
  calculate(basePrice: Money, context: PricingContext): Money {
    const factor = this.getSeasonalFactor(context.date);
    return basePrice.multiply(factor);
  }
}
```

#### Builder Pattern (pour les tests)
Construire des objets de test lisibles et maintenables.

```typescript
class OrderBuilder {
  private props: Partial<OrderProps> = {
    id: OrderId.generate(),
    status: OrderStatus.Pending,
    items: [],
    createdAt: new Date(),
  };

  withStatus(status: OrderStatus): this { this.props.status = status; return this; }
  withItem(item: OrderItem): this { this.props.items!.push(item); return this; }
  withItems(items: OrderItem[]): this { this.props.items = items; return this; }
  paidOn(date: Date): this { this.props.status = OrderStatus.Paid; this.props.paidAt = date; return this; }

  build(): Order { return Order.reconstitute(this.props as OrderProps); }
}

// Usage dans les tests -- clair et expressif
const paidOrder = new OrderBuilder()
  .withItem(aLineItem().withProduct('Widget').withQuantity(3).build())
  .paidOn(new Date('2025-06-15'))
  .build();
```

#### Repository Pattern
Abstraire l'accès aux données pour isoler la logique métier de la persistance. Incontournable pour la testabilité.

```typescript
interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: OrderId): Promise<Order | null>;
  findByCustomer(customerId: CustomerId): Promise<Order[]>;
  findUnpaidOlderThan(date: Date): Promise<Order[]>;
}

// Implémentation concrète pour production
class PostgresOrderRepository implements OrderRepository { /* ... */ }

// Implémentation in-memory pour les tests
class InMemoryOrderRepository implements OrderRepository {
  private orders: Map<string, Order> = new Map();
  async save(order: Order): Promise<void> { this.orders.set(order.id.value, order); }
  async findById(id: OrderId): Promise<Order | null> { return this.orders.get(id.value) ?? null; }
  /* ... */
}
```

#### Result/Either Pattern
Remplacer les exceptions pour le flux de contrôle métier par des types de retour explicites.

```typescript
type Result<T, E = Error> =
  | { success: true; value: T }
  | { success: false; error: E };

class UserService {
  async register(data: RegistrationData): Promise<Result<User, RegistrationError>> {
    const existingUser = await this.userRepo.findByEmail(data.email);
    if (existingUser) {
      return { success: false, error: new EmailAlreadyTakenError(data.email) };
    }

    const user = User.create(data);
    await this.userRepo.save(user);
    return { success: true, value: user };
  }
}
```

### Patterns à utiliser avec discernement

- **Singleton** : privilégier l'injection de dépendances. Le Singleton rend le code difficile à tester et crée un couplage global.
- **Observer** : utile pour le découplage événementiel mais rend le flux d'exécution difficile à tracer. Préférer des event bus explicites.
- **Abstract Factory** : rarement justifié dans les applications modernes utilisant des conteneurs d'injection de dépendances.
- **Decorator** : puissant pour ajouter des comportements transversaux (logging, caching, retry) sans modifier le code existant. À utiliser quand OCP l'exige.

### Value Objects

Encapsuler les concepts métier dans des types dédiés plutôt que des primitives. C'est l'un des patterns les plus impactants sur la qualité du code.

```typescript
// AVANT : primitive obsession
function createUser(name: string, email: string, age: number): User { /* ... */ }
// Rien n'empêche d'appeler createUser(email, name, -5)

// APRÈS : Value Objects
class Email {
  private constructor(readonly value: string) {}
  static create(raw: string): Result<Email, InvalidEmailError> {
    if (!EMAIL_REGEX.test(raw)) return { success: false, error: new InvalidEmailError(raw) };
    return { success: true, value: new Email(raw.toLowerCase().trim()) };
  }
}

class Age {
  private constructor(readonly value: number) {}
  static create(raw: number): Result<Age, InvalidAgeError> {
    if (raw < 0 || raw > 150) return { success: false, error: new InvalidAgeError(raw) };
    return { success: true, value: new Age(Math.floor(raw)) };
  }
}

function createUser(name: UserName, email: Email, age: Age): User { /* ... */ }
// Impossible de mélanger les paramètres, validation garantie à la construction
```

---

## Summary Checklist

Vérifier ces points sur chaque contribution de code :

- [ ] Chaque classe/module a une seule responsabilité clairement identifiable
- [ ] Les dépendances sont injectées via des abstractions, pas des concrétions
- [ ] Les noms révèlent l'intention sans nécessiter de commentaire explicatif
- [ ] La complexité cyclomatique de chaque fonction est inférieure à 10
- [ ] Aucune imbrication ne dépasse 2 niveaux
- [ ] Les concepts métier sont encapsulés dans des Value Objects
- [ ] Le code se lit de haut en bas comme un article
- [ ] Les commentaires expliquent le "pourquoi", jamais le "quoi"
- [ ] Aucune duplication de logique métier n'existe
- [ ] Les patterns utilisés sont justifiés par un besoin réel, pas par anticipation
