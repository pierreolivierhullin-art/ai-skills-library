# Études de Cas — Développement Mobile en Production

## Vue d'Ensemble

Ces études de cas couvrent des projets réels : un MVP Expo en 6 semaines, une optimisation de performance critique, une migration progressive d'une app native vers Flutter, et un déploiement offline-first pour des techniciens de terrain.

---

## Cas 1 — MVP en 6 Semaines avec Expo et Supabase

### Contexte

Startup logistique (4 personnes, 2 devs). Besoin : application de livraison pour chauffeurs (iOS + Android) avec tracking GPS, scan de codes-barres, signature électronique, et synchronisation avec un back-office web.

Budget technique : 8 000 EUR. Délai : 6 semaines pour le pilote avec 12 chauffeurs.

### Stack Choisie

```
Frontend mobile : Expo (React Native) + TypeScript
Backend + Auth : Supabase (PostgreSQL + Auth + Storage + Realtime)
Navigation : Expo Router (file-based, deep links gratuits)
State : Zustand + TanStack Query
Maps : react-native-maps + expo-location
Scanner : expo-barcode-scanner
Signature : react-native-signature-canvas
Deploy : EAS Build + EAS Update (OTA)
```

### Architecture

```typescript
// Structure simplifiée du projet
src/
├── app/
│   ├── (auth)/
│   │   └── login.tsx          // Authentification chauffeur
│   ├── (tabs)/
│   │   ├── tournée.tsx         // Liste des livraisons du jour
│   │   ├── scan.tsx            // Scanner codes-barres
│   │   └── profil.tsx
│   └── livraison/[id].tsx     // Détail + confirmation
├── features/
│   ├── tournée/               // Logique livraisons
│   ├── tracking/              // GPS en arrière-plan
│   └── signature/             // Capture signature
└── shared/
    ├── supabase.ts            // Client Supabase
    └── hooks/

// Tracking GPS avec Supabase Realtime
// tracking/useTracking.ts
export function useTracking(tournéeId: string) {
  useEffect(() => {
    let cleanup: (() => void) | null = null;

    ServiceLocalisation.démarrerSuivi().then(() => {
      cleanup = ServiceCapteurs.démarrerAccéléromètre(async ({ x, y, z }) => {
        const pos = await Location.getCurrentPositionAsync({});
        await supabase.from('positions').insert({
          tournée_id: tournéeId,
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
          précision: pos.coords.accuracy,
        });
      }, 30000); // Toutes les 30s
    });

    return () => cleanup?.();
  }, [tournéeId]);
}
```

### Problèmes Rencontrés et Solutions

**Problème 1 — Compression images** : les photos de livraison (preuve de dépôt) faisaient 4-8 MB. Upload lent sur 4G rural.

Solution :
```typescript
// Compression systématique avant upload
const uri = await ServiceMédias.optimiser(photoUri); // 1024px max, JPEG 75%
// Résultat : 4MB → 280KB en moyenne, upload 10x plus rapide
```

**Problème 2 — Tests uniquement sur simulateur** : le scanner de codes-barres ne fonctionnait pas sur simulateur iOS. Bug découvert le jour J.

Solution : EAS Build + TestFlight dès la semaine 2. Règle instaurée : toute fonctionnalité native testée sur appareil physique.

**Problème 3 — Supabase Realtime + mobile** : les connexions WebSocket se fermaient en arrière-plan iOS.

Solution :
```typescript
// Reconnexion automatique au retour en premier plan
AppState.addEventListener('change', (état) => {
  if (état === 'active') {
    supabase.realtime.connect();
  }
});
```

### Résultats (Pilote 6 Semaines)

| Métrique | Valeur |
|---|---|
| Délai de livraison | 6 semaines ✓ |
| Chauffeurs onboardés | 12 (objectif atteint) |
| Taux d'adoption | 100% (app obligatoire) |
| Bugs critiques | 2 (corrigés via OTA update J+1 et J+3) |
| Coût infra mensuel | 47 EUR (Supabase Pro) |
| Temps moyen de livraison | -18% (paperasse éliminée) |

**Leçon** : Expo + Supabase est une combinaison redoutablement efficace pour les MVP. Le gain de temps vient surtout de l'absence d'infrastructure à gérer. Tester sur appareil physique dès la semaine 1, pas la veille du lancement.

---

## Cas 2 — Optimisation Performance : de 2,1s à 400ms au Cold Start

### Contexte

Application e-commerce (React Native CLI, 150K utilisateurs actifs, iOS + Android). Cold start time : 2,1 secondes mesuré en prod sur mid-range Android. Objectif : < 600ms (benchmark concurrent).

### Diagnostic

```bash
# Profiling avec React Native Performance Monitor
# Identifier les bottlenecks :
# - JS bundle size : 8.2MB (non-minifié)
# - Images non-optimisées chargées au boot
# - 12 providers React au démarrage
# - Polices chargées de façon synchrone
```

**Problèmes identifiés** :
1. Bundle JS de 8.2 MB sans code splitting
2. 6 appels API au démarrage (dont 4 non-critiques)
3. Images PNG lourdes dans les assets
4. Hermes désactivé (JSC utilisé)

### Optimisations Appliquées

**1 — Activer Hermes** (gain le plus rapide) :
```json
// android/app/build.gradle
project.ext.react = [
  enableHermes: true,
]
// iOS : Build Settings → HERMES_ENABLED = YES
// Résultat : -400ms cold start immédiat
```

**2 — Lazy loading des écrans non-critiques** :
```typescript
// Avant : import direct
import EcranProfil from './EcranProfil';

// Après : lazy loading avec React.lazy
const EcranProfil = React.lazy(() => import('./EcranProfil'));
const EcranParametres = React.lazy(() => import('./EcranParametres'));
const EcranHistorique = React.lazy(() => import('./EcranHistorique'));

// Résultat : bundle initial réduit de 8.2MB → 3.1MB
```

**3 — Skeleton screens** (UX perçue) :
```typescript
// Afficher du contenu immédiatement pendant le chargement
function ListeProduits() {
  const { data, isLoading } = useQuery({ queryKey: ['produits'], queryFn: fetchProduits });

  if (isLoading) return <SkeletonListe />;
  return <FlatList data={data} renderItem={renderProduit} />;
}

// Skeleton avec Reanimated shimmer
function SkeletonListe() {
  const animation = useSharedValue(0);
  // ... shimmer animation
  return (
    <View>
      {Array(5).fill(0).map((_, i) => (
        <Animated.View key={i} style={[styles.skeletonItem, animatedStyle]} />
      ))}
    </View>
  );
}
```

**4 — Réduire les providers au démarrage** :
```typescript
// Avant : 12 providers imbriqués au boot
// Après : lazy initialization des providers non-critiques
function App() {
  return (
    <AuthProvider>           // Critique — au boot
      <ThemeProvider>        // Critique — au boot
        <NavigationContainer>
          <Suspense fallback={<SplashScreen />}>
            <LazyAnalyticsProvider>  // Non-critique — lazy
              <LazyNotificationsProvider>  // Non-critique — lazy
                <Routes />
              </LazyNotificationsProvider>
            </LazyAnalyticsProvider>
          </Suspense>
        </NavigationContainer>
      </ThemeProvider>
    </AuthProvider>
  );
}
```

### Résultats

| Métrique | Avant | Après |
|---|---|---|
| Cold start (mid-range Android) | 2,100ms | 380ms |
| Cold start (iPhone 12) | 1,200ms | 290ms |
| Bundle JS initial | 8.2 MB | 3.1 MB |
| Appels API au boot | 6 | 2 (critiques uniquement) |
| Note App Store performance | 3.2/5 | 4.6/5 |

**Leçon** : activer Hermes en premier (gain immédiat, zéro effort). Ensuite le lazy loading. Les skeleton screens améliorent la performance *perçue* sans changer les métriques réelles — et c'est ce que l'utilisateur ressent.

---

## Cas 3 — Migration Native vers Flutter : Stratégie Add-to-App

### Contexte

Groupe retail (app iOS Swift + Android Kotlin, 5 ans d'âge, 500K utilisateurs). L'équipe mobile (6 devs iOS + 6 devs Android) maintenait deux codebases divergentes. Décision : migrer vers Flutter sur 18 mois sans interruption de service.

**Contrainte clé** : l'app ne peut pas être retirée de la production. Migration progressive obligatoire.

### Stratégie Add-to-App

Flutter "Add-to-App" permet d'intégrer un `FlutterFragment` ou `FlutterViewController` dans une app native existante. On migre écran par écran.

```swift
// iOS : intégrer un écran Flutter dans l'app Swift existante
import Flutter

class PaiementViewController: UIViewController {
  override func viewDidLoad() {
    super.viewDidLoad()

    let flutterEngine = (UIApplication.shared.delegate as! AppDelegate).flutterEngine
    let flutterVC = FlutterViewController(engine: flutterEngine, nibName: nil, bundle: nil)

    addChild(flutterVC)
    view.addSubview(flutterVC.view)
    flutterVC.view.frame = view.bounds
  }
}
```

```kotlin
// Android : intégrer Flutter dans Activity existante
class PaiementActivity : AppCompatActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    val engine = (application as MainApplication).flutterEngine
    val fragment = FlutterFragment.withCachedEngineId("main_engine").build()
    supportFragmentManager.commit {
      add(R.id.flutter_container, fragment)
    }
  }
}
```

### Communication Native ↔ Flutter

```dart
// Flutter — MethodChannel pour appeler le code natif
class ServiceAuth {
  static const _channel = MethodChannel('com.monapp/auth');

  static Future<String?> obtenirToken() async {
    try {
      return await _channel.invokeMethod<String>('getAuthToken');
    } on PlatformException catch (e) {
      debugPrint('Erreur token: ${e.message}');
      return null;
    }
  }
}
```

```swift
// iOS — Handler du MethodChannel
let channel = FlutterMethodChannel(name: "com.monapp/auth",
                                   binaryMessenger: controller.binaryMessenger)
channel.setMethodCallHandler { call, result in
  if call.method == "getAuthToken" {
    result(AuthService.shared.currentToken)
  }
}
```

### Ordre de Migration

```
Phase 1 (mois 1-4) : Écrans à faible risque
  ├── Onboarding (nouveau code, peu de legacy)
  ├── Profil utilisateur
  └── Paramètres

Phase 2 (mois 5-10) : Écrans core
  ├── Catalogue produits (le plus complexe)
  ├── Recherche
  └── Compte fidélité

Phase 3 (mois 11-18) : Écrans transactionnels
  ├── Panier
  ├── Checkout / Paiement
  └── Suivi commande
```

### Résultats

| Métrique | Avant (2 codebases) | Après (Flutter) |
|---|---|---|
| Développeurs mobile | 12 (6+6) | 7 (Flutter) |
| Temps de livraison feature | 6 semaines | 3 semaines |
| Taux de crash | 0.8% | 0.2% |
| Couverture tests | 34% | 71% |
| Parité iOS/Android | 83% des features | 100% |

**Leçon** : la stratégie Add-to-App est la seule voie viable pour migrer une app en production. Migrer les écrans à faible risque en premier pour former l'équipe. Le MethodChannel est puissant mais verbose — documenter chaque interface soigneusement.

---

## Cas 4 — Application Offline-First pour Techniciens de Terrain

### Contexte

Entreprise de maintenance industrielle (280 techniciens, inspections de pipelines en zones rurales). Problème : les techniciens n'ont pas de réseau 60% du temps. L'ancienne app (PWA) perdait les données non-synchronisées.

Besoin : app React Native qui fonctionne sans réseau et synchronise intelligemment.

### Architecture Offline-First

```typescript
// La règle : toutes les opérations écrivent d'abord localement
// La synchronisation est toujours asynchrone

// sync/syncService.ts
export class ServiceSync {
  // File d'attente des opérations en attente
  private queue: SyncOperation[] = [];

  async exécuterOpération<T>(
    opLocale: () => Promise<T>,
    opDistante: () => Promise<T>,
  ): Promise<T> {
    // Toujours exécuter localement d'abord
    const résultatLocal = await opLocale();

    // Tenter la synchronisation si connecté
    if (await NetInfo.fetch().then(s => s.isConnected)) {
      try {
        await opDistante();
      } catch {
        this.queue.push({ opDistante, timestamp: Date.now() });
      }
    } else {
      this.queue.push({ opDistante, timestamp: Date.now() });
    }

    return résultatLocal;
  }

  async synchroniserQueue() {
    const opsPendantes = [...this.queue];
    this.queue = [];

    for (const op of opsPendantes) {
      try {
        await op.opDistante();
      } catch {
        this.queue.push(op); // Remettre en queue si échec
      }
    }
  }
}
```

### WatermelonDB pour le Stockage Local

```typescript
// database/inspection.model.ts
export class Inspection extends Model {
  static table = 'inspections';
  static associations = {
    photos: { type: 'has_many', foreignKey: 'inspection_id' },
  } as const;

  @field('site_id') siteId!: string;
  @field('statut') statut!: 'brouillon' | 'terminée' | 'synchronisée';
  @field('technicien_id') technicienId!: string;
  @date('débutée_à') débutéeÀ!: Date;
  @date('terminée_à') terminéeÀ?: Date;
  @json('données_formulaire', v => v) donnéesFormulaire!: Record<string, unknown>;
  @field('sync_pending') syncPending!: boolean;
}

// Créer une inspection — toujours offline-first
async function créerInspection(siteId: string) {
  return database.write(async () => {
    return database.get<Inspection>('inspections').create(inspection => {
      inspection.siteId = siteId;
      inspection.statut = 'brouillon';
      inspection.technicienId = auth.userId;
      inspection.débutéeÀ = new Date();
      inspection.syncPending = true;
    });
  });
}
```

### File d'Attente Photos avec MMKV

```typescript
// La caméra peut prendre des photos même sans réseau
// Les photos sont stockées localement et uploadées quand le réseau revient

const QUEUE_PHOTOS = 'queue_photos_upload';

interface PhotoEnAttente {
  inspectionId: string;
  uriLocale: string;
  tentatives: number;
  crééeÀ: number;
}

export class FilePhotos {
  static ajouter(photo: Omit<PhotoEnAttente, 'tentatives' | 'crééeÀ'>) {
    const queue = charger<PhotoEnAttente[]>(QUEUE_PHOTOS, []);
    queue.push({ ...photo, tentatives: 0, crééeÀ: Date.now() });
    sauvegarder(QUEUE_PHOTOS, queue);
  }

  static async traiter() {
    const queue = charger<PhotoEnAttente[]>(QUEUE_PHOTOS, []);
    const restantes: PhotoEnAttente[] = [];

    for (const photo of queue) {
      try {
        const url = await ServiceMédias.uploader(photo.uriLocale, '/api/photos');
        await api.associerPhoto(photo.inspectionId, url);
        await FileSystem.deleteAsync(photo.uriLocale, { idempotent: true });
      } catch {
        if (photo.tentatives < 3) {
          restantes.push({ ...photo, tentatives: photo.tentatives + 1 });
        }
        // Après 3 tentatives : abandon + log erreur
      }
    }

    sauvegarder(QUEUE_PHOTOS, restantes);
  }
}

// Déclencher le traitement quand le réseau revient
NetInfo.addEventListener(état => {
  if (état.isConnected && état.isInternetReachable) {
    FilePhotos.traiter();
    ServiceSync.getInstance().synchroniserQueue();
  }
});
```

### Indicateur de Connectivité

```typescript
// Bandeau persistant indiquant le statut réseau + données en attente
function BandeauConnectivité() {
  const { isConnected } = useNetInfo();
  const [enAttente, setEnAttente] = useState(0);

  useEffect(() => {
    const queue = charger<unknown[]>('queue_photos_upload', []);
    setEnAttente(queue.length);
  }, []);

  if (isConnected && enAttente === 0) return null;

  return (
    <View style={[styles.bandeau, isConnected ? styles.avertissement : styles.hors_ligne]}>
      <Text style={styles.texte}>
        {isConnected
          ? `Synchronisation en cours (${enAttente} éléments)`
          : `Hors ligne — ${enAttente} éléments en attente`}
      </Text>
    </View>
  );
}
```

### Résultats (12 Mois Post-Déploiement)

| Métrique | Avant (PWA) | Après (React Native offline-first) |
|---|---|---|
| Données perdues/mois | 340 inspections | 0 |
| Productivité techniciens | Base | +23% (plus d'attente réseau) |
| Temps de synchronisation | N/A | < 30s au retour en zone couverte |
| Adoption app | 67% | 98% |
| Erreurs de saisie | 12% | 3% (validation instantanée) |

**Leçon** : l'architecture offline-first nécessite de repenser l'UX complètement — l'utilisateur ne doit jamais voir "erreur réseau". Chaque opération doit réussir localement. WatermelonDB + MMKV est la combinaison optimale : WatermelonDB pour les données relationnelles, MMKV pour les files d'attente et l'état temporaire. Le bandeau de connectivité est indispensable pour la confiance utilisateur.
