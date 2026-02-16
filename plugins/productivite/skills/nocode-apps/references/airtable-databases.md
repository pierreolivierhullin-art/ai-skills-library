# Airtable & Bases de Donnees Visuelles — Modelisation, Vues, Automations & Integration

## Overview

Ce document de reference couvre les fondamentaux d'Airtable et des bases de donnees visuelles, de la conception du modele de donnees a l'integration avec les systemes externes. Il fournit les bases theoriques, les patterns pratiques et les approches avancees necessaires pour construire des applications robustes sur Airtable et ses alternatives. Utiliser ce guide comme fondation pour tout projet impliquant une base de donnees visuelle, que ce soit pour un CRM interne, un tracker de projet, un inventaire ou un systeme de gestion complexe.

---

## Airtable — Fondamentaux

### Architecture de base

Airtable organise les donnees selon une hierarchie a quatre niveaux :

1. **Workspace** : conteneur de niveau superieur qui regroupe les bases liees a un domaine, un departement ou un projet. Les permissions sont gerees au niveau du workspace (owner, creator, editor, commenter, viewer).
2. **Base** : equivalent d'une base de donnees. Chaque base contient des tables liees entre elles. Une base represente generalement un domaine metier coherent (ex. "Gestion Commerciale", "Suivi Projets").
3. **Table** : equivalent d'une table relationnelle. Chaque table contient des records (lignes) et des fields (colonnes). Les tables sont liees entre elles par des linked record fields.
4. **View** : representation visuelle filtree et triee d'une table. Chaque table peut avoir plusieurs vues sans dupliquer les donnees. Les vues sont le mecanisme principal pour adapter l'affichage a chaque persona.

### Types de champs (Field Types)

Airtable propose plus de 25 types de champs natifs. Maitriser les types de champs est essentiel pour construire un modele de donnees robuste.

#### Champs de base

| Type | Usage | Bonnes pratiques |
|---|---|---|
| **Single line text** | Noms, titres, identifiants courts | Utiliser comme primary field pour nommer chaque record de maniere unique |
| **Long text** | Descriptions, notes, commentaires | Activer le rich text formatting pour les contenus structures |
| **Number** | Quantites, montants, scores | Configurer le format (integer, decimal, precision) selon le cas d'usage |
| **Currency** | Montants monetaires | Toujours specifier la devise et la precision (2 decimales) |
| **Percent** | Taux, ratios, pourcentages | Stocker la valeur en pourcentage (0-100), pas en decimal (0-1) |
| **Date** | Dates, deadlines, jalons | Activer le time field si necessaire, configurer le fuseau horaire |
| **Checkbox** | Booleens, statuts binaires | Ideal pour les flags (actif/inactif, valide/invalide, fait/a faire) |
| **Single select** | Categories a choix unique | Limiter a 20-30 options maximum, utiliser des couleurs coherentes |
| **Multiple select** | Tags, categories multiples | Ne pas utiliser pour modeliser des relations — preferer les linked records |
| **Email** | Adresses email | Validation automatique du format, cliquable en mode lecture |
| **Phone** | Numeros de telephone | Pas de validation de format strict — standardiser par convention |
| **URL** | Liens web | Validation automatique, cliquable en mode lecture |
| **Attachment** | Fichiers, images, documents | Limite de 100 MB par fichier (plan Pro), stockage inclus dans le quota |

#### Champs relationnels et calcules

| Type | Usage | Fonctionnement |
|---|---|---|
| **Linked record** | Relations entre tables | Cree une relation bidirectionnelle. Supporte one-to-many et many-to-many. C'est le champ le plus important pour un modele de donnees propre |
| **Lookup** | Recuperer un champ d'une table liee | Affiche la valeur d'un champ de la table liee via un linked record. Lecture seule, mis a jour automatiquement |
| **Rollup** | Agreger des valeurs de records lies | Calcule une aggregation (SUM, COUNT, AVG, MIN, MAX, COUNTA) sur un champ des records lies. Indispensable pour les totaux et les metriques |
| **Count** | Compter les records lies | Cas simplifie du rollup : compte le nombre de records lies. Utile pour les metriques rapides |
| **Formula** | Calculs sur les champs du meme record | Syntaxe proprietaire Airtable. Supporte les operations mathematiques, texte, date, logique. Ne peut pas reference directement des champs d'autres tables (utiliser lookup d'abord) |
| **Created time** | Timestamp de creation automatique | Genere automatiquement, non modifiable. Indispensable pour l'audit trail |
| **Last modified time** | Timestamp de derniere modification | Configure sur des champs specifiques ou sur tout le record. Essentiel pour le suivi des mises a jour |
| **Created by / Last modified by** | Utilisateur createur / modificateur | Genere automatiquement. Utile pour l'audit et la responsabilisation |
| **Autonumber** | Identifiant sequentiel automatique | Genere automatiquement, unique, non recyclable. Ideal pour les numeros de reference (TICKET-001) |
| **Button** | Declencheur d'action | Execute un script, ouvre une URL ou declenche une automation. Ajoute de l'interactivite aux vues |

---

## Modelisation Relationnelle en Airtable

### Principes fondamentaux

La modelisation relationnelle en Airtable suit les memes principes que la modelisation en base de donnees classique, avec quelques specificites liees a la plateforme.

#### Regle 1 — Une table par entite

Chaque entite metier distincte doit avoir sa propre table. Les entites typiques sont : Clients, Projets, Taches, Produits, Commandes, Employes, Fournisseurs, Evenements.

**Symptome d'un mauvais decoupage** : une table contient une colonne "Type" ou "Categorie" qui distingue des enregistrements fondamentalement differents (ex. une table "Contacts" avec un champ "Type" = Client/Fournisseur/Partenaire). Dans ce cas, envisager de separer en tables distinctes.

#### Regle 2 — Normaliser pour eliminer la duplication

Ne jamais stocker la meme information a deux endroits. Si le nom d'un client apparait dans la table Commandes, il doit etre recupere via un linked record + lookup, pas saisi manuellement.

**Test de duplication** : si vous modifiez une information (ex. adresse d'un client), devez-vous la modifier dans plusieurs tables ? Si oui, le modele n'est pas normalise.

#### Regle 3 — Relations explicites via Linked Records

Toujours utiliser les linked record fields pour materialiser les relations entre tables. Ne jamais utiliser un champ texte contenant le nom d'un record d'une autre table — c'est fragile et non maintenable.

### Patterns relationnels

#### One-to-Many (1:N)

Le pattern le plus frequent. Un record parent est lie a plusieurs records enfants.

**Exemples** :
- Un Client a plusieurs Commandes
- Un Projet a plusieurs Taches
- Un Departement a plusieurs Employes

**Implementation** : creer un linked record field dans la table enfant pointant vers la table parent. Airtable cree automatiquement le champ reciproque dans la table parent.

**Rollups typiques** :
- Dans la table Client : COUNT des Commandes, SUM du montant des Commandes, MAX de la date de derniere Commande.
- Dans la table Projet : COUNT des Taches, pourcentage de Taches completees (ROLLUP avec formula).

#### Many-to-Many (M:N)

Quand un record peut etre lie a plusieurs records dans les deux sens.

**Exemples** :
- Un Employe possede plusieurs Competences, et une Competence est partagee par plusieurs Employes.
- Un Produit appartient a plusieurs Categories, et une Categorie contient plusieurs Produits.

**Implementation** : creer une table de jonction (junction table) qui contient deux linked record fields, un vers chaque table.

```
Table: Employes
- Nom
- Poste
- (linked to Employe_Competences)

Table: Competences
- Nom de la competence
- Niveau requis
- (linked to Employe_Competences)

Table: Employe_Competences (junction)
- Linked to Employes
- Linked to Competences
- Niveau maitrise (single select: Debutant, Intermediaire, Expert)
- Date d'evaluation
- Certificat (attachment)
```

La table de jonction peut contenir des attributs propres a la relation (niveau de maitrise, date, commentaires).

#### Self-referencing

Quand une table se refere a elle-meme (hierarchie, relations parent-enfant au sein de la meme entite).

**Exemples** :
- Un Employe a un Manager (qui est aussi un Employe)
- Une Tache a des Sous-taches (qui sont aussi des Taches)

**Implementation** : creer un linked record field dans la table qui pointe vers la meme table. Attention : Airtable ne supporte pas nativement les requetes recursives — pour les hierarchies profondes, envisager des champs formula ou des automations.

---

## Vues Airtable en Detail

### Grid View (Vue Grille)

La vue par defaut, semblable a un tableur. Ideal pour la saisie de donnees, l'edition en masse et l'analyse tabulaire.

**Configuration optimale** :
- Masquer les champs non pertinents pour le contexte (hide fields).
- Grouper par un champ categoriel (group by) pour organiser visuellement.
- Filtrer pour limiter les records affiches au contexte necessaire.
- Trier par pertinence (date, priorite, statut).
- Colorer les records selon un critere (conditional record coloring).

**Bonnes pratiques** :
- Creer une vue par persona ou par cas d'usage plutot qu'une vue unique pour tout le monde.
- Nommer les vues de maniere descriptive ("Taches en cours - Equipe Dev", pas "Vue 1").
- Verrouiller les vues de reference pour eviter les modifications accidentelles.

### Kanban View

Organise les records en colonnes basees sur un champ single select ou collaborator. Ideal pour les workflows avec des etapes (pipeline commercial, workflow de validation, sprint board).

**Cas d'usage** :
- Pipeline commercial : Prospect → Qualification → Proposition → Negociation → Gagne/Perdu.
- Workflow de contenu : Idee → Brouillon → Revue → Approuve → Publie.
- Gestion de tickets : Nouveau → En cours → En attente → Resolu → Ferme.

**Configuration** :
- Choisir le champ de stack (colonne) : single select ou collaborator.
- Configurer le card cover avec un champ attachment pour un rendu visuel.
- Afficher les champs cles sur la carte (titre, priorite, assignee, deadline).

### Calendar View

Affiche les records sur un calendrier base sur un champ date. Ideal pour la planification, les deadlines et les evenements.

**Cas d'usage** :
- Planning editorial : articles, posts reseaux sociaux, newsletters.
- Calendrier de livraisons : dates de livraison prevues par commande.
- Planning d'equipe : conges, formations, evenements.

### Gallery View

Affiche chaque record comme une carte visuelle avec une image principale. Ideal pour les catalogues, portfolios et annuaires visuels.

**Cas d'usage** :
- Catalogue produits avec photos.
- Portfolio de projets avec captures d'ecran.
- Annuaire d'equipe avec photos de profil.

### Gantt View

Affiche les records sur une timeline avec dates de debut et de fin. Supporte les dependances entre taches.

**Cas d'usage** :
- Planning de projet avec jalons et dependances.
- Roadmap produit avec phases et livrables.
- Planning de production avec sequences d'operations.

### Form View

Genere un formulaire de saisie public ou prive pour alimenter une table. Le formulaire cree un nouveau record a chaque soumission.

**Configuration avancee** :
- Personnaliser le titre, la description et le message de confirmation.
- Conditionner l'affichage des champs (conditional logic) selon les reponses.
- Rediriger vers une URL apres soumission.
- Limiter les soumissions (une par utilisateur).

---

## Airtable Automations

### Architecture des automations

Les automations Airtable suivent un pattern trigger → condition → action(s).

#### Triggers disponibles

| Trigger | Declenchement | Cas d'usage typique |
|---|---|---|
| **When a record is created** | Nouveau record dans une table | Notification, initialisation de champs, creation de records lies |
| **When a record is updated** | Modification d'un champ specifique | Changement de statut, mise a jour de date, alerte |
| **When a record matches conditions** | Un record entre dans un filtre defini | Alerte quand deadline < J+3, notification quand montant > seuil |
| **At a scheduled time** | Intervalle regulier (toutes les heures, quotidien, hebdomadaire) | Rapports periodiques, nettoyage, synchronisation |
| **When a form is submitted** | Soumission d'un formulaire lie | Confirmation, routage, creation de records dans d'autres tables |
| **When a button is clicked** | Clic sur un champ Button | Action manuelle declenchee par l'utilisateur |

#### Actions disponibles

| Action | Fonction | Limites |
|---|---|---|
| **Send email** | Envoyer un email avec des champs dynamiques | 100 emails/automation/run, templates basiques |
| **Send Slack message** | Poster dans un canal ou en DM | Necessite integration Slack configuree |
| **Create record** | Creer un record dans une table (meme base ou autre base) | Supporte cross-base depuis 2024 |
| **Update record** | Modifier les champs d'un record existant | Peut mettre a jour le record declencheur ou un record lie |
| **Find records** | Rechercher des records correspondant a des criteres | Retourne une liste de records, utilisable dans les actions suivantes |
| **Run a script** | Executer du code JavaScript | Acces aux inputs/outputs, API calls, logique complexe |
| **Call webhook** | Appeler une URL externe (POST/GET) | Timeout de 30 secondes, payload JSON |

### Patterns d'automation recommandes

#### Pattern 1 — Notification conditionnelle

```
Trigger: When record is updated (field: Status)
Condition: Status = "Urgent" AND Assignee is not empty
Action 1: Send Slack message to Assignee channel
Action 2: Send email to Assignee with record details
Action 3: Update record — set "Notification Sent" = true
```

#### Pattern 2 — Creation en cascade

```
Trigger: When record is created in "Projets"
Action 1: Create record in "Taches" — linked to Projet, Title = "Kickoff meeting"
Action 2: Create record in "Taches" — linked to Projet, Title = "Specification"
Action 3: Create record in "Taches" — linked to Projet, Title = "Revue finale"
Action 4: Update Projet record — set Status = "En cours"
```

#### Pattern 3 — Rapport periodique

```
Trigger: Scheduled — every Monday at 9:00 AM
Action 1: Find records where Status = "En retard"
Action 2: Run script — format records into summary
Action 3: Send email to managers with formatted summary
```

### Limites des automations

- **Quotas** : 25 000 runs/mois (Pro), 100 000 runs/mois (Enterprise). Un run = une execution complete du trigger + actions.
- **Pas de branchement conditionnel natif** : les conditions filtrent au niveau du trigger, mais il n'y a pas de if/else dans le flux d'actions. Utiliser des scripts pour la logique complexe.
- **Pas de boucle native** : pour iterer sur une liste de records, utiliser l'action "Find records" suivie d'un script.
- **Timeout des scripts** : 30 secondes pour les scripts d'automation. Pour les traitements longs, decouper en plusieurs automations chainees.

---

## Airtable Interface Designer

### Concept

L'Interface Designer permet de creer des interfaces personnalisees (dashboards, formulaires, portails) au-dessus des tables Airtable, sans exposer la structure brute des donnees.

### Elements d'interface

| Element | Fonction | Cas d'usage |
|---|---|---|
| **Grid** | Tableau filtrable et triable | Liste de records avec actions |
| **Record list** | Liste compacte de records | Navigation laterale |
| **Record detail** | Vue detaillee d'un record | Fiche complete avec edition |
| **Form** | Formulaire de creation/edition | Saisie guidee avec validation |
| **Chart** | Graphiques (bar, line, pie, scatter) | KPIs et metriques visuelles |
| **Number** | Metrique unique grand format | KPI principal en haut de page |
| **Timeline** | Vue chronologique | Planning et jalons |
| **Button** | Declencheur d'action | Lancer un workflow, ouvrir une URL |

### Patterns d'interface

#### Dashboard operationnel

```
Layout:
- Header: titre + date de derniere mise a jour
- Row 1: 4 Number elements (KPIs: total projets, en cours, en retard, taux de completion)
- Row 2: Chart bar (projets par statut) + Chart pie (projets par departement)
- Row 3: Grid filtree (projets en retard, tries par deadline)
```

#### Portail de soumission

```
Layout:
- Header: logo + titre + instructions
- Body: Form element avec champs conditionels
- Footer: record list (mes soumissions precedentes, filtrees par utilisateur connecte)
```

---

## Integration Patterns

### Airtable API

L'API REST d'Airtable permet les operations CRUD sur les tables.

**Caracteristiques** :
- Base URL : `https://api.airtable.com/v0/{baseId}/{tableName}`
- Authentification : Bearer token (Personal Access Token ou OAuth)
- Rate limit : 5 requetes/seconde par base
- Pagination : 100 records par page, curseur `offset` pour les pages suivantes
- Filtres : parametre `filterByFormula` avec syntaxe Airtable formula

**Limites critiques** :
- 5 requetes/seconde — prevoir du throttling pour les traitements en masse.
- 100 records par requete — paginer pour les tables volumineuses.
- Pas de webhooks natifs entrants — utiliser des automations ou des services tiers pour le temps reel.

### Connecteurs d'integration

| Outil | Type | Forces | Limites |
|---|---|---|---|
| **Zapier** | iPaaS no-code | 7 000+ applications, simple, fiable | Cout par tache, latence (polling), logique limitee |
| **Make (ex-Integromat)** | iPaaS visuel | Scenarios complexes, boucles, conditions, cout avantageux | Courbe d'apprentissage, debugging parfois difficile |
| **n8n** | iPaaS open-source | Self-hosted, gratuit, extensible, code JS | Necessite hebergement, maintenance technique |
| **Airtable Sync** | Natif Airtable | Synchronisation inter-bases temps reel | Unidirectionnel (2-way en beta), meme workspace requis |

### Patterns d'integration recommandes

#### Pattern 1 — CRM to Email Marketing

```
Airtable (Contacts) --> Zapier --> Mailchimp
Trigger: nouveau contact avec "Newsletter = true"
Action: ajouter a la liste Mailchimp correspondante
Enrichissement: tag Mailchimp selon le segment Airtable
```

#### Pattern 2 — Form to Multi-Table

```
Typeform/Tally --> Webhook --> Make --> Airtable
1. Form submission declenche webhook
2. Make parse les donnees
3. Make cherche si le contact existe deja (Find record)
4. Si oui: update record + create linked record (nouvelle demande)
5. Si non: create contact + create linked record
```

#### Pattern 3 — Airtable to Dashboard

```
Airtable --> API --> Google Sheets / Looker Studio
Sync periodique (hourly) via Make ou script
Transformation des donnees pour le format dashboard
Visualisation dans Looker Studio (ex-Data Studio)
```

---

## Formules Airtable — Reference

### Syntaxe de base

Les formules Airtable utilisent une syntaxe similaire a Excel mais avec des specificites propres.

#### Fonctions texte

| Fonction | Syntaxe | Exemple |
|---|---|---|
| Concatenation | `CONCATENATE(str1, str2)` ou `str1 & str2` | `{Prenom} & " " & {Nom}` |
| Majuscules | `UPPER(str)` | `UPPER({Nom})` → "DUPONT" |
| Minuscules | `LOWER(str)` | `LOWER({Email})` |
| Longueur | `LEN(str)` | `LEN({Description})` |
| Substitution | `SUBSTITUTE(str, old, new)` | `SUBSTITUTE({Tel}, " ", "")` |
| Extraction | `MID(str, start, count)` | `MID({Code}, 1, 3)` → 3 premiers caracteres |
| Recherche | `FIND(needle, haystack)` | `FIND("@", {Email})` |

#### Fonctions logiques

| Fonction | Syntaxe | Exemple |
|---|---|---|
| Condition | `IF(test, yes, no)` | `IF({Status} = "Termine", "OK", "En cours")` |
| ET logique | `AND(cond1, cond2)` | `AND({Montant} > 1000, {Status} = "Valide")` |
| OU logique | `OR(cond1, cond2)` | `OR({Priorite} = "Haute", {Deadline} < TODAY())` |
| Branchement | `SWITCH(expr, val1, res1, val2, res2, default)` | `SWITCH({Statut}, "A faire", "Rouge", "En cours", "Orange", "Vert")` |
| Vide | `IF(BLANK({Field}), "N/A", {Field})` | Gestion des champs vides |

#### Fonctions date

| Fonction | Syntaxe | Exemple |
|---|---|---|
| Aujourd'hui | `TODAY()` | Reference a la date du jour |
| Maintenant | `NOW()` | Reference a l'instant present |
| Difference | `DATETIME_DIFF(d1, d2, 'days')` | `DATETIME_DIFF({Deadline}, TODAY(), 'days')` → jours restants |
| Ajout | `DATEADD({Date}, 30, 'days')` | Ajouter 30 jours a une date |
| Format | `DATETIME_FORMAT({Date}, 'DD/MM/YYYY')` | Formatage pour affichage |
| Jour de semaine | `WEEKDAY({Date})` | 0 = dimanche, 6 = samedi |

#### Formules utiles courantes

```
// Jours de retard
IF(AND({Status} != "Termine", {Deadline} < TODAY()),
  DATETIME_DIFF(TODAY(), {Deadline}, 'days') & " jours de retard",
  "Dans les temps"
)

// Priorite calculee
IF(DATETIME_DIFF({Deadline}, TODAY(), 'days') < 3, "Critique",
  IF(DATETIME_DIFF({Deadline}, TODAY(), 'days') < 7, "Haute",
    IF(DATETIME_DIFF({Deadline}, TODAY(), 'days') < 14, "Moyenne", "Basse")
  )
)

// Progression (%) basee sur un rollup
ROUND(
  IF({Total Taches} = 0, 0,
    {Taches Terminees} / {Total Taches} * 100
  ), 0
) & "%"

// Reference unique
"PRJ-" & RIGHT("000" & {Autonumber}, 4)
// Resultat: PRJ-0001, PRJ-0042, PRJ-0153
```

---

## Limites d'Airtable et Strategies de Contournement

### Limites structurelles

| Limite | Valeur (Plan Pro) | Valeur (Enterprise) | Strategie de contournement |
|---|---|---|---|
| Records par base | 50 000 par table | 250 000 par table | Archivage periodique, bases multiples avec sync |
| Champs par table | 500 | 500 | Evaluer si des champs doivent etre dans une table separee |
| Tables par base | 50+ | 50+ | Rarement limitant en pratique |
| Taille d'attachment | 100 MB par fichier | 100 MB par fichier | Stocker les gros fichiers dans Google Drive/S3, lien dans Airtable |
| Automation runs | 25 000/mois | 100 000/mois | Optimiser les triggers, regrouper les actions, utiliser Make/Zapier pour le surplus |
| API rate limit | 5 req/sec | 5 req/sec | Queue et throttling, batch operations |
| Formulas | Pas de cross-table reference | Idem | Utiliser lookup + formula sur le champ lookup |

### Strategies d'optimisation

1. **Archivage actif** : deplacer les records anciens ou resolus vers une base d'archive. Utiliser une automation declenchee par une date ou un statut.
2. **Bases multiples avec Airtable Sync** : diviser les donnees entre plusieurs bases et synchroniser les tables de reference. Permet de depasser les limites par base.
3. **Vues filrees comme "index"** : creer des vues avec des filtres stricts pour limiter le nombre de records charges dans l'interface. Ameliore la performance de l'UI.
4. **Champs formula vs lookup** : preferer les lookups aux formulas complexes. Les lookups sont mis en cache par Airtable, les formulas sont recalculees a chaque affichage.
5. **Attachments externes** : stocker les fichiers volumineux dans un service dedie (Google Drive, Dropbox, S3) et ne mettre qu'un lien URL dans Airtable. Reduit la taille de la base et ameliore les performances.

---

## Alternatives a Airtable

### NocoDB

- **Positionnement** : alternative open-source a Airtable, self-hosted ou cloud.
- **Backend** : se connecte a des bases de donnees existantes (MySQL, PostgreSQL, SQL Server, SQLite). Les donnees restent dans votre base de donnees — NocoDB ajoute une couche visuelle.
- **Forces** : gratuit (self-hosted), pas de limite de records, donnees sous votre controle, API compatible Airtable.
- **Limites** : moins de polish UI, automations moins riches, pas d'Interface Designer equivalent.
- **Quand choisir NocoDB** : donnees sensibles necessitant un hebergement on-premise, volumes superieurs a 100K records, besoin d'acceder aux donnees directement en SQL.

### Baserow

- **Positionnement** : alternative open-source a Airtable, orientee developpeurs et equipes tech.
- **Backend** : PostgreSQL natif, self-hosted ou cloud manage.
- **Forces** : open-source (MIT license), API riche, plugins extensibles, pas de limite de records en self-hosted, formules avancees.
- **Limites** : ecosysteme plus restreint, moins d'integrations natives, communaute plus petite.
- **Quand choisir Baserow** : equipes techniques preferant l'open-source, besoin de customisation poussee, volumes importants.

### Smartsheet

- **Positionnement** : plateforme de gestion de travail collaboratif, orientee entreprise et gestion de projets.
- **Forces** : Gantt natif puissant, gestion de portefeuille de projets, automations robustes, rapports inter-sheets, conformite enterprise (SOC2, FedRAMP).
- **Limites** : modele de donnees moins flexible qu'Airtable (pas de vrais linked records), interface moins intuitive, plus cher.
- **Quand choisir Smartsheet** : gestion de projets complexes avec Gantt et dependances, organisations enterprise avec exigences de conformite, equipes deja sur l'ecosysteme Smartsheet.

### Google Sheets + AppSheet

- **Positionnement** : Google Sheets comme base de donnees avec AppSheet comme couche applicative.
- **Forces** : gratuit (Sheets), integration native Google Workspace, familiarite des utilisateurs, AppSheet ajoute les formulaires, vues mobiles et automations.
- **Limites** : performance degradee au-dela de 10K lignes dans Sheets, pas de vraies relations (simulation par VLOOKUP), concurrence d'acces limitee.
- **Quand choisir** : petits volumes, ecosysteme Google dominant, budget minimal, prototypage rapide.

---

## Bonnes Pratiques de Gouvernance Airtable

### Convention de nommage

Adopter et documenter une convention de nommage coherente pour tous les elements :

- **Bases** : `[Departement] Nom descriptif` (ex. "Sales Pipeline", "HR Recrutement").
- **Tables** : nom pluriel de l'entite en PascalCase ou avec espaces (ex. "Projets", "Ligne de Commande").
- **Champs** : nom descriptif sans abbreviation, prefixer les champs techniques (ex. "_formula_priorite", "_rollup_total").
- **Vues** : `[Usage] Description` (ex. "Dashboard Taches en retard", "Formulaire Nouvelle demande").
- **Automations** : `[Trigger] → [Action] Description` (ex. "Record created → Notify Slack New Project").

### Documentation

Documenter chaque base avec :
- Un README (dans un champ long text d'une table "Documentation" ou dans un document externe).
- Le schema de donnees (tables, relations, champs calcules).
- La liste des automations avec leur logique.
- Les vues principales et leur usage.
- Le proprietaire et les utilisateurs autorises.

### Backup et restauration

- **Snapshots Airtable** : disponibles sur les plans payants, restauration possible mais limitee dans le temps.
- **Export CSV regulier** : automatiser l'export CSV de chaque table via l'API + script cron. Stocker dans Google Drive ou S3.
- **Duplication de base** : dupliquer periodiquement la base entiere comme sauvegarde complete (inclut vues, automations, interfaces).
- **Documentation as Code** : exporter le schema de la base (via API metadata) et le versionner dans un repository Git.

---

## Checklist de Conception d'une Base Airtable

1. **Definir les entites** : lister toutes les entites metier et leurs attributs.
2. **Identifier les relations** : tracer les liens entre entites (1:N, M:N, hierarchiques).
3. **Choisir les types de champs** : assigner le type de champ le plus precis a chaque attribut.
4. **Configurer les linked records** : creer les relations entre tables.
5. **Ajouter les champs calcules** : rollups, lookups, formules pour les donnees derivees.
6. **Creer les vues** : une vue par persona ou par cas d'usage.
7. **Configurer l'access control** : permissions par workspace, base, table et vue.
8. **Mettre en place les automations** : notifications, creations en cascade, mises a jour automatiques.
9. **Importer les donnees** : import CSV/Excel, nettoyage, validation de coherence.
10. **Documenter** : schema, conventions, automations, proprietaire, procedures de backup.
11. **Tester avec des utilisateurs** : feedback sur l'ergonomie, les vues, les formulaires.
12. **Deployer et monitorer** : suivi d'adoption, metriques d'usage, alertes sur les quotas.
