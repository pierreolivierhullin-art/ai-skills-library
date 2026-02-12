# Data Governance & Quality — DAMA-DMBOK, Cataloging, Lineage, MDM & Data Contracts

## Overview

Ce document de reference couvre la gouvernance des donnees selon le framework DAMA-DMBOK, le catalogage des donnees, la lineage, la qualite des donnees et son monitoring, le Master Data Management (MDM), les roles de data ownership et stewardship, ainsi que les data contracts. Utiliser ce guide pour etablir et operer un programme de gouvernance des donnees mature et efficace.

This reference document covers data governance per the DAMA-DMBOK framework, data cataloging, data lineage, data quality rules and monitoring, Master Data Management (MDM), data ownership and stewardship roles, and data contracts. Use this guide to establish and operate a mature and effective data governance program.

---

## DAMA-DMBOK Framework — Deep Dive

### Data Governance Organization

#### Modeles organisationnels / Organizational Models

Choisir le modele de gouvernance adapte a la taille et a la culture de l'organisation :

| Modele | Description | Quand l'utiliser |
|---|---|---|
| **Centralise** | Equipe de gouvernance unique, regles uniformes | Organisations reglementees, besoin de coherence forte |
| **Federe (Data Mesh)** | Chaque domaine gere ses propres donnees, standards communs | Organisations decentralisees, equipes autonomes |
| **Hybride** | Equipe centrale pour les standards, equipes de domaine pour l'execution | La plupart des cas, bon equilibre gouvernance/agilite |

#### Roles et responsabilites / Roles and Responsibilities

| Role | Responsabilite | Profil |
|---|---|---|
| **Chief Data Officer (CDO)** | Strategie data, sponsor executif de la gouvernance | C-level, vision strategique |
| **Data Governance Council** | Decisions de gouvernance cross-domaine, arbitrage | Leaders de chaque domaine |
| **Data Owner** | Decisions metier sur ses donnees (acces, qualite, retention) | Manager metier du domaine |
| **Data Steward** | Execution operationnelle de la gouvernance (qualite, catalogue, regles) | Profil mixte metier/technique |
| **Data Engineer** | Implementation technique des pipelines et des controles | Ingenieur data |
| **Analytics Engineer** | Modelisation, semantic layer, datasets certifies | Profil hybride engineering/analytics |
| **Data Protection Officer (DPO)** | Conformite RGPD, registre des traitements, DPIA | Juridique / compliance |

#### Policies et Standards

Formaliser les politiques de gouvernance dans des documents accessibles et versionnes :

- **Data Classification Policy** : definir les niveaux de classification (Public, Internal, Confidential, Restricted) et les regles de traitement associees (chiffrement, acces, retention).
- **Data Quality Policy** : definir les seuils de qualite minimaux par dataset (completude > 99%, unicite 100%, freshness < 24h) et les processus de remediation.
- **Data Access Policy** : definir les regles d'acces par role et par classification. Appliquer le principe du moindre privilege.
- **Data Retention Policy** : definir les durees de conservation par type de donnee et les processus de suppression/archivage.
- **Data Naming Convention** : standardiser les noms de tables, colonnes, metriques et dimensions dans tout l'ecosysteme data.

---

## Data Cataloging

### Pourquoi un catalogue de donnees / Why a Data Catalog

Un data catalog est le registre central de tous les actifs de donnees de l'organisation. Il repond aux questions : "Quelles donnees existent ? Ou sont-elles ? Que signifient-elles ? Qui en est responsable ? Quelle est leur qualite ?"

Sans catalogue, les equipes passent 30-50% de leur temps a chercher et comprendre les donnees. Le catalogue reduit le time-to-insight et elimine la duplication d'efforts.

### Outils de catalogage / Cataloging Tools

#### DataHub (LinkedIn / Acryl Data)

- **Open source** : projet open source mature, soutenu par Acryl Data (version managed).
- **Ingestion automatique** : connecteurs pour 50+ sources (databases, data warehouses, BI tools, orchestrators, pipelines). Ingestion via push (APIs) et pull (recipes).
- **Lineage automatique** : capture de la lineage depuis dbt, Airflow, Spark, SQL parsers. Visualisation graphique des dependencies.
- **Business glossary** : creation de termes metier, association aux colonnes et datasets, gestion des synonymes.
- **Data quality integration** : integration avec Great Expectations, Soda, dbt tests pour afficher les resultats de qualite dans le catalogue.
- **Architecture** : basee sur un metadata graph (GMS — Generalized Metadata Service) avec Kafka pour l'ingestion temps reel et Elasticsearch pour la recherche.

#### Atlan

- **Managed platform** : solution SaaS de catalogage et de gouvernance. Pas d'infrastructure a gerer.
- **Active metadata** : au-dela du catalogage passif, Atlan propose des workflows automatises (alerts sur les changements de schema, propagation des tags, workflows d'approbation).
- **Collaboration** : commentaires, annotations, tickets integres dans le catalogue. Experience similaire a un outil collaboratif moderne (Notion-like).
- **Lineage multi-couche** : lineage depuis les sources jusqu'aux dashboards, incluant les transformations intermediaires.
- **Classification automatique** : detection automatique de PII et de donnees sensibles via des patterns et du ML.

#### OpenMetadata

- **Open source** : projet Apache en forte croissance. Alternative open source a Atlan.
- **Architecture moderne** : API-first, deploiement containerise (Docker, Kubernetes).
- **Data quality native** : moteur de qualite integre (pas besoin d'outil tiers pour des controles basiques).
- **Data insights** : tableaux de bord analytiques sur l'utilisation du catalogue lui-meme (quels datasets sont les plus consultes, quels termes manquent de documentation).
- **Collaboration** : conversations, taches, announcements integres au catalogue.

### Contenu du catalogue / Catalog Content

Chaque entree du catalogue doit contenir au minimum :

| Metadonnee | Type | Description |
|---|---|---|
| **Nom technique** | Technique | Nom de la table, vue, dataset |
| **Nom metier** | Business | Nom comprehensible par les utilisateurs metier |
| **Description** | Business | Definition detaillee, contexte, usage |
| **Owner** | Governance | Data Owner (metier) et equipe technique responsable |
| **Classification** | Security | Niveau de sensibilite (Public, Internal, Confidential, Restricted) |
| **Tags** | Discovery | Tags thematiques, domaine, source |
| **Schema** | Technique | Colonnes, types, descriptions par colonne |
| **Lineage** | Technique | Sources en amont, consommateurs en aval |
| **Qualite** | Quality | Score de qualite, derniers resultats de tests |
| **Freshness** | Operations | Derniere mise a jour, frequence de rafraichissement |
| **Termes du glossary** | Business | Termes metier associes depuis le business glossary |
| **SLA** | Operations | SLAs de disponibilite et de fraicheur |

---

## Data Lineage

### Types de lineage / Lineage Types

- **Table-level lineage** : montre les dependances entre tables et vues. Repond a "cette table depend de quelles sources ?" et "quels dashboards seraient impactes si je modifie cette table ?"
- **Column-level lineage** : montre les transformations au niveau colonne. Repond a "d'ou vient la valeur de cette colonne ?" et "comment est calculee cette metrique ?"
- **Pipeline-level lineage** : montre les dependances entre jobs et pipelines (DAGs Airflow, dbt models, Spark jobs). Repond a "quel est l'ordre d'execution ?" et "quel pipeline a produit ces donnees ?"

### Sources de lineage / Lineage Sources

| Source | Methode de capture | Outils |
|---|---|---|
| **dbt** | Parsing du manifest.json et du catalog.json | DataHub, Atlan, Elementary |
| **SQL queries** | Parsing SQL statique ou dynamique | sqllineage, OpenLineage |
| **Airflow** | Extraction depuis les DAGs et les metadata | OpenLineage, Marquez |
| **Spark** | SparkListener, OpenLineage integration | OpenLineage, Marquez |
| **BI tools** | API Tableau/Power BI/Looker | DataHub, Atlan |
| **Bases de donnees** | System views (pg_depend, information_schema) | DataHub connectors |

### OpenLineage Standard

OpenLineage est un standard ouvert pour la collecte de lineage. Adopter OpenLineage pour normaliser la capture de lineage entre differents outils et technologies. Les principaux composants :

- **Run Events** : START, COMPLETE, FAIL — marquer le debut et la fin de chaque job.
- **Datasets** : inputs et outputs de chaque job, avec schema et facets.
- **Facets** : metadonnees additionnelles (qualite, schema, provenance, statistiques).

```json
{
  "eventType": "COMPLETE",
  "eventTime": "2026-01-15T10:30:00Z",
  "run": { "runId": "run-uuid-123" },
  "job": {
    "namespace": "dbt-production",
    "name": "fct_orders"
  },
  "inputs": [
    { "namespace": "warehouse", "name": "raw.orders" },
    { "namespace": "warehouse", "name": "raw.customers" }
  ],
  "outputs": [
    { "namespace": "warehouse", "name": "analytics.fct_orders" }
  ]
}
```

---

## Data Quality — Rules, Testing & Monitoring

### Strategie de qualite en couches / Layered Quality Strategy

Implementer les controles de qualite a chaque couche du pipeline :

```
Source Systems --> [Source quality checks]
  --> Ingestion --> [Schema validation, row count, freshness]
    --> Staging (Bronze) --> [Null checks, type checks, deduplication]
      --> Transformation (Silver) --> [Business rules, cross-source reconciliation]
        --> Mart (Gold) --> [Metric validation, anomaly detection, SLA checks]
          --> BI Layer --> [Dashboard-level freshness, data completeness]
```

### Outils de qualite / Quality Tools

#### dbt Tests

Les tests dbt sont la premiere ligne de defense. Integrer des tests a chaque modele :

```yaml
# models/staging/stg_orders.yml
models:
  - name: stg_orders
    description: "Staged orders from the source system"
    columns:
      - name: order_id
        description: "Primary key for orders"
        data_tests:
          - unique
          - not_null
      - name: customer_id
        data_tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id
      - name: order_status
        data_tests:
          - accepted_values:
              values: ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
      - name: order_amount
        data_tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: ">= 0"

# Tests custom au niveau du modele
    data_tests:
      - dbt_utils.recency:
          datepart: hour
          field: updated_at
          interval: 24
      - row_count_greater_than:
          min_count: 1000
```

#### Great Expectations (GX)

Great Expectations fournit un framework Python complet pour definir, documenter et valider les attentes sur les donnees :

```python
# Definir une Expectation Suite
import great_expectations as gx

context = gx.get_context()

# Creer un checkpoint de validation
datasource = context.data_sources.add_pandas("orders_source")
data_asset = datasource.add_dataframe_asset("orders")

batch = data_asset.add_batch_definition_whole_dataframe("full_batch")

suite = context.suites.add(
    gx.ExpectationSuite(name="orders_quality_suite")
)

# Ajouter des expectations
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(column="order_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="order_amount", min_value=0, max_value=1000000
    )
)
suite.add_expectation(
    gx.expectations.ExpectTableRowCountToBeBetween(
        min_value=1000, max_value=10000000
    )
)
```

#### Soda

Soda utilise un langage declaratif (SodaCL) pour definir des checks de qualite :

```yaml
# checks/orders_checks.yml
checks for analytics.fct_orders:
  # Freshness
  - freshness(updated_at) < 24h

  # Volume
  - row_count > 1000
  - row_count_change < 50%

  # Completeness
  - missing_count(order_id) = 0
  - missing_count(customer_id) = 0
  - missing_percent(email) < 5%

  # Validity
  - invalid_count(order_status) = 0:
      valid values: [pending, confirmed, shipped, delivered, cancelled]
  - invalid_count(order_amount) = 0:
      valid min: 0

  # Uniqueness
  - duplicate_count(order_id) = 0

  # Cross-source reconciliation
  - row_count same as analytics.stg_orders

  # Custom SQL
  - total_revenue_check:
      total_revenue query: |
        SELECT SUM(order_amount) as total
        FROM analytics.fct_orders
        WHERE order_date = CURRENT_DATE - 1
      fail: when total < 10000
```

### Data Observability

Au-dela des tests ponctuels, mettre en place une observabilite continue des donnees :

- **Elementary** : open source, integre a dbt. Genere des dashboards de qualite automatiques, detecte les anomalies sur le volume, la freshness et les distributions.
- **Monte Carlo** : solution SaaS leader en data observability. Detection automatique d'anomalies, lineage, alerting, incident management. Positionne comme le "Datadog des donnees".
- **Soda Cloud** : version managed de Soda avec des dashboards de qualite, des alertes et un suivi temporel des metrics de qualite.

#### Metriques de qualite a monitorer / Quality Metrics to Monitor

| Metrique | Definition | Seuil recommande |
|---|---|---|
| **Data Quality Score** | Score composite (0-100) pondere sur les 6 dimensions | > 95% |
| **Freshness SLA compliance** | % de datasets rafraichis dans les SLAs | > 99% |
| **Test pass rate** | % de tests de qualite reussis | > 98% |
| **Mean time to detect (MTTD)** | Temps moyen de detection d'un probleme de qualite | < 1 heure |
| **Mean time to resolve (MTTR)** | Temps moyen de resolution d'un incident data | < 4 heures |
| **Catalog coverage** | % de datasets documentes dans le catalogue | > 90% |
| **Glossary coverage** | % de colonnes metier liees a un terme du glossary | > 80% |

---

## Master Data Management (MDM)

### Concepts fondamentaux / Core Concepts

Le MDM vise a creer et maintenir un "golden record" unique et autorise pour chaque entite metier (client, produit, fournisseur, employe, localisation). Sans MDM, les entites sont definies differemment dans chaque systeme, rendant le reporting cross-systeme incoherent.

### Styles d'implementation MDM / MDM Implementation Styles

| Style | Description | Complexite | Cas d'usage |
|---|---|---|---|
| **Registry** | Index central pointant vers les systemes sources (pas de duplication) | Faible | Reporting cross-systeme, reconciliation |
| **Consolidation** | Hub central en lecture seule agrege les donnees sources | Moyenne | BI / analytics, vue 360 client |
| **Coexistence** | Hub central synchronise bi-directionnellement avec les sources | Elevee | Gouvernance proactive, data stewardship |
| **Transaction** | Hub central est la source de verite, alimente les systemes en aval | Tres elevee | Golden record autoritaire, processus critiques |

### Processus MDM / MDM Process

1. **Data profiling** : analyser les donnees sources pour comprendre les formats, les doublons, les incoherences.
2. **Standardisation** : normaliser les formats (adresses, noms, codes). Utiliser des libraries de standardisation (libpostal pour les adresses, phonenumbers pour les telephones).
3. **Matching** : identifier les records potentiellement dupliques via des algorithmes de matching (exact, fuzzy, probabiliste). Outils : Dedupe.io, Splink, Informatica MDM, Reltio.
4. **Merging** : fusionner les records dupliques en un golden record. Definir des regles de survivance (quel systeme fait autorite pour chaque attribut).
5. **Enrichment** : completer le golden record avec des donnees externes (firmographic, demographic, geolocation).
6. **Distribution** : publier le golden record vers les systemes consommateurs via API, events ou batch sync.
7. **Stewardship** : les Data Stewards examinent et resolvent les cas ambigus de matching et de merge.

### MDM dans le Modern Data Stack

Dans le contexte du Modern Data Stack, l'approche MDM evolue :

- **dbt-based MDM** : implementer la logique de matching et de merging dans dbt avec des modeles dedies (staging, matching, golden record). Moins sophistique qu'un outil MDM dedie mais integre nativement dans le pipeline de transformation.
- **Reverse ETL for MDM** : publier le golden record depuis le data warehouse vers les systemes operationnels via Reverse ETL (Census, Hightouch, Polytomic).
- **Entity resolution** : utiliser des techniques de ML pour la resolution d'entites a grande echelle (Zingg, Splink, Senzing).

---

## Data Contracts

### Definition et objectif / Definition and Purpose

Un data contract est un accord formel entre un producteur de donnees et ses consommateurs. Il specifie le schema, la semantique, la qualite, la fraicheur et les responsabilites. Les data contracts permettent de decouvrir les problemes de donnees a la source plutot qu'en aval dans les dashboards.

### Anatomie d'un data contract / Data Contract Anatomy

```yaml
# data-contracts/orders-contract.yml
apiVersion: v1
kind: DataContract
metadata:
  name: orders-domain-contract
  version: 2.1.0
  owner: order-team@company.com
  domain: commerce
  description: |
    Contract for the orders data product. Contains all confirmed
    and processed orders from the commerce platform.

schema:
  type: object
  properties:
    order_id:
      type: string
      format: uuid
      description: "Unique identifier for the order"
      pii: false
    customer_id:
      type: string
      format: uuid
      description: "Reference to the customer entity"
      pii: false
    order_date:
      type: string
      format: date-time
      description: "Timestamp when the order was placed (UTC)"
    order_status:
      type: string
      enum: [pending, confirmed, shipped, delivered, cancelled]
      description: "Current status of the order"
    total_amount:
      type: number
      minimum: 0
      description: "Total order amount in EUR"
    customer_email:
      type: string
      format: email
      description: "Customer email address"
      pii: true
      classification: confidential

quality:
  completeness:
    order_id: 100%
    customer_id: 100%
    order_date: 100%
    order_status: 100%
    total_amount: 99.5%
  uniqueness:
    order_id: 100%
  freshness:
    max_delay: 1h
    check_column: updated_at
  volume:
    min_rows_per_day: 1000
    max_change_percent: 50%

sla:
  availability: 99.9%
  refresh_frequency: hourly
  support_channel: "#data-orders-support"
  incident_response_time: 1h

consumers:
  - name: analytics-team
    usage: "BI dashboards, revenue reporting"
    access_level: read
  - name: ml-team
    usage: "Demand forecasting model"
    access_level: read

breaking_changes:
  notification_period: 30 days
  migration_support: true
```

### Enforcement des data contracts / Data Contract Enforcement

Automatiser la verification des data contracts dans le pipeline CI/CD :

1. **Schema validation** : verifier que le schema reel correspond au schema contractuel a chaque run de pipeline. Utiliser des schema registries (Confluent, AWS Glue) ou des validateurs YAML/JSON Schema.
2. **Quality checks** : executer les seuils de qualite definis dans le contrat (Soda, Great Expectations, dbt tests).
3. **Freshness monitoring** : verifier que les donnees sont livrees dans les SLAs definis.
4. **Breaking change detection** : detecter les changements de schema incompatibles (suppression de colonne, changement de type) avant le deployment.
5. **Consumer notification** : alerter automatiquement les consommateurs en cas de violation de contrat ou de changement planifie.

---

## Data Stewardship Operations

### Processus quotidiens du Data Steward / Daily Stewardship Processes

1. **Triage des alertes qualite** : examiner les alertes de qualite (tests echoues, anomalies detectees). Classifier en critique (blocage business), majeur (degradation) ou mineur (cosmetique).
2. **Resolution des incidents data** : investiguer les causes racines des problemes de qualite. Coordonner la remediation avec les equipes d'engineering et metier.
3. **Revue du catalogue** : valider les nouvelles entrees du catalogue, verifier les descriptions et les tags, associer les termes du glossary.
4. **Stewardship MDM** : resoudre les cas de matching ambigus, valider les merges proposes par le systeme automatise.
5. **Demandes d'acces** : evaluer et approuver les demandes d'acces aux donnees en fonction de la classification et du besoin metier (principe du moindre privilege).

### Metriques de stewardship / Stewardship Metrics

| Metrique | Objectif |
|---|---|
| Alertes qualite resolues dans les SLAs | > 95% |
| Temps moyen de triage des alertes | < 2 heures |
| Backlog de documentation catalogue | < 20 items |
| Cas MDM en attente de resolution | < 50 |
| Satisfaction des consommateurs de donnees (survey) | > 4/5 |
