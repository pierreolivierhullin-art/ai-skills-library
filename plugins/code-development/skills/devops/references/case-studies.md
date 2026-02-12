# Études de cas — DevOps

## Cas 1 : Construction d'une Internal Developer Platform

### Contexte
CloudScale, scale-up SaaS B2B de 120 personnes (40 développeurs répartis en 8 squads), opère 35 microservices sur Kubernetes (EKS). Chaque squad gère son propre pipeline CI/CD, ses Helm charts, et ses configurations Terraform. L'équipe plateforme (3 SREs) passe 80% de son temps à répondre aux tickets des développeurs : "mon déploiement a échoué", "comment créer un nouveau service", "je ne trouve pas les logs de staging".

### Problème
Le temps moyen de création d'un nouveau service est de 2 semaines (config K8s, pipeline CI, monitoring, base de données, secrets). Les développeurs passent 30% de leur temps sur des tâches d'infrastructure au lieu de coder des features. La charge cognitive est énorme : chaque développeur doit maîtriser Terraform, Helm, ArgoCD, Datadog, et les spécificités de 3 environnements. Les métriques DORA sont médiocres : deployment frequency de 2/semaine, lead time de 5 jours, change failure rate de 18%.

### Approche
1. **Backstage comme portail développeur** : Déploiement de Backstage (Spotify) comme Internal Developer Platform. Catalogue de services unifié avec ownership, documentation, SLOs, et dépendances. Chaque service est visible et navigable depuis un seul endroit.
2. **Software Templates** : Création de 4 templates Backstage pour les nouveaux services : "API Service" (Node.js/Fastify), "Worker" (processeur de queue), "Frontend" (Next.js), "Data Pipeline" (Python/Dagster). Chaque template provisionne automatiquement : repo GitHub, pipeline CI (GitHub Actions), Helm chart, namespace K8s, base de données, monitoring, et alertes.
3. **Golden paths** : Définition de "chemins pavés" standardisés pour les opérations courantes : déploiement, rollback, feature flags, database migration, secrets rotation. Les développeurs suivent le golden path par défaut et ne dévient que s'ils acceptent la charge de maintenance.
4. **GitOps avec ArgoCD** : Centralisation de tous les manifestes K8s dans un repo GitOps. ArgoCD réconcilie automatiquement l'état du cluster avec le repo. Les développeurs mergent un PR pour déployer — plus de `kubectl apply` manuel.

### Résultat
- Temps de création d'un nouveau service passé de 2 semaines à 30 minutes (template Backstage)
- Temps développeur sur l'infra réduit de 30% à 8% (libère ~9 devs-jours/semaine)
- DORA metrics : deployment frequency 12/semaine (×6), lead time 1.2 jours (÷4), change failure rate 6% (÷3)
- Tickets infra pour l'équipe plateforme réduits de 75% — les SREs passent 60% de leur temps sur des projets d'amélioration
- Onboarding d'un nouveau développeur : premier déploiement en production en 2 jours (vs 3 semaines)

### Leçons apprises
- Le platform engineering n'est pas un projet mais un produit — il faut l'itérer avec du feedback développeur, comme n'importe quel produit.
- Commencer par les golden paths avant de déployer un portail — la valeur vient de la standardisation, pas de l'outil.
- L'adoption se fait par la valeur, pas par le mandat — si le golden path est plus rapide que le DIY, les développeurs l'adoptent naturellement.

---

## Cas 2 : Pipeline CI/CD zero-downtime pour une app critique

### Contexte
PayEase, fintech de 50 personnes, traite 200K transactions/jour via une API déployée sur AWS ECS Fargate. Le pipeline CI/CD utilise GitHub Actions avec un déploiement direct en production après les tests. L'application est un monolithe Node.js avec une base PostgreSQL (RDS).

### Problème
3 incidents de production en 2 mois liés aux déploiements : une migration de base qui locke les tables pendant 8 minutes (transactions en timeout), un bug de régression non détecté par les tests déployé à 100% des utilisateurs, et un rollback qui prend 25 minutes car il nécessite un revert de migration. Le taux d'échec des déploiements est de 15%. Le stress des déploiements mène l'équipe à ne déployer que les mardis et jeudis, créant des batchs de changements risqués.

### Approche
1. **Blue-green deployments** : Migration de ECS rolling update vers un déploiement blue-green avec ALB (Application Load Balancer). Le nouveau code est déployé sur un nouveau target group ("green"), validé par des smoke tests automatiques, puis le trafic bascule instantanément. Rollback en 30 secondes (rebascule vers "blue").
2. **Zero-downtime migrations** : Adoption du pattern "expand and contract" pour les migrations de base : Phase 1 (expand) — ajouter la nouvelle colonne/table sans supprimer l'ancienne ; Phase 2 (migrate) — migrer les données ; Phase 3 (contract) — supprimer l'ancien schéma. Chaque phase est un déploiement séparé.
3. **Canary analysis automatisée** : Avant la bascule blue-green complète, 5% du trafic est envoyé au "green" pendant 10 minutes. Un job GitHub Actions compare les métriques (error rate, latence p95, status codes) entre blue et green. Si les métriques divergent de >10%, rollback automatique.
4. **Feature flags systématiques** : Intégration de LaunchDarkly. Chaque feature derrière un flag. Les déploiements ne changent que le code disponible — l'activation se fait séparément via le dashboard. Rollback d'une feature en 1 clic, sans redéploiement.

### Résultat
- Zéro downtime sur les 6 derniers mois (vs 3 incidents en 2 mois avant)
- Taux d'échec de déploiement réduit de 15% à 2%
- Temps de rollback passé de 25 minutes à 30 secondes (blue-green switch)
- Fréquence de déploiement passée de 2/semaine à 3/jour — les développeurs déploient avec confiance
- Lead time réduit de 5 jours à 4 heures (du commit au production)
- Migrations de base : zéro lock de table en production grâce au pattern expand-contract

### Leçons apprises
- Le blue-green deployment est le meilleur investissement pour la confiance en production — le rollback instantané change la psychologie de l'équipe.
- Les migrations zero-downtime exigent de la discipline (3 phases au lieu d'1) mais éliminent la classe entière de bugs de migration.
- Les feature flags découplent le déploiement technique de la release fonctionnelle — c'est le catalyseur du "deploy small, deploy often".

---

## Cas 3 : Sécurisation de la supply chain logicielle

### Contexte
SecureOps, éditeur SaaS de compliance (30 personnes), est certifié SOC 2 Type II et vise la certification ISO 27001. L'application utilise 450 dépendances npm, 30 images Docker, et déploie via GitHub Actions sur AWS EKS. Le pipeline CI exécute des tests mais aucun scan de sécurité.

### Problème
Un audit ISO 27001 pré-certification révèle des non-conformités critiques : aucune traçabilité de la chaîne de build (impossible de prouver que l'image en production correspond au code audité), 23 vulnérabilités CVE critiques dans les dépendances, des images Docker basées sur Ubuntu 22.04 avec 150+ packages inutiles, et des credentials longue durée dans GitHub Actions pour l'accès AWS.

### Approche
1. **SLSA Level 2 provenance** : Intégration de Sigstore (cosign) dans le pipeline. Chaque image Docker est signée avec une clé éphémère et une attestation de provenance SLSA L2 est générée. La provenance lie l'image au commit, au pipeline, et au builder de manière vérifiable cryptographiquement.
2. **Scanning automatisé en CI** : Trivy scanne les images Docker (vulnérabilités OS + application), Snyk analyse les dépendances npm (`snyk test`), et Checkov valide les configurations Terraform. Quality gate : zéro CVE critique/haute autorisée. Dependabot activé avec auto-merge pour les patches de sécurité.
3. **Images minimales** : Migration de toutes les images Docker de Ubuntu vers des images distroless (Google) ou Alpine. Les images passent de 800MB à 45MB. Réduction de la surface d'attaque de 90% (moins de packages = moins de CVEs potentielles).
4. **OIDC pour l'authentification cloud** : Remplacement de tous les AWS access keys dans GitHub Actions par l'OIDC federation (GitHub → AWS STS). Zéro credential longue durée. Chaque job obtient un token temporaire (1h max) avec des permissions minimales via des rôles IAM dédiés.

### Résultat
- Certification ISO 27001 obtenue — la traçabilité de la supply chain est citée comme point fort
- CVE critiques/hautes réduites de 23 à 0 (et maintenues à 0 via le scanning continu)
- Taille des images Docker réduite de 800MB à 45MB (÷18) — déploiements 4× plus rapides
- Zéro credential longue durée dans le CI — suppression d'un vecteur d'attaque majeur
- Chaque image en production est traçable jusqu'au commit source avec preuve cryptographique

### Leçons apprises
- La sécurité de la supply chain est devenue un prérequis de certification, pas un "nice-to-have" — intégrer dès le premier pipeline.
- Les images distroless/Alpine divisent la surface d'attaque ET le temps de déploiement — c'est un double bénéfice.
- L'OIDC federation élimine le problème de rotation des credentials cloud en CI — c'est la pratique standard qui devrait remplacer toute utilisation d'access keys.
