# Études de cas — Data Literacy & Visualisation

## Cas 1 : Programme de démocratisation des données dans un grand groupe de distribution

### Contexte
Groupe Beauval Distribution, réseau de 320 magasins de bricolage et jardinage en France, 9 500 collaborateurs, 1,8 milliard d'EUR de chiffre d'affaires. Les données de vente, stock et fidélité sont centralisées dans un entrepôt de données, mais seuls 12 analystes au siège produisent les rapports. Les directeurs de magasin reçoivent des tableaux Excel hebdomadaires de 15 onglets qu'ils consultent rarement.

### Problème
Seulement 8 % des directeurs de magasin déclarent utiliser les données pour leurs décisions d'assortiment et de pricing local. Les demandes d'analyses ad hoc adressées à l'équipe data centrale ont un délai de traitement moyen de 11 jours, créant un goulet d'étranglement permanent. Le taux d'erreur dans les décisions de réapprovisionnement local atteint 23 %, générant 4,2 millions d'EUR de surstock annuel.

### Approche
1. **Diagnostic de maturité data** : Enquête auprès de 280 directeurs de magasin et 45 responsables régionaux pour évaluer le niveau de compréhension des indicateurs clés (marge brute, rotation de stock, taux de démarque) — résultat : 62 % ne maîtrisent pas le calcul de la marge contributive.
2. **Programme de formation par niveaux** : Déploiement d'un parcours en 3 niveaux (fondamentaux data — 8 h, analyse opérationnelle — 12 h, data champion — 20 h) avec des cas pratiques issus de données réelles anonymisées du réseau, dispensé en présentiel par vagues de 40 personnes.
3. **Portail data self-service** : Création d'un portail Tableau avec 8 dashboards interactifs conçus avec les directeurs de magasin (performance magasin, analyse panier, suivi promo, benchmark régional), intégrant un glossaire métier de 85 indicateurs et des info-bulles explicatives sur chaque visualisation.
4. **Réseau de data champions** : Identification et formation approfondie de 32 data champions (1 par région), chargés d'accompagner leurs pairs, de remonter les besoins analytiques et d'animer des ateliers mensuels de lecture de données en réunion régionale.

### Résultat
- Taux d'utilisation des données pour les décisions locales passé de 8 % à 67 % en 10 mois
- Délai moyen des demandes ad hoc réduit de 11 jours à 2 jours (les directeurs trouvent 75 % des réponses en self-service)
- Surstock réduit de 4,2 millions d'EUR à 1,9 million d'EUR (baisse de 55 %)
- 289 directeurs formés sur 320 (taux de complétion de 90 %), dont 32 certifiés data champions

### Leçons apprises
- La formation seule ne suffit pas : sans un outil self-service ergonomique, les directeurs retombent dans l'habitude de demander des rapports au siège
- Les data champions issus du terrain ont un impact bien supérieur à des formateurs externes car ils parlent le langage métier et connaissent les réalités opérationnelles
- Le glossaire métier partagé est un investissement modeste (3 semaines de travail) mais un accélérateur majeur d'adoption car il élimine les ambiguïtés d'interprétation

---

## Cas 2 : Refonte des dashboards de direction pour une entreprise SaaS — data storytelling

### Contexte
Cloudeo, éditeur SaaS français de solutions de gestion locative, 180 collaborateurs, 22 millions d'EUR d'ARR, en phase de scale-up avec une levée de série B de 35 millions d'EUR. Le comité de direction (8 membres) reçoit chaque lundi un deck PowerPoint de 42 slides produit manuellement par le FP&A, compilant des données issues de Salesforce, Stripe, Mixpanel et du SIRH. Chaque C-level interprète les chiffres différemment.

### Problème
La préparation du deck hebdomadaire consomme 2,5 jours-homme par semaine. Les réunions de direction de 2 heures se transforment en débats sur la fiabilité des chiffres plutôt qu'en prises de décision. Le board a identifié 3 incohérences majeures entre les métriques présentées aux investisseurs et les données internes lors du dernier conseil d'administration, fragilisant la crédibilité du management.

### Approche
1. **Atelier d'alignement sur les métriques clés** : Animation de 3 sessions de 2 heures avec le CODIR pour définir collectivement les 15 KPIs stratégiques (MRR, NDR, CAC, LTV, burn rate, NPS, etc.), leur formule de calcul exacte, leur source de vérité unique et les seuils d'alerte associés.
2. **Architecture narrative des dashboards** : Conception de 3 dashboards selon les principes du data storytelling — un dashboard "santé business" en page d'accueil avec les 5 signaux vitaux, un dashboard "croissance" structuré comme un funnel (acquisition, activation, rétention, expansion) et un dashboard "efficience opérationnelle" (burn multiple, magic number, règle des 40).
3. **Design visuel et hiérarchie informationnelle** : Application des principes de Tufte et Few : suppression du chartjunk, usage de sparklines pour les tendances, code couleur sémantique (vert/orange/rouge) basé sur les seuils définis, annotations contextuelles automatiques sur les variations significatives (> 2 écarts-types).
4. **Rituel data-driven et formation CODIR** : Formation du CODIR à la lecture des dashboards (3 h), instauration d'un rituel de 30 minutes le lundi matin (10 min lecture individuelle, 20 min discussion des anomalies et décisions), suppression du deck PowerPoint manuel.

### Résultat
- Temps de préparation du reporting direction réduit de 2,5 jours à 2 heures par semaine (automatisation à 92 %)
- Durée des réunions de direction réduite de 2 h à 45 min avec un nombre de décisions actionnables doublé (de 3 à 6 par réunion en moyenne)
- Zéro incohérence de métriques détectée sur les 4 trimestres suivants vis-à-vis du board
- NPS interne du CODIR sur la qualité du reporting passé de 12 à 78

### Leçons apprises
- Le principal problème n'est jamais l'outil de visualisation mais l'absence de consensus sur la définition des métriques — l'alignement en amont est un prérequis non négociable
- Un dashboard efficace raconte une histoire avec un fil narratif clair ; un empilement de graphiques sans structure génère plus de confusion que de clarté
- La suppression du deck manuel n'est acceptable par les parties prenantes que si le dashboard automatisé offre une expérience de lecture supérieure, ce qui exige un investissement significatif en design

---

## Cas 3 : Programme de pensée statistique pour réduire la mauvaise interprétation des données dans un groupe pharmaceutique

### Contexte
Laboratoires Vauclaire, groupe pharmaceutique européen de 4 200 collaborateurs, spécialisé en oncologie et immunologie, avec un budget R&D annuel de 280 millions d'EUR. Les décisions critiques (avancement de molécules en phase clinique, allocation budgétaire, stratégie de lancement) s'appuient sur des analyses statistiques complexes, mais les comités décisionnels sont composés majoritairement de profils non-statisticiens.

### Problème
Un audit interne révèle que 41 % des présentations au comité de développement contiennent au moins une interprétation statistique erronée (confusion corrélation/causalité, mauvaise lecture des intervalles de confiance, biais de survivant). Deux décisions de go/no-go sur des molécules en phase II ont été influencées par des erreurs d'interprétation de p-values, entraînant un surinvestissement estimé à 12 millions d'EUR sur un programme finalement abandonné.

### Approche
1. **Cartographie des biais décisionnels** : Analyse rétrospective de 60 présentations de comité de développement sur 18 mois, identification et classification de 147 erreurs d'interprétation statistique regroupées en 8 catégories (confusion p-value/taille d'effet, extrapolation abusive de sous-groupes, négligence des intervalles de confiance, etc.).
2. **Programme de formation "Statistical Thinking"** : Développement d'un programme de 24 heures sur 8 semaines pour les 85 membres des comités décisionnels, centré sur l'intuition statistique plutôt que le calcul — utilisation de simulations interactives, de cas réels anonymisés issus de l'historique du laboratoire et d'exercices de pré-mortem statistique.
3. **Checklists et garde-fous décisionnels** : Création d'une checklist de 12 points de vérification statistique obligatoire pour toute présentation en comité (taille d'échantillon, puissance statistique, intervalles de confiance affichés, distinction corrélation/causalité, analyse de sensibilité), intégrée au template officiel de présentation.
4. **Binôme statisticien/décideur** : Instauration d'un système de revue croisée où chaque présentation est relue par un biostatisticien référent qui produit un avis d'une page résumant les forces, limites et points de vigilance de l'analyse, distribué aux membres du comité 48 h avant la réunion.

### Résultat
- Taux de présentations contenant des erreurs statistiques réduit de 41 % à 9 % en 12 mois
- Temps de décision moyen en comité réduit de 3,2 semaines à 1,8 semaine grâce à des discussions mieux cadrées
- Aucune décision de go/no-go contestée pour raison méthodologique sur les 18 mois suivant le déploiement (vs. 4 contestations les 18 mois précédents)
- Score moyen au test de littératie statistique passé de 47/100 à 79/100 pour les participants au programme

### Leçons apprises
- Les erreurs d'interprétation statistique les plus coûteuses ne viennent pas d'un manque de compétence technique mais d'un excès de confiance dans des résultats présentés sans contexte méthodologique
- Les checklists obligatoires sont plus efficaces que la formation seule car elles créent un filet de sécurité systématique indépendant du niveau individuel
- Le format "avis du biostatisticien" transforme le rôle du statisticien de producteur de chiffres en conseiller de décision, ce qui augmente son impact et sa légitimité dans l'organisation
