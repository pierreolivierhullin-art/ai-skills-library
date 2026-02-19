---
name: real-time-systems
version: 1.0.0
description: >
  WebSockets real-time applications, Server-Sent Events SSE, Socket.io rooms namespaces,
  real-time state synchronization, pub/sub patterns, presence channels online users,
  collaborative editing CRDT conflict-free replicated data types, operational transform,
  Redis pub/sub, NATS messaging, Supabase Realtime, Ably Pusher, long polling,
  connection management backpressure, real-time notifications, live dashboards
---

# Real-Time Systems — WebSockets, SSE et Communication Temps Réel

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu construis des notifications en temps réel (chat, alertes, tableaux de bord live)
- Tu implémente un système de collaboration (édition simultanée, présence, curseurs)
- Tu diffuses des mises à jour de données sans polling (prix boursiers, métriques, scores)
- Tu as besoin de pousser des événements serveur → client sans requête du client
- Tu choisis entre WebSocket, SSE, et long polling pour ton cas d'usage
- Tu veux scaler une solution temps réel sur plusieurs instances de serveur

---

## Comparaison des Technologies

| Critère | WebSocket | SSE | Long Polling |
|---|---|---|---|
| Direction | Bidirectionnel | Serveur → Client | Serveur → Client |
| Protocole | WS/WSS | HTTP | HTTP |
| Reconnexion auto | Manuelle | Automatique | Manuelle |
| Proxies/firewalls | Parfois bloqué | Compatible | Compatible |
| Charge serveur | Connexion persistante | Connexion persistante | Requête par message |
| Usage idéal | Chat, jeux, collaboration | Notifications, flux | Fallback, legacy |

---

## WebSockets Natifs

### Serveur Node.js avec `ws`

```typescript
import { WebSocketServer, WebSocket } from 'ws';
import { IncomingMessage } from 'http';

interface ClientMeta {
  userId: string;
  roomId: string;
}

// Map pour suivre les clients connectés
const clients = new Map<WebSocket, ClientMeta>();

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (ws: WebSocket, req: IncomingMessage) => {
  const url = new URL(req.url!, 'ws://localhost');
  const userId = url.searchParams.get('userId') ?? 'anonyme';
  const roomId = url.searchParams.get('roomId') ?? 'default';

  clients.set(ws, { userId, roomId });
  console.log(`Client connecté : ${userId} → salle ${roomId}`);

  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data.toString());
      handleMessage(ws, message);
    } catch {
      ws.send(JSON.stringify({ type: 'ERREUR', payload: 'Message invalide' }));
    }
  });

  ws.on('close', () => {
    clients.delete(ws);
    broadcastToRoom(roomId, { type: 'USER_LEFT', payload: { userId } }, ws);
  });

  // Envoyer confirmation de connexion
  ws.send(JSON.stringify({ type: 'CONNECTE', payload: { userId, roomId } }));
  broadcastToRoom(roomId, { type: 'USER_JOINED', payload: { userId } }, ws);
});

// Diffuser un message à tous les clients d'une salle
function broadcastToRoom(
  roomId: string,
  message: object,
  exclude?: WebSocket,
): void {
  const payload = JSON.stringify(message);
  for (const [client, meta] of clients) {
    if (meta.roomId === roomId && client !== exclude && client.readyState === WebSocket.OPEN) {
      client.send(payload);
    }
  }
}

function handleMessage(ws: WebSocket, message: { type: string; payload: unknown }): void {
  const meta = clients.get(ws);
  if (!meta) return;

  switch (message.type) {
    case 'CHAT':
      broadcastToRoom(meta.roomId, {
        type: 'CHAT',
        payload: { userId: meta.userId, texte: message.payload, ts: Date.now() },
      });
      break;
    case 'PING':
      ws.send(JSON.stringify({ type: 'PONG' }));
      break;
  }
}
```

### Client TypeScript avec reconnexion automatique

```typescript
class WebSocketClient {
  private ws: WebSocket | null = null;
  private handlers = new Map<string, (payload: unknown) => void>();
  private reconnectDelay = 1000;
  private maxReconnectDelay = 30_000;

  constructor(private readonly url: string) {
    this.connect();
  }

  private connect(): void {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('Connexion établie');
      this.reconnectDelay = 1000;  // Réinitialiser
    };

    this.ws.onmessage = (event) => {
      try {
        const { type, payload } = JSON.parse(event.data);
        this.handlers.get(type)?.(payload);
      } catch { /* ignorer les messages malformés */ }
    };

    this.ws.onclose = () => {
      console.log(`Déconnecté. Reconnexion dans ${this.reconnectDelay}ms`);
      setTimeout(() => this.connect(), this.reconnectDelay);
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay);
    };
  }

  on<T>(type: string, handler: (payload: T) => void): void {
    this.handlers.set(type, handler as (payload: unknown) => void);
  }

  send(type: string, payload: unknown): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, payload }));
    }
  }

  disconnect(): void {
    this.ws?.close();
  }
}

// Usage
const client = new WebSocketClient('ws://localhost:8080?userId=alice&roomId=equipe-dev');
client.on('CHAT', (payload) => console.log(payload));
client.send('CHAT', 'Bonjour à tous !');
```

---

## Server-Sent Events (SSE)

SSE est idéal pour les flux unidirectionnels : notifications, tableaux de bord live, progression de tâches.

```typescript
// Endpoint SSE avec Express
import express from 'express';
import { EventEmitter } from 'events';

const app = express();
const eventBus = new EventEmitter();

// Map des clients SSE connectés par userId
const sseClients = new Map<string, express.Response>();

app.get('/api/events/:userId', (req, res) => {
  const { userId } = req.params;

  // Headers SSE obligatoires
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');  // Désactiver le buffer Nginx

  // Envoyer un commentaire pour maintenir la connexion
  res.write(': keepalive\n\n');

  sseClients.set(userId, res);

  // Keepalive toutes les 30s
  const heartbeat = setInterval(() => {
    res.write(': keepalive\n\n');
  }, 30_000);

  req.on('close', () => {
    clearInterval(heartbeat);
    sseClients.delete(userId);
  });
});

// Fonction pour pousser un événement à un utilisateur
function pushEvent(userId: string, event: string, data: object): void {
  const client = sseClients.get(userId);
  if (!client) return;

  client.write(`event: ${event}\n`);
  client.write(`data: ${JSON.stringify(data)}\n`);
  client.write(`id: ${Date.now()}\n`);
  client.write('\n');  // Ligne vide = fin de l'événement
}

// Client JavaScript
const eventSource = new EventSource('/api/events/alice');

eventSource.addEventListener('COMMANDE_LIVREE', (event) => {
  const data = JSON.parse(event.data);
  console.log(`Commande ${data.commandeId} livrée !`);
});

eventSource.addEventListener('NOTIFICATION', (event) => {
  const { titre, message } = JSON.parse(event.data);
  // Afficher une toast notification
});

eventSource.onerror = () => {
  // EventSource se reconnecte automatiquement avec le Last-Event-ID
};
```

---

## Socket.io — Salles et Namespaces

```typescript
import { Server, Socket } from 'socket.io';
import { createServer } from 'http';

const httpServer = createServer();
const io = new Server(httpServer, {
  cors: { origin: process.env.CLIENT_URL, credentials: true },
  pingTimeout: 60_000,
  pingInterval: 25_000,
});

// Namespace pour le chat (isolation des événements)
const chat = io.of('/chat');

interface UserSocket extends Socket {
  data: { userId: string; displayName: string };
}

chat.use(async (socket: UserSocket, next) => {
  // Middleware d'authentification
  const token = socket.handshake.auth.token;
  const user = await verifyToken(token);
  if (!user) return next(new Error('Non autorisé'));
  socket.data = { userId: user.id, displayName: user.nom };
  next();
});

chat.on('connection', (socket: UserSocket) => {
  const { userId, displayName } = socket.data;

  socket.on('REJOINDRE_SALLE', async (roomId: string) => {
    await socket.join(roomId);

    // Obtenir les membres de la salle
    const sockets = await chat.in(roomId).fetchSockets();
    const membres = sockets.map(s => (s as UserSocket).data.displayName);

    // Notifier tout le monde dans la salle
    chat.to(roomId).emit('MEMBRE_REJOINT', { userId, displayName, membres });
  });

  socket.on('MESSAGE', (payload: { roomId: string; texte: string }) => {
    const message = {
      id: crypto.randomUUID(),
      userId,
      displayName,
      texte: payload.texte,
      ts: new Date().toISOString(),
    };

    // Diffuser à tous sauf l'émetteur
    socket.to(payload.roomId).emit('MESSAGE', message);
    // Confirmer à l'émetteur
    socket.emit('MESSAGE_CONFIRME', { id: message.id });
  });

  socket.on('disconnecting', () => {
    for (const roomId of socket.rooms) {
      if (roomId !== socket.id) {
        chat.to(roomId).emit('MEMBRE_PARTI', { userId, displayName });
      }
    }
  });
});
```

---

## Pub/Sub avec Redis — Scalabilité Multi-Instance

Avec plusieurs instances de serveur, chaque client est connecté à une seule instance. Redis pub/sub permet de diffuser les messages entre instances.

```typescript
import { createClient } from 'redis';

const publisher = createClient({ url: process.env.REDIS_URL });
const subscriber = publisher.duplicate();

await Promise.all([publisher.connect(), subscriber.connect()]);

// S'abonner aux événements d'une room
await subscriber.subscribe('room:equipe-dev', (messageJson) => {
  const message = JSON.parse(messageJson);
  // Diffuser aux clients WebSocket connectés sur cette instance
  broadcastToRoom('equipe-dev', message);
});

// Publier un événement (reçu par toutes les instances)
async function publishToRoom(roomId: string, event: object): Promise<void> {
  await publisher.publish(`room:${roomId}`, JSON.stringify(event));
}

// Avec Socket.io : utiliser l'adapter Redis officiel
import { createAdapter } from '@socket.io/redis-adapter';
io.adapter(createAdapter(publisher, subscriber));
// → Automatiquement géré : io.to(roomId).emit() traverse les instances
```

---

## Présence — Utilisateurs en Ligne

```typescript
// Suivre la présence avec Redis
const PRESENCE_TTL = 30;  // secondes

async function setPresence(userId: string, status: 'en-ligne' | 'absent'): Promise<void> {
  const key = `presence:${userId}`;
  if (status === 'en-ligne') {
    await publisher.set(key, 'en-ligne', { EX: PRESENCE_TTL });
  } else {
    await publisher.del(key);
  }
  await publisher.publish('presence', JSON.stringify({ userId, status }));
}

async function getOnlineUsers(userIds: string[]): Promise<string[]> {
  const keys = userIds.map(id => `presence:${id}`);
  const values = await publisher.mGet(keys);
  return userIds.filter((_, i) => values[i] === 'en-ligne');
}

// Renouveler le TTL périodiquement (heartbeat)
setInterval(async () => {
  await setPresence(currentUserId, 'en-ligne');
}, 20_000);
```

---

## React Hook — WebSocket

```typescript
import { useEffect, useRef, useCallback, useState } from 'react';

type WSStatus = 'connecting' | 'open' | 'closed';

function useWebSocket<T>(url: string) {
  const wsRef = useRef<WebSocket | null>(null);
  const [status, setStatus] = useState<WSStatus>('connecting');
  const handlersRef = useRef(new Map<string, (payload: unknown) => void>());

  useEffect(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => setStatus('open');
    ws.onclose = () => setStatus('closed');
    ws.onmessage = (event) => {
      try {
        const { type, payload } = JSON.parse(event.data);
        handlersRef.current.get(type)?.(payload);
      } catch { /* ignorer */ }
    };

    return () => ws.close();
  }, [url]);

  const send = useCallback((type: string, payload: unknown) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type, payload }));
    }
  }, []);

  const on = useCallback((type: string, handler: (payload: T) => void) => {
    handlersRef.current.set(type, handler as (payload: unknown) => void);
    return () => handlersRef.current.delete(type);
  }, []);

  return { send, on, status };
}
```

---

## Références

- `references/websockets-sse.md` — Protocole WebSocket, framing, heartbeat, backpressure, SSE avancé
- `references/pub-sub-scaling.md` — Redis pub/sub, NATS, Kafka pour temps réel, Socket.io adapters, multi-région
- `references/realtime-state.md` — CRDT (Yjs, Automerge), présence avancée, curseurs collaboratifs, conflict resolution
- `references/case-studies.md` — 4 cas : chat d'équipe, dashboard métriques live, éditeur collaboratif, notifications multi-canal
