# Modeles de Pricing SaaS -- Per-Seat, Usage-Based et Freemium

## Overview

Ce document de reference couvre les 5 modeles de pricing dominants dans l'industrie SaaS : flat-rate, per-seat, usage-based, tiered et freemium. Il analyse les forces et faiblesses de chaque modele, les conditions d'application optimale, et fournit des outils de decision pour choisir ou migrer entre modeles. Un simulateur Python permet de projeter les revenus selon les hypotheses choisies. Les benchmarks sectoriels ancrent les decisions dans des donnees de marche actuelles.

---

## Key Concepts

### Vue d'Ensemble des 5 Modeles SaaS

| Modele | Formule | Predictabilite revenus | Barrier to entry | Scalabilite | Fit PLG |
|---|---|---|---|---|---|
| Flat-rate | Prix fixe mensuel | Tres haute | Moyenne | Faible | Non |
| Per-seat | Prix x nombre d'utilisateurs | Haute | Basse | Moyenne | Partiel |
| Usage-based | Prix x consommation | Moyenne | Tres basse | Tres haute | Oui |
| Tiered | Plans predefinis | Haute | Variable | Moyenne | Partiel |
| Freemium | Gratuit + conversion payante | Basse | Tres basse | Haute | Oui (natif) |

### Flat-Rate Pricing

Un seul prix pour tout le monde, toutes features comprises. Rarement optimal car il ne capture pas la diversite des profils de valeur. Convient aux produits tres homogenes (un outil simple avec un seul usage) ou aux marches ou la simplicite est un argument de vente majeur.

**Exemple** : Basecamp a longtemps pratique le flat-rate (99 USD/mois, equipes illimitees) comme element de positionnement differenciateur face a Asana et Monday.com.

**Piege** : les gros clients sur-payent et cherchent des alternatives sur mesure. Les petits clients sous-payent et la valeur capturee est sous-optimale. Le flat-rate mene generalement a un sous-investissement dans la segmentation.

---

## Frameworks & Methods

### Per-Seat (Par Utilisateur)

**Formule** : MRR = Nombre de sieges x Prix par siege

**Avantages** :
- Previsibilite du revenu excellente : chaque nouveau collaborateur = revenu additionnel.
- Simple a comprendre pour l'acheteur : le budget RH est lineaire, le cout SaaS aussi.
- Expansible naturellement : la croissance de l'equipe client genere de l'expansion revenue sans action commerciale.
- Facile a auditer et a facturer : le nombre d'utilisateurs actifs est mesurable.

**Inconvenients** :
- Cree une resistance a l'adoption : les managers limitent le nombre de licences pour controler les couts, ce qui nuit a l'usage et au ROI reel.
- Ne capture pas la valeur intensive : un power user qui realise 10x plus de valeur qu'un utilisateur lambda paie le meme prix.
- Vulnerable au right-sizing agressif : en periode budgetaire tendue, les clients suppriment les licences (churn partiel) sans churner completement.
- Inadapte aux produits a faible nombre d'utilisateurs mais fort impact (ex: BI tool utilise par 5 analysts mais impactant 1 000 employes).

**Quand l'utiliser** : produits de collaboration (CRM, messagerie, gestion de projets), valeur directement proportionnelle au nombre d'utilisateurs, marche ou le per-seat est la norme etablie (switching costs cognitifs trop eleves pour imposer un modele different).

**Exemples** : Salesforce (25-300 USD/user/mois selon edition), Slack (7.25-12.50 USD/user/mois), HubSpot Sales Hub (45-120 USD/user/mois).

**Optimisations** : proposer des paliers de volume (1-10 users, 11-50, 51-200, 200+) avec des prix degressifs pour reduire la resistance a l'adoption. Distinguer les "full users" des "view-only users" ou "collaborators" a prix reduit.

### Usage-Based Pricing (Consumption)

**Formule** : MRR = Volume consomme x Prix unitaire

**Metriques usage courantes par secteur** :

| Secteur | Metrique | Exemples |
|---|---|---|
| API & infrastructure | Appels API, requetes, tokens | Twilio (prix/SMS), OpenAI (prix/1000 tokens), Stripe (% par transaction) |
| Data & analytics | GB traites, requetes, compute hours | Snowflake (credits compute), BigQuery (TB traites) |
| Communication | Emails envoyes, SMS, minutes d'appel | SendGrid (prix/email), Vonage (prix/minute) |
| Observabilite | Logs ingeres, metriques, traces | Datadog (hosts monitores + custom metrics) |
| Stockage | GB stockes, transactions | AWS S3, Cloudflare R2 |

**Avantages** :
- Aligne parfaitement le prix sur la valeur creee : plus le client utilise, plus il paie, plus il a de valeur.
- Barrier to entry tres faible : un nouveau client peut commencer avec un budget minimal et scaler.
- Potentiel d'expansion revenue automatique : un client qui grandit genere naturellement plus de revenu sans intervention commerciale.
- Fit naturel avec le PLG : decouverte gratuite ou quasi-gratuite, monetisation progressive.

**Inconvenients** :
- Revenus impredictibles : la variabilite de la consommation cree des "bill shock" pour les clients et de l'incertitude pour le forecast finance.
- Couts d'infrastructure variables difficiles a couvrir : si un client consomme soudainement 10x, les couts augmentent en temps reel mais le revenu aussi -- ce qui est positif, mais necessite une gestion de tresorerie rigoureuse.
- Difficulte de budgetisation pour les clients : les acheteurs enterprise detestent les budgets variables. Necessite souvent de proposer des commitments (credits prepays, annual commits).
- Friction au scaling : les clients qui anticipent une forte croissance peuvent negocier des tarifs preferentiels chez les concurrents.

**Comment mitiger l'impredictibilite** :
- Proposer des spend caps et des alertes de consommation en temps reel (tableau de bord client).
- Offrir des packages de credits prepays avec un discount (commit annuel de 12 000 USD = 10 000 USD en credits, soit 17% de discount).
- Proposer un minimum mensuel avec un tarif degressive au-dela ("floor + usage" model).
- Utiliser des metriques de consommation lissees (moyenne mobile sur 3 mois) plutot que spot.

### Freemium

**Definition** : le produit de base est disponible gratuitement, sans limite de temps, mais avec des limitations fonctionnelles ou de capacite. La monetisation vient de la conversion vers des plans payants.

**Benchmarks de conversion freemium vers payant** :

| Performance | Taux de conversion free -> paid |
|---|---|
| Excellent (top 10%) | > 10% |
| Bon | 5-10% |
| Standard | 2-5% |
| Insuffisant | < 2% |

**PLG Motion (Product-Led Growth)** : le freemium est l'instrument principal du PLG. L'acquisition se fait par le produit (viral loops, partage, templates), pas par les commerciaux. Le produit lui-meme genere le desir de passer au payant (activation, aha moment, habitude d'usage).

**Feature gating strategy** : identifier les features qui doivent etre en free (attraction, activation, retention) vs en payant (monetisation).

| Tier | Features | Objectif |
|---|---|---|
| Free | Core features, limites de volume (ex: 3 projets, 1 GB) | Acquisition, activation, generation de virabilite |
| Pro | Features avancees, volumes eleves, integrations | Monetisation utilisateurs individuels et petites equipes |
| Team | Collaboration, admin, permissions, SSO | Monetisation equipes (10-50 personnes) |
| Enterprise | SLA, securite avancee, support dedie, custom | Monetisation grands comptes |

**Limites freemium** : le free tier a un cout direct (infrastructure, support) et un cout indirect (dilution de la valeur percue, support de clients qui ne payeront jamais). Calculer le CAC effectif du freemium en incluant ces couts. Ne jamais lancer un freemium sans avoir modelise le cout du free user et defini un taux de conversion cible.

**Erreur classique de feature gating** : mettre la feature la plus utilisee en payant trop tot. Le resultat est une friction qui bloque l'activation avant meme que l'utilisateur ait atteint l'aha moment. Mettre en payant les features qui apportent de la valeur supplementaire APRES que l'utilisateur a vu la valeur du free.

### Tiered Pricing

Le tiered pricing propose 3 plans (ou plus) avec des combinaisons de features et de limites de volume differentes.

**Structure classique 3 tiers** :

| | Starter | Pro | Enterprise |
|---|---|---|---|
| Prix indicatif | 29-49 EUR/mois | 99-199 EUR/mois | Custom (500+ EUR/mois) |
| Cible | Freelances, TPE | PME, scale-ups | Grands comptes |
| Utilisateurs | 1-3 | 5-15 | Illimite |
| Stockage | 5 GB | 50 GB | Illimite |
| Integrations | 2-3 basiques | 10+ | API custom + SSO |
| Support | Email | Email + Chat | CSM dedie |
| SLA | Aucun | 99.5% | 99.9%+ |

**Anchoring effect** : l'existence du plan Enterprise (meme si rare) rend le plan Pro "raisonnable" par contraste. Le Starter sert de hook et de reference basse. Concevoir les 3 plans en pensant a cet effet psychologique, pas seulement aux features.

**Feature allocation par tier** : regle des 3/5/10. Le plan Starter couvre ~30% des besoins des clients cibles. Le Pro couvre ~80%. L'Enterprise couvre 100% + des besoins specifiques grands comptes (compliance, SLA, integrations proprietary).

### Enterprise Pricing

**Custom pricing** : pour les grands comptes (generalement > 50 000 EUR/an ARR), le prix est negocie individuellement. Le tarif catalogue sert de point de reference mais jamais de prix final.

**Processus procurement** : les grands comptes ont des processus d'achat formalises (RFP, appels d'offres, validation juridique et securite, comites d'achat multi-decideurs). Prevoir 3 a 12 mois de cycle de vente. Le commercial devient un orchestrateur du processus plutot qu'un vendeur de features.

**ROI selling vs feature selling** : en enterprise, le prix n'est pas justifie par les features mais par le ROI mesurable. Preparer un business case chiffre pour chaque opportunite significative (> 50 000 EUR ARR). Cf. le template Value Calculator dans le document value-based-pricing.md.

---

## Tools & Implementation

### Simulateur Revenus SaaS en Python

```python
import numpy as np
import pandas as pd

def simuler_revenus_saas(modele='per_seat', mois=24, **params):
    """
    Simule les revenus MRR/ARR selon le modele de pricing et les hypotheses.

    Parametres selon modele :
    - per_seat : prix_par_siege, nouveaux_clients_par_mois, sieges_par_client,
                 taux_expansion_mensuel, taux_churn_mensuel
    - usage_based : prix_par_unite, nouveaux_clients_par_mois, consommation_initiale,
                    croissance_conso_mensuelle, taux_churn_mensuel
    - freemium : utilisateurs_free_par_mois, taux_conversion, prix_pro,
                 taux_churn_mensuel
    """
    mrr_history = []
    clients_actifs = 0
    mrr_actuel = 0

    if modele == 'per_seat':
        prix = params.get('prix_par_siege', 50)
        new_clients = params.get('nouveaux_clients_par_mois', 10)
        sieges = params.get('sieges_par_client', 8)
        expansion = params.get('taux_expansion_mensuel', 0.02)
        churn = params.get('taux_churn_mensuel', 0.015)

        clients = []
        for m in range(mois):
            # Ajout nouveaux clients
            for _ in range(new_clients):
                clients.append({'sieges': sieges, 'actif': True})
            # Expansion et churn
            for c in clients:
                if c['actif']:
                    c['sieges'] = c['sieges'] * (1 + expansion)
                    if np.random.random() < churn:
                        c['actif'] = False
            mrr = sum(c['sieges'] * prix for c in clients if c['actif'])
            mrr_history.append({'mois': m+1, 'mrr': round(mrr), 'modele': 'per_seat'})

    elif modele == 'usage_based':
        prix = params.get('prix_par_unite', 0.05)
        new_clients = params.get('nouveaux_clients_par_mois', 15)
        conso_init = params.get('consommation_initiale', 1000)
        croissance = params.get('croissance_conso_mensuelle', 0.08)
        churn = params.get('taux_churn_mensuel', 0.02)

        clients = []
        for m in range(mois):
            for _ in range(new_clients):
                clients.append({'conso': conso_init, 'actif': True})
            for c in clients:
                if c['actif']:
                    c['conso'] = c['conso'] * (1 + croissance)
                    if np.random.random() < churn:
                        c['actif'] = False
            mrr = sum(c['conso'] * prix for c in clients if c['actif'])
            mrr_history.append({'mois': m+1, 'mrr': round(mrr), 'modele': 'usage_based'})

    elif modele == 'freemium':
        free_par_mois = params.get('utilisateurs_free_par_mois', 200)
        taux_conv = params.get('taux_conversion', 0.03)
        prix_pro = params.get('prix_pro', 29)
        churn = params.get('taux_churn_mensuel', 0.04)

        clients_payants = []
        for m in range(mois):
            nouveaux_payants = int(free_par_mois * taux_conv)
            for _ in range(nouveaux_payants):
                clients_payants.append({'actif': True})
            for c in clients_payants:
                if c['actif'] and np.random.random() < churn:
                    c['actif'] = False
            mrr = sum(prix_pro for c in clients_payants if c['actif'])
            mrr_history.append({'mois': m+1, 'mrr': mrr, 'modele': 'freemium'})

    df = pd.DataFrame(mrr_history)
    df['arr'] = df['mrr'] * 12
    return df

# Comparaison des trois modeles
per_seat = simuler_revenus_saas('per_seat', mois=24,
    prix_par_siege=50, nouveaux_clients_par_mois=8, sieges_par_client=10,
    taux_expansion_mensuel=0.02, taux_churn_mensuel=0.015)

usage_based = simuler_revenus_saas('usage_based', mois=24,
    prix_par_unite=0.01, nouveaux_clients_par_mois=20,
    consommation_initiale=5000, croissance_conso_mensuelle=0.07,
    taux_churn_mensuel=0.02)

freemium = simuler_revenus_saas('freemium', mois=24,
    utilisateurs_free_par_mois=300, taux_conversion=0.04,
    prix_pro=29, taux_churn_mensuel=0.05)

print("MRR mois 24 :")
print(f"  Per-seat  : {per_seat.iloc[-1]['mrr']:,.0f} EUR")
print(f"  Usage-based: {usage_based.iloc[-1]['mrr']:,.0f} EUR")
print(f"  Freemium  : {freemium.iloc[-1]['mrr']:,.0f} EUR")
```

### Transition Per-Seat vers Usage-Based

La migration est l'une des decisions de pricing les plus risquees. Un client per-seat a un budget previsible. Passer en usage-based lui impose une incertitude qu'il n'a pas demandee.

**Protocole de migration en 5 etapes** :

**Etape 1 -- Analyse du parc client** : segmenter les clients actuels en 3 groupes selon leur usage reel vs le nombre de sieges payes : (a) sous-utilisateurs (< 60% des sieges actifs), (b) utilisateurs normaux (60-90% actifs), (c) sur-utilisateurs (> 90% actifs, contraints par le nombre de sieges).

**Etape 2 -- Simulation de l'impact** : calculer pour chaque client ce que serait sa facture en usage-based selon sa consommation historique. Identifier les clients qui paieraient plus (risque de churn) et ceux qui paieraient moins (risque de bad surprise dans l'autre sens -- perte de revenu).

**Etape 3 -- Communication progressive** : annoncer la migration 90 jours a l'avance. Proposer d'abord le nouveau modele en opt-in aux clients qui y gagneraient. Convertir ensuite les autres avec un accompagnement personnalise.

**Etape 4 -- Grandfathering selectif** : proposer un gel des conditions aux clients les plus a risque (gros ARR, faible usage, champion interne fragile) pendant 12-18 mois. Cout : revenu sous-optimal a court terme. Benefice : retention du client pendant la periode de transition.

**Etape 5 -- Monitoring post-migration** : suivre hebdomadairement le MRR par cohorte de migration. Identifier les signaux de churn precoces (reduction de consommation, tickets support, absence de connexion > 14 jours).

---

## Benchmarks Sectoriels

**Pricing SaaS horizontal vs vertical** :

| Type | Exemples | Fourchette de prix | Logique de prix |
|---|---|---|---|
| SaaS horizontal | Notion, Slack, Zoom | 8-50 EUR/user/mois | Volume utilisateurs, feature gating |
| SaaS vertical (PME) | Restaurant, salon, immobilier | 50-300 EUR/mois flat | Valeur sectorielle, simplicite |
| SaaS vertical (Enterprise) | Veeva, Workiva, Procore | 50 000-500 000 EUR/an | ROI sectoriel, compliance |
| Infra / Developer tools | Twilio, Datadog, Segment | Usage-based | Consommation technique |

**NRR (Net Revenue Retention) par modele** :

| Modele | NRR median | NRR excellent (top quartile) |
|---|---|---|
| Per-seat | 100-108% | > 115% |
| Usage-based | 110-120% | > 130% |
| Freemium | 95-105% | > 115% |
| Tiered | 102-112% | > 120% |

**ARR par employee (efficacite capital)** :

| Stade | ARR/FTE typique | ARR/FTE excellent |
|---|---|---|
| Seed (< 2M ARR) | 80-120 K EUR | > 150 K EUR |
| Series A (2-10M ARR) | 120-180 K EUR | > 200 K EUR |
| Series B (10-50M ARR) | 150-220 K EUR | > 250 K EUR |
| Scale (> 50M ARR) | 180-300 K EUR | > 350 K EUR |

---

## Common Mistakes

**Choisir le modele par defaut sectoriel sans analyse** : si tous les concurrents sont en per-seat, passer en usage-based peut etre un avantage competitif -- ou un desavantage si le marche n'est pas pret. Analyser d'abord le comportement de consommation des clients.

**Freemium sans tracking de l'activation** : lancer un freemium sans mesurer le taux d'activation (% d'utilisateurs qui atteignent l'aha moment) mene a un free tier couteux sans conversion. Definir l'aha moment avant de lancer.

**Tiered pricing avec des tiers trop proches** : si les prix entre tiers sont trop serres ou les features trop similaires, les clients choisiront toujours le moins cher. Creer une differentiation suffisamment forte (pas juste des limites de volume, mais des capabilities qualitativement differentes).

**Migrer en usage-based sans outils de monitoring** : le usage-based sans dashboard de consommation en temps reel pour le client genere du bill shock et du churn. L'observabilite est un prerequis non-negociable du usage-based.
