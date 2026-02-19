---
name: accessibility
version: 1.0.0
description: >
  Web accessibility WCAG 2.1 2.2, a11y testing, ARIA attributes, screen reader compatibility,
  keyboard navigation, color contrast, accessible forms, focus management, semantic HTML,
  axe-core testing, accessible design patterns, WAI-ARIA, disability inclusive design,
  RGAA compliance, legal accessibility requirements, accessibilité numérique
---

# Accessibilité Web — WCAG et A11y en Production

## Quand Activer ce Skill

Ce skill est pertinent quand :
- L'application doit être conforme WCAG 2.1 AA (standard européen, RGAA en France)
- Une obligation légale d'accessibilité existe (services publics, >250 salariés en France)
- Tu veux étendre ton audience (15% de la population mondiale en situation de handicap)
- Les audits Lighthouse accessibilité sont en dessous de 90
- Les tests automatisés signalent des violations axe-core
- Tu conçois des formulaires, modals, ou navigation complexe

---

## WCAG — Les 4 Principes POUR

**P** — Perceptible : tout contenu doit être perceptible par au moins un sens
**O** — Opérable : toutes les fonctions doivent être utilisables au clavier
**U** — Understandable (Compréhensible) : contenu et interface compréhensibles
**R** — Robuste : compatible avec les technologies d'assistance (lecteurs d'écran)

**Niveaux** : A (minimum), **AA (standard légal)**, AAA (optimal)

---

## HTML Sémantique — La Base

```html
<!-- ❌ Div soup — aucune sémantique -->
<div class="header">
  <div class="nav">
    <div onclick="goto('/')">Accueil</div>
    <div onclick="goto('/produits')">Produits</div>
  </div>
</div>
<div class="main-content">
  <div class="article-title">Mon Article</div>
  <div class="article-body">Contenu...</div>
</div>

<!-- ✅ HTML sémantique — lecteurs d'écran comprennent la structure -->
<header>
  <nav aria-label="Navigation principale">
    <ul>
      <li><a href="/">Accueil</a></li>
      <li><a href="/produits">Produits</a></li>
    </ul>
  </nav>
</header>
<main>
  <article>
    <h1>Mon Article</h1>
    <p>Contenu...</p>
  </article>
</main>
<footer>
  <p>© 2025 MonApp</p>
</footer>
```

### Hiérarchie des Titres

```html
<!-- Une seule <h1> par page — titre principal -->
<h1>Catalogue Produits</h1>

  <h2>Électronique</h2>
    <h3>Smartphones</h3>
      <h4>Apple</h4>
    <h3>Ordinateurs</h3>

  <h2>Mode</h2>
    <h3>Femmes</h3>
    <h3>Hommes</h3>

<!-- Ne jamais sauter de niveau (h1 → h3) pour des raisons visuelles -->
<!-- Utiliser CSS pour ajuster la taille, pas les niveaux de titres -->
```

---

## ARIA — Accessible Rich Internet Applications

### Règle d'or : No ARIA > Bad ARIA

```html
<!-- ❌ ARIA inutile sur des éléments sémantiques natifs -->
<button role="button" aria-pressed="false">Cliquer</button>
<!-- role="button" est redondant sur <button> -->

<!-- ✅ ARIA seulement pour les widgets custom -->
<div role="button" tabindex="0" aria-pressed="false"
     onclick="toggle()" onkeydown="handleKey(event)">
  Basculer
</div>

<!-- ✅ Mieux : utiliser <button> (sémantique native) -->
<button type="button" aria-pressed="false" onclick="toggle()">
  Basculer
</button>
```

### aria-label, aria-labelledby, aria-describedby

```html
<!-- aria-label : quand le texte visible est insuffisant -->
<button aria-label="Fermer la modal">✕</button>
<button aria-label="Supprimer l'article iPhone 15">🗑</button>

<!-- aria-labelledby : associer à un titre existant -->
<section aria-labelledby="titre-stats">
  <h2 id="titre-stats">Statistiques du mois</h2>
  <p>CA : 45 000 EUR</p>
</section>

<!-- aria-describedby : description supplémentaire -->
<input
  type="password"
  aria-describedby="aide-password"
  aria-required="true"
>
<p id="aide-password">
  Minimum 8 caractères, une majuscule, un chiffre.
</p>
```

### Live Regions — Notifications Dynamiques

```html
<!-- Annonces pour les lecteurs d'écran sans déplacer le focus -->

<!-- aria-live="polite" : annonce à la fin du message en cours -->
<div aria-live="polite" aria-atomic="true" class="sr-only" id="status">
  <!-- Contenu injecté par JS quand une action réussit -->
</div>

<!-- aria-live="assertive" : annonce immédiate (erreurs critiques) -->
<div role="alert" aria-live="assertive" class="sr-only" id="error-live">
</div>
```

```typescript
// Injecter dans la live region
function annoncer(message: string, type: 'polite' | 'assertive' = 'polite') {
  const region = document.getElementById(
    type === 'polite' ? 'status' : 'error-live'
  );
  if (region) {
    region.textContent = ''; // Reset pour forcer la ré-annonce
    setTimeout(() => { region.textContent = message; }, 50);
  }
}

// Exemple d'usage
async function soumettreFormulaire() {
  try {
    await api.créerCommande(données);
    annoncer('Commande créée avec succès');
  } catch {
    annoncer('Erreur lors de la création de la commande', 'assertive');
  }
}
```

---

## Navigation au Clavier

### Focus Management

```typescript
// Gestion du focus dans les modals
function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const déclencheurRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      déclencheurRef.current = document.activeElement as HTMLElement;
      // Déplacer le focus vers la modal
      const premierFocusable = modalRef.current?.querySelector<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      premierFocusable?.focus();
    } else {
      // Retourner le focus à l'élément déclencheur
      déclencheurRef.current?.focus();
    }
  }, [isOpen]);

  // Focus trap : empêcher le focus de sortir de la modal
  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Escape') { onClose(); return; }
    if (e.key !== 'Tab') return;

    const focusables = modalRef.current?.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    ) ?? [];
    const premier = focusables[0];
    const dernier = focusables[focusables.length - 1];

    if (e.shiftKey && document.activeElement === premier) {
      e.preventDefault();
      dernier.focus();
    } else if (!e.shiftKey && document.activeElement === dernier) {
      e.preventDefault();
      premier.focus();
    }
  }

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-titre"
      onKeyDown={handleKeyDown}
    >
      <h2 id="modal-titre">Confirmer la suppression</h2>
      {children}
      <button onClick={onClose}>Annuler</button>
    </div>
  );
}
```

### Skip Links

```html
<!-- Premier élément de la page : permet de sauter la navigation -->
<a href="#main-content" class="skip-link">
  Aller au contenu principal
</a>

<nav><!-- navigation... --></nav>

<main id="main-content" tabindex="-1">
  <!-- Contenu principal -->
</main>
```

```css
/* Visible seulement au focus clavier */
.skip-link {
  position: absolute;
  top: -100%;
  left: 1rem;
  background: #000;
  color: #fff;
  padding: 0.5rem 1rem;
  z-index: 9999;
}

.skip-link:focus {
  top: 1rem;
}
```

---

## Formulaires Accessibles

```typescript
function FormulaireConnexion() {
  const [erreurs, setErreurs] = useState<Record<string, string>>({});

  return (
    <form noValidate onSubmit={handleSubmit}>
      {/* Associer label et input avec htmlFor/id */}
      <div>
        <label htmlFor="email">
          Adresse email
          <span aria-hidden="true"> *</span>
          <span className="sr-only">(obligatoire)</span>
        </label>
        <input
          id="email"
          type="email"
          name="email"
          autoComplete="email"
          required
          aria-required="true"
          aria-invalid={!!erreurs.email}
          aria-describedby={erreurs.email ? 'email-error' : 'email-hint'}
        />
        <p id="email-hint" className="aide">
          Format : exemple@domaine.com
        </p>
        {erreurs.email && (
          <p id="email-error" role="alert" className="erreur">
            {erreurs.email}
          </p>
        )}
      </div>

      {/* Groupe de boutons radio avec fieldset/legend */}
      <fieldset>
        <legend>Type de compte</legend>
        <label>
          <input type="radio" name="type" value="personal" /> Personnel
        </label>
        <label>
          <input type="radio" name="type" value="business" /> Professionnel
        </label>
      </fieldset>

      <button type="submit">Se connecter</button>
    </form>
  );
}
```

---

## Contraste et Couleurs

### Ratios WCAG AA

| Contexte | Ratio minimum AA | Ratio optimal AAA |
|---|---|---|
| Texte normal (< 18px) | 4,5 : 1 | 7 : 1 |
| Texte grand (≥ 18px bold, ≥ 24px) | 3 : 1 | 4,5 : 1 |
| Composants UI (boutons, inputs) | 3 : 1 | — |

```css
/* ❌ Contraste insuffisant */
.badge-warning {
  color: #f59e0b; /* Jaune sur blanc : ratio 2,1:1 — insuffisant */
  background: #ffffff;
}

/* ✅ Contraste conforme AA */
.badge-warning {
  color: #92400e; /* Brun foncé sur jaune clair : ratio 4,8:1 */
  background: #fef3c7;
}
```

```typescript
// Vérifier le contraste programmatiquement
import { getContrastRatio } from 'colorjs.io';

function vérifierContraste(couleurTexte: string, couleurFond: string): {
  ratio: number;
  aa: boolean;
  aaa: boolean;
} {
  const ratio = getContrastRatio(couleurTexte, couleurFond);
  return {
    ratio,
    aa: ratio >= 4.5,
    aaa: ratio >= 7,
  };
}
```

### Ne pas Utiliser Seulement la Couleur

```html
<!-- ❌ Couleur seule pour indiquer une erreur -->
<input style="border: 2px solid red">

<!-- ✅ Couleur + icône + texte -->
<div class="champ-erreur">
  <input
    aria-invalid="true"
    aria-describedby="erreur-msg"
    class="bordure-rouge"
  >
  <p id="erreur-msg" class="message-erreur">
    <span aria-hidden="true">⚠️ </span>
    Ce champ est obligatoire
  </p>
</div>
```

---

## Tests d'Accessibilité

### Automatisés avec axe-core

```typescript
// Intégration axe dans Vitest/Jest
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('FormulaireConnexion est accessible', async () => {
  const { container } = render(<FormulaireConnexion />);
  const résultats = await axe(container);
  expect(résultats).toHaveNoViolations();
});

// Playwright avec axe
import { checkA11y, injectAxe } from 'axe-playwright';

test('Page d\'accueil — accessibilité', async ({ page }) => {
  await page.goto('/');
  await injectAxe(page);
  await checkA11y(page, '#main-content', {
    axeOptions: { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa'] } },
  });
});
```

### Tests Manuels — Checklist

```
Navigation clavier
├── ✅ Tab traverse tous les éléments interactifs dans l'ordre logique
├── ✅ Focus visible sur chaque élément (outline non supprimé)
├── ✅ Modal : focus trap + retour au déclencheur à la fermeture
└── ✅ Menu déroulant : navigation avec flèches

Lecteur d'écran (tester avec NVDA/Windows, VoiceOver/Mac)
├── ✅ Tous les images ont un alt descriptif (ou alt="" si décorative)
├── ✅ Les boutons ont un label compréhensible hors contexte
├── ✅ Les formulaires annoncent les erreurs
└── ✅ Les notifications dynamiques sont annoncées

Visuellement
├── ✅ Ratio de contraste ≥ 4,5:1 (texte normal)
├── ✅ Information pas transmise seulement par la couleur
├── ✅ Texte redimensionnable jusqu'à 200% sans perte de contenu
└── ✅ Pas d'animation auto-déclenchée > 3s (ou bouton pause)
```

---

## CSS Accessible

```css
/* Focus visible — ne jamais supprimer sans remplacer */
:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
  border-radius: 2px;
}

/* Classe utilitaire screen-reader only */
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

/* Respecter les préférences de mouvement réduit */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Mode contraste élevé */
@media (forced-colors: active) {
  .badge {
    border: 1px solid ButtonText; /* Forcer une bordure visible */
  }
}
```

---

## Références

- `references/wcag-criteria.md` — Critères WCAG 2.1/2.2 AA détaillés avec exemples
- `references/aria-patterns.md` — WAI-ARIA Authoring Practices (accordions, menus, tabs, etc.)
- `references/testing-tools.md` — axe-core, Lighthouse, NVDA, VoiceOver, Accessibility Insights
- `references/case-studies.md` — 4 cas : audit RGAA service public, refacto formulaire, modal accessible
