# Études de cas — Data Engineering

## Cas 1 : Migration d'un ETL legacy vers une stack moderne ELT avec dbt et Snowflake

### Contexte
Groupe Lefèvre Industries, ETI industrielle de 2 800 salariés basée à Lyon, spécialisée dans la fabrication de composants aéronautiques. Le système décisionnel repose depuis 12 ans sur une chaîne ETL Informatica PowerCenter alimentant un data warehouse Oracle on-premise. L'équipe data de 6 personnes passe 70 % de son temps en maintenance corrective des pipelines existants.

### Problème
Les jobs ETL cumulent un temps d'exécution moyen de 9 h 40 par nuit, avec un taux d'échec de 18 % nécessitant des reprises manuelles quotidiennes. Le coût annuel de licences Informatica et Oracle atteint 380 000 EUR, tandis que le délai moyen de livraison d'un nouveau rapport est de 14 semaines. La dette technique rend toute évolution structurelle quasi impossible.

### Approche
1. **Audit et cartographie des flux** : Inventaire exhaustif des 247 jobs ETL existants, classification par criticité métier (P1 à P4) et identification des 83 transformations réellement utilisées par les consommateurs finaux.
2. **Architecture cible ELT** : Déploiement de Snowflake comme entrepôt cloud, Fivetran pour l'ingestion des 12 sources (ERP SAP, CRM, MES), et dbt Core pour les transformations versionnées sous Git avec 100 % de couverture de tests.
3. **Migration incrémentale par domaine** : Migration progressive sur 5 vagues de 6 semaines chacune, en commençant par le domaine finance (le plus documenté), avec exécution parallèle ancien/nouveau système et comparaison automatisée des résultats.
4. **Décommissionnement et formation** : Extinction progressive d'Informatica, formation de l'équipe à dbt et SQL analytique (40 h par personne), mise en place de revues de code data et documentation automatique via dbt docs.

### Résultat
- Temps d'exécution nocturne réduit de 9 h 40 à 1 h 15 (baisse de 87 %)
- Taux d'échec des pipelines passé de 18 % à 2,3 %
- Coût annuel d'infrastructure réduit de 380 000 EUR à 145 000 EUR (économie de 62 %)
- Délai de livraison d'un nouveau rapport ramené de 14 semaines à 3 semaines

### Leçons apprises
- La migration incrémentale par domaine métier réduit considérablement le risque par rapport à une approche big-bang
- L'exécution parallèle ancien/nouveau système est indispensable pour garantir la confiance des métiers dans les données migrées
- Investir dans la formation de l'équipe existante plutôt que recruter des profils spécialisés assure une meilleure continuité opérationnelle

---

## Cas 2 : Pipeline de streaming temps réel avec Kafka pour un moteur de recommandation e-commerce

### Contexte
ModaStream, pure player e-commerce français de mode et accessoires, 45 millions d'EUR de chiffre d'affaires annuel, 1,2 million de visiteurs uniques mensuels. Le système de recommandation produits fonctionne en batch quotidien sur la base des données de navigation de la veille. L'équipe data compte 4 data engineers et 2 data scientists.

### Problème
Le moteur de recommandation batch génère des suggestions obsolètes : un client ayant acheté un article le matin se voit encore recommander ce même article le soir. Le taux de clic sur les recommandations stagne à 2,1 % et le panier moyen associé aux suggestions est de 38 EUR. Les pics de trafic lors des ventes flash (x8 le trafic normal) provoquent des pertes de données de navigation estimées à 15 % des événements.

### Approche
1. **Collecte événementielle temps réel** : Déploiement d'Apache Kafka (cluster de 6 brokers) avec un schéma registry Avro pour capturer les événements de navigation, ajout panier, achat et recherche, soit environ 12 millions d'événements par jour en régime normal.
2. **Traitement stream avec Kafka Streams** : Développement de micro-services de transformation calculant en temps réel les profils de session utilisateur (catégories visitées, fourchette de prix, marques consultées) avec une fenêtre glissante de 30 minutes et une latence cible inférieure à 500 ms.
3. **Feature store temps réel** : Alimentation d'un feature store Redis contenant les 25 features clés par utilisateur, consommé directement par le modèle de recommandation via une API de scoring avec un SLA de réponse à 50 ms au p99.
4. **Observabilité et résilience** : Mise en place d'un monitoring Prometheus/Grafana sur le consumer lag, le throughput et la latence end-to-end, avec alertes automatiques et mécanisme de replay depuis les topics Kafka en cas d'incident.

### Résultat
- Latence de recommandation passée de 24 h (batch J-1) à 800 ms en moyenne
- Taux de clic sur les recommandations augmenté de 2,1 % à 5,8 % (+176 %)
- Panier moyen des achats issus de recommandations passé de 38 EUR à 62 EUR (+63 %)
- Zéro perte d'événement mesurée lors des 3 dernières ventes flash (pics à 2 400 événements/seconde)

### Leçons apprises
- Le passage au temps réel ne concerne pas uniquement la technologie : le modèle de recommandation lui-même doit être repensé pour exploiter des features de session courte
- Un schéma registry strict dès le départ évite des semaines de debugging liées à des incompatibilités de format entre producteurs et consommateurs
- Le dimensionnement du cluster Kafka doit anticiper les pics de charge avec un facteur x10 par rapport au trafic nominal pour absorber les ventes flash sans dégradation

---

## Cas 3 : Implémentation d'une architecture Data Lakehouse pour un groupe média

### Contexte
Groupe Médias Confluence, conglomérat média français regroupant 3 chaînes TV, 8 stations radio, 12 sites web éditoriaux et une plateforme de streaming. Le groupe génère quotidiennement 2,4 To de données hétérogènes (logs de streaming, données publicitaires, audiences TV Médiamétrie, contenus éditoriaux, données CRM). Deux silos coexistent : un data lake S3 sous-exploité et un data warehouse Redshift saturé.

### Problème
Les analystes média attendent en moyenne 4 jours pour obtenir une vue consolidée des audiences cross-canal. Le data lake contient 18 mois de données brutes sans catalogage ni gouvernance, rendant 60 % des données inexploitables. Le coût combiné S3 + Redshift atteint 52 000 EUR par mois, avec un taux d'utilisation effectif de Redshift de seulement 35 % en raison de requêtes mal optimisées.

### Approche
1. **Architecture lakehouse sur Delta Lake** : Migration vers une architecture lakehouse unifiée avec Delta Lake sur S3, organisée en trois couches (bronze/silver/gold) et orchestrée par Apache Spark sur Databricks, permettant de combiner stockage économique et requêtes analytiques performantes.
2. **Ingestion multi-format unifiée** : Développement de connecteurs standardisés pour les 7 types de sources (API Médiamétrie, flux publicitaires programmatiques en JSON, logs Kafka du player streaming, fichiers CSV CRM, données semi-structurées réseaux sociaux) avec validation de schéma à l'ingestion.
3. **Couche sémantique et catalogage** : Déploiement d'Unity Catalog pour le catalogage automatique des 340 tables, avec lignage de données end-to-end, contrôle d'accès par rôle métier (éditorial, régie pub, direction générale) et documentation automatique des métriques d'audience.
4. **Optimisation des performances et des coûts** : Mise en place du Z-ordering sur les colonnes de date et de canal, partitionnement par média et par jour, configuration de l'auto-scaling Databricks avec plafond budgétaire et migration des requêtes récurrentes vers des tables matérialisées Delta.

### Résultat
- Délai d'obtention d'une vue audience cross-canal réduit de 4 jours à 35 minutes
- Taux de données exploitables dans le lac passé de 40 % à 94 % grâce au catalogage et à la validation de qualité
- Coût mensuel d'infrastructure réduit de 52 000 EUR à 31 000 EUR (économie de 40 %)
- Nombre de requêtes analytiques exécutées par les équipes métier multiplié par 6 (de 180 à 1 100 par semaine)

### Leçons apprises
- L'architecture en couches bronze/silver/gold impose une discipline de transformation qui résout naturellement les problèmes de qualité des données accumulés dans un data lake non gouverné
- Le catalogage et le lignage ne sont pas des fonctionnalités optionnelles : sans eux, un lakehouse reproduit les mêmes travers qu'un data lake classique
- L'implication des équipes métier dans la définition de la couche gold (métriques, dimensions, grain) est le facteur déterminant du taux d'adoption
