# Infrastructure & Cloud — Cloud Strategy, Multi-Cloud, Networking, DR & Edge Computing

## Overview

Ce document de reference couvre les fondamentaux de l'infrastructure IT et du cloud : strategie cloud (IaaS/PaaS/SaaS), comparatif des providers (AWS, GCP, Azure, OVH/Scaleway), multi-cloud et cloud souverain, architecture reseau, virtualisation et conteneurisation, plan de reprise d'activite (PRA/PCA), edge computing, FinOps/FOCUS et GreenOps. Utiliser ce guide pour concevoir, migrer et optimiser l'infrastructure IT, en privilegiant une approche cloud-smart plutot que cloud-first dogmatique.

---

## Strategie Cloud — IaaS, PaaS, SaaS

### Les trois modeles de service

| Modele | Controle client | Gestion provider | Cas d'usage typiques |
|---|---|---|---|
| **IaaS** (Infrastructure as a Service) | OS, runtime, applications, donnees | Serveurs, stockage, reseau, virtualisation | Workloads legacy migres, applications custom, tests/dev |
| **PaaS** (Platform as a Service) | Applications, donnees | OS, runtime, middleware, serveurs | Developpement d'applications, APIs, microservices |
| **SaaS** (Software as a Service) | Configuration, donnees | Tout le stack technique | CRM, ERP, collaboration, ITSM |

### Framework de decision par workload

Pour chaque workload, evaluer quatre dimensions :

1. **Criticite metier** : impact en cas d'indisponibilite (T1/T2/T3).
2. **Sensibilite des donnees** : donnees personnelles, donnees reglementees, propriete intellectuelle.
3. **Exigences de performance** : latence, debit, disponibilite (SLA 99.9%, 99.95%, 99.99%).
4. **Elasticite** : variabilite de la charge (saisonniere, evenementielle, previsible).

### Les 6R de la migration cloud

Pour chaque application du portefeuille, determiner la strategie de migration :

| Strategie | Description | Quand utiliser | Effort |
|---|---|---|---|
| **Retain** | Garder on-premise | Contraintes reglementaires, dependencies hardware, ROI negatif | Nul |
| **Retire** | Decommissionner | Application obsolete, < 10 utilisateurs, fonctionnalite couverte ailleurs | Faible |
| **Rehost** (Lift & Shift) | Migrer tel quel vers IaaS cloud | Migration rapide, premier pas vers le cloud, applications stables | Faible |
| **Replatform** | Ajustements mineurs pour le cloud | Beneficier de services manages (RDS, Cloud SQL) sans refonte | Moyen |
| **Refactor** | Reconcevoir pour le cloud-native | Applications strategiques necessitant scalabilite, performance, modernisation | Eleve |
| **Repurchase** | Remplacer par du SaaS | Solution SaaS mature existante, application non differenciante | Moyen |

### Plan de migration cloud type

```
Phase 1 — Assessment (4-8 semaines)
  - Inventaire du parc applicatif et infrastructure
  - Classification des workloads (criticite, sensibilite, complexite)
  - Attribution d'une strategie 6R a chaque workload
  - Estimation des couts cloud cibles (TCO comparatif on-premise vs cloud)
  - Identification des dependances et des risques

Phase 2 — Landing Zone (4-8 semaines)
  - Architecture multi-comptes / projets (AWS Organizations, Azure Management Groups, GCP Folders)
  - Reseau (VPC, subnets, peering, VPN/interconnexion)
  - Identite et acces (IAM, SSO, roles)
  - Securite (Security Hub, Defender, Security Command Center, WAF, KMS)
  - Monitoring et logging (CloudWatch, Azure Monitor, Cloud Monitoring)
  - FinOps (tagging, budgets, alertes)
  - IaC (Terraform modules pour la landing zone)

Phase 3 — Migration par vagues (3-18 mois)
  - Vague 1 : applications non critiques (test de la plateforme, montee en competence)
  - Vague 2 : applications departementales (premiers gains de productivite)
  - Vague 3 : applications critiques (migration avec PRA, bascule progressive)
  - Chaque vague : migration, tests, validation, bascule, optimisation

Phase 4 — Optimisation continue
  - FinOps : rightsizing, reserved instances, spot, savings plans
  - Performance : monitoring, tuning, auto-scaling
  - Securite : revue continue, conformite, audits
  - Modernisation : evolution progressive du rehost vers replatform/refactor
```

---

## Comparatif des Cloud Providers

### AWS, GCP, Azure — Positionnement

| Critere | AWS | Azure | GCP |
|---|---|---|---|
| **Part de marche mondiale** | ~31% | ~25% | ~11% |
| **Force principale** | Largeur de l'offre (200+ services), maturite | Integration ecosysteme Microsoft, hybride | Data/ML, Kubernetes (GKE), prix competitif |
| **Compute** | EC2, Lambda, ECS/EKS, Fargate | VMs, Azure Functions, AKS, Container Apps | Compute Engine, Cloud Run, GKE, Cloud Functions |
| **Storage** | S3, EBS, EFS, Glacier | Blob Storage, Managed Disks, Files | Cloud Storage, Persistent Disk, Filestore |
| **Database** | RDS, Aurora, DynamoDB, Redshift | SQL Database, Cosmos DB, Synapse | Cloud SQL, Spanner, BigQuery, Firestore |
| **Networking** | VPC, ELB, CloudFront, Route53, Direct Connect | VNet, Load Balancer, Front Door, ExpressRoute | VPC, Cloud Load Balancing, Cloud CDN, Interconnect |
| **AI/ML** | SageMaker, Bedrock, Rekognition | Azure ML, Azure OpenAI, Cognitive Services | Vertex AI, Gemini API, AutoML |
| **Prix (compute)** | Reference | Comparable (-5 a +5%) | Generalement 5-15% moins cher |
| **Regions Europe (FR)** | Paris (eu-west-3) | France Central (Paris) | europe-west9 (Paris) |
| **Certification SecNumCloud** | Non (mais partenariats) | Bleu (Orange/Capgemini) | S3NS (Thales) |

### Cloud souverain et acteurs europeens

| Provider | Pays | Force | Certification |
|---|---|---|---|
| **OVHcloud** | France | Souverainete, prix competitif, bare metal, Kubernetes (MKS) | SecNumCloud (certains DCs), HDS |
| **Scaleway** | France | Developer experience, serverless, bare metal GPU | HDS, en cours SecNumCloud |
| **Outscale (Dassault)** | France | Cloud de confiance, secteur defense, regulated industries | SecNumCloud |
| **T-Systems (Open Telekom Cloud)** | Allemagne | Souverainete allemande, basee sur OpenStack | C5 (BSI), en cours EUCS |
| **Ionos** | Allemagne | PME, prix competitif, datacenters europeens | ISO 27001, C5 |

### Recommandation de choix

- **Ecosysteme Microsoft (O365, Teams, Dynamics)** : privilegier Azure pour la coherence.
- **Workloads data/ML intensifs** : GCP offre BigQuery et Vertex AI parmi les meilleurs du marche.
- **Largeur de service et maturite** : AWS reste la reference en termes de profondeur de l'offre.
- **Souverainete et secteur public/defense** : OVHcloud, Outscale, ou offres souveraines S3NS/Bleu.
- **Startup / PME avec budget contraint** : Scaleway, OVH, ou GCP (credits startup genereux).

---

## Architecture Multi-Cloud

### Quand le multi-cloud est justifie

Le multi-cloud veritable (meme workload sur plusieurs providers) est rarement justifie. Le multi-cloud pragmatique (workloads differents sur des providers differents) est courant et souvent pertinent :

| Scenario | Justification | Approche |
|---|---|---|
| **Best-of-breed** | Exploiter les forces de chaque provider | GCP pour la data, AWS pour l'infra generique, Azure pour O365 |
| **Resilience** | Eviter la dependance a un seul provider | Provider principal + provider secondaire pour les workloads critiques |
| **Reglementaire** | Contraintes de localisation ou de souverainete | Cloud public pour les workloads standards, cloud souverain pour les donnees sensibles |
| **M&A** | Heritage de providers differents apres fusion/acquisition | Rationaliser progressivement vers une strategie coherente |

### Patterns d'architecture multi-cloud

- **Abstraction layer** : utiliser Terraform / Pulumi pour abstraire les providers. Definir des modules reutilisables par provider avec une interface commune. Attention : l'abstraction complete est illusoire, chaque provider a ses specificites.
- **Mesh networking** : interconnecter les clouds via des passerelles VPN ou des solutions d'interconnexion privee (AWS Direct Connect, Azure ExpressRoute, GCP Interconnect). Utiliser un mesh reseau (Aviatrix, Alkira) pour simplifier la connectivite multi-cloud.
- **Data gravity** : les donnees sont difficiles et couteuses a deplacer. Placer le compute pres des donnees, pas l'inverse. Definir un "data home" par dataset et minimiser les transferts cross-cloud.
- **Unified observability** : utiliser une plateforme d'observabilite multi-cloud (Datadog, Grafana Cloud, Dynatrace) pour avoir une vue unifiee des performances et des couts.

---

## Architecture Reseau

### Principes de conception reseau

1. **Segmentation** : separer les environnements (production, staging, dev) et les zones de securite (DMZ, interne, gestion) par des VPC/VNet distincts.
2. **Zero Trust** : ne jamais faire confiance au reseau. Authentifier et autoriser chaque flux, meme interne. Implementer la micro-segmentation.
3. **Defense en profondeur** : WAF en peripherie, firewalls entre segments, IDS/IPS, chiffrement en transit et au repos.
4. **Haute disponibilite** : architecture multi-AZ pour les workloads critiques, redondance des composants reseau (load balancers, passerelles).

### Architecture reseau cloud type

```
[Internet]
     |
[CDN / WAF]  (CloudFront + AWS WAF / Azure Front Door / Cloud Armor)
     |
[Load Balancer public]  (ALB / Azure LB / Cloud LB)
     |
[VPC/VNet Production]
  +-- Subnet public (bastion, NAT Gateway)
  +-- Subnet applicatif (app servers, containers)
  +-- Subnet donnees (RDS, Redis, ElastiCache)
  +-- Subnet management (monitoring, CI/CD runners)
     |
[Peering / Transit Gateway]
     |
[VPC/VNet Corporate / On-premise]  (via VPN ou Direct Connect)
```

### Connectivite hybride (cloud <-> on-premise)

| Solution | Debit | Latence | Cout | Usage |
|---|---|---|---|---|
| **VPN Site-to-Site** | Jusqu'a 1.25 Gbps | Variable (internet) | Faible | PME, workloads non critiques |
| **Direct Connect / ExpressRoute / Interconnect** | 1-100 Gbps | Previsible, faible | Eleve (500-5000 EUR/mois) | Workloads critiques, gros volumes |
| **SD-WAN** | Variable | Optimisee | Moyen | Multi-sites, QoS, agilite |

---

## Virtualisation & Conteneurisation

### Virtualisation (VMs)

La virtualisation reste pertinente pour :
- Applications legacy non conteneurisables
- Workloads Windows (Active Directory, SQL Server)
- Environnements necessitant un isolement fort (multi-tenancy securisee)
- Solutions VMware existantes (migration vers VMware Cloud on AWS, Azure VMware Solution, ou Google Cloud VMware Engine)

### Conteneurisation (Docker / Kubernetes)

La conteneurisation est le standard de facto pour les applications cloud-native :

**Docker** — bonnes pratiques :
- Images multi-stage pour reduire la taille
- Base images minimales (distroless, Alpine, Chainguard)
- Ne jamais utiliser `:latest` en production, toujours tagger avec le SHA du commit
- Scanner les images (Trivy, Snyk Container, Grype) dans le pipeline CI/CD
- Ne pas stocker de secrets dans les images (utiliser des secrets managers)
- Un processus par conteneur (separation des concerns)

**Kubernetes** — guide de choix :
| Option | Quand utiliser | Complexite |
|---|---|---|
| **Managed K8s** (EKS, GKE, AKS) | Majorite des cas, focus sur les applications | Moyenne |
| **Serverless containers** (Fargate, Cloud Run, Container Apps) | Workloads stateless, scaling rapide, simplification | Faible |
| **Self-managed K8s** | Edge, air-gapped, contraintes specifiques | Elevee |
| **Managed K8s souverain** (OVH MKS, Scaleway Kapsule) | Souverainete, cout, marche europeen | Moyenne |

### Serverless

Le serverless (FaaS : Lambda, Cloud Functions, Azure Functions) est pertinent pour :
- Evenements et triggers (traitement de fichiers, webhooks, event-driven)
- APIs a trafic variable (scaling automatique a zero)
- Batch processing et ETL legers
- Prototypage rapide

Attention aux limites : cold starts, duree d'execution maximale (15 min Lambda), complexite de debugging, vendor lock-in.

---

## PRA/PCA — Plan de Reprise et de Continuite d'Activite

### Definitions

- **PCA (Plan de Continuite d'Activite)** : ensemble des mesures pour maintenir l'activite en cas de sinistre.
- **PRA (Plan de Reprise d'Activite)** : ensemble des mesures pour reprendre l'activite apres un sinistre.
- **RPO (Recovery Point Objective)** : perte de donnees maximale acceptable (ex : 1 heure = on accepte de perdre jusqu'a 1h de donnees).
- **RTO (Recovery Time Objective)** : duree maximale d'indisponibilite acceptable (ex : 4 heures = le service doit etre restaure en moins de 4h).

### Strategies de DR par niveau de criticite

| Niveau | RPO | RTO | Strategie | Cout relatif |
|---|---|---|---|---|
| **Tier 1** (Critique) | < 15 min | < 1 h | Active-Active (multi-region) | Tres eleve (x2-3) |
| **Tier 2** (Important) | < 1 h | < 4 h | Warm Standby (infra pre-provisionnee) | Eleve (x1.5-2) |
| **Tier 3** (Standard) | < 24 h | < 24 h | Pilot Light (infra minimale, scaling a la demande) | Moyen (x1.2-1.5) |
| **Tier 4** (Non critique) | < 72 h | < 72 h | Backup & Restore (backups, reconstruction on demand) | Faible (x1.1) |

### Architecture DR multi-region

```
[Region primaire (Paris)]          [Region secondaire (Francfort)]
  +-- Application (active)            +-- Application (standby ou active)
  +-- Base de donnees (primary)       +-- Base de donnees (replica async/sync)
  +-- Stockage (primary)              +-- Stockage (replique cross-region)
  +-- DNS : 100% trafic                +-- DNS : 0% (failover) ou 50% (active-active)
```

### Tests de DR

Tester le PRA au minimum une fois par an (deux fois pour les Tier 1). Types de tests :
- **Tabletop exercise** : simulation sur papier, parcours des procedures. Faible cout, premier niveau de validation.
- **Walkthrough** : test des procedures pas a pas sans bascule reelle. Validation de la documentation.
- **Simulation** : bascule reelle en environnement de test isole. Validation technique.
- **Full failover** : bascule reelle en production vers la region secondaire. Validation complete. A planifier soigneusement.

---

## Edge Computing

### Definition et cas d'usage

L'edge computing rapproche le traitement des donnees du lieu ou elles sont generees, plutot que de les envoyer vers un datacenter central ou le cloud.

Cas d'usage pertinents :
- **IoT industriel** : traitement en temps reel des capteurs (predictive maintenance, quality control) sur site de production.
- **Retail / Point de vente** : caisses autonomes, digital signage, analytics video en magasin.
- **Sante** : dispositifs medicaux connectes avec traitement local pour la latence et la conformite.
- **Vehicules autonomes / drones** : traitement embarque pour les decisions en temps reel.
- **CDN / Media** : distribution de contenu au plus pres des utilisateurs (Cloudflare Workers, AWS CloudFront Functions, Fastly Compute).

### Architecture edge

```
[Cloud Central]
  +-- Orchestration (Fleet management, config, updates)
  +-- Data lake (donnees agregees, ML training)
  +-- Monitoring centralise
       |
  [Edge Gateway / Hub]
  +-- Compute local (inference ML, pre-traitement)
  +-- Stockage temporaire (buffer, cache)
  +-- Connectivite (4G/5G, WiFi, LoRa)
       |
  [Devices / Capteurs]
  +-- Acquisition de donnees
  +-- Actions locales (actuateurs)
```

Solutions : AWS IoT Greengrass, Azure IoT Edge, GCP Anthos for Edge, AWS Outposts, Azure Stack Edge, k3s/k0s pour Kubernetes edge.

---

## FinOps & GreenOps

### FinOps — Framework FOCUS

Le FinOps est la discipline de gestion financiere du cloud. Le standard FOCUS (FinOps Open Cost and Usage Specification) normalise les donnees de couts multi-cloud pour permettre la comparaison et l'analyse cross-provider.

#### Les trois phases du FinOps

1. **Inform** : visibilite sur les couts. Tagging obligatoire (equipe, projet, environnement), reporting par centre de cout, allocation des couts partages.
2. **Optimize** : reduction des couts. Rightsizing, reserved instances, savings plans, spot instances, suppression des ressources orphelines, auto-shutdown dev/test.
3. **Operate** : gouvernance continue. Budgets et alertes, revues mensuelles par equipe, KPIs FinOps, integration dans le cycle de decision.

#### Leviers d'optimisation

| Levier | Potentiel de reduction | Effort |
|---|---|---|
| **Suppression des ressources inutilisees** | 10-30% | Faible |
| **Rightsizing** (ajuster la taille des instances) | 10-20% | Moyen |
| **Reserved Instances / Savings Plans** (engagement 1-3 ans) | 30-60% | Moyen |
| **Spot Instances** (workloads tolerants aux interruptions) | 60-90% | Eleve |
| **Auto-scaling** (ajuster la capacite a la demande) | 10-30% | Moyen |
| **Choix de region** (regions moins cheres) | 5-15% | Faible |
| **Architecture serverless** (payer a l'usage) | Variable | Eleve |

#### KPIs FinOps

| KPI | Description | Cible |
|---|---|---|
| **Cloud spend vs budget** | Ecart entre la depense reelle et le budget | < 5% d'ecart |
| **Coverage rate** (RI/SP) | % de la depense couverte par des engagements | > 70% pour les workloads stables |
| **Waste rate** | % de ressources inutilisees ou surdimensionnees | < 10% |
| **Unit cost** | Cout par transaction, par utilisateur, par requete | Tendance decroissante |
| **Tagging compliance** | % de ressources correctement taguees | > 95% |

### GreenOps — IT Durable

Le GreenOps etend le FinOps a la dimension environnementale :
- **Mesurer** : utiliser les outils de carbon footprint des providers (AWS Customer Carbon Footprint Tool, Azure Emissions Impact Dashboard, Google Carbon Footprint).
- **Reduire** : choisir des regions alimentees en energie renouvelable, optimiser le rightsizing (moins de compute = moins d'energie), utiliser le serverless (mutualisation), eteindre les ressources non utilisees.
- **Compenser** : en dernier recours, apres optimisation, compenser les emissions residuelles.
- **Reporter** : integrer les metriques carbone IT dans le reporting ESG/RSE de l'entreprise (scope 2 et scope 3).

---

## State of the Art (2024-2026)

### Tendances majeures en infrastructure et cloud

1. **Platform Engineering et IDP** : les equipes infrastructure evoluent vers le platform engineering. Au lieu de gerer des tickets de provisioning, elles construisent des plateformes self-service (Internal Developer Platforms) basees sur Backstage, Port ou Kratix. Les developpeurs deploient en autonomie via des golden paths pre-configures (templates, pipelines, guardrails). Cela reduit le time-to-production de semaines a heures.

2. **FinOps generalisee et FOCUS standard** : le FinOps devient une pratique standard dans toute organisation cloud. Le standard FOCUS permet enfin la comparaison normalisee des couts entre AWS, Azure et GCP. Les outils de FinOps (Apptio, CAST AI, Kubecost) integrent l'IA pour les recommandations automatiques d'optimisation. Les equipes infra sont desormais comptables de leurs couts.

3. **Cloud souverain europeen mature** : les offres de cloud souverain (S3NS, Bleu, Outscale, OVHcloud SecNumCloud) atteignent un niveau de maturite fonctionnelle suffisant pour les workloads de production. Le label SecNumCloud 3.2 de l'ANSSI et la future certification europeenne EUCS (European Union Cybersecurity Certification Scheme for Cloud) deviennent des criteres de selection cles. Les secteurs regules (finance, sante, defense, secteur public) basculent vers ces offres.

4. **GPU Cloud et AI Infrastructure** : l'explosion de la demande en GPU pour l'IA generative transforme le marche cloud. Les providers (AWS avec les instances P5/Trainium, GCP avec les TPU v5, Azure avec les GPU AMD MI300X) se livrent une guerre pour l'offre GPU. Les startups (CoreWeave, Lambda Labs, Together AI) offrent du GPU as a Service specialise. L'optimisation de l'inference (quantization, distillation, batching) devient une competence infra cle.

5. **Infrastructure as Code mature et policy-as-code** : Terraform reste le leader de l'IaC mais Pulumi (IaC en langages de programmation reels) gagne du terrain. L'OpenTofu (fork open source de Terraform apres le changement de licence HashiCorp/IBM) se consolide. La policy-as-code (OPA/Rego, Kyverno, Sentinel, Cedar) permet d'encoder les regles de gouvernance (securite, couts, conformite) et de les appliquer automatiquement dans les pipelines.

6. **Kubernetes comme couche d'abstraction universelle** : Kubernetes n'est plus seulement un orchestrateur de conteneurs : il devient la couche d'abstraction universelle pour toute l'infrastructure. Crossplane permet de provisionner des ressources cloud via des CRDs Kubernetes. ArgoCD/Flux gerent le GitOps. Backstage construit des portails developpeurs par-dessus. L'ecosysteme CNCF (Cloud Native Computing Foundation) compte 200+ projets graduates et incubating.

7. **Reseau Zero Trust et SASE** : le modele de securite perimetrique (chateau fort) est definitvement abandonne au profit du Zero Trust. Les solutions SASE (Secure Access Service Edge) combinent SD-WAN + CASB + ZTNA + SWG dans une offre unifiee (Zscaler, Palo Alto Prisma Access, Cloudflare One). La micro-segmentation (Illumio, Guardicore/Akamai) complete l'approche en securisant les flux internes.

8. **Edge AI et 5G private** : l'edge computing connait un regain d'interet avec l'IA generative embarquee et la 5G privee. Les cas d'usage industriels (quality inspection par vision par ordinateur, predictive maintenance, robotique) justifient le deploiement d'une infrastructure edge avec inference ML locale. Les solutions de 5G privee (Nokia, Ericsson, AWS Private 5G) offrent la connectivite necessaire pour les sites industriels.

9. **Disaster Recovery as Code** : les PRA/PCA evoluent vers des approches codifiees et testables. L'IaC permet de reconstruire toute l'infrastructure en quelques minutes. Les tests de DR automatises (AWS Elastic Disaster Recovery, Azure Site Recovery) remplacent les tests annuels manuels. Le chaos engineering (Gremlin, LitmusChaos) teste en continu la resilience des systemes.

10. **Observability-as-Code et OpenTelemetry** : OpenTelemetry devient le standard de facto pour l'instrumentation des applications (metriques, logs, traces). Les pipelines d'observabilite sont codifies (Terraform pour les dashboards, alertes en code). Les plateformes (Datadog, Grafana Cloud, Dynatrace) convergent vers une offre unifiee metriques + logs + traces + profiling + RUM.
