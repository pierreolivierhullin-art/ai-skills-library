# Infrastructure as Code — Terraform, Pulumi, GitOps & IaC Testing

## Introduction

**FR** — Ce guide de reference couvre l'Infrastructure as Code (IaC) dans toutes ses dimensions : Terraform, Pulumi, AWS CDK, Ansible, GitOps avec ArgoCD et Flux, tests d'infrastructure, detection de drift et gestion d'etat. L'IaC est le fondement d'une infrastructure reproductible, auditable et versionnable. Traiter l'infrastructure exactement comme le code applicatif : avec des reviews, des tests et un deploiement automatise.

**EN** — This reference guide covers Infrastructure as Code (IaC) across all dimensions: Terraform, Pulumi, AWS CDK, Ansible, GitOps with ArgoCD and Flux, infrastructure testing, drift detection, and state management. IaC is the foundation of reproducible, auditable, and versionable infrastructure. Treat infrastructure exactly like application code: with reviews, tests, and automated deployment.

---

## 1. Terraform — The Industry Standard

### Project Structure

Organize Terraform code in a modular, environment-aware structure:

```
infrastructure/
  modules/
    networking/
      main.tf
      variables.tf
      outputs.tf
    compute/
      main.tf
      variables.tf
      outputs.tf
    database/
      main.tf
      variables.tf
      outputs.tf
  environments/
    dev/
      main.tf          # Calls modules with dev-specific vars
      terraform.tfvars
      backend.tf        # S3 + DynamoDB state backend
    staging/
      main.tf
      terraform.tfvars
      backend.tf
    production/
      main.tf
      terraform.tfvars
      backend.tf
```

**FR** — Separer les modules (logique reutilisable) des environnements (configuration specifique). Chaque environnement a son propre state backend et ses propres variables.

### HCL Best Practices

```hcl
# Use descriptive variable names with validation
variable "instance_type" {
  description = "EC2 instance type for the application server"
  type        = string
  default     = "t3.medium"

  validation {
    condition     = can(regex("^t3\\.", var.instance_type))
    error_message = "Only t3 instance types are allowed in this module."
  }
}

# Use locals for computed values
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
    Repository  = "github.com/org/infra"
  }
}

# Use for_each over count for resources with identity
resource "aws_security_group_rule" "ingress" {
  for_each = var.ingress_rules

  type              = "ingress"
  from_port         = each.value.port
  to_port           = each.value.port
  protocol          = "tcp"
  cidr_blocks       = each.value.cidrs
  security_group_id = aws_security_group.main.id
}

# Use data sources to reference existing resources
data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["main-vpc"]
  }
}
```

**EN** — Key HCL practices: use `for_each` instead of `count` (avoids index-based drift), add `validation` blocks to variables, tag every resource with `ManagedBy = "terraform"`, use `locals` for computed values.

### Terraform Modules

```hcl
# Calling a module
module "api_service" {
  source  = "git::https://github.com/org/terraform-modules.git//modules/ecs-service?ref=v2.3.1"

  service_name    = "api"
  container_image = "ghcr.io/org/api:${var.api_image_tag}"
  cpu             = 512
  memory          = 1024
  desired_count   = var.environment == "production" ? 3 : 1

  environment_variables = {
    DATABASE_URL = data.aws_ssm_parameter.database_url.value
    LOG_LEVEL    = var.environment == "production" ? "warn" : "debug"
  }
}
```

**FR** — Versionner les modules par tags Git. Ne jamais referencer `?ref=main` en production. Chaque module doit avoir des variables clairement documentees, des outputs utiles et un README avec des exemples.

### State Management

**EN** — Terraform state is the most critical piece of your IaC setup. Mismanage it and you risk data loss or resource orphaning.

```hcl
# backend.tf — Remote state with S3 + DynamoDB locking
terraform {
  backend "s3" {
    bucket         = "myorg-terraform-state"
    key            = "production/api/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}
```

State management rules:
- **Always use remote state** with locking (S3+DynamoDB, GCS, Terraform Cloud, or Azure Blob).
- **Never commit state files** to Git. Add `*.tfstate` and `*.tfstate.backup` to `.gitignore`.
- **Use separate state per environment** and per service. A single monolithic state file is a scalability and blast radius problem.
- **Enable state encryption** at rest and in transit.
- **Use `terraform state` commands carefully**. Always `terraform plan` before `terraform apply`. Require approval for state-modifying operations.

### Workspaces vs. Directory Separation

**EN** — Prefer directory-per-environment over workspaces for production infrastructure. Workspaces share a backend configuration and can lead to accidental cross-environment operations. Use workspaces only for ephemeral environments (PR preview environments, developer sandboxes).

**FR** — Preferer un repertoire par environnement aux workspaces pour l'infrastructure de production. Les workspaces partagent la configuration du backend et peuvent mener a des operations inter-environnements accidentelles.

### Terraform CI Pipeline

```yaml
# GitHub Actions — Terraform CI
name: Terraform
on:
  pull_request:
    paths: ['infrastructure/**']
  push:
    branches: [main]
    paths: ['infrastructure/**']

jobs:
  plan:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.TERRAFORM_ROLE_ARN }}
          aws-region: eu-west-1
      - run: terraform init
        working-directory: infrastructure/environments/staging
      - run: terraform plan -out=plan.tfplan
        working-directory: infrastructure/environments/staging
      - uses: borchero/terraform-plan-comment@v2
        with:
          plan-file: infrastructure/environments/staging/plan.tfplan

  apply:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.TERRAFORM_ROLE_ARN }}
          aws-region: eu-west-1
      - run: terraform init && terraform apply -auto-approve
        working-directory: infrastructure/environments/production
```

**EN** — Run `terraform plan` on every PR and post the plan as a PR comment. Run `terraform apply` only on merge to main, with an environment protection rule requiring manual approval for production.

---

## 2. Pulumi — Programmatic IaC

### Why Pulumi

Use Pulumi when the team prefers real programming languages over HCL, when infrastructure logic requires complex conditionals, loops, or abstractions, or when tight integration with application code is valuable.

### Pulumi with TypeScript

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const environment = pulumi.getStack(); // "dev", "staging", "production"

// Create a VPC with tagged subnets
const vpc = new aws.ec2.Vpc("main", {
  cidrBlock: "10.0.0.0/16",
  enableDnsHostnames: true,
  tags: { Name: `${environment}-vpc`, ManagedBy: "pulumi" },
});

// Use programming constructs for complex logic
const azs = ["eu-west-1a", "eu-west-1b", "eu-west-1c"];
const publicSubnets = azs.map((az, index) =>
  new aws.ec2.Subnet(`public-${index}`, {
    vpcId: vpc.id,
    cidrBlock: `10.0.${index}.0/24`,
    availabilityZone: az,
    mapPublicIpOnLaunch: true,
    tags: { Name: `${environment}-public-${az}` },
  })
);

// Create a reusable component
class FargateService extends pulumi.ComponentResource {
  public readonly url: pulumi.Output<string>;

  constructor(name: string, args: FargateServiceArgs, opts?: pulumi.ComponentResourceOptions) {
    super("custom:FargateService", name, {}, opts);
    // ... service creation logic
    this.url = loadBalancer.dnsName;
    this.registerOutputs({ url: this.url });
  }
}

// Export outputs
export const vpcId = vpc.id;
export const subnetIds = publicSubnets.map(s => s.id);
```

**FR** — Pulumi permet d'utiliser TypeScript, Python, Go ou C# pour definir l'infrastructure. Les avantages : autocompletion IDE, tests unitaires natifs, abstractions via classes et fonctions, et logique conditionnelle naturelle.

### Pulumi State Management

- Use Pulumi Cloud (managed backend) for team collaboration with built-in RBAC, audit logs, and secrets management.
- Alternatively, use S3 or Azure Blob as a self-managed backend: `pulumi login s3://my-pulumi-state`.
- Use stacks to represent environments: `pulumi stack select production`.

---

## 3. AWS CDK

### CDK with TypeScript

```typescript
import { Stack, StackProps, RemovalPolicy } from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';

export class ApiStack extends Stack {
  constructor(scope: Construct, id: string, props: StackProps & { environment: string }) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'Vpc', { maxAzs: 3 });

    const cluster = new ecs.Cluster(this, 'Cluster', { vpc });

    new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'ApiService', {
      cluster,
      taskImageOptions: {
        image: ecs.ContainerImage.fromRegistry(`ghcr.io/org/api:${process.env.IMAGE_TAG}`),
        environment: {
          NODE_ENV: props.environment,
        },
      },
      desiredCount: props.environment === 'production' ? 3 : 1,
      publicLoadBalancer: true,
    });
  }
}
```

**EN** — CDK generates CloudFormation under the hood. Use L2/L3 constructs (high-level abstractions) for common patterns. Drop to L1 constructs only when needed. CDK is AWS-only; use Terraform or Pulumi for multi-cloud.

**FR** — CDK genere du CloudFormation. Utiliser les constructs L2/L3 pour les patrons courants. CDK est reserve a AWS ; utiliser Terraform ou Pulumi pour le multi-cloud.

---

## 4. Ansible — Configuration Management

### When to Use Ansible

Use Ansible to complement declarative IaC, not replace it. Ansible excels at:
- Configuring existing servers (software installation, service configuration)
- Running ad-hoc operational tasks across fleets
- Managing legacy infrastructure that predates containerization
- Application deployment to VMs when containers are not viable

```yaml
# playbook.yml — Configure a web server
---
- hosts: webservers
  become: true
  vars:
    app_version: "{{ lookup('env', 'APP_VERSION') }}"

  roles:
    - common
    - nginx
    - app-deploy

  tasks:
    - name: Ensure application is running
      systemd:
        name: myapp
        state: started
        enabled: true

    - name: Run health check
      uri:
        url: "http://localhost:8080/health"
        status_code: 200
      retries: 5
      delay: 3
```

**FR** — Utiliser Ansible pour la gestion de configuration, pas pour le provisionnement d'infrastructure. Combiner Terraform (provisionnement) + Ansible (configuration) pour les environnements bases sur des VMs.

---

## 5. GitOps with ArgoCD and Flux

### GitOps Principles

1. **Declarative**: The entire system is described declaratively in Git.
2. **Versioned and immutable**: The desired state is versioned in Git, providing an audit trail.
3. **Pulled automatically**: Agents (ArgoCD, Flux) pull the desired state and reconcile.
4. **Continuously reconciled**: Agents detect and correct drift between desired and actual state.

### ArgoCD Setup and Configuration

```yaml
# ArgoCD Application manifest
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: api-production
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/k8s-manifests.git
    targetRevision: main
    path: apps/api/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: api
  syncPolicy:
    automated:
      prune: true        # Delete resources removed from Git
      selfHeal: true     # Correct manual drift
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 3
      backoff:
        duration: 5s
        maxDuration: 3m
        factor: 2
```

### ArgoCD ApplicationSets for Multi-Environment

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: api
spec:
  generators:
    - list:
        elements:
          - env: dev
            cluster: dev-cluster
            revision: main
          - env: staging
            cluster: staging-cluster
            revision: main
          - env: production
            cluster: prod-cluster
            revision: v2.3.1   # Pin production to a tag
  template:
    metadata:
      name: 'api-{{env}}'
    spec:
      source:
        repoURL: https://github.com/org/k8s-manifests.git
        targetRevision: '{{revision}}'
        path: 'apps/api/overlays/{{env}}'
      destination:
        server: '{{cluster}}'
        namespace: api
```

**FR** — ApplicationSets permettent de deployer la meme application sur plusieurs environnements ou clusters a partir d'un seul template. Epingler la production a un tag specifique, utiliser `main` pour dev et staging.

### Flux CD

```yaml
# Flux GitRepository + Kustomization
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: infra
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/k8s-manifests
  ref:
    branch: main

---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: api
  namespace: flux-system
spec:
  interval: 5m
  path: ./apps/api/overlays/production
  prune: true
  sourceRef:
    kind: GitRepository
    name: infra
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: api
      namespace: api
```

**EN** — Flux uses a pull-based model with controllers watching Git repositories. It integrates natively with Kustomize and Helm. Choose Flux for teams that prefer Kubernetes-native tooling with less UI overhead than ArgoCD.

---

## 6. IaC Testing

### Terraform Testing with Terratest

```go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVpcModule(t *testing.T) {
    t.Parallel()

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../modules/networking",
        Vars: map[string]interface{}{
            "environment": "test",
            "cidr_block":  "10.99.0.0/16",
        },
    })

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcId)

    subnetCount := terraform.Output(t, terraformOptions, "subnet_count")
    assert.Equal(t, "3", subnetCount)
}
```

**FR** — Terratest cree de vraies ressources, les teste, puis les detruit. Executer ces tests dans un compte AWS sandbox dedie. Couteux en temps et en argent — utiliser pour les modules critiques, pas pour chaque changement.

### Static Analysis with Checkov

```yaml
# CI step for IaC static analysis
- name: Run Checkov
  uses: bridgecrewio/checkov-action@v12
  with:
    directory: infrastructure/
    framework: terraform
    soft_fail: false
    output_format: sarif
    download_external_modules: true
```

**EN** — Checkov scans IaC files for security misconfigurations (e.g., unencrypted S3 buckets, overly permissive security groups, missing logging). Run it on every PR. Also consider tfsec, Trivy IaC scanning, or OPA/Rego policies for custom rules.

### Terraform Native Tests (v1.6+)

```hcl
# tests/vpc.tftest.hcl
run "create_vpc" {
  command = apply

  variables {
    environment = "test"
    cidr_block  = "10.99.0.0/16"
  }

  assert {
    condition     = aws_vpc.main.cidr_block == "10.99.0.0/16"
    error_message = "VPC CIDR block does not match"
  }

  assert {
    condition     = length(aws_subnet.public) == 3
    error_message = "Expected 3 public subnets"
  }
}
```

**FR** — Depuis Terraform 1.6, utiliser les tests natifs HCL (`terraform test`) pour valider les modules sans outil externe. Plus simple que Terratest pour les validations basiques.

---

## 7. Drift Detection

### What Is Drift

**EN** — Drift occurs when the actual state of infrastructure diverges from the desired state defined in code. Causes: manual changes via console, failed applies, external processes modifying resources.

### Detecting Drift

```bash
# Terraform drift detection
terraform plan -detailed-exitcode
# Exit code 0 = no changes, 1 = error, 2 = changes detected (drift)
```

**EN** — Run drift detection on a schedule (daily or hourly for critical infrastructure). Alert on drift and auto-remediate when safe.

```yaml
# Scheduled drift detection in GitHub Actions
name: Drift Detection
on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8am UTC

jobs:
  detect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: |
          terraform init
          terraform plan -detailed-exitcode 2>&1 | tee plan-output.txt
          EXIT_CODE=$?
          if [ $EXIT_CODE -eq 2 ]; then
            echo "DRIFT DETECTED" >> $GITHUB_STEP_SUMMARY
            # Send alert to Slack/PagerDuty
          fi
        working-directory: infrastructure/environments/production
```

### GitOps-Based Drift Correction

**EN** — ArgoCD and Flux continuously reconcile desired state with actual state. Enable `selfHeal: true` in ArgoCD to automatically revert manual changes. This is the strongest form of drift prevention — the system corrects itself within minutes.

**FR** — ArgoCD et Flux reconcilent en continu l'etat desire avec l'etat reel. Activer `selfHeal: true` dans ArgoCD pour reverter automatiquement les changements manuels.

---

## 8. State Management Best Practices

### The State Management Checklist

1. **Remote backend**: Always use a remote backend with locking. Never use local state in team environments.
2. **State per component**: Split state by service and environment. A single state file for all infrastructure is fragile and slow.
3. **State encryption**: Encrypt at rest (S3 SSE, GCS encryption) and in transit (TLS).
4. **State access control**: Restrict who can read and write state. State files often contain sensitive outputs (database passwords, API keys).
5. **State backup**: Enable versioning on the state backend (S3 versioning). Allows recovery from corrupted state.
6. **Import existing resources**: Use `terraform import` or `pulumi import` to bring manually created resources under IaC management. Never recreate what already exists.
7. **State migrations**: Use `terraform state mv` to refactor module structure without destroying and recreating resources.
8. **Sensitive outputs**: Mark outputs containing secrets as `sensitive = true` in Terraform. Use `pulumi.secret()` in Pulumi.

```hcl
output "database_password" {
  value     = random_password.db.result
  sensitive = true
}
```

**FR** — La gestion de l'etat est le point de defaillance le plus critique de l'IaC. Suivre cette checklist systematiquement pour chaque nouveau projet.

### Cross-Stack References

```hcl
# Read outputs from another state file
data "terraform_remote_state" "networking" {
  backend = "s3"
  config = {
    bucket = "myorg-terraform-state"
    key    = "production/networking/terraform.tfstate"
    region = "eu-west-1"
  }
}

resource "aws_instance" "app" {
  subnet_id = data.terraform_remote_state.networking.outputs.private_subnet_ids[0]
}
```

**EN** — Use `terraform_remote_state` data sources or Terraform Cloud/Spacelift run triggers to create dependencies between state files. Keep cross-stack references minimal — they create implicit coupling.

**FR** — Utiliser `terraform_remote_state` pour lire les outputs d'un autre state. Minimiser les references inter-stacks — elles creent un couplage implicite.

---

## 9. Platform Engineering and IaC

### Golden Paths with Backstage Templates

Embed IaC best practices in Backstage software templates so that every new service starts with proper infrastructure:

```yaml
# Backstage template — scaffolds a new service with Terraform module
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: microservice-with-infra
  title: Microservice with Infrastructure
spec:
  parameters:
    - title: Service Details
      properties:
        serviceName:
          type: string
        environment:
          type: string
          enum: [dev, staging, production]
  steps:
    - id: fetch-skeleton
      action: fetch:template
      input:
        url: ./skeleton
    - id: publish
      action: publish:github
    - id: register
      action: catalog:register
```

**EN** — Platform engineering removes the need for every team to become IaC experts. Provide golden paths that embed security, observability, and deployment best practices by default. Teams customize parameters, not infrastructure architecture.

**FR** — Le platform engineering elimine le besoin pour chaque equipe de devenir experte en IaC. Fournir des golden paths qui integrent securite, observabilite et bonnes pratiques de deploiement par defaut.
