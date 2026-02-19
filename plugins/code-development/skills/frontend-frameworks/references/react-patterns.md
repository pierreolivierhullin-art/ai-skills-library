# React — Patterns Avancés et Architecture

## Overview

Ce document de référence couvre les patterns avancés de React appliqués à des architectures de production. Il traite la composition profonde de composants, la gestion d'état complexe avec `useReducer`, l'optimisation des re-renders, les portails, Suspense et Error Boundaries. Ces patterns ne sont pas des règles rigides — ce sont des outils à mobiliser quand la complexité les justifie.

---

## Compound Components — Composition Avancée

Le pattern Compound Component permet de créer des composants qui partagent un état implicite via Context, exposant une API déclarative et flexible à leurs consommateurs.

### Implémentation avec Context et displayName

```typescript
// components/Select/Select.tsx
import { createContext, useContext, useState, useId, ReactNode } from 'react';

interface SelectContextValue {
  value: string | null;
  onChange: (val: string) => void;
  isOpen: boolean;
  setOpen: (open: boolean) => void;
  labelId: string;
}

const SelectContext = createContext<SelectContextValue | null>(null);

function useSelectContext(componentName: string) {
  const ctx = useContext(SelectContext);
  if (!ctx) {
    throw new Error(`${componentName} doit être utilisé à l'intérieur de <Select />`);
  }
  return ctx;
}

// Root component
function Select({
  children,
  value,
  onChange,
  defaultValue = null,
}: {
  children: ReactNode;
  value?: string | null;
  onChange?: (val: string) => void;
  defaultValue?: string | null;
}) {
  const labelId = useId();
  const [internalValue, setInternalValue] = useState<string | null>(defaultValue);
  const [isOpen, setOpen] = useState(false);

  // Supporte mode contrôlé et non contrôlé
  const resolvedValue = value !== undefined ? value : internalValue;
  const handleChange = (val: string) => {
    if (onChange) onChange(val);
    else setInternalValue(val);
    setOpen(false);
  };

  return (
    <SelectContext.Provider value={{ value: resolvedValue, onChange: handleChange, isOpen, setOpen, labelId }}>
      <div role="combobox" aria-expanded={isOpen} aria-labelledby={labelId}>
        {children}
      </div>
    </SelectContext.Provider>
  );
}

// Sous-composants
function SelectTrigger({ children }: { children: ReactNode }) {
  const { isOpen, setOpen, labelId } = useSelectContext('Select.Trigger');
  return (
    <button id={labelId} onClick={() => setOpen(!isOpen)} aria-haspopup="listbox">
      {children}
    </button>
  );
}

function SelectList({ children }: { children: ReactNode }) {
  const { isOpen } = useSelectContext('Select.List');
  if (!isOpen) return null;
  return <ul role="listbox">{children}</ul>;
}

function SelectOption({ value, children }: { value: string; children: ReactNode }) {
  const ctx = useSelectContext('Select.Option');
  const isSelected = ctx.value === value;
  return (
    <li
      role="option"
      aria-selected={isSelected}
      onClick={() => ctx.onChange(value)}
      style={{ fontWeight: isSelected ? 'bold' : 'normal' }}
    >
      {children}
    </li>
  );
}

// Attacher les sous-composants et exposer les displayNames
Select.Trigger = SelectTrigger;
Select.List = SelectList;
Select.Option = SelectOption;

SelectTrigger.displayName = 'Select.Trigger';
SelectList.displayName = 'Select.List';
SelectOption.displayName = 'Select.Option';

// Usage — API déclarative, état partagé implicitement
function ExemplePays() {
  const [pays, setPays] = useState('fr');
  return (
    <Select value={pays} onChange={setPays}>
      <Select.Trigger>Choisir un pays</Select.Trigger>
      <Select.List>
        <Select.Option value="fr">France</Select.Option>
        <Select.Option value="de">Allemagne</Select.Option>
        <Select.Option value="es">Espagne</Select.Option>
      </Select.List>
    </Select>
  );
}
```

### Quand utiliser le Compound Component

- L'API du composant est utilisée dans de nombreux endroits avec des variantes de layout différentes.
- Les sous-composants ont besoin d'accéder à un état partagé sans que le parent de l'utilisateur ait à le gérer.
- Les composants de librairie d'interface (Tabs, Accordion, Dialog, Dropdown, Combobox) bénéficient quasi-systématiquement de ce pattern.

---

## Render Props vs Children as Function vs Hooks

Ces trois patterns résolvent le même problème — partager de la logique avec un état — mais avec des trade-offs différents.

```typescript
// ❌ Render Props (2017-2019) — verbose, nesting profond possible
function MouseTracker({ render }: { render: (pos: { x: number; y: number }) => ReactNode }) {
  const [pos, setPos] = useState({ x: 0, y: 0 });
  return <div onMouseMove={e => setPos({ x: e.clientX, y: e.clientY })}>{render(pos)}</div>;
}
// Usage : <MouseTracker render={({ x, y }) => <p>{x}, {y}</p>} />

// ❌ Children as Function (variante du render prop) — même problèmes
function MouseTracker({ children }: { children: (pos: { x: number; y: number }) => ReactNode }) {
  const [pos, setPos] = useState({ x: 0, y: 0 });
  return <div onMouseMove={e => setPos({ x: e.clientX, y: e.clientY })}>{children(pos)}</div>;
}

// ✅ Custom Hook — composable, flat, TypeScript-friendly
function useMousePosition() {
  const [pos, setPos] = useState({ x: 0, y: 0 });
  useEffect(() => {
    const handler = (e: MouseEvent) => setPos({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handler);
    return () => window.removeEventListener('mousemove', handler);
  }, []);
  return pos;
}
// Usage : const { x, y } = useMousePosition(); // Propre, composable
```

Les render props restent utiles quand la logique est indissociable du rendu (bibliothèques comme `react-table` v7, `downshift`) ou quand la logique doit contrôler le rendu de l'hôte (patterns d'injection de ref). Dans tout autre cas, préférer les hooks.

---

## Higher-Order Components — Cas d'Usage Résiduels

Les HOC ont été largement remplacés par les hooks, mais restent pertinents dans certains contextes.

```typescript
// HOC withAuth — encore utile pour des class components legacy ou des libs tierces
function withAuth<P extends object>(Component: React.ComponentType<P>) {
  function AuthenticatedComponent(props: P) {
    const { user, isLoading } = useAuth();
    if (isLoading) return <Spinner />;
    if (!user) return <Redirect to="/login" />;
    return <Component {...props} />;
  }
  AuthenticatedComponent.displayName = `withAuth(${Component.displayName ?? Component.name})`;
  return AuthenticatedComponent;
}

// HOC withLogging — instrumenter des composants tiers sans les modifier
function withLogging<P extends object>(Component: React.ComponentType<P>, label: string) {
  function LoggedComponent(props: P) {
    useEffect(() => {
      console.log(`[${label}] monté`, props);
      return () => console.log(`[${label}] démonté`);
    }, []);
    return <Component {...props} />;
  }
  LoggedComponent.displayName = `withLogging(${label})`;
  return LoggedComponent;
}

// Quand les HOC sont encore pertinents en 2025 :
// 1. Intégration avec des libs tierces qui attendent des class components
// 2. Composition d'ordre supérieur déclarative (compose(withAuth, withLogging, withTheme)(Component))
// 3. Wrapping de composants dont le code source ne peut pas être modifié
// Dans tous les autres cas, convertir la logique en custom hook.
```

---

## Context API — Bonnes Pratiques

### Découpage des Contexts pour éviter les re-renders

```typescript
// ❌ Un seul gros context — tout re-render si n'importe quelle valeur change
const AppContext = createContext<{ user: User; theme: Theme; panier: Panier }>(...);

// ✅ Contexts séparés par domaine de changement
const UserContext = createContext<User | null>(null);
const ThemeContext = createContext<Theme>('light');
const PanierContext = createContext<PanierState>(initialPanier);

// Provider avec lazy initialization et mémoïsation
function PanierProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<ItemPanier[]>(() => {
    // Lazy initialization — exécuté une seule fois au montage
    try {
      const stored = localStorage.getItem('panier');
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });

  // useMemo : la référence de l'objet ne change que si items change
  const value = useMemo(
    () => ({
      items,
      total: items.reduce((sum, i) => sum + i.prix * i.quantité, 0),
      ajouter: (item: ItemPanier) => setItems(prev => [...prev, item]),
      retirer: (id: string) => setItems(prev => prev.filter(i => i.id !== id)),
    }),
    [items]
  );

  return <PanierContext.Provider value={value}>{children}</PanierContext.Provider>;
}

// Hook d'accès typé avec guard
export function usePanier() {
  const ctx = useContext(PanierContext);
  if (!ctx) throw new Error('usePanier doit être utilisé dans PanierProvider');
  return ctx;
}
```

### Context avec useReducer — Pattern Redux-like léger

```typescript
// Quand useState devient insuffisant mais Redux serait surdimensionné

type ActionPanier =
  | { type: 'AJOUTER'; payload: ItemPanier }
  | { type: 'RETIRER'; payload: { id: string } }
  | { type: 'MODIFIER_QUANTITE'; payload: { id: string; quantité: number } }
  | { type: 'VIDER' };

function réducteurPanier(state: ItemPanier[], action: ActionPanier): ItemPanier[] {
  switch (action.type) {
    case 'AJOUTER': {
      const existant = state.find(i => i.id === action.payload.id);
      if (existant) {
        return state.map(i =>
          i.id === action.payload.id ? { ...i, quantité: i.quantité + 1 } : i
        );
      }
      return [...state, { ...action.payload, quantité: 1 }];
    }
    case 'RETIRER':
      return state.filter(i => i.id !== action.payload.id);
    case 'MODIFIER_QUANTITE':
      return state.map(i =>
        i.id === action.payload.id ? { ...i, quantité: action.payload.quantité } : i
      );
    case 'VIDER':
      return [];
    default:
      return state; // TypeScript garantit l'exhaustivité avec never
  }
}
```

---

## useReducer pour l'État Complexe

### Discriminated Unions TypeScript — Sécurité Totale

```typescript
// État d'une requête asynchrone — discriminated union
type EtatRequete<T> =
  | { statut: 'idle' }
  | { statut: 'chargement' }
  | { statut: 'succès'; données: T }
  | { statut: 'erreur'; erreur: Error };

type ActionRequete<T> =
  | { type: 'LANCER' }
  | { type: 'SUCCÈS'; données: T }
  | { type: 'ERREUR'; erreur: Error }
  | { type: 'RÉINITIALISER' };

function réducteurRequete<T>(
  state: EtatRequete<T>,
  action: ActionRequete<T>
): EtatRequete<T> {
  switch (action.type) {
    case 'LANCER': return { statut: 'chargement' };
    case 'SUCCÈS': return { statut: 'succès', données: action.données };
    case 'ERREUR': return { statut: 'erreur', erreur: action.erreur };
    case 'RÉINITIALISER': return { statut: 'idle' };
  }
}

// Custom hook générique — réutilisable pour n'importe quelle requête
function useRequêteAsync<T>(fn: () => Promise<T>) {
  const [état, dispatch] = useReducer(réducteurRequete<T>, { statut: 'idle' });

  const exécuter = useCallback(async () => {
    dispatch({ type: 'LANCER' });
    try {
      const données = await fn();
      dispatch({ type: 'SUCCÈS', données });
    } catch (e) {
      dispatch({ type: 'ERREUR', erreur: e as Error });
    }
  }, [fn]);

  return { état, exécuter };
}

// Narrowing TypeScript dans le composant — zéro unsafe cast
function AffichageRequête<T>({ état }: { état: EtatRequete<T>; renderSuccès: (d: T) => ReactNode }) {
  if (état.statut === 'idle') return <p>En attente...</p>;
  if (état.statut === 'chargement') return <Skeleton />;
  if (état.statut === 'erreur') return <Alerte message={état.erreur.message} />;
  // TypeScript sait ici que état.statut === 'succès' et que données est de type T
  return <>{renderSuccès(état.données)}</>;
}
```

### Quand choisir useReducer vs useState

| Critère | useState | useReducer |
|---|---|---|
| Nombre de variables d'état | 1-3 indépendantes | 4+ liées entre elles |
| Transitions d'état | Simples, directes | Dépendent de l'état précédent |
| Logique de mise à jour | Triviale | Complexe, conditionnelle |
| Testabilité | Composant à tester | Réducteur pur, testable isolément |
| Debug | Limité | Chaque action est traçable |

---

## Portails — Rendu Hors de la Hiérarchie DOM

Les portails permettent de rendre des enfants dans un nœud DOM qui existe en dehors de la hiérarchie DOM du composant parent, tout en maintenant la hiérarchie React (bubbling d'événements, contexte).

```typescript
import { createPortal } from 'react-dom';
import { useEffect, useRef } from 'react';

// Portail vers un nœud DOM existant
function Modal({ isOpen, onClose, children }: ModalProps) {
  const portalRoot = document.getElementById('modal-root')!;

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      return () => { document.body.style.overflow = ''; };
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return createPortal(
    <div role="dialog" aria-modal="true">
      <div className="overlay" onClick={onClose} />
      <div className="modal-content">{children}</div>
    </div>,
    portalRoot
  );
}

// Tooltip avec portail — évite les problèmes de overflow:hidden parent
function Tooltip({ children, contenu }: { children: ReactNode; contenu: string }) {
  const [visible, setVisible] = useState(false);
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const refAncre = useRef<HTMLSpanElement>(null);

  const afficher = () => {
    if (refAncre.current) {
      const rect = refAncre.current.getBoundingClientRect();
      setPosition({ top: rect.bottom + window.scrollY + 8, left: rect.left + window.scrollX });
      setVisible(true);
    }
  };

  return (
    <>
      <span ref={refAncre} onMouseEnter={afficher} onMouseLeave={() => setVisible(false)}>
        {children}
      </span>
      {visible && createPortal(
        <div role="tooltip" style={{ position: 'absolute', top: position.top, left: position.left }}>
          {contenu}
        </div>,
        document.body
      )}
    </>
  );
}
```

---

## Suspense et lazy — Code Splitting et Data Fetching

### Code Splitting avec lazy

```typescript
import { lazy, Suspense } from 'react';

// lazy : charge le composant seulement quand il est nécessaire
const EditeurMarkdown = lazy(() => import('./EditeurMarkdown'));
const TableauDeBord = lazy(() => import('./TableauDeBord'));
const RapportAnalytique = lazy(() => import('./RapportAnalytique'));

// Boundaries Suspense à des niveaux stratégiques
function App() {
  return (
    <Router>
      <Suspense fallback={<SqueletteNavigation />}>
        <Navigation />
      </Suspense>
      <Suspense fallback={<SqueletteContenu />}>
        <Routes>
          <Route path="/dashboard" element={<TableauDeBord />} />
          <Route path="/rapports/:id" element={<RapportAnalytique />} />
          <Route path="/edition" element={<EditeurMarkdown />} />
        </Routes>
      </Suspense>
    </Router>
  );
}
```

### Data Fetching avec use() — React 19

```typescript
// React 19 : use() peut suspendre sur une Promise
import { use, Suspense } from 'react';

// Server Component ou client avec cache
async function fetchUtilisateur(id: string): Promise<Utilisateur> {
  const res = await fetch(`/api/utilisateurs/${id}`);
  if (!res.ok) throw new Error('Utilisateur introuvable');
  return res.json();
}

// Client Component utilisant use()
function ProfilUtilisateur({ promesse }: { promesse: Promise<Utilisateur> }) {
  // use() suspend le composant jusqu'à la résolution de la promesse
  const utilisateur = use(promesse);
  return (
    <div>
      <h1>{utilisateur.nom}</h1>
      <p>{utilisateur.email}</p>
    </div>
  );
}

// Composition avec Suspense + Error Boundary
function PageProfil({ userId }: { userId: string }) {
  const promesse = fetchUtilisateur(userId); // Ne pas await — passer la promesse

  return (
    <ErrorBoundary fallback={<ErreurProfil />}>
      <Suspense fallback={<SqueletteProfil />}>
        <ProfilUtilisateur promesse={promesse} />
      </Suspense>
    </ErrorBoundary>
  );
}
```

---

## Error Boundaries

```typescript
'use client'; // En Next.js App Router

import { Component, ErrorInfo, ReactNode } from 'react';
import { ErrorBoundary as ReactErrorBoundary, FallbackProps } from 'react-error-boundary';

// ❌ Class component — syntaxe verbieuse, mais encore nécessaire pour certains cas
class ErrorBoundaryManuelle extends Component<
  { children: ReactNode; fallback: ReactNode },
  { hasError: boolean; error: Error | null }
> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    // Reporter à Sentry, Datadog, etc.
    logError(error, info.componentStack);
  }

  render() {
    if (this.state.hasError) return this.props.fallback;
    return this.props.children;
  }
}

// ✅ react-error-boundary — API fonctionnelle, reset, onError
function FallbackErreur({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <div role="alert" className="erreur-container">
      <h2>Une erreur est survenue</h2>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Réessayer</button>
    </div>
  );
}

// Utilisation avec resetKeys — réinitialise automatiquement si la clé change
function SectionDonnées({ userId }: { userId: string }) {
  return (
    <ReactErrorBoundary
      FallbackComponent={FallbackErreur}
      onError={(error, info) => logError(error, info.componentStack)}
      resetKeys={[userId]} // Réinitialise si userId change
    >
      <DonnéesUtilisateur userId={userId} />
    </ReactErrorBoundary>
  );
}
```

---

## React DevTools Profiler — Workflow d'Optimisation

### Lecture du Flame Graph

Le Profiler enregistre les rendus sur une période et affiche un flamegraph où chaque barre représente un composant.

```
Flame Graph — Lecture
─────────────────────────────────────────────────────
App (2.1ms)
├── Navigation (0.1ms) — gris : n'a pas re-rendu
├── ListeProduits (1.8ms) — jaune/rouge : a re-rendu
│   ├── Filtres (0.2ms)
│   ├── CarteProduit × 24 (1.4ms total) ← PROBLÈME
│   └── Pagination (0.2ms)
└── Pied de page (0.1ms) — gris

Clé de lecture :
- Gris   : composant non re-rendu (mémoïsé ou non affecté)
- Jaune  : re-rendu court (< 1ms) — probablement OK
- Orange : re-rendu moyen (1-10ms) — à surveiller
- Rouge  : re-rendu long (> 10ms) — à optimiser
```

### Intégration why-did-you-render

```typescript
// src/wdyr.ts — importer en premier dans index.tsx
import React from 'react';

if (process.env.NODE_ENV === 'development') {
  const { default: whyDidYouRender } = await import('@welldone-software/why-did-you-render');
  whyDidYouRender(React, {
    trackAllPureComponents: true, // Tracker tous les React.memo
    logOnDifferentValues: true,
    titleColor: '#e91e63',
    diffNameColor: '#9c27b0',
  });
}

// Sur un composant spécifique
const CarteProduit = memo(function CarteProduit({ produit }: Props) {
  return <div>{produit.nom}</div>;
});
(CarteProduit as any).whyDidYouRender = true;
// La console affichera quelles props ont changé et pourquoi le re-render a eu lieu
```

---

## Strict Mode — Implications

```typescript
// main.tsx
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

En mode développement, `StrictMode` :
- Double-exécute les effets (`useEffect`) pour détecter les effets de bord non nettoyés : monter → démonter → remonter.
- Double-appelle les corps de fonctions composants et les réducteurs pour détecter les mutations d'état.
- Avertit sur les méthodes de cycle de vie dépréciées.

Impact pratique : si un `useEffect` produit des effets de bord visibles deux fois (requêtes dupliquées, timers multiples), le cleanup est manquant ou insuffisant.

```typescript
// ✅ Cleanup correct — résiste au double-mount de StrictMode
useEffect(() => {
  const controller = new AbortController();
  fetch('/api/données', { signal: controller.signal })
    .then(r => r.json())
    .then(setDonnées)
    .catch(e => { if (e.name !== 'AbortError') setErreur(e); });
  return () => controller.abort(); // Cleanup — annule la requête au démontage
}, []);
```

---

## Récapitulatif — Arbre de Décision des Patterns

```
Besoin de partager de la logique entre composants ?
│
├── Logique pure sans état → Custom hook
├── Logique avec état partagé entre quelques composants proches → Lifting state up
├── Logique avec état partagé largement → Context + useReducer (ou Zustand)
└── Logique de rendu flexible (UI configurable) → Compound Component

Besoin d'optimiser les re-renders ?
│
├── Composant enfant re-render trop souvent → React.memo + useCallback sur les handlers
├── Calcul coûteux à chaque render → useMemo
├── Nombreuses variables d'état liées → useReducer avec discriminated union
└── État indépendant du cycle de vie React → useRef

Rendu hors de la hiérarchie DOM (modals, tooltips) → Portails

Chargement conditionnel de code → React.lazy + Suspense

Gestion des erreurs de rendu → Error Boundary (react-error-boundary)
```
