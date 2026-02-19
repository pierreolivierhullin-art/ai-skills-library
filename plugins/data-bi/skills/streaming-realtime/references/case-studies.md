# Etudes de Cas — Streaming et Real-Time Analytics en Production

## Vue d'Ensemble

Ces etudes de cas illustrent des deployments reels : une fintech qui implemente la detection de fraude en temps reel, un e-commerce qui migre vers une architecture streaming-first, un operateur industriel IoT qui deploy du monitoring temps reel, et une startup qui construit son premier pipeline streaming sans infrastructure lourde.

---

## Cas 1 — Fintech : Detection de Fraude en Temps Reel (< 200ms)

### Contexte

Fintech de paiement BtoB (8 millions de transactions/mois, ticket moyen 340 EUR). Probleme : systeme de detection de fraude batch qui tourne toutes les 4 heures → les fraudes detectees apres plusieurs transactions, avant blocage.

Pertes moyennes liees a la fraude : 1.2% du volume (480K EUR/mois). Objectif : detection en < 200ms pour bloquer avant autorisation, reduire les pertes a < 0.3%.

### Architecture Deployee

**Pipeline** :
```
Transactions (API) → Kafka (topic: transactions-raw)
                          ↓
                     Flink Stream Processor
                          ├── Enrichissement (profil utilisateur depuis Redis)
                          ├── Feature Engineering (vitesse, patterns, historique 1h)
                          ├── Scoring ML (modele charge en memoire Flink)
                          └── Decision (< 200ms end-to-end)
                          ↓
              ┌──────────────────────────┐
              ↓                          ↓
    Kafka (transactions-scored)    Redis (score cache, TTL 1h)
              ↓
    API Gateway (bloque si score > 0.8)
```

### Implementation du Feature Engineering Temps Reel

```java
public class FraudFeatureExtractor extends KeyedProcessFunction<String, Transaction, ScoredTransaction> {

    // Etat : fenetre glissante 1 heure par user
    private ListState<Transaction> recentTransactions;
    private ValueState<UserProfile> userProfile;

    @Override
    public void processElement(Transaction tx, Context ctx, Collector<ScoredTransaction> out) throws Exception {

        List<Transaction> recent = Lists.newArrayList(recentTransactions.get());
        recent.add(tx);
        recent.removeIf(t -> t.getTimestamp() < ctx.timestamp() - 3_600_000);  // 1h
        recentTransactions.update(recent);

        // Features calculees en temps reel
        Map<String, Double> features = new HashMap<>();

        // Vitesse (nb transactions dans la derniere heure)
        features.put("tx_count_1h", (double) recent.size());

        // Montant anormal
        double avg_amount = recent.stream().mapToDouble(Transaction::getAmount).average().orElse(0);
        features.put("amount_deviation", Math.abs(tx.getAmount() - avg_amount) / (avg_amount + 1));

        // Changement de pays
        UserProfile profile = userProfile.value();
        features.put("new_country", tx.getCountry().equals(profile.getHomeCountry()) ? 0.0 : 1.0);

        // Heure inhabituelle
        int hour = LocalDateTime.ofInstant(Instant.ofEpochMilli(tx.getTimestamp()), ZoneOffset.UTC).getHour();
        features.put("unusual_hour", (hour < 6 || hour > 23) ? 1.0 : 0.0);

        // Score ML
        double fraudScore = mlModel.predict(features);

        out.collect(new ScoredTransaction(tx, fraudScore, features));
    }
}
```

### Resultats (6 mois)

| Metrique | Avant | Apres |
|---|---|---|
| Latence de detection | 4 heures | 145ms (p95) |
| Taux de fraude | 1.2% du volume | 0.28% du volume |
| Economies mensuelles | — | 375K EUR |
| Faux positifs (transactions bloquees a tort) | N/A | 0.08% (acceptable) |
| Throughput | N/A | 4 000 tx/seconde (pic) |

**Couts infrastructure** : 8 500 EUR/mois (cluster Kafka + Flink Kubernetes + Redis). ROI en 1 semaine.

**Lecon** : la detection de fraude en temps reel necessite deux composants souvent separes : le feature engineering streaming (Flink) et le modele ML (charge en memoire dans le processor — pas d'appel HTTP synchrone). Chaque appel HTTP synchrone dans le chemin critique ajoute 10-50ms de latence.

---

## Cas 2 — E-commerce : Migration vers une Architecture Streaming-First

### Contexte

E-commerce mode (2.5M clients, 15M EUR de CA mensuel). Architecture legacy : batch ETL toutes les 4 heures vers un Data Warehouse Redshift. Problemes :
- Dashboard CA visible avec 4 heures de retard → decisions publicitaires suboptimales
- Detecter les ruptures de stock avec 4 heures de delai → ventes ratees
- Machine de recommandation alimentee quotidiennement → recommendations peu pertinentes

**Objectif** : passer a un reporting avec < 5 minutes de latence sur les metriques cles.

### Migration Progressive (6 Mois)

**Phase 1 (mois 1-2) — Kafka comme backbone** :
- Deploiement Confluent Cloud (managed Kafka)
- Publication de tous les evenements e-commerce dans Kafka (commandes, vues produit, clics)
- CDC Debezium depuis PostgreSQL pour les changements de stock

**Phase 2 (mois 3-4) — Premier pipeline streaming** :
- Deploiement Flink sur Kubernetes (Flink Operator)
- Premier use case : CA temps reel par categorie → ClickHouse → Grafana dashboard
- Second use case : alerte stock < 5 unites → notification Slack automatique

**Phase 3 (mois 5-6) — Generalisation** :
- Migration du rapport CA (ancien batch 4h → streaming < 5 min)
- Alimentation de la machine de recommandation (sessions en cours → suggestions produits)
- Donnees publicitaires : optimisation campagnes Meta/Google basee sur les conversions temps reel

### Architecture Finale

```
Shopify Webhooks ─────┐
iOS/Android App  ─────┤
PostgreSQL (CDC) ─────┤→ Confluent Cloud (Kafka)
Google Analytics ─────┘         ↓
                          Flink (managed Kubernetes)
                          ├── Revenue aggregation (1min windows)
                          ├── Stock alerts (threshold detection)
                          ├── Session enrichment (recommender data)
                          └── Ad conversion attribution (30min window)
                                    ↓
                    ┌───────────────────────────────┐
                    ↓               ↓               ↓
               ClickHouse     Redis Cache      Redshift
               (OLAP 5min)    (live metrics)   (historical)
                    ↓               ↓
               Grafana        React Dashboard
               (operations)   (marketing team)
```

### Resultats

| Metrique | Avant (batch 4h) | Apres (streaming) |
|---|---|---|
| Latence reporting CA | 4 heures | 3 minutes |
| Ruptures de stock detectees | Apres 4h | Apres 45 secondes |
| Uplift publicite (budget realoue en temps reel) | — | +8% ROAS |
| Recommandations pertinentes (CTR) | 2.1% | 3.8% |
| Temps de query dashboard | 8-15 secondes | 200-500ms |

**Obstacle rencontre** : la migration du ETL batch vers le streaming a necessite de refactoriser la logique de calcul des remises (complexe, stateful). Solution : maintenir le batch pour les remises complexes (un seul cas) et streamer tout le reste.

---

## Cas 3 — Operateur Industriel : Monitoring IoT 50 000 Capteurs

### Contexte

Groupe industriel avec 12 usines (France, Allemagne, Italie). 50 000 capteurs IoT (temperature, pression, vibration, debit). Volume : 500 messages/seconde par capteur en agregation = 25 millions de messages/heure.

Probleme : les pannes machines couteuses (arret de production = 15 000 EUR/heure) ne sont detectees qu'apres le fait. Objectif : maintenance predictive avec 30-60 minutes d'avance.

### Architecture

```
Capteurs IoT (MQTT)
         ↓
MQTT Broker (Eclipse Mosquitto — edge computing)
         ↓
Kafka (topic par usine et type de capteur)
├── factory-paris.temperature
├── factory-paris.vibration
├── factory-berlin.pressure
└── ...
         ↓
Flink Stream Processor (cluster central)
├── Aggregation (moyenne 1 min, 5 min, 15 min par capteur)
├── Anomalie Detection (Z-score sur 24h glissantes)
├── Correlation Analysis (vibration + temperature avant panne)
└── ML Predictif (modele par type machine, reentraine hebdo)
         ↓
         ├── InfluxDB (metriques temps-serie pour visualisation)
         ├── Kafka (alertes → systeme GMAO)
         └── S3 (archive pour ML training)
         ↓
Grafana (dashboard operational) + GMAO (alertes maintenance)
```

### Detection d'Anomalie en Streaming

```java
public class AnomalyDetector extends KeyedProcessFunction<String, SensorReading, Alert> {

    // Etat : statistiques glissantes 24h
    private MapState<String, Double> rollingStats;  // {mean, std, min, max}

    @Override
    public void processElement(SensorReading reading, Context ctx, Collector<Alert> out) throws Exception {

        Map<String, Double> stats = rollingStats.entries().stream()
            .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

        if (stats.isEmpty()) {
            // Premiere mesure
            stats.put("mean", reading.getValue());
            stats.put("std", 0.0);
            stats.put("count", 1.0);
        } else {
            // Mise a jour incrementale des statistiques (Welford's algorithm)
            double n = stats.get("count") + 1;
            double delta = reading.getValue() - stats.get("mean");
            double newMean = stats.get("mean") + delta / n;
            double m2 = stats.get("m2_accumulator") + delta * (reading.getValue() - newMean);

            stats.put("mean", newMean);
            stats.put("std", n > 1 ? Math.sqrt(m2 / (n - 1)) : 0);
            stats.put("count", n);
            stats.put("m2_accumulator", m2);
        }

        rollingStats.putAll(stats);

        // Detection Z-score
        double mean = stats.get("mean");
        double std = stats.get("std");

        if (std > 0) {
            double zScore = Math.abs((reading.getValue() - mean) / std);

            if (zScore > 3.5) {  // Alerte severe
                out.collect(new Alert(
                    reading.getSensorId(),
                    "CRITICAL",
                    String.format("Z-score: %.2f (valeur: %.2f, mean: %.2f, std: %.2f)",
                                  zScore, reading.getValue(), mean, std),
                    ctx.timestamp()
                ));
            } else if (zScore > 2.5) {  // Alerte warning
                out.collect(new Alert(reading.getSensorId(), "WARNING", ...));
            }
        }
    }
}
```

### Resultats (12 mois post-deployment)

| Metrique | Avant | Apres |
|---|---|---|
| Pannes non detectees a l'avance | 78% | 12% |
| Delai moyen de detection pre-panne | 0 (reactif) | 47 minutes |
| Arrets non planifies | 24/an | 7/an |
| Cout des arrets non planifies | 2.4M EUR/an | 700K EUR/an |
| Cout infrastructure streaming | — | 180K EUR/an |
| ROI net | — | 1.52M EUR/an |

---

## Cas 4 — Startup : Premier Pipeline Streaming sans Infrastructure Lourde

### Contexte

Startup B2B analytics (12 employes, 2 data engineers). Besoin : alertes en temps reel pour les clients quand leurs KPIs depassent des seuils. Budget data infrastructure : 2 000 EUR/mois maximum.

Contrainte : pas de Flink (trop complexe pour 2 personnes), pas de Kafka self-hosted (trop a maintenir).

### Stack Choisie (Budget Contraint)

**Kafka managed** : Confluent Cloud Starter (500 EUR/mois pour 3 GB/heure de throughput).

**Stream processing** : Faust (librairie Python Kafka Streams-like — pas de cluster a gerer, embarque dans l'application).

**Storage** : TimescaleDB sur Supabase (base de donnees temps-serie PostgreSQL — 25 EUR/mois).

**Alerting** : logique dans Faust → webhook vers l'API du client.

### Implementation avec Faust

```python
import faust
from datetime import timedelta

app = faust.App(
    'kpi-alerting',
    broker='kafka://kafka.confluent.cloud:9092',
    store='rocksdb://',  # State persistant
)

# Schema des events
class KpiEvent(faust.Record):
    client_id: str
    metric_name: str
    value: float
    timestamp: float

class Alert(faust.Record):
    client_id: str
    metric_name: str
    current_value: float
    threshold: float
    triggered_at: float

# Topic d'entree
kpi_topic = app.topic('kpi-events', value_type=KpiEvent)

# Table pour les seuils clients
thresholds_table = app.Table('client-thresholds', default=dict)

# Table pour le rate limiting (max 1 alerte / 30 min par metrique)
last_alert_table = app.Table('last-alerts', default=float)

@app.agent(kpi_topic)
async def process_kpi(events):
    async for event in events:
        client_thresholds = thresholds_table[event.client_id]
        threshold = client_thresholds.get(event.metric_name)

        if threshold is None:
            continue

        # Verifier le seuil
        if event.value > threshold:
            # Rate limiting : max 1 alerte par 30 minutes
            last_alert_key = f"{event.client_id}:{event.metric_name}"
            last_alert = last_alert_table[last_alert_key]

            if event.timestamp - last_alert > 1800:  # 30 minutes
                last_alert_table[last_alert_key] = event.timestamp
                await send_alert(Alert(
                    client_id=event.client_id,
                    metric_name=event.metric_name,
                    current_value=event.value,
                    threshold=threshold,
                    triggered_at=event.timestamp
                ))

async def send_alert(alert: Alert):
    """Envoyer l'alerte via webhook."""
    webhook_url = get_client_webhook(alert.client_id)
    async with aiohttp.ClientSession() as session:
        await session.post(webhook_url, json=alert.to_representation())
```

### Resultats

| Metrique | Valeur |
|---|---|
| Latence alerte | 2-8 secondes (vs objectif < 30s) |
| Throughput max | 50 000 events/seconde (suffisant) |
| Cout infrastructure | 525 EUR/mois total |
| Temps d'implementation | 3 semaines (vs 3 mois estimés avec Flink) |
| Code maintenu par | 1 data engineer (temps partiel) |

**Lecon** : pour les startups, la simplicite operationnelle prime. Faust (Python) permet de faire 80% de ce que Flink fait avec 20% de la complexite. Migrer vers Flink quand le throughput ou la complexite le necessitent — pas avant. Le vrai risque n'est pas la sur-ingenierie technique, c'est de ne pas livrer la feature assez vite.
