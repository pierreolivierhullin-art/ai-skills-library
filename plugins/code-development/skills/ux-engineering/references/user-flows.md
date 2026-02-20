# User Flows, Navigation & Architecture de l'Information

## Overview

Ce document de référence couvre la conception et l'implémentation des flux utilisateur, des patterns de navigation, et de l'architecture de l'information dans les applications React modernes. Maîtriser ces concepts permet de créer des expériences fluides où les utilisateurs trouvent ce dont ils ont besoin sans friction. Applique ces patterns dès la phase de conception, avant d'écrire la moindre ligne de code — un bon flux documenté évite les refactorings coûteux à mi-projet.

---

## Cartographie des Flux Utilisateur

### Anatomie d'un flux utilisateur

Un flux utilisateur (user flow) décrit le chemin qu'emprunte un utilisateur pour accomplir un objectif précis dans ton application. Chaque flux contient trois types de chemins :

- **Happy path** : le chemin idéal sans erreur ni hésitation
- **Edge cases** : les cas limites (données vides, quota dépassé, premier usage)
- **Error paths** : les chemins d'erreur (réseau, validation, permissions refusées)

Documente ces trois dimensions avant d'implémenter quoi que ce soit. Un diagramme simple en Mermaid suffit pour la communication d'équipe :

```
// Exemple de flux d'inscription — à mettre dans un fichier .md ou Notion

Arrivée page → [Formulaire email/mot de passe]
  ↓ Happy path
[Validation côté client OK]
  ↓
[Appel API POST /auth/register]
  ↓ Succès (201)            ↓ Erreur (409 email pris)    ↓ Erreur réseau
[Redirection /onboarding]   [Message "Email déjà utilisé"] [Toast "Vérifier connexion"]
  ↓
[Étape 1 : Profil]
  ↓
[Étape 2 : Préférences]
  ↓
[Dashboard]
```

### Convention de notation des flux

Utilise ces symboles dans tes diagrammes pour standardiser la communication :

| Symbole | Signification |
|---------|---------------|
| Rectangle | Action utilisateur ou écran |
| Losange | Décision (condition) |
| Ovale | Début / Fin du flux |
| Flèche pleine | Transition normale |
| Flèche pointillée | Redirection automatique |
| [Texte entre crochets] | Condition de la transition |

### TypeScript : modélisation des états d'un flux

Représente les états d'un flux complexe avec un type discriminant — cela force la complétude dans les switch/case et évite les états impossibles :

```typescript
// types/flux-inscription.ts
type ÉtatFluxInscription =
  | { étape: 'formulaire'; erreurs: Record<string, string> }
  | { étape: 'vérification-email'; email: string }
  | { étape: 'onboarding'; utilisateurId: string; étapeOnboarding: 1 | 2 | 3 }
  | { étape: 'terminé'; utilisateurId: string };

type ActionFlux =
  | { type: 'SOUMETTRE_FORMULAIRE'; email: string; motDePasse: string }
  | { type: 'EMAIL_VÉRIFIÉ'; token: string }
  | { type: 'ÉTAPE_ONBOARDING_SUIVANTE' }
  | { type: 'TERMINER_ONBOARDING' };

function réduireFlux(
  état: ÉtatFluxInscription,
  action: ActionFlux
): ÉtatFluxInscription {
  switch (état.étape) {
    case 'formulaire':
      if (action.type === 'SOUMETTRE_FORMULAIRE') {
        return { étape: 'vérification-email', email: action.email };
      }
      return état;

    case 'vérification-email':
      if (action.type === 'EMAIL_VÉRIFIÉ') {
        return { étape: 'onboarding', utilisateurId: action.token, étapeOnboarding: 1 };
      }
      return état;

    case 'onboarding':
      if (action.type === 'ÉTAPE_ONBOARDING_SUIVANTE' && état.étapeOnboarding < 3) {
        return { ...état, étapeOnboarding: (état.étapeOnboarding + 1) as 2 | 3 };
      }
      if (action.type === 'TERMINER_ONBOARDING') {
        return { étape: 'terminé', utilisateurId: état.utilisateurId };
      }
      return état;

    case 'terminé':
      return état;
  }
}
```

---

## Architecture de l'Information

### Principes fondamentaux de l'IA

L'architecture de l'information (IA) organise le contenu pour que les utilisateurs trouvent ce dont ils ont besoin. Applique ces quatre principes :

1. **Principe d'organisation** : regroupe les éléments selon des critères logiques pour l'utilisateur, pas pour ton organisation interne
2. **Principe de labellisation** : utilise le vocabulaire de tes utilisateurs, pas le jargon métier ou technique
3. **Principe de navigation** : offre plusieurs chemins vers la même information (menu, recherche, liens contextuels)
4. **Principe de recherche** : prévois comment les utilisateurs chercheront quand la navigation échoue

### Card sorting — méthode pratique

Le card sorting est une technique de recherche utilisateur pour valider ton IA avant de l'implémenter. Procède ainsi :

- **Ouvert** : donne 30-40 cartes représentant du contenu, demande aux utilisateurs de les regrouper et nommer les groupes → révèle les modèles mentaux
- **Fermé** : donne les mêmes cartes avec des catégories prédéfinies → valide une IA existante
- **Seuil de consensus** : si 70%+ des participants placent un élément dans la même catégorie, cette association est solide

### Sitemap : structure de navigation documentée

Documente la structure de ton application avant de configurer ton routeur :

```
/ (Racine)
├── /dashboard
│   ├── /dashboard/analytics
│   └── /dashboard/reports
├── /projets
│   ├── /projets (liste)
│   ├── /projets/nouveau
│   └── /projets/:id
│       ├── /projets/:id/aperçu
│       ├── /projets/:id/tâches
│       └── /projets/:id/paramètres
├── /équipe
│   ├── /équipe/membres
│   └── /équipe/invitations
└── /paramètres
    ├── /paramètres/profil
    ├── /paramètres/facturation
    └── /paramètres/intégrations
```

Cette carte devient directement la configuration de ton routeur React Router v6 ou Next.js.

---

## Navigation en React — React Router v6 et Next.js App Router

### React Router v6 — configuration avec layouts imbriqués

```typescript
// app/router.tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { LayoutApp } from './layouts/LayoutApp';
import { LayoutProjet } from './layouts/LayoutProjet';
import { PageDashboard } from './pages/PageDashboard';
import { PageProjets } from './pages/PageProjets';
import { PageProjetAperçu } from './pages/PageProjetAperçu';
import { PageProjetTâches } from './pages/PageProjetTâches';
import { PageErreur } from './pages/PageErreur';

const routeur = createBrowserRouter([
  {
    path: '/',
    element: <LayoutApp />,
    errorElement: <PageErreur />,
    children: [
      {
        index: true,
        element: <PageDashboard />,
      },
      {
        path: 'projets',
        children: [
          {
            index: true,
            element: <PageProjets />,
          },
          {
            path: ':projetId',
            element: <LayoutProjet />,
            loader: async ({ params }) => {
              // Chargement des données du projet avant le rendu
              const projet = await récupérerProjet(params.projetId!);
              if (!projet) throw new Response('Projet non trouvé', { status: 404 });
              return projet;
            },
            children: [
              {
                index: true,
                element: <PageProjetAperçu />,
              },
              {
                path: 'tâches',
                element: <PageProjetTâches />,
              },
              {
                path: 'paramètres',
                lazy: () => import('./pages/PageProjetParamètres'),
              },
            ],
          },
        ],
      },
    ],
  },
]);

export function Routeur() {
  return <RouterProvider router={routeur} />;
}
```

### Next.js App Router — structure de fichiers

```
app/
├── layout.tsx               ← Layout racine (HTML, body, providers)
├── page.tsx                 ← Page d'accueil /
├── (dashboard)/             ← Groupe de routes (pas dans l'URL)
│   ├── layout.tsx           ← Layout partagé pour le dashboard
│   ├── dashboard/
│   │   └── page.tsx         ← /dashboard
│   └── analytics/
│       └── page.tsx         ← /analytics
├── projets/
│   ├── page.tsx             ← /projets
│   ├── nouveau/
│   │   └── page.tsx         ← /projets/nouveau
│   └── [projetId]/
│       ├── layout.tsx       ← Layout du projet (barre latérale, onglets)
│       ├── page.tsx         ← /projets/:projetId
│       ├── tâches/
│       │   └── page.tsx     ← /projets/:projetId/tâches
│       └── @modal/          ← Slot parallèle pour modales
│           └── (.)tâches/[tâcheId]/
│               └── page.tsx ← Modale intercept
└── api/
    └── projets/
        └── route.ts
```

```typescript
// app/projets/[projetId]/layout.tsx
import { notFound } from 'next/navigation';
import { NavigationProjet } from '@/components/NavigationProjet';

interface PropriétésLayout {
  children: React.ReactNode;
  params: Promise<{ projetId: string }>;
}

export default async function LayoutProjet({ children, params }: PropriétésLayout) {
  const { projetId } = await params;
  const projet = await récupérerProjet(projetId);

  if (!projet) {
    notFound();
  }

  return (
    <div className="flex h-screen">
      <NavigationProjet projet={projet} />
      <main className="flex-1 overflow-auto p-6">
        {children}
      </main>
    </div>
  );
}
```

---

## Composant Fil d'Ariane (Breadcrumb) avec ARIA

Le fil d'ariane aide les utilisateurs à comprendre leur position dans la hiérarchie et à remonter rapidement. Implémente-le avec une sémantique ARIA correcte :

```typescript
// components/FilAriane.tsx
import { Link, useMatches } from 'react-router-dom';

interface MigaBreadcrumb {
  label: string;
  chemin?: string;
}

// Ajoute cette propriété au handle de chaque route dans ta config routeur :
// handle: { filAriane: (data: DonnéesRoute) => ({ label: data.nom }) }

export function FilAriane() {
  const correspondances = useMatches();

  const migas = correspondances
    .filter((m) => m.handle && (m.handle as { filAriane?: unknown }).filAriane)
    .map((m) => {
      const handle = m.handle as { filAriane: (data: unknown) => MigaBreadcrumb };
      return {
        ...handle.filAriane(m.data),
        id: m.id,
        chemin: m.pathname,
      };
    });

  if (migas.length <= 1) return null;

  return (
    <nav aria-label="Fil d'Ariane">
      <ol
        className="flex items-center gap-1 text-sm text-gris-500"
        itemScope
        itemType="https://schema.org/BreadcrumbList"
      >
        {migas.map((miga, index) => {
          const estDernière = index === migas.length - 1;

          return (
            <li
              key={miga.id}
              className="flex items-center gap-1"
              itemProp="itemListElement"
              itemScope
              itemType="https://schema.org/ListItem"
            >
              {estDernière ? (
                <span
                  className="font-medium text-gris-900"
                  aria-current="page"
                  itemProp="name"
                >
                  {miga.label}
                </span>
              ) : (
                <>
                  <Link
                    to={miga.chemin ?? '#'}
                    className="hover:text-gris-900 transition-colors underline-offset-2 hover:underline"
                    itemProp="item"
                  >
                    <span itemProp="name">{miga.label}</span>
                  </Link>
                  <ChevronDroiteIcone
                    className="h-3 w-3 shrink-0 text-gris-400"
                    aria-hidden="true"
                  />
                </>
              )}
              <meta itemProp="position" content={String(index + 1)} />
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
```

Usage dans la configuration du routeur :

```typescript
// Ajoute le handle à chaque route qui doit apparaître dans le fil d'Ariane
{
  path: ':projetId',
  loader: chargerProjet,
  handle: {
    filAriane: (données: Projet) => ({
      label: données.nom,
    }),
  },
  // ...
}
```

---

## Indicateur de Progression Multi-Étapes

```typescript
// components/IndicateurProgression.tsx
interface Étape {
  id: string;
  label: string;
  description?: string;
}

type StatutÉtape = 'complétée' | 'actuelle' | 'à-venir';

interface PropriétésIndicateurProgression {
  étapes: Étape[];
  étapeActuelle: number; // index 0-based
  orientation?: 'horizontal' | 'vertical';
  afficherDescriptions?: boolean;
}

export function IndicateurProgression({
  étapes,
  étapeActuelle,
  orientation = 'horizontal',
  afficherDescriptions = false,
}: PropriétésIndicateurProgression) {
  function obtenirStatut(index: number): StatutÉtape {
    if (index < étapeActuelle) return 'complétée';
    if (index === étapeActuelle) return 'actuelle';
    return 'à-venir';
  }

  return (
    <nav aria-label="Progression du formulaire">
      <ol
        className={`flex ${orientation === 'vertical' ? 'flex-col gap-4' : 'items-center gap-0'}`}
        role="list"
      >
        {étapes.map((étape, index) => {
          const statut = obtenirStatut(index);
          const estDernière = index === étapes.length - 1;

          return (
            <li
              key={étape.id}
              className={`flex ${orientation === 'horizontal' ? 'flex-1 items-center' : 'items-start gap-3'}`}
              aria-current={statut === 'actuelle' ? 'step' : undefined}
            >
              {/* Cercle indicateur */}
              <div className="flex shrink-0 flex-col items-center">
                <div
                  className={`
                    flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium
                    transition-colors duration-200
                    ${statut === 'complétée' ? 'bg-bleu-600 text-blanc' : ''}
                    ${statut === 'actuelle' ? 'border-2 border-bleu-600 bg-blanc text-bleu-600' : ''}
                    ${statut === 'à-venir' ? 'border-2 border-gris-300 bg-blanc text-gris-400' : ''}
                  `}
                  aria-hidden="true"
                >
                  {statut === 'complétée' ? (
                    <CocheIcone className="h-4 w-4" />
                  ) : (
                    <span>{index + 1}</span>
                  )}
                </div>

                {/* Ligne de connexion — orientation verticale */}
                {orientation === 'vertical' && !estDernière && (
                  <div
                    className={`mt-1 h-full w-0.5 ${index < étapeActuelle ? 'bg-bleu-600' : 'bg-gris-200'}`}
                    aria-hidden="true"
                  />
                )}
              </div>

              {/* Texte de l'étape */}
              <div className={`${orientation === 'horizontal' ? 'ml-3 min-w-0' : 'pb-4'}`}>
                <span
                  className={`
                    block text-sm font-medium
                    ${statut === 'actuelle' ? 'text-bleu-600' : ''}
                    ${statut === 'complétée' ? 'text-gris-900' : ''}
                    ${statut === 'à-venir' ? 'text-gris-400' : ''}
                  `}
                >
                  {étape.label}
                </span>
                {afficherDescriptions && étape.description && (
                  <span className="mt-0.5 block text-xs text-gris-500">
                    {étape.description}
                  </span>
                )}
              </div>

              {/* Ligne de connexion — orientation horizontale */}
              {orientation === 'horizontal' && !estDernière && (
                <div
                  className={`mx-4 h-0.5 flex-1 ${index < étapeActuelle ? 'bg-bleu-600' : 'bg-gris-200'}`}
                  aria-hidden="true"
                />
              )}
            </li>
          );
        })}
      </ol>

      {/* Annonce pour les lecteurs d'écran */}
      <div className="sr-only" aria-live="polite">
        Étape {étapeActuelle + 1} sur {étapes.length} : {étapes[étapeActuelle]?.label}
      </div>
    </nav>
  );
}
```

---

## Navigation par Onglets avec Support Clavier

```typescript
// components/NavigationOnglets.tsx
import { useRef, KeyboardEvent } from 'react';

interface Onglet {
  id: string;
  label: string;
  contenu: React.ReactNode;
  désactivé?: boolean;
}

interface PropriétésOnglets {
  onglets: Onglet[];
  ongletActif: string;
  surChangement: (id: string) => void;
  variant?: 'ligne' | 'pilule' | 'boîte';
}

export function NavigationOnglets({
  onglets,
  ongletActif,
  surChangement,
  variant = 'ligne',
}: PropriétésOnglets) {
  const réfsOnglets = useRef<(HTMLButtonElement | null)[]>([]);

  function gérerNavigationClavier(
    événement: KeyboardEvent<HTMLButtonElement>,
    indexActuel: number
  ) {
    const ongletsActifs = onglets.filter((o) => !o.désactivé);
    let nouvelIndex = indexActuel;

    switch (événement.key) {
      case 'ArrowRight':
      case 'ArrowDown':
        événement.preventDefault();
        nouvelIndex = (indexActuel + 1) % onglets.length;
        // Saute les onglets désactivés
        while (onglets[nouvelIndex]?.désactivé) {
          nouvelIndex = (nouvelIndex + 1) % onglets.length;
        }
        break;

      case 'ArrowLeft':
      case 'ArrowUp':
        événement.preventDefault();
        nouvelIndex = (indexActuel - 1 + onglets.length) % onglets.length;
        while (onglets[nouvelIndex]?.désactivé) {
          nouvelIndex = (nouvelIndex - 1 + onglets.length) % onglets.length;
        }
        break;

      case 'Home':
        événement.preventDefault();
        nouvelIndex = 0;
        while (onglets[nouvelIndex]?.désactivé) nouvelIndex++;
        break;

      case 'End':
        événement.preventDefault();
        nouvelIndex = onglets.length - 1;
        while (onglets[nouvelIndex]?.désactivé) nouvelIndex--;
        break;

      default:
        return;
    }

    réfsOnglets.current[nouvelIndex]?.focus();
    surChangement(onglets[nouvelIndex].id);
  }

  const ongletActuel = onglets.find((o) => o.id === ongletActif);

  return (
    <div>
      <div
        role="tablist"
        aria-label="Navigation principale"
        className={`flex ${variant === 'ligne' ? 'border-b border-gris-200' : 'gap-1 p-1 bg-gris-100 rounded-lg'}`}
      >
        {onglets.map((onglet, index) => {
          const estActif = onglet.id === ongletActif;

          return (
            <button
              key={onglet.id}
              ref={(el) => { réfsOnglets.current[index] = el; }}
              role="tab"
              aria-selected={estActif}
              aria-controls={`panneau-${onglet.id}`}
              id={`onglet-${onglet.id}`}
              tabIndex={estActif ? 0 : -1}
              disabled={onglet.désactivé}
              onClick={() => !onglet.désactivé && surChangement(onglet.id)}
              onKeyDown={(e) => gérerNavigationClavier(e, index)}
              className={`
                px-4 py-2 text-sm font-medium transition-all duration-150
                focus:outline-none focus-visible:ring-2 focus-visible:ring-bleu-500 focus-visible:ring-offset-2
                disabled:cursor-not-allowed disabled:opacity-40
                ${variant === 'ligne' && estActif ? 'border-b-2 border-bleu-600 text-bleu-600' : ''}
                ${variant === 'ligne' && !estActif ? 'text-gris-600 hover:text-gris-900 hover:border-b-2 hover:border-gris-300' : ''}
                ${variant === 'pilule' && estActif ? 'bg-bleu-600 text-blanc rounded-full' : ''}
                ${variant === 'pilule' && !estActif ? 'text-gris-600 hover:text-gris-900 rounded-full' : ''}
              `}
            >
              {onglet.label}
            </button>
          );
        })}
      </div>

      {onglets.map((onglet) => (
        <div
          key={onglet.id}
          role="tabpanel"
          id={`panneau-${onglet.id}`}
          aria-labelledby={`onglet-${onglet.id}`}
          hidden={onglet.id !== ongletActif}
          tabIndex={0}
          className="mt-4 focus:outline-none"
        >
          {onglet.contenu}
        </div>
      ))}
    </div>
  );
}
```

---

## Recherche avec Debounce et Autocomplétion

### Hook de recherche avec debounce

```typescript
// hooks/useRechercheDebounce.ts
import { useState, useEffect, useRef, useCallback } from 'react';

interface OptionRecherche<T> {
  délaiMs?: number;
  rechercherFn: (requête: string) => Promise<T[]>;
  nombreMinCaractères?: number;
}

interface ÉtatRecherche<T> {
  requête: string;
  résultats: T[];
  chargement: boolean;
  erreur: string | null;
}

export function useRechercheDebounce<T>({
  délaiMs = 300,
  rechercherFn,
  nombreMinCaractères = 2,
}: OptionRecherche<T>) {
  const [état, setÉtat] = useState<ÉtatRecherche<T>>({
    requête: '',
    résultats: [],
    chargement: false,
    erreur: null,
  });

  const annulerRef = useRef<AbortController | null>(null);
  const minuterieRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const définirRequête = useCallback(
    (nouvelleRequête: string) => {
      setÉtat((prev) => ({ ...prev, requête: nouvelleRequête }));

      if (minuterieRef.current) clearTimeout(minuterieRef.current);

      if (nouvelleRequête.length < nombreMinCaractères) {
        setÉtat((prev) => ({ ...prev, résultats: [], chargement: false }));
        return;
      }

      setÉtat((prev) => ({ ...prev, chargement: true, erreur: null }));

      minuterieRef.current = setTimeout(async () => {
        // Annule la requête précédente si elle est encore en cours
        annulerRef.current?.abort();
        annulerRef.current = new AbortController();

        try {
          const résultats = await rechercherFn(nouvelleRequête);
          setÉtat((prev) => ({ ...prev, résultats, chargement: false }));
        } catch (err) {
          if ((err as Error).name !== 'AbortError') {
            setÉtat((prev) => ({
              ...prev,
              erreur: 'Erreur lors de la recherche',
              chargement: false,
            }));
          }
        }
      }, délaiMs);
    },
    [délaiMs, rechercherFn, nombreMinCaractères]
  );

  useEffect(() => {
    return () => {
      if (minuterieRef.current) clearTimeout(minuterieRef.current);
      annulerRef.current?.abort();
    };
  }, []);

  return { ...état, définirRequête };
}
```

### Composant d'autocomplétion accessible

```typescript
// components/ChampAutocomplétion.tsx
import { useRef, useState, useId } from 'react';
import { useRechercheDebounce } from '@/hooks/useRechercheDebounce';

interface Suggestion {
  id: string;
  label: string;
  description?: string;
}

interface PropriétésAutocomplétion {
  placeholder?: string;
  surSélection: (suggestion: Suggestion) => void;
  rechercherFn: (requête: string) => Promise<Suggestion[]>;
  label: string;
}

export function ChampAutocomplétion({
  placeholder = 'Rechercher...',
  surSélection,
  rechercherFn,
  label,
}: PropriétésAutocomplétion) {
  const identifiant = useId();
  const [ouvert, setOuvert] = useState(false);
  const [indexFocus, setIndexFocus] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);

  const { requête, résultats, chargement, définirRequête } =
    useRechercheDebounce<Suggestion>({
      rechercherFn,
      délaiMs: 250,
    });

  function gérerChangement(e: React.ChangeEvent<HTMLInputElement>) {
    définirRequête(e.target.value);
    setOuvert(true);
    setIndexFocus(-1);
  }

  function gérerClavier(e: React.KeyboardEvent<HTMLInputElement>) {
    if (!ouvert) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setIndexFocus((prev) => Math.min(prev + 1, résultats.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setIndexFocus((prev) => Math.max(prev - 1, -1));
        break;
      case 'Enter':
        e.preventDefault();
        if (indexFocus >= 0 && résultats[indexFocus]) {
          sélectionner(résultats[indexFocus]);
        }
        break;
      case 'Escape':
        setOuvert(false);
        setIndexFocus(-1);
        break;
    }
  }

  function sélectionner(suggestion: Suggestion) {
    surSélection(suggestion);
    setOuvert(false);
    setIndexFocus(-1);
    inputRef.current?.blur();
  }

  const idListe = `${identifiant}-liste`;

  return (
    <div className="relative">
      <label htmlFor={identifiant} className="mb-1.5 block text-sm font-medium text-gris-700">
        {label}
      </label>
      <div className="relative">
        <input
          ref={inputRef}
          id={identifiant}
          type="search"
          role="combobox"
          aria-expanded={ouvert && résultats.length > 0}
          aria-controls={idListe}
          aria-activedescendant={
            indexFocus >= 0 ? `${idListe}-option-${indexFocus}` : undefined
          }
          aria-autocomplete="list"
          value={requête}
          onChange={gérerChangement}
          onKeyDown={gérerClavier}
          onFocus={() => résultats.length > 0 && setOuvert(true)}
          onBlur={() => setTimeout(() => setOuvert(false), 150)}
          placeholder={placeholder}
          autoComplete="off"
          className="w-full rounded-lg border border-gris-300 px-3 py-2 pr-9 text-sm
                     focus:border-bleu-500 focus:outline-none focus:ring-2 focus:ring-bleu-500/20"
        />

        {chargement && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2" aria-hidden="true">
            <SpinnerIcone className="h-4 w-4 animate-spin text-gris-400" />
          </div>
        )}
      </div>

      {ouvert && résultats.length > 0 && (
        <ul
          id={idListe}
          role="listbox"
          aria-label={`Suggestions pour "${requête}"`}
          className="absolute z-50 mt-1 w-full overflow-hidden rounded-lg border border-gris-200
                     bg-blanc shadow-lg"
        >
          {résultats.map((suggestion, index) => (
            <li
              key={suggestion.id}
              id={`${idListe}-option-${index}`}
              role="option"
              aria-selected={index === indexFocus}
              onClick={() => sélectionner(suggestion)}
              onMouseEnter={() => setIndexFocus(index)}
              className={`cursor-pointer px-3 py-2 text-sm transition-colors
                ${index === indexFocus ? 'bg-bleu-50 text-bleu-700' : 'text-gris-700 hover:bg-gris-50'}`}
            >
              <span className="font-medium">{suggestion.label}</span>
              {suggestion.description && (
                <span className="mt-0.5 block text-xs text-gris-400">
                  {suggestion.description}
                </span>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

---

## Deep Links — URL et États Navigables

### Principe des URL comme état partageable

Tout état que l'utilisateur pourrait vouloir partager, mémoriser ou retrouver doit vivre dans l'URL. Cela inclut : les filtres actifs, les onglets sélectionnés, les pages de pagination, les termes de recherche, et les modales importantes.

```typescript
// hooks/useParamètresURL.ts
import { useSearchParams } from 'react-router-dom';
import { useCallback } from 'react';

// Sérialise/désérialise les filtres depuis l'URL
export function useParamètresURL() {
  const [paramètres, setParamètres] = useSearchParams();

  const lire = useCallback(
    <T extends string>(clé: string, défaut: T): T => {
      return (paramètres.get(clé) as T) ?? défaut;
    },
    [paramètres]
  );

  const lireTableau = useCallback(
    (clé: string): string[] => {
      return paramètres.getAll(clé);
    },
    [paramètres]
  );

  const définir = useCallback(
    (mises_à_jour: Record<string, string | string[] | null>) => {
      setParamètres(
        (prév) => {
          const nouveaux = new URLSearchParams(prév);
          for (const [clé, valeur] of Object.entries(mises_à_jour)) {
            if (valeur === null) {
              nouveaux.delete(clé);
            } else if (Array.isArray(valeur)) {
              nouveaux.delete(clé);
              valeur.forEach((v) => nouveaux.append(clé, v));
            } else {
              nouveaux.set(clé, valeur);
            }
          }
          return nouveaux;
        },
        { replace: true } // évite de polluer l'historique du navigateur
      );
    },
    [setParamètres]
  );

  return { lire, lireTableau, définir };
}

// Exemple d'usage dans une page de liste
function PageListeProjets() {
  const { lire, lireTableau, définir } = useParamètresURL();

  const recherche = lire('q', '');
  const statuts = lireTableau('statut');
  const tri = lire<'nom' | 'date' | 'priorité'>('tri', 'date');
  const page = parseInt(lire('page', '1'), 10);

  // URL résultante : /projets?q=mobile&statut=actif&statut=pause&tri=priorité&page=2
  // — 100% partageable et mémorisable dans les favoris

  return (
    <div>
      <input
        value={recherche}
        onChange={(e) => définir({ q: e.target.value || null, page: '1' })}
        placeholder="Rechercher..."
      />
      {/* ... */}
    </div>
  );
}
```

---

## Navigation Mobile — Gestes et Bouton Retour

### Gestion du bouton retour Android et des gestes iOS

```typescript
// hooks/useNavigationMobile.ts
import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

interface OptionsNavigationMobile {
  intercepterRetour?: boolean;
  surRetour?: () => void;
}

export function useNavigationMobile({
  intercepterRetour = false,
  surRetour,
}: OptionsNavigationMobile = {}) {
  const naviguer = useNavigate();
  const emplacement = useLocation();

  useEffect(() => {
    if (!intercepterRetour) return;

    // Ajoute une entrée d'historique fantôme pour intercepter le retour
    window.history.pushState({ intercepté: true }, '');

    function gérerPopstate(événement: PopStateEvent) {
      if (événement.state?.intercepté) {
        // L'utilisateur a appuyé sur Retour
        if (surRetour) {
          surRetour();
        } else {
          naviguer(-1);
        }
      }
    }

    window.addEventListener('popstate', gérerPopstate);
    return () => {
      window.removeEventListener('popstate', gérerPopstate);
    };
  }, [intercepterRetour, surRetour, naviguer]);
}

// Composant tiroir (drawer) avec gestion du swipe et du retour
import { useRef } from 'react';

interface PropriétésTiroir {
  ouvert: boolean;
  surFermeture: () => void;
  children: React.ReactNode;
  côté?: 'gauche' | 'droite';
}

export function TiroirNavigation({
  ouvert,
  surFermeture,
  children,
  côté = 'gauche',
}: PropriétésTiroir) {
  const débutGlissementRef = useRef<number | null>(null);

  // Intercepte le bouton retour pour fermer le tiroir
  useNavigationMobile({
    intercepterRetour: ouvert,
    surRetour: surFermeture,
  });

  function gérerDébutGlissement(e: React.TouchEvent) {
    débutGlissementRef.current = e.touches[0].clientX;
  }

  function gérerFinGlissement(e: React.TouchEvent) {
    if (débutGlissementRef.current === null) return;
    const delta = e.changedTouches[0].clientX - débutGlissementRef.current;
    const seuil = 80; // pixels

    if (côté === 'gauche' && delta < -seuil) surFermeture();
    if (côté === 'droite' && delta > seuil) surFermeture();

    débutGlissementRef.current = null;
  }

  return (
    <>
      {/* Fond semi-transparent */}
      {ouvert && (
        <div
          className="fixed inset-0 z-40 bg-noir/50 backdrop-blur-sm"
          onClick={surFermeture}
          aria-hidden="true"
        />
      )}

      {/* Panneau du tiroir */}
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Menu de navigation"
        className={`
          fixed inset-y-0 z-50 w-72 bg-blanc shadow-xl
          transition-transform duration-300 ease-in-out
          ${côté === 'gauche' ? 'left-0' : 'right-0'}
          ${ouvert
            ? 'translate-x-0'
            : côté === 'gauche' ? '-translate-x-full' : 'translate-x-full'
          }
        `}
        onTouchStart={gérerDébutGlissement}
        onTouchEnd={gérerFinGlissement}
      >
        <button
          onClick={surFermeture}
          className="absolute right-4 top-4 rounded-full p-1 text-gris-500 hover:text-gris-900
                     focus:outline-none focus-visible:ring-2 focus-visible:ring-bleu-500"
          aria-label="Fermer le menu"
        >
          <FermerIcone className="h-5 w-5" />
        </button>

        {children}
      </div>
    </>
  );
}
```

---

## Recherche Facettée — Filtres Combinés

```typescript
// components/RechercheAvecFiltres.tsx
import { useState, useTransition } from 'react';
import { useParamètresURL } from '@/hooks/useParamètresURL';

interface Facette {
  clé: string;
  label: string;
  options: Array<{ valeur: string; label: string; nombre: number }>;
}

interface PropriétésRechercheAvecFiltres {
  facettes: Facette[];
  nombreRésultats: number;
  children: React.ReactNode;
}

export function RechercheAvecFiltres({
  facettes,
  nombreRésultats,
  children,
}: PropriétésRechercheAvecFiltres) {
  const { lire, lireTableau, définir } = useParamètresURL();
  const [enTransition, startTransition] = useTransition();
  const [tiroirOuvert, setTiroirOuvert] = useState(false);

  const recherche = lire('q', '');
  const filtresActifs = facettes.reduce<Record<string, string[]>>(
    (acc, facette) => ({
      ...acc,
      [facette.clé]: lireTableau(facette.clé),
    }),
    {}
  );

  const nombreFiltresActifs = Object.values(filtresActifs).flat().length;

  function basculerFiltre(clé: string, valeur: string) {
    const actifs = filtresActifs[clé] ?? [];
    const nouveaux = actifs.includes(valeur)
      ? actifs.filter((v) => v !== valeur)
      : [...actifs, valeur];

    startTransition(() => {
      définir({ [clé]: nouveaux.length > 0 ? nouveaux : null, page: '1' });
    });
  }

  function réinitialiser() {
    const remise_à_zéro = facettes.reduce<Record<string, null>>(
      (acc, f) => ({ ...acc, [f.clé]: null }),
      {}
    );
    startTransition(() => {
      définir({ ...remise_à_zéro, q: null, page: '1' });
    });
  }

  return (
    <div className="flex gap-6">
      {/* Panneau de filtres — desktop */}
      <aside className="hidden w-56 shrink-0 lg:block" aria-label="Filtres">
        <div className="flex items-center justify-between mb-4">
          <span className="text-sm font-medium text-gris-900">
            Filtres {nombreFiltresActifs > 0 && (
              <span className="ml-1 rounded-full bg-bleu-100 px-2 py-0.5 text-xs text-bleu-700">
                {nombreFiltresActifs}
              </span>
            )}
          </span>
          {nombreFiltresActifs > 0 && (
            <button
              onClick={réinitialiser}
              className="text-xs text-bleu-600 hover:text-bleu-800"
            >
              Tout effacer
            </button>
          )}
        </div>

        {facettes.map((facette) => (
          <fieldset key={facette.clé} className="mb-5">
            <legend className="mb-2 text-xs font-semibold uppercase tracking-wide text-gris-500">
              {facette.label}
            </legend>
            <ul className="space-y-1.5">
              {facette.options.map((option) => {
                const coché = filtresActifs[facette.clé]?.includes(option.valeur) ?? false;
                return (
                  <li key={option.valeur}>
                    <label className="flex cursor-pointer items-center gap-2 text-sm text-gris-700 hover:text-gris-900">
                      <input
                        type="checkbox"
                        checked={coché}
                        onChange={() => basculerFiltre(facette.clé, option.valeur)}
                        className="rounded border-gris-300 text-bleu-600
                                   focus:ring-2 focus:ring-bleu-500 focus:ring-offset-1"
                      />
                      <span className="flex-1">{option.label}</span>
                      <span className="text-xs text-gris-400">({option.nombre})</span>
                    </label>
                  </li>
                );
              })}
            </ul>
          </fieldset>
        ))}
      </aside>

      {/* Résultats */}
      <div className="flex-1 min-w-0">
        <div className="mb-4 flex items-center justify-between">
          <p className="text-sm text-gris-500" aria-live="polite" aria-atomic="true">
            {enTransition ? 'Mise à jour...' : `${nombreRésultats} résultat${nombreRésultats !== 1 ? 's' : ''}`}
          </p>
        </div>
        <div className={enTransition ? 'opacity-60 transition-opacity' : ''}>
          {children}
        </div>
      </div>
    </div>
  );
}
```

---

## Checklist de Validation des Flux et de la Navigation

Avant de livrer une fonctionnalité impliquant des flux ou de la navigation, vérifie ces points :

**Flux utilisateur**
- [ ] Les happy paths, edge cases et error paths sont documentés
- [ ] Les états impossibles sont prévenus par les types TypeScript
- [ ] Les transitions entre pages sont cohérentes et prévisibles

**Architecture de l'information**
- [ ] La profondeur de navigation ne dépasse pas 3 niveaux pour le contenu principal
- [ ] Les labels utilisent le vocabulaire des utilisateurs (pas le jargon technique)
- [ ] Plusieurs chemins mènent aux contenus importants

**Accessibilité et wayfinding**
- [ ] Le fil d'ariane est présent sur les pages profondes avec `aria-label` et `aria-current="page"`
- [ ] Les indicateurs de progression annoncent l'étape actuelle via `aria-live`
- [ ] La navigation par onglets fonctionne au clavier (flèches, Home, End)
- [ ] Le focus est géré correctement lors des transitions de page

**URL et deep links**
- [ ] Les états filtrables/triables/paginables vivent dans l'URL
- [ ] Le bouton Retour du navigateur se comporte de manière attendue
- [ ] Les URL partagées chargent le bon état de l'interface

**Mobile**
- [ ] Le bouton Retour Android ferme les tiroirs/modales avant de remonter
- [ ] Les gestes de glissement fonctionnent sur les composants tiroir
- [ ] La navigation de bas de page (bottom navigation) respecte les zones de sécurité iOS
