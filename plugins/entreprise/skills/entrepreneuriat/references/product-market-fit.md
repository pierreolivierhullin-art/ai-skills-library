# Product-Market Fit -- Mesure, Signaux et Pivot

Reference operationnelle sur la mesure et l'atteinte du Product-Market Fit. Couvre les definitions de reference (Andreessen, Ellis, Blank), les methodes de mesure (test Ellis, NPS, retention curves), la methode Superhuman, les signaux specifiques au B2B, la decision pivot/persevere et les metriques quantitatives critiques. Utiliser ce document comme guide de diagnostic du PMF a chaque etape du developpement produit.

---

## Definition du PMF -- Trois Perspectives de Reference

### Marc Andreessen (2007) -- La Definition Originale

"Le product-market fit signifie etre dans un bon marche avec un produit capable de satisfaire ce marche."

Andreessen insiste sur la notion de **marche** comme variable primaire. Un bon produit dans un mauvais marche echoue. Un produit mediocre dans un marche exceptionnel peut reussir. Le marche tire le produit vers le haut quand le PMF est atteint -- les clients viennent d'eux-memes, le bouche-a-oreille s'emballe, les commerciaux ne peuvent pas repondre a toutes les demandes.

**Implication pratique** : avant d'optimiser le produit, valider que le marche est suffisamment grand et que le probleme est suffisamment douloureux. Un produit excellent dans un marche inexistant ou trop petit ne produira jamais de PMF.

### Sean Ellis (2008-2010) -- La Mesure Operationnelle

Sean Ellis (Dropbox, Eventbrite, LogMeIn) a propose la mesure la plus operationnelle du PMF : le test de la deception.

**Question unique** : "Comment vous sentiriez-vous si vous ne pouviez plus utiliser [produit] ?"

Reponses possibles :
- Tres decu
- Plutot decu
- Pas vraiment decu (le produit ne m'est pas indispensable)
- Sans objet (j'ai arrete de l'utiliser)

**Seuil PMF** : si >= 40% des utilisateurs actifs repondent "tres decu", le produit a atteint (ou est proche d') un PMF suffisant pour scaler.

**Conditions d'application du test Ellis :**
- Sonder uniquement les utilisateurs **actifs** (ceux qui ont utilise le produit au moins 2 fois dans les 2 derniers mois)
- Exclure les early adopters trop indulgents (les premiers 10-20% qui essaient tout)
- Taille minimale : 40-50 reponses pour une significativite acceptable
- Format : survey anonyme, pas d'interview directe (biais de politesse)
- Frequence : tous les trimestres, ou apres chaque iteration majeure du produit

**Interpreter les resultats en dessous de 40% :**
- 25-35% : signal prometteur, le PMF est possible. Analyser le segment "tres decu" -- qui sont-ils ? Quelles features utilisent-ils ? Concentrer le developpement sur ce sous-segment.
- 15-25% : probleme significatif. Retourner aux entretiens clients pour comprendre ce qui manque.
- < 15% : probleme fondamental. Envisager un pivot de segment ou de proposition de valeur.

### Steve Blank -- Le PMF comme Processus de Discovery

Steve Blank (The Startup Owner's Manual) definit le PMF comme l'aboutissement du Customer Development process : le moment ou l'entreprise a valide que le segment cible a un probleme, que la solution resout ce probleme, et que les clients sont prets a payer un prix qui rend le modele economique viable.

**Blank insiste sur la sequence** :
1. Customer Discovery : valider le probleme et le segment (pas encore de produit)
2. Customer Validation : valider la solution et le modele de revenus (MVP, premiers clients)
3. Customer Creation : scaler l'acquisition (post-PMF)
4. Company Building : construire l'organisation (echelle)

**Erreur commune** : passer a l'etape 3 (customer creation, scaler) avant d'avoir valide les etapes 1 et 2. C'est la cause principale des echecs post-Serie A.

---

## Le Test Sean Ellis -- Guide d'Application

### Implementation du Survey

**Outil recommande** : Typeform, Google Forms, ou Delighted. Simple et court.

```
Questions du survey PMF (dans l'ordre) :

1. Comment vous sentiriez-vous si vous ne pouviez plus utiliser [Produit] ?
   O Tres decu
   O Plutot decu
   O Pas vraiment decu
   O Je n'utilise plus [Produit]

2. [Si "Tres decu" ou "Plutot decu"]
   Quel type de personnes beneficierait le plus de [Produit] ?
   [Reponse libre -- identifier les personas les plus engages]

3. [Si "Tres decu" ou "Plutot decu"]
   Quel est le principal benefice que vous retirez de [Produit] ?
   [Reponse libre -- identifier la proposition de valeur percue]

4. [Si "Pas vraiment decu" ou "Je n'utilise plus"]
   Qu'est-ce qui vous manque dans [Produit] actuellement ?
   [Reponse libre -- identifier les lacunes cles]

5. Comment pourrait-on ameliorer [Produit] pour mieux repondre a vos besoins ?
   [Reponse libre]
```

### Analyse et Action

**Etape 1 : Calculer le score global**
Pourcentage de "tres decu" sur le total des repondants (hors "n'utilise plus").

**Etape 2 : Segmenter les "tres decu"**
Qui sont-ils ? Firmographics (taille, secteur, role), comportements d'usage (features utilisees, frequence), canaux d'acquisition. Ce profil est l'ICP le plus affile.

**Etape 3 : Analyser le benefice percu**
Quels mots utilisent-ils pour decrire le benefice principal ? Ce verbatim est le meilleur messaging possible -- utiliser leurs mots exactement dans les landing pages et les emails.

**Etape 4 : Comprendre les "pas vraiment decu"**
Qu'est-ce qui les empeche d'etre "tres decu" ? Y a-t-il une feature manquante critique ? Un probleme d'onboarding ? Un segment non pertinent (faux positifs dans l'acquisition) ?

**Etape 5 : Definir les actions prioritaires**
Si score < 40% : identifier les features utilisees par les "tres decu" et les mettre en avant pour les autres segments. Reduire la friction vers ces features dans l'onboarding.

---

## NPS comme Proxy du PMF -- Limites et Usage

### Net Promoter Score : definition et calcul

```
NPS = % Promoteurs (note 9-10) - % Detracteurs (note 0-6)
```

Question : "Sur une echelle de 0 a 10, quelle est la probabilite que vous recommandiez [Produit] a un collegue ou ami ?"

### Benchmarks NPS par industrie (B2B SaaS)

| Score NPS | Interpretation | Benchmark sectoriel SaaS |
|---|---|---|
| > 50 | Excellent, fort PMF signal | > 50 = top 10% SaaS |
| 30-50 | Bon, PMF probable | 30-50 = bon |
| 10-30 | Moyen, PMF incertain | Mediane SaaS |
| 0-10 | Faible, PMF absent | Signal d'alarme |
| < 0 | Critique | Abandon ou pivot necessaire |

**NPS benchmarks par categorie :**
- CRM & Sales Tools : NPS moyen ~32
- Outils de collaboration : NPS moyen ~45
- Outils de gestion de projet : NPS moyen ~38
- Plateformes marketing : NPS moyen ~28
- Outils RH : NPS moyen ~22

### Limites du NPS comme mesure de PMF

**Limite 1 : Le NPS mesure l'intention, pas le comportement.** Un utilisateur peut dire qu'il recommanderait le produit sans jamais le faire. La retention et le referral reel sont de meilleurs signaux que le NPS.

**Limite 2 : Le NPS est influence par le recours recent.** Un utilisateur qui a eu une mauvaise experience recente donnera un score bas meme si l'experience globale est positive. Contextualiser le NPS avec la date du dernier contact.

**Limite 3 : Le NPS ne capture pas le "pourquoi".** Toujours accompagner la question NPS d'une question ouverte : "Quelle est la raison principale de votre note ?" Le verbatim est plus instructif que le score.

**Limite 4 : Le NPS varie selon la methode de distribution.** Email in-app vs email external vs entretien telephonique produisent des scores differents. Standardiser la methode.

**Recommandation** : utiliser le NPS comme indicateur de tendance (est-il en hausse ou en baisse sur les 3 derniers mois ?) plutot que comme mesure absolue du PMF.

---

## Retention -- Le Signal Primaire du PMF

### Pourquoi la retention est superieure au NPS et au test Ellis

La retention est le comportement observable, pas l'intention declaree. Un utilisateur retenu paie, utilise et potentiellement recommande le produit. Un utilisateur churne est un vote negatif definitif. La retention est la metrique la plus difficile a manipuler et la plus predictive du succes a long terme.

**Principe fondamental** : si la retention est forte, tous les autres problemes (acquisition, monetisation) sont solubles avec du temps et de l'argent. Si la retention est faible, aucune quantite d'acquisition ne compense le churn -- c'est le tonneau des Danaides.

### Courbes de Retention -- Lecture et Interpretation

**Construction d'une courbe de retention par cohorte :**

```
% utilisateurs actifs
100% |*
     | *
 80% |  *
     |   *
 60% |    *
     |     * *
 40% |        * * *
     |              * * * * * (stabilisation = PMF)
 20% |
     |_______________________________________
     D1  D7  D14  D30  D60  D90  D180   Jours
```

**Lecture des 3 profils de courbe :**

| Profil | Signal | Interpretation |
|---|---|---|
| **Courbe qui s'aplatit** (asymptote positive) | PMF probable | Le produit a un coeur d'utilisateurs fideles. Scaler. |
| **Courbe qui tend vers 0** | Absence de PMF | Le produit ne retient pas. Pivoter avant de scaler. |
| **Courbe en smile** (remonte apres une chute) | PMF sur un sous-segment | Identifier qui revient et pourquoi. Focaliser. |

### Benchmarks de Retention par Categorie

| Categorie | D1 retention | D7 retention | D30 retention | D90 retention |
|---|---|---|---|---|
| **Consumer mobile (quotidien)** | > 60% | > 35% | > 20% | > 12% |
| **Consumer mobile (hebdo)** | > 40% | > 20% | > 12% | > 8% |
| **SaaS B2B (quotidien)** | > 70% | > 50% | > 40% | > 35% |
| **SaaS B2B (hebdo/mensuel)** | > 50% | > 35% | > 25% | > 20% |
| **E-commerce** | > 30% | > 15% | > 8% | > 5% |

**DAU/MAU Ratio** : mesure l'engagement quotidien rapporte a l'engagement mensuel.
- > 50% : outil quotidien critique (Slack, Gmail) -- PMF fort
- 25-50% : outil frequent -- PMF probable
- 10-25% : usage irregulier -- signal mixte
- < 10% : usage rare -- absence de PMF ou usage hebdomadaire naturel

### Triangle de Retention (Reforge Framework)

Le triangle de retention (Casey Winters, Brian Balfour -- Reforge) decompose la retention en trois dimensions :

**1. New User Retention** : comment bien on onboarde les nouveaux utilisateurs vers le "aha moment"
**2. Current User Retention** : comment bien on engage les utilisateurs actifs existants (habit loops, nouvelles features)
**3. Resurrected User Retention** : comment bien on re-engage les utilisateurs dormants (re-engagement emails, notifications)

Ameliorer chacune de ces dimensions a un impact different selon le stade :
- Pre-PMF : focaliser sur New User Retention (onboarding vers le aha moment)
- Post-PMF : focaliser sur Current User Retention (approfondissement de l'engagement)
- Scale : focaliser sur Resurrected User Retention (maximiser le LTV)

---

## Methode Superhuman -- Le PMF Score Avance

Rahul Vohra (CEO Superhuman) a publie en 2018 la methodologie la plus detaillee pour mesurer et ameliorer le PMF progressivement.

### Les 4 Etapes de la Methode Superhuman

**Etape 1 : Implementer le survey Sean Ellis**
Poser la question "tres decu" a tous les utilisateurs actifs. Collecter egalement : personas, features principales utilisees, benefice percu.

**Etape 2 : Segmenter les reponses par persona**
Le score global peut etre trompeur. Decomposer le score par segment (industrie, taille d'entreprise, role, cas d'usage). Il est possible qu'un segment specifique soit a 60% et un autre a 15%.

**Etape 3 : Identifier les "very disappointed" et ignorer les autres**
Analyser exclusivement les utilisateurs qui repondent "tres decu" :
- Quels benefices decrivent-ils ?
- Quelles features utilisent-ils le plus ?
- Quel vocabulaire emploient-ils pour decrire le probleme resolu ?

Ce groupe est le vrai PMF signal. Construire le produit pour maximiser ce groupe, pas pour satisfaire tout le monde.

**Etape 4 : Double down sur les "very disappointed"**
Concentrer le roadmap sur les features valorisees par les "tres decu". Concentrer l'acquisition sur les canaux qui amenent des profils similaires. Accepter de sacrifier les fonctionnalites qui plaisent aux "plutot decu" mais pas aux "tres decu".

**Resultat Superhuman** : en appliquant cette methodologie sur 6 mois, Superhuman a fait passer son score PMF de 22% a 58%.

---

## PMF dans le B2B -- Signaux Differents

### Pourquoi le PMF B2B se mesure differemment

Dans le B2B, les utilisateurs sont rarement les acheteurs. La retention est souvent contractuelle (engagement annuel). Le "very disappointed" peut etre rare car l'utilisateur n'a pas le choix (outil impose par l'employeur). Utiliser des signaux complementaires.

**Signaux PMF specifiques B2B :**

| Signal | Description | Seuil PMF |
|---|---|---|
| **NRR (Net Revenue Retention)** | MRR fin de periode / MRR debut + expansion - churn | > 100% (> 110% = fort PMF) |
| **Renouvellements spontanes** | Clients qui renouvellent sans relance commerciale | > 80% des renouvellements |
| **Expansion revenue** | Upsell et cross-sell generes organiquement | > 30% du nouveau MRR |
| **Referrals B2B** | Clients qui recommandent activement (sans incitation) | > 20% de l'acquisition |
| **Usage expansion** | Clients qui ajoutent des sieges, des modules ou des utilisateurs | Croissance du compte > 20%/an |
| **Churn volontaire vs involontaire** | % de churn du au produit vs raisons externes | Churn volontaire < 5%/an |

### Calcul du NRR

```
NRR = (MRR debut de periode + Expansion MRR - Contraction MRR - Churn MRR)
       / MRR debut de periode x 100

Exemple :
- MRR debut janvier : 100 000 EUR
- Expansion (upsell, nouveaux sieges) : + 15 000 EUR
- Contraction (downsell) : - 5 000 EUR
- Churn (annulations) : - 8 000 EUR
- MRR fin janvier : 102 000 EUR

NRR = (100 000 + 15 000 - 5 000 - 8 000) / 100 000 = 102%
```

NRR > 100% signifie que les revenus des clients existants croissent -- meme sans nouveaux clients. C'est le signe le plus fort du PMF en B2B.

---

## Pivot vs Persevere -- Framework de Decision

### La Question la Plus Difficile de l'Entrepreneuriat

Le pivot est l'une des decisions les plus difficiles : pivoter trop tot sacrifie une strategie qui aurait pu fonctionner avec plus de temps. Pivoter trop tard gaspille des mois sur une strategie condamnee. Utiliser ce framework de decision structure.

### Les 5 Signaux qui Indiquent un Pivot Necessaire

| Signal | Description | Action recommandee |
|---|---|---|
| **Retention nulle apres 90 jours** | Les utilisateurs essaient et n'utilisent plus | Entretiens "churn" pour comprendre pourquoi |
| **Pas de referrals malgre la satisfaction** | Les clients sont "satisfaits" mais ne recommandent pas | Le PMF est insuffisant -- la valeur n'est pas assez forte |
| **Coût d'acquisition inexorablement croissant** | Chaque nouveau client coute de plus en plus cher | Le marche adressable est epuise ou mal cible |
| **Conversion tres faible malgre beaucoup d'efforts** | < 1% de taux de conversion après > 100 demos | Probleme de proposition de valeur ou de segment |
| **Les clients n'utilisent pas le coeur du produit** | Ils utilisent le produit pour autre chose que prevu | Possibilite de pivot vers cet autre usage |

### Les 5 Faux Signes de PMF (Pieges)

**Faux signe 1 : L'enthousiasme des early adopters**
Les premiers utilisateurs sont souvent des innovateurs qui adorent tout ce qui est nouveau. Leur enthousiasme ne predis pas l'adoption par la majorite. Tester avec des utilisateurs "mainstream" (pragmatiques), pas seulement des passionnes de technologie.

**Faux signe 2 : Un gros client qui s'est engage**
Un contrat enterprise de 100 000 EUR n'est pas un PMF. C'est peut-etre un contrat sur-mesure, une relation personnelle, ou un besoin unique. Le PMF demande la repetabilite et la generalisation.

**Faux signe 3 : La croissance court terme dopee par la pub**
Une croissance forte avec des depenses publicitaires elevees peut masquer un taux de retention desastreux. Mesurer la retention des cohortes d'acquisition payante -- si elles churnent a 80% dans les 30 jours, la publicite ne fait que retarder l'inevitable.

**Faux signe 4 : Des metriques de vanite en hausse**
Utilisateurs inscrits, downloads, page views -- ces metriques ne disent rien sur la valeur creee. Focaliser sur les metriques d'engagement et de retention.

**Faux signe 5 : La confirmation des fondateurs**
Les fondateurs ont un biais naturel vers la confirmation que leur produit fonctionne. Chercher activement les signaux negatifs. Interviewer les churns, les prospects qui ont dit non, les utilisateurs inactifs.

### Types de Pivots (Steve Blank & Eric Ries)

| Type de pivot | Definition | Quand l'utiliser |
|---|---|---|
| **Customer segment pivot** | Meme produit, autre segment client | Le produit a de la valeur mais pas pour le segment initial |
| **Problem pivot** | Meme segment, autre probleme a resoudre | Le segment est bon mais le probleme resolu n'est pas assez douloureux |
| **Solution pivot** | Meme probleme et segment, autre approche technique | La solution actuelle ne resout pas le probleme efficacement |
| **Channel pivot** | Meme produit, autre canal de distribution | Le canal actuel ne genere pas de ROI |
| **Revenue model pivot** | Meme produit et segment, autre modele de monetisation | Le modele de prix ne correspond pas au comportement d'achat |
| **Technology pivot** | Meme probleme, nouvelle technologie | Une nouvelle technologie permet de resoudre le probleme mieux et moins cher |

**Processus de decision pivot :**
1. Quantifier les signaux negatifs (retention, conversion, entretiens)
2. Identifier l'hypothese qui a echoue (segment, probleme, solution, canal ?)
3. Evaluer le cout du pivot (ressources, temps, equipe)
4. Definir le prochain test minimal pour valider la nouvelle direction
5. Fixer une deadline claire pour evaluer les resultats du pivot

---

## Mesure Quantitative du PMF -- Tableau de Bord

### Les 5 Metriques Critiques

```python
# Calcul de la courbe de retention depuis des donnees brutes
# Input : dataframe avec colonnes [user_id, event_date]

import pandas as pd
import numpy as np

def calculate_retention(df, cohort_col='signup_date', event_col='activity_date', user_col='user_id'):
    """
    Calcule la retention par cohorte d'inscription.

    Retourne un dataframe avec :
    - Lignes : cohortes (mois d'inscription)
    - Colonnes : periodes (M0, M1, M2, ...)
    - Valeurs : % d'utilisateurs actifs par periode
    """
    # Formater les dates en mois
    df['cohort_month'] = pd.to_datetime(df[cohort_col]).dt.to_period('M')
    df['activity_month'] = pd.to_datetime(df[event_col]).dt.to_period('M')

    # Calculer la periode relative (M0 = mois d'inscription)
    df['period'] = (df['activity_month'] - df['cohort_month']).apply(lambda x: x.n)

    # Taille de chaque cohorte
    cohort_sizes = df.groupby('cohort_month')[user_col].nunique()

    # Utilisateurs actifs par cohorte et periode
    cohort_activity = df.groupby(['cohort_month', 'period'])[user_col].nunique().reset_index()
    cohort_activity = cohort_activity.pivot(index='cohort_month', columns='period', values=user_col)

    # Calculer le taux de retention
    retention = cohort_activity.divide(cohort_sizes, axis=0) * 100

    return retention.round(1)

# Usage : retention_matrix = calculate_retention(pd.read_csv('user_events.csv'))
```

### Dashboard PMF -- Metriques Hebdomadaires

| Metrique | Definition | Mesure | Seuil Alarme | Seuil PMF |
|---|---|---|---|---|
| **Test Ellis** | % "tres decu" | Mensuel | < 20% | > 40% |
| **D30 Retention** | % actifs a 30 jours | Cohorte hebdo | < 15% | > 30% |
| **DAU/MAU** | Engagement quotidien | Quotidien | < 10% | > 25% |
| **NRR** (B2B) | Net Revenue Retention | Mensuel | < 90% | > 100% |
| **Organic referral rate** | % acquisition via referral | Mensuel | < 5% | > 20% |
| **Churn mensuel** | % MRR perdu / mois | Mensuel | > 5% | < 2% |

---

## Post-PMF -- Scaler sans Perdre le PMF

**3 pieges du scaling** : (1) croissance trop rapide de l'equipe -- les nouvelles recrues n'ont pas le contexte des entretiens clients fondateurs, accompagner chaque recrutement d'une immersion client ; (2) ajouter des features pour plaire a tout le monde -- le PMF repose sur la resonance forte avec un segment specifique, nommer un "PMF guardian" qui challenge chaque addition au roadmap ; (3) negliger la qualite produit -- une degradation de la fiabilite ou de la performance fait chuter la retention, maintenir les metriques de retention comme garde-fous absolus.

**Signaux de degradation du PMF** : churn mensuel en hausse pendant 3 mois consecutifs, NRR passant sous 100%, score Ellis en baisse de > 10 points sur un trimestre, feedback negatif croissant sur G2 ou Capterra, augmentation du ticket moyen de support, baisse du taux de renouvellement spontane.
