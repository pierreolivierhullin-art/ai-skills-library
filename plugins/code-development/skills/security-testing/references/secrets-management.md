# Gestion des Secrets — Vault, Rotation et CI/CD

> Référence complète pour éliminer les secrets du code source, les centraliser dans des coffres-forts, et les faire tourner automatiquement sans interruption de service.

---

## Pourquoi les Secrets dans le Code sont Catastrophiques

### Exemples historiques documentés

**Uber (2016)** : Les credentials AWS étaient stockés dans un dépôt GitHub privé. Un attaquant y a accédé et a récupéré les données de 57 millions d'utilisateurs. Amende RGPD : 148 millions de dollars.

**Toyota (2023)** : Une clé d'API GitLab exposée dans un dépôt public pendant cinq ans a permis l'accès aux données de 296 000 clients.

**Twitch (2021)** : Des credentials de déploiement dans le code source ont facilité l'exfiltration de 125 Go de données dont le code source complet et les rémunérations des streamers.

**CircleCI (2022)** : Un token de session compromis dans leur pipeline CI a donné accès à tous les secrets des clients stockés dans le système.

### La règle fondamentale

```
Aucun secret ne doit jamais apparaître dans :
  - Le code source (même commenté)
  - Les messages de commit git
  - Les logs d'application ou de CI
  - Les images Docker (layers inclus)
  - Les fichiers de configuration versionnés (.env, config.yaml...)
  - Les variables d'environnement visibles (ps aux, /proc/1/environ)
```

---

## Détection des Secrets — Gitleaks et TruffleHog

### Gitleaks — Scan de l'historique git

```bash
# Installation
brew install gitleaks
# ou
docker pull zricethezav/gitleaks:latest

# Scan du dépôt courant (historique complet)
gitleaks detect --source . --verbose

# Scan d'un commit spécifique
gitleaks detect --source . --log-opts "HEAD~5..HEAD"

# Rapport JSON
gitleaks detect --source . --report-format json --report-path gitleaks-report.json

# Vérification du staged (utilisé en pre-commit hook)
gitleaks protect --staged --verbose
```

### Configuration Gitleaks custom

```toml
# .gitleaks.toml
title = "Gitleaks Custom Config"

[extend]
useDefault = true  # Hériter des règles par défaut

# Règles supplémentaires spécifiques à l'organisation
[[rules]]
id = "internal-api-key"
description = "Clé API interne - format ORG_sk_..."
regex = '''ORG_sk_[a-zA-Z0-9]{32}'''
severity = "CRITICAL"
tags = ["api-key", "internal"]

[[rules]]
id = "database-connection-string"
description = "Chaîne de connexion base de données"
regex = '''(postgresql|mysql|mongodb)://[^:]+:[^@]+@'''
severity = "CRITICAL"

# Exclusions légitimes
[[allowlist]]
description = "Tests et exemples de documentation"
regexes = [
  '''EXAMPLE_KEY_REPLACE_ME''',
  '''sk_test_[a-zA-Z0-9]{24}''',  # Clés Stripe de test
]
paths = [
  '''tests/.*''',
  '''docs/.*''',
  '''.*\.example$''',
]
```

### TruffleHog — Détection avec entropie

```bash
# Installation
brew install trufflehog

# Scan d'un dépôt GitHub (public ou privé avec token)
trufflehog github --repo https://github.com/org/repo --only-verified

# Scan de l'historique git local
trufflehog git file://. --since-commit HEAD~50 --only-verified

# Scan d'une image Docker (layers inclus)
trufflehog docker --image myapp:latest

# Scan d'un bucket S3
trufflehog s3 --bucket my-bucket --only-verified

# Intégration CI — output JSON
trufflehog git file://. --json --only-verified 2>&1 | tee trufflehog-report.json
```

### Configuration pre-commit hooks

```yaml
# .pre-commit-config.yaml
repos:
  # Gitleaks — scan des secrets
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks
        name: Detect Secrets (Gitleaks)
        description: Détecte les secrets dans le code avant le commit

  # detect-secrets — approche par liste blanche
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        name: Detect Secrets (baseline)
        args: ['--baseline', '.secrets.baseline']
        exclude: package.lock.json

  # Vérification générale des bonnes pratiques
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
        args: ['--maxkb=1024']
      - id: detect-private-key
      - id: check-merge-conflict
```

```bash
# Installation des hooks
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg

# Générer la baseline (secrets connus/acceptés)
detect-secrets scan > .secrets.baseline

# Mise à jour de la baseline après révision
detect-secrets audit .secrets.baseline
```

---

## GitHub Secret Scanning

### Configuration dans le dépôt

```yaml
# Dans GitHub → Settings → Security → Code security and analysis :
# ✅ Secret scanning : activé
# ✅ Push protection : activé (bloque le push si secret détecté)
# ✅ Validity checks : activé (vérifie si le secret est encore actif)

# Partenaires de détection intégrés (70+) :
# AWS Access Keys, GCP credentials, Azure connection strings,
# Stripe API keys, Twilio, Slack, GitHub tokens, npm tokens...
```

### Gestion des alertes Secret Scanning

```bash
# Via GitHub CLI — lister les alertes actives
gh secret-scanning list-alerts --repo org/repo --state open

# Voir le détail d'une alerte
gh api repos/org/repo/secret-scanning/alerts/1

# Résoudre une alerte (après révocation + rotation)
gh api repos/org/repo/secret-scanning/alerts/1 \
  --method PATCH \
  -f state=resolved \
  -f resolution=revoked
```

---

## HashiCorp Vault — Coffre-fort Centralisé

### Architecture et concepts clés

```
Vault Architecture :
  ├── Auth Methods : AppRole, OIDC, Kubernetes, AWS IAM
  ├── Secrets Engines : KV, Database, PKI, AWS, Transit
  ├── Policies : contrôle d'accès fine-grained
  └── Audit Logs : traçabilité complète de chaque accès
```

### KV Secrets Engine (version 2)

```bash
# Activer le KV v2
vault secrets enable -path=secret kv-v2

# Créer un secret
vault kv put secret/myapp/production \
  db_password="$(openssl rand -base64 32)" \
  api_key="$(openssl rand -hex 32)"

# Lire un secret
vault kv get secret/myapp/production

# Lister les versions
vault kv metadata get secret/myapp/production

# Restaurer une version précédente
vault kv rollback -version=2 secret/myapp/production

# Politique d'accès en lecture seule
vault policy write myapp-read - <<EOF
path "secret/data/myapp/production" {
  capabilities = ["read"]
}
path "secret/metadata/myapp/production" {
  capabilities = ["list", "read"]
}
EOF
```

### Dynamic Secrets — Base de données

```bash
# Activer le secrets engine Database
vault secrets enable database

# Configurer la connexion PostgreSQL
vault write database/config/my-postgresql \
  plugin_name=postgresql-database-plugin \
  allowed_roles="myapp-role" \
  connection_url="postgresql://{{username}}:{{password}}@db.example.com:5432/mydb" \
  username="vault" \
  password="vault-root-password"

# Créer un rôle avec TTL court
vault write database/roles/myapp-role \
  db_name=my-postgresql \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Générer des credentials temporaires
vault read database/creds/myapp-role
# Key      Value
# username v-appro-myapp-role-AbCdEf123456
# password A1b2C3d4E5f6...
# lease_duration 1h
```

### AppRole Auth — pour les applications

```bash
# Activer AppRole
vault auth enable approle

# Créer un rôle applicatif
vault write auth/approle/role/myapp \
  token_policies="myapp-read" \
  token_ttl="15m" \
  token_max_ttl="1h" \
  secret_id_ttl="24h" \
  secret_id_num_uses=10

# Récupérer les credentials AppRole
ROLE_ID=$(vault read -field=role_id auth/approle/role/myapp/role-id)
SECRET_ID=$(vault write -field=secret_id -f auth/approle/role/myapp/secret-id)

# S'authentifier et obtenir un token
vault write auth/approle/login role_id=$ROLE_ID secret_id=$SECRET_ID
```

### PKI — Certificats TLS dynamiques

```bash
# Activer le PKI secrets engine
vault secrets enable pki
vault secrets tune -max-lease-ttl=87600h pki

# Générer le CA racine
vault write -field=certificate pki/root/generate/internal \
  common_name="example.com" \
  ttl=87600h > CA_cert.crt

# Configurer les endpoints CRL/OCSP
vault write pki/config/urls \
  issuing_certificates="https://vault.example.com/v1/pki/ca" \
  crl_distribution_points="https://vault.example.com/v1/pki/crl"

# Créer un rôle pour émettre des certificats
vault write pki/roles/example-dot-com \
  allowed_domains="example.com,*.example.com" \
  allow_subdomains=true \
  max_ttl=72h

# Émettre un certificat
vault write pki/issue/example-dot-com \
  common_name="api.example.com" \
  ttl=24h
```

### Intégration Node.js avec Vault

```typescript
import Vault from 'node-vault';

const vault = Vault({
  apiVersion: 'v1',
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN, // Pour le développement local uniquement
});

// Authentification AppRole pour la production
async function getVaultToken(): Promise<string> {
  const result = await vault.approleLogin({
    role_id: process.env.VAULT_ROLE_ID!,
    secret_id: process.env.VAULT_SECRET_ID!,
  });
  return result.auth.client_token;
}

// Récupérer des secrets avec cache local et renouvellement
class SecretManager {
  private cache = new Map<string, { value: string; expiresAt: number }>();

  async getSecret(path: string, key: string): Promise<string> {
    const cacheKey = `${path}:${key}`;
    const cached = this.cache.get(cacheKey);

    if (cached && cached.expiresAt > Date.now()) {
      return cached.value;
    }

    const result = await vault.read(path);
    const value = result.data.data[key];

    // Cache avec TTL de 5 minutes (renouvellement avant expiration)
    this.cache.set(cacheKey, {
      value,
      expiresAt: Date.now() + 5 * 60 * 1000,
    });

    return value;
  }
}

// Usage au démarrage de l'application
const secretManager = new SecretManager();
const dbPassword = await secretManager.getSecret('secret/data/myapp/production', 'db_password');
```

### Intégration Python avec Vault

```python
import hvac
import os
from functools import lru_cache

client = hvac.Client(url=os.environ['VAULT_ADDR'])

# Authentification Kubernetes (depuis un pod)
def authenticate_k8s():
    with open('/var/run/secrets/kubernetes.io/serviceaccount/token') as f:
        jwt_token = f.read()
    client.auth.kubernetes.login(
        role='myapp-role',
        jwt=jwt_token,
    )

@lru_cache(maxsize=None)
def get_secret(path: str, key: str) -> str:
    """Récupère un secret depuis Vault avec cache en mémoire."""
    secret = client.secrets.kv.v2.read_secret_version(path=path)
    return secret['data']['data'][key]

# Usage
db_password = get_secret('myapp/production', 'db_password')
```

---

## AWS Secrets Manager

### Création et rotation de secrets

```bash
# Créer un secret
aws secretsmanager create-secret \
  --name "myapp/production/database" \
  --description "Credentials base de données production" \
  --secret-string '{"username":"myapp","password":"<generated>"}' \
  --tags '[{"Key":"Environment","Value":"production"},{"Key":"Application","Value":"myapp"}]'

# Rotation automatique avec Lambda
aws secretsmanager rotate-secret \
  --secret-id "myapp/production/database" \
  --rotation-lambda-arn "arn:aws:lambda:eu-west-1:123456789:function:SecretsRotation" \
  --rotation-rules '{"AutomaticallyAfterDays": 30}'
```

### Lambda de rotation (PostgreSQL)

```python
import boto3
import psycopg2
import json
import secrets
import string

def lambda_handler(event, context):
    """Fonction de rotation pour les credentials PostgreSQL."""
    secret_id = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    client = boto3.client('secretsmanager')

    if step == 'createSecret':
        # Générer un nouveau mot de passe
        new_password = generate_password(32)
        client.put_secret_value(
            SecretId=secret_id,
            ClientRequestToken=token,
            SecretString=json.dumps({**get_current_secret(client, secret_id), 'password': new_password}),
            VersionStages=['AWSPENDING'],
        )

    elif step == 'setSecret':
        # Appliquer le nouveau mot de passe en base
        current = get_current_secret(client, secret_id)
        pending = get_pending_secret(client, secret_id, token)
        conn = psycopg2.connect(
            host=current['host'], dbname=current['dbname'],
            user=current['username'], password=current['password'],
        )
        with conn.cursor() as cur:
            cur.execute(f"ALTER USER {pending['username']} WITH PASSWORD %s", (pending['password'],))
        conn.commit()

    elif step == 'testSecret':
        # Vérifier que le nouveau mot de passe fonctionne
        pending = get_pending_secret(client, secret_id, token)
        conn = psycopg2.connect(
            host=pending['host'], dbname=pending['dbname'],
            user=pending['username'], password=pending['password'],
        )
        conn.close()

    elif step == 'finishSecret':
        # Marquer la version comme active
        client.update_secret_version_stage(
            SecretId=secret_id,
            VersionStage='AWSCURRENT',
            MoveToVersionId=token,
        )

def generate_password(length: int) -> str:
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(chars) for _ in range(length))
```

### Accès depuis ECS avec IAM Task Role

```json
// Politique IAM pour la task ECS
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": [
        "arn:aws:secretsmanager:eu-west-1:123456789:secret:myapp/production/*"
      ]
    }
  ]
}
```

```typescript
// Accès depuis Node.js avec SDK AWS (credentials automatiques depuis le task role)
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'eu-west-1' });

async function getSecret(secretName: string): Promise<Record<string, string>> {
  const command = new GetSecretValueCommand({ SecretId: secretName });
  const response = await client.send(command);

  if (response.SecretString) {
    return JSON.parse(response.SecretString);
  }
  throw new Error('Secret non disponible');
}

// Au démarrage de l'application
const dbCreds = await getSecret('myapp/production/database');
const pool = new Pool({
  host: dbCreds.host,
  user: dbCreds.username,
  password: dbCreds.password,
  database: dbCreds.dbname,
});
```

### CDK — Infrastructure as Code pour Secrets Manager

```typescript
import * as cdk from 'aws-cdk-lib';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as rds from 'aws-cdk-lib/aws-rds';

// Créer un secret avec rotation automatique
const dbSecret = new secretsmanager.Secret(this, 'DatabaseSecret', {
  secretName: 'myapp/production/database',
  generateSecretString: {
    secretStringTemplate: JSON.stringify({ username: 'myapp' }),
    generateStringKey: 'password',
    excludePunctuation: true,
    passwordLength: 32,
  },
  replicaRegions: [{ region: 'us-east-1' }], // Réplication multi-région
});

// Attacher la rotation automatique (via SingleUser rotation Lambda)
const db = new rds.DatabaseInstance(this, 'Database', { /* ... */ });
db.addRotationSingleUser({ automaticallyAfter: cdk.Duration.days(30) });
```

---

## Variables d'Environnement — Bonnes Pratiques

### Hiérarchie des solutions

```
Moins sécurisé  ────────────────────────────────  Plus sécurisé

.env en clair → .env chiffré (dotenv-vault) → Injection 1Password → Vault/AWS SM
```

### dotenv-vault — .env chiffré dans le dépôt

```bash
# Installation
npm install --save-dev dotenv-vault

# Initialiser (crée le compte sur dotenv.org)
npx dotenv-vault new

# Pousser les secrets (chiffrement AES-256)
npx dotenv-vault push

# Créer un .env pour la CI/CD (DOTENV_KEY récupéré depuis le dashboard)
# Le .env chiffré (.env.vault) peut être commité en toute sécurité
echo "DOTENV_KEY=dotenv://:key_abc123..." >> .env.production

# Dans le code
import 'dotenv/config'; // Déchiffre automatiquement si DOTENV_KEY est présent
```

### 1Password CLI — Injection de secrets

```bash
# Installation
brew install 1password-cli

# Authentification
op signin

# Injection dans une commande
op run --env-file=.env.1password -- node server.js

# .env.1password (fichier de mapping, committé)
DB_PASSWORD=op://Production/Database/password
API_KEY=op://Production/Stripe/api_key
JWT_SECRET=op://Production/JWT/secret
```

---

## Doppler — Gestion des Secrets en Équipe

```bash
# Installation
brew install dopplerhq/cli/doppler

# Authentification et configuration
doppler login
doppler setup --project myapp --config production

# Injecter les secrets dans l'application
doppler run -- node server.js

# Synchronisation vers GitHub Actions
doppler secrets download --project myapp --config ci --format env > /dev/null
# Ou utiliser le GitHub Action officiel Doppler

# Intégration Kubernetes — Doppler Operator
kubectl apply -f https://github.com/DopplerHQ/kubernetes-operator/releases/latest/download/recommended.yaml
```

```yaml
# kubernetes-secret.yml — Doppler Kubernetes Operator
apiVersion: secrets.doppler.com/v1alpha1
kind: DopplerSecret
metadata:
  name: myapp-secrets
  namespace: production
spec:
  tokenSecret:
    name: doppler-token-secret  # Secret K8s contenant le token Doppler
  managedSecret:
    name: myapp-env             # Secret K8s créé/mis à jour automatiquement
    namespace: production
  config: production
  project: myapp
```

---

## Playbook de Rotation — Zéro Downtime

### Stratégie de rotation blue-green

```
Phase 1 — Préparation (J-7)
  ├── Identifier tous les consommateurs du secret
  ├── Vérifier que l'application peut charger les secrets au runtime (pas au démarrage uniquement)
  └── Tester la rotation en staging

Phase 2 — Double validité (J0, étape 1)
  ├── Générer le nouveau secret dans le coffre-fort
  ├── Configurer le service cible pour accepter ANCIEN et NOUVEAU (dual-write période)
  └── Déployer sans rotation — vérifier que tout fonctionne

Phase 3 — Bascule progressive (J0, étape 2)
  ├── Recharger les applications (rolling restart sans downtime)
  ├── Vérifier les métriques d'erreur pendant 15 minutes
  └── Si erreur : rollback immédiat vers l'ancien secret

Phase 4 — Révocation (J0 + 1h)
  ├── Révoquer l'ancien secret dans le service cible
  ├── Archiver l'ancien secret dans le coffre avec statut 'deprecated'
  └── Mettre à jour la documentation
```

### Script de rotation Node.js

```typescript
async function rotateSecret(secretPath: string, rotationFn: () => Promise<string>) {
  const logger = getLogger();
  const metrics = getMetrics();

  logger.info(`Début rotation secret : ${secretPath}`);

  // 1. Générer le nouveau secret
  const newSecret = await rotationFn();

  // 2. Stocker dans Vault avec deux versions actives
  await vault.write(`${secretPath}`, { value: newSecret });

  // 3. Recharger les applications (exemple : rolling restart K8s)
  await kubectl.rolloutRestart('deployment/myapp');
  await kubectl.rolloutStatus('deployment/myapp', { timeout: 300 });

  // 4. Vérifier la santé après rotation
  const healthCheck = await fetch('https://api.example.com/health');
  if (!healthCheck.ok) {
    logger.error('Health check échoué après rotation — rollback');
    await vault.write(`${secretPath}`, { value: oldSecret }); // Restauration
    throw new Error('Rotation annulée : health check failed');
  }

  // 5. Révoquer l'ancienne version
  await vault.delete(`${secretPath}`, { version: previousVersion });

  metrics.increment('secret.rotation.success', { path: secretPath });
  logger.info(`Rotation réussie : ${secretPath}`);
}
```

---

## Scan des Secrets dans les Images Docker

### Dive — Inspection des layers

```bash
# Installation
brew install dive

# Analyser les layers d'une image
dive myapp:latest

# Mode CI — échoue si des fichiers potentiellement secrets sont trouvés
CI=true dive myapp:latest --ci-config .dive-ci.yml
```

```yaml
# .dive-ci.yml
rules:
  lowestEfficiency: 0.9    # Efficacité minimum des layers
  highestWastedBytes: 20MB # Bytes gaspillés maximum
  highestUserWastedPercent: 0.20
```

```bash
# Recherche manuelle de secrets dans les layers Docker
docker save myapp:latest | tar -xO --wildcards '*/layer.tar' | \
  tar -tv | grep -E '\.(env|pem|key|p12|pfx)$'

# Mieux : utiliser Trivy pour les secrets dans les images
trivy image --security-checks secret myapp:latest
```

---

## GitHub Actions — OIDC Federation (Zéro Secret)

### Principe — Plus de secrets dans GitHub Actions

```yaml
# Au lieu de stocker AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY dans les secrets GitHub,
# utiliser OIDC pour obtenir des credentials temporaires directement depuis AWS.

# .github/workflows/deploy.yml
name: Deploy with OIDC (pas de secrets AWS stockés)

on:
  push:
    branches: [main]

permissions:
  id-token: write  # Requis pour OIDC
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/github-actions-deploy
          aws-region: eu-west-1
          # Pas de access key ou secret key — credentials temporaires via OIDC !

      - name: Deploy
        run: aws s3 sync dist/ s3://my-bucket/
```

### Configuration AWS pour OIDC

```bash
# Créer le provider OIDC dans AWS
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1

# Politique de confiance du rôle IAM
cat > trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:org/myrepo:ref:refs/heads/main"
        }
      }
    }
  ]
}
EOF

aws iam create-role \
  --role-name github-actions-deploy \
  --assume-role-policy-document file://trust-policy.json
```

### GitHub Actions — Secrets vs Environment Secrets

```yaml
# Hiérarchie des secrets GitHub Actions (du moins au plus sécurisé) :

# 1. Repository secrets — visibles par tous les workflows et branches
#    Utiliser pour les secrets non-sensibles à l'environnement

# 2. Environment secrets — limités à un environnement spécifique
#    Nécessitent une approbation manuelle pour les déploiements production
jobs:
  deploy-production:
    environment:
      name: production
      url: https://example.com
    # Les secrets de l'environnement "production" ne sont disponibles
    # qu'ici, après approbation des reviewers configurés
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.PROD_API_KEY }}  # Secret d'environnement
        run: ./deploy.sh

# 3. OIDC Federation — recommandé pour les credentials cloud (pas de secret du tout)
```

---

## Récapitulatif — Décisions d'Architecture

| Contexte | Solution recommandée | Raison |
|----------|---------------------|--------|
| Dev local (équipe) | Doppler ou 1Password CLI | Synchronisation d'équipe, pas de .env partagé |
| CI/CD (GitHub) | GitHub Env Secrets + OIDC | OIDC pour cloud, secrets chiffrés pour le reste |
| Application (K8s) | HashiCorp Vault + Vault Agent | Rotation automatique, audit complet |
| Application (AWS) | AWS Secrets Manager + Task Role | Intégration native, rotation managée |
| Startup / petite équipe | Doppler | Simple, multiplateforme, rotation intégrée |
| Audit et conformité | HashiCorp Vault Enterprise | Audit logs, namespace isolation |

**Règle absolue** : si un secret apparaît dans `git log --all -p`, il est compromis. Révoquer immédiatement, puis nettoyer l'historique avec `git-filter-repo` et forcer une rotation de tous les accès.
