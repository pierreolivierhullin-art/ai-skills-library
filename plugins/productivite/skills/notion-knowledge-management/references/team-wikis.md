# Wikis d'Equipe -- Confluence, Notion Team, Structure, Gouvernance & Adoption

## Overview

Ce document de reference couvre la conception, le deploiement et la gouvernance des wikis d'equipe et des bases de connaissances organisationnelles. Il detaille les architectures d'information adaptees aux equipes de 10 a 10 000 personnes, les bonnes pratiques sur Confluence et Notion Team, la gouvernance documentaire, les types de contenu essentiels, les strategies d'adoption et les metriques de sante d'un wiki. Utiliser ce guide pour concevoir des wikis qui restent vivants et utiles dans la duree, pas des cimetieres documentaires abandonnes apres 3 mois.

---

## Key Concepts

### Pourquoi un wiki d'equipe ?

Un wiki d'equipe repond a trois problemes fondamentaux :

1. **La perte de connaissances** : quand un collaborateur quitte l'entreprise, son savoir part avec lui. Un wiki capture et preserve les connaissances critiques independamment des individus. Sans wiki, le bus factor de l'equipe est dangereusement bas.

2. **La repetition des reponses** : les memes questions reviennent en boucle ("Comment deployer en production ?", "Quelle est la politique de conges ?", "Comment acceder au VPN ?"). Un wiki bien structure transforme chaque reponse en une ressource permanente. Regle : si une question est posee plus de 2 fois, la reponse doit etre documentee.

3. **La friction d'onboarding** : sans documentation, l'integration d'un nouveau collaborateur depend entierement des disponibilites des collegues seniors. Un wiki d'onboarding structure reduit le temps d'autonomie de 3 mois a 3-4 semaines.

### Les 3 dimensions d'un wiki reussi

1. **Structure** : l'architecture de l'information -- comment le contenu est organise, categorise et relie. Sans structure, le wiki est un tas informe de pages ou personne ne trouve rien.

2. **Contenu** : la qualite, la pertinence et la fraicheur de l'information documentee. Un wiki avec une belle structure mais du contenu obsolete est pire que pas de wiki du tout -- il induit en erreur.

3. **Culture** : les habitudes, les rituels et les incentives qui maintiennent le wiki vivant. La technologie ne suffit pas -- il faut une culture de documentation active.

---

## Architecture de l'information

### Principes d'architecture pour les wikis d'equipe

#### Hierarchie a 3 niveaux maximum

```
Niveau 1 : Espaces / Sections (5-10 maximum)
|
+-- Niveau 2 : Categories / Sous-sections (5-15 par espace)
|   |
|   +-- Niveau 3 : Pages de contenu
```

Au-dela de 3 niveaux de profondeur, la navigation devient penible et les pages sont "enterrees". Si un contenu necessiterait un 4e niveau, c'est un signal qu'il faut restructurer.

#### Architecture type par taille d'organisation

**Equipe (5-20 personnes) :**

```
Wiki Equipe
|
+-- Accueil (dashboard equipe, liens rapides)
+-- Onboarding (guide du nouveau, contacts cles, acces)
+-- Processus (comment faire X, Y, Z)
+-- Decisions (log des decisions avec contexte)
+-- Reunions (templates + historique des CR)
+-- Ressources (liens utiles, outils, glossaire)
```

**Departement (20-100 personnes) :**

```
Wiki Departement
|
+-- Accueil (vision, objectifs, organigramme)
+-- Onboarding
|   +-- Guide du nouveau
|   +-- Outils et acces
|   +-- Qui fait quoi
|
+-- Processus & Procedures
|   +-- [Processus metier 1]
|   +-- [Processus metier 2]
|   +-- Templates
|
+-- Documentation technique / metier
|   +-- [Domaine 1]
|   +-- [Domaine 2]
|
+-- Gouvernance
|   +-- Decisions (ADR, decision log)
|   +-- Politiques et guidelines
|   +-- Retrospectives
|
+-- Projets (liens vers les pages projets)
```

**Entreprise (100+ personnes) :**

```
Wiki Entreprise
|
+-- Portail d'accueil (navigation globale, recherche)
+-- Espaces par departement (Engineering, Product, Marketing, Sales, HR, Finance)
+-- Espace transversal
|   +-- Onboarding general
|   +-- Culture & valeurs
|   +-- Politiques RH (conges, teletravail, avantages)
|   +-- Securite & conformite
|   +-- Glossaire entreprise
|
+-- Espace projets (cross-departement)
+-- Knowledge base produit (documentation produit interne)
```

### Patterns d'architecture

#### Hub & Spoke

La page hub centralise les liens et la navigation pour un domaine. Les pages de detail (spokes) contiennent le contenu substantiel. Le hub ne contient pas de contenu long -- il sert de carte et de point d'entree.

**Exemple de page hub :**
```
# Engineering Wiki

Bienvenue dans l'espace Engineering.

## Acces rapides
- [Onboarding Engineering](./onboarding)
- [Architecture & ADR](./architecture)
- [Runbooks](./runbooks)

## Par equipe
- [Backend](./backend)
- [Frontend](./frontend)
- [Data](./data)
- [Infra / DevOps](./infra)

## Processus
- [Code review guidelines](./code-review)
- [Deployment process](./deployment)
- [Incident management](./incidents)

## Contacts
| Role | Nom | Slack |
|------|-----|-------|
| VP Engineering | ... | @... |
| Engineering Manager Backend | ... | @... |
```

#### Progressive Disclosure

Montrer l'information du general au specifique. La page d'accueil donne une vue d'ensemble avec des liens vers les details. Chaque niveau de navigation revele plus de detail.

**Niveau 1** : "Voici nos 5 processus principaux" (liste de liens)
**Niveau 2** : "Voici le processus de deploiement" (vue d'ensemble en 5 etapes)
**Niveau 3** : "Voici l'etape 3 du deploiement en detail" (pas-a-pas avec screenshots)

#### Living Documents vs Snapshots

Distinguer deux types de pages :
- **Living documents** : pages mises a jour en continu (processus, guidelines, FAQ). Elles n'ont pas de date de creation significative -- seule la date de derniere mise a jour compte.
- **Snapshots** : pages figees dans le temps (comptes rendus de reunions, ADR, retrospectives). Elles ne sont pas modifiees apres creation, sauf correction d'erreur.

---

## Confluence -- Bonnes pratiques

### Architecture Confluence

Confluence organise le contenu en :
- **Spaces** : conteneurs de haut niveau (1 par equipe ou departement)
- **Pages** : le contenu, avec une hierarchie parent-enfant
- **Labels** : tags transversaux pour la categorisation cross-space
- **Templates** : modeles de pages pour la standardisation

#### Bonnes pratiques Confluence

1. **Un space par equipe ou domaine** : ne pas creer de space par projet (trop volatile). Un space = un domaine de connaissance durable.

2. **Page tree structure** : la hierarchie des pages doit refleter la structure conceptuelle, pas l'organigramme. Les reorganisations internes ne doivent pas casser la navigation du wiki.

3. **Labels systematiques** : definir un vocabulaire de labels controle (10-20 labels maximum). Exemples : `how-to`, `reference`, `decision`, `runbook`, `onboarding`, `template`, `obsolete`.

4. **Templates obligatoires** : creer des templates Confluence pour chaque type de contenu recurrent. Configurer les templates comme "blueprints" pour qu'ils soient proposes lors de la creation de page.

5. **Macros utiles** :
   - **Table of Contents** : generee automatiquement a partir des headings
   - **Excerpt Include** : reutiliser un extrait d'une page dans une autre
   - **Page Properties** : ajouter des metadonnees structurees (owner, statut, date de revue)
   - **Content by Label** : afficher dynamiquement les pages avec un label donne
   - **Status** : afficher un badge de statut (Draft, In Review, Published, Obsolete)

6. **Permissions** : utiliser les groupes Confluence pour les permissions, pas les utilisateurs individuels. Definir des permissions par space, pas par page (sauf exceptions).

### Confluence vs Notion pour les equipes

| Critere | Confluence | Notion |
|---|---|---|
| **Taille d'equipe ideale** | 50-10 000+ | 5-500 |
| **Gouvernance** | Robuste (permissions fines, audit log, compliance) | Basique (teamspaces, permissions simples) |
| **Integration Atlassian** | Native (Jira, Bitbucket, Trello) | Via API ou outils tiers |
| **Flexibilite** | Moyenne (format page wiki) | Elevee (databases, vues, blocs) |
| **Recherche** | Bonne, amelioree avec AI (Atlassian Intelligence) | Bonne, amelioree avec Notion AI |
| **Collaboration temps reel** | Bonne | Excellente |
| **Templates** | Blueprints structurees | Tres flexibles (page + database) |
| **Courbe d'apprentissage** | Faible (editeur familier) | Moderee (concepts Notion specifiques) |
| **Prix par utilisateur** | $5.75-11/mois (Standard/Premium) | $8-15/mois (Plus/Business) |
| **SSO / SCIM** | Standard et Premium | Business et Enterprise |

---

## Notion pour les equipes

### Team Spaces

Les teamspaces Notion sont des espaces dedies a des equipes avec leurs propres parametres :

- **Permissions par teamspace** : Full access, Can edit, Can view, Can comment. Definir le niveau par defaut et les exceptions.
- **Default page permissions** : configurer les permissions par defaut pour les nouvelles pages creees dans le teamspace.
- **Sidebar customization** : personnaliser la sidebar du teamspace pour mettre en avant les pages les plus importantes.

### Workflows d'equipe dans Notion

#### 1. Workflow de documentation

```
Brouillon --> En revue --> Publie --> En maintenance --> Archive
```

Implementer via une propriete Status dans une database "Documents" :
- **Brouillon** : l'auteur redige. Pas de visibilite equipe.
- **En revue** : un reviewer est assigne. Feedback via commentaires.
- **Publie** : le document est visible par l'equipe. Le reviewer a valide.
- **En maintenance** : le document est publie mais necessite une mise a jour.
- **Archive** : le document n'est plus pertinent. Deplace dans une vue archive.

#### 2. Workflow de decision (ADR)

```
Proposition --> Discussion --> Decision --> Implementation --> Revue
```

Chaque decision est documentee dans une database "Decisions" avec :
- Titre de la decision
- Contexte : quel probleme cherche-t-on a resoudre ?
- Options envisagees (2-4 options avec avantages/inconvenients)
- Decision prise et justification
- Consequences attendues
- Date de revue prevue (6-12 mois)

#### 3. Workflow de reunion

Avant la reunion :
- Creer la page a partir du template "CR Reunion"
- Remplir l'agenda (topics + owners)
- Partager le lien avec les participants

Pendant la reunion :
- Prendre les notes directement dans la page Notion
- Utiliser les mentions (@nom) pour les actions assignees

Apres la reunion :
- Completer les decisions et actions
- Notifier les absents
- Relier le CR aux projets et decisions concernes

---

## Types de contenu essentiels

### Taxonomie des contenus d'un wiki

| Type | Description | Template | Cycle de vie |
|---|---|---|---|
| **How-To Guide** | Procedure pas-a-pas pour accomplir une tache | Etapes numerotees, screenshots, prerequis | Living document, revue semestrielle |
| **Reference** | Documentation factuelle (API, config, specs) | Format structure, table des matieres | Living document, MAJ continue |
| **Tutorial** | Guide d'apprentissage pour un concept | Progression pedagogique, exercices | Living document, revue annuelle |
| **ADR** | Architecture Decision Record | Contexte, options, decision, consequences | Snapshot, jamais modifie |
| **Runbook** | Procedure de resolution d'incident | Diagnostic, etapes, escalade, rollback | Living document, teste regulierement |
| **Decision Log** | Journal des decisions d'equipe | Date, decision, contexte, decideur | Snapshot chronologique |
| **Meeting Notes** | Compte rendu de reunion | Participants, agenda, decisions, actions | Snapshot, reference future |
| **RFC / Proposal** | Proposition technique ou organisationnelle | Probleme, solution proposee, alternatives, plan | Snapshot apres approbation |
| **FAQ** | Questions frequentes avec reponses | Q&A format, categories | Living document, enrichi en continu |
| **Glossaire** | Definitions des termes metier | Terme, definition, contexte d'usage | Living document, enrichi progressivement |
| **Onboarding Guide** | Parcours d'integration nouveau collaborateur | Jour 1, semaine 1, mois 1, checklist | Living document, revue trimestrielle |
| **Postmortem** | Analyse post-incident | Timeline, impact, root cause, actions | Snapshot |

### Template ADR (Architecture Decision Record)

```markdown
# ADR-[numero] : [Titre de la decision]

**Statut** : Propose / Accepte / Decline / Remplace par ADR-XX
**Date** : YYYY-MM-DD
**Decideurs** : [noms]
**Contexte technique** : [domaine]

## Contexte

[Description du probleme ou de la situation qui necessite une decision.
Inclure les contraintes, les dependencies et le contexte technique.]

## Options envisagees

### Option 1 : [Nom]
- **Description** : [...]
- **Avantages** : [...]
- **Inconvenients** : [...]
- **Cout estime** : [...]

### Option 2 : [Nom]
- **Description** : [...]
- **Avantages** : [...]
- **Inconvenients** : [...]
- **Cout estime** : [...]

### Option 3 : [Nom]
- [...]

## Decision

[L'option choisie et la justification detaillee du choix.]

## Consequences

- **Positives** : [...]
- **Negatives** : [...]
- **Risques** : [...]

## Date de revue prevue

[Date a laquelle la decision sera reevaluee, typiquement 6-12 mois.]
```

### Template Runbook

```markdown
# Runbook : [Nom de l'incident / procedure]

**Derniere mise a jour** : YYYY-MM-DD
**Owner** : [nom]
**Severite associee** : [S1/S2/S3/S4]
**Temps de resolution cible** : [duree]

## Symptomes

- [Comment identifier que cet incident se produit ?]
- [Alertes associees : nom de l'alerte, dashboard]

## Diagnostic

1. [Premiere verification a effectuer]
2. [Deuxieme verification]
3. [Commandes ou requetes de diagnostic]

## Resolution

### Scenario A : [Description du scenario]
1. [Etape 1]
2. [Etape 2]
3. [Verification que la resolution a fonctionne]

### Scenario B : [Description du scenario]
1. [Etape 1]
2. [Etape 2]

## Rollback

[Procedure de rollback si la resolution aggrave le probleme]

## Escalade

| Niveau | Contact | Quand escalader |
|--------|---------|-----------------|
| L1 | [nom / equipe] | [critere] |
| L2 | [nom / equipe] | [critere] |
| L3 | [nom / equipe] | [critere] |

## Historique des incidents

| Date | Duree | Cause | Resolution appliquee |
|------|-------|-------|---------------------|
| YYYY-MM-DD | XX min | [...] | Scenario A |
```

---

## Gouvernance documentaire

### Roles et responsabilites

| Role | Responsabilites | Charge estimee |
|------|-----------------|----------------|
| **Wiki Champion / Knowledge Manager** | Vision globale, architecture, metriques, evangelisation | 20-40% du temps |
| **Space Owner** | Architecture et qualite d'un espace/section | 5-10% du temps |
| **Content Owner** | Maintenance et exactitude d'un ensemble de pages | 2-5% du temps |
| **Contributeur** | Creation et mise a jour du contenu dans le cadre defini | Integre au workflow quotidien |
| **Reviewer** | Validation de la qualite et de l'exactitude du contenu | Ponctuel, sur demande |

### Cycle de revue du contenu

| Frequence | Action | Responsable |
|-----------|--------|-------------|
| **Continue** | Mise a jour lors de tout changement de processus ou d'outil | Content Owner |
| **Mensuelle** | Revue des pages les plus consultees pour verifier l'exactitude | Content Owner |
| **Trimestrielle** | Audit des pages non consultees depuis 90 jours | Wiki Champion |
| **Trimestrielle** | Revue de la structure et de la navigation | Wiki Champion |
| **Semestrielle** | Audit complet : pages obsoletes, liens casses, lacunes | Wiki Champion + Space Owners |
| **Annuelle** | Retrospective globale du wiki et planification | Wiki Champion + Direction |

### Politique d'archivage

Definir des criteres clairs pour l'archivage :
- Page non consultee depuis 180 jours et non marquee comme "reference permanente"
- Projet termine depuis plus de 90 jours (les CR et decisions restent, les notes de travail sont archivees)
- Processus remplace par un nouveau processus (l'ancien est archive avec mention du remplacement)
- Information factuellement obsolete (ex : documentation d'un outil abandonne)

Procedure d'archivage :
1. Identifier les pages candidates (via metriques ou audit)
2. Notifier le Content Owner et demander confirmation
3. Ajouter un bandeau "Cette page est archivee. Pour la version actuelle, voir [lien]"
4. Deplacer dans l'espace Archive (ne pas supprimer)
5. Les pages archivees restent cherchables mais ne sont plus visibles dans la navigation

### Convention de nommage

Definir une convention stricte des le jour 1. Exemples :

| Type de contenu | Convention | Exemple |
|-----------------|------------|---------|
| How-To | `How to [action]` | "How to deploy to production" |
| ADR | `ADR-[NNN]: [Titre]` | "ADR-042: Choix de PostgreSQL comme base primaire" |
| Runbook | `Runbook: [Incident/Procedure]` | "Runbook: Database failover" |
| CR Reunion | `[YYYY-MM-DD] CR [Nom reunion]` | "2026-02-10 CR Sprint Planning" |
| RFC | `RFC-[NNN]: [Titre]` | "RFC-015: Migration vers Kubernetes" |
| Policy | `[Domaine] Policy: [Sujet]` | "HR Policy: Remote work" |

---

## Strategies d'adoption

### Les 4 leviers de l'adoption

#### 1. Utilite percue (le contenu doit etre utile)

Le levier le plus puissant pour l'adoption est la qualite et la pertinence du contenu. Un wiki qui repond reellement aux questions que les gens se posent sera utilise naturellement. Commencer par documenter les 10 questions les plus frequemment posees (identifier via Slack, emails, conversations).

#### 2. Facilite d'acces (le wiki doit etre trouvable)

- Integrer le lien du wiki dans la sidebar Slack ou Teams
- Ajouter le wiki en page d'accueil du navigateur des nouveaux collaborateurs
- Configurer un bot Slack qui suggere des pages wiki quand certains mots-cles sont mentionnes
- Creer des raccourcis clavier ou des bookmarks pour les sections les plus utilisees

#### 3. Habitudes et rituels (le wiki doit faire partie du workflow)

- Exiger un lien wiki dans chaque ticket Jira pour la documentation technique
- Commencer chaque reunion par "quelqu'un a-t-il mis a jour le wiki cette semaine ?"
- Inclure la contribution au wiki dans les objectifs individuels et les evaluations de performance
- Celebrer les contributeurs les plus actifs (leaderboard, mention en all-hands)

#### 4. Leadership par l'exemple (les managers doivent montrer l'exemple)

Si les managers ne documentent pas et ne consultent pas le wiki, personne ne le fera. Les leaders doivent :
- Documenter leurs propres decisions dans le wiki
- Repondre aux questions en partageant un lien wiki plutot qu'en reexpliquant
- Participer aux revues de contenu
- Mentionner le wiki dans les communications d'equipe

### Plan de deploiement en 12 semaines

| Semaine | Activite | Objectif |
|---------|----------|----------|
| 1-2 | Audit des besoins, choix de l'outil, definition de l'architecture | Architecture validee |
| 3-4 | Configuration de l'outil, creation des templates, migration initiale | Workspace pret |
| 5-6 | Pilote avec 5-10 early adopters | 20 pages creees, feedback collecte |
| 7-8 | Iteration sur la structure et les templates | Architecture ajustee |
| 9-10 | Deploiement a l'equipe complete, formation | 80% de l'equipe a cree au moins 1 page |
| 11-12 | Etablissement des rituels de maintenance, nomination des owners | Gouvernance operationnelle |

### Gerer la resistance au changement

| Objection | Reponse | Action |
|-----------|---------|--------|
| "Je n'ai pas le temps de documenter" | "Documenter 5 min maintenant evite de reexpliquer 30 min 10 fois" | Montrer le ROI avec des exemples concrets |
| "L'info change trop vite" | "C'est pourquoi le wiki est vivant, pas un document fige" | Simplifier le processus de mise a jour |
| "Personne ne lit le wiki" | "Parce que le contenu n'est pas encore assez utile. Contribuer l'ameliore" | Creer du contenu de haute valeur pour amorcer |
| "Je prefere demander a un collegue" | "Le collegue n'est pas toujours disponible. Le wiki, si" | Encourager les reponses avec lien wiki |
| "C'est encore un outil de plus" | "C'est LE lieu central, pas un outil supplementaire" | Integrer le wiki dans les outils existants (Slack, Jira) |

---

## Metriques de sante du wiki

### KPIs principaux

| Metrique | Formule | Cible | Frequence |
|----------|---------|-------|-----------|
| **Taux d'adoption** | Utilisateurs actifs / utilisateurs totaux | > 70% | Mensuel |
| **Taux de contribution** | Contributeurs (edits) / utilisateurs actifs | > 30% | Mensuel |
| **Pages creees / mois** | Nouvelles pages creees dans le mois | Croissant ou stable | Mensuel |
| **Pages consultees / jour** | Nombre de pages vues par jour | Croissant | Hebdomadaire |
| **Taux de freshness** | Pages mises a jour < 6 mois / total pages | > 70% | Trimestriel |
| **Pages orphelines** | Pages sans liens entrants | < 10% du total | Trimestriel |
| **Temps de recherche moyen** | Temps entre la recherche et le clic sur un resultat | < 30 sec | Trimestriel (sondage) |
| **Satisfaction utilisateur** | NPS ou score de satisfaction du wiki | > 40 (NPS) | Semestriel |
| **Ratio contenu/utilisateur** | Pages / utilisateurs actifs | 5-15 pages/utilisateur | Trimestriel |
| **Taux d'archivage** | Pages archivees / total pages creees (cumule) | 20-40% (signe de maintenance active) | Annuel |

### Dashboard de sante du wiki

Construire un dashboard synthetique avec 4 quadrants :

```
+---------------------------+---------------------------+
| CROISSANCE                | QUALITE                   |
| - Pages creees / mois     | - Taux de freshness       |
| - Nouveaux contributeurs  | - Pages orphelines        |
| - Espaces actifs          | - Liens casses            |
+---------------------------+---------------------------+
| ENGAGEMENT                | GOUVERNANCE               |
| - Pages vues / jour       | - Pages avec owner        |
| - Recherches / jour       | - Pages avec date revue   |
| - Taux de contribution    | - Templates utilises      |
+---------------------------+---------------------------+
```

### Signaux d'alerte

- Taux de freshness < 50% : le wiki devient un musee. Lancer un sprint de mise a jour.
- Taux de contribution < 15% : le wiki est un monologue, pas une collaboration. Former et inciter.
- Pages orphelines > 20% : la navigation est deficiente. Revoir la structure et les liens.
- Aucune page creee depuis 30 jours : le wiki est moribond. Intervention urgente du Wiki Champion.
- Plus de 50% des recherches sans resultat : le contenu ne couvre pas les besoins. Analyser les recherches infructueuses.

---

## Migration entre plateformes wiki

### Checklist de migration

1. **Audit du contenu source** : inventorier toutes les pages, identifier le contenu actif (< 6 mois) vs obsolete, estimer le volume a migrer (typiquement 30-50% du contenu total).

2. **Mapping de la structure** : definir comment la structure source se traduit dans l'outil cible. Les espaces Confluence deviennent-ils des teamspaces Notion ? Les labels deviennent-ils des tags ou des proprietes ?

3. **Migration des templates** : recreer les templates dans l'outil cible avant de migrer le contenu. Profiter de la migration pour ameliorer les templates.

4. **Migration par lots** : migrer espace par espace, equipe par equipe. Ne pas tout migrer en big bang. Valider chaque lot avec les utilisateurs concernes.

5. **Verification des liens** : les liens internes sont souvent casses apres migration. Prevoir un sprint de correction des liens.

6. **Formation** : former les utilisateurs sur le nouvel outil avant de couper l'ancien. La formation est plus importante que la migration technique.

7. **Periode de cohabitation** : maintenir l'ancien outil en lecture seule pendant 3-6 mois. Rediriger les utilisateurs vers le nouveau wiki.

8. **Mesure post-migration** : comparer les metriques d'adoption avant et apres migration. S'assurer que le changement est positif.

### Pieges courants de la migration

- **Migrer le contenu obsolete** : profiter de la migration pour faire le tri. Ne migrer que le contenu actif et pertinent.
- **Reproduire la meme structure** : si la structure de l'ancien wiki etait deficiente, ne pas la reproduire a l'identique. La migration est l'occasion de restructurer.
- **Negliger la formation** : un nouvel outil sans formation = un wiki vide. Investir dans la formation autant que dans la migration technique.
- **Couper l'ancien outil trop tot** : les utilisateurs ont besoin de temps pour s'adapter. Maintenir l'ancien en lecture seule pendant la transition.
- **Ignorer les integrations** : verifier que toutes les integrations (Slack bots, liens dans Jira, bookmarks) pointent vers le nouvel outil.
