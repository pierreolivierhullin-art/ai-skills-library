# Security Hardening

Reference complete pour le durcissement securitaire des applications web modernes (2024-2026). Couvre OWASP Top 10, prevention des injections, security headers, CSP, CORS, rate limiting, et scanning de dependances.

---

## OWASP Top 10 (2021) — Guide d'implementation

Le OWASP Top 10 est la reference mondiale pour les vulnerabilites applicatives web les plus critiques. Traiter chaque categorie comme un requirement non-negociable.

### A01:2021 — Broken Access Control

La vulnerabilite la plus courante. Concerne tout contournement des controles d'acces.

**Mesures d'attenuation :**

- Implementer le deny-by-default pour tous les endpoints
- Valider l'autorisation cote serveur pour chaque requete (ne jamais se fier au client)
- Utiliser des references indirectes (UUIDs) plutot que des IDs sequentiels
- Implementer RLS au niveau base de donnees comme couche de defense supplementaire
- Verifier la propriete de la ressource avant toute operation (IDOR prevention)
- Desactiver le directory listing du serveur web
- Limiter le rate des requetes API pour les endpoints sensibles
- Logger chaque echec d'autorisation et alerter sur les patterns anormaux

**Test :**

```
1. Tenter d'acceder aux ressources d'un autre utilisateur en changeant l'ID dans l'URL
2. Tenter d'acceder a des endpoints admin sans le role admin
3. Tenter d'effectuer des operations CRUD non autorisees
4. Tester les IDOR (Insecure Direct Object Reference) sur chaque endpoint
5. Verifier que les endpoints API respectent les memes controles que l'UI
```

### A02:2021 — Cryptographic Failures

Concerne l'exposition de donnees sensibles due a un chiffrement absent ou defaillant.

**Mesures d'attenuation :**

- Chiffrer toutes les donnees en transit avec TLS 1.2+ (preferer TLS 1.3)
- Chiffrer les donnees sensibles au repos (AES-256-GCM)
- Ne jamais implementer sa propre cryptographie — utiliser des librairies eprouvees
- Hasher les mots de passe avec **bcrypt** (cost factor 12+), **scrypt**, ou **Argon2id** (recommande)
- Ne jamais utiliser MD5, SHA1, ou SHA256 seul pour les mots de passe
- Generer les cles et IV avec un CSPRNG (Cryptographically Secure Pseudo-Random Number Generator)
- Desactiver le caching des reponses contenant des donnees sensibles
- Classifier les donnees et appliquer le chiffrement proportionnellement a la sensibilite

**Algorithmes recommandes (2024-2026) :**

| Usage | Algorithme recommande | A eviter |
|-------|----------------------|----------|
| Hachage mot de passe | Argon2id, bcrypt (cost 12+) | MD5, SHA-*, PBKDF2 faible |
| Chiffrement symetrique | AES-256-GCM, ChaCha20-Poly1305 | DES, 3DES, AES-ECB |
| Chiffrement asymetrique | RSA-OAEP (2048+), ECDH P-256 | RSA-PKCS1v1.5 |
| Signature | Ed25519, ECDSA P-256, RSA-PSS | RSA-PKCS1v1.5 |
| TLS | TLS 1.3, TLS 1.2 (ciphersuites modernes) | SSL, TLS 1.0, TLS 1.1 |
| KDF | HKDF, Argon2 | Derivation maison |

### A03:2021 — Injection

Toute forme d'injection de code ou de commandes non sanitisees.

**SQL Injection — Prevention :**

```typescript
// INTERDIT : concatenation directe
const query = `SELECT * FROM users WHERE email = '${email}'`; // VULNERABLE

// OBLIGATOIRE : requetes parametrees
const query = 'SELECT * FROM users WHERE email = $1';
const result = await pool.query(query, [email]);

// ORM : utiliser les methodes de l'ORM, jamais de raw queries avec interpolation
const user = await prisma.user.findUnique({ where: { email } });
```

**NoSQL Injection — Prevention :**

```typescript
// INTERDIT : objet non valide directement dans la requete
const user = await db.users.findOne({ email: req.body.email }); // VULNERABLE si email = {"$gt": ""}

// OBLIGATOIRE : valider et typer les inputs
const email = z.string().email().parse(req.body.email);
const user = await db.users.findOne({ email });
```

**Command Injection — Prevention :**

- Ne jamais utiliser `exec()`, `system()`, ou `eval()` avec des inputs utilisateur
- Utiliser des librairies specifiques plutot que des commandes shell
- Si commande shell inevitable, utiliser `execFile()` avec des arguments separes (pas de concatenation)

**Template Injection — Prevention :**

- Ne jamais passer d'inputs utilisateur comme templates (Jinja2, Handlebars, etc.)
- Configurer les template engines en mode sandbox si disponible

### A04:2021 — Insecure Design

Concerne les failles de conception architecturale, pas les bugs d'implementation.

**Mesures d'attenuation :**

- Realiser un threat modeling (STRIDE, PASTA) pour chaque feature sensible
- Implementer des use cases et des abuse cases (misuse cases) en phase de design
- Appliquer les principes de defense en profondeur des le design
- Documenter les trust boundaries et les data flows
- Revoir l'architecture avec un focus securite avant l'implementation

### A05:2021 — Security Misconfiguration

**Mesures d'attenuation :**

- Automatiser la configuration de securite via Infrastructure as Code (IaC)
- Desactiver toutes les fonctionnalites non necessaires (debug mode, endpoints de test, comptes par defaut)
- Maintenir un processus de hardening reproductible pour chaque environnement
- Scanner regulierement les configurations (CIS Benchmarks)
- Separer les configurations par environnement (dev, staging, production)
- Mettre a jour les frameworks, librairies et serveurs regulierement

### A06:2021 — Vulnerable and Outdated Components

**Mesures d'attenuation :**

- Scanner les dependances en CI/CD avec Snyk, Dependabot, ou Trivy
- Configurer les alertes automatiques pour les CVE critiques
- Maintenir un inventaire des dependances (SBOM - Software Bill of Materials)
- Mettre a jour les dependances regulierement (weekly automated PRs)
- Supprimer les dependances non utilisees
- Utiliser `npm audit`, `pip audit`, ou equivalent pour chaque ecosysteme

### A07:2021 — Identification and Authentication Failures

Voir le fichier de reference `authentication-patterns.md` pour un traitement exhaustif.

### A08:2021 — Software and Data Integrity Failures

**Mesures d'attenuation :**

- Verifier l'integrite des dependances (checksums, signatures)
- Utiliser des lock files (`package-lock.json`, `Pipfile.lock`, `go.sum`)
- Signer les commits Git (GPG ou SSH signing)
- Implementer des checks d'integrite pour les pipelines CI/CD
- Ne jamais deserialiser des donnees non fiables sans validation de schema
- Utiliser Subresource Integrity (SRI) pour les scripts tiers

### A09:2021 — Security Logging and Monitoring Failures

**Mesures d'attenuation :**

- Logger tous les evenements de securite : login/logout, failed auth, access denied, privilege changes
- Ne jamais logger de secrets, tokens, mots de passe, ou PII non masquees
- Implementer un format de log structure (JSON) avec correlation IDs
- Centraliser les logs (ELK, Datadog, Grafana Loki)
- Configurer des alertes pour les patterns suspects (brute force, privilege escalation, anomalies)
- Definir un temps de retention des logs conforme aux exigences reglementaires
- Tester regulierement que le monitoring detecte les incidents simules

### A10:2021 — Server-Side Request Forgery (SSRF)

**Mesures d'attenuation :**

- Valider et sanitiser toutes les URLs fournies par l'utilisateur
- Maintenir une allow-list des domaines/IPs autorisees pour les requetes sortantes
- Bloquer les requetes vers les plages d'adresses privees (10.0.0.0/8, 172.16.0.0/12, 169.254.169.254, etc.)
- Utiliser un proxy dedie pour les requetes sortantes avec filtrage
- Desactiver les redirections HTTP pour les requetes cote serveur
- Segmenter le reseau pour limiter l'impact d'un SSRF

---

## Input Validation & Sanitization

### Strategie de validation

Appliquer une strategie de validation en couches :

```
Layer 1 : Validation de format (client-side, UX only)
Layer 2 : Validation de schema (server-side, Zod/Joi/Yup)
Layer 3 : Validation metier (server-side, logique applicative)
Layer 4 : Sanitisation avant stockage/affichage
Layer 5 : Parametrage des requetes (prepared statements, ORM)
```

**Implementation avec Zod (TypeScript) :**

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email().max(255).toLowerCase(),
  name: z.string().min(1).max(100).trim(),
  age: z.number().int().min(13).max(150).optional(),
  role: z.enum(['user', 'editor']),  // Jamais 'admin' via l'API publique
  bio: z.string().max(1000).optional(),
});

// Dans le handler
const parsed = CreateUserSchema.safeParse(req.body);
if (!parsed.success) {
  return res.status(400).json({ errors: parsed.error.flatten() });
}
const validatedData = parsed.data; // Type-safe et valide
```

### Regles de validation par type

| Type de donnee | Validation | Sanitisation |
|----------------|------------|-------------|
| Email | Regex RFC 5322 + max 255 chars | toLowerCase, trim |
| Nom/texte libre | Max length, charset allow-list | Trim, HTML escape |
| URL | Validation URL + protocol allow-list (https) | Normalisation |
| Entier | Range check, type check | parseInt strict |
| UUID | Format validation (regex ou librairie) | Aucune |
| HTML riche (si requis) | Sanitiser avec DOMPurify ou equivalent | Allow-list de tags |
| Nom de fichier | Allow-list de caracteres, pas de path traversal | Supprimer `../`, `\`, null bytes |
| JSON | Validation de schema (JSON Schema, Zod) | Parser strict |

### Principe : Allow-List over Deny-List

Toujours preferer les allow-lists aux deny-lists. Definir ce qui est autorise plutot que ce qui est interdit. Les deny-lists sont inevitablement incompletes face a des encodages creatifs.

---

## XSS Prevention (Cross-Site Scripting)

### Types de XSS

- **Stored XSS** : Payload stocke en base et restitue a d'autres utilisateurs. Le plus dangereux.
- **Reflected XSS** : Payload dans l'URL reflete dans la reponse.
- **DOM-based XSS** : Payload manipule le DOM cote client sans passer par le serveur.

### Mesures de prevention

1. **Echapper les outputs** selon le contexte :
   - HTML body : HTML entity encoding (`<` -> `&lt;`)
   - HTML attributs : Attribute encoding + quotes obligatoires
   - JavaScript : JavaScript encoding (ne jamais inserer de donnees dans des inline scripts)
   - URL : URL encoding (`encodeURIComponent`)
   - CSS : CSS encoding (eviter les valeurs dynamiques dans les styles)

2. **Utiliser un framework avec auto-escaping** : React (JSX escape par defaut), Vue (template escape par defaut), Angular (sanitisation automatique). Ne jamais utiliser `dangerouslySetInnerHTML` (React), `v-html` (Vue), ou `innerHTML` sans sanitisation prealable.

3. **Content Security Policy (CSP)** : Voir section CSP ci-dessous.

4. **Sanitisation HTML riche** : Si du HTML utilisateur est necessaire (editeur WYSIWYG), utiliser DOMPurify cote client et un sanitiseur cote serveur :

```typescript
import DOMPurify from 'dompurify';

const cleanHTML = DOMPurify.sanitize(userHTML, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li'],
  ALLOWED_ATTR: ['href', 'target', 'rel'],
});
```

---

## CSRF Prevention (Cross-Site Request Forgery)

### Strategie de defense

Combiner plusieurs mecanismes :

1. **SameSite cookies** : Configurer `SameSite=Lax` (minimum) ou `SameSite=Strict` pour les cookies de session.

2. **CSRF tokens** : Pour les formulaires et les requetes mutationnelles :
   - Generer un token aleatoire unique par session (ou par requete)
   - L'inclure dans un champ hidden du formulaire ou un header custom
   - Valider le token cote serveur pour chaque requete POST/PUT/DELETE

3. **Double Submit Cookie** : Alternative si le state server-side est impossible :
   - Envoyer le CSRF token dans un cookie (non HttpOnly) ET dans le body/header
   - Verifier que les deux valeurs correspondent

4. **Custom headers** : Pour les API appelees via JavaScript, exiger un header custom (`X-Requested-With`, `X-CSRF-Token`). Les requetes cross-origin ne peuvent pas ajouter de headers custom sans preflight CORS.

### Frameworks modernes

La plupart des frameworks modernes gerent le CSRF automatiquement :

- **Next.js** : Utiliser les Server Actions (CSRF protection integree)
- **Django** : Middleware CSRF actif par defaut
- **Rails** : `protect_from_forgery` actif par defaut
- **Laravel** : Middleware VerifyCsrfToken actif par defaut
- **SPA + API** : SameSite cookies + BFF pattern eliminent la plupart des risques CSRF

---

## Content Security Policy (CSP)

### Configuration progressive

Deployer CSP progressivement :

**Phase 1 : Report-Only (observation)**

```
Content-Security-Policy-Report-Only: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; report-uri /csp-report
```

**Phase 2 : Enforcement strict**

```
Content-Security-Policy:
  default-src 'none';
  script-src 'self' 'nonce-{random}';
  style-src 'self' 'nonce-{random}';
  img-src 'self' data: https://cdn.example.com;
  font-src 'self' https://fonts.gstatic.com;
  connect-src 'self' https://api.example.com;
  frame-src 'none';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
  frame-ancestors 'none';
  upgrade-insecure-requests;
  report-uri /csp-report
```

### Regles critiques

- Ne jamais utiliser `'unsafe-inline'` pour `script-src` en production. Utiliser des nonces (`'nonce-{random}'`) ou des hashes.
- Ne jamais utiliser `'unsafe-eval'` sauf obligation absolue (certains frameworks legacy).
- Utiliser `'strict-dynamic'` si des scripts charges dynamiquement sont necessaires.
- Generer un nouveau nonce pour chaque reponse HTTP (ne jamais reutiliser).
- Configurer `frame-ancestors 'none'` pour prevenir le clickjacking (remplace X-Frame-Options).

---

## CORS (Cross-Origin Resource Sharing)

### Configuration securisee

```typescript
// Configuration CORS Express.js
import cors from 'cors';

const corsOptions = {
  origin: (origin, callback) => {
    const allowedOrigins = [
      'https://app.example.com',
      'https://admin.example.com',
    ];
    // Autoriser les requetes sans origin (mobile apps, curl)
    // OU restreindre strictement selon le contexte
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Request-ID'],
  credentials: true,
  maxAge: 86400, // Preflight cache: 24 heures
};

app.use(cors(corsOptions));
```

### Regles critiques

- Ne jamais utiliser `Access-Control-Allow-Origin: *` avec `credentials: true`
- Ne jamais refleter dynamiquement l'header `Origin` de la requete sans validation
- Limiter les methodes autorisees au strict necessaire
- Limiter les headers autorises au strict necessaire
- Configurer un `maxAge` pour reduire les preflight requests

---

## Security Headers

### Configuration complete recommandee

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
X-XSS-Protection: 0
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
```

**Notes :**

- `X-XSS-Protection: 0` : Desactiver explicitement. Le filtre XSS du navigateur est deprecie et peut introduire des vulnerabilites.
- `Permissions-Policy` : Restreindre les API sensibles du navigateur. Ajouter uniquement les permissions necessaires.
- `COOP/COEP/CORP` : Necessaires pour activer l'isolation cross-origin (requis pour SharedArrayBuffer, mesures de timing precises).

### Implementation Helmet.js (Node.js)

```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'none'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https://cdn.example.com"],
      connectSrc: ["'self'", "https://api.example.com"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      frameAncestors: ["'none'"],
      baseUri: ["'self'"],
      formAction: ["'self'"],
    },
  },
  crossOriginEmbedderPolicy: true,
  crossOriginOpenerPolicy: true,
  crossOriginResourcePolicy: { policy: "same-origin" },
  hsts: { maxAge: 63072000, includeSubDomains: true, preload: true },
  referrerPolicy: { policy: "strict-origin-when-cross-origin" },
}));
```

---

## Rate Limiting & DDoS Protection

### Strategie de rate limiting

Implementer un rate limiting multi-couches :

**Layer 1 : CDN / Edge (Cloudflare, AWS CloudFront)**

- DDoS protection L3/L4 automatique
- Rate limiting L7 par IP, geolocation, ASN
- Bot detection et challenge (Turnstile, hCaptcha)

**Layer 2 : API Gateway / Load Balancer**

- Rate limiting par API key / client ID
- Throttling par endpoint (endpoints sensibles = limites basses)
- Circuit breaker pour les services downstream

**Layer 3 : Application**

- Rate limiting par utilisateur authentifie
- Rate limiting specifique par action (login: 5/min, signup: 3/min, password reset: 1/min)
- Sliding window algorithm recommande (plus precis que fixed window)

**Implementation Redis (Node.js) :**

```typescript
import { RateLimiterRedis } from 'rate-limiter-flexible';

const loginLimiter = new RateLimiterRedis({
  storeClient: redisClient,
  keyPrefix: 'rl:login',
  points: 5,           // 5 tentatives
  duration: 60,         // par minute
  blockDuration: 300,   // bloquer 5 minutes apres depassement
});

const apiLimiter = new RateLimiterRedis({
  storeClient: redisClient,
  keyPrefix: 'rl:api',
  points: 100,          // 100 requetes
  duration: 60,         // par minute
});

// Middleware
async function rateLimitMiddleware(req, res, next) {
  try {
    const key = req.user?.id || req.ip;
    await apiLimiter.consume(key);
    next();
  } catch (rateLimiterRes) {
    res.set('Retry-After', String(Math.ceil(rateLimiterRes.msBeforeNext / 1000)));
    res.status(429).json({ error: 'Too Many Requests' });
  }
}
```

### Reponses aux rate limits

- Retourner un status **429 Too Many Requests**
- Inclure le header `Retry-After` avec le nombre de secondes d'attente
- Inclure les headers `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- Ne pas reveler d'informations sur l'existence de comptes via le rate limiting

---

## Dependency Scanning

### Outils recommandes

| Outil | Type | Integration | Forces |
|-------|------|-------------|--------|
| **Snyk** | SaaS + CLI | CI/CD, IDE, GitHub | Base CVE etendue, fix automatiques |
| **Dependabot** | GitHub natif | GitHub Actions | Natif GitHub, PRs automatiques |
| **Trivy** | Open-source | CI/CD, containers | Scan containers + deps + IaC |
| **Socket** | SaaS | npm, GitHub | Detection supply chain attacks |
| **Renovate** | Open-source / SaaS | CI/CD, multi-platform | Tres configurable, grouping |

### Pipeline CI/CD securise

```yaml
# GitHub Actions example
name: Security Scan
on: [push, pull_request]

jobs:
  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Check for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified
```

### Politique de mise a jour

- Configurer les mises a jour automatiques pour les patches de securite (Dependabot, Renovate)
- Revoir et merger les PRs de securite dans les 48 heures pour les CVE critiques
- Maintenir un SBOM (Software Bill of Materials) a jour
- Bloquer les merges si des vulnerabilites critiques sont detectees

---

## Checklist de durcissement

Utiliser cette checklist pour chaque application en production :

- [ ] HTTPS force partout, TLS 1.2+ uniquement, HSTS preload active
- [ ] Security headers complets (CSP, HSTS, X-Content-Type-Options, etc.)
- [ ] CSP deploye en mode enforcement (pas uniquement report-only)
- [ ] CORS configure avec des origines explicites (pas de wildcard)
- [ ] Input validation cote serveur pour chaque endpoint
- [ ] Protection CSRF active pour les requetes mutationnelles
- [ ] Rate limiting configure sur les endpoints sensibles
- [ ] Dependency scanning en CI/CD avec seuil bloquant
- [ ] Secrets scanning en CI/CD (GitGuardian ou TruffleHog)
- [ ] Logging securitaire (pas de secrets, format structure, retention definie)
- [ ] Monitoring et alerting sur les evenements de securite
- [ ] Error handling securise (pas de stack traces en production)
- [ ] Directory listing desactive sur le serveur web
- [ ] Fonctionnalites de debug desactivees en production
- [ ] Comptes par defaut supprimes ou desactives
- [ ] Mises a jour de securite appliquees dans les 48h pour les CVE critiques
