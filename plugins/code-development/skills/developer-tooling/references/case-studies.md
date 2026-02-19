# Études de Cas — Developer Tooling en Production

## Cas 1 — Migration vers Monorepo (Startup, 12 développeurs, 4 repos séparés)

### Contexte

Une startup SaaS avec 12 développeurs répartis sur 4 dépôts distincts : `web` (Next.js), `api` (Fastify), `mobile` (React Native), et `shared` (types et utilitaires). La synchronisation des types partagés était manuelle — chaque équipe maintenait sa propre définition du type `User`.

### Problèmes identifiés

- Le type `User` existait en 4 versions légèrement différentes : `userId` dans l'API, `id` dans le frontend, `user_id` dans le mobile
- Les PR qui touchaient l'interface entre les services cassaient silencieusement les autres dépôts
- L'onboarding d'un nouveau développeur prenait 2 jours (cloner 4 repos, configurer les env vars, comprendre les versions Node compatibles)
- Chaque repo avait son propre CI : 4 × 12 minutes = 48 minutes de compute à chaque modification partagée

### Solution — Migration Turborepo + pnpm workspaces

#### Phase 1 : Créer le monorepo (sans toucher au code)

```bash
# Créer la structure initiale
mkdir company-monorepo && cd company-monorepo
pnpm init

# Importer les 4 repos comme sous-dossiers
git subtree add --prefix=apps/web https://github.com/company/web.git main
git subtree add --prefix=apps/api https://github.com/company/api.git main
git subtree add --prefix=apps/mobile https://github.com/company/mobile.git main
git subtree add --prefix=packages/shared https://github.com/company/shared.git main
```

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
```

```json
// package.json (racine)
{
  "name": "company-monorepo",
  "private": true,
  "scripts": {
    "dev": "turbo run dev --parallel",
    "build": "turbo run build",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "type-check": "turbo run type-check"
  },
  "devDependencies": {
    "turbo": "^2.0.0"
  }
}
```

#### Phase 2 : Extraire le package de types partagés

```
packages/
  types/
    src/
      user.ts
      auth.ts
      billing.ts
    package.json
    tsconfig.json
  utils/
    src/
      date.ts
      validation.ts
    package.json
```

```typescript
// packages/types/src/user.ts — source unique de vérité
export interface User {
  id: string;                    // Anciennement userId / user_id
  email: string;
  displayName: string;
  role: "admin" | "member" | "viewer";
  createdAt: Date;
  updatedAt: Date;
}

export interface UserProfile extends User {
  avatarUrl?: string;
  bio?: string;
  preferences: UserPreferences;
}

export interface UserPreferences {
  theme: "light" | "dark" | "system";
  language: "fr" | "en";
  notifications: {
    email: boolean;
    push: boolean;
    slack: boolean;
  };
}
```

```json
// packages/types/package.json
{
  "name": "@company/types",
  "version": "1.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": "./src/index.ts"
  }
}
```

```json
// apps/web/package.json — consommation du type partagé
{
  "dependencies": {
    "@company/types": "workspace:*"
  }
}
```

#### Phase 3 : CI unifié avec remote caching

```json
// turbo.json
{
  "$schema": "https://turborepo.org/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["src/**", "tsconfig.json", "package.json"],
      "outputs": [".next/**", "dist/**", "!.next/cache/**"]
    },
    "test": {
      "dependsOn": ["^build"],
      "inputs": ["src/**", "test/**", "vitest.config.ts"],
      "outputs": ["coverage/**"]
    },
    "type-check": {
      "dependsOn": ["^build"],
      "inputs": ["src/**", "tsconfig.json"],
      "outputs": []
    },
    "lint": {
      "inputs": ["src/**", ".eslintrc.js"],
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - uses: pnpm/action-setup@v3
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - run: pnpm install --frozen-lockfile

      - name: Build, test et lint
        run: pnpm turbo run build test lint type-check
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

### Résultats mesurés

| Métrique                        | Avant              | Après              | Amélioration    |
|---------------------------------|--------------------|--------------------|-----------------|
| Durée CI totale                 | 4 × 12min = 48min  | 8min (avec cache)  | 6× plus rapide  |
| Durée CI (cache froid)          | 48min              | 22min              | 2.2×            |
| Onboarding nouveau développeur  | 2 jours            | 2 heures           | 8×              |
| Désynchronisations de types     | 3-4 par semaine    | 0                  | Éliminé         |
| Coût mensuel GitHub Actions     | ~$180              | ~$45               | -75%            |

### Leçon clé

La migration vers un monorepo se fait impérativement en 3 phases distinctes. Tout faire en une seule PR est une erreur fréquente qui crée un diff illisible, bloque les reviews, et multiplie les risques de régression. La phase 1 ne touche pas au code applicatif — elle change seulement la structure. La phase 2 extrait les packages sans modifier leur API. La phase 3 unifie le CI.

---

## Cas 2 — Build 8min → 45s avec Turborepo (Agence Web)

### Contexte

Une agence web avec un monorepo Next.js contenant 3 applications clients, un Storybook partagé, et 3 packages internes (`ui`, `utils`, `config`). Chaque PR déclenchait un build complet de tout le monorepo, que les changements concernent un composant ou un fichier de configuration.

### Problème — Build séquentiel sans cache

```json
// turbo.json AVANT — configuration naïve sans inputs/outputs précis
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"]
    },
    "storybook:build": {
      "dependsOn": ["^build"]
    }
  }
}
```

Avec cette configuration, Turborepo ne peut pas déterminer précisément quand le cache est invalide. Il rebuilde tout si n'importe quel fichier change — y compris les fichiers de test, les READMEs, ou les fichiers de configuration non utilisés au build.

### Solution — Inputs et outputs précis

```json
// turbo.json APRÈS — hashing précis par task
{
  "$schema": "https://turborepo.org/schema.json",
  "globalEnv": ["CI", "NODE_ENV"],
  "globalDependencies": ["tsconfig.base.json", ".nvmrc"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": [
        "src/**/*.{ts,tsx,js,jsx}",
        "public/**",
        "next.config.ts",
        "tailwind.config.ts",
        "postcss.config.js",
        "tsconfig.json",
        "package.json"
      ],
      "outputs": [
        ".next/**",
        "dist/**",
        "!.next/cache/**"
      ],
      "env": ["NEXT_PUBLIC_API_URL", "NEXT_PUBLIC_ANALYTICS_KEY"]
    },
    "test": {
      "dependsOn": ["^build"],
      "inputs": [
        "src/**/*.{ts,tsx}",
        "**/*.test.{ts,tsx}",
        "**/*.spec.{ts,tsx}",
        "vitest.config.ts",
        "vitest.setup.ts"
      ],
      "outputs": ["coverage/**"]
    },
    "storybook:build": {
      "dependsOn": ["^build"],
      "inputs": [
        "src/**/*.{ts,tsx}",
        "**/*.stories.{ts,tsx}",
        ".storybook/**",
        "tsconfig.json"
      ],
      "outputs": ["storybook-static/**"]
    },
    "lint": {
      "inputs": [
        "src/**/*.{ts,tsx,js}",
        ".eslintrc.js",
        ".eslintignore"
      ],
      "outputs": []
    }
  }
}
```

### GitHub Actions avec TURBO_TOKEN

```yaml
# .github/workflows/pr.yml
name: Pull Request

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  build-test:
    name: Build & Test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - name: Setup pnpm
        uses: pnpm/action-setup@v3
        with:
          version: 9

      - name: Setup Node.js 20
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - name: Installer les dépendances
        run: pnpm install --frozen-lockfile

      - name: Build, Test, Lint (avec cache Turbo)
        run: pnpm turbo run build test lint storybook:build
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ vars.TURBO_TEAM }}
          NEXT_PUBLIC_API_URL: ${{ vars.STAGING_API_URL }}

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./apps/*/coverage/lcov.info,./packages/*/coverage/lcov.info
```

### Graphe de dépendances du monorepo

```
apps/client-a  ──┐
apps/client-b  ──┤──► packages/ui ──┐
apps/client-c  ──┘                  ├──► packages/utils
                                    └──► packages/config
storybook      ────────────────────►packages/ui
```

Grâce aux `inputs` précis, changer un test dans `apps/client-a` n'invalide pas le cache de `apps/client-b` ou du Storybook. Avant : toute modification invalidait tout. Après : seuls les packages réellement affectés sont reconstruits.

### Résultats mesurés

| Scénario                              | Avant    | Après    | Amélioration |
|---------------------------------------|----------|----------|--------------|
| Build complet (cache froid)           | 8min     | 4min 30s | 1.8×         |
| PR sur un composant UI                | 8min     | 45s      | 10.7×        |
| PR sur la config (non-UI)             | 8min     | 15s      | 32×          |
| Cache hit rate (après 1 semaine)      | 0%       | 82%      | +82pts       |
| Coût compute CI mensuel               | $320     | $32      | -90%         |

### Leçon clé

Définir les `inputs` avec précision est le levier le plus impactant de Turborepo. Utiliser `"**"` (pattern générique) comme input revient à ne pas avoir de cache du tout, car tout changement de fichier invalide le hash. Lister explicitement les fichiers qui influencent réellement l'output de chaque tâche — et exclure les tests du build, les fixtures des lints, etc. — multiplie le taux de cache hit par 5 à 10.

---

## Cas 3 — CLI Interne Équipe (Fintech, 20 développeurs)

### Contexte

Une fintech avec 20 développeurs créait des micro-services Fastify + Prisma + Vitest. Chaque nouveau service nécessitait la création manuelle de ~20 fichiers selon des conventions non documentées. Les services étaient souvent incomplets (certains sans migrations DB, d'autres sans tests d'intégration).

### Problèmes identifiés

- 2 heures de setup par nouveau micro-service (et souvent plus pour les développeurs juniors)
- Inconsistance dans la structure : 40% des services manquaient de tests d'intégration, 25% n'avaient pas de healthcheck
- Documentation générée à la main et souvent obsolète dès la première semaine
- Standards de code définis dans un Confluence que personne ne lisait

### Solution — CLI `company-cli` avec Commander + Ink + Plop

#### Architecture du CLI

```
company-cli/
  src/
    cli/
      index.ts              ← Commander setup
      commands/
        generate-service.ts
        run-migration.ts
        validate-service.ts
      ui/
        ServiceGenerator.tsx ← Ink components
        ProgressBar.tsx
    templates/
      service/              ← Templates Plop
        src/
          index.ts.hbs
          server.ts.hbs
          routes/
            health.ts.hbs
        prisma/
          schema.prisma.hbs
        docker-compose.yml.hbs
        Dockerfile.hbs
        README.md.hbs
    plopfile.ts
  package.json
  tsconfig.json
```

#### Commander setup avec sous-commandes

```typescript
// src/cli/index.ts
import { Command } from "commander";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pkg = JSON.parse(
  readFileSync(path.join(__dirname, "../../package.json"), "utf-8")
);

const program = new Command();

program
  .name("company-cli")
  .description("CLI interne — génération de services et utilitaires")
  .version(pkg.version)
  .hook("preAction", async () => {
    // Vérifier les mises à jour disponibles
    const { checkForUpdates } = await import("./update-checker.js");
    await checkForUpdates(pkg.version);
  });

// Sous-commande : generate
const generate = program.command("generate").alias("g")
  .description("Générer du code à partir de templates");

generate
  .command("service <name>")
  .description("Créer un nouveau micro-service complet")
  .option("-p, --port <number>", "Port HTTP du service", "3000")
  .option("--no-docker", "Omettre la configuration Docker")
  .option("--no-tests", "Omettre les tests (déconseillé)")
  .option("-d, --database <type>", "Type de BDD", "postgres")
  .action(async (name, options) => {
    const { render } = await import("ink");
    const React = (await import("react")).default;
    const { ServiceGenerator } = await import("./ui/ServiceGenerator.js");

    render(
      React.createElement(ServiceGenerator, {
        serviceName: name,
        options,
        onComplete: (success: boolean) => {
          process.exit(success ? 0 : 1);
        },
      })
    );
  });

// Sous-commande : validate
program
  .command("validate [service-path]")
  .description("Valider qu'un service respecte les standards de l'équipe")
  .option("--fix", "Corriger automatiquement les problèmes mineurs")
  .action(async (servicePath, options) => {
    const { validateService } = await import("./commands/validate-service.js");
    const targetPath = servicePath ?? process.cwd();
    const result = await validateService(targetPath, options);

    if (!result.valid) {
      console.error(`\nNon-conformités trouvées: ${result.errors.length}`);
      result.errors.forEach((e) => console.error(`  ✗ ${e}`));
      process.exit(1);
    }

    console.log("\n✓ Service conforme aux standards");
  });

// Sous-commande : migration
program
  .command("migrate <migration-name>")
  .description("Créer et appliquer une migration Prisma")
  .option("--env <environment>", "Environnement cible", "development")
  .action(async (migrationName, options) => {
    const { runMigration } = await import("./commands/run-migration.js");
    await runMigration(migrationName, options);
  });

program.parseAsync(process.argv).catch((err) => {
  console.error("\x1b[31mErreur:\x1b[0m", err.message);
  if (process.env.DEBUG) console.error(err.stack);
  process.exit(1);
});
```

#### Template Plop pour un micro-service

```typescript
// src/plopfile.ts
import type { NodePlopAPI } from "plop";

export default function (plop: NodePlopAPI) {
  plop.setHelper("upperFirst", (str: string) =>
    str.charAt(0).toUpperCase() + str.slice(1)
  );

  plop.setGenerator("service", {
    description: "Micro-service Fastify complet",
    prompts: [], // Les prompts viennent de Commander
    actions: (data) => [
      // Structure de base
      {
        type: "addMany",
        destination: "{{kebabCase name}}",
        templateFiles: "../templates/service/**",
        base: "../templates/service",
        data,
      },
      // README généré avec la date et la version Node
      {
        type: "add",
        path: "{{kebabCase name}}/README.md",
        templateFile: "../templates/README.md.hbs",
        data: { ...data, date: new Date().toISOString().split("T")[0] },
      },
    ],
  });
}
```

```handlebars
{{! templates/service/src/index.ts.hbs }}
import Fastify from "fastify";
import { registerRoutes } from "./routes/index.js";
import { logger } from "./lib/logger.js";

const PORT = parseInt(process.env.PORT ?? "{{port}}", 10);
const HOST = process.env.HOST ?? "0.0.0.0";

const server = Fastify({
  logger: {
    level: process.env.LOG_LEVEL ?? "info",
    serializers: {
      req: (req) => ({ method: req.method, url: req.url }),
    },
  },
});

await registerRoutes(server);

try {
  await server.listen({ port: PORT, host: HOST });
  logger.info({ port: PORT }, "{{upperFirst name}} service démarré");
} catch (err) {
  server.log.error(err);
  process.exit(1);
}
```

### Résultats mesurés

| Métrique                            | Avant     | Après    | Amélioration |
|-------------------------------------|-----------|----------|--------------|
| Temps de création d'un service      | 2 heures  | 8 minutes | 15×         |
| Conformité aux standards (mesurée)  | 60%       | 100%     | +40pts       |
| Documentation présente au J+7       | 30%       | 100%     | +70pts       |
| Tests d'intégration présents        | 55%       | 100%     | +45pts       |
| Satisfaction développeurs (NPS)     | +12       | +58      | +46pts       |

### Leçon clé

Un CLI interne est un investissement à ROI immédiat. 8 minutes sauvées par service × 2 services par semaine × 20 développeurs = des centaines d'heures par an. Au-delà du temps, le vrai bénéfice est la conformité automatique aux standards — il est plus facile de suivre les conventions quand le générateur les applique que de lire un document de 40 pages.

---

## Cas 4 — CI/CD Unifié pour Monorepo (Scale-up, 40 développeurs)

### Contexte

Une scale-up SaaS avec 40 développeurs et 12 services dans un monorepo Nx. L'équipe avait migré vers Nx il y a 6 mois mais continuait à construire et tester tous les services à chaque PR, sans utiliser les commandes `affected`. Le CI prenait 45 minutes et bloquait les merges.

### Problèmes identifiés

- CI de 45 minutes sur chaque PR, même pour un changement de README
- File d'attente de 8-10 PR en attente de CI simultanément
- Développeurs qui rebranch sur `main` pendant l'attente, créant des conflits
- Coût GitHub Actions : $2,400/mois pour 40 développeurs
- Moral de l'équipe affecté par les longs cycles de feedback

### Solution — Nx Affected + Matrix Strategy + pnpm Store Cache

#### Workflow GitHub Actions avec `nx affected`

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main, develop]

jobs:
  # Job 1 : calculer les projets affectés
  setup:
    runs-on: ubuntu-latest
    outputs:
      affected-apps: ${{ steps.affected.outputs.apps }}
      affected-libs: ${{ steps.affected.outputs.libs }}
      has-affected: ${{ steps.affected.outputs.has-affected }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Nécessaire pour comparer avec main

      - uses: pnpm/action-setup@v3
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - name: Get pnpm store directory
        run: echo "STORE_PATH=$(pnpm store path --silent)" >> $GITHUB_ENV

      - uses: actions/cache@v4
        with:
          path: ${{ env.STORE_PATH }}
          key: ${{ runner.os }}-pnpm-${{ hashFiles('**/pnpm-lock.yaml') }}
          restore-keys: ${{ runner.os }}-pnpm-

      - run: pnpm install --frozen-lockfile

      - name: Calculer les projets affectés
        id: affected
        run: |
          BASE="origin/${{ github.base_ref }}"

          # Obtenir les apps affectées
          APPS=$(npx nx print-affected --target=build --base=$BASE \
            --select=tasks.target.project --type=app 2>/dev/null \
            | tr ',' '\n' | grep -v '^$' | jq -R . | jq -sc . || echo "[]")

          # Obtenir les libs affectées
          LIBS=$(npx nx print-affected --target=test --base=$BASE \
            --select=tasks.target.project --type=lib 2>/dev/null \
            | tr ',' '\n' | grep -v '^$' | jq -R . | jq -sc . || echo "[]")

          HAS_AFFECTED=$([ "$APPS" = "[]" ] && [ "$LIBS" = "[]" ] && echo "false" || echo "true")

          echo "apps=$APPS" >> $GITHUB_OUTPUT
          echo "libs=$LIBS" >> $GITHUB_OUTPUT
          echo "has-affected=$HAS_AFFECTED" >> $GITHUB_OUTPUT

          echo "Apps affectées: $APPS"
          echo "Libs affectées: $LIBS"

  # Job 2 : Tester les libs en parallèle
  test-libs:
    needs: setup
    if: needs.setup.outputs.has-affected == 'true' && needs.setup.outputs.affected-libs != '[]'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        project: ${{ fromJson(needs.setup.outputs.affected-libs) }}
      fail-fast: false
      max-parallel: 6
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - name: Restore pnpm store
        uses: actions/cache@v4
        with:
          path: ${{ needs.setup.outputs.store-path }}
          key: ${{ runner.os }}-pnpm-${{ hashFiles('**/pnpm-lock.yaml') }}
      - run: pnpm install --frozen-lockfile
      - name: Test ${{ matrix.project }}
        run: npx nx test ${{ matrix.project }} --coverage --ci
        env:
          NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        if: always()
        with:
          flags: ${{ matrix.project }}

  # Job 3 : Build et test des apps en parallèle
  test-apps:
    needs: setup
    if: needs.setup.outputs.has-affected == 'true' && needs.setup.outputs.affected-apps != '[]'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        project: ${{ fromJson(needs.setup.outputs.affected-apps) }}
      fail-fast: false
      max-parallel: 4
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - name: Build ${{ matrix.project }}
        run: npx nx build ${{ matrix.project }}
        env:
          NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}
      - name: Test ${{ matrix.project }}
        run: npx nx test ${{ matrix.project }} --coverage --ci
        env:
          NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}

  # Job 4 : Gate final (obligatoire pour le merge)
  ci-complete:
    needs: [test-libs, test-apps]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Vérifier le statut global
        run: |
          if [ "${{ needs.test-libs.result }}" = "failure" ] || \
             [ "${{ needs.test-apps.result }}" = "failure" ]; then
            echo "CI échoué"
            exit 1
          fi
          echo "CI réussi"
```

#### Configuration Nx Cloud pour le cache distribué

```json
// nx.json
{
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "nxCloudAccessToken": "${NX_CLOUD_ACCESS_TOKEN}",
  "parallel": 4,
  "cacheDirectory": ".nx/cache",
  "targetDefaults": {
    "build": {
      "cache": true,
      "dependsOn": ["^build"],
      "inputs": ["production", "^production"]
    },
    "test": {
      "cache": true,
      "inputs": [
        "default",
        "^production",
        "{workspaceRoot}/jest.preset.js",
        "{workspaceRoot}/vitest.workspace.ts"
      ]
    },
    "lint": {
      "cache": true,
      "inputs": [
        "default",
        "{workspaceRoot}/.eslintrc.json",
        "{workspaceRoot}/.eslintignore"
      ]
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*", "sharedGlobals"],
    "production": [
      "default",
      "!{projectRoot}/**/?(*.)+(spec|test).[jt]s?(x)",
      "!{projectRoot}/src/test-setup.[jt]s",
      "!{projectRoot}/.eslintrc.json",
      "!{projectRoot}/README.md"
    ],
    "sharedGlobals": [
      "{workspaceRoot}/tsconfig.base.json",
      "{workspaceRoot}/.env.test"
    ]
  }
}
```

### Distribution du temps de CI après optimisation

```
PR sur une lib isolée:
├── setup (calculer affected)    : 90s
├── test-libs (1 lib, parallèle) : 3min
└── ci-complete                  : 10s
Total: ~5min                     (vs 45min avant)

PR sur une app:
├── setup                        : 90s
├── test-libs (dépendances)      : 4min (parallèle)
├── test-apps (1 app)            : 6min
└── ci-complete                  : 10s
Total: ~8min                     (vs 45min avant)

PR transversale (refactoring):
├── setup                        : 90s
├── test-libs (8 libs, parallèle): 8min
├── test-apps (4 apps, parallèle): 10min
└── ci-complete                  : 10s
Total: ~22min                    (vs 45min avant)
```

### Résultats mesurés

| Métrique                              | Avant     | Après (P50) | Après (P99)  |
|---------------------------------------|-----------|-------------|--------------|
| Durée CI par PR                       | 45min     | 8min        | 22min        |
| PR bloquées dans la file              | 8-10      | 1-2         | 4            |
| Coût GitHub Actions mensuel           | $2,400    | $840        | —            |
| Délai moyen de feedback               | 52min     | 11min       | —            |
| Satisfaction développeurs (NPS)       | -5        | +42         | —            |
| Incidents de régression post-merge    | 3/mois    | 0.5/mois    | —            |

### Analyse du coût

```
Avant:
  - 40 développeurs × 5 PR/jour = 200 PR/jour
  - 200 × 45min = 9,000 min-runner/jour
  - GitHub Actions: 9,000min × $0.008 = $72/jour = $2,160/mois

Après:
  - 200 PR/jour × 8min moyen = 1,600 min-runner/jour
  - GitHub Actions: 1,600min × $0.008 = $12.8/jour = $384/mois
  - Nx Cloud: $300/mois (10 contributors plan)
  - Total: $684/mois (-65%)
```

### Leçon clé

La combinaison `nx affected` + remote cache est le duo incontournable pour scaler le CI d'un monorepo. `affected` garantit que seuls les packages réellement impactés par un changement sont traités. Le remote cache s'assure que les résultats déjà calculés (même par un autre développeur sur la même branche) ne sont pas recalculés. Ensemble, ils réduisent le CI de 45 minutes à moins de 10 minutes pour 80% des PR — et c'est cette proportion, pas le cas extrême, qui détermine la vélocité d'une équipe.

---

## Synthèse — Patterns Communs aux 4 Cas

| Pattern                         | Cas 1 | Cas 2 | Cas 3 | Cas 4 |
|---------------------------------|-------|-------|-------|-------|
| Migration progressive (phases)  | ✓     | —     | —     | —     |
| Remote caching                  | ✓     | ✓     | —     | ✓     |
| Inputs/outputs précis           | ✓     | ✓     | —     | ✓     |
| Parallelisation CI              | ✓     | —     | —     | ✓     |
| Affected commands               | —     | —     | —     | ✓     |
| CLI interne pour les standards  | —     | —     | ✓     | —     |
| Source unique de vérité (types) | ✓     | —     | —     | —     |
| Feedback loop < 10min           | ✓     | ✓     | ✓     | ✓     |

Le fil conducteur : **réduire le temps entre "écrire du code" et "avoir un feedback"**. Que ce soit via un cache de build, un CLI qui génère du code conforme, ou un CI qui ne teste que ce qui a changé, chaque optimisation vise à réduire la friction cognitive et le temps d'attente qui fragmentent le flow des développeurs.
