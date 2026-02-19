# Kafka — Fondamentaux et Configuration

## Vue d'Ensemble

Apache Kafka est un log distribue et un systeme de messagerie. Originellement cree par LinkedIn (2011), il est devenu le standard de l'industrie pour le transport d'evenements en temps reel. Kafka n'est pas qu'une simple queue de messages — c'est un log persistant, repartitionne et replique qui permet de rejouer les evenements.

---

## Architecture Interne

### Le Commit Log

Le concept fondamental de Kafka est le **commit log** : une sequence ordonnee et immuable d'enregistrements. Chaque nouveau message est appende a la fin. Les messages ne sont jamais modifies ni supprimes (avant la retention configuree).

**Consequences** :
- Lecture ultra-rapide (lecture sequentielle sur disque — optimisee par le systeme d'exploitation)
- Rejouer les evenements a partir de n'importe quel point (utile pour le replay, le debugging, la migration)
- Decouplage complet producteur/consommateur

### Topics et Partitions

**Topic** : categorisation logique des messages. Analogue a une table en base de donnees.

**Partition** : sous-division d'un topic pour le parallelisme. Un topic de N partitions peut etre consomme par N consommateurs en parallele.

```
Topic: order-events
├── Partition 0: [msg0, msg3, msg6, msg9...]  → Consumer A
├── Partition 1: [msg1, msg4, msg7, msg10...] → Consumer B
└── Partition 2: [msg2, msg5, msg8, msg11...] → Consumer C
```

**Offset** : position d'un message dans une partition. Unique par partition. Le consommateur track son offset pour savoir ou il en est.

**Ordering** : l'ordre est garanti DANS une partition, pas entre partitions. Pour un ordre global strict : utiliser 1 seule partition (au detriment du parallelisme).

**Partitioning key** : le producteur peut specifier une cle. Tous les messages avec la meme cle vont dans la meme partition → ordre garanti pour un meme user_id ou order_id.

```python
# Meme user → meme partition → ordre garanti
producer.produce(
    topic='order-events',
    key=user_id.encode(),  # La cle determine la partition
    value=event_json,
)
```

### Replication et Haute Disponibilite

**Replication factor** : combien de copies de chaque partition existent dans le cluster.

**Leader** : la partition "principale" sur un broker. Toutes les lectures et ecritures passent par le leader.

**Follower** : replicas passifs. Si le leader tombe, un follower devient le nouveau leader (election automatique).

**Configuration recommandee production** :
```yaml
# Topic config
replication.factor: 3      # 3 copies par partition
min.insync.replicas: 2     # Au moins 2 replicas confirment avant ACK
```

**Impact sur la durabilite** :
- `acks=0` : producteur n'attend pas de confirmation. Ultra-rapide, zero durabilite.
- `acks=1` : leader confirme. Rapide, risque de perte si le leader tombe avant replication.
- `acks=all` : tous les ISR (In-Sync Replicas) confirment. Le plus lent, zero perte possible.

---

## Configuration Avancee

### Producteur

```python
from confluent_kafka import Producer

producer = Producer({
    # Connexion
    'bootstrap.servers': 'broker1:9092,broker2:9092,broker3:9092',

    # Durabilite
    'acks': 'all',                    # Attendre tous les ISR
    'enable.idempotence': True,       # Exactly-once delivery (desactive les duplicats)
    'retries': 2147483647,            # Retries infinis avec idempotence
    'max.in.flight.requests.per.connection': 5,

    # Performance
    'batch.size': 32768,              # 32KB par batch
    'linger.ms': 10,                  # Attendre 10ms pour batcher
    'compression.type': 'lz4',       # Compression LZ4 (rapide)
    'buffer.memory': 33554432,        # 32MB buffer memoire

    # Timeouts
    'delivery.timeout.ms': 120000,    # 2 min max pour delivrer
    'request.timeout.ms': 30000,      # 30s par requete
})
```

### Consommateur

```python
from confluent_kafka import Consumer

consumer = Consumer({
    # Connexion
    'bootstrap.servers': 'broker1:9092,broker2:9092,broker3:9092',
    'group.id': 'my-consumer-group',

    # Offset management
    'auto.offset.reset': 'earliest',  # 'earliest' ou 'latest'
    'enable.auto.commit': False,      # Commit manuel recommande
    'auto.commit.interval.ms': 5000,  # Si auto-commit active

    # Performance
    'max.poll.records': 500,          # Messages par poll()
    'fetch.min.bytes': 1,             # Pas d'attente minimum
    'fetch.max.wait.ms': 500,         # Max 500ms avant retour vide
    'max.partition.fetch.bytes': 1048576,  # 1MB par partition

    # Heartbeat et session
    'session.timeout.ms': 30000,      # 30s sans heartbeat → rebalance
    'heartbeat.interval.ms': 3000,    # Heartbeat toutes les 3s
    'max.poll.interval.ms': 300000,   # 5 min max entre polls
})
```

---

## Schema Registry

Le Schema Registry est un service centralisé qui stocke les schemas (Avro, JSON Schema, Protobuf) des messages Kafka. Il garantit la compatibilite entre producteurs et consommateurs.

### Pourquoi Schema Registry

**Probleme sans schema** : si un producteur change le format d'un message (renomme un champ, change un type), le consommateur casse silencieusement.

**Solution** : le schema est versionne et valide avant chaque message. La compatibilite est verifiee au niveau du registry.

### Implementation avec Avro

```python
from confluent_kafka.avro import AvroProducer
from confluent_kafka.schema_registry import SchemaRegistryClient

# Schema Avro pour un evenement de commande
order_schema = """
{
  "type": "record",
  "name": "Order",
  "namespace": "com.mycompany.orders",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "user_id", "type": "string"},
    {"name": "amount", "type": "double"},
    {"name": "currency", "type": {"type": "enum", "name": "Currency", "symbols": ["EUR", "USD", "GBP"]}},
    {"name": "created_at", "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "items", "type": {"type": "array", "items": {
      "type": "record",
      "name": "OrderItem",
      "fields": [
        {"name": "product_id", "type": "string"},
        {"name": "quantity", "type": "int"},
        {"name": "unit_price", "type": "double"}
      ]
    }}}
  ]
}
"""

schema_registry = SchemaRegistryClient({'url': 'http://schema-registry:8081'})

producer = AvroProducer(
    {
        'bootstrap.servers': 'kafka:9092',
        'schema.registry.url': 'http://schema-registry:8081',
    },
    default_value_schema=schema_registry.get_latest_version('order-events-value').schema
)

# Le message sera valide contre le schema avant envoi
producer.produce(
    topic='order-events',
    value={
        'order_id': 'ord-12345',
        'user_id': 'usr-456',
        'amount': 89.99,
        'currency': 'EUR',
        'created_at': int(datetime.now().timestamp() * 1000),
        'items': [{'product_id': 'prod-789', 'quantity': 2, 'unit_price': 44.995}]
    }
)
```

### Compatibility Modes

| Mode | Description | Usage |
|---|---|---|
| BACKWARD | Le nouveau schema peut lire les anciens messages | Ajouter des champs optionnels |
| FORWARD | L'ancien schema peut lire les nouveaux messages | Supprimer des champs optionnels |
| FULL | Backward + Forward | Changements non-breaking uniquement |
| NONE | Aucune validation | A eviter en production |

---

## Kafka Connect — Integration de Sources et Sinks

Kafka Connect est un framework pour connecter Kafka avec des systemes externes sans code custom.

### Connectors Essentiels

**Sources (inject data into Kafka)** :
- **Debezium PostgreSQL/MySQL** : CDC (change data capture) depuis les bases SQL
- **Debezium MongoDB** : CDC depuis MongoDB
- **S3 Source** : lire des fichiers depuis S3 et les injecter dans Kafka
- **HTTP Source** : polling d'une API REST

**Sinks (export data from Kafka)** :
- **Elasticsearch Sink** : indexer les events dans Elasticsearch pour la recherche
- **S3 Sink** : archiver les events dans S3 (data lake)
- **JDBC Sink** : ecrire dans PostgreSQL/MySQL depuis Kafka
- **Snowflake/BigQuery Sink** : alimenter le data warehouse

### Configuration d'un Connector S3 Sink

```json
{
  "name": "s3-archive-connector",
  "config": {
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "tasks.max": "3",
    "topics": "order-events,payment-events,user-events",
    "s3.region": "eu-west-1",
    "s3.bucket.name": "my-kafka-archive",
    "s3.part.size": "67108864",
    "flush.size": "10000",
    "rotate.interval.ms": "3600000",
    "rotate.schedule.interval.ms": "3600000",
    "storage.class": "io.confluent.connect.s3.storage.S3Storage",
    "format.class": "io.confluent.connect.s3.format.parquet.ParquetFormat",
    "parquet.codec": "snappy",
    "locale": "en_US",
    "timezone": "UTC",
    "timestamp.extractor": "RecordField",
    "timestamp.field": "created_at"
  }
}
```

---

## Monitoring et Observabilite

### Metriques JMX Critiques

**Producer metrics** :
- `record-send-rate` : messages produits par seconde
- `record-error-rate` : taux d'erreur (doit etre = 0)
- `request-latency-avg` : latence moyenne des requetes

**Consumer metrics** :
- `records-consumed-rate` : messages consommes par seconde
- `records-lag-max` : lag maximum (retard du consommateur)
- `commit-latency-avg` : latence des commits d'offset

**Broker metrics** :
- `UnderReplicatedPartitions` : partitions avec moins de replicas que prevu (alerte critique)
- `ActiveControllerCount` : doit etre = 1 dans le cluster
- `RequestsPerSec` : throughput global

### Consumer Lag — Le KPI Central

Le lag consumer = nombre de messages dans la partition - offset du consommateur. Un lag croissant = le consommateur ne suit pas.

```bash
# Verifier le lag avec kafka-consumer-groups
kafka-consumer-groups.sh \
  --bootstrap-server kafka:9092 \
  --describe \
  --group my-consumer-group

# Output:
# GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
# my-group        order-events    0          1523456         1523456         0
# my-group        order-events    1          1498232         1498240         8
# my-group        order-events    2          1612000         1612150         150  ← lag!
```

**Alertes recommandees** :
- Lag > 10 000 messages : alerte warning
- Lag > 100 000 messages : alerte critique
- Lag en croissance > 1h : investigation immediate

---

## Kafka Streams — Processing Embarque

Kafka Streams est une librairie Java qui permet de faire du stream processing directement dans votre application — sans infrastructure Flink ou Spark separate.

```java
// Kafka Streams — exemple de comptage en temps reel
StreamsBuilder builder = new StreamsBuilder();

KStream<String, String> orderEvents = builder.stream("order-events");

// Compter les commandes par statut sur une fenetre de 1 heure
KTable<Windowed<String>, Long> statusCounts = orderEvents
    .mapValues(json -> parseOrderStatus(json))
    .groupBy((key, status) -> status)
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofHours(1)))
    .count();

// Ecrire le resultat dans un topic de sortie
statusCounts.toStream()
    .map((windowedStatus, count) -> KeyValue.pair(
        windowedStatus.key() + "@" + windowedStatus.window().start(),
        count.toString()
    ))
    .to("order-status-counts");

KafkaStreams streams = new KafkaStreams(builder.build(), streamsConfig);
streams.start();
```

**Kafka Streams vs Flink** :
- Kafka Streams : plus simple, embarque dans l'app, pas de cluster a gerer. Limite aux besoins simples.
- Flink : plus puissant, state management avance, gestion des late data, meilleur pour les topologies complexes.

---

## Deploiement Production

### Sizing du Cluster

**Calcul du nombre de brokers** :
```
Throughput requis : 1 GB/s entrant
Throughput d'un broker : ~200 MB/s (typique)
Replication factor : 3
Brokers requis : (1000 / 200) × 3 = 15 brokers
```

**Disques** : preferer NVMe SSD pour les brokers Kafka. La performance d'ecriture est critique.

**Retention** : configurer la retention en fonction de votre use case.
- Temps reel pur : 24-72h
- Replay et debug : 7-30 jours
- Data lake via S3 sink : 24h (l'archive est sur S3)

### Kafka sur Kubernetes (Strimzi)

```yaml
# Strimzi Kafka Cluster
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: production-cluster
spec:
  kafka:
    replicas: 3
    resources:
      requests:
        memory: 8Gi
        cpu: "2"
      limits:
        memory: 16Gi
        cpu: "4"
    storage:
      type: persistent-claim
      size: 1Ti
      class: fast-ssd
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      default.replication.factor: 3
      min.insync.replicas: 2
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 100Gi
```

### Alternatives Managees

| Service | Provider | Avantage |
|---|---|---|
| **Confluent Cloud** | Confluent | Full managed, Schema Registry inclus |
| **MSK** | AWS | Integre AWS, simple si deja sur AWS |
| **Event Hubs** | Azure | Compatible Kafka API, integre Azure |
| **Pub/Sub** | GCP | API differente mais similaire conceptuellement |
| **Redpanda** | Redpanda | Compatible Kafka, 10x plus rapide, pas de JVM |
