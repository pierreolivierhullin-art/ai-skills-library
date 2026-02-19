# XState v5 Avancé — Acteurs, Guards Complexes et Tests

## Overview

Ce document de référence couvre XState v5 en profondeur : le modèle d'acteurs, les guards et actions avancés, les APIs modernes introduites dans la v5, les outils de visualisation et de test, ainsi que le guide de migration depuis la v4. Utiliser ces patterns pour construire des machines robustes, testables et maintenables.

---

## Actor Model — createActor vs spawnChild vs invoke

### Comprendre les trois formes d'acteurs

XState v5 repose entièrement sur le modèle d'acteurs. Distinguer précisément les trois façons de créer un acteur est fondamental pour architecturer correctement une machine.

```
createActor(machine)   → Acteur racine, cycle de vie géré manuellement
invoke                 → Acteur enfant lié au cycle de vie d'un état
spawnChild(machine)    → Acteur enfant lié au cycle de vie de la machine parente
```

**`createActor`** — utiliser quand l'acteur représente le point d'entrée principal de l'application ou d'un composant React. Il faut appeler `.start()` manuellement et `.stop()` pour le nettoyage.

```typescript
import { createActor } from 'xstate';
import { machinePanier } from './panier.machine';

// Point d'entrée — cycle de vie géré par le composant ou le module
const acteurPanier = createActor(machinePanier, {
  input: { utilisateurId: 'usr_123' },
  inspect: (inspectionEvent) => {
    // Connecter au devtools XState
    console.log(inspectionEvent);
  },
});

acteurPanier.start();
acteurPanier.subscribe((snapshot) => {
  console.log('État courant :', snapshot.value);
  console.log('Contexte :', snapshot.context);
});

// Nettoyage propre
acteurPanier.stop();
```

**`invoke`** — utiliser pour les effets de bord liés à un état précis (promesses, callbacks, observables). L'acteur invoqué démarre quand l'état devient actif et s'arrête automatiquement quand l'état est quitté.

```typescript
import { setup, fromPromise, fromCallback } from 'xstate';

const machineRecherche = setup({
  actors: {
    // fromPromise : pour les opérations async ponctuelles
    rechercherProduits: fromPromise(async ({ input }: { input: { requête: string } }) => {
      const réponse = await fetch(`/api/produits?q=${input.requête}`);
      if (!réponse.ok) throw new Error('Recherche échouée');
      return réponse.json() as Promise<{ produits: Produit[] }>;
    }),

    // fromCallback : pour les connexions longue durée (WebSocket, timers)
    écouterMisesÀJour: fromCallback(({ input, sendBack, receive }) => {
      const ws = new WebSocket(`wss://api.monapp.fr/stream?id=${input.id}`);

      ws.onmessage = (event) => {
        sendBack({ type: 'MISE_À_JOUR_REÇUE', données: JSON.parse(event.data) });
      };

      ws.onerror = () => sendBack({ type: 'CONNEXION_ERREUR' });

      // Recevoir des messages depuis la machine parente
      receive((event) => {
        if (event.type === 'ENVOYER_MESSAGE') {
          ws.send(JSON.stringify(event.message));
        }
      });

      // Cleanup automatique quand l'état est quitté
      return () => ws.close();
    }),
  },
}).createMachine({
  id: 'recherche',
  initial: 'inactif',
  states: {
    inactif: {
      on: { RECHERCHER: { target: 'chargement', actions: assign({ requête: ({ event }) => event.terme }) } },
    },
    chargement: {
      invoke: {
        src: 'rechercherProduits',
        input: ({ context }) => ({ requête: context.requête }),
        onDone: {
          target: 'résultats',
          actions: assign({ produits: ({ event }) => event.output.produits }),
        },
        onError: {
          target: 'erreur',
          actions: assign({ erreur: ({ event }) => (event.error as Error).message }),
        },
      },
    },
    résultats: {},
    erreur: {},
  },
});
```

**`spawnChild`** — utiliser pour créer des acteurs enfants dynamiques dont le nombre n'est pas connu à l'avance (liste d'items, téléchargements parallèles, connexions multiples).

```typescript
import { setup, spawnChild, stopChild, sendTo } from 'xstate';

// Machine pour un téléchargement individuel
const machineTéléchargement = setup({
  types: {
    input: {} as { url: string; fichier: string },
  },
}).createMachine({
  id: 'téléchargement',
  initial: 'en_cours',
  context: ({ input }) => ({ url: input.url, fichier: input.fichier, progression: 0 }),
  states: {
    en_cours: {
      on: {
        PROGRESSION: { actions: assign({ progression: ({ event }) => event.pourcentage }) },
        TERMINÉ: 'complété',
        ERREUR: 'échoué',
      },
    },
    complété: { type: 'final' },
    échoué: { type: 'final' },
  },
});

// Machine gestionnaire de téléchargements multiples
const machineGestionnaire = setup({
  types: {
    context: {} as {
      téléchargements: Record<string, ActorRefFrom<typeof machineTéléchargement>>;
    },
  },
  actors: { machineTéléchargement },
}).createMachine({
  id: 'gestionnaire',
  context: { téléchargements: {} },
  on: {
    AJOUTER_TÉLÉCHARGEMENT: {
      actions: assign({
        téléchargements: ({ context, event, spawn }) => ({
          ...context.téléchargements,
          [event.id]: spawn('machineTéléchargement', {
            id: event.id,
            input: { url: event.url, fichier: event.fichier },
          }),
        }),
      }),
    },
    ANNULER_TÉLÉCHARGEMENT: {
      actions: [
        stopChild(({ event }) => event.id),
        assign({
          téléchargements: ({ context, event }) => {
            const { [event.id]: _, ...reste } = context.téléchargements;
            return reste;
          },
        }),
      ],
    },
  },
});
```

---

## Système d'Acteurs — Communication Inter-Acteurs

### sendTo, raise, forwardTo

Choisir le bon mécanisme de communication selon la relation entre acteurs.

```typescript
import { setup, sendTo, raise, forwardTo, assign } from 'xstate';

const machineParente = setup({
  actors: { machineEnfant },
}).createMachine({
  context: { acteurEnfant: null as ActorRef | null },
  states: {
    actif: {
      entry: assign({
        acteurEnfant: ({ spawn }) => spawn('machineEnfant', { id: 'enfant-1' }),
      }),
      on: {
        // sendTo : envoyer un événement à un acteur spécifique par référence ou ID
        NOTIFIER_ENFANT: {
          actions: sendTo('enfant-1', { type: 'NOTIFICATION', message: 'Bonjour' }),
        },

        // sendTo avec données dynamiques du contexte
        METTRE_À_JOUR_ENFANT: {
          actions: sendTo(
            ({ context }) => context.acteurEnfant!,
            ({ event }) => ({ type: 'MISE_À_JOUR', données: event.données }),
          ),
        },

        // raise : envoyer un événement à soi-même (traitement interne)
        AUTO_TRAITEMENT: {
          actions: raise({ type: 'TRAITEMENT_INTERNE', timestamp: Date.now() }),
        },

        // forwardTo : rediriger l'événement reçu tel quel vers un enfant
        REDIRIGER: {
          actions: forwardTo('enfant-1'),
        },
      },
    },
  },
});
```

### Acteurs persistants et communication bidirectionnelle

```typescript
// Acteur parent qui écoute les réponses de ses enfants
const machineOrchestratrice = setup({
  actors: { machineTâche },
}).createMachine({
  context: { résultats: [] as string[], tâchesActives: {} as Record<string, ActorRef> },
  on: {
    // L'enfant envoie des résultats via sendTo au parent (référencé via parentRef)
    RÉSULTAT_TÂCHE: {
      actions: assign({
        résultats: ({ context, event }) => [...context.résultats, event.résultat],
      }),
    },
  },
});

// Dans la machine enfant, référencer le parent
const machineTâche = setup({}).createMachine({
  states: {
    traitement: {
      invoke: {
        src: 'exécuterTâche',
        onDone: {
          actions: sendTo(({ system }) => system.get('orchestratrice'), ({ event }) => ({
            type: 'RÉSULTAT_TÂCHE',
            résultat: event.output,
          })),
        },
      },
    },
  },
});
```

---

## Guards Complexes — Compositions et Named Guards

### Combinaisons and(), or(), not()

XState v5 introduit des helpers de composition de guards pour construire des conditions lisibles sans code impératif.

```typescript
import { setup, and, or, not } from 'xstate';

const machineCommande = setup({
  types: {
    context: {} as {
      stock: number;
      montantTotal: number;
      utilisateurVérifié: boolean;
      tentativesPaiement: number;
      paysLivraison: string;
      estAbonné: boolean;
    },
  },
  guards: {
    // Guards atomiques — nommer clairement pour la réutilisation
    stockSuffisant: ({ context }) => context.stock > 0,
    montantValide: ({ context }) => context.montantTotal > 0 && context.montantTotal < 10000,
    utilisateurVérifié: ({ context }) => context.utilisateurVérifié,
    peutRéessayer: ({ context }) => context.tentativesPaiement < 3,
    paysSupported: ({ context }) => ['FR', 'BE', 'CH'].includes(context.paysLivraison),
    montantPremium: ({ context }) => context.montantTotal > 500,
    estAbonné: ({ context }) => context.estAbonné,

    // Guards composés — combiner les atomiques avec and(), or(), not()
    peutCommander: and(['stockSuffisant', 'montantValide', 'utilisateurVérifié', 'paysSupported']),
    peutPayer: and(['peutCommander', 'peutRéessayer']),
    bénéficieRéduction: or(['estAbonné', 'montantPremium']),
    doitVérifierIdentité: and(['montantValide', not('utilisateurVérifié')]),

    // Guard inline avec context ET event
    quantitéDisponible: ({ context, event }) => {
      return context.stock >= (event as { quantité: number }).quantité;
    },
  },
}).createMachine({
  id: 'commande',
  initial: 'panier',
  states: {
    panier: {
      on: {
        COMMANDER: [
          // Transitions gardées — première condition vraie gagne
          { guard: 'doitVérifierIdentité', target: 'vérificationIdentité' },
          { guard: 'peutCommander', target: 'paiement' },
          { target: 'erreurCommande' }, // Fallback sans guard
        ],
      },
    },
    paiement: {
      on: {
        PAYER: {
          guard: 'peutPayer',
          target: 'traitement',
        },
        RÉESSAYER: {
          guard: 'peutRéessayer',
          target: 'paiement',
        },
      },
    },
    vérificationIdentité: {},
    traitement: {},
    erreurCommande: {},
  },
});
```

---

## Actions Built-in — assign, raise, sendTo, log, stop

### assign partiel vs complet

```typescript
import { setup, assign, raise, log, stopChild } from 'xstate';

const machineFormulaire = setup({
  types: {
    context: {} as {
      étape: number;
      données: { nom: string; email: string; adresse: string };
      erreurs: Record<string, string>;
      acteurValidation: ActorRef | null;
    },
  },
}).createMachine({
  context: {
    étape: 1,
    données: { nom: '', email: '', adresse: '' },
    erreurs: {},
    acteurValidation: null,
  },
  states: {
    saisie: {
      on: {
        METTRE_À_JOUR_CHAMP: {
          // assign partiel — ne mettre à jour que les champs spécifiés
          actions: assign({
            données: ({ context, event }) => ({
              ...context.données,
              [event.champ]: event.valeur,
            }),
            erreurs: ({ context, event }) => {
              const { [event.champ]: _, ...erreursRestantes } = context.erreurs;
              return erreursRestantes;
            },
          }),
        },

        ÉTAPE_SUIVANTE: {
          actions: [
            // assign multiple champs en une fois
            assign({
              étape: ({ context }) => context.étape + 1,
              erreurs: {},
            }),
            // log pour le debugging — visible dans les devtools
            log(({ context }) => `Passage à l'étape ${context.étape + 1}`),
            // raise pour déclencher un traitement interne
            raise({ type: 'VALIDER_ÉTAPE' }),
          ],
        },

        ARRÊTER_VALIDATION: {
          actions: [
            stopChild(({ context }) => context.acteurValidation),
            assign({ acteurValidation: null }),
          ],
        },
      },
    },
  },
});
```

---

## History States — Shallow vs Deep History

### Reprendre après interruption

Les history states permettent de mémoriser quel état était actif avant de quitter une région et d'y revenir.

```typescript
const machineÉditeur = setup({}).createMachine({
  id: 'éditeur',
  initial: 'édition',
  states: {
    édition: {
      initial: 'contenu',
      states: {
        contenu: { on: { ALLER_STYLES: 'styles', ALLER_PARAMÈTRES: 'paramètres' } },
        styles: { on: { ALLER_CONTENU: 'contenu' } },
        paramètres: {
          initial: 'général',
          states: {
            général: { on: { ALLER_AVANCÉ: 'avancé' } },
            avancé: {},
          },
        },
        // shallow history : mémorise uniquement le sous-état direct
        histoireSuperficielle: { type: 'history', history: 'shallow' },
        // deep history : mémorise toute la hiérarchie d'états actifs
        histoireProfonde: { type: 'history', history: 'deep' },
      },
      on: {
        INTERRUPTION: 'interruption',
      },
    },
    interruption: {
      on: {
        REPRENDRE_SUPERFICIEL: 'édition.histoireSuperficielle',
        REPRENDRE_PROFOND: 'édition.histoireProfonde',
      },
    },
  },
});

// Exemple de comportement :
// L'utilisateur est dans édition.paramètres.avancé
// Il reçoit une interruption (alerte, notification)
// shallow history → reprend à édition.paramètres (sous-état direct mémorisé)
// deep history    → reprend à édition.paramètres.avancé (état exact mémorisé)
```

---

## Deep State Matching — matches() vs hasTag()

### Quand utiliser tags plutôt que matches

`state.matches()` vérifie la valeur d'état exacte. `state.hasTag()` est plus souple : un tag peut être appliqué à plusieurs états simultanément, ce qui permet d'interroger le comportement plutôt que la topologie.

```typescript
const machinePaiement = setup({
  types: {
    context: {} as { tentatives: number; référence: string | null },
  },
}).createMachine({
  states: {
    saisie: {
      tags: ['éditable', 'formulaireVisible'],
    },
    validation: {
      tags: ['chargement', 'formulaireVisible'],
    },
    traitement3DS: {
      tags: ['chargement', 'bloquant'],
    },
    succès: {
      tags: ['terminal', 'positif'],
    },
    erreurRéseau: {
      tags: ['erreur', 'récupérable'],
    },
    erreurCarte: {
      tags: ['erreur', 'terminal'],
    },
  },
});

// Dans le composant React — préférer hasTag() pour des conditions métier
function UIFormulairePaiement({ snapshot }: { snapshot: SnapshotFrom<typeof machinePaiement> }) {
  // ✅ hasTag — interroge le comportement, pas la topologie
  const afficherFormulaire = snapshot.hasTag('formulaireVisible');
  const estEnChargement = snapshot.hasTag('chargement');
  const estTerminal = snapshot.hasTag('terminal');
  const estRécupérable = snapshot.hasTag('récupérable');

  // ❌ matches avec états multiples — fragile si la hiérarchie change
  const afficherFormulaireFragile =
    snapshot.matches('saisie') || snapshot.matches('validation');

  return (
    <>
      {afficherFormulaire && <FormulaireChamps disabled={estEnChargement} />}
      {estEnChargement && <Spinner />}
      {estRécupérable && <BoutonRéessayer />}
    </>
  );
}
```

---

## XState v5 Nouvelles APIs — fromPromise, fromCallback, fromObservable

### Setup() — la nouvelle façon de définir les machines

`setup()` est l'API principale de XState v5 pour typer correctement les machines. Elle remplace la configuration séparée des types dans le `createMachine` de la v4.

```typescript
import { setup, fromPromise, fromCallback, fromObservable } from 'xstate';
import { fromEventPattern } from 'rxjs';

const machineComplète = setup({
  types: {
    context: {} as { données: Données | null; erreur: string | null },
    events: {} as
      | { type: 'DÉMARRER' }
      | { type: 'DONNÉE_REÇUE'; donnée: Données }
      | { type: 'ERREUR'; message: string },
    input: {} as { configId: string },
  },

  actors: {
    // fromPromise — opération async ponctuelle avec input typé
    chargerDonnées: fromPromise(async ({ input }: { input: { id: string } }) => {
      const res = await fetch(`/api/données/${input.id}`);
      return res.json() as Promise<Données>;
    }),

    // fromCallback — connexion longue durée, peut recevoir des messages
    écouterÉvénements: fromCallback<{ type: 'DONNÉES_PUSH'; données: Données }, { canal: string }>(
      ({ input, sendBack }) => {
        const source = new EventSource(`/api/stream/${input.canal}`);
        source.onmessage = (e) => sendBack({ type: 'DONNÉES_PUSH', données: JSON.parse(e.data) });
        return () => source.close(); // Cleanup
      },
    ),

    // fromObservable — intégration RxJS
    observerWebSocket: fromObservable(({ input }: { input: { url: string } }) => {
      return fromEventPattern<MessageEvent>(
        (handler) => {
          const ws = new WebSocket(input.url);
          ws.onmessage = handler;
          return ws;
        },
        (_, ws) => ws.close(),
      );
    }),
  },
}).createMachine({
  input: ({ input }) => input,
  context: { données: null, erreur: null },
  initial: 'inactif',
  states: {
    inactif: { on: { DÉMARRER: 'chargement' } },
    chargement: {
      invoke: {
        src: 'chargerDonnées',
        input: ({ context }) => ({ id: 'config-1' }),
        onDone: { target: 'actif', actions: assign({ données: ({ event }) => event.output }) },
        onError: { target: 'erreur', actions: assign({ erreur: ({ event }) => String(event.error) }) },
      },
    },
    actif: {},
    erreur: {},
  },
});
```

---

## Tests des Machines — Stratégies Complètes

### createActor + send + expect

```typescript
import { createActor } from 'xstate';
import { machinePaiement } from './paiement.machine';

describe('machinePaiement', () => {
  it('doit transitionner de saisie vers traitement lors de SOUMETTRE', () => {
    const acteur = createActor(machinePaiement).start();

    acteur.send({ type: 'SOUMETTRE', email: 'test@example.fr', montant: 50 });

    expect(acteur.getSnapshot().value).toBe('traitement');
    expect(acteur.getSnapshot().context.email).toBe('test@example.fr');

    acteur.stop();
  });

  it('ne doit pas réessayer après 3 tentatives', () => {
    const acteur = createActor(machinePaiement, {
      // Injecter un état initial avec 3 tentatives
      snapshot: machinePaiement.resolveState({
        value: 'erreur',
        context: { tentatives: 3, email: 'x@y.fr', montant: 10, erreur: 'Refusé', référenceCommande: null },
      }),
    }).start();

    acteur.send({ type: 'RÉESSAYER' });

    // La transition est bloquée par le guard peutRéessayer
    expect(acteur.getSnapshot().value).toBe('erreur');

    acteur.stop();
  });
});
```

### Snapshot Testing

```typescript
import { createActor } from 'xstate';

it('snapshot de la machine après soumission', () => {
  const acteur = createActor(machinePaiement).start();
  acteur.send({ type: 'SOUMETTRE', email: 'snap@test.fr', montant: 99 });

  const snapshot = acteur.getSnapshot();
  // Sérialiser le snapshot pour comparaison
  expect(JSON.stringify({ value: snapshot.value, context: snapshot.context }))
    .toMatchSnapshot();

  acteur.stop();
});
```

### @xstate/test — Model-Based Testing

```typescript
import { createTestModel } from '@xstate/test';
import { machinePaiement } from './paiement.machine';

const modèleTest = createTestModel(machinePaiement);

// Générer automatiquement tous les chemins de test
const plans = modèleTest.getShortestPathPlans();

plans.forEach((plan) => {
  describe(plan.description, () => {
    plan.paths.forEach((path) => {
      it(path.description, async () => {
        await path.test({
          // Mapper les états aux assertions sur l'UI ou l'acteur
          saisie: async (acteur) => {
            expect(acteur.getSnapshot().value).toBe('saisie');
          },
          traitement: async (acteur) => {
            expect(acteur.getSnapshot().value).toBe('traitement');
          },
          succès: async (acteur) => {
            expect(acteur.getSnapshot().value).toBe('succès');
            expect(acteur.getSnapshot().context.référenceCommande).toBeTruthy();
          },
          erreur: async (acteur) => {
            expect(acteur.getSnapshot().value).toBe('erreur');
            expect(acteur.getSnapshot().context.erreur).toBeTruthy();
          },
        });
      });
    });
  });
});
```

---

## Stately Studio — Import, Export et Simulation

### Workflows avec Stately Studio

Utiliser Stately Studio comme outil de communication et de validation avant de coder.

```
Workflow recommandé :
1. Ouvrir https://stately.ai/editor/new
2. Coller le code de la machine (ou importer depuis GitHub)
3. Simuler les transitions avec l'outil de simulation intégré
4. Identifier les états et transitions manquants
5. Générer des tests depuis Studio (bouton "Generate tests")
6. Exporter vers TypeScript et intégrer dans le projet

Fonctionnalités clés :
- Visualisation du graphe d'états en temps réel
- Simulation interactive — cliquer sur les transitions pour les tester
- Détection des états unreachable et des dead ends
- Collaboration en temps réel (comme Figma pour les machines)
- Génération automatique de tests @xstate/test
- Intégration GitHub — synchroniser la machine avec le dépôt
```

---

## Migration XState v4 → v5 — Breaking Changes

### Changements majeurs à connaître

```typescript
// ❌ XState v4 — patterns obsolètes
import { createMachine, assign } from 'xstate';

const machineV4 = createMachine(
  {
    id: 'exemple',
    context: { compte: 0 },
    states: {
      actif: {
        on: {
          // v4 : actions comme tableau de strings
          INCRÉMENTER: { actions: ['incrémenterCompte', 'loguer'] },
        },
      },
    },
  },
  {
    // v4 : implémentations séparées du schéma
    actions: {
      incrémenterCompte: assign({ compte: (ctx) => ctx.compte + 1 }),
      loguer: (context) => console.log(context),
    },
    guards: {
      comptePositif: (context) => context.compte > 0,
    },
    services: {
      chargerDonnées: () => fetch('/api/données').then((r) => r.json()),
    },
  },
);

// ✅ XState v5 — nouvelle API setup()
import { setup, assign, fromPromise } from 'xstate';

const machineV5 = setup({
  types: {
    context: {} as { compte: number },
    events: {} as { type: 'INCRÉMENTER' } | { type: 'CHARGER' },
  },
  // v5 : actors remplace services
  actors: {
    chargerDonnées: fromPromise(async () => {
      const r = await fetch('/api/données');
      return r.json();
    }),
  },
  actions: {
    incrémenterCompte: assign({ compte: ({ context }) => context.compte + 1 }),
    // v5 : log est une action built-in
  },
  guards: {
    comptePositif: ({ context }) => context.compte > 0,
  },
}).createMachine({
  context: { compte: 0 },
  states: {
    actif: {
      on: {
        // v5 : actions directement dans la transition
        INCRÉMENTER: { actions: ['incrémenterCompte'] },
      },
    },
  },
});
```

### Tableau récapitulatif des migrations

```
v4                          → v5
──────────────────────────────────────────────────────
services                    → actors
interpret()                 → createActor()
service.start()             → actor.start()
service.send()              → actor.send()
state.event                 → snapshot.event
State.from()                → machine.resolveState()
send() action               → sendTo() action
pure() action               → supprimé (utiliser assign)
choose() action             → if/else dans setup guards
invoke.id                   → invoke.systemId (optionnel)
{ type: 'xstate.done.actor.X' } → { type: 'xstate.done.actor.X' } (identique)
createMachine(schema, impl) → setup({ actors, guards, actions }).createMachine()
```

---

## Références Complémentaires

- Documentation officielle XState v5 : https://stately.ai/docs
- Stately Studio : https://stately.ai/editor
- @xstate/test pour le model-based testing : https://stately.ai/docs/xstate-test
- Migration v4→v5 : https://stately.ai/docs/migration
