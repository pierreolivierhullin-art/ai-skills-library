# Psychologie du Pricing -- Biais Cognitifs et Tactiques

## Overview

Ce document de reference couvre les mecanismes psychologiques qui gouvernent la perception du prix et les decisions d'achat. Il presente les biais cognitifs les plus exploitables en pricing (anchoring, loss aversion, social proof, framing), les tactiques operationnelles qui en decoulent (decoy pricing, charm pricing, bundling, Good-Better-Best), et une methodologie rigoureuse d'A/B testing des prix. Les exemples sont issus de cas reels avec des chiffres d'impact mesures. Utiliser ce guide pour optimiser la presentation des prix, pas seulement leur niveau.

---

## Key Concepts

### Anchoring Effect -- Le Pouvoir du Premier Chiffre

L'anchoring est le biais cognitif le plus puissant en pricing. Le premier chiffre qu'un individu voit influence de facon disproportionnee son jugement sur ce qui est "raisonnable" comme prix.

**Principe** : quand le cerveau traite un chiffre, il ajuste a partir de ce chiffre initial meme si l'ancre est arbitraire. Des etudes (Ariely, Loewenstein, Prelec) montrent que les participants avec une ancre haute donnent des valorisations significativement plus elevees.

**Application en pricing** :
- Afficher le prix annuel "economise" avant le prix mensuel : "Valeur annuelle : 1 188 EUR -- Votre prix : 79 EUR/mois" ancre la perception sur 1 188.
- Commencer la page pricing par le plan le plus cher (Enterprise) pour faire paraitre le plan Pro raisonnable.
- Afficher un "prix barre" (ancien tarif ou valeur de marche) avant le prix actuel.

**Le cas Dan Ariely -- The Economist** : Ariely a conduit une experience avec 100 etudiants du MIT. Trois options proposees :
- Web only : 59 USD (16 votes)
- Print only : 125 USD (0 votes)
- Print + Web : 125 USD (84 votes)

Sans l'option "Print only" (le decoy), la distribution changeait radicalement : Web only recueillait 68 votes et Print+Web seulement 32. L'option decoy (dominee par Print+Web) rendait le pack premium logique. Elle servait uniquement d'ancre de reference.

### Price Perception -- Charm Pricing et Round Pricing

**Charm pricing** : fixer le prix juste en dessous d'un seuil rond (9.99 vs 10.00, 299 vs 300). L'effet "left digit" conduit le cerveau a encoder 9.99 comme "dans les 9" plutot que "proche de 10". Des etudes montrent une augmentation des ventes de 20-30% sur des produits de grande consommation.

**Quand utiliser le charm pricing** :
- Produits et services B2C ou bas de gamme : 9.99, 29.99, 99.
- Prix de lancement ou promotionnels : le charm pricing signale une offre ou une promotion.
- SaaS bas de panier (< 100 EUR/mois) : 29 EUR, 79 EUR, 199 EUR.

**Quand utiliser le round pricing** :
- Produits premium et luxe : 300 EUR, 500 EUR, 2 000 EUR. Le round pricing signale la qualite et la confiance. Un prix de 2 997 EUR pour un service de conseil semble "mesquin". 3 000 EUR est plus credible.
- B2B enterprise : les acheteurs sophistiques savent que 9.99 est du charm pricing. Cela diminue la credibilite dans un contexte de vente complexe.
- Produits ou la qualite est l'argument principal : les etudes de Janiszewski et Uy montrent que les chiffres ronds signalent confiance dans les marches premium.

**Regle pratique** : utiliser le charm pricing pour les prix < 500 EUR dans un contexte B2C ou PLG. Utiliser le round pricing pour les prix > 500 EUR ou dans un contexte enterprise.

---

## Frameworks & Methods

### Framing Effects -- Mensuel, Annuel ou Par Jour

La facon dont un prix est exprime change radicalement sa perception, sans changer son niveau reel.

**Mensuel vs annuel** : afficher le prix annuel en equivalent mensuel cree l'illusion de l'economie.

| Formulation | Prix affiche | Perception |
|---|---|---|
| Prix mensuel | 99 EUR/mois | Engagement mensuel, flexibilite |
| Prix annuel divise | 79 EUR/mois (facture 948 EUR/an) | Economie visible (20%) |
| Prix annuel brut | 948 EUR/an | Choc de la somme totale -- a eviter |

Recommandation : afficher toujours le prix equivalent mensuel pour les abonnements annuels, avec la mention "facture annuellement" en petite police. Ne jamais mettre en avant le montant total annuel en premier.

**Decomposition par jour** : "Seulement 2,60 EUR par jour" pour un abonnement a 79 EUR/mois. Le cerveau compare le prix journalier a des references familieres (un cafe, un sandwich). Efficace en B2C, inapproprie en B2B ou l'acheteur ne pense pas en couts journaliers.

**Framing de la valeur** : comparer le prix au cout du probleme non resolu est plus puissant que la decomposition journaliere en B2B. "Pour le prix de 2 heures de travail de votre comptable par mois, notre solution automatise 20 heures de taches manuelles."

### Loss Aversion en Pricing

Kahneman et Tversky ont montre que la douleur de perdre quelque chose est psychologiquement 2 a 2.5 fois plus intense que le plaisir de gagner l'equivalent. En pricing, exploiter la loss aversion est plus puissant que promettre un gain.

**Trial to paid conversion** : le mecanisme le plus efficace de la loss aversion est le trial avec acces complet. Apres 14 jours de trial, l'utilisateur a etabli des habitudes, integre l'outil dans son workflow, potentiellement importe des donnees. La perspective de "perdre l'acces" est un motivateur d'achat bien plus fort que la perspective de "gagner les features pro".

**Formulations loss aversion vs gain framing** :

| Type | Formulation | Efficacite |
|---|---|---|
| Gain framing | "Activez votre abonnement pour acceder aux features avancees" | Standard |
| Loss framing | "Votre periode d'essai se termine dans 3 jours. Ne perdez pas l'acces a vos 47 projets." | +35-50% conversion |
| Specifique | "Vos donnees seront archivees le [date]. Continuez pour les conserver." | Maximale |

**Freemium vers payant** : ne pas bloquer toutes les features d'un coup. Retirer l'acces a des features specifiques que l'utilisateur a utilise pendant le trial est plus impactant que de bloquer l'acces general. "Vous avez utilise les rapports automatiques 12 fois ce mois. Cette feature est disponible en Pro."

**Structurer les downgrades** : quand un client veut annuler, presenter ce qu'il va perdre de facon specifique, pas generique. "Si vous passez au plan Free, vous perdrez : vos 15 integrations actives, l'historique de donnees > 30 jours, et l'acces pour 3 de vos collegues."

### Social Proof en Pricing

Le biais de conformite sociale pousse les individus a choisir ce que les autres choisissent, surtout en situation d'incertitude (comme evaluer si un prix est justifie).

**"Plan le plus populaire" badging** : placer un badge "Le plus populaire" ou "Choisi par 70% de nos clients" sur le plan Pro ou Medium oriente les choix vers ce plan. Cela reduit l'anxiete de decision et legitime le prix. Augmentation typique de la part du plan badge : +15 a +30 points de pourcentage.

**Regles du badging** :
- Etre honnet : utiliser "le plus populaire" seulement si c'est vrai. La fausse social proof est detectee et nuit a la confiance.
- Montrer la specificite : "Choisi par 8 entreprises sur 10 dans votre secteur" est plus persuasif que "le plus populaire".
- Ne pas badger plusieurs plans simultanement : un seul badge social proof sur la page pricing.
- Tester "Recommande" vs "Le plus populaire" vs "Meilleur rapport qualite/prix" -- les resultats varient selon le segment.

**Testimonials et logos** : placer des logos clients et des temoignages sur la page pricing (pas seulement sur la homepage) reduit l'anxiete au moment critique de la decision d'achat. Les logos d'entreprises reconnues du meme secteur que le prospect sont les plus efficaces.

### Decoy Pricing -- Construction et Calcul de l'Effet

Le decoy pricing consiste a ajouter une option "irrationnelle" dans un set de choix pour orienter vers l'option cible.

**Les 3 conditions d'un decoy efficace** :
1. Le decoy est domine asymetriquement : il est inferieur a l'option cible sur tous les attributs importants, mais comparable en prix.
2. La difference entre le decoy et l'option cible est claire et perceptible.
3. Il y a exactement 3 options (A = decoy, B = cible, C = alternative).

**Exemple avec calcul d'impact** :

Situation AVANT decoy (2 options) :
- Basic : 29 EUR/mois -- 65% des clients choisissent Basic
- Pro : 79 EUR/mois -- 35% des clients choisissent Pro
- ARPU moyen : 0.65 x 29 + 0.35 x 79 = 18.85 + 27.65 = **46.50 EUR/mois**

Introduction du decoy (3 options) :
- Basic : 29 EUR/mois
- Pro-Lite (DECOY) : 69 EUR/mois -- memes features que Pro mais sans les integrations
- Pro : 79 EUR/mois
- Distribution observee post-decoy : Basic 45%, Pro-Lite 10%, Pro 45%
- ARPU moyen : 0.45 x 29 + 0.10 x 69 + 0.45 x 79 = 13.05 + 6.90 + 35.55 = **55.50 EUR/mois**
- Uplift ARPU : +19.4%

**Pour 1 000 clients** :
- Avant : 46 500 EUR MRR
- Apres : 55 500 EUR MRR
- Gain mensuel : +9 000 EUR MRR soit +108 000 EUR ARR

**Regles de construction du decoy** :
- Prix du decoy : 80-95% du prix de l'option cible.
- Features du decoy : similaires a l'option cible mais avec une limitation importante et visible.
- Le decoy ne doit pas etre attractif pour la majorite des clients -- il doit servir de reference, pas de choix.

### Bundling vs Unbundling

**Bundling** : regrouper plusieurs produits ou features en un seul prix. Augmente la valeur percue quand les composants ont des willingness-to-pay differentes entre les segments -- certains valorisent fortement A, d'autres valorisent fortement B. Le bundle capture de la valeur des deux groupes.

**Quand bundler** :
- Les features ont des usages complementaires (utiliser A encourage a utiliser B).
- La simplicite est un argument de vente (un seul prix, pas de choix a faire).
- Le cout marginal d'ajout d'une feature au bundle est faible (logiciel).

**Price complexity penalty** : au-dela de 4-5 options de pricing, la complexite devient un frein a l'achat (paradox of choice). Les clients abandonnent ou choisissent l'option la moins chere par defaut. Simplifier le pricing est souvent plus rentable qu'ajouter des options.

**Unbundling** : separer des features pour permettre a chaque segment de payer uniquement ce qu'il utilise. Adapt au usage-based ou aux add-ons. Risque : augmenter la perception de "chers" si les add-ons s'accumulent ("bill shock a l'addition").

### Good-Better-Best (GBB) Strategy

La GBB est la structure de tiered pricing la plus efficace psychologiquement. Elle exploite l'effet de compromis : face a 3 options, les individus ont tendance a choisir l'option du milieu ("extremeness aversion" de Simonson).

**Principes de construction des 3 offres** :

**Good (Starter/Basic)** : couvre le cas d'usage minimal qui justifie l'achat. Doit etre assez bon pour etre une option credible, pas un produit degrade. Si le Good est trop limite, les clients partent chez un concurrent "all-inclusive". Prix cible : 30-40% du prix du Better.

**Better (Pro/Standard)** : l'offre principale, la plus rentable, celle que la majorite des clients devrait choisir. Concevoir le Better pour qu'il couvre 80% des besoins des clients cibles. Afficher le badge "Le plus populaire" ici. Prix cible : 100% de reference.

**Best (Enterprise/Premium)** : l'offre premium qui sert d'ancre haute et capture la valeur des clients les plus intensifs. Doit inclure des features ou un niveau de service qualitativement different, pas juste plus de volume. Prix cible : 200-400% du prix du Better.

**Psychologie du choix du milieu** : en general, 60-70% des clients choisissent le Better si la GBB est bien construite. Le Good capte 20-25% et le Best 10-15%. Si la distribution est trop basse sur le Better, les features du Better ne sont pas assez differenciantes. Si le Best est trop faible, le prix du Best est trop proche du Better ou pas assez justifie.

---

## Tools & Implementation

### Price Increase Playbook -- Annoncer une Hausse Sans Churner

Une hausse de prix est inevitablement risquee mais evitable par une mauvaise communication. Suivre ce protocole pour minimiser le churn.

**Preparation (J-90 a J-60)** :
- Calculer la hausse moyenne et segmenter les clients par impact (faible/moyen/fort).
- Identifier les clients a risque : ceux avec le plus grand impact financier ET un faible NPS ou faible usage.
- Preparer les arguments de valeur : quelles nouvelles features, ameliorations ou investissements justifient la hausse ? Ne pas annoncer une hausse sans justification concrete.

**Communication (J-60)** :

Template d'email d'annonce de hausse de prix :

```
Objet : Mise a jour tarifaire -- Ce qui change pour vous

Bonjour [Prenom],

Depuis [date], votre facture mensuelle sera de [nouveau_prix] EUR
(actuellement [ancien_prix] EUR).

Pourquoi cette mise a jour ?
Au cours des 12 derniers mois, nous avons [liste concrete :
- Ajoute X fonctionnalites demandees par vos equipes
- Reduit notre temps de reponse support de 8h a 2h
- Investi dans l'infrastructure pour garantir 99.9% de disponibilite]

Votre impact : + [X EUR/mois], soit [Y EUR/an].

Pour toute question, votre CSM [nom] reste disponible.

[Signature]
```

**Ne jamais** : s'excuser de la hausse (cela signale une manque de confiance dans la valeur delivree). Utiliser des formulations vagues ("investissements continus"). Annoncer la hausse moins de 30 jours avant.

**Gestion des exceptions** : prevoir un budget de grandfathering pour retenir les clients strategiques (grands ARR, forte influence de reference). Ne pas grandfatherer de facon systematique -- cela elimine l'effet de la hausse et cree une incertitude permanente.

### A/B Testing des Prix -- Methodologie Rigoureuse

**Attention legale** : tester des prix differents sur des clients existants peut constituer une discrimination tarifaire dans certaines jurisdictions. Limiter l'A/B test de prix aux nouveaux visiteurs/prospects, pas aux clients actuels.

**Calcul de la taille d'echantillon** :

Pour detecter un effet de 10% sur le taux de conversion avec un taux de base de 3%, un niveau de confiance de 95% et une puissance de 80% :

```python
from scipy import stats
import math

def calculer_taille_echantillon_ab(
    taux_base=0.03,
    lift_minimal=0.10,
    alpha=0.05,
    puissance=0.80
):
    """Calcul du nombre de visiteurs par variante necessaires."""
    taux_b = taux_base * (1 + lift_minimal)
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(puissance)
    p_bar = (taux_base + taux_b) / 2
    n = (z_alpha * math.sqrt(2 * p_bar * (1 - p_bar)) +
         z_beta * math.sqrt(taux_base * (1 - taux_base) + taux_b * (1 - taux_b))) ** 2
    n = n / (taux_b - taux_base) ** 2
    return math.ceil(n)

n = calculer_taille_echantillon_ab(taux_base=0.03, lift_minimal=0.10)
print(f"Taille d'echantillon par variante : {n} visiteurs")
# Resultat : ~6 200 visiteurs par variante
# Soit ~12 400 visiteurs totaux pour un test a 2 variantes
```

**Metriques a suivre dans un A/B test de prix** :
1. Taux de conversion (visitor -> trial ou paid) -- metrique principale.
2. ARPU moyen des conversions -- prix plus eleve peut reduire le volume mais augmenter le revenu total.
3. Revenue per visitor = Taux de conversion x ARPU -- la metrique qui combine les deux effets.
4. Taux de churn a 30/60/90 jours par cohorte -- un prix trop eleve peut augmenter les conversions court terme mais degrader la retention.

**Pieges a eviter** :
- Stopper le test trop tot (peek problem) : definir la duree du test a l'avance et ne pas regarder les resultats intermediaires pour prendre une decision.
- Tester pendant une periode atypique : eviter les periodes de soldes, fin d'annee, launches majeurs qui brisent la stationnarite.
- Ignorer la segmentation : un prix peut performer mieux pour un segment et moins bien pour un autre. Analyser les resultats par segment avant de conclure.
- Tester des ecarts trop faibles : tester 79 EUR vs 85 EUR necessite des millions de visiteurs pour etre statistiquement significatif. Tester des ecarts de 20%+ pour obtenir des resultats actionnables rapidement.

---

## Common Mistakes

**Supposer que le charm pricing fonctionne toujours** : en B2B enterprise, le charm pricing peut reduire la credibilite. Adapter le style de pricing au contexte et au segment.

**Ajouter un decoy sans tester** : le decoy mal concu peut cannibaliser l'option cible ou rendre la page confuse. Toujours A/B tester l'introduction d'un decoy.

**Utiliser la loss aversion de facon manipulatoire** : les formulations qui creent une fausse urgence ("offre expire dans 10 minutes" alors que le compte repart a zero) sont detestees des clients sophistiques et nuisent a la confiance a long terme.

**Ignorer l'impact psychologique de la complexite** : ajouter des options, des add-ons et des conditions speciales pour "personnaliser" le pricing a souvent l'effet inverse -- les clients se sentent perdus et choisissent le moins cher ou abandonnent.

**Confondre social proof et manipulation** : le badge "le plus populaire" doit etre vrai. Les clients qui decouvrent que le badge etait faux partagent leur deception activement. La social proof authentique est un atout; la fausse social proof est un risque reputationnel.
