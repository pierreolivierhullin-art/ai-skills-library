# Accessibility -- WCAG 2.2, ARIA, Legal Compliance & Testing

Reference complete pour l'accessibilite numerique : standards, implementation technique, conformite legale et strategies de test. Complete reference for digital accessibility: standards, technical implementation, legal compliance, and testing strategies.

---

## 1. WCAG 2.2 -- Guidelines Completes

### Structure des WCAG / WCAG Structure

Les Web Content Accessibility Guidelines (WCAG) 2.2 sont organisees en 4 principes (POUR), 13 guidelines et 86 criteres de succes (success criteria) repartis en 3 niveaux de conformite.

The Web Content Accessibility Guidelines (WCAG) 2.2 are organized into 4 principles (POUR), 13 guidelines, and 86 success criteria distributed across 3 conformance levels.

### Principe 1 -- Perceivable / Perceptible

L'information et les composants d'interface doivent etre presentables aux utilisateurs de maniere perceptible.

**1.1 Text Alternatives (A)**
- Fournir un texte alternatif (`alt`) pour toute image non decorative. Decrire la fonction, pas l'apparence.
- Utiliser `alt=""` (vide, pas absent) pour les images decoratives afin qu'elles soient ignorees par les lecteurs d'ecran.
- Pour les images complexes (graphiques, diagrammes), fournir une description longue via `aria-describedby` ou un lien vers une page descriptive.
- Les icones interactives doivent avoir un `aria-label` ou un texte visuellement cache (`sr-only`).

**1.2 Time-Based Media (A/AA/AAA)**
- Fournir des sous-titres pour tout contenu audio (A).
- Fournir une audio-description pour tout contenu video (AA).
- Fournir une transcription textuelle pour le contenu audio-seul (A).

**1.3 Adaptable (A/AA)**
- Utiliser le HTML semantique pour transmettre la structure (`<h1>`-`<h6>`, `<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`).
- S'assurer que l'ordre de lecture du DOM correspond a l'ordre visuel.
- Ne pas s'appuyer uniquement sur des indices sensoriels (couleur, forme, position) pour transmettre l'information.
- **Nouveau WCAG 2.2** : l'orientation de l'ecran ne doit pas etre restreinte sauf necessity fonctionnelle (1.3.4 AA).

**1.4 Distinguishable / Distinguable (A/AA/AAA)**
- **Contraste texte** : ratio minimum 4.5:1 pour le texte normal, 3:1 pour le texte large (>= 18pt ou >= 14pt bold) (AA).
- **Contraste AAA** : ratio 7:1 pour le texte normal, 4.5:1 pour le texte large.
- **Contraste des elements UI** : ratio minimum 3:1 pour les bordures, icones, focus indicators et composants interactifs (AA, 1.4.11).
- **Reflow** : le contenu doit etre lisible sans scroll horizontal a 320px CSS de largeur (AA, 1.4.10).
- **Text spacing** : le contenu doit rester fonctionnel avec espacement modifie (line-height 1.5x, letter-spacing 0.12em, word-spacing 0.16em) (AA, 1.4.12).
- **Content on Hover/Focus** : tout contenu qui apparait au survol/focus doit etre dismissable, hoverable et persistant (AA, 1.4.13).

### Principe 2 -- Operable / Utilisable

Les composants d'interface et la navigation doivent etre utilisables.

**2.1 Keyboard Accessible (A)**
- Toutes les fonctionnalites doivent etre accessibles au clavier.
- Pas de piege clavier : l'utilisateur doit pouvoir quitter tout composant avec Tab ou Escape.
- **Nouveau WCAG 2.2** : les raccourcis clavier a caractere unique doivent pouvoir etre desactives ou reconfigures (2.1.4 A).

**2.2 Enough Time (A/AA/AAA)**
- Les limites de temps doivent etre ajustables, extensibles ou desactivables.
- Le contenu en mouvement, clignotant ou defilant doit pouvoir etre mis en pause.

**2.3 Seizures and Physical Reactions (A/AAA)**
- Pas de contenu clignotant plus de 3 fois par seconde (A).
- Respecter `prefers-reduced-motion` pour les animations.

**2.4 Navigable (A/AA/AAA)**
- Fournir un mecanisme de bypass (skip to content link) (A).
- Chaque page doit avoir un titre descriptif unique (A).
- L'ordre du focus doit etre logique et previsible (A).
- La destination des liens doit etre determinable a partir du texte du lien (A) ou du contexte (AA).
- **Focus visible** : les elements focalisables doivent avoir un indicateur de focus visible d'au moins 2px de contraste (AA, 2.4.7 renforce en 2.2).
- **Nouveau WCAG 2.2 -- Focus Not Obscured (Minimum)** (AA, 2.4.11) : l'element focalise ne doit pas etre entierement cache par d'autres contenus (sticky headers, modals).
- **Nouveau WCAG 2.2 -- Focus Not Obscured (Enhanced)** (AAA, 2.4.12) : l'element focalise ne doit pas etre partiellement cache.
- **Nouveau WCAG 2.2 -- Focus Appearance** (AAA, 2.4.13) : l'indicateur de focus doit avoir une surface minimum et un contraste suffisant.

**2.5 Input Modalities (A/AA)**
- Les gestes multi-points ou complexes doivent avoir une alternative a point unique (A, 2.5.1).
- L'activation des pointeurs peut etre annulee (A, 2.5.2).
- **Nouveau WCAG 2.2 -- Dragging Movements** (AA, 2.5.7) : toute fonctionnalite de glisser-deposer doit avoir une alternative sans glissement.
- **Nouveau WCAG 2.2 -- Target Size (Minimum)** (AA, 2.5.8) : les cibles interactives doivent avoir au minimum 24x24 CSS pixels, sauf exceptions.

### Principe 3 -- Understandable / Comprehensible

L'information et l'utilisation de l'interface doivent etre comprehensibles.

**3.1 Readable (A/AA/AAA)**
- Declarer la langue de la page avec `lang` sur `<html>` (A).
- Indiquer les changements de langue dans le contenu avec `lang` sur l'element (AA).

**3.2 Predictable (A/AA)**
- Les elements interactifs ne doivent pas changer le contexte au focus (A).
- Les mecanismes de navigation doivent etre coherents entre les pages (AA).
- **Nouveau WCAG 2.2 -- Consistent Help** (A, 3.2.6) : les mecanismes d'aide (chat, telephone, FAQ) doivent apparaitre au meme endroit sur toutes les pages.

**3.3 Input Assistance (A/AA/AAA)**
- Les erreurs de saisie doivent etre detectees et decrites textuellement (A).
- Des labels ou instructions doivent etre fournis pour les champs de formulaire (A).
- Les suggestions de correction doivent etre proposees quand possible (AA).
- **Nouveau WCAG 2.2 -- Redundant Entry** (A, 3.3.7) : ne pas demander a l'utilisateur de ressaisir des informations deja fournies dans le meme processus.
- **Nouveau WCAG 2.2 -- Accessible Authentication (Minimum)** (AA, 3.3.8) : les processus d'authentification ne doivent pas reposer sur des tests cognitifs (memorisation, puzzles) sauf si des alternatives sont disponibles (password manager, copier-coller).
- **Nouveau WCAG 2.2 -- Accessible Authentication (Enhanced)** (AAA, 3.3.9) : aucun test cognitif d'aucune sorte dans l'authentification.

### Principe 4 -- Robust / Robuste

**4.1 Compatible (A)**
- Utiliser un HTML valide et bien forme.
- Fournir `name`, `role` et `value` pour tous les composants d'interface (parsable par les technologies d'assistance).
- **Nouveau WCAG 2.2** : status messages utilisant `role="status"` ou `aria-live` pour informer sans deplacer le focus (4.1.3 AA).

---

## 2. ARIA -- Roles, States & Properties

### Regle d'or de l'ARIA / Golden Rule of ARIA

**"No ARIA is better than bad ARIA."** Utiliser d'abord les elements HTML natifs. N'ajouter ARIA que quand aucun element HTML ne convient.

### Roles essentiels / Essential Roles

| Role | Usage | Element HTML natif |
|---|---|---|
| `role="button"` | Element cliquable non-`<button>` | Preferer `<button>` |
| `role="link"` | Navigation non-`<a>` | Preferer `<a href>` |
| `role="dialog"` | Fenetre modale | Preferer `<dialog>` |
| `role="alert"` | Message urgent | `<div role="alert">` |
| `role="status"` | Mise a jour non urgente | `<div role="status">` |
| `role="tablist/tab/tabpanel"` | Interface a onglets | Pas d'equivalent natif |
| `role="menu/menuitem"` | Menu d'application | Pas d'equivalent natif |
| `role="tree/treeitem"` | Arborescence | Pas d'equivalent natif |
| `role="grid/row/gridcell"` | Grille interactive | `<table>` pour data |
| `role="navigation"` | Zone de navigation | Preferer `<nav>` |
| `role="banner"` | En-tete principal | Preferer `<header>` |
| `role="main"` | Contenu principal | Preferer `<main>` |
| `role="complementary"` | Contenu complementaire | Preferer `<aside>` |
| `role="contentinfo"` | Pied de page | Preferer `<footer>` |

### States et Properties essentiels / Essential States and Properties

**States (changent dynamiquement) :**
- `aria-expanded="true/false"` : element ouvrable (accordion, dropdown, menu).
- `aria-selected="true/false"` : element selectionne (tab, option, treeitem).
- `aria-checked="true/false/mixed"` : case a cocher, switch.
- `aria-pressed="true/false"` : bouton toggle.
- `aria-disabled="true"` : element desactive (preferer `disabled` natif quand possible).
- `aria-hidden="true"` : masque l'element aux technologies d'assistance. **ATTENTION** : ne jamais utiliser sur un element focalisable.
- `aria-invalid="true"` : champ en erreur.
- `aria-busy="true"` : element en cours de chargement.
- `aria-current="page/step/true"` : element courant dans une navigation ou un processus.

**Properties (generalement statiques) :**
- `aria-label="string"` : nom accessible quand le texte visible n'est pas suffisant.
- `aria-labelledby="id"` : reference un autre element comme label.
- `aria-describedby="id"` : reference un element fournissant une description supplementaire.
- `aria-required="true"` : champ obligatoire (preferer `required` natif).
- `aria-live="polite/assertive"` : region dont les mises a jour sont annoncees aux lecteurs d'ecran.
- `aria-controls="id"` : identifie l'element controle par l'element courant.
- `aria-owns="id"` : declare une relation parent-enfant quand le DOM ne la reflète pas.
- `aria-haspopup="true/menu/dialog/listbox"` : indique qu'un element ouvre un popup.

### Patterns ARIA courants / Common ARIA Patterns

**Modal Dialog:**
```html
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Confirm deletion</h2>
  <p id="dialog-desc">This action cannot be undone.</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```
- Gerer le focus trap : pieger le focus dans le dialog.
- Restaurer le focus sur l'element declencheur a la fermeture.
- Appliquer `inert` sur le contenu derriere le dialog (ou `aria-hidden`).

**Tabs:**
```html
<div role="tablist" aria-label="Settings sections">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">General</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2" tabindex="-1">Security</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">...</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>...</div>
```
- Navigation fleches gauche/droite entre les tabs.
- Seul le tab selectionne est dans l'ordre Tab (les autres ont `tabindex="-1"`).

**Combobox (Autocomplete):**
```html
<label for="search">Search</label>
<input id="search" role="combobox" aria-expanded="true" aria-controls="results"
       aria-activedescendant="option-2" aria-autocomplete="list">
<ul id="results" role="listbox">
  <li id="option-1" role="option">Result 1</li>
  <li id="option-2" role="option" aria-selected="true">Result 2</li>
</ul>
```

---

## 3. Keyboard Navigation

### Patterns de navigation clavier / Keyboard Navigation Patterns

Implementer ces patterns de navigation clavier pour chaque type de composant interactif.

| Component | Tab | Arrow Keys | Enter/Space | Escape |
|---|---|---|---|---|
| **Button** | Focus | - | Activate | - |
| **Link** | Focus | - | Navigate | - |
| **Checkbox** | Focus | - | Toggle | - |
| **Radio Group** | Focus group | Move selection | - | - |
| **Tabs** | Focus tablist | Switch tab | - | - |
| **Menu** | Open/Focus | Navigate items | Select item | Close |
| **Dialog** | Focus trap | - | - | Close |
| **Combobox** | Focus input | Navigate options | Select option | Close listbox |
| **Tree** | Focus tree | Navigate/expand/collapse | Activate | - |
| **Accordion** | Focus headers | Move between headers | Toggle panel | - |

### Focus Management

- Utiliser `tabindex="0"` pour rendre un element non-natif focalisable dans l'ordre normal.
- Utiliser `tabindex="-1"` pour rendre un element programmatiquement focalisable mais pas dans l'ordre Tab.
- Ne jamais utiliser `tabindex` > 0 : cela brise l'ordre naturel de navigation.
- Gerer le focus trap dans les modals avec une boucle : dernier element focalisable -> premier element focalisable.
- Utiliser l'attribut `inert` (natif HTML) pour desactiver l'interaction sur le contenu derriere un modal/overlay.
- Apres une action destructive (suppression d'element), deplacer le focus vers l'element precedent ou suivant logique.

### Focus Visible Styling

```css
/* Reset browser defaults and provide custom focus indicator */
:focus-visible {
  outline: 2px solid var(--ds-color-focus);
  outline-offset: 2px;
  border-radius: var(--ds-border-radius-sm);
}

/* Remove outline for mouse clicks while keeping for keyboard */
:focus:not(:focus-visible) {
  outline: none;
}

/* Ensure sufficient contrast for focus indicator */
/* WCAG 2.4.7 requires visible focus; 2.4.13 AAA defines minimum area */
@media (forced-colors: active) {
  :focus-visible {
    outline: 2px solid Highlight;
  }
}
```

---

## 4. Screen Reader Compatibility

### Tester avec les lecteurs d'ecran / Testing with Screen Readers

Tester systematiquement avec au minimum deux combinaisons lecteur d'ecran + navigateur.

| Screen Reader | OS | Browser | Market Share |
|---|---|---|---|
| **NVDA** | Windows | Firefox, Chrome | ~30% |
| **JAWS** | Windows | Chrome, Edge | ~40% |
| **VoiceOver** | macOS/iOS | Safari | ~25% |
| **TalkBack** | Android | Chrome | ~5% |

**Checklist de test lecteur d'ecran / Screen Reader Testing Checklist:**
1. Naviguer la page avec Tab : verifier que tous les elements interactifs sont atteignables et annonces correctement.
2. Naviguer par headings (H key) : verifier la hierarchie `h1` > `h2` > `h3` sans sauts.
3. Naviguer par landmarks : verifier que `<nav>`, `<main>`, `<aside>`, `<footer>` sont annonces.
4. Remplir un formulaire : verifier que les labels, les erreurs et les instructions sont annonces.
5. Interagir avec les composants complexes (tabs, accordions, menus) : verifier les annonces ARIA.
6. Verifier les live regions : les messages de statut, erreurs et notifications sont annonces sans deplacement du focus.
7. Verifier les images : les alt texts sont pertinents et les images decoratives sont ignorees.

### Techniques pour le texte visuellement cache / Visually Hidden Text Techniques

```css
/* Utility class for screen-reader-only text */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Allow sr-only elements to become visible on focus (skip links) */
.sr-only-focusable:focus,
.sr-only-focusable:active {
  position: static;
  width: auto;
  height: auto;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

---

## 5. Color Contrast & Visual Design

### Ratios de contraste / Contrast Ratios

| Element | Level AA | Level AAA |
|---|---|---|
| Normal text (< 18pt / < 14pt bold) | 4.5:1 | 7:1 |
| Large text (>= 18pt / >= 14pt bold) | 3:1 | 4.5:1 |
| UI components & graphical objects | 3:1 | 3:1 |
| Focus indicators | 3:1 | 3:1 |

**Outils de verification / Verification Tools:**
- Chrome DevTools : inspecteur de couleurs avec ratio de contraste integre.
- Stark (Figma plugin) : verification du contraste et simulation de daltonisme.
- WebAIM Contrast Checker : verification en ligne rapide.
- Polypane : navigateur de dev avec verification de contraste en temps reel.

### Ne pas s'appuyer uniquement sur la couleur / Do Not Rely on Color Alone

- Ajouter des icones ou motifs aux indicateurs colores (error = couleur rouge + icone erreur + texte).
- Utiliser des motifs ou hachures dans les graphiques en plus des couleurs.
- Tester avec un simulateur de daltonisme (protanopie, deuteranopie, tritanopie).
- Respecter `prefers-color-scheme` et `prefers-contrast` pour adapter les themes.

### Support High Contrast Mode

```css
@media (forced-colors: active) {
  .button {
    border: 1px solid ButtonText;
  }
  .icon {
    forced-color-adjust: auto;
  }
}

@media (prefers-contrast: more) {
  :root {
    --ds-color-border-default: var(--ds-color-gray-800);
    --ds-color-text-secondary: var(--ds-color-gray-800);
  }
}
```

---

## 6. Testing Tools & Strategies

### Outils automatises / Automated Tools

| Tool | Type | Coverage | Integration |
|---|---|---|---|
| **axe-core** | Library | ~57% des criteres WCAG | Jest, Cypress, Playwright, Storybook |
| **Lighthouse** | Audit | Score a11y (subset axe) | Chrome DevTools, CI |
| **Pa11y** | CLI/CI | WCAG 2.1 AA | CI pipeline |
| **WAVE** | Browser extension | Visual overlay | Manuel |
| **IBM Equal Access** | Library + extension | Rule-based | CI, browser |
| **Storybook a11y addon** | Storybook | axe-core per story | Development |

### Integration en CI / CI Integration

Automatiser les tests d'accessibilite dans le pipeline CI pour bloquer les regressions.

**Avec axe-core + Playwright / With axe-core + Playwright:**
```typescript
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("homepage has no accessibility violations", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag22aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});

test("login form accessibility", async ({ page }) => {
  await page.goto("/login");
  // Focus on form area specifically
  const results = await new AxeBuilder({ page })
    .include("#login-form")
    .withTags(["wcag2a", "wcag2aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

**Avec jest-axe / With jest-axe:**
```typescript
import { render } from "@testing-library/react";
import { axe, toHaveNoViolations } from "jest-axe";
expect.extend(toHaveNoViolations);

test("Button component is accessible", async () => {
  const { container } = render(<Button>Click me</Button>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Strategie de test en couches / Layered Testing Strategy

1. **Development time** : Storybook a11y addon + linter rules (eslint-plugin-jsx-a11y).
2. **Unit/Integration tests** : jest-axe assertions sur chaque composant.
3. **E2E tests** : axe-core + Playwright sur les parcours critiques.
4. **CI gate** : Lighthouse a11y score minimum (90+), zero violations axe.
5. **Manual audit** : audit trimestriel complet (keyboard, screen reader, zoom 200%).
6. **User testing** : sessions avec des utilisateurs en situation de handicap (annuel minimum).

---

## 7. Legal Compliance -- EAA, RGAA, Section 508

### European Accessibility Act (EAA) -- Directive 2019/882

L'EAA est une directive europeenne transposee en droit national par chaque etat membre, avec une date d'application au **28 juin 2025**.

The EAA is a European directive transposed into national law by each member state, with an application date of **June 28, 2025**.

**Perimetre / Scope:**
- Sites web et applications mobiles de services : e-commerce, banque, transport, telecommunications, media audiovisuels, ebooks.
- S'applique aux entreprises privees (pas uniquement le secteur public).
- Concerne les produits et services mis sur le marche apres juin 2025.

**Exigences techniques / Technical Requirements:**
- Conformite WCAG 2.1 AA minimum (EN 301 549 standard).
- Documentation de conformite (declaration d'accessibilite).
- Mecanisme de feedback utilisateur pour signaler les problemes d'accessibilite.
- Obligations de suivi et de reporting.

**Sanctions / Penalties:**
- Definies par chaque etat membre. Incluent amendes, interdiction de mise sur le marche, dommages-interets.
- Recours possibles par les utilisateurs et les associations.

### RGAA 4.1 (France)

Le Referentiel General d'Amelioration de l'Accessibilite est le referentiel francais, obligatoire pour le secteur public et certaines entreprises privees (CA > 250M euros).

**Specificites / Specificities:**
- Base sur WCAG 2.1 AA avec des criteres de test operationnels detailles.
- 106 criteres de controle regroupes en 13 thematiques.
- Obligation de publication d'une declaration d'accessibilite.
- Obligation de publication d'un schema pluriannuel (plan d'accessibilite).
- Sanction : 20 000 euros par service non conforme et par an.
- Audit par un expert certifie ou auto-evaluation.

### Section 508 (United States)

Le Section 508 du Rehabilitation Act s'applique aux agences federales americaines et aux organisations recevant des fonds federaux.

**Exigences / Requirements:**
- Conformite WCAG 2.0 AA (mise a jour vers 2.1 en cours de discussion).
- S'applique aux sites web, applications, documents, logiciels et materiel informatique.
- Voluntary Product Accessibility Template (VPAT) : document declaratif de conformite demande par les agences.

### Matrice de conformite / Compliance Matrix

| Regulation | Geography | Scope | Standard | Deadline |
|---|---|---|---|---|
| **EAA** | EU 27 | Private + public | WCAG 2.1 AA (EN 301 549) | June 2025 |
| **RGAA 4.1** | France | Public + large private | WCAG 2.1 AA | Active |
| **Section 508** | United States | Federal + funded | WCAG 2.0 AA | Active |
| **ADA** | United States | Private (case law) | WCAG 2.1 AA (de facto) | Active |
| **AODA** | Ontario, Canada | Public + large private | WCAG 2.0 AA | Active |
| **EN 301 549** | Europe | ICT procurement | WCAG 2.1 AA + extras | Active |

---

## 8. Implementation Checklist

### Checklist de conformite par composant / Per-Component Compliance Checklist

Appliquer cette checklist lors du developpement de chaque composant interactif :

- [ ] **Semantique HTML** : utiliser l'element HTML natif le plus semantique possible.
- [ ] **Nom accessible** : le composant a un nom accessible (label, aria-label, aria-labelledby).
- [ ] **Role** : le role ARIA est correct (ou derive de l'element HTML natif).
- [ ] **States** : les etats sont communiques (aria-expanded, aria-selected, aria-checked, aria-disabled, aria-invalid).
- [ ] **Keyboard** : le composant est entierement utilisable au clavier avec les patterns attendus.
- [ ] **Focus visible** : l'indicateur de focus est visible et a un contraste suffisant (3:1 minimum).
- [ ] **Focus management** : le focus est gere correctement (trap dans les modals, restauration apres fermeture).
- [ ] **Contraste** : les couleurs respectent les ratios de contraste (4.5:1 texte, 3:1 UI).
- [ ] **Responsive** : le composant fonctionne a 200% de zoom et a 320px de largeur.
- [ ] **Motion** : les animations respectent `prefers-reduced-motion`.
- [ ] **Screen reader** : le composant est correctement annonce par NVDA/VoiceOver.
- [ ] **Error handling** : les erreurs sont communiquees textuellement et associees au champ via `aria-describedby`.
- [ ] **Target size** : les cibles interactives font au minimum 24x24 CSS pixels (WCAG 2.2).
- [ ] **Test automatise** : un test axe-core passe sans violation.

---

## References

- W3C, *Web Content Accessibility Guidelines (WCAG) 2.2* -- https://www.w3.org/TR/WCAG22/
- W3C, *ARIA Authoring Practices Guide* -- https://www.w3.org/WAI/ARIA/apg/
- European Accessibility Act (Directive 2019/882) -- https://eur-lex.europa.eu/eli/dir/2019/882
- RGAA 4.1 -- https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/
- Section 508 -- https://www.section508.gov
- Deque, *axe-core Rules* -- https://github.com/dequelabs/axe-core
- Heydon Pickering, *Inclusive Components* (2019)
- Sara Soueidan, *Practical Accessibility* (2024)
- WebAIM Million Report -- https://webaim.org/projects/million/
