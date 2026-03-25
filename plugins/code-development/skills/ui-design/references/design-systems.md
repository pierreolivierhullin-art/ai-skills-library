# Design Systems -- Architecture, Tokens & Governance

Reference complete pour la conception, l'implementation et la gouvernance de design systems modernes. Complete reference for designing, implementing, and governing modern design systems.

---

## 1. Atomic Design Methodology

### Fondements / Foundations

Appliquer la methodologie Atomic Design de Brad Frost comme cadre structurant pour la hierarchie de composants. Cette approche decompose les interfaces en cinq niveaux de granularite, chacun avec des responsabilites distinctes.

Apply Brad Frost's Atomic Design methodology as the structuring framework for component hierarchy. This approach decomposes interfaces into five levels of granularity, each with distinct responsibilities.

### Atoms

Les atoms sont les blocs de construction fondamentaux, insecables, du design system. Ils ne peuvent pas etre decomposees davantage sans perdre leur fonction.

Atoms are the fundamental, indivisible building blocks of the design system. They cannot be broken down further without losing their function.

**Exemples / Examples:**
- `Button` : variantes (primary, secondary, ghost, destructive), etats (default, hover, active, focus, disabled, loading).
- `Input` : types (text, email, password, number, search), etats (default, focus, error, disabled, readonly).
- `Icon` : systeme d'icones SVG sprite ou composants individuels, taille standardisee (16, 20, 24, 32px).
- `Badge` : variantes semantiques (info, success, warning, error), tailles.
- `Typography` : composants de texte (Heading, Text, Label, Caption) avec variantes de poids et taille.
- `Spacer` : composant d'espacement utilisant les tokens de spacing.
- `Avatar` : image utilisateur avec fallback initiales, tailles standardisees.
- `Divider` : separateur horizontal/vertical.

**Regles pour les atoms / Rules for atoms:**
- Chaque atom doit etre entierement auto-contenu et ne dependre d'aucun autre composant.
- Exposer un API de props minimal et explicite (variante, taille, etat, `asChild` pour le polymorphisme).
- Implementer les roles ARIA et la gestion du focus intrinsequement.
- Documenter toutes les variantes et etats dans Storybook avec des stories dediees.

### Molecules

Les molecules combinent plusieurs atoms pour former des unites fonctionnelles coherentes. Elles representent le premier niveau de composition.

Molecules combine multiple atoms to form coherent functional units. They represent the first level of composition.

**Exemples / Examples:**
- `FormField` : combine Label + Input + HelperText/ErrorMessage. Gere l'association `htmlFor`/`id` automatiquement.
- `SearchBar` : combine Input + Button (submit) + Icon (search). Gere le focus et le debounce.
- `Card` : combine un conteneur avec Header, Body, Footer slots. Supporte les variantes interactive/static.
- `NavItem` : combine Icon + Text + Badge (optional). Gere l'etat actif et le focus.
- `Breadcrumb` : combine des liens avec separateurs. Gere l'ARIA `nav` et `aria-current`.
- `Tooltip` : combine un trigger et un contenu positionne. Gere l'accessibilite (`role="tooltip"`, `aria-describedby`).

**Regles pour les molecules / Rules for molecules:**
- Chaque molecule doit utiliser exclusivement des atoms du design system comme blocs de construction.
- Gerer la logique d'interaction locale (toggle, hover, focus management).
- Accepter des props de composition (`children`, `slots`, render props) pour la flexibilite.

### Organisms

Les organismes sont des composants complexes composes de molecules et d'atoms, representant des sections distinctes de l'interface.

Organisms are complex components composed of molecules and atoms, representing distinct sections of the interface.

**Exemples / Examples:**
- `Header` : combine Logo + Navigation + SearchBar + UserMenu. Gere le responsive (hamburger menu mobile).
- `DataTable` : combine Table + Pagination + Sorting + Filtering + SelectionState. Virtualization pour les grands datasets.
- `Modal/Dialog` : combine Overlay + DialogContent + Header + Body + Footer + FocusTrap. Gere `inert` sur le contenu derriere.
- `Form` : combine plusieurs FormFields + validation + submission. Integration avec React Hook Form ou Conform.
- `Sidebar` : combine NavItems + Sections + CollapsibleGroups. Gere l'etat ouvert/ferme et la navigation clavier.

**Regles pour les organismes / Rules for organisms:**
- Encapsuler la logique metier locale mais rester agnostique au domaine applicatif.
- Gerer leur propre etat interne complexe (selection, tri, pagination).
- Fournir une API de callbacks (`onSort`, `onChange`, `onSubmit`) pour l'integration.

### Templates

Les templates definissent la structure de mise en page sans contenu specifique. Ils representent l'architecture de la page.

Templates define the layout structure without specific content. They represent the page architecture.

**Exemples / Examples:**
- `DashboardLayout` : sidebar + header + main content area + optional right panel.
- `AuthLayout` : layout centre avec branding pour les pages login/register/forgot-password.
- `SettingsLayout` : navigation verticale tabs + content area.

### Pages

Les pages sont des instances de templates remplies avec du contenu reel. Elles representent le niveau de fidelite le plus eleve et sont specifiques a l'application.

Pages are template instances filled with real content. They represent the highest fidelity level and are application-specific.

---

## 2. Design Tokens -- W3C Specification & Architecture

### W3C Design Tokens Format Module

Adopter le format W3C Design Tokens Community Group (DTCG) comme standard pour la definition des tokens. Ce format garantit l'interoperabilite entre outils (Figma, Style Dictionary, Cobalt UI).

Adopt the W3C Design Tokens Community Group (DTCG) format as the standard for token definition. This format ensures interoperability across tools (Figma, Style Dictionary, Cobalt UI).

**Structure du fichier JSON / JSON File Structure:**

```json
{
  "color": {
    "brand": {
      "primary": {
        "$value": "#0066FF",
        "$type": "color",
        "$description": "Primary brand color / Couleur principale de marque"
      },
      "primary-light": {
        "$value": "#3388FF",
        "$type": "color"
      }
    },
    "semantic": {
      "action": {
        "$value": "{color.brand.primary}",
        "$type": "color",
        "$description": "Color for interactive actions / Couleur pour les actions interactives"
      },
      "error": {
        "$value": "#DC2626",
        "$type": "color"
      },
      "success": {
        "$value": "#16A34A",
        "$type": "color"
      }
    }
  },
  "spacing": {
    "xs": { "$value": "4px", "$type": "dimension" },
    "sm": { "$value": "8px", "$type": "dimension" },
    "md": { "$value": "16px", "$type": "dimension" },
    "lg": { "$value": "24px", "$type": "dimension" },
    "xl": { "$value": "32px", "$type": "dimension" },
    "2xl": { "$value": "48px", "$type": "dimension" }
  },
  "typography": {
    "heading-1": {
      "$value": {
        "fontFamily": "{fontFamily.display}",
        "fontSize": "36px",
        "fontWeight": 700,
        "lineHeight": 1.2,
        "letterSpacing": "-0.02em"
      },
      "$type": "typography"
    }
  }
}
```

### Architecture a trois niveaux / Three-Tier Architecture

Implementer une architecture de tokens structuree en trois niveaux pour maximiser la maintenabilite et la coherence.

**Niveau 1 -- Global Tokens (Primitives):**
Valeurs brutes sans semantique : palette de couleurs complete, echelle typographique, echelle de spacing. Ces tokens ne sont jamais references directement dans les composants.

```
color.blue.500 = #3B82F6
color.gray.100 = #F3F4F6
font.size.16 = 16px
spacing.4 = 16px
```

**Niveau 2 -- Alias Tokens (Semantic):**
Tokens semantiques qui referent les global tokens. Ils portent le sens d'usage et sont le niveau principal de reference dans les composants.

```
color.action.primary = {color.blue.500}
color.background.surface = {color.gray.100}
color.text.primary = {color.gray.900}
color.border.default = {color.gray.200}
font.size.body = {font.size.16}
spacing.component.gap = {spacing.4}
```

**Niveau 3 -- Component Tokens:**
Tokens specifiques a un composant, referant les alias tokens. Utiliser uniquement quand un composant necessite des valeurs qui ne s'appliquent qu'a lui.

```
button.color.background = {color.action.primary}
button.color.text = {color.text.inverse}
button.spacing.padding-x = {spacing.component.gap}
button.border.radius = {border.radius.md}
```

### Theming avec les tokens / Theming with Tokens

Implementer le theming (light/dark mode, multi-brand) en reassignant les alias tokens sans toucher aux global tokens ni aux component tokens.

```json
{
  "light": {
    "color.background.surface": "{color.white}",
    "color.text.primary": "{color.gray.900}",
    "color.border.default": "{color.gray.200}"
  },
  "dark": {
    "color.background.surface": "{color.gray.900}",
    "color.text.primary": "{color.gray.100}",
    "color.border.default": "{color.gray.700}"
  }
}
```

### Categories de tokens essentielles / Essential Token Categories

| Category | Description | Examples |
|---|---|---|
| **Color** | Palette, semantique, etats | brand, background, text, border, error, success |
| **Typography** | Families, sizes, weights, line heights | heading, body, caption, code, display |
| **Spacing** | Marges, paddings, gaps | xs (4px) to 4xl (64px), component gaps |
| **Border** | Width, radius, style | radius-sm, radius-md, radius-full, width-thin |
| **Elevation** | Box shadows, z-index | shadow-sm, shadow-md, shadow-lg, z-modal |
| **Motion** | Durations, easing functions | duration-fast (100ms), duration-normal (200ms), ease-out |
| **Breakpoints** | Responsive thresholds | sm (640px), md (768px), lg (1024px), xl (1280px) |
| **Opacity** | Transparency levels | disabled (0.5), overlay (0.8), hover (0.04) |

---

## 3. Design Token Pipeline -- Figma to Code

### Workflow de synchronisation / Synchronization Workflow

Implementer un pipeline automatise pour propager les tokens de Figma vers toutes les plateformes cibles.

```
Figma Variables (source of truth)
    |
    v
Export plugin (Tokens Studio / Variables export)
    |
    v
JSON (W3C DTCG format) -- committed to Git
    |
    v
Style Dictionary / Cobalt UI (transformation)
    |
    +---> CSS Custom Properties (web)
    +---> SCSS Variables (legacy web)
    +---> Tailwind theme config (Tailwind projects)
    +---> Swift UIColor extensions (iOS)
    +---> Kotlin Color objects (Android)
    +---> JSON (design tool sync)
```

### Configuration Style Dictionary

```javascript
// style-dictionary.config.js
export default {
  source: ["tokens/**/*.json"],
  platforms: {
    css: {
      transformGroup: "css",
      buildPath: "dist/css/",
      files: [{
        destination: "tokens.css",
        format: "css/variables",
        options: {
          outputReferences: true // preserve references as var(--...)
        }
      }]
    },
    tailwind: {
      transformGroup: "js",
      buildPath: "dist/tailwind/",
      files: [{
        destination: "theme.js",
        format: "javascript/module-flat"
      }]
    },
    ios: {
      transformGroup: "ios-swift",
      buildPath: "dist/ios/",
      files: [{
        destination: "Tokens.swift",
        format: "ios-swift/class.swift",
        className: "DesignTokens"
      }]
    }
  }
};
```

### Figma Best Practices

- Utiliser les **Figma Variables** (pas les anciens styles) pour les couleurs, spacing et breakpoints.
- Organiser les variables en collections : Primitives, Semantic, Component.
- Activer les modes pour le theming (Light, Dark, High Contrast).
- Utiliser le **Tokens Studio** plugin pour l'export en format W3C DTCG.
- Nommer les variables avec la meme convention que les tokens code : `color/brand/primary`, `spacing/md`.

---

## 4. Storybook -- Component Documentation & Testing

### Configuration avancee / Advanced Configuration

Configurer Storybook comme plateforme centrale de documentation, testing et collaboration du design system.

**Addons essentiels / Essential Addons:**
- `@storybook/addon-a11y` : audit d'accessibilite integre (axe-core) dans chaque story.
- `@storybook/addon-interactions` : tests d'interaction (click, type, keyboard) directement dans Storybook.
- `@storybook/addon-designs` : integration Figma pour comparer design vs implementation.
- `@storybook/addon-viewport` : preview responsive avec breakpoints personnalises.
- `@storybook/test-runner` : execution des interaction tests en CI.
- `chromatic` : visual regression testing integre.

### Structure des stories / Story Structure

Organiser les stories par composant avec des categories claires.

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";
import { expect, userEvent, within } from "@storybook/test";

const meta: Meta<typeof Button> = {
  title: "Atoms/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["primary", "secondary", "ghost", "destructive"],
    },
    size: { control: "select", options: ["sm", "md", "lg"] },
  },
  parameters: {
    design: {
      type: "figma",
      url: "https://figma.com/file/xxx/Design-System?node-id=123",
    },
  },
};
export default meta;

type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: { variant: "primary", children: "Click me" },
};

export const AllVariants: Story = {
  render: () => (
    <div style={{ display: "flex", gap: "8px" }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="destructive">Destructive</Button>
    </div>
  ),
};

export const KeyboardInteraction: Story = {
  args: { variant: "primary", children: "Click me" },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole("button");
    await userEvent.tab();
    await expect(button).toHaveFocus();
    await userEvent.keyboard("{Enter}");
  },
};
```

### Visual Regression Testing

Implementer le visual regression testing avec Chromatic ou Percy pour detecter les regressions visuelles a chaque PR.

**Pipeline CI / CI Pipeline:**
1. Chaque PR declenche un build Storybook.
2. Chromatic capture des screenshots de chaque story.
3. Les diff visuels sont revues par l'equipe design.
4. Les tests d'interaction et d'accessibilite sont executes via le test-runner.
5. Le merge est bloque si des regressions visuelles non approuvees ou des violations a11y sont detectees.

---

## 5. Multi-Platform Design Systems

### Strategies multi-plateformes / Cross-Platform Strategies

Concevoir des design systems qui fonctionnent sur web, iOS, Android et potentiellement desktop.

**Approche 1 -- Tokens partages, composants natifs :**
Partager les design tokens (via Style Dictionary) mais implementer les composants nativement sur chaque plateforme. Recommande pour la meilleure experience native.

**Approche 2 -- Web Components :**
Implementer les composants en Web Components (Lit, Stencil) pour une compatibilite cross-framework (React, Vue, Angular, vanilla). Recommande pour les organisations avec de multiples frameworks web.

**Approche 3 -- Cross-platform frameworks :**
Utiliser React Native (avec React Native Web) ou Flutter pour partager les composants. Recommande uniquement si la velocite l'emporte sur l'experience native.

### Web Components avec Lit

```typescript
// ds-button.ts
import { LitElement, html, css } from "lit";
import { customElement, property } from "lit/decorators.js";

@customElement("ds-button")
export class DsButton extends LitElement {
  @property() variant: "primary" | "secondary" = "primary";
  @property({ type: Boolean }) disabled = false;

  static styles = css`
    :host {
      display: inline-flex;
    }
    button {
      padding: var(--ds-spacing-sm) var(--ds-spacing-md);
      border-radius: var(--ds-border-radius-md);
      font-family: var(--ds-font-family-body);
      cursor: pointer;
    }
    button[data-variant="primary"] {
      background: var(--ds-color-action-primary);
      color: var(--ds-color-text-inverse);
    }
  `;

  render() {
    return html`
      <button
        data-variant=${this.variant}
        ?disabled=${this.disabled}
        part="button"
      >
        <slot></slot>
      </button>
    `;
  }
}
```

---

## 6. Gouvernance & Versioning

### Modele de gouvernance / Governance Model

Etablir un processus clair pour les contributions, les revues et les evolutions du design system.

**Structure de l'equipe / Team Structure:**
- **Core team** (2-4 personnes) : maintient le design system, revue les contributions, gere les releases.
- **Contributors** : equipes produit qui soumettent des nouveaux composants ou des modifications via RFC.
- **Consumers** : equipes qui utilisent le design system sans contribuer directement.

**Processus de contribution / Contribution Process:**
1. **Proposal (RFC)** : ouvrir une RFC decrivant le besoin, les use cases, l'API proposee et les considerations a11y.
2. **Design Review** : revue par l'equipe design pour valider la coherence visuelle.
3. **Implementation** : developper le composant avec stories, tests et documentation.
4. **Code Review** : revue par la core team pour valider la qualite, l'a11y, la performance.
5. **Release** : integration dans la prochaine version du design system.

### Versioning Strategy

Appliquer le Semantic Versioning (semver) strictement :
- **MAJOR** (breaking) : suppression de props, changement d'API, refonte visuelle majeure.
- **MINOR** (feature) : nouveau composant, nouvelle variante, nouvelle prop non-breaking.
- **PATCH** (fix) : correction de bug, amelioration d'accessibilite, ajustement visuel mineur.

**Migration Guides:**
Pour chaque version majeure, publier un guide de migration detaille avec :
- Liste complete des breaking changes.
- Codemods automatises quand possible (`jscodeshift`, `ast-grep`).
- Periode de deprecation (minimum 1 version mineure avant suppression).

### Metriques de sante / Health Metrics

Mesurer la sante du design system avec ces KPIs :
- **Adoption rate** : pourcentage de composants du design system vs composants custom.
- **Coverage** : nombre de produits utilisant le design system / total produits.
- **Contribution frequency** : nombre de PRs externes par mois.
- **Bug rate** : nombre de bugs rapportes par composant par mois.
- **Design-dev parity** : ecart entre les specs Figma et l'implementation.
- **Accessibility score** : score moyen axe-core sur l'ensemble des stories.
- **Consumer satisfaction** : NPS ou DSAT (Design System Satisfaction Score) trimestriel.

---

## 7. AI-Assisted Design Systems (2024-2026)

### Integration de l'IA dans le workflow / AI Integration in the Workflow

Exploiter l'IA generative pour accelerer le travail du design system sans compromettre la qualite.

**Use cases valides / Valid Use Cases:**
- **Generation de variantes** : utiliser l'IA pour generer des variantes de composants (dark mode, high contrast) a partir d'un design existant.
- **Documentation automatique** : generer la documentation des props, des guidelines d'usage et des exemples a partir du code source.
- **Audit d'accessibilite augmente** : combiner les outils automatises (axe) avec l'IA pour detecter des patterns d'accessibilite subtils (langage complexe, hierarchie de heading illogique).
- **Design token generation** : generer des echelles de couleurs harmonieuses, des echelles typographiques et des echelles de spacing a partir de quelques tokens de reference.
- **Code generation** : generer le squelette d'un composant (stories, tests, types) a partir d'une spec Figma.

**Garde-fous / Guardrails:**
- Ne jamais accepter du code genere par IA sans revue humaine pour l'accessibilite.
- Valider systematiquement les contrastes de couleur generes par IA.
- Utiliser l'IA comme accelerateur, jamais comme remplacement du design review humain.
- Documenter quand l'IA a ete utilisee dans le processus de creation.

---

## References

- Brad Frost, *Atomic Design* (2016) -- https://atomicdesign.bradfrost.com
- W3C Design Tokens Community Group -- https://www.w3.org/community/design-tokens/
- Style Dictionary documentation -- https://amzn.github.io/style-dictionary
- Storybook documentation -- https://storybook.js.org/docs
- Alla Kholmatova, *Design Systems* (Smashing Magazine, 2017)
- Nathan Curtis, *Modular Web Design* (2010)
- Figma Variables documentation -- https://help.figma.com/hc/en-us/articles/15339657135383
