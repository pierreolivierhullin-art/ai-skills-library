# Fonctionnalités Natives Mobile — Guide d'Implémentation

## Vue d'Ensemble

Les fonctionnalités natives différencient une application mobile d'un site web. Ce guide couvre l'implémentation des APIs natives essentielles en React Native (Expo) et Flutter, avec du code de production prêt à l'emploi.

---

## Notifications Push

### Architecture

```
Application mobile → FCM (Android) / APNs (iOS) → Appareil utilisateur
         ↑
Backend (votre serveur) décide quand et à qui envoyer
```

Trois acteurs : votre backend, l'infrastructure Firebase/Apple, et l'application. Le token push est l'identifiant unique de l'installation.

### Expo Notifications — Setup Complet

```typescript
// notifications/service.ts
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import Constants from 'expo-constants';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

export class ServiceNotifications {
  static async initialiser(): Promise<string | null> {
    if (!Device.isDevice) {
      console.warn('Notifications: appareil physique requis');
      return null;
    }

    const { status: existant } = await Notifications.getPermissionsAsync();
    let statut = existant;

    if (existant !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      statut = status;
    }

    if (statut !== 'granted') return null;

    if (Platform.OS === 'android') {
      await Notifications.setNotificationChannelAsync('default', {
        name: 'Notifications générales',
        importance: Notifications.AndroidImportance.MAX,
        vibrationPattern: [0, 250, 250, 250],
      });

      await Notifications.setNotificationChannelAsync('alertes', {
        name: 'Alertes urgentes',
        importance: Notifications.AndroidImportance.HIGH,
        enableLights: true,
        lightColor: '#FF0000',
      });
    }

    const token = await Notifications.getExpoPushTokenAsync({
      projectId: Constants.expoConfig?.extra?.eas?.projectId,
    });

    return token.data;
  }

  static configurerEcouteurs(
    onReçue: (n: Notifications.Notification) => void,
    onCliquée: (r: Notifications.NotificationResponse) => void,
  ) {
    const s1 = Notifications.addNotificationReceivedListener(onReçue);
    const s2 = Notifications.addNotificationResponseReceivedListener(onCliquée);
    return () => {
      Notifications.removeNotificationSubscription(s1);
      Notifications.removeNotificationSubscription(s2);
    };
  }

  static async envoyerLocale(titre: string, corps: string, données?: Record<string, unknown>) {
    await Notifications.scheduleNotificationAsync({
      content: { title: titre, body: corps, data: données ?? {}, badge: 1 },
      trigger: null, // immédiat
    });
  }
}
```

```typescript
// Hook React
function useNotifications() {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    ServiceNotifications.initialiser().then(t => {
      setToken(t);
      if (t) api.enregistrerTokenPush(t);
    });

    return ServiceNotifications.configurerEcouteurs(
      (n) => console.log('Notification reçue:', n.request.content.title),
      (r) => {
        const data = r.notification.request.content.data;
        if (data.type === 'commande') {
          navigation.navigate('DétailCommande', { id: data.id });
        }
      },
    );
  }, []);

  return { token };
}
```

### Backend Node.js avec Expo SDK

```typescript
import { Expo, ExpoPushMessage } from 'expo-server-sdk';

const expo = new Expo({ accessToken: process.env.EXPO_ACCESS_TOKEN });

export async function envoyerNotification(tokens: string[], titre: string, corps: string, données?: Record<string, unknown>) {
  const messages: ExpoPushMessage[] = tokens
    .filter(Expo.isExpoPushToken)
    .map(to => ({ to, sound: 'default', title: titre, body: corps, data: données ?? {} }));

  const chunks = expo.chunkPushNotifications(messages);
  for (const chunk of chunks) {
    const tickets = await expo.sendPushNotificationsAsync(chunk);
    tickets.forEach((ticket, i) => {
      if (ticket.status === 'error' && ticket.details?.error === 'DeviceNotRegistered') {
        supprimerToken(tokens[i]);
      }
    });
  }
}
```

---

## Deep Linking

### iOS — Universal Links

```xml
<!-- ios/MonApp/MonApp.entitlements -->
<key>com.apple.developer.associated-domains</key>
<array>
  <string>applinks:monapp.com</string>
</array>
```

```json
// https://monapp.com/.well-known/apple-app-site-association
{
  "applinks": {
    "details": [{
      "appIDs": ["TEAMID.com.monapp.ios"],
      "components": [
        { "/": "/produit/*" },
        { "/": "/commande/*" }
      ]
    }]
  }
}
```

### Android — App Links

```xml
<!-- AndroidManifest.xml -->
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="https" android:host="monapp.com" />
</intent-filter>
<intent-filter>
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="monapp" />
</intent-filter>
```

### Gestion dans l'Application

```typescript
// Configuration React Navigation
const linking = {
  prefixes: ['monapp://', 'https://monapp.com'],
  config: {
    screens: {
      Accueil: '',
      Produit: 'produit/:id',
      Commande: 'commande/:commandeId',
    },
  },
};

// Gérer le lien initial (app fermée)
useEffect(() => {
  Linking.getInitialURL().then(url => {
    if (url) traiterLienProfond(url);
  });

  const abonnement = Linking.addEventListener('url', ({ url }) => traiterLienProfond(url));
  return () => abonnement.remove();
}, []);
```

---

## Authentification Biométrique

```typescript
import * as LocalAuthentication from 'expo-local-authentication';

export class ServiceBiométrique {
  static async disponible(): Promise<{ ok: boolean; types: string[] }> {
    const hardware = await LocalAuthentication.hasHardwareAsync();
    if (!hardware) return { ok: false, types: [] };

    const inscrit = await LocalAuthentication.isEnrolledAsync();
    if (!inscrit) return { ok: false, types: [] };

    const types = await LocalAuthentication.supportedAuthenticationTypesAsync();
    const noms = types.map(t => {
      switch (t) {
        case LocalAuthentication.AuthenticationType.FINGERPRINT: return 'Empreinte';
        case LocalAuthentication.AuthenticationType.FACIAL_RECOGNITION: return 'Face ID';
        default: return 'Biométrie';
      }
    });

    return { ok: true, types: noms };
  }

  static async authentifier(message = 'Confirmez votre identité'): Promise<boolean> {
    const { ok } = await this.disponible();
    if (!ok) return false;

    const résultat = await LocalAuthentication.authenticateAsync({
      promptMessage: message,
      cancelLabel: 'Annuler',
      disableDeviceFallback: false,
      fallbackLabel: 'Code PIN',
    });

    return résultat.success;
  }
}

// Composant écran protégé
function EcranProtégé({ children }: { children: React.ReactNode }) {
  const [ok, setOk] = useState(false);

  useEffect(() => {
    ServiceBiométrique.authentifier('Déverrouillez l\'application').then(succès => {
      setOk(succès);
      if (!succès) navigation.goBack();
    });
  }, []);

  if (!ok) return <ActivityIndicator />;
  return <>{children}</>;
}
```

---

## Caméra et Gestion des Médias

```typescript
import * as ImagePicker from 'expo-image-picker';
import { manipulateAsync, SaveFormat } from 'expo-image-manipulator';

export class ServiceMédias {
  static async demanderPermissions(): Promise<boolean> {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    return status === 'granted';
  }

  static async choisirImage(opts = { aspect: [4, 3] as [number, number] }) {
    const résultat = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: opts.aspect,
      quality: 0.8,
    });
    return résultat.canceled ? null : résultat.assets[0];
  }

  static async prendrePhoto() {
    const résultat = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.8,
    });
    return résultat.canceled ? null : résultat.assets[0];
  }

  // Optimiser avant upload : resize + compression
  static async optimiser(uri: string): Promise<string> {
    const résultat = await manipulateAsync(
      uri,
      [{ resize: { width: 1024 } }],
      { compress: 0.75, format: SaveFormat.JPEG },
    );
    return résultat.uri;
  }

  static async uploader(uri: string, endpoint: string): Promise<string> {
    const uriOpt = await this.optimiser(uri);
    const form = new FormData();
    form.append('image', { uri: uriOpt, type: 'image/jpeg', name: `img_${Date.now()}.jpg` } as never);
    const resp = await fetch(endpoint, { method: 'POST', body: form });
    const { url } = await resp.json();
    return url;
  }
}
```

---

## Géolocalisation

```typescript
import * as Location from 'expo-location';
import * as TaskManager from 'expo-task-manager';

const TASK_SUIVI = 'SUIVI_GPS';

TaskManager.defineTask(TASK_SUIVI, async ({ data, error }) => {
  if (error) { console.error(error); return; }
  const { locations } = data as { locations: Location.LocationObject[] };
  await api.mettreAJourPosition(locations[locations.length - 1]);
});

export class ServiceLocalisation {
  static async obtenirPosition() {
    const { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') throw new Error('Permission refusée');
    return Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Balanced });
  }

  static async démarrerSuivi() {
    const { status } = await Location.requestBackgroundPermissionsAsync();
    if (status !== 'granted') throw new Error('Permission arrière-plan refusée');

    await Location.startLocationUpdatesAsync(TASK_SUIVI, {
      accuracy: Location.Accuracy.Balanced,
      timeInterval: 30000,
      distanceInterval: 50,
      foregroundService: {
        notificationTitle: 'Suivi actif',
        notificationBody: 'Votre position est partagée',
      },
    });
  }

  static arrêterSuivi() {
    return Location.stopLocationUpdatesAsync(TASK_SUIVI);
  }

  static distanceHaversine(
    p1: { latitude: number; longitude: number },
    p2: { latitude: number; longitude: number },
  ): number {
    const R = 6371e3;
    const φ1 = (p1.latitude * Math.PI) / 180;
    const φ2 = (p2.latitude * Math.PI) / 180;
    const Δφ = ((p2.latitude - p1.latitude) * Math.PI) / 180;
    const Δλ = ((p2.longitude - p1.longitude) * Math.PI) / 180;
    const a = Math.sin(Δφ / 2) ** 2 + Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) ** 2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  }
}
```

---

## Bluetooth BLE

```typescript
import { BleManager, Device } from 'react-native-ble-plx';

const UUID_BATTERIE = '0000180f-0000-1000-8000-00805f9b34fb';
const UUID_NIVEAU = '00002a19-0000-1000-8000-00805f9b34fb';

export class ServiceBluetooth {
  private manager = new BleManager();
  private connectés = new Map<string, Device>();

  async scanner(
    onTrouvé: (d: Device) => void,
    durée = 10000,
    serviceUUIDs?: string[],
  ) {
    this.manager.startDeviceScan(serviceUUIDs ?? null, { allowDuplicates: false }, (err, device) => {
      if (err) { console.error(err); return; }
      if (device) onTrouvé(device);
    });
    setTimeout(() => this.manager.stopDeviceScan(), durée);
  }

  async connecter(id: string): Promise<Device> {
    this.manager.stopDeviceScan();
    const device = await this.manager.connectToDevice(id);
    await device.discoverAllServicesAndCharacteristics();
    this.connectés.set(id, device);
    return device;
  }

  async lireNiveauBatterie(id: string): Promise<number> {
    const device = this.connectés.get(id);
    if (!device) throw new Error('Appareil non connecté');
    const c = await device.readCharacteristicForService(UUID_BATTERIE, UUID_NIVEAU);
    return Buffer.from(c.value!, 'base64').readUInt8(0);
  }

  déconnecter(id: string) {
    this.connectés.get(id)?.cancelConnection();
    this.connectés.delete(id);
  }
}
```

---

## Capteurs — Accéléromètre et Détection de Secousse

```typescript
import { Accelerometer } from 'expo-sensors';

export class ServiceCapteurs {
  static démarrerAccéléromètre(
    onDonnées: (d: { x: number; y: number; z: number }) => void,
    intervalleMs = 100,
  ) {
    Accelerometer.setUpdateInterval(intervalleMs);
    const sub = Accelerometer.addListener(onDonnées);
    return () => sub.remove();
  }

  static détecterSecousse(onSecousse: () => void) {
    const SEUIL = 1.5;
    let dernière = 0;

    return this.démarrerAccéléromètre(({ x, y, z }) => {
      const acc = Math.sqrt(x * x + y * y + z * z);
      const now = Date.now();
      if (acc > SEUIL && now - dernière > 1000) {
        dernière = now;
        onSecousse();
      }
    }, 50);
  }
}
```

---

## Stockage Local — MMKV et WatermelonDB

### MMKV — Clé/Valeur Ultra-Rapide

```typescript
import { MMKV } from 'react-native-mmkv';

export const stockage = new MMKV({
  id: 'app',
  encryptionKey: process.env.MMKV_KEY,
});

export function sauvegarder<T>(clé: string, valeur: T) {
  stockage.set(clé, JSON.stringify(valeur));
}

export function charger<T>(clé: string, défaut: T): T {
  const v = stockage.getString(clé);
  if (!v) return défaut;
  try { return JSON.parse(v); } catch { return défaut; }
}
```

### WatermelonDB — Base Relationnelle Observable

```typescript
import { appSchema, tableSchema } from '@nozbe/watermelondb';
import { Model } from '@nozbe/watermelondb';
import { field, date } from '@nozbe/watermelondb/decorators';

export const schéma = appSchema({
  version: 1,
  tables: [
    tableSchema({
      name: 'produits',
      columns: [
        { name: 'nom', type: 'string' },
        { name: 'prix', type: 'number' },
        { name: 'catégorie_id', type: 'string', isIndexed: true },
        { name: 'synchronisé_à', type: 'number', isOptional: true },
      ],
    }),
  ],
});

export class Produit extends Model {
  static table = 'produits';
  @field('nom') nom!: string;
  @field('prix') prix!: number;
  @field('catégorie_id') catégorieId!: string;
  @date('synchronisé_à') synchroniséÀ!: Date;
}
```

---

## NFC

```typescript
import NfcManager, { NfcTech, Ndef } from 'react-native-nfc-manager';

export class ServiceNFC {
  static async initialiser() {
    const ok = await NfcManager.isSupported();
    if (ok) await NfcManager.start();
    return ok;
  }

  static async lire(): Promise<string | null> {
    try {
      await NfcManager.requestTechnology(NfcTech.Ndef);
      const tag = await NfcManager.getTag();
      if (tag?.ndefMessage?.[0]) {
        return Ndef.text.decodePayload(tag.ndefMessage[0].payload as never);
      }
      return null;
    } finally {
      await NfcManager.cancelTechnologyRequest();
    }
  }

  static async écrire(texte: string) {
    const octets = Ndef.encodeMessage([Ndef.textRecord(texte)]);
    if (!octets) throw new Error('Encodage échoué');
    try {
      await NfcManager.requestTechnology(NfcTech.Ndef);
      await NfcManager.writeNdefMessage(octets);
    } finally {
      await NfcManager.cancelTechnologyRequest();
    }
  }
}
```

---

## Récapitulatif des Packages Natifs

| Fonctionnalité | React Native (Expo) | Flutter |
|---|---|---|
| Notifications push | expo-notifications | firebase_messaging |
| Deep linking | expo-linking | go_router + app_links |
| Biométrie | expo-local-authentication | local_auth |
| Caméra | expo-camera + expo-image-picker | camera_awesome |
| Géolocalisation | expo-location | geolocator |
| Bluetooth BLE | react-native-ble-plx | flutter_blue_plus |
| NFC | react-native-nfc-manager | nfc_manager |
| Capteurs | expo-sensors | sensors_plus |
| Stockage local | MMKV + WatermelonDB | Hive + Isar |
| Permissions | expo-permissions | permission_handler |

**Règle d'or** : toujours demander les permissions au moment de l'utilisation (just-in-time), jamais au démarrage. Le taux d'acceptation est 2-3x supérieur quand l'utilisateur comprend pourquoi la permission est nécessaire.
