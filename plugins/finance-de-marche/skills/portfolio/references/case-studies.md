# Études de cas — Construction & Gestion de Portefeuille

## Cas 1 : Construction de portefeuille selon la Théorie Moderne du Portefeuille pour un family office

### Contexte
Le Family Office Beaumont, basé à Genève, gère un patrimoine financier de 5 M€ pour la famille Beaumont, entrepreneurs dans le secteur de la santé. Le mandat prévoit un horizon d'investissement de 12 ans, un objectif de rendement réel de 4,5 % annualisé, et une tolérance maximale à un drawdown de -15 %. L'allocation historique, héritée d'un conseiller précédent, est concentrée à 80 % sur des actions françaises du SBF 120.

### Problème
L'analyse du portefeuille existant révèle un ratio de Sharpe de 0,48, une volatilité annualisée de 19,2 % et un biais domestique extrême avec 73 % de corrélation au CAC 40. Le drawdown maximum historique atteint -28 % (mars 2020), largement au-delà du mandat. La concentration sectorielle est critique : 45 % en santé (conflit avec le risque professionnel de la famille) et 22 % en énergie.

### Approche
1. **Optimisation mean-variance avec contraintes** : Construction de la frontière efficiente sur 8 classes d'actifs (actions Europe, US, Émergents, obligations souveraines, crédit IG, immobilier coté, matières premières, private equity) avec 15 ans de données. Application de contraintes de liquidité (minimum 70 % en actifs liquides) et de décorrélation avec le secteur santé (bêta sectoriel < 0,3).
2. **Allocation stratégique cible** : Définition d'un portefeuille optimal sur la frontière efficiente : actions internationales 45 % (dont 15 % US, 12 % Europe hors France, 10 % Émergents, 8 % Japon), obligations 30 % (dont 20 % souveraines, 10 % crédit IG), alternatifs 15 % (REITs 8 %, or 4 %, infrastructure 3 %), liquidités 10 %.
3. **Transition progressive sur 6 mois** : Plan de migration en 4 phases pour limiter l'impact fiscal et le slippage de marché. Cession prioritaire des positions santé et des lignes les moins liquides. Utilisation d'ETF comme véhicules de transition avant la sélection finale des fonds.
4. **Cadre de rééquilibrage dynamique** : Mise en place d'un rééquilibrage basé sur des bandes de tolérance (±3 % pour les actions, ±2 % pour les obligations) plutôt qu'un calendrier fixe. Intégration d'un overlay tactique permettant une déviation de ±5 % sur la poche actions selon un modèle momentum/valorisation.

### Résultat
- Ratio de Sharpe amélioré de 0,48 à 0,87 sur les 18 premiers mois post-transition
- Volatilité annualisée réduite de 19,2 % à 11,4 % (-40 %), dans l'enveloppe du mandat
- Rendement annualisé de 6,8 % contre 5,1 % pour l'ancien portefeuille sur la même période
- Drawdown maximum contenu à -9,3 % lors de la correction d'octobre 2024, contre -14,7 % pour le CAC 40

### Leçons apprises
- Le biais domestique est le destructeur de Sharpe le plus fréquent chez les investisseurs européens et sa correction produit des gains immédiats
- La transition progressive sur 6 mois a permis d'économiser 38 000 € de coûts fiscaux par rapport à une restructuration immédiate
- Les bandes de tolérance asymétriques réduisent le nombre de rééquilibrages de 40 % par rapport à un calendrier fixe tout en capturant mieux les dislocations

---

## Cas 2 : Stratégie de rééquilibrage factoriel par ETF pour un investisseur autonome

### Contexte
Sophie Lefèvre, 38 ans, ingénieure en data science, gère un portefeuille de 180 000 € en gestion autonome via un courtier en ligne. Investisseuse disciplinée depuis 8 ans, elle a accumulé 14 ETF au fil du temps sans cadre d'allocation structuré. Elle souhaite implémenter une approche factorielle systématique (value, momentum, quality, low volatility) tout en maintenant des coûts de gestion inférieurs à 0,25 % par an.

### Problème
L'audit du portefeuille montre des doublons significatifs : 4 ETF avec une corrélation supérieure à 0,92 entre eux, une exposition factorielle involontaire au growth de 0,35 et au momentum de -0,12, et un TER moyen pondéré de 0,31 %. Le rééquilibrage ad hoc (2 à 3 fois par an sans règles précises) génère un turnover excessif de 65 % et des frais de transaction de 890 € annuels.

### Approche
1. **Analyse factorielle du portefeuille existant** : Décomposition des 14 ETF en expositions aux 5 facteurs Fama-French (marché, taille, value, profitabilité, investissement) plus momentum. Identification des redondances et des lacunes : surexposition au facteur marché (+1,12), sous-exposition au value (-0,18) et au quality (-0,22).
2. **Construction du portefeuille factoriel cible** : Sélection de 7 ETF couvrant les 4 facteurs cibles avec des contraintes de liquidité (encours > 500 M€), de coût (TER < 0,30 %) et de réplication (physique privilégiée). Allocation : marché large 40 %, value 20 %, momentum 15 %, quality 15 %, low vol 10 %. TER moyen pondéré cible de 0,19 %.
3. **Protocole de rééquilibrage à seuil et momentum** : Définition de bandes de rééquilibrage à ±4 % par facteur avec un filtre momentum de 12 mois : surpondération du facteur affichant le meilleur momentum relatif dans la bande autorisée (+2 % supplémentaires). Exécution trimestrielle avec vérification mensuelle des seuils.
4. **Automatisation du suivi et du reporting** : Création d'un tableau de bord Python (bibliothèque QuantStats) calculant automatiquement les expositions factorielles, le tracking error par rapport à l'allocation cible, et les signaux de rééquilibrage. Alerte automatique lorsqu'un seuil est franchi.

### Résultat
- Réduction du nombre d'ETF de 14 à 7 et du TER moyen de 0,31 % à 0,19 % (-39 %)
- Surperformance de 2,3 % annualisée par rapport au MSCI World sur 14 mois grâce aux primes factorielles
- Réduction des frais de transaction de 890 € à 340 € par an grâce au turnover ramené de 65 % à 28 %
- Tracking error par rapport à l'allocation cible maintenu sous 1,2 % grâce au rééquilibrage à seuil

### Leçons apprises
- La majorité des portefeuilles d'ETF accumulés organiquement contiennent 30 à 50 % de redondance factorielle
- Le rééquilibrage à seuil surperforme le rééquilibrage calendaire de 0,4 à 0,8 % par an en réduisant les transactions contre-tendance
- L'ajout d'un tilt momentum au sein des bandes de tolérance ajoute 0,6 % de rendement annualisé sans augmenter la complexité opérationnelle

---

## Cas 3 : Optimisation du tax-loss harvesting pour un investisseur fortuné multi-actifs

### Contexte
Philippe Durand, 55 ans, dirigeant d'une entreprise technologique, dispose d'un portefeuille de 2,3 M€ réparti entre un CTO (compte-titres ordinaire) de 1,5 M€ et un PEA de 800 000 € plafonné. Sa tranche marginale d'imposition est de 45 % et il est soumis au PFU de 30 % sur les plus-values du CTO. Le portefeuille multi-actifs comprend des actions individuelles, des ETF, des obligations et des produits structurés.

### Problème
L'analyse fiscale révèle que Philippe a payé 89 000 € d'impôts sur les plus-values en 2023 alors qu'il détenait simultanément 142 000 € de moins-values latentes non cristallisées. L'absence de stratégie de tax-loss harvesting systématique lui coûte entre 25 000 € et 40 000 € par an en impôts évitables. De plus, l'allocation entre PEA et CTO n'est pas optimisée fiscalement.

### Approche
1. **Cartographie fiscale complète** : Inventaire de chaque ligne avec son prix de revient fiscal, sa plus ou moins-value latente, sa durée de détention, et son éligibilité aux abattements. Classification en 4 catégories : gains réalisables à moindre coût fiscal (PEA), pertes à cristalliser (CTO), positions neutres, et positions à conserver pour abattement de durée.
2. **Protocole de tax-loss harvesting systématique** : Mise en place d'un scan mensuel des positions en moins-value latente supérieure à 2 000 € sur le CTO. Vente et remplacement immédiat par un ETF similaire mais non identique (corrélation > 0,95, même classe d'actif) pour maintenir l'exposition de marché tout en cristallisant la perte fiscale. Respect strict du délai de carence de 2 mois avant rachat du titre original.
3. **Optimisation de la localisation fiscale** : Migration progressive des actifs à fort rendement attendu (small caps, émergents) vers le PEA et des actifs à faible rendement ou génération de pertes fréquentes (obligations, matières premières) vers le CTO. Rééquilibrage inter-enveloppes trimestriel.
4. **Compensation gains/pertes planifiée** : Planification annuelle de la cristallisation coordonnée des gains et des pertes. Accélération des ventes à perte en novembre-décembre pour compenser les gains déjà réalisés. Report des plus-values non urgentes à l'exercice suivant si le quota de pertes est épuisé.

### Résultat
- Économie fiscale de 37 400 € la première année grâce à la cristallisation de 124 800 € de pertes latentes
- Rendement après impôts amélioré de 1,6 point de pourcentage annualisé (de 5,2 % à 6,8 % net)
- Réduction du taux effectif d'imposition sur les gains de 28,4 % à 19,1 % grâce à l'optimisation PEA/CTO
- Création d'un stock de pertes reportables de 67 000 € utilisable sur les 10 exercices suivants

### Leçons apprises
- Le tax-loss harvesting est la seule source d'alpha véritablement gratuite et son rendement marginal est proportionnel au taux d'imposition du contribuable
- Le remplacement par ETF corrélé est préférable à la simple sortie car il élimine le risque de marché pendant la période de carence
- La localisation fiscale entre PEA et CTO génère un gain structurel de 0,8 à 1,2 % par an qui se compose sur la durée
