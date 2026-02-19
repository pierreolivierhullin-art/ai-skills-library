---
name: security-testing
version: 1.0.0
description: >
  Application security testing, SAST static analysis, DAST dynamic testing, OWASP ZAP,
  Burp Suite, dependency scanning, secrets detection, SQL injection XSS CSRF prevention,
  security code review, pen testing, vulnerability assessment, OWASP Top 10,
  supply chain security, container scanning, security CI/CD pipeline, DevSecOps
---

# Security Testing — DevSecOps et OWASP

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu mets en place un pipeline de sécurité CI/CD (DevSecOps)
- Tu dois auditer une application pour les vulnérabilités OWASP Top 10
- Tu gères des secrets, API keys, credentials dans le code
- Tu dois scanner les dépendances pour les CVE connues
- Un pentest est requis avant un lancement ou une certification (SOC2, ISO27001)
- Tu veux intégrer du SAST/DAST dans ton workflow de développement

---

## OWASP Top 10 — Vulnérabilités Critiques

### A01 — Broken Access Control

```typescript
// ❌ Vulnérable : l'utilisateur peut accéder aux données d'un autre
app.get('/api/commandes/:id', async (req, res) => {
  const commande = await db.commandes.findById(req.params.id);
  res.json(commande); // N'importe qui peut voir n'importe quelle commande !
});

// ✅ Correct : vérifier que la ressource appartient à l'utilisateur authentifié
app.get('/api/commandes/:id', requireAuth, async (req, res) => {
  const commande = await db.commandes.findOne({
    where: {
      id: req.params.id,
      userId: req.user.id, // Forcer le filtre par user
    },
  });

  if (!commande) {
    return res.status(404).json({ error: 'Commande non trouvée' });
    // 404 plutôt que 403 pour ne pas révéler l'existence de la ressource
  }

  res.json(commande);
});
```

### A02 — Cryptographic Failures

```typescript
// ❌ Vulnérable : hash MD5 crackable en secondes
import crypto from 'crypto';
const hash = crypto.createHash('md5').update(password).digest('hex');

// ✅ Correct : bcrypt avec salt rounds adaptatifs
import bcrypt from 'bcrypt';
const SALT_ROUNDS = 12; // 2^12 itérations → ~300ms en 2025
const hash = await bcrypt.hash(password, SALT_ROUNDS);
const valid = await bcrypt.compare(passwordEntrée, hashStocké);

// ❌ Données sensibles en clair dans la DB
{ card_number: '4111111111111111', cvv: '123' }

// ✅ Chiffrement des données sensibles
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

function chiffrer(texte: string): { iv: string; données: string } {
  const iv = randomBytes(16);
  const cipher = createCipheriv('aes-256-gcm', Buffer.from(process.env.ENCRYPTION_KEY!, 'hex'), iv);
  const chiffré = Buffer.concat([cipher.update(texte, 'utf8'), cipher.final()]);
  return { iv: iv.toString('hex'), données: chiffré.toString('hex') };
}
```

### A03 — SQL Injection

```typescript
// ❌ Vulnérable : concaténation directe
const query = `SELECT * FROM users WHERE email = '${email}'`;
// email = "'; DROP TABLE users; --" → catastrophe

// ✅ Requêtes paramétrées (ORM ou prepared statements)
// Avec Drizzle ORM (safe par défaut)
const user = await db.select().from(users).where(eq(users.email, email));

// Avec pg raw (si nécessaire)
const result = await pool.query(
  'SELECT * FROM users WHERE email = $1',
  [email] // Jamais interpolé dans la string
);

// Avec Prisma
const user = await prisma.user.findUnique({ where: { email } });
```

### A07 — XSS (Cross-Site Scripting)

```typescript
// ❌ Vulnérable : dangerouslySetInnerHTML sans sanitisation
<div dangerouslySetInnerHTML={{ __html: contenuUtilisateur }} />

// ✅ Sanitiser avec DOMPurify avant injection HTML
import DOMPurify from 'dompurify';

const contenuPropre = DOMPurify.sanitize(contenuUtilisateur, {
  ALLOWED_TAGS: ['p', 'strong', 'em', 'a', 'ul', 'li'],
  ALLOWED_ATTR: ['href', 'rel'],
  FORCE_HTTPS: true,
});

<div dangerouslySetInnerHTML={{ __html: contenuPropre }} />

// Content Security Policy (défense en profondeur)
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self' 'nonce-{NONCE}'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "connect-src 'self' https://api.monapp.com",
    ].join('; '),
  },
];
```

---

## SAST — Analyse Statique de Code

### Semgrep — Règles Personnalisées

```yaml
# .semgrep/security.yml
rules:
  - id: no-hardcoded-secrets
    patterns:
      - pattern: |
          const $VAR = "sk_live_..."
      - pattern: |
          const $VAR = "AKIA..."
    message: "Secret potentiellement hardcodé dans $VAR"
    severity: ERROR
    languages: [javascript, typescript]

  - id: sql-injection-risk
    pattern: |
      `SELECT * FROM ${...}...`
    message: "Interpolation SQL potentiellement dangereuse"
    severity: WARNING
    languages: [javascript, typescript]

  - id: crypto-weak-algorithm
    patterns:
      - pattern: crypto.createHash('md5')
      - pattern: crypto.createHash('sha1')
    message: "Algorithme de hash faible pour les mots de passe"
    severity: ERROR
    languages: [javascript]
```

```yaml
# CI/CD — Semgrep dans GitHub Actions
# .github/workflows/sast.yml
name: SAST Security Scan
on: [push, pull_request]
jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/default
            p/javascript
            p/typescript
            p/nodejs
            p/owasp-top-ten
          publishToken: ${{ secrets.SEMGREP_APP_TOKEN }}
          auditOn: push
```

### ESLint Security Plugin

```javascript
// eslint.config.js
import security from 'eslint-plugin-security';
import noSecrets from 'eslint-plugin-no-secrets';

export default [
  {
    plugins: { security, 'no-secrets': noSecrets },
    rules: {
      'security/detect-eval-with-expression': 'error',
      'security/detect-non-literal-fs-filename': 'error',
      'security/detect-non-literal-regexp': 'warn',
      'security/detect-object-injection': 'warn',
      'security/detect-possible-timing-attacks': 'error',
      'no-secrets/no-secrets': ['error', { tolerance: 4.5 }],
    },
  },
];
```

---

## Gestion des Secrets

### Détection de Secrets dans le Code

```bash
# Gitleaks — scanner les secrets dans git
# Installation
brew install gitleaks

# Scanner le repo entier
gitleaks detect --source=. --verbose

# Pre-commit hook
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

```yaml
# CI/CD — TruffleHog dans GitHub Actions
# .github/workflows/secrets.yml
name: Secret Scanning
on: [push, pull_request]
jobs:
  trufflehog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: TruffleHog scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
```

### Rotation de Secrets Compromis

```bash
# Si un secret est détecté dans git :
# 1. Révoquer immédiatement le secret (API provider)
# 2. Générer un nouveau secret
# 3. Supprimer du code ET de l'historique git

# Supprimer de l'historique avec git-filter-repo
pip install git-filter-repo
git filter-repo --path-glob '*.env' --invert-paths
# OU pour un fichier spécifique avec le secret
git filter-repo --replace-text expressions.txt

# 4. Force push (coordonner avec l'équipe)
git push origin --force --all
git push origin --force --tags
```

---

## Dépendances — Scanning des CVE

### npm audit et OWASP Dependency-Check

```bash
# Audit npm
npm audit --audit-level=high

# Correction automatique (quand safe)
npm audit fix

# Rapport JSON pour CI
npm audit --json > audit-report.json
```

```yaml
# Snyk dans CI/CD
# .github/workflows/deps.yml
name: Dependency Security
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 9 * * 1' # Chaque lundi
jobs:
  snyk:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high --fail-on=all
```

### Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
      day: monday
      time: "09:00"
    open-pull-requests-limit: 10
    groups:
      patch-updates:
        update-types: ["patch"]
      minor-updates:
        update-types: ["minor"]
    ignore:
      - dependency-name: "some-legacy-package"
        update-types: ["version-update:semver-major"]
```

---

## DAST — Tests Dynamiques

### OWASP ZAP Baseline Scan

```yaml
# .github/workflows/dast.yml
name: DAST Security Scan
on:
  schedule:
    - cron: '0 2 * * 0' # Chaque dimanche
  workflow_dispatch:
jobs:
  zap-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Démarrer l'application
        run: |
          npm ci && npm run build
          npm run start &
          sleep 10

      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.9.0
        with:
          target: 'http://localhost:3000'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'

      - name: Upload ZAP Report
        uses: actions/upload-artifact@v4
        with:
          name: zap-report
          path: report_html.html
```

---

## Container Security

```dockerfile
# Dockerfile sécurisé
FROM node:20-alpine AS builder
# Alpine = image minimale (moins de surface d'attaque)

WORKDIR /app
COPY package*.json ./
# Installer seulement les dépendances de prod
RUN npm ci --only=production && npm cache clean --force

COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

# Ne pas tourner en root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules

USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

```yaml
# Scanner l'image Docker avec Trivy
- name: Scan Docker image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'monapp:${{ github.sha }}'
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'
    exit-code: '1' # Fail le build si vulnérabilités critiques
```

---

## Security Headers Checklist

```typescript
// next.config.js — headers de sécurité complets
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
];
// Score securityheaders.com : A+ visé
```

---

## Références

- `references/owasp-top10.md` — OWASP Top 10 détaillé avec exemples d'attaques et fixes
- `references/sast-dast-tools.md` — Semgrep, Snyk, ZAP, Burp Suite, Trivy en détail
- `references/secrets-management.md` — HashiCorp Vault, AWS Secrets Manager, rotation, CI/CD
- `references/case-studies.md` — 4 cas : injection SQL détectée, secret exposé GitHub, pentest résultats
