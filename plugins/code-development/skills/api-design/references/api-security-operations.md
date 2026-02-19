# API Security & Operations — Authentication, Rate Limiting, Documentation, Testing, Monitoring

## Overview

Ce document de référence couvre la sécurité et les opérations des APIs modernes (2024-2026). Il traite l'authentification (OAuth2, JWT, API Keys, mTLS), l'autorisation, le rate limiting, l'OWASP API Security Top 10, la documentation OpenAPI, le testing (contrat, charge, sécurité), le monitoring, et la sécurité des webhooks.

---

## Authentication Patterns

### API Keys

Mécanisme le plus simple pour identifier un consommateur d'API. Transmettre la clé via un header dédié (`X-API-Key` ou `Authorization: ApiKey <key>`), jamais dans l'URL (visible dans les logs et l'historique navigateur).

Règles d'implémentation :
- Générer des clés avec un CSPRNG (minimum 32 octets, encodé en base62 ou hex)
- Préfixer les clés pour identifier l'environnement : `sk_live_`, `sk_test_`
- Hacher les clés en base (SHA-256) — ne jamais stocker la clé en clair
- Supporter la rotation : permettre plusieurs clés actives simultanément
- Implémenter une date d'expiration configurable
- Logger chaque utilisation pour l'audit et le tracking d'usage

**Limites** : une API key identifie une application, pas un utilisateur. Ne pas utiliser comme seul mécanisme pour les opérations sensibles — combiner avec OAuth2 ou mTLS.

### OAuth2 Flows

| Flow | Usage | Client type | Refresh token |
|---|---|---|---|
| **Authorization Code + PKCE** | Applications web, mobile, SPA | Public | Oui |
| **Client Credentials** | Service-to-service (M2M) | Confidentiel | Non |
| **Device Authorization** | IoT, smart TV, CLI | Public | Oui |
| **Refresh Token** | Renouvellement de l'access token | Tous | N/A |

#### Authorization Code + PKCE (flux principal)

```
1. Client génère code_verifier (random 43-128 chars) + code_challenge = SHA256(code_verifier)
2. Client redirige vers /authorize avec code_challenge, state, redirect_uri
3. Utilisateur s'authentifie et consent
4. Authorization Server redirige vers redirect_uri avec authorization_code
5. Client échange code + code_verifier contre tokens via POST /token
6. Serveur vérifie SHA256(code_verifier) == code_challenge
7. Tokens retournés : access_token (court) + refresh_token (long) + id_token (si OIDC)
```

Règles : toujours utiliser `response_type=code`, générer un `state` unique par requête, enregistrer des `redirect_uri` exactes (pas de wildcards), valider le `state` au retour.

#### Client Credentials (M2M)

```
1. Client s'authentifie via POST /token avec client_id + client_secret
2. Authorization Server retourne un access_token (pas de refresh_token)
3. Client utilise l'access_token dans le header Authorization: Bearer
```

Stocker les client_secret dans un secret manager. Rotation tous les 90 jours maximum. Considérer mTLS (RFC 8705) pour les environnements haute sécurité.

### JWT — Structure, Validation, Rotation

#### Structure

Un JWT est composé de trois parties encodées en Base64url séparées par des points : Header (algorithme, type), Payload (claims), Signature.

#### Algorithmes recommandés

| Contexte | Algorithme | Justification |
|---|---|---|
| Tokens distribués | **RS256** (RSA-SHA256) | Clé publique distribuable pour validation |
| Alternative moderne | **EdDSA** (Ed25519) | Plus performant, clés plus courtes |
| Tokens internes | **ES256** (ECDSA P-256) | Bon compromis taille/sécurité |
| A proscrire | HS256 pour tiers, `alg: none` | Clé partagée = risque, none = bypass |

#### Validation systématique

Valider chaque JWT reçu selon cette séquence :
1. Vérifier la signature avec la clé publique (via JWKS endpoint)
2. Vérifier `iss` (issuer) correspond au provider attendu
3. Vérifier `aud` (audience) contient le client_id
4. Vérifier `exp` (expiration) est dans le futur
5. Vérifier `iat` (issued at) est raisonnable
6. Rejeter tout algorithme inattendu (prévention de l'attaque par confusion d'algorithme)

#### Rotation des clés

- Access tokens : TTL de **5 à 15 minutes**
- Refresh tokens : TTL de **7 à 30 jours**, rotation on use obligatoire
- Clés de signature (JWKS) : rotation tous les **90 jours**, publier les anciennes clés pendant le chevauchement
- Détection de réutilisation : si un refresh token déjà consommé est présenté, révoquer toute la famille de tokens

### mTLS (Mutual TLS)

Authentification bidirectionnelle : le serveur et le client présentent chacun un certificat TLS. Utilisé pour la communication service-to-service en environnements haute sécurité (finance, santé, infrastructure critique).

Avantages : authentification forte sans secrets partagés, résistant au vol de tokens. Inconvénients : gestion complexe des certificats (PKI), renouvellement automatique nécessaire (cert-manager).

### Comparaison des mécanismes

| Mécanisme | Sécurité | Complexité | Cas d'usage principal |
|---|---|---|---|
| **API Key** | Faible | Faible | Tracking, quotas, APIs publiques simples |
| **OAuth2 + PKCE** | Élevée | Moyenne | Apps web/mobile avec utilisateurs |
| **Client Credentials** | Moyenne | Faible | Service-to-service (M2M) |
| **JWT Bearer** | Moyenne | Moyenne | APIs stateless, microservices |
| **mTLS** | Très élevée | Élevée | Infrastructure critique, zero-trust |

---

## Authorization

### RBAC (Role-Based Access Control)

Attribuer des permissions via des rôles prédéfinis. Simple à implémenter et à comprendre.

```
Utilisateur → Rôle(s) → Permission(s)
  alice    → admin    → users:read, users:write, users:delete
  bob      → editor   → users:read, articles:read, articles:write
  charlie  → viewer   → users:read, articles:read
```

Adapté quand les patterns d'accès sont stables et prévisibles. Limité quand les règles dépendent du contexte (propriétaire de la ressource, heure, localisation).

### ABAC (Attribute-Based Access Control)

Évaluer les permissions selon des attributs du sujet, de la ressource, de l'action et de l'environnement.

```
Règle : ALLOW si
  subject.role == "editor"
  AND resource.status == "draft"
  AND resource.department == subject.department
  AND environment.time BETWEEN 08:00 AND 20:00
```

Plus flexible que RBAC mais plus complexe à auditer. Utiliser un moteur de politiques dédié (Open Policy Agent, Cedar, Cerbos).

### Scopes OAuth2

Les scopes limitent les permissions d'un access token. Définir des scopes granulaires alignés sur les ressources et les actions de l'API.

```
read:users          — Lire les profils utilisateurs
write:users         — Créer et modifier les utilisateurs
delete:users        — Supprimer les utilisateurs
read:orders         — Lire les commandes
write:orders        — Créer et modifier les commandes
admin:billing       — Gérer la facturation
```

Principe du moindre privilège : le client demande uniquement les scopes nécessaires. Le serveur d'autorisation valide que le client est autorisé à demander ces scopes.

### Field-Level Permissions

Filtrer les champs retournés selon le rôle ou les scopes du consommateur :

| Champ | `read:users` | `read:users:admin` |
|---|---|---|
| `id` | Oui | Oui |
| `name` | Oui | Oui |
| `email` | Non | Oui |
| `phone` | Non | Oui |
| `internal_notes` | Non | Oui |

Implémenter via un serializer conditionnel ou un middleware de filtrage post-query.

### Ownership-Based Access

Vérifier que l'utilisateur authentifié est le propriétaire de la ressource avant d'autoriser l'accès. Combiné avec RLS (Row-Level Security) en base de données pour une défense en profondeur.

```sql
-- PostgreSQL RLS example
CREATE POLICY user_own_data ON orders
  USING (user_id = current_setting('app.current_user_id')::uuid);
```

### Arbre de décision — Choix du modèle d'autorisation

```
Quel est le besoin d'autorisation ?
+-- Rôles fixes et stables (admin, editor, viewer)
|   +-- RBAC : simple, auditable, standard
+-- Règles dépendant du contexte (propriétaire, département, heure)
|   +-- ABAC : flexible, moteur de politiques (OPA, Cedar)
+-- API publique avec tokens OAuth2
|   +-- Scopes : granularité par ressource/action
+-- Données multi-tenant avec isolation stricte
|   +-- RLS + ownership : défense en profondeur au niveau BDD
+-- Combinaison de plusieurs besoins
    +-- Hybride : RBAC pour les rôles + scopes pour les tokens + RLS pour l'isolation
```

---

## Rate Limiting

### Algorithmes

| Algorithme | Principe | Avantages | Inconvénients |
|---|---|---|---|
| **Fixed Window** | Compteur réinitialisé à intervalle fixe (ex : 100 req/min) | Simple à implémenter | Burst au changement de fenêtre (jusqu'à 2x la limite) |
| **Sliding Window** | Fenêtre glissante pondérée entre la fenêtre courante et la précédente | Lisse les bursts | Légèrement plus complexe |
| **Token Bucket** | Bucket rempli à un taux fixe, chaque requête consomme un token | Autorise les bursts contrôlés | Nécessite un stockage du bucket |
| **Leaky Bucket** | File d'attente avec débit de sortie fixe | Débit parfaitement constant | Latence ajoutée en file d'attente |

**Recommandation** : utiliser le sliding window pour les APIs publiques (bon compromis précision/simplicité). Utiliser le token bucket quand les bursts occasionnels sont acceptables.

### Limites par consommateur

Définir des plans de rate limiting différenciés :

| Plan | Requêtes/minute | Requêtes/jour | Burst | Use case |
|---|---|---|---|---|
| **Free** | 60 | 1 000 | 10 | Prototypage, évaluation |
| **Standard** | 600 | 50 000 | 50 | Production standard |
| **Enterprise** | 6 000 | 500 000 | 200 | Haute volumétrie |
| **Internal** | 30 000 | Illimité | 500 | Services internes |

Appliquer des limites spécifiques par endpoint pour les opérations coûteuses (recherche, exports, mutations).

### Headers de Rate Limiting

Inclure systématiquement les headers standardisés (IETF draft RateLimit) :

```
RateLimit-Limit: 100
RateLimit-Remaining: 42
RateLimit-Reset: 1705312800
Retry-After: 30
```

- `RateLimit-Limit` : nombre maximum de requêtes dans la fenêtre courante
- `RateLimit-Remaining` : requêtes restantes dans la fenêtre
- `RateLimit-Reset` : timestamp Unix de la réinitialisation de la fenêtre
- `Retry-After` : secondes d'attente avant la prochaine requête autorisée (retourné avec le 429)

### Réponse 429 — Design

```json
{
  "type": "https://api.example.com/errors/rate-limit-exceeded",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "Vous avez dépassé la limite de 100 requêtes par minute. Réessayez dans 30 secondes.",
  "retry_after": 30,
  "limit": 100,
  "remaining": 0,
  "reset": 1705312800,
  "documentation_url": "https://api.example.com/docs/rate-limiting"
}
```

Ne jamais révéler d'informations sur l'existence de comptes ou de ressources via le comportement du rate limiting.

---

## OWASP API Security Top 10 (2023)

### Tableau de synthèse

| Rang | Risque | Description courte |
|---|---|---|
| API1 | Broken Object Level Authorization (BOLA) | Accès aux objets d'autres utilisateurs |
| API2 | Broken Authentication | Failles dans les mécanismes d'authentification |
| API3 | Broken Object Property Level Authorization | Exposition ou modification de propriétés non autorisées |
| API4 | Unrestricted Resource Consumption | Absence de limites sur les ressources consommées |
| API5 | Broken Function Level Authorization (BFLA) | Accès à des fonctions réservées à d'autres rôles |
| API6 | Unrestricted Access to Sensitive Business Flows | Abus automatisé de workflows métier |
| API7 | Server-Side Request Forgery (SSRF) | Requêtes serveur vers des cibles non autorisées |
| API8 | Security Misconfiguration | Mauvaise configuration de sécurité |
| API9 | Improper Inventory Management | APIs non inventoriées ou non retirées |
| API10 | Unsafe Consumption of APIs | Consommation non sécurisée d'APIs tierces |

### API1 — Broken Object Level Authorization (BOLA)

**Description** : un attaquant modifie l'identifiant d'un objet dans la requête pour accéder aux données d'un autre utilisateur (ex : `GET /orders/123` → `GET /orders/456`).

**Exemple** : un utilisateur accède aux commandes d'un autre utilisateur en itérant les IDs séquentiels.

**Mitigation** :
- Vérifier la propriété de chaque objet avant de retourner ou modifier la ressource
- Utiliser des UUIDs plutôt que des IDs séquentiels
- Implémenter RLS (Row-Level Security) au niveau base de données
- Tester systématiquement les IDOR (Insecure Direct Object Reference) sur chaque endpoint

### API2 — Broken Authentication

**Description** : failles dans les flux d'authentification permettant l'usurpation d'identité.

**Exemple** : absence de rate limiting sur le endpoint de login, permettant le brute force.

**Mitigation** :
- Implémenter OAuth 2.1 + PKCE pour tous les clients publics
- Rate limiter les endpoints d'authentification (5 tentatives/minute)
- Utiliser des access tokens à TTL court (5-15 min) avec rotation des refresh tokens
- Implémenter la détection de réutilisation des refresh tokens

### API3 — Broken Object Property Level Authorization

**Description** : l'API expose des propriétés sensibles ou permet la modification de propriétés qui devraient être en lecture seule.

**Exemple** : un `PATCH /users/me` qui accepte `{"role": "admin"}` et l'applique sans validation.

**Mitigation** :
- Définir des schémas de requête et de réponse explicites (allow-list de champs)
- Séparer les DTOs de lecture et d'écriture
- Ne jamais utiliser de mass assignment sans allow-list explicite
- Filtrer les champs en réponse selon le rôle/scope du consommateur

### API4 — Unrestricted Resource Consumption

**Description** : absence de limites sur les ressources consommées par une requête (mémoire, CPU, bande passante, nombre de résultats).

**Exemple** : `GET /users?limit=1000000` retourne un million d'enregistrements, saturant le serveur.

**Mitigation** :
- Imposer des limites de pagination (max 100 éléments par page)
- Limiter la taille des payloads (body, uploads)
- Implémenter le rate limiting par consommateur
- Définir des timeouts pour les requêtes longues
- Limiter la complexité des requêtes (GraphQL : depth limiting, cost analysis)

### API5 — Broken Function Level Authorization (BFLA)

**Description** : un utilisateur accède à des fonctions réservées à un autre rôle (ex : un utilisateur standard qui appelle des endpoints admin).

**Exemple** : `DELETE /admin/users/123` accessible sans vérification du rôle admin.

**Mitigation** :
- Implémenter le deny-by-default pour tous les endpoints
- Centraliser la logique d'autorisation (middleware, policy engine)
- Séparer les routes admin des routes utilisateur
- Tester les accès cross-rôles systématiquement

### API6 — Unrestricted Access to Sensitive Business Flows

**Description** : l'API permet l'automatisation abusive de workflows métier (achat en masse, scraping, spam).

**Exemple** : un bot qui achète tous les billets d'un concert via l'API de réservation.

**Mitigation** :
- Identifier les business flows sensibles et les protéger spécifiquement
- Implémenter des CAPTCHAs ou challenges pour les actions sensibles
- Détecter les patterns d'usage anormaux (fréquence, volume, vitesse)
- Appliquer des limites métier (max 4 billets par utilisateur, cooldown entre achats)

### API7 — Server-Side Request Forgery (SSRF)

**Description** : l'API effectue des requêtes vers des URLs contrôlées par l'attaquant.

**Exemple** : `POST /import {"url": "http://169.254.169.254/latest/meta-data/"}` pour accéder aux métadonnées cloud.

**Mitigation** :
- Valider et filtrer toutes les URLs fournies par l'utilisateur
- Bloquer les plages d'adresses privées et les métadonnées cloud
- Utiliser un proxy dédié avec allow-list pour les requêtes sortantes
- Désactiver les redirections HTTP pour les requêtes côté serveur

### API8 — Security Misconfiguration

**Description** : configuration de sécurité manquante ou incorrecte (CORS permissif, headers absents, debug activé).

**Exemple** : `Access-Control-Allow-Origin: *` avec `credentials: true`, exposant les cookies à tout domaine.

**Mitigation** :
- Automatiser la configuration de sécurité via IaC
- Désactiver les fonctionnalités de debug en production
- Configurer les security headers (CSP, HSTS, X-Content-Type-Options)
- Scanner les configurations régulièrement (CIS Benchmarks)

### API9 — Improper Inventory Management

**Description** : APIs non inventoriées, anciennes versions non retirées, endpoints de test exposés en production.

**Exemple** : `/api/v1/users` (déprécié, sans auth) coexiste avec `/api/v2/users` (sécurisé).

**Mitigation** :
- Maintenir un inventaire complet de toutes les APIs et versions exposées
- Retirer les anciennes versions selon la politique de sunset
- Séparer les environnements (test, staging, production) strictement
- Scanner l'infrastructure pour détecter les APIs non documentées (shadow APIs)

### API10 — Unsafe Consumption of APIs

**Description** : l'application fait confiance aveuglément aux réponses d'APIs tierces sans validation.

**Exemple** : l'API interne désérialise et stocke les données d'une API partenaire sans validation de schéma, permettant l'injection.

**Mitigation** :
- Valider et sanitiser toutes les données reçues d'APIs tierces
- Appliquer des timeouts et du circuit breaking sur les appels externes
- Utiliser HTTPS pour toutes les communications avec les APIs tierces
- Évaluer la posture de sécurité des partenaires API

---

## API Documentation

### OpenAPI 3.1 — Structure

```yaml
openapi: "3.1.0"
info:
  title: Order Management API
  version: "2.0.0"
  description: API de gestion des commandes
  contact:
    name: API Support
    email: api@example.com
  license:
    name: Apache 2.0

servers:
  - url: https://api.example.com/v2
    description: Production
  - url: https://sandbox.api.example.com/v2
    description: Sandbox

paths:
  /orders:
    get:
      operationId: listOrders
      summary: Lister les commandes
      tags: [Orders]
      parameters:
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Liste paginée des commandes
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderListResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/RateLimited'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
```

Règles : documenter chaque endpoint, paramètre, schéma de requête/réponse et code d'erreur. Inclure des exemples concrets. Valider la spec automatiquement dans le CI avec Spectral.

### Outils de documentation

| Outil | Type | Forces | Faiblesses |
|---|---|---|---|
| **Scalar** | OSS, moderne | Design moderne, try-it-out, personnalisable | Écosystème récent |
| **Redoc** | OSS | Rendu élégant, trois colonnes, SEO-friendly | Pas de try-it-out natif |
| **Stoplight** | SaaS/OSS | Design-first, gouvernance, mock server | Coût pour les fonctionnalités avancées |
| **Swagger UI** | OSS | Standard de facto, try-it-out intégré | Design daté, personnalisation limitée |
| **Bump.sh** | SaaS | Changelog automatique, diff entre versions | SaaS uniquement |

### Auto-génération

- Générer la documentation interactive depuis la spec OpenAPI dans le CI/CD
- Générer les SDKs client type-safe : **Speakeasy** (multi-langage), **openapi-typescript** (TypeScript), **openapi-generator** (multi-langage OSS)
- Valider la spec avec **Spectral** (linting de règles de style et de cohérence)
- Générer les mock servers avec **Prism** pour le développement parallèle frontend/backend

### Changelog et versioning de la documentation

Maintenir un changelog structuré pour chaque version de l'API :

```markdown
## v2.3.0 (2026-02-15)
### Added
- Endpoint `GET /orders/{id}/timeline` pour l'historique des événements
- Champ optionnel `metadata` sur les ressources Order

### Changed
- La pagination par défaut passe de 20 à 25 éléments par page

### Deprecated
- Le champ `order.shipping_info` sera remplacé par `order.shipping` en v3.0 (sunset : 2026-09-01)
```

Utiliser les headers `Deprecation` et `Sunset` (RFC 8594) pour signaler les dépréciations dans les réponses HTTP.

---

## API Testing

### Contract Testing (Pact)

Valider que le fournisseur (provider) respecte le contrat attendu par chaque consommateur (consumer). Le Consumer-Driven Contract Testing garantit la compatibilité sans déploiement conjoint.

```
1. Le consumer génère un contrat (pact file) décrivant ses attentes
2. Le pact file est partagé via un Pact Broker
3. Le provider exécute les tests de vérification contre le contrat
4. Le Pact Broker vérifie la compatibilité avant chaque déploiement (can-i-deploy)
```

Intégrer les contract tests dans le CI/CD. Bloquer le déploiement si les contrats sont violés.

### Integration Testing

Tester les endpoints de bout en bout avec une base de données de test :

```typescript
describe('POST /orders', () => {
  it('crée une commande avec les champs requis', async () => {
    const response = await request(app)
      .post('/v2/orders')
      .set('Authorization', `Bearer ${testToken}`)
      .send({ customer_id: 'cust_123', items: [{ product_id: 'prod_1', quantity: 2 }] })
      .expect(201);

    expect(response.body.order.id).toBeDefined();
    expect(response.body.order.status).toBe('pending');
  });

  it('retourne 401 sans authentification', async () => {
    await request(app).post('/v2/orders').send({}).expect(401);
  });

  it('retourne 400 avec un payload invalide', async () => {
    const response = await request(app)
      .post('/v2/orders')
      .set('Authorization', `Bearer ${testToken}`)
      .send({ invalid: true })
      .expect(400);

    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
});
```

### Property-Based Testing

Générer des entrées aléatoires pour découvrir des cas limites non anticipés :

- Valider que l'API retourne toujours un format d'erreur cohérent pour toute entrée invalide
- Vérifier l'idempotence : appeler deux fois un endpoint avec le même `Idempotency-Key` retourne le même résultat
- Tester la sérialisation/désérialisation roundtrip
- Outils : **fast-check** (TypeScript), **Hypothesis** (Python), **QuickCheck** (Haskell/Erlang)

### Load Testing

| Outil | Langage | Forces | Idéal pour |
|---|---|---|---|
| **k6** | JavaScript | Scriptable, métriques riches, CI-friendly | Tests de charge réguliers en CI |
| **Artillery** | YAML/JS | Configuration simple, plugins cloud | Tests de charge rapides |
| **Locust** | Python | Distribué, scriptable | Scénarios complexes |
| **Gatling** | Scala/Java | Haute performance, rapports détaillés | Tests de charge massifs |

Scénarios à tester :
- **Smoke test** : charge minimale, valider que le système fonctionne (10 VUs, 1 min)
- **Load test** : charge nominale attendue (100 VUs, 10 min)
- **Stress test** : charge au-delà de la capacité nominale (500 VUs, 10 min)
- **Spike test** : burst soudain de trafic (0 → 1000 VUs en 30 sec)
- **Soak test** : charge nominale sur longue durée pour détecter les fuites mémoire (100 VUs, 4h)

### Security Testing

- **OWASP ZAP** : scanner automatisé de vulnérabilités API (DAST). Intégrer dans le CI pour le scan des endpoints. Configurer les contexts d'authentification pour tester en mode authentifié.
- **Nuclei** : scanner de vulnérabilités template-based. Templates communautaires pour les CVEs connues et les misconfigurations.
- **Burp Suite** : testing manuel et automatisé pour les pentests approfondis.

### Fuzz Testing

Envoyer des entrées malformées, aléatoires ou extrêmes pour découvrir des crashs, des fuites de données ou des comportements inattendus :

- Fuzzer les headers, les query parameters, le body JSON, les paths
- Tester les limites : chaînes vides, chaînes très longues, caractères Unicode, null bytes, injections SQL/XSS dans tous les champs
- Outils : **RESTler** (Microsoft, fuzzing stateful d'APIs REST), **Schemathesis** (fuzzing basé sur OpenAPI spec), **API Fuzzer** (OWASP)

---

## API Monitoring

### Métriques essentielles (RED Method)

Instrumenter chaque endpoint avec les métriques RED :

| Métrique | Description | Alerte |
|---|---|---|
| **Rate** | Requêtes par seconde par endpoint | Variation > 50% vs baseline |
| **Errors** | Taux d'erreur (4xx, 5xx) par endpoint | 5xx > 1%, 4xx > 10% |
| **Duration** | Latence par endpoint (percentiles) | p99 > SLO |

### Latence — Percentiles

Ne jamais utiliser la moyenne pour la latence. Toujours rapporter et alerter sur les percentiles :

| Percentile | Signification | Usage |
|---|---|---|
| **p50** (médiane) | Expérience typique de 50% des utilisateurs | Baseline de performance |
| **p95** | Expérience des 5% les plus lents | SLI principal pour les SLOs |
| **p99** | Latence de queue (tail latency) | Détection des problèmes affectant une minorité significative |
| **p99.9** | Extrêmes | Services critiques (paiement, authentification) |

Configurer les alertes sur les percentiles, pas sur la moyenne. Un p99 qui dépasse le SLO indique un problème réel même si la moyenne reste acceptable.

### Error Rates par endpoint

Catégoriser les erreurs pour un diagnostic rapide :

```
Erreurs client (4xx) :
+-- 400 Bad Request → Problème de validation, documenter mieux l'API
+-- 401 Unauthorized → Tokens expirés, problème d'authentification
+-- 403 Forbidden → Problème d'autorisation, vérifier les scopes/rôles
+-- 404 Not Found → Ressource inexistante ou URL incorrecte
+-- 429 Too Many Requests → Rate limiting, ajuster les quotas si légitime

Erreurs serveur (5xx) :
+-- 500 Internal Server Error → Bug applicatif, investiguer immédiatement
+-- 502 Bad Gateway → Service upstream indisponible
+-- 503 Service Unavailable → Surcharge ou maintenance
+-- 504 Gateway Timeout → Requête upstream trop lente
```

### Usage Analytics

Collecter les métriques d'usage pour piloter l'évolution de l'API :
- Endpoints les plus utilisés et les moins utilisés (candidats au sunset)
- Consommateurs les plus actifs et leur pattern d'usage
- Taux d'adoption des nouvelles versions
- Time-to-first-call par nouveau consommateur (indicateur de DX)

### Anomaly Detection

Détecter les patterns anormaux automatiquement :
- Pics soudains de trafic sur un endpoint spécifique (possible attaque)
- Augmentation du taux d'erreur 401/403 (brute force ou credentials leakés)
- Changement de pattern d'usage par un consommateur (compromission possible)
- Latence qui dérive progressivement (dégradation de performance)

### SLO/SLA Tracking

Définir des SLOs (Service Level Objectives) par tier d'API :

| Tier | Disponibilité | Latence p95 | Latence p99 | Error rate |
|---|---|---|---|---|
| **Critique** (paiement, auth) | 99.99% | < 200ms | < 500ms | < 0.01% |
| **Standard** (CRUD métier) | 99.9% | < 500ms | < 1s | < 0.1% |
| **Non-critique** (analytics, exports) | 99.5% | < 2s | < 5s | < 1% |

Calculer et publier les SLIs (Service Level Indicators) en temps réel. Configurer un error budget et alerter quand le budget est consommé à 80%.

---

## Webhook Security

### Signature HMAC

Signer chaque payload de webhook avec HMAC-SHA256 pour garantir l'authenticité et l'intégrité :

```
Webhook-Signature: sha256=a1b2c3d4e5f6...
Webhook-Id: wh_msg_123456
Webhook-Timestamp: 1705312800
```

Calcul de la signature :

```python
import hmac, hashlib

def compute_signature(secret: str, timestamp: str, body: str) -> str:
    message = f"{timestamp}.{body}"
    return hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
```

Le consommateur recalcule la signature avec son secret partagé et compare. Rejeter si la signature ne correspond pas.

### Replay Protection

- Inclure un timestamp dans le header (`Webhook-Timestamp`)
- Rejeter les webhooks dont le timestamp dépasse **5 minutes** par rapport à l'horloge du serveur
- Stocker les `Webhook-Id` déjà traités et rejeter les doublons (fenêtre de déduplication de 24h)

### IP Whitelisting

Publier la liste des adresses IP source des webhooks. Permettre aux consommateurs de filtrer le trafic entrant par IP. Mettre à jour la liste via un endpoint dédié (`GET /webhooks/ip-ranges`).

### Verification Endpoint

Exposer un mécanisme de vérification pour valider l'URL du webhook lors de l'enregistrement :

```
1. Le consommateur enregistre une URL de webhook
2. Le serveur envoie un challenge (GET avec un token de vérification)
3. Le consommateur retourne le token dans la réponse
4. Le serveur confirme l'enregistrement
```

### Retry Policies

Implémenter un retry avec backoff exponentiel pour les webhooks en échec :

| Tentative | Délai | Délai cumulé |
|---|---|---|
| 1 | Immédiat | 0 |
| 2 | 30 secondes | 30s |
| 3 | 5 minutes | 5min 30s |
| 4 | 30 minutes | 35min 30s |
| 5 | 2 heures | 2h 35min |
| 6 | 8 heures | 10h 35min |

Après épuisement des retries, marquer le webhook comme failed et notifier le consommateur. Exposer un dashboard de delivery logs consultable par le consommateur (`GET /webhooks/{id}/deliveries`).

---

## State of the Art (2025-2026)

### API Security Platforms

Les plateformes de sécurité API émergent comme catégorie à part entière :

| Plateforme | Spécialité | Approche |
|---|---|---|
| **Salt Security** | Détection de menaces API | Analyse du trafic API en temps réel, détection d'attaques, shadow API discovery |
| **Noname Security** | Posture management | Inventaire API, conformité, détection d'anomalies, intégration CI/CD |
| **42Crunch** | API security testing | Audit de la spec OpenAPI, conformité OWASP, scan actif des endpoints |
| **Traceable AI** | API threat detection | Analyse comportementale, corrélation cross-API, DLP pour APIs |
| **Wallarm** | WAF/WAAP API-native | Protection runtime, auto-découverte des APIs, virtual patching |

### AI-Powered API Testing

L'IA transforme le testing d'APIs :
- **Génération automatique de tests** depuis la spec OpenAPI avec couverture des cas limites
- **Fuzzing intelligent** guidé par l'IA pour découvrir des vulnérabilités complexes (chaînes d'appels multi-étapes)
- **Détection de breaking changes** par analyse du trafic réel vs spec (Optic, Akita)
- **Génération d'exemples** réalistes pour la documentation via LLMs

### API Governance Automation

L'automatisation de la gouvernance API devient standard :
- **Spectral** + règles custom pour le linting de la spec OpenAPI en CI
- **Optic** pour la détection automatique de breaking changes par comparaison de specs
- **API Catalogs** centralisés (Backstage, Port, Cortex) pour l'inventaire et la découvrabilité
- **Conformité automatique** : validation des conventions de nommage, des patterns de sécurité, et de la documentation complète avant chaque merge

### Zero-Trust APIs

L'approche zero-trust appliquée aux APIs :
- **Vérification continue** : chaque requête est authentifiée et autorisée, même interne
- **mTLS généralisé** via service mesh (Istio, Linkerd) pour le chiffrement et l'authentification service-to-service
- **Token binding** (DPoP) : lier les tokens au client qui les a reçus pour prévenir le vol
- **Least privilege dynamique** : ajuster les permissions en temps réel selon le contexte (risque, localisation, device)
- **API Gateway as Policy Enforcement Point** : centraliser l'application des politiques de sécurité au niveau du gateway (Envoy, Kong, Cloudflare API Shield)
