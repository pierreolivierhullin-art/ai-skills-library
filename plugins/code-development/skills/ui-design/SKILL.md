---
name: ui-design
description: >
  Expert guide for UI design, design systems, visual design, component libraries, CSS architecture,
  design tokens, typography, color theory, Figma workflows, shadcn/ui, Radix, Tailwind, accessibility
  compliance, Core Web Vitals, and atomic design. Invoke this skill proactively whenever the user
  is working on visual interfaces, components, or design systems — even if framed as 'styling',
  'frontend', or 'theming'. If pixels, components, tokens, or visual consistency are in scope,
  this skill applies.
version: 1.0.0
last_updated: 2026-03-25
---

# UI Design & Design Systems

Expert-level guidance for user interface design, design system architecture, CSS architecture, component development, accessibility compliance, and frontend performance.

## Overview

Ce skill couvre la dimension **UI** de la discipline design : design systems, design tokens, architecture CSS, bibliothèques de composants, accessibilité et performance perçue. Il s'appuie sur les standards modernes (2024-2026) : design tokens W3C, container queries, View Transitions API, CSS layers, Interaction to Next Paint (INP), et conformité à l'European Accessibility Act (EAA 2025).

Un design system mature réduit le temps de développement de 30 à 50% et garantit la cohérence visuelle à l'échelle. L'accessibilité intégrée dès la conception évite les coûts de remédiation et les risques juridiques croissants sous l'EAA.

## When This Skill Applies

- **Design systems** : création ou évolution d'un design system, définition de design tokens, architecture de composants (atomic design), gouvernance et versioning.
- **Architecture CSS** : choix entre CSS Modules, Tailwind, CSS-in-JS, CSS Layers, BEM ; organisation du code de style à grande échelle.
- **Composants UI** : implémentation de composants headless (Radix, Ark UI), compound components, bibliothèques (shadcn/ui, MUI, Chakra).
- **Accessibilité** : audit WCAG 2.1/2.2, implémentation ARIA, conformité EAA/RGAA/Section 508, navigation clavier, lecteurs d'écran.
- **Performance UI** : Core Web Vitals (LCP, INP, CLS), skeleton screens, View Transitions API, optimisation des assets.
- **Figma/Storybook** : workflow design-to-code, documentation de composants, visual regression testing, design tokens pipeline.

## Core Principles

### Principle 1 — Design Tokens as Single Source of Truth
Les design tokens sont le contrat entre design et code. Architecture à trois niveaux : global tokens → alias tokens (sémantiques) → component tokens. Propager via Style Dictionary vers web, iOS, Android depuis une source unique (Figma Variables ou JSON W3C).

### Principle 2 — Accessibility as Foundation, Not Afterthought
Intégrer l'accessibilité dès la conception. Viser WCAG 2.2 AA comme minimum, anticiper l'EAA (juin 2025). Tester avec des technologies d'assistance réelles (VoiceOver, NVDA, JAWS), pas uniquement des outils automatisés. L'accessibilité améliore l'expérience pour tous.

### Principle 3 — Progressive Enhancement & Resilience
Construire d'abord pour le scénario le plus contraint (connexion lente, ancien navigateur, AT), puis enrichir progressivement. Utiliser les fonctionnalités CSS modernes (container queries, `:has()`, `@layer`) avec des fallbacks. Le contenu essentiel doit fonctionner sans JavaScript.

### Principle 4 — Performance is UX
Optimiser pour les Core Web Vitals : LCP < 2.5s, INP < 200ms, CLS < 0.1. La performance perçue (skeleton screens, optimistic updates, View Transitions API) est aussi importante que la performance réelle.

### Principle 5 — Component-Driven Architecture
Concevoir des composants isolés, composables et documentables. Adopter l'atomic design (atoms → molecules → organisms → templates → pages). Chaque composant : autonome, testable dans Storybook, versionné.

### Principle 6 — Separation of Logic and Presentation
Utiliser les composants headless (Radix UI, Headless UI, Ark UI) pour séparer la logique d'interaction du style. Permet le restyling complet sans modifier la logique, et l'accessibilité est intrinsèque aux primitives headless.

## Key Frameworks & Methods

### Design System Architecture

Structure en couches :
1. **Foundation Layer** : design tokens (couleurs, typographie, spacing, elevation, motion, breakpoints).
2. **Core Components (Atoms)** : Button, Input, Icon, Badge, Typography, Spacer.
3. **Composite Components (Molecules)** : SearchBar, FormField, Card, NavItem.
4. **Pattern Components (Organisms)** : Header, Sidebar, DataTable, Modal, Form.
5. **Templates & Layouts** : PageShell, DashboardLayout, AuthLayout.

### CSS Architecture Decision Matrix

| Approach | Best For | Scoping | Runtime Cost | DX |
|---|---|---|---|---|
| **CSS Modules** | App components | Auto-scoped | Zero | Bon |
| **Tailwind CSS** | Rapid prototyping, utility-first | Class-based | Zero | Très bon |
| **Vanilla Extract / Panda CSS** | Typed styles, tokens | Auto-scoped | Zero (build-time) | Bon |
| **CSS Layers (@layer)** | Large systems, cascade control | Explicit layers | Zero | Moyen |
| **BEM** | Legacy, convention-based | Convention | Zero | Moyen |

Privilégier les solutions zero-runtime (Tailwind, CSS Modules, Vanilla Extract) par rapport aux CSS-in-JS runtime (styled-components, Emotion) pour les apps sensibles à la performance.

### Accessibility Compliance Framework

- **Niveau A** (minimum légal) : alt text, navigation clavier, pas de pièges clavier, bypass blocks.
- **Niveau AA** (cible EAA) : contraste 4.5:1 (texte), 3:1 (large texte), redimensionnement 200%, reflow, focus visible, messages d'erreur.
- **Niveau AAA** (excellence) : contraste 7:1, timing ajustable, pas d'animation auto.

## Decision Guide

### Design System Decision Tree

```
1. Taille de l'équipe et nombre de produits ?
   |-- 1 produit, équipe < 5 → Library légère (Shadcn/UI)
   |-- 2-5 produits, équipe < 20 → Design system interne (Storybook + tokens)
   +-- > 5 produits, équipe > 20 → Design system full (gouvernance, versioning, multi-platform)

2. Quelle approche CSS ?
   |-- Prototypage rapide, petite équipe → Tailwind CSS
   |-- App complexe, design system strict → CSS Modules ou Vanilla Extract
   +-- Multi-framework → Design tokens + CSS custom properties

3. Niveau d'accessibilité ?
   |-- Produit EU (EAA 2025) → WCAG 2.2 AA obligatoire
   |-- Produit US (Section 508) → WCAG 2.1 AA obligatoire
   +-- Tout produit → WCAG 2.2 AA comme baseline
```

### State Management Decision

| Situation | Solution recommandée |
|---|---|
| UI state local | `useState` / `useReducer` |
| Server state (API data) | TanStack Query / SWR |
| Global state simple | Zustand / Jotai |
| URL state | URL search params (nuqs) |
| Form state | React Hook Form / Conform |

## Common Patterns & Anti-Patterns

### Patterns recommandés

- **Compound Components** : `<Tabs>`, `<Tabs.List>`, `<Tabs.Panel>` pour la flexibilité et l'accessibilité intrinsèque.
- **Headless UI** : séparer logique et présentation (Radix UI, Headless UI, Ark UI). Restyling complet sans modifier la logique.
- **Design Token Pipeline** : Figma Variables → JSON (W3C) → Style Dictionary → CSS custom properties + Swift/Kotlin.
- **Progressive Disclosure** : révéler la complexité graduellement. Options avancées uniquement à la demande.
- **Skeleton Screens** : structure visible pendant le chargement pour améliorer la performance perçue (LCP).
- **View Transitions** : navigations fluides entre pages/états, remplaçant les animations JavaScript coûteuses.

### Anti-patterns critiques

- **Div Soup** : `<div>` partout au lieu de la sémantique HTML (`<nav>`, `<main>`, `<article>`). Détectable via Lighthouse.
- **Z-Index Wars** : z-index arbitraires. Utiliser un système de layers géré par tokens.
- **Inaccessible Custom Components** : recréer `<select>`, `<dialog>`, `<datepicker>` sans ARIA roles et keyboard navigation. Utiliser des primitives headless.
- **Layout Shift Negligence** : ne pas réserver l'espace pour images, fonts, contenus dynamiques → CLS élevé.
- **Props Drilling for Theming** : passer les variables de thème en props au lieu de CSS custom properties ou ThemeProvider.

## Implementation Workflow

### Phase 1 — Design Foundation (1-2 semaines)
1. Définir les design tokens (couleurs, typographie, spacing, elevation, motion) en format W3C.
2. Établir la grille responsive et la stratégie de breakpoints (mobile-first, container queries).
3. Créer la hiérarchie de composants (atomic design inventory).
4. Configurer Figma avec les librairies de composants et les variables synchronisées aux tokens.

### Phase 2 — Component Development (2-4 semaines)
5. Implémenter les atoms dans Storybook avec variantes, états et stories d'accessibilité.
6. Construire les molecules et organismes en composant les atoms.
7. Implémenter l'accessibilité intrinsèque : ARIA roles, keyboard navigation, focus management, live regions.
8. Écrire les tests : visual regression (Chromatic/Percy), interaction tests (Testing Library), axe-core assertions.
9. Documenter chaque composant : props API, guidelines d'usage, do/don't, exemples de code.

### Phase 3 — Integration & Optimization (1-2 semaines)
10. Assembler les templates à partir des composants du design system.
11. Optimiser les Core Web Vitals : lazy loading, code splitting, font optimization, image optimization (AVIF/WebP).
12. Implémenter les View Transitions pour les navigations inter-pages.
13. Valider la conformité WCAG 2.2 AA (audit automatisé + manuel).

### Phase 4 — Governance & Scale (ongoing)
14. Processus de contribution au design system (RFC, review, merge).
15. Automatiser : a11y checks en CI, visual regression, design token lint.
16. Versionner le design system (semver) et publier un changelog.
17. Mesurer l'adoption (analytics d'usage des composants) et planifier des revues trimestrielles.

## Maturity Model

### Niveau 1 — Ad-hoc
- CSS non structuré, incohérences visuelles, accessibilité ignorée, aucun composant réutilisable.
- **Indicateurs** : design system adoption 0%, accessibility score < 30%.

### Niveau 2 — Consistant
- Bibliothèque de composants de base (boutons, inputs, typographie) dans Figma et code.
- Conventions visuelles établies, CSS structuré (Tailwind ou Modules).
- **Indicateurs** : design system adoption 20-40%, Core Web Vitals partiellement verts.

### Niveau 3 — Design System
- Design system complet avec design tokens W3C, Storybook documenté, pipeline Figma-to-code.
- Composants headless accessibles, atomic design structuré, tests de régression visuelle en CI.
- **Indicateurs** : adoption 40-70%, accessibility score 60-80%, Core Web Vitals verts.

### Niveau 4 — Governed
- Design system gouverné avec processus de contribution (RFC, review, changelog semver).
- Accessibilité WCAG 2.2 AA validée, tests avec AT réelles.
- **Indicateurs** : adoption 70-90%, accessibility score > 85%.

### Niveau 5 — Multi-platform
- Design system multi-plateforme (web, mobile, desktop) avec tokens propagés automatiquement.
- Conformité EAA/WCAG AAA sur les parcours critiques, innovation UX continue.
- **Indicateurs** : adoption > 90%, accessibility score > 95%, Core Web Vitals top 10%.

## Checklist Accessibilité WCAG

| Critère | Niveau | Vérifié |
|---|---|---|
| Contraste texte | AA (4.5:1) | ☐ |
| Contraste grands textes | AA (3:1) | ☐ |
| Navigation clavier | A | ☐ |
| Focus visible | AA | ☐ |
| Textes alternatifs images | A | ☐ |
| Labels des formulaires | A | ☐ |
| Messages d'erreur | A | ☐ |
| Hiérarchie des titres | A | ☐ |
| Landmarks ARIA | AA | ☐ |
| Responsive (320px min) | AA | ☐ |

## Additional Resources

- **[Design Systems](./references/design-systems.md)** — Atomic design, architecture design tokens W3C, pipeline Figma-to-code, Storybook avancé, gouvernance.
- **[Accessibility](./references/accessibility.md)** — WCAG 2.1/2.2 complet, ARIA roles, outils de test (axe, Lighthouse), EAA 2025, RGAA, Section 508.
- **[Frontend Architecture](./references/frontend-architecture.md)** — Component patterns, state management, CSS architecture, Core Web Vitals, View Transitions API.

## See Also

- **ux-research** (`code-development/ux-research`) — Recherche utilisateur, usability testing, personas et user journeys (la dimension UX de cette discipline)
- **accessibility** (`code-development/accessibility`) — Guide dédié WCAG, ARIA et inclusive design
- **frontend-frameworks** (`code-development/frontend-frameworks`) — React, Next.js, SSR/SSG patterns
- **web-performance** (`code-development/web-performance`) — Core Web Vitals, bundle optimization, caching
- **design-tools** (`productivite/design-tools`) — Figma, Canva, Adobe Express pour les non-designers
