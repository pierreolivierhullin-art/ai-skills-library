# Études de Cas — Frontend Frameworks en Production

## Cas 1 : Migration Pages Router → App Router (SaaS 50K Utilisateurs)

### Contexte

Planify, SaaS de gestion de projets B2B, sert 50 000 utilisateurs actifs mensuels avec un abonnement mensuel moyen de 45 EUR. L'application Next.js 12 (Pages Router) existe depuis 3 ans — 180 pages, 320 composants, 45 000 lignes de TypeScript. L'équipe frontend est composée de 6 développeurs. Le bundle JavaScript client pèse 2.1 Mo (parsé), le LCP médian est à 3.8s, et le TTI à 4.9s sur mobile 4G. Le CTO impose un objectif de Core Web Vitals dans le vert avant le renouvellement des abonnements annuels dans 4 mois, suite à des retours clients sur la lenteur de l'application.

### Problème

L'architecture Pages Router présente trois problèmes structurels. Premièrement, `getServerSideProps` est abusé sur 60% des pages alors que les données ne sont pas dynamiques par utilisateur — tout le HTML est régénéré à chaque requête. Deuxièmement, le bundle client embarque des dizaines de composants de visualisation de données (charts, tableaux) qui ne sont utiles que dans certaines vues, faute de code-splitting systématique. Troisièmement, les mises en page imbriquées (tableau de bord → section → sous-section) provoquent un problème de "layout shift" à chaque navigation car chaque page remonte toute la hiérarchie de composants.

L'équipe est consciente que la réécriture complète en App Router en parallèle du développement produit est impossible. La contrainte : livrer les améliorations de performance en production sans bloquer les 4 développeurs travaillant sur les nouvelles fonctionnalités.

### Solution

**Stratégie : migration page par page par valeur business**

La migration a suivi une approche "incrementale cohabitante" : les Pages Router et App Router coexistent dans le même projet Next.js 14 pendant 8 semaines, le routing étant automatiquement résolu par Next.js (App Router prioritaire sur `app/`, Pages Router pour le reste).

**Phase 1 — RSC pour les pages data-heavy (semaines 1-3)**

Les pages de rapport et d'analytics (18 pages) ont été migrées en priorité. Ce sont les pages avec le plus de `getServerSideProps` et le plus de données statiques par session.

```typescript
// ❌ AVANT : Pages Router — getServerSideProps
// pages/dashboard/rapports.tsx
export const getServerSideProps: GetServerSideProps = async (ctx) => {
  const session = await getServerSession(ctx.req, ctx.res);
  const rapports = await prisma.rapport.findMany({
    where: { équipeId: session.user.équipeId },
    orderBy: { créeÀ: 'desc' },
    take: 50,
  });
  return { props: { rapports: JSON.parse(JSON.stringify(rapports)) } };
};

export default function PageRapports({ rapports }: { rapports: Rapport[] }) {
  return <ListeRapports rapports={rapports} />;
}
```

```typescript
// ✅ APRÈS : App Router — Server Component direct
// app/(dashboard)/rapports/page.tsx
import { auth } from '@/lib/auth'; // next-auth v5 Server Component compatible
import { db } from '@/lib/database';

export default async function PageRapports() {
  const session = await auth(); // Accès direct — pas de getServerSideProps
  if (!session) redirect('/login');

  // Accès DB direct — pas de sérialisation/désérialisation JSON
  const rapports = await db.query.rapports.findMany({
    where: eq(schéma.rapports.équipeId, session.user.équipeId),
    orderBy: [desc(schéma.rapports.créeÀ)],
    limit: 50,
  });

  return (
    <div>
      {/* Server Component pur — aucun JS envoyé pour ce composant */}
      <EntêteRapports count={rapports.length} />
      {/* Client Component pour les interactions (filtres, tri) */}
      <Suspense fallback={<SqueletteRapports />}>
        <ListeRapportsClient rapports={rapports} />
      </Suspense>
    </div>
  );
}
```

**Phase 2 — Server Actions remplaçant les API routes (semaines 4-6)**

Les 23 API routes dédiées aux mutations (créer/modifier/supprimer) ont été converties en Server Actions. Bénéfice : suppression du code fetch côté client, progressive enhancement natif, validation Zod centralisée côté serveur.

```typescript
// app/actions/projets.ts
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';

const schémaNouveauProjet = z.object({
  nom: z.string().min(3, 'Minimum 3 caractères').max(60),
  description: z.string().max(500).optional(),
  dateÉchéance: z.coerce.date().min(new Date(), 'La date doit être dans le futur'),
});

export async function créerProjet(
  prevState: ActionState,
  formData: FormData
): Promise<ActionState> {
  const session = await auth();
  if (!session) return { erreur: 'Non authentifié' };

  const validation = schémaNouveauProjet.safeParse(Object.fromEntries(formData));
  if (!validation.success) {
    return { erreur: validation.error.errors[0].message };
  }

  const projet = await db.insert(schéma.projets).values({
    ...validation.data,
    équipeId: session.user.équipeId,
    créateurId: session.user.id,
  }).returning();

  revalidatePath('/dashboard/projets');
  revalidateTag(`équipe-${session.user.équipeId}-projets`);

  return { succès: true, projetId: projet[0].id };
}
```

**Phase 3 — layouts imbriqués et loading.tsx (semaines 7-8)**

```
app/(dashboard)/
├── layout.tsx          ← Navigation principale — rendue une fois, persist entre routes
├── loading.tsx         ← Suspense boundary : squelette affiché pendant navigation
├── projets/
│   ├── layout.tsx      ← Barre latérale projets — persist dans /projets/*
│   ├── page.tsx        ← Liste des projets
│   ├── loading.tsx     ← Squelette spécifique à la liste
│   └── [id]/
│       ├── layout.tsx  ← En-tête projet + onglets — persist entre onglets
│       ├── page.tsx    ← Vue générale
│       ├── tâches/page.tsx
│       └── membres/page.tsx
```

### Métriques Avant / Après

| Métrique | Avant (Pages Router) | Après (App Router) | Amélioration |
|---|---|---|---|
| Bundle JS client | 2.1 Mo parsé | 1.26 Mo parsé | **-40%** |
| LCP médian | 3.8s | 2.1s | **-45%** |
| TTI médian (mobile 4G) | 4.9s | 2.7s | **-45%** |
| Requêtes DB par navigation | 3.2 moy. | 1.4 moy. | **-56%** |
| API routes en production | 23 | 4 (webhooks seulement) | **-83%** |
| Durée de migration | — | 8 semaines (2 dev) | — |

### Leçon Principale

La migration page par page, en commençant par les pages à fort trafic et à données non-dynamiques, produit des gains rapides et mesurables sans bloquer le développement produit. L'investissement le plus important n'est pas la réécriture du code mais la réflexion sur la frontière Client/Serveur pour chaque composant. Un composant qui lit des données statiques et n'a pas d'interactivité doit être Server Component par défaut, même s'il était historiquement client.

---

## Cas 2 : Refactorisation State Management — Context Hell → Zustand + TanStack Query

### Contexte

Mediboard, plateforme de gestion médicale pour les cliniques, a une application React 18 (sans Next.js, Vite + React Router) avec 4 ans d'histoire. L'état global est géré entièrement par React Context : 14 Contexts imbriqués au niveau racine de l'application. L'équipe de 8 développeurs constate depuis 6 mois des performances dégradées sur des machines de bureau standard utilisées par les infirmières — les salles de soin utilisent des postes HP avec 8 Go de RAM et Chrome.

### Problème

Un profil React DevTools enregistré lors de l'ouverture du module "Admission patient" révèle 47 re-renders en cascade pour un seul clic — le bouton "Nouvelle admission". La cause : le Context `PatientContext` contient à la fois les données patients (200+ entrées) et des états UI (modal ouverte, patient sélectionné, filtres). Quand le modal s'ouvre (`modalOuverte = true`), tous les 47 composants consommant `PatientContext` re-rendent, dont des composants purement affichage qui n'utilisent que `patients.length`.

```typescript
// ❌ AVANT : Un context trop large
interface PatientContextValue {
  patients: Patient[];        // Données — change rarement
  chargement: boolean;        // État fetch
  erreur: Error | null;
  modalOuverte: boolean;      // UI state — change souvent
  patientSélectionné: string | null;  // UI state
  filtres: Filtres;           // UI state
  rechercheTexte: string;     // UI state — change à chaque frappe
  setModalOuverte: (v: boolean) => void;
  sélectionnerPatient: (id: string) => void;
  setFiltres: (f: Filtres) => void;
  setRechercheTexte: (t: string) => void;
  rafraîchir: () => Promise<void>;
}
// Résultat : 47 composants abonnés à TOUT ce Context
```

### Solution

**Architecture cible : séparation données serveur / état UI**

```
TanStack Query    → données patients (cache, loading, erreur, refresh)
Zustand           → état UI global (modal, sélection, filtres)
useState local    → état temporaire de formulaire
```

**Étape 1 — Extraire les données serveur vers TanStack Query**

```typescript
// queries/patients.queries.ts
import { queryOptions, useMutation, useQueryClient } from '@tanstack/react-query';

export const patientQueries = {
  all: (filtres: Filtres) => queryOptions({
    queryKey: ['patients', filtres],
    queryFn: () => api.getPatients(filtres),
    staleTime: 2 * 60 * 1000, // 2 min — données médicales, fraîcheur importante
    gcTime: 10 * 60 * 1000,
  }),

  detail: (id: string) => queryOptions({
    queryKey: ['patient', id],
    queryFn: () => api.getPatient(id),
    enabled: !!id,
  }),
};

// Usage dans les composants — sélecteurs précis évitent les re-renders inutiles
function CompteurPatients() {
  const { data } = useQuery(patientQueries.all(filtresVides));
  return <span>{data?.length ?? 0} patients</span>;
  // Re-render seulement si le nombre de patients change
}
```

**Étape 2 — État UI vers Zustand avec sélecteurs atomiques**

```typescript
// store/admissions.store.ts
import { create } from 'zustand';

interface AdmissionsStore {
  modalOuverte: boolean;
  patientSélectionné: string | null;
  filtres: Filtres;
  rechercheTexte: string;
  // Actions
  ouvrirModal: () => void;
  fermerModal: () => void;
  sélectionnerPatient: (id: string | null) => void;
  setFiltres: (filtres: Partial<Filtres>) => void;
  setRechercheTexte: (texte: string) => void;
}

export const useAdmissionsStore = create<AdmissionsStore>()((set) => ({
  modalOuverte: false,
  patientSélectionné: null,
  filtres: filtresParDéfaut,
  rechercheTexte: '',

  ouvrirModal: () => set({ modalOuverte: true }),
  fermerModal: () => set({ modalOuverte: false, patientSélectionné: null }),
  sélectionnerPatient: (id) => set({ patientSélectionné: id }),
  setFiltres: (filtres) => set(state => ({ filtres: { ...state.filtres, ...filtres } })),
  setRechercheTexte: (rechercheTexte) => set({ rechercheTexte }),
}));

// Sélecteurs précis — chaque composant souscrit exactement ce qu'il utilise
const modalOuverte = useAdmissionsStore(state => state.modalOuverte);
// Ce composant ne re-render PAS si rechercheTexte change
```

### Métriques Avant / Après

| Métrique | Avant | Après | Amélioration |
|---|---|---|---|
| Re-renders par clic "Nouvelle admission" | 47 | 3 | **-94%** |
| Temps de réponse perçu (clic → modal visible) | 280ms | 18ms | **-94%** |
| Mémoire JS heap (session 1h) | 380 Mo | 195 Mo | **-49%** |
| Plaintes performance utilisateurs (mois) | 23 tickets | 1 ticket | **-96%** |
| Durée de refactorisation | — | 3 semaines (1 dev) | — |

### Leçon Principale

La règle d'or : ne jamais mettre dans le même Context des données qui changent à des fréquences différentes. Les données serveur (patients) et l'état UI (modal, filtres) évoluent à des rythmes fondamentalement différents et doivent être gérés par des outils différents. TanStack Query pour les données distantes, Zustand ou Context ciblé pour l'état UI partagé — jamais les deux dans le même Context.

---

## Cas 3 : E-commerce Next.js — ISR et Revalidation On-Demand

### Contexte

Maison Leroux, distributeur de mobilier haut de gamme en ligne, opère un catalogue de 50 000 SKUs sur Next.js 14. Chaque fiche produit affiche le prix, le stock, 8-15 photos, les dimensions, les couleurs disponibles et les avis clients. Le taux de conversion est de 3.2%, et chaque seconde de LCP supplémentaire coûte en moyenne 0.3% de conversion selon les tests A/B internes. Le stock est géré dans un ERP SAP avec des mises à jour en temps quasi-réel (délai max 15 minutes exigé par contrat avec les fournisseurs). L'équipe technique est de 3 développeurs.

### Problème

La génération SSR de chaque fiche produit à chaque requête pénalise les performances : le TTFB moyen est de 820ms car SAP est interrogé à chaque requête, même pour un produit dont le stock n'a pas changé depuis 6 heures. La mise en cache CDN (CloudFront) est configurée à 0 pour éviter les données périmées — décision prise suite à un incident où des clients ont commandé des produits affichés en stock alors qu'ils étaient épuisés. Résultat : aucune mise en cache, performances SSR pures.

### Solution

**Architecture : ISR + revalidation on-demand déclenchée par SAP**

Le problème fondamental n'est pas le cache — c'est l'absence de mécanisme d'invalidation fiable. La solution combine ISR (cache jusqu'à 1 heure) avec une invalidation ciblée déclenchée dès qu'un produit change dans SAP.

```typescript
// app/produits/[slug]/page.tsx

// Pré-générer les 500 produits les plus vus au build
export async function generateStaticParams() {
  const produits = await db.query.produits.findMany({
    orderBy: [desc(schéma.produits.vues)],
    limit: 500,
    columns: { slug: true },
  });
  return produits.map(p => ({ slug: p.slug }));
}

// Les autres slugs : génération à la demande et mise en cache
export const dynamicParams = true; // Défaut — génère les pages non pré-buildées

// Revalidation ISR : toutes les 3600s si pas d'invalidation on-demand
export const revalidate = 3600;

export default async function PageProduit({ params }: { params: { slug: string } }) {
  const produit = await getProduit(params.slug); // Mis en cache avec le tag

  if (!produit) notFound();

  return (
    <main>
      <GalerieProduit images={produit.images} />
      {/* Stock temps réel via Client Component — données non cachées */}
      <Suspense fallback={<IndicateurStock skeleton />}>
        <StockTempsRéel produitId={produit.id} />
      </Suspense>
      <PrixProduit produit={produit} />
      <DescriptionProduit description={produit.description} />
    </main>
  );
}

// lib/produits.ts — fetch avec tag pour invalidation ciblée
import { unstable_cache } from 'next/cache';

export const getProduit = unstable_cache(
  async (slug: string) => {
    return db.query.produits.findFirst({
      where: eq(schéma.produits.slug, slug),
      with: { images: true, catégorie: true, attributs: true },
    });
  },
  ['produit-par-slug'],
  {
    revalidate: 3600,
    tags: (slug) => [`produit-${slug}`, 'produits'],
  }
);
```

**Webhook SAP → invalidation on-demand**

```typescript
// app/api/webhooks/sap/route.ts
import { revalidateTag } from 'next/cache';
import { NextRequest, NextResponse } from 'next/server';
import { createHmac } from 'crypto';

interface SapWebhookPayload {
  type: 'STOCK_UPDATE' | 'PRIX_UPDATE' | 'PRODUIT_DESACTIVE';
  produitIds: string[];
  timestamp: string;
}

export async function POST(request: NextRequest) {
  // Vérification signature HMAC — authentifier les appels SAP
  const signature = request.headers.get('x-sap-signature');
  const corps = await request.text();
  const signatureAttendue = createHmac('sha256', process.env.SAP_WEBHOOK_SECRET!)
    .update(corps)
    .digest('hex');

  if (!signature || !timingSafeEqual(Buffer.from(signature), Buffer.from(signatureAttendue))) {
    return NextResponse.json({ erreur: 'Signature invalide' }, { status: 401 });
  }

  const payload: SapWebhookPayload = JSON.parse(corps);

  // Récupérer les slugs correspondant aux IDs SAP
  const produits = await db.query.produits.findMany({
    where: inArray(schéma.produits.sapId, payload.produitIds),
    columns: { id: true, slug: true },
  });

  // Invalider les caches ciblés — seulement les produits modifiés
  for (const produit of produits) {
    revalidateTag(`produit-${produit.slug}`);
  }

  // Pour les mises à jour de prix : invalider aussi les pages catégorie
  if (payload.type === 'PRIX_UPDATE') {
    revalidateTag('pages-catégorie');
  }

  console.log(`Invalidé ${produits.length} fiches produit suite à événement SAP ${payload.type}`);
  return NextResponse.json({ invalidés: produits.length });
}
```

**Stock temps réel — Client Component isolé**

```typescript
// components/StockTempsRéel.tsx — données NON cachées, fraîches à chaque render
'use client';

function StockTempsRéel({ produitId }: { produitId: string }) {
  const { data: stock } = useQuery({
    queryKey: ['stock', produitId],
    queryFn: () => fetch(`/api/stock/${produitId}`).then(r => r.json()),
    refetchInterval: 5 * 60 * 1000, // Rafraîchir toutes les 5 min
    staleTime: 2 * 60 * 1000,
  });

  if (!stock) return null;

  return (
    <div className="stock-indicator">
      {stock.quantité > 10 ? (
        <span className="en-stock">En stock</span>
      ) : stock.quantité > 0 ? (
        <span className="stock-limité">Plus que {stock.quantité} en stock</span>
      ) : (
        <span className="épuisé">Épuisé — délai {stock.délaiApprovisionnement}j</span>
      )}
    </div>
  );
}
```

### Métriques Avant / Après

| Métrique | Avant (SSR pur) | Après (ISR + on-demand) | Amélioration |
|---|---|---|---|
| TTFB médian | 820ms | 45ms (hit cache) | **-95%** |
| LCP médian | 2.9s | 1.4s | **-52%** |
| Requêtes SAP/min en heure de pointe | 1 200 | 8 (webhooks) | **-99%** |
| Taux de conversion | 3.2% | 3.8% | **+19%** |
| Incidents "produit épuisé commandé" | 3/mois | 0 en 6 mois | **Éliminés** |
| Coût hébergement (compute) | Base | Base × 0.4 | **-60%** |

### Leçon Principale

ISR sans revalidation on-demand n'est qu'une mise en cache approximative. La combinaison ISR + webhook d'invalidation ciblée offre le meilleur des deux mondes : performance CDN maximale avec fraîcheur contrôlée. Le découplage du stock (Client Component avec polling) de la fiche produit (Server Component mis en cache) est la clé : les données à haute fréquence de changement ne doivent jamais être dans le même cache que les données stables.

---

## Cas 4 : Micro-Frontend avec Module Federation

### Contexte

Kantoor, éditeur d'une suite RH enterprise (paie, recrutement, congés, formations, reporting), opère avec 5 squads autonomes de 6 développeurs chacune. Historiquement, une seule application React monolithique de 280 000 lignes, déployée toutes les deux semaines après une phase de validation croisée entre squads. Les conflits de merge entre squads font perdre en moyenne 3 jours par sprint. Le design system partagé (80 composants) introduit des breaking changes qui bloquent des squads non concernées.

### Problème

La monorepo partagée crée une dépendance organisationnelle coûteuse. Une squad qui modifie le composant `DataTable` du design system pour ses besoins peut casser les 4 autres squads. Le pipeline CI prend 22 minutes pour toute la suite — chaque push de n'importe quelle squad bloque les autres pendant ce temps. La version de React est bloquée à 17 car une mise à jour nécessite la validation simultanée de toutes les squads, un effort de coordination impossible à orchestrer.

### Solution

**Architecture : Module Federation (Webpack 5) avec shell orchestrateur**

```
                         ┌─────────────────────────┐
                         │   Shell Application      │
                         │   (React 18, routing)   │
                         │   Port 3000              │
                         └──────────┬──────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
   ┌──────▼──────┐          ┌───────▼──────┐         ┌───────▼──────┐
   │   MF Paie   │          │  MF Recrut.  │         │  MF Congés   │
   │  Port 3001  │          │  Port 3002   │         │  Port 3003   │
   └─────────────┘          └──────────────┘         └──────────────┘
          │                         │
   ┌──────▼──────┐          ┌───────▼──────┐
   │  MF Formation│          │ MF Reporting │
   │  Port 3004  │          │  Port 3005   │
   └─────────────┘          └──────────────┘
          │                         │
          └──────────┬──────────────┘
                     │
          ┌──────────▼──────────────┐
          │    Design System MF     │
          │    (shared singleton)   │
          └─────────────────────────┘
```

**Configuration Module Federation**

```javascript
// shell/webpack.config.js
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'shell',
      remotes: {
        mfPaie: `mfPaie@${process.env.MF_PAIE_URL}/remoteEntry.js`,
        mfRecrutement: `mfRecrutement@${process.env.MF_RECRUTEMENT_URL}/remoteEntry.js`,
        mfCongés: `mfCongés@${process.env.MF_CONGES_URL}/remoteEntry.js`,
        mfFormation: `mfFormation@${process.env.MF_FORMATION_URL}/remoteEntry.js`,
        mfReporting: `mfReporting@${process.env.MF_REPORTING_URL}/remoteEntry.js`,
        designSystem: `designSystem@${process.env.DESIGN_SYSTEM_URL}/remoteEntry.js`,
      },
      shared: {
        react: { singleton: true, requiredVersion: '^18.0.0' },
        'react-dom': { singleton: true, requiredVersion: '^18.0.0' },
        'react-router-dom': { singleton: true },
        // Design system : singleton pour éviter les instances multiples
        '@kantoor/design-system': { singleton: true, eager: true },
      },
    }),
  ],
};

// mf-paie/webpack.config.js — chaque micro-frontend expose ses routes
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'mfPaie',
      filename: 'remoteEntry.js',
      exposes: {
        './Module': './src/module', // Point d'entrée des routes paie
        './BullettinPaie': './src/components/BulletinPaie', // Composant réutilisable
      },
      shared: { /* mêmes singletons */ },
    }),
  ],
};
```

**Shell : chargement lazy des micro-frontends**

```typescript
// shell/src/App.tsx
import { lazy, Suspense } from 'react';

const ModulePaie = lazy(() => import('mfPaie/Module'));
const ModuleRecrutement = lazy(() => import('mfRecrutement/Module'));
const ModuleCongés = lazy(() => import('mfCongés/Module'));

function App() {
  return (
    <ErrorBoundary fallback={<ErreurModuleMicrofrontend />}>
      <Router>
        <Navigation />
        <Suspense fallback={<ChargementModule />}>
          <Routes>
            <Route path="/paie/*" element={<ModulePaie />} />
            <Route path="/recrutement/*" element={<ModuleRecrutement />} />
            <Route path="/congés/*" element={<ModuleCongés />} />
          </Routes>
        </Suspense>
      </Router>
    </ErrorBoundary>
  );
}

// Communication inter-modules via événements custom (pas de couplage direct)
function ErreurModuleMicrofrontend({ erreur }: { erreur: Error }) {
  // Si un MF est down, afficher l'erreur sans impacter les autres
  return (
    <div role="alert">
      <h2>Module temporairement indisponible</h2>
      <p>Les autres modules de la suite restent accessibles.</p>
    </div>
  );
}
```

**Partage d'état via événements custom — découplage total**

```typescript
// shared/events.ts — bus d'événements léger entre micro-frontends
type KantoorEvent =
  | { type: 'UTILISATEUR_SÉLECTIONNÉ'; employéId: string }
  | { type: 'CONGÉ_APPROUVÉ'; congéId: string; employéId: string }
  | { type: 'NAVIGATION'; route: string };

const eventBus = new EventTarget();

export function émettreÉvénement(event: KantoorEvent) {
  eventBus.dispatchEvent(new CustomEvent(event.type, { detail: event }));
}

export function écouterÉvénement<T extends KantoorEvent['type']>(
  type: T,
  handler: (event: Extract<KantoorEvent, { type: T }>) => void
) {
  const listener = (e: Event) => handler((e as CustomEvent).detail);
  eventBus.addEventListener(type, listener);
  return () => eventBus.removeEventListener(type, listener);
}

// Dans mf-paie : émettre un événement quand un bulletin est généré
émettreÉvénement({ type: 'CONGÉ_APPROUVÉ', congéId: '123', employéId: '456' });

// Dans mf-reporting : écouter et réagir
useEffect(() => {
  return écouterÉvénement('CONGÉ_APPROUVÉ', ({ employéId }) => {
    queryClient.invalidateQueries(['rapport-congés', employéId]);
  });
}, []);
```

### Métriques Avant / Après

| Métrique | Avant (monolithe) | Après (Module Federation) | Amélioration |
|---|---|---|---|
| Fréquence de déploiement | Bi-hebdomadaire (toute la suite) | Quotidienne par squad | **+7x** |
| Temps de pipeline CI | 22 min (tout) | 4-6 min (par MF) | **-75%** |
| Conflits de merge bloquants | 3j perdus/sprint | 0.5j perdus/sprint | **-83%** |
| Bundle initial (première charge) | 1.8 Mo | 2.4 Mo shell + lazy | **+33%** |
| Incidents cross-squad (MF down) | N/A | 2/mois (isolés) | Isolés |
| Temps d'onboarding nouvelle squad | 2 semaines | 3 jours | **-75%** |

### Écueils Rencontrés et Solutions

**Conflit de versions de dépendances partagées** : la squad Formation avait mis à jour `date-fns` en v3 alors que les autres utilisaient v2. Les deux versions ont été chargées simultanément, augmentant le bundle de 180 Ko. Solution : politique de gouvernance des dépendances partagées documentée dans un ADR, avec une PR de mise à jour coordonnée mensuelle.

**Overhead de bundle** : le `remoteEntry.js` de chaque MF ajoute 15-25 Ko de runtime Module Federation. Sur 6 MFs, le surcoût est de ~120 Ko — acceptable compte tenu du gain en déploiement indépendant.

**Tests d'intégration cross-MF** : les tests unitaires par MF sont simples, mais les parcours utilisateurs traversant plusieurs MFs (ex: créer un congé dans mf-congés et voir l'impact dans mf-paie) nécessitent une infrastructure de tests E2E avec tous les MFs démarrés simultanément. Playwright avec `docker-compose` pour les 6 MFs a résolu ce problème au prix d'un pipeline E2E de 18 minutes.

### Leçon Principale

Module Federation est un outil organisationnel autant que technique. Il résout le problème de déploiement indépendant entre équipes, mais introduit une complexité opérationnelle significative (versioning, tests cross-MF, observabilité distribuée). Le critère de décision principal n'est pas la taille de l'application mais la taille de l'équipe : en dessous de 3 squads autonomes, une monorepo bien organisée avec Nx ou Turborepo apporte les mêmes bénéfices organisationnels sans la complexité de Module Federation.
