# Supabase Stack Reference

> Reference detaillee pour la stack Supabase. Couvre l'authentification, le stockage, le temps reel, les Edge Functions, PostgREST, le CLI, le developpement local, les webhooks et les triggers.

---

## Architecture Overview

Supabase est un Backend-as-a-Service (BaaS) open-source construit sur PostgreSQL. Comprendre son architecture pour en tirer le meilleur parti :

```
Client (Browser / Mobile / Server)
    |
    ├── supabase-js SDK (auto-generated types)
    |
    ├── Auth (GoTrue) ─────────── JWT issuance & verification
    ├── PostgREST ─────────────── Auto-generated REST API from schema
    ├── Realtime ──────────────── WebSocket server (broadcast, presence, DB changes)
    ├── Storage ───────────────── S3-compatible object storage with RLS
    ├── Edge Functions ────────── Deno runtime at the edge
    ├── Supavisor ─────────────── Connection pooler (replaces PgBouncer)
    |
    └── PostgreSQL ────────────── Source of truth, RLS policies, triggers, extensions
```

Principe fondamental : PostgreSQL est le centre de gravite. Chaque composant Supabase s'appuie sur les capacites natives de PostgreSQL (RLS, triggers, extensions). Concevoir en "Postgres-first".

## Supabase Auth

### Configuration des providers

```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// Email/Password signup
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secureP@ssw0rd',
  options: {
    data: {
      full_name: 'Jean Dupont',
      organization_id: 'org_123',
    },
    emailRedirectTo: 'https://app.example.com/auth/callback',
  },
});

// OAuth (Google, GitHub, etc.)
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'https://app.example.com/auth/callback',
    scopes: 'email profile',
    queryParams: {
      access_type: 'offline',  // refresh token pour Google
      prompt: 'consent',
    },
  },
});

// Magic Link (passwordless)
const { data, error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com',
  options: {
    emailRedirectTo: 'https://app.example.com/auth/callback',
  },
});

// Phone OTP
const { data, error } = await supabase.auth.signInWithOtp({
  phone: '+33612345678',
});
```

### Auth Callback Handler (Next.js App Router)

```typescript
// app/auth/callback/route.ts
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get('code');
  const next = searchParams.get('next') ?? '/dashboard';

  if (code) {
    const cookieStore = await cookies();
    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          getAll: () => cookieStore.getAll(),
          setAll: (cookiesToSet) => {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          },
        },
      }
    );

    const { error } = await supabase.auth.exchangeCodeForSession(code);
    if (!error) {
      return NextResponse.redirect(`${origin}${next}`);
    }
  }

  return NextResponse.redirect(`${origin}/auth/error`);
}
```

### Integration Auth + RLS

Le pattern central de Supabase : les policies RLS utilisent directement le JWT de l'utilisateur authentifie.

```sql
-- Activer RLS sur la table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Policy : les utilisateurs voient uniquement leurs documents
CREATE POLICY "Users can view own documents"
  ON documents FOR SELECT
  USING (auth.uid() = user_id);

-- Policy : les utilisateurs creent des documents pour eux-memes
CREATE POLICY "Users can create own documents"
  ON documents FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Policy : les utilisateurs modifient leurs propres documents
CREATE POLICY "Users can update own documents"
  ON documents FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Policy : les utilisateurs suppriment leurs propres documents
CREATE POLICY "Users can delete own documents"
  ON documents FOR DELETE
  USING (auth.uid() = user_id);

-- Policy avancee : acces base sur les roles (stockes dans le JWT)
CREATE POLICY "Admins can view all documents"
  ON documents FOR SELECT
  USING (
    (auth.jwt() ->> 'role') = 'admin'
    OR auth.uid() = user_id
  );

-- Policy avec sous-requete : acces base sur l'appartenance a une organisation
CREATE POLICY "Org members can view org documents"
  ON documents FOR SELECT
  USING (
    organization_id IN (
      SELECT org_id FROM organization_members
      WHERE user_id = auth.uid()
    )
  );

-- IMPORTANT : utiliser security definer functions pour les logiques complexes
CREATE OR REPLACE FUNCTION is_org_admin(org_id uuid)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT EXISTS (
    SELECT 1 FROM organization_members
    WHERE user_id = auth.uid()
      AND organization_id = org_id
      AND role = 'admin'
  );
$$;

CREATE POLICY "Org admins can manage documents"
  ON documents FOR ALL
  USING (is_org_admin(organization_id));
```

### Custom Claims dans le JWT

Enrichir le JWT avec des donnees custom (role, tenant_id, permissions) via un hook :

```sql
-- Fonction hook qui ajoute des claims au JWT
CREATE OR REPLACE FUNCTION custom_access_token_hook(event jsonb)
RETURNS jsonb
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
  claims jsonb;
  user_role text;
  user_org_id uuid;
BEGIN
  -- Recuperer le role et l'org de l'utilisateur
  SELECT role, organization_id INTO user_role, user_org_id
  FROM user_profiles
  WHERE id = (event->>'user_id')::uuid;

  -- Ajouter aux claims
  claims := event->'claims';
  claims := jsonb_set(claims, '{user_role}', to_jsonb(user_role));
  claims := jsonb_set(claims, '{org_id}', to_jsonb(user_org_id));

  -- Retourner l'event modifie
  event := jsonb_set(event, '{claims}', claims);
  RETURN event;
END;
$$;

-- Donner les permissions necessaires
GRANT USAGE ON SCHEMA public TO supabase_auth_admin;
GRANT SELECT ON user_profiles TO supabase_auth_admin;
```

## Supabase Storage

### Configuration des buckets

```typescript
// Creer un bucket prive
const { data, error } = await supabase.storage.createBucket('documents', {
  public: false,
  fileSizeLimit: 10 * 1024 * 1024,  // 10 MB
  allowedMimeTypes: ['application/pdf', 'image/png', 'image/jpeg'],
});

// Creer un bucket public (avatars, images publiques)
const { data, error } = await supabase.storage.createBucket('avatars', {
  public: true,
  fileSizeLimit: 2 * 1024 * 1024,  // 2 MB
  allowedMimeTypes: ['image/png', 'image/jpeg', 'image/webp'],
});
```

### Storage Policies (RLS)

```sql
-- Policy : les utilisateurs uploadent dans leur propre dossier
CREATE POLICY "Users upload to own folder"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'documents'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

-- Policy : les utilisateurs lisent leurs propres fichiers
CREATE POLICY "Users read own files"
  ON storage.objects FOR SELECT
  USING (
    bucket_id = 'documents'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

-- Policy : les utilisateurs suppriment leurs propres fichiers
CREATE POLICY "Users delete own files"
  ON storage.objects FOR DELETE
  USING (
    bucket_id = 'documents'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

-- Policy : acces public en lecture au bucket avatars
CREATE POLICY "Public read avatars"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'avatars');
```

### Upload & Download

```typescript
// Upload un fichier dans le dossier de l'utilisateur
const userId = (await supabase.auth.getUser()).data.user?.id;

const { data, error } = await supabase.storage
  .from('documents')
  .upload(`${userId}/report-2024.pdf`, file, {
    contentType: 'application/pdf',
    upsert: false, // echouer si le fichier existe deja
  });

// Generer une URL signee (expiration limitee)
const { data: signedUrl } = await supabase.storage
  .from('documents')
  .createSignedUrl(`${userId}/report-2024.pdf`, 3600); // 1 heure

// URL publique (buckets publics uniquement)
const { data: publicUrl } = supabase.storage
  .from('avatars')
  .getPublicUrl(`${userId}/avatar.jpg`);
```

### Image Transformations

Supabase Storage supporte les transformations d'images a la volee :

```typescript
// Redimensionner et convertir
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl(`${userId}/avatar.jpg`, {
    transform: {
      width: 200,
      height: 200,
      resize: 'cover',  // 'cover' | 'contain' | 'fill'
      format: 'webp',
      quality: 80,
    },
  });
```

## Supabase Realtime

### Broadcast (messages ephemeres entre clients)

Utiliser le broadcast pour la communication directe entre clients sans persistence.

```typescript
// Creer un channel de broadcast
const channel = supabase.channel('room:lobby');

// Ecouter les messages
channel
  .on('broadcast', { event: 'cursor_move' }, (payload) => {
    console.log('Cursor moved:', payload);
  })
  .subscribe();

// Envoyer un message broadcast
channel.send({
  type: 'broadcast',
  event: 'cursor_move',
  payload: { x: 100, y: 200, userId: 'abc' },
});
```

### Presence (suivi des utilisateurs en ligne)

```typescript
const channel = supabase.channel('room:lobby');

// Ecouter les changements de presence
channel
  .on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState();
    console.log('Online users:', Object.keys(state).length);
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('User joined:', newPresences);
  })
  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    console.log('User left:', leftPresences);
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await channel.track({
        user_id: currentUser.id,
        username: currentUser.name,
        online_at: new Date().toISOString(),
      });
    }
  });

// Se deconnecter proprement
await channel.untrack();
```

### Postgres Changes (ecouter les changements de base de donnees)

```typescript
// Ecouter tous les INSERT sur la table messages
const channel = supabase
  .channel('db-changes')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'messages',
      filter: 'room_id=eq.123',  // filtre optionnel
    },
    (payload) => {
      console.log('New message:', payload.new);
    }
  )
  .on(
    'postgres_changes',
    {
      event: 'UPDATE',
      schema: 'public',
      table: 'messages',
      filter: 'room_id=eq.123',
    },
    (payload) => {
      console.log('Updated message:', payload.new, 'was:', payload.old);
    }
  )
  .subscribe();
```

Configuration cote PostgreSQL : activer la publication pour les tables souhaitees :

```sql
-- Ajouter les tables a la publication Realtime
ALTER PUBLICATION supabase_realtime ADD TABLE messages;
ALTER PUBLICATION supabase_realtime ADD TABLE notifications;

-- IMPORTANT : definir des RLS policies car Realtime respecte le RLS
-- Les clients ne recoivent que les changements des lignes qu'ils ont le droit de voir
```

### Realtime Performance Tips

- Limiter le nombre de channels par client (< 100)
- Utiliser des filtres (`filter` parameter) pour reduire le trafic
- Privilegier le broadcast pour les donnees ephemeres (curseurs, typing indicators)
- Utiliser les postgres changes uniquement pour les donnees persistees
- Configurer le `heartbeat_interval` pour detecter les deconnexions rapidement
- Considerer le throttling cote client pour les evenements haute frequence

## Edge Functions

### Structure d'une Edge Function

Les Edge Functions Supabase utilisent le runtime Deno. Elles s'executent au edge avec un cold start < 50ms.

```typescript
// supabase/functions/send-notification/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  // Gerer les preflight CORS
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Creer un client Supabase avec le JWT de l'utilisateur
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization')! },
        },
      }
    );

    // Verifier l'authentification
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Logique metier
    const { recipient_id, message } = await req.json();

    // Utiliser le service_role pour les operations admin
    const adminClient = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    );

    const { error } = await adminClient
      .from('notifications')
      .insert({
        user_id: recipient_id,
        sender_id: user.id,
        message,
        type: 'direct_message',
      });

    if (error) throw error;

    return new Response(JSON.stringify({ success: true }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }
});
```

### Cas d'usage des Edge Functions

| Cas d'usage | Pourquoi une Edge Function |
|-------------|--------------------------|
| **Webhooks tiers** | Recevoir et valider des webhooks Stripe, GitHub, etc. |
| **Envoi d'emails** | Appeler Resend, SendGrid, ou Postmark depuis le serveur |
| **AI/LLM** | Appeler OpenAI, Anthropic depuis le serveur (cles secretes) |
| **Logique metier complexe** | Orchestration multi-tables avec validation |
| **Cron jobs** | Declenchement periodique via pg_cron + pg_net |
| **Transformation de donnees** | Processing avant stockage |

### Invoquer une Edge Function depuis le client

```typescript
// Appel simple
const { data, error } = await supabase.functions.invoke('send-notification', {
  body: { recipient_id: 'user_456', message: 'Hello!' },
});

// Appel avec streaming (pour AI/LLM)
const { data } = await supabase.functions.invoke('ai-chat', {
  body: { prompt: 'Explain quantum computing' },
});

// data est un ReadableStream si la fonction retourne du streaming
const reader = data.getReader();
const decoder = new TextDecoder();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  console.log(decoder.decode(value));
}
```

### Edge Function avec Database Trigger

Declencher une Edge Function automatiquement sur un changement de base de donnees via `pg_net` et Database Webhooks :

```sql
-- Creer un webhook qui appelle une Edge Function sur INSERT
CREATE OR REPLACE FUNCTION notify_on_new_order()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM net.http_post(
    url := 'https://your-project.supabase.co/functions/v1/process-order',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'Authorization', 'Bearer ' || current_setting('supabase.service_role_key')
    ),
    body := jsonb_build_object(
      'order_id', NEW.id,
      'customer_id', NEW.customer_id,
      'total', NEW.total_amount
    )
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_new_order
  AFTER INSERT ON orders
  FOR EACH ROW EXECUTE FUNCTION notify_on_new_order();
```

## PostgREST Auto-Generated APIs

Supabase expose automatiquement une API REST complete generee depuis le schema PostgreSQL via PostgREST. Comprendre les conventions pour en tirer parti.

### Query Syntax

```typescript
// SELECT avec filtres
const { data } = await supabase
  .from('products')
  .select('id, name, price, category:categories(name)')  // jointure auto
  .eq('status', 'active')
  .gte('price', 10)
  .lte('price', 100)
  .order('price', { ascending: true })
  .range(0, 19);  // pagination offset (0-indexed)

// INSERT
const { data, error } = await supabase
  .from('orders')
  .insert({ customer_id: userId, total_amount: 99.99 })
  .select()  // retourner la ligne inseree
  .single();

// UPSERT (insert or update)
const { data } = await supabase
  .from('user_preferences')
  .upsert(
    { user_id: userId, theme: 'dark', language: 'fr' },
    { onConflict: 'user_id' }
  )
  .select()
  .single();

// UPDATE
const { data } = await supabase
  .from('orders')
  .update({ status: 'shipped', shipped_at: new Date().toISOString() })
  .eq('id', orderId)
  .select()
  .single();

// DELETE
const { error } = await supabase
  .from('orders')
  .delete()
  .eq('id', orderId);
```

### Appeler des fonctions PostgreSQL via RPC

```sql
-- Fonction PostgreSQL
CREATE OR REPLACE FUNCTION get_dashboard_stats(org_id uuid)
RETURNS jsonb
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT jsonb_build_object(
    'total_users', (SELECT count(*) FROM users WHERE organization_id = org_id),
    'total_orders', (SELECT count(*) FROM orders WHERE organization_id = org_id),
    'revenue_30d', (
      SELECT coalesce(sum(total_amount), 0)
      FROM orders
      WHERE organization_id = org_id
        AND created_at > now() - interval '30 days'
    )
  );
$$;
```

```typescript
// Appeler depuis le client
const { data, error } = await supabase.rpc('get_dashboard_stats', {
  org_id: 'org_123',
});
// data = { total_users: 42, total_orders: 156, revenue_30d: 12500.00 }
```

### Type Generation

Generer automatiquement les types TypeScript depuis le schema de base de donnees :

```bash
# Generer les types
npx supabase gen types typescript --project-id your-project-id > src/types/database.ts

# Ou depuis une instance locale
npx supabase gen types typescript --local > src/types/database.ts
```

```typescript
// Utiliser les types generes
import { Database } from '@/types/database';

type Tables = Database['public']['Tables'];
type Order = Tables['orders']['Row'];
type InsertOrder = Tables['orders']['Insert'];
type UpdateOrder = Tables['orders']['Update'];

// Client type-safe
const supabase = createClient<Database>(url, key);

// Autocompletion et verification des types
const { data } = await supabase
  .from('orders')  // autocomplete des noms de tables
  .select('id, status, total_amount')  // verification des colonnes
  .eq('status', 'pending');  // verification du type de la valeur
// data est type: Pick<Order, 'id' | 'status' | 'total_amount'>[]
```

## Supabase CLI & Local Development

### Setup initial

```bash
# Installer le CLI
npm install -g supabase

# Initialiser le projet
npx supabase init

# Demarrer l'environnement local (Docker requis)
npx supabase start

# URLs locales :
# API URL:    http://127.0.0.1:54321
# DB URL:     postgresql://postgres:postgres@127.0.0.1:54322/postgres
# Studio URL: http://127.0.0.1:54323
# Inbucket:   http://127.0.0.1:54324  (emails de test)
```

### Structure du projet

```
supabase/
├── config.toml              # Configuration du projet
├── migrations/
│   ├── 20240101000000_init.sql
│   ├── 20240115000000_add_orders.sql
│   └── 20240201000000_add_rls.sql
├── functions/
│   ├── send-notification/
│   │   └── index.ts
│   └── process-order/
│       └── index.ts
├── seed.sql                 # Donnees de test
└── tests/
    └── database/
        └── orders_test.sql
```

### Gestion des migrations

```bash
# Creer une nouvelle migration
npx supabase migration new add_products_table

# Appliquer les migrations en local
npx supabase db reset  # reset + replay toutes les migrations + seed

# Pousser les migrations en production
npx supabase db push

# Generer une migration depuis un diff (apres modifications manuelles en local)
npx supabase db diff --use-migra -f add_index_products

# Lier au projet distant
npx supabase link --project-ref your-project-id

# Pull le schema distant (introspection)
npx supabase db pull
```

### Tester les Edge Functions en local

```bash
# Demarrer une Edge Function en local avec hot reload
npx supabase functions serve send-notification --env-file .env.local

# Tester avec curl
curl -i --location --request POST \
  'http://127.0.0.1:54321/functions/v1/send-notification' \
  --header 'Authorization: Bearer eyJ...' \
  --header 'Content-Type: application/json' \
  --data '{"recipient_id": "user_456", "message": "test"}'

# Deployer une Edge Function
npx supabase functions deploy send-notification

# Deployer toutes les Edge Functions
npx supabase functions deploy
```

### Environnement de CI/CD

```yaml
# .github/workflows/supabase.yml
name: Supabase CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: supabase/setup-cli@v1
        with:
          version: latest

      - name: Start Supabase
        run: supabase start

      - name: Run migrations
        run: supabase db reset

      - name: Run tests
        run: supabase test db

      - name: Verify types
        run: |
          supabase gen types typescript --local > src/types/database.ts
          npx tsc --noEmit

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: supabase/setup-cli@v1

      - name: Link project
        run: supabase link --project-ref ${{ secrets.SUPABASE_PROJECT_ID }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: Push migrations
        run: supabase db push
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: Deploy Edge Functions
        run: supabase functions deploy
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
```

## Database Webhooks & Triggers

### Patterns de triggers PostgreSQL avec Supabase

```sql
-- Trigger : mettre a jour updated_at automatiquement
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Appliquer sur toutes les tables necessaires
CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

```sql
-- Trigger : creer un profil utilisateur automatiquement apres inscription
CREATE OR REPLACE FUNCTION create_user_profile()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.user_profiles (id, email, full_name)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', '')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION create_user_profile();
```

```sql
-- Trigger : envoyer une notification via pg_net quand une commande est creee
CREATE OR REPLACE FUNCTION notify_new_order()
RETURNS TRIGGER AS $$
BEGIN
    -- Notifier via le channel PostgreSQL (pour Realtime)
    PERFORM pg_notify('new_order', json_build_object(
        'order_id', NEW.id,
        'customer_id', NEW.customer_id,
        'total', NEW.total_amount
    )::text);

    -- Optionnel : appeler un webhook externe via pg_net
    PERFORM net.http_post(
        url := 'https://hooks.slack.com/services/...',
        headers := '{"Content-Type": "application/json"}'::jsonb,
        body := jsonb_build_object(
            'text', format('Nouvelle commande #%s : %s EUR', NEW.id, NEW.total_amount)
        )
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_order_created
    AFTER INSERT ON orders
    FOR EACH ROW EXECUTE FUNCTION notify_new_order();
```

### Database Webhooks via le Dashboard

Supabase offre une interface graphique pour configurer des webhooks sans SQL :

1. Aller dans Database > Webhooks dans le Dashboard
2. Creer un webhook sur une table et un evenement (INSERT, UPDATE, DELETE)
3. Specifier l'URL de destination (Edge Function ou endpoint externe)
4. Configurer les headers (Authorization, etc.)
5. Le webhook envoie automatiquement le payload avec `old_record` et `record`

## Supabase Production Checklist

Appliquer ces verifications avant la mise en production :

### Securite
1. Activer RLS sur TOUTES les tables accessibles depuis le client
2. Verifier que chaque table a des policies explicites (pas de "allow all")
3. Ne jamais exposer le `service_role_key` cote client
4. Configurer les domaines autorises dans Auth > URL Configuration
5. Activer le CAPTCHA sur les formulaires d'inscription si necessaire
6. Verifier les permissions des fonctions PostgreSQL (`SECURITY DEFINER` vs `INVOKER`)

### Performance
7. Activer Supavisor (connection pooling) avec le bon mode (transaction pour les serverless)
8. Creer des index sur les colonnes utilisees dans les policies RLS
9. Utiliser `select()` avec des colonnes explicites (pas de `select('*')` en production)
10. Configurer les cache headers sur les buckets Storage publics

### Operations
11. Activer les backups Point-in-Time Recovery (PITR) sur le plan Pro
12. Configurer les alertes de quota (base de donnees, storage, bandwidth)
13. Mettre en place le monitoring avec les metriques Supabase Dashboard
14. Documenter les procedures de rollback pour les migrations
15. Configurer les variables d'environnement des Edge Functions via le Dashboard (pas en dur dans le code)

### Type Safety
16. Generer les types TypeScript a chaque modification de schema (`supabase gen types`)
17. Integrer la generation de types dans le pipeline CI/CD
18. Utiliser le client type-safe `createClient<Database>()` partout
