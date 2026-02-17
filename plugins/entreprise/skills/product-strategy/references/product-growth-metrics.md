# Product Growth & Metrics -- North Star, PLG, Retention & Unit Economics

## Overview

Ce document de reference couvre les metriques et frameworks essentiels pour piloter la croissance produit : North Star Metric, Product-Led Growth (PLG), onboarding et activation, retention et analyse de cohortes, expansion revenue, unit economics (LTV, CAC, payback) et metriques SaaS. Utiliser ce guide pour structurer chaque decision de croissance avec rigueur, en privilegiant les metriques actionnables aux vanity metrics et en reliant chaque indicateur a un levier d'action concret.

---

## North Star Metric Framework

La North Star Metric (NSM) est la metrique unique qui capture la valeur fondamentale delivree aux utilisateurs. Elle aligne l'organisation autour d'un objectif commun et reflete simultanement la valeur utilisateur et la valeur business.

**Criteres de selection d'une bonne NSM :**

| Critere | Question de validation | Exemple |
|---|---|---|
| **Valeur utilisateur** | Reflete-t-elle la valeur percue par l'utilisateur ? | "Rapports generes" (pas "logins") |
| **Leading indicator** | Est-elle predictive de la croissance future du revenu ? | La retention D30 predit le revenu a 6 mois |
| **Actionnable** | L'equipe produit peut-elle l'influencer directement ? | Eviter les metriques dependantes du marche |
| **Comprehensible** | Toute l'organisation la comprend-elle ? | Langage simple, pas de jargon |
| **Mesurable** | Peut-on la mesurer avec precision et frequence ? | Donnees disponibles quotidiennement |
| **Non-manipulable** | Resistante au gaming ? | "Taches completees" > "temps dans l'app" |

**NSM par type de business :**

| Type de business | North Star Metric | Input Metrics typiques |
|---|---|---|
| **SaaS B2B (productivite)** | Taches completees par semaine | Activation rate, DAU/WAU, features adoptees |
| **SaaS B2B (data/analytics)** | Rapports generes et partages | Time-to-first-report, sources connectees |
| **Marketplace** | Transactions completees | Offre listee, demande active, match rate |
| **Media / contenu** | Temps de consommation de qualite | DAU, temps par session, taux de completion |
| **E-commerce** | Repeat purchase rate | Conversion rate, panier moyen, NPS |
| **Fintech** | Volume de transactions mensuelles | Comptes actifs, transactions par user |

**Arbre de decision NSM :**

```
1. Quelle valeur fondamentale est delivree ?
   +-- Gain de temps / productivite --> Taches completees, temps economise
   +-- Revenu genere pour l'utilisateur --> Volume d'affaires, ROI mesurable
   +-- Connexion / collaboration --> Interactions, messages, partages
   +-- Contenu / information --> Consommation, engagement, retention

2. Frequence de perception de la valeur ?
   +-- Quotidienne --> Metrique DAU-based
   +-- Hebdomadaire --> Metrique WAU-based
   +-- Mensuelle --> Metrique MAU-based
```

Limiter a 3-5 input metrics. Chaque equipe possede un ou deux input metrics qu'elle pilote au quotidien.

---

## Product-Led Growth (PLG)

### Self-Serve Motion et Conditions Prealables

Le PLG repose sur la capacite du produit a se vendre lui-meme. Conditions prealables : time-to-value court (minutes, pas jours), complexite d'adoption faible, valeur demonstrable avant l'achat, ACV compatible avec le self-serve (< 15-20K EUR/an).

### Design du Freemium

| Strategie | Description | Exemple |
|---|---|---|
| **Feature-limited** | Features avancees reservees au tier payant | Slack : historique limite a 90 jours en free |
| **Usage-limited** | Toutes les features avec limites quantitatives | Airtable : limite de lignes |
| **Seat-limited** | Gratuit pour un nombre limite d'utilisateurs | Figma : gratuit pour 3 projets |
| **Reverse trial** | Acces premium temporaire puis downgrade | Ahrefs : 7 jours premium puis free |

Regles : le free tier doit permettre d'atteindre le "aha moment", la limite doit etre naturelle (liee a l'usage), l'upgrade doit coincider avec un moment de succes.

### Time-to-Value (TTV) Optimization

```
Benchmarks TTV :
+-- Excellent : < 5 minutes (Canva, Loom, Calendly)
+-- Bon : 5-30 minutes (Notion, Airtable)
+-- Acceptable : 30 min - 2 heures (HubSpot, Amplitude)
+-- Risque : > 2 heures --> Repenser le parcours
```

Tactiques : eliminer les champs non indispensables, proposer des templates pre-remplis, social login, guider vers la premiere action de valeur immediatement, reporter les configurations avancees.

### Activation Metrics

| Metrique | Formule | Benchmark |
|---|---|---|
| **Activation Rate** | Users au aha moment / Total inscrits | 20-40% (bon), > 40% (excellent) |
| **Time-to-Activate** | Temps median inscription --> aha moment | < 1 jour |
| **Setup Completion** | Users onboarding complet / Total inscrits | > 60% |

### Viral Loops

```
k-factor = i x c (i = invitations envoyees, c = taux de conversion des invites)
Si k > 1 : croissance virale autonome
Cycle Time = temps entre inscription et inscription des invites
```

| Type | Mecanisme | Exemple | Levier |
|---|---|---|---|
| **Inherente** | L'usage expose d'autres personnes | Calendly, Loom | Visibilite marque dans le flux |
| **Collaborative** | Meilleur a plusieurs | Slack, Figma | Friction d'invitation minimale |
| **Incitative** | Recompense pour l'invitation | Dropbox, Revolut | Reward alignee sur la valeur |
| **Word-of-mouth** | Recommandations organiques | Superhuman, Linear | NPS > 50, moments "wow" |

---

## Onboarding Optimization

### Identification du Aha Moment

1. **Hypothese qualitative** : interviewer 10-15 utilisateurs retenus ("Quand avez-vous compris la valeur ?")
2. **Analyse de correlation** : identifier les actions des 7 premiers jours correlees avec la retention D30+
3. **Segmentation** : comparer parcours retenus vs churnes
4. **Validation experimentale** : guider un groupe test vers l'action identifiee, mesurer l'impact

### Onboarding Progressif

```
Phase 1 — Premiere session (0-5 min)
+-- Objectif : premiere victoire (aha moment), 1-2 actions max

Phase 2 — Premier jour (5 min - 24h)
+-- Objectif : valeur secondaire, personnalisation legere

Phase 3 — Premiere semaine (J1-J7)
+-- Objectif : ancrer l'habitude, features avancees, integrations

Phase 4 — Premier mois (J7-J30)
+-- Objectif : activation complete, collaboration, workflows avances
```

### Checklists et Empty States

**Checklists** : 4-6 etapes max (effet Zeigarnik), premiere etape deja cochee, chaque etape mene a une action de valeur, recompense a la completion. **Empty states** : transformer chaque ecran vide en invitation a l'action avec templates, donnees d'exemple ou tutoriel contextuel. Le CTA doit mener a la premiere action de valeur.

### Activation Rate Benchmarks

| Segment | Median | Top quartile |
|---|---|---|
| **SaaS B2B (self-serve)** | 20-30% | > 40% |
| **SaaS B2B (sales-assisted)** | 30-50% | > 60% |
| **SaaS B2C** | 15-25% | > 35% |
| **Mobile apps** | 10-20% | > 25% |

---

## Retention Analysis

### Analyse de Cohortes

| Cohorte | M0 | M1 | M2 | M3 | M6 | M12 |
|---|---|---|---|---|---|---|
| **Jan 2025** | 100% | 45% | 35% | 30% | 25% | 20% |
| **Fev 2025** | 100% | 50% | 40% | 35% | 28% | -- |
| **Mar 2025** | 100% | 55% | 45% | 38% | -- | -- |

Lecture horizontale : evolution d'une cohorte dans le temps. Lecture verticale : comparaison entre cohortes au meme stade. Lecture diagonale : impact d'un evenement sur toutes les cohortes actives. Une courbe qui se stabilise (plateau) indique le PMF. Une courbe tendant vers zero indique un probleme fondamental.

### Retention Benchmarks (D1/D7/D30/D60/D90)

| Stade | SaaS B2B | SaaS B2C | Mobile App | Marketplace |
|---|---|---|---|---|
| **D1** | > 40% | > 25% | > 20% | > 30% |
| **D7** | > 25% | > 15% | > 10% | > 20% |
| **D30** | > 15% | > 8% | > 5% | > 12% |
| **D60** | > 12% | > 5% | > 3% | > 8% |
| **D90** | > 10% | > 4% | > 2% | > 6% |

### Churn Analysis

| Type | Definition | Action corrective |
|---|---|---|
| **Early churn** (< 30j) | Probleme d'activation ou de TTV | Optimiser l'onboarding |
| **Mid-term churn** (30-90j) | Valeur insuffisante, gap de features | Approfondir la proposition de valeur |
| **Late churn** (> 90j) | Changement de besoin ou concurrent | Expansion, switching costs |
| **Involuntary churn** | Echec de paiement, carte expiree | Dunning emails, retry logic, card updater |

### Strategies de Reactivation

```
1. Inactif recent (7-14 jours)
   +-- Email + in-app : rappel valeur + CTA action
   +-- Taux cible : 15-25%

2. Inactif moyen (15-30 jours)
   +-- Email + push : nouveautes + offre incitative
   +-- Taux cible : 8-15%

3. Inactif long (31-90 jours)
   +-- Sequence 3 emails : proposition de valeur repositionnee + social proof
   +-- Taux cible : 3-8%

4. Churne (> 90 jours)
   +-- Email trimestriel : annonces majeures + temoignages
   +-- Taux cible : 1-3%
```

---

## Expansion Revenue

### Mecanismes et NRR

| Mecanisme | Description | Declencheur |
|---|---|---|
| **Upsell** | Migration vers un tier superieur | Limites du tier atteintes |
| **Cross-sell** | Produit additionnel | Besoin adjacent identifie |
| **Seat expansion** | Ajout d'utilisateurs | Adoption par de nouvelles equipes |
| **Usage expansion** | Consommation accrue | Croissance naturelle de l'activite |

```
NRR = (MRR debut + Expansion - Contraction - Churn) / MRR debut x 100
+-- < 90% : modele fragile
+-- 100-110% : bon (expansion compense le churn)
+-- 110-130% : excellent (Datadog : 130%, Snowflake : 131%)
+-- > 130% : exceptionnel (Twilio historique : 155%)
```

### Product-Qualified Leads (PQL)

Le PQL est base sur le comportement produit, pas sur le telechargement d'un livre blanc.

| Signal | Poids |
|---|---|
| A atteint le aha moment | +30 pts |
| A invite 2+ coequipiers | +20 pts |
| A visite la pricing page | +15 pts |
| A atteint une limite du free tier | +15 pts |
| Usage croissant sur 7 jours | +15 pts |
| Match ICP (> 50 employes) | +10 pts |
| **Seuil PQL : >= 70 pts** | **Transmission au Sales** |

---

## Product Analytics Stack

| Critere | Amplitude | Mixpanel | PostHog | Segment |
|---|---|---|---|---|
| **Type** | Product analytics | Product analytics | Analytics + session replay | CDP |
| **Force** | Behavioral analytics, cohortes | Event analytics, funnels | Open source, all-in-one | Collecte, routage, integrations |
| **Self-hosted** | Non | Non | Oui | Non |
| **Free tier** | 50M events/mois | 20M events/mois | 1M events (cloud), illimite (self-hosted) | 1 000 visitors/mois |
| **Experimentation** | Oui (natif) | Non | Oui (feature flags + A/B) | Non |
| **Ideal pour** | Equipes matures, analyse avancee | Startups, mid-market | Startups tech, privacy | Hub de donnees unifie |

```
1. Besoin principal ?
   +-- Collecter et router les donnees --> Segment
   +-- Analyser le comportement utilisateur --> Aller a 2

2. Budget limite ou besoin self-hosting ?
   +-- Oui --> PostHog
   +-- Non --> Aller a 3

3. Maturite analytics ?
   +-- Avancee --> Amplitude
   +-- Intermediaire --> Mixpanel ou Amplitude
   +-- Debutante --> PostHog ou Mixpanel
```

---

## Unit Economics

### LTV — Trois Methodes de Calcul

**Methode 1 -- Simple :** LTV = ARPA mensuel x Gross Margin % / Monthly Churn Rate. Exemple : 200 x 0.80 / 0.03 = 5 333 EUR.

**Methode 2 -- Avec expansion :** LTV = ARPA mensuel x Gross Margin % / (Churn Rate - Expansion Rate). Exemple : 200 x 0.80 / (0.03 - 0.015) = 10 667 EUR. Condition : churn > expansion.

**Methode 3 -- Par cohorte (la plus precise) :** Sommer le revenu reel de chaque cohorte mois par mois. Necessite 12-24 mois de donnees historiques.

### CAC par Canal

| Canal | CAC median (SaaS B2B) | Payback | Scalabilite |
|---|---|---|---|
| **Organique (SEO/content)** | 200-800 EUR | 3-12 mois | Elevee |
| **Paid Search** | 500-2 000 EUR | 6-18 mois | Moyenne |
| **Paid Social (LinkedIn)** | 800-2 500 EUR | 8-18 mois | Moyenne |
| **Outbound (SDR/BDR)** | 1 500-5 000 EUR | 12-24 mois | Lineaire |
| **PLG / self-serve** | 50-300 EUR | 1-6 mois | Tres elevee |
| **Referral / viral** | 30-200 EUR | 1-3 mois | Tres elevee |

### LTV:CAC et Payback

| LTV:CAC | Interpretation | Action |
|---|---|---|
| **< 1.0** | Chaque client detruit de la valeur | Revoir le modele |
| **1.0 - 3.0** | Insuffisant | Ameliorer retention ou reduire CAC |
| **3.0 - 5.0** | Zone saine | Scaler l'acquisition |
| **> 5.0** | Sous-investissement probable | Accelerer l'acquisition |

```
Payback = CAC / (ARPA mensuel x Gross Margin %)
+-- SaaS SMB : < 6 mois (excellent), 6-12 mois (bon)
+-- SaaS Mid-Market : < 12 mois (excellent), 12-18 mois (acceptable)
+-- SaaS Enterprise : < 18 mois (excellent), 18-24 mois (acceptable)
```

### Benchmarks par Stade

| Metrique | Seed | Serie A | Serie B+ | Scale |
|---|---|---|---|---|
| **LTV:CAC** | > 2:1 | > 3:1 | > 3:1 | > 4:1 |
| **Payback** | < 18 mois | < 12 mois | < 12 mois | < 9 mois |
| **Gross Margin** | > 60% | > 70% | > 75% | > 80% |
| **NRR** | > 90% | > 100% | > 110% | > 120% |

---

## SaaS Metrics Dashboard

| Metrique | Formule | Benchmark |
|---|---|---|
| **MRR** | Somme abonnements mensuels recurrents | MoM > 10% (early), > 5% (growth) |
| **ARR** | MRR x 12 | Seuils : 1M, 10M, 100M EUR |
| **Logo Churn** | Clients perdus / Clients debut mois | SMB < 5%/mois ; Enterprise < 1%/mois |
| **Revenue Churn** | MRR perdu / MRR debut mois | < 2%/mois (SMB), < 0.5% (Enterprise) |
| **NRR** | (MRR + Expansion - Contraction - Churn) / MRR | > 110% (bon), > 120% (excellent) |
| **ARPU** | MRR / Nombre de clients | Croissant dans le temps |
| **DAU/MAU** | Actifs quotidiens / mensuels | > 20% (B2B), > 50% (outil quotidien) |
| **Quick Ratio** | (New + Expansion MRR) / (Churn + Contraction MRR) | > 4 (excellent), > 2 (sain) |
| **Rule of 40** | Growth Rate % + EBITDA Margin % | > 40% (sain) |
| **Magic Number** | Net New ARR (QoQ) / S&M Spend (Q-1) | > 0.75 (efficient), > 1.0 (excellent) |
| **Burn Multiple** | Net Burn / Net New ARR | < 1.5x (efficient) |

**MRR Waterfall (exemple) :**

```
MRR Debut : 500K EUR
  + New MRR :        +60K (nouveaux clients)
  + Expansion MRR :  +35K (upsell, seats)
  - Contraction MRR : -10K (downgrades)
  - Churned MRR :    -25K (clients perdus)
  = MRR Fin : 560K EUR (+12% MoM)
Quick Ratio = (60 + 35) / (10 + 25) = 2.7
```

---

## State of the Art (2025-2026)

### AI-Powered Analytics

- **Anomaly detection automatique** : Amplitude AI, PostHog et Statsig detectent les variations anormales et alertent avant l'aggravation. Plus besoin de surveiller manuellement des dizaines de dashboards.
- **Natural language querying** : interroger les donnees en langage naturel sans SQL ni configuration de funnels.
- **Automated insight generation** : identification automatique des segments a forte retention, parcours d'activation optimaux et correlations actions-outcomes.

### Predictive Retention

- **Churn prediction scoring** : score de risque par client en temps reel base sur les patterns d'usage (frequence en baisse, features abandonees, tickets repetitifs). Le customer success intervient proactivement.
- **Next best action** : recommandation automatique de l'action la plus susceptible de retenir un utilisateur a risque.
- **LTV prediction** : estimation du LTV individuel des le premier mois pour allouer les ressources CSM aux comptes a fort potentiel.

### Automated Experimentation

- **Multi-armed bandit** : allocation automatique du trafic aux variantes gagnantes, reduisant le cout d'opportunite vs A/B tests classiques.
- **Feature experimentation at scale** : gestion de centaines d'experiments simultanees avec controle des interactions (Statsig, Eppo, LaunchDarkly).
- **AI-generated hypotheses** : l'IA suggere des hypotheses d'experimentation basees sur l'analyse des donnees d'usage.

### Convergence PLG et Product-Led Sales (PLS)

- **Automated PQL routing** : les signaux produit declenchent automatiquement des workflows de sales outreach via Pocus, Correlated ou Endgame.
- **Reverse trials** : commencer par le tier premium puis downgrade vers le free tier. Augmente les conversions de 20-40% vs free trial classique.

### Metrics AI-Native

- **AI feature adoption rate** : % d'utilisateurs actifs sur les features IA
- **Cost per inference** : cout unitaire de chaque appel IA, directement lie a la marge brute
- **AI gross margin** : 50-65% typique (vs 75-85% SaaS traditionnel)
- **Token efficiency** : ratio valeur delivree / tokens consommes, optimisable par prompt engineering et caching
