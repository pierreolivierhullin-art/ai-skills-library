# Tests Composants et E2E — React Testing Library et Playwright

## React Testing Library : Philosophie et Queries Prioritaires

React Testing Library repose sur un principe central : **tester ce que l'utilisateur voit et fait**, pas les détails d'implémentation. Un test bien écrit ne sait pas si le composant utilise `useState` ou un contexte Redux — il interagit avec l'interface comme un utilisateur réel.

La hiérarchie des queries est la clé. Toujours utiliser la query la plus accessible disponible :

| Priorité | Query | Quand l'utiliser |
|----------|-------|-----------------|
| 1 | `getByRole` | Boutons, liens, inputs, headings — presque toujours |
| 2 | `getByLabelText` | Champs de formulaire avec label associé |
| 3 | `getByPlaceholderText` | Si pas de label (à éviter — inaccessible) |
| 4 | `getByText` | Texte visible non interactif |
| 5 | `getByDisplayValue` | Valeur actuelle d'un input/select |
| 6 | `getByAltText` | Images avec alt text |
| 7 | `getByTitle` | Attribut title (rarement utile) |
| 8 | `getByTestId` | Dernier recours — indique souvent un problème d'accessibilité |

---

## `getByRole` en Profondeur

`getByRole` est la query la plus puissante car elle cible les éléments par leur rôle ARIA — exactement ce que les technologies d'assistance utilisent.

```typescript
import { render, screen } from '@testing-library/react'
import { LoginForm } from './LoginForm'

describe('LoginForm', () => {
  it('affiche les champs et le bouton de connexion', () => {
    render(<LoginForm />)

    // Heading de niveau 1
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Connexion')

    // Input de type texte — accessible par son label
    const emailInput = screen.getByRole('textbox', { name: /adresse email/i })
    expect(emailInput).toBeInTheDocument()

    // Checkbox avec état
    const rememberMe = screen.getByRole('checkbox', { name: /se souvenir de moi/i })
    expect(rememberMe).not.toBeChecked()

    // Bouton submit
    const submitBtn = screen.getByRole('button', { name: /se connecter/i })
    expect(submitBtn).toBeEnabled()
  })

  it('désactive le bouton si le formulaire est invalide', () => {
    render(<LoginForm />)
    // Bouton désactivé initialement (formulaire vide)
    expect(screen.getByRole('button', { name: /se connecter/i })).toBeDisabled()
  })

  it('affiche les options du select', () => {
    render(<LanguageSelector />)

    // Option sélectionnée
    expect(screen.getByRole('option', { name: 'Français', selected: true })).toBeInTheDocument()

    // Option non sélectionnée
    expect(screen.getByRole('option', { name: 'English', selected: false })).toBeInTheDocument()
  })

  it('navigue dans un arbre accessible', () => {
    render(<NavigationMenu />)

    // Élément avec hidden: true inclut les éléments ARIA cachés
    const hiddenItem = screen.getByRole('menuitem', { name: /paramètres/i, hidden: true })
    expect(hiddenItem).toBeInTheDocument()
  })
})
```

---

## `userEvent` v14 : Interactions Réalistes

`userEvent` v14 simule les interactions utilisateur de manière plus réaliste que `fireEvent`. La méthode `setup()` est obligatoire — elle crée un contexte qui gère l'état des interactions (position du curseur, touches enfoncées, etc.).

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LoginForm } from './LoginForm'

describe('LoginForm — interactions', () => {
  // setup() en dehors des tests pour partager l'instance
  const user = userEvent.setup()

  it('saisit un email et un mot de passe puis soumet', async () => {
    const onSubmit = vi.fn()
    render(<LoginForm onSubmit={onSubmit} />)

    // type simule la frappe caractère par caractère
    await user.type(screen.getByLabelText(/adresse email/i), 'alice@example.com')
    await user.type(screen.getByLabelText(/mot de passe/i), 'secret123')

    // click sur le bouton submit
    await user.click(screen.getByRole('button', { name: /se connecter/i }))

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'alice@example.com',
      password: 'secret123',
    })
  })

  it('sélectionne une option dans un select', async () => {
    render(<CountrySelector />)

    await user.selectOptions(
      screen.getByRole('combobox', { name: /pays/i }),
      'France'
    )

    expect(screen.getByRole('option', { name: 'France' })).toBeSelected()
  })

  it('upload un fichier', async () => {
    render(<FileUploader />)

    const file = new File(['contenu du fichier'], 'photo.png', { type: 'image/png' })
    const input = screen.getByLabelText(/choisir un fichier/i)

    await user.upload(input, file)

    expect(screen.getByText('photo.png')).toBeInTheDocument()
  })

  it('navigation clavier dans un menu', async () => {
    render(<DropdownMenu />)

    // Ouvrir avec Enter
    await user.keyboard('{Enter}')
    expect(screen.getByRole('menu')).toBeVisible()

    // Naviguer avec les flèches
    await user.keyboard('{ArrowDown}')
    await user.keyboard('{ArrowDown}')
    await user.keyboard('{Enter}')

    expect(screen.getByText('Deuxième option sélectionnée')).toBeInTheDocument()
  })

  it('clear puis retape dans un input', async () => {
    render(<SearchBar defaultValue="ancienne recherche" />)

    const input = screen.getByRole('searchbox')
    await user.clear(input)
    await user.type(input, 'nouvelle recherche')

    expect(input).toHaveValue('nouvelle recherche')
  })
})
```

---

## Testing des Composants Asynchrones

```typescript
import { render, screen, waitFor, waitForElementToBeRemoved } from '@testing-library/react'

describe('UserProfile — async', () => {
  it('affiche les données après chargement (findBy)', async () => {
    render(<UserProfile userId="123" />)

    // findBy* attend automatiquement (1000ms par défaut)
    const name = await screen.findByText('Alice Martin')
    expect(name).toBeInTheDocument()
  })

  it('retire le spinner après chargement', async () => {
    render(<UserProfile userId="123" />)

    // Attendre que l'élément disparaisse — plus expressif
    await waitForElementToBeRemoved(() => screen.queryByRole('progressbar'))

    expect(screen.getByText('Alice Martin')).toBeInTheDocument()
  })

  it('affiche un message d\'erreur si la requête échoue', async () => {
    server.use(
      http.get('/api/users/123', () => HttpResponse.error()),
    )

    render(<UserProfile userId="123" />)

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('Impossible de charger le profil')
    })
  })

  it('waitFor avec assertion multiple', async () => {
    render(<Dashboard />)

    await waitFor(() => {
      // Toutes les assertions doivent passer dans le même callback
      expect(screen.getByText('Chiffre d\'affaires')).toBeInTheDocument()
      expect(screen.getByText('15 342 €')).toBeInTheDocument()
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    })
  })
})
```

---

## Custom Render : Wrapper de Providers

La plupart des composants dépendent de providers (Redux, React Query, Router, Theme). Le custom render évite de répéter le setup dans chaque test.

```typescript
// src/test/utils/renderWithProviders.tsx
import { render, RenderOptions } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Provider } from 'react-redux'
import { MemoryRouter } from 'react-router-dom'
import { ThemeProvider } from '../contexts/ThemeContext'
import { createStore } from '../store'

interface RenderWithProvidersOptions extends Omit<RenderOptions, 'wrapper'> {
  initialRoute?: string
  preloadedState?: Partial<RootState>
}

export function renderWithProviders(
  ui: React.ReactElement,
  {
    initialRoute = '/',
    preloadedState = {},
    ...renderOptions
  }: RenderWithProvidersOptions = {}
) {
  // QueryClient configuré pour les tests (pas de retry, pas de refetch)
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  })

  const store = createStore(preloadedState)

  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <MemoryRouter initialEntries={[initialRoute]}>
        <Provider store={store}>
          <QueryClientProvider client={queryClient}>
            <ThemeProvider>
              {children}
            </ThemeProvider>
          </QueryClientProvider>
        </Provider>
      </MemoryRouter>
    )
  }

  return {
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
    store,
    queryClient,
  }
}

// Utilisation dans les tests
it('affiche le tableau de bord de l\'utilisateur connecté', () => {
  renderWithProviders(<Dashboard />, {
    preloadedState: { auth: { user: { name: 'Alice', role: 'admin' } } },
    initialRoute: '/dashboard',
  })

  expect(screen.getByText('Bienvenue, Alice')).toBeInTheDocument()
  expect(screen.getByRole('link', { name: /administration/i })).toBeInTheDocument()
})
```

---

## Test des Hooks Custom

```typescript
import { renderHook, act } from '@testing-library/react'
import { useCounter } from './useCounter'
import { useUserData } from './useUserData'

describe('useCounter', () => {
  it('incrémente et décrémente', () => {
    const { result } = renderHook(() => useCounter(0))

    act(() => result.current.increment())
    expect(result.current.count).toBe(1)

    act(() => result.current.decrement())
    expect(result.current.count).toBe(0)
  })

  it('ne descend pas en dessous du minimum', () => {
    const { result } = renderHook(() => useCounter(0, { min: 0 }))

    act(() => result.current.decrement())
    expect(result.current.count).toBe(0) // bloqué à 0
  })
})

describe('useUserData — hook avec dépendances', () => {
  it('charge les données utilisateur', async () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <QueryClientProvider client={new QueryClient({ defaultOptions: { queries: { retry: false } } })}>
        {children}
      </QueryClientProvider>
    )

    const { result } = renderHook(() => useUserData('123'), { wrapper })

    expect(result.current.isLoading).toBe(true)

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.data?.name).toBe('Alice')
  })
})
```

---

## Playwright : Tests E2E avec les Locators

Playwright favorise les locators accessibles, comme RTL. La différence majeure : Playwright teste le vrai navigateur.

```typescript
// tests/e2e/checkout.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Tunnel de commande', () => {
  test('complète un achat avec succès', async ({ page }) => {
    await page.goto('/products')

    // Locators accessibles — équivalents Playwright de getByRole
    await page.getByRole('button', { name: /ajouter au panier/i }).first().click()
    await page.getByRole('link', { name: /voir le panier/i }).click()

    await expect(page.getByRole('heading', { name: /votre panier/i })).toBeVisible()
    await expect(page.getByText(/1 article/i)).toBeVisible()

    await page.getByRole('button', { name: /commander/i }).click()

    // Formulaire de livraison
    await page.getByLabel(/prénom/i).fill('Alice')
    await page.getByLabel(/nom/i).fill('Martin')
    await page.getByLabel(/adresse email/i).fill('alice@example.com')

    await page.getByRole('button', { name: /passer au paiement/i }).click()

    // Vérifier la confirmation
    await expect(page.getByRole('heading', { name: /commande confirmée/i })).toBeVisible()
    await expect(page.getByText(/numéro de commande/i)).toBeVisible()
  })
})
```

---

## Page Object Model (POM)

Le POM encapsule les sélecteurs et les actions d'une page, rendant les tests plus maintenables.

```typescript
// tests/e2e/pages/LoginPage.ts
import { Page, Locator, expect } from '@playwright/test'

export class LoginPage {
  private readonly emailInput: Locator
  private readonly passwordInput: Locator
  private readonly submitButton: Locator
  private readonly errorMessage: Locator

  constructor(private page: Page) {
    this.emailInput = page.getByLabel(/adresse email/i)
    this.passwordInput = page.getByLabel(/mot de passe/i)
    this.submitButton = page.getByRole('button', { name: /se connecter/i })
    this.errorMessage = page.getByRole('alert')
  }

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message)
  }

  async expectRedirectTo(path: string) {
    await expect(this.page).toHaveURL(new RegExp(path))
  }
}

// Utilisation dans les tests
test('connexion avec identifiants invalides', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.goto()
  await loginPage.login('bad@example.com', 'wrongpassword')
  await loginPage.expectError('Identifiants incorrects')
})
```

---

## Playwright Fixtures Avancées

```typescript
// tests/e2e/fixtures.ts
import { test as base, Page } from '@playwright/test'
import { LoginPage } from './pages/LoginPage'

type Fixtures = {
  authenticatedPage: Page
  adminPage: Page
  loginPage: LoginPage
}

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page)
    await use(loginPage)
  },

  // Fixture de page authentifiée — réutilise le storage state
  authenticatedPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: 'tests/e2e/.auth/user.json',
    })
    const page = await context.newPage()
    await use(page)
    await context.close()
  },

  adminPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: 'tests/e2e/.auth/admin.json',
    })
    const page = await context.newPage()
    await use(page)
    await context.close()
  },
})

// Générer les storage states en global setup
// tests/e2e/globalSetup.ts
export default async function globalSetup() {
  const browser = await chromium.launch()
  const context = await browser.newContext()
  const page = await context.newPage()

  await page.goto('http://localhost:3000/login')
  await page.getByLabel(/email/i).fill('user@example.com')
  await page.getByLabel(/password/i).fill('password')
  await page.getByRole('button', { name: /login/i }).click()

  await context.storageState({ path: 'tests/e2e/.auth/user.json' })
  await browser.close()
}
```

---

## Visual Regression Testing

```typescript
test('le tableau de bord correspond au visuel de référence', async ({ page }) => {
  await page.goto('/dashboard')
  await page.waitForLoadState('networkidle')

  // Screenshot de la page entière
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixelRatio: 0.02, // 2% de différence tolérée
    threshold: 0.1,
  })
})

test('le bouton principal correspond au visuel', async ({ page }) => {
  await page.goto('/components')

  // Screenshot d'un élément spécifique
  const button = page.getByRole('button', { name: /commander maintenant/i })
  await expect(button).toHaveScreenshot('cta-button.png')
})
```

Mettre à jour les screenshots de référence :

```bash
npx playwright test --update-snapshots
```

---

## Tests d'Accessibilité avec @axe-core/playwright

```typescript
import { checkA11y, injectAxe } from 'axe-playwright'

test.describe('Accessibilité', () => {
  test('la page de connexion est accessible', async ({ page }) => {
    await page.goto('/login')
    await injectAxe(page)

    await checkA11y(page, undefined, {
      detailedReport: true,
      detailedReportOptions: {
        html: true,
      },
    })
  })

  test('le formulaire de commande respecte les critères WCAG AA', async ({ page }) => {
    await page.goto('/checkout')
    await injectAxe(page)

    // Vérifier seulement les règles critiques (impact: 'critical' | 'serious')
    await checkA11y(page, '#checkout-form', {
      axeOptions: {
        runOnly: {
          type: 'tag',
          values: ['wcag2a', 'wcag2aa'],
        },
      },
    })
  })
})
```

---

## CI/CD avec Playwright : Sharding et Artifacts

```yaml
# .github/workflows/e2e.yml
name: Tests E2E

on: [push]

jobs:
  e2e:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]  # Diviser en 4 workers parallèles

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4

      - name: Installer les dépendances Playwright
        run: npx playwright install --with-deps chromium

      - name: Lancer les tests E2E (shard ${{ matrix.shard }}/4)
        run: npx playwright test --shard=${{ matrix.shard }}/4
        env:
          BASE_URL: http://localhost:3000

      - name: Upload artifacts (screenshots, traces)
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report-shard-${{ matrix.shard }}
          path: playwright-report/
          retention-days: 7
```

```typescript
// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,       // 2 retries en CI seulement
  workers: process.env.CI ? 1 : undefined, // 1 worker en CI pour la stabilité

  use: {
    trace: 'on-first-retry',       // Trace uniquement si retry
    screenshot: 'only-on-failure', // Screenshot en cas d'échec
    video: 'retain-on-failure',    // Vidéo en cas d'échec
  },

  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
})
```

---

## Storybook Interaction Tests

```typescript
// src/components/LoginForm/LoginForm.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { within, userEvent, expect } from '@storybook/test'
import { LoginForm } from './LoginForm'

const meta: Meta<typeof LoginForm> = {
  component: LoginForm,
  title: 'Forms/LoginForm',
}
export default meta

type Story = StoryObj<typeof LoginForm>

export const FilledAndSubmitted: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)

    // Simuler le remplissage du formulaire
    await userEvent.type(
      canvas.getByLabelText(/adresse email/i),
      'alice@example.com'
    )
    await userEvent.type(
      canvas.getByLabelText(/mot de passe/i),
      'motdepasse123'
    )

    // Vérifier l'état avant soumission
    await expect(canvas.getByRole('button', { name: /se connecter/i })).toBeEnabled()

    // Soumettre
    await userEvent.click(canvas.getByRole('button', { name: /se connecter/i }))

    // Vérifier l'état après soumission
    await expect(canvas.getByRole('progressbar')).toBeVisible()
  },
}

export const ValidationErrors: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)

    // Soumettre sans remplir → affiche les erreurs
    await userEvent.click(canvas.getByRole('button', { name: /se connecter/i }))

    await expect(canvas.getByText(/email requis/i)).toBeVisible()
    await expect(canvas.getByText(/mot de passe requis/i)).toBeVisible()
  },
}
```

---

## Tableau de Décision : Quelle Query Utiliser

| Cas | Query recommandée | Exemple |
|-----|------------------|---------|
| Bouton | `getByRole('button', { name })` | `getByRole('button', { name: /supprimer/i })` |
| Input avec label | `getByLabelText` | `getByLabelText(/email/i)` |
| Input sans label | `getByPlaceholderText` | À éviter — corriger l'accessibilité |
| Texte non interactif | `getByText` | `getByText(/bienvenue/i)` |
| Titre | `getByRole('heading', { level })` | `getByRole('heading', { level: 2 })` |
| Lien | `getByRole('link', { name })` | `getByRole('link', { name: /accueil/i })` |
| Image | `getByAltText` | `getByAltText(/logo de l'entreprise/i)` |
| Composant sans rôle accessible | `getByTestId` | Dernier recours uniquement |
