# Email Mastery -- Outlook Avance, Gmail Avance, Regles, Filtres, Templates & Automatisation

## Overview

Ce document de reference couvre la maitrise avancee de l'email professionnel : configuration experte d'Outlook et de Gmail, creation de regles et filtres automatiques, templates et snippets de reponse, gestion des signatures, delegation et boites partagees, strategies d'archivage, maitrise de la recherche, optimisation mobile, securite email (phishing, chiffrement), et analytics. L'email reste le canal de communication professionnel dominant avec plus de 350 milliards de messages envoyes par jour en 2025. Un professionnel moyen recoit 120 a 150 emails par jour et passe 2,5 heures quotidiennes a les traiter. La maitrise avancee de son client email n'est pas un luxe technique — c'est un levier de productivite fondamental qui peut liberer 30 a 60 minutes par jour.

---

## Outlook Avance (Microsoft 365)

### Regles de messagerie

Les regles Outlook permettent de router automatiquement les emails entrants et sortants selon des criteres precis. Elles s'executent cote serveur (Exchange Online) ou cote client, et s'appliquent dans l'ordre de priorite defini.

#### Regles essentielles a configurer

1. **Newsletters et abonnements** : Condition = expediteur contient "newsletter" OU "unsubscribe" dans le corps. Action = deplacer vers le dossier "Newsletters", marquer comme lu. Cette regle seule peut eliminer 20 a 40% du volume entrant.

2. **Notifications automatiques** : Condition = expediteur provient de systemes (JIRA, GitHub, Salesforce, SAP, Trello, etc.). Action = deplacer vers "Notifications", marquer comme lu. Consulter ce dossier 1 a 2 fois par jour.

3. **CC informatif** : Condition = je suis en CC (pas en destinataire direct). Action = deplacer vers "CC / FYI", marquer categorie "Informatif". Les emails en CC sont rarement urgents — les traiter en lot.

4. **Emails de mon manager** : Condition = expediteur = adresse du manager. Action = marquer avec la categorie "Prioritaire", jouer un son de notification specifique. Seule exception a la regle "pas de notification".

5. **Listes de distribution** : Condition = envoye a une liste de distribution specifique. Action = deplacer vers le dossier de la liste, ne pas notifier. Les listes de distribution generent un volume considerable d'emails non directement actionnables.

#### Bonnes pratiques pour les regles

- Limiter le nombre de regles a 15-20 maximum pour la maintenabilite
- Tester chaque regle avec "Executer maintenant" avant de l'activer
- Revoir les regles chaque trimestre : supprimer les obsoletes, ajuster les criteres
- Utiliser "Arreter le traitement des regles suivantes" pour les regles prioritaires
- Preferer les regles cote serveur (s'appliquent meme quand Outlook est ferme) aux regles cote client

### Quick Steps

Les Quick Steps sont des macros en un clic qui combinent plusieurs actions. Ils sont accessibles depuis la barre d'outils ou via des raccourcis clavier (Ctrl+Shift+1 a 9).

#### Quick Steps recommandes

| Quick Step | Actions combinees | Raccourci |
|---|---|---|
| **Deleguer** | Transferer a [personne], ajouter texte "Merci de traiter", marquer comme fait | Ctrl+Shift+1 |
| **Planifier** | Creer une tache a partir de l'email, deplacer vers @Action | Ctrl+Shift+2 |
| **Archiver + Repondre court** | Repondre avec template "Bien recu, merci", archiver | Ctrl+Shift+3 |
| **Reunion** | Creer une invitation a partir de l'email (sujet, participants pre-remplis) | Ctrl+Shift+4 |
| **Attente** | Deplacer vers @Attente, creer un rappel a J+3 | Ctrl+Shift+5 |

### Categories et codes couleur

Les categories Outlook permettent de taguer les emails avec des couleurs et des libelles. Contrairement aux dossiers, un email peut avoir plusieurs categories.

Systeme de categories recommande :

| Categorie | Couleur | Usage |
|---|---|---|
| @Action | Rouge | Email necessitant une action de ma part |
| @Attente | Orange | Email delegue ou en attente de reponse |
| @Reference | Bleu | Information a conserver pour reference |
| @Lire | Vert | Contenu a lire quand du temps est disponible |
| Prioritaire | Violet | Emails du manager, de la direction, ou urgents |
| Projet X | Jaune | Emails lies a un projet specifique |

### Search Folders (Dossiers de recherche)

Les Search Folders sont des vues dynamiques qui affichent les emails correspondant a des criteres sans les deplacer physiquement. Ils sont extremement utiles pour creer des vues transversales.

Search Folders recommandes :
- **Emails non lus de plus de 24h** : identifier les emails oublies
- **Emails avec pieces jointes > 5 Mo** : gerer le stockage
- **Emails envoyes sans reponse depuis 3 jours** : relances a effectuer
- **Emails marques pour suivi** : vue consolidee des suivis
- **Emails de mon equipe cette semaine** : vision d'equipe

### Focused Inbox

Focused Inbox utilise l'apprentissage automatique pour separer les emails en deux onglets :
- **Focused** : emails importants et actionnables (expediteurs frequents, reponses directes, mentions)
- **Other** : newsletters, notifications, CC, emails de masse

Pour optimiser Focused Inbox :
- Deplacer manuellement les emails mal classes (l'algorithme apprend)
- Verifier l'onglet "Other" 1 a 2 fois par jour (pas plus)
- Combiner avec les regles de messagerie pour un tri encore plus fin
- Desactiver Focused Inbox si vous preferez un controle total via les regles manuelles

### Scheduling et envoi differe

Outlook permet de planifier l'envoi des emails a un horaire precis. Utiliser cette fonctionnalite pour :
- Eviter d'envoyer des emails tard le soir ou le week-end (respecter les horaires de l'equipe)
- Programmer les emails non urgents pour le lendemain matin (meilleur taux de lecture)
- Envoyer les rappels et relances a des horaires strategiques (mardi/mercredi matin : meilleur taux d'ouverture)

Configuration : onglet Options > Differrer la livraison > Date et heure d'envoi. Possibilite de configurer une regle par defaut qui differe tous les emails de X minutes (filet de securite anti-erreur).

### Outlook Copilot (2025-2026)

Microsoft Copilot dans Outlook offre des capacites avancees :
- **Resume de fils de discussion** : synthese en 3 points des echanges longs
- **Brouillons assistes** : generation de reponses en fonction du contexte et du ton souhaite
- **Coaching de ton** : analyse du ton de l'email avant envoi (trop direct ? trop vague ?)
- **Categorisation intelligente** : suggestions de classement basees sur le contenu
- **Extraction d'actions** : identification automatique des action items dans un email

---

## Gmail Avance (Google Workspace)

### Filtres Gmail

Les filtres Gmail sont l'equivalent des regles Outlook. Ils s'appliquent aux emails entrants et peuvent etre appliques retroactivement aux emails existants.

#### Creation de filtres

Acces : Parametres (roue dentee) > Voir tous les parametres > Filtres et adresses bloquees > Creer un filtre.

Criteres de filtrage disponibles :
- **De** : adresse ou domaine de l'expediteur
- **A** : adresse du destinataire (utile pour les alias +tag)
- **Objet** : mots-cles dans l'objet
- **Contient les mots** : recherche dans le corps de l'email
- **Ne contient pas** : exclusion de termes
- **Taille** : superieure ou inferieure a une taille
- **Contient une piece jointe** : oui/non
- **Exclure les conversations importees** : oui/non

Actions disponibles :
- Ignorer la boite de reception (archiver)
- Marquer comme lu
- Ajouter un libelle
- Transferer a une adresse
- Supprimer
- Ne jamais envoyer dans le spam
- Toujours/jamais marquer comme important
- Appliquer un modele (template)
- Categoriser (Principal, Reseaux sociaux, Promotions, Notifications, Forums)

#### Filtres essentiels

1. **Newsletters** : De contient "newsletter" OU "noreply" OU "no-reply" → Ajouter libelle "Newsletters", ignorer la boite de reception, marquer comme lu
2. **Notifications systeme** : De contient "@github.com" OU "@jira" OU "@trello" → Ajouter libelle "Notifications", ignorer la boite de reception
3. **CC/BCC** : A ne contient PAS mon adresse directe → Ajouter libelle "CC-FYI", marquer comme lu
4. **Emails internes importants** : De contient "@monentreprise.com" ET De contient "direction" → Ne jamais envoyer dans le spam, marquer comme important

#### Technique du Plus Addressing

Gmail ignore tout ce qui suit le signe "+" dans une adresse. Utiliser cette fonctionnalite pour creer des alias de filtrage :
- `nom+newsletters@gmail.com` pour les abonnements
- `nom+achats@gmail.com` pour les confirmations de commande
- `nom+projet-x@gmail.com` pour un projet specifique

Creer ensuite des filtres bases sur le champ "A" pour un routage automatique precis.

### Labels (Libelles)

Les labels Gmail sont plus flexibles que les dossiers Outlook : un email peut avoir plusieurs labels, et les labels supportent une hierarchie (labels imbriques).

Systeme de labels recommande :

```
@Action
@Attente
@Reference
@Lire
──────────
Projets/
  Projet-Alpha
  Projet-Beta
  Projet-Gamma
──────────
Personnes/
  Manager
  Equipe
  Clients
──────────
Type/
  Newsletters
  Notifications
  Factures
  Contrats
```

Bonnes pratiques :
- Utiliser le prefixe "@" pour les labels d'action (ils apparaissent en premier dans la liste)
- Limiter les labels a 20-30 maximum (au-dela, la navigation devient penible)
- Utiliser des couleurs coherentes avec le systeme de categories
- Reviser les labels chaque trimestre pour supprimer les obsoletes

### Multiple Inboxes

La fonctionnalite Multiple Inboxes de Gmail permet d'afficher jusqu'a 5 sections supplementaires a cote de la boite de reception principale.

Configuration recommandee (Parametres > Avance > Multiple Inboxes) :
- **Section 1** : `label:@Action` — Emails necessitant une action
- **Section 2** : `label:@Attente` — Emails en attente de reponse
- **Section 3** : `is:starred` — Emails marques d'une etoile (VIP)
- **Section 4** : `label:@Lire` — Contenu a lire plus tard

Position recommandee : a droite de la boite de reception. Taille maximale : 25 emails par section.

### Templates (Modeles de reponse)

Activer les templates : Parametres > Avance > Templates > Activer.

Pour creer un template : rediger un nouvel email, cliquer sur les trois points > Templates > Enregistrer le brouillon comme template.

Pour utiliser un template : nouveau message, trois points > Templates > Inserer le template.

Les templates Gmail sont simples mais limites (pas de variables dynamiques). Pour des templates avances avec personalisation, utiliser des extensions comme Streak, Mixmax, ou Yesware, qui supportent les variables (`{{prenom}}`, `{{entreprise}}`, `{{date}}`).

### Gmail Confidential Mode

Le mode confidentiel de Gmail permet d'envoyer des emails avec :
- **Date d'expiration** : l'email devient inaccessible apres la date fixee
- **Code SMS** : le destinataire doit verifier son identite via un code SMS
- **Pas de transfert** : le destinataire ne peut pas transferer, copier, imprimer ou telecharger le contenu

Utiliser le mode confidentiel pour les informations sensibles : donnees personnelles, informations financieres, contrats en negociation, identifiants temporaires.

### Gmail AI Features (2025-2026)

Google Gemini dans Gmail :
- **Aide a la redaction** : "Help me write" genere des brouillons a partir d'un prompt en langage naturel
- **Raffinement de ton** : formaliser, raccourcir, detailler un brouillon existant
- **Resume de conversations** : synthese automatique des fils de discussion longs
- **Smart Reply ameliore** : reponses suggerees plus contextuelles et plus longues
- **Extraction de taches** : identification des action items et creation de taches dans Google Tasks

---

## Templates et Snippets d'Email

### Pourquoi les templates sont essentiels

Un professionnel envoie en moyenne 40 emails par jour. Parmi ceux-ci, 60 a 70% sont des variations de 10 a 15 types de messages recurrents. Creer des templates pour ces messages recurrents permet de :
- Reduire le temps de redaction de 50 a 80% par email
- Garantir la coherence et la qualite de la communication
- Eliminer la fatigue decisionnelle ("comment formuler ca ?")
- Standardiser les reponses de l'equipe

### Templates essentiels a creer

#### 1. Accuse de reception

```
Objet : RE: [objet original]

Bonjour [Prenom],

Bien recu, merci pour votre message.
Je reviens vers vous [delai : dans la journee / d'ici vendredi / la semaine prochaine]
avec [une reponse detaillee / les elements demandes / ma proposition].

Cordialement,
[Signature]
```

#### 2. Demande d'information

```
Objet : Demande d'information — [sujet]

Bonjour [Prenom],

Dans le cadre de [contexte], j'aurais besoin des informations suivantes :

1. [Information 1]
2. [Information 2]
3. [Information 3]

Serait-il possible de me les transmettre d'ici le [date] ?
N'hesitez pas a me contacter si vous avez des questions.

Merci par avance,
[Signature]
```

#### 3. Relance polie

```
Objet : RE: [objet original] — Relance

Bonjour [Prenom],

Je me permets de revenir vers vous concernant mon email du [date].
Avez-vous eu l'occasion de [consulter le document / valider la proposition / etc.] ?

Je reste disponible si vous avez besoin de precisions.

Cordialement,
[Signature]
```

#### 4. Refus poli

```
Objet : RE: [objet original]

Bonjour [Prenom],

Merci pour votre [proposition / invitation / demande].
Apres reflexion, je ne suis malheureusement pas en mesure de [accepter / participer /
contribuer] pour le moment en raison de [raison breve et honnete].

[Optionnel : suggestion alternative — "Je vous suggere de contacter [personne]"
ou "Je serais disponible a partir de [date]"]

Je vous souhaite [bonne continuation / une excellente journee].

Cordialement,
[Signature]
```

#### 5. Delegation

```
Objet : FW: [objet original] — Action requise

Bonjour [Prenom],

Je te transfere ce sujet car tu es la personne la mieux placee pour le traiter.

Contexte : [resume en 2-3 lignes]
Action attendue : [action precise]
Deadline : [date]

Merci de me confirmer la prise en charge.

[Signature]
```

### Outils de templates avances

| Outil | Plateforme | Fonctionnalites | Prix |
|---|---|---|---|
| **Text Blaze** | Chrome (Gmail, Outlook Web) | Snippets avec variables, logique conditionnelle, formules | Gratuit (basique), 7$/mois |
| **Streak** | Gmail | CRM integre, templates avec merge fields, tracking | Gratuit (basique), 15$/mois |
| **Mixmax** | Gmail | Templates, sequences, scheduling, tracking | 29$/mois |
| **Brevo Templates** | Tous clients | Templates HTML, campagnes, analytics | Gratuit (basique) |
| **Outlook Quick Parts** | Outlook Desktop | Blocs de texte reutilisables (texte + images) | Inclus dans Office |
| **Outlook My Templates** | Outlook Web | Templates simples accessibles depuis le volet lateral | Inclus dans M365 |

---

## Gestion des Signatures

### Principes d'une signature professionnelle

Une signature email efficace doit etre :
- **Concise** : 4 a 6 lignes maximum (nom, titre, entreprise, telephone, lien)
- **Mobile-friendly** : pas d'images lourdes, texte lisible sur petit ecran
- **Coherente** : meme format pour toute l'equipe (charte graphique)
- **Actuelle** : verifier et mettre a jour chaque trimestre

Structure recommandee :

```
[Prenom Nom] | [Titre]
[Entreprise]
[Telephone] | [Email]
[LinkedIn] | [Site web]
```

Eviter : les citations inspirationnelles, les disclaimers juridiques de 20 lignes (sauf obligation legale), les logos en haute resolution (poids email), les animations GIF.

### Gestion multi-signatures

Configurer plusieurs signatures pour differents contextes :
- **Signature complete** : premier email a un nouveau contact (toutes les coordonnees)
- **Signature courte** : reponses dans un fil de discussion (prenom + telephone seulement)
- **Signature projet** : signature specifique pour un projet avec le logo du projet
- **Signature interne** : version allege pour les emails internes

---

## Delegation et Boites Partagees

### Delegation d'email

La delegation d'email permet a un assistant ou un collegue d'acceder a une boite email et d'envoyer des messages "De la part de" ou "Au nom de" le proprietaire.

**Outlook / Exchange** :
- Acces delegue via Fichier > Parametres du compte > Acces delegue
- Niveaux : Reviewer (lecture seule), Author (lire + creer), Editor (lire, creer, modifier, supprimer)
- Le delegue peut envoyer "Au nom de" (mention visible) ou "En tant que" (transparent pour le destinataire)

**Gmail / Google Workspace** :
- Parametres > Comptes > Ajouter un autre compte > Accorder l'acces a votre compte
- Le delegue accede a la boite via le menu de profil
- Les emails envoyes par le delegue affichent "envoye par [delegue] au nom de [proprietaire]"

### Boites partagees vs Listes de distribution

| Caracteristique | Boite partagee | Liste de distribution |
|---|---|---|
| **Adresse** | support@entreprise.com (boite a part entiere) | equipe@entreprise.com (alias vers membres) |
| **Reponses** | Centralisees dans la boite partagee | Chaque membre recoit et repond individuellement |
| **Suivi** | Visibilite sur qui a repondu, qui traite | Aucune visibilite sur le traitement |
| **Historique** | Historique complet dans la boite partagee | Disperse dans les boites individuelles |
| **Usage** | Support client, RH, comptabilite | Communication d'equipe, diffusion d'information |

Recommandation : utiliser les boites partagees pour tout email necessitant un suivi de traitement. Reserver les listes de distribution pour la communication unidirectionnelle (annonces, newsletters internes).

---

## Strategies d'Archivage

### Philosophie d'archivage

Deux ecoles s'affrontent :

1. **Archivage par dossiers** : classer chaque email dans un dossier specifique (par projet, par client, par sujet). Avantage : navigation logique. Inconvenient : temps de classement, difficulte de choix quand un email concerne plusieurs sujets.

2. **Archivage en vrac + recherche** : tout archiver dans un dossier unique "Archive" et utiliser la recherche pour retrouver. Avantage : zero temps de classement. Inconvenient : necessite une maitrise de la recherche avancee.

Recommandation 2025-2026 : **l'archivage en vrac + recherche** est plus efficace grace a la puissance des moteurs de recherche modernes (Outlook Search, Gmail Search). Le temps economise sur le classement compense largement le temps de recherche occasionnel. Exception : les emails reglementes (conformite, audit) qui necessitent un classement structure impose.

### Politique de retention

| Type d'email | Duree de retention | Action |
|---|---|---|
| **Transactionnel** (confirmations, notifications) | 30 jours | Suppression automatique via regle |
| **Operationnel** (echanges projets) | 1 an | Archivage automatique apres projet |
| **Contractuel** (contrats, accords, engagements) | 5-10 ans | Archivage long terme + backup |
| **Legal hold** (litige en cours) | Jusqu'a resolution | Ne pas supprimer, etiqueter "Legal Hold" |
| **Personnel** (networking, mentoring) | Indefini | Archiver avec label specifique |

---

## Maitrise de la Recherche Email

### Operateurs de recherche Outlook

| Operateur | Exemple | Description |
|---|---|---|
| `from:` | `from:jean.dupont@entreprise.com` | Emails d'un expediteur specifique |
| `to:` | `to:equipe@entreprise.com` | Emails envoyes a une adresse |
| `subject:` | `subject:budget 2026` | Mots dans l'objet |
| `hasattachment:yes` | `hasattachment:yes from:manager` | Emails avec pieces jointes |
| `received:` | `received:this week` | Emails recus cette semaine |
| `category:` | `category:Prioritaire` | Emails d'une categorie |
| `AND / OR / NOT` | `from:client NOT subject:newsletter` | Operateurs logiques |

### Operateurs de recherche Gmail

| Operateur | Exemple | Description |
|---|---|---|
| `from:` | `from:jean@entreprise.com` | Expediteur |
| `to:` | `to:me` | Destinataire |
| `subject:` | `subject:reunion hebdo` | Objet |
| `has:attachment` | `has:attachment filename:pdf` | Pieces jointes |
| `after:` / `before:` | `after:2025/01/01 before:2025/06/30` | Periode |
| `is:starred` | `is:starred is:unread` | Etoiles et statut |
| `label:` | `label:projet-alpha` | Label specifique |
| `larger:` / `smaller:` | `larger:10M` | Taille du message |
| `in:anywhere` | `in:anywhere budget` | Rechercher partout (y compris spam et corbeille) |

Astuce avancee Gmail : utiliser la barre de recherche pour creer des filtres. Saisir les criteres de recherche, cliquer sur "Afficher les options de recherche", puis "Creer un filtre".

---

## Optimisation Mobile

### Principes pour l'email mobile

- **Trier, ne pas traiter** : sur mobile, marquer les emails (etoile, flag, snooze) pour traitement ulterieur sur desktop. Ne repondre que si < 2 minutes et la reponse est simple.
- **Notifications selectrices** : activer les notifications uniquement pour les VIP (manager, clients cles). Desactiver toutes les autres notifications.
- **Signatures mobiles** : configurer une signature courte pour le mobile (prenom + telephone). Retirer la mention "Envoye depuis mon iPhone" (non professionnel).
- **Mode offline** : configurer la synchronisation offline pour lire et preparer des reponses sans connexion (avion, metro).

### Applications email recommandees (2025-2026)

| Application | Plateforme | Points forts |
|---|---|---|
| **Outlook Mobile** | iOS, Android | Integration Microsoft 365, Focused Inbox, calendrier integre |
| **Gmail** | iOS, Android | Filtres, labels, integration Google Workspace, Gemini AI |
| **Spark** | iOS, Android, Mac | Smart Inbox, templates, delegation en equipe, AI writing |
| **Superhuman** | iOS, Android, Mac, Web | Vitesse, raccourcis clavier, AI triage, split inbox |
| **Shortwave** | Web, iOS, Android | AI bundling, groupement par sujet, focus mode |

---

## Securite Email

### Reconnaissance du phishing

Signaux d'alerte a verifier systematiquement :

1. **Adresse de l'expediteur** : verifier le domaine exact (ex : `@microsoft-security.com` n'est PAS `@microsoft.com`)
2. **Urgence artificielle** : "Votre compte sera suspendu dans 24h" — les organisations legitimes ne menacent pas par email
3. **Liens suspects** : survoler le lien AVANT de cliquer pour verifier l'URL reelle. Verifier que le domaine correspond a l'expediteur
4. **Pieces jointes inattendues** : ne jamais ouvrir un fichier `.exe`, `.scr`, `.zip` non sollicite. Se mefier des documents Word/Excel avec macros
5. **Fautes d'orthographe** : les emails de phishing contiennent souvent des erreurs (attention : l'IA generative ameliore la qualite des phishing en 2025-2026)
6. **Demandes d'information sensible** : aucune organisation legitime ne demande un mot de passe ou un numero de carte par email

### Chiffrement des emails

| Methode | Outlook | Gmail | Description |
|---|---|---|---|
| **TLS** | Automatique (Exchange) | Automatique | Chiffrement en transit (standard, transparent) |
| **S/MIME** | Support natif | Support natif (Google Workspace) | Certificats individuels, signature et chiffrement |
| **OME** | Office Message Encryption | — | Chiffrement Microsoft pour destinataires externes |
| **Mode confidentiel** | — | Natif Gmail | Expiration, code SMS, pas de transfert |
| **PGP** | Via plugins | Via plugins (FlowCrypt) | Chiffrement bout en bout, gestion cles manuelle |

Recommandation : le TLS est suffisant pour 90% des communications professionnelles. Utiliser S/MIME ou OME pour les donnees sensibles (RH, finance, M&A). Utiliser le mode confidentiel Gmail pour les partages ponctuels sensibles.

---

## Analytics Email

### Metriques a suivre

| Metrique | Comment mesurer | Objectif |
|---|---|---|
| **Emails recus/jour** | Compteur email ou RescueTime | Reduire de 20% par trimestre (via filtres, desabonnement) |
| **Temps email/jour** | Toggl Track, RescueTime, Viva Insights | < 1 heure par jour pour un contributeur individuel |
| **Inbox end-of-day** | Comptage manuel | 0 (Inbox Zero) |
| **Temps de reponse moyen** | Outlook Insights, Gmail Meter | < 4h pour emails directs, < 24h pour CC |
| **Emails envoyes/jour** | Compteur email | Reduire en privilegiant d'autres canaux quand pertinent |
| **Taux de desabonnement** | Mensuel, apres nettoyage | Desabonner 5-10 listes par mois jusqu'a stabilisation |

### Outils d'analytics email

- **Viva Insights (Microsoft 365)** : temps passe en email, reunions, focus time. Tableau de bord personnel avec recommandations. Integration Outlook native.
- **Gmail Meter** : rapport hebdomadaire sur le volume, les expediteurs principaux, les heures d'activite. Plugin gratuit pour Google Workspace.
- **RescueTime** : tracking automatique du temps par application (email, navigateur, outils). Rapports de productivite detailles.
- **EmailAnalytics** : visualisation des patterns d'email d'equipe. Utile pour les managers qui veulent comprendre la charge email de leur equipe.
- **SaneBox Analytics** : statistiques sur les emails traites, archives, et filtres. Mesure de l'efficacite du tri automatique.

---

## Desabonnement et Nettoyage

### Strategie de desabonnement

La premiere action pour reduire le volume d'email est un desabonnement massif des newsletters et listes non essentielles.

Processus recommande :
1. Rechercher "unsubscribe" ou "se desabonner" dans la boite email
2. Lister toutes les sources recurrentes non essentielles
3. Se desabonner directement depuis chaque email (lien en bas de page)
4. Pour les sources resistantes : utiliser Unroll.me (attention a la confidentialite) ou creer un filtre de suppression automatique
5. Repeter chaque mois pendant 3 mois, puis chaque trimestre

### Clean Email et SaneBox

- **Clean Email** : outil de nettoyage qui regroupe les emails par expediteur et par type. Permet de desabonner, archiver, ou supprimer en masse. Regles automatiques d'archivage.
- **SaneBox** : filtrage intelligent qui apprend du comportement. Cree des dossiers automatiques (SaneLater, SaneNews, SaneNoReplies). Service externe compatible avec tous les clients email.

Recommandation : commencer par un nettoyage manuel (gratuit, formateur), puis envisager SaneBox ou Clean Email si le volume reste > 100 emails/jour apres 3 mois d'optimisation.

---

## Email et Communication Asynchrone

### Quand NE PAS envoyer un email

L'email n'est pas toujours le bon canal. Regles de decision :

| Situation | Canal recommande |
|---|---|
| Discussion qui necessite plus de 3 allers-retours | Appel telephone ou visioconference |
| Information urgente (< 1h) | Message instantane (Slack, Teams) |
| Feedback sensible ou emotionnel | Conversation en personne ou visio |
| Partage de document pour collaboration | Lien vers document partage (Google Docs, SharePoint) |
| Annonce a toute l'equipe | Canal Slack/Teams dedie |
| Suivi de tache ou projet | Outil de gestion de projet (Jira, Asana, Trello) |

### Ecrire des emails efficaces

Principes de redaction pour maximiser le taux de reponse et minimiser les allers-retours :

1. **Objet explicite** : l'objet doit resumer l'action attendue. "[ACTION] Validation budget Q3 avant vendredi" plutot que "Budget"
2. **Une demande par email** : si plusieurs sujets, envoyer plusieurs emails. Un email multi-sujets genere des reponses partielles
3. **Bottom Line Up Front (BLUF)** : la conclusion ou la demande en premier paragraphe. Le contexte ensuite.
4. **Formatage scannable** : bullets, gras pour les points cles, paragraphes courts. Les emails longs en blocs de texte ne sont pas lus
5. **Deadline explicite** : "Merci de me repondre avant le mercredi 12 mars a 17h" plutot que "des que possible"
6. **Minimiser les destinataires** : chaque CC supplementaire reduit la probabilite de reponse (diffusion de responsabilite). Ne mettre en CC que les personnes qui ont un besoin reel de l'information

---

## Integrations et Ecosystem Email

### Outlook + Microsoft 365

- **Teams** : partager un email dans un canal Teams en un clic. Utiliser Teams pour les discussions et email pour les communications formelles
- **OneNote** : envoyer un email a OneNote pour archivage et annotation (bouton "Envoyer a OneNote")
- **To Do** : transformer un email en tache To Do avec un clic (flag). Synchronisation bidirectionnelle
- **SharePoint / OneDrive** : envoyer des liens plutot que des pieces jointes. Controle de version et permissions

### Gmail + Google Workspace

- **Google Chat** : partager un email dans un espace Google Chat. Basculer entre email et chat selon la nature de l'echange
- **Google Tasks** : creer une tache a partir d'un email (glisser-deposer dans le volet Tasks)
- **Google Drive** : pieces jointes automatiquement sauvegardees dans Drive. Partage de liens au lieu de fichiers
- **Google Calendar** : creer un evenement a partir d'un email. Integration bidirectionnelle des invitations

### Outils tiers d'integration

- **Zapier / Make** : connecter l'email a des centaines d'applications (CRM, task manager, spreadsheet, base de donnees)
- **IFTTT** : automatisations simples (ex : sauvegarder les pieces jointes Gmail dans Google Drive)
- **Power Automate** : automatisation native Microsoft 365 (ex : creer une tache Planner pour chaque email flagge)
