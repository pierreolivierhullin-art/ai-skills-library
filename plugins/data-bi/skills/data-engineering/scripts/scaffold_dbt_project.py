#!/usr/bin/env python3
"""
scaffold_dbt_project.py
------------------------
Crée la structure complète d'un projet dbt avec architecture Medallion
(bronze / silver / gold).

Structure générée :
  <project>/
  ├── dbt_project.yml
  ├── profiles.yml
  ├── README.md
  ├── models/
  │   ├── bronze/          ← Ingestion brute (sources)
  │   │   └── sources.yml
  │   ├── silver/          ← Nettoyage, typage, déduplication
  │   │   ├── _silver.yml
  │   │   └── stg_<project>__example.sql
  │   └── gold/            ← Agrégations métier, marts
  │       ├── _gold.yml
  │       └── mart_<project>__example.sql
  ├── tests/
  │   └── generic/
  ├── macros/
  │   └── utils.sql
  ├── seeds/
  │   └── .gitkeep
  ├── snapshots/
  │   └── .gitkeep
  └── analyses/
      └── .gitkeep

Adapters supportés : bigquery | snowflake | postgres | redshift | duckdb

Usage :
  python3 scaffold_dbt_project.py [nom_projet] [adapter]

Exemples :
  python3 scaffold_dbt_project.py mon_projet bigquery
  python3 scaffold_dbt_project.py analytics_platform snowflake
  python3 scaffold_dbt_project.py local_dev duckdb
"""

import os
import sys
import textwrap
from pathlib import Path
from datetime import date

# ---------------------------------------------------------------------------
# Adapters supportés
# ---------------------------------------------------------------------------

SUPPORTED_ADAPTERS = {
    "bigquery":  "dbt-bigquery",
    "snowflake": "dbt-snowflake",
    "postgres":  "dbt-postgres",
    "redshift":  "dbt-redshift",
    "duckdb":    "dbt-duckdb",
}

ADAPTER_PROFILES = {
    "bigquery": """\
{project_name}:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth                      # ou service-account
      project: your-gcp-project-id      # MODIFIER
      dataset: {project_name}_dev
      threads: 4
      timeout_seconds: 300
      location: EU                       # ou US
      # keyfile: /path/to/service_account.json  # si method: service-account
    prod:
      type: bigquery
      method: service-account
      project: your-gcp-project-id      # MODIFIER
      dataset: {project_name}_prod
      threads: 8
      timeout_seconds: 600
      location: EU
      keyfile: /path/to/service_account.json  # MODIFIER
""",

    "snowflake": """\
{project_name}:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: your_account.region      # MODIFIER (ex: xy12345.eu-west-1)
      user: your_user                   # MODIFIER
      password: "{{ env_var('DBT_SNOWFLAKE_PASSWORD') }}"
      role: TRANSFORMER                 # MODIFIER
      database: {project_name_upper}_DEV
      warehouse: COMPUTE_WH
      schema: public
      threads: 4
      client_session_keep_alive: false
    prod:
      type: snowflake
      account: your_account.region      # MODIFIER
      user: dbt_prod_user               # MODIFIER
      password: "{{ env_var('DBT_SNOWFLAKE_PASSWORD_PROD') }}"
      role: TRANSFORMER
      database: {project_name_upper}_PROD
      warehouse: COMPUTE_WH_PROD
      schema: public
      threads: 8
      client_session_keep_alive: false
""",

    "postgres": """\
{project_name}:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost                   # MODIFIER
      user: dbt_user                   # MODIFIER
      password: "{{ env_var('DBT_POSTGRES_PASSWORD') }}"
      port: 5432
      dbname: {project_name}_dev       # MODIFIER
      schema: public
      threads: 4
      keepalives_idle: 0
      connect_timeout: 10
      search_path: public
    prod:
      type: postgres
      host: your-prod-host             # MODIFIER
      user: dbt_prod_user              # MODIFIER
      password: "{{ env_var('DBT_POSTGRES_PASSWORD_PROD') }}"
      port: 5432
      dbname: {project_name}_prod      # MODIFIER
      schema: public
      threads: 8
""",

    "redshift": """\
{project_name}:
  target: dev
  outputs:
    dev:
      type: redshift
      host: your-cluster.region.redshift.amazonaws.com  # MODIFIER
      user: dbt_user             # MODIFIER
      password: "{{ env_var('DBT_REDSHIFT_PASSWORD') }}"
      port: 5439
      dbname: {project_name}_dev
      schema: public
      threads: 4
      ra3_node: true
    prod:
      type: redshift
      host: your-cluster.region.redshift.amazonaws.com  # MODIFIER
      user: dbt_prod_user
      password: "{{ env_var('DBT_REDSHIFT_PASSWORD_PROD') }}"
      port: 5439
      dbname: {project_name}_prod
      schema: public
      threads: 8
      ra3_node: true
""",

    "duckdb": """\
{project_name}:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: '{project_name}_dev.duckdb'
      threads: 4
    prod:
      type: duckdb
      path: '{project_name}_prod.duckdb'
      threads: 8
""",
}


# ---------------------------------------------------------------------------
# Contenu des fichiers
# ---------------------------------------------------------------------------

def dbt_project_yml(project_name: str, adapter: str) -> str:
    return f"""\
# dbt_project.yml — {project_name}
# Généré par scaffold_dbt_project.py le {date.today().isoformat()}
#
# Documentation : https://docs.getdbt.com/reference/dbt_project.yml

name: '{project_name}'
version: '1.0.0'
config-version: 2

profile: '{project_name}'

# Chemins des ressources (conventions dbt par défaut)
model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

# Répertoire de compilation / exécution
target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

# ────────────────────────────────────────────────
# Configuration des modèles par couche Medallion
# ────────────────────────────────────────────────
models:
  {project_name}:

    # BRONZE — Données brutes, ingestion fidèle
    # Matérialisées en VIEW pour économiser le stockage (pas de transformation)
    bronze:
      +materialized: view
      +schema: bronze
      +tags: ["bronze", "raw"]
      +docs:
        show: true

    # SILVER — Nettoyage, typage, déduplication
    # Matérialisées en TABLE pour performance et isoler la logique de nettoyage
    silver:
      +materialized: table
      +schema: silver
      +tags: ["silver", "staging"]
      +docs:
        show: true

    # GOLD — Agrégations métier, data marts
    # Matérialisées en TABLE ; utiliser incremental pour les grandes tables
    gold:
      +materialized: table
      +schema: gold
      +tags: ["gold", "mart"]
      +docs:
        show: true

# ────────────────────────────────────────────────
# Configuration des seeds
# ────────────────────────────────────────────────
seeds:
  {project_name}:
    +schema: seeds
    +tags: ["seed"]

# ────────────────────────────────────────────────
# Configuration des snapshots
# ────────────────────────────────────────────────
snapshots:
  {project_name}:
    +schema: snapshots
    +tags: ["snapshot"]
    +strategy: timestamp           # ou check
    +updated_at: updated_at        # colonne de timestamp de mise à jour

# ────────────────────────────────────────────────
# Variables de projet (surchargeables via CLI)
# ────────────────────────────────────────────────
vars:
  # Fenêtre d'incrément par défaut pour les modèles incrementaux
  start_date: '2020-01-01'

  # Suffixe d'environnement (dev / prod)
  env_suffix: ''

  # Activer/désactiver les tests de qualité lourds en dev
  run_heavy_tests: false
"""


def profiles_yml(project_name: str, adapter: str) -> str:
    template = ADAPTER_PROFILES.get(adapter, ADAPTER_PROFILES["postgres"])
    return f"""\
# profiles.yml — {project_name}
# Généré par scaffold_dbt_project.py le {date.today().isoformat()}
#
# IMPORTANT : Ce fichier contient des credentials. NE PAS committer en l'état.
# Placer dans ~/.dbt/profiles.yml ou utiliser des variables d'environnement.
# Documentation : https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles

{template.format(
    project_name=project_name,
    project_name_upper=project_name.upper()
)}
"""


def sources_yml(project_name: str) -> str:
    return f"""\
# models/bronze/sources.yml
# Déclaration des sources de données brutes.
# Ces sources correspondent aux tables chargées par votre outil d'ingestion
# (Fivetran, Airbyte, custom ingestion scripts).
#
# Convention de nommage :
#   - source name  : nom du système source (ex: salesforce, postgres_app)
#   - table name   : nom exact de la table dans la source
#
# Documentation : https://docs.getdbt.com/docs/build/sources

version: 2

sources:

  # ── Exemple : base de données applicative (PostgreSQL / MySQL) ──────────
  - name: app_db
    description: >
      Base de données de l'application principale.
      Chargée via Airbyte dans le schéma raw_app_db.
    database: "{{{{ env_var('DBT_SOURCE_DATABASE', '{project_name}_dev') }}}}"
    schema: raw_app_db               # Modifier selon votre setup
    loader: airbyte                  # airbyte | fivetran | custom
    loaded_at_field: _loaded_at      # Champ de timestamp d'ingestion (freshnesscheck)

    # Contrôle de fraîcheur des données (data freshness)
    freshness:
      warn_after:  {{count: 12, period: hour}}
      error_after: {{count: 24, period: hour}}

    tables:
      - name: users
        description: "Table des utilisateurs de l'application."
        columns:
          - name: id
            description: "Identifiant unique de l'utilisateur."
            tests:
              - not_null
              - unique
          - name: email
            description: "Adresse email (PII - ne pas exposer en gold)."
            tests:
              - not_null
          - name: created_at
            description: "Date de création du compte."
            tests:
              - not_null
          - name: updated_at
            description: "Date de dernière mise à jour."

      - name: orders
        description: "Table des commandes."
        columns:
          - name: id
            tests:
              - not_null
              - unique
          - name: user_id
            tests:
              - not_null
              - relationships:
                  to: source('app_db', 'users')
                  field: id
          - name: status
            tests:
              - not_null
              - accepted_values:
                  values: ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
          - name: amount_cents
            description: "Montant en centimes (éviter les flottants)."
            tests:
              - not_null
          - name: created_at
            tests:
              - not_null

      - name: products
        description: "Catalogue produits."
        columns:
          - name: id
            tests:
              - not_null
              - unique
          - name: name
            tests:
              - not_null
          - name: price_cents
            tests:
              - not_null

  # ── Exemple : outil CRM (Salesforce via Fivetran) ───────────────────────
  - name: salesforce
    description: >
      Données CRM Salesforce chargées via Fivetran.
      Schéma : raw_salesforce.
    schema: raw_salesforce
    loader: fivetran
    loaded_at_field: _fivetran_synced

    freshness:
      warn_after:  {{count: 6, period: hour}}
      error_after: {{count: 12, period: hour}}

    tables:
      - name: account
        description: "Comptes Salesforce (entreprises clientes)."
        columns:
          - name: id
            tests:
              - not_null
              - unique
          - name: name
            tests:
              - not_null
          - name: _fivetran_deleted
            description: "True si l'enregistrement a été supprimé dans Salesforce."

      - name: opportunity
        description: "Opportunités commerciales."
        columns:
          - name: id
            tests:
              - not_null
              - unique
          - name: account_id
            tests:
              - not_null
          - name: stage_name
            tests:
              - not_null
          - name: amount
            description: "Montant de l'opportunité en devise locale."
          - name: close_date
            tests:
              - not_null
"""


def silver_yml(project_name: str) -> str:
    return f"""\
# models/silver/_silver.yml
# Documentation et tests des modèles Silver (staging / nettoyage).
#
# Convention de nommage Silver :
#   stg_<source>__<entity>.sql
#   ex: stg_app_db__users.sql, stg_salesforce__opportunities.sql
#
# Rôle de la couche Silver :
#   - Renommer les colonnes selon la convention snake_case
#   - Caster les types (string → date, cents → float, etc.)
#   - Dédupliquer (en conservant l'enregistrement le plus récent)
#   - Filtrer les enregistrements supprimés (_fivetran_deleted)
#   - Appliquer les tests de qualité fondamentaux (not_null, unique, relationships)
#   - NE PAS appliquer de logique métier (réservé à Gold)

version: 2

models:

  - name: stg_{project_name}__example
    description: >
      Modèle de staging exemple pour le projet {project_name}.
      Source : app_db.orders — Nettoyage et typage des commandes.
    config:
      materialized: table
      tags: ["silver", "staging", "orders"]
    columns:
      - name: order_id
        description: "Clé primaire de la commande (surrogate key)."
        tests:
          - not_null
          - unique
      - name: user_id
        description: "Identifiant de l'utilisateur ayant passé la commande."
        tests:
          - not_null
      - name: order_status
        description: "Statut normalisé de la commande."
        tests:
          - not_null
          - accepted_values:
              values: ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
      - name: order_amount_eur
        description: "Montant de la commande converti en EUR (depuis centimes)."
        tests:
          - not_null
      - name: created_at
        description: "Timestamp de création de la commande (UTC)."
        tests:
          - not_null
      - name: updated_at
        description: "Timestamp de dernière mise à jour (UTC)."
"""


def silver_example_sql(project_name: str) -> str:
    return f"""\
-- models/silver/stg_{project_name}__example.sql
-- Modèle Silver : nettoyage et staging des commandes.
--
-- Source    : {{ source('app_db', 'orders') }}
-- Cible     : schéma silver
-- Fréquence : batch quotidien (ou incrémental sur created_at)
--
-- Transformations appliquées :
--   1. Renommage des colonnes → convention snake_case explicite
--   2. Cast des types (amount_cents → amount_eur en NUMERIC)
--   3. Filtrage des enregistrements invalides (amount <= 0)
--   4. Normalisation du status (upper → lower)

{{{{
  config(
    materialized = 'incremental',
    unique_key   = 'order_id',
    on_schema_change = 'sync_all_columns',
    -- Partitionnement (BigQuery / Snowflake) :
    -- partition_by = {{"field": "created_at", "data_type": "timestamp", "granularity": "day"}},
    -- cluster_by   = ['user_id', 'order_status']
  )
}}}}

with

source as (

    select * from {{{{ source('app_db', 'orders') }}}}

    -- Filtre incrémental : ne traiter que les nouvelles lignes en mode incremental
    {{%- if is_incremental() %}}
    where updated_at > (select max(updated_at) from {{{{ this }}}})
    {{%- endif %}}

),

renamed as (

    select
        -- Identifiants
        id                                          as order_id,
        user_id,

        -- Montant : conversion centimes → euros avec précision NUMERIC
        round(cast(amount_cents as numeric) / 100, 2)  as order_amount_eur,

        -- Statut normalisé en minuscules
        lower(trim(status))                         as order_status,

        -- Timestamps castés en UTC
        cast(created_at as timestamp)               as created_at,
        cast(updated_at as timestamp)               as updated_at,

        -- Métadonnées de chargement
        _loaded_at

    from source

),

filtered as (

    select *
    from renamed
    where
        -- Écarter les commandes avec un montant invalide
        order_amount_eur > 0

        -- Écarter les enregistrements sans timestamp de création
        and created_at is not null

)

select * from filtered
"""


def gold_yml(project_name: str) -> str:
    return f"""\
# models/gold/_gold.yml
# Documentation et tests des modèles Gold (data marts).
#
# Convention de nommage Gold :
#   mart_<domaine>__<entité>.sql
#   ex: mart_sales__daily_revenue.sql, mart_customers__cohorts.sql
#
# Rôle de la couche Gold :
#   - Agréger les données Silver en métriques métier
#   - Construire des dimensions et des faits (star schema si besoin)
#   - Alimenter les dashboards, les APIs analytiques, et le semantic layer
#   - Appliquer la logique métier (définitions officielles des KPIs)
#   - Matérialiser en TABLE ou en INCREMENTAL selon le volume

version: 2

models:

  - name: mart_{project_name}__example
    description: >
      Data mart exemple : agrégation quotidienne du chiffre d'affaires par statut.
      Alimenté par stg_{project_name}__example.
      Consommateurs : dashboard BI, rapport hebdomadaire direction.
    config:
      materialized: table
      tags: ["gold", "mart", "revenue"]
    columns:
      - name: order_date
        description: "Date de la commande (granularité : jour)."
        tests:
          - not_null
      - name: order_status
        description: "Statut de la commande."
        tests:
          - not_null
      - name: order_count
        description: "Nombre de commandes pour ce jour / statut."
        tests:
          - not_null
      - name: total_revenue_eur
        description: "Chiffre d'affaires total en EUR."
        tests:
          - not_null
      - name: avg_order_value_eur
        description: "Valeur moyenne des commandes en EUR."
"""


def gold_example_sql(project_name: str) -> str:
    return f"""\
-- models/gold/mart_{project_name}__example.sql
-- Data Mart : agrégation quotidienne du CA par statut de commande.
--
-- Source    : silver.stg_{project_name}__example
-- Cible     : schéma gold
-- Fréquence : batch quotidien
-- Consommateurs : dashboard BI, reporting direction
--
-- Définition officielle des KPIs :
--   - total_revenue_eur : somme des commandes DELIVERED (hors annulées)
--   - avg_order_value_eur : moyenne sur les commandes DELIVERED uniquement

{{{{
  config(
    materialized = 'table',
    -- Pour les grandes tables, utiliser incremental :
    -- materialized = 'incremental',
    -- unique_key   = ['order_date', 'order_status'],
    -- on_schema_change = 'sync_all_columns',
  )
}}}}

with

orders as (

    select * from {{{{ ref('stg_{project_name}__example') }}}}

),

daily_revenue as (

    select
        cast(created_at as date)    as order_date,
        order_status,

        count(*)                    as order_count,
        sum(order_amount_eur)       as total_revenue_eur,
        avg(order_amount_eur)       as avg_order_value_eur,
        min(order_amount_eur)       as min_order_value_eur,
        max(order_amount_eur)       as max_order_value_eur

    from orders
    group by 1, 2

),

final as (

    select
        order_date,
        order_status,
        order_count,
        round(total_revenue_eur,    2)  as total_revenue_eur,
        round(avg_order_value_eur,  2)  as avg_order_value_eur,
        round(min_order_value_eur,  2)  as min_order_value_eur,
        round(max_order_value_eur,  2)  as max_order_value_eur,

        -- Métriques cumulées (window functions)
        sum(total_revenue_eur) over (
            order by order_date
            rows between unbounded preceding and current row
        )                               as cumulative_revenue_eur

    from daily_revenue

)

select * from final
order by order_date desc, order_status
"""


def macros_utils_sql(project_name: str) -> str:
    return f"""\
-- macros/utils.sql
-- Bibliothèque de macros utilitaires pour le projet {project_name}.
-- Ces macros sont disponibles dans tous les modèles via {{{{ macro_name() }}}}.

-- ──────────────────────────────────────────────────────────────────────────
-- generate_surrogate_key
-- Génère une clé surrogate déterministe à partir de plusieurs colonnes.
-- Usage : {{{{ generate_surrogate_key(['col1', 'col2']) }}}}
-- ──────────────────────────────────────────────────────────────────────────
{{%- macro generate_surrogate_key(column_names) -%}}
    {{{{- dbt_utils.generate_surrogate_key(column_names) -}}}}
{{%- endmacro -%}}


-- ──────────────────────────────────────────────────────────────────────────
-- cents_to_currency
-- Convertit un montant en centimes vers une devise flottante.
-- Usage : {{{{ cents_to_currency('amount_cents') }}}}
-- ──────────────────────────────────────────────────────────────────────────
{{%- macro cents_to_currency(column_name, precision=2) -%}}
    round(cast({{{{ column_name }}}} as numeric) / 100, {{{{ precision }}}})
{{%- endmacro -%}}


-- ──────────────────────────────────────────────────────────────────────────
-- current_timestamp_utc
-- Retourne le timestamp actuel en UTC (compatibilité multi-adapter).
-- Usage : {{{{ current_timestamp_utc() }}}}
-- ──────────────────────────────────────────────────────────────────────────
{{%- macro current_timestamp_utc() -%}}
    {{%- if target.type == 'bigquery' -%}}
        current_timestamp()
    {{%- elif target.type == 'snowflake' -%}}
        convert_timezone('UTC', current_timestamp())::timestamp_ntz
    {{%- else -%}}
        now() at time zone 'utc'
    {{%- endif -%}}
{{%- endmacro -%}}


-- ──────────────────────────────────────────────────────────────────────────
-- is_incremental_run
-- Macro de logging pour le mode d'exécution.
-- Usage : {{{{ log(is_incremental_run(), info=true) }}}}
-- ──────────────────────────────────────────────────────────────────────────
{{%- macro is_incremental_run() -%}}
    {{%- if is_incremental() -%}}
        "Mode incremental : traitement des nouvelles lignes uniquement."
    {{%- else -%}}
        "Mode full refresh : reconstruction complète de la table."
    {{%- endif -%}}
{{%- endmacro -%}}


-- ──────────────────────────────────────────────────────────────────────────
-- safe_divide
-- Division sécurisée qui retourne NULL (et non une erreur) si dénominateur = 0.
-- Usage : {{{{ safe_divide('numerator', 'denominator') }}}}
-- ──────────────────────────────────────────────────────────────────────────
{{%- macro safe_divide(numerator, denominator) -%}}
    case
        when {{{{ denominator }}}} = 0 or {{{{ denominator }}}} is null
        then null
        else {{{{ numerator }}}} / {{{{ denominator }}}}
    end
{{%- endmacro -%}}
"""


def readme_md(project_name: str, adapter: str) -> str:
    pkg = SUPPORTED_ADAPTERS.get(adapter, "dbt-core")
    return f"""\
# {project_name} — Projet dbt

Généré par `scaffold_dbt_project.py` le {date.today().isoformat()}.

## Architecture Medallion

```
Sources brutes
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│  BRONZE  — Ingestion fidèle, vues sur les données brutes        │
│  Schéma : bronze  │  Matérialisation : VIEW                     │
│  Transformations : aucune (miroir de la source)                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  SILVER  — Nettoyage, typage, déduplication                     │
│  Schéma : silver  │  Matérialisation : TABLE / INCREMENTAL      │
│  Transformations : renommage, cast, filtres, dédup              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  GOLD    — Agrégations métier, data marts                       │
│  Schéma : gold    │  Matérialisation : TABLE / INCREMENTAL      │
│  Consommateurs : dashboards BI, APIs analytiques, reporting     │
└─────────────────────────────────────────────────────────────────┘
```

## Prérequis

```bash
pip install dbt-core {pkg}
```

## Configuration

1. Copier `profiles.yml` dans `~/.dbt/profiles.yml`
2. Mettre à jour les credentials (host, user, password, project, etc.)
3. Utiliser des variables d'environnement pour les secrets :
   ```bash
   export DBT_{project_name.upper()}_PASSWORD="votre_mot_de_passe"
   ```

## Commandes de base

```bash
# Vérifier la connexion
dbt debug

# Installer les packages dbt (dbt_utils, etc.)
dbt deps

# Compiler les modèles sans exécuter
dbt compile

# Exécuter tous les modèles
dbt run

# Exécuter les tests de données
dbt test

# Exécuter models + tests en une commande
dbt build

# Sélectionner un sous-ensemble de modèles
dbt run --select silver          # Couche Silver uniquement
dbt run --select tag:gold        # Modèles taggés "gold"
dbt run --select +mart_{project_name}__example  # Et toutes ses dépendances

# Mode incremental (ne traite que les nouvelles lignes)
dbt run --select stg_{project_name}__example

# Full refresh (reconstruire toute la table)
dbt run --full-refresh --select stg_{project_name}__example

# Générer et servir la documentation
dbt docs generate
dbt docs serve
```

## Conventions de nommage

| Couche  | Préfixe      | Exemple                          |
|---------|--------------|----------------------------------|
| Bronze  | _(source)_   | `sources.yml`                    |
| Silver  | `stg_`       | `stg_app_db__orders.sql`         |
| Gold    | `mart_`      | `mart_sales__daily_revenue.sql`  |
| Macros  | _(libre)_    | `utils.sql`, `date_spine.sql`    |

## Structure du projet

```
{project_name}/
├── dbt_project.yml      # Configuration principale du projet
├── profiles.yml         # Connexion à la base de données (NE PAS committer)
├── models/
│   ├── bronze/          # Déclarations de sources (sources.yml)
│   ├── silver/          # Modèles de staging (stg_*.sql)
│   └── gold/            # Data marts (mart_*.sql)
├── tests/               # Tests génériques custom
├── macros/              # Macros réutilisables (utils.sql)
├── seeds/               # Données de référence statiques (CSV)
└── snapshots/           # Snapshots SCD Type 2
```

## CI/CD recommandé

```yaml
# .github/workflows/dbt.yml (exemple GitHub Actions)
- name: dbt build (slim CI)
  run: |
    dbt build --select state:modified+ --defer --state ./prod_artifacts
```

## Ressources

- [dbt documentation](https://docs.getdbt.com/)
- [dbt best practices](https://docs.getdbt.com/guides/best-practices)
- [dbt-utils](https://hub.getdbt.com/dbt-labs/dbt_utils/latest/)
"""


# ---------------------------------------------------------------------------
# Scaffold principal
# ---------------------------------------------------------------------------

def scaffold(project_name: str, adapter: str):
    base = Path(project_name)

    if base.exists():
        print(f"[ATTENTION] Le répertoire '{project_name}/' existe déjà.")
        answer = input("Continuer et écraser les fichiers existants ? [o/N] ").strip().lower()
        if answer not in ("o", "oui", "y", "yes"):
            print("Annulation.")
            sys.exit(0)

    # Arborescence de répertoires
    dirs = [
        base,
        base / "models" / "bronze",
        base / "models" / "silver",
        base / "models" / "gold",
        base / "tests" / "generic",
        base / "macros",
        base / "seeds",
        base / "snapshots",
        base / "analyses",
        base / "target",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Fichiers à créer
    files = {
        base / "dbt_project.yml":
            dbt_project_yml(project_name, adapter),

        base / "profiles.yml":
            profiles_yml(project_name, adapter),

        base / "README.md":
            readme_md(project_name, adapter),

        base / "models" / "bronze" / "sources.yml":
            sources_yml(project_name),

        base / "models" / "silver" / "_silver.yml":
            silver_yml(project_name),

        base / "models" / "silver" / f"stg_{project_name}__example.sql":
            silver_example_sql(project_name),

        base / "models" / "gold" / "_gold.yml":
            gold_yml(project_name),

        base / "models" / "gold" / f"mart_{project_name}__example.sql":
            gold_example_sql(project_name),

        base / "macros" / "utils.sql":
            macros_utils_sql(project_name),

        base / "seeds" / ".gitkeep":        "",
        base / "snapshots" / ".gitkeep":    "",
        base / "analyses" / ".gitkeep":     "",
        base / "target" / ".gitignore":     "*\n!.gitignore\n",
    }

    # .gitignore racine
    gitignore_content = textwrap.dedent("""\
        target/
        dbt_packages/
        logs/
        .DS_Store
        *.pyc
        profiles.yml
    """)
    files[base / ".gitignore"] = gitignore_content

    # packages.yml (dépendances dbt)
    packages_content = textwrap.dedent(f"""\
        # packages.yml — {project_name}
        # Dépendances du projet dbt.
        # Installer avec : dbt deps
        #
        # Documentation : https://hub.getdbt.com/

        packages:
          - package: dbt-labs/dbt_utils
            version: [">=1.0.0", "<2.0.0"]

          # Décommenter pour les tests de qualité avancés :
          # - package: calogica/dbt_expectations
          #   version: [">=0.10.0", "<0.11.0"]

          # Décommenter pour l'audit trail :
          # - package: dbt-labs/audit_helper
          #   version: [">=0.12.0", "<0.13.0"]
    """)
    files[base / "packages.yml"] = packages_content

    # Écriture des fichiers
    created = []
    for path, content in files.items():
        path.write_text(content, encoding="utf-8")
        created.append(str(path))

    return base, created


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage : python3 scaffold_dbt_project.py <nom_projet> [adapter]")
        print(f"Adapters : {' | '.join(SUPPORTED_ADAPTERS.keys())}")
        sys.exit(1)

    project_name = sys.argv[1].strip().lower().replace("-", "_").replace(" ", "_")
    adapter      = sys.argv[2].strip().lower() if len(sys.argv) > 2 else "postgres"

    if adapter not in SUPPORTED_ADAPTERS:
        print(f"[ERREUR] Adapter '{adapter}' non supporté.")
        print(f"Adapters disponibles : {', '.join(SUPPORTED_ADAPTERS.keys())}")
        sys.exit(1)

    print(f"\nScaffolding dbt project '{project_name}' avec adapter '{adapter}'...")
    base, created = scaffold(project_name, adapter)

    print(f"\n[OK] Projet dbt cree : {base.resolve()}/")
    print(f"\nFichiers generes ({len(created)}) :")
    for f in sorted(created):
        print(f"  {f}")

    pkg = SUPPORTED_ADAPTERS[adapter]
    print(f"\nProchaines etapes :")
    print(f"  1. pip install dbt-core {pkg}")
    print(f"  2. Copier {base}/profiles.yml dans ~/.dbt/profiles.yml")
    print(f"  3. Configurer les credentials dans ~/.dbt/profiles.yml")
    print(f"  4. cd {base} && dbt debug")
    print(f"  5. dbt deps   (installe dbt_utils et autres packages)")
    print(f"  6. dbt build  (compile + execute + teste)")
    print(f"\nDocumentation : {base}/README.md")


if __name__ == "__main__":
    main()
