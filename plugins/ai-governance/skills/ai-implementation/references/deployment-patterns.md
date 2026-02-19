# Deployment Patterns — REST API, Batch, Streaming, Shadow, Canary & Edge

## Overview

Ce guide couvre les principaux patterns de deploiement de modeles ML en production : inference en ligne via REST API, batch inference, streaming inference, shadow deployment pour la validation sans risque, canary release pour le deploiement progressif, pattern champion/challenger, et deploiement sur edge pour les contraintes IoT et temps reel. Pour chaque pattern, le guide detaille quand l'utiliser, comment l'implementer, et les metriques de succes.

---

## REST API Inference — Deploiement en Ligne

### Quand Utiliser

- Predictions individuelles necessitant une reponse immediate (< 1 seconde)
- Applications web ou mobiles qui integrent le ML en temps reel
- Systemes de recommandation lors du chargement d'une page
- Modeles de scoring en temps reel (fraude, credit, eligibilite)

### Implementation avec FastAPI

```python
# api/main.py — API de serving de modele avec FastAPI
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
import time
import logging
import mlflow

app = FastAPI(title="ML Model Serving API", version="1.0.0")
logger = logging.getLogger(__name__)

# Charger le modele au demarrage (pas a chaque requete)
MODEL_URI = "models:/churn-prediction/Production"
model = mlflow.pyfunc.load_model(MODEL_URI)
model_version_info = mlflow.get_model_version_by_alias("churn-prediction", "Production")

class PredictionInput(BaseModel):
    customer_id: str
    nb_transactions_30d: int
    total_amount_30d: float
    days_since_last_transaction: int
    support_tickets_90d: int
    subscription_age_days: int

    @validator('nb_transactions_30d')
    def transactions_non_negative(cls, v):
        if v < 0:
            raise ValueError('nb_transactions_30d doit etre non-negatif')
        return v

    @validator('total_amount_30d')
    def amount_non_negative(cls, v):
        if v < 0:
            raise ValueError('total_amount_30d doit etre non-negatif')
        return v

class PredictionOutput(BaseModel):
    customer_id: str
    churn_probability: float
    risk_level: str
    model_version: str
    prediction_timestamp: float

@app.get("/health")
async def health():
    return {"status": "healthy", "model": "churn-prediction", "version": model_version_info.version}

@app.post("/predict", response_model=PredictionOutput)
async def predict(request: Request, input_data: PredictionInput):
    start_time = time.time()

    try:
        # Preparer les features
        features = {
            'nb_transactions_30d': input_data.nb_transactions_30d,
            'total_amount_30d': input_data.total_amount_30d,
            'days_since_last_transaction': input_data.days_since_last_transaction,
            'support_tickets_90d': input_data.support_tickets_90d,
            'subscription_age_days': input_data.subscription_age_days,
        }

        # Inference
        proba = float(model.predict(features)['churn_probability'])

        # Classification du risque
        risk_level = "high" if proba > 0.7 else "medium" if proba > 0.4 else "low"

        # Logguer pour le monitoring
        latency_ms = (time.time() - start_time) * 1000
        logger.info(
            "prediction_served",
            extra={
                "customer_id": input_data.customer_id,
                "churn_probability": proba,
                "risk_level": risk_level,
                "latency_ms": latency_ms,
                "model_version": model_version_info.version
            }
        )

        return PredictionOutput(
            customer_id=input_data.customer_id,
            churn_probability=round(proba, 4),
            risk_level=risk_level,
            model_version=model_version_info.version,
            prediction_timestamp=time.time()
        )

    except Exception as e:
        logger.error(f"Prediction error for customer {input_data.customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Prediction service error")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"error": "Internal server error"})
```

### Benchmark de Latence

Avant le deploiement, benchmarker la latence avec des donnees de taille production :

```bash
# Benchmark avec wrk (HTTP benchmarking tool)
wrk -t 4 -c 100 -d 30s \
  --script=benchmark/post_request.lua \
  http://localhost:8080/predict

# Ou avec Locust (Python)
# locust -f benchmark/locustfile.py --host http://localhost:8080

# Cibles de latence recommandees par type d'application
# API critique (paiement, fraude) : P99 < 50ms
# API recommandation temps reel : P99 < 200ms
# API analytique : P99 < 500ms
# API batch-like : P99 < 5000ms
```

---

## Batch Inference — Predictions en Lot

### Quand Utiliser

- Predictions quotidiennes ou hebdomadaires sur toute la base client
- Scores precalcules pour des campagnes marketing (envoyer les emails a haut risque)
- Prevision de la demande pour le lendemain ou la semaine suivante
- Scoring de tout le catalogue produit (recommandations pre-calculees)

### Architecture Batch

```python
# batch_inference.py — Batch scoring avec Spark ou pandas
import pandas as pd
import mlflow
import boto3
from datetime import datetime

def run_batch_inference(
    input_path: str,
    output_path: str,
    model_uri: str,
    batch_size: int = 10_000
):
    """
    Execute une inference batch sur un grand volume de donnees.

    Args:
        input_path: Chemin S3 vers les donnees d'inference (Parquet)
        output_path: Chemin S3 vers les resultats (Parquet)
        model_uri: URI MLflow du modele (ex: "models:/churn-prediction/Production")
        batch_size: Nombre de lignes traitees par batch
    """
    # Charger le modele
    model = mlflow.pyfunc.load_model(model_uri)
    model_version = mlflow.MlflowClient().get_model_version_by_alias(
        "churn-prediction", "Production"
    ).version

    # Lire les donnees
    df = pd.read_parquet(input_path)
    feature_columns = [c for c in df.columns if c not in ['customer_id', 'target']]

    results = []
    total_batches = (len(df) + batch_size - 1) // batch_size

    for i in range(0, len(df), batch_size):
        batch_num = i // batch_size + 1
        batch = df.iloc[i:i + batch_size]

        # Inference sur le batch
        predictions = model.predict(batch[feature_columns])
        batch_results = pd.DataFrame({
            'customer_id': batch['customer_id'],
            'churn_probability': predictions['churn_probability'],
            'prediction_date': datetime.today().strftime('%Y-%m-%d'),
            'model_version': model_version
        })
        results.append(batch_results)

        if batch_num % 10 == 0:
            print(f"Batch {batch_num}/{total_batches} traite")

    # Sauvegarder les resultats
    final_results = pd.concat(results, ignore_index=True)
    final_results.to_parquet(output_path, index=False)
    print(f"Predictions sauvegardees : {len(final_results)} clients")

    return final_results

# Scheduler avec Airflow
# dag = DAG("daily-churn-scoring", schedule_interval="0 6 * * *")
# batch_task = PythonOperator(task_id="run_batch", python_callable=run_batch_inference)
```

---

## Streaming Inference

### Quand Utiliser

- Predictions sur des evenements en temps quasi-reel (< 5 secondes)
- Scoring de fraude sur les transactions au fil de l'eau
- Recommandations declenchees par des evenements (vue de page, clic)
- Alertes en temps reel basees sur un comportement detecte

### Architecture Streaming avec Kafka

```python
# streaming_inference.py — Consumer Kafka pour l'inference en streaming
from confluent_kafka import Consumer, Producer, KafkaError
import json
import mlflow

# Charger le modele
model = mlflow.pyfunc.load_model("models:/fraud-detection/Production")

consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'fraud-detector',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': False
})

producer = Producer({'bootstrap.servers': 'kafka:9092'})

consumer.subscribe(['transactions-raw'])

def process_transaction(transaction: dict) -> dict:
    """Score une transaction pour le risque de fraude."""
    features = extract_features(transaction)
    fraud_probability = float(model.predict(features)['fraud_proba'])

    return {
        'transaction_id': transaction['transaction_id'],
        'customer_id': transaction['customer_id'],
        'amount': transaction['amount'],
        'fraud_probability': fraud_probability,
        'fraud_flag': fraud_probability > 0.8,
        'scored_at': time.time()
    }

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                logger.error(f"Consumer error: {msg.error()}")
            continue

        transaction = json.loads(msg.value().decode('utf-8'))
        result = process_transaction(transaction)

        # Publier le resultat
        producer.produce(
            'transactions-scored',
            key=str(result['transaction_id']),
            value=json.dumps(result).encode('utf-8')
        )
        producer.poll(0)

        # Committer l'offset apres traitement reussi
        consumer.commit(asynchronous=False)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
    producer.flush()
```

---

## Shadow Deployment

### Principe

Le shadow deployment (ou dark launch) consiste a faire tourner le nouveau modele en parallele du modele de production sans que ses predictions affectent les utilisateurs. Le nouveau modele recoit les memes requetes, loggue ses predictions, mais seul le modele actuel repond a l'utilisateur.

```python
# shadow_proxy.py — Proxy qui envoie les requetes aux deux modeles
import asyncio
import httpx
import logging

CURRENT_MODEL_URL = "http://churn-api-v2:8080/predict"
SHADOW_MODEL_URL = "http://churn-api-v3:8080/predict"

async def predict_with_shadow(request_data: dict) -> dict:
    """
    Envoie la requete au modele actuel ET au modele shadow.
    Retourne uniquement la reponse du modele actuel.
    """
    async with httpx.AsyncClient(timeout=5.0) as client:
        # Lancer les deux requetes en parallele
        current_task = asyncio.create_task(
            client.post(CURRENT_MODEL_URL, json=request_data)
        )
        shadow_task = asyncio.create_task(
            client.post(SHADOW_MODEL_URL, json=request_data)
        )

        # Attendre la reponse du modele actuel (critique)
        current_response = await current_task
        current_result = current_response.json()

        # Logguer la reponse du shadow en arriere-plan (non bloquant)
        try:
            shadow_response = await asyncio.wait_for(shadow_task, timeout=3.0)
            shadow_result = shadow_response.json()

            # Logguer la comparaison pour analyse
            logger.info("shadow_comparison", extra={
                "customer_id": request_data["customer_id"],
                "current_proba": current_result["churn_probability"],
                "shadow_proba": shadow_result["churn_probability"],
                "divergence": abs(current_result["churn_probability"] - shadow_result["churn_probability"]),
                "decision_changed": (current_result["churn_probability"] > 0.5) != (shadow_result["churn_probability"] > 0.5)
            })

        except asyncio.TimeoutError:
            logger.warning(f"Shadow model timeout for customer {request_data['customer_id']}")

    # Retourner uniquement la reponse du modele actuel
    return current_result
```

### Analyse du Shadow Deployment

Apres 1-2 semaines de shadow :

```python
# analyse_shadow.py — Comparer les predictions des deux modeles
import pandas as pd
import numpy as np
from scipy import stats

# Charger les logs (depuis BigQuery, S3, etc.)
logs = pd.read_parquet("logs/shadow_comparison.parquet")

# 1. Divergence globale
print(f"Predictions identiques (meme bucket) : {(logs['divergence'] < 0.1).mean():.1%}")
print(f"Decisions differentes : {logs['decision_changed'].mean():.1%}")

# 2. Distribution des probabilites
print(f"\nModele actuel - Proba moyenne : {logs['current_proba'].mean():.3f}")
print(f"Modele shadow - Proba moyenne : {logs['shadow_proba'].mean():.3f}")

# 3. Test statistique (les deux distributions sont-elles equivalentes ?)
ks_stat, ks_pvalue = stats.ks_2samp(logs['current_proba'], logs['shadow_proba'])
print(f"\nTest KS - statistic: {ks_stat:.4f}, p-value: {ks_pvalue:.4f}")
if ks_pvalue < 0.05:
    print("ATTENTION : Les distributions different significativement")

# 4. Segments les plus divergents
high_divergence = logs[logs['divergence'] > 0.2]
print(f"\nCas de forte divergence (>20 points) : {len(high_divergence)}")
print(high_divergence.groupby('risk_level')['divergence'].describe())

# Critere de passage au canary release :
# - Taux de decision change < 5%
# - Aucune divergence systematique sur un segment
# - Latence du shadow dans la SLA
```

---

## Canary Release

### Implementation Progressive

```python
# canary_router.py — Routage progressif entre champion et challenger
import random
from enum import Enum

class ModelVersion(Enum):
    CHAMPION = "v2"  # Version actuelle (production)
    CHALLENGER = "v3"  # Nouvelle version

def route_request(customer_id: str, canary_percentage: float) -> ModelVersion:
    """
    Route une requete vers le champion ou le challenger.
    Utilise customer_id pour un routage deterministe (meme client = meme modele).

    Args:
        customer_id: Identifiant du client
        canary_percentage: Pourcentage de trafic vers le challenger (0.0 - 1.0)
    """
    # Hash deterministe : le meme client va toujours vers le meme modele
    hash_value = hash(customer_id) % 100
    if hash_value < canary_percentage * 100:
        return ModelVersion.CHALLENGER
    return ModelVersion.CHAMPION

# Escalade progressive
CANARY_SCHEDULE = [
    {"percentage": 0.01, "duration_hours": 24, "check": "error_rate < 1%"},
    {"percentage": 0.05, "duration_hours": 48, "check": "latency_p99 < SLA"},
    {"percentage": 0.25, "duration_hours": 72, "check": "business_kpi stable"},
    {"percentage": 0.50, "duration_hours": 48, "check": "business_kpi + challenger"},
    {"percentage": 1.00, "duration_hours": 0, "check": "migration complete"}
]
```

### Metriques de Rollback Automatique

```python
# rollback_monitor.py — Surveillance et rollback automatique
from dataclasses import dataclass

@dataclass
class CanaryThresholds:
    max_error_rate: float = 0.01      # 1% max d'erreurs
    max_latency_p99_ms: float = 200   # 200ms max au P99
    min_predictions_per_hour: int = 100  # Minimum de predictions pour valider
    max_divergence_from_champion: float = 0.10  # Max 10% de difference de distribution

def check_canary_health(metrics: dict) -> tuple[bool, str]:
    """
    Verifie la sante du canary et decide si un rollback est necessaire.
    Retourne (should_rollback, reason).
    """
    thresholds = CanaryThresholds()

    if metrics['error_rate'] > thresholds.max_error_rate:
        return True, f"Error rate {metrics['error_rate']:.2%} exceeds threshold {thresholds.max_error_rate:.2%}"

    if metrics['latency_p99_ms'] > thresholds.max_latency_p99_ms:
        return True, f"Latency P99 {metrics['latency_p99_ms']:.0f}ms exceeds threshold {thresholds.max_latency_p99_ms:.0f}ms"

    if metrics['sample_size'] < thresholds.min_predictions_per_hour:
        return False, "Insufficient sample size — monitoring only"

    if metrics['distribution_divergence'] > thresholds.max_divergence_from_champion:
        return True, f"Distribution divergence {metrics['distribution_divergence']:.3f} exceeds threshold"

    return False, "All metrics within bounds"
```

---

## Champion / Challenger

### Pattern et Benefices

Le pattern champion/challenger maintient en permanence deux modeles en production :
- **Champion** : le modele de production (90-95% du trafic)
- **Challenger** : le nouveau modele en evaluation (5-10% du trafic)

Ce pattern permet une comparaison continue sans avoir a planifier des campagnes d'A/B test.

```python
# champion_challenger.py
class ChampionChallengerRouter:
    def __init__(self, champion_model, challenger_model, challenger_traffic=0.10):
        self.champion = champion_model
        self.challenger = challenger_model
        self.challenger_traffic = challenger_traffic
        self.metrics = {"champion": [], "challenger": []}

    def predict(self, features: dict, customer_id: str) -> dict:
        # Routage deterministe par customer_id
        is_challenger = (hash(customer_id) % 100) < (self.challenger_traffic * 100)

        if is_challenger:
            result = self.challenger.predict(features)
            result['model_group'] = 'challenger'
        else:
            result = self.champion.predict(features)
            result['model_group'] = 'champion'

        # Logguer pour la comparaison
        self.metrics[result['model_group']].append(result)
        return result

    def evaluate_challenger(self) -> dict:
        """Compare les performances du champion et du challenger."""
        champion_metrics = calculate_metrics(self.metrics['champion'])
        challenger_metrics = calculate_metrics(self.metrics['challenger'])

        return {
            "champion": champion_metrics,
            "challenger": challenger_metrics,
            "challenger_wins": challenger_metrics['business_kpi'] > champion_metrics['business_kpi'],
            "recommendation": "PROMOTE" if challenger_metrics['business_kpi'] > champion_metrics['business_kpi'] * 1.05 else "KEEP_CHAMPION"
        }
```

---

## Edge et Modeles Embarques

### Quand Deployer sur Edge

- Contraintes de latence < 10ms (impossible avec un appel reseau)
- Connectivite intermittente (objets IoT, vehicules, appareils mobiles)
- Confidentialite (les donnees ne doivent pas quitter l'appareil)
- Couts d'inference cloud trop eleves a l'echelle (millions d'appareils)

### Optimisation des Modeles pour l'Edge

```python
# Quantization : reduire la taille et accelerer l'inference
import onnxruntime
import numpy as np

# Etape 1 : Exporter le modele en ONNX (format universel pour l'edge)
import mlflow.onnx
onnx_model = mlflow.onnx.load_model("models:/churn-prediction/Production")

# Etape 2 : Quantification INT8 (taille /4, inference 2-3x plus rapide)
from onnxruntime.quantization import quantize_dynamic, QuantType

quantize_dynamic(
    model_input="model.onnx",
    model_output="model_quantized.onnx",
    weight_type=QuantType.QInt8
)

# Etape 3 : Inference avec ONNX Runtime (supporte CPU, GPU, ARM, NPU)
sess = onnxruntime.InferenceSession("model_quantized.onnx")

def predict_edge(features: dict) -> float:
    input_array = np.array([[features[k] for k in FEATURE_ORDER]], dtype=np.float32)
    output = sess.run(None, {sess.get_inputs()[0].name: input_array})
    return float(output[0][0][1])  # Probabilite de la classe positive

# Benchmarks typiques apres quantification
# Modele float32 : 15ms inference, 50MB
# Modele INT8    : 5ms inference, 12MB (3x plus rapide, 4x plus petit)
```

### Formats de Modeles pour l'Edge

| Format | Plateforme cible | Avantages | Limitations |
|---|---|---|---|
| **ONNX** | CPU, GPU, ARM, NPU (universel) | Multi-plateforme, bien supporte | Pas tout le ML |
| **TFLite** | Android, iOS, microcontroleurs | Tres compact, optimise mobile | Ecosysteme TensorFlow |
| **CoreML** | iOS, macOS (Apple) | Integration native Apple, NPU Apple Silicon | Apple uniquement |
| **TensorRT** | GPU NVIDIA (edge + cloud) | Performances maximales sur GPU NVIDIA | NVIDIA uniquement |
| **ONNX Runtime** | Windows, Linux, mobile (Microsoft) | Tres performant, large support | |
