# Études de cas — BI, Reporting & Data Governance

## Cas 1 : Mise en place d'un framework de gouvernance des données avec data catalog et monitoring qualité

### Contexte
Assurances Atlantique, compagnie d'assurance mutualiste couvrant 1,6 million d'assurés en IARD et prévoyance, 3 100 collaborateurs, présente dans 14 départements du Grand Ouest. L'entreprise exploite 23 applications métier alimentant un data warehouse de 4,8 To. Aucune politique formelle de gouvernance des données n'existe ; les définitions de KPIs varient selon les directions.

### Problème
Le régulateur (ACPR) a émis 3 recommandations lors du dernier contrôle sur la traçabilité des données utilisées dans les calculs de solvabilité. En interne, 34 % des rapports réglementaires nécessitent des corrections manuelles avant soumission. Les équipes actuarielles estiment passer 6 heures par semaine à vérifier la cohérence des données entre systèmes, et 5 définitions concurrentes du "taux de sinistralité" coexistent dans l'organisation.

### Approche
1. **Organisation de la gouvernance** : Nomination d'un Chief Data Officer rattaché à la direction générale, création d'un comité data governance mensuel réunissant les 7 directeurs métier, désignation de 14 data owners (un par domaine métier) et de 28 data stewards responsables de la qualité opérationnelle au quotidien.
2. **Déploiement du data catalog** : Implémentation d'un data catalog sur DataHub recensant les 1 240 tables du data warehouse, avec documentation collaborative des métadonnées métier, lignage technique automatisé depuis les pipelines dbt, et glossaire métier unifié de 320 termes validés par les data owners.
3. **Framework de qualité des données** : Mise en place de Great Expectations pour le monitoring automatisé de la qualité avec 850 règles de validation couvrant la complétude, l'unicité, la fraîcheur, la cohérence inter-tables et la conformité aux plages de valeurs métier, exécutées à chaque chargement de données.
4. **Tableaux de bord de gouvernance** : Création d'un dashboard de pilotage affichant le score de qualité par domaine (de 0 à 100), le taux de documentation du catalog, le nombre d'anomalies détectées et leur délai de résolution, présenté mensuellement au comité data governance et trimestriellement au COMEX.

### Résultat
- Taux de correction manuelle des rapports réglementaires réduit de 34 % à 4 % en 9 mois
- Score moyen de qualité des données passé de 61/100 à 91/100 sur les domaines critiques (sinistres, provisions, solvabilité)
- Temps de vérification des données actuarielles réduit de 6 h à 45 min par semaine (baisse de 87 %)
- Zéro recommandation du régulateur sur la traçabilité des données lors du contrôle suivant

### Leçons apprises
- La gouvernance des données ne peut pas être un projet purement IT : le rattachement du CDO à la direction générale et l'implication des directeurs métier sont des conditions sine qua non de réussite
- Démarrer le data catalog par les données réglementaires (celles à fort enjeu de conformité) crée un effet de levier qui facilite l'extension aux autres domaines
- Le score de qualité affiché par domaine introduit une dynamique de comparaison saine entre directions et accélère la prise en charge des anomalies

---

## Cas 2 : Migration d'une BI artisanale Excel vers une plateforme self-service Metabase/Looker

### Contexte
NovaTech Solutions, ESN française de 650 collaborateurs spécialisée en transformation digitale, 78 millions d'EUR de chiffre d'affaires. La gestion financière et le pilotage commercial reposent sur un écosystème de 87 fichiers Excel partagés sur un drive réseau, maintenus par 5 contrôleurs de gestion. Le directeur financier et les 12 directeurs de practice consultent des extractions Excel envoyées par email chaque vendredi.

### Problème
Les contrôleurs de gestion consacrent 60 % de leur temps à la production de rapports et seulement 40 % à l'analyse à valeur ajoutée. Trois erreurs de formule Excel non détectées au T2 ont conduit à une surestimation du taux de marge projet de 2,3 points, faussant les décisions de staffing sur 4 projets majeurs. Le délai de clôture mensuelle est de 12 jours ouvrés, contre une cible à 5 jours.

### Approche
1. **Cartographie et rationalisation des besoins** : Audit des 87 fichiers Excel pour identifier les 23 rapports réellement utilisés et les 156 indicateurs calculés, réduction à 42 indicateurs essentiels après ateliers de priorisation avec les directeurs de practice et la direction financière.
2. **Architecture data et modélisation** : Construction d'un modèle dimensionnel centré sur les axes projet, collaborateur, client et période dans PostgreSQL, alimenté par des pipelines dbt depuis les 4 sources (ERP Sage, CRM HubSpot, outil de staffing, pointage des temps), avec rafraîchissement toutes les 4 heures.
3. **Déploiement Metabase self-service** : Configuration de Metabase avec 8 dashboards thématiques (P&L mensuel, suivi staffing, pipeline commercial, rentabilité par practice, suivi trésorerie, analyse client, benchmark consultants, indicateurs RH), formation de 35 utilisateurs clés en 3 vagues de 4 heures.
4. **Gouvernance des métriques et adoption** : Mise en place d'un dictionnaire de métriques intégré à Metabase (définition, formule, source, responsable), certification officielle des dashboards validés par le contrôle de gestion, et process de demande d'évolution via un formulaire standardisé avec SLA de 5 jours.

### Résultat
- Part du temps des contrôleurs de gestion consacré à l'analyse passée de 40 % à 75 % (production de rapports réduite de 60 % à 25 %)
- Délai de clôture mensuelle réduit de 12 jours à 4,5 jours ouvrés
- Zéro erreur de calcul détectée sur les 6 mois suivant le déploiement (contre 3 erreurs majeures au T2 précédent)
- Taux d'adoption de Metabase à 83 % des utilisateurs cibles après 3 mois (mesure : connexion hebdomadaire)

### Leçons apprises
- La rationalisation des indicateurs (de 156 à 42) est l'étape la plus difficile politiquement mais la plus déterminante : chaque indicateur supprimé est une source de confusion en moins
- La certification officielle des dashboards par le contrôle de gestion crée un cercle vertueux de confiance qui accélère l'abandon des fichiers Excel
- Prévoir un budget de 20 % du projet pour l'accompagnement post-déploiement (support, évolutions mineures, formation de rattrapage) est essentiel pour maintenir l'adoption dans la durée

---

## Cas 3 : Projet de Master Data Management pour un groupe industriel multi-entités

### Contexte
Groupe Fonderies Réunies, groupe industriel de 5 600 collaborateurs réparti en 4 filiales (fonderie, usinage, traitement de surface, assemblage) opérant sur 11 sites en France et en Belgique. Chaque filiale dispose de son propre ERP (2 SAP, 1 Oracle, 1 Sage) et de ses propres référentiels clients, fournisseurs et articles. Le groupe réalise 420 millions d'EUR de chiffre d'affaires avec 2 200 clients actifs.

### Problème
Un même client peut exister sous 3 à 5 identifiants différents selon les filiales, rendant impossible une vue consolidée du chiffre d'affaires client groupe. L'écart entre le CA client consolidé calculé manuellement et les données systèmes atteint 8,7 millions d'EUR (2,1 % du CA). Les doublons fournisseurs génèrent 340 000 EUR de surcoûts annuels par perte de pouvoir de négociation, et 12 % des commandes inter-filiales subissent des erreurs de référencement article.

### Approche
1. **Diagnostic et périmètre MDM** : Analyse de la qualité des données de référence sur les 4 ERP : identification de 4 800 doublons clients (taux de 38 %), 1 200 doublons fournisseurs (taux de 22 %) et 15 000 articles sans correspondance inter-filiales. Priorisation du projet sur 3 domaines : clients, fournisseurs, articles.
2. **Plateforme MDM et golden records** : Déploiement d'une solution MDM (Informatica MDM) comme hub centralisé, avec algorithmes de matching probabiliste (nom, adresse, SIRET) pour constituer les golden records — une fiche de référence unique par entité, validée par les data stewards métier de chaque filiale.
3. **Règles de gouvernance et workflows** : Définition de 45 règles de qualité sur les données de référence (complétude SIRET obligatoire, format adresse normalisé, classification article unifiée), workflows de création/modification/désactivation avec validation par le data steward du domaine concerné et propagation automatique vers les 4 ERP.
4. **Réconciliation et nettoyage initial** : Campagne de dédoublonnage en 3 phases (automatique pour les correspondances > 95 %, assistée pour 80-95 %, manuelle pour < 80 %), mobilisant 8 data stewards sur 4 mois, suivie de l'activation des contrôles de qualité bloquants à la saisie dans chaque ERP.

### Résultat
- Nombre de doublons clients réduit de 4 800 à 120 (taux de dédoublonnage de 97,5 %)
- Vue consolidée du CA client groupe fiable à 99,6 % (écart résiduel de 1,7 million d'EUR contre 8,7 millions précédemment)
- Surcoûts fournisseurs liés aux doublons réduits de 340 000 EUR à 45 000 EUR par an (économie de 87 %)
- Taux d'erreur de référencement article inter-filiales passé de 12 % à 1,8 %

### Leçons apprises
- Le MDM est avant tout un projet organisationnel : 60 % de l'effort porte sur la définition des règles de gouvernance et l'alignement des filiales, 40 % sur la technologie
- Le nettoyage initial des données est un investissement massif mais ponctuel ; la vraie valeur réside dans les contrôles de qualité bloquants qui empêchent la réintroduction de doublons
- Impliquer les directeurs de filiale dès le cadrage en leur montrant l'impact financier des doublons sur leur propre périmètre transforme des résistances potentielles en sponsorship actif
