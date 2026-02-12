# Secrets Management

Reference complete pour la gestion securisee des secrets applicatifs (2024-2026). Couvre le stockage de secrets, la rotation de cles, la gestion des certificats, le scanning en CI/CD, et l'architecture zero-trust pour les secrets.

---

## Principes fondamentaux

### Qu'est-ce qu'un secret ?

Un secret est toute donnee dont la divulgation compromettrait la securite du systeme :

- Cles API (tierces et internes)
- Credentials de base de donnees (username/password, connection strings)
- Tokens d'acces (OAuth, service accounts)
- Certificats TLS et cles privees
- Cles de chiffrement (encryption keys, signing keys)
- Webhooks secrets et signing keys
- Credentials de services cloud (AWS access keys, GCP service account keys)
- SSH keys
- Passphrases et master keys de secret managers

### Regles absolues

1. **Ne jamais commiter de secrets dans le code source** — Aucune exception. Meme dans des branches "temporaires" ou des repos "prives".
2. **Ne jamais logger de secrets** — Masquer les secrets dans tous les outputs de logs, meme en mode debug.
3. **Ne jamais transmettre de secrets en clair** — Toujours utiliser des canaux chiffres (TLS).
4. **Ne jamais partager de secrets par email, Slack, ou autre canal non securise** — Utiliser un secret manager ou un outil de partage ephemere (1Password, Vault).
5. **Toujours avoir un plan de rotation** — Chaque secret doit pouvoir etre revoque et remplace sans downtime.

---

## Secret Managers — Solutions

### HashiCorp Vault

Le standard de l'industrie pour la gestion de secrets en entreprise.

**Architecture :**

```
[Application] -> [Vault Agent/Sidecar] -> [Vault Server]
                                               |
                              [Storage Backend: Raft, Consul, etc.]
                                               |
                              [Auth Methods: Kubernetes, AWS IAM, AppRole, etc.]
```

**Fonctionnalites cles :**

- **Dynamic Secrets** : Generer des credentials ephemeres a la demande (database credentials, AWS credentials, PKI certificates). Chaque application recoit ses propres credentials avec un TTL court.
- **Secret Engines** : KV (key-value), Database, PKI, Transit (encryption-as-a-service), SSH, AWS, GCP, Azure.
- **Auth Methods** : Kubernetes service account, AWS IAM, AppRole, OIDC/JWT, LDAP, certificate-based.
- **Policies** : Controle d'acces granulaire base sur des paths et des capabilities.
- **Audit** : Logging detaille de chaque acces a un secret.
- **Lease & Renewal** : Chaque secret a un TTL et peut etre renouvele ou revoque.

**Implementation Dynamic Database Secrets :**

```hcl
# Configurer le secret engine database
resource "vault_database_secrets_mount" "db" {
  path = "database"

  postgresql {
    name              = "myapp-db"
    connection_url    = "postgresql://{{username}}:{{password}}@db.example.com:5432/myapp"
    allowed_roles     = ["app-readonly", "app-readwrite"]
    root_rotation_statements = ["ALTER USER \"{{name}}\" WITH PASSWORD '{{password}}'"]
  }
}

# Role pour l'application (readonly)
resource "vault_database_secret_backend_role" "app_readonly" {
  backend = vault_database_secrets_mount.db.path
  name    = "app-readonly"
  db_name = "myapp-db"

  creation_statements = [
    "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';",
    "GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";",
  ]

  revocation_statements = [
    "DROP ROLE IF EXISTS \"{{name}}\";",
  ]

  default_ttl = "1h"
  max_ttl     = "24h"
}
```

**Acces depuis l'application (Node.js) :**

```typescript
import vault from 'node-vault';

const vaultClient = vault({
  apiVersion: 'v1',
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN, // ou auth Kubernetes
});

// Lire un secret statique
const { data } = await vaultClient.read('secret/data/myapp/config');
const apiKey = data.data.api_key;

// Obtenir des credentials dynamiques de base de donnees
const dbCreds = await vaultClient.read('database/creds/app-readonly');
const { username, password, lease_id, lease_duration } = dbCreds.data;

// Renouveler le lease avant expiration
setTimeout(async () => {
  await vaultClient.write('sys/leases/renew', { lease_id });
}, (lease_duration - 60) * 1000); // Renouveler 60s avant expiration
```

### AWS Secrets Manager

Solution managee pour les environnements AWS.

**Fonctionnalites cles :**

- Rotation automatique via Lambda functions
- Integration native avec RDS, Redshift, DocumentDB
- Chiffrement avec AWS KMS
- Versioning des secrets
- Cross-account sharing via resource policies

**Implementation rotation automatique :**

```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'eu-west-1' });

async function getSecret(secretName: string): Promise<Record<string, string>> {
  const response = await client.send(
    new GetSecretValueCommand({
      SecretId: secretName,
      VersionStage: 'AWSCURRENT',
    })
  );
  return JSON.parse(response.SecretString!);
}

// Utilisation avec cache
import { createSecretCache } from '@aws-sdk/client-secrets-manager';

const secretCache = createSecretCache({
  client,
  cacheItemTTL: 300000, // 5 minutes de cache
});

const dbSecret = await secretCache.getSecretValue('myapp/database');
```

**Configuration Terraform pour rotation automatique :**

```hcl
resource "aws_secretsmanager_secret" "db_credentials" {
  name                    = "myapp/database"
  recovery_window_in_days = 7

  tags = {
    Environment = "production"
    Application = "myapp"
  }
}

resource "aws_secretsmanager_secret_rotation" "db_rotation" {
  secret_id           = aws_secretsmanager_secret.db_credentials.id
  rotation_lambda_arn = aws_lambda_function.secret_rotation.arn

  rotation_rules {
    automatically_after_days = 30
    schedule_expression      = "rate(30 days)"
  }
}
```

### GCP Secret Manager

Solution managee pour les environnements Google Cloud.

**Fonctionnalites cles :**

- Versioning natif des secrets
- IAM granulaire au niveau du secret individuel
- Chiffrement avec Cloud KMS (CMEK supporte)
- Replication configurable (automatique ou user-managed)
- Integration native avec Cloud Run, GKE, Cloud Functions

**Implementation :**

```typescript
import { SecretManagerServiceClient } from '@google-cloud/secret-manager';

const client = new SecretManagerServiceClient();

async function getSecret(secretName: string): Promise<string> {
  const [version] = await client.accessSecretVersion({
    name: `projects/my-project/secrets/${secretName}/versions/latest`,
  });
  return version.payload!.data!.toString();
}
```

### Comparaison des solutions

| Critere | Vault | AWS Secrets Manager | GCP Secret Manager | Azure Key Vault |
|---------|-------|--------------------|--------------------|-----------------|
| **Type** | Self-hosted / HCP | Managed | Managed | Managed |
| **Dynamic secrets** | Natif (DB, AWS, PKI) | Via Lambda | Non natif | Non natif |
| **Rotation automatique** | Natif | Natif (RDS, etc.) | Manuelle/custom | Natif (limité) |
| **Multi-cloud** | Oui | AWS only | GCP only | Azure only |
| **Encryption-as-a-service** | Transit engine | KMS | Cloud KMS | Key Vault |
| **Pricing** | Infra (ou HCP) | Par secret + par acces | Par version + par acces | Par operation |
| **Ideal pour** | Multi-cloud, on-prem | AWS-native | GCP-native | Azure-native |

---

## API Key Management

### Design de cles API

**Structure recommandee :**

```
Prefixe visible + partie secrete

Format : {prefix}_{environment}_{random}
Exemple : sk_live_EXAMPLE_KEY_REPLACE_ME_1234567890

Conventions :
  sk_ = secret key (cote serveur uniquement)
  pk_ = public key (cote client, safe to expose)
  wh_ = webhook secret
  _live_ = production
  _test_ = staging/test
```

Le prefixe permet d'identifier rapidement le type et l'environnement sans exposer la partie secrete. Facilite aussi le scanning automatique de secrets.

### Stockage et hachage

Ne jamais stocker les cles API en clair en base de donnees. Appliquer le meme traitement que pour les mots de passe :

```typescript
import { createHash, randomBytes, timingSafeEqual } from 'crypto';

// Generation
function generateApiKey(): { key: string; hash: string; prefix: string } {
  const random = randomBytes(32).toString('hex');
  const prefix = `sk_live_${random.slice(0, 8)}`;
  const key = `sk_live_${random}`;
  const hash = createHash('sha256').update(key).digest('hex');
  return { key, hash, prefix };
}

// Stockage en base : stocker hash + prefix (pour lookup)
// Afficher key a l'utilisateur UNE SEULE FOIS a la creation

// Verification
function verifyApiKey(providedKey: string, storedHash: string): boolean {
  const providedHash = createHash('sha256').update(providedKey).digest('hex');
  return timingSafeEqual(Buffer.from(providedHash), Buffer.from(storedHash));
}
```

### Rotation de cles API

Implementer un processus de rotation sans downtime :

```
1. Generer une nouvelle cle (version N+1)
2. L'ancienne cle (version N) reste active pendant une periode de grace
3. Notifier le proprietaire de la cle de la rotation imminente
4. Apres la periode de grace, desactiver l'ancienne cle
5. Logger l'utilisation des anciennes cles pour identifier les clients non migres
```

**Schema pour supporter la rotation :**

```sql
CREATE TABLE api_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) NOT NULL,
  prefix TEXT NOT NULL,             -- 'sk_live_a3f8b2c9' (pour lookup rapide)
  key_hash TEXT NOT NULL,           -- SHA-256 de la cle complete
  name TEXT,                        -- 'Production API Key'
  scopes TEXT[] DEFAULT '{}',       -- Permissions de la cle
  environment TEXT NOT NULL,        -- 'live', 'test'
  status TEXT DEFAULT 'active',     -- 'active', 'rotating', 'revoked'
  expires_at TIMESTAMPTZ,           -- Expiration optionnelle
  last_used_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now(),
  revoked_at TIMESTAMPTZ,
  revoked_reason TEXT
);

CREATE INDEX idx_api_keys_prefix ON api_keys(prefix) WHERE status = 'active';
```

---

## Environment Variable Management

### Hierarchie des configurations

```
Priorite (haute -> basse) :
  1. Secret Manager (Vault, AWS SM, etc.) — secrets sensibles
  2. Variables d'environnement du runtime — configuration specifique au deploiement
  3. Fichiers de configuration — valeurs par defaut, non-secrets
  4. Valeurs par defaut dans le code — fallback ultime (jamais pour les secrets)
```

### Bonnes pratiques

- **Separer secrets et configuration** : Les secrets vont dans un secret manager. La configuration non-sensible (feature flags, URLs, thresholds) peut rester en variables d'environnement.
- **Ne jamais utiliser `.env` en production** : Les fichiers `.env` sont pour le developpement local uniquement. En production, utiliser le secret manager ou les variables d'environnement injectees par le runtime (Kubernetes secrets, ECS task definition, etc.).
- **Valider les variables au demarrage** : Verifier la presence et le format de toutes les variables requises au boot de l'application. Echouer immediatement si une variable critique manque.

```typescript
import { z } from 'zod';

const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  OAUTH_CLIENT_ID: z.string().min(1),
  OAUTH_CLIENT_SECRET: z.string().min(1),
  ALLOWED_ORIGINS: z.string().transform(s => s.split(',')),
  PORT: z.string().transform(Number).pipe(z.number().int().positive()),
});

// Valider au demarrage — crash si invalide
export const env = EnvSchema.parse(process.env);
```

### `.env` files — Regles de securite

- Ajouter `.env` et `.env.*` au `.gitignore` (sauf `.env.example`)
- Maintenir un `.env.example` avec les noms de variables (sans les valeurs reelles)
- Ne jamais utiliser `.env.production` avec des secrets reels dans le repo
- Pour le dev local, utiliser `.env.local` (non commite)

```bash
# .gitignore
.env
.env.*
!.env.example
```

---

## Certificate Management (TLS)

### Strategie TLS

- **Toujours utiliser TLS 1.2 ou 1.3** — Desactiver TLS 1.0 et 1.1
- **Preferer TLS 1.3** — Plus rapide (1-RTT handshake), plus securise (ciphersuites simplifiees)
- **HSTS preload** — Soumettre le domaine a la preload list pour forcer HTTPS dans tous les navigateurs

### Let's Encrypt — Automatisation

Automatiser l'emission et le renouvellement des certificats avec Let's Encrypt :

**Avec certbot (standalone) :**

```bash
# Emission initiale
certbot certonly --standalone -d example.com -d www.example.com --agree-tos --email admin@example.com

# Renouvellement automatique (cron)
0 0 1 * * certbot renew --quiet --post-hook "systemctl reload nginx"
```

**Avec cert-manager (Kubernetes) :**

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
      - http01:
          ingress:
            class: nginx

---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: myapp-tls
  namespace: production
spec:
  secretName: myapp-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - app.example.com
    - api.example.com
  renewBefore: 720h  # Renouveler 30 jours avant expiration
```

### mTLS (Mutual TLS) pour les microservices

Implementer mTLS pour l'authentification mutuelle entre services :

```
Service A <--mTLS--> Service B

Chaque service possede :
  - Un certificat client signe par la CA interne
  - La CA root pour verifier les certificats des autres services
  - Le serveur exige le certificat client (verify_client=on)
```

**Service mesh (Istio) pour mTLS automatique :**

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT  # Forcer mTLS pour toutes les communications
```

L'avantage du service mesh : les certificats sont generes, distribues et renouveles automatiquement. L'application n'a pas a gerer les certificats.

---

## Secrets Scanning in CI/CD

### Outils de scanning

| Outil | Type | Detection | Integration | Specialite |
|-------|------|-----------|-------------|-----------|
| **GitGuardian** | SaaS | Pre-commit + CI + monitoring | GitHub, GitLab, CI/CD | Monitoring continu, dashboard |
| **TruffleHog** | Open-source | Pre-commit + CI | Git, GitHub Actions | Entropy + regex, verification active |
| **Gitleaks** | Open-source | Pre-commit + CI | Git, GitHub Actions | Rapide, configurable |
| **detect-secrets** | Open-source (Yelp) | Pre-commit | Git | Baseline approach, low FP |
| **GitHub Secret Scanning** | GitHub natif | Push protection | GitHub | Natif, alerts automatiques |

### Implementation multi-couches

**Layer 1 : Pre-commit hook (developer workstation)**

```bash
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
        args: ['--config', '.gitleaks.toml']

  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.63.0
    hooks:
      - id: trufflehog
        args: ['--only-verified', '--fail']
```

**Layer 2 : CI/CD pipeline (bloquant)**

```yaml
# GitHub Actions
- name: TruffleHog Scan
  uses: trufflesecurity/trufflehog@main
  with:
    extra_args: --only-verified --fail

- name: Gitleaks Scan
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Layer 3 : Monitoring continu (post-merge)**

Configurer GitGuardian ou GitHub Secret Scanning pour monitorer en continu le repository et alerter sur tout secret detecte, meme dans l'historique Git.

### Configuration Gitleaks

```toml
# .gitleaks.toml
[extend]
useDefault = true

[[rules]]
id = "custom-api-key"
description = "Custom API Key pattern"
regex = '''(?i)(sk_live_|pk_live_|wh_)[a-z0-9]{32,}'''
tags = ["key", "custom"]

[allowlist]
paths = [
  '''\.env\.example$''',
  '''tests/fixtures/''',
  '''docs/examples/''',
]
```

### Procedure en cas de secret commite

Reagir immediatement si un secret est detecte dans le code :

```
1. REVOQUER le secret immediatement (ne pas attendre)
2. Generer un nouveau secret
3. Deployer la mise a jour avec le nouveau secret
4. Investiguer : determiner si le secret a ete exploite (verifier les logs d'acces)
5. Nettoyer l'historique Git si necessaire (git filter-repo)
6. Post-mortem : identifier la cause root et ameliorer les controles
```

Attention : Meme apres suppression du commit, le secret reste dans l'historique Git et dans les caches de GitHub/GitLab. La revocation est la seule mesure fiable.

---

## Zero-Trust Secrets Architecture

### Principes

L'approche zero-trust pour les secrets repose sur :

1. **Identite machine verifiee** : Chaque workload prouve son identite avant d'acceder aux secrets (Kubernetes service account, AWS IAM role, SPIFFE identity).
2. **Secrets ephemeres** : Preferer les secrets a duree de vie courte (dynamic secrets) aux secrets statiques.
3. **Just-in-time access** : Accorder l'acces aux secrets sensibles uniquement quand necessaire, pour la duree necessaire.
4. **Encryption everywhere** : Chiffrer les secrets en transit et au repos. Utiliser envelope encryption.
5. **Audit complet** : Logger chaque acces a un secret, chaque rotation, chaque revocation.

### Architecture cible

```
[Application Pod]
    |
    v
[Vault Agent Injector / CSI Driver]  <-- Injecte les secrets dans le pod
    |
    v
[Vault Server]
    |-- Auth via Kubernetes ServiceAccount (identity verification)
    |-- Policies basees sur le namespace, service, et label
    |-- Dynamic secrets (database credentials, cloud credentials)
    |-- TTL court (1h pour DB creds, 15min pour tokens sensibles)
    |-- Audit log vers SIEM
```

### Kubernetes Secrets — Limitations et alternatives

Les Kubernetes Secrets natifs ne sont **pas chiffres par defaut** (ils sont base64-encoded, pas encrypted). Ne pas les utiliser pour des secrets sensibles sans mesures additionnelles.

**Options pour ameliorer la securite des secrets Kubernetes :**

1. **External Secrets Operator** : Synchronise les secrets depuis un secret manager externe (Vault, AWS SM, GCP SM) vers des Kubernetes Secrets.

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: myapp-secrets
  data:
    - secretKey: database-url
      remoteRef:
        key: secret/data/myapp/database
        property: url
    - secretKey: api-key
      remoteRef:
        key: secret/data/myapp/api
        property: key
```

2. **Vault CSI Provider** : Monte les secrets comme fichiers dans le pod, sans creer de Kubernetes Secret.

3. **Sealed Secrets** : Chiffre les secrets avec une cle publique pour les stocker en Git (GitOps-compatible). Seul le controller dans le cluster peut les dechiffrer.

4. **SOPS (Secrets OPerationS)** : Chiffre les fichiers de secrets avec des cles cloud KMS (AWS, GCP, Azure). Compatible GitOps.

### SPIFFE / SPIRE pour l'identite machine

SPIFFE (Secure Production Identity Framework For Everyone) fournit une identite cryptographique a chaque workload :

```
SPIFFE ID : spiffe://trust-domain/path
Exemple : spiffe://example.com/ns/production/sa/myapp

SPIRE (SPIFFE Runtime Environment) :
  1. Agent sur chaque node verifie l'identite du workload
  2. Emet un SVID (SPIFFE Verifiable Identity Document) = certificat X.509 court-lived
  3. Le workload utilise le SVID pour s'authentifier aupres de Vault, d'autres services, etc.
```

L'avantage : Identite machine forte, sans secrets statiques, avec rotation automatique des certificats.

---

## Checklist de gestion des secrets

- [ ] Secret manager deploye et operationnel (Vault, AWS SM, GCP SM)
- [ ] Tous les secrets migres depuis les fichiers de configuration et variables d'environnement
- [ ] Rotation automatique configuree pour tous les secrets critiques
- [ ] Dynamic secrets utilises pour les credentials de base de donnees
- [ ] Pre-commit hook de secrets scanning installe sur tous les postes developpeur
- [ ] Secrets scanning en CI/CD avec politique bloquante
- [ ] Monitoring continu des repositories pour les secrets exposes
- [ ] Procedure de revocation documentee et testee
- [ ] Audit logging actif pour tous les acces aux secrets
- [ ] Certificats TLS automatiquement renouveles (Let's Encrypt / cert-manager)
- [ ] mTLS actif entre les microservices en production
- [ ] `.env` files dans `.gitignore`, `.env.example` a jour
- [ ] Variables d'environnement validees au demarrage de l'application
- [ ] Separation claire entre secrets et configuration non-sensible
- [ ] RBAC applique sur le secret manager (least privilege per service)
