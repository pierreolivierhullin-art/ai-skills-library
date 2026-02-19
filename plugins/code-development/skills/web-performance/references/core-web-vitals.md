# Core Web Vitals — Métriques, Mesure et Optimisation

## Vue d'ensemble des Core Web Vitals

Les Core Web Vitals sont trois métriques définies par Google pour mesurer l'expérience utilisateur réelle sur le web. Depuis 2021, elles constituent un facteur de ranking SEO officiel dans les algorithmes de recherche. Contrairement aux métriques de laboratoire purement techniques, les CWV mesurent ce que l'utilisateur perçoit : vitesse d'affichage, stabilité visuelle, réactivité aux interactions.

Les trois métriques actuelles (état 2024-2025) :
- **LCP** (Largest Contentful Paint) — vitesse d'affichage du contenu principal
- **CLS** (Cumulative Layout Shift) — stabilité visuelle
- **INP** (Interaction to Next Paint) — réactivité aux interactions, remplace FID depuis mars 2024

Deux métriques complémentaires non incluses dans le score CWV mais importantes :
- **FCP** (First Contentful Paint) — premier pixel de contenu rendu
- **TTFB** (Time to First Byte) — temps de réponse serveur

---

## LCP — Largest Contentful Paint

### Anatomie et décomposition

Le LCP mesure le temps entre le début de la navigation et l'affichage du plus grand élément de contenu visible dans le viewport. L'élément candidat est généralement : une image `<img>`, une image de fond CSS via `background-image`, un élément `<video>` (poster), ou un bloc de texte `<p>`, `<h1>`.

Chrome décompose le LCP en quatre sous-parties diagnostiques :

```
LCP total = TTFB + Load Delay + Load Time + Render Delay

TTFB         : Temps serveur (< 200ms idéal)
Load Delay   : Délai avant que le navigateur découvre et commence à charger la ressource LCP
Load Time    : Temps de téléchargement de la ressource LCP elle-même
Render Delay : Délai entre fin du téléchargement et affichage effectif à l'écran
```

Pour visualiser ces sous-parties dans Chrome DevTools :
1. Ouvrir DevTools → onglet Performance
2. Enregistrer un rechargement de page
3. Dans la timeline, repérer l'événement LCP (marqueur violet)
4. Dans le panneau "Timings", les quatre phases apparaissent en hover sur le marqueur LCP

### TTFB — Time to First Byte comme prérequis LCP

Un TTFB élevé pénalise mécaniquement le LCP puisque tout commence après la réponse serveur. Seuils :
- Bon : < 800ms
- À améliorer : 800ms–1800ms
- Mauvais : > 1800ms

Causes fréquentes d'un TTFB lent et solutions :

```
TTFB lent → diagnostic :
├── Serveur géographiquement éloigné de l'utilisateur → utiliser un CDN edge (Cloudflare, Vercel Edge)
├── Rendu serveur lent (requêtes DB, calculs) → cache SSR, ISR (Next.js), streaming
├── Absence de cache HTTP → configurer Cache-Control sur les pages HTML
└── Cold start serverless → warm-up, ou basculer vers edge functions
```

```typescript
// Next.js : mesurer et logger le TTFB côté serveur
// app/page.tsx
import { headers } from 'next/headers';

export async function generateMetadata() {
  const start = Date.now();
  const data = await fetchCriticalData();
  console.log(`[TTFB] Fetch critical data: ${Date.now() - start}ms`);
  return {};
}

// Réponse en streaming pour améliorer le TTFB perçu
// Le HTML commence à s'envoyer avant que toutes les données soient prêtes
export default async function Page() {
  return (
    <main>
      <HeroSection /> {/* Rendu immédiat — pas de fetch */}
      <Suspense fallback={<ProductSkeleton />}>
        <AsyncProducts /> {/* Streamed après — fetch() interne */}
      </Suspense>
    </main>
  );
}
```

### Ressources render-blocking et Load Delay

Le navigateur ne peut pas afficher le LCP tant que le Critical Rendering Path n'est pas complété. Les ressources bloquantes retardent ce chemin :

```html
<!-- ❌ CSS bloquant dans le <head> : bloque tout rendu jusqu'au chargement -->
<link rel="stylesheet" href="/styles/app.css">
<link rel="stylesheet" href="/styles/vendor.css">

<!-- ✅ CSS critique inline + CSS non-critique en async -->
<style>
  /* CSS critique uniquement : hero, header, above-the-fold */
  .hero { background: #000; color: #fff; padding: 4rem; }
  .nav { display: flex; gap: 1rem; }
</style>
<!-- CSS non-critique chargé en async -->
<link rel="preload" href="/styles/app.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/styles/app.css"></noscript>

<!-- ❌ JavaScript bloquant sans defer/async -->
<script src="/app.js"></script>

<!-- ✅ JS différé : ne bloque pas le parser HTML -->
<script src="/app.js" defer></script>
<!-- ou async pour les scripts indépendants (analytics, etc.) -->
<script src="/analytics.js" async></script>
```

### Optimisation de l'image LCP

L'image hero est le candidat LCP le plus fréquent. Erreurs classiques et solutions :

```html
<!-- ❌ Problème 1 : image LCP sans preload → découverte tardive -->
<!-- Le navigateur ne découvre l'image qu'en parsant le HTML puis le CSS -->
<div style="background-image: url('/hero.webp')"></div>

<!-- ✅ Solution : preload déclaratif dans le <head> -->
<link
  rel="preload"
  as="image"
  href="/hero-1200.webp"
  imagesrcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1200.webp 1200w"
  imagesizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  fetchpriority="high"
>

<!-- ❌ Problème 2 : lazy loading sur l'image LCP -->
<img src="/hero.webp" loading="lazy" alt="Hero">

<!-- ✅ Solution : eager + fetchpriority high pour l'image LCP -->
<img
  src="/hero-800.webp"
  srcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1200.webp 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  loading="eager"
  fetchpriority="high"
  width="1200"
  height="630"
  alt="Image hero principale"
>

<!-- ❌ Problème 3 : image trop grande (4000x2000px chargée sur mobile) -->
<!-- Toujours servir des images redimensionnées côté serveur -->
```

### Render Delay — causes et élimination

Le Render Delay survient quand l'image est téléchargée mais ne s'affiche pas encore. Causes :

```javascript
// Cause 1 : JavaScript bloque le main thread juste avant le paint
// Éviter les scripts lourds synchrones au chargement de la page

// Cause 2 : Animations CSS sur l'élément LCP avec opacity:0 → opacity:1
// ❌ L'élément est "techniquement visible" mais opacity:0 cache l'image
.hero-img {
  opacity: 0;
  animation: fadeIn 1s ease forwards; /* Retarde le LCP ! */
}

// ✅ Utiliser visibility ou simplement afficher immédiatement l'image LCP
// Les animations d'apparition sont belles mais coûtent du LCP

// Cause 3 : Fonts bloquant le rendu du texte LCP (FOIT — Flash of Invisible Text)
// Si le candidat LCP est un texte, attendre la fonte retarde le LCP
@font-face {
  font-family: 'MyFont';
  src: url('/fonts/myfont.woff2') format('woff2');
  font-display: swap; /* Affiche le fallback immédiatement, swap quand prêt */
}
```

---

## CLS — Cumulative Layout Shift

### Anatomie des layout shifts

Un layout shift se produit quand un élément visible change de position entre deux frames consécutifs. Le score CLS est la somme de tous les layout shifts inattendus pondérés par la surface déplacée et la distance parcourue :

```
Score layout shift = Impact Fraction × Distance Fraction

Impact Fraction : fraction de viewport affectée par le mouvement
Distance Fraction : fraction de viewport représentant la distance maximale de déplacement
```

### Cause 1 : Images sans dimensions explicites

```html
<!-- ❌ Sans dimensions : le navigateur ne peut pas réserver l'espace -->
<!-- Il alloue 0px de hauteur, puis saute quand l'image charge -->
<img src="/produit.jpg" alt="Produit">

<!-- ✅ Dimensions explicites en HTML : le navigateur calcule l'aspect-ratio à l'avance -->
<img src="/produit.jpg" alt="Produit" width="400" height="300">

<!-- ✅ Ou en CSS avec aspect-ratio -->
<style>
  .product-img {
    width: 100%;
    aspect-ratio: 4 / 3; /* Réserve l'espace avec le bon ratio */
    object-fit: cover;
  }
</style>
<img src="/produit.jpg" alt="Produit" class="product-img">

<!-- ✅ Pour les vidéos : même approche -->
<div style="aspect-ratio: 16 / 9; width: 100%;">
  <iframe src="https://youtube.com/embed/xxx" loading="lazy"
    width="100%" height="100%" frameborder="0"></iframe>
</div>
```

### Cause 2 : Contenu dynamique inséré au-dessus du contenu existant

```javascript
// ❌ Bannière cookies / notifications injectée dynamiquement en haut de page
// déplace tout le contenu vers le bas → CLS élevé
document.body.insertBefore(cookieBanner, document.body.firstChild);

// ✅ Réserver l'espace à l'avance avec un placeholder
// La bannière occupe l'espace mais son contenu arrive dynamiquement
```

```css
/* ✅ Réserver l'espace pour la bannière même avant son chargement */
.cookie-banner-placeholder {
  min-height: 60px; /* Hauteur connue de la bannière */
  width: 100%;
}

/* ✅ Ou utiliser position: fixed pour les éléments qui ne déplacent pas le flux */
.cookie-banner {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  /* Un élément fixed n'impacte pas le CLS */
}
```

### Cause 3 : Publicités et emplacements ads

```html
<!-- ❌ Slot publicitaire sans dimensions réservées -->
<div id="ad-banner"></div>
<!-- Quand le script publicitaire charge, il injecte une iframe de 250px → layout shift -->

<!-- ✅ Réserver l'espace aux dimensions standard IAB -->
<div id="ad-banner" style="min-height: 250px; width: 100%; max-width: 970px;">
  <!-- Optionnel : placeholder visuel pendant le chargement -->
  <div class="ad-placeholder" aria-hidden="true"></div>
</div>
```

```css
.ad-placeholder {
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 250px;
  color: #999;
  font-size: 12px;
}
.ad-placeholder::after {
  content: 'Publicité';
}
```

### Cause 4 : Web fonts — FOUT et FOIT

```css
/* FOIT (Flash of Invisible Text) : texte invisible pendant le chargement de la fonte
   → pas de CLS mais mauvais LCP si c'est un titre */
@font-face {
  font-family: 'Heading';
  src: url('/fonts/heading.woff2') format('woff2');
  font-display: block; /* Invisible jusqu'à chargement — risque LCP */
}

/* FOUT (Flash of Unstyled Text) : texte affiché en fallback, puis swap
   → peut causer un léger CLS si les métriques des fontes diffèrent */
@font-face {
  font-family: 'Body';
  src: url('/fonts/body.woff2') format('woff2');
  font-display: swap; /* Fallback immédiat + swap = CLS possible */
}

/* ✅ font-display: optional — meilleure option pour éviter tout CLS */
/* N'utilise la police web que si elle est déjà en cache ou charge très vite */
@font-face {
  font-family: 'Body';
  src: url('/fonts/body.woff2') format('woff2');
  font-display: optional;
}

/* ✅ size-adjust pour réduire le CLS lors du swap : aligne les métriques */
@font-face {
  font-family: 'Body-Fallback';
  src: local('Arial');
  size-adjust: 102%; /* Ajuster jusqu'à ce que le texte occupe le même espace */
  ascent-override: 90%;
  descent-override: 25%;
  line-gap-override: 0%;
}
```

---

## INP — Interaction to Next Paint

### Anatomie d'une interaction INP

L'INP mesure la latence de la pire interaction (parmi toutes les interactions d'une session) entre l'événement utilisateur et le prochain affichage. Une interaction se décompose en trois phases :

```
INP total = Input Delay + Processing Time + Presentation Delay

Input Delay       : délai avant que le callback de l'événement commence à s'exécuter
                    (caused by long tasks occupying the main thread)
Processing Time   : temps d'exécution du callback de l'événement lui-même
Presentation Delay: délai entre la fin du callback et l'affichage visuel du résultat
```

### Identifier les interactions lentes

```javascript
// Observer les interactions lentes avec PerformanceObserver
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    // entry.name = 'click', 'keydown', 'pointerdown', etc.
    if (entry.duration > 200) { // INP "à améliorer"
      console.warn(`Interaction lente détectée: ${entry.name}`, {
        duration: entry.duration,
        startTime: entry.startTime,
        processingStart: entry.processingStart,
        processingEnd: entry.processingEnd,
        // Calculer les phases
        inputDelay: entry.processingStart - entry.startTime,
        processingTime: entry.processingEnd - entry.processingStart,
        presentationDelay: entry.duration - (entry.processingEnd - entry.startTime),
      });
    }
  }
});

observer.observe({ type: 'event', buffered: true, durationThreshold: 100 });
```

### Réduire l'Input Delay avec scheduler.yield()

L'Input Delay est causé par des long tasks (tâches > 50ms) qui occupent le main thread au moment où l'utilisateur interagit. La solution est de découper ces tâches :

```javascript
// ❌ Problème : traitement synchrone de 10 000 éléments = long task
function filtrerProduits(produits, critères) {
  return produits.filter(p => correspondAuxCritères(p, critères));
  // Si produits.length = 10000 et correspondAuxCritères est complexe = 300ms de blocage
}

// ✅ Solution 1 : scheduler.yield() (Chrome 115+, en cours de standardisation)
async function filtrerProduitsAsync(produits, critères) {
  const résultats = [];
  for (let i = 0; i < produits.length; i++) {
    if (i % 500 === 0 && i > 0) {
      await scheduler.yield(); // Rend le contrôle au navigateur, permet d'autres interactions
    }
    if (correspondAuxCritères(produits[i], critères)) {
      résultats.push(produits[i]);
    }
  }
  return résultats;
}

// ✅ Solution 2 : setTimeout avec 0ms pour céder le main thread (compatible tous navigateurs)
function yieldToMain() {
  return new Promise(resolve => setTimeout(resolve, 0));
}

async function filtrerProduitsCompatible(produits, critères) {
  const résultats = [];
  for (let i = 0; i < produits.length; i++) {
    if (i % 200 === 0 && i > 0) {
      await yieldToMain();
    }
    if (correspondAuxCritères(produits[i], critères)) {
      résultats.push(produits[i]);
    }
  }
  return résultats;
}
```

### Web Workers pour le Processing Time

Pour les calculs vraiment lourds, déporter hors du main thread :

```javascript
// worker.js — s'exécute dans un thread séparé
self.onmessage = function({ data: { produits, critères } }) {
  const résultats = produits.filter(p => correspondAuxCritères(p, critères));
  self.postMessage({ résultats });
};

// main.js — interface utilisateur reste fluide pendant le calcul
const worker = new Worker('/workers/filtre-produits.js');

function filtrerAvecWorker(produits, critères) {
  return new Promise((resolve) => {
    worker.postMessage({ produits, critères });
    worker.onmessage = ({ data: { résultats } }) => resolve(résultats);
  });
}

// Usage dans un handler de clic — INP non impacté par le calcul dans le Worker
document.querySelector('#filtrer').addEventListener('click', async () => {
  const résultats = await filtrerAvecWorker(tousLesProduits, critèresActuels);
  afficherRésultats(résultats); // Mise à jour UI dans le main thread
});
```

### Réduire le Presentation Delay

```javascript
// ❌ Style recalculation forcé (forced reflow) après interaction
button.addEventListener('click', () => {
  element.style.display = 'block';
  const hauteur = element.offsetHeight; // Force un reflow synchrone !
  console.log(hauteur);
  element.style.transform = `translateY(-${hauteur}px)`;
});

// ✅ Lire les propriétés de layout avant d'écrire
button.addEventListener('click', () => {
  const hauteur = element.offsetHeight; // Lecture en premier
  element.style.display = 'block';      // Écriture ensuite
  element.style.transform = `translateY(-${hauteur}px)`;
});

// ✅ Utiliser requestAnimationFrame pour grouper les updates visuels
button.addEventListener('click', () => {
  requestAnimationFrame(() => {
    // Toutes les mises à jour DOM dans le même frame
    element1.classList.add('active');
    element2.style.opacity = '1';
    element3.textContent = 'Mis à jour';
  });
});
```

---

## FCP — First Contentful Paint

Le FCP mesure le temps jusqu'au premier pixel de contenu (texte, image, SVG, canvas non-blanc). Un FCP lent indique généralement un problème de render-blocking ou de TTFB.

**Seuils** : Bon < 1,8s | À améliorer 1,8s–3s | Mauvais > 3s

```html
<!-- Optimiser le FCP : éliminer toutes les ressources bloquantes -->
<head>
  <!-- ✅ CSS critique inline — pas de requête réseau bloquante -->
  <style>
    /* Above-the-fold uniquement : header, hero, navigation */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, sans-serif; }
    .header { /* ... */ }
    .hero { /* ... */ }
  </style>

  <!-- ✅ Preconnect aux origines tierces critiques -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- ✅ Pas de JavaScript synchrone bloquant avant le contenu -->
</head>
```

---

## TTFB — Time to First Byte

Le TTFB mesure le délai entre la requête HTTP et la réception du premier octet de la réponse. C'est le prédicteur le plus fort du LCP et du FCP pour les pages SSR.

```
TTFB = DNS Resolution + TCP Connection + TLS Handshake + Server Processing + Transfer Start

Optimisations par phase :
├── DNS Resolution     : dns-prefetch, TTL long sur les enregistrements DNS
├── TCP + TLS          : HTTP/2 ou HTTP/3, CDN géographiquement proche
├── Server Processing  : cache SSR, optimisation des requêtes DB, edge computing
└── Transfer Start     : compression Brotli/gzip, streaming HTTP
```

---

## Chrome UX Report (CrUX) — Données Terrain

### Lab data vs Field data

```
Lab data (données de laboratoire)     Field data (données terrain / RUM)
──────────────────────────────────    ──────────────────────────────────
Lighthouse en local ou CI             Chrome UX Report (CrUX)
Conditions contrôlées                 Données réelles d'utilisateurs Chrome
Répétable, déterministe              Variable selon l'appareil, la connexion
Utile pour le débogage               Décisif pour le ranking SEO Google
Pas de données sur de vrais users    30 jours glissants, percentile 75
```

Google utilise exclusivement les Field Data (CrUX) pour le ranking. Un score Lighthouse de 100 ne garantit rien si les vrais utilisateurs sur mobile 3G ont un LCP à 5s.

### Accéder aux données CrUX

```javascript
// API CrUX (Google — gratuite, clé API requise)
const réponse = await fetch(
  'https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=VOTRE_CLÉ_API',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      url: 'https://votre-site.com/',
      formFactor: 'PHONE', // 'DESKTOP' | 'TABLET' | 'PHONE' | omis = tous
      metrics: ['largest_contentful_paint', 'cumulative_layout_shift', 'interaction_to_next_paint'],
    }),
  }
);

const { record } = await réponse.json();

// Lire le percentile 75 (seuil Google)
const lcp = record.metrics.largest_contentful_paint;
console.log(`LCP p75: ${lcp.percentiles.p75}ms`);
console.log(`LCP distribution:`, lcp.histogram);
// histogram = [{start: 0, end: 2500, density: 0.72}, {start: 2500, end: 4000, density: 0.18}, ...]
```

---

## Real User Monitoring avec la bibliothèque web-vitals

```typescript
// src/instrumentation/web-vitals.ts
import { onCLS, onINP, onLCP, onFCP, onTTFB, type Metric } from 'web-vitals/attribution';

// La version "attribution" donne le contexte de cause de chaque métrique

function envoyerMétrique(métrique: Metric) {
  const payload = {
    name: métrique.name,
    value: métrique.value,
    delta: métrique.delta,        // Variation depuis la dernière mesure
    rating: métrique.rating,      // 'good' | 'needs-improvement' | 'poor'
    id: métrique.id,              // Identifiant unique de la session métrique
    navigationType: métrique.navigationType, // 'navigate' | 'reload' | 'back-forward'
    url: window.location.href,
    userAgent: navigator.userAgent,
    timestamp: Date.now(),
  };

  // Attribution spécifique par métrique
  if (métrique.name === 'LCP' && 'attribution' in métrique) {
    const attr = (métrique as any).attribution;
    Object.assign(payload, {
      lcpElement: attr.element,         // Sélecteur CSS de l'élément LCP
      lcpUrl: attr.url,                 // URL de la ressource LCP
      lcpTimeToFirstByte: attr.timeToFirstByte,
      lcpResourceLoadDelay: attr.resourceLoadDelay,
      lcpResourceLoadDuration: attr.resourceLoadDuration,
      lcpElementRenderDelay: attr.elementRenderDelay,
    });
  }

  if (métrique.name === 'CLS' && 'attribution' in métrique) {
    const attr = (métrique as any).attribution;
    Object.assign(payload, {
      clsLargestShiftTarget: attr.largestShiftTarget,
      clsLargestShiftValue: attr.largestShiftValue,
      clsLargestShiftTime: attr.largestShiftTime,
      clsLoadState: attr.loadState,
    });
  }

  // Envoyer via sendBeacon pour ne pas bloquer la navigation
  if (navigator.sendBeacon) {
    navigator.sendBeacon('/api/vitals', JSON.stringify(payload));
  } else {
    fetch('/api/vitals', { method: 'POST', body: JSON.stringify(payload), keepalive: true });
  }
}

// Enregistrer tous les observers
onCLS(envoyerMétrique);
onINP(envoyerMétrique, { reportAllChanges: true }); // Rapport à chaque interaction
onLCP(envoyerMétrique);
onFCP(envoyerMétrique);
onTTFB(envoyerMétrique);
```

---

## PageSpeed Insights API — Intégration CI/CD

```typescript
// scripts/check-performance.ts — vérification automatique après déploiement
async function vérifierPerformance(url: string) {
  const apiUrl = `https://www.googleapis.com/pagespeedonline/v5/runPagespeed` +
    `?url=${encodeURIComponent(url)}&strategy=mobile&key=${process.env.PSI_API_KEY}`;

  const réponse = await fetch(apiUrl);
  const données = await réponse.json();

  const { categories, audits } = données.lighthouseResult;
  const métriques = données.loadingExperience?.metrics; // Données CrUX si disponibles

  console.log('=== Rapport PageSpeed Insights ===');
  console.log(`Score Performance (lab): ${Math.round(categories.performance.score * 100)}`);

  if (métriques) {
    console.log('\n=== Core Web Vitals (terrain) ===');
    console.log(`LCP: ${métriques.LARGEST_CONTENTFUL_PAINT_MS?.percentile}ms (${métriques.LARGEST_CONTENTFUL_PAINT_MS?.category})`);
    console.log(`CLS: ${métriques.CUMULATIVE_LAYOUT_SHIFT_SCORE?.percentile} (${métriques.CUMULATIVE_LAYOUT_SHIFT_SCORE?.category})`);
    console.log(`INP: ${métriques.INTERACTION_TO_NEXT_PAINT?.percentile}ms (${métriques.INTERACTION_TO_NEXT_PAINT?.category})`);
  }

  // Échouer le CI si les seuils ne sont pas respectés
  const scorePerf = categories.performance.score * 100;
  if (scorePerf < 80) {
    console.error(`Échec : score performance ${scorePerf} < 80`);
    process.exit(1);
  }
}

vérifierPerformance(process.argv[2] || 'https://votre-site.com');
```

---

## Outils de Débogage

### Chrome DevTools — onglet Performance

Workflow de débogage par métrique :

**LCP** :
1. Ouvrir DevTools → Performance → Enregistrer un rechargement
2. Chercher l'event "LCP" dans la timeline (bande "Timings")
3. Cliquer dessus → voir les 4 phases dans le panneau inférieur
4. Identifier la phase la plus longue → corriger en priorité

**CLS** :
1. Dans Performance, chercher les "Layout Shift" events (bande orange)
2. Cliquer sur un shift → le panneau inférieur montre l'élément déplacé
3. Dans Elements, inspecter l'élément pour trouver pourquoi il bouge

**INP** :
1. Performance → enregistrer une interaction
2. Chercher dans la bande "Main" les long tasks (blocs rouges)
3. Le "Total Blocking Time" est la somme des temps > 50ms de toutes les long tasks

### Extension Web Vitals pour Chrome

```
Installation : Chrome Web Store → "Web Vitals"

Affiche en overlay sur toute page :
├── LCP en temps réel avec l'élément candidat mis en évidence
├── CLS avec visualisation des zones de shift
├── INP avec la pire interaction de la session
└── Badge vert/orange/rouge dans la toolbar Chrome
```

### Workflow de mesure complet

```
1. MESURER EN TERRAIN
   └── Search Console → Core Web Vitals → identifier les pages problématiques

2. REPRODUIRE EN LAB
   └── PageSpeed Insights sur les URLs problématiques
   └── Lighthouse en DevTools (mode Incognito, throttling 4G)

3. DIAGNOSTIQUER
   ├── LCP > 2,5s → DeVTools Performance → 4 phases → corriger TTFB ou image
   ├── CLS > 0,1  → Layout Shift dans Performance → trouver l'élément
   └── INP > 200ms → Long Tasks dans Performance → découper ou Web Worker

4. CORRIGER ET VALIDER
   └── Déployer → attendre 28 jours → Search Console confirme amélioration CrUX

5. MONITORER EN CONTINU
   └── web-vitals library → endpoint analytics → alertes si régression
```

---

## Seuils de Référence par Métrique

| Métrique | Bon | À améliorer | Mauvais | Percentile Google |
|----------|-----|-------------|---------|-------------------|
| LCP | < 2,5s | 2,5s–4s | > 4s | p75 |
| CLS | < 0,1 | 0,1–0,25 | > 0,25 | p75 |
| INP | < 200ms | 200ms–500ms | > 500ms | p75 |
| FCP | < 1,8s | 1,8s–3s | > 3s | p75 |
| TTFB | < 800ms | 800ms–1800ms | > 1800ms | p75 |

Google évalue le **75ème percentile** de vos utilisateurs : 75% de vos sessions doivent respecter le seuil "Bon" pour que la page soit considérée comme performante.
