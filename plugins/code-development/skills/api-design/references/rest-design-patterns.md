# REST Design Patterns — Resource Modeling, HTTP Methods, Status Codes, Pagination, Filtering, Bulk Operations

## Overview

Référence approfondie sur les patterns de conception REST. Couvre la modélisation des ressources, la sémantique des méthodes HTTP, les codes de statut, la pagination avancée, le filtrage, les réponses partielles, les opérations en masse, HATEOAS et le caching HTTP. Appliquer ces patterns systématiquement pour concevoir des APIs REST prévisibles, performantes et évolutives.

---

## Resource Modeling

### Identification des ressources

Une ressource REST représente une entité ou un concept du domaine métier, pas une table de base de données. Identifier les ressources en analysant le domaine, pas le schéma de stockage.

```
Arbre de décision — Modélisation des ressources :
+-- L'entité a-t-elle un identifiant unique ?
    +-- Oui → Ressource à part entière (/orders/{id})
    +-- Non → Est-ce un attribut d'une autre ressource ?
        +-- Oui → Champ de la ressource parente
        +-- Non → Est-ce une relation entre ressources ?
            +-- Oui → Sous-ressource ou lien HATEOAS
            +-- Non → Est-ce un processus ou une action ?
                +-- Oui → Ressource de processus (/order-cancellations)
                +-- Non → Probablement un query parameter
```

### Conventions de nommage

| Règle | Correct | Incorrect | Raison |
|---|---|---|---|
| Noms pluriels pour les collections | `/users` | `/user` | Cohérence et clarté sémantique |
| kebab-case pour les URIs multi-mots | `/order-items` | `/orderItems`, `/order_items` | Standard URI (RFC 3986) |
| Noms, pas de verbes dans les URIs | `/orders` | `/getOrders`, `/createOrder` | Les méthodes HTTP portent l'action |
| Pas de trailing slash | `/users` | `/users/` | Éviter les redirections inutiles |
| Minuscules uniquement | `/api/v1/users` | `/API/V1/Users` | Les URIs sont case-sensitive (RFC 3986) |
| Identifiants opaques de préférence | `/users/usr_8x7Kp2` | `/users/42` | Les IDs séquentiels exposent des informations |

### Sub-resources & Relations

Limiter l'imbrication des ressources à 2 niveaux maximum. Au-delà, la lisibilité et la maintenabilité se dégradent.

```
# Collection et singleton
GET    /users                          # collection de users
GET    /users/{userId}                 # singleton (un user)

# Sous-ressource directe (1 niveau)
GET    /users/{userId}/orders          # commandes d'un utilisateur
POST   /users/{userId}/orders          # créer une commande pour cet utilisateur

# Sous-ressource imbriquée (2 niveaux — maximum)
GET    /users/{userId}/orders/{orderId}

# Au-delà de 2 niveaux — APLATIR
# NON : /users/{userId}/orders/{orderId}/items/{itemId}/reviews
# OUI : /order-items/{itemId}/reviews
# OUI : /reviews?order_item_id={itemId}
```

### Singleton vs Collection

| Type | URI | GET | POST | PUT | DELETE |
|---|---|---|---|---|---|
| **Collection** | `/orders` | Liste paginée | Créer | Remplacement bulk (rare) | Suppression bulk (rare) |
| **Singleton** | `/orders/{id}` | Détail | N/A (405) | Remplacer | Supprimer |
| **Singleton implicite** | `/users/{id}/profile` | Le profil | N/A | Remplacer | N/A |

### URI Design Rules

```
Structure standard :
+-- Schéma : https://
+-- Hôte : api.example.com
+-- Préfixe de version : /v1
+-- Ressource : /orders
+-- Identifiant (optionnel) : /orders/{orderId}
+-- Sous-ressource (optionnel) : /orders/{orderId}/items
+-- Query parameters : ?status=pending&sort=-created_at

Résultat : https://api.example.com/v1/orders/{orderId}/items?status=active
```

Actions non-CRUD — utiliser des sous-ressources verbales ou des ressources de processus :

```
# Approche 1 : sous-ressource verbale (action)
POST   /orders/{id}/cancel
POST   /orders/{id}/refund
POST   /users/{id}/verify-email

# Approche 2 : ressource de processus (état)
POST   /order-cancellations       { "orderId": "ORD-123" }
POST   /email-verifications       { "userId": "USR-456" }

# Approche 3 : opération longue durée (async)
POST   /reports/generate          → 202 Accepted + Location: /jobs/JOB-789
GET    /jobs/JOB-789              → { "status": "processing", "progress": 45 }
```

---

## HTTP Methods & Semantics

### Référence complète des méthodes

| Méthode | Sémantique | Idempotent | Safe | Corps requête | Corps réponse | Cacheable |
|---|---|---|---|---|---|---|
| `GET` | Lire une ressource | Oui | Oui | Non | Oui | Oui |
| `POST` | Créer ou déclencher | Non | Non | Oui | Oui | Non* |
| `PUT` | Remplacer entièrement | Oui | Non | Oui | Oui | Non |
| `PATCH` | Modifier partiellement | Non** | Non | Oui | Oui | Non |
| `DELETE` | Supprimer | Oui | Non | Optionnel | Optionnel | Non |
| `HEAD` | Métadonnées seulement | Oui | Oui | Non | Non | Oui |
| `OPTIONS` | Capacités du serveur | Oui | Oui | Non | Oui | Non |

*POST peut être rendu cacheable avec des headers explicites (Cache-Control).
**PATCH peut être rendu idempotent via JSON Merge Patch (RFC 7396).

### Idempotency — Définition et implications

Une opération est idempotente si l'exécuter N fois produit le même résultat que l'exécuter 1 fois. Cela concerne l'état du serveur, pas nécessairement la réponse.

```
Arbre de décision — Idempotency :
+-- La méthode est-elle GET, HEAD, OPTIONS ?
|   +-- Oui → Toujours idempotente et safe
+-- La méthode est-elle PUT ou DELETE ?
|   +-- Oui → Toujours idempotente (par spécification)
+-- La méthode est-elle POST ?
|   +-- Non idempotente par défaut
|   +-- Rendre idempotente avec un header Idempotency-Key
+-- La méthode est-elle PATCH ?
    +-- Dépend du format de patch
    +-- JSON Merge Patch (RFC 7396) → idempotent
    +-- JSON Patch (RFC 6902) → non idempotent (opérations séquentielles)
```

### PUT vs PATCH — Quand utiliser quoi

| Critère | PUT | PATCH |
|---|---|---|
| **Sémantique** | Remplacement complet de la ressource | Modification partielle |
| **Payload** | La ressource complète | Seulement les champs à modifier |
| **Champs absents** | Réinitialisés à leur valeur par défaut ou null | Inchangés |
| **Idempotent** | Oui (toujours) | Dépend du format |
| **Cas d'usage** | Formulaires complets, config complète | Mise à jour d'un champ, toggle |

```json
// PUT /users/USR-123 — remplacement complet
{
  "name": "Alice Martin",
  "email": "alice@example.com",
  "role": "admin",
  "bio": "Updated bio",
  "avatar_url": null
}

// PATCH /users/USR-123 — modification partielle (JSON Merge Patch)
{
  "bio": "Updated bio"
}
// Seul le champ "bio" est modifié, les autres restent inchangés
```

---

## Status Codes

### Référence complète par catégorie

#### 2xx — Succès

| Code | Nom | Usage | Headers associés |
|---|---|---|---|
| 200 | OK | GET, PUT, PATCH réussis avec corps de réponse | — |
| 201 | Created | POST réussi (ressource créée) | `Location: /resources/{id}` |
| 202 | Accepted | Opération asynchrone acceptée | `Location: /jobs/{id}` |
| 204 | No Content | DELETE réussi, PUT/PATCH sans corps de retour | — |

#### 3xx — Redirection

| Code | Nom | Usage | Headers associés |
|---|---|---|---|
| 301 | Moved Permanently | Ressource déplacée définitivement | `Location: nouvelle-url` |
| 302 | Found | Redirection temporaire (éviter pour les APIs) | `Location` |
| 304 | Not Modified | Cache valide (ETag/If-None-Match) | `ETag` |
| 307 | Temporary Redirect | Redirection temporaire en conservant la méthode | `Location` |
| 308 | Permanent Redirect | Redirection permanente en conservant la méthode | `Location` |

#### 4xx — Erreur client

| Code | Nom | Usage | Exemple |
|---|---|---|---|
| 400 | Bad Request | Syntaxe invalide, JSON malformé | Body non parseable |
| 401 | Unauthorized | Non authentifié (token manquant ou expiré) | Bearer token absent |
| 403 | Forbidden | Authentifié mais non autorisé | Accès à une ressource d'un autre tenant |
| 404 | Not Found | Ressource inexistante | ID inconnu |
| 405 | Method Not Allowed | Méthode non supportée sur cette ressource | POST sur un singleton |
| 409 | Conflict | Conflit avec l'état actuel | Violation de contrainte unique, version conflict |
| 410 | Gone | Ressource supprimée définitivement | Endpoint déprécié et retiré |
| 412 | Precondition Failed | Pré-condition non satisfaite | If-Match ETag incorrect |
| 413 | Payload Too Large | Corps de requête trop volumineux | Upload dépassant la limite |
| 415 | Unsupported Media Type | Content-Type non supporté | XML envoyé à une API JSON-only |
| 422 | Unprocessable Entity | Validation métier échouée | Email invalide, montant négatif |
| 429 | Too Many Requests | Rate limit dépassé | `Retry-After: 30` |

#### 5xx — Erreur serveur

| Code | Nom | Usage | Action client |
|---|---|---|---|
| 500 | Internal Server Error | Erreur non prévue côté serveur | Retry avec backoff |
| 502 | Bad Gateway | Service upstream défaillant | Retry avec backoff |
| 503 | Service Unavailable | Maintenance ou surcharge | Respecter `Retry-After` |
| 504 | Gateway Timeout | Timeout d'un service upstream | Retry avec backoff |

### Anti-patterns de status codes

```
Anti-patterns fréquents :
+-- 200 pour tout (y compris les erreurs)
|   → Empêche les clients d'utiliser le code HTTP pour le branching
|   → Les proxies et CDN ne peuvent pas distinguer succès/erreur
|
+-- 500 pour les erreurs de validation
|   → Masque les vrais problèmes serveur dans le monitoring
|   → Le client ne sait pas si c'est sa faute ou celle du serveur
|
+-- 404 pour les erreurs d'autorisation
|   → Fuite d'information (confirme l'existence de la ressource)
|   → Acceptable uniquement pour masquer l'existence (cas sécurité)
|
+-- 200 avec { "error": true } dans le body
|   → Le client doit parser le body pour détecter les erreurs
|   → Incompatible avec les outils HTTP standards
```

---

## Pagination Deep Dive

### Comparaison des stratégies

| Stratégie | Mécanisme | Performance | Saut de page | Stabilité | Complexité |
|---|---|---|---|---|---|
| **Offset** | `?offset=20&limit=10` | O(offset+limit) | Oui | Instable si insertions | Faible |
| **Page** | `?page=3&per_page=10` | O(offset+limit) | Oui | Instable si insertions | Faible |
| **Cursor** | `?cursor=abc&limit=10` | O(limit) | Non | Stable | Moyenne |
| **Keyset** | `?after_id=123&limit=10` | O(limit) | Non | Stable | Moyenne |

### Offset-based Pagination

Acceptable pour les petits datasets (< 100K lignes) ou les interfaces admin avec navigation par numéro de page.

```
GET /api/v1/products?offset=40&limit=20
```

```sql
-- Requête SQL correspondante
SELECT * FROM products
ORDER BY created_at DESC
LIMIT 20 OFFSET 40;
-- ATTENTION : performance O(offset+limit), la DB scanne offset+limit lignes
```

Réponse :

```json
{
  "data": [...],
  "pagination": {
    "offset": 40,
    "limit": 20,
    "total_count": 1542
  }
}
```

### Cursor-based Pagination (recommandée)

Utiliser un curseur opaque (encodé en base64url) contenant les informations de position. Le curseur est un token que seul le serveur interprète.

```
GET /api/v1/orders?cursor=eyJpZCI6MTAwLCJjcmVhdGVkX2F0IjoiMjAyNS0wMS0xNSJ9&limit=25
```

```sql
-- Le curseur décodé contient : {"id": 100, "created_at": "2025-01-15"}
-- Requête SQL correspondante (keyset sous le capot)
SELECT * FROM orders
WHERE (created_at, id) < ('2025-01-15', 100)
ORDER BY created_at DESC, id DESC
LIMIT 26;  -- limit + 1 pour détecter has_more
```

Réponse :

```json
{
  "data": [...],
  "pagination": {
    "has_more": true,
    "next_cursor": "eyJpZCI6NzUsImNyZWF0ZWRfYXQiOiIyMDI1LTAxLTEwIn0",
    "previous_cursor": "eyJpZCI6MTAwLCJjcmVhdGVkX2F0IjoiMjAyNS0wMS0xNSJ9"
  }
}
```

### Keyset Pagination

Variante transparente du cursor-based. Les paramètres de position sont explicites dans l'URL. Très performant avec un index composé.

```
GET /api/v1/events?created_after=2025-01-15T10:00:00Z&after_id=EVT-500&limit=50
```

```sql
-- Requête SQL avec index composé (created_at, id)
SELECT * FROM events
WHERE created_at >= '2025-01-15T10:00:00Z'
  AND (created_at > '2025-01-15T10:00:00Z' OR id > 'EVT-500')
ORDER BY created_at ASC, id ASC
LIMIT 51;
```

### Link Headers (RFC 8288)

Fournir les liens de navigation dans les headers HTTP en plus du body, conformément au standard :

```
Link: <https://api.example.com/v1/orders?cursor=abc123&limit=25>; rel="next",
      <https://api.example.com/v1/orders?cursor=xyz789&limit=25>; rel="prev",
      <https://api.example.com/v1/orders?limit=25>; rel="first"
```

### Total count — Considérations de performance

```
Arbre de décision — Faut-il retourner total_count ?
+-- Le client a-t-il besoin du nombre total ?
    +-- Non → Ne pas le calculer (performance)
    +-- Oui → Le dataset est-il < 100K lignes ?
        +-- Oui → COUNT(*) acceptable, retourner total_count
        +-- Non → Fournir total_count comme estimation
            +-- PostgreSQL : pg_class.reltuples (estimation rapide)
            +-- Ou : retourner has_more sans total_count
            +-- Ou : calculer en async et cacher le résultat
```

---

## Filtering, Sorting & Search

### Query Parameter Patterns

#### Filtrage simple (égalité)

```
GET /api/v1/orders?status=pending&customer_id=CUST-789
```

#### Filtrage avec opérateurs (LHS brackets)

Convention recommandée : le nom du champ suivi de l'opérateur entre crochets.

```
GET /api/v1/orders?created_at[gte]=2025-01-01&created_at[lt]=2025-07-01
GET /api/v1/products?price[lte]=100&category[in]=electronics,books
GET /api/v1/users?name[like]=martin
```

| Opérateur | Signification | Exemple |
|---|---|---|
| `eq` | Égal (défaut) | `?status[eq]=active` |
| `neq` | Différent | `?status[neq]=deleted` |
| `gt` | Supérieur strict | `?price[gt]=50` |
| `gte` | Supérieur ou égal | `?created_at[gte]=2025-01-01` |
| `lt` | Inférieur strict | `?price[lt]=100` |
| `lte` | Inférieur ou égal | `?created_at[lte]=2025-12-31` |
| `in` | Dans une liste | `?status[in]=active,pending` |
| `nin` | Pas dans une liste | `?status[nin]=deleted,archived` |
| `like` | Contient (wildcard) | `?name[like]=mart` |
| `is_null` | Est null | `?deleted_at[is_null]=true` |

#### Sorting

Convention : préfixe `-` pour DESC, `+` ou pas de préfixe pour ASC. Supporter le tri multi-colonnes.

```
GET /api/v1/orders?sort=-created_at,+total_amount
# Tri par created_at DESC puis total_amount ASC
```

#### Full-text Search

Séparer la recherche plein texte du filtrage par champ. Utiliser un paramètre `q` ou `search` dédié.

```
GET /api/v1/products?q=wireless+headphones&category=electronics&sort=-relevance
```

Pour les recherches avancées avec de nombreux critères, considérer un endpoint POST dédié :

```
POST /api/v1/products/search
{
  "query": "wireless headphones",
  "filters": {
    "category": ["electronics"],
    "price": { "min": 20, "max": 200 },
    "in_stock": true
  },
  "sort": [{ "field": "relevance", "order": "desc" }],
  "pagination": { "cursor": null, "limit": 25 }
}
```

---

## Partial Responses & Field Selection

### Fields Parameter (Sparse Fieldsets)

Permettre aux clients de spécifier les champs retournés pour réduire la taille du payload et la charge serveur.

```
GET /api/v1/users?fields=id,name,email
GET /api/v1/orders?fields=id,status,total_amount,customer.name
```

Réponse avec `fields=id,name,email` :

```json
{
  "data": [
    { "id": "USR-123", "name": "Alice Martin", "email": "alice@example.com" },
    { "id": "USR-456", "name": "Bob Dupont", "email": "bob@example.com" }
  ]
}
```

### Expand / Embed Patterns

Permettre l'inclusion de ressources liées pour éviter le problème N+1 (chatty API).

```
# Sans expand : 1 requête pour la commande + 1 requête pour le client
GET /api/v1/orders/ORD-123
# Réponse : { "id": "ORD-123", "customer_id": "CUST-789", ... }

# Avec expand : 1 seule requête
GET /api/v1/orders/ORD-123?expand=customer,items
```

Réponse avec expand :

```json
{
  "id": "ORD-123",
  "status": "pending",
  "customer": {
    "id": "CUST-789",
    "name": "Alice Martin",
    "email": "alice@example.com"
  },
  "items": [
    { "id": "ITEM-1", "product_name": "Widget", "quantity": 3, "unit_price": 29.99 }
  ]
}
```

Contrôler la profondeur d'expansion pour éviter les réponses explosives :

```
# Limiter à 1 niveau d'expansion
GET /api/v1/orders?expand=customer          → OK
# Limiter à 2 niveaux maximum
GET /api/v1/orders?expand=customer.address  → OK
# Refuser au-delà
GET /api/v1/orders?expand=customer.address.country.region → 400 Bad Request
```

---

## Bulk Operations

### Batch Create

Créer plusieurs ressources en une seule requête. Définir clairement la sémantique transactionnelle.

```
POST /api/v1/users/batch
Content-Type: application/json

{
  "items": [
    { "name": "Alice Martin", "email": "alice@example.com", "role": "member" },
    { "name": "Bob Dupont", "email": "bob@example.com", "role": "admin" },
    { "name": "Charlie Lévy", "email": "invalid-email", "role": "member" }
  ]
}
```

### Batch Update

```
PATCH /api/v1/products/batch
Content-Type: application/json

{
  "items": [
    { "id": "PROD-1", "price": 29.99 },
    { "id": "PROD-2", "price": 49.99, "status": "active" },
    { "id": "PROD-999", "price": 19.99 }
  ]
}
```

### Batch Delete

```
DELETE /api/v1/tags/batch
Content-Type: application/json

{
  "ids": ["TAG-1", "TAG-2", "TAG-3"]
}
```

### Transaction Semantics

| Stratégie | Comportement | Réponse en cas d'échec partiel |
|---|---|---|
| **All-or-nothing** | Annule tout si un élément échoue | 422 avec erreurs détaillées |
| **Partial success** | Traite chaque élément indépendamment | 207 Multi-Status avec résultat par élément |
| **Best-effort** | Traite autant que possible, ignore les erreurs | 200 avec compteurs succès/échec |

Réponse avec gestion d'échec partiel (207 Multi-Status) :

```json
{
  "results": [
    { "index": 0, "status": 201, "id": "USR-100", "success": true },
    { "index": 1, "status": 201, "id": "USR-101", "success": true },
    {
      "index": 2,
      "status": 422,
      "success": false,
      "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid email format",
        "field": "email"
      }
    }
  ],
  "summary": {
    "total": 3,
    "succeeded": 2,
    "failed": 1
  }
}
```

### Async Bulk Operations

Pour les opérations en masse dépassant un seuil de volume ou de durée, adopter un pattern asynchrone :

```
POST /api/v1/imports
Content-Type: application/json

{
  "type": "products",
  "source_url": "https://storage.example.com/imports/products-2025.csv",
  "options": { "on_conflict": "update", "batch_size": 500 }
}
```

```
HTTP/1.1 202 Accepted
Location: /api/v1/jobs/JOB-456

{
  "job_id": "JOB-456",
  "status": "queued",
  "estimated_duration_seconds": 120,
  "status_url": "/api/v1/jobs/JOB-456"
}
```

Polling du statut :

```json
{
  "job_id": "JOB-456",
  "status": "processing",
  "progress": { "total": 5000, "processed": 3200, "failed": 12 },
  "started_at": "2025-06-15T10:30:00Z",
  "errors_url": "/api/v1/jobs/JOB-456/errors"
}
```

---

## HATEOAS & Hypermedia

### Principes fondamentaux

HATEOAS (Hypermedia as the Engine of Application State) permet aux clients de naviguer dans l'API en suivant les liens inclus dans les réponses, plutôt que de construire des URLs en dur.

### HAL (Hypertext Application Language)

Format le plus répandu pour les APIs hypermedia. Simple et lisible.

```json
{
  "id": "ORD-123",
  "status": "pending",
  "total": 149.99,
  "_links": {
    "self": { "href": "/orders/ORD-123" },
    "cancel": { "href": "/orders/ORD-123/cancel", "method": "POST" },
    "payment": { "href": "/orders/ORD-123/payment", "method": "POST" },
    "customer": { "href": "/customers/CUST-789" }
  },
  "_embedded": {
    "items": [
      {
        "id": "ITEM-1",
        "product": "Widget",
        "_links": { "self": { "href": "/order-items/ITEM-1" } }
      }
    ]
  }
}
```

### JSON:API

Standard plus structuré avec séparation des données, relations et métadonnées.

```json
{
  "data": {
    "type": "orders",
    "id": "ORD-123",
    "attributes": { "status": "pending", "total": 149.99 },
    "relationships": {
      "customer": { "data": { "type": "customers", "id": "CUST-789" } },
      "items": { "data": [{ "type": "order-items", "id": "ITEM-1" }] }
    },
    "links": { "self": "/orders/ORD-123" }
  },
  "included": [
    { "type": "customers", "id": "CUST-789", "attributes": { "name": "Alice" } }
  ]
}
```

### Siren

Format riche avec actions et sous-entités. Adapté aux workflows complexes.

```json
{
  "class": ["order"],
  "properties": { "id": "ORD-123", "status": "pending", "total": 149.99 },
  "actions": [
    {
      "name": "cancel-order",
      "title": "Cancel Order",
      "method": "POST",
      "href": "/orders/ORD-123/cancel",
      "type": "application/json"
    }
  ],
  "links": [
    { "rel": ["self"], "href": "/orders/ORD-123" },
    { "rel": ["customer"], "href": "/customers/CUST-789" }
  ]
}
```

### Approche pragmatique

```
Arbre de décision — HATEOAS, quand l'appliquer ?
+-- L'API a-t-elle des workflows avec transitions d'état ?
|   +-- Oui → HATEOAS apporte de la valeur (liens d'actions dynamiques)
|   +-- Non → CRUD simple, HATEOAS est superflu
+-- Les consommateurs sont-ils des clients génériques (navigateurs, crawlers) ?
|   +-- Oui → HATEOAS facilite la découverte
|   +-- Non → Les consommateurs connaissent l'API, liens statiques suffisent
+-- L'API est-elle publique avec beaucoup de consommateurs ?
    +-- Oui → HATEOAS réduit le couplage client-serveur
    +-- Non → API interne, la documentation OpenAPI suffit

Recommandation : adopter un HATEOAS léger (liens self + actions possibles)
sans imposer un format complet comme Siren pour les APIs standard.
```

---

## Caching

### ETags (Entity Tags)

#### Strong ETags

Représentent une correspondance exacte octet par octet de la ressource. Générés à partir d'un hash du contenu.

```
# Réponse initiale
HTTP/1.1 200 OK
ETag: "a1b2c3d4e5f6"

# Requête conditionnelle
GET /api/v1/products/PROD-123
If-None-Match: "a1b2c3d4e5f6"

# Si la ressource n'a pas changé
HTTP/1.1 304 Not Modified
```

#### Weak ETags

Représentent une équivalence sémantique (pas nécessairement identique octet par octet). Préfixés par `W/`.

```
ETag: W/"v42"
# Utilisé quand le contenu peut varier légèrement (formatage, whitespace)
# tout en étant sémantiquement identique
```

### Last-Modified / If-Modified-Since

Alternative aux ETags basée sur les timestamps. Moins précis mais plus simple.

```
# Réponse initiale
HTTP/1.1 200 OK
Last-Modified: Wed, 15 Jan 2025 10:30:00 GMT

# Requête conditionnelle
GET /api/v1/products/PROD-123
If-Modified-Since: Wed, 15 Jan 2025 10:30:00 GMT

# Si la ressource n'a pas changé
HTTP/1.1 304 Not Modified
```

### Cache-Control Directives

| Directive | Effet | Cas d'usage |
|---|---|---|
| `public` | Cacheable par tous (CDN, proxies, navigateur) | Données publiques (catalogue) |
| `private` | Cacheable uniquement par le navigateur | Données utilisateur |
| `no-cache` | Valider auprès du serveur avant d'utiliser le cache | Données fréquemment mises à jour |
| `no-store` | Ne jamais stocker (aucun cache) | Données sensibles (finances) |
| `max-age=N` | Durée de validité en secondes | Données stables |
| `s-maxage=N` | Durée pour les caches partagés (CDN) | Override max-age pour CDN |
| `stale-while-revalidate=N` | Servir le cache périmé pendant la revalidation | Haute disponibilité |
| `immutable` | Ne jamais revalider | Assets versionnés (CSS/JS avec hash) |

Exemples de combinaisons :

```
# Catalogue produits — cache CDN 5 min, revalidation en arrière-plan
Cache-Control: public, s-maxage=300, stale-while-revalidate=60

# Profil utilisateur — cache navigateur seul, 1 min
Cache-Control: private, max-age=60

# Données financières — jamais cacher
Cache-Control: no-store

# Ressource avec ETag — toujours revalider
Cache-Control: no-cache
ETag: "abc123"
```

### Conditional Requests — Mise à jour optimiste

Utiliser les requêtes conditionnelles pour éviter les conflits de mise à jour (lost update problem).

```
# 1. Le client lit la ressource et reçoit l'ETag
GET /api/v1/products/PROD-123
→ ETag: "v42"

# 2. Le client met à jour en envoyant l'ETag
PUT /api/v1/products/PROD-123
If-Match: "v42"
{ "name": "Widget Pro", "price": 39.99 }

# 3a. Si personne n'a modifié entre-temps
→ 200 OK + ETag: "v43"

# 3b. Si un autre client a modifié la ressource
→ 412 Precondition Failed
# Le client doit relire la ressource et résoudre le conflit
```

### CDN Integration

```
Arbre de décision — Stratégie de cache CDN :
+-- L'endpoint retourne-t-il des données identiques pour tous les utilisateurs ?
|   +-- Oui → Cache CDN (public, s-maxage)
|   +-- Non → L'endpoint varie-t-il par un header prévisible ?
|       +-- Oui → Vary header + cache CDN conditionnel
|       +-- Non → Pas de cache CDN (private ou no-store)
+-- Les données changent-elles rarement ?
    +-- Oui → TTL long (s-maxage=3600) + stale-while-revalidate
    +-- Non → TTL court (s-maxage=60) + revalidation ETag
```

```
# Headers pour cache CDN avec variation par langue
Cache-Control: public, s-maxage=300, stale-while-revalidate=60
Vary: Accept-Language, Accept-Encoding
Surrogate-Key: products product-PROD-123
# Surrogate-Key permet l'invalidation ciblée sur Fastly, Cloudflare, etc.
```

---

## State of the Art (2025-2026)

### JSON:API 1.1

La spécification JSON:API 1.1 apporte des améliorations significatives par rapport à la version 1.0 : support natif des profils d'extension (permettant de standardiser les extensions custom), opérations atomiques pour les mutations batch, et meilleure intégration avec les systèmes d'événements. Considérer JSON:API comme format standard lorsque l'API nécessite des relations complexes et une sérialisation cohérente.

### OpenAPI 3.1

OpenAPI 3.1 aligne complètement le schéma avec JSON Schema 2020-12, éliminant les divergences des versions précédentes. Utiliser OpenAPI 3.1 pour toute nouvelle spécification. Les outils modernes (Scalar, Redocly, Speakeasy) supportent pleinement cette version et permettent la génération automatique de SDKs type-safe, de documentation interactive et de contract tests.

### HTTP/3 & QUIC

HTTP/3, basé sur le protocole de transport QUIC, élimine le head-of-line blocking au niveau transport et réduit significativement la latence de connexion (0-RTT handshake). Pour les APIs REST, les bénéfices principaux sont :
- Meilleure performance sur réseaux instables (mobile, Wi-Fi).
- Multiplexage sans blocage inter-streams.
- Migration de connexion transparente (changement de réseau sans interruption).
- Support croissant des CDN et load balancers (Cloudflare, AWS CloudFront, Nginx).

### API Mesh & Composable APIs

L'approche API Mesh consiste à composer des APIs provenant de sources multiples en une interface unifiée. Plutôt que de dupliquer la logique d'agrégation dans chaque client, un mesh layer centralise la composition, la transformation et le routage. Les outils comme GraphQL Mesh, API Gateway composition (Kong, Tyk) et les BFF patterns facilitent cette approche. Combiner avec les Packaged Business Capabilities (PBCs) de l'architecture MACH pour construire des systèmes modulaires et composables.

### Tendances émergentes

| Tendance | Impact sur le design REST | Maturité |
|---|---|---|
| **AI-friendly APIs** | Descriptions sémantiques riches, tool-use formats (MCP), découvrabilité | Adoption rapide |
| **WebTransport** | Alternative aux WebSockets basée sur HTTP/3, datagrams | Expérimental |
| **Idempotency-Key standard (IETF)** | Standardisation du header pour les retries sûrs | Draft avancé |
| **RateLimit headers (RFC 9110)** | Standardisation de RateLimit-Limit/Remaining/Reset | Adoption en cours |
| **Structured Fields (RFC 8941)** | Format structuré pour les headers HTTP | Stable |
| **API Linting as Code** | Spectral, Optic, Redocly CLI intégrés dans le CI/CD | Mainstream |
