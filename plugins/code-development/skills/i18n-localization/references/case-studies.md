# Case Studies — 4 Projets i18n en Production

## Cas 1 — Migration vers next-intl dans un monorepo Next.js 14

### Contexte

FlowDesk, éditeur SaaS B2B de gestion de projets et de collaboration d'équipes, a construit une plateforme utilisée par 8 000 entreprises dans 12 pays. L'architecture repose sur un monorepo Turborepo hébergeant 3 applications Next.js distinctes : `app-web` (interface principale pour les utilisateurs), `app-admin` (back-office interne), et `app-onboarding` (tunnel d'inscription et d'activation). Les 3 applications partagent un package `@flowdesk/ui` (composants Radix + Tailwind) et un package `@flowdesk/api-client` (client tRPC). L'équipe technique compte 22 développeurs front-end répartis en 4 squads produit, plus 2 développeurs dédiés à l'infrastructure frontend.

FlowDesk supporte 12 langues : français (défaut), anglais, espagnol, allemand, portugais, néerlandais, italien, polonais, tchèque, suédois, japonais et coréen. La base de traductions contient 4 200 clés réparties en 18 namespaces. Les traductions sont gérées sur Phrase (anciennement Phraseapp) par une équipe de 6 traducteurs externes.

### Problème

L'internationalisation repose sur react-i18next configuré uniquement côté client, hérité d'une époque où les 3 applications étaient des SPA classiques (Create React App). La migration vers Next.js App Router 2 ans plus tôt a été faite en mode "pages router" pour éviter de tout réécrire, puis progressivement vers l'App Router sans refonte de la couche i18n. Les conséquences techniques sont sévères :

**Hydration mismatches** : 15 à 30 erreurs par jour remontées dans Sentry, principalement sur les pages avec des dates formatées (tableaux de bord) et des nombres (factures, rapports financiers). Les erreurs provoquent un flash de contenu non traduit au chargement initial avant que React ne réhydrate le DOM.

**Aucune type-safety** : Les clés de traduction sont des strings non typées. Un développeur peut appeler `t('dashboard.metrics.users')` alors que la clé s'appelle `t('dashboard.metrics.utilisateurs')` — l'erreur n'est détectée qu'en production quand la chaîne de traduction manquante est rendue littéralement. Le nombre de clés manquantes en production oscillait entre 3 et 8 par semaine.

**Pas de SSR** : Toutes les traductions sont chargées côté client, ce qui entraîne un rendu initial sans contenu traduit. Sur la page produit (SEO-critique), le Largest Contentful Paint est pénalisé de 200 à 350ms par rapport à un rendu serveur.

**Namespaces fragmentés** : Chaque namespace est un fichier JSON séparé chargé à la demande par i18next. Les collisions de nommage entre les 3 applications sont fréquentes (même clé, traduction différente), et la duplication de certaines clés communes est estimée à 340 clés (~8%).

### Solution

La migration vers next-intl a été planifiée sur 12 semaines, avec un objectif de 0 hydration mismatch, 100% de type-safety sur les clés de traduction, et un LCP amélioré d'au moins 150ms sur les pages produit.

**Architecture cible** : Créer un package partagé `@flowdesk/i18n` dans le monorepo Turborepo, contenant les fichiers `messages/` communs aux 3 applications, la configuration next-intl partagée (`i18n.ts`), les types TypeScript générés, et les scripts de validation des traductions.

**Formats personnalisés centralisés** : Définir une fois dans `@flowdesk/i18n/config.ts` les formats de dates, nombres et devises utilisés dans les 3 applications — éviter les divergences de rendu entre `app-web` et `app-onboarding`.

**generateStaticParams** : Ajouter `generateStaticParams` dans le layout de chaque application pour pré-rendre les routes statiques dans les 12 locales au build time. Les pages produit (SEO-critiques) passent de rendu à la demande à statique généré.

### Processus de migration

**Phase 1 — Infrastructure (semaines 1-2)** : Créer le package `@flowdesk/i18n`. Consolider les 3 sets de fichiers de traduction en un set unique dans `packages/i18n/messages/`, en résolvant les 340 doublons par une revue manuelle. Configurer next-intl dans `app-web` uniquement, sur une seule route pilote (`/tableau-de-bord`). Valider que les hydration mismatches disparaissent sur cette route.

**Phase 2 — Migration progressive route par route (semaines 3-8)** : Migrer les routes de `app-web` par ordre de priorité (trafic décroissant). Pour chaque route, la démarche est : remplacer `useTranslation()` par `useTranslations()`, remplacer les fonctions `getServerSideProps` par des Server Components, ajouter les namespaces dans `generateMetadata`. Un script de codemods AST automatise 70% de la migration mécanique.

**Phase 3 — app-admin et app-onboarding (semaines 9-11)** : Répliquer la migration sur les 2 autres applications. Les 2 applications bénéficient du retour d'expérience de app-web et migrent plus vite.

**Phase 4 — Validation et type-safety (semaine 12)** : Activer le typage strict TypeScript global via le fichier `global.d.ts`. Corriger les 47 erreurs de compilation révélées par le typage (clés inexistantes, variables ICU incorrectes). Intégrer le script de validation des traductions dans la CI GitHub Actions.

```typescript
// packages/i18n/src/config.ts — Configuration partagée entre les 3 apps
import { getRequestConfig } from 'next-intl/server';

export const locales = [
  'fr', 'en', 'es', 'de', 'pt', 'nl', 'it', 'pl', 'cs', 'sv', 'ja', 'ko'
] as const;

export type Locale = (typeof locales)[number];

export default getRequestConfig(async ({ locale }) => {
  if (!locales.includes(locale as Locale)) notFound();

  return {
    messages: (await import(`../messages/${locale}.json`)).default,
    formats: {
      dateTime: {
        short: { day: 'numeric', month: 'short', year: 'numeric' },
        long: { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' },
        time: { hour: '2-digit', minute: '2-digit' },
      },
      number: {
        currency: { style: 'currency', currency: 'EUR', minimumFractionDigits: 2 },
        percent: { style: 'percent', minimumFractionDigits: 1 },
        compact: { notation: 'compact' },
      },
    },
  };
});
```

```bash
# Script de validation des clés — exécuté en CI
# Vérifie que toutes les clés de fr.json existent dans les 11 autres locales

#!/bin/bash
REFERENCE="packages/i18n/messages/fr.json"
ERREURS=0

for LOCALE in en es de pt nl it pl cs sv ja ko; do
  CIBLE="packages/i18n/messages/${LOCALE}.json"
  MANQUANTES=$(node scripts/compare-keys.js "$REFERENCE" "$CIBLE")
  COUNT=$(echo "$MANQUANTES" | grep -c "MANQUANT" || true)

  if [ "$COUNT" -gt 0 ]; then
    echo "❌ [${LOCALE}] ${COUNT} clé(s) manquante(s)"
    echo "$MANQUANTES"
    ERREURS=$((ERREURS + COUNT))
  fi
done

exit $ERREURS
```

### Résultats

- **0 hydration mismatch** : Aucune erreur Sentry liée à l'i18n depuis le déploiement de la phase 4. Le volume d'erreurs est passé de 20/jour à 0.
- **LCP -200ms** sur les pages produit grâce au SSR des traductions. Mesuré via un test A/B sur le déploiement progressif (30% du trafic sur la nouvelle version pendant 2 semaines).
- **100% type-safe** : Les 47 erreurs révélées par le typage strict ont toutes été corrigées. Aucune clé manquante en production depuis 4 mois.
- **Duplication éliminée** : Les 340 clés dupliquées ont été consolidées, réduisant la surface de maintenance de 8%.
- **Build time** : `generateStaticParams` sur 12 locales augmente le temps de build de 4 min 30 s à 7 min — acceptable, compensé par la suppression du SSR à la demande pour les pages statiques.

### Leçons apprises

La migration route par route avec un script de codemods automatise l'essentiel du travail mécanique, mais la consolidation des doublons de traductions est la partie la plus chronophage — prévoir 2 semaines de revue manuelle pour 340 clés. La phase pilote sur une seule route est indispensable : elle révèle les cas particuliers (dates, composants richText, namespaces partagés) avant de les rencontrer à l'échelle. La type-safety révèle systématiquement des bugs latents : les 47 erreurs TypeScript trouvées lors de la phase 4 auraient toutes été des bugs silencieux en production sans le typage strict.

---

## Cas 2 — Ajout du Support Arabe RTL en 2 Semaines

### Contexte

FormBuild, éditeur d'une application de création de formulaires en ligne, sert 500 000 utilisateurs dans 42 pays. L'application est une SPA React (Vite + React 18) avec react-i18next et supporte déjà 8 langues latines : anglais, français, espagnol, allemand, portugais, néerlandais, italien, et polonais. La base de code comprend 180 composants React, 12 000 lignes de CSS (Tailwind CSS v3.4), et environ 2 800 clés de traduction. Une analyse géographique du trafic révèle 100 000 utilisateurs arabophones potentiels dans les pays du Golfe, d'Égypte et du Maroc, actuellement non servis par une version arabe.

Le product manager fixe un objectif de 2 semaines pour livrer la version arabe en production, avec un impératif absolu de 0 régression sur les 8 langues existantes.

### Problème

L'audit initial de la base de code révèle l'ampleur du travail :

**1 847 propriétés CSS physiques** identifiées via grep dans les 180 composants : `margin-left`, `margin-right`, `padding-left`, `padding-right`, `border-left`, `border-right`, `text-align: left`, `text-align: right`, `left:`, `right:` dans les fichiers CSS et les classes Tailwind physiques (`ml-*`, `mr-*`, `pl-*`, `pr-*`, `text-left`, `text-right`, `border-l-*`, `border-r-*`).

**Icônes directionnelles non mirrorées** : 34 icônes identifiées (flèches, chevrons, boutons "suivant/précédent") qui doivent être inversées en RTL.

**Chiffres arabes-indiens** : L'application affiche des statistiques de formulaires (nombre de réponses, taux de complétion). Pour la locale `ar-SA`, Intl.NumberFormat retourne des chiffres arabes-indiens (٤٢٪) alors que le design ne prévoit que des chiffres latins.

**Police arabe absente** : La police Inter (utilisée pour les 8 langues latines) ne couvre pas le script arabe. Sans configuration explicite, les caractères arabes s'affichent en police système — rendu visuellement incohérent.

**Placeholders de formulaires** : Les 280 champs de formulaire ont des placeholders qui s'alignent à gauche sans règle CSS RTL — rendu cassé en arabe.

### Solution

La contrainte de 2 semaines impose une approche structurée et parallélisée entre 3 développeurs.

**Jour 1-2 — Audit automatisé et plan de migration** : Exécuter le script grep pour identifier toutes les propriétés physiques. Classer les 1 847 occurrences en 3 catégories : automatiquement migrables (1 402 — propriétés simples), nécessitant une revue manuelle (312 — propriétés dans des calculs ou conditions), et à traiter avec `rtl:` Tailwind (133 — icônes, gradients).

**Jour 3-7 — Migration CSS** : Écrire un script de codemod (jscodeshift) pour remplacer automatiquement les 1 402 propriétés Tailwind physiques par leurs équivalents logiques. Traiter manuellement les 312 cas complexes. Ajouter les classes `rtl:` pour les 133 cas spéciaux. Configurer la police Cairo pour l'arabe via next/font.

**Jour 8-10 — Intégration i18next-icu et traductions** : Configurer i18next avec i18next-icu pour le support ICU. Importer les 2 800 traductions arabes livrées par l'équipe de traduction (Phrase). Configurer `Intl.NumberFormat` avec `numberingSystem: 'latn'` pour les locales arabes (décision produit : conserver les chiffres latins pour la cohérence visuelle avec les autres locales).

**Jour 11-12 — Tests et QA** : Exécuter la suite Playwright de 180 tests de snapshot — comparer les rendus LTR et RTL, valider que les 8 locales existantes ne sont pas régressées. QA manuel par un locuteur natif arabe (contrat ponctuel avec une agence de localisation).

**Jour 13-14 — Déploiement progressif** : Déploiement à 5% du trafic arabe le jour 13, 50% le jour 14 après validation des métriques, 100% en fin de jour 14.

```bash
# Script d'audit des propriétés physiques Tailwind
grep -r --include="*.tsx" --include="*.jsx" --include="*.css" \
  -E '\b(ml|mr|pl|pr|text-left|text-right|border-l|border-r|left-|right-|rounded-l|rounded-r)\b' \
  src/ \
  | grep -v 'rtl:\|ltr:\|//\|/\*' \
  > audit-proprietes-physiques.txt

echo "Total propriétés physiques : $(wc -l < audit-proprietes-physiques.txt)"
```

```typescript
// Configuration Intl.NumberFormat pour l'arabe — chiffres latins forcés
function formaterNombreAr(valeur: number, options?: Intl.NumberFormatOptions): string {
  return new Intl.NumberFormat('ar', {
    ...options,
    // Forcer les chiffres latins (0-9) pour la cohérence visuelle
    numberingSystem: 'latn',
  } as Intl.NumberFormatOptions & { numberingSystem: string }).format(valeur);
}

// Alternative — utiliser la sous-locale ar-MA (Maroc) qui utilise les chiffres latins
const formatterArMA = new Intl.NumberFormat('ar-MA', {
  style: 'percent',
}).format(0.42);
// Résultat : "42 %" (chiffres latins, conformément à l'usage marocain)
```

```css
/* globals.css — Configuration RTL pour les formulaires */
[dir="rtl"] {
  /* Police arabe pour tous les éléments textuels */
  font-family: var(--font-cairo), 'Noto Sans Arabic', system-ui, sans-serif;
}

/* Placeholders des inputs — alignement RTL */
[dir="rtl"] input::placeholder,
[dir="rtl"] textarea::placeholder {
  text-align: right;
}

/* Champs email, URL, tel — toujours LTR même en RTL */
[dir="rtl"] input[type="email"],
[dir="rtl"] input[type="url"],
[dir="rtl"] input[type="tel"],
[dir="rtl"] input[type="number"] {
  direction: ltr;
  text-align: right;
}
```

### Résultats

- **RTL pixel-perfect en 2 semaines** : Livré dans le délai fixé, avec un rendu validé par un locuteur natif arabe.
- **0 régression LTR** : La suite Playwright de 180 tests passe à 100% pour les 8 locales existantes. Aucun ticket support sur les langues LTR dans les 3 mois suivants.
- **+15 000 utilisateurs arabophones en 3 mois** après le lancement de la version arabe, représentant 3% des nouveaux utilisateurs et un marché potentiel de 2,1M€ de revenus annuels.
- **1 847 propriétés physiques → 0** : La base de code est désormais entièrement en propriétés logiques, facilitant l'ajout futur de l'hébreu et du persan.
- **Temps de migration** : 1 402 propriétés migrées automatiquement par le codemod en 3 minutes. 445 traitées manuellement en 2 jours.

### Leçons apprises

Le codemod automatique couvre les 75% de cas simples et économise 2 jours de migration manuelle — l'investissement de 4 heures pour écrire le script est rentabilisé immédiatement. La décision de forcer les chiffres latins (`numberingSystem: 'latn'`) simplifie le travail de design et évite les problèmes de rendu dans les graphiques (Chart.js, Recharts ne supportent pas nativement les chiffres arabes-indiens). Prévoir un QA par un locuteur natif est non-négociable : les tests automatiques ne détectent pas les nuances culturelles (sens de lecture des formulaires, ordre des champs nom/prénom inversé en arabe).

---

## Cas 3 — Workflow Crowdin CI/CD avec Validation Automatique

### Contexte

ProcureFlow, éditeur d'une solution d'achats et de gestion des fournisseurs pour les ETI, travaille avec une équipe de 50 traducteurs externes (agence de traduction spécialisée en logiciels B2B) pour localiser l'application dans 15 langues. La base contient 10 200 clés de traduction réparties en 24 namespaces. Le rythme de livraison est de 3 releases par mois (releases bimensuelles + 1 hotfix), chaque release incluant en moyenne 80 à 150 nouvelles clés.

L'équipe de développement compte 35 développeurs dont 8 front-end. Crowdin est la plateforme TMS (Translation Management System) choisie pour sa compatibilité GitHub et son API robuste.

### Problème

Le processus de gestion des traductions est entièrement manuel et génère des incidents récurrents :

**Traductions manquantes en production** : En moyenne 12 clés manquantes par release arrivent en production — elles s'affichent avec la clé brute (`dashboard.metrics.users`) ou en anglais (fallback i18next). Les utilisateurs signalent ces anomalies via le support, créant des tickets urgents non planifiés.

**Conflits de merge** : Les fichiers `messages/*.json` sont fréquemment en conflit quand plusieurs branches ajoutent des clés en parallèle. La résolution manuelle des conflits prend 2 à 4 heures par release et génère parfois des erreurs de syntaxe JSON non détectées.

**Délai de livraison** : Le cycle de traduction actuel dure 10 à 15 jours : création de la PR avec les nouvelles clés → export manuel vers Crowdin → traduction par les 50 traducteurs → import manuel → PR de retour. Ce délai impose soit de livrer sans traductions (et patcher plus tard), soit de bloquer la release.

**Clés inutilisées** : 340 clés présentes dans les fichiers de traduction ne sont plus utilisées dans le code (refactoring, fonctionnalités supprimées). Elles polluent la base et allongent le temps de traduction payé à l'agence.

### Solution

Mettre en place une intégration GitHub-Crowdin entièrement automatisée, avec des gates de qualité bloquants dans la CI.

**Architecture du workflow** :

```
Developer push (feat/...) → CI validation locale
→ PR merged to main → Action: push sources vers Crowdin
→ Crowdin notifie les traducteurs → Traduction (2-3 jours)
→ Crowdin crée une PR automatique "feat: translations [crowdin]"
→ CI validation des traductions → Gate qualité (coverage > 98%)
→ Review automatique + merge → Disponible pour la prochaine release
```

```yaml
# .github/workflows/i18n-push.yml — Pousser les nouvelles clés vers Crowdin
name: Push sources vers Crowdin

on:
  push:
    branches: [main]
    paths:
      - 'packages/i18n/messages/fr.json'  # Locale de référence uniquement

jobs:
  push-sources:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Valider la syntaxe JSON de la locale de référence
        run: node -e "JSON.parse(require('fs').readFileSync('packages/i18n/messages/fr.json', 'utf8'))"

      - name: Valider les messages ICU
        run: npx ts-node scripts/valider-icu.ts --locale fr

      - name: Pousser les sources vers Crowdin
        uses: crowdin/github-action@v1
        with:
          upload_sources: true
          upload_translations: false
          crowdin_branch_name: ${{ github.sha }}
        env:
          CROWDIN_PROJECT_ID: ${{ secrets.CROWDIN_PROJECT_ID }}
          CROWDIN_PERSONAL_TOKEN: ${{ secrets.CROWDIN_TOKEN }}
```

```yaml
# .github/workflows/i18n-download.yml — Télécharger et valider les traductions
name: Télécharger traductions Crowdin

on:
  # Déclenché par un webhook Crowdin quand coverage >= 98%
  repository_dispatch:
    types: [crowdin-translations-ready]
  # Ou manuellement
  workflow_dispatch:

jobs:
  download-translations:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Télécharger les traductions depuis Crowdin
        uses: crowdin/github-action@v1
        with:
          upload_sources: false
          download_translations: true
          create_pull_request: true
          pull_request_title: 'feat: mise à jour des traductions [crowdin]'
          pull_request_labels: 'translations,automated'
          crowdin_branch_name: ${{ github.event.client_payload.branch }}
        env:
          CROWDIN_PROJECT_ID: ${{ secrets.CROWDIN_PROJECT_ID }}
          CROWDIN_PERSONAL_TOKEN: ${{ secrets.CROWDIN_TOKEN }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

```yaml
# .github/workflows/i18n-validation.yml — Gate de qualité sur les PRs de traduction
name: Validation des traductions

on:
  pull_request:
    paths:
      - 'packages/i18n/messages/*.json'

jobs:
  valider:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci

      - name: Clés manquantes (bloquant si > 0)
        run: npx ts-node scripts/valider-cles-manquantes.ts --seuil 0

      - name: Clés inutilisées (rapport seulement)
        run: npx ts-node scripts/detecter-cles-inutilisees.ts --reporter github

      - name: Validation ICU (bloquant si message malformé)
        run: npx ts-node scripts/valider-icu.ts --toutes-locales

      - name: Couverture de traduction (bloquant si < 98%)
        run: npx ts-node scripts/coverage.ts --seuil 98

      - name: Publier le rapport de couverture en commentaire PR
        uses: actions/github-script@v7
        with:
          script: |
            const rapport = require('./scripts/coverage-report.json');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Couverture des traductions\n${rapport.markdown}`
            });
```

```typescript
// scripts/detecter-cles-inutilisees.ts
import { glob } from 'glob';
import * as fs from 'fs';
import fr from '../packages/i18n/messages/fr.json';

// Aplatir toutes les clés de la locale de référence
function aplatirCles(obj: object, prefixe = ''): string[] {
  return Object.entries(obj).flatMap(([cle, valeur]) => {
    const cleComplete = prefixe ? `${prefixe}.${cle}` : cle;
    return typeof valeur === 'object'
      ? aplatirCles(valeur as object, cleComplete)
      : [cleComplete];
  });
}

async function detecterClesInutilisees(): Promise<void> {
  const toutesLesCles = aplatirCles(fr);

  // Lire tous les fichiers source (TSX, TS)
  const fichiers = await glob('apps/**/*.{tsx,ts}', { cwd: process.cwd() });
  const contenuFichiers = fichiers
    .map((f) => fs.readFileSync(f, 'utf8'))
    .join('\n');

  const clesInutilisees = toutesLesCles.filter((cle) => {
    // Rechercher chaque clé dans le code source
    const dernierSegment = cle.split('.').pop()!;
    return !contenuFichiers.includes(`'${dernierSegment}'`) &&
           !contenuFichiers.includes(`"${dernierSegment}"`);
  });

  console.log(`\nClés potentiellement inutilisées : ${clesInutilisees.length}`);
  clesInutilisees.forEach((c) => console.log(`  - ${c}`));
}

detecterClesInutilisees();
```

### Résultats

- **0 clé manquante en production depuis 6 mois** : Le gate de qualité bloquant (`--seuil 0`) empêche toute PR de traduction de passer si une clé est absente dans au moins une des 15 locales.
- **Délai de livraison des traductions réduit de 60%** : Le cycle est passé de 10-15 jours à 4-6 jours grâce à l'automatisation de l'upload vers Crowdin et de la création de PR.
- **340 clés inutilisées identifiées et supprimées** lors de l'audit initial, réduisant la base de traduction de 3.3% et économisant environ 2 800€ de frais de traduction annuels.
- **0 conflit de merge** sur les fichiers de traduction depuis la mise en place : Crowdin crée des PRs dédiées sur une branche isolée, jamais sur main directement.
- **Rapport de couverture automatique** : Chaque PR affiche un commentaire avec le taux de couverture par locale, permettant de décider d'inclure ou non la locale dans la release.

### Leçons apprises

Le webhook Crowdin → GitHub (via `repository_dispatch`) est la clé du workflow entièrement automatisé — sans lui, il faut déclencher manuellement le download. Le configurer demande 2 heures de mise en place dans Crowdin mais économise des dizaines d'heures sur la durée. Le rapport de couverture en commentaire de PR est très apprécié des développeurs — ils comprennent immédiatement l'impact de leurs changements sur les traductions sans aller dans Crowdin. Définir un seuil de 98% plutôt que 100% permet de gérer les rares cas de traductions en cours pour une langue moins prioritaire sans bloquer les autres.

---

## Cas 4 — Détection Automatique des Hardcoded Strings

### Contexte

InsightDash, éditeur d'une plateforme d'analytics et de business intelligence pour les équipes data, a décidé d'internationaliser son application React après 4 ans de développement en anglais uniquement. L'application est une SPA React 18 avec Vite, Redux Toolkit, et une base de code de 200 000 lignes (950 composants, 340 hooks, 220 fichiers de services). Aucun système d'i18n n'est en place — tout le texte est codé en dur dans le JSX et le JavaScript. L'objectif est de supporter le français, l'espagnol, l'allemand, le japonais et le coréen en 6 mois, en priorisant les pages les plus visitées.

L'équipe technique compte 18 développeurs front-end. Le CTO fixe une contrainte : la migration i18n ne doit pas bloquer les développements produit en cours — elle doit se faire en parallèle, de manière progressive.

### Problème

Le premier audit manuel sur 10 composants révèle 3 000 strings codées en dur estimées dans l'ensemble du projet (extrapolation statistique). Ces strings incluent :

- **Textes UI** (boutons, labels, titres, messages d'erreur, placeholders) — ~60% du total
- **Messages d'erreur et de validation** (côté client) — ~20%
- **Textes de configuration** (noms de colonnes de tableaux, noms de métriques) — ~15%
- **Textes techniques non traduisibles** (noms de variables, logs, identifiants) — ~5%

Le défi est triple : **détecter** automatiquement les strings, **classifier** celles qui doivent être traduites vs celles qui ne le doivent pas, et **extraire** progressivement sans casser l'application.

### Solution

**Phase 1 — Détection automatique (semaines 1-2)** : Configurer ESLint avec `eslint-plugin-i18n-json` et un plugin custom pour détecter les strings JSX et les props de composants. L'objectif n'est pas de zéro warning immédiatement, mais d'avoir une liste exhaustive classée par priorité.

```javascript
// .eslintrc.js — Règles de détection des strings codées en dur
module.exports = {
  plugins: ['i18n-json', '@local/detect-hardcoded-strings'],
  rules: {
    // Détecter les strings dans le JSX (contenu entre balises)
    '@local/detect-hardcoded-strings/jsx-text': 'warn',
    // Détecter les props de composants avec des strings UI
    '@local/detect-hardcoded-strings/jsx-props': ['warn', {
      propsACibler: ['label', 'placeholder', 'title', 'aria-label', 'tooltip'],
      exclure: ['className', 'id', 'data-testid', 'type', 'href', 'src'],
    }],
    // Détecter les strings dans les objets (config de tableaux, etc.)
    '@local/detect-hardcoded-strings/object-strings': ['warn', {
      patterns: ['header:', 'label:', 'title:', 'description:'],
    }],
  },
};
```

```bash
# Exécuter l'audit ESLint et générer un rapport CSV classé par nombre d'occurrences
npx eslint src/ --rule '@local/detect-hardcoded-strings/jsx-text: warn' \
  --format json \
  | node scripts/generer-rapport-audit.js \
  > audit-hardcoded-strings.csv

# Résultat : 3 247 strings détectées dans 847 fichiers
# Classées par : fichier, ligne, type (jsx-text|prop), contenu, priorité estimée
```

**Phase 2 — Classification et prioritisation (semaines 3-4)** : Analyser le rapport CSV. Classifier automatiquement par règles : strings de moins de 3 caractères → non traduisibles (IDs, codes) ; strings contenant uniquement des chiffres, URLs, emails → non traduisibles ; strings provenant de fichiers `*.config.*` ou `*.constants.*` → configuration (traiter séparément).

```typescript
// scripts/classifier-strings.ts — Classification automatique
interface StringDetectee {
  fichier: string;
  ligne: number;
  contenu: string;
  type: 'jsx-text' | 'prop' | 'objet';
}

type Categorie = 'traduire' | 'config' | 'ignorer';

function classifier(string: StringDetectee): Categorie {
  const { contenu, fichier } = string;

  // Ignorer les strings techniques
  if (contenu.length < 3) return 'ignorer';
  if (/^[A-Z_0-9]+$/.test(contenu)) return 'ignorer'; // Constantes
  if (/^https?:\/\//.test(contenu)) return 'ignorer';  // URLs
  if (/^[\d.,€$%]+$/.test(contenu)) return 'ignorer';  // Chiffres

  // Strings de configuration (noms de colonnes, métriques)
  if (fichier.includes('.config.') || fichier.includes('.constants.')) {
    return 'config';
  }

  // Strings de test — ne pas migrer
  if (fichier.includes('.test.') || fichier.includes('.spec.')) {
    return 'ignorer';
  }

  // Tout le reste → à traduire
  return 'traduire';
}
```

**Phase 3 — Extraction par codemods AST (semaines 5-16)** : Utiliser jscodeshift pour extraire automatiquement les strings classées "traduire" et les remplacer par des appels `t('clé')`. Les codemods traitent module par module, en commençant par les pages les plus visitées (analytics de la Home page).

```javascript
// codemods/extraire-jsx-text.js — jscodeshift transform
module.exports = function(fileInfo, api) {
  const j = api.jscodeshift;
  const root = j(fileInfo.source);
  const extractions = [];

  // Trouver tous les noeuds JSX avec du texte littéral
  root.find(j.JSXText).forEach((path) => {
    const texte = path.value.value.trim();
    if (!texte || texte.length < 3) return;

    // Générer une clé à partir du texte (slug)
    const cle = genererCle(texte, fileInfo.path);

    // Remplacer le texte JSX par {t('cle')}
    j(path).replaceWith(
      j.jsxExpressionContainer(
        j.callExpression(j.identifier('t'), [j.stringLiteral(cle)])
      )
    );

    extractions.push({ cle, texte, fichier: fileInfo.path });
  });

  // Écrire les extractions dans un fichier pour mise à jour de fr.json
  if (extractions.length > 0) {
    appendToExtractionLog(extractions);
  }

  return root.toSource();
};

function genererCle(texte, fichier) {
  // Extraire le nom du composant depuis le chemin du fichier
  const nomComposant = path.basename(fichier, '.tsx').toLowerCase();

  // Convertir le texte en slug
  const slug = texte
    .toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')  // Supprimer les accents
    .replace(/[^a-z0-9\s]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .slice(0, 40);  // Limiter la longueur

  return `${nomComposant}.${slug}`;
}
```

**Phase 4 — Pseudo-localisation en CI (semaine 17+)** : Après extraction d'une partie des strings, intégrer la pseudo-localisation dans la CI pour détecter automatiquement les régressions (nouvelles strings codées en dur).

```typescript
// scripts/pseudo-localiser.ts — Génère messages/pseudo.json
import fr from '../src/locales/fr.json';

function pseudoLocaliser(texte: string): string {
  const accents: Record<string, string> = {
    a: 'â', e: 'ê', i: 'î', o: 'ô', u: 'û',
    A: 'Â', E: 'Ê', I: 'Î', O: 'Ô', U: 'Û',
  };

  const transforme = [...texte]
    .map((c) => accents[c] ?? c)
    .join('');

  // Padding pour simuler les langues plus longues (allemand +30%, finnois +50%)
  return `[ŕéf ${transforme} ŕéf]`;
}

function pseudoLocaliserMessages(messages: object): object {
  return Object.fromEntries(
    Object.entries(messages).map(([cle, valeur]) => [
      cle,
      typeof valeur === 'string' ? pseudoLocaliser(valeur) : pseudoLocaliserMessages(valeur as object),
    ])
  );
}

const pseudo = pseudoLocaliserMessages(fr);
fs.writeFileSync('src/locales/pseudo.json', JSON.stringify(pseudo, null, 2));
```

```yaml
# .github/workflows/pseudo-localisation.yml — CI gate anti-régression
name: Pseudo-localisation CI

on: [pull_request]

jobs:
  tester-pseudo:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx ts-node scripts/pseudo-localiser.ts
      - name: Lancer l'application avec la pseudo-locale
        run: npm run build -- --env VITE_LOCALE=pseudo
      - name: Tests Playwright avec pseudo-locale
        run: npx playwright test --project=pseudo
        # Les tests détectent les strings non pseudo-localisées (= hardcoded)
      - name: Compter les strings hardcoded restantes
        run: npx eslint src/ --rule '@local/detect-hardcoded-strings/jsx-text: error' --format json | node scripts/compter-regressions.js
```

### Résultats

- **95% des strings extraites en 3 mois** : 3 085 des 3 247 strings détectées ont été extraites et intégrées dans `fr.json`. Les 162 restantes sont des strings de configuration traitées séparément ou des cas limites documentés.
- **La pseudo-localisation bloque les régressions en CI** : Depuis l'activation du gate, 0 nouvelle string hardcoded n'a atteint la branche main. Les développeurs reçoivent un rapport clair avec le nom du fichier et la ligne à corriger.
- **Processus non-bloquant pour le produit** : La migration s'est faite en parallèle des développements produit grâce aux codemods module par module. Aucune feature n'a été retardée.
- **Couverture de traduction au lancement FR/ES/DE** : 98,7% des clés traduites en espagnol et allemand, 97,2% en japonais et coréen — au-dessus du seuil de 97% fixé pour le lancement.
- **Économie de temps** : Les codemods automatiques ont extrait 70% des strings sans intervention manuelle, économisant environ 180 heures de migration manuelle estimées.

### Leçons apprises

La classification automatique des strings (traduire / config / ignorer) est la clé pour éviter de noyer les développeurs sous des milliers de warnings ESLint non pertinents. Sans classification, les équipes désactivent les règles ESLint. Les codemods AST fonctionnent remarquablement bien pour 70% des cas simples, mais les 30% restants — strings dans les closures, strings dynamiques concaténées, objets de configuration — nécessitent une intervention manuelle. Documenter ces cas dans un fichier `MIGRATION-I18N.md` permet aux développeurs de les traiter de manière cohérente. La pseudo-localisation est l'investissement le plus rentable sur le long terme : une fois en place, elle garantit que la dette i18n ne ré-augmente pas, sans effort supplémentaire de la part de l'équipe.
