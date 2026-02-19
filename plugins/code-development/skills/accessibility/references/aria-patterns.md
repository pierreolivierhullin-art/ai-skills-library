# WAI-ARIA Patterns — Widgets Accessibles

## Overview

Référence complète des patterns WAI-ARIA Authoring Practices (APG) avec implémentation HTML/TypeScript pour chaque widget. Le principe fondamental : utiliser les éléments HTML natifs en priorité (un `<button>` n'a pas besoin de `role="button"`). ARIA ne remplace pas le HTML sémantique, il l'augmente pour les widgets complexes que HTML ne peut pas exprimer nativement.

**Règle d'or** : No ARIA is better than bad ARIA. Une page sans ARIA mais avec du HTML sémantique correct est plus accessible qu'une page avec de l'ARIA mal utilisé.

---

## Accordion (Accordéon)

### Structure et interactions

Un accordéon affiche une liste de sections pouvant être étendues ou réduites. Chaque section a un bouton déclencheur et un panneau de contenu.

**Interactions clavier** :
- `Enter` / `Space` : bascule l'état du panneau (ouvert/fermé)
- `Tab` : déplace le focus vers l'accordéon suivant ou hors du widget
- `Shift+Tab` : déplace le focus vers l'accordéon précédent ou hors du widget
- `Flèche bas` (optionnel) : focus sur l'accordéon suivant
- `Flèche haut` (optionnel) : focus sur l'accordéon précédent
- `Home` (optionnel) : focus sur le premier accordéon
- `End` (optionnel) : focus sur le dernier accordéon

### Implémentation TypeScript

```typescript
import { useState, useId, KeyboardEvent } from 'react';

interface AccordionItem {
  id: string;
  titre: string;
  contenu: React.ReactNode;
}

function Accordion({ items }: { items: AccordionItem[] }) {
  const [ouvert, setOuvert] = useState<string | null>(null);
  const baseId = useId();

  function basculer(itemId: string) {
    setOuvert(prev => prev === itemId ? null : itemId);
  }

  function handleKeyDown(e: KeyboardEvent, index: number) {
    const boutons = document.querySelectorAll<HTMLButtonElement>('[data-accordion-btn]');
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        boutons[Math.min(index + 1, boutons.length - 1)]?.focus();
        break;
      case 'ArrowUp':
        e.preventDefault();
        boutons[Math.max(index - 1, 0)]?.focus();
        break;
      case 'Home':
        e.preventDefault();
        boutons[0]?.focus();
        break;
      case 'End':
        e.preventDefault();
        boutons[boutons.length - 1]?.focus();
        break;
    }
  }

  return (
    <div>
      {items.map((item, index) => {
        const isOuvert = ouvert === item.id;
        const btnId = `${baseId}-btn-${item.id}`;
        const panelId = `${baseId}-panel-${item.id}`;

        return (
          <div key={item.id}>
            {/* Le bouton est l'élément déclencheur de l'accordéon */}
            <h3>
              <button
                id={btnId}
                data-accordion-btn
                aria-expanded={isOuvert}
                aria-controls={panelId}
                onClick={() => basculer(item.id)}
                onKeyDown={(e) => handleKeyDown(e, index)}
              >
                {item.titre}
                {/* Indicateur visuel — masqué aux lecteurs d'écran car aria-expanded suffit */}
                <span aria-hidden="true">{isOuvert ? '▲' : '▼'}</span>
              </button>
            </h3>

            {/* Panneau de contenu */}
            <div
              id={panelId}
              role="region"
              aria-labelledby={btnId}
              hidden={!isOuvert}
            >
              {item.contenu}
            </div>
          </div>
        );
      })}
    </div>
  );
}
```

**Erreurs fréquentes** :
- Oublier `aria-controls` qui relie le bouton à son panneau
- Utiliser `display: none` au lieu de `hidden` (les deux cachent aux lecteurs d'écran — `hidden` est préférable car plus sémantique)
- Mettre `role="region"` sans `aria-labelledby` (les régions sans nom sont inutiles)
- Imbriquer le bouton dans un `<div>` au lieu d'un titre (`<h2>`, `<h3>`) pour préserver la hiérarchie

---

## Combobox / Autocomplete

### Structure et interactions

Un combobox est un champ de saisie associé à une liste de suggestions. Il peut être editable (l'utilisateur tape) ou sélectionnable (liste fixe).

**Interactions clavier** :
- `Flèche bas` : ouvre la liste et déplace le focus sur la première option
- `Flèche haut` : ouvre la liste et déplace le focus sur la dernière option
- `Flèche bas/haut` (liste ouverte) : navigue dans les options
- `Enter` : sélectionne l'option mise en évidence
- `Escape` : ferme la liste et revient au champ
- `Tab` : ferme la liste et déplace le focus hors du combobox
- `Home` / `End` : aller à la première/dernière option

### Implémentation TypeScript

```typescript
import { useState, useRef, useId, KeyboardEvent } from 'react';

interface Option {
  id: string;
  label: string;
}

function Combobox({
  options,
  label,
  placeholder,
  onSelect
}: {
  options: Option[];
  label: string;
  placeholder?: string;
  onSelect: (option: Option) => void;
}) {
  const [valeur, setValeur] = useState('');
  const [listeVisible, setListeVisible] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLUListElement>(null);
  const baseId = useId();
  const inputId = `${baseId}-input`;
  const listId = `${baseId}-liste`;

  const optionsFiltrees = options.filter(o =>
    o.label.toLowerCase().includes(valeur.toLowerCase())
  );

  function getOptionId(index: number) {
    return `${baseId}-option-${index}`;
  }

  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (!listeVisible) setListeVisible(true);
        setActiveIndex(i => Math.min(i + 1, optionsFiltrees.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        if (!listeVisible) setListeVisible(true);
        setActiveIndex(i => Math.max(i - 1, 0));
        break;
      case 'Enter':
        e.preventDefault();
        if (activeIndex >= 0 && optionsFiltrees[activeIndex]) {
          sélectionner(optionsFiltrees[activeIndex]);
        }
        break;
      case 'Escape':
        setListeVisible(false);
        setActiveIndex(-1);
        inputRef.current?.focus();
        break;
      case 'Tab':
        setListeVisible(false);
        break;
    }
  }

  function sélectionner(option: Option) {
    setValeur(option.label);
    setListeVisible(false);
    setActiveIndex(-1);
    onSelect(option);
    inputRef.current?.focus();
  }

  return (
    <div>
      <label htmlFor={inputId}>{label}</label>

      <input
        ref={inputRef}
        id={inputId}
        type="text"
        role="combobox"
        aria-expanded={listeVisible}
        aria-autocomplete="list"
        aria-controls={listId}
        aria-activedescendant={activeIndex >= 0 ? getOptionId(activeIndex) : undefined}
        value={valeur}
        placeholder={placeholder}
        onChange={e => {
          setValeur(e.target.value);
          setListeVisible(true);
          setActiveIndex(-1);
        }}
        onFocus={() => setListeVisible(true)}
        onBlur={() => setTimeout(() => setListeVisible(false), 150)}
        onKeyDown={handleKeyDown}
        autoComplete="off"
      />

      {listeVisible && optionsFiltrees.length > 0 && (
        <ul
          ref={listRef}
          id={listId}
          role="listbox"
          aria-label={label}
        >
          {optionsFiltrees.map((option, index) => (
            <li
              key={option.id}
              id={getOptionId(index)}
              role="option"
              aria-selected={index === activeIndex}
              onClick={() => sélectionner(option)}
              onMouseEnter={() => setActiveIndex(index)}
            >
              {option.label}
            </li>
          ))}
        </ul>
      )}

      {listeVisible && optionsFiltrees.length === 0 && (
        /* Annonce "aucun résultat" aux lecteurs d'écran */
        <div role="status" aria-live="polite" className="sr-only">
          Aucun résultat pour "{valeur}"
        </div>
      )}
    </div>
  );
}
```

**Erreurs fréquentes** :
- Oublier `aria-activedescendant` — c'est ce qui annonce l'option mise en évidence sans déplacer le focus DOM
- Déplacer le focus DOM dans la liste (l'input doit garder le focus)
- Utiliser `aria-autocomplete="inline"` pour une liste filtrée (`"list"` est correct)
- Ne pas gérer le `onBlur` avec un délai — l'événement blur se déclenche avant le click sur une option

---

## Dialog / Modal

### Structure et interactions

Une boîte de dialogue modale capture le focus et empêche l'interaction avec le reste de la page jusqu'à fermeture.

**Interactions clavier** :
- `Tab` : déplace le focus parmi les éléments focusables de la modal (cycle)
- `Shift+Tab` : déplace le focus en arrière dans la modal (cycle)
- `Escape` : ferme la modal

### Implémentation TypeScript

```typescript
import { useEffect, useRef, useId, KeyboardEvent } from 'react';
import { createPortal } from 'react-dom';

const FOCUSABLES = [
  'a[href]',
  'button:not([disabled])',
  'input:not([disabled])',
  'select:not([disabled])',
  'textarea:not([disabled])',
  '[tabindex]:not([tabindex="-1"])',
].join(', ');

function Modal({
  isOpen,
  onClose,
  titre,
  children,
  taille = 'medium'
}: {
  isOpen: boolean;
  onClose: () => void;
  titre: string;
  children: React.ReactNode;
  taille?: 'small' | 'medium' | 'large';
}) {
  const modalRef = useRef<HTMLDivElement>(null);
  const déclencheurRef = useRef<HTMLElement | null>(null);
  const titreId = useId();

  useEffect(() => {
    if (isOpen) {
      // Mémoriser l'élément actif avant ouverture
      déclencheurRef.current = document.activeElement as HTMLElement;

      // Déplacer le focus vers le premier élément focusable de la modal
      setTimeout(() => {
        const premier = modalRef.current?.querySelector<HTMLElement>(FOCUSABLES);
        premier?.focus();
      }, 50);

      // Bloquer le scroll de la page
      document.body.style.overflow = 'hidden';
    } else {
      // Restaurer le focus
      déclencheurRef.current?.focus();
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  function handleKeyDown(e: KeyboardEvent<HTMLDivElement>) {
    if (e.key === 'Escape') {
      onClose();
      return;
    }

    if (e.key !== 'Tab') return;

    // Focus trap
    const focusables = Array.from(
      modalRef.current?.querySelectorAll<HTMLElement>(FOCUSABLES) ?? []
    );
    if (focusables.length === 0) return;

    const premier = focusables[0];
    const dernier = focusables[focusables.length - 1];

    if (e.shiftKey) {
      if (document.activeElement === premier) {
        e.preventDefault();
        dernier.focus();
      }
    } else {
      if (document.activeElement === dernier) {
        e.preventDefault();
        premier.focus();
      }
    }
  }

  if (!isOpen) return null;

  return createPortal(
    <>
      {/* Fond assombri — click ferme la modal */}
      <div
        className="modal-overlay"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* La modal elle-même */}
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titreId}
        className={`modal modal-${taille}`}
        onKeyDown={handleKeyDown}
      >
        <div className="modal-header">
          <h2 id={titreId}>{titre}</h2>
          <button
            onClick={onClose}
            aria-label={`Fermer : ${titre}`}
            className="modal-close"
          >
            <span aria-hidden="true">✕</span>
          </button>
        </div>

        <div className="modal-body">
          {children}
        </div>
      </div>
    </>,
    document.body
  );
}
```

**Erreurs fréquentes** :
- `aria-modal="true"` seul ne suffit pas pour tous les lecteurs d'écran — le focus trap JS reste nécessaire
- VoiceOver iOS ignore `aria-modal` — il faut masquer le reste de la page via `aria-hidden="true"` sur le contenu hors modal
- Ne pas restaurer le focus au déclencheur à la fermeture
- `role="alertdialog"` pour les confirmations critiques (différent de `role="dialog"`)

```typescript
// ✅ Masquer le contenu hors modal pour VoiceOver iOS
useEffect(() => {
  const mainContent = document.getElementById('root');
  if (isOpen && mainContent) {
    mainContent.setAttribute('aria-hidden', 'true');
  } else if (mainContent) {
    mainContent.removeAttribute('aria-hidden');
  }
}, [isOpen]);
```

---

## Menu de Navigation

### Structure et interactions

Un menu de navigation est une liste de liens de navigation principale. Différent d'un `role="menu"` (menu d'application) qui suit les interactions des menus d'applications de bureau.

**Interactions pour `<nav>` avec sous-menus** :
- `Enter` / `Space` : ouvre le sous-menu
- `Escape` : ferme le sous-menu, retourne au déclencheur
- `Flèche bas` : navigue dans le sous-menu ouvert
- `Flèche haut` : navigue en arrière dans le sous-menu
- `Tab` : ferme le sous-menu et avance dans le flux

```typescript
function NavigationMenu({ items }: { items: NavItem[] }) {
  const [sousMenuOuvert, setSousMenuOuvert] = useState<string | null>(null);

  return (
    <nav aria-label="Navigation principale">
      <ul role="list">
        {items.map(item => (
          <li key={item.id}>
            {item.sousItems ? (
              /* Item avec sous-menu */
              <>
                <button
                  aria-expanded={sousMenuOuvert === item.id}
                  aria-controls={`sous-menu-${item.id}`}
                  onClick={() => setSousMenuOuvert(
                    prev => prev === item.id ? null : item.id
                  )}
                >
                  {item.label}
                </button>
                <ul
                  id={`sous-menu-${item.id}`}
                  hidden={sousMenuOuvert !== item.id}
                  role="list"
                >
                  {item.sousItems.map(sousItem => (
                    <li key={sousItem.id}>
                      <a href={sousItem.href}>{sousItem.label}</a>
                    </li>
                  ))}
                </ul>
              </>
            ) : (
              /* Lien simple */
              <a
                href={item.href}
                aria-current={item.estActif ? 'page' : undefined}
              >
                {item.label}
              </a>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
}
```

**`role="menu"` vs `<nav>`** : utiliser `role="menu"` uniquement pour les menus d'application de type application de bureau (menus contextuels, barres de menu), pas pour la navigation de site.

---

## Tabs (Onglets)

### Structure et interactions

**Interactions clavier** :
- `Tab` : déplace le focus vers l'onglet actif, puis vers le panneau associé
- `Flèche gauche/droite` : navigue entre les onglets (activation automatique ou manuelle)
- `Home` : premier onglet
- `End` : dernier onglet
- `Enter` / `Space` : si activation manuelle, active l'onglet mis en évidence

### Implémentation TypeScript

```typescript
import { useState, useRef, useId, KeyboardEvent } from 'react';

interface TabItem {
  id: string;
  label: string;
  contenu: React.ReactNode;
}

function Tabs({
  items,
  activationAutomatique = true
}: {
  items: TabItem[];
  activationAutomatique?: boolean;
}) {
  const [ongletActif, setOngletActif] = useState(items[0]?.id ?? '');
  const [ongletMisEnEvidence, setOngletMisEnEvidence] = useState(items[0]?.id ?? '');
  const tabListRef = useRef<HTMLDivElement>(null);
  const baseId = useId();

  function getTabId(itemId: string) { return `${baseId}-tab-${itemId}`; }
  function getPanelId(itemId: string) { return `${baseId}-panel-${itemId}`; }

  function naviguer(direction: 'prev' | 'next' | 'first' | 'last') {
    const currentIndex = items.findIndex(i => i.id === ongletMisEnEvidence);
    let nextIndex = currentIndex;

    switch (direction) {
      case 'next': nextIndex = (currentIndex + 1) % items.length; break;
      case 'prev': nextIndex = (currentIndex - 1 + items.length) % items.length; break;
      case 'first': nextIndex = 0; break;
      case 'last': nextIndex = items.length - 1; break;
    }

    const nextId = items[nextIndex].id;
    setOngletMisEnEvidence(nextId);

    if (activationAutomatique) {
      setOngletActif(nextId);
    }

    // Déplacer le focus DOM vers le nouvel onglet
    document.getElementById(getTabId(nextId))?.focus();
  }

  function handleKeyDown(e: KeyboardEvent<HTMLDivElement>) {
    switch (e.key) {
      case 'ArrowRight': e.preventDefault(); naviguer('next'); break;
      case 'ArrowLeft': e.preventDefault(); naviguer('prev'); break;
      case 'Home': e.preventDefault(); naviguer('first'); break;
      case 'End': e.preventDefault(); naviguer('last'); break;
      case 'Enter':
      case ' ':
        if (!activationAutomatique) {
          e.preventDefault();
          setOngletActif(ongletMisEnEvidence);
        }
        break;
    }
  }

  return (
    <div>
      {/* Liste d'onglets */}
      <div
        ref={tabListRef}
        role="tablist"
        aria-label="Sections de contenu"
        onKeyDown={handleKeyDown}
      >
        {items.map(item => (
          <button
            key={item.id}
            id={getTabId(item.id)}
            role="tab"
            aria-selected={ongletActif === item.id}
            aria-controls={getPanelId(item.id)}
            tabIndex={ongletActif === item.id ? 0 : -1}
            onClick={() => {
              setOngletActif(item.id);
              setOngletMisEnEvidence(item.id);
            }}
          >
            {item.label}
          </button>
        ))}
      </div>

      {/* Panneaux de contenu */}
      {items.map(item => (
        <div
          key={item.id}
          id={getPanelId(item.id)}
          role="tabpanel"
          aria-labelledby={getTabId(item.id)}
          hidden={ongletActif !== item.id}
          tabIndex={0}
        >
          {item.contenu}
        </div>
      ))}
    </div>
  );
}
```

**Erreurs fréquentes** :
- `tabIndex={-1}` sur les onglets non sélectionnés — correct, la navigation se fait via les flèches
- Oublier `tabIndex={0}` sur le tabpanel — sans ça, l'utilisateur ne peut pas Tab dans le contenu du panneau
- Activer l'onglet dès la navigation au clavier sans laisser le choix à l'utilisateur (activation automatique vs manuelle)

---

## Tooltip

### Tooltip vs Description — Deux patterns distincts

**Tooltip (role="tooltip")** : complément d'information déclenchée au survol/focus, non indispensable à la compréhension :
```html
<!-- ✅ Tooltip informatif — déclenché au hover/focus -->
<button
  type="button"
  aria-describedby="aide-format"
  id="btn-aide"
>
  ℹ Format de date
</button>
<div
  id="aide-format"
  role="tooltip"
>
  Format attendu : JJ/MM/AAAA. Exemple : 15/06/2024
</div>
```

**aria-describedby** : description permanente associée à un champ (toujours dans le DOM) :
```html
<!-- ✅ Description permanente — toujours annoncée -->
<input
  type="text"
  id="code-postal"
  aria-describedby="aide-cp"
>
<p id="aide-cp">5 chiffres, par exemple : 75001</p>
```

```typescript
// ✅ Tooltip accessible avec délai pour éviter les clignements
function Tooltip({ contenu, children }: { contenu: string; children: React.ReactNode }) {
  const [visible, setVisible] = useState(false);
  const timerRef = useRef<number | null>(null);
  const tooltipId = useId();

  function afficher() {
    timerRef.current = window.setTimeout(() => setVisible(true), 500);
  }

  function masquer() {
    if (timerRef.current) clearTimeout(timerRef.current);
    setVisible(false);
  }

  return (
    <span
      style={{ position: 'relative', display: 'inline-block' }}
      onMouseEnter={afficher}
      onMouseLeave={masquer}
      onFocusCapture={afficher}
      onBlurCapture={masquer}
    >
      <span aria-describedby={visible ? tooltipId : undefined}>
        {children}
      </span>
      {visible && (
        <span
          id={tooltipId}
          role="tooltip"
          style={{
            position: 'absolute',
            bottom: '120%',
            left: '50%',
            transform: 'translateX(-50%)',
            whiteSpace: 'nowrap',
          }}
        >
          {contenu}
        </span>
      )}
    </span>
  );
}
```

---

## Alert et Status

### Différence entre rôles de live region

| Rôle | aria-live | Comportement | Usage |
|---|---|---|---|
| `role="alert"` | `assertive` | Interrompt le lecteur d'écran immédiatement | Erreurs critiques, alertes de sécurité |
| `role="status"` | `polite` | Annonce à la fin du message en cours | Confirmations, mises à jour non urgentes |
| `role="log"` | `polite` | Annonce les ajouts | Chat, logs, listes en croissance |
| `role="progressbar"` | — | Valeur mise à jour programmatiquement | Téléchargements, progression |
| `aria-live="off"` | Pas d'annonce | Masquer aux lecteurs d'écran | Régions mises à jour silencieusement |

```typescript
// Hook pour les annonces de live region
function useLiveRegion() {
  const statusRef = useRef<HTMLDivElement>(null);
  const alertRef = useRef<HTMLDivElement>(null);

  function annoncer(message: string, type: 'polite' | 'assertive' = 'polite') {
    const ref = type === 'polite' ? statusRef : alertRef;
    if (!ref.current) return;

    // Reset pour forcer la ré-annonce du même message
    ref.current.textContent = '';
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        if (ref.current) ref.current.textContent = message;
      });
    });
  }

  const LiveRegions = () => (
    <>
      <div
        ref={statusRef}
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      />
      <div
        ref={alertRef}
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
        className="sr-only"
      />
    </>
  );

  return { annoncer, LiveRegions };
}

// Usage
function Formulaire() {
  const { annoncer, LiveRegions } = useLiveRegion();

  async function handleSubmit() {
    try {
      await api.sauvegarder(données);
      annoncer('Modifications enregistrées avec succès', 'polite');
    } catch (err) {
      annoncer('Erreur lors de la sauvegarde. Réessayez.', 'assertive');
    }
  }

  return (
    <>
      <LiveRegions />
      {/* Formulaire... */}
    </>
  );
}
```

---

## Tree View (Arborescence)

### Structure et interactions

**Interactions clavier** :
- `Flèche droite` : développe le nœud fermé ; si développé, déplace sur le premier enfant
- `Flèche gauche` : réduit le nœud ouvert ; si réduit, remonte au parent
- `Flèche bas/haut` : navigue entre nœuds visibles (sans ouvrir/fermer)
- `Enter` / `Space` : sélectionne ou active le nœud
- `Home` / `End` : premier/dernier nœud visible

```typescript
function TreeView({ nœuds }: { nœuds: TreeNode[] }) {
  const [développés, setDéveloppés] = useState<Set<string>>(new Set());
  const [sélectionné, setSélectionné] = useState<string | null>(null);

  function basculerNœud(id: string) {
    setDéveloppés(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  return (
    <ul role="tree" aria-label="Structure de fichiers">
      {nœuds.map(nœud => (
        <TreeItem
          key={nœud.id}
          nœud={nœud}
          niveau={1}
          développés={développés}
          sélectionné={sélectionné}
          onBasculer={basculerNœud}
          onSélectionner={setSélectionné}
        />
      ))}
    </ul>
  );
}

function TreeItem({ nœud, niveau, développés, sélectionné, onBasculer, onSélectionner }: TreeItemProps) {
  const aDesEnfants = nœud.enfants && nœud.enfants.length > 0;
  const estDéveloppé = développés.has(nœud.id);
  const estSélectionné = sélectionné === nœud.id;

  return (
    <li
      role="treeitem"
      aria-level={niveau}
      aria-expanded={aDesEnfants ? estDéveloppé : undefined}
      aria-selected={estSélectionné}
      tabIndex={estSélectionné ? 0 : -1}
      onClick={() => {
        if (aDesEnfants) onBasculer(nœud.id);
        onSélectionner(nœud.id);
      }}
    >
      <span aria-hidden="true">
        {aDesEnfants ? (estDéveloppé ? '▼' : '▶') : '  '}
      </span>
      {nœud.label}

      {aDesEnfants && estDéveloppé && (
        <ul role="group">
          {nœud.enfants!.map(enfant => (
            <TreeItem
              key={enfant.id}
              nœud={enfant}
              niveau={niveau + 1}
              développés={développés}
              sélectionné={sélectionné}
              onBasculer={onBasculer}
              onSélectionner={onSélectionner}
            />
          ))}
        </ul>
      )}
    </li>
  );
}
```

---

## Data Table (Tableau de Données)

### Tableaux simples vs complexes

```html
<!-- ✅ Tableau simple — scope suffit -->
<table>
  <caption>Résultats des ventes par région — T1 2024</caption>
  <thead>
    <tr>
      <th scope="col">Région</th>
      <th scope="col">CA (k€)</th>
      <th scope="col">Variation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Île-de-France</th>
      <td>1 245</td>
      <td>+12%</td>
    </tr>
    <tr>
      <th scope="row">PACA</th>
      <td>876</td>
      <td>+8%</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Total</th>
      <td>4 521</td>
      <td>+10%</td>
    </tr>
  </tfoot>
</table>

<!-- ✅ Tableau complexe — headers + id pour les cellules ambiguës -->
<table>
  <caption>Disponibilité des équipes par projet et par semaine</caption>
  <thead>
    <tr>
      <td></td>
      <th id="eq-dev" scope="col">Équipe Dev</th>
      <th id="eq-design" scope="col">Équipe Design</th>
    </tr>
    <tr>
      <td></td>
      <th id="s1-dev" headers="eq-dev" scope="col">Sem 1</th>
      <th id="s2-dev" headers="eq-dev" scope="col">Sem 2</th>
      <th id="s1-design" headers="eq-design" scope="col">Sem 1</th>
      <th id="s2-design" headers="eq-design" scope="col">Sem 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="projet-a" scope="row">Projet A</th>
      <td headers="projet-a s1-dev eq-dev">80%</td>
      <td headers="projet-a s2-dev eq-dev">60%</td>
      <td headers="projet-a s1-design eq-design">40%</td>
      <td headers="projet-a s2-design eq-design">80%</td>
    </tr>
  </tbody>
</table>
```

---

## Progress / Loading States

```typescript
// ✅ Barre de progression déterminée
function ProgressBar({ valeur, max = 100, label }: ProgressProps) {
  const pourcentage = Math.round((valeur / max) * 100);
  return (
    <div>
      <div
        role="progressbar"
        aria-valuenow={valeur}
        aria-valuemin={0}
        aria-valuemax={max}
        aria-label={label}
        aria-valuetext={`${pourcentage}% complété`}
        style={{ width: `${pourcentage}%` }}
      />
      <span aria-hidden="true">{pourcentage}%</span>
    </div>
  );
}

// ✅ Spinner de chargement indéterminé
function Spinner({ message = 'Chargement en cours' }: { message?: string }) {
  return (
    <div aria-live="polite" aria-busy="true">
      <div
        role="progressbar"
        aria-label={message}
        aria-valuetext={message}
      >
        {/* Animation CSS */}
      </div>
      <span className="sr-only">{message}</span>
    </div>
  );
}

// ✅ Annonce de fin de chargement
function ContenuChargé({ données, estEnChargement }: Props) {
  return (
    <div
      aria-live="polite"
      aria-busy={estEnChargement}
    >
      {estEnChargement
        ? <Spinner message="Chargement des données..." />
        : <TableauDonnées données={données} />
      }
    </div>
  );
}
```
