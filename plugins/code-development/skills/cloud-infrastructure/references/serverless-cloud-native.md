# Serverless & Cloud-Native — Lambda, Cloud Run, Azure Functions & Event-Driven Architecture

## Overview

Ce guide couvre les architectures serverless et cloud-native : fonctions as a service (Lambda, Cloud Functions, Azure Functions), conteneurs serverless (Cloud Run, App Runner, Container Apps), architectures événementielles, et les patterns d'optimisation serverless. L'objectif est de savoir quand et comment adopter le serverless pour simplifier l'opérationnel, réduire les coûts, et scaler automatiquement.

---

## Fondamentaux du Serverless

### Qu'est-ce que le Serverless ?

Le serverless ne signifie pas "sans serveurs" — il signifie que vous ne gérez pas les serveurs. Le cloud provider s'occupe de :
- Provisionnement et scaling automatique
- Maintenance et mises à jour de l'OS et du runtime
- Haute disponibilité et tolérance aux pannes
- Facturation à l'usage (pas de ressources idle)

**Modèles serverless** :

| Modèle | Exemples | Granularité | Use case |
|---|---|---|---|
| **FaaS (Functions)** | Lambda, Cloud Functions | Par invocation | Event handlers, APIs légères, traitements ponctuels |
| **Conteneurs serverless** | Cloud Run, App Runner | Par requête | APIs complexes, microservices, ML serving |
| **BaaS (Backend)** | DynamoDB, Firestore, S3 | Par opération | Stockage, base de données, auth |
| **Orchestration serverless** | Step Functions, Cloud Workflows | Par exécution | Workflows multi-étapes |

### Avantages et Limites

**Avantages** :
- Scaling automatique de 0 à millions de requêtes
- Pas de gestion d'infrastructure (moins de charge ops)
- Coût proportionnel à l'usage réel (pas de ressources idle)
- Haute disponibilité par défaut (multi-AZ inclus)
- Déploiement rapide et itératif

**Limites** :
- **Cold start** : latence de démarrage (10ms-15s selon le runtime et la taille)
- **Durée maximale** : Lambda = 15 min, Cloud Functions = 60 min
- **État** : les fonctions sont stateless (l'état doit être externalisé dans Redis, DynamoDB, etc.)
- **Debug complexe** : logs distribués, difficile à reproduire localement
- **Coût à très haut volume** : au-delà de ~1M requêtes/jour, les VMs peuvent être moins chères

---

## AWS Lambda — Référence du FaaS

### Configuration et Bonnes Pratiques

```python
# handler.py — Lambda function Python optimisée
import json
import boto3
import os
from typing import Any, Dict

# ✅ Initialiser les clients AWS EN DEHORS du handler (réutilisation entre invocations)
# Le container Lambda est réutilisé entre invocations chaudes — profiter de ce cache
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

# ✅ Charger les secrets au démarrage, pas à chaque invocation
import boto3
secrets_client = boto3.client('secretsmanager')
secret_value = secrets_client.get_secret_value(
    SecretId=os.environ['SECRET_ARN']
)['SecretString']
API_KEY = json.loads(secret_value)['api_key']


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler Lambda avec gestion correcte des erreurs et des réponses HTTP.
    """
    try:
        # Valider les inputs
        body = json.loads(event.get('body', '{}'))
        customer_id = body.get('customer_id')
        if not customer_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'customer_id is required'}),
                'headers': {'Content-Type': 'application/json'}
            }

        # Logique métier
        result = process_customer(customer_id)

        return {
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {
                'Content-Type': 'application/json',
                'X-Request-Id': context.aws_request_id
            }
        }

    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        # Loguer l'erreur complète pour le debugging
        print(f"Unexpected error: {str(e)}")
        raise  # Reraise pour que Lambda retente (si configuré) et alerte


def process_customer(customer_id: str) -> Dict:
    response = table.get_item(Key={'customer_id': customer_id})
    return response.get('Item', {})
```

### Infrastructure as Code pour Lambda (Terraform)

```hcl
# Lambda function avec IAM role minimal
resource "aws_lambda_function" "api" {
  filename         = "lambda_package.zip"
  function_name    = "${var.env}-customer-api"
  role             = aws_iam_role.lambda_execution.arn
  handler          = "handler.handler"
  runtime          = "python3.11"
  timeout          = 30      # Secondes
  memory_size      = 256     # MB — ajuster après profiling
  source_code_hash = filebase64sha256("lambda_package.zip")

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.customers.name
      SECRET_ARN = aws_secretsmanager_secret.api_key.arn
      LOG_LEVEL  = var.env == "production" ? "INFO" : "DEBUG"
    }
  }

  # Logs dans CloudWatch
  depends_on = [aws_cloudwatch_log_group.lambda]

  # VPC si accès à des ressources privées (RDS, ElastiCache)
  # vpc_config {
  #   subnet_ids         = var.private_subnet_ids
  #   security_group_ids = [aws_security_group.lambda.id]
  # }

  tags = var.common_tags
}

# IAM role minimal (least privilege)
resource "aws_iam_role" "lambda_execution" {
  name = "${var.env}-lambda-api-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "lambda_dynamodb" {
  name = "dynamodb-access"
  role = aws_iam_role.lambda_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ]
        Resource = aws_dynamodb_table.customers.arn
      },
      {
        Effect   = "Allow"
        Action   = "secretsmanager:GetSecretValue"
        Resource = aws_secretsmanager_secret.api_key.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "${aws_cloudwatch_log_group.lambda.arn}:*"
      }
    ]
  })
}

# Provisioned concurrency pour éliminer le cold start (production)
resource "aws_lambda_provisioned_concurrency_config" "api" {
  count                             = var.env == "production" ? 1 : 0
  function_name                     = aws_lambda_function.api.function_name
  qualifier                         = aws_lambda_alias.live.name
  provisioned_concurrent_executions = 5  # 5 instances toujours chaudes
}
```

### Optimisation du Cold Start

```python
# Techniques pour réduire le cold start Lambda

# 1. Réduire la taille du package (moins de dépendances = cold start plus court)
# Utiliser des layers Lambda pour les dépendances volumineuses
# aws lambda publish-layer-version --layer-name pandas-numpy --zip-file fileb://layer.zip

# 2. Lazy imports — ne pas importer ce qui n'est pas toujours nécessaire
def handler(event, context):
    # Import au moment où c'est nécessaire, pas au chargement du module
    if event.get('action') == 'ml_predict':
        import xgboost  # Import conditionnel si pas toujours utilisé

# 3. Utiliser des runtimes avec cold start rapide
# Python 3.11 > Java 17 > Node.js 18 > .NET 8 (du plus rapide au plus lent)

# 4. Configurer SnapStart (Java) ou Provisioned Concurrency (tous runtimes)
# SnapStart : enregistre un snapshot après l'initialisation → cold start quasi-nul en Java

# 5. Garder les fonctions Lambda légères — les fonctions > 250MB ont un cold start long
# Viser < 50MB non compressé pour les fonctions Python

# 6. Utiliser /tmp pour le cache inter-invocations (512MB-10GB selon la config)
import os
import pickle

MODEL_PATH = '/tmp/model.pkl'

def load_or_cache_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    else:
        model = load_model_from_s3()
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        return model

# Le modèle est chargé une fois et mis en cache dans /tmp entre les invocations chaudes
model = load_or_cache_model()
```

---

## Google Cloud Run — Serverless Containers

### Pourquoi Cloud Run Plutôt que Lambda ?

Cloud Run exécute des conteneurs Docker arbitraires sans limite de langage ou de dépendances. Avantages vs Lambda :
- Pas de limite de 15 minutes (timeout jusqu'à 60 min)
- N'importe quel langage ou runtime
- Conteneurs Docker standard (facile à tester localement)
- Gestion des requêtes HTTP standard (pas de format event Lambda)
- Scale to zero (0 coût quand pas de trafic)

```dockerfile
# Dockerfile optimisé pour Cloud Run
FROM python:3.11-slim

# Réduire la taille de l'image (moins de packages = démarrage plus rapide)
RUN pip install --no-cache-dir fastapi uvicorn[standard] pydantic

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

# Cloud Run utilise la variable d'environnement PORT
ENV PORT=8080
EXPOSE 8080

# Uvicorn avec workers adaptatifs
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080",
     "--workers", "1", "--loop", "uvloop"]
```

```python
# src/main.py — FastAPI sur Cloud Run
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()

class PredictionRequest(BaseModel):
    customer_id: str
    features: dict

class PredictionResponse(BaseModel):
    customer_id: str
    churn_probability: float
    risk_level: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        proba = model.predict_proba([list(request.features.values())])[0][1]
        risk = "high" if proba > 0.7 else "medium" if proba > 0.4 else "low"

        return PredictionResponse(
            customer_id=request.customer_id,
            churn_probability=round(proba, 4),
            risk_level=risk
        )
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")
```

```bash
# Déploiement Cloud Run via gcloud
gcloud run deploy churn-api \
  --image europe-west1-docker.pkg.dev/mon-projet/apps/churn-api:v1.2.3 \
  --region europe-west1 \
  --platform managed \
  --min-instances 0 \          # Scale to zero
  --max-instances 100 \         # Max scaling
  --memory 512Mi \
  --cpu 1 \
  --timeout 30s \
  --concurrency 80 \            # Requêtes simultanées par instance
  --set-env-vars MODEL_VERSION=v3,LOG_LEVEL=INFO \
  --set-secrets MODEL_BUCKET=model-bucket-name:latest \
  --service-account churn-api-sa@mon-projet.iam.gserviceaccount.com \
  --no-allow-unauthenticated    # Requiert une authentification
```

---

## Architecture Event-Driven

### Patterns d'Architecture Événementielle

**Fan-out Pattern** : Un événement déclenche plusieurs traitements en parallèle.

```
[Source Event]
      |
[SNS / Pub/Sub]    ← Découplage
      |
  +---+---+---+
  |   |   |   |
[FaF][FaF][FaF]    ← Fonctions parallèles
```

```python
# Lambda fan-out : une Lambda publie vers SNS, plusieurs Lambdas écoutent
import boto3
import json

sns_client = boto3.client('sns')

def handler(event, context):
    # Publier l'événement vers SNS pour fan-out
    sns_client.publish(
        TopicArn=os.environ['ORDER_TOPIC_ARN'],
        Message=json.dumps({
            'order_id': event['order_id'],
            'customer_id': event['customer_id'],
            'amount': event['amount'],
            'event_type': 'ORDER_CREATED'
        }),
        MessageAttributes={
            'event_type': {
                'DataType': 'String',
                'StringValue': 'ORDER_CREATED'
            }
        }
    )
```

**Saga Pattern** : Orchestrer des transactions distribuées avec compensation en cas d'échec.

```python
# Step Functions pour orchestrer une saga
# Définir la state machine en JSON ou via AWS CDK
saga_definition = {
    "Comment": "Order fulfillment saga",
    "StartAt": "ReserveInventory",
    "States": {
        "ReserveInventory": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:...inventory-reserve",
            "Catch": [{
                "ErrorEquals": ["InventoryError"],
                "Next": "CancelOrder",
                "ResultPath": "$.error"
            }],
            "Next": "ProcessPayment"
        },
        "ProcessPayment": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:...payment-process",
            "Catch": [{
                "ErrorEquals": ["PaymentError"],
                "Next": "ReleaseInventory"
            }],
            "Next": "ShipOrder"
        },
        "ShipOrder": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:...shipping-create",
            "End": True
        },
        "ReleaseInventory": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:...inventory-release",
            "Next": "CancelOrder"
        },
        "CancelOrder": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:...order-cancel",
            "End": True
        }
    }
}
```

---

## Comparaison des Plateformes Serverless

### Functions as a Service

| Critère | AWS Lambda | Google Cloud Functions | Azure Functions |
|---|---|---|---|
| **Langages** | 9 runtimes officiels + conteneur | Python, Node, Go, Java, Ruby | C#, JavaScript, Python, Java, PowerShell |
| **Timeout max** | 15 minutes | 60 minutes (gen 2) | 230 secondes (HTTP), illimité (timer) |
| **Mémoire max** | 10 GB | 32 GB (gen 2) | 14 GB (Premium) |
| **Cold start** | 10ms-1s (Python) | 100ms-2s | 100ms-2s |
| **Concurrence** | 1000 par région (configurable) | 3000 par région | Illimitée (Premium) |
| **Triggers** | 200+ event sources | 20+ event sources | 30+ event sources |
| **Prix** | 0.20 USD/M invocations + compute | 0.40 USD/M invocations + compute | 0.20 USD/M invocations + compute |

### Containers Serverless

| Critère | Cloud Run (GCP) | AWS App Runner | Azure Container Apps |
|---|---|---|---|
| **Scale to zero** | Oui | Oui | Oui |
| **Cold start** | ~1-3s (image petite) | ~2-5s | ~2-5s |
| **Timeout** | 60 minutes | 120 secondes | 240 secondes |
| **Concurrence** | Configurable (1-1000 req/instance) | 1 req/container (par défaut) | Configurable |
| **VPC** | Oui (via Serverless VPC Connector) | Oui | Oui |
| **GPU** | Non (utiliser GKE Autopilot) | Non | Non |
| **Prix** | Pay-per-request + compute | Pay-per-compute | Pay-per-compute |
| **Recommandé pour** | APIs HTTP, ML serving, microservices | Applications simples AWS | Microservices Azure |

---

## Monitoring et Observabilité Serverless

### Métriques Clés à Monitorer

```python
# CloudWatch Metrics pour Lambda (via AWS SDK ou Terraform)
# Métriques standard (gratuites) :
# - Duration : durée d'exécution (P50, P95, P99)
# - Errors : nombre d'erreurs
# - Throttles : nombre de throttlings (concurrence dépassée)
# - Invocations : nombre total d'invocations
# - ConcurrentExecutions : concurrence simultanée

# Alarmes recommandées
import boto3

cw = boto3.client('cloudwatch')

# Alarme sur le taux d'erreur > 1%
cw.put_metric_alarm(
    AlarmName='lambda-api-error-rate',
    MetricName='Errors',
    Namespace='AWS/Lambda',
    Dimensions=[{'Name': 'FunctionName', 'Value': 'production-customer-api'}],
    Statistic='Sum',
    Period=300,       # 5 minutes
    EvaluationPeriods=2,
    Threshold=10,     # Plus de 10 erreurs sur 5 min
    ComparisonOperator='GreaterThanThreshold',
    AlarmActions=[os.environ['SNS_ALARM_ARN']]
)
```

### Structured Logging pour Serverless

```python
import json
import logging
import time

class JSONLogger:
    def __init__(self, function_name):
        self.function_name = function_name
        logging.basicConfig(level=logging.INFO)

    def info(self, message, **kwargs):
        self._log("INFO", message, **kwargs)

    def error(self, message, **kwargs):
        self._log("ERROR", message, **kwargs)

    def _log(self, level, message, **kwargs):
        log_entry = {
            "timestamp": time.time(),
            "level": level,
            "function": self.function_name,
            "message": message,
            **kwargs
        }
        print(json.dumps(log_entry))  # Lambda envoie stdout vers CloudWatch

logger = JSONLogger("customer-api")

def handler(event, context):
    start_time = time.time()

    logger.info("Request received",
                request_id=context.aws_request_id,
                path=event.get('path'),
                method=event.get('httpMethod'))

    result = process_request(event)

    logger.info("Request completed",
                request_id=context.aws_request_id,
                duration_ms=(time.time() - start_time) * 1000,
                status_code=result['statusCode'])

    return result
```

---

## Anti-Patterns Serverless Critiques

| Anti-Pattern | Description | Solution |
|---|---|---|
| **Lambda monolithique** | Une Lambda gère tout (routing, business logic, data access) | Séparer en Lambdas spécialisées avec responsabilité unique |
| **Synchronous chaining** | Lambda A appelle Lambda B qui appelle Lambda C en synchrone | Utiliser des queues (SQS, Pub/Sub) pour découpler |
| **Grand package Lambda** | Package Lambda > 250MB (toutes dépendances incluses) | Lambda Layers, multi-stage Docker, tree-shaking |
| **VPC sans NAT** | Lambda dans un VPC sans NAT Gateway ne peut pas accéder à internet | Configurer un NAT Gateway ou utiliser VPC endpoints |
| **Pas de dead letter queue** | Messages en échec silencieusement perdus | Configurer DLQ (SQS) pour toutes les Lambdas asynchrones |
| **Logs non structurés** | Logs texte non structuré, difficile à requêter | JSON structured logging systématique |
| **Concurrence non limitée** | Lambda scale à 1000+ et sature une base de données** | Configurer reserved concurrency et connection pooling (RDS Proxy) |
