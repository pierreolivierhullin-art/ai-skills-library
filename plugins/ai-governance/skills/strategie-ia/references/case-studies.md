# Études de cas — Stratégie IA & Gouvernance des Modèles

## Cas 1 : Création d'un Centre d'Excellence IA dans un grand groupe d'assurance

### Contexte
Groupe Prévoyance Européenne (GPE), acteur majeur de l'assurance en France avec 9 200 collaborateurs, 6,8 milliards d'euros de primes collectées et 4,2 millions d'assurés. Le groupe dispose de 23 initiatives IA dispersées dans 7 directions métier, sans coordination centrale ni mutualisation des compétences. Le budget IA consolidé est de 14 M€/an mais le ROI global est jugé « non démontrable » par la direction financière.

### Problème
L'absence de gouvernance centralisée génère une duplication massive des efforts : 4 équipes distinctes développent des modèles de scoring client avec des approches incompatibles. Le time-to-market moyen d'un projet IA est de 14 mois (vs 6 mois chez les concurrents insurtechs). 67 % des projets IA n'atteignent jamais la production, et les 33 % déployés ne disposent d'aucun suivi de performance post-déploiement. Le comité exécutif exige une restructuration complète de la stratégie IA avec résultats mesurables sous 18 mois.

### Approche
1. **Diagnostic et design organisationnel** : Audit de maturité IA sur 5 dimensions (stratégie, données, technologie, talents, gouvernance) selon le framework MIT/BCG. Score initial : 2,1/5. Conception d'un modèle hub-and-spoke : un Centre d'Excellence IA central de 35 personnes (CoE) coordonnant des relais IA intégrés dans chaque direction métier (18 data translators). Rattachement du CoE directement au COO pour garantir le mandat transverse.
2. **Constitution de l'équipe et montée en compétence** : Recrutement de 22 profils spécialisés (ML engineers, data engineers, MLOps, product managers IA) et reconversion interne de 13 collaborateurs via un programme de 6 mois. Mise en place d'une IA Academy interne dispensant 4 niveaux de formation : sensibilisation (tous collaborateurs, 4h), praticien (métiers, 5 jours), expert (technique, 12 semaines), leader (comex, 2 jours). Objectif : 3 000 collaborateurs formés en 12 mois.
3. **Plateforme et industrialisation** : Déploiement d'une plateforme ML mutualisée (Databricks + MLflow + Kubernetes) avec feature store partagé, catalogue de modèles réutilisables et pipelines CI/CD standardisés. Définition de 4 niveaux de criticité modèle avec processus de validation proportionnés (du self-service pour les modèles exploratoires à la validation comité pour les modèles réglementés). Réduction du time-to-market cible : 4 mois.
4. **Gouvernance et pilotage par la valeur** : Création d'un AI Board trimestriel (CDO, CFO, CTO, directeurs métier) priorisant les cas d'usage par valeur business estimée et faisabilité technique. Implémentation d'un framework de mesure du ROI IA avec 3 catégories : gains directs (automatisation), gains indirects (qualité de décision), et valeur stratégique (avantage compétitif). Tableau de bord mensuel consolidant 12 KPI.

### Résultat
- Time-to-market moyen des projets IA réduit de 14 à 5,2 mois (-63 %)
- Taux de mise en production passé de 33 % à 71 % des projets initiés
- ROI IA démontrable de 23 M€ sur les 18 premiers mois (vs 14 M€ investis), soit un ratio de 1,64
- 2 850 collaborateurs formés via l'IA Academy, dont 340 certifiés praticien ou expert

### Leçons apprises
- Le rattachement hiérarchique du CoE est déterminant : un rattachement à la DSI seul crée un biais technologique, tandis qu'un rattachement au COO ou au CDO garantit l'orientation business et le mandat transverse
- Les data translators (profils hybrides métier/data) sont le maillon critique le plus sous-estimé : sans eux, la communication entre le CoE et les directions métier se dégrade en 3 mois
- La mutualisation du feature store a généré à elle seule 30 % des gains de productivité en éliminant la re-création de variables déjà calculées par d'autres équipes

---

## Cas 2 : Framework de décision Build vs Buy pour l'IA dans une entreprise de retail

### Contexte
Maisons Colbert, enseigne française de distribution spécialisée dans l'ameublement et la décoration, 3 800 salariés, 185 magasins et un site e-commerce représentant 28 % du chiffre d'affaires (1,2 Md€ total). L'entreprise identifie 9 cas d'usage IA prioritaires (recommandation produit, pricing dynamique, prévision de demande, chatbot, détection de fraude, optimisation logistique, analyse d'avis clients, visual search, et personnalisation email) mais dispose d'un budget limité de 3,5 M€ et d'une équipe data de seulement 12 personnes.

### Problème
Sans cadre décisionnel, les 3 premiers projets IA sont lancés en mode « build from scratch » par l'équipe interne, mobilisant 100 % de la capacité pendant 9 mois sans livrer de valeur en production. Le directeur digital exige simultanément un chatbot fonctionnel sous 3 mois et un moteur de recommandation sous 6 mois. L'équipe data est en burnout (turnover de 42 % sur 12 mois), les délais explosent, et le comex commence à questionner l'investissement IA global.

### Approche
1. **Conception du framework décisionnel** : Développement d'une matrice de décision Build/Buy/Partner évaluant chaque cas d'usage sur 8 critères pondérés : différenciation compétitive (25 %), disponibilité de solutions marché (15 %), complexité d'intégration (15 %), coût total sur 3 ans (15 %), time-to-value (10 %), dépendance données propriétaires (10 %), compétences requises vs disponibles (5 %), et risque réglementaire (5 %). Scoring de 1 à 5 par critère avec seuil de décision : Build si score > 3,5, Buy si < 2,5, Partner entre les deux.
2. **Évaluation systématique des 9 cas d'usage** : Ateliers de scoring réunissant équipe data, métiers, achats et direction financière sur 3 semaines. Benchmark de 28 solutions SaaS du marché. Résultat : 2 cas en Build (recommandation produit, prévision de demande -- forte dépendance aux données propriétaires), 4 cas en Buy (chatbot, détection de fraude, analyse d'avis, personnalisation email), 3 cas en Partner (pricing dynamique, visual search, optimisation logistique).
3. **Plan d'exécution séquencé** : Déploiement en 3 vagues sur 18 mois. Vague 1 (mois 1-4) : achats SaaS rapides (chatbot Intercom + module IA, fraude Signifyd) pour démontrer la valeur IA immédiate. Vague 2 (mois 3-10) : Build recommandation et prévision avec l'équipe interne libérée des sujets Buy. Vague 3 (mois 8-18) : partenariats avec intégrateurs spécialisés pour pricing et logistique.
4. **Gouvernance fournisseurs et réversibilité** : Négociation systématique de clauses de réversibilité (export des données et modèles), SLA de performance, et droits d'audit sur les solutions Buy. Mise en place d'un comité d'évaluation semestriel réévaluant chaque décision Buy/Build/Partner avec possibilité de bascule si le contexte évolue (compétences internes, maturité marché, budget).

### Résultat
- 6 cas d'usage en production en 12 mois (vs 0 sur les 9 mois précédents)
- Budget total consommé : 2,9 M€ sur 3,5 M€ alloués (économie de 17 %)
- ROI cumulé des 6 cas d'usage déployés : 5,2 M€/an (recommandation : +8 % de panier moyen, prévision : -23 % de ruptures, chatbot : -35 % d'appels niveau 1)
- Turnover de l'équipe data réduit de 42 % à 11 % grâce au recentrage sur les projets à forte valeur ajoutée

### Leçons apprises
- La décision Build vs Buy doit être réévaluée régulièrement : 2 des 4 cas initialement classés « Buy » ont été basculés en « Build » après 18 mois, lorsque l'équipe interne avait acquis suffisamment de maturité et que les solutions SaaS montraient leurs limites de personnalisation
- Le séquencement « Quick wins Buy d'abord, Build stratégique ensuite » est essentiel pour maintenir le soutien du comex : la démonstration rapide de valeur achète le temps nécessaire aux projets Build plus longs
- Le coût total de possession d'une solution Buy est systématiquement sous-estimé de 30 à 50 % si l'on ne comptabilise pas l'intégration, la personnalisation, la formation et la dépendance fournisseur

---

## Cas 3 : Évaluation de maturité IA et feuille de route pour une banque de taille intermédiaire

### Contexte
Banque Rhône-Alpes Participations (BRAP), établissement bancaire régional de 1 600 collaborateurs avec 520 000 clients particuliers et 38 000 clients professionnels. L'actif sous gestion est de 18 Md€. La banque dispose d'un département data de 8 personnes rattaché à la DSI, ayant livré 3 modèles de scoring (risque crédit, attrition, cross-sell) en production depuis 2 ans, mais sans stratégie IA formalisée ni vision à moyen terme.

### Problème
Le conseil d'administration mandate une évaluation complète de la maturité IA après que deux concurrents régionaux annoncent des investissements massifs en IA (12 M€ et 8 M€ respectivement). La BRAP craint un décrochage compétitif sur l'expérience client digitale et l'efficacité opérationnelle. Le budget disponible est de 4,2 M€ sur 3 ans, nettement inférieur aux concurrents, imposant une stratégie de focalisation. Le régulateur (ACPR) renforce parallèlement ses attentes sur la gouvernance des modèles (guidelines EBA/ECB sur le risque modèle).

### Approche
1. **Évaluation de maturité structurée** : Déploiement du framework d'évaluation sur 6 dimensions : stratégie et vision (1,8/5), données et infrastructure (2,4/5), talents et compétences (2,0/5), gouvernance et éthique (1,5/5), cas d'usage et valeur (2,6/5), culture et adoption (1,9/5). Score global : 2,0/5 (« Émergent »). Benchmark détaillé avec 12 banques comparables européennes (moyenne secteur : 2,7/5). Identification de 3 gaps critiques : gouvernance, talents, et infrastructure data.
2. **Priorisation des cas d'usage par valeur et faisabilité** : Identification de 22 cas d'usage potentiels via des ateliers avec les 6 directions métier. Évaluation selon une matrice impact business (0-100) vs faisabilité technique (0-100) vs exigence réglementaire. Sélection de 8 cas d'usage prioritaires regroupés en 3 domaines : excellence opérationnelle (automatisation KYC, détection d'anomalies comptables, OCR documents), expérience client (conseiller augmenté, chatbot FAQ, next-best-action), et gestion des risques (early warning crédit, stress testing enrichi).
3. **Construction de la feuille de route triennale** : Phase 1 « Fondations » (mois 1-12, 1,4 M€) : recrutement de 6 profils clés, déploiement d'un data lake unifié, mise en place de la gouvernance modèle conforme EBA, et livraison de 3 quick wins (automatisation KYC, OCR, chatbot FAQ). Phase 2 « Accélération » (mois 13-24, 1,6 M€) : déploiement de la plateforme MLOps, livraison de 3 cas d'usage avancés (conseiller augmenté, early warning, détection d'anomalies), formation de 400 collaborateurs. Phase 3 « Différenciation » (mois 25-36, 1,2 M€) : next-best-action, stress testing enrichi, et exploration IA générative.
4. **Cadre de gouvernance et conformité** : Rédaction d'une politique IA de 45 pages couvrant cycle de vie des modèles, gestion des risques modèle (MRM), éthique, et conformité réglementaire. Création d'un comité modèle mensuel validant chaque mise en production. Mise en place d'un inventaire centralisé des modèles avec classification par niveau de risque (4 tiers). Préparation à l'AI Act : cartographie des 8 cas d'usage selon la classification de risque européenne.

### Résultat
- Score de maturité IA passé de 2,0 à 3,3/5 en 24 mois (cible 3,8/5 à 36 mois)
- 6 cas d'usage en production à la fin de la phase 2, générant 3,1 M€ de valeur annuelle identifiée
- Automatisation KYC : réduction du temps de traitement de 35 minutes à 8 minutes par dossier, économie de 1,2 M€/an
- Conformité réglementaire : zéro observation majeure lors de l'inspection ACPR sur la gouvernance des modèles

### Leçons apprises
- Pour une banque de taille intermédiaire, la stratégie de focalisation sur 6-8 cas d'usage à fort impact est plus rentable que la dispersion sur 20 initiatives : le budget limité impose une discipline de priorisation impitoyable
- La gouvernance des modèles n'est pas un frein mais un accélérateur : les processus de validation structurés réduisent le time-to-market en éliminant les allers-retours tardifs avec la conformité et le risque
- L'évaluation de maturité est un outil de communication interne puissant : la visualisation des gaps par rapport aux concurrents a été le déclencheur le plus efficace pour obtenir le sponsorship du conseil d'administration et l'adhésion des directions métier
