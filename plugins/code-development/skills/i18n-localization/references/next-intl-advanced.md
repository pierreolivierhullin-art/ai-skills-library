# next-intl Avancé — Type-Safety, SSR/RSC et Routing par Locale

## Overview

Référence approfondie sur next-intl en mode avancé. Couvre la type-safety complète avec TypeScript strict, les formats personnalisés, les messages imbriqués et namespaces, la gestion SSR/RSC sans hydration mismatch, le routing par locale, les métadonnées i18n et les stratégies de cache. Appliquer ces patterns pour une internationalisation robuste, typée et performante dans une application Next.js App Router.

---

## Type-Safety Complète avec TypeScript Strict

### Générer les types à partir des messages

next-intl supporte la génération automatique des types TypeScript à partir des fichiers de messages. Configurer le fichier `i18n.ts` pour activer le typage strict des clés de traduction.

```typescript
// i18n.ts
import { getRequestConfig } from 'next-intl/server';
import { notFound } from 'next/navigation';

export const locales = ['fr', 'en', 'es', 'ar', 'de', 'ja'] as const;
export type Locale = (typeof locales)[number];

// Définir les types de messages — pointe vers la locale de référence (fr)
// next-intl inférera les types de toutes les clés disponibles
export default getRequestConfig(async ({ locale }) => {
  if (!locales.includes(locale as Locale)) notFound();

  return {
    messages: (await import(`./messages/${locale}.json`)).default,
  };
});
```

```typescript
// Créer global.d.ts à la racine du projet
// next-intl lit ce fichier pour le typage des clés de traduction
import fr from './messages/fr.json';

declare module 'next-intl' {
  interface AppConfig {
    // La locale de référence définit les types disponibles
    Messages: typeof fr;
    // Optionnel : restreindre les locales acceptées
    Locale: 'fr' | 'en' | 'es' | 'ar' | 'de' | 'ja';
  }
}
```

### Autocomplete et vérification à la compilation

Avec le typage activé, TypeScript détecte les clés manquantes et propose l'autocomplétion.

```typescript
// Composant avec typage strict — les erreurs apparaissent à la compilation
import { useTranslations } from 'next-intl';

function BoutonPaiement() {
  const t = useTranslations('checkout');

  return (
    <div>
      {/* ✅ Autocomplétion : TypeScript propose checkout.submit, checkout.cancel, etc. */}
      <button>{t('submit')}</button>

      {/* ❌ Erreur TypeScript : 'checkout.inexistant' n'existe pas dans messages/fr.json */}
      {/* <button>{t('inexistant')}</button> */}

      {/* ✅ Typage des variables interpolées */}
      {/* TypeScript sait que 'greeting' attend { nom: string } */}
      <p>{t('greeting', { nom: 'Alice' })}</p>
    </div>
  );
}
```

### generateStaticParams pour les locales

Utiliser `generateStaticParams` pour pré-générer toutes les routes par locale au moment du build.

```typescript
// app/[locale]/layout.tsx
import { locales } from '@/i18n';
import type { Locale } from '@/i18n';

// Déclarer statiquement toutes les locales supportées
// Next.js pré-rendra une version de la page pour chaque locale
export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

// Typer strictement le paramètre locale
interface LocaleLayoutProps {
  children: React.ReactNode;
  params: { locale: Locale };
}

export default async function LocaleLayout({
  children,
  params: { locale },
}: LocaleLayoutProps) {
  return (
    <html lang={locale}>
      <body>{children}</body>
    </html>
  );
}
```

---

## Formats Personnalisés — Dates, Monnaies et Unités

### Définir des formats custom dans la configuration

Centraliser tous les formats dans `i18n.ts` pour garantir la cohérence à travers l'application.

```typescript
// i18n.ts — Formats centralisés
export default getRequestConfig(async ({ locale }) => {
  return {
    messages: (await import(`./messages/${locale}.json`)).default,

    formats: {
      dateTime: {
        // Format compact : "15 jan. 2025" (fr), "Jan 15, 2025" (en)
        short: {
          day: 'numeric',
          month: 'short',
          year: 'numeric',
        },
        // Format long avec jour de la semaine : "mardi 15 janvier 2025"
        long: {
          weekday: 'long',
          day: 'numeric',
          month: 'long',
          year: 'numeric',
        },
        // Heure seule : "14:30"
        time: {
          hour: '2-digit',
          minute: '2-digit',
        },
        // Date et heure : "15 jan. 2025 à 14:30"
        dateAndTime: {
          day: 'numeric',
          month: 'short',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        },
      },
      number: {
        // Monnaie EUR avec 2 décimales
        currency: {
          style: 'currency',
          currency: 'EUR',
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        },
        // Pourcentage avec 1 décimale : "42,5 %"
        percent: {
          style: 'percent',
          minimumFractionDigits: 1,
          maximumFractionDigits: 1,
        },
        // Nombre compact : "1,2 M" / "1.2M"
        compact: {
          notation: 'compact',
          compactDisplay: 'short',
        },
        // Unité — kilogrammes
        weight: {
          style: 'unit',
          unit: 'kilogram',
          unitDisplay: 'short',
        },
      },
    },
  };
});
```

### Utiliser les formats dans les composants

```typescript
// Server Component
import { getFormatter } from 'next-intl/server';

async function CarteFacture({ facture }: { facture: Facture }) {
  const format = await getFormatter();

  return (
    <div>
      {/* Utiliser les formats nommés définis dans i18n.ts */}
      <time>{format.dateTime(facture.date, 'long')}</time>
      <span>{format.number(facture.montantHT, 'currency')}</span>
      <span>{format.number(facture.tauxTVA, 'percent')}</span>

      {/* Format relatif — "il y a 3 jours" */}
      <span>{format.relativeTime(-3, 'day')}</span>
    </div>
  );
}

// Client Component
'use client';
import { useFormatter } from 'next-intl';

function PrixProduit({ prix, poids }: { prix: number; poids: number }) {
  const format = useFormatter();

  return (
    <div>
      <span className="prix">{format.number(prix, 'currency')}</span>
      <span className="poids">{format.number(poids, 'weight')}</span>
    </div>
  );
}
```

### richText — HTML dans les traductions

```json
// messages/fr.json
{
  "legal": {
    "cgu": "En cliquant, vous acceptez nos <lienCGU>Conditions d'utilisation</lienCGU> et notre <lienPrivacy>Politique de confidentialité</lienPrivacy>.",
    "alerte": "⚠️ <gras>Attention</gras> : cette action est <italique>irréversible</italique>."
  }
}
```

```typescript
// Utilisation de richText pour les composants React dans les traductions
import { useTranslations } from 'next-intl';

function TexteLegal() {
  const t = useTranslations('legal');

  return (
    <p>
      {t.rich('cgu', {
        lienCGU: (chunks) => (
          <a href="/cgu" className="underline text-blue-600">
            {chunks}
          </a>
        ),
        lienPrivacy: (chunks) => (
          <a href="/privacy" className="underline text-blue-600">
            {chunks}
          </a>
        ),
      })}
    </p>
  );
}
```

---

## Messages Imbriqués et Namespaces

### Structure de fichiers messages/

Organiser les traductions en namespaces logiques par domaine fonctionnel.

```
messages/
├── fr.json         — locale de référence (source of truth)
├── en.json
├── es.json
├── ar.json
└── de.json
```

```json
// messages/fr.json — Structure par namespace
{
  "commun": {
    "actions": {
      "enregistrer": "Enregistrer",
      "annuler": "Annuler",
      "supprimer": "Supprimer",
      "confirmer": "Confirmer"
    },
    "etats": {
      "chargement": "Chargement en cours...",
      "erreur": "Une erreur est survenue",
      "vide": "Aucun résultat"
    }
  },
  "navigation": {
    "tableau-de-bord": "Tableau de bord",
    "parametres": "Paramètres",
    "profil": "Mon profil",
    "deconnexion": "Se déconnecter"
  },
  "tableau-de-bord": {
    "titre": "Tableau de bord",
    "metrics": {
      "utilisateurs": "{count, plural, =0 {Aucun utilisateur} =1 {1 utilisateur} other {# utilisateurs}}",
      "revenus": "Revenus : {montant, number, currency}",
      "croissance": "Croissance : {taux, number, percent}"
    },
    "widget": {
      "recent": "Activité récente",
      "voir-tout": "Voir tout"
    }
  },
  "erreurs": {
    "404": "Page introuvable",
    "403": "Accès refusé",
    "500": "Erreur serveur — réessayez dans quelques instants",
    "reseau": "Vérifiez votre connexion internet"
  }
}
```

### Accéder aux namespaces imbriqués

```typescript
// Accéder à un namespace précis via useTranslations
import { useTranslations } from 'next-intl';

function BoutonsSauvegarder() {
  // Namespace 'commun.actions' — accès direct aux sous-clés
  const t = useTranslations('commun.actions');

  return (
    <div>
      <button>{t('enregistrer')}</button>  {/* "Enregistrer" */}
      <button>{t('annuler')}</button>       {/* "Annuler" */}
    </div>
  );
}

function MetriquesDashboard({ stats }: { stats: Stats }) {
  // Namespace 'tableau-de-bord.metrics'
  const t = useTranslations('tableau-de-bord.metrics');

  return (
    <div>
      <p>{t('utilisateurs', { count: stats.nbUsers })}</p>
      <p>{t('revenus', { montant: stats.revenusMensuels })}</p>
      <p>{t('croissance', { taux: stats.tauxCroissance })}</p>
    </div>
  );
}
```

### Lazy loading de namespaces

Dans les grandes applications, éviter de charger tous les messages d'un coup. Configurer next-intl pour ne charger que les messages du namespace courant.

```typescript
// app/[locale]/tableau-de-bord/page.tsx
import { getTranslations, unstable_setRequestLocale } from 'next-intl/server';

// Pré-charger uniquement le namespace nécessaire pour cette page
export async function generateMetadata({
  params: { locale },
}: {
  params: { locale: string };
}) {
  const t = await getTranslations({ locale, namespace: 'tableau-de-bord' });
  return { title: t('titre') };
}

export default async function PageTableauDeBord({
  params: { locale },
}: {
  params: { locale: string };
}) {
  unstable_setRequestLocale(locale);
  const t = await getTranslations('tableau-de-bord');

  return (
    <main>
      <h1>{t('titre')}</h1>
    </main>
  );
}
```

---

## SSR/RSC — Éviter les Hydration Mismatches

### Sources courantes de mismatch

Les hydration mismatches surviennent quand le HTML rendu côté serveur diffère du DOM produit côté client. En i18n, les sources principales sont :

| Source | Problème | Solution |
|---|---|---|
| `new Date()` côté client | La date change entre le rendu serveur et client | Utiliser `useNow()` |
| `Intl.DateTimeFormat` avec timezone implicite | Le serveur (UTC) et le navigateur ont des timezones différentes | Utiliser `useTimeZone()` |
| `navigator.language` | Pas disponible côté serveur | Utiliser `useLocale()` uniquement côté client |
| Locale détectée dynamiquement | Différence entre la locale serveur et la locale client | Passer la locale via le layout |

### useNow() — Date stable sans mismatch

```typescript
// ❌ Mauvais — provoque un hydration mismatch
'use client';
function DateActuelle() {
  // new Date() côté serveur ≠ new Date() côté client (quelques ms d'écart)
  const maintenant = new Date();
  return <span>{maintenant.toLocaleDateString()}</span>;
}

// ✅ Correct — useNow() utilise la même valeur côté serveur et client
'use client';
import { useNow, useFormatter } from 'next-intl';

function DateActuelle() {
  // next-intl synchronise la valeur entre serveur et client
  const maintenant = useNow({ updateInterval: 1000 * 60 }); // rafraîchi chaque minute
  const format = useFormatter();

  return <time>{format.dateTime(maintenant, 'long')}</time>;
}
```

### useTimeZone() — Timezone cohérente

```typescript
'use client';
import { useTimeZone, useFormatter } from 'next-intl';

function HeureLocale({ dateUTC }: { dateUTC: Date }) {
  // Récupère la timezone configurée dans i18n.ts (ou défaut UTC)
  const timezone = useTimeZone();
  const format = useFormatter();

  return (
    <time title={`Timezone : ${timezone}`}>
      {format.dateTime(dateUTC, {
        timeZone: timezone,
        hour: '2-digit',
        minute: '2-digit',
      })}
    </time>
  );
}

// Configurer la timezone dans i18n.ts pour éviter les mismatches
export default getRequestConfig(async ({ locale }) => {
  return {
    messages: (await import(`./messages/${locale}.json`)).default,
    // Timezone fixe ou déterminée côté serveur uniquement
    timeZone: 'Europe/Paris',
  };
});
```

### Patterns React Server Components vs Client Components

```typescript
// ✅ Server Component — utiliser les fonctions server de next-intl
import { getTranslations, getFormatter } from 'next-intl/server';

async function CarteProduitServeur({ produit }: { produit: Produit }) {
  const t = await getTranslations('produits');
  const format = await getFormatter();

  return (
    <article>
      <h2>{t('titre', { nom: produit.nom })}</h2>
      <p>{format.number(produit.prix, 'currency')}</p>
      <time>{format.dateTime(produit.dateAjout, 'short')}</time>
    </article>
  );
}

// ✅ Client Component — utiliser les hooks
'use client';
import { useTranslations, useFormatter } from 'next-intl';

function FiltreInteractif({ onFiltre }: { onFiltre: (val: string) => void }) {
  const t = useTranslations('filtres');
  const format = useFormatter();

  return (
    <div>
      <label>{t('titre')}</label>
      <button onClick={() => onFiltre('asc')}>{t('tri.croissant')}</button>
      <button onClick={() => onFiltre('desc')}>{t('tri.decroissant')}</button>
    </div>
  );
}
```

---

## next-intl Routing Avancé

### localizeHref — Liens i18n typés

```typescript
// Utiliser localizeHref pour construire des URLs avec locale préfixée
import { Link } from '@/navigation'; // navigation.ts généré par createLocalizedPathnamesNavigation

// navigation.ts — Configuration centrale du routing i18n
import { createLocalizedPathnamesNavigation } from 'next-intl/navigation';
import { locales } from './i18n';

// Chemins localisés par locale — slug différent selon la langue
export const { Link, redirect, usePathname, useRouter } =
  createLocalizedPathnamesNavigation({
    locales,
    pathnames: {
      '/': '/',
      '/tableau-de-bord': {
        fr: '/tableau-de-bord',
        en: '/dashboard',
        es: '/panel',
        ar: '/لوحة-التحكم',
        de: '/ubersicht',
        ja: '/ダッシュボード',
      },
      '/produits/[slug]': {
        fr: '/produits/[slug]',
        en: '/products/[slug]',
        es: '/productos/[slug]',
        ar: '/منتجات/[slug]',
        de: '/produkte/[slug]',
        ja: '/製品/[slug]',
      },
      '/contact': {
        fr: '/contact',
        en: '/contact',
        es: '/contacto',
        ar: '/اتصل-بنا',
        de: '/kontakt',
        ja: '/お問い合わせ',
      },
    },
  } as const);
```

```typescript
// Utilisation du composant Link localisé
import { Link, useRouter } from '@/navigation';
import { useLocale } from 'next-intl';

function MenuNavigation() {
  const locale = useLocale();
  const router = useRouter();

  const changerLocale = (nouvelleLocale: string) => {
    // Redirige vers la même route dans la nouvelle locale
    router.replace('/tableau-de-bord', { locale: nouvelleLocale });
  };

  return (
    <nav>
      {/* Link gère automatiquement le préfixe de locale et le chemin localisé */}
      <Link href="/tableau-de-bord">Tableau de bord</Link>
      <Link href={{ pathname: '/produits/[slug]', params: { slug: 'widget-pro' } }}>
        Widget Pro
      </Link>

      {/* Sélecteur de locale */}
      <select value={locale} onChange={(e) => changerLocale(e.target.value)}>
        <option value="fr">Français</option>
        <option value="en">English</option>
        <option value="es">Español</option>
        <option value="ar">العربية</option>
      </select>
    </nav>
  );
}
```

### Middleware Edge — Détection et Redirection

```typescript
// middleware.ts — Configuration avancée du middleware
import createMiddleware from 'next-intl/middleware';
import { NextRequest, NextResponse } from 'next/server';

// Middleware next-intl de base
const intlMiddleware = createMiddleware({
  locales: ['fr', 'en', 'es', 'ar', 'de', 'ja'],
  defaultLocale: 'fr',
  // 'as-needed' : /fr/ omis pour la locale par défaut, /en/... pour les autres
  localePrefix: 'as-needed',
  // Lire Accept-Language uniquement si pas de cookie
  localeDetection: true,
  // Fichier pathnames pour les chemins localisés
  pathnames: {
    '/tableau-de-bord': {
      fr: '/tableau-de-bord',
      en: '/dashboard',
    },
  },
});

export function middleware(request: NextRequest) {
  // Exclure les routes API et les fichiers statiques
  const pathname = request.nextUrl.pathname;

  // Logique de fallback personnalisée avant de déléguer à next-intl
  if (pathname.startsWith('/api/')) {
    return NextResponse.next();
  }

  return intlMiddleware(request);
}

export const config = {
  // Matcher : toutes les routes sauf _next, assets statiques et API
  matcher: ['/((?!_next|_vercel|.*\\..*).*)'],
};
```

---

## Metadata i18n — SEO et hreflang

### generateMetadata avec traductions

```typescript
// app/[locale]/page.tsx
import { getTranslations } from 'next-intl/server';
import { locales } from '@/i18n';
import type { Metadata } from 'next';

interface PageProps {
  params: { locale: string };
}

// Générer les métadonnées SEO avec traductions et hreflang
export async function generateMetadata({
  params: { locale },
}: PageProps): Promise<Metadata> {
  const t = await getTranslations({ locale, namespace: 'meta' });
  const baseUrl = 'https://monapp.com';

  return {
    title: t('titre'),
    description: t('description'),
    alternates: {
      // hreflang pour chaque locale supportée
      languages: Object.fromEntries(
        locales.map((loc) => [
          loc,
          `${baseUrl}/${loc === 'fr' ? '' : loc}`,
        ])
      ),
      canonical: `${baseUrl}/${locale === 'fr' ? '' : locale}`,
    },
    openGraph: {
      title: t('og.titre'),
      description: t('og.description'),
      locale: locale,
      // Toutes les locales alternatives pour og:locale:alternate
      alternateLocale: locales.filter((l) => l !== locale),
    },
  };
}
```

```json
// messages/fr.json — namespace meta
{
  "meta": {
    "titre": "MonApp — La solution tout-en-un",
    "description": "Gérez votre activité efficacement avec MonApp. Essai gratuit 30 jours.",
    "og": {
      "titre": "MonApp — La solution tout-en-un",
      "description": "Gérez votre activité efficacement avec MonApp."
    }
  }
}
```

---

## Stratégies de Cache par Locale

### revalidation avec generateStaticParams

```typescript
// app/[locale]/produits/[slug]/page.tsx
import { locales } from '@/i18n';

// Pré-générer toutes les combinaisons locale × slug
export async function generateStaticParams() {
  const produits = await getProduits();

  return locales.flatMap((locale) =>
    produits.map((produit) => ({
      locale,
      slug: produit.slug,
    }))
  );
}

// Revalidation ISR par locale — 1 heure
export const revalidate = 3600;
```

### Cache par locale avec Next.js fetch

```typescript
// Inclure la locale dans la cache key
async function getTraductions(locale: string) {
  const res = await fetch(`https://cdn.traductions.io/api/${locale}/messages.json`, {
    next: {
      // Revalider les traductions toutes les 24h
      revalidate: 86400,
      // Tag pour l'invalidation manuelle : revalidateTag('traductions-fr')
      tags: [`traductions-${locale}`],
    },
  });
  return res.json();
}
```

---

## Tests avec NextIntlClientProvider

### Configurer le provider dans les tests

```typescript
// test/utils/i18n-wrapper.tsx
import { NextIntlClientProvider } from 'next-intl';
import fr from '@/messages/fr.json';
import en from '@/messages/en.json';

const messages = { fr, en } as const;

export function creerWrapperI18n(locale: 'fr' | 'en' = 'fr') {
  return function WrapperI18n({ children }: { children: React.ReactNode }) {
    return (
      <NextIntlClientProvider locale={locale} messages={messages[locale]}>
        {children}
      </NextIntlClientProvider>
    );
  };
}

// Utilitaire pour le rendu avec locale
export function renderAvecLocale(
  ui: React.ReactElement,
  locale: 'fr' | 'en' = 'fr'
) {
  return render(ui, { wrapper: creerWrapperI18n(locale) });
}
```

```typescript
// __tests__/BoutonSauvegarder.test.tsx
import { screen } from '@testing-library/react';
import { renderAvecLocale } from '@/test/utils/i18n-wrapper';
import BoutonSauvegarder from '@/components/BoutonSauvegarder';

describe('BoutonSauvegarder', () => {
  it('affiche le texte en français', () => {
    renderAvecLocale(<BoutonSauvegarder />, 'fr');
    expect(screen.getByRole('button')).toHaveTextContent('Enregistrer');
  });

  it('affiche le texte en anglais', () => {
    renderAvecLocale(<BoutonSauvegarder />, 'en');
    expect(screen.getByRole('button')).toHaveTextContent('Save');
  });
});
```

### Snapshots par locale

```typescript
// __tests__/CarteProduit.snapshot.test.tsx
import { renderAvecLocale } from '@/test/utils/i18n-wrapper';

const produitTest = {
  nom: 'Widget Pro',
  prix: 49.99,
  dateAjout: new Date('2025-01-15T10:00:00Z'),
};

describe('CarteProduit — snapshots i18n', () => {
  const locales = ['fr', 'en', 'es'] as const;

  locales.forEach((locale) => {
    it(`snapshot correct pour locale ${locale}`, () => {
      const { container } = renderAvecLocale(
        <CarteProduit produit={produitTest} />,
        locale
      );
      expect(container).toMatchSnapshot();
    });
  });
});
```

---

## next-i18n-router vs next-intl — Tableau de Décision

| Critère | next-intl | next-i18n-router |
|---|---|---|
| **App Router natif** | Oui — conçu pour l'App Router | Partiel — wrapper du routing Next.js |
| **Type-safety** | Complète (types inférés des messages) | Non |
| **Server Components** | Natif (getTranslations, getFormatter) | Non — client-side seulement |
| **Routing localisé** | Oui (pathnames localisés par locale) | Basique (préfixe de locale seulement) |
| **Formats personnalisés** | Oui (formats centralisés dans i18n.ts) | Non |
| **richText** | Oui | Non |
| **Taille du bundle** | ~12 KB client | ~4 KB client |
| **Maturité** | Élevée (v3+, maintenu activement) | Faible (moins de contributions) |
| **Quand utiliser** | Toujours pour les nouveaux projets Next.js App Router | Jamais — préférer next-intl |

**Recommandation** : utiliser next-intl pour tout nouveau projet Next.js App Router. next-i18n-router ne présente aucun avantage significatif et manque des fonctionnalités clés de next-intl.
