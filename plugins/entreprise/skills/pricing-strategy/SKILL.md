---
name: pricing-strategy
version: 1.0.0
description: >
  Use this skill when the user asks about "pricing strategy", "stratégie de prix", "value-based pricing", "tarification", "SaaS pricing", "freemium model", "pricing model", "willingness to pay", "elasticité prix", "price positioning", "packaging produit", "monétisation", "augmentation de prix", "price testing", "usage-based pricing", "seat-based pricing", "enterprise pricing", discusses how to price a product or service, build pricing tiers, or optimize revenue through pricing decisions.
---

# Pricing Strategy — Tarification et Monetisation

## Overview

Le pricing est l'un des leviers de croissance les plus puissants et les plus sous-exploites. Une etude McKinsey montre qu'une hausse de 1% du prix moyen, sans perte de volume, génere en moyenne 8% d'amelioration de l'EBITDA — 5x plus qu'une reduction des couts et 3x plus qu'une hausse de volume equivalent.

Pourtant, la majorite des entreprises (particulierement les startups) adoptent un pricing par defaut : "concurrent X fait N EUR, je fais N-20% pour etre competitif". Cette approche detruit de la valeur et ignore la realite de la perception de valeur des clients.

Ce skill couvre les 3 approches fondamentales du pricing, les modeles SaaS specifiques, la psychologie des prix et le processus de pricing testing.

---

## Les 3 Approches Fondamentales

### 1. Cost-Plus Pricing (A Eviter)

**Logique** : Prix = Couts + Marge souhaitee.

**Probleme** : ignore completement la valeur percue par le client et le prix que les concurrents pratiquent. Un client ne paie pas en fonction de vos couts — il paie en fonction de la valeur qu'il recoit.

**Usage legitime** : industries ou les couts sont la reference (BTP, services professionnels a la journee, production manufacturiere).

### 2. Competitive Pricing (Utile mais Insuffisant)

**Logique** : Se positionner par rapport aux concurrents (dessus, dessous ou à parite).

**Probleme** : cree une course vers le bas si tout le marche suit la meme logique. Approprié uniquement si votre produit est un commodity sans differentiation.

**Usage legitime** : marches tres matures avec peu de differentiation (carburant, telecom).

### 3. Value-Based Pricing (Optimal)

**Logique** : Prix fixe en fonction de la valeur economique creee pour le client.

**Fondamental** : si votre logiciel économise 50 000 EUR/an a votre client, vous pouvez facturer 10 000 EUR/an (ratio 5:1 = "value-to-price ratio" acceptable en B2B SaaS).

**Process** :
1. Identifier la valeur quantifiable creee (gains + couts evites)
2. Estimer le Willingness to Pay (WTP) de chaque segment
3. Fixer le prix entre votre cout et le WTP du client

**Exemple concret — SaaS RH** :
- Un ERP RH automatise 3h/semaine de travail administratif pour chaque RH
- Entreprise de 500 personnes : 2 RH = 6h/semaine economisees = ~15 000 EUR/an de valeur
- Prix acceptable : 3 000-6 000 EUR/an (capture 20-40% de la valeur creee)

---

## Mesurer le Willingness to Pay

### Van Westendorp Price Sensitivity Meter

4 questions posees en survey (100+ repondants representatifs) :

1. "A quel prix considereriez-vous ce produit comme trop cher pour l'acheter ?"
2. "A quel prix commenceriez-vous a douter de la qualite du produit ?"
3. "A quel prix trouveriez-vous ce produit avantageux ?"
4. "A quel prix trouveriez-vous ce produit tellement bon marche que vous en douteriez ?"

**Interpretation** : le "Point of Marginal Cheapness" et le "Point of Marginal Expensiveness" definissent la plage de prix acceptable. Le prix optimal se situe entre ces deux bornes.

### Conjoint Analysis

Presenter des packages alternatifs avec differentes combinaisons de features et prix, demander au repondant de choisir. L'analyse statistique revele la valeur de chaque feature et le WTP global.

**Outils** : Qualtrics, SurveyMonkey (Advanced), Typeform + calcul manuel.

### Techniques Qualitatives

Interviews client semi-structurees : "Quel budget avez-vous prevu pour ce type de solution ?" (ne jamais demander "combien paieriez-vous ?").

5 Whys sur le budget : comprendre les contraintes, les approbations internes, les comparaisons.

---

## Modeles de Pricing SaaS

### Per-Seat / User-Based

**Principe** : facturation au nombre d'utilisateurs actifs.

**Avantages** : simple a comprendre, croissance naturelle avec l'adoption, revenus predictibles.

**Inconvenients** : incite les clients a limiter le nombre de licences (friction), desaligne valeur et prix (un utilisateur intensif = meme prix qu'un utilisateur occasionnel).

**Exemples** : Salesforce (150 EUR/user/mois), Slack (7-12 EUR/user/mois), Notion.

**Quand utiliser** : logiciels de collaboration, CRM, outils de communication.

### Usage-Based / Consumption

**Principe** : facturation proportionnelle a l'usage (API calls, volume de donnees, transactions, emails envoyes).

**Avantages** : aligne parfaitement prix et valeur, faible friction a l'acces (entry low), croissance automatique avec l'usage.

**Inconvenients** : revenus moins predictibles, complexite de facturation, difficulte de budgeting pour le client.

**Exemples** : AWS (par ressource), Stripe (2.9% + 0.30 EUR/transaction), Twilio (par SMS/minute), OpenAI (par token).

**Quand utiliser** : infra, APIs, services transactionnels, early adopters avec usage variable.

### Freemium

**Principe** : une version basique gratuite, features avancees payantes.

**Logique** : le produit est son propre commercial. Viral by design.

**Metriques cles** :
- Free-to-Paid Conversion Rate : 2-5% est standard, >5% est excellent
- Time to Convert : combien de temps avant conversion ?
- Feature Usage : quelles features font convertir ?

**Erreur frequente** : le "freemium trap" — gratuit trop genereux → personne ne convert. Regles : la version gratuite doit creer de la valeur mais frustrer sur un point cle que le payant resout.

**Exemples** : Spotify, Dropbox (limit storage), HubSpot (limit contacts), Canva (limit design tools).

**Quand utiliser** : B2C ou B2SMB, produit viral, adoption individuelle avant expansion dans une entreprise.

### Tiered Packaging (Good / Better / Best)

**Principe** : 3-4 tiers avec des features et des prix croissants.

**Structure optimale** :
| | Starter | Pro | Enterprise |
|---|---|---|---|
| Prix | 29 EUR/mois | 99 EUR/mois | Custom |
| Usage | 1 user, 5 projets | 10 users, illimite | Illimite + SSO + API |
| Support | Email | Chat | Dedicated CSM |

**La regle du tiers du milieu** : 60-70% des clients choisissent le tier du milieu. Calibrer le "Pro" avec les features les plus valorisees. Ancrer le prix avec un "Enterprise" plus cher.

**Decoy pricing** : rendre un tier moins attractif pour pousser vers le tier superieur. Exemple : Tier 2 a 89 EUR avec 5 users, Tier 3 a 99 EUR avec 10 users → Tier 3 semble "offert".

---

## Psychologie des Prix

### Price Anchoring (Ancrage)

Le premier prix presente devient la reference cognitive. Presenter le prix le plus cher en premier, puis descendre.

**Application** : toujours presenter l'offre Enterprise (ou annuelle) en premier dans le pricing page.

### Charm Pricing

99 EUR parait significativement moins cher que 100 EUR (meme si la difference reelle est 1%). En B2B, l'effet est moins fort mais reste present sur les montants < 1 000 EUR.

**B2B exception** : les acheteurs enterprise preferent les prix ronds (1 000, 5 000, 10 000 EUR) — percu comme plus professionnel, plus facile a mettre en budget.

### Bundling et Packaging

Grouper des features dans un bundle reduit la sensibilite au prix (le client evalue le bundle globalement, pas feature par feature).

**Meilleur bundle** : associer 1 feature haute valeur perçue + 1-2 features faible cout marginal pour vous.

### Billing Frequency

Facturation annuelle avec remise 15-20% : augmente le LTV, reduit le churn, ameliore le cash-flow.

**Formulation** : ne pas dire "payer annuellement pour economiser 20%" — dire "7,99 EUR/mois, facture annuellement" plutôt que "95,88 EUR/an".

---

## Pricing Testing

### A/B Testing sur le Pricing

**Methodologie** :
- Nouveau trafic uniquement (eviter la confusion des clients existants)
- Variation : prix du tier Pro (+20%, -20%), changement de packaging
- Metriques : taux de conversion, MRR/visiteur, mix de tiers
- Duree : minimum 4 semaines, > 500 conversions par variant

**Outils** : Stripe (experiments), ProfitWell Retain, Chargebee, Paddle.

### Cohort Pricing

Tester differents prix sur differents segments geographiques (prix US vs Europe vs APAC souvent differents de 30-50%).

**Outil simple** : plans distincts par pays dans Stripe, mesurer les differences de conversion et MRR.

---

## Decision Guide — Quel Modele Choisir

| Contexte | Modele recommande | Raison |
|---|---|---|
| SaaS B2B, equipes | Per-seat | Simple, previsible, croissance naturelle |
| API / Infra | Usage-based | Aligne avec la valeur, faible friction |
| B2C large audience | Freemium | Viral, adoption masse |
| SMB + Enterprise | Tiered | Accommode differents budgets |
| Grande valeur creee, acheteurs rationnels | Value-based custom | Capture la valeur reelle |
| E-commerce / transactionnel | Pourcentage du volume | Aligne avec le succes client |

---

## Augmentation de Prix — Comment Proceder

1. **Justifier la valeur** : documenter les ameliorations produit depuis le dernier pricing, les benchmarks marche.
2. **Segmenter** : augmentation pour les nouveaux clients d'abord, puis migration progressive des existants.
3. **Grandfathering temporaire** : les clients anciens gardent leur prix 6-12 mois avec communication transparente.
4. **Communication proactive** : annoncer 60 jours avant. Ne jamais surprendre. Expliquer le "pourquoi valeur".
5. **Offrir un lock-in** : permettre aux clients de bloquer l'ancien prix s'ils passent annuel maintenant.

**Regle empirique** : une hausse de prix < 20% sur un produit B2B dont le client est satisfait entraine en moyenne < 5% de churn.

---

## Maturity Model — Pricing

| Niveau | Caracteristique |
|---|---|
| **1 — Intuitif** | Prix fixe "au doigt mouille", jamais testé, pas de segments |
| **2 — Cost-plus** | Prix base sur les couts + marge, competitive benchmarking basique |
| **3 — Structure** | Tiers clairs, packaging coherent, processus de revue annuelle |
| **4 — Value-based** | WTP mesure, pricing par segment, tests A/B sur les changements |
| **5 — Dynamique** | Usage-based sophistique, pricing ML-assisted, optimisation continue du mix |
