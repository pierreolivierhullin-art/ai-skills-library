# Optimisation du Bundle — Webpack, Vite et Code Splitting

## Comprendre le Problème du Bundle

Un bundle JavaScript non optimisé est la cause la plus fréquente d'un TTI (Time to Interactive) élevé. Le navigateur doit télécharger, parser, compiler et exécuter l'intégralité du JS avant que l'application soit utilisable. Chaque kilooctet de JS coûte environ 2× plus en temps de traitement qu'un kilooctet d'image : le download est similaire, mais le parsing et l'exécution s'ajoutent.

Objectifs typiques pour une application web moderne :
- Bundle initial (code critique) : < 150 KB gzippé
- Bundle total (toutes chunks) : < 500 KB gzippé
- Aucune dépendance dupliquée
- 0 code mort importé (tree shaking effectif)

---

## Analyse du Bundle — Comprendre Avant d'Optimiser

### webpack-bundle-analyzer

```bash
npm install --save-dev webpack-bundle-analyzer
```

```javascript
// webpack.config.js
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',      // Génère un fichier HTML statique
      reportFilename: 'bundle-report.html',
      openAnalyzer: false,         // Ne pas ouvrir automatiquement (utile en CI)
      generateStatsFile: true,     // Génère stats.json pour d'autres outils
      statsFilename: 'stats.json',
    }),
  ],
};

// Ou via variable d'environnement pour ne pas activer en prod
module.exports = {
  plugins: [
    process.env.ANALYZE && new BundleAnalyzerPlugin(),
  ].filter(Boolean),
};
```

```bash
# Générer le rapport
ANALYZE=true npm run build

# Lire le rapport : ouvrir bundle-report.html dans le navigateur
# Chercher :
# - Rectangles énormes = dépendances lourdes à optimiser
# - Même dépendance présente dans plusieurs chunks = duplication
# - Dossier "node_modules" dominant = opportunité de lazy loading
```

### rollup-plugin-visualizer (Vite)

```bash
npm install --save-dev rollup-plugin-visualizer
```

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    visualizer({
      filename: 'dist/bundle-stats.html',
      open: process.env.ANALYZE === 'true', // Ouvrir auto si ANALYZE=true
      gzipSize: true,    // Afficher la taille gzippée
      brotliSize: true,  // Afficher la taille Brotli
      template: 'treemap', // 'treemap' | 'sunburst' | 'network'
    }),
  ],
});
```

### source-map-explorer — Analyse précise du bundle final

```bash
npm install --save-dev source-map-explorer

# Générer avec source maps
npm run build -- --sourcemap

# Analyser
npx source-map-explorer dist/assets/*.js

# Output : tableau avec chaque module et sa contribution exacte en bytes
# Plus précis que webpack-bundle-analyzer pour du code splitté
```

### Lire un rapport de bundle — méthodologie

```
Rapport bundle : questions à se poser
─────────────────────────────────────
1. Quelle est la taille du chunk initial (entry point) ?
   → Objectif < 150KB gzippé pour le premier JS critique

2. Quelles bibliothèques occupent > 20KB ?
   → Candidats : moment.js, lodash, date-fns complet, antd complet, etc.

3. Y a-t-il des bibliothèques présentes dans plusieurs chunks ?
   → Duplication : configurer splitChunks ou manualChunks

4. Le code applicatif est-il bien séparé du code vendor ?
   → Chunks vendor changent rarement = meilleur cache navigateur

5. Y a-t-il des imports de l'intégralité d'une lib alors qu'on utilise 5% ?
   → moment.js (330KB) quand on a besoin de format() → remplacer par date-fns ciblé
```

---

## Tree Shaking — Principes et Pièges

### Pourquoi le tree shaking fonctionne (ou pas)

Le tree shaking repose sur l'analyse statique des imports/exports ESM. Le bundler peut déterminer à la compilation quels exports ne sont jamais importés et les éliminer.

```javascript
// ✅ ESM : analyse statique possible → tree shaking fonctionne
export function utilisée() { return 42; }
export function nonUtilisée() { return 0; } // Sera éliminée si jamais importée

// ❌ CommonJS : dynamique → tree shaking impossible
module.exports = {
  utilisée: function() { return 42; },
  nonUtilisée: function() { return 0; }, // Toujours incluse même si non importée
};

// ❌ Import CJS d'une lib : pas de tree shaking même avec bundler moderne
const _ = require('lodash'); // 70KB complet, toujours

// ✅ Import ESM ciblé : tree shaking effectif
import { groupBy } from 'lodash-es'; // 2KB seulement
```

### Le champ `sideEffects` dans package.json

```json
// package.json d'une bibliothèque — déclarer les side effects
{
  "name": "ma-bibliothèque",
  "sideEffects": false,
  // false = tous les fichiers sont purs, tree shaking agressif autorisé

  // OU : lister les fichiers avec side effects réels
  "sideEffects": [
    "*.css",           // Les imports CSS ont des effets (injectent des styles)
    "./src/polyfills.js", // Polyfills modifient l'environnement global
    "./src/register.js"   // Enregistre des service workers, etc.
  ]
}
```

```javascript
// Côté consommateur : vérifier que vos imports n'ont pas de side effects cachés

// ❌ Import avec side effect implicite
import 'some-lib/register'; // Enregistre quelque chose globalement → pas tree-shakeable

// ❌ Re-export barrel files peuvent casser le tree shaking
// src/components/index.ts
export { Button } from './Button';
export { Modal } from './Modal';     // Même si non utilisé, bundler peut inclure tout
export { DataTable } from './DataTable';

// ✅ Import direct depuis le fichier source
import { Button } from './components/Button';
// Contourne le barrel file pour un tree shaking parfait
```

### Remplacer les bibliothèques lourdes

```javascript
// ❌ moment.js : 330KB minifié, non tree-shakeable
import moment from 'moment';
const formaté = moment(date).format('DD/MM/YYYY');

// ✅ date-fns : tree-shakeable, ~2KB par fonction
import { format } from 'date-fns';
const formaté = format(date, 'dd/MM/yyyy');

// ✅ Encore mieux pour des cas simples : API native Intl
const formaté = new Intl.DateTimeFormat('fr-FR').format(date);

// ❌ lodash CommonJS : 70KB complet
import _ from 'lodash';
const résultat = _.groupBy(items, 'type');

// ✅ lodash-es : tree-shakeable
import { groupBy, sortBy, uniqBy } from 'lodash-es';

// ✅ Ou fonctions natives ES2015+ (souvent suffisant)
const résultat = Object.groupBy(items, item => item.type); // Chrome 117+, Node 21+

// ❌ axios : 12KB gzippé pour du simple fetch
import axios from 'axios';
const data = await axios.get('/api/users');

// ✅ fetch natif ou ky (3KB) pour les besoins simples
const data = await fetch('/api/users').then(r => r.json());
```

---

## Code Splitting — Stratégies

### Route-based splitting (splitting par route)

Chaque route charge uniquement son propre code. C'est l'optimisation avec le meilleur ratio effort/gain.

```typescript
// React Router v6 avec lazy loading
import { lazy, Suspense } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

// ✅ Chaque route est un chunk séparé
const Accueil = lazy(() => import('./pages/Accueil'));
const Catalogue = lazy(() => import('./pages/Catalogue'));
const ProduitDétail = lazy(() => import('./pages/ProduitDétail'));
const Panier = lazy(() => import('./pages/Panier'));
const Paiement = lazy(() => import('./pages/Paiement'));  // 300KB de libs Stripe
const Compte = lazy(() => import('./pages/Compte'));
const Administration = lazy(() => import('./pages/Administration')); // Jamais chargé pour users normaux

function PageChargement() {
  return <div className="page-skeleton" aria-live="polite">Chargement...</div>;
}

const router = createBrowserRouter([
  { path: '/', element: <Suspense fallback={<PageChargement />}><Accueil /></Suspense> },
  { path: '/catalogue', element: <Suspense fallback={<PageChargement />}><Catalogue /></Suspense> },
  { path: '/produit/:id', element: <Suspense fallback={<PageChargement />}><ProduitDétail /></Suspense> },
  { path: '/panier', element: <Suspense fallback={<PageChargement />}><Panier /></Suspense> },
  { path: '/paiement', element: <Suspense fallback={<PageChargement />}><Paiement /></Suspense> },
  { path: '/compte', element: <Suspense fallback={<PageChargement />}><Compte /></Suspense> },
  { path: '/admin/*', element: <Suspense fallback={<PageChargement />}><Administration /></Suspense> },
]);

export default function App() {
  return <RouterProvider router={router} />;
}
```

### Component-based splitting (splitting par composant)

Pour les composants lourds et conditionnels : modales, éditeurs riches, graphiques, cartes interactives.

```typescript
// ❌ Toujours chargé même si la modale n'est jamais ouverte
import { ModaleÉditeurRiche } from './ModaleÉditeurRiche'; // ~500KB avec TipTap/ProseMirror

// ✅ Chargé seulement quand la modale s'ouvre
const ModaleÉditeurRiche = lazy(() => import('./ModaleÉditeurRiche'));

function PageArticle() {
  const [modaleOuverte, setModaleOuverte] = useState(false);

  return (
    <>
      <button onClick={() => setModaleOuverte(true)}>Éditer l'article</button>

      {modaleOuverte && (
        <Suspense fallback={<div>Chargement de l'éditeur...</div>}>
          <ModaleÉditeurRiche onClose={() => setModaleOuverte(false)} />
        </Suspense>
      )}
    </>
  );
}

// Autres exemples de composants à lazy-loader :
const CarteCesium = lazy(() => import('./CarteCesium'));     // Cesium.js : 3MB
const ÉditeurCode = lazy(() => import('./ÉditeurCode'));     // Monaco Editor : 2MB
const GraphiqueD3 = lazy(() => import('./GraphiqueD3'));      // D3.js : 300KB
const ExporteurPDF = lazy(() => import('./ExporteurPDF'));    // jsPDF + html2canvas : 600KB
```

### Dynamic imports avec preloading

```typescript
// prefetch : charger en arrière-plan pendant l'inactivité (faible priorité)
// Utiliser pour les routes probablement visitées ensuite
function BoutonPanier() {
  const router = useRouter();

  // Précharger la page panier au survol du bouton (avant le clic)
  const préchargerPanier = () => {
    import(/* webpackPrefetch: true */ './pages/Panier');
    // Vite : import('./pages/Panier?prefetch')
  };

  return (
    <button
      onMouseEnter={préchargerPanier}
      onClick={() => router.push('/panier')}
    >
      Voir le panier
    </button>
  );
}

// preload : charger immédiatement à haute priorité
// Utiliser quand on est sûr que la ressource sera nécessaire très bientôt
function ÉtapeCommande({ étape }: { étape: number }) {
  useEffect(() => {
    if (étape === 1) {
      // L'utilisateur est à l'étape 1 → précharger l'étape 2 immédiatement
      import(/* webpackPreload: true */ './ÉtapePaiement');
    }
  }, [étape]);

  return <div>/* ... */</div>;
}

// Preloading programmatique sans dynamic import
function préchargerRoute(chemin: string) {
  const link = document.createElement('link');
  link.rel = 'prefetch';
  link.href = chemin;
  document.head.appendChild(link);
}
```

---

## Configuration Vite — Optimisation Avancée

```typescript
// vite.config.ts — configuration complète d'optimisation
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],

  build: {
    // Taille cible pour les chunks (en bytes)
    chunkSizeWarningLimit: 500, // Avertissement si chunk > 500KB

    rollupOptions: {
      output: {
        // ✅ Stratégie manualChunks : contrôle fin sur les chunks
        manualChunks: (id) => {
          // Chunk séparé pour React et ses dépendances proches
          if (id.includes('node_modules/react') ||
              id.includes('node_modules/react-dom') ||
              id.includes('node_modules/scheduler')) {
            return 'react-vendor';
          }

          // Chunk séparé pour le routeur
          if (id.includes('node_modules/react-router')) {
            return 'router';
          }

          // Chunk séparé pour les utilitaires (lodash-es, date-fns, etc.)
          if (id.includes('node_modules/lodash-es') ||
              id.includes('node_modules/date-fns')) {
            return 'utils';
          }

          // Chunk séparé pour UI components library
          if (id.includes('node_modules/@radix-ui') ||
              id.includes('node_modules/framer-motion')) {
            return 'ui-vendor';
          }

          // Charts séparés car souvent conditionnels
          if (id.includes('node_modules/recharts') ||
              id.includes('node_modules/d3')) {
            return 'charts';
          }
        },

        // Naming pattern pour un cache navigateur optimal
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]',
      },
    },

    // ✅ Tree shaking renforcé
    minify: 'esbuild',
    target: 'es2020', // Syntaxe moderne = bundle plus petit

    // ✅ Source maps en production pour le monitoring d'erreurs (Sentry, etc.)
    sourcemap: process.env.GENERATE_SOURCEMAP === 'true',
  },

  // ✅ Optimisation des dépendances en développement
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom'],
    exclude: ['@vite/client'],
  },
});
```

---

## Configuration Webpack — Optimisation Avancée

```javascript
// webpack.config.js — configuration production optimisée
const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = {
  mode: 'production',

  optimization: {
    // ✅ Tree shaking : déclarer que les modules sont sans side effects
    usedExports: true,
    sideEffects: true, // Respecte le champ sideEffects de package.json

    // ✅ Minification avancée
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true,   // Supprimer les console.log en production
            drop_debugger: true,
            pure_funcs: ['console.info', 'console.debug', 'console.warn'],
          },
          mangle: { safari10: true }, // Compatibilité Safari 10
        },
      }),
      new CssMinimizerPlugin(),
    ],

    // ✅ Stratégie de splitting des chunks
    splitChunks: {
      chunks: 'all', // Optimiser les chunks async ET synchrones
      maxInitialRequests: 30,
      maxAsyncRequests: 30,
      minSize: 20000, // Ne pas créer de chunk < 20KB
      maxSize: 250000, // Tenter de découper les chunks > 250KB

      cacheGroups: {
        // React core : très stable, mis en cache longtemps
        reactVendor: {
          test: /[\\/]node_modules[\\/](react|react-dom|scheduler)[\\/]/,
          name: 'react-vendor',
          priority: 30,
          reuseExistingChunk: true,
        },

        // Vendor générique : toutes les autres dépendances npm
        defaultVendors: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10,
          reuseExistingChunk: true,
        },

        // Code commun entre plusieurs chunks applicatifs
        common: {
          minChunks: 2, // Doit être utilisé dans au moins 2 chunks
          name: 'common',
          priority: 5,
          reuseExistingChunk: true,
          enforce: true,
        },
      },
    },

    // ✅ Runtime chunk séparé pour un meilleur cache
    runtimeChunk: 'single',
  },

  resolve: {
    // ✅ Favoriser les versions ESM des packages pour le tree shaking
    mainFields: ['module', 'browser', 'main'],
  },
};
```

---

## Compression — Brotli vs Gzip

### Comparaison des algorithmes

| Algorithme | Ratio de compression | Vitesse de décompression | Support navigateur |
|------------|---------------------|--------------------------|-------------------|
| **Brotli** | ~15-25% mieux que gzip | Équivalent à gzip | 96% (HTTPS requis) |
| **Gzip** | Référence | Rapide | 100% |
| **zstd** | Similaire à Brotli | Plus rapide | Chrome 118+, en cours |

### Configuration Nginx — compression pré-générée

```nginx
# /etc/nginx/conf.d/compression.conf

# Compression gzip à la volée (fallback)
gzip on;
gzip_vary on;
gzip_comp_level 6;      # 1-9 : 6 est le bon compromis vitesse/ratio
gzip_min_length 1000;   # Ne pas compresser les petits fichiers
gzip_types
  text/plain
  text/css
  text/javascript
  application/javascript
  application/json
  application/xml
  image/svg+xml
  font/woff2;

# Brotli statique : servir des fichiers .br pré-compressés (meilleur ratio)
# Requiert le module ngx_brotli (apt install libnginx-mod-brotli)
brotli on;
brotli_static on;       # Servir les fichiers .br pré-compressés si disponibles
brotli_comp_level 6;
brotli_types
  text/plain
  text/css
  application/javascript
  application/json
  image/svg+xml;
```

```bash
# Script de build : pré-générer les fichiers compressés
#!/bin/bash
# compress-assets.sh — à intégrer dans le pipeline CI/CD

BUILD_DIR="dist"

echo "Génération des fichiers Brotli..."
find "$BUILD_DIR" -type f \( -name "*.js" -o -name "*.css" -o -name "*.html" -o -name "*.svg" \) | \
  while read file; do
    brotli --force --quality=11 "$file" -o "${file}.br"
    echo "  Créé: ${file}.br ($(du -sh "${file}.br" | cut -f1))"
  done

echo "Génération des fichiers Gzip..."
find "$BUILD_DIR" -type f \( -name "*.js" -o -name "*.css" -o -name "*.html" \) | \
  while read file; do
    gzip --force --keep --best "$file"
  done

echo "Compression terminée."
```

### Configuration Cloudflare — compression automatique

```
# Cloudflare Dashboard → Speed → Optimization
# ✅ Brotli : ON (Cloudflare compresse automatiquement en Brotli pour les navigateurs compatibles)
# ✅ Gzip : ON (fallback automatique)

# Cloudflare comprime à la volée — pas besoin de pré-compresser côté serveur
# Mais la compression pré-générée (statique) est plus efficace en temps CPU
```

---

## Polyfills — Optimisation Différentielle

### @babel/preset-env avec targets

```javascript
// babel.config.js
module.exports = {
  presets: [
    ['@babel/preset-env', {
      // ✅ Cibler uniquement les navigateurs qui ont besoin de polyfills
      targets: {
        browsers: [
          '>0.5%',           // Navigateurs avec > 0.5% de parts de marché
          'last 2 versions', // Dernières 2 versions de chaque navigateur
          'not dead',        // Navigateurs maintenus
          'not ie 11',       // Exclure IE11 explicitement
        ],
      },
      useBuiltIns: 'usage', // Ajouter seulement les polyfills utilisés dans le code
      corejs: 3,             // Version de core-js
      modules: false,        // Garder les modules ESM pour le tree shaking
    }],
  ],
};

// ✅ Avec browserslist dans package.json (partagé entre Babel, PostCSS, etc.)
// package.json
{
  "browserslist": {
    "production": [">0.5%", "last 2 versions", "not dead", "not ie 11"],
    "development": ["last 1 chrome version", "last 1 firefox version"]
  }
}
```

### Differential serving — Servir deux bundles

```html
<!-- HTML : servir le bundle moderne aux navigateurs récents, legacy aux anciens -->

<!-- Bundle moderne : ESM, pas de polyfills lourds, plus petit -->
<script type="module" src="/assets/app-modern.js"></script>

<!-- Bundle legacy : CommonJS transpilé, polyfills complets -->
<!-- nomodule : ignoré par les navigateurs qui comprennent "type=module" -->
<script nomodule src="/assets/app-legacy.js"></script>

<!-- Résultat :
  Chrome/Firefox/Safari récents → chargent SEULEMENT app-modern.js (plus petit)
  IE11 / vieux navigateurs → chargent SEULEMENT app-legacy.js
  Les deux scripts ne se chargent JAMAIS simultanément
-->
```

```typescript
// vite.config.ts — générer le bundle legacy avec @vitejs/plugin-legacy
import legacy from '@vitejs/plugin-legacy';

export default defineConfig({
  plugins: [
    legacy({
      targets: ['defaults', 'not IE 11'],
      additionalLegacyPolyfills: ['regenerator-runtime/runtime'],
      modernPolyfills: true, // Polyfills minimalistes pour les navigateurs modernes
    }),
  ],
});
```

---

## Module Federation — Micro-Frontends

```javascript
// webpack.config.js — Host app : consomme les modules distants
const { ModuleFederationPlugin } = require('webpack').container;

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'host',
      remotes: {
        // Déclarer les applications distantes
        checkout: 'checkout@https://checkout.domaine.com/remoteEntry.js',
        catalogue: 'catalogue@https://catalogue.domaine.com/remoteEntry.js',
      },
      shared: {
        // Partager React entre les micro-frontends pour éviter la duplication
        react: { singleton: true, requiredVersion: '^18.0.0' },
        'react-dom': { singleton: true, requiredVersion: '^18.0.0' },
      },
    }),
  ],
};

// webpack.config.js — Remote app (checkout) : expose ses composants
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'checkout',
      filename: 'remoteEntry.js',
      exposes: {
        './Paiement': './src/components/Paiement',
        './Panier': './src/components/Panier',
      },
      shared: {
        react: { singleton: true },
        'react-dom': { singleton: true },
      },
    }),
  ],
};

// Utilisation dans le host : import dynamique du composant distant
const Paiement = lazy(() => import('checkout/Paiement'));
```

---

## Audit et Métriques de Bundle

### Performance budget avec bundlesize

```json
// package.json — définir un budget de bundle
{
  "bundlesize": [
    { "path": "./dist/assets/react-vendor-*.js", "maxSize": "50 kB" },
    { "path": "./dist/assets/index-*.js",         "maxSize": "100 kB" },
    { "path": "./dist/assets/vendors-*.js",       "maxSize": "150 kB" },
    { "path": "./dist/assets/*.css",              "maxSize": "30 kB" }
  ]
}
```

```yaml
# .github/workflows/bundle-check.yml
name: Bundle Size Check
on: [pull_request]
jobs:
  bundle:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - name: Check bundle size
        run: npx bundlesize
      - name: Report bundle stats
        uses: andresz1/size-limit-action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

### Détecter les dépendances dupliquées

```bash
# npm : détecter les packages en double
npm dedupe --dry-run

# Analyser les duplicates avec duplicate-package-checker-webpack-plugin
npm install --save-dev duplicate-package-checker-webpack-plugin
```

```javascript
// webpack.config.js
const DuplicatePackageCheckerPlugin = require('duplicate-package-checker-webpack-plugin');

module.exports = {
  plugins: [
    new DuplicatePackageCheckerPlugin({
      verbose: true,    // Montrer quels packages importent les duplicates
      strict: true,     // Échouer le build si des duplicates sont trouvées
    }),
  ],
};
```

---

## Récapitulatif — Gains Typiques par Optimisation

| Optimisation | Réduction bundle typique | Complexité |
|---|---|---|
| Code splitting par route | -40 à -70% du bundle initial | Faible |
| Lazy loading composants lourds | -10 à -30% selon les cas | Faible |
| Remplacement moment.js → date-fns | -300KB (-120KB gzippé) | Faible |
| Remplacement lodash → lodash-es | -50KB gzippé | Très faible |
| Tree shaking activé | -10 à -20% variable | Moyen |
| Compression Brotli vs Gzip | -15 à -25% | Faible (infra) |
| Differential serving | -20 à -30% pour les navigateurs modernes | Moyen |
| Module federation (si micro-frontend) | Partage des dépendances communes | Élevé |
