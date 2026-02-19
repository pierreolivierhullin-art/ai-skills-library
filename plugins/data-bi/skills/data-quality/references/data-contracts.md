# Data Contracts — Specification, Implementation et Gouvernance

## Vue d'Ensemble

Un data contract est un accord formel entre un producteur de donnees et ses consommateurs, specifiant la structure, la semantique, les SLOs de qualite et les modalites de changement. Introduit par Andrew Jones (2022) et popularise par Chad Sanderson, le data contract transforme les dependances implicites en engagements explicites — reduisant drastiquement les incidents lies aux breaking changes non coordonnes.

---

## Pourquoi les Data Contracts

### Le Probleme sans Contrat

```
Equipe Order Management
    └── Modifie la colonne "amount" en "amount_eur" (renommage "evident")
            |
            ↓ Pas de notification
Equipe Finance
    └── Requete SELECT amount FROM orders → ERREUR en production
            |
            ↓ 4 heures plus tard
Rapport mensuel CA → Chiffres faux → Decision strategique incorrecte
```

Sans contrat : les breaking changes se propagent silencieusement. Le temps de detection est long, le cout de correction est eleve, la confiance dans les donnees se degrade.

### La Solution avec Contrat

```
Equipe Order Management
    └── Renomme "amount" en "amount_eur" dans le contrat (version majeure : v1 → v2)
            |
            ↓ Validation CI/CD : alerte les consumers du breaking change
Equipe Finance (consumer enregistre)
    └── Recoit notification 30 jours avant la deprecation de v1
            |
            ↓ Met a jour ses requetes avant la date de deprecation
Rapport mensuel CA → Pas d'impact
```

---

## Standard de Specification — Open Data Contract Standard (ODCS)

ODCS (version 0.9.9, 2024) est le standard ouvert le plus adopte pour les data contracts. Format YAML, extensible.

### Structure Complete

```yaml
# ===== EN-TETE =====
dataContractSpecification: 0.9.9
id: orders-daily-v2                           # Identifiant unique
info:
  title: Orders Daily Aggregated
  version: 2.1.0
  status: active                               # active | deprecated | draft
  description: |
    Agregation quotidienne des commandes par client et categorie produit.
    Produit par le domaine Order Management.
    Consomme par : Finance (CA mensuel), Marketing (segmentation).
  owner: order-management-team
  contact:
    name: Marie Martin
    email: marie.martin@company.com
    channel: "#data-order-mgmt"               # Canal Slack
  tags:
    - orders
    - revenue
    - gold-layer
  links:
    documentation: "https://datahub.company.com/dataset/orders_daily"
    data_quality_report: "https://elementary.company.com/orders_daily"

# ===== SERVEURS =====
servers:
  production:
    type: bigquery
    project: prod-data-platform
    dataset: gold
    table: orders_daily
    environment: production
  staging:
    type: bigquery
    project: staging-data-platform
    dataset: gold_staging
    table: orders_daily
    environment: staging

# ===== TERMES D'USAGE =====
terms:
  usage: >
    Usage interne uniquement. Ne pas utiliser pour des reportings externes
    sans validation de l'equipe Finance.
  limitations: >
    Les commandes annulees dans les 2h suivant la passation sont exclues.
    Les commandes internationales hors zone Euro sont en EUR convertis au
    taux du jour de la commande (source: ECB).
  billing: internal-chargeback
  noticePeriod: P30D                          # 30 jours de notice pour breaking changes

# ===== MODELE DE DONNEES =====
models:
  orders_daily:
    description: "Une ligne par (customer_id, order_date)"
    type: table
    fields:
      order_date:
        type: date
        required: true
        description: "Date de la commande en UTC"
        example: "2025-03-15"
        constraints:
          - type: "not_null"
          - type: "date_range"
            min: "2020-01-01"
            max: "today"

      customer_id:
        type: string
        required: true
        description: "Identifiant unique du client (format: CUST-XXXXXXXX)"
        example: "CUST-12345678"
        pii: false                             # Pseudonymise
        constraints:
          - type: "not_null"
          - type: "pattern"
            value: "^CUST-[0-9]{8}$"

      revenue_eur:
        type: decimal
        precision: 18
        scale: 2
        required: true
        description: "Revenu total HT en EUR pour ce client ce jour"
        constraints:
          - type: "not_null"
          - type: "range"
            min: 0
            max: 1000000

      order_count:
        type: integer
        required: true
        description: "Nombre de commandes distinctes"
        constraints:
          - type: "not_null"
          - type: "range"
            min: 1

      product_category:
        type: string
        required: true
        description: "Categorie principale des produits commandes"
        constraints:
          - type: "not_null"
          - type: "enum"
            values: ["electronics", "clothing", "food", "home", "other"]

      order_status:
        type: string
        required: true
        description: "Statut dominant de la commande"
        constraints:
          - type: "enum"
            values: ["completed", "pending", "refunded"]

# ===== QUALITE DE DONNEES =====
quality:
  type: SodaCL
  specification:
    checks for orders_daily:
      - freshness(order_date) < 26h:
          name: "Table fraiche (SLO: donnees J-1 avant 6h)"
      - row_count > 50000:
          name: "Volume minimum"
      - row_count < 200000:
          name: "Volume maximum (detection duplicates)"
      - missing_count(customer_id) = 0:
          name: "customer_id jamais null"
      - duplicate_count(order_date, customer_id) = 0:
          name: "Unicite (order_date, customer_id)"
      - min(revenue_eur) >= 0:
          name: "Revenu non-negatif"
      - invalid_percent(product_category) < 0.5%:
          name: "Categories valides"

# ===== SLOs =====
servicelevels:
  availability:
    description: "Table disponible en production"
    percentage: 99.5%
    period: monthly
  freshness:
    description: "Donnees du J-1 disponibles avant 06h00 CET"
    threshold: 26h
    measurement: "last_modified timestamp"
  completeness:
    description: "customer_id jamais null"
    percentage: 100%
  uniqueness:
    description: "(order_date, customer_id) unique"
    percentage: 100%

# ===== HISTORIQUE DES VERSIONS =====
changelog:
  - version: 2.1.0
    date: 2025-06-01
    changes: "Ajout du champ order_status"
    type: minor
    breaking: false
  - version: 2.0.0
    date: 2025-01-15
    changes: "Renommage amount → revenue_eur, ajout product_category"
    type: major
    breaking: true
    migration: |
      Remplacer 'amount' par 'revenue_eur' dans toutes les requetes.
      Le contrat v1.x sera maintenu jusqu'au 2025-03-15.
  - version: 1.0.0
    date: 2024-03-01
    changes: "Creation du contrat"
    type: major
    breaking: false
```

---

## Validation Automatique en CI/CD

### GitHub Actions — Gate sur les Breaking Changes

```yaml
# .github/workflows/data-contract-check.yml
name: Data Contract Validation

on:
  pull_request:
    paths:
      - 'contracts/**/*.yaml'
      - 'models/**/*.sql'

jobs:
  validate-contracts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Historique complet pour la comparaison

      - name: Install datacontract-cli
        run: pip install datacontract-cli

      - name: Validate contract syntax
        run: |
          for f in contracts/**/*.yaml; do
            datacontract lint $f
          done

      - name: Check for breaking changes
        run: |
          # Comparer avec la version en production (branche main)
          git diff origin/main -- contracts/ | python scripts/detect_breaking_changes.py

      - name: Run quality tests
        env:
          BIGQUERY_PROJECT: ${{ secrets.BQ_STAGING_PROJECT }}
        run: |
          datacontract test contracts/orders-daily-v2.yaml \
            --server staging
```

```python
# scripts/detect_breaking_changes.py
import sys
import yaml
import re

def is_breaking_change(old_contract: dict, new_contract: dict) -> list:
    breaking = []

    old_fields = old_contract.get('models', {}).get('orders_daily', {}).get('fields', {})
    new_fields = new_contract.get('models', {}).get('orders_daily', {}).get('fields', {})

    # Colonnes supprimees
    for field in set(old_fields.keys()) - set(new_fields.keys()):
        breaking.append(f"Breaking: Column '{field}' was removed")

    # Changements de type
    for field in set(old_fields.keys()) & set(new_fields.keys()):
        old_type = old_fields[field].get('type')
        new_type = new_fields[field].get('type')
        if old_type != new_type:
            breaking.append(f"Breaking: Column '{field}' type changed: {old_type} → {new_type}")

        # required passe de false a true
        old_required = old_fields[field].get('required', False)
        new_required = new_fields[field].get('required', False)
        if not old_required and new_required:
            breaking.append(f"Breaking: Column '{field}' became required")

    return breaking

# Parse le diff git et comparer les contrats
# ...
```

### datacontract-cli — Outil de Reference

```bash
# Installation
pip install datacontract-cli

# Linting (validation syntaxique)
datacontract lint contracts/orders-daily-v2.yaml

# Test sur les donnees reelles
datacontract test contracts/orders-daily-v2.yaml \
  --server production \
  --bigquery-project prod-data-platform

# Generer la documentation HTML
datacontract export contracts/orders-daily-v2.yaml --format html > docs/orders-daily.html

# Comparer deux versions
datacontract diff contracts/orders-daily-v1.yaml contracts/orders-daily-v2.yaml

# Publier dans un catalogue (Datahub, OpenMetadata)
datacontract publish contracts/orders-daily-v2.yaml \
  --target datahub \
  --datahub-server https://datahub.company.com
```

---

## Gouvernance des Data Contracts

### Workflow de Creation d'un Nouveau Contrat

```
1. Producteur (equipe Order Management)
   → Redige le premier draft du contrat en YAML
   → Definit le schema, les SLOs, les termes d'usage

2. Revue par les consommateurs (equipes Finance, Marketing)
   → Valident les definitions semantiques
   → Verifient que les SLOs sont suffisants pour leurs besoins
   → Proposent des champs additionnels si necessaire

3. Validation DQ (Data Quality Engineer ou Data Steward)
   → Verifie que les contraintes de qualite sont measurables
   → S'assure que les SLOs sont atteignables

4. Approbation et Merge
   → PR review avec au moins 1 consommateur + 1 producteur
   → CI/CD valide le contrat (lint + test sur staging)
   → Merge dans main → publication dans le catalogue

5. Publication et Communication
   → Annonce dans le canal #data-contracts-updates
   → Catalogue mis a jour automatiquement
   → Consommateurs informes de l'existence du nouveau contrat
```

### Workflow de Breaking Change

```
Producteur detecte un besoin de breaking change
        |
        ↓
Creation d'une version majeure (ex: v1.x → v2.0)
        |
        ↓
Notification OBLIGATOIRE aux consommateurs
    (email auto + message Slack #data-contracts-updates)
    Message : "Breaking change prevu sur orders_daily, migration requise avant [date]"
        |
        ↓
Periode de transition (min 30 jours selon le contrat)
    - Les deux versions (v1 et v2) coexistent
    - v1 marquee "deprecated" dans le catalogue
    - Consommateurs migrent a leur rythme
        |
        ↓
Deprecation de v1 a la date annoncee
    - Alertes si des requetes utilisent encore v1 (detectees via lineage)
    - Periode de grace supplementaire si justifiee
        |
        ↓
Suppression de v1
```

### Matrice de Responsabilite (RACI)

| Activite | Producteur | Consommateur | Data Steward | Platform Team |
|---|---|---|---|---|
| Rediger le contrat | **R/A** | C | C | I |
| Valider les definitions semantiques | C | **R/A** | C | I |
| Valider les SLOs | **R/A** | C | C | I |
| Maintenir la conformite | **R/A** | I | C | I |
| Notifier les breaking changes | **R/A** | I | C | I |
| Gerer le catalogue | I | I | **R** | **A** |
| CI/CD validation | I | I | I | **R/A** |

---

## Anti-Patterns des Data Contracts

**Anti-pattern 1 : Contrats trop granulaires** :
Un contrat par colonne ou par partition cree une bureaucratie ingerable. Niveau correct : un contrat par data product (table ou vue materializee exposee aux consommateurs).

**Anti-pattern 2 : Contrats sans consommateurs enregistres** :
Un contrat sans liste de consommateurs connus ne peut pas notifier les breaking changes. Maintenir un registre des consommateurs actifs.

**Anti-pattern 3 : SLOs inatteignables** :
Un SLO de freshness < 1h pour un pipeline qui tourne toutes les 4h cree des alertes permanentes. Calibrer les SLOs sur ce qui est rellement atteignable + une marge.

**Anti-pattern 4 : Contrats jamais mis a jour** :
Si le contrat devient desynchronise de la realite (schema derive, SLOs non mesures), il perd sa valeur. Implémenter des verifications automatiques hebdomadaires : le contrat est-il toujours en accord avec le schema reel ?

**Anti-pattern 5 : "Contract washing"** :
Creer des contrats pour cocher une case sans changer les pratiques (pas de validation CI/CD, pas de notification des breaking changes, pas de monitoring des SLOs). Le contrat doit etre live et execute, pas un document statique.
