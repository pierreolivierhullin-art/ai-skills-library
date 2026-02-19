---
name: testing-strategies
version: 1.0.0
description: >
  Testing strategies, Vitest unit testing, React Testing Library component testing,
  MSW mock service worker, Playwright component tests, mutation testing Stryker,
  contract testing Pact, property-based testing fast-check, test doubles mocks stubs spies,
  coverage thresholds, snapshot testing, integration testing, test pyramid,
  TDD red-green-refactor, given-when-then BDD, AAA pattern arrange-act-assert,
  test isolation, flaky tests, testing best practices
---

# Testing Strategies — Tests Automatisés de A à Z

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu mets en place une stratégie de tests pour un nouveau projet ou une équipe
- Les tests existants sont lents, fragiles (flaky), ou ne détectent pas les vrais bugs
- Tu impléments du TDD ou du BDD sur une fonctionnalité complexe
- Tu veux introduire le mutation testing pour mesurer la qualité des tests
- Tu as besoin de mocker des APIs externes sans les appeler réellement
- Tu veux valider des contrats d'API entre microservices (contract testing)

---

## La Pyramide des Tests

```
          /\
         /  \
        / E2E \          → Playwright (5-10% des tests)
       /________\
      /          \
     / Integration \     → Supertest, API tests (20-30%)
    /______________\
   /                \
  /    Unit Tests    \   → Vitest, RTL (60-70%)
 /____________________\
```

**Règle d'or** : plus un test est haut dans la pyramide, plus il est lent et fragile. Maximiser les tests unitaires, minimiser les E2E.

---

## Vitest — Tests Unitaires Modernes

### Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    environment: 'node',         // 'jsdom' pour les composants React
    globals: true,                // describe, it, expect sans import
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 70,
        statements: 80,
      },
      exclude: ['**/*.config.*', '**/index.ts', '**/*.d.ts'],
    },
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
});
```

### Patterns Fondamentaux

```typescript
// Pattern AAA (Arrange, Act, Assert)
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { PanierService } from '@/services/panier';
import { ProduitsRepository } from '@/repositories/produits';

describe('PanierService', () => {
  let service: PanierService;
  let mockRepo: MockRepository<ProduitsRepository>;

  beforeEach(() => {
    // Arrange : préparer l'état initial
    mockRepo = createMockRepository(ProduitsRepository);
    service = new PanierService(mockRepo);
  });

  it('doit calculer le total avec remise', async () => {
    // Arrange
    mockRepo.trouver.mockResolvedValue({ id: '1', prix: 100, tva: 0.2 });

    // Act
    const total = await service.calculerTotal('1', { remise: 0.1, quantite: 2 });

    // Assert
    expect(total).toEqual({
      sousTotal: 200,
      remise: 20,
      tva: 36,
      total: 216,
    });
  });

  it('doit lever une erreur si le produit est introuvable', async () => {
    mockRepo.trouver.mockResolvedValue(null);

    await expect(service.calculerTotal('inexistant', { quantite: 1 }))
      .rejects.toThrow('Produit introuvable : inexistant');
  });
});
```

### Test Doubles : Mock, Stub, Spy

```typescript
import { vi, Mock } from 'vitest';

// Mock : remplacer complètement un module
vi.mock('@/lib/email', () => ({
  envoyerEmail: vi.fn().mockResolvedValue({ messageId: 'mock-123' }),
}));

// Spy : observer sans remplacer
const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
// Après le test :
expect(spy).toHaveBeenCalledWith('Erreur attendue');
spy.mockRestore();

// Stub : retourner des données de test
const stubDate = vi.spyOn(Date, 'now').mockReturnValue(1700000000000);

// Timer fakes : tester du code avec setTimeout/setInterval
vi.useFakeTimers();
const callback = vi.fn();
setTimeout(callback, 1000);
vi.advanceTimersByTime(999);
expect(callback).not.toHaveBeenCalled();
vi.advanceTimersByTime(1);
expect(callback).toHaveBeenCalledOnce();
vi.useRealTimers();
```

---

## React Testing Library — Composants

### Principe : Tester le comportement, pas l'implémentation

```typescript
// tests/components/FormulaireConnexion.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FormulaireConnexion } from '@/components/FormulaireConnexion';

const user = userEvent.setup();

describe('FormulaireConnexion', () => {
  it('doit afficher les erreurs de validation', async () => {
    render(<FormulaireConnexion onConnexion={vi.fn()} />);

    // Cliquer sur soumettre sans remplir
    await user.click(screen.getByRole('button', { name: /se connecter/i }));

    // Vérifier les messages d'erreur accessibles
    expect(await screen.findByRole('alert', { name: /email requis/i })).toBeInTheDocument();
  });

  it('doit appeler onConnexion avec les données valides', async () => {
    const mockConnexion = vi.fn().mockResolvedValue({ success: true });
    render(<FormulaireConnexion onConnexion={mockConnexion} />);

    await user.type(screen.getByLabelText(/email/i), 'alice@example.com');
    await user.type(screen.getByLabelText(/mot de passe/i), 'MonMotDePasse123!');
    await user.click(screen.getByRole('button', { name: /se connecter/i }));

    await waitFor(() => {
      expect(mockConnexion).toHaveBeenCalledWith({
        email: 'alice@example.com',
        motDePasse: 'MonMotDePasse123!',
      });
    });
  });

  it('doit afficher un message d\'erreur si la connexion échoue', async () => {
    const mockConnexion = vi.fn().mockRejectedValue(new Error('Identifiants invalides'));
    render(<FormulaireConnexion onConnexion={mockConnexion} />);

    await user.type(screen.getByLabelText(/email/i), 'alice@example.com');
    await user.type(screen.getByLabelText(/mot de passe/i), 'mauvais');
    await user.click(screen.getByRole('button', { name: /se connecter/i }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Identifiants invalides');
  });
});
```

---

## MSW — Mock Service Worker

MSW intercepte les requêtes réseau au niveau du service worker (navigateur) ou de Node.js. Les tests utilisent de vraies requêtes `fetch`/`axios` sans modifier le code source.

```typescript
// tests/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      nom: 'Alice',
      email: 'alice@example.com',
    });
  }),

  http.post('/api/auth/login', async ({ request }) => {
    const body = await request.json() as { email: string; motDePasse: string };

    if (body.email === 'alice@example.com' && body.motDePasse === 'correct') {
      return HttpResponse.json({ token: 'jwt-mock-token' });
    }

    return HttpResponse.json(
      { message: 'Identifiants invalides' },
      { status: 401 },
    );
  }),
];

// tests/setup.ts
import { setupServer } from 'msw/node';
import { handlers } from './mocks/handlers';

const server = setupServer(...handlers);

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Dans un test : surcharger le handler pour un cas spécifique
it('doit gérer les erreurs réseau', async () => {
  server.use(
    http.get('/api/users/123', () => {
      return HttpResponse.error();  // Simule une panne réseau
    }),
  );

  // ...le test vérifie la gestion d'erreur
});
```

---

## Tests d'Intégration — API

```typescript
// tests/integration/users.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { app } from '@/app';
import { prisma } from '@/lib/prisma';

describe('POST /api/users', () => {
  beforeAll(async () => {
    // Utiliser une DB de test (PostgreSQL avec transactions)
    await prisma.$executeRaw`BEGIN`;
  });

  afterAll(async () => {
    await prisma.$executeRaw`ROLLBACK`;
    await prisma.$disconnect();
  });

  it('doit créer un utilisateur avec un email unique', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', nom: 'Test User' })
      .expect(201);

    expect(res.body).toMatchObject({
      id: expect.any(String),
      email: 'test@example.com',
      nom: 'Test User',
      créeA: expect.any(String),
    });

    // Vérifier en base
    const userEnBase = await prisma.user.findUnique({
      where: { email: 'test@example.com' },
    });
    expect(userEnBase).not.toBeNull();
  });

  it('doit retourner 409 si l\'email existe déjà', async () => {
    await prisma.user.create({ data: { email: 'existant@example.com', nom: 'Existant' } });

    await request(app)
      .post('/api/users')
      .send({ email: 'existant@example.com', nom: 'Nouveau' })
      .expect(409);
  });
});
```

---

## Property-Based Testing avec fast-check

```typescript
import fc from 'fast-check';
import { calculerRemise, formaterPrix } from '@/utils/prix';

describe('calculerRemise — property-based', () => {
  it('la remise doit toujours être entre 0 et le prix original', () => {
    fc.assert(
      fc.property(
        fc.float({ min: 0.01, max: 10_000 }),  // prix
        fc.float({ min: 0, max: 1 }),            // taux de remise
        (prix, taux) => {
          const remise = calculerRemise(prix, taux);
          return remise >= 0 && remise <= prix;
        },
      ),
    );
  });

  it('formaterPrix doit toujours retourner une string non vide', () => {
    fc.assert(
      fc.property(
        fc.float({ min: 0, max: 1_000_000 }),
        fc.constantFrom('EUR', 'USD', 'GBP'),
        (montant, devise) => {
          const résultat = formaterPrix(montant, devise);
          return typeof résultat === 'string' && résultat.length > 0;
        },
      ),
    );
  });
});
```

---

## Mutation Testing avec Stryker

```bash
# Installation
npm install --save-dev @stryker-mutator/core @stryker-mutator/vitest-runner
```

```json
// stryker.config.json
{
  "testRunner": "vitest",
  "reporters": ["html", "clear-text"],
  "coverageAnalysis": "perTest",
  "mutate": ["src/**/*.ts", "!src/**/*.d.ts"],
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  }
}
```

**Mutation Score** : un test qui passe même avec du code muté n'est pas un vrai test. Stryker révèle les assertions manquantes.

```typescript
// Code source
function estMajeur(age: number): boolean {
  return age >= 18;  // Stryker mutera en > 18, <= 18, etc.
}

// Test insuffisant (ne détecte pas la mutation >= → > )
it('retourne true pour 18 ans', () => {
  expect(estMajeur(18)).toBe(true);  // Passe avec age > 18 ? NON → mutation survivante
});

// Test complet
it('retourne true pour 18 ans exactement', () => {
  expect(estMajeur(18)).toBe(true);   // Tue la mutation >= → >
  expect(estMajeur(17)).toBe(false);  // Tue la mutation >= → <=
  expect(estMajeur(19)).toBe(true);
});
```

---

## Références

- `references/unit-integration.md` — Vitest avancé, test doubles, isolation, patterns DI, in-memory repositories
- `references/component-e2e.md` — React Testing Library avancé, Playwright component tests, visual regression
- `references/advanced-patterns.md` — MSW avancé, Pact contract testing, Stryker mutation, fast-check, test architecture
- `references/case-studies.md` — 4 cas : migration Jest→Vitest, 0%→80% coverage, contract testing microservices, TDD feature
