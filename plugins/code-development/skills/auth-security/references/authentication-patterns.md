# Authentication Patterns

Reference complete des patterns d'authentification modernes (2024-2026). Couvre OAuth 2.0/2.1, OpenID Connect, JWT, MFA, passkeys/WebAuthn, SSO, et les identity providers modernes.

---

## OAuth 2.0 / 2.1 Flows

### Evolution de OAuth 2.0 vers OAuth 2.1

OAuth 2.1 consolide les meilleures pratiques accumulees depuis OAuth 2.0 (RFC 6749) en un seul document normatif. Les changements majeurs a retenir :

- **PKCE obligatoire** pour tous les clients (publics ET confidentiels). Ne plus jamais implementer un Authorization Code flow sans PKCE.
- **Implicit flow supprime** : Ce flux exposait le token dans l'URL fragment, il est desormais officiellement deprecie. Migrer tous les clients existants vers Authorization Code + PKCE.
- **Resource Owner Password Credentials (ROPC) supprime** : Ce flux transmettait le mot de passe directement au client. Ne plus l'utiliser sous aucun pretexte.
- **Refresh tokens** : Obligation de les lier au client (sender-constrained) ou d'utiliser la rotation systematique.
- **Bearer tokens** : Recommandation forte d'utiliser des tokens sender-constrained (DPoP - Demonstrating Proof of Possession) pour limiter l'impact d'un vol de token.

### Authorization Code Flow + PKCE

C'est le flux principal pour toute application interactive (SPA, mobile, server-side).

```
1. Client genere code_verifier (random 43-128 chars) et code_challenge = SHA256(code_verifier)
2. Client redirige vers /authorize avec code_challenge et code_challenge_method=S256
3. Utilisateur s'authentifie aupres de l'Authorization Server
4. Authorization Server redirige vers redirect_uri avec authorization_code
5. Client echange le code + code_verifier contre des tokens via /token (POST, backend-to-backend)
6. Authorization Server verifie SHA256(code_verifier) == code_challenge
7. Tokens (access_token + refresh_token + id_token si OIDC) sont retournes
```

Regles d'implementation :

- Toujours utiliser `response_type=code` (jamais `token` ou `id_token` seul)
- Generer un `state` parameter unique par requete pour prevenir les CSRF
- Valider le `state` au retour avant tout traitement
- Utiliser `nonce` si OIDC est implique pour proteger l'id_token contre le replay
- Enregistrer des `redirect_uri` exactes (pas de wildcards) dans l'Authorization Server

### Client Credentials Flow

Pour la communication machine-to-machine (M2M) sans interaction utilisateur.

```
1. Client s'authentifie aupres du /token endpoint avec client_id + client_secret
2. Authorization Server retourne un access_token (pas de refresh_token)
3. Client utilise l'access_token pour appeler l'API
```

Regles d'implementation :

- Stocker les client_secret dans un secret manager, jamais dans le code
- Implementer la rotation automatique des client_secret (tous les 90 jours maximum)
- Utiliser des scopes minimaux pour limiter les permissions du token
- Considerer mTLS (mutual TLS) comme methode d'authentification client pour les environnements haute securite (RFC 8705)
- Limiter le TTL de l'access_token (15-60 minutes maximum)

### Device Authorization Flow

Pour les appareils a interface limitee (smart TV, IoT, CLI tools).

```
1. Device demande un device_code et user_code au /device/authorize endpoint
2. Utilisateur visite l'URL affichee et saisit le user_code sur un autre appareil
3. Device poll le /token endpoint periodiquement
4. Une fois l'utilisateur authentifie, le device recoit les tokens
```

Utiliser un `interval` de polling raisonnable (5 secondes minimum) et respecter le `slow_down` retourne par le serveur.

---

## OpenID Connect (OIDC)

### Concepts fondamentaux

OIDC est une couche d'identite construite sur OAuth 2.0. Elle ajoute :

- **ID Token** : Un JWT signe contenant les claims d'identite de l'utilisateur (sub, email, name, etc.)
- **UserInfo Endpoint** : API pour recuperer les claims supplementaires
- **Discovery** : Endpoint `.well-known/openid-configuration` pour la decouverte automatique de la configuration
- **Scopes standard** : `openid` (obligatoire), `profile`, `email`, `address`, `phone`

### Validation de l'ID Token

Valider systematiquement chaque ID Token recu :

1. Verifier la signature avec la cle publique du provider (via JWKS endpoint)
2. Verifier que `iss` (issuer) correspond au provider attendu
3. Verifier que `aud` (audience) contient le client_id de l'application
4. Verifier que `exp` (expiration) est dans le futur
5. Verifier que `iat` (issued at) est raisonnable (pas trop ancien)
6. Verifier le `nonce` si un nonce a ete envoye dans la requete
7. Verifier que `azp` (authorized party) correspond au client_id si present

### Federation d'identite et multi-provider

Supporter plusieurs providers OIDC (Google, Microsoft, Apple, etc.) avec une approche unifiee :

- Maintenir une table de mapping entre le `sub` du provider et l'utilisateur interne
- Gerer le cas de "account linking" : un meme email provenant de providers differents
- Ne jamais utiliser l'email comme identifiant unique cross-provider (l'email peut etre recycle)
- Utiliser `sub` + `iss` comme identifiant unique pour chaque identite federee

---

## JWT Best Practices

### Structure et algorithmes

Un JWT est compose de trois parties : Header, Payload, Signature, encodees en Base64url et separees par des points.

Regles pour les algorithmes :

- Utiliser **RS256** (RSA-SHA256) ou **ES256** (ECDSA-P256) pour les tokens emis par un serveur (asymetrique, la cle publique peut etre distribuee)
- Utiliser **EdDSA** (Ed25519) comme alternative moderne plus performante
- Ne jamais utiliser `alg: none` (desactiver explicitement dans la configuration du parser)
- Ne jamais utiliser **HS256** pour des tokens transmis a des tiers (la cle secrete devrait rester confidentielle)
- Rejeter explicitement tout JWT avec un algorithme inattendu (attaque par confusion d'algorithme)

### Access Token Best Practices

- Fixer un TTL court : **5 a 15 minutes** maximum
- Inclure uniquement les claims necessaires (sub, scopes, iat, exp, iss, aud)
- Ne pas stocker de donnees sensibles dans le payload (PII, roles detailles) — le JWT peut etre decode par quiconque le possede
- Utiliser des tokens opaques (reference tokens) si la confidentialite du payload est requise
- Implementer DPoP (Demonstrating Proof-of-Possession) pour lier le token au client qui l'a recu

### Refresh Token Best Practices

- Fixer un TTL de **7 a 30 jours** maximum (selon la sensibilite de l'application)
- Implementer la **rotation on use** : chaque echange genere un nouveau refresh token et invalide l'ancien
- Stocker les refresh tokens cote serveur (jamais en clair dans localStorage)
- Implementer la **detection de reutilisation** (reuse detection) : si un refresh token deja consomme est presente, revoquer toute la famille de tokens et forcer la re-authentification
- Lier le refresh token au device/fingerprint si possible

### Token Revocation

Les JWT etant stateless, la revocation necessite un mecanisme supplementaire :

- **Token blacklist/denylist** : Maintenir une liste des `jti` (JWT ID) revoques, verifiee a chaque requete. Utiliser Redis avec TTL aligne sur l'expiration du token.
- **Token versioning** : Stocker un `tokenVersion` par utilisateur en base. Inclure cette version dans le JWT. Incrementer la version pour invalider tous les tokens existants.
- **Short-lived tokens** : Avec des access tokens de 5 minutes, la fenetre de vulnerabilite est limitee meme sans revocation explicite.

---

## MFA — Multi-Factor Authentication

### Hierarchie des facteurs (du plus faible au plus fort)

1. **SMS OTP** : Vulnerable au SIM swapping et SS7 interception. Eviter si possible. Acceptable uniquement comme fallback de dernier recours.
2. **Email OTP** : Legerement meilleur que SMS, mais depend de la securite du compte email.
3. **TOTP (Time-based One-Time Password)** : Applications comme Google Authenticator, Authy. Bon compromis securite/UX. Implementer selon RFC 6238.
4. **Push notification** : Apps proprietaires (Duo, Microsoft Authenticator). Attention au "MFA fatigue" — implementer le number matching.
5. **Hardware security keys (FIDO U2F)** : YubiKey, Titan. Phishing-resistant. Excellent pour les comptes a haute valeur.
6. **Passkeys / WebAuthn** : Le standard de reference 2024-2026. Phishing-resistant, resistant au replay, UX fluide.

### Implementation TOTP

```
1. Generer un secret de 160 bits minimum (20 octets) par utilisateur
2. Encoder en Base32 et presenter via QR code (otpauth://totp/...)
3. Exiger la saisie d'un code valide pour confirmer l'activation
4. Generer et afficher des recovery codes (8-10 codes a usage unique)
5. Stocker le secret chiffre en base de donnees
6. A la verification : accepter le code courant +-1 window (30 secondes de tolerance)
7. Implementer un rate limiting strict sur la verification (5 tentatives max)
```

### Implementation Passkeys / WebAuthn

Les passkeys sont la methode d'authentification recommandee en 2024-2026. Elles remplacent les mots de passe et le MFA traditionnel en une seule operation phishing-resistant.

**Registration (attestation) :**

```
1. Serveur genere un challenge aleatoire (32 octets minimum)
2. Serveur envoie PublicKeyCredentialCreationOptions :
   - rp (relying party) : id = domaine, name = nom de l'app
   - user : id (opaque, pas l'email), name, displayName
   - challenge : le challenge genere
   - pubKeyCredParams : [{alg: -7 (ES256)}, {alg: -257 (RS256)}]
   - authenticatorSelection : residentKey = "preferred", userVerification = "preferred"
   - attestation : "none" (sauf besoin compliance specifique)
3. Navigateur/OS presente le dialog de creation (Touch ID, Face ID, Windows Hello, etc.)
4. Client retourne PublicKeyCredential avec attestationObject et clientDataJSON
5. Serveur valide le challenge, l'origin, extrait la cle publique, et la stocke
```

**Authentication (assertion) :**

```
1. Serveur genere un nouveau challenge
2. Serveur envoie PublicKeyCredentialRequestOptions avec allowCredentials (optionnel pour discoverable credentials)
3. Navigateur/OS presente le dialog d'authentification
4. Client signe le challenge avec la cle privee
5. Serveur verifie la signature avec la cle publique stockee
6. Serveur verifie le compteur de signature (protection anti-clone)
```

Regles d'implementation :

- Supporter les **discoverable credentials** (passkeys synchonisees) pour une UX optimale
- Permettre l'enregistrement de **multiples passkeys** par utilisateur (un par device/ecosystem)
- Implementer un fallback vers une autre methode (email OTP) en cas de perte de tous les authenticators
- Utiliser les librairies server-side eprouvees : `@simplewebauthn/server` (Node), `py_webauthn` (Python), `webauthn-rs` (Rust)

---

## SSO & SAML

### OIDC pour le SSO moderne

Preferer OIDC a SAML pour les nouvelles implementations SSO :

- Plus simple a implementer et debugger (JSON vs XML)
- Support natif des SPA et applications mobiles
- Meilleur ecosysteme de librairies modernes
- Compatible avec les passkeys et les flows OAuth 2.1

### SAML 2.0 pour le SSO entreprise legacy

SAML reste necessaire pour l'integration avec les IdP entreprise (ADFS, Shibboleth, certains Okta/Azure AD setups legacy).

Regles d'implementation SAML :

- Toujours valider la signature XML de la SAML Response entiere
- Verifier l'`Issuer`, l'`Audience`, le `Recipient`, et les conditions temporelles
- Proteger contre les attaques XML Signature Wrapping (XSW) — utiliser une librairie maintenue
- Implementer le Single Logout (SLO) si requis, mais privilegier la gestion de session cote application

---

## Session vs Token-Based Authentication

### Session-based (recommande pour les apps web classiques)

```
Avantages :
- Revocation instantanee (supprimer la session cote serveur)
- Pas de donnees sensibles cote client
- Compatible avec les cookies HttpOnly/Secure/SameSite

Inconvenients :
- Necessite un store de sessions cote serveur (Redis recommande)
- Plus complexe a scaler horizontalement (sticky sessions ou store partage)
- Necessite une protection CSRF
```

Configuration cookie recommandee :

```
Set-Cookie: session_id=<opaque_value>;
  HttpOnly;
  Secure;
  SameSite=Lax;
  Path=/;
  Max-Age=3600;
  Domain=.example.com
```

### Token-based (recommande pour les API et les architectures distribuees)

```
Avantages :
- Stateless (pas de store serveur requis pour la validation)
- Ideal pour les microservices et les API publiques
- Cross-domain naturellement (pas de cookies)

Inconvenients :
- Revocation complexe (necessite blacklist ou short-lived tokens)
- Risque de vol si mal stocke cote client
- Taille du token peut impacter les performances
```

### BFF Pattern (Backend-For-Frontend) — Approche hybride recommandee

Combiner le meilleur des deux mondes pour les SPA :

```
1. Le BFF (serveur) gere le flux OAuth et stocke les tokens en session securisee
2. Le SPA communique avec le BFF via des cookies HttpOnly
3. Le BFF ajoute l'access token aux requetes vers l'API (Authorization: Bearer)
4. Le SPA ne voit jamais les tokens OAuth
```

Avantage : Securite des sessions (cookies HttpOnly) + compatibilite OAuth/OIDC. C'est le pattern recommande par la communaute securite pour les SPA en 2024-2026.

---

## Passwordless Authentication

### Magic Links

Implementation securisee des magic links :

- Generer un token cryptographiquement aleatoire (32 octets minimum, URL-safe)
- Fixer un TTL court : **10 a 15 minutes** maximum
- Usage unique : invalider le token immediatement apres utilisation
- Lier le token a une session/device pour prevenir le forwarding
- Rate limiter l'envoi d'emails (1 par minute, 5 par heure par adresse)
- Hacher le token en base (SHA256) — ne jamais stocker le token en clair

### Email OTP

- Generer un code de 6 a 8 chiffres
- TTL de 5 a 10 minutes maximum
- Maximum 3 tentatives de verification avant regeneration obligatoire
- Rate limiter l'envoi et la verification

---

## Modern Identity Providers — Comparaison

### Decision Matrix

| Critere | Clerk | Auth0 | Supabase Auth | Keycloak | Firebase Auth |
|---------|-------|-------|---------------|----------|---------------|
| **Type** | SaaS | SaaS | SaaS/Self-host | Self-hosted | SaaS |
| **Passkeys** | Natif | Natif | Via extension | Plugin | Non natif |
| **SSO/SAML** | Entreprise plan | Inclus | Limité | Complet | Non |
| **Customisation UI** | Composants React | Universal Login | Basique | Themes | Basique |
| **Multi-tenant** | Organisations | Organizations | RLS-based | Realms | Non natif |
| **Pricing modele** | Par MAU | Par MAU | Par MAU (generous free) | Gratuit (infra) | Generous free |
| **Self-hosting** | Non | Non | Oui | Oui | Non |
| **Ideal pour** | SaaS B2B React/Next | Enterprise B2B/B2C | Apps Supabase/PG | On-premise, control total | Prototypage rapide |

### Recommandations par contexte

```
Startup SaaS B2B avec React/Next.js ?
  -> Clerk : DX excellente, passkeys natifs, organisations multi-tenant

Application entreprise avec besoins SSO complexes ?
  -> Auth0 : Ecosysteme mature, SAML/OIDC complet, Actions extensibles

Stack Supabase / PostgreSQL-centric ?
  -> Supabase Auth : Integration native avec RLS, GoTrue-based, cout reduit

Exigences de souverainete / on-premise ?
  -> Keycloak : Open-source, self-hosted, controle total, federation complete

Prototype rapide / hackathon ?
  -> Firebase Auth : Setup en 5 minutes, free tier genereux
```

---

## Checklist d'implementation

Utiliser cette checklist pour chaque systeme d'authentification :

- [ ] HTTPS force partout (HSTS preload)
- [ ] Flux OAuth 2.1 + PKCE pour tous les clients publics
- [ ] Tokens stockes de maniere securisee (cookies HttpOnly ou BFF pattern)
- [ ] Access tokens avec TTL court (5-15 min)
- [ ] Refresh token rotation implementee avec reuse detection
- [ ] Passkeys/WebAuthn comme methode primaire proposee
- [ ] MFA disponible et encouragee (TOTP minimum, passkeys ideal)
- [ ] Recovery flow securise (recovery codes, email verification)
- [ ] Rate limiting sur login, registration, et recovery
- [ ] Account lockout apres N tentatives echouees (avec notification)
- [ ] Logging des evenements d'authentification (succes, echecs, anomalies)
- [ ] Protection CSRF pour tous les formulaires et les endpoints mutatifs
- [ ] Session timeout et idle timeout configures
- [ ] Password policy robuste si mots de passe utilises (NIST SP 800-63B : 8+ chars, check against breached passwords, pas de regles de complexite arbitraires)
