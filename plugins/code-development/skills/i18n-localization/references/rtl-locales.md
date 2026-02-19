# RTL et Langues Bidirectionnelles — Arabe, Hébreu et CSS Logique

## Overview

Référence complète sur le support des langues RTL (de droite à gauche) dans les applications web. Couvre les propriétés CSS logiques, le plugin Tailwind RTL, l'algorithme bidi Unicode, les polices arabes et hébraïques, les chiffres arabes-indiens, les tests Playwright et les détails d'implémentation pour un rendu pixel-perfect en arabe, hébreu et persan. Appliquer ces patterns pour ajouter le support RTL sans régression LTR.

---

## CSS Logical Properties — Référence Complète

### Principes des propriétés logiques

Les propriétés CSS logiques remplacent les références directionnelles physiques (left, right, top, bottom) par des références logiques relatives au sens d'écriture du document.

```
Axe inline : la direction du texte
  → En LTR (gauche à droite) : inline-start = left, inline-end = right
  → En RTL (droite à gauche) : inline-start = right, inline-end = left

Axe block : perpendiculaire au texte
  → Toujours : block-start = top, block-end = bottom (pour les scripts horizontaux)
```

### Tableau de correspondance complet — physique vers logique

| Propriété physique | Propriété logique | Comportement RTL |
|---|---|---|
| `margin-left` | `margin-inline-start` | Devient margin-right en RTL |
| `margin-right` | `margin-inline-end` | Devient margin-left en RTL |
| `margin-top` | `margin-block-start` | Inchangé (même sens vertical) |
| `margin-bottom` | `margin-block-end` | Inchangé |
| `padding-left` | `padding-inline-start` | Devient padding-right en RTL |
| `padding-right` | `padding-inline-end` | Devient padding-left en RTL |
| `padding-top` | `padding-block-start` | Inchangé |
| `padding-bottom` | `padding-block-end` | Inchangé |
| `border-left` | `border-inline-start` | Bascule en RTL |
| `border-right` | `border-inline-end` | Bascule en RTL |
| `left` | `inset-inline-start` | Bascule en RTL |
| `right` | `inset-inline-end` | Bascule en RTL |
| `top` | `inset-block-start` | Inchangé |
| `bottom` | `inset-block-end` | Inchangé |
| `text-align: left` | `text-align: start` | Droite en RTL |
| `text-align: right` | `text-align: end` | Gauche en RTL |
| `float: left` | `float: inline-start` | Bascule en RTL |
| `float: right` | `float: inline-end` | Bascule en RTL |
| `width` | `inline-size` | Identique (longueur de la ligne) |
| `height` | `block-size` | Identique (hauteur du bloc) |
| `min-width` | `min-inline-size` | Identique |
| `max-width` | `max-inline-size` | Identique |
| `border-top-left-radius` | `border-start-start-radius` | Bascule en RTL |
| `border-top-right-radius` | `border-start-end-radius` | Bascule en RTL |
| `border-bottom-left-radius` | `border-end-start-radius` | Bascule en RTL |
| `border-bottom-right-radius` | `border-end-end-radius` | Bascule en RTL |

### Exemples pratiques — Migration physique vers logique

```css
/* ❌ Propriétés physiques — ne s'adaptent pas au RTL */
.carte {
  padding-left: 1.5rem;
  padding-right: 1rem;
  margin-left: auto;
  border-left: 3px solid #3b82f6;
  text-align: left;
}

.icone-fleche {
  left: 1rem;
  position: absolute;
}

/* ✅ Propriétés logiques — s'adaptent automatiquement au RTL */
.carte {
  padding-inline-start: 1.5rem;
  padding-inline-end: 1rem;
  margin-inline-start: auto;
  border-inline-start: 3px solid #3b82f6;
  text-align: start;
}

.icone-fleche {
  inset-inline-start: 1rem;
  position: absolute;
}
```

```css
/* Shorthand logique — padding et margin */
.composant {
  /* padding-inline: 1rem = padding-inline-start + padding-inline-end */
  padding-inline: 1rem;

  /* padding-block: 0.5rem = padding-block-start + padding-block-end */
  padding-block: 0.5rem;

  /* Équivalent logique de : padding: 0.5rem 1rem */
}

/* Inset logique — position absolue */
.badge {
  position: absolute;
  inset-block-start: 0.5rem;   /* top: 0.5rem */
  inset-inline-end: 0.5rem;    /* right en LTR, left en RTL */
}
```

---

## Tailwind CSS RTL — Plugin et Modifiers

### Installer et configurer le support RTL

Depuis Tailwind CSS v3.3, les modifiers `rtl:` et `ltr:` sont disponibles nativement sans plugin externe.

```javascript
// tailwind.config.ts — Configuration pour le support RTL
import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};

export default config;
```

### Classes Tailwind logiques — à utiliser par défaut

```html
<!-- ❌ Classes physiques — ne s'adaptent pas au RTL -->
<div class="ml-4 mr-2 pl-4 text-left border-l-4">
  <span class="left-2">...</span>
</div>

<!-- ✅ Classes logiques — s'adaptent automatiquement -->
<div class="ms-4 me-2 ps-4 text-start border-s-4">
  <span class="start-2">...</span>
</div>
```

```
Correspondances Tailwind logique :
  ms-*  = margin-inline-start (ex: ms-4 = margin-inline-start: 1rem)
  me-*  = margin-inline-end
  ps-*  = padding-inline-start
  pe-*  = padding-inline-end
  start-* = inset-inline-start (pour position absolute/fixed)
  end-*   = inset-inline-end
  text-start = text-align: start
  text-end   = text-align: end
  border-s-* = border-inline-start
  border-e-* = border-inline-end
  rounded-s-* = border-start-start-radius + border-end-start-radius
  rounded-e-* = border-start-end-radius + border-end-end-radius
```

### Modifiers rtl: et ltr: — cas spéciaux

Utiliser `rtl:` uniquement pour les cas où la propriété logique équivalente n'existe pas.

```html
<!-- Cas 1 : icônes directionnelles — inverser en RTL -->
<svg class="rtl:scale-x-[-1]" ...>...</svg>

<!-- Cas 2 : gradient directionnel -->
<div class="bg-gradient-to-r rtl:bg-gradient-to-l from-blue-500 to-purple-500">
  ...
</div>

<!-- Cas 3 : animation de slide depuis la droite -->
<div class="translate-x-full ltr:-translate-x-full rtl:translate-x-full">
  ...
</div>

<!-- Cas 4 : propriété non couverte par les classes logiques -->
<div class="ltr:origin-left rtl:origin-right">
  Élément avec transform-origin directionnel
</div>
```

### Stratégie de migration — audit des classes physiques

```bash
# Identifier toutes les classes physiques à migrer dans les fichiers TSX/HTML
grep -r --include="*.tsx" --include="*.html" \
  -E 'class(Name)?=.*\b(ml|mr|pl|pr|text-left|text-right|left-|right-|border-l|border-r|rounded-l|rounded-r)\b' \
  src/ \
  | grep -v 'rtl:\|ltr:' # Exclure celles déjà traitées
```

```
Priorité de migration :
  1. Priorité haute (visible immédiatement en RTL) :
     - text-left / text-right → text-start / text-end
     - ml-* / mr-* → ms-* / me-*
     - pl-* / pr-* → ps-* / pe-*
     - border-l / border-r → border-s / border-e

  2. Priorité moyenne (layout) :
     - left-* / right-* → start-* / end-*
     - float-left / float-right → float-start / float-end
     - rounded-l-* / rounded-r-* → rounded-s-* / rounded-e-*

  3. Cas spéciaux (traiter avec rtl:) :
     - Icônes directionnelles (flèches, chevrons)
     - Gradients directionnels
     - Animations de slide
```

---

## Algorithme Bidi Unicode — Texte Mixte AR/EN

### Comprendre le problème bidi

Dans un texte mixte arabe/anglais, le navigateur applique l'algorithme bidi Unicode pour déterminer la direction de chaque segment. Sans isolation, des artefacts visuels apparaissent.

```html
<!-- Problème : "Prix : 100€" en arabe — le € et le nombre peuvent se retrouver à gauche -->
<p dir="rtl">السعر: 100€</p>

<!-- Solution 1 : unicode-bidi avec isolation -->
<p dir="rtl" style="unicode-bidi: isolate;">السعر: 100€</p>

<!-- Solution 2 : bidi isolate (recommandé en HTML5) -->
<p dir="rtl">السعر: <bdi>100€</bdi></p>
```

### Caractères de contrôle bidi Unicode

| Caractère | Code | Nom | Usage |
|---|---|---|---|
| LRM | U+200E | Left-to-Right Mark | Forcer LTR après du texte RTL |
| RLM | U+200F | Right-to-Left Mark | Forcer RTL après du texte LTR |
| LRE | U+202A | Left-to-Right Embedding | Début d'une section LTR (déprécié) |
| RLE | U+202B | Right-to-Left Embedding | Début d'une section RTL (déprécié) |
| LRI | U+2066 | Left-to-Right Isolate | Isoler une section LTR (recommandé) |
| RLI | U+2067 | Right-to-Left Isolate | Isoler une section RTL (recommandé) |
| FSI | U+2068 | First Strong Isolate | Isoler selon le premier caractère fort |
| PDI | U+2069 | Pop Directional Isolate | Fermer LRI/RLI/FSI |
| ALM | U+061C | Arabic Letter Mark | Marquer du texte arabe dans contexte LTR |

### Isolation bidi en CSS et JavaScript

```css
/* Isolation bidi pour les éléments avec texte mixte */
.texte-mixte {
  unicode-bidi: isolate;  /* Équivalent HTML de <bdi> */
}

/* Pour les éléments enfants dans un container RTL */
.prix-en-chiffres {
  unicode-bidi: isolate;
  direction: ltr;  /* Les chiffres et montants toujours LTR */
}
```

```typescript
// Utilité en JavaScript — ajouter des marques directionnelles
function ajouterMarqueBidi(texte: string, direction: 'ltr' | 'rtl'): string {
  const LRI = '\u2066';  // Left-to-Right Isolate
  const RLI = '\u2067';  // Right-to-Left Isolate
  const PDI = '\u2069';  // Pop Directional Isolate

  const debut = direction === 'ltr' ? LRI : RLI;
  return `${debut}${texte}${PDI}`;
}

// Formater un montant en préservant l'ordre LTR dans un texte arabe
function formaterMontantArabeRTL(montant: number, locale = 'ar'): string {
  const montantFormate = new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: 'SAR',
  }).format(montant);

  // Isoler le montant en LTR pour qu'il s'affiche correctement dans le texte RTL
  return ajouterMarqueBidi(montantFormate, 'ltr');
}
```

---

## Polices Arabes — Configuration Google Fonts

### Polices arabes recommandées

| Police | Usage | Caractéristiques |
|---|---|---|
| Cairo | Applications SaaS, UI | Géométrique, moderne, excellente lisibilité |
| Tajawal | Dashboards, données | Condensée, adaptée aux tableaux |
| Noto Naskh Arabic | Corps de texte long | Serif, haute lisibilité en texte courant |
| Noto Sans Arabic | Interface générale | Sans-serif équilibré, poids multiples |
| IBM Plex Arabic | Applications techniques | Monospace-adjacent, chiffres alignés |

### Configurer les polices pour multi-script

```typescript
// app/layout.tsx — Polices multi-script avec Next.js Font Optimization
import { Cairo, Inter } from 'next/font/google';

// Police latine — pour FR, EN, ES...
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-latin',
  display: 'swap',
});

// Police arabe — pour AR
const cairo = Cairo({
  subsets: ['arabic'],
  variable: '--font-arabic',
  weight: ['400', '500', '600', '700'],
  display: 'swap',
});

export default function RootLayout({
  children,
  params: { locale },
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  const estRTL = locale === 'ar' || locale === 'he';

  return (
    <html
      lang={locale}
      dir={estRTL ? 'rtl' : 'ltr'}
      // Appliquer les deux variables CSS — la bonne est activée via CSS
      className={`${inter.variable} ${cairo.variable}`}
    >
      <body>{children}</body>
    </html>
  );
}
```

```css
/* globals.css — Sélectionner la bonne police selon la direction */
:root {
  font-family: var(--font-latin), system-ui, sans-serif;
}

/* Activer la police arabe quand dir="rtl" */
[dir="rtl"] {
  font-family: var(--font-arabic), 'Noto Sans Arabic', sans-serif;
}

/* Certains éléments gardent toujours la police latine (chiffres, code) */
[dir="rtl"] code,
[dir="rtl"] pre,
[dir="rtl"] .chiffres-latins {
  font-family: var(--font-latin), monospace;
  direction: ltr;
  unicode-bidi: isolate;
}
```

### Prévention FOUT/FOIT pour les polices multi-script

```typescript
// Précharger les polices critiques dans les métadonnées
export const metadata: Metadata = {
  // Next.js gère automatiquement le preload via next/font
  // Mais ajouter manuellement si besoin de contrôle fin
};

// Pour les locales RTL, précharger explicitement la police arabe
// dans le <head> via un lien preload
function PolicesPrechargees({ locale }: { locale: string }) {
  if (locale !== 'ar') return null;

  return (
    <>
      <link
        rel="preload"
        href="/fonts/cairo-400.woff2"
        as="font"
        type="font/woff2"
        crossOrigin="anonymous"
      />
      <link
        rel="preload"
        href="/fonts/cairo-600.woff2"
        as="font"
        type="font/woff2"
        crossOrigin="anonymous"
      />
    </>
  );
}
```

---

## Chiffres Arabes-Indiens vs Chiffres Latins

### Comprendre les systèmes de chiffres

L'arabe utilise deux systèmes de chiffres selon le contexte :
- **Chiffres arabes-indiens** (٠١٢٣٤٥٦٧٨٩) : utilisés au Moyen-Orient
- **Chiffres arabes latins** (0123456789) : utilisés au Maghreb et dans les contextes internationaux

### Intl.NumberFormat — Contrôler le système de chiffres

```typescript
// Système de chiffres par sous-locale
const exemples = [
  { locale: 'ar', label: 'Arabe (Moyen-Orient)', systeme: 'arab' },
  { locale: 'ar-MA', label: 'Arabe marocain', systeme: 'latn' },
  { locale: 'ar-EG', label: 'Arabe égyptien', systeme: 'arab' },
  { locale: 'ar-SA', label: 'Arabe saoudien', systeme: 'arab' },
];

const nombre = 1234567.89;

// Affichage avec chiffres arabes-indiens (Moyen-Orient)
const formatArabe = new Intl.NumberFormat('ar-SA').format(nombre);
console.log(formatArabe); // ١٬٢٣٤٬٥٦٧٫٨٩

// Forcer les chiffres latins avec numberingSystem
const formatArabeLatin = new Intl.NumberFormat('ar-SA', {
  numberingSystem: 'latn',
} as Intl.NumberFormatOptions).format(nombre);
console.log(formatArabeLatin); // 1,234,567.89

// Chiffres hébreux
const formatHebreu = new Intl.NumberFormat('he').format(nombre);
console.log(formatHebreu); // 1,234,567.89 (hébreu utilise les chiffres latins)
```

```typescript
// Conversion manuelle — chiffres latins vers arabes-indiens
function convertirChiffresArabesIndiens(texte: string): string {
  const chiffresArabes = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  return texte.replace(/[0-9]/g, (c) => chiffresArabes[parseInt(c)]);
}

// Conversion inverse — arabes-indiens vers latins
function convertirChiffresLatins(texte: string): string {
  return texte.replace(/[٠-٩]/g, (c) =>
    String(c.charCodeAt(0) - '٠'.charCodeAt(0))
  );
}
```

---

## Formulaires RTL — Placeholders, Select et Inputs

### Alignement des placeholders et champs

```css
/* ❌ Le placeholder s'aligne à gauche en RTL si non corrigé */
input::placeholder {
  /* Pas de direction explicite — hérite du contexte */
}

/* ✅ Aligner explicitement le placeholder en RTL */
[dir="rtl"] input::placeholder {
  text-align: right;
  direction: rtl;
}

/* Champ email/URL/téléphone — toujours LTR même en RTL */
[dir="rtl"] input[type="email"],
[dir="rtl"] input[type="url"],
[dir="rtl"] input[type="tel"] {
  direction: ltr;
  text-align: right; /* Aligner à droite dans le champ RTL */
}

/* Input number — toujours LTR */
[dir="rtl"] input[type="number"] {
  direction: ltr;
}
```

### Select — Chevron de droite à gauche

```css
/* ✅ Repositionner le chevron du select en RTL */
[dir="rtl"] select {
  /* Supprimer l'apparence native pour contrôler le positionnement */
  appearance: none;
  background-image: url("data:image/svg+xml,..."); /* Chevron SVG */
  background-position: left 0.75rem center; /* Gauche en RTL */
  padding-left: 2.5rem;  /* Espace pour le chevron à gauche */
  padding-right: 0.75rem;
}
```

```typescript
// Composant Select RTL-aware avec Radix UI
import * as Select from '@radix-ui/react-select';
import { useLocale } from 'next-intl';

function SelectLocale({ valeur, onChangement, options }: SelectProps) {
  const locale = useLocale();
  const estRTL = ['ar', 'he', 'fa', 'ur'].includes(locale);

  return (
    <Select.Root value={valeur} onValueChange={onChangement}>
      <Select.Trigger dir={estRTL ? 'rtl' : 'ltr'} className="...">
        <Select.Value />
        <Select.Icon>
          {/* L'icône chevron doit être à gauche en RTL */}
          <ChevronDown />
        </Select.Icon>
      </Select.Trigger>
      <Select.Portal>
        {/* Le portail hérite automatiquement de dir du document */}
        <Select.Content dir={estRTL ? 'rtl' : 'ltr'}>
          <Select.Viewport>
            {options.map((opt) => (
              <Select.Item key={opt.valeur} value={opt.valeur}>
                <Select.ItemText>{opt.libelle}</Select.ItemText>
              </Select.Item>
            ))}
          </Select.Viewport>
        </Select.Content>
      </Select.Portal>
    </Select.Root>
  );
}
```

---

## Images et Icônes Directionnelles

### Miroir des icônes directionnelles

```typescript
// Composant d'icône RTL-aware
import { useLocale } from 'next-intl';

const ICONES_DIRECTIONNELLES = new Set([
  'arrow-left', 'arrow-right',
  'chevron-left', 'chevron-right',
  'back', 'forward',
  'send', 'reply',
  'next', 'previous',
]);

interface IconeProps {
  nom: string;
  className?: string;
}

function Icone({ nom, className = '' }: IconeProps) {
  const locale = useLocale();
  const estRTL = ['ar', 'he', 'fa', 'ur'].includes(locale);

  // Appliquer le miroir horizontal uniquement pour les icônes directionnelles
  const classesMiroir =
    estRTL && ICONES_DIRECTIONNELLES.has(nom) ? 'scale-x-[-1]' : '';

  return (
    <span className={`inline-block ${classesMiroir} ${className}`}>
      {/* Icône SVG ici */}
    </span>
  );
}
```

### Sticky elements et positionnement des dropdowns

```css
/* Sticky sidebar — changer de côté en RTL */
.sidebar {
  position: sticky;
  inset-block-start: 0;    /* top: 0 */
  inset-inline-start: 0;   /* left en LTR, right en RTL */
}

/* Scrollbar — positionner à gauche en RTL (navigateurs modernes) */
[dir="rtl"] {
  /* Chrome/Edge — déjà géré automatiquement avec dir="rtl" */
  /* Firefox — nécessite une configuration explicite */
}
```

```typescript
// Positionnement des dropdowns avec Radix UI en RTL
import * as Popover from '@radix-ui/react-popover';

function MenuDeroulant({ enfants, declencheur }: MenuProps) {
  const locale = useLocale();
  const estRTL = ['ar', 'he', 'fa', 'ur'].includes(locale);

  return (
    <Popover.Root>
      <Popover.Trigger>{declencheur}</Popover.Trigger>
      <Popover.Portal>
        <Popover.Content
          // Aligner le dropdown du bon côté selon la direction
          align={estRTL ? 'start' : 'end'}
          side="bottom"
          dir={estRTL ? 'rtl' : 'ltr'}
        >
          {enfants}
        </Popover.Content>
      </Popover.Portal>
    </Popover.Root>
  );
}
```

---

## Tests RTL avec Playwright

### Assertions sur l'attribut dir

```typescript
// tests/rtl/layout.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Support RTL — Arabe', () => {
  test.beforeEach(async ({ page }) => {
    // Naviguer vers la version arabe de l'application
    await page.goto('/ar');
  });

  test('le document a dir="rtl"', async ({ page }) => {
    const html = page.locator('html');
    await expect(html).toHaveAttribute('dir', 'rtl');
    await expect(html).toHaveAttribute('lang', 'ar');
  });

  test('la sidebar est à droite en RTL', async ({ page }) => {
    const sidebar = page.locator('[data-testid="sidebar"]');
    const boutonPrincipal = page.locator('[data-testid="bouton-principal"]');

    const boxSidebar = await sidebar.boundingBox();
    const boxBouton = await boutonPrincipal.boundingBox();

    // En RTL, la sidebar doit être à droite du bouton principal
    expect(boxSidebar!.x).toBeGreaterThan(boxBouton!.x + boxBouton!.width);
  });

  test('le texte arabe s'aligne à droite', async ({ page }) => {
    const paragraphe = page.locator('p').first();
    const direction = await paragraphe.evaluate((el) =>
      window.getComputedStyle(el).direction
    );
    expect(direction).toBe('rtl');
  });

  test('les icônes directionnelles sont inversées', async ({ page }) => {
    const iconeRetour = page.locator('[data-testid="icone-retour"]');
    const transform = await iconeRetour.evaluate((el) =>
      window.getComputedStyle(el).transform
    );
    // scaleX(-1) appliqué — la matrice de transformation reflète l'inversion
    expect(transform).toContain('-1');
  });
});
```

### Comparaison par screenshot entre LTR et RTL

```typescript
// tests/rtl/screenshot-comparison.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Screenshot RTL vs LTR', () => {
  const pages = [
    { chemin: '/', nom: 'accueil' },
    { chemin: '/tableau-de-bord', nom: 'dashboard' },
    { chemin: '/produits', nom: 'produits' },
  ];

  pages.forEach(({ chemin, nom }) => {
    test(`${nom} — LTR snapshot de référence`, async ({ page }) => {
      await page.goto(`/fr${chemin}`);
      await page.waitForLoadState('networkidle');

      // Snapshot de référence LTR
      await expect(page).toHaveScreenshot(`${nom}-ltr.png`, {
        fullPage: true,
        threshold: 0.02,  // 2% de tolérance pour les anti-alias
      });
    });

    test(`${nom} — RTL sans régression LTR`, async ({ page }) => {
      await page.goto(`/ar${chemin}`);
      await page.waitForLoadState('networkidle');

      // Snapshot RTL — valider visuellement l'inversion du layout
      await expect(page).toHaveScreenshot(`${nom}-rtl.png`, {
        fullPage: true,
        threshold: 0.02,
      });
    });
  });
});
```

```typescript
// playwright.config.ts — Configuration multi-locale
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  projects: [
    {
      name: 'chromium-ltr',
      use: { browserName: 'chromium' },
      testMatch: '**/ltr/**',
    },
    {
      name: 'chromium-rtl',
      use: {
        browserName: 'chromium',
        // Forcer la locale arabe au niveau du navigateur
        locale: 'ar-SA',
        extraHTTPHeaders: { 'Accept-Language': 'ar' },
      },
      testMatch: '**/rtl/**',
    },
  ],
  // Dossier de stockage des screenshots de référence
  snapshotDir: './tests/snapshots',
  updateSnapshots: 'none',  // 'none' en CI, 'all' pour mise à jour
});
```

---

## Performance — Chargement Multi-Script

### Stratégie de chargement des polices

```typescript
// Charger conditionnellement les polices selon la locale
// Éviter de charger les polices arabes pour les locales LTR

async function getPolicesParLocale(locale: string) {
  const LOCALES_ARABES = ['ar', 'fa', 'ur'];
  const LOCALES_HEBRAIQUES = ['he'];

  if (LOCALES_ARABES.includes(locale)) {
    // Charger uniquement les subsets arabes
    const { Cairo } = await import('next/font/google');
    return Cairo({ subsets: ['arabic'], variable: '--font-rtl' });
  }

  if (LOCALES_HEBRAIQUES.includes(locale)) {
    const { Noto_Sans_Hebrew } = await import('next/font/google');
    return Noto_Sans_Hebrew({ subsets: ['hebrew'], variable: '--font-rtl' });
  }

  return null; // Pas de police RTL pour les locales latines
}
```

```
Recommandations de performance pour les polices multi-script :

  1. Utiliser next/font — optimisation automatique (preload, font-display, self-hosting)
  2. Subsets ciblés — ne télécharger que les glyphes de la locale courante
  3. Variable fonts — un seul fichier pour tous les poids (Cairo Variable)
  4. font-display: swap — afficher le texte immédiatement avec la police système
  5. Précharger uniquement la police critique (weight 400, 600)
  6. Cache-Control: immutable — les polices sont des assets versionnés
```
