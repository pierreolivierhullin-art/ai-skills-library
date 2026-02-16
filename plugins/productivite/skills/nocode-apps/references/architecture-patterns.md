# Architecture No-Code — Data Model, Securite, Performance, Scalabilite & Gouvernance

## Overview

Ce document de reference couvre les aspects architecturaux des applications no-code : modelisation des donnees, securite et controle d'acces, optimisation de performance, limites de scalabilite, gouvernance organisationnelle, strategies de test, monitoring, sauvegarde et conformite reglementaire. Il fournit les patterns, frameworks et checklists necessaires pour construire des applications no-code de niveau professionnel, maintenables et scalables. Utiliser ce guide comme reference pour chaque decision architecturale, de la conception initiale a la migration eventuelle vers du code.

---

## Architecture de Donnees No-Code

### Patterns de modelisation

#### Pattern 1 — Flat Model (Modele plat)

Toutes les donnees dans une seule table, sans relations.

```
Table: Contacts
| Nom | Email | Entreprise | Adresse Entreprise | Telephone Entreprise | Statut |
```

**Quand l'utiliser** : donnees simples sans repetition (liste de courses, inventaire basique, log d'evenements).

**Limites** :
- Duplication inevitable des donnees (adresse entreprise repetee pour chaque contact de la meme entreprise).
- Incoherences (l'adresse de l'entreprise A est differente dans deux records).
- Mise a jour penible (changer l'adresse de l'entreprise necessite de modifier tous les records concernes).
- Performance degradee avec le volume (recherche sur des colonnes non indexees).

**Verdict** : acceptable uniquement pour les tables de moins de 500 records sans donnees relationnelles. Migrer vers un modele relationnel des que la complexite augmente.

#### Pattern 2 — Relational Model (Modele relationnel)

Donnees separees en tables distinctes liees par des relations.

```
Table: Contacts               Table: Entreprises
| Nom | Email | Entreprise* |  | Nom | Adresse | Telephone | Secteur |
                    |                      ^
                    +--- linked record ----+

Table: Interactions
| Date | Type | Contact* | Notes |
            |
            +--- linked to Contacts
```

**Quand l'utiliser** : tout projet serieux avec des donnees qui ont des relations entre elles.

**Avantages** :
- Pas de duplication — chaque information est stockee une seule fois.
- Coherence garantie — modifier l'adresse de l'entreprise se fait en un seul endroit.
- Requetes puissantes — rollups, lookups, filtres sur les relations.
- Scalabilite — le modele se complexifie sans degrader la qualite des donnees.

**Implementation en Airtable** :
- Utiliser les linked record fields pour materialiser les relations.
- Ajouter des lookups pour afficher les champs de la table liee dans la table courante.
- Ajouter des rollups pour agreger les donnees des records lies (COUNT, SUM, AVG).

#### Pattern 3 — Hub-and-Spoke (Etoile)

Une table centrale (hub) liee a plusieurs tables satellites (spokes).

```
                    Table: Documents
                         |
Table: Taches ----> Table: Projets <---- Table: Commentaires
                         |
                    Table: Equipe
                         |
                    Table: Budget
```

**Quand l'utiliser** : applications de gestion ou une entite centrale (Projet, Client, Produit) est enrichie par des entites satellites.

**Avantages** :
- Structure claire et intuitive — tout gravite autour de l'entite principale.
- Navigation naturelle — depuis le hub, on accede a toutes les informations satellites.
- Reporting simple — les rollups sur le hub agregent les donnees de tous les spokes.

#### Pattern 4 — Normalized with Junction Tables

Modele pleinement normalise avec des tables de jonction pour les relations many-to-many.

```
Table: Projets           Table: Projet_Membres (junction)      Table: Employes
| Nom | Statut |    <-->  | Projet* | Employe* | Role |  <-->  | Nom | Poste |
                          | Projet A | Marie   | Lead  |
                          | Projet A | Jean    | Dev   |
                          | Projet B | Marie   | Reviewer |
```

**Quand l'utiliser** : relations many-to-many ou chaque relation porte des attributs propres (role dans le projet, date d'affectation, pourcentage d'allocation).

**Avantages** :
- Modelisation fidele de la realite metier.
- Attributs de relation stockes proprement.
- Requetes et filtres sur les attributs de la relation.

**Attention** : les tables de jonction augmentent la complexite du modele. Ne les utiliser que quand les relations sont reellement many-to-many et/ou portent des attributs.

### Erreurs de modelisation frequentes

| Erreur | Symptome | Solution |
|---|---|---|
| **Champ multi-select au lieu de linked record** | On utilise un multiple select pour stocker des references a d'autres entites | Remplacer par un linked record field vers une table dediee |
| **Colonnes repetitives** | `Tache_1`, `Tache_2`, `Tache_3` dans une table Projets | Creer une table Taches liee a Projets par linked record |
| **Donnees dans le nom du champ** | Colonnes `Jan_2025`, `Fev_2025`, `Mar_2025` | Creer une table de donnees temporelles avec une colonne Date et une colonne Valeur |
| **Table unique pour tout** | Une table de 50+ colonnes avec un champ "Type" pour distinguer les entites | Separer en tables distinctes par entite |
| **Donnees dupliquees** | L'adresse du client est saisie manuellement dans chaque commande | Utiliser un linked record vers la table Clients + lookup pour l'adresse |
| **Pas de primary field significatif** | Le primary field est un autonumber ou un champ generique | Definir un primary field descriptif (nom + identifiant unique) |

---

## Securite et Access Control

### Modele RBAC (Role-Based Access Control)

Le RBAC est le modele de controle d'acces standard pour les applications no-code. Il repose sur l'attribution de roles aux utilisateurs, chaque role definissant un ensemble de permissions.

#### Definition des roles typiques

| Role | Description | Permissions typiques |
|---|---|---|
| **Super Admin** | Administrateur global de la plateforme | Tout : creation/suppression de tables, gestion des utilisateurs, configuration |
| **Admin** | Administrateur d'une application ou d'un domaine | CRUD sur toutes les donnees du domaine, gestion des vues, automations |
| **Manager** | Responsable d'une equipe ou d'un processus | CRUD sur les donnees de son equipe, lecture sur les donnees globales, approbation |
| **Editor** | Contributeur principal | Creation et modification de ses propres records, lecture des records partages |
| **Viewer** | Consultation uniquement | Lecture seule sur les donnees autorisees, pas de creation ni de modification |
| **External** | Utilisateur externe (client, fournisseur, partenaire) | Lecture/creation limitee a ses propres donnees, pas d'acces aux donnees internes |

#### Implementation par plateforme

**Airtable** :
- Permissions au niveau du workspace (owner, creator, editor, commenter, viewer).
- Permissions au niveau de la base (memes niveaux).
- Vues personnelles vs vues partagees — les vues personnelles ne sont visibles que par leur createur.
- Interface Designer : permissions par interface (qui peut voir quelle interface).
- Limitation : pas de permissions au niveau du champ dans les vues grille (possible dans Interface Designer).

**Bubble** :
- Privacy Rules au niveau des data types — definissent qui peut voir, trouver, modifier, supprimer chaque type de donnees.
- Page-level conditions — certaines pages ne sont accessibles que si une condition est remplie (ex. Current User's Role = Admin).
- Element-level conditions — afficher/masquer des elements selon le role de l'utilisateur.
- Workflow conditions — empecher l'execution d'un workflow si l'utilisateur n'a pas le bon role.

**Softr** :
- User Groups — chaque utilisateur appartient a un ou plusieurs groupes.
- Page-level permissions — chaque page est attribuee a des groupes.
- Data filtering — les donnees affichees sont filtrees automatiquement selon l'utilisateur connecte.
- Block-level visibility — les blocks individuels peuvent etre visibles ou masques selon le groupe.

**Retool** :
- Permission Groups — groupes de permissions (Admin, Editor, Viewer) par application.
- Page-level permissions — restriction d'acces par page.
- Component-level permissions — desactiver ou masquer des composants selon le groupe.
- Query-level permissions — restreindre l'execution de certaines queries (DELETE, UPDATE) a certains groupes.

### Principes de securite

#### Principe du moindre privilege (Least Privilege)

Chaque utilisateur doit avoir uniquement les permissions necessaires a l'execution de ses taches, et rien de plus. Ne jamais donner un acces administrateur "au cas ou". Commencer avec le minimum de permissions et ajouter au besoin.

#### Separation des environnements

Maintenir des environnements separes pour le developpement, le test et la production. Ne jamais tester de nouvelles fonctionnalites directement dans l'environnement de production. En no-code, cela se traduit par :
- Airtable : base de developpement separee, synchronisee avec la production pour les donnees de reference.
- Bubble : environnement "Development" vs "Live" avec deploiement controle.
- Retool : staging environment avec deploiement via Git.

#### Audit trail

Tracer qui fait quoi et quand dans l'application :
- Airtable : champs Created by, Last modified by, Created time, Last modified time sur chaque table.
- Bubble : logs natifs (Server Logs, Application Logs), custom logging via creation de records dans une table Logs.
- Retool : audit logs natifs (qui a execute quelle query, quand).

#### Gestion des secrets

- Ne jamais stocker de cles API, mots de passe ou tokens dans les champs de donnees visibles.
- Utiliser les "secrets" ou "environment variables" fournis par la plateforme (Retool Secrets, Bubble API keys).
- Pour les automations, utiliser les credentials stockees de maniere securisee dans la plateforme d'integration (Make, Zapier).
- Chiffrer les donnees sensibles au repos si la plateforme le supporte (Airtable Enterprise, Bubble Dedicated).

---

## Optimisation de Performance

### Principes generaux

Les applications no-code ont des contraintes de performance specifiques liees aux plateformes sous-jacentes. Comprendre ces contraintes et optimiser en consequence est essentiel pour une experience utilisateur fluide.

### Optimisation par couche

#### Couche donnees

1. **Limiter le nombre de records charges** : utiliser des filtres pour ne charger que les donnees necessaires. Ne jamais afficher une vue non filtree sur une table de plus de 1 000 records.
2. **Indexer les champs de recherche** : dans Bubble et Retool, s'assurer que les champs frequemment utilises dans les filtres sont indexes.
3. **Archiver les donnees anciennes** : deplacer les records anciens ou resolus vers une table ou base d'archive pour maintenir la table principale legere.
4. **Optimiser les formules** : les formules complexes (imbrications de IF, DATETIME_DIFF sur tous les records) ralentissent le chargement. Preferer les lookups et rollups aux formules quand c'est possible.
5. **Eviter les champs attachment volumineux** : les fichiers attaches sont charges avec le record. Stocker les fichiers volumineux dans un service externe (S3, Google Drive) et ne garder que le lien.

#### Couche logique

1. **Limiter les automations simultanees** : trop d'automations declenchees par le meme evenement creent des conflits et des ralentissements. Regrouper les actions dans une seule automation quand c'est possible.
2. **Eviter les boucles recursives** : une automation qui modifie un record qui declenche une autre automation qui modifie le meme record = boucle infinie. Utiliser des champs flags ("_automation_processed") pour eviter les re-declenchements.
3. **Optimiser les scripts** : dans Retool et Airtable, les scripts ont des timeouts stricts (30 secondes). Optimiser les boucles, limiter les appels API dans les scripts.
4. **Batch operations** : regrouper les operations (create, update) en batch plutot que de les executer une par une. L'API Airtable supporte jusqu'a 10 records par requete de creation/modification.

#### Couche presentation

1. **Limiter les elements par page** : dans Bubble, chaque element sur la page consomme des ressources. Viser moins de 50 elements visibles simultanement.
2. **Lazy loading** : charger les donnees au fur et a mesure que l'utilisateur scrolle ou navigue, pas tout d'un coup au chargement de la page.
3. **Compression des images** : compresser les images avant de les uploader. Utiliser des formats modernes (WebP) et des tailles adaptees (pas de photo 4K pour une miniature de 200px).
4. **Pagination** : paginer les listes longues plutot que d'afficher tous les records. 20-50 records par page est un bon compromis.
5. **Caching** : utiliser les mecanismes de cache de la plateforme (Retool caching, Bubble repeating group pagination) pour eviter les requetes repetees.

### Benchmarks de performance par plateforme

| Plateforme | Chargement page (cible) | Records max sans degradation | Utilisateurs simultanes | Notes |
|---|---|---|---|---|
| **Airtable** | < 3s | 10 000 par vue | 50 (plan Pro) | Degradation notable au-dela de 20K records par table |
| **Retool** | < 2s | 100 000+ (SQL) | 100+ | Performance liee a la base de donnees sous-jacente |
| **Glide** | < 2s | 25 000 | 100 | Degradation avec Google Sheets > 5K rows |
| **AppSheet** | < 3s | 50 000 | 100 | Performance liee a la source (Sheets vs Cloud SQL) |
| **Bubble** | < 3-5s | 100 000+ | Variable | Tres sensible a l'optimisation — peut etre lent si mal configure |
| **Softr** | < 2s | Limites Airtable | Illimite (CDN) | Les pages statiques sont rapides, les blocs dynamiques dependent d'Airtable |

---

## Limites de Scalabilite et Strategies

### Limites structurelles des plateformes

| Limite | Airtable | Bubble | Retool | Impact |
|---|---|---|---|---|
| **Records** | 50K/table (Pro), 250K (Enterprise) | Illimite (mais performance) | Illimite (SQL) | Bloquant pour les applications a fort volume |
| **Utilisateurs** | Selon plan | Selon plan + workload | Par siege | Cout lineaire avec les utilisateurs |
| **Automations** | 25K runs/mois (Pro) | Workload units | Illimite (Enterprise) | Bloquant pour les applications a haute frequence |
| **API** | 5 req/sec | Selon plan | Illimite | Bloquant pour les integrations temps reel |
| **Stockage** | 20GB (Pro) | Selon plan | N/A | Bloquant pour les applications avec beaucoup de fichiers |
| **Complexite logique** | Formules + scripts limites | Workflows illimites | JS illimite | Bloquant pour la logique metier complexe |

### Strategies de scalabilite

#### Strategie 1 — Sharding horizontal (multi-bases)

Diviser les donnees entre plusieurs bases Airtable en utilisant la synchronisation inter-bases.

```
Base: CRM Actif (< 50K records)
  - Clients actifs
  - Opportunites en cours
  - Contacts recents

Base: CRM Archive (< 50K records)
  - Clients inactifs
  - Opportunites fermees (> 6 mois)
  - Contacts anciens

Base: CRM Reporting
  - Tables de reference synchronisees
  - Vues de reporting aggregees
```

#### Strategie 2 — Architecture hybride (no-code + code)

Utiliser le no-code pour l'interface et la logique simple, et du code pour les traitements lourds.

```
[Interface Softr / Retool]
       |
[Airtable (donnees operationnelles)]
       |
[API custom (Node.js/Python)]
       |
[PostgreSQL (donnees historiques, analytics)]
```

**Cas d'usage** : l'interface utilisateur reste en no-code (rapide a modifier), mais les calculs complexes, les traitements de masse et le stockage volumineux sont geres par du code.

#### Strategie 3 — Migration progressive vers du code

Migrer les composants qui atteignent les limites de la plateforme, tout en conservant le reste en no-code.

**Approche** :
1. Identifier le composant qui atteint ses limites (base de donnees, logique, performance).
2. Reconstruire ce composant en code (ex. migrer la base Airtable vers PostgreSQL).
3. Connecter le composant code au reste de l'application no-code via API.
4. Tester la coexistence.
5. Iterer sur les autres composants si necessaire.

---

## Framework de Gouvernance No-Code

### Pilier 1 — Conventions de nommage

Definir et documenter des conventions de nommage pour tous les elements :

| Element | Convention | Exemple |
|---|---|---|
| **Workspace** | `[Organisation] Domaine` | "Acme Sales", "Acme HR" |
| **Base** | `Domaine - Nom descriptif` | "Sales - Pipeline Commercial" |
| **Table** | Nom pluriel, PascalCase | "Projets", "LignesDeCommande" |
| **Champ** | Nom descriptif, prefixe technique | "Nom", "Email", "_formula_priorite", "_rollup_total" |
| **Vue** | `[Type] Description (Persona)` | "Dashboard Taches en retard (Manager)" |
| **Automation** | `[Trigger] → [Action] Description` | "Record created → Slack Notify New Project" |
| **Interface** | `[Type] Nom (Audience)` | "Dashboard KPI (Direction)" |

### Pilier 2 — Documentation

Chaque application no-code doit avoir une documentation minimale :

#### Fiche application

```
# [Nom de l'application]

## Informations generales
- Proprietaire: [Nom + role]
- Date de creation: [date]
- Derniere mise a jour: [date]
- Plateforme: [Airtable / Bubble / Retool / etc.]
- Criticite: [Haute / Moyenne / Basse]
- Nombre d'utilisateurs: [nombre]

## Objectif
[Description en 2-3 phrases du probleme resolu]

## Schema de donnees
[Diagramme ou liste des tables, champs et relations]

## Automations
| Nom | Trigger | Actions | Frequence |
|-----|---------|---------|-----------|

## Integrations
| Systeme | Type | Direction | Frequence |
|---------|------|-----------|-----------|

## Access control
| Role | Permissions | Utilisateurs |
|------|-------------|-------------|

## Procedures
- Backup: [frequence et methode]
- Restauration: [procedure]
- Support: [contact et processus]
```

### Pilier 3 — Ownership

Chaque application doit avoir un proprietaire clairement identifie :

- **Owner** : responsable de l'application, de sa maintenance et de son evolution. C'est le point de contact unique pour les questions et les problemes.
- **Bus factor** : au minimum 2 personnes doivent connaitre chaque application critique. Documenter et former un backup pour chaque owner.
- **Transfert de propriete** : quand un owner quitte l'equipe, un transfert formel doit avoir lieu (documentation, formation, mise a jour des accreditations).

### Pilier 4 — Lifecycle Management

Definir un cycle de vie pour chaque application :

```
1. Proposition → Evaluation du besoin, choix de plateforme
2. Construction → Developpement, tests, documentation
3. Deploiement → Formation, lancement, monitoring initial
4. Exploitation → Usage quotidien, support, mises a jour mineures
5. Evolution → Nouvelles fonctionnalites, integrations, optimisations
6. Revue → Evaluation annuelle : toujours pertinent ? A optimiser ? A migrer ?
7. Decommissionnement → Export des donnees, archivage, suppression
```

### Pilier 5 — Catalogue d'applications

Maintenir un catalogue centralise de toutes les applications no-code de l'organisation :

| Application | Plateforme | Owner | Criticite | Utilisateurs | Derniere revue |
|---|---|---|---|---|---|
| CRM Commercial | Airtable | Marie D. | Haute | 25 | 2025-12 |
| Portail Client | Softr | Jean P. | Haute | 200 | 2025-11 |
| Tracker RH | Airtable | Sophie L. | Moyenne | 10 | 2025-10 |
| Formulaire NPS | Tally | Marc R. | Basse | N/A | 2025-09 |

---

## Strategies de Test en No-Code

### Niveaux de test

#### Test 1 — Validation du modele de donnees

Avant de construire les interfaces, valider que le modele de donnees est correct :

- [ ] Chaque entite metier a sa propre table.
- [ ] Les relations sont materialisees par des linked records (pas des champs texte).
- [ ] Les champs ont le bon type (date, nombre, select, pas tout en texte).
- [ ] Les champs obligatoires sont configures.
- [ ] Les valeurs par defaut sont definies.
- [ ] Les rollups et lookups retournent les bonnes valeurs.
- [ ] Les formules calculent correctement (tester avec des cas limites : 0, negatif, vide, null).

#### Test 2 — Test des automations

Chaque automation doit etre testee individuellement :

- [ ] Le trigger se declenche correctement (creer/modifier un record de test).
- [ ] Les conditions filtrent correctement (tester les cas positifs et negatifs).
- [ ] Les actions produisent le resultat attendu (verifier les records crees/modifies, les emails envoyes, les webhooks appeles).
- [ ] Les cas limites sont geres (champs vides, valeurs extremes, records lies absents).
- [ ] Les erreurs sont gerees gracieusement (pas de crash silencieux, notification en cas d'erreur).

#### Test 3 — Test de l'interface utilisateur

Tester chaque ecran et chaque interaction :

- [ ] Les donnees affichees sont correctes et a jour.
- [ ] Les filtres et tris fonctionnent comme attendu.
- [ ] Les formulaires valident correctement les saisies.
- [ ] Les boutons declenchent les bonnes actions.
- [ ] L'acces est correctement restreint par role (tester avec un compte viewer, editor, admin).
- [ ] L'experience mobile est fonctionnelle (tester sur smartphone et tablette).
- [ ] Les messages d'erreur sont clairs et utiles.

#### Test 4 — Test de charge

Pour les applications critiques, tester la performance sous charge :

- [ ] Charger la page principale avec le volume de donnees de production.
- [ ] Simuler des soumissions de formulaire simultanees.
- [ ] Verifier que les automations n'atteignent pas les quotas en conditions normales.
- [ ] Mesurer le temps de chargement des pages les plus lourdes.
- [ ] Identifier les goulots d'etranglement (vues non filtrees, formules complexes, images lourdes).

### Test continu

- **Apres chaque modification** : tester la fonctionnalite modifiee et les fonctionnalites adjacentes.
- **Avant chaque deploiement** : parcourir les scenarios critiques (smoke test).
- **Mensuellement** : verifier les automations (execution, quotas, erreurs), les integrations (connectivite, donnees synchronisees) et les performances (temps de chargement).

---

## Monitoring et Alertes

### Metriques a monitorer

| Metrique | Source | Seuil d'alerte | Action |
|---|---|---|---|
| **Automation runs restants** | Dashboard Airtable | < 20% du quota mensuel | Optimiser les triggers ou upgrader le plan |
| **Nombre de records** | Table info Airtable | > 80% de la limite | Archiver ou sharding |
| **Erreurs d'automation** | Logs d'automation | > 5 erreurs/jour | Diagnostiquer et corriger |
| **Temps de chargement** | Test manuel / monitoring | > 5 secondes | Optimiser les vues et les donnees |
| **Taux d'adoption** | Login tracking | < 50% de l'equipe cible | Formation et communication |
| **Integrations en erreur** | Dashboard Make/Zapier | Toute erreur | Corriger immediatement |
| **Stockage utilise** | Dashboard plateforme | > 80% du quota | Nettoyer les attachments ou upgrader |

### Outils de monitoring

- **Airtable** : dashboard d'automations (runs, erreurs), revision history, audit logs (Enterprise).
- **Bubble** : Server Logs, Application Logs, capacity usage dashboard.
- **Retool** : audit logs, query performance metrics, error tracking.
- **Make / Zapier** : dashboard d'execution, alertes sur erreurs, historique des runs.
- **UptimeRobot / Better Uptime** : monitoring de disponibilite des portails et applications publiques.

---

## Backup et Disaster Recovery

### Strategies de backup

#### Backup des donnees

| Methode | Frequence | Retention | Plateformes |
|---|---|---|---|
| **Export CSV manuel** | Hebdomadaire | 3 mois | Toutes |
| **Export CSV automatise (API + script)** | Quotidien | 6 mois | Airtable, Bubble, Retool |
| **Airtable Snapshot** | Automatique | 1 an (Enterprise) | Airtable |
| **Duplication de base** | Mensuel | 3 mois | Airtable |
| **Database backup SQL** | Quotidien | 30 jours | Retool (source SQL), Bubble (Dedicated) |
| **Export Bubble** | Mensuel | 6 mois | Bubble |

#### Backup de la configuration

- **Airtable** : exporter le schema de la base via l'API Metadata. Documenter les automations et les interfaces manuellement.
- **Bubble** : utiliser la fonctionnalite "Copy to another app" pour dupliquer l'application complete. Exporter les settings et les API keys.
- **Retool** : utiliser le Git Sync pour versionner les applications dans un repository Git.

### Plan de reprise d'activite (PRA)

Definir un plan de reprise pour chaque application critique :

```
Application: [Nom]
Criticite: [Haute / Moyenne / Basse]

Scenarios de panne:
1. Panne de la plateforme (Airtable/Bubble down)
   - Impact: [description]
   - RTO (Recovery Time Objective): [duree]
   - RPO (Recovery Point Objective): [duree]
   - Action: attendre la resolution, communiquer aux utilisateurs

2. Suppression accidentelle de donnees
   - Impact: [description]
   - RTO: 2h
   - RPO: 24h (dernier backup)
   - Action: restaurer depuis le dernier backup CSV/snapshot

3. Corruption de la configuration (automation cassee, vue modifiee)
   - Impact: [description]
   - RTO: 4h
   - RPO: derniere documentation valide
   - Action: reconfigurer depuis la documentation, restaurer depuis la duplication de base

4. Depart du proprietaire de l'application
   - Impact: [description]
   - RTO: 1 semaine
   - Action: transfert au backup owner, consulter la documentation
```

---

## Conformite Reglementaire

### GDPR (RGPD)

Les applications no-code manipulant des donnees personnelles de residents de l'UE doivent respecter le RGPD :

#### Checklist GDPR pour applications no-code

- [ ] **Registre des traitements** : l'application est documentee dans le registre des traitements de l'organisation.
- [ ] **Base legale** : la base legale du traitement est identifiee (consentement, contrat, interet legitime).
- [ ] **Minimisation** : seules les donnees necessaires sont collectees et stockees.
- [ ] **Duree de conservation** : une duree de conservation est definie et automatisee (archivage/suppression automatique).
- [ ] **Droits des personnes** : les processus de reponse aux demandes d'acces, rectification, suppression et portabilite sont documentes.
- [ ] **Sous-traitant** : un DPA (Data Processing Agreement) est signe avec chaque plateforme et chaque outil d'integration.
- [ ] **Hebergement** : l'hebergement des donnees est compatible avec les exigences de l'organisation (UE, France, etc.).
- [ ] **Chiffrement** : les donnees sensibles sont chiffrees au repos et en transit.
- [ ] **Access control** : l'acces aux donnees personnelles est restreint aux personnes autorisees (RBAC).
- [ ] **Audit trail** : les acces et modifications aux donnees personnelles sont traces.

#### Localisation des donnees par plateforme

| Plateforme | Hebergement standard | Option UE | DPA disponible |
|---|---|---|---|
| **Airtable** | USA (AWS) | Non (Enterprise: possible) | Oui |
| **Bubble** | USA (AWS) | Non (Dedicated: choix de region) | Oui |
| **Retool** | USA (AWS) | Self-hosted possible (on-premise EU) | Oui |
| **Softr** | USA (AWS) | Non | Oui |
| **Glide** | USA (GCP) | Non | Oui |
| **AppSheet** | GCP (variable) | Option GCP EU | Oui (via Google) |
| **Tally** | EU (Belgique) | Natif EU | Oui |
| **Typeform** | USA / EU (option) | Oui (Data Residency) | Oui |

### SOC 2

Pour les applications no-code traitant des donnees clients ou financieres, la conformite SOC 2 de la plateforme peut etre requise :

| Plateforme | SOC 2 Type II | Notes |
|---|---|---|
| **Airtable** | Oui | Rapport disponible sur demande |
| **Bubble** | Non | Pas de certification SOC 2 actuellement |
| **Retool** | Oui | Rapport disponible, option on-premise pour controle total |
| **Softr** | Non | Pas de certification SOC 2 actuellement |
| **Glide** | Non | En cours de certification |
| **AppSheet** | Oui (via Google Cloud) | Couvert par les certifications Google Cloud |

---

## Migration No-Code vers Code

### Quand migrer

La migration du no-code vers le code est justifiee quand :

1. **Limites de performance** : l'application est lente malgre les optimisations, le volume de donnees depasse les capacites de la plateforme.
2. **Limites fonctionnelles** : la logique metier requise depasse les capacites de la plateforme (algorithmes complexes, traitements temps reel, calculs intensifs).
3. **Couts prohibitifs** : le cout de la plateforme a l'echelle (par utilisateur, par record, par automation) depasse le cout de maintenance d'une application codee.
4. **Exigences de securite** : les exigences de securite ou de conformite ne peuvent pas etre satisfaites par la plateforme (certifications specifiques, hebergement sur site).
5. **Vendor lock-in inacceptable** : la dependance a la plateforme represente un risque strategique inacceptable (fermeture du service, changement de pricing).

### Quand NE PAS migrer

- L'application fonctionne bien et repond aux besoins actuels et previsibles.
- L'equipe n'a pas les competences de developpement pour maintenir une application codee.
- Le cout de migration (temps, budget, risque) depasse les benefices attendus.
- L'application est temporaire ou non critique.

### Approche de migration recommandee

#### Phase 1 — Audit et planification
1. Documenter exhaustivement l'application no-code : modele de donnees, logique metier, workflows, integrations, utilisateurs, permissions.
2. Identifier les composants a migrer en priorite (bottlenecks) vs ceux qui peuvent rester en no-code.
3. Choisir la stack technologique cible (framework frontend, backend, base de donnees).
4. Estimer l'effort de migration (temps, equipe, budget).
5. Definir le plan de coexistence temporaire.

#### Phase 2 — Construction parallele
6. Construire la base de donnees cible (PostgreSQL, MySQL) et migrer le schema de donnees.
7. Construire les API backend qui repliquent la logique metier de l'application no-code.
8. Construire l'interface frontend qui reproduit les ecrans et les interactions.
9. Mettre en place la synchronisation de donnees entre l'ancienne et la nouvelle application.
10. Tester en parallele (les deux applications traitent les memes donnees).

#### Phase 3 — Bascule progressive
11. Migrer les utilisateurs par groupe (equipe pilote → generalisation).
12. Maintenir l'ancienne application en lecture seule pendant la transition.
13. Verifier la coherence des donnees apres migration.
14. Decommissionner l'ancienne application apres la periode de transition (30-90 jours).
15. Documenter la nouvelle application et former les equipes de maintenance.

### Anti-patterns de migration

- **Big Bang** : migrer tout d'un coup sans periode de coexistence. Risque de perte de donnees et de fonctionnalites manquantes.
- **Migration sans specifications** : reconstruire l'application sans documenter l'existant. Le resultat sera incomplet et les utilisateurs insatisfaits.
- **Over-engineering** : profiter de la migration pour ajouter des fonctionnalites non demandees. La migration doit reproduire l'existant, pas le reinventer.
- **Ignorer les utilisateurs** : ne pas impliquer les utilisateurs finaux dans la validation de la nouvelle application. Ils connaissent les subtilites et les cas limites.

---

## Checklist Architecture No-Code

### Avant le build

- [ ] Probleme metier clairement defini et documente.
- [ ] Utilisateurs cibles identifies (personas, nombre, devices).
- [ ] Modele de donnees concu (entites, relations, champs, types).
- [ ] Plateforme choisie et justifiee (criteres documentes).
- [ ] Limites de la plateforme evaluees (records, users, automations).
- [ ] Access control defini (roles, permissions).
- [ ] Conventions de nommage definies et documentees.

### Pendant le build

- [ ] Modele de donnees implemente avec les bons types de champs et les relations.
- [ ] Vues configurees par persona / cas d'usage.
- [ ] Automations testees individuellement (trigger, conditions, actions).
- [ ] Integrations configurees et testees (webhooks, API, connecteurs).
- [ ] Access control configure et teste (tester avec chaque role).
- [ ] Documentation maintenue a jour (schema, automations, regles metier).

### Apres le deploiement

- [ ] Utilisateurs formes.
- [ ] Monitoring en place (adoption, erreurs, quotas, performance).
- [ ] Procedure de backup definie et active.
- [ ] Plan de reprise d'activite documente.
- [ ] Conformite GDPR verifiee (registre, DPA, droits des personnes).
- [ ] Revue trimestrielle planifiee (usage, performance, evolution).
- [ ] Owner et backup owner identifies et documentes.
