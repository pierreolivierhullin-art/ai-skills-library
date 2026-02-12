# Études de cas — Auth & Security

## Cas 1 : Migration vers une architecture Zero Trust

### Contexte
MédiCloud, éditeur SaaS santé de 70 personnes, héberge des données de santé (HDS) pour 150 établissements. L'architecture repose sur un réseau privé (VPC) avec des services communiquant en HTTP non chiffré en interne, un VPN pour l'accès des développeurs, et une authentification par session cookies sur un Identity Provider legacy (Keycloak 15, non maintenu).

### Problème
Un audit de sécurité mandaté par l'ANSSI révèle des failles critiques : communication inter-services non chiffrée, accès développeur trop permissif (tous les devs ont accès à toutes les bases de données de production), absence de segmentation réseau, et tokens de session avec un TTL de 30 jours sans rotation. Le rapport conclut que la compromission d'un seul service permettrait un mouvement latéral vers toutes les données patients. L'entreprise a 6 mois pour remédier sous peine de perte de la certification HDS.

### Approche
1. **mTLS entre tous les services** : Déploiement d'un service mesh (Istio) sur le cluster Kubernetes. Chaque service dispose d'un certificat TLS géré par cert-manager avec rotation automatique toutes les 24h. Communication inter-services chiffrée et mutuellement authentifiée.
2. **Migration vers OAuth 2.1 + Passkeys** : Remplacement de Keycloak 15 par Keycloak 24 avec support OAuth 2.1, PKCE obligatoire pour tous les clients, et intégration des passkeys (WebAuthn) comme méthode d'authentification primaire. Access tokens avec TTL de 5 minutes, refresh token rotation on use.
3. **Policy engine centralisé** : Déploiement d'Open Policy Agent (OPA) comme policy engine centralisé. Toutes les décisions d'autorisation passent par OPA avec des policies écrites en Rego, versionnées et testées en CI. RBAC granulaire : les développeurs n'accèdent qu'aux services de leur squad.
4. **Layered authorization** : Implémentation de RLS (Row-Level Security) dans PostgreSQL pour l'isolation des données par établissement. Chaque requête est filtrée au niveau base de données, indépendamment de la couche applicative.

### Résultat
- Certification HDS maintenue — audit de remediation passé avec zéro non-conformité critique
- Surface d'attaque réduite de 85% : un service compromis ne peut plus accéder aux données d'autres services
- Temps de propagation d'un incident de sécurité (blast radius) réduit de "toute l'infra" à "un service isolé"
- 92% des utilisateurs adoptent les passkeys en 3 mois (UX supérieure aux mots de passe)
- Temps d'accès développeur à la production passé de "permanent" à "just-in-time" (30 min max par session)

### Leçons apprises
- Le Zero Trust n'est pas un produit mais une architecture — il faut repenser chaque couche de communication et d'accès.
- Le service mesh (Istio) simplifie le mTLS mais ajoute une complexité opérationnelle significative — prévoir 2 mois de montée en compétence de l'équipe SRE.
- Les passkeys offrent une UX supérieure ET une sécurité supérieure — c'est le rare cas où sécurité et expérience utilisateur s'alignent parfaitement.

---

## Cas 2 : Sécurisation d'une API multi-tenant B2B

### Contexte
ApiForge, éditeur d'une plateforme d'intégration API (iPaaS) pour les ETI, gère 80 clients avec des milliers de workflows automatisés transitant par la plateforme. L'architecture est un monolithe Node.js/Express avec une base PostgreSQL partagée. L'authentification utilise des API keys statiques stockées en variables d'environnement.

### Problème
Un incident de sécurité majeur : une API key d'un client a fuité dans un dépôt GitHub public (commitée accidentellement par un développeur). Avant la détection (72h), un attaquant a pu accéder aux données de ce client et, en exploitant une faille d'IDOR (Insecure Direct Object Reference), a consulté les configurations de 12 autres clients. L'investigation révèle : aucune isolation des données par tenant au niveau base, API keys sans expiration ni rotation, absence de rate limiting, logs insuffisants pour le forensic.

### Approche
1. **Row-Level Security** : Migration vers une architecture où chaque requête SQL est filtrée par le `tenant_id` via des PostgreSQL RLS policies. Le `tenant_id` est extrait du JWT et injecté dans le contexte de session PostgreSQL (`SET app.current_tenant`). Impossible d'accéder aux données d'un autre tenant, même avec une faille applicative.
2. **OAuth 2.1 + API keys rotatives** : Remplacement des API keys statiques par un système OAuth 2.1 Client Credentials pour le M2M. Les API keys legacy sont migrées vers des tokens avec TTL de 90 jours et rotation automatique. Notification email 30 jours avant expiration.
3. **Rate limiting et abuse detection** : Implémentation de rate limiting par tenant (Redis + token bucket algorithm) avec des limites par endpoint et par tenant. Détection d'anomalies : alertes sur les pics de requêtes, les accès à des ressources inhabituelles, et les patterns de scanning.
4. **Security monitoring** : Logging structuré de chaque action avec `tenant_id`, `user_id`, `ip`, `action`, `resource_id`. Dashboard de sécurité en temps réel (Datadog) avec alertes sur les événements critiques : failed auth attempts, privilege escalation, cross-tenant access attempts.

### Résultat
- Isolation des données garantie au niveau base de données — même une faille applicative ne permet plus d'accéder aux données d'un autre tenant
- Temps de détection d'incident (MTTD) réduit de 72h à 15 minutes grâce au monitoring et aux alertes
- Zéro fuite de données cross-tenant depuis l'implémentation (12 mois)
- Conformité SOC 2 Type II obtenue — requis par 60% des prospects enterprise
- API keys sans rotation éliminées — 100% des clients migrés vers le nouveau système en 4 mois

### Leçons apprises
- Le RLS au niveau PostgreSQL est la dernière ligne de défense la plus robuste pour le multi-tenant — il fonctionne même quand le code applicatif a des bugs.
- Les API keys statiques sont une bombe à retardement — toute API key doit avoir une expiration et un mécanisme de rotation automatique.
- Le security monitoring proactif est aussi important que la prévention — sans detection capabilities, les incidents durent des jours au lieu de minutes.

---

## Cas 3 : Implémentation de passkeys et passwordless pour un SaaS grand public

### Contexte
FitTrack, application mobile et web de fitness avec 2M d'utilisateurs actifs, utilise une authentification classique email/mot de passe avec TOTP comme MFA optionnel. Le taux d'adoption du MFA est de 8%. L'application est développée en React Native (mobile) et Next.js (web) avec un backend Node.js.

### Problème
L'entreprise subit 15-20 tentatives de credential stuffing par semaine (utilisation de mots de passe volés sur d'autres services). 30% des tickets support concernent des problèmes de mot de passe (oubli, réinitialisation, blocage MFA). Le taux de conversion signup est de 35% — l'analyse montre que 40% des abandons se font à l'étape de création de mot de passe. La CNIL recommande un renforcement de l'authentification suite à un contrôle.

### Approche
1. **Passkeys comme méthode primaire** : Implémentation de WebAuthn/FIDO2 via la librairie SimpleWebAuthn côté serveur et les APIs natives des navigateurs/OS. Les passkeys sont proposées comme méthode d'inscription par défaut, avec email/mot de passe comme fallback.
2. **Magic links comme alternative** : Pour les utilisateurs sur des appareils ne supportant pas les passkeys, implémentation de magic links par email (lien à usage unique, TTL de 10 minutes, rate limited).
3. **Migration progressive** : Les utilisateurs existants sont invités à créer une passkey lors de leur prochaine connexion via un prompt non-intrusif. Campagne email pour les utilisateurs à haut risque (mot de passe faible détecté via HaveIBeenPwned API).
4. **BFF pattern pour le web** : Implémentation d'un Backend-For-Frontend qui gère les sessions via des cookies HttpOnly/Secure/SameSite=Strict. Les tokens ne sont jamais exposés au JavaScript côté client. Le BFF proxy les appels API avec le token en header Authorization.

### Résultat
- Credential stuffing éliminé pour les utilisateurs avec passkeys (impossible par design)
- Taux de conversion signup passé de 35% à 52% (+48%) — les passkeys suppriment la friction de création de mot de passe
- Tickets support liés aux mots de passe réduits de 70%
- 45% des utilisateurs actifs ont migré vers les passkeys en 6 mois (adoption organique)
- Temps de login médian réduit de 12 secondes (email + mot de passe) à 2 secondes (passkey biométrique)
- Conformité CNIL validée — l'authentification est considérée comme "état de l'art"

### Leçons apprises
- Les passkeys sont la meilleure amélioration de sécurité qui améliore AUSSI l'UX — c'est l'argument le plus convaincant pour les stakeholders.
- La migration progressive est essentielle — forcer les passkeys provoque une perte d'utilisateurs. Proposer, ne pas imposer.
- Le BFF pattern est indispensable pour les SPAs — stocker des tokens dans le navigateur (même en mémoire) est inférieur en sécurité aux cookies HttpOnly gérés par le BFF.
