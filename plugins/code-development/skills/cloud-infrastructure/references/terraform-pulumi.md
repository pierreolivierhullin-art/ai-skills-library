# Terraform & Pulumi — IaC Avancé, Modules, State & Testing

## Overview

Ce guide couvre les pratiques avancées d'Infrastructure as Code avec Terraform et Pulumi : structuration en modules réutilisables, gestion du state remote avec locking, workspaces pour le multi-environnement, testing de l'infrastructure avec Terratest, et drift detection. Il couvre également les cas où Pulumi est préférable à Terraform et comment migrer entre les deux.

---

## Terraform — Fondamentaux Avancés

### Structure d'un Projet Terraform Professionnel

```
infrastructure/
├── modules/                    # Modules réutilisables (versionnés)
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── rds-postgres/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ecs-service/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── alb/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── stacks/                     # Configurations par stack (state séparé)
│   ├── networking/             # Stack réseau (VPC, subnets, NAT)
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── backend.tf
│   │   └── terraform.tfvars
│   ├── database/               # Stack base de données (RDS, ElastiCache)
│   │   ├── main.tf
│   │   └── ...
│   └── application/            # Stack applicative (ECS, ALB, Lambda)
│       ├── main.tf
│       └── ...
├── envs/                       # Tfvars par environnement
│   ├── dev.tfvars
│   ├── staging.tfvars
│   └── production.tfvars
└── Makefile                    # Commandes standardisées
```

### Modules Terraform Réutilisables

```hcl
# modules/rds-postgres/variables.tf
variable "identifier" {
  description = "Identifiant unique de l'instance RDS"
  type        = string
}

variable "instance_class" {
  description = "Classe de l'instance RDS"
  type        = string
  default     = "db.t3.medium"
  validation {
    condition     = can(regex("^db\\.", var.instance_class))
    error_message = "La classe d'instance doit commencer par 'db.'"
  }
}

variable "allocated_storage" {
  description = "Taille du stockage en GB"
  type        = number
  default     = 20
  validation {
    condition     = var.allocated_storage >= 20 && var.allocated_storage <= 65536
    error_message = "Le stockage doit être entre 20 et 65536 GB"
  }
}

variable "db_name" {
  description = "Nom de la base de données initiale"
  type        = string
  sensitive   = false
}

variable "subnet_ids" {
  description = "Liste des IDs de subnets privés pour RDS"
  type        = list(string)
}

variable "vpc_security_group_ids" {
  description = "Liste des IDs de security groups"
  type        = list(string)
}

variable "tags" {
  description = "Tags à appliquer à toutes les ressources"
  type        = map(string)
  default     = {}
}
```

```hcl
# modules/rds-postgres/main.tf
resource "aws_db_subnet_group" "this" {
  name       = "${var.identifier}-subnet-group"
  subnet_ids = var.subnet_ids

  tags = merge(var.tags, {
    Name = "${var.identifier}-subnet-group"
  })
}

resource "aws_db_instance" "this" {
  identifier     = var.identifier
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.instance_class

  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.allocated_storage * 3  # Auto-scaling storage
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = var.db_name
  username = "postgres"
  password = random_password.db_password.result

  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = var.vpc_security_group_ids

  # Haute disponibilité
  multi_az               = var.environment == "production" ? true : false
  publicly_accessible    = false

  # Backups
  backup_retention_period = var.environment == "production" ? 14 : 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"

  # Monitoring
  monitoring_interval                   = 60
  monitoring_role_arn                   = aws_iam_role.rds_monitoring.arn
  performance_insights_enabled          = true
  performance_insights_retention_period = 7

  # Protection contre la suppression en production
  deletion_protection       = var.environment == "production" ? true : false
  skip_final_snapshot       = var.environment == "production" ? false : true
  final_snapshot_identifier = "${var.identifier}-final-${formatdate("YYYY-MM-DD", timestamp())}"

  tags = merge(var.tags, {
    Name = var.identifier
  })

  lifecycle {
    prevent_destroy = false
    ignore_changes  = [password]  # Le password est géré par AWS Secrets Manager
  }
}

resource "random_password" "db_password" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_secretsmanager_secret" "db_password" {
  name                    = "${var.identifier}/postgres/password"
  recovery_window_in_days = 0  # Suppression immédiate (à ajuster en production)
  tags                    = var.tags
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id
  secret_string = jsonencode({
    username = "postgres"
    password = random_password.db_password.result
    host     = aws_db_instance.this.address
    port     = aws_db_instance.this.port
    dbname   = var.db_name
  })
}
```

### Remote State avec Locking

```hcl
# stacks/networking/backend.tf
terraform {
  backend "s3" {
    bucket         = "mon-org-terraform-state"
    key            = "networking/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:eu-west-1:123456789:key/abc-123"

    # DynamoDB pour le locking (prévient les apply concurrents)
    dynamodb_table = "terraform-state-lock"
  }

  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}
```

```bash
# Créer le bucket S3 et la table DynamoDB pour le state (une seule fois)
aws s3api create-bucket \
  --bucket mon-org-terraform-state \
  --region eu-west-1 \
  --create-bucket-configuration LocationConstraint=eu-west-1

aws s3api put-bucket-versioning \
  --bucket mon-org-terraform-state \
  --versioning-configuration Status=Enabled

aws s3api put-bucket-encryption \
  --bucket mon-org-terraform-state \
  --server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms"}}]}'

aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region eu-west-1
```

### Workspaces pour Multi-Environnement

```hcl
# Utiliser les workspaces pour différencier dev/staging/production
# Terraform workspace = isolation du state dans le même backend

# Dans le code : référencer le workspace courant
locals {
  env = terraform.workspace  # "dev", "staging", "production"

  # Configuration par environnement
  config = {
    dev = {
      instance_type  = "t3.small"
      min_capacity   = 1
      max_capacity   = 2
      multi_az       = false
    }
    staging = {
      instance_type  = "t3.medium"
      min_capacity   = 2
      max_capacity   = 4
      multi_az       = false
    }
    production = {
      instance_type  = "m5.large"
      min_capacity   = 3
      max_capacity   = 20
      multi_az       = true
    }
  }
}

# Utilisation dans les ressources
resource "aws_ecs_service" "api" {
  desired_count = local.config[local.env].min_capacity
  # ...
}
```

```bash
# Gestion des workspaces
terraform workspace list
terraform workspace new dev
terraform workspace new staging
terraform workspace new production
terraform workspace select production

# Appliquer en ciblant l'environnement
terraform workspace select production
terraform plan -var-file="envs/production.tfvars"
terraform apply -var-file="envs/production.tfvars"
```

---

## Testing de l'Infrastructure — Terratest

```go
// tests/vpc_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestVPCModule(t *testing.T) {
    t.Parallel()

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../../modules/vpc",
        Vars: map[string]interface{}{
            "vpc_cidr": "10.0.0.0/16",
            "azs":      []string{"eu-west-1a", "eu-west-1b", "eu-west-1c"},
            "name":     "test-vpc",
            "tags": map[string]string{
                "Environment": "test",
                "ManagedBy":   "Terraform",
            },
        },
    })

    // Cleanup automatique à la fin du test
    defer terraform.Destroy(t, terraformOptions)

    // Apply l'infrastructure
    terraform.InitAndApply(t, terraformOptions)

    // Vérifier les outputs
    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcId)

    privateSubnetIds := terraform.OutputList(t, terraformOptions, "private_subnet_ids")
    require.Equal(t, 3, len(privateSubnetIds), "Doit avoir 3 subnets privés")

    publicSubnetIds := terraform.OutputList(t, terraformOptions, "public_subnet_ids")
    require.Equal(t, 3, len(publicSubnetIds), "Doit avoir 3 subnets publics")

    // Vérifier que le VPC est bien configuré via l'API AWS
    // (aucun subnet privé ne doit avoir un accès direct à internet)
}
```

### Analyse Statique de Sécurité — tfsec et Checkov

```bash
# tfsec — analyse de sécurité statique
pip install tfsec  # ou via brew install tfsec

# Scanner un module
tfsec modules/rds-postgres/

# Exemple de sortie :
# CRITICAL [aws-rds-encrypt-instance-storage-data] RDS instance storage is not encrypted
# MEDIUM   [aws-rds-enable-deletion-protection] Instance does not have deletion protection

# Checkov — plus de règles, YAML/JSON aussi
pip install checkov

# Scanner avec Checkov
checkov -d stacks/networking/ --framework terraform

# Intégrer dans GitHub Actions
# .github/workflows/security-scan.yml
steps:
  - name: Security Scan (Checkov)
    uses: bridgecrewio/checkov-action@master
    with:
      directory: infrastructure/
      framework: terraform
      soft_fail: false  # Échouer si des issues critiques sont trouvées
```

### Drift Detection

```bash
# Détecter le drift entre le state et l'infrastructure réelle
terraform plan -detailed-exitcode
# Exit code 0 : pas de changements
# Exit code 1 : erreur
# Exit code 2 : changements détectés (drift)

# Script de détection automatique du drift
#!/bin/bash
for stack in stacks/*/; do
    echo "Vérification du drift : $stack"
    cd "$stack"
    terraform workspace select production
    EXITCODE=$(terraform plan -detailed-exitcode 2>&1; echo $?)
    if [ "$EXITCODE" = "2" ]; then
        echo "DRIFT DETECTE dans $stack — investigation requise"
        # Envoyer une alerte
        curl -X POST "$SLACK_WEBHOOK" \
          -H "Content-Type: application/json" \
          -d "{\"text\": \"Drift Terraform détecté dans $stack\"}"
    fi
    cd ../..
done
```

---

## Pulumi — IaC avec de Vrais Langages

### Quand Choisir Pulumi vs Terraform

| Situation | Recommandation |
|---|---|
| Logique conditionnelle complexe (boucles, conditions, fonctions) | Pulumi |
| Équipes principalement dev (Python, TypeScript) | Pulumi |
| Tests unitaires de l'IaC en langage natif | Pulumi |
| Génération dynamique de ressources (nombre variable) | Pulumi |
| Infrastructure multi-cloud avec providers Terraform existants | Terraform |
| Équipes ops habituées au HCL | Terraform |
| Modules réutilisables dans le Terraform Registry | Terraform |
| Migration progressive depuis Terraform | Pulumi (CDKTF) |

### Exemple Pulumi TypeScript

```typescript
// index.ts — Infrastructure VPC + ECS avec Pulumi TypeScript
import * as aws from "@pulumi/aws";
import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config();
const env = pulumi.getStack();  // dev, staging, production
const isProduction = env === "production";

// Configuration par environnement (logique native TypeScript)
const instanceTypes: Record<string, string> = {
    dev: "t3.small",
    staging: "t3.medium",
    production: "m5.large",
};

// VPC
const vpc = new aws.ec2.Vpc("main-vpc", {
    cidrBlock: "10.0.0.0/16",
    enableDnsHostnames: true,
    enableDnsSupport: true,
    tags: {
        Name: `${env}-vpc`,
        Environment: env,
        ManagedBy: "Pulumi",
    },
});

// Subnets privés dans 3 AZs (boucle TypeScript native)
const availabilityZones = ["eu-west-1a", "eu-west-1b", "eu-west-1c"];
const privateSubnets = availabilityZones.map((az, index) =>
    new aws.ec2.Subnet(`private-subnet-${index}`, {
        vpcId: vpc.id,
        cidrBlock: `10.0.${index + 10}.0/24`,
        availabilityZone: az,
        mapPublicIpOnLaunch: false,
        tags: {
            Name: `${env}-private-${az}`,
            Type: "private",
        },
    })
);

// RDS avec configuration différenciée par environnement
const rdsSubnetGroup = new aws.rds.SubnetGroup("rds-subnet-group", {
    subnetIds: privateSubnets.map(s => s.id),
    tags: { Environment: env },
});

const database = new aws.rds.Instance("main-db", {
    identifier: `${env}-postgres`,
    engine: "postgres",
    engineVersion: "15.4",
    instanceClass: instanceTypes[env],
    allocatedStorage: isProduction ? 100 : 20,
    multiAz: isProduction,
    deletionProtection: isProduction,
    skipFinalSnapshot: !isProduction,
    dbSubnetGroupName: rdsSubnetGroup.name,
    tags: { Environment: env, ManagedBy: "Pulumi" },
});

// Exports
export const vpcId = vpc.id;
export const privateSubnetIds = privateSubnets.map(s => s.id);
export const dbEndpoint = database.endpoint;
```

### Testing Pulumi avec Jest

```typescript
// __tests__/infrastructure.test.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Mock du runtime Pulumi pour les tests
pulumi.runtime.setMocks({
    newResource: (args) => {
        return { id: `${args.name}-id`, state: args.inputs };
    },
    call: (args) => ({ outputs: {} }),
});

// Importer le code infrastructure après le mock
import "../index";

describe("VPC Configuration", () => {
    it("should have DNS support enabled", async () => {
        const vpc = await (await import("../index")).vpc;
        const enableDnsSupport = await vpc.enableDnsSupport;
        expect(enableDnsSupport).toBe(true);
    });

    it("should not be publicly accessible in production", async () => {
        const db = await (await import("../index")).database;
        const publiclyAccessible = await db.publiclyAccessible;
        expect(publiclyAccessible).toBeFalsy();
    });
});
```

---

## Convention de Nommage et Tagging

### Convention de Nommage des Ressources

```hcl
# Format : {org}-{env}-{stack}-{resource_type}-{purpose}
locals {
  prefix = "${var.organization}-${terraform.workspace}"

  # Exemples :
  # acme-production-networking-vpc-main
  # acme-staging-application-ecs-api
  # acme-dev-database-rds-postgres-main
}

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = merge(var.common_tags, {
    Name = "${local.prefix}-vpc-main"
  })
}
```

### Tags Obligatoires

```hcl
# variables.tf — Tags communs obligatoires
variable "common_tags" {
  description = "Tags appliqués à toutes les ressources"
  type = object({
    Environment  = string  # dev, staging, production
    Team         = string  # data, backend, platform
    Project      = string  # nom du projet
    CostCenter   = string  # centre de coût
    ManagedBy    = string  # Terraform, Pulumi, Manual
    Owner        = string  # email du responsable
  })
  validation {
    condition     = contains(["dev", "staging", "production"], var.common_tags.Environment)
    error_message = "Environment doit être: dev, staging, ou production"
  }
}
```

---

## Makefile Standardisé

```makefile
# Makefile pour standardiser les commandes Terraform

ENV ?= dev
STACK ?= networking

.PHONY: init plan apply destroy fmt validate docs

init:
	cd stacks/$(STACK) && \
	terraform workspace select $(ENV) || terraform workspace new $(ENV) && \
	terraform init -upgrade

plan:
	cd stacks/$(STACK) && \
	terraform workspace select $(ENV) && \
	terraform plan -var-file="../../envs/$(ENV).tfvars" -out=tfplan

apply:
	cd stacks/$(STACK) && \
	terraform workspace select $(ENV) && \
	terraform apply tfplan

destroy:
	@echo "ATTENTION : Vous êtes sur le point de détruire l'environnement $(ENV) - stack $(STACK)"
	@read -p "Confirmez en tapant le nom de l'environnement : " confirm && [ "$$confirm" = "$(ENV)" ]
	cd stacks/$(STACK) && \
	terraform workspace select $(ENV) && \
	terraform destroy -var-file="../../envs/$(ENV).tfvars"

fmt:
	terraform fmt -recursive .

validate:
	cd stacks/$(STACK) && terraform validate

security-scan:
	checkov -d . --framework terraform
	tfsec .

drift-check:
	cd stacks/$(STACK) && \
	terraform workspace select $(ENV) && \
	terraform plan -detailed-exitcode -var-file="../../envs/$(ENV).tfvars" && \
	echo "Pas de drift détecté" || echo "DRIFT DÉTECTÉ - investigation requise"

docs:
	terraform-docs markdown table . > README.md
```

---

## Gestion des Secrets en IaC

### Anti-Pattern : Ne Jamais Faire

```hcl
# MAUVAIS — secrets en clair dans le code
resource "aws_db_instance" "main" {
  password = "MonMotDePasseSecret123!"  # Ne JAMAIS faire ça
}
```

### Pattern Correct : AWS Secrets Manager

```hcl
# CORRECT — générer et stocker dans Secrets Manager
resource "random_password" "db" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret" "db_password" {
  name                    = "production/rds/postgres/password"
  recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db.result
}

resource "aws_db_instance" "main" {
  password = random_password.db.result  # Généré, jamais hardcodé
  # L'application lit le secret depuis Secrets Manager, pas depuis Terraform
}
```

### OIDC pour le CI/CD — Pas de Credentials Longue Durée

```hcl
# Provider OIDC pour GitHub Actions → AWS (sans AWS access keys)
data "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
}

resource "aws_iam_role" "github_actions_terraform" {
  name = "github-actions-terraform-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Federated = data.aws_iam_openid_connect_provider.github.arn }
      Action    = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:mon-org/mon-repo:*"
        }
      }
    }]
  })
}
```
