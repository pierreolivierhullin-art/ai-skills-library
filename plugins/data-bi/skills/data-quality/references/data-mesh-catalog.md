# Data Mesh & Data Catalog — Architecture et Implementation

## Vue d'Ensemble

Le data mesh (Zhamak Dehghani, 2019) est une approche architecturale et organisationnelle qui decentralise la propriete et la responsabilite des donnees vers les domaines metier. Le data catalog est l'infrastructure de decouverte qui rend ce paradigme viable a grande echelle : sans catalogue, le data mesh devient un archipel de data silos. Les deux concepts sont complementaires et indissociables en pratique.

---

## Data Mesh — Implementation Pratique

### Principe 1 : Domain Ownership — Comment l'Organiser

**Identification des domaines data** :

Un domaine data est une equipe ou un groupe d'equipes avec une responsabilite metier coherente. Les domaines emergent naturellement des bounded contexts du DDD (Domain-Driven Design).

```
Exemple : Scale-up e-commerce (200 employes)

Domaine Customer
├── Source-aligned data products
│   ├── customer_events (stream Kafka en temps reel)
│   └── customer_profiles_raw (snapshot quotidien)
└── Consumer-aligned data products
    ├── customer_360 (vue consolidee)
    └── customer_segments (segmentation ML)

Domaine Order
├── Source-aligned data products
│   ├── order_events (stream)
│   └── orders_raw (snapshot)
└── Consumer-aligned data products
    ├── orders_daily (agrege)
    └── revenue_by_product

Domaine Finance
├── Consomme : orders_daily, customer_segments
└── Produit : p_and_l_monthly, budget_vs_actual

Domaine Marketing
├── Consomme : customer_360, orders_daily
└── Produit : campaign_performance, marketing_roi
```

**Checklist du domain ownership** :
- [ ] Chaque data product a un owner nomme (pas une equipe anonyme)
- [ ] L'owner est disponible pour repondre aux questions des consommateurs (SLA de reponse defini)
- [ ] L'equipe owner controle le pipeline de production du data product
- [ ] L'equipe owner est alertee en premier en cas d'incident qualite

### Principe 2 : Data as a Product — La Difference en Pratique

**Data product vs table** :

| Dimension | Simple table | Data product |
|---|---|---|
| Owner | Personne / equipe inconnue | Owner nomme et responsable |
| Documentation | Peu ou pas | Description, schema, exemples, cas d'usage |
| SLOs | Aucun | Freshness, completude, unicite mesures |
| Versioning | Pas de convention | Versionnee (v1, v2...) avec changelog |
| Contrat | Pas de contrat | Data contract signe avec les consommateurs |
| Decouverte | Connaissance tribale | Publie dans le catalogue |
| Acces | Acces direct ou indirect | Interface stable avec documentation |

**Anatomie d'un Data Product** :

```yaml
# data-product.yaml — customer_360
id: customer-360-v1
domain: customer
name: Customer 360
version: 1.4.0
owner: customer-domain-team
steward: data-steward@company.com

description: |
  Vue unifiee du client integrant les donnees CRM, comportement produit,
  et historique d'achat. Reference pour toute analyse client.

classification:
  sensitivity: internal          # public | internal | confidential | restricted
  pii: pseudonymized             # yes | no | pseudonymized | anonymized
  retention: 2_years

ports:
  output:
    - name: bigquery_table
      type: bigquery
      location: prod-platform.gold.customer_360
      contract: contracts/customer-360-v1.yaml
    - name: rest_api
      type: rest
      endpoint: https://data-api.company.com/v1/customers

slos:
  freshness: "< 24h"
  availability: "99.5%"
  completeness: "email_address null < 5%"

tags: [customer, 360, gold, analytical]
```

### Principe 3 : Self-Serve Infrastructure — Ce que la Platform Team Doit Fournir

La platform team (anciennement "central data team") dans un data mesh ne produit plus de data products — elle cree l'infrastructure qui permet aux domaines de le faire eux-memes.

**Catalogue de services self-serve** :

| Service | Outil | Description |
|---|---|---|
| Ingestion self-serve | Airbyte, Fivetran | Connecter une source sans help de la plateforme |
| Transformation | dbt templates, dbt Cloud | Creer des modeles dbt avec CI/CD inclus |
| Orchestration | Airflow (hosted), Prefect Cloud | Scheduler ses propres pipelines |
| Catalogue | Datahub, OpenMetadata | Publier et decouvrir des data products |
| Monitoring qualite | Elementary, Soda | Instrumenter la qualite sans dev specifique |
| Acces et securite | Column-level security, row filters | Appliquer les politiques d'acces automatiquement |

**Developer Experience pour les domaines** :

```bash
# Exemple : creer un nouveau data product avec un template
data-platform create-product \
  --domain customer \
  --name customer_events \
  --type streaming \
  --source postgres://crm-db/customers

# Scaffold genere :
# ├── data-product.yaml
# ├── contracts/customer-events-v1.yaml
# ├── dbt/models/customer/customer_events.sql
# ├── dbt/models/customer/schema.yml
# └── airflow/dags/customer_events_dag.py
```

### Principe 4 : Federated Computational Governance

**Ce que la Data Guild centralise** :
- Standards de naming (naming conventions pour les tables, les colonnes, les data products)
- Template de data contract (format ODCS standard)
- Politique de classification des donnees (public, interne, confidentiel, restreint)
- Metriques de qualite minimales (chaque data product doit avoir au moins : freshness, volume, unicite)
- Politique de retention (durees de conservation par niveau de classification)
- Regles de securite (qui peut acceder a quoi, par role)

**Ce que la Data Guild ne centralise pas** :
- Les transformations metier (chaque domaine les definit)
- Les SLOs specifiques (au-dessus du minimum mandatory)
- Le rythme de mise a jour
- Les outils de transformation (dans les limites des outils approuves)

---

## Data Catalog — Implementation

### Datahub (LinkedIn, open source)

Datahub est le catalogue open source le plus complet. Architecture : un graphe de metadonnees central avec des connecteurs automatiques vers les sources de donnees.

**Architecture** :
```
Sources de metadonnees
├── BigQuery (schema auto-discover)
├── dbt (lineage + description des modeles)
├── Airflow (pipeline lineage)
├── Looker / Tableau (rapport lineage)
└── Custom (via Python SDK ou REST API)
        |
        ↓ [Ingestion via GMS - Generalized Metadata Service]
Datahub GMS (metadata store)
    ├── Search index (Elasticsearch)
    ├── Graph (Neo4j ou en memoire)
    └── Storage (MySQL ou Postgres)
        |
        ↓
Datahub Frontend (React UI)
    ├── Recherche par mot-cle
    ├── Vue lineage interactive
    ├── Profil de donnees (statistiques)
    └── Documentation collaborative
```

**Ingestion automatique depuis dbt** :
```yaml
# datahub-ingest.yaml
source:
  type: dbt
  config:
    manifest_path: ./target/manifest.json
    catalog_path: ./target/catalog.json
    sources_path: ./target/sources.json
    target_platform: bigquery
    target_platform_instance: prod-data-platform
    include_column_lineage: true
    include_descriptions: true

sink:
  type: datahub-rest
  config:
    server: "https://datahub.company.com"
    token: ${DATAHUB_GMS_TOKEN}
```

```bash
# Ingestion en une commande
datahub ingest -c datahub-ingest.yaml
```

**Python SDK pour les metadonnees custom** :
```python
from datahub.emitter.mce_builder import make_dataset_urn
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import (
    DatasetPropertiesClass,
    OwnershipClass,
    OwnerClass,
    OwnershipTypeClass,
)

emitter = DatahubRestEmitter("https://datahub.company.com", token=TOKEN)

# Definir le proprietaire d'un dataset
dataset_urn = make_dataset_urn("bigquery", "prod-platform.gold.customer_360")

ownership = OwnershipClass(
    owners=[
        OwnerClass(
            owner="urn:li:corpGroup:customer-domain-team",
            type=OwnershipTypeClass.DATAOWNER,
        )
    ]
)

properties = DatasetPropertiesClass(
    description="Vue unifiee du client — voir data-product.yaml pour les details",
    customProperties={
        "domain": "customer",
        "data_product_version": "1.4.0",
        "slo_freshness": "24h",
        "data_contract": "contracts/customer-360-v1.yaml",
    },
    tags=["gold", "customer", "analytical"],
)

emitter.emit_mces([...])
```

### OpenMetadata (open source)

Alternative moderne a Datahub, avec une UI plus conviviale et une integration native des data contracts.

**Avantages vs Datahub** :
- Interface plus moderne et intuitive
- Data quality integree (Great Expectations, dbt tests visibles directement)
- Data contracts en beta native
- Installation plus simple (Docker Compose)

```bash
# Demarrage rapide
git clone https://github.com/open-metadata/OpenMetadata
cd OpenMetadata
./bootstrap/bootstrap_storage.sh init
python openmetadata_ingestion/setup.py install

# Ingestion BigQuery
metadata ingest -c ingestion_config/bigquery_config.yaml
```

---

## Data Quality Score — Mesurer la Sante du Catalogue

### Score de Qualite par Data Product

```python
def calculate_data_product_score(data_product: dict) -> dict:
    """
    Score composite sur 5 dimensions (0-100 par dimension)
    """
    scores = {}

    # 1. Documentation (0-20 pts)
    doc_score = 0
    doc_score += 5 if data_product.get('description') else 0
    doc_score += 5 if data_product.get('owner') else 0
    doc_score += 5 if all(f.get('description') for f in data_product.get('fields', {}).values()) else 0
    doc_score += 5 if data_product.get('tags') else 0
    scores['documentation'] = doc_score

    # 2. Freshness (0-20 pts)
    last_update = get_last_update(data_product['id'])
    slo_hours = parse_slo_freshness(data_product.get('slos', {}).get('freshness', '48h'))
    hours_since_update = (datetime.now() - last_update).total_seconds() / 3600
    scores['freshness'] = 20 if hours_since_update < slo_hours else max(0, 20 - int(hours_since_update - slo_hours))

    # 3. Qualite (0-20 pts) — basé sur les résultats des tests
    test_results = get_latest_test_results(data_product['id'])
    pass_rate = test_results['passed'] / test_results['total'] if test_results['total'] > 0 else 0
    scores['quality'] = int(pass_rate * 20)

    # 4. Contrat (0-20 pts)
    contract_score = 0
    contract_score += 10 if data_product.get('contract') else 0
    contract_score += 5 if data_product.get('contract_version') else 0
    contract_score += 5 if data_product.get('consumers_registered') else 0
    scores['contract'] = contract_score

    # 5. Lineage (0-20 pts)
    lineage_score = 0
    lineage_score += 10 if data_product.get('upstream_lineage') else 0
    lineage_score += 10 if data_product.get('downstream_lineage') else 0
    scores['lineage'] = lineage_score

    scores['total'] = sum(scores.values())
    return scores
```

**Dashboard de sante du catalogue** :

| Data Product | Documentation | Freshness | Qualite | Contrat | Lineage | TOTAL |
|---|---|---|---|---|---|---|
| customer_360 | 18/20 | 20/20 | 19/20 | 20/20 | 20/20 | **97/100** |
| orders_daily | 15/20 | 20/20 | 17/20 | 20/20 | 20/20 | **92/100** |
| revenue_forecast | 10/20 | 15/20 | 12/20 | 10/20 | 15/20 | **62/100** |
| ad_hoc_analysis | 5/20 | 0/20 | 5/20 | 0/20 | 5/20 | **15/100** |

Seuil minimum pour un data product en production : 70/100. En dessous : plan d'amelioration obligatoire avec l'owner.

---

## Anti-Patterns du Data Mesh

**"Data mesh theatre"** : Renommer les equipes "domaine X" sans changer les responsabilites, les processus et les incentives. Le data mesh necessite un transfert reel de responsabilite — pas juste d'organigramme.

**"Pas assez grand pour le data mesh"** : Le data mesh est adapte aux organisations avec au moins 5 domaines data actifs et une equipe data centrale de plus de 10 personnes. En dessous, un data warehouse centralise bien gouverne est souvent plus efficace.

**"Le catalogue comme fin en soi"** : Remplir le catalogue est une activite de maintenance, pas une fin. Si les data scientists ne l'utilisent pas pour decouvrir des datasets, le catalogue ne sert pas son objectif. Mesurer l'utilisation du catalogue, pas uniquement son remplissage.

**"Pas de data platform team"** : Sans equipe plateforme qui fournit les outils self-serve, chaque domaine reinvente la roue. Le data mesh ne supprime pas la plateforme centrale — il en change le role.
