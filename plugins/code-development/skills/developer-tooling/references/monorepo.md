# Monorepo Avancé — Turborepo, Nx et Gestion des Packages

## Turborepo Remote Caching

Le remote cache est le différenciateur principal de Turborepo en CI. Sans lui, chaque runner reconstruit tout depuis zéro.

### Vercel Remote Cache (gratuit)

```bash
# Authentification via le CLI Vercel
npx turbo login
npx turbo link

# Variables d'environnement pour CI
TURBO_TOKEN=your_vercel_token
TURBO_TEAM=your_team_slug
```

```json
// turbo.json — activation du remote cache
{
  "$schema": "https://turborepo.org/schema.json",
  "remoteCache": {
    "enabled": true,
    "signature": true
  },
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**", "!.next/cache/**"]
    }
  }
}
```

### Self-hosted avec MinIO ou S3

Pour les équipes qui ne veulent pas dépendre de Vercel, un backend S3-compatible suffit.

```bash
# MinIO en local ou sur un serveur dédié
docker run -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD=password123 \
  minio/minio server /data --console-address ":9001"
```

```bash
# Variables pour pointer vers le cache self-hosted
TURBO_API=http://your-cache-server.internal:3000
TURBO_TOKEN=your_secret_token
TURBO_TEAM=myteam

# Utiliser turbo-remote-cache (package npm)
npx turbo-remote-cache --port 3000 \
  --storage-provider s3 \
  --storage-path my-turbo-cache-bucket
```

Le package `turbo-remote-cache` implémente l'API Turborepo et supporte S3, GCS, Azure Blob, et le système de fichiers local. Idéal pour les entreprises avec des contraintes réseau.

## Turborepo Tasks Avancées — Inputs, Outputs et Hashing

### Définir des inputs explicites

Par défaut, Turborepo hashe tous les fichiers du package pour déterminer si le cache est valide. Préciser les `inputs` améliore drastiquement le taux de cache hit.

```json
{
  "tasks": {
    "test": {
      "dependsOn": ["^build"],
      "inputs": [
        "src/**/*.ts",
        "src/**/*.tsx",
        "test/**/*.ts",
        "vitest.config.ts",
        "tsconfig.json"
      ],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "inputs": [
        "src/**/*.{ts,tsx}",
        ".eslintrc.js",
        ".eslintignore"
      ],
      "outputs": []
    },
    "build": {
      "dependsOn": ["^build"],
      "inputs": [
        "src/**",
        "public/**",
        "next.config.ts",
        "tailwind.config.ts",
        "tsconfig.json"
      ],
      "outputs": [".next/**", "dist/**", "!.next/cache/**"]
    }
  }
}
```

### Variables d'environnement dans le hash

```json
{
  "globalEnv": ["NODE_ENV", "CI"],
  "globalDependencies": [".env.production", "tsconfig.base.json"],
  "tasks": {
    "build": {
      "env": ["NEXT_PUBLIC_API_URL", "NEXT_PUBLIC_STRIPE_KEY"],
      "dependsOn": ["^build"],
      "outputs": [".next/**"]
    }
  }
}
```

`globalEnv` affecte tous les tasks. `env` au niveau d'un task n'affecte que ce task. Si `NEXT_PUBLIC_API_URL` change entre staging et production, le cache sera différent — comportement correct.

## Nx Computation Caching et Affected Commands

### Nx Cloud et le cache distribué

```bash
# Initialisation Nx Cloud
npx nx connect

# nx.json avec Nx Cloud
```

```json
{
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "nxCloudAccessToken": "your_token_here",
  "targetDefaults": {
    "build": {
      "cache": true,
      "dependsOn": ["^build"],
      "inputs": ["production", "^production"]
    },
    "test": {
      "cache": true,
      "inputs": ["default", "^production", "{workspaceRoot}/jest.preset.js"]
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*", "sharedGlobals"],
    "production": [
      "default",
      "!{projectRoot}/**/?(*.)+(spec|test).[jt]s?(x)",
      "!{projectRoot}/src/test-setup.[jt]s"
    ],
    "sharedGlobals": ["{workspaceRoot}/tsconfig.base.json"]
  }
}
```

### Affected commands — ne traiter que ce qui a changé

```bash
# Tester uniquement les projets affectés par les changements
nx affected --target=test

# Build des projets affectés depuis main
nx affected --target=build --base=main --head=HEAD

# Affected avec parallelisation
nx affected --target=test --parallel=4

# Visualiser le project graph
nx graph

# Voir ce qui est affecté sans exécuter
nx print-affected --target=build --base=main
```

### Project Graph API

```typescript
// Exploiter le graphe programmatiquement
import { createProjectGraphAsync } from "@nx/devkit";

async function analyzeGraph() {
  const graph = await createProjectGraphAsync();

  // Tous les projets
  const projects = Object.keys(graph.nodes);

  // Dépendances d'un projet
  const deps = graph.dependencies["my-app"];
  console.log(
    "Dépendances directes:",
    deps.map((d) => d.target)
  );

  // Trouver les projets qui dépendent de shared-ui
  const dependents = Object.entries(graph.dependencies)
    .filter(([, deps]) => deps.some((d) => d.target === "shared-ui"))
    .map(([project]) => project);

  console.log("Projets dépendant de shared-ui:", dependents);
}
```

## Nx Plugins et Génération de Code

### Plugins officiels et génération

```bash
# Ajouter un plugin Next.js
nx add @nx/next

# Générer une application
nx g @nx/next:application my-app --directory=apps/my-app

# Générer un composant React
nx g @nx/react:component Button --project=shared-ui --export

# Générer une bibliothèque partagée
nx g @nx/js:library utils --directory=libs/utils --bundler=tsc
```

### Exécuteur custom Nx

```typescript
// libs/nx-plugins/src/executors/docker-build/executor.ts
import { ExecutorContext, runExecutor } from "@nx/devkit";
import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

interface DockerBuildSchema {
  imageName: string;
  tag: string;
  dockerfile?: string;
  buildArgs?: Record<string, string>;
}

export default async function dockerBuildExecutor(
  options: DockerBuildSchema,
  context: ExecutorContext
): Promise<{ success: boolean }> {
  const projectRoot =
    context.workspace.projects[context.projectName!].root;
  const dockerfile = options.dockerfile ?? "Dockerfile";
  const args = Object.entries(options.buildArgs ?? {})
    .map(([k, v]) => `--build-arg ${k}=${v}`)
    .join(" ");

  const cmd = `docker build -t ${options.imageName}:${options.tag} ${args} -f ${projectRoot}/${dockerfile} ${projectRoot}`;

  console.log(`Exécution: ${cmd}`);

  try {
    const { stdout, stderr } = await execAsync(cmd);
    if (stdout) console.log(stdout);
    if (stderr) console.error(stderr);
    return { success: true };
  } catch (error) {
    console.error("Erreur lors du build Docker:", error);
    return { success: false };
  }
}
```

## pnpm Workspace Protocols

### Différences entre les protocoles

| Protocole     | Signification                                | Usage recommandé                         |
|---------------|----------------------------------------------|------------------------------------------|
| `workspace:*` | Utilise toujours la version workspace locale | Packages internes — version exacte       |
| `workspace:^` | Résout en `^version` lors de la publication  | Packages internes publiés sur npm        |
| `workspace:~` | Résout en `~version` lors de la publication  | Packages avec patches fréquents          |

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
  - "libs/*"
```

```json
// apps/web/package.json
{
  "dependencies": {
    "@company/ui": "workspace:*",
    "@company/utils": "workspace:*",
    "@company/config": "workspace:^"
  }
}
```

Lors du `pnpm publish`, `workspace:*` est remplacé par la version exacte actuelle (`1.2.3`), `workspace:^` devient `^1.2.3`.

### Optimiser les node_modules avec pnpm

```yaml
# .npmrc
shamefully-hoist=false
strict-peer-dependencies=false
auto-install-peers=true

# Hisser uniquement certains packages (nécessaire pour certains outils legacy)
public-hoist-pattern[]=*prettier*
public-hoist-pattern[]=*eslint*
public-hoist-pattern[]=@types/*
```

```bash
# Comparer les temps d'installation
time pnpm install --frozen-lockfile          # ~15s avec cache
time npm ci                                  # ~90s avec cache
time yarn install --frozen-lockfile          # ~60s avec cache

# Analyser l'espace disque
pnpm store status
pnpm store prune  # Nettoyer les packages non utilisés
```

## Versioning des Packages — Changesets

### Independent vs Fixed mode

**Fixed mode** : tous les packages ont la même version. Simple, adapté aux frameworks monolithiques (Angular, React core).

**Independent mode** : chaque package a sa propre version. Plus flexible, adapté aux bibliothèques utilitaires avec des cycles de release différents.

```json
// .changeset/config.json
{
  "$schema": "https://unpkg.com/@changesets/config@2.3.1/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "fixed": [],
  "linked": [["@company/ui", "@company/ui-react", "@company/ui-vue"]],
  "access": "restricted",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": ["@company/docs", "@company/examples"]
}
```

### Workflows automatisés avec GitHub Actions

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches:
      - main

concurrency: ${{ github.workflow }}-${{ github.ref }}

jobs:
  release:
    name: Release
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup pnpm
        uses: pnpm/action-setup@v3
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Create Release PR or Publish
        uses: changesets/action@v1
        with:
          publish: pnpm run release
          version: pnpm run version
          commit: "chore: version packages"
          title: "chore: version packages"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

```json
// package.json (racine)
{
  "scripts": {
    "version": "changeset version",
    "release": "turbo run build --filter=./packages/* && changeset publish"
  }
}
```

### Snapshot releases pour les pre-releases

```bash
# Créer un changeset
pnpm changeset

# Entrer en mode pre-release (pour une feature branch)
pnpm changeset pre enter next

# Créer une snapshot release (sans modifier les versions officielles)
pnpm changeset version --snapshot next
pnpm changeset publish --tag next

# Sortir du mode pre-release
pnpm changeset pre exit
```

## Module Boundaries avec Nx

### Configuration des règles de frontière

```javascript
// .eslintrc.js
module.exports = {
  root: true,
  plugins: ["@nx"],
  overrides: [
    {
      files: ["*.ts", "*.tsx"],
      rules: {
        "@nx/enforce-module-boundaries": [
          "error",
          {
            enforceBuildableLibDependency: true,
            allow: [],
            depConstraints: [
              {
                sourceTag: "scope:app",
                onlyDependOnLibsWithTags: ["scope:shared", "scope:feature", "type:ui"],
              },
              {
                sourceTag: "scope:feature",
                onlyDependOnLibsWithTags: ["scope:shared", "type:ui", "type:util"],
              },
              {
                sourceTag: "scope:shared",
                onlyDependOnLibsWithTags: ["scope:shared", "type:util"],
              },
              {
                sourceTag: "type:ui",
                onlyDependOnLibsWithTags: ["type:util", "type:model"],
              },
              {
                sourceTag: "type:util",
                onlyDependOnLibsWithTags: ["type:util", "type:model"],
              },
            ],
          },
        ],
      },
    },
  ],
};
```

```json
// project.json (exemple pour un package)
{
  "name": "shared-ui",
  "tags": ["scope:shared", "type:ui"]
}
```

## Testing dans un Monorepo

### Partage de configuration Vitest

```typescript
// vitest.workspace.ts (racine)
import { defineWorkspace } from "vitest/config";

export default defineWorkspace([
  "packages/*/vitest.config.ts",
  "apps/*/vitest.config.ts",
]);
```

```typescript
// vitest.config.base.ts (configuration partagée)
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov", "html"],
      thresholds: {
        lines: 80,
        branches: 75,
        functions: 80,
        statements: 80,
      },
    },
    reporters: process.env.CI ? ["junit", "verbose"] : ["verbose"],
    outputFile: {
      junit: "./test-results/junit.xml",
    },
  },
});
```

```typescript
// packages/my-lib/vitest.config.ts
import { mergeConfig } from "vitest/config";
import baseConfig from "../../vitest.config.base";

export default mergeConfig(baseConfig, {
  test: {
    include: ["src/**/*.test.ts"],
  },
});
```

### Test affected uniquement

```bash
# Nx : tester seulement les packages affectés
nx affected --target=test --base=origin/main

# Turborepo : filter sur les packages modifiés
turbo run test --filter=...[origin/main]

# Turbo avec filtre combiné
turbo run test --filter=...[origin/main] --filter=!docs
```

## CI/CD pour les Monorepos

### Matrix strategy GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  # Étape 1 : calculer les packages affectés
  compute-affected:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: pnpm/action-setup@v3
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - run: pnpm install --frozen-lockfile

      - id: set-matrix
        run: |
          AFFECTED=$(npx nx print-affected --target=test --base=origin/main --select=tasks.target.project | tr ',' '\n' | jq -R . | jq -sc .)
          echo "matrix={\"project\":$AFFECTED}" >> $GITHUB_OUTPUT

  # Étape 2 : exécuter en parallèle
  test:
    needs: compute-affected
    runs-on: ubuntu-latest
    strategy:
      matrix: ${{ fromJson(needs.compute-affected.outputs.matrix) }}
      fail-fast: false
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: npx nx test ${{ matrix.project }} --coverage
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

### Cache des node_modules avec pnpm

```yaml
- name: Get pnpm store directory
  shell: bash
  run: echo "STORE_PATH=$(pnpm store path --silent)" >> $GITHUB_ENV

- name: Cache pnpm store
  uses: actions/cache@v4
  with:
    path: ${{ env.STORE_PATH }}
    key: ${{ runner.os }}-pnpm-store-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      ${{ runner.os }}-pnpm-store-

- run: pnpm install --frozen-lockfile
```

## Checklist — Santé d'un Monorepo

| Critère                             | Outil              | Commande de vérification              |
|-------------------------------------|--------------------|---------------------------------------|
| Cycles de dépendances               | Nx / Madge         | `nx graph` puis vérification visuelle |
| Module boundaries respectées        | ESLint + Nx        | `nx lint --all`                       |
| Types partagés synchronisés         | TypeScript         | `tsc --noEmit -p tsconfig.base.json`  |
| Cache hit rate > 70%                | Turborepo          | Dashboard Vercel Remote Cache         |
| Packages affected correctement      | Nx affected        | `nx print-affected`                   |
| Versions lockfile à jour            | pnpm               | `pnpm install --frozen-lockfile`      |
| Changesets cohérents                | Changesets         | `pnpm changeset status`               |
