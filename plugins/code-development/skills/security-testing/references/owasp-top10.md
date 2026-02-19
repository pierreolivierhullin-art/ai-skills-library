# OWASP Top 10 — Vulnérabilités et Remédiation

> Référence technique complète des 10 catégories OWASP 2021, avec exemples de code vulnérable, corrections et méthodes de détection. Stack : TypeScript / Node.js / Express.

---

## A01 — Broken Access Control

### Mécanisme de la vulnérabilité

Le contrôle d'accès brisé est la catégorie #1 depuis 2021. Elle regroupe les cas où un utilisateur peut accéder à des ressources ou effectuer des actions qui dépassent ses droits. Les patterns les plus courants : IDOR (Insecure Direct Object Reference), privilege escalation horizontale ou verticale, et contournement de contrôle via manipulation d'URL ou de paramètres.

### Code vulnérable

```typescript
// ❌ IDOR — accès à n'importe quelle commande par ID
app.get('/api/orders/:orderId', async (req, res) => {
  const order = await db.orders.findById(req.params.orderId);
  if (!order) return res.status(404).json({ error: 'Not found' });
  return res.json(order); // Aucune vérification que la commande appartient à l'utilisateur
});

// ❌ Élévation de privilège — modification du rôle en body
app.put('/api/users/:userId', async (req, res) => {
  const updated = await db.users.update(req.params.userId, req.body); // req.body peut contenir { role: 'admin' }
  return res.json(updated);
});
```

### Code corrigé

```typescript
// ✅ IDOR corrigé — liaison stricte utilisateur/ressource
app.get('/api/orders/:orderId', authenticate, async (req, res) => {
  const order = await db.orders.findOne({
    id: req.params.orderId,
    userId: req.user.id, // Filtre obligatoire sur le propriétaire
  });
  if (!order) return res.status(404).json({ error: 'Not found' });
  return res.json(order);
});

// ✅ Mise à jour avec liste blanche de champs
app.put('/api/users/:userId', authenticate, async (req, res) => {
  if (req.user.id !== req.params.userId && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }
  // Extraction explicite des champs autorisés — jamais req.body en entier
  const { firstName, lastName, email } = req.body;
  const updated = await db.users.update(req.params.userId, { firstName, lastName, email });
  return res.json(updated);
});
```

### Détection

- Tests manuels : changer l'ID dans l'URL pour un autre utilisateur de test.
- Outils : OWASP ZAP avec le scanner d'autorisation, Burp Suite Autorize plugin.
- SAST : Semgrep règle `javascript.express.security.audit.express-path-join-resolve-traversal`.

### Règles de prévention

1. Implémenter le contrôle d'accès au niveau du modèle de données, pas uniquement en UI.
2. Refuser par défaut (deny by default) : tout ce qui n'est pas explicitement autorisé est interdit.
3. Journaliser les échecs de contrôle d'accès et alerter en cas de pattern répété.
4. Utiliser des tokens opaques (UUID v4) plutôt que des IDs séquentiels.
5. Tester chaque endpoint avec des comptes de différents rôles dans les tests d'intégration.

---

## A02 — Cryptographic Failures

### Mécanisme de la vulnérabilité

Anciennement "Sensitive Data Exposure", cette catégorie couvre le mauvais usage de la cryptographie : stockage de mots de passe en clair ou avec MD5/SHA-1, transmission non chiffrée, clés codées en dur, algorithmes obsolètes (DES, RC4), IV réutilisés en CBC.

### Code vulnérable

```typescript
// ❌ Mot de passe haché avec MD5 (non salé, cassable par table arc-en-ciel)
import crypto from 'crypto';
const passwordHash = crypto.createHash('md5').update(password).digest('hex');

// ❌ Chiffrement AES avec IV statique codé en dur
const IV = Buffer.from('0000000000000000', 'hex'); // IV fixe = catastrophique
const cipher = crypto.createCipheriv('aes-256-cbc', key, IV);
```

### Code corrigé

```typescript
import bcrypt from 'bcrypt';
import crypto from 'crypto';

// ✅ Hachage de mot de passe avec bcrypt (salt automatique, work factor adaptatif)
const SALT_ROUNDS = 12; // Ajuster selon les performances serveur
async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS);
}
async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// ✅ Chiffrement AES-256-GCM avec IV aléatoire et authentification intégrée
function encrypt(plaintext: string, key: Buffer): string {
  const iv = crypto.randomBytes(12); // 96 bits pour GCM
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
  const authTag = cipher.getAuthTag();
  // Stockage : iv (12) + authTag (16) + ciphertext
  return Buffer.concat([iv, authTag, encrypted]).toString('base64');
}

function decrypt(ciphertext: string, key: Buffer): string {
  const buf = Buffer.from(ciphertext, 'base64');
  const iv = buf.slice(0, 12);
  const authTag = buf.slice(12, 28);
  const encrypted = buf.slice(28);
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(authTag);
  return decipher.update(encrypted) + decipher.final('utf8');
}
```

### Configuration TLS

```nginx
# nginx — TLS 1.2+ uniquement, suites fortes
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

### Détection

- `testssl.sh` pour auditer la configuration TLS.
- Semgrep : règles `crypto` pour détecter MD5/SHA1 dans les contextes sensibles.
- `npm audit` pour identifier les dépendances utilisant des algos obsolètes.

### Règles de prévention

1. Ne jamais utiliser MD5 ou SHA-1 pour les mots de passe — bcrypt, scrypt ou Argon2 uniquement.
2. Toujours générer des IV aléatoires via `crypto.randomBytes()`.
3. Préférer AES-256-GCM (authentifié) à AES-256-CBC.
4. Stocker les clés de chiffrement hors du code source (voir secrets management).
5. Forcer HTTPS et configurer HSTS avec `preload`.

---

## A03 — Injection

### Mécanisme de la vulnérabilité

L'injection survient quand des données non fiables sont envoyées à un interpréteur. SQL injection (SQLi), NoSQL injection (MongoDB `$where`), command injection, LDAP injection, template injection. Cause fondamentale : confusion entre données et instructions.

### SQL Injection

```typescript
// ❌ Requête construite par concaténation
app.get('/api/products', async (req, res) => {
  const { category } = req.query;
  const query = `SELECT * FROM products WHERE category = '${category}'`;
  // Payload : ?category=' OR '1'='1
  const results = await db.raw(query);
  return res.json(results);
});

// ✅ Requête paramétrée avec Knex
app.get('/api/products', async (req, res) => {
  const { category } = req.query;
  const results = await db('products')
    .where('category', String(category)) // Paramètre bindé, pas interpolé
    .select('id', 'name', 'price'); // Sélection explicite des colonnes
  return res.json(results);
});
```

### NoSQL Injection (MongoDB)

```typescript
// ❌ Opérateur MongoDB injectable via req.body
app.post('/api/login', async (req, res) => {
  const { username, password } = req.body;
  // Payload JSON : { "username": { "$ne": null }, "password": { "$ne": null } }
  const user = await User.findOne({ username, password });
  // ...
});

// ✅ Validation stricte du type des entrées
import { z } from 'zod';
const loginSchema = z.object({
  username: z.string().min(1).max(100),
  password: z.string().min(1).max(200),
});

app.post('/api/login', async (req, res) => {
  const parsed = loginSchema.safeParse(req.body);
  if (!parsed.success) return res.status(400).json({ error: 'Invalid input' });
  const { username, password } = parsed.data;
  // Zod garantit que username et password sont des strings, pas des objets
  const user = await User.findOne({ username }).select('+passwordHash');
  if (!user || !await bcrypt.compare(password, user.passwordHash)) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
});
```

### Command Injection

```typescript
import { exec, execFile } from 'child_process';
import { promisify } from 'util';
const execFileAsync = promisify(execFile);

// ❌ exec avec interpolation de chaîne
app.post('/api/convert', (req, res) => {
  const { filename } = req.body;
  exec(`convert ${filename} output.pdf`, (err, stdout) => { /* ... */ });
  // Payload : filename = "file.jpg; rm -rf /"
});

// ✅ execFile avec arguments séparés — pas d'interprétation shell
app.post('/api/convert', async (req, res) => {
  const { filename } = req.body;
  // Validation : nom de fichier sûr uniquement
  if (!/^[\w\-. ]+\.(jpg|png|gif)$/i.test(filename)) {
    return res.status(400).json({ error: 'Invalid filename' });
  }
  const safePath = path.join('/uploads', path.basename(filename)); // Évite path traversal
  await execFileAsync('convert', [safePath, 'output.pdf']); // Arguments séparés
  return res.json({ success: true });
});
```

### Détection

- Semgrep : règles `javascript.lang.security.audit.sqli`, `node-child-process-injection`.
- Tests automatisés : SQLMap pour SQLi, Burp Suite Intruder avec payloads injection.

### Règles de prévention

1. Toujours utiliser des requêtes paramétrées ou des ORM (Prisma, TypeORM, Knex).
2. Valider et typer strictement toutes les entrées avec Zod ou Joi.
3. Utiliser `execFile` au lieu de `exec` pour les commandes système.
4. Principe du moindre privilège pour le compte de base de données.

---

## A04 — Insecure Design

### Mécanisme de la vulnérabilité

L'insecure design désigne les failles architecturales : absence de modélisation des menaces, flows métier exploitables (ex. : commander avec un prix négatif), manque de contrôles de taux, flux d'authentification contournables.

### Threat Modeling — STRIDE

```
Pour chaque fonctionnalité, évaluer :
Spoofing       → Qui peut se faire passer pour quelqu'un d'autre ?
Tampering      → Quelles données peuvent être modifiées illégitimement ?
Repudiation    → Peut-on nier avoir effectué une action ?
Info Disclosure → Quelles données sensibles peuvent fuiter ?
Denial of Service → Quel composant peut être saturé ?
Elevation of Privilege → Comment escalader des droits ?
```

### Exemple : flow de remise exploitable

```typescript
// ❌ La réduction est calculée côté client et envoyée au serveur
// Requête : POST /api/checkout { items: [...], discount: 99 }
app.post('/api/checkout', async (req, res) => {
  const { items, discount } = req.body;
  const total = calculateTotal(items) * (1 - discount / 100); // Discount contrôlé par l'attaquant
  await chargeCard(total);
});

// ✅ Toute logique de prix calculée côté serveur, code promo validé en base
app.post('/api/checkout', authenticate, async (req, res) => {
  const { items, promoCode } = req.body;
  const serverTotal = await calculateTotalFromDB(items); // Prix récupérés depuis la base
  let discount = 0;
  if (promoCode) {
    const promo = await db.promoCodes.findOne({ code: promoCode, active: true });
    if (!promo || promo.usageCount >= promo.maxUses) {
      return res.status(400).json({ error: 'Invalid promo code' });
    }
    discount = promo.discountPercent;
  }
  const finalTotal = serverTotal * (1 - discount / 100);
  await chargeCard(finalTotal);
});
```

### Règles de prévention

1. Intégrer le threat modeling (STRIDE, PASTA) dès la phase de design sprint.
2. Utiliser des user stories de sécurité : "En tant qu'attaquant, je veux...".
3. Implémenter des limites métier côté serveur (quantité max, prix min, délai entre opérations).
4. Réviser le design avec des tests d'abus (abuse cases) avant le développement.

---

## A05 — Security Misconfiguration

### Mécanisme de la vulnérabilité

Configurations par défaut non modifiées, services inutiles activés, messages d'erreur verbeux, headers de sécurité manquants, permissions trop larges sur S3/Docker/Kubernetes.

### Headers HTTP avec Helmet

```typescript
import helmet from 'helmet';
import express from 'express';

const app = express();

// ✅ Configuration Helmet complète
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'nonce-{NONCE}'"], // Générer un nonce par requête
      styleSrc: ["'self'", "'unsafe-inline'"], // Éviter 'unsafe-inline' si possible
      imgSrc: ["'self'", 'data:', 'https://cdn.example.com'],
      connectSrc: ["'self'", 'https://api.example.com'],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      frameAncestors: ["'none'"],
      upgradeInsecureRequests: [],
    },
  },
  hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
  permissionsPolicy: {
    features: { geolocation: ['none'], camera: ['none'], microphone: ['none'] },
  },
}));

// Supprimer l'en-tête X-Powered-By
app.disable('x-powered-by');
```

### Docker Hardening

```dockerfile
# ❌ Image root, pas de restriction
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]

# ✅ Image non-root, distroless, read-only
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --chown=nonroot:nonroot . .
USER nonroot
EXPOSE 3000
CMD ["server.js"]
```

```yaml
# Kubernetes — Security Context
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: api
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
```

### Détection

- `docker bench security` pour auditer la configuration Docker.
- `kube-bench` pour Kubernetes CIS Benchmark.
- Mozilla Observatory pour les headers HTTP.

---

## A06 — Vulnerable and Outdated Components

### Mécanisme de la vulnérabilité

Dépendances avec CVE connues, composants sans support, packages abandonnés, images Docker obsolètes. La supply chain est un vecteur d'attaque majeur (ex. : Log4Shell via Log4j).

### npm audit et Snyk

```bash
# Audit des dépendances npm
npm audit --audit-level=moderate

# Correction automatique des vulnérabilités corrigeables
npm audit fix

# Snyk — analyse plus approfondie avec remediation
npx snyk test --severity-threshold=high
npx snyk monitor # Surveillance continue en CI

# Mise à jour des dépendances avec vérification des breaking changes
npx npm-check-updates --interactive
```

### Configuration Dependabot

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule:
      interval: weekly
      day: monday
      time: "09:00"
    open-pull-requests-limit: 10
    groups:
      production-deps:
        dependency-type: production
        update-types: ["minor", "patch"]
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]
```

### Règles de prévention

1. Intégrer `npm audit` et Snyk dans le pipeline CI comme étape bloquante.
2. Configurer Dependabot ou Renovate pour les mises à jour automatiques.
3. Surveiller les advisory via GitHub Advisories ou OSV.dev.
4. Maintenir un inventaire des dépendances (SBOM — voir sast-dast-tools).

---

## A07 — Identification and Authentication Failures

### Mécanisme de la vulnérabilité

Absence de protection contre le brute force, mots de passe faibles autorisés, sessions non invalidées, JWT mal configurés (algorithme `none`, clé faible), session fixation.

### Protection brute force avec express-rate-limit

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import { createClient } from 'redis';

const redisClient = createClient({ url: process.env.REDIS_URL });

// Limite stricte sur les endpoints d'authentification
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 tentatives par fenêtre par IP
  standardHeaders: true,
  legacyHeaders: false,
  store: new RedisStore({ sendCommand: (...args) => redisClient.sendCommand(args) }),
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too many login attempts. Please try again in 15 minutes.',
    });
  },
});

app.post('/api/auth/login', authLimiter, loginHandler);
```

### JWT — pièges courants

```typescript
import jwt from 'jsonwebtoken';

// ❌ Pièges JWT fréquents
// 1. Algorithme 'none' — token non signé accepté
jwt.verify(token, secret, { algorithms: ['none'] }); // INTERDIT

// 2. Clé symétrique faible ou codée en dur
const secret = 'secret'; // Trop faible, prévisible

// ❌ Pas de validation de l'audience ou de l'émetteur
jwt.verify(token, secret); // Manque iss/aud

// ✅ Configuration JWT sécurisée
const JWT_SECRET = process.env.JWT_SECRET; // 256 bits minimum, depuis l'environnement
const JWT_ISSUER = 'https://auth.example.com';
const JWT_AUDIENCE = 'https://api.example.com';

function signToken(userId: string): string {
  return jwt.sign(
    { sub: userId },
    JWT_SECRET,
    {
      algorithm: 'HS256',
      expiresIn: '15m', // Access token court
      issuer: JWT_ISSUER,
      audience: JWT_AUDIENCE,
    }
  );
}

function verifyToken(token: string): jwt.JwtPayload {
  return jwt.verify(token, JWT_SECRET, {
    algorithms: ['HS256'], // Liste blanche explicite
    issuer: JWT_ISSUER,
    audience: JWT_AUDIENCE,
  }) as jwt.JwtPayload;
}
```

### Session Fixation

```typescript
// ❌ Réutilisation du session ID avant/après authentification
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body);
  req.session.userId = user.id; // Même session ID qu'avant la connexion
});

// ✅ Régénération du session ID après authentification
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body);
  await new Promise<void>((resolve, reject) =>
    req.session.regenerate((err) => (err ? reject(err) : resolve()))
  );
  req.session.userId = user.id; // Nouveau session ID
  req.session.createdAt = Date.now();
});
```

---

## A08 — Software and Data Integrity Failures

### Mécanisme de la vulnérabilité

Mise à jour automatique sans vérification d'intégrité, CDN compromis, pipeline CI/CD sans signature, dépendances sans SRI (Subresource Integrity), attaques de la supply chain (ex. : SolarWinds, event-stream npm).

### Subresource Integrity (SRI)

```html
<!-- ❌ CDN sans vérification d'intégrité -->
<script src="https://cdn.example.com/lib.min.js"></script>

<!-- ✅ SRI — hash SHA-384 vérifié par le navigateur -->
<script
  src="https://cdn.example.com/lib.min.js"
  integrity="sha384-AbCdEf..."
  crossorigin="anonymous"
></script>
```

```bash
# Générer le hash SRI
curl -s https://cdn.example.com/lib.min.js | openssl dgst -sha384 -binary | openssl base64 -A
# Ou utiliser srihash.org
```

### Vérification d'intégrité dans le pipeline CI

```yaml
# GitHub Actions — vérification de la signature des actions
steps:
  - uses: actions/checkout@v4  # Version pinée, pas @main
  # Utiliser le SHA du commit pour une épinglage absolu
  - uses: actions/setup-node@1a4442cacd436585916779262731d1f068594b6
    with:
      node-version: '20'
```

### Règles de prévention

1. Ajouter SRI à tous les assets chargés depuis des CDN externes.
2. Épingler les GitHub Actions à leur SHA de commit (pas à un tag).
3. Signer les artifacts de build avec Sigstore/cosign.
4. Utiliser `npm ci` (pas `npm install`) en CI pour respecter le `package-lock.json`.

---

## A09 — Security Logging and Monitoring Failures

### Ce qu'il NE faut PAS logger

```typescript
// ❌ Ne jamais logger ces informations
logger.info(`Login attempt: ${username}:${password}`); // Mot de passe en clair
logger.debug(`Payment data: ${JSON.stringify(creditCard)}`); // PAN, CVV
logger.info(`Token issued: ${jwtToken}`); // Token valide en logs
logger.error(`DB error for query: ${rawSqlQuery}`); // Peut contenir des données sensibles
```

### Ce qu'il FAUT logger

```typescript
import { createLogger, format, transports } from 'winston';

const logger = createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: format.combine(
    format.timestamp(),
    format.errors({ stack: true }),
    format.json()
  ),
  transports: [
    new transports.Console(),
    new transports.File({ filename: '/var/log/app/security.log' }),
  ],
});

// ✅ Événements de sécurité à logger systématiquement
function logSecurityEvent(event: {
  type: 'auth_success' | 'auth_failure' | 'access_denied' | 'rate_limit' | 'suspicious_activity';
  userId?: string;
  ip: string;
  userAgent: string;
  resource?: string;
  reason?: string;
}) {
  logger.warn({
    ...event,
    timestamp: new Date().toISOString(),
    correlationId: req.headers['x-correlation-id'],
    // Jamais de données sensibles dans les logs
  });
}

// Exemples d'usage
logSecurityEvent({ type: 'auth_failure', ip: req.ip, userAgent: req.headers['user-agent'], reason: 'invalid_password' });
logSecurityEvent({ type: 'access_denied', userId: req.user.id, resource: '/admin', ip: req.ip, userAgent: req.headers['user-agent'] });
```

### Intégration SIEM

```yaml
# Filebeat → Elasticsearch (ELK Stack)
filebeat.inputs:
  - type: filestream
    paths:
      - /var/log/app/security.log
    parsers:
      - ndjson:
          target: ""
          overwrite_keys: true

output.elasticsearch:
  hosts: ["https://elasticsearch:9200"]
  index: "security-events-%{+yyyy.MM.dd}"
  ssl.certificate_authorities: ["/etc/ssl/certs/ca.crt"]
```

### Règles de prévention

1. Logger tous les événements d'authentification (succès et échecs).
2. Logger les accès refusés avec le contexte (utilisateur, ressource, raison).
3. Ne jamais logger de données sensibles : passwords, tokens, PAN, données personnelles.
4. Centraliser les logs dans un SIEM (ELK, Splunk, Datadog) avec alertes.
5. Définir des alertes sur les patterns suspects (>10 échecs/minute, accès admin inattendu).

---

## A10 — Server-Side Request Forgery (SSRF)

### Mécanisme de la vulnérabilité

SSRF : le serveur effectue une requête HTTP vers une URL contrôlée par l'attaquant. En cloud (AWS, GCP, Azure), cela permet d'accéder au service de métadonnées de l'instance (`169.254.169.254`) et de voler les credentials IAM. Vecteurs courants : import d'URL, preview de lien, webhook.

### Code vulnérable

```typescript
// ❌ Requête vers une URL fournie par l'utilisateur sans validation
app.post('/api/fetch-preview', async (req, res) => {
  const { url } = req.body;
  const response = await fetch(url); // Payload : http://169.254.169.254/latest/meta-data/iam/
  const html = await response.text();
  return res.json({ preview: html }); // Renvoie les credentials AWS !
});
```

### Code corrigé avec allow-listing

```typescript
import { URL } from 'url';
import dns from 'dns/promises';
import net from 'net';

const ALLOWED_DOMAINS = new Set(['example.com', 'api.example.com', 'cdn.example.com']);

async function isPrivateIP(hostname: string): Promise<boolean> {
  try {
    const addresses = await dns.resolve4(hostname);
    return addresses.some((addr) => {
      return (
        net.isIPv4(addr) && (
          addr.startsWith('10.') ||
          addr.startsWith('172.16.') || // 172.16.0.0/12
          addr.startsWith('192.168.') ||
          addr.startsWith('127.') ||
          addr === '169.254.169.254' || // AWS metadata
          addr === '0.0.0.0'
        )
      );
    });
  } catch {
    return true; // En cas d'erreur DNS, refuser par défaut
  }
}

async function validateAndFetch(rawUrl: string): Promise<Response> {
  let parsed: URL;
  try {
    parsed = new URL(rawUrl);
  } catch {
    throw new Error('Invalid URL format');
  }

  // Allow-list sur le protocole
  if (!['https:', 'http:'].includes(parsed.protocol)) {
    throw new Error('Protocol not allowed'); // Bloque file://, gopher://, etc.
  }

  // Allow-list sur le domaine
  if (!ALLOWED_DOMAINS.has(parsed.hostname)) {
    throw new Error(`Domain not allowed: ${parsed.hostname}`);
  }

  // Résolution DNS et vérification IP privée (DNS rebinding protection)
  if (await isPrivateIP(parsed.hostname)) {
    throw new Error('Private IP ranges are not allowed');
  }

  return fetch(parsed.toString(), {
    redirect: 'error', // Ne pas suivre les redirections automatiquement
    signal: AbortSignal.timeout(5000),
  });
}

app.post('/api/fetch-preview', async (req, res) => {
  try {
    const response = await validateAndFetch(req.body.url);
    const text = await response.text();
    return res.json({ preview: text.slice(0, 10000) }); // Limiter la taille
  } catch (err) {
    return res.status(400).json({ error: (err as Error).message });
  }
});
```

### Détection

- Burp Suite Collaborator pour détecter les requêtes sortantes du serveur.
- OWASP ZAP : active scanner avec payloads SSRF.
- En code review : chercher `fetch(req.body.url)`, `axios.get(userInput)`, `http.get(param)`.

### Règles de prévention

1. Toujours utiliser une allow-list de domaines autorisés, jamais une denylist d'IPs.
2. Résoudre le DNS et vérifier que l'IP de destination n'est pas privée (DNS rebinding).
3. Désactiver le suivi automatique des redirections HTTP.
4. Bloquer l'accès au service de métadonnées cloud au niveau réseau (IMDSv2 sur AWS).
5. Considérer un proxy sortant dédié pour toutes les requêtes externes.

---

## Récapitulatif — Matrice de priorité

| Catégorie | Sévérité | Complexité de fix | Priorité |
|-----------|----------|-------------------|----------|
| A01 Broken Access Control | Critique | Moyenne | P0 |
| A02 Cryptographic Failures | Critique | Faible | P0 |
| A03 Injection | Critique | Faible | P0 |
| A04 Insecure Design | Élevée | Haute | P1 |
| A05 Security Misconfiguration | Élevée | Faible | P0 |
| A06 Vulnerable Components | Moyenne | Faible | P1 |
| A07 Auth Failures | Élevée | Moyenne | P0 |
| A08 Integrity Failures | Élevée | Moyenne | P1 |
| A09 Logging Failures | Moyenne | Faible | P1 |
| A10 SSRF | Élevée | Moyenne | P0 |

**Règle d'or** : tester chaque catégorie explicitement dans les tests d'intégration et lors de chaque pentest. L'OWASP Testing Guide v4.2 fournit les cas de test détaillés pour chaque catégorie.
