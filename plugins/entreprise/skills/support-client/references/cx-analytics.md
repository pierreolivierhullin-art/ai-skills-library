# CX & Analytics — Voice of Customer, NPS/CSAT/CES, Journey Mapping & Support Metrics

## Overview

Ce document de reference couvre la mesure et l'optimisation de l'experience client (CX) : programmes Voice of Customer, deploiement NPS/CSAT/CES, journey mapping, service blueprinting, analytics support et forecasting. La CX est la somme de toutes les interactions qu'un client a avec une entreprise. La mesurer et l'ameliorer systematiquement est le levier le plus puissant de retention et de croissance. Utiliser ce guide pour concevoir et piloter un programme CX data-driven.

---

## Voice of Customer (VoC) Programs

### Architecture d'un programme VoC

Un programme VoC mature collecte, analyse et agit sur le feedback client de maniere systematique a travers trois piliers :

**Pilier 1 — Feedback Sollicite (Ask)**
- Enquetes NPS, CSAT, CES transactionnelles et relationnelles.
- Enquetes thematiques (onboarding feedback, product feedback, exit surveys).
- Interviews client approfondies (1-on-1) pour les insights qualitatifs.
- Focus groups pour tester des concepts ou des evolutions.
- Advisory boards pour les clients strategiques.

**Pilier 2 — Feedback Non Sollicite (Listen)**
- Analyse des tickets support (themes, sentiment, tendances).
- Analyse des avis publics (G2, Capterra, Trustpilot, App Store).
- Social listening (mentions sur X/Twitter, LinkedIn, Reddit, forums).
- Analyse des conversations de vente (appels enregistres, emails).
- Feedback in-app spontane (widget "Feedback" dans le produit).

**Pilier 3 — Feedback Comportemental (Observe)**
- Product analytics (patterns d'usage, friction points, drop-offs).
- Session recordings (Hotjar, FullStory, Clarity) pour observer le comportement.
- Heatmaps pour identifier les zones d'interaction et de confusion.
- A/B testing pour valider les hypotheses d'amelioration.
- Funnel analytics pour identifier les points de chute.

### VoC Data Integration

Centraliser toutes les sources de feedback dans un repository unique :

```
Sources de feedback
+-- Enquetes (Typeform, SurveyMonkey, Delighted, Qualtrics)
+-- Tickets support (Zendesk, Intercom, Freshdesk)
+-- Avis publics (G2, Capterra, Trustpilot)
+-- Social media (Sprout Social, Brandwatch, Mention)
+-- Product analytics (Amplitude, Mixpanel, Pendo)
+-- Sales conversations (Gong, Chorus)
|
v
[VoC Platform / Data Warehouse]
|
v
[Analyse : themes, sentiment, tendances, correlations]
|
v
[Actions : closed-loop, product roadmap, process improvement]
```

**Outils VoC dedies** : Medallia, Qualtrics XM, InMoment, Chattermill, MonkeyLearn.
**Approche pragmatique (budget limite)** : centraliser dans un spreadsheet ou un outil BI (Metabase, Looker) avec des imports reguliers des differentes sources.

---

## NPS / CSAT / CES — Implementation Detaillee

### Net Promoter Score (NPS)

**Question** : "Sur une echelle de 0 a 10, quelle est la probabilite que vous recommandiez [Produit] a un collegue ou ami ?"

**Calcul** : NPS = % Promoteurs (9-10) - % Detracteurs (0-6). Plage : -100 a +100.

**Types de NPS** :

| Type | Frequence | Cible | Objectif |
|---|---|---|---|
| **Relational NPS (rNPS)** | Trimestriel ou semestriel | Tous les clients actifs | Mesurer la satisfaction globale et son evolution |
| **Transactional NPS (tNPS)** | Post-evenement | Clients ayant vecu l'evenement | Mesurer la satisfaction sur un touchpoint specifique |

**Implementation du rNPS** :

1. **Frequence** : trimestriel pour les SaaS B2B, semestriel pour les grands comptes. Ne pas envoyer plus de 4 fois/an.
2. **Echantillonnage** : envoyer a tous les clients actifs (pas d'echantillonnage si la base < 10 000 clients). Pour les grandes bases, echantillonner aleatoirement avec stratification par segment.
3. **Timing** : eviter les periodes de facturation, les vacances et les 48h suivant un incident. Envoyer en milieu de semaine (mardi-jeudi), en fin de matinee.
4. **Canal** : email pour le B2B (taux de reponse 15-30%), in-app pour le B2C/PLG (taux de reponse 20-40%).
5. **Follow-up question** : toujours inclure une question ouverte : "Qu'est-ce qui explique principalement votre note ?" Le qualitatif est plus actionnable que le score.
6. **Taux de reponse** : viser > 20% pour la significativite statistique. Un taux < 10% indique un probleme de methode.

**Analyse du NPS** :

- Segmenter par : plan/tier, anciennete, usage, industrie, taille entreprise.
- Analyser les themes des commentaires par segment (promoteurs : qu'est-ce qu'ils aiment ? detracteurs : qu'est-ce qui les frustre ?).
- Tracker la tendance trimestrielle, pas le score absolu. Une amelioration de +5 points/trimestre est significative.
- Calculer le "NPS Economics" : correlations entre NPS et retention, expansion, referral.

### Customer Satisfaction Score (CSAT)

**Question** : "Comment evaluez-vous votre satisfaction concernant [interaction specifique] ?" (echelle 1-5 ou 1-7)

**Calcul** : CSAT = (Nombre de reponses 4-5 / Nombre total de reponses) x 100.

**Cas d'usage du CSAT** :

| Touchpoint | Quand envoyer | Delai | Canal | Cible |
|---|---|---|---|---|
| Post-ticket support | A la resolution | Immediat | Email / In-app | > 85% |
| Post-chat | Fin de conversation | Immediat | Widget chat | > 85% |
| Post-appel | Fin de l'appel | < 1h | SMS / Email | > 88% |
| Post-onboarding | Fin du parcours onboarding | J30 | Email | > 80% |
| Post-achat | Apres la premiere commande | J3-J7 | Email | > 80% |
| Post-feature release | Apres utilisation d'une nouvelle feature | J7-J14 | In-app | > 75% |

**Bonnes pratiques CSAT** :

1. **Question unique** : ne pas combiner CSAT avec d'autres questions dans la meme enquete. Maximum : 1 question de scoring + 1 question ouverte.
2. **Contextualisation** : toujours preciser le sujet de la satisfaction ("Concernant votre ticket #12345..."), pas une satisfaction generique.
3. **Taux de reponse** : viser > 25% sur les enquetes post-ticket. Envoyer dans les 2h suivant la resolution pour maximiser le taux.
4. **Analyse par canal** : comparer la CSAT entre les canaux (chat vs email vs telephone) pour identifier les canaux sous-performants.
5. **Agent-level CSAT** : mesurer la CSAT par agent pour le coaching et la QA (avec un minimum de 20 reponses par agent pour la significativite).

### Customer Effort Score (CES)

**Question** : "[Entreprise] a rendu facile la resolution de mon probleme." (echelle 1-7, de "Pas du tout d'accord" a "Tout a fait d'accord")

**Calcul** : CES = moyenne des reponses (variante : % de reponses 5-7 / total).

**Pourquoi le CES est crucial** :
Le CES est le meilleur predicteur de fidelite client (Matthew Dixon, "The Effortless Experience", 2013). Reduire l'effort client a un impact plus fort sur la retention que surpasser les attentes. 96% des clients avec une experience a fort effort deviennent infideles vs 9% des clients avec une experience a faible effort.

**Implementation du CES** :

1. **Post-interaction** : envoyer apres chaque interaction support (ticket, chat, self-service).
2. **Post-process** : envoyer apres des processus complexes (onboarding, migration, integration).
3. **Post-self-service** : mesurer l'effort percu sur les parcours self-service (KB, chatbot).
4. **Analyse des drivers** : identifier les facteurs d'effort eleve — nombre de canaux utilises, nombre de contacts, temps d'attente, nombre de transferts, besoin de repeter le probleme.

**CES Action Framework** :

| Score CES | Interpretation | Action |
|---|---|---|
| 6-7 | Effort minimal | Documenter les best practices, repliquer |
| 5 | Effort modere | Identifier les petites frictions a eliminer |
| 3-4 | Effort eleve | Revoir le processus, simplifier les etapes |
| 1-2 | Effort extreme | Intervention immediate, redesign du processus |

---

## Customer Journey Mapping

### Methodologie de Journey Mapping

Le customer journey map est une representation visuelle de l'experience du client a travers tous les touchpoints avec l'entreprise.

**Etape 1 — Definir le scope**
- Choisir le persona cible (un seul persona par map).
- Definir le debut et la fin du journey (ex : de la decouverte au renouvellement, ou un sous-journey comme l'onboarding).
- Identifier l'objectif du client dans ce journey.

**Etape 2 — Cartographier les phases**
Decouper le parcours en 5-8 phases principales :

```
[Decouverte] -> [Evaluation] -> [Achat] -> [Onboarding] -> [Utilisation] -> [Support] -> [Renouvellement/Expansion]
```

**Etape 3 — Pour chaque phase, documenter :**

| Element | Description | Exemple |
|---|---|---|
| **Actions client** | Ce que le client fait | Recherche Google, visite site, demo, ticket support |
| **Touchpoints** | Points de contact avec l'entreprise | Site web, email, chat, telephone, produit, facture |
| **Thoughts** | Ce que le client pense | "Est-ce que ca va resoudre mon probleme ?" |
| **Emotions** | Ce que le client ressent (satisfaction -> frustration) | Enthousiasme lors de la demo, frustration lors du setup |
| **Pain Points** | Points de douleur identifies | Temps d'attente long au support, documentation confuse |
| **Opportunities** | Opportunites d'amelioration | Chatbot pour les questions frequentes, guide interactif |
| **Metrics** | Mesure de l'experience a ce point | CSAT post-onboarding, CES post-support |

**Etape 4 — Visualiser le parcours emotionnel**
Tracer une courbe emotionnelle sur le journey : ou le client est satisfait (peaks) et ou il est frustre (valleys). Les valleys sont les priorites d'amelioration.

**Etape 5 — Prioriser les actions**
Pour chaque pain point identifie :
- Impact : combien de clients sont concernes ? Quel est l'impact sur la retention ?
- Effort : combien de ressources sont necessaires pour resoudre ?
- Prioriser par ratio impact/effort.

### Service Blueprinting

Le service blueprint etend le journey map en ajoutant les processus internes necessaires pour delivrer l'experience.

**Couches du service blueprint** :

```
+----------------------------------------------------------+
| CUSTOMER ACTIONS    | Ce que le client fait/voit          |
|----------------------------------------------------------+
| FRONTSTAGE          | Actions visibles (agent, UI, email) |
| (Ligne de visibilite)                                     |
|----------------------------------------------------------+
| BACKSTAGE           | Actions internes invisibles          |
|                     | (traitement ticket, escalade, etc.) |
|----------------------------------------------------------+
| SUPPORT PROCESSES   | Systemes, outils, processus         |
|                     | (CRM, ticketing, KB, monitoring)    |
+----------------------------------------------------------+
```

**Quand utiliser le service blueprint** :
- Redesign d'un processus support (ex : parcours d'escalade).
- Lancement d'un nouveau canal de support.
- Diagnostic d'une experience client degradee.
- Onboarding d'une nouvelle equipe sur les processus existants.

### Touchpoint Optimization

Pour chaque touchpoint identifie dans le journey map :

1. **Mesurer** : associer une metrique CX (CSAT, CES, NPS transactionnel).
2. **Benchmarker** : comparer la performance du touchpoint vs les autres touchpoints et vs les benchmarks sectoriels.
3. **Identifier les gaps** : les touchpoints avec un score < moyenne - 1 ecart-type sont prioritaires.
4. **Optimiser** : appliquer la methode PDCA (Plan-Do-Check-Act) sur les touchpoints prioritaires.
5. **Monitorer** : suivre l'evolution post-optimisation pendant 90 jours minimum.

---

## Closed-Loop Feedback

### Le processus closed-loop

Le closed-loop feedback est le processus systematique de suivi de chaque feedback client negatif :

```
[Feedback negatif recu] -> [Alerte automatique] -> [Prise en charge] -> [Contact client]
         |                                                                     |
         v                                                                     v
   [Categorisation]                                                  [Resolution / Action]
         |                                                                     |
         v                                                                     v
   [Root Cause Analysis]                                           [Confirmation client]
         |                                                                     |
         v                                                                     v
   [Action systemique]                                             [Cloture + Suivi]
   (process improvement,
    product fix, training)
```

### Inner Loop (Individuel)

**Objectif** : repondre a chaque detracteur individuellement dans les 48h.

1. **Alerte** : le systeme detecte un feedback negatif (NPS 0-6, CSAT 1-2, CES 1-3) et alerte le CSM ou l'agent responsable.
2. **Preparation** : avant de contacter le client, revoir l'historique complet (tickets, usage, interactions precedentes).
3. **Contact** : appeler le client (prefere a l'email pour les detracteurs). Ecouter activement, valider l'emotion, comprendre la cause racine.
4. **Action** : resoudre le probleme immediat ou proposer un plan d'action avec un delai.
5. **Suivi** : re-contacter a la date promise pour confirmer la resolution.
6. **Documentation** : documenter la cause, l'action et le resultat dans le CRM/CS platform.

**Impact mesure** : 50% des detracteurs NPS recontactes dans les 48h passent en passif ou promoteur. Le churn des detracteurs contacts est 30-40% inferieur a celui des detracteurs non contacts.

### Outer Loop (Systemique)

**Objectif** : identifier les causes racines recurrentes et les traiter structurellement.

1. **Aggregation** : regrouper les feedbacks par theme/cause (mensuel).
2. **Priorisation** : classer les themes par frequence x impact.
3. **Root Cause Analysis** : pour les top 5 themes, conduire une analyse causale (5 Whys, Ishikawa).
4. **Action Plan** : definir des actions correctives assignees a des owners avec des deadlines.
5. **Implementation** : executer les actions (fix produit, amelioration process, formation equipe).
6. **Validation** : mesurer l'impact a 90 jours (reduction du theme dans les feedbacks, amelioration du score).
7. **Communication** : informer les clients que leur feedback a conduit a des ameliorations ("You asked, we listened").

---

## Support Analytics

### Metrics Framework

Organiser les metriques support en quatre categories :

#### Efficiency Metrics (Performance operationnelle)

| Metrique | Definition | Calcul | Cible | Frequence |
|---|---|---|---|---|
| **AHT (Average Handle Time)** | Temps moyen de traitement d'un ticket | (Temps de travail agent + temps d'attente) / nombre de tickets | Email: 10-15 min, Chat: 8-12 min, Phone: 6-8 min | Quotidien |
| **First Response Time (FRT)** | Temps avant la premiere reponse | Heure premiere reponse - heure creation ticket | < SLA par priorite | Quotidien |
| **Resolution Time** | Temps entre creation et resolution | Heure resolution - heure creation (hors temps "en attente client") | P1: 4h, P2: 8h, P3: 24h | Quotidien |
| **Agent Utilization** | % du temps agent passe sur des tickets | Temps sur tickets / temps total disponible | 70-80% | Hebdomadaire |
| **Cost per Ticket** | Cout moyen de resolution d'un ticket | Cout total support / nombre de tickets resolus | SaaS B2B: 8-15 EUR | Mensuel |
| **Cost per Contact** | Cout moyen par interaction | Cout total canal / nombre interactions | Chat: 5 EUR, Phone: 8-12 EUR, Email: 6-10 EUR | Mensuel |

#### Quality Metrics (Qualite de la resolution)

| Metrique | Definition | Calcul | Cible | Frequence |
|---|---|---|---|---|
| **FCR (First Contact Resolution)** | % de tickets resolus au premier contact | Tickets resolus sans reouverture ni relance / total tickets | > 75% | Hebdomadaire |
| **Reopen Rate** | % de tickets rouverts apres resolution | Tickets rouverts / tickets resolus | < 5% | Hebdomadaire |
| **QA Score** | Score qualite des interactions evaluees | Moyenne des scores QA par agent | > 80/100 | Mensuel |
| **Escalation Rate** | % de tickets escalades | Tickets escalades / total tickets | < 15% | Hebdomadaire |
| **Transfer Rate** | Nombre moyen de transferts par ticket | Total transferts / total tickets | < 1.5 | Hebdomadaire |
| **One-Touch Resolution** | % de tickets resolus en une seule reponse | Tickets resolus en 1 reponse / total tickets | > 40% | Mensuel |

#### Customer Impact Metrics (Impact client)

| Metrique | Definition | Calcul | Cible | Frequence |
|---|---|---|---|---|
| **CSAT** | Satisfaction client post-interaction | % de reponses positives (4-5/5) | > 85% | Continu |
| **CES** | Effort percu par le client | Moyenne des scores CES | > 5.5/7 | Continu |
| **NPS** | Propension a recommander | % promoteurs - % detracteurs | > 30 (bon), > 50 (excellent) | Trimestriel |
| **Self-Service Resolution Rate** | % de questions resolues en self-service | 1 - (tickets / (tickets + visites KB reussies)) | > 40% | Mensuel |
| **Deflection Rate** | % de contacts evites par le self-service | Interactions chatbot resolues / (chatbot + tickets) | > 30% | Mensuel |
| **Customer Wait Time** | Temps d'attente avant interaction | Heure premiere interaction - heure demande | Chat: < 30s, Phone: < 60s | Temps reel |

#### Strategic Metrics (Impact business)

| Metrique | Definition | Calcul | Cible | Frequence |
|---|---|---|---|---|
| **Support-Influenced Churn** | % de churn lie a une mauvaise experience support | Churn avec tickets negatifs / total churn | < 20% du churn | Trimestriel |
| **Support-Influenced NRR** | Impact du support sur la retention revenue | NRR des comptes avec CSAT > 4 vs CSAT < 3 | Delta > 15 points | Trimestriel |
| **Cost to Serve Ratio** | Cout support / revenue client | Cout support / ARR | < 5% (SaaS B2B) | Trimestriel |
| **Support ROI** | Retour sur investissement du support | (Churn evite x ARR + upsell assiste) / cout support | > 3x | Annuel |

### Agent Performance Dashboard

Pour chaque agent, tracker :

| Metrique | Calcul | Seuil OK | Seuil alerte |
|---|---|---|---|
| CSAT individuel | CSAT sur ses tickets (min 20 reponses) | > 85% | < 75% |
| FCR individuel | % de tickets resolus au premier contact | > 70% | < 55% |
| AHT individuel | Temps moyen de traitement | +/- 20% de la moyenne equipe | > 50% au-dessus |
| Volume traite | Tickets resolus / jour | > 80% de la capacite | < 60% |
| QA Score | Score moyen des evaluations QA | > 80/100 | < 70/100 |
| Reopen Rate | % de tickets rouverts | < 5% | > 10% |
| Backlog individuel | Tickets ouverts assignes | < 15 | > 25 |

**Attention** : ne pas utiliser les metriques individuelles de maniere punitive. Elles servent au coaching et a l'identification des besoins de formation. Un AHT eleve peut indiquer des tickets plus complexes, pas necessairement une performance faible.

---

## Ticket Volume Forecasting

### Methodes de prevision

**1. Methode historique simple**
Utiliser la moyenne mobile des 4-8 dernieres semaines ajustee par la saisonnalite. Convient pour les equipes avec un volume stable.

```
Prevision(semaine N) = Moyenne(semaines N-4 a N-1) x Coefficient_saisonnier(semaine N)
```

**2. Methode par regression**
Modeliser le volume en fonction de variables explicatives :
- Nombre de clients actifs (correlation forte)
- Releases recentes (pic de +20-40% dans les 48h post-release)
- Jour de la semaine (lundi et mardi = pic, vendredi = creux)
- Saisonnalite (fin de trimestre, Black Friday, renouvellements)
- Incidents en cours (pic proportionnel a l'impact)

**3. ML-Based Forecasting**
Pour les equipes avec un volume > 5000 tickets/mois et un historique > 12 mois, les modeles ML (Prophet de Facebook/Meta, ARIMA, LSTM) offrent des previsions plus precises. Integrer les features contextuelles : calendrier de releases, campagnes marketing, incidents.

### Staffing Based on Forecast

Convertir la prevision de volume en besoin de staffing :

```
Agents necessaires = (Volume prevu x AHT moyen) / (Heures disponibles par agent x Utilization cible)

Exemple :
- Volume prevu : 2000 tickets/semaine
- AHT moyen : 12 min (0.2h)
- Heures disponibles par agent : 35h/semaine
- Utilization cible : 75%

Agents necessaires = (2000 x 0.2) / (35 x 0.75) = 400 / 26.25 = 15.2 -> 16 agents

+ Buffer (15% absences/formation) = 16 x 1.15 = 18.4 -> 19 agents
```

---

## State of the Art (2024-2026)

### Tendances majeures

**1. AI-Powered CX Analytics**
L'IA generative transforme l'analyse CX. En 2024-2025, l'analyse de sentiment et de themes dans les feedbacks clients atteint une precision de 85-90% grace aux LLM. En 2025-2026, les plateformes CX (Qualtrics, Medallia, InMoment) integrent des "CX Copilots" qui synthetisent automatiquement les insights, identifient les tendances emergentes et proposent des actions prioritaires. L'analyse qui prenait 2 jours prend desormais 2 minutes.

**2. Real-Time Experience Management**
Le shift du "measure after the fact" vers le "detect and act in real-time". Les plateformes modernes detectent les experiences negatives en temps reel (sentiment negatif dans un chat, friction in-app, attente excessive) et declenchent des interventions immediates (escalade, offre compensatoire, contact proactif). Le "closed-loop" passe de 48h a < 1h pour les interactions en temps reel.

**3. Predictive CX**
Les modeles ML predisent la satisfaction future a partir des signaux comportementaux. Au lieu de mesurer le NPS apres-coup, les entreprises predisent le "Predicted NPS" pour chaque client et interviennent avant que la satisfaction ne se degrade. La precision des modeles predictifs atteint 75-80% en 2025, contre 60% en 2023.

**4. Journey Analytics Platforms**
L'evolution du journey mapping statique (PowerPoint) vers le journey analytics dynamique. Des outils comme Pointillist (Genesys), Thunderhead, et Adobe Journey Optimizer analysent les parcours reels (pas les parcours desires) a partir des donnees comportementales. Ils identifient automatiquement les parcours qui menent au churn, a la conversion ou a la satisfaction.

**5. Emotion AI & Sentiment Detection**
L'analyse des emotions dans les interactions support se sophistique. Au-dela du sentiment positif/negatif, les outils detectent la frustration, la confusion, l'urgence et l'enthousiasme en temps reel dans le texte, la voix et meme la video. Ces signaux emotionnels enrichissent le routing (escalade immediate si frustration elevee), le coaching agent (feedback en temps reel sur le ton) et les analytics CX (correlations entre emotions et outcomes).

**6. Unified Customer Data Platforms (CDP) pour CX**
La convergence entre les Customer Data Platforms (CDP) et les outils CX permet une personnalisation de l'experience basee sur l'ensemble des donnees client : comportement produit, historique support, transactions, profil demographique, preferences. Les CDP (Segment, mParticle, Rudderstack) alimentent les outils CX avec des profils enrichis en temps reel pour des experiences hyper-personnalisees.

**7. CX Governance & Accountability**
Les organisations les plus matures mettent en place une gouvernance CX structuree : un CX Council cross-fonctionnel (Support, Product, Sales, Marketing, CS) se reunit mensuellement pour revoir les metriques CX, prioriser les initiatives d'amelioration et mesurer les resultats. Le CX devient un KPI de performance au niveau executive, souvent lie a la remuneration variable du management.

**8. Sustainability & Ethics in CX Measurement**
Les pratiques de mesure CX evoluent vers plus d'ethique et de respect : consentement explicite pour les enquetes, transparence sur l'utilisation des donnees, reduction de la "survey fatigue" via l'inference IA (predire la satisfaction au lieu de la demander), respect du RGPD et des preferences de communication. Les entreprises les plus avancees communiquent publiquement leur NPS et leurs engagements d'amelioration.

### Benchmarks CX Analytics 2025

| Metrique | SaaS B2B | E-commerce | Services financiers | Telecom |
|---|---|---|---|---|
| NPS moyen | 30-45 | 40-55 | 20-35 | 10-25 |
| CSAT moyen | 82-88% | 78-85% | 75-82% | 70-78% |
| CES moyen | 5.2-5.8/7 | 5.0-5.6/7 | 4.5-5.2/7 | 4.0-4.8/7 |
| Survey Response Rate (NPS) | 20-30% | 10-20% | 15-25% | 8-15% |
| Closed-Loop Rate (detracteurs) | 50-70% | 20-40% | 40-60% | 25-40% |
| Time to Close Loop | 24-48h | 48-72h | 24-72h | 48-96h |
| CX-Driven Initiatives / Quarter | 5-10 | 3-8 | 4-8 | 3-6 |

### Outils CX Analytics — Panorama 2025

| Outil | Specialite | Taille cible | Prix indicatif |
|---|---|---|---|
| **Qualtrics XM** | Plateforme VoC complete, survey + analytics + action | Enterprise | 25K+ EUR/an |
| **Medallia** | Experience management enterprise, real-time | Enterprise | 30K+ EUR/an |
| **Delighted** | NPS/CSAT/CES simple et elegant | SMB-Mid | 2K+ EUR/an |
| **Hotjar** | Behavior analytics (heatmaps, recordings, feedback) | All sizes | 0-400 EUR/mois |
| **FullStory** | Digital experience analytics, session replay | Mid-Enterprise | 5K+ EUR/an |
| **Chattermill** | Analyse AI des feedbacks textuels | Mid-Enterprise | 10K+ EUR/an |
| **Pointillist** | Journey analytics dynamique | Enterprise | 20K+ EUR/an |
| **Amplitude** | Product analytics (complementaire CX) | All sizes | 0-50K EUR/an |
| **Zendesk Explore** | Analytics support natif | All sizes | Inclus dans Zendesk |
| **Metabase / Looker** | BI generaliste pour dashboards custom | All sizes | 0-30K EUR/an |
