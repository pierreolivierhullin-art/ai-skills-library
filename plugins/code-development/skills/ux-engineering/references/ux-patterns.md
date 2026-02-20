# UX Patterns — Empty States, Error States, Loading States & Micro-interactions

## Overview

Ce document couvre les patterns UX fondamentaux qu'un ingénieur frontend doit maîtriser : états vides, chargement, erreur, succès, micro-interactions, toasts, modales et animations. Ces patterns sont le premier point de contact entre l'utilisateur et la qualité perçue de ton produit.

---

## 1. Empty States — Les Quatre Variantes

Il existe quatre types distincts, chacun avec un message et une action optimale.

| Variante | Déclencheur | Action prioritaire |
|---|---|---|
| **First-use** | Aucune donnée créée | CTA primaire pour créer |
| **User-cleared** | Utilisateur a tout supprimé | CTA doux + option d'annulation |
| **No-results** | Recherche/filtre sans résultat | Réinitialiser les filtres |
| **Error** | Échec de chargement | Bouton "Réessayer" |

```typescript
// components/EmptyState/EmptyState.tsx
type EmptyStateVariant = 'first-use' | 'cleared' | 'no-results' | 'error';

interface EmptyStateProps {
  variant: EmptyStateVariant;
  title?: string;
  description?: string;
  action?: { label: string; onClick: () => void };
  icon?: React.ReactNode;
}

const defaults: Record<EmptyStateVariant, { title: string; description: string }> = {
  'first-use':  { title: 'Commence par créer ton premier élément',
                  description: 'Crée ton premier projet pour voir apparaître tes données.' },
  'cleared':    { title: 'Tu as tout supprimé',
                  description: "Ajoute de nouveaux éléments quand tu es prêt." },
  'no-results': { title: 'Aucun résultat trouvé',
                  description: 'Essaie de modifier tes critères ou de réinitialiser les filtres.' },
  'error':      { title: 'Impossible de charger le contenu',
                  description: 'Une erreur est survenue. Réessaie dans quelques instants.' },
};

export function EmptyState({ variant, title, description, action, icon }: EmptyStateProps) {
  const d = defaults[variant];
  return (
    <div className="flex flex-col items-center justify-center py-16 px-8 text-center" role="status">
      {icon && <div className="mb-6 text-gray-300" aria-hidden="true">{icon}</div>}
      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
        {title ?? d.title}
      </h3>
      <p className="text-sm text-gray-500 max-w-sm mb-8">{description ?? d.description}</p>
      {action && (
        <button onClick={action.onClick}
          className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
          {action.label}
        </button>
      )}
    </div>
  );
}
```

**Règles clés :** Ne jamais afficher juste "Aucun résultat" — reprends le terme recherché dans le message. Pour les first-use states, utilise un ton encourageant, jamais une excuse.

---

## 2. Loading States — Skeleton vs Spinner

**Matrice de décision :**
- Durée < 300ms → rien (un flash est pire que l'absence de loader)
- Durée 300ms–2s + structure connue → **skeleton screen**
- Durée 300ms–2s + structure inconnue → **spinner**
- Action ponctuelle (save, delete) → **spinner inline dans le bouton**
- Premier chargement de page → **skeleton** systématiquement

```typescript
// components/Skeleton/Skeleton.tsx
interface SkeletonProps {
  className?: string;
  variant?: 'text' | 'rectangular' | 'circular' | 'rounded';
  width?: string | number;
  height?: string | number;
  lines?: number;
}

export function Skeleton({ className = '', variant = 'rectangular', width, height, lines = 1 }: SkeletonProps) {
  const variantClass = {
    text: 'rounded h-4', rectangular: '', circular: 'rounded-full', rounded: 'rounded-lg',
  }[variant];

  if (variant === 'text' && lines > 1) {
    return (
      <div className={`space-y-2 ${className}`} aria-hidden="true">
        {Array.from({ length: lines }).map((_, i) => (
          <div key={i} className={`skeleton-shimmer bg-gray-200 dark:bg-gray-700 rounded h-4`}
            style={{ width: i === lines - 1 ? '75%' : '100%' }} />
        ))}
      </div>
    );
  }
  return (
    <div className={`skeleton-shimmer bg-gray-200 dark:bg-gray-700 ${variantClass} ${className}`}
      style={{ width, height }} aria-hidden="true" />
  );
}

// Skeleton composite représentant un card
export function CardSkeleton() {
  return (
    <div className="p-4 border border-gray-200 rounded-xl space-y-3" aria-hidden="true">
      <div className="flex items-center gap-3">
        <Skeleton variant="circular" width={40} height={40} />
        <div className="flex-1 space-y-2">
          <Skeleton variant="text" width="60%" height={14} />
          <Skeleton variant="text" width="40%" height={12} />
        </div>
      </div>
      <Skeleton variant="rounded" height={160} className="w-full" />
      <Skeleton variant="text" lines={3} />
    </div>
  );
}
```

```css
/* styles/skeleton.css */
@keyframes skeleton-shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
.skeleton-shimmer {
  background: linear-gradient(
    90deg,
    rgb(var(--skeleton-base)/1) 25%,
    rgb(var(--skeleton-hi)/1) 50%,
    rgb(var(--skeleton-base)/1) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
}
:root     { --skeleton-base: 229 231 235; --skeleton-hi: 243 244 246; }
.dark     { --skeleton-base: 55 65 81;    --skeleton-hi: 75 85 99;    }

@media (prefers-reduced-motion: reduce) {
  .skeleton-shimmer { animation: none; background: rgb(var(--skeleton-base)/1); }
}
```

---

## 3. Error States — Boundaries, Inline & Pages

### Error Boundary avec fallback utilisateur

```typescript
// components/ErrorBoundary/ErrorBoundary.tsx
import { Component, ReactNode, ErrorInfo } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, reset: () => void) => ReactNode);
  onError?: (error: Error, info: ErrorInfo) => void;
}

export class ErrorBoundary extends Component<Props, { error: Error | null }> {
  state = { error: null };
  static getDerivedStateFromError(e: Error) { return { error: e }; }
  componentDidCatch(error: Error, info: ErrorInfo) { this.props.onError?.(error, info); }
  reset = () => this.setState({ error: null });

  render() {
    if (this.state.error) {
      return typeof this.props.fallback === 'function'
        ? this.props.fallback(this.state.error, this.reset)
        : this.props.fallback ?? <ErrorFallback onReset={this.reset} />;
    }
    return this.props.children;
  }
}

function ErrorFallback({ onReset }: { onReset: () => void }) {
  return (
    <div role="alert" className="flex flex-col items-center py-16 px-8 text-center">
      <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
        Quelque chose s'est mal passé
      </h2>
      <p className="text-sm text-gray-500 max-w-sm mb-6">
        Une erreur inattendue s'est produite. Nos équipes en ont été informées automatiquement.
      </p>
      <button onClick={onReset}
        className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg
          hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
        Réessayer
      </button>
    </div>
  );
}
```

### Inline vs Toast — Règle de décision

**Inline** : erreur liée à un champ précis, l'utilisateur doit agir sur cet élément, validation de formulaire.

**Toast** : erreur système/réseau, action terminée en arrière-plan, pas d'action immédiate requise.

Ne jamais utiliser les deux simultanément pour la même erreur.

### Page 404 (Next.js App Router)

```typescript
// app/not-found.tsx
import Link from 'next/link';
export default function NotFound() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
      <div className="text-center px-8 max-w-lg">
        <p className="text-8xl font-black text-gray-200 dark:text-gray-800 mb-4" aria-hidden="true">404</p>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Cette page n'existe pas</h1>
        <p className="text-gray-500 mb-8">La page a peut-être été déplacée. Vérifie l'URL ou retourne à l'accueil.</p>
        <div className="flex justify-center gap-3">
          <Link href="/"
            className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors">
            Retour à l'accueil
          </Link>
          <button onClick={() => history.back()}
            className="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors">
            Page précédente
          </button>
        </div>
      </div>
    </main>
  );
}
```

---

## 4. Toast Notifications — Système avec Zustand

```typescript
// lib/toast.ts
import { create } from 'zustand';
import { nanoid } from 'nanoid';

type ToastVariant = 'success' | 'error' | 'warning' | 'info';
interface Toast { id: string; variant: ToastVariant; title: string;
  description?: string; duration?: number; action?: { label: string; onClick: () => void } }

const useToastStore = create<{
  toasts: Toast[];
  add: (t: Omit<Toast, 'id'>) => string;
  remove: (id: string) => void;
}>((set) => ({
  toasts: [],
  add: (t) => { const id = nanoid(); set(s => ({ toasts: [...s.toasts, { ...t, id }] })); return id; },
  remove: (id) => set(s => ({ toasts: s.toasts.filter(t => t.id !== id) })),
}));

// API publique
export const toast = {
  success: (title: string, opts?: Partial<Omit<Toast, 'id'|'variant'|'title'>>) =>
    useToastStore.getState().add({ variant: 'success', title, duration: 4000, ...opts }),
  error: (title: string, opts?: Partial<Omit<Toast, 'id'|'variant'|'title'>>) =>
    useToastStore.getState().add({ variant: 'error', title, duration: 8000, ...opts }),
  warning: (title: string, opts?: Partial<Omit<Toast, 'id'|'variant'|'title'>>) =>
    useToastStore.getState().add({ variant: 'warning', title, duration: 6000, ...opts }),
};

export { useToastStore };
```

```typescript
// components/Toast/ToastContainer.tsx
import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useToastStore } from '@/lib/toast';

const styles = {
  success: 'bg-green-50 border-green-200 text-green-800 dark:bg-green-950 dark:border-green-800 dark:text-green-200',
  error:   'bg-red-50 border-red-200 text-red-800 dark:bg-red-950 dark:border-red-800 dark:text-red-200',
  warning: 'bg-amber-50 border-amber-200 text-amber-800 dark:bg-amber-950 dark:border-amber-800 dark:text-amber-200',
  info:    'bg-blue-50 border-blue-200 text-blue-800 dark:bg-blue-950 dark:border-blue-800 dark:text-blue-200',
};

function ToastItem({ toast }: { toast: ReturnType<typeof useToastStore>['toasts'][number] }) {
  const remove = useToastStore(s => s.remove);
  useEffect(() => {
    if (!toast.duration) return;
    const t = setTimeout(() => remove(toast.id), toast.duration);
    return () => clearTimeout(t);
  }, [toast.id, toast.duration, remove]);

  return (
    <motion.div layout role="alert" aria-live="assertive" aria-atomic="true"
      initial={{ opacity: 0, y: 16, scale: 0.95 }} animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, x: 48, scale: 0.95 }}
      transition={{ type: 'spring', stiffness: 300, damping: 25 }}
      className={`flex items-start gap-3 min-w-80 max-w-sm px-4 py-3 border rounded-xl shadow-lg ${styles[toast.variant]}`}>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-semibold">{toast.title}</p>
        {toast.description && <p className="text-xs opacity-80 mt-0.5">{toast.description}</p>}
        {toast.action && (
          <button onClick={() => { toast.action!.onClick(); remove(toast.id); }}
            className="mt-2 text-xs font-semibold underline underline-offset-2 hover:no-underline">
            {toast.action.label}
          </button>
        )}
      </div>
      <button onClick={() => remove(toast.id)} aria-label="Fermer" className="opacity-60 hover:opacity-100 transition-opacity">×</button>
    </motion.div>
  );
}

// Position : bas-droite desktop, bas-centré mobile. Max 3 toasts visibles.
export function ToastContainer() {
  const toasts = useToastStore(s => s.toasts);
  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 items-end" aria-label="Notifications">
      <AnimatePresence mode="sync">
        {toasts.slice(-3).map(t => <ToastItem key={t.id} toast={t} />)}
      </AnimatePresence>
    </div>
  );
}
```

**Durées par variante :** success 4s, info 5s, warning 6s, error 8s. Les erreurs durent plus longtemps car l'utilisateur doit lire et agir.

---

## 5. Confirmation Dialog

```typescript
// components/ConfirmDialog/ConfirmDialog.tsx
import { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { createPortal } from 'react-dom';

interface ConfirmDialogProps {
  isOpen: boolean; title: string; description: string;
  confirmLabel?: string; cancelLabel?: string;
  variant?: 'danger' | 'default';
  onConfirm: () => void; onCancel: () => void;
  isLoading?: boolean;
}

export function ConfirmDialog({
  isOpen, title, description,
  confirmLabel = 'Confirmer', cancelLabel = 'Annuler',
  variant = 'default', onConfirm, onCancel, isLoading = false,
}: ConfirmDialogProps) {
  const cancelRef = useRef<HTMLButtonElement>(null);

  // Focus sur "Annuler" par défaut — plus sûr pour les actions destructrices
  useEffect(() => { if (isOpen) setTimeout(() => cancelRef.current?.focus(), 50); }, [isOpen]);
  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === 'Escape' && isOpen) onCancel(); };
    document.addEventListener('keydown', fn);
    return () => document.removeEventListener('keydown', fn);
  }, [isOpen, onCancel]);
  useEffect(() => {
    document.body.style.overflow = isOpen ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [isOpen]);

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm" onClick={onCancel} aria-hidden="true" />
          <motion.div role="dialog" aria-modal="true"
            aria-labelledby="dlg-title" aria-describedby="dlg-desc"
            initial={{ opacity: 0, scale: 0.95, y: 8 }} animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 8 }}
            transition={{ type: 'spring', stiffness: 300, damping: 25 }}
            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50
              w-full max-w-md bg-white dark:bg-gray-900 rounded-2xl shadow-xl p-6">
            <h2 id="dlg-title" className="text-base font-semibold text-gray-900 dark:text-gray-100 mb-2">{title}</h2>
            <p id="dlg-desc" className="text-sm text-gray-500 dark:text-gray-400 mb-6">{description}</p>
            <div className="flex justify-end gap-3">
              <button ref={cancelRef} onClick={onCancel} disabled={isLoading}
                className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800
                  border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700
                  focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 transition-colors">
                {cancelLabel}
              </button>
              <button onClick={onConfirm} disabled={isLoading}
                className={`px-4 py-2 text-sm font-medium text-white rounded-lg
                  focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 transition-colors
                  ${variant === 'danger'
                    ? 'bg-red-600 hover:bg-red-700 focus:ring-red-500'
                    : 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500'}`}>
                {isLoading ? 'En cours…' : confirmLabel}
              </button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>,
    document.body
  );
}
```

**Quand ne pas utiliser une modale :** formulaire > 5 champs (→ page dédiée), contenu principalement consultatif (→ panneau latéral), sur mobile avec clavier virtuel.

---

## 6. Micro-interactions — Framer Motion

### Bouton avec feedback de pression

```typescript
// components/Button/AnimatedButton.tsx
import { motion, HTMLMotionProps } from 'framer-motion';

interface AnimatedButtonProps extends HTMLMotionProps<'button'> {
  variant?: 'primary' | 'secondary' | 'destructive';
  isLoading?: boolean;
}

export function AnimatedButton({ variant = 'primary', isLoading = false, children, disabled, ...props }: AnimatedButtonProps) {
  const isDisabled = disabled || isLoading;
  const variantClass = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50',
    destructive: 'bg-red-600 text-white hover:bg-red-700',
  }[variant];

  return (
    <motion.button
      className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors
        focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
        disabled:opacity-50 disabled:cursor-not-allowed ${variantClass}`}
      whileTap={{ scale: isDisabled ? 1 : 0.97 }}
      whileHover={{ scale: isDisabled ? 1 : 1.02 }}
      transition={{ type: 'spring', stiffness: 400, damping: 17 }}
      disabled={isDisabled}
      {...props}
    >
      {isLoading
        ? <span className="flex items-center gap-2">
            <motion.span className="inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full"
              animate={{ rotate: 360 }} transition={{ duration: 0.8, repeat: Infinity, ease: 'linear' }} aria-hidden="true" />
            Chargement…
          </span>
        : children}
    </motion.button>
  );
}
```

### Toggle switch animé

```typescript
// components/Toggle/Toggle.tsx
import { motion } from 'framer-motion';

export function Toggle({ checked, onChange, label, disabled = false }:
  { checked: boolean; onChange: (v: boolean) => void; label: string; disabled?: boolean }) {
  return (
    <label className={`flex items-center gap-3 cursor-pointer select-none ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}>
      <button role="switch" aria-checked={checked} aria-label={label} disabled={disabled}
        onClick={() => !disabled && onChange(!checked)}
        className={`relative w-11 h-6 rounded-full transition-colors duration-200
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
          ${checked ? 'bg-blue-600' : 'bg-gray-300 dark:bg-gray-600'}`}>
        <motion.span className="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow-md"
          animate={{ x: checked ? 20 : 0 }}
          transition={{ type: 'spring', stiffness: 500, damping: 30 }} aria-hidden="true" />
      </button>
      <span className="text-sm text-gray-700 dark:text-gray-300">{label}</span>
    </label>
  );
}
```

### Liste animée — ajout et suppression

```typescript
// AnimatePresence gère les entrées/sorties de la liste
import { motion, AnimatePresence } from 'framer-motion';

const item = {
  hidden: { opacity: 0, height: 0, y: -8 },
  visible: { opacity: 1, height: 'auto', y: 0,
    transition: { type: 'spring', stiffness: 300, damping: 25 } },
  exit: { opacity: 0, height: 0, x: -20, transition: { duration: 0.2 } },
};

export function AnimatedList({ items, onRemove }:
  { items: { id: string; label: string }[]; onRemove: (id: string) => void }) {
  return (
    <ul aria-live="polite" className="space-y-2">
      <AnimatePresence initial={false}>
        {items.map(it => (
          <motion.li key={it.id} variants={item} initial="hidden" animate="visible" exit="exit" layout
            className="flex items-center justify-between px-4 py-3 bg-white dark:bg-gray-800
              border border-gray-200 dark:border-gray-700 rounded-lg">
            <span className="text-sm">{it.label}</span>
            <button onClick={() => onRemove(it.id)} aria-label={`Supprimer ${it.label}`}
              className="text-gray-400 hover:text-red-500 transition-colors">×</button>
          </motion.li>
        ))}
      </AnimatePresence>
    </ul>
  );
}
```

---

## 7. Optimistic UI & Form Field avec Validation Inline

### UI Optimiste — hook de suppression avec rollback

```typescript
// hooks/useOptimisticDelete.ts
import { useState } from 'react';

export function useOptimisticDelete<T>({
  items, onDelete, getId,
}: { items: T[]; onDelete: (id: string) => Promise<void>; getId: (item: T) => string }) {
  const [optimisticItems, setItems] = useState(items);
  const [error, setError] = useState<string | null>(null);

  const handleDelete = async (id: string) => {
    const previous = optimisticItems;
    setItems(prev => prev.filter(item => getId(item) !== id)); // optimiste
    setError(null);
    try {
      await onDelete(id);
    } catch {
      setItems(previous); // rollback
      setError("La suppression a échoué. L'élément a été restauré.");
    }
  };

  return { optimisticItems, handleDelete, error };
}
```

**UI pessimiste** : obligatoire pour tout ce qui est financier, irréversible ou critique (paiement, suppression de compte). Ne jamais confirmer visuellement un paiement avant la réponse Stripe.

### Form Field avec animation d'erreur

```typescript
// components/FormField/FormField.tsx
import { forwardRef, InputHTMLAttributes } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface FormFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string; error?: string; hint?: string;
}

export const FormField = forwardRef<HTMLInputElement, FormFieldProps>(
  ({ label, error, hint, id, className = '', ...props }, ref) => {
    const fieldId = id ?? `field-${label.toLowerCase().replace(/\s+/g, '-')}`;
    return (
      <div className="space-y-1.5">
        <label htmlFor={fieldId} className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          {label}
          {props.required && <span className="ml-1 text-red-500" aria-hidden="true">*</span>}
        </label>
        <input ref={ref} id={fieldId}
          aria-describedby={error ? `${fieldId}-error` : hint ? `${fieldId}-hint` : undefined}
          aria-invalid={error ? 'true' : undefined}
          className={`block w-full px-3 py-2 text-sm border rounded-lg shadow-sm transition-all duration-150
            placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-0
            ${error
              ? 'border-red-400 focus:ring-red-400 bg-red-50/50 dark:bg-red-950/20'
              : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:border-gray-600 dark:bg-gray-800'
            } ${className}`}
          {...props} />
        {hint && !error && (
          <p id={`${fieldId}-hint`} className="text-xs text-gray-500">{hint}</p>
        )}
        <AnimatePresence mode="wait">
          {error && (
            <motion.p id={`${fieldId}-error`} role="alert"
              initial={{ opacity: 0, y: -4, height: 0 }} animate={{ opacity: 1, y: 0, height: 'auto' }}
              exit={{ opacity: 0, y: -4, height: 0 }} transition={{ duration: 0.15 }}
              className="text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <span aria-hidden="true">✕</span>{error}
            </motion.p>
          )}
        </AnimatePresence>
      </div>
    );
  }
);
FormField.displayName = 'FormField';
```

---

## 8. Animation & Motion — Règles Essentielles

### prefers-reduced-motion — Non-négociable

```typescript
// hooks/useReducedMotion.ts
import { useEffect, useState } from 'react';
export function useReducedMotion() {
  const [reduced, setReduced] = useState(
    () => typeof window !== 'undefined'
      && window.matchMedia('(prefers-reduced-motion: reduce)').matches
  );
  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const fn = (e: MediaQueryListEvent) => setReduced(e.matches);
    mq.addEventListener('change', fn);
    return () => mq.removeEventListener('change', fn);
  }, []);
  return reduced;
}
```

### Timing de référence

| Contexte | Durée | Easing |
|---|---|---|
| Micro-interactions (hover, tap) | 80–120ms | `ease-out` |
| Transitions d'état (open/close) | 150–200ms | `ease-in-out` |
| Apparition de contenu (fade, slide) | 200–300ms | `ease-out` |
| Animations d'onboarding | 300–500ms | spring `stiffness 200, damping 20` |
| Jamais au-delà de | 500ms | — |

### CSS transitions vs Framer Motion

**CSS** : hover, focus ring, color, transform simples → GPU natif, 0 JS.

```css
.button {
  transition: transform 80ms ease-out, background-color 150ms ease-in-out;
}
.button:hover  { transform: scale(1.02); }
.button:active { transform: scale(0.97); }
```

**Framer Motion** : `AnimatePresence` (entrées/sorties), `layout` animations, états React conditionnels, spring physics, drag & drop avec contraintes.

---

## Références

- Framer Motion documentation — https://www.framer.com/motion/
- Radix UI Primitives (modales accessibles) — https://www.radix-ui.com/primitives
- W3C ARIA Authoring Practices Guide — https://www.w3.org/WAI/ARIA/apg/
- MDN, `prefers-reduced-motion` — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Zustand documentation — https://zustand-demo.pmnd.rs/
- Luke Wroblewski, *Web Form Design* (Rosenfeld Media, 2008)
