---
name: web-performance
version: 1.0.0
description: >
  Optimise web performance, Core Web Vitals, Lighthouse score, bundle optimization,
  lazy loading, caching strategies, CDN, reduce Time to First Byte, improve LCP FID CLS,
  speed up website application loading, frontend performance, render blocking resources,
  image optimization, code splitting, tree shaking, performance budget
---

# Web Performance — Core Web Vitals et Optimisation

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Les métriques Lighthouse sont en dessous de 90 (Performance)
- Les Core Web Vitals sont en rouge ou orange dans Search Console
- Le bundle JS dépasse 500 KB (parsed)
- Le LCP (Largest Contentful Paint) dépasse 2,5 secondes
- Les utilisateurs se plaignent de lenteur ou le bounce rate est élevé
- Tu veux améliorer le SEO (Core Web Vitals = facteur de ranking Google)

---

## Core Web Vitals — Les 3 Métriques Clés

### LCP — Largest Contentful Paint

**Définition** : temps de rendu du plus grand élément visible (image hero, titre H1, vidéo).

**Seuils** :
- ✅ Bon : < 2,5 secondes
- ⚠️ À améliorer : 2,5–4 secondes
- ❌ Mauvais : > 4 secondes

**Causes principales** :
```
LCP lent → identifier la cause :
├── Ressource bloquante (CSS, JS en <head>)
├── Server response time (TTFB > 600ms)
├── Image non-optimisée (format, taille, pas de preload)
└── Client-side rendering (CSR sans SSR)
```

**Optimisations LCP** :
```html
<!-- 1. Preload l'image LCP -->
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">

<!-- 2. Images responsive avec srcset -->
<img
  src="/hero-800.webp"
  srcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1200.webp 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  loading="eager"
  fetchpriority="high"
  alt="Hero image"
>

<!-- 3. Éviter le lazy loading sur l'image LCP -->
<!-- Ne pas mettre loading="lazy" sur l'image hero -->
```

### CLS — Cumulative Layout Shift

**Définition** : mesure l'instabilité visuelle (éléments qui bougent pendant le chargement).

**Seuils** :
- ✅ Bon : < 0,1
- ⚠️ À améliorer : 0,1–0,25
- ❌ Mauvais : > 0,25

**Causes et fixes** :
```css
/* 1. Toujours définir width/height sur les images */
img {
  width: 100%;
  height: auto;
  aspect-ratio: 16 / 9; /* Réserve l'espace avant chargement */
}

/* 2. Réserver l'espace pour les publicités/iframes */
.ad-container {
  min-height: 250px; /* Hauteur de l'annonce attendue */
}

/* 3. Polices web : éviter le FOUT */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: optional; /* Pas de layout shift : fallback si police lente */
}
```

### INP — Interaction to Next Paint (remplace FID depuis mars 2024)

**Définition** : délai de réponse à toutes les interactions utilisateur (clics, saisies).

**Seuils** :
- ✅ Bon : < 200ms
- ⚠️ À améliorer : 200–500ms
- ❌ Mauvais : > 500ms

**Optimiser INP** :
```javascript
// Problème : long task bloque le main thread
function traitementLourd(données) {
  // 500ms de traitement → freeze l'interface
  for (const item of données) { /* heavy work */ }
}

// Solution 1 : scheduler.yield() (Chrome 115+)
async function traitementOptimisé(données) {
  for (let i = 0; i < données.length; i++) {
    if (i % 100 === 0) await scheduler.yield(); // Libérer le thread toutes les 100 items
    /* traitement item */
  }
}

// Solution 2 : Web Worker pour les calculs intensifs
const worker = new Worker('/workers/calcul.js');
worker.postMessage({ données });
worker.onmessage = ({ data }) => { /* résultat */ };
```

---

## Mesurer les Performances

### Lighthouse en CI/CD

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [push, pull_request]
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci && npm run build
      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

```json
// lighthouserc.json
{
  "ci": {
    "collect": {
      "startServerCommand": "npm run start",
      "url": ["http://localhost:3000", "http://localhost:3000/produits"]
    },
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.9}],
        "largest-contentful-paint": ["error", {"maxNumericValue": 2500}],
        "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}],
        "total-blocking-time": ["error", {"maxNumericValue": 300}]
      }
    }
  }
}
```

### Web Vitals en Production (Real User Monitoring)

```typescript
// src/lib/vitals.ts
import { onCLS, onINP, onLCP, onFCP, onTTFB } from 'web-vitals';

function envoyerMétrique(métrique: any) {
  // Envoyer à votre service d'analytics
  fetch('/api/vitals', {
    method: 'POST',
    body: JSON.stringify({
      name: métrique.name,
      value: métrique.value,
      rating: métrique.rating, // 'good' | 'needs-improvement' | 'poor'
      id: métrique.id,
      navigationType: métrique.navigationType,
    }),
  });
}

onCLS(envoyerMétrique);
onINP(envoyerMétrique);
onLCP(envoyerMétrique);
onFCP(envoyerMétrique);
onTTFB(envoyerMétrique);
```

---

## Optimisation du Bundle JavaScript

### Analyse du Bundle

```bash
# Next.js : analyzer intégré
ANALYZE=true npm run build

# Vite : rollup-plugin-visualizer
npm install --save-dev rollup-plugin-visualizer
```

```typescript
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    visualizer({
      filename: 'bundle-stats.html',
      open: true,
      gzipSize: true,
      brotliSize: true,
    }),
  ],
});
```

### Code Splitting et Lazy Loading

```typescript
// React : lazy loading des routes (ne charge que la page active)
import { lazy, Suspense } from 'react';

const TableauDeBord = lazy(() => import('./pages/TableauDeBord'));
const Paramètres = lazy(() => import('./pages/Paramètres'));
const Rapports = lazy(() => import('./pages/Rapports'));

function Router() {
  return (
    <Suspense fallback={<Skeleton />}>
      <Routes>
        <Route path="/dashboard" element={<TableauDeBord />} />
        <Route path="/settings" element={<Paramètres />} />
        <Route path="/reports" element={<Rapports />} />
      </Routes>
    </Suspense>
  );
}

// Lazy loading de librairies lourdes
async function exporterPDF() {
  const { default: jsPDF } = await import('jspdf'); // ~300KB — chargé seulement au clic
  const doc = new jsPDF();
  doc.save('rapport.pdf');
}
```

### Tree Shaking

```typescript
// ❌ Import de toute la librairie (lodash = 70KB)
import _ from 'lodash';
const résultat = _.groupBy(données, 'catégorie');

// ✅ Import ciblé (lodash-es = 2KB pour groupBy)
import { groupBy } from 'lodash-es';
const résultat = groupBy(données, 'catégorie');

// ❌ date-fns complet (75KB)
import * as dateFns from 'date-fns';

// ✅ Import ciblé (2KB)
import { format, addDays } from 'date-fns';
```

### Performance Budget

```json
// performance-budget.json
{
  "resourceSizes": [
    { "resourceType": "script",     "budget": 300 },
    { "resourceType": "total",      "budget": 1500 },
    { "resourceType": "image",      "budget": 500 },
    { "resourceType": "stylesheet", "budget": 100 }
  ],
  "timings": [
    { "metric": "interactive",      "budget": 3000 },
    { "metric": "first-contentful-paint", "budget": 1500 }
  ]
}
```

---

## Optimisation des Images

### Formats Modernes

| Format | Usage | Gain vs JPEG |
|---|---|---|
| **WebP** | Photos, screenshots | -25–35% |
| **AVIF** | Photos haute qualité | -50% (support 95%+) |
| **SVG** | Icônes, logos, illustrations | Vectoriel = pas de perte |
| **JPEG** | Fallback, compatibilité maximale | Référence |

```html
<!-- Picture avec fallbacks -->
<picture>
  <source type="image/avif" srcset="/hero.avif">
  <source type="image/webp" srcset="/hero.webp">
  <img src="/hero.jpg" alt="Hero" width="1200" height="630">
</picture>
```

### Next.js Image Optimization

```typescript
import Image from 'next/image';

// Next.js gère automatiquement : WebP/AVIF, responsive, lazy loading, placeholder
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={630}
  priority          // Pas de lazy loading pour l'image LCP
  placeholder="blur" // Blur hash pendant le chargement
  blurDataURL="data:image/jpeg;base64,..." // Généré automatiquement
/>
```

---

## Caching et CDN

### HTTP Cache Headers

```typescript
// Next.js / Express : headers de cache
export function cacheHeaders(type: 'static' | 'dynamic' | 'api') {
  switch (type) {
    case 'static':   // Assets avec hash dans le nom (_next/static/*)
      return 'public, max-age=31536000, immutable'; // 1 an
    case 'dynamic':  // Pages HTML
      return 'public, max-age=0, s-maxage=3600, stale-while-revalidate=86400';
    case 'api':      // Données JSON
      return 'private, max-age=0, must-revalidate';
  }
}

// next.config.js
module.exports = {
  headers: async () => [
    {
      source: '/_next/static/:path*',
      headers: [{ key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }],
    },
    {
      source: '/images/:path*',
      headers: [{ key: 'Cache-Control', value: 'public, max-age=86400, stale-while-revalidate=604800' }],
    },
  ],
};
```

### Service Worker et Workbox

```typescript
// Stratégies de cache avec Workbox
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';

// Assets statiques : Cache First (priorité au cache)
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images-cache',
    plugins: [new ExpirationPlugin({ maxEntries: 100, maxAgeSeconds: 30 * 24 * 60 * 60 })],
  }),
);

// Pages HTML : Network First (priorité au réseau, fallback cache)
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({ cacheName: 'pages-cache' }),
);

// API JSON : Stale While Revalidate (cache immédiat + refresh en arrière-plan)
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new StaleWhileRevalidate({ cacheName: 'api-cache' }),
);
```

---

## Server-Side Rendering et TTFB

### Optimiser le TTFB (Time to First Byte)

**Seuil** : < 800ms (idéalement < 200ms)

```typescript
// Next.js App Router : streaming SSR pour améliorer le TTFB perçu
import { Suspense } from 'react';

export default async function Page() {
  return (
    <div>
      {/* Contenu critique rendu immédiatement */}
      <Hero />

      {/* Contenu lent en Suspense — streamed après */}
      <Suspense fallback={<SkeletonProduits />}>
        <ListeProduits />  {/* fetch() async à l'intérieur */}
      </Suspense>

      <Suspense fallback={<SkeletonRecommandations />}>
        <Recommandations /> {/* fetch() async à l'intérieur */}
      </Suspense>
    </div>
  );
}
```

---

## Checklist Performance

```
LCP < 2,5s
├── ✅ Image LCP avec preload + fetchpriority="high"
├── ✅ TTFB < 800ms (serveur rapide, edge CDN)
├── ✅ Pas de render-blocking CSS critique non-inliné
└── ✅ Format WebP/AVIF

CLS < 0,1
├── ✅ width/height sur toutes les images
├── ✅ Espace réservé pour les publicités
└── ✅ font-display: optional ou swap

INP < 200ms
├── ✅ Pas de long task > 50ms (profiler Chrome)
├── ✅ Heavy work dans Web Workers
└── ✅ Debounce sur les listeners fréquents (scroll, resize)

Bundle
├── ✅ Code splitting par route
├── ✅ Lazy loading des librairies lourdes
├── ✅ Tree shaking actif (imports ciblés)
└── ✅ Pas de duplicate packages (npm dedupe)
```

---

## Références

- `references/core-web-vitals.md` — Métriques détaillées, outils de mesure, CrUX data
- `references/bundle-optimization.md` — Webpack/Vite config, tree shaking, code splitting avancé
- `references/image-caching-cdn.md` — Formats, CDN config, service workers, cache strategies
- `references/case-studies.md` — 4 cas réels : e-commerce +40% conversion, SaaS LCP 4s→1,2s
