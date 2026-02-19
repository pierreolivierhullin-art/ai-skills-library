# Open Innovation & Ecosystemes d'Innovation

## Vue d'Ensemble

L'open innovation (Henry Chesbrough, 2003) repose sur le principe que les meilleures idees ne se trouvent pas uniquement a l'interieur de l'entreprise. Les flux d'innovation sont bidirectionnels : **inbound** (faire entrer des idees et technologies exterieures) et **outbound** (monetiser les technologies internes inutilisees). Pour les grandes organisations, l'open innovation est souvent le seul moyen d'acceder a la vitesse d'innovation des ecosystemes startups.

---

## Modeles d'Open Innovation

### 1. Partenariats Startups

**Venture Clienting** (modele prioritaire en 2024-2026) :
Le venture clienting consiste a acheter la solution d'une startup comme premier client strategique, plutot que d'investir dans son capital. Avantages : acces rapide a la technologie, pas de dilution, deal contractuel clair, la startup beneficie d'une reference majeure.

Processus :
```
1. Challenge interne (2 sem) : definir le probleme business a resoudre
2. Scouting startups (2-4 sem) : identifier 10-20 candidats via bases de
   donnees (Dealroom, Crunchbase, PitchBook) ou accelerateurs
3. Evaluation (2 sem) : Demo + fit technique + fit organisationnel
4. Pilot (1-3 mois) : PoC paye sur un perimetre limite
5. Deploiement : si pilot concluant, contrat cadre + rollout
```

Differences avec le Corporate Venture Capital :
| Dimension | Venture Clienting | Corporate VC |
|---|---|---|
| Relation | Client-Fournisseur | Investisseur-Startup |
| Acces technologie | Immédiat (contrat) | Indirect (board) |
| Risque financier | Faible (pilot = budget ops) | Eleve (capital) |
| Dependance | Non (multi-fournisseur) | Possible si participation forte |
| Timeframe | 3-6 mois | 5-10 ans |

**Accelerateurs Corporates** :
Un accelerateur corporate selectionne des startups early-stage, leur fournit pendant 3-6 mois : acces aux experts internes, POC paye, reseau clients. En echange : visibilite sur la technologie, option d'investissement, parfois equity symbolique.

Exemples : SNCF Digital Ventures, BNP Paribas Open Innovation, Total Energies Ventures, Orange Fab, L'Oreal BOLD.

**Hackathons** :
- **Interne** : mobiliser les collaborateurs sur un defi innovant en 24-48h. Objectif : culture d'innovation, identification des intrapreneurs, ideation rapide.
- **Externe/Mix** : inviter des startups, etudiants, freelances. Objectif : diversite des perspectives, recrutement, relations ecosysteme.
- **Erreur frequente** : hackathon sans suite. Si les prototypes ne sont pas suivis d'un programme de preaccceleration, l'energie generee se dissipe et les participants sont demotives.

### 2. Partenariats Recherche et Universites

**Co-recherche** : financer une chaire universitaire en echange d'un acces prioritaire aux resultats. Cout : 100-500k EUR/an. Horizon : 3-5 ans. Adapte aux technologies de rupture (horizon 3).

**CIFRE** (Conventions Industrielles de Formation par la Recherche) : cofinancement d'un doctorant avec l'ANRT. Le doctorant travaille 50% chez l'entreprise, 50% en labo. Cout entreprise : ~14-17k EUR/an (subvention ANRT de 14k EUR). Excellent rapport qualite/prix pour la recherche appliquee.

**Transfert technologique** : acheter une licence sur un brevet d'universite ou de labo public. Sources : SATT (Societes d'Acceleration du Transfert de Technologies), CNRS, INRIA, CEA.

### 3. Open Source et API Economy

**Contribuer a l'open source** : Google, Meta, Microsoft et LinkedIn ont tous construit des avantages strategiques en open-sourcant des technologies (TensorFlow, React, Kubernetes, Kafka). Les benefices : recrutement, reputation, adoption de standards, contributions externes gratuites.

**API Economy** : ouvrir ses donnees ou services via une API permet a des tiers de construire des services complementaires. Ex : API SNCF → 200+ applications tierces, API Banque de France → fintechs, API Impots → solutions comptables.

**Developer Relations** : equipe dediee a animer la communaute de developpeurs autour des APIs et SDKs. DevRel = mix de product management, marketing et engineering.

### 4. Crowdsourcing et Open Challenges

**Platforms de challenges** : InnoCentive (racheté par Wazoku), Kaggle (ML/data), HeroX. Principe : publier un probleme technique avec une recompense (10k-1M USD). La foule propose des solutions. L'entreprise choisit la meilleure.

**Cas d'usage adapte** : problemes bien definis avec un critere de succes clair (un algorithme qui bat tel benchmark, une formule chimique avec telles proprietes). Moins adapte aux problemes vagues ou impliquant des donnees confidentielles.

---

## Scouting et Evaluation des Startups

### Sources de scouting

| Source | Type | Acces |
|---|---|---|
| Dealroom | Base de donnees startups europeennes | Payant (abonnement) |
| Crunchbase | Base mondiale | Freemium |
| PitchBook | Professionnel, donnees financieres | Payant (tres cher) |
| Product Hunt | Nouvelles applications, SaaS | Gratuit |
| Accelerateurs (YC, Station F, etc.) | Batches de startups selectionnes | Gratuit (portfolio public) |
| LinkedIn | Identification directe | Gratuit |
| Veille brevets (Google Patents, Espacenet) | Technologies emergentes | Gratuit |

### Scorecard d'evaluation startup (exemple)

**1. Probleme et Marche (20 pts)**
- Probleme reel et significatif (10 pts)
- Taille de marche addressable (10 pts)

**2. Solution et Differentiation (25 pts)**
- Maturite technologique (TRL 1-9) (10 pts)
- Moat defensable (brevet, effet reseau, donnees) (10 pts)
- Demo fonctionnelle (5 pts)

**3. Traction (20 pts)**
- Premiers clients / références (10 pts)
- Metriques de croissance (ARR, retention) (10 pts)

**4. Fit Strategique (20 pts)**
- Alignement avec nos defis (10 pts)
- Complementarite (pas de concurrence directe) (10 pts)

**5. Equipe (15 pts)**
- Experience du domaine (10 pts)
- Capacite d'execution (5 pts)

**Decision** : > 70 pts → Pilot | 50-70 pts → Suivi | < 50 pts → Rejet

### Due Diligence pour un Pilot

- **Technique** : revue de code ou architecture, test de charge, securite (questionnaire OWASP)
- **Juridique** : propriete intellectuelle (qui possede le code du pilot ?), RGPD (ou sont les donnees ?), condition de sortie si la startup fait faillite
- **Financiere** : runway (combien de mois avant de manquer de cash), cap table (investisseurs presents), levees passes
- **Contractuelle** : NDA, accord de co-developpement si applicable, conditions de sortie

---

## Programme d'Open Innovation — Gouvernance

### Structure organisationnelle

```
Chief Innovation Officer
        |
Open Innovation Manager (1-2 pers.)
        |
   ┌────┴────────────────────────────┐
Scout &    Programme      Legal &    Finance
Scouting   Manager       IP Counsel  (budget)
(relationships
 ecosysteme)
```

**Le "Innovation Scout"** : role cle — expertise ecosysteme, reseau personnel, capacite a identifier rapidement les startups pertinentes. Souvent ex-VC ou ex-fondateur.

### Budget type pour un programme d'open innovation (ETI)

| Poste | Budget annuel | Commentaire |
|---|---|---|
| Equipe (2 ETP) | 250-350k EUR | OI Manager + Scout |
| Pilots startups (3-5/an) | 150-250k EUR | 30-50k EUR par pilot |
| Hackathon annuel | 30-80k EUR | Avec suite programmatique |
| Abonnements scouting | 20-40k EUR | Dealroom, evenements |
| **Total** | **450-720k EUR** | Hors CVC si applicable |

### KPIs d'un programme d'open innovation

**Metriques de pipeline** :
- Nombre de startups evaluees / an
- Taux de conversion : evaluation → pilot → deploiement
- Temps moyen de la premiere rencontre au premier contrat

**Metriques d'impact** :
- Nombre de solutions deployees en production
- Revenus generes ou couts evites attribuables
- Technologies acquises ou licenciees

**Metriques d'ecosysteme** :
- Visibilite dans l'ecosysteme startup (mentionnes dans X deals)
- Qualite du reseau (acces aux deal flow des meilleurs VCs)

---

## Propriete Intellectuelle en Open Innovation

### Enjeux critiques

**Qui possede quoi dans un co-developpement ?**

```
Scenario 1 — Startup developpe sur commande :
→ Travail fait for hire → appartient a l'entreprise
   Risque : demotivation de la startup si 100% transfert

Scenario 2 — Co-developpement :
→ Definir a l'avance : background IP (chacun garde le sien)
   vs foreground IP (le nouveau cree ensemble)
   La "foreground IP" peut etre : co-detenue (50/50),
   detenue par l'un avec licence a l'autre, ou separee par domaine

Scenario 3 — Venture Clienting standard :
→ L'entreprise achete une licence d'utilisation, pas le code
   La startup garde sa propriete intellectuelle
   Verifier : licence exclusive ou non-exclusive ?
```

**Checklist contractuelle OI** :
- [ ] Propriete des developpements issus du pilot
- [ ] Licence d'utilisation en cas d'arret de la startup (source code escrow)
- [ ] Confidentialite et NDA bilateral
- [ ] Clause de non-sollicitation mutuelle (equipes)
- [ ] Droit de premier regard en cas de cession de la startup
- [ ] Conditions de sortie et duree minimum du contrat

---

## Ecosysteme Startup Francais — Ressources

| Structure | Role | Contact |
|---|---|---|
| Station F | Plus grand campus startup mondial (Paris) | stationf.co |
| Bpifrance Le Hub | Mise en relation startups-grands groupes | bpifrance-lhub.fr |
| French Tech | Communaute nationale des startups | lafrenchtech.com |
| Numa | Accelerateur B2B, formations OI | numa.co |
| Euratechnologies (Lille) | Ecosysteme tech regional | euratechnologies.com |
| LVMH Maison des Startups | Retail/Luxe/Art | — |
| Agoranov | Deeptech (Paris) | agoranov.com |

**Agenda cle** : Viva Tech (Paris, mai/juin) — plus grande conference Tech/Startup d'Europe. Presente dans tous les grands stands des ETI et grandes entreprises francaises.
