# Build Tools — Vite, esbuild, Rollup et Webpack 5

## Vite Dev Server — Architecture HMR

Le dev server de Vite repose sur deux mécanismes distincts : le pre-bundling des dépendances (via esbuild) et le HMR natif (via les ES modules du navigateur).

### Pre-bundling avec esbuild

```bash
# Forcer le re-bundling des dépendances
vite --force

# Inspecter le cache de pre-bundling
ls node_modules/.vite/deps/
```

```typescript
// vite.config.ts — configuration avancée du pre-bundling
import { defineConfig } from "vite";

export default defineConfig({
  optimizeDeps: {
    // Forcer l'inclusion dans le pre-bundle (dépendances non-ESM)
    include: ["lodash-es", "date-fns", "@company/ui"],
    // Exclure du pre-bundle (si déjà ESM natif)
    exclude: ["@vueuse/core"],
    // Options passées à esbuild pendant le pre-bundling
    esbuildOptions: {
      target: "es2020",
      plugins: [
        {
          name: "fix-cjs-imports",
          setup(build) {
            build.onLoad({ filter: /\.cjs$/ }, async (args) => {
              const contents = await import("fs").then((fs) =>
                fs.promises.readFile(args.path, "utf8")
              );
              return { contents, loader: "js" };
            });
          },
        },
      ],
    },
  },
  server: {
    // HMR avec WebSocket sécurisé (proxy nginx)
    hmr: {
      protocol: "wss",
      host: "dev.myapp.local",
      port: 443,
      clientPort: 443,
    },
    // Mode SSR dev
    middlewareMode: false,
  },
});
```

### SSR dev mode avec Vite

```typescript
// server.ts — Vite en mode middleware pour SSR
import express from "express";
import { createServer as createViteServer } from "vite";

async function createServer() {
  const app = express();

  const vite = await createViteServer({
    server: { middlewareMode: true },
    appType: "custom",
  });

  app.use(vite.middlewares);

  app.use("*", async (req, res, next) => {
    try {
      const url = req.originalUrl;
      const template = await vite.transformIndexHtml(
        url,
        `<html><head></head><body><div id="app"></div></body></html>`
      );
      const { render } = await vite.ssrLoadModule("/src/entry-server.ts");
      const html = await render(url);
      res.status(200).set({ "Content-Type": "text/html" }).end(
        template.replace(`<div id="app"></div>`, `<div id="app">${html}</div>`)
      );
    } catch (e) {
      vite.ssrFixStacktrace(e as Error);
      next(e);
    }
  });

  app.listen(5173, () => console.log("Serveur SSR sur http://localhost:5173"));
}

createServer();
```

## Vite Plugins Avancés

### Plugin d'inspection (`vite-plugin-inspect`)

```bash
pnpm add -D vite-plugin-inspect
```

```typescript
import Inspect from "vite-plugin-inspect";

export default defineConfig({
  plugins: [
    Inspect({
      build: true,
      outputDir: ".vite-inspect",
    }),
  ],
});
// Accessible sur http://localhost:5173/__inspect/
```

### Écrire un plugin Vite custom

```typescript
// plugins/vite-plugin-env-validator.ts
import type { Plugin, ResolvedConfig } from "vite";

interface EnvValidatorOptions {
  required: string[];
  warnOnly?: boolean;
}

export function envValidator(options: EnvValidatorOptions): Plugin {
  let config: ResolvedConfig;

  return {
    name: "vite-plugin-env-validator",
    // Accès à la config résolue
    configResolved(resolvedConfig) {
      config = resolvedConfig;
    },
    // Transformer le HTML d'entrée
    transformIndexHtml(html) {
      if (config.mode === "development") {
        return html.replace(
          "</head>",
          `<script>console.log("ENV:", import.meta.env)</script></head>`
        );
      }
      return html;
    },
    // Transformer les fichiers source
    transform(code, id) {
      if (!id.endsWith(".ts") && !id.endsWith(".tsx")) return;
      // Vérifier que les variables d'env obligatoires sont définies
      for (const key of options.required) {
        if (!process.env[key] && config.mode === "production") {
          const msg = `Variable d'environnement manquante: ${key}`;
          if (options.warnOnly) {
            console.warn(`[env-validator] ${msg}`);
          } else {
            this.error(msg);
          }
        }
      }
      return null; // pas de transformation du code
    },
    // Étendre le dev server
    configureServer(server) {
      server.middlewares.use("/api/env-check", (_req, res) => {
        const missing = options.required.filter((k) => !process.env[k]);
        res.writeHead(missing.length ? 500 : 200, {
          "Content-Type": "application/json",
        });
        res.end(JSON.stringify({ ok: missing.length === 0, missing }));
      });
    },
  };
}
```

## esbuild API Programmatique

### `transform` vs `build`

```typescript
import * as esbuild from "esbuild";

// transform : traite un seul fichier en mémoire (pas d'I/O)
const result = await esbuild.transform(`
  const greet = (name: string) => \`Hello, \${name}!\`;
  export default greet;
`, {
  loader: "ts",
  target: "es2018",
  minify: true,
  sourcemap: true,
});
console.log(result.code);

// build : entrée/sortie fichiers, bundling complet
const ctx = await esbuild.context({
  entryPoints: ["src/index.ts"],
  bundle: true,
  outdir: "dist",
  platform: "node",
  target: "node20",
  external: ["express", "prisma"],
  define: {
    "process.env.NODE_ENV": JSON.stringify(process.env.NODE_ENV ?? "production"),
  },
  metafile: true,
});

// Watch mode
await ctx.watch();
console.log("Watching...");

// Analyser le metafile
const { text } = await esbuild.analyzeMetafile(ctx.metafile!, {
  verbose: true,
});
console.log(text);

await ctx.dispose();
```

### Plugins esbuild (onLoad, onResolve, onEnd)

```typescript
import * as esbuild from "esbuild";

const svgPlugin: esbuild.Plugin = {
  name: "svg-as-react",
  setup(build) {
    // Intercepter la résolution des imports .svg?react
    build.onResolve({ filter: /\.svg\?react$/ }, (args) => ({
      path: args.path.replace("?react", ""),
      namespace: "svg-react",
    }));

    // Transformer le SVG en composant React
    build.onLoad({ filter: /.*/, namespace: "svg-react" }, async (args) => {
      const fs = await import("fs/promises");
      const svgContent = await fs.readFile(args.path, "utf8");
      const componentName = args.path
        .split("/")
        .pop()!
        .replace(".svg", "")
        .replace(/-([a-z])/g, (_, c: string) => c.toUpperCase());

      return {
        contents: `
          import React from 'react';
          export default function ${componentName}(props) {
            return ${svgContent.replace("<svg", "<svg {...props}")};
          }
        `,
        loader: "jsx",
      };
    });

    // Post-processing après le build
    build.onEnd((result) => {
      if (result.errors.length === 0) {
        console.log(`Build réussi: ${Object.keys(result.metafile?.outputs ?? {}).length} fichiers générés`);
      }
    });
  },
};

await esbuild.build({
  entryPoints: ["src/index.tsx"],
  bundle: true,
  outdir: "dist",
  plugins: [svgPlugin],
  metafile: true,
});
```

## Rollup Config Avancée

### Code splitting manuel avec `manualChunks`

```typescript
// rollup.config.ts
import { defineConfig } from "rollup";
import typescript from "@rollup/plugin-typescript";
import { nodeResolve } from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import { visualizer } from "rollup-plugin-visualizer";

export default defineConfig({
  input: {
    index: "src/index.ts",
    cli: "src/cli.ts",
  },
  output: {
    dir: "dist",
    format: "esm",
    chunkFileNames: "chunks/[name]-[hash].js",
    // Séparation manuelle des chunks
    manualChunks(id) {
      if (id.includes("node_modules")) {
        // Regrouper les dépendances par famille
        if (id.includes("@aws-sdk")) return "vendor-aws";
        if (id.includes("zod") || id.includes("valibot")) return "vendor-validation";
        if (id.includes("react")) return "vendor-react";
        return "vendor"; // tout le reste ensemble
      }
    },
  },
  plugins: [
    nodeResolve({ preferBuiltins: true }),
    commonjs(),
    typescript({ tsconfig: "./tsconfig.build.json" }),
    visualizer({
      filename: "dist/bundle-stats.html",
      gzipSize: true,
      brotliSize: true,
      open: process.env.CI !== "true",
    }),
  ],
});
```

### Virtual modules Rollup

```typescript
// Plugin de virtual module pour injecter la version
const versionPlugin = {
  name: "virtual-version",
  resolveId(id: string) {
    if (id === "virtual:version") return id;
    return null;
  },
  load(id: string) {
    if (id === "virtual:version") {
      const pkg = require("./package.json");
      return `export const VERSION = "${pkg.version}"; export const BUILD_DATE = "${new Date().toISOString()}";`;
    }
    return null;
  },
};

// Utilisation dans le code source
// import { VERSION } from "virtual:version";
```

## Webpack 5 Module Federation

### Configuration avancée avec singleton et version requirements

```javascript
// webpack.config.js — Application shell (host)
const { ModuleFederationPlugin } = require("webpack").container;

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: "shell",
      remotes: {
        // Remote statique
        "auth-app": "authApp@https://auth.mycompany.com/remoteEntry.js",
        // Remote dynamique (défini au runtime)
        "feature-flags": "featureFlags@[featureFlagsUrl]/remoteEntry.js",
      },
      shared: {
        react: {
          singleton: true,      // Une seule instance React (obligatoire)
          requiredVersion: "^18.2.0",
          eager: true,          // Charger sans attendre les async chunks
        },
        "react-dom": {
          singleton: true,
          requiredVersion: "^18.2.0",
          eager: true,
        },
        "@company/design-system": {
          singleton: true,
          requiredVersion: "^2.0.0",
        },
      },
    }),
  ],
};
```

```javascript
// webpack.config.js — Micro-frontend (remote)
new ModuleFederationPlugin({
  name: "authApp",
  filename: "remoteEntry.js",
  exposes: {
    "./LoginPage": "./src/pages/LoginPage",
    "./AuthProvider": "./src/context/AuthProvider",
    "./useAuth": "./src/hooks/useAuth",
  },
  shared: {
    react: { singleton: true, requiredVersion: "^18.2.0" },
    "react-dom": { singleton: true, requiredVersion: "^18.2.0" },
  },
});
```

```typescript
// Chargement dynamique d'un remote au runtime
async function loadRemote(scope: string, module: string) {
  // Initialiser le scope partagé
  await __webpack_init_sharing__("default");

  const container = (window as any)[scope];
  await container.init(__webpack_share_scopes__.default);

  const factory = await container.get(module);
  return factory();
}

// Utilisation
const { LoginPage } = await loadRemote("authApp", "./LoginPage");
```

## Comparaison Build Tools 2025

| Outil       | Dev server | Build prod | Config      | Ecosystem  | Module Federation |
|-------------|------------|------------|-------------|------------|-------------------|
| Vite 5      | ~50ms      | Via Rollup | Simple      | Excellent  | Plugin tiers      |
| Turbopack   | ~10ms      | Beta       | Intégré Next| Next.js    | Non               |
| Rspack      | ~100ms     | Très rapide| Compatible WP| Croissant | Oui (native)      |
| Parcel 2    | ~200ms     | Rapide     | Zéro config | Moyen      | Partiel           |
| Webpack 5   | ~3000ms    | Lent       | Complexe    | Très riche | Natif             |
| esbuild     | Via plugin | Ultra-rapide| API bas-niveau| Minimal | Non               |

## Source Maps — Sécurité et Upload

```typescript
// vite.config.ts — source maps par environnement
export default defineConfig(({ mode }) => ({
  build: {
    sourcemap: mode === "production"
      ? "hidden"   // source maps générées mais non référencées (pour Sentry)
      : "inline",  // inline pour le développement
  },
}));
```

```javascript
// webpack.config.js — types de source maps
module.exports = {
  devtool: process.env.NODE_ENV === "production"
    ? "nosources-source-map"  // aucun code source dans les source maps (privacy)
    : "cheap-module-source-map", // dev : rapide, lignes seulement
};
```

```bash
# Upload des source maps vers Sentry après le build
npx @sentry/cli sourcemaps upload \
  --org my-org \
  --project my-project \
  --url-prefix "~/static/js" \
  ./dist/static/js

# Supprimer les source maps du serveur après upload
find dist -name "*.map" -delete
```

## Tree Shaking Avancé

### sideEffects et annotations `/*#__PURE__*/`

```json
// package.json — déclarer les fichiers sans side effects
{
  "name": "@company/utils",
  "sideEffects": [
    "*.css",
    "dist/polyfills.js"
  ]
}
```

```typescript
// Annotations pour les expressions pures (utilisées par Rollup/Webpack)
export const createLogger = /*#__PURE__*/ (name: string) => ({
  info: (msg: string) => console.log(`[${name}] ${msg}`),
  error: (msg: string) => console.error(`[${name}] ${msg}`),
});

// ANTI-PATTERN : barrel files qui cassent le tree shaking
// ❌ libs/ui/index.ts
export * from "./Button";
export * from "./Modal";
export * from "./Table"; // importé même si inutilisé

// ✓ Préférer les imports directs
import { Button } from "@company/ui/Button";
```

```bash
# Profiler les barrel files avec `vite-bundle-analyzer`
npx vite-bundle-analyzer dist/stats.json

# Ou avec `source-map-explorer`
npx source-map-explorer dist/*.js --html dist/treemap.html
```

## Bundle Analysis avec Budgets

### `size-limit` — alertes sur régression

```json
// package.json
{
  "scripts": {
    "size": "size-limit",
    "analyze": "size-limit --why"
  },
  "size-limit": [
    {
      "name": "SDK core",
      "path": "dist/index.esm.js",
      "limit": "10 KB",
      "import": "{ createClient }"
    },
    {
      "name": "Full bundle",
      "path": "dist/index.esm.js",
      "limit": "25 KB"
    }
  ]
}
```

```yaml
# .github/workflows/bundle-size.yml
- name: Check bundle size
  run: pnpm run size
  # Échoue si le bundle dépasse les limites définies
```

```bash
# bundlesize — alternative simple
npx bundlesize --config bundlesize.config.json
```

```json
// bundlesize.config.json
{
  "files": [
    { "path": "dist/main.*.js", "maxSize": "100 kB" },
    { "path": "dist/vendor.*.js", "maxSize": "200 kB" },
    { "path": "dist/*.css", "maxSize": "30 kB" }
  ]
}
```

## Compilation TypeScript — Performances Comparées

```bash
# tsc natif — vérification de types uniquement (no emit)
time tsc --noEmit                  # ~8s sur 50K lignes

# ts-node — exécution directe (lent, charge tout)
time ts-node src/index.ts          # ~3s de démarrage

# tsx — basé sur esbuild, sans vérification de types
time tsx src/index.ts              # ~200ms de démarrage

# ts-node avec transpileOnly (sans type checking)
time ts-node --transpileOnly src/index.ts  # ~500ms

# esbuild seul — le plus rapide
time esbuild src/index.ts --bundle --platform=node --outfile=dist/index.js  # ~50ms
```

```json
// tsconfig.json — optimisations pour la compilation incrémentale
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": ".tsbuildinfo",
    "composite": true,       // Nécessaire pour les project references
    "skipLibCheck": true,    // Éviter de re-vérifier les .d.ts des node_modules
    "isolatedModules": true  // Compatible avec esbuild/swc (pas de const enum)
  }
}
```

## Compilation Conditionnelle

```typescript
// Variables remplacées à la compilation par le bundler
if (import.meta.env.DEV) {
  console.log("Mode développement — débogage activé");
  // Ce bloc est éliminé en production (dead code elimination)
}

// Équivalent avec process.env (Webpack/esbuild)
if (process.env.NODE_ENV !== "production") {
  performExpensiveValidation(data);
}

// Feature flags compilés (éliminés si false)
declare const __FEATURE_NEW_DASHBOARD__: boolean;
if (__FEATURE_NEW_DASHBOARD__) {
  // Ce code n'est pas inclus dans le bundle si le flag est false
  registerModule(NewDashboard);
}
```

```typescript
// vite.config.ts — define pour les feature flags
export default defineConfig({
  define: {
    __DEV__: JSON.stringify(process.env.NODE_ENV !== "production"),
    __FEATURE_NEW_DASHBOARD__: JSON.stringify(process.env.FEATURE_NEW_DASHBOARD === "true"),
    __VERSION__: JSON.stringify(process.env.npm_package_version),
  },
});
```

Le compilateur élimine automatiquement les branches mortes : `if (false) { ... }` n'est jamais inclus dans le bundle final, ce qui réduit la taille sans aucun effort à l'exécution.
