# Data Modeling — Kimball, Data Vault 2.0, SCD & Physical Models

## Overview

Ce document de reference couvre les methodologies de modelisation des donnees pour les entrepots de donnees et les plateformes analytiques. Il traite le dimensional modeling de Kimball (star schema, snowflake schema), le Data Vault 2.0, les Slowly Changing Dimensions (SCD), les modeles conceptuel/logique/physique, et le pattern One Big Table (OBT). Utiliser ce guide pour choisir et implementer la strategie de modelisation adaptee au contexte.

This reference document covers data modeling methodologies for data warehouses and analytical platforms. It covers Kimball dimensional modeling (star schema, snowflake schema), Data Vault 2.0, Slowly Changing Dimensions (SCD), conceptual/logical/physical models, and the One Big Table (OBT) pattern. Use this guide to choose and implement the modeling strategy appropriate to the context.

---

## Conceptual / Logical / Physical Models

### Les trois couches de modelisation / Three Modeling Layers

Toujours proceder en trois etapes, du plus abstrait au plus concret. Ne jamais sauter directement au modele physique.

#### Modele conceptuel / Conceptual Model

- **Objectif** : capturer les entites metier et leurs relations a haut niveau. Communication avec les parties prenantes non techniques.
- **Audience** : Data Owners, Business Analysts, Product Managers.
- **Contenu** : entites (Client, Commande, Produit), relations (passe, contient, appartient a), cardinalites (1:N, N:M).
- **Notation** : diagramme entite-relation (ERD) simplifie, ou format libre (whiteboards, Miro).
- **Principe** : zero jargon technique. Les noms doivent correspondre au vocabulaire metier (ubiquitous language).

```
[Client] --1:N--> [Commande] --N:M--> [Produit]
                      |
                   [Paiement]
```

#### Modele logique / Logical Model

- **Objectif** : detailler les attributs, les types de donnees logiques, les cles, les contraintes et les regles metier. Independent de la technologie cible.
- **Audience** : Analytics Engineers, Data Architects, Data Stewards.
- **Contenu** : attributs detailles, types logiques (texte, entier, date, booleen), cles primaires et etrangeres, contraintes (not null, unique, check), regles de derivation (champ calcule).
- **Notation** : ERD detaille (UML, Crow's Foot, IDEF1X).

```
Client
  PK client_id         : UUID
     nom               : VARCHAR(100) NOT NULL
     email             : VARCHAR(255) NOT NULL UNIQUE
     date_inscription  : DATE NOT NULL
     segment           : ENUM('B2B', 'B2C', 'Enterprise')

Commande
  PK commande_id       : UUID
  FK client_id         : UUID NOT NULL --> Client.client_id
     date_commande     : TIMESTAMP NOT NULL
     statut            : ENUM('pending','confirmed','shipped','delivered','cancelled')
     montant_total     : DECIMAL(12,2) NOT NULL CHECK(>= 0)
```

#### Modele physique / Physical Model

- **Objectif** : implementation concrete dans la technologie cible (Snowflake, BigQuery, Redshift, PostgreSQL). Optimise pour la performance.
- **Audience** : Data Engineers, DBAs.
- **Contenu** : DDL (CREATE TABLE), types de donnees specifiques a la plateforme, partitionnement, clustering, indexation, compression, materialized views.
- **Decisions specifiques au moteur** :

| Decision | Snowflake | BigQuery | Redshift |
|---|---|---|---|
| **Partitioning** | Micro-partitioning auto | Partition by date/integer | DISTKEY + SORTKEY |
| **Clustering** | Cluster keys manuels | Clustering columns | Compound/Interleaved SORTKEY |
| **Types** | VARIANT pour semi-structured | STRUCT, ARRAY, JSON | SUPER type |
| **Materialization** | Dynamic tables, MViews | Materialized views | MViews, late-binding views |
| **Compression** | Automatique | Automatique | Encodage par colonne (AZ64, LZO) |

---

## Kimball Dimensional Modeling

### Principes fondamentaux / Core Principles

La methodologie Kimball est le standard de reference pour la modelisation analytique depuis 30 ans. Ses principes fondamentaux restent pleinement pertinents dans le Modern Data Stack.

#### Les 4 etapes du dimensional design (Kimball)

1. **Choisir le processus metier** : identifier le processus mesurable (ventes, commandes, visites, incidents). Chaque processus genere une fact table.
2. **Declarer le grain** : definir exactement ce que represente une ligne de la fact table. Le grain doit etre le plus atomique possible (une transaction, un evenement, un clic). Ne jamais melanger les grains dans une meme fact table.
3. **Identifier les dimensions** : les dimensions repondent aux questions who, what, where, when, why, how. Chaque dimension enrichit l'analyse du fait.
4. **Identifier les faits** : les faits sont les mesures numeriques du processus (montant, quantite, duree, score). Classifier chaque fait : additif, semi-additif ou non-additif.

#### Types de faits / Fact Types

| Type | Definition | Exemple | Operations possibles |
|---|---|---|---|
| **Additif** | Sommable sur toutes les dimensions | Revenue, quantite vendue | SUM, AVG, COUNT |
| **Semi-additif** | Sommable sur certaines dimensions (pas le temps) | Solde de compte, stock | SUM (sauf sur le temps), AVG |
| **Non-additif** | Non sommable | Ratio, pourcentage, prix unitaire | AVG, MIN, MAX, weighted avg |

#### Types de fact tables / Fact Table Types

| Type | Grain | Cas d'usage | Exemples |
|---|---|---|---|
| **Transaction fact** | Une ligne par evenement | Evenements discrets | Ventes, clics, logs |
| **Periodic snapshot** | Une ligne par periode | Etats periodiques | Balance quotidienne, stock mensuel |
| **Accumulating snapshot** | Une ligne par processus (mise a jour) | Processus avec etapes | Pipeline de vente, workflow |
| **Factless fact** | Fait sans mesure numerique | Evenements de presence/absence | Presence en cours, eligibilite |

### Star Schema

Le star schema est la modelisation recommandee par defaut pour l'analytique. Une fact table centrale entoureee de dimension tables denormalisees.

```sql
-- Fact table
CREATE TABLE fct_orders (
    order_key           BIGINT PRIMARY KEY,     -- Surrogate key
    customer_key        BIGINT REFERENCES dim_customer(customer_key),
    product_key         BIGINT REFERENCES dim_product(product_key),
    date_key            INT REFERENCES dim_date(date_key),
    store_key           BIGINT REFERENCES dim_store(store_key),
    promotion_key       BIGINT REFERENCES dim_promotion(promotion_key),
    order_natural_key   VARCHAR(50),            -- Natural/business key
    order_quantity      INT NOT NULL,
    unit_price          DECIMAL(10,2) NOT NULL,
    discount_amount     DECIMAL(10,2) DEFAULT 0,
    net_amount          DECIMAL(12,2) NOT NULL, -- Derived: quantity * unit_price - discount
    tax_amount          DECIMAL(10,2) NOT NULL,
    total_amount        DECIMAL(12,2) NOT NULL  -- net_amount + tax_amount
);

-- Dimension table (denormalisee)
CREATE TABLE dim_customer (
    customer_key        BIGINT PRIMARY KEY,     -- Surrogate key
    customer_id         VARCHAR(50) NOT NULL,   -- Natural key
    customer_name       VARCHAR(200) NOT NULL,
    email               VARCHAR(255),
    segment             VARCHAR(50),
    industry            VARCHAR(100),
    city                VARCHAR(100),
    region              VARCHAR(50),
    country             VARCHAR(50),
    -- SCD Type 2 columns
    valid_from          TIMESTAMP NOT NULL,
    valid_to            TIMESTAMP,              -- NULL = current record
    is_current          BOOLEAN DEFAULT TRUE,
    -- Audit
    loaded_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Date dimension (toujours creer une dim_date dediee)
CREATE TABLE dim_date (
    date_key            INT PRIMARY KEY,        -- YYYYMMDD format
    full_date           DATE NOT NULL,
    day_of_week         SMALLINT NOT NULL,
    day_name            VARCHAR(10) NOT NULL,
    day_of_month        SMALLINT NOT NULL,
    day_of_year         SMALLINT NOT NULL,
    week_of_year        SMALLINT NOT NULL,
    iso_week            SMALLINT NOT NULL,
    month_number        SMALLINT NOT NULL,
    month_name          VARCHAR(10) NOT NULL,
    quarter             SMALLINT NOT NULL,
    year                SMALLINT NOT NULL,
    fiscal_quarter      SMALLINT,
    fiscal_year         SMALLINT,
    is_weekend          BOOLEAN NOT NULL,
    is_holiday          BOOLEAN DEFAULT FALSE,
    holiday_name        VARCHAR(100)
);
```

#### Bonnes pratiques star schema / Star Schema Best Practices

- **Surrogate keys** : toujours utiliser des surrogate keys (BIGINT auto-increment ou hash) comme cles primaires des dimensions. Conserver la natural key (business key) comme attribut. Les surrogate keys isolent le modele des changements de cles dans les systemes sources.
- **Denormaliser les dimensions** : une dimension doit contenir tous les attributs descriptifs, meme si cela implique de la redondance. La denormalisation ameliore les performances de requetage et simplifie les jointures.
- **Conformed dimensions** : partager les dimensions entre plusieurs fact tables pour permettre le drill-across (analyse cross-processus). dim_date, dim_customer et dim_product sont les candidates classiques au conforming.
- **Degenerate dimensions** : les attributs dimensionnels qui n'ont pas de table de dimension propre sont stockes directement dans la fact table (ex. : numero de commande, numero de facture).
- **Role-playing dimensions** : une meme dimension peut jouer plusieurs roles (dim_date utilisee comme order_date, ship_date, delivery_date). Creer des vues ou des alias pour chaque role.
- **Junk dimensions** : regrouper les drapeaux et indicateurs binaires (flags) dans une dimension "junk" plutot que de les stocker dans la fact table. Reduit la largeur de la fact table.

### Snowflake Schema

Le snowflake schema normalise les dimensions hierarchiques en plusieurs tables liees. Par exemple, `dim_product` est decomposee en `dim_product` -> `dim_subcategory` -> `dim_category`.

#### Quand utiliser le snowflake / When to Use Snowflake Schema

- Dimensions tres larges avec des hierarchies profondes (geographie : pays -> region -> ville -> code postal).
- Besoin de mise a jour granulaire des niveaux hierarchiques.
- Contexte OLTP-like ou la normalisation reduit le stockage et simplifie les mises a jour.

#### Quand eviter le snowflake / When to Avoid

- Performance de requetage : chaque niveau de normalisation ajoute une jointure. Sur les moteurs colonnaires modernes (Snowflake, BigQuery), la denormalisation (star) est generalement plus performante.
- Complexite pour les utilisateurs self-service : les utilisateurs non techniques trouvent le star schema plus intuitif.

---

## Data Vault 2.0

### Principes fondamentaux / Core Principles

Data Vault 2.0 (Dan Linstedt) est une methodologie de modelisation conçue pour les environnements a sources multiples, a historique complet et a evolution frequente. Contrairement a Kimball (optimise pour le reporting), Data Vault est optimise pour l'integration et l'auditabilite.

#### Les 3 types d'entites Data Vault / Three Entity Types

| Entite | Role | Cle | Contenu |
|---|---|---|---|
| **Hub** | Identite metier unique | Business key (hash) | Business key, load_date, record_source |
| **Link** | Relation entre hubs | Hash des business keys liees | FK vers les hubs, load_date, record_source |
| **Satellite** | Attributs descriptifs et contextuels | FK vers hub/link + load_date | Attributs, load_date, record_source, hash_diff |

#### Exemple d'implementation / Implementation Example

```sql
-- Hub : identite unique d'un client
CREATE TABLE hub_customer (
    hub_customer_hk     BINARY(32) PRIMARY KEY,  -- Hash de la business key
    customer_bk         VARCHAR(50) NOT NULL,     -- Business key naturelle
    load_date           TIMESTAMP NOT NULL,
    record_source       VARCHAR(100) NOT NULL
);

-- Hub : identite unique d'une commande
CREATE TABLE hub_order (
    hub_order_hk        BINARY(32) PRIMARY KEY,
    order_bk            VARCHAR(50) NOT NULL,
    load_date           TIMESTAMP NOT NULL,
    record_source       VARCHAR(100) NOT NULL
);

-- Link : relation entre client et commande
CREATE TABLE link_customer_order (
    link_customer_order_hk  BINARY(32) PRIMARY KEY,  -- Hash des 2 hub HKs
    hub_customer_hk         BINARY(32) NOT NULL REFERENCES hub_customer,
    hub_order_hk            BINARY(32) NOT NULL REFERENCES hub_order,
    load_date               TIMESTAMP NOT NULL,
    record_source           VARCHAR(100) NOT NULL
);

-- Satellite : attributs du client (historises)
CREATE TABLE sat_customer_details (
    hub_customer_hk     BINARY(32) NOT NULL REFERENCES hub_customer,
    load_date           TIMESTAMP NOT NULL,
    load_end_date       TIMESTAMP,                -- NULL = record actif
    record_source       VARCHAR(100) NOT NULL,
    hash_diff           BINARY(32) NOT NULL,      -- Hash des attributs pour detecter les changements
    customer_name       VARCHAR(200),
    email               VARCHAR(255),
    segment             VARCHAR(50),
    city                VARCHAR(100),
    country             VARCHAR(50),
    PRIMARY KEY (hub_customer_hk, load_date)
);

-- Satellite : attributs de la commande
CREATE TABLE sat_order_details (
    hub_order_hk        BINARY(32) NOT NULL REFERENCES hub_order,
    load_date           TIMESTAMP NOT NULL,
    load_end_date       TIMESTAMP,
    record_source       VARCHAR(100) NOT NULL,
    hash_diff           BINARY(32) NOT NULL,
    order_status        VARCHAR(20),
    order_amount        DECIMAL(12,2),
    currency            VARCHAR(3),
    PRIMARY KEY (hub_order_hk, load_date)
);
```

### Data Vault 2.0 Patterns avances / Advanced Patterns

#### Point-in-Time (PIT) Tables

Les PIT tables sont des tables de performance qui pre-joignent les satellites d'un hub a chaque point dans le temps. Elles eliminent le besoin de sous-requetes complexes pour recuperer les attributs courants :

```sql
CREATE TABLE pit_customer AS
SELECT
    h.hub_customer_hk,
    snap.snapshot_date,
    sd.load_date AS details_load_date,
    se.load_date AS email_prefs_load_date
FROM hub_customer h
CROSS JOIN dim_date snap
LEFT JOIN sat_customer_details sd
    ON h.hub_customer_hk = sd.hub_customer_hk
    AND sd.load_date <= snap.snapshot_date
    AND (sd.load_end_date > snap.snapshot_date OR sd.load_end_date IS NULL)
LEFT JOIN sat_customer_email_prefs se
    ON h.hub_customer_hk = se.hub_customer_hk
    AND se.load_date <= snap.snapshot_date
    AND (se.load_end_date > snap.snapshot_date OR se.load_end_date IS NULL);
```

#### Bridge Tables

Les bridge tables pre-joignent les links et leurs hubs pour simplifier et accelerer les requetes analytiques. Elles servent d'interface entre la couche Data Vault (Raw Vault) et la couche Business Vault / presentation.

#### Business Vault

La couche Business Vault ajoute la logique metier au Raw Vault :
- **Computed Satellites** : satellites avec des attributs derives ou calcules (ex. : segment client base sur le CA cumule).
- **Business Links** : links crees par logique metier (pas directement issus des sources).
- **Reference Tables** : tables de reference partagees (codes pays, devises).

### Kimball vs Data Vault — Decision Matrix

| Critere | Kimball (Star/Snowflake) | Data Vault 2.0 |
|---|---|---|
| **Optimise pour** | Performance de requetage, self-service BI | Integration, historique complet, auditabilite |
| **Nombre de sources** | Peu de sources stables | Nombreuses sources heterogenes |
| **Historisation** | SCD Types (selective) | Historisation complete par defaut |
| **Agilite schema** | Changements couteux (impact sur les faits/dimensions) | Additif (ajout de hubs, links, satellites sans impact) |
| **Complexite** | Moyenne (intuitif pour les analystes) | Elevee (couche de presentation necessaire) |
| **Loading** | Transformation lourde a l'ingestion | Chargement rapide (insert-only), transformation en aval |
| **Cas d'usage ideal** | BI departementale, datasets stables | Enterprise data warehouse, compliance, multi-source |

### Architecture combinee recommandee / Recommended Combined Architecture

Dans le Modern Data Stack, combiner les approches :

```
Sources --> Ingestion (raw / bronze)
  --> Data Vault (raw vault + business vault) -- Integration et historisation
    --> Kimball star schemas (gold / marts) -- Presentation et BI
      --> Semantic layer --> BI tools
```

Cette architecture combine la flexibilite d'integration du Data Vault avec la performance de requetage du star schema Kimball. dbt est l'outil ideal pour implementer les transformations entre couches.

---

## Slowly Changing Dimensions (SCD)

### Vue d'ensemble des types SCD / SCD Types Overview

Les SCD gerent l'evolution des attributs dimensionnels dans le temps. Choisir le type adapte au besoin metier.

| Type | Comportement | Historique | Complexite | Cas d'usage |
|---|---|---|---|---|
| **Type 0** | Fixe (jamais de mise a jour) | Non | Nulle | Attributs immuables (date de naissance, code source) |
| **Type 1** | Ecrasement (overwrite) | Non | Faible | Corrections, attributs non historises |
| **Type 2** | Nouvelle ligne avec validite | Complet | Moyenne | Historique complet requis (segment client, adresse) |
| **Type 3** | Colonne valeur precedente | Partiel (1 version) | Faible | Historique limite a la derniere valeur |
| **Type 4** | Table d'historique separee | Complet (table separee) | Moyenne | Performance sur la dimension courante |
| **Type 6** | Hybride (1 + 2 + 3) | Complet + acces rapide | Elevee | Besoin de l'historique ET de la valeur courante sur chaque ligne |

### Implementation SCD Type 2 avec dbt

```sql
-- models/dimensions/dim_customer.sql
-- Utiliser le macro dbt snapshot pour SCD Type 2

{% snapshot snap_customer %}

{{
    config(
      target_schema='snapshots',
      unique_key='customer_id',
      strategy='check',
      check_cols=['customer_name', 'email', 'segment', 'city', 'country'],
      invalidate_hard_deletes=True,
    )
}}

SELECT
    customer_id,
    customer_name,
    email,
    segment,
    city,
    country,
    updated_at
FROM {{ source('raw', 'customers') }}

{% endsnapshot %}
```

```sql
-- models/marts/dim_customer.sql
-- Transformer le snapshot en dimension SCD Type 2

WITH snapshot_data AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['customer_id', 'dbt_valid_from']) }} AS customer_key,
        customer_id,
        customer_name,
        email,
        segment,
        city,
        country,
        dbt_valid_from  AS valid_from,
        dbt_valid_to    AS valid_to,
        CASE WHEN dbt_valid_to IS NULL THEN TRUE ELSE FALSE END AS is_current
    FROM {{ ref('snap_customer') }}
)

SELECT * FROM snapshot_data
```

### Implementation SCD Type 6 (Hybrid)

Le type 6 combine les types 1, 2 et 3 : historique complet (type 2) + valeur courante sur chaque ligne (type 1) + valeur precedente (type 3).

```sql
-- La dimension contient :
-- 1. Historique complet (lignes multiples, valid_from/valid_to) -- Type 2
-- 2. Valeur courante sur chaque ligne historique -- Type 1
-- 3. Valeur precedente -- Type 3

SELECT
    customer_key,
    customer_id,
    segment           AS segment_current,    -- Type 1 : toujours la valeur courante
    segment_previous,                         -- Type 3 : valeur precedente
    segment_historical,                       -- Type 2 : valeur de la periode
    valid_from,
    valid_to,
    is_current
FROM dim_customer_type6
```

---

## One Big Table (OBT) Pattern

### Definition et cas d'usage / Definition and Use Cases

Le pattern OBT consiste a pre-joindre toutes les dimensions a la fact table dans une seule table large et denormalisee. C'est l'approche la plus simple pour les moteurs colonnaires modernes.

#### Quand utiliser OBT / When to Use OBT

- **Equipe petite** : pas de resources pour maintenir un modele dimensionnel complet.
- **Moteur colonnaire** : Snowflake, BigQuery, ClickHouse gerent efficacement les tables larges.
- **Cas d'usage simple** : un seul processus metier, peu de dimensions, pas de drill-across.
- **BI outil simple** : Metabase, Superset — les outils qui ne gerent pas nativement les jointures multi-tables.
- **Prototypage rapide** : validation rapide d'un modele avant d'investir dans un star schema complet.

#### Quand eviter OBT / When to Avoid OBT

- **Donnees volumineuses** : la denormalisation extreme peut creer des tables de plusieurs TB.
- **Multi-processus** : quand plusieurs processus metier partagent les memes dimensions (besoin de conformed dimensions et de drill-across).
- **Historisation complexe** : la gestion des SCD est delicate dans un OBT.
- **Equipes multiples** : risque de logique metier dispersee dans des OBTs differents.

#### Implementation OBT avec dbt

```sql
-- models/marts/obt_orders.sql
-- One Big Table pour l'analyse des commandes

SELECT
    -- Facts
    o.order_id,
    o.order_date,
    o.order_quantity,
    o.unit_price,
    o.discount_amount,
    o.net_amount,
    o.total_amount,

    -- Customer dimensions (denormalisees)
    c.customer_id,
    c.customer_name,
    c.email,
    c.segment       AS customer_segment,
    c.city          AS customer_city,
    c.country       AS customer_country,

    -- Product dimensions (denormalisees)
    p.product_id,
    p.product_name,
    p.category      AS product_category,
    p.subcategory   AS product_subcategory,
    p.brand         AS product_brand,

    -- Date dimensions (denormalisees)
    d.full_date     AS order_full_date,
    d.day_name      AS order_day_name,
    d.month_name    AS order_month_name,
    d.quarter       AS order_quarter,
    d.year          AS order_year,
    d.is_weekend    AS order_is_weekend,

    -- Store dimensions
    s.store_name,
    s.store_city,
    s.store_region

FROM {{ ref('fct_orders') }} o
LEFT JOIN {{ ref('dim_customer') }} c ON o.customer_key = c.customer_key AND c.is_current = TRUE
LEFT JOIN {{ ref('dim_product') }} p ON o.product_key = p.product_key
LEFT JOIN {{ ref('dim_date') }} d ON o.date_key = d.date_key
LEFT JOIN {{ ref('dim_store') }} s ON o.store_key = s.store_key
```

---

## dbt Modeling Conventions

### Structure de projet recommandee / Recommended Project Structure

```
models/
├── staging/                    -- 1:1 avec les sources, nettoyage minimal
│   ├── source_crm/
│   │   ├── _source_crm.yml    -- Source definition + freshness
│   │   ├── stg_crm__customers.sql
│   │   └── stg_crm__contacts.sql
│   └── source_billing/
│       ├── _source_billing.yml
│       ├── stg_billing__subscriptions.sql
│       └── stg_billing__invoices.sql
├── intermediate/               -- Logique de transformation reutilisable
│   ├── int_customer_enriched.sql
│   └── int_order_items_pivoted.sql
├── marts/                      -- Modeles finaux pour la BI
│   ├── core/                   -- Dimensions et faits partages
│   │   ├── dim_customer.sql
│   │   ├── dim_product.sql
│   │   ├── dim_date.sql
│   │   └── fct_orders.sql
│   ├── marketing/              -- Marts specifiques au domaine
│   │   └── fct_campaign_performance.sql
│   └── finance/
│       └── fct_revenue.sql
└── metrics/                    -- Semantic layer definitions
    └── revenue_metrics.yml
```

### Conventions de nommage / Naming Conventions

| Couche | Prefix | Exemple | Description |
|---|---|---|---|
| **Staging** | `stg_` | `stg_crm__customers` | Source system + double underscore + entity |
| **Intermediate** | `int_` | `int_customer_enriched` | Transformations intermediaires |
| **Dimensions** | `dim_` | `dim_customer` | Dimension tables |
| **Facts** | `fct_` | `fct_orders` | Fact tables |
| **Metrics** | `mtr_` ou YAML | `mtr_revenue` | Metric definitions |
| **Snapshots** | `snap_` | `snap_customer` | SCD snapshots |

### Materialisation recommandee / Recommended Materialization

| Couche | Materialisation | Raison |
|---|---|---|
| **Staging** | `view` | Pas de stockage additionnel, toujours a jour |
| **Intermediate** | `ephemeral` ou `view` | Logic reutilisable sans materialisation |
| **Dimensions** | `table` | Performance, jointures frequentes |
| **Facts** | `incremental` | Volume important, ajout de nouvelles lignes |
| **OBT** | `table` ou `incremental` | Pre-jointure pour la BI |
| **Metrics** | depends on tool | Semantic layer, pas de materialisation directe |
