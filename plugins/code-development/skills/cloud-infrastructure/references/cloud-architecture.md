# Cloud Architecture — Patterns, Réseaux, Haute Disponibilité & FinOps

## Overview

Ce guide couvre les patterns d'architecture cloud avancés : conception du réseau (VPC, subnets, routing), haute disponibilité et disaster recovery, FinOps opérationnel, sécurité cloud by design, et patterns d'architecture applicative cloud-native (microservices cloud, event-driven, multi-tier). Il s'adresse aux architectes et ingénieurs qui conçoivent des systèmes cloud robustes et économiques.

---

## Conception du Réseau Cloud

### Architecture VPC Recommandée

Une bonne architecture VPC sépare les ressources par niveau de confiance et d'accessibilité.

```hcl
# Terraform — VPC avec 3 couches (public / private / data)
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "${var.env}-vpc"
  cidr = "10.0.0.0/16"

  azs = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]

  # Subnets publics : load balancers, NAT gateways
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]

  # Subnets privés : application servers, Kubernetes nodes
  private_subnets = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]

  # Subnets data : bases de données, ElastiCache (aucun accès internet)
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

  # NAT Gateway : permet aux subnets privés d'accéder à internet en sortie
  enable_nat_gateway     = true
  single_nat_gateway     = var.env != "production"  # 1 NAT en dev, 3 en prod
  one_nat_gateway_per_az = var.env == "production"

  # VPC Flow Logs : indispensable pour l'audit et la détection d'anomalies réseau
  enable_flow_log                      = true
  create_flow_log_cloudwatch_log_group = true
  flow_log_cloudwatch_log_group_retention_in_days = 30

  tags = var.common_tags
}
```

### Dimensionnement des CIDR

Dimensionner les CIDR dès le départ pour éviter les migrations douloureuses.

| Scope | CIDR recommandé | Adresses disponibles | Commentaire |
|---|---|---|---|
| **VPC** | /16 | 65 536 | Prévoir de la croissance |
| **Subnet public** | /24 | 251 | Assez pour les LBs et NAT |
| **Subnet privé** | /22 | 1 019 | Assez pour les pods K8s |
| **Subnet data** | /24 | 251 | Peu d'instances DB |
| **Peering avec on-premise** | /8 réservé | - | Éviter les chevauchements |

### Security Groups vs NACLs

| Critère | Security Groups | Network ACLs |
|---|---|---|
| **Scope** | Instance (stateful) | Subnet (stateless) |
| **Stateful/Stateless** | Stateful (réponse auto autorisée) | Stateless (retour à configurer) |
| **Règles** | Allow uniquement | Allow et Deny |
| **Évaluation** | Toutes les règles | Ordre numérique (première correspondance) |
| **Usage recommandé** | Contrôle fin par instance | Défense en profondeur (blocages IP) |

**Pattern recommandé** :
- Security Groups : contrôle principal du trafic (par application, par tier)
- NACLs : blocage d'IPs malveillantes ou de plages réseau entières

```hcl
# Security Group — Pattern minimal pour une API
resource "aws_security_group" "api" {
  name        = "${var.env}-api-sg"
  description = "Security group for API servers"
  vpc_id      = module.vpc.vpc_id

  # Trafic entrant : uniquement depuis le load balancer
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "HTTP from ALB"
  }

  # Trafic sortant : accès à la DB et aux APIs externes
  egress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.rds.id]
    description     = "PostgreSQL to RDS"
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS to internet (APIs externes)"
  }

  tags = merge(var.common_tags, { Name = "${var.env}-api-sg" })
}
```

---

## Haute Disponibilité et Disaster Recovery

### Niveaux de Disponibilité

| SLA | Downtime max/mois | Pattern requis |
|---|---|---|
| 99% | 7h 18min | Single AZ, auto-restart |
| 99.9% | 43 min | Multi-AZ actif-passif |
| 99.95% | 21 min | Multi-AZ actif-actif |
| 99.99% | 4 min | Multi-région actif-actif |
| 99.999% | 26 sec | Multi-région + chaos engineering |

### Architecture Multi-AZ (99.9% à 99.95%)

```hcl
# Auto Scaling Group multi-AZ
resource "aws_autoscaling_group" "api" {
  name                = "${var.env}-api-asg"
  min_size            = var.env == "production" ? 3 : 1
  max_size            = var.env == "production" ? 20 : 3
  desired_capacity    = var.env == "production" ? 3 : 1

  # Distribuer sur plusieurs AZs
  vpc_zone_identifier = module.vpc.private_subnets

  # Politique de santé : remplacer les instances unhealthy
  health_check_type         = "ELB"
  health_check_grace_period = 300

  # Distribuer équitablement entre AZs
  availability_zone_rebalancing = "Enabled"

  launch_template {
    id      = aws_launch_template.api.id
    version = "$Latest"
  }

  # Pas de terminaison lors des déploiements blue-green
  lifecycle {
    create_before_destroy = true
    ignore_changes        = [desired_capacity]
  }

  tag {
    key                 = "Environment"
    value               = var.env
    propagate_at_launch = true
  }
}

# Scaling policies
resource "aws_autoscaling_policy" "cpu_out" {
  name                   = "scale-out-cpu"
  autoscaling_group_name = aws_autoscaling_group.api.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = 2

  policy_type = "StepScaling"
  step_adjustment {
    metric_interval_lower_bound = 0
    metric_interval_upper_bound = 10
    scaling_adjustment          = 1
  }
  step_adjustment {
    metric_interval_lower_bound = 10
    scaling_adjustment          = 3
  }
}
```

### Disaster Recovery — RTO et RPO

| Stratégie | RTO | RPO | Coût | Description |
|---|---|---|---|---|
| **Backup & Restore** | Heures | Heures | Faible | Sauvegardes régulières, restauration manuelle |
| **Pilot Light** | 10-30 min | Minutes | Moyen | Infrastructure minimale en veille (DB répliquée) |
| **Warm Standby** | 5-10 min | Secondes | Élevé | Infrastructure réduite mais active en standby |
| **Multi-Site Active-Active** | < 1 min | < 1 sec | Très élevé | Infrastructure complète dans 2+ régions |

**Implémentation Pilot Light avec Terraform** :

```hcl
# Région primaire (eu-west-1)
provider "aws" {
  alias  = "primary"
  region = "eu-west-1"
}

# Région de DR (eu-central-1)
provider "aws" {
  alias  = "dr"
  region = "eu-central-1"
}

# RDS avec réplication cross-région
resource "aws_db_instance" "primary" {
  provider         = aws.primary
  identifier       = "production-postgres"
  # ... configuration primaire
  backup_retention_period = 14
  backup_window           = "03:00-04:00"
}

resource "aws_db_instance" "replica" {
  provider             = aws.dr
  identifier           = "dr-postgres-replica"
  replicate_source_db  = aws_db_instance.primary.arn
  instance_class       = "db.t3.medium"  # Instance plus petite en standby
  skip_final_snapshot  = true
}
```

---

## FinOps — Optimisation des Coûts Cloud

### Framework de Gouvernance des Coûts

**Pilier 1 — Visibilité** : Savoir où va l'argent, par équipe, par service, par environnement.

```hcl
# Tags obligatoires sur toutes les ressources
variable "required_tags" {
  type = object({
    Environment = string  # dev, staging, production
    Team        = string  # platform, data, backend
    Project     = string  # nom du projet
    CostCenter  = string  # centre de coût comptable
    ManagedBy   = string  # Terraform, Pulumi, Manual
  })
  validation {
    condition = (
      contains(["dev", "staging", "production"], var.required_tags.Environment) &&
      length(var.required_tags.Team) > 0 &&
      length(var.required_tags.Project) > 0
    )
    error_message = "Tags obligatoires manquants ou invalides"
  }
}
```

**Pilier 2 — Optimisation** : Rightsizing, réservations, spot instances.

```python
# Script d'analyse des ressources sous-utilisées
import boto3
from datetime import datetime, timedelta

def find_underutilized_instances(min_cpu_threshold=20, lookback_days=14):
    """
    Identifie les instances EC2 avec utilisation CPU moyenne < seuil.
    Candidats au rightsizing.
    """
    ec2 = boto3.client('ec2', region_name='eu-west-1')
    cw = boto3.client('cloudwatch', region_name='eu-west-1')

    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )

    underutilized = []
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=lookback_days)

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']

            # Récupérer les métriques CPU
            response = cw.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,  # 1 jour
                Statistics=['Average', 'Maximum']
            )

            if response['Datapoints']:
                avg_cpu = sum(d['Average'] for d in response['Datapoints']) / len(response['Datapoints'])
                max_cpu = max(d['Maximum'] for d in response['Datapoints'])

                if avg_cpu < min_cpu_threshold:
                    underutilized.append({
                        'instance_id': instance_id,
                        'instance_type': instance['InstanceType'],
                        'avg_cpu': round(avg_cpu, 1),
                        'max_cpu': round(max_cpu, 1),
                        'recommendation': 'Consider downsizing'
                    })

    return underutilized
```

**Pilier 3 — Planification** : Acheter des réservations pour les workloads stables.

```python
# Calculer les économies potentielles avec Reserved Instances
def ri_savings_analysis(instance_type, region, utilization_hours_per_month):
    """
    Compare le coût on-demand vs Reserved Instance (1 an, no upfront).
    """
    # Prix approximatifs en USD (à mettre à jour depuis l'API AWS Pricing)
    on_demand_prices = {
        "t3.medium": 0.0416,   # USD/heure
        "m5.large": 0.096,
        "m5.xlarge": 0.192,
        "c5.xlarge": 0.17,
        "r5.xlarge": 0.252,
    }

    # Réduction RI 1 an no upfront ≈ 38%
    ri_discount = 0.38

    hourly_od = on_demand_prices.get(instance_type, 0.10)
    hourly_ri = hourly_od * (1 - ri_discount)

    monthly_od_cost = hourly_od * utilization_hours_per_month
    monthly_ri_cost = hourly_ri * 730  # 730h/mois, on paye même si éteint

    # RI est rentable si l'utilisation > break-even
    break_even_hours = monthly_ri_cost / hourly_od
    monthly_savings = monthly_od_cost - monthly_ri_cost if utilization_hours_per_month > break_even_hours else 0

    return {
        "instance_type": instance_type,
        "monthly_on_demand": round(monthly_od_cost, 2),
        "monthly_ri": round(monthly_ri_cost, 2),
        "monthly_savings": round(monthly_savings, 2),
        "break_even_hours": round(break_even_hours, 0),
        "recommendation": "BUY RI" if utilization_hours_per_month > break_even_hours else "KEEP ON-DEMAND"
    }
```

### Environnements Non-Production — Arrêt Automatique

```python
# scripts/stop_nonprod_resources.py
# Exécuter via EventBridge Rule à 20h00 heure locale (lundi-vendredi)

import boto3

def stop_nonprod_instances():
    """Arrête les instances EC2 non-production en fin de journée."""
    ec2 = boto3.client('ec2', region_name='eu-west-1')

    # Trouver les instances dev et staging avec le tag Environment
    instances = ec2.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']},
            {'Name': 'tag:Environment', 'Values': ['dev', 'staging']},
            # Ne pas arrêter les instances explicitement marquées "always-on"
            {'Name': 'tag:AlwaysOn', 'Values': ['false']}
        ]
    )

    instance_ids = [
        i['InstanceId']
        for r in instances['Reservations']
        for i in r['Instances']
    ]

    if instance_ids:
        ec2.stop_instances(InstanceIds=instance_ids)
        print(f"Instances arrêtées : {instance_ids}")
        # Économie typique : 65% du coût mensuel (arrêt 16h/jour + WE)

# Relancer le matin (8h00)
def start_nonprod_instances():
    ec2 = boto3.client('ec2', region_name='eu-west-1')
    instances = ec2.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['stopped']},
            {'Name': 'tag:Environment', 'Values': ['dev', 'staging']},
            {'Name': 'tag:AlwaysOn', 'Values': ['false']}
        ]
    )
    instance_ids = [i['InstanceId'] for r in instances['Reservations'] for i in r['Instances']]
    if instance_ids:
        ec2.start_instances(InstanceIds=instance_ids)
```

---

## Sécurité Cloud by Design

### Modèle de Sécurité en Couches

```
Couche 1 — Périmètre réseau
  WAF + Shield → filtre les attaques web et DDoS
  CloudFront / Cloud CDN → cache + protection edge

Couche 2 — Réseau VPC
  NACLs → blocage d'IPs malveillantes au niveau subnet
  Security Groups → contrôle d'accès par instance (least privilege)
  VPC Flow Logs → audit de tout le trafic réseau

Couche 3 — Identité et Accès
  IAM Roles + Policies → least privilege pour chaque service
  MFA obligatoire → pour tous les accès humans
  OIDC Federation → CI/CD sans credentials longue durée

Couche 4 — Application
  TLS 1.2+ → chiffrement en transit (mTLS entre services)
  Validation des inputs → injection prevention
  Rate limiting → protection contre les abus

Couche 5 — Données
  KMS → chiffrement au repos (RDS, S3, EBS)
  Secrets Manager → gestion centralisée des secrets
  S3 Block Public Access → aucun bucket public par défaut

Couche 6 — Audit et Détection
  CloudTrail / Audit Logs → traçabilité de toutes les actions API
  GuardDuty / Security Command Center → détection des menaces ML
  Security Hub / Security Command Center → agrégation des findings
```

### IAM — Bonnes Pratiques

```hcl
# Politique IAM minimale pour une Lambda qui accède à DynamoDB et S3
resource "aws_iam_policy" "lambda_minimal" {
  name        = "${var.env}-lambda-minimal-policy"
  description = "Politique minimale pour Lambda churn-api"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # DynamoDB : accès limité à une table et aux opérations nécessaires
      {
        Sid    = "DynamoDBReadWrite"
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:Query"
        ]
        Resource = [
          "arn:aws:dynamodb:eu-west-1:${data.aws_caller_identity.current.account_id}:table/${var.env}-customers",
          "arn:aws:dynamodb:eu-west-1:${data.aws_caller_identity.current.account_id}:table/${var.env}-customers/index/*"
        ]
      },
      # S3 : accès limité à un prefix dans un bucket
      {
        Sid    = "S3ModelRead"
        Effect = "Allow"
        Action = ["s3:GetObject"]
        Resource = "arn:aws:s3:::${var.model_bucket}/models/${var.env}/*"
      },
      # Secrets Manager : accès au secret spécifique
      {
        Sid    = "SecretsRead"
        Effect = "Allow"
        Action = ["secretsmanager:GetSecretValue"]
        Resource = "arn:aws:secretsmanager:eu-west-1:${data.aws_caller_identity.current.account_id}:secret:${var.env}/api-key-*"
      }
    ]
  })
}
```

### Encryption et Gestion des Clés

```hcl
# KMS Key pour le chiffrement des données sensibles
resource "aws_kms_key" "data_encryption" {
  description             = "Clé de chiffrement pour les données sensibles ${var.env}"
  deletion_window_in_days = 30
  enable_key_rotation     = true  # Rotation automatique annuelle

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # Accès admin complet au compte
      {
        Sid    = "EnableIAMRootAccess"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      # Accès limité aux services autorisés
      {
        Sid    = "AllowRDSEncryption"
        Effect = "Allow"
        Principal = { Service = "rds.amazonaws.com" }
        Action   = ["kms:Decrypt", "kms:GenerateDataKey", "kms:CreateGrant"]
        Resource = "*"
      }
    ]
  })

  tags = merge(var.common_tags, { Purpose = "data-encryption" })
}

resource "aws_kms_alias" "data_encryption" {
  name          = "alias/${var.env}-data-encryption"
  target_key_id = aws_kms_key.data_encryption.key_id
}
```

---

## Patterns d'Architecture Cloud-Native

### Pattern 1 — Three-Tier Cloud-Native

```
Internet → Route 53 (DNS) → CloudFront (CDN/WAF)
              |
         Application Load Balancer (public subnet)
              |
         ECS/EKS Tasks (private subnet, auto-scaling)
              |
         RDS Aurora + ElastiCache (data subnet)
```

**Règles** :
- Load balancer dans le subnet public, application dans le private
- Base de données dans le subnet data (pas d'accès depuis les subnets publics)
- Auto-scaling group ou ECS service avec min 2 instances (au moins 2 AZs)
- Health checks sur le load balancer avec seuils appropriés

### Pattern 2 — Event-Driven Cloud-Native

```
API Gateway → Lambda (validation) → SQS Queue → Lambda (processing) → DynamoDB
                                          ↓
                                    SNS → Lambda (notification) → SES
                                    SNS → Lambda (audit log)   → S3 + Athena
```

**Avantages** :
- Découplage fort entre les composants
- Retry automatique avec DLQ (Dead Letter Queue)
- Scaling indépendant de chaque composant

### Pattern 3 — CQRS + Event Sourcing

```
Write path:
  API → Command Handler → Event Store (DynamoDB) → Event Bus (EventBridge)
                                                         ↓
Read path:                                     Projections → Read Models (ElastiSearch, DynamoDB)
  API → Query Handler → Read Models
```

### Matrice de Décision Architecturale

| Critère | Monolithe cloud | Microservices cloud | Serverless event-driven |
|---|---|---|---|
| **Équipe** | Petite (< 5 devs) | Moyenne à grande | Petite à moyenne |
| **Trafic** | Prévisible et modéré | Variable ou élevé | Très variable, spiky |
| **Latence** | Faible (tout in-process) | Modérée (réseau) | Variable (cold start) |
| **Complexité ops** | Faible | Élevée (K8s, service mesh) | Faible |
| **Coût** | Prévisible | Variable | Pay-per-use |
| **Déploiement** | Simple | Complexe | Simple |
| **Quand choisir** | Démarrage, MVP | Scaling avancé | Tâches événementielles |

---

## Checklist d'Architecture Cloud

### Review d'Architecture — Questions à Vérifier

```
Fiabilité
[ ] Les composants critiques sont déployés dans au moins 2 AZs
[ ] Des health checks sont configurés sur tous les services
[ ] Un plan de DR est documenté et testé (RTO < ___, RPO < ___)
[ ] Les dépendances externes ont des circuit breakers ou des fallbacks

Sécurité
[ ] Aucune ressource n'est accessible depuis internet sans nécessité
[ ] Les credentials ne sont pas hardcodés (Secrets Manager / Secret Manager)
[ ] Le chiffrement au repos est activé sur toutes les données sensibles
[ ] Les logs d'audit sont activés et conservés au moins 90 jours
[ ] Les permissions IAM respectent le least privilege

Performance
[ ] Les tables de base de données sont indexées correctement
[ ] Un CDN est en place pour les ressources statiques
[ ] L'auto-scaling est configuré avec des métriques pertinentes
[ ] Des load tests ont été conduits sur des scénarios de pic de trafic

Coûts
[ ] Toutes les ressources ont les tags obligatoires
[ ] Des budgets avec alertes sont configurés
[ ] Les réservations sont en place pour les workloads stables
[ ] Les environnements non-production ont un arrêt automatique

Opérationnel
[ ] Le monitoring et les alertes sont configurés
[ ] Un runbook documenté pour les opérations courantes
[ ] Les pipelines IaC sont en place (pas de ClickOps)
[ ] Les secrets sont rotés régulièrement
```
