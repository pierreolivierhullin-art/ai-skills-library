---
name: operations
description: This skill should be used when the user asks about "operational excellence", "supply chain management", "lean management", "Six Sigma", "quality management", discusses process optimization, SLA management, or needs guidance on logistics, inventory, or continuous improvement.
version: 1.0.0
---

# Operations / Delivery — Excellence Operationnelle

## Overview

Ce skill couvre l'ensemble des disciplines liees a l'excellence operationnelle et au delivery. Il fournit un cadre structure pour concevoir, optimiser et piloter les operations d'une organisation, de la gestion des processus a la supply chain, en passant par la qualite, la gestion de services et l'environnement de travail. L'excellence operationnelle ne se resume pas a la reduction des couts : elle englobe la creation de valeur durable par l'amelioration continue des processus, la maitrise de la qualite, la resilience de la chaine d'approvisionnement et la satisfaction des parties prenantes. Appliquer systematiquement les principes decrits ici pour guider chaque decision operationnelle, en privilegiant la rigueur, la mesure et l'amelioration continue.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Conception ou optimisation de processus** : design de workflows, analyse de flux de valeur (VSM), identification des gaspillages, mise en place du Lean Management ou du Six Sigma.
- **Gestion de la supply chain** : demand planning, gestion des stocks (EOQ, safety stock, ABC/XYZ), logistique (3PL, last mile, reverse logistics), procurement, S&OP.
- **Management de la qualite** : mise en place d'un QMS (ISO 9001), Total Quality Management (TQM), analyse de causes racines (Ishikawa, 5 Whys, 8D), maitrise statistique des procedes (SPC).
- **Gestion des services et SLA** : design de SLA/SLO/SLI, gestion des incidents, capacity management, Continual Service Improvement (CSI).
- **Workplace et facilities management** : conception des espaces de travail, HSE (Hygiene Securite Environnement), gestion du workplace hybride, durabilite dans les operations.
- **Transformation operationnelle** : programmes d'excellence operationnelle, deploiement de la Theory of Constraints (ToC), Kaizen events, pilotage par les KPI operationnels.

## Core Principles

### Principle 1 — Measure Before You Improve
Ne jamais lancer une initiative d'amelioration sans avoir d'abord etabli une baseline quantifiee. Definir des indicateurs mesurables pour chaque processus (lead time, taux de defauts, OEE, taux de service). Utiliser ces metriques pour prioriser les actions et valider objectivement chaque amelioration. Sans mesure, il n'y a pas d'amelioration — il n'y a que du changement.

### Principle 2 — Flow over Utilization
Privilegier la fluidite du flux (flow efficiency) plutot que l'optimisation du taux d'utilisation des ressources. Un systeme a 100% d'utilisation genere des files d'attente exponentielles (loi de Little, theorie des files d'attente). Identifier et eliminer les goulots d'etranglement selon la Theory of Constraints avant de chercher a occuper chaque ressource.

### Principle 3 — Respect for People
L'excellence operationnelle repose sur l'engagement des equipes. Appliquer le principe Lean du "respect des personnes" : impliquer les operateurs dans l'identification des problemes (Gemba walk), valoriser les suggestions d'amelioration (Kaizen), et investir dans la formation continue. Les meilleurs processus sont ceux concus et ameliores par ceux qui les executent.

### Principle 4 — Built-In Quality
Integrer la qualite a chaque etape du processus plutot que de compter sur l'inspection finale. Appliquer le concept Jidoka (autonomation) : arreter le processus des qu'un defaut est detecte. Concevoir des systemes Poka-Yoke (anti-erreur) pour prevenir les defauts a la source.

### Principle 5 — End-to-End Visibility
Maintenir une visibilite de bout en bout sur la chaine de valeur. Utiliser des control towers, des dashboards temps reel et des systemes d'alerte pour detecter les anomalies avant qu'elles ne deviennent des crises. La visibilite est le prerequis de l'agilite operationnelle.

### Principle 6 — Resilience over Efficiency
Concevoir les operations pour la resilience, pas uniquement pour l'efficience maximale. Un systeme trop optimise est fragile. Integrer des buffers strategiques (safety stock, capacite excedentaire, sources alternatives) pour absorber les chocs. L'objectif est une chaine de valeur anti-fragile.

## Key Frameworks & Methods

### Lean Management Toolbox

| Outil | Usage principal | Quand l'utiliser |
|---|---|---|
| **Value Stream Mapping (VSM)** | Cartographier le flux de valeur end-to-end | Diagnostic initial, identification des gaspillages |
| **5S** | Organisation du poste de travail | Fondation de toute demarche Lean |
| **Kaizen** | Amelioration continue par petits pas | En permanence, via des events de 3-5 jours |
| **Kanban** | Gestion visuelle du flux de travail | Pilotage du WIP, reduction du lead time |
| **Gemba Walk** | Observation sur le terrain | Quotidien pour les managers, hebdomadaire pour les dirigeants |
| **A3 Thinking** | Resolution de problemes structuree | Problemes complexes necessitant une analyse approfondie |
| **Heijunka** | Lissage de la production | Quand la variabilite de la demande impacte le flux |

### Six Sigma Methodology

| Phase DMAIC | Objectif | Outils cles |
|---|---|---|
| **Define** | Definir le probleme et le scope | Project Charter, SIPOC, Voice of Customer |
| **Measure** | Quantifier la performance actuelle | Gage R&R, Capability analysis (Cp, Cpk), Data collection plan |
| **Analyze** | Identifier les causes racines | Ishikawa, 5 Whys, Regression, Hypothesis testing |
| **Improve** | Mettre en oeuvre les solutions | DOE, Piloting, Poka-Yoke, FMEA |
| **Control** | Perenniser les gains | SPC charts, Control plans, Standard work |

### Supply Chain Planning Matrix

| Horizon | Processus | Frequence | Outils |
|---|---|---|---|
| **Strategique (1-5 ans)** | Network design, sourcing strategy | Annuel | Optimization models, scenario planning |
| **Tactique (3-18 mois)** | S&OP, capacity planning | Mensuel | Demand sensing, ATP/CTP |
| **Operationnel (0-3 mois)** | MRP, scheduling, replenishment | Quotidien/Hebdo | APS, WMS, TMS |
| **Execution (temps reel)** | Order management, dispatching | Temps reel | OMS, control tower, IoT |

## Decision Guide

### Arbre de decision pour le choix de la methodologie d'amelioration

```
1. Quel est le type de probleme ?
   +-- Gaspillages et flux (lead time, WIP, surstocks) --> Lean (VSM, Kaizen)
   +-- Variabilite et defauts (taux de rebut, erreurs) --> Six Sigma (DMAIC)
   +-- Goulot d'etranglement unique --> Theory of Constraints (5 Focusing Steps)
   +-- Combinaison des trois --> Lean Six Sigma + ToC

2. Quel est le niveau de maturite de l'organisation ?
   +-- Debutant --> 5S + Gemba + Kanban basique
   +-- Intermediaire --> VSM + Kaizen events + DMAIC
   +-- Avance --> Lean Six Sigma integre + Design for Six Sigma (DMADV)

3. Quel est l'horizon temporel ?
   +-- Quick wins (< 1 mois) --> Kaizen blitz, 5S, Poka-Yoke
   +-- Moyen terme (1-6 mois) --> Projet DMAIC, programme Lean
   +-- Long terme (> 6 mois) --> Transformation culturelle, deploiement Hoshin Kanri
```

### Criteres de choix pour la strategie de stock

| Critere | Make-to-Stock (MTS) | Make-to-Order (MTO) | Assemble-to-Order (ATO) |
|---|---|---|---|
| Variabilite de la demande | Faible | Elevee | Moyenne |
| Personnalisation | Aucune | Totale | Modulaire |
| Lead time client | Court (immediat) | Long | Moyen |
| Risque d'obsolescence | Eleve | Faible | Moyen |
| Investissement stock | Eleve | Faible | Moyen |

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Daily Management System (DMS)** : structurer la gestion quotidienne avec des reunions courtes (tier meetings), des tableaux de management visuel et une escalade structuree. Ne jamais piloter les operations uniquement par des rapports mensuels — le terrain doit etre visible quotidiennement.
- **Demand-Driven MRP (DDMRP)** : positionner des buffers strategiques de decouplage dans la supply chain pour absorber la variabilite. Remplacer les previsions detaillees par des signaux de demande reelle quand c'est possible.
- **Control Tower** : centraliser la visibilite sur la supply chain end-to-end avec des alertes temps reel, des KPI dynamiques et des capacites de scenario planning. Indispensable a partir d'une complexite supply chain moyenne.
- **Gemba-based Problem Solving** : resoudre les problemes la ou ils se produisent (le Gemba), avec les personnes qui les vivent. Ne jamais concevoir des solutions depuis une salle de reunion sans avoir observe le terrain.
- **Standard Work** : documenter la meilleure methode connue pour chaque tache critique. Le standard work n'est pas une contrainte rigide — c'est la base a partir de laquelle l'amelioration est possible.

### Anti-patterns critiques

- **Tool-before-Problem** : deployer un outil (5S, Six Sigma, ERP) sans avoir clairement defini le probleme a resoudre. Le choix de la methode doit suivre le diagnostic, pas le preceder.
- **Island of Excellence** : optimiser un processus localement sans considerer l'impact sur le flux global. Un gain de productivite sur un poste non-goulot n'ameliore rien — il genere du stock intermediaire.
- **KPI Theater** : afficher des KPI sur des ecrans sans que personne ne reagisse quand ils passent au rouge. Chaque KPI doit avoir un proprietaire, des seuils d'action et un processus d'escalade defini.
- **Forecast-Dependent Supply Chain** : batir une supply chain entierement dependante de la precision des previsions. Combiner forecasting et demand sensing avec des strategies de bufferisation pour absorber l'erreur inevitable.
- **Quality by Inspection** : compter sur le controle qualite en fin de ligne pour detecter les defauts. L'inspection ne cree pas la qualite — elle ne fait que trier. Integrer la qualite dans chaque etape du processus.

## Implementation Workflow

### Phase 1 — Diagnostic & Baseline
1. Realiser un Gemba walk pour observer les operations telles qu'elles sont reellement (pas telles qu'elles sont decrites dans les procedures).
2. Cartographier la chaine de valeur (VSM current state) pour identifier les gaspillages, les goulots et les points de rupture.
3. Etablir la baseline quantifiee : lead time, takt time, OEE, taux de service, couts de non-qualite, niveaux de stock.
4. Identifier la contrainte principale du systeme (Theory of Constraints — Step 1).
5. Prioriser les chantiers d'amelioration selon l'impact metier et la faisabilite.

### Phase 2 — Design & Quick Wins
6. Designer le flux cible (VSM future state) en eliminant les gaspillages identifies.
7. Lancer les quick wins (5S, Poka-Yoke, reorganisation de layout) pour creer de la dynamique.
8. Definir le systeme de management visuel (Daily Management System).
9. Former les equipes aux outils et methodes retenus.
10. Mettre en place les SLA/SLO internes et externes.

### Phase 3 — Deploiement & Amelioration
11. Deployer les ameliorations par vagues (pilote puis generalisation).
12. Lancer les chantiers DMAIC pour les problemes de variabilite.
13. Mettre en oeuvre la planification S&OP si applicable.
14. Deployer les outils de visibilite (control tower, dashboards operationnels).
15. Etablir les routines Kaizen (events reguliers, suggestion system).

### Phase 4 — Perennisation & Culture
16. Ancrer les gains dans le standard work documente.
17. Mettre en place les cartes de controle SPC sur les processus cles.
18. Deployer le Hoshin Kanri pour aligner les objectifs operationnels sur la strategie.
19. Former les Green Belts et Black Belts internes pour autonomiser l'amelioration continue.
20. Evaluer la maturite operationnelle annuellement et ajuster la feuille de route.

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[Lean & Six Sigma](./references/lean-six-sigma.md)** : fondamentaux du Lean Management, methodologie Six Sigma (DMAIC, DMADV), outils (5S, Kaizen, VSM, A3), Theory of Constraints, Lean Six Sigma integre, tendances 2024-2026 (Lean 4.0, AI-augmented continuous improvement).
- **[Supply Chain Management](./references/supply-chain.md)** : demand planning, gestion des stocks (EOQ, safety stock, ABC/XYZ), logistique (3PL, last mile, reverse logistics), procurement et sourcing strategique, S&OP, supply chain visibility et resilience, tendances 2024-2026 (digital supply chain twin, autonomous logistics).
- **[Quality Management](./references/quality-management.md)** : systemes de management de la qualite (ISO 9001:2015), TQM, amelioration continue (PDCA, A3, 8D), analyse de causes racines (Ishikawa, 5 Whys, Pareto), maitrise statistique des procedes (SPC), tendances 2024-2026 (Quality 4.0, predictive quality, AI-driven inspection).
- **[Service Delivery & Workplace](./references/service-delivery.md)** : design de SLA/SLO/SLI, gestion des incidents, capacity et availability management, Continual Service Improvement (CSI), facilities management, HSE, workplace hybride, tendances 2024-2026 (ITIL 4, XLA, smart buildings).
