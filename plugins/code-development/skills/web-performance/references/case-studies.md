# Études de Cas — Web Performance en Production

## Introduction

Ces quatre études de cas illustrent des scénarios réels de dégradation de performance et les optimisations appliquées pour les corriger. Chaque cas suit la même structure : contexte applicatif, diagnostic initial (métriques Lighthouse + terrain), optimisations appliquées avec le code exact, résultats mesurés, et la leçon principale à retenir.

---

## Cas 1 — E-commerce Shopify-style : LCP 4,2s → 1,1s

### Contexte

Boutique en ligne de mode avec 50 000 produits, stack technique : Next.js 14, hébergé sur Vercel, CDN Cloudflare en front, images stockées sur AWS S3. Le traffic est majoritairement mobile (68%). Le site souffre d'un bounce rate de 42% et le taux de conversion sur mobile est 60% inférieur au desktop.

### Diagnostic initial

**Lighthouse (mobile, throttling 4G simulé) :**
```
Performance score  : 41 / 100
LCP                : 4,2 s   ❌ (Mauvais > 4s)
CLS                : 0,18    ⚠️ (À améliorer)
INP                : 220 ms  ⚠️ (À améliorer)
TBT                : 480 ms
FCP                : 2,8 s
TTFB               : 1,4 s
```

**Core Web Vitals terrain (CrUX, percentile 75, mobile) :**
```
LCP : 4,8 s   ❌
CLS : 0,22    ❌
INP : 310 ms  ⚠️
```

**Analyse du problème avec Chrome DevTools :**

Décomposition du LCP (élément : image hero 1800×600px sur la page d'accueil) :
```
TTFB              : 1 380 ms  ← Serveur Vercel US, utilisateurs FR → 1,4s aller-retour
Load Delay        : 420 ms   ← Image découverte seulement après parsing du CSS
Load Time         : 2 100 ms ← Image JPEG 640KB téléchargée
Render Delay      : 300 ms   ← Script analytics bloquant avant premier paint

LCP total         : 4 200 ms
```

### Optimisations appliquées

**Optimisation 1 : TTFB — Activer le CDN Cloudflare pour le SSR**

Le site tournait en SSR pur sur Vercel US (sans cache CDN pour le HTML) car les pages produit étaient marquées `no-store`. Migration vers ISR + cache Cloudflare :

```typescript
// app/page.tsx — Page d'accueil : ISR avec revalidation 5 minutes
export const revalidate = 300; // 5 minutes

// app/produit/[slug]/page.tsx — Pages produit : ISR avec revalidation 10 minutes
export const revalidate = 600;

// Résultat : le HTML est servi depuis le CDN Cloudflare (datacenter FR/EU)
// TTFB : 1380ms → 95ms (-93%)
```

```
# Cloudflare Cache Rule ajoutée :
If URI Path matches wildcard "/produit/*"
Then: Edge Cache TTL = 10 minutes, Browser TTL = 0
     Respect Cache-Control from origin = false
```

**Optimisation 2 : Image LCP — Format, taille et preload**

```html
<!-- AVANT : image non optimisée, découverte tardivement -->
<div class="hero" style="background-image: url('/hero-banner.jpg')">
  <!-- Image en CSS = découverte après CSS parsing = Load Delay élevé -->
</div>

<!-- APRÈS : image HTML avec preload + AVIF/WebP + dimensions exactes -->
```

```typescript
// APRÈS : composant Hero Next.js optimisé
import Image from 'next/image';

// Dans le <head> via Next.js metadata : preload de l'image LCP
// next.config.ts
const nextConfig = {
  async headers() {
    return [{
      source: '/',
      headers: [{
        key: 'Link',
        value: '</images/hero-800.avif>; rel=preload; as=image; type="image/avif"; fetchpriority=high',
      }],
    }];
  },
};

// Composant Hero
function HeroBanner() {
  return (
    <div className="hero-container" style={{ position: 'relative', width: '100%', height: '400px' }}>
      <picture>
        <source
          type="image/avif"
          srcSet="/images/hero-400.avif 400w, /images/hero-800.avif 800w"
          sizes="100vw"
        />
        <source
          type="image/webp"
          srcSet="/images/hero-400.webp 400w, /images/hero-800.webp 800w"
          sizes="100vw"
        />
        <img
          src="/images/hero-800.jpg"
          alt="Collection Printemps 2025"
          width="1200"
          height="400"
          loading="eager"
          fetchPriority="high"
          style={{ objectFit: 'cover', width: '100%', height: '100%' }}
        />
      </picture>
    </div>
  );
}
// Image hero : JPEG 640KB → AVIF 148KB (-77%)
// Load Time : 2100ms → 490ms (connexion 4G, 10 Mbps)
```

**Optimisation 3 : CLS — Images produit sans dimensions**

```typescript
// AVANT : images produit dans la grille sans dimensions
function CarteProduit({ produit }) {
  return (
    <div>
      <img src={produit.imageUrl} alt={produit.nom} /> {/* Aucune dimension → CLS */}
      <h3>{produit.nom}</h3>
    </div>
  );
}

// APRÈS : aspect-ratio réservé + Next.js Image
import Image from 'next/image';

function CarteProduit({ produit }) {
  return (
    <div>
      <div style={{ position: 'relative', aspectRatio: '1 / 1' }}>
        <Image
          src={produit.imageUrl}
          alt={produit.nom}
          fill
          style={{ objectFit: 'cover' }}
          sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 25vw"
          loading="lazy"
        />
      </div>
      <h3>{produit.nom}</h3>
    </div>
  );
}
// CLS grille produits : 0,18 → 0,03
```

### Résultats mesurés

| Métrique | Avant | Après | Delta |
|---|---|---|---|
| LCP (lab) | 4,2 s | 1,1 s | -74% |
| LCP (terrain p75) | 4,8 s | 1,4 s | -71% |
| CLS (lab) | 0,18 | 0,04 | -78% |
| TTFB | 1 380 ms | 95 ms | -93% |
| Performance Score | 41 | 91 | +50 pts |

**Impact business (30 jours après) :**
- Taux de conversion mobile : +38%
- Bounce rate : 42% → 28% (-33%)
- Revenue mobile : +40% (corrélation directe avec la baisse du LCP)

### Leçon principale

Le TTFB était la cause racine cachée derrière un LCP catastrophique. L'image était souvent montrée comme coupable par Lighthouse, mais optimiser uniquement l'image sans résoudre le TTFB n'aurait donné qu'une amélioration de 40% au lieu de 74%. **Toujours diagnostiquer les 4 phases du LCP avant d'optimiser.**

---

## Cas 2 — SaaS Dashboard React : TTI 8s → 2,5s

### Contexte

Application SaaS B2B de gestion de projet, React 18 + React Router v6 + Vite, déployée sur AWS CloudFront. 12 routes principales, 8 modales lourdes (éditeur de texte, graphiques), bibliothèques : TipTap (éditeur), Recharts (graphiques), lodash (utilitaires). L'application charge l'ensemble du bundle à chaque ouverture.

### Diagnostic initial

**Lighthouse :**
```
Performance score  : 23 / 100
LCP                : 6,1 s
TTI                : 8,2 s   ← Main bottleneck
TBT                : 2 300 ms
FCP                : 3,8 s
Bundle JS total    : 2,1 MB (parsé = 2× en temps CPU)
```

**Analyse bundle (rollup-plugin-visualizer) :**
```
Bundle breakdown (2,1 MB total, non-gzippé) :
  TipTap + ProseMirror : 680 KB (33%)  — utilisé seulement dans 2 routes
  Recharts + D3        : 420 KB (20%)  — utilisé dans 4 routes sur 12
  lodash (CJS complet) : 290 KB (14%)  — tree shaking impossible
  React + React DOM    : 180 KB (9%)
  React Router         : 95 KB (5%)
  Code applicatif      : 335 KB (16%)
  Autres deps          : 100 KB (5%)
```

### Optimisations appliquées

**Optimisation 1 : Code splitting par route**

```typescript
// AVANT : toutes les routes importées statiquement
import TableauDeBord from './pages/TableauDeBord';
import Projets from './pages/Projets';
import ÉditeurProjet from './pages/ÉditeurProjet';  // Charge TipTap (680KB) pour TOUT LE MONDE
import Rapports from './pages/Rapports';             // Charge Recharts (420KB) pour TOUT LE MONDE
import Membres from './pages/Membres';
import Paramètres from './pages/Paramètres';
// ... 12 imports statiques

// APRÈS : code splitting avec React.lazy
import { lazy, Suspense } from 'react';

const TableauDeBord = lazy(() => import('./pages/TableauDeBord'));
const Projets = lazy(() => import('./pages/Projets'));
const ÉditeurProjet = lazy(() => import('./pages/ÉditeurProjet'));     // TipTap : chargé à la demande
const Rapports = lazy(() => import('./pages/Rapports'));               // Recharts : chargé à la demande
const Membres = lazy(() => import('./pages/Membres'));
const Paramètres = lazy(() => import('./pages/Paramètres'));
const AdminUtilisateurs = lazy(() => import('./pages/AdminUtilisateurs'));
const FacturationAbonnements = lazy(() => import('./pages/FacturationAbonnements'));
const Intégrations = lazy(() => import('./pages/Intégrations'));
const Analytics = lazy(() => import('./pages/Analytics'));
const NotificationsParamètres = lazy(() => import('./pages/NotificationsParamètres'));
const SécuritéParamètres = lazy(() => import('./pages/SécuritéParamètres'));

function AppRoutes() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route path="/" element={<TableauDeBord />} />
        <Route path="/projets" element={<Projets />} />
        <Route path="/projets/:id/editer" element={<ÉditeurProjet />} />
        <Route path="/rapports" element={<Rapports />} />
        {/* ... */}
      </Routes>
    </Suspense>
  );
}

// Résultat : bundle initial 2,1MB → 335KB (code applicatif seul)
// Économie : TipTap (680KB) + Recharts (420KB) = 1,1MB non chargé au démarrage
```

**Optimisation 2 : Lazy loading des 8 modales lourdes**

```typescript
// AVANT : toutes les modales chargées même si jamais ouvertes
import { ModaleÉditeurDescription } from './modales/ModaleÉditeurDescription'; // TipTap
import { ModaleGraphiqueGantt } from './modales/ModaleGraphiqueGantt';           // D3 + Recharts
import { ModaleImportCSV } from './modales/ModaleImportCSV';                     // Papa Parse + logique lourde

// APRÈS : chargement à l'ouverture de la modale
const ModaleÉditeurDescription = lazy(() => import('./modales/ModaleÉditeurDescription'));
const ModaleGraphiqueGantt = lazy(() => import('./modales/ModaleGraphiqueGantt'));
const ModaleImportCSV = lazy(() => import('./modales/ModaleImportCSV'));

function PageProjet({ projet }) {
  const [modaleOuverte, setModaleOuverte] = useState<string | null>(null);

  return (
    <>
      <button onClick={() => setModaleOuverte('description')}>Modifier description</button>
      <button onClick={() => setModaleOuverte('gantt')}>Vue Gantt</button>
      <button onClick={() => setModaleOuverte('import')}>Importer données</button>

      {modaleOuverte && (
        <Suspense fallback={<ModaleChargement />}>
          {modaleOuverte === 'description' && (
            <ModaleÉditeurDescription onClose={() => setModaleOuverte(null)} projet={projet} />
          )}
          {modaleOuverte === 'gantt' && (
            <ModaleGraphiqueGantt onClose={() => setModaleOuverte(null)} projet={projet} />
          )}
          {modaleOuverte === 'import' && (
            <ModaleImportCSV onClose={() => setModaleOuverte(null)} projetId={projet.id} />
          )}
        </Suspense>
      )}
    </>
  );
}
```

**Optimisation 3 : Tree shaking lodash — migration vers lodash-es**

```bash
# AVANT : lodash CJS (290KB, non tree-shakeable)
npm uninstall lodash
npm uninstall @types/lodash

# APRÈS : lodash-es ESM (tree-shakeable)
npm install lodash-es
npm install --save-dev @types/lodash-es
```

```typescript
// AVANT : import destructuré mais toujours CommonJS sous le capot
import { groupBy, sortBy, uniqBy, debounce, throttle, cloneDeep } from 'lodash';
// → 290KB inclus dans le bundle (tree shaking inefficace sur CJS)

// APRÈS : lodash-es ESM → tree shaking fonctionne
import { groupBy, sortBy, uniqBy, debounce, throttle, cloneDeep } from 'lodash-es';
// → Seules les 6 fonctions importées sont incluses → ~12KB au lieu de 290KB

// Vérification dans vite.config.ts : s'assurer que lodash-es n'est pas externalisé
export default defineConfig({
  optimizeDeps: {
    include: ['lodash-es'], // S'assurer que Vite l'optimise correctement
  },
});
```

**Optimisation 4 : Prefetch des routes probables**

```typescript
// Prefetch intelligent basé sur la navigation probable
function NavigationSidebar() {
  const préchargerRoute = (moduleLoader: () => Promise<any>) => {
    // Déclencher le prefetch au survol sans attendre le clic
    moduleLoader();
  };

  return (
    <nav>
      <NavLink
        to="/projets"
        onMouseEnter={() => préchargerRoute(() => import('./pages/Projets'))}
      >
        Projets
      </NavLink>
      <NavLink
        to="/rapports"
        onMouseEnter={() => préchargerRoute(() => import('./pages/Rapports'))}
      >
        Rapports
      </NavLink>
    </nav>
  );
}
```

### Résultats mesurés

| Métrique | Avant | Après | Delta |
|---|---|---|---|
| Bundle initial | 2,1 MB | 380 KB | -82% |
| Bundle gzippé initial | 680 KB | 118 KB | -83% |
| TTI | 8,2 s | 2,5 s | -70% |
| TBT | 2 300 ms | 210 ms | -91% |
| FCP | 3,8 s | 1,4 s | -63% |
| Performance Score | 23 | 88 | +65 pts |

**Impact produit :**
- Time to interactive divisé par 3,3
- Taux d'abandon au chargement : -58%
- NPS utilisateurs : +22 points (corrélation avec les retours qualitatifs sur "la vitesse")

### Leçon principale

Dans une SPA React avec beaucoup de routes et de fonctionnalités, **le code splitting est l'optimisation à plus fort levier**. 82% de réduction du bundle initial en une journée de travail. La règle : tout ce qui n'est pas visible immédiatement à l'ouverture de l'application doit être lazy-loadé.

---

## Cas 3 — Site Média : CLS 0,45 → 0,02

### Contexte

Site d'actualités (type Figaro/L'Équipe), Next.js 13, 8 millions de pages vues/mois, monétisé par publicité display (Google Ad Manager). Le CLS catastrophique est signalé par Google Search Console comme affectant 73% des URLs. L'équipe SEO rapporte une baisse de 15% du trafic organique depuis 3 mois, corrélée à la mise à jour de l'algorithme Page Experience de Google.

### Diagnostic initial

**Core Web Vitals terrain (Search Console) :**
```
CLS : 0,45   ❌ Mauvais (> 0,25) — 73% des URLs
LCP : 3,1 s  ⚠️ À améliorer
INP : 380 ms ⚠️ À améliorer
```

**Analyse détaillée du CLS via web-vitals attribution :**
```
Source des layout shifts identifiés :
1. Images articles sans dimensions     : +0,18 (40% du CLS total)
2. Slots publicitaires GAM             : +0,14 (31%)
3. Fonte titres (FOUT avec Inter)      : +0,08 (18%)
4. Widgets réseaux sociaux dynamiques  : +0,05 (11%)
```

### Optimisations appliquées

**Optimisation 1 : Images articles — dimensions obligatoires**

```typescript
// AVANT : composant article sans dimensions sur les images
function ImageArticle({ src, alt }: { src: string; alt: string }) {
  return <img src={src} alt={alt} className="article-image" />;
  // Navigateur : réserve 0px → reflow quand l'image charge → CLS 0,18
}

// APRÈS : dimensions obligatoires ou aspect-ratio
import Image from 'next/image';

// Option A : dimensions connues depuis le CMS
interface ImageArticleProps {
  src: string;
  alt: string;
  width: number;
  height: number;
}

function ImageArticle({ src, alt, width, height }: ImageArticleProps) {
  return (
    <figure style={{ margin: 0 }}>
      <Image
        src={src}
        alt={alt}
        width={width}
        height={height}
        style={{ width: '100%', height: 'auto' }}
        loading="lazy"
        sizes="(max-width: 768px) 100vw, 740px"
      />
    </figure>
  );
}

// Option B : ratio fixe quand les dimensions ne sont pas dans le CMS
function ImageArticleFill({ src, alt }: { src: string; alt: string }) {
  return (
    <div style={{ position: 'relative', aspectRatio: '16 / 9', width: '100%' }}>
      <Image
        src={src}
        alt={alt}
        fill
        style={{ objectFit: 'cover' }}
        loading="lazy"
        sizes="(max-width: 768px) 100vw, 740px"
      />
    </div>
  );
}
// CLS des images : 0,18 → 0,01
```

**Optimisation 2 : Slots publicitaires Google Ad Manager**

```typescript
// AVANT : slot pub sans hauteur réservée
function SlotPublicitaire({ id }: { id: string }) {
  useEffect(() => {
    // googletag.cmd.push(() => { ... }) — injecte l'iframe après le rendu
  }, []);
  return <div id={id} />;
  // Iframe injectée : 300x250px → pousse tout le contenu → CLS 0,14
}

// APRÈS : dimensions réservées avant injection du script publicitaire
function SlotPublicitaire({
  id,
  largeur,
  hauteur,
  format,
}: {
  id: string;
  largeur: number;
  hauteur: number;
  format: 'leaderboard' | 'rectangle' | 'halfpage';
}) {
  const [chargé, setChargé] = useState(false);

  // Dimensions standards IAB
  const hauteurMinimale = {
    leaderboard: 90,   // 728×90
    rectangle: 250,    // 300×250
    halfpage: 600,     // 300×600
  }[format] ?? hauteur;

  return (
    <div
      id={id}
      style={{
        minHeight: hauteurMinimale,
        width: '100%',
        maxWidth: largeur,
        margin: '0 auto',
        backgroundColor: '#f5f5f5', // Placeholder visuel
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
      aria-label="Espace publicitaire"
    >
      {!chargé && (
        <span style={{ color: '#999', fontSize: '11px' }}>Publicité</span>
      )}
    </div>
  );
}

// Utilisation dans le template article
function ArticleTemplate({ article }) {
  return (
    <article>
      <h1>{article.titre}</h1>

      {/* Slot leaderboard au-dessus du contenu : espace réservé avant script pub */}
      <SlotPublicitaire id="div-gpt-ad-leaderboard" largeur={728} hauteur={90} format="leaderboard" />

      <div className="article-body">{/* contenu */}</div>

      {/* Rectangle inline dans le contenu */}
      <SlotPublicitaire id="div-gpt-ad-rectangle-1" largeur={300} hauteur={250} format="rectangle" />
    </article>
  );
}
// CLS des publicités : 0,14 → 0,01
```

**Optimisation 3 : Polices — éliminer le FOUT**

```css
/* AVANT : font-display:swap → FOUT → CLS 0,08 */
/* La fonte Inter s'affiche après 800ms → le texte se redimensionne */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-regular.woff2') format('woff2');
  font-display: swap;
}

/* APRÈS : font-display:optional + size-adjust sur le fallback */

/* 1. Ajuster le fallback système pour correspondre à Inter */
@font-face {
  font-family: 'Inter-Fallback';
  src: local('Arial');
  /* Ces valeurs sont calculées avec fontaine ou à la main */
  ascent-override: 90.2%;
  descent-override: 22.48%;
  line-gap-override: 0%;
  size-adjust: 107.5%;
}

/* 2. Déclarer Inter avec optional : utilisé seulement si déjà en cache ou très rapide */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-regular.woff2') format('woff2'),
       url('/fonts/inter-regular.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: optional; /* Pas de swap → pas de FOUT → CLS 0 */
}

body {
  /* Inter si disponible, sinon le fallback ajusté, sinon system-ui */
  font-family: 'Inter', 'Inter-Fallback', system-ui, sans-serif;
}
```

```typescript
// APRÈS : preload de la fonte dans Next.js + font-display:optional
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'optional',  // Évite tout layout shift
  preload: true,
  fallback: ['system-ui', '-apple-system'],
});
// CLS des fontes : 0,08 → 0,00
```

### Résultats mesurés

| Métrique | Avant | Après | Delta |
|---|---|---|---|
| CLS (terrain p75) | 0,45 | 0,02 | -96% |
| CLS (lab) | 0,38 | 0,02 | -95% |
| URLs "Mauvaises" Search Console | 73% | 2% | -97% |
| Trafic organique (8 semaines post) | Base | +22% | +22% |

**Impact SEO :**
- Retour aux positions précédentes dans les SERPs Google en 6 semaines
- +22% de trafic organique récupéré sur les 8 semaines suivantes

### Leçon principale

Le CLS est le Core Web Vital le plus sous-estimé par les développeurs mais l'un des plus pénalisants pour le SEO. **Les trois causes représentent presque toujours la totalité du CLS** : images sans dimensions (toujours), publicités sans espace réservé (toujours pour les sites monétisés), polices FOUT (souvent). Corriger ces trois causes en priorité.

---

## Cas 4 — Application B2B : INP 650ms → 140ms

### Contexte

Application de gestion RH (SIRH) en React 18, Vite, TypeScript. L'application gère des exports de fichiers CSV de 50 000 lignes, des tableaux de données triables/filtrables de 10 000 entrées, et un formulaire multi-étapes complexe. Les utilisateurs se plaignent que l'interface "freeze" après chaque interaction : clic sur "Trier", saisie dans les filtres, clic sur "Exporter CSV".

### Diagnostic initial

**Lighthouse :**
```
Performance score : 67 / 100
INP               : 650 ms  ❌ (Mauvais > 500ms)
TBT               : 1 800 ms
LCP               : 2,1 s
CLS               : 0,04
```

**Profiling Chrome DevTools — Main Thread :**

```
Long Tasks identifiées (> 50ms) :
1. "trier()" → onClick bouton colonne   : 340 ms
   └── Quicksort de 10 000 objets + re-render React complet

2. "filtrer()" → onChange input recherche: 280 ms (déclenché à chaque touche)
   └── Filtre linéaire de 10 000 objets + re-render

3. "exporterCSV()" → onClick bouton      : 1 200 ms
   └── Stringify 50 000 lignes en CSV + téléchargement
   └── Bloque l'UI pendant 1,2 secondes

INP p75 : 650ms (pire interaction = exporterCSV → sort → filtre)
Input Delay moyen : 120ms (tâches en cours bloquent la réponse)
Processing Time moyen : 430ms
Presentation Delay moyen : 100ms
```

### Optimisations appliquées

**Optimisation 1 : Débouncer les filtres de recherche**

```typescript
// AVANT : filtre déclenché à chaque touche → long task à chaque keypress
function TableauEmployés({ employés }: { employés: Employé[] }) {
  const [recherche, setRecherche] = useState('');

  const employésFiltés = employés.filter(e =>
    e.nom.toLowerCase().includes(recherche.toLowerCase()) ||
    e.prénom.toLowerCase().includes(recherche.toLowerCase()) ||
    e.email.toLowerCase().includes(recherche.toLowerCase())
  ); // 10 000 objets × 3 comparaisons = long task à chaque touche

  return (
    <div>
      <input
        value={recherche}
        onChange={e => setRecherche(e.target.value)}
        placeholder="Rechercher..."
      />
      <TableauVirtuel données={employésFiltés} />
    </div>
  );
}

// APRÈS : debounce 200ms + useDeferredValue pour le filtrage
import { useDeferredValue, useCallback } from 'react';
import { useMemo } from 'react';

function TableauEmployés({ employés }: { employés: Employé[] }) {
  const [recherche, setRecherche] = useState('');

  // useDeferredValue : le filtrage est différé, l'input reste réactif immédiatement
  const rechercheDouce = useDeferredValue(recherche);

  // useMemo : ne recalculer que si la recherche change réellement
  const employésFiltés = useMemo(() => {
    if (!rechercheDouce) return employés;
    const terme = rechercheDouce.toLowerCase();
    return employés.filter(e =>
      e.nom.toLowerCase().includes(terme) ||
      e.prénom.toLowerCase().includes(terme) ||
      e.email.toLowerCase().includes(terme)
    );
  }, [employés, rechercheDouce]);

  const estEnTransition = recherche !== rechercheDouce;

  return (
    <div>
      <input
        value={recherche}
        onChange={e => setRecherche(e.target.value)}
        placeholder="Rechercher..."
      />
      {estEnTransition && <span>Recherche en cours...</span>}
      <TableauVirtuel
        données={employésFiltés}
        style={{ opacity: estEnTransition ? 0.7 : 1 }}
      />
    </div>
  );
}
```

**Optimisation 2 : Tri des données avec scheduler.yield()**

```typescript
// AVANT : tri synchrone de 10 000 objets = long task de 340ms
async function trierEmployés(employés: Employé[], colonne: keyof Employé, sens: 'asc' | 'desc') {
  return [...employés].sort((a, b) => {
    const va = a[colonne];
    const vb = b[colonne];
    if (va < vb) return sens === 'asc' ? -1 : 1;
    if (va > vb) return sens === 'asc' ? 1 : -1;
    return 0;
  });
  // Array.sort en JS est in-place et synchrone → bloque le main thread
}

// APRÈS : utiliser un Web Worker pour le tri
// workers/tri-worker.ts
self.onmessage = function({ data: { employés, colonne, sens } }) {
  const triés = [...employés].sort((a, b) => {
    const va = a[colonne];
    const vb = b[colonne];
    if (va < vb) return sens === 'asc' ? -1 : 1;
    if (va > vb) return sens === 'asc' ? 1 : -1;
    return 0;
  });
  self.postMessage({ triés });
};

// Hook pour le tri en Web Worker
function useTriWorker() {
  const workerRef = useRef<Worker | null>(null);

  useEffect(() => {
    workerRef.current = new Worker(
      new URL('./workers/tri-worker.ts', import.meta.url),
      { type: 'module' }
    );
    return () => workerRef.current?.terminate();
  }, []);

  const trier = useCallback((employés: Employé[], colonne: keyof Employé, sens: 'asc' | 'desc') => {
    return new Promise<Employé[]>((resolve) => {
      if (!workerRef.current) return resolve(employés);
      workerRef.current.onmessage = ({ data: { triés } }) => resolve(triés);
      workerRef.current.postMessage({ employés, colonne, sens });
    });
  }, []);

  return { trier };
}

// Dans le composant
function TableauEmployés({ employés }) {
  const { trier } = useTriWorker();
  const [données, setDonnées] = useState(employés);
  const [enTri, setEnTri] = useState(false);

  async function gérerTri(colonne: keyof Employé) {
    setEnTri(true);
    const triés = await trier(données, colonne, 'asc');
    setDonnées(triés);
    setEnTri(false);
  }

  return (
    <div>
      <EnTête onTri={gérerTri} />
      {enTri && <BandeauChargement message="Tri en cours..." />}
      <Corps données={données} />
    </div>
  );
}
// Long task tri : 340ms → 0ms (dans le Worker, main thread libre)
```

**Optimisation 3 : Export CSV dans un Web Worker avec scheduler.yield()**

```typescript
// workers/csv-worker.ts — export CSV hors main thread
self.onmessage = async function({ data: { employés } }) {
  const colonnes = ['id', 'nom', 'prénom', 'email', 'département', 'poste', 'salaire', 'dateArrivée'];
  const lignes: string[] = [];

  // En-tête
  lignes.push(colonnes.join(';'));

  // Traitement par batch avec yield pour ne pas bloquer le Worker lui-même
  const BATCH_SIZE = 1000;
  for (let i = 0; i < employés.length; i += BATCH_SIZE) {
    const batch = employés.slice(i, i + BATCH_SIZE);
    for (const emp of batch) {
      const ligne = colonnes.map(col => {
        const val = emp[col as keyof typeof emp];
        // Échapper les valeurs avec virgules/guillemets pour CSV valide
        if (typeof val === 'string' && (val.includes(';') || val.includes('"'))) {
          return `"${val.replace(/"/g, '""')}"`;
        }
        return val ?? '';
      }).join(';');
      lignes.push(ligne);
    }

    // Signaler la progression
    self.postMessage({
      type: 'progress',
      progression: Math.round(((i + BATCH_SIZE) / employés.length) * 100),
    });

    // Petit délai pour ne pas saturer le Worker
    await new Promise(resolve => setTimeout(resolve, 0));
  }

  const csvContent = lignes.join('\n');
  self.postMessage({ type: 'done', csvContent });
};

// Dans le composant React
function BoutonExportCSV({ employés }: { employés: Employé[] }) {
  const [progression, setProgression] = useState(0);
  const [exporting, setExporting] = useState(false);

  async function exporterCSV() {
    setExporting(true);
    setProgression(0);

    const worker = new Worker(new URL('./workers/csv-worker.ts', import.meta.url), { type: 'module' });

    const csvContent = await new Promise<string>((resolve) => {
      worker.onmessage = ({ data }) => {
        if (data.type === 'progress') setProgression(data.progression);
        if (data.type === 'done') {
          worker.terminate();
          resolve(data.csvContent);
        }
      };
      worker.postMessage({ employés });
    });

    // Télécharger le fichier (uniquement cette partie dans le main thread)
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `employés-${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);

    setExporting(false);
    setProgression(100);
  }

  return (
    <div>
      <button onClick={exporterCSV} disabled={exporting}>
        {exporting ? `Export en cours... ${progression}%` : 'Exporter CSV'}
      </button>
      {exporting && (
        <div role="progressbar" aria-valuenow={progression} style={{ width: `${progression}%` }} />
      )}
    </div>
  );
}
// Long task export CSV : 1 200ms main thread → 0ms (entièrement dans Worker)
```

**Optimisation 4 : Virtualisation du tableau (10 000 lignes → 20 lignes rendues)**

```typescript
// Utiliser react-virtual ou @tanstack/react-virtual
import { useVirtualizer } from '@tanstack/react-virtual';

function TableauVirtuel({ données }: { données: Employé[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: données.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Hauteur estimée de chaque ligne : 50px
    overscan: 5,            // Pré-rendre 5 lignes hors viewport de chaque côté
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      {/* Conteneur virtuel à la hauteur totale (10 000 × 50px = 500 000px) */}
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map((item) => (
          <div
            key={item.index}
            data-index={item.index}
            ref={virtualizer.measureElement} // Mesure réelle pour les hauteurs variables
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${item.start}px)`,
            }}
          >
            <LigneEmployé employé={données[item.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
// Nœuds DOM rendus : 10 000 → ~25 (virtualisés) → re-renders plus rapides
```

### Résultats mesurés

| Métrique | Avant | Après | Delta |
|---|---|---|---|
| INP (terrain p75) | 650 ms | 140 ms | -78% |
| Long task tri | 340 ms | ~0 ms | -100% |
| Long task filtre | 280 ms | < 50 ms | -82% |
| Long task export CSV | 1 200 ms | ~5 ms | -99% |
| TBT | 1 800 ms | 180 ms | -90% |
| Performance Score | 67 | 94 | +27 pts |

**Impact utilisateurs :**
- Taux de satisfaction (CSAT) : +34 points
- Tickets de support liés à la lenteur : -71%
- Adoption de la fonctionnalité export CSV : +85% (les utilisateurs évitaient l'export car il gelait l'UI)

### Leçon principale

**Les Web Workers sont la solution pour les calculs intensifs côté client.** L'erreur classique est de mettre du code lourd dans des `useEffect` ou des event handlers React, qui s'exécutent tous sur le main thread. Tout traitement dépassant 50ms qui ne nécessite pas d'accès au DOM doit être déporté dans un Worker. Les gains sont systématiquement de 80 à 100% sur la réduction du long task correspondant.

---

## Synthèse Comparative

| Cas | Contexte | Métrique principale | Amélioration | Levier principal |
|---|---|---|---|---|
| E-commerce | LCP 4,2s → 1,1s | LCP | -74% | CDN edge + AVIF + preload |
| SaaS Dashboard | TTI 8s → 2,5s | TTI / Bundle | -70% TTI, -82% bundle | Code splitting par route |
| Site Média | CLS 0,45 → 0,02 | CLS | -96% | Dimensions images + slots pub |
| Application B2B | INP 650ms → 140ms | INP | -78% | Web Workers + virtualisation |

**Trois règles universelles émergent de ces cas :**

1. **Diagnostiquer avant d'optimiser** : chaque cas aurait pu être traité dans la mauvaise direction sans un diagnostic précis via DevTools et les données CrUX terrain.

2. **Corriger la cause racine** : dans le Cas 1, l'image semblait coupable mais le TTFB de 1,4s était le vrai problème. Dans le Cas 4, le problème n'était pas React mais les long tasks JavaScript sur le main thread.

3. **Mesurer l'impact** : toute optimisation doit être validée par une métrique chiffrée avant/après sur les données terrain (CrUX), pas seulement en laboratoire (Lighthouse). Un score Lighthouse parfait ne garantit pas de bonnes métriques terrain sur des appareils réels.
