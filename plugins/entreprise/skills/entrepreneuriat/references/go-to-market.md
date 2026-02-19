# Go-to-Market -- Strategie de Lancement et Acquisition

Reference operationnelle sur la strategie go-to-market pour startups et nouveaux produits. Couvre les trois motions GTM (PLG, SLG, CLG), la definition de l'ICP, le messaging framework, les canaux d'acquisition B2B, le pricing comme levier GTM et un playbook de lancement en 90 jours. Utiliser ce document pour structurer chaque decision de mise sur le marche, de la validation du segment cible jusqu'a l'optimisation de la machine d'acquisition.

---

## Definition du GTM -- Sequence de Decisions

Le Go-to-Market est la sequence de decisions qui definit comment une entreprise atteint ses clients cibles, delivre sa proposition de valeur et genere des revenus. Ce n'est pas un plan marketing -- c'est une architecture de croissance.

**La sequence GTM dans l'ordre correct :**

```
1. Segment cible (ICP)
      |
      v
2. Proposition de valeur (message)
      |
      v
3. Canal d'acquisition (comment on les atteint)
      |
      v
4. Motion de vente (comment on les convaincu)
      |
      v
5. Modele de revenus (comment on monetise)
      |
      v
6. Metriques de succes (comment on mesure)
```

**Erreur frequente** : commencer par le canal (ex : "on va faire du LinkedIn") avant d'avoir defini l'ICP et le message. Le canal est toujours une consequence du segment, pas une decision independante.

---

## Les 3 Motions GTM

### Motion 1 -- Product-Led Growth (PLG)

**Definition** : le produit lui-meme est le principal vecteur d'acquisition, d'activation, de retention et d'expansion. L'utilisateur decouvre, adopte et recommande le produit sans interaction commerciale obligatoire. Le produit remplace (ou assiste) le marketing et les ventes traditionnelles.

**Conditions prealables pour un PLG viable :**
- Le produit delivre de la valeur avant l'achat (free tier ou free trial)
- Le time-to-value est court : l'utilisateur percoit la valeur en minutes ou heures, pas en jours
- Le produit a une composante virale ou collaborative (l'usage implique naturellement d'autres personnes)
- L'ACV est compatible avec le self-serve (< 15 000 EUR/an pour le tier PLG core)
- La complexite d'integration est faible (pas besoin d'un consultant pour deployer)

**Metriques cles du PLG :**

| Metrique | Definition | Benchmark cible |
|---|---|---|
| **Activation rate** | % nouveaux utilisateurs qui atteignent le "aha moment" dans les 7 jours | > 40% |
| **Time-to-value (TTV)** | Temps entre l'inscription et la premiere experience de valeur | < 5 minutes |
| **PQL rate** | % d'utilisateurs qui deviennent des Product-Qualified Leads | 5-15% des signups |
| **Self-serve conversion** | % de trials/freemium qui se convertissent en payants sans contact commercial | > 3-8% |
| **Viral coefficient (k)** | Nouveaux utilisateurs generes par chaque utilisateur existant | > 0.3 (k > 1 = croissance exponentielle) |
| **DAU/MAU ratio** | Frequence d'utilisation (mesure l'engagement) | > 20% pour B2B SaaS |

**Exemples de produits PLG :**
- **Slack** : un utilisateur invite ses collegues, le produit ne fonctionne qu'en equipe. La valeur croit avec le nombre d'utilisateurs.
- **Notion** : templates publics, partage de pages, databases partagees. L'utilisateur individuel amene l'equipe.
- **Figma** : collaboration en temps reel au coeur du produit. Un designer partage avec un developpeur qui s'inscrit.
- **Calendly** : chaque lien de reservation est une publicite pour le produit.

**Quand le PLG marche :**
- Produit B2B horizontal (outil de productivite, communication, collaboration)
- Segment PME ou individus (decisions d'achat rapides)
- Probleme universel avec un "aha moment" clair et rapide
- Effets de reseau naturels dans le produit

**Quand le PLG ne marche pas :**
- Produit d'infrastructure (le benefice n'est pas visible par l'utilisateur final)
- Produit necessitant une integration complexe ou une formation longue
- Segment enterprise ou la decision est collectee et politique
- Produit tres niche ou specifique (pas assez d'utilisateurs pour des effets viraux)

### Motion 2 -- Sales-Led Growth (SLG)

**Definition** : une equipe de vente proactive drive l'acquisition et la conversion. Les commerciaux identifient les prospects (outbound) ou traitent les leads entrants (inbound) et les convertissent via un processus de vente structure.

**Structure de l'equipe SLG :**

| Role | Responsabilite | Ratio recommande |
|---|---|---|
| **SDR (Sales Development Rep)** | Prospection outbound, qualification initiale, prise de RDV | 1 SDR pour 2-3 AE |
| **AE (Account Executive)** | Gestion du cycle de vente de la decouverte au closing | Cible : 600K-1M EUR ARR/AE |
| **CSM (Customer Success)** | Retention, expansion, renouvellement | 1 CSM pour 1-2M EUR ARR |
| **Sales Manager** | Coaching, pipeline review, recrutement | 1 manager pour 6-8 ICs |

**Framework de qualification MEDDIC :**

- **M** -- Metrics : quels resultats mesurables le prospect cherche-t-il ? (ex : reduire le temps de traitement de 50%)
- **E** -- Economic Buyer : qui a le budget et le pouvoir de decision finale ?
- **D** -- Decision Criteria : quels sont les criteres formels et informels de selection ?
- **D** -- Decision Process : quelles sont les etapes et les acteurs du processus de decision ?
- **I** -- Identify Pain : quel est le probleme douloureux que le prospect cherche a resoudre ?
- **C** -- Champion : qui a un interet personnel dans la reussite du projet et peut influencer en interne ?

Un deal sans Champion identifie et sans acces a l'Economic Buyer a moins de 20% de chance de closing. Disqualifier rapidement les deals ou ces elements sont absents.

**Exemples de produits SLG :**
- **Salesforce** : cycle de vente 3-12 mois, ACV > 50 000 EUR, equipe de vente importante
- **Workday** : deal enterprise, decision collective, implementation longue
- **HubSpot** : motion hybride (PLG pour le bas du marche, SLG pour le mid et enterprise)

**Quand le SLG s'impose :**
- ACV > 20 000 EUR (le ticket justifie un commercial dedie)
- Cycle de vente > 1 mois (processus de decision complexe)
- Decisions d'achat collectives (comites, directions multiples)
- Necessite d'education du marche ou de personnalisation forte
- Secteurs reglements (sante, finance, defense) ou la confiance est critique

### Motion 3 -- Community-Led Growth (CLG)

**Definition** : la communaute des utilisateurs est le principal moteur de decouverte, d'adoption et de retention. Les membres de la communaute recrute d'autres membres, creent du contenu, s'entraident et deviennent des ambassadeurs du produit.

**Caracteristiques du CLG :**
- Fonctionnel dans les ecosystemes techniques (developpeurs, designers, data scientists)
- Necessite un investissement long terme avant de voir des resultats (6-18 mois)
- Creer des effets de reseau forts et des couts de changement eleves
- Exemples : HashiCorp (Terraform community), Figma (community de designers), dbt (analytics engineers)

**Metriques CLG :**
- Membres actifs mensuels de la communaute
- Contenu genere par la communaute (posts, templates, plugins)
- Signups attribues a la communaute (UTM tracking + self-reported)
- Community-influenced pipeline (deals ou la communaute a joue un role)

---

## Segmentation ICP -- Ideal Customer Profile

### Pourquoi l'ICP est la decision la plus importante du GTM

L'ICP mal defini est la cause numero 1 des echecs GTM. En vendant a tout le monde, on ne vend a personne : le message est vague, le canal est inefficace, le produit ne repond pas parfaitement a un besoin specifique. L'ICP precis permet d'aller chercher les clients ou le probleme est le plus aigu, ou la willingness-to-pay est la plus forte, et ou le cycle de vente est le plus court.

**Regle d'or** : commencer avec l'ICP le plus etroit possible, prouver le modele sur ce segment, puis l'elargir. Il est toujours plus facile d'elargir un ICP reussi que de le restreindre apres echec.

### Composantes de l'ICP B2B

**Firmographics (donnees objectives de l'entreprise) :**
- Taille d'entreprise : nombre d'employes, chiffre d'affaires
- Secteur d'activite : industrie, sous-secteur
- Geographie : pays, region, culture
- Maturite technologique : stack actuelle, adoption SaaS, budget tech
- Stade de croissance : startup, scale-up, PME etablie, grand groupe

**Technographics (signaux liees a la technologie utilisee) :**
- Outils concurrents ou complementaires utilises (ex : "utilise HubSpot" = signal de maturite marketing)
- Presence ou absence de certains systemes (ex : "pas de solution RH centralisee")
- Maturite data : utilise-t-on un data warehouse ? Un BI tool ?

**Behavioral signals (signaux comportementaux observables) :**
- Recrutement actif (LinkedIn Jobs) dans un domaine specifique = signal de besoin
- Levee de fonds recente = budget disponible et croissance acceleree
- Changement de direction (nouveau VP Sales, nouveau CTO) = fenetre de changement
- Adoption recente d'un outil complementaire = signal de maturite

**Psychographics (profil du decision-maker) :**
- Persona : role, seniority, responsabilites
- Motivations : quels KPIs le decision-maker cherche-t-il a ameliorer ?
- Pain points : quelles frustrations revient regulierement dans les entretiens ?
- Vocabulaire : quels termes utilise-t-il pour decrire le probleme ?

### Template ICP -- Remplir pour chaque segment cible

```
## ICP -- [Nom du segment]

### Firmographics
- Taille : [ex. 50-200 employes]
- Secteur : [ex. SaaS B2B, logistique, industrie manufacturiere]
- Geographie : [ex. France, Europe de l'Ouest, DACH]
- Revenue : [ex. 5-50M EUR ARR]
- Maturite tech : [ex. stack SaaS, budget IT > 100K EUR/an]

### Technographics
- Utilise : [ex. Salesforce, HubSpot, Slack]
- N'utilise pas encore : [ex. solution de notre categorie]
- Signal de readiness : [ex. a recemment adopte un CRM = prochaine etape]

### Persona Decision-Maker
- Role : [ex. VP Sales, Head of Revenue Operations]
- Seniority : [ex. C-level ou N-1]
- KPIs prioritaires : [ex. pipeline, forecast accuracy, win rate]
- Vocabulaire du probleme : [ex. "nos preventes sont infiables", "nos reps perdent du temps"]

### Behavioral Triggers
- Signal 1 : [ex. recrutement de 3+ SDR en 6 mois]
- Signal 2 : [ex. levee de fonds Serie A ou Serie B]
- Signal 3 : [ex. nouveau VP Sales depuis < 6 mois]

### Disqualifiant
- [ex. < 10 employes : budget insuffisant]
- [ex. secteur public : cycle trop long]
- [ex. deja sous contrat avec concurrent X pendant > 12 mois]
```

---

## Messaging Framework

### Problem-Agitate-Solution (PAS)

Structure en 3 temps pour les messages a haute conversion :

1. **Problem** : identifier et nommer le probleme du segment avec le vocabulaire exact qu'il utilise
2. **Agitate** : amplifier la douleur causee par ce probleme (consequences si non resolu, cout de l'inaction)
3. **Solution** : presenter la solution et comment elle elimine le probleme

**Exemple** :
- Problem : "Vos managers passent 3 heures a preparer chaque entretien de performance."
- Agitate : "Le resultat : des entretiens bacles, des objectifs mal alignes et des collaborateurs qui ne comprennent pas comment progresser. Le turnover cote."
- Solution : "PerfTrack reduit le temps de preparation a 20 minutes et garantit des entretiens structures, documentes et lies aux objectifs de l'equipe."

### Before/After/Bridge (BAB)

Structure alternative, particulierement efficace en SaaS B2B :

- **Before** : decrire la situation actuelle douloureuse (avant le produit)
- **After** : decrire l'etat desire (apres le produit, les resultats obtenus)
- **Bridge** : le produit est le pont entre les deux etats

### Template Elevator Pitch

```
Pour [audience cible]
qui [probleme ou besoin]
[Nom du produit] est un [categorie de produit]
qui [benefice principal / proposition de valeur unique].
Contrairement a [principale alternative],
notre produit [differentiation cle].
```

**Exemple** :
```
Pour les VP Sales de scale-ups
qui perdent en moyenne 40% de leurs leads par manque de qualification rigoureuse,
SalesPilot est une plateforme de Revenue Intelligence
qui predit la probabilite de closing de chaque deal en temps reel et recommande les actions suivantes.
Contrairement a Salesforce ou les donnees sont entrees manuellement et peu fiables,
SalesPilot se connecte aux emails, appels et reunions pour capturer automatiquement les signaux MEDDIC.
```

---

## Canaux d'Acquisition B2B -- Comparaison

| Canal | Cout | Delai | Scalabilite | Qualification | Quand l'utiliser |
|---|---|---|---|---|---|
| **Cold Outbound (email/LinkedIn)** | Faible (temps SDR) | Court (< 1 mois) | Moyen | Faible (non-intentionnel) | Pre-PMF pour valider l'ICP, deals enterprise |
| **Inbound Content (SEO/blog)** | Moyen (creation contenu) | Long (6-18 mois) | Eleve | Eleve (intentionnel) | Post-PMF, categories ou les clients cherchent activement |
| **Paid (Google Ads, LinkedIn Ads)** | Eleve (CPC) | Court (jours) | Eleve | Moyen | Tester le messaging, scaler apres PMF |
| **Partnerships (integrateurs, revendeurs)** | Faible (setup) | Moyen (3-6 mois) | Eleve | Moyen | Post-PMF, acces a des marches adjacents |
| **Product Virality (referral, partage)** | Tres faible | Variable | Tres eleve | Eleve | PLG, produits collaboratifs |
| **Events (salons, webinars)** | Moyen a eleve | Court (event) | Faible | Variable | Lancement, brand awareness, qualification enterprise |
| **Community (Slack, Discord, forums)** | Faible (temps) | Long (12+ mois) | Moyen | Eleve | Produits techniques, ecosysteme developpeurs |

**Regle du canal early-stage** : tester 2-3 canaux simultanement, identifier celui qui produit les leads les mieux qualifies au cout d'acquisition le plus bas, puis allouer 80% des ressources a ce canal avant de diversifier.

---

## Pricing & Packaging comme Levier GTM

### Le Pricing n'est pas une ligne comptable -- c'est un signal strategique

Le prix communique le positionnement, filtre l'ICP et structure l'adoption. Une mauvaise strategie de pricing peut detruire un GTM parfait.

**Freemium** : adapte quand le COGS du tier gratuit est negligeable, quand l'adoption individuelle precede l'adoption equipe, et quand la conversion gratuit --> payant est mesurable. Risque : le gratuit cannibalise le payant si les limites sont mal calibrees.

**Free Trial (time-limited)** : 14 ou 30 jours avec acces complet. Force la decision d'achat, qualifie mieux que le freemium. Adapte quand le time-to-value est court et quand le produit est complexe a evaluer sans le contexte complet.

**Land and Expand** : entrer avec un prix bas sur un departement ou un cas d'usage limite, puis etendre a l'entreprise. Adapte pour le B2B enterprise ou la decision globale est difficile a obtenir. Metriques : NRR > 120%, expansion revenue > 30% du nouveau MRR.

**Packaging recommande par segment :**

| Tier | Cible | Prix | Objectif GTM |
|---|---|---|---|
| **Free/Starter** | Individus, PME < 10 employes | 0-20 EUR/mois | Acquisition, viralite |
| **Growth/Pro** | Equipes 10-50 employes | 50-200 EUR/mois | Monetisation core, self-serve |
| **Business/Scale** | Entreprises 50-200 employes | 200-1 000 EUR/mois | Expansion, AE-assisted |
| **Enterprise** | Grands comptes 200+ employes | Custom (> 1 000 EUR/mois) | SLG, contrats annuels |

---

## GTM Scorecard -- Metriques par Phase

### Phase 1 : Pre-PMF (Recherche du PMF)

Priorite : apprendre, pas scaler. Les metriques sont principalement qualitatives.

| Metrique | Definition | Cible pre-PMF |
|---|---|---|
| Entretiens clients | Nombre d'entretiens problem-discovery + solution-validation | 50+ entretiens |
| Taux de confirmation probleme | % d'interviewes qui confirment le probleme sans guidage | > 70% |
| Lettres d'intention | Clients prets a payer avant que le produit existe | 5-10 LOIs |
| Activation (MVP) | % des premiers utilisateurs qui realisent l'action cle | > 50% |
| Retention D30 | % des premiers utilisateurs encore actifs apres 30 jours | > 30% |

### Phase 2 : Post-PMF (Optimisation du GTM)

Priorite : optimiser le moteur d'acquisition et prouver la repetabilite.

| Metrique | Definition | Cible post-PMF |
|---|---|---|
| CAC | Cout d'acquisition d'un client payant | Defini par LTV/CAC > 3:1 |
| Payback period | Mois pour recuperer le CAC | < 12 mois (< 6 = excellent) |
| MRR Growth | Croissance mensuelle du MRR | > 10% MoM |
| NRR | Net Revenue Retention | > 100% (> 110% = excellent) |
| Churn mensuel | % MRR perdu par mois | < 2% mensuel |
| CAC payback canal | Payback period par canal d'acquisition | Identifier le canal le plus efficace |

---

## Calcul du Marche -- TAM, SAM, SOM

### Methode Bottom-Up (recommandee pour les investisseurs)

Ne jamais utiliser la methode top-down ("marche mondial des logiciels RH = 50Md EUR, on en prend 1%"). Cette approche est perçue comme paresseuse. Utiliser la methode bottom-up.

**TAM (Total Addressable Market)** : l'ensemble du marche potentiel si on avait 100% des clients possibles.

```
TAM = Nombre de clients potentiels x ACV moyen

Exemple SaaS RH :
- Entreprises de 50-500 employes en France = 45 000 entreprises
- ACV moyen = 3 600 EUR/an
- TAM France = 45 000 x 3 600 EUR = 162M EUR
```

**SAM (Serviceable Addressable Market)** : la part du TAM que le modele actuel peut adresser (contraintes geographiques, de segment, de canal).

```
SAM = TAM x % de marche reellement adressable

Exemple :
- On commence uniquement sur les entreprises tech et SaaS (20% du TAM)
- On couvre uniquement la France (pas les marches francophones)
- SAM = 162M EUR x 20% = 32M EUR
```

**SOM (Serviceable Obtainable Market)** : la part realiste du SAM que l'entreprise peut capturer dans les 3-5 ans.

```
SOM = SAM x % de part de marche realistic

Exemple :
- On vise 5% du SAM dans les 5 ans
- SOM = 32M EUR x 5% = 1.6M EUR ARR
- Validation : 450 clients x 3 600 EUR ACV = 1.62M EUR
```

**Validation bottom-up** : decomposer le SOM en nombre de clients x ACV. Ce nombre doit etre atteignable avec l'equipe et le budget prevu.

---

## Playbook de Lancement en 90 Jours

### Semaines 1-2 : Preparation

- Finaliser l'ICP et valider avec 10 entretiens de confirmation
- Rediger le messaging framework (one-liner, elevator pitch, 3 piliers)
- Construire la liste cible initiale (300-500 prospects ICP qualifies)
- Configurer le CRM (pipeline stages, champs de qualification, templates d'emails)
- Creer le kit de vente : one-pager, deck de decouverte, template de proposal

### Semaines 3-6 : Premier lancement

- Lancer les premieres sequences outbound (email + LinkedIn) : 50 contacts/semaine
- Objectif : 10-15 rendez-vous de decouverte (discovery calls)
- Mesurer : taux d'ouverture email (> 40%), taux de reponse (> 5%), taux de conversion RDV
- Iterer sur le messaging apres chaque discovery call (quels mots resonent ?)
- Qualifier chaque opportunite avec MEDDIC ou BANT

### Semaines 7-10 : Premiere conversion

- Objectif : 3-5 propositions envoyees, 1-2 premiers clients signes
- Collecter le feedback exhaustif sur chaque deal gagne et perdu
- Documenter les objections recurrentes et les reponses qui fonctionnent
- Creer la premiere case study ou temoignage client (avec permission)
- Tester un deuxieme canal d'acquisition (ex : inbound content, events)

### Semaines 11-13 : Optimisation et scaling

- Analyser les metriques du premier cycle : CAC, taux de closing, cycle de vente
- Identifier le profil des clients qui ont converti le plus vite (affiner l'ICP)
- Scaler le canal qui a produit le meilleur ratio effort/resultat
- Recruter ou freelancer si le volume justifie l'embauche d'un premier commercial
- Etablir la cadence de reporting hebdomadaire (MRR, pipeline, metriques d'acquisition)
