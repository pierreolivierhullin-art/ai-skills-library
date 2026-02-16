# App Builders — Retool, Glide, AppSheet, Bubble, Softr & Plateformes No-Code

## Overview

Ce document de reference couvre les principales plateformes de construction d'applications no-code et low-code. Il fournit une analyse approfondie de Retool, Glide, AppSheet, Bubble et Softr, avec leurs architectures, cas d'usage optimaux, forces, limites et strategies de deploiement. Utiliser ce guide pour choisir la plateforme adaptee a chaque projet, concevoir l'architecture applicative et planifier le deploiement et la maintenance.

---

## Retool — Outils Internes et Admin Panels

### Positionnement

Retool est une plateforme low-code specialisee dans la construction d'outils internes. Son positionnement est unique : elle cible les equipes techniques qui ont besoin de construire rapidement des interfaces d'administration, des dashboards operationnels et des back-offices connectes a des bases de donnees SQL et des API.

### Architecture

Retool fonctionne selon un modele component-based avec data queries :

1. **Data Sources** : connexion directe a des bases de donnees (PostgreSQL, MySQL, MongoDB, BigQuery, Snowflake), des API REST/GraphQL, Google Sheets, Airtable, Firebase, et plus de 50 sources de donnees.
2. **Queries** : requetes SQL natives, appels API, transformateurs JavaScript. Les queries sont le coeur de Retool — elles alimentent les composants en donnees et declenchent des actions.
3. **Components** : biblioteque de 100+ composants UI preconstruits (tables, formulaires, graphiques, boutons, modals, onglets, containers). Chaque composant expose des proprietes configurables et des event handlers.
4. **Event Handlers** : logique declenchee par les interactions utilisateur (clic, soumission de formulaire, changement de valeur). Permet de chainer des queries et des actions.
5. **Transformers** : code JavaScript pour transformer les donnees entre les queries et les composants.

### Composants cles

| Composant | Usage | Configuration |
|---|---|---|
| **Table** | Affichage tabulaire avec tri, filtre, pagination, edition inline | Source: query SQL/API, colonnes configurables, actions par ligne |
| **Form** | Formulaire de saisie avec validation | Champs mappes sur les colonnes de la source, validation custom |
| **Chart** | Graphiques (bar, line, pie, area, scatter) | Source: query, axes configurables, series multiples |
| **Text Input / Select / Date** | Champs de saisie individuels | Valeur par defaut, validation, binding bidirectionnel |
| **Modal** | Fenetre modale pour les details ou confirmations | Declenchee par un bouton ou un event handler |
| **Container / Tabs** | Organisation du layout | Imbriquer des composants, creer des vues a onglets |
| **JSON Explorer** | Visualisation de donnees JSON | Debug et exploration de reponses API |
| **File Upload** | Upload de fichiers | Stockage S3 ou base64, limites de taille configurables |

### Cas d'usage optimaux

- **Admin panels** : gestion d'utilisateurs, moderation de contenu, configuration d'application, gestion de droits.
- **Dashboards operationnels** : metriques temps reel, alertes, monitoring de services.
- **Outils de support** : consultation de profils client, historique des interactions, actions de remboursement.
- **Back-office e-commerce** : gestion des commandes, des stocks, des promotions, des retours.
- **Outils data** : requetes ad-hoc, exploration de donnees, rapports custom.

### Forces et limites

**Forces** :
- Connexion SQL native — ecrire de vraies requetes SQL, pas des abstractions limitantes.
- Composants riches et professionnels — table avec tri, filtre, export, edition inline out-of-the-box.
- JavaScript everywhere — transformers, event handlers, custom components. Flexibilite quasi illimitee pour les developpeurs.
- Self-hosted option — Retool On-Premise pour les organisations avec des exigences de securite strictes.
- Git sync — versionner les applications dans Git, branching, pull requests.
- Permissions granulaires — RBAC par application, par page, par composant.

**Limites** :
- Necessite des competences techniques — SQL et JavaScript sont quasi obligatoires pour des applications non triviales.
- Pas adapte aux applications publiques (customer-facing) — concu pour les outils internes uniquement.
- Tarification elevee — a partir de $10/utilisateur/mois (Cloud), significativement plus pour l'Enterprise.
- Courbe d'apprentissage — le modele queries + components + event handlers demande un investissement initial de 1-2 semaines.
- Experience mobile limitee — les applications Retool sont optimisees pour desktop, le responsive est possible mais necessite du travail supplementaire.

### Deploiement

- **Retool Cloud** : SaaS manage, deployment immediat, pas de maintenance infrastructure.
- **Retool On-Premise** : Docker/Kubernetes, donnees et applications restent dans votre infrastructure. Adapte aux organisations avec des contraintes de securite (banques, sante, defense).
- **Retool Embedded** : integrer des applications Retool dans vos propres produits SaaS (portails clients, dashboards embedded).

---

## Glide — Applications Mobiles No-Code

### Positionnement

Glide est une plateforme no-code specialisee dans la creation d'applications mobiles (Progressive Web Apps) a partir de sources de donnees existantes (Google Sheets, Airtable, Excel, SQL). Son approche mobile-first et sa simplicite en font un choix ideal pour les applications terrain, les outils de collecte de donnees et les applications d'equipe.

### Architecture

1. **Data Source** : Google Sheets, Airtable, Excel, Glide Tables (base de donnees native), SQL (via connexion directe).
2. **Glide Tables** : base de donnees native de Glide, plus performante que Google Sheets pour les volumes importants. Supporte les relations, les computed columns et les row owners.
3. **Layout System** : systeme de mise en page base sur des screens preconfigures (List, Details, Form, Map, Chart, Calendar, Kanban).
4. **Components** : composants visuels configurables (titre, image, bouton, champ de saisie, carte, liste, graphique).
5. **Actions** : logique declenchee par les interactions (navigation, creation/modification de record, envoi d'email, notification push, ouverture d'URL).
6. **Computed Columns** : colonnes calculees dans Glide Tables (if-then-else, template, math, lookup, rollup, relation).

### Cas d'usage optimaux

- **Applications terrain** : collecte de donnees sur le terrain (inspections, inventaires, rapports de visite, relevees).
- **Annuaires d'equipe** : repertoire des employes avec photos, coordonnees, competences.
- **Outils de suivi** : suivi des taches, des livraisons, des maintenances, des incidents.
- **Catalogues** : catalogue produits, portfolio projets, menu restaurant, listing immobilier.
- **Applications evenementielles** : programme de conference, gestion d'inscriptions, check-in.

### Forces et limites

**Forces** :
- Rapidite de construction — une application fonctionnelle en 30-60 minutes.
- Mobile-first — PWA optimisee pour smartphone, installable sur l'ecran d'accueil.
- Glide Tables — base de donnees native performante, pas de dependance a Google Sheets pour la production.
- Row Owners — securite granulaire au niveau de la ligne (chaque utilisateur voit uniquement ses donnees).
- Templates — bibliotheque de templates preconstruits pour demarrer rapidement.

**Limites** :
- Logique limitee — pas de workflows complexes, pas de branchements conditionnels avances.
- Design contraint — les layouts sont preconfigures, la personnalisation du design est limitee.
- Pas de web app complete — l'experience desktop existe mais est secondaire par rapport au mobile.
- Limites de donnees — 25 000 rows (Business), extensible mais avec un cout supplementaire.
- Pas d'API pour construire des integrations custom — dependance aux connecteurs existants et a Zapier/Make.

### Deploiement

- **PWA** : deploiement instantane via un lien URL. L'application peut etre ajoutee a l'ecran d'accueil du smartphone.
- **Custom domain** : utiliser son propre domaine pour l'URL de l'application (plan Business+).
- **QR Code** : generer un QR code pour faciliter l'acces des utilisateurs terrain.

---

## AppSheet — Ecosysteme Google Native

### Positionnement

AppSheet est la plateforme no-code de Google, integree a Google Workspace. Elle permet de creer des applications mobiles et web a partir de Google Sheets, Excel, SQL databases et Cloud SQL. Son integration native avec l'ecosysteme Google (Drive, Calendar, Gmail, Maps) en fait le choix naturel pour les organisations Google Workspace.

### Architecture

1. **Data Sources** : Google Sheets (natif), Excel, Cloud SQL (MySQL, PostgreSQL), Salesforce, Smartsheet, OData, REST API.
2. **Data Model** : AppSheet genere automatiquement un modele de donnees a partir de la source. Les colonnes sont typees (Text, Number, Date, Enum, Ref, Image, LatLong) et les relations sont definies via des colonnes Ref.
3. **Views** : ecrans de l'application, configures par type (Table, Detail, Form, Map, Chart, Calendar, Dashboard, Deck).
4. **Actions** : logique declenchee par les interactions utilisateur ou les conditions (navigation, modification de donnees, envoi d'email, appel API).
5. **Bots (Automations)** : workflows declenches par des evenements (creation, modification, suppression, schedule). Un bot = event + process (sequence de steps).
6. **Expressions** : langage de formules proprietaire AppSheet pour les calculs, conditions et validations. Syntaxe specifique (ex. `SELECT(Taches[Titre], [Projet] = [_THISROW].[Projet])`).

### Expressions AppSheet — Reference

Le langage d'expressions AppSheet est puissant mais possede une syntaxe unique qu'il faut maitriser.

| Fonction | Syntaxe | Exemple |
|---|---|---|
| Condition | `IF(test, yes, no)` | `IF([Status] = "Urgent", "Rouge", "Vert")` |
| Selection | `SELECT(table[column], condition)` | `SELECT(Taches[Titre], [Projet] = [_THISROW].[Projet])` |
| Comptage | `COUNT(SELECT(...))` | `COUNT(SELECT(Taches[ID], [Status] = "En cours"))` |
| Lookup | `LOOKUP(value, table, column, result)` | `LOOKUP([Client ID], Clients, [ID], [Nom])` |
| Reference | `[_THISROW].[Column]` | Reference au record courant |
| Context | `USEREMAIL()` | Email de l'utilisateur connecte |
| Date | `TODAY()`, `NOW()`, `TIMENOW()` | Dates et heures courantes |
| Math | `SUM()`, `AVERAGE()`, `MAX()`, `MIN()` | Aggregations |

### Cas d'usage optimaux

- **Applications Google Workspace** : outils qui s'integrent nativement avec Sheets, Drive, Calendar, Gmail.
- **Applications terrain** : collecte de donnees avec mode offline, photos geolocalisees, signatures.
- **Approbations et workflows** : circuits de validation multi-niveaux, demandes de conge, notes de frais.
- **Inventaires et inspections** : suivi d'actifs, checklist d'inspection, rapports photographiques.
- **Planning et reservations** : gestion de salles, planning d'equipe, reservation de materiel.

### Forces et limites

**Forces** :
- Integration Google native — Sheets, Drive, Calendar, Gmail, Maps sont des sources et des actions natives.
- Mode offline robuste — les donnees sont synchronisees automatiquement quand la connexion revient. Essentiel pour les applications terrain.
- Generation automatique — AppSheet genere une application fonctionnelle a partir d'un Google Sheets existant en quelques minutes.
- Bots puissants — automations avec steps chaines (email, SMS, push notification, webhook, modifier donnees).
- Securite — filter conditions pour limiter les donnees visibles par utilisateur, integration Google SSO.
- Duet AI — assistance IA pour la creation d'expressions, la configuration d'applications et la generation de bots.

**Limites** :
- Expressions complexes — la syntaxe AppSheet est unique et la courbe d'apprentissage est reelle pour les expressions avancees.
- Design limite — les options de personnalisation visuelle sont moins riches que Bubble ou meme Glide.
- Performance avec Google Sheets — les Sheets volumineux (> 5 000 lignes) ralentissent significativement l'application. Migrer vers Cloud SQL pour les volumes importants.
- Debugging difficile — les erreurs dans les expressions sont parfois cryptiques et difficiles a diagnostiquer.
- Dependance Google — si l'organisation quitte Google Workspace, la migration est significative.

---

## Bubble — Applications Web Full-Stack

### Positionnement

Bubble est la plateforme no-code la plus puissante pour construire des applications web completes (SaaS, marketplaces, portails, applications metier complexes). C'est la seule plateforme no-code qui permet de construire des applications de niveau production avec une logique metier complexe, une base de donnees relationnelle native, un systeme d'authentification complet et un deploiement professionnel.

### Architecture

1. **Database** : base de donnees relationnelle native (PostgreSQL sous le capot). Types de donnees (data types), champs (fields), relations (one-to-many, many-to-many). Privacy rules pour le controle d'acces au niveau des donnees.
2. **Design** : editeur visuel WYSIWYG avec un systeme de composants (elements). Responsive design avec des breakpoints configurables. CSS custom possible via plugins.
3. **Workflows** : logique metier declenchee par des evenements (clic, page load, condition, API, schedule). Chaque workflow est une sequence d'actions (create/modify thing, navigate, send email, API call, set state, show/hide element).
4. **API Connector** : connexion a des API externes en GET/POST/PUT/DELETE. Configuration des headers, body, authentification. Responses mappees sur des types Bubble.
5. **Backend Workflows** : workflows executes cote serveur (scheduled, recursive, API trigger). Essentiels pour les traitements longs, les taches periodiques et les API endpoints.
6. **Plugins** : marketplace de 2 000+ plugins creees par la communaute (payments, charts, maps, auth providers, AI, integrations).

### Systeme de Workflows en Detail

Les workflows sont le coeur de la logique dans Bubble. Chaque workflow est compose de :

- **Trigger** : evenement declencheur (element clicked, page loaded, condition true, API received, scheduled).
- **Conditions** : conditions supplementaires pour l'execution (Only when...).
- **Actions** : sequence d'actions executees dans l'ordre (create thing, make changes to thing, navigate to page, send email, schedule API workflow, set state, show/hide element, run JavaScript).

#### Patterns de workflow courants

**Pattern 1 — CRUD complet**
```
Workflow: Create
  Trigger: Button "Creer" clicked
  Action 1: Create a new Thing (type = Projet, fields = inputs)
  Action 2: Navigate to page "Projet Detail" (data = Result of Step 1)
  Action 3: Show success toast

Workflow: Update
  Trigger: Button "Sauvegarder" clicked
  Action 1: Make changes to Current Page's Projet (fields = inputs)
  Action 2: Show success toast

Workflow: Delete
  Trigger: Button "Supprimer" clicked
  Condition: Alert confirmed
  Action 1: Delete Current Page's Projet
  Action 2: Navigate to page "Projets List"
```

**Pattern 2 — Inscription avec validation**
```
Workflow: Sign Up
  Trigger: Button "S'inscrire" clicked
  Condition: All inputs valid
  Action 1: Sign the user up (email, password)
  Action 2: Create a new Thing (type = UserProfile, fields = nom, entreprise)
  Action 3: Make changes to User (UserProfile = Result of Step 2)
  Action 4: Send email (confirmation)
  Action 5: Navigate to page "Dashboard"
```

### Privacy Rules

Les privacy rules sont le systeme d'access control au niveau des donnees dans Bubble. Elles definissent qui peut voir, trouver, modifier et supprimer chaque type de donnees.

```
Data Type: Projet
  Privacy Rule 1: Owner Access
    - Who: Current User = This Projet's Creator
    - Can view: all fields
    - Can find: yes
    - Can modify: yes
    - Can delete: yes

  Privacy Rule 2: Team Member Access
    - Who: Current User is in This Projet's Team Members
    - Can view: all fields except Budget
    - Can find: yes
    - Can modify: Statut, Taches
    - Can delete: no

  Privacy Rule 3: Public Access (no rule matches)
    - Can view: Nom, Description only
    - Can find: yes (if public = yes)
    - Can modify: no
    - Can delete: no
```

### Cas d'usage optimaux

- **SaaS applications** : applications multi-tenant avec inscription, abonnement, facturation.
- **Marketplaces** : mise en relation acheteurs/vendeurs, gestion des listings, paiements, avis.
- **Portails complexes** : portails clients avec authentification, dashboards, gestion documentaire.
- **Applications metier complexes** : CRM, ERP legers, outils de gestion avec logique metier avancee.
- **MVP de startups** : prototype fonctionnel pour valider une hypothese produit avant de coder.

### Forces et limites

**Forces** :
- Puissance — la seule plateforme no-code capable de construire des applications de niveau SaaS.
- Base de donnees native — modele relationnel complet avec privacy rules, pas de dependance externe.
- Extensibilite — 2 000+ plugins, API Connector, custom JavaScript, backend workflows.
- Deploiement pro — custom domain, SSL, CDN, staging/production environments.
- Communaute — 3M+ d'utilisateurs, forum actif, documentation exhaustive, tutoriels abondants.

**Limites** :
- Courbe d'apprentissage elevee — 2-4 semaines pour devenir productif, 2-3 mois pour maitriser les patterns avances.
- Performance — les applications Bubble peuvent etre lentes si mal optimisees (queries non efficientes, trop d'elements sur une page, images non compressees).
- Vendor lock-in fort — le code genere par Bubble n'est pas exportable. Si vous quittez Bubble, vous reconstruisez de zero.
- SEO limite — le rendu client-side rend le SEO plus difficile (ameliore avec la version 2025+ et les meta tags dynamiques).
- Couts a l'echelle — le pricing par workload units peut devenir significatif pour les applications a fort trafic (> 10K utilisateurs actifs).

---

## Softr — Portails et Sites avec Airtable

### Positionnement

Softr est une plateforme no-code specialisee dans la creation de portails clients, d'intranets et de sites web connectes a Airtable ou Google Sheets. Son approche est la plus simple du marche : choisir un template, connecter une source de donnees, personnaliser et publier en quelques heures.

### Architecture

1. **Data Source** : Airtable (natif, bidirectionnel), Google Sheets, HubSpot CRM, Notion (beta). Airtable est la source de donnees recommandee et la plus integree.
2. **Blocks** : composants preconstruits que l'on place sur les pages (list, details, form, chart, hero, features, CTA, pricing, FAQ, testimonials, team, footer).
3. **User Authentication** : systeme d'authentification integre avec Airtable comme user database. Supporte email/password, Magic Link, Google SSO, SSO SAML (Enterprise).
4. **Conditional Visibility** : afficher ou masquer des blocks, des boutons ou des champs selon le role de l'utilisateur, ses donnees ou des conditions custom.
5. **Custom Domains** : deploiement sur un domaine personnalise avec SSL automatique.

### Blocks principaux

| Block | Fonction | Configuration |
|---|---|---|
| **List** | Affiche une liste de records (grille, liste, cards) | Source Airtable, filtres, tri, champs affiches, pagination |
| **List Details** | Page de detail d'un record | Champs affiches, actions (edit, delete), layout |
| **Form** | Formulaire de creation/edition de record | Champs mappes, validation, conditions, redirect |
| **Chart** | Graphiques | Source Airtable, type (bar, line, pie), axes |
| **Kanban** | Vue kanban | Source Airtable, champ de colonne, champs sur carte |
| **Calendar** | Vue calendrier | Source Airtable, champ date, champs affiches |
| **Action Button** | Bouton avec action | Update record, open URL, open modal, send email |
| **Conditional Form** | Formulaire avec logique conditionnelle | Champs visibles selon les reponses |

### User Management

Softr integre un systeme de gestion d'utilisateurs avec Airtable comme backend :

1. **Users Table** : une table Airtable "Users" contient les profils utilisateurs (email, nom, role, groupe).
2. **Authentication** : email/password, Magic Link (lien de connexion par email), Google SSO.
3. **Roles & Groups** : les roles sont definis par un champ dans la table Users. Les groupes permettent de regrouper les utilisateurs pour les permissions.
4. **Page-level Permissions** : chaque page peut etre restreinte a des roles ou groupes specifiques.
5. **Data Filtering** : les donnees affichees sont automatiquement filtrees selon l'utilisateur connecte (ex. "ne montrer que les records ou le champ Email = utilisateur connecte").

### Cas d'usage optimaux

- **Portails clients** : espace client securise avec suivi de commandes, documents, historique, support.
- **Portails fournisseurs** : soumission de catalogues, suivi de commandes, facturation.
- **Intranets d'equipe** : annuaire, ressources, actualites, formulaires internes.
- **Directories et listings** : annuaire d'entreprises, repertoire de professionnels, catalogue avec filtres.
- **Sites membres** : contenu premium, cours en ligne, communaute avec niveaux d'acces.

### Forces et limites

**Forces** :
- Simplicite extreme — la plateforme la plus facile a prendre en main pour creer un portail fonctionnel.
- Airtable integration — bidirectionnelle, temps reel, configuration en quelques clics.
- Templates professionnels — 50+ templates couvrant les cas d'usage courants.
- User management integre — authentification, roles, permissions sans configuration complexe.
- Pricing accessible — plan gratuit genereux, plans payes a partir de $49/mois.

**Limites** :
- Personnalisation design limitee — les blocks sont preconfigures, le CSS custom est limite.
- Logique limitee — pas de workflows complexes, pas de calculs avances, dependance a Airtable pour la logique.
- Performance avec Airtable — les limites d'Airtable (50K records, API rate limits) s'appliquent directement.
- Pas adapte aux applications complexes — pour des logiques metier avancees, preferer Bubble ou Retool.
- SEO basique — les fonctionnalites SEO sont presentes mais moins avancees que les CMS specialises.

---

## Comparaison Detaillee des Plateformes

### Matrice de comparaison

| Critere | Retool | Glide | AppSheet | Bubble | Softr |
|---|---|---|---|---|---|
| **Type d'app** | Outils internes | Mobile-first | Mobile + Web | Web full-stack | Portails & sites |
| **Public cible** | Developpeurs | Non-tech | Semi-tech | Semi-tech / Tech | Non-tech |
| **Backend** | SQL/API externe | Sheets/Airtable/SQL | Sheets/SQL | Natif (PostgreSQL) | Airtable/Sheets |
| **Logique metier** | JS + SQL (forte) | Limitee | Expressions (moyenne) | Workflows (forte) | Tres limitee |
| **Mobile** | Limite | Excellent (PWA) | Excellent (natif) | Responsive | Responsive |
| **Offline** | Non | Partiel | Oui (natif) | Non | Non |
| **Auth** | SSO/SAML | Email/Google | Google SSO | Email/Google/SSO | Email/Magic Link/SSO |
| **API** | Natif (fort) | Via integrations | Via bots | API Connector (fort) | Via Airtable |
| **Self-hosted** | Oui (On-Premise) | Non | Non | Non | Non |
| **Free tier** | Oui (5 users) | Oui (limite) | Oui (10 users) | Oui (limite) | Oui (limite) |
| **Pricing entry** | $10/user/mois | $25/app/mois | $5/user/mois | $29/mois | $49/mois |
| **Temps 1ere app** | 2-5 jours | 1-3 heures | 1-3 heures | 1-2 semaines | 1-3 heures |
| **Vendor lock-in** | Moyen (SQL exportable) | Fort | Moyen (Sheets exportable) | Tres fort | Moyen (Airtable exportable) |

### Arbre de decision rapide

```
Besoin d'un outil interne avec SQL ? --> Retool
Besoin d'une app mobile simple ? --> Glide
Ecosysteme Google Workspace ? --> AppSheet
Besoin d'une app web complexe (SaaS, marketplace) ? --> Bubble
Besoin d'un portail client avec Airtable ? --> Softr
Besoin d'un formulaire avance ? --> Tally ou Typeform
Prototype rapide < 1 jour ? --> Glide ou Softr
```

---

## Architecture Patterns pour Applications No-Code

### Pattern 1 — Monolithique (Single Platform)

Tout est construit sur une seule plateforme.

```
[Utilisateurs] --> [Bubble / Retool / AppSheet]
                      |
                   [BDD native]
```

**Quand l'utiliser** : applications simples a moyennes, equipe reduite, pas d'integrations complexes.
**Avantage** : simplicite, pas de synchronisation entre outils.
**Risque** : vendor lock-in, limites de la plateforme.

### Pattern 2 — Data Layer + Presentation Layer (Composable)

Separer la couche de donnees de la couche de presentation.

```
[Portail client] --> [Softr] --> [Airtable] <-- [Admin panel] --> [Retool]
                                    |
                               [Automations]
                                    |
                              [Make / Zapier]
```

**Quand l'utiliser** : besoin de vues differentes pour differents publics (clients vs admins), donnees centralisees dans Airtable.
**Avantage** : chaque couche utilise l'outil le plus adapte, donnees centralisees.
**Risque** : synchronisation entre outils, complexite d'integration.

### Pattern 3 — Hub & Spoke (Integration-Centric)

Une plateforme d'automatisation au centre connecte les outils specialises.

```
[Formulaire Tally] --\
[Airtable CRM]     --+--> [Make / n8n] --+--> [Slack notifications]
[Google Sheets]    --/                    +--> [Email campaigns]
                                          +--> [Google Sheets reports]
```

**Quand l'utiliser** : ecosysteme multi-outils existant, besoin de synchroniser des donnees entre plusieurs sources.
**Avantage** : flexibilite, chaque outil reste independant.
**Risque** : complexite des automations, points de defaillance multiples.

---

## Deploiement et Hosting

### Strategies de deploiement

| Strategie | Description | Plateformes |
|---|---|---|
| **SaaS manage** | L'application est hebergee par la plateforme, deploiement immediat | Toutes |
| **Custom domain** | Utiliser son propre domaine avec un CNAME | Bubble, Softr, Glide, AppSheet |
| **Self-hosted** | L'application et les donnees sont sur votre infrastructure | Retool uniquement |
| **Embedded** | L'application est integree dans un produit existant (iframe, SDK) | Retool, Softr |
| **PWA** | L'application est installable comme une app native sur mobile | Glide, AppSheet |

### Environnements

| Environnement | Usage | Plateformes supportees |
|---|---|---|
| **Development** | Construction et tests | Bubble, Retool |
| **Staging** | Tests d'acceptance avant production | Bubble (version test), Retool |
| **Production** | Application live pour les utilisateurs finaux | Toutes |

Bubble est la seule plateforme no-code qui offre un vrai workflow development → staging → production avec deploiement controle.

---

## Pricing — Analyse Comparative (2025-2026)

### Modeles de pricing

| Plateforme | Modele | Free tier | Plan d'entree | Enterprise |
|---|---|---|---|---|
| **Retool** | Par utilisateur | 5 users, fonctionnalites limitees | $10/user/mois (Standard) | Custom pricing |
| **Glide** | Par application | 1 app, 500 rows | $25/app/mois (Maker) | Custom pricing |
| **AppSheet** | Par utilisateur | 10 users, fonctionnalites limitees | $5/user/mois (Starter) | $10/user/mois (Enterprise) |
| **Bubble** | Par application | 1 app, limites strictes | $29/mois (Starter) | $349/mois (Team) |
| **Softr** | Par application | 1 app, 5 users | $49/mois (Basic) | Custom pricing |

### Facteurs de cout caches

- **Retool** : le cout par utilisateur augmente vite — 50 utilisateurs x $10 = $500/mois. Les utilisateurs en lecture seule sont moins chers.
- **Glide** : le cout est par application — si vous avez 10 micro-apps, le cout s'additionne.
- **AppSheet** : le prix par utilisateur est bas, mais les fonctionnalites avancees (bots, offline, security) necessitent le plan Enterprise.
- **Bubble** : le plan Starter est limite (workflow executions capped). Les applications a fort trafic necessitent le plan Team ou superieur.
- **Softr** : le plan gratuit est genereux (5 utilisateurs), mais les fonctionnalites cles (custom domain, remove branding) necessitent un plan paye.

---

## Strategies de Migration

### Migration entre plateformes no-code

La migration entre plateformes no-code est couteuse car il n'existe pas de standard d'interoperabilite. Les strategies dependent de l'architecture de l'application source.

#### Migration avec donnees separees (Airtable-centric)

Si les donnees sont dans Airtable et que seule la couche de presentation change (ex. Softr → Bubble), la migration est relativement simple :
1. Exporter les donnees depuis Airtable (CSV ou API).
2. Recreer le modele de donnees dans la nouvelle plateforme.
3. Importer les donnees.
4. Reconstruire les interfaces et la logique.
5. Tester et deployer progressivement.

#### Migration monolithique (ex. Bubble → Code)

Si l'application entiere est construite sur une seule plateforme (typiquement Bubble), la migration est une reconstruction complete :
1. Documenter toutes les fonctionnalites, la logique metier et les workflows.
2. Exporter les donnees (Bubble permet l'export CSV).
3. Concevoir l'architecture de la nouvelle application (framework, base de donnees).
4. Reconstruire l'application de zero en utilisant la documentation comme specification.
5. Migrer les donnees, tester et deployer en parallele.
6. Basculer progressivement les utilisateurs.

### Migration no-code vers code

La migration du no-code vers le code est souvent motivee par :
- Les limites de performance de la plateforme no-code.
- Le besoin de fonctionnalites non supportees.
- Le cout devenu prohibitif a l'echelle.
- Le besoin de controle total sur l'infrastructure.

**Approche recommandee** :
1. **Ne pas migrer tout d'un coup** — identifier les fonctionnalites critiques a migrer en priorite.
2. **Coexistence temporaire** — la nouvelle application codee coexiste avec l'application no-code pendant la transition.
3. **API comme couche d'abstraction** — utiliser des API pour synchroniser les donnees entre les deux systemes pendant la migration.
4. **Specifications = application no-code** — l'application no-code existante est la meilleure specification fonctionnelle pour la reconstruction.

---

## Checklist de Selection de Plateforme

1. **Definir le type d'application** : interne vs externe, web vs mobile, simple vs complexe.
2. **Identifier les utilisateurs** : nombre, niveau technique, devices, mode de connexion.
3. **Evaluer la complexite des donnees** : volume, relations, securite, sources existantes.
4. **Evaluer la complexite de la logique** : workflows, conditions, calculs, integrations.
5. **Verifier l'ecosysteme** : outils existants (Google, Airtable, SQL), integrations requises.
6. **Estimer le budget** : cout par utilisateur vs par application, couts caches.
7. **Evaluer le risque de lock-in** : exportabilite des donnees, dependance a la plateforme.
8. **Tester avec un prototype** : construire un prototype minimal sur la plateforme candidate en 1-2 jours.
9. **Valider la scalabilite** : limites de records, d'utilisateurs, de performances.
10. **Verifier la conformite** : GDPR, SOC2, hebergement des donnees, SSO.
