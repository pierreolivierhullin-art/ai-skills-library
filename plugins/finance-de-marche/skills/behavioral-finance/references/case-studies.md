# Études de cas — Finance Comportementale

## Cas 1 : Surmonter l'aversion aux pertes lors d'une correction de marché

### Contexte
Marc Delaunay, 52 ans, cadre dirigeant dans l'industrie pharmaceutique, dispose d'un portefeuille personnel de 1,2 M€ investi à 70 % en actions européennes et 30 % en obligations investment grade. Investisseur autonome depuis 15 ans, il a historiquement obtenu un rendement annualisé de 7,3 %, mais ses performances chutent systématiquement lors des phases baissières en raison de ventes paniques récurrentes.

### Problème
Lors de la correction de marché de septembre 2024 (-14 % sur l'Euro Stoxx 50 en six semaines), Marc a liquidé 40 % de ses positions actions en trois jours, cristallisant une perte de 68 000 €. L'analyse rétrospective montre qu'un maintien des positions aurait généré un gain de 42 000 € sur les trois mois suivants. Ce schéma s'était déjà produit en 2020 et 2022, représentant un manque à gagner cumulé estimé à 185 000 € sur cinq ans.

### Approche
1. **Diagnostic comportemental structuré** : Réalisation d'un journal de trading rétrospectif sur 36 mois identifiant 12 épisodes de vente impulsive, tous corrélés à des baisses intra-journalières supérieures à -3 %. Score d'aversion aux pertes mesuré à 2,8x (ratio douleur/plaisir via questionnaire Kahneman-Tversky).
2. **Mise en place de règles systématiques** : Définition d'un protocole écrit interdisant toute vente dans les 72 heures suivant une baisse de plus de -5 %. Création d'une checklist pré-transaction de 8 points incluant la vérification des fondamentaux et la consultation d'un pair de confiance.
3. **Automatisation des rééquilibrages** : Programmation de rééquilibrages trimestriels automatiques via son courtier, avec des seuils de déclenchement à ±5 % de l'allocation cible. Suppression des alertes de prix quotidiennes remplacées par un reporting mensuel.
4. **Pré-engagement et fractionnement** : Mise en place d'ordres limites prédéfinis pour acheter lors de baisses de -10 % et -20 % (stratégie d'achat programmé contra-cyclique), mobilisant 15 % de la poche liquidités à chaque palier.

### Résultat
- Réduction de 83 % des transactions impulsives (de 12 à 2 épisodes sur les 12 mois suivants)
- Surperformance de 4,1 % par rapport à son historique personnel sur la période
- Économie de frais de transaction de 3 200 € grâce à la réduction du turnover de 45 % à 12 %
- Rendement annualisé remonté à 8,9 % contre 5,2 % lors des années précédentes avec corrections

### Leçons apprises
- L'aversion aux pertes se combat par des règles ex ante, pas par la volonté au moment du stress
- Le délai de latence de 72 heures élimine plus de 80 % des décisions émotionnelles
- L'automatisation des rééquilibrages retire l'émotion du processus décisionnel

---

## Cas 2 : Protocoles de mitigation des biais cognitifs sur un desk de prop trading

### Contexte
Vertex Capital Partners, desk de prop trading basé à Paris avec 8 traders et 45 M€ de capital déployé, spécialisé dans les stratégies directionnelles sur indices et devises. Le desk affichait un Sharpe ratio de 0,92 en 2023 mais souffrait d'une dispersion importante entre traders (écart-type des P&L individuels de 34 %), suggérant des biais comportementaux non maîtrisés.

### Problème
L'analyse des 2 400 transactions de l'année révélait trois biais systématiques : effet de disposition (durée moyenne des positions perdantes 2,3x plus longue que les gagnantes), biais d'ancrage (78 % des objectifs de prix fixés sur des niveaux ronds ou des plus-hauts historiques), et excès de confiance post-série gagnante (taille des positions augmentée de 40 % en moyenne après 3 gains consécutifs). Coût estimé de ces biais : 2,8 M€ de manque à gagner annuel.

### Approche
1. **Audit comportemental quantitatif** : Déploiement d'un outil d'analyse des transactions mesurant 14 métriques comportementales par trader, incluant le ratio disposition, le temps de détention asymétrique, et le coefficient de sur-trading. Chaque trader a reçu un profil de biais personnalisé.
2. **Système de peer review pré-trade** : Instauration d'une règle imposant la validation par un pair pour toute position dépassant 2 % du capital ou toute augmentation de taille après une série de 3 gains. Mise en place de binômes rotatifs hebdomadaires.
3. **Limites dynamiques ajustées au comportement** : Réduction automatique de 25 % des limites de position pour tout trader dont le ratio disposition dépasse 1,5x sur une fenêtre glissante de 20 jours. Restauration progressive sur 10 jours de conformité.
4. **Débriefing hebdomadaire structuré** : Session de 45 minutes chaque vendredi analysant les 3 meilleures et 3 pires décisions de la semaine sous l'angle comportemental, avec scoring collectif des biais identifiés et suivi de leur évolution.

### Résultat
- Sharpe ratio du desk passé de 0,92 à 1,34 en 9 mois (+45 %)
- Réduction de la dispersion inter-traders de 34 % à 18 % d'écart-type
- Diminution du ratio de disposition moyen de 2,3x à 1,2x
- Gain net additionnel estimé à 1,9 M€ sur l'année, soit +4,2 % de rendement sur le capital

### Leçons apprises
- Les biais cognitifs sont quantifiables et leur coût peut être mesuré avec précision
- Le peer review pré-trade est plus efficace que les limites rigides car il préserve la flexibilité tactique
- Le suivi hebdomadaire crée une culture de conscience comportementale qui s'auto-renforce

---

## Cas 3 : Intégration de nudges comportementaux dans un robo-advisor

### Contexte
FinWise, robo-advisor français gérant 320 M€ pour 12 000 clients particuliers avec un ticket moyen de 26 700 €. La plateforme propose des portefeuilles ETF diversifiés avec rééquilibrage automatique. Malgré une performance moyenne de 6,8 % annualisée, le taux d'attrition atteignait 22 % par an, principalement concentré sur les périodes de volatilité élevée (VIX > 25).

### Problème
L'analyse des données clients révélait que 35 % des résiliations survenaient dans les 5 jours suivant une baisse de plus de -3 % du portefeuille. Les clients sortants affichaient ensuite un rendement inférieur de 3,2 % à ceux restés investis sur les 12 mois suivants. Le coût d'acquisition client étant de 180 €, le churn représentait une perte annuelle de 475 000 € en coûts directs et 2,1 M€ en AUM perdus.

### Approche
1. **Segmentation comportementale des clients** : Classification des 12 000 clients en 4 profils comportementaux (sereins 28 %, vigilants 34 %, anxieux 26 %, paniqueurs 12 %) basée sur la fréquence de connexion, les mouvements de souris sur les pages de performance, et l'historique de modifications de profil de risque.
2. **Nudges contextuels personnalisés** : Déploiement de messages ciblés lors des baisses : pour les anxieux, affichage de la performance cumulée depuis l'ouverture plutôt que la variation récente ; pour les paniqueurs, fenêtre de simulation montrant l'impact historique de la sortie pendant les corrections.
3. **Friction positive sur les désinvestissements** : Ajout d'un délai de réflexion de 24 heures pour tout retrait supérieur à 20 % du portefeuille pendant les périodes de VIX > 25, accompagné d'une notification rappelant la stratégie long terme définie à l'ouverture du compte.
4. **Programme de renforcement positif** : Envoi trimestriel d'un bilan comportemental personnel montrant les gains réalisés grâce au maintien de la discipline, incluant un comparatif avec le rendement hypothétique en cas de sortie lors des épisodes de stress passés.

### Résultat
- Réduction du taux d'attrition de 22 % à 11 % en 12 mois (-50 %)
- Diminution de 62 % des demandes de retrait impulsif pendant les épisodes de volatilité
- Augmentation des AUM de 320 M€ à 385 M€ grâce à la meilleure rétention (+20 %)
- Amélioration du rendement moyen client de 6,8 % à 7,5 % grâce à la réduction du market timing

### Leçons apprises
- Le recadrage temporel (afficher la performance cumulée plutôt que récente) est le nudge le plus efficace pour les profils anxieux
- La friction positive ne génère pas de frustration client si elle est accompagnée d'une explication pédagogique
- Les bilans comportementaux trimestriels créent un effet de gamification vertueuse qui renforce la discipline d'investissement
