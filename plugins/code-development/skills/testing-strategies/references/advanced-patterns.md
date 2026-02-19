# Patterns de Test Avancés — MSW, Pact, Stryker et fast-check

## MSW Avancé : Mock Service Worker

MSW intercepte les requêtes réseau au niveau du service worker (navigateur) ou de Node.js. C'est l'approche recommandée pour mocker les API REST et GraphQL dans les tests, car elle fonctionne de manière transparente dans tous les environnements sans modifier le code de production.

### Configuration multi-environnement

```typescript
// src/mocks/handlers/usersHandlers.ts
import { http, HttpResponse, delay } from 'msw'
import type { User } from '@/types/user'

// Handlers typés avec les types de l'API
export const usersHandlers = [
  http.get<never, never, User>('/api/users/:id', async ({ params }) => {
    // Simuler une latence réseau réaliste
    await delay(150)

    if (params.id === 'not-found') {
      return HttpResponse.json(
        { error: 'Utilisateur introuvable' },
        { status: 404 }
      )
    }

    return HttpResponse.json({
      id: params.id as string,
      name: 'Alice Martin',
      email: 'alice@example.com',
      role: 'user',
    })
  }),

  http.post<never, { email: string; password: string }>('/api/auth/login', async ({ request }) => {
    const body = await request.json()

    if (body.email === 'invalid@example.com') {
      return HttpResponse.json(
        { error: 'Identifiants incorrects' },
        { status: 401 }
      )
    }

    return HttpResponse.json({
      token: 'mock-jwt-token',
      user: { id: '1', email: body.email, role: 'user' },
    })
  }),
]
```

```typescript
// src/mocks/server.ts — pour Node.js (Vitest)
import { setupServer } from 'msw/node'
import { usersHandlers } from './handlers/usersHandlers'
import { productsHandlers } from './handlers/productsHandlers'

export const server = setupServer(
  ...usersHandlers,
  ...productsHandlers,
)

// src/test/setup.ts
import { server } from '@/mocks/server'

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers()) // reset après chaque test
afterAll(() => server.close())
```

### Passthrough et réseau conditionnel

```typescript
// http.passthrough() — laisser passer certaines requêtes vers le vrai réseau
import { http, passthrough } from 'msw'

export const handlers = [
  // Intercepter les API de l'application
  http.get('/api/*', () => {
    return HttpResponse.json({ mocked: true })
  }),

  // Laisser passer les CDN et ressources statiques
  http.get('https://cdn.example.com/*', () => passthrough()),

  // Laisser passer selon une condition
  http.get('/api/feature-flags', ({ request }) => {
    if (request.headers.get('x-test-passthrough') === 'true') {
      return passthrough()
    }
    return HttpResponse.json({ 'new-checkout': false })
  }),
]
```

### Override de handlers dans un test spécifique

```typescript
import { http, HttpResponse } from 'msw'
import { server } from '@/mocks/server'
import { render, screen, waitFor } from '@testing-library/react'
import { UserProfile } from './UserProfile'

it('affiche un message d\'erreur en cas d\'échec réseau', async () => {
  // Override temporaire pour CE test uniquement
  server.use(
    http.get('/api/users/:id', () => {
      return HttpResponse.error() // erreur réseau
    })
  )

  render(<UserProfile userId="123" />)

  await waitFor(() => {
    expect(screen.getByRole('alert')).toHaveTextContent('Impossible de charger le profil')
  })
  // server.resetHandlers() dans afterEach restaure les handlers par défaut
})
```

### Intégration avec @tanstack/query

```typescript
// src/test/utils/renderWithMSW.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render } from '@testing-library/react'

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,      // pas de retry en tests
        gcTime: 0,         // pas de cache entre les tests
        staleTime: 0,
      },
      mutations: { retry: false },
    },
  })
}

export function renderWithQuery(ui: React.ReactElement) {
  const queryClient = createTestQueryClient()
  return {
    ...render(
      <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>
    ),
    queryClient,
  }
}
```

---

## Contract Testing avec Pact

Le contract testing résout le problème des intégrations entre services : comment s'assurer que le service A et le service B parlent le même langage, sans lancer les deux en même temps ?

### Consumer : définir le contrat attendu

```typescript
// tests/pact/orderService.consumer.pact.ts
import { PactV3, MatchersV3 } from '@pact-foundation/pact'
import { describe, it, beforeAll, afterAll } from 'vitest'

const { like, eachLike, regex } = MatchersV3

const provider = new PactV3({
  consumer: 'OrderService',
  provider: 'PaymentService',
  dir: './pacts',
  logLevel: 'warn',
})

describe('OrderService → PaymentService', () => {
  it('peut initier un paiement', async () => {
    await provider
      .given('un client avec des fonds suffisants')
      .uponReceiving('une demande de paiement valide')
      .withRequest({
        method: 'POST',
        path: '/payments',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': regex('Bearer .+', 'Bearer valid-token'),
        },
        body: {
          orderId: like('order-123'),
          amount: like(4900),
          currency: like('EUR'),
          customerId: like('cust-456'),
        },
      })
      .willRespondWith({
        status: 201,
        headers: { 'Content-Type': 'application/json' },
        body: {
          paymentId: like('pay-789'),
          status: like('pending'),
          createdAt: like('2024-01-15T10:00:00Z'),
        },
      })
      .executeTest(async (mockServer) => {
        // Tester le code réel du OrderService contre le mock Pact
        const paymentClient = new PaymentClient({ baseUrl: mockServer.url })
        const result = await paymentClient.initiatePayment({
          orderId: 'order-123',
          amount: 4900,
          currency: 'EUR',
          customerId: 'cust-456',
        })

        expect(result.paymentId).toBeDefined()
        expect(result.status).toBe('pending')
      })
  })

  it('gère le refus de paiement', async () => {
    await provider
      .given('un client avec des fonds insuffisants')
      .uponReceiving('une demande de paiement refusée')
      .withRequest({
        method: 'POST',
        path: '/payments',
        body: {
          orderId: like('order-999'),
          amount: like(99999),
          currency: like('EUR'),
          customerId: like('cust-broke'),
        },
      })
      .willRespondWith({
        status: 402,
        body: {
          error: like('Fonds insuffisants'),
          code: like('INSUFFICIENT_FUNDS'),
        },
      })
      .executeTest(async (mockServer) => {
        const paymentClient = new PaymentClient({ baseUrl: mockServer.url })

        await expect(
          paymentClient.initiatePayment({
            orderId: 'order-999',
            amount: 99999,
            currency: 'EUR',
            customerId: 'cust-broke',
          })
        ).rejects.toThrow('Fonds insuffisants')
      })
  })
})
```

### Provider : vérifier le contrat

```typescript
// tests/pact/paymentService.provider.pact.ts
import { PactV3, VerifierOptions } from '@pact-foundation/pact'
import app from '../../src/app'
import { describe, it } from 'vitest'

describe('PaymentService — vérification du contrat', () => {
  it('satisfait le contrat du OrderService', async () => {
    const verifier = new PactV3({
      provider: 'PaymentService',
      providerBaseUrl: 'http://localhost:3001',
    })

    await verifier.verifyProvider({
      pactBrokerUrl: process.env.PACT_BROKER_URL,
      pactBrokerToken: process.env.PACT_BROKER_TOKEN,
      publishVerificationResult: process.env.CI === 'true',
      providerVersion: process.env.GIT_COMMIT,

      // State handlers : préparer l'état de la DB pour chaque interaction
      stateHandlers: {
        'un client avec des fonds suffisants': async () => {
          await db.seed({ customers: [{ id: 'cust-456', balance: 10000 }] })
        },
        'un client avec des fonds insuffisants': async () => {
          await db.seed({ customers: [{ id: 'cust-broke', balance: 0 }] })
        },
      },
    })
  })
})
```

### Workflow CI avec can-i-deploy

```yaml
# .github/workflows/pact.yml
- name: Publier les pacts
  run: npx pact-broker publish ./pacts
    --broker-base-url ${{ secrets.PACT_BROKER_URL }}
    --broker-token ${{ secrets.PACT_BROKER_TOKEN }}
    --consumer-app-version ${{ github.sha }}
    --branch ${{ github.ref_name }}

- name: can-i-deploy ?
  run: npx pact-broker can-i-deploy
    --pacticipant OrderService
    --version ${{ github.sha }}
    --to-environment production
    --broker-base-url ${{ secrets.PACT_BROKER_URL }}
    --broker-token ${{ secrets.PACT_BROKER_TOKEN }}
```

---

## Mutation Testing avec Stryker

Stryker introduit des bugs délibérés dans le code (mutants) et vérifie que les tests les détectent. Un mutant "survivant" révèle un test insuffisant.

```json
// stryker.config.json
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "testRunner": "vitest",
  "reporters": ["html", "clear-text", "progress"],
  "coverageAnalysis": "perTest",
  "mutate": [
    "src/features/**/*.ts",
    "!src/features/**/*.test.ts",
    "!src/features/**/*.d.ts"
  ],
  "vitest": {
    "configFile": "vitest.config.ts"
  },
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  },
  "tempDirName": ".stryker-tmp",
  "cleanTempDir": true
}
```

### Comprendre le mutation score

Stryker applique des mutations classiques :

| Type de mutant | Exemple de mutation | Ce qu'il teste |
|---------------|-------------------|----------------|
| `BooleanLiteral` | `true` → `false` | Les conditions booléennes |
| `ConditionalExpression` | `a > b` → `a >= b` | Les comparaisons aux limites |
| `ArithmeticOperator` | `a + b` → `a - b` | Les calculs |
| `StringLiteral` | `"error"` → `""` | Les messages d'erreur |
| `BlockStatement` | Supprime le corps d'une fonction | Les effets de bord |

```typescript
// Exemple : ce code a un mutant survivant
function calculateDiscount(total: number, isVip: boolean): number {
  if (isVip) {
    return total * 0.2  // Mutant : 0.2 → 0.1 — le test ne vérifie pas la valeur exacte ?
  }
  return 0
}

// Test insuffisant (mutant survit)
it('applique une remise aux VIP', () => {
  const discount = calculateDiscount(100, true)
  expect(discount).toBeGreaterThan(0) // trop vague !
})

// Test complet (tue le mutant)
it('applique une remise de 20% aux VIP', () => {
  expect(calculateDiscount(100, true)).toBe(20)   // valeur exacte
  expect(calculateDiscount(100, false)).toBe(0)   // contre-exemple
  expect(calculateDiscount(200, true)).toBe(40)   // autre montant
})
```

---

## Property-Based Testing avec fast-check

Le property-based testing génère automatiquement des centaines de cas de test. Au lieu de tester des exemples précis, on teste des propriétés invariantes.

```typescript
import * as fc from 'fast-check'
import { describe, it, expect } from 'vitest'
import { calculateTax, formatPrice, sortItems } from './utils'

describe('Propriétés invariantes', () => {
  // Propriété : la TVA est toujours entre 0 et le montant HT
  it('la TVA est toujours positive et inférieure au montant', () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 1_000_000 }),  // montant en centimes
        fc.float({ min: 0, max: 0.3 }),            // taux entre 0% et 30%
        (amount, taxRate) => {
          const tax = calculateTax(amount, taxRate)
          expect(tax).toBeGreaterThanOrEqual(0)
          expect(tax).toBeLessThanOrEqual(amount)
        }
      )
    )
  })

  // Propriété : le tri est stable et idempotent
  it('trier deux fois donne le même résultat que trier une fois', () => {
    fc.assert(
      fc.property(
        fc.array(fc.record({ id: fc.string(), price: fc.integer({ min: 0 }) })),
        (items) => {
          const onceSorted = sortItems([...items])
          const twiceSorted = sortItems([...onceSorted])
          expect(twiceSorted).toEqual(onceSorted)
        }
      ),
      { numRuns: 1000 } // 1000 exemples générés
    )
  })

  // Shrinking automatique : fast-check trouve le plus petit exemple qui échoue
  it('formatPrice round-trip', () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 999_999 }),
        (cents) => {
          const formatted = formatPrice(cents)
          expect(formatted).toMatch(/\d+,\d{2}\s€/)
        }
      )
    )
  })
})
```

### Arbitraires personnalisés

```typescript
// Générer des données métier réalistes
const validEmail = fc.string({ minLength: 1, maxLength: 50 })
  .map(s => `${s.replace(/[^a-z]/gi, 'a')}@example.com`)

const validUser = fc.record({
  id: fc.uuid(),
  email: validEmail,
  age: fc.integer({ min: 18, max: 120 }),
  balance: fc.integer({ min: 0, max: 1_000_000 }),
})

const validOrder = fc.record({
  items: fc.array(
    fc.record({
      productId: fc.uuid(),
      quantity: fc.integer({ min: 1, max: 100 }),
      unitPrice: fc.integer({ min: 1, max: 100_000 }),
    }),
    { minLength: 1, maxLength: 20 }
  ),
})

// Tester des invariants sur des données métier complexes
it('le total d\'une commande est la somme de ses lignes', () => {
  fc.assert(
    fc.property(validOrder, (order) => {
      const expectedTotal = order.items.reduce(
        (sum, item) => sum + item.quantity * item.unitPrice,
        0
      )
      expect(calculateOrderTotal(order)).toBe(expectedTotal)
    })
  )
})
```

### `fc.modelRun` pour les state machines

```typescript
// Tester une state machine de panier d'achat
import * as fc from 'fast-check'

interface CartModel {
  items: Map<string, number> // productId → quantity
}

interface RealCart {
  addItem(productId: string, qty: number): void
  removeItem(productId: string): void
  getTotal(): number
  getItemCount(): number
}

class AddItemCommand {
  constructor(public productId: string, public qty: number) {}

  check(model: CartModel) { return true } // toujours applicable

  run(model: CartModel, real: RealCart) {
    model.items.set(this.productId, (model.items.get(this.productId) ?? 0) + this.qty)
    real.addItem(this.productId, this.qty)

    // Invariant après chaque commande
    expect(real.getItemCount()).toBe(
      Array.from(model.items.values()).reduce((a, b) => a + b, 0)
    )
  }
}

it('le panier respecte ses invariants pour toute séquence d\'actions', () => {
  fc.assert(
    fc.property(
      fc.commands([
        fc.record({ productId: fc.uuid(), qty: fc.integer({ min: 1, max: 5 }) })
          .map(({ productId, qty }) => new AddItemCommand(productId, qty)),
        // ... autres commandes (RemoveItem, UpdateQty, etc.)
      ]),
      (commands) => {
        const model: CartModel = { items: new Map() }
        const real = new ShoppingCart()
        fc.modelRun(() => ({ model, real }), commands)
      }
    )
  )
})
```

---

## Testing Trophy vs Testing Pyramid

La Testing Pyramid traditionnelle (beaucoup d'unitaires, peu d'E2E) a évolué vers le Testing Trophy de Kent C. Dodds.

```
        /\
       /E2E\          ← peu mais critiques
      /------\
     /Intégra-\       ← la majorité des tests
    /  tion    \
   /------------\
  /  Unitaires   \    ← pour la logique pure
 /----------------\
/   Static (lint)  \  ← gratuit, valeur élevée
```

**Règle pratique :**

| Type | Quand écrire | Proportion cible |
|------|-------------|-----------------|
| Statique (TypeScript, ESLint) | Toujours | — |
| Unitaire | Logique métier pure, algorithmes | 20-30% |
| Intégration | Composants avec dépendances, API routes | 50-60% |
| E2E | Parcours utilisateurs critiques | 10-20% |

**Quand préférer les tests d'intégration aux unitaires :**
- Quand la logique dépend de plusieurs modules qui interagissent
- Quand le mock serait plus complexe que l'implémentation réelle
- Quand on teste des comportements, pas des implémentations

---

## Validation des Contrats d'API avec openapi-backend

```typescript
// tests/api/contractValidation.test.ts
import OpenAPIBackend from 'openapi-backend'
import { describe, it, expect, beforeAll } from 'vitest'
import supertest from 'supertest'
import app from '../../src/app'

let api: OpenAPIBackend

beforeAll(async () => {
  api = new OpenAPIBackend({
    definition: './openapi.yaml',
    validate: true,
    strict: true,
  })
  await api.init()
})

it('GET /users/:id respecte le schéma OpenAPI', async () => {
  const response = await supertest(app).get('/api/users/123')

  const valid = await api.validateResponse(response.body, 'getUser', response.status)

  expect(valid.errors).toBeNull()
  expect(response.status).toBe(200)
})

it('POST /users valide le body de la requête', async () => {
  const invalidBody = { email: 'pas-un-email', name: '' }
  const response = await supertest(app)
    .post('/api/users')
    .send(invalidBody)
    .expect(400)

  // La réponse d'erreur respecte aussi le schéma OpenAPI
  const valid = await api.validateResponse(response.body, 'createUser', 400)
  expect(valid.errors).toBeNull()
})
```

---

## Exécution Parallèle et Isolation des Workers

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    // pool: 'threads' (défaut) — partagent le même process Node.js
    // pool: 'forks' — processus séparés, meilleure isolation, plus lent
    pool: 'forks',

    poolOptions: {
      forks: {
        singleFork: false, // un process par fichier de test
        maxForks: 4,       // max 4 processus parallèles
      },
    },

    // Isolation totale : chaque fichier de test dans son module scope
    isolate: true,

    // Reporter verbeux pour le debug
    reporter: process.env.CI ? ['junit', 'github-actions'] : ['verbose'],
  },
})
```

---

## Qualité du Code de Test : Linting

```json
// .eslintrc.json — règles pour les fichiers de test
{
  "overrides": [
    {
      "files": ["**/*.test.ts", "**/*.test.tsx"],
      "plugins": ["testing-library", "vitest"],
      "extends": [
        "plugin:testing-library/react",
        "plugin:vitest/recommended"
      ],
      "rules": {
        "testing-library/no-debugging-utils": "error",
        "testing-library/no-wait-for-multiple-assertions": "error",
        "testing-library/prefer-screen-queries": "error",
        "testing-library/no-node-access": "error",

        "vitest/no-disabled-tests": "warn",
        "vitest/no-focused-tests": "error",
        "vitest/expect-expect": "error",
        "vitest/no-identical-title": "error",
        "vitest/valid-expect": "error",

        // Éviter beforeAll pour les side effects
        "no-restricted-syntax": [
          "warn",
          {
            "selector": "CallExpression[callee.name='beforeAll']",
            "message": "Préférer beforeEach pour éviter le partage d'état entre tests"
          }
        ]
      }
    }
  ]
}
```

---

## Mesurer la Qualité des Tests

| Métrique | Ce qu'elle mesure | Limite |
|----------|------------------|--------|
| Statement coverage | % de lignes exécutées | Ne détecte pas les tests sans assertions |
| Branch coverage | % de branches (if/else) | Ne garantit pas la pertinence des assertions |
| Mutation score | % de mutants tués | Mesure la qualité réelle des assertions |
| Test execution time | Vitesse de la suite | Indicateur de maintenabilité |

**Cible recommandée :**

```
Statement coverage : ≥ 80% (ne pas courir après 100%)
Branch coverage    : ≥ 70%
Mutation score     : ≥ 75% sur la logique métier critique
Test suite CI      : < 5 minutes pour la boucle de feedback
```

La couverture à 100% avec des tests sans assertions est pire que 70% de couverture avec un mutation score de 90%. **La couverture mesure ce qui est exécuté, le mutation score mesure ce qui est vérifié.**

---

## Checklist Tests de Qualité Professionnelle

```
Tests unitaires :
  ☐ Chaque test a un seul comportement à vérifier
  ☐ Le nom du test décrit le comportement (pas la méthode)
  ☐ AAA pattern : Arrange → Act → Assert
  ☐ Pas de logique conditionnelle dans les tests
  ☐ Reset du state dans beforeEach, pas dans afterEach

Tests d'intégration :
  ☐ MSW configuré pour tous les appels réseau
  ☐ Pas d'appels réseau réels en CI
  ☐ Transactions ou cleanup après chaque test DB

Contract testing :
  ☐ Pacts publiés dans le broker après chaque merge
  ☐ can-i-deploy bloque le déploiement si contrat cassé

Mutation testing :
  ☐ Stryker lancé en CI sur la logique métier critique
  ☐ Mutation score ≥ 75% sur les modules clés
```
