# Études de cas — Options & Gestion des Risques

## Cas 1 : Stratégie de génération de revenus par covered calls et cash-secured puts sur un portefeuille de dividendes

### Contexte
Isabelle Marchand, 61 ans, ancienne directrice financière, gère un portefeuille de 850 000 € composé de 25 titres européens à dividendes (rendement moyen 3,8 %). Récemment retraitée, elle cherche à compléter ses revenus annuels de 15 000 € nets issus des dividendes sans augmenter significativement le risque du portefeuille ni modifier sa composition fondamentale.

### Problème
Les taux obligataires ayant baissé à 2,9 % sur le Bund 10 ans, les alternatives de revenus fixes sont insuffisantes. Isabelle a besoin de 28 000 € de revenus annuels supplémentaires pour maintenir son niveau de vie. La simple augmentation de l'allocation en titres à haut dividende concentrerait le portefeuille sur des secteurs fragiles (utilities, telecom) et dégraderait la diversification.

### Approche
1. **Sélection des sous-jacents éligibles** : Identification de 12 titres sur 25 disposant d'options liquides avec un spread bid-ask inférieur à 3 % et un volume quotidien supérieur à 500 contrats. Couverture de 480 000 € du portefeuille, soit 56 % de la valeur totale.
2. **Stratégie de covered calls systématique** : Vente mensuelle de calls couverts à delta 0,25 (probabilité d'exercice de 25 %) sur les 12 titres éligibles, générant un premium moyen de 0,8 % par mois. Roulement systématique à 5 jours de l'échéance si le call est dans la monnaie.
3. **Cash-secured puts opportunistes** : Déploiement de 120 000 € en cash collatéral pour la vente de puts à delta -0,20 sur 4 titres de qualité présents sur la watchlist d'Isabelle. Strikes fixés 10-15 % sous le cours actuel, créant des points d'entrée attractifs en cas d'assignation.
4. **Gestion du risque d'assignation** : Définition de règles claires — acceptation de l'assignation sur les covered calls si plus-value supérieure à 12 %, sinon roulement vers l'échéance suivante avec crédit net. Pour les puts, assignation acceptée uniquement si le titre reste dans les critères fondamentaux.

### Résultat
- Revenus additionnels de primes de 31 200 € sur 12 mois, soit 3,7 % de rendement supplémentaire sur le portefeuille
- Rendement total (dividendes + primes) porté à 7,5 % contre 3,8 % précédemment
- Seulement 3 assignations de covered calls sur 144 contrats vendus (taux d'assignation de 2,1 %)
- Acquisition via puts de 2 nouveaux titres à des prix inférieurs de 12 % et 14 % au cours du jour de la vente du put

### Leçons apprises
- Le delta 0,25 offre le meilleur compromis entre rendement des primes et probabilité de conservation des titres
- La combinaison covered calls + cash-secured puts transforme un portefeuille de dividendes en machine à revenus sans dénaturer la stratégie fondamentale
- Le roulement systématique à J-5 permet de capturer 85 % du theta decay tout en préservant la flexibilité

---

## Cas 2 : Couverture de portefeuille par puts protecteurs et collars lors d'un pic de volatilité

### Contexte
Gestion Patrimoniale Rhône-Alpes (GPRA), family office gérant 18 M€ pour la famille Dumont, industriels lyonnais. Le portefeuille est investi à 65 % en actions (11,7 M€), 25 % en obligations et 10 % en alternatifs. Le mandat impose une perte maximale annuelle de -8 % sur la poche actions, contrainte réglementaire liée au pacte familial.

### Problème
En octobre 2024, le VIX passe de 14 à 32 en deux semaines suite aux tensions géopolitiques et à une révision des anticipations de taux. Le portefeuille actions affiche déjà -5,2 % YTD, ne laissant qu'une marge de 2,8 % avant de déclencher la clause de protection du mandat. Le coût estimé d'une couverture complète par puts ATM s'élève à 420 000 € (3,6 % du portefeuille actions), jugé prohibitif.

### Approche
1. **Analyse de la structure de volatilité** : Étude du skew de volatilité sur l'Euro Stoxx 50 révélant une prime de 8 points entre les puts OTM à -10 % et les puts ATM. Identification d'une opportunité de financement par collar en raison de la volatilité implicite élevée des calls OTM.
2. **Couverture par collar à coût réduit** : Achat de puts à strike -8 % sur 7,5 M€ de la poche actions (coût : 185 000 €) financé à 70 % par la vente de calls à strike +12 % (prime reçue : 130 000 €). Coût net de la couverture ramené à 55 000 € soit 0,47 % du portefeuille actions.
3. **Puts protecteurs partiels sur les positions concentrées** : Achat de puts ATM spécifiques sur les 3 plus grosses positions individuelles (2,8 M€ cumulés, 24 % du portefeuille actions), représentant le risque de concentration le plus élevé. Coût additionnel de 78 000 €.
4. **Monétisation progressive de la couverture** : Plan de débouclage en 3 paliers — vente de 33 % des puts si le VIX repasse sous 22, 33 % sous 18, et conservation du dernier tiers jusqu'à échéance. Réinvestissement des primes récupérées en obligations courtes.

### Résultat
- Protection activée lors de la baisse additionnelle de -6,8 % du marché, limitant la perte du portefeuille actions à -7,4 % (sous le seuil de -8 %)
- Coût total de la couverture de 133 000 € soit 1,14 % du portefeuille actions, contre 3,6 % pour une couverture classique
- Gain sur les puts protecteurs des positions concentrées de 210 000 € lors du rebond partiel (vente à profit)
- Mandat respecté, évitant le déclenchement de la clause de liquidation partielle estimée à 1,2 M€ de coûts d'opportunité

### Leçons apprises
- Le collar est l'instrument optimal en période de volatilité élevée car le skew finance naturellement la couverture
- La couverture des positions concentrées par des puts individuels est plus efficace que la couverture indicielle pure lorsque la corrélation intra-portefeuille est inférieure à 0,7
- Un plan de débouclage prédéfini évite de conserver la couverture trop longtemps et de subir l'érosion du theta

---

## Cas 3 : Stratégie de trading de volatilité par iron condors et straddles en saison de résultats

### Contexte
Thomas Renault, 34 ans, trader indépendant spécialisé en options sur actions américaines, opérant avec un capital de 280 000 €. Il se concentre sur les earnings seasons (4 périodes de 3 semaines par an) en exploitant les écarts entre volatilité implicite et volatilité réalisée autour des publications de résultats. Son track record montre un rendement annualisé de 18 % mais avec un drawdown maximal de -22 %.

### Problème
La saison Q3 2024 s'annonce particulièrement complexe : la volatilité implicite médiane des straddles pre-earnings sur le S&P 500 s'établit à 38 %, soit 12 points au-dessus de la volatilité réalisée historique médiane. Thomas suspecte une surenchère de la volatilité implicite mais identifie 15 titres sur sa watchlist où le premium semble justifié par des incertitudes fondamentales réelles. L'enjeu est de séparer les opportunités de vente de volatilité des cas où l'achat est préférable.

### Approche
1. **Modèle de scoring de la volatilité pre-earnings** : Construction d'un score composite sur 5 critères — écart IV/RV historique, dispersion des estimations analystes, activité inhabituelle sur options, résultats du secteur déjà publiés, et pattern de volatilité réalisée post-earnings des 8 derniers trimestres. Classement des 40 titres de la watchlist en 3 catégories : vente, achat, neutre.
2. **Iron condors sur les titres à volatilité surévaluée** : Déploiement de 18 iron condors (catégorie vente, score < 30) avec des wings à 1,5 écart-type du move implicite. Taille par position limitée à 2 % du capital (5 600 €). Ratio risk/reward cible de 1:3 (prime reçue / perte max).
3. **Straddles sur les titres à incertitude fondamentale élevée** : Achat de 8 straddles ATM (catégorie achat, score > 70) avec un budget de prime limité à 4 % de la valeur du sous-jacent. Objectif de mouvement post-earnings supérieur à 1,3x le move implicite. Débouclage systématique à J+1 après la publication.
4. **Gestion du risque de portefeuille** : Exposition nette vega maintenue entre -15 000 € et +15 000 €. Corrélation croisée des positions vérifiée pour éviter la concentration sectorielle (maximum 3 positions dans le même secteur). Stop-loss global à -5 % du capital pour la saison.

### Résultat
- Rendement de la saison Q3 : +7,2 % sur le capital total (20 160 €) en 18 jours de trading
- Taux de succès des iron condors : 14/18 profitables (78 %), gain moyen de 820 € par position
- Taux de succès des straddles : 5/8 profitables (63 %), gain moyen de 1 450 € par position gagnante
- Drawdown maximal intra-saison limité à -3,1 %, contre -22 % historique, grâce au dimensionnement discipliné

### Leçons apprises
- Le scoring systématique de la volatilité pre-earnings élimine le biais de confirmation et améliore le taux de succès de 15 points par rapport au jugement discrétionnaire
- Les iron condors à 1,5 écart-type offrent un meilleur ratio rendement/risque que les positions plus serrées malgré des primes unitaires plus faibles
- La discipline de débouclage à J+1 capture l'essentiel du vol crush tout en évitant l'exposition au risque directionnel post-earnings
