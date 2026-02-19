---
name: mobile-development
version: 1.0.0
description: >
  Use this skill when the user asks about "développement mobile", "React Native", "Flutter", "PWA", "application mobile", "iOS", "Android", "App Store", "Google Play", "push notifications", "deep linking", "mobile architecture", "offline-first", "biometrics mobile", "Expo", "capacitor", "mobile performance", "ASO App Store Optimization", discusses building cross-platform or native mobile applications, or needs guidance on mobile development frameworks, architecture patterns, and app distribution.
---

# Développement Mobile — React Native, Flutter & PWA

## Overview

Le développement mobile en 2025-2026 se polarise entre trois approches : React Native (JavaScript/TypeScript, écosystème React), Flutter (Dart, Google), et les PWA (Progressive Web Apps, web standard). Le choix dépend de l'équipe existante, des fonctionnalités natives requises, et des contraintes de déploiement.

Le temps où chaque plateforme (iOS/Android) nécessitait une équipe dédiée est révolu pour la majorité des projets. Les frameworks cross-platform couvrent aujourd'hui 90%+ des cas d'usage avec des performances quasi-natives.

---

## Décision Guide — Choisir son Approche

### Critères de Sélection

| Critère | React Native | Flutter | PWA |
|---|---|---|---|
| **Équipe existante** | Web/React | Dart (nouveau) | Web standard |
| **Performances** | Très bonnes (JSI) | Excellentes | Bonnes |
| **Accès natif** | Via modules natifs | Via plugins | Limité (API Web) |
| **Taille d'app** | ~10-20 MB | ~20-30 MB | 0 (web) |
| **Time to market** | Rapide | Moyen | Très rapide |
| **Coût de dev** | Partage ~85% code | Partage ~95% code | 100% partagé |
| **App Store** | Oui | Oui | Non (sauf Samsung) |
| **Offline** | Excellent | Excellent | Partiel |
| **Hot Reload** | Oui | Oui (très rapide) | HMR web |

### Quand Choisir React Native

- Équipe JavaScript/TypeScript existante
- Intégration avec un écosystème React web
- Besoin d'accès natif modéré (camera, notifications, localisation)
- Écosystème npm (millions de packages)
- Expo : idéal pour démarrer rapidement sans config native

```typescript
// React Native avec Expo — démarrage ultra-rapide
// npx create-expo-app my-app --template blank-typescript

import { View, Text, StyleSheet } from 'react-native';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Mon App React Native</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
  },
});
```

### Quand Choisir Flutter

- Nouveau projet sans contrainte d'équipe
- Performances critiques (animations 60/120fps, graphiques)
- UI très customisée (Flutter contrôle chaque pixel)
- Applications desktop en plus du mobile (Flutter supporte macOS, Windows, Linux)
- Préférence pour la compilation AOT (Ahead-of-Time)

```dart
// Flutter — widget composable
import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Mon App Flutter')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Bienvenue',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            ElevatedButton(
              onPressed: () {},
              child: Text('Action'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### Quand Choisir PWA

- Application principalement web avec quelques features mobiles
- Pas besoin de l'App Store (distribution directe, enterprise)
- Contraintes de budget/délai très fortes
- Fonctionnalités natives limitées (pas de camera avancée, pas de Bluetooth)
- B2B interne, portail client, tableau de bord

---

## Architecture Mobile

### Clean Architecture pour Mobile

```
lib/ (Flutter) ou src/ (React Native)
├── presentation/       # UI, screens, widgets
│   ├── screens/
│   ├── widgets/
│   └── state/          # State management
├── domain/             # Business logic (pas de dépendances UI)
│   ├── entities/
│   ├── repositories/   # Interfaces
│   └── usecases/
├── data/               # Implémentation des repositories
│   ├── repositories/
│   ├── datasources/    # API, local DB
│   └── models/         # DTOs
└── core/
    ├── errors/
    ├── network/
    └── utils/
```

### State Management

**React Native** :
- **Zustand** : simple, performant, minimal boilerplate (recommandé pour la majorité)
- **Redux Toolkit** : si application très complexe avec beaucoup d'état partagé
- **Jotai** : atomic state, excellent pour les états granulaires
- **React Query / TanStack Query** : pour le server state (cache, sync, loading states)

```typescript
// Zustand store — simple et efficace
import { create } from 'zustand';

interface AuthStore {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  isAuthenticated: false,
  login: async (credentials) => {
    const user = await authService.login(credentials);
    set({ user, isAuthenticated: true });
  },
  logout: () => set({ user: null, isAuthenticated: false }),
}));
```

**Flutter** :
- **Riverpod** : le plus robuste, type-safe, testable (recommandé)
- **Bloc/Cubit** : pattern Redux-like, excellent pour les équipes venant d'Angular
- **Provider** : simple, officiel Google, limité pour les gros projets

### Navigation

**React Native** :
- **React Navigation** : standard de l'écosystème
  - Stack Navigator (push/pop)
  - Tab Navigator (bottom tabs)
  - Drawer Navigator (side menu)
- **Expo Router** : file-based routing (comme Next.js), recommandé avec Expo

**Flutter** :
- **GoRouter** : URL-based routing, deep link natif
- **Navigator 2.0** : API officielle, plus verbeux

---

## Fonctionnalités Natives Essentielles

### Push Notifications

**React Native avec Expo** :
```typescript
import * as Notifications from 'expo-notifications';
import { registerForPushNotificationsAsync } from './notifications';

// Demander la permission
const { status } = await Notifications.requestPermissionsAsync();
if (status !== 'granted') {
  alert('Permission refusée pour les notifications');
  return;
}

// Obtenir le token Expo Push
const token = await Notifications.getExpoPushTokenAsync({
  projectId: Constants.expoConfig?.extra?.eas?.projectId,
});

// Envoyer au backend pour stockage
await api.registerPushToken(token.data);

// Configurer le handler de réception
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});
```

**Backend (Node.js)** :
```javascript
// Envoyer via Expo Push API
const messages = tokens.map(token => ({
  to: token,
  title: 'Nouveau message',
  body: 'Vous avez un nouveau message de Pierre',
  data: { screen: 'Messages', threadId: '123' },
}));

await fetch('https://exp.host/--/api/v2/push/send', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(messages),
});
```

### Deep Linking

Permettre à une URL d'ouvrir une page spécifique de l'app.

**React Navigation + Expo** :
```typescript
// app.json
{
  "expo": {
    "scheme": "myapp",  // myapp://
    "intentFilters": [  // Android
      {
        "action": "VIEW",
        "data": { "scheme": "https", "host": "myapp.com" }
      }
    ]
  }
}

// Navigation linking config
const linking = {
  prefixes: ['myapp://', 'https://myapp.com'],
  config: {
    screens: {
      Home: '',
      Profile: 'user/:id',
      Product: 'products/:productId',
    },
  },
};

<NavigationContainer linking={linking}>
```

### Biométrie (Face ID / Fingerprint)

```typescript
import * as LocalAuthentication from 'expo-local-authentication';

async function authenticateWithBiometrics(): Promise<boolean> {
  // Vérifier la disponibilité
  const compatible = await LocalAuthentication.hasHardwareAsync();
  if (!compatible) return false;

  const enrolled = await LocalAuthentication.isEnrolledAsync();
  if (!enrolled) {
    Alert.alert('Aucune biométrie configurée sur cet appareil');
    return false;
  }

  // Authentifier
  const result = await LocalAuthentication.authenticateAsync({
    promptMessage: 'Confirmer votre identité',
    fallbackLabel: 'Utiliser le code PIN',
    cancelLabel: 'Annuler',
  });

  return result.success;
}
```

### Stockage Local et Offline-First

```typescript
// MMKV — stockage synchrone ultra-rapide (alternative à AsyncStorage)
import { MMKV } from 'react-native-mmkv';

const storage = new MMKV();
storage.set('user.token', 'eyJ...');
const token = storage.getString('user.token');

// WatermelonDB — base de données relationnelle performante pour offline-first
// Synchronise avec le backend quand la connexion est disponible
import { synchronize } from '@nozbe/watermelondb/sync';

await synchronize({
  database,
  pullChanges: async ({ lastPulledAt }) => {
    const response = await api.pull({ lastPulledAt });
    return { changes: response.changes, timestamp: response.timestamp };
  },
  pushChanges: async ({ changes }) => {
    await api.push({ changes });
  },
});
```

---

## Performance Mobile

### Mesurer les Performances

**React Native Profiler** : intégré dans React DevTools. Identifier les composants qui re-rendent inutilement.

**Flipper** : outil de debugging Facebook/Meta. Profiling réseau, base de données, performance.

**Détecteur de rendus excessifs** :
```typescript
// Activer en développement
if (__DEV__) {
  const whyDidYouRender = require('@welldone-software/why-did-you-render');
  whyDidYouRender(React, { trackAllPureComponents: true });
}
```

### Optimisations Clés

**FlatList vs ScrollView** : toujours utiliser FlatList/SectionList pour les listes longues. ScrollView rend tous les éléments simultanément.

```typescript
// FlatList avec optimisations
<FlatList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  keyExtractor={(item) => item.id}
  // Performances
  maxToRenderPerBatch={10}
  windowSize={5}
  removeClippedSubviews={true}
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,  // hauteur fixe = beaucoup plus rapide
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>
```

**Memo et Callbacks** :
```typescript
// Éviter les re-renders inutiles
const ItemCard = React.memo(({ item, onPress }) => {
  return <TouchableOpacity onPress={() => onPress(item.id)}>...</TouchableOpacity>;
});

// Stabiliser les callbacks
const handlePress = useCallback((id: string) => {
  navigation.navigate('Detail', { id });
}, [navigation]);
```

---

## App Store Optimization (ASO)

### App Store (iOS) — Éléments Clés

**Title** (30 chars) : mot-clé principal + nom app. Ex: "Slack: Messagerie pro équipe".

**Subtitle** (30 chars) : 2ème mot-clé fort. Ex: "Chat, vidéo & collaboration".

**Keywords field** (100 chars) : mots-clés séparés par virgules, pas de répétition du titre.

**Screenshots** : 6-10 screenshots avec texte descriptif. Le 1er est le plus important (seul visible dans la recherche). Tester différentes versions.

**App Preview video** : 15-30s. Montre le coeur du produit. Augmente la conversion de 20-35%.

**Ratings** : demander une évaluation au bon moment (après une action réussie, pas à l'ouverture).

```typescript
import * as StoreReview from 'expo-store-review';

// Demander après 3 actions réussies (panier validé, document créé, etc.)
if (successfulActionsCount >= 3 && await StoreReview.isAvailableAsync()) {
  await StoreReview.requestReview();
}
```

### Play Store (Android)

Similaire à l'App Store avec quelques différences :
- **Short description** (80 chars) : tagline
- **Long description** (4000 chars) : inclure les mots-clés naturellement
- Indexation Google : Google indexe le contenu de la description (comme le SEO web)

---

## Maturity Model — Mobile Development

| Niveau | Caractéristique |
|---|---|
| **1 — Web uniquement** | Pas d'app mobile, site web non responsive |
| **2 — PWA de base** | Site web responsive + manifest.json, installable |
| **3 — App cross-platform** | React Native ou Flutter, fonctionnalités natives basiques |
| **4 — App production** | CI/CD, push notifications, deep linking, analytics, crash reporting |
| **5 — Mobile-first** | Offline-first, performance optimisée, ASO actif, A/B testing |
