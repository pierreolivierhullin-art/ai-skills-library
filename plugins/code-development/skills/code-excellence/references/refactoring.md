# Refactoring & Technical Debt

Référence approfondie sur les techniques de refactoring, la gestion du legacy code et la maîtrise de la dette technique.

---

## Table of Contents

1. [Refactoring Fundamentals](#refactoring-fundamentals)
2. [Refactoring Catalog](#refactoring-catalog)
3. [Working with Legacy Code](#working-with-legacy-code)
4. [Strangler Fig Pattern](#strangler-fig-pattern)
5. [Branch by Abstraction](#branch-by-abstraction)
6. [Incremental Modernization](#incremental-modernization)
7. [Technical Debt Identification & Management](#technical-debt-identification--management)
8. [Code Smells Catalog](#code-smells-catalog)

---

## Refactoring Fundamentals

### Définition

Le refactoring est la modification de la structure interne du code sans altérer son comportement observable externe. Il ne s'agit pas de :
- Corriger des bugs (c'est du bug fixing).
- Ajouter des fonctionnalités (c'est du développement).
- Optimiser les performances (c'est de l'optimisation).

Le refactoring est un investissement dans la maintenabilité qui se rembourse par une vélocité accrue sur les modifications futures.

### Préconditions absolues

Avant tout refactoring, vérifier ces conditions :

1. **Des tests existent** : ne jamais refactorer sans filet de sécurité. Si les tests n'existent pas, les écrire d'abord (tests de caractérisation).
2. **Les tests passent** : partir d'un état vert. Un refactoring commence vert et se termine vert.
3. **Les commits sont petits** : chaque étape de refactoring est un commit autonome. Pouvoir revenir en arrière à tout moment.
4. **Le code est sous version control** : évident, mais critique pour pouvoir annuler.

### Le workflow de refactoring

```
1. S'assurer que les tests passent (GREEN)
2. Identifier un code smell ou une amélioration structurelle
3. Appliquer UNE transformation de refactoring
4. Lancer les tests → doivent passer (GREEN)
5. Commiter
6. Répéter
```

Ne jamais combiner refactoring et changement de comportement dans le même commit. Séparer clairement les deux types de modifications.

---

## Refactoring Catalog

### Extract Method / Extract Function

**Quand** : un bloc de code au sein d'une méthode a une intention distincte identifiable.
**Pourquoi** : améliorer la lisibilité, permettre la réutilisation, réduire la complexité.

```typescript
// AVANT
function printOwing(invoice: Invoice): void {
  let outstanding = 0;

  console.log('***********************');
  console.log('**** Customer Owes ****');
  console.log('***********************');

  for (const order of invoice.orders) {
    outstanding += order.amount;
  }

  const today = new Date();
  invoice.dueDate = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 30);

  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
  console.log(`due: ${invoice.dueDate.toLocaleDateString()}`);
}

// APRÈS
function printOwing(invoice: Invoice): void {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  recordDueDate(invoice);
  printDetails(invoice, outstanding);
}

function printBanner(): void {
  console.log('***********************');
  console.log('**** Customer Owes ****');
  console.log('***********************');
}

function calculateOutstanding(invoice: Invoice): number {
  return invoice.orders.reduce((sum, order) => sum + order.amount, 0);
}

function recordDueDate(invoice: Invoice): void {
  const today = new Date();
  invoice.dueDate = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 30);
}

function printDetails(invoice: Invoice, outstanding: number): void {
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
  console.log(`due: ${invoice.dueDate.toLocaleDateString()}`);
}
```

### Inline Method / Inline Function

**Quand** : le corps de la fonction est aussi clair que son nom, ou la fonction ne fait qu'un appel délégué sans valeur ajoutée.
**Pourquoi** : éliminer l'indirection inutile.

```typescript
// AVANT : indirection sans valeur
function getRating(driver: Driver): number {
  return moreThanFiveLateDeliveries(driver) ? 2 : 1;
}
function moreThanFiveLateDeliveries(driver: Driver): boolean {
  return driver.numberOfLateDeliveries > 5;
}

// APRÈS
function getRating(driver: Driver): number {
  return driver.numberOfLateDeliveries > 5 ? 2 : 1;
}
```

### Rename Variable / Rename Method / Rename Class

**Quand** : le nom actuel ne révèle pas l'intention ou est trompeur.
**Pourquoi** : le nommage est l'outil de documentation le plus puissant.

Appliquer systématiquement ces renommages lors de chaque revue de code. Un mauvais nom est une dette technique immédiate.

```typescript
// AVANT
const d = new Date();        // d quoi ?
const a = items.filter(x => x.s > 0);  // a quoi ? s quoi ?
function calc(o: any): number { /* ... */ }  // calc quoi ?

// APRÈS
const orderDate = new Date();
const availableItems = items.filter(item => item.stockQuantity > 0);
function calculateShippingCost(order: Order): Money { /* ... */ }
```

### Move Method / Move Field

**Quand** : une méthode ou un champ utilise davantage les données d'une autre classe que de la sienne.
**Pourquoi** : améliorer la cohésion, réduire le couplage.

**Heuristique** : si une méthode de la classe A appelle 3 méthodes de la classe B et 0 de la classe A, elle appartient probablement à B (Feature Envy).

### Replace Conditional with Polymorphism

**Quand** : un switch/case ou une cascade de if/else sélectionne un comportement basé sur un type.
**Pourquoi** : respecter OCP, faciliter l'extension.

```typescript
// AVANT
function calculatePay(employee: Employee): Money {
  switch (employee.type) {
    case 'engineer':
      return employee.baseSalary.add(employee.bonus);
    case 'manager':
      return employee.baseSalary.add(employee.bonus).add(employee.stockOptions);
    case 'intern':
      return employee.stipend;
    default:
      throw new Error(`Unknown employee type: ${employee.type}`);
  }
}

// APRÈS
interface PayCalculator {
  calculate(): Money;
}

class EngineerPay implements PayCalculator {
  constructor(private employee: Engineer) {}
  calculate(): Money { return this.employee.baseSalary.add(this.employee.bonus); }
}

class ManagerPay implements PayCalculator {
  constructor(private employee: Manager) {}
  calculate(): Money {
    return this.employee.baseSalary.add(this.employee.bonus).add(this.employee.stockOptions);
  }
}

class InternPay implements PayCalculator {
  constructor(private employee: Intern) {}
  calculate(): Money { return this.employee.stipend; }
}
```

### Introduce Parameter Object

**Quand** : plusieurs paramètres voyagent toujours ensemble.
**Pourquoi** : réduire le nombre de paramètres, révéler un concept métier implicite.

```typescript
// AVANT
function findTransactions(
  startDate: Date,
  endDate: Date,
  minAmount: number,
  maxAmount: number,
  accountId: string
): Transaction[] { /* ... */ }

// APRÈS
interface TransactionFilter {
  dateRange: DateRange;
  amountRange: MoneyRange;
  accountId: AccountId;
}

function findTransactions(filter: TransactionFilter): Transaction[] { /* ... */ }
```

### Replace Magic Number with Symbolic Constant

```typescript
// AVANT
if (password.length < 8) { /* ... */ }
if (retryCount > 3) { /* ... */ }
const tax = price * 0.2;

// APRÈS
const MIN_PASSWORD_LENGTH = 8;
const MAX_RETRY_ATTEMPTS = 3;
const VAT_RATE_FRANCE = 0.2;

if (password.length < MIN_PASSWORD_LENGTH) { /* ... */ }
if (retryCount > MAX_RETRY_ATTEMPTS) { /* ... */ }
const tax = price * VAT_RATE_FRANCE;
```

### Decompose Conditional

**Quand** : une condition complexe masque l'intention.

```typescript
// AVANT
if (date.getMonth() >= 6 && date.getMonth() <= 8 && !isHoliday(date) && bookings > capacity * 0.8) {
  charge = quantity * summerRate * 1.1;
} else {
  charge = quantity * regularRate;
}

// APRÈS
if (isSummerPeak(date, bookings, capacity)) {
  charge = summerPeakCharge(quantity);
} else {
  charge = regularCharge(quantity);
}
```

### Replace Temp with Query

**Quand** : une variable temporaire est calculée une fois et utilisée ensuite. Extraire le calcul dans une méthode nommée.

```typescript
// AVANT
function calculateTotal(order: Order): Money {
  const basePrice = order.quantity * order.unitPrice;
  const discount = Math.max(0, order.quantity - 100) * order.unitPrice * 0.05;
  const shipping = Math.min(basePrice * 0.1, Money.of(50));
  return Money.of(basePrice - discount + shipping);
}

// APRÈS
class Order {
  get basePrice(): Money { return this.quantity * this.unitPrice; }
  get volumeDiscount(): Money { return Math.max(0, this.quantity - 100) * this.unitPrice * 0.05; }
  get shippingCost(): Money { return Money.min(this.basePrice.multiply(0.1), Money.of(50)); }
  get total(): Money { return this.basePrice.subtract(this.volumeDiscount).add(this.shippingCost); }
}
```

---

## Working with Legacy Code

### La définition de Michael Feathers

Le legacy code est du code sans tests. Indépendamment de son âge ou de sa technologie, un code sans tests est un code qu'on ne peut pas modifier en confiance.

### Étape 1 : Écrire des tests de caractérisation

Avant de modifier du legacy code, écrire des tests qui capturent le comportement actuel, même s'il contient des bugs.

```typescript
// Test de caractérisation : capturer le comportement actuel
describe('LegacyPricingEngine (characterization)', () => {
  it('calculates price for standard product', () => {
    const engine = new LegacyPricingEngine();
    // On ne sait pas si 107.10 est "correct", mais c'est le comportement actuel
    expect(engine.calculatePrice('STANDARD', 100, 'FR')).toBeCloseTo(107.10, 2);
  });

  it('calculates price for premium product with discount', () => {
    expect(engine.calculatePrice('PREMIUM', 200, 'US')).toBeCloseTo(185.50, 2);
  });

  // Ajouter autant de cas que nécessaire pour couvrir les chemins existants
});
```

### Étape 2 : Identifier les seams (points de jointure)

Un seam est un endroit du code où on peut modifier le comportement sans modifier le code lui-même. Types de seams :

- **Object seam** : substituer une dépendance par un test double via l'héritage ou l'injection.
- **Preprocessing seam** : utiliser le préprocesseur ou la configuration pour substituer un comportement (C/C++).
- **Link seam** : substituer une implémentation au moment du linking ou du chargement de module.

```typescript
// Legacy code avec dépendance directe (non testable)
class ReportGenerator {
  generate(): Report {
    const data = Database.query('SELECT * FROM sales'); // dépendance statique
    // ... logique complexe
  }
}

// Introduire un seam par extraction de paramètre
class ReportGenerator {
  generate(dataSource: DataSource = new DatabaseSource()): Report {
    const data = dataSource.fetchSales();
    // ... logique complexe
  }
}

// Maintenant testable :
test('generates report from sales data', () => {
  const fakeSource = new FakeDataSource([sale1, sale2, sale3]);
  const report = new ReportGenerator().generate(fakeSource);
  expect(report.totalRevenue).toBe(Money.of(450));
});
```

### Étape 3 : Sprout Method / Sprout Class

Quand on doit ajouter une fonctionnalité à du legacy code non testable, ne pas modifier le code existant. Faire "pousser" (sprout) le nouveau code dans une méthode ou classe séparée, entièrement testée.

```typescript
// Legacy code non testable
class OrderProcessor {
  process(order: Order): void {
    // 200 lignes de logique opaque non testée
    // On doit ajouter la validation des adresses

    // SPROUT METHOD : ajouter la nouvelle logique dans une méthode testée indépendamment
    const validationResult = this.validateShippingAddress(order.shippingAddress);
    if (!validationResult.isValid) {
      throw new InvalidAddressError(validationResult.errors);
    }

    // ... reste du legacy code
  }

  // Nouvelle méthode entièrement testable
  validateShippingAddress(address: Address): ValidationResult {
    // Logique propre, testée en TDD
  }
}
```

### Étape 4 : Wrap Method / Wrap Class

Encapsuler le code legacy existant dans un wrapper qui ajoute le comportement souhaité sans modifier l'original.

```typescript
// Wrap Class : ajouter du logging sans modifier la classe legacy
class LoggingOrderProcessor implements OrderProcessor {
  constructor(
    private readonly inner: LegacyOrderProcessor,
    private readonly logger: Logger
  ) {}

  process(order: Order): void {
    this.logger.info(`Processing order ${order.id}`, { items: order.items.length });
    const startTime = performance.now();

    this.inner.process(order); // délègue au legacy

    const duration = performance.now() - startTime;
    this.logger.info(`Order ${order.id} processed in ${duration}ms`);
  }
}
```

---

## Strangler Fig Pattern

### Principe

Remplacer progressivement un système legacy par un nouveau système en détournant le trafic route par route, fonctionnalité par fonctionnalité. Le nouveau système "étrangle" l'ancien comme un figuier étrangleur entoure un arbre hôte.

### Étapes de mise en oeuvre

```
Phase 1 : INTERCEPT
  Placer un proxy/router devant le système legacy qui route
  100% du trafic vers l'ancien système.

Phase 2 : IMPLEMENT
  Implémenter la première fonctionnalité dans le nouveau système.
  Le proxy route cette fonctionnalité vers le nouveau système,
  le reste vers l'ancien.

Phase 3 : MIGRATE
  Migrer progressivement les fonctionnalités une par une.
  À chaque étape, le nouveau système prend en charge une part
  croissante du trafic.

Phase 4 : RETIRE
  Quand 100% du trafic est routé vers le nouveau système,
  décommissionner l'ancien.
```

### Implémentation concrète

```typescript
// Router/proxy qui permet la migration progressive
class OrderRouter {
  constructor(
    private readonly legacyService: LegacyOrderService,
    private readonly newService: ModernOrderService,
    private readonly featureFlags: FeatureFlags
  ) {}

  async createOrder(request: CreateOrderRequest): Promise<OrderResponse> {
    if (this.featureFlags.isEnabled('new-order-creation')) {
      return this.newService.createOrder(request);
    }
    return this.legacyService.createOrder(request);
  }

  async getOrder(id: string): Promise<OrderResponse> {
    // Déjà migré
    return this.newService.getOrder(id);
  }

  async cancelOrder(id: string): Promise<void> {
    // Pas encore migré
    return this.legacyService.cancelOrder(id);
  }
}
```

### Parallel Run (Shadow Mode)

Avant de basculer le trafic, exécuter les deux systèmes en parallèle et comparer les résultats :

```typescript
async createOrder(request: CreateOrderRequest): Promise<OrderResponse> {
  const legacyResult = await this.legacyService.createOrder(request);

  // Shadow mode : exécuter le nouveau service en parallèle sans impacter l'utilisateur
  this.newService.createOrder(request)
    .then(newResult => {
      if (!deepEqual(legacyResult, newResult)) {
        this.logger.warn('Result mismatch', { legacy: legacyResult, new: newResult });
        this.metrics.increment('strangler.mismatch', { route: 'createOrder' });
      }
    })
    .catch(error => {
      this.logger.error('New service error in shadow mode', { error });
    });

  return legacyResult; // toujours retourner le résultat legacy en shadow mode
}
```

---

## Branch by Abstraction

### Principe

Remplacer une dépendance ou une implémentation dans un système en production sans créer une branche longue. Utiliser une abstraction (interface) pour permettre la coexistence temporaire de l'ancienne et de la nouvelle implémentation.

### Les étapes

```
1. ABSTRACT : créer une abstraction (interface) au-dessus de l'implémentation actuelle.
2. ADAPT : faire implémenter cette abstraction par le code existant.
3. CLIENT MIGRATION : faire dépendre tous les clients de l'abstraction (pas de la concrétions).
4. NEW IMPLEMENTATION : créer la nouvelle implémentation derrière la même abstraction.
5. SWITCH : basculer vers la nouvelle implémentation (via config, feature flag).
6. CLEANUP : supprimer l'ancienne implémentation et, si nécessaire, l'abstraction.
```

```typescript
// Étape 1-2 : Créer l'abstraction et adapter l'existant
interface NotificationSender {
  send(userId: UserId, message: NotificationMessage): Promise<void>;
}

class LegacyEmailNotifier implements NotificationSender {
  async send(userId: UserId, message: NotificationMessage): Promise<void> {
    // ancien code SMTP direct
  }
}

// Étape 3 : Les clients utilisent l'abstraction
class OrderService {
  constructor(private readonly notifier: NotificationSender) {}
  // ...
}

// Étape 4 : Nouvelle implémentation
class ModernNotificationService implements NotificationSender {
  async send(userId: UserId, message: NotificationMessage): Promise<void> {
    // nouveau service via API, multi-canal (email + push + SMS)
  }
}

// Étape 5 : Basculer via configuration
// container.register(NotificationSender, ModernNotificationService);
```

---

## Incremental Modernization

### La stratégie de la tranche verticale

Moderniser par tranches verticales (fonctionnalité complète du frontend à la DB) plutôt que par couches horizontales (d'abord toute la DB, puis tout le backend, etc.).

```
ÉVITER (modernisation horizontale) :
  Sprint 1 : migrer toute la base de données
  Sprint 2 : réécrire tout le backend
  Sprint 3 : réécrire tout le frontend
  → Risque maximal, valeur livrée à la fin uniquement

PRÉFÉRER (modernisation verticale) :
  Sprint 1 : migrer la fonctionnalité "Commandes" (DB + API + UI)
  Sprint 2 : migrer la fonctionnalité "Catalogue" (DB + API + UI)
  Sprint 3 : migrer la fonctionnalité "Paiement" (DB + API + UI)
  → Valeur livrée à chaque sprint, risque contenu
```

### Prioriser avec la matrice Business Value / Technical Risk

```
                    Business Value élevée
                           │
            ┌──────────────┼──────────────┐
            │   QUICK WIN  │  STRATEGIC   │
            │  Priorité 2  │  Priorité 1  │
            │              │              │
  Risque ───┼──────────────┼──────────────┤
  faible    │              │              │  Risque
            │   IGNORE     │  DELEGATE    │  élevé
            │  Priorité 4  │  Priorité 3  │
            │              │              │
            └──────────────┼──────────────┘
                           │
                    Business Value faible
```

### Le "Mikado Method" pour les gros refactorings

Utiliser la méthode Mikado pour décomposer un refactoring complexe en étapes réalisables :

1. Définir l'objectif final du refactoring.
2. Essayer d'appliquer le changement directement.
3. Quand ça casse, noter ce qui empêche le changement (prérequis).
4. Annuler (revert) le changement.
5. Résoudre les prérequis un par un (chacun étant un sous-objectif).
6. Répéter récursivement jusqu'à ce que l'objectif soit atteignable.

Cela produit un graphe de dépendances (le "Mikado Graph") qu'on résout des feuilles vers la racine.

---

## Technical Debt Identification & Management

### Les quatre quadrants de la dette technique (Martin Fowler)

```
                    Délibérée
                       │
           ┌───────────┼───────────┐
           │ PRUDENTE   │ PRUDENTE  │
           │ DÉLIBÉRÉE  │ INVOLON-  │
           │            │ TAIRE     │
           │ "On sait   │ "On       │
           │  qu'on     │  découvre │
 Prudente ─┤  coupe     │  après    ├─ Imprudente
           │  ici pour  │  coup     │
           │  livrer"   │  qu'on    │
           │            │  aurait   │
           │ IMPRUDENTE │  dû..."   │
           │ DÉLIBÉRÉE  │ IMPRUD.   │
           │            │ INVOLON.  │
           │ "Pas le    │ "C'est    │
           │  temps de  │  quoi un  │
           │  designer" │  design?" │
           └───────────┼───────────┘
                       │
                  Involontaire
```

- **Prudente/Délibérée** : dette acceptée consciemment avec un plan de remboursement. "Expédions maintenant, on refactorera dans le sprint suivant."
- **Prudente/Involontaire** : dette découverte après coup. "Maintenant qu'on comprend mieux le domaine, on voit que notre modèle est inadapté."
- **Imprudente/Délibérée** : dette par négligence consciente. "Pas le temps de faire des tests." La plus dangereuse.
- **Imprudente/Involontaire** : dette par incompétence. Nécessite de la formation.

### Identifier la dette technique

#### Métriques automatisables

| Métrique | Outil | Seuil d'alerte |
|---|---|---|
| Complexité cyclomatique | SonarQube, ESLint | > 15 par fonction |
| Duplication de code | SonarQube, jscpd | > 5% |
| Code churn (fichiers souvent modifiés) | `git log --stat`, CodeScene | Top 10% = hotspots |
| Coupling (dépendances entrantes/sortantes) | deptree, Madge, NDepend | Afferent coupling > 20 |
| Âge des TODO/FIXME | grep + git blame | > 3 mois |
| Temps de build/test | CI metrics | Augmentation > 20% sur 3 mois |

#### Analyse qualitative

- **Onboarding time** : combien de temps pour qu'un nouveau développeur soit productif dans ce module ? Si > 2 semaines, il y a dette.
- **Fear factor** : quels fichiers/modules l'équipe a peur de toucher ? Ce sont les hotspots critiques.
- **Bug clustering** : quels modules concentrent le plus de bugs ? Corrélation forte avec la dette.

### Gérer la dette technique

#### La règle du 20%

Allouer 20% de chaque sprint au remboursement de dette technique. Ne pas demander la permission -- c'est une pratique d'ingénierie, pas une feature.

#### Le Tech Debt Register

Maintenir un registre vivant de la dette technique :

```markdown
| ID | Description | Impact | Effort | Priorité | Responsable | Deadline |
|----|-------------|--------|--------|----------|-------------|----------|
| TD-001 | God class OrderProcessor (800 lignes) | Élevé | M (3j) | P1 | Team Backend | Sprint 24 |
| TD-002 | Tests d'intégration absents sur PaymentService | Critique | L (5j) | P0 | @alice | Sprint 23 |
| TD-003 | Dépendance directe à SendGrid sans abstraction | Moyen | S (1j) | P2 | @bob | Sprint 25 |
```

#### Boy Scout Rule à l'échelle

Ne pas planifier de "sprint de dette technique". Intégrer le remboursement dans le flux normal :
- Chaque PR améliore un aspect du code touché (renommage, extraction, ajout de test).
- Les hotspots identifiés par le code churn sont les cibles prioritaires.
- Les bugs sont toujours accompagnés d'un test de non-régression et d'un refactoring du code incriminé.

---

## Code Smells Catalog

### Smells dans les fonctions

| Code Smell | Symptôme | Refactoring recommandé |
|---|---|---|
| Long Method | Fonction > 20 lignes | Extract Method |
| Long Parameter List | > 3 paramètres | Introduce Parameter Object |
| Flag Argument | Booléen qui change le comportement | Séparer en deux fonctions |
| Nested Conditionals | > 2 niveaux d'imbrication | Guard Clauses, Extract Method |
| Side Effects cachés | La fonction modifie un état non évident | Rendre l'effet explicite (nom, retour) |

### Smells dans les classes

| Code Smell | Symptôme | Refactoring recommandé |
|---|---|---|
| God Class | Classe > 200 lignes, responsabilités multiples | Extract Class par responsabilité |
| Feature Envy | Méthode qui utilise surtout les données d'une autre classe | Move Method |
| Data Clump | Mêmes groupes de données dans plusieurs endroits | Introduce Parameter Object / Value Object |
| Primitive Obsession | Types primitifs pour des concepts métier | Introduce Value Object |
| Refused Bequest | Sous-classe qui n'utilise pas les méthodes héritées | Replace Inheritance with Delegation |

### Smells dans les interactions

| Code Smell | Symptôme | Refactoring recommandé |
|---|---|---|
| Shotgun Surgery | Un changement métier touche 10+ fichiers | Move Method/Field pour centraliser |
| Divergent Change | Un fichier est modifié pour des raisons différentes | Extract Class par axe de changement |
| Message Chain | `a.getB().getC().getD().doSomething()` | Introduce intermediary, Law of Demeter |
| Middle Man | Classe qui ne fait que déléguer | Inline Class ou Remove Middle Man |
| Inappropriate Intimacy | Deux classes qui accèdent aux détails internes de l'autre | Move Method, Extract Class |

### Smells dans l'architecture

| Code Smell | Symptôme | Refactoring recommandé |
|---|---|---|
| Circular Dependencies | A dépend de B qui dépend de A | Dependency Inversion, Extract Interface |
| Dead Code | Code jamais exécuté | Delete (git est votre historique) |
| Speculative Generality | Abstractions créées "au cas où" | Inline Class, Remove Parameter |
| Parallel Inheritance | Créer une sous-classe de A oblige à créer une sous-classe de B | Merge hierarchies, Strategy pattern |

---

## Summary Checklist

Vérifier ces points pour tout travail de refactoring ou de gestion de dette technique :

- [ ] Des tests (caractérisation ou unitaires) couvrent le code à refactorer avant toute modification
- [ ] Chaque transformation de refactoring est un commit atomique (vert à vert)
- [ ] Le refactoring et les changements de comportement sont dans des commits séparés
- [ ] La dette technique est identifiée, cataloguée et priorisée dans un registre
- [ ] Les hotspots (code churn + complexité) sont les cibles prioritaires de refactoring
- [ ] 20% de la capacité du sprint est allouée au remboursement de dette
- [ ] Les patterns Strangler Fig et Branch by Abstraction sont utilisés pour les migrations progressives
- [ ] Le Mikado Method décompose les gros refactorings en étapes réalisables
- [ ] La Boy Scout Rule est appliquée sur chaque contribution
- [ ] Aucun code n'est commenté "au cas où" -- git est l'historique
