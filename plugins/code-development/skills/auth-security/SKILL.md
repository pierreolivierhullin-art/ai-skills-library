---
name: auth-security
description: This skill should be used when the user asks about "authentication", "authorization", "OAuth 2.0", "OpenID Connect", "JWT", "OWASP", "application security", "RBAC", "ABAC", "secrets management", "encryption", "zero trust", "passkeys", "WebAuthn", "authentification", "autorisation", "sécurité applicative", "gestion des secrets", "chiffrement", "OIDC", "SSO", "single sign-on", "MFA", "2FA", "multi-factor authentication", "session management", "gestion des sessions", "CORS", "CSRF", "XSS", "SQL injection", "security headers", "certificate management", "TLS", "SSL", "API security", "sécurité API", "token management", "refresh token", "identity provider", "IdP", "Keycloak", "Auth0", "Clerk", "NextAuth", or needs guidance on application security, identity management, and access control.
version: 1.1.0
last_updated: 2026-02
---

# Auth & Security

## Overview

Ce skill couvre l'ensemble du spectre de la securite applicative moderne : authentification, autorisation, gestion des secrets, durcissement applicatif et architecture zero-trust. Il synthetise les meilleures pratiques 2024-2026 incluant OAuth 2.1, les passkeys/WebAuthn, les policy engines (OPA, Cedar), et les approches zero-trust. Utiliser ce skill comme reference systematique pour toute decision touchant a l'identite, aux acces et a la securite dans une application.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- Conception ou audit d'un systeme d'authentification (login, signup, SSO, MFA)
- Implementation de flux OAuth 2.0/2.1 ou OpenID Connect
- Gestion de JWT (emission, validation, rotation, revocation)
- Mise en place de passkeys, WebAuthn, ou authentification passwordless
- Conception d'un modele d'autorisation (RBAC, ABAC, ReBAC, RLS)
- Integration d'un identity provider (Clerk, Auth0, Supabase Auth, Keycloak)
- Durcissement securitaire (OWASP Top 10, headers HTTP, CSP, CORS, CSRF)
- Gestion des secrets, cles API, certificats TLS
- Audit de securite, revue de code orientee securite
- Architecture zero-trust ou migration vers un modele least-privilege

## Core Principles

### 1. Defense in Depth (Defense en profondeur)

Ne jamais s'appuyer sur une seule couche de securite. Combiner validation cote client, validation cote serveur, WAF, rate limiting, monitoring et alerting. Chaque couche doit etre autonome : si une couche tombe, les autres continuent de proteger.

### 2. Least Privilege (Moindre privilege)

Accorder exactement les permissions necessaires, jamais plus. Appliquer ce principe a chaque niveau : tokens OAuth (scopes minimaux), roles utilisateur, acces base de donnees (RLS), permissions systeme, network policies. Preferer les permissions deny-by-default avec allow-list explicite.

### 3. Zero Trust

Ne jamais faire confiance implicitement a un acteur, meme a l'interieur du perimetre reseau. Verifier chaque requete : identite, device posture, contexte reseau, comportement. Appliquer le principe "never trust, always verify" avec validation continue plutot que validation unique au login.

### 4. Secure by Default

Configurer chaque composant avec les parametres les plus securises par defaut. Forcer HTTPS partout (HSTS preload). Utiliser SameSite=Lax minimum pour les cookies. Activer CSP en mode restrictif. Chiffrer les donnees au repos et en transit. Rendre la securite invisible pour le developpeur : les choix par defaut doivent etre les choix surs.

### 5. Fail Secure

En cas d'erreur ou d'exception, refuser l'acces plutot que de l'accorder. Un crash du service d'autorisation doit bloquer les requetes, pas les laisser passer. Ne jamais exposer de details d'erreur internes (stack traces, requetes SQL) dans les reponses d'erreur.

## Key Frameworks & Methods

### Authentication Stack (2024-2026)

| Methode | Cas d'usage | Securite | UX |
|---------|-------------|----------|----|
| Passkeys / WebAuthn | Auth primaire, remplacement mot de passe | Tres haute (phishing-resistant) | Excellente |
| OAuth 2.1 + PKCE | Apps tierces, SPA, mobile | Haute | Bonne |
| OIDC (OpenID Connect) | SSO entreprise, federation d'identite | Haute | Bonne |
| TOTP / OTP | MFA second facteur | Moyenne-Haute | Moyenne |
| Magic Links | Apps grand public, onboarding simplifie | Moyenne | Bonne |
| SAML 2.0 | SSO legacy entreprise | Haute | Moyenne |

### Authorization Models

| Modele | Complexite | Flexibilite | Cas d'usage |
|--------|-----------|-------------|-------------|
| RBAC | Faible | Moyenne | Apps simples, equipes fixes |
| ABAC | Haute | Tres haute | Contexte dynamique, compliance |
| ReBAC | Moyenne-Haute | Haute | Graphes sociaux, documents partages |
| RLS (Row-Level Security) | Moyenne | Moyenne | Multi-tenant, isolation donnees |
| Policy Engines (OPA/Cedar) | Haute | Tres haute | Microservices, authorization-as-code |

### Security Standards

- **OWASP Top 10 (2021+)** : Reference obligatoire pour toute application web
- **OWASP ASVS** : Standard de verification de securite applicative, utiliser comme checklist
- **NIST SP 800-63** : Lignes directrices pour l'identite numerique et l'authentification
- **FIDO2/WebAuthn** : Standard pour l'authentification passwordless et passkeys

## Decision Guide

### Choisir un flux d'authentification

```
Application web classique (server-rendered) ?
  -> Session-based auth + cookies HttpOnly + CSRF tokens
  -> Considerer passkeys comme methode primaire

SPA (Single Page Application) ?
  -> OAuth 2.1 Authorization Code + PKCE
  -> Stocker tokens en memoire (PAS localStorage)
  -> Utiliser BFF (Backend-For-Frontend) pattern si possible

Application mobile native ?
  -> OAuth 2.1 Authorization Code + PKCE
  -> Stocker tokens dans le keychain/keystore securise
  -> Implementer biometric unlock via passkeys

API machine-to-machine ?
  -> OAuth 2.1 Client Credentials
  -> mTLS pour les environnements haute securite
  -> Rotation automatique des credentials

Microservices internes ?
  -> mTLS entre services
  -> JWT propagation avec validation a chaque hop
  -> Service mesh (Istio/Linkerd) pour le zero-trust network
```

### Choisir un modele d'autorisation

```
Moins de 5 roles fixes, logique simple ?
  -> RBAC classique, suffisant et maintenable

Permissions dependant du contexte (heure, localisation, device) ?
  -> ABAC avec policy engine (OPA ou Cedar)

Partage de ressources entre utilisateurs (Google Docs-like) ?
  -> ReBAC (Relation-Based Access Control)
  -> Considerer OpenFGA ou Authzed/SpiceDB

Application multi-tenant avec isolation stricte ?
  -> RLS au niveau base de donnees (PostgreSQL policies)
  -> Combiner avec RBAC pour les permissions intra-tenant

Architecture microservices complexe ?
  -> Policy engine centralise (OPA avec Rego, ou Cedar)
  -> Authorization-as-code avec tests automatises
```

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **BFF Pattern (Backend-For-Frontend)** : Gerer les tokens OAuth cote serveur via un backend dedie au frontend. Ne jamais exposer les tokens directement au navigateur. Le BFF stocke les tokens en session securisee et relay les appels API.

- **Token Rotation** : Implementer la rotation automatique des refresh tokens (rotation on use). Chaque utilisation d'un refresh token en genere un nouveau et invalide l'ancien. Detecter la reutilisation d'un refresh token deja consomme comme indicateur de compromission et revoquer toute la famille de tokens.

- **Layered Authorization** : Appliquer l'autorisation a chaque couche — API gateway (rate limiting, auth basique), service applicatif (logique metier, RBAC/ABAC), base de donnees (RLS). Ne jamais se reposer sur une seule couche.

- **Secrets Rotation Automatique** : Configurer la rotation automatique pour tous les secrets (cles API, credentials DB, certificats). Utiliser des secrets ephemeres quand possible (Vault dynamic secrets). Viser un TTL maximal de 24h pour les secrets haute sensibilite.

- **Security Headers Systematiques** : Appliquer sur chaque reponse HTTP : `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`.

### Anti-patterns a eviter

- **Stocker des JWT dans localStorage** : Vulnerable aux attaques XSS. Utiliser des cookies HttpOnly, Secure, SameSite=Strict ou stocker en memoire cote client avec un BFF.

- **JWT comme session** : Ne pas utiliser les JWT comme sessions longue duree sans mecanisme de revocation. Un JWT est un bearer token : une fois emis, il est valide jusqu'a expiration. Preferer des access tokens courts (5-15 min) avec refresh token rotation.

- **Roles hardcodes dans le code** : Ne pas disperser `if (user.role === 'admin')` dans le code. Centraliser la logique d'autorisation dans un service ou middleware dedie. Utiliser un policy engine pour les cas complexes.

- **Secrets en clair dans le code ou les variables d'environnement non securisees** : Ne jamais commiter de secrets. Utiliser un secret manager (Vault, AWS Secrets Manager). Scanner le code en CI avec GitGuardian ou TruffleHog.

- **Validation uniquement cote client** : Toujours valider et sanitizer les inputs cote serveur. La validation cote client est une commodite UX, jamais une mesure de securite.

- **CORS wildcard en production** : Ne jamais utiliser `Access-Control-Allow-Origin: *` pour des endpoints authentifies. Specifier les origines autorisees explicitement.

## Implementation Workflow

### Phase 1 : Fondations securitaires

1. Configurer HTTPS partout avec HSTS preload
2. Mettre en place les security headers sur toutes les reponses
3. Configurer CSP en mode report-only, puis enforcer progressivement
4. Implementer rate limiting global (API gateway ou middleware)
5. Activer le secrets scanning dans le pipeline CI/CD

### Phase 2 : Authentification

1. Selectionner un identity provider adapte (Clerk, Auth0, Supabase Auth, Keycloak)
2. Implementer le flux OAuth 2.1 + PKCE pour les clients publics
3. Configurer la gestion de session (cookies securises ou BFF pattern)
4. Ajouter MFA avec support passkeys/WebAuthn comme option primaire
5. Implementer la rotation automatique des refresh tokens
6. Mettre en place les protections CSRF pour les formulaires

### Phase 3 : Autorisation

1. Definir le modele d'autorisation (RBAC, ABAC, ReBAC) selon les besoins
2. Implementer l'autorisation au niveau API (middleware/guards)
3. Configurer RLS au niveau base de donnees pour le multi-tenant
4. Ecrire des tests unitaires et d'integration pour chaque policy
5. Envisager un policy engine (OPA/Cedar) si la complexite le justifie

### Phase 4 : Durcissement et monitoring

1. Auditer l'application contre l'OWASP Top 10 et l'ASVS
2. Implementer input validation stricte avec allow-lists
3. Configurer le logging securitaire (pas de secrets dans les logs)
4. Mettre en place le monitoring des evenements de securite (failed logins, privilege escalation attempts)
5. Planifier la rotation automatique de tous les secrets
6. Executer des scans de dependances (Snyk, Dependabot) en CI

### Phase 5 : Zero Trust et amelioration continue

1. Implementer mTLS entre microservices
2. Deployer un service mesh si l'architecture le justifie
3. Mettre en place la verification continue (re-authentification pour actions sensibles)
4. Realiser des pentests reguliers et des exercices de threat modeling
5. Maintenir un runbook de reponse aux incidents de securite



## State of the Art (2025-2026)

La sécurité applicative fait face à de nouveaux défis :

- **Passkeys et passwordless** : Les passkeys (WebAuthn/FIDO2) remplacent progressivement les mots de passe, supportées nativement par les OS et navigateurs majeurs.
- **Zero Trust Architecture (ZTA)** : L'approche "never trust, always verify" devient le standard, avec une vérification continue des identités et des postures.
- **AI-powered security** : L'IA détecte les menaces en temps réel (anomaly detection, behavioral analysis) mais crée aussi de nouveaux vecteurs d'attaque (prompt injection, data exfiltration).
- **Supply chain security** : Les SBOM (Software Bill of Materials) et les signatures de provenance (SLSA, Sigstore) deviennent obligatoires pour sécuriser la chaîne logicielle.
- **Post-quantum readiness** : La migration vers des algorithmes résistants au quantique (NIST PQC) commence pour les applications sensibles.

## Template actionnable

### Matrice RBAC

| Rôle | Lire | Créer | Modifier | Supprimer | Admin |
|---|---|---|---|---|---|
| **Visiteur** | ☐ Public | ✗ | ✗ | ✗ | ✗ |
| **Utilisateur** | ☑ Propres données | ☑ | ☑ Propres | ✗ | ✗ |
| **Manager** | ☑ Équipe | ☑ | ☑ Équipe | ☐ Limité | ✗ |
| **Admin** | ☑ Tout | ☑ | ☑ Tout | ☑ | ☑ |
| **Super Admin** | ☑ Tout | ☑ | ☑ Tout | ☑ | ☑ Complet |

## Prompts types

- "Comment implémenter OAuth 2.0 + OIDC dans mon app Next.js ?"
- "Aide-moi à sécuriser mon API avec JWT et refresh tokens"
- "Propose un système RBAC pour mon application multi-tenant"
- "Comment gérer les secrets en production de manière sécurisée ?"
- "Fais un audit OWASP Top 10 de mon application"
- "Comment implémenter les passkeys / WebAuthn ?"

## Skills connexes

| Skill | Lien |
|---|---|
| Architecture | `code-development:architecture` — Security by design et architecture sécurisée |
| Juridique | `entreprise:juridique` — RGPD, protection des données et conformité |
| Backend & DB | `code-development:backend-db` — Sécurité des données et chiffrement |
| IT Systèmes | `entreprise:it-systemes` — Cybersécurité et gouvernance IT |
| AI Risk | `ai-governance:ai-risk` — Sécurité des systèmes IA et prompt injection |

## Additional Resources

Consulter les fichiers de reference pour un approfondissement detaille :

- **[Authentication Patterns](./references/authentication-patterns.md)** : Flux OAuth 2.0/2.1, OIDC, JWT best practices, MFA/passkeys/WebAuthn, SSO/SAML, passwordless, comparaison des identity providers modernes, session vs token-based auth.

- **[Authorization Models](./references/authorization-models.md)** : RBAC, ABAC, ReBAC, Row-Level Security, policy engines (OPA, Cedar, Casbin), API authorization & scopes, patterns de conception de permissions, tendances fine-grained authorization.

- **[Security Hardening](./references/security-hardening.md)** : OWASP Top 10 (2021+), validation et sanitisation d'inputs, prevention XSS/CSRF/injection, CSP, CORS, security headers, rate limiting, protection DDoS, scanning de dependances.

- **[Secrets Management](./references/secrets-management.md)** : Stockage de secrets (Vault, AWS/GCP Secret Manager), rotation de cles API, gestion des variables d'environnement, certificats TLS, secrets scanning en CI/CD, architecture zero-trust pour les secrets.
