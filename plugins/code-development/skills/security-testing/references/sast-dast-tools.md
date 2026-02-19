# SAST, DAST et Outils de Sécurité

> Référence complète des outils d'analyse statique, dynamique et de scan de conteneurs. Configurations prêtes à l'emploi pour intégrer la sécurité dans chaque étape du pipeline CI/CD.

---

## SAST — Analyse Statique de Code

### Comparaison des outils SAST

| Critère | Semgrep | SonarQube | CodeQL | Checkmarx |
|---------|---------|-----------|--------|-----------|
| Licence | OSS / Pro | Community / Enterprise | Gratuit via GH | Payant |
| Langues | 30+ | 30+ | 10+ | 35+ |
| Règles custom | Très facile (YAML) | Java complexe | QL (complexe) | Difficile |
| Faux positifs | Moyen | Moyen | Faible | Faible |
| Vitesse | Très rapide | Lent (compilation) | Lent | Très lent |
| Intégration CI | Native | Sonar Scanner | GitHub native | Plugin |
| Idéal pour | Règles métier custom | Qualité globale | Vulnérabilités profondes | Entreprise |

---

## Semgrep — Règles Custom TypeScript/Node.js

### Installation et configuration de base

```bash
# Installation
pip install semgrep
# ou via Homebrew
brew install semgrep

# Scan avec règles officielles OWASP
semgrep --config=p/owasp-top-ten .

# Scan avec règles Node.js
semgrep --config=p/nodejs-security .

# Scan et output SARIF pour GitHub
semgrep --config=p/owasp-top-ten --sarif --output=semgrep.sarif .
```

### Règles Semgrep custom

```yaml
# .semgrep/custom-rules.yml
rules:
  # Détection de console.log avec données potentiellement sensibles
  - id: no-sensitive-console-log
    patterns:
      - pattern: console.log($X)
      - metavariable-regex:
          metavariable: $X
          regex: '.*(password|token|secret|key|credential|auth).*'
    message: |
      Ne pas logger des données potentiellement sensibles. Variable : $X
    languages: [typescript, javascript]
    severity: WARNING
    metadata:
      category: security
      cwe: CWE-312

  # Détection d'eval() — risque d'injection de code
  - id: no-eval
    pattern: eval($X)
    message: "eval() est dangereux et permet l'injection de code arbitraire."
    languages: [typescript, javascript]
    severity: ERROR
    metadata:
      category: security
      cwe: CWE-95

  # Détection de req.query directement dans une requête SQL
  - id: sqli-req-query
    patterns:
      - pattern: |
          $DB.raw(`...${$REQ.query.$PARAM}...`)
      - pattern: |
          $DB.raw("..." + $REQ.query.$PARAM + "...")
    message: "Possible injection SQL : paramètre de requête utilisé directement dans raw()."
    languages: [typescript, javascript]
    severity: ERROR
    metadata:
      category: security
      cwe: CWE-89

  # Détection de secrets codés en dur
  - id: hardcoded-secret
    patterns:
      - pattern: |
          const $SECRET = "..."
      - metavariable-regex:
          metavariable: $SECRET
          regex: '.*(secret|password|api_key|token|private_key).*'
      - metavariable-regex:
          metavariable: $VALUE
          regex: '^(?!process\.env).*'
    message: "Secret potentiellement codé en dur. Utiliser des variables d'environnement."
    languages: [typescript, javascript]
    severity: ERROR
    metadata:
      category: security
      cwe: CWE-798

  # Détection de désactivation de validation SSL
  - id: no-ssl-verify-false
    patterns:
      - pattern: |
          { rejectUnauthorized: false }
      - pattern: |
          NODE_TLS_REJECT_UNAUTHORIZED = "0"
    message: "La désactivation de la validation SSL est interdite en production."
    languages: [typescript, javascript]
    severity: ERROR

  # Path traversal via req.params
  - id: path-traversal
    patterns:
      - pattern: path.join($BASE, $REQ.params.$PARAM)
      - pattern-not: path.join($BASE, path.basename($REQ.params.$PARAM))
    message: "Risque de path traversal. Utiliser path.basename() pour assainir le paramètre."
    languages: [typescript, javascript]
    severity: ERROR
    metadata:
      cwe: CWE-22
```

### Intégration dans le pipeline CI

```yaml
# .github/workflows/semgrep.yml
name: Semgrep Security Scan

on:
  pull_request: {}
  push:
    branches: [main, develop]

jobs:
  semgrep:
    name: Semgrep Scan
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      - name: Run Semgrep
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/owasp-top-ten
            p/nodejs-security
            p/typescript
            .semgrep/custom-rules.yml
          generateSarif: "1"

      - name: Upload SARIF to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep.sarif
        if: always()
```

---

## SonarQube — Quality Gates Sécurité

### Configuration sonar-project.properties

```properties
# sonar-project.properties
sonar.projectKey=my-api
sonar.projectName=My API
sonar.sources=src
sonar.tests=src
sonar.test.inclusions=**/*.test.ts,**/*.spec.ts
sonar.typescript.lcov.reportPaths=coverage/lcov.info
sonar.exclusions=node_modules/**,dist/**,coverage/**

# Seuils de sécurité
sonar.security.hotspots.inheritanceMode=CHILD

# Quality Gate personnalisé (via API ou UI)
# Conditions bloquantes pour les PRs :
# - Nouvelles vulnérabilités : 0
# - Nouveaux Security Hotspots non reviewés : 0
# - New code coverage < 80%
# - New duplications > 3%
```

### Bloquer les PRs via Quality Gate

```yaml
# .github/workflows/sonarqube.yml
name: SonarQube Analysis

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Shallow clones désactivés pour l'analyse complète

      - name: Run Tests with Coverage
        run: npm ci && npm run test:coverage

      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@v2
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

      - name: SonarQube Quality Gate Check
        uses: SonarSource/sonarqube-quality-gate-action@v1
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        # Cette action échoue si le Quality Gate n'est pas passé → PR bloquée
```

---

## GitHub Advanced Security — CodeQL

### Activation et configuration

```yaml
# .github/workflows/codeql.yml
name: CodeQL Analysis

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * 1' # Scan hebdomadaire le lundi à 2h

jobs:
  analyze:
    name: Analyze (${{ matrix.language }})
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      matrix:
        language: [javascript-typescript]

    steps:
      - uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: +security-extended,security-and-quality
          # security-extended inclut des requêtes supplémentaires OWASP

      - name: Autobuild
        uses: github/codeql-action/autobuild@v3

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{ matrix.language }}"
          upload: true
```

### Secret Scanning et Dependency Review

```yaml
# .github/workflows/dependency-review.yml
name: Dependency Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Dependency Review
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: moderate
          deny-licenses: GPL-3.0, AGPL-3.0 # Licences interdites
          comment-summary-in-pr: always
```

```yaml
# .github/secret_scanning.yml (configuration du secret scanning)
# Dans les paramètres du dépôt → Security → Secret scanning
# Activer :
# - Secret scanning alerts
# - Push protection (bloque le push si un secret est détecté)
# - Validity checks
```

---

## DAST — OWASP ZAP

### Baseline Scan (passif — adapté à la CI)

```bash
# Scan passif (aucune modification sur l'application)
docker run --rm \
  -v $(pwd)/reports:/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t https://staging.example.com \
  -r zap-baseline-report.html \
  -J zap-baseline-report.json \
  -x zap-baseline-report.xml \
  -a # Inclure les alertes de niveau Alpha
```

### API Scan avec spécification OpenAPI

```bash
# Scan d'API avec la spécification OpenAPI (Swagger)
docker run --rm \
  -v $(pwd):/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py \
  -t https://staging-api.example.com/openapi.json \
  -f openapi \
  -r zap-api-report.html \
  -J zap-api-report.json \
  -z "-configfile /zap/wrk/zap-config.yml"
```

```yaml
# zap-config.yml — Configuration ZAP pour l'API scan
replacer.full_list(0).description=auth_token
replacer.full_list(0).enabled=true
replacer.full_list(0).matchtype=REQ_HEADER
replacer.full_list(0).matchstr=Authorization
replacer.full_list(0).regex=false
replacer.full_list(0).replacement=Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### ZAP en CI/CD avec authentification

```yaml
# .github/workflows/zap-scan.yml
name: OWASP ZAP Security Scan

on:
  schedule:
    - cron: '0 3 * * *' # Scan nocturne quotidien
  workflow_dispatch:

jobs:
  zap-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to staging
        run: echo "Staging deployment step here"

      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.12.0
        with:
          target: 'https://staging.example.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a -j'
          fail_action: true # Fail si des alertes High sont trouvées

      - name: ZAP API Scan
        uses: zaproxy/action-api-scan@v0.7.0
        with:
          target: 'https://staging-api.example.com/openapi.json'
          format: openapi
          fail_action: true

      - name: Upload ZAP Report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: zap-reports
          path: report_html.html
```

```tsv
# .zap/rules.tsv — Personnalisation des alertes ZAP
# ID	IGNORE/WARN/FAIL	Description
10202	WARN	Absence of Anti-CSRF Tokens (SPA avec JWT = acceptable)
10016	WARN	Web Browser XSS Protection Not Enabled (géré par Helmet)
10035	FAIL	Strict-Transport-Security Header Not Set
90022	FAIL	Application Error Disclosure
40012	FAIL	Cross Site Scripting (Reflected)
40014	FAIL	Cross Site Scripting (Persistent)
40018	FAIL	SQL Injection
40019	WARN	SQL Injection - MySQL
```

---

## Burp Suite — Workflow de Test Manuel

### Configuration du proxy

```bash
# Configuration du proxy Burp Suite (port 8080 par défaut)
# Dans le navigateur ou curl :
curl --proxy http://127.0.0.1:8080 \
     --cacert ~/.burp/burp_ca.der \
     https://target.example.com/api/endpoint

# Installation du certificat CA Burp
# Télécharger depuis http://burp/cert
# macOS : sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain burp_ca.der
```

### Active Scanner — Configuration recommandée

```
Burp Suite Pro → Scanner → Scan Configuration :

Insertion Points :
  ✅ URL parameters
  ✅ Body parameters
  ✅ HTTP headers (sauf Host)
  ✅ Cookie parameters
  ✅ JSON/XML body values
  ❌ Path parameters (risque de 404 en masse)

Checks actifs à prioriser :
  ✅ SQL injection
  ✅ XSS (reflected + stored)
  ✅ Path traversal
  ✅ Server-side template injection
  ✅ SSRF
  ✅ XXE
  ❌ DoS checks (environnement de staging uniquement)
```

### Intruder — Brute force et fuzzing

```
Burp Intruder → Payload sets pour tests d'authentification :

  Type : Sniper (1 position variable)
  Position : valeur du paramètre password
  Payload : fichier wordlist (rockyou.txt filtré sur top 1000)

  Throttle : 500ms entre les requêtes (éviter de bloquer le compte)
  Grep Match : "Invalid credentials" (identifier les échecs)
  Grep Extract : Extraire le session token pour détecter un changement

Repeater — Tests manuels répétés :
  - Modifier les headers Authorization
  - Tester les contournements d'authentification
  - Vérifier les comportements différenciés (timing attacks)
```

---

## Nikto — Scan de Vulnérabilités Web

```bash
# Scan basique
nikto -h https://target.example.com

# Scan avec authentification HTTP Basic
nikto -h https://target.example.com -id user:password

# Scan en limitant les faux positifs (mode SSL)
nikto -h https://target.example.com -ssl -Tuning 1234bde

# Output en format XML pour intégration
nikto -h https://target.example.com -Format xml -o nikto-report.xml

# Tuning flags utiles :
# 1 : File upload
# 2 : Misconfiguration
# 3 : Information disclosure
# 4 : Injection (XSS/HTML)
# b : Software identification
# d : Remote file retrieval (server-side)
# e : Denial of service
```

---

## Sécurité des APIs — OWASP API Top 10

### Tests Postman pour la sécurité des APIs

```javascript
// Collection Postman — Tests de sécurité automatisés

// Test 1 : Vérification des headers de sécurité
pm.test("Security headers présents", function() {
  pm.expect(pm.response.headers.get("X-Content-Type-Options")).to.equal("nosniff");
  pm.expect(pm.response.headers.get("X-Frame-Options")).to.equal("DENY");
  pm.expect(pm.response.headers.get("Strict-Transport-Security")).to.not.be.undefined;
  pm.expect(pm.response.headers.get("Content-Security-Policy")).to.not.be.undefined;
});

// Test 2 : Pas d'exposition de stack trace
pm.test("Pas de stack trace exposée", function() {
  const body = pm.response.text();
  pm.expect(body).to.not.include("Error:");
  pm.expect(body).to.not.include("at Object.");
  pm.expect(body).to.not.include("node_modules");
});

// Test 3 : Rate limiting en place
pm.test("Rate limit headers présents", function() {
  const rateLimitRemaining = pm.response.headers.get("RateLimit-Remaining")
    || pm.response.headers.get("X-RateLimit-Remaining");
  pm.expect(rateLimitRemaining).to.not.be.undefined;
});

// Test 4 : Pas de données sensibles exposées
pm.test("Pas de données sensibles dans la réponse", function() {
  const body = pm.response.json();
  const bodyStr = JSON.stringify(body);
  pm.expect(bodyStr).to.not.include("password");
  pm.expect(bodyStr).to.not.include("passwordHash");
  pm.expect(bodyStr).to.not.include("secret");
});

// Test 5 : IDOR — accès à une ressource d'un autre utilisateur
pm.test("IDOR : ressource inaccessible pour un autre utilisateur", function() {
  // Doit retourner 403 ou 404, jamais 200 avec des données
  pm.expect([403, 404]).to.include(pm.response.code);
});
```

### API Fuzzing avec wfuzz

```bash
# Fuzzing des paramètres d'API
wfuzz -c \
  -z file,/usr/share/wordlists/wfuzz/general/common.txt \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --hc 404 \
  https://api.example.com/FUZZ

# Fuzzing d'IDs numériques (IDOR)
wfuzz -c \
  -z range,1-1000 \
  -H "Authorization: Bearer USER_A_TOKEN" \
  --hc 403,404 \
  https://api.example.com/orders/FUZZ
  # Alerter sur les 200 qui ne correspondent pas aux commandes de l'utilisateur A
```

---

## Scan de Conteneurs

### Trivy — Scan d'images Docker

```bash
# Scan complet d'une image (vulnérabilités + configs + secrets)
trivy image --severity HIGH,CRITICAL \
  --format sarif \
  --output trivy-results.sarif \
  myapp:latest

# Scan du code source (IaC, secrets, vulnérabilités)
trivy fs --security-checks vuln,secret,config \
  --format json \
  --output trivy-fs-results.json \
  .

# Scan du Dockerfile et des configs Kubernetes
trivy config --format table ./k8s/

# Bloquer le build si vulnérabilités critiques
trivy image --exit-code 1 --severity CRITICAL myapp:latest
```

### Grype — Alternative légère

```bash
# Installation
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Scan d'une image
grype myapp:latest --fail-on critical

# Scan d'un SBOM existant
grype sbom:./sbom.json

# Ignorer des CVE spécifiques (avec justification)
cat > .grype.yml << EOF
ignore:
  - vulnerability: CVE-2023-XXXXX
    reason: "Mitigated by WAF rule, fix pending in upstream"
    expires: "2024-06-01"
EOF
```

### Docker Scout (intégré à Docker Desktop)

```bash
# Analyse des vulnérabilités
docker scout cves myapp:latest

# Recommandations de mise à jour de l'image de base
docker scout recommendations myapp:latest

# Comparaison entre deux versions
docker scout compare myapp:v1.0 myapp:v1.1

# Intégration CI avec seuil de blocage
docker scout cves --exit-code --only-severity critical,high myapp:latest
```

---

## SBOM — Software Bill of Materials

### Génération avec Syft

```bash
# Installation
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

# Générer un SBOM en format CycloneDX (standard OWASP)
syft myapp:latest -o cyclonedx-json=sbom-cyclonedx.json

# Générer un SBOM en format SPDX (standard Linux Foundation)
syft myapp:latest -o spdx-json=sbom-spdx.json

# Générer pour le code source (pas l'image)
syft dir:. -o cyclonedx-json=sbom-source.json

# Générer et attacher à l'image avec cosign (signature)
syft myapp:latest -o cyclonedx-json=sbom.json
cosign attest --predicate sbom.json --type cyclonedx myapp@sha256:...
```

---

## Pipeline CI/CD de Sécurité Complet

```yaml
# .github/workflows/security-pipeline.yml
name: Full Security Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # 1. Analyse statique de code
  sast:
    name: SAST — Semgrep + CodeQL
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Semgrep Scan
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/owasp-top-ten
            p/nodejs-security
            .semgrep/custom-rules.yml
          generateSarif: "1"

      - name: Upload Semgrep SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep.sarif
        if: always()

  # 2. Scan des dépendances
  dependency-check:
    name: Dependency Vulnerability Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm ci

      - name: npm audit
        run: npm audit --audit-level=high

      - name: Snyk Security Scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high --fail-on=upgradable

  # 3. Scan des secrets
  secret-scan:
    name: Secret Detection
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Historique complet pour Gitleaks

      - name: Gitleaks Secret Scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # 4. Build et scan de l'image Docker
  container-scan:
    name: Container Security Scan
    runs-on: ubuntu-latest
    needs: [sast, dependency-check]
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker Image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Trivy Image Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
          exit-code: '1'
          severity: CRITICAL,HIGH

      - name: Upload Trivy Results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: trivy-results.sarif
        if: always()

      - name: Generate SBOM
        run: |
          syft myapp:${{ github.sha }} -o cyclonedx-json=sbom.json

      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.json

  # 5. DAST sur l'environnement de staging
  dast:
    name: DAST — OWASP ZAP
    runs-on: ubuntu-latest
    needs: [container-scan]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Staging
        run: echo "Déploiement staging ici"

      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.12.0
        with:
          target: 'https://staging.example.com'
          fail_action: true

      - name: ZAP API Scan
        uses: zaproxy/action-api-scan@v0.7.0
        with:
          target: 'https://staging-api.example.com/openapi.json'
          format: openapi
          fail_action: true

  # 6. Rapport de synthèse
  security-report:
    name: Security Report
    runs-on: ubuntu-latest
    needs: [sast, dependency-check, secret-scan, container-scan, dast]
    if: always()
    steps:
      - name: Create Security Summary
        run: |
          echo "## Security Scan Summary" >> $GITHUB_STEP_SUMMARY
          echo "| Check | Status |" >> $GITHUB_STEP_SUMMARY
          echo "|-------|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| SAST (Semgrep) | ${{ needs.sast.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Dependencies | ${{ needs.dependency-check.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Secret Scan | ${{ needs.secret-scan.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Container Scan | ${{ needs.container-scan.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| DAST (ZAP) | ${{ needs.dast.result }} |" >> $GITHUB_STEP_SUMMARY
```

---

## Récapitulatif — Choix des outils par contexte

| Contexte | Outil recommandé | Pourquoi |
|----------|-----------------|----------|
| Startup / OSS | Semgrep + Trivy + ZAP | 100% gratuit, rapide à intégrer |
| Scale-up | Semgrep Pro + Snyk + ZAP | Meilleur support, Dashboard centralisé |
| Grande entreprise | SonarQube Enterprise + Checkmarx + Burp Enterprise | Intégration SSO, reporting avancé |
| Bug bounty / pentest | Burp Suite Pro + ZAP | Contrôle manuel, extensions |
| Kubernetes | Trivy Operator + Falco | Scan continu en cluster |
| Supply chain | Syft + Grype + Sigstore | SBOM + vérification d'intégrité |

**Priorité d'implémentation** : commencer par les secrets (Gitleaks pre-commit) → SAST (Semgrep) → dépendances (npm audit + Dependabot) → container scan (Trivy) → DAST (ZAP baseline). Chaque étape bloque la CI si des problèmes critiques sont détectés.
