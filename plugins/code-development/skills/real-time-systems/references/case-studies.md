# Études de Cas — Systèmes Temps Réel en Production

## Cas 1 — Chat d'Équipe (Startup SaaS, 5 000 Utilisateurs)

### Contexte

Une startup développe un outil de communication pour une niche verticale (coordination d'équipes terrain dans la logistique). L'application est construite avec Next.js côté client et Fastify côté serveur, déployée sur Kubernetes avec 2 instances. L'outil gère ~5 000 utilisateurs actifs et des salles de discussion persistantes.

### Problème Initial

Le premier prototype utilisait des WebSockets natifs sans couche de persistence ni synchronisation multi-instances :

- Les messages n'étaient pas stockés en base de données — à la reconnexion, le client ne voyait aucun historique
- Les 2 instances Fastify n'étaient pas synchronisées : un message envoyé à l'instance A n'atteignait jamais les clients connectés à l'instance B
- Les reconnexions fréquentes (réseau mobile instable sur le terrain) causaient des pertes silencieuses de messages
- Pas de numérotation de séquence — impossible de détecter les messages manqués

### Solution

```
┌─────────────────────────────────────────────────────────────┐
│                        Nginx (SSL)                          │
│              proxy_http_version 1.1 + Upgrade               │
└─────────────┬─────────────────────────────┬─────────────────┘
              │                             │
     ┌────────▼────────┐         ┌──────────▼────────┐
     │  Fastify + SIO  │         │  Fastify + SIO    │
     │   Instance 1    │         │   Instance 2      │
     └────────┬────────┘         └──────────┬────────┘
              │                             │
              └──────────────┬──────────────┘
                             │
                      ┌──────▼──────┐
                      │    Redis    │
                      │  Streams    │
                      │  Adapter   │
                      └──────┬──────┘
                             │
                    ┌────────▼────────┐
                    │   PostgreSQL    │
                    │  (messages,     │
                    │   rooms, users) │
                    └─────────────────┘
```

**Stack choisie :** Socket.io avec `@socket.io/redis-streams-adapter` (persistence vs pub/sub), PostgreSQL pour l'historique des messages, Redis Streams comme bus inter-instances.

```typescript
// server/chat.ts — Serveur Socket.io avec Redis Streams Adapter et persistence

import { createServer } from 'http';
import { Server, Socket } from 'socket.io';
import { createAdapter } from '@socket.io/redis-streams-adapter';
import { createClient } from 'redis';
import { db } from './db';  // Client PostgreSQL

const httpServer = createServer();
const io = new Server(httpServer, {
  cors: { origin: process.env.CLIENT_URL, credentials: true },
  transports: ['websocket'],  // Forcer WebSocket, pas de polling fallback
});

const redisClient = createClient({ url: process.env.REDIS_URL });
await redisClient.connect();

// Redis Streams Adapter — persistence des messages cross-instances
io.adapter(createAdapter(redisClient, {
  streamName: 'chat:messages',
  maxLen: 50_000,
}));

interface MessagePayload {
  roomId: string;
  content: string;
  tempId: string;  // ID temporaire côté client pour l'optimistic update
}

io.on('connection', async (socket: Socket) => {
  const userId = socket.handshake.auth.userId as string;

  socket.on('JOIN_ROOM', async ({ roomId }: { roomId: string }) => {
    // Vérifier l'autorisation d'accès à la salle
    const hasAccess = await db.query(
      'SELECT 1 FROM room_members WHERE room_id = $1 AND user_id = $2',
      [roomId, userId],
    );
    if (hasAccess.rows.length === 0) {
      socket.emit('ERROR', { code: 'FORBIDDEN', message: 'Accès refusé à cette salle' });
      return;
    }

    await socket.join(roomId);

    // Envoyer les 50 derniers messages pour l'affichage initial
    const history = await db.query<{
      id: string; content: string; user_id: string; display_name: string; created_at: Date;
    }>(
      `SELECT m.id, m.content, m.user_id, u.display_name, m.created_at
       FROM messages m JOIN users u ON m.user_id = u.id
       WHERE m.room_id = $1 ORDER BY m.created_at DESC LIMIT 50`,
      [roomId],
    );

    socket.emit('ROOM_HISTORY', {
      roomId,
      messages: history.rows.reverse(),
    });
  });

  socket.on('SEND_MESSAGE', async ({ roomId, content, tempId }: MessagePayload) => {
    // Persister immédiatement en base de données
    const { rows } = await db.query<{ id: string; created_at: Date }>(
      'INSERT INTO messages (room_id, user_id, content) VALUES ($1, $2, $3) RETURNING id, created_at',
      [roomId, userId, content],
    );
    const { id: messageId, created_at } = rows[0];

    const message = {
      id: messageId,
      tempId,         // Permet au client de remplacer l'optimistic update
      roomId,
      userId,
      content,
      createdAt: created_at.toISOString(),
    };

    // Diffuser à tous les membres de la salle — traverse Redis → toutes les instances
    io.to(roomId).emit('NEW_MESSAGE', message);
  });
});

// Reconnexion avec replay des messages manqués
// Le client envoie son dernier messageId connu — le serveur renvoie ce qui manque
socket.on('RECONNECT_SYNC', async ({ roomId, lastMessageId }: {
  roomId: string;
  lastMessageId: string;
}) => {
  const missed = await db.query<{ id: string; content: string; user_id: string; created_at: Date }>(
    `SELECT m.id, m.content, m.user_id, m.created_at
     FROM messages m
     WHERE m.room_id = $1 AND m.id > $2
     ORDER BY m.created_at ASC
     LIMIT 200`,
    [roomId, lastMessageId],
  );

  if (missed.rows.length > 0) {
    socket.emit('MISSED_MESSAGES', { roomId, messages: missed.rows });
  }
});
```

```typescript
// client/useChat.ts — Hook React avec reconnexion et replay

import { useEffect, useRef, useState, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';

interface Message {
  id: string;
  content: string;
  userId: string;
  createdAt: string;
}

export function useChat(roomId: string, userId: string) {
  const socketRef = useRef<Socket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const lastMessageIdRef = useRef<string | null>(null);

  useEffect(() => {
    const socket = io(process.env.NEXT_PUBLIC_WS_URL!, {
      auth: { userId },
      transports: ['websocket'],
      reconnectionDelay: 1000,
      reconnectionDelayMax: 30_000,
      reconnectionAttempts: Infinity,
    });

    socketRef.current = socket;

    socket.on('connect', () => {
      socket.emit('JOIN_ROOM', { roomId });

      // Après une reconnexion, demander les messages manqués
      if (lastMessageIdRef.current) {
        socket.emit('RECONNECT_SYNC', {
          roomId,
          lastMessageId: lastMessageIdRef.current,
        });
      }
    });

    socket.on('ROOM_HISTORY', ({ messages: hist }: { messages: Message[] }) => {
      setMessages(hist);
      if (hist.length > 0) {
        lastMessageIdRef.current = hist[hist.length - 1].id;
      }
    });

    socket.on('MISSED_MESSAGES', ({ messages: missed }: { messages: Message[] }) => {
      setMessages(prev => {
        const existingIds = new Set(prev.map(m => m.id));
        const newOnes = missed.filter(m => !existingIds.has(m.id));
        return [...prev, ...newOnes];
      });
    });

    socket.on('NEW_MESSAGE', (message: Message) => {
      setMessages(prev => [...prev, message]);
      lastMessageIdRef.current = message.id;
    });

    return () => { socket.disconnect(); };
  }, [roomId, userId]);

  const sendMessage = useCallback((content: string) => {
    const tempId = crypto.randomUUID();
    // Optimistic update immédiat
    setMessages(prev => [...prev, {
      id: tempId,
      content,
      userId,
      createdAt: new Date().toISOString(),
    }]);
    socketRef.current?.emit('SEND_MESSAGE', { roomId, content, tempId });
  }, [roomId, userId]);

  return { messages, sendMessage };
}
```

### Résultats

| Métrique | Avant | Après |
|----------|-------|-------|
| Messages perdus à la reconnexion | Fréquent (100%) | 0 en 6 mois |
| Synchronisation multi-instance | Non fonctionnelle | Validée à 10 instances |
| Latence P99 (message → affichage) | 180ms | < 50ms |
| Temps de reconnexion avec historique | N/A | < 300ms |

**Leçon principale** : toujours persister les messages immédiatement à la réception et implémenter le replay basé sur un curseur (dernier ID reçu). Le réseau mobile est intrinsèquement instable — concevoir pour la déconnexion, pas pour la connexion permanente.

---

## Cas 2 — Dashboard Métriques Live (IoT, 50 000 Appareils)

### Contexte

Fabricant d'équipements industriels proposant un dashboard de monitoring en temps réel. Chaque appareil (capteurs de température, vibrations, pression) envoie ses métriques toutes les secondes. 50 000 appareils × 1 mesure/seconde = 50 000 événements par seconde en ingestion.

### Problème Initial

La première architecture créait une connexion WebSocket par appareil vers le dashboard du client. C'était insoutenable :

- 50 000 connexions WebSocket simultanées par instance de dashboard
- Le navigateur ne peut pas afficher 50 000 mises à jour par seconde de manière utile
- Coût infrastructure extrême (chaque connexion WebSocket utilise ~50 KB de mémoire côté serveur)
- Grafana était insuffisamment flexible pour le UX custom requis (alertes contextuelles, drill-down)

### Solution

**Idée clé** : agréger les données côté serveur avant de les pousser au client. Le client n'a besoin que des valeurs moyennes/max/min sur des fenêtres de 5 secondes, pas de chaque événement brut.

```
50K appareils → MQTT Broker → Aggregation Worker → Redis Pub/Sub → SSE Server → Dashboard
                              (fenêtres de 5s)      (200 events/s)    (SSE)
```

**SSE** (et non WebSocket) : le flux est unidirectionnel (serveur → client), SSE est plus simple, compatible avec tous les proxies, et se reconnecte automatiquement.

```typescript
// workers/metrics-aggregator.ts — Fenêtrage et agrégation

import { Redis } from 'ioredis';
import mqtt from 'mqtt';

interface RawMetric {
  deviceId: string;
  sensorType: 'temperature' | 'vibration' | 'pressure';
  value: number;
  timestamp: number;
}

interface AggregatedMetric {
  deviceId: string;
  sensorType: string;
  avg: number;
  min: number;
  max: number;
  count: number;
  windowStart: number;
  windowEnd: number;
}

const redis = new Redis(process.env.REDIS_URL!);
const mqttClient = mqtt.connect(process.env.MQTT_BROKER_URL!);

// Fenêtres d'agrégation en mémoire (5 secondes par device)
const windows = new Map<string, { values: number[]; sensorType: string }>();

mqttClient.subscribe('devices/+/metrics');

mqttClient.on('message', (_topic: string, payload: Buffer) => {
  const metric: RawMetric = JSON.parse(payload.toString());
  const key = `${metric.deviceId}:${metric.sensorType}`;

  if (!windows.has(key)) {
    windows.set(key, { values: [], sensorType: metric.sensorType });
  }
  windows.get(key)!.values.push(metric.value);
});

// Publier les agrégats toutes les 5 secondes
setInterval(async () => {
  const aggregated: AggregatedMetric[] = [];
  const now = Date.now();

  for (const [key, window] of windows) {
    if (window.values.length === 0) continue;

    const [deviceId, sensorType] = key.split(':');
    const values = window.values;
    const avg = values.reduce((s, v) => s + v, 0) / values.length;
    const min = Math.min(...values);
    const max = Math.max(...values);

    aggregated.push({
      deviceId,
      sensorType,
      avg: Math.round(avg * 100) / 100,
      min,
      max,
      count: values.length,
      windowStart: now - 5000,
      windowEnd: now,
    });

    // Vider la fenêtre
    window.values = [];
  }

  if (aggregated.length > 0) {
    // Publier l'agrégat — ~200 events/s au lieu de 50 000
    await redis.publish('metrics:aggregated', JSON.stringify(aggregated));

    // Stocker les dernières valeurs pour les nouveaux clients qui se connectent
    for (const metric of aggregated) {
      await redis.setex(
        `device:${metric.deviceId}:latest:${metric.sensorType}`,
        60,  // TTL 60s
        JSON.stringify(metric),
      );
    }
  }
}, 5_000);
```

```typescript
// server/sse-metrics.ts — Endpoint SSE qui diffuse les agrégats

import express from 'express';
import { Redis } from 'ioredis';

const app = express();

interface SSEClient {
  res: express.Response;
  deviceIds: Set<string>;  // Filtrer par appareils surveillés
}

const clients = new Map<string, SSEClient>();

app.get('/api/metrics/stream', async (req, res) => {
  // Authentification
  const token = req.headers.authorization?.replace('Bearer ', '');
  const session = await verifyToken(token!);
  if (!session) { res.status(401).end(); return; }

  const deviceIds = new Set((req.query.devices as string ?? '').split(',').filter(Boolean));

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');

  const clientId = session.userId;
  clients.set(clientId, { res, deviceIds });

  // Envoyer les dernières valeurs connues immédiatement (éviter l'affichage vide)
  const redis = new Redis(process.env.REDIS_URL!);
  const latestKeys = [...deviceIds].flatMap(id =>
    ['temperature', 'vibration', 'pressure'].map(s => `device:${id}:latest:${s}`)
  );

  if (latestKeys.length > 0) {
    const latestValues = await redis.mget(...latestKeys);
    const snapshot = latestValues
      .filter((v): v is string => v !== null)
      .map(v => JSON.parse(v));

    if (snapshot.length > 0) {
      res.write(`event: SNAPSHOT\n`);
      res.write(`data: ${JSON.stringify(snapshot)}\n\n`);
    }
  }

  const heartbeat = setInterval(() => res.write(': heartbeat\n\n'), 20_000);

  req.on('close', () => {
    clearInterval(heartbeat);
    clients.delete(clientId);
    redis.disconnect();
  });
});

// Abonner le serveur SSE aux agrégats Redis
const subscriber = new Redis(process.env.REDIS_URL!);
await subscriber.subscribe('metrics:aggregated');

subscriber.on('message', (_channel: string, messageJson: string) => {
  const allMetrics: Array<{ deviceId: string }> = JSON.parse(messageJson);

  for (const [_clientId, client] of clients) {
    // Filtrer les métriques selon les appareils surveillés par ce client
    const relevant = client.deviceIds.size === 0
      ? allMetrics
      : allMetrics.filter(m => client.deviceIds.has(m.deviceId));

    if (relevant.length > 0) {
      client.res.write(`event: METRICS_UPDATE\n`);
      client.res.write(`data: ${JSON.stringify(relevant)}\n\n`);
    }
  }
});

async function verifyToken(_token: string): Promise<{ userId: string } | null> {
  // Vérification JWT
  return { userId: 'user-1' };
}
```

### Résultats

| Métrique | Avant | Après |
|----------|-------|-------|
| Événements/seconde côté client | 50 000 | ~200 (agrégés) |
| Connexions WebSocket simultanées | 50 000 (par instance) | ~500 SSE (par instance) |
| Latence dashboard | Impossible à afficher | < 2s (fenêtre 5s + transit) |
| Mémoire serveur par connexion | ~50 KB (WS) | ~8 KB (SSE) |
| Coût infrastructure (mensuel) | -68% grâce à la réduction de connexions |

**Leçon principale** : agréger côté serveur avant d'envoyer au client. L'œil humain ne perçoit pas plus de ~30 FPS — afficher 50 000 mises à jour par seconde n'a aucun sens et sature le navigateur. Une fenêtre de 5 secondes avec min/max/avg est plus informative et 250× moins chère.

---

## Cas 3 — Éditeur Collaboratif de Documents (PME, 200 Utilisateurs)

### Contexte

Cabinet d'avocats utilisant un éditeur de contrats juridiques. Deux ou trois avocats travaillent fréquemment sur le même document simultanément. Avant la refonte, l'outil utilisait un système de "dernière écriture gagne" avec un verrou explicite (un seul utilisateur pouvait éditer à la fois).

### Problème Initial

- Le système de verrou bloquait la collaboration : si Alice oubliait de libérer le verrou, personne ne pouvait éditer
- L'absence de verrou (mode "dernière écriture gagne") causait des conflits quotidiens : deux avocats modifiant le même paragraphe voyaient les modifications de l'autre écrasées
- Pas de présence — impossible de savoir si quelqu'un d'autre était en train d'éditer
- L'autosave brut (POST toutes les 30s) avec `last-write-wins` détruisait le travail concurrent

### Solution

**TipTap + Yjs + Hocuspocus** — la combinaison la plus rapide à implémenter pour l'édition collaborative professionnelle.

```typescript
// server/collaboration.ts — Serveur Hocuspocus avec persistence PostgreSQL

import { Server } from '@hocuspocus/server';
import { Database } from '@hocuspocus/extension-database';
import { Logger } from '@hocuspocus/extension-logger';
import { fromUint8Array, toUint8Array } from 'js-base64';
import { pgPool } from './db';

const server = Server.configure({
  port: 1234,
  timeout: 30_000,

  extensions: [
    new Logger(),

    new Database({
      // Charger le snapshot Yjs depuis PostgreSQL à l'ouverture du document
      fetch: async ({ documentName }) => {
        const result = await pgPool.query<{ ydoc_state: string }>(
          'SELECT ydoc_state FROM documents WHERE id = $1',
          [documentName],
        );
        if (result.rows.length === 0) return null;
        return toUint8Array(result.rows[0].ydoc_state);
      },

      // Sauvegarder le snapshot toutes les 30 secondes (configuré par Hocuspocus)
      store: async ({ documentName, state }) => {
        await pgPool.query(
          `INSERT INTO documents (id, ydoc_state, updated_at)
           VALUES ($1, $2, NOW())
           ON CONFLICT (id) DO UPDATE SET ydoc_state = $2, updated_at = NOW()`,
          [documentName, fromUint8Array(state)],
        );
      },
    }),
  ],

  async onAuthenticate({ token, documentName }) {
    // Vérifier que l'utilisateur a accès au document
    const user = await verifyJWT(token);
    const hasAccess = await checkDocumentAccess(user.id, documentName);
    if (!hasAccess) throw new Error('Accès refusé');

    return {
      user: {
        id: user.id,
        name: user.displayName,
        color: generateUserColor(user.id),
      },
    };
  },

  async onConnect({ socketId, documentName, context }) {
    console.log(`${context.user.name} a ouvert le document ${documentName}`);
  },

  async onDisconnect({ socketId, documentName, context }) {
    console.log(`${context.user.name} a fermé le document ${documentName}`);
  },
});

await server.listen();

async function verifyJWT(_token: string): Promise<{ id: string; displayName: string }> {
  return { id: 'user-1', displayName: 'Alice' };
}
async function checkDocumentAccess(_userId: string, _docId: string): Promise<boolean> {
  return true;
}
function generateUserColor(userId: string): string {
  const colors = ['#4F46E5', '#7C3AED', '#DB2777', '#DC2626', '#D97706', '#059669'];
  const hash = userId.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0);
  return colors[hash % colors.length];
}
```

```typescript
// client/ContractEditor.tsx — TipTap avec collaboration et curseurs

import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Collaboration from '@tiptap/extension-collaboration';
import CollaborationCursor from '@tiptap/extension-collaboration-cursor';
import Placeholder from '@tiptap/extension-placeholder';
import * as Y from 'yjs';
import { HocuspocusProvider } from '@hocuspocus/provider';
import { useEffect, useState } from 'react';

interface Props {
  documentId: string;
  authToken: string;
  currentUser: { name: string; color: string };
}

export function ContractEditor({ documentId, authToken, currentUser }: Props) {
  const [connectedUsers, setConnectedUsers] = useState<Array<{ name: string; color: string }>>([]);
  const [isSyncing, setIsSyncing] = useState(true);

  const ydoc = new Y.Doc();
  const provider = new HocuspocusProvider({
    url: process.env.NEXT_PUBLIC_COLLAB_URL!,
    name: documentId,
    document: ydoc,
    token: authToken,

    onSynced: () => setIsSyncing(false),

    onAwarenessChange: ({ states }) => {
      const users = states
        .filter(s => s.user)
        .map(s => ({ name: s.user.name, color: s.user.color }));
      setConnectedUsers(users);
    },
  });

  const editor = useEditor({
    extensions: [
      StarterKit.configure({ history: false }),
      Placeholder.configure({ placeholder: 'Commencez à rédiger votre contrat…' }),
      Collaboration.configure({ document: ydoc }),
      CollaborationCursor.configure({
        provider,
        user: currentUser,
        render(user: { name: string; color: string }) {
          // Rendu du curseur distant avec le nom de l'utilisateur
          const cursor = document.createElement('span');
          cursor.classList.add('collaboration-cursor__caret');
          cursor.style.borderColor = user.color;

          const label = document.createElement('div');
          label.classList.add('collaboration-cursor__label');
          label.style.backgroundColor = user.color;
          label.textContent = user.name;

          cursor.insertBefore(label, null);
          return cursor;
        },
      }),
    ],
  });

  return (
    <div className="editor-container">
      <div className="presence-bar">
        {connectedUsers.map(u => (
          <span key={u.name} style={{ backgroundColor: u.color }} className="user-avatar">
            {u.name[0].toUpperCase()}
          </span>
        ))}
        {isSyncing && <span className="sync-indicator">Synchronisation…</span>}
      </div>
      <EditorContent editor={editor} />
    </div>
  );
}
```

### Résultats

| Métrique | Avant | Après |
|----------|-------|-------|
| Conflits de contenu par semaine | 8-12 (frustration élevée) | 0 en 8 mois |
| Utilisateurs simultanés max sur un doc | 1 (verrou) | 12 testés |
| Latence des curseurs distants | N/A | < 100ms |
| Temps d'implémentation | Estimation 3 mois (OT custom) | 3 semaines (TipTap + Hocuspocus) |
| Perte de données en cas de crash serveur | Fréquente | Jamais (snapshot 30s) |

**Leçon principale** : Yjs + Hocuspocus est la solution la plus rapide et la plus fiable pour l'édition collaborative. Ne jamais implémenter un CRDT from scratch — la complexité théorique des cas limites est considérable. Le stack TipTap + Yjs + Hocuspocus est battle-tested et couvre les curseurs, l'historique local et la persistence automatiquement.

---

## Cas 4 — Notifications Multi-Canal (E-commerce, 2 Millions d'Utilisateurs)

### Contexte

Marketplace e-commerce avec 2 millions d'utilisateurs actifs mensuels. Notifications critiques : confirmation de commande, livraison, remboursement, promotions personnalisées. Trois canaux de livraison : WebSocket (temps réel, onglet ouvert), email (fallback si déconnecté), SMS (urgences uniquement).

### Problème Initial

- Un utilisateur avec 3 onglets ouverts recevait la même notification 3 fois
- Si l'utilisateur avait l'onglet fermé au moment de l'envoi, la notification était perdue (aucun fallback)
- Pas de centre de notifications persistant — les notifications disparaissaient après rafraîchissement
- Le même event Kafka était parfois consommé plusieurs fois par des workers en crash-loop (doublon email)

### Solution

```
Kafka Consumer                    Redis Bloom Filter
(order.events)        event       (déduplication         PostgreSQL
     │           ──────────►     par event_id)     ──► (notifications table)
     │                                │                       │
     │                          Si nouveau                    │
     │                                │                       │
     │                    ┌───────────▼──────────┐            │
     │                    │   WebSocket Hub       │◄───────────┘
     │                    │  (si user connecté)  │
     │                    └───────────┬──────────┘
     │                                │
     │                    Si non délivré après 30s
     │                                │
     │                    ┌───────────▼──────────┐
     └───────────────────►│   Email Queue         │
                          │   (SQS / BullMQ)     │
                          └───────────┬──────────┘
                                      │
                          Si non délivré après 2h
                                      │
                          ┌───────────▼──────────┐
                          │    SMS Queue          │
                          │  (urgences uniquement)│
                          └──────────────────────┘
```

```typescript
// workers/notification-processor.ts — Consumer Kafka avec déduplication

import { Kafka, EachMessagePayload } from 'kafkajs';
import { createClient } from 'redis';
import { db } from './db';
import { websocketHub } from './ws-hub';
import { emailQueue } from './queues';

const kafka = new Kafka({ clientId: 'notification-worker', brokers: [process.env.KAFKA_BROKER!] });
const consumer = kafka.consumer({ groupId: 'notification-processor' });
const redis = createClient({ url: process.env.REDIS_URL });
await Promise.all([consumer.connect(), redis.connect()]);

// Bloom filter Redis pour la déduplication (léger, ~1MB pour 100K événements)
// Alternative simple : SET avec NX + TTL
async function isAlreadyProcessed(eventId: string): Promise<boolean> {
  const key = `notif:processed:${eventId}`;
  // SET NX (not exists) — retourne 1 si la clé a été créée, 0 si elle existait déjà
  const result = await redis.set(key, '1', { NX: true, EX: 86_400 });  // TTL 24h
  return result === null;  // null = clé existait déjà = déjà traité
}

interface OrderEvent {
  eventId: string;
  type: 'ORDER_CONFIRMED' | 'ORDER_SHIPPED' | 'ORDER_DELIVERED';
  userId: string;
  orderId: string;
  orderTotal: number;
  estimatedDelivery?: string;
}

await consumer.subscribe({ topics: ['order.events'] });

await consumer.run({
  eachMessage: async ({ message }: EachMessagePayload) => {
    const event: OrderEvent = JSON.parse(message.value!.toString());

    // 1. Déduplication — évite de traiter deux fois le même événement
    if (await isAlreadyProcessed(event.eventId)) {
      console.log(`Événement ${event.eventId} déjà traité — ignoré`);
      return;
    }

    // 2. Persister la notification en base de données
    const notification = await db.query<{ id: string }>(
      `INSERT INTO notifications (user_id, type, payload, status, created_at)
       VALUES ($1, $2, $3, 'pending', NOW()) RETURNING id`,
      [event.userId, event.type, JSON.stringify(event)],
    );
    const notificationId = notification.rows[0].id;

    // 3. Tenter la livraison WebSocket temps réel
    const delivered = await websocketHub.sendToUser(event.userId, {
      type: 'NOTIFICATION',
      notificationId,
      payload: buildNotificationPayload(event),
    });

    if (delivered) {
      // Marquer comme livré en temps réel
      await db.query(
        'UPDATE notifications SET status = $1, delivered_at = NOW() WHERE id = $2',
        ['delivered_realtime', notificationId],
      );
    } else {
      // Utilisateur non connecté — planifier le fallback email
      await emailQueue.add('send-notification-email', {
        notificationId,
        userId: event.userId,
        event,
      }, {
        delay: 30_000,       // Attendre 30s — peut-être que l'utilisateur va se connecter
        attempts: 3,
        backoff: { type: 'exponential', delay: 60_000 },
      });
    }
  },
});

function buildNotificationPayload(event: OrderEvent): object {
  const messages: Record<string, string> = {
    ORDER_CONFIRMED: `Votre commande #${event.orderId} est confirmée (${event.orderTotal}€)`,
    ORDER_SHIPPED: `Votre commande #${event.orderId} est en route !`,
    ORDER_DELIVERED: `Votre commande #${event.orderId} a été livrée.`,
  };
  return { title: 'Mise à jour commande', body: messages[event.type] ?? '', orderId: event.orderId };
}
```

```typescript
// client/NotificationCenter.tsx — Centre de notifications React avec persistence

import { useEffect, useState, useCallback } from 'react';
import { io } from 'socket.io-client';

interface Notification {
  id: string;
  type: string;
  payload: { title: string; body: string; orderId?: string };
  createdAt: string;
  readAt: string | null;
}

export function NotificationCenter({ userId }: { userId: string }) {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    // Charger les notifications persistantes à l'ouverture (quel que soit l'état de connexion)
    fetch('/api/notifications?limit=20')
      .then(r => r.json())
      .then((data: { notifications: Notification[] }) => {
        setNotifications(data.notifications);
        setUnreadCount(data.notifications.filter(n => !n.readAt).length);
      });

    // S'abonner aux nouvelles notifications en temps réel
    const socket = io(process.env.NEXT_PUBLIC_WS_URL!, {
      auth: { userId },
    });

    socket.on('NOTIFICATION', (notification: Notification) => {
      setNotifications(prev => [notification, ...prev]);
      setUnreadCount(prev => prev + 1);

      // Envoyer le receipt de livraison
      socket.emit('NOTIFICATION_RECEIVED', { notificationId: notification.id });
    });

    return () => { socket.disconnect(); };
  }, [userId]);

  const markAsRead = useCallback(async (notificationId: string) => {
    await fetch(`/api/notifications/${notificationId}/read`, { method: 'POST' });
    setNotifications(prev => prev.map(n =>
      n.id === notificationId ? { ...n, readAt: new Date().toISOString() } : n,
    ));
    setUnreadCount(prev => Math.max(0, prev - 1));
  }, []);

  return (
    <div className="notification-center">
      <div className="notification-header">
        <h3>Notifications</h3>
        {unreadCount > 0 && <span className="badge">{unreadCount}</span>}
      </div>
      <ul>
        {notifications.map(n => (
          <li key={n.id} className={n.readAt ? 'read' : 'unread'} onClick={() => markAsRead(n.id)}>
            <strong>{n.payload.title}</strong>
            <p>{n.payload.body}</p>
            <time>{new Date(n.createdAt).toLocaleString('fr-FR')}</time>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Résultats

| Métrique | Avant | Après |
|----------|-------|-------|
| Doublons de notifications | Fréquents (3 onglets = 3 notifs) | 0 (déduplication Redis) |
| Delivery rate (temps réel uniquement) | ~65% (utilisateurs connectés) | 99.2% (temps réel + email fallback) |
| Notifications perdues (onglet fermé) | Fréquentes | 0 (persistence + fallback) |
| Cohérence entre sessions | Non (disparaissait au refresh) | Complète (PostgreSQL) |
| Traitement doublons Kafka (re-delivery) | Causait des emails en double | 0 (NX + TTL Redis) |

**Leçon principale** : les notifications temps réel nécessitent toujours une stratégie de fallback. Ne jamais compter uniquement sur la connexion WebSocket active. La combinaison persistence (PostgreSQL) + déduplication (Redis NX) + fallback (email après 30s) + delivery receipt est le pattern robuste pour les notifications à grande échelle.

---

## Synthèse des Patterns Communs

| Pattern | Cas 1 (Chat) | Cas 2 (IoT) | Cas 3 (Éditeur) | Cas 4 (Notifs) |
|---------|-------------|-------------|-----------------|----------------|
| Protocole | WebSocket (SIO) | SSE | WebSocket (Yjs) | WebSocket |
| Persistence | PostgreSQL | Redis (latest) | PostgreSQL (Yjs) | PostgreSQL |
| Replay reconnexion | Cursor (lastId) | Snapshot initial | Yjs sync | Inbox chargé au démarrage |
| Multi-instance | Redis Streams adapter | Redis Pub/Sub | Hocuspocus clustering | Kafka + Redis |
| Déduplication | N/A | N/A | CRDT (natif) | Redis NX + TTL |
| Fallback dégradé | Historique limité | Cache Redis latest | Mode lecture seule | Email + SMS |
