# Temporal.io — Configuration, Versioning et Patterns Avancés

## Overview

Ce document de référence couvre Temporal.io en profondeur : l'architecture du serveur, la configuration des workers, les namespaces, les signaux et queries avancés, le continue-as-new, les Temporal Schedules, le versioning de workflows, le saga pattern avec compensation, les child workflows, et la comparaison Cloud vs self-hosted. Utiliser Temporal pour tout processus métier devant survivre aux redémarrages serveur et dont la durée dépasse quelques secondes.

---

## Architecture Temporal — Schéma et Composants

### Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (SDK TypeScript)                  │
│  workflowClient.start()   workflowClient.signal()               │
│  workflowClient.query()   scheduleClient.create()               │
└────────────────────────────┬────────────────────────────────────┘
                             │ gRPC
┌────────────────────────────▼────────────────────────────────────┐
│                       TEMPORAL SERVER                           │
│                                                                 │
│  ┌─────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │  Frontend Service│  │  History Service │  │Matching Service│  │
│  │  (API Gateway)  │  │  (état workflow)  │  │(assignation   │  │
│  └─────────────────┘  └──────────────────┘  │ task queues)  │  │
│                                              └───────────────┘  │
│  ┌─────────────────┐  ┌──────────────────┐                     │
│  │  Internal Worker│  │  Visibility DB   │                     │
│  │  (timers, retry)│  │  (recherche UI)  │                     │
│  └─────────────────┘  └──────────────────┘                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
┌─────────────▼──────────┐   ┌─────────────▼──────────┐
│   BACKEND (Cassandra    │   │   VISIBILITY (Elastic   │
│   ou PostgreSQL)        │   │   Search ou PostgreSQL) │
│   Stockage de l'historique│ │   Recherche de workflows│
└────────────────────────┘   └────────────────────────┘
              │
┌─────────────▼──────────────────────────────────────────────────┐
│                         WORKERS                                 │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Worker Process (Node.js)                               │   │
│  │  ├── Workflow Worker (exécute le code déterministe)    │   │
│  │  └── Activity Worker (exécute les effets de bord)      │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

### Choix du backend

```
PostgreSQL  → Préférer pour < 1M workflows actifs, déploiements simples
Cassandra   → Préférer pour > 1M workflows actifs, scalabilité horizontale
             (Temporal Cloud utilise Cassandra en interne)

Visibility :
PostgreSQL  → Suffisant pour les petites et moyennes installations
ElasticSearch → Obligatoire si filtrage avancé des workflows (tag:, type:, status:)
```

---

## Worker Configuration — Concurrence et Rate Limits

### Configuration complète d'un worker

```typescript
// worker.ts
import { Worker, NativeConnection } from '@temporalio/worker';
import * as activities from './activities';

async function run() {
  // Connexion explicite avec TLS pour la production
  const connexion = await NativeConnection.connect({
    address: process.env.TEMPORAL_ADDRESS ?? 'localhost:7233',
    tls: process.env.NODE_ENV === 'production'
      ? {
          serverNameOverride: process.env.TEMPORAL_SERVER_NAME,
          serverRootCACertificate: Buffer.from(process.env.TEMPORAL_TLS_CA!, 'base64'),
          clientCertPair: {
            crt: Buffer.from(process.env.TEMPORAL_TLS_CERT!, 'base64'),
            key: Buffer.from(process.env.TEMPORAL_TLS_KEY!, 'base64'),
          },
        }
      : undefined,
  });

  const worker = await Worker.create({
    connexion,
    namespace: process.env.TEMPORAL_NAMESPACE ?? 'default',

    // Task queue — isoler par domaine fonctionnel
    taskQueue: 'paiements-worker',

    // Chemins vers les workflows (compilés)
    workflowsPath: require.resolve('./workflows'),
    activities,

    // Concurrence — adapter selon la taille des VMs
    maxConcurrentWorkflowTaskExecutions: 100,   // Workflows en parallèle
    maxConcurrentActivityTaskExecutions: 50,    // Activities en parallèle
    maxConcurrentLocalActivityExecutions: 20,   // Local activities (sans round-trip)

    // Rate limits — protection des systèmes downstream
    maxActivitiesPerSecond: 100,                // Taux global du worker
    maxTaskQueueActivitiesPerSecond: 50,        // Taux au niveau de la task queue

    // Timeout de poll — augmenter en production pour réduire les connexions
    stickyScheduleToStartTimeout: '10s',
  });

  // Graceful shutdown
  process.on('SIGINT', () => worker.shutdown());
  process.on('SIGTERM', () => worker.shutdown());

  console.log('Worker démarré sur la task queue paiements-worker');
  await worker.run();
}

run().catch((err) => {
  console.error('Erreur fatale du worker :', err);
  process.exit(1);
});
```

### Dimensionnement des workers

```
Règles de dimensionnement :
─────────────────────────────────────────────────────────────────
maxConcurrentWorkflows   → CPU × 10 à 20 (code déterministe, peu de CPU)
maxConcurrentActivities  → Limité par les ressources système :
  - I/O-bound (API, DB) → CPU × 5 à 10
  - CPU-bound           → CPU × 1 à 2

Monitoring des saturation :
- temporal_worker_task_slots_available → doit être > 0
- temporal_activity_schedule_to_start_latency → alarme si > 500ms
- temporal_workflow_task_schedule_to_start_latency → alarme si > 200ms

Recommandation production :
- Déployer workers en autoscaling sur métriques de latence
- Séparer les workers par task queue pour isoler les domaines
- Worker critique (paiements) → instances dédiées, pas de co-location
```

---

## Namespaces — Isolation par Environnement

### Créer et gérer les namespaces

```bash
# Créer les namespaces avec la CLI Temporal
temporal operator namespace create \
  --namespace dev \
  --retention 7d \
  --description "Développement local"

temporal operator namespace create \
  --namespace staging \
  --retention 14d \
  --description "Environnement de staging"

temporal operator namespace create \
  --namespace production \
  --retention 90d \
  --description "Production — conserver 90 jours pour audits"

# Lister les namespaces existants
temporal operator namespace list
```

### Configuration dans le SDK

```typescript
// client.ts — client réutilisable par namespace
import { Client, Connection } from '@temporalio/client';

function créerClientTemporal(namespace: string): Client {
  const connexion = await Connection.connect({
    address: process.env.TEMPORAL_ADDRESS!,
  });

  return new Client({ connexion, namespace });
}

// Utiliser le namespace approprié selon l'environnement
const client = créerClientTemporal(process.env.TEMPORAL_NAMESPACE ?? 'development');

// Démarrer un workflow dans le namespace configuré
await client.workflow.start(workflowOnboarding, {
  taskQueue: 'onboarding-worker',
  workflowId: `onboarding-${utilisateurId}`,
  args: [utilisateurId],
});
```

### Retention policies

```
Durée de rétention recommandée par environnement :
─────────────────────────────────────────────────
dev         → 1 à 7 jours (nettoyage fréquent)
staging     → 14 à 30 jours
production  → 30 à 90 jours selon exigences légales

Important : la rétention s'applique après la fermeture du workflow.
Les workflows en cours (ouverts) ne sont jamais supprimés.
Un workflow onboarding de 14 jours + rétention 30 jours
→ conservé jusqu'à 44 jours après démarrage.
```

---

## Signaux et Queries Avancés

### defineSignal, defineQuery, setHandler

```typescript
// types/signaux.ts — Définir les signaux et queries séparément pour le partage
import { defineSignal, defineQuery } from '@temporalio/workflow';

// Signaux (entrées asynchrones, modifient l'état)
export const signalPaiementReçu = defineSignal<[{ référence: string; montant: number }]>('paiementReçu');
export const signalCommandeAnnulée = defineSignal<[{ raison: string }]>('commandeAnnulée');
export const signalLivraionConfirmée = defineSignal('livraisonConfirmée');

// Queries (lectures synchrones, ne modifient pas l'état)
export const queryStatutCommande = defineQuery<StatutCommande>('statutCommande');
export const queryHistorique = defineQuery<ÉvénementCommande[]>('historique');
export const queryEstimationLivraison = defineQuery<Date | null>('estimationLivraison');
```

```typescript
// workflows/commande.workflow.ts
import {
  proxyActivities, sleep, condition, setHandler, defineSignal, defineQuery
} from '@temporalio/workflow';
import {
  signalPaiementReçu, signalCommandeAnnulée,
  queryStatutCommande, queryHistorique
} from '../types/signaux';

export async function workflowCommande(commandeId: string): Promise<void> {
  let statut: StatutCommande = 'EN_ATTENTE_PAIEMENT';
  let paiementReçu = false;
  let annulée = false;
  const historique: ÉvénementCommande[] = [];

  const ajouterÉvénement = (type: string, données?: unknown) => {
    historique.push({ type, timestamp: new Date().toISOString(), données });
  };

  // Enregistrer les handlers de signaux AVANT le premier await
  // (convention Temporal : setHandler doit être appelé de manière synchrone)
  setHandler(signalPaiementReçu, ({ référence, montant }) => {
    paiementReçu = true;
    statut = 'PAYÉE';
    ajouterÉvénement('PAIEMENT_REÇU', { référence, montant });
  });

  setHandler(signalCommandeAnnulée, ({ raison }) => {
    annulée = true;
    statut = 'ANNULÉE';
    ajouterÉvénement('ANNULÉE', { raison });
  });

  // Enregistrer les handlers de queries
  setHandler(queryStatutCommande, () => statut);
  setHandler(queryHistorique, () => [...historique]);

  ajouterÉvénement('CRÉÉE');

  // Attendre le paiement (max 24h)
  const payéÀTemps = await condition(() => paiementReçu || annulée, '24h');

  if (annulée || !payéÀTemps) {
    statut = 'EXPIRÉE';
    await libérerStock(commandeId);
    return;
  }

  // Continuer le traitement...
  statut = 'EN_PRÉPARATION';
  await préparerCommande(commandeId);
}
```

### signalWithStart — créer et signaler en une opération atomique

```typescript
// Utile quand le workflow peut ou ne pas encore exister
const handle = await client.workflow.signalWithStart(workflowCommande, {
  workflowId: `commande-${commandeId}`,
  taskQueue: 'commandes-worker',
  args: [commandeId],
  signal: signalPaiementReçu,
  signalArgs: [{ référence: 'PAY-456', montant: 99.90 }],
  // Si le workflow existe déjà → envoyer le signal uniquement
  // Si le workflow n'existe pas → démarrer ET envoyer le signal
});

// Interroger l'état depuis une API REST
const queryClient = client.workflow.getHandle(`commande-${commandeId}`);
const statut = await queryClient.query(queryStatutCommande);
```

---

## Continue-as-New — Gérer les Historiques Longs

### Éviter la limite des 50 000 événements

```typescript
import { continueAsNew, isCancellation } from '@temporalio/workflow';

interface ÉtatWorkflowLongDurée {
  itération: number;
  totalTraité: number;
  curseur: string | null;
  configId: string;
}

export async function workflowTraitementLongDurée(état: ÉtatWorkflowLongDurée): Promise<void> {
  const { itération, totalTraité, curseur, configId } = état;

  // Traiter un lot de données
  const résultat = await traiterLot({ curseur, tailleLot: 100, configId });

  const nouvelÉtat: ÉtatWorkflowLongDurée = {
    itération: itération + 1,
    totalTraité: totalTraité + résultat.nbTraité,
    curseur: résultat.curseurSuivant,
    configId,
  };

  // Stratégie de continue-as-new :
  // Se déclencher AVANT d'atteindre 50K événements (marge de sécurité à 10K)
  if (itération % 100 === 0 || résultat.curseurSuivant === null) {
    if (résultat.curseurSuivant !== null) {
      // Continue avec un historique frais, en transmettant l'état
      await continueAsNew<typeof workflowTraitementLongDurée>(nouvelÉtat);
    }
    // Si curseurSuivant === null, le traitement est complet
    return;
  }

  // Récursion normale dans la même exécution
  return workflowTraitementLongDurée(nouvelÉtat);
}

// Démarrer le workflow avec l'état initial
await client.workflow.start(workflowTraitementLongDurée, {
  workflowId: 'traitement-catalogue-2024',
  taskQueue: 'traitement-worker',
  args: [{ itération: 0, totalTraité: 0, curseur: null, configId: 'catalogue-v3' }],
});
```

---

## Temporal Schedules — Remplacer les Cron Jobs

### Créer un schedule Temporal

```typescript
import { ScheduleClient, ScheduleOverlapPolicy } from '@temporalio/client';

const scheduleClient = new ScheduleClient({ connexion, namespace: 'production' });

// Remplacer un cron job de rapport hebdomadaire
const schedule = await scheduleClient.create({
  scheduleId: 'rapport-hebdomadaire-clients',
  spec: {
    // Format cron standard — tous les lundis à 8h00 UTC
    cronExpressions: ['0 8 * * MON'],
    // Ou utiliser les intervalles structurés
    // intervals: [{ every: '7d', offset: '8h' }],
  },
  action: {
    type: 'startWorkflow',
    workflowType: workflowRapportHebdomadaire,
    taskQueue: 'rapports-worker',
    workflowExecutionTimeout: '2h',
    args: [{ typeRapport: 'activité_clients', format: 'pdf' }],
  },
  policies: {
    // Que faire si l'exécution précédente est encore en cours
    overlap: ScheduleOverlapPolicy.SKIP,  // Ignorer si en cours
    // BUFFER_ONE — mettre en attente une exécution max
    // ALLOW_ALL  — lancer même si en cours (parallélisme)

    // Rattrapage des exécutions manquées (ex: serveur down le weekend)
    catchupWindow: '4h',  // Rattraper jusqu'à 4h d'exécutions manquées
  },
  state: {
    note: 'Rapport d\'activité client envoyé chaque lundi matin',
    paused: false,
  },
});

// Opérations sur le schedule existant
const handle = scheduleClient.getHandle('rapport-hebdomadaire-clients');

// Mettre en pause pendant la maintenance
await handle.pause('Maintenance planifiée du 15 au 20 janvier');

// Déclencher manuellement (backfill ou test)
await handle.trigger(ScheduleOverlapPolicy.ALLOW_ALL);

// Rattraper les exécutions manquées sur une période
await handle.backfill([
  {
    start: new Date('2024-01-01T08:00:00Z'),
    end: new Date('2024-01-22T08:00:00Z'),
    overlap: ScheduleOverlapPolicy.BUFFER_ONE,
  },
]);

// Reprendre après pause
await handle.unpause('Maintenance terminée');
```

---

## Versioning de Workflows — Déploiements sans Interruption

### getVersion() pour les mises à jour incrémentales

```typescript
import { patched, deprecatePatch } from '@temporalio/workflow';

export async function workflowCommande(commandeId: string): Promise<void> {
  // Stratégie de versioning avec patched() (anciennement getVersion())
  // Les workflows déjà en cours utilisent l'ancien chemin
  // Les nouveaux workflows utilisent le nouveau chemin

  // Étape 1 — Ajouter la nouvelle logique avec patch
  if (patched('ajout-vérification-fraude')) {
    // Nouveau code — appliqué aux workflows démarrés après ce déploiement
    const résultatFraude = await vérifierFraude(commandeId);
    if (résultatFraude.suspect) {
      await marquerSuspect(commandeId);
      return;
    }
  }
  // Ancien code — exécuté par les workflows démarrés avant le patch

  await traiterCommande(commandeId);

  // Étape 2 — Nouveau comportement pour la livraison
  if (patched('livraison-express-disponible')) {
    const méthode = await choisirMéthodeExpédition(commandeId);
    await expédier(commandeId, méthode);
  } else {
    // Ancien comportement simple
    await expédier(commandeId, 'standard');
  }

  await notifierClient(commandeId);
}

// Étape 3 — Après que TOUS les anciens workflows sont terminés :
// Supprimer les branches obsolètes et appeler deprecatePatch()
export async function workflowCommandeV2(commandeId: string): Promise<void> {
  deprecatePatch('ajout-vérification-fraude');
  deprecatePatch('livraison-express-disponible');

  // Code propre sans branches de versioning
  const résultatFraude = await vérifierFraude(commandeId);
  if (résultatFraude.suspect) {
    await marquerSuspect(commandeId);
    return;
  }

  await traiterCommande(commandeId);
  const méthode = await choisirMéthodeExpédition(commandeId);
  await expédier(commandeId, méthode);
  await notifierClient(commandeId);
}
```

### Checklist de déploiement sans downtime

```
Déploiement d'une nouvelle version de workflow :

Phase 1 — Ajouter le patch (deploy)
  ✓ Entourer le nouveau code avec patched('nom-descriptif')
  ✓ Déployer les nouveaux workers (les anciens continuent)
  ✓ Vérifier dans Temporal UI que les nouveaux workflows utilisent le patch

Phase 2 — Attendre la fin des anciens workflows
  ✓ Monitorer temporal_open_workflow_executions en baisse
  ✓ Confirmer dans Temporal UI que 0 workflow actif utilise l'ancien chemin

Phase 3 — Nettoyer le code
  ✓ Remplacer patched() par deprecatePatch()
  ✓ Supprimer les branches obsolètes
  ✓ Déployer la version propre
```

---

## Saga Pattern avec Compensation — Rollback Orchestré

### Commande e-commerce avec 3 activités et compensation complète

```typescript
// workflows/paiement-fractionné.workflow.ts
import { proxyActivities, ActivityFailure, ApplicationFailure } from '@temporalio/workflow';

const actvités = proxyActivities<typeof activitésPaiement>({
  startToCloseTimeout: '30s',
  retry: { maximumAttempts: 3, backoffCoefficient: 2, initialInterval: '1s' },
});

interface RésultatPaiement {
  chargeId: string;
  transfertVendeurId: string | null;
  factureAssuranceId: string | null;
}

export async function workflowPaiementFractionné(
  params: { commandeId: string; montantClient: number; montantVendeur: number; montantAssurance: number }
): Promise<RésultatPaiement> {
  const { commandeId, montantClient, montantVendeur, montantAssurance } = params;

  let chargeId: string | null = null;
  let transfertVendeurId: string | null = null;
  let factureAssuranceId: string | null = null;

  try {
    // Étape 1 — Charger le client
    chargeId = await actvités.chargerClient({
      commandeId,
      montant: montantClient,
      idempotencyKey: `charge-${commandeId}`,
    });

    // Étape 2 — Payer le vendeur
    transfertVendeurId = await actvités.payerVendeur({
      commandeId,
      montant: montantVendeur,
      idempotencyKey: `vendeur-${commandeId}`,
    });

    // Étape 3 — Facturer l'assurance
    factureAssuranceId = await actvités.facturerAssurance({
      commandeId,
      montant: montantAssurance,
      idempotencyKey: `assurance-${commandeId}`,
    });

    return { chargeId, transfertVendeurId, factureAssuranceId };

  } catch (erreur) {
    // Compensation ordonnée — défaire dans l'ordre inverse
    const erreursCompensation: Error[] = [];

    if (factureAssuranceId) {
      try {
        await actvités.rembourserAssurance({
          factureId: factureAssuranceId,
          raison: `Compensation saga — commande ${commandeId}`,
        });
      } catch (e) {
        erreursCompensation.push(e as Error);
      }
    }

    if (transfertVendeurId) {
      try {
        await actvités.rembourserVendeur({
          transfertId: transfertVendeurId,
          raison: `Compensation saga — commande ${commandeId}`,
        });
      } catch (e) {
        erreursCompensation.push(e as Error);
      }
    }

    if (chargeId) {
      try {
        await actvités.rembourserClient({
          chargeId,
          raison: `Compensation saga — commande ${commandeId}`,
        });
      } catch (e) {
        erreursCompensation.push(e as Error);
      }
    }

    // Si des compensations ont échoué, signaler pour intervention manuelle
    if (erreursCompensation.length > 0) {
      await actvités.alerterOpérations({
        commandeId,
        erreursCompensation: erreursCompensation.map((e) => e.message),
        contexteSaga: { chargeId, transfertVendeurId, factureAssuranceId },
      });
    }

    // Re-lever l'erreur originale avec contexte
    throw ApplicationFailure.nonRetryable(
      `Saga échouée pour la commande ${commandeId} — compensations effectuées`,
      'SagaÉchouée',
      { erreurOriginale: String(erreur), erreursCompensation: erreursCompensation.length },
    );
  }
}
```

---

## Child Workflows — Fan-out et Isolation de Domaine

### executeChild et startChild

```typescript
import { executeChild, startChild, ParentClosePolicy } from '@temporalio/workflow';

export async function workflowTraitementBulk(commandeIds: string[]): Promise<void> {
  // Fan-out : lancer des traitements en parallèle
  const promesses = commandeIds.map((commandeId) =>
    executeChild(workflowCommande, {
      workflowId: `commande-${commandeId}`,
      taskQueue: 'commandes-worker',
      args: [commandeId],
      // Timeout par enfant
      workflowExecutionTimeout: '1h',
    }),
  );

  // Attendre TOUS les enfants
  const résultats = await Promise.allSettled(promesses);
  const échecs = résultats.filter((r) => r.status === 'rejected');

  if (échecs.length > 0) {
    await enregistrerÉchecs(échecs.map((e) => (e as PromiseRejectedResult).reason));
  }
}

// startChild (non-bloquant) — utile quand le parent ne doit pas attendre
export async function workflowDéclencheurAsync(payload: Payload): Promise<void> {
  // Démarrer l'enfant sans attendre sa complétion
  const enfantHandle = await startChild(workflowLongDurée, {
    workflowId: `long-${payload.id}`,
    taskQueue: 'traitement-lourd-worker',
    args: [payload],
    // ABANDON : si le parent se ferme, l'enfant continue indépendamment
    parentClosePolicy: ParentClosePolicy.ABANDON,
  });

  // Le parent peut retourner immédiatement
  console.log(`Workflow enfant démarré : ${enfantHandle.workflowId}`);
}
```

---

## Temporal Cloud vs Self-Hosted — Comparaison

### Tableau de décision

```
Critère                  Temporal Cloud              Self-Hosted
─────────────────────────────────────────────────────────────────────
Configuration initiale   < 30 min                    2 à 5 jours
Maintenance              Zéro (géré par Temporal)    Équipe SRE dédiée
Coût (< 1M actions/mois) ~150–300 $/mois             Infra + ingénierie
Coût (> 10M actions/mois)Comparer avec self-hosted    Potentiellement moins cher
SLA garanti              99.99% (SLA contractuel)    Dépend de votre infra
Conformité (RGPD, SOC2)  SOC2 Type II, GDPR ready   Contrôle total des données
Namespace isolation      Par compte, multi-région    Par déploiement
Temporal UI              Inclus, version Cloud        À déployer séparément
Monitoring               Métriques Prometheus incluses Prometheus + Grafana à configurer
Multi-région             Oui (US, EU, AP)             À architecturer manuellement

Recommandation :
- Startup / MVP / < 3 SREs → Temporal Cloud (focus produit)
- Grande entreprise / exigences data souveraineté → Self-hosted avec Helm chart
- Secteur financier/santé → Self-hosted avec Cassandra sur cloud privé
```

### Configuration Temporal Cloud

```typescript
// Connexion à Temporal Cloud — utiliser mTLS ou API keys
const connexion = await NativeConnection.connect({
  address: `${process.env.TEMPORAL_CLOUD_NAMESPACE}.tmprl.cloud:7233`,
  tls: {
    clientCertPair: {
      crt: Buffer.from(process.env.TEMPORAL_CLOUD_CERT!, 'base64'),
      key: Buffer.from(process.env.TEMPORAL_CLOUD_KEY!, 'base64'),
    },
  },
});

const client = new Client({
  connexion,
  namespace: process.env.TEMPORAL_CLOUD_NAMESPACE!, // format: nom.ACCOUNT_ID
});
```

### Monitoring Temporal UI

```
Dashboards essentiels à configurer :

1. Vue Workflows
   - Filtrer par status: open | closed | failed
   - Recherche par workflowId, runId, workflowType
   - Historique complet d'un workflow (chaque event avec timestamp)

2. Métriques clés à alerter
   - temporal_workflow_failed_total       → Workflows échoués
   - temporal_activity_failed_total       → Activities échouées
   - temporal_worker_task_slots_available → Saturation workers (< 10 = alerte)
   - temporal_schedule_miss_latency       → Schedules manquées

3. Temporal UI — accès rapide
   - Workflow detail → voir le stack trace d'une erreur
   - Event history  → rejouer mentalement l'exécution
   - Pending activities → identifier les activités bloquées
   - Signal history → voir tous les signaux reçus et quand
```

---

## Références Complémentaires

- Documentation officielle Temporal TypeScript SDK : https://docs.temporal.io/dev-guide/typescript
- Temporal Cloud : https://cloud.temporal.io
- Temporal Schedules : https://docs.temporal.io/workflows#schedule
- Saga pattern avec Temporal : https://docs.temporal.io/workflows#saga
- Monitoring avec Prometheus : https://docs.temporal.io/self-hosted-guide/prometheus-grafana-setup
