# Etudes de Cas -- User Research & Product Discovery

## Overview

Ce document presente cinq etudes de cas illustrant comment des organisations de premier plan ont utilise la recherche utilisateur pour transformer leurs produits et services.
Chaque cas met en evidence des methodes specifiques (ethnographie, diary studies, JTBD, A/B testing comportemental, tests d'utilisabilite continus), les insights decouverts, et l'impact concret sur les decisions produit.
Ces exemples couvrent des contextes varies -- marketplace grand public, streaming musical, services publics numeriques, edtech mobile et SaaS B2B -- pour montrer que la recherche utilisateur, appliquee avec rigueur, produit des resultats mesurables independamment du secteur ou de la taille de l'organisation.

---

## Cas 1 : Airbnb -- La refonte guidee par la recherche terrain

### Contexte

En 2009, Airbnb est une startup en difficulte.
La plateforme de location entre particuliers genere moins de 200 dollars de revenus par semaine.
Les fondateurs Brian Chesky, Joe Gebbia et Nathan Blecharczyk observent que les annonces stagnent, que les taux de conversion restent faibles et que la confiance entre hotes et voyageurs ne s'etablit pas.
Les photos des logements sont mediocres, les descriptions manquent de personnalite, et l'experience de reservation reste generique.
L'equipe, composee de 3 personnes, ne dispose d'aucune donnee comportementale significative et ne comprend pas pourquoi les visiteurs du site ne convertissent pas.
Le modele economique repose sur la commission sur les reservations, mais le volume de transactions est trop faible pour assurer la survie de l'entreprise.

### Probleme

Le probleme central est un deficit de confiance.
Les utilisateurs potentiels hesitent a louer le logement d'un inconnu et les hotes craignent d'accueillir des etrangers chez eux.
Les photos amateurs degradent la perception de qualite des annonces.
Le processus de reservation ne cree aucun lien humain entre les parties.
L'equipe ne comprend pas les motivations profondes des voyageurs qui choisissent Airbnb plutot qu'un hotel, ni les freins psychologiques qui bloquent les autres.
Les metriques web classiques (trafic, taux de rebond) ne suffisent pas a expliquer le blocage.
Sans recherche utilisateur, l'equipe risque de construire des fonctionnalites basees sur des hypotheses erronees.

### Approche

1. **Immersion ethnographique** : Les fondateurs se rendent a New York, leur principal marche, pour sejourner chez des hotes Airbnb et observer l'experience de bout en bout.
Pendant plusieurs semaines, ils vivent l'experience utilisateur complete -- recherche d'annonce, reservation, arrivee, sejour, depart.
Cette immersion revele les points de friction invisibles dans les donnees : la qualite deplorable des photos, l'absence d'informations sur le quartier, le manque de personnalisation de l'accueil.

2. **Interviews contextuelles avec les hotes** : En parallele, les fondateurs conduisent des entretiens approfondis avec les hotes dans leur environnement reel (contextual inquiry).
Ils observent comment les hotes preparent leur logement, redigent leurs annonces et gerent les interactions avec les voyageurs.
Ces sessions revelent que les hotes sont fiers de leur logement mais ne savent pas le mettre en valeur en ligne.

3. **Service photography program** : A partir des observations terrain, l'equipe lance un programme de photographie professionnelle gratuite pour les hotes.
Les fondateurs testent differents styles visuels (photos editoriales vs documentaires vs lifestyle) et mesurent l'impact sur les taux de clic et de reservation.
Cette approche combine observation qualitative et validation quantitative.

4. **Journey mapping collaboratif** : L'equipe cartographie l'integralite du parcours utilisateur, de la premiere visite sur le site au retour post-sejour, en identifiant 45 points de contact.
Pour chaque etape, ils documentent les emotions observees (enthousiasme, anxiete, frustration, soulagement) et les moments de verite qui font basculer la decision.
Ce journey map, affiche en grand format dans les bureaux, devient l'outil de reference pour prioriser les ameliorations.

5. **Tests iteratifs des mecanismes de confiance** : L'equipe teste differents mecanismes -- profils verifies, avis bidirectionnels (hote et voyageur), messagerie interne, garantie hote.
Chaque mecanisme est evalue qualitativement (interviews post-reservation) et quantitativement (impact sur la conversion).

### Resultat

- Les annonces avec photos professionnelles generent 2,5 fois plus de reservations, validant l'insight terrain sur l'importance du visuel dans la construction de la confiance.
- Le chiffre d'affaires hebdomadaire passe de 200 a plus de 400 dollars en quelques semaines, puis connait une croissance exponentielle.
- Le systeme d'avis bidirectionnels devient le mecanisme de confiance le plus efficace : les annonces avec plus de 3 avis convertissent 4 fois mieux.
- Le journey mapping permet d'identifier et de resoudre 12 points de friction majeurs dans le parcours de reservation, reduisant le taux d'abandon de 35%.
- La culture de recherche terrain s'ancre dans l'ADN de l'entreprise : "Don't design for your users, design with them" devient un principe fondateur.

### Lecons apprises

- L'immersion ethnographique revele des insights que les donnees quantitatives ne peuvent pas capturer.
Les fondateurs n'auraient jamais identifie le probleme des photos en analysant uniquement les logs du serveur.
- Le contextual inquiry avec les hotes a demontre que les fournisseurs d'un marketplace sont aussi des utilisateurs dont les besoins meritent une recherche dediee.
- La combinaison quali-quanti est essentielle : les observations terrain generent des hypotheses, les tests quantitatifs les valident.
- La recherche utilisateur a un ROI mesurable meme pour une startup en phase de survie : quelques semaines de terrain ont debloquer la croissance de l'entreprise.

---

## Cas 2 : Spotify -- Discover Weekly, ne du diagnostic de la fatigue de decouverte

### Contexte

En 2014, Spotify compte plus de 60 millions d'utilisateurs actifs et un catalogue de plus de 30 millions de titres.
La plateforme a resolu le probleme de l'acces a la musique, mais un nouveau probleme emerge : le paradoxe du choix.
Face a un catalogue immense, les utilisateurs tendent a se replier sur leurs titres favoris et explorent de moins en moins de nouveaux artistes.
Les metriques internes montrent que 80% du temps d'ecoute se concentre sur 20% du catalogue, et que le nombre de titres uniques ecoutes par utilisateur stagne.
L'equipe produit suspecte un probleme de decouverte mais ne dispose pas d'une comprehension fine du phenomene.

### Probleme

L'equipe identifie un symptome -- la stagnation de la diversite d'ecoute -- mais ne comprend pas les causes profondes.
Les hypotheses internes divergent : algorithme insuffisant, interface inadaptee, ou desinteret des utilisateurs pour la nouveaute.
Les solutions de decouverte existantes (radio, playlists editoriales, browse) sont utilisees par moins de 15% des utilisateurs.
Le risque strategique est reel : si les utilisateurs se lassent, ils pourraient quitter la plateforme pour un concurrent.
Le taux de churn des utilisateurs "en boucle" (ecoutant moins de 5 artistes differents par semaine) est 40% superieur a celui des utilisateurs explorant activement.

### Approche

1. **Diary studies sur 3 semaines** : L'equipe recrute 25 utilisateurs de profils varies dans 5 pays.
Pendant 3 semaines, chaque participant documente quotidiennement ses moments d'ecoute : contexte (trajet, travail, sport), etat emotionnel, choix de musique et degre de satisfaction.
Les participants utilisent une application de journaling avec des prompts structures.
L'equipe complete les journaux par des entretiens hebdomadaires de 30 minutes.

2. **Identification de la "fatigue de decouverte"** : L'analyse thematique des 525 entrees de journal revele un pattern recurrent : les utilisateurs veulent decouvrir de la nouvelle musique mais trouvent l'effort cognitif trop eleve.
Parcourir des recommandations, ecouter des extraits, evaluer la compatibilite avec ses gouts -- ce processus actif est percu comme un travail, pas comme un plaisir.
Les participants expriment un desir de "decouverte passive" : recevoir de la bonne musique sans effort.

3. **Entretiens JTBD** : L'equipe conduit 15 entretiens approfondis (60 min) en utilisant le framework Jobs-to-be-Done.
Le job principal identifie : "Quand je suis dans un moment d'ecoute detendu, je veux que de la musique nouvelle mais compatible avec mes gouts arrive sans effort, pour enrichir mon repertoire sans investir d'energie cognitive."
L'anxiete principale : "tomber sur de la musique que je n'aime pas et gacher mon moment d'ecoute."

4. **Prototypage et tests rapides** : L'equipe conçoit 4 concepts et les teste avec 20 utilisateurs : un flux continu de recommandations, une playlist personnalisee hebdomadaire, un mix quotidien, un mode radio ameliore.
La playlist hebdomadaire genere le plus d'enthousiasme : le format fini (30 titres) reduit l'anxiete du choix infini, la cadence hebdomadaire cree de l'anticipation, et le format playlist est familier.

5. **Lancement progressif** : Discover Weekly est lance en beta aupres de 1% des utilisateurs, avec des metriques de suivi : taux d'ecoute, taux de completion, taux de sauvegarde, impact sur la diversite d'ecoute.
L'equipe conduit des interviews post-lancement avec 30 beta-testeurs pour ajuster l'algorithme.

### Resultat

- Discover Weekly atteint 40 millions d'utilisateurs en 10 semaines apres son lancement global.
- Le taux de sauvegarde des titres est de 25% (1 titre sur 4 ajoute a une playlist personnelle).
- La diversite d'ecoute augmente de 30%, avec une exposition a 2,5 fois plus d'artistes differents par mois.
- Le churn des utilisateurs actifs de Discover Weekly est 20% inferieur a celui des non-utilisateurs.
- Plus de 5 milliards de titres sont streames via Discover Weekly la premiere annee, dont 50% d'artistes jamais ecoutes.

### Lecons apprises

- Les diary studies sont la methode ideale pour comprendre les comportements dans la duree.
Un entretien ponctuel n'aurait pas revele le pattern de "fatigue de decouverte" qui n'emerge qu'au fil des jours.
- Le framework JTBD a permis de reformuler le probleme : non pas "decouvrir de la musique" mais "enrichir son repertoire sans effort dans des moments d'ouverture."
- Tester 4 concepts en parallele a permis d'identifier la solution optimale plus rapidement.
La playlist hebdomadaire n'etait pas l'idee initiale la plus populaire dans l'equipe.
- Le nom "discovery fatigue" a ete crucial pour communiquer l'insight en interne.
Un insight bien nomme se diffuse dans l'organisation et influence les decisions au-dela de l'equipe de recherche.

---

## Cas 3 : GOV.UK -- La recherche utilisateur a l'echelle du service public

### Contexte

En 2011, le gouvernement britannique cree le Government Digital Service (GDS) avec la mission de transformer les services publics numeriques.
Les 1 800 sites web du gouvernement sont fragmentes, chaque ministere operant de maniere independante avec ses propres standards, taxonomie et processus.
Les citoyens doivent naviguer entre des dizaines de sites pour des demarches simples (renouveler un passeport, payer ses impots, creer une entreprise).
Les taux de completion des demarches en ligne varient de 15% a 60%, et le cout moyen d'une transaction en ligne est 20 fois inferieur a celui d'une transaction en guichet physique.
Le gouvernement identifie un potentiel d'economie de plusieurs milliards de livres si les citoyens adoptent les services numeriques.

### Probleme

Les sites gouvernementaux sont conçus du point de vue de l'administration, pas du citoyen.
La navigation reflete l'organigramme ministeriel, pas les besoins des utilisateurs.
Le langage est administratif et jargonneux, les formulaires sont longs et complexes.
L'utilisateur doit souvent savoir a quel ministere s'adresser avant de pouvoir trouver l'information.
Les tentatives precedentes (Directgov, BusinessLink) ont echoue car elles aggregeaient les contenus existants sans repenser les parcours.
Le defi est double : creer un site unique (GOV.UK) remplacant 1 800 sites, et installer une culture de la recherche utilisateur dans une administration orientee processus et conformite.

### Approche

1. **Equipe de recherche integree** : Le GDS recrute des UX researchers comme membres a part entiere des equipes produit.
Chaque equipe de service (passeport, impots, permis de conduire) integre un researcher dedie qui participe a toutes les ceremonies agile.
Ce positionnement structurel garantit que la recherche influence les decisions quotidiennes.

2. **Tests d'utilisabilite continus** : Le GDS met en place des tests hebdomadaires dans un lab dedie et en sessions distantes.
Chaque semaine, 5 a 8 citoyens representatifs testent les services en developpement.
Les sessions sont diffusees en direct dans les bureaux du GDS et les ministeres, permettant aux fonctionnaires de voir les difficultes des citoyens.
Principe : aucun service ne passe en production sans test avec des utilisateurs reels, incluant personnes handicapees, agees et a faible litteracie numerique.

3. **Accessibility-first research** : Le GDS fait de l'accessibilite un critere central, pas un ajout tardif.
Les panels incluent systematiquement des utilisateurs de lecteurs d'ecran, personnes avec troubles cognitifs, malvoyantes et a mobilite reduite.
Les tests revelent que les ameliorations d'accessibilite beneficient a tous : simplifier le langage aide les personnes dyslexiques mais aussi les non-natifs anglophones.
Le design guide impose un niveau de lisibilite Flesch-Kincaid de 8e annee maximum.

4. **Content testing et plain language** : L'equipe conduit des tests de comprehension systematiques sur les contenus administratifs.
Les citoyens sont confrontes a des textes reels et doivent expliquer dans leurs propres mots ce qu'ils ont compris.
Les resultats revelent que 40% des contenus gouvernementaux sont incomprehensibles pour le citoyen moyen.
Le GDS etablit des normes de redaction en langage clair et teste chaque contenu avant publication.

5. **Service assessments** : Le GDS cree un processus d'evaluation exigeant la preuve documentee de recherche utilisateur a chaque phase (discovery, alpha, beta, live).
Un service sans preuve de tests avec des utilisateurs reels ne peut pas etre mis en production.
Cette exigence institutionnelle transforme la recherche d'une bonne pratique optionnelle en prerequis obligatoire.

### Resultat

- GOV.UK remplace 1 800 sites en un site unique avec plus de 300 000 pages de contenu.
- Le taux de completion des 25 demarches principales passe de 40% a 82%.
- Les economies sont estimees a 4,1 milliards de livres sur 4 ans.
- Le score de satisfaction utilisateur atteint 84%, un niveau inedit pour un service public numerique.
- Le GDS forme plus de 400 researchers et etablit la recherche utilisateur comme discipline reconnue dans la fonction publique britannique.
- Le Government Service Design Manual est adopte comme reference par plus de 15 gouvernements dans le monde.

### Lecons apprises

- Integrer les researchers dans les equipes produit est le facteur structurel le plus important.
Un researcher dedie construit une relation de confiance et une connaissance du domaine que les interventions ponctuelles ne permettent pas.
- La diffusion video des sessions de test est l'outil de conviction le plus puissant.
Voir un citoyen echouer a remplir un formulaire change les mentalites plus efficacement que n'importe quel rapport.
Le GDS recommande un minimum de 2 "exposure hours" par mois pour chaque membre d'equipe.
- L'accessibilite n'est pas un cas limite : concevoir pour les cas extremes ameliore l'experience pour tous (curb cut effect).
- Rendre la recherche obligatoire par des mecanismes institutionnels (service assessments) est plus efficace que de compter sur la bonne volonte.
La contrainte cree l'habitude, et l'habitude cree la culture.

---

## Cas 4 : Duolingo -- La gamification fondee sur la recherche comportementale

### Contexte

Duolingo est lance en 2012 avec l'ambition de rendre l'apprentissage des langues gratuit et accessible.
L'application connait une croissance rapide (plus de 300 millions de telecharges en 2019), mais l'equipe fait face au defi majeur des applications educatives : la retention.
Apprendre une langue est un processus long (6 a 12 mois), mais la majorite des utilisateurs abandonnent dans les premieres semaines.
L'equipe dispose d'une masse de donnees comportementales considerable -- chaque interaction, chaque erreur, chaque session est tracee -- mais manque de comprehension qualitative des mecanismes psychologiques sous-jacents.

### Probleme

Le taux de retention a J14 est de 12% : 88% des nouveaux utilisateurs arretent dans les deux premieres semaines.
A J30, il tombe a 5%.
L'abandon se concentre sur deux periodes critiques : J2-J3 (apres l'enthousiasme initial) et J10-J14 (quand la difficulte augmente).
Les notifications push et emails de rappel ont un impact qui s'erode avec le temps.
Les utilisateurs qui desactivent les notifications churnernt 2 fois plus vite, mais les forcer degrade la satisfaction.
Le defi : trouver des mecanismes d'engagement intrinseque plutot qu'extrinseque.

### Approche

1. **Interviews de churn segmentees** : L'equipe conduit 60 entretiens segmentes en 3 groupes : utilisateurs actifs (30+ jours), churners J7-J14 et churners J14-J30.
Les entretiens utilisent la technique du switch interview (JTBD) pour reconstituer le moment exact de la decision d'arreter ou de continuer.
Les utilisateurs actifs mentionnent un sentiment de progression visible et un engagement social.
Les churners mentionnent un plateau d'apprentissage et une absence de recompense immediate.

2. **Analyse comportementale granulaire** : L'equipe data analyse les patterns de 50 000 utilisateurs sur 90 jours, croisant donnees d'usage et donnees de retention.
Predicteurs identifies : les utilisateurs completant 3+ sessions dans les 48 premieres heures ont un taux de retention J30 de 22% (vs 3% pour une seule session).
Les utilisateurs maintenant un streak de 7 jours consecutifs ont un taux de retention J90 de 45%.

3. **A/B testing systematique de la gamification** : L'equipe teste 23 variantes de mecanismes sur 12 mois, chacune structuree autour d'une hypothese issue de la recherche.
Le "streak freeze" : preserver sa serie en cas d'absence d'un jour pour reduire l'anxiete de perte.
Le systeme de ligues : competition sociale entre pairs pour augmenter l'engagement hebdomadaire.
Les coeurs/vies limitees : la rarete des tentatives pour augmenter l'attention.
Chaque test dimensionne pour detecter un effet de 2% sur la retention J14.

4. **Diary studies de 4 semaines** : 20 nouveaux utilisateurs documentent quotidiennement leur motivation, humeur avant/apres session, et facteurs externes influencant leur decision de pratiquer.
Les journaux revelent un cycle motivationnel previsible : enthousiasme (J1-J3), premier creux (J4-J7), deuxieme souffle lie au streak (J7-J14), deuxieme creux (J14-J21), puis stabilisation ou abandon.
Ces insights permettent de chronometrer precisement les interventions de retention.

5. **Tests d'utilisabilite du onboarding** : 30 nouveaux utilisateurs testent le processus d'inscription et les premieres lecons (10 tests par variante).
Le placement test est un moment critique : trop facile, il ennuie les faux debutants ; trop difficile, il decourage les vrais debutants.
La version optimale propose un mini-objectif atteignable en 5 minutes qui genere un sentiment immediat de competence.

### Resultat

- La retention J14 passe de 12% a 21% sur 18 mois (+75% d'amelioration relative).
- Le systeme de streaks devient le mecanisme le plus efficace : retention 3 fois superieure pour les utilisateurs avec streak actif.
Le "streak freeze" reduit le churn post-interruption de 40%.
- Le systeme de ligues augmente les sessions hebdomadaires de 17% parmi les utilisateurs competitifs (35% de la base).
- L'optimisation du onboarding augmente le taux de completion de la premiere lecon de 68% a 89% et le retour a J2 de 42% a 55%.
- Les revenus augmentent de 45% en 18 mois, portes par la base d'utilisateurs actifs et le taux de conversion premium.

### Lecons apprises

- Combiner recherche qualitative (interviews, diary studies) et quantitative (cohortes, A/B testing) produit des insights plus robustes que l'une ou l'autre isolement.
Les interviews revelent le "pourquoi", les donnees revelent le "quoi" et le "combien."
- Le switch interview est particulierement efficace pour comprendre le churn : reconstituer le moment precis de la decision d'arreter revele les declencheurs que les questions generales ne capturent pas.
- Les diary studies cartographient les cycles motivationnels et permettent de chronometrer les interventions.
Sans cette comprehension temporelle, les interventions risquent d'arriver trop tot ou trop tard.
- L'A/B testing a grande echelle exige une discipline rigoureuse : hypothese explicite, dimensionnement de l'echantillon, criteres predetermines, et duree suffisante pour capturer les effets a long terme.

---

## Cas 5 : Intercom -- Le framework Jobs-to-be-Done pour repenser les categories produit

### Contexte

Intercom est fonde en 2011 comme plateforme de messagerie client pour les entreprises.
En 2014, l'entreprise a leve 23 millions de dollars et compte plusieurs milliers de clients.
Le produit a evolue organiquement : a la messagerie initiale se sont ajoutes le support client (inbox partagee), l'onboarding (messages cibles), l'engagement (notifications, emails automatises) et le feedback.
L'equipe produit, dirigee par Des Traynor (co-fondateur) et Paul Adams (VP Product), fait face a une complexite croissante : le produit fait trop de choses, les clients ne comprennent pas ce qu'Intercom peut faire pour eux, et les equipes internes ne savent plus comment prioriser.

### Probleme

La segmentation produit est basee sur les fonctionnalites (Acquire, Engage, Support), mais cette categorisation ne correspond pas a la maniere dont les clients pensent a leurs besoins.
Les prospects demandent "Est-ce qu'Intercom fait du support ?" ou "Est-ce qu'Intercom remplace mon outil d'emailing ?" -- des questions cadrees par les categories concurrentes, pas par leurs problemes reels.
Le taux de conversion des trials est de 8%.
L'analyse des churners montre que 35% n'ont jamais compris quel probleme Intercom resolvait pour eux.
Le positionnement, le packaging et la roadmap sont construits autour des fonctionnalites ("ce que nous avons construit") plutot que des problemes clients ("ce qu'ils essaient d'accomplir").

### Approche

1. **Formation au framework JTBD** : L'equipe etudie les travaux de Clayton Christensen et Bob Moesta.
Des Traynor et Paul Adams organisent des ateliers pour adapter le framework au SaaS B2B.
L'hypothese centrale : les clients n'achetent pas un produit pour ses fonctionnalites mais pour le progres qu'il permet d'accomplir.
La question strategique est reformulee : "Quels jobs nos clients essaient-ils d'accomplir, et comment les aider mieux que les alternatives ?"

2. **Switch interviews avec 85 clients** : L'equipe conduit 85 entretiens (60-90 min) en utilisant la technique du switch interview de Bob Moesta.
Chaque entretien reconstitue le moment ou le client a decide d'adopter Intercom : situation declenchante, alternatives evaluees, anxietes, resultat espere.
Trois segments : nouveaux clients (< 3 mois), clients etablis (6-18 mois), anciens clients ayant churne.
Chaque entretien est enregistre, transcrit et analyse thematiquement.

3. **Identification des jobs et mapping des forces** : L'analyse revele 5 jobs principaux :
(a) convertir les visiteurs en utilisateurs qualifies,
(b) aider les nouveaux utilisateurs a atteindre leur premier succes rapidement,
(c) resoudre les problemes des clients existants efficacement,
(d) maintenir l'engagement des utilisateurs inactifs,
(e) collecter et agir sur le feedback produit.
L'equipe cartographie les forces du switch pour chaque job : push (frustrations actuelles), pull (attraits d'Intercom), anxietes (peur du changement) et habitudes (familiarite avec les outils existants).

4. **Reorganisation du produit autour des jobs** : La suite Intercom est reorganisee en 4 produits correspondant aux jobs : Messages (onboarding/engagement), Inbox (support conversationnel), Articles (self-service), et un produit transversal de donnees client.
Chaque produit est positionne par le job qu'il accomplit, pas par ses fonctionnalites.
Le site web, le pricing, les scripts de vente et les parcours de onboarding sont realignes.
La roadmap est repriorisee par contribution aux jobs, pas par faisabilite technique ou demande brute.

5. **Validation par tests de proposition de valeur** : L'equipe teste le nouveau positionnement avec 40 prospects naifs.
Les participants sont exposes a l'ancienne page (centree fonctionnalites) puis a la nouvelle (centree jobs), et doivent expliquer ce que fait Intercom.
La comprehension du produit passe de 22% a 64%.
Des tests de premier clic sur les parcours de trial verifient que les nouveaux utilisateurs trouvent rapidement le job qu'ils veulent accomplir.

### Resultat

- Le taux de conversion des trials passe de 8% a 14,5% (+81%) dans les 6 mois suivant le repositionnement.
- Le churn a 90 jours diminue de 18%, car les clients activent les bonnes fonctionnalites des l'onboarding.
- La valeur moyenne des contrats (ACV) augmente de 30%, le positionnement par jobs revelant les opportunites d'upsell naturelles.
- La roadmap gagne en clarte : les demandes sont evaluees par contribution aux 5 jobs, reduisant les debats subjectifs en comite produit.
- L'approche JTBD est documentee et partagee publiquement par Des Traynor et Paul Adams, devenant une reference dans la communaute produit.

### Lecons apprises

- Le framework JTBD transforme la maniere de penser le produit : passer de "quelles fonctionnalites construire" a "quels jobs accomplir" change les priorites, le positionnement et l'experience.
C'est un outil strategique autant qu'un outil de recherche.
- Les switch interviews sont la methode la plus efficace pour identifier les jobs.
Reconstituer le parcours de decision revele les motivations profondes et les moments de verite que les questionnaires de satisfaction ne capturent pas.
- 85 entretiens representent un investissement significatif, mais le ROI est strategique : les insights ont restructure le positionnement, le packaging, la roadmap et les processus de vente.
Un tel investissement se justifie pour des enjeux structurels, pas tactiques.
- La validation avec des prospects naifs est essentielle.
Les clients existants sont biaises par leur experience ; seuls les prospects naifs indiquent si le message est comprehensible pour un nouveau venu.
- Le JTBD n'est pas un exercice ponctuel : les jobs evoluent avec le marche, et la cartographie doit etre revisitee annuellement.
