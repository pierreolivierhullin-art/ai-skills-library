---
name: nocode-apps
description: This skill should be used when the user asks about "no-code development", "low-code platform", "Airtable", "Retool", "Glide", "AppSheet", "Bubble", "Softr", "internal tools", "visual database", "no-code app builder", "citizen development", "business applications", "forms advanced", "Tally forms", "Typeform", "portals", "applications internes", "développement sans code", "bases de données visuelles", "applications métier", "outils internes", "formulaires avancés", "prototypage rapide", "MVP no-code", "client portal", discusses no-code/low-code application development, visual databases, or needs guidance on building internal tools, forms, and business applications without coding.
version: 1.0.0
last_updated: 2026-02
---

# Applications No-Code / No-Code Applications

## Overview

Ce skill couvre l'ensemble des disciplines liees au developpement d'applications sans code et a faible code. Il fournit un cadre structure pour concevoir, construire et deployer des applications metier en utilisant des plateformes visuelles : Airtable pour les bases de donnees relationnelles et la gestion de donnees, Retool pour les outils internes SQL-natifs, Glide pour les applications mobiles, AppSheet pour l'ecosysteme Google, Bubble pour les applications web full-stack, Softr pour les portails clients, Tally et Typeform pour les formulaires avances. Le no-code represente la democratisation du developpement applicatif — il permet aux utilisateurs metier (citizen developers) de construire leurs propres solutions sans dependre d'une equipe technique, tout en maintenant un niveau de qualite et de gouvernance professionnel. Appliquer systematiquement les principes decrits ici pour guider chaque decision de conception, en privilegiant le probleme metier avant la plateforme, le modele de donnees avant l'interface, et l'iteration rapide avec les utilisateurs finaux avant le deploiement a grande echelle.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Applications internes** : CRM custom, project tracker, asset management, employee directory, knowledge base, helpdesk interne, outils de gestion de stock.
- **Portails clients et fournisseurs** : portails self-service, suivi de commandes, soumission de documents, espaces collaboratifs, dashboards partages.
- **MVP et prototypage rapide** : validation d'hypotheses produit, proof of concept, demarche Lean Startup appliquee aux outils internes, hackathons.
- **Formulaires avances et workflows** : formulaires conditionnels, calculs integres, upload de fichiers, paiements, approbations multi-niveaux, formulaires multi-etapes.
- **Bases de donnees visuelles** : structuration de donnees relationnelles, vues multiples (grille, kanban, calendrier, galerie), champs calcules et liens entre tables.
- **Automatisation metier** : workflows declenchees par des evenements, notifications conditionnelles, synchronisation de donnees inter-applications.
- **Dashboards operationnels** : tableaux de bord temps reel, reporting visuel, KPI tracking, vues consolidees multi-sources.
- **Intranets et portails d'equipe** : pages d'accueil equipe, annuaires, bibliotheques de ressources, espaces projets.

## Core Principles

### Principle 1 — Problem First, Platform Second
Ne jamais choisir une plateforme no-code avant d'avoir clairement defini le probleme metier a resoudre. Commencer par documenter le besoin, les utilisateurs cibles, les flux de donnees et les contraintes. La plateforme est un moyen, pas une fin. Un mauvais choix de plateforme entraine des migrations couteuses et des limitations frustrantes.

### Principle 2 — Start with the Data Model
Toute application no-code repose sur un modele de donnees. Concevoir le schema relationnel avant de construire l'interface. Identifier les entites, les relations (one-to-many, many-to-many), les champs obligatoires et les regles de validation. Un modele de donnees bien concu simplifie tout le reste — un modele mal concu genere une dette technique impossible a rembourser.

### Principle 3 — Build for the End User
Concevoir chaque ecran, formulaire et vue en pensant a l'utilisateur final, pas au constructeur. Tester avec de vrais utilisateurs des la premiere iteration. Privilegier la simplicite et la clarte : chaque ecran doit avoir un objectif unique et evident. L'adoption est le seul KPI qui compte — une application parfaite que personne n'utilise est un echec.

### Principle 4 — Iterate Fast with Real Users
Deployer une premiere version minimale en jours, pas en semaines. Collecter du feedback reel, mesurer l'usage, iterer rapidement. Le no-code permet des cycles de build-measure-learn de quelques heures. Exploiter cet avantage au maximum. Ne jamais attendre d'avoir une version "complete" pour la montrer aux utilisateurs.

### Principle 5 — Plan for Scale from Day One
Anticiper les limites de la plateforme choisie : nombre de lignes, nombre d'utilisateurs, volume d'automations, couts par utilisateur. Concevoir l'architecture pour pouvoir migrer ou etendre sans tout reconstruire. Documenter les dependances et les points de couplage. Le succes d'un outil no-code cree une demande que la plateforme initiale ne peut pas toujours absorber.

### Principle 6 — Governance & Maintainability
Traiter les applications no-code avec le meme serieux que les applications codees. Documenter chaque application (objectif, proprietaire, schema de donnees, automations). Definir des conventions de nommage, des standards d'access control et des procedures de backup. Sans gouvernance, le no-code devient du "shadow IT" incontrole.

## Key Frameworks & Methods

### Platform Selection Matrix

| Critere | Airtable | Retool | Glide | AppSheet | Bubble | Softr |
|---|---|---|---|---|---|---|
| **Type principal** | Base de donnees visuelle | Outils internes | Apps mobiles | Apps Google-native | Apps web full-stack | Portails & sites |
| **Complexite** | Faible-Moyenne | Moyenne-Elevee | Faible | Moyenne | Elevee | Faible |
| **Backend** | Natif (tables) | SQL/API externe | Sheets/Airtable | Sheets/SQL | Natif (BDD) | Airtable/Sheets |
| **Mobile** | Responsive | Limite | Natif mobile | Natif mobile | Responsive | Responsive |
| **Automations** | Integrees | Scripts JS | Limitees | Bots integres | Workflows natifs | Via Zapier/Make |
| **Prix/utilisateur** | $$$  | $$$$ | $$ | $$$ | $$$$ | $$ |
| **Cas d'usage ideal** | CRM, tracker, base collaborative | Admin panels, dashboards internes | Apps terrain, collecte mobile | Apps Google Workspace | SaaS, marketplace, app complexe | Portails clients, intranets |
| **Courbe d'apprentissage** | 2-5 jours | 5-15 jours | 1-3 jours | 3-7 jours | 15-30 jours | 1-3 jours |

### Data Model Patterns

- **Flat Model** : une seule table avec tous les champs. Adapte uniquement pour les cas simples (liste de contacts, inventaire basique). Limite : duplication de donnees, incoherences.
- **Relational Model** : tables liees par des relations (linked records dans Airtable, foreign keys dans Retool). Standard recommande pour toute application serieuse. Permet les rollups, lookups et agregations.
- **Hub-and-Spoke** : une table centrale (ex. Projets) avec des tables satellites liees (Taches, Documents, Commentaires). Pattern le plus frequent pour les applications de gestion.
- **Many-to-Many with Junction Table** : pour les relations complexes (ex. Employes <-> Competences). Utiliser une table de jonction intermediaire pour modeliser la relation.

### No-Code Architecture Layers

1. **Data Layer** : modele de donnees, tables, relations, regles de validation, champs calcules.
2. **Logic Layer** : automations, workflows, conditions, calculs, regles metier.
3. **Presentation Layer** : interfaces, vues, formulaires, dashboards, portails.
4. **Integration Layer** : API, webhooks, connecteurs (Zapier, Make), synchronisations.
5. **Security Layer** : authentification, autorisation (RBAC), permissions par champ/vue/table.

### Build vs Buy Decision Framework

| Critere | Construire en no-code | Acheter un SaaS specialise |
|---|---|---|
| Besoin specifique et unique | Oui | Non |
| Processus standard du marche | Non | Oui |
| Budget disponible | Faible-Moyen | Moyen-Eleve |
| Delai de mise en oeuvre | Court (jours/semaines) | Moyen (semaines/mois) |
| Competences internes | Citizen developers disponibles | Equipe IT disponible |
| Integration requise | Simple (API, Zapier) | Complexe (middleware, SSO) |
| Volume de donnees | < 100K lignes | > 100K lignes |

## Decision Guide

### Arbre de decision pour le choix de plateforme

```
1. Quel est le type d'application ?
   +-- Base de donnees collaborative / tracker --> Airtable
   +-- Outil interne / admin panel --> Retool
   +-- Application mobile terrain --> Glide ou AppSheet
   +-- Portail client / site avec login --> Softr
   +-- Application web complexe (SaaS, marketplace) --> Bubble
   +-- Formulaire avance / collecte de donnees --> Tally ou Typeform

2. Quel est l'ecosysteme existant ?
   +-- Google Workspace dominant --> AppSheet
   +-- Airtable deja en place --> Softr ou Glide
   +-- SQL databases existantes --> Retool
   +-- Aucun ecosysteme --> Airtable + Softr ou Bubble

3. Quel est le niveau technique de l'equipe ?
   +-- Non-technique --> Glide, Softr, Tally
   +-- Semi-technique --> Airtable, AppSheet
   +-- Technique --> Retool, Bubble
```

### Arbre de decision pour l'approche base de donnees

```
1. Volume de donnees ?
   +-- < 50K lignes --> Airtable, Google Sheets
   +-- 50K - 500K lignes --> Airtable Enterprise, AppSheet
   +-- > 500K lignes --> PostgreSQL + Retool, Supabase + Bubble

2. Relations entre donnees ?
   +-- Pas de relations --> Google Sheets, flat Airtable
   +-- Relations simples (1-to-many) --> Airtable standard
   +-- Relations complexes (many-to-many) --> Airtable avec junction tables, Bubble

3. Acces concurrent ?
   +-- < 10 utilisateurs simultanes --> Toute plateforme
   +-- 10-50 utilisateurs --> Airtable, AppSheet
   +-- > 50 utilisateurs --> Retool + SQL, Bubble
```

### Quand no-code vs low-code vs code

```
1. Complexite de la logique metier ?
   +-- Simple (CRUD, filtres, vues) --> No-code pur
   +-- Moyenne (calculs, conditions, workflows) --> No-code avance
   +-- Elevee (algorithmes, integrations complexes) --> Low-code ou code

2. Exigences de performance ?
   +-- Standard (< 1s de latence) --> No-code
   +-- Elevees (temps reel, gros volumes) --> Low-code ou code

3. Duree de vie prevue ?
   +-- Temporaire (< 6 mois) --> No-code
   +-- Permanente, critique --> No-code avec plan de migration ou code
```

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Relational Data Model** : structurer les donnees en tables liees avec des linked records. Ne jamais stocker des informations repetees dans une meme table. Utiliser les lookups et rollups pour agreger les donnees sans duplication.
- **Role-Based Access Control (RBAC)** : definir des roles (admin, editor, viewer) et configurer les permissions par vue, par table et par champ. Ne jamais donner un acces complet a tous les utilisateurs. Appliquer le principe du moindre privilege.
- **Progressive Forms** : decouper les formulaires longs en etapes logiques avec des conditions. Afficher uniquement les champs pertinents selon les reponses precedentes. Reduire la charge cognitive pour augmenter le taux de completion.
- **Linked Records as Single Source of Truth** : centraliser chaque type d'information dans une table unique et utiliser des liens pour y acceder depuis d'autres tables. Eviter la saisie manuelle d'informations disponibles ailleurs.
- **Computed Fields for Consistency** : utiliser les champs formules, rollups et lookups plutot que la saisie manuelle pour toute donnee derivee. Les calculs automatiques eliminent les erreurs et garantissent la coherence.

### Anti-patterns critiques

- **Spreadsheet-as-Database** : utiliser un Google Sheets de 50 colonnes et 10 000 lignes comme base de donnees, sans relations, sans validation et sans controle d'acces. Migrer vers une vraie base relationnelle (Airtable, Supabase) des que le volume depasse 1 000 lignes ou que les donnees ont des relations.
- **No Access Control** : laisser tous les utilisateurs acceder a toutes les donnees en lecture et ecriture. Risque de suppression accidentelle, de modification non autorisee et de fuite de donnees sensibles.
- **One Mega-Table** : stocker toutes les informations dans une seule table avec 50+ colonnes. Le symptome typique est la presence de colonnes "Type" pour distinguer des categories qui devraient etre des tables separees.
- **Ignoring Mobile** : construire une application uniquement pour desktop alors que les utilisateurs finaux sont sur le terrain avec des smartphones. Tester systematiquement l'experience mobile.
- **No Documentation** : ne pas documenter le modele de donnees, les automations et les regles metier de l'application. Quand le createur quitte l'equipe, l'application devient une boite noire ingeree.

## Implementation Workflow

### Phase 1 — Discovery & Requirements (Jours 1-3)
1. Identifier le probleme metier precis a resoudre et les utilisateurs cibles (personas).
2. Documenter les flux de donnees actuels (souvent manuels : emails, spreadsheets, fichiers partages).
3. Definir les user stories prioritaires selon le framework MoSCoW (Must, Should, Could, Won't).
4. Evaluer les contraintes : volume de donnees, nombre d'utilisateurs, exigences de securite, budget.
5. Choisir la plateforme adaptee en utilisant la Platform Selection Matrix.

### Phase 2 — Data Model & Architecture (Jours 3-5)
6. Concevoir le schema de donnees relationnel : tables, champs, types, relations, contraintes.
7. Creer les tables et configurer les champs avec les validations et valeurs par defaut.
8. Definir les vues (grid, kanban, calendar, gallery) pour chaque persona.
9. Configurer l'access control : roles, permissions par vue/table/champ.
10. Importer les donnees existantes et valider la coherence.

### Phase 3 — Build & Iterate (Jours 5-10)
11. Construire les interfaces principales (formulaires de saisie, vues de consultation, dashboards).
12. Configurer les automations : notifications, changements de statut, synchronisations.
13. Tester avec 3-5 utilisateurs pilotes et collecter le feedback structure.
14. Iterer rapidement sur les retours (2-3 cycles de feedback en une semaine).
15. Documenter les automations et les regles metier.

### Phase 4 — Deployment & Adoption (Jours 10-15)
16. Former les utilisateurs finaux avec des guides visuels et des sessions live.
17. Deployer progressivement (equipe pilote puis generalisation).
18. Mettre en place le monitoring d'usage (taux de connexion, fonctionnalites utilisees).
19. Definir le processus de support et de remontee des bugs.
20. Planifier la revue post-deploiement a J+30.

### Phase 5 — Optimize & Scale (Continu)
21. Analyser les metriques d'usage et identifier les fonctionnalites sous-utilisees ou manquantes.
22. Optimiser les performances (vues, automations, requetes).
23. Etendre les fonctionnalites selon les retours utilisateurs priorises.
24. Evaluer regulierement les limites de la plateforme et planifier la migration si necessaire.
25. Maintenir la documentation a jour et former les nouveaux utilisateurs.

## Modele de maturite

### Niveau 1 — Ad Hoc
- Les besoins applicatifs sont resolus par des spreadsheets partages, des emails et des fichiers sur un drive.
- Pas de modele de donnees structure : les informations sont dispersees et dupliquees.
- Les utilisateurs construisent des solutions individuelles sans coordination ni standards.
- **Indicateurs** : 0 application no-code en production, temps de recherche d'information > 15 min/jour, taux d'erreur de saisie > 10%.

### Niveau 2 — Experimental
- Une ou deux applications no-code sont en production, construites par des early adopters.
- Le modele de donnees est basique (tables plates, peu de relations) mais fonctionnel.
- Les automations simples sont en place (notifications, changements de statut).
- **Indicateurs** : 1-3 applications no-code en production, adoption > 50% de l'equipe cible, reduction du temps de traitement de 20%+.

### Niveau 3 — Structure
- Un catalogue d'applications no-code est maintenu avec des conventions de nommage et de la documentation.
- Les modeles de donnees sont relationnels avec des linked records, rollups et lookups.
- Le RBAC est configure sur toutes les applications avec des roles definis.
- **Indicateurs** : 5-15 applications en production, citizen developers identifies et formes, governance documentee.

### Niveau 4 — Optimise
- Les applications no-code sont integrees entre elles et avec les systemes existants (ERP, CRM, API).
- Les workflows complexes sont automatises end-to-end (multi-etapes, conditions, approbations).
- Les metriques d'usage sont suivies et les applications sont optimisees en continu.
- **Indicateurs** : 15-50 applications en production, integrations actives avec 3+ systemes, temps de deploiement d'une nouvelle app < 5 jours.

### Niveau 5 — Plateforme
- Le no-code est une competence organisationnelle avec une communaute de citizen developers formee.
- Une plateforme interne standardisee (templates, composants reutilisables, guidelines) accelere le developpement.
- L'IA assiste la creation d'applications (generation de schemas, interfaces, automations).
- **Indicateurs** : 50+ applications en production, delai moyen de creation < 2 jours, taux de satisfaction utilisateur > 90%, ROI documente par application.

## Rythme operationnel

| Cadence | Activite | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Hebdomadaire** | Revue des demandes d'applications et priorisation du backlog | No-Code Lead / Product Owner | Backlog priorise et planning sprint |
| **Bi-mensuel** | Revue d'usage des applications — adoption, bugs, feedback | No-Code Lead + Utilisateurs cles | Rapport d'usage et plan d'amelioration |
| **Mensuel** | Audit de gouvernance — documentation, permissions, naming | No-Code Lead + IT | Rapport d'audit et actions correctives |
| **Mensuel** | Formation citizen developers — nouvelles fonctionnalites et bonnes pratiques | No-Code Lead | Session de formation + guide mis a jour |
| **Trimestriel** | Revue d'architecture — limites plateformes, migrations, integrations | No-Code Lead + CTO | Feuille de route technique trimestrielle |
| **Trimestriel** | Benchmark plateformes — nouvelles fonctionnalites, pricing, alternatives | No-Code Lead | Note de veille technologique |
| **Annuel** | Bilan no-code — ROI, maturite, strategie N+1 | No-Code Lead + Direction | Bilan annuel et strategie no-code N+1 |

## State of the Art (2025-2026)

Le developpement no-code integre les evolutions majeures suivantes :

- **AI-Generated Apps** : les plateformes integrent des moteurs d'IA capables de generer des applications completes a partir d'une description en langage naturel. Airtable Cobuilder, Retool AI, Glide AI et AppSheet Duet AI transforment un prompt en schema de donnees, interface et automations en quelques minutes.
- **Natural Language to App** : la frontiere entre prompt et configuration s'estompe. L'utilisateur decrit ce qu'il veut ("un tracker de bugs avec assignation et priorite") et l'IA genere l'application. Le role du citizen developer evolue de constructeur a curateur et validateur.
- **Composable No-Code** : les architectures monolithiques cedent la place a des approches composables ou chaque couche (donnees, logique, interface, integration) peut etre geree par un outil specialise. Airtable pour les donnees, Retool pour l'admin, Softr pour le portail, Make pour les automations.
- **Embedded AI** : l'IA s'integre directement dans les applications no-code sous forme de champs intelligents (classification automatique, extraction d'entites, generation de texte, analyse de sentiment). Airtable AI Fields et Bubble AI actions permettent d'ajouter de l'intelligence sans une seule ligne de code.
- **Marketplace Ecosystems** : les plateformes no-code developpent des ecosystemes de templates, plugins et extensions creees par la communaute. Bubble Marketplace, Airtable Universe et Softr Templates accelerent le demarrage en offrant des applications preconstruites a personnaliser.
- **Enterprise No-Code** : les grandes organisations adoptent le no-code avec des exigences de gouvernance, SSO, audit trail, conformite SOC2 et GDPR. Les plateformes repondent avec des fonctionnalites enterprise : Airtable Enterprise, Retool Enterprise, Bubble Dedicated.

## Template actionnable

### Brief de projet no-code

| Section | Contenu |
|---|---|
| **Nom du projet** | ___ |
| **Probleme a resoudre** | Description du probleme metier en 2-3 phrases |
| **Utilisateurs cibles** | Personas, nombre, niveau technique, devices |
| **Donnees** | Entites principales, volume estime, sources existantes |
| **Fonctionnalites Must-Have** | Liste des user stories prioritaires (MoSCoW - Must) |
| **Fonctionnalites Should-Have** | Fonctionnalites souhaitees mais non bloquantes |
| **Integrations requises** | Systemes a connecter (CRM, email, Slack, API) |
| **Securite & acces** | Roles, donnees sensibles, conformite requise |
| **Plateforme envisagee** | Plateforme choisie et justification |
| **Delai cible** | Date de deploiement pilote / generalisation |
| **Criteres de succes** | KPIs mesurables (adoption, temps gagne, erreurs reduites) |
| **Proprietaire** | Nom du responsable de l'application |

## Prompts types

- "Aide-moi a choisir la meilleure plateforme no-code pour construire un CRM interne"
- "Concois le modele de donnees Airtable pour une gestion de projets avec taches, assignations et deadlines"
- "Comment creer un portail client avec Softr connecte a ma base Airtable ?"
- "Propose une architecture no-code pour un systeme de ticketing interne"
- "Aide-moi a configurer des automations Airtable pour les notifications de validation"
- "Quels sont les limites d'Airtable et quand faut-il migrer vers une solution codee ?"
- "Cree un formulaire multi-etapes avec Tally incluant logique conditionnelle et calculs"
- "Compare Retool et Bubble pour un dashboard operationnel avec donnees SQL"

## Limites et Red Flags

Ce skill n'est PAS adapte pour :
- **Developpement d'applications a forte charge** (> 100K utilisateurs, temps reel critique, calculs intensifs) --> Utiliser plutot : `code-development:architecture`
- **Architecture technique et infrastructure** (cloud, containers, CI/CD, microservices) --> Utiliser plutot : `code-development:devops`
- **Pipelines de donnees et ETL** (data warehouse, data lake, transformations lourdes) --> Utiliser plutot : `data-bi:data-engineering`
- **Automatisation de workflows inter-applications** (Zapier, Make, n8n en profondeur) --> Utiliser plutot : `productivite:automatisation-workflows`
- **Gestion de projet et methodologies** (Agile, Scrum, Kanban methodologique) --> Utiliser plutot : `entreprise:gestion-de-projets`

Signaux d'alerte en cours d'utilisation :
- Une application Airtable depasse 50 000 lignes sans strategie d'archivage — risque de degradation de performance et couts eleves
- Plus de 20 automations s'executent sur la meme base sans documentation — risque de conflits, boucles infinies et depassement de quotas
- Un seul citizen developer maintient toutes les applications critiques — bus factor de 1, risque operationnel majeur
- Aucune sauvegarde ni procedure de restauration n'est en place — risque de perte de donnees irreversible
- Les donnees sensibles (RH, finance, sante) sont stockees sans access control ni chiffrement — non-conformite GDPR et risque legal

## Skills connexes

| Skill | Lien |
|---|---|
| Automatisation & Workflows | `productivite:automatisation-workflows` — Automatisation inter-applications (Zapier, Make, n8n) |
| Excel & Spreadsheets | `productivite:excel-spreadsheets` — Donnees tabulaires et modelisation |
| Notion & Knowledge Management | `productivite:notion-knowledge-management` — Bases de connaissances et wikis |
| Collaboration Digitale | `productivite:collaboration-digitale` — Outils collaboratifs et communication |
| IT Systemes | `entreprise:it-systemes` — Architecture SI et gouvernance IT |
| Data Engineering | `data-bi:data-engineering` — Pipelines de donnees et transformations |

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[Airtable & Bases de Donnees Visuelles](./references/airtable-databases.md)** : fondamentaux Airtable (bases, tables, champs, vues), modelisation relationnelle, champs avances (formules, rollups, lookups), Airtable Automations, Interface Designer, Extensions, patterns d'integration (API, Zapier, Make), limites et alternatives (NocoDB, Baserow, Smartsheet).
- **[App Builders](./references/app-builders.md)** : Retool (outils internes, SQL-natif, composants), Glide (mobile-first, Sheets/Airtable backend), AppSheet (Google ecosystem, expressions), Bubble (full-stack web apps, workflows), Softr (portails Airtable), comparaison detaillee, architecture, deploiement, pricing, strategies de migration.
- **[Formulaires & Portails](./references/forms-portals.md)** : form builders modernes (Tally, Typeform, JotForm, Google Forms), fonctionnalites avancees (logique conditionnelle, calculs, uploads, paiements), patterns form-to-workflow, portails clients/fournisseurs, portails self-service, embedding, analytics, accessibilite, conformite GDPR.
- **[Architecture No-Code](./references/architecture-patterns.md)** : patterns d'architecture de donnees (relationnel, flat, hybride), securite et access control (RBAC), optimisation de performance, limites de scalabilite, framework de gouvernance (naming, documentation, ownership, lifecycle), testing, monitoring, backup, conformite (GDPR, SOC2), migration no-code vers code.
