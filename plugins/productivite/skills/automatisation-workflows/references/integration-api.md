# Integration API & Connecteurs — REST, Webhooks, OAuth, Synchronisation & Transformation

## Overview

Ce document de reference couvre les fondamentaux de l'integration API dans le contexte de l'automatisation de workflows no-code et low-code. Il fournit les bases necessaires pour comprendre, configurer et debugger les appels API REST, les webhooks, les mecanismes d'authentification (API key, OAuth 2.0, Bearer token) et les patterns de synchronisation de donnees. L'objectif est de rendre les non-developpeurs autonomes dans la configuration d'integrations API fiables et securisees, et de fournir aux developpeurs les patterns avances pour les cas complexes.

---

## 1. REST API — Fondamentaux pour les Non-Developpeurs

### Qu'est-ce qu'une API REST

Une API (Application Programming Interface) REST est un ensemble de regles qui permet a deux applications de communiquer entre elles via le protocole HTTP. Quand un workflow N8N, Zapier ou Make "se connecte" a une application, il utilise l'API de cette application pour lire ou modifier des donnees.

**Analogie** : une API est comme un serveur dans un restaurant. Le client (votre workflow) ne va pas en cuisine (la base de donnees) — il passe commande au serveur (l'API) qui rapporte le plat (les donnees).

### Structure d'une requete API

Chaque appel API comporte 5 elements :

| Element | Description | Exemple |
|---|---|---|
| **URL (endpoint)** | L'adresse de la ressource | `https://api.hubspot.com/crm/v3/contacts` |
| **Methode HTTP** | L'action a effectuer | GET, POST, PUT, PATCH, DELETE |
| **Headers** | Metadonnees de la requete | `Authorization: Bearer token123` |
| **Body** | Les donnees envoyees (POST, PUT, PATCH) | `{"email": "john@example.com", "name": "John"}` |
| **Query parameters** | Filtres et options dans l'URL | `?limit=100&offset=0&status=active` |

### Methodes HTTP

| Methode | Action | Equivalent CRUD | Idempotent | Body |
|---|---|---|---|---|
| **GET** | Lire des donnees | Read | Oui | Non |
| **POST** | Creer une ressource | Create | Non | Oui |
| **PUT** | Remplacer une ressource entiere | Update (total) | Oui | Oui |
| **PATCH** | Modifier partiellement une ressource | Update (partiel) | Oui* | Oui |
| **DELETE** | Supprimer une ressource | Delete | Oui | Non |

*PATCH est idempotent si l'operation de modification est elle-meme idempotente (ex: `set field = value`).

**Regles d'utilisation** :
- Utiliser GET pour la lecture (ne jamais modifier des donnees avec un GET)
- Utiliser POST pour la creation (attention aux doublons — verifier si un upsert est possible)
- Privilegier PATCH sur PUT pour les mises a jour partielles (moins de risque d'ecraser des champs)
- Utiliser DELETE avec prudence (verifier si un soft delete est preferable)

### Codes de Statut HTTP

Comprendre les codes de statut est essentiel pour le debugging et la gestion d'erreurs :

| Code | Categorie | Signification | Action dans le workflow |
|---|---|---|---|
| **200** | Succes | Requete reussie | Continuer le traitement |
| **201** | Succes | Ressource creee | Continuer, extraire l'ID de la nouvelle ressource |
| **204** | Succes | Succes sans contenu | Continuer (pas de body en retour) |
| **301/302** | Redirection | URL deplacee | La plupart des clients HTTP suivent automatiquement |
| **400** | Erreur client | Requete malformee | Verifier le format du body et les champs requis |
| **401** | Erreur client | Non authentifie | Verifier le token/API key, renouveler si expire |
| **403** | Erreur client | Non autorise | Verifier les permissions/scopes du token |
| **404** | Erreur client | Ressource introuvable | Verifier l'URL et l'ID de la ressource |
| **409** | Erreur client | Conflit (doublon) | La ressource existe deja — utiliser un upsert |
| **422** | Erreur client | Donnees invalides | Verifier les valeurs des champs (format, type, obligatoire) |
| **429** | Erreur client | Rate limit depasse | Attendre et reessayer (lire le header Retry-After) |
| **500** | Erreur serveur | Erreur interne | Reessayer (erreur transitoire cote serveur) |
| **502/503** | Erreur serveur | Service indisponible | Reessayer avec backoff (le service est temporairement down) |
| **504** | Erreur serveur | Timeout gateway | Reessayer, verifier si l'operation a quand meme ete executee |

**Regles de gestion des erreurs par code** :
- 4xx (sauf 429) : ne pas retrier, corriger la requete
- 429 : retrier apres le delai indique dans le header `Retry-After`
- 5xx : retrier avec backoff exponentiel (1s, 2s, 4s, 8s)

---

## 2. Patterns d'Authentification

### API Key

Le mecanisme le plus simple : une cle secrete envoyee avec chaque requete.

**Transmission** :
- Header : `Authorization: Api-Key sk_live_EXAMPLE_KEY_REPLACE_ME` ou `X-API-Key: sk_live_EXAMPLE_KEY_REPLACE_ME`
- Query parameter : `?api_key=sk_live_EXAMPLE_KEY_REPLACE_ME` (deconseille — visible dans les logs)

**Avantages** : simple, pas d'expiration automatique, pas de flux d'autorisation complexe.
**Inconvenients** : pas de scoping granulaire, rotation manuelle, pas de revocation partielle.

**Bonnes pratiques** :
1. Toujours transmettre la cle via header (jamais en query parameter)
2. Stocker la cle dans le credential store de la plateforme (jamais en clair dans le workflow)
3. Utiliser des cles differentes par environnement (dev, staging, production)
4. Rotation tous les 90 jours ou immediatement en cas de suspicion de compromission
5. Restreindre les permissions de la cle au minimum necessaire (si l'API le permet)

**Configuration dans les plateformes** :

| Plateforme | Configuration |
|---|---|
| **N8N** | Credential type "Header Auth" ou "API Key" avec champ Header Name et Header Value |
| **Zapier** | Configure dans la connexion de l'app, stocke dans le vault Zapier |
| **Make** | Connexion custom avec header personnalise ou module HTTP avec headers |
| **Power Automate** | Custom connector avec API Key authentication ou HTTP action avec headers |

### OAuth 2.0

Le standard d'authentification moderne, utilise par Google, Microsoft, Salesforce, HubSpot, Slack et la majorite des API SaaS.

**Flux Authorization Code (le plus courant)** :

```
1. L'utilisateur clique "Connecter" dans la plateforme
2. Redirection vers la page d'autorisation du service (ex: Google)
3. L'utilisateur se connecte et autorise l'acces
4. Le service renvoie un "authorization code" a la plateforme
5. La plateforme echange le code contre un "access token" et un "refresh token"
6. L'access token est utilise pour les appels API (valide 1-24h)
7. Quand l'access token expire, le refresh token obtient un nouveau access token
```

**Composants OAuth 2.0** :

| Composant | Description | Duree de vie |
|---|---|---|
| **Client ID** | Identifiant de l'application | Permanent |
| **Client Secret** | Secret de l'application | Permanent (a proteger) |
| **Authorization Code** | Code temporaire echange contre les tokens | ~10 minutes |
| **Access Token** | Token d'acces pour les appels API | 1-24 heures |
| **Refresh Token** | Token pour renouveler l'access token | 30-90 jours ou permanent |
| **Scopes** | Permissions demandees | Definis a la connexion |

**Scopes courants** :

```
Google :
  - gmail.readonly (lire les emails)
  - gmail.send (envoyer des emails)
  - drive.readonly (lire les fichiers Drive)
  - sheets (lire et ecrire dans Google Sheets)
  - calendar.events (gerer les evenements de calendrier)

Slack :
  - chat:write (poster des messages)
  - channels:read (lire la liste des canaux)
  - users:read (lire les profils utilisateurs)

HubSpot :
  - crm.objects.contacts.read (lire les contacts)
  - crm.objects.contacts.write (modifier les contacts)
  - crm.objects.deals.read (lire les deals)
```

**Gestion dans les plateformes no-code** :

Les plateformes gerent le flux OAuth 2.0 automatiquement pour les connecteurs natifs. L'utilisateur clique sur "Connect", s'authentifie, et la plateforme gere le stockage des tokens et leur renouvellement. Pour les API custom, il faut configurer manuellement :
- Client ID et Client Secret
- Authorization URL et Token URL
- Scopes necessaires
- Redirect URI (fourni par la plateforme)

### Bearer Token

Un token d'acces envoye dans le header Authorization. C'est generalement le resultat d'un flux OAuth 2.0 ou d'une generation manuelle dans l'interface de l'API.

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Difference avec API Key** : un Bearer token a generalement une duree de vie limitee et peut etre scoped (permissions specifiques), tandis qu'une API key est souvent permanente et offre un acces complet.

### Authentification personnalisee

Certaines API utilisent des schemas d'authentification non standard :

| Schema | Exemple | Configuration |
|---|---|---|
| **Basic Auth** | `Authorization: Basic base64(user:pass)` | Login + mot de passe encodes en Base64 |
| **Digest Auth** | Challenge-response avec hash | Rare, gere par certains clients HTTP |
| **HMAC Signature** | Signature du body avec un secret partage | Calcul de hash (SHA-256) du payload |
| **Custom Header** | `X-Custom-Auth: token` | Header personnalise |
| **Session Cookie** | Cookie de session apres login | Login initial puis envoi du cookie |

---

## 3. Webhooks — Configuration et Securite

### Fonctionnement des webhooks

Un webhook est un appel HTTP envoye automatiquement par un service quand un evenement se produit. C'est un "callback" : au lieu de demander periodiquement "y a-t-il du nouveau ?" (polling), le service dit "je t'appelle quand il y a du nouveau" (push).

**Configuration typique** :

```
1. Generer une URL de webhook dans votre plateforme d'automatisation
   Ex: https://hooks.zapier.com/hooks/catch/123456/abcdef/
   Ex: https://n8n.example.com/webhook/order-created
   Ex: https://hook.eu1.make.com/abc123def456

2. Enregistrer cette URL dans le service source
   Ex: HubSpot > Settings > Webhooks > Add URL

3. Configurer les evenements a recevoir
   Ex: contact.created, deal.updated, invoice.paid

4. Le service source enverra un POST a l'URL quand l'evenement se produit
```

### Securisation des webhooks

#### HMAC Signature

La methode de securisation la plus courante. Le service source signe le payload avec un secret partage, et le recepteur verifie la signature.

**Processus** :

```
Cote source (ex: Stripe) :
  1. Calculer la signature : HMAC-SHA256(webhook_secret, payload)
  2. Envoyer la signature dans un header : Stripe-Signature: t=timestamp,v1=signature

Cote recepteur (votre workflow) :
  1. Extraire la signature du header
  2. Recalculer la signature avec le meme secret et le body recu
  3. Comparer les deux signatures
  4. Si identiques : traiter le webhook
  5. Si differentes : rejeter (401 Unauthorized)
```

**Implementation dans N8N** :

```javascript
// Code Node — Validation HMAC
const crypto = require('crypto');
const secret = $env.WEBHOOK_SECRET;
const signature = $input.first().headers['x-signature'];
const payload = JSON.stringify($input.first().json);

const expected = crypto
  .createHmac('sha256', secret)
  .update(payload)
  .digest('hex');

if (signature !== expected) {
  throw new Error('Invalid webhook signature');
}

// Signature valide, continuer le traitement
return $input.all();
```

#### IP Whitelisting

Restreindre les appels webhook aux adresses IP connues du service source :

```
Services courants et leurs IP :
- Stripe : publier sur https://stripe.com/docs/ips
- GitHub : https://api.github.com/meta (webhooks key)
- HubSpot : documentation des IP ranges
```

**Implementation** : configurer le firewall ou le reverse proxy (nginx, Cloudflare) pour n'accepter que les IP autorisees sur l'URL du webhook.

#### Token dans l'URL

Inclure un token secret dans l'URL du webhook :

```
https://n8n.example.com/webhook/order-created?token=SECRET_TOKEN_REPLACE_ME
```

Moins securise que HMAC (le token est dans les logs d'URL) mais simple a implementer et suffisant pour les cas d'usage non critiques.

### Fiabilite des webhooks

Les webhooks ne sont pas garantis : le reseau peut echouer, le recepteur peut etre temporairement indisponible. Strategies pour garantir la fiabilite :

1. **Reponse rapide** : repondre avec un 200 OK dans les 5 secondes. Traiter le payload de maniere asynchrone si le traitement est long.

2. **Gestion des re-deliveries** : la plupart des services renvoient le webhook si pas de reponse 2xx. Implementer l'idempotence (deduplication par event_id) pour eviter les doublons.

3. **Queue intermediaire** : pour les webhooks critiques, stocker le payload dans une queue (Redis, base de donnees) avant le traitement. Le traitement echoue sans perdre le payload.

4. **Dead Letter Queue** : si le traitement echoue apres retries, stocker le webhook dans une DLQ pour investigation manuelle.

5. **Monitoring des webhooks** : surveiller le volume de webhooks recus et alerter en cas de chute soudaine (peut indiquer un probleme de configuration ou une desynchronisation).

### Webhook vs Polling — Decision

| Critere | Webhook | Polling |
|---|---|---|
| **Latence** | Temps reel (secondes) | 1-15 minutes |
| **Efficacite** | Tres efficace (appel uniquement quand evenement) | Gaspillage (appels meme sans changement) |
| **Configuration** | Plus complexe (URL, securite, validation) | Plus simple (juste l'API key) |
| **Fiabilite** | Risque de perte si recepteur down | Aucun risque de perte (les donnees sont dans l'API) |
| **Prerequis** | Le service source doit supporter les webhooks | Toute API est pollable |
| **Cout** | Moins de tasks/operations | Plus de tasks/operations |

**Recommandation** : utiliser les webhooks quand disponibles. Ajouter un polling de reconciliation quotidien pour detecter les webhooks manques.

---

## 4. Data Mapping et Transformation

### Mapping entre systemes

La transformation de donnees entre deux API differentes est l'une des taches les plus courantes en integration :

**Exemple : HubSpot vers Salesforce**

```
HubSpot (source)              Salesforce (cible)
---                           ---
properties.firstname    -->   FirstName
properties.lastname     -->   LastName
properties.email        -->   Email
properties.phone        -->   Phone
properties.company      -->   Account.Name (lookup)
properties.lifecyclestage --> LeadSource (mapping de valeurs)
  "lead"               -->   "Web"
  "marketingqualifiedlead" --> "Marketing"
  "salesqualifiedlead"  --> "Sales"
properties.createdate   -->   CreatedDate (format ISO -> SF format)
```

### Transformation de formats

| Transformation | Source | Cible | Methode |
|---|---|---|---|
| **Date** | "2025-12-31" | "31/12/2025" | `formatDate()` ou `moment.js` |
| **Devise** | 1234.56 | "1 234,56 EUR" | `toLocaleString()` + devise |
| **Telephone** | "(555) 123-4567" | "+15551234567" | Regex + prefixe pays |
| **Boolean** | "Yes"/"No" | true/false | Mapping conditionnel |
| **Enum** | "active" | 1 | Lookup table |
| **Nom** | "John DOE" | { first: "John", last: "Doe" } | Split + capitalize |
| **Adresse** | JSON structure | "Rue, CP Ville, Pays" | Concatenation formatee |

### JSON Path et acces aux donnees

Naviguer dans les structures JSON complexes retournees par les API :

```json
{
  "data": {
    "customer": {
      "id": 12345,
      "name": "Acme Corp",
      "contacts": [
        {
          "email": "john@acme.com",
          "role": "decision_maker",
          "phone": {
            "mobile": "+33612345678",
            "office": "+33112345678"
          }
        },
        {
          "email": "jane@acme.com",
          "role": "technical",
          "phone": {
            "mobile": "+33698765432"
          }
        }
      ],
      "metadata": {
        "created_at": "2025-01-15T10:30:00Z",
        "source": "website"
      }
    }
  }
}
```

**Acces aux donnees** :

| Donnee | JSON Path | N8N | Make |
|---|---|---|---|
| Nom du client | `data.customer.name` | `{{$json.data.customer.name}}` | `{{1.data.customer.name}}` |
| Email du 1er contact | `data.customer.contacts[0].email` | `{{$json.data.customer.contacts[0].email}}` | `{{1.data.customer.contacts[1].email}}` (index 1 dans Make) |
| Telephone mobile | `data.customer.contacts[0].phone.mobile` | `{{$json.data.customer.contacts[0].phone.mobile}}` | `{{1.data.customer.contacts[1].phone.mobile}}` |
| Date de creation | `data.customer.metadata.created_at` | `{{$json.data.customer.metadata.created_at}}` | `{{1.data.customer.metadata.created_at}}` |
| Nombre de contacts | `data.customer.contacts.length` | `{{$json.data.customer.contacts.length}}` | `{{length(1.data.customer.contacts)}}` |

---

## 5. Pagination

### Pourquoi la pagination

Les API limitent le nombre de resultats par requete (typiquement 20-100 elements) pour des raisons de performance. Pour recuperer tous les elements, il faut faire plusieurs requetes.

### Types de pagination

#### Offset-based

Le plus courant. Utilise `limit` et `offset` (ou `page` et `per_page`).

```
GET /api/contacts?limit=100&offset=0    --> elements 1 a 100
GET /api/contacts?limit=100&offset=100  --> elements 101 a 200
GET /api/contacts?limit=100&offset=200  --> elements 201 a 300
...jusqu'a recevoir moins de 100 elements (fin de la liste)
```

**Implementation dans les workflows** :

```
Variable : offset = 0
Variable : all_results = []

Boucle :
  --> GET /api/contacts?limit=100&offset={offset}
  --> Ajouter les resultats a all_results
  --> Si nombre de resultats < 100 : sortir de la boucle
  --> Sinon : offset = offset + 100, recommencer
```

**Inconvenient** : les inserts ou suppressions pendant la pagination peuvent causer des doublons ou des omissions.

#### Cursor-based

Utilise un "cursor" (token opaque) pour marquer la position dans la liste. Plus fiable que l'offset-based.

```
GET /api/contacts?limit=100
  Response : { data: [...], next_cursor: "abc123" }

GET /api/contacts?limit=100&cursor=abc123
  Response : { data: [...], next_cursor: "def456" }

GET /api/contacts?limit=100&cursor=def456
  Response : { data: [...], next_cursor: null }  --> fin de la liste
```

**API utilisant la pagination cursor** : Slack, Stripe, Facebook Graph API, Notion.

#### Link-based

L'API fournit l'URL complete de la page suivante dans les headers ou le body.

```
Response headers :
  Link: <https://api.example.com/contacts?page=2>; rel="next"

Response body :
  { "data": [...], "links": { "next": "https://api.example.com/contacts?page=2" } }
```

**API utilisant la pagination link** : GitHub API, certaines API REST standards.

### Pagination dans les plateformes no-code

| Plateforme | Support pagination |
|---|---|
| **N8N** | Manuel via boucle "Split In Batches" ou "HTTP Request" avec pagination options |
| **Zapier** | Automatique pour les connecteurs natifs, manuel pour les webhooks/HTTP |
| **Make** | Module "Repeater" + HTTP Request, ou pagination native des connecteurs |
| **Power Automate** | "Do Until" loop + HTTP action, ou pagination native des connecteurs |

---

## 6. Rate Limiting et Throttling

### Comprendre le rate limiting

Les API limitent le nombre de requetes par periode pour proteger leurs serveurs. Depasser la limite retourne une erreur 429 (Too Many Requests).

### Limites courantes

| API | Limite | Periode | Header de limite |
|---|---|---|---|
| **HubSpot** | 100 requetes | 10 secondes | `X-HubSpot-RateLimit-Daily-Remaining` |
| **Slack** | 1 requete | 1 seconde (Tier 1) | `X-RateLimit-Remaining` |
| **Google Sheets** | 60 requetes | 60 secondes par utilisateur | `X-RateLimit-Remaining` |
| **Stripe** | 100 requetes | 1 seconde (live) | `RateLimit-Remaining` |
| **Notion** | 3 requetes | 1 seconde | `X-RateLimit-Remaining` |
| **Salesforce** | Variable | 24 heures | `Sforce-Limit-Info` |
| **GitHub** | 5000 requetes | 1 heure (authenticated) | `X-RateLimit-Remaining` |

### Strategies de throttling

#### Strategie 1 — Delai fixe entre les requetes

Ajouter un delai entre chaque appel API pour rester sous la limite :

```
Pour HubSpot (100 req/10s) :
  Delai = 10s / 100 = 100ms entre chaque requete

Pour Notion (3 req/s) :
  Delai = 1s / 3 = 333ms entre chaque requete
```

#### Strategie 2 — Batching

Regrouper les operations pour reduire le nombre d'appels :

```
Au lieu de :
  POST /contacts (1 contact) x 100 = 100 requetes

Faire :
  POST /contacts/batch (100 contacts) x 1 = 1 requete
```

API avec support batch : HubSpot, Salesforce, Google, Notion, Airtable.

#### Strategie 3 — Retry sur 429

Quand l'API retourne un 429, attendre et reessayer :

```
Appel API
  --> 429 Too Many Requests
  --> Lire le header Retry-After (ex: 5 secondes)
  --> Attendre 5 secondes
  --> Reessayer
  --> 200 OK : continuer
```

#### Strategie 4 — Quota monitoring

Surveiller la consommation du quota en lisant les headers de rate limit :

```
Apres chaque appel :
  Remaining = header['X-RateLimit-Remaining']
  Reset = header['X-RateLimit-Reset']

  Si Remaining < 10 :
    Attendre jusqu'a Reset
    Ou ralentir les appels
```

---

## 7. Synchronisation Temps Reel vs Batch

### Comparaison

| Dimension | Temps reel (webhook/event) | Batch (schedule/polling) |
|---|---|---|
| **Latence** | Secondes | Minutes a heures |
| **Complexite** | Elevee (idempotence, ordre, retries) | Faible (traitement en bloc) |
| **Volume** | Unitaire (1 evenement = 1 traitement) | En masse (N elements par cycle) |
| **Coherence** | Eventuelle (delai entre source et cible) | Periodique (coherent a chaque cycle) |
| **Cout** | Variable (depend du volume d'evenements) | Previsible (fixe par cycle) |
| **Resilience** | Risque de perte de webhooks | Pas de perte (les donnees sont dans l'API) |

### Quand utiliser le temps reel

- Notifications et alertes (un deal est cree, un paiement est recu)
- Actions critiques necessitant une reponse immediate (approbation, escalade)
- Synchronisation ou la latence impacte l'experience utilisateur
- Evenements peu frequents (< 100/heure)

### Quand utiliser le batch

- Synchronisations massives (import/export de donnees)
- Rapports et agregations periodiques
- Traitements lourds en termes de calcul ou d'API calls
- Reconciliation de donnees entre systemes
- Evenements tres frequents (> 1000/heure) ou le cout unitaire du temps reel est prohibitif

### Pattern hybride recommande

Combiner les deux approches pour le meilleur des deux mondes :

```
Temps reel (webhook) :
  --> Traiter les evenements au fil de l'eau
  --> Synchronisation unitaire immediate

Batch quotidien (schedule) :
  --> Reconciliation : verifier que tous les webhooks ont bien ete traites
  --> Rattrapage : traiter les evenements manques
  --> Nettoyage : corriger les incoherences
```

---

## 8. Patterns d'Integration API Courants

### CRUD Standard

Les operations de base sur une ressource :

```
Creer :   POST   /api/v1/contacts       + body JSON
Lire un : GET    /api/v1/contacts/{id}
Lire tous : GET  /api/v1/contacts        + query params (pagination, filtres)
Modifier : PATCH /api/v1/contacts/{id}   + body JSON (champs modifies)
Supprimer : DELETE /api/v1/contacts/{id}
```

### Search

Rechercher des ressources par criteres :

```
GET /api/v1/contacts/search?q=john&field=email
POST /api/v1/contacts/search + body { "filters": [...] }
```

Certaines API (HubSpot, Salesforce, Notion) utilisent POST pour les recherches complexes avec un body JSON contenant les criteres.

### Bulk Operations

Traiter plusieurs elements en une seule requete :

```
POST /api/v1/contacts/batch
Body : {
  "inputs": [
    { "email": "john@example.com", "name": "John" },
    { "email": "jane@example.com", "name": "Jane" },
    { "email": "bob@example.com", "name": "Bob" }
  ]
}

Response : {
  "results": [
    { "id": "1", "status": "created" },
    { "id": "2", "status": "created" },
    { "id": null, "status": "error", "message": "Invalid email" }
  ]
}
```

**Regles pour les bulk operations** :
1. Verifier la taille de batch maximale documentee par l'API (souvent 100-1000 elements)
2. Gerer les reponses partielles (certains elements reussissent, d'autres echouent)
3. Logger les erreurs individuelles pour retraitement
4. Utiliser les bulk operations pour reduire le nombre d'appels API et respecter les rate limits

---

## 9. Integrations API Populaires

### Slack

**Cas d'usage** : notifications, alertes, commandes, reporting dans les canaux.

| Action | Endpoint | Methode |
|---|---|---|
| Poster un message | `chat.postMessage` | POST |
| Mettre a jour un message | `chat.update` | POST |
| Lister les canaux | `conversations.list` | GET |
| Ajouter une reaction | `reactions.add` | POST |
| Uploader un fichier | `files.upload` | POST |

**Bonnes pratiques Slack** :
- Utiliser les Block Kit pour des messages riches et interactifs
- Utiliser un webhook Slack pour les notifications simples (pas besoin d'app Slack complete)
- Respecter le rate limiting (1 msg/s par canal pour les bots)
- Utiliser les threads pour les conversations liees (eviter de polluer les canaux)

### Google (Sheets, Drive, Calendar)

**Google Sheets** — le "base de donnees du pauvre" souvent utilise dans les automatisations :

| Action | Usage | Attention |
|---|---|---|
| Lire des lignes | Data source pour les workflows | Rate limit : 60 req/min/user |
| Ecrire des lignes | Stocker les resultats | Limiter les ecritures (batch si possible) |
| Mettre a jour une ligne | Modifier un statut, un montant | Identifier la ligne par un ID unique |
| Supprimer une ligne | Nettoyage | Preferer le soft delete (colonne "archive") |

**Google Drive** :
- Trigger sur nouveau fichier dans un dossier
- Upload de fichiers generes par le workflow
- Gestion des permissions de partage

**Google Calendar** :
- Creer des evenements automatiquement
- Verifier la disponibilite avant de planifier
- Envoyer des rappels personnalises

### HubSpot

**CRM de reference pour les workflows marketing et sales** :

| Action | Endpoint | Rate limit |
|---|---|---|
| Creer un contact | `/crm/v3/objects/contacts` | 100 req/10s |
| Rechercher des contacts | `/crm/v3/objects/contacts/search` | 4 req/s |
| Creer un deal | `/crm/v3/objects/deals` | 100 req/10s |
| Batch create | `/crm/v3/objects/contacts/batch/create` | 100 contacts/batch |
| Webhooks | Subscription API | Temps reel |

### Stripe

**Plateforme de paiement avec une API exemplaire** :

| Evenement webhook | Cas d'usage |
|---|---|
| `payment_intent.succeeded` | Confirmer la commande, envoyer la facture |
| `invoice.paid` | Mettre a jour le CRM, renouveler l'abonnement |
| `customer.subscription.deleted` | Declencher le processus de retention |
| `charge.failed` | Notifier le client, tenter un autre moyen de paiement |
| `checkout.session.completed` | Provisionner le service, envoyer l'email de bienvenue |

**Bonnes pratiques Stripe** :
- Toujours valider la signature du webhook avec le signing secret
- Utiliser les cles d'idempotence pour les operations de creation
- Tester avec les cles de test (mode test) avant la production
- Utiliser les events Stripe plutot que le polling pour la synchronisation

### Notion

**Base de donnees et wiki utilises comme backend pour les automatisations** :

| Action | Endpoint | Rate limit |
|---|---|---|
| Creer une page | `POST /v1/pages` | 3 req/s |
| Mettre a jour une page | `PATCH /v1/pages/{id}` | 3 req/s |
| Query une database | `POST /v1/databases/{id}/query` | 3 req/s |
| Rechercher | `POST /v1/search` | 3 req/s |

**Bonnes pratiques Notion** :
- Respecter le rate limit strict (3 req/s) — ajouter des delais dans les boucles
- Utiliser les filtres dans les queries pour reduire le volume de donnees
- Notion ne supporte pas les webhooks natifs — utiliser un service tiers (Notion Watcher, Make trigger) ou le polling

---

## 10. Debugging des Appels API

### Outils de debugging

| Outil | Usage | Prix |
|---|---|---|
| **Postman** | Tester les appels API manuellement | Gratuit (basic) |
| **Insomnia** | Alternative a Postman, plus legere | Gratuit (basic) |
| **cURL** | Tester les appels en ligne de commande | Gratuit |
| **webhook.site** | Capturer et inspecter les webhooks entrants | Gratuit (basic) |
| **RequestBin** | Alternative a webhook.site | Gratuit |
| **Charles Proxy** | Intercepter les appels HTTP pour le debugging | Payant |
| **Histoires d'execution** | Logs natifs de chaque plateforme | Inclus |

### Methodologie de debugging

```
1. IDENTIFIER le probleme
   --> Quel est le code de statut HTTP retourne ?
   --> Quel est le message d'erreur dans le body de la reponse ?
   --> Le probleme est-il intermittent ou constant ?

2. REPRODUIRE en isolation
   --> Copier l'URL, les headers et le body de la requete echouee
   --> Rejouer dans Postman ou cURL
   --> Le meme resultat se produit-il ?

3. ANALYSER
   --> 401/403 : probleme d'authentification (token expire, permissions insuffisantes)
   --> 400/422 : probleme de format (champ manquant, type incorrect, valeur invalide)
   --> 404 : URL incorrecte ou ressource supprimee
   --> 429 : rate limit depasse (attendre et reessayer)
   --> 500/502/503 : probleme cote serveur (temporaire, reessayer)

4. CORRIGER
   --> Mettre a jour les credentials si expirees
   --> Corriger le format du body si invalide
   --> Ajouter du throttling si rate limited
   --> Contacter le support de l'API si erreur serveur persistante

5. PREVENIR
   --> Ajouter de la gestion d'erreurs au workflow
   --> Ajouter du monitoring sur les codes d'erreur
   --> Documenter le probleme et la solution pour reference future
```

### Commandes cURL utiles pour le debugging

```bash
# GET simple avec authentification
curl -X GET "https://api.example.com/v1/contacts" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"

# POST avec body JSON
curl -X POST "https://api.example.com/v1/contacts" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "name": "John"}'

# Voir les headers de reponse (rate limits, etc.)
curl -v -X GET "https://api.example.com/v1/contacts" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Tester un webhook en local
curl -X POST "http://localhost:5678/webhook/test" \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: your_secret" \
  -d '{"event": "test", "data": {"id": 123}}'
```

### Erreurs courantes et solutions

| Erreur | Cause probable | Solution |
|---|---|---|
| "Unauthorized" (401) | Token expire ou invalide | Renouveler le token, verifier les credentials |
| "Forbidden" (403) | Permissions insuffisantes | Verifier les scopes OAuth, les roles de l'API key |
| "Not Found" (404) | URL incorrecte ou ressource supprimee | Verifier l'URL, l'ID de la ressource, la version de l'API |
| "Validation Error" (422) | Champ manquant ou format incorrect | Lire le detail de l'erreur, verifier les champs obligatoires |
| "Rate Limited" (429) | Trop de requetes | Ajouter un delai, utiliser le batching, lire Retry-After |
| "Timeout" | L'API ne repond pas dans le delai | Augmenter le timeout, verifier la connectivite, reessayer |
| "CORS Error" | Appel depuis un navigateur non autorise | Ne pas appeler les API depuis le frontend, utiliser un backend |
| "SSL Error" | Certificat invalide ou expire | Verifier le certificat du serveur, mettre a jour les CA |
| "JSON Parse Error" | La reponse n'est pas du JSON valide | Verifier le Content-Type de la reponse, le body peut etre du HTML (page d'erreur) |
