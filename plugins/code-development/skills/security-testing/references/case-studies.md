# Études de Cas — Sécurité Applicative en Production

> Quatre incidents réels reconstitués (entreprises anonymisées) pour illustrer la découverte, l'impact, la remédiation et les leçons apprises. Chaque cas est traité avec le niveau de détail qu'une équipe technique doit connaître pour éviter les mêmes erreurs.

---

## Cas 1 — Injection SQL Découverte lors d'un Pentest (E-commerce)

### Contexte

**Secteur** : E-commerce B2C, 80 000 commandes par mois.
**Stack** : Node.js / Express, MySQL, hébergement AWS EC2 (pas d'RDS).
**Équipe** : 12 développeurs, aucun process de sécurité formalisé.
**Déclencheur** : Premier pentest externe mandaté avant une levée de fonds Serie A, réalisé par une société spécialisée pendant 5 jours.

### Découverte — Jour 2 du pentest

Le pentesteur analyse l'endpoint de recherche produits. Un paramètre `sort` attire son attention.

**Requête originale** :
```
GET /api/products?category=shoes&sort=price_asc
```

**Test d'injection** :
```
GET /api/products?category=shoes&sort=price_asc' AND SLEEP(5)--
```

La réponse prend exactement 5 secondes → confirmation d'une injection SQL temporelle (blind time-based SQLi).

**Code vulnérable identifié** :
```typescript
// src/routes/products.ts — tel que trouvé lors du pentest
app.get('/api/products', async (req, res) => {
  const { category, sort, page = 1, limit = 20 } = req.query;

  // ❌ Construction directe de la chaîne ORDER BY
  // Le paramètre "sort" n'est pas validé ni paramétré
  const orderClause = sort ? `ORDER BY ${sort}` : 'ORDER BY created_at DESC';

  const query = `
    SELECT id, name, price, image_url, stock
    FROM products
    WHERE category = ?
    ${orderClause}
    LIMIT ? OFFSET ?
  `;

  const results = await db.query(query, [category, limit, (page - 1) * limit]);
  return res.json(results);
});
```

**La clause `ORDER BY` ne peut pas être paramétrée en SQL standard**, ce qui a conduit l'équipe à l'interpoler directement.

### Blast Radius

L'outil `sqlmap` a été utilisé (avec autorisation, dans le cadre du pentest) pour mesurer l'étendue :

```bash
sqlmap -u "https://shop.example.com/api/products?sort=price_asc" \
  --dbms=mysql \
  --level=3 \
  --risk=2 \
  --dump-all \
  --batch

# Résultat après 45 minutes :
# [*] Database: shop_production
# [*] Table: users (47,832 records) → emails, password hashes (MD5 !), adresses
# [*] Table: orders (380,000 records) → historique complet, adresses de livraison
# [*] Table: payment_tokens (47,000 records) → tokens Stripe (heureusement pas les PAN)
# [*] Privilèges DB : SELECT, INSERT, UPDATE sur toute la base
#     (l'utilisateur MySQL avait trop de droits)
```

**Impact potentiel** :
- 47 832 comptes utilisateurs avec emails et mots de passe MD5 (cassables par rainbow table).
- Historique d'achat complet de 380 000 commandes.
- Tokens de paiement Stripe (non les numéros de carte — mitigé par Stripe).
- Données personnelles soumises au RGPD → obligation de notification à la CNIL sous 72h.

Le pentesteur a stoppé l'extraction après 500 lignes (pratique standard) et a remis le rapport immédiatement.

### Remédiation Immédiate (J0 → J3)

**J0 — Heure 0 : War room déclenché**

```bash
# Vérification de l'absence d'exploitation réelle (logs d'accès nginx)
grep -E "sort=.*'|sort=.*SLEEP|sort=.*UNION|sort=.*--" /var/log/nginx/access.log | \
  grep -v "pentest-ip-range" | wc -l
# Résultat : 0 → aucune exploitation externe détectée avant le pentest
```

**J0 — Heure 2 : Patch d'urgence**

```typescript
// ✅ Correction : validation par liste blanche des paramètres de tri
const ALLOWED_SORT_FIELDS = new Map<string, string>([
  ['price_asc',    'price ASC'],
  ['price_desc',   'price DESC'],
  ['name_asc',     'name ASC'],
  ['name_desc',    'name DESC'],
  ['newest',       'created_at DESC'],
  ['bestseller',   'sales_count DESC'],
]);

app.get('/api/products', async (req, res) => {
  const { category, sort, page = 1, limit = 20 } = req.query;

  const sortClause = ALLOWED_SORT_FIELDS.get(String(sort)) ?? 'created_at DESC';

  // ✅ ORDER BY construit depuis la liste blanche côté serveur
  const results = await db('products')
    .where('category', String(category))
    .orderByRaw(sortClause)  // Valeur provenant de notre Map, pas de l'utilisateur
    .limit(Number(limit))
    .offset((Number(page) - 1) * Number(limit))
    .select('id', 'name', 'price', 'image_url', 'stock');

  return res.json(results);
});
```

**J1 — Audit complet des endpoints**

```bash
# Recherche systématique des patterns dangereux dans tout le codebase
grep -rn "db.query\|db.raw\|mysql.query" src/ | grep -v "?"
# → 3 autres occurrences trouvées dans les routes admin (moins exposées)
```

**J2 — Migration des mots de passe**

```typescript
// Remplacement de MD5 par bcrypt lors de la prochaine connexion
// (impossible de migrer sans la connaissance des mots de passe en clair)
async function loginHandler(req, res) {
  const user = await db('users').where({ email: req.body.email }).first();

  // Si le hash est MD5 (32 hex chars), comparer avec MD5 et re-hacher
  if (user.password_hash.match(/^[a-f0-9]{32}$/)) {
    const md5Hash = crypto.createHash('md5').update(req.body.password).digest('hex');
    if (md5Hash !== user.password_hash) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    // Migration transparente vers bcrypt
    const bcryptHash = await bcrypt.hash(req.body.password, 12);
    await db('users').where({ id: user.id }).update({ password_hash: bcryptHash });
  } else {
    // Hash bcrypt — comparaison normale
    if (!await bcrypt.compare(req.body.password, user.password_hash)) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
  }
  // ...
}
```

**J3 — Notification CNIL**

Notification envoyée dans les 72h (obligation RGPD Art. 33) avec :
- Description de la vulnérabilité.
- Mesures correctives déjà appliquées.
- Absence d'exploitation confirmée par les logs.
- Plan de hardening à 30 jours.

### Hardening Post-Incident (J4 → J30)

```yaml
# Mesures implémentées dans les 30 jours suivants :

Technique :
  ✅ Semgrep intégré en CI (détection injection dans les futures PRs)
  ✅ Principe de moindre privilège : utilisateur DB avec SELECT uniquement
     pour les routes publiques, utilisateur séparé pour les écritures
  ✅ Audit de toutes les requêtes SQL (outil : knex-logger en staging)
  ✅ WAF AWS (rate limiting + règles SQLi de base)
  ✅ Migration vers RDS avec encryption at rest

Process :
  ✅ Code review obligatoire avec checklist sécurité pour les PRs touchant la DB
  ✅ Pentest annuel contractualisé
  ✅ Formation OWASP Top 10 pour toute l'équipe (demi-journée)

Monitoring :
  ✅ Alerte sur les requêtes SQL longues (> 2s) → détection des SLEEP()
  ✅ Dashboard Datadog sur les 4xx/5xx par endpoint
```

### Leçons Apprises

1. **`ORDER BY` est le talon d'Achille des requêtes paramétrées** : les colonnes de tri ne peuvent pas être paramétrées. La seule solution sûre est la liste blanche côté serveur.
2. **MD5 pour les mots de passe est inacceptable en 2024** : même sans compromission directe, les hashes MD5 sont cassables en minutes. Migration vers bcrypt obligatoire.
3. **Le pentest externe trouve ce que les développeurs ne voient plus** : l'équipe avait regardé ce code des dizaines de fois sans voir l'injection.
4. **Les privilèges DB trop larges amplifient les dégâts** : avec un compte SELECT-only, l'injection aurait permis la lecture mais pas l'écriture.

---

## Cas 2 — Clé API Exposée sur GitHub (Startup SaaS)

### Contexte

**Secteur** : SaaS B2B, outil d'analyse marketing, 200 clients.
**Stack** : Next.js, Vercel, OpenAI API, SendGrid, Stripe.
**Équipe** : 3 développeurs fondateurs, tous CTO en pratique.
**Déclencheur** : Email de GitHub Security à 14h37 un mercredi : "We have found a potentially sensitive token."

### Timeline de l'Exposition

```
T-180 jours : Commit initial du projet, .env inclus par erreur dans le premier push
              (le .gitignore n'avait pas encore été configuré pour les .env)

T-90 jours  : Le dépôt est passé en public "pour partager avec un freelance"
              → La clé OpenAI (sk-...) et la clé Stripe live (sk_live_...) deviennent publiques

T-0         : GitHub Secret Scanning détecte les clés et envoie l'alerte
              (délai de détection GitHub : environ 90 jours — le secret était en cache)

T+0h15      : Le CTO reçoit l'email, le lit, fait une pause de 5 minutes

T+0h20      : Premier réflexe MAUVAIS : suppression du fichier .env sur GitHub
              (le fichier est supprimé mais RESTE dans l'historique git)

T+0h25      : Vérification du dashboard OpenAI → 47$ de charges inattendues
              (quelqu'un a utilisé la clé pour générer du texte)

T+0h30      : Vérification du dashboard Stripe → aucune transaction suspecte
              (la clé Stripe était en mode live mais aucune tentative détectée)

T+0h35      : RÉVOCATION immédiate des deux clés (OpenAI + Stripe)
```

### Actions Immédiates

**Étape 1 — Révocation (priorité absolue)**

```bash
# Clé OpenAI — Dashboard platform.openai.com → API keys → Revoke
# Clé Stripe — Dashboard dashboard.stripe.com → Developers → API keys → Roll key

# Vérification que les clés ne fonctionnent plus
curl -s https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-old-key-here" | jq .error
# → {"message": "Incorrect API key provided"}
```

**Étape 2 — Nettoyage de l'historique git (BFS Sensitive)**

```bash
# ⚠️  Opération destructive — informer TOUTE l'équipe avant

# Identifier les commits contenant le secret
git log --all --oneline -- .env
# → abc1234 Initial commit (il y a 180 jours)

# Option 1 : git-filter-repo (recommandé — plus rapide que BFG)
pip install git-filter-repo

git filter-repo --path .env --invert-paths --force
# Supprime .env de TOUT l'historique

# Ou pour ne supprimer que les lignes contenant le secret :
git filter-repo --replace-text <(echo 'sk-oldkey==>REMOVED_SECRET') --force

# Option 2 : BFG Repo Cleaner (Java)
java -jar bfg.jar --delete-files .env
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Forcer le push (TOUTE l'équipe doit re-cloner après)
git push origin --force --all
git push origin --force --tags
```

**Étape 3 — Vérification post-nettoyage**

```bash
# S'assurer que le secret n'est plus accessible
git log --all -p | grep "sk-"
# → Aucun résultat

# Mais attention : GitHub peut garder des copies en cache pendant 3 mois
# → Contacter GitHub Support pour demander la purge du cache
# → URL: https://support.github.com/contact
```

**Étape 4 — Audit des accès**

```bash
# OpenAI — vérifier l'usage pendant la période d'exposition
# Dashboard → Usage → Filtrer par date (T-90j à T-0)
# → 47$ d'usage non reconnu = compromission confirmée

# Stripe — vérifier les logs d'API
curl https://api.stripe.com/v1/events?limit=100&type=charge.created \
  -u sk_live_OLD_KEY: | jq '.data[].created' | xargs -I{} date -r {}
# → Aucune charge suspecte dans la période

# Analyser les logs de l'application (Vercel logs)
vercel logs --since 90d | grep "openai\|stripe" | grep -v "200"
```

### Mise en Place du Secret Scanning

```yaml
# Après l'incident : configuration complète anti-récidive

# 1. .gitignore renforcé
cat >> .gitignore << 'EOF'
# Secrets — JAMAIS commités
.env
.env.*
!.env.example
*.pem
*.key
*.p12
*.pfx
service-account.json
credentials.json
EOF

# 2. Vérification que .env n'est pas déjà tracké
git ls-files --error-unmatch .env 2>/dev/null && git rm --cached .env

# 3. Pre-commit hook avec Gitleaks
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks

# Installation
pre-commit install
```

```bash
# Test du hook
echo "OPENAI_API_KEY=sk-test123456789012345678901234" >> test.env
git add test.env
git commit -m "test"
# → 🚨 Gitleaks détecte et bloque le commit !
# ► No commit created

# Nettoyage
git checkout -- test.env
rm test.env
```

### .env.example — Template Public Sécurisé

```bash
# .env.example (commité dans le dépôt, sans valeurs réelles)
NODE_ENV=development

# OpenAI
OPENAI_API_KEY=sk-REPLACE_WITH_YOUR_KEY

# Stripe
STRIPE_PUBLIC_KEY=pk_test_REPLACE_WITH_YOUR_KEY
STRIPE_SECRET_KEY=sk_test_REPLACE_WITH_YOUR_KEY

# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/myapp_dev

# Email (SendGrid)
SENDGRID_API_KEY=SG.REPLACE_WITH_YOUR_KEY

# JWT
JWT_SECRET=REPLACE_WITH_32_CHAR_MINIMUM_RANDOM_STRING
```

### Leçons Apprises

1. **La suppression du fichier ne suffit pas** : git conserve l'historique. `git filter-repo` est obligatoire pour une suppression réelle.
2. **GitHub Secret Scanning a un délai** : la clé était exposée depuis 90 jours avant détection. La push protection (activée à l'avance) aurait bloqué le push initial.
3. **Les clés Stripe live ne doivent jamais être dans le code** : même en dépôt privé. Utiliser les clés de test en développement, les clés live uniquement via variables d'environnement Vercel/Heroku.
4. **L'audit d'usage révèle la compromission** : 47$ non reconnus sur OpenAI = la clé a été utilisée par un tiers. Toujours auditer l'usage historique après une exposition.
5. **Coût financier réel** : 47$ de charges OpenAI + 2 jours de travail développeur = environ 2 000€ d'impact direct. Un préjudice réputationnel potentiellement bien plus important.

---

## Cas 3 — Mise en Place DevSecOps (Scale-up, 20 Développeurs)

### Contexte

**Secteur** : Fintech B2B, plateforme de gestion de trésorerie.
**Stack** : Node.js / NestJS, React, PostgreSQL, Kubernetes (EKS), AWS.
**Équipe** : 20 développeurs, 1 DevOps, 0 profil sécurité.
**Déclencheur** : Exigence contractuelle d'un grand compte (banque) : ISO 27001 ou SOC 2 Type II dans les 12 mois.
**Durée de la transformation** : 3 mois pour le pipeline, 12 mois pour la certification.

### Audit Initial — État des Lieux (Semaine 1)

```
Résultats de l'audit de départ :

Code :
  ✗ Aucun SAST — 0 règle de sécurité en CI
  ✗ npm audit bloqué dans la CI : 47 vulnérabilités (3 critiques, 12 high)
  ✗ 14 secrets identifiés dans l'historique git (tokens, passwords)
  ✗ Aucune validation des entrées sur 60% des endpoints

Infrastructure :
  ✗ Images Docker rootées
  ✗ Secrets en variables d'environnement en clair dans les manifests K8s
  ✗ Pas de network policies dans Kubernetes
  ✗ RDS sans chiffrement at-rest (base de données financières !)

Process :
  ✗ Code review sans checklist sécurité
  ✗ Aucun pentest réalisé
  ✗ Pas de process de gestion des incidents de sécurité
  ✗ Aucune formation sécurité pour les développeurs

Score OWASP SAMM (Software Assurance Maturity Model) : 1.1 / 3.0
```

### Roadmap 3 Mois

#### Mois 1 — Fondations (Quick Wins)

**Semaines 1-2 : Nettoyage des secrets et CI bloquante**

```bash
# Semaine 1 : nettoyage de l'historique git
git filter-repo --replace-text secrets.txt --force

# Rotation de tous les secrets identifiés
# → 14 secrets révoqués et régénérés en 1 journée (war room)

# Semaine 2 : Gitleaks pre-commit pour TOUS les développeurs
# Script d'installation envoyé à l'équipe :
curl -s https://raw.githubusercontent.com/gitleaks/gitleaks/main/scripts/install.sh | bash
pre-commit install
```

**Semaines 3-4 : Semgrep en CI (mode warning d'abord)**

```yaml
# Phase 1 : Semgrep en mode "warn only" (ne bloque pas les PRs)
# → collecter les métriques de base sans bloquer le travail

# Résultats après 2 semaines :
# - 847 findings en mode warning
# - 23 findings CRITICAL (injection, hardcoded secrets)
# - 156 findings HIGH (XSS, open redirect, missing auth)
# - 668 findings MEDIUM/LOW

# Plan : corriger les CRITICAL en priorité, puis bloquer la CI sur CRITICAL
```

**Sélection des outils (benchmark de 2 semaines)**

| Outil évalué | Score (1-5) | Décision | Raison |
|-------------|------------|---------|--------|
| Semgrep OSS | 4.5 | ✅ Retenu | Règles custom faciles, rapide |
| SonarQube CE | 3.0 | ❌ Écarté | Trop lent, UI complexe pour l'équipe |
| Snyk | 4.0 | ✅ Retenu | Dépendances + images + IaC |
| OWASP ZAP | 4.0 | ✅ Retenu | DAST gratuit, intégration CI native |
| Checkmarx | 3.5 | ❌ Écarté | Trop cher, ROI faible pour 20 devs |
| Dependabot | 4.5 | ✅ Retenu | Natif GitHub, zéro friction |

#### Mois 2 — Pipeline Complet

```yaml
# Pipeline de sécurité déployé en Mois 2
# .github/workflows/security.yml

name: Security Pipeline
on: [push, pull_request]

jobs:
  secret-scan:
    steps:
      - uses: gitleaks/gitleaks-action@v2  # Bloquant dès le Mois 1

  sast:
    steps:
      - name: Semgrep
        # Mode bloquant sur CRITICAL uniquement (Semaine 5)
        # Mode bloquant sur HIGH à partir de la Semaine 8
        run: semgrep --config=.semgrep/ --error --severity=ERROR .

  dependency-scan:
    steps:
      - run: npm audit --audit-level=high  # Bloquant
      - uses: snyk/actions/node@master     # Bloquant sur HIGH+

  container-scan:
    steps:
      - name: Trivy
        run: trivy image --exit-code 1 --severity CRITICAL myapp:${{ github.sha }}

  dast:
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: zaproxy/action-baseline@v0.12.0
        with:
          target: 'https://staging.fintech.example.com'
```

**Migration des secrets vers AWS Secrets Manager**

```typescript
// Avant (Mois 1) : secrets en variables d'environnement K8s (en clair dans les manifests)
// Après (Mois 2) : AWS Secrets Manager avec External Secrets Operator

// external-secrets.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: myapp-env-secrets
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: fintech/production/database
        property: connection_url
    - secretKey: STRIPE_SECRET_KEY
      remoteRef:
        key: fintech/production/stripe
        property: secret_key
```

#### Mois 3 — Culture et Durabilité

**Programme Security Champions**

```
Structure du programme :

1. Sélection (Semaine 9) :
   - 1 champion par équipe (4 équipes = 4 champions)
   - Volontariat + validation du manager
   - 10% du temps dédié à la sécurité

2. Formation des champions (Semaine 10-11) :
   - 2 jours : OWASP Top 10 en pratique (hands-on sur une app volontairement vulnérable : WebGoat)
   - 1 jour : Utilisation de Burp Suite pour tester leurs propres APIs
   - 1 jour : Gestion des incidents de sécurité

3. Rôle des champions :
   - Reviewer sécurité obligatoire sur les PRs à risque élevé
   - Point de contact pour les questions sécurité de leur équipe
   - Participation aux security reviews mensuelles
   - Remontée des findings Semgrep vers le backlog

4. Formation de toute l'équipe (Semaine 12) :
   - Session de 3h : "Secure Coding pour Node.js/TypeScript"
   - Workshop pratique : corriger 5 vulnérabilités réelles trouvées dans le codebase
   - Quiz anonyme pour mesurer la progression
```

### Métriques — Avant / Après

```
Métriques collectées avant et après le programme (3 mois) :

Vulnérabilités détectées par la CI :
  Mois 1 (baseline, mode warn) : 847 findings
  Fin Mois 2 (mode bloquant)   : 124 findings restants (correction des CRITICAL/HIGH)
  Fin Mois 3                   : 38 findings (quasi-uniquement des LOW/INFO)

Réduction : -95% des vulnérabilités critiques et high

Métriques opérationnelles :
  Mean Time to Detect (MTTD) vuln critique :
    Avant : ∞ (pas de détection automatique)
    Après : < 5 minutes (CI bloquante sur chaque PR)

  Mean Time to Remediate (MTTR) vuln high :
    Avant : N/A
    Après : 3.2 jours (médiane sur les 3 derniers mois)

  Couverture des tests de sécurité :
    Avant : 0% des endpoints testés automatiquement
    Après : 100% (DAST sur staging à chaque déploiement main)

  Dépendances vulnérables (npm audit high+) :
    Avant : 15 (3 critiques)
    Après : 0 (Dependabot + Snyk, résolution sous 72h)

  Score OWASP SAMM :
    Avant : 1.1 / 3.0
    Après : 2.4 / 3.0 (objectif SOC 2 : > 2.0)

Adoption par l'équipe :
  - Gitleaks pre-commit : 100% des développeurs (enforced via repo settings)
  - Participation formation : 19/20 développeurs (1 absent maladie)
  - Score quiz sécurité : 72% en moyenne (objectif : 70%)
  - PRs avec finding sécurité corrigé < 24h : 84%
```

### Budget du Programme

```
Coûts directs (3 mois) :
  Snyk Team (20 devs)         : 3 000 € (500€/mois × 3 + setup)
  Formation externe (1 jour)  : 2 500 € (formateur OWASP certifié)
  Pentest final (validation)  : 12 000 € (4 jours, 2 pentesteurs)
  Temps ingénierie (DevOps)   : ~25 000 € (1 DevOps à 80% pendant 3 mois)
  ─────────────────────────────────────────
  Total                       : ~42 500 €

ROI estimé :
  Incident de sécurité évité (probabilité 40% sans programme) :
    Coût moyen incident fintech : 150 000 - 500 000 €
    → ROI conservateur : 60 000 € économisés × 40% = 24 000 €

  Contrat signé grâce à la conformité SOC 2 :
    Valeur annuelle du contrat banque : 180 000 €
    → Sans le programme, contrat perdu → ROI = 180 000 €

  Total ROI estimé première année : > 200 000 €
```

### Leçons Apprises

1. **Commencer en mode "warn" avant de bloquer** : activer Semgrep en mode bloquant dès le départ sur 847 findings aurait paralysé l'équipe. La montée progressive a permis l'adhésion.
2. **Les Security Champions sont le vrai levier de changement culturel** : les outils sans les personnes n'ont aucun effet. Les champions ancrent la sécurité dans chaque équipe.
3. **Mesurer pour convaincre** : les métriques MTTD/MTTR ont convaincu la direction de continuer l'investissement. Sans métriques, la sécurité reste perçue comme un coût.
4. **Le pentest externe valide le programme** : les pentesteurs n'ont trouvé aucune vulnérabilité critique lors du pentest de validation — preuve que le pipeline fonctionne.

---

## Cas 4 — SSRF dans une Fonctionnalité d'Upload de Fichier (Bug Bounty)

### Contexte

**Secteur** : Plateforme collaborative (type Notion/Confluence), 50 000 utilisateurs actifs.
**Stack** : Node.js / Express, React, AWS S3, Kubernetes.
**Programme bug bounty** : HackerOne, démarré depuis 6 mois, scope : `*.platform.example.com`.
**Fonctionnalité vulnérable** : Import de fichiers depuis une URL externe (type "Importer depuis Google Drive ou une URL publique").

### Découverte par le Bug Bounty (J0)

Un chercheur en sécurité (username : `xss_hunter_fr`) soumet un rapport à 09h23 avec la sévérité "High" :

**Rapport HackerOne (résumé)** :

```
Titre : SSRF via l'endpoint /api/files/import-from-url

Étapes pour reproduire :

1. Se connecter avec un compte gratuit
2. POST /api/files/import-from-url
   Body : { "url": "http://169.254.169.254/latest/meta-data/" }
3. La réponse contient les métadonnées AWS de l'instance EC2

Réponse obtenue :
{
  "content": "ami-id\nami-launch-index\nami-manifest-path\nhostname\n
               iam/\ninstance-action\ninstance-id\ninstance-type\n
               local-hostname\nlocal-ipv4\nnetwork/\n..."
}

4. Accès aux credentials IAM :
   POST /api/files/import-from-url
   Body : { "url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/" }
   → Nom du rôle IAM révélé : "platform-ec2-role"

   POST /api/files/import-from-url
   Body : { "url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/platform-ec2-role" }
   → AccessKeyId, SecretAccessKey, Token (credentials temporaires AWS !)

Impact : accès complet à AWS avec le rôle EC2 (S3, RDS, etc.)
```

### Mécanisme Technique

**Code vulnérable identifié après triage**

```typescript
// src/routes/files.ts — tel que trouvé
app.post('/api/files/import-from-url', authenticate, async (req, res) => {
  const { url, filename } = req.body;

  // ❌ Aucune validation de l'URL
  try {
    const response = await axios.get(url, {
      responseType: 'arraybuffer',
      timeout: 10000,
      maxContentLength: 50 * 1024 * 1024, // 50MB max
    });

    const s3Key = `users/${req.user.id}/${filename || 'imported-file'}`;
    await s3.putObject({
      Bucket: process.env.S3_BUCKET,
      Key: s3Key,
      Body: response.data,
      ContentType: response.headers['content-type'],
    }).promise();

    return res.json({ key: s3Key, size: response.data.length });
  } catch (error) {
    return res.status(400).json({ error: 'Failed to fetch URL' });
  }
});
```

**Pourquoi c'est grave**

```
Rôle IAM de l'instance EC2 (platform-ec2-role) avait les permissions :
  ✗ s3:* sur tous les buckets (y compris les backups)
  ✗ rds-db:connect sur toutes les instances RDS
  ✗ ssm:GetParameter (secrets dans Parameter Store)
  ✗ ecr:GetAuthorizationToken (accès aux images Docker privées)

Avec les credentials temporaires AWS récupérés via SSRF :
  → Lecture de tous les fichiers des 50 000 utilisateurs (S3)
  → Accès à la base de données production (RDS)
  → Récupération des secrets applicatifs (SSM)
  → Potentielle persistence via ECR
```

### Réponse à l'Incident (J0 → J3)

**J0, 09h45 — Triage et confirmation**

```bash
# Reproduction confirmée en staging par le Head of Security
curl -X POST https://staging.platform.example.com/api/files/import-from-url \
  -H "Authorization: Bearer STAGING_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "http://169.254.169.254/latest/meta-data/iam/"}'
# → Confirmation : SSRF réelle, sévérité critique reclassée

# Vérification des logs : exploitation réelle ?
# Recherche dans les logs CloudTrail d'appels depuis des IPs inconnues
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=GetObject \
  --start-time 2024-01-01T00:00:00Z \
  --query 'Events[?contains(CloudTrailEvent, `"userAgent":"Go-http-client"`)].EventTime'
# → Aucun accès suspect confirmé (le chercheur a stoppé après la preuve de concept)
```

**J0, 10h15 — Mitigation d'urgence (feature flag)**

```typescript
// Désactivation immédiate de la fonctionnalité via feature flag
// LaunchDarkly / Unleash — toggle en 30 secondes sans déploiement
featureFlags.disable('import-from-url');

// Dans le handler :
app.post('/api/files/import-from-url', authenticate, async (req, res) => {
  if (!featureFlags.isEnabled('import-from-url')) {
    return res.status(503).json({
      error: 'Cette fonctionnalité est temporairement indisponible.',
      retry_after: 3600,
    });
  }
  // ...
});
```

**J0, 11h00 — IMDSv2 activé en urgence (mitigation infrastructure)**

```bash
# Activer IMDSv2 (exige un token pour accéder aux métadonnées — SSRF basique ne fonctionne plus)
# Pour toutes les instances du cluster EKS

aws ec2 modify-instance-metadata-options \
  --instance-id $(curl -s http://169.254.169.254/latest/meta-data/instance-id) \
  --http-tokens required \
  --http-endpoint enabled

# Pour les nouveaux noeuds EKS (launch template)
aws ec2 modify-launch-template \
  --launch-template-id lt-xxx \
  --launch-template-data '{"MetadataOptions":{"HttpTokens":"required","HttpPutResponseHopLimit":1}}'

# Vérification : SSRF sur IMDSv2 nécessite un PUT préalable (non supporté par SSRF simple)
curl -s http://169.254.169.254/latest/meta-data/
# → 401 Unauthorized (maintenant protégé)
```

**J1 → J3 — Correction dans le code**

```typescript
import { URL } from 'url';
import dns from 'dns/promises';
import net from 'net';
import ipRangeCheck from 'ip-range-check';

// Liste des ranges IP privées et protégées
const BLOCKED_IP_RANGES = [
  '0.0.0.0/8',
  '10.0.0.0/8',
  '100.64.0.0/10',
  '127.0.0.0/8',
  '169.254.0.0/16',    // AWS metadata et link-local
  '172.16.0.0/12',
  '192.0.0.0/24',
  '192.168.0.0/16',
  '198.18.0.0/15',
  '198.51.100.0/24',
  '203.0.113.0/24',
  '240.0.0.0/4',
  '255.255.255.255/32',
  // AWS ECS metadata endpoint
  '169.254.170.2/32',
];

async function validateExternalUrl(rawUrl: string): Promise<URL> {
  let parsed: URL;
  try {
    parsed = new URL(rawUrl);
  } catch {
    throw new Error('Format d\'URL invalide.');
  }

  // Protocole : HTTPS uniquement pour les imports de fichiers
  if (parsed.protocol !== 'https:') {
    throw new Error('Seul HTTPS est accepté pour les imports de fichiers.');
  }

  // Pas d'authentification dans l'URL
  if (parsed.username || parsed.password) {
    throw new Error('L\'URL ne peut pas contenir de credentials.');
  }

  // Résolution DNS — vérification de l'IP de destination
  let addresses: string[];
  try {
    addresses = await dns.resolve4(parsed.hostname);
  } catch {
    throw new Error('Impossible de résoudre le nom de domaine.');
  }

  for (const addr of addresses) {
    if (ipRangeCheck(addr, BLOCKED_IP_RANGES)) {
      throw new Error('Cette adresse IP n\'est pas autorisée (plage privée ou réservée).');
    }
  }

  return parsed;
}

// Handler corrigé
app.post('/api/files/import-from-url', authenticate, rateLimiter, async (req, res) => {
  const { url, filename } = req.body;

  let validatedUrl: URL;
  try {
    validatedUrl = await validateExternalUrl(url);
  } catch (err) {
    return res.status(400).json({ error: (err as Error).message });
  }

  const response = await axios.get(validatedUrl.toString(), {
    responseType: 'arraybuffer',
    timeout: 10000,
    maxContentLength: 50 * 1024 * 1024,
    // Désactiver le suivi des redirections (risque de SSRF via redirect)
    maxRedirects: 0,
    // Ne pas envoyer les cookies de session dans la requête sortante
    withCredentials: false,
  });

  // Vérification du Content-Type (éviter les fichiers exécutables)
  const contentType = response.headers['content-type'] || '';
  const ALLOWED_CONTENT_TYPES = [
    'application/pdf', 'image/jpeg', 'image/png', 'image/gif',
    'image/webp', 'text/plain', 'application/json',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  ];
  if (!ALLOWED_CONTENT_TYPES.some(ct => contentType.startsWith(ct))) {
    return res.status(400).json({ error: `Type de fichier non autorisé : ${contentType}` });
  }

  // Upload vers S3
  const safeFilename = path.basename(filename || 'imported-file').replace(/[^a-zA-Z0-9._-]/g, '_');
  const s3Key = `users/${req.user.id}/${Date.now()}-${safeFilename}`;
  await s3.putObject({ Bucket: process.env.S3_BUCKET, Key: s3Key, Body: response.data }).promise();

  return res.json({ key: s3Key, size: response.data.length });
});
```

### Restriction IAM — Principe de Moindre Privilège

```json
// Politique IAM révisée pour le rôle EC2 (après l'incident)
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3UserUploadsOnly",
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::platform-uploads/users/*"
    },
    {
      "Sid": "DenyMetadataAccess",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:sourceIP": "169.254.169.254"
        }
      }
    }
  ]
}
```

### Outcome du Bug Bounty

```
Chronologie des communications :

J0, 09h23  : Réception du rapport HackerOne
J0, 09h45  : Triage confirmé, sévérité : Critical (9.1 CVSS)
J0, 10h15  : Mitigation (feature flag)
J0, 11h00  : IMDSv2 activé
J0, 14h00  : Mise à jour HackerOne : "Fixed in progress"
J3, 16h00  : Correction déployée en production
J5, 09h00  : Rapport fermé comme "Resolved", bounty attribué

Bounty attribué : 3 500 $ (Critical — selon le barème du programme)

Communication publique :
  - Disclosure coordonnée à 90 jours (standard HackerOne)
  - CVE demandé (non attribué — vulnérabilité corrigée avant l'expiration)
  - Post-mortem public sur le blog technique (3 mois après)
```

### Leçons Apprises

1. **IMDSv2 doit être activé dès le démarrage** : IMDSv2 transforme une SSRF critique en vecteur beaucoup plus difficile à exploiter. Configuration obligatoire dans les launch templates et AMI de base.
2. **La résolution DNS doit précéder la requête HTTP** : valider l'URL par regex ne suffit pas. Il faut résoudre le DNS et vérifier que l'IP de destination n'est pas dans une plage privée.
3. **Les redirections HTTP sont un vecteur SSRF** : `maxRedirects: 0` est la configuration correcte pour les imports de fichiers externes. Une redirection vers une IP interne contourne les validations d'URL.
4. **Le bug bounty est un investissement rentable** : 3 500 $ de bounty pour une vulnérabilité qui aurait pu coûter plusieurs millions en cas d'exploitation réelle. Un CISO rationnel augmente le barème.
5. **Le principe de moindre privilège IAM est la dernière ligne de défense** : même avec la SSRF corrigée, un rôle EC2 avec accès `s3:*` sur tous les buckets est une catastrophe en attente. Toujours scoper les permissions IAM à la ressource minimale nécessaire.

---

## Récapitulatif — Patterns Communs

```
Leçons transversales des 4 cas :

Technique :
  ✅ Valider TOUTES les entrées (URL, paramètres de tri, identifiants)
  ✅ Principe de moindre privilège à tous les niveaux (DB, IAM, K8s)
  ✅ Defense in depth : plusieurs couches de protection (code + infra + monitoring)
  ✅ Les logs permettent de déterminer si une vulnérabilité a été exploitée

Process :
  ✅ Feature flags pour mitigation rapide sans déploiement d'urgence
  ✅ War room déclenché immédiatement pour les vulnérabilités critiques
  ✅ Communication transparente avec les chercheurs (bug bounty)
  ✅ Post-mortem public = confiance des utilisateurs

Culture :
  ✅ La sécurité est l'affaire de toute l'équipe, pas d'un seul expert
  ✅ Investir dans la formation AVANT l'incident
  ✅ Les programmes bug bounty détectent ce que les équipes internes ne voient pas
  ✅ Chaque incident est une opportunité de systématiser les contrôles
```
