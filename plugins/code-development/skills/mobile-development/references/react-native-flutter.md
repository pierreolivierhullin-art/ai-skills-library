# React Native vs Flutter — Comparaison approfondie

## Vue d'ensemble

React Native et Flutter sont les deux frameworks de développement mobile multiplateforme les plus adoptés en 2025. Ce document compare en profondeur leur architecture, leurs performances, leurs écosystèmes et fournit des exemples de code côte à côte pour les cas d'usage courants.

---

## React Native

### Architecture et philosophie

React Native repose sur JavaScript/TypeScript et le paradigme React. L'interface utilisateur est rendue par des composants natifs réels de la plateforme (UIView sur iOS, View sur Android), ce qui garantit une apparence et un comportement authentiquement natifs.

#### Expo Workflow vs Bare Workflow

**Expo Managed Workflow** est le point d'entrée recommandé pour les nouveaux projets :

```bash
# Initialiser un projet Expo
npx create-expo-app mon-app --template blank-typescript
cd mon-app
npx expo start
```

Avantages du Managed Workflow :
- Pas de configuration native requise (Xcode, Android Studio optionnels)
- Over-the-air updates (OTA) via EAS Update
- Accès à toutes les APIs natives via les modules Expo
- Build cloud via EAS Build sans machine Mac pour iOS

Limites du Managed Workflow :
- Impossible d'ajouter du code natif personnalisé directement
- Taille de l'app plus grande (SDK Expo inclus)
- Moins de contrôle sur les configurations natives

**Bare Workflow** offre un contrôle total :

```bash
# Éjecter vers le bare workflow
npx expo eject

# Ou initialiser directement
npx react-native init MonApp --template react-native-template-typescript
```

Le bare workflow est nécessaire quand :
- Des modules natifs personnalisés (Objective-C/Swift, Kotlin/Java) sont requis
- Les performances sont critiques et nécessitent des optimisations bas niveau
- Des SDKs tiers natifs doivent être intégrés (ex: SDK Stripe natif, ARKit)

---

### JSI — JavaScript Interface pour la performance native

La JSI (JavaScript Interface) est l'innovation architecturale centrale de la Nouvelle Architecture React Native. Elle remplace l'ancien pont asynchrone basé sur JSON par une interface C++ synchrone.

**Ancien pont (à éviter) :**
```
JS Thread → Sérialisation JSON → Bridge → Désérialisation → Native Thread
```

**JSI (moderne) :**
```
JS Thread → Référence directe C++ → Native Thread (synchrone)
```

Implémentation d'un module natif avec JSI :

```cpp
// NativeCalculator.cpp
#include "NativeCalculator.h"

namespace facebook::react {

NativeCalculator::NativeCalculator(std::shared_ptr<CallInvoker> jsInvoker)
    : NativeCalculatorCxxSpec<NativeCalculator>(std::move(jsInvoker)) {}

double NativeCalculator::add(jsi::Runtime& rt, double a, double b) {
  return a + b; // Appel synchrone, aucune sérialisation
}

} // namespace facebook::react
```

```typescript
// Utilisation côté TypeScript
import { NativeModules } from 'react-native';
const { NativeCalculator } = NativeModules;

// Appel synchrone via JSI
const result = NativeCalculator.add(1.5, 2.5); // = 4.0
```

---

### Nouvelle Architecture — Fabric + TurboModules

**Fabric** est le nouveau moteur de rendu React Native :
- Rendu synchrone possible (suppression des lags de l'ancien modèle asynchrone)
- Support du mode concurrent React (Suspense, Transitions)
- Meilleure gestion de la priorité des mises à jour UI

**TurboModules** remplacent les Native Modules classiques :
- Chargement paresseux (lazy loading) des modules natifs
- Types sûrs grâce à la spécification CodeGen
- Réduction du temps de démarrage de 15 à 40%

Activation dans `android/gradle.properties` :

```properties
newArchEnabled=true
```

Et dans `ios/Podfile` :

```ruby
# Nouvelle Architecture activée par défaut depuis RN 0.74
ENV['RCT_NEW_ARCH_ENABLED'] = '1'
```

---

### Bibliothèques clés React Native

#### React Navigation 6+ — Navigation

```typescript
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

type RootStackParams = {
  Accueil: undefined;
  Profil: { userId: string };
  Parametres: undefined;
};

const Stack = createStackNavigator<RootStackParams>();
const Tab = createBottomTabNavigator();

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        tabBarStyle: { paddingBottom: 8 },
      }}
    >
      <Tab.Screen name="Accueil" component={AccueilScreen} />
      <Tab.Screen name="Profil" component={ProfilScreen} />
    </Tab.Navigator>
  );
}

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Accueil">
        <Stack.Screen name="Accueil" component={TabNavigator} />
        <Stack.Screen
          name="Profil"
          component={ProfilScreen}
          options={{ title: 'Mon Profil' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

#### TanStack Query — Gestion des données asynchrones

```typescript
import { QueryClient, useQuery, useMutation } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});

// Hook personnalisé typé avec pagination
function useUtilisateurs(page: number) {
  return useQuery({
    queryKey: ['utilisateurs', page],
    queryFn: () => api.getUtilisateurs(page),
    placeholderData: (previousData) => previousData,
  });
}

// Mutation avec invalidation de cache automatique
function useCreerUtilisateur() {
  return useMutation({
    mutationFn: api.creerUtilisateur,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['utilisateurs'] });
    },
  });
}
```

#### Zustand — Gestion d'état légère et typée

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthState {
  utilisateur: Utilisateur | null;
  token: string | null;
  connecter: (credentials: Credentials) => Promise<void>;
  deconnecter: () => void;
}

const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      utilisateur: null,
      token: null,
      connecter: async (credentials) => {
        const { utilisateur, token } = await api.auth.login(credentials);
        set({ utilisateur, token });
      },
      deconnecter: () => set({ utilisateur: null, token: null }),
    }),
    {
      name: 'auth-store',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

#### MMKV — Stockage synchrone ultra-rapide

```typescript
import { MMKV } from 'react-native-mmkv';

// MMKV est environ 10x plus rapide qu'AsyncStorage
const storage = new MMKV({
  id: 'app-storage',
  encryptionKey: process.env.MMKV_KEY,
});

// Lecture et écriture synchrones (aucun await requis)
storage.set('preferences', JSON.stringify({ theme: 'sombre', langue: 'fr' }));
const preferences = JSON.parse(storage.getString('preferences') ?? '{}');

// Intégration avec Zustand pour la persistance typée
const zustandMMKVStorage = {
  getItem: (name: string) => storage.getString(name) ?? null,
  setItem: (name: string, value: string) => storage.set(name, value),
  removeItem: (name: string) => storage.delete(name),
};
```

#### Reanimated 3 — Animations fluides à 60/120 fps

```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  interpolate,
  Extrapolation,
} from 'react-native-reanimated';

function CarteAnimee({ estOuverte }: { estOuverte: boolean }) {
  const hauteur = useSharedValue(estOuverte ? 200 : 80);

  // S'exécute entièrement sur le thread UI natif — zéro jank
  const styleAnime = useAnimatedStyle(() => ({
    height: withSpring(estOuverte ? 200 : 80, {
      damping: 15,
      stiffness: 100,
    }),
    opacity: interpolate(
      hauteur.value,
      [80, 200],
      [0.7, 1],
      Extrapolation.CLAMP
    ),
  }));

  return (
    <Animated.View style={[styles.carte, styleAnime]}>
      <Contenu />
    </Animated.View>
  );
}
```

---

## Flutter

### Dart — Bases du langage

Dart est le langage compilé AOT (Ahead-of-Time) utilisé par Flutter. Sa syntaxe est proche de TypeScript et Kotlin, avec null-safety obligatoire depuis Dart 2.12.

```dart
// Types null-safe : le compilateur interdit les erreurs de null
String? nomOptionnel = null;
String nomObligatoire = 'Flutter';

// Classe immutable avec constructeur const
class Utilisateur {
  final String id;
  final String email;
  final DateTime creeA;

  const Utilisateur({
    required this.id,
    required this.email,
    required this.creeA,
  });

  // Constructeur factory pour la désérialisation JSON
  factory Utilisateur.depuisJson(Map<String, dynamic> json) {
    return Utilisateur(
      id: json['id'] as String,
      email: json['email'] as String,
      creeA: DateTime.parse(json['cree_a'] as String),
    );
  }

  Map<String, dynamic> versJson() => {
    'id': id,
    'email': email,
    'cree_a': creeA.toIso8601String(),
  };
}

// Extensions — enrichir les types existants
extension StringExtensions on String {
  String capitaliser() =>
      isEmpty ? this : '${this[0].toUpperCase()}${substring(1)}';

  bool get estEmailValide =>
      RegExp(r'^[\w.-]+@[\w.-]+\.[a-z]{2,}$').hasMatch(this);
}
```

### Arbre de widgets — Tout est widget

Flutter construit son interface via un arbre de widgets immuables. Layout, style, animation et logique sont tous des widgets.

```dart
class CarteProduit extends StatelessWidget {
  final Produit produit;
  final VoidCallback onAjouterAuPanier;

  const CarteProduit({
    super.key,
    required this.produit,
    required this.onAjouterAuPanier,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          ClipRRect(
            borderRadius: const BorderRadius.vertical(top: Radius.circular(12)),
            child: Image.network(
              produit.imageUrl,
              height: 180,
              width: double.infinity,
              fit: BoxFit.cover,
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  produit.nom,
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 8),
                Text(
                  '${produit.prix.toStringAsFixed(2)} €',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    color: Theme.of(context).colorScheme.primary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                FilledButton.icon(
                  onPressed: onAjouterAuPanier,
                  icon: const Icon(Icons.shopping_cart),
                  label: const Text('Ajouter au panier'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

### Moteur de rendu Skia/Impeller

Flutter dessine sa propre interface via Skia (ou Impeller depuis Flutter 3.10) — sans composants natifs OS. Cela garantit une cohérence pixel-perfect entre iOS et Android, mais implique une apparence moins "native" par défaut.

### Riverpod 2 — Gestion d'état réactive

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// FutureProvider pour les données asynchrones avec cache
final utilisateursProvider = FutureProvider.family<List<Utilisateur>, int>(
  (ref, page) async {
    final repo = ref.watch(userRepositoryProvider);
    return repo.getUtilisateurs(page: page);
  },
);

// NotifierProvider pour la logique d'état complexe
final panierProvider = NotifierProvider<PanierNotifier, PanierState>(
  PanierNotifier.new,
);

class PanierNotifier extends Notifier<PanierState> {
  @override
  PanierState build() => const PanierState(articles: []);

  void ajouterArticle(Produit produit) {
    state = state.copyWith(
      articles: [...state.articles, ArticlePanier(produit: produit, quantite: 1)],
    );
  }

  void retirerArticle(String produitId) {
    state = state.copyWith(
      articles: state.articles.where((a) => a.produit.id != produitId).toList(),
    );
  }
}

// Widget qui se reconstruit uniquement quand l'état change
class EcranPanier extends ConsumerWidget {
  const EcranPanier({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final panier = ref.watch(panierProvider);
    return ListView.builder(
      itemCount: panier.articles.length,
      itemBuilder: (ctx, i) => ArticlePanierTile(article: panier.articles[i]),
    );
  }
}
```

### GoRouter — Navigation type-safe

```dart
import 'package:go_router/go_router.dart';

final routeurProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authStateProvider);

  return GoRouter(
    initialLocation: '/',
    redirect: (context, state) {
      if (!authState.estConnecte && !state.matchedLocation.startsWith('/auth')) {
        return '/auth/connexion';
      }
      return null;
    },
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const EcranAccueil(),
        routes: [
          GoRoute(
            path: 'produit/:id',
            builder: (context, state) => EcranProduit(
              id: state.pathParameters['id']!,
            ),
          ),
        ],
      ),
      GoRoute(
        path: '/panier',
        builder: (context, state) => const EcranPanier(),
      ),
    ],
  );
});
```

### Dio — Client HTTP avec intercepteurs

```dart
import 'package:dio/dio.dart';

class ApiClient {
  late final Dio _dio;

  ApiClient({required String baseUrl, required String token}) {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 30),
      headers: {'Content-Type': 'application/json'},
    ));

    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) {
        options.headers['Authorization'] = 'Bearer $token';
        handler.next(options);
      },
      onError: (error, handler) async {
        if (error.response?.statusCode == 401) {
          await rafraichirToken();
          handler.resolve(await _dio.fetch(error.requestOptions));
        } else {
          handler.next(error);
        }
      },
    ));
  }

  Future<List<Produit>> getProduits({int page = 1}) async {
    final reponse = await _dio.get('/produits', queryParameters: {'page': page});
    return (reponse.data as List).map(Produit.depuisJson).toList();
  }
}
```

### Hive — Stockage local NoSQL

```dart
import 'package:hive_flutter/hive_flutter.dart';

@HiveType(typeId: 0)
class CacheProduit extends HiveObject {
  @HiveField(0)
  final String id;

  @HiveField(1)
  final String donnees;

  @HiveField(2)
  final DateTime expiresA;

  CacheProduit({required this.id, required this.donnees, required this.expiresA});

  bool get estValide => DateTime.now().isBefore(expiresA);
}

// Initialisation au démarrage
await Hive.initFlutter();
Hive.registerAdapter(CacheProduitAdapter());
final boite = await Hive.openBox<CacheProduit>('cache');

// Pattern cache-then-network
Future<Produit> getProduit(String id) async {
  final cache = boite.get(id);
  if (cache != null && cache.estValide) {
    return Produit.depuisJson(jsonDecode(cache.donnees));
  }
  final produit = await api.getProduit(id);
  await boite.put(id, CacheProduit(
    id: id,
    donnees: jsonEncode(produit.versJson()),
    expiresA: DateTime.now().add(const Duration(hours: 1)),
  ));
  return produit;
}
```

---

## Comparaison côte à côte — Formulaire avec validation

**React Native (TypeScript + React Hook Form + Zod) :**

```typescript
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schemaConnexion = z.object({
  email: z.string().email('Email invalide'),
  motDePasse: z.string().min(8, 'Minimum 8 caractères'),
});

type FormConnexion = z.infer<typeof schemaConnexion>;

function FormulaireConnexion() {
  const { control, handleSubmit, formState: { errors } } =
    useForm<FormConnexion>({ resolver: zodResolver(schemaConnexion) });

  return (
    <View style={styles.conteneur}>
      <Controller
        control={control}
        name="email"
        render={({ field: { onChange, value } }) => (
          <TextInput
            value={value}
            onChangeText={onChange}
            placeholder="Email"
            keyboardType="email-address"
            autoCapitalize="none"
          />
        )}
      />
      {errors.email && <Text style={styles.erreur}>{errors.email.message}</Text>}
      <Button title="Se connecter" onPress={handleSubmit(onSoumettre)} />
    </View>
  );
}
```

**Flutter (Dart + Form widget natif) :**

```dart
class FormulaireConnexion extends StatefulWidget {
  const FormulaireConnexion({super.key});

  @override
  State<FormulaireConnexion> createState() => _FormulaireConnexionState();
}

class _FormulaireConnexionState extends State<FormulaireConnexion> {
  final _cle = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _motDePasseController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _cle,
      child: Column(
        children: [
          TextFormField(
            controller: _emailController,
            decoration: const InputDecoration(labelText: 'Email'),
            keyboardType: TextInputType.emailAddress,
            validator: (valeur) {
              if (valeur == null || !valeur.contains('@')) {
                return 'Email invalide';
              }
              return null;
            },
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: () {
              if (_cle.currentState!.validate()) {
                context.read<AuthNotifier>().connecter(
                  email: _emailController.text,
                  motDePasse: _motDePasseController.text,
                );
              }
            },
            child: const Text('Se connecter'),
          ),
        ],
      ),
    );
  }
}
```

---

## Tableau de décision

| Critère | React Native | Flutter |
|---|---|---|
| Expérience requise | JavaScript/TypeScript | Dart (à apprendre) |
| Apparence native OS | Oui (composants système) | Non (moteur propre, cohérent) |
| Performance rendu | Très bonne (JSI + Fabric) | Excellente (AOT, 120fps) |
| Taille de l'app | ~15 Mo | ~25 Mo (moteur Skia) |
| Écosystème packages | Très large (npm) | Excellent et croissant |
| Support Web | Expérimental | Stable |
| Support Desktop | Limité | Windows, macOS, Linux |
| Hot reload | Oui | Oui (plus rapide) |
| Entreprises majeures | Meta, Shopify, Discord | Google, Alibaba, BMW |

**Choisir React Native si** : équipe JavaScript existante, apparence native stricte requise, partage de code avec une application web React.

**Choisir Flutter si** : performances critiques à 120fps, UI entièrement personnalisée, déploiement multi-plateformes complet (mobile + web + desktop + embarqué).
