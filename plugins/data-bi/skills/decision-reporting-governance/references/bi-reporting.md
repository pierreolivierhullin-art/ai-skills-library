# BI & Reporting — Tools, Dashboard Design & KPI Frameworks

## Overview

Ce document de reference couvre les outils de Business Intelligence, les bonnes pratiques de conception de dashboards, le self-service BI, l'automatisation du reporting et les frameworks de KPIs. Utiliser ce guide pour choisir l'outil BI adapte, concevoir des tableaux de bord actionnables et etablir un framework de metriques robuste.

This reference document covers Business Intelligence tools, dashboard design best practices, self-service BI, reporting automation, and KPI frameworks. Use this guide to select the right BI tool, design actionable dashboards, and establish a robust metrics framework.

---

## BI Tools — In-Depth Comparison

### Power BI (Microsoft)

#### Forces et cas d'usage / Strengths and Use Cases
- **Integration Microsoft** : integration native avec Azure, Microsoft 365, Teams, SharePoint. Recommander pour les organisations fortement investies dans l'ecosysteme Microsoft.
- **DAX (Data Analysis Expressions)** : langage de mesures puissant permettant des calculs complexes (time intelligence, running totals, calculated columns). DAX est verbeux mais extremement flexible pour la modelisation de mesures.
- **Power Query (M language)** : editeur ETL visuel integre pour la preparation de donnees. Utile pour des transformations legeres, mais ne pas s'en servir comme pipeline ETL principal.
- **Dataflows & Datamarts** : couches de preparation et de stockage integrees pour le self-service. Les dataflows servent de couche de transformation partageable entre rapports.
- **Governance** : workspaces, deployment pipelines (dev/test/prod), row-level security (RLS), endorsement (certified/promoted datasets). Power BI Premium ajoute les paginated reports, le XMLA endpoint et le capacity-based licensing.

#### Limites / Limitations
- Modele de donnees en memoire (VertiPaq) : limite par la RAM disponible. Pour les tres grands volumes, utiliser le mode DirectQuery ou les composite models (import + DirectQuery).
- DAX a une courbe d'apprentissage significative pour les calculs avances.
- L'ecosysteme est ferme : difficile a integrer hors de Microsoft sans Premium.

#### Architecture recommandee
```
Sources --> Azure Data Factory / dbt --> Data Warehouse (Synapse/Fabric)
  --> Power BI Dataset (import ou DirectQuery)
    --> Power BI Report (visualisations)
      --> Power BI App (distribution)
```

### Tableau (Salesforce)

#### Forces et cas d'usage / Strengths and Use Cases
- **Visualisation avancee** : moteur VizQL exceptionnel pour l'exploration visuelle. Tableau excelle dans l'analyse exploratoire ad-hoc et les visualisations complexes (geospatiales, statistiques, multi-axes).
- **Tableau Prep** : outil visuel de preparation de donnees avec des capacites de nettoyage et de transformation drag-and-drop.
- **Tableau Cloud / Server** : deploiement cloud natif ou on-premise. Governance via projects, permissions, certified data sources.
- **Extensions et communaute** : vaste ecosysteme d'extensions, connecteurs et une communaute active (Tableau Public, Makeover Monday).
- **Tableau Pulse (2024-2026)** : insights automatiques par IA, metriques naturelles en langage naturel, alerting intelligent. Tendance forte vers l'analytics augmentee.

#### Limites / Limitations
- Cout eleve : licensing par utilisateur, pas de tier gratuit significatif.
- Semantic layer limitee : les calculs sont definis dans les workbooks, ce qui peut creer des incoherences entre rapports. Tableau Catalog (Data Management Add-on) ameliore la gouvernance mais ajoute un cout.
- Performance degradee sur les tres grands datasets sans extracts optimises.

#### Architecture recommandee
```
Sources --> dbt / ETL --> Cloud Data Warehouse (Snowflake, BigQuery, Redshift)
  --> Tableau Published Data Source (extracts ou live connection)
    --> Tableau Workbook (dashboards)
      --> Tableau Cloud/Server (distribution + governance)
```

### Looker (Google Cloud)

#### Forces et cas d'usage / Strengths and Use Cases
- **LookML** : langage de modelisation declaratif qui constitue une vraie semantic layer. LookML definit les mesures, dimensions, relations et logique metier dans un code versionnable (git). C'est le principal differenciateur de Looker : une source de verite unique pour les definitions metier.
- **Governed self-service** : les utilisateurs explorent les donnees dans le cadre defini par le modele LookML. Impossible de creer des metriques incoherentes si le modele est bien concu.
- **Integration Google Cloud** : natif avec BigQuery. Performances optimales sur BigQuery grace au pushdown SQL.
- **Looker Studio (ex-Data Studio)** : version gratuite et simplifiee pour les rapports legers et le partage externe. Ne pas confondre avec Looker (enterprise).
- **Embedded analytics** : SDK robuste pour integrer des visualisations et des explores dans des applications tierces.

#### Limites / Limitations
- Courbe d'apprentissage de LookML : necessite des competences developpeur (versionning, code review, testing).
- Lie a Google Cloud : bien que des connecteurs existent pour d'autres bases, les performances optimales sont sur BigQuery.
- Cout premium : positionnement enterprise, peu adapte aux petites structures.

#### Architecture recommandee
```
Sources --> dbt --> BigQuery (data warehouse)
  --> Looker LookML project (semantic layer, git-managed)
    --> Looker Explores + Dashboards (self-service)
      --> Looker Embedded / Looker API (integration)
```

### Metabase (Open Source)

#### Forces et cas d'usage / Strengths and Use Cases
- **Simplicite** : interface intuitive permettant aux utilisateurs non techniques de poser des "questions" sans SQL. Ideal pour la mise en place rapide de self-service BI dans des equipes de taille moyenne.
- **Open source** : deployment auto-heberge gratuit (Docker, JAR). Version Cloud payante avec SSO, audit, sandboxing.
- **SQL natif** : possibilite d'ecrire des requetes SQL natives pour les analyses avancees, avec parametrage dynamique (variables dans les filtres).
- **Models** : feature permettant de definir des modeles reutilisables (views SQL materilisees) pour centraliser la logique metier.
- **Embedding** : embedding via iframe ou SDK avec filtering cote serveur. Solution abordable pour l'embedded analytics.

#### Limites / Limitations
- Governance limitee : pas de semantic layer complete, pas de lineage natif, permissions basiques comparees a Power BI ou Looker.
- Performance : pas de moteur de cache avance, depend entierement de la base sous-jacente.
- Visualisations moins avancees que Tableau (pas de geo-spatial avance, statistiques limitees).

### Apache Superset (Open Source)

#### Forces et cas d'usage / Strengths and Use Cases
- **Open source & extensible** : entierement open source (Apache License 2.0), extensible via plugins Python. Deployer sur Kubernetes pour la scalabilite.
- **SQL-first** : concu pour les utilisateurs techniques confortables avec SQL. SQL Lab integre pour l'exploration ad-hoc.
- **Connecteurs multiples** : supporte 30+ bases de donnees via SQLAlchemy (Postgres, MySQL, Snowflake, BigQuery, ClickHouse, Trino, Druid, etc.).
- **Semantic layer basique** : metriques et dimensions definissables dans les datasets. Moins puissant que LookML mais suffisant pour des equipes techniques.
- **Caching** : integration Redis/Memcached pour le cache de requetes. Ameliore significativement les performances sur les dashboards frequemment accedes.

#### Limites / Limitations
- Interface moins polie que les solutions commerciales. L'experience utilisateur pour les profils non techniques est perfectible.
- Embedded analytics basique (iframe uniquement sans feature avancee de tenanting).
- Maintenance et operations : l'auto-hebergement requiert des competences DevOps.

---

## Dashboard Design — Best Practices

### Hierarchie visuelle / Visual Hierarchy

Organiser chaque dashboard selon une hierarchie claire. Appliquer les principes suivants :

1. **KPIs en premier** : placer les metriques cles en haut du dashboard dans des cartes KPI (big numbers). Limiter a 5-7 KPIs par vue. Chaque KPI doit afficher la valeur actuelle, la tendance (sparkline ou fleche), et la comparaison avec la periode precedente ou l'objectif.

2. **Pyramide inversee** : du general au specifique. Zone superieure = metriques de synthese. Zone intermediaire = graphiques de tendance et decomposition. Zone inferieure = detail et tableaux granulaires.

3. **Layout en Z ou F** : respecter les patterns de lecture naturels. Les informations les plus importantes en haut a gauche, les actions et filtres en haut ou sur un panneau lateral.

4. **Cohesion visuelle** : utiliser une palette de couleurs limitee (3-5 couleurs). Reserver le rouge et le vert pour les indicateurs de performance (pas pour la decoration). Appliquer une typographie coherente avec une hierarchie de taille (titre > sous-titre > label > detail).

### Types de graphiques et leur usage / Chart Type Selection

| Type | Cas d'usage | A eviter quand |
|---|---|---|
| **Bar chart** | Comparaison de categories | Plus de 15 categories |
| **Line chart** | Tendances temporelles | Donnees non chronologiques |
| **Stacked bar** | Composition de categories | Plus de 5 sous-categories |
| **Scatter plot** | Correlation entre 2 variables | Donnees non continues |
| **Pie / Donut** | Composition (parts de marche) | Plus de 5 segments |
| **Heatmap** | Patterns dans 2 dimensions | Utilisateurs non analytiques |
| **Table / Pivot** | Detail, export, recherche | Resume executif |
| **KPI card** | Metrique unique avec contexte | Besoin de tendance detaillee |
| **Waterfall** | Decomposition d'un total | Plus de 10 etapes |
| **Funnel** | Conversion, processus sequentiel | Etapes non sequentielles |
| **Treemap** | Hierarchie + proportion | Beaucoup de petits segments |
| **Gauge** | Progression vers un objectif unique | Multiples objectifs |

### Interactivite et filtrage / Interactivity and Filtering

- **Filtres globaux** : placer les filtres temporels et dimensionnels en position proeminente (header ou barre laterale). Toujours definir des valeurs par defaut pertinentes.
- **Cross-filtering** : activer le cross-filtering entre visualisations pour que la selection sur un graphique filtre les autres. Tester que les interactions sont coherentes et performantes.
- **Drill-down / Drill-through** : permettre de passer d'une vue agregee a une vue detaillee (ex. : clic sur une region pour voir les villes). Implementer via des liens de navigation ou des drill-through pages.
- **Tooltips enrichis** : afficher des informations contextuelles au survol (sparklines, valeurs complementaires, explications).
- **Bookmarks / Saved views** : permettre aux utilisateurs de sauvegarder leurs configurations de filtres pour un acces rapide.

### Performance des dashboards / Dashboard Performance

Optimiser les performances pour une experience utilisateur fluide :

- **Extracts vs Live connections** : utiliser des extracts (Tableau) ou le mode Import (Power BI) pour les dashboards consultes frequemment. Reserver les connexions live pour les donnees temps reel.
- **Aggregation tables** : pre-agreger les donnees au niveau de grain necessaire pour le dashboard. Un dashboard executif n'a pas besoin du grain transactionnel.
- **Incremental refresh** : configurer le rafraichissement incrementiel pour les grandes tables (ne recharger que les nouvelles donnees).
- **Query optimization** : surveiller les requetes generees par l'outil BI. Ajouter des index, materialiser les vues, utiliser des colonnes de partitionnement.
- **Caching** : activer le cache de requetes au niveau de l'outil BI et du data warehouse. Definir des TTL (time-to-live) adaptes a la fraicheur requise.

---

## Self-Service BI

### Principes du Self-Service gouverne / Governed Self-Service Principles

Le self-service BI ne signifie pas "chacun fait ce qu'il veut". Implementer un cadre structure :

1. **Certified datasets** : les Analytics Engineers creent des datasets certifies (marques, documentes, testes). Les utilisateurs metier construisent leurs analyses exclusivement sur ces datasets.

2. **Semantic layer** : centraliser les definitions de metriques dans une semantic layer (dbt metrics layer, Looker LookML, Cube.js, Power BI datasets certifies). Interdire la redefinition de metriques dans les rapports individuels.

3. **Training & enablement** : former les utilisateurs metier sur l'outil BI et les datasets disponibles. Proposer des templates de dashboards et des guides de bonnes pratiques. Mettre en place un programme de "Data Champions" dans chaque equipe metier.

4. **Guardrails techniques** : row-level security (RLS) pour limiter l'acces aux donnees sensibles. Data masking pour les PII. Query governors pour limiter la taille des requetes et eviter les full-table scans.

5. **Feedback loop** : mettre en place un canal de feedback pour que les utilisateurs signalent les incoherences, demandent de nouvelles metriques et suggerent des ameliorations. Traiter ces demandes dans un backlog priorise.

### Niveaux de self-service / Self-Service Maturity Levels

| Niveau | Description | Outils | Gouvernance |
|---|---|---|---|
| **L1 — Consommation** | Consulter des dashboards preconstruits | Tableau Viewer, Power BI App | Dashboards certifies, RLS |
| **L2 — Exploration** | Explorer les donnees dans des cadres definis | Looker Explore, Metabase Questions | Datasets certifies, semantic layer |
| **L3 — Creation** | Creer de nouveaux dashboards sur datasets certifies | Tableau Creator, Power BI Pro | Templates, guidelines, review process |
| **L4 — Modelisation** | Creer de nouveaux datasets et metriques | dbt, LookML, SQL | Code review, data contracts, CI/CD |

---

## Reporting Automation

### Scheduled Reports & Subscriptions

Automatiser la distribution des rapports pour eliminer le reporting manuel :

- **Email subscriptions** : configurer des envois planifies (quotidien, hebdomadaire, mensuel) avec des rapports en PDF ou en image. Tous les outils BI majeurs supportent cette fonctionnalite.
- **Slack/Teams integration** : envoyer les rapports et les alertes dans les canaux de communication de l'equipe. Power BI et Tableau offrent des integrations natives avec Teams/Slack.
- **Burst reporting** : generer et distribuer automatiquement des rapports personnalises par destinataire (region, equipe, client). Utile pour les rapports mensuels par manager ou les rapports clients.
- **Threshold-based alerts** : declencher des alertes quand un KPI depasse un seuil (chiffre d'affaires quotidien < objectif, taux d'erreur > 5%). Configurer dans l'outil BI ou dans un outil de monitoring dedie.

### Operational Reporting vs Analytical Reporting

| Critere | Operational Reporting | Analytical Reporting |
|---|---|---|
| **Frequence** | Temps reel a quotidien | Hebdomadaire a mensuel |
| **Audience** | Operations, support, equipes terrain | Management, analysts, executives |
| **Granularite** | Transactionnelle (detail) | Agregee (resume, tendances) |
| **Action** | Reaction immediate | Decision strategique |
| **Fraicheur** | Minutes a heures | Jours a semaines |
| **Outils** | Dashboards live, alertes, notifications | Rapports planifies, presentations |

---

## KPI Frameworks & Metric Trees

### Metric Tree Pattern

Decomposer chaque KPI strategique en un arbre de metriques operationnelles actionnables. Chaque feuille de l'arbre doit etre directement influencable par une equipe et mesurable.

```
Revenue (ARR)
├── New Revenue
│   ├── Number of new customers
│   │   ├── Leads generated (Marketing)
│   │   ├── Conversion rate (Sales)
│   │   └── Average deal size (Sales)
│   └── Expansion revenue
│       ├── Upsell rate (Customer Success)
│       └── Cross-sell rate (Product)
├── Retained Revenue
│   ├── Gross retention rate
│   │   ├── Churn rate (Customer Success)
│   │   └── Downgrade rate (Product)
│   └── Customer lifetime value (CLV)
└── Cost efficiency
    ├── Customer acquisition cost (CAC)
    ├── CAC payback period
    └── LTV/CAC ratio
```

### SMART KPI Definition Template

Pour chaque KPI, formaliser la definition avec les elements suivants :

| Champ | Description | Exemple |
|---|---|---|
| **Nom / Name** | Nom clair et non ambigu | Monthly Recurring Revenue (MRR) |
| **Definition** | Formule de calcul precise | Sum of all active subscription amounts at month end |
| **Source** | Table et champ source | `billing.subscriptions.amount` WHERE `status = 'active'` |
| **Grain** | Niveau de granularite | Monthly, per subscription |
| **Owner** | Equipe responsable | Finance / Revenue Operations |
| **Objectif / Target** | Valeur cible et horizon | 500K EUR by Q4 2026 |
| **Seuils / Thresholds** | Vert / Jaune / Rouge | Green: >= 100% target, Yellow: 80-99%, Red: < 80% |
| **Frequence** | Cadence de mise a jour | Daily refresh, monthly review |
| **Segmentations** | Axes de decomposition | By plan, by region, by cohort |

### Frameworks de KPIs standards / Standard KPI Frameworks

#### Balanced Scorecard (Kaplan & Norton)
Organiser les KPIs en 4 perspectives strategiques :
- **Financial** : revenue, profitability, cost efficiency, cash flow
- **Customer** : satisfaction (NPS, CSAT), retention, acquisition, share of wallet
- **Internal processes** : cycle time, quality, efficiency, innovation
- **Learning & Growth** : employee satisfaction, training, technology adoption

#### OKR (Objectives & Key Results)
Definir des objectifs qualitatifs ambitieux et les mesurer par des key results quantitatifs :
- **Objective** : "Devenir le leader de la satisfaction client dans notre marche" (qualitatif, inspirant)
- **KR1** : NPS passe de 45 a 65 d'ici Q2 (quantitatif, mesurable)
- **KR2** : Temps de resolution moyen reduit de 24h a 4h (quantitatif, mesurable)
- **KR3** : 90% des tickets resolus au premier contact (quantitatif, mesurable)

#### North Star Metric
Identifier la metrique unique qui capture la valeur fondamentale delivree aux clients :
- **SaaS B2B** : Weekly Active Users, or Activation Rate
- **E-commerce** : Weekly Purchases per Active Customer
- **Marketplace** : Gross Merchandise Volume (GMV) per Active Seller
- **Media** : Total Time Spent / Daily Active Users

Decomposer la North Star Metric en input metrics controlables par chaque equipe via un metric tree.

### Semantic Layer Implementation

#### dbt Metrics Layer
```yaml
# models/metrics/revenue_metrics.yml
metrics:
  - name: monthly_recurring_revenue
    label: "Monthly Recurring Revenue (MRR)"
    description: "Sum of all active subscription amounts at month end"
    type: simple
    type_params:
      measure: subscription_amount
    filter: |
      {{ Dimension('subscription__status') }} = 'active'
    time_grains: [day, week, month, quarter, year]
    dimensions:
      - plan_type
      - region
      - customer_segment

  - name: net_revenue_retention
    label: "Net Revenue Retention (NRR)"
    description: "Revenue from existing customers compared to same cohort prior period"
    type: derived
    type_params:
      expr: "current_period_revenue / prior_period_revenue"
      metrics:
        - name: current_period_revenue
          filter: |
            {{ Dimension('customer__is_existing') }} = true
        - name: prior_period_revenue
          offset_window: 1 month
```

#### Cube.js Semantic Layer
```javascript
// schema/Revenue.js
cube('Revenue', {
  sql_table: 'analytics.fct_revenue',

  measures: {
    mrr: {
      type: 'sum',
      sql: 'subscription_amount',
      title: 'Monthly Recurring Revenue',
      format: 'currency',
      filters: [{ sql: `${CUBE}.status = 'active'` }],
    },
    customer_count: {
      type: 'count_distinct',
      sql: 'customer_id',
      title: 'Active Customers',
    },
    arpu: {
      type: 'number',
      sql: `${mrr} / NULLIF(${customer_count}, 0)`,
      title: 'Average Revenue Per User',
      format: 'currency',
    },
  },

  dimensions: {
    plan_type: { sql: 'plan_type', type: 'string' },
    region: { sql: 'region', type: 'string' },
    signup_date: { sql: 'signup_date', type: 'time' },
  },
});
```

---

## Data Storytelling

### Structure d'un data story / Data Story Structure

Structurer chaque presentation de donnees comme un recit :

1. **Contexte / Setup** : rappeler l'objectif, le KPI suivi et la periode analysee. Accrocher l'attention avec un chiffre cle ou une tendance surprenante.

2. **Constat / Insight** : presenter les donnees factuelles. Montrer la tendance, la comparaison ou l'anomalie. Utiliser la visualisation la plus adaptee au message.

3. **Analyse / Why** : expliquer pourquoi. Decomposer le KPI pour identifier les drivers. Utiliser des decompositions (metric tree), des segmentations et des comparaisons temporelles.

4. **Recommandation / Action** : proposer des actions concretes basees sur l'analyse. Chaque recommandation doit etre actionnable, attribuee a une equipe et mesurable.

5. **Next steps** : definir les prochaines etapes, les responsables et les echeances. Anticiper les questions et les objections.

### Principes du data storytelling efficace

- **Un message par visualisation** : chaque graphique doit transmettre un message unique et clair. Ajouter un titre descriptif qui enonce le constat (ex. : "Le churn a augmente de 15% en Q3, porte par le segment PME" plutot que "Evolution du churn").
- **Annoter les visualisations** : ajouter des annotations pour guider la lecture (fleches, labels, zones de surbrillance). Ne pas laisser l'interpretation au hasard.
- **Comparer pour donner du contexte** : une metrique seule n'a pas de sens. Toujours comparer avec une reference : periode precedente, objectif, benchmark sectoriel, moyenne historique.
- **Eliminer le bruit** : supprimer tout element visuel non informatif (gridlines excessives, 3D, backgrounds decoratifs, legendes redondantes). Appliquer le principe de Tufte : maximiser le ratio data-ink.
