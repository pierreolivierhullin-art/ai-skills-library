# Design Patterns de Workflows — Architecture, Fiabilite, Scalabilite & Gouvernance

## Overview

Ce document de reference couvre les design patterns fondamentaux et avances pour la conception de workflows automatises. Il fournit les bases architecturales, les patterns de fiabilite (gestion d'erreurs, idempotence, retry), les strategies de test et de monitoring, ainsi que les pratiques de gouvernance necessaires pour maintenir un portefeuille d'automatisations sain et scalable. Ces patterns sont agnostiques de la plateforme — ils s'appliquent a N8N, Power Automate, Zapier, Make et toute autre solution d'orchestration.

---

## 1. Patterns d'Architecture de Workflows

### Pattern 1 — Sequentiel (Pipeline)

Le pattern le plus simple : les actions s'executent dans un ordre strict, chaque etape recevant les donnees de l'etape precedente.

```
Trigger --> Etape 1 --> Etape 2 --> Etape 3 --> Fin
```

**Quand l'utiliser** :
- Processus lineaires sans branchement
- Chaque etape depend du resultat de la precedente
- Nombre d'etapes limite (< 10)

**Forces** : simple a comprendre, facile a debugger, flux de donnees previsible.
**Faiblesses** : un echec bloque tout le workflow, pas de parallelisme, temps d'execution cumule.

**Exemples** : envoi d'email de confirmation apres inscription, creation de facture apres commande, notification Slack apres deploiement.

### Pattern 2 — Parallele (Fan-out)

Plusieurs actions s'executent simultanement a partir d'un point de divergence.

```
Trigger --> Etape 1
        |-> Etape 2
        |-> Etape 3
        --> (toutes completees) --> Fin
```

**Quand l'utiliser** :
- Actions independantes pouvant s'executer en parallele
- Besoin de reduire le temps d'execution total
- Notifications multi-canal (email + Slack + SMS simultanement)

**Forces** : temps d'execution optimal, independance entre branches.
**Faiblesses** : synchronisation necessaire si un resultat agrege est attendu, complexite de gestion d'erreurs (que faire si 2 branches sur 3 echouent).

**Regles** :
1. Chaque branche parallele doit etre independante (pas de dependances croisees)
2. Definir la strategie en cas d'echec partiel : tout ou rien, best effort, compensation
3. Si un resultat agrege est necessaire, utiliser un point de synchronisation (fan-in / merge)

### Pattern 3 — Branching (Conditionnel)

Le flux se divise selon des conditions, chaque branche executant un traitement different.

```
Trigger --> Condition ?
            +-- Condition A vraie --> Traitement A
            +-- Condition B vraie --> Traitement B
            +-- Sinon (default)   --> Traitement par defaut
```

**Quand l'utiliser** :
- Routage selon le type d'evenement, le montant, le statut, la source
- Traitement differentie selon les criteres metier
- Remplacement de plusieurs workflows simples par un seul workflow avec branches

**Forces** : logique centralisee, maintenance plus facile qu'avec des workflows separes.
**Faiblesses** : complexite croissante avec le nombre de branches, difficulte de test (chaque branche doit etre testee).

**Regles** :
1. Toujours inclure une branche "default" pour les cas non prevus
2. Limiter a 5-7 branches maximum — au-dela, decomposer en sub-workflows
3. Documenter les conditions de chaque branche avec des exemples
4. Logger la branche empruntee pour faciliter le debugging

### Pattern 4 — Boucle (Iterator)

Le workflow itere sur une collection d'elements, appliquant le meme traitement a chacun.

```
Trigger --> Recuperer la liste
        --> Pour chaque element :
            --> Traitement unitaire
            --> (optionnel) Aggregation des resultats
        --> Rapport final
```

**Quand l'utiliser** :
- Traitement d'une liste de contacts, de commandes, de fichiers
- Import ou export de donnees en lots
- Application d'une mise a jour a tous les elements d'une collection

**Forces** : traitement uniforme et previsible, progres mesurable.
**Faiblesses** : temps d'execution proportionnel au nombre d'elements, consommation de tasks/operations, risque de timeout ou de rate limiting.

**Regles** :
1. Implementer du batching (traiter par lots de 50-100 plutot qu'un par un)
2. Gerer les erreurs par element (ne pas arreter tout le lot pour une erreur unitaire)
3. Logger le progres (element X sur Y traite) pour le monitoring
4. Prevoir un mecanisme de reprise en cas d'interruption (checkpoint)
5. Respecter les rate limits des API (ajouter des delais entre les appels si necessaire)

### Pattern 5 — Saga (Transaction distribuee)

Le workflow execute une sequence d'actions avec compensation en cas d'echec. Si une etape echoue, les etapes precedentes sont annulees dans l'ordre inverse.

```
Trigger --> Action 1 (+ compensation 1)
        --> Action 2 (+ compensation 2)
        --> Action 3 (+ compensation 3)

En cas d'echec a l'etape 3 :
        --> Compensation 2 (annuler action 2)
        --> Compensation 1 (annuler action 1)
        --> Notification d'echec
```

**Quand l'utiliser** :
- Operations multi-systemes ou la coherence est critique
- Processus ou un echec partiel est pire que pas d'execution du tout
- Transactions impliquant des paiements, des creations de comptes, des reservations

**Forces** : coherence des donnees, rollback automatique, audit trail complet.
**Faiblesses** : complexite elevee, chaque action doit avoir une compensation, temps d'implementation significatif.

**Exemple concret — Onboarding employe** :
```
1. Creer compte email (compensation : supprimer compte email)
2. Creer compte Slack (compensation : desactiver compte Slack)
3. Attribuer licence logiciel (compensation : revoquer licence)
4. Creer dans le SIRH (compensation : supprimer du SIRH)

Si l'etape 3 echoue :
  --> Desactiver compte Slack
  --> Supprimer compte email
  --> Notifier RH de l'echec
```

### Pattern 6 — Event-Driven (Pub/Sub)

Les workflows sont declenches par des evenements publies sur un bus. Les producteurs et les consommateurs sont decoules.

```
Producteur --> Event Bus --> Consommateur 1 (workflow A)
                         --> Consommateur 2 (workflow B)
                         --> Consommateur 3 (workflow C)
```

**Quand l'utiliser** :
- Architecture a grande echelle avec de nombreux workflows interdependants
- Besoin de decouplage fort entre les systemes
- Ajout frequents de nouveaux traitements pour les memes evenements

**Forces** : decouplage maximal, scalabilite, ajout de consommateurs sans modifier le producteur.
**Faiblesses** : complexite d'infrastructure, difficulte de tracabilite end-to-end, eventual consistency.

**Implementation dans les plateformes no-code** :
- Utiliser un webhook central comme "event bus" leger
- Le producteur POST l'evenement au webhook
- Le webhook declenche le workflow consommateur
- Pour le fan-out, utiliser un workflow "dispatcher" qui appelle plusieurs webhooks

---

## 2. Types de Triggers

### Webhook (temps reel)

- **Fonctionnement** : le systeme source envoie un HTTP POST au workflow quand l'evenement se produit
- **Latence** : quasi-instantanee (secondes)
- **Avantages** : temps reel, pas de consommation de resources entre les evenements, efficace
- **Inconvenients** : necessite que le systeme source supporte les webhooks, risque de perte si le recepteur est indisponible, pas de replay natif

**Securisation des webhooks** :
1. Valider la signature HMAC (le systeme source signe le payload avec un secret partage)
2. Verifier les headers d'authentification (Bearer token, API key)
3. Restreindre les IP sources quand possible
4. Valider le format du payload avant traitement
5. Repondre rapidement (< 5s) pour eviter les timeouts et les re-deliveries

### Polling (interrogation periodique)

- **Fonctionnement** : le workflow interroge l'API source a intervalles reguliers pour detecter les nouveaux elements
- **Latence** : depend de la frequence (1 min a 15 min selon la plateforme)
- **Avantages** : fonctionne avec toute API (pas besoin de webhooks), aucune configuration cote source
- **Inconvenients** : latence, consommation de ressources meme sans nouveaux evenements, risque de doublons

**Bonnes pratiques pour le polling** :
1. Stocker le dernier element traite (ID, timestamp) pour la deduplication
2. Utiliser des filtres cote API pour ne recuperer que les nouveaux elements (parametre `created_after`, `updated_since`)
3. Adapter la frequence au besoin reel (pas besoin de polling toutes les minutes pour un rapport hebdomadaire)
4. Gerer les cas de pagination (l'API peut retourner plus d'elements que prevu)

### Schedule (planifie)

- **Fonctionnement** : le workflow s'execute a des heures/jours fixes, type cron
- **Latence** : predeterminee par la configuration
- **Avantages** : previsible, adapte aux traitements batch, pas de dependance externe
- **Inconvenients** : pas temps reel, execution meme si pas de donnees a traiter

**Cas d'usage** : rapports quotidiens, synchronisations nocturnes, nettoyage periodique, relances automatiques.

### Event (evenement systeme)

- **Fonctionnement** : le workflow se declenche sur un evenement interne de la plateforme ou du systeme
- **Exemples** : nouveau fichier dans un dossier, modification d'une ligne dans un spreadsheet, email recu, message Teams
- **Avantages** : integration native, pas de configuration complexe
- **Inconvenients** : limite aux evenements supportes par la plateforme

---

## 3. Patterns de Gestion d'Erreurs

### Retry avec Backoff Exponentiel

En cas d'echec d'un appel (timeout, erreur serveur 5xx, rate limiting 429), reessayer avec des delais croissants :

```
Tentative 1 : immediate
  --> Echec --> Attendre 1 seconde
Tentative 2 :
  --> Echec --> Attendre 2 secondes
Tentative 3 :
  --> Echec --> Attendre 4 secondes
Tentative 4 :
  --> Echec --> Attendre 8 secondes
Tentative 5 (derniere) :
  --> Echec --> Notifier + stocker pour retraitement manuel
```

**Regles** :
1. Limiter le nombre de retries (3-5 tentatives maximum)
2. Ajouter du jitter (variation aleatoire) au delai pour eviter les thundering herds
3. Ne retrier que les erreurs transitoires (5xx, timeout, 429). Ne jamais retrier les erreurs 4xx (sauf 429).
4. Logger chaque retry pour le monitoring

### Dead Letter Queue (DLQ)

Les elements qui echouent apres tous les retries sont places dans une file d'attente dediee pour retraitement ulterieur :

```
Workflow principal
  --> Traitement de l'element
  --> En cas d'echec apres retries :
      --> Stocker dans la DLQ (table, data store, spreadsheet)
      --> Notifier l'equipe

Workflow de retraitement (quotidien ou manuel)
  --> Lire les elements de la DLQ
  --> Retenter le traitement
  --> Si succes : supprimer de la DLQ
  --> Si echec : incrementer le compteur d'echecs
  --> Si compteur > seuil : escalade manuelle
```

**Implementation** :
- **Zapier** : utiliser Zapier Tables comme DLQ
- **Make** : utiliser un Data Store comme DLQ
- **N8N** : utiliser une table PostgreSQL ou un Google Sheet comme DLQ
- **Power Automate** : utiliser une liste SharePoint ou une table Dataverse comme DLQ

### Circuit Breaker

Si un service externe echoue de maniere repetee, arreter temporairement les appels pour eviter la surcharge et les echecs en cascade :

```
Etat FERME (normal)
  --> Appels normaux vers le service
  --> Si X echecs consecutifs : passer en OUVERT

Etat OUVERT (arret)
  --> Tous les appels sont ignores ou rediriges vers un fallback
  --> Apres un delai (ex: 5 minutes) : passer en SEMI-OUVERT

Etat SEMI-OUVERT (test)
  --> Autoriser 1 appel test
  --> Si succes : repasser en FERME
  --> Si echec : repasser en OUVERT
```

**Implementation dans les plateformes no-code** :
1. Stocker l'etat du circuit breaker dans un data store (etat, compteur d'echecs, timestamp du dernier echec)
2. Avant chaque appel, verifier l'etat du circuit breaker
3. Apres chaque appel, mettre a jour le compteur
4. Utiliser un workflow schedule pour tester periodiquement les circuits ouverts

### Fallback (degradation gracieuse)

Quand le traitement principal echoue, executer un traitement alternatif degrade :

```
Tentative principale : envoyer via API Slack
  --> Echec :
      Fallback 1 : envoyer par email
      --> Echec :
          Fallback 2 : stocker dans un log pour envoi ulterieur
```

**Regles** :
1. Le fallback doit etre plus simple et plus fiable que le traitement principal
2. Notifier qu'un fallback a ete utilise (pour investigation)
3. Revenir automatiquement au traitement principal quand le service est retabli
4. Ne pas enchainer trop de niveaux de fallback (2-3 maximum)

---

## 4. Patterns de Transformation de Donnees

### Mapping de champs

Correspondance entre les champs du systeme source et du systeme cible :

```
Source (CRM)          -->  Cible (Facturation)
---                        ---
contact.first_name    -->  customer.prenom
contact.last_name     -->  customer.nom
contact.email         -->  customer.email_principal
contact.company       -->  customer.societe
deal.amount           -->  invoice.montant_ht
deal.currency         -->  invoice.devise
```

**Regles** :
1. Documenter le mapping dans un tableau avant de l'implementer
2. Gerer les champs optionnels (valeur par defaut si absent)
3. Valider les types de donnees (nombre vs chaine, format de date)
4. Gerer les champs calcules (TVA = montant_HT x taux_TVA)

### Normalisation des donnees

Standardiser les formats de donnees entre systemes :

| Type | Source (variable) | Cible (normalise) | Transformation |
|---|---|---|---|
| **Telephone** | "+33 6 12 34 56 78", "06.12.34.56.78" | "+33612345678" | Supprimer espaces/points, ajouter prefixe |
| **Email** | "John.DOE@Example.COM" | "john.doe@example.com" | Mettre en minuscules |
| **Date** | "12/31/2025", "31-12-2025" | "2025-12-31T00:00:00Z" | Convertir en ISO 8601 |
| **Devise** | "1,234.56", "1 234,56" | 1234.56 | Convertir en nombre flottant |
| **Pays** | "France", "FR", "FRA" | "FR" | Convertir en code ISO 3166-1 alpha-2 |

### Enrichissement de donnees

Augmenter les donnees source avec des informations complementaires provenant de services tiers :

```
Donnees source (email)
  --> Enrichissement 1 : recherche dans le CRM (client existant ?)
  --> Enrichissement 2 : API Clearbit (informations entreprise)
  --> Enrichissement 3 : API Hunter (validation email)
  --> Donnees enrichies (email + nom + entreprise + validation + historique client)
```

### Agregation de donnees

Combiner des donnees de sources multiples en une vue unifiee :

```
Source 1 : CRM (contacts et deals)
Source 2 : Facturation (factures et paiements)
Source 3 : Support (tickets et satisfaction)
  --> Merge par cle commune (email ou ID client)
  --> Calcul des metriques agregees (CA total, nombre de tickets, NPS)
  --> Resultat : vue client 360 degres
```

---

## 5. Patterns d'Idempotence

### Pourquoi l'idempotence est critique

Les webhooks peuvent etre delivres plusieurs fois. Les workflows peuvent etre relances apres un echec. Les schedules peuvent se chevaucher. Sans idempotence, ces situations creent des doublons, des actions repetees et des incoherences.

### Pattern 1 — Deduplication par ID unique

```
Recevoir l'evenement
  --> Extraire l'ID unique (event_id, order_id, transaction_id)
  --> Verifier dans le data store : cet ID a-t-il deja ete traite ?
      +-- Oui : ignorer (deja traite)
      +-- Non : traiter + stocker l'ID dans le data store
```

### Pattern 2 — Upsert au lieu d'Insert

Utiliser des operations "upsert" (update if exists, insert if not) plutot que des "insert" aveugles :

```
Au lieu de :
  --> Creer un contact dans le CRM (risque de doublon)

Faire :
  --> Rechercher le contact par email dans le CRM
      +-- Existe : mettre a jour les champs modifies
      +-- N'existe pas : creer le contact
```

### Pattern 3 — Idempotency Key

Generer une cle d'idempotence a partir des donnees d'entree et l'envoyer avec chaque requete :

```
Idempotency key = hash(order_id + timestamp + action)
  --> Envoyer la requete avec le header "Idempotency-Key: {key}"
  --> L'API cible ignore les requetes avec une cle deja traitee
```

Stripe, PayPal et de nombreuses API financieres supportent nativement les cles d'idempotence.

### Pattern 4 — Check-before-Act

Verifier l'etat actuel avant d'agir :

```
Avant d'envoyer un email de relance :
  --> Verifier que l'email de relance n'a pas deja ete envoye (flag dans le CRM)
  --> Verifier que le client n'a pas paye entre-temps
  --> Si toutes les conditions sont remplies : envoyer l'email + mettre le flag
```

---

## 6. Testing de Workflows

### Niveaux de test

| Niveau | Description | Comment |
|---|---|---|
| **Test unitaire de node** | Tester chaque node/module independamment | Execution manuelle avec donnees mockees |
| **Test d'integration** | Tester le workflow complet avec des API de test | Utiliser des sandboxes et des API de test |
| **Test de bout en bout** | Tester le workflow avec des donnees reelles | Execution en environnement de pre-production |
| **Test de charge** | Verifier le comportement sous volume | Envoyer N webhooks et verifier les resultats |
| **Test de resilience** | Verifier la gestion d'erreurs | Simuler des echecs (API down, timeout, payload invalide) |

### Checklist de test

```
[ ] Cas nominal : le workflow fonctionne avec des donnees valides
[ ] Donnees vides : champs optionnels manquants, tableaux vides
[ ] Donnees invalides : format incorrect, types incompatibles
[ ] Doublons : le meme evenement est declenche 2 fois
[ ] Grand volume : 100+ elements a traiter dans une boucle
[ ] Echec API : le service externe est indisponible
[ ] Rate limiting : l'API retourne un 429
[ ] Timeout : une etape prend plus de temps que prevu
[ ] Payload volumineux : fichiers > 1 Mo, tableaux > 1000 elements
[ ] Permissions : les credentials ont les droits suffisants
[ ] Concurrence : 2 executions simultanees du meme workflow
[ ] Recovery : le workflow reprend correctement apres une interruption
```

### Environnements de test

**Strategie recommandee** :

1. **Sandbox/Dev** : utiliser les environnements sandbox des API (Stripe test mode, HubSpot sandbox, Salesforce sandbox)
2. **Donnees de test** : creer un jeu de donnees de test representatif (nominaux + cas limites)
3. **Isolation** : les workflows de test ne doivent jamais affecter les donnees de production
4. **Reproduction des erreurs** : utiliser des services comme webhook.site ou RequestBin pour capturer et rejouer les payloads

---

## 7. Monitoring et Alerting

### Metriques essentielles

| Metrique | Description | Seuil d'alerte |
|---|---|---|
| **Taux de succes** | % d'executions reussies | < 95% |
| **Taux d'echec** | % d'executions en erreur | > 5% |
| **Duree moyenne** | Temps moyen d'execution | > 2x la duree normale |
| **Executions/periode** | Nombre d'executions par heure/jour | Ecart > 50% vs moyenne |
| **Queue depth** | Nombre d'executions en attente | > 100 elements |
| **Latence webhook** | Temps entre reception et traitement | > 30 secondes |
| **Taux de retry** | % d'actions necessitant un retry | > 10% |

### Architecture de monitoring

```
Workflows en production
  --> Logger chaque execution (ID, statut, duree, donnees cles)
  --> Agreger dans un dashboard (Google Sheets, Notion, DataDog, Grafana)
  --> Alertes automatiques :
      --> Echec : notification Slack immediate
      --> Degradation : email quotidien si taux de succes < 95%
      --> Absence : alerte si le workflow ne s'execute pas depuis X heures
```

### Pattern "Heartbeat Monitor"

Surveiller que les workflows attendus s'executent bien :

```
Workflow monitore (schedule quotidien)
  --> A la fin de l'execution : envoyer un "heartbeat" (webhook ou mise a jour)

Workflow sentinelle (schedule toutes les 2 heures)
  --> Verifier le timestamp du dernier heartbeat
  --> Si > 26 heures : alerter (le workflow quotidien n'a pas tourne)
```

### Centralisation des logs

Quelque soit la plateforme, centraliser les logs dans un outil unique :

- **Google Sheets** : simple, adapte pour < 50 workflows. Une ligne par execution avec timestamp, workflow, statut, duree, message.
- **Notion** : database Notion comme journal d'execution. Filtres et vues pour le suivi.
- **Airtable** : entre Google Sheets et une vraie base de donnees. Bon pour 50-200 workflows.
- **Datadog / Grafana** : pour les organisations matures avec 200+ workflows. Dashboards, alertes, correlations.

---

## 8. Documentation et Versioning

### Documentation d'un workflow

Chaque workflow en production doit avoir une fiche descriptive :

```
=== FICHE WORKFLOW ===
ID : WF-2025-042
Nom : [Sales] HubSpot -> Slack - New deal notification
Owner : equipe.commerciale@exemple.com
Plateforme : Make
Criticite : Haute

OBJECTIF :
Notifier l'equipe commerciale dans Slack quand un nouveau deal est
cree dans HubSpot avec un montant superieur a 10 000 EUR.

TRIGGER :
HubSpot webhook - Deal created

ETAPES :
1. Recevoir le webhook HubSpot (validation signature)
2. Filtrer : montant >= 10 000 EUR
3. Enrichir avec les donnees du contact associe
4. Formater le message Slack avec les details du deal
5. Poster dans #sales-notifications

GESTION D'ERREURS :
- Echec API HubSpot : retry x3 avec backoff
- Echec Slack : fallback email au responsable commercial
- Echec general : notification dans #automation-errors

DEPENDANCES :
- HubSpot (API key : credential store ref #HC-001)
- Slack (OAuth : credential store ref #SC-003)

METRIQUES :
- Executions/jour : ~15
- Taux de succes : 99.8%
- Duree moyenne : 3 secondes

HISTORIQUE :
- 2025-01 : creation initiale
- 2025-03 : ajout du filtre montant > 10k
- 2025-06 : ajout enrichissement contact
- 2025-09 : ajout fallback email
```

### Versioning des workflows

Les plateformes no-code ne proposent generalement pas de versioning natif robuste. Strategies de contournement :

1. **Export JSON periodique** : exporter les workflows au format JSON et les versionner dans Git. Automatiser l'export avec un workflow schedule.

2. **Naming convention avec version** : inclure un numero de version dans le nom du workflow.
   ```
   [Sales] HubSpot -> Slack - Deal notification (v2.3)
   ```

3. **Changelog** : maintenir un changelog dans la documentation du workflow (qui a change quoi, quand, pourquoi).

4. **Workflow de deploiement** : dans les environnements critiques, utiliser un workflow CI/CD pour le deploiement des automatisations (export, test, promotion dev -> staging -> production).

### Naming Conventions

Adopter des conventions coherentes dans toute l'organisation :

**Format recommande** :
```
[Domaine] Source -> Destination - Action (vX.Y)
```

**Exemples** :
```
[Sales] HubSpot -> Slack - New deal notification (v2.1)
[HR] BambooHR -> Google Workspace - Employee onboarding (v1.3)
[Finance] Stripe -> QuickBooks - Invoice sync (v3.0)
[Support] Zendesk -> Notion - Ticket summary (v1.0)
[Marketing] Typeform -> HubSpot - Lead capture (v2.0)
[Ops] Schedule -> Slack - Daily report (v1.5)
```

**Structure de dossiers/tags** :
```
/automations
  /sales
  /marketing
  /hr
  /finance
  /operations
  /support
  /internal-tools
  /monitoring
```

---

## 9. Gouvernance

### Matrice RACI pour l'automatisation

| Activite | Automation Owner | Business User | IT / Admin | Management |
|---|---|---|---|---|
| Identifier les opportunites | C | R | I | I |
| Concevoir le workflow | R | C | C | I |
| Implementer | R | I | C | I |
| Tester | R | A | C | I |
| Deployer en production | R | I | A | I |
| Monitorer | R | I | C | I |
| Maintenir les credentials | C | I | R | I |
| Auditer la securite | I | I | R | A |
| Mesurer le ROI | R | C | I | A |

R = Responsable, A = Approbateur, C = Consulte, I = Informe

### Politique de revue

| Cadence | Revue | Contenu |
|---|---|---|
| **Continue** | Monitoring des echecs | Dashboard, alertes, correction immediate |
| **Mensuelle** | Revue de performance | Metriques, optimisations, nouveaux besoins |
| **Trimestrielle** | Audit de securite | Credentials, permissions, DLP compliance |
| **Trimestrielle** | Revue de pertinence | Workflows obsoletes, doublons, rationalisation |
| **Annuelle** | Revue strategique | ROI global, maturite, feuille de route, budget |

### Gestion du cycle de vie

```
Etat du workflow :
  DRAFT --> TESTING --> ACTIVE --> DEPRECATED --> ARCHIVED

DRAFT : en cours de conception, pas encore operationnel
TESTING : en cours de test, pas de donnees de production
ACTIVE : en production, monitore et maintenu
DEPRECATED : toujours actif mais en cours de remplacement, ne plus modifier
ARCHIVED : desactive, conserve pour reference
```

**Regles de cycle de vie** :
1. Tout workflow doit passer par TESTING avant ACTIVE
2. Un workflow sans owner passe en DEPRECATED automatiquement
3. Un workflow en erreur > 30 jours sans action passe en DEPRECATED
4. Les workflows ARCHIVED sont conserves 1 an puis supprimes

---

## 10. Patterns de Securite

### Gestion des secrets

| Methode | Securite | Plateformes |
|---|---|---|
| **Credential store natif** | Elevee | N8N, Zapier, Make, Power Automate |
| **Variables d'environnement** | Moyenne | N8N (self-hosted) |
| **Secrets manager externe** | Tres elevee | HashiCorp Vault, AWS Secrets Manager |
| **Hardcode dans le workflow** | Inacceptable | Jamais |

**Regles** :
1. Utiliser systematiquement le credential store natif de la plateforme
2. Ne jamais hardcoder des secrets dans les configurations, les expressions ou les Code Nodes
3. Utiliser des comptes de service dedies (pas de comptes personnels)
4. Rotation des credentials tous les 90 jours minimum
5. Audit des acces et des permissions trimestriel

### OAuth 2.0 dans les workflows

La plupart des plateformes gerent OAuth 2.0 nativement. Points d'attention :

1. **Refresh tokens** : la plateforme doit renouveler automatiquement les tokens expires
2. **Scopes minimaux** : ne demander que les permissions necessaires lors de la configuration
3. **Revocation** : prevoir un processus de revocation rapide en cas de compromission
4. **Multi-tenant** : si le workflow sert plusieurs clients, utiliser une connexion par tenant

### Data Loss Prevention (DLP)

Prevenir la fuite de donnees sensibles via les workflows :

1. **Classification** : identifier les workflows qui manipulent des donnees sensibles (PII, donnees financieres, donnees de sante)
2. **Restriction** : empecher les workflows sensibles d'envoyer des donnees vers des services non approuves
3. **Masquage** : masquer les donnees sensibles dans les logs et les notifications (email partiel, numero de carte tronque)
4. **Audit** : tracer tous les acces aux donnees sensibles via les workflows
5. **Chiffrement** : chiffrer les donnees en transit (HTTPS obligatoire) et au repos (credential store chiffre)

### Isolation et moindre privilege

```
Principe : chaque workflow n'accede qu'aux donnees et actions
strictement necessaires a son fonctionnement.

Exemples :
- Un workflow de notification n'a pas besoin d'acces en ecriture au CRM
- Un workflow de reporting n'a pas besoin d'acces aux donnees individuelles
- Un workflow de synchronisation n'a pas besoin d'acces a la suppression

Implementation :
- Creer des API keys scoped (read-only, write-only, scope par objet)
- Utiliser des comptes de service avec des roles granulaires
- Segmenter les workflows par niveau de sensibilite des donnees
```
