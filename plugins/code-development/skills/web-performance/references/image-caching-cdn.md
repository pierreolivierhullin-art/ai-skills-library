# Images, Cache et CDN — Stratégies Complètes

## Images — Formats et Compression

### Comparaison des formats modernes

Le choix du format d'image est la décision avec le plus grand impact sur le poids des pages. Voici un tableau de référence basé sur des benchmarks réels (encodage à qualité perceptuelle équivalente) :

| Format | Meilleur usage | Gain vs JPEG | Support (2025) | Notes |
|--------|---------------|--------------|----------------|-------|
| **AVIF** | Photos, screenshots | -50 à -60% | 96% | Encodage lent, décodage rapide. Meilleur ratio. |
| **WebP** | Photos, images UI | -25 à -35% | 99%+ | Bon compromis qualité/support. |
| **JPEG XL** | Photos haute qualité | -35 à -50% | Limité (Chrome) | Standard en cours d'adoption. |
| **SVG** | Logos, icônes, illustrations | N/A (vectoriel) | 100% | Infiniment scalable, modifiable en CSS. |
| **PNG** | Images avec transparence | Référence | 100% | Utiliser WebP/AVIF quand possible. |
| **JPEG** | Fallback universel | Référence | 100% | Éviter en 2025 sauf contrainte. |
| **GIF** | Animations simples | N/A | 100% | Utiliser WebM/MP4 ou CSS animations à la place. |

### Benchmarks par type de contenu

```
Photos produits e-commerce (1200x800, qualité perceptuelle équivalente) :
  JPEG     : 180 KB (référence)
  WebP     : 115 KB (-36%)
  AVIF     : 78 KB  (-57%)

Screenshots d'interface (2400x1600, texte + UI) :
  PNG      : 890 KB (référence)
  WebP     : 520 KB (-42%)
  AVIF     : 310 KB (-65%)

Illustrations avec zones de couleur plate :
  PNG      : 340 KB
  WebP     : 190 KB (-44%)
  AVIF     : 140 KB (-59%)

Animations (exemple : spinner, animation courte) :
  GIF      : 450 KB (référence)
  WebM     : 85 KB  (-81%) → utiliser <video> au lieu de <img>
  AVIF séquencé : 120 KB (-73%)
```

### Balise `<picture>` avec fallbacks progressifs

```html
<!-- Pattern complet : AVIF → WebP → JPEG -->
<picture>
  <!-- AVIF pour les navigateurs modernes -->
  <source
    type="image/avif"
    srcset="
      /images/hero-400.avif 400w,
      /images/hero-800.avif 800w,
      /images/hero-1200.avif 1200w
    "
    sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  >
  <!-- WebP pour Chrome/Firefox plus anciens -->
  <source
    type="image/webp"
    srcset="
      /images/hero-400.webp 400w,
      /images/hero-800.webp 800w,
      /images/hero-1200.webp 1200w
    "
    sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  >
  <!-- JPEG comme fallback universel -->
  <img
    src="/images/hero-800.jpg"
    alt="Image hero principale"
    width="1200"
    height="630"
    loading="eager"
    fetchpriority="high"
  >
</picture>

<!-- Pour les images non-critiques (below-the-fold) -->
<picture>
  <source type="image/avif" srcset="/images/produit.avif">
  <source type="image/webp" srcset="/images/produit.webp">
  <img
    src="/images/produit.jpg"
    alt="Nom du produit"
    width="400"
    height="400"
    loading="lazy"     <!-- Lazy loading pour les images hors viewport -->
    decoding="async"   <!-- Décodage asynchrone : ne bloque pas le thread principal -->
  >
</picture>
```

---

## Next.js Image Optimization

### Configuration et composant Image

```typescript
// next.config.ts — configuration du composant Image
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  images: {
    // Formats générés automatiquement (ordre de préférence)
    formats: ['image/avif', 'image/webp'],

    // Largeurs de breakpoints pour le srcset responsive
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],

    // Domaines autorisés pour les images externes
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
        port: '',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: '**.cloudinary.com',
      },
    ],

    // Cache des images transformées (en secondes)
    minimumCacheTTL: 86400, // 24h minimum

    // Taille maximale de l'image en cache
    dangerouslyAllowSVG: false, // Ne pas permettre les SVG dynamiques (XSS risk)

    // Loader personnalisé (voir section Cloudinary)
    loader: 'default', // ou 'cloudinary', 'imgix', 'akamai', ou custom
  },
};

export default nextConfig;
```

```typescript
// Composant Image — tous les cas d'usage

import Image from 'next/image';

// 1. Image hero (LCP) — priority obligatoire
function HeroSection() {
  return (
    <div className="hero">
      <Image
        src="/images/hero.jpg"
        alt="Bannière principale"
        width={1200}
        height={630}
        priority              // Désactive le lazy loading, ajoute preload
        quality={85}          // 75 par défaut, 85 pour les images hero
        placeholder="blur"    // Affiche un blur pendant le chargement
        // blurDataURL auto-généré par Next.js pour les images locales
      />
    </div>
  );
}

// 2. Image de contenu — lazy loading par défaut
function CarteProduit({ produit }: { produit: Produit }) {
  return (
    <div className="card">
      <Image
        src={produit.imageUrl}
        alt={produit.nom}
        width={400}
        height={400}
        // loading="lazy" est le défaut — pas besoin de le spécifier
        sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
        // sizes : indique au navigateur la taille affichée selon le viewport
        // Crucial pour le bon srcset et éviter de charger des images trop grandes
        placeholder="blur"
        blurDataURL={produit.blurHash} // Généré côté serveur avec plaiceholder ou sharp
      />
    </div>
  );
}

// 3. Image en fill — pour couvrir un conteneur de dimensions variables
function BannerImage({ src }: { src: string }) {
  return (
    <div style={{ position: 'relative', width: '100%', height: '400px' }}>
      <Image
        src={src}
        alt="Bannière"
        fill                  // Remplit le conteneur parent (doit être position:relative)
        style={{ objectFit: 'cover' }}
        sizes="100vw"
        priority
      />
    </div>
  );
}

// 4. Génération du blurDataURL côté serveur (Next.js server component)
import { getPlaiceholder } from 'plaiceholder'; // npm install plaiceholder sharp

async function getProduitAvecBlur(produit: Produit) {
  const { base64 } = await getPlaiceholder(produit.imageUrl, { size: 10 });
  return { ...produit, blurDataURL: base64 };
}
```

### Loader personnalisé pour Cloudinary/Imgix

```typescript
// lib/cloudinary-loader.ts
import type { ImageLoaderProps } from 'next/image';

export function cloudinaryLoader({ src, width, quality }: ImageLoaderProps): string {
  // src = le chemin relatif sans le domaine Cloudinary
  // Ex: "/produits/sneakers-blanc.jpg" → full URL Cloudinary avec transformations
  const params = [
    `w_${width}`,          // Redimensionner à la largeur demandée
    `q_${quality || 'auto'}`, // Qualité automatique ou spécifiée
    'f_auto',              // Format automatique : AVIF si supporté, sinon WebP, sinon JPEG
    'c_fill',              // Crop : remplir les dimensions
    'g_auto',              // Gravité : centrer intelligemment (détection de visages)
    'dpr_auto',            // Pixel density ratio automatique
  ].join(',');

  return `https://res.cloudinary.com/votre-cloud/image/upload/${params}${src}`;
}

// Utilisation dans le composant Image
<Image
  loader={cloudinaryLoader}
  src="/produits/sneakers-blanc.jpg"
  alt="Sneakers blanc"
  width={400}
  height={400}
/>
// → Génère: https://res.cloudinary.com/votre-cloud/image/upload/w_400,q_auto,f_auto,c_fill/produits/sneakers-blanc.jpg
```

---

## Cloudinary & Imgix — API de Transformation

### Cloudinary — transformations programmatiques

```typescript
// lib/cloudinary.ts — SDK avec transformations typées
import { v2 as cloudinary } from 'cloudinary';

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

// Générer une URL avec transformations
function urlImageProduit(publicId: string, options: {
  largeur: number;
  hauteur?: number;
  qualité?: number;
  format?: 'auto' | 'webp' | 'avif';
  crop?: 'fill' | 'fit' | 'thumb';
}) {
  return cloudinary.url(publicId, {
    width: options.largeur,
    height: options.hauteur,
    quality: options.qualité ?? 'auto',
    fetch_format: options.format ?? 'auto',
    crop: options.crop ?? 'fill',
    gravity: 'auto',   // Recadrage intelligent
    dpr: 'auto',
    secure: true,
  });
}

// Transformations avancées
const urlThumbnail = cloudinary.url('produit/sneakers-blanc', {
  transformation: [
    // Étape 1 : recadrer autour du sujet principal
    { width: 800, height: 800, crop: 'fill', gravity: 'auto' },
    // Étape 2 : fond blanc pour les images produit
    { background: 'white' },
    // Étape 3 : ajouter watermark
    { overlay: 'watermark', opacity: 20, gravity: 'south_east' },
    // Étape 4 : optimiser
    { quality: 'auto', fetch_format: 'auto' },
  ],
  secure: true,
});

// Upload avec transformations automatiques à l'upload
await cloudinary.uploader.upload(cheminFichier, {
  public_id: 'produit/sneakers-blanc',
  eager: [
    // Pré-générer les variantes courantes
    { width: 400, height: 400, crop: 'fill', quality: 'auto', fetch_format: 'auto' },
    { width: 800, height: 800, crop: 'fill', quality: 'auto', fetch_format: 'auto' },
    { width: 1200, height: 1200, crop: 'fill', quality: 'auto', fetch_format: 'auto' },
  ],
  eager_async: true,
});
```

---

## HTTP Cache — Stratégie Complète

### Comprendre les directives Cache-Control

```
Cache-Control: <directives>

Directives de stockage :
  public          : Cache dans les proxies/CDN ET le navigateur
  private         : Cache dans le navigateur uniquement (pas de CDN)
  no-store        : Jamais mis en cache (données sensibles)
  no-cache        : Mis en cache mais toujours re-validé avant utilisation

Directives de durée :
  max-age=N       : TTL en secondes pour le navigateur
  s-maxage=N      : TTL pour les CDN/proxies (override max-age pour les caches partagés)

Directives de comportement :
  immutable       : Le fichier ne changera JAMAIS → pas de re-validation même après expiration
  stale-while-revalidate=N  : Servir le cache expiré pendant N secondes tout en re-validant en arrière-plan
  stale-if-error=N          : Servir le cache même si le serveur répond 5xx, pendant N secondes
  must-revalidate : Doit re-valider après expiration (pas de stale-while-revalidate implicite)
```

### Stratégies par type de ressource

```typescript
// Stratégie complète de headers cache (Next.js / Express)

const CACHE_STRATEGIES = {
  // Assets statiques avec hash dans le nom (_next/static/chunks/main-abc123.js)
  // Le hash change à chaque modification → peut être caché indéfiniment
  staticHashedAssets: 'public, max-age=31536000, immutable',
  // = Cache 1 an, jamais re-validé (navigateur sait que l'URL change si le fichier change)

  // Pages HTML SSR : courte durée + CDN cache + stale-while-revalidate
  htmlPages: 'public, max-age=0, s-maxage=3600, stale-while-revalidate=86400',
  // = Navigateur : jamais de cache local
  //   CDN : cache 1 heure
  //   Si le cache CDN est expiré : servir le stale pendant 24h, régénérer en arrière-plan

  // Pages ISR (Incremental Static Regeneration) Next.js
  isrPages: 'public, max-age=0, s-maxage=60, stale-while-revalidate=86400, stale-if-error=604800',
  // = CDN cache 1 minute, stale acceptable 24h, tolérance d'erreur 7 jours

  // API publique : données lisibles sans authentification
  apiPublique: 'public, max-age=60, s-maxage=300, stale-while-revalidate=600',

  // API privée : données utilisateur spécifiques
  apiPrivée: 'private, max-age=0, must-revalidate',

  // Données sensibles : jamais mises en cache
  sensibles: 'no-store',

  // Images optimisées (avec hash ou versioning dans l'URL)
  images: 'public, max-age=86400, stale-while-revalidate=604800',
  // = Cache 24h, stale acceptable 7 jours

  // Fontes web (stables, changent rarement)
  fonts: 'public, max-age=31536000, immutable',
};

// Application dans next.config.ts
const nextConfig = {
  async headers() {
    return [
      {
        source: '/_next/static/:path*',
        headers: [{ key: 'Cache-Control', value: CACHE_STRATEGIES.staticHashedAssets }],
      },
      {
        source: '/images/:path*',
        headers: [{ key: 'Cache-Control', value: CACHE_STRATEGIES.images }],
      },
      {
        source: '/fonts/:path*',
        headers: [{ key: 'Cache-Control', value: CACHE_STRATEGIES.fonts }],
      },
      {
        source: '/api/public/:path*',
        headers: [{ key: 'Cache-Control', value: CACHE_STRATEGIES.apiPublique }],
      },
      {
        source: '/api/user/:path*',
        headers: [{ key: 'Cache-Control', value: CACHE_STRATEGIES.apiPrivée }],
      },
    ];
  },
};
```

---

## Service Worker — Stratégies de Cache avec Workbox

```typescript
// src/sw.ts — Service Worker avec Workbox

import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching';
import { registerRoute, NavigationRoute } from 'workbox-routing';
import {
  CacheFirst,
  NetworkFirst,
  NetworkOnly,
  StaleWhileRevalidate,
} from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';
import { BackgroundSyncPlugin } from 'workbox-background-sync';

// ✅ Pré-cacher les assets critiques (injectés par le build tool)
precacheAndRoute(self.__WB_MANIFEST);
cleanupOutdatedCaches(); // Supprimer les vieux caches de précache

// ─── Stratégie 1 : Cache First ─────────────────────────────────────────────
// Usage : images, fontes, assets statiques stables
// Comportement : cherche en cache d'abord, réseau seulement si absent du cache
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images-v1',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({
        maxEntries: 150,         // Maximum 150 images en cache
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 jours
        purgeOnQuotaError: true,  // Supprimer si le quota est dépassé
      }),
    ],
  })
);

registerRoute(
  ({ url }) => url.pathname.startsWith('/fonts/') ||
               url.pathname.endsWith('.woff2'),
  new CacheFirst({
    cacheName: 'fonts-v1',
    plugins: [
      new ExpirationPlugin({ maxAgeSeconds: 365 * 24 * 60 * 60 }), // 1 an
    ],
  })
);

// ─── Stratégie 2 : Network First ───────────────────────────────────────────
// Usage : pages HTML, navigation, données critiques fraîches
// Comportement : réseau en priorité, cache en fallback si réseau indisponible
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({
    cacheName: 'pages-v1',
    networkTimeoutSeconds: 3, // Basculer vers le cache si réseau > 3s
    plugins: [
      new CacheableResponsePlugin({ statuses: [200] }),
      new ExpirationPlugin({ maxEntries: 50 }),
    ],
  })
);

// ─── Stratégie 3 : Stale While Revalidate ──────────────────────────────────
// Usage : API data, contenu dynamique acceptable légèrement obsolète
// Comportement : réponse cache immédiate + mise à jour en arrière-plan
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/produits'),
  new StaleWhileRevalidate({
    cacheName: 'api-produits-v1',
    plugins: [
      new CacheableResponsePlugin({ statuses: [200] }),
      new ExpirationPlugin({
        maxEntries: 100,
        maxAgeSeconds: 5 * 60, // 5 minutes avant de considérer le cache stale
      }),
    ],
  })
);

// ─── Stratégie 4 : Network Only ────────────────────────────────────────────
// Usage : endpoints POST/PUT/DELETE, données sensibles, paiements
registerRoute(
  ({ url, request }) =>
    url.pathname.startsWith('/api/paiement') ||
    request.method !== 'GET',
  new NetworkOnly({
    plugins: [
      // Background sync : réessayer les requêtes échouées quand la connexion revient
      new BackgroundSyncPlugin('mutation-queue', {
        maxRetentionTime: 24 * 60, // Réessayer pendant 24h max
      }),
    ],
  })
);
```

---

## CDN — Configuration et Edge Caching

### Cloudflare — règles de cache avancées

```
# Cloudflare Dashboard → Rules → Cache Rules

# Règle 1 : Assets statiques Next.js → cache permanent
If URI Path contains "/_next/static/"
Then: Cache eligibility = Eligible for cache
      Edge Cache TTL = 1 year
      Browser Cache TTL = 1 year

# Règle 2 : Images → cache long avec revalidation
If URI Path contains "/images/"
Then: Cache eligibility = Eligible for cache
      Edge Cache TTL = 1 week
      Browser Cache TTL = 1 day

# Règle 3 : Pages SSR → cache court avec stale-while-revalidate
If URI Path = "/" or URI Path contains "/catalogue"
Then: Cache eligibility = Eligible for cache
      Edge Cache TTL = 1 hour
      Respect Origin Cache-Control = true

# Règle 4 : API routes → pas de cache CDN
If URI Path contains "/api/"
Then: Cache eligibility = Bypass cache
```

```typescript
// API Cloudflare pour purger le cache après un déploiement
async function purgerCacheCloudflare(urls: string[]) {
  const réponse = await fetch(
    `https://api.cloudflare.com/client/v4/zones/${process.env.CF_ZONE_ID}/purge_cache`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.CF_API_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ files: urls }),
    }
  );

  const résultat = await réponse.json();
  if (!résultat.success) {
    throw new Error(`Purge cache Cloudflare échouée: ${JSON.stringify(résultat.errors)}`);
  }
  console.log(`Cache purgé pour ${urls.length} URLs`);
}

// Appeler après chaque déploiement via webhook ou CI/CD
await purgerCacheCloudflare([
  'https://votre-site.com/',
  'https://votre-site.com/catalogue',
  'https://votre-site.com/promotions',
]);

// Purger tout le cache (attention : trafic élevé momentané sur l'origine)
async function purgerToutLeCache() {
  const réponse = await fetch(
    `https://api.cloudflare.com/client/v4/zones/${process.env.CF_ZONE_ID}/purge_cache`,
    {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${process.env.CF_API_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ purge_everything: true }),
    }
  );
  return réponse.json();
}
```

### Edge SSR — Rendering au plus proche de l'utilisateur

```typescript
// Next.js : forcer le rendu en edge (Vercel Edge Functions, Cloudflare Workers)
export const runtime = 'edge'; // Exporter depuis n'importe quel route handler

// Avantages :
// - Rendu dans le datacenter le plus proche de l'utilisateur (< 50ms TTFB partout)
// - Démarrage instantané (pas de cold start Node.js)
// Limitations :
// - Pas d'accès à certaines API Node.js (fs, crypto complet, etc.)
// - Pas de DB directe : utiliser des DB edge-compatibles (PlanetScale, Neon, Turso)

export default async function Page() {
  const data = await fetch('https://api.votre-service.com/data', {
    next: { revalidate: 60 }, // Cache Next.js data cache : 60 secondes
  });
  return <div>{/* ... */}</div>;
}
```

---

## CSS Critique — Inlining et Extraction

### critters — inlining automatique du CSS critique

```typescript
// next.config.ts — critters s'intègre directement dans Next.js via experimental
const nextConfig = {
  experimental: {
    optimizeCss: true, // Active critters automatiquement (extraction CSS critique)
  },
};

// Comportement :
// 1. Next.js génère les pages HTML statiques
// 2. critters analyse chaque page et extrait le CSS "above-the-fold"
// 3. Ce CSS critique est inliné dans le <style> du <head>
// 4. Le reste du CSS est chargé en async (link preload + onload)
```

```javascript
// Configuration manuelle avec critters (pour webpack custom)
const Critters = require('critters-webpack-plugin');

module.exports = {
  plugins: [
    new Critters({
      // Stratégies d'inlining
      strategy: 'critical',    // 'critical' | 'all' | 'media' | 'container'
      pruneSource: true,        // Supprimer le CSS inliné du fichier CSS externe
      mergeStylesheets: true,   // Fusionner tous les <style> inline en un seul
      preload: 'swap',          // Méthode de chargement du CSS non-critique
      noscriptFallback: true,   // Fallback pour JavaScript désactivé
    }),
  ],
};
```

---

## Resource Hints — Optimiser l'Ordre de Chargement

### Tous les resource hints et leur usage

```html
<head>
  <!-- ─── preconnect ────────────────────────────────────────────────────── -->
  <!-- Établit la connexion TCP+TLS en avance. Utiliser pour les origines
       tierces critiques (CDN, fonts, API). Ne pas abuser : coûte des ressources. -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://cdn.votre-site.com">

  <!-- ─── dns-prefetch ─────────────────────────────────────────────────── -->
  <!-- Résout le DNS en avance. Plus léger que preconnect. Utiliser pour les
       origines moins critiques ou nombreuses. -->
  <link rel="dns-prefetch" href="https://analytics.votre-site.com">
  <link rel="dns-prefetch" href="https://cdn.partenaire.com">

  <!-- ─── preload ──────────────────────────────────────────────────────── -->
  <!-- Charge la ressource immédiatement à haute priorité. Utiliser pour
       les ressources critiques découvertes tardivement (image LCP, fonte critique). -->
  <!-- Image LCP : le plus important -->
  <link rel="preload" as="image" href="/hero.webp" fetchpriority="high">
  <!-- Ou avec srcset responsive -->
  <link rel="preload" as="image"
    imagesrcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1200.webp 1200w"
    imagesizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
    fetchpriority="high">

  <!-- Fonte critique -->
  <link rel="preload" as="font" type="font/woff2"
    href="/fonts/inter-regular.woff2" crossorigin>

  <!-- Script critique non-defer -->
  <link rel="preload" as="script" href="/critical-init.js">

  <!-- ─── prefetch ─────────────────────────────────────────────────────── -->
  <!-- Charge en arrière-plan à basse priorité pendant l'inactivité.
       Utiliser pour les ressources de la prochaine navigation probable. -->
  <link rel="prefetch" href="/pages/catalogue.js">
  <link rel="prefetch" as="image" href="/images/next-promo.webp">

  <!-- ─── modulepreload ────────────────────────────────────────────────── -->
  <!-- Comme preload mais pour les ES modules : parse et compile aussi.
       Plus efficace que preload pour les modules JS. -->
  <link rel="modulepreload" href="/assets/react-vendor-abc123.js">
</head>
```

---

## Optimisation des Polices Web

### Stratégie complète de chargement des fontes

```html
<!-- Étape 1 : preconnect aux serveurs de fontes Google -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Étape 2 : preload des fontes les plus critiques (uniquement 1-2 max) -->
<link rel="preload" as="font" type="font/woff2"
  href="https://fonts.gstatic.com/s/inter/v13/inter-regular.woff2"
  crossorigin>

<!-- Étape 3 : chargement asynchrone de la CSS des fontes -->
<link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=optional"
>
```

### Self-hosting des fontes (recommandé)

```bash
# Télécharger et optimiser avec google-webfonts-helper
# ou utiliser fontsource (npm)

npm install @fontsource/inter
```

```typescript
// layout.tsx (Next.js App Router)
import { Inter } from 'next/font/google';

// Next.js télécharge et self-host automatiquement la fonte
// Avec subsetting, preload, et zero layout shift
const inter = Inter({
  subsets: ['latin'],          // Subset : ne charger que les caractères nécessaires
  display: 'optional',         // font-display: optional → pas de FOUT/FOIT
  variable: '--font-inter',    // Variable CSS pour une utilisation flexible
  preload: true,               // Preload automatique dans le <head>
  fallback: ['system-ui', 'arial'], // Polices de fallback précises
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
```

```css
/* Subsetting manuel avec fonttools (Python) */
/* Installer : pip install fonttools brotli zopfli */
/* Commande : pyftsubset Inter-Regular.ttf --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD" --output-file=inter-regular-subset.woff2 --flavor=woff2 */

/* Résultat typique : 85KB → 18KB pour le subset latin */

@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-regular-subset.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: optional;
  /* size-adjust pour réduire le layout shift lors du swap */
  size-adjust: 100%;
  ascent-override: 90%;
  descent-override: 22%;
}
```

---

## Récapitulatif — Décisions Clés

| Décision | Recommandation 2025 | Impact |
|---|---|---|
| Format image | AVIF premier, WebP fallback, JPEG dernier recours | Très élevé |
| Dimensions images | Toujours `width` + `height` ou `aspect-ratio` | CLS critique |
| Image LCP | `priority` + `fetchpriority="high"` + preload | LCP critique |
| Cache assets statiques | `immutable` + hash dans l'URL | Performance cache |
| Cache pages SSR | `stale-while-revalidate` + CDN | UX + serveur |
| Fontes web | Self-host + `font-display: optional` + subset | LCP + CLS |
| Service Worker | Workbox avec stratégies différenciées par ressource | Offline + perf |
| CDN | Edge CDN (Cloudflare/Vercel) géographiquement proche | TTFB partout |
