# Zapier & Make (Integromat) — Zaps, Scenarios, Integration Patterns & Best Practices

## Overview

Ce document de reference couvre en profondeur les deux plateformes d'automatisation cloud les plus populaires pour les PME, les equipes marketing et les citizen developers : Zapier (leader en nombre d'integrations, simplicite d'usage) et Make, anciennement Integromat (puissance visuelle, flexibilite des scenarios). Il inclut egalement IFTTT pour les automatisations simples et personnelles. Ce guide fournit les patterns de conception, les strategies d'optimisation des couts et les bonnes pratiques pour tirer le meilleur parti de chaque plateforme.

---

## 1. Zapier — Architecture et Concepts Fondamentaux

### Le modele Zap

Un Zap est l'unite fondamentale d'automatisation dans Zapier. Chaque Zap se compose de :

- **Trigger** : l'evenement declencheur. Un seul trigger par Zap. Types :
  - **Instant (webhook)** : declenchement en temps reel quand l'evenement se produit (la plupart des triggers modernes)
  - **Polling** : Zapier interroge l'application toutes les 1-15 minutes selon le plan (Free : 15 min, Premium : 1 min)
  - **Schedule** : declenchement a intervalles reguliers (toutes les heures, tous les jours)

- **Actions** : les operations executees apres le trigger. Un Zap peut contenir plusieurs actions chainee (multi-step Zaps).

- **Filters** : conditions qui arretent l'execution du Zap si elles ne sont pas satisfaites. Les filters ne consomment pas de "task" quand ils arretent le flux.

- **Paths** : branches conditionnelles qui routent l'execution vers differents chemins selon des conditions (equivalent d'un IF/ELSE ou SWITCH). Chaque path peut contenir plusieurs actions.

### Tasks et modele de facturation

La facturation de Zapier repose sur les "tasks". Une task correspond a une action executee avec succes. Le trigger et les filters ne comptent pas comme des tasks.

**Exemple de comptage** :
```
Trigger : Nouveau email (0 task)
  --> Filter : sujet contient "commande" (0 task)
  --> Action 1 : Creer une ligne Google Sheets (1 task)
  --> Action 2 : Envoyer notification Slack (1 task)
  --> Action 3 : Mettre a jour HubSpot (1 task)
= 3 tasks par execution
```

**Optimisation des tasks** :
- Utiliser des Filters en amont pour eviter les executions inutiles
- Combiner les actions quand possible (un seul appel API au lieu de plusieurs)
- Utiliser Looping by Zapier avec parcimonie (chaque iteration consomme des tasks)
- Deplacer les traitements volumineux vers des webhooks personnalises ou des Functions

### Architecture multi-step avancee

Zapier supporte des workflows multi-step avec les elements suivants :

| Element | Description | Cas d'usage |
|---|---|---|
| **Multi-step** | Chainer plusieurs actions en sequence | Pipeline de traitement lineaire |
| **Paths** | Branching conditionnel (A/B/C) | Routage selon le type, le montant, le statut |
| **Filters** | Arret conditionnel du Zap | Ne traiter que certains evenements |
| **Formatter** | Transformation de donnees inline | Formatage de dates, textes, nombres |
| **Delay** | Attente programmee | Envoyer un follow-up apres 3 jours |
| **Looping** | Iteration sur une liste | Traiter chaque ligne d'un tableau |
| **Sub-Zap** | Appel d'un autre Zap (via webhook) | Modularisation et reutilisation |

### Zapier Tables

Zapier Tables est une base de donnees legere integree a Zapier, permettant de stocker et gerer des donnees directement dans la plateforme :

- **Stockage structure** : tables avec colonnes typees (texte, nombre, date, lien, email)
- **CRUD natif** : actions Zapier pour creer, lire, mettre a jour et supprimer des enregistrements
- **Deduplication** : utiliser une colonne unique comme cle pour eviter les doublons
- **Etat et suivi** : stocker l'etat d'avancement d'un processus multi-etapes
- **Cache et lookup** : utiliser comme cache pour les donnees frequemment consultees

**Cas d'usage Tables** :
- Pipeline de leads avec suivi du statut
- Inventaire de workflows avec leur etat de sante
- Registry des contacts traites pour deduplication
- Configuration dynamique des workflows (parametres modifiables sans editer le Zap)

### Zapier Interfaces

Zapier Interfaces permet de creer des interfaces web simples connectees aux Zaps :

- **Formulaires** : collecte de donnees avec validation et declenchement de Zaps
- **Pages** : affichage de donnees issues de Zapier Tables
- **Kanban** : vue kanban pour le suivi de processus
- **Chatbot** : interface conversationnelle basee sur l'IA pour les interactions utilisateurs

### Zapier Central

Zapier Central (2025-2026) est la nouvelle generation d'automatisation de Zapier, basee sur des agents IA :

- **Bots** : agents autonomes qui peuvent observer des evenements, raisonner et agir
- **Natural Language** : creation de bots par description en langage naturel
- **Multi-app** : un bot peut interagir avec plusieurs applications simultanement
- **Behaviors** : regles definies en langage naturel ("Quand je recois un email de facturation, extrais le montant et cree une ligne dans le spreadsheet")
- **Knowledge** : les bots peuvent acceder a une base de connaissances pour contextualiser leurs actions

---

## 2. Make (Integromat) — Scenarios et Modules

### Le modele Scenario

Make utilise une approche visuelle basee sur des "scenarios" — des diagrammes visuels ou les modules (nodes) sont connectes par des liens de donnees :

- **Modules** : les briques de base. Chaque module represente une action dans une application specifique. Types :
  - **Trigger modules** : declenchent le scenario (webhook, polling, schedule)
  - **Action modules** : executent des operations (CRUD, envoi, mise a jour)
  - **Search modules** : recherchent des donnees dans une application
  - **Aggregator modules** : combinent plusieurs elements en un seul
  - **Iterator modules** : decomposent un tableau en elements individuels
  - **Transformer modules** : modifient le format ou la structure des donnees

- **Routes (Routers)** : permettent de creer des branches paralleles ou conditionnelles dans le scenario. Chaque route peut avoir un filtre conditionnel.

- **Links** : connexions entre modules qui transportent les donnees (bundles). Un bundle est l'unite de donnees qui circule entre les modules.

### Data Mapping dans Make

Le systeme de mapping de Make est l'un de ses points forts, offrant une interface visuelle riche pour transformer les donnees :

**Acces aux donnees** :
- Clic sur un champ pour afficher les donnees disponibles depuis les modules precedents
- Drag-and-drop des variables depuis le panneau de mapping
- Utilisation de fonctions de transformation inline

**Fonctions de transformation** :

| Categorie | Fonctions | Exemple |
|---|---|---|
| **Texte** | `lower`, `upper`, `trim`, `replace`, `substring`, `split`, `join` | `{{lower(1.email)}}` |
| **Nombre** | `round`, `ceil`, `floor`, `abs`, `min`, `max`, `sum` | `{{round(1.amount; 2)}}` |
| **Date** | `formatDate`, `parseDate`, `addDays`, `addMonths`, `dateDifference` | `{{formatDate(1.created; "DD/MM/YYYY")}}` |
| **Tableau** | `length`, `first`, `last`, `slice`, `map`, `sort`, `distinct` | `{{length(1.items)}}` |
| **Logique** | `if`, `ifempty`, `switch`, `coalesce` | `{{if(1.status = "active"; "Oui"; "Non")}}` |
| **Encodage** | `base64`, `md5`, `sha1`, `encodeURL`, `decodeURL` | `{{encodeURL(1.name)}}` |

### Iterators et Aggregators

Make excelle dans le traitement de listes grace a ses modules Iterator et Aggregator :

**Iterator** :
- Decompose un tableau en elements individuels (bundles)
- Chaque element est traite independamment par les modules suivants
- Indispensable pour traiter les lignes d'un CSV, les contacts d'une liste, les items d'une commande

**Aggregator** :
- Recombine les bundles individuels en un seul bundle
- Types : Array Aggregator, Text Aggregator, Numeric Aggregator
- Permet de construire un resultat agrege apres traitement iteratif

**Exemple complet** :

```
HTTP Module (GET /api/orders)
  --> Iterator (decompose orders[])
      --> Pour chaque order :
          --> HTTP Module (GET /api/products/{product_id})
          --> Set Variable (calculer total_line = quantity * price)
      --> Array Aggregator (reagreger en un tableau)
  --> Google Sheets (ecrire le tableau agrege)
  --> Slack (notifier avec le nombre de commandes traitees)
```

### Data Stores

Les Data Stores de Make sont des bases de donnees cle-valeur integrees :

- **Stockage persistant** : jusqu'a 10 000 enregistrements (selon le plan)
- **Operations CRUD** : Get, Add, Update, Delete, Search
- **Cle unique** : chaque enregistrement a une cle unique pour la deduplication
- **Inter-scenario** : partageable entre plusieurs scenarios

**Cas d'usage** :
- Deduplication (stocker les IDs deja traites)
- Cache de donnees (eviter les appels API repetitifs)
- Etat persistant entre executions (compteurs, flags)
- Configuration dynamique des scenarios

### Gestion d'erreurs dans Make

Make propose un systeme de gestion d'erreurs sophistique :

- **Error Handler** : route speciale attachee a un module, qui s'active en cas d'erreur
- **Directives d'erreur** :
  - **Resume** : ignore l'erreur et continue avec une valeur par defaut
  - **Commit** : sauvegarde les resultats partiels et arrete le scenario
  - **Rollback** : annule toutes les operations et arrete le scenario
  - **Break** : stocke l'erreur dans la file "Incomplete executions" pour retraitement
  - **Ignore** : ignore l'erreur silencieusement (deconseille sauf cas specifiques)

**Pattern recommande** :

```
Module risque (ex: HTTP Request)
  |
  +--> Error Handler route
       --> Break directive (stocker pour retraitement)
       --> Slack notification (alerter l'equipe)
```

Les "Incomplete Executions" sont consultables dans l'interface Make et peuvent etre relancees manuellement ou automatiquement apres correction du probleme.

---

## 3. Comparaison Detaillee Zapier vs Make

### Forces et faiblesses

| Dimension | Zapier | Make (Integromat) |
|---|---|---|
| **Nombre d'integrations** | 7000+ apps | 1500+ modules |
| **Facilite d'usage** | Tres facile (lineaire, intuitif) | Moyen (visuel, plus de concepts) |
| **Flexibilite** | Moyenne (paths, filters) | Elevee (routers, iterators, aggregators) |
| **Transformation de donnees** | Limitee (Formatter, Code by Zapier) | Riche (fonctions natives, JSON/XML natif) |
| **Visualisation** | Lineaire (liste d'etapes) | Diagramme visuel (graphe de nodes) |
| **Traitement de listes** | Looping (basic) | Iterator + Aggregator (avance) |
| **Gestion d'erreurs** | Basique (retry, notification) | Avancee (handler, directives, incomplete executions) |
| **Stockage integre** | Zapier Tables (simple) | Data Stores (cle-valeur, plus technique) |
| **IA integree** | Zapier Central (agents IA) | AI modules (en developpement) |
| **API/Webhook** | Webhooks by Zapier + Code by Zapier | HTTP module natif + custom webhooks |
| **Prix (entree)** | ~20 USD/mois (750 tasks) | ~10 USD/mois (10 000 operations) |

### Modeles de facturation compares

**Zapier** — facturation par "tasks" :
- Free : 100 tasks/mois, 5 Zaps, single-step uniquement
- Starter (~20 USD/mois) : 750 tasks/mois, multi-step
- Professional (~50 USD/mois) : 2 000 tasks/mois, paths, custom logic
- Team (~70 USD/mois) : 2 000 tasks/mois, partage, permissions
- Enterprise : sur devis, SSO, admin controls

**Make** — facturation par "operations" :
- Free : 1 000 operations/mois, 2 scenarios actifs
- Core (~10 USD/mois) : 10 000 operations/mois, scenarios illimites
- Pro (~18 USD/mois) : 10 000 operations/mois, custom functions, priority execution
- Teams (~34 USD/mois) : 10 000 operations/mois, team features
- Enterprise : sur devis, SSO, audit logs

**Comparaison du cout reel** :

Le comptage differe entre les plateformes :
- Zapier : 1 task = 1 action executee avec succes
- Make : 1 operation = 1 module execute (triggers, actions et transformations comptent tous)

Pour un workflow de 5 etapes (1 trigger + 4 actions) execute 100 fois :
- Zapier : 400 tasks (4 actions x 100 executions)
- Make : 500 operations (5 modules x 100 executions)

En general, Make est plus economique pour les workflows complexes avec beaucoup de transformations, tandis que Zapier peut etre plus economique pour les workflows simples avec peu d'etapes.

### Strategies d'optimisation des couts

**Zapier** :
1. Utiliser des Filters en amont pour eviter les executions inutiles (0 task)
2. Combiner les actions : un seul HTTP Request au lieu de plusieurs actions separees
3. Utiliser les webhooks Zapier plutot que le polling pour un declenchement plus rapide
4. Regrouper les Zaps similaires avec Paths plutot que des Zaps separes
5. Utiliser Formatter au lieu de Code by Zapier quand possible (meme cout mais plus fiable)
6. Surveiller les Zaps a haut volume et optimiser les plus consommateurs

**Make** :
1. Utiliser des Filters apres le trigger pour stopper les executions inutiles
2. Privilegier les modules natifs aux HTTP Requests generiques (souvent plus optimises)
3. Utiliser l'Aggregator avant les envois pour reduire le nombre d'operations
4. Configurer le scheduling optimal (pas besoin de polling toutes les minutes si le traitement est hebdomadaire)
5. Utiliser les Data Stores comme cache pour eviter les appels API repetitifs
6. Combiner les routes pour traiter plusieurs cas dans un seul scenario

---

## 4. IFTTT — Automatisations Simples

### Positionnement

IFTTT (If This Then That) est la plateforme d'automatisation la plus simple, concue pour les utilisateurs non-techniques et les automatisations personnelles :

- **Applets** : l'unite d'automatisation. Un trigger, une action (version gratuite) ou plusieurs actions (Pro+).
- **Services** : 800+ services connectes, avec une force dans l'IoT (smart home, wearables) et les reseaux sociaux.
- **Simplicite** : configuration en quelques clics, pas de courbe d'apprentissage.

### Quand utiliser IFTTT

| Cas d'usage | Recommandation |
|---|---|
| Smart home et IoT | IFTTT est le leader (Philips Hue, Nest, Ring, etc.) |
| Automatisations personnelles simples | IFTTT est ideal (1 trigger, 1-3 actions) |
| Social media automation | IFTTT couvre bien les reseaux sociaux |
| Automatisations metier complexes | Utiliser Zapier ou Make |
| Transformation de donnees | Utiliser Make (beaucoup plus puissant) |
| Workflows multi-branches | Utiliser Zapier (paths) ou Make (routers) |

### Limites d'IFTTT

- Pas de conditions complexes ou de branches conditionnelles
- Pas de transformation de donnees (ou tres limitee)
- Pas de gestion d'erreurs structuree
- Delai d'execution variable (parfois plusieurs minutes)
- Nombre d'applets actives limite selon le plan
- Pas adapte aux automatisations metier critiques

---

## 5. Patterns Avances

### Webhook comme hub d'integration

Utiliser les webhooks comme point d'entree universel pour les automatisations :

**Pattern "Webhook Gateway"** :
```
Application source
  --> POST webhook URL (Zapier/Make)
      --> Validation du payload
      --> Routage par type d'evenement
          --> Route 1 : traitement A
          --> Route 2 : traitement B
          --> Route default : log + alerte
```

**Dans Zapier** :
- "Webhooks by Zapier" comme trigger (catch hook)
- Paths pour le routage conditionnel
- Custom Request pour les appels API sortants

**Dans Make** :
- "Custom Webhook" comme trigger
- Router pour le routage multi-branches
- HTTP module pour les appels API sortants
- Webhook Response pour renvoyer un resultat au systeme source

### Custom API Calls

Quand un connecteur natif ne couvre pas le besoin, utiliser les appels API personnalises :

**Zapier — Code by Zapier** :
```javascript
// Code by Zapier (JavaScript)
const response = await fetch('https://api.example.com/v1/contacts', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${inputData.api_key}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: inputData.email,
    name: inputData.name,
    source: 'zapier_automation'
  })
});

const data = await response.json();
output = [{ contact_id: data.id, status: data.status }];
```

**Make — HTTP Module** :
- URL : `https://api.example.com/v1/contacts`
- Method : POST
- Headers : `Authorization: Bearer {{1.api_key}}`
- Body type : JSON
- Request content : mapper les champs visuellement ou en JSON brut
- Parse response : activer pour exploiter les donnees de retour dans les modules suivants

### Synchronisation bidirectionnelle

Pattern pour maintenir la coherence entre deux systemes :

```
Scenario 1 : CRM -> ERP (declencheur = modification CRM)
  --> Trigger : Contact modifie dans CRM
  --> Check : le champ "last_synced_from" != "ERP" (eviter les boucles)
  --> Action : Mettre a jour dans ERP
  --> Action : Marquer dans CRM "last_synced_from" = "CRM"

Scenario 2 : ERP -> CRM (declencheur = modification ERP)
  --> Trigger : Contact modifie dans ERP
  --> Check : le champ "last_synced_from" != "CRM" (eviter les boucles)
  --> Action : Mettre a jour dans CRM
  --> Action : Marquer dans ERP "last_synced_from" = "ERP"
```

**Regles critiques pour la synchronisation bidirectionnelle** :
1. Toujours inclure un mecanisme anti-boucle (flag de source, timestamp de derniere sync)
2. Definir un systeme maitre en cas de conflit (quel systeme a la priorite)
3. Logger chaque synchronisation pour le debugging
4. Gerer les cas de suppression (soft delete, marqueur, synchroniser ou ignorer)
5. Tester avec des volumes reels avant la mise en production

### Traitement de fichiers

Pattern pour traiter les fichiers (CSV, Excel, PDF) dans les plateformes no-code :

**Zapier** :
```
Trigger : Nouveau fichier dans Google Drive
  --> Parser : convertir CSV en donnees structurees
  --> Looping : traiter chaque ligne
      --> Action : creer/mettre a jour dans CRM
  --> Notification : rapport de traitement
```

**Make** :
```
Trigger : Nouveau fichier dans Dropbox
  --> Download File module
  --> CSV Parser module (delimiter, headers)
  --> Iterator (chaque ligne)
      --> Router :
          --> Route 1 (si nouveau) : Creer dans CRM
          --> Route 2 (si existant) : Mettre a jour dans CRM
  --> Aggregator (compiler les resultats)
  --> Email module (rapport avec succes/erreurs)
```

### Orchestration multi-Zap / multi-scenario

Pour les automatisations complexes, decomposer en plusieurs Zaps/scenarios interconnectes :

**Pattern Hub-and-Spoke** :
```
Zap/Scenario principal (Hub)
  --> Recoit l'evenement declencheur
  --> Valide et enrichit les donnees
  --> Declenche les Zaps/scenarios enfants via webhook :
      --> Spoke 1 : Traitement CRM
      --> Spoke 2 : Facturation
      --> Spoke 3 : Notification
      --> Spoke 4 : Reporting
```

Avantages : modularite, testing independant, reutilisation, limites d'erreurs (un echec dans un spoke n'affecte pas les autres).

---

## 6. Templates et Cas d'Usage Courants

### Marketing Automation

**Lead capture et qualification** :
```
Typeform (nouveau formulaire soumis)
  --> Zapier/Make : enrichir avec Clearbit/Hunter
  --> Scorer le lead (criteres predefinies)
  --> Router :
      --> Score eleve : creer dans CRM + assigner au commercial + notification Slack
      --> Score moyen : ajouter a la sequence de nurturing (Mailchimp/ActiveCampaign)
      --> Score faible : ajouter a la newsletter
```

### Operations / IT

**Onboarding employe** :
```
BambooHR (nouvel employe)
  --> Creer compte Google Workspace
  --> Creer compte Slack + ajouter aux canaux
  --> Creer compte dans les outils (Jira, Notion, etc.)
  --> Envoyer email de bienvenue avec les acces
  --> Planifier les reunions d'onboarding (Google Calendar)
  --> Notifier le manager et l'equipe RH
```

### Finance

**Rapprochement et reporting** :
```
Schedule (chaque lundi 8h)
  --> Recuperer les transactions Stripe de la semaine
  --> Recuperer les factures QuickBooks
  --> Rapprocher par montant et date
  --> Generer un rapport de rapprochement
  --> Alerter si ecarts > seuil
  --> Envoyer le rapport au DAF par email
```

---

## 7. Migration entre Plateformes

### De Zapier vers Make

| Element Zapier | Equivalent Make | Notes |
|---|---|---|
| Zap | Scenario | 1:1 mapping |
| Trigger | Trigger module | Configurer les connexions Make |
| Action | Action module | Verifier les champs disponibles |
| Filter | Filter (apres module) | Syntaxe de conditions similaire |
| Path | Router | Plus flexible dans Make |
| Formatter | Fonctions de transformation | Syntaxe differente |
| Code by Zapier | Code module (JavaScript) | Migration directe possible |
| Zapier Tables | Data Store | Architecture differente |
| Delay | Sleep module | 1:1 mapping |
| Looping | Iterator | Plus puissant dans Make |

**Etapes de migration** :
1. Exporter la liste des Zaps actifs avec leurs configurations
2. Identifier les equivalents Make pour chaque connecteur
3. Reconstruire les scenarios dans Make en commencant par les plus simples
4. Tester chaque scenario avec des donnees reelles
5. Activer les scenarios Make et desactiver les Zaps Zapier en parallele pendant 2 semaines
6. Decommissionner les Zaps apres validation

### De Make vers Zapier

La migration dans ce sens peut impliquer des pertes de fonctionnalite si les scenarios Make utilisent des features avancees :
- Les Iterators + Aggregators doivent etre remplaces par Looping by Zapier (plus limite)
- Les Routers multi-branches deviennent des Paths (maximum 3 branches sans plan Enterprise)
- Les Data Stores n'ont pas d'equivalent direct (utiliser Zapier Tables ou un service externe)
- Les fonctions de transformation complexes necessitent Code by Zapier

### De IFTTT vers Zapier/Make

Migration generalement simple car les applets IFTTT sont des automatisations simples :
1. Lister les applets actives et leur logique
2. Recreer dans Zapier (si simplicite souhaitee) ou Make (si flexibilite necessaire)
3. Pour les applets IoT, verifier que le device est supporte dans la nouvelle plateforme

---

## 8. Securite et Bonnes Pratiques

### Gestion des connexions

- **Comptes de service** : utiliser des comptes de service dedies pour les connexions (pas de comptes personnels). Si un employe quitte, les automatisations continuent de fonctionner.
- **Permissions minimales** : configurer les connexions avec les permissions strictement necessaires (scopes OAuth minimaux).
- **Rotation des tokens** : planifier la rotation des API keys et tokens. Documenter les connexions utilisees par chaque Zap/scenario.
- **Audit periodique** : reviser les connexions actives trimestriellement et revoquer celles qui ne sont plus utilisees.

### Naming conventions

Adopter des conventions de nommage coherentes pour faciliter la maintenance :

```
Format : [Domaine] - [Source] -> [Destination] - [Action]

Exemples :
- [Sales] - HubSpot -> Slack - New deal notification
- [HR] - BambooHR -> Google Workspace - Employee onboarding
- [Finance] - Stripe -> QuickBooks - Invoice sync
- [Marketing] - Typeform -> HubSpot - Lead capture
```

### Documentation

Documenter chaque workflow avec :
1. **Objectif** : que fait ce workflow et pourquoi
2. **Owner** : qui est responsable de la maintenance
3. **Trigger** : quel evenement declenche le workflow
4. **Etapes** : description des actions dans l'ordre
5. **Gestion d'erreurs** : comment les erreurs sont gerees
6. **Dependances** : quels systemes sont concernes
7. **Frequence** : combien de fois le workflow s'execute
8. **Date de derniere revue** : quand le workflow a ete revu pour la derniere fois

### Monitoring et alertes

**Zapier** :
- Task History : historique des executions avec statut
- Error alerts : notification email en cas d'erreur
- Zapier Manager : vue centralisee de tous les Zaps et leur sante
- App Status : page de statut des connecteurs

**Make** :
- Scenario History : historique detaille avec donnees de chaque module
- Incomplete Executions : file d'attente des executions en erreur
- Notifications : email ou webhook sur erreurs
- Dashboard : vue d'ensemble des scenarios et de leur consommation

---

## 9. Tendances et Evolution (2025-2026)

### Zapier

- **Zapier Central** : plateforme d'agents IA autonomes qui observent, raisonnent et agissent. Les bots remplacent progressivement les Zaps lineaires pour les cas d'usage complexes.
- **Zapier Tables + Interfaces** : evolution vers une plateforme applicative legere, ou les automatisations ne sont qu'un composant d'une application complete (formulaire + logique + base de donnees + interface).
- **AI Actions** : actions alimentees par l'IA pour la classification, l'extraction, la generation de texte et le resume, integrees nativement dans les Zaps.
- **Canvas** : nouvelle interface visuelle (en plus de la vue lineaire traditionnelle) pour concevoir des workflows plus complexes, se rapprochant de l'interface de Make.
- **Enterprise features** : SSO, SCIM, audit logs, DLP, approvals pour les grandes organisations.

### Make

- **AI Assistant** : assistant IA pour la creation et le debugging de scenarios en langage naturel.
- **Make Apps** : possibilite de creer des applications personnalisees (connecteurs custom) et de les publier dans le marketplace Make.
- **Functions** : custom functions reutilisables pour les transformations de donnees complexes (disponible sur le plan Pro).
- **Teams features** : espaces d'equipe, roles granulaires, templates partages et governance.
- **Performance** : execution plus rapide, meilleure gestion des gros volumes et optimisation automatique des scenarios.

### Convergence du marche

Les plateformes convergent vers un modele integre combinant :
1. Automatisation de workflows (coeur de metier)
2. Base de donnees integree (Zapier Tables, Make Data Stores)
3. Interface utilisateur (Zapier Interfaces, Make custom apps)
4. IA integree (agents, classification, extraction)
5. Governance enterprise (SSO, audit, DLP)

Cette convergence rapproche les plateformes no-code d'automatisation des plateformes no-code d'applications (Retool, Bubble), creant un continuum entre automatisation et developpement d'applications.
