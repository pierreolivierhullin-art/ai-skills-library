# Outils de Test A11y — Automatisés et Manuels

## Overview

Référence complète des outils de test d'accessibilité, de leur intégration dans la chaîne CI/CD, et des protocoles de tests manuels. Les outils automatisés détectent environ 30 à 40% des problèmes d'accessibilité WCAG AA — les tests manuels et avec lecteurs d'écran restent indispensables pour atteindre la conformité.

**Répartition réaliste** :
- Outils automatisés : 30–40% des violations WCAG détectables
- Tests clavier manuels : +20% supplémentaires
- Tests avec lecteurs d'écran : +30% supplémentaires
- Tests utilisateurs avec AT : +10% supplémentaires

---

## Tests Automatisés

### axe-core — La Référence

axe-core est le moteur de test d'accessibilité open-source le plus utilisé, développé par Deque Systems. Il analyse le DOM et remonte les violations WCAG 2.1/2.2.

#### Intégration Jest / Vitest avec jest-axe

```bash
npm install --save-dev jest-axe @types/jest-axe
```

```typescript
// vitest.setup.ts ou jest.setup.ts
import { expect } from 'vitest';
import { toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);
```

```typescript
// __tests__/formulaire-connexion.test.tsx
import { render } from '@testing-library/react';
import { axe } from 'jest-axe';
import FormulaireConnexion from '../components/FormulaireConnexion';

describe('FormulaireConnexion — accessibilité', () => {
  it('ne doit avoir aucune violation axe', async () => {
    const { container } = render(<FormulaireConnexion />);
    const résultats = await axe(container);
    expect(résultats).toHaveNoViolations();
  });

  it('affiche les erreurs de validation de façon accessible', async () => {
    const { container, getByRole } = render(<FormulaireConnexion />);

    // Soumettre le formulaire vide pour déclencher les erreurs
    const boutonSoumettre = getByRole('button', { name: /se connecter/i });
    boutonSoumettre.click();

    // Vérifier que les erreurs sont accessibles
    const résultats = await axe(container, {
      rules: {
        'color-contrast': { enabled: false }, // Désactiver si les couleurs sont testées séparément
      },
    });
    expect(résultats).toHaveNoViolations();
  });

  it('mode sombre — contraste correct', async () => {
    document.documentElement.setAttribute('data-theme', 'dark');
    const { container } = render(<FormulaireConnexion />);
    const résultats = await axe(container, {
      runOnly: { type: 'tag', values: ['wcag2aa'] },
    });
    expect(résultats).toHaveNoViolations();
    document.documentElement.removeAttribute('data-theme');
  });
});
```

#### Configuration avancée axe

```typescript
// Configuration axe pour des règles spécifiques
const axeOptions = {
  // Cibler uniquement les critères WCAG 2.1 AA
  runOnly: {
    type: 'tag',
    values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'],
  },

  // Désactiver des règles spécifiques avec justification
  rules: {
    // La règle de contraste ne fonctionne pas bien sur les overlays
    'color-contrast': { enabled: false },

    // On teste le contenu dynamique séparément
    'aria-live-region': { enabled: false },
  },

  // Contexte : tester uniquement une partie de la page
  context: '#main-content',

  // Inclure les violations cachées (éléments display:none)
  iframes: true,
};

const résultats = await axe(container, axeOptions);

// Affichage détaillé des violations en cas d'échec
if (résultats.violations.length > 0) {
  console.error(
    'Violations axe détectées :',
    résultats.violations.map(v => ({
      id: v.id,
      impact: v.impact,
      description: v.description,
      help: v.helpUrl,
      éléments: v.nodes.map(n => n.html),
    }))
  );
}
```

#### Niveaux d'impact axe

| Impact | Signification | Exemple |
|---|---|---|
| `critical` | Bloque complètement l'accès | Image sans alt, formulaire sans label |
| `serious` | Accès très difficile | Contraste insuffisant, focus manquant |
| `moderate` | Accès difficile pour certains AT | aria-label manquant sur icône |
| `minor` | Conforme avec réserve | Utilisation non recommandée d'ARIA |

---

### Playwright avec axe-playwright

```bash
npm install --save-dev axe-playwright
```

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    baseURL: 'http://localhost:3000',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
  ],
});
```

```typescript
// tests/a11y/pages.spec.ts
import { test, expect } from '@playwright/test';
import { injectAxe, checkA11y, getViolations } from 'axe-playwright';

test.describe('Accessibilité des pages principales', () => {

  test.beforeEach(async ({ page }) => {
    // Attendre que la page soit stable avant le test
    await page.waitForLoadState('networkidle');
    await injectAxe(page);
  });

  test('Page d\'accueil', async ({ page }) => {
    await page.goto('/');
    await checkA11y(page, undefined, {
      axeOptions: {
        runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa'] },
      },
      detailedReport: true,
      detailedReportOptions: { html: true },
    });
  });

  test('Formulaire de connexion — états successifs', async ({ page }) => {
    await page.goto('/connexion');

    // État initial
    await checkA11y(page, '#formulaire-connexion');

    // Soumettre avec erreurs
    await page.click('button[type="submit"]');
    await page.waitForSelector('[role="alert"]');
    await checkA11y(page, '#formulaire-connexion');

    // Après connexion réussie
    await page.fill('#email', 'test@exemple.fr');
    await page.fill('#mot-de-passe', 'MotDePasseValide123!');
    await page.click('button[type="submit"]');
    await page.waitForURL('/tableau-de-bord');
    await checkA11y(page);
  });

  test('Modal de confirmation', async ({ page }) => {
    await page.goto('/commandes');
    await page.click('[data-testid="btn-supprimer-commande"]');

    // Attendre l'ouverture de la modal
    await page.waitForSelector('[role="dialog"]');

    // Tester l'accessibilité de la modal ouverte
    await checkA11y(page, '[role="dialog"]');

    // Tester le focus trap
    await page.keyboard.press('Tab');
    const focusedElement = await page.evaluate(() => document.activeElement?.getAttribute('data-testid'));
    expect(['btn-confirmer', 'btn-annuler', 'btn-fermer-modal']).toContain(focusedElement);
  });

  test('Pages avec contenu dynamique', async ({ page }) => {
    await page.goto('/tableau-de-bord');

    // Changer de filtre et vérifier la mise à jour
    await page.selectOption('#filtre-periode', '30j');
    await page.waitForSelector('[aria-busy="false"]'); // Attendre fin de chargement

    const violations = await getViolations(page);
    expect(violations.filter(v => v.impact === 'critical' || v.impact === 'serious')).toHaveLength(0);
  });
});
```

---

### Pipeline CI — GitHub Actions

```yaml
# .github/workflows/a11y.yml
name: Tests d'accessibilité

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  a11y-unit:
    name: Tests unitaires axe
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run test:a11y
        env:
          CI: true

  a11y-e2e:
    name: Tests E2E Playwright
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - name: Démarrer l'application
        run: npm run build && npm run start &
        env:
          NODE_ENV: production
      - name: Attendre que l'application soit prête
        run: npx wait-on http://localhost:3000 --timeout 60000
      - name: Tests Playwright a11y
        run: npx playwright test tests/a11y/
      - name: Publier le rapport Playwright
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30

  lighthouse-a11y:
    name: Score Lighthouse accessibilité
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci && npm run build
      - uses: treosh/lighthouse-ci-action@v11
        with:
          configPath: '.lighthouserc.json'
          serverBaseUrl: ${{ secrets.LHCI_SERVER_URL }}
          token: ${{ secrets.LHCI_TOKEN }}
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

```json
// .lighthouserc.json
{
  "ci": {
    "collect": {
      "startServerCommand": "npm run start",
      "url": [
        "http://localhost:3000",
        "http://localhost:3000/connexion",
        "http://localhost:3000/tableau-de-bord",
        "http://localhost:3000/produits"
      ],
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "categories:accessibility": ["error", { "minScore": 0.90 }],
        "categories:best-practices": ["warn", { "minScore": 0.85 }]
      }
    },
    "upload": {
      "target": "lhci",
      "serverBaseUrl": "https://lhci.monapp.fr"
    }
  }
}
```

---

### Limites des Tests Automatisés

Les outils automatisés **ne peuvent pas détecter** :

| Problème | Raison |
|---|---|
| Texte alternatif significatif (alt correct ≠ alt utile) | Ne peut pas évaluer la pertinence sémantique |
| Ordre de lecture logique | Détermine si l'ordre DOM est logique visuellement |
| Focus management dans les SPA | Comportement dynamique après navigation |
| Compréhensibilité des labels | Un label présent n'est pas forcément compréhensible |
| Expérience lecteur d'écran réelle | L'annonce textuelle n'est pas testée automatiquement |
| Erreurs de logique de form | La validation et les suggestions dépendent du contexte |
| Interactions complexes | Drag-and-drop, gestures, widgets multi-étapes |

---

## Lighthouse — Interprétation du Score

### Score d'accessibilité Lighthouse

Le score Lighthouse accessibilité est pondéré — certaines audits comptent plus que d'autres :

```
Score 0–49 : Critique — violations majeures, nombreux utilisateurs bloqués
Score 50–74 : Insuffisant — problèmes significatifs à corriger en priorité
Score 75–89 : Acceptable — améliorations nécessaires pour la conformité AA
Score 90–100 : Bon — peu de problèmes automatisables, compléter avec tests manuels
```

**Limites importantes** :
- Un score de 100 ne signifie PAS la conformité WCAG AA — Lighthouse ne teste que ~30% des critères
- Le score est pondéré et peut masquer une violation critique de faible poids statistique
- Tester plusieurs URLs représentatives (page d'accueil seule n'est pas suffisant)

### Audits Lighthouse clés pour l'accessibilité

```
Audits à impact élevé :
├── image-alt : images avec alt manquant ou vide sur images informatives
├── button-name : boutons sans nom accessible
├── form-field-multiple-labels : champs avec plusieurs labels conflictuels
├── label : champs de formulaire sans label associé
├── link-name : liens sans texte accessible
├── color-contrast : texte avec contraste insuffisant (4,5:1 pour texte normal)
├── html-has-lang : attribut lang manquant sur <html>
├── document-title : <title> manquant ou vide
└── meta-viewport : user-scalable=no dans la meta viewport (bloque le zoom)

Audits à impact moyen :
├── aria-allowed-attr : attributs ARIA non valides pour le rôle
├── aria-required-attr : attributs ARIA obligatoires manquants
├── aria-roles : rôles ARIA invalides
├── aria-valid-attr-value : valeurs ARIA invalides
├── bypass : pas de mécanisme de saut (skip link)
├── duplicate-id : IDs dupliqués dans le DOM
├── focus-traps : focus trap non libérable
├── heading-order : hiérarchie de titres non logique
└── tabindex : tabindex > 0 (casse l'ordre de navigation)
```

---

## Accessibility Insights for Web

Extension Chrome/Edge développée par Microsoft. Deux modes principaux :

### FastPass (5 minutes)

Analyse automatique des problèmes les plus courants — équivalent axe-core sur la page active :
1. Installer l'extension
2. Cliquer sur "FastPass"
3. Exécuter les vérifications automatiques
4. Parcourir la checklist manuelle des tabstops (ordre de focus)

### Assessment (complet — 3h à une journée)

Processus guidé couvrant tous les critères WCAG 2.1 AA avec instructions de test manuel pour chaque critère :
- 24 groupes de tests
- Instructions pas-à-pas pour chaque critère
- Rapport exportable en HTML/CSV

---

## Protocole de Test au Clavier — 20 Points

Effectuer ce protocole sur chaque page ou flux principal :

```
NAVIGATION DE BASE
[ ] 1. Tab depuis l'URL : le premier élément focusé est le skip link ou le premier élément interactif
[ ] 2. Tab traverse tous les éléments interactifs dans l'ordre logique de lecture
[ ] 3. Shift+Tab permet de revenir en arrière dans le même ordre
[ ] 4. L'indicateur de focus est visible sur chaque élément (pas outline: none)
[ ] 5. Aucun élément interactif n'est ignoré par Tab

CONTRÔLES INTERACTIFS
[ ] 6. Tous les boutons répondent à Enter et Space
[ ] 7. Les liens répondent à Enter
[ ] 8. Les cases à cocher basculent avec Space
[ ] 9. Les boutons radio se sélectionnent avec les flèches dans un groupe
[ ] 10. Les listes déroulantes s'ouvrent avec Alt+Flèche bas (Windows) ou Space

WIDGETS COMPLEXES
[ ] 11. Les menus déroulants : ouverture, navigation flèches, Escape pour fermer
[ ] 12. Les accordéons : Enter/Space pour ouvrir/fermer
[ ] 13. Les onglets : flèches gauche/droite pour naviguer, Tab pour aller dans le contenu
[ ] 14. Les modals : focus se déplace dans la modal à l'ouverture, Escape ferme, focus revient au déclencheur

FORMULAIRES
[ ] 15. Tous les champs sont atteignables et remplissables au clavier
[ ] 16. La soumission fonctionne avec Enter sur les champs texte ou Tab vers le bouton Submit
[ ] 17. Les erreurs de validation reçoivent le focus ou sont annoncées

NAVIGATION ET SKIP
[ ] 18. Le skip link "Aller au contenu principal" est fonctionnel (visible au focus)
[ ] 19. Après navigation dans une SPA, le focus est géré (déplacé vers le nouveau contenu ou le titre de page)
[ ] 20. Aucun piège au clavier non intentionnel (Tab peut toujours sortir de chaque composant)
```

---

## Tests avec Lecteurs d'Écran

### NVDA + Chrome (Windows) — Le Duo Standard

NVDA (NonVisual Desktop Access) est gratuit et open-source. Chrome est le navigateur avec le meilleur support ARIA.

**Installation** : https://www.nvaccess.org/download/

#### Raccourcis NVDA essentiels

```
NAVIGATION GÉNÉRALE
Insert+F7           : Ouvrir la liste des éléments (liens, titres, formulaires, landmarks)
Insert+F5           : Ouvrir la liste des champs de formulaire
Insert+F3           : Trouver un texte dans la page
Insert+Ctrl+F       : Trouver du texte (mode navigation)

LECTURE
Insert+Flèche bas   : Lire depuis la position actuelle
Insert+Ctrl          : Arrêter la lecture
Insert+Tab           : Lire le focus actuel et ses propriétés
Insert+F             : Annoncer le format actuel (lors de la lecture)

MODES DE NAVIGATION
Insert+Space         : Basculer entre mode navigation et mode application
Insert+V             : Activer/désactiver le mode virtuel

NAVIGATION PAR ÉLÉMENTS
H                   : Titre suivant
Shift+H             : Titre précédent
1-6                 : Titre de niveau correspondant (1=h1, 2=h2...)
F                   : Champ de formulaire suivant
B                   : Bouton suivant
L                   : Lien suivant
T                   : Tableau suivant
D                   : Region/Landmark suivant
G                   : Graphique suivant
```

#### Protocole de test NVDA

```
AVANT DE COMMENCER
1. Activer NVDA (Ctrl+Alt+N ou raccourci bureau)
2. Ouvrir Chrome et naviguer vers la page
3. S'assurer que NVDA lit bien la page (Insert+Flèche bas)

VÉRIFICATIONS STRUCTURELLES
4. Insert+F7 → onglet Titres : la hiérarchie est-elle logique ?
5. Insert+F7 → onglet Liens : les libellés de liens sont-ils descriptifs ?
6. Insert+F7 → onglet Landmarks : page > header/nav/main/footer présents ?
7. Naviguer avec H : l'ordre des titres représente-t-il le contenu ?

FORMULAIRES
8. Naviguer avec F jusqu'aux champs
9. Vérifier que chaque champ est annoncé avec : nom + type + valeur + état
10. Exemple attendu : "Adresse email, édition, vide, obligatoire"
11. Soumettre avec erreurs et vérifier les annonces

CONTENU DYNAMIQUE
12. Déclencher une action AJAX (filtre, bouton)
13. Vérifier que le résultat est annoncé (live region) ou que le focus est déplacé
14. Tester une notification de succès/erreur

IMAGES
15. Naviguer avec G
16. Vérifier que les images informatives ont un alt descriptif
17. Vérifier que les images décoratives sont ignorées (alt vide)
```

---

### VoiceOver + Safari (macOS)

VoiceOver est intégré à macOS. Safari est le navigateur recommandé pour VoiceOver.

**Activation** : Cmd+F5 (ou Menu Pomme > Préférences Système > Accessibilité > VoiceOver)

#### Raccourcis VoiceOver essentiels

```
NAVIGATION GÉNÉRALE
VO = Ctrl+Option (touches modificatrices VoiceOver)

VO+A                : Lire depuis la position actuelle
VO+S                : Arrêter la lecture
VO+Shift+M          : Ouvrir le menu contextuel VoiceOver
VO+U                : Rotor (sélectionner le type de navigation)

ROTOR (VO+U) — Navigation par catégorie
← → dans le Rotor   : Choisir la catégorie (Titres, Liens, Formulaires, Landmarks...)
↑ ↓ dans le Rotor   : Naviguer dans la catégorie sélectionnée

NAVIGATION DANS LA PAGE
VO+Cmd+H            : Titre suivant
VO+Cmd+J            : Champ de formulaire suivant
VO+Cmd+L            : Lien suivant
VO+Cmd+T            : Tableau suivant

FORMULAIRES
VO+Shift+Down       : Entrer dans un formulaire (mode formulaire)
Escape              : Sortir du mode formulaire
Tab                 : Prochain champ interactif
```

#### Particularités VoiceOver à tester

```
ARIA-MODAL
VoiceOver iOS ignore aria-modal="true" sur les modals.
Solution : masquer le contenu hors modal avec aria-hidden="true"
Test : ouvrir une modal → VO ne doit pas permettre d'atteindre le contenu en arrière-plan

LIVE REGIONS
VoiceOver annonce les role="alert" et aria-live="polite" différemment de NVDA.
Tester que les notifications dynamiques sont bien annoncées.

TABLEAUX COMPLEXES
VoiceOver lit les tableaux différemment : activer la navigation tableau avec VO+Shift+↑↓←→
```

---

### JAWS + Edge (Windows) — Environnement Entreprise

JAWS (Job Access With Speech) est le lecteur d'écran le plus utilisé en entreprise (payant). Edge est recommandé avec JAWS pour le support ARIA.

```
RACCOURCIS JAWS ESSENTIELS
Insert+F6           : Liste des titres
Insert+F5           : Liste des champs de formulaire
Insert+F7           : Liste des liens
Insert+F3           : Trouver du texte
H                   : Titre suivant (mode navigation)
Tab                 : Champ de formulaire suivant
F                   : Formulaire suivant
R                   : Région/Landmark suivante

MODE FORMULAIRE (JAWS)
Entrer : Insert+F5 ou Tab sur un champ actif
Sortir : Numpad+Plus ou Escape
```

---

## Tests Mobile

### VoiceOver iOS

**Activer** : Réglages > Accessibilité > VoiceOver (ou triple-clic sur bouton latéral)

```
GESTES ESSENTIELS
Glisser 1 doigt droite/gauche  : Élément suivant/précédent
Double-tap                     : Activer l'élément sélectionné
Glisser 3 doigts haut/bas      : Faire défiler la page
Glisser 2 doigts haut          : Lire depuis le début
Rotor : tordre 2 doigts        : Choisir mode navigation (Titres, Mots, Caractères...)

POINTS DE VIGILANCE IOS
- aria-modal ignoré : tester le confinement des modals manuellement
- focus-trap : s'assurer que le focus ne sort pas des modals
- touch target : cibles minimum 44×44 pt physiques
- Input > zoom automatique : font-size < 16px déclenche le zoom (éviter)
```

### TalkBack Android

**Activer** : Paramètres > Accessibilité > TalkBack

```
GESTES ESSENTIELS
Glisser droite/gauche          : Élément suivant/précédent
Double-tap                     : Activer l'élément
Glisser 2 doigts haut/bas      : Faire défiler
Glisser 3 doigts en L          : Ouvrir le menu de navigation globale

POINTS DE VIGILANCE ANDROID
- Chrome + TalkBack : le support ARIA est généralement bon sur Chrome
- role="application" : empêche TalkBack d'utiliser les gestes standard — éviter sauf cas très spécifiques
- Texte dynamique : les live regions fonctionnent bien avec aria-live="polite"
```

---

## Outils de Contraste des Couleurs

### Colour Contrast Analyser (Desktop)

Application gratuite (Windows/macOS) par TPGi. Permet de mesurer le contraste entre deux couleurs en utilisant le pipette pour échantillonner des couleurs à l'écran.

**Utilisation** :
1. Télécharger sur https://www.tpgi.com/color-contrast-checker/
2. Utiliser la pipette "Foreground" sur la couleur du texte
3. Utiliser la pipette "Background" sur la couleur du fond
4. Lire le ratio et les indicateurs AA/AAA

Particulièrement utile pour les éléments non textuels (icônes, bordures, composants UI) — Lighthouse ne les analyse pas toujours bien.

### Vérification via DevTools Chrome

```javascript
// Console Chrome DevTools — vérifier le contraste d'un élément
// Sélectionner un élément → Computed → rechercher color
// Ou utiliser l'onglet Accessibility → Computed Properties

// Programmatique en tests
async function getComputedContrast(page: Page, selector: string) {
  return page.evaluate((sel) => {
    const el = document.querySelector(sel);
    if (!el) return null;
    const styles = window.getComputedStyle(el);
    return {
      color: styles.color,
      backgroundColor: styles.backgroundColor,
      fontSize: styles.fontSize,
      fontWeight: styles.fontWeight,
    };
  }, selector);
}
```

### Bookmarklet Contrast Ratio

```javascript
// Bookmarklet à ajouter aux favoris pour tester les contrastes en live
javascript:(function(){
  var s=document.createElement('script');
  s.src='https://accessibility-bookmarklets.org/build/highlight-tab.js';
  document.head.appendChild(s);
})();
```

---

## Arbre d'Accessibilité — DevTools Navigateur

### Chrome DevTools — Onglet Accessibility

1. Ouvrir DevTools (F12)
2. Sélectionner un élément dans l'inspecteur
3. Cliquer sur l'onglet "Accessibility"
4. Consulter :
   - **Computed Properties** : nom accessible, rôle, description
   - **Accessibility Tree** : structure de l'arbre ARIA

### Firefox DevTools — Panneau Accessibility

1. Ouvrir DevTools (F12)
2. Cliquer sur l'onglet "Accessibility"
3. Activer le panneau (si désactivé)
4. Explorer l'arbre d'accessibilité interactif
5. Utiliser le sélecteur de propriétés pour filtrer (contraste, nom, description)

**Utilisation pratique** :
```
Vérifier qu'un bouton a un nom accessible :
1. Inspecter le bouton
2. Onglet Accessibility → Computed Properties
3. "Name" doit être non vide et descriptif
4. "Role" doit être "button"
5. "State" doit indiquer l'état correct (expanded, selected, etc.)
```

---

## IBM Equal Access Checker

Extension Chrome/Firefox gratuite développée par IBM. Couvre WCAG 2.1 et 2.2, avec quelques règles supplémentaires pour IBMA (IBM Accessibility).

**Avantage par rapport à axe** : classifications différentes, peut détecter des problèmes non couverts par axe. Recommandé d'utiliser les deux en complément.

**Lancer en CI** :
```bash
npm install --save-dev accessibility-checker
```
```typescript
import { getCompliance } from 'accessibility-checker';

const results = await getCompliance(html, 'Mon-page-test');
// results.results : tableau des violations
// results.summary : résumé par catégorie
```

---

## aXe DevTools — Comparaison Free vs Pro

| Fonctionnalité | axe DevTools Free | axe DevTools Pro |
|---|---|---|
| Règles WCAG 2.1 AA | ~55 règles | 100+ règles |
| Intelligent Guided Tests | Non | Oui (guide les tests manuels) |
| Intégration CI | axe-core open-source | API + reporting centralisé |
| Tests composants React/Vue | jest-axe (open-source) | Modules spécialisés |
| Rapport PDF/export | Non | Oui |
| Support WCAG 2.2 | Partiel | Complet |
| Prix | Gratuit | ~$100/utilisateur/mois |

**Recommandation** : axe DevTools Free + jest-axe + Playwright est suffisant pour la plupart des projets. Pro est justifié pour les organismes soumis à audit RGAA obligatoire.

---

## Stratégie de Test Recommandée

```
DÉVELOPPEMENT (par composant)
├── jest-axe dans les tests unitaires de chaque composant
├── Storybook a11y addon (basé sur axe) pour chaque story
└── Vérification manuelle des nouvelles interactions clavier

INTÉGRATION (par PR)
├── Playwright a11y sur les pages critiques (parcours utilisateur)
├── Lighthouse CI sur les URLs principales (score minimum 90)
└── Revue de code : checklist accessibilité

RELEASE (avant mise en production)
├── Test clavier complet sur les nouveaux flux (protocole 20 points)
├── Test NVDA+Chrome sur les formulaires et modals
├── Test VoiceOver+Safari si audience Mac/iOS significative
└── Rapport de conformité documenté

TRIMESTRIEL (conformité RGAA)
├── Audit complet avec Accessibility Insights Assessment
├── Test avec utilisateurs utilisant des technologies d'assistance
└── Mise à jour de la déclaration d'accessibilité
```
