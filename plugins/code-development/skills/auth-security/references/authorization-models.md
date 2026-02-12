# Authorization Models

Reference complete des modeles d'autorisation modernes (2024-2026). Couvre RBAC, ABAC, ReBAC, Row-Level Security, policy engines, API authorization, et les patterns de conception de permissions.

---

## Principes fondamentaux de l'autorisation

### Separation Authentication vs Authorization

Toujours separer ces deux responsabilites distinctes :

- **Authentification** : "Qui est cet acteur ?" — Verifier l'identite
- **Autorisation** : "Cet acteur a-t-il le droit d'effectuer cette action sur cette ressource ?" — Verifier les permissions

Ne jamais melanger ces deux concerns dans le meme middleware ou service. Authentifier d'abord, autoriser ensuite. Un acteur authentifie n'est pas forcement autorise.

### Deny by Default

Configurer le systeme pour refuser tout acces par defaut. Chaque permission doit etre explicitement accordee. En cas de doute, d'erreur, ou de policy manquante, refuser l'acces. Ce principe est la fondation de tout modele d'autorisation robuste.

### Principle of Least Privilege

Accorder a chaque acteur le minimum de permissions necessaire pour accomplir sa tache. Revoir et ajuster les permissions regulierement. Implementer des permissions temporaires (just-in-time access) pour les operations sensibles.

---

## RBAC — Role-Based Access Control

### Concept

RBAC attribue des permissions a des roles, et des roles a des utilisateurs. C'est le modele le plus repandu et le plus simple a comprendre.

```
User -> Role(s) -> Permission(s) -> Resource(s)

Exemple :
  Alice -> [editor] -> [articles:read, articles:write, articles:publish] -> /articles/*
  Bob -> [viewer] -> [articles:read] -> /articles/*
```

### Implementation recommandee

**Schema de base (PostgreSQL) :**

```sql
CREATE TABLE roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT UNIQUE NOT NULL,        -- 'admin', 'editor', 'viewer'
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE permissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  resource TEXT NOT NULL,            -- 'articles', 'users', 'settings'
  action TEXT NOT NULL,              -- 'read', 'write', 'delete', 'admin'
  UNIQUE(resource, action)
);

CREATE TABLE role_permissions (
  role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
  permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,
  PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE user_roles (
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
  scope TEXT DEFAULT 'global',       -- 'global', 'org:uuid', 'project:uuid'
  granted_at TIMESTAMPTZ DEFAULT now(),
  granted_by UUID REFERENCES users(id),
  PRIMARY KEY (user_id, role_id, scope)
);
```

**Middleware d'autorisation (Node.js / Express) :**

```typescript
function requirePermission(resource: string, action: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const userPermissions = await getUserPermissions(req.user.id);
    const hasPermission = userPermissions.some(
      p => p.resource === resource && p.action === action
    );
    if (!hasPermission) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

// Usage
app.delete('/api/articles/:id', requirePermission('articles', 'delete'), deleteArticle);
```

### Hierarchie de roles

Implementer une hierarchie si necessaire : `admin > editor > viewer`. Un role superieur herite des permissions des roles inferieurs.

```sql
CREATE TABLE role_hierarchy (
  parent_role_id UUID REFERENCES roles(id),
  child_role_id UUID REFERENCES roles(id),
  PRIMARY KEY (parent_role_id, child_role_id)
);
```

### Quand utiliser RBAC

- Application avec un nombre fixe de roles (< 10)
- Permissions qui ne dependent pas du contexte dynamique
- Equipe de taille modeste ou structure organisationnelle stable
- Besoin de simplicite et de lisibilite dans les audits

### Limites de RBAC

- **Role explosion** : Le nombre de roles croit exponentiellement avec la granularite des permissions
- **Manque de contexte** : RBAC ne prend pas en compte les attributs dynamiques (heure, localisation, device)
- **Difficulte multi-tenant** : Necessite des roles scopes (role@organization) qui ajoutent de la complexite

---

## ABAC — Attribute-Based Access Control

### Concept

ABAC prend les decisions d'autorisation en evaluant des attributs de multiples sources :

- **Subject attributes** : role, departement, clearance level, localisation
- **Resource attributes** : proprietaire, classification, date de creation, sensibilite
- **Action attributes** : type d'action, methode HTTP
- **Environment attributes** : heure, adresse IP, device posture, risque de session

```
Policy : ALLOW if
  subject.department == resource.department AND
  subject.clearance >= resource.classification AND
  environment.time BETWEEN "09:00" AND "18:00" AND
  environment.device_posture == "compliant"
```

### Implementation avec un Policy Engine

Utiliser un policy engine dedie plutot que de coder les regles en dur :

**OPA (Open Policy Agent) avec Rego :**

```rego
package authz

default allow := false

allow if {
    input.subject.role == "editor"
    input.resource.type == "article"
    input.action == "edit"
    input.resource.owner == input.subject.id
}

allow if {
    input.subject.role == "admin"
}

allow if {
    input.subject.department == input.resource.department
    input.subject.clearance >= input.resource.classification
    time.now_ns() >= time.parse_rfc3339_ns(input.environment.business_hours_start)
    time.now_ns() <= time.parse_rfc3339_ns(input.environment.business_hours_end)
}
```

**Cedar (AWS) :**

```cedar
permit(
  principal in Role::"editor",
  action == Action::"edit",
  resource in ResourceType::"Article"
) when {
  resource.owner == principal
};

permit(
  principal in Role::"admin",
  action,
  resource
);

forbid(
  principal,
  action,
  resource
) when {
  context.risk_score > 80
};
```

### Quand utiliser ABAC

- Decisions d'autorisation dependant de multiples attributs contextuels
- Exigences de compliance reglementaire (HIPAA, SOX, GDPR)
- Environnements ou les permissions changent dynamiquement
- Besoin de policies auditables et versionnees

---

## ReBAC — Relationship-Based Access Control

### Concept

ReBAC definit les autorisations en fonction des relations entre les entites. Inspire du modele de Google Zanzibar (systeme d'autorisation de Google Drive, YouTube, etc.).

```
Tuples de relation :
  document:readme#owner@user:alice
  document:readme#viewer@team:engineering#member
  team:engineering#member@user:bob
  folder:docs#parent@document:readme

Verification :
  "user:bob peut-il lire document:readme ?"
  -> bob est member de team:engineering
  -> team:engineering est viewer de document:readme
  -> viewer implique permission read
  -> AUTORISE
```

### Solutions ReBAC modernes

| Solution | Type | Langage DSL | Performance | Cas d'usage |
|----------|------|-------------|-------------|-------------|
| **OpenFGA** | Open-source (CNCF) | DSL type-based | Haute | SaaS, general purpose |
| **SpiceDB / Authzed** | Open-source / SaaS | Zanzibar-like | Tres haute | Scale enterprise |
| **Ory Keto** | Open-source | Namespace-based | Haute | Stack Ory |
| **Warrant** | SaaS | API-first | Haute | Integration rapide |

### Modelisation OpenFGA

```
model
  schema 1.1

type user

type team
  relations
    define member: [user]
    define admin: [user]

type document
  relations
    define owner: [user]
    define editor: [user, team#member]
    define viewer: [user, team#member]
    define can_read: viewer or editor or owner
    define can_write: editor or owner
    define can_delete: owner
    define can_share: owner

type folder
  relations
    define owner: [user]
    define viewer: [user, team#member]
    define parent: [document]
```

### Quand utiliser ReBAC

- Systemes de partage de documents (Google Drive, Notion-like)
- Reseaux sociaux et graphes de relations
- Applications ou les permissions derivent des relations entre entites
- Besoin d'heritage de permissions (folder -> document -> comment)

---

## Row-Level Security (RLS)

### Concept

RLS applique les regles d'autorisation directement au niveau de la base de donnees. Chaque requete SQL ne retourne que les lignes auxquelles l'utilisateur a acces.

### Implementation PostgreSQL

```sql
-- Activer RLS sur la table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Forcer RLS meme pour les table owners
ALTER TABLE documents FORCE ROW LEVEL SECURITY;

-- Policy : les utilisateurs ne voient que leurs propres documents
CREATE POLICY documents_isolation ON documents
  FOR ALL
  USING (owner_id = current_setting('app.current_user_id')::uuid);

-- Policy : les admins voient tout dans leur organisation
CREATE POLICY documents_org_admin ON documents
  FOR ALL
  USING (
    org_id = current_setting('app.current_org_id')::uuid
    AND current_setting('app.current_role') = 'admin'
  );

-- Policy multi-tenant stricte
CREATE POLICY tenant_isolation ON documents
  FOR ALL
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

**Configuration du contexte applicatif :**

```typescript
// Middleware pour setter le contexte RLS dans la connexion PostgreSQL
async function setRLSContext(pool: Pool, userId: string, orgId: string, role: string) {
  const client = await pool.connect();
  await client.query(`SET LOCAL app.current_user_id = '${userId}'`);
  await client.query(`SET LOCAL app.current_org_id = '${orgId}'`);
  await client.query(`SET LOCAL app.current_role = '${role}'`);
  return client;
}
```

### RLS avec Supabase

Supabase rend RLS accessible via son SDK et son dashboard :

```sql
-- Supabase : utiliser auth.uid() pour l'utilisateur courant
CREATE POLICY "Users can view own data" ON profiles
  FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update own data" ON profiles
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Utiliser auth.jwt() pour acceder aux claims du token
CREATE POLICY "Org members can view org data" ON org_data
  FOR SELECT
  USING (org_id = (auth.jwt() ->> 'org_id')::uuid);
```

### Quand utiliser RLS

- Applications multi-tenant avec isolation stricte des donnees
- Defense in depth : ajouter une couche d'autorisation au niveau donnees
- Applications ou la logique d'acces est principalement basee sur la propriete des donnees
- Stack PostgreSQL-centric (Supabase, bare PostgreSQL)

### Precautions RLS

- Tester les policies de maniere exhaustive (un oubli de policy = fuite de donnees)
- Attention aux performances : les policies RLS ajoutent des conditions a chaque requete
- Utiliser EXPLAIN ANALYZE pour verifier que les indexes supportent les policies
- Ne jamais desactiver RLS "temporairement" en production
- Combiner RLS avec des autorisations applicatives (defense in depth)

---

## Policy Engines

### OPA (Open Policy Agent)

OPA est le standard de-facto pour l'authorization-as-code dans les architectures cloud-native.

**Architecture d'integration :**

```
[Application] ---> [OPA Sidecar/Service] ---> Decision (allow/deny)
                        |
                    [Policy Bundle]
                    (Rego policies + data)
```

**Patterns de deploiement :**

- **Sidecar** : OPA deploye a cote de chaque service (latence minimale, ~1ms)
- **Service centralise** : Un service OPA partage (plus simple a gerer, latence reseau)
- **Library** : OPA integre comme librairie dans l'application (Go, Wasm)
- **Envoy plugin** : OPA comme filtre d'autorisation dans un service mesh

**Bonnes pratiques Rego :**

- Ecrire des tests unitaires pour chaque policy (`opa test`)
- Versionner les policies dans Git (GitOps)
- Utiliser les bundles pour distribuer les policies et les donnees
- Implementer des decisions par defaut explicites (`default allow := false`)
- Structurer les policies par domaine (`package authz.articles`, `package authz.users`)

### Cedar (AWS Verified Permissions)

Cedar est le langage de policies d'AWS, concu pour etre performant et analysable formellement.

**Avantages de Cedar :**

- Syntaxe plus lisible que Rego pour les non-developpeurs
- Analyse formelle possible (verification de proprietes)
- Performance garantie (evaluation en temps constant)
- Integration native avec AWS Verified Permissions (managed service)
- Support des entity hierarchies natif

**Quand choisir Cedar vs OPA :**

```
Ecosysteme AWS, besoin d'un managed service ?
  -> Cedar + AWS Verified Permissions

Architecture Kubernetes / cloud-agnostic ?
  -> OPA + Gatekeeper

Besoin de policies complexes avec logique avancee ?
  -> OPA (Rego plus expressif)

Besoin de lisibilite pour des non-developpeurs ?
  -> Cedar (syntaxe plus accessible)

Besoin de verification formelle des policies ?
  -> Cedar (prouvable mathematiquement)
```

### Casbin

Casbin est un framework d'autorisation multi-langage supportant RBAC, ABAC, et des modeles custom.

```
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act
```

Casbin est ideal pour les applications monolithiques ou les equipes cherchant une solution legere avec un modele configurable sans service externe.

---

## API Authorization & Scopes

### Design de scopes OAuth

Structurer les scopes de maniere hierarchique et granulaire :

```
Format : resource:action

Exemples :
  articles:read        -- Lire les articles
  articles:write       -- Creer/modifier des articles
  articles:delete      -- Supprimer des articles
  users:read           -- Lire les profils utilisateurs
  users:admin          -- Administration des utilisateurs
  billing:read         -- Voir la facturation
  billing:manage       -- Gerer la facturation

Scopes agreges :
  articles:*           -- Toutes les permissions articles
  admin                -- Acces administrateur complet
```

### API Gateway Authorization

Implementer l'autorisation en couches au niveau de l'API gateway :

```
Layer 1 : API Gateway
  -> Valider le token (signature, expiration, audience)
  -> Verifier les scopes requis pour la route
  -> Rate limiting par client/scope

Layer 2 : Service applicatif
  -> Verifier les permissions fines (RBAC/ABAC)
  -> Logique metier d'autorisation
  -> Filtrage des donnees retournees

Layer 3 : Base de donnees
  -> RLS pour l'isolation multi-tenant
  -> Contraintes d'integrite
```

### Permission Design Patterns

**Pattern : Permission hierarchy avec wildcard**

```typescript
const permissionHierarchy = {
  'admin': ['*'],
  'articles:admin': ['articles:read', 'articles:write', 'articles:delete', 'articles:publish'],
  'articles:write': ['articles:read'],
  'billing:manage': ['billing:read'],
};

function hasPermission(userPermissions: string[], required: string): boolean {
  return userPermissions.some(p =>
    p === required ||
    p === '*' ||
    (permissionHierarchy[p] || []).includes(required)
  );
}
```

**Pattern : Resource-scoped permissions**

```typescript
// Permission liee a un resource specifique
interface ScopedPermission {
  permission: string;      // 'articles:write'
  scope: string;           // 'org:acme-corp' ou 'project:website'
  resource_id?: string;    // 'article:123' (optionnel, pour le fine-grained)
}
```

---

## Tendances Fine-Grained Authorization (2024-2026)

### Authorization as Code

Traiter les policies d'autorisation comme du code :

- Versionner dans Git avec code review
- Tester avec des tests unitaires et d'integration
- Deployer via CI/CD avec rollback
- Monitorer les decisions d'autorisation en production

### Decentralized Authorization

Chaque service possede et enforce ses propres policies, mais utilise un framework commun (OPA, Cedar). Les policies sont distribuees via des bundles, pas centralisees dans un service unique.

### Continuous Authorization

Ne pas se limiter a une verification au moment de la requete. Evaluer en continu :

- Re-verifier les permissions lors de changements de contexte
- Implementer des session risk scores qui evoluent en temps reel
- Revoquer les acces automatiquement en cas d'anomalie detectee

### Checklist d'implementation autorisation

- [ ] Modele d'autorisation defini et documente (RBAC, ABAC, ReBAC, ou hybride)
- [ ] Autorisation appliquee a chaque couche (API, service, base de donnees)
- [ ] Principe deny-by-default enforce
- [ ] Tests unitaires pour chaque policy d'autorisation
- [ ] Logging des decisions d'autorisation (allow et deny)
- [ ] Audit trail des changements de permissions et de roles
- [ ] Revue reguliere des permissions attribuees (access review)
- [ ] Separation des duties pour les actions sensibles
- [ ] Permissions temporaires avec expiration automatique
- [ ] Documentation des roles et permissions accessible aux equipes
