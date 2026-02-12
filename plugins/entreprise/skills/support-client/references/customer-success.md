# Customer Success — Health Scoring, Proactive Engagement & Churn Prevention

## Overview

Ce document de reference couvre l'ensemble des pratiques du Customer Success Management (CSM) : health scoring, engagement proactif, prevention du churn, Quarterly Business Reviews, expansion/upsell, et outillage. Le Customer Success est la discipline qui transforme les clients en partenaires de long terme et le support en levier de croissance. Utiliser ce guide pour structurer et optimiser un programme CS aligné sur la retention et l'expansion du revenue.

---

## Customer Success Foundations

### CS vs Support — Distinction fondamentale

| Dimension | Customer Support | Customer Success |
|---|---|---|
| **Posture** | Reactive (le client vient) | Proactive (on va vers le client) |
| **Objectif** | Resoudre le probleme actuel | Garantir la valeur a long terme |
| **Metrique nord** | CSAT, FCR | Net Revenue Retention (NRR) |
| **Horizon** | Interaction par interaction | Cycle de vie client complet |
| **Declencheur** | Ticket / Demande client | Donnees, signaux, milestones |
| **Couvre** | Tous les clients | Comptes segmentes (high-touch a tech-touch) |

Les deux fonctions sont complementaires et doivent partager les donnees et les insights. Un probleme de support recurrent est un signal pour le CS ; une initiative CS (onboarding, training) reduit le volume de support.

### Customer Lifecycle Stages

Definir le parcours client en phases avec des objectifs et des playbooks specifiques :

```
[Acquisition] -> [Onboarding] -> [Adoption] -> [Value Realization] -> [Expansion] -> [Renewal]
                      |               |                |                    |              |
                      v               v                v                    v              v
                 Time-to-Value   Feature Depth    ROI Mesurable       Upsell/Cross    Renouvellement
                   (< 14j)       (> 5 features)   (QBR proof)         (NRR > 110%)    (GRR > 90%)
```

**Metriques cles par phase** :

| Phase | Duree typique | Metrique | Cible | Action CS |
|---|---|---|---|---|
| Onboarding | 14-30 jours | Time-to-First-Value (TTFV) | < 14j | Kickoff call, setup guide, check-ins |
| Adoption | 30-90 jours | Feature Adoption Rate | > 5 features cles | Training, use case workshops |
| Value Realization | 90-180 jours | ROI mesurable, objectifs atteints | ROI > 3x | QBR, business reviews, case study |
| Expansion | 180+ jours | Net Revenue Retention | > 110% | Upsell proposals, cross-sell, referral |
| Renewal | -90j avant echeance | Gross Revenue Retention | > 90% | Renewal planning, negotiation |

---

## Health Scoring

### Health Score Architecture

Le health score est l'indicateur central du CS. Il predit la sante de la relation client et declenche les interventions proactives.

**Principes de construction** :

1. **Composite et pondere** : combiner 5-8 signaux avec des poids refletant leur pouvoir predictif du churn.
2. **Data-driven, pas subjectif** : minimiser les inputs manuels. Privilegier les donnees comportementales objectives (usage, engagement) aux evaluations subjectives des CSM.
3. **Granulaire et actionnable** : afficher non seulement le score global mais aussi les sous-scores par dimension pour identifier les actions specifiques.
4. **Calibre regulierement** : valider le modele tous les trimestres en correlant le health score avec le churn reel. Ajuster les poids si necessaire.

### Health Score Model Detaille

**Dimension 1 — Product Usage (poids : 30%)**

| Signal | Mesure | Score 0-100 | Source |
|---|---|---|---|
| Frequence d'utilisation | DAU/MAU ratio | < 10% = 0, > 50% = 100 | Product analytics |
| Profondeur d'utilisation | Nombre de features actives / features disponibles | < 20% = 0, > 60% = 100 | Product analytics |
| Tendance | Variation d'usage sur 30j | Baisse > 30% = 0, stable/croissance = 100 | Product analytics |
| Users actifs vs licences | % de licences reellement utilisees | < 30% = 0, > 70% = 100 | License management |

**Dimension 2 — Engagement (poids : 20%)**

| Signal | Mesure | Score 0-100 | Source |
|---|---|---|---|
| Logins executifs | Frequence de login des sponsors/decision-makers | 0 login/mois = 0, > 4 = 100 | Product analytics |
| Participation events | Webinars, trainings, user groups | 0 = 20, > 2/trim = 100 | Event tracking |
| Reponse aux communications | Ouverture emails CS, reponse aux enquetes | < 10% = 0, > 50% = 100 | Email analytics |
| Presence du champion | Champion actif et engage | Depart champion = 0, actif = 100 | CRM / CSM input |

**Dimension 3 — Support Health (poids : 15%)**

| Signal | Mesure | Score 0-100 | Source |
|---|---|---|---|
| Volume de tickets | Tendance sur 90j | Hausse > 50% = 20, stable/baisse = 100 | Ticketing |
| Severite des tickets | % de tickets P1/P2 | > 30% = 0, < 5% = 100 | Ticketing |
| Sentiment tickets | Analyse NLP du ton des messages | Negatif > 50% = 0, positif > 70% = 100 | NLP analysis |
| Tickets ouverts ages | Nombre de tickets ouverts > 7j | > 5 = 0, 0 = 100 | Ticketing |

**Dimension 4 — Satisfaction (poids : 15%)**

| Signal | Mesure | Score 0-100 | Source |
|---|---|---|---|
| NPS | Score NPS le plus recent | Detracteur = 0, passif = 50, promoteur = 100 | Enquetes |
| CSAT | Moyenne CSAT sur 90j | < 3/5 = 0, > 4.5/5 = 100 | Enquetes |
| Feedback qualitatif | Analyse des commentaires | Negatif dominant = 20, positif = 100 | NLP analysis |

**Dimension 5 — Financial Health (poids : 15%)**

| Signal | Mesure | Score 0-100 | Source |
|---|---|---|---|
| Paiements | Retard de paiement | > 60j = 0, a jour = 100 | Billing |
| Contrat | Proximite du renouvellement | < 30j sans engagement = 20, > 180j = 100 | CRM |
| Mouvement de plan | Evolution recente | Downgrade = 0, stable = 60, upgrade = 100 | Billing |
| Discussions commerciales | Negociations en cours | Demande de reduction = 20, expansion = 100 | CRM / CSM |

**Dimension 6 — Relationship (poids : 5%)**

| Signal | Mesure | Score 0-100 | Source |
|---|---|---|---|
| Multi-threading | Nombre de contacts dans le compte | 1 = 20, > 5 = 100 | CRM |
| Seniorite des contacts | Niveau du sponsor | Manager = 40, VP = 70, C-level = 100 | CRM |
| Qualite de la relation | Evaluation CSM | Difficile = 20, bonne = 70, excellente = 100 | CSM input |

### Health Score Segmentation & Actions

| Score | Categorie | Couleur | Action |
|---|---|---|---|
| 80-100 | Healthy | Vert | Expansion play : identifier les opportunites d'upsell et de referral |
| 60-79 | Stable | Jaune-vert | Monitoring : maintenir l'engagement, approfondir l'adoption |
| 40-59 | At Risk | Orange | Intervention : appel CS, plan d'action, resolution des irritants |
| 0-39 | Critical | Rouge | Rescue plan : escalade au management, intervention executive, plan de retention urgent |

---

## Proactive Engagement Playbooks

### Playbook 1 — Onboarding (J0 a J30)

**Objectif** : atteindre le Time-to-First-Value en < 14 jours.

| Etape | Timing | Action | Owner | Success Criteria |
|---|---|---|---|---|
| Welcome | J0 | Email de bienvenue personnalise + acces ressources | Automatique | Email ouvert |
| Kickoff Call | J1-3 | Appel de lancement : objectifs client, plan de succes | CSM | Objectifs documentes |
| Technical Setup | J3-7 | Assistance a la configuration, import de donnees | CSM + Support | Setup complete |
| First Value | J7-14 | Verification du premier cas d'usage reussi | CSM | Feature cle utilisee |
| Adoption Check | J21 | Point de suivi : usage, questions, roadblocks | CSM | Usage > seuil minimum |
| Onboarding Close | J30 | Bilan onboarding, transition vers phase Adoption | CSM | TTFV atteint, CSAT > 4/5 |

**Signaux d'alerte onboarding** :
- Pas de login dans les 3 premiers jours -> Email + appel CSM
- Setup technique non complete a J7 -> Proposition de session d'aide
- Pas de "first value" a J14 -> Escalade au CSM manager
- Feedback negatif au bilan J30 -> Plan de remediation

### Playbook 2 — Adoption Acceleration (J30 a J90)

**Objectif** : augmenter le Feature Adoption Rate a > 60% des fonctionnalites cles.

| Action | Declencheur | Format | Contenu |
|---|---|---|---|
| Feature Discovery | < 3 features utilisees a J30 | In-app guide + email | "Saviez-vous que [feature] peut vous aider a [objectif] ?" |
| Use Case Workshop | J45 | Session video 30 min | Presenter 3 use cases pertinents pour le client |
| Power User Training | J60 | Webinar ou formation | Formation avancee sur les features a fort impact |
| Admin Training | J75 | Documentation + session | Autonomiser l'admin client sur la configuration |
| Adoption Review | J90 | Appel bilan | Mesurer l'adoption, identifier les gaps, planifier |

### Playbook 3 — Churn Risk Intervention

**Objectif** : ramener un compte "At Risk" (score < 60) vers "Stable" (> 60).

**Declenchement** : health score < 60 OU baisse > 20 points sur 30 jours OU 2+ tickets P1 en 30 jours OU NPS detracteur OU champion qui quitte l'entreprise.

| Etape | Timing | Action | Owner |
|---|---|---|---|
| 1. Alerte | J0 | Notification automatique au CSM et manager CS | Systeme |
| 2. Diagnostic | J0-J2 | Analyser les causes : usage, tickets, satisfaction, changements | CSM |
| 3. Outreach | J2-J3 | Contact client (appel prefere) pour comprendre la situation | CSM |
| 4. Action Plan | J3-J5 | Co-construire un plan d'action avec le client (max 5 actions) | CSM + client |
| 5. Execution | J5-J30 | Executer le plan : resolution bugs, training, ajustements | CSM + equipes |
| 6. Executive Sponsor | J7 (si P1) | Impliquer un sponsor exec cote fournisseur pour les cas critiques | VP CS / CRO |
| 7. Follow-up | J15 | Point de suivi intermediaire | CSM |
| 8. Bilan | J30 | Evaluer les resultats, ajuster si necessaire | CSM |
| 9. Stabilisation | J60 | Confirmer que le score est remonte au-dessus de 60 | CSM |

**Taux de recuperation cible** : 60-70% des comptes "At Risk" ramenes a "Stable" dans les 60 jours.

### Playbook 4 — Expansion & Upsell

**Objectif** : generer du Net Revenue Expansion aupres des comptes en bonne sante.

**Declenchement** : health score > 80 ET usage > 70% du plan ET ROI demontre.

| Signal d'expansion | Action | Format |
|---|---|---|
| Usage proche de la limite du plan | Proposer un upgrade proactif | Email + appel CSM |
| Demandes de features du plan superieur | Presenter la valeur des features avancees | Demo personnalisee |
| Nouveaux cas d'usage identifies en QBR | Proposer des modules/produits complementaires | Proposition + business case |
| Champion satisfait et influent | Demander une reference ou un referral | Appel CSM |
| Expansion de l'equipe client | Proposer des licences supplementaires | Email + proposition |

### Playbook 5 — Renewal Management

**Objectif** : Gross Revenue Retention > 90%, Renewal Rate > 85%.

| Timing (avant echeance) | Action | Owner |
|---|---|---|
| -180 jours | Revue interne du compte : health score, usage, risques | CSM |
| -120 jours | QBR pre-renouvellement : bilan de valeur, roadmap | CSM + client |
| -90 jours | Lancement du processus de renouvellement | CSM + Sales/AM |
| -60 jours | Proposition formelle avec conditions | Sales/AM |
| -30 jours | Follow-up, negociation si necessaire | Sales/AM + CSM |
| -14 jours | Escalade si non signe | CS Manager |
| -7 jours | Escalade executive si non signe | VP CS + CRO |
| J0 | Renouvellement ou churn — post-mortem dans les deux cas | CS + Sales |

---

## Quarterly Business Reviews (QBR)

### Structure d'un QBR efficace

Duree : 45-60 min. Ratio : 70% valeur client / 20% roadmap / 10% actions.

**Agenda recommande** :

1. **Recap des objectifs** (5 min) — Rappeler les objectifs business du client definis lors du kickoff ou du QBR precedent. "Votre objectif etait de [X]. Voici ou nous en sommes."

2. **Resultats et ROI** (15 min) — Presenter les metriques d'usage, les resultats obtenus et le ROI calcule. Utiliser des visuels clairs (graphiques, comparaisons avant/apres). Chiffrer la valeur en euros ou en heures economisees quand c'est possible.

3. **Insights et recommandations** (10 min) — Partager des insights actionables bases sur les donnees d'usage. "Nous avons remarque que [observation]. Nous recommandons [action] pour [benefice]." Comparer avec les benchmarks du secteur.

4. **Success stories** (5 min) — Partager un use case d'un client similaire qui a obtenu des resultats remarquables. Effet miroir et aspiration.

5. **Roadmap produit** (10 min) — Presenter les evolutions a venir qui sont pertinentes pour le client. Connecter chaque feature aux objectifs du client.

6. **Plan d'action mutuel** (10 min) — Definir 3-5 actions concretes pour le prochain trimestre, avec owners et deadlines des deux cotes.

7. **Feedback** (5 min) — Demander un feedback ouvert sur la relation, le produit et le support.

### QBR Preparation Checklist

- [ ] Donnees d'usage extraites et analysees (30 derniers jours + tendance)
- [ ] ROI calcule ou estime
- [ ] Historique des tickets et satisfaction revu
- [ ] Health score actuel et evolution
- [ ] Objectifs du QBR precedent revus (atteints ou non)
- [ ] Presentation personnalisee creee (pas de template generique)
- [ ] Participants confirmes cote client (inclure le sponsor executif)
- [ ] Participants internes alignes (CSM + Product si necessaire)

### QBR Anti-Patterns

- **Product Demo deguisee** : le QBR n'est pas une demo produit. Se concentrer sur les resultats client, pas sur les features.
- **Monologue fournisseur** : le QBR est un dialogue. Poser des questions, ecouter. Le client doit parler au moins 40% du temps.
- **Pas de donnees** : presenter des resultats sans donnees concretes reduit la credibilite. Chiffrer tout.
- **Pas de plan d'action** : un QBR sans next steps est un meeting inutile. Toujours conclure par des actions concretes.
- **Trop frequent ou trop rare** : trimestriel est le bon rythme pour les comptes mid-market+. Pour les comptes tech-touch, un "Digital QBR" (email automatise avec donnees) peut suffire.

---

## Customer Success Tools

### Gainsight

**Forces** : plateforme CS la plus complete du marche, health scoring avance avec Gainsight PX (product analytics integre), CTAs automatisees, Journey Orchestrator pour les playbooks automatises, Staircase AI pour l'intelligence relationnelle.
**Faiblesses** : complexe a configurer et a maintenir, cout eleve (15-25K EUR/an minimum), necessite un admin dedie.
**Ideal pour** : equipes CS matures (5+ CSMs), ARR > 10M EUR, besoin d'automatisation avancee.

**Configuration API (exemple webhook health score alert)** :

```json
{
  "webhook_config": {
    "name": "health_score_alert",
    "url": "https://votre-app.example.com/webhooks/cs-alert",
    "method": "POST",
    "auth": {
      "type": "api_key",
      "key": "FAKE_GAINSIGHT_KEY_000000000000"
    },
    "trigger": {
      "type": "health_score_change",
      "condition": "score_drops_below",
      "threshold": 60,
      "time_window_days": 7
    }
  }
}
```

### ChurnZero

**Forces** : excellent rapport fonctionnalites/complexite, real-time health scoring, in-app communications, plays automatisees, bon pour les equipes B2B SaaS mid-market.
**Faiblesses** : moins profond que Gainsight pour les analytics avancees, moins d'integrations natives.
**Ideal pour** : equipes CS en croissance (3-15 CSMs), ARR 2-20M EUR, besoin de mise en oeuvre rapide.

### Totango

**Forces** : modele modulaire (SuccessBLOCs = templates preconfigurees par use case), bon product analytics integre, interface intuitive, tarification flexible.
**Faiblesses** : moins puissant que Gainsight pour les scenarios complexes, reporting intermediaire.
**Ideal pour** : equipes CS qui demarrent ou cherchent un deploiement rapide, ARR 1-15M EUR.

### Vitally

**Forces** : design moderne, excellente experience utilisateur, integration native Slack/Teams, health scoring intuitif, bon pour les equipes product-led growth (PLG).
**Faiblesses** : fonctionnalites avancees limitees vs Gainsight, moins adapte aux grandes equipes.
**Ideal pour** : startups PLG et equipes CS small/mid (2-10 CSMs), ARR < 10M EUR.

### Planhat

**Forces** : tres fort en Europe, excellent product analytics, revenue analytics integre, interface clean, bon multi-product support.
**Faiblesses** : ecosysteme d'integrations en construction, moins connu que les leaders US.
**Ideal pour** : equipes CS europeennes, ARR 2-30M EUR, besoin de revenue analytics.

### Comparaison synthetique

| Critere | Gainsight | ChurnZero | Totango | Vitally | Planhat |
|---|---|---|---|---|---|
| Prix entree (annuel) | 15K+ EUR | 8K+ EUR | 5K+ EUR | 4K+ EUR | 6K+ EUR |
| Complexite setup | Elevee | Moyenne | Faible-Moyenne | Faible | Moyenne |
| Health scoring | Tres avance | Avance | Avance | Bon | Avance |
| Product analytics | Oui (PX) | Basique | Oui | Bon | Tres bon |
| Playbooks automation | Excellent | Bon | Bon (SuccessBLOCs) | Basique | Bon |
| Reporting | Tres avance | Bon | Bon | Intermediaire | Bon |
| Integrations | 100+ | 50+ | 60+ | 40+ | 50+ |
| Ideal pour | Enterprise | Mid-market | SMB-Mid | Startups/PLG | Mid-market EU |

---

## CS Segmentation & Operating Models

### Segmentation par valeur client

| Segment | ARR typique | Modele CS | Ratio CSM:Comptes | Budget CS/compte |
|---|---|---|---|---|
| **Strategic / Enterprise** | > 100K EUR | High-Touch | 1:5-15 | > 5K EUR/an |
| **Mid-Market** | 20-100K EUR | Mid-Touch | 1:25-50 | 1-3K EUR/an |
| **SMB / Growth** | 5-20K EUR | Low-Touch | 1:100-200 | 200-500 EUR/an |
| **Self-Serve / PLG** | < 5K EUR | Tech-Touch | 1:500-2000 | < 100 EUR/an |

### High-Touch Model
- CSM dedie avec connaissance approfondie du compte.
- QBR trimestriels en personne ou video.
- Plan de succes personnalise avec objectifs business.
- Acces direct au management CS et au product team.
- Executive Business Reviews (EBR) semestrielles avec C-level.

### Mid-Touch Model
- CSM partage entre 25-50 comptes.
- QBR semestriels (video ou digital).
- Playbooks standardises avec personnalisation par segment.
- Communications proactives email + in-app.
- Webinars de groupe par industrie ou use case.

### Low-Touch / Tech-Touch Model
- Pas de CSM dedie — equipe CS pooled pour les interventions ponctuelles.
- Onboarding automatise (email sequences, in-app guides, videos).
- Health score monitoring automatise avec alertes pour intervention humaine.
- Digital QBR (email automatise avec donnees d'usage et recommandations).
- Communaute et self-service comme canaux principaux.

### Digital CS at Scale

L'approche "Digital CS" consiste a automatiser les interactions CS via la technologie :

1. **Automated Email Journeys** : sequences d'emails personnalises basees sur le lifecycle stage, l'usage et le segment. Outils : Intercom, Customer.io, Iterable.
2. **In-App Messaging** : messages contextuels declenches par le comportement (feature non adoptee, milestone atteint). Outils : Pendo, Intercom, Userpilot.
3. **Digital QBR** : email automatise mensuel/trimestriel avec les metriques d'usage, le health score et des recommandations personnalisees.
4. **Community Programs** : forums, user groups, ambassador programs pour creer de l'engagement sans intervention directe du CSM.
5. **Webinar Programs** : webinars recurrents par theme (onboarding, best practices, advanced features) ouverts a tous les clients.

---

## State of the Art (2024-2026)

### Tendances majeures

**1. AI-Powered Customer Success**
L'IA transforme le CS a plusieurs niveaux. En 2024-2025, les CSM utilisent l'IA comme copilot pour la preparation des calls (resume automatique du compte, talking points suggeres, risques identifies). En 2025-2026, l'IA va plus loin : prediction fine du churn avec 30-60 jours d'avance (precision > 80%), recommandations d'actions personnalisees pour chaque compte, generation automatique de bilans QBR et de plans de succes. Gainsight Staircase AI, ChurnZero AI, et des solutions comme Clari, Gong integrent ces capacites.

**2. Revenue-Centric CS**
Le CS evolue du "customer happiness" vers le "revenue optimization". Les organisations les plus avancees mesurent le CS directement en impact revenue : contribution au NRR, expansion pipeline generee par le CS, churn revenue prevented. Le CSM devient un "Revenue CSM" avec des objectifs de Net Revenue Retention (> 110%) et d'expansion (contribution a 20-30% du pipeline de renouvellement). Les outils CS integrent nativement le revenue tracking.

**3. Digital-First, Human-When-It-Matters**
Le modele hybride digital + humain se generalise. 70-80% des interactions CS sont automatisees (emails, in-app, chatbot CS), et l'intervention humaine est reservee aux moments a fort impact : onboarding comptes strategiques, churn risk intervention, expansion discussions, executive alignment. Ce modele permet d'augmenter le ratio CSM:comptes de 1:50 a 1:200+ sans degrader les resultats.

**4. Product-Led Customer Success**
Le CS s'integre profondement avec le produit. Les signaux produit (usage, adoption, engagement) alimentent les health scores et declenchent les playbooks automatiquement. Les CSM ne sont plus des "relationship managers" mais des "value consultants" armes de donnees produit. Les outils PLG (Pendo, Heap, Amplitude) se connectent nativement aux plateformes CS.

**5. Pooled CS & Specialized Pods**
L'organisation CS evolue du modele "un CSM par compte" vers des pods specialises : un pod onboarding, un pod adoption, un pod retention, un pod expansion. Les comptes circulent entre les pods selon leur lifecycle stage. Ce modele permet aux CSMs de developper une expertise profonde et d'etre plus efficaces. Pour le tech-touch, les equipes "Pooled CS" interviennent de maniere reactive sur les alertes health score sans assignation permanente.

**6. Customer Success Qualified Leads (CSQL)**
Le CS devient une source majeure de leads qualifies pour les equipes Sales. Les CSMs identifient les opportunites d'expansion (nouveau departement, nouveau use case, augmentation de licences) et les transmettent comme CSQLs avec le contexte complet. Les organisations matures generent 20-40% de leur pipeline d'expansion via les CSQLs.

**7. Outcome-Based CS**
Le CS evolue de la gestion de la relation vers la gestion des resultats (outcomes). Le CSM co-definit avec le client des "Success Plans" avec des objectifs mesurables et un ROI cible. Chaque QBR mesure la progression vers ces objectifs. Ce shift positionne le CS comme un partenaire strategique et non comme un service de confort. Les clients qui atteignent leurs outcomes ont un taux de renouvellement de 95%+ vs 70% pour ceux qui ne les atteignent pas.

### Benchmarks CS 2025

| Metrique | Percentile 25 | Mediane | Percentile 75 | Best-in-Class |
|---|---|---|---|---|
| Gross Revenue Retention (GRR) | 82% | 88% | 93% | 97%+ |
| Net Revenue Retention (NRR) | 95% | 105% | 115% | 130%+ |
| Logo Churn Rate (annuel) | 18% | 12% | 7% | < 3% |
| Time-to-First-Value | 30j+ | 21j | 14j | < 7j |
| QBR Completion Rate | 40% | 60% | 80% | 95%+ |
| CSM:Account ratio (mid-market) | 1:80 | 1:50 | 1:30 | 1:15 |
| Health Score Accuracy (vs actual churn) | 55% | 65% | 75% | 85%+ |
| CSQL contribution to pipeline | 5% | 15% | 30% | 45%+ |
| Onboarding completion rate | 60% | 75% | 85% | 95%+ |
| CS ROI (revenue retained / CS cost) | 3x | 5x | 8x | 15x+ |
