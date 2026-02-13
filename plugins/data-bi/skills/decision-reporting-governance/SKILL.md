---
name: decision-reporting-governance
description: This skill should be used when the user asks about "business intelligence", "BI dashboards", "data governance", "data quality", "data modeling", "KPI frameworks", "data catalog", "master data management", "data lineage", "Power BI", "Tableau", "Looker", "Metabase", "data contracts", "intelligence d'affaires", "tableaux de bord BI", "gouvernance des données", "qualité des données", "modélisation des données", "cadres KPI", "catalogue de données", "gestion des données de référence", "MDM", "lignage des données", "traçabilité des données", "data mesh", "data fabric", "data steward", "data owner", "DAMA", "DMBOK", "dimensional modeling", "star schema", "modèle en étoile", "data dictionary", "dictionnaire de données", "reporting automatisé", "automated reporting", "self-service BI", "BI en libre-service", "data observability", "semantic layer", "couche sémantique", or needs guidance on BI reporting, data governance, and data quality management.
version: 1.2.0
last_updated: 2026-02
---

# Decision Reporting & Governance — BI, Data Quality & Modeling

## Overview

Ce skill couvre l'ensemble des disciplines liées au reporting decisionnel, a la gouvernance des donnees et a la modelisation. Il fournit un cadre structure pour concevoir des tableaux de bord performants, etablir une gouvernance des donnees robuste, garantir la qualite des donnees et modeliser des entrepots de donnees selon les methodologies de reference. Appliquer systematiquement les principes decrits ici pour guider chaque decision relative au BI, a la data governance et au data modeling, en privilegiant la rigueur methodologique, la lisibilite metier et la conformite reglementaire.

This skill covers the full spectrum of decision reporting, data governance, and data modeling disciplines. It provides a structured framework for designing performant dashboards, establishing robust data governance, ensuring data quality, and modeling data warehouses using industry-standard methodologies. Systematically apply the principles described here to guide every decision related to BI, data governance, and data modeling, prioritizing methodological rigor, business readability, and regulatory compliance.

## When This Skill Applies

Activer ce skill dans les situations suivantes / Activate this skill in the following situations:

- **Conception de dashboards et rapports** : choix d'outil BI (Power BI, Tableau, Looker, Metabase, Superset), design de tableaux de bord, KPI frameworks, metric trees, self-service BI.
- **Gouvernance des donnees** : mise en place d'un programme de data governance (DAMA-DMBOK), catalogage (Atlan, DataHub, OpenMetadata), data lineage, data ownership, data stewardship, data contracts.
- **Qualite des donnees** : definition de regles de qualite, implementation de tests (Great Expectations, Soda, dbt tests), monitoring de la qualite, data observability, master data management (MDM).
- **Modelisation des donnees** : dimensional modeling (Kimball star/snowflake), Data Vault 2.0, Slowly Changing Dimensions (SCD), conceptual/logical/physical models, One Big Table (OBT) pattern.
- **Analytics avancee** : descriptive, diagnostic, predictive, prescriptive analytics, statistical analysis, data storytelling.
- **Privacy et conformite** : RGPD/GDPR data mapping, data classification, anonymization, pseudonymization, retention policies.

## Core Principles

### Principle 1 — Business-First Design

Concevoir chaque dashboard, modele de donnees et regle de qualite en partant du besoin metier, jamais de la donnee brute. Poser la question "Quelle decision ce livrable permet-il de prendre ?" avant tout travail technique. Aligner chaque KPI sur un objectif strategique mesurable.

Design every dashboard, data model, and quality rule starting from the business need, never from raw data. Ask "What decision does this deliverable enable?" before any technical work. Align every KPI to a measurable strategic objective.

### Principle 2 — Single Source of Truth (SSOT)

Etablir une source de verite unique pour chaque metrique, dimension et entite metier. Eliminer les definitions contradictoires en formalisant un business glossary centralise. Implementer une semantic layer (dbt metrics, Looker LookML, Cube.js) pour garantir la coherence des calculs.

Establish a single source of truth for every metric, dimension, and business entity. Eliminate contradictory definitions by formalizing a centralized business glossary. Implement a semantic layer (dbt metrics, Looker LookML, Cube.js) to ensure calculation consistency.

### Principle 3 — Data Quality as a First-Class Citizen

Traiter la qualite des donnees comme une contrainte non negociable, pas comme un correctif post-hoc. Integrer les tests de qualite dans les pipelines de transformation (dbt tests, Great Expectations, Soda). Mesurer la qualite sur les 6 dimensions DAMA : completude, unicite, validite, coherence, exactitude, actualite.

Treat data quality as a non-negotiable constraint, not as a post-hoc fix. Integrate quality tests into transformation pipelines (dbt tests, Great Expectations, Soda). Measure quality across the 6 DAMA dimensions: completeness, uniqueness, validity, consistency, accuracy, timeliness.

### Principle 4 — Governed Self-Service

Permettre l'autonomie des utilisateurs metier tout en maintenant la gouvernance. Fournir un cadre self-service BI avec des datasets certifies, des metriques standardisees et des garde-fous (row-level security, masking). L'objectif est de democratiser l'acces aux donnees sans sacrifier la fiabilite ni la conformite.

Enable business user autonomy while maintaining governance. Provide a self-service BI framework with certified datasets, standardized metrics, and guardrails (row-level security, masking). The goal is to democratize data access without sacrificing reliability or compliance.

### Principle 5 — Privacy by Design

Integrer la protection des donnees personnelles des la conception (RGPD article 25). Classifier les donnees, appliquer les techniques d'anonymisation/pseudonymisation, definir des politiques de retention et documenter les traitements dans un registre. Ne jamais stocker de donnees personnelles sans finalite explicite et base legale.

Integrate personal data protection from the design stage (GDPR article 25). Classify data, apply anonymization/pseudonymization techniques, define retention policies, and document processing in a register. Never store personal data without an explicit purpose and legal basis.

### Principle 6 — Iterative Modeling

Privilegier une approche iterative de la modelisation : commencer par un modele conceptuel aligne sur le metier, raffiner en modele logique, puis implementer le modele physique. Ne jamais sauter directement au modele physique. Valider chaque couche avec les parties prenantes metier et techniques.

Favor an iterative modeling approach: start with a conceptual model aligned with the business, refine into a logical model, then implement the physical model. Never skip directly to the physical model. Validate each layer with business and technical stakeholders.

## Key Frameworks & Methods

### BI Tool Selection Matrix

| Critere / Criteria | Power BI | Tableau | Looker | Metabase | Superset |
|---|---|---|---|---|---|
| **Cas d'usage principal** | Enterprise BI, Microsoft ecosystem | Advanced visualization, exploration | Governed metrics, LookML semantic layer | Quick self-service, open source | Technical users, open source |
| **Semantic layer** | DAX measures | Calculated fields | LookML (natif) | Questions/Models | SQL-based metrics |
| **Embedded analytics** | Power BI Embedded | Tableau Embedded | Looker Embedded | iframe / API | iframe / API |
| **Cout / Cost** | $$$ (Pro/Premium) | $$$$ | $$$$ (Google Cloud) | Free / $$ (Cloud) | Free (OSS) |
| **Courbe d'apprentissage** | Moyenne | Moyenne-Elevee | Elevee (LookML) | Faible | Moyenne |
| **Gouvernance** | Forte (workspaces, RLS) | Moyenne | Tres forte (modele centralise) | Basique | Basique-Moyenne |

### Data Governance Maturity Model (DAMA-DMBOK)

Evaluer la maturite de la gouvernance sur les 11 domaines DAMA-DMBOK :

1. **Data Governance** : strategy, organization, policies, stewardship
2. **Data Architecture** : models, integration, data flows
3. **Data Modeling & Design** : conceptual, logical, physical models
4. **Data Storage & Operations** : database management, data ops
5. **Data Security** : access control, encryption, masking
6. **Data Integration & Interoperability** : ETL/ELT, APIs, MDM
7. **Documents & Content** : unstructured data management
8. **Reference & Master Data** : MDM, reference data management
9. **Data Warehousing & BI** : reporting, analytics, dashboards
10. **Metadata Management** : technical, business, operational metadata
11. **Data Quality** : profiling, monitoring, remediation

### Data Quality Dimensions (6 Dimensions DAMA)

| Dimension | Definition | Exemple de test |
|---|---|---|
| **Completude / Completeness** | Pas de valeurs manquantes inattendues | `NOT NULL` checks, % de remplissage |
| **Unicite / Uniqueness** | Pas de doublons | Tests de cle primaire, deduplication |
| **Validite / Validity** | Conforme au format et aux regles metier | Regex, domaines de valeurs, ranges |
| **Coherence / Consistency** | Concordance entre sources et systemes | Cross-source reconciliation |
| **Exactitude / Accuracy** | Conformite a la realite du monde reel | Comparaison avec source autorisee |
| **Actualite / Timeliness** | Fraicheur acceptable pour l'usage | SLA de rafraichissement, freshness checks |

### Dimensional Modeling Decision Guide

```
1. Quel est le grain du fait ? (What is the fact grain?)
   --> Definir le grain le plus atomique possible

2. Quelles sont les dimensions ?
   --> Identifier toutes les dimensions d'analyse (who, what, where, when, why, how)

3. Quels sont les faits mesurables ?
   --> Additive, semi-additive, non-additive measures

4. Quel schema adopter ?
   +-- Besoins de performance en lecture, simplicite --> Star schema (Kimball)
   +-- Besoins de normalisation des dimensions --> Snowflake schema
   +-- Historique complexe, sources multiples, audit --> Data Vault 2.0
   +-- Cas simple, petites equipes, BI moderne --> One Big Table (OBT)

5. Comment gerer l'historique des dimensions ?
   +-- Pas d'historique requis --> SCD Type 1 (overwrite)
   +-- Historique complet requis --> SCD Type 2 (new row, valid_from/valid_to)
   +-- Historique sur quelques attributs --> SCD Type 3 (previous value column)
   +-- Historique rapide (snapshot) --> SCD Type 6 (hybrid 1+2+3)
```

## Decision Guide

### Arbre de decision reporting / Reporting Decision Tree

```
1. Qui est le consommateur principal ?
   +-- Executives / C-level --> Executive dashboard (5-7 KPIs max, metric trees)
   +-- Data analysts --> Self-service BI + SQL access (Looker, Metabase)
   +-- Operational teams --> Operational dashboards (real-time, alerting)
   +-- External stakeholders --> Embedded analytics, PDF exports

2. Quel type d'analytics est requis ?
   +-- Descriptive (Que s'est-il passe ?) --> Dashboards, standard reports
   +-- Diagnostic (Pourquoi ?) --> Drill-down, ad-hoc analysis, filtering
   +-- Predictive (Que va-t-il se passer ?) --> ML models, forecasting, statistical
   +-- Prescriptive (Que faire ?) --> Optimization, recommendations, simulations

3. Quelle gouvernance est requise ?
   +-- Forte (reglemente, multi-equipes) --> Looker, Power BI Premium + data catalog
   +-- Moyenne (equipes data matures) --> dbt + Tableau/Power BI + data contracts
   +-- Legere (startup, petite equipe) --> Metabase/Superset + dbt tests
```

### Arbre de decision data governance / Data Governance Decision Tree

```
1. Quelle est la maturite actuelle (DAMA maturity assessment) ?
   +-- Level 1 (Initial) --> Focus on data catalog + business glossary first
   +-- Level 2 (Repeatable) --> Add data quality monitoring + ownership
   +-- Level 3 (Defined) --> Implement data contracts + lineage
   +-- Level 4 (Managed) --> Automate governance + compliance monitoring
   +-- Level 5 (Optimized) --> AI-driven governance + continuous improvement

2. Quel est le driver principal ?
   +-- Conformite reglementaire (RGPD, SOX) --> Data classification + DPO + DPIA
   +-- Qualite des donnees --> Quality rules + monitoring + SLAs
   +-- Self-service analytics --> Data catalog + certified datasets + semantic layer
   +-- Integration / MDM --> Golden records + match/merge + data stewardship
```

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Metric Tree / KPI Decomposition** : decomposer chaque KPI strategique en un arbre de sous-metriques actionnables. Le chiffre d'affaires se decompose en nombre de clients x panier moyen x frequence d'achat. Chaque feuille doit etre directement actionnable par une equipe.
- **Certified Datasets** : creer des datasets certifies et versionnes dans la semantic layer. Les utilisateurs self-service travaillent exclusivement sur des datasets certifies, jamais sur les tables brutes.
- **Data Contracts** : formaliser les contrats de donnees entre producteurs et consommateurs (schema, SLAs de qualite, freshness, ownership). Utiliser des outils comme Soda, DataHub contracts, ou des fichiers YAML versionnes.
- **Data Mesh Governance** : appliquer une gouvernance federee ou chaque domaine est responsable de ses data products, avec des standards globaux (interoperabilite, qualite minimale, discoverability).
- **Layered Modeling (medallion)** : organiser les modeles en couches Bronze (raw), Silver (cleaned/conformed), Gold (business-ready). Chaque couche a des regles de qualite specifiques.

### Anti-patterns critiques

- **Dashboard Sprawl** : proliferation non gouvernee de dashboards sans ownership ni maintenance. Resultat : metriques contradictoires, confusion metier. Auditer et retirer les dashboards non utilises tous les trimestres.
- **Vanity Metrics** : KPIs qui flattent mais ne declenchent pas d'action (pages vues sans conversion, nombre de telechargements sans retention). Exiger qu'un KPI soit lie a une action et a un objectif.
- **Schema-on-Read sans gouvernance** : stocker toutes les donnees dans un data lake sans schema ni catalogue. Resultat : data swamp inutilisable. Toujours cataloguer et profiler les donnees a l'ingestion.
- **Copy-Paste SQL** : repliquer les memes transformations dans des dizaines de dashboards. Centraliser la logique dans la semantic layer ou les modeles dbt.
- **RGPD Afterthought** : traiter la conformite RGPD comme un projet ponctuel. Integrer la classification, le consentement et la retention dans les pipelines de donnees de maniere continue.

## Implementation Workflow

### Phase 1 — Discovery & Assessment

1. Cartographier les sources de donnees existantes et evaluer leur qualite via un data profiling (row count, null %, distribution, outliers).
2. Identifier les parties prenantes metier, leurs besoins decisionnels et les KPIs prioritaires.
3. Evaluer la maturite de la gouvernance avec un assessment DAMA-DMBOK (11 domaines, niveaux 1-5).
4. Inventorier les outils existants (BI, ETL, bases, catalogue) et identifier les gaps.
5. Classifier les donnees sensibles (PII, PHI, financial) et cartographier les traitements RGPD.

### Phase 2 — Foundation & Governance Setup

6. Deployer un data catalog (DataHub, Atlan, OpenMetadata) et initialiser le business glossary avec les definitions metier validees.
7. Definir les roles : Data Owner (decideur metier), Data Steward (gardien qualite), Data Engineer (implementation), Analytics Engineer (modelisation).
8. Formaliser les data contracts entre producteurs et consommateurs (schema, freshness SLA, quality SLA).
9. Implementer les regles de qualite fondamentales dans les pipelines (dbt tests, Great Expectations, Soda checks).
10. Definir les politiques de classification, retention et anonymisation conformes au RGPD.

### Phase 3 — Modeling & BI Development

11. Concevoir le modele conceptuel avec les parties prenantes metier (entites, relations, definitions).
12. Traduire en modele logique : star schema / snowflake (Kimball) ou Data Vault 2.0 selon le contexte.
13. Implementer le modele physique avec dbt (staging, intermediate, mart layers) et appliquer les conventions de nommage.
14. Construire la semantic layer (dbt metrics, LookML, DAX measures) pour garantir la coherence des calculs.
15. Concevoir les dashboards selon les principes de data visualization : hierarchie visuelle, 5-7 KPIs max par vue, storytelling oriente decision.

### Phase 4 — Operationalization & Continuous Improvement

16. Deployer les dashboards avec row-level security, refresh schedules et alerting.
17. Mettre en place le data quality monitoring continu (Soda, Elementary, Monte Carlo) avec alertes automatiques.
18. Former les utilisateurs metier au self-service BI avec les datasets certifies.
19. Planifier les revues trimestrielles : audit des dashboards (usage analytics), revue des data contracts, mise a jour du catalogue et du glossary.
20. Mesurer et rapporter les KPIs de la gouvernance elle-meme : data quality score, catalogue coverage, SLA compliance, time-to-insight.


## Rythme opérationnel

| Cadence | Activité | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Hebdomadaire** | Revue du score de qualité des données | Data Steward | Dashboard qualité et alertes critiques |
| **Hebdomadaire** | Monitoring de l'usage des dashboards | Data Analyst | Rapport d'adoption et anomalies d'usage |
| **Mensuel** | Comité de data stewardship | Data Governance Lead | Compte-rendu et plan d'actions |
| **Mensuel** | Revue des KPIs et mise à jour du catalogue | Data Steward + Métier | Catalogue KPI actualisé |
| **Trimestriel** | Évaluation de maturité de la gouvernance data | Data Governance Lead | Scorecard de maturité et axes de progrès |
| **Trimestriel** | Audit du data lineage et du catalogue | Data Steward | Rapport d'audit et actions de remédiation |
| **Annuel** | Actualisation de la stratégie et des politiques data | CDO / Head of Data | Charte data governance et roadmap annuelle |

## State of the Art (2025-2026)

La BI et la gouvernance des données se transforment :

- **Semantic layer universel** : Les couches sémantiques (dbt Semantic Layer, Cube, AtScale) unifient les définitions de métriques entre les outils BI, éliminant les incohérences.
- **Data mesh opérationnel** : L'architecture data mesh (domain ownership, data as a product, self-serve platform) passe de la théorie à l'implémentation dans les grandes organisations.
- **AI-augmented BI** : Les outils BI intègrent des LLM pour le querying en langage naturel, la génération automatique d'insights et les alertes intelligentes.
- **Data contracts** : Les contrats de données formalisent les engagements entre producteurs et consommateurs, améliorant la fiabilité et la qualité.
- **Data observability** : Les outils de monitoring de la qualité des données (Monte Carlo, Elementary, Soda) détectent les anomalies avant qu'elles n'impactent les dashboards.

## Template actionnable

### Framework de KPIs par niveau

| Niveau | KPI | Formule | Source | Fréquence | Owner |
|---|---|---|---|---|---|
| **Stratégique** | ___ | ___ | ___ | Mensuel | C-Level |
| **Stratégique** | ___ | ___ | ___ | Mensuel | C-Level |
| **Tactique** | ___ | ___ | ___ | Hebdomadaire | Manager |
| **Tactique** | ___ | ___ | ___ | Hebdomadaire | Manager |
| **Opérationnel** | ___ | ___ | ___ | Quotidien | Équipe |
| **Opérationnel** | ___ | ___ | ___ | Quotidien | Équipe |

> Règle : max 5 KPIs stratégiques, 10 tactiques, 15 opérationnels.

## Prompts types

- "Comment mettre en place une gouvernance des données dans notre organisation ?"
- "Aide-moi à concevoir un dashboard BI pour le comité de direction"
- "Propose un framework de KPIs pour piloter notre activité"
- "Comment choisir entre Power BI, Tableau et Looker ?"
- "Aide-moi à créer un data catalog pour notre entreprise"
- "Comment définir des data contracts entre équipes ?"

## Skills connexes

| Skill | Lien |
|---|---|
| Data Engineering | `data-bi:data-engineering` — Pipelines et infrastructure de données |
| Data Literacy | `data-bi:data-literacy` — Visualisation et storytelling des données |
| Finance | `entreprise:finance` — KPIs financiers et tableaux de bord |
| Stratégie | `entreprise:strategie` — Aide à la décision stratégique |
| Product Analytics | `code-development:product-analytics` — Métriques produit et instrumentation |

## Glossaire

| Terme | Définition |
|-------|-----------|
| **DAMA-DMBOK** | Data Management Body of Knowledge — référentiel international de la gestion des données couvrant 11 domaines (gouvernance, qualité, architecture, sécurité, etc.). |
| **Data Catalog** | Inventaire centralisé et consultable de tous les actifs de données d'une organisation, incluant métadonnées techniques, descriptions métier et lignage. Exemples : DataHub, Atlan, OpenMetadata. |
| **Data Lineage** | Traçabilité de bout en bout des données : origine, transformations successives et destinations. Permet l'analyse d'impact et le débogage des pipelines. |
| **Data Steward** | Responsable opérationnel de la qualité et de la conformité des données d'un domaine. Définit et applique les règles de qualité au quotidien. |
| **Data Owner** | Responsable métier décisionnaire d'un domaine de données. Définit les règles d'accès, valide les définitions et arbitre les priorités de qualité. |
| **Master Data Management (MDM)** | Discipline visant à créer et maintenir un référentiel unique (golden record) pour les entités métier clés (clients, produits, fournisseurs) à travers les systèmes. |
| **Data Quality Score** | Score agrégé mesurant la qualité des données sur les 6 dimensions DAMA (complétude, unicité, validité, cohérence, exactitude, actualité), exprimé en pourcentage. |
| **Data Contract** | Accord formel entre producteurs et consommateurs de données spécifiant le schéma, les SLAs de fraîcheur et de qualité, et les responsabilités respectives. |
| **Dimensional Modeling (Kimball)** | Méthodologie de modélisation de Ralph Kimball pour les entrepôts de données, organisée autour de tables de faits (mesures) et de dimensions (contextes d'analyse). |
| **Star Schema** | Modèle en étoile : une table de faits centrale reliée directement à des tables de dimensions dénormalisées. Optimisé pour la performance en lecture et la simplicité des requêtes BI. |
| **Snowflake Schema** | Variante du star schema où les tables de dimensions sont normalisées en sous-dimensions. Réduit la redondance au prix d'une complexité accrue des jointures. |
| **Data Vault 2.0** | Méthodologie de modélisation orientée audit et historisation, basée sur des hubs (clés métier), links (relations) et satellites (attributs horodatés). Adaptée aux environnements multi-sources. |
| **SCD (Slowly Changing Dimension)** | Technique de gestion de l'historique des dimensions. Type 1 : écrasement. Type 2 : nouvelle ligne avec dates de validité. Type 3 : colonne de valeur précédente. |
| **KPI Tree** | Arbre de décomposition hiérarchique des indicateurs clés de performance, du KPI stratégique aux métriques opérationnelles actionnables par chaque équipe. |
| **Self-service BI** | Approche permettant aux utilisateurs métier d'explorer et d'analyser les données de manière autonome via des datasets certifiés et des outils BI accessibles, sans dépendance systématique envers l'équipe data. |
| **Semantic Layer** | Couche d'abstraction entre les données brutes et les outils de consommation, centralisant les définitions de métriques et les règles de calcul pour garantir la cohérence. Exemples : dbt Semantic Layer, LookML, Cube. |
| **Data Mesh** | Architecture décentralisée où chaque domaine métier est responsable de ses propres data products, avec une gouvernance fédérée et des standards d'interopérabilité communs. |
| **Data Fabric** | Architecture intégrée utilisant des métadonnées actives et l'automatisation (ML) pour connecter, gouverner et consommer les données à travers des environnements hétérogènes et distribués. |
| **RGPD (Règlement Général sur la Protection des Données)** | Réglementation européenne (2018) encadrant la collecte, le traitement et le stockage des données personnelles. Impose le consentement, le droit à l'oubli, la portabilité et la protection dès la conception (privacy by design). |

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[BI & Reporting](./references/bi-reporting.md)** : comparaison detaillee des outils BI, bonnes pratiques de design de dashboards, self-service BI, automatisation du reporting, KPI frameworks et metric trees.
- **[Data Governance & Quality](./references/data-governance-quality.md)** : framework DAMA-DMBOK, catalogage des donnees, data lineage, regles et monitoring de la qualite, MDM, ownership et stewardship, data contracts.
- **[Data Modeling](./references/data-modeling.md)** : dimensional modeling Kimball (star/snowflake), Data Vault 2.0, types de Slowly Changing Dimensions, modeles conceptuel/logique/physique, pattern One Big Table.
- **[Analytics & Privacy](./references/analytics-privacy.md)** : analytics descriptive/diagnostique/predictive/prescriptive, analyse statistique, cartographie RGPD, classification des donnees, techniques d'anonymisation, politiques de retention.

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.
