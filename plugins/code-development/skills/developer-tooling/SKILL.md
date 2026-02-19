---
name: developer-tooling
version: 1.0.0
description: >
  Monorepo Turborepo Nx pnpm workspaces, build tools Vite esbuild Rollup tsup,
  code generation Plop Hygen scaffolding, CLI tools Node.js Commander Ink,
  developer experience automation, changesets versioning publishing,
  pre-commit hooks husky lint-staged, dotfiles zsh configuration,
  terminal productivity tmux, module federation, workspace optimization,
  tool configuration ESLint Prettier Biome, dependency management
---

# Developer Tooling — Productivité et Outillage Développeur

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu mets en place un monorepo et dois choisir entre Turborepo et Nx
- Les builds deviennent trop lents et tu veux optimiser avec du caching ou du parallélisme
- Tu veux standardiser la création de fichiers avec des générateurs de code
- Tu construis un outil CLI pour ton équipe ou tes utilisateurs
- Tu veux mettre en place des hooks de pre-commit pour garantir la qualité du code
- Tu gères le versioning et la publication de packages dans un monorepo

---

## Monorepo avec Turborepo

```bash
# Créer un monorepo Turborepo
npx create-turbo@latest mon-projet --package-manager pnpm
```

```json
// turbo.json — Configuration du pipeline
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],    // Attendre que les dépendances soient buildées d'abord
      "outputs": [".next/**", "!.next/cache/**", "dist/**"],
      "cache": true
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "cache": true
    },
    "lint": {
      "outputs": [],
      "cache": true
    },
    "dev": {
      "cache": false,
      "persistent": true           // Processus longue durée (dev server)
    },
    "type-check": {
      "dependsOn": ["^build"],
      "outputs": [],
      "cache": true
    }
  }
}
```

```
# Structure d'un monorepo Turborepo
mon-projet/
├── apps/
│   ├── web/           # Next.js
│   ├── api/           # Fastify
│   └── admin/         # Next.js
├── packages/
│   ├── ui/            # Composants partagés
│   ├── config-eslint/ # Config ESLint partagée
│   ├── config-ts/     # tsconfig de base
│   └── utils/         # Utilitaires communs
├── pnpm-workspace.yaml
├── turbo.json
└── package.json
```

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

### Package partagé bien configuré

```json
// packages/utils/package.json
{
  "name": "@mon-projet/utils",
  "version": "0.0.0",
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "dev": "tsup src/index.ts --format cjs,esm --dts --watch"
  }
}
```

```typescript
// packages/utils/tsup.config.ts
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['cjs', 'esm'],
  dts: true,
  clean: true,
  sourcemap: true,
  treeshake: true,
});
```

---

## Nx — Pour les Grands Monorepos

```bash
npx create-nx-workspace@latest mon-espace --preset=ts
```

```json
// nx.json
{
  "targetDefaults": {
    "build": {
      "cache": true,
      "dependsOn": ["^build"]
    },
    "test": { "cache": true },
    "lint": { "cache": true }
  },
  "affected": {
    "defaultBase": "main"  // Calculer les packages affectés depuis main
  }
}
```

```bash
# Nx : ne tester que les packages affectés par les changements
npx nx affected --target=test

# Visualiser le graphe de dépendances
npx nx graph
```

---

## Build Tools — Vite, esbuild, Rollup

### Vite — Library Mode

```typescript
// vite.config.ts (pour une librairie)
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import dts from 'vite-plugin-dts';
import { resolve } from 'path';

export default defineConfig({
  plugins: [
    react(),
    dts({ include: ['src'], rollupTypes: true }),
  ],
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: 'MaLibrairie',
      formats: ['es', 'cjs'],
      fileName: (format) => `index.${format === 'es' ? 'mjs' : 'cjs'}`,
    },
    rollupOptions: {
      // Externaliser React et React-DOM
      external: ['react', 'react-dom', 'react/jsx-runtime'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
    minify: 'esbuild',
    sourcemap: true,
  },
});
```

### esbuild — Build Ultra-Rapide

```typescript
// build.ts
import * as esbuild from 'esbuild';

await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  platform: 'node',
  target: 'node18',
  format: 'esm',
  outfile: 'dist/index.mjs',
  external: ['better-sqlite3'],  // Ne pas bundler les native modules
  minify: process.env.NODE_ENV === 'production',
  sourcemap: true,
  define: {
    'process.env.VERSION': JSON.stringify(process.env.npm_package_version),
  },
});
```

---

## Hooks Pre-Commit avec Husky + lint-staged

```bash
npm install --save-dev husky lint-staged
npx husky init
```

```bash
# .husky/pre-commit
#!/bin/sh
npx lint-staged
```

```bash
# .husky/commit-msg
#!/bin/sh
npx --no -- commitlint --edit "$1"
```

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ],
    "*.{ts,tsx,js,jsx}": [
      "vitest related --run"  // Tests liés aux fichiers modifiés
    ]
  }
}
```

---

## Code Generation avec Plop

```javascript
// plopfile.js
export default function (plop) {
  // Générateur de composants React
  plop.setGenerator('component', {
    description: 'Créer un composant React',
    prompts: [
      { type: 'input', name: 'nom', message: 'Nom du composant :' },
      { type: 'list', name: 'type', message: 'Type :', choices: ['ui', 'feature', 'layout'] },
    ],
    actions: [
      {
        type: 'add',
        path: 'src/components/{{type}}/{{pascalCase nom}}/index.tsx',
        templateFile: 'plop-templates/component.hbs',
      },
      {
        type: 'add',
        path: 'src/components/{{type}}/{{pascalCase nom}}/{{pascalCase nom}}.test.tsx',
        templateFile: 'plop-templates/component.test.hbs',
      },
      {
        type: 'add',
        path: 'src/components/{{type}}/{{pascalCase nom}}/{{pascalCase nom}}.stories.tsx',
        templateFile: 'plop-templates/component.stories.hbs',
      },
    ],
  });
}
```

```handlebars
{{! plop-templates/component.hbs }}
import { type FC } from 'react';

interface {{pascalCase nom}}Props {
  className?: string;
}

export const {{pascalCase nom}}: FC<{{pascalCase nom}}Props> = ({ className }) => {
  return (
    <div className={className}>
      {{pascalCase nom}}
    </div>
  );
};

{{pascalCase nom}}.displayName = '{{pascalCase nom}}';
```

---

## CLI avec Commander + Ink

```typescript
// src/cli.ts
import { Command } from 'commander';
import { render } from 'ink';
import React from 'react';

const program = new Command();

program
  .name('mon-cli')
  .description('Outil CLI pour l\'équipe')
  .version('1.0.0');

program
  .command('generer <type>')
  .description('Générer des fichiers')
  .option('-n, --nom <nom>', 'Nom de l\'élément')
  .option('--seche', 'Mode test sans écriture de fichiers')
  .action(async (type, options) => {
    // Utiliser Ink pour une UI interactive dans le terminal
    const { waitUntilExit } = render(
      React.createElement(GenerateurUI, { type, options }),
    );
    await waitUntilExit();
  });

program.parse();
```

---

## Changesets — Versioning dans un Monorepo

```bash
npm install --save-dev @changesets/cli
npx changeset init
```

```bash
# Workflow quotidien
# 1. Après chaque PR : créer un changeset
npx changeset
# → Demande : quels packages changent ? patch/minor/major ? Description ?

# 2. En CI : vérifier qu'un changeset existe
npx changeset status --since=origin/main

# 3. Pour une release : bumper les versions et publier
npx changeset version   # Mise à jour des versions et CHANGELOG
npx changeset publish   # npm publish pour chaque package modifié
```

```json
// .changeset/config.json
{
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "linked": [],
  "access": "restricted",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": ["@mon-projet/eslint-config", "@mon-projet/tsconfig"]
}
```

---

## ESLint + Biome — Linting Moderne

```typescript
// eslint.config.mjs (flat config)
import js from '@eslint/js';
import ts from 'typescript-eslint';
import react from 'eslint-plugin-react-hooks';
import importPlugin from 'eslint-plugin-import';

export default ts.config(
  js.configs.recommended,
  ...ts.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      'react-hooks': react,
      import: importPlugin,
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-floating-promises': 'error',
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      'import/order': ['error', { 'newlines-between': 'always' }],
    },
  },
  {
    ignores: ['dist/**', '.next/**', 'node_modules/**'],
  },
);
```

---

## Références

- `references/monorepo.md` — Turborepo avancé (remote caching, Vercel), Nx plugins, workspace protocols, changesets avancé
- `references/build-tools.md` — Vite plugins, Rollup config, esbuild plugins, Webpack 5 Module Federation
- `references/dx-automation.md` — Plop templates avancés, Hygen, Yeoman, scaffolding CLI, dotfiles zsh/fish, terminal tmux/wezterm
- `references/case-studies.md` — 4 cas : migration vers monorepo, build 8min→45s avec Turborepo, CLI interne équipe, CI/CD unifié
