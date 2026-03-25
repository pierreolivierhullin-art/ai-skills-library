# Frontend Architecture -- Components, State, CSS & Performance

Reference complete pour l'architecture frontend moderne : patterns de composants, gestion d'etat, architecture CSS, Core Web Vitals et progressive enhancement. Complete reference for modern frontend architecture: component patterns, state management, CSS architecture, Core Web Vitals, and progressive enhancement.

---

## 1. Component Patterns

### Atomic Component Hierarchy

Implementer la hierarchie de composants selon le modele atomic design adapte aux frameworks modernes (React, Vue, Svelte, Solid).

**Regles generales / General Rules:**
- Chaque composant doit avoir une seule responsabilite clairement definie.
- Les composants doivent etre composables : privilegier la composition a l'heritage.
- Typer strictement les props avec TypeScript (interfaces explicites, pas de `any`).
- Utiliser le pattern `asChild` ou `as` pour le polymorphisme de rendu sans wrapper inutile.
- Documenter chaque composant public dans Storybook avec des stories pour chaque variante et etat.

### Compound Components Pattern

Le pattern compound components permet de creer des composants complexes flexibles et accessibles en distribuant l'etat via le contexte.

```tsx
// Compound component pattern with Context
import { createContext, useContext, useState, ReactNode } from "react";

interface TabsContextType {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

function useTabs() {
  const context = useContext(TabsContext);
  if (!context) throw new Error("useTabs must be used within <Tabs>");
  return context;
}

// Root component manages state
function Tabs({ defaultValue, children }: { defaultValue: string; children: ReactNode }) {
  const [activeTab, setActiveTab] = useState(defaultValue);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div role="tablist">{children}</div>
    </TabsContext.Provider>
  );
}

// Sub-component accesses shared state via context
function Tab({ id, children }: { id: string; children: ReactNode }) {
  const { activeTab, setActiveTab } = useTabs();
  return (
    <button
      role="tab"
      aria-selected={activeTab === id}
      tabIndex={activeTab === id ? 0 : -1}
      onClick={() => setActiveTab(id)}
    >
      {children}
    </button>
  );
}

function Panel({ id, children }: { id: string; children: ReactNode }) {
  const { activeTab } = useTabs();
  if (activeTab !== id) return null;
  return <div role="tabpanel">{children}</div>;
}

// Attach sub-components to root
Tabs.Tab = Tab;
Tabs.Panel = Panel;

// Usage:
// <Tabs defaultValue="general">
//   <Tabs.Tab id="general">General</Tabs.Tab>
//   <Tabs.Tab id="security">Security</Tabs.Tab>
//   <Tabs.Panel id="general">General settings...</Tabs.Panel>
//   <Tabs.Panel id="security">Security settings...</Tabs.Panel>
// </Tabs>
```

**Avantages / Benefits:**
- L'API est declarative et auto-documentee.
- Les sous-composants communiquent via le contexte, pas via le drilling de props.
- L'accessibilite (roles ARIA, keyboard navigation) est integree au niveau du composant.
- Le consommateur a le controle total de la structure et du placement.

### Headless Component Pattern

Separer la logique d'interaction de la presentation pour permettre un restyling complet.

**Approche hooks / Hooks Approach:**
```tsx
// useToggle.ts - headless logic
function useToggle(defaultOpen = false) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const toggle = () => setIsOpen((prev) => !prev);
  const open = () => setIsOpen(true);
  const close = () => setIsOpen(false);

  return {
    isOpen,
    toggle,
    open,
    close,
    triggerProps: {
      "aria-expanded": isOpen,
      onClick: toggle,
    },
    contentProps: {
      hidden: !isOpen,
    },
  };
}

// Usage with any visual style
function Accordion({ title, children }: { title: string; children: ReactNode }) {
  const { triggerProps, contentProps, isOpen } = useToggle();
  return (
    <div>
      <button {...triggerProps} className="accordion-trigger">
        {title}
        <ChevronIcon direction={isOpen ? "up" : "down"} />
      </button>
      <div {...contentProps} className="accordion-content">
        {children}
      </div>
    </div>
  );
}
```

**Libraries headless recommandees / Recommended Headless Libraries:**

| Library | Framework | Components | Approach |
|---|---|---|---|
| **Radix UI** | React | ~30 primitives | Unstyled, a11y-first |
| **Headless UI** | React, Vue | ~10 primitives | Unstyled, Tailwind-friendly |
| **Ark UI** | React, Vue, Solid | ~40 primitives | State machines (Zag.js) |
| **React Aria** | React | ~40 hooks | Adobe, hooks-based |
| **Melt UI** | Svelte | ~30 primitives | Svelte-native |
| **Kobalte** | Solid | ~30 primitives | Solid-native |

### Render Props & Slot Pattern

**Render Props** permettent au composant parent de controler le rendu d'une partie du composant enfant.

```tsx
// Render prop pattern for custom rendering
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => ReactNode;
  renderEmpty?: () => ReactNode;
}

function List<T>({ items, renderItem, renderEmpty }: ListProps<T>) {
  if (items.length === 0) return renderEmpty?.() ?? <p>No items</p>;
  return <ul>{items.map((item, i) => <li key={i}>{renderItem(item, i)}</li>)}</ul>;
}
```

**Slot Pattern (Vue style, applicable React):**
```tsx
// Slot-based composition
interface CardProps {
  header?: ReactNode;
  footer?: ReactNode;
  children: ReactNode;
}

function Card({ header, footer, children }: CardProps) {
  return (
    <div className="card">
      {header && <div className="card-header">{header}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}
```

### Polymorphic Components (asChild Pattern)

Permettre au consommateur de changer l'element HTML racine sans wrapper supplementaire.

```tsx
import { Slot } from "@radix-ui/react-slot";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
  variant?: "primary" | "secondary";
}

function Button({ asChild, variant = "primary", className, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button";
  return <Comp className={cn("btn", `btn-${variant}`, className)} {...props} />;
}

// Usage as button:
// <Button variant="primary">Click</Button>

// Usage as link:
// <Button asChild variant="primary">
//   <a href="/page">Navigate</a>
// </Button>
```

---

## 2. State Management

### Taxonomie des etats / State Taxonomy

Classifier chaque piece d'etat dans la bonne categorie avant de choisir un outil de gestion.

| Category | Examples | Location | Tool |
|---|---|---|---|
| **UI State** | modal open, sidebar collapsed, hover | Component-local | useState, useReducer |
| **Server State** | API data, user profile, list items | Cache (remote source) | TanStack Query, SWR |
| **URL State** | page, filters, sort, search query | URL | URL params, nuqs |
| **Form State** | field values, validation, dirty state | Form instance | React Hook Form, Conform |
| **Global UI State** | theme, locale, notifications | App-wide | Zustand, Jotai, Context |
| **Cross-tab State** | auth status, real-time sync | Browser-wide | Broadcast Channel, signals |

### Server State -- TanStack Query

TanStack Query (anciennement React Query) est le standard pour la gestion du server state. Il encapsule le fetching, le caching, la synchronisation et les mutations.

```tsx
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

// Query with automatic caching and refetching
function useUsers() {
  return useQuery({
    queryKey: ["users"],
    queryFn: () => fetch("/api/users").then((r) => r.json()),
    staleTime: 5 * 60 * 1000, // 5 minutes before refetch
    gcTime: 30 * 60 * 1000,   // 30 minutes in garbage collection
  });
}

// Mutation with optimistic update
function useUpdateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (user: User) =>
      fetch(`/api/users/${user.id}`, {
        method: "PATCH",
        body: JSON.stringify(user),
      }),
    onMutate: async (newUser) => {
      await queryClient.cancelQueries({ queryKey: ["users"] });
      const previous = queryClient.getQueryData(["users"]);
      queryClient.setQueryData(["users"], (old: User[]) =>
        old.map((u) => (u.id === newUser.id ? { ...u, ...newUser } : u))
      );
      return { previous };
    },
    onError: (_err, _user, context) => {
      queryClient.setQueryData(["users"], context?.previous);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
}
```

### Global State -- Zustand

Zustand fournit une solution minimaliste pour le global state sans boilerplate.

```tsx
import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

interface UIStore {
  sidebarOpen: boolean;
  theme: "light" | "dark";
  toggleSidebar: () => void;
  setTheme: (theme: "light" | "dark") => void;
}

const useUIStore = create<UIStore>()(
  devtools(
    persist(
      (set) => ({
        sidebarOpen: true,
        theme: "light",
        toggleSidebar: () =>
          set((state) => ({ sidebarOpen: !state.sidebarOpen })),
        setTheme: (theme) => set({ theme }),
      }),
      { name: "ui-store" }
    )
  )
);

// Usage in component -- only re-renders when selected slice changes
function Sidebar() {
  const isOpen = useUIStore((state) => state.sidebarOpen);
  const toggle = useUIStore((state) => state.toggleSidebar);
  // ...
}
```

### Atomic State -- Jotai

Jotai utilise un modele d'atomes pour un state granulaire et composable, ideal pour eviter les re-renders inutiles.

```tsx
import { atom, useAtom, useAtomValue, useSetAtom } from "jotai";

// Primitive atoms
const countAtom = atom(0);
const doubleCountAtom = atom((get) => get(countAtom) * 2); // derived

// Async atom (combines with server state)
const userAtom = atom(async () => {
  const response = await fetch("/api/user");
  return response.json();
});

// Usage
function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const doubled = useAtomValue(doubleCountAtom);
  // only re-renders when countAtom changes
}
```

### Signals (TC39 Proposal & Framework Implementations)

Les signals representent le futur du state management reactif, avec des implementations dans Preact, Solid, Angular et une proposition TC39 en cours.

**Principes / Principles:**
- Fine-grained reactivity : seuls les composants dependant d'un signal specifique sont re-rendus.
- Pas de selectors ni de memoization manuelle.
- Performance superieure pour les UIs complexes avec de nombreuses mises a jour granulaires.

```tsx
// Preact Signals example
import { signal, computed, effect } from "@preact/signals-react";

const count = signal(0);
const doubled = computed(() => count.value * 2);

// Automatic fine-grained updates -- no re-render of parent
function Counter() {
  return <button onClick={() => count.value++}>Count: {count}</button>;
}
```

### State Management Decision Flowchart

```
Is the data from a remote API?
|-- Yes -> TanStack Query / SWR
+-- No -> Is it in the URL?
    |-- Yes -> URL search params (nuqs)
    +-- No -> Is it form data?
        |-- Yes -> React Hook Form / Conform
        +-- No -> Is it used by multiple components?
            |-- No -> useState / useReducer
            +-- Yes -> How many consumers?
                |-- 2-3 nearby -> React Context + useReducer
                +-- Many across the app -> Zustand or Jotai
```

---

## 3. CSS Architecture

### CSS Modules

CSS Modules fournissent un scoping automatique des classes CSS au niveau du composant, sans runtime cost.

```css
/* Button.module.css */
.root {
  display: inline-flex;
  align-items: center;
  padding: var(--ds-spacing-sm) var(--ds-spacing-md);
  border-radius: var(--ds-border-radius-md);
  font-family: var(--ds-font-family-body);
  transition: background-color var(--ds-duration-fast) var(--ds-ease-out);
}

.primary {
  background: var(--ds-color-action-primary);
  color: var(--ds-color-text-inverse);
}

.primary:hover {
  background: var(--ds-color-action-primary-hover);
}
```

```tsx
import styles from "./Button.module.css";
import { cn } from "@/lib/utils";

function Button({ variant = "primary", className, ...props }) {
  return <button className={cn(styles.root, styles[variant], className)} {...props} />;
}
```

### Tailwind CSS

Tailwind CSS est une approche utility-first qui accelere le developpement en eliminant le context-switching entre HTML et CSS.

**Configuration avec design tokens / Configuration with Design Tokens:**
```javascript
// tailwind.config.ts
import type { Config } from "tailwindcss";
import tokens from "./dist/tailwind/theme";

export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: tokens.colors,
      spacing: tokens.spacing,
      fontFamily: tokens.fontFamily,
      borderRadius: tokens.borderRadius,
    },
  },
  plugins: [
    require("@tailwindcss/container-queries"),
    require("tailwindcss-animate"),
  ],
} satisfies Config;
```

**Bonnes pratiques Tailwind / Tailwind Best Practices:**
- Extraire les combinaisons repetees en composants, pas en classes `@apply` (qui defait l'interet utility-first).
- Utiliser `cn()` (clsx + tailwind-merge) pour la composition conditionnelle de classes.
- Configurer le theme depuis les design tokens pour la coherence.
- Utiliser les container queries (`@container`) pour le responsive au niveau du composant.

### CSS-in-JS Zero-Runtime (Vanilla Extract, Panda CSS)

Privilegier les solutions zero-runtime qui generent du CSS statique au build time.

**Vanilla Extract:**
```typescript
// button.css.ts
import { style, styleVariants } from "@vanilla-extract/css";
import { vars } from "./theme.css";

export const root = style({
  display: "inline-flex",
  alignItems: "center",
  padding: `${vars.spacing.sm} ${vars.spacing.md}`,
  borderRadius: vars.borderRadius.md,
  transition: `background-color ${vars.duration.fast} ${vars.ease.out}`,
});

export const variants = styleVariants({
  primary: { background: vars.color.action.primary, color: vars.color.text.inverse },
  secondary: { background: vars.color.action.secondary, color: vars.color.text.primary },
});
```

**Panda CSS:**
```tsx
import { css } from "../styled-system/css";

function Button({ variant = "primary", children }) {
  return (
    <button
      className={css({
        display: "inline-flex",
        padding: "sm md",
        borderRadius: "md",
        bg: variant === "primary" ? "action.primary" : "action.secondary",
        color: variant === "primary" ? "text.inverse" : "text.primary",
        _hover: { bg: "action.primaryHover" },
      })}
    >
      {children}
    </button>
  );
}
```

### CSS Layers (@layer)

Les CSS Layers (CSS Cascade Layers) permettent de controler explicitement l'ordre de la cascade, eliminant les problemes de specificite.

```css
/* Define layer order -- first declared = lowest priority */
@layer reset, tokens, base, components, utilities, overrides;

@layer reset {
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
  }
}

@layer tokens {
  :root {
    --ds-color-primary: #0066ff;
    --ds-spacing-md: 16px;
  }
}

@layer base {
  body {
    font-family: var(--ds-font-family-body);
    color: var(--ds-color-text-primary);
  }
}

@layer components {
  .button { /* ... */ }
  .card { /* ... */ }
}

@layer utilities {
  .sr-only { /* ... */ }
  .flex { display: flex; }
}

@layer overrides {
  /* Page-specific overrides with highest priority */
}
```

### Container Queries

Les container queries permettent le responsive design au niveau du composant (pas du viewport), essentiel pour les design systems.

```css
/* Define a container */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* Respond to container size, not viewport */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

@container card (max-width: 399px) {
  .card {
    display: flex;
    flex-direction: column;
  }
}

/* Container query units */
.card-title {
  font-size: clamp(1rem, 3cqi, 1.5rem); /* cqi = container query inline */
}
```

**Quand utiliser container queries vs media queries / When to Use:**
- **Container queries** : composants reutilisables dans des contextes de taille differente (sidebar, main content, modal). Design system components.
- **Media queries** : layout global de la page, changements structurels majeurs (navigation mobile vs desktop).

---

## 4. Core Web Vitals Optimization

### Les 3 metriques / The 3 Metrics (2024-2026)

| Metric | Full Name | Measures | Good | Needs Improvement | Poor |
|---|---|---|---|---|---|
| **LCP** | Largest Contentful Paint | Loading performance | < 2.5s | 2.5s - 4.0s | > 4.0s |
| **INP** | Interaction to Next Paint | Responsiveness | < 200ms | 200ms - 500ms | > 500ms |
| **CLS** | Cumulative Layout Shift | Visual stability | < 0.1 | 0.1 - 0.25 | > 0.25 |

**Note :** INP (Interaction to Next Paint) a remplace FID (First Input Delay) comme metrique officielle en mars 2024. INP mesure la latence de TOUTES les interactions (pas seulement la premiere), ce qui est un standard plus exigeant.

### Optimiser LCP (Largest Contentful Paint)

LCP mesure le temps de rendu du plus grand element visible dans le viewport (generalement une image hero, un titre principal ou un bloc de texte).

**Strategies d'optimisation / Optimization Strategies:**

1. **Optimiser le critical rendering path:**
   - Inliner le CSS critique (above-the-fold) dans le `<head>`.
   - Precharger les ressources critiques : `<link rel="preload" as="image" href="hero.webp">`.
   - Eliminer les render-blocking resources (CSS/JS non critiques).

2. **Optimiser les images:**
   - Utiliser les formats modernes : AVIF (meilleure compression) avec fallback WebP.
   - Implementer le responsive images pattern avec `<picture>` et `srcset`.
   - Specifier `width` et `height` sur les `<img>` pour reserver l'espace.
   - Utiliser `loading="lazy"` sur les images below-the-fold, `fetchpriority="high"` sur le LCP element.
   - Utiliser un CDN d'images avec transformation on-the-fly (Cloudinary, imgix, Vercel Image).

3. **Optimiser les fonts:**
   - Utiliser `font-display: swap` ou `font-display: optional` pour eviter le FOIT.
   - Precharger les fonts critiques : `<link rel="preload" as="font" crossorigin>`.
   - Subsetter les fonts pour inclure uniquement les caracteres utilises.
   - Considerer les system font stacks pour eliminer le font loading.

```html
<head>
  <!-- Preload critical resources -->
  <link rel="preload" as="image" href="/hero.avif" type="image/avif">
  <link rel="preload" as="font" href="/fonts/Inter-Variable.woff2"
        type="font/woff2" crossorigin>

  <!-- Inline critical CSS -->
  <style>/* critical above-the-fold CSS */</style>

  <!-- Defer non-critical CSS -->
  <link rel="stylesheet" href="/styles.css" media="print"
        onload="this.media='all'">
</head>
```

### Optimiser INP (Interaction to Next Paint)

INP mesure la latence entre une interaction utilisateur (click, tap, key press) et la prochaine frame peinte. Il capture le pire cas (p98) parmi toutes les interactions de la session.

**Strategies d'optimisation / Optimization Strategies:**

1. **Reduire le travail du main thread:**
   - Decomposer les taches longues (> 50ms) avec `requestIdleCallback`, `scheduler.yield()` ou `setTimeout(fn, 0)`.
   - Deplacer les calculs lourds dans des Web Workers.
   - Eviter le layout thrashing (lire puis ecrire le DOM en boucle).

2. **Optimiser les event handlers:**
   - Debounce les input handlers (search, resize).
   - Utiliser `requestAnimationFrame` pour les mises a jour visuelles.
   - Eviter les re-renders React inutiles (memo, useMemo, useCallback, selectors Zustand).

3. **Optimiser le rendering:**
   - Virtualiser les longues listes (TanStack Virtual, react-window).
   - Utiliser `content-visibility: auto` pour le lazy rendering du contenu hors viewport.
   - Implementer des optimistic updates pour un feedback instantane.

```tsx
// Break up long tasks with yield
async function processLargeDataset(items: Item[]) {
  const CHUNK_SIZE = 100;
  for (let i = 0; i < items.length; i += CHUNK_SIZE) {
    const chunk = items.slice(i, i + CHUNK_SIZE);
    processChunk(chunk);
    // Yield to the main thread between chunks
    await scheduler.yield();
  }
}

// Optimistic update pattern for instant feedback
function LikeButton({ postId }: { postId: string }) {
  const [optimisticLiked, setOptimisticLiked] = useState(false);

  async function handleLike() {
    setOptimisticLiked(true); // Instant visual feedback
    try {
      await api.likePost(postId);
    } catch {
      setOptimisticLiked(false); // Rollback on error
    }
  }

  return <button onClick={handleLike}>{optimisticLiked ? "Liked" : "Like"}</button>;
}
```

### Optimiser CLS (Cumulative Layout Shift)

CLS mesure la somme des shifts de layout inattendus pendant toute la duree de vie de la page. Un layout shift est inattendu quand il n'est pas declenche par une interaction utilisateur dans les 500ms precedentes.

**Strategies d'optimisation / Optimization Strategies:**

1. **Reserver l'espace pour les medias:**
   - Toujours specifier `width` et `height` ou `aspect-ratio` sur les images et videos.
   - Utiliser le pattern `aspect-ratio` CSS pour les conteneurs d'images dynamiques.

2. **Gerer les fonts:**
   - Utiliser `font-display: optional` pour eliminer le FOUT (Flash of Unstyled Text) shift.
   - Utiliser `size-adjust` pour matcher la taille du fallback font avec la web font.

3. **Eviter les injections dynamiques:**
   - Ne pas injecter de contenu au-dessus du contenu existant (bannieres, bars de notification).
   - Reserver l'espace pour les ads et embeds avec `min-height`.
   - Utiliser CSS `contain: layout` pour isoler les sections dynamiques.

```css
/* Reserve space for images */
.hero-image {
  aspect-ratio: 16 / 9;
  width: 100%;
  object-fit: cover;
}

/* Prevent layout shifts from dynamic content */
.ad-slot {
  min-height: 250px; /* Reserve space */
  contain: layout;   /* Isolate layout */
}

/* Font size adjustment to prevent FOUT shift */
@font-face {
  font-family: "Inter";
  src: url("/fonts/Inter.woff2") format("woff2");
  font-display: optional;
  size-adjust: 100%;
}
```

---

## 5. View Transitions API

### Page Transitions

L'API View Transitions permet des transitions fluides entre les etats de la page ou entre les pages (MPA et SPA) sans JavaScript d'animation complexe.

**SPA View Transitions:**
```typescript
// Wrap state changes in startViewTransition
function navigateTo(url: string) {
  if (!document.startViewTransition) {
    // Fallback for unsupported browsers
    updateDOM(url);
    return;
  }

  document.startViewTransition(async () => {
    await updateDOM(url);
  });
}
```

**CSS pour les transitions / Transition CSS:**
```css
/* Default crossfade (applied automatically) */
::view-transition-old(root) {
  animation: fade-out 0.3s ease-out;
}
::view-transition-new(root) {
  animation: fade-in 0.3s ease-in;
}

/* Named transitions for specific elements */
.hero-image {
  view-transition-name: hero;
}

::view-transition-old(hero) {
  animation: slide-out-left 0.3s ease-out;
}
::view-transition-new(hero) {
  animation: slide-in-right 0.3s ease-in;
}

/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation-duration: 0.01ms !important;
  }
}
```

**MPA View Transitions (cross-document):**
```css
/* Enable in CSS for cross-document transitions */
@view-transition {
  navigation: auto;
}
```

**Integration avec les frameworks / Framework Integration:**
- **Next.js** : support experimental via `next/navigation` et le hook `useViewTransitionState`.
- **Astro** : support natif via `<ViewTransitions />` component.
- **Nuxt** : support via `<NuxtPage>` avec la prop `transition`.

---

## 6. Progressive Enhancement

### Principes / Principles

Construire les interfaces en couches, chaque couche enrichissant l'experience sans etre requise.

**Couche 1 -- HTML semantique (baseline):**
- Le contenu est accessible et navigable sans CSS ni JavaScript.
- Les formulaires fonctionnent avec des soumissions classiques (form action POST).
- Les liens naviguent vers des pages completes.

**Couche 2 -- CSS (presentation):**
- Le layout, la typographie, les couleurs et les animations enrichissent l'experience.
- Les fonctionnalites CSS modernes sont utilisees avec `@supports` pour les fallbacks.

**Couche 3 -- JavaScript (interaction):**
- Les interactions riches (SPA navigation, optimistic updates, real-time) enrichissent l'experience.
- Le contenu essentiel reste accessible si JavaScript echoue.

### Feature Detection Pattern

```css
/* CSS feature detection */
@supports (container-type: inline-size) {
  .component-wrapper {
    container-type: inline-size;
  }
}

@supports not (container-type: inline-size) {
  /* Fallback with media queries */
  @media (min-width: 640px) {
    .component { /* ... */ }
  }
}

/* :has() selector with fallback */
@supports selector(:has(*)) {
  .form-field:has(:invalid) {
    border-color: var(--ds-color-error);
  }
}
```

```typescript
// JavaScript feature detection
if ("startViewTransition" in document) {
  document.startViewTransition(() => updateDOM());
} else {
  updateDOM();
}

if ("scheduler" in window && "yield" in scheduler) {
  await scheduler.yield();
} else {
  await new Promise((r) => setTimeout(r, 0));
}
```

### Responsive Design Strategy

**Mobile-first baseline:**
```css
/* Base styles = mobile */
.grid {
  display: flex;
  flex-direction: column;
  gap: var(--ds-spacing-md);
}

/* Enhance for larger viewports */
@media (min-width: 768px) {
  .grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Container queries for component-level responsiveness */
@container (min-width: 400px) {
  .card {
    flex-direction: row;
  }
}
```

---

## 7. Performance Monitoring & Budgets

### Performance Budgets

Definir des budgets de performance comme des contraintes de design.

| Metric | Budget | Justification |
|---|---|---|
| **LCP** | < 2.5s (p75) | Google ranking factor |
| **INP** | < 200ms (p75) | Perceived responsiveness |
| **CLS** | < 0.1 (p75) | Visual stability |
| **Total JS** | < 200KB (gzipped) | Parse/eval time on mobile |
| **Total CSS** | < 50KB (gzipped) | Render-blocking resource |
| **First Load** | < 100KB (JS+CSS) | Initial page load budget |
| **Bundle per route** | < 50KB (JS) | Code splitting target |

### Monitoring Tools

| Tool | Type | Data Source | Use Case |
|---|---|---|---|
| **Chrome UX Report (CrUX)** | Field data | Real users (Chrome) | Production monitoring |
| **Lighthouse** | Lab data | Simulated | Development audit |
| **WebPageTest** | Lab data | Real devices | Deep analysis |
| **Sentry Performance** | Field data | Real users (all) | Error + perf correlation |
| **Vercel Analytics** | Field data | Real users | Next.js/Vercel projects |
| **SpeedCurve** | Lab + Field | Synthetic + real | Continuous monitoring |

### CI Performance Gates

Integrer les checks de performance dans le pipeline CI pour prevenir les regressions.

```yaml
# Lighthouse CI configuration
# lighthouserc.json
{
  "ci": {
    "collect": {
      "url": ["http://localhost:3000/", "http://localhost:3000/products"],
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "interactive": ["error", { "maxNumericValue": 3500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-byte-weight": ["warning", { "maxNumericValue": 500000 }]
      }
    },
    "upload": {
      "target": "lhci",
      "serverBaseUrl": "https://lhci.example.com"
    }
  }
}
```

---

## References

- web.dev, *Core Web Vitals* -- https://web.dev/vitals/
- web.dev, *Interaction to Next Paint (INP)* -- https://web.dev/inp/
- web.dev, *View Transitions API* -- https://developer.chrome.com/docs/web-platform/view-transitions
- MDN, *CSS Container Queries* -- https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
- MDN, *CSS Cascade Layers* -- https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Cascade_layers
- TanStack Query documentation -- https://tanstack.com/query
- Zustand documentation -- https://zustand-demo.pmnd.rs/
- Radix UI documentation -- https://www.radix-ui.com
- Vanilla Extract documentation -- https://vanilla-extract.style
- Tailwind CSS documentation -- https://tailwindcss.com/docs
- Addy Osmani, *Image Optimization* (2021)
