# Next.js App Router — Guide Complet

## Overview

L'App Router (Next.js 13.4+, stable depuis 14) est une réécriture fondamentale du modèle mental de Next.js. Il introduit les React Server Components comme primitive centrale, un système de layouts imbriqués, et des conventions de fichiers pour le chargement, les erreurs et les métadonnées. Ce guide couvre chaque concept avec des exemples de production.

---

## App Router vs Pages Router — Différences Fondamentales

| Concept | Pages Router | App Router |
|---|---|---|
| Modèle de rendu | SSR/SSG/ISR via `getServerSideProps`, `getStaticProps` | RSC par défaut, rendu configurable par segment |
| Layouts | `_app.tsx`, composition manuelle | Layouts imbriqués automatiques via `layout.tsx` |
| Loading states | Spinner global, manual | `loading.tsx` avec Suspense automatique |
| Gestion d'erreurs | `_error.tsx` global | `error.tsx` par segment de route |
| Data fetching | Props injectées par Next.js | `async/await` direct dans les Server Components |
| Client/Serveur | Tout est client par défaut, SSR optionnel | Serveur par défaut, client opt-in avec `'use client'` |
| Mutations | API Routes + fetch client | Server Actions avec `'use server'` |
| Metadata | `next/head` dans chaque page | `metadata` export ou `generateMetadata` |

### Structure de répertoires App Router

```
app/
├── layout.tsx              ← Layout racine (obligatoire, html + body)
├── page.tsx                ← Route /
├── loading.tsx             ← Suspense boundary pour la route /
├── error.tsx               ← Error boundary pour la route /
├── not-found.tsx           ← 404 pour la route /
├── (auth)/                 ← Route group — ne crée pas de segment URL
│   ├── login/page.tsx      ← Route /login
│   └── register/page.tsx   ← Route /register
├── dashboard/
│   ├── layout.tsx          ← Layout imbriqué — wrape toutes les routes /dashboard/*
│   ├── page.tsx            ← Route /dashboard
│   └── analytics/
│       └── page.tsx        ← Route /dashboard/analytics
├── produits/
│   ├── page.tsx            ← Route /produits
│   └── [id]/
│       ├── page.tsx        ← Route /produits/[id]
│       └── avis/page.tsx   ← Route /produits/[id]/avis
└── api/
    └── webhook/route.ts    ← Route handler (équivalent API route)
```

---

## Server Components — Explication Complète

Les React Server Components s'exécutent exclusivement sur le serveur. Leur code n'est jamais envoyé au navigateur — seul le HTML résultant est transmis au client.

```typescript
// app/produits/page.tsx — Server Component (par défaut dans App Router)
// PAS de 'use client' → Server Component
import { db } from '@/lib/database'; // Import direct de la DB — possible car serveur uniquement
import { cookies, headers } from 'next/headers'; // APIs serveur

export default async function PageProduits({
  searchParams,
}: {
  searchParams: { catégorie?: string; page?: string };
}) {
  // Accès direct à la base de données — pas de fetch vers une API intermédiaire
  const produits = await db.query.produits.findMany({
    where: searchParams.catégorie
      ? eq(schéma.produits.catégorie, searchParams.catégorie)
      : undefined,
    limit: 24,
    offset: (Number(searchParams.page ?? 1) - 1) * 24,
    orderBy: [desc(schéma.produits.créeÀ)],
  });

  // Accès aux cookies/headers serveur directement
  const session = await getSession(cookies());
  const userAgent = headers().get('user-agent');

  return (
    <main>
      <h1>Produits</h1>
      {/* Client Component imbriqué — reçoit des données sérialisables en props */}
      <FiltresClient catégorieInitiale={searchParams.catégorie} />
      {/* Autres Server Components — composition native */}
      {produits.map(p => (
        <CarteProduitServeur key={p.id} produit={p} utilisateur={session?.user} />
      ))}
    </main>
  );
}
```

### Ce que les Server Components ne peuvent PAS faire

```typescript
// ❌ Interdit dans un Server Component
'use client'; // → Convertit en Client Component

// Pas d'état React
const [count, setCount] = useState(0); // ERREUR

// Pas d'effets
useEffect(() => {}, []); // ERREUR

// Pas d'event handlers dans le JSX
<button onClick={handleClick}>...</button> // ERREUR

// Pas d'accès aux APIs navigateur
window.localStorage.getItem('clé'); // ERREUR
document.getElementById('foo'); // ERREUR
```

---

## Client Components — Composition Îles d'Interactivité

```typescript
// components/FiltresClient.tsx
'use client'; // Directive explicite — tout ce fichier s'exécute côté client

import { useRouter, useSearchParams, usePathname } from 'next/navigation';
import { useTransition } from 'react';

export function FiltresClient({ catégorieInitiale }: { catégorieInitiale?: string }) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [isPending, startTransition] = useTransition();

  const changerCatégorie = (catégorie: string) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set('catégorie', catégorie);
    params.delete('page'); // Reset la pagination

    startTransition(() => {
      router.push(`${pathname}?${params.toString()}`);
    });
  };

  return (
    <div style={{ opacity: isPending ? 0.7 : 1 }}>
      {CATÉGORIES.map(cat => (
        <button
          key={cat.id}
          onClick={() => changerCatégorie(cat.id)}
          aria-pressed={catégorieInitiale === cat.id}
        >
          {cat.nom}
        </button>
      ))}
    </div>
  );
}
```

### Pattern : Server Component Parent → Client Component Enfant

```typescript
// ✅ Composition correcte
// app/page.tsx (Server Component)
import { BoutonLike } from './BoutonLike'; // Client Component

async function PageArticle({ params }: { params: { id: string } }) {
  const article = await db.getArticle(params.id); // Côté serveur
  return (
    <article>
      <h1>{article.titre}</h1>
      <p>{article.contenu}</p>
      {/* Passer des données sérialisables au Client Component */}
      <BoutonLike articleId={article.id} likesInitiaux={article.likes} />
    </article>
  );
}

// ❌ Anti-pattern : import d'un Server Component dans un Client Component
// 'use client'
// import { ComposantServeur } from './serveur'; // Ne fonctionnera pas
// Les Server Components ne peuvent être passés qu'en tant que props children
// depuis un parent Server Component
```

---

## Server Actions — Mutations sans API Routes

```typescript
// app/actions/produits.ts
'use server'; // Toutes les fonctions de ce fichier sont des Server Actions

import { revalidatePath, revalidateTag } from 'next/cache';
import { redirect } from 'next/navigation';
import { z } from 'zod';

const schémaCréation = z.object({
  nom: z.string().min(2).max(100),
  prix: z.coerce.number().positive(),
  catégorieId: z.string().uuid(),
  description: z.string().optional(),
});

// Server Action — s'exécute sur le serveur, peut être appelée depuis le client
export async function créerProduit(
  état: { erreur?: string; succès?: boolean },
  formData: FormData
): Promise<{ erreur?: string; succès?: boolean }> {
  // Validation côté serveur
  const résultat = schémaCréation.safeParse({
    nom: formData.get('nom'),
    prix: formData.get('prix'),
    catégorieId: formData.get('catégorieId'),
    description: formData.get('description'),
  });

  if (!résultat.success) {
    return { erreur: résultat.error.errors[0].message };
  }

  // Vérification d'autorisation côté serveur
  const session = await vérifierSession();
  if (!session?.user.peutGérerProduits) {
    return { erreur: 'Non autorisé' };
  }

  try {
    await db.insert(schéma.produits).values(résultat.data);
    revalidatePath('/produits'); // Invalider le cache de la page produits
    revalidateTag('produits');   // Invalider toutes les données taguées 'produits'
  } catch (e) {
    return { erreur: 'Erreur lors de la création' };
  }

  redirect('/produits'); // Redirection après succès
}

// Client Component utilisant la Server Action
'use client';
import { useActionState } from 'react'; // React 19 / Next.js 15
import { créerProduit } from '../actions/produits';

function FormulaireNouveauProduit() {
  const [état, action, isPending] = useActionState(créerProduit, {});

  return (
    <form action={action}>
      <input name="nom" placeholder="Nom du produit" required />
      <input name="prix" type="number" step="0.01" required />
      <select name="catégorieId">
        {CATÉGORIES.map(c => <option key={c.id} value={c.id}>{c.nom}</option>)}
      </select>
      {état.erreur && <p role="alert" className="erreur">{état.erreur}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? 'Création...' : 'Créer le produit'}
      </button>
    </form>
  );
}
```

### Progressive Enhancement avec Server Actions

Les formulaires utilisant des Server Actions fonctionnent même sans JavaScript côté client — le formulaire HTML natif envoie les données via POST. C'est l'avantage fondamental par rapport aux mutations via fetch.

---

## Route Handlers — API Routes App Router

```typescript
// app/api/produits/route.ts
import { NextRequest, NextResponse } from 'next/server';

// GET /api/produits
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const catégorie = searchParams.get('catégorie');

  const produits = await db.query.produits.findMany({
    where: catégorie ? eq(schéma.produits.catégorie, catégorie) : undefined,
  });

  return NextResponse.json(produits);
}

// POST /api/produits
export async function POST(request: NextRequest) {
  const session = await getServerSession();
  if (!session) return NextResponse.json({ erreur: 'Non autorisé' }, { status: 401 });

  const corps = await request.json();
  const produit = await db.insert(schéma.produits).values(corps).returning();

  revalidateTag('produits');
  return NextResponse.json(produit[0], { status: 201 });
}

// app/api/produits/[id]/route.ts — Route dynamique
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  await db.delete(schéma.produits).where(eq(schéma.produits.id, params.id));
  revalidatePath('/produits');
  return new NextResponse(null, { status: 204 });
}
```

---

## Middleware — Auth, i18n, A/B Testing

```typescript
// middleware.ts — s'exécute à la périphérie (Edge Runtime)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Auth : protéger les routes /dashboard/*
  if (pathname.startsWith('/dashboard')) {
    const token = request.cookies.get('session-token')?.value;
    if (!token || !vérifierToken(token)) {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  // i18n : détecter la langue et rediriger
  if (pathname === '/') {
    const langue = request.headers.get('accept-language')?.split(',')[0] ?? 'fr';
    const langueSupport = ['fr', 'en', 'de'].includes(langue.slice(0, 2)) ? langue.slice(0, 2) : 'fr';
    return NextResponse.redirect(new URL(`/${langueSupport}`, request.url));
  }

  // A/B Testing : assigner un groupe et ajouter un header
  const groupeAB = request.cookies.get('ab-groupe')?.value;
  if (!groupeAB && pathname.startsWith('/checkout')) {
    const response = NextResponse.next();
    const groupe = Math.random() > 0.5 ? 'A' : 'B';
    response.cookies.set('ab-groupe', groupe, { maxAge: 60 * 60 * 24 * 30 });
    response.headers.set('x-ab-groupe', groupe);
    return response;
  }

  return NextResponse.next();
}

export const config = {
  // Matcher : quelles routes déclenchent le middleware
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
```

---

## Routes Parallèles et Routes Interceptées

```typescript
// app/layout.tsx — Routes parallèles : afficher deux sections simultanément
export default function Layout({
  children,
  // @tableau et @notifications sont des "slots" définis par les dossiers @
  tableau,
  notifications,
}: {
  children: React.ReactNode;
  tableau: React.ReactNode;
  notifications: React.ReactNode;
}) {
  return (
    <div>
      {children}
      <div className="dashboard-grid">
        {tableau}
        {notifications}
      </div>
    </div>
  );
}

// app/@modal/(.)produits/[id]/page.tsx — Route interceptée pour un modal
// (.produits/[id] intercepte /produits/[id] quand on navigue depuis la même section
'use client';
import { useRouter } from 'next/navigation';

export default function ModalProduit({ params }: { params: { id: string } }) {
  const router = useRouter();
  return (
    <div className="modal-overlay" onClick={() => router.back()}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        {/* Contenu du produit — URL reste /produits/[id] mais affiché en modal */}
        <ProduitRapide id={params.id} />
      </div>
    </div>
  );
}
```

---

## Cache — Stratégie Avancée

```typescript
// 1. Cache de fetch — contrôle par requête
async function getDonnéesProduit(id: string) {
  const res = await fetch(`https://api.exemple.com/produits/${id}`, {
    next: {
      revalidate: 3600,        // ISR : revalider toutes les heures
      tags: ['produits', `produit-${id}`], // Tags pour invalidation ciblée
    },
    // cache: 'no-store' → toujours frais (SSR)
    // cache: 'force-cache' → permanent jusqu'à invalidation manuelle
  });
  return res.json();
}

// 2. unstable_cache — cacher des appels DB (non-fetch)
import { unstable_cache } from 'next/cache';

const getProduitsParCatégorie = unstable_cache(
  async (catId: string) => {
    return db.query.produits.findMany({ where: eq(schéma.produits.catégorie, catId) });
  },
  ['produits-catégorie'], // Clé de cache
  { revalidate: 600, tags: ['produits'] } // 10 min, invalider avec revalidateTag('produits')
);

// 3. Invalidation on-demand depuis une Server Action ou Route Handler
import { revalidatePath, revalidateTag } from 'next/cache';

// Webhook Stripe : invalider les données de commande après paiement
export async function POST(request: NextRequest) {
  const événement = await vérifierWebhookStripe(request);

  if (événement.type === 'checkout.session.completed') {
    const commandeId = événement.data.object.metadata.commandeId;
    revalidateTag(`commande-${commandeId}`);  // Ciblé
    revalidatePath('/dashboard/commandes');    // Segment de route
  }

  return NextResponse.json({ reçu: true });
}

// 4. React cache — déduplication dans le même rendu
import { cache } from 'react';

// Plusieurs appels à getUtilisateur(id) dans le même rendu → 1 seule requête
export const getUtilisateur = cache(async (id: string) => {
  return db.query.utilisateurs.findFirst({ where: eq(schéma.utilisateurs.id, id) });
});
```

---

## Metadata API

```typescript
// app/produits/[id]/page.tsx

// Metadata statique
export const metadata: Metadata = {
  title: 'Catalogue Produits',
  description: 'Découvrez notre sélection de produits',
};

// Metadata dynamique — async, accès aux données
export async function generateMetadata(
  { params }: { params: { id: string } },
  parent: ResolvingMetadata
): Promise<Metadata> {
  const produit = await getProduit(params.id);
  const parentMeta = await parent;
  const imagesParentes = parentMeta.openGraph?.images ?? [];

  return {
    title: `${produit.nom} — Boutique`,
    description: produit.descriptionCourte,
    openGraph: {
      title: produit.nom,
      description: produit.descriptionCourte,
      images: [{ url: produit.imageUrl, width: 1200, height: 630 }, ...imagesParentes],
      type: 'website',
    },
    alternates: {
      canonical: `https://exemple.com/produits/${params.id}`,
    },
  };
}
```

---

## generateStaticParams et Fallback

```typescript
// app/produits/[id]/page.tsx

// Pré-générer les pages produits au build time
export async function generateStaticParams() {
  // Générer les routes statiques pour les 1000 produits les plus vus
  const produits = await db.query.produits.findMany({
    orderBy: [desc(schéma.produits.vues)],
    limit: 1000,
    columns: { id: true },
  });

  return produits.map(p => ({ id: p.id }));
}

// Comportement pour les routes non pré-générées
export const dynamicParams = true; // true (défaut) : générer à la demande et mettre en cache
// dynamicParams = false → 404 pour les IDs non pré-générés
```

---

## Déploiement — Vercel vs Self-Hosted

### Vercel (référence)

Déploiement natif : `git push` déclenche le build. Les fonctionnalités suivantes nécessitent Vercel ou une configuration équivalente : Edge Middleware géographiquement distribué, Image Optimization via CDN, ISR via infrastructure dédiée.

### Self-Hosted Node.js

```dockerfile
# Dockerfile optimisé pour Next.js standalone
FROM node:22-alpine AS deps
WORKDIR /app
COPY package*.json .
RUN npm ci --only=production

FROM node:22-alpine AS builder
WORKDIR /app
COPY . .
COPY --from=deps /app/node_modules ./node_modules
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Mode standalone : sortie autonome incluant les dépendances nécessaires
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
```

```javascript
// next.config.js — activer le mode standalone
const nextConfig = {
  output: 'standalone', // Génère .next/standalone avec tout le nécessaire
};
```

### Variables d'environnement — Sécurité

```typescript
// ✅ Variables serveur uniquement — jamais exposées au client
POSTGRES_URL=postgresql://...
STRIPE_SECRET_KEY=sk_live_EXAMPLE_KEY_REPLACE_ME

// ✅ Variables exposées au client — préfixe NEXT_PUBLIC_ obligatoire
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
NEXT_PUBLIC_APP_URL=https://monapp.com

// Accès TypeScript sécurisé
import { z } from 'zod';

const envServeur = z.object({
  POSTGRES_URL: z.string().url(),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
}).parse(process.env);

// Ne jamais accéder à process.env directement dans des Server Components critiques
// — utiliser un module env/ validé à l'initialisation
```
