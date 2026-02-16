# Edition Collaborative — Google Docs, Co-authoring, Revision, Workflow d'Approbation

## Overview

Ce document de reference couvre l'ensemble des pratiques d'edition collaborative de documents : fonctionnalites collaboratives de Google Docs, co-edition dans Microsoft Word (desktop et web), bonnes pratiques du suivi des modifications (Track Changes), workflows de commentaires, mode suggestion, workflows d'approbation multi-niveaux, historique des versions, resolution de conflits, controle d'acces et directives de redaction collaborative. Utiliser ce guide pour mettre en place des processus de collaboration documentaire efficaces, garantissant la qualite du contenu, la tracabilite des modifications et la fluidite des circuits de validation.

---

## Google Docs — Collaboration Native en Temps Reel

### Architecture collaborative de Google Docs

Google Docs a ete concu des l'origine comme un outil de collaboration en temps reel. Son architecture repose sur le modele OT (Operational Transformation) qui permet a plusieurs utilisateurs d'editer simultanement le meme document sans conflits de donnees.

### Fonctionnalites collaboratives cles

#### Co-edition en temps reel
- **Presence** : chaque utilisateur connecte au document est identifie par un curseur de couleur unique avec son nom. On voit en permanence qui edite quoi et ou.
- **Modifications instantanees** : les modifications apparaissent en temps reel pour tous les participants, avec une latence inferieure a 200 millisecondes dans des conditions reseau normales.
- **Pas de verrouillage** : contrairement aux systemes traditionnels, aucune section n'est verrouillee. Deux utilisateurs peuvent editer le meme paragraphe simultanement, le systeme OT resolvant les conflits en temps reel.
- **Hors ligne** : Google Docs supporte l'edition hors ligne (via Chrome et l'extension Google Docs Offline). Les modifications sont synchronisees automatiquement lors de la reconnexion.

#### Mode Suggestion
Le mode Suggestion de Google Docs est l'equivalent du Track Changes de Word, mais natif au cloud :
- **Activation** : cliquer sur l'icone de mode d'edition (crayon en haut a droite) et selectionner "Suggestion" (au lieu de "Edition").
- **Visualisation** : les suggestions apparaissent en couleur (differente par auteur) avec un texte barre pour les suppressions et un texte colore pour les ajouts.
- **Acceptation/Rejet** : chaque suggestion peut etre acceptee (coche) ou rejetee (croix) individuellement. L'auteur du document ou un editeur peut traiter les suggestions.
- **Commentaire sur suggestion** : on peut ajouter un commentaire a une suggestion pour expliquer le raisonnement ou discuter de la modification proposee.

#### Commentaires et mentions
- **Commentaires contextuels** : selectionner du texte puis Ctrl+Alt+M (ou clic droit > Commenter) pour ajouter un commentaire ancre au texte selectionne.
- **Mentions** : utiliser @nom ou @email dans un commentaire pour notifier un collegue. Le collegue recoit une notification par email avec un lien direct vers le commentaire.
- **Assignation** : cocher "Assigner a [nom]" pour transformer un commentaire en tache assignee. L'assigne recoit une notification et peut marquer la tache comme terminee.
- **Resolution** : un commentaire peut etre "Resolu" une fois traite. Les commentaires resolus sont archives mais restent accessibles via le menu Commentaires.
- **Fil de discussion** : chaque commentaire supporte un fil de discussion (replies) pour les echanges multi-tours.

#### Historique des versions
- **Historique complet** : Google Docs enregistre chaque modification avec l'auteur et l'horodatage, creant un historique complet et permanent.
- **Versions nommees** : on peut nommer une version specifique (Fichier > Historique des versions > Nommer la version actuelle) pour marquer un jalon (ex. : "Version soumise au client", "Version approuvee COMEX").
- **Restauration** : on peut restaurer n'importe quelle version anterieure. La restauration cree un point de version nomme automatiquement ("Avant restauration").
- **Comparaison** : on peut comparer la version actuelle avec n'importe quelle version anterieure pour visualiser les differences.

### Controle d'acces dans Google Docs

| Niveau d'acces | Droits | Usage typique |
|---|---|---|
| **Proprietaire** | Tout (edition, partage, suppression, transfert) | Createur du document |
| **Editeur** | Edition du contenu, ajout de commentaires, suggestion, partage | Co-auteurs, relecteurs principaux |
| **Commentateur** | Ajout de commentaires et suggestions, pas d'edition directe | Relecteurs, parties prenantes |
| **Lecteur** | Lecture seule, pas de commentaires | Distribution finale, archives |

#### Options de partage avancees
- **Lien partage** : partage par lien avec choix du niveau d'acces (lecteur, commentateur, editeur). Le lien peut etre restreint aux membres de l'organisation (Google Workspace).
- **Partage par email** : partage direct avec des utilisateurs specifiques, avec notification par email.
- **Date d'expiration** : pour les partages temporaires, definir une date d'expiration apres laquelle l'acces est automatiquement revoque (fonctionnalite Google Workspace Business/Enterprise).
- **Empechement de telecharcement** : option pour empecher les lecteurs et commentateurs de telecharger, imprimer ou copier le document.
- **Approbation de transfert** : option pour empecher les editeurs de modifier les parametres de partage ou d'ajouter de nouveaux utilisateurs.

### Google Docs — Fonctionnalites avancees pour la collaboration

#### Smart Chips
Les Smart Chips sont des elements interactifs inseres directement dans le texte du document :
- **@Personne** : insere un chip avec le nom, la photo et les coordonnees d'un collegue. Permet de voir rapidement la disponibilite et de demarrer une conversation.
- **@Fichier** : insere un lien riche vers un autre fichier Google (Docs, Sheets, Slides, PDF) avec apercu au survol.
- **@Date** : insere une date interactive avec rappel optionnel et integration Google Calendar.
- **@Reunion** : insere un lien vers une reunion Google Meet avec les details (participants, heure).
- **@Tache** : cree une tache Google Tasks directement depuis le document, avec assignation et echeance.

#### Building Blocks dans Google Docs
Google Docs propose des blocs de construction pre-configures accessibles via le menu Insertion ou en tapant "@" :
- **Tableau de suivi de projet** : tableau pre-formate avec colonnes (tache, responsable, statut, echeance).
- **Notes de reunion** : structure pre-formatee (date, participants, ordre du jour, decisions, actions).
- **Email draft** : modele de brouillon d'email integre dans le document.
- **Dropdown chips** : menus deroulants personnalisables integres dans le texte (statut : En cours / Termine / Bloque).

#### Variables dans Google Docs (2025-2026)
Google Docs a introduit les variables (Smart Chips Variables) qui permettent de definir une valeur une seule fois et de l'utiliser partout dans le document :
1. Inserer une variable : Insertion > Smart Chips > Variables.
2. Nommer la variable (ex. : "Nom du client", "Date du projet").
3. Saisir la valeur une seule fois.
4. Inserer la meme variable a d'autres endroits du document — elle affiche automatiquement la meme valeur.
5. Modifier la valeur a un endroit — elle se met a jour partout.

Cette fonctionnalite est particulierement utile pour les templates ou les memes informations (nom du client, date, reference) apparaissent a plusieurs endroits.

---

## Microsoft Word — Co-edition et Collaboration

### Co-edition dans Word (OneDrive / SharePoint)

Microsoft Word supporte la co-edition en temps reel depuis Word 2016, a condition que le document soit stocke sur OneDrive ou SharePoint :

#### Word Desktop (application bureau)
- **Enregistrement automatique** : quand le document est stocke sur OneDrive/SharePoint, l'enregistrement automatique s'active (bouton en haut a gauche). Chaque modification est sauvegardee automatiquement toutes les quelques secondes.
- **Indicateurs de presence** : les co-editeurs sont affiches dans la barre de titre. Leur curseur et leur zone d'edition sont signales par un drapeau de couleur dans le document.
- **Resolution de conflits** : si deux utilisateurs modifient le meme paragraphe, Word detecte le conflit et affiche une notification permettant de choisir quelle version conserver.
- **Commentaires et @mentions** : fonctionnement similaire a Google Docs — commentaires ancres au texte, mentions avec notification, fils de discussion.

#### Word Online (application web)
- **Co-edition complete** : Word Online offre une co-edition en temps reel comparable a Google Docs, avec des curseurs de couleur et des modifications instantanees.
- **Fonctionnalites reduites** : Word Online ne supporte pas toutes les fonctionnalites de Word Desktop (macros, champs avances, certaines options de mise en page). Les fonctionnalites manquantes sont accessibles en ouvrant le document dans l'application desktop ("Ouvrir dans l'application de bureau").
- **Pas d'installation requise** : fonctionne dans n'importe quel navigateur web, ce qui facilite la collaboration avec des parties prenantes externes qui n'ont pas Word installe.

### Track Changes dans Word — Bonnes Pratiques

#### Configuration recommandee

| Parametre | Configuration recommandee | Raison |
|---|---|---|
| **Affichage des modifications** | Balisage simple (Simple Markup) | Vue propre avec indicateurs discrets |
| **Insertions** | Souligne, couleur par auteur | Identification claire des ajouts |
| **Suppressions** | Barre, couleur par auteur | Identification claire des retraits |
| **Deplacements** | Activer le suivi des deplacements | Distinguer deplacement et suppression + ajout |
| **Formatage** | Activer le suivi du formatage | Detecter les changements de style |
| **Bulles** | Montrer les revisions dans les bulles pour le formatage uniquement | Evite l'encombrement visuel |
| **Volet de revision** | Afficher le volet vertical | Navigation rapide entre les modifications |

#### Processus de revision structure

```
CYCLE DE REVISION DOCUMENTAIRE

Phase 1 — Redaction (Auteur)
├── Rediger le contenu avec les styles du template
├── Completer les metadonnees (auteur, version, date)
├── Executer le verificateur d'accessibilite et corriger les erreurs
└── Sauvegarder en v0.1 (brouillon)

Phase 2 — Auto-revision (Auteur)
├── Relire a froid (attendre au moins 24h si possible)
├── Verifier la structure (table des matieres coherente)
├── Verifier les references croisees (Ctrl+A, F9)
├── Passer le correcteur orthographique et grammatical
└── Sauvegarder en v0.9 (pret pour revue)

Phase 3 — Revue par les pairs (Relecteurs)
├── Activer le suivi des modifications (Ctrl+Shift+E)
├── Chaque relecteur fait UN SEUL passage
├── Utiliser le mode Suggestion (pas d'edition directe)
├── Commenter pour les modifications complexes ou debattables
├── Chaque relecteur enregistre sa version revisee
└── L'auteur combine les revisions (Revision > Combiner)

Phase 4 — Integration (Auteur)
├── Passer en revue chaque modification (Accepter/Rejeter + Suivante)
├── Repondre aux commentaires (resoudre ou discuter)
├── Appliquer les corrections retenues
├── Mettre a jour les references croisees et la table des matieres
└── Sauvegarder en v1.0 (version finale candidate)

Phase 5 — Validation finale (Approbateur)
├── Lecture finale du document propre (sans marques de revision)
├── Validation formelle (signature, approbation electronique)
├── Verification que toutes les marques de revision ont ete traitees
│   └── Revision > Verifier le document (aucune donnee personnelle, aucune marque residuelle)
└── Publication / distribution de la version finale
```

### Comparaison Google Docs vs. Word pour la Collaboration

| Critere | Google Docs | Microsoft Word (OneDrive/SharePoint) |
|---|---|---|
| **Co-edition temps reel** | Natif, fluide, sans conflit | Natif (web), avec conflits occasionnels (desktop) |
| **Mode Suggestion** | Integre, intuitif | Track Changes, plus puissant mais plus complexe |
| **Commentaires** | Simples, @mentions, assignation | @mentions, fil de discussion, pas d'assignation native |
| **Historique** | Illimite, automatique, versions nommees | Historique des versions (OneDrive/SharePoint) |
| **Hors ligne** | Chrome uniquement (extension requise) | Word Desktop (natif), synchronisation OneDrive |
| **Mise en forme avancee** | Limitee (pas de champs, macros limitees) | Completes (styles, champs, macros, publipostage) |
| **Controle d'acces** | Proprietaire, editeur, commentateur, lecteur | Permissions SharePoint (granulaires, heritees) |
| **Integration** | Google Workspace (Sheets, Slides, Calendar) | Microsoft 365 (Excel, PowerPoint, Teams, Outlook) |
| **Formats de sortie** | PDF, DOCX, ODT, RTF, TXT, HTML, EPUB | PDF, DOCX, ODT, RTF, TXT, HTML, XPS |
| **Accessibilite** | Bon | Excellent (verificateur integre) |
| **Convient pour** | Collaboration rapide, documents simples a moyens | Documents complexes, mise en forme avancee |

---

## Workflows d'Approbation Documentaire

### Types de workflows d'approbation

| Type | Description | Complexite | Outils |
|---|---|---|---|
| **Sequentiel** | Approbation en serie (A, puis B, puis C) | Faible | Email, SharePoint, Power Automate |
| **Parallele** | Approbation simultanee (A ET B ET C) | Moyenne | SharePoint, Power Automate |
| **Conditionnel** | Approbation selon des conditions (si montant > 10K, ajouter le CFO) | Elevee | Power Automate, outils dedies |
| **Hierarchique** | Approbation en escalade (manager, directeur, DG) | Moyenne | SharePoint, Power Automate, SAP |
| **Consensus** | Approbation a la majorite ou a l'unanimite | Elevee | Outils dedies, vote electronique |

### Workflow d'approbation dans SharePoint

SharePoint offre des workflows d'approbation natifs pour les documents stockes dans les bibliotheques de documents :

#### Configuration d'un workflow d'approbation standard
1. **Bibliotheque de documents** : stocker les documents dans une bibliotheque SharePoint avec les colonnes de metadonnees appropriees (statut, version, auteur, date de soumission).
2. **Workflow natif** : activer le workflow d'approbation integre a SharePoint (Parametres de la bibliotheque > Parametres du workflow > Ajouter un workflow > Approbation).
3. **Configuration** : definir les approbateurs (individus ou groupes), le type de workflow (sequentiel ou parallele), le delai d'approbation, et les actions en cas de rejet ou d'expiration.
4. **Demarrage** : le workflow peut etre demarre automatiquement (a la creation ou modification d'un document) ou manuellement par l'auteur.
5. **Traitement** : chaque approbateur recoit une notification (email et/ou Teams) avec un lien vers le document et les options Approuver/Rejeter/Demander des modifications.
6. **Conclusion** : une fois tous les approbateurs ayant rendu leur decision, le statut du document est mis a jour (Approuve, Rejete, ou En revision).

### Workflow d'approbation avec Power Automate

Power Automate permet de creer des workflows d'approbation plus complexes et personnalises :

#### Exemple : workflow d'approbation conditionnelle

```
DECLENCHEUR : Nouveau fichier dans SharePoint > Bibliotheque "Contrats"

CONDITION 1 : Montant du contrat (propriete du document)
├── Montant <= 10 000 EUR
│   └── APPROBATION : Manager direct (sequentiel)
│       ├── Approuve → Statut = "Approuve", notification auteur
│       └── Rejete → Statut = "Rejete", notification auteur avec commentaires
│
├── 10 000 EUR < Montant <= 50 000 EUR
│   └── APPROBATION : Manager + Directeur BU (sequentiel)
│       ├── Manager approuve → Envoyer au Directeur BU
│       │   ├── Directeur approuve → Statut = "Approuve"
│       │   └── Directeur rejette → Retour a l'auteur
│       └── Manager rejette → Retour a l'auteur
│
└── Montant > 50 000 EUR
    └── APPROBATION : Manager + Directeur BU + DAF + DG (sequentiel)
        ├── Chaque approbateur doit approuver avant passage au suivant
        ├── Tout rejet → Retour a l'auteur avec commentaires
        └── Toutes approbations → Statut = "Approuve", notification auteur

APRES APPROBATION :
├── Generer le PDF final (connecteur Word Online)
├── Envoyer pour signature electronique (connecteur DocuSign)
├── Archiver dans la bibliotheque "Contrats signes"
└── Mettre a jour le CRM (connecteur Dynamics/Salesforce)
```

### Workflow d'approbation dans Google Workspace

Google Workspace propose des fonctionnalites d'approbation natives (disponibles avec les editions Business Standard et superieures) :

#### Approbation de fichiers Google Docs
1. Ouvrir le document dans Google Docs.
2. Aller dans Fichier > Approbations.
3. Ajouter les approbateurs et definir la date limite.
4. Chaque approbateur peut Approuver, Demander des modifications, ou Rejeter.
5. Le statut d'approbation est visible directement dans le document et dans Google Drive.

#### Limites
- Workflow simple (un seul niveau, pas de conditions).
- Pour des workflows complexes, utiliser Google Apps Script ou des outils tiers (Kissflow, ProcessMaker, Wrk).

---

## Resolution de Conflits et Gestion des Versions

### Types de conflits en edition collaborative

| Type de conflit | Description | Prevention | Resolution |
|---|---|---|---|
| **Conflit de contenu** | Deux auteurs modifient le meme paragraphe | Repartir les sections entre auteurs | Comparer les versions, choisir la meilleure |
| **Conflit de style** | Un auteur change le formatage global | Verrouiller les styles dans le template | Restaurer les styles du template |
| **Conflit de structure** | Un auteur reorganise les sections | Definir la structure avant la redaction | Revenir a la structure convenue |
| **Conflit de version** | Deux auteurs travaillent sur des copies differentes | Utiliser un systeme de co-edition en temps reel | Combiner les versions (Word Combine) |
| **Conflit semantique** | Deux sections contiennent des informations contradictoires | Assigner un seul auteur par sujet | Revue editoriale par un coordinateur |

### Strategies de prevention des conflits

#### Repartition par sections
- Assigner chaque section a un auteur unique et responsable.
- L'auteur de la section a l'autorite editoriale sur son contenu.
- Les autres contributeurs utilisent le mode Suggestion pour proposer des modifications.
- Un coordinateur editorial assure la coherence entre les sections.

#### Convention de verrouillage temporaire
Dans les environnements ou la co-edition en temps reel n'est pas disponible :
1. L'auteur qui souhaite editer une section place un commentaire "EN COURS D'EDITION — [Nom] — [Date/Heure]" au debut de la section.
2. Les autres auteurs s'abstiennent d'editer cette section pendant la periode d'edition.
3. Une fois termine, l'auteur supprime le commentaire et notifie les autres.
4. Cette convention repose sur la discipline des auteurs et n'est pas techniquement contraignante.

#### Utilisation du check-out/check-in SharePoint
SharePoint offre un mecanisme de check-out/check-in qui verrouille un document pendant qu'un utilisateur l'edite :
1. **Check-out** : l'utilisateur "extrait" le document, ce qui empeche les autres de le modifier.
2. **Edition** : l'utilisateur edite le document hors ligne ou en ligne.
3. **Check-in** : l'utilisateur "archive" le document, ce qui libere le verrouillage et cree une nouvelle version.
4. **Commentaire de version** : lors du check-in, l'utilisateur peut ajouter un commentaire decrivant les modifications apportees.

Ce mecanisme est adapte aux workflows sequentiels (un seul editeur a la fois) et aux documents sensibles necessitant un controle strict.

### Gestion des versions

#### Strategie de versionage

| Type de version | Convention | Usage | Exemple |
|---|---|---|---|
| **Brouillon** | v0.x | Redaction en cours, iterations internes | v0.1, v0.2, v0.9 |
| **Version majeure** | vX.0 | Version publiee, approuvee, diffusee | v1.0, v2.0 |
| **Version mineure** | vX.Y | Corrections, mises a jour legeres | v1.1, v1.2 |
| **Revision** | vX.Y.Z | Corrections mineures sans impact fonctionnel | v1.0.1 |

#### Historique des modifications

Inclure un tableau d'historique des modifications en debut de document :

| Version | Date | Auteur | Description des modifications |
|---|---|---|---|
| v0.1 | 2026-01-10 | J. Dupont | Creation du brouillon initial |
| v0.5 | 2026-01-20 | J. Dupont | Integration des retours de l'equipe |
| v0.9 | 2026-01-28 | J. Dupont | Version candidate pour approbation |
| v1.0 | 2026-02-05 | M. Martin (approbateur) | Version approuvee et publiee |
| v1.1 | 2026-02-12 | J. Dupont | Correction de coquilles et mise a jour des chiffres |

---

## Directives de Redaction Collaborative

### Roles dans la redaction collaborative

| Role | Responsabilites | Droits | Nombre typique |
|---|---|---|---|
| **Coordinateur editorial** | Definir la structure, assurer la coherence, gerer le calendrier | Edition, approbation, partage | 1 |
| **Auteur de section** | Rediger le contenu de sa section, integrer les suggestions | Edition de sa section | 1 par section |
| **Relecteur technique** | Verifier l'exactitude technique du contenu | Commentaires, suggestions | 1-3 |
| **Relecteur editorial** | Verifier le style, la grammaire, la coherence | Commentaires, suggestions | 1-2 |
| **Approbateur** | Valider formellement le document | Lecture, approbation | 1-3 |

### Protocole de redaction collaborative

1. **Kick-off editorial** : reunion de lancement ou le coordinateur presente la structure du document, assigne les sections, definit le calendrier et les conventions.
2. **Redaction parallele** : chaque auteur redige sa section dans le document partage, en respectant la structure convenue et les styles du template.
3. **Checkpoint intermediaire** : le coordinateur organise une revue intermediaire pour verifier la coherence entre les sections, identifier les redondances et les lacunes.
4. **Revue croisee** : chaque auteur relit les sections des autres auteurs en mode Suggestion et ajoute des commentaires constructifs.
5. **Integration** : chaque auteur integre les suggestions et commentaires sur sa section, en repondant a chaque commentaire.
6. **Revision editoriale** : le relecteur editorial fait un passage complet pour harmoniser le style, la terminologie et le ton.
7. **Revision technique** : le relecteur technique verifie l'exactitude des informations, des chiffres et des references.
8. **Finalisation** : le coordinateur assemble la version finale, genere la table des matieres, verifie les references croisees et soumet pour approbation.

### Conventions de commentaires

Pour garantir des commentaires utiles et actionnables :

| Type de commentaire | Prefixe | Exemple |
|---|---|---|
| **Question** | [QUESTION] | [QUESTION] Ce chiffre est-il a jour ? Source ? |
| **Suggestion** | [SUGGESTION] | [SUGGESTION] Reformuler pour plus de clarte |
| **Correction** | [CORRECTION] | [CORRECTION] Erreur factuelle — le reglement date de 2024, pas 2023 |
| **Action requise** | [ACTION] | [ACTION] @Jean Ajouter le graphique des ventes Q4 |
| **Information** | [INFO] | [INFO] La direction a valide cette orientation le 15/01 |
| **A discuter** | [DISCUSSION] | [DISCUSSION] Deux options possibles ici, a trancher en reunion |

---

## Outils Complementaires pour la Collaboration Documentaire

### Outils de co-edition et collaboration

| Outil | Type | Points forts | Limites |
|---|---|---|---|
| **Google Docs** | Cloud natif | Co-edition temps reel, simplicite | Mise en forme limitee |
| **Microsoft Word Online** | Cloud | Integration M365, co-edition | Fonctionnalites reduites vs. desktop |
| **Microsoft Word Desktop** | Desktop + cloud | Fonctionnalites completes | Co-edition moins fluide que web |
| **Notion** | Cloud | Organisation, bases de donnees, wikis | Pas concu pour les documents longs |
| **Dropbox Paper** | Cloud | Simplicite, integration Dropbox | Fonctionnalites limitees |
| **Quip** | Cloud (Salesforce) | Integration Salesforce, feuilles de calcul | Ecosysteme Salesforce requis |
| **Overleaf** | Cloud (LaTeX) | Co-edition LaTeX, historique | Courbe d'apprentissage LaTeX |

### Outils de revue et approbation

| Outil | Type | Points forts | Usage typique |
|---|---|---|---|
| **SharePoint Workflows** | M365 natif | Integration M365, gratuit | Entreprises Microsoft |
| **Power Automate** | M365 natif | Workflows complexes, conditions | Approbations conditionnelles |
| **Adobe Acrobat** | Desktop + cloud | Revue PDF, annotations avancees | Documents finalises PDF |
| **Filestage** | SaaS | Revue visuelle, multi-format | Agences, equipes creatives |
| **ProofHub** | SaaS | Gestion de projet + revue | Equipes projet |

### Outils de gestion de versions documentaires

| Outil | Type | Points forts | Usage typique |
|---|---|---|---|
| **SharePoint** | M365 | Versionnage automatique, check-in/out | Entreprises Microsoft |
| **Google Drive** | Cloud | Historique illimite (Workspace) | Entreprises Google |
| **Git (pour Markdown/LaTeX)** | Open source | Diff precis, branches, merge | Documentation technique |
| **M-Files** | DMS | Classification automatique, metadata | Gestion documentaire structuree |
| **DocuWare** | DMS | Archivage, workflows | Archivage et conformite |

---

## Collaboration sur Documents Techniques (Markdown et LaTeX)

### Collaboration sur Markdown avec Git

Pour les documents techniques (documentation logicielle, wikis, specifications), la collaboration sur Markdown via Git offre des avantages uniques :

- **Diff precis** : Git identifie exactement les lignes modifiees, ajoutees ou supprimees, avec un diff lisible.
- **Branches** : chaque contributeur peut travailler sur une branche dediee sans affecter la branche principale.
- **Pull Requests / Merge Requests** : les modifications sont soumises via des pull requests qui permettent la revue de code (ici, revue de contenu) avant l'integration.
- **Conflits explicites** : quand deux contributeurs modifient la meme ligne, Git signale un conflit qui doit etre resolu explicitement.
- **CI/CD documentaire** : des pipelines automatises peuvent generer le document final (HTML, PDF) a chaque merge sur la branche principale.

#### Workflow Git pour la documentation

```
1. Auteur cree une branche : feature/section-3-analyse
2. Auteur redige le contenu en Markdown
3. Auteur commit et pousse la branche
4. Auteur ouvre une Pull Request vers la branche principale
5. Relecteurs commentent la Pull Request (revue en ligne)
6. Auteur integre les retours (nouveaux commits)
7. Approbation par les relecteurs
8. Merge dans la branche principale
9. Pipeline CI/CD genere automatiquement le document final
```

### Collaboration sur LaTeX avec Overleaf

Overleaf est la plateforme de reference pour la collaboration en temps reel sur des documents LaTeX :

- **Co-edition temps reel** : comme Google Docs, mais pour LaTeX. Plusieurs auteurs peuvent editer simultanement avec des curseurs de couleur.
- **Compilation en temps reel** : le document PDF est recompile automatiquement a chaque modification, avec un apercu en temps reel.
- **Historique des versions** : chaque modification est enregistree. On peut nommer des versions (labels) et restaurer des versions anterieures.
- **Track Changes** : Overleaf offre un mode Track Changes (editions premium) qui fonctionne comme Word Track Changes mais pour LaTeX.
- **Commentaires** : commentaires ancres au texte, avec mentions et fils de discussion.
- **Integration Git** : possibilite de synchroniser un projet Overleaf avec un depot Git (GitHub, GitLab) pour combiner la collaboration Overleaf avec le workflow Git.

---

## Securite et Conformite en Collaboration Documentaire

### Risques de securite specifiques a la collaboration

| Risque | Description | Mitigation |
|---|---|---|
| **Partage excessif** | Document partage avec des personnes non autorisees | Audit regulier des partages, expiration automatique |
| **Fuite de donnees** | Contenu copie vers des outils non securises | DLP (Data Loss Prevention), restrictions de copie/telechargement |
| **Version non controlee** | Document telecharge, modifie localement, redistribue | Privilegier l'edition en ligne, sensibiliser les utilisateurs |
| **Commentaires sensibles** | Informations confidentielles dans les commentaires | Supprimer les commentaires avant distribution externe |
| **Metadonnees exposees** | Auteur, modifications, proprietes visibles dans le fichier | Inspecter le document avant envoi (Word : Verifier le document) |
| **Acces residuel** | Anciens collaborateurs conservent l'acces | Revue periodique des permissions, revocation automatique au depart |

### Checklist de securite avant distribution externe

| Verification | Action | Outil |
|---|---|---|
| Supprimer les commentaires et marques de revision | Revision > Supprimer tous les commentaires ; Accepter toutes les modifications | Word |
| Inspecter le document | Fichier > Verifier la presence de problemes > Inspecter le document | Word |
| Supprimer les donnees personnelles | Inspecter > Supprimer les proprietes du document et informations personnelles | Word |
| Verifier les liens hypertexte | S'assurer qu'aucun lien ne pointe vers des ressources internes | Manuel |
| Convertir en PDF | Exporter en PDF pour figer le contenu | Word / Google Docs |
| Verifier le partage | Confirmer que seuls les destinataires prevus ont acces | Drive / SharePoint |
| Proteger le PDF | Ajouter un mot de passe ou des restrictions si necessaire | Acrobat / outil PDF |
