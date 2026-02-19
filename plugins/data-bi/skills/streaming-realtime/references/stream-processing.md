# Stream Processing — Apache Flink et Spark Streaming

## Vue d'Ensemble

Le stream processing transforme des sequences d'evenements en resultats utiles : agregations, detections d'anomalies, enrichissements, joins entre streams. Deux moteurs dominent le marche : Apache Flink (reference pour la production enterprise) et Apache Spark Structured Streaming (polyvalent, moins avance sur les semantiques de streaming). Ce document couvre les deux avec leurs cas d'usage respectifs.

---

## Concepts Fondamentaux

### Event Time vs Processing Time

**Event Time** : le timestamp de l'evenement tel qu'il s'est produit dans le monde reel.

**Processing Time** : le timestamp de reception du message par le systeme de traitement.

**Ingestion Time** : le timestamp d'entree dans Kafka (entre les deux).

**Pourquoi ca compte** :
```
Evenement produit a 10h00 sur un telephone mobile hors ligne
→ Kafka le recooit a 10h45 quand le telephone se reconnecte
→ Processing Time = 10h45 (incorrect pour l'analytique)
→ Event Time = 10h00 (correct)
```

**Regle** : toujours travailler en Event Time pour les analyses business. Processing Time seulement pour les metriques systeme (latence du pipeline lui-meme).

### Late Data et Watermarks

**Probleme** : en Event Time, les messages peuvent arriver en retard (mobile offline, retard reseau). Le systeme de streaming ne sait pas quand il a "tout" les donnees d'une fenetre.

**Watermark** : le systeme declare "je pense avoir recu tous les messages jusqu'au timestamp T-D" ou D est le delai maximal tolere.

```java
// Flink — watermark avec 5 secondes de tolerance
WatermarkStrategy<Order> strategy = WatermarkStrategy
    .<Order>forBoundedOutOfOrderness(Duration.ofSeconds(5))
    .withTimestampAssigner((order, ts) -> order.getCreatedAt().toEpochMilli());

DataStream<Order> orders = env
    .fromSource(kafkaSource, strategy, "Orders Source");
```

**Trade-off** :
- Watermark trop agressif (D petit) → certains messages late sont ignores → resultats incorrects
- Watermark trop conservateur (D grand) → la fenetre attend longtemps avant de se fermer → latence elevee

---

## Apache Flink — Reference Avancee

### Operateurs Essentiels

**map / flatMap / filter** :
```java
// Transformer chaque ordre en un OrderMetric
DataStream<OrderMetric> metrics = orders
    .filter(order -> order.getStatus().equals("COMPLETED"))
    .map(order -> new OrderMetric(
        order.getUserId(),
        order.getAmount(),
        order.getCreatedAt()
    ));
```

**keyBy** : partitionner le stream par une cle. Tous les elements avec la meme cle vont au meme sous-tache (operator instance).

```java
// Partitionner par user_id pour calculer le montant par utilisateur
KeyedStream<Order, String> byUser = orders.keyBy(Order::getUserId);
```

**Aggregations** :
```java
// Somme des montants par user sur une fenetre de 1 heure
DataStream<UserRevenue> hourlyRevenue = orders
    .keyBy(Order::getUserId)
    .window(TumblingEventTimeWindows.of(Time.hours(1)))
    .aggregate(new AggregateFunction<Order, Double, UserRevenue>() {
        @Override
        public Double createAccumulator() { return 0.0; }

        @Override
        public Double add(Order order, Double accumulator) {
            return accumulator + order.getAmount();
        }

        @Override
        public UserRevenue getResult(Double accumulator) {
            return new UserRevenue(accumulator);
        }

        @Override
        public Double merge(Double a, Double b) { return a + b; }
    });
```

### Process Functions — Logique Avancee

Les `ProcessFunction` donnent acces a l'etat, aux timers et aux metadata — pour des logiques impossibles avec les simples aggregations.

```java
// Detection de fraude : plus de 5 transactions en 60 secondes
public class FraudDetector extends KeyedProcessFunction<String, Transaction, Alert> {

    private ValueState<Integer> transactionCount;
    private ValueState<Long> timerTimestamp;

    @Override
    public void open(Configuration config) {
        transactionCount = getRuntimeContext().getState(
            new ValueStateDescriptor<>("count", Integer.class, 0)
        );
        timerTimestamp = getRuntimeContext().getState(
            new ValueStateDescriptor<>("timer", Long.class)
        );
    }

    @Override
    public void processElement(Transaction tx, Context ctx, Collector<Alert> out) throws Exception {
        int count = transactionCount.value() + 1;
        transactionCount.update(count);

        // Premier evenement → enregistrer un timer dans 60 secondes
        if (count == 1) {
            long timer = ctx.timestamp() + 60_000L;
            ctx.timerService().registerEventTimeTimer(timer);
            timerTimestamp.update(timer);
        }

        // Seuil depasse → alerter
        if (count >= 5) {
            out.collect(new Alert(ctx.getCurrentKey(), "Fraud: " + count + " transactions in 60s"));
        }
    }

    @Override
    public void onTimer(long timestamp, OnTimerContext ctx, Collector<Alert> out) throws Exception {
        // La fenetre de 60s est ecoulee → reset le compteur
        transactionCount.clear();
        timerTimestamp.clear();
    }
}
```

### State Backends

L'etat dans Flink peut etre stocke de differentes facons :

**MemoryStateBackend** : etat en memoire JVM. Rapide mais limite et non-persistent. Dev seulement.

**FsStateBackend** : checkpoints sur le systeme de fichiers (HDFS, S3). Etat local en memoire.

**RocksDBStateBackend** : etat sur disque (RocksDB), checkpoints sur S3. Le plus scalable pour les grands etats. Requis si l'etat depasse la RAM disponible.

```java
// Configurer RocksDB comme state backend
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.setStateBackend(new EmbeddedRocksDBStateBackend());
env.getCheckpointConfig().setCheckpointStorage("s3://my-bucket/flink-checkpoints");
env.enableCheckpointing(60_000);  // Checkpoint toutes les 60 secondes
```

### Joins entre Streams

**Interval Join** : joindre deux streams dans une fenetre de temps relative.

```java
// Joindre les commandes avec les paiements (paiement arrive dans les 5 minutes apres la commande)
orders
    .keyBy(Order::getOrderId)
    .intervalJoin(payments.keyBy(Payment::getOrderId))
    .between(Time.seconds(-10), Time.minutes(5))  // Paiement arrive 10s avant a 5min apres
    .process(new ProcessJoinFunction<Order, Payment, OrderWithPayment>() {
        @Override
        public void processElement(Order order, Payment payment, Context ctx, Collector<OrderWithPayment> out) {
            out.collect(new OrderWithPayment(order, payment));
        }
    });
```

---

## Spark Structured Streaming

### Pourquoi Choisir Spark Streaming

Spark Structured Streaming est excellent si :
- L'equipe utilise deja Spark pour le batch (meme code, meme API)
- Besoin de ML en streaming (Spark MLlib integration)
- Latence >= 1 seconde acceptable (micro-batch mode)
- Besoin de Delta Lake pour l'ACID sur le data lake

### Micro-Batch vs Continuous Processing

**Micro-batch** (defaut) : Spark collecte les messages sur une periode (trigger), traite le batch, ecrit les resultats. Latence : 100ms-1s. Plus robuste.

**Continuous Processing** : traitement evenement par evenement. Latence : ~1ms. Moins stable, moins de fonctionnalites.

### Implementation

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum, count
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

spark = SparkSession.builder \
    .appName("OrderStreamProcessor") \
    .config("spark.sql.streaming.checkpointLocation", "s3://my-bucket/spark-checkpoints") \
    .getOrCreate()

# Schema des messages
order_schema = StructType() \
    .add("order_id", StringType()) \
    .add("user_id", StringType()) \
    .add("amount", DoubleType()) \
    .add("created_at", TimestampType())

# Lire depuis Kafka
raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "order-events") \
    .option("startingOffsets", "latest") \
    .load()

# Parser le JSON
orders = raw_stream \
    .select(from_json(col("value").cast("string"), order_schema).alias("data")) \
    .select("data.*") \
    .withWatermark("created_at", "5 minutes")  # Tolerer 5 min de retard

# Agregation par fenetre de 1 heure
hourly_stats = orders \
    .groupBy(
        window(col("created_at"), "1 hour"),
        col("user_id")
    ) \
    .agg(
        count("order_id").alias("order_count"),
        sum("amount").alias("total_amount")
    )

# Ecrire dans Kafka
query = hourly_stats \
    .select(
        col("user_id").alias("key"),
        to_json(struct("*")).alias("value")
    ) \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("topic", "order-hourly-stats") \
    .outputMode("update") \
    .trigger(processingTime="10 seconds") \
    .start()

query.awaitTermination()
```

### Output Modes

| Mode | Description | Compatibilite |
|---|---|---|
| **Append** | Seules les nouvelles lignes sont ecrites | Pas d'aggregation (ou aggregation sans update) |
| **Update** | Les lignes mises a jour sont ecrites | Aggregations avec watermark |
| **Complete** | Toute la table est re-ecrite a chaque trigger | Aggregations sans watermark (attention a la taille) |

### Delta Lake avec Spark Streaming

```python
# Ecrire en streaming dans Delta Lake (ACID, time travel)
query = orders.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "s3://bucket/checkpoints/orders") \
    .start("s3://bucket/delta/orders")

# Query batch sur le meme Delta Lake
spark.read.format("delta").load("s3://bucket/delta/orders") \
    .where("amount > 1000") \
    .show()

# Time travel — lire les donnees d'hier
spark.read.format("delta") \
    .option("timestampAsOf", "2025-01-15 10:00:00") \
    .load("s3://bucket/delta/orders") \
    .show()
```

---

## Flink vs Spark Streaming — Comparaison

| Critere | Flink | Spark Streaming |
|---|---|---|
| **Latence** | Quelques ms (true streaming) | 100ms-1s (micro-batch) |
| **Exactly-once** | Natif et robuste | Via idempotent writes |
| **State management** | Excellent (RocksDB, TieredState) | Bon mais moins flexible |
| **Late data** | Excellent (watermarks avances) | Bon (watermarks basiques) |
| **Courbe d'apprentissage** | Elevee (Java/Scala natif) | Moyenne (Python API) |
| **Ecosysteme ML** | Limites | Excellent (MLlib, pandas API) |
| **Integration Delta Lake** | Possible (connector) | Natif |
| **Batch + Streaming** | Possible (DataStream + Table API) | Excellent (meme API) |
| **Communaute** | Plus petite mais specialisee | Tres large |
| **Use case ideal** | Streaming critique, latence faible | Teams Spark existantes, ML |

---

## Exactly-Once Semantics

### At-Most-Once, At-Least-Once, Exactly-Once

**At-Most-Once** : message traite 0 ou 1 fois. Perte possible. Acceptable pour les logs non-critiques.

**At-Least-Once** : message traite 1+ fois. Duplicats possibles. Le plus simple a implementer.

**Exactly-Once** : message traite exactement 1 fois. Le plus difficile. Requis pour les finances, les stocks, les compteurs critiques.

### Exactly-Once avec Flink

```java
// Configuration pour exactly-once
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Activer checkpointing
env.enableCheckpointing(30_000);  // Checkpoint toutes les 30s
env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(5_000);
env.getCheckpointConfig().setCheckpointTimeout(60_000);

// Source Kafka avec exactly-once
KafkaSource<String> source = KafkaSource.<String>builder()
    .setBootstrapServers("kafka:9092")
    .setTopics("order-events")
    .setGroupId("flink-exactly-once")
    .setStartingOffsets(OffsetsInitializer.committed())
    .setValueOnlyDeserializer(new SimpleStringSchema())
    .build();

// Sink Kafka avec exactly-once (transactions)
KafkaSink<String> sink = KafkaSink.<String>builder()
    .setBootstrapServers("kafka:9092")
    .setRecordSerializer(KafkaRecordSerializationSchema.builder()
        .setTopic("output-topic")
        .setValueSerializationSchema(new SimpleStringSchema())
        .build())
    .setDeliveryGuarantee(DeliveryGuarantee.EXACTLY_ONCE)  // Transactional producer
    .setTransactionalIdPrefix("flink-txn")
    .build();
```

---

## Monitoring des Pipelines

### Flink Dashboard

Le Flink Web UI (port 8081) expose :
- Topologie du job (DAG)
- Backpressure par operateur (si rouge → goulot d'etranglement)
- Latence par tache
- Progression des checkpoints
- Taux de throughput par operateur

### Metriques Prometheus

```yaml
# Flink metrics reporter (prometheus)
metrics.reporters: prometheus
metrics.reporter.prometheus.class: org.apache.flink.metrics.prometheus.PrometheusReporter
metrics.reporter.prometheus.port: 9249
```

**Metriques critiques** :
- `flink_taskmanager_job_task_backPressuredTimeMsPerSecond` : temps de backpressure
- `flink_jobmanager_job_numRestarts` : nombre de redemarrages (doit etre proche de 0)
- `flink_taskmanager_job_task_checkpointing_*` : duree et statut des checkpoints
- `flink_taskmanager_Status_JVM_Memory_Heap_Used` : utilisation memoire
