---
name: ux-engineering
version: 1.0.0
description: >
  user flow parcours utilisateur user journey onboarding first-run experience,
  progressive onboarding activation flow onboarding flow,
  conversion optimization CRO taux de conversion checkout flow parcours d'achat,
  low friction friction faible réduire la friction ergonomie,
  navigation intuitive information architecture wayfinding,
  form UX formulaire UX error state error handling empty state,
  loading state skeleton screen progressive disclosure,
  micro-interaction expérience utilisateur fluide,
  expérience utilisateur fluide UX engineering
---

# UX Engineering — Parcours Utilisateur, Onboarding & Conversion

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu conçois ou améliores un parcours utilisateur (inscription, checkout, activation)
- Tu implémentes un onboarding first-run pour un nouveau produit ou une fonctionnalité
- Tu veux réduire la friction sur un formulaire ou un tunnel de conversion
- Tu dois coder des états vides, des états d'erreur ou des états de chargement
- Tu travailles sur l'architecture de navigation d'une application (menus, breadcrumbs, stepper)
- Tu veux ajouter des micro-interactions pour renforcer le feedback utilisateur
- Tu analyses un taux de conversion faible et cherches des améliorations côté code
- Tu implémentes la progressive disclosure pour simplifier une interface complexe

---

## Fondamentaux — Design de Parcours Utilisateur

```
Principes clés du parcours utilisateur :
├── Clarté          — L'utilisateur sait toujours où il est et ce qu'il doit faire
├── Continuité      — Chaque étape découle naturellement de la précédente
├── Feedback        — Chaque action produit une réponse visible immédiate
├── Réversibilité   — L'utilisateur peut annuler, revenir en arrière, corriger
├── Progression     — La complexité augmente graduellement (progressive disclosure)
└── Récupération    — Les erreurs sont prévisibles et facilement corrigibles

Anti-patterns courants :
// ❌ Trop d'informations demandées d'un coup → abandon
// ❌ Pas de feedback après une action → confusion
// ❌ Erreur affichée uniquement à la soumission → frustration
// ❌ Navigation sans indicateur de position → désorientation
// ❌ État vide sans call-to-action → impasse
```

### Modèle HOOKED — Rétention par le Parcours

```
Déclencheur → Action → Récompense variable → Investissement
    ↑                                               |
    └───────────────────────────────────────────────┘

Exemple onboarding SaaS :
1. Déclencheur  : Email de bienvenue avec CTA "Créer mon premier projet"
2. Action       : Inscription simplifiée (email + mot de passe uniquement)
3. Récompense   : Valeur immédiate visible avant la fin de l'onboarding
4. Investissement : L'utilisateur connecte ses données, invite l'équipe
```

---

## Onboarding & First-Run Experience

```
Stratégies d'onboarding selon le type de produit :
────────────────────────────────────────────────────────────────
Complexité faible   → Tooltip tour, empty state éducatif
Complexité moyenne  → Progressive onboarding (déverrouiller au fur et à mesure)
Complexité élevée   → Wizard guidé + vidéo + base de connaissances intégrée
B2C grand public    → Onboarding "0 friction" (OAuth, skip possible)
B2B / SaaS          → Onboarding "valeur rapide" (aha-moment en < 5 min)
```

### Wizard d'Onboarding Multi-Étapes

```typescript
// hooks/useOnboardingWizard.ts
import { useState, useCallback } from 'react';

export interface ÉtapeOnboarding {
  id: string;
  titre: string;
  description: string;
  obligatoire: boolean;
  complétée: boolean;
}

const ÉTAPES_ONBOARDING: ÉtapeOnboarding[] = [
  {
    id: 'profil',
    titre: 'Ton profil',
    description: 'Personnalise ton espace de travail',
    obligatoire: true,
    complétée: false,
  },
  {
    id: 'équipe',
    titre: 'Ton équipe',
    description: 'Invite tes collaborateurs',
    obligatoire: false,
    complétée: false,
  },
  {
    id: 'intégration',
    titre: 'Première intégration',
    description: 'Connecte ton outil préféré',
    obligatoire: false,
    complétée: false,
  },
  {
    id: 'premier-projet',
    titre: 'Premier projet',
    description: 'Crée ton premier projet en 2 minutes',
    obligatoire: true,
    complétée: false,
  },
];

export function useOnboardingWizard(utilisateurId: string) {
  const [étapes, setÉtapes] = useState(ÉTAPES_ONBOARDING);
  const [étapeCourante, setÉtapeCourante] = useState(0);
  const [enChargement, setEnChargement] = useState(false);

  const pourcentageProgression = Math.round(
    (étapes.filter((é) => é.complétée).length / étapes.length) * 100
  );

  const étapesObligatoiresComplétées = étapes
    .filter((é) => é.obligatoire)
    .every((é) => é.complétée);

  const marquerComplétée = useCallback(
    async (étapeId: string) => {
      setEnChargement(true);
      try {
        await fetch(`/api/onboarding/${utilisateurId}/étapes/${étapeId}`, {
          method: 'PATCH',
          body: JSON.stringify({ complétée: true }),
        });

        setÉtapes((prev) =>
          prev.map((é) =>
            é.id === étapeId ? { ...é, complétée: true } : é
          )
        );

        // Passer automatiquement à l'étape suivante non complétée
        const prochaineÉtape = étapes.findIndex(
          (é, i) => i > étapeCourante && !é.complétée
        );
        if (prochaineÉtape !== -1) setÉtapeCourante(prochaineÉtape);
      } finally {
        setEnChargement(false);
      }
    },
    [utilisateurId, étapeCourante, étapes]
  );

  const ignorerÉtape = useCallback(
    (étapeId: string) => {
      const étape = étapes.find((é) => é.id === étapeId);
      if (étape?.obligatoire) return; // Impossible d'ignorer une étape obligatoire

      const prochaineÉtape = étapes.findIndex(
        (é, i) => i > étapeCourante && !é.complétée
      );
      if (prochaineÉtape !== -1) setÉtapeCourante(prochaineÉtape);
    },
    [étapes, étapeCourante]
  );

  return {
    étapes,
    étapeCourante,
    étapeActive: étapes[étapeCourante],
    pourcentageProgression,
    étapesObligatoiresComplétées,
    enChargement,
    marquerComplétée,
    ignorerÉtape,
    allerÀÉtape: setÉtapeCourante,
  };
}
```

```typescript
// components/OnboardingChecklist.tsx
function OnboardingChecklist({ utilisateurId }: { utilisateurId: string }) {
  const {
    étapes, pourcentageProgression, étapesObligatoiresComplétées,
    marquerComplétée, ignorerÉtape, allerÀÉtape,
  } = useOnboardingWizard(utilisateurId);

  if (étapesObligatoiresComplétées && pourcentageProgression === 100) {
    return null; // Masquer la checklist une fois tout complété
  }

  return (
    <aside className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <header className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">
          Bien démarrer
        </h2>
        <span className="text-sm font-medium text-blue-600">
          {pourcentageProgression}% complété
        </span>
      </header>

      {/* Barre de progression */}
      <div
        role="progressbar"
        aria-valuenow={pourcentageProgression}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label="Progression de l'onboarding"
        className="mb-4 h-2 overflow-hidden rounded-full bg-gray-100"
      >
        <div
          className="h-full rounded-full bg-blue-600 transition-all duration-500"
          style={{ width: `${pourcentageProgression}%` }}
        />
      </div>

      <ul className="space-y-3">
        {étapes.map((étape, index) => (
          <li
            key={étape.id}
            className={`flex items-start gap-3 rounded-lg p-3 transition-colors
              ${étape.complétée ? 'bg-green-50' : 'hover:bg-gray-50 cursor-pointer'}`}
            onClick={() => !étape.complétée && allerÀÉtape(index)}
          >
            <div
              className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full
                ${étape.complétée
                  ? 'bg-green-500 text-white'
                  : 'border-2 border-gray-300'}`}
            >
              {étape.complétée && <span aria-hidden>✓</span>}
            </div>
            <div className="min-w-0 flex-1">
              <p className={`text-sm font-medium
                ${étape.complétée ? 'text-green-700 line-through' : 'text-gray-900'}`}>
                {étape.titre}
                {étape.obligatoire && !étape.complétée && (
                  <span className="ml-1 text-xs text-gray-400">(requis)</span>
                )}
              </p>
              {!étape.complétée && (
                <p className="text-xs text-gray-500">{étape.description}</p>
              )}
            </div>
            {!étape.complétée && !étape.obligatoire && (
              <button
                onClick={(e) => { e.stopPropagation(); ignorerÉtape(étape.id); }}
                className="text-xs text-gray-400 hover:text-gray-600"
                aria-label={`Ignorer l'étape ${étape.titre}`}
              >
                Ignorer
              </button>
            )}
          </li>
        ))}
      </ul>
    </aside>
  );
}
```

---

## Réduire la Friction — Low Friction Design

```
Sources de friction à éliminer :
├── Cognitive    — Trop d'options, trop de texte, interface surchargée
├── Mécanique    — Trop de clics, formulaires longs, répétition d'informations
├── Temporelle   — Attentes perçues comme longues, pas de feedback de progression
├── Confiance    — Manque de preuves sociales, incertitude sur la sécurité
└── Technique    — Erreurs obscures, comportements inattendus, bugs visuels
```

### Formulaire avec Validation Inline et Autofill

```typescript
// components/FormulaireInscription.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schémaInscription = z.object({
  email: z
    .string()
    .min(1, "L'email est requis")
    .email("Format d'email invalide"),
  motDePasse: z
    .string()
    .min(8, 'Au moins 8 caractères')
    .regex(/[A-Z]/, 'Au moins une majuscule')
    .regex(/[0-9]/, 'Au moins un chiffre'),
  prénomNom: z.string().min(2, 'Ton prénom est requis'),
});

type DonnéesInscription = z.infer<typeof schémaInscription>;

function ChampTexte({
  label,
  erreur,
  indicEstValide,
  ...props
}: React.InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  erreur?: string;
  indicEstValide?: boolean;
}) {
  const id = props.name ?? label.toLowerCase().replace(/\s/g, '-');

  return (
    <div className="group">
      <label htmlFor={id} className="mb-1.5 block text-sm font-medium text-gray-700">
        {label}
      </label>
      <div className="relative">
        <input
          {...props}
          id={id}
          aria-describedby={erreur ? `${id}-erreur` : undefined}
          aria-invalid={!!erreur}
          className={`w-full rounded-lg border px-3.5 py-2.5 text-sm transition-colors outline-none
            focus:ring-2 focus:ring-offset-1
            ${erreur
              ? 'border-red-400 focus:ring-red-300'
              : indicEstValide
              ? 'border-green-400 focus:ring-green-300'
              : 'border-gray-300 focus:ring-blue-300 focus:border-blue-400'
            }`}
        />
        {indicEstValide && !erreur && (
          <span
            aria-hidden
            className="absolute right-3 top-1/2 -translate-y-1/2 text-green-500"
          >
            ✓
          </span>
        )}
      </div>
      {erreur && (
        <p
          id={`${id}-erreur`}
          role="alert"
          className="mt-1.5 flex items-center gap-1 text-xs text-red-600"
        >
          <span aria-hidden>⚠</span> {erreur}
        </p>
      )}
    </div>
  );
}

export function FormulaireInscription() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, dirtyFields, isValid },
    watch,
  } = useForm<DonnéesInscription>({
    resolver: zodResolver(schémaInscription),
    mode: 'onBlur',          // Valider à la perte de focus (évite les erreurs prématurées)
    reValidateMode: 'onChange', // Re-valider en temps réel dès qu'une erreur est affichée
  });

  const valeurs = watch();

  const onSubmit = async (données: DonnéesInscription) => {
    await fetch('/api/auth/inscription', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(données),
    });
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      noValidate // Désactiver la validation native (trop inconsistante)
      className="space-y-4"
    >
      <ChampTexte
        label="Prénom"
        type="text"
        autoComplete="given-name"
        placeholder="Alice"
        erreur={errors.prénomNom?.message}
        indicEstValide={dirtyFields.prénomNom && !errors.prénomNom}
        {...register('prénomNom')}
      />

      <ChampTexte
        label="Email"
        type="email"
        autoComplete="email"
        placeholder="alice@exemple.fr"
        erreur={errors.email?.message}
        indicEstValide={dirtyFields.email && !errors.email}
        {...register('email')}
      />

      <div>
        <ChampTexte
          label="Mot de passe"
          type="password"
          autoComplete="new-password"
          erreur={errors.motDePasse?.message}
          indicEstValide={dirtyFields.motDePasse && !errors.motDePasse}
          {...register('motDePasse')}
        />
        {/* Indicateur de force du mot de passe */}
        {valeurs.motDePasse && (
          <div className="mt-2 flex gap-1" aria-label="Force du mot de passe">
            {[8, 12, 16].map((seuil) => (
              <div
                key={seuil}
                className={`h-1 flex-1 rounded-full transition-colors ${
                  valeurs.motDePasse.length >= seuil
                    ? 'bg-green-400'
                    : 'bg-gray-200'
                }`}
              />
            ))}
          </div>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting || !isValid}
        className="w-full rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold
          text-white transition-all hover:bg-blue-700 disabled:cursor-not-allowed
          disabled:opacity-50 focus:outline-none focus:ring-2 focus:ring-blue-500
          focus:ring-offset-2"
      >
        {isSubmitting ? 'Création du compte…' : 'Créer mon compte gratuitement'}
      </button>
    </form>
  );
}
```

---

## Navigation & Information Architecture

```
Patterns de navigation selon la complexité :
────────────────────────────────────────────────────────────────
1-5 pages        → Barre de navigation horizontale (top nav)
5-15 sections    → Sidebar avec icônes + labels
15+ sections     → Sidebar hiérarchique avec groupes repliables
Contenus longs   → Anchor nav (table des matières latérale)
Multi-niveaux    → Breadcrumb obligatoire
Flux linéaires   → Stepper (progression visible)
```

### Stepper de Progression

```typescript
// components/StepperProgression.tsx
interface ÉtapeStepper {
  id: string;
  titre: string;
  statut: 'complétée' | 'active' | 'à-venir';
}

function StepperProgression({
  étapes,
  étapeCourante,
}: {
  étapes: ÉtapeStepper[];
  étapeCourante: number;
}) {
  return (
    <nav aria-label="Progression du formulaire">
      <ol className="flex items-center">
        {étapes.map((étape, index) => (
          <li
            key={étape.id}
            className={`flex items-center ${index < étapes.length - 1 ? 'flex-1' : ''}`}
            aria-current={étape.statut === 'active' ? 'step' : undefined}
          >
            {/* Numéro / icône d'étape */}
            <div className="flex flex-col items-center">
              <div
                className={`flex h-9 w-9 items-center justify-center rounded-full border-2
                  text-sm font-semibold transition-all
                  ${étape.statut === 'complétée'
                    ? 'border-blue-600 bg-blue-600 text-white'
                    : étape.statut === 'active'
                    ? 'border-blue-600 bg-white text-blue-600'
                    : 'border-gray-300 bg-white text-gray-400'
                  }`}
              >
                {étape.statut === 'complétée' ? (
                  <span aria-hidden>✓</span>
                ) : (
                  <span>{index + 1}</span>
                )}
              </div>
              <span
                className={`mt-2 text-xs font-medium ${
                  étape.statut === 'à-venir' ? 'text-gray-400' : 'text-gray-700'
                }`}
              >
                {étape.titre}
              </span>
            </div>

            {/* Ligne de connexion */}
            {index < étapes.length - 1 && (
              <div
                aria-hidden
                className={`mx-2 mb-4 h-0.5 flex-1 transition-all ${
                  étapes[index + 1]?.statut !== 'à-venir'
                    ? 'bg-blue-600'
                    : 'bg-gray-200'
                }`}
              />
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}
```

---

## États Vides, Erreurs & Loading States

### Empty State Éducatif

```typescript
// components/ÉtatVide.tsx
interface ÉtatVideProps {
  icône: React.ReactNode;
  titre: string;
  description: string;
  actionPrimaire?: {
    label: string;
    onClick: () => void;
  };
  actionSecondaire?: {
    label: string;
    href: string;
  };
}

function ÉtatVide({
  icône, titre, description, actionPrimaire, actionSecondaire,
}: ÉtatVideProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      <div
        aria-hidden
        className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl
          bg-gray-100 text-3xl"
      >
        {icône}
      </div>
      <h3 className="mb-2 text-base font-semibold text-gray-900">{titre}</h3>
      <p className="mb-6 max-w-sm text-sm text-gray-500">{description}</p>
      <div className="flex flex-col items-center gap-3 sm:flex-row">
        {actionPrimaire && (
          <button
            onClick={actionPrimaire.onClick}
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium
              text-white hover:bg-blue-700 focus:outline-none focus:ring-2
              focus:ring-blue-500 focus:ring-offset-2"
          >
            {actionPrimaire.label}
          </button>
        )}
        {actionSecondaire && (
          <a
            href={actionSecondaire.href}
            className="text-sm text-blue-600 hover:underline"
          >
            {actionSecondaire.label}
          </a>
        )}
      </div>
    </div>
  );
}

// Utilisation
<ÉtatVide
  icône="📋"
  titre="Aucun projet pour l'instant"
  description="Crée ton premier projet pour centraliser tes tâches et collaborer avec ton équipe."
  actionPrimaire={{ label: 'Créer un projet', onClick: ouvrirModalCréation }}
  actionSecondaire={{ label: 'Voir un exemple', href: '/démo' }}
/>
```

### Skeleton Screen — Performance Perçue

```typescript
// components/SkeletonCard.tsx
function SkeletonCard() {
  return (
    <div
      aria-hidden="true" // Masqué des lecteurs d'écran
      className="animate-pulse rounded-xl border border-gray-100 bg-white p-5 shadow-sm"
    >
      {/* Avatar + nom */}
      <div className="mb-4 flex items-center gap-3">
        <div className="h-10 w-10 rounded-full bg-gray-200" />
        <div className="space-y-1.5">
          <div className="h-3.5 w-32 rounded bg-gray-200" />
          <div className="h-2.5 w-20 rounded bg-gray-100" />
        </div>
      </div>
      {/* Contenu */}
      <div className="space-y-2">
        <div className="h-3 w-full rounded bg-gray-200" />
        <div className="h-3 w-5/6 rounded bg-gray-200" />
        <div className="h-3 w-4/6 rounded bg-gray-100" />
      </div>
    </div>
  );
}

// Wrapper générique avec gestion du suspense
function ListeAvecChargement<T>({
  données,
  enChargement,
  erreur,
  rendreCarte,
  nombreSquelettes = 3,
  étatVide,
}: {
  données: T[] | undefined;
  enChargement: boolean;
  erreur: Error | null;
  rendreCarte: (élément: T) => React.ReactNode;
  nombreSquelettes?: number;
  étatVide: React.ReactNode;
}) {
  if (erreur) return <BandeauErreur erreur={erreur} />;

  if (enChargement) {
    return (
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3" aria-busy="true">
        {Array.from({ length: nombreSquelettes }).map((_, i) => (
          <SkeletonCard key={i} />
        ))}
        <span className="sr-only">Chargement en cours…</span>
      </div>
    );
  }

  if (!données?.length) return <>{étatVide}</>;

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {données.map(rendreCarte)}
    </div>
  );
}
```

### Bandeau d'Erreur Actionnable

```typescript
// components/BandeauErreur.tsx
interface BandeauErreurProps {
  erreur: Error;
  réessayer?: () => void;
  contexte?: string;
}

function BandeauErreur({ erreur, réessayer, contexte }: BandeauErreurProps) {
  return (
    <div
      role="alert"
      aria-live="assertive"
      className="flex items-start gap-4 rounded-xl border border-red-200
        bg-red-50 p-4 text-sm"
    >
      <span aria-hidden className="mt-0.5 text-red-500">⚠</span>
      <div className="flex-1">
        <p className="font-medium text-red-800">
          {contexte ?? 'Une erreur est survenue'}
        </p>
        <p className="mt-1 text-red-600">
          {erreur.message}
        </p>
        {réessayer && (
          <button
            onClick={réessayer}
            className="mt-3 text-red-700 underline hover:no-underline
              focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1"
          >
            Réessayer
          </button>
        )}
      </div>
    </div>
  );
}
```

---

## Optimisation de la Conversion (CRO)

```
Leviers CRO côté développeur :
├── Vitesse         — Chaque 100ms de latence = -1% de conversion (Amazon)
├── Formulaire      — Chaque champ supplémentaire = -10% de complétion
├── Social proof    — Compteurs en temps réel, avatars de clients récents
├── Urgence/rareté  — Stocks limités, offres temporelles (à utiliser éthiquement)
├── Confiance       — HTTPS visible, logos de sécurité, mentions légales accessibles
└── Optimistic UI   — Afficher le succès avant confirmation serveur
```

### Optimistic UI — Réduire la Latence Perçue

> **React 19+** : utilise `useOptimistic` (hook natif) pour les cas simples — il gère automatiquement le rollback. Pour les cas complexes ou multi-étapes, le pattern manuel ci-dessous reste plus explicite.

```typescript
// hooks/useOptimisticLike.ts
import { useState, useTransition } from 'react';

export function useOptimisticLike(initialCount: number, initialLiked: boolean) {
  const [nombreAims, setNombreAims] = useState(initialCount);
  const [estAimé, setEstAimé] = useState(initialLiked);
  const [isPending, startTransition] = useTransition();

  const basculerAim = async (postId: string) => {
    // 1. Mise à jour immédiate (optimiste)
    const ancienNombre = nombreAims;
    const ancienEstAimé = estAimé;

    setEstAimé(!estAimé);
    setNombreAims(estAimé ? nombreAims - 1 : nombreAims + 1);

    // 2. Requête serveur en arrière-plan
    startTransition(async () => {
      try {
        const réponse = await fetch(`/api/posts/${postId}/aimer`, {
          method: 'POST',
        });
        if (!réponse.ok) throw new Error('Échec');
      } catch {
        // 3. Rollback si erreur
        setEstAimé(ancienEstAimé);
        setNombreAims(ancienNombre);
      }
    });
  };

  return { nombreAims, estAimé, isPending, basculerAim };
}
```

### Micro-Interactions — Feedback Immédiat

```typescript
// components/BoutonAvecRetour.tsx
import { useState } from 'react';

type ÉtatBouton = 'inactif' | 'chargement' | 'succès' | 'erreur';

function BoutonAvecRetour({
  action,
  labelInactif,
  labelChargement = 'Enregistrement…',
  labelSuccès = 'Enregistré !',
  labelErreur = 'Réessayer',
}: {
  action: () => Promise<void>;
  labelInactif: string;
  labelChargement?: string;
  labelSuccès?: string;
  labelErreur?: string;
}) {
  const [état, setÉtat] = useState<ÉtatBouton>('inactif');

  const handleClick = async () => {
    if (état === 'chargement') return;

    setÉtat('chargement');
    try {
      await action();
      setÉtat('succès');
      // Revenir à l'état initial après 2 secondes
      setTimeout(() => setÉtat('inactif'), 2000);
    } catch {
      setÉtat('erreur');
      setTimeout(() => setÉtat('inactif'), 3000);
    }
  };

  const styles: Record<ÉtatBouton, string> = {
    inactif: 'bg-blue-600 hover:bg-blue-700 text-white',
    chargement: 'bg-blue-400 cursor-wait text-white',
    succès: 'bg-green-600 text-white',
    erreur: 'bg-red-600 text-white',
  };

  const labels: Record<ÉtatBouton, string> = {
    inactif: labelInactif,
    chargement: labelChargement,
    succès: labelSuccès,
    erreur: labelErreur,
  };

  return (
    <button
      onClick={handleClick}
      disabled={état === 'chargement'}
      aria-busy={état === 'chargement'}
      aria-label={labels[état]}
      className={`rounded-lg px-4 py-2 text-sm font-medium transition-all duration-200
        focus:outline-none focus:ring-2 focus:ring-offset-2
        ${styles[état]}`}
    >
      <span
        className="inline-flex items-center gap-2 transition-all duration-200"
      >
        {état === 'chargement' && (
          <span
            aria-hidden
            className="inline-block h-4 w-4 animate-spin rounded-full
              border-2 border-white border-t-transparent"
          />
        )}
        {labels[état]}
      </span>
    </button>
  );
}
```

### Progressive Disclosure

```typescript
// components/ParametresAvancés.tsx
import { useState } from 'react';

function ParametresAvancés({ children }: { children: React.ReactNode }) {
  const [ouvert, setOuvert] = useState(false);

  return (
    <div className="mt-4 border-t border-gray-100 pt-4">
      <button
        type="button"
        onClick={() => setOuvert(!ouvert)}
        aria-expanded={ouvert}
        aria-controls="paramètres-avancés"
        className="flex w-full items-center justify-between text-sm
          text-gray-500 hover:text-gray-800 transition-colors"
      >
        <span>Paramètres avancés</span>
        <span
          aria-hidden
          className={`transition-transform duration-200 ${ouvert ? 'rotate-180' : ''}`}
        >
          ▾
        </span>
      </button>

      <div
        id="paramètres-avancés"
        hidden={!ouvert}
        className={`mt-4 space-y-4 ${ouvert ? 'animate-fade-in' : ''}`}
      >
        {children}
      </div>
    </div>
  );
}
```

---

## Quick Reference

```
Checklist UX Engineering — Parcours Utilisateur
──────────────────────────────────────────────────────────────────
Onboarding
  ☐ L'aha-moment est atteignable en < 5 minutes
  ☐ Les étapes obligatoires sont différenciées des facultatives
  ☐ Une étape peut être ignorée ou reprise plus tard
  ☐ La progression est visible et persistante

Formulaires
  ☐ Validation inline (onChange ou onBlur, pas uniquement onSubmit)
  ☐ Messages d'erreur spécifiques et actionnables (pas de "champ invalide")
  ☐ autocomplete configuré sur tous les champs standards
  ☐ Le bouton de soumission reflète l'état (chargement, succès, erreur)
  ☐ Désactiver le submit pendant le traitement (anti double-soumission)

États de l'interface
  ☐ Chaque liste a un empty state avec un call-to-action
  ☐ Les skeletons respectent la forme du contenu réel
  ☐ Les erreurs sont localisées au champ concerné (pas uniquement globales)
  ☐ Les erreurs réseau proposent un bouton "Réessayer"
  ☐ aria-live="polite/assertive" sur les zones de feedback dynamiques

Navigation
  ☐ Un breadcrumb ou un stepper est présent sur les flux multi-étapes
  ☐ L'item actif de la navigation est identifiable visuellement et en a11y
  ☐ Le titre de la page reflète l'étape en cours

Conversion
  ☐ Les actions critiques utilisent l'optimistic UI quand c'est possible
  ☐ Le bouton primaire est clairement identifiable (hiérarchie visuelle)
  ☐ Le formulaire d'inscription ne demande que l'essentiel (email + mdp)
  ☐ Les micro-interactions confirment chaque action utilisateur
```

```
Anti-patterns à éviter
──────────────────────────────────────────────────────────────────
❌ Valider uniquement à la soumission → frustration, perte de données
❌ Empty state sans CTA → impasse, l'utilisateur ne sait pas quoi faire
❌ Skeleton avec forme différente du contenu réel → layout shift jarring
❌ Erreur générique "Une erreur est survenue" → l'utilisateur ne peut pas agir
❌ Onboarding obligatoire et non ignorable → abandon immédiat
❌ Bouton de soumission actif pendant le traitement → double-soumission
❌ Progressive disclosure cachant des informations critiques → frustration
❌ Navigation sans indicateur de position → désorientation
```

---

## Références

- `references/user-flows.md` — Cartographie des flux utilisateur, architecture de l'information, navigation React (Router v6, Next.js App Router), breadcrumbs, indicateurs de progression, recherche avec debounce, navigation mobile et deep links
- `references/onboarding.md` — Onboarding SaaS avancé (Product-led Growth, activation loops, email nurturing, tooltips contextuels), wizard multi-étapes, checklists gamifiées, métriques d'activation (time-to-value, activation rate)
- `references/conversion-ux.md` — CRO pour développeurs (audit de friction, form UX avec React Hook Form + Zod, checkout optimization, optimistic UI, trust signals, mobile conversion avec Payment Request API)
- `references/ux-patterns.md` — Bibliothèque de patterns UX : empty states, skeleton screens, toast notifications, confirmation dialogs, micro-interactions Framer Motion, error boundaries, progressive disclosure
