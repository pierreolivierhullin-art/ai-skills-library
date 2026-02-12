# FP&A & Financial Modeling — Planification, Modeles Financiers, Scenarios & Rolling Forecasts

## Overview

Ce document de reference couvre les disciplines du FP&A (Financial Planning & Analysis) et de la modelisation financiere : construction de modeles a 3 etats, driver-based planning, analyse de scenarios, rolling forecasts, reporting board/COMEX et benchmarking. Utiliser ce guide comme fondation pour structurer la planification financiere, produire des previsions fiables et transformer les donnees en intelligence decisionnelle.

---

## FP&A — Role et Organisation

### Mission du FP&A

Le FP&A est le trait d'union entre la strategie et l'execution financiere. Sa mission se decline en quatre axes :

1. **Planifier** : construire le budget, les forecasts et les plans a moyen terme alignes avec la strategie.
2. **Analyser** : expliquer les ecarts entre le reel et le plan, identifier les tendances, alerter sur les risques.
3. **Anticiper** : produire des scenarios, simuler l'impact des decisions strategiques, projeter les trajectoires financieres.
4. **Communiquer** : traduire les chiffres en narratif actionnable pour le COMEX, le board et les investisseurs.

### Organisation type d'une equipe FP&A

| Role | Responsabilites | Profil |
|---|---|---|
| **VP Finance / CFO** | Vision strategique, relations investisseurs, arbitrages | Senior, business partner du CEO |
| **Head of FP&A** | Pilotage du processus budgetaire, coordination des forecasts, reporting board | 8-12 ans d'experience, maitrise modelisation |
| **FP&A Manager / Business Partner** | Analyse de la performance par BU, challenge des operationnels, scenarios | 5-8 ans, mix finance + business |
| **Financial Analyst** | Construction des modeles, automatisation des reportings, analyses ad hoc | 2-5 ans, competences techniques (Excel avance, SQL, BI) |
| **Data / BI Analyst** | Infrastructure de donnees, dashboards, automatisation des flux | 2-5 ans, competences data (Python, dbt, Looker/Power BI) |

### FP&A Maturity Model

| Niveau | Caracteristiques | Outils | % temps prospectif |
|---|---|---|---|
| **1 — Reactive** | Reporting historique, clotures longues, budget annuel fige | Excel | 10-20% |
| **2 — Informed** | Reporting mensuel fiable, analyse d'ecarts, reforecasts | Excel + BI (Power BI, Looker) | 30-40% |
| **3 — Predictive** | Rolling forecast, scenarios, driver-based planning | EPM (Pigment, Anaplan) + BI | 50-60% |
| **4 — Strategic** | Scenarios en temps reel, IA predictive, business partnering avance | EPM + AI + Data platform | 70-80% |

Objectif : atteindre le niveau 3 minimum pour toute entreprise de plus de 50 employes ou 10M EUR de CA.

---

## Driver-Based Planning

### Principes

Le driver-based planning consiste a construire les previsions financieres a partir de drivers operationnels plutot que de lignes comptables. Au lieu de prevoir "les charges de personnel seront de 4.2M EUR", modeliser "nous aurons 85 ETP a un cout moyen de 49K EUR avec un taux de charges de 45%".

#### Avantages du driver-based planning

- **Transparence** : chaque hypothese est explicite et challengeable.
- **Sensibilite** : modifier un driver recalcule automatiquement toute la cascade financiere.
- **Agilite** : les reforecasts sont plus rapides car on ne modifie que les drivers qui changent.
- **Appropriation** : les operationnels comprennent et valident les hypotheses car elles sont exprimees dans leur langage.

### Drivers types par fonction

| Fonction | Drivers cles | Metriques derivees |
|---|---|---|
| **Commercial** | Pipeline, taux de conversion, taille moyenne des deals, cycle de vente | CA nouveau, CA recurrent, mix produit |
| **Marketing** | Budget media, CAC par canal, taux de conversion, nombre de MQL/SQL | Leads generes, cout d'acquisition |
| **Produit / Tech** | Nombre de developpeurs, velocite, ratio features/maintenance | Cout de dev, time-to-market |
| **RH** | Headcount par departement, taux de turnover, cout moyen par ETP | Masse salariale, couts de recrutement |
| **Operations** | Volume de production, rendement, taux de defaut, cout matiere | COGS, marge brute |
| **Support / CS** | Nombre de tickets, temps moyen de resolution, CSAT | Cout de support par client |

### Construction d'un modele driver-based

```
Etape 1 : Identifier les 15-25 drivers cles qui expliquent 80% de la performance financiere
   |
Etape 2 : Definir les relations entre drivers et lignes financieres
   |-- CA = Nombre de clients x ARPU
   |-- COGS = Volume x Cout unitaire standard
   |-- Masse salariale = Headcount x Cout moyen x (1 + Taux charges)
   |-- Marketing = Budget par canal x Nombre de canaux
   |
Etape 3 : Calibrer les drivers sur l'historique (12-24 mois de donnees)
   |
Etape 4 : Definir les hypotheses de projection pour chaque driver
   |-- Scenario base : tendance historique + ajustements connus
   |-- Scenario haut : hypotheses optimistes sur les drivers cles
   |-- Scenario bas : stress test sur les drivers sensibles
   |
Etape 5 : Automatiser la cascade (driver -> P&L -> bilan -> cash flow)
```

---

## Modele Financier a 3 Etats (3-Statement Model)

### Architecture du Modele

Le modele financier integre a 3 etats (P&L, bilan, tableau de flux de tresorerie) est le standard de la modelisation financiere. Chaque etat est lie aux deux autres par des relations comptables fondamentales.

#### Liens entre les 3 etats

```
P&L --> Bilan : le resultat net alimente les capitaux propres (report a nouveau)
P&L --> Cash Flow : le resultat net est le point de depart du cash flow (methode indirecte)

Bilan --> Cash Flow : les variations de BFR (actif circulant - passif circulant) impactent le cash flow
Bilan --> P&L : les amortissements et provisions (bilan) sont des charges du P&L

Cash Flow --> Bilan : la variation de tresorerie met a jour la ligne de cash au bilan
Cash Flow --> Bilan : les investissements (CAPEX) alimentent les immobilisations au bilan
```

### Structure du P&L de Gestion

```
Chiffre d'affaires brut
  - Rabais, remises, ristournes
= Chiffre d'affaires net
  - Couts des marchandises vendues (COGS) / Couts de production
= Marge brute (Gross Margin)                     [KPI : % marge brute]
  - Frais de R&D
  - Frais commerciaux et marketing (S&M)
  - Frais generaux et administratifs (G&A)
= EBITDA                                          [KPI : % EBITDA]
  - Dotations aux amortissements et provisions (D&A)
= EBIT (Resultat d'exploitation)                  [KPI : % EBIT]
  - Resultat financier (interets nets)
= Resultat courant avant impots
  - Impot sur les societes (IS)
= Resultat net                                    [KPI : % resultat net]
```

### Construction du Bilan Previsionnel

| Poste | Methode de prevision | Driver |
|---|---|---|
| **Immobilisations nettes** | Immobilisations N-1 + CAPEX - Amortissements - Cessions | Plan d'investissement |
| **Stocks** | DIO (Days Inventory Outstanding) x COGS / 365 | Politique de stockage |
| **Creances clients** | DSO (Days Sales Outstanding) x CA / 365 | Conditions de paiement |
| **Dettes fournisseurs** | DPO (Days Payable Outstanding) x Achats / 365 | Conditions negociees |
| **Tresorerie** | Solde de tresorerie issu du tableau de flux | Cash flow cumule |
| **Dette financiere** | Dette N-1 + Nouveaux tirages - Remboursements | Plan de financement |
| **Capitaux propres** | CP N-1 + Resultat net - Dividendes + Augmentations de capital | Politique de distribution |

### Tableau de Flux de Tresorerie (Methode Indirecte)

```
Resultat net
  + Dotations aux amortissements et provisions (charges non cash)
  - Reprises de provisions (produits non cash)
  +/- Variation du BFR
     - Variation des stocks (augmentation = consommation de cash)
     - Variation des creances clients (augmentation = consommation de cash)
     + Variation des dettes fournisseurs (augmentation = source de cash)
     +/- Autres variations de BFR
= Cash flow d'exploitation (CFO)                  [KPI cle]

  - Acquisitions d'immobilisations (CAPEX)
  + Cessions d'immobilisations
  - Acquisitions de filiales (net de tresorerie acquise)
= Cash flow d'investissement (CFI)

  + Augmentations de capital
  + Nouveaux emprunts
  - Remboursements d'emprunts
  - Dividendes verses
  - Rachats d'actions
= Cash flow de financement (CFF)

Variation de tresorerie = CFO + CFI + CFF
Tresorerie fin de periode = Tresorerie debut + Variation
```

### Free Cash Flow (FCF)

```
FCF = Cash flow d'exploitation - CAPEX de maintenance
    = EBITDA - Impots cash - Variation du BFR - CAPEX de maintenance

FCF to Equity = FCF - Interets nets - Remboursements de dette + Nouveaux emprunts
FCF to Firm = EBIT x (1 - Taux IS) + D&A - CAPEX - Variation du BFR
```

Le FCF est la metrique ultime de creation de valeur car il mesure le cash genere par l'activite apres reinvestissement necessaire. Un FCF positif et croissant est le signe d'une entreprise saine.

---

## Scenario Analysis & Sensitivity

### Types de Scenarios

| Type | Description | Usage |
|---|---|---|
| **Base case** | Scenario central base sur les hypotheses les plus probables | Planification, budget, cibles operationnelles |
| **Upside (best case)** | Hypotheses favorables sur les drivers cles (+15-25% sur le CA, marges ameliorees) | Dimensionnement des opportunites, plans de croissance acceleres |
| **Downside (worst case)** | Stress test des drivers critiques (-20-30% sur le CA, degradation des marges) | Plans de contingence, reserves de cash, covenants |
| **Scenario strategique** | Impact d'une decision structurante (acquisition, nouveau marche, pivot produit) | Aide a la decision strategique, business case |
| **Black swan** | Evenement extreme a faible probabilite (pandemie, crise financiere, perte du client n1) | Test de resilience, plans de survie |

### Construction des Scenarios

```
Pour chaque scenario, definir :
1. Les hypotheses modifiees (quels drivers changent et de combien)
2. Le declencheur (trigger event)
3. Le timing (quand l'impact se materialise)
4. Les actions de mitigation prevues
5. L'impact sur le P&L, le bilan et le cash flow

Exemple — Scenario downside :
- Trigger : perte du client representant 15% du CA
- Timing : perte effective a M+3, impact CA sur 9 mois
- Hypotheses : CA -15%, pas de remplacement la premiere annee
- Mitigation : plan de reduction des couts (-10% OPEX), gel des recrutements
- Impact : EBITDA -35%, cash burn de 6 mois, tresorerie reste positive si action rapide
```

### Analyse de Sensibilite

L'analyse de sensibilite mesure l'impact de la variation d'un driver unique sur un KPI cible (toutes choses egales par ailleurs). Presenter sous forme de tableau de sensibilite croise.

#### Tableau de sensibilite type (EBITDA en fonction de 2 variables)

```
                    Croissance CA
EBITDA (M EUR)    -10%    Base    +10%    +20%
Marge brute -3%    2.1     3.5     4.9     6.3
Marge brute Base   3.0     4.5     6.0     7.5
Marge brute +3%    3.9     5.5     7.1     8.7
```

Ce format permet de visualiser immediatement la combinaison d'hypotheses la plus risquee et la plus favorable.

### Simulation Monte Carlo

Pour les modeles complexes, utiliser la simulation Monte Carlo :
1. Definir les distributions de probabilite de chaque driver cle (normal, triangulaire, uniforme).
2. Generer 10 000+ combinaisons aleatoires de drivers.
3. Calculer le P&L/cash flow pour chaque combinaison.
4. Analyser la distribution des resultats : moyenne, mediane, percentiles (P10, P25, P75, P90).
5. Presenter les resultats sous forme de cones de probabilite (fan charts).

Outils : @RISK (Excel add-in), Crystal Ball, Python (scipy, numpy), R.

---

## Rolling Forecast

### Principes du Rolling Forecast

Le rolling forecast est une prevision glissante sur un horizon fixe (typiquement 12 a 18 mois) mise a jour mensuellement ou trimestriellement. Contrairement au budget annuel qui "vieillit" au fil de l'exercice, le rolling forecast maintient une visibilite constante sur l'avenir.

#### Budget traditionnel vs Rolling Forecast

| Critere | Budget annuel | Rolling Forecast |
|---|---|---|
| **Horizon** | Exercice comptable (12 mois fixes) | 12-18 mois glissants |
| **Frequence de mise a jour** | 1 fois/an (+ reforecasts) | Mensuel ou trimestriel |
| **Granulite** | Detaille (par mois, par compte) | Macro (par trimestre, par driver) |
| **Effort** | Eleve (3-4 mois de processus) | Modere si driver-based |
| **Pertinence en fin d'exercice** | Faible (hypotheses obsoletes) | Toujours actuelle |
| **Culture** | "Atteindre le budget" | "S'adapter a la realite" |

#### Mise en oeuvre du Rolling Forecast

1. **Definir l'horizon** : 12 mois minimum (toujours voir au-dela de l'exercice en cours). 18 mois recommande pour les secteurs cycliques ou les entreprises en croissance rapide.
2. **Fixer la granulite** : les 3 premiers mois en detail mensuel, les mois 4-6 en detail mensuel ou agrege, les mois 7-18 en detail trimestriel.
3. **Identifier les 15-20 drivers cles** : ne pas reconstruire tout le P&L ligne par ligne. Se concentrer sur les drivers a fort impact (CA par produit/client, headcount, CAPEX).
4. **Automatiser la collecte** : les operationnels mettent a jour leurs drivers dans un outil collaboratif (Pigment, Anaplan) plutot que par echange de fichiers.
5. **Produire le forecast integre** : cascade automatique driver -> P&L -> bilan -> cash flow.
6. **Comparer au budget** : le rolling forecast ne remplace pas le budget comme reference de pilotage. Les deux coexistent : le budget sert a mesurer la performance, le rolling forecast sert a anticiper.

---

## Board Reporting & COMEX Communication

### Principes du Reporting Board

Le reporting board doit etre synthetique, actionnable et oriente vers la decision. Respecter la regle "So what?" : chaque slide doit repondre a la question "et alors, que fait-on ?".

#### Structure type d'un reporting board (10-15 slides)

| Section | Contenu | Format |
|---|---|---|
| **Executive Summary** | 3-5 messages cles, alertes, decisions requises | Texte + KPIs en traffic light |
| **P&L Summary** | Reel vs budget vs N-1, EBITDA bridge | Tableau + bridge chart |
| **Revenue Deep Dive** | CA par produit/region/segment, pipeline commercial | Graphiques, commentaires |
| **OPEX Review** | Couts par nature, headcount, ratio efficiency | Tableau, trend lines |
| **Cash Position** | Tresorerie, FCF, prevision 13 semaines, covenant compliance | Graphique de tresorerie |
| **KPIs Operationnels** | 8-12 KPIs cles en traffic light (rouge/orange/vert) | Dashboard |
| **Forecast Update** | Mise a jour du rolling forecast, comparaison au budget | Bridge chart |
| **Risks & Opportunities** | Top 5 risques et opportunites avec probabilite et impact | Matrice risques |
| **Decisions Required** | 2-3 decisions attendues du board avec options et recommandation | Format RACI |

#### Bonnes pratiques de communication financiere

- **Pyramide inversee** : commencer par la conclusion et le "so what", puis detailler. Le board doit comprendre l'essentiel dans les 2 premieres minutes.
- **Traffic light system** : vert (on track), orange (alerte, action en cours), rouge (hors trajectoire, decision requise). Appliquer a chaque KPI.
- **Narrative + chiffres** : chaque chiffre doit etre accompagne d'un commentaire qualitatif. Chaque commentaire doit etre etaye par un chiffre.
- **Comparer 3 references** : toujours presenter reel vs budget vs N-1 (ou reel vs forecast vs N-1). Jamais un chiffre isole.
- **Actions correctives** : chaque ecart negatif materiel doit etre accompagne d'un plan d'action date avec un responsable identifie.

---

## Benchmarking Financier

### Methode de Benchmarking

1. **Identifier les pairs** : selectionner 5-10 entreprises comparables par taille, secteur, modele economique et geographie.
2. **Collecter les donnees** : rapports annuels, bases de donnees (S&P Capital IQ, PitchBook, Statista), enquetes sectorielles.
3. **Normaliser** : ajuster les donnees pour les rendre comparables (normes comptables, perimetre, devises, evenements exceptionnels).
4. **Comparer les ratios cles** : marges, croissance, intensite capitalistique, productivite, BFR.
5. **Identifier les ecarts** : positionner l'entreprise sur chaque metrique (quartile 1 a 4) et identifier les axes d'amelioration.

### Ratios de Benchmarking par Secteur

| Ratio | SaaS B2B | E-commerce | Industrie | Services |
|---|---|---|---|---|
| **Marge brute** | 70-85% | 25-45% | 30-50% | 50-70% |
| **Marge EBITDA** | 15-35% (a maturite) | 5-15% | 10-20% | 15-25% |
| **Croissance CA** | 30-100% (early) / 15-30% (mature) | 15-40% | 3-10% | 5-15% |
| **Rule of 40** | Croissance + marge > 40% | N/A | N/A | N/A |
| **DSO** | 45-75 jours | 5-15 jours | 50-80 jours | 60-90 jours |
| **CAPEX / CA** | 3-8% | 5-15% | 10-25% | 2-5% |
| **CA / employe** | 150-300K EUR | 200-500K EUR | 150-350K EUR | 100-200K EUR |

---

## State of the Art (2024-2026)

### FP&A Augmente par l'IA

L'intelligence artificielle transforme fondamentalement le metier du FP&A :

- **Forecasting predictif** : les modeles de ML (XGBoost, Prophet, ARIMA augmente) complementent les previsions traditionnelles base sur le jugement humain. Les meilleures pratiques combinent des modeles statistiques avec le jugement des experts (ensemble forecasting). Precision amelioree de 15-30% sur les previsions de CA a 3-6 mois selon les etudes.
- **Detection d'anomalies** : les algorithmes identifient automatiquement les ecarts inhabituels dans les donnees financieres (lignes de depenses hors norme, ratios anormaux) et alertent le FP&A avant la revue manuelle.
- **Scenario generation automatique** : les modeles GenAI (GPT-4, Claude) peuvent generer des scenarios a partir de descriptions textuelles et calibrer les hypotheses sur des donnees de marche. L'analyste valide et ajuste plutot que de construire de zero.
- **Narrative intelligence** : generation automatique de commentaires d'ecarts, de rapports de performance et de briefings board. Reduction de 40-60% du temps consacre a la redaction narrative selon les premiers retours d'experience.
- **Natural language querying** : les dirigeants posent des questions en langage naturel ("quel est notre DSO par region ce trimestre ?") et obtiennent des reponses instantanees a partir des donnees financieres. Outils : ThoughtSpot, Sigma Computing, fonctionnalites Q&A de Power BI.

### xP&A — Extended Planning & Analysis

Le concept d'xP&A (Gartner, 2020) etend le FP&A au-dela de la finance pour integrer la planification operationnelle (ventes, supply chain, workforce) dans un modele unifie :

- **Sales & Operations Planning (S&OP) integre** : le forecast financier est directement alimente par le forecast commercial (pipeline CRM) et le plan de production (ERP).
- **Workforce planning** : la prevision de masse salariale est liee au plan de recrutement, au plan de formation et aux projections d'attrition.
- **CAPEX planning** : les investissements sont planifies en lien avec la roadmap produit et la strategie de croissance.
- **Impact** : elimination des silos de planification, coherence des hypotheses entre fonctions, reduction du cycle de planification de 30-50%.

### Connected Planning et Real-Time Finance

L'architecture de donnees moderne permet une finance en temps reel :

- **Data mesh applique a la finance** : chaque domaine (comptabilite, controlling, tresorerie) publie ses donnees financieres comme des "data products" consommables par les autres.
- **Reverse ETL** : les donnees analytiques (KPIs, forecasts) sont poussees vers les outils operationnels (CRM, ERP) pour que les decisions soient informees en temps reel.
- **Embedded analytics** : les KPIs financiers sont integres directement dans les workflows operationnels (dashboard de vente avec marge en temps reel, dashboard RH avec cout du turnover).
- **Event-driven finance** : declenchement automatique de re-forecasts lorsqu'un evenement significatif se produit (perte d'un gros client, signature d'un contrat majeur, changement de taux de change > seuil).

### Zero-Based Budgeting (ZBB) Modernise

Le ZBB (chaque ligne de depense est justifiee a partir de zero chaque annee, sans reference au budget precedent) connait un renouveau en 2024-2026, porte par les contraintes de marge et les outils modernes :

- **ZBB selectif** : appliquer le ZBB uniquement aux postes de depenses discretionnaires (marketing, consulting, deplacements, outils SaaS) et non aux couts structurels.
- **ZBB continu** : revue trimestrielle des depenses plutot qu'annuelle, pour capter plus rapidement les economies.
- **Outils** : les plateformes FP&A modernes permettent d'automatiser le processus ZBB (collecte des justificatifs, workflow d'approbation, suivi des economies).
- **Culture** : le ZBB fonctionne quand il est presente comme un outil d'allocation optimale des ressources, pas comme un exercice de coupe budgetaire.

### Continuous Planning et Scenario Planning as a Service

Les organisations les plus matures abandonnent le cycle plan/forecast/reforecast au profit d'un "continuous planning" :

- **Trigger-based replanning** : au lieu de mettre a jour le forecast a date fixe, le declencheur est un evenement (ecart >X% sur un KPI, evenement marche, decision strategique).
- **Scenario libraries** : constitution de bibliotheques de scenarios pre-calibres (recession, hypercroissance, perte de client cle, changement reglementaire) activables en quelques clics.
- **War room financier** : en cas de crise, capacite a produire un scenario d'impact complet (P&L, cash, bilan) en moins de 48 heures au lieu de 2-3 semaines.
- **Digital twins financiers** : replique numerique du modele financier de l'entreprise permettant de simuler l'impact de toute decision en temps reel avant execution.
