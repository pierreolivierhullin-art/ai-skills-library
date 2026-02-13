---
name: finance
description: This skill should be used when the user asks about "financial planning", "FP&A", "budget forecasting", "cash management", "fundraising strategy", "financial modeling", "planification financière", "prévision budgétaire", "gestion de trésorerie", "levée de fonds", "modélisation financière", "business plan financier", "unit economics", "SaaS metrics", "MRR", "ARR", "churn rate", "LTV", "CAC", "burn rate", "runway", "P&L", "compte de résultat", "bilan", "balance sheet", "cash flow", "flux de trésorerie", "EBITDA", "ROI", "audit interne", "internal audit", "tax strategy", "stratégie fiscale", "corporate finance", "valorisation", "valuation", "due diligence financière", discusses unit economics, or needs guidance on corporate finance, tax strategy, or internal audit.
version: 1.2.0
last_updated: 2026-02
---

# Finance d'Entreprise — Corporate Financial Management

## Overview

Ce skill couvre l'ensemble des disciplines de la finance d'entreprise : comptabilite et reporting financier, controle de gestion, FP&A (Financial Planning & Analysis), tresorerie, fiscalite, audit interne, fundraising et analyse financiere. Il fournit un cadre de decision structure pour piloter la performance financiere, optimiser la structure de financement et soutenir la prise de decision strategique a tous les niveaux de l'organisation. La finance d'entreprise ne se limite pas a la production de chiffres : elle constitue le systeme nerveux qui relie strategie, operations et creation de valeur. Appliquer systematiquement les principes decrits ici pour garantir rigueur, transparence et anticipation dans chaque decision financiere.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Comptabilite et clotures** : passage d'ecritures, clotures mensuelles/trimestrielles/annuelles, consolidation groupe, rapprochements bancaires, production des etats financiers (bilan, compte de resultat, tableau de flux de tresorerie), normes PCG/IFRS.
- **Controle de gestion** : construction budgetaire, reforecast, analyse des ecarts (volume/prix/mix), calcul de couts (ABC, couts standards, couts marginaux), analyse de rentabilite par produit/client/canal.
- **FP&A et modelisation** : modeles financiers a 3 etats (P&L, bilan, cash flow), scenarios et sensibilites, rolling forecasts, reporting board/COMEX, benchmarking sectoriel.
- **Tresorerie et cash management** : previsions de tresorerie (13 semaines), financement du BFR (affacturage, Dailly), couverture de change, cash pooling, gestion de la dette.
- **Fiscalite** : optimisation IS/TVA, credits d'impot (CIR, CII), prix de transfert, integration fiscale groupe, structuration internationale.
- **Audit et controle interne** : referentiel COSO, planification d'audit, audits operationnels, matrices de segregation des taches (SoD), cartographie des risques.
- **Fundraising et relations investisseurs** : levees de fonds (seed a IPO), pitch decks financiers, modelisation pour investisseurs, gestion de la cap table, pactes d'actionnaires.
- **Analyse financiere et KPIs** : ratios financiers, unit economics (CAC, LTV, payback), metriques SaaS (MRR, ARR, NDR, churn), pilotage du BFR (DSO, DPO, DIO).

## Core Principles

### Principle 1 — Cash Is King, Profit Is an Opinion

Privilegier toujours l'analyse cash a l'analyse comptable. Le resultat net est sujet a des conventions comptables (amortissements, provisions, etalement) ; le cash flow est factuel. Construire systematiquement un tableau de flux de tresorerie (direct ou indirect) pour chaque decision majeure. Surveiller le free cash flow (FCF) comme indicateur ultime de creation de valeur. Un euro de profit qui ne se convertit pas en cash est un signal d'alerte.

### Principle 2 — Variance Analysis as a Management Discipline

Ne jamais presenter un chiffre sans son ecart par rapport au budget, au reforecast et a N-1. L'analyse des ecarts (volume, prix, mix, change, perimetre) est le langage du controle de gestion. Decomposer chaque ecart en composantes actionnables. Un ecart non explique est un ecart non manage.

### Principle 3 — Three Lines of Defense

Appliquer le modele des trois lignes de defense pour structurer la gouvernance financiere : (1) le management operationnel est responsable de ses risques, (2) les fonctions de controle (controlling, compliance, risk) supervisent et challengent, (3) l'audit interne fournit une assurance independante. Ce modele garantit que chaque risque financier est identifie, evalue et traite a un niveau appropriate.

### Principle 4 — Forward-Looking over Backward-Looking

Consacrer 70% du temps de la fonction finance a l'anticipation (previsions, scenarios, simulations) et 30% au reporting historique. Les organisations performantes utilisent des rolling forecasts plutot que des budgets annuels figes. Un bon FP&A transforme les donnees historiques en intelligence decisionnelle tournee vers l'avenir.

### Principle 5 — Materiality and Proportionality

Adapter le niveau de detail et de controle a l'enjeu financier. Ne pas appliquer le meme niveau de granulite a un poste representant 0.5% des charges et a un poste representant 30%. Definir des seuils de materialite clairs pour le reporting, l'audit et l'analyse. Concentrer les ressources de la fonction finance sur les postes a fort impact.

### Principle 6 — Single Source of Truth

Maintenir un referentiel financier unique et reconcilie. Interdire les "shadow spreadsheets" et les versions multiples de la verite. Le plan comptable, le referentiel analytique, le plan de comptes de gestion et les KPIs doivent etre definis une seule fois et partages par toutes les fonctions. Toute divergence entre comptabilite et controle de gestion est un dysfonctionnement a corriger immediatement.

## Key Frameworks & Methods

### Financial Statement Architecture

| Etat financier | Objet | Metriques cles | Frequence |
|---|---|---|---|
| **Compte de resultat (P&L)** | Performance economique sur la periode | CA, marge brute, EBITDA, EBIT, resultat net | Mensuel |
| **Bilan** | Patrimoine a une date donnee | Capitaux propres, dette nette, BFR, actif immobilise | Trimestriel/Annuel |
| **Tableau de flux de tresorerie** | Mouvements de cash sur la periode | FCF, flux d'exploitation, d'investissement, de financement | Mensuel |
| **Tableau de variation des capitaux propres** | Evolution des fonds propres | Capital, reserves, resultat, OCI | Annuel |

### Costing Methods Decision Matrix

| Methode | Principe | Forces | Limites | Cas d'usage |
|---|---|---|---|---|
| **Couts complets (absorption)** | Affecte tous les couts (directs + indirects) aux produits | Vision complete, conforme aux normes | Arbitraire dans la repartition des indirects | Reporting statutaire, pricing |
| **Couts variables (direct costing)** | Seuls les couts variables sont affectes aux produits | Aide a la decision court terme, marge sur couts variables | Ignore les couts fixes | Decisions make or buy, mix produit |
| **ABC (Activity-Based Costing)** | Affecte les couts via les activites consommatrices de ressources | Precision pour les couts indirects, identifie les activites non creatives de valeur | Complexe a maintenir, couteux | Entreprises multi-produits, services |
| **Couts standards** | Reference normative (standard) comparee au reel | Facilite l'analyse des ecarts, simplifie la gestion | Necessite une mise a jour reguliere des standards | Industrie, production en serie |

### Budget & Forecast Framework

```
1. Budget annuel (N+1)
   |-- Top-down : objectifs strategiques COMEX -> enveloppes par BU
   |-- Bottom-up : estimations operationnelles par centre de responsabilite
   |-- Iteration : reconciliation et arbitrage entre les deux approches
   |
2. Reforecast (3 a 4 par an)
   |-- Revision des hypotheses cles (volumes, pricing, couts)
   |-- Integration du reel cumule + prevision du restant a realiser
   |-- Focus sur les ecarts materiels (> seuil de materialite)
   |
3. Rolling Forecast (12 a 18 mois glissants)
   +-- Mise a jour mensuelle ou trimestrielle
   +-- Depasse l'exercice comptable pour une vision continue
   +-- Combine drivers operationnels et hypotheses macro
```

### Cash Management Framework

| Horizon | Objectif | Outil | Frequence de mise a jour |
|---|---|---|---|
| **Court terme (13 semaines)** | Anticiper les positions de tresorerie, eviter les impasses | Cash flow forecast detaille (encaissements/decaissements) | Hebdomadaire |
| **Moyen terme (3-12 mois)** | Planifier le financement du BFR et les investissements | Budget de tresorerie | Mensuel |
| **Long terme (1-5 ans)** | Structurer la dette, planifier les levees | Plan de financement | Trimestriel/Annuel |

### Fundraising Stage Framework

| Stage | Montant typique | Investisseurs | Metriques attendues | Valorisation indicative |
|---|---|---|---|---|
| **Pre-seed** | 100K-500K EUR | BA, incubateurs | Equipe, vision, prototype | 1-3M EUR |
| **Seed** | 500K-2M EUR | BA, micro-VC | MVP, premiers users, PMF signals | 3-8M EUR |
| **Serie A** | 2-10M EUR | VC early-stage | ARR 500K-2M, croissance >100%, unit economics en amelioration | 10-30M EUR |
| **Serie B** | 10-30M EUR | VC growth | ARR 5-15M, NDR >110%, LTV/CAC >3, path to profitability | 50-150M EUR |
| **Serie C+** | 30-100M+ EUR | Growth equity, PE | ARR >30M, EBITDA positive ou proche, expansion internationale | 200M+ EUR |
| **IPO** | Variable | Marche public | Rentabilite demontree, gouvernance, reporting IFRS | Multiples sectoriels |

## Decision Guide

### Arbre de decision pour le pilotage financier

```
1. Quel est l'enjeu financier ?
   |-- Pilotage de la performance operationnelle
   |   |-- Cloture et reporting -> Comptabilite & Reporting Financier
   |   |-- Analyse des ecarts et couts -> Controle de Gestion
   |   +-- Previsions et scenarios -> FP&A
   |
   |-- Gestion de la liquidite et du financement
   |   |-- Tresorerie court terme -> Cash Management (13 semaines)
   |   |-- Financement du BFR -> Treasury (affacturage, Dailly, lignes RCF)
   |   +-- Structure de capital -> Fundraising / Debt Management
   |
   |-- Conformite et gouvernance
   |   |-- Obligations fiscales -> Tax Strategy
   |   |-- Controle des processus -> Internal Audit / COSO
   |   +-- Reporting reglementaire -> Statutory Reporting
   |
   +-- Creation de valeur et communication
       |-- Analyse de rentabilite -> KPIs & Unit Economics
       |-- Communication investisseurs -> Investor Relations
       +-- Valorisation -> Financial Modeling

2. Quel referentiel comptable appliquer ?
   |-- Societe individuelle francaise -> PCG (Plan Comptable General)
   |-- Groupe cote en UE -> IFRS obligatoire
   |-- Groupe non cote francais -> PCG pour les comptes sociaux + IFRS ou CRC pour les comptes consolides
   +-- Filiale de groupe international -> IFRS ou US GAAP selon la maison mere

3. Quel niveau de detail pour l'analyse de couts ?
   |-- Industrie avec production standardisee -> Couts standards + analyse d'ecarts
   |-- Services avec couts indirects importants -> ABC (Activity-Based Costing)
   |-- Startup / PME avec peu de produits -> Direct costing + marge sur couts variables
   +-- Decision ponctuelle (make or buy, pricing) -> Couts marginaux / incrementaux
```

### Selection du mode de financement du BFR

| Instrument | Cout indicatif | Delai de mise en place | Impact bilan | Cas d'usage |
|---|---|---|---|---|
| **Affacturage (factoring)** | 0.5-2% du CA cede | 2-4 semaines | Deconsolidant (sans recours) | PME avec poste clients important |
| **Cession Dailly** | Euribor + 1-3% | 1-2 semaines | Pas de deconsolidation | Financement ponctuel de creances |
| **Ligne RCF (Revolving Credit Facility)** | Euribor + 1-4% + commitment fee | 4-8 semaines | Dette financiere | ETI/grands groupes, flexibilite |
| **Escompte commercial** | Taux d'escompte + commissions | Immediat | Pas de deconsolidation | Transactions ponctuelles |
| **Reverse factoring (supply chain finance)** | Negocie par l'acheteur | Variable | Hors bilan fournisseur | Grands donneurs d'ordre |

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Driver-Based Planning** : construire le budget et les previsions sur des drivers operationnels (nombre de clients, ARPU, taux de conversion, headcount) plutot que sur des lignes comptables. Cela rend les previsions plus intuitives, plus faciles a challenger et plus reactives aux changements d'hypotheses.
- **Monthly Business Review (MBR)** : instaurer une revue mensuelle de performance structuree : reel vs budget vs reforecast vs N-1, KPIs operationnels, actions correctives. Limiter a 10-15 slides. Chaque ecart materiel doit etre accompagne d'une explication et d'un plan d'action.
- **Waterfall Bridge** : presenter les ecarts sous forme de pont (bridge chart) decomposant la variation entre deux periodes en composantes (volume, prix, mix, change, perimetre, couts). C'est le format standard attendu par les COMEX et les investisseurs.
- **Scenario Planning (Base / Upside / Downside)** : produire systematiquement trois scenarios pour chaque prevision majeure. Le scenario base sert a la planification, les scenarios haut et bas servent a dimensionner les reserves et les plans de contingence.
- **Cash Conversion Cycle Monitoring** : suivre le cycle de conversion du cash (DSO + DIO - DPO) comme indicateur synthetique de l'efficacite du BFR. Fixer des objectifs par composante et mesurer mensuellement.

### Anti-patterns critiques

- **Budget-as-a-Target Syndrome** : traiter le budget comme un objectif intangible plutot que comme une reference de pilotage. Un budget depasse de 3% avec une croissance du CA de 20% au-dessus du plan n'est pas un probleme. Toujours analyser les ecarts en relatif et en contexte.
- **Spreadsheet Hell** : gerer la planification financiere, la consolidation ou le reporting sur des fichiers Excel non controles, non versionnes, avec des liens circulaires et des macros fragiles. Migrer vers des outils FP&A dedies (Pigment, Anaplan, Planful) des que la complexite le justifie.
- **Rear-View Mirror Finance** : consacrer 80% du temps de la DAF a cloturer les comptes et 20% a anticiper. Inverser le ratio. Automatiser les clotures, standardiser les ecritures recurrentes, et reallouer les ressources vers le FP&A et l'analyse decisionnelle.
- **Vanity Metrics** : presenter des metriques flatteuses mais non pertinentes (CA brut vs net, EBITDA ajuste avec trop de retraitements, nombre de clients sans distinction actifs/churnes). Toujours presenter les metriques les plus conservatives et les plus pertinentes pour la decision.
- **Siloed Finance** : cloisonner comptabilite, controle de gestion, tresorerie et fiscalite sans referentiel commun. Les ecarts entre la compta et le controlling, ou entre le budget de tresorerie et le P&L previsionnel, detruisent la credibilite de la DAF.

## Implementation Workflow

### Phase 1 — Diagnostic Financier / Financial Diagnostic
1. Auditer l'organisation de la DAF : effectifs, competences, outils, processus, delais de cloture.
2. Evaluer la maturite du reporting : frequence, fiabilite, granulite, delai de production.
3. Cartographier les flux financiers : encaissements, decaissements, intercompany, devises.
4. Identifier les quick wins : automatisation des ecritures recurrentes, reduction du delai de cloture, elimination des taches manuelles sans valeur ajoutee.

### Phase 2 — Structuration du Referentiel / Reference Framework
5. Definir le plan comptable et le referentiel analytique (centres de couts, axes d'analyse, drivers).
6. Construire le modele de P&L de gestion (management P&L) aligne avec le P&L statutaire.
7. Definir les KPIs par niveau de responsabilite (groupe, BU, equipe) avec les cibles et les seuils d'alerte.
8. Mettre en place le calendrier de cloture et le calendrier budgetaire.

### Phase 3 — Construction du Modele Financier / Financial Model Build
9. Construire le modele financier integre (P&L, bilan, cash flow) avec hypotheses explicites.
10. Implementer le budget et le processus de reforecast (top-down/bottom-up).
11. Developper les previsions de tresorerie (13 semaines + moyen terme).
12. Mettre en place les tableaux de bord operationnels (MBR, KPIs, bridges).

### Phase 4 — Optimisation et Pilotage Continu / Optimization & Ongoing Management
13. Automatiser les clotures (pre-closing checklists, ecritures recurrentes, reconciliations auto).
14. Deployer le rolling forecast et les scenarios (base/up/down).
15. Optimiser le BFR (negociation des delais fournisseurs, relance clients, gestion des stocks).
16. Structurer la veille fiscale et les opportunites d'optimisation (CIR, integration fiscale, prix de transfert).
17. Mettre en place la revue trimestrielle des risques financiers (change, taux, liquidite, credit).




## Modèle de maturité

### Niveau 1 — Comptable
- La fonction finance se limite à la production des états financiers et à la conformité légale
- Les clôtures sont longues (> 15 jours) et manuelles, avec de nombreuses corrections post-clôture
- Pas de contrôle de gestion formalisé ni de prévisions structurées
- **Indicateurs** : délai de clôture > 15 jours ouvrés, pas de forecast formalisé, cash conversion cycle non mesuré

### Niveau 2 — Structuré
- Le référentiel comptable et analytique est défini ; les clôtures sont mensuelles et documentées
- Un budget annuel est construit (top-down/bottom-up) avec au moins 2 reforecasts par an
- Le reporting mensuel inclut le P&L, les KPIs principaux et une analyse des écarts de base
- **Indicateurs** : délai de clôture 10-15 jours, précision forecast ± 15 %, cash conversion cycle mesuré

### Niveau 3 — Analytique
- L'analyse des écarts est systématique (volume, prix, mix, change) avec des bridges présentés au COMEX
- Les prévisions de trésorerie à 13 semaines sont maintenues et fiables
- Le contrôle de gestion produit des analyses de rentabilité par produit, client et canal
- **Indicateurs** : délai de clôture 5-10 jours, précision forecast ± 10 %, cash conversion cycle optimisé trimestriellement

### Niveau 4 — Stratégique
- Le rolling forecast (12-18 mois glissants) remplace le budget figé comme outil de pilotage principal
- Le FP&A est un business partner reconnu qui éclaire les décisions stratégiques avec des scénarios
- L'automatisation des écritures récurrentes et des réconciliations libère du temps pour l'analyse
- **Indicateurs** : délai de clôture < 5 jours, précision forecast ± 5 %, contribution active de la DAF aux décisions stratégiques

### Niveau 5 — Prédictif
- L'IA augmente le FP&A : détection d'anomalies, prévisions machine learning, scénarios automatisés
- La clôture tend vers le temps réel grâce à la réconciliation continue et l'automatisation complète
- La finance pilote la création de valeur avec des modèles prédictifs (churn, LTV, demand sensing)
- **Indicateurs** : clôture en continu (< 3 jours), précision forecast ± 3 %, cash conversion cycle best-in-class sectoriel

## Rythme opérationnel

| Cadence | Activité | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Hebdomadaire** | Revue de la position de trésorerie et prévisions à 13 semaines | Trésorier | Tableau de trésorerie hebdomadaire |
| **Hebdomadaire** | Suivi des encaissements et relance clients (DSO) | Credit Manager | Rapport d'âge des créances |
| **Mensuel** | Clôture comptable et production du reporting de gestion | DAF + Contrôleur de Gestion | P&L, bilan, bridge des écarts |
| **Mensuel** | Monthly Business Review (MBR) — présentation au COMEX | DAF | Pack MBR (10-15 slides + KPIs) |
| **Trimestriel** | Rolling forecast et mise à jour des scénarios (base/up/down) | FP&A Manager | Forecast 12-18 mois + analyse de sensibilité |
| **Trimestriel** | Revue des risques financiers (change, taux, liquidité, crédit) | DAF + Trésorier | Cartographie des risques financiers actualisée |
| **Annuel** | Construction budgétaire et plan de financement | DAF + DG | Budget N+1 + plan de financement 3 ans |

## State of the Art (2025-2026)

La fonction financière se transforme avec l'automatisation et les nouvelles métriques :

- **FP&A augmenté par l'IA** : Les outils de financial planning intègrent le machine learning pour des prévisions plus précises, la détection d'anomalies et des scénarios automatisés.
- **Real-time finance** : Les clôtures comptables tendent vers le temps réel grâce à l'automatisation des flux et la réconciliation continue.
- **Métriques SaaS avancées** : Au-delà du MRR/ARR, les investisseurs scrutent le Net Dollar Retention (NDR), le CAC payback, la Rule of 40 et le burn multiple.
- **Embedded finance** : L'intégration de services financiers (paiements, lending, assurance) directement dans les produits crée de nouveaux modèles de revenus.
- **Green finance et taxonomie** : Les obligations de reporting CSRD et la taxonomie européenne imposent de nouveaux cadres de reporting financier extra-financier.

## Template actionnable

### Unit Economics SaaS

| Métrique | Formule | Votre valeur | Benchmark |
|---|---|---|---|
| **MRR** | Σ abonnements mensuels | ___ € | - |
| **ARR** | MRR × 12 | ___ € | - |
| **CAC** | Coûts acquisition / nouveaux clients | ___ € | < LTV/3 |
| **LTV** | ARPU × durée vie moyenne | ___ € | > 3× CAC |
| **LTV/CAC** | LTV / CAC | ___ | > 3.0 |
| **Churn mensuel** | Clients perdus / clients début de mois | ___ % | < 2% |
| **Burn rate** | Dépenses mensuelles nettes | ___ € | - |
| **Runway** | Trésorerie / burn rate | ___ mois | > 18 mois |
| **Payback period** | CAC / ARPU mensuel | ___ mois | < 12 mois |

## Prompts types

- "Construis un modèle financier pour ma startup sur 3 ans"
- "Comment calculer et optimiser notre unit economics (LTV/CAC) ?"
- "Aide-moi à préparer un budget prévisionnel annuel"
- "Quels KPIs financiers suivre pour un SaaS en croissance ?"
- "Comment structurer un pitch deck financier pour une levée de fonds ?"
- "Analyse mon P&L et identifie les leviers d'optimisation"

## Skills connexes

| Skill | Lien |
|---|---|
| Stratégie | `entreprise:strategie` — Alignement financier avec la vision stratégique |
| Commercial | `entreprise:commercial` — Prévision de revenus et forecast |
| Risk Management | `entreprise:risk-management` — Gestion des risques financiers |
| Payment Stripe | `code-development:payment-stripe` — Implémentation de la monétisation |
| Decision Reporting | `data-bi:decision-reporting-governance` — KPIs et tableaux de bord financiers |

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[Accounting & Controlling](./references/accounting-controlling.md)** : normes comptables (PCG, IFRS), consolidation, clotures mensuelles/annuelles, analyse des ecarts, methodes de calcul de couts (ABC, couts standards, direct costing), controle de gestion operationnel.
- **[FP&A & Financial Modeling](./references/fpa-modeling.md)** : FP&A, modeles financiers a 3 etats, analyse de scenarios, rolling forecasts, reporting COMEX/board, benchmarking, driver-based planning.
- **[Treasury & Tax](./references/treasury-tax.md)** : cash management, previsions de tresorerie 13 semaines, financement du BFR (affacturage, Dailly), couverture de change, cash pooling, optimisation fiscale (IS, TVA, CIR), prix de transfert.
- **[Fundraising & KPIs](./references/fundraising-kpis.md)** : processus de levee de fonds (seed a IPO), relations investisseurs, unit economics (CAC, LTV, payback), metriques SaaS (MRR, ARR, NDR, churn), analyse financiere et ratios cles.

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.