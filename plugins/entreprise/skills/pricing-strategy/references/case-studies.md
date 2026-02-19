# Etudes de Cas -- Pricing Strategy en Pratique

## Overview

Ce document presente 4 etudes de cas detaillees de decisions de pricing strategy : migration per-seat vers usage-based, lancement de prix par Van Westendorp, implementation du decoy pricing, et gestion d'une hausse de prix +40% en enterprise SaaS. Chaque cas inclut le contexte, le raisonnement de la decision, l'implementation step-by-step, les resultats mesures et les lecons transposables. Ces cas sont composites, inspires de situations reelles dans l'industrie SaaS europeenne (2021-2024).

---

## Cas 1 -- SaaS B2B : Passage du Per-Seat au Usage-Based

### Contexte

**Entreprise** : SaaS analytics de donnees clients (style Amplitude/Mixpanel pour PME europeennes). Fond en 2018, 200 clients actifs, ARR de 2,4 M EUR au moment de la decision (mi-2022).

**Modele initial** : per-seat, 45 EUR/utilisateur/mois. Tarif degressif a partir de 10 sieges. Contrats annuels avec 180 jours de preavis.

**Probleme identifie** : le taux de churn atteint 18% annuel. Les entretiens de churn revelent un pattern coherent : les clients sur-paient. Une analyse du parc montre que 62% des clients ont des sieges "dormants" (< 1 connexion par semaine) representant en moyenne 38% de leurs sieges payes. Ces clients ont le sentiment de payer pour des licences inutilisees.

**Signal concurrent** : deux concurrents directs ont migre vers un modele usage-based (prix par volume de donnees analysees) en 2021. Le discours commercial des concurrents ("payez uniquement pour ce que vous utilisez") resonne fortement dans les appels de prospection perdus.

### Decision de Migration

**Analyse du parc client** :

| Segment | Nb clients | % ARR | Usage moyen | Impact migration estime |
|---|---|---|---|---|
| Sous-utilisateurs (< 60% sieges actifs) | 124 | 41% | 48% d'actifs | -15% facture moyenne |
| Utilisateurs normaux (60-90% actifs) | 58 | 38% | 74% d'actifs | -5% a +3% |
| Sur-utilisateurs (> 90% actifs) | 18 | 21% | 96% d'actifs | +20% facture moyenne |

La simulation revele que 62% des clients paieraient moins en usage-based sur la base de leur consommation historique. C'est une perte de revenu court terme mais un investissement en retention et en expansion.

**Nouvelle metrique de facturation** : events analyses par mois (chaque action utilisateur trackee = 1 event). Fourchette typique : 500 000 a 10 000 000 events/mois selon la taille du client.

**Grille tarifaire usage-based** :

| Volume events/mois | Prix par millier d'events |
|---|---|
| 0 - 500 K | 0.10 EUR |
| 500 K - 2 M | 0.08 EUR |
| 2 M - 10 M | 0.06 EUR |
| > 10 M | Negociable |

**Minimum mensuel** : 99 EUR/mois (equivalent a 990 000 events au tarif de base).

### Implementation

**Phase 1 (Mois 1-2) -- Infrastructure** : deployer le tracking de consommation en temps reel. Construire le dashboard client montrant la consommation du mois, la tendance, et la facture projete. Tester le mecanisme de facturation usage-based en interne.

**Phase 2 (Mois 3) -- Communication** : envoyer un email a tous les clients avec 90 jours de preavis. Segmenter le message :
- Sous-utilisateurs : "Bonne nouvelle -- votre nouvelle facture sera probablement inferieure."
- Sur-utilisateurs : "Votre usage intensif sera mieux refleted -- voici ce que vous paieriez aujourd'hui."
- Utilisateurs normaux : "Impact neutre ou faible -- voici votre simulation personnalisee."

**Phase 3 (Mois 4-5) -- Opt-in volontaire** : proposer la migration en usage-based en opt-in pour les clients qui y gagneraient. 89 clients (sous-utilisateurs et normaux) migrent volontairement en 6 semaines.

**Phase 4 (Mois 6) -- Migration forcee** : les 111 clients restants sont migres automatiquement. Proposer un grandfathering de 12 mois aux 18 plus gros clients a risque (ARR > 30 000 EUR par client).

**Phase 5 (Mois 7-12) -- Monitoring** : suivi hebdomadaire du MRR, NRR et churn par cohorte de migration. Intervention proactive aupres des clients dont la consommation stagne ou baisse.

### Resultats

| Metrique | Avant migration (M0) | 6 mois apres (M6) | 12 mois apres (M12) |
|---|---|---|---|
| ARR | 2 400 000 EUR | 2 180 000 EUR | 2 850 000 EUR |
| MRR | 200 000 EUR | 181 600 EUR | 237 500 EUR |
| Churn annuel | 18% | 12% (projete) | 9% (realise) |
| NRR | 105% | - | 128% |
| ARPU | 1 000 EUR/mois | 908 EUR/mois | 1 187 EUR/mois |
| Clients actifs | 200 | 200 | 201 |

La baisse de l'ARR a M6 etait anticipee (-9%) : c'est le "trough" de la migration. Le rebond au-dela du niveau initial a M12 vient de deux effets : la croissance organique de la consommation des clients existants (+expansion revenue) et une amelioration du taux de conversion sur les nouveaux clients ("payez ce que vous consommez" est un argument plus fort dans les appels de vente).

### Lecon Principale

La migration per-seat vers usage-based necessite d'accepter une baisse de revenu a court terme pour gagner en retention et en expansion revenue a long terme. Le facteur cle de succes est la transparence : les clients qui comprennent leur consommation et voient leur facture evoluer de facon logique ne churnen pas. Ceux qui decouvrent une hausse surprise sans dashboard de suivi churnenent.

---

## Cas 2 -- Startup : Van Westendorp pour Fixer le Prix de Lancement

### Contexte

**Entreprise** : SaaS RH pre-lancement, outil de gestion des entretiens annuels et du suivi des objectifs pour PME de 50-300 employes. Equipe de 4 personnes (2 fondateurs tech, 1 CSO, 1 designer). En 2023, phase pre-revenue.

**Probleme** : les fondateurs ont une intuition de prix a 99 EUR/mois (base sur le cout de la solution concurrente la moins chere). Avant le lancement, ils veulent valider ou invalider cette intuition par des donnees.

**Alternative disponible** : la plupart des prospects gererent les entretiens annuels avec des formulaires Google Docs et des tableurs. Un concurrent etabli (Lattice) est positionne a 11 USD/utilisateur/mois, soit ~1 100 USD/mois pour 100 employes -- hors de portee des PME cibles.

### Methodologie Van Westendorp Complete

**Survey design** : 85 prospects identifies via LinkedIn (DRH et responsables RH de PME 50-300 employes en France et Belgique). Taux de reponse : 68% (58 repondants complets). La survey presente d'abord une demo video de 3 minutes du produit, puis les 4 questions Van Westendorp.

**Questions posees** :
1. "A quel prix mensuel (pour votre entreprise, quelle que soit la taille) ce logiciel vous semblerait-il trop cher pour etre envisageable ?"
2. "A quel prix ce logiciel vous semblerait-il cher, mais vous l'acheteriez quand meme si votre budget le permettait ?"
3. "A quel prix ce logiciel vous semblerait-il etre une bonne affaire, un prix tres raisonnable ?"
4. "A quel prix ce logiciel vous semblerait-il si bon marche que vous douteriez de sa qualite ou de sa perennite ?"

**Distribution des reponses** :

| Question | Mediane | P25 | P75 |
|---|---|---|---|
| Trop cher | 399 EUR | 249 EUR | 599 EUR |
| Cher mais acceptable | 249 EUR | 149 EUR | 349 EUR |
| Bon marche | 149 EUR | 99 EUR | 199 EUR |
| Trop bon marche | 79 EUR | 49 EUR | 119 EUR |

**Points cles identifies** :
- PMC (Point of Marginal Cheapness) : 89 EUR/mois
- PME (Point of Marginal Expensiveness) : 319 EUR/mois
- OPP (Optimal Price Point) : 189 EUR/mois
- IDP (Indifference Price Point) : 199 EUR/mois

**Acceptable Price Range** : 89 - 319 EUR/mois

**Revelation** : l'intuition des fondateurs (99 EUR/mois) est en dessous du PMC pour 38% des repondants -- ces prospects auraient des doutes sur la qualite d'un produit a 99 EUR. L'OPP suggerait 189 EUR, soit presque le double de l'intuition initiale.

### Test A/B 249 EUR vs 199 EUR

**Decision** : tester deux prix au-dessus de l'OPP pour maximiser la marge tout en restant dans l'APR.

**Methodologie** : split de la liste de prospects waitlist (210 inscrits). 105 recoivent l'offre de lancement a 199 EUR/mois, 105 a 249 EUR/mois. Les deux groupes ont acces a un trial de 14 jours, puis decision d'achat.

**Resultats du test** :

| | 199 EUR/mois | 249 EUR/mois |
|---|---|---|
| Trials actives | 105 | 105 |
| Conversions paid | 23 (22%) | 19 (18%) |
| MRR genere | 4 577 EUR | 4 731 EUR |
| Churn 60j | 2 clients | 1 client |
| NPS moyen | 42 | 48 |

**Interpretation** : le prix a 249 EUR convertit 4 points de moins en taux de conversion, mais genere plus de MRR (+3.4%) et moins de churn. Les clients a 249 EUR ont un NPS plus eleve, suggerant que le prix plus eleve renforce la perception de valeur et l'engagement.

**Decision finale** : lancement a 249 EUR/mois. Le plan annuel est propose a 199 EUR/mois equivalent (soit 2 388 EUR/an), encodant un discount annuel de 20%.

### Resultats a 12 Mois

- 67 clients actifs
- ARR : 193 608 EUR (65% en annuel)
- Churn mensuel : 2.1%
- NRR : 118% (expansion via augmentation du nombre d'employes dans les entreprises clientes)

### Lecon Principale

L'intuition de prix des fondateurs est systematiquement biaisee vers le bas. Deux mecanismes expliquent ce biais : la peur de la rejection ("si c'est trop cher, personne ne va acheter") et la comparaison avec les concurrents les moins chers plutot qu'avec la valeur creee. La methode Van Westendorp revele que le marche a souvent une willingness-to-pay 2 a 3x superieure a l'intuition initiale. Un prix trop bas reduit la valeur percue ET la marge -- c'est un double desavantage.

---

## Cas 3 -- E-commerce : Decoy Pricing et Uplift de Panier

### Contexte

**Entreprise** : marketplace e-commerce B2B permettant a des vendeurs professionnels de vendre leurs produits en ligne. 3 plans d'abonnement pour les vendeurs (structure en place depuis le lancement, 2020).

**Structure initiale (2 plans)** :
- Basic : 29 EUR/mois -- Commission 3%, 100 produits max, pas de boutique personnalisee
- Pro : 99 EUR/mois -- Commission 1.5%, produits illimites, boutique personnalisee, statistiques

**Distribution observee** : 78% des vendeurs sur Basic, 22% sur Pro.
**ARPU** : 0.78 x 29 + 0.22 x 99 = 22.62 + 21.78 = **44.40 EUR/mois**

**Probleme** : la majorite des vendeurs reste sur Basic, limitant le panier moyen. Le plan Pro est percu comme "trop cher" ou "pour les gros vendeurs" meme par des vendeurs qui vendraient assez pour que la reduction de commission (1.5% vs 3%) compense largement la difference de prix.

### Implementation du Decoy Pricing

**Analyse** : le saut de 29 EUR a 99 EUR (x3.4) est psychologiquement trop important. Il n'y a pas de point de reference intermediaire qui rende le Pro "raisonnable".

**Nouveau plan (le decoy)** -- Pro Lite :
- Prix : 79 EUR/mois
- Commission : 1.5% (identique au Pro)
- Produits : 500 max (vs illimites en Pro)
- Boutique personnalisee : Non (vs Oui en Pro)
- Statistiques : basiques seulement (vs avancees en Pro)

**Logique du decoy** : Pro Lite est facture 79 EUR/mois -- seulement 20 EUR de moins que le Pro a 99 EUR. Mais Pro Lite n'a pas de boutique personnalisee, a une limite de 500 produits et des stats basiques. Pour 20 EUR de plus, le Pro offre nettement plus. Le Pro Lite existe pour rendre le Pro attractif, pas pour etre choisi.

**Presentation de la page pricing** :

| | Basic | Pro Lite | Pro |
|---|---|---|---|
| Prix | 29 EUR/mois | 79 EUR/mois | **99 EUR/mois** |
| Commission | 3% | 1.5% | **1.5%** |
| Produits | 100 | 500 | **Illimites** |
| Boutique personnalisee | Non | Non | **Oui** |
| Statistiques | Basiques | Basiques | **Avancees** |
| Badge | -- | -- | **Recommande** |

### Resultats (Avant / Apres sur 3 Mois)

| Metrique | Avant decoy | Apres decoy (M+3) | Delta |
|---|---|---|---|
| % vendeurs sur Basic | 78% | 52% | -26 pts |
| % vendeurs sur Pro Lite | 0% | 14% | +14 pts |
| % vendeurs sur Pro | 22% | 34% | +12 pts |
| ARPU | 44.40 EUR | 58.96 EUR | +32.8% |
| MRR (1 000 vendeurs) | 44 400 EUR | 58 960 EUR | +14 560 EUR |
| ARR impact | -- | -- | +174 720 EUR |

**Analyse de la distribution** : l'introduction du Pro Lite a surtout fait migrer des vendeurs de Basic vers Pro (pas vers Pro Lite). Le Pro Lite a ete choisi par 14% des vendeurs -- principalement des nouveaux inscrits qui voulaient un point de depart avant le Pro. C'est l'effet decoy attendu : le Pro Lite rend le Pro "logique" plus qu'il n'est lui-meme attractif.

**Impact sur les revenus de commission** : en plus de l'augmentation de l'abonnement, la baisse de la commission de 3% a 1.5% pour plus de vendeurs augmente leur volume de ventes (ils investissent davantage en marketing car chaque vente est plus rentable). L'effet indirect sur le GMV de la plateforme est estime a +8% -- amplifiant encore les revenus de commission totaux.

### Lecon Principale

L'effet decoy fonctionne mieux quand les differences entre les options sont claires et perceptibles. Un decoy trop proche de l'option cible (en features) ne joue pas son role d'ancre -- les clients le choisissent reellement. Un decoy trop eloigne en prix n'est pas vu comme une reference valide. La plage ideale pour le prix du decoy : 75-90% du prix de l'option cible.

---

## Cas 4 -- Enterprise SaaS : Price Increase +40%

### Contexte

**Entreprise** : SaaS compliance et gestion des risques pour secteur financier (banques, assurances, SGP). Fonde en 2016, 85 clients enterprise, ARR de 6,8 M EUR en 2022. Equipe de 62 personnes.

**Historique tarifaire** : les prix n'ont pas ete revus depuis 2019. Entre-temps, l'equipe produit a delivre 3 modules majeurs (reporting DORA, module stress-testing, API compliance automatise), la disponibilite est passee de 99.2% a 99.95%, et l'equipe support a triple.

**Signal d'alerte** : le benchmark sectoriel (achat d'une etude Gartner + 12 entretiens informels avec des clients) revele que les prix pratiques sont 35-50% en dessous du marche pour un produit de qualification equivalente. Les concurrents facturent 120 000 - 180 000 EUR/an pour des produits moins avances. Le tarif moyen actuel des clients est de 80 000 EUR/an.

**Probleme financier** : avec un CAC de 45 000 EUR et un MRR/client de 6 667 EUR, le CAC payback period est de 6.7 mois. Mais le cout de service (CSM + support + infrastructure) represente 38% du revenu -- comprimant la marge brute a 62%, insuffisant pour les objectifs d'un eventuel tour de financement Series B (cible : > 75% marge brute SaaS).

### Preparation de la Hausse

**Analyse benchmarks** :

| Concurrent | Positionnement | Prix typique | Marge brute estimee |
|---|---|---|---|
| Leader US (adapte EU) | Full suite compliance | 180 000 - 400 000 EUR/an | 82% |
| Pure player EU n1 | Reporting + audit | 90 000 - 150 000 EUR/an | 71% |
| Pure player EU n2 | Stress-testing specialiste | 80 000 - 120 000 EUR/an | 68% |
| Notre solution | Full suite + API | **80 000 EUR/an (median)** | 62% |

**Calcul churn attendu** :
- Base de 85 clients
- Hypothese conservatrice : 20% de churn (17 clients) sur les clients les plus price-sensitive
- Hypothese centrale : 10% de churn (8-9 clients)
- ARR perdu au pire cas : 17 x 80 000 EUR = 1 360 000 EUR
- ARR gagne sur 68 clients restants : +40% x 68 x 80 000 EUR = 2 176 000 EUR
- Net ARR impact au pire cas : +816 000 EUR (+12% ARR)
- Net ARR impact au cas central : +2 448 000 EUR (+36% ARR)

**Decision** : hausse de prix de +40% effective au 1er janvier 2023. Nouveaux contrats a partir de septembre 2022 aux nouveaux tarifs. Clients existants : renouvellement aux nouveaux tarifs (pas de grandfathering global).

### Communication et Segmentation

**Segmentation des clients pour la communication** :

| Segment | Criteres | Nb clients | Traitement |
|---|---|---|---|
| Champions | NPS > 50, usage > 80%, ARR > 100K | 18 | Appel CSM + meeting direction, message "partner" |
| Core | NPS 30-50, usage 60-80%, ARR 50-100K | 41 | Email personnalise + appel CSM si renouvellement dans 6 mois |
| At-risk | NPS < 30 OU usage < 50%, ARR < 50K | 26 | Grandfathering 12 mois + plan de valeur |

**Template de communication Champions** :

Le CSM envoie un email personnalise 90 jours avant le renouvellement, suivi d'un appel. Message cle :

- Remercier pour 3-5 ans de partenariat (specifique a chaque client).
- Presenter les 3 modules majeurs livres depuis le dernier renouvellement.
- Citer des metriques de valeur specifiques a ce client (ex : "Votre equipe a genere 847 rapports DORA automatises cette annee").
- Annoncer la hausse (+40%) avec la justification : investissements produit, SLA, infrastructure.
- Proposer un engagement 2 ans pour lisser l'impact : +30% la premiere annee, +10% la deuxieme.

**Gestion des objections** :

| Objection | Reponse |
|---|---|
| "C'est trop cher, on va regarder les alternatives" | "Je comprends. Nous pouvons organiser un benchmark compare -- je suis confiant dans notre positionnement vs [concurrent]. Voulez-vous qu'on le fasse ensemble ?" |
| "Notre budget est fixe pour l'annee prochaine" | "Je peux travailler avec votre DAF pour structurer l'engagement sur 2 ans et lisser la hausse." |
| "On n'utilise pas toutes les features" | "Identifions ensemble les modules non actives -- je vous propose un onboarding dedie sur [module specifique] pour maximiser votre ROI." |
| "Nos concurrents ont le meme pour moins cher" | "Lesquels ? Regardons ensemble -- la plupart des offres a ce prix n'incluent pas [SLA 99.95%, module DORA, API temps reel]." |

### Resultats

**Adoption des nouveaux tarifs** :

| Segment | Clients | Churn observe | Hausse acceptee | Engagement 2 ans |
|---|---|---|---|---|
| Champions (18) | 18 | 0 | 18/18 | 11/18 |
| Core (41) | 41 | 4 | 36/41 | 18/36 |
| At-risk (26) | 26 | 3 | 23/26 (grandfathered) | 2/23 |
| **Total** | **85** | **7 (8.2%)** | **77 clients** | **31/77** |

**Impact financier** :

| Metrique | Avant hausse | Apres hausse (M+12) | Delta |
|---|---|---|---|
| ARR | 6 800 000 EUR | 9 180 000 EUR | +35% |
| Clients actifs | 85 | 78 | -7 |
| ARPU | 80 000 EUR/an | 117 692 EUR/an | +47% |
| Marge brute | 62% | 74% | +12 pts |
| NRR | 108% | 143% | +35 pts |
| Churn clients | 12% (base) | 8.2% (hausse) | -3.8 pts |

**Churn observe vs anticipe** : 8.2% vs 20% anticipe au pire cas. Le churn a ete concentre sur 3 clients Core et 4 clients At-risk -- exactement les segments prevus. Aucun client Champion n'a churne.

**Effet signal** : la hausse de prix a eu un effet inattendu positif sur le pipeline commercial. Les nouvelles opportunites ont eu une conversion contractuelle plus rapide -- "si c'est plus cher, c'est que c'est le meilleur" est un signal de qualite en compliance ou le risque de choisir un mauvais outil est eleve.

### Lecon Principale

Les clients enterprise acceptent les hausses de prix importantes (40% et plus) quand trois conditions sont reunies : (1) la valeur delivree est concrete et documentee, (2) la relation avec le CSM est solide et le dialogue a ete ouvert bien avant l'annonce, (3) des mecanismes de flexibilite (engagement 2 ans, grandfathering cible) sont proposes aux clients a risque. La peur du churn pousse les entreprises SaaS a sous-tarifer pendant des annees -- ce qui est une erreur strategique que les clients les plus fidelises ne "punissent" pas si le changement est bien gere.

---

## Synthese des Lecons Transversales

| Cas | Contexte | Lecon Cle | Metrique Impact |
|---|---|---|---|
| Migration per-seat → usage | SaaS analytics 200 clients | Accepter la baisse court terme pour gagner en NRR long terme | NRR 105% → 128% |
| Van Westendorp pre-lancement | SaaS RH pre-revenue | Les fondateurs sous-estiment la WTP x2-3 | Prix optimal 249 EUR vs intuition 99 EUR |
| Decoy pricing marketplace | E-commerce 1 000 vendeurs | L'effet decoy fonctionne si differences claires | ARPU +32.8% |
| Price increase +40% enterprise | SaaS compliance 85 clients | La valeur documentee protege du churn lors des hausses | NRR +35 pts, churn 8% vs 20% anticipe |

**Principe commun** : dans tous les cas, la peur de la reaction marche pousse a des decisions sous-optimales (rester en per-seat, fixer un prix trop bas, ne pas implementer de decoy, ne pas augmenter les prix). Les entreprises qui ancrent leurs decisions de pricing dans des donnees (PSM, simulations, benchmarks, segmentation) surperforment systematiquement celles qui suivent leur intuition.
