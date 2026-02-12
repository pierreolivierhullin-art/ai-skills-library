# Études de cas — Backend Development & Database Management

## Cas 1 : Optimisation d'une base PostgreSQL pour un SaaS analytics

### Contexte
InsightBoard, SaaS B2B d'analytics marketing, gère 500M de lignes d'événements dans une base PostgreSQL 15 hébergée sur AWS RDS (db.r6g.2xlarge). L'application utilise Prisma comme ORM avec un backend Node.js. 50 clients génèrent chacun 500K-5M d'événements par mois. Les dashboards client affichent des agrégations sur des périodes variables (7j, 30j, 90j, 12 mois).

### Problème
Les dashboards deviennent inutilisables : les requêtes d'agrégation sur 90 jours prennent 15-45 secondes. L'EXPLAIN ANALYZE révèle des sequential scans sur les tables d'événements malgré la présence d'index B-tree sur `tenant_id` et `created_at`. Le connection pool (PgBouncer) sature avec 200 connexions actives aux heures de pointe. Le coût RDS a doublé en 6 mois (scaling vertical) sans amélioration significative des performances.

### Approche
1. **Partitionnement par date** : Conversion de la table `events` (500M lignes) en table partitionnée par mois (`PARTITION BY RANGE (created_at)`). Chaque partition contient ~40M lignes. PostgreSQL élimine automatiquement les partitions non pertinentes lors des requêtes filtrées par date (partition pruning).
2. **Index couvrants et partiels** : Création d'index covering (`CREATE INDEX ... INCLUDE (value, metadata)`) pour les requêtes de dashboard, éliminant les heap fetches. Index partiels sur les événements récents (`WHERE created_at > NOW() - INTERVAL '90 days'`) pour les requêtes les plus fréquentes.
3. **Vues matérialisées** : Création de 3 vues matérialisées pré-agrégées (daily_metrics, weekly_metrics, monthly_metrics) par tenant et par type d'événement. Rafraîchissement incrémental toutes les 15 minutes via pg_cron. Les dashboards interrogent les vues matérialisées au lieu des tables brutes.
4. **Migration vers Supavisor** : Remplacement de PgBouncer par Supavisor pour un connection pooling plus efficace avec support du prepared statement protocol. Configuration en mode transaction pooling avec un pool de 50 connexions backend pour 500 connexions client.

### Résultat
- Temps de réponse dashboard passé de 15-45s à 200ms-1.2s (÷30)
- Sequential scans éliminés — 100% des requêtes dashboard utilisent des index ou des vues matérialisées
- Connexions backend réduites de 200 à 50 grâce au pooling optimisé
- Coût RDS réduit de 40% : retour à une instance db.r6g.xlarge (scaling down)
- Capacité à supporter 2× plus de clients sans modification d'infrastructure

### Leçons apprises
- Le partitionnement par date est le premier levier pour les tables d'événements à forte volumétrie — il doit être prévu dès la conception du schéma, pas après.
- Les vues matérialisées transforment les performances des dashboards analytics, mais le rafraîchissement doit être soigneusement planifié pour ne pas surcharger la base.
- EXPLAIN ANALYZE est l'outil le plus sous-utilisé — l'analyser systématiquement sur les 10 requêtes les plus fréquentes avant d'investir dans le scaling vertical.

---

## Cas 2 : Architecture backend multi-tenant avec Supabase et RLS

### Contexte
TeamBoard, startup SaaS de gestion de projets (12 personnes, 4 développeurs), lance un MVP avec Supabase comme backend. L'application Next.js utilise le client Supabase directement depuis le frontend pour les opérations CRUD. 200 équipes (tenants) utilisent la plateforme avec un total de 3000 utilisateurs.

### Problème
Après 6 mois de croissance rapide, un client signale qu'il voit les projets d'une autre équipe dans son dashboard. L'investigation révèle que les RLS policies sont incomplètes : la table `comments` n'a aucune policy (oubli lors d'une migration), et la policy de la table `tasks` vérifie `auth.uid() = user_id` au lieu de `team_id = (SELECT team_id FROM team_members WHERE user_id = auth.uid())`. Le client Supabase côté frontend a un accès direct à la base sans couche de validation intermédiaire.

### Approche
1. **Audit RLS complet** : Script SQL automatisé qui vérifie que chaque table accessible a au moins une RLS policy active pour SELECT, INSERT, UPDATE et DELETE. Résultat : 5 tables sur 18 sans policies complètes. Correction immédiate.
2. **Pattern de tenant isolation** : Création d'une fonction PostgreSQL `current_tenant_id()` qui extrait le `team_id` de l'utilisateur authentifié. Toutes les RLS policies utilisent cette fonction comme filtre. Un trigger `BEFORE INSERT` injecte automatiquement le `tenant_id` sur chaque insertion.
3. **Edge Functions comme API layer** : Migration des opérations critiques (création de projet, invitation de membres, modification de permissions) depuis les appels Supabase directs vers des Edge Functions Deno. Les Edge Functions utilisent le `service_role` key avec des validations métier explicites avant chaque opération.
4. **Tests RLS automatisés** : Suite de tests pgTAP qui vérifie l'isolation des données : un utilisateur du tenant A ne peut JAMAIS lire, modifier ou supprimer des données du tenant B. Ces tests s'exécutent dans le pipeline CI à chaque migration.

### Résultat
- Fuite de données cross-tenant éliminée — zéro incident en 8 mois depuis la remédiation
- 100% des tables avec RLS policies complètes et testées
- Tests RLS dans le CI : 47 assertions vérifiant l'isolation à chaque migration
- Confiance accrue des clients enterprise — le mécanisme d'isolation est auditable et documenté
- Temps de développement pour les nouvelles features réduit de 20% grâce aux patterns standardisés (tenant isolation automatique)

### Leçons apprises
- Le RLS Supabase est puissant mais fragile — un oubli de policy sur une seule table expose toutes les données de cette table. L'automatisation de la vérification est obligatoire.
- Le client Supabase en frontend ne doit JAMAIS être la seule couche de sécurité — les Edge Functions ajoutent une validation métier que le RLS ne peut pas exprimer.
- Les tests d'isolation doivent être traités comme des tests de sécurité critiques — ils s'exécutent à chaque migration, pas uniquement en release.

---

## Cas 3 : Migration d'ORM et optimisation N+1 pour une API GraphQL

### Contexte
SocialHub, plateforme de gestion de réseaux sociaux (30 personnes), expose une API GraphQL (Apollo Server) avec TypeORM sur PostgreSQL. L'API sert 10K requêtes/minute avec une latence p95 de 2.5 secondes. Le frontend React effectue des requêtes GraphQL imbriquées pour charger les dashboards : comptes sociaux → posts → métriques → commentaires.

### Problème
L'analyse des query plans révèle un problème massif de N+1 queries. Une seule requête GraphQL "tableau de bord" génère jusqu'à 450 requêtes SQL (1 pour les comptes + 15 par compte pour les posts + 10 par post pour les métriques). TypeORM charge les relations en lazy loading par défaut, et chaque resolver GraphQL déclenche des requêtes indépendantes. Le pool de connexions PostgreSQL sature 3 fois par jour, provoquant des timeouts.

### Approche
1. **DataLoader pattern** : Implémentation de DataLoader (Facebook) pour chaque entité. Les requêtes N+1 sont automatiquement regroupées en batch queries. Un DataLoader par requête GraphQL (scope per-request) pour éviter les problèmes de cache cross-request.
2. **Migration TypeORM → Drizzle ORM** : Migration progressive de TypeORM vers Drizzle ORM pour le type-safety et le contrôle explicite des jointures. Drizzle génère des requêtes SQL prévisibles et permet les jointures explicites avec `db.query.accounts.findMany({ with: { posts: { with: { metrics: true } } } })`.
3. **Query complexity analysis** : Implémentation d'un plugin Apollo Server qui calcule la complexité de chaque requête GraphQL et rejette les requêtes dépassant un seuil (score > 500). Cela empêche les requêtes excessivement imbriquées.
4. **Pagination par curseur** : Remplacement de la pagination offset (`LIMIT 20 OFFSET 100`) par la pagination par curseur (`WHERE id > :cursor ORDER BY id LIMIT 20`) pour les listes de posts et commentaires. Performance O(1) au lieu de O(n).

### Résultat
- Requêtes SQL par requête GraphQL réduites de 450 à 4-8 (×60)
- Latence p95 passée de 2.5s à 180ms (÷14)
- Saturation du connection pool éliminée — connexions actives réduites de 180 à 35
- Coût RDS réduit de 30% (downgrade d'instance possible)
- Migration Drizzle complétée en 8 semaines sans downtime (migration table par table)

### Leçons apprises
- Le N+1 query est le problème de performance #1 des APIs GraphQL — le DataLoader pattern doit être implémenté dès le premier jour, pas après.
- Les ORMs avec lazy loading par défaut (TypeORM, Sequelize) sont dangereux avec GraphQL — préférer des ORMs explicites (Drizzle, Prisma) qui forcent la déclaration des relations à charger.
- La pagination par curseur est dramatiquement plus performante que l'offset pour les grands datasets — le surcoût d'implémentation est minimal.
