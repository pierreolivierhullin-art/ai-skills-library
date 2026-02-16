# Templates & Systemes -- Design de Templates, Systemes Relationnels, Automatisation & Scaling

## Overview

Ce document de reference couvre la conception de templates, la construction de systemes relationnels, l'automatisation des workflows de connaissances et le scaling des systemes de gestion documentaire du personnel a l'organisation. Il detaille les principes de design de templates (consistance, flexibilite, progressive disclosure), les systemes de databases relationnelles dans Notion, les patterns d'automatisation, la gestion du cycle de vie du contenu, les strategies de backup et d'export. Utiliser ce guide pour construire des systemes de connaissances robustes, maintenables et evolutifs.

---

## Key Concepts

### Pourquoi les templates sont essentiels

Les templates sont le mecanisme le plus efficace pour garantir la qualite et la consistance d'une base de connaissances. Sans templates :
- Chaque contributeur invente son propre format, rendant la lecture et la recherche difficiles
- Les informations critiques sont oubliees (pas de checklist de completude)
- Le temps de creation de contenu est plus long (partir d'une page blanche vs remplir un cadre)
- La maintenance est couteuse (chaque page est unique, pas de traitement en lot possible)

Avec des templates bien concus :
- Le temps de creation de contenu diminue de 40-60%
- La completude des informations augmente de 30-50%
- La recherche est plus efficace (structure previsible)
- Le onboarding des nouveaux contributeurs est accelere

### Les 3 dimensions du design de templates

1. **Consistance** : chaque instance d'un template produit un document avec la meme structure, les memes sections et le meme niveau de detail. La consistance permet la comparaison, la recherche et le traitement en lot.

2. **Flexibilite** : le template doit s'adapter a differents contextes sans perdre sa structure. Utiliser des sections optionnelles (marquees clairement) plutot que des structures rigides qui ne conviennent qu'a un cas sur deux.

3. **Progressive disclosure** : le template doit guider le contributeur du general au specifique. Les sections obligatoires en premier, les sections optionnelles ensuite. Ne pas noyer le contributeur sous 30 champs a remplir des la premiere page.

---

## Design de templates

### Principes de conception

#### 1. Commencer par l'usage, pas par la structure

Avant de concevoir un template, repondre a ces questions :
- Qui va remplir ce template ? (profil, niveau de competence, frequence d'utilisation)
- Qui va lire le document produit ? (audience, contexte de lecture)
- Quelle decision ou action ce document va-t-il alimenter ?
- Quelles informations sont absolument necessaires vs nice-to-have ?

#### 2. La regle du 80/20

Un bon template couvre 80% des cas d'usage avec 20% de la complexite possible. Ne pas essayer de couvrir tous les cas de figure dans un seul template. Preferer 3 templates simples a 1 template monolithique avec 50 champs optionnels.

#### 3. Sections obligatoires vs optionnelles

Marquer clairement les sections obligatoires et optionnelles. Formats recommandes :
- `## Section obligatoire` (sans annotation)
- `## Section optionnelle (si applicable)` (annotation explicite)
- Utiliser des callouts ou des toggles pour les sections optionnelles afin de ne pas encombrer visuellement

#### 4. Instructions inline

Inclure des instructions directement dans le template, en italique ou dans des callouts, pour guider le contributeur. Supprimer les instructions apres remplissage.

Exemple :
```markdown
## Contexte

_Decrire le probleme ou la situation en 3-5 phrases. Inclure les contraintes
et les dependencies. Eviter le jargon technique sauf si l'audience est technique._

[Votre texte ici]
```

#### 5. Exemples integres

Pour les templates complexes, inclure un exemple rempli en plus du template vide. L'exemple montre le niveau de detail attendu et leve les ambiguites.

### Templates par plateforme

#### Templates Notion

Notion propose 3 types de templates :

**1. Database templates** : templates applicables aux elements d'une database. Quand un nouvel element est cree dans la database, l'utilisateur peut choisir un template qui pre-remplit les proprietes et le contenu de la page.

Configuration :
- Ouvrir la database --> cliquer sur la fleche a cote de "New" --> "New template"
- Definir les proprietes par defaut (status, tags, owner)
- Definir le contenu de la page (structure, sections, instructions)
- Possibilite de creer plusieurs templates par database (ex : "Bug report", "Feature request", "Epic")

**2. Page templates / Template buttons** : boutons inseres dans une page qui creent du contenu predifini. Utiles pour les contenus repetitifs au sein d'une meme page.

Configuration :
- Inserer un bloc "Template button" (commande `/template`)
- Definir le label du bouton (ex : "Ajouter une entree journal")
- Definir le contenu a generer a chaque clic
- Le contenu peut inclure des mentions de date, des checkboxes, des liens

**3. Notion Templates Gallery** : templates publics partageables. Utiles pour distribuer des structures standardisees a l'echelle de l'organisation ou publiquement.

#### Templates Obsidian

Obsidian propose deux systemes de templates :

**1. Templates core plugin** : systeme natif simple. Les templates sont des fichiers Markdown dans un dossier dedie. Inserer un template copie le contenu du fichier dans la note courante.

Variables disponibles :
- `{{title}}` : titre de la note courante
- `{{date}}` : date du jour (format configurable)
- `{{time}}` : heure courante

**2. Templater plugin (communautaire)** : systeme avance avec syntaxe programmable.

Variables et commandes :
```
<% tp.date.now("YYYY-MM-DD") %>  // Date du jour
<% tp.file.title %>               // Titre du fichier
<% tp.file.creation_date() %>     // Date de creation
<% tp.system.prompt("Sujet ?") %> // Demander une saisie a l'utilisateur
<% tp.file.cursor() %>            // Placer le curseur ici apres insertion
```

Fonctionnalites avancees de Templater :
- **Folder templates** : appliquer automatiquement un template en fonction du dossier dans lequel la note est creee
- **Template on file creation** : appliquer un template automatiquement a la creation d'une nouvelle note
- **Scripts JavaScript** : executer des scripts JS dans les templates pour des transformations complexes
- **Commandes systeme** : executer des commandes shell depuis un template

---

## Systemes relationnels dans Notion

### Principes de conception relationnelle

#### 1. Identifier les entites

Avant de creer des databases, identifier les entites (les "choses" a tracker) et leurs relations :

| Question | Resultat |
|----------|----------|
| Qu'est-ce qu'on track ? | Entites --> Databases |
| Quelles sont les proprietes de chaque entite ? | Proprietes --> Colonnes |
| Comment les entites sont-elles liees ? | Relations --> Liens entre databases |
| Quelles agregations sont necessaires ? | Rollups --> Calculs sur les relations |

#### 2. Normaliser (mais pas trop)

Comme en conception de bases de donnees relationnelles, normaliser pour eviter la duplication. Mais ne pas sur-normaliser -- Notion n'est pas PostgreSQL. La regle : si une information est modifiee a un seul endroit et affichee a plusieurs, elle doit etre dans sa propre database reliee. Si elle est specifique a un seul contexte, une simple propriete suffit.

#### 3. La database source unique

Pour chaque type d'information, definir une database source unique (single source of truth). Les linked databases permettent d'afficher cette source dans differents contextes avec differents filtres et vues, sans dupliquer les donnees.

### Patterns relationnels avances

#### Pattern 1 : Master-Detail

Une database "master" (vue d'ensemble) reliee a une database "detail" (elements granulaires).

```
[Projects] 1 -----> N [Tasks]
   |
   +-- Proprietes : Nom, Status, Owner, Deadline
   +-- Rollups depuis Tasks : Count, % Done, Next deadline

[Tasks]
   +-- Proprietes : Nom, Status, Assignee, Due date, Effort
   +-- Relation : Project (select parmi les projets existants)
```

#### Pattern 2 : Hub central

Une database centrale reliee a plusieurs databases peripheriques.

```
                    [Meetings]
                        |
[Tasks] ---- [Projects] ---- [Documents]
                        |
                    [Risks]
                        |
                    [Decisions]
```

Le projet sert de hub : en ouvrant une page projet, on accede a toutes les taches, reunions, documents, risques et decisions associes via les relations.

#### Pattern 3 : Many-to-Many avec database de jonction

Quand deux entites ont une relation many-to-many avec des attributs sur la relation, creer une database de jonction.

```
[Contacts] N -----> N [Skills]

Devient :

[Contacts] 1 --> N [Contact-Skills] N <-- 1 [Skills]
                        |
                        +-- Niveau (Junior/Senior/Expert)
                        +-- Date de validation
                        +-- Certifie (checkbox)
```

#### Pattern 4 : Self-reference (hierarchie)

Une database reliee a elle-meme pour creer des hierarchies dans une seule database.

```
[Pages Wiki]
   +-- Propriete : Titre, Contenu, Owner, Tags
   +-- Relation "Parent" : --> [Pages Wiki] (self-reference)
   +-- Relation "Children" : <-- [Pages Wiki] (reciproque automatique)
```

Cela permet de construire une arborescence dans une seule database, avec une vue Board groupee par "Parent" ou une vue Table avec filtres sur la profondeur.

#### Pattern 5 : Pipeline / Workflow

Une database avec une propriete Status structuree comme un pipeline, enrichie de relations vers les databases d'historique et de metadata.

```
[Deals]
   +-- Status : Lead --> Qualified --> Proposal --> Negotiation --> Closed Won / Lost
   +-- Relation --> [Companies]
   +-- Relation --> [Contacts]
   +-- Relation --> [Activities] (calls, emails, meetings)

[Activities]
   +-- Type : Call, Email, Meeting, Note
   +-- Date, Notes, Outcome
   +-- Relation --> [Deals]
   +-- Relation --> [Contacts]
```

### Design de dashboards

#### Principes de conception de dashboards Notion

1. **One-glance understanding** : le dashboard doit communiquer l'etat du systeme en moins de 5 secondes. Utiliser des callouts colores, des proprietes Status, et des rollups pour les KPIs cles.

2. **Actionable, pas decoratif** : chaque element du dashboard doit permettre une action ou une decision. Eviter les metriques "vanity" qui ne declenchent aucune action.

3. **Structure en grille** : utiliser les colonnes Notion pour creer une mise en page en grille. Format recommande : 2-3 colonnes pour les KPIs en haut, puis des linked databases filtrees en dessous.

4. **Linked databases filtrees** : le dashboard n'est pas une nouvelle database -- c'est un assemblage de linked databases avec des filtres specifiques. Ex : "Taches urgentes" = linked database filtree sur Priority = "Haute" et Status != "Done".

#### Template de dashboard projet

```
# Dashboard Projet [Nom]

## Colonnes KPI (layout 3 colonnes)

| Avancement | Budget | Risques |
|------------|--------|---------|
| [Rollup % taches done] | [Budget consomme / total] | [Count risques ouverts] |
| Barre de progression | Barre de progression | Indicateur couleur |

## Taches prioritaires
[Linked database "Taches" filtree : Project = [ce projet] AND Status != Done, tri Priority desc, limit 10]

## Prochaines deadlines
[Linked database "Taches" filtree : Project = [ce projet] AND Due date = Next 14 days, tri Date asc]

## Decisions recentes
[Linked database "Decisions" filtree : Project = [ce projet], tri Date desc, limit 5]

## Risques ouverts
[Linked database "Risques" filtree : Project = [ce projet] AND Status = Open, tri Severite desc]
```

---

## Automatisation des workflows de connaissances

### Patterns d'automatisation

#### 1. Capture automatisee

| Source | Outil d'automatisation | Destination | Declencheur |
|--------|----------------------|-------------|-------------|
| Email important | Zapier / Make | Database Notion "Inbox" | Label Gmail ou regle Outlook |
| Article web | Notion Web Clipper / Readwise | Database "Lectures" | Clic sur l'extension navigateur |
| Message Slack | Slack workflow + Notion API | Database "Captures Slack" | Emoji reaction (ex : :bookmark:) |
| Reunion (transcription) | Otter.ai / Fireflies + API | Page Notion "CR Reunions" | Fin de reunion Google Meet/Zoom |
| Tweet / post LinkedIn | IFTTT / Zapier | Database "Veille" | Bookmark ou like |
| Highlight Kindle | Readwise | Database "Notes de lecture" | Sync automatique quotidienne |

#### 2. Traitement automatise

| Declencheur | Action | Implementation |
|-------------|--------|----------------|
| Nouvelle page dans "Inbox" | Notifier le owner | Notion automation + Slack |
| Page non traitee depuis 7 jours | Relance email | Zapier + condition sur date |
| Status passe a "Published" | Ajouter au MOC correspondant | Notion automation (modifier une relation) |
| Deadline dans 3 jours | Rappel Slack | Notion automation + Slack integration |
| Page non consultee depuis 180 jours | Suggerer l'archivage | Script API Notion + notification |

#### 3. Distribution automatisee

| Contenu | Canal | Frequence | Implementation |
|---------|-------|-----------|----------------|
| Digest des nouvelles pages | Email ou Slack | Hebdomadaire | Script API + newsletter interne |
| Pages mises a jour | Channel Slack dedie | Quotidien | Notion automation + Slack |
| Metriques du wiki | Dashboard Notion | Temps reel | Rollups et formules Notion |
| Rapport de sante du wiki | Email a la direction | Mensuel | Script API + rapport PDF |

### Automatisation avec Make (ex-Integromat)

Make est l'outil d'automatisation le plus flexible pour les workflows Notion :

#### Scenario type : Capture Slack vers Notion

```
Declencheur : Reaction emoji :notion: sur un message Slack
|
+-- Module 1 : Watch Slack reactions
+-- Module 2 : Get message content
+-- Module 3 : Create Notion page
|   +-- Database : "Captures Slack"
|   +-- Properties :
|       - Title = premiers 50 caracteres du message
|       - Source = "Slack"
|       - Channel = nom du channel
|       - Author = nom de l'auteur
|       - Date = date du message
|       - Status = "Inbox"
|   +-- Content : texte complet du message + lien vers l'original
+-- Module 4 : Reply Slack (confirmation)
```

#### Scenario type : Audit automatise de freshness

```
Declencheur : Schedule (tous les lundis a 9h)
|
+-- Module 1 : Query Notion database "Documents"
|   +-- Filtre : Last edited time < 180 jours ago
|   +-- Filtre : Status = "Published"
|
+-- Module 2 : Iterer sur les resultats
|   |
|   +-- Module 3 : Send Slack DM au Content Owner
|       +-- Message : "La page [titre] n'a pas ete mise a jour
|           depuis [X] jours. Veuillez la revoir ou la proposer
|           a l'archivage."
|
+-- Module 4 : Update Notion pages
|   +-- Ajouter tag "Review needed"
```

### Automatisation avec l'API Notion (Python)

Pour les automations complexes ou personnalisees, utiliser l'API Notion directement :

```python
# Exemple : script d'audit des pages orphelines
import requests
from datetime import datetime, timedelta

NOTION_TOKEN = "ntn_YOUR_TOKEN_HERE"
DATABASE_ID = "your_database_id"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# 1. Recuperer toutes les pages
def get_all_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    pages = []
    has_more = True
    next_cursor = None

    while has_more:
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        pages.extend(data["results"])
        has_more = data["has_more"]
        next_cursor = data.get("next_cursor")

    return pages

# 2. Identifier les pages orphelines (sans liens entrants)
def find_orphan_pages(pages):
    # Extraire tous les IDs mentionnes dans les contenus
    linked_ids = set()
    for page in pages:
        # Recuperer les blocs de la page
        blocks_url = f"https://api.notion.com/v1/blocks/{page['id']}/children"
        blocks = requests.get(blocks_url, headers=headers).json()
        for block in blocks.get("results", []):
            # Chercher les mentions de pages
            if block.get("type") == "paragraph":
                for text in block["paragraph"].get("rich_text", []):
                    if text.get("type") == "mention":
                        mention = text["mention"]
                        if mention.get("type") == "page":
                            linked_ids.add(mention["page"]["id"])

    # Identifier les pages jamais mentionnees
    all_ids = {page["id"] for page in pages}
    orphans = all_ids - linked_ids

    return [p for p in pages if p["id"] in orphans]

# 3. Taguer les pages orphelines
def tag_orphans(orphan_pages):
    for page in orphan_pages:
        url = f"https://api.notion.com/v1/pages/{page['id']}"
        payload = {
            "properties": {
                "Tags": {
                    "multi_select": [
                        {"name": "orphan"},
                        {"name": "review-needed"}
                    ]
                }
            }
        }
        requests.patch(url, headers=headers, json=payload)
```

---

## Scaling des systemes de connaissances

### Du personnel au collectif

#### Phase 1 : Systeme personnel (1 personne)

| Aspect | Configuration |
|--------|---------------|
| **Outil** | Obsidian ou Notion personnel |
| **Methode** | PARA + Zettelkasten |
| **Structure** | 4 dossiers PARA + Inbox |
| **Maintenance** | Weekly review (30 min) |
| **Volume** | 50-500 notes |

#### Phase 2 : Systeme d'equipe (5-20 personnes)

| Aspect | Configuration |
|--------|---------------|
| **Outil** | Notion Team ou Confluence |
| **Methode** | PARA adapte + templates + conventions |
| **Structure** | Teamspace + databases relationnelles |
| **Roles** | 1 wiki champion + content owners par domaine |
| **Maintenance** | Weekly review individuelle + monthly review equipe |
| **Volume** | 200-2000 pages |
| **Governance** | Convention de nommage + templates obligatoires + cycle de revue |

**Actions cles pour le passage personnel --> equipe :**
1. Migrer les connaissances partagees du systeme personnel vers le wiki d'equipe
2. Garder le systeme personnel pour les notes de reflexion et les captures brutes
3. Definir la frontiere entre ce qui est prive et ce qui est partage
4. Creer des templates d'equipe valides par consensus
5. Nommer un wiki champion responsable de la sante du systeme

#### Phase 3 : Systeme departemental (20-100 personnes)

| Aspect | Configuration |
|--------|---------------|
| **Outil** | Notion Business ou Confluence Standard |
| **Methode** | Information Architecture formelle + gouvernance documentaire |
| **Structure** | Teamspaces par equipe + espace transversal + hub de navigation |
| **Roles** | Knowledge Manager + space owners + content owners |
| **Maintenance** | Cycle de revue trimestriel + audit semestriel |
| **Volume** | 1000-10 000 pages |
| **Governance** | Politique documentaire formelle + permissions par role + archivage automatise |

**Actions cles pour le passage equipe --> departement :**
1. Definir une architecture d'information globale avec taxonomie unifiee
2. Nommer un Knowledge Manager a temps partiel (20-40%)
3. Formaliser la politique documentaire (creation, revue, archivage)
4. Mettre en place des metriques de sante du wiki
5. Integrer la contribution au wiki dans les objectifs individuels

#### Phase 4 : Systeme d'entreprise (100+ personnes)

| Aspect | Configuration |
|--------|---------------|
| **Outil** | Confluence Premium/Enterprise ou Notion Enterprise |
| **Methode** | Knowledge Management formel + IA |
| **Structure** | Federation d'espaces + portail central + recherche unifiee |
| **Roles** | Head of Knowledge Management + team de KM |
| **Maintenance** | Processus continu avec equipe dediee |
| **Volume** | 10 000-100 000+ pages |
| **Governance** | Politique d'entreprise + SSO/SCIM + compliance + audit trail |

**Actions cles pour le passage departement --> entreprise :**
1. Creer une equipe Knowledge Management dediee (2-5 personnes)
2. Deployer un portail central de navigation cross-departement
3. Mettre en place la recherche unifiee (Notion AI Q&A, Confluence AI, ou outil tiers)
4. Definir des SLA de freshness par type de contenu
5. Integrer le wiki dans les processus critiques (onboarding, incident management, decision-making)
6. Implementer le RAG (Retrieval-Augmented Generation) pour un chatbot interne alimente par le wiki

### Gestion des conflits de scaling

| Conflit | Cause | Resolution |
|---------|-------|------------|
| **Duplication de contenu** | Plusieurs equipes documentent le meme sujet | Definir un owner unique par sujet, utiliser des linked databases |
| **Fragmentation des espaces** | Trop de teamspaces sans navigation transversale | Creer un portail central avec liens vers tous les espaces |
| **Inconsistance des formats** | Chaque equipe invente ses templates | Definir des templates globaux obligatoires + templates locaux optionnels |
| **Surcharge d'information** | Volume trop important, recherche noye | Archiver agressivement, ameliorer le tagging, deployer la recherche IA |
| **Permissions complexes** | Trop de niveaux de permissions, acces refuse a tort | Simplifier : 3 niveaux max (public interne, equipe, confidentiel) |

---

## Gestion du cycle de vie du contenu

### Les 5 etapes du cycle de vie

```
1. CREATION
   |
   +-- Template selectionne
   +-- Contenu redige
   +-- Proprietes remplies (owner, tags, type)
   +-- Statut : "Draft"
   |
2. REVUE
   |
   +-- Reviewer assigne
   +-- Feedback donne (commentaires Notion/Confluence)
   +-- Corrections appliquees
   +-- Statut : "In Review"
   |
3. PUBLICATION
   |
   +-- Reviewer valide
   +-- Page visible par l'audience cible
   +-- Liens ajoutes depuis les MOC et pages connexes
   +-- Notification aux parties prenantes
   +-- Statut : "Published"
   |
4. MAINTENANCE
   |
   +-- Revue periodique (selon le type de contenu)
   +-- Mise a jour lors de changements factuels
   +-- Enrichissement progressif
   +-- Statut : "Published" (date de derniere mise a jour visible)
   |
5. ARCHIVAGE
   |
   +-- Contenu obsolete identifie (audit ou metrique automatique)
   +-- Confirmation du Content Owner
   +-- Bandeau "Archive" ajoute avec lien vers le remplacement si applicable
   +-- Deplace dans l'espace Archive
   +-- Statut : "Archived"
```

### SLA de freshness par type de contenu

| Type de contenu | Frequence de revue | SLA de mise a jour apres changement | Owner |
|-----------------|-------------------|--------------------------------------|-------|
| Processus operationnel | Trimestriel | 48h | Process Owner |
| Documentation technique | Semestriel | 1 semaine | Tech Lead |
| Runbook | Apres chaque incident | 24h | On-call engineer |
| Policy / Guideline | Annuel | 1 mois | Department Head |
| Onboarding guide | Trimestriel | 1 semaine | HR / Manager |
| ADR / Decision log | Jamais (snapshot) | N/A | Auteur |
| Meeting notes | Jamais (snapshot) | N/A | Scribe |
| FAQ | Mensuel | 48h | Support / Knowledge Manager |
| Glossaire | Trimestriel | 1 semaine | Knowledge Manager |

---

## Backup et export

### Strategies de backup

#### Pourquoi sauvegarder un wiki cloud ?

Meme avec des outils cloud fiables (Notion, Confluence), le backup est necessaire pour :
- **Protection contre les erreurs humaines** : suppression accidentelle de pages, modifications erronees
- **Conformite et audit** : certaines reglementations exigent des sauvegardes independantes
- **Portabilite** : pouvoir migrer vers un autre outil sans dependre du fournisseur
- **Continuite d'activite** : acces aux connaissances meme en cas de panne du fournisseur

#### Methodes de backup par outil

**Notion :**
- **Export natif** : Settings --> Export all workspace content (Markdown + CSV ou HTML). Manuel, a planifier mensuellement.
- **API automatisee** : script qui exporte toutes les pages via l'API Notion, a planifier quotidiennement ou hebdomadairement.
- **Outils tiers** : Notion Backups (SaaS), notion-backup (open source), Notabase.
- **Format recommande** : Markdown pour la portabilite, HTML pour la fidelite visuelle.

**Confluence :**
- **Export natif** : Space settings --> Export space (HTML, XML, PDF). Manuel, par space.
- **Administration** : Site administration --> Backup manager (export complet du site). Necessite les droits admin.
- **API automatisee** : script utilisant l'API Confluence pour exporter le contenu.
- **Outils tiers** : Confluence Backup plugins, scripts open source.

**Obsidian :**
- **Backup natif** : le vault est un dossier local -- le backup est un simple backup de fichiers.
- **Git** : utiliser le plugin Obsidian Git pour versionner le vault sur GitHub/GitLab. Commit automatique toutes les heures ou quotidien.
- **Cloud sync** : Syncthing, iCloud, Google Drive, ou Obsidian Sync (payant).

#### Script de backup Notion (structure)

```python
# Structure d'un script de backup Notion
# Execution : cron job quotidien a 3h du matin

import os
import json
import requests
from datetime import datetime

NOTION_TOKEN = "ntn_YOUR_TOKEN_HERE"
BACKUP_DIR = "/path/to/backups"
DATE = datetime.now().strftime("%Y-%m-%d")

def backup_database(database_id, name):
    """Exporter tous les elements d'une database en JSON"""
    output_dir = os.path.join(BACKUP_DIR, DATE, name)
    os.makedirs(output_dir, exist_ok=True)

    # Query all pages
    pages = query_all_pages(database_id)

    for page in pages:
        # Export properties
        page_data = {
            "id": page["id"],
            "properties": page["properties"],
            "created_time": page["created_time"],
            "last_edited_time": page["last_edited_time"]
        }

        # Export content (blocks)
        blocks = get_all_blocks(page["id"])
        page_data["content"] = blocks

        # Save to file
        filename = sanitize_filename(get_title(page)) + ".json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(page_data, f, ensure_ascii=False, indent=2)

    print(f"Backed up {len(pages)} pages from {name}")

def cleanup_old_backups(keep_days=30):
    """Supprimer les backups de plus de 30 jours"""
    # Implementation de la rotation des backups
    pass

# Executer le backup
databases_to_backup = [
    ("database_id_1", "Projects"),
    ("database_id_2", "Documents"),
    ("database_id_3", "Tasks"),
]

for db_id, name in databases_to_backup:
    backup_database(db_id, name)

cleanup_old_backups(keep_days=30)
```

### Strategie de retention

| Type de backup | Frequence | Retention | Stockage |
|----------------|-----------|-----------|----------|
| **Snapshot quotidien** | Quotidien | 30 jours | Cloud storage (S3, GCS) |
| **Snapshot hebdomadaire** | Hebdomadaire | 12 semaines | Cloud storage |
| **Archive mensuelle** | Mensuel | 24 mois | Cold storage |
| **Archive annuelle** | Annuel | 7 ans (conformite) | Cold storage + offline |

### Export pour migration

Lors d'une migration vers un autre outil, l'export doit preserver :

1. **Le contenu** : texte, images, fichiers attaches
2. **La structure** : hierarchie des pages, navigation
3. **Les metadonnees** : proprietes, tags, dates, owners
4. **Les relations** : liens entre pages, relations entre databases
5. **L'historique** : versions precedentes si disponibles

#### Checklist d'export pour migration

- [ ] Exporter toutes les pages en Markdown (portabilite maximale)
- [ ] Exporter les databases en CSV (metadonnees structurees)
- [ ] Telecharger tous les fichiers attaches (images, PDF, documents)
- [ ] Documenter les relations entre databases (schema relationnel)
- [ ] Exporter les templates separement
- [ ] Verifier la completude de l'export (nombre de pages source vs export)
- [ ] Tester l'import dans l'outil cible avec un echantillon
- [ ] Documenter les pertes de fidelite (formatage, fonctionnalites non supportees)

---

## Anti-patterns de templates et systemes

### Les erreurs les plus courantes

1. **Le template cathedrale** : un template avec 40 champs obligatoires qui decoure tout contributeur. Resultat : le template est contourne ou rempli a minima. Solution : 5-7 champs obligatoires maximum, le reste en optionnel.

2. **La database tentaculaire** : une seule database qui tente de tout tracker (projets, taches, documents, contacts, idees). Resultat : 50 proprietes, vues illisibles, performance degradee. Solution : une database par entite, reliees entre elles.

3. **L'automatisation prematuree** : automatiser des workflows avant de les avoir valides manuellement. Resultat : automations qui propagent des erreurs a grande echelle. Solution : pratiquer manuellement pendant 4-6 semaines, puis automatiser les patterns valides.

4. **Le dashboard decoratif** : un dashboard visuellement seduisant mais sans donnees actionnables. Resultat : le dashboard est consulte une fois puis oublie. Solution : chaque metrique du dashboard doit declencher une action si elle depasse un seuil.

5. **La migration big bang** : migrer tout le contenu d'un coup vers un nouveau systeme sans pilote ni formation. Resultat : confusion, perte de productivite, retour a l'ancien outil. Solution : migration par lots avec pilote sur une equipe avant deploiement generalise.

6. **L'absence de meta-documentation** : le systeme de connaissances n'est pas lui-meme documente. Resultat : seul le createur sait comment le systeme fonctionne. Solution : documenter les conventions, les templates, les workflows et les roles dans une section "Meta" du wiki.

7. **Le versioning implicite** : pas de systeme de gestion de versions pour les documents critiques. Resultat : on ne sait pas quelle version est la derniere, les modifications sont perdues. Solution : utiliser l'historique de versions de Notion/Confluence, ou versionner explicitement les documents critiques (v1.0, v1.1, v2.0).
