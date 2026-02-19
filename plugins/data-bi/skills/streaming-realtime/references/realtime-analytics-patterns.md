# Patterns d'Architecture Real-Time Analytics

## Vue d'Ensemble

Les patterns d'architecture definissent comment organiser les composants d'un systeme de streaming pour atteindre les objectifs business. Ce document couvre les patterns fondamentaux (Lambda, Kappa), les patterns de donnees (Event Sourcing, CQRS, CDC), et les architectures de real-time analytics (OLAP en streaming, materialized views).

---

## Architectures Fondamentales

### Lambda Architecture

**Principe** : deux chemins paralleles — batch (haute precision, haute latence) et streaming (faible precision, faible latence) — combines dans une couche de service.

```
Sources → Kafka ─┬→ Batch Layer (Spark/Hive) → Batch Views
                 └→ Speed Layer (Flink/Storm) → Realtime Views
                                                     ↓
                                              Serving Layer → Query
```

**Avantages** : separation claire des preoccupations, tolerance aux pannes du streaming, precisión du batch.

**Inconvenients** :
- Double complexity : maintenir deux systemes differents pour la meme logique metier
- Code duplique : la meme transformation en deux langages/frameworks
- Reconciliation complexe : merger les resultats batch et streaming

**Usage actuel** : de moins en moins recommande. Principalement pour les systemes legacy et les cas ou le batch est indispensable pour les corrections historiques.

### Kappa Architecture

**Principe** : un seul systeme de streaming. Le batch est remplace par du streaming sur des donnees historiques (rejouer Kafka depuis le debut).

```
Sources → Kafka → Flink/Spark Streaming → Serving Layer → Query
              ↑
         (Retention longue : 30-90 jours)
         Permet de "rejouer" pour corriger des bugs
```

**Avantages** :
- Simplicite : une seule logique de transformation
- Correctness : pas de reconciliation batch/streaming
- Flexibilite : rejouer depuis n'importe quel point en cas de bug

**Inconvenients** :
- Rejouer est lent pour les tres longues periodes (solution : snapshots periodiques dans S3)
- La retention Kafka peut etre couteuse pour plusieurs mois de donnees

**Usage recommande** : le standard pour les nouvelles architectures. Completer avec des snapshots S3 si le rejouer de > 7 jours est necessaire.

### Streaming-First avec Data Lakehouse

**Principe** : Delta Lake / Iceberg / Hudi permettent des tables ACID sur S3. Le streaming ecrit directement en ACID, et le batch lit les memes tables. Un seul stockage, deux modes d'acces.

```
Sources → Kafka → Flink (streaming) → Delta Lake (S3)
                                           ↓
                              ┌────────────┴───────────────┐
                              ↓                            ↓
                     Spark SQL (batch)            Presto/Trino (interactive)
                     pour les reports             pour l'exploration
```

---

## Event Sourcing

### Definition et Principes

L'event sourcing stocke le systeme comme une sequence d'evenements immutables plutôt que comme un etat courant.

**Base de donnees traditionnelle** :
```sql
-- L'etat courant : on ne sait pas comment on y est arrive
SELECT * FROM orders WHERE order_id = '123';
-- status = 'DELIVERED', amount = 89.99
```

**Event Sourcing** :
```
Topic: order-events (toute l'histoire)
1. { type: "ORDER_PLACED",    orderId: "123", amount: 89.99, ts: "10:00" }
2. { type: "PAYMENT_RECEIVED", orderId: "123", txId: "tx-456", ts: "10:01" }
3. { type: "STOCK_RESERVED",  orderId: "123", warehouse: "Lyon", ts: "10:02" }
4. { type: "SHIPPED",         orderId: "123", carrier: "DHL", ts: "14:30" }
5. { type: "DELIVERED",       orderId: "123", signature: "J.Dupont", ts: "09:15+1" }
```

**Reconstituer l'etat courant** :
```python
def get_order_state(order_id: str, events: list) -> dict:
    """Rejouer les evenements pour obtenir l'etat courant."""
    state = {}
    for event in sorted(events, key=lambda e: e['timestamp']):
        if event['type'] == 'ORDER_PLACED':
            state = {'id': order_id, 'status': 'PLACED', 'amount': event['amount']}
        elif event['type'] == 'PAYMENT_RECEIVED':
            state['status'] = 'PAID'
            state['payment_id'] = event['txId']
        elif event['type'] == 'SHIPPED':
            state['status'] = 'SHIPPED'
            state['carrier'] = event['carrier']
        elif event['type'] == 'DELIVERED':
            state['status'] = 'DELIVERED'
    return state
```

### Avantages de l'Event Sourcing

**Audit trail complet** : impossible de falsifier l'historique. Requis dans les secteurs reglementes (finance, sante).

**Debug et root cause analysis** : rejouer les evenements pour reproduire un probleme exactement.

**Projections multiples** : le meme stream d'evenements peut alimenter plusieurs "vues" differentes sans re-interroger la source.

**Compensation facile** : pour annuler une action, emmetre un evenement de compensation (pas de DELETE/UPDATE).

### Considerations Pratiques

**Snapshot pattern** : pour eviter de rejouer 1 million d'evenements pour obtenir l'etat d'un objet, creer des snapshots periodiques.

```python
# Snapshot toutes les 100 evenements
def get_order_state_with_snapshot(order_id: str) -> dict:
    # 1. Charger le dernier snapshot
    snapshot = load_snapshot(order_id)  # ex: {state: {...}, event_seq: 950}

    # 2. Rejouer seulement depuis le snapshot
    events_since = get_events_since(order_id, snapshot['event_seq'])

    # 3. Reconstituer l'etat
    return apply_events(snapshot['state'], events_since)
```

---

## CQRS (Command Query Responsibility Segregation)

### Principe

Separer les operations d'ecriture (Commands) et de lecture (Queries) sur des modeles differents.

```
Write Side                          Read Side
─────────                           ─────────
Command Handler                     Query Handler
    ↓                                   ↑
Domain Model                        Read Model (optimisé)
    ↓                                   ↑
Event Store (Kafka)         →→→     Projection Builder
```

### Implementation avec Kafka

```python
# WRITE SIDE — Command Handler
class PlaceOrderCommand:
    def __init__(self, user_id: str, items: list, payment_method: str):
        self.user_id = user_id
        self.items = items
        self.payment_method = payment_method

class OrderCommandHandler:
    def handle(self, command: PlaceOrderCommand):
        # Validation domain
        if not self.validate_stock(command.items):
            raise InsufficientStockError()

        # Emettre l'evenement
        event = {
            'type': 'ORDER_PLACED',
            'order_id': generate_uuid(),
            'user_id': command.user_id,
            'items': command.items,
            'total': self.calculate_total(command.items),
            'timestamp': datetime.now().isoformat()
        }
        kafka_producer.produce('order-events', json.dumps(event))

# READ SIDE — Projection Builder (consomme les events Kafka)
class OrderReadModelBuilder:
    def __init__(self, db: Database):
        self.db = db

    def handle_order_placed(self, event: dict):
        """Construire la vue de lecture depuis l'event."""
        self.db.execute("""
            INSERT INTO orders_read_model
            (order_id, user_id, status, total, created_at, items_count)
            VALUES (?, ?, 'PLACED', ?, ?, ?)
        """, (
            event['order_id'],
            event['user_id'],
            event['total'],
            event['timestamp'],
            len(event['items'])
        ))

    def handle_order_shipped(self, event: dict):
        self.db.execute("""
            UPDATE orders_read_model
            SET status = 'SHIPPED', shipped_at = ?, carrier = ?
            WHERE order_id = ?
        """, (event['timestamp'], event['carrier'], event['order_id']))
```

### Read Models Multiples

Le meme stream d'evenements peut alimenter plusieurs read models optimises pour differents use cases :

```
Kafka: order-events
    ├── Projection A: Orders table (PostgreSQL) — pour le backoffice
    ├── Projection B: Orders Elasticsearch — pour la recherche
    ├── Projection C: Orders OLAP (ClickHouse) — pour l'analytique
    └── Projection D: User order history (Redis cache) — pour l'API
```

---

## Change Data Capture (CDC)

### Debezium — Architecture et Configuration

Debezium lit le Write-Ahead Log (WAL) de PostgreSQL pour capturer chaque INSERT, UPDATE, DELETE et les publier comme evenements Kafka.

**Pourquoi le WAL** : le WAL est ecrit avant chaque operation en base — c'est la source de verite la plus fiable. Debezium est une lecture "non-intrusive" (pas de triggers, pas de polling de la base).

**Configuration PostgreSQL pour Debezium** :
```sql
-- 1. Activer le mode WAL logique
-- (modifier postgresql.conf)
-- wal_level = logical
-- max_wal_senders = 1
-- max_replication_slots = 1

-- 2. Creer un slot de replication
SELECT pg_create_logical_replication_slot('debezium_slot', 'pgoutput');

-- 3. Accorder les permissions a l'utilisateur Debezium
CREATE ROLE debezium WITH REPLICATION LOGIN PASSWORD 'secret';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;
```

**Connector Debezium** :
```json
{
  "name": "postgres-source",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "secret",
    "database.dbname": "production",
    "database.server.name": "prod",
    "table.include.list": "public.orders,public.customers,public.products",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_slot",
    "publication.name": "dbz_publication",
    "snapshot.mode": "initial",
    "decimal.handling.mode": "double",
    "heartbeat.interval.ms": "30000"
  }
}
```

**Format des events Debezium** :
```json
{
  "op": "u",          // c=create, u=update, d=delete, r=read(snapshot)
  "ts_ms": 1704067200000,
  "before": {         // Etat avant (null pour les INSERTs)
    "order_id": "123",
    "status": "PLACED",
    "amount": 89.99
  },
  "after": {          // Etat apres (null pour les DELETEs)
    "order_id": "123",
    "status": "PAID",
    "amount": 89.99
  },
  "source": {
    "db": "production",
    "table": "orders",
    "lsn": 12345678
  }
}
```

### Patterns CDC

**Database Migration sans downtime** :
1. Activer CDC sur l'ancienne base
2. Migrate les donnees historiques (snapshot)
3. Appliquer les deltas CDC pendant la migration
4. Basculer quand les deux bases sont synchrones

**Invalidation de cache** :
```python
# Consommateur CDC qui invalide le cache Redis
def on_order_updated(cdc_event: dict):
    order_id = cdc_event['after']['order_id']
    redis_client.delete(f"order:{order_id}")
    redis_client.delete(f"user_orders:{cdc_event['after']['user_id']}")
```

**Synchronisation Elasticsearch** :
```python
# Indexer dans Elasticsearch depuis CDC sans Logstash
def on_product_changed(cdc_event: dict):
    if cdc_event['op'] == 'd':
        es_client.delete(index='products', id=cdc_event['before']['product_id'])
    else:
        es_client.index(index='products', id=cdc_event['after']['product_id'],
                        document=transform_for_es(cdc_event['after']))
```

---

## Materialize Views en Temps Reel

### Le Pattern

Une materialized view classique (SQL) est calculee periodiquement (REFRESH). Une materialized view "streaming" est maintenue en continu — chaque event entrant met a jour la vue.

### Materialize (Base de Donnees)

```sql
-- Creer une source depuis Kafka
CREATE SOURCE order_source
FROM KAFKA CONNECTION kafka_connection (TOPIC 'order-events')
FORMAT JSON;

-- Vue materialisee : CA par heure
CREATE MATERIALIZED VIEW hourly_revenue AS
SELECT
    date_trunc('hour', to_timestamp((data->>'created_at')::double precision)) as hour,
    SUM((data->>'amount')::double precision) as revenue,
    COUNT(*) as order_count
FROM order_source
GROUP BY date_trunc('hour', to_timestamp((data->>'created_at')::double precision));

-- Query → resultat toujours a jour, calcul incremental
SELECT * FROM hourly_revenue
WHERE hour > now() - INTERVAL '24 hours'
ORDER BY hour DESC;
```

### ClickHouse — OLAP Temps Reel

ClickHouse est une base OLAP column-store capable d'ingerer des millions de lignes par seconde et de repondre a des queries analytiques en millisecondes.

```sql
-- Table ClickHouse avec ingestion depuis Kafka
CREATE TABLE orders_kafka
ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'order-events',
    kafka_group_name = 'clickhouse_consumer',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 3;

-- Table persistante
CREATE TABLE orders (
    order_id String,
    user_id String,
    amount Float64,
    status LowCardinality(String),
    created_at DateTime,
    date Date MATERIALIZED toDate(created_at)
) ENGINE = MergeTree()
PARTITION BY date
ORDER BY (user_id, created_at);

-- Materialized view qui transfère Kafka → Table persistante
CREATE MATERIALIZED VIEW orders_mv TO orders AS
SELECT * FROM orders_kafka;

-- Query analytique en temps reel (millisecondes)
SELECT
    toStartOfHour(created_at) as hour,
    count() as orders,
    sum(amount) as revenue,
    avg(amount) as avg_order
FROM orders
WHERE created_at >= now() - INTERVAL 24 HOUR
GROUP BY hour
ORDER BY hour DESC;
```

---

## Real-Time Dashboard — Architecture Complète

### Stack Reference 2025

```
Data Sources
├── App Events → Kafka (SDK mobile/web)
├── DB Changes → Kafka (Debezium CDC)
└── IoT/API → Kafka (producers directs)

Processing (Flink)
├── Enrichissement (join avec referentiel)
├── Agregation (fenetres 1min, 5min, 1h)
└── Anomalie Detection (seuils + ML)

Storage
├── Redis (top metrics, < 5 min freshness, TTL 24h)
├── ClickHouse (historique OLAP, queries rapides)
└── Delta Lake/S3 (archive, ML training)

Serving
├── WebSocket (push des metrics a < 5 secondes)
├── REST API (queries ad hoc sur ClickHouse)
└── Grafana / Superset (dashboards standard)
```

### Gestion des Pics de Charge

Kafka comme buffer naturel : si le backend de traitement est temporairement sature, les messages s'accumulent dans Kafka (lag augmente). Quand la capacite est restauree, le systeme rattrape son retard sans perte de donnees.

**Scaling horizontal** : augmenter le nombre de partitions Kafka → augmenter les consumers Flink → throughput scale lineairement.
