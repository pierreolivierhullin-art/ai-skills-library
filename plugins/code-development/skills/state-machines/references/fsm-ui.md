# FSM pour Interfaces Complexes — Formulaires Wizard, Drag-and-Drop et Animations

## Overview

Ce document de référence couvre l'application des machines à états finis aux interfaces utilisateur complexes : formulaires wizard multi-étapes, drag-and-drop, menus accessibles, animations coordonnées, et comparaisons avec les solutions alternatives (Zustand, Redux Toolkit, Jotai). Utiliser XState pour les interactions UI dont la logique d'état dépasse deux niveaux de conditions imbriquées.

---

## Formulaires Wizard Multi-Étapes — Machine Complète

### Architecture de la machine wizard

```typescript
import { setup, assign, fromPromise } from 'xstate';

interface DonnéesWizard {
  // Étape 1 — Informations personnelles
  prénom: string;
  nom: string;
  email: string;
  téléphone: string;

  // Étape 2 — Adresse
  adresseLigne1: string;
  adresseLigne2: string;
  ville: string;
  codePostal: string;
  pays: string;

  // Étape 3 — Abonnement
  plan: 'starter' | 'pro' | 'enterprise' | '';
  périodicité: 'mensuel' | 'annuel';
  codePromo: string | null;
  réduction: number;

  // Méta
  erreurs: Record<string, string>;
  étapeActuelle: 1 | 2 | 3 | 4;
  soumis: boolean;
  référenceInscription: string | null;
}

const machineWizardInscription = setup({
  types: {
    context: {} as DonnéesWizard,
    events: {} as
      | { type: 'ÉTAPE_SUIVANTE' }
      | { type: 'ÉTAPE_PRÉCÉDENTE' }
      | { type: 'METTRE_À_JOUR'; champ: keyof DonnéesWizard; valeur: string }
      | { type: 'APPLIQUER_PROMO'; code: string }
      | { type: 'SOUMETTRE' }
      | { type: 'RÉINITIALISER' },
  },
  actors: {
    validerÉtape1: fromPromise(async ({ input }: { input: Pick<DonnéesWizard, 'prénom' | 'nom' | 'email' | 'téléphone'> }) => {
      const erreurs: Record<string, string> = {};
      if (!input.prénom.trim()) erreurs.prénom = 'Le prénom est requis';
      if (!input.nom.trim()) erreurs.nom = 'Le nom est requis';
      if (!input.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) erreurs.email = 'Email invalide';
      if (Object.keys(erreurs).length > 0) throw erreurs;
      return true;
    }),

    validerÉtape2: fromPromise(async ({ input }: { input: Pick<DonnéesWizard, 'adresseLigne1' | 'ville' | 'codePostal' | 'pays'> }) => {
      const erreurs: Record<string, string> = {};
      if (!input.adresseLigne1.trim()) erreurs.adresseLigne1 = 'L\'adresse est requise';
      if (!input.codePostal.match(/^\d{5}$/)) erreurs.codePostal = 'Code postal invalide (5 chiffres)';
      if (!input.ville.trim()) erreurs.ville = 'La ville est requise';
      if (Object.keys(erreurs).length > 0) throw erreurs;
      return true;
    }),

    appliquerCodePromo: fromPromise(async ({ input }: { input: { code: string } }) => {
      const réponse = await fetch('/api/promos/valider', {
        method: 'POST',
        body: JSON.stringify({ code: input.code }),
        headers: { 'Content-Type': 'application/json' },
      });
      if (!réponse.ok) throw new Error('Code promo invalide');
      return réponse.json() as Promise<{ réduction: number }>;
    }),

    soumettreInscription: fromPromise(async ({ input }: { input: DonnéesWizard }) => {
      const réponse = await fetch('/api/inscriptions', {
        method: 'POST',
        body: JSON.stringify(input),
        headers: { 'Content-Type': 'application/json' },
      });
      if (!réponse.ok) throw new Error('Échec de l\'inscription');
      return réponse.json() as Promise<{ référence: string }>;
    }),
  },
  guards: {
    étape1Remplie: ({ context }) =>
      Boolean(context.prénom && context.nom && context.email),
    étape2Remplie: ({ context }) =>
      Boolean(context.adresseLigne1 && context.ville && context.codePostal),
    étape3Remplie: ({ context }) => Boolean(context.plan),
    peutReculer: ({ context }) => context.étapeActuelle > 1,
  },
}).createMachine({
  id: 'wizardInscription',
  initial: 'étape1',
  context: {
    prénom: '', nom: '', email: '', téléphone: '',
    adresseLigne1: '', adresseLigne2: '', ville: '', codePostal: '', pays: 'FR',
    plan: '', périodicité: 'mensuel', codePromo: null, réduction: 0,
    erreurs: {}, étapeActuelle: 1, soumis: false, référenceInscription: null,
  },

  on: {
    METTRE_À_JOUR: {
      actions: assign({
        [({ event }) => event.champ]: ({ event }) => event.valeur,
        erreurs: ({ context, event }) => {
          const { [event.champ]: _, ...reste } = context.erreurs;
          return reste;
        },
      }),
    },
  },

  states: {
    étape1: {
      meta: { titre: 'Informations personnelles', progression: 25 },
      on: {
        ÉTAPE_SUIVANTE: {
          guard: 'étape1Remplie',
          target: 'validationÉtape1',
        },
      },
    },

    validationÉtape1: {
      invoke: {
        src: 'validerÉtape1',
        input: ({ context }) => ({
          prénom: context.prénom, nom: context.nom,
          email: context.email, téléphone: context.téléphone,
        }),
        onDone: {
          target: 'étape2',
          actions: assign({ étapeActuelle: 2, erreurs: {} }),
        },
        onError: {
          target: 'étape1',
          actions: assign({ erreurs: ({ event }) => event.error as Record<string, string> }),
        },
      },
    },

    étape2: {
      meta: { titre: 'Adresse de livraison', progression: 50 },
      on: {
        ÉTAPE_SUIVANTE: { guard: 'étape2Remplie', target: 'validationÉtape2' },
        ÉTAPE_PRÉCÉDENTE: { target: 'étape1', actions: assign({ étapeActuelle: 1 }) },
      },
    },

    validationÉtape2: {
      invoke: {
        src: 'validerÉtape2',
        input: ({ context }) => ({
          adresseLigne1: context.adresseLigne1, ville: context.ville,
          codePostal: context.codePostal, pays: context.pays,
        }),
        onDone: { target: 'étape3', actions: assign({ étapeActuelle: 3 }) },
        onError: { target: 'étape2', actions: assign({ erreurs: ({ event }) => event.error as Record<string, string> }) },
      },
    },

    étape3: {
      meta: { titre: 'Choisir un plan', progression: 75 },
      on: {
        ÉTAPE_SUIVANTE: { guard: 'étape3Remplie', target: 'récapitulatif' },
        ÉTAPE_PRÉCÉDENTE: { target: 'étape2', actions: assign({ étapeActuelle: 2 }) },
        APPLIQUER_PROMO: { target: 'applicationPromo' },
      },
    },

    applicationPromo: {
      invoke: {
        src: 'appliquerCodePromo',
        input: ({ event }) => ({ code: (event as { type: 'APPLIQUER_PROMO'; code: string }).code }),
        onDone: {
          target: 'étape3',
          actions: assign({
            codePromo: ({ event }) => 'code',
            réduction: ({ event }) => event.output.réduction,
          }),
        },
        onError: {
          target: 'étape3',
          actions: assign({ erreurs: { codePromo: 'Code promo invalide ou expiré' } }),
        },
      },
    },

    récapitulatif: {
      meta: { titre: 'Récapitulatif', progression: 90 },
      on: {
        SOUMETTRE: 'soumission',
        ÉTAPE_PRÉCÉDENTE: { target: 'étape3', actions: assign({ étapeActuelle: 3 }) },
      },
    },

    soumission: {
      invoke: {
        src: 'soumettreInscription',
        input: ({ context }) => context,
        onDone: {
          target: 'succès',
          actions: assign({ soumis: true, référenceInscription: ({ event }) => event.output.référence }),
        },
        onError: {
          target: 'récapitulatif',
          actions: assign({ erreurs: { soumission: 'Erreur lors de l\'inscription. Réessayez.' } }),
        },
      },
    },

    succès: {
      meta: { titre: 'Inscription confirmée', progression: 100 },
      type: 'final',
    },
  },
});
```

### Intégration XState + React Hook Form

```typescript
import { useMachine } from '@xstate/react';
import { useForm } from 'react-hook-form';

function ÉtapeInfosPersonnelles() {
  const [état, envoyer] = useMachine(machineWizardInscription);
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      prénom: état.context.prénom,
      nom: état.context.nom,
      email: état.context.email,
    },
  });

  // Synchroniser React Hook Form → machine à chaque changement
  const synchroniser = (champ: string) => (valeur: string) =>
    envoyer({ type: 'METTRE_À_JOUR', champ: champ as keyof DonnéesWizard, valeur });

  const soumettrÉtape = handleSubmit(() => {
    // React Hook Form valide le format local, la machine valide côté serveur
    envoyer({ type: 'ÉTAPE_SUIVANTE' });
  });

  return (
    <form onSubmit={soumettrÉtape}>
      <input
        {...register('prénom', { required: 'Requis', onChange: (e) => synchroniser('prénom')(e.target.value) })}
      />
      {errors.prénom && <p>{errors.prénom.message}</p>}
      {/* Erreurs de la machine (validation serveur) */}
      {état.context.erreurs.prénom && <p>{état.context.erreurs.prénom}</p>}

      <button type="submit" disabled={état.matches('validationÉtape1')}>
        {état.matches('validationÉtape1') ? 'Validation...' : 'Suivant'}
      </button>
    </form>
  );
}
```

---

## Drag-and-Drop Machine — États et Guards

### Machine pour une liste réordonnable

```typescript
import { setup, assign } from 'xstate';

interface ContextDnD {
  items: { id: string; titre: string; colonneId: string }[];
  itemGlissé: string | null;
  colonneSource: string | null;
  colonneCible: string | null;
  indexCible: number | null;
  positionSouris: { x: number; y: number };
}

const machineDragAndDrop = setup({
  types: {
    context: {} as ContextDnD,
    events: {} as
      | { type: 'COMMENCER_GLISSER'; itemId: string; colonneId: string; x: number; y: number }
      | { type: 'SURVOL_COLONNE'; colonneId: string; indexCible: number }
      | { type: 'QUITTER_COLONNE' }
      | { type: 'DÉPOSER' }
      | { type: 'ANNULER' }
      | { type: 'DÉPLACER_SOURIS'; x: number; y: number },
  },
  guards: {
    // Guard : peut-on déposer dans cette colonne ?
    colonneAccepte: ({ context, event }) => {
      if (event.type !== 'SURVOL_COLONNE') return false;
      // Exemple : limiter à 10 items par colonne
      const itemsDansColonne = context.items.filter((i) => i.colonneId === event.colonneId);
      return itemsDansColonne.length < 10;
    },
    différenteColonne: ({ context }) =>
      context.colonneCible !== null && context.colonneCible !== context.colonneSource,
  },
  actions: {
    réorganiserItems: assign({
      items: ({ context }) => {
        if (!context.itemGlissé || !context.colonneCible || context.indexCible === null) {
          return context.items;
        }

        const itemsDéplacés = context.items.filter((i) => i.id !== context.itemGlissé);
        const itemGlissé = context.items.find((i) => i.id === context.itemGlissé)!;
        const itemMàJ = { ...itemGlissé, colonneId: context.colonneCible };

        // Insérer à l'index cible dans la nouvelle colonne
        const itemsNouvelleColonne = itemsDéplacés.filter((i) => i.colonneId === context.colonneCible);
        const itemsAutresColonnes = itemsDéplacés.filter((i) => i.colonneId !== context.colonneCible);

        itemsNouvelleColonne.splice(context.indexCible, 0, itemMàJ);
        return [...itemsAutresColonnes, ...itemsNouvelleColonne];
      },
    }),
  },
}).createMachine({
  id: 'dragAndDrop',
  initial: 'repos',
  context: {
    items: [], itemGlissé: null, colonneSource: null,
    colonneCible: null, indexCible: null, positionSouris: { x: 0, y: 0 },
  },

  states: {
    repos: {
      on: {
        COMMENCER_GLISSER: {
          target: 'glissement',
          actions: assign({
            itemGlissé: ({ event }) => event.itemId,
            colonneSource: ({ event }) => event.colonneId,
            positionSouris: ({ event }) => ({ x: event.x, y: event.y }),
          }),
        },
      },
    },

    glissement: {
      on: {
        DÉPLACER_SOURIS: {
          actions: assign({ positionSouris: ({ event }) => ({ x: event.x, y: event.y }) }),
        },
        SURVOL_COLONNE: [
          {
            guard: 'colonneAccepte',
            target: 'survol',
            actions: assign({
              colonneCible: ({ event }) => event.colonneId,
              indexCible: ({ event }) => event.indexCible,
            }),
          },
        ],
        ANNULER: {
          target: 'repos',
          actions: assign({ itemGlissé: null, colonneSource: null, colonneCible: null }),
        },
      },
    },

    survol: {
      on: {
        QUITTER_COLONNE: {
          target: 'glissement',
          actions: assign({ colonneCible: null, indexCible: null }),
        },
        SURVOL_COLONNE: [
          {
            guard: 'colonneAccepte',
            actions: assign({
              colonneCible: ({ event }) => event.colonneId,
              indexCible: ({ event }) => event.indexCible,
            }),
          },
        ],
        DÉPOSER: {
          target: 'repos',
          actions: ['réorganiserItems', assign({ itemGlissé: null, colonneSource: null, colonneCible: null, indexCible: null })],
        },
        ANNULER: {
          target: 'repos',
          actions: assign({ itemGlissé: null, colonneSource: null, colonneCible: null, indexCible: null }),
        },
      },
    },
  },
});
```

---

## Menus et Popovers Complexes — Accessibilité et Clavier

### Machine open/closed/animating avec interactions clavier

```typescript
import { setup, assign } from 'xstate';

const machinePopover = setup({
  types: {
    context: {} as {
      ancreÉlément: HTMLElement | null;
      popoverÉlément: HTMLElement | null;
      premierFocusable: HTMLElement | null;
      dernierFocusable: HTMLElement | null;
    },
    events: {} as
      | { type: 'OUVRIR'; ancre: HTMLElement }
      | { type: 'FERMER' }
      | { type: 'ANIMATION_OUVERTURE_TERMINÉE' }
      | { type: 'ANIMATION_FERMETURE_TERMINÉE' }
      | { type: 'TAB' }
      | { type: 'SHIFT_TAB' }
      | { type: 'ESCAPE' }
      | { type: 'CLIC_EXTÉRIEUR' },
  },
  actions: {
    piégerFocus: ({ context }) => {
      // Trouver tous les éléments focusables dans le popover
      const focusables = context.popoverÉlément?.querySelectorAll<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      if (focusables?.length) {
        focusables[0].focus(); // Focus sur le premier élément
      }
    },
    restaurerFocus: ({ context }) => {
      context.ancreÉlément?.focus();
    },
    déplacerFocusSuivant: ({ context }) => {
      const actif = document.activeElement as HTMLElement;
      if (actif === context.dernierFocusable) {
        context.premierFocusable?.focus(); // Cycle
      }
    },
    déplacerFocusPrécédent: ({ context }) => {
      const actif = document.activeElement as HTMLElement;
      if (actif === context.premierFocusable) {
        context.dernierFocusable?.focus(); // Cycle inverse
      }
    },
  },
}).createMachine({
  id: 'popover',
  initial: 'fermé',
  states: {
    fermé: {
      on: {
        OUVRIR: {
          target: 'animationOuverture',
          actions: assign({ ancreÉlément: ({ event }) => event.ancre }),
        },
      },
    },
    animationOuverture: {
      entry: assign({ /* classe CSS d'animation */ }),
      on: {
        ANIMATION_OUVERTURE_TERMINÉE: { target: 'ouvert', actions: ['piégerFocus'] },
        ESCAPE: { target: 'fermé', actions: ['restaurerFocus'] },
      },
    },
    ouvert: {
      on: {
        FERMER: 'animationFermeture',
        ESCAPE: { target: 'animationFermeture', actions: ['restaurerFocus'] },
        CLIC_EXTÉRIEUR: 'animationFermeture',
        TAB: { actions: ['déplacerFocusSuivant'] },
        SHIFT_TAB: { actions: ['déplacerFocusPrécédent'] },
      },
    },
    animationFermeture: {
      on: {
        ANIMATION_FERMETURE_TERMINÉE: 'fermé',
      },
    },
  },
});
```

---

## Animations Coordonnées avec Framer Motion

### Déclencher les animations depuis les transitions XState

```typescript
import { useMachine, useSelector } from '@xstate/react';
import { motion, AnimatePresence } from 'framer-motion';

function WizardAnimé() {
  const [état, envoyer, acteur] = useMachine(machineWizardInscription);

  const étapeActuelle = useSelector(acteur, (s) => s.context.étapeActuelle);
  const estEnValidation = useSelector(acteur, (s) =>
    s.matches('validationÉtape1') || s.matches('validationÉtape2'),
  );

  return (
    <div className="wizard-conteneur">
      {/* Barre de progression animée par la machine */}
      <motion.div
        className="barre-progression"
        animate={{ width: `${état.getMeta()?.progression ?? 0}%` }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      />

      {/* Transitions entre étapes — AnimatePresence gère l'entrée/sortie */}
      <AnimatePresence mode="wait">
        <motion.div
          key={étapeActuelle} // Changement de key = nouvelle animation
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -50 }}
          transition={{ duration: 0.25, ease: 'easeInOut' }}
        >
          {étapeActuelle === 1 && <ÉtapeInfosPersonnelles />}
          {étapeActuelle === 2 && <ÉtapeAdresse />}
          {étapeActuelle === 3 && <ÉtapePlan />}
        </motion.div>
      </AnimatePresence>

      {/* Indicateur de chargement coordonné */}
      <AnimatePresence>
        {estEnValidation && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            className="overlay-validation"
          >
            <Spinner />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
```

---

## Comparaison XState vs Zustand vs Redux Toolkit

### Quand choisir XState

```
Utiliser XState quand :
✓ La logique d'état a des transitions explicites (état A → événement → état B)
✓ L'état peut être dans des modes mutuellement exclusifs (idle/loading/error/success)
✓ Il faut documenter le comportement — la machine est une spécification vivante
✓ Les tests doivent couvrir toutes les transitions (model-based testing)
✓ Des effets de bord sont liés à des états précis (invoke)
✓ L'UI a des interactions complexes (wizard, DnD, menus avec focus trap)

Utiliser Zustand quand :
✓ L'état est principalement des données sans transitions complexes
✓ Besoin d'un store global simple et léger (< 5 KB)
✓ Les actions ne suivent pas un flux prédéfini
✓ L'équipe préfère une API minimaliste et familière (proche de useState)
✓ Pas d'interactions asynchrones complexes à modéliser

Utiliser Redux Toolkit quand :
✓ L'équipe a déjà un store Redux existant
✓ Besoin des Redux DevTools pour time-travel debugging
✓ Gestion d'une grande quantité d'état normalisé (entités, relations)
✓ Middleware complexe (RTK Query pour le caching des requêtes)
```

### Migration Zustand → XState

```typescript
// Avant — Zustand avec logique d'état implicite
const useStorePanier = create((set, get) => ({
  items: [],
  estChargement: false,
  erreur: null,
  ajouterItem: async (produit) => {
    set({ estChargement: true });
    try {
      const résultat = await fetch('/api/panier/ajouter', { method: 'POST', body: JSON.stringify(produit) });
      set({ items: await résultat.json(), estChargement: false });
    } catch (e) {
      set({ estChargement: false, erreur: e.message }); // ← état incohérent possible
    }
  },
}));

// Après — XState avec transitions explicites
const machinePanier = setup({
  actors: {
    ajouterItem: fromPromise(async ({ input }) => {
      const res = await fetch('/api/panier/ajouter', { method: 'POST', body: JSON.stringify(input) });
      return res.json();
    }),
  },
}).createMachine({
  initial: 'inactif',
  context: { items: [], erreur: null },
  states: {
    inactif: {
      on: { AJOUTER: 'chargement' },
    },
    chargement: {
      // estChargement est implicite — l'état "chargement" EST le chargement
      invoke: {
        src: 'ajouterItem',
        input: ({ event }) => event.produit,
        onDone: { target: 'inactif', actions: assign({ items: ({ event }) => event.output }) },
        onError: { target: 'erreur', actions: assign({ erreur: ({ event }) => String(event.error) }) },
      },
    },
    erreur: {
      on: { RÉESSAYER: 'inactif', EFFACER_ERREUR: { target: 'inactif', actions: assign({ erreur: null }) } },
    },
  },
});
```

### Redux Toolkit createSlice vs machines

```typescript
// Redux Toolkit — adapté pour les données normalisées
const sliceProduits = createSlice({
  name: 'produits',
  initialState: produitsAdapter.getInitialState({ statut: 'idle', erreur: null }),
  reducers: {
    produitMàJ: produitsAdapter.updateOne,
  },
  extraReducers: (builder) => {
    builder
      .addCase(chargerProduits.pending, (state) => { state.statut = 'loading'; })
      .addCase(chargerProduits.fulfilled, (state, action) => {
        state.statut = 'succeeded';
        produitsAdapter.setAll(state, action.payload);
      })
      .addCase(chargerProduits.rejected, (state, action) => {
        state.statut = 'failed';
        state.erreur = action.error.message ?? null;
      });
  },
});

// XState — adapté pour les flux avec états complexes
// Utiliser RTK pour le catalogue produits (données, normalisées, pas de flux)
// Utiliser XState pour le checkout (flux, transitions, guards)
```

---

## Jotai Atoms + XState — État Global Partagé

### atom from actor

```typescript
import { atom, useAtom, useAtomValue } from 'jotai';
import { createActor } from 'xstate';
import { machinePanier } from './panier.machine';

// Créer l'acteur XState comme singleton partagé
const acteurPanierSingleton = createActor(machinePanier);
acteurPanierSingleton.start();

// Exposer l'état de la machine comme atom Jotai
const snapshotPanierAtom = atom(acteurPanierSingleton.getSnapshot());

// Synchroniser les mises à jour de la machine vers Jotai
acteurPanierSingleton.subscribe((snapshot) => {
  // Mettre à jour l'atom manuellement (via store Jotai)
});

// Hook pour consommer la machine depuis n'importe quel composant
function useStatePanier() {
  const snapshot = useAtomValue(snapshotPanierAtom);
  return {
    items: snapshot.context.items,
    estChargement: snapshot.matches('chargement'),
    ajouter: (produit: Produit) => acteurPanierSingleton.send({ type: 'AJOUTER', produit }),
  };
}
```

---

## useSelector vs useMachine — Performances

### Éviter les re-renders inutiles avec useSelector

```typescript
import { useActor, useSelector } from '@xstate/react';

// ❌ useMachine — re-render à CHAQUE changement d'état ou de contexte
function ComposantNaïf() {
  const [état] = useMachine(machinePanier); // Re-render si n'importe quel champ change
  return <span>{état.context.items.length} articles</span>;
}

// ✅ useSelector — re-render uniquement si le résultat du sélecteur change
function ComposantOptimisé({ acteur }: { acteur: ActorRefFrom<typeof machinePanier> }) {
  const nbArticles = useSelector(acteur, (snapshot) => snapshot.context.items.length);
  // Re-render uniquement si nbArticles change

  const estEnChargement = useSelector(acteur, (snapshot) => snapshot.matches('chargement'));
  // Re-render uniquement si l'état chargement change

  return (
    <span className={estEnChargement ? 'opacity-50' : ''}>
      {nbArticles} articles
    </span>
  );
}

// Pattern recommandé : passer l'acteur en prop pour useSelector
function AppPanier() {
  const [, , acteur] = useMachine(machinePanier); // Acteur racine ici seulement

  return (
    <div>
      <CompteurArticles acteur={acteur} />
      <TotalPrix acteur={acteur} />
      <BoutonCommander acteur={acteur} />
    </div>
  );
}

// Sélecteurs mémoïsés avec comparaison personnalisée
const sélecteurItems = (snapshot: SnapshotFrom<typeof machinePanier>) =>
  snapshot.context.items;

function ListeArticles({ acteur }: { acteur: ActorRefFrom<typeof machinePanier> }) {
  // Comparateur personnalisé — re-render uniquement si les IDs changent
  const items = useSelector(
    acteur,
    sélecteurItems,
    (a, b) => a.map((i) => i.id).join(',') === b.map((i) => i.id).join(','),
  );

  return (
    <ul>
      {items.map((item) => <ArticleItem key={item.id} acteur={acteur} itemId={item.id} />)}
    </ul>
  );
}
```

---

## Références Complémentaires

- XState + React Hook Form integration : https://stately.ai/docs/xstate-react
- Framer Motion documentation : https://www.framer.com/motion
- Radix UI pour les composants accessibles : https://www.radix-ui.com
- Zustand documentation : https://github.com/pmndrs/zustand
- Jotai + XState : https://jotai.org/docs/integrations/xstate
