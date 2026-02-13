# Études de cas — Commercial / Ventes

## Cas 1 : Mise en place d'un processus de vente structuré B2B

### Contexte
CyberGuard, éditeur de solutions de cybersécurité B2B (60 personnes), opère sur le marché français des PME et ETI avec une offre de détection et réponse aux menaces (EDR/XDR). L'entreprise, fondée il y a 5 ans par d'anciens ingénieurs de l'ANSSI, dispose d'une technologie reconnue mais peine à convertir cette excellence technique en performance commerciale. L'équipe de 8 commerciaux, recrutés progressivement sans cadre unifié, opère chacun avec sa propre méthode de qualification, ses propres outils de suivi (entre Excel, Notion et CRM Salesforce utilisé de manière disparate) et ses propres critères pour avancer un deal dans le pipeline. Le VP Sales, recruté 6 mois plus tôt, est mandaté pour structurer la machine commerciale.

### Problème
Le taux de closing est de 12% (vs 25% benchmark sectoriel cybersécurité B2B), signalant un problème systémique de qualification des opportunités. Le cycle de vente moyen s'étire sur 120 jours, deux fois plus long que les concurrents directs, en raison de l'absence de mutual action plans et de la difficulté à engager les décideurs économiques. Les prévisions de ventes ne sont fiables qu'à 40%, rendant impossible toute planification fiable du recrutement ou des investissements marketing. Les commerciaux passent 60% de leur temps sur des deals qui n'aboutissent jamais, faute de critères objectifs de disqualification. Le pipeline est gonflé artificiellement (3,2M€ affichés pour un objectif de 800K€ trimestriel), créant une illusion de volume qui masque la faiblesse du taux de conversion.

### Approche
1. **Audit du pipeline** : Analyse rétrospective de 200 deals (gagnés et perdus) sur les 18 derniers mois pour identifier les facteurs prédictifs de succès. L'audit a révélé que les deals gagnés avaient systématiquement un champion interne identifié, un accès au décideur économique avant la démo, et un événement déclencheur documenté (audit de sécurité, incident, réglementation). Cette analyse a fourni la base empirique pour définir les critères de qualification.
2. **Déploiement MEDDIC** : Formation intensive de l'équipe à la qualification MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion) sur 3 jours, avec des critères de passage explicites entre chaque étape du pipeline. Un score MEDDIC minimum de 4/6 est requis pour qu'un deal avance au stade "Proposal". Les commerciaux ont d'abord résisté au framework, le jugeant trop rigide, avant d'en constater les bénéfices sur leurs propres deals.
3. **Sales playbook** : Création d'un playbook structuré couvrant l'intégralité du cycle — script de discovery call avec 15 questions calibrées, guide de démo personnalisée par persona (RSSI, DSI, DG), template de business case chiffré (coût d'un incident vs coût de la solution), et mutual action plan co-construit avec le prospect. Le playbook a été développé en collaboration avec les 2 top performers de l'équipe pour capitaliser sur leurs bonnes pratiques.
4. **Weekly pipeline review** : Revue hebdomadaire du pipeline de 90 minutes avec scoring systématique MEDDIC de chaque deal, et discipline stricte de "kill" des deals non qualifiés (score MEDDIC < 3/6 depuis plus de 30 jours). Le VP Sales coach chaque commercial sur 2-3 deals prioritaires, en se concentrant sur les actions concrètes à mener dans la semaine. Cette discipline a réduit le pipeline de 3,2M€ à 1,8M€ en volume, mais augmenté le taux de conversion de manière spectaculaire.
5. **Outillage CRM** : Refonte complète des étapes Salesforce alignées sur MEDDIC, avec des champs obligatoires pour chaque critère de qualification. Dashboards de performance en temps réel (pipeline velocity, conversion par étape, forecast weighted), accessibles à toute l'équipe pour créer une culture de transparence et de saine émulation.

### Résultat
- Taux de closing passé de 12% à 28% en 6 mois, dépassant le benchmark sectoriel de 25%
- Cycle de vente réduit de 120 à 75 jours, grâce aux mutual action plans et à l'engagement plus précoce des décideurs économiques
- Forecast accuracy passée de 40% à 82%, permettant une planification fiable des recrutements et investissements
- Revenu par commercial augmenté de 45%, sans recrutement supplémentaire
- Pipeline "propre" réduit en volume de 44% mais produisant 2,3× plus de revenus qu'avant la transformation
- Onboarding des nouveaux commerciaux réduit de 6 à 3 mois grâce au playbook structuré

### Leçons apprises
- La discipline de disqualification (savoir dire non) est aussi importante que la qualification — les meilleurs commerciaux sont ceux qui tuent les mauvais deals le plus tôt, libérant du temps pour les opportunités à fort potentiel.
- Un pipeline plus petit mais mieux qualifié produit plus de revenus qu'un pipeline gonflé — la vanity metric du volume de pipeline est le piège le plus fréquent des équipes commerciales B2B.
- Le coaching hebdomadaire (pas mensuel) est le levier le plus efficace pour changer les comportements — la fréquence crée l'habitude, et le feedback en temps réel est 5× plus impactant que la revue mensuelle rétrospective.
- L'implication des top performers dans la création du playbook est essentielle pour l'adoption : un processus imposé top-down sera contourné, un processus co-construit sera approprié.

---

## Cas 2 : Transformation RevOps dans un scale-up

### Contexte
InsightPlatform, scale-up data analytics (120 personnes, 8M€ ARR), développe une plateforme de business intelligence en self-service pour les équipes marketing des ETI et grands comptes. Après une série A réussie de 12M€ il y a 18 mois, l'entreprise est en phase d'accélération commerciale avec un objectif de 20M€ d'ARR pour la série B. L'organisation commerciale est structurée en 3 équipes distinctes — marketing (12 personnes, acquisition), sales (15 commerciaux, conversion) et customer success (8 CSM, rétention/expansion) — chacune avec son propre manager, son propre outil principal et ses propres indicateurs de performance. Le désalignement chronique entre ces trois fonctions est identifié par le board comme le principal frein à l'accélération.

### Problème
Le handoff marketing vers sales perd 35% des leads (pas de suivi dans les 24h, leads transférés sans qualification suffisante, routing manuel avec des erreurs d'assignation), ce qui génère de la frustration côté marketing ("on génère des leads que personne ne traite") et côté sales ("les leads marketing sont de mauvaise qualité"). Le handoff sales vers CS provoque 15% de churn dans les 3 premiers mois, dû à des promesses commerciales non documentées et un onboarding démarrant trop tard. Les trois équipes utilisent des définitions différentes des métriques clés : marketing compte un MQL dès le téléchargement d'un contenu, sales exige un échange téléphonique, et CS mesure l'activation différemment du produit. Le blame game entre équipes consomme une énergie considérable lors des comités mensuels, sans jamais résoudre les problèmes structurels.

### Approche
1. **Création d'une fonction RevOps** : Recrutement d'un Head of RevOps expérimenté (ex-HubSpot), rattaché au COO avec un mandat transverse explicite sur marketing, sales et CS. L'équipe RevOps de 3 personnes (Head + 1 ops analyst + 1 data engineer) a été positionnée comme un service partagé, pas comme une fonction de contrôle, pour éviter les réactions défensives des équipes. Le mandat a été validé en CODIR avec des OKR spécifiques sur l'alignement inter-équipes.
2. **Unified data model** : Définition commune et documentée de chaque métrique clé (MQL : score ≥ 50 + intent signal, SQL : BANT qualifié par un SDR, PQL : activation produit ≥ 3 features, activation : 2 dashboards créés en 14 jours, health score : composite de 5 signaux d'usage). Toutes les métriques ont été unifiées dans un seul dashboard HubSpot accessible à tous, éliminant les versions contradictoires qui alimentaient les conflits. Ce travail de définition, apparemment simple, a pris 6 semaines de négociation entre les équipes.
3. **SLA inter-équipes** : Formalisation de SLA réciproques — Marketing s'engage sur un volume mensuel de SQL (pas de MQL), Sales sur un temps de traitement < 4h et un taux de conversion SQL-to-opportunity de 30%, CS sur un NRR > 110% et un CSAT onboarding > 4/5. Les SLA sont revus mensuellement avec un système de bonus collectif lié à leur respect, créant une responsabilité mutuelle plutôt qu'un blame game unidirectionnel.
4. **Automatisation des handoffs** : Routing automatique des leads qualifiés vers le commercial le plus pertinent (par segment, géographie et charge de travail), séquences de nurturing automatisées pour les leads non prêts (score < 50), et playbook de handoff sales vers CS incluant un document de transfert standardisé (promesses commerciales, configuration vendue, contacts clés, risques identifiés). Le handoff sales-CS inclut désormais un appel tripartite systématique (commercial + CSM + client) pour assurer la continuité.

### Résultat
- Taux de suivi des leads dans les 24h passé de 65% à 98%, grâce au routing automatique et aux alertes temps réel
- Churn premiers 3 mois réduit de 15% à 4%, grâce au handoff structuré et à l'onboarding anticipé
- NRR passé de 95% à 112%, porté par une meilleure collaboration sales-CS sur l'expansion
- Pipeline velocity améliorée de 40%, grâce à l'élimination des frictions inter-équipes
- Temps passé en blame game lors des comités réduit de 60% à 10% — les SLA objectivent les discussions
- CAC payback réduit de 14 à 9 mois, le RevOps ayant identifié et éliminé 3 sources de déperdition dans le funnel

### Leçons apprises
- RevOps n'est pas un rôle IT ou analytics — c'est un rôle stratégique qui nécessite un mandat explicite du CODIR et un rattachement au C-level. Un RevOps enterré dans l'IT n'aura jamais la légitimité pour aligner les équipes.
- Les SLA inter-équipes créent de la responsabilité mutuelle et réduisent le blame game — à condition d'être réciproques. Un SLA unilatéral (marketing doit livrer X leads) sans contrepartie (sales doit les traiter en Y heures) est voué à l'échec.
- L'unification des définitions métriques est le premier quick win — sans langage commun, pas d'alignement. Ce travail est souvent perçu comme trivial mais c'est la fondation sur laquelle tout le reste repose.
- Le bonus collectif lié aux SLA inter-équipes a transformé la dynamique : les équipes passent d'une logique de "c'est leur faute" à une logique de "comment on peut s'aider mutuellement".

---

## Cas 3 : Stratégie de Social Selling B2B

### Contexte
ConseilPlus, cabinet de conseil en transformation digitale (40 consultants), est reconnu pour l'expertise de ses consultants seniors dans l'accompagnement des ETI et grands comptes dans leurs projets de digitalisation. Le cabinet, fondé il y a 12 ans par 3 associés issus de grands cabinets, a bâti sa réputation sur la qualité de ses livrables et le bouche-à-oreille de ses clients satisfaits. Le développement commercial dépend quasi exclusivement du réseau personnel des 3 associés et des recommandations clients, un modèle qui a bien fonctionné pendant une décennie mais montre ses limites. Le carnet de commandes baisse de 20% sur les 12 derniers mois, et les méthodes traditionnelles (networking en événements, recommandations, appels d'offres publics) ne suffisent plus à compenser le non-renouvellement naturel du portefeuille clients.

### Problème
Les 15 consultants seniors, bien qu'experts reconnus dans leur domaine, n'ont aucun réflexe commercial et considèrent le développement business comme "le travail des associés". Le taux de réponse aux cold emails est de 2%, rendant cette approche non viable à l'échelle. Le cabinet n'a aucune présence digitale malgré une expertise reconnue dans le milieu professionnel : les profils LinkedIn des consultants sont incomplets, aucun contenu n'est publié, et le site web n'a pas été mis à jour depuis 3 ans. Pendant ce temps, des concurrents plus jeunes mais plus visibles en ligne captent des prospects que ConseilPlus aurait naturellement attirés par le passé. Les associés réalisent que l'expertise non visible est une expertise perdue dans un monde où les décideurs font leur benchmark en ligne avant de contacter un cabinet.

### Approche
1. **Personal branding des experts** : Programme de formation LinkedIn sur 8 semaines pour 15 consultants seniors, couvrant l'optimisation de profils (photo professionnelle, headline orientée valeur, section "À propos" narrative), la définition d'une stratégie de contenu individuelle alignée sur l'expertise de chacun, et l'installation d'une routine de publication (15 minutes/jour). Chaque consultant a défini 3 thématiques d'expertise et un angle éditorial différenciant. Un photographe professionnel a été mobilisé pour les photos de profil.
2. **Content factory** : Mise en place d'un flux de contenus expert alimenté par les missions en cours (anonymisées et validées par les clients) — retours d'expérience terrain, méthodologies propriétaires, analyses de tendances sectorielles. Un rédacteur freelance a été recruté pour transformer les notes techniques des consultants en posts LinkedIn engageants. La production cible est de 3 posts par consultant par semaine, répartis entre posts courts (insights), posts longs (méthodologies) et articles de fond mensuels. Un calendrier éditorial partagé évite les doublons et assure une couverture thématique équilibrée.
3. **Social selling process** : Processus structuré en 4 étapes — engagement régulier sur les posts des prospects cibles (commentaires à valeur ajoutée, pas de "bravo" vides), connexion personnalisée avec un message contextuel, partage de contenu à valeur adapté aux enjeux identifiés du prospect, puis transition naturelle vers un échange (café virtuel, déjeuner). Le processus interdit explicitement le pitch direct en message privé. Chaque consultant a défini une liste de 50 prospects cibles mis à jour mensuellement.
4. **Mesure et coaching** : SSI (Social Selling Index) LinkedIn suivi mensuellement comme KPI individuel, coaching individuel bi-mensuel avec un expert social selling externe pendant 6 mois. Les sessions de coaching incluent la revue des performances (impressions, engagement, connexions), le feedback sur les contenus publiés, et l'ajustement de la stratégie. Un channel Slack dédié permet aux consultants de partager leurs succès et de s'entraider sur la création de contenu.

### Résultat
- SSI moyen de l'équipe passé de 35 à 68 en 6 mois (top 5% des utilisateurs LinkedIn dans le secteur conseil)
- 45 rendez-vous qualifiés générés via LinkedIn en 6 mois (vs 0 avant), avec un taux de conversion en proposition de 40%
- 8 nouvelles missions signées directement attribuées au social selling (520K€ de CA), avec un CAC quasi nul
- Notoriété : +300% d'impressions mensuelles et 2 invitations à des conférences sectorielles majeures (dont une keynote)
- Effet secondaire inattendu : 3 candidatures spontanées de consultants seniors attirés par la visibilité du cabinet
- Pipeline commercial reconstitué à 6 mois de visibilité, contre 2 mois avant le programme

### Leçons apprises
- Le social selling n'est pas de la vente sur LinkedIn — c'est du relationship building à échelle. Les consultants qui ont le mieux performé sont ceux qui ont adopté une posture de partage d'expertise plutôt que de prospection déguisée.
- La régularité (3 posts/semaine) compte plus que la perfection du contenu — un post imparfait publié vaut mieux qu'un post parfait jamais finalisé. L'algorithme LinkedIn récompense la constance.
- Les consultants les plus réticents au début deviennent souvent les meilleurs ambassadeurs une fois qu'ils voient les résultats — le premier rendez-vous obtenu via LinkedIn est le déclic. Commencer avec des volontaires enthousiastes crée un effet d'entraînement naturel.
- Le rédacteur freelance est un investissement clé : transformer l'expertise technique en contenu engageant est un métier à part entière, et les consultants ne peuvent pas y consacrer le temps nécessaire en plus de leurs missions.
