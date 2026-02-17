# Etudes de Cas -- Product Strategy & Roadmap

## Overview

Ces etudes de cas illustrent les concepts cles de la strategie produit a travers cinq entreprises qui ont defini les standards du product management moderne. Chaque cas detaille les decisions strategiques, les frameworks utilises et les metriques d'impact.

Utiliser ces exemples comme references concretes pour alimenter les reflexions sur la vision produit, la priorisation, la discovery continue et les strategies de croissance product-led. Les cinq cas couvrent des concepts complementaires : dogfooding et North Star Metric (Slack), user research et community-led growth (Notion), differenciation technologique et creation de categorie (Figma), strategie opinionnee et execution rapide (Linear), et mesure systematique du PMF (Superhuman).

---

## Cas 1 : Slack -- De l'outil interne au moteur de Product-Led Growth

### Contexte

Slack nait en 2013 comme un outil interne developpe par l'equipe de Tiny Speck, startup de jeu video fondee par Stewart Butterfield (co-fondateur de Flickr). L'equipe de 45 personnes construit un jeu multijoueur appele Glitch et developpe un systeme de communication interne pour coordonner le travail distribue entre San Francisco, Vancouver et New York. Le jeu echoue commercialement et ferme en novembre 2012, mais l'equipe realise que l'outil de communication qu'elle a construit resout un probleme universel : la fragmentation des communications d'equipe. Butterfield decide de pivoter l'entreprise vers ce produit.

Le marche de la communication d'entreprise est domine par Microsoft (Lync/Skype for Business), Cisco (WebEx) et HipChat (Atlassian), mais aucun acteur ne propose une experience utilisateur comparable aux applications grand public.

### Probleme

Le marche de la communication d'entreprise en 2013 presente trois problemes structurels :

- **Surcharge d'email** : un employe de bureau recoit en moyenne 121 emails par jour (etude Radicati Group, 2013), dont 30% seulement sont pertinents
- **Fragmentation des outils** : les equipes utilisent en moyenne 5 a 7 outils differents pour communiquer, sans integration entre eux
- **Ecart d'experience** : les outils professionnels sont concus pour les departements IT, pas pour les utilisateurs finaux -- interfaces archaiques, deploiements complexes

La question strategique centrale : comment creer un produit adopte par les equipes elles-memes (bottom-up), sans necessiter une decision d'achat top-down par l'IT ?

### Approche

1. **Dogfooding intensif et PMF iteratif** : Avant tout lancement externe, l'equipe utilise exclusivement Slack pendant 6 mois en interne. Butterfield instaure une regle : tout feedback doit etre remonte via un canal dedie (#meta-feedback), creant une boucle de retour continue. Cette periode permet d'identifier et de resoudre plus de 500 problemes d'utilisabilite avant la beta privee.

2. **Beta privee selective et mesure du PMF** : En mai 2013, Slack lance une beta privee sur invitation, limitee a 8 entreprises partenaires (dont Rdio, Cozy et Medium). L'equipe mesure le PMF via deux metriques : le pourcentage d'equipes envoyant plus de 2 000 messages dans les 30 premiers jours et le taux de retention D30. En aout 2013, 100% des equipes beta depassent le seuil de 2 000 messages et la retention D30 atteint 93%.

3. **Definition de la North Star Metric** : Slack choisit le nombre de messages envoyes par equipe par jour, une metrique qui capture l'adoption, l'engagement et la valeur delivree. Cette NSM est decomposee en input metrics : equipes actives, utilisateurs actifs par equipe, canaux crees et integrations connectees. Chaque feature de la roadmap est evaluee par son impact sur ces input metrics.

4. **Boucle de croissance virale intrinseque** : La viralite est integree dans le produit lui-meme. Pour qu'un canal soit utile, il faut y inviter ses collegues. Chaque nouvel utilisateur invite en moyenne 3 a 5 personnes dans les 48 heures. Le coefficient viral depasse 1.0 des les premiers mois, generant une croissance organique exponentielle. L'equipe renforce cette boucle en facilitant l'invitation (un seul clic) et en rendant l'onboarding instantane.

5. **Strategie d'integrations comme moat** : Slack lance un programme d'integrations connectant plus de 80 outils tiers (GitHub, Trello, Google Drive, JIRA). Chaque integration augmente le switching cost, renforce l'effet reseau et positionne Slack comme le hub central de l'information. En 2015, le nombre d'integrations atteint 900.

### Resultat

- Lancement public en fevrier 2014 : 8 000 entreprises inscrites le premier jour
- 500 000 DAU en fevrier 2015 (12 mois post-lancement)
- 1 million de DAU en juin 2015, croissance de 100% en 4 mois sans budget d'acquisition significatif
- Conversion freemium vers plan payant de 30% (benchmark B2B SaaS : 2-5%)
- 93% des equipes depassant le seuil de 2 000 messages deviennent payantes
- Valorisation de 1,12Md$ en avril 2014 (licorne en moins de 12 mois post-lancement)
- Acquisition par Salesforce en 2021 pour 27,7Md$

### Lecons apprises

- Le dogfooding est un prerequis pour le PMF dans les outils de productivite. Les 6 mois d'utilisation interne ont permis un niveau de polish qu'aucun concurrent n'avait. Appliquer systematiquement cette pratique avant tout lancement externe.
- La North Star Metric doit capturer la valeur delivree, pas l'activite brute. "Messages envoyes" fonctionne car il est correle a la valeur (communication d'equipe effective). Choisir une NSM dont l'augmentation prouve que les utilisateurs obtiennent plus de valeur.
- La viralite la plus puissante est inherente au fonctionnement du produit, pas aux incitations artificielles (parrainage, reductions). Slack est plus utile quand plus de collegues l'utilisent, ce qui cree une boucle de croissance auto-entretenue.
- La strategie d'integrations cree un moat plus durable que les features -- les concurrents peuvent copier une fonctionnalite, mais pas un ecosysteme de 900 integrations. Investir dans les API et les partenariats technologiques des les premiers stades.

---

## Cas 2 : Notion -- Croissance par les templates et la communaute

### Contexte

Notion est fonde en 2013 par Ivan Zhao et Simon Last a San Francisco. La vision : unifier documents, bases de donnees, wikis et gestion de projet dans un seul espace de travail. Apres un premier lancement rate en 2015 (Notion 1.0, mal accueilli pour sa complexite), l'equipe de 4 personnes s'installe a Kyoto au Japon pendant 18 mois pour reconstruire le produit de zero. Notion 2.0 est lance en mars 2018.

Le marche est sature d'outils specialises : Evernote (notes), Google Docs (documents), Trello (kanban), Confluence (wiki), Airtable (bases de donnees). Chaque outil fait bien une chose, mais la fragmentation genere de la friction. Le defi strategique : convaincre les utilisateurs d'abandonner plusieurs outils au profit d'une plateforme unifiee.

### Probleme

Trois obstacles structurels menacent l'adoption :

- **Blank canvas** : la flexibilite extreme cree une paralysie pour les nouveaux utilisateurs. Taux de retention D7 de 45%, en dessous du seuil acceptable de 50%
- **Perception erronee** : 70% des utilisateurs d'essai (entretiens Q2 2018) percoivent Notion comme un concurrent d'Evernote, pas comme un remplacement de leur stack complet
- **Cout de migration** : passer de 3 a 5 outils specialises vers Notion represente un investissement en temps que la plupart des equipes ne sont pas pretes a consentir

### Approche

1. **User research intensive pour redefinir le positionnement** : Entre avril et septembre 2018, l'equipe conduit plus de 200 entretiens structures autour de la question : "Decrivez-moi votre espace de travail ideal." L'analyse revele que les utilisateurs cherchent un systeme pour organiser leur vie professionnelle de maniere personnalisee. Pivot du positionnement : de "all-in-one workspace" a "connected workspace that adapts to you".

2. **Templates comme moteur d'onboarding** : En octobre 2018, Notion lance une galerie de templates couvrant 15 cas d'usage : CRM personnel, wiki d'equipe, suivi d'habitudes, gestion de projet. Chaque template montre une capacite specifique (blocs, bases relationnelles, vues multiples) et est fonctionnel immediatement. Impact : les utilisateurs qui dupliquent un template dans les 24 premieres heures ont une retention D30 de 72%, contre 38% pour ceux qui commencent avec une page vierge.

3. **Community-led discovery** : En 2019, Notion ouvre la publication de templates communautaires. Des ambassadeurs emergent, creant templates avances et tutoriels YouTube. Le programme "Notion Ambassadors" est formalise en 2020 avec 200 ambassadeurs dans 40 pays. Un ecosysteme marchand se developpe sur Gumroad, generant plusieurs millions de dollars par an. Chaque template partage devient un vecteur d'acquisition organique.

4. **Strategie de use case expansion** : Penetration par use case plutot que positionnement plateforme generique. Premier use case : le wiki d'equipe (remplacement de Confluence), pour son ratio impact/effort de migration optimal. L'expansion vers la gestion de projet puis les documents se fait naturellement. Le "use case expansion rate" passe de 1,2 a 3,8 categories par workspace entre 2019 et 2021.

5. **Product-led growth self-serve** : Modele freemium genereux (usage individuel gratuit sans limite) pour maximiser l'adoption individuelle, avec upsell vers le plan Team lors de l'invitation de collegues. Metrique de conversion cle : le "team activation moment" -- 3 membres collaborant sur le meme document dans les 14 premiers jours.

### Resultat

- Retention D7 passee de 45% a 62% apres l'introduction des templates (+38%)
- 4M utilisateurs en 2020, 30M en 2022, 100M en 2024 -- croissance portee a 80% par l'organique
- Valorisation passee de 800M$ (2019) a 10Md$ (2021)
- Plus de 250 000 templates communautaires disponibles en 2024
- NPS de 65 (top 5% des outils SaaS B2B)
- Sean Ellis score de 58%, bien au-dessus du seuil PMF de 40%

### Lecons apprises

- La user research qualitative peut reveler un positionnement radicalement different de celui prevu. Les 200 entretiens ont transforme la trajectoire du produit.
- Le blank canvas est un tueur silencieux de retention. Fournir des templates fonctionnels immediatement est le levier d'onboarding le plus sous-estime dans les outils flexibles.
- La communaute est le meilleur moteur de discovery a long terme. Les ambassadeurs font le travail d'education produit que l'equipe marketing ne peut pas faire a grande echelle.
- L'expansion par use case (atterrir avec un cas, etendre vers les autres) est plus efficace que le positionnement plateforme des le depart.

---

## Cas 3 : Figma -- Le multiplayer comme differenciation strategique

### Contexte

Figma est fonde en 2012 par Dylan Field (20 ans, ancien stagiaire LinkedIn) et Evan Wallace (ancien Google). L'entreprise passe 4 ans en mode stealth avant sa premiere version publique en septembre 2016. Le marche du design d'interface est domine par Sketch (leader macOS avec 1 million d'utilisateurs payants) et Adobe (position dominante historique).

Le workflow standard des designers en 2016 : creer dans Sketch, exporter en PNG ou PDF, partager via InVision ou Zeplin pour les feedbacks, iterer manuellement. Ce processus genere une latence de 24 a 48 heures entre chaque cycle de feedback, des problemes de versioning et une exclusion des non-designers du processus de creation.

### Probleme

Le workflow fragmentaire du design presente trois problemes fondamentaux :

- **Collaboration** : les designers travaillent en silo dans leurs fichiers locaux, le partage requiert des exports manuels et des outils tiers, creant une stack de 4 a 6 outils pour un seul workflow
- **Versioning** : les fichiers vivent sur les machines locales avec des conventions de nommage manuelles ("Homepage_v3_final_FINAL2.sketch"), generant conflits et pertes de travail
- **Accessibilite** : seuls les designers equipes d'un Mac et d'une licence Sketch peuvent participer, excluant developers, PMs et stakeholders

La question strategique : construire un outil de design professionnel dans le navigateur, avec une performance native, et une collaboration temps reel qui transforme le design en activite d'equipe ?

### Approche

1. **Pari technologique : WebGL et CRDTs** : Pendant 4 ans (2012-2016), Figma investit dans deux innovations. Un moteur de rendu 2D base sur WebGL offrant des performances natives dans le navigateur. Et un systeme de collaboration temps reel base sur les CRDTs (Conflict-free Replicated Data Types) permettant le travail simultanee sans conflits. Ce choix, extremement risque en 2012, fonde la differenciation strategique de Figma.

2. **Positionnement "multiplayer" comme categorie** : Plutot que "un meilleur Sketch" ou "Sketch dans le navigateur", Figma invente la categorie du "multiplayer design". Le terme emprunte au gaming evoque la collaboration temps reel. Ce positionnement evite la comparaison feature-by-feature et redefinit les criteres de choix du marche autour de la collaboration.

3. **Browser-first pour eliminer les barrieres** : Le navigateur elimine trois barrieres simultanement : pas d'installation (un lien suffit), pas de restriction d'OS (Windows, Mac, Linux, Chromebook), et un partage frictionless (lien = acces). Un PM peut commenter dans Figma, un developer peut inspecter et extraire le CSS, un stakeholder peut observer une session en direct. Figma transforme le design de "fichier" en "URL".

4. **Freemium pour l'adoption bottom-up** : Le plan gratuit (3 projets, editeurs illimites en draft) permet a n'importe quel designer d'adopter individuellement. La metrique d'activation : le moment ou un designer invite un non-designer a commenter. Ce moment transforme Figma d'outil individuel en outil d'equipe et declenche la boucle d'expansion.

5. **Ecosysteme de plugins et community files** : En aout 2019, Figma lance les plugins communautaires (1 000 plugins en 6 mois). La fonctionnalite "Community Files" permet de publier design systems, templates et kits UI. Cette strategie de plateforme cree un ecosysteme qui renforce la valeur et augmente les switching costs.

### Resultat

- De 0 a 4 millions d'utilisateurs entre 2016 et 2021, depassant Sketch en parts de marche des 2020
- ARR de 400M$ en 2022, croissance de plus de 100%/an pendant 3 ans consecutifs
- Offre de rachat par Adobe pour 20Md$ en 2022 (annulee en 2023 pour raisons regulatoires)
- 85% des equipes design du Fortune 500 utilisent Figma en 2023
- Coefficient viral : chaque designer invite en moyenne 7 non-designers, effet multiplicateur x8
- NRR superieur a 150%, porte par l'expansion au sein des organisations
- Plus de 5 000 plugins et 300 000 community files

### Lecons apprises

- Un pari technologique fondamental peut creer un avantage quasi-inattaquable. Les 4 ans de stealth ont rendu la differenciation technique extremement difficile a repliquer.
- Le positionnement par creation de categorie est plus puissant que le positionnement comparatif. Redefinir les criteres de choix oblige les concurrents a jouer selon de nouvelles regles.
- Le modele browser-first transforme le produit de "fichier" en "URL", changeant fondamentalement la dynamique de partage et d'adoption.
- Rendre le produit utile a des roles adjacents (non-designers) multiplie par 8 la base d'utilisateurs potentiels au sein de chaque organisation.

---

## Cas 4 : Linear -- La strategie produit opinionnee comme avantage competitif

### Contexte

Linear est fonde en 2019 par Karri Saarinen (ancien lead designer Airbnb, co-createur du design system Coinbase) et Tuomas Artman (ancien engineering manager Uber). Le produit est un outil de suivi d'issues pour les equipes d'ingenierie. Le marche est domine par Jira (Atlassian), utilise par plus de 75 000 organisations, avec un quasi-monopole enterprise.

Jira est reconnu pour sa flexibilite infinie -- et simultanement deteste par une majorite de ses utilisateurs pour sa complexite, sa lenteur et la surcharge de configuration. D'autres alternatives existent (Asana, Monday, Shortcut, ClickUp) mais ciblent la gestion de projet generique et manquent de profondeur pour les workflows d'ingenierie.

Le marche semble verrouille : Jira beneficie d'effets de reseau massifs (integrations, habitudes, donnees historiques) et d'un lock-in institutionnel dans la plupart des grandes organisations.

### Probleme

Les enquetes conduites par Saarinen et Artman aupres de 50 CTOs revelent trois frustrations recurrentes :

- **Lenteur** : temps de chargement de 4 a 8 secondes par board, actions courantes necessitant plusieurs clics. Pour des ingenieurs passant 30 a 60 minutes par jour dans l'outil, la friction accumulee est considerable
- **Sur-configuration** : des centaines de champs, workflows et permissions personnalisables qui generent des semaines de configuration et une dette de complexite
- **UX degradee** : interface non repensee depuis des annees, accumulation de fonctionnalites creant une experience fragmentee

Le pari strategique : existe-t-il un marche pour un outil opinionne qui sacrifie la flexibilite au profit de la vitesse et de la simplicite ?

### Approche

1. **Contraindre pour simplifier** : Linear impose un workflow standard (Backlog, Todo, In Progress, Done, Cancelled) avec des adaptations limitees, et un ensemble reduit de champs couvrant 90% des besoins. Chaque feature retiree est une decision consciente. Le principe interne : "We don't build features for edge cases. We build the best experience for the common case."

2. **Performance comme feature produit** : Architecture client-first (synchronisation locale, optimistic updates) garantissant un temps de reponse de moins de 50ms pour toute action. Les transitions sont instantanees, la creation d'un ticket prend moins de 2 secondes. Metrique interne : chaque interaction doit se ressentir "instantanee" (< 100ms de temps percu).

3. **Keyboard-first et developer experience** : Chaque action peut etre executee sans la souris, avec raccourcis memorisables et command palette (Cmd+K). Cette approche cible les ingenieurs au detriment de la decouverte intuitive pour les debutants. Le pari : si les ingenieurs adorent l'outil, l'adoption suit.

4. **Execution rapide comme avantage competitif** : Avec moins de 50 personnes (contre 7 000+ chez Atlassian), Linear publie des changelogs hebdomadaires detailles qui deviennent un outil marketing. Chaque changelog est concu comme un mini-article avec captures, explications de design et details techniques. Les changelogs sont suivis par 15 000 abonnes.

5. **Adoption bottom-up exclusive** : Pas de force de vente, pas de demos obligatoires, pas de contrats annuels. Un ingenieur decouvre Linear, l'essaie avec son equipe, puis convertit. Moment d'activation : quand l'equipe complete son premier sprint et constate la difference de vitesse. Linear investit dans le contenu (articles, guides de migration) plutot que dans la vente.

### Resultat

- Plus de 10 000 equipes en 2023 (Vercel, Ramp, Coinbase, Cash App, Watershed)
- ARR depassant 30M$ en 2023, croissance de plus de 200%/an
- Levees de 52M$ a une valorisation de 400M$ (Series B, 2022)
- NPS de 72, le plus eleve de la categorie (Jira : 10-15)
- Creation d'un ticket : 1,8s dans Linear vs 12s dans Jira
- 60% des nouvelles equipes migrent depuis Jira
- Moins de 60 personnes gerant un produit utilise par des dizaines de milliers d'equipes

### Lecons apprises

- Un produit opinionne qui fait bien 80% des cas d'usage peut battre un produit flexible qui fait mediocrement 100% des cas. Evaluer pour chaque feature si la flexibilite ajoutee vaut la complexite induite.
- La performance est une feature produit. La difference entre 50ms et 5 secondes se traduit directement en satisfaction et en adoption.
- L'execution rapide avec une petite equipe est un avantage structurel contre les incumbents. Publier les changelogs de maniere visible pour rendre le momentum tangible.
- Cibler le praticien (ingenieur) plutot que le decideur (VP Engineering). Concevoir l'experience pour le power user, pas pour le buyer.

---

## Cas 5 : Superhuman -- Le moteur systematique de Product-Market Fit

### Contexte

Superhuman est fonde en 2014 par Rahul Vohra, egalement fondateur de Rapportive (extension Gmail acquise par LinkedIn en 2012). Le produit est un client email premium pour les professionnels a haut volume de correspondance. Le marche est domine par Gmail (1,8 milliard d'utilisateurs) et Outlook (400 millions), deux produits gratuits. Plusieurs startups ont tente de reinventer l'email (Mailbox, Inbox by Google, Newton) et la plupart ont echoue.

Le marche est considere comme impossible par de nombreux investisseurs : comment construire un business viable en concurrencant un produit gratuit de Google sur un cas d'usage ou les habitudes sont profondement ancrees ?

Vohra passe 3 ans (2014-2017) a construire le produit en stealth avec 15 personnes, finance par 33M$ de levees de fonds.

### Probleme

En Q3 2017, apres 3 ans de developpement, Superhuman est en beta privee avec environ 100 utilisateurs. Le produit est fonctionnellement abouti (client email rapide, keyboard-first, design soigne), mais Vohra ne peut repondre a la question fondamentale : avons-nous atteint le PMF ?

Les signaux sont ambigus :
- Certains utilisateurs refusent de revenir a Gmail, d'autres desinstallent
- NPS de 45 -- correct mais pas exceptionnel
- Retention D30 de 60% -- insuffisante pour un client email principal
- Feedbacks contradictoires : plus d'integrations, plus de raccourcis, "trop different" de Gmail

L'equipe est desorientee par l'absence de boussole claire pour piloter les iterations.

### Approche

1. **Implementation systematique du Sean Ellis Test** : En janvier 2018, Vohra envoie a tous les utilisateurs actifs (environ 150) la question : "Comment vous sentiriez-vous si vous ne pouviez plus utiliser Superhuman ?" Reponses possibles : "Tres decu(e)", "Un peu decu(e)", "Pas decu(e)", "Je ne l'utilise plus". Resultat initial : 22% repondent "Tres decu(e)", bien en dessous du seuil PMF de 40%. Ce score fournit une baseline mesurable.

2. **Segmentation pour identifier le coeur de cible** : Vohra segmente les reponses par profil. Les fondateurs de startups et managing partners de fonds VC scorent a 48% ("Tres decu(e)"), au-dessus du seuil, tandis que les autres profils scorent a 12%. Decision decisive : doubler sur le segment ou le PMF est le plus fort et ignorer temporairement les autres.

3. **Roadmap extraite du questionnaire PMF** : Deux questions complementaires : "Quel est le principal benefice ?" et "Comment ameliorer Superhuman ?" Vohra se concentre sur les suggestions des utilisateurs "Tres decu(e)" et "Un peu decu(e)" uniquement, ignorant les feedbacks des "Pas decu(e)" (hors coeur de cible). Themes prioritaires : vitesse, raccourcis clavier, recherche instantanee, snooze et calendrier integre.

4. **Boucle iterative de mesure du PMF** : Rituel trimestriel -- le Sean Ellis test est renvoye a tous les utilisateurs actifs et le score PMF est recalcule. Ce score devient la North Star Metric pendant la phase pre-PMF. L'equipe ne mesure ni le revenue ni l'acquisition, uniquement le pourcentage de "Tres decu(e)". Chaque initiative de la roadmap est evaluee par sa contribution attendue a l'amelioration de ce score. Progression :
   - Q1 2018 : 22% (baseline)
   - Q2 2018 : 33% (apres amelioration vitesse, raccourcis, recherche)
   - Q4 2018 : 42% (seuil PMF de 40% depasse pour la premiere fois)
   - Q2 2019 : 58% (PMF consolide)

5. **Waitlist et onboarding individuel** : Plutot qu'un lancement public, waitlist atteignant 300 000 personnes. Chaque nouvel utilisateur passe par un onboarding individuel de 30 minutes en video. Trois objectifs : maximiser la retention, collecter du feedback structure, creer un effet de rarete renforcant la desirabilite. Le ratio d'onboarding (1 session pour 1 000 inscrits) alimente le bouche-a-oreille.

### Resultat

- Score Sean Ellis passe de 22% a 58% en 18 mois, progression methodique et reproductible
- Waitlist de 300 000 personnes, couverture mediatique massive sans budget marketing
- Retention D90 superieure a 85% parmi les utilisateurs onboardes, exceptionnel pour un produit email payant
- ARR depassant 30M$ en 2022, avec un prix premium de 30$/mois/utilisateur dans un marche ou le concurrent principal (Gmail) est gratuit
- Levees cumulees de 108M$ (Series C, 2021) a une valorisation de 825M$
- Le framework PMF de Vohra est adopte par des centaines de startups et enseigne chez Y Combinator, a16z et First Round
- NPS passe de 45 a 75 apres l'implementation du moteur PMF

### Lecons apprises

- Le PMF n'est pas un evenement binaire mais un score continu. Implementer le Sean Ellis test comme metrique recurrente et piloter la roadmap en fonction de ce score.
- La segmentation des repondants est aussi importante que le score global. Identifier le segment "Tres decu(e)" et doubler dessus plutot que de diluer le produit.
- Les feedbacks des utilisateurs qui n'aiment pas le produit sont du bruit. Se concentrer sur les suggestions des "Tres decu(e)" et "Un peu decu(e)" pour construire la roadmap.
- La rarete artificielle (waitlist, onboarding individuel) est une strategie viable pour les produits premium. Le cout de l'onboarding (30 min/utilisateur) est compense par une retention et un LTV exceptionnels.
- La methode Superhuman demontre que le PMF peut etre traite comme un probleme d'ingenierie : mesurer, segmenter, prioriser, iterer, re-mesurer. Cette approche systematique est transposable a n'importe quel produit, quel que soit le stade ou le marche.
