# Études de Cas — Testing Strategies en Production

## Vue d'ensemble

Ces quatre études de cas documentent des migrations et implémentations réelles de stratégies de test. Chacune illustre un contexte spécifique, les problèmes concrets rencontrés, les solutions appliquées, et les métriques mesurées.

| Cas | Contexte | Défi principal | Résultat clé |
|-----|----------|---------------|-------------|
| 1 | Migration Jest → Vitest | Performance CI | 8 min → 2,5 min |
| 2 | 0% → 80% couverture | Dette technique | 0 régression en 6 mois |
| 3 | Contract testing micro-services | Integration hell | E2E 45 min → 8 min |
| 4 | TDD algorithme de scoring | Logique complexe | 98% mutation score |

---

## Cas 1 — Migration Jest → Vitest (Startup SaaS, 800 Tests)

### Contexte

Une startup SaaS développait une application Next.js avec environ 800 tests répartis en unitaires et d'intégration. La stack utilisait Jest avec Babel pour la transpilation ES modules, avec un fichier de configuration qui avait accumulé 80 lignes de config au fil des 18 mois de développement.

**Stack initiale :**
- Next.js 13, TypeScript, Prisma
- Jest 29 avec `babel-jest` et `@babel/preset-typescript`
- `ts-jest` pour certains fichiers
- `msw` v1 pour les mocks réseau
- CI : GitHub Actions, 3 jobs parallèles

### Problème

L'équipe de 4 développeurs subissait une friction quotidienne majeure :

- **CI prenant 8 minutes** pour 800 tests — trop long pour un feedback rapide
- **Watch mode lent** : 3-5 secondes pour relancer les tests après une modification
- **Configuration fragile** : `moduleNameMapper` avec 12 entrées pour gérer les alias de chemins
- **Mocks hoisting imprévisibles** : `jest.mock()` devait être en haut du fichier, mais les imports ES6 causaient des erreurs selon l'ordre

Extrait du fichier de config problématique :

```javascript
// jest.config.js — avant (80 lignes)
const nextJest = require('next/jest')

const createJestConfig = nextJest({
  dir: './',
})

const customJestConfig = {
  setupFilesAfterFramework: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/components/(.*)$': '<rootDir>/src/components/$1',
    '^@/lib/(.*)$': '<rootDir>/src/lib/$1',
    '^@/hooks/(.*)$': '<rootDir>/src/hooks/$1',
    '^@/types/(.*)$': '<rootDir>/src/types/$1',
    '^@/utils/(.*)$': '<rootDir>/src/utils/$1',
    '^@/services/(.*)$': '<rootDir>/src/services/$1',
    '^@/store/(.*)$': '<rootDir>/src/store/$1',
    '^@/features/(.*)$': '<rootDir>/src/features/$1',
    '^@/api/(.*)$': '<rootDir>/src/api/$1',
    '^@/constants/(.*)$': '<rootDir>/src/constants/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(gif|ttf|eot|svg|png)$': '<rootDir>/__mocks__/fileMock.js',
  },
  testEnvironment: 'jest-environment-jsdom',
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': ['babel-jest', { presets: ['next/babel'] }],
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.tsx',
    '!src/pages/_app.tsx',
    '!src/pages/_document.tsx',
  ],
  coverageThreshold: {
    global: {
      branches: 60,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
  testPathIgnorePatterns: ['<rootDir>/.next/', '<rootDir>/node_modules/'],
  moduleDirectories: ['node_modules', '<rootDir>/'],
  testMatch: ['**/__tests__/**/*.[jt]s?(x)', '**/?(*.)+(spec|test).[jt]s?(x)'],
  // ... 30 autres lignes de config
}

module.exports = createJestConfig(customJestConfig)
```

### Solution : Migration en 2 Jours

**Jour 1 : installation et config de base**

```bash
npm remove jest jest-environment-jsdom babel-jest @babel/preset-typescript ts-jest
npm install -D vitest @vitejs/plugin-react jsdom @testing-library/jest-dom
```

```typescript
// vitest.config.ts — après (20 lignes)
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    include: ['src/**/*.test.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{ts,tsx}'],
      exclude: ['src/**/*.d.ts', 'src/**/*.stories.tsx'],
    },
  },
})
```

**Différences notables — pièges migratoires :**

**Piège 1 : Hoisting de `vi.mock` différent de `jest.mock`**

```typescript
// Jest — fonctionnait grâce au hoisting Babel
import { sendEmail } from './emailService'
jest.mock('./emailService')

// Vitest — vi.mock est aussi hoisted, mais avec une différence subtile :
// les imports nommés doivent utiliser la factory function
import { sendEmail } from './emailService'
vi.mock('./emailService', () => ({
  sendEmail: vi.fn().mockResolvedValue({ success: true }),
}))

// PIÈGE : en Jest, on pouvait faire jest.fn() sans factory
// En Vitest, sans factory, le module est auto-mocké différemment
```

**Piège 2 : Format des snapshots**

```bash
# Les snapshots Jest et Vitest ont un format légèrement différent
# Solution : supprimer les .snap existants et les régénérer
find src -name '*.snap' -delete
npx vitest run --update-snapshots
```

**Piège 3 : Fake timers API légèrement différente**

```typescript
// Jest
jest.useFakeTimers()
jest.setSystemTime(new Date('2024-01-15'))
jest.useRealTimers()

// Vitest — API identique mais dans beforeEach/afterEach
beforeEach(() => vi.useFakeTimers())
afterEach(() => vi.useRealTimers())

// DIFFÉRENCE : Vitest require vi.setSystemTime() après vi.useFakeTimers()
// Jest permettait de passer la date directement à useFakeTimers()
vi.useFakeTimers()
vi.setSystemTime(new Date('2024-01-15'))
```

**Jour 2 : in-source testing pour les utils**

```typescript
// src/utils/pricing.ts
export function applyDiscount(price: number, discountPercent: number): number {
  if (discountPercent < 0 || discountPercent > 100) {
    throw new Error(`Remise invalide : ${discountPercent}%`)
  }
  return Math.round(price * (1 - discountPercent / 100))
}

if (import.meta.vitest) {
  const { it, expect, describe } = import.meta.vitest

  describe('applyDiscount', () => {
    it('applique une remise de 20%', () => {
      expect(applyDiscount(1000, 20)).toBe(800)
    })
    it('lève une erreur pour une remise négative', () => {
      expect(() => applyDiscount(1000, -5)).toThrow('Remise invalide')
    })
  })
}
```

### Métriques

| Indicateur | Avant (Jest) | Après (Vitest) |
|-----------|-------------|---------------|
| Durée CI (800 tests) | 8 min | 2,5 min |
| Watch mode (relance) | 3-5 s | < 0,5 s |
| Lignes de config | 80 | 20 |
| Fichiers de config | 3 (`jest.config.js`, `.babelrc`, `jest.setup.js`) | 1 (`vitest.config.ts`) |
| Durée de migration | — | 2 jours |

### Leçon Clé

Vitest est un drop-in replacement pour les projets Vite/ESM. Les seules différences structurelles concernent le hoisting des mocks (toujours utiliser la factory function) et le format des snapshots. La migration vaut toujours l'investissement pour les projets > 6 mois, car le gain de DX est immédiat et permanent.

---

## Cas 2 — 0% → 80% de Couverture (Agence Web, 3 Développeurs)

### Contexte

Une agence web avait migré une application de facturation de Laravel vers Node.js/TypeScript 8 mois auparavant. Trois développeurs maintenaient le projet. Zéro test écrit — la migration avait été faite dans l'urgence.

**Stack :**
- Node.js, TypeScript, Express, Prisma
- Stripe pour les paiements
- SendGrid pour les emails
- PostgreSQL

### Problème

La situation était préoccupante :
- **Bugs en production** sur la logique de facturation (calcul TVA, remises cumulées)
- **Onboarding coûteux** : un nouveau développeur mettait 2 semaines à comprendre les règles de facturation
- **Refactoring impossible** : personne n'osait toucher le code de facturation

Le code existant n'était pas structuré pour être facilement testable — dépendances directes vers Stripe et la DB dans la même fonction :

```typescript
// src/billing/invoiceService.ts — code legacy difficile à tester
export async function createInvoice(customerId: string, items: OrderItem[]) {
  // Dépendance directe vers la DB
  const customer = await prisma.customer.findUnique({ where: { id: customerId } })
  if (!customer) throw new Error('Client introuvable')

  // Logique métier mélangée avec les effets de bord
  const subtotal = items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0)
  const discountRate = customer.tier === 'premium' ? 0.15 : customer.tier === 'partner' ? 0.25 : 0
  const discount = Math.round(subtotal * discountRate)
  const taxableAmount = subtotal - discount
  const taxRate = customer.country === 'FR' ? 0.20 : customer.country === 'BE' ? 0.21 : 0
  const tax = Math.round(taxableAmount * taxRate)
  const total = taxableAmount + tax

  // Appel Stripe direct
  const paymentIntent = await stripe.paymentIntents.create({
    amount: total,
    currency: 'eur',
    customer: customer.stripeId,
  })

  // Persistance et email dans la même fonction
  const invoice = await prisma.invoice.create({
    data: { customerId, items, subtotal, discount, tax, total, stripePaymentIntentId: paymentIntent.id }
  })

  await sendgrid.send({
    to: customer.email,
    subject: `Facture #${invoice.id}`,
    html: generateInvoiceHtml(invoice),
  })

  return invoice
}
```

### Solution : Approche "Characterization Tests"

**Étape 1 : Characterization tests — capturer le comportement actuel**

Avant de refactorer, écrire des tests qui décrivent ce que le code fait actuellement (pas ce qu'il devrait faire idéalement). Ces tests servent de filet de sécurité.

```typescript
// src/billing/__tests__/invoiceCalculation.characterization.test.ts
// Objectif : capturer le comportement actuel, même s'il est imparfait

describe('Calcul de facture — comportement actuel', () => {
  it('calcule la TVA à 20% pour les clients français', () => {
    // On découvre le comportement en lisant le code
    const result = calculateInvoiceAmounts({
      subtotal: 1000,
      customerCountry: 'FR',
      customerTier: 'standard',
    })

    // Ce test documente le comportement réel
    expect(result.tax).toBe(200)
    expect(result.total).toBe(1200)
  })

  it('applique la remise partner AVANT la TVA (comportement actuel)', () => {
    // On découvre que la remise s'applique avant la base taxable — est-ce correct ?
    // Pour l'instant : on documente, on ne change pas
    const result = calculateInvoiceAmounts({
      subtotal: 1000,
      customerCountry: 'FR',
      customerTier: 'partner', // 25% de remise
    })

    // subtotal 1000 → remise 250 → taxable 750 → TVA 150 → total 900
    expect(result.discount).toBe(250)
    expect(result.tax).toBe(150)
    expect(result.total).toBe(900)
  })
})
```

**Étape 2 : Extraire la logique pure avec l'InMemoryRepository**

```typescript
// src/billing/invoiceCalculator.ts — logique pure extraite
export interface InvoiceCalculationInput {
  items: Array<{ quantity: number; unitPrice: number }>
  customerTier: 'standard' | 'premium' | 'partner'
  customerCountry: string
}

export interface InvoiceCalculationResult {
  subtotal: number
  discountRate: number
  discount: number
  taxableAmount: number
  taxRate: number
  tax: number
  total: number
}

export function calculateInvoiceAmounts(input: InvoiceCalculationInput): InvoiceCalculationResult {
  const subtotal = input.items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0)

  const discountRates: Record<string, number> = {
    standard: 0,
    premium: 0.15,
    partner: 0.25,
  }
  const discountRate = discountRates[input.customerTier] ?? 0
  const discount = Math.round(subtotal * discountRate)
  const taxableAmount = subtotal - discount

  const taxRates: Record<string, number> = {
    FR: 0.20,
    BE: 0.21,
    DE: 0.19,
  }
  const taxRate = taxRates[input.customerCountry] ?? 0
  const tax = Math.round(taxableAmount * taxRate)
  const total = taxableAmount + tax

  return { subtotal, discountRate, discount, taxableAmount, taxRate, tax, total }
}
```

```typescript
// src/billing/invoiceService.ts — refactoré avec injection de dépendances
export interface InvoiceRepository {
  create(data: CreateInvoiceData): Promise<Invoice>
  findById(id: string): Promise<Invoice | null>
}

export interface PaymentGateway {
  createPaymentIntent(amount: number, currency: string, customerId: string): Promise<{ id: string }>
}

export interface NotificationService {
  sendInvoiceEmail(invoice: Invoice, customer: Customer): Promise<void>
}

export class InvoiceService {
  constructor(
    private readonly invoiceRepo: InvoiceRepository,
    private readonly paymentGateway: PaymentGateway,
    private readonly notificationService: NotificationService,
  ) {}

  async createInvoice(customer: Customer, items: OrderItem[]): Promise<Invoice> {
    const amounts = calculateInvoiceAmounts({
      items,
      customerTier: customer.tier,
      customerCountry: customer.country,
    })

    const payment = await this.paymentGateway.createPaymentIntent(
      amounts.total, 'eur', customer.externalPaymentId
    )

    const invoice = await this.invoiceRepo.create({
      customerId: customer.id,
      items,
      ...amounts,
      paymentIntentId: payment.id,
    })

    await this.notificationService.sendInvoiceEmail(invoice, customer)
    return invoice
  }
}
```

**Étape 3 : InMemoryRepository pour les tests de service**

```typescript
// src/test/repositories/inMemoryInvoiceRepository.ts
export class InMemoryInvoiceRepository implements InvoiceRepository {
  private invoices = new Map<string, Invoice>()
  private nextId = 1

  async create(data: CreateInvoiceData): Promise<Invoice> {
    const invoice: Invoice = {
      id: `inv-${this.nextId++}`,
      createdAt: new Date(),
      ...data,
    }
    this.invoices.set(invoice.id, invoice)
    return invoice
  }

  async findById(id: string): Promise<Invoice | null> {
    return this.invoices.get(id) ?? null
  }

  clear() { this.invoices.clear() }
  getAll(): Invoice[] { return Array.from(this.invoices.values()) }
}

// Tests du service avec InMemory
describe('InvoiceService', () => {
  let invoiceRepo: InMemoryInvoiceRepository
  let paymentGateway: { createPaymentIntent: ReturnType<typeof vi.fn> }
  let notificationService: { sendInvoiceEmail: ReturnType<typeof vi.fn> }
  let service: InvoiceService

  beforeEach(() => {
    invoiceRepo = new InMemoryInvoiceRepository()
    paymentGateway = { createPaymentIntent: vi.fn().mockResolvedValue({ id: 'pi_mock_123' }) }
    notificationService = { sendInvoiceEmail: vi.fn().mockResolvedValue(undefined) }
    service = new InvoiceService(invoiceRepo, paymentGateway, notificationService)
  })

  it('crée une facture avec les montants corrects', async () => {
    const customer: Customer = { id: 'c1', tier: 'premium', country: 'FR', externalPaymentId: 'cus_123' }
    const items = [{ quantity: 2, unitPrice: 5000 }] // 2 × 50€ = 100€ HT

    const invoice = await service.createInvoice(customer, items)

    expect(invoice.subtotal).toBe(10000)    // 100€
    expect(invoice.discount).toBe(1500)     // 15% de remise premium
    expect(invoice.taxableAmount).toBe(8500) // 85€ base taxable
    expect(invoice.tax).toBe(1700)          // 20% TVA = 17€
    expect(invoice.total).toBe(10200)       // 102€
    expect(paymentGateway.createPaymentIntent).toHaveBeenCalledWith(10200, 'eur', 'cus_123')
    expect(notificationService.sendInvoiceEmail).toHaveBeenCalledOnce()
  })
})
```

### Résultats Mesurés

| Indicateur | Avant | Après (3 semaines) |
|-----------|-------|-------------------|
| Couverture de code | 0% | 80% |
| Bugs facturation en prod | 2-3/mois | 0 en 6 mois |
| Temps onboarding (facturation) | 2 semaines | 3 jours |
| Refactoring majeur réussi | Impossible | Réalisé en 1 semaine |

### Leçon Clé

Les characterization tests permettent de tester du code legacy sans le refactorer d'abord. L'ordre est : tester → comprendre → refactorer → tester mieux. Ne jamais refactorer du code sans tests. Les InMemoryRepositories sont l'investissement le plus rentable : écrits une fois, utilisés dans des dizaines de tests.

---

## Cas 3 — Contract Testing entre Micro-services (Scale-up, 6 Services)

### Contexte

Une scale-up avec 6 micro-services Node.js qui communiquaient par API REST. Chaque service avait sa propre équipe de 2-3 développeurs. La suite de tests E2E complète prenait 45 minutes.

**Services :**
- `order-service` : gestion des commandes
- `payment-service` : traitement des paiements (appelé par order-service)
- `inventory-service` : stocks (appelé par order-service)
- `notification-service` : emails et SMS
- `user-service` : authentification et profils
- `analytics-service` : événements et métriques

### Problème : Integration Hell

Le problème central était le couplage silencieux entre services :

```
Symptôme : L'équipe payment-service modifie le champ "status" de la réponse
           de "pending" à "processing" (changement logique de leur côté)
           → order-service casse silencieusement
           → Découvert en staging après 2 jours
           → Rollback d'urgence et perte de 4h de travail
```

Les tests E2E nécessitaient de lancer les 6 services simultanément, ce qui rendait la suite fragile et lente.

### Solution : Pact Consumer-Driven Contracts

**Service Commandes (consumer) — définir le contrat**

```typescript
// order-service/tests/pact/paymentService.consumer.pact.ts
import { PactV3, MatchersV3 } from '@pact-foundation/pact'

const { like, regex } = MatchersV3

const provider = new PactV3({
  consumer: 'OrderService',
  provider: 'PaymentService',
  dir: path.join(__dirname, '../../../pacts'),
})

describe('OrderService → PaymentService : contrat', () => {
  it('initie un paiement pour une commande', async () => {
    await provider
      .given('PaymentService est disponible')
      .uponReceiving('POST /payments — initiation de paiement')
      .withRequest({
        method: 'POST',
        path: '/payments',
        headers: {
          'Content-Type': 'application/json',
          'X-Service-Token': like('valid-service-token'),
        },
        body: {
          orderId: like('order-abc-123'),
          amount: like(4900),
          currency: regex('EUR|USD|GBP', 'EUR'),
          customerId: like('cust-xyz-456'),
        },
      })
      .willRespondWith({
        status: 201,
        body: {
          paymentId: like('pay-def-789'),
          status: like('pending'),  // ← Le contrat fixe "pending" — tout changement casse
          estimatedCompletionAt: like('2024-01-15T10:05:00Z'),
        },
      })
      .executeTest(async (mockServer) => {
        // Tester le vrai code du OrderService
        const orderService = new OrderService({
          paymentServiceUrl: mockServer.url,
          serviceToken: 'valid-service-token',
        })

        const result = await orderService.initiatePaymentForOrder('order-abc-123', {
          amount: 4900,
          currency: 'EUR',
          customerId: 'cust-xyz-456',
        })

        expect(result.paymentId).toBeDefined()
        expect(result.status).toBe('pending')
      })
  })
})
```

**Service Paiements (provider) — vérifier le contrat**

```typescript
// payment-service/tests/pact/provider.pact.ts
import { PactV3 } from '@pact-foundation/pact'
import { startServer, stopServer } from '../../src/server'

describe('PaymentService — vérification des contrats', () => {
  let server: ReturnType<typeof startServer>

  beforeAll(async () => {
    server = await startServer({ port: 3001 })
  })

  afterAll(async () => {
    await stopServer(server)
  })

  it('satisfait tous les contrats des consumers', async () => {
    const verifier = new PactV3({
      provider: 'PaymentService',
      providerBaseUrl: 'http://localhost:3001',
    })

    await verifier.verifyProvider({
      pactBrokerUrl: process.env.PACT_BROKER_URL!,
      pactBrokerToken: process.env.PACT_BROKER_TOKEN!,
      publishVerificationResult: process.env.CI === 'true',
      providerVersion: process.env.GITHUB_SHA,
      providerVersionBranch: process.env.GITHUB_REF_NAME,

      stateHandlers: {
        'PaymentService est disponible': async () => {
          // Aucune préparation nécessaire — le service est toujours dispo
        },
        'paiement en attente pour la commande order-abc-123': async () => {
          await testDb.seed({
            payments: [{ id: 'pay-def-789', orderId: 'order-abc-123', status: 'pending' }],
          })
        },
      },
    })
  })
})
```

**Workflow CI complet**

```yaml
# .github/workflows/ci.yml — order-service
name: CI — Order Service

on: [push]

jobs:
  test-and-publish-pact:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Tests unitaires et d'intégration
        run: npm test

      - name: Générer les pacts (consumer tests)
        run: npm run test:pact:consumer

      - name: Publier les pacts dans le broker
        run: |
          npx pact-broker publish ./pacts \
            --broker-base-url ${{ secrets.PACT_BROKER_URL }} \
            --broker-token ${{ secrets.PACT_BROKER_TOKEN }} \
            --consumer-app-version ${{ github.sha }} \
            --branch ${{ github.ref_name }}

      - name: can-i-deploy en production ?
        run: |
          npx pact-broker can-i-deploy \
            --pacticipant OrderService \
            --version ${{ github.sha }} \
            --to-environment production \
            --broker-base-url ${{ secrets.PACT_BROKER_URL }} \
            --broker-token ${{ secrets.PACT_BROKER_TOKEN }}

  deploy:
    needs: test-and-publish-pact
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Déployer en production
        run: ./scripts/deploy.sh production
      - name: Enregistrer le déploiement dans Pact Broker
        run: |
          npx pact-broker record-deployment \
            --pacticipant OrderService \
            --version ${{ github.sha }} \
            --environment production
```

### Résultats Mesurés

| Indicateur | Avant (E2E seuls) | Après (Pact + E2E critiques) |
|-----------|-------------------|-----------------------------|
| Durée CI | 45 min | 8 min |
| Régressions inter-services | 3-4/mois | 0 en 4 mois |
| Déploiements indépendants | Impossible | Quotidiens par équipe |
| Confiance au déploiement | Faible | Élevée (can-i-deploy) |

### Leçon Clé

Le contract testing libère les équipes pour déployer indépendamment sans peur. L'investissement initial (configurer Pact Broker, écrire les premiers contrats) est amorti dès le premier bug inter-services évité. La règle : **un contrat cassé = la CI bloque immédiatement**, pas dans 2 jours en staging.

---

## Cas 4 — TDD sur une Feature Complexe (Fintech, Algorithme de Scoring)

### Contexte

Une fintech développait un nouvel algorithme de scoring de risque crédit pour l'octroi de prêts. L'algorithme évaluait 12 critères (revenus, historique de paiement, endettement, stabilité professionnelle, etc.) avec des pondérations variables par segment de clientèle. La régulation exigeait une traçabilité complète des décisions.

**Contraintes :**
- Score final entre 0 et 1000
- 4 segments : `student`, `employed`, `self_employed`, `retired`
- Chaque segment a ses propres pondérations
- Audit trail obligatoire pour chaque décision

### Problème

L'algorithme était impossible à tester manuellement car :
- 12 critères × 4 segments = 48 combinaisons de pondérations
- Règles métier changeantes (le service juridique modifiait les seuils tous les trimestres)
- Les edge cases (revenus = 0, âge = 18, historique = null) causaient des NaN non détectés

### Solution : TDD Strict + Property-Based Testing

**Cycle TDD — exemple complet sur une règle**

```typescript
// ROUGE : le test échoue d'abord (la fonction n'existe pas encore)
describe('calculateIncomeScore', () => {
  it('retourne 0 pour un revenu nul', () => {
    expect(calculateIncomeScore(0, 'employed')).toBe(0)
  })
})
// → ReferenceError: calculateIncomeScore is not defined ✓ (rouge attendu)

// VERT minimal : faire passer le test avec le minimum de code
function calculateIncomeScore(monthlyIncome: number, segment: Segment): number {
  if (monthlyIncome === 0) return 0
  return 0 // valeur par défaut temporaire
}

// Ajouter le test suivant (encore rouge)
it('retourne 500 pour le revenu médian d\'un salarié (2 500€)', () => {
  expect(calculateIncomeScore(2500, 'employed')).toBe(500)
})

// REFACTOR : implémentation réelle après plusieurs cycles TDD
export function calculateIncomeScore(monthlyIncome: number, segment: Segment): number {
  if (monthlyIncome < 0) throw new Error(`Revenu invalide : ${monthlyIncome}`)
  if (monthlyIncome === 0) return 0

  const benchmarks: Record<Segment, { median: number; max: number }> = {
    student: { median: 600, max: 2000 },
    employed: { median: 2500, max: 8000 },
    self_employed: { median: 3000, max: 10000 },
    retired: { median: 1800, max: 4000 },
  }

  const { median, max } = benchmarks[segment]

  if (monthlyIncome <= median) {
    // Score linéaire de 0 à 500 entre 0 et la médiane
    return Math.round((monthlyIncome / median) * 500)
  } else {
    // Score logarithmique de 500 à 1000 au-dessus de la médiane
    const excess = Math.min(monthlyIncome - median, max - median)
    const excessRatio = excess / (max - median)
    return Math.round(500 + excessRatio * 500)
  }
}
```

**Property-Based Testing pour les invariants mathématiques**

```typescript
// src/scoring/__tests__/scoringInvariants.property.test.ts
import * as fc from 'fast-check'
import { calculateCreditScore, calculateIncomeScore, Segment } from '../creditScorer'

const segments: Segment[] = ['student', 'employed', 'self_employed', 'retired']
const segmentArb = fc.constantFrom(...segments)

describe('Invariants mathématiques du scoring', () => {
  // Invariant 1 : le score final est TOUJOURS entre 0 et 1000
  it('le score final est toujours dans [0, 1000]', () => {
    fc.assert(
      fc.property(
        fc.record({
          monthlyIncome: fc.integer({ min: 0, max: 50_000 }),
          paymentHistory: fc.float({ min: 0, max: 1 }),
          debtRatio: fc.float({ min: 0, max: 2 }),     // jusqu'à 200% de DTI
          yearsEmployed: fc.integer({ min: 0, max: 40 }),
          age: fc.integer({ min: 18, max: 85 }),
          creditScore: fc.integer({ min: 300, max: 850 }), // score Banque de France
        }),
        segmentArb,
        (applicant, segment) => {
          const score = calculateCreditScore(applicant, segment)
          expect(score).toBeGreaterThanOrEqual(0)
          expect(score).toBeLessThanOrEqual(1000)
          expect(Number.isInteger(score)).toBe(true) // pas de décimales
          expect(Number.isNaN(score)).toBe(false)    // jamais NaN
        }
      ),
      { numRuns: 10_000 } // 10 000 exemples aléatoires
    )
  })

  // Invariant 2 : le score est monotone par rapport au revenu (toutes choses égales)
  it('un revenu plus élevé ne peut pas produire un score plus faible', () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 9_000 }),
        fc.integer({ min: 1, max: 1_000 }),
        segmentArb,
        (baseIncome, delta, segment) => {
          const scoreBase = calculateIncomeScore(baseIncome, segment)
          const scoreHigher = calculateIncomeScore(baseIncome + delta, segment)
          expect(scoreHigher).toBeGreaterThanOrEqual(scoreBase)
        }
      )
    )
  })

  // Invariant 3 : les edge cases ne produisent pas d'erreurs
  it('gère les valeurs extrêmes sans lever d\'erreur', () => {
    const extremeCases = [
      { monthlyIncome: 0, age: 18, segment: 'student' as Segment },
      { monthlyIncome: 100_000, age: 85, segment: 'retired' as Segment },
      { monthlyIncome: 1, age: 18, segment: 'employed' as Segment },
    ]

    for (const { monthlyIncome, age, segment } of extremeCases) {
      expect(() =>
        calculateCreditScore({ monthlyIncome, age, paymentHistory: 0, debtRatio: 2, yearsEmployed: 0, creditScore: 300 }, segment)
      ).not.toThrow()
    }
  })
})
```

**Snapshot Tests pour les matrices de décision**

```typescript
// src/scoring/__tests__/decisionMatrix.snapshot.test.ts
import { generateDecisionMatrix } from '../decisionMatrix'

it('la matrice de décision pour le segment "employed" correspond au référentiel', () => {
  const matrix = generateDecisionMatrix('employed', {
    incomeBreakpoints: [1000, 2500, 5000, 8000],
    debtRatioBreakpoints: [0.2, 0.4, 0.6],
  })

  // La snapshot documente les décisions de crédit — tout changement est visible
  expect(matrix).toMatchInlineSnapshot(`
    {
      "segment": "employed",
      "decisions": [
        { "incomeRange": "0-1000", "debtRatio": "0-20%", "decision": "reject", "score": 150 },
        { "incomeRange": "0-1000", "debtRatio": "20-40%", "decision": "reject", "score": 100 },
        { "incomeRange": "1000-2500", "debtRatio": "0-20%", "decision": "review", "score": 450 },
        { "incomeRange": "1000-2500", "debtRatio": "20-40%", "decision": "review", "score": 380 },
        { "incomeRange": "2500-5000", "debtRatio": "0-20%", "decision": "approve", "score": 720 },
        { "incomeRange": "2500-5000", "debtRatio": "20-40%", "decision": "approve", "score": 640 },
        { "incomeRange": "5000+", "debtRatio": "0-20%", "decision": "approve", "score": 920 },
        { "incomeRange": "5000+", "debtRatio": "20-40%", "decision": "approve", "score": 850 },
      ]
    }
  `)
})
```

**Résultats Stryker sur l'algorithme**

```bash
$ npx stryker run

Fichier                     | % Score | Survivants | Tués | Timeout
----------------------------|---------|------------|------|--------
creditScorer.ts             |   98.2% |          2 |  108 |      3
incomeScore.ts              |  100.0% |          0 |   42 |      0
debtRatioScore.ts           |   97.8% |          1 |   45 |      1
paymentHistoryScore.ts      |  100.0% |          0 |   38 |      0
decisionMatrix.ts           |   96.5% |          2 |   56 |      0

Score global                |   98.4% |

2 mutants survivants dans creditScorer.ts :
  Ligne 87 : ConditionalExpression — `score >= 900` → `score > 900`
  Ligne 112: ArithmeticOperator — `weights.income * 0.35` → `weights.income * 0.36`
```

Ces 2 mutants survivants ont conduit à ajouter 2 tests de valeurs limites précises, portant le score à 100%.

### Résultats Mesurés

| Indicateur | Résultat |
|-----------|----------|
| Mutation score (algorithme) | 98% → 100% après corrections |
| Bugs en production sur le scoring | 0 depuis le lancement |
| Temps de modification des règles | 2h (tests + déploiement) |
| Couverture des branches | 97% |
| Documentation de l'algorithme | Tests = spec exécutable |

### Leçon Clé

Le TDD sur la logique métier critique offre le meilleur ROI en testing. Les tests deviennent la spécification exécutable — quand les règles métier changent, modifier les tests en premier force à réfléchir à l'impact avant de modifier le code. Le property-based testing avec fast-check est indispensable pour les algorithmes numériques : il trouve des edge cases qu'aucun développeur n'aurait imaginé manuellement.

---

## Synthèse : Choisir la Bonne Approche

| Situation | Approche recommandée | Cas illustré |
|-----------|---------------------|-------------|
| Migration Jest → Vitest sur projet Vite | Drop-in replacement en 2 jours | Cas 1 |
| Ajouter des tests à du code legacy | Characterization tests d'abord | Cas 2 |
| Services qui s'appellent mutuellement | Contract testing avec Pact | Cas 3 |
| Logique métier complexe avec règles précises | TDD + property-based testing | Cas 4 |
| Performance CI dégradée | Vitest + sharding Playwright | Cas 1 |
| Bugs en production sur la facturation | InMemoryRepository + tests d'intégration | Cas 2 |
| Déploiements indépendants entre équipes | Pact Broker + can-i-deploy | Cas 3 |
| Algorithme avec invariants mathématiques | fast-check + mutation testing | Cas 4 |
