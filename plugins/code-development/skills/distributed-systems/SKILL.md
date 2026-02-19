---
name: distributed-systems
version: 1.0.0
description: >
  Distributed systems patterns, event sourcing, CQRS command query responsibility segregation,
  saga pattern choreography orchestration, outbox pattern transactional messaging,
  domain events, eventual consistency, message queues Kafka RabbitMQ,
  idempotency distributed locking, CAP theorem, two-phase commit,
  circuit breaker retry bulkhead, compensating transactions, event store
---

# Distributed Systems — Patterns de Systèmes Distribués

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu décomposes un monolithe en micro-services et dois coordonner des transactions distribuées
- Tu dois garantir la cohérence des données sans transactions ACID cross-services
- Tu utilises une architecture event-driven (Kafka, RabbitMQ) et dois gérer les échecs
- Tu veux découpler les services avec l'outbox pattern pour éviter la double écriture
- Tu modélises un domaine complexe avec event sourcing (historique d'audit complet)
- Tu as des problèmes de disponibilité et dois appliquer des patterns de résilience

---

## Théorème CAP — Compromis Fondamentaux

```
        Cohérence
           /\
          /  \
         /    \
        /  CA  \
       / (RDBMS)\
      /          \
     /____________\
    Disponibilité  Tolérance réseau
    (MongoDB,       (ZooKeeper,
     Cassandra)      HBase)
```

**Règle** : en cas de partition réseau, choisir entre cohérence (CP) ou disponibilité (AP).

| Système | Choix | Conséquence |
|---|---|---|
| PostgreSQL/MySQL | CA | Pas tolérant aux partitions (monolithe OK) |
| MongoDB (par défaut) | AP | Données potentiellement temporairement obsolètes |
| Redis Cluster | AP | Peut perdre des écritures récentes en cas de fail-over |
| Kafka | CP | Peut refuser les écritures si pas de quorum |

---

## Event Sourcing

Au lieu de stocker l'état actuel, on stocke **tous les événements** qui ont conduit à cet état.

```typescript
// Les événements du domaine (immuables)
type EvenementCompte =
  | { type: 'COMPTE_OUVERT'; payload: { proprietaireId: string; soldInitial: number } }
  | { type: 'DEPOT_EFFECTUE'; payload: { montant: number; reference: string } }
  | { type: 'RETRAIT_EFFECTUE'; payload: { montant: number; reference: string } }
  | { type: 'COMPTE_FERME'; payload: { raison: string } };

// L'agrégat est reconstruit depuis les événements
interface CompteAggregate {
  id: string;
  proprietaireId: string;
  solde: number;
  actif: boolean;
  version: number;  // Pour l'optimistic locking
}

function rejouerEvenements(events: EvenementCompte[]): CompteAggregate {
  return events.reduce((state, event) => {
    switch (event.type) {
      case 'COMPTE_OUVERT':
        return { ...state, proprietaireId: event.payload.proprietaireId, solde: event.payload.soldInitial, actif: true };
      case 'DEPOT_EFFECTUE':
        return { ...state, solde: state.solde + event.payload.montant };
      case 'RETRAIT_EFFECTUE':
        return { ...state, solde: state.solde - event.payload.montant };
      case 'COMPTE_FERME':
        return { ...state, actif: false };
      default:
        return state;
    }
  }, { id: '', proprietaireId: '', solde: 0, actif: false, version: 0 });
}

// Stockage dans un event store (PostgreSQL)
async function appendEvents(
  aggregateId: string,
  events: EvenementCompte[],
  expectedVersion: number,
  db: Database,
): Promise<void> {
  await db.transaction(async (trx) => {
    // Optimistic locking : vérifier la version
    const dernierVersion = await trx
      .select('version')
      .from('events')
      .where('aggregate_id', aggregateId)
      .orderBy('version', 'desc')
      .first();

    if ((dernierVersion?.version ?? -1) !== expectedVersion) {
      throw new Error(`Conflit de version : attendu ${expectedVersion}`);
    }

    await trx('events').insert(
      events.map((event, i) => ({
        aggregate_id: aggregateId,
        type: event.type,
        payload: JSON.stringify(event.payload),
        version: expectedVersion + i + 1,
        created_at: new Date(),
      })),
    );
  });
}
```

---

## CQRS — Command Query Responsibility Segregation

```typescript
// Côté COMMAND : écriture via l'agrégat (event sourcing)
interface CommandHandler<C, R> {
  handle(command: C): Promise<R>;
}

class EffectuerRetraitHandler implements CommandHandler<EffectuerRetrait, void> {
  constructor(
    private readonly evenementStore: EvenementStore,
    private readonly eventBus: EventBus,
  ) {}

  async handle({ compteId, montant, reference }: EffectuerRetrait): Promise<void> {
    // Charger l'agrégat
    const events = await this.evenementStore.charger(compteId);
    const compte = rejouerEvenements(events);

    // Règles métier
    if (!compte.actif) throw new Error('Compte fermé');
    if (compte.solde < montant) throw new Error('Solde insuffisant');

    // Créer et persister le nouvel événement
    const newEvent: EvenementCompte = {
      type: 'RETRAIT_EFFECTUE',
      payload: { montant, reference },
    };

    await this.evenementStore.append(compteId, [newEvent], compte.version);

    // Publier pour les projections QUERY
    await this.eventBus.publish(compteId, newEvent);
  }
}

// Côté QUERY : lectures optimisées (projection dénormalisée)
// La projection est mise à jour via les événements
class ProjectionCompteLecture {
  async handleEvenement(aggregateId: string, event: EvenementCompte): Promise<void> {
    switch (event.type) {
      case 'DEPOT_EFFECTUE':
      case 'RETRAIT_EFFECTUE':
        await db('comptes_lecture').where('id', aggregateId).update({
          solde: db.raw('solde + ?', [
            event.type === 'DEPOT_EFFECTUE' ? event.payload.montant : -event.payload.montant,
          ]),
          derniere_transaction: new Date(),
        });
        break;
    }
  }
}
```

---

## Saga Pattern — Transactions Distribuées

La saga coordonne une transaction qui touche plusieurs services, avec des transactions compensatoires en cas d'échec.

### Orchestration (centralisée)

```typescript
enum EtatSagaCommande {
  DEMARREE = 'DEMARREE',
  PAIEMENT_EN_COURS = 'PAIEMENT_EN_COURS',
  STOCK_RESERVE = 'STOCK_RESERVE',
  COMPLETEE = 'COMPLETEE',
  COMPENSATION_EN_COURS = 'COMPENSATION_EN_COURS',
  ANNULEE = 'ANNULEE',
}

class SagaCreerCommande {
  constructor(
    private readonly paiementService: PaiementService,
    private readonly stockService: StockService,
    private readonly livraisonService: LivraisonService,
    private readonly db: Database,
  ) {}

  async executer(commande: NouvelleCommande): Promise<void> {
    const sagaId = crypto.randomUUID();
    let paiementId: string | null = null;
    let reservationId: string | null = null;

    try {
      // Étape 1 : Paiement
      await this.mettreÀJourEtat(sagaId, EtatSagaCommande.PAIEMENT_EN_COURS);
      paiementId = await this.paiementService.débiter(commande.clientId, commande.total);

      // Étape 2 : Réservation stock
      await this.mettreÀJourEtat(sagaId, EtatSagaCommande.STOCK_RESERVE);
      reservationId = await this.stockService.réserver(commande.articles);

      // Étape 3 : Livraison
      await this.livraisonService.planifier(commande.adresse, reservationId);

      await this.mettreÀJourEtat(sagaId, EtatSagaCommande.COMPLETEE);

    } catch (erreur) {
      await this.mettreÀJourEtat(sagaId, EtatSagaCommande.COMPENSATION_EN_COURS);

      // Compensation dans l'ordre inverse
      if (reservationId) {
        await this.stockService.libérer(reservationId).catch(e =>
          console.error('Échec libération stock', e),
        );
      }
      if (paiementId) {
        await this.paiementService.rembourser(paiementId).catch(e =>
          console.error('Échec remboursement', e),
        );
      }

      await this.mettreÀJourEtat(sagaId, EtatSagaCommande.ANNULEE);
      throw erreur;
    }
  }

  private async mettreÀJourEtat(sagaId: string, état: EtatSagaCommande): Promise<void> {
    await this.db('sagas').upsert({ id: sagaId, état, mis_à_jour_a: new Date() });
  }
}
```

---

## Outbox Pattern — Garantie de Publication

Évite la double écriture (DB + message broker) en utilisant une table outbox dans la même transaction.

```typescript
// La table outbox est dans la même DB que les données métier
await db.transaction(async (trx) => {
  // 1. Mise à jour métier
  const commande = await trx('commandes').insert({
    client_id: clientId,
    total: montant,
    statut: 'CREE',
  }).returning('*');

  // 2. Écriture dans l'outbox (même transaction = atomique)
  await trx('outbox').insert({
    id: crypto.randomUUID(),
    aggregate_id: commande[0].id,
    event_type: 'COMMANDE_CREEE',
    payload: JSON.stringify({ commandeId: commande[0].id, clientId, montant }),
    created_at: new Date(),
    published: false,
  });
  // Si la transaction échoue, les deux annulations sont atomiques
});

// Worker de publication (polling ou CDC avec Debezium)
async function publishOutboxEvents(): Promise<void> {
  const events = await db('outbox')
    .where('published', false)
    .orderBy('created_at', 'asc')
    .limit(100);

  for (const event of events) {
    try {
      await kafkaProducer.send({
        topic: event.event_type.toLowerCase(),
        messages: [{ key: event.aggregate_id, value: event.payload }],
      });

      await db('outbox').where('id', event.id).update({ published: true });
    } catch (error) {
      console.error(`Échec publication event ${event.id}:`, error);
      // Réessayer au prochain tour
    }
  }
}
```

---

## Idempotency Keys — Prévenir les Doublons

```typescript
// Middleware d'idempotence pour les APIs REST
async function idempotencyMiddleware(req: Request, res: Response, next: NextFunction) {
  const idempotencyKey = req.headers['idempotency-key'] as string;
  if (!idempotencyKey) return next();

  // Vérifier si la requête a déjà été traitée
  const cached = await redis.get(`idempotency:${idempotencyKey}`);
  if (cached) {
    const { status, body } = JSON.parse(cached);
    return res.status(status).json(body);
  }

  // Intercepter la réponse pour la mettre en cache
  const originalJson = res.json.bind(res);
  res.json = (body) => {
    redis.set(
      `idempotency:${idempotencyKey}`,
      JSON.stringify({ status: res.statusCode, body }),
      { EX: 86400 },  // 24h
    );
    return originalJson(body);
  };

  next();
}
```

---

## Circuit Breaker

```typescript
enum EtatCircuit { FERME, OUVERT, SEMI_OUVERT }

class CircuitBreaker<T> {
  private état = EtatCircuit.FERME;
  private échecs = 0;
  private dernierÉchec: number | null = null;

  constructor(
    private readonly fn: () => Promise<T>,
    private readonly seuil = 5,
    private readonly timeout = 60_000,
  ) {}

  async exécuter(): Promise<T> {
    if (this.état === EtatCircuit.OUVERT) {
      if (Date.now() - (this.dernierÉchec ?? 0) > this.timeout) {
        this.état = EtatCircuit.SEMI_OUVERT;
      } else {
        throw new Error('Circuit ouvert — service indisponible');
      }
    }

    try {
      const résultat = await this.fn();
      this.onSuccès();
      return résultat;
    } catch (error) {
      this.onÉchec();
      throw error;
    }
  }

  private onSuccès(): void {
    this.échecs = 0;
    this.état = EtatCircuit.FERME;
  }

  private onÉchec(): void {
    this.échecs++;
    this.dernierÉchec = Date.now();
    if (this.échecs >= this.seuil) {
      this.état = EtatCircuit.OUVERT;
    }
  }
}
```

---

## Références

- `references/event-sourcing.md` — Event store, projections, snapshots, replaying events, EventStoreDB
- `references/messaging-patterns.md` — Kafka topologie, RabbitMQ exchanges, choreography, outbox avec Debezium
- `references/resilience-patterns.md` — Circuit breaker, retry exponentiel, bulkhead, timeout, rate limiting distribué
- `references/case-studies.md` — 4 cas : monolithe→micro-services, saga e-commerce, outbox pattern, event sourcing caisse
