---
name: ui-ux
description: This skill should be used when the user asks about "UI design", "UX research", "design system", "component library", "accessibility", "WCAG", "responsive design", "design tokens", "Figma", "Storybook", "atomic design", "frontend architecture", "CSS architecture", "Core Web Vitals", "design d'interface", "recherche UX", "système de design", "bibliothèque de composants", "accessibilité", "design responsive", "jetons de design", "architecture frontend", "Tailwind CSS", "CSS-in-JS", "styled-components", "shadcn/ui", "Radix UI", "Material UI", "Chakra UI", "animation", "Framer Motion", "micro-interactions", "wireframe", "prototype", "maquette", "user testing", "tests utilisateurs", "heuristiques de Nielsen", "information architecture", "dark mode", "theming", "mobile-first", or needs guidance on user interface design, user experience, and design system implementation.
version: 1.1.0
last_updated: 2026-02
---

# UI/UX Design, Design Systems & Accessibility

Expert-level guidance for user interface design, user experience research, design system architecture, accessibility compliance, and modern frontend implementation.

## Overview

Ce skill couvre l'ensemble de la discipline UI/UX : de la recherche utilisateur au design d'interface, des design systems aux architectures frontend, de l'accessibilite a la performance perçue. Appliquer systematiquement les principes decrits ici pour concevoir des interfaces performantes, accessibles et maintenables. L'approche integre les standards modernes (2024-2026) : design tokens W3C, container queries, View Transitions API, CSS layers, Interaction to Next Paint (INP) comme Core Web Vital, et conformite a l'European Accessibility Act (EAA 2025).

This skill covers the full UI/UX discipline: from user research to interface design, from design systems to frontend architecture, from accessibility to perceived performance. Apply the principles described here systematically to build performant, accessible, and maintainable interfaces. The approach incorporates modern standards (2024-2026): W3C design tokens, container queries, View Transitions API, CSS layers, Interaction to Next Paint (INP) as a Core Web Vital, and compliance with the European Accessibility Act (EAA 2025).

Le design d'interface n'est pas une discipline decorative. Il determine directement les taux de conversion, la retention utilisateur, les couts de support et la conformite legale. Un design system mature reduit le temps de developpement de 30 a 50%, tandis qu'une mauvaise accessibilite expose l'organisation a des risques juridiques croissants sous l'EAA.

## When This Skill Applies

Activer ce skill dans les situations suivantes / Activate this skill in the following situations:

- **Recherche utilisateur** : planification d'interviews, usability testing, creation de personas, user journey mapping, analyse heuristique, design sprints.
- **Design d'interface** : wireframing, prototypage, choix typographiques, hierarchie visuelle, responsive design, design d'interactions et micro-interactions.
- **Design systems** : creation ou evolution d'un design system, definition de design tokens, architecture de composants (atomic design), gouvernance et versioning.
- **Accessibilite** : audit WCAG 2.1/2.2, implementation ARIA, conformite EAA/RGAA/Section 508, navigation clavier, compatibilite lecteurs d'ecran.
- **Architecture frontend** : choix de CSS architecture (BEM, CSS Modules, Tailwind, CSS-in-JS), state management, component patterns, optimisation Core Web Vitals.
- **Integration Figma/Storybook** : workflow design-to-code, documentation de composants, visual regression testing.

## Core Principles

### Principle 1 -- User-Centered Design First
Fonder chaque decision de design sur des donnees utilisateur reelles, jamais sur des suppositions. Conduire au minimum un cycle de recherche (interviews, tests d'utilisabilite) avant de finaliser toute decision de design significative. Valider chaque iteration par des metriques mesurables : taux de completion de tache, System Usability Scale (SUS), taux d'erreur.

### Principle 2 -- Accessibility as Foundation, Not Afterthought
Integrer l'accessibilite des la conception, pas en phase de remediation. Viser la conformite WCAG 2.2 AA comme minimum, anticiper l'EAA (European Accessibility Act) applicable en juin 2025. Tester avec des technologies d'assistance reelles (VoiceOver, NVDA, JAWS) et pas uniquement avec des outils automatises. L'accessibilite beneficie a tous les utilisateurs : sous-titres, contraste, navigation clavier.

### Principle 3 -- Design Tokens as Single Source of Truth
Utiliser les design tokens conformes a la spec W3C Design Tokens Community Group comme contrat entre design et code. Les tokens encapsulent couleurs, typographie, spacing, elevation, motion et breakpoints. Implementer une architecture a trois niveaux : global tokens, alias tokens (semantiques), et component tokens. Propager les tokens du fichier source vers toutes les plateformes (web, iOS, Android) via Style Dictionary ou Cobalt UI.

### Principle 4 -- Progressive Enhancement & Resilience
Construire d'abord pour le scenario le plus contraint (connexion lente, ancien navigateur, technologie d'assistance), puis enrichir progressivement. Utiliser les fonctionnalites CSS modernes (container queries, `:has()`, `@layer`) avec des fallbacks. Chaque composant doit fonctionner sans JavaScript pour le contenu essentiel.

### Principle 5 -- Performance is UX
Traiter la performance comme un aspect fondamental de l'experience utilisateur. Optimiser pour les Core Web Vitals : LCP < 2.5s, INP < 200ms, CLS < 0.1. La performance perçue (skeleton screens, optimistic updates, View Transitions API) est aussi importante que la performance reelle.

### Principle 6 -- Component-Driven Architecture
Concevoir des composants isoles, composables et documentables. Adopter l'atomic design (atoms, molecules, organisms, templates, pages) pour structurer la hierarchie de composants. Chaque composant doit etre autonome, testable individuellement dans Storybook, et versionne.

## Key Frameworks & Methods

### UX Research Methods Matrix

| Method | When | Effort | Data Type |
|---|---|---|---|
| **User Interviews** | Discovery, validation | Moyen | Qualitatif |
| **Usability Testing** | Prototype, post-launch | Moyen-Eleve | Qualitatif + Quantitatif |
| **Surveys** | Large-scale validation | Faible | Quantitatif |
| **Card Sorting** | Information architecture | Faible | Qualitatif |
| **Diary Studies** | Long-term behavior | Eleve | Qualitatif |
| **A/B Testing** | Optimization | Moyen | Quantitatif |
| **Heuristic Evaluation** | Quick audit | Faible | Expert review |
| **Contextual Inquiry** | Deep understanding | Eleve | Qualitatif |

### Design System Architecture

Structurer le design system en couches / Structure the design system in layers:

1. **Foundation Layer** : design tokens (couleurs, typographie, spacing, elevation, motion, breakpoints).
2. **Core Components (Atoms)** : Button, Input, Icon, Badge, Typography, Spacer.
3. **Composite Components (Molecules)** : SearchBar, FormField, Card, NavItem.
4. **Pattern Components (Organisms)** : Header, Sidebar, DataTable, Modal, Form.
5. **Templates & Layouts** : PageShell, DashboardLayout, AuthLayout.

### CSS Architecture Decision Matrix

| Approach | Best For | Scoping | Runtime Cost | DX |
|---|---|---|---|---|
| **CSS Modules** | App components | Auto-scoped | Zero | Bon |
| **Tailwind CSS** | Rapid prototyping, utility-first | Class-based | Zero | Tres bon |
| **CSS-in-JS (Panda, Vanilla Extract)** | Typed styles, tokens | Auto-scoped | Zero (build-time) | Bon |
| **CSS Layers (@layer)** | Large systems, cascade control | Explicit layers | Zero | Moyen |
| **BEM** | Traditional, legacy | Convention | Zero | Moyen |

Privilegier les solutions zero-runtime (Tailwind, CSS Modules, Vanilla Extract, Panda CSS) par rapport aux CSS-in-JS runtime (styled-components, Emotion) pour les applications sensibles a la performance.

### Accessibility Compliance Framework

Suivre cette hierarchie de conformite :
- **Niveau A** (minimum legal) : alternative texte, navigation clavier, pas de pieges clavier, bypass blocks.
- **Niveau AA** (cible recommandee / EAA requirement) : contraste 4.5:1 (texte), 3:1 (large texte), redimensionnement 200%, reflow, focus visible, messages d'erreur.
- **Niveau AAA** (excellence) : contraste 7:1, langue des signes, timing ajustable, pas d'animation auto.

## Decision Guide

### Arbre de decision design system / Design System Decision Tree

```
1. Taille de l'equipe et nombre de produits ?
   |-- 1 produit, equipe < 5 -> Library de composants legere (Shadcn/UI)
   |-- 2-5 produits, equipe < 20 -> Design system interne (Storybook + tokens)
   +-- > 5 produits, equipe > 20 -> Design system full (gouvernance, versioning, multi-platform)

2. Quelle approche CSS ?
   |-- Prototypage rapide, petite equipe -> Tailwind CSS
   |-- Application complexe, design system strict -> CSS Modules ou Vanilla Extract
   +-- Multi-framework (React, Vue, Web Components) -> Design tokens + CSS custom properties

3. Quel niveau d'accessibilite viser ?
   |-- Produit EU (EAA 2025) -> WCAG 2.2 AA obligatoire
   |-- Produit US (Section 508) -> WCAG 2.1 AA obligatoire
   |-- Produit FR (secteur public) -> RGAA 4.1 (base WCAG 2.1 AA)
   +-- Tout produit -> WCAG 2.2 AA comme baseline recommandee
```

### State Management Decision

| Situation | Solution recommandee |
|---|---|
| UI state local | `useState` / `useReducer` |
| Server state (API data) | TanStack Query / SWR |
| Global state simple | Zustand / Jotai |
| Global state complexe | Redux Toolkit (si existant), Zustand |
| URL state | URL search params (nuqs, next-usequerystate) |
| Form state | React Hook Form / Conform |
| Cross-tab state | Signals / Broadcast Channel API |

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Compound Components** : concevoir des composants composes (`<Tabs>`, `<Tabs.List>`, `<Tabs.Panel>`) pour la flexibilite et l'accessibilite intrinseque.
- **Headless UI** : separer la logique d'interaction (hooks, state machines) de la presentation (Radix UI, Headless UI, Ark UI). Permettre le restyling complet sans modifier la logique.
- **Design Token Pipeline** : Figma Variables -> JSON (W3C format) -> Style Dictionary -> CSS custom properties + Swift/Kotlin constants.
- **Progressive Disclosure** : reveler la complexite graduellement. Afficher les options avancees uniquement quand l'utilisateur les demande.
- **Skeleton Screens** : afficher la structure de la page pendant le chargement pour ameliorer la performance perçue (LCP).
- **View Transitions** : utiliser l'API View Transitions pour des navigations fluides entre pages/etats, remplacant les animations JavaScript couteuses.

### Anti-patterns critiques

- **Div Soup** : utiliser des `<div>` partout au lieu de la semantique HTML (`<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`). Detecter via l'audit Lighthouse accessibility.
- **Z-Index Wars** : empiler des z-index arbitraires. Utiliser un systeme de layers gere par des tokens (overlay, modal, tooltip, popover).
- **Props Drilling for Theming** : passer les variables de theme en props au lieu d'utiliser CSS custom properties ou un ThemeProvider.
- **Inaccessible Custom Components** : recreer des `<select>`, `<dialog>`, `<datepicker>` sans implementer les ARIA roles, states et keyboard navigation. Utiliser des primitives headless a la place.
- **Layout Shift Negligence** : ne pas reserver l'espace pour les images, fonts et contenus dynamiques, causant un CLS eleve.
- **Mobile-Only Testing** : tester uniquement sur simulateurs au lieu d'appareils reels. Les performances et l'ergonomie divergent significativement.

## Implementation Workflow

### Phase 1 -- Research & Discovery (1-2 semaines)
1. Conduire des interviews utilisateur (minimum 5 participants) pour identifier les besoins et pain points.
2. Creer des personas et user journey maps bases sur les donnees reelles.
3. Realiser un audit heuristique de l'existant (Nielsen's 10 heuristics).
4. Auditer l'accessibilite existante avec axe-core, Lighthouse et tests manuels (clavier, lecteur d'ecran).
5. Mesurer les Core Web Vitals existants via CrUX (Chrome UX Report) et les field data.

### Phase 2 -- Design Foundation (1-2 semaines)
6. Definir les design tokens (couleurs, typographie, spacing, elevation, motion) en format W3C.
7. Etablir la grille responsive et la strategie de breakpoints (mobile-first, container queries).
8. Creer la hierarchie de composants (atomic design inventory).
9. Produire les wireframes low-fidelity et les valider par des tests d'utilisabilite rapides (guerilla testing).
10. Configurer Figma avec les libraries de composants et les variables synchronisees aux tokens.

### Phase 3 -- Component Development (2-4 semaines)
11. Implementer les atoms dans Storybook avec les variantes, etats et stories d'accessibilite.
12. Construire les molecules et organismes en composant les atoms.
13. Implementer l'accessibilite intrinseque : roles ARIA, keyboard navigation, focus management, annonces live regions.
14. Ecrire les tests : visual regression (Chromatic/Percy), interaction tests (Testing Library), axe-core assertions.
15. Documenter chaque composant : props API, guidelines d'usage, do/don't, exemples de code.

### Phase 4 -- Integration & Optimization (1-2 semaines)
16. Assembler les templates et pages a partir des composants du design system.
17. Optimiser les Core Web Vitals : lazy loading, code splitting, font optimization (`font-display: swap`), image optimization (AVIF/WebP, `<picture>`).
18. Implementer les View Transitions pour les navigations inter-pages.
19. Conduire des tests d'utilisabilite sur le prototype haute fidelite (minimum 5 participants).
20. Valider la conformite WCAG 2.2 AA avec un audit complet (automatise + manuel).

### Phase 5 -- Governance & Scale (ongoing)
21. Mettre en place le processus de contribution au design system (RFC, review, merge).
22. Automatiser la validation : a11y checks en CI, visual regression, design token lint.
23. Versionner le design system (semver) et publier un changelog.
24. Mesurer l'adoption (analytics d'usage des composants) et la satisfaction (Design System Satisfaction Score).
25. Planifier des revues trimestrielles pour evoluer le systeme (deprecation, nouveaux patterns).



## State of the Art (2025-2026)

Le design d'interface et l'expérience utilisateur évoluent rapidement :

- **AI-generated UI** : Les outils génèrent des composants, des layouts et du code frontend à partir de descriptions ou de maquettes (v0.dev, Claude artifacts).
- **Design systems matures** : shadcn/ui, Radix et les headless components deviennent le standard, séparant la logique du style.
- **Accessibilité renforcée** : L'European Accessibility Act (2025) impose l'accessibilité numérique, accélérant l'adoption des standards WCAG 2.2.
- **Micro-interactions et motion** : Les animations subtiles (Framer Motion, CSS animations) deviennent essentielles pour la perception de qualité.
- **Design tokens et multi-platform** : Les design tokens permettent de maintenir la cohérence visuelle entre web, mobile et desktop à partir d'une source unique.

## Template actionnable

### Checklist d'accessibilité WCAG

| Critère | Niveau | Vérifié | Notes |
|---|---|---|---|
| **Contraste texte** | AA (4.5:1) | ☐ | ___ |
| **Contraste grands textes** | AA (3:1) | ☐ | ___ |
| **Navigation clavier** | A | ☐ | ___ |
| **Focus visible** | AA | ☐ | ___ |
| **Textes alternatifs images** | A | ☐ | ___ |
| **Labels des formulaires** | A | ☐ | ___ |
| **Messages d'erreur** | A | ☐ | ___ |
| **Hiérarchie des titres** | A | ☐ | ___ |
| **Landmarks ARIA** | AA | ☐ | ___ |
| **Responsive (320px min)** | AA | ☐ | ___ |

## Prompts types

- "Comment construire un design system avec Tailwind et shadcn/ui ?"
- "Aide-moi à améliorer l'accessibilité WCAG de mon application"
- "Propose une architecture de composants pour mon app React"
- "Comment optimiser les Core Web Vitals de mon site ?"
- "Aide-moi à concevoir un flow d'onboarding utilisateur efficace"
- "Quelle stratégie CSS adopter pour un projet à grande échelle ?"

## Skills connexes

| Skill | Lien |
|---|---|
| Code Excellence | `code-development:code-excellence` — Qualité du code frontend et composants |
| Product Analytics | `code-development:product-analytics` — Métriques UX et tests A/B |
| Data Literacy | `data-bi:data-literacy` — Visualisation de données et design d'information |
| Process Engineering | `code-development:process-engineering` — Design process et collaboration design-dev |
| Marketing | `entreprise:marketing` — Conversion, parcours client et landing pages |

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[Design Systems](./references/design-systems.md)** -- Atomic design en profondeur, architecture de design tokens (W3C spec), pipeline Figma-to-code, Storybook avance, component libraries multi-plateformes, gouvernance et versioning de design systems.

- **[Accessibility](./references/accessibility.md)** -- WCAG 2.1/2.2 complet (criteres A, AA, AAA), ARIA roles et states, navigation clavier, compatibilite lecteurs d'ecran, outils de test (axe, Lighthouse, WAVE, Pa11y), European Accessibility Act (EAA 2025), RGAA, Section 508.

- **[UX Research](./references/ux-research.md)** -- Methodes de recherche utilisateur (interviews, surveys, usability testing, diary studies), personas et user journeys, Jobs-to-be-Done, evaluation heuristique (Nielsen's 10), card sorting, contextual inquiry, design thinking, Google Ventures Design Sprint.

- **[Frontend Architecture](./references/frontend-architecture.md)** -- Component patterns (atomic, compound, render props), state management (Redux, Zustand, Jotai, signals), CSS architecture (BEM, CSS Modules, Tailwind, CSS-in-JS), optimisation Core Web Vitals (LCP, INP, CLS), progressive enhancement, View Transitions API, container queries.

### Ouvrages et references fondamentaux
- Steve Krug, *Don't Make Me Think* (3rd ed., 2014)
- Brad Frost, *Atomic Design* (2016)
- Alla Kholmatova, *Design Systems* (2017)
- Heydon Pickering, *Inclusive Components* (2019)
- Adam Silver, *Form Design Patterns* (2018)
- Vitaly Friedman, *Smart Interface Design Patterns* (2022)
- W3C, *Web Content Accessibility Guidelines (WCAG) 2.2* (2023)
- W3C Design Tokens Community Group, *Design Tokens Format Module* (2023-2025)
