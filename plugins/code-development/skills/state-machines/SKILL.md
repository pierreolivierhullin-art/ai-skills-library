---
name: state-machines
version: 1.0.0
description: >
  State machines XState v5 finite state machines FSM statecharts actors,
  parallel states guards actions services invoke promises,
  React useSelector useMachine XState hooks,
  Temporal.io workflows durable execution activities saga compensation,
  business workflows long-running processes orchestration,
  UI state machines checkout wizard multistep form,
  state visualization Stately Studio inspector debugging,
  Redux Zustand state management comparison patterns
---

# State Machines — XState, Statecharts et Workflows Durables

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu as une logique d'état complexe avec de nombreux `if/else` et états incohérents possibles
- Tu dois modéliser un workflow multi-étapes (checkout, onboarding, formulaire wizard)
- Tu veux utiliser XState v5 pour rendre l'état d'une UI explicite et testable
- Tu construis des processus métier long-running avec Temporal.io (commandes, paiements, onboardings)
- Tu veux visualiser et déboguer les transitions d'état de ton application
- Tu gères des états asynchrones complexes (fetch → loading → success | error → retry)

---

## Fondamentaux — Machine à États Finis

```
Concepts clés :
├── État (state)       — Une situation dans laquelle peut se trouver le système
├── Transition         — Un changement d'état déclenché par un événement
├── Événement (event)  — Ce qui provoque une transition
├── Action             — Effet de bord lors d'une transition (sans retour)
├── Guard (condition)  — Condition booléenne pour autoriser une transition
└── Context            — Données attachées à la machine (état étendu)

Anti-pattern sans machine à états :
// ❌ États incohérents possibles : isLoading + isError = true en même temps ?
const [isLoading, setIsLoading] = useState(false);
const [isError, setIsError] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);

// ✅ Avec une machine à états : un seul état actif à la fois
type ÉtatPaiement = 'saisie' | 'traitement' | 'succès' | 'erreur';
```

---

## XState v5 — Machines à États pour TypeScript

```typescript
import { setup, createActor, assign, fromPromise } from 'xstate';

// Machine de checkout e-commerce
const machinePaiement = setup({
  types: {
    context: {} as {
      montant: number;
      email: string;
      tentatives: number;
      erreur: string | null;
      référenceCommande: string | null;
    },
    events: {} as
      | { type: 'SOUMETTRE'; email: string; montant: number }
      | { type: 'RÉESSAYER' }
      | { type: 'ANNULER' },
  },
  actors: {
    traiterPaiement: fromPromise(async ({
      input,
    }: {
      input: { email: string; montant: number };
    }) => {
      const réponse = await fetch('/api/paiements', {
        method: 'POST',
        body: JSON.stringify(input),
      });
      if (!réponse.ok) throw new Error('Paiement refusé');
      return (await réponse.json()) as { référence: string };
    }),
  },
  guards: {
    peutRéessayer: ({ context }) => context.tentatives < 3,
  },
}).createMachine({
  id: 'paiement',
  initial: 'saisie',
  context: {
    montant: 0,
    email: '',
    tentatives: 0,
    erreur: null,
    référenceCommande: null,
  },

  states: {
    saisie: {
      on: {
        SOUMETTRE: {
          target: 'traitement',
          actions: assign({
            email: ({ event }) => event.email,
            montant: ({ event }) => event.montant,
          }),
        },
      },
    },

    traitement: {
      invoke: {
        src: 'traiterPaiement',
        input: ({ context }) => ({
          email: context.email,
          montant: context.montant,
        }),
        onDone: {
          target: 'succès',
          actions: assign({
            référenceCommande: ({ event }) => event.output.référence,
          }),
        },
        onError: {
          target: 'erreur',
          actions: assign({
            tentatives: ({ context }) => context.tentatives + 1,
            erreur: ({ event }) => (event.error as Error).message,
          }),
        },
      },
    },

    succès: {
      type: 'final',
    },

    erreur: {
      on: {
        RÉESSAYER: {
          guard: 'peutRéessayer',
          target: 'traitement',
          actions: assign({ erreur: null }),
        },
        ANNULER: 'saisie',
      },
    },
  },
});

// Créer et démarrer l'acteur
const acteur = createActor(machinePaiement);
acteur.start();
acteur.send({ type: 'SOUMETTRE', email: 'user@ex.fr', montant: 99.99 });
```

---

## XState v5 + React

```typescript
// hooks/usePaiement.ts
import { useMachine } from '@xstate/react';
import { machinePaiement } from './machines/paiement.machine';

export function usePaiement() {
  const [état, envoyer, acteur] = useMachine(machinePaiement);

  return {
    // États dérivés
    estEnTraitement: état.matches('traitement'),
    estSuccès: état.matches('succès'),
    estErreur: état.matches('erreur'),
    peutRéessayer: état.context.tentatives < 3,

    // Context
    référenceCommande: état.context.référenceCommande,
    messageErreur: état.context.erreur,
    tentatives: état.context.tentatives,

    // Actions
    soumettre: (email: string, montant: number) =>
      envoyer({ type: 'SOUMETTRE', email, montant }),
    réessayer: () => envoyer({ type: 'RÉESSAYER' }),
    annuler: () => envoyer({ type: 'ANNULER' }),
  };
}

// Composant React — état toujours cohérent
function FormulairePaiement() {
  const {
    estEnTraitement, estSuccès, estErreur,
    peutRéessayer, référenceCommande, messageErreur,
    soumettre, réessayer,
  } = usePaiement();

  if (estSuccès) {
    return (
      <div className="alert-success">
        <p>Paiement confirmé !</p>
        <p>Référence : {référenceCommande}</p>
      </div>
    );
  }

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      const data = new FormData(e.currentTarget);
      soumettre(data.get('email') as string, 99.99);
    }}>
      <input name="email" type="email" required />
      <button type="submit" disabled={estEnTraitement}>
        {estEnTraitement ? 'Traitement...' : 'Payer 99.99€'}
      </button>
      {estErreur && (
        <div className="alert-error">
          <p>{messageErreur}</p>
          {peutRéessayer && (
            <button type="button" onClick={réessayer}>
              Réessayer
            </button>
          )}
        </div>
      )}
    </form>
  );
}
```

---

## États Parallèles — Régions Orthogonales

```typescript
// Machine avec états parallèles (actifs simultanément)
const machineÉditeur = setup({
  types: {
    context: {} as {
      contenu: string;
      titre: string;
    },
    events: {} as
      | { type: 'SAISIR_TITRE'; valeur: string }
      | { type: 'SAISIR_CONTENU'; valeur: string }
      | { type: 'SAUVEGARDER' }
      | { type: 'PUBLIER' },
  },
}).createMachine({
  id: 'éditeur',
  type: 'parallel',  // États actifs en même temps
  context: { contenu: '', titre: '' },

  states: {
    // Région 1 : état de saisie
    formulaire: {
      initial: 'inchangé',
      states: {
        inchangé: {
          on: {
            SAISIR_TITRE: {
              target: 'modifié',
              actions: assign({ titre: ({ event }) => event.valeur }),
            },
            SAISIR_CONTENU: {
              target: 'modifié',
              actions: assign({ contenu: ({ event }) => event.valeur }),
            },
          },
        },
        modifié: {
          on: {
            SAUVEGARDER: 'sauvegarde',
          },
        },
        sauvegarde: {
          invoke: {
            src: 'sauvegarder',
            onDone: 'inchangé',
            onError: 'modifié',
          },
        },
      },
    },

    // Région 2 : état de publication (indépendant)
    publication: {
      initial: 'brouillon',
      states: {
        brouillon: {
          on: { PUBLIER: 'publication' },
        },
        publication: {
          invoke: {
            src: 'publier',
            onDone: 'publié',
            onError: 'brouillon',
          },
        },
        publié: { type: 'final' },
      },
    },
  },
});
```

---

## Temporal.io — Workflows Durables

```typescript
// workflows/onboarding.workflow.ts
import { proxyActivities, sleep, condition, setHandler, defineSignal, defineQuery } from '@temporalio/workflow';
import type * as activities from './onboarding.activities';

// Proxy des activités (exécutées dans des workers séparés)
const {
  envoyerEmailBienvenue,
  créerCompteStripe,
  envoyerEmailRappel,
  envoyerEmailConversion,
  désactiverEssai,
} = proxyActivities<typeof activities>({
  startToCloseTimeout: '30 seconds',
  retry: {
    maximumAttempts: 3,
    initialInterval: '1s',
    backoffCoefficient: 2,
  },
});

// Signaux (entrées externes)
const signalCompteActivé = defineSignal('compteActivé');
const signalAbonnementSouscrit = defineSignal('abonnementSouscrit');

// Queries (état interrogeable de l'extérieur)
const queryStatut = defineQuery<string>('statut');

// Workflow d'onboarding — survit aux redémarrages serveur
export async function workflowOnboarding(utilisateurId: string): Promise<void> {
  let compteActivé = false;
  let abonnementSouscrit = false;
  let statut = 'email_envoyé';

  // Gérer les signaux entrants
  setHandler(signalCompteActivé, () => { compteActivé = true; });
  setHandler(signalAbonnementSouscrit, () => { abonnementSouscrit = true; });
  setHandler(queryStatut, () => statut);

  // Étape 1 : Créer le compte Stripe (avec retry automatique)
  await créerCompteStripe(utilisateurId);
  await envoyerEmailBienvenue(utilisateurId);
  statut = 'bienvenue_envoyé';

  // Étape 2 : Attendre l'activation du compte (max 7 jours)
  const activéÀTemps = await condition(
    () => compteActivé,
    '7 days'
  );

  if (!activéÀTemps) {
    await envoyerEmailRappel(utilisateurId, 'compte_non_activé');
    statut = 'rappel_envoyé';

    // Attendre encore 7 jours puis désactiver
    await sleep('7 days');
    if (!compteActivé) {
      await désactiverEssai(utilisateurId);
      return;
    }
  }

  statut = 'compte_activé';

  // Étape 3 : Attendre la souscription (14 jours d'essai gratuit)
  await sleep('7 days');
  if (!abonnementSouscrit) {
    await envoyerEmailConversion(utilisateurId, 'j7');
  }

  await sleep('7 days');
  if (!abonnementSouscrit) {
    await envoyerEmailConversion(utilisateurId, 'j14_dernier_rappel');
  }

  // Fin de l'essai
  if (!abonnementSouscrit) {
    await désactiverEssai(utilisateurId);
    statut = 'essai_expiré';
  } else {
    statut = 'converti';
  }
}
```

```typescript
// workflows/onboarding.activities.ts
import { ApplicationFailure } from '@temporalio/activity';
import { resend } from '../lib/email';
import { stripe } from '../lib/stripe';

export async function créerCompteStripe(utilisateurId: string) {
  const utilisateur = await db.utilisateurs.findOrThrow(utilisateurId);

  const compte = await stripe.customers.create({
    email: utilisateur.email,
    name: utilisateur.nom,
    metadata: { utilisateurId },
  });

  await db.utilisateurs.update(utilisateurId, {
    stripeCustomerId: compte.id,
  });
}

export async function envoyerEmailBienvenue(utilisateurId: string) {
  const utilisateur = await db.utilisateurs.findOrThrow(utilisateurId);

  const { error } = await resend.emails.send({
    from: 'noreply@monapp.fr',
    to: utilisateur.email,
    subject: 'Bienvenue !',
    react: EmailBienvenue({ prénom: utilisateur.prénom }),
  });

  if (error) {
    // ApplicationFailure = erreur métier, pas de retry
    throw ApplicationFailure.nonRetryable(
      `Impossible d'envoyer l'email: ${error.message}`
    );
  }
}
```

---

## Visualisation avec Stately Studio

```typescript
// Annoter la machine pour la visualisation
// Importer sur https://stately.ai/registry/new

/** @xstate-layout N4IgpgJg5mDOIC5QGUCuA7... */
const machine = setup({ ... }).createMachine({
  // La machine peut être copiée-collée directement dans Stately Studio
  // pour visualiser le graphe d'états et simuler des transitions
});

// Debug en développement
import { createBrowserInspector } from '@statelyai/inspect';

const { inspect } = createBrowserInspector();

const acteur = createActor(machine, {
  inspect,  // Active le devtools dans le navigateur
});
```

---

## Quand Choisir Quoi ?

```
Problème                     → Solution recommandée
───────────────────────────────────────────────────────────────────
État UI complexe             → XState v5 avec useMachine()
Workflow multi-étapes court  → XState invoked promises
Processus métier long-running
  qui survit aux redémarrages → Temporal.io Workflow
Compensation de saga         → Temporal.io (signaux + conditions)
État global simple           → Zustand / Jotai
Formulaire wizard            → XState + React Hook Form
Séquence de micro-tâches
  avec retry/backoff         → Temporal.io Activities

Règle d'or : si le processus doit survivre à un redémarrage serveur
ou durer plus de quelques secondes → Temporal.io plutôt que XState
```

---

## Références

- `references/xstate-patterns.md` — XState v5 avancé (acteurs spawné/invoked, système d'acteurs, deep state matching, guards complexes, actions built-in), Stately Studio, tests des machines
- `references/temporal-workflows.md` — Temporal.io en profondeur (namespaces, worker configuration, versioning de workflows, continue-as-new, schedules, signaux/queries avancés)
- `references/fsm-ui.md` — Patterns UI avec XState (formulaires wizard, drag-and-drop, menus complexes, animations coordonnées), React Flow, comparaison avec Zustand/Redux
- `references/case-studies.md` — 4 cas : checkout e-commerce avec XState (0 état incohérent), workflow Temporal onboarding 14 jours, migration useState → XState, saga de paiement avec compensation
