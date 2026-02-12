# Études de cas — Process Engineering

## Cas 1 : Amélioration des métriques DORA d'une équipe engineering

### Contexte
DataVault, éditeur SaaS de data governance (90 personnes, 25 développeurs en 5 squads), mesure ses métriques DORA pour la première fois lors d'un assessment engineering. L'entreprise utilise Jira, GitHub, et déploie sur AWS via un pipeline Jenkins custom.

### Problème
Les résultats DORA sont alarmants : deployment frequency de 1 release/mois (batch de 80-120 PRs), lead time for changes de 21 jours (du commit au production), change failure rate de 22% (1 release sur 5 nécessite un hotfix), MTTR de 6 heures (debugging difficile car trop de changements par release). L'équipe est classée "Low performer" selon le benchmark DORA. Les développeurs sont frustrés par les cycles longs et les releases stressantes.

### Approche
1. **Diagnostic du value stream** : Mapping complet du flux de livraison avec timestamps réels : coding (3 jours) → PR review (5 jours) → QA manual testing (4 jours) → staging deployment (2 jours) → change advisory board approval (3 jours) → production (4 jours). Le ratio temps actif/temps d'attente est de 25%/75%.
2. **Élimination des bottlenecks** : Suppression du QA manual testing (remplacé par des tests automatisés en CI), suppression du change advisory board (remplacé par des quality gates automatisés), migration Jenkins → GitHub Actions avec des pipelines standardisés.
3. **Trunk-based development** : Migration du GitFlow (branches develop, release, hotfix) vers le trunk-based development. PRs limitées à 200 lignes, feature flags (Unleash) pour découpler deploy de release, branches de < 1 jour.
4. **Engineering metrics dashboard** : Déploiement de LinearB pour mesurer en continu les DORA metrics, cycle time, PR review time, et coding time. Dashboard visible par tous. Revue hebdomadaire des tendances en retrospective.

### Résultat
- Deployment frequency passée de 1/mois à 8/semaine (×32)
- Lead time réduit de 21 jours à 1.8 jour (÷12)
- Change failure rate réduit de 22% à 4% (releases plus petites = moins de risque)
- MTTR réduit de 6h à 35 min (rollback rapide + changements isolés)
- Classification DORA passée de "Low" à "Elite" en 6 mois
- Developer satisfaction (survey) passée de 3.5/10 à 8/10

### Leçons apprises
- Le value stream mapping révèle que 75% du lead time est du temps d'attente, pas du temps de travail — les plus gros gains viennent de l'élimination des queues et des approbations manuelles.
- Le trunk-based development est le catalyseur principal des métriques DORA elite — il force des PRs petites, des tests robustes, et un déploiement continu.
- Les métriques DORA doivent être visibles et discutées en équipe — la transparence crée l'élan d'amélioration.

---

## Cas 2 : Programme d'onboarding développeur accéléré

### Contexte
FinBridge, fintech de 60 personnes en hypercroissance, embauche 15 développeurs en 6 mois. L'équipe existante de 20 développeurs travaille sur un monolithe TypeScript/Next.js avec Supabase, déployé sur Vercel. Il n'existe aucun processus d'onboarding formalisé — chaque nouveau développeur est "parrainé" par un senior qui lui montre le codebase pendant 2-3 semaines.

### Problème
Le time-to-first-commit (premier commit en production) est de 4 semaines en moyenne. Les seniors passent 40% de leur temps à onboarder, réduisant leur productivité. Les nouveaux développeurs posent les mêmes questions répétitives (comment configurer l'env local, comment déployer, où trouver la doc API, comment tester). Le turnover des nouveaux est de 25% dans les 6 premiers mois — ils citent la frustration de l'onboarding comme raison principale.

### Approche
1. **Devcontainer standardisé** : Création d'un `.devcontainer` Docker avec toutes les dépendances (Node.js, PostgreSQL local, Redis, Supabase CLI, extensions VS Code, seed data). Le nouvel arrivant clone le repo, ouvre dans VS Code → Codespaces, et a un environnement fonctionnel en < 10 minutes.
2. **Documentation-as-code** : Migration de la documentation depuis Notion (désynchronisée) vers le repo (Markdown). Structure : `/docs/getting-started.md`, `/docs/architecture/`, `/docs/runbooks/`, `/docs/adr/`. Freshness checks automatisés : un bot alerte si un doc n'a pas été mis à jour depuis 90 jours alors que le code associé a changé.
3. **Onboarding pathway gamifié** : Création de 20 "quests" progressives dans un fichier `ONBOARDING.md` : Quest 1 (jour 1) → configurer l'env, Quest 2 → fixer un bug tagué "good first issue", Quest 5 → shipper une feature derrière un feature flag, Quest 10 → faire une PR de > 100 lignes avec tests, Quest 20 → être reviewer sur 3 PRs.
4. **Buddy program structuré** : Chaque nouvel arrivant a un buddy (pas son manager) pendant 30 jours. Le buddy consacre 30 min/jour (pas plus) pour des check-ins. Un template de check-in guide la conversation : blocages, apprentissages, feedback sur le processus.

### Résultat
- Time-to-first-commit réduit de 4 semaines à 3 jours (÷9)
- Temps des seniors sur l'onboarding réduit de 40% à 10% (devcontainer + docs + quests remplacent 80% du pairing)
- Turnover 6 mois des nouveaux réduit de 25% à 5%
- 100% des nouveaux développeurs complètent les 10 premières quests en < 2 semaines
- eNPS des nouveaux (survey à 30 jours) passé de +5 à +52
- La documentation est maintenant à jour (freshness check) — les questions répétitives ont chuté de 80%

### Leçons apprises
- Le devcontainer est le ROI le plus élevé de l'onboarding — éliminer les 2-3 jours de "ça marche pas sur ma machine" transforme la première impression.
- La documentation dans le repo (pas dans un wiki séparé) est la seule qui reste à jour — la proximité avec le code force la maintenance.
- Le buddy program structuré est crucial — sans cadre, le buddy fait trop ou pas assez. Le template de 30 min/jour est le bon format.

---

## Cas 3 : Mise en place d'un processus RFC pour les décisions techniques

### Contexte
AdTech, plateforme de publicité programmatique (100 personnes, 30 développeurs), évolue rapidement avec 5-8 décisions techniques majeures par mois : choix de base de données, migration de framework, adoption d'un nouveau service cloud, changement d'architecture. Les décisions sont prises en réunion informelle entre 2-3 personnes et rarement documentées.

### Problème
Des décisions techniques coûteuses sont prises sans consultation large : migration vers MongoDB décidée par 2 développeurs (sans consulter l'équipe data qui avait des besoins relationnels), adoption de Kubernetes décidée sans évaluer les alternatives serverless, et remplacement de l'ORM sans migration plan. Les développeurs non-consultés découvrent les changements au moment de l'implémentation et contestent les choix — débats tardifs, rework, frustration. L'absence de documentation rend impossible de comprendre pourquoi un choix a été fait 6 mois plus tard.

### Approche
1. **Processus RFC (Request for Comments)** : Toute décision ayant un impact sur plus de 2 équipes ou coûtant plus de 2 semaines-développeur nécessite une RFC. Template structuré : Problème, Contexte, Proposition, Alternatives envisagées, Impact (équipes, migration, coût), Plan d'implémentation, Questions ouvertes.
2. **Workflow de review** : La RFC est soumise en PR sur le repo `engineering-rfcs`. Période de commentaire de 5 jours ouvrés. Minimum 2 reviewers de squads différentes. L'auteur doit répondre à chaque commentaire. Décision finale par le tech lead concerné après la période de review.
3. **ADR pour les décisions finales** : Chaque RFC approuvée génère un ADR (Architecture Decision Record) résumant le contexte, la décision et les conséquences. Les ADR sont versionnés et consultables.
4. **Catalogue de décisions** : Un site statique (Docusaurus) auto-généré depuis les RFCs et ADR, searchable, avec des tags par domaine (backend, frontend, infra, data). Les développeurs consultent le catalogue avant de proposer une nouvelle RFC pour éviter les doublons.

### Résultat
- 45 RFCs rédigées en 6 mois — 38 approuvées, 5 rejetées (économisant 12 semaines-dev de mauvais choix), 2 en cours
- Contestation tardive de décisions réduite de 80% — les désaccords s'expriment pendant la période de review
- Temps de la RFC au début de l'implémentation : 8 jours (période de review + itération) — un investissement qui évite des semaines de rework
- 100% des décisions techniques majeures documentées et traçables
- Onboarding technique accéléré — les nouveaux développeurs lisent les RFCs pour comprendre l'histoire des choix

### Leçons apprises
- Le processus RFC transforme les décisions techniques de "politique informelle" en "ingénierie rationnelle" — la qualité des décisions augmente significativement.
- La période de review de 5 jours semble lente mais évite les mois de rework — c'est un investissement massif en prévention.
- Le catalogue searchable de décisions est aussi précieux que les décisions elles-mêmes — il évite de redébattre des sujets déjà tranchés.
