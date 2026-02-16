# Plateformes de Messagerie — Teams, Slack, Configuration Avancee & Gouvernance

## Overview

Ce document de reference couvre en profondeur les deux plateformes dominantes de messagerie et collaboration en entreprise : Microsoft Teams et Slack. Il detaille l'architecture, la configuration avancee, les patterns d'usage, la gouvernance, la securite, et les fonctionnalites 2025-2026 de chaque plateforme. Utiliser ce guide pour concevoir, deployer et administrer un workspace de messagerie professionnel, performant et gouverne, que ce soit pour une PME de 50 personnes ou une multinationale de 50 000 collaborateurs. Les recommandations s'appliquent aux versions actuelles : Microsoft Teams (New Teams, Microsoft 365), Slack (Pro, Business+, Enterprise Grid).

---

## PARTIE 1 — Microsoft Teams

### Architecture Fondamentale

Microsoft Teams s'articule autour d'une hierarchie a trois niveaux qu'il faut imperativement comprendre avant toute configuration :

#### Niveau 1 — L'Organisation (Tenant)
Le tenant Microsoft 365 est le conteneur racine. Il definit le perimetre de securite, les politiques d'acces, et les configurations globales. Un tenant = une organisation. Les politiques de Teams (messagerie, reunions, appels, applications) se configurent au niveau du tenant dans le Teams Admin Center. Chaque decision prise a ce niveau impacte tous les utilisateurs.

#### Niveau 2 — Les Teams (Equipes)
Une Team est un espace de collaboration dedie a un groupe de personnes. Chaque Team possede un site SharePoint associe (stockage de fichiers), une boite aux lettres de groupe Exchange (email de groupe), et un plan Planner (gestion de taches). Les Teams peuvent etre de type :
- **Privee** : acces sur invitation ou approbation du proprietaire. Recommande pour les equipes operationnelles et les projets confidentiels.
- **Publique** : tout membre de l'organisation peut rejoindre. Recommande pour les communautes thematiques et les channels d'information.
- **Org-wide** : tous les membres de l'organisation sont automatiquement membres (limite a 10 000 personnes). Recommande pour les annonces globales.

#### Niveau 3 — Les Channels (Canaux)
Les channels sont les espaces de conversation au sein d'une Team. Trois types de channels existent :
- **Standard** : accessible a tous les membres de la Team. Les messages et fichiers sont visibles par tous.
- **Prive** : accessible uniquement aux membres invites du channel. Possede son propre site SharePoint. Utiliser pour les sujets sensibles au sein d'une Team plus large.
- **Partage (Shared)** : accessible a des personnes d'autres Teams ou meme d'autres organisations. Ideal pour la collaboration transverse sans multiplier les Teams.

#### Tabs, Apps et Connecteurs
Chaque channel peut etre enrichi avec des tabs (onglets) qui integrent d'autres applications directement dans Teams :
- **Tabs natifs** : Files (SharePoint), Wiki/Loop, Planner, OneNote, Power BI, Lists.
- **Apps tierces** : Jira, Trello, Miro, Figma, Salesforce, ServiceNow — integrees via le Teams App Store.
- **Connecteurs** : flux RSS, webhooks entrants, notifications GitHub, Jenkins, Azure DevOps — pour automatiser les flux d'information.
- **Bots** : assistants conversationnels qui repondent aux questions, executent des commandes ou automatisent des taches dans les channels.

### Configuration Avancee de Teams

#### Breakout Rooms
Les breakout rooms permettent de diviser une reunion Teams en sous-groupes pour des discussions paralleles :
- Configuration possible avant la reunion (pre-assignment) ou pendant (creation dynamique).
- Le presentateur peut assigner les participants manuellement ou automatiquement (aleatoire).
- Limite : jusqu'a 50 salles, 300 participants au total.
- Les participants peuvent appeler l'organisateur pour revenir dans la salle principale.
- Les enregistrements et transcriptions ne fonctionnent que dans la salle principale — documenter les discussions de sous-groupe via un note-taker designe dans chaque salle.

#### Town Halls (anciennement Live Events)
Les Town Halls remplacent les Live Events depuis 2024 et sont concus pour les communications a grande echelle :
- Capacite jusqu'a 10 000 participants (20 000 avec les licences Premium).
- Mode presentateur/audience : les presentateurs partagent du contenu, l'audience regarde et interagit via le Q&A.
- Q&A structure : les questions de l'audience sont moderees avant publication. Les organisateurs peuvent repondre en texte ou en live.
- Enregistrement automatique et disponible apres l'evenement.
- Integration PowerPoint Live pour des presentations interactives.
- Rapports de participation et d'engagement post-evenement.
- Recommandation : utiliser les Town Halls pour les all-hands, les annonces strategiques, et les evenements internes de plus de 100 participants.

#### Loop Components
Microsoft Loop introduit des composants collaboratifs portables qui fonctionnent a travers les applications Microsoft 365 :
- **Loop components dans Teams** : tableaux, listes de taches, paragraphes, Q&A qui peuvent etre inseres dans un message Teams et edites en temps reel par tous les participants.
- **Synchronisation cross-app** : un composant Loop cree dans Teams est editable dans Outlook, Word, et l'application Loop dediee. Les modifications sont synchronisees en temps reel.
- **Cas d'usage** : agenda de reunion collaboratif, liste d'actions post-reunion, brainstorming rapide, tableau de suivi — directement dans le flux de conversation, pas dans un document separe.
- **Gouvernance** : les composants Loop sont stockes dans le OneDrive de leur createur. Configurer les politiques de partage et de retention en consequence dans le SharePoint Admin Center.

#### Copilot dans Teams (2025-2026)
Microsoft Copilot apporte l'IA generative directement dans Teams :
- **Resume de reunion** : Copilot genere un resume structure de la reunion avec les decisions prises, les actions assignees, et les points de desaccord identifies.
- **Rattrapage intelligent** : en arrivant en retard a une reunion, demander a Copilot "What have I missed?" pour obtenir un resume en temps reel.
- **Resume de chat** : demander a Copilot de resumer les 7 derniers jours de conversation d'un channel pour rattraper le contexte.
- **Composition assistee** : Copilot aide a rediger des messages en ajustant le ton, la longueur et le format.
- **Q&A sur les fichiers** : interroger Copilot sur le contenu des fichiers partages dans le channel sans les ouvrir.
- **Prerequis** : licence Microsoft 365 Copilot (add-on payant). Verifier les politiques de confidentialite des donnees avant activation.

### Gouvernance de Teams

#### Politique de creation de Teams
Sans gouvernance, les organisations finissent avec des centaines de Teams redondantes et abandonnees. Definir une politique claire :
- **Qui peut creer une Team** : restreindre la creation aux managers ou a un groupe dedie (via Azure AD group policy). Mettre en place un processus de demande pour les autres.
- **Formulaire de creation** : nom (selon la convention), objectif, proprietaire(s), duree de vie prevue, membres initiaux.
- **Convention de nommage** : imposer un format standardise. Exemples :
  - Equipes permanentes : `[Departement] - [Equipe]` → "Engineering - Backend", "Marketing - Content"
  - Projets : `[PRJ] [Nom du projet] [Annee]` → "PRJ Migration CRM 2025"
  - Communautes : `[COM] [Theme]` → "COM Data Community"
- **Validation** : un administrateur valide la creation pour eviter les doublons et verifier la conformite a la convention.

#### Cycle de vie des Teams
- **Creation** : validation, nommage, configuration initiale (channels, tabs, permissions).
- **Utilisation active** : monitoring de l'activite, ajout/retrait de membres, ajout de channels.
- **Inactivite** : alerte automatique apres 90 jours sans activite (configurable via Azure AD lifecycle policies).
- **Archivage** : figer la Team (lecture seule, contenu preserved mais plus de nouvelles contributions). Utiliser pour les projets termines.
- **Suppression** : 30 jours apres archivage sans opposition, suppression definitive (avec recovery possible pendant 30 jours supplementaires via soft delete).

#### Politique de channels
- **Channel General** : ne PAS l'utiliser comme poubelle. Le renommer en "Annonces" et le reserver aux communications officielles de l'equipe.
- **Channels standard** : creer des channels thematiques clairs. Exemples pour une equipe produit : "Design", "Engineering", "Sprint-Planning", "Releases", "Random".
- **Channels prives** : utiliser avec parcimonie. Chaque channel prive cree un site SharePoint separe et complique la gouvernance. Recommandation : max 2-3 channels prives par Team.
- **Channels partages** : privilegier les shared channels pour la collaboration transverse plutot que d'inviter des externes dans toute la Team.

---

## PARTIE 2 — Slack

### Architecture d'un Workspace Slack

#### Workspace et Organisation
- **Workspace** : l'espace Slack d'une entreprise. Contient les channels, les utilisateurs, et les configurations.
- **Enterprise Grid** : pour les grandes organisations, Enterprise Grid permet de gerer plusieurs workspaces sous une organisation unifiee avec SSO, gouvernance centralisee, et channels partages entre workspaces.
- **Slack Connect** : permet d'inviter des personnes externes (clients, fournisseurs, partenaires) dans des channels dedies sans leur donner acces au reste du workspace.

#### Channels
Les channels sont le coeur de Slack. Chaque channel est un flux de conversation dedie a un sujet :
- **Public** : tout membre du workspace peut le trouver et le rejoindre. Recommande par defaut pour maximiser la transparence.
- **Prive** : seuls les membres invites y ont acces. Utiliser uniquement pour les sujets reellement confidentiels (RH, legal, finance sensible).
- **Recommandation de ratio** : viser 70% de channels publics, 30% de channels prives. Un workspace avec une majorite de channels prives est un signal d'alerte sur la culture de transparence.

#### Sections (Sidebar Organization)
Depuis 2024, Slack permet d'organiser les channels dans la sidebar en sections personnalisees :
- Creer des sections thematiques : "Mon equipe", "Projets actifs", "Veille", "Social".
- Reorganiser les channels par priorite plutot que par ordre alphabetique.
- Recommander aux utilisateurs de configurer 4-6 sections maximum pour garder la sidebar lisible.
- Les sections sont personnelles — chaque utilisateur a sa propre organisation.

#### Workflows et Automatisations
Slack Workflow Builder permet de creer des automatisations sans code directement dans Slack :
- **Formulaires** : creer des formulaires de demande (conge, support IT, idee) qui postent les resultats dans un channel.
- **Messages programmes** : envoyer des messages automatiques a des moments cles (rappel de standup, welcome message pour les nouveaux membres).
- **Reactions comme triggers** : declencher une action quand quelqu'un ajoute un emoji specifique (ex : ajouter un :ticket: cree un ticket dans Jira).
- **Integration avec des services externes** : Google Sheets, Salesforce, Jira, GitHub — les workflows peuvent lire et ecrire dans ces systemes.
- **Workflow Builder nouvelle generation (2025)** : interface drag-and-drop plus puissante, conditions if/then, variables, integrations natives avec plus de 100 services.

#### Canvas
Slack Canvas est un document collaboratif integre directement dans Slack :
- Chaque channel peut avoir un Canvas associe qui sert de documentation de reference.
- Permet de centraliser les informations persistantes (objectifs du channel, liens utiles, processus, FAQ) sans qu'elles soient noyees dans le flux de messages.
- Les Canvas supportent le texte formate, les listes, les tableaux, les images, les videos embeddees, et les liens vers des messages Slack.
- Recommandation : utiliser un Canvas dans chaque channel de projet pour documenter l'objectif, le scope, les membres, les liens cles, et les decisions.

### Configuration Avancee de Slack

#### Slack Huddles
Les Huddles sont des appels audio/video legers directement dans Slack, sans planification formelle :
- Un clic pour demarrer un Huddle dans un channel ou un DM.
- Les autres membres du channel voient une notification et peuvent rejoindre quand ils veulent.
- Partage d'ecran, threads de discussion lies au Huddle, reactions emoji en temps reel.
- Ideal pour les discussions spontanees de 5-15 minutes qui remplacent le "tu as 2 minutes ?" au bureau.
- Recommandation : encourager les Huddles comme alternative aux reunions planifiees pour les questions rapides. Fixer une norme : si la discussion depasse 15 minutes, planifier une vraie reunion.

#### Slack Connect
Slack Connect permet la collaboration avec des organisations externes :
- Inviter des utilisateurs externes dans des channels dedies (pas d'acces au reste du workspace).
- Ideal pour la collaboration agence/client, fournisseur/acheteur, partenaire/partenaire.
- Configuration : l'administrateur du workspace doit approuver les connexions externes.
- Securite : definir quels types de fichiers peuvent etre partages, si le screen sharing est autorise en Huddle, et quelles integrations sont accessibles.
- Convention de nommage : prefixer les channels externes avec `#ext-` pour les identifier immediatement (`#ext-agency-creative`, `#ext-partner-api`).
- Gouvernance : auditer les channels Slack Connect trimestriellement. Fermer les channels avec des partenaires dont la collaboration est terminee.

#### Slack AI (2025-2026)
Slack AI apporte des capacites d'intelligence artificielle natives :
- **Resume de channels** : demander a Slack AI de resumer les conversations des derniers jours dans un channel. Ideal pour rattraper le contexte apres un conge ou sur un channel peu suivi.
- **Resume de threads** : resumer les longs threads de discussion en quelques points cles.
- **Recherche intelligente** : poser des questions en langage naturel sur l'historique des conversations. Slack AI cherche dans les messages, fichiers et Canvas pour fournir des reponses contextuelles.
- **Suggestions de reponse** : Slack AI peut suggerer des reponses aux messages bases sur le contexte de la conversation.
- **Disponibilite** : Slack AI est disponible sur les plans Business+ et Enterprise Grid. Il respecte les permissions existantes — il ne peut pas acceder aux channels prives dont l'utilisateur n'est pas membre.

---

## PARTIE 3 — Comparaison Teams vs Slack

### Matrice de Comparaison

| Critere | Microsoft Teams | Slack |
|---|---|---|
| **Ecosysteme** | Microsoft 365 (Office, SharePoint, OneDrive, Power Platform) | Standalone, integrations API avec tout |
| **Force principale** | Integration bureautique et reunions | Experience de chat et extensibilite |
| **Reunions** | Native, tres complete (breakout rooms, Town Halls, Copilot) | Huddles legers, Zoom/Meet pour les grandes reunions |
| **Fichiers** | SharePoint integre (co-editing natif Office) | Integration externe (Google Drive, Dropbox, Box) |
| **Recherche** | Basique (ameliore avec Copilot) | Excellente nativamente, encore meilleure avec Slack AI |
| **Customisation** | Limitee (Power Platform pour l'avance) | Tres elevee (API riche, App Directory, Workflow Builder) |
| **UX/Rapidite** | Plus lourd, meilleur sur desktop | Plus rapide, meilleur pour les power users |
| **Administration** | Teams Admin Center + Azure AD (puissant mais complexe) | Workspace settings (plus simple, moins de profondeur) |
| **Securite** | Microsoft Purview, DLP, retention avancee, eDiscovery | Enterprise Key Management, DLP, audit logs |
| **Prix** | Inclus dans Microsoft 365 (valeur percue elevee) | Payant separement (Pro, Business+, Enterprise Grid) |
| **Ideal pour** | Organisations deja Microsoft-centric, grands groupes | Organisations tech-native, culture dev, startups/scaleups |

### Recommandations de Choix

```
L'organisation est-elle deja sur Microsoft 365 ?
├── OUI → L'organisation est-elle satisfaite de Teams ?
│   ├── OUI → Rester sur Teams, investir dans la configuration avancee
│   └── NON → Le budget permet-il d'ajouter Slack ?
│       ├── OUI → Deployer Slack pour le chat, garder Teams pour les reunions
│       └── NON → Optimiser Teams (formation, gouvernance, bots)
├── NON → L'organisation est-elle sur Google Workspace ?
│   ├── OUI → Slack + Google Meet est la combinaison naturelle
│   └── NON → Evaluer les besoins
│       ├── Organisation tech/startup → Slack
│       ├── Organisation corporate classique → Teams (avec Microsoft 365)
│       └── Organisation mixte → Tester les deux et decider en 3 mois
```

---

## PARTIE 4 — Conventions de Nommage

### Schema General de Nommage

Le nommage des channels est un acte de design organisationnel. Un mauvais nommage rend l'information introuvable. Un bon nommage rend le workspace auto-documentant.

#### Principes
1. **Prefixe obligatoire** : chaque channel commence par un prefixe qui indique sa categorie (`team-`, `project-`, `help-`, etc.).
2. **Kebab-case** : tout en minuscules, mots separes par des tirets. Pas d'espaces, pas de camelCase, pas d'underscores.
3. **Lisibilite** : le nom doit etre comprehensible sans explication supplementaire.
4. **Consistance** : appliquer les memes conventions dans tout le workspace, sans exception.
5. **Langue** : choisir une langue unique pour les noms de channels (anglais recommande pour les organisations internationales).

#### Catalogue de Prefixes Recommandes

| Prefixe | Description | Exemples |
|---|---|---|
| `announce-` | Communications officielles, lecture seule pour la plupart | `announce-all`, `announce-engineering`, `announce-rh` |
| `team-` | Espace quotidien d'une equipe permanente | `team-backend`, `team-design`, `team-sales-emea` |
| `project-` | Channel temporaire lie a un projet | `project-redesign-website`, `project-migration-aws` |
| `topic-` | Discussion transverse sur un sujet specifique | `topic-accessibility`, `topic-ai-ethics`, `topic-security` |
| `help-` | Questions et support | `help-it`, `help-rh`, `help-legal`, `help-data` |
| `social-` | Discussions informelles et cohesion | `social-random`, `social-music`, `social-running` |
| `ext-` | Channels avec des partenaires externes | `ext-agency-brand`, `ext-client-acme` |
| `feed-` ou `bot-` | Notifications automatisees | `feed-github-deploys`, `bot-monitoring-alerts` |
| `ask-` | Questions ouvertes a la communaute | `ask-product`, `ask-engineering` |
| `wg-` | Working groups (groupes de travail temporaires) | `wg-remote-policy`, `wg-comp-review` |

### Nommage dans Teams

Dans Microsoft Teams, le nommage s'applique a deux niveaux :
- **Noms de Teams** : format `[Categorie] - [Nom]`. Exemples : "Engineering - Platform", "PRJ - Migration CRM 2025", "COM - Data Community".
- **Noms de Channels** : format descriptif sans prefixe (le contexte est donne par la Team). Exemples dans la Team "Engineering - Platform" : "General" (renomme en "Annonces"), "Architecture", "Code Reviews", "Incidents", "Random".

---

## PARTIE 5 — Gouvernance du Workspace

### Roles et Responsabilites

| Role | Responsabilites | Profil |
|---|---|---|
| **Workspace Owner** | Configuration globale, securite, facturation, politiques | IT Director / CTO |
| **Workspace Admin** | Gestion des membres, apps, integrations, compliance | IT Admin |
| **Channel Owner** | Creation, configuration, moderation du channel | Manager ou lead de projet |
| **Collaboration Champion** | Promotion des bonnes pratiques, formation, support de niveau 1 | Super-user volontaire (1 par equipe) |
| **User** | Utilisation quotidienne dans le respect des conventions | Tous les collaborateurs |

### Politique d'Archivage

L'archivage est la cle d'un workspace propre et navigable :
- **Channels de projet** : archiver dans les 7 jours suivant la cloture du projet. Le channel reste lisible mais pas editable.
- **Channels inactifs** : envoyer un avertissement automatique apres 60 jours d'inactivite. Archiver automatiquement apres 90 jours sans reponse.
- **Channels temporaires** : creer avec une date d'expiration des le depart (events, hackathons, campagnes).
- **Audit trimestriel** : l'administrateur passe en revue tous les channels et identifie ceux a archiver, renommer, ou consolider.
- **Recommandation** : viser un ratio de 80% de channels actifs (au moins 1 message par semaine) sur le nombre total de channels visibles.

### Politique d'Integrations et d'Applications

- **Approbation centralisee** : ne pas laisser chaque utilisateur installer n'importe quelle application. Definir un catalogue d'applications approuvees et un processus de demande pour les nouvelles.
- **Audit regulier** : revoir les integrations installees chaque trimestre. Desactiver celles qui ne sont plus utilisees ou dont le fournisseur ne repond plus aux criteres de securite.
- **Limite par channel** : eviter la surcharge de bots et connecteurs dans un meme channel. Un channel avec 5 bots qui postent est un channel que personne ne lit.
- **Integrations recommandees** : calendrier (Google Calendar, Outlook), gestion de projet (Jira, Asana, Linear), CI/CD (GitHub, GitLab), monitoring (PagerDuty, Datadog), standup async (Geekbot, Standuply).

---

## PARTIE 6 — Gestion des Notifications

### Le Probleme de la Notification Fatigue

La surnotification est l'ennemi de la productivite dans les outils de messagerie. Un collaborateur moyen recoit 50-100 notifications par jour sur Slack ou Teams, creant des interruptions constantes qui fragmentent l'attention et empechent le travail profond.

### Configuration Recommandee pour les Utilisateurs

| Parametre | Recommandation | Justification |
|---|---|---|
| **Notifications par defaut** | Mentions directes et mots-cles uniquement | Reduire le bruit aux messages qui vous concernent vraiment |
| **Do Not Disturb** | Activer entre 19h et 8h (ajuster selon les preferences) | Proteger le temps personnel |
| **Notifications de threads** | Uniquement les threads auxquels vous participez | Eviter de suivre tous les threads d'un channel |
| **Channels bruyants** | Muter les channels a forte activite, consulter en batch | Reduire les interruptions |
| **Son de notification** | Desactiver sur desktop, garder sur mobile pour les urgences | Reduire la stimulation constante |
| **Badges** | Desactiver le compteur de messages non lus pour les channels mutees | Reduire l'anxiete de la boite de reception |

### Recommandations pour les Emetteurs

- **`@channel`** : utiliser uniquement pour les annonces qui concernent TOUS les membres du channel ET qui necessitent une action. Maximum 1-2 fois par semaine par channel.
- **`@here`** : utiliser pour atteindre les personnes actuellement en ligne. Moins intrusif que `@channel` car n'envoie pas de notification push aux personnes en DND.
- **`@mention` individuelle** : preferer les mentions individuelles quand le message concerne une personne specifique.
- **Horaires d'envoi** : eviter d'envoyer des messages non urgents en dehors des heures de travail. Utiliser la fonctionnalite "schedule message" pour programmer l'envoi au debut de la journee de travail du destinataire.
- **Threads** : TOUJOURS repondre dans les threads, jamais dans le corps principal du channel. Cela reduit les notifications pour les personnes non concernees par la discussion.

---

## PARTIE 7 — Recherche et Organisation de l'Information

### Optimisation de la Recherche dans Slack

La recherche est l'une des forces majeures de Slack. Maitriser les operateurs de recherche avances :

| Operateur | Usage | Exemple |
|---|---|---|
| `in:#channel` | Chercher dans un channel specifique | `in:#team-product roadmap` |
| `from:@user` | Chercher les messages d'un utilisateur | `from:@marie budget Q3` |
| `before:` / `after:` | Filtrer par date | `after:2025-01-01 migration` |
| `has:link` | Messages contenant un lien | `has:link in:#team-backend` |
| `has:reaction:emoji` | Messages avec une reaction specifique | `has:reaction:white_check_mark` |
| `is:thread` | Messages dans des threads | `is:thread decision` |
| `to:me` | Messages qui vous mentionnent | `to:me review` |

### Optimisation de la Recherche dans Teams

La recherche Teams est moins puissante nativement mais s'ameliore avec Copilot :
- Utiliser les filtres de recherche : personnes, messages, fichiers.
- Filtrer par equipe ou channel pour reduire le perimetre.
- Avec Copilot : poser des questions en langage naturel ("What did we decide about the pricing model last week?").
- Recommandation : pour les informations critiques, ne pas se reposer uniquement sur la recherche dans le chat. Documenter les decisions dans un Wiki, un OneNote ou un SharePoint.

---

## PARTIE 8 — Securite et Compliance

### Microsoft Teams — Securite

- **Microsoft Purview** : DLP (Data Loss Prevention) pour empecher le partage de donnees sensibles (numeros de carte bancaire, numeros de securite sociale) dans les messages et fichiers Teams.
- **Retention Policies** : configurer la retention des messages (duree de conservation, suppression automatique) selon les exigences reglementaires (RGPD, SOX, HIPAA).
- **eDiscovery** : recherche et export des messages Teams pour les enquetes legales et les audits.
- **Conditional Access** : restreindre l'acces a Teams selon le device (gere vs non gere), la localisation, et le niveau de risque (Azure AD Conditional Access).
- **Information Barriers** : empecher la communication entre certains groupes (ex : muraille de Chine entre les equipes M&A et les equipes Trading).
- **Guest Access** : configurer finement les permissions des invites externes (acces aux fichiers, creation de channels, participation aux reunions).

### Slack — Securite

- **Enterprise Key Management (EKM)** : les organisations Enterprise Grid peuvent utiliser leurs propres cles de chiffrement (AWS KMS) pour le chiffrement des messages et fichiers stockes par Slack.
- **DLP integre et tiers** : Slack propose des politiques DLP natives (Business+ et Enterprise Grid) et s'integre avec des solutions tierces (Nightfall, Polymer).
- **Audit Logs** : journaux d'audit detailles de toutes les actions administratives et utilisateur (connexions, creation de channels, partage de fichiers, installations d'apps).
- **Session Management** : forcer la deconnexion des sessions, imposer des durees de session maximales, et configurer le SSO obligatoire (SAML/SCIM).
- **Channel Management Policies** : restreindre qui peut creer des channels, inviter des membres, installer des applications.
- **Data Residency** : Slack propose le choix de la region de stockage des donnees (US, EU, AU, JP) pour repondre aux exigences de souverainete.

### Compliance Commune

Quel que soit l'outil, verifier les points suivants :
- **RGPD** : informer les collaborateurs sur le traitement de leurs donnees de messagerie. Configurer la retention appropriee. Gerer les demandes de droit d'acces et de suppression.
- **Droit a la deconnexion** : configurer les heures de Do Not Disturb par defaut et sensibiliser les managers au respect de ces horaires.
- **Archivage legal** : si l'organisation est soumise a des obligations d'archivage (secteur financier, sante), configurer la retention longue duree et l'archivage des messages dans un systeme tiers si necessaire.
- **Surveillance** : la surveillance des communications est strictement encadree par le RGPD et le droit du travail. Consulter le DPO et le service juridique avant toute mise en place d'outils de monitoring.

---

## PARTIE 9 — Bonnes Pratiques Transverses

### Onboarding sur la Plateforme

L'onboarding des nouveaux collaborateurs sur l'outil de messagerie est un moment critique :
1. **Guide de demarrage** : fournir un guide en 1 page couvrant la convention de nommage, les channels a rejoindre, les regles de base (threads, notifications, DND).
2. **Channels par defaut** : configurer les channels que chaque nouveau membre rejoint automatiquement (`announce-all`, `social-random`, `help-it`, + channels de son equipe).
3. **Buddy system** : assigner un "collaboration buddy" qui accompagne le nouveau pendant la premiere semaine sur l'usage de l'outil.
4. **Channel dedie** : creer un channel `#onboarding` ou les nouveaux posent leurs questions sans crainte.
5. **Message de bienvenue automatise** : configurer un workflow qui envoie un message de bienvenue personnalise avec les liens utiles et les conventions.

### Hygiene du Workspace

- **Statut personnalise** : encourager les collaborateurs a mettre a jour leur statut (en reunion, en focus, en conge, en deplacement) pour que les collegues sachent quand et comment les joindre.
- **Profil complet** : nom, photo, titre, fuseau horaire, equipe, et pronoms. Un profil complet facilite la collaboration avec des personnes qu'on n'a jamais rencontrees physiquement.
- **Pinned messages** : epingler les messages importants dans chaque channel (objectif du channel, liens utiles, decisions cles). Revoir les messages epingles regulierement pour supprimer les obsoletes.
- **Reactions emoji comme signal** : definir des conventions de reactions (`eyes` = j'ai vu, `white_check_mark` = c'est fait, `thumbsup` = d'accord, `hourglass` = en cours) pour reduire les messages de reponse.
- **Nettoyage regulier** : quitter les channels qu'on ne suit plus, muter ceux qu'on consulte rarement, reorganiser sa sidebar.

### Migration entre Plateformes

Si l'organisation envisage une migration de Teams vers Slack (ou inversement) :
1. **Audit de l'existant** : cartographier tous les channels, integrations, bots, workflows, et fichiers dans la plateforme actuelle.
2. **Design de la cible** : ne pas reproduire l'architecture existante a l'identique. Profiter de la migration pour rationaliser et appliquer les bonnes pratiques.
3. **Migration des donnees** : evaluer le besoin de migrer l'historique des conversations. Souvent, repartir de zero est plus sain que de migrer des annees de messages. Archiver l'ancienne plateforme en lecture seule pendant 6 mois.
4. **Formation** : former les utilisateurs a la nouvelle plateforme AVANT la migration. Identifier des champions par equipe pour accompagner la transition.
5. **Periode de transition** : faire coexister les deux plateformes pendant 2-4 semaines maximum, puis couper l'ancienne pour eviter la fragmentation.
6. **Support renforce** : mettre en place un support dedie pendant les 4 premieres semaines post-migration (channel de support, permanences, FAQ).
