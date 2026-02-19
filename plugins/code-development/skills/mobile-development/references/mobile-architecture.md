# Architecture Mobile — Principes et Patterns

## Vue d'ensemble

Une architecture mobile bien conçue est le fondement d'une application maintenable, testable et évolutive. Ce document couvre les patterns architecturaux éprouvés, de la Clean Architecture aux stratégies offline-first, avec des exemples concrets en TypeScript et Dart.

---

## Clean Architecture pour Mobile

La Clean Architecture de Robert C. Martin s'adapte parfaitement au mobile en trois couches distinctes, chacune avec des responsabilités claires et des dépendances unidirectionnelles (toujours vers l'intérieur).

```
┌────────────────────────────────────────┐
│           Présentation                 │
│  (UI, ViewModels, State Management)   │
├────────────────────────────────────────┤
│             Domaine                    │
│  (Entités, UseCases, Interfaces)       │
├────────────────────────────────────────┤
│             Données                    │
│  (Repositories, DataSources, API)      │
└────────────────────────────────────────┘
       Dépendances : toujours vers le domaine
```

### Couche Domaine — Le cœur métier

La couche domaine est indépendante de tout framework. Elle ne connaît ni React Native, ni Flutter, ni aucune bibliothèque externe.

```typescript
// domain/entities/commande.ts
export interface LigneCommande {
  readonly produitId: string;
  readonly quantite: number;
  readonly prixUnitaire: number;
}

export class Commande {
  constructor(
    public readonly id: string,
    public readonly lignes: LigneCommande[],
    public readonly creeA: Date,
    public readonly statut: StatutCommande,
  ) {}

  get montantTotal(): number {
    return this.lignes.reduce(
      (total, ligne) => total + ligne.quantite * ligne.prixUnitaire,
      0
    );
  }

  get estModifiable(): boolean {
    return this.statut === StatutCommande.EN_ATTENTE;
  }

  ajouterLigne(ligne: LigneCommande): Commande {
    if (!this.estModifiable) {
      throw new Error('Impossible de modifier une commande déjà traitée');
    }
    return new Commande(
      this.id,
      [...this.lignes, ligne],
      this.creeA,
      this.statut,
    );
  }
}

export enum StatutCommande {
  EN_ATTENTE = 'en_attente',
  CONFIRMEE = 'confirmee',
  EXPEDIEE = 'expediee',
  LIVREE = 'livree',
  ANNULEE = 'annulee',
}
```

```typescript
// domain/repositories/commande-repository.ts
// Interface définie dans le domaine, implémentée dans la couche données
export interface CommandeRepository {
  getCommande(id: string): Promise<Commande>;
  listerCommandes(options: { page: number; statut?: StatutCommande }): Promise<Commande[]>;
  creerCommande(lignes: LigneCommande[]): Promise<Commande>;
  annulerCommande(id: string): Promise<Commande>;
}

// domain/usecases/passer-commande.usecase.ts
export class PasserCommandeUseCase {
  constructor(
    private commandeRepo: CommandeRepository,
    private inventaireRepo: InventaireRepository,
    private notificationService: NotificationService,
  ) {}

  async executer(lignes: LigneCommande[]): Promise<Resultat<Commande>> {
    // Règle métier : vérifier la disponibilité des stocks
    for (const ligne of lignes) {
      const stock = await this.inventaireRepo.getStock(ligne.produitId);
      if (stock.quantiteDisponible < ligne.quantite) {
        return Resultat.echec(`Stock insuffisant pour ${ligne.produitId}`);
      }
    }

    // Créer la commande via le repository
    const commande = await this.commandeRepo.creerCommande(lignes);

    // Notifier l'utilisateur (service abstrait)
    await this.notificationService.envoyerConfirmation(commande);

    return Resultat.succes(commande);
  }
}
```

### Couche Données — Implémentation des repositories

```typescript
// data/repositories/commande-repository.impl.ts
export class CommandeRepositoryImpl implements CommandeRepository {
  constructor(
    private readonly remoteDataSource: CommandeRemoteDataSource,
    private readonly localDataSource: CommandeLocalDataSource,
    private readonly networkInfo: NetworkInfo,
  ) {}

  async getCommande(id: string): Promise<Commande> {
    if (await this.networkInfo.estConnecte) {
      try {
        const commandeDto = await this.remoteDataSource.getCommande(id);
        await this.localDataSource.mettreEnCache(commandeDto);
        return CommandeMapper.versEntite(commandeDto);
      } catch (e) {
        // Fallback transparent vers le cache local
        const cached = await this.localDataSource.getCommande(id);
        return CommandeMapper.versEntite(cached);
      }
    } else {
      const cached = await this.localDataSource.getCommande(id);
      return CommandeMapper.versEntite(cached);
    }
  }

  async creerCommande(lignes: LigneCommande[]): Promise<Commande> {
    const dto = await this.remoteDataSource.creerCommande(
      lignes.map(CommandeMapper.ligneVersDto)
    );
    await this.localDataSource.sauvegarder(dto);
    return CommandeMapper.versEntite(dto);
  }
}
```

### Couche Présentation — MVVM avec React Native

```typescript
// presentation/viewmodels/commandes-viewmodel.ts
interface CommandesState {
  commandes: Commande[];
  estEnChargement: boolean;
  erreur: string | null;
  pageActuelle: number;
  aToutCharge: boolean;
}

function useCommandesViewModel() {
  const [etat, setEtat] = useState<CommandesState>({
    commandes: [],
    estEnChargement: false,
    erreur: null,
    pageActuelle: 1,
    aToutCharge: false,
  });

  const useCase = useDependance(ListerCommandesUseCase);

  const charger = useCallback(async (page = 1) => {
    setEtat(prev => ({ ...prev, estEnChargement: true, erreur: null }));
    try {
      const nouvelles = await useCase.executer({ page });
      setEtat(prev => ({
        ...prev,
        commandes: page === 1 ? nouvelles : [...prev.commandes, ...nouvelles],
        pageActuelle: page,
        aToutCharge: nouvelles.length < PAGE_SIZE,
        estEnChargement: false,
      }));
    } catch (e) {
      setEtat(prev => ({
        ...prev,
        erreur: 'Impossible de charger les commandes',
        estEnChargement: false,
      }));
    }
  }, [useCase]);

  const chargerSuivant = useCallback(() => {
    if (!etat.estEnChargement && !etat.aToutCharge) {
      charger(etat.pageActuelle + 1);
    }
  }, [etat, charger]);

  useEffect(() => { charger(1); }, [charger]);

  return { ...etat, charger, chargerSuivant };
}
```

---

## Pattern MVVM — Équivalent Flutter avec Riverpod

```dart
// Flutter: ViewModel déclaratif avec Riverpod Notifier
@riverpod
class CommandesNotifier extends _$CommandesNotifier {
  @override
  Future<List<Commande>> build() async {
    return ref.watch(listerCommandesUseCaseProvider).executer(page: 1);
  }

  Future<void> rafraichir() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(listerCommandesUseCaseProvider).executer(page: 1),
    );
  }
}

// La vue consomme le ViewModel via ref.watch
class EcranCommandes extends ConsumerWidget {
  const EcranCommandes({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final etat = ref.watch(commandesNotifierProvider);

    return etat.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, stack) => MessageErreur(message: err.toString()),
      data: (commandes) => ListeCommandes(commandes: commandes),
    );
  }
}
```

---

## Gestion d'état — Flux de données unidirectionnel

Le flux unidirectionnel (Unidirectional Data Flow — UDF) garantit que les changements d'état sont prévisibles et traçables. C'est le pattern fondamental de React Native et Flutter.

```
UI Event → Action → Reducer/Notifier → Nouvel état → Mise à jour UI
   ↑                                                         |
   └─────────────────────────────────────────────────────────┘
```

Implémentation d'un store avec Immer pour l'immuabilité :

```typescript
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface PanierState {
  articles: ArticlePanier[];
  couponCode: string | null;
  actions: {
    ajouterArticle: (produit: Produit) => void;
    supprimerArticle: (id: string) => void;
    modifierQuantite: (id: string, quantite: number) => void;
    appliquerCoupon: (code: string) => Promise<void>;
    vider: () => void;
  };
}

const usePanierStore = create<PanierState>()(
  immer((set) => ({
    articles: [],
    couponCode: null,
    actions: {
      ajouterArticle: (produit) =>
        set((state) => {
          const existant = state.articles.find(a => a.produit.id === produit.id);
          if (existant) {
            existant.quantite += 1;
          } else {
            state.articles.push({ produit, quantite: 1 });
          }
        }),

      supprimerArticle: (id) =>
        set((state) => {
          state.articles = state.articles.filter(a => a.produit.id !== id);
        }),

      modifierQuantite: (id, quantite) =>
        set((state) => {
          const article = state.articles.find(a => a.produit.id === id);
          if (article) {
            article.quantite = Math.max(0, quantite);
            if (article.quantite === 0) {
              state.articles = state.articles.filter(a => a.produit.id !== id);
            }
          }
        }),

      appliquerCoupon: async (code) => {
        const estValide = await api.validerCoupon(code);
        if (estValide) {
          set((state) => { state.couponCode = code; });
        }
      },

      vider: () => set({ articles: [], couponCode: null }),
    },
  }))
);

// Sélecteur mémoïsé pour éviter les re-renders inutiles
const selectionnerTotal = (state: PanierState) =>
  state.articles.reduce((sum, a) => sum + a.produit.prix * a.quantite, 0);
```

---

## Architecture de Navigation

### Patterns de navigation mobile

**Navigation en pile (Stack)** — Pour les flux linéaires :
```
Accueil → Catégorie → Produit → Panier → Confirmation
```

**Navigation en onglets (Tabs)** — Pour les sections principales de l'app :
```
[Accueil] [Explorer] [Panier] [Profil]
```

**Navigation modale** — Pour les actions contextuelles ou les flux courts :
```
Panier → [Modal] Sélection d'adresse → Retour au panier
```

**Deep Links** — Liens profonds vers un écran spécifique :
```
app://commandes/123 → ÉcranCommandes → DétailCommande(id=123)
```

```typescript
// Hiérarchie de navigation complète et typée
type NavigationHierarchie = {
  // Navigation principale par onglets
  RacineTab: {
    AccueilStack: {
      Accueil: undefined;
      CatégorieProduits: { categorieId: string };
      DétailProduit: { produitId: string };
    };
    ExplorerStack: {
      Explorer: undefined;
      ResultatsRecherche: { requete: string };
    };
    ProfilStack: {
      Profil: undefined;
      Parametres: undefined;
      Abonnement: undefined;
    };
  };
  // Modals superposées à la navigation principale
  PanierModal: undefined;
  ConfirmationCommandeModal: { commandeId: string };
};
```

---

## Architecture Offline-First

### Mises à jour optimistes

Les mises à jour optimistes affichent le résultat attendu immédiatement, avant la confirmation du serveur, pour une expérience perçue comme instantanée.

```typescript
function useAjouterAuPanier() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.ajouterArticle,
    onMutate: async (nouvelArticle) => {
      // Annuler les requêtes en cours pour éviter les conflits de cache
      await queryClient.cancelQueries({ queryKey: ['panier'] });

      // Sauvegarder l'état actuel pour rollback éventuel
      const panierPrecedent = queryClient.getQueryData(['panier']);

      // Mise à jour optimiste immédiate — l'UI se met à jour avant la réponse API
      queryClient.setQueryData(['panier'], (ancien: Panier) => ({
        ...ancien,
        articles: [
          ...ancien.articles,
          { ...nouvelArticle, id: 'temp-' + Date.now(), statut: 'en_attente' },
        ],
      }));

      return { panierPrecedent };
    },
    onError: (err, _nouvelArticle, context) => {
      // Rollback automatique en cas d'erreur réseau
      queryClient.setQueryData(['panier'], context?.panierPrecedent);
    },
    onSettled: () => {
      // Resynchroniser avec le serveur dans tous les cas
      queryClient.invalidateQueries({ queryKey: ['panier'] });
    },
  });
}
```

### File d'attente de synchronisation

```typescript
// Gestion des actions offline avec file d'attente persistante
interface ActionPendante {
  id: string;
  type: string;
  payload: unknown;
  timestamp: number;
  tentatives: number;
}

class SynchronisationService {
  private fileAttente: ActionPendante[] = [];
  private readonly MAX_TENTATIVES = 5;

  async mettreEnFile(action: Omit<ActionPendante, 'id' | 'timestamp' | 'tentatives'>) {
    const actionComplete: ActionPendante = {
      ...action,
      id: uuid(),
      timestamp: Date.now(),
      tentatives: 0,
    };
    this.fileAttente.push(actionComplete);
    await this.persister();
  }

  async synchroniser() {
    if (!await networkInfo.estConnecte) return;

    for (const action of [...this.fileAttente]) {
      try {
        await this.executerAction(action);
        this.fileAttente = this.fileAttente.filter(a => a.id !== action.id);
      } catch (e) {
        action.tentatives += 1;
        if (action.tentatives >= this.MAX_TENTATIVES) {
          await this.signalerEchec(action);
          this.fileAttente = this.fileAttente.filter(a => a.id !== action.id);
        }
      }
    }
    await this.persister();
  }

  private async persister() {
    // Sauvegarder la file dans MMKV pour survivre aux redémarrages
    storage.set('sync_queue', JSON.stringify(this.fileAttente));
  }
}
```

### Résolution de conflits

```typescript
// Stratégies de résolution quand local et serveur divergent
enum StrategieResolution {
  SERVEUR_GAGNE = 'serveur',         // Données serveur écrasent le local
  CLIENT_GAGNE = 'client',           // Données locales écrasent le serveur
  DERNIERE_MODIFICATION = 'timestamp', // La modification la plus récente l'emporte
  FUSION = 'merge',                  // Fusion intelligente champ par champ
}

class ResolveurConflits {
  resoudre<T extends { modifieA: Date }>(
    local: T,
    distant: T,
    strategie: StrategieResolution,
  ): T {
    switch (strategie) {
      case StrategieResolution.SERVEUR_GAGNE:
        return distant;
      case StrategieResolution.CLIENT_GAGNE:
        return local;
      case StrategieResolution.DERNIERE_MODIFICATION:
        return local.modifieA > distant.modifieA ? local : distant;
      case StrategieResolution.FUSION:
        return this.fusionner(local, distant);
    }
  }

  private fusionner<T>(local: T, distant: T): T {
    // Les champs non-null du client ont la priorité sur le serveur
    return Object.entries(distant as Record<string, unknown>).reduce(
      (resultat, [cle, valeurDistante]) => ({
        ...resultat,
        [cle]: (local as Record<string, unknown>)[cle] ?? valeurDistante,
      }),
      {} as T
    );
  }
}
```

---

## Organisation du code — Feature-first

Structure recommandée pour un projet React Native de taille moyenne à grande :

```
src/
├── app/                    # Configuration globale (providers, navigation racine)
│   ├── providers.tsx
│   └── navigation.tsx
├── features/               # Fonctionnalités organisées par domaine métier
│   ├── auth/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── repositories/    # Interfaces seulement
│   │   │   └── usecases/
│   │   ├── data/
│   │   │   ├── datasources/     # Implémentations API et cache
│   │   │   ├── models/          # DTOs et mappers
│   │   │   └── repositories/    # Implémentations concrètes
│   │   └── presentation/
│   │       ├── screens/
│   │       ├── components/
│   │       └── hooks/           # ViewModels sous forme de hooks
│   └── commandes/
│       └── (même structure)
├── shared/                 # Code transversal entre features
│   ├── components/         # Composants UI réutilisables
│   ├── hooks/              # Hooks utilitaires génériques
│   ├── services/           # Services transversaux (réseau, analytics)
│   └── utils/              # Fonctions pures utilitaires
└── infrastructure/         # Configuration technique bas niveau
    ├── api/                # Client HTTP configuré
    ├── storage/            # Couche de stockage abstrait
    └── di/                 # Conteneur d'injection de dépendances
```

---

## Injection de dépendances

```typescript
// Conteneur DI léger adapté au mobile
class ConteneurDI {
  private static instance: ConteneurDI;
  private readonly dependances = new Map<symbol, unknown>();

  static getInstance() {
    if (!this.instance) this.instance = new ConteneurDI();
    return this.instance;
  }

  enregistrer<T>(token: symbol, factory: () => T): void {
    this.dependances.set(token, factory());
  }

  resoudre<T>(token: symbol): T {
    const instance = this.dependances.get(token);
    if (!instance) throw new Error(`Dépendance non enregistrée: ${String(token)}`);
    return instance as T;
  }
}

// Tokens typés pour éviter les collisions
const TOKENS = {
  CommandeRepository: Symbol('CommandeRepository'),
  PasserCommandeUseCase: Symbol('PasserCommandeUseCase'),
  InventaireRepository: Symbol('InventaireRepository'),
};

// Configuration au démarrage de l'app
const conteneur = ConteneurDI.getInstance();
conteneur.enregistrer(TOKENS.CommandeRepository, () =>
  new CommandeRepositoryImpl(
    new CommandeRemoteDataSource(apiClient),
    new CommandeLocalDataSource(storage),
    networkInfo
  )
);
conteneur.enregistrer(TOKENS.PasserCommandeUseCase, () =>
  new PasserCommandeUseCase(
    conteneur.resoudre(TOKENS.CommandeRepository),
    conteneur.resoudre(TOKENS.InventaireRepository),
    notificationService
  )
);

// Hook React pour résoudre les dépendances dans les composants
function useDependance<T>(token: symbol): T {
  return useMemo(() => ConteneurDI.getInstance().resoudre<T>(token), [token]);
}
```

---

## Architecture de tests

### Tests unitaires — UseCase isolé avec mocks

```typescript
describe('PasserCommandeUseCase', () => {
  let useCase: PasserCommandeUseCase;
  let commandeRepo: jest.Mocked<CommandeRepository>;
  let inventaireRepo: jest.Mocked<InventaireRepository>;
  let notificationService: jest.Mocked<NotificationService>;

  beforeEach(() => {
    commandeRepo = {
      creerCommande: jest.fn(),
      getCommande: jest.fn(),
      listerCommandes: jest.fn(),
      annulerCommande: jest.fn(),
    };
    inventaireRepo = {
      getStock: jest.fn(),
    };
    notificationService = {
      envoyerConfirmation: jest.fn(),
    };
    useCase = new PasserCommandeUseCase(
      commandeRepo, inventaireRepo, notificationService
    );
  });

  it('crée une commande si le stock est suffisant', async () => {
    inventaireRepo.getStock.mockResolvedValue({ quantiteDisponible: 10 });
    commandeRepo.creerCommande.mockResolvedValue(commandeFactice);

    const resultat = await useCase.executer([
      { produitId: 'p1', quantite: 3, prixUnitaire: 29.99 }
    ]);

    expect(resultat.estSucces).toBe(true);
    expect(commandeRepo.creerCommande).toHaveBeenCalledTimes(1);
    expect(notificationService.envoyerConfirmation).toHaveBeenCalledWith(commandeFactice);
  });

  it('échoue si le stock est insuffisant', async () => {
    inventaireRepo.getStock.mockResolvedValue({ quantiteDisponible: 1 });

    const resultat = await useCase.executer([
      { produitId: 'p1', quantite: 5, prixUnitaire: 29.99 }
    ]);

    expect(resultat.estEchec).toBe(true);
    expect(commandeRepo.creerCommande).not.toHaveBeenCalled();
  });
});
```

### Tests Flutter — Widget et intégration

```dart
// Test de widget Flutter isolé
testWidgets('CarteProduit affiche le prix formaté', (WidgetTester tester) async {
  final produit = Produit(
    id: '1',
    nom: 'Écouteurs Bluetooth',
    prix: 89.99,
    imageUrl: 'https://example.com/image.jpg',
  );

  await tester.pumpWidget(
    MaterialApp(
      home: CarteProduit(
        produit: produit,
        onAjouterAuPanier: () {},
      ),
    ),
  );

  expect(find.text('Écouteurs Bluetooth'), findsOneWidget);
  expect(find.text('89.99 €'), findsOneWidget);
  expect(find.byIcon(Icons.shopping_cart), findsOneWidget);
});
```

---

## Récapitulatif des décisions architecturales

| Décision | Option recommandée | Justification |
|---|---|---|
| Architecture globale | Clean Architecture + MVVM | Séparation des responsabilités, testabilité |
| Organisation des fichiers | Feature-first (par domaine) | Scalabilité, co-localisation du code lié |
| Gestion d'état global | Zustand (RN) / Riverpod (Flutter) | Léger, typé, testable sans boilerplate |
| Gestion des requêtes | TanStack Query / Riverpod FutureProvider | Cache, retry, invalidation automatiques |
| Navigation | React Navigation 6 / GoRouter | Communauté, type safety, deep links |
| Stockage local | MMKV + SQLite | Performance synchrone, chiffrement |
| Injection de dépendances | Conteneur DI simple ou inversify-lite | Testabilité, couplage faible |
| Tests | Pyramid : unitaires > widget > E2E | Couverture maximale au coût minimal |
