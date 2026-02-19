---
name: i18n-localization
version: 1.0.0
description: >
  Internationalization i18n localization l10n React Next.js applications,
  i18next react-i18next next-intl configuration namespaces interpolation,
  ICU message format plurals gender ordinals,
  RTL right-to-left Arabic Hebrew bidirectional text CSS logical properties,
  locale detection language negotiation Accept-Language,
  date time number currency formatting Intl API,
  translation management Crowdin Phrase Lokalise CAT tools,
  locale-first architecture SSR hydration mismatch,
  pseudo-localization testing i18n CI pipeline
---

# Internationalisation (i18n) — Localisation Multilingue d'Applications

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu dois prendre en charge plusieurs langues dans une application React/Next.js
- Tu configures i18next, next-intl, ou react-intl pour la première fois
- Tu as des problèmes de pluriel, genre grammatical, ou formats de nombres/dates
- Tu dois supporter une langue RTL (arabe, hébreu, persan)
- Tu veux mettre en place un workflow de traduction avec une équipe ou des traducteurs
- Tu dois tester l'i18n automatiquement en CI

---

## next-intl — i18n pour Next.js App Router

```
apps/web/
├── messages/
│   ├── fr.json
│   ├── en.json
│   └── ar.json
├── i18n.ts
├── middleware.ts
└── app/
    └── [locale]/
        ├── layout.tsx
        └── page.tsx
```

```typescript
// i18n.ts — Configuration de la bibliothèque
import { getRequestConfig } from 'next-intl/server';
import { notFound } from 'next/navigation';

export const locales = ['fr', 'en', 'es', 'ar'] as const;
export type Locale = (typeof locales)[number];

export default getRequestConfig(async ({ locale }) => {
  // Valider que le locale demandé est supporté
  if (!locales.includes(locale as Locale)) notFound();

  return {
    messages: (await import(`./messages/${locale}.json`)).default,
    // Format par défaut pour les dates et nombres
    formats: {
      dateTime: {
        short: { day: 'numeric', month: 'short', year: 'numeric' },
        long: { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' },
      },
      number: {
        currency: { style: 'currency', minimumFractionDigits: 2 },
        percent: { style: 'percent', maximumFractionDigits: 1 },
      },
    },
  };
});
```

```typescript
// middleware.ts — Détection et redirection automatique
import createMiddleware from 'next-intl/middleware';

export default createMiddleware({
  locales: ['fr', 'en', 'es', 'ar'],
  defaultLocale: 'fr',
  localeDetection: true,      // Lit Accept-Language header
  localePrefix: 'as-needed',  // /fr/ seulement si pas défaut
});

export const config = {
  matcher: ['/((?!api|_next|_vercel|.*\\..*).*)'],
};
```

```typescript
// app/[locale]/layout.tsx
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';

export default async function LocaleLayout({
  children,
  params: { locale },
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  const messages = await getMessages();

  return (
    <html lang={locale} dir={locale === 'ar' ? 'rtl' : 'ltr'}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

---

## Format des Messages — ICU Message Format

```json
// messages/fr.json
{
  "common": {
    "save": "Enregistrer",
    "cancel": "Annuler",
    "loading": "Chargement en cours..."
  },
  "user": {
    "greeting": "Bonjour, {nom} !",
    "lastSeen": "Dernière connexion : {date, date, long}",
    "balance": "Solde : {montant, number, currency}"
  },
  "notifications": {
    "count": "{count, plural,\n  =0 {Aucune notification}\n  =1 {1 notification non lue}\n  other {# notifications non lues}\n}",
    "newFollowers": "{count, plural,\n  =1 {{name} vous suit maintenant}\n  other {{name} et {count, number} autres vous suivent}\n}"
  },
  "invoice": {
    "status": "{statut, select,\n  brouillon {Brouillon}\n  envoyé {Envoyé}\n  payé {Payé}\n  annulé {Annulé}\n  other {Statut inconnu}\n}"
  }
}
```

```typescript
// Utilisation dans les composants Server et Client
import { useTranslations, useFormatter } from 'next-intl';

// Composant Server Component
import { getTranslations, getFormatter } from 'next-intl/server';

async function PageFacture({ params }: { params: { id: string } }) {
  const t = await getTranslations('notifications');
  const format = await getFormatter();

  const facture = await getFacture(params.id);

  return (
    <div>
      <h1>{t('count', { count: facture.nb_articles })}</h1>
      <p>{format.dateTime(facture.date, 'long')}</p>
      <p>{format.number(facture.total, 'currency')}</p>
    </div>
  );
}

// Composant Client Component
'use client';
function BoutonSauvegarder() {
  const t = useTranslations('common');
  return <button>{t('save')}</button>;
}
```

---

## i18next + React — Pour les SPA et Vite

```typescript
// src/i18n/config.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import Backend from 'i18next-http-backend';

i18n
  .use(Backend)          // Chargement asynchrone des fichiers de traduction
  .use(LanguageDetector) // Détection automatique depuis navigator.language
  .use(initReactI18next)
  .init({
    fallbackLng: 'fr',
    supportedLngs: ['fr', 'en', 'es', 'ar'],
    defaultNS: 'common',
    ns: ['common', 'user', 'dashboard', 'errors'],

    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },

    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage'],
    },

    interpolation: {
      escapeValue: false,   // React échappe déjà les valeurs
    },

    // Pluralisation avancée avec ICU
    // i18next-icu pour le format ICU message complet
  });

export default i18n;
```

```typescript
// Utilisation avec hooks
import { useTranslation, Trans } from 'react-i18next';

function PageProfil({ user }: { user: User }) {
  const { t, i18n } = useTranslation('user');

  const changerLangue = (langue: string) => {
    i18n.changeLanguage(langue);
  };

  return (
    <div>
      {/* Interpolation simple */}
      <h1>{t('greeting', { nom: user.prénom })}</h1>

      {/* Pluralisation */}
      <p>{t('notifications.count', { count: user.nbNotifs })}</p>

      {/* Composant Trans pour du HTML dans les traductions */}
      <Trans
        i18nKey="accepterCGU"
        components={{
          lien: <a href="/cgu" className="underline" />,
          gras: <strong />,
        }}
      />
      {/* messages/fr.json: "accepterCGU": "J'accepte les <lien>CGU</lien> et la <gras>politique de confidentialité</gras>" */}
    </div>
  );
}
```

---

## Formatage des Dates, Nombres et Devises

```typescript
// Utiliser l'API Intl native — toujours préférer à moment.js / date-fns pour l'i18n
function formatage(locale: string) {
  // Dates — sensible à la locale
  const formatterDate = new Intl.DateTimeFormat(locale, {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
  // fr: "15 janvier 2025" | en: "January 15, 2025" | ar: "١٥ يناير ٢٠٢٥"
  console.log(formatterDate.format(new Date('2025-01-15')));

  // Monnaies
  const formatterEUR = new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: 'EUR',
    minimumFractionDigits: 2,
  });
  // fr: "1 234,56 €" | en-US: "€1,234.56" | ar: "١٬٢٣٤٫٥٦ €"
  console.log(formatterEUR.format(1234.56));

  // Nombres relatifs
  const formatterRelatif = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });
  // fr: "il y a 3 jours" | en: "3 days ago"
  console.log(formatterRelatif.format(-3, 'day'));
}
```

---

## RTL — Langues de Droite à Gauche

```css
/* Utiliser les propriétés logiques CSS — s'adaptent automatiquement au sens */
.card {
  /* ✅ Logique (s'adapte à RTL/LTR) */
  padding-inline: 1rem;      /* = padding-left + padding-right */
  margin-inline-start: 1rem; /* = margin-left en LTR, margin-right en RTL */
  border-inline-end: 1px solid;

  /* ❌ Physique (ne s'adapte pas) */
  /* padding-left: 1rem; */
  /* margin-left: 1rem; */
}

/* Flex et Grid — déjà RTL-aware */
.navigation {
  display: flex;
  gap: 1rem;
  /* ✅ L'ordre s'inverse automatiquement en dir="rtl" */
}

/* Icônes directionnelles — à retourner en RTL */
.icone-fleche {
  transform: scaleX(1);
}
[dir='rtl'] .icone-fleche {
  transform: scaleX(-1);
}
```

```typescript
// Détecter si une locale est RTL
const LOCALES_RTL = new Set(['ar', 'he', 'fa', 'ur']);

function estRTL(locale: string): boolean {
  return LOCALES_RTL.has(locale);
}

// Dans le layout
<html lang={locale} dir={estRTL(locale) ? 'rtl' : 'ltr'}>
```

---

## Pseudo-Localisation — Tester l'i18n en CI

```typescript
// Générer du pseudo-texte pour détecter les problèmes d'affichage
// Objectifs :
// - Détecter les textes codés en dur (hardcoded strings)
// - Vérifier que l'UI gère les textes plus longs (langues latines ~30% plus longues que l'anglais)
// - Tester la gestion des caractères spéciaux

function pseudoLocaliser(texte: string): string {
  const accents: Record<string, string> = {
    a: 'á', e: 'é', i: 'í', o: 'ó', u: 'ú',
    A: 'Á', E: 'É', I: 'Í', O: 'Ó', U: 'Ú',
  };

  const transformé = texte
    .split('')
    .map(c => accents[c] ?? c)
    .join('');

  // Ajouter du padding pour simuler les langues plus longues
  const padding = 'xxx';
  return `[${padding} ${transformé} ${padding}]`;
}

// "Save" → "[xxx Sávé xxx]"
// Textes non-traduits restent identiques → facile à repérer
```

---

## Workflow de Traduction avec Crowdin

```yaml
# crowdin.yml — Synchronisation automatique
files:
  - source: /messages/en.json
    translation: /messages/%locale%.json
    type: i18next_multilingual
    update_option: update_as_unapproved

# GitHub Actions — Soumettre les nouvelles clés
- name: Push sources to Crowdin
  uses: crowdin/github-action@v1
  with:
    upload_sources: true
    download_translations: false
    crowdin_branch_name: main
  env:
    CROWDIN_PROJECT_ID: ${{ secrets.CROWDIN_PROJECT_ID }}
    CROWDIN_PERSONAL_TOKEN: ${{ secrets.CROWDIN_TOKEN }}

# Après validation des traductions
- name: Download translations from Crowdin
  uses: crowdin/github-action@v1
  with:
    upload_sources: false
    download_translations: true
    create_pull_request: true
    pull_request_title: 'feat: update translations'
```

---

## Références

- `references/next-intl-advanced.md` — next-intl configuration avancée (type-safety, formats personnalisés, messages imbriqués, SSR/RSC hydration), next-i18n-router, routing par locale
- `references/icu-plurals.md` — ICU message format complet (plurals par règle CLDR, ordinaux, sélect, nested), i18next-icu, Fluent (Mozilla), gestion des genres grammaticaux
- `references/rtl-locales.md` — CSS logique complet, Tailwind RTL, tests Playwright RTL, polices arabes/hébraïques, chiffres arabes-indiens, bidi algorithm
- `references/case-studies.md` — 4 cas : migration vers next-intl dans un monorepo, RTL arabe ajouté en 2 semaines, workflow Crowdin CI/CD, détection des hardcoded strings automatisée
