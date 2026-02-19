---
name: streaming-realtime
version: 1.0.0
description: >
  Use this skill when the user asks about "streaming data", "real-time analytics", "Kafka", "Apache Flink", "Spark Streaming", "event streaming", "event-driven architecture", "CDC change data capture", "event sourcing", "CQRS", "message queue", "pub-sub", "Kinesis", "Pub/Sub Google", "real-time dashboard", "stream processing", "watermarks", "windowing", "exactly-once semantics", discusses processing data in real-time, building event-driven systems, or needs guidance on streaming infrastructure and real-time data pipelines.
---

# Streaming & Real-Time Analytics

## Vue d'Ensemble

La distinction fondamentale en architecture data : le traitement batch traite des donnees historiques accumulees (toutes les heures, toutes les nuits) ; le streaming traite chaque evenement au fur et a mesure qu'il se produit. Le choix entre les deux determine fondamentalement la latence de votre analytique et la complexite de votre systeme.

En 2025-2026, le modele "Lambda Architecture" (batch + streaming separes) est de plus en plus remplace par une architecture streaming-first qui peut aussi produire des resultats batch — simplification majeure de la stack.

---

## Batch vs Streaming — Quand Choisir

### Criteres de Decision

| Critere | Batch | Streaming |
|---|---|---|
| **Latence acceptable** | > 1 heure | < 1 minute |
| **Complexite technique** | Faible | Haute |
| **Cout infrastructure** | Faible | Moyen a eleve |
| **Maturite equipe** | Faible requise | Elevee requise |
| **Use cases** | Reporting, ML training | Alertes, fraude, monitoring |

### Use Cases Streaming (Ou Le Batch Ne Suffit Pas)

- **Detection de fraude** : identifier une transaction frauduleuse en < 200ms, avant autorisation
- **Alertes operationnelles** : serveur en surcharge detecte en 30 secondes, pas 1 heure
- **Personnalisation temps reel** : recommandations basees sur la navigation actuelle
- **Monitoring IoT** : capteurs industriels qui necessitent une reponse immediate
- **Trading financier** : execution a la milliseconde
- **Customer journey** : savoir qu'un client est bloque dans le funnel MAINTENANT

---

## Apache Kafka — Fondamentaux

### Architecture

**Topics** : categories de messages. Analogie : un topic = un canal Slack.

**Partitions** : un topic est divise en partitions pour la scalabilite et le parallelisme. Plus de partitions = plus de consommateurs en parallele.

**Producers** : applications qui ecrivent des messages dans Kafka.

**Consumers** : applications qui lisent des messages depuis Kafka.

**Consumer Groups** : plusieurs consommateurs partageant le travail. Chaque partition est assignee a un seul consommateur par groupe.

**Brokers** : serveurs Kafka. Cluster de 3+ brokers pour la haute disponibilite.

**Retention** : les messages sont conserves pendant une duree configuree (7 jours par defaut). Kafka n'est pas seulement une queue — c'est un log distribue.

### Configuration Kafka Optimale

```yaml
# Producer config
acks: all                    # Attendre confirmation de tous les replicas
retries: 3                   # Retries en cas d'echec
batch.size: 16384            # Batch de 16KB pour l'efficacite
linger.ms: 5                 # Attendre 5ms pour batcher plus de messages
compression.type: snappy     # Compression pour reduire le reseau

# Consumer config
auto.offset.reset: earliest  # Lire depuis le debut si pas d'offset
enable.auto.commit: false    # Commit manuel pour contrôle exact
max.poll.records: 500        # Nombre max de messages par poll
```

### Producer Python

```python
from confluent_kafka import Producer
import json
from datetime import datetime

producer = Producer({
    'bootstrap.servers': 'kafka:9092',
    'acks': 'all',
    'retries': 3,
    'compression.type': 'snappy',
})

def produce_event(topic: str, event: dict, key: str = None):
    """Produire un evenement dans Kafka avec gestion d'erreur."""
    message = {
        'timestamp': datetime.utcnow().isoformat(),
        'data': event,
    }

    producer.produce(
        topic=topic,
        key=key.encode('utf-8') if key else None,
        value=json.dumps(message).encode('utf-8'),
        callback=delivery_callback,
    )
    producer.poll(0)  # Declencher les callbacks

def delivery_callback(err, msg):
    if err:
        print(f'Erreur de livraison: {err}')
    else:
        print(f'Message livre: {msg.topic()} partition {msg.partition()} offset {msg.offset()}')

# Exemple d'usage
produce_event(
    topic='order-events',
    event={'order_id': '12345', 'status': 'placed', 'amount': 89.99},
    key='user-456',
)
producer.flush()  # S'assurer que tous les messages sont envoyes
```

### Consumer Python

```python
from confluent_kafka import Consumer, KafkaError
import json

consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'order-processor-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,  # Commit manuel
    'max.poll.interval.ms': 300000,  # 5 min max entre polls
})

consumer.subscribe(['order-events'])

def process_batch(messages):
    """Traiter un batch de messages."""
    for msg in messages:
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue  # Fin de partition normale
            raise Exception(f'Erreur Kafka: {msg.error()}')

        event = json.loads(msg.value().decode('utf-8'))
        # Logique de traitement
        handle_order_event(event['data'])

try:
    while True:
        messages = consumer.consume(num_messages=100, timeout=1.0)
        if messages:
            process_batch(messages)
            consumer.commit()  # Commit seulement apres traitement reussi
finally:
    consumer.close()
```

---

## Stream Processing

### Apache Flink — Le Standard Enterprise

Flink est le moteur de stream processing le plus avance pour la production. Support de l'exactly-once semantics, gestion des late data, windowing avance.

**Concepts cles** :

**DataStream API** :
```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Source Kafka
KafkaSource<String> source = KafkaSource.<String>builder()
    .setBootstrapServers("kafka:9092")
    .setTopics("order-events")
    .setGroupId("flink-processor")
    .setValueOnlyDeserializer(new SimpleStringSchema())
    .build();

DataStream<String> stream = env.fromSource(source, WatermarkStrategy.noWatermarks(), "Kafka Source");

// Transformation
DataStream<OrderMetrics> metrics = stream
    .map(json -> parseOrder(json))
    .keyBy(order -> order.getUserId())
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new OrderAggregator());

// Sink
metrics.sinkTo(KafkaSink.<OrderMetrics>builder()
    .setBootstrapServers("kafka:9092")
    .setRecordSerializer(new OrderMetricsSerializer("order-metrics"))
    .build());

env.execute("Order Stream Processor");
```

**Windowing** :

| Type | Description | Usage |
|---|---|---|
| **Tumbling Window** | Fenetres fixes non-chevauchantes (5 min, 1h) | Agregations periodiques |
| **Sliding Window** | Fenetres se chevauchant (5 min toutes les 1 min) | Moving averages |
| **Session Window** | Fenetre basee sur l'inactivite utilisateur | User sessions analytics |
| **Global Window** | Tous les elements ensemble | Custom triggers |

### ksqlDB — SQL sur Kafka

Pour les equipes moins a l'aise avec Java/Scala, ksqlDB permet d'ecrire du SQL directement sur les streams Kafka.

```sql
-- Creer un stream depuis un topic Kafka
CREATE STREAM orders_stream (
    order_id VARCHAR,
    user_id VARCHAR,
    amount DOUBLE,
    status VARCHAR,
    created_at TIMESTAMP
) WITH (
    KAFKA_TOPIC = 'order-events',
    VALUE_FORMAT = 'JSON',
    TIMESTAMP = 'created_at'
);

-- Agregation en temps reel : CA par heure
CREATE TABLE hourly_revenue AS
SELECT
    TIMESTAMPTOSTRING(WINDOWSTART, 'yyyy-MM-dd HH:00') as hour,
    SUM(amount) as total_revenue,
    COUNT(*) as order_count
FROM orders_stream
WINDOW TUMBLING (SIZE 1 HOUR)
GROUP BY TIMESTAMPTOSTRING(WINDOWSTART, 'yyyy-MM-dd HH:00')
EMIT CHANGES;

-- Detection d'anomalies : commandes > 1000 EUR
CREATE STREAM high_value_orders AS
SELECT *
FROM orders_stream
WHERE amount > 1000
EMIT CHANGES;
```

---

## Patterns Architecture

### Event Sourcing

Au lieu de stocker l'etat courant (la commande EST "livree"), stocker tous les evenements qui ont amene a cet etat (commandPassee → paiementValide → expedieEntrepot → livree).

**Avantages** :
- Audit trail complet impossible a falsifier
- Rejouer les evenements pour reconstruire n'importe quel etat passe
- Base naturelle pour le CQRS

**Exemple** :
```
Topic: order-events
  { type: "ORDER_PLACED", orderId: "123", amount: 89.99, ts: "10:00" }
  { type: "PAYMENT_VALIDATED", orderId: "123", paymentId: "pay_xxx", ts: "10:01" }
  { type: "SHIPPED", orderId: "123", carrier: "Chronopost", ts: "10:05" }
  { type: "DELIVERED", orderId: "123", ts: "10:30" }
```

### CQRS (Command Query Responsibility Segregation)

Separer les operations d'ecriture (commands) et de lecture (queries) sur des modeles de donnees differents.

**Write side** : evenements Kafka → append-only log.
**Read side** : materialized views optimisees pour chaque use case de lecture.

### Change Data Capture (CDC)

Capturer les changements dans une base de donnees relationnelle et les publier comme evenements Kafka.

**Debezium** : outil CDC le plus utilise. Lit le WAL (Write-Ahead Log) de PostgreSQL/MySQL.

```yaml
# connector-config.json pour Debezium + PostgreSQL
{
  "name": "postgres-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "secret",
    "database.dbname": "orders_db",
    "table.include.list": "public.orders,public.customers",
    "plugin.name": "pgoutput",
    "topic.prefix": "cdc"
  }
}
```

Chaque `INSERT`, `UPDATE`, `DELETE` dans PostgreSQL devient un evenement dans le topic `cdc.public.orders`.

---

## Real-Time Dashboards

### Architecture Complete

```
Sources (apps, APIs, IoT)
        ↓
Kafka (transport)
        ↓
Flink / ksqlDB (processing)
        ↓
   ┌────┴────┐
   ↓         ↓
Redis     Materialize / ClickHouse
(cache)   (OLAP temps reel)
   ↓         ↓
WebSocket  REST API
        ↓
Dashboard (Grafana, Metabase, custom)
```

### Materialize — OLAP Streaming

Base de donnees qui maintient des vues SQL a jour en temps reel au fur et a mesure que les donnees arrivent depuis Kafka.

```sql
-- Connexion Kafka
CREATE SOURCE orders_source
FROM KAFKA CONNECTION kafka_connection
TOPIC 'order-events'
FORMAT JSON;

-- Vue materialisee maintenue en temps reel
CREATE MATERIALIZED VIEW live_revenue AS
SELECT
    date_trunc('minute', created_at) as minute,
    SUM(amount) as revenue,
    COUNT(*) as orders
FROM orders_source
GROUP BY date_trunc('minute', created_at);

-- Query temps reel (resultat toujours a jour)
SELECT * FROM live_revenue ORDER BY minute DESC LIMIT 10;
```

---

## Maturity Model — Streaming Data

| Niveau | Caracteristique |
|---|---|
| **1 — Batch uniquement** | Jobs quotidiens/horaires, latence > 1h |
| **2 — Micro-batch** | Spark Structured Streaming, Airflow toutes les 5-15 min |
| **3 — Kafka basique** | Transport d'evenements, consumers simples, pas de processing avance |
| **4 — Stream Processing** | Flink ou ksqlDB, windowing, detection d'anomalies, CDC |
| **5 — Streaming-First** | Event sourcing, CQRS, real-time ML inference, zero-latency analytics |
