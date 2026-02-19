# Etudes de Cas — Data Quality en Production

## Vue d'Ensemble

Ces etudes de cas illustrent des implementations reelles de data quality : un programme data contracts dans une scale-up, la migration vers un data mesh dans un groupe industriel, la mise en place de data observability dans une fintech, et une crise qualite des donnees geree avec un playbook structure.

---

## Cas 1 — Programme Data Contracts dans une Scale-up SaaS (6 Mois)

### Contexte

Scale-up SaaS B2B (180 employes, 12 personnes dans l'equipe data). Probleme principal : 3-4 incidents de donnees par mois lies a des breaking changes non communiques entre equipes. Le dernier incident majeur avait rendu le dashboard CEO faux pendant 48h (colonne renommee par l'equipe Product sans notification). Impact : perte de confiance de la direction dans les donnees, et 2 jours de travail de remediation.

### Approche

**Phase 1 — Inventaire et priorisation (4 semaines)** :

Inventaire de tous les datasets gold et silver avec consommateurs connus. 23 data assets identifies. Priorisation sur 3 criteres :
- Nombre de consommateurs (> 3 equipes → prioritaire)
- Frequence de modification historique (> 1 changement/mois → risque)
- Impact business si faux (dashboard C-level, rapports reglementaires → critique)

8 datasets prioritaires identifies pour une implementation immediate.

**Phase 2 — Creation des premiers contrats (6 semaines)** :

Pour chaque dataset prioritaire :
1. Workshop de 2h avec le producteur et les consommateurs principaux
2. Redaction du contrat en YAML (schema, SLOs, termes)
3. Revue et signature (symbolique mais formelle) des parties prenantes
4. Integration dans le repo dbt avec CI/CD de validation

**Phase 3 — Outillage et automatisation (8 semaines)** :

- Mise en place de `datacontract-cli` dans le CI/CD GitHub Actions
- Alerte automatique Slack quand un PR modifie un contrat (canal #data-contract-changes)
- Periode de notification obligatoire de 21 jours avant tout breaking change (inscrite dans le processus de revue de PR)
- Elementary deploye pour le monitoring continu des SLOs des contrats

**Phase 4 — Generalisation (reste de l'annee)** :

- Formation de toutes les equipes productrices de data (demi-journee)
- Template de contrat dans la doc interne
- Objectif : 100% des data products gold avec un contrat d'ici fin d'annee

### Resultats (6 mois post-implementation)

| Indicateur | Avant | Apres | Delta |
|---|---|---|---|
| Incidents lies aux breaking changes | 3.5/mois | 0.4/mois | -89% |
| Temps de detection d'un incident | 6.2h | 0.8h | -87% |
| Temps de remediation | 11h | 2.5h | -77% |
| Score de confiance (survey trimestriel) | 52/100 | 78/100 | +50% |
| Couverture data contracts (gold layer) | 0% | 62% | +62 pts |

**ROI calcule** :
- Incidents evites : 3.1/mois × 13.5h/incident × 150 EUR/h = 6 300 EUR/mois economies
- Investissement (14 semaines de travail data engineer) : ~25 000 EUR
- Payback : 4 mois

**Lecon principale** : Le changement le plus impactant n'etait pas technique mais culturel — rendre obligatoire la notification de 21 jours avant breaking change. La technologie (CI/CD) permet juste d'appliquer cette regle automatiquement.

---

## Cas 2 — Migration Data Mesh dans un Groupe Industriel (18 Mois)

### Contexte

Groupe industriel (4 500 employes, 6 BUs distinctes — automobile, aeronautique, defense, energie, electronique, services). Equipe data centrale de 15 personnes completement submergee par les demandes des BUs. Delai moyen de livraison d'un nouveau rapport : 8 semaines. Frustration des BUs : "les donnees qu'on nous livre ne correspondent pas a ce qu'on a besoin".

### Architecture Cible

```
Data Platform Team (5 personnes) — enablement only
├── Infrastructure self-serve (Airbyte, dbt Cloud, Datahub)
├── Standards (naming, contrats, securite, qualite minimale)
└── Support tier 2 (pas de delivery)

Domaine Automobile (2 data engineers embeds)
├── sales_daily, inventory, quality_metrics
└── Data products consommes par Finance et Ventes Auto

Domaine Aeronautique (1 data engineer embed)
├── production_kpis, certification_tracking
└── Data products consommes par Operations et Reglementaire

[... 4 autres domaines ...]

Catalogue Datahub (commun a tous les domaines)
Data Guild (gouvernance — 1 representant par domaine)
```

### Deroulement de la Migration

**Mois 1-3 — Preparation et pilote** :
Selection du domaine pilote : Automobile (equipe data la plus mature, sponsor fort). Transfert de 2 data engineers vers l'equipe Automobile. Formation intensive data mesh pour les 2 data engineers (5 jours). Configuration de l'infrastructure self-serve (dbt Cloud, Airbyte, Datahub).

**Mois 4-6 — Deploiement pilote Automobile** :
Premiere version des data products Automobile en production avec contrats et SLOs. Feedback collecte : "le dbt Cloud self-serve fonctionne bien, mais les data engineers ne savaient pas comment definir les domaines de donnees". Formation DDD (Domain-Driven Design) organisee.

**Mois 7-12 — Extension progressive** :
Migration des domaines Aeronautique, Energie, Electronics. Chaque migration dure 6-8 semaines (formation + migration des pipelines + creation des data products + validation des SLOs).

**Mois 13-18 — Defense, Services + Consolidation** :
Migration des 2 derniers domaines. Mise en place de la Data Guild (reunions bimensuelles des data stewards). Bilan et optimisation.

### Resultats (18 mois)

| Indicateur | Avant | Apres |
|---|---|---|
| Delai livraison nouveau rapport | 8 semaines | 1.5 semaines |
| Tickets a l'equipe data centrale | 45/mois | 8/mois |
| Satisfaction BUs (survey) | 54/100 | 81/100 |
| Data products avec SLOs mesures | 0 | 47 |
| Incidents qualite avec impact business | 6/trimestre | 1.2/trimestre |
| Employes data dans les domaines | 0 | 11 (vs 0 avant) |

**Couts et ROI** :
- Infrastructure additionnelle : +80k EUR/an (dbt Cloud, Datahub)
- Embauche data engineers domaines : +4 postes a 70k EUR = 280k EUR/an
- Economies : equipe centrale reduite de 15 a 9 = -6 postes = -420k EUR/an
- Valeur metier (rapports plus rapides, decisions meilleures) : estimé +1.2M EUR/an
- **ROI net : +1.26M EUR/an**

**Obstacles rencontres** :
- La Defense avait des contraintes de securite (SI classifie) incompatibles avec le cloud central — solution : instance Datahub separee avec air gap
- Certains data engineers embeds dans les domaines se sentaient "trop isoles" de leurs pairs data — solution : Data Guild avec communaute de pratique mensuelle

---

## Cas 3 — Data Observability dans une Fintech Reglementee

### Contexte

Fintech de paiement (350 employes, 2 millions de transactions/jour). Obligation reglementaire ACPR : disponibilite des donnees de reporting a J+1 avant 09h00. Deux fois dans l'annee, le reporting ACPR avait ete livre en retard ou avec des anomalies — avec des avertissements de l'autorite de controle. Objectif : zero incident sur les donnees reglementaires.

### Architecture de Data Observability Deployee

**Couche 1 — Tests dbt (premiere ligne)** :
```yaml
# Tous les modeles alimentant les rapports ACPR
models:
  - name: regulatory_daily_positions
    meta:
      criticality: REGULATORY  # Tag special pour les tables reglementaires
    tests:
      - not_null:
          column_name: position_date
      - dbt_utils.recency:
          datepart: hour
          field: loaded_at
          interval: 22  # Alerte si table pas rafraichie depuis 22h
      - elementary.table_anomalies:
          anomaly_sensitivity: 2.5  # Plus sensible sur les tables reglementaires
      - expect_table_row_count_to_be_between:
          min_value: 1500000
          max_value: 3000000
```

**Couche 2 — Soda scans horaires** :
```yaml
# regulatory-checks.yml
checks for regulatory_daily_positions:
  - freshness(position_date) < 23h:
      name: "Fraicheur reglementaire"
      alert:
        when not between 20h and 23h
      fail:
        when > 23h
  - row_count between 1500000 and 3000000
  - missing_count(position_id) = 0
  - missing_count(counterparty_id) = 0
  - invalid_count(currency) = 0:
      valid values: [EUR, USD, GBP, JPY, CHF]
  - duplicate_count(position_id, position_date) = 0
```

**Couche 3 — Monte Carlo pour l'anomalie detection ML** :
Monte Carlo detecte les anomalies statistiques que les regles manuelles ne capturent pas : drift progressif de la distribution, correlations inhabituelles entre colonnes.

**Paging hierarchy** :
```
Test echoue dans dbt → Slack #data-quality-regulatory (alerte)
        |
        ↓ si non resolu dans 30 min
Soda scan alerte → PagerDuty (on-call data engineer)
        |
        ↓ si impact confirm sur le reporting ACPR
Monte Carlo alerte → PagerDuty + escalade au Head of Data
```

### Resultats (12 mois post-implementation)

- Zero incident de reporting ACPR manque ou retarde
- Temps de detection moyen des anomalies : 23 min (vs 4h avant)
- Faux positifs : 2.3/semaine (acceptable — chacun resolu en < 15 min en moyenne)
- Cout de l'outillage (Monte Carlo + Soda Pro) : 42k EUR/an
- Cout d'un incident reglementaire (estimation conservatrice) : > 200k EUR (temps + avertissement + audit)
- ROI : protege contre 3+ incidents potentiels/an = >> 600k EUR de valeur

---

## Cas 4 — Crise Qualite Geree avec un Playbook

### Contexte

E-commerce (90M EUR de CA, 25 personnes data). Mardi 08h35 : l'equipe Finance signale que le rapport de CA de la veille montre une baisse de 42% vs la meme periode — impossible pour un lundi ordinaire. Le rapport est deja arrive au CFO.

### Chronologie de la Gestion de Crise

**08h35 — Alert** : Signalement via le canal Slack #data-incidents (equipe Finance).

**08h37 — Activation du playbook** : Le Data Engineer d'astreinte prend le ticket et l'escalade au niveau 2 (Head of Data en copie).

**08h45 — Diagnostic rapide** :
- Verification de la fraicheur : orders_daily charge correctement (freshness = OK)
- Verification du volume : 47 800 lignes (vs baseline de 52 000 — -8%, dans les tolerances)
- Verification des tests dbt : TOUS PASSES. Le probleme n'est pas dans les tests existants.

**08h52 — Root cause analysis via lineage** :
- Remonter dans le lineage : orders_daily ← orders_silver ← orders_raw
- Verifier orders_raw : colonne "total_amount" presente
- Verifier orders_silver : colonne "revenue_eur" presente
- Verifier orders_daily : colonne "revenue_eur" presente

**09h05 — Discovery** :
Nouvelle feature deployee en production la veille : les remises (discounts) sont maintenant deduits de "total_amount" dans la source. Le CA affiche est donc le CA net de remises, pas le CA brut. Le CA a bien baisse de 42% en "net remises" parce que la campagne promotionnelle a commence la veille.

En realite : le CA brut etait normal. C'etait une question de definition, pas une anomalie de donnees.

**09h15 — Communication** :
Message au CFO et a la Finance : "Le rapport est correct — il reflete le CA net de remises suite a un changement dans le systeme source. Le CA brut est normal. Voici les deux chiffres cote a cote."

**09h30 — Post-mortem schedule** :
Cause racine : le changement dans le systeme source n'a pas ete communique a l'equipe data. La definition de "CA" dans le rapport n'etait pas documentee dans le data catalog.

**Actions correctives** :
1. Data contract cree pour orders_daily incluant la definition explicite de "revenue_eur" (CA net de remises ou brut ?)
2. Process: tout changement de la source orders doit notifier l'equipe data via un ticket JIRA standard
3. Rapport CA mis a jour pour afficher les deux : CA brut ET CA net
4. Alerte de changement definitif de metrique (si CA net < 70% de CA brut → alerte sur une anomalie de remise inhabituellement haute)

**Lecon principale** : La plupart des "incidents de donnees" ne sont pas des bugs techniques — ce sont des problemes de definition et de communication entre les equipes qui produisent et consomment les donnees. Les data contracts et le catalogue reduisent ce type d'incident en rendant les definitions explicites et partagees.
