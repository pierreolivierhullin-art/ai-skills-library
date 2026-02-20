# Conversion Rate Optimization — Friction, Forms & Funnel Engineering

Référence technique approfondie sur l'optimisation du taux de conversion (CRO) côté engineering : audit de friction, UX de formulaires, flows d'inscription et de checkout, instrumentation, UI optimiste et signaux de confiance.

Deep technical reference for conversion rate optimization from the engineering perspective: friction audit, form UX, sign-up and checkout flows, instrumentation, optimistic UI, and trust signals.

---

## Table of Contents

1. [Friction Audit — Identifier les Points de Friction](#friction-audit)
2. [Form UX — Validation, Défauts & Autocomplete](#form-ux)
3. [Checkout Flow Optimization](#checkout-flow)
4. [Sign-up Flow Optimization](#signup-flow)
5. [CTA Design — États, Loading & Accessibilité](#cta-design)
6. [Instrumentation du Funnel de Conversion](#funnel-instrumentation)
7. [Optimistic UI — Feedback Immédiat](#optimistic-ui)
8. [Progressive Disclosure](#progressive-disclosure)
9. [Trust Signals — Implémentation Technique](#trust-signals)
10. [Mobile Conversion — Thumb Zone & Paiements Natifs](#mobile-conversion)

---

## 1. Friction Audit — Identifier les Points de Friction {#friction-audit}

### Qu'est-ce que la friction en UX ?

La friction est tout ce qui ralentit ou décourage un utilisateur entre son intention et la complétion de l'objectif. Elle se manifeste à trois niveaux : cognitif (trop d'information à traiter), moteur (trop d'étapes ou d'actions) et émotionnel (méfiance, anxiété).

**Métriques clés à mesurer en permanence :**
- **Drop-off rate par étape** : pourcentage d'utilisateurs qui abandonnent à chaque étape du funnel
- **Time on form** : temps passé sur un formulaire — au-delà de 3 min pour un formulaire simple, suspect
- **Field error rate** : taux d'erreur par champ — un taux > 15% indique une mauvaise validation ou un label ambigu
- **Rage clicks** : clics répétés sur un élément — souvent symptôme d'un bouton non réactif ou d'une redirection inattendue
- **Scroll depth** : jusqu'où les utilisateurs scrollent sur une landing page avant de partir

### Audit de charge cognitive

Évalue chaque écran avec la règle des 3 questions de Steve Krug : un utilisateur doit pouvoir répondre en moins de 5 secondes à (1) Où suis-je ?, (2) Que puis-je faire ici ?, (3) Où dois-je aller ensuite ?

**Checklist technique pour l'audit :**
- [ ] Nombre de champs par formulaire — supprimer tout champ non indispensable (chaque champ supplémentaire réduit la complétion de ~5%)
- [ ] Nombre de choix dans les menus déroulants — limiter à 7 options max (loi de Hick)
- [ ] Présence d'un "inscription obligatoire" pour accéder au produit — privilégier le guest checkout ou le try-before-register
- [ ] Labels ambigus — tester avec 5 utilisateurs non initiés
- [ ] Messages d'erreur génériques ("Erreur") vs. actionables ("Ton email est déjà utilisé — connecte-toi plutôt")
- [ ] Présence de CAPTCHA — chaque CAPTCHA coûte ~10% de conversions

### Outils d'audit recommendés

| Outil | Usage | Coût |
|---|---|---|
| Hotjar / Microsoft Clarity | Heatmaps, session recordings, rage clicks | Freemium |
| FullStory | Session replay avec search on events | Payant |
| Google Analytics 4 | Funnel exploration, drop-off rates | Gratuit |
| Datadog RUM | Real User Monitoring, error tracking | Payant |
| UserTesting | Tests utilisateurs qualitatifs | Payant |

---

## 2. Form UX — Validation, Défauts & Autocomplete {#form-ux}

### Ordre des champs et defaults intelligents

Place les champs dans l'ordre de résistance croissante. Commence par ce qui est facile (email, prénom), termine par ce qui est sensible (téléphone, adresse). Ne demande jamais plus que ce dont tu as besoin au moment T.

**Règles d'or pour les formulaires :**
1. **Un seul champ par ligne** — la complétion augmente de 15% en layout colonne unique vs. multi-colonnes
2. **Labels au-dessus, pas à l'intérieur** — les placeholders disparaissent à la saisie et créent de la confusion
3. **Validation inline, pas au submit** — l'utilisateur doit savoir immédiatement si un champ est valide
4. **Formats permissifs** — accepte `06 12 34 56 78`, `0612345678` et `+33612345678` pour un numéro de téléphone
5. **Autofill natif** — toujours utiliser les attributs `autocomplete` HTML5 corrects

### Formulaire avec validation inline — React Hook Form + Zod

```typescript
// components/forms/RegisterForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useState } from 'react';

const registerSchema = z.object({
  email: z
    .string()
    .min(1, 'L\'email est requis')
    .email('Format d\'email invalide'),
  password: z
    .string()
    .min(8, 'Minimum 8 caractères')
    .regex(/[A-Z]/, 'Au moins une majuscule')
    .regex(/[0-9]/, 'Au moins un chiffre'),
  firstName: z.string().min(2, 'Prénom trop court').max(50),
  phone: z
    .string()
    .optional()
    .refine(
      (val) => !val || /^(\+33|0)[1-9](\d{8})$/.test(val.replace(/\s/g, '')),
      { message: 'Numéro de téléphone invalide' }
    ),
});

type RegisterFormData = z.infer<typeof registerSchema>;

interface FieldFeedbackProps {
  error?: string;
  isDirty: boolean;
  isValid: boolean;
  children: React.ReactNode;
  errorId?: string; // pour lier aria-describedby de l'input au message d'erreur
}

// Composant réutilisable pour l'état visuel d'un champ
function FieldFeedback({ error, isDirty, isValid, children, errorId }: FieldFeedbackProps) {
  return (
    <div className="relative">
      {children}
      {/* Icône d'état inline — ne pas utiliser uniquement la couleur */}
      {isDirty && (
        <span
          className={`absolute right-3 top-1/2 -translate-y-1/2 text-sm ${
            isValid ? 'text-green-600' : 'text-red-600'
          }`}
          aria-hidden="true"
        >
          {isValid ? '✓' : '✗'}
        </span>
      )}
      {error && (
        <p id={errorId} role="alert" className="mt-1 text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}

export function RegisterForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, dirtyFields, touchedFields, isSubmitting },
    watch,
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    mode: 'onBlur',         // Valide au blur, pas à chaque keystroke
    reValidateMode: 'onChange', // Re-valide en temps réel après la première erreur
  });

  const onSubmit = async (data: RegisterFormData) => {
    await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      {/* Email en premier — c'est l'identifiant principal */}
      <div className="space-y-4">
        <label htmlFor="email" className="block text-sm font-medium">
          Email <span aria-label="requis">*</span>
        </label>
        <FieldFeedback
          error={errors.email?.message}
          isDirty={!!dirtyFields.email}
          isValid={!errors.email && !!dirtyFields.email}
          errorId="email-error"
        >
          <input
            id="email"
            type="email"
            autoComplete="email"
            inputMode="email"
            aria-invalid={!!errors.email}
            aria-describedby={errors.email ? 'email-error' : undefined}
            className={`w-full rounded-md border px-3 py-2 ${
              errors.email ? 'border-red-500' : 'border-gray-300'
            }`}
            {...register('email')}
          />
        </FieldFeedback>

        {/* Prénom avant nom — plus humain, réduit la résistance */}
        <label htmlFor="firstName" className="block text-sm font-medium">
          Prénom <span aria-label="requis">*</span>
        </label>
        <FieldFeedback
          error={errors.firstName?.message}
          isDirty={!!dirtyFields.firstName}
          isValid={!errors.firstName && !!dirtyFields.firstName}
        >
          <input
            id="firstName"
            type="text"
            autoComplete="given-name"
            aria-invalid={!!errors.firstName}
            className="w-full rounded-md border border-gray-300 px-3 py-2"
            {...register('firstName')}
          />
        </FieldFeedback>

        {/* Mot de passe — avec indicateur de force */}
        <label htmlFor="password" className="block text-sm font-medium">
          Mot de passe <span aria-label="requis">*</span>
        </label>
        <FieldFeedback
          error={errors.password?.message}
          isDirty={!!dirtyFields.password}
          isValid={!errors.password && !!dirtyFields.password}
        >
          <input
            id="password"
            type="password"
            autoComplete="new-password"
            aria-invalid={!!errors.password}
            className="w-full rounded-md border border-gray-300 px-3 py-2"
            {...register('password')}
          />
        </FieldFeedback>

        {/* Téléphone optionnel — clairement indiqué */}
        <label htmlFor="phone" className="block text-sm font-medium">
          Téléphone <span className="text-gray-500 font-normal">(optionnel)</span>
        </label>
        <FieldFeedback
          error={errors.phone?.message}
          isDirty={!!dirtyFields.phone}
          isValid={!errors.phone && !!dirtyFields.phone}
        >
          <input
            id="phone"
            type="tel"
            autoComplete="tel"
            inputMode="tel"
            placeholder="+33 6 12 34 56 78"
            className="w-full rounded-md border border-gray-300 px-3 py-2"
            {...register('phone')}
          />
        </FieldFeedback>
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="mt-6 w-full rounded-md bg-blue-600 py-2.5 text-white disabled:opacity-60"
      >
        {isSubmitting ? 'Création du compte...' : 'Créer mon compte'}
      </button>
    </form>
  );
}
```

### Attributs `autocomplete` essentiels

```html
<!-- Toujours spécifier autocomplete pour activer l'autofill navigateur -->
<input autocomplete="email" />
<input autocomplete="given-name" />
<input autocomplete="family-name" />
<input autocomplete="tel" />
<input autocomplete="new-password" />
<input autocomplete="current-password" />
<input autocomplete="street-address" />
<input autocomplete="postal-code" />
<input autocomplete="cc-number" />
<input autocomplete="cc-exp" />
<input autocomplete="cc-csc" />
```

L'autofill correctement configuré réduit le time-on-form de 30% à 50% sur mobile.

---

## 3. Checkout Flow Optimization {#checkout-flow}

### Guest Checkout — La priorité absolue

Force jamais l'inscription avant l'achat. Le guest checkout augmente les conversions de 30% à 45% (Baymard Institute). Propose l'inscription post-achat, quand l'utilisateur a déjà un contexte (son numéro de commande à sauvegarder).

**Architecture recommandée :**
1. Email → 2. Adresse → 3. Livraison → 4. Paiement → 5. Confirmation + invitation à créer un compte

### Address Autocomplete — Google Places API

```typescript
// hooks/useAddressAutocomplete.ts
import { useEffect, useRef, useState } from 'react';

interface ParsedAddress {
  street: string;
  city: string;
  postalCode: string;
  country: string;
}

function parseGooglePlace(place: google.maps.places.PlaceResult): ParsedAddress {
  const components = place.address_components ?? [];
  const get = (type: string) =>
    components.find((c) => c.types.includes(type))?.long_name ?? '';

  const streetNumber = get('street_number');
  const route = get('route');

  return {
    street: [streetNumber, route].filter(Boolean).join(' '),
    city: get('locality') || get('postal_town'),
    postalCode: get('postal_code'),
    country: components.find((c) => c.types.includes('country'))?.short_name ?? '',
  };
}

export function useAddressAutocomplete(
  inputRef: React.RefObject<HTMLInputElement>,
  onSelect: (address: ParsedAddress) => void
) {
  const autocompleteRef = useRef<google.maps.places.Autocomplete | null>(null);

  useEffect(() => {
    if (!inputRef.current || !window.google) return;

    autocompleteRef.current = new google.maps.places.Autocomplete(inputRef.current, {
      types: ['address'],
      componentRestrictions: { country: ['fr', 'be', 'ch'] },
      fields: ['address_components', 'formatted_address'],
    });

    const listener = autocompleteRef.current.addListener('place_changed', () => {
      const place = autocompleteRef.current!.getPlace();
      if (place.address_components) {
        onSelect(parseGooglePlace(place));
      }
    });

    return () => {
      google.maps.event.removeListener(listener);
    };
  }, [inputRef, onSelect]);
}

// Utilisation dans le formulaire de checkout
function CheckoutAddressForm() {
  const inputRef = useRef<HTMLInputElement>(null);
  const { setValue } = useFormContext();

  useAddressAutocomplete(inputRef, (address) => {
    setValue('street', address.street, { shouldValidate: true });
    setValue('city', address.city, { shouldValidate: true });
    setValue('postalCode', address.postalCode, { shouldValidate: true });
    // Remplissage automatique de tous les champs — réduit les erreurs de saisie
  });

  return (
    <input
      ref={inputRef}
      type="text"
      placeholder="Commence à taper ton adresse..."
      autoComplete="street-address"
    />
  );
}
```

### Mémorisation des moyens de paiement

Utilise Stripe `PaymentElement` avec `setup_future_usage: 'off_session'` pour tokeniser la carte. À la prochaine visite, propose un one-click avec les derniers 4 chiffres affichés. Couplé à une CVV re-demandée pour la sécurité, ce pattern augmente les conversions en repeat purchase de 40%.

---

## 4. Sign-up Flow Optimization {#signup-flow}

### Formulaire multi-étapes avec tracking

Divise un long formulaire d'inscription en étapes progressives. Chaque étape doit avoir un objectif unique et prendre moins de 30 secondes à compléter.

```typescript
// components/forms/MultiStepSignup.tsx
import { useState, useCallback } from 'react';
import { track } from '@/lib/analytics';

type Step = 'email' | 'profile' | 'preferences' | 'confirmation';

const STEPS: Step[] = ['email', 'profile', 'preferences', 'confirmation'];

interface StepProgressProps {
  current: Step;
  steps: Step[];
}

function StepProgress({ current, steps }: StepProgressProps) {
  const currentIndex = steps.indexOf(current);

  return (
    <nav aria-label="Étapes d'inscription">
      <ol className="flex items-center gap-2">
        {steps.map((step, index) => {
          const isCompleted = index < currentIndex;
          const isCurrent = step === current;

          return (
            <li key={step} className="flex items-center gap-2">
              <span
                className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium ${
                  isCompleted
                    ? 'bg-green-600 text-white'
                    : isCurrent
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-500'
                }`}
                aria-current={isCurrent ? 'step' : undefined}
              >
                {isCompleted ? '✓' : index + 1}
              </span>
              {index < steps.length - 1 && (
                <span
                  className={`h-0.5 w-8 ${isCompleted ? 'bg-green-600' : 'bg-gray-200'}`}
                  aria-hidden="true"
                />
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

export function MultiStepSignup() {
  const [currentStep, setCurrentStep] = useState<Step>('email');
  const [formData, setFormData] = useState<Record<string, unknown>>({});
  const [stepStartTime, setStepStartTime] = useState(Date.now());

  const handleStepComplete = useCallback(
    (stepData: Record<string, unknown>) => {
      const timeSpent = Date.now() - stepStartTime;

      // Tracking de chaque étape — essentiel pour identifier les abandons
      track('signup_step_completed', {
        step: currentStep,
        step_index: STEPS.indexOf(currentStep),
        time_spent_ms: timeSpent,
      });

      const mergedData = { ...formData, ...stepData };
      setFormData(mergedData);

      const nextIndex = STEPS.indexOf(currentStep) + 1;
      if (nextIndex < STEPS.length) {
        const nextStep = STEPS[nextIndex];
        setCurrentStep(nextStep);
        setStepStartTime(Date.now());

        // Tracking de la vue de l'étape suivante
        track('signup_step_viewed', {
          step: nextStep,
          step_index: nextIndex,
        });
      }
    },
    [currentStep, formData, stepStartTime]
  );

  const handleStepBack = useCallback(() => {
    const prevIndex = STEPS.indexOf(currentStep) - 1;
    if (prevIndex >= 0) {
      track('signup_step_back', { from_step: currentStep });
      setCurrentStep(STEPS[prevIndex]);
    }
  }, [currentStep]);

  return (
    <div className="mx-auto max-w-md space-y-8">
      <StepProgress current={currentStep} steps={STEPS} />

      {/* Rendu conditionnel de l'étape courante */}
      {currentStep === 'email' && (
        <EmailStep onComplete={handleStepComplete} />
      )}
      {currentStep === 'profile' && (
        <ProfileStep onComplete={handleStepComplete} onBack={handleStepBack} />
      )}
      {currentStep === 'preferences' && (
        <PreferencesStep onComplete={handleStepComplete} onBack={handleStepBack} />
      )}
      {currentStep === 'confirmation' && (
        <ConfirmationStep data={formData} />
      )}
    </div>
  );
}
```

### Progressive Profiling — Ne pas tout demander d'un coup

Collecte l'information en plusieurs sessions. À l'inscription, demande uniquement l'email. Lors de la première utilisation, demande le prénom. Après la 3ème session, demande le rôle ou l'entreprise. Cette technique augmente les taux d'activation de 25% car elle réduit le ticket d'entrée.

### Social Login & Magic Link

```typescript
// Implémentation avec NextAuth.js
// pages/api/auth/[...nextauth].ts
import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';
import EmailProvider from 'next-auth/providers/email';

export default NextAuth({
  providers: [
    // Social login — zéro friction, un clic
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    // Magic link — pas de mot de passe à mémoriser
    EmailProvider({
      server: process.env.EMAIL_SERVER,
      from: process.env.EMAIL_FROM,
      // Personnalise l'email pour augmenter le taux d'ouverture
      sendVerificationRequest: async ({ identifier, url, provider }) => {
        await sendMagicLinkEmail({ to: identifier, url });
      },
    }),
  ],
  callbacks: {
    async signIn({ user, account }) {
      // Track l'origine de l'inscription
      await track('user_signed_up', {
        method: account?.provider,
        email: user.email,
      });
      return true;
    },
  },
});
```

---

## 5. CTA Design — États, Loading & Accessibilité {#cta-design}

### Composant Button complet avec tous les états

```typescript
// components/ui/Button.tsx
import { forwardRef, ButtonHTMLAttributes } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  // Base — toujours présente
  [
    'inline-flex items-center justify-center gap-2',
    'rounded-md font-medium transition-all duration-150',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2',
    'disabled:pointer-events-none disabled:opacity-50',
    // Touch target minimum 44x44px (WCAG 2.5.5)
    'min-h-[44px] min-w-[44px] px-4 py-2',
  ],
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800',
        secondary: 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 active:bg-gray-100',
        destructive: 'bg-red-600 text-white hover:bg-red-700',
        ghost: 'text-gray-700 hover:bg-gray-100',
      },
      size: {
        sm: 'min-h-[36px] px-3 text-sm',
        md: 'min-h-[44px] px-4',
        lg: 'min-h-[52px] px-6 text-lg',
      },
    },
    defaultVariants: { variant: 'primary', size: 'md' },
  }
);

type ButtonState = 'idle' | 'loading' | 'success' | 'error';

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  state?: ButtonState;
  loadingText?: string;
  successText?: string;
  errorText?: string;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      state = 'idle',
      loadingText = 'Chargement...',
      successText = 'Succès !',
      errorText = 'Réessayer',
      variant,
      size,
      disabled,
      className,
      ...props
    },
    ref
  ) => {
    const isLoading = state === 'loading';
    const isSuccess = state === 'success';
    const isError = state === 'error';

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        // aria-busy signale aux screen readers que l'action est en cours
        aria-busy={isLoading}
        // aria-live pour annoncer les changements d'état
        aria-live="polite"
        className={buttonVariants({ variant: isError ? 'destructive' : variant, size, className })}
        {...props}
      >
        {isLoading && (
          <svg
            className="h-4 w-4 animate-spin"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
        )}
        {isSuccess && <span aria-hidden="true">✓</span>}
        {isError && <span aria-hidden="true">⚠</span>}

        <span>
          {isLoading ? loadingText : isSuccess ? successText : isError ? errorText : children}
        </span>
      </button>
    );
  }
);

Button.displayName = 'Button';

// Utilisation avec gestion d'état automatique
function SubmitButton({ onSubmit }: { onSubmit: () => Promise<void> }) {
  const [state, setState] = useState<ButtonState>('idle');

  const handleClick = async () => {
    setState('loading');
    try {
      await onSubmit();
      setState('success');
      // Retour à l'état idle après le feedback de succès
      setTimeout(() => setState('idle'), 2000);
    } catch {
      setState('error');
      setTimeout(() => setState('idle'), 3000);
    }
  };

  return (
    <Button
      state={state}
      onClick={handleClick}
      loadingText="Envoi en cours..."
      successText="Message envoyé !"
      errorText="Échec — Réessayer"
    >
      Envoyer
    </Button>
  );
}
```

**Impact mesurable des états de bouton :**
- Loading state visible → réduit les double-soumissions de 70%
- Success feedback (2s) → augmente la satisfaction perçue de 30%
- Error state actionable → augmente le retry rate de 45%

---

## 6. Instrumentation du Funnel de Conversion {#funnel-instrumentation}

### Architecture d'events pour un funnel e-commerce

```typescript
// lib/conversion-tracking.ts
import { analytics } from './analytics-client';

// Typage strict des events — prévient les erreurs de nommage
type FunnelEvent =
  | { name: 'page_viewed'; properties: { page: string; referrer?: string } }
  | { name: 'product_viewed'; properties: { product_id: string; price: number; category: string } }
  | { name: 'add_to_cart'; properties: { product_id: string; quantity: number; price: number } }
  | { name: 'checkout_started'; properties: { cart_value: number; item_count: number } }
  | { name: 'checkout_step_completed'; properties: { step: number; step_name: string } }
  | { name: 'payment_info_entered'; properties: { method: string } }
  | { name: 'order_completed'; properties: { order_id: string; revenue: number; currency: string } };

export function trackFunnelEvent(event: FunnelEvent) {
  analytics.track(event.name, {
    ...event.properties,
    timestamp: new Date().toISOString(),
    session_id: getSessionId(),
    // Propriétés contextuelles automatiques
    page_url: window.location.href,
    device_type: getDeviceType(),
  });
}

// Hook React pour le tracking de vue de page
export function usePageTracking(page: string) {
  useEffect(() => {
    trackFunnelEvent({
      name: 'page_viewed',
      properties: { page, referrer: document.referrer || undefined },
    });
  }, [page]);
}

// Mesure du temps passé entre deux étapes
export class FunnelTimer {
  private startTimes = new Map<string, number>();

  start(step: string) {
    this.startTimes.set(step, performance.now());
  }

  complete(step: string): number {
    const start = this.startTimes.get(step) ?? performance.now();
    return Math.round(performance.now() - start);
  }
}

// Détection des abandons de formulaire
export function useFormAbandonTracking(formId: string) {
  const hasInteracted = useRef(false);

  useEffect(() => {
    const handleInteraction = () => {
      hasInteracted.current = true;
    };

    const form = document.getElementById(formId);
    form?.addEventListener('input', handleInteraction, { once: true });

    return () => {
      // Cleanup = utilisateur quitte sans compléter
      if (hasInteracted.current) {
        trackFunnelEvent({
          name: 'checkout_started', // Adapte selon le funnel
          properties: { cart_value: 0, item_count: 0 },
        });
      }
    };
  }, [formId]);
}
```

### Dashboard de monitoring de funnel

Configure des alertes automatiques sur ces seuils :
- Drop-off à l'étape email > 60% → problème de confiance ou de formulaire
- Drop-off à l'étape paiement > 30% → problème technique ou de confiance
- Temps moyen sur le checkout > 5 min → trop de champs ou erreurs fréquentes

---

## 7. Optimistic UI — Feedback Immédiat {#optimistic-ui}

### Pattern avec React Query

L'UI optimiste affiche le résultat immédiatement, avant la confirmation serveur. Elle réduit la latence perçue de 200-500ms et augmente la satisfaction utilisateur, au prix d'une gestion de rollback en cas d'erreur.

```typescript
// hooks/useOptimisticLike.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface Post {
  id: string;
  likeCount: number;
  isLiked: boolean;
}

export function useOptimisticLike(postId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (newLikedState: boolean) => {
      const response = await fetch(`/api/posts/${postId}/like`, {
        method: newLikedState ? 'POST' : 'DELETE',
      });
      if (!response.ok) throw new Error('Like failed');
      return response.json();
    },

    onMutate: async (newLikedState: boolean) => {
      // 1. Annule les queries en cours pour éviter les conflits
      await queryClient.cancelQueries({ queryKey: ['post', postId] });

      // 2. Snapshot de l'état précédent pour le rollback
      const previousPost = queryClient.getQueryData<Post>(['post', postId]);

      // 3. Mise à jour optimiste immédiate — l'UI répond instantanément
      queryClient.setQueryData<Post>(['post', postId], (old) => {
        if (!old) return old;
        return {
          ...old,
          isLiked: newLikedState,
          likeCount: old.likeCount + (newLikedState ? 1 : -1),
        };
      });

      return { previousPost };
    },

    onError: (error, newLikedState, context) => {
      // Rollback en cas d'erreur — revient à l'état précédent
      if (context?.previousPost) {
        queryClient.setQueryData(['post', postId], context.previousPost);
      }
      // Notifie l'utilisateur de l'échec
      toast.error('Action impossible pour le moment. Réessaie plus tard.');
    },

    onSettled: () => {
      // Revalide depuis le serveur après mutation (succès ou échec)
      queryClient.invalidateQueries({ queryKey: ['post', postId] });
    },
  });
}

// Composant utilisant le hook
function LikeButton({ postId }: { postId: string }) {
  const { data: post } = useQuery({ queryKey: ['post', postId], queryFn: fetchPost });
  const { mutate: toggleLike, isPending } = useOptimisticLike(postId);

  return (
    <button
      onClick={() => toggleLike(!post?.isLiked)}
      aria-pressed={post?.isLiked}
      aria-label={post?.isLiked ? 'Retirer le like' : 'Liker'}
      // Pas de disabled — l'UI optimiste permet d'ignorer le isPending
      className={`flex items-center gap-1 ${post?.isLiked ? 'text-red-500' : 'text-gray-500'}`}
    >
      <span aria-hidden="true">{post?.isLiked ? '♥' : '♡'}</span>
      <span>{post?.likeCount}</span>
    </button>
  );
}
```

---

## 8. Progressive Disclosure {#progressive-disclosure}

### Masquer la complexité par défaut

Montre les options avancées uniquement quand l'utilisateur en a besoin. Ce pattern réduit la charge cognitive initiale et améliore les taux de complétion des formulaires de 20% à 35%.

```typescript
// components/ui/AdvancedOptions.tsx
import { useState } from 'react';

interface AdvancedOptionsProps {
  children: React.ReactNode;
  label?: string;
  defaultOpen?: boolean;
}

export function AdvancedOptions({
  children,
  label = 'Options avancées',
  defaultOpen = false,
}: AdvancedOptionsProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const contentId = useId();

  return (
    <div className="mt-4 border-t pt-4">
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        aria-expanded={isOpen}
        aria-controls={contentId}
        className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
      >
        <span
          className={`transition-transform duration-200 ${isOpen ? 'rotate-90' : ''}`}
          aria-hidden="true"
        >
          ▶
        </span>
        {label}
      </button>

      {/* Animation CSS — évite les recalculs JS de hauteur */}
      <div
        id={contentId}
        className={`overflow-hidden transition-all duration-300 ${
          isOpen ? 'max-h-[1000px] opacity-100' : 'max-h-0 opacity-0'
        }`}
        aria-hidden={!isOpen}
      >
        <div className="pt-4">{children}</div>
      </div>
    </div>
  );
}

// Exemple d'utilisation dans un formulaire de paiement
function PaymentForm() {
  return (
    <form>
      {/* Options essentielles — toujours visibles */}
      <CardNumberField />
      <ExpiryAndCVCFields />

      {/* Options avancées — masquées par défaut */}
      <AdvancedOptions label="Facturation & options fiscales">
        <CompanyNameField />
        <VATNumberField />
        <BillingAddressDifferent />
      </AdvancedOptions>
    </form>
  );
}
```

---

## 9. Trust Signals — Implémentation Technique {#trust-signals}

### Positionnement stratégique des signaux de confiance

Place les trust signals au plus près du point de décision : juste au-dessus du bouton "Acheter" ou "S'inscrire", et dans le footer du formulaire de paiement.

```typescript
// components/conversion/TrustBadges.tsx
interface TrustBadgeProps {
  context: 'checkout' | 'signup' | 'landing';
}

export function TrustBadges({ context }: TrustBadgeProps) {
  return (
    <div
      className="flex flex-wrap items-center justify-center gap-4 py-3"
      aria-label="Garanties et sécurité"
    >
      {/* Badge SSL — toujours présent */}
      <div className="flex items-center gap-1.5 text-sm text-gray-600">
        <svg aria-hidden="true" className="h-4 w-4 text-green-600">
          {/* Icône cadenas */}
        </svg>
        <span>Connexion sécurisée SSL</span>
      </div>

      {/* Badges contextuels */}
      {context === 'checkout' && (
        <>
          <div className="flex items-center gap-1.5 text-sm text-gray-600">
            <span aria-hidden="true">↩</span>
            <span>Retour gratuit 30 jours</span>
          </div>
          <div className="flex items-center gap-1.5 text-sm text-gray-600">
            <span aria-hidden="true">🛡</span>
            <span>Paiement sécurisé Stripe</span>
          </div>
        </>
      )}

      {context === 'signup' && (
        <div className="flex items-center gap-1.5 text-sm text-gray-600">
          <span aria-hidden="true">✉</span>
          <span>Sans carte bancaire — annulable à tout moment</span>
        </div>
      )}
    </div>
  );
}

// Widget d'avis — chargement lazy pour ne pas bloquer le LCP
function ReviewWidget({ productId }: { productId: string }) {
  const { data: reviews, isLoading } = useQuery({
    queryKey: ['reviews', productId],
    queryFn: () => fetchReviews(productId),
    // Ne bloque pas le rendu initial
    placeholderData: { average: 4.8, count: 1243, recent: [] },
  });

  return (
    <div className="flex items-center gap-2" aria-label={`Note: ${reviews?.average} sur 5`}>
      <StarRating value={reviews?.average ?? 0} readonly />
      <span className="text-sm font-medium">{reviews?.average?.toFixed(1)}</span>
      <span className="text-sm text-gray-500">({reviews?.count?.toLocaleString('fr-FR')} avis)</span>
    </div>
  );
}
```

### Social Proof — Counter en temps réel

```typescript
// Afficher "X personnes regardent cet article" — crée l'urgence
function LiveViewerCount({ productId }: { productId: string }) {
  const [count, setCount] = useState<number | null>(null);

  useEffect(() => {
    // WebSocket ou SSE pour les updates en temps réel
    const eventSource = new EventSource(`/api/products/${productId}/viewers`);
    eventSource.onmessage = (e) => setCount(JSON.parse(e.data).count);
    return () => eventSource.close();
  }, [productId]);

  if (!count || count < 3) return null; // N'affiche pas si pas assez de preuves sociales

  return (
    <p className="text-sm text-orange-700" aria-live="polite">
      <span aria-hidden="true">👁</span> {count} personnes regardent cet article en ce moment
    </p>
  );
}
```

---

## 10. Mobile Conversion — Thumb Zone & Paiements Natifs {#mobile-conversion}

### Thumb Zone — Design pour la zone de confort du pouce

Sur un smartphone tenu à une main, 75% de l'écran est accessible sans déplacer la main. Place les CTAs principaux dans la zone inférieure centrale (la plus accessible). Évite de mettre des actions critiques dans les coins supérieurs.

```typescript
// Composant de barre d'actions mobile fixe en bas
function MobileCheckoutBar({ price, onCheckout }: { price: number; onCheckout: () => void }) {
  return (
    <div
      className={[
        // Positionné dans la thumb zone inférieure
        'fixed bottom-0 left-0 right-0 z-50',
        'bg-white border-t border-gray-200 p-4',
        // Safe area pour les iPhones avec home indicator
        'pb-[calc(1rem+env(safe-area-inset-bottom))]',
      ].join(' ')}
    >
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-lg font-bold">{formatPrice(price)}</p>
          <p className="text-xs text-gray-500">Livraison gratuite</p>
        </div>
        <button
          onClick={onCheckout}
          // Touch target minimum 44x44px — idéalement 48x48px sur mobile
          className="flex-1 rounded-lg bg-blue-600 py-3.5 text-white font-medium text-base min-h-[48px]"
        >
          Commander
        </button>
      </div>
    </div>
  );
}
```

### Apple Pay & Google Pay — Payment Request API

```typescript
// hooks/useNativePayment.ts
export function useNativePayment() {
  const [isAvailable, setIsAvailable] = useState(false);

  useEffect(() => {
    // Détecte si le navigateur supporte les paiements natifs
    if (window.PaymentRequest) {
      const request = new PaymentRequest(
        [{ supportedMethods: 'https://apple.com/apple-pay' },
         { supportedMethods: 'https://google.com/pay' }],
        { total: { label: 'Total', amount: { currency: 'EUR', value: '0' } } }
      );
      request.canMakePayment().then(setIsAvailable);
    }
  }, []);

  const requestPayment = async (amount: number, description: string) => {
    // Délègue à Stripe qui gère Apple Pay et Google Pay uniformément
    const stripe = await loadStripe(process.env.NEXT_PUBLIC_STRIPE_KEY!);
    const elements = stripe!.elements();
    const paymentElement = elements.create('payment', {
      // Stripe détecte automatiquement Apple Pay / Google Pay
      wallets: { applePay: 'auto', googlePay: 'auto' },
    });
    // ... mount et confirmation
  };

  return { isAvailable, requestPayment };
}

// Bouton conditionnel — Apple Pay si disponible, sinon checkout classique
function CheckoutButton({ price }: { price: number }) {
  const { isAvailable, requestPayment } = useNativePayment();

  if (isAvailable) {
    return (
      <button
        onClick={() => requestPayment(price, 'Commande')}
        className="w-full rounded-lg bg-black py-3.5 text-white flex items-center justify-center gap-2 min-h-[48px]"
        aria-label="Payer avec Apple Pay"
      >
        {/* Logo Apple Pay — ne pas modifier le design officiel */}
        <ApplePayLogo aria-hidden="true" />
      </button>
    );
  }

  return (
    <button className="w-full rounded-lg bg-blue-600 py-3.5 text-white min-h-[48px]">
      Procéder au paiement
    </button>
  );
}
```

**Impact mesuré des paiements natifs mobiles :**
- Apple Pay vs. checkout traditionnel : +35% à +65% de conversion sur iOS (Apple, 2024)
- Réduction du temps de checkout de 3 min à 15 secondes
- Taux d'abandon mobile : 85% checkout classique → 40% avec paiement natif

---

## Métriques de Référence CRO

| Métrique | Benchmark moyen | Top Performer |
|---|---|---|
| Taux de conversion e-commerce | 2–4% | > 6% |
| Drop-off formulaire inscription | 60–70% | < 30% |
| Drop-off checkout (ajout panier → achat) | 65–85% | < 40% |
| Conversion avec guest checkout vs. inscription forcée | +25–45% | — |
| Conversion Apple Pay vs. carte classique (mobile) | +35–65% | — |
| Impact d'un champ supplémentaire dans un formulaire | -5% à -10% | — |
| Impact du CAPTCHA | -10% à -15% | — |

Utilise ces benchmarks comme seuils d'alerte dans tes dashboards, pas comme objectifs. Chaque produit a son propre profil d'utilisateurs — mesure ton contexte spécifique avec des A/B tests rigoureux avant de tirer des conclusions.
