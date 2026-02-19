---
name: data-quality
version: 1.0.0
description: >
  Use this skill when the user asks about "data quality", "data observability", "data contracts", "data mesh", "data catalog", "data lineage", "data freshness", "data volume anomaly", "schema drift", "Great Expectations", "Monte Carlo data", "dbt tests", "data products", "data ownership", "federated governance", "data SLOs", discusses data reliability engineering, building trust in data pipelines, or needs guidance on implementing data contracts, data mesh architecture, and data quality monitoring.
---

# Data Quality — Observabilite, Data Contracts, Data Mesh & Data Catalog

## Overview

La qualite des donnees est la contrainte numero un des projets analytiques et IA : 80% du temps d'un data scientist est depense a nettoyer et verifier les donnees, pas a modeliser. L'approche moderne ne cherche plus a "nettoyer" les donnees a posteriori mais a garantir leur fiabilite a la source, en continu.

**Quatre piliers de la qualite de donnees moderne** :
- **Data Observability** : savoir quand les donnees sont cassees, avant que l'utilisateur ne s'en rende compte
- **Data Contracts** : accords explicites entre producteurs et consommateurs de donnees sur la structure, la semantique et les SLOs
- **Data Mesh** : architecture organisationnelle ou les domaines metier possedent leurs donnees comme des produits
- **Data Catalog** : inventaire actif (pas un wiki statique) de toutes les donnees de l'organisation avec contexte, lineage et gouvernance

**Le cout de la mauvaise qualite des donnees** : Selon Gartner, la mauvaise qualite des donnees coute en moyenne 12.9 millions USD par an aux organisations. 83% des CDOs citent la qualite des donnees comme leur premier obstacle.

**Evolution du paradigme** : Reactive (corriger les erreurs quand elles sont signalees) → Proactive (detecter avant impact) → Preventive (empecher les erreurs d'entrer dans le pipeline).

## Core Principles

**1. Fail fast, fail loudly.** Un pipeline qui produit silencieusement des donnees incorrectes est pire qu'un pipeline arrete. Les alertes sur la qualite doivent etre bruyantes, visibles et actionnables. Le silence n'est pas une garantie de qualite.

**2. Shift left — la qualite a la source.** Detecter les problemes le plus tot possible dans le pipeline reduit le cout de correction par 10x. Les tests de qualite appartiennent au producteur de donnees, pas seulement au consommateur.

**3. Data contracts — des accords explicites.** Les dependencies implicites sur les schemas et la semantique des donnees sont la source principale de pannes. Rendre ces dependances explicites par des contrats versiones et gates.

**4. Observabilite sur les 5 piliers.** La qualite d'un dataset se mesure sur : Freshness (fraicheur), Volume (quantite), Distribution (statistiques), Schema (structure), et Lineage (origine). Un monitoring partiel cree des angles morts.

**5. Ownership des donnees au domaine.** La qualite des donnees s'ameliore quand les equipes qui produisent les donnees sont responsables de leur qualite downstream. Le modele centralise (data team unique responsable de tout) ne scale pas.

**6. Data products, pas pipelines.** Un data product a un owner, un SLO de qualite, une documentation et une version. Un pipeline est une implementation. Penser "produit" change la culture de la responsabilite.

## Les 5 Piliers de la Data Observability

| Pilier | Definition | Alertes typiques |
|---|---|---|
| **Freshness** | Les donnees sont-elles arrivees a l'heure ? | Table non mise a jour depuis X heures |
| **Volume** | Le volume est-il dans la plage attendue ? | Volume < 80% ou > 120% de la normale |
| **Distribution** | Les statistiques sont-elles stables ? | Moyenne, median, % null en dehors de Z-score |
| **Schema** | La structure a-t-elle change ? | Colonne ajoutee/supprimee, type change |
| **Lineage** | D'ou viennent les donnees, qui les utilise ? | Impact analysis lors d'un changement upstream |

## Data Contracts — Specification et Implementation

### Definition
Un data contract est un accord formel entre un producteur de donnees et ses consommateurs, specifiant :
- La **structure** : schema, types, contraintes
- La **semantique** : definitions metier des champs
- Les **SLOs de qualite** : freshness, completude, unicite
- Les **modalites de changement** : deprecation, versioning, delai de notification

### Format de Specification (YAML — Open Data Contract Standard)

```yaml
# contrat: orders_v2.yaml
dataContractSpecification: 0.9.9
id: orders-daily-v2
info:
  title: Orders Daily Aggregated
  version: 2.1.0
  description: |
    Aggregation quotidienne des commandes par client et categorie produit.
    Produit par le domaine Order Management, consomme par Finance et Marketing.
  owner: order-management-team
  contact:
    email: data-owner@company.com

servers:
  production:
    type: bigquery
    project: prod-data-platform
    dataset: gold
    table: orders_daily

terms:
  usage: >
    Usage interne uniquement. Ne pas utiliser pour du reporting externe.
  limitations: >
    Les commandes annulees dans les 2h sont exclues.
  billing: internal
  noticePeriod: 30 days

models:
  orders_daily:
    fields:
      order_date:
        type: date
        required: true
        description: Date de la commande (UTC)
      customer_id:
        type: string
        required: true
        pattern: "^CUST-[0-9]{8}$"
      revenue_eur:
        type: decimal
        required: true
        minimum: 0
        description: Revenu HT en EUR

quality:
  type: SodaCL
  specification:
    checks for orders_daily:
      - freshness(order_date) < 26h
      - row_count > 50000
      - missing_count(customer_id) = 0
      - duplicate_count(order_date, customer_id) = 0
      - min(revenue_eur) >= 0

servicelevels:
  availability:
    description: Table disponible a 06h00 CET
    percentage: 99.5%
  freshness:
    description: Donnees du J-1 disponibles a 06h00 CET
    threshold: 26h
```

### Workflow d'implementation

1. **Ecriture du contrat** : Le producteur (squad Order Management) redige le contrat en YAML
2. **Revue par les consommateurs** : Finance et Marketing valident les definitions et SLOs
3. **Integration en CI/CD** : Le contrat est gate avant merge — un changement de schema incompatible bloque le pipeline
4. **Monitoring continu** : Le contrat est execute automatiquement a chaque nouvelle partition
5. **Gestion des breaking changes** : Version majeure + periode de deprecation de 30 jours minimum

## Data Mesh — Architecture et Principes

### Les 4 Principes (Zhamak Dehghani)

**1. Domain Ownership** : Chaque domaine metier (Order Management, Customer, Finance) est responsable de ses donnees en tant que produits. Pas de transfert de responsabilite vers une equipe data centrale.

**2. Data as a Product** : Un data product a : un owner, une documentation, un SLO de qualite, une version, une API stable, une interface de decouverte. Pas juste une table dans un schema.

**3. Self-serve Data Infrastructure** : L'infrastructure data (ingestion, transformation, stockage, catalogue) est un service interne avec UX — les domaines peuvent creer et decouvrir des data products sans tickets a l'equipe plateforme.

**4. Federated Computational Governance** : Les standards de qualite, de securite et d'interoperabilite sont definis centralement (guild data) mais implementes par chaque domaine. Equilibre entre autonomie et coherence.

### Architecture type Data Mesh

```
Data Platform Team (enablement)
├── Infrastructure self-serve (ingestion tools, dbt templates, CI/CD)
├── Data Catalog (Datahub, Collibra, OpenMetadata)
└── Standards & Governance (data contracts spec, quality SLOs, security policies)

Domain: Order Management
├── Source-aligned data products (raw orders, order events)
├── Aggregate data products (orders_daily, revenue_by_product)
└── Data Contract: orders_daily_v2.yaml

Domain: Customer
├── customer_360 data product
├── customer_segments data product
└── Data Contracts: customer_v1.yaml

Domain: Finance
├── Consomme: orders_daily, customer_360
└── Produit: p&l_monthly, revenue_forecast
```

### Data Mesh vs Data Warehouse Central

| Dimension | Data Warehouse Central | Data Mesh |
|---|---|---|
| Ownership | Equipe data centrale | Domaines metier |
| Scalabilite organisationnelle | Goulot d'etranglement a partir de ~5 domaines | Scale par domaine |
| Consistance | Haute (un lieu) | Requiert governance federee |
| Time to market | Lent (dependance equipe centrale) | Rapide (autonomie domaine) |
| Adapte pour | Organisations < 50 personnes data | Organisations avec > 5 domaines data actifs |

## Data Catalog — De l'Inventaire au Systeme Vivant

### Ce qu'un bon Data Catalog doit faire
- **Decouverte** : trouver une table par mot-cle metier, pas par chemin technique
- **Contexte** : description, owner, statut (actif/deprecie), sensibilite
- **Lineage** : d'ou vient la table, quels rapports dependent de cette table
- **Qualite** : score de qualite en temps reel, historique des incidents
- **Gouvernance** : classification des donnees sensibles, acces, audit log

### Outils principaux

| Outil | Positionnement | Points forts |
|---|---|---|
| **Datahub** (LinkedIn, open source) | Plateforme complete, metadata graph | Lineage automatique, intégrations nombreuses |
| **OpenMetadata** (open source) | Alternative moderne a Datahub | UI moderne, data contracts integres |
| **Collibra** | Enterprise, gouvernance avancee | Stewardship workflows, compliance |
| **Alation** | Mid-market, BI-centric | Bonne UX, collaboration |
| **dbt + Elementary** | Leger, code-first | Parfait si dbt central, gratuit |

## Outils d'Implementation

### dbt Tests (qualite integree au code)

```yaml
# models/gold/schema.yml
models:
  - name: orders_daily
    description: "Commandes quotidiennes agregees"
    columns:
      - name: order_date
        tests:
          - not_null
          - dbt_utils.recency:
              datepart: day
              field: order_date
              interval: 1
      - name: customer_id
        tests:
          - not_null
          - unique
          - relationships:
              to: ref('customers')
              field: customer_id
      - name: revenue_eur
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
```

### Great Expectations (tests Python avances)

```python
import great_expectations as gx

context = gx.get_context()
validator = context.get_validator(
    datasource_name="prod_bigquery",
    data_asset_name="orders_daily"
)

# Tests statistiques
validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_mean_to_be_between("revenue_eur", 45, 120)
validator.expect_table_row_count_to_be_between(50000, 200000)
validator.expect_column_proportion_of_unique_values_to_be_between(
    "order_date", min_value=0.99
)

results = validator.validate()
if not results.success:
    raise ValueError(f"Data quality check failed: {results}")
```

## Data Quality SLOs — Exemples

| Data Product | SLO Freshness | SLO Completude | SLO Unicite |
|---|---|---|---|
| orders_daily | < 26h | customer_id null = 0% | (order_date, customer_id) 100% unique |
| customer_360 | < 48h | email null < 5% | customer_id 100% unique |
| revenue_forecast | Lundi 08h00 | - | forecast_date unique par BU |

## Maturity Model — Data Quality

| Niveau | Caracteristique | Indicateurs |
|---|---|---|
| **1 — Reactif** | Les problemes sont signales par les utilisateurs | Tickets "les chiffres sont faux" frequents |
| **2 — Monitore** | Alertes de base (freshness, volume) | Dashboard de sante des pipelines |
| **3 — Teste** | Tests dbt sur les tables cles | Taux de couverture tests > 80% tables gold |
| **4 — Contracte** | Data contracts en production | Breaking changes detectes avant impact |
| **5 — Produit** | Data mesh, data products avec SLOs publics | Score de qualite visible dans le catalogue |

## Limites et Points de Vigilance

- Le data mesh est une transformation organisationnelle, pas seulement technique : sans ownership clair des domaines et sans culture "data as product", la technique seule echoue
- Les data contracts creent de la friction positive (breaking changes detectes) mais aussi de la friction negative (agilite reduite) — bien calibrer les contraintes
- Un catalogue non maintenu est pire qu'un catalogue absent : allouer une fraction du temps des data stewards a la maintenance active
- La qualite des donnees a la source requiert des engagements des equipes product/engineering — la data team seule ne peut pas l'imposer
- Great Expectations et Monte Carlo sont complementaires, pas alternatifs : Great Expectations pour les tests business logiques, Monte Carlo pour la detection d'anomalies statistiques automatisee
