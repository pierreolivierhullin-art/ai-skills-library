# Tests Unitaires et d'Intégration — Vitest et Patterns Avancés

## Architecture de Tests : Organiser son Projet

La structure des fichiers de test reflète la maturité d'une équipe. Deux approches dominent : la co-localisation (tests à côté des fichiers source) et le dossier `__tests__` centralisé.

**Co-localisation** — recommandée pour les projets modernes :

```
src/
  features/
    billing/
      invoiceCalculator.ts
      invoiceCalculator.test.ts       ← test co-localisé
      invoiceCalculator.bench.ts      ← benchmark optionnel
    users/
      userService.ts
      userService.test.ts
      userService.integration.test.ts ← suffixe pour distinguer
```

**Dossier centralisé** — utile pour les tests d'intégration lourds :

```
src/
  features/billing/invoiceCalculator.ts
tests/
  unit/billing/invoiceCalculator.test.ts
  integration/billing/invoiceCalculator.integration.test.ts
  e2e/billing/checkout.e2e.test.ts
```

**Naming conventions** à respecter impérativement :

| Suffixe | Usage | Environnement |
|---------|-------|---------------|
| `.test.ts` | Tests unitaires et d'intégration légers | `node` ou `jsdom` |
| `.integration.test.ts` | Tests avec vraie DB ou services externes | `node` |
| `.e2e.test.ts` | Tests end-to-end Playwright | `chromium` |
| `.bench.ts` | Benchmarks de performance | `node` |
| `.spec.ts` | Alias de `.test.ts` — éviter le mélange dans un même projet | — |

La cohérence prime sur la convention choisie. Ce qui compte : un développeur qui rejoint l'équipe doit comprendre instantanément où se trouvent les tests d'un module.

---

## Vitest Config Avancée

### Configuration de base avec workspace mode

Le workspace mode de Vitest permet de gérer plusieurs environnements dans un seul projet — essentiel pour les monorepos ou les projets full-stack.

```typescript
// vitest.config.ts (racine)
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    workspace: ['packages/*', 'apps/*'],
  },
})
```

```typescript
// packages/core/vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    name: 'core',
    environment: 'node',
    include: ['src/**/*.test.ts'],
    exclude: ['src/**/*.integration.test.ts'],
    coverage: {
      provider: 'v8',
      include: ['src/**/*.ts'],
      exclude: [
        'src/**/*.test.ts',
        'src/**/*.d.ts',
        'src/index.ts',          // re-exports seulement
        'src/types/**',          // types purs, pas de logique
        'src/**/generated/**',   // code généré automatiquement
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 70,
        statements: 80,
      },
    },
  },
})
```

```typescript
// apps/frontend/vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    name: 'frontend',
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    include: ['src/**/*.test.tsx', 'src/**/*.test.ts'],
  },
})
```

### `vi.stubEnv` pour les variables d'environnement

Contrairement à la manipulation directe de `process.env`, `vi.stubEnv` restaure automatiquement les valeurs après le test.

```typescript
import { describe, it, expect, vi, afterEach } from 'vitest'
import { getApiBaseUrl } from './config'

describe('getApiBaseUrl', () => {
  afterEach(() => {
    vi.unstubAllEnvs() // restauration automatique
  })

  it('retourne l\'URL de production en mode prod', () => {
    vi.stubEnv('NODE_ENV', 'production')
    vi.stubEnv('API_URL', 'https://api.monapp.com')

    expect(getApiBaseUrl()).toBe('https://api.monapp.com')
  })

  it('retourne localhost en mode développement', () => {
    vi.stubEnv('NODE_ENV', 'development')
    // API_URL non défini → valeur par défaut

    expect(getApiBaseUrl()).toBe('http://localhost:3000')
  })
})
```

### In-source testing

Les in-source tests coexistent avec le code source dans le même fichier — idéal pour les fonctions utilitaires pures.

```typescript
// src/utils/formatPrice.ts
export function formatPrice(cents: number, currency = 'EUR'): string {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency,
  }).format(cents / 100)
}

// Le bloc if (import.meta.vitest) est éliminé en production
if (import.meta.vitest) {
  const { it, expect } = import.meta.vitest

  it('formate 1999 centimes en 19,99 €', () => {
    expect(formatPrice(1999)).toBe('19,99 €')
  })

  it('gère le dollar américain', () => {
    expect(formatPrice(1999, 'USD')).toBe('19,99 $US')
  })
}
```

Activer dans la config :

```typescript
test: {
  includeSource: ['src/**/*.ts'],
}
```

---

## Patterns d'Isolation : Dependency Injection et Ports & Adapters

### Constructor Injection

```typescript
// src/features/users/userService.ts
export interface UserRepository {
  findById(id: string): Promise<User | null>
  save(user: User): Promise<User>
  delete(id: string): Promise<void>
}

export interface EmailService {
  sendWelcomeEmail(email: string): Promise<void>
}

export class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly emailService: EmailService,
  ) {}

  async createUser(data: CreateUserDto): Promise<User> {
    const existing = await this.userRepository.findById(data.email)
    if (existing) throw new Error('Utilisateur déjà existant')

    const user = new User(data)
    const saved = await this.userRepository.save(user)
    await this.emailService.sendWelcomeEmail(saved.email)
    return saved
  }
}
```

### In-Memory Repository : implémentation pour les tests

```typescript
// src/test/repositories/inMemoryUserRepository.ts
export class InMemoryUserRepository implements UserRepository {
  private users = new Map<string, User>()

  async findById(id: string): Promise<User | null> {
    return this.users.get(id) ?? null
  }

  async save(user: User): Promise<User> {
    this.users.set(user.id, user)
    return user
  }

  async delete(id: string): Promise<void> {
    this.users.delete(id)
  }

  // Méthodes de test uniquement — pas dans l'interface
  clear(): void {
    this.users.clear()
  }

  getAll(): User[] {
    return Array.from(this.users.values())
  }

  seed(users: User[]): void {
    users.forEach(u => this.users.set(u.id, u))
  }
}
```

```typescript
// src/features/users/userService.test.ts
describe('UserService', () => {
  let userRepository: InMemoryUserRepository
  let emailService: { sendWelcomeEmail: ReturnType<typeof vi.fn> }
  let userService: UserService

  beforeEach(() => {
    userRepository = new InMemoryUserRepository()
    emailService = { sendWelcomeEmail: vi.fn().mockResolvedValue(undefined) }
    userService = new UserService(userRepository, emailService)
  })

  it('crée un utilisateur et envoie l\'email de bienvenue', async () => {
    const data = { email: 'alice@example.com', name: 'Alice' }

    const user = await userService.createUser(data)

    expect(user.email).toBe('alice@example.com')
    expect(userRepository.getAll()).toHaveLength(1)
    expect(emailService.sendWelcomeEmail).toHaveBeenCalledWith('alice@example.com')
  })

  it('lève une erreur si l\'utilisateur existe déjà', async () => {
    const data = { email: 'alice@example.com', name: 'Alice' }
    await userService.createUser(data)

    await expect(userService.createUser(data)).rejects.toThrow('Utilisateur déjà existant')
  })
})
```

---

## Test Doubles : Mock, Stub, Spy, Fake

Ces quatre concepts sont souvent confondus. Chacun a un rôle précis.

| Type | Définition | Usage principal |
|------|-----------|-----------------|
| **Stub** | Retourne des valeurs prédéfinies, sans vérification | Simuler les dépendances qui fournissent des données |
| **Mock** | Vérifie que certaines méthodes sont appelées (avec quels args) | Tester les effets de bord (emails, analytics, événements) |
| **Spy** | Enveloppe une vraie implémentation pour observer les appels | Observer sans modifier le comportement |
| **Fake** | Implémentation simplifiée mais fonctionnelle | Remplacer des services complexes (DB, cache) en tests |

```typescript
// STUB : fournit des données, on n'assertit pas dessus
const stubUserRepo = {
  findById: vi.fn().mockResolvedValue({ id: '1', name: 'Alice' }),
  save: vi.fn(),
}

// MOCK : on assertit sur les appels
const mockEmailService = {
  sendWelcomeEmail: vi.fn().mockResolvedValue(undefined),
}
// ... après l'appel :
expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledOnce()
expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith('alice@example.com')

// SPY : observe sans remplacer
const logSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
// ... après l'appel :
expect(logSpy).toHaveBeenCalledWith(expect.stringContaining('Erreur critique'))

// FAKE : InMemoryUserRepository est un Fake — voir section précédente
```

---

## `vi.mock` et `vi.doMock` : Mocking de Modules ES

### Mock complet d'un module

```typescript
// vi.mock est hoisted automatiquement en haut du fichier
vi.mock('./emailService', () => ({
  sendWelcomeEmail: vi.fn().mockResolvedValue(undefined),
  sendPasswordReset: vi.fn().mockResolvedValue(undefined),
}))

import { sendWelcomeEmail } from './emailService'
import { createUser } from './userService'

it('envoie un email de bienvenue', async () => {
  await createUser({ email: 'test@example.com' })
  expect(sendWelcomeEmail).toHaveBeenCalledWith('test@example.com')
})
```

### Mock partiel avec `vi.importActual`

```typescript
vi.mock('./config', async (importOriginal) => {
  const actual = await importOriginal<typeof import('./config')>()
  return {
    ...actual,
    // On remplace seulement la partie qu'on veut contrôler
    getFeatureFlag: vi.fn().mockReturnValue(true),
  }
})
```

### `vi.doMock` pour les mocks conditionnels (non-hoisted)

```typescript
it('gère l\'indisponibilité du service de paiement', async () => {
  vi.doMock('./paymentService', () => ({
    charge: vi.fn().mockRejectedValue(new Error('Service indisponible')),
  }))

  const { processOrder } = await import('./orderService')
  await expect(processOrder({ amount: 100 })).rejects.toThrow('Service indisponible')

  vi.doUnmock('./paymentService')
})
```

---

## Tests Asynchrones

```typescript
describe('tests asynchrones', () => {
  // async/await — approche recommandée
  it('résout avec la valeur correcte', async () => {
    const result = await fetchUser('123')
    expect(result.name).toBe('Alice')
  })

  // Vérifier les rejections
  it('rejette avec un message d\'erreur', async () => {
    await expect(fetchUser('invalid-id')).rejects.toThrow('Utilisateur introuvable')
    await expect(fetchUser('invalid-id')).rejects.toThrowError(/introuvable/i)
  })

  // toResolve / toReject (Vitest uniquement)
  it('la promesse résout sans erreur', async () => {
    await expect(saveUser(validUser)).resolves.toBeDefined()
  })

  // Erreurs async dans les callbacks — piège classique
  it('erreur dans un callback async', async () => {
    // FAUX POSITIF : le test passe même si l'assertion échoue
    // eventEmitter.on('data', async (data) => {
    //   expect(data).toBe('invalide') // silencieusement ignoré
    // })

    // CORRECT : utiliser une promesse explicite
    const result = await new Promise<string>((resolve) => {
      eventEmitter.on('data', resolve)
      eventEmitter.emit('data', 'valeur-attendue')
    })
    expect(result).toBe('valeur-attendue')
  })
})
```

---

## Matchers Personnalisés avec `expect.extend`

```typescript
// src/test/matchers/index.ts
import { expect } from 'vitest'

interface CustomMatchers<R = unknown> {
  toBeValidEmail(): R
  toBeWithinRange(min: number, max: number): R
}

declare module 'vitest' {
  interface Assertion<T = any> extends CustomMatchers<T> {}
  interface AsymmetricMatchersContaining extends CustomMatchers {}
}

expect.extend({
  toBeValidEmail(received: string) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    const pass = emailRegex.test(received)
    return {
      pass,
      message: () =>
        pass
          ? `"${received}" ne devrait pas être un email valide`
          : `"${received}" devrait être un email valide`,
    }
  },

  toBeWithinRange(received: number, min: number, max: number) {
    const pass = received >= min && received <= max
    return {
      pass,
      message: () =>
        `${received} devrait être entre ${min} et ${max}`,
    }
  },
})

// Utilisation dans les tests
it('valide le format email', () => {
  expect('alice@example.com').toBeValidEmail()
  expect('pas-un-email').not.toBeValidEmail()
})

it('le score est dans la plage valide', () => {
  expect(calculateScore(user)).toBeWithinRange(0, 1000)
})
```

---

## Lifecycle Hooks : Quand Utiliser Chacun

```typescript
describe('lifecycle hooks', () => {
  // beforeAll : setup coûteux partagé — connexion DB, démarrage serveur
  // ATTENTION : l'état est partagé entre tous les tests → risque de couplage
  beforeAll(async () => {
    await db.connect()
  })

  afterAll(async () => {
    await db.disconnect()
  })

  // beforeEach : reset de l'état entre chaque test → toujours préférer ceci
  beforeEach(() => {
    userRepository.clear()
    vi.clearAllMocks() // reset les appels sans supprimer l'implémentation
  })

  // afterEach : nettoyage des effets de bord du test
  afterEach(async () => {
    await db.rollback() // annuler les changements faits pendant le test
  })

  // PIÈGES À ÉVITER
  // ❌ Ne pas muter des variables dans beforeAll puis les utiliser dans les tests
  // ❌ Ne pas dépendre de l'ordre des tests (chaque test doit être indépendant)
  // ❌ Ne pas utiliser afterAll pour du cleanup qui devrait être dans afterEach
})
```

---

## Test des Dates avec `vi.useFakeTimers`

```typescript
describe('tests de dates et timers', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('calcule l\'expiration à 30 jours', () => {
    vi.setSystemTime(new Date('2024-01-15T10:00:00Z'))

    const subscription = createSubscription({ durationDays: 30 })

    expect(subscription.expiresAt).toEqual(new Date('2024-02-14T10:00:00Z'))
  })

  it('envoie un rappel après 24h', async () => {
    const sendReminder = vi.fn()
    scheduleReminder(sendReminder, 24 * 60 * 60 * 1000)

    // Avancer le temps de 23h → pas encore
    vi.advanceTimersByTime(23 * 60 * 60 * 1000)
    expect(sendReminder).not.toHaveBeenCalled()

    // Avancer d'1h de plus → déclenchement
    vi.advanceTimersByTime(1 * 60 * 60 * 1000)
    expect(sendReminder).toHaveBeenCalledOnce()
  })

  it('gère les setInterval avec runAllTimers', async () => {
    const heartbeat = vi.fn()
    startHeartbeat(heartbeat, 5000)

    vi.runAllTimers() // exécute tous les timers en attente
    expect(heartbeat).toHaveBeenCalled()
  })
})
```

---

## Snapshot Testing

Les snapshots capturent une représentation sérialisée d'une valeur. Ils sont utiles pour les objets complexes, les structures de configuration, et les outputs de transformation.

```typescript
// toMatchSnapshot : écrit dans un fichier .snap externe
it('génère la config complète', () => {
  const config = generateDeploymentConfig({ env: 'production', region: 'eu-west-1' })
  expect(config).toMatchSnapshot()
})

// toMatchInlineSnapshot : la snapshot est inline dans le code — plus lisible
it('génère le résumé de facture', () => {
  const invoice = createInvoiceSummary({
    items: [
      { name: 'Plan Pro', amount: 4900 },
      { name: 'Siège supplémentaire', amount: 990 },
    ],
    taxRate: 0.2,
  })

  expect(invoice).toMatchInlineSnapshot(`
    {
      "subtotal": 5890,
      "tax": 1178,
      "total": 7068,
      "currency": "EUR",
      "itemCount": 2,
    }
  `)
})
```

**Quand utiliser les snapshots :**
- Objets de configuration complexes dont on veut détecter les changements accidentels
- Output de transformation de données (sérialisation, mappers)
- Structure d'erreurs d'API

**Quand les éviter :**
- Composants React (préférer les assertions explicites sur le comportement)
- Valeurs qui changent souvent légitimement (timestamps, IDs générés)
- Quand la snapshot est si grande qu'on ne la lit plus

---

## Tests d'Intégration avec vraie DB

### Transactions pour le rollback automatique

```typescript
// src/test/helpers/dbTestHelper.ts
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export async function withTestTransaction<T>(
  fn: (tx: Omit<PrismaClient, '$connect' | '$disconnect' | '$on' | '$transaction' | '$use'>) => Promise<T>
): Promise<T> {
  return prisma.$transaction(async (tx) => {
    const result = await fn(tx)
    // Toujours rollback après le test
    throw new RollbackError(result)
  }).catch((err) => {
    if (err instanceof RollbackError) return err.result as T
    throw err
  })
}

class RollbackError {
  constructor(public result: unknown) {}
}
```

```typescript
// src/features/billing/invoiceRepository.integration.test.ts
describe('InvoiceRepository — intégration DB', () => {
  it('sauvegarde et retrouve une facture', async () => {
    await withTestTransaction(async (tx) => {
      const repo = new InvoiceRepository(tx)
      const invoice = await repo.create({
        customerId: 'cust_123',
        amount: 4900,
        status: 'draft',
      })

      const found = await repo.findById(invoice.id)
      expect(found).toMatchObject({ amount: 4900, status: 'draft' })
      // La transaction est rollbackée → pas de données persistées
    })
  })
})
```

### TestContainers pour PostgreSQL

```typescript
// src/test/helpers/testDatabase.ts
import { PostgreSqlContainer } from '@testcontainers/postgresql'
import { PrismaClient } from '@prisma/client'
import { execSync } from 'child_process'

let container: Awaited<ReturnType<typeof PostgreSqlContainer.prototype.start>>
let prisma: PrismaClient

export async function setupTestDatabase() {
  container = await new PostgreSqlContainer('postgres:16-alpine')
    .withDatabase('testdb')
    .withUsername('test')
    .withPassword('test')
    .start()

  const connectionString = container.getConnectionUri()
  process.env.DATABASE_URL = connectionString

  // Appliquer les migrations
  execSync('npx prisma migrate deploy', {
    env: { ...process.env, DATABASE_URL: connectionString },
  })

  prisma = new PrismaClient({ datasources: { db: { url: connectionString } } })
  await prisma.$connect()

  return { prisma, container }
}

export async function teardownTestDatabase() {
  await prisma.$disconnect()
  await container.stop()
}
```

```typescript
// vitest.config.ts — timeout plus long pour TestContainers
test: {
  globalSetup: './src/test/globalSetup.ts',
  hookTimeout: 60_000, // 60 secondes pour démarrer le conteneur
  testTimeout: 30_000,
}
```

---

## Résumé des Décisions Clés

| Situation | Pattern recommandé |
|-----------|-------------------|
| Tester la logique métier isolée | Constructor injection + InMemoryRepository |
| Tester les effets de bord (emails, events) | Mock avec assertion sur les appels |
| Observer une méthode sans la remplacer | Spy avec `vi.spyOn` |
| Remplacer un service externe complet | Fake (implémentation simplifiée) |
| Variables d'environnement dans les tests | `vi.stubEnv` + `vi.unstubAllEnvs()` |
| Dates et timers | `vi.useFakeTimers` + `vi.setSystemTime` |
| Tests d'intégration DB — isolation | Transactions avec rollback |
| Tests d'intégration DB — vraie infra | TestContainers |
| Objets complexes de configuration | Snapshot inline |
