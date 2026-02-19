# State Management — Zustand, Jotai, Redux Toolkit

## Overview

Ce document de référence couvre les solutions de gestion d'état pour les applications React en 2025. Il traite chaque outil en profondeur — Zustand, Jotai, Redux Toolkit, et TanStack Query — avec leurs patterns avancés, leurs intégrations TypeScript, et les critères de choix entre solutions. Le choix d'un outil de state management est une décision d'architecture qui doit être faite consciemment, pas par défaut.

---

## Arbre de Décision — Quel Outil Choisir

```
Quelle est la nature de cet état ?
│
├── État local d'un seul composant (formulaire, toggle, animation)
│   └── useState / useReducer → pas besoin d'outil externe
│
├── État partagé entre quelques composants proches dans l'arbre
│   └── Lifting state up + Context simple
│
├── Données serveur (fetch, cache, synchronisation)
│   └── TanStack Query (React Query) — standard de l'industrie
│
├── État UI global simple (thème, sidebar ouverte, notifications)
│   └── Zustand — léger, sans boilerplate
│
├── Collections atomiques (items sélectionnés, config par entité)
│   └── Jotai — atoms composables, granulaires
│
└── État global complexe avec logique métier riche
    ├── Application de taille moyenne → Zustand avec slices
    └── Grande application avec équipe + DevTools nécessaires → Redux Toolkit
```

### Comparaison Rapide

| | Zustand | Jotai | Redux Toolkit | TanStack Query |
|---|---|---|---|---|
| Bundle (gzippé) | ~1.2 Ko | ~3 Ko | ~13 Ko | ~13 Ko |
| Philosophie | Store impératif | Atomes fonctionnels | Flux Redux moderne | Server state dédié |
| TypeScript | Excellent | Excellent | Excellent | Excellent |
| DevTools | Redux DevTools | Jotai DevTools | Redux DevTools natif | TanStack Query DevTools |
| React Native | Oui | Oui | Oui | Oui |
| Courbe d'apprentissage | Faible | Faible-Moyenne | Moyenne | Faible-Moyenne |
| Cas d'usage idéal | UI state global | État fin et composable | Apps complexes, équipes | Données distantes |

---

## Zustand — Patterns Avancés

### Pattern Slices avec TypeScript

Le pattern slices décompose un store complexe en morceaux indépendants recombinés dans un seul `create`.

```typescript
// store/slices/produits.slice.ts
import { StateCreator } from 'zustand';

export interface ProduitsSlice {
  produits: Produit[];
  filtre: string;
  setProduits: (produits: Produit[]) => void;
  setFiltre: (filtre: string) => void;
  produitsFiltrés: () => Produit[];
}

export const créerProduitsSlice: StateCreator<
  ProduitsSlice & PanierSlice, // Accès au store complet pour les computed
  [['zustand/immer', never], ['zustand/devtools', never]],
  [],
  ProduitsSlice
> = (set, get) => ({
  produits: [],
  filtre: '',

  setProduits: (produits) => set(state => { state.produits = produits; }),
  setFiltre: (filtre) => set(state => { state.filtre = filtre; }),

  produitsFiltrés: () => {
    const { produits, filtre } = get();
    if (!filtre) return produits;
    return produits.filter(p =>
      p.nom.toLowerCase().includes(filtre.toLowerCase())
    );
  },
});

// store/slices/panier.slice.ts
export interface PanierSlice {
  items: ItemPanier[];
  ajouter: (produit: Produit) => void;
  retirer: (id: string) => void;
  vider: () => void;
  total: () => number;
}

export const créerPanierSlice: StateCreator<
  ProduitsSlice & PanierSlice,
  [['zustand/immer', never], ['zustand/devtools', never]],
  [],
  PanierSlice
> = (set, get) => ({
  items: [],

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

  vider: () => set(state => { state.items = []; }),

  total: () => get().items.reduce((sum, i) => sum + i.prix * i.quantité, 0),
});

// store/app.store.ts — Combinaison des slices
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

type AppStore = ProduitsSlice & PanierSlice;

export const useAppStore = create<AppStore>()(
  devtools(
    persist(
      immer((...args) => ({
        ...créerProduitsSlice(...args),
        ...créerPanierSlice(...args),
      })),
      {
        name: 'app-store',
        // partialize : persister seulement le panier, pas les produits (chargés depuis API)
        partialize: (state): Partial<AppStore> => ({ items: state.items }),
      }
    ),
    { name: 'App Store' }
  )
);
```

### Sélecteurs et Shallow pour Éviter les Re-renders

```typescript
import { shallow } from 'zustand/shallow';

// ❌ Re-render si N'IMPORTE QUELLE valeur du store change
const { items, total, ajouter } = useAppStore();

// ✅ Re-render seulement si items OU total changent (shallow comparison)
const { items, total } = useAppStore(
  state => ({ items: state.items, total: state.total() }),
  shallow
);

// ✅ Sélecteur primitif — re-render seulement si le nombre d'items change
const nombreItems = useAppStore(state => state.items.length);

// ✅ Pattern hook dédié — encapsule la logique de sélection
export function useNombreItems() {
  return useAppStore(state => state.items.length);
}

export function useProduitsDansPanier() {
  return useAppStore(
    state => new Set(state.items.map(i => i.id)),
    (a, b) => {
      // Comparaison custom — égalité par contenu du Set
      if (a.size !== b.size) return false;
      for (const val of a) { if (!b.has(val)) return false; }
      return true;
    }
  );
}
```

### Middleware Immer — Mutations Immutables

```typescript
// Sans immer — syntax verbose pour les mises à jour imbriquées
set(state => ({
  ...state,
  utilisateur: {
    ...state.utilisateur,
    adresse: {
      ...state.utilisateur.adresse,
      ville: 'Paris',
    },
  },
}));

// Avec immer — mutations directes, immer gère l'immutabilité
set(state => { state.utilisateur.adresse.ville = 'Paris'; });
```

---

## Jotai — Atomes Composables

Jotai adopte une approche "bottom-up" : partir de petits atomes primitifs et les composer.

### Atomes de Base et Dérivés

```typescript
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai';
import { atomWithStorage, atomWithReset, RESET } from 'jotai/utils';

// Atomes primitifs
const produitsAtom = atom<Produit[]>([]);
const filtreAtom = atom<string>('');
const pageAtom = atom<number>(1);

// Atome dérivé (read-only) — se recalcule si produitsAtom ou filtreAtom change
const produitsFiltrésAtom = atom(get => {
  const produits = get(produitsAtom);
  const filtre = get(filtreAtom);
  return filtre
    ? produits.filter(p => p.nom.toLowerCase().includes(filtre.toLowerCase()))
    : produits;
});

// Atome dérivé avec pagination
const produitsPageAtom = atom(get => {
  const filtrés = get(produitsFiltrésAtom);
  const page = get(pageAtom);
  const PAR_PAGE = 24;
  return {
    items: filtrés.slice((page - 1) * PAR_PAGE, page * PAR_PAGE),
    total: filtrés.length,
    totalPages: Math.ceil(filtrés.length / PAR_PAGE),
  };
});

// atomWithStorage — persist automatiquement dans localStorage
const thèmeAtom = atomWithStorage<'light' | 'dark'>('thème', 'light');
const panierAtom = atomWithStorage<ItemPanier[]>('panier', []);

// Utilisation optimisée — seulement ce dont le composant a besoin
function FiltreRecherche() {
  const [filtre, setFiltre] = useAtom(filtreAtom);
  return <input value={filtre} onChange={e => setFiltre(e.target.value)} />;
  // Ce composant ne re-render PAS si les produits changent
}

function ListeProduits() {
  const { items, total, totalPages } = useAtomValue(produitsPageAtom);
  const setPage = useSetAtom(pageAtom);
  // Ne re-render que si la page courante de produits change
  return (/* ... */);
}
```

### Atomes Asynchrones

```typescript
import { atom } from 'jotai';
import { loadable } from 'jotai/utils';

// Atome qui fetche des données
const utilisateurAtom = atom(async (get) => {
  const userId = get(userIdAtom);
  const response = await fetch(`/api/utilisateurs/${userId}`);
  if (!response.ok) throw new Error('Utilisateur introuvable');
  return response.json() as Promise<Utilisateur>;
});

// loadable — gérer loading/error sans Suspense
const utilisateurLoadableAtom = loadable(utilisateurAtom);

function ProfilUtilisateur() {
  const état = useAtomValue(utilisateurLoadableAtom);

  if (état.state === 'loading') return <Spinner />;
  if (état.state === 'hasError') return <Erreur message={String(état.error)} />;
  // état.state === 'hasData'
  return <Profil utilisateur={état.data} />;
}
```

### atomFamily — Collections d'Atomes

```typescript
import { atomFamily } from 'jotai/utils';

// Un atome par produit — granularité maximale
const étatSélectionAtomFamily = atomFamily((produitId: string) =>
  atom(false) // false = non sélectionné
);

// Atome dérivé : IDs de tous les produits sélectionnés
const produitsSélectionnésAtom = atom(get => {
  return TOUS_PRODUIT_IDS.filter(id => get(étatSélectionAtomFamily(id)));
});

function CarteProduit({ produit }: { produit: Produit }) {
  const [estSélectionné, setSélectionné] = useAtom(étatSélectionAtomFamily(produit.id));
  // Re-render seulement si CET atome change — pas les autres produits
  return (
    <div style={{ border: estSélectionné ? '2px solid blue' : '1px solid grey' }}>
      <input type="checkbox" checked={estSélectionné} onChange={e => setSélectionné(e.target.checked)} />
      {produit.nom}
    </div>
  );
}
```

---

## Redux Toolkit — Applications Complexes

Redux Toolkit (RTK) est Redux moderne : moins de boilerplate, TypeScript first, patterns intégrés.

### createSlice et createAsyncThunk

```typescript
// store/slices/commandesSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// Thunk typé pour les appels asynchrones
export const fetchCommandes = createAsyncThunk(
  'commandes/fetchTout',
  async (filtres: FiltresCommande, { rejectWithValue }) => {
    try {
      const response = await api.getCommandes(filtres);
      return response.data;
    } catch (error) {
      return rejectWithValue((error as AxiosError).response?.data);
    }
  }
);

export const annulerCommande = createAsyncThunk(
  'commandes/annuler',
  async ({ id, raison }: { id: string; raison: string }, { dispatch }) => {
    const result = await api.annulerCommande(id, raison);
    dispatch(fetchCommandes({})); // Rafraîchir la liste après annulation
    return result.data;
  }
);

interface EtatCommandes {
  items: Commande[];
  chargement: boolean;
  erreur: string | null;
  sélectionnée: string | null;
}

const initialState: EtatCommandes = {
  items: [],
  chargement: false,
  erreur: null,
  sélectionnée: null,
};

const commandesSlice = createSlice({
  name: 'commandes',
  initialState,
  reducers: {
    sélectionner(state, action: PayloadAction<string>) {
      state.sélectionnée = action.payload;
    },
    désélectionner(state) {
      state.sélectionnée = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchCommandes.pending, (state) => {
        state.chargement = true;
        state.erreur = null;
      })
      .addCase(fetchCommandes.fulfilled, (state, action) => {
        state.chargement = false;
        state.items = action.payload;
      })
      .addCase(fetchCommandes.rejected, (state, action) => {
        state.chargement = false;
        state.erreur = action.payload as string ?? 'Erreur inconnue';
      });
  },
});

export const { sélectionner, désélectionner } = commandesSlice.actions;
export default commandesSlice.reducer;
```

### createEntityAdapter — État Normalisé

```typescript
import { createEntityAdapter, createSlice } from '@reduxjs/toolkit';

const produitsAdapter = createEntityAdapter<Produit>({
  selectId: (produit) => produit.id,
  sortComparer: (a, b) => a.nom.localeCompare(b.nom),
});

const produitsSlice = createSlice({
  name: 'produits',
  initialState: produitsAdapter.getInitialState({ chargement: false }),
  reducers: {
    produitAjouté: produitsAdapter.addOne,
    produitsAjoutés: produitsAdapter.setMany,
    produitModifié: produitsAdapter.updateOne,
    produitSupprimé: produitsAdapter.removeOne,
  },
  extraReducers: (builder) => {
    builder.addCase(fetchProduits.fulfilled, (state, action) => {
      produitsAdapter.setAll(state, action.payload);
      state.chargement = false;
    });
  },
});

// Sélecteurs générés automatiquement par l'adapter
export const {
  selectAll: sélectionnerTousProduits,
  selectById: sélectionnerProduitParId,
  selectIds: sélectionnerIdsProduits,
  selectTotal: sélectionnerNombreProduits,
} = produitsAdapter.getSelectors((state: RootState) => state.produits);
```

### RTK Query — Data Fetching Intégré

```typescript
// store/api/commandesApi.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const commandesApi = createApi({
  reducerPath: 'commandesApi',
  baseQuery: fetchBaseQuery({
    baseUrl: '/api',
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) headers.set('authorization', `Bearer ${token}`);
      return headers;
    },
  }),
  tagTypes: ['Commande', 'Produit'],

  endpoints: (builder) => ({
    getCommandes: builder.query<Commande[], FiltresCommande>({
      query: (filtres) => ({ url: '/commandes', params: filtres }),
      providesTags: (result) =>
        result
          ? [...result.map(c => ({ type: 'Commande' as const, id: c.id })), 'Commande']
          : ['Commande'],
    }),

    annulerCommande: builder.mutation<Commande, { id: string; raison: string }>({
      query: ({ id, raison }) => ({
        url: `/commandes/${id}/annuler`,
        method: 'POST',
        body: { raison },
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'Commande', id }],
    }),

    créerCommande: builder.mutation<Commande, NouvelleCommande>({
      query: (commande) => ({ url: '/commandes', method: 'POST', body: commande }),
      invalidatesTags: ['Commande'],
      // Optimistic update
      async onQueryStarted(arg, { dispatch, queryFulfilled }) {
        try {
          const { data: nouvelleCommande } = await queryFulfilled;
          dispatch(
            commandesApi.util.updateQueryData('getCommandes', {}, draft => {
              draft.unshift(nouvelleCommande);
            })
          );
        } catch {}
      },
    }),
  }),
});

export const {
  useGetCommandesQuery,
  useAnnulerCommandeMutation,
  useCréerCommandeMutation,
} = commandesApi;
```

---

## TanStack Query — Patterns Avancés

### Requêtes Dépendantes et Parallèles

```typescript
// Requête dépendante — attend que userId soit disponible
function ProfilUtilisateur({ userId }: { userId: string | null }) {
  const { data: utilisateur } = useQuery({
    queryKey: ['utilisateur', userId],
    queryFn: () => api.getUtilisateur(userId!),
    enabled: !!userId, // Ne s'exécute pas si userId est null/undefined
  });

  const { data: commandes } = useQuery({
    queryKey: ['commandes', utilisateur?.id],
    queryFn: () => api.getCommandesUtilisateur(utilisateur!.id),
    enabled: !!utilisateur, // Attend la résolution de la requête précédente
  });
}

// Requêtes parallèles multiples avec useQueries
function ComparaisonProduits({ ids }: { ids: string[] }) {
  const résultats = useQueries({
    queries: ids.map(id => ({
      queryKey: ['produit', id],
      queryFn: () => api.getProduit(id),
      staleTime: 5 * 60 * 1000,
    })),
  });

  const produits = résultats.filter(r => r.isSuccess).map(r => r.data!);
  const enChargement = résultats.some(r => r.isLoading);
}
```

### Prefetching au Survol

```typescript
function LienProduit({ produit }: { produit: Produit }) {
  const queryClient = useQueryClient();

  const précharger = () => {
    queryClient.prefetchQuery({
      queryKey: ['produit', produit.id],
      queryFn: () => api.getProduit(produit.id),
      staleTime: 10 * 60 * 1000,
    });
  };

  return (
    <Link
      href={`/produits/${produit.id}`}
      onMouseEnter={précharger} // Précharge au survol — données disponibles au clic
      onFocus={précharger}      // Accessibilité : précharger aussi au focus clavier
    >
      {produit.nom}
    </Link>
  );
}
```

### Infinite Queries

```typescript
function ListeInfinie() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['produits', 'infini'],
    queryFn: ({ pageParam = 1 }) => api.getProduits({ page: pageParam, limite: 24 }),
    getNextPageParam: (dernièrePage, toutesPages) =>
      dernièrePage.hasMore ? toutesPages.length + 1 : undefined,
    initialPageParam: 1,
  });

  // Intersection Observer pour le scroll infini automatique
  const refSentinelle = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting && hasNextPage) fetchNextPage(); },
      { threshold: 0.5 }
    );
    if (refSentinelle.current) observer.observe(refSentinelle.current);
    return () => observer.disconnect();
  }, [hasNextPage, fetchNextPage]);

  return (
    <div>
      {data?.pages.flatMap(page => page.items).map(p => (
        <CarteProduit key={p.id} produit={p} />
      ))}
      <div ref={refSentinelle}>
        {isFetchingNextPage && <Spinner />}
      </div>
    </div>
  );
}
```

### Optimistic Updates

```typescript
function useAjouterCommentaire(produitId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (contenu: string) => api.ajouterCommentaire(produitId, contenu),

    onMutate: async (contenu) => {
      // Annuler les requêtes en cours pour éviter les conflits
      await queryClient.cancelQueries({ queryKey: ['commentaires', produitId] });

      // Sauvegarder l'état actuel pour rollback
      const snapshot = queryClient.getQueryData<Commentaire[]>(['commentaires', produitId]);

      // Mise à jour optimiste
      const commentaireOptimiste: Commentaire = {
        id: `temp-${Date.now()}`,
        contenu,
        auteur: 'Moi',
        créeÀ: new Date().toISOString(),
        _optimiste: true,
      };

      queryClient.setQueryData<Commentaire[]>(
        ['commentaires', produitId],
        old => [commentaireOptimiste, ...(old ?? [])]
      );

      return { snapshot }; // Retourné dans onError pour le rollback
    },

    onError: (err, variables, context) => {
      // Rollback vers l'état sauvegardé
      queryClient.setQueryData(['commentaires', produitId], context?.snapshot);
    },

    onSettled: () => {
      // Toujours rafraîchir après succès ou erreur
      queryClient.invalidateQueries({ queryKey: ['commentaires', produitId] });
    },
  });
}
```

---

## Migration Entre Solutions

### Contexte → Zustand

```typescript
// ❌ Avant : Context avec re-renders cascadants
const AppContext = createContext<AppState>(defaultState);
// Tout composant consommant le context re-render si N'IMPORTE QUELLE valeur change

// ✅ Après : Zustand avec sélecteurs ciblés
// 1. Créer le store Zustand avec le même état
// 2. Remplacer useContext(AppContext) par des sélecteurs précis
// 3. Supprimer le Provider — Zustand est un singleton externe à l'arbre React
const utilisateur = useAppStore(state => state.utilisateur); // Sélecteur ciblé
```

### Redux classique → Redux Toolkit

```typescript
// ❌ Avant : Redux classique — verbose
// Action types constants, action creators manuels, reducer avec switch imbriqués

// ✅ Après : RTK — remplacer reducer par slice
// 1. createSlice remplace les action types + creators + reducer
// 2. configureStore remplace createStore + combineReducers + middleware manual
// 3. createAsyncThunk remplace les thunks manuels
// Migration possible progressivement slice par slice
```

### fetch manuel → TanStack Query

```typescript
// ❌ Avant : useEffect + useState (gestion manuelle du cache)
const [données, setDonnées] = useState(null);
const [chargement, setChargement] = useState(false);
useEffect(() => {
  setChargement(true);
  fetch('/api/produits').then(r => r.json()).then(d => {
    setDonnées(d);
    setChargement(false);
  });
}, []);

// ✅ Après : useQuery (cache, revalidation, loading states automatiques)
const { data: données, isLoading: chargement } = useQuery({
  queryKey: ['produits'],
  queryFn: () => fetch('/api/produits').then(r => r.json()),
});
// Migration : remplacer chaque useEffect de fetch par useQuery
```
