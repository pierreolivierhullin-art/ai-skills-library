# Études de Cas — Architectures Cloud en Production

## Vue d'Ensemble

Ces études de cas illustrent la conception et l'implémentation d'infrastructures cloud dans différents contextes : migration, greenfield, multi-cloud, et optimisation FinOps.

---

## Cas 1 — Migration Cloud-Native pour une Scale-up E-Commerce (AWS)

### Contexte

Plateforme e-commerce B2C avec 1.2 millions de commandes/mois, infrastructure on-premise vieillissante (serveurs physiques co-localisés). Temps de déploiement : 3 semaines. Disponibilité en production : 97.2% (2.8% de downtime). Objectif : passer à 99.9% de disponibilité et réduire le temps de déploiement à < 1 heure.

### Architecture Cible

**Stack retenu** : AWS (équipe habituée à l'écosystème AWS, plusieurs certifications AWS)

**Composants clés** :
- **Compute** : ECS Fargate (pas de gestion de nodes EC2) avec auto-scaling
- **Base de données** : Aurora PostgreSQL (3 AZs, réplication automatique)
- **Cache** : ElastiCache Redis (sessions, cache produits)
- **Stockage** : S3 (images, médias, exports)
- **CDN** : CloudFront avec comportements de cache différenciés
- **Réseau** : VPC avec 3 AZs, subnets publics/privés/data

**IaC** : Terraform avec modules réutilisables, state dans S3 + DynamoDB locking

**CI/CD** : GitHub Actions → ECR → ECS (déploiement blue-green via CodeDeploy)

### Migration en 3 Phases

**Phase 1 — Fondations (6 semaines)** :
- Provisionnement du VPC, subnets, IAM, S3 pour les logs et state Terraform
- Configuration Aurora PostgreSQL avec migration de données via AWS DMS
- Tests de performance : Aurora vs. PostgreSQL on-premise (Aurora 2.3x plus rapide sur les requêtes complexes)

**Phase 2 — Containerisation (4 semaines)** :
- Dockerisation de l'application (image de 180MB après optimisation multi-stage)
- Configuration ECS Task Definitions et Services
- Mise en place du CI/CD avec GitHub Actions (build → push ECR → deploy ECS)
- Environnement staging opérationnel, tests de charge réussis (600 req/sec soutenues)

**Phase 3 — Bascule Production (2 semaines)** :
- Shadow deployment : production on-premise + ECS en parallèle pendant 1 semaine
- Bascule DNS progressive via Route 53 weighted routing (10% → 50% → 100%)
- Monitoring CloudWatch avec dashboards et alertes

### Résultats

| Métrique | Avant | Après | Delta |
|---|---|---|---|
| Disponibilité | 97.2% | 99.92% | +2.72 points |
| Temps de déploiement | 3 semaines | 18 minutes | -99.6% |
| Temps de réponse P99 | 1.8s | 380ms | -78% |
| Coût mensuel infrastructure | 28k EUR | 19k EUR | -32% |
| Capacité max (req/sec) | 120 | 800+ | +567% |

**FinOps** : L'équipe avait surestimé les besoins initiaux. Après 2 mois de monitoring, rightsizing des Fargate tasks (-30% mémoire allouée) et achat de 1-year Reserved Instances pour Aurora — économie additionnelle de 3.2k EUR/mois.

---

## Cas 2 — Infrastructure Data Platform sur GCP (Greenfield)

### Contexte

Scale-up de fintech (200 personnes) construisant une data platform from scratch pour alimenter des dashboards analytiques, des modèles de scoring crédit, et des rapports réglementaires (ACPR). Stack technique de l'équipe engineering : Python, dbt, Airflow.

### Choix du Cloud Provider

**Décision : GCP**, justifiée par :
- BigQuery comme data warehouse (serverless, pas de gestion de cluster, SQL standard)
- Vertex AI pour les modèles de scoring (besoin ML natif)
- Bonne intégration avec dbt (BigQuery adapter mature)
- Cloud Run pour les APIs de serving des modèles (pas de K8s à gérer)

### Architecture Retenue

```
Sources → Cloud Storage (GCS) → Airflow (Cloud Composer) → BigQuery
                                      ↓                           ↓
                                   dbt Cloud           Vertex AI (scoring)
                                      ↓                           ↓
                              BigQuery (marts)          Cloud Run (API)
                                      ↓
                               Looker Studio
```

**IaC Terraform** :

```hcl
# Structure des projets GCP (un projet par environnement)
# gcp-fintech-dev, gcp-fintech-staging, gcp-fintech-production

resource "google_project" "data_platform" {
  name       = "fintech-data-${var.env}"
  project_id = "fintech-data-${var.env}"
  org_id     = var.org_id

  labels = {
    environment = var.env
    team        = "data"
    managed_by  = "terraform"
  }
}

# BigQuery datasets par couche medallion
resource "google_bigquery_dataset" "bronze" {
  project    = google_project.data_platform.project_id
  dataset_id = "bronze"
  location   = "EU"
  description = "Données brutes ingérées (immuables)"

  # Rétention des données
  default_table_expiration_ms = var.env != "production" ? 604800000 : null  # 7 jours en dev

  labels = { layer = "bronze", managed_by = "terraform" }
}

resource "google_bigquery_dataset" "silver" {
  project    = google_project.data_platform.project_id
  dataset_id = "silver"
  location   = "EU"
  description = "Données nettoyées et conformées"
  labels     = { layer = "silver" }
}

resource "google_bigquery_dataset" "gold" {
  project    = google_project.data_platform.project_id
  dataset_id = "gold"
  location   = "EU"
  description = "Agrégations métier et marts analytiques"
  labels     = { layer = "gold" }
}
```

### Sécurité et Conformité ACPR

Contraintes réglementaires pour les données financières :
- Données localisées en EU (BigQuery dataset location = "EU")
- Audit logging activé sur tous les accès BigQuery
- Chiffrement avec Cloud KMS (clés gérées par le client)
- VPC Service Controls pour isoler BigQuery du réseau public

```hcl
# Organisation Policy pour forcer la localisation EU des données
resource "google_organization_policy" "restrict_data_location" {
  org_id     = var.org_id
  constraint = "constraints/gcp.resourceLocations"

  list_policy {
    allow {
      values = ["in:eu-locations"]
    }
  }
}

# Audit logging BigQuery
resource "google_project_iam_audit_config" "bigquery_audit" {
  project = google_project.data_platform.project_id
  service = "bigquery.googleapis.com"

  audit_log_config {
    log_type = "DATA_READ"    # Qui lit les données
  }
  audit_log_config {
    log_type = "DATA_WRITE"   # Qui écrit les données
  }
}
```

### FinOps BigQuery

BigQuery facturation sur 2 modèles :
- **On-demand** : 5 USD/TB de données scannées — idéal pour les requêtes irrégulières
- **Capacity** (slots) : 1 600 USD/mois pour 100 slots — idéal pour les charges prévisibles

**Optimisations mises en place** :
1. Partitionnement par date sur toutes les tables > 10 GB (réduction des scans de 70-90%)
2. Clustering sur les colonnes de filtre fréquent (customer_id, product_category)
3. Vues matérialisées pour les requêtes fréquentes en gold layer
4. Budget BigQuery avec alerte à 80% du budget mensuel

**Résultat** : Coût BigQuery réduit de 67% après optimisation (de 4 800 EUR/mois à 1 600 EUR/mois).

---

## Cas 3 — Architecture Multi-Cloud pour une Entreprise Industrielle (Azure + AWS)

### Contexte

Groupe industriel européen (8 000 employés) avec :
- Applications de gestion (ERP, CRM) sur Azure (AD, Office 365)
- Applications IoT et données temps réel sur AWS
- Besoin de connecter les deux environnements pour les dashboards de direction

### Architecture Hybride

**Décision** : Conserver les deux clouds (Azure pour l'enterprise IT, AWS pour l'opérationnel) avec une interconnexion sécurisée.

```
Azure AD (Identity)  ←→  AWS IAM (Federation via SAML/OIDC)
        |                          |
Azure VNet  ←→ ExpressRoute/VPN ←→ AWS VPC
        |                          |
Azure SQL (ERP data)         AWS IoT Core (sensors)
Azure Blob (Documents)       AWS S3 (data lake)
Azure DevOps (CI/CD)         AWS SageMaker (ML)
        |                          |
        └──────── Power BI ────────┘
                (unified dashboards)
```

**Fédération d'identité** : Azure AD comme IDP principal, fédération vers AWS via SAML 2.0. Les utilisateurs se connectent avec leurs identifiants Microsoft et accèdent aux ressources AWS avec des rôles assumés automatiquement.

```hcl
# Terraform — Fédération Azure AD vers AWS IAM
resource "aws_iam_saml_provider" "azure_ad" {
  name                   = "AzureAD-SAML"
  saml_metadata_document = file("azure_ad_metadata.xml")
}

resource "aws_iam_role" "azure_ad_engineers" {
  name = "AzureAD-Engineers"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Federated = aws_iam_saml_provider.azure_ad.arn }
      Action    = "sts:AssumeRoleWithSAML"
      Condition = {
        StringEquals = {
          "SAML:aud" = "https://signin.aws.amazon.com/saml"
        }
        StringLike = {
          "SAML:groups" = "aws-engineers-*"  # Groupe Azure AD
        }
      }
    }]
  })
}
```

### Optimisation des Coûts Multi-Cloud

**Challenge** : Maîtriser les coûts sur deux factures distinctes avec des modèles de pricing différents.

**Solution** : Dashboard unifié avec CloudHealth (outil tiers multi-cloud FinOps).

**Règles de gouvernance** :
1. Tout nouveau workload documenté avec la justification du cloud choisi
2. Revue mensuelle des coûts par workload et par cloud
3. Policy : pas de duplication de services entre les deux clouds sans justification

---

## Cas 4 — FinOps — Réduction de 40% des Coûts AWS (3 Mois)

### Contexte

Start-up SaaS (50 personnes) avec une facture AWS de 65 000 EUR/mois sans aucune gouvernance des coûts. Pas de tags, pas de budgets, pas de rightsizing. Objectif : réduire de 25% sans dégrader les performances.

### Audit Initial

**Distribution des coûts** :
- EC2 (instances on-demand, aucune RI) : 38% = 24 700 EUR
- RDS (over-provisioned) : 22% = 14 300 EUR
- S3 (versioning sans lifecycle) : 18% = 11 700 EUR
- ElastiCache (production size en dev aussi) : 12% = 7 800 EUR
- Transfert de données (egress) : 10% = 6 500 EUR

### Actions Réalisées

**Mois 1 — Quick Wins** :
- Tags obligatoires sur toutes les ressources (automated avec SCP qui bloque les ressources non taguées)
- Arrêt des environnements dev/staging en dehors des heures de bureau (-65% sur ces environnements)
- Lifecycle policy sur S3 : transition vers S3 Standard-IA après 30 jours, Glacier après 90 jours
- Suppression des 127 EBS snapshots de plus de 90 jours (non référencés)
- **Économie mois 1** : -14 200 EUR (-21.8%)

**Mois 2 — Rightsizing** :
- Analyse CloudWatch Compute Optimizer : 23 instances EC2 sous-utilisées identifiées
- Rightsizing de 15 instances (ex: m5.2xlarge → m5.large, utilisation CPU moyenne était 12%)
- RDS : downsize de 3 instances de développement, passage en Aurora Serverless pour les workloads irréguliers
- ElastiCache : réduction à cache.t3.medium en dev/staging (vs cache.r5.xlarge en production)
- **Économie mois 2** : -9 100 EUR supplémentaires

**Mois 3 — Réservations** :
- Analyse des workloads stables (> 80% d'utilisation sur 3 mois)
- Achat de Compute Savings Plans 1 an : -18 000 EUR/an d'engagement → -38% sur EC2 eligible
- RDS Reserved Instances pour les instances de production stables
- **Économie mois 3** : -3 800 EUR supplémentaires sur le récurrent

### Résultats

| Mois | Facture AWS | Économie vs. Baseline |
|---|---|---|
| Avant (baseline) | 65 000 EUR | - |
| Mois 1 | 50 800 EUR | -21.8% |
| Mois 2 | 41 700 EUR | -35.8% |
| Mois 3 | 38 500 EUR | -40.8% |

**ROI du projet FinOps** : Investissement de 2 jours-ingénieur par mois pendant 3 mois = 15 000 EUR. Économies annuelles : (65 000 - 38 500) × 12 = 318 000 EUR. **ROI : 21x la première année**.

**Leçons apprises** :
1. Le rightsizing seul représente souvent 15-25% d'économies immédiates
2. Les environnements non-production représentent fréquemment 30-40% de la facture alors qu'ils peuvent être éteints la nuit et le week-end
3. Les Savings Plans (flexible) sont supérieurs aux Reserved Instances pour les stacks dynamiques car ils s'appliquent à n'importe quel type d'instance
