# Onboarding, First-Run Experience & Activation

Référence complète pour concevoir et implémenter des flows d'onboarding efficaces : modèles d'onboarding, stratégie blank state, funnel d'activation, checklists gamifiées, tooltips, wizards multi-étapes et mesure du time-to-value. Complete reference for designing and implementing effective onboarding flows: onboarding models, blank state strategy, activation funnel, gamified checklists, tooltips, multi-step wizards, and time-to-value measurement.

---

## 1. Modèles d'Onboarding

### Choisir le bon modèle

Adapte le modèle d'onboarding à la complexité du produit et au profil de l'utilisateur.

| Modèle | Contexte | Avantages | Inconvénients |
|---|---|---|---|
| **Product Tour** | SaaS complexe, B2B | Couverture totale, guidé | Intrusif, abandons élevés |
| **Checklist** | Produits avec setup initial | Autonome, gamification | Peut sembler lourd |
| **Progressive** | Feature-rich, découverte graduelle | Naturel, non intrusif | Slow time-to-value |
| **Contextuel** | Produits avec UX complexe | Pertinent, au bon moment | Coordination difficile |
| **Blank State** | Outils de création, dashboards | Simple, direct | Peu de guidance |
| **Wizard** | Config obligatoire (SaaS, CRM) | Collecte données clés | Friction au démarrage |

**Règle d'or :** Ne pas combiner plus de deux modèles simultanément. L'onboarding le plus efficace est celui qui amène l'utilisateur à son premier succès le plus rapidement possible — pas celui qui lui montre le plus de fonctionnalités.

### Product Tour vs. Onboarding Contextuel

Le product tour linéaire (Intercom, Appcues) convient aux produits où l'utilisateur doit connaître le chemin complet avant de commencer. L'onboarding contextuel (tooltips déclenchés par des actions) est préférable quand l'utilisateur peut trouver de la valeur sans avoir tout vu.

**Critère décisif :** Si un utilisateur peut accomplir son premier succès sans connaître 80 % des fonctionnalités, utilise l'onboarding contextuel. Sinon, opte pour un product tour court (5 étapes maximum).

---

## 2. First-Run Experience & Blank State

### Stratégie Blank State

Le blank state est le premier écran qu'un utilisateur voit dans un contexte vide. C'est une opportunité, pas un problème.

**Les trois types de blank state :**

1. **Blank state initial** — premier accès, aucune donnée. Objectif : démontrer la valeur promise et déclencher la première action.
2. **Blank state de recherche/filtre** — aucun résultat. Objectif : aider l'utilisateur à réessayer.
3. **Blank state de succès** — tâche complétée, liste vidée. Objectif : célébrer et proposer la suite.

**Règles pour le blank state initial :**
- Affiche toujours une **illustration** ou un visuel qui représente l'état futur (montre ce que le produit ressemblera une fois rempli).
- Inclus un **call-to-action primaire** unique et clair.
- Propose optionnellement des **données de démo** ou un exemple importable.
- Explique le **bénéfice** (ce que l'utilisateur va gagner), pas la fonctionnalité.

```tsx
// BlankState component — initial empty state
interface BlankStateProps {
  title: string;
  description: string;
  illustration?: React.ReactNode;
  primaryAction: {
    label: string;
    onClick: () => void;
  };
  secondaryAction?: {
    label: string;
    onClick: () => void;
  };
}

function BlankState({
  title,
  description,
  illustration,
  primaryAction,
  secondaryAction,
}: BlankStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-8 text-center max-w-md mx-auto">
      {illustration && (
        <div className="mb-6 text-muted-foreground" aria-hidden="true">
          {illustration}
        </div>
      )}
      <h2 className="text-xl font-semibold text-foreground mb-2">{title}</h2>
      <p className="text-sm text-muted-foreground mb-8 leading-relaxed">{description}</p>
      <div className="flex flex-col sm:flex-row gap-3">
        <button
          onClick={primaryAction.onClick}
          className="btn btn-primary"
        >
          {primaryAction.label}
        </button>
        {secondaryAction && (
          <button
            onClick={secondaryAction.onClick}
            className="btn btn-secondary"
          >
            {secondaryAction.label}
          </button>
        )}
      </div>
    </div>
  );
}

// Usage — Dashboard blank state
function ProjectsBlankState() {
  const { startOnboarding } = useOnboarding();
  return (
    <BlankState
      title="Crée ton premier projet"
      description="Organise ton travail en projets. Invite ton équipe, assigne des tâches et suis la progression en temps réel."
      illustration={<ProjectsIllustration />}
      primaryAction={{
        label: "Créer un projet",
        onClick: () => startOnboarding("project-creation"),
      }}
      secondaryAction={{
        label: "Importer un exemple",
        onClick: () => importDemoProject(),
      }}
    />
  );
}
```

### Setup Wizard — Collecte des données clés

Utilise un wizard de setup quand le produit a besoin d'informations pour être personnalisé dès le départ. Garde-le court : 3-5 étapes maximum, chaque étape avec une seule question claire.

---

## 3. Funnel d'Activation & Moment "Aha"

### Définir le moment "Aha"

Le moment "Aha" est l'instant où l'utilisateur comprend concrètement la valeur du produit. Il est défini par une **action** observable, pas un sentiment.

**Exemples de moments "Aha" connus :**

| Produit | Moment "Aha" | Délai cible |
|---|---|---|
| **Slack** | Envoyer le premier message à un collègue | < 5 min |
| **Trello** | Déplacer une carte de "À faire" à "Terminé" | < 10 min |
| **GitHub** | Premier commit pushé | < 30 min |
| **Figma** | Partager un design en lien public | < 20 min |
| **Notion** | Créer et partager une page | < 15 min |

**Comment trouver ton moment "Aha" :**
1. Analyse les cohortes : quels utilisateurs restent actifs à J+30 ? Quelle action ont-ils accomplie dans les premières 24h que les churners n'ont pas faite ?
2. Formule une hypothèse : "Les utilisateurs qui [action] dans les [délai] ont [X]% de rétention à J+30."
3. Valide avec les données. Itère.

### Mesurer l'Activation

L'**activation rate** mesure le pourcentage d'utilisateurs inscrits qui ont atteint le moment "Aha" dans une fenêtre de temps définie.

```typescript
// Activation tracking — define and measure activation events
interface ActivationEvent {
  userId: string;
  event: string;
  properties?: Record<string, unknown>;
  timestamp: Date;
}

// Define activation milestones
const ACTIVATION_MILESTONES = {
  PROFILE_COMPLETED: "profile_completed",
  FIRST_PROJECT_CREATED: "project_created",
  FIRST_TEAM_MEMBER_INVITED: "team_member_invited",
  FIRST_TASK_COMPLETED: "task_completed", // <-- "Aha moment"
} as const;

// Track activation progress
async function trackActivation(
  userId: string,
  milestone: keyof typeof ACTIVATION_MILESTONES
) {
  const event = ACTIVATION_MILESTONES[milestone];

  // Send to analytics (Segment, Amplitude, Mixpanel)
  analytics.track(event, {
    userId,
    timestamp: new Date().toISOString(),
  });

  // Update activation progress in DB
  await db.user.update({
    where: { id: userId },
    data: {
      activationMilestones: {
        push: event,
      },
      activatedAt:
        milestone === "FIRST_TASK_COMPLETED" ? new Date() : undefined,
    },
  });
}

// Calculate activation rate for a cohort
async function getActivationRate(
  cohortStartDate: Date,
  cohortEndDate: Date
): Promise<number> {
  const [totalUsers, activatedUsers] = await Promise.all([
    db.user.count({
      where: { createdAt: { gte: cohortStartDate, lte: cohortEndDate } },
    }),
    db.user.count({
      where: {
        createdAt: { gte: cohortStartDate, lte: cohortEndDate },
        activatedAt: { not: null },
      },
    }),
  ]);
  return totalUsers > 0 ? activatedUsers / totalUsers : 0;
}
```

---

## 4. Onboarding Progressif & Feature Flags

### Révéler les Fonctionnalités Graduellement

L'onboarding progressif consiste à ne montrer les fonctionnalités avancées qu'une fois les fonctionnalités de base maîtrisées. Cela réduit la charge cognitive et augmente la rétention.

**Niveaux de déverrouillage :**
- **Niveau 1 (J0-J3)** — Fonctionnalités core, flux principal, premier succès.
- **Niveau 2 (J3-J14)** — Fonctionnalités de collaboration, intégrations basiques.
- **Niveau 3 (J14+)** — Fonctionnalités avancées, automatisations, analytics.

```tsx
// Progressive feature disclosure with feature flags
import { useFlags } from "@/lib/feature-flags";
import { useOnboardingProgress } from "@/hooks/useOnboardingProgress";

function NavigationMenu() {
  const flags = useFlags();
  const { level, completedMilestones } = useOnboardingProgress();

  return (
    <nav>
      {/* Always visible — core features */}
      <NavItem href="/dashboard" icon={<HomeIcon />} label="Tableau de bord" />
      <NavItem href="/projects" icon={<FolderIcon />} label="Projets" />

      {/* Level 2 — unlocked after first project created */}
      {level >= 2 && (
        <>
          <NavItem href="/team" icon={<UsersIcon />} label="Équipe" />
          <NavItem href="/integrations" icon={<PlugIcon />} label="Intégrations" />
        </>
      )}

      {/* Level 3 — unlocked after 14 days or specific actions */}
      {level >= 3 && (
        <>
          <NavItem href="/automations" icon={<ZapIcon />} label="Automatisations" />
          <NavItem href="/analytics" icon={<BarChartIcon />} label="Analytics" />
        </>
      )}

      {/* Feature flag — gradual rollout to % of users */}
      {flags.newReportingModule && (
        <NavItem
          href="/reports"
          icon={<FileTextIcon />}
          label="Rapports"
          badge="Nouveau"
        />
      )}
    </nav>
  );
}
```

### Feature Flags pour le Rollout Progressif

Utilise les feature flags pour déployer de nouvelles fonctionnalités à un sous-ensemble d'utilisateurs et les introduire via l'onboarding contextuel.

```typescript
// Feature flag service — lightweight implementation
interface FeatureFlag {
  key: string;
  enabled: boolean;
  rolloutPercentage: number; // 0-100
  userIds?: string[]; // Specific user overrides
}

function isFeatureEnabled(
  flag: FeatureFlag,
  userId: string
): boolean {
  // Explicit override
  if (flag.userIds?.includes(userId)) return true;
  if (!flag.enabled) return false;

  // Percentage-based rollout using consistent hashing
  const hash = cyrb53(userId + flag.key);
  const userPercentile = (hash % 100) + 1;
  return userPercentile <= flag.rolloutPercentage;
}

// Deterministic hash function (djb2 variant)
function cyrb53(str: string): number {
  let h1 = 0xdeadbeef, h2 = 0x41c6ce57;
  for (let i = 0; i < str.length; i++) {
    const ch = str.charCodeAt(i);
    h1 = Math.imul(h1 ^ ch, 2654435761);
    h2 = Math.imul(h2 ^ ch, 1597334677);
  }
  return 4294967296 * (2097151 & h2) + (h1 >>> 0);
}
```

---

## 5. Onboarding Checklists

### Checklist Gamifiée avec Progress Tracking

La checklist d'onboarding est l'un des patterns les plus efficaces pour guider l'activation. La barre de progression déclenche l'effet de "completion bias" — les utilisateurs ont plus envie de terminer une checklist à 60 % qu'à 0 %.

```tsx
// OnboardingChecklist component with progress tracking
interface ChecklistItem {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  action?: {
    label: string;
    href?: string;
    onClick?: () => void;
  };
  xpReward?: number; // Gamification points
}

interface OnboardingChecklistProps {
  items: ChecklistItem[];
  onDismiss?: () => void;
}

function OnboardingChecklist({ items, onDismiss }: OnboardingChecklistProps) {
  const completedCount = items.filter((i) => i.completed).length;
  const totalCount = items.length;
  const progressPercent = Math.round((completedCount / totalCount) * 100);
  const isCompleted = completedCount === totalCount;

  if (isCompleted) {
    return <ChecklistCompletedBanner onDismiss={onDismiss} />;
  }

  return (
    <div className="rounded-xl border border-border bg-card p-5 shadow-sm">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="font-semibold text-foreground">
            Mise en route ({completedCount}/{totalCount})
          </h3>
          <p className="text-xs text-muted-foreground mt-0.5">
            Complète ces étapes pour tirer le meilleur de l'outil.
          </p>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="text-muted-foreground hover:text-foreground"
            aria-label="Masquer la checklist"
          >
            <XIcon className="h-4 w-4" />
          </button>
        )}
      </div>

      {/* Progress bar */}
      <div
        role="progressbar"
        aria-valuenow={progressPercent}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`${progressPercent}% complété`}
        className="mb-4"
      >
        <div className="flex justify-between text-xs text-muted-foreground mb-1.5">
          <span>{progressPercent}% complété</span>
          <span>{totalCount - completedCount} étapes restantes</span>
        </div>
        <div className="h-2 rounded-full bg-muted overflow-hidden">
          <div
            className="h-full rounded-full bg-primary transition-all duration-500 ease-out"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Items */}
      <ul className="space-y-2">
        {items.map((item) => (
          <ChecklistItemRow key={item.id} item={item} />
        ))}
      </ul>
    </div>
  );
}

function ChecklistItemRow({ item }: { item: ChecklistItem }) {
  return (
    <li className={`flex items-start gap-3 p-2.5 rounded-lg transition-colors
      ${item.completed ? "opacity-60" : "hover:bg-muted/50"}`}
    >
      <div className={`mt-0.5 flex-shrink-0 h-5 w-5 rounded-full border-2 flex items-center justify-center
        ${item.completed
          ? "border-primary bg-primary text-primary-foreground"
          : "border-muted-foreground"
        }`}
      >
        {item.completed && <CheckIcon className="h-3 w-3" />}
      </div>
      <div className="flex-1 min-w-0">
        <p className={`text-sm font-medium ${item.completed ? "line-through" : ""}`}>
          {item.title}
        </p>
        {!item.completed && (
          <p className="text-xs text-muted-foreground mt-0.5">{item.description}</p>
        )}
      </div>
      {!item.completed && item.action && (
        <button
          onClick={item.action.onClick}
          className="text-xs text-primary font-medium flex-shrink-0 hover:underline"
        >
          {item.action.label} →
        </button>
      )}
      {item.xpReward && item.completed && (
        <span className="text-xs text-amber-600 font-medium flex-shrink-0">
          +{item.xpReward} XP
        </span>
      )}
    </li>
  );
}

// Dismissal patterns — persist user preference
function useChecklistDismissal(checklistId: string) {
  const [dismissed, setDismissed] = useState(() => {
    return localStorage.getItem(`checklist_dismissed_${checklistId}`) === "true";
  });

  const dismiss = () => {
    localStorage.setItem(`checklist_dismissed_${checklistId}`, "true");
    setDismissed(true);
    analytics.track("onboarding_checklist_dismissed", { checklistId });
  };

  return { dismissed, dismiss };
}
```

---

## 6. Tooltips & Coach Marks

### Pattern Tooltip Positionné

Implémente les tooltips de coach mark avec un calcul de position intelligent pour éviter les débordements de viewport.

```tsx
// CoachMark component — targeted tooltip for feature discovery
import { useFloating, offset, flip, shift, arrow } from "@floating-ui/react";
import { useRef, useEffect } from "react";

interface CoachMarkProps {
  targetRef: React.RefObject<HTMLElement>;
  title: string;
  description: string;
  step?: number;
  totalSteps?: number;
  onNext?: () => void;
  onPrev?: () => void;
  onDismiss: () => void;
  placement?: "top" | "bottom" | "left" | "right";
}

function CoachMark({
  targetRef,
  title,
  description,
  step,
  totalSteps,
  onNext,
  onPrev,
  onDismiss,
  placement = "bottom",
}: CoachMarkProps) {
  const arrowRef = useRef<HTMLDivElement>(null);

  const { refs, floatingStyles, context, middlewareData, placement: resolvedPlacement } =
    useFloating({
      placement,
      middleware: [
        offset(12),
        flip({ fallbackAxisSideDirection: "start" }),
        shift({ padding: 8 }),
        arrow({ element: arrowRef }),
      ],
    });

  // Attach floating ref to target element
  useEffect(() => {
    if (targetRef.current) {
      refs.setReference(targetRef.current);
    }
  }, [targetRef, refs]);

  // Highlight target element
  useEffect(() => {
    const target = targetRef.current;
    if (!target) return;
    target.style.position = "relative";
    target.style.zIndex = "1001";
    target.classList.add("coach-mark-target");
    return () => {
      target.style.position = "";
      target.style.zIndex = "";
      target.classList.remove("coach-mark-target");
    };
  }, [targetRef]);

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/40 z-[1000]"
        onClick={onDismiss}
        aria-hidden="true"
      />

      {/* Tooltip */}
      <div
        ref={refs.setFloating}
        style={floatingStyles}
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className="z-[1002] w-72 rounded-xl bg-popover border border-border shadow-xl p-4"
      >
        {/* Arrow */}
        <div
          ref={arrowRef}
          className="absolute h-2 w-2 rotate-45 bg-popover border-border"
          style={{
            left: middlewareData.arrow?.x,
            top: middlewareData.arrow?.y,
            [resolvedPlacement.startsWith("bottom") ? "top" : "bottom"]: -5,
          }}
        />

        {/* Step indicator */}
        {step && totalSteps && (
          <div className="flex gap-1 mb-3">
            {Array.from({ length: totalSteps }, (_, i) => (
              <div
                key={i}
                className={`h-1 flex-1 rounded-full ${
                  i < step ? "bg-primary" : "bg-muted"
                }`}
              />
            ))}
          </div>
        )}

        <h3 className="font-semibold text-sm text-popover-foreground mb-1">{title}</h3>
        <p className="text-xs text-muted-foreground mb-4 leading-relaxed">{description}</p>

        <div className="flex items-center justify-between">
          <button
            onClick={onDismiss}
            className="text-xs text-muted-foreground hover:text-foreground"
          >
            Ignorer
          </button>
          <div className="flex gap-2">
            {onPrev && (
              <button onClick={onPrev} className="btn btn-ghost btn-sm">
                Précédent
              </button>
            )}
            {onNext ? (
              <button onClick={onNext} className="btn btn-primary btn-sm">
                Suivant {step && totalSteps ? `(${step}/${totalSteps})` : ""}
              </button>
            ) : (
              <button onClick={onDismiss} className="btn btn-primary btn-sm">
                Compris
              </button>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
```

**Note sur les bibliothèques :** [Shepherd.js](https://shepherdjs.dev/) et [Intro.js](https://introjs.com/) sont des alternatives prêtes à l'emploi. Utilise-les pour des product tours complexes. Pour des coach marks simples et contextuels, l'implémentation custom avec [Floating UI](https://floating-ui.com/) est préférable — elle est plus légère et s'intègre nativement dans ton design system.

---

## 7. Context Provider d'Onboarding

### Onboarding Context & Hook

Centralise l'état d'onboarding dans un context React pour un accès facile dans toute l'application.

```tsx
// OnboardingContext — centralized onboarding state management
import {
  createContext,
  useContext,
  useReducer,
  useCallback,
  ReactNode,
} from "react";

interface OnboardingState {
  isActive: boolean;
  currentFlow: string | null;
  currentStep: number;
  completedSteps: string[];
  completedFlows: string[];
  dismissedTours: string[];
}

type OnboardingAction =
  | { type: "START_FLOW"; flow: string }
  | { type: "NEXT_STEP" }
  | { type: "PREV_STEP" }
  | { type: "COMPLETE_STEP"; stepId: string }
  | { type: "COMPLETE_FLOW"; flow: string }
  | { type: "DISMISS_TOUR"; tourId: string }
  | { type: "RESET" };

const initialState: OnboardingState = {
  isActive: false,
  currentFlow: null,
  currentStep: 0,
  completedSteps: [],
  completedFlows: [],
  dismissedTours: [],
};

function onboardingReducer(
  state: OnboardingState,
  action: OnboardingAction
): OnboardingState {
  switch (action.type) {
    case "START_FLOW":
      return { ...state, isActive: true, currentFlow: action.flow, currentStep: 0 };
    case "NEXT_STEP":
      return { ...state, currentStep: state.currentStep + 1 };
    case "PREV_STEP":
      return { ...state, currentStep: Math.max(0, state.currentStep - 1) };
    case "COMPLETE_STEP":
      if (state.completedSteps.includes(action.stepId)) return state;
      return { ...state, completedSteps: [...state.completedSteps, action.stepId] };
    case "COMPLETE_FLOW":
      return {
        ...state,
        isActive: false,
        currentFlow: null,
        currentStep: 0,
        completedFlows: state.completedFlows.includes(action.flow)
          ? state.completedFlows
          : [...state.completedFlows, action.flow],
      };
    case "DISMISS_TOUR":
      return {
        ...state,
        isActive: false,
        currentFlow: null,
        dismissedTours: state.dismissedTours.includes(action.tourId)
          ? state.dismissedTours
          : [...state.dismissedTours, action.tourId],
      };
    case "RESET":
      return initialState;
    default:
      return state;
  }
}

interface OnboardingContextValue {
  state: OnboardingState;
  startFlow: (flow: string) => void;
  nextStep: () => void;
  prevStep: () => void;
  completeStep: (stepId: string) => void;
  completeFlow: (flow: string) => void;
  dismissTour: (tourId: string) => void;
  isFlowCompleted: (flow: string) => boolean;
  isTourDismissed: (tourId: string) => boolean;
}

const OnboardingContext = createContext<OnboardingContextValue | null>(null);

export function OnboardingProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(onboardingReducer, initialState);

  const startFlow = useCallback((flow: string) => {
    dispatch({ type: "START_FLOW", flow });
    analytics.track("onboarding_flow_started", { flow });
  }, []);

  const nextStep = useCallback(() => dispatch({ type: "NEXT_STEP" }), []);
  const prevStep = useCallback(() => dispatch({ type: "PREV_STEP" }), []);

  const completeStep = useCallback((stepId: string) => {
    dispatch({ type: "COMPLETE_STEP", stepId });
    analytics.track("onboarding_step_completed", { stepId });
  }, []);

  const completeFlow = useCallback((flow: string) => {
    dispatch({ type: "COMPLETE_FLOW", flow });
    analytics.track("onboarding_flow_completed", { flow });
  }, []);

  const dismissTour = useCallback((tourId: string) => {
    dispatch({ type: "DISMISS_TOUR", tourId });
    analytics.track("onboarding_tour_dismissed", { tourId });
  }, []);

  const isFlowCompleted = useCallback(
    (flow: string) => state.completedFlows.includes(flow),
    [state.completedFlows]
  );

  const isTourDismissed = useCallback(
    (tourId: string) => state.dismissedTours.includes(tourId),
    [state.dismissedTours]
  );

  return (
    <OnboardingContext.Provider
      value={{
        state,
        startFlow,
        nextStep,
        prevStep,
        completeStep,
        completeFlow,
        dismissTour,
        isFlowCompleted,
        isTourDismissed,
      }}
    >
      {children}
    </OnboardingContext.Provider>
  );
}

export function useOnboarding() {
  const context = useContext(OnboardingContext);
  if (!context) throw new Error("useOnboarding must be used within <OnboardingProvider>");
  return context;
}
```

---

## 8. Wizard Multi-Étapes

### Setup Wizard avec State Management

```tsx
// Multi-step wizard with typed state management
interface WizardStep<T = Record<string, unknown>> {
  id: string;
  title: string;
  description?: string;
  component: React.ComponentType<WizardStepProps<T>>;
  validate?: (data: T) => boolean | Promise<boolean>;
  optional?: boolean;
}

interface WizardStepProps<T> {
  data: T;
  onChange: (updates: Partial<T>) => void;
  onNext: () => void;
  onPrev: () => void;
}

// Onboarding wizard for new users
interface OnboardingData {
  fullName: string;
  companyName: string;
  teamSize: "solo" | "small" | "medium" | "large";
  useCase: string[];
  inviteEmails: string[];
}

function useWizard<T extends Record<string, unknown>>(
  steps: WizardStep<T>[],
  initialData: T,
  onComplete: (data: T) => void
) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [data, setData] = useState<T>(initialData);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const currentStep = steps[currentStepIndex];
  const isFirstStep = currentStepIndex === 0;
  const isLastStep = currentStepIndex === steps.length - 1;
  const progressPercent = Math.round(
    ((currentStepIndex + 1) / steps.length) * 100
  );

  const onChange = useCallback(
    (updates: Partial<T>) => setData((prev) => ({ ...prev, ...updates })),
    []
  );

  const goNext = useCallback(async () => {
    if (currentStep.validate) {
      const valid = await currentStep.validate(data);
      if (!valid) return;
    }
    if (isLastStep) {
      setIsSubmitting(true);
      try {
        await onComplete(data);
      } finally {
        setIsSubmitting(false);
      }
    } else {
      setCurrentStepIndex((i) => i + 1);
    }
  }, [currentStep, data, isLastStep, onComplete]);

  const goPrev = useCallback(() => {
    if (!isFirstStep) setCurrentStepIndex((i) => i - 1);
  }, [isFirstStep]);

  return {
    currentStep,
    currentStepIndex,
    data,
    onChange,
    goNext,
    goPrev,
    isFirstStep,
    isLastStep,
    isSubmitting,
    progressPercent,
  };
}

// Wizard UI wrapper
function OnboardingWizard() {
  const wizard = useWizard(
    ONBOARDING_STEPS,
    {
      fullName: "",
      companyName: "",
      teamSize: "small",
      useCase: [],
      inviteEmails: [],
    },
    async (data) => {
      await api.completeOnboarding(data);
      router.push("/dashboard");
    }
  );

  const StepComponent = wizard.currentStep.component;

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background p-4">
      <div className="w-full max-w-lg">
        {/* Progress */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">
              Étape {wizard.currentStepIndex + 1} sur {ONBOARDING_STEPS.length}
            </span>
            <span className="text-sm text-muted-foreground">
              {wizard.progressPercent}%
            </span>
          </div>
          <div className="h-1.5 bg-muted rounded-full overflow-hidden">
            <div
              className="h-full bg-primary rounded-full transition-all duration-300"
              style={{ width: `${wizard.progressPercent}%` }}
            />
          </div>
        </div>

        {/* Step content */}
        <div className="bg-card rounded-2xl border border-border shadow-sm p-8">
          <h2 className="text-xl font-semibold mb-1">{wizard.currentStep.title}</h2>
          {wizard.currentStep.description && (
            <p className="text-sm text-muted-foreground mb-6">
              {wizard.currentStep.description}
            </p>
          )}
          <StepComponent
            data={wizard.data}
            onChange={wizard.onChange}
            onNext={wizard.goNext}
            onPrev={wizard.goPrev}
          />
        </div>

        {/* Navigation */}
        <div className="flex justify-between mt-4">
          <button
            onClick={wizard.goPrev}
            disabled={wizard.isFirstStep}
            className="btn btn-ghost disabled:opacity-0"
          >
            ← Précédent
          </button>
          <button
            onClick={wizard.goNext}
            disabled={wizard.isSubmitting}
            className="btn btn-primary"
          >
            {wizard.isLastStep
              ? wizard.isSubmitting
                ? "Finalisation..."
                : "Terminer"
              : "Suivant →"}
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

## 9. Personalisation & Re-Onboarding

### Questionnaire de Personalisation

Capture le contexte utilisateur dès le départ pour personnaliser l'expérience. Limite le questionnaire à 3-5 questions avec des réponses pré-définies (pas de champs libres).

```tsx
// Role-based onboarding flow selection
type UserRole = "developer" | "designer" | "product-manager" | "executive";
type TeamSize = "solo" | "2-10" | "11-50" | "50+";

interface OnboardingProfile {
  role: UserRole;
  teamSize: TeamSize;
  primaryGoal: string;
}

// Map profile to onboarding flow
function getOnboardingFlow(profile: OnboardingProfile): string[] {
  const flowMap: Record<UserRole, string[]> = {
    developer: [
      "api-key-setup",
      "sdk-installation",
      "first-integration",
      "invite-teammates",
    ],
    designer: [
      "design-file-import",
      "component-library-tour",
      "share-with-team",
      "first-prototype",
    ],
    "product-manager": [
      "team-setup",
      "first-project",
      "milestone-creation",
      "analytics-overview",
    ],
    executive: [
      "team-setup",
      "dashboard-overview",
      "reporting-tour",
    ],
  };
  return flowMap[profile.role] ?? flowMap["product-manager"];
}
```

### Re-Onboarding — Nouvelles Fonctionnalités

Réintroduis les utilisateurs existants lors du lancement de nouvelles fonctionnalités. Utilise un déclencheur contextuel (pas une popup au démarrage).

```tsx
// Feature announcement with contextual trigger
interface FeatureAnnouncement {
  id: string;
  title: string;
  description: string;
  ctaLabel: string;
  ctaHref: string;
  targetPage: string; // Show only on relevant page
  minAccountAgeDays: number; // Don't show to brand new users
  expiresAt: Date;
}

function useFeatureAnnouncement(announcement: FeatureAnnouncement) {
  const { user } = useAuth();
  const [dismissed, setDismissed] = useState(() =>
    localStorage.getItem(`announcement_${announcement.id}`) === "dismissed"
  );

  const accountAgeDays = user
    ? Math.floor(
        (Date.now() - new Date(user.createdAt).getTime()) / (1000 * 60 * 60 * 24)
      )
    : 0;

  const shouldShow =
    !dismissed &&
    new Date() < announcement.expiresAt &&
    accountAgeDays >= announcement.minAccountAgeDays;

  const dismiss = () => {
    localStorage.setItem(`announcement_${announcement.id}`, "dismissed");
    setDismissed(true);
    analytics.track("feature_announcement_dismissed", { id: announcement.id });
  };

  const acknowledge = () => {
    localStorage.setItem(`announcement_${announcement.id}`, "dismissed");
    setDismissed(true);
    analytics.track("feature_announcement_clicked", { id: announcement.id });
  };

  return { shouldShow, dismiss, acknowledge };
}
```

---

## 10. Séquences Email d'Onboarding

### Drip Campaign Déclenchée par les Événements In-App

Les emails d'onboarding les plus efficaces sont déclenchés par des **événements comportementaux**, pas par un calendrier fixe.

```typescript
// Email trigger system — event-driven drip campaign
type OnboardingEmailTrigger =
  | { type: "user_signed_up"; userId: string }
  | { type: "user_inactive"; userId: string; daysSinceLastVisit: number }
  | { type: "step_not_completed"; userId: string; stepId: string; daysElapsed: number }
  | { type: "aha_moment_reached"; userId: string }
  | { type: "trial_ending"; userId: string; daysRemaining: number };

interface OnboardingEmail {
  templateId: string;
  subject: string;
  triggerDelay: number; // Hours after trigger event
  condition: (trigger: OnboardingEmailTrigger) => boolean;
}

const ONBOARDING_EMAIL_SEQUENCE: OnboardingEmail[] = [
  {
    templateId: "welcome-get-started",
    subject: "Bienvenue ! Par où commencer ?",
    triggerDelay: 0,
    condition: (t) => t.type === "user_signed_up",
  },
  {
    templateId: "first-value-tip",
    subject: "1 astuce pour ton premier succès avec [Produit]",
    triggerDelay: 24,
    condition: (t) => t.type === "user_signed_up",
  },
  {
    templateId: "stuck-recovery",
    subject: "Tu n'es pas seul — voici comment débloquer [étape]",
    triggerDelay: 48,
    condition: (t) =>
      t.type === "step_not_completed" &&
      t.stepId === "first-project" &&
      t.daysElapsed >= 2,
  },
  {
    templateId: "aha-congratulations",
    subject: "Félicitations ! Tu viens de débloquer [fonctionnalité]",
    triggerDelay: 0,
    condition: (t) => t.type === "aha_moment_reached",
  },
  {
    templateId: "re-engagement",
    subject: "On a ajouté [X] nouvelles fonctionnalités depuis ta dernière visite",
    triggerDelay: 0,
    condition: (t) =>
      t.type === "user_inactive" && t.daysSinceLastVisit >= 7,
  },
];

// Trigger email sending via webhook to email provider (Resend, Postmark, SendGrid)
async function triggerOnboardingEmail(
  event: OnboardingEmailTrigger,
  userEmail: string
) {
  const emailsToSend = ONBOARDING_EMAIL_SEQUENCE.filter((e) =>
    e.condition(event)
  );

  for (const email of emailsToSend) {
    if (email.triggerDelay > 0) {
      // Schedule via job queue (BullMQ, Inngest, etc.)
      await jobQueue.schedule(
        "send-onboarding-email",
        { templateId: email.templateId, userEmail },
        { delay: email.triggerDelay * 60 * 60 * 1000 }
      );
    } else {
      await emailProvider.send({
        to: userEmail,
        template: email.templateId,
      });
    }
  }
}
```

---

## 11. Mesurer l'Onboarding

### Métriques Clés

| Métrique | Définition | Cible | Outil |
|---|---|---|---|
| **Activation Rate** | % users ayant atteint l'Aha moment dans 7 jours | > 40% | Mixpanel, Amplitude |
| **Time-to-Value** | Temps médian entre inscription et premier succès | < 10 min | Heap, Amplitude |
| **Onboarding Completion Rate** | % users ayant terminé la checklist/wizard | > 60% | Custom events |
| **Step Drop-off Rate** | % d'abandons à chaque étape du wizard | < 15% par étape | Funnel analysis |
| **Tour Dismissal Rate** | % users qui skippent le product tour | < 40% | Custom events |
| **D7 Retention** | % users actifs à J+7 parmi les activés | > 50% | Cohort analysis |

### Analyse des Drop-offs

```typescript
// Onboarding funnel analysis
interface OnboardingFunnelStep {
  stepId: string;
  stepName: string;
  usersEntered: number;
  usersCompleted: number;
  medianTimeSeconds: number;
}

function analyzeOnboardingFunnel(
  steps: OnboardingFunnelStep[]
): { bottleneck: string; dropoffRate: number } {
  let maxDropoff = 0;
  let bottleneck = steps[0].stepId;

  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    const dropoffRate =
      step.usersEntered > 0
        ? 1 - step.usersCompleted / step.usersEntered
        : 0;

    console.log(
      `${step.stepName}: ${Math.round(dropoffRate * 100)}% abandonnent ` +
      `(temps médian: ${step.medianTimeSeconds}s)`
    );

    if (dropoffRate > maxDropoff) {
      maxDropoff = dropoffRate;
      bottleneck = step.stepId;
    }
  }

  return { bottleneck, dropoffRate: maxDropoff };
}

// Track time-to-value
function useTimeToValue(ahaEventName: string) {
  useEffect(() => {
    const signupTime = sessionStorage.getItem("signup_timestamp");
    if (!signupTime) return;

    const handler = (event: CustomEvent) => {
      if (event.detail.name === ahaEventName) {
        const ttv = Date.now() - parseInt(signupTime, 10);
        analytics.track("time_to_value", {
          milliseconds: ttv,
          seconds: Math.round(ttv / 1000),
          minutes: Math.round(ttv / 60000),
        });
      }
    };

    window.addEventListener("analytics_event", handler as EventListener);
    return () => window.removeEventListener("analytics_event", handler as EventListener);
  }, [ahaEventName]);
}
```

### Logique de Déclenchement du Product Tour

```tsx
// Product tour trigger logic — smart activation conditions
function useShouldShowProductTour(tourId: string) {
  const { user } = useAuth();
  const { isTourDismissed } = useOnboarding();

  return useMemo(() => {
    if (!user) return false;
    if (isTourDismissed(tourId)) return false;

    const accountAgeDays = Math.floor(
      (Date.now() - new Date(user.createdAt).getTime()) / (1000 * 60 * 60 * 24)
    );

    // Don't show to users older than 3 days — they've found their way
    if (accountAgeDays > 3) return false;

    // Don't show if user has already completed relevant actions
    if (user.activationMilestones?.includes("first-project-created")) return false;

    // Show only on first visit to dashboard (track with session storage)
    const hasSeenDashboard = sessionStorage.getItem(`tour_${tourId}_triggered`);
    if (hasSeenDashboard) return false;

    sessionStorage.setItem(`tour_${tourId}_triggered`, "true");
    return true;
  }, [user, tourId, isTourDismissed]);
}
```

---

## Références

- Samuel Hulick, *The Elements of User Onboarding* (UserOnboard.com)
- Wes Bush, *Product-Led Growth: How to Build a Product That Sells Itself* (2019)
- Amplitude, *The Product Intelligence Report: Activation Benchmarks* -- https://amplitude.com/resources
- Floating UI, *Positioning Tooltips & Popovers* -- https://floating-ui.com/docs/getting-started
- Shepherd.js, *JavaScript Tour Library* -- https://shepherdjs.dev/docs/
- Appcues, *Onboarding Best Practices* -- https://www.appcues.com/blog
- Intercom, *Inside Intercom: Onboarding* -- https://www.intercom.com/resources
- Mixpanel, *Activation Rate Guide* -- https://mixpanel.com/blog/activation-rate/
