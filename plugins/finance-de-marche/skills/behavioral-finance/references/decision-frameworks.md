# Decision Frameworks — Cadres de Decision pour l'Investissement

## Overview

Ce document de reference approfondit les cadres de decision utilises en finance comportementale pour ameliorer la qualite des decisions d'investissement. Il couvre le modele dual-process de Kahneman (Systeme 1 vs Systeme 2), l'analyse des heuristiques, la Prospect Theory en detail, le pre-mortem analysis de Gary Klein, le checklist-based investing, le decision journaling structure, la calibration probabiliste, et le Bayesian updating applique a l'investissement. Utiliser ce guide pour construire un processus de decision rigoureux qui neutralise les biais cognitifs par la structure plutot que par la volonte.

This reference document deepens the decision frameworks used in behavioral finance to improve investment decision quality: Kahneman's dual-process model, heuristic analysis, Prospect Theory, pre-mortem analysis, checklist-based investing, decision journaling, probabilistic calibration, and Bayesian updating.

---

## System 1 vs System 2 — Le Modele Dual-Process (Kahneman, 2011)

### Fondements theoriques

Daniel Kahneman, dans *Thinking, Fast and Slow* (2011), propose un modele a deux systemes de pensee :

| Caracteristique | Systeme 1 (Pensee rapide) | Systeme 2 (Pensee lente) |
|---|---|---|
| **Mode** | Automatique, intuitif | Delibere, analytique |
| **Effort** | Faible, sans effort conscient | Eleve, requiert attention |
| **Vitesse** | Instantane | Lent |
| **Conscience** | Inconscient, invisible | Conscient, explicite |
| **Contexte d'activation** | Par defaut, toujours actif | Active sur demande, ou par echec du Systeme 1 |
| **Erreurs typiques** | Biais heuristiques, substitution | Paresse cognitive, rationalisations |
| **Forces** | Pattern recognition, reactions rapides | Calcul, logique, planification |

### Le probleme fondamental en investissement

Le Systeme 1 domine les decisions d'investissement pour plusieurs raisons :
- **Surcharge informationnelle** : le flux continu de news, prix, opinions et donnees sature la capacite du Systeme 2, forcant un repli sur le Systeme 1.
- **Pression temporelle** : les marches bougent en temps reel. L'urgence percue active le Systeme 1.
- **Charge emotionnelle** : l'argent est un domaine emotionnel. Les pertes et les gains activent des reponses limbiques qui court-circuitent le Systeme 2.
- **Fatigue decisionnelle** : le Systeme 2 est une ressource epuisable (ego depletion, Baumeister). Apres des heures de trading, le Systeme 1 prend le relais.

### Erreurs specifiques du Systeme 1 en finance

1. **Substitution de question** : le Systeme 1 remplace une question difficile par une question facile. "Cette entreprise est-elle un bon investissement ?" est remplace par "Est-ce que j'aime cette entreprise ?" ou "Ai-je recemment entendu parler de cette entreprise ?"
2. **Pattern matching errone** : le Systeme 1 identifie des patterns dans le bruit aleatoire (apophenie). Un graphique de cours ressemble a un pattern technique -> achat. En realite, la plupart des patterns chartistes ont une valeur predictive nulle ou marginale.
3. **Reponse affective (affect heuristic)** : le jugement est influence par l'emotion ressentie envers un actif. "J'aime Apple en tant que marque" -> "Apple est un bon investissement." Les deux propositions sont independantes.
4. **WYSIATI (What You See Is All There Is)** : le Systeme 1 construit l'histoire la plus coherente avec les informations disponibles, sans considerer les informations manquantes. Un pitch d'investissement convaincant est dangereux precisement parce qu'il est concu pour activer WYSIATI.

### Strategies pour activer le Systeme 2

1. **Checklists obligatoires** : une checklist force un processus sequentiel et delibere, activant le Systeme 2 mecaniquement.
2. **Delai de reflexion** : imposer un delai (24h minimum) entre l'identification d'une opportunite et l'execution.
3. **Ecriture** : ecrire sa these d'investissement active le Systeme 2. L'ecriture force la linearisation d'une pensee qui, en mode Systeme 1, est floue et impressionniste.
4. **Quantification** : transformer les jugements qualitatifs en estimations quantitatives ("c'est cher" -> "P/E de 35 vs moyenne sectorielle de 20, soit une prime de 75%").
5. **Environnement controle** : reduire les stimuli (fermer les ecrans de marche, desactiver les alertes, trader dans un environnement calme).
6. **Timing optimal** : prendre les decisions importantes le matin, quand le Systeme 2 est frais. Eviter les decisions apres le dejeuner (post-lunch dip) ou en fin de journee.

---

## Heuristiques vs Pensee Analytique — Quand Utiliser Quoi

### Taxonomie des heuristiques en finance

| Heuristique | Mecanisme | Erreur typique en finance | Correctif analytique |
|---|---|---|---|
| **Representativite** | Juger par ressemblance au prototype | "Cette startup ressemble a Amazon a ses debuts" -> acheter sans analyse | Taux de base : 90% des startups echouent |
| **Disponibilite** | Estimer par facilite de rappel | Surestimer le risque de krach apres un documentaire sur 2008 | Statistiques objectives de frequence |
| **Ancrage** | Ajuster insuffisamment depuis un point de depart | Acheter car "30% sous le plus haut historique" | Valorisation intrinseque independante |
| **Affect** | Juger par l'emotion ressentie | "J'adore ce produit -> j'achete l'action" | Analyse financiere independante du sentiment |
| **Recognition** | Preferer le familier | Surponderer les grandes capitalisations connues (home bias) | Diversification systematique |
| **1/N** | Repartir egalement entre les options | Allocation egale entre N fonds proposes -> sous-optimal | Optimisation mean-variance |
| **Peak-end rule** | Juger une experience par son pic et sa fin | Memoire biaisee du dernier krach (panique finale) | Analyse statistique des drawdowns historiques |

### Quand l'heuristique est acceptable

Les heuristiques ne sont pas toujours nocives. Gerd Gigerenzer (ecole de la rationalite ecologique) montre que dans certains contextes, les heuristiques simples surperforment les modeles complexes :
- **Environnements a forte incertitude** (vs risque calculable) : quand les distributions de probabilite sont inconnues, un modele complexe avec de nombreux parametres estime mal. Une heuristique simple (1/N allocation, par exemple) peut etre plus robuste.
- **Decisions a faible enjeu** : le cout cognitif de l'analyse formelle depasse le benefice pour les decisions mineures.
- **Screening initial** : utiliser des heuristiques rapides pour filtrer l'univers d'investissement, puis appliquer l'analyse formelle sur le sous-ensemble retenu.

**Regle pratique** : utiliser le Systeme 1 (heuristiques) pour le screening et le filtrage. Utiliser le Systeme 2 (analytique) pour toute decision impliquant plus de 1% du portefeuille.

---

## Prospect Theory — Approfondissement (Kahneman & Tversky, 1979)

### Les quatre composantes de la Prospect Theory

#### 1. Reference dependence (dependance au point de reference)

Les individus evaluent les resultats comme des gains ou des pertes par rapport a un point de reference, et non en termes de richesse totale (contrairement a la theorie de l'utilite attendue).

**Implications en investissement** :
- Le point de reference le plus courant est le prix d'achat. Tout mouvement est juge par rapport a ce point, pas par rapport a la valeur intrinseque.
- Le point de reference peut etre deplace : un objectif d'analyste, le rendement d'un indice de reference, le rendement d'un pair.
- La manipulation du point de reference est un levier de decision : cadrer un investissement comme "20% sous le plus haut" (gain potentiel) vs "20% au-dessus du plus bas" (gain realise) change la perception.

#### 2. Loss aversion (aversion aux pertes)

La fonction de valeur est plus raide pour les pertes que pour les gains. Le ratio typique est de 2 a 2.5 (coefficient de loss aversion, lambda).

**Formulation mathematique simplifiee** :
```
v(x) = x^alpha            pour x >= 0 (gains)
v(x) = -lambda * |x|^beta  pour x < 0 (pertes)

Parametres typiques (Tversky & Kahneman, 1992) :
alpha = 0.88, beta = 0.88, lambda = 2.25
```

#### 3. Diminishing sensitivity (sensibilite decroissante)

La sensibilite aux changements diminue quand on s'eloigne du point de reference. La difference entre gagner 100 EUR et 200 EUR est percue comme plus grande que la difference entre gagner 1100 EUR et 1200 EUR, bien que la difference objective soit identique (100 EUR). Cela explique pourquoi les investisseurs sont averses au risque dans le domaine des gains (preferer un gain certain) et preneurs de risque dans le domaine des pertes (preferer un pari pour eviter une perte certaine).

#### 4. Probability weighting (ponderation des probabilites)

Les individus deforment les probabilites objectives. Ils surponderent les evenements rares et sous-ponderent les evenements frequents.

| Probabilite objective | Ponderation typique | Implication financiere |
|---|---|---|
| 0.01 (1%) | Surponderee (~5.5%) | Explique l'achat de billets de loterie et de puts OTM tres bon marche |
| 0.10 (10%) | Surponderee (~18.6%) | Explique la survalorisation des options bon marche (lottery tickets) |
| 0.50 (50%) | Legerement sous-ponderee | Indifference relative pour les evenements "50/50" |
| 0.90 (90%) | Sous-ponderee (~71.2%) | Explique la surassurance et les ventes de panique (sous-ponderation de la probabilite de reprise) |
| 0.99 (99%) | Sous-ponderee (~91.2%) | Explique la peur irrationnelle d'evenements quasi-certains |

**Application directe** : la surponderation des evenements rares explique pourquoi les options tres hors de la monnaie (OTM) sont systematiquement surpayees, et pourquoi les investisseurs sont attires par les actions "lottery ticket" (forte volatilite, faible probabilite de gain enorme).

---

## Pre-Mortem Analysis — Methode de Gary Klein

### Protocole detaille

Le pre-mortem, developpe par le psychologue Gary Klein, est publie dans Harvard Business Review (2007). Il inverse la logique du post-mortem traditionnel : au lieu d'analyser un echec apres qu'il s'est produit, on imagine que l'echec s'est produit et on en recherche les causes.

#### Etape 1 — Formulation

Rassembler l'equipe de decision (ou se preparer seul). Enoncer la decision envisagee : "Nous allons investir 500 000 EUR dans l'action X avec un horizon de 18 mois."

#### Etape 2 — Projection negative

Annoncer : "Imaginez que nous sommes dans 18 mois. L'investissement a ete un desastre complet. Nous avons perdu 50% du capital." Chaque participant ecrit independamment (important : pas de discussion avant) toutes les raisons plausibles de cet echec.

#### Etape 3 — Aggregation

Collecter et regrouper toutes les raisons identifiees. Classer par :
- **Probabilite** : quelle est la vraisemblance de ce scenario ?
- **Impact** : quelle serait la gravite si ce scenario se realisait ?
- **Detectabilite** : pourrait-on detecter ce scenario avant qu'il ne cause des dommages irreversibles ?

#### Etape 4 — Mitigation

Pour chaque risque a haute probabilite ou haut impact :
- Definir des indicateurs d'alerte precoce (leading indicators).
- Definir des actions preventives realisables.
- Definir des plans de contingence (si le scenario se realise, que fait-on ?).
- Integrer dans le dimensionnement de la position.

#### Etape 5 — Decision finale

Reevaluer la decision a la lumiere du pre-mortem. Options :
- Proceder avec les mitigations en place.
- Reduire la taille de la position.
- Reporter la decision pour obtenir plus d'information.
- Annuler la decision si les risques sont inacceptables.

### Pourquoi le pre-mortem est superieur a l'analyse de risque classique

1. **Contourne l'overconfidence** : le cadrage "l'echec a eu lieu" reduit l'optimisme naturel et le biais de planification.
2. **Active le Systeme 2** : l'exercice d'imagination concrete force une reflexion deliberee.
3. **Legitimise la dissidence** : dans un contexte de groupe, le pre-mortem donne la permission d'exprimer des doutes sans etre percu comme negatif.
4. **Genere plus de risques** : les recherches de Klein montrent que les pre-mortems identifient 30% plus de risques que les analyses de risque classiques.

---

## Checklist-Based Investing — Investir par Checklist

### Fondements (Gawande, 2009)

Atul Gawande, dans *The Checklist Manifesto*, demontre que les checklists reduisent les erreurs dans les domaines complexes (chirurgie, aviation, construction). En investissement, les checklists compensent :
- La fatigue decisionnelle (le Systeme 2 s'epuise).
- Les oublis systematiques (biais de disponibilite, WYSIATI).
- La pression emotionnelle (l'excitation ou la peur court-circuitent le processus).

### Types de checklists en investissement

#### Checklist de Pre-Investissement (DO-CONFIRM)

A utiliser comme verification finale avant d'executer une decision deja analysee :

```
CHECKLIST PRE-INVESTISSEMENT
================================
FONDAMENTAUX
[ ] La these d'investissement est documentee par ecrit
[ ] L'avantage competitif (moat) est identifie et durable
[ ] Les etats financiers des 5 derniers exercices ont ete analyses
[ ] La valorisation est justifiee par au moins 2 methodes independantes
[ ] Les hypotheses de croissance sont realistes (comparees au secteur)
[ ] Le management a ete evalue (track record, alignement d'interets, skin in the game)

RISQUES
[ ] Les 3 principaux risques sont identifies et documentes
[ ] Un pre-mortem a ete conduit pour les positions > 3% du portefeuille
[ ] Le scenario de worst-case est survivable (drawdown maximal acceptable)
[ ] Les conditions d'invalidation de la these sont definies

BIAIS
[ ] L'argument contraire le plus fort a ete articule (steel-man)
[ ] Aucun biais identifiable n'influence la decision (FOMO, anchoring, confirmation)
[ ] L'etat emotionnel est neutre (pas de revenge trading, pas d'euphorie post-gains)

EXECUTION
[ ] Le sizing est conforme au risk management (Kelly criterion, max % portfolio)
[ ] Le stop-loss est defini avant l'entree
[ ] L'objectif de sortie et le ratio risk/reward sont documentes
[ ] La decision respecte le plan de trading ecrit
```

#### Checklist de Sortie (READ-DO)

A executer sequentiellement quand un trigger de sortie est active :

```
CHECKLIST DE SORTIE
========================
[ ] Le stop-loss est atteint -> EXECUTER (pas de renegociation)
[ ] L'objectif est atteint -> verifier si les fondamentaux justifient de tenir
[ ] La these a ete invalidee -> SORTIR quelle que soit la P&L
[ ] Un evenement materiel a change les fondamentaux -> reevaluer de zero
[ ] Le sizing est devenu trop gros vs le portefeuille -> rebalancer
```

### Implementation pratique

1. **Personnaliser** : adapter les checklists a son style d'investissement (value, growth, quantitatif, macro).
2. **Physique ou digitale** : une checklist papier posee a cote de l'ecran est plus efficace qu'un fichier numerique oublie. La friction physique est intentionnelle.
3. **Evolutive** : ajouter des items apres chaque erreur identifiee en post-mortem. La checklist est un document vivant.
4. **Non negociable** : une checklist est un commitment device. Si un item n'est pas coche, la decision ne passe pas. Pas d'exceptions.

---

## Decision Journaling — Protocole Approfondi

### Structure du journal

Le decision journaling est la pratique la plus impactante pour ameliorer la qualite decisionnelle a long terme. Il cree une base de donnees personnelle de decisions, permettant l'analyse retrospective des patterns de biais et la calibration des estimations.

#### Entree pre-decision

```
DATE : ____________
DECISION : ____________ [description factuelle : acheter/vendre/garder X a Y EUR]
THESE EN UNE PHRASE : ____________
CATALYSEUR : ____________ [qu'est-ce qui declenche la decision maintenant ?]
HORIZON : ____________ [timeframe de la these]
CONVICTION : __ /10
ETAT EMOTIONNEL : stress __/10, fatigue __/10, excitation __/10
BIAIS POTENTIELS IDENTIFIES : ____________
ARGUMENT CONTRAIRE LE PLUS FORT : ____________
PROBABILITE DE SUCCES ESTIMEE : __ % [pour calibration future]
CONDITIONS D'INVALIDATION : ____________
```

#### Entree post-decision (a completer apres la conclusion du trade)

```
DATE DE SORTIE : ____________
RESULTAT : +/- __ EUR (__ %)
LA THESE ETAIT-ELLE CORRECTE ? ____________
LE RESULTAT EST-IL DU AU SKILL OU A LA CHANCE ? ____________
QUALITE DU PROCESSUS : __ /10 [independamment du resultat]
BIAIS DETECTES RETROSPECTIVEMENT : ____________
LECON APPRISE : ____________
MODIFICATION DE LA CHECKLIST NECESSAIRE ? ____________
```

### Analyse du journal — Metriques de calibration

Apres 50+ entrees, analyser les metriques suivantes :

| Metrique | Calcul | Objectif |
|---|---|---|
| **Calibration** | % de succes reel vs % estime par tranche de confiance | 70% estime -> ~70% realise |
| **Disposition ratio** | PGR / PLR | < 1.0 (idealement) |
| **Brier Score** | Moyenne de (probabilite estimee - resultat)^2 | < 0.25 |
| **Hit rate vs process quality** | Correlation entre note de process et resultat | Correlation positive attendue a long terme |
| **Biais recurrents** | Frequence de chaque biais dans les entrees post-decision | Identifier le top 3 |
| **Emotional impact** | Correlation entre etat emotionnel et qualite de decision | Idealement pas de correlation |

---

## Bayesian Updating Applique a l'Investissement

### Principe

Le theoreme de Bayes fournit un cadre formel pour mettre a jour ses croyances a la lumiere de nouvelles informations :

```
P(These | Evidence) = P(Evidence | These) * P(These) / P(Evidence)

Ou :
- P(These)          = probabilite a priori (avant la nouvelle information)
- P(Evidence|These) = vraisemblance (probabilite d'observer cette evidence si la these est vraie)
- P(Evidence)       = probabilite totale de l'evidence
- P(These|Evidence) = probabilite a posteriori (apres mise a jour)
```

### Exemple concret

**These** : "L'entreprise X va depasser ses objectifs de croissance de 20% cette annee" — probabilite a priori : 30%.

**Nouvelle information** : Le T1 montre une croissance de 25% (vs 20% attendu).

**Question bayesienne** : si l'entreprise allait effectivement depasser son objectif annuel de 20%, quelle est la probabilite d'observer un T1 a +25% ? Estimation : 60%.

**Question complementaire** : si l'entreprise n'allait PAS depasser son objectif, quelle est la probabilite d'observer un T1 a +25% quand meme (saisonnalite, one-off) ? Estimation : 20%.

**Mise a jour** :
```
P(depasse | T1 fort) = 0.60 * 0.30 / (0.60 * 0.30 + 0.20 * 0.70)
                     = 0.18 / (0.18 + 0.14)
                     = 0.18 / 0.32
                     = 0.5625 (~56%)
```

La probabilite est passee de 30% a 56%. Ce processus formel evite les biais de :
- **Base rate neglect** : ignorer la probabilite a priori (30%) et reagir excessivement a la nouvelle information.
- **Conservatism** : ne pas mettre a jour suffisamment (rester a 35% malgre une evidence forte).
- **Confirmation bias** : ne mettre a jour que quand l'evidence confirme la these.

### Implementation pratique

1. **Assigner des probabilites explicites** a chaque these d'investissement dans le journal de decisions.
2. **A chaque nouvelle information**, recalculer formellement (meme approximativement) la probabilite mise a jour.
3. **Definir des seuils d'action** : si la probabilite passe sous 30%, sortir. Si elle passe au-dessus de 70%, renforcer. Entre les deux, maintenir.
4. **Pratiquer regulierement** la mise a jour bayesienne pour developper l'intuition du calibrage probabiliste.

---

## Calibration Probabiliste — Methode de Tetlock

### Le probleme de la calibration

Philip Tetlock, dans *Superforecasting* (2015), demontre que la plupart des experts sont mal calibres : quand ils estiment un evenement a 80% probable, il se realise en realite 60% du temps. Les superforecasters sont definis par une calibration superieure.

### Exercices de calibration

1. **Trivia calibration** : repondre a 50 questions factuelles en assignant un intervalle de confiance a 90%. Si le calibrage est bon, la vraie reponse devrait etre dans l'intervalle 90% du temps. La plupart des gens n'atteignent que 50-60%.
2. **Market prediction** : predire la direction du marche a 1 semaine, 1 mois, 3 mois avec des probabilites explicites. Tracker les resultats sur un tableur. Comparer les probabilites estimees aux taux de realisation reels.
3. **Fermi estimation** : s'entrainer a estimer des grandeurs inconnues par decomposition logique pour developper la pensee quantitative.

### Amelioration de la calibration

- **Elargir les intervalles de confiance** : si vos intervalles a 90% ne contiennent la reponse que 60% du temps, elargir systematiquement (par ~50%) jusqu'a la convergence.
- **Granularite des probabilites** : utiliser des echelles fines (5% d'increment : 55%, 60%, 65%) plutot que des categories floues ("probable", "possible").
- **Inside view vs Outside view** : toujours commencer par l'outside view (base rate, classe de reference) puis ajuster avec l'inside view (specificites de la situation). La plupart des erreurs viennent d'un inside view sans outside view.
- **Update frequently** : les superforecasters mettent a jour leurs estimations frequemment et par petits increments, plutot que de s'ancrer a une estimation initiale.

---

## Synthesis — Architecture de Decision Optimale

Assembler tous les frameworks dans une architecture de decision integree :

```
ARCHITECTURE DE DECISION — FLUX COMPLET
==========================================

1. SCREENING (Systeme 1 acceptable)
   -> Filtrage rapide de l'univers d'investissement
   -> Heuristiques simples (secteur, taille, liquidite)

2. ANALYSE (Systeme 2 obligatoire)
   -> Valorisation quantitative (DCF, multiples)
   -> Analyse qualitative (moat, management, secteur)
   -> Assignation d'une probabilite a priori (Bayes)

3. CHALLENGE (Anti-biais)
   -> Steel-man de la these contraire
   -> Pre-mortem pour positions significatives
   -> Verification de l'etat emotionnel

4. DECISION (Checklist)
   -> Pre-trade checklist complete
   -> Journal de decision pre-rempli
   -> Sizing et risk management

5. EXECUTION (Mecanique)
   -> Ordres pre-definis (entree, stop, objectif)
   -> Pas de modification sans nouvelle analyse

6. SUIVI (Bayesian updating)
   -> Mise a jour des probabilites a chaque nouvelle info
   -> Regles de sortie si seuils franchis

7. POST-MORTEM (Apprentissage)
   -> Journal de decision complete
   -> Analyse process quality vs outcome
   -> Mise a jour de la checklist si necessaire
```
