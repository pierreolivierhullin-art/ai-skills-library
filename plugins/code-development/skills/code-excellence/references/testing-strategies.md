# Testing Strategies

Référence approfondie sur les stratégies de test modernes, du TDD au contract testing.

---

## Table of Contents

1. [Test Pyramid & Modern Alternatives](#test-pyramid--modern-alternatives)
2. [Test-Driven Development (TDD)](#test-driven-development-tdd)
3. [Behavior-Driven Development (BDD)](#behavior-driven-development-bdd)
4. [Property-Based Testing](#property-based-testing)
5. [Contract Testing](#contract-testing)
6. [Snapshot Testing](#snapshot-testing)
7. [Mutation Testing](#mutation-testing)
8. [Mocking Strategies](#mocking-strategies)
9. [Meaningful Coverage vs 100%](#meaningful-coverage-vs-100)
10. [Modern Testing Tools & Approaches](#modern-testing-tools--approaches)

---

## Test Pyramid & Modern Alternatives

### La pyramide classique

La pyramide des tests (Mike Cohn) reste le modèle de base pour structurer une stratégie de test. Respecter la distribution suivante :

```
          /  E2E  \          ~10% -- lents, fragiles, coûteux
         /  (UI)   \         Scénarios critiques uniquement
        /___________\
       /             \
      / Integration   \     ~20% -- vitesse modérée
     /   (API, DB)     \    Interactions entre composants
    /___________________\
   /                     \
  /     Unit Tests        \  ~70% -- rapides, isolés
 /   (Logic, Domain)       \ Logique métier pure
/___________________________ \
```

### Le "Testing Trophy" (Kent C. Dodds)

Pour les applications frontend et full-stack modernes, considérer le Testing Trophy qui met l'accent sur les tests d'intégration :

```
          /  E2E  \          Quelques smoke tests
         /         \
        /___________\
       /             \
      / Integration   \     MAJORITÉ -- tests les plus rentables
     /  (Components,   \    Testent le comportement réel utilisateur
    /    API routes)    \
   /____________________\
   \                    /
    \   Unit Tests     /     Algorithmes et logique pure uniquement
     \________________/
      \  Static  /           TypeScript, ESLint, Prettier
       \________/
```

### Choisir le bon modèle

| Contexte | Modèle recommandé |
|---|---|
| Backend avec logique métier complexe (DDD) | Pyramide classique |
| Application frontend React/Vue/Svelte | Testing Trophy |
| Microservices avec contrats API | Pyramide + Contract testing |
| Application legacy sans tests | Tests de caractérisation d'abord |
| CLI / bibliothèque | Pyramide classique (unit-heavy) |

---

## Test-Driven Development (TDD)

### Le cycle Red-Green-Refactor

Suivre ce cycle avec discipline :

1. **RED** : écrire un test qui échoue. Ce test doit exprimer une intention de comportement, pas un détail d'implémentation. Ne pas écrire plus de code de test que nécessaire pour obtenir un échec.

2. **GREEN** : écrire le minimum de code de production pour faire passer le test. Ne pas optimiser, ne pas généraliser. L'objectif est uniquement le vert.

3. **REFACTOR** : améliorer le code de production et de test sans changer le comportement. Éliminer la duplication, améliorer les noms, extraire des abstractions.

```typescript
// Exemple TDD : implémentation d'un validateur d'email

// RED -- Test 1 : un email valide est accepté
test('should accept a valid email', () => {
  expect(isValidEmail('user@example.com')).toBe(true);
});

// GREEN -- Implémentation minimale
function isValidEmail(email: string): boolean {
  return true; // minimal pour passer le premier test
}

// RED -- Test 2 : rejeter un email sans @
test('should reject email without @', () => {
  expect(isValidEmail('userexample.com')).toBe(false);
});

// GREEN -- Ajouter la vérification minimale
function isValidEmail(email: string): boolean {
  return email.includes('@');
}

// RED -- Test 3 : rejeter un email sans domaine
test('should reject email without domain', () => {
  expect(isValidEmail('user@')).toBe(false);
});

// GREEN
function isValidEmail(email: string): boolean {
  const parts = email.split('@');
  return parts.length === 2 && parts[1].includes('.');
}

// REFACTOR -- Nettoyer et extraire
function isValidEmail(email: string): boolean {
  const [localPart, domain] = email.split('@');
  if (!localPart || !domain) return false;
  return domain.includes('.') && !domain.startsWith('.') && !domain.endsWith('.');
}
```

### Les trois lois du TDD (Robert C. Martin)

1. Ne pas écrire de code de production tant qu'un test unitaire qui échoue n'existe pas.
2. Ne pas écrire plus de test que nécessaire pour obtenir un échec (une erreur de compilation compte comme un échec).
3. Ne pas écrire plus de code de production que nécessaire pour faire passer le test qui échoue.

### Transformation Priority Premise (TPP)

Appliquer les transformations dans cet ordre de priorité lors du passage Red-Green :

1. `{} -> nil` (pas de code -> retourner nil/null)
2. `nil -> constant` (retourner une constante)
3. `constant -> variable` (introduire une variable)
4. `unconditional -> conditional` (ajouter un if)
5. `scalar -> collection` (utiliser une collection)
6. `statement -> recursion/iteration` (ajouter une boucle)
7. `value -> mutated value` (transformer une valeur)

Suivre cet ordre évite les sauts d'implémentation et maintient des incréments minimaux.

### Quand NE PAS faire de TDD

Reconnaître les situations où TDD n'est pas optimal :
- **Prototypage/spike** : explorer d'abord, stabiliser ensuite, puis écrire les tests.
- **Code fortement dépendant d'I/O** : interfaces UI, requêtes réseau -- préférer les tests d'intégration après coup.
- **Code CRUD trivial** : un test d'intégration sur le endpoint est plus pertinent qu'un test unitaire du mapper.

---

## Behavior-Driven Development (BDD)

### Écrire des spécifications en Gherkin

Exprimer les comportements attendus dans un langage partagé entre développeurs, QA et product owners.

```gherkin
Feature: Shopping cart discount application
  As a registered customer
  I want to apply a discount code to my cart
  So that I can get a reduced price on my order

  Background:
    Given I am a registered customer
    And I have items worth 100.00 EUR in my cart

  Scenario: Apply a valid percentage discount code
    Given a valid discount code "SUMMER20" for 20% off
    When I apply the discount code "SUMMER20"
    Then my cart total should be 80.00 EUR
    And the discount "SUMMER20 (-20%)" should appear on my cart

  Scenario: Apply an expired discount code
    Given an expired discount code "OLD10"
    When I apply the discount code "OLD10"
    Then I should see the error "This discount code has expired"
    And my cart total should remain 100.00 EUR

  Scenario: Apply a discount code with minimum purchase requirement
    Given a valid discount code "BIG50" requiring a minimum of 150.00 EUR
    When I apply the discount code "BIG50"
    Then I should see the error "Minimum purchase of 150.00 EUR required"
    And my cart total should remain 100.00 EUR

  Scenario Outline: Apply various discount types
    Given a valid discount code "<code>" for <type> of <value>
    When I apply the discount code "<code>"
    Then my cart total should be <expected> EUR

    Examples:
      | code     | type       | value | expected |
      | PERC10   | percentage | 10%   | 90.00    |
      | FLAT15   | flat       | 15    | 85.00    |
      | PERC50   | percentage | 50%   | 50.00    |
```

### Implémenter les step definitions

```typescript
// steps/discount.steps.ts
import { Given, When, Then } from '@cucumber/cucumber';

Given('a valid discount code {string} for {int}% off', function (code: string, percent: number) {
  this.discountCode = DiscountCode.percentage(code, percent, { expiresAt: futureDate() });
  this.discountRepository.save(this.discountCode);
});

When('I apply the discount code {string}', async function (code: string) {
  this.result = await this.cartService.applyDiscount(this.cart.id, code);
});

Then('my cart total should be {float} EUR', function (expectedTotal: number) {
  expect(this.cart.total.amount).toBeCloseTo(expectedTotal, 2);
});
```

### BDD sans Cucumber

Appliquer l'esprit BDD sans l'outillage Gherkin en structurant les tests avec `describe`/`it` de manière comportementale :

```typescript
describe('ShoppingCart', () => {
  describe('when applying a discount code', () => {
    it('should reduce the total by the discount percentage', () => { /* ... */ });
    it('should reject an expired discount code', () => { /* ... */ });
    it('should reject a code below minimum purchase threshold', () => { /* ... */ });
    it('should not allow combining two percentage discounts', () => { /* ... */ });
  });
});
```

---

## Property-Based Testing

### Principe

Au lieu de tester des exemples spécifiques, vérifier des propriétés (invariants) qui doivent être vraies pour toute entrée valide. Le framework génère des centaines d'entrées aléatoires et vérifie l'invariant.

### Exemples avec fast-check (TypeScript)

```typescript
import fc from 'fast-check';

// Propriété : encoder puis décoder doit retourner la valeur originale (round-trip)
test('JSON encode/decode roundtrip', () => {
  fc.assert(
    fc.property(fc.anything(), (value) => {
      const encoded = JSON.stringify(value);
      if (encoded !== undefined) {
        expect(JSON.parse(encoded)).toEqual(value);
      }
    })
  );
});

// Propriété : le tri d'un tableau préserve sa longueur et ses éléments
test('sorting preserves array length and elements', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      const sorted = [...arr].sort((a, b) => a - b);
      expect(sorted).toHaveLength(arr.length);
      expect(sorted.every((v, i, a) => i === 0 || a[i - 1] <= v)).toBe(true);
      // Chaque élément original est présent
      for (const item of arr) {
        expect(sorted.filter(x => x === item).length)
          .toBe(arr.filter(x => x === item).length);
      }
    })
  );
});

// Propriété métier : le montant total d'une commande est toujours >= 0
test('order total is always non-negative', () => {
  fc.assert(
    fc.property(
      fc.array(
        fc.record({
          price: fc.float({ min: 0.01, max: 10000, noNaN: true }),
          quantity: fc.integer({ min: 1, max: 100 }),
        }),
        { minLength: 1 }
      ),
      fc.float({ min: 0, max: 0.5, noNaN: true }), // discount rate
      (items, discountRate) => {
        const order = Order.create(items, discountRate);
        expect(order.total.amount).toBeGreaterThanOrEqual(0);
      }
    )
  );
});
```

### Quand utiliser le property-based testing

| Cas d'usage | Propriétés à vérifier |
|---|---|
| Sérialisation/désérialisation | Round-trip : `decode(encode(x)) === x` |
| Tri, filtrage | Idempotence, préservation de taille, ordonnancement |
| Calculs financiers | Non-négativité, conservation des totaux, commutativité |
| Parsers | Round-trip, rejet des entrées invalides |
| Structures de données | Invariants structurels après chaque opération |
| Refactoring | Équivalence : `newImpl(x) === oldImpl(x)` pour tout `x` |

---

## Contract Testing

### Principe

Valider que le contrat (schéma de requête/réponse) entre un consumer et un provider est respecté, sans nécessiter de déploiement intégré. Remplacer les tests d'intégration end-to-end coûteux par des vérifications de contrat légères.

### Avec Pact

```typescript
// Consumer side : définir les attentes
const provider = new PactV4({
  consumer: 'OrderService',
  provider: 'InventoryService',
});

describe('Inventory API contract', () => {
  it('should return stock availability for a product', async () => {
    await provider
      .addInteraction()
      .given('product SKU-123 has 42 units in stock')
      .uponReceiving('a request for stock availability')
      .withRequest('GET', '/api/inventory/SKU-123')
      .willRespondWith(200, (builder) => {
        builder.jsonBody({
          sku: 'SKU-123',
          available: 42,
          warehouse: 'EU-WEST',
        });
      })
      .executeTest(async (mockServer) => {
        const client = new InventoryClient(mockServer.url);
        const stock = await client.getStock('SKU-123');
        expect(stock.available).toBe(42);
      });
  });
});

// Provider side : vérifier le contrat publié
// Le provider Pact Verifier rejoue les interactions contre le vrai service
const verifier = new Verifier({
  providerBaseUrl: 'http://localhost:3001',
  pactUrls: ['./pacts/orderservice-inventoryservice.json'],
  stateHandlers: {
    'product SKU-123 has 42 units in stock': async () => {
      await seedDatabase({ sku: 'SKU-123', stock: 42 });
    },
  },
});
```

### Consumer-Driven vs Provider-Driven

| Approche | Quand l'utiliser |
|---|---|
| Consumer-Driven (Pact) | Le consumer définit ses besoins ; le provider s'y conforme. Idéal pour les microservices internes. |
| Provider-Driven (OpenAPI/AsyncAPI) | Le provider publie un schéma ; les consumers s'adaptent. Idéal pour les APIs publiques. |
| Bidirectional | Combiner les deux via Pactflow pour les environnements complexes. |

---

## Snapshot Testing

### Principe et usage approprié

Capturer la sortie d'un composant ou d'une fonction et la comparer à une référence enregistrée. Utile pour détecter les régressions non intentionnelles.

```typescript
// Snapshot de composant React
test('renders user profile correctly', () => {
  const { container } = render(<UserProfile user={mockUser} />);
  expect(container).toMatchSnapshot();
});

// Snapshot d'API response
test('GET /api/users returns expected structure', async () => {
  const response = await request(app).get('/api/users/1');
  expect(response.body).toMatchInlineSnapshot(`
    {
      "id": 1,
      "name": "Alice",
      "email": "alice@example.com",
      "role": "admin",
    }
  `);
});
```

### Règles d'utilisation

- **Utiliser** pour capturer des régressions sur des sorties complexes (HTML rendu, réponses API, AST).
- **Préférer les inline snapshots** (`toMatchInlineSnapshot`) pour les petites sorties -- le diff est visible directement dans le test.
- **Ne PAS utiliser** comme substitut de véritables assertions comportementales.
- **Mettre à jour** les snapshots intentionnellement (`--updateSnapshot`) après vérification manuelle, jamais en aveugle.
- **Éviter** les snapshots sur des sorties qui changent fréquemment (timestamps, IDs auto-générés) -- utiliser des matchers partiels.

---

## Mutation Testing

### Principe

Évaluer la qualité des tests en injectant des modifications (mutations) dans le code de production et en vérifiant que les tests détectent chaque mutation. Un mutant "survivant" (non détecté) indique un test manquant ou insuffisant.

### Types de mutations

| Mutation | Exemple | Ce qu'elle teste |
|---|---|---|
| Remplacement d'opérateur | `>` devient `>=` | Conditions limites |
| Remplacement de constante | `0` devient `1` | Valeurs spécifiques |
| Suppression d'instruction | `return result;` supprimé | Couverture réelle |
| Négation de condition | `if (x)` devient `if (!x)` | Branches conditionnelles |
| Remplacement de retour | `return true` devient `return false` | Assertions effectives |

### Outils et intégration

- **JavaScript/TypeScript** : Stryker Mutator (`@stryker-mutator/core`)
- **Java** : PITest
- **Python** : mutmut, cosmic-ray
- **C#** : Stryker.NET

```bash
# Exécuter Stryker sur un projet TypeScript
npx stryker run

# Résultat attendu : mutation score > 80%
# Analyser les mutants survivants pour identifier les tests manquants
```

**Règle** : viser un mutation score > 80% sur la logique métier critique. Ne pas appliquer le mutation testing sur le code d'infrastructure (overhead trop élevé pour un gain marginal).

---

## Mocking Strategies

### La hiérarchie des test doubles

Comprendre les différences et utiliser le bon type :

| Type | Comportement | Usage |
|---|---|---|
| **Dummy** | Objet passé mais jamais utilisé | Remplir un paramètre requis |
| **Stub** | Retourne des valeurs prédéfinies | Contrôler les données d'entrée |
| **Spy** | Enregistre les appels reçus | Vérifier les interactions |
| **Mock** | Stub + vérification d'appels | Tester les effets de bord |
| **Fake** | Implémentation simplifiée fonctionnelle | Remplacer un service (in-memory DB) |

### Principes de mocking sain

1. **Ne mocker que ce qui est au boundary** : I/O, base de données, appels réseau, horloge système. Ne jamais mocker la logique métier interne.

2. **Préférer les Fakes aux Mocks** pour les repositories et services :

```typescript
// PRÉFÉRER : un Fake réutilisable
class InMemoryUserRepository implements UserRepository {
  private users: Map<string, User> = new Map();

  async save(user: User): Promise<void> {
    this.users.set(user.id.value, user);
  }

  async findById(id: UserId): Promise<User | null> {
    return this.users.get(id.value) ?? null;
  }
}

// ÉVITER : des mocks jetables dans chaque test
const mockRepo = {
  save: jest.fn().mockResolvedValue(undefined),
  findById: jest.fn().mockResolvedValue(someUser),
};
// Fragile : couplé aux détails d'appel, ne vérifie pas la logique du repo
```

3. **Tester le comportement, pas l'implémentation** :

```typescript
// MAUVAIS : couplé aux détails d'appel
test('should call repository.save with correct arguments', async () => {
  await userService.register(userData);
  expect(mockRepo.save).toHaveBeenCalledWith(expect.objectContaining({ email: 'test@example.com' }));
});

// BON : vérifie le comportement observable
test('should persist the registered user', async () => {
  await userService.register(userData);
  const savedUser = await userRepo.findByEmail(Email.create('test@example.com').value);
  expect(savedUser).not.toBeNull();
  expect(savedUser!.name.value).toBe('Alice');
});
```

### Contrôler le temps et l'aléatoire

```typescript
// Injecter une Clock abstraite plutôt que dépendre de Date.now()
interface Clock {
  now(): Date;
}

class SystemClock implements Clock {
  now(): Date { return new Date(); }
}

class FixedClock implements Clock {
  constructor(private readonly date: Date) {}
  now(): Date { return this.date; }
}

// Dans les tests :
const clock = new FixedClock(new Date('2025-07-01T10:00:00Z'));
const service = new SubscriptionService(clock);
```

---

## Meaningful Coverage vs 100%

### Pourquoi 100% de couverture est un piège

La couverture de code (line coverage, branch coverage) mesure quelles lignes sont exécutées pendant les tests, pas si le comportement est correctement vérifié. Un test sans assertion qui exécute du code compte dans la couverture.

```typescript
// 100% coverage, 0% de valeur
test('processOrder does not throw', () => {
  processOrder(someOrder); // aucune assertion -- que vérifie-t-on ?
});
```

### Métriques de couverture à combiner

| Métrique | Ce qu'elle mesure | Cible |
|---|---|---|
| Line coverage | Lignes exécutées | 80%+ global |
| Branch coverage | Branches conditionnelles traversées | 75%+ |
| Mutation score | Tests qui détectent les mutations | 80%+ sur le domaine |
| Assertion density | Nombre d'assertions par test | >= 1 assertion significative |

### Stratégie de couverture par zone

```
Code métier critique (calculs, règles, validations)
  → 90%+ line coverage + 80%+ mutation score

Code d'orchestration (services, controllers)
  → 75%+ line coverage via tests d'intégration

Code d'infrastructure (config, wiring, migrations)
  → Tests de smoke / health check suffisants

Code UI (composants visuels)
  → Snapshot + tests d'interaction sur les comportements critiques
```

---

## Modern Testing Tools & Approaches

### Outils par écosystème (2024-2026)

| Écosystème | Unit/Integration | E2E | Property-Based | Contract | Mutation |
|---|---|---|---|---|---|
| TypeScript/JS | Vitest, Jest | Playwright, Cypress | fast-check | Pact, MSW | Stryker |
| Python | pytest | Playwright | Hypothesis | Pact | mutmut |
| Java/Kotlin | JUnit 5, Kotest | Selenium, Playwright | jqwik | Spring Cloud Contract, Pact | PITest |
| Go | testing + testify | Playwright | rapid | Pact | go-mutesting |
| Rust | built-in + rstest | -- | proptest | -- | cargo-mutants |
| C# | xUnit, NUnit | Playwright | FsCheck | Pact | Stryker.NET |

### Testcontainers

Utiliser Testcontainers pour les tests d'intégration nécessitant des services externes réels (bases de données, message brokers, caches) :

```typescript
import { PostgreSqlContainer } from '@testcontainers/postgresql';

describe('UserRepository integration', () => {
  let container: StartedPostgreSqlContainer;
  let repository: PostgresUserRepository;

  beforeAll(async () => {
    container = await new PostgreSqlContainer().start();
    const pool = new Pool({ connectionString: container.getConnectionUri() });
    await runMigrations(pool);
    repository = new PostgresUserRepository(pool);
  }, 60_000);

  afterAll(async () => {
    await container.stop();
  });

  it('should save and retrieve a user', async () => {
    const user = UserBuilder.aUser().build();
    await repository.save(user);
    const found = await repository.findById(user.id);
    expect(found).toEqual(user);
  });
});
```

### AI-Assisted Test Generation

Utiliser les outils d'IA (Copilot, Claude, Codium) comme accélérateur de rédaction de tests, tout en appliquant ces garde-fous :
- Toujours relire et valider les tests générés -- l'IA peut produire des tests sans assertion réelle.
- Utiliser l'IA pour générer des cas limites et des edge cases souvent oubliés.
- Ne pas déléguer la conception de la stratégie de test à l'IA -- elle reste une décision d'ingénierie.
- Utiliser l'IA pour écrire les test builders et les fixtures, tâches mécaniques à forte valeur d'automatisation.

---

## Summary Checklist

Vérifier la stratégie de test sur chaque projet :

- [ ] La répartition des tests suit la pyramide (ou le trophy) appropriée au contexte
- [ ] Le TDD est appliqué sur la logique métier complexe
- [ ] Les tests expriment des comportements, pas des détails d'implémentation
- [ ] Le property-based testing couvre les invariants critiques (calculs, sérialisation)
- [ ] Le contract testing valide les interactions entre services
- [ ] Les mocks sont limités aux boundaries (I/O), les fakes sont préférés
- [ ] La couverture est mesurée par zone (métier > orchestration > infrastructure)
- [ ] Le mutation testing évalue la pertinence des tests sur le code critique
- [ ] Chaque test suit le pattern AAA (Arrange-Act-Assert) et a un nom descriptif
- [ ] Les tests sont rapides (< 10s pour la suite unitaire, < 2min pour l'intégration)
