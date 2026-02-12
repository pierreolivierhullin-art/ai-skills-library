# Risk Assessment — Identification, Evaluation Methods, Heat Maps, KRIs, Stress Testing

Reference complete pour l'identification et l'evaluation des risques d'entreprise, les methodologies qualitatives, semi-quantitatives et quantitatives, les matrices de risques, les KRIs, les risques emergents et les analyses de scenarios (2024-2026).

---

## Risk Register & Taxonomy — Structurer l'identification des risques

### Taxonomie des risques d'entreprise

Structurer l'identification des risques autour d'une taxonomie adaptee a l'organisation. Voici une taxonomie de reference a adapter :

**Niveau 1 — Categories principales** :

| Categorie | Perimetre | Exemples |
|-----------|----------|----------|
| **Strategique** | Risques lies aux choix strategiques et a l'environnement concurrentiel | Disruption du modele d'affaires, echec M&A, perte de marche, dependance client/fournisseur |
| **Operationnel** | Risques lies aux processus, personnes et systemes internes | Defaillance processus, erreur humaine, panne IT, fraude interne, perte de competences cles |
| **Financier** | Risques lies aux flux financiers et aux marches | Liquidite, credit, change, taux d'interet, valorisation d'actifs |
| **Conformite** | Risques lies aux lois, reglementations et normes | Non-conformite reglementaire, sanctions, litige, manquement contractuel |
| **Reputationnel** | Risques lies a l'image et a la confiance des parties prenantes | Crise mediatique, perte de confiance clients, scandale ethique |
| **Cyber** | Risques lies a la securite des systemes d'information | Cyberattaque, ransomware, fuite de donnees, indisponibilite IT |
| **Climatique / ESG** | Risques lies au changement climatique et aux enjeux durables | Risque physique (inondation, canicule), risque de transition, greenwashing |
| **Geopolitique** | Risques lies a l'instabilite politique et aux relations internationales | Sanctions, conflit arme, nationalisation, restriction d'export |

**Niveau 2 — Sous-categories** : decliner chaque categorie en sous-categories specifiques au secteur et a l'organisation. Une banque aura des sous-categories financieres bien plus detaillees (risque de marche, risque de credit, risque de liquidite, risque de contrepartie) qu'une entreprise industrielle.

### Risk Register — Template operationnel

Chaque risque du registre doit contenir les informations suivantes :

```
RISK REGISTER ENTRY
===================
Risk ID           : RISK-[CATEGORY]-[NNN]     (ex: RISK-OPS-042)
Risk Title        : Titre court et explicite
Category          : Categorie de niveau 1 et 2
Description       : Description detaillee du scenario de risque
                    Format : "Si [evenement declencheur], alors [consequence]
                    impactant [population/processus] avec [type d'impact]"
Risk Owner        : Nom, fonction (personne physique)
Business Unit     : Unite(s) concernee(s)

EVALUATION INHERENTE (avant controles)
Probability       : 1-Rare | 2-Peu probable | 3-Possible | 4-Probable | 5-Tres probable
Impact            : 1-Negligeable | 2-Mineur | 3-Modere | 4-Majeur | 5-Critique
Velocity          : Lent (>1 an) | Modere (1-6 mois) | Rapide (1-4 semaines) | Immediat (<1 semaine)
Inherent Risk     : Probability x Impact = [Score]

CONTROLES EXISTANTS
Controls          : Liste des controles en place
Control Effectiveness : Forte | Adequate | Faible | Inexistante

EVALUATION RESIDUELLE (apres controles)
Residual Probability : [1-5]
Residual Impact      : [1-5]
Residual Risk Score  : [Score]

PLAN D'ACTION
Response Strategy : Eviter | Attenuer | Transferer | Accepter
Action Plan       : Actions specifiques, proprietaire, echeance
Target Risk Level : Niveau de risque cible apres actions
KRI Associated    : Indicateur(s) de suivi associe(s)

SUIVI
Status            : Ouvert | En traitement | Accepte | Ferme
Last Review       : Date de derniere revue
Next Review       : Date de prochaine revue
Change History    : Historique des modifications
```

### Methodes d'identification des risques

Combiner plusieurs methodes pour assurer l'exhaustivite :

**Ateliers de risques (risk workshops)** : reunir les parties prenantes cles (management, experts metier, fonctions support) pour identifier les risques de maniere collaborative. Utiliser des techniques de facilitation (brainstorming structure, technique Delphi, analyse pre-mortem). Duree recommandee : 2-3 heures par business unit. Programmer au minimum une session annuelle par unite majeure.

**Interviews individuelles** : completer les ateliers par des entretiens individuels avec les dirigeants et les experts cles. Les interviews revelent souvent des risques que les participants n'osent pas evoquer en groupe (risques de fraude, dysfonctionnements internes, tensions interpersonnelles).

**Analyse de l'historique** : exploiter la base d'incidents, les rapports d'audit, les reclamations clients, les contentieux passes. L'historique est un predicteur imparfait mais indispensable. Analyser les tendances sur 3 a 5 ans.

**Veille externe** : surveiller l'environnement reglementaire, concurrentiel, technologique et geopolitique. Analyser les incidents survenus dans le secteur (benchmarking d'incidents). Suivre les publications des regulateurs et des associations professionnelles.

**Analyse pre-mortem** : imaginer que le projet ou l'initiative a echoue et reconstituer les causes de l'echec. Technique particulierement efficace pour les projets strategiques et les lancements de produits.

---

## Methodologies d'evaluation des risques

### Evaluation qualitative

L'evaluation qualitative est la methode la plus repandue et la plus accessible. Elle repose sur le jugement d'expert pour classer les risques en categories de probabilite et d'impact.

**Echelle de probabilite** :

| Niveau | Designation | Description | Frequence indicative |
|--------|------------|-------------|---------------------|
| 1 | Rare | Evenement exceptionnel, jamais survenu dans l'organisation | < 1 fois en 10 ans |
| 2 | Peu probable | Evenement survenu rarement, conditions inhabituelles | 1 fois en 5-10 ans |
| 3 | Possible | Evenement pouvant se produire dans des conditions normales | 1 fois en 2-5 ans |
| 4 | Probable | Evenement susceptible de se produire regulierement | 1 a 3 fois par an |
| 5 | Tres probable | Evenement attendu dans la plupart des circonstances | > 3 fois par an |

**Echelle d'impact** :

| Niveau | Designation | Financier | Operationnel | Reputationnel | Reglementaire |
|--------|------------|-----------|-------------|---------------|--------------|
| 1 | Negligeable | < 50K EUR | Perturbation mineure, < 2h | Impact local, non mediatise | Observation, remarque |
| 2 | Mineur | 50K-500K EUR | Perturbation limitee, < 1 jour | Couverture locale, impact limite | Non-conformite mineure, mise en demeure |
| 3 | Modere | 500K-5M EUR | Perturbation significative, 1-5 jours | Couverture nationale, perte clients limitee | Sanction financiere moderee |
| 4 | Majeur | 5M-50M EUR | Interruption majeure, 5-30 jours | Couverture internationale, perte clients significative | Sanction majeure, mise sous surveillance |
| 5 | Critique | > 50M EUR | Interruption prolongee, > 30 jours, survie menacee | Crise mediatique majeure, perte de confiance generalisee | Retrait d'agrement, poursuites penales |

**Important** : adapter les echelles financieres a la taille de l'organisation. Les seuils ci-dessus correspondent a une ETI/grande entreprise (CA > 100M EUR). Pour une PME, diviser les seuils par 10 ou 100.

### Evaluation semi-quantitative

L'evaluation semi-quantitative ajoute de la granularite en introduisant des scores numeriques et des facteurs supplementaires.

**Methode AMDEC/FMEA (Analyse des Modes de Defaillance, de leurs Effets et de leur Criticite)** :

Calculer un indice de priorite du risque (IPR/RPN) en combinant trois facteurs :

```
IPR = Frequence (F) x Gravite (G) x Detectabilite (D)

F : Frequence d'occurrence (1-10)
G : Gravite de l'impact (1-10)
D : Difficulte de detection (1-10, ou 10 = non detectable)

IPR maximal : 1000
Seuil d'action typique : IPR > 100 necessite un plan d'action
```

L'AMDEC est particulierement adaptee aux risques processus (industriels, IT, supply chain). Conduire l'AMDEC en atelier avec les experts du processus concerne.

**Bow-tie analysis** :

La methode bow-tie (noeud papillon) est un outil visuel puissant pour analyser un risque specifique en identifiant :
- A gauche : les **menaces** (causes) et les **barrieres de prevention** qui empechent l'evenement de se produire
- Au centre : l'**evenement redoute** (le risque qui se materialise)
- A droite : les **consequences** et les **barrieres de mitigation** qui limitent l'impact

```
MENACES                    EVENEMENT REDOUTE              CONSEQUENCES

[Menace 1] --[Barriere P1]--> |                    | --[Barriere M1]--> [Consequence 1]
[Menace 2] --[Barriere P2]--> | CYBERATTAQUE       | --[Barriere M2]--> [Consequence 2]
[Menace 3] --[Barriere P3]--> | RANSOMWARE         | --[Barriere M3]--> [Consequence 3]
[Menace 4] -----------------> |                    | --[Barriere M4]--> [Consequence 4]

Barrieres prevention :          Barrieres mitigation :
- Firewall, segmentation       - Backups testes
- Formation phishing            - PRA/DRP active
- Patch management              - Assurance cyber
- MFA obligatoire               - Communication de crise
```

Evaluer l'efficacite de chaque barriere (couleur : vert/jaune/rouge). Une barriere absente ou inefficace revele une vulnerabilite prioritaire.

### Evaluation quantitative

L'evaluation quantitative exprime les risques en termes financiers (perte attendue, valeur exposee) et utilise des methodes statistiques.

**Expected Loss (perte attendue)** :

```
Expected Loss = Probability x Impact (en valeur monetaire)

Exemple :
- Risque de fraude fournisseur
- Probabilite annuelle : 15% (basee sur historique sectoriel)
- Impact moyen : 2M EUR
- Expected Loss = 0.15 x 2,000,000 = 300,000 EUR/an

Utiliser l'Expected Loss pour :
- Justifier les investissements en controles (le controle coute moins que la perte attendue)
- Comparer les risques entre eux sur une base commune
- Alimenter la decision d'assurance (prime vs perte attendue)
```

**Simulation Monte Carlo** :

La simulation Monte Carlo genere des milliers de scenarios aleatoires pour modeliser la distribution des pertes potentielles.

```
Processus :
1. Definir les variables d'entree et leurs distributions de probabilite
   (ex: probabilite de panne = distribution beta, impact = distribution lognormale)
2. Generer N scenarios aleatoires (typiquement 10,000-100,000)
3. Calculer la perte pour chaque scenario
4. Analyser la distribution des resultats

Outputs :
- Perte attendue (moyenne de la distribution)
- Perte maximale probable au seuil de confiance 95% (VaR 95%)
- Perte maximale probable au seuil de confiance 99% (VaR 99%)
- Distribution des scenarios (percentiles)

Outils : @Risk (Palisade), Crystal Ball (Oracle), Python (numpy/scipy)
```

**FAIR (Factor Analysis of Information Risk)** :

FAIR est la methode de reference pour la quantification des risques cyber en termes financiers. Elle decompose le risque en facteurs mesurables :

```
Risk = Loss Event Frequency x Loss Magnitude

Loss Event Frequency :
  = Threat Event Frequency x Vulnerability
  (Combien de fois la menace se presente x probabilite d'exploiter la vulnerabilite)

Loss Magnitude :
  = Primary Loss + Secondary Loss
  Primary : couts directs (reponse incident, restauration, productivite perdue)
  Secondary : couts indirects (amendes, litiges, perte de clients, atteinte reputation)
```

---

## Heat Maps & Risk Matrices — Cartographies de risques

### Matrice de risques 5x5

La matrice de risques est l'outil de communication le plus efficace pour presenter le profil de risque au management et au conseil d'administration.

```
IMPACT
  5 | Critique    |  5  | 10  | 15  | 20  | 25  |
  4 | Majeur      |  4  |  8  | 12  | 16  | 20  |
  3 | Modere      |  3  |  6  |  9  | 12  | 15  |
  2 | Mineur      |  2  |  4  |  6  |  8  | 10  |
  1 | Negligeable |  1  |  2  |  3  |  4  |  5  |
    +-------------+-----+-----+-----+-----+-----+
                  |  1  |  2  |  3  |  4  |  5  |
                  |Rare |Peu  |Poss.|Prob.|Tres |
                  |     |prob.|     |     |prob.|
                                PROBABILITE

Zones de risque :
  Score 1-4   : FAIBLE    (vert)     -> Accepter, monitorer
  Score 5-9   : MODERE    (jaune)    -> Attenuer, plan d'action
  Score 10-16 : ELEVE     (orange)   -> Traitement prioritaire
  Score 17-25 : CRITIQUE  (rouge)    -> Action immediate, escalade
```

### Regles de construction d'une heat map efficace

1. **Limiter le nombre de risques affiches** : une heat map avec 200 risques est illisible. Afficher les 15-25 risques principaux. Utiliser des sous-heat maps par categorie pour le detail.

2. **Differencier risque inherent et risque residuel** : afficher les deux (par exemple avec une fleche du risque inherent vers le risque residuel) pour visualiser l'effet des controles.

3. **Ajouter la dimension velocity** : un risque a impact critique et vitesse immediate exige une reponse differente d'un risque a impact critique mais a evolution lente. Utiliser la taille ou la forme des points pour representer la velocity.

4. **Mettre a jour regulierement** : une heat map datee de plus de 6 mois est obsolete. Viser une mise a jour trimestrielle minimum.

5. **Eviter les biais de representation** : ne pas concentrer artificiellement les risques au centre de la matrice. Challenger les evaluations "moyennes" qui evitent de prendre position.

---

## Key Risk Indicators (KRIs) — Indicateurs cles de risque

### Principes de conception des KRIs

Un bon KRI possede les caracteristiques suivantes :

- **Mesurable** : quantifiable objectivement, sans interpretation subjective
- **Predictif** : signale une evolution du risque AVANT que le risque ne se materialise (indicateur avance, pas retarde)
- **Actionnable** : un depassement de seuil declenche une action concrete et documentee
- **Temporel** : mesure a frequence definie, avec historique et tendance
- **Proportionne** : le cout de collecte est proportionnel a la valeur de l'information

### Exemples de KRIs par categorie

| Categorie | KRI | Seuil d'alerte (jaune) | Seuil critique (rouge) | Frequence |
|-----------|-----|----------------------|----------------------|-----------|
| **Operationnel** | Taux de rotation du personnel cle | > 10%/an | > 20%/an | Mensuel |
| **Operationnel** | Nombre d'incidents de production | > 5/mois | > 15/mois | Hebdomadaire |
| **Financier** | Ratio de liquidite (current ratio) | < 1.5 | < 1.0 | Mensuel |
| **Financier** | Concentration client (% CA top client) | > 20% | > 35% | Trimestriel |
| **Cyber** | Nombre de vulnerabilites critiques non patchees | > 5 | > 15 | Hebdomadaire |
| **Cyber** | Delai moyen de correction des vulnerabilites critiques | > 15 jours | > 30 jours | Mensuel |
| **Conformite** | Nombre de retards de formation obligatoire | > 10% effectif | > 25% effectif | Mensuel |
| **Conformite** | Nombre de non-conformites ouvertes | > 3 | > 10 | Mensuel |
| **Reputationnel** | Score NPS | < 30 | < 10 | Mensuel |
| **Reputationnel** | Nombre de plaintes clients graves | > 5/mois | > 15/mois | Hebdomadaire |
| **Supply chain** | Taux de dependance fournisseur unique | > 30% achats | > 50% achats | Trimestriel |
| **Supply chain** | Delai de livraison moyen vs SLA | > +10% | > +25% | Hebdomadaire |

### Dashboard de risque — Architecture

Structurer le tableau de bord de risque en trois niveaux :

**Niveau strategique (conseil d'administration)** :
- Heat map consolidee des risques majeurs (top 15-20)
- Evolution du profil de risque vs appetence au risque
- KRIs strategiques en depassement
- Incidents majeurs et near-misses du trimestre
- Etat d'avancement des plans d'action prioritaires

**Niveau tactique (direction)** :
- Heat map par business unit ou categorie de risque
- Tous les KRIs avec statut et tendance
- Detail des risques en depassement de tolerance
- Suivi des plans d'action avec proprietaires et echeances
- Points reglementaires et de conformite

**Niveau operationnel (management)** :
- KRIs operationnels en temps reel
- Incidents ouverts et en traitement
- Statut des controles et des actions correctives
- Alertes et notifications

---

## Emerging Risks — Identification et veille

### Definition et caracteristiques

Un risque emergent est un risque nouveau ou en evolution dont les contours sont encore mal definis et dont l'impact potentiel est difficile a quantifier. Caracteristiques :

- **Incertitude elevee** : probabilite et impact difficilement estimables
- **Horizon temporel** : peut se materialiser dans 1 a 10 ans
- **Potentiel de disruption** : peut transformer fondamentalement le profil de risque
- **Interconnexion** : souvent lie a d'autres risques (effets en cascade)

### Risques emergents prioritaires (2024-2026)

| Risque emergent | Horizon | Impact potentiel | Secteurs les plus exposes |
|----------------|---------|-----------------|--------------------------|
| **IA generative non maitrisee** | Immediat-2 ans | Reputationnel, legal, operationnel | Tous secteurs |
| **Deepfakes et desinformation** | Immediat-2 ans | Reputationnel, fraude | Finance, media, politique |
| **Souverainete numerique** | 1-3 ans | Strategique, operationnel | Tech, defense, sante |
| **Risque climatique physique** | 2-10 ans | Operationnel, financier, assurance | Industrie, agriculture, immobilier |
| **Resistance antimicrobienne** | 3-10 ans | Operationnel, supply chain | Sante, agroalimentaire |
| **Quantum computing (crypto)** | 5-10 ans | Cyber, confidentialite | Finance, defense, tech |
| **Penurie de competences critiques** | Immediat-3 ans | Operationnel, strategique | Tech, sante, industrie |
| **Polarisation sociopolitique** | Immediat-5 ans | Reputationnel, operationnel | Tous secteurs |

### Processus de veille sur les risques emergents

1. **Definir les sources** : publications regulateurs, rapports WEF (Global Risks Report), rapports sectoriels, think tanks, publications academiques, signaux faibles (brevets, startups, legislation en preparation)
2. **Organiser la collecte** : assigner la veille thematique a des experts internes. Completer par des outils de veille automatisee (NLP sur flux d'actualites, alertes Google, Feedly)
3. **Evaluer et qualifier** : revue trimestrielle des risques emergents identifies. Evaluer la plausibilite, l'horizon temporel et l'impact potentiel
4. **Integrer dans le registre** : ajouter les risques emergents qualifies au registre avec un tag "emergent" et une revue plus frequente
5. **Declencher des analyses approfondies** : pour les risques emergents juges significatifs, lancer des analyses de scenarios dediees

---

## Scenario Analysis & Stress Testing

### Scenario analysis

L'analyse de scenarios explore l'impact de situations hypothetiques plausibles sur l'organisation. Contrairement a l'evaluation de risque classique (un risque = un scenario), l'analyse de scenarios combine plusieurs evenements pour modeliser des situations complexes.

**Types de scenarios** :

| Type | Description | Utilisation |
|------|-------------|------------|
| **Best case** | Evolution favorable de l'ensemble des facteurs | Calibrer les objectifs ambitieux |
| **Base case** | Continuation des tendances actuelles | Reference pour le budget et les previsions |
| **Adverse** | Deterioration significative d'un ou plusieurs facteurs | Tester la resilience et calibrer les reserves |
| **Severe** | Combinaison d'evenements adverses extremes mais plausibles | Stress testing reglementaire, BCP |
| **Reverse stress test** | Identifier les scenarios qui mettraient l'organisation en defaillance | Identifier les vulnerabilites existentielles |

**Processus de construction d'un scenario** :

1. **Definir l'objectif** : que cherche-t-on a tester ? (solidite financiere, continuite operationnelle, reputation)
2. **Identifier les facteurs de risque** : quels evenements ou tendances pourraient impacter l'objectif ?
3. **Construire la narration** : ecrire le deroulement du scenario de maniere detaillee et chronologique
4. **Quantifier les impacts** : estimer l'impact financier, operationnel, reputationnel de chaque phase du scenario
5. **Evaluer la reponse** : les plans existants (BCP, reserves financieres, assurances) sont-ils suffisants ?
6. **Tirer les conclusions** : identifier les vulnerabilites et definir les actions correctives

### Stress testing

Le stress testing est une forme specifique d'analyse de scenarios focalisee sur la resistance de l'organisation a des conditions extremes.

**Stress testing financier** :
- Tester la resistance de la tresorerie a un choc de revenus (-20%, -40%, -60%)
- Simuler l'impact d'une hausse des taux d'interet (+200bps, +400bps)
- Evaluer la solidite du bilan face a une depreciation des actifs
- Modeliser l'impact d'un defaut de paiement d'un client majeur

**Stress testing operationnel** :
- Simuler la perte d'un site critique (incendie, inondation, cyberattaque)
- Tester l'impact de la perte d'un fournisseur cle pendant 3 mois
- Evaluer la capacite a operer avec 30-50% de l'effectif indisponible
- Simuler une panne IT prolongee (> 48h) sur les systemes critiques

**Stress testing reputationnel** :
- Modeliser l'impact d'une crise mediatique majeure sur les ventes et la retention clients
- Evaluer les consequences d'un scandale ethique (travail des enfants dans la supply chain, corruption)
- Simuler la fuite massive de donnees personnelles et l'impact RGPD

---

## State of the Art (2024-2026)

### Tendances majeures en evaluation des risques

**1. Risk Intelligence augmentee par l'IA** : les outils de risk assessment integrent desormais des capacites d'IA pour automatiser l'identification de risques (NLP sur contrats, actualites, rapports financiers), predire la materialisation de risques (modeles predictifs sur historique d'incidents), et generer des recommandations de mitigation. Les plateformes comme Riskonnect, LogicGate et Archer integrent des modules d'IA generative pour l'analyse de risques en 2025-2026.

**2. Continuous Risk Assessment** : le modele traditionnel d'evaluation annuelle des risques cede la place a une evaluation continue. Les KRIs automatises, la surveillance en temps reel des signaux faibles et les dashboards dynamiques permettent une mise a jour quasi-temps reel du profil de risque. La frequence de revue passe de annuelle a trimestrielle (minimum), voire continue pour les risques cyber et operationnels.

**3. Interconnected Risk Modeling** : les organisations matures modelisent les interdependances entre risques (risk interdependency mapping). Un evenement declencheur peut provoquer une cascade de risques : une cyberattaque peut entrainer une interruption operationnelle, une fuite de donnees, une sanction reglementaire, une crise de reputation et une perte de clients. La modelisation de ces cascades permet de reveler le "vrai" impact d'un risque.

**4. Climate Risk Integration** : la Task Force on Climate-related Financial Disclosures (TCFD, desormais integree dans les standards ISSB/IFRS S2) et la CSRD europeenne imposent l'integration des risques climatiques dans les exercices de scenario analysis. Les entreprises doivent tester leur resilience face a des scenarios de rechauffement (+1.5C, +2C, +3C) et de transition energetique (tarification carbone, interdictions sectorielles).

**5. Quantification systematique** : la tendance est a la quantification financiere des risques, meme pour les categories traditionnellement evaluees qualitativement (reputation, ESG). La methode FAIR pour le cyber, les modeles actuariels pour les risques climatiques, et les analyses economiques pour les risques reputationnels gagnent en adoption. L'objectif : comparer les risques entre eux et avec le cout des mitigations sur une base commune (EUR/USD).

**6. Dynamic Risk Appetite** : l'appetence au risque evolue d'un enonce statique vers un cadre dynamique qui s'ajuste aux conditions de marche. En periode de crise, l'organisation reduit son appetence ; en periode de croissance, elle peut l'augmenter de maniere controlee. Les seuils de tolerance sont revus trimestriellement et non plus annuellement.

**7. Third-Party Risk Scoring** : l'evaluation des risques lies aux tiers (fournisseurs, partenaires) s'automatise via des plateformes de scoring en continu (BitSight, SecurityScorecard pour le cyber, EcoVadis pour l'ESG, Dun & Bradstreet pour le financier). Ces scores alimentent automatiquement le registre des risques et declenchent des alertes en cas de degradation.

### Outils d'evaluation des risques (2024-2026)

| Outil | Specialite | Forces |
|-------|-----------|--------|
| **Palisade @Risk** | Simulation Monte Carlo (Excel add-in) | Accessibilite, integration Excel |
| **RiskLens** | Quantification FAIR des risques cyber | Reference FAIR, reporting executif |
| **Resolver (Kyndryl)** | Risk assessment et incident management | Workflows, integration IT |
| **Origami Risk** | Risk management et assurance integres | Plateforme unifiee, analytics |
| **Navex Global** | GRC et whistleblowing integres | Compliance leader, hotline |
| **BitSight / SecurityScorecard** | Scoring cyber des tiers | Monitoring continu, benchmarking |
| **EcoVadis** | Scoring ESG des fournisseurs | Standard europeen, supply chain |
| **Python (scipy, numpy, pandas)** | Modelisation quantitative sur mesure | Flexibilite, gratuit, communaute |
