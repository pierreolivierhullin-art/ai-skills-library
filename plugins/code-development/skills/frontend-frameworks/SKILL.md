---
name: frontend-frameworks
version: 1.0.0
description: >
  React patterns, Next.js App Router, SSR SSG ISR rendering strategies, state management
  Zustand Redux Toolkit, React Query TanStack Query, TypeScript React, component architecture,
  Vue Nuxt, frontend architecture best practices, hooks patterns, performance optimization React,
  server components, hydration, streaming
---

# Frontend Frameworks — React, Next.js et Patterns Modernes

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu construis une application React ou Next.js
- Tu dois choisir entre SSR, SSG, ISR, ou CSR
- L'architecture composants est à repenser (props drilling, state management)
- Tu intègres React Query / TanStack Query pour le data fetching
- Tu optimises les re-renders et les performances React
- Tu migres de Pages Router vers App Router (Next.js 13+)

---

## React — Patterns Fondamentaux

### Composition vs Héritage

```typescript
// ❌ Props drilling profond (anti-pattern)
function App() {
  const [user, setUser] = useState(null);
  return <Layout user={user} onLogout={() => setUser(null)} />;
}
function Layout({ user, onLogout }) {
  return <Header user={user} onLogout={onLogout} />;
}
function Header({ user, onLogout }) {
  return <Avatar user={user} onLogout={onLogout} />;
}

// ✅ Composition avec slot pattern
function Layout({ children, header }) {
  return (
    <div>
      <nav>{header}</nav>
      <main>{children}</main>
    </div>
  );
}

function App() {
  const [user, setUser] = useState(null);
  return (
    <Layout header={<Avatar user={user} onLogout={() => setUser(null)} />}>
      <Contenu />
    </Layout>
  );
}
```

### Custom Hooks — Séparation Logique/UI

```typescript
// Extraire la logique dans des hooks réutilisables

// hooks/useProduits.ts
export function useProduits(filtres: FiltresProduits) {
  return useQuery({
    queryKey: ['produits', filtres],
    queryFn: () => api.getProduits(filtres),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

// hooks/useLocalStorage.ts
export function useLocalStorage<T>(clé: string, défaut: T) {
  const [valeur, setValeur] = useState<T>(() => {
    try {
      const item = localStorage.getItem(clé);
      return item ? JSON.parse(item) : défaut;
    } catch { return défaut; }
  });

  const sauvegarder = useCallback((val: T | ((prev: T) => T)) => {
    setValeur(prev => {
      const nvlle = typeof val === 'function' ? (val as Function)(prev) : val;
      localStorage.setItem(clé, JSON.stringify(nvlle));
      return nvlle;
    });
  }, [clé]);

  return [valeur, sauvegarder] as const;
}

// Composant propre — zéro logique
function ListeProduits({ filtres }: { filtres: FiltresProduits }) {
  const { data, isLoading, error } = useProduits(filtres);

  if (isLoading) return <Skeleton />;
  if (error) return <MessageErreur />;
  return <>{data?.map(p => <CarteProduit key={p.id} produit={p} />)}</>;
}
```

### Optimisation des Re-renders

```typescript
import { memo, useMemo, useCallback } from 'react';

// memo : éviter les re-renders si les props n'ont pas changé
const CarteProduit = memo(function CarteProduit({ produit, onAjouterPanier }: Props) {
  return (
    <div>
      <h3>{produit.nom}</h3>
      <button onClick={() => onAjouterPanier(produit.id)}>Ajouter</button>
    </div>
  );
});

// useCallback : stabiliser les fonctions passées en props
function ListeProduits({ produits }: { produits: Produit[] }) {
  const { ajouterAuPanier } = usePanier();

  // Sans useCallback : nouvelle référence à chaque render → CarteProduit re-render
  // Avec useCallback : même référence si ajouterAuPanier ne change pas
  const handleAjouter = useCallback(
    (id: string) => ajouterAuPanier(id),
    [ajouterAuPanier]
  );

  return (
    <>
      {produits.map(p => (
        <CarteProduit key={p.id} produit={p} onAjouterPanier={handleAjouter} />
      ))}
    </>
  );
}

// useMemo : calculs coûteux
function Statistiques({ transactions }: { transactions: Transaction[] }) {
  const stats = useMemo(() => ({
    total: transactions.reduce((sum, t) => sum + t.montant, 0),
    moyenne: transactions.reduce((sum, t) => sum + t.montant, 0) / transactions.length,
    parCatégorie: Object.groupBy(transactions, t => t.catégorie),
  }), [transactions]); // Recalculé seulement si transactions change

  return <TableauStats stats={stats} />;
}
```

---

## State Management

### Zustand — Léger et Puissant

```typescript
// store/panier.store.ts
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface PanierState {
  items: ItemPanier[];
  total: number;
  // Actions
  ajouter: (produit: Produit) => void;
  retirer: (id: string) => void;
  vider: () => void;
}

export const usePanierStore = create<PanierState>()(
  devtools(
    persist(
      immer((set, get) => ({
        items: [],
        get total() {
          return get().items.reduce((sum, i) => sum + i.prix * i.quantité, 0);
        },

        ajouter: (produit) => set(state => {
          const existant = state.items.find(i => i.id === produit.id);
          if (existant) {
            existant.quantité += 1;
          } else {
            state.items.push({ ...produit, quantité: 1 });
          }
        }),

        retirer: (id) => set(state => {
          state.items = state.items.filter(i => i.id !== id);
        }),

        vider: () => set({ items: [] }),
      })),
      { name: 'panier' } // Persist dans localStorage
    )
  )
);

// Sélecteurs pour éviter les re-renders inutiles
const nombreItems = usePanierStore(state => state.items.length); // Re-render seulement si count change
const total = usePanierStore(state => state.total);
```

### TanStack Query — Server State

```typescript
// queries/produits.queries.ts
import { queryOptions, useMutation, useQueryClient } from '@tanstack/react-query';

// Factory de query options (typé, réutilisable)
export const produitQueries = {
  all: () => queryOptions({
    queryKey: ['produits'],
    queryFn: api.getProduits,
    staleTime: 5 * 60 * 1000,
  }),

  detail: (id: string) => queryOptions({
    queryKey: ['produits', id],
    queryFn: () => api.getProduit(id),
    staleTime: 10 * 60 * 1000,
  }),

  parCatégorie: (catId: string) => queryOptions({
    queryKey: ['produits', 'catégorie', catId],
    queryFn: () => api.getProduitsParCatégorie(catId),
  }),
};

// Mutation avec optimistic update
export function useAjouterProduit() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.créerProduit,

    // Optimistic update : UI mise à jour avant la réponse serveur
    onMutate: async (nouveauProduit) => {
      await queryClient.cancelQueries({ queryKey: ['produits'] });
      const snapshot = queryClient.getQueryData(['produits']);

      queryClient.setQueryData(['produits'], (old: Produit[]) => [
        ...old,
        { ...nouveauProduit, id: crypto.randomUUID(), _optimistic: true },
      ]);

      return { snapshot };
    },

    onError: (err, _, context) => {
      queryClient.setQueryData(['produits'], context?.snapshot); // Rollback
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['produits'] }); // Refresh
    },
  });
}
```

---

## Next.js App Router

### Stratégies de Rendu

```typescript
// app/produits/page.tsx — SSG (Static Site Generation)
// Rendu au build time → CDN cache → ultra-rapide
export const revalidate = 3600; // ISR : revalider toutes les heures

export async function generateStaticParams() {
  const catégories = await api.getCatégories();
  return catégories.map(c => ({ catégorieId: c.id }));
}

// app/dashboard/page.tsx — SSR dynamique
// export const dynamic = 'force-dynamic'; // Rendu à chaque requête

// app/produits/[id]/page.tsx — PPR (Partial Pre-Rendering, Next.js 14+)
import { Suspense } from 'react';

export default function Page({ params }: { params: { id: string } }) {
  return (
    <div>
      {/* Rendu statique au build */}
      <InfosProduitStatiques id={params.id} />

      {/* Streamé dynamiquement */}
      <Suspense fallback={<SkeletonAvis />}>
        <Avis produitId={params.id} />
      </Suspense>

      <Suspense fallback={<SkeletonStock />}>
        <StockTempsReel produitId={params.id} />
      </Suspense>
    </div>
  );
}
```

### Server Components vs Client Components

```typescript
// ✅ Server Component (par défaut dans App Router)
// - Accès direct à la DB, secrets, fs
// - Pas de useState, useEffect, event handlers
// - Pas envoyé au client → bundle plus léger

// app/produits/liste-server.tsx
async function ListeProduitsServer({ catégorieId }: { catégorieId: string }) {
  // Accès direct à la DB (pas de fetch)
  const produits = await db.query.produits.findMany({
    where: eq(produits.catégorieId, catégorieId),
  });

  return (
    <ul>
      {produits.map(p => (
        <li key={p.id}>
          <span>{p.nom}</span>
          {/* Client Component imbriqué — reçoit les données en props */}
          <BoutonAjouterPanier produitId={p.id} prix={p.prix} />
        </li>
      ))}
    </ul>
  );
}

// ✅ Client Component — uniquement pour l'interactivité
'use client';
// app/produits/bouton-panier.tsx
function BoutonAjouterPanier({ produitId, prix }: Props) {
  const { ajouter } = usePanierStore();
  return (
    <button onClick={() => ajouter({ id: produitId, prix })}>
      Ajouter au panier
    </button>
  );
}
```

### Data Fetching Patterns

```typescript
// Parallel data fetching (éviter les waterfalls)
export default async function Page({ params }: { params: { id: string } }) {
  // ❌ Séquentiel : 2 requêtes en cascade = lent
  // const produit = await api.getProduit(params.id);
  // const avis = await api.getAvis(params.id);

  // ✅ Parallèle : 2 requêtes simultanées
  const [produit, avis] = await Promise.all([
    api.getProduit(params.id),
    api.getAvis(params.id),
  ]);

  return <PageProduit produit={produit} avis={avis} />;
}

// Cache et déduplication automatique (React cache)
import { cache } from 'react';

export const getProduit = cache(async (id: string) => {
  return db.query.produits.findFirst({ where: eq(produits.id, id) });
});
// Appels multiples à getProduit(id) dans le même render → 1 seule requête DB
```

---

## Gestion des Formulaires

```typescript
// React Hook Form + Zod : validation typée
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schémaProduit = z.object({
  nom: z.string().min(2, 'Minimum 2 caractères').max(100),
  prix: z.number().positive('Le prix doit être positif'),
  description: z.string().optional(),
  catégorieId: z.string().uuid('Catégorie invalide'),
});

type FormulaireProduit = z.infer<typeof schémaProduit>;

function FormulaireAjoutProduit() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormulaireProduit>({
    resolver: zodResolver(schémaProduit),
    defaultValues: { prix: 0 },
  });

  const { mutate, isPending } = useAjouterProduit();

  const onSubmit = handleSubmit(données => mutate(données));

  return (
    <form onSubmit={onSubmit}>
      <input {...register('nom')} placeholder="Nom du produit" />
      {errors.nom && <span>{errors.nom.message}</span>}

      <input {...register('prix', { valueAsNumber: true })} type="number" />
      {errors.prix && <span>{errors.prix.message}</span>}

      <button disabled={isSubmitting || isPending}>
        {isPending ? 'Ajout...' : 'Ajouter'}
      </button>
    </form>
  );
}
```

---

## Patterns Avancés

### Error Boundaries

```typescript
'use client';
import { ErrorBoundary } from 'react-error-boundary';

function FallbackErreur({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <div role="alert">
      <p>Une erreur est survenue : {error.message}</p>
      <button onClick={resetErrorBoundary}>Réessayer</button>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary FallbackComponent={FallbackErreur} onError={logError}>
      <MonComposant />
    </ErrorBoundary>
  );
}
```

### Render Patterns Decision Tree

```
Quel rendu choisir ?
│
├── Données statiques, identiques pour tous ?
│   └── SSG (generateStaticParams) → CDN cache, ultra-rapide
│
├── Données statiques mais mises à jour régulièrement ?
│   └── ISR (revalidate: N secondes) → rebuild automatique
│
├── Données personnalisées par utilisateur / temps réel ?
│   └── SSR (dynamic = 'force-dynamic') → rendu serveur à chaque req.
│
├── Interactivité pure (toggle, modal, état local) ?
│   └── Client Component avec useState
│
└── Données serveur + interactivité = composants hybrides
    └── Server Component (fetch) → Client Component (UI interactive)
```

---

## Références

- `references/react-patterns.md` — Patterns avancés, compound components, render props, context
- `references/nextjs-app-router.md` — App Router en détail, Server Actions, middleware, auth
- `references/state-management.md` — Zustand, Jotai, Redux Toolkit, comparaison
- `references/case-studies.md` — 4 cas : migration Pages→App Router, refacto state management
