# WebSockets et SSE — Protocoles et Implémentation

## Protocole WebSocket : Anatomie du Handshake

WebSocket démarre comme une requête HTTP standard, puis effectue un upgrade de protocole. Le client envoie un header `Upgrade: websocket` accompagné d'un nonce aléatoire encodé en Base64 (`Sec-WebSocket-Key`). Le serveur répond avec un statut `101 Switching Protocols` et calcule l'acceptation via SHA-1 du nonce concatené au GUID `258EAFA5-E914-47DA-95CA-C5AB0DC85B11`.

```
GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13

HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

Après l'upgrade, la connexion TCP persiste et les deux parties peuvent envoyer des frames à tout moment.

### Structure des Frames WebSocket

Chaque frame possède un header binaire compact :

| Bit(s) | Champ | Description |
|--------|-------|-------------|
| 0 | FIN | 1 = dernière frame du message |
| 1-3 | RSV1-3 | Extensions (ex : compression) |
| 4-7 | Opcode | 0x0 = continuation, 0x1 = texte, 0x2 = binaire, 0x8 = close, 0x9 = ping, 0xA = pong |
| 8 | MASK | 1 = client → serveur (obligatoire), 0 = serveur → client |
| 9-15 | Payload len | Longueur sur 7 bits, 16 ou 64 bits selon la valeur |
| 16-47 | Masking key | 4 octets si MASK=1 |
| … | Payload | Données XOR avec masking key si MASK=1 |

Le masquage côté client est obligatoire selon la RFC 6455 pour éviter les attaques de cache poisoning sur les proxies HTTP intermédiaires.

La fragmentation permet d'envoyer des messages de taille inconnue à l'avance : première frame avec FIN=0, frames de continuation avec opcode 0x0, dernière frame avec FIN=1.

---

## Backpressure : Gérer la Pression sur le Buffer

Sans contrôle de flux, un émetteur rapide peut saturer le buffer d'envoi et provoquer des OOM ou des déconnexions silencieuses.

### `bufferedAmount` côté client

```typescript
// Client : vérifier le buffer avant d'envoyer
class ThrottledWebSocket {
  private ws: WebSocket;
  private readonly MAX_BUFFER = 64 * 1024; // 64 KB

  constructor(url: string) {
    this.ws = new WebSocket(url);
  }

  sendWithBackpressure(data: string): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.ws.readyState !== WebSocket.OPEN) {
        return reject(new Error('Connexion fermée'));
      }

      const attemptSend = () => {
        if (this.ws.bufferedAmount > this.MAX_BUFFER) {
          // Buffer trop plein — attendre avant de réessayer
          setTimeout(attemptSend, 50);
          return;
        }
        this.ws.send(data);
        resolve();
      };

      attemptSend();
    });
  }
}
```

### Événement `drain` côté serveur (bibliothèque `ws`)

```typescript
import { WebSocketServer, WebSocket } from 'ws';

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (ws: WebSocket) => {
  let isPaused = false;

  // Écouter le signal de drain : le buffer est à nouveau vide
  ws.on('drain', () => {
    isPaused = false;
    resumeDataProduction();
  });

  function sendData(data: Buffer): boolean {
    // ws.send() retourne false si le buffer est plein
    const canContinue = ws.send(data) !== false;
    if (!canContinue && !isPaused) {
      isPaused = true;
      pauseDataProduction();
    }
    return canContinue;
  }

  function pauseDataProduction(): void {
    // Arrêter la source de données (ex : pauseR() sur un stream)
    console.log('Backpressure détectée — pause de la production');
  }

  function resumeDataProduction(): void {
    console.log('Buffer drainé — reprise de la production');
  }
});
```

---

## Reconnexion avec Exponential Backoff et Jitter

Sans jitter, des milliers de clients se reconnectent simultanément après une coupure serveur, créant un "thundering herd" qui remet le serveur à genoux immédiatement après sa relance.

```typescript
class ResilientWebSocketClient {
  private ws: WebSocket | null = null;
  private reconnectAttempt = 0;
  private readonly BASE_DELAY = 1_000;        // 1s
  private readonly MAX_DELAY = 60_000;         // 60s
  private readonly MAX_ATTEMPTS = 10;
  private explicitClose = false;

  constructor(
    private readonly url: string,
    private readonly onMessage: (data: unknown) => void,
  ) {
    this.connect();
  }

  private computeDelay(): number {
    // Exponential backoff : 1s, 2s, 4s, 8s… plafonné à 60s
    const exponential = Math.min(
      this.BASE_DELAY * Math.pow(2, this.reconnectAttempt),
      this.MAX_DELAY,
    );
    // Jitter ±30% : éviter la synchronisation de milliers de clients
    const jitter = exponential * (0.7 + Math.random() * 0.6);
    return Math.floor(jitter);
  }

  private connect(): void {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log(`Connecté après ${this.reconnectAttempt} tentative(s)`);
      this.reconnectAttempt = 0;
    };

    this.ws.onmessage = (event: MessageEvent) => {
      try {
        this.onMessage(JSON.parse(event.data as string));
      } catch { /* ignorer les messages malformés */ }
    };

    this.ws.onclose = (event: CloseEvent) => {
      if (this.explicitClose) return;

      if (this.reconnectAttempt >= this.MAX_ATTEMPTS) {
        console.error('Nombre maximum de tentatives atteint');
        return;
      }

      const delay = this.computeDelay();
      console.log(
        `Déconnecté (code ${event.code}). Tentative ${this.reconnectAttempt + 1}/${this.MAX_ATTEMPTS} dans ${delay}ms`,
      );
      this.reconnectAttempt++;
      setTimeout(() => this.connect(), delay);
    };

    this.ws.onerror = (err) => {
      console.error('Erreur WebSocket :', err);
    };
  }

  close(): void {
    this.explicitClose = true;
    this.ws?.close(1000, 'Fermeture normale');
  }
}
```

---

## WebSocket Sécurisé : WSS, Auth et Rate Limiting

### Vérification d'origine et authentification

```typescript
import { WebSocketServer, WebSocket } from 'ws';
import { IncomingMessage } from 'http';
import jwt from 'jsonwebtoken';

const ALLOWED_ORIGINS = new Set([
  'https://app.mondomaine.fr',
  'https://staging.mondomaine.fr',
]);

// Compteur de connexions par IP pour rate limiting
const connectionsByIp = new Map<string, number>();
const MAX_CONNECTIONS_PER_IP = 10;

const wss = new WebSocketServer({
  port: 8080,

  // verifyClient : appelé avant l'upgrade, bloque les connexions invalides
  verifyClient(info: { origin: string; req: IncomingMessage }, callback: (result: boolean, code?: number, message?: string) => void): void {
    // 1. Vérifier l'origine
    if (!ALLOWED_ORIGINS.has(info.origin)) {
      callback(false, 403, 'Origine non autorisée');
      return;
    }

    // 2. Rate limiting par IP
    const ip = info.req.socket.remoteAddress ?? 'unknown';
    const current = connectionsByIp.get(ip) ?? 0;
    if (current >= MAX_CONNECTIONS_PER_IP) {
      callback(false, 429, 'Trop de connexions depuis cette IP');
      return;
    }
    connectionsByIp.set(ip, current + 1);

    callback(true);
  },
});

// Authentification par token JWT au premier message
// (l'URL query param expose le token dans les logs serveur — préférer le premier message)
wss.on('connection', (ws: WebSocket) => {
  let authenticated = false;
  let userId: string | null = null;

  const authTimeout = setTimeout(() => {
    if (!authenticated) {
      ws.close(4001, 'Authentification expirée');
    }
  }, 5_000);

  ws.on('message', (data: Buffer) => {
    const message = JSON.parse(data.toString()) as { type: string; token?: string; payload?: unknown };

    if (!authenticated) {
      if (message.type !== 'AUTH' || !message.token) {
        ws.close(4001, 'Premier message doit être AUTH');
        return;
      }

      try {
        const decoded = jwt.verify(message.token, process.env.JWT_SECRET!) as { sub: string };
        userId = decoded.sub;
        authenticated = true;
        clearTimeout(authTimeout);
        ws.send(JSON.stringify({ type: 'AUTH_OK', payload: { userId } }));
      } catch {
        ws.close(4001, 'Token invalide');
      }
      return;
    }

    // Traiter le message normal avec userId garanti
    handleAuthenticatedMessage(ws, userId!, message);
  });
});

function handleAuthenticatedMessage(
  ws: WebSocket,
  userId: string,
  message: { type: string; payload?: unknown },
): void {
  // Logique métier
}
```

---

## Bibliothèque `ws` — Options Avancées

```typescript
import { WebSocketServer } from 'ws';

const wss = new WebSocketServer({
  port: 8080,

  // Compression per-message (économise 40-70% de bande passante sur JSON)
  perMessageDeflate: {
    zlibDeflateOptions: {
      level: 6,           // Compromis CPU/compression (1=rapide, 9=max)
      memLevel: 8,
    },
    zlibInflateOptions: {
      chunkSize: 10 * 1024,
    },
    clientNoContextTakeover: true,   // Empêcher le client de conserver le contexte
    serverNoContextTakeover: true,   // Réduire la mémoire serveur
    threshold: 1024,                  // Compresser seulement les messages > 1KB
  },

  // Limite la taille des messages pour éviter les attaques DoS
  maxPayload: 5 * 1024 * 1024,  // 5 MB maximum

  // Sélectionner le sous-protocole selon ceux demandés par le client
  handleProtocols(protocols: Set<string>): string | false {
    if (protocols.has('chat.v2')) return 'chat.v2';
    if (protocols.has('chat.v1')) return 'chat.v1';
    return false;  // Rejeter si aucun protocole compatible
  },
});

// Ping/Pong heartbeat pour détecter les connexions zombies
const HEARTBEAT_INTERVAL = 30_000;

const interval = setInterval(() => {
  wss.clients.forEach((ws) => {
    const extWs = ws as WebSocket & { isAlive: boolean };
    if (!extWs.isAlive) {
      extWs.terminate();  // Couper sans attendre de FIN
      return;
    }
    extWs.isAlive = false;
    extWs.ping();
  });
}, HEARTBEAT_INTERVAL);

wss.on('connection', (ws) => {
  const extWs = ws as typeof ws & { isAlive: boolean };
  extWs.isAlive = true;
  extWs.on('pong', () => { extWs.isAlive = true; });
});

wss.on('close', () => clearInterval(interval));
```

---

## SSE Avancé : Replay, Retry et Événements Nommés

### `Last-Event-ID` pour le replay sur reconnexion

```typescript
import express from 'express';
import { Redis } from 'ioredis';

const app = express();
const redis = new Redis(process.env.REDIS_URL!);

// Stocker les N derniers événements dans Redis pour le replay
const EVENT_HISTORY_KEY = 'sse:events';
const MAX_HISTORY = 100;

async function storeEvent(event: { id: string; type: string; data: unknown }): Promise<void> {
  await redis.lpush(EVENT_HISTORY_KEY, JSON.stringify(event));
  await redis.ltrim(EVENT_HISTORY_KEY, 0, MAX_HISTORY - 1);
}

async function getEventsSince(lastEventId: string): Promise<Array<{ id: string; type: string; data: unknown }>> {
  const events = await redis.lrange(EVENT_HISTORY_KEY, 0, MAX_HISTORY - 1);
  const parsed = events.map(e => JSON.parse(e) as { id: string; type: string; data: unknown });

  // Retourner les événements plus récents que lastEventId
  const idx = parsed.findIndex(e => e.id === lastEventId);
  if (idx === -1) return parsed.slice(0, 20);  // Fallback : 20 derniers événements
  return parsed.slice(0, idx);  // Tous les événements après le dernier reçu
}

app.get('/api/stream', async (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');

  // Délai de reconnexion suggéré au client (en ms)
  res.write('retry: 3000\n\n');

  // Rejouer les événements manqués depuis la dernière déconnexion
  const lastEventId = req.headers['last-event-id'] as string | undefined;
  if (lastEventId) {
    const missed = await getEventsSince(lastEventId);
    for (const event of missed.reverse()) {
      sendSSEEvent(res, event.type, event.data, event.id);
    }
  }

  // Heartbeat pour maintenir la connexion à travers les proxies
  const heartbeat = setInterval(() => {
    res.write(': heartbeat\n\n');
  }, 20_000);

  const subscriber = redis.duplicate();
  await subscriber.subscribe('sse:channel');

  subscriber.on('message', (_channel, messageJson) => {
    const event = JSON.parse(messageJson) as { id: string; type: string; data: unknown };
    sendSSEEvent(res, event.type, event.data, event.id);
  });

  req.on('close', () => {
    clearInterval(heartbeat);
    subscriber.disconnect();
  });
});

function sendSSEEvent(res: express.Response, type: string, data: unknown, id?: string): void {
  if (id) res.write(`id: ${id}\n`);
  res.write(`event: ${type}\n`);
  res.write(`data: ${JSON.stringify(data)}\n`);
  res.write('\n');
}
```

### SSE avec Next.js App Router

```typescript
// app/api/stream/route.ts
import { NextRequest } from 'next/server';
import { Redis } from 'ioredis';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function GET(request: NextRequest): Promise<Response> {
  const redis = new Redis(process.env.REDIS_URL!);

  const encoder = new TextEncoder();
  let isConnected = true;

  const stream = new ReadableStream({
    async start(controller) {
      // Heartbeat pour maintenir la connexion Next.js ouverte
      const heartbeat = setInterval(() => {
        if (!isConnected) return;
        controller.enqueue(encoder.encode(': heartbeat\n\n'));
      }, 15_000);

      // S'abonner aux événements Redis
      const subscriber = redis.duplicate();
      await subscriber.subscribe('stream:events');

      subscriber.on('message', (_ch, msg) => {
        if (!isConnected) return;
        const { type, data, id } = JSON.parse(msg);
        const chunk = `id: ${id}\nevent: ${type}\ndata: ${JSON.stringify(data)}\n\n`;
        controller.enqueue(encoder.encode(chunk));
      });

      // Nettoyer à la déconnexion du client
      request.signal.addEventListener('abort', () => {
        isConnected = false;
        clearInterval(heartbeat);
        subscriber.disconnect();
        controller.close();
      });
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no',
    },
  });
}
```

---

## Comparaison WebSocket, SSE et Long Polling

| Critère | WebSocket | SSE | Long Polling |
|---------|-----------|-----|--------------|
| Direction du flux | Bidirectionnel | Serveur → Client | Serveur → Client |
| Protocole | WS/WSS (TCP) | HTTP/1.1 ou HTTP/2 | HTTP |
| Reconnexion automatique | Non (manuelle) | Oui (navigateur natif) | Non (manuelle) |
| Support proxies/firewalls | Parfois bloqué | Toujours compatible | Toujours compatible |
| Overhead par message | ~2 octets (frame header) | ~30 octets (format texte) | ~700 octets (headers HTTP) |
| Nombre de connexions max (navigateur) | Illimité | 6 par domaine (HTTP/1.1) | 6 par domaine (HTTP/1.1) |
| Support HTTP/2 | Non (protocole séparé) | Oui (multiplexé) | Non recommandé |
| Cas d'usage idéal | Chat, jeux, collaboration, streaming binaire | Notifications, dashboards, progression | Fallback, environnements legacy |
| Complexité serveur | Moyenne (état de connexion) | Faible | Faible |
| Support navigateur | Excellent | Excellent (sauf IE) | Excellent |

### Long Polling : Implémentation Hold-and-Release

```typescript
// Long polling avec timeout et libération immédiate sur événement
app.get('/api/poll', async (req, res) => {
  const since = parseInt(req.query.since as string) || 0;
  const TIMEOUT = 30_000;  // 30s maximum d'attente

  // Vérifier si des messages sont déjà disponibles
  const pending = await getMessagesSince(since);
  if (pending.length > 0) {
    res.json({ messages: pending, timestamp: Date.now() });
    return;
  }

  // Aucun message — tenir la connexion ouverte (hold)
  let resolved = false;
  const timeoutId = setTimeout(() => {
    if (!resolved) {
      resolved = true;
      res.json({ messages: [], timestamp: Date.now() });  // Réponse vide = timeout
    }
  }, TIMEOUT);

  // S'abonner aux nouveaux messages (release immédiat)
  const unsubscribe = subscribeToMessages((message) => {
    if (!resolved) {
      resolved = true;
      clearTimeout(timeoutId);
      unsubscribe();
      res.json({ messages: [message], timestamp: Date.now() });
    }
  });

  req.on('close', () => {
    resolved = true;
    clearTimeout(timeoutId);
    unsubscribe();
  });
});

async function getMessagesSince(since: number): Promise<unknown[]> {
  // Requête DB ou cache Redis
  return [];
}

function subscribeToMessages(callback: (msg: unknown) => void): () => void {
  // Retourne une fonction de désabonnement
  return () => {};
}
```

---

## Scaling WebSocket : Sticky Sessions et Redis Adapter

### Le problème des sticky sessions

Avec un load balancer classique (round-robin), un client qui se reconnecte peut atterrir sur une instance différente et perdre son état de session. La solution est le sticky sessions (session affinity) au niveau L4, mais elle crée une répartition inégale.

La vraie solution est de ne pas avoir d'état local sur les instances et d'utiliser Redis comme bus partagé.

```
Client A ─────┐                     ┌─── Instance 1
Client B ──── Load Balancer ────────┤         │
Client C ─────┘     (L4/L7)         └─── Instance 2
                                              │
                                       Redis Pub/Sub
                                    (message bus partagé)
```

### Scaling avec `@socket.io/redis-adapter`

```typescript
import { createServer } from 'http';
import { Server } from 'socket.io';
import { createClient } from 'redis';
import { createAdapter } from '@socket.io/redis-adapter';

const httpServer = createServer();
const io = new Server(httpServer);

const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);

// L'adapter Redis intercept toutes les émissions et les propage via pub/sub
io.adapter(createAdapter(pubClient, subClient));

// Désormais, io.to('room-123').emit() fonctionne même si les clients
// sont connectés sur des instances différentes
io.on('connection', (socket) => {
  socket.on('join', (roomId: string) => {
    socket.join(roomId);
  });

  socket.on('message', ({ roomId, content }: { roomId: string; content: string }) => {
    // Cet emit atteindra tous les clients dans la room,
    // quelle que soit l'instance à laquelle ils sont connectés
    io.to(roomId).emit('message', { content, from: socket.id });
  });
});

httpServer.listen(parseInt(process.env.PORT ?? '3000'));
```

---

## Tests WebSocket avec Vitest

```typescript
// tests/websocket.test.ts
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import { WebSocketServer, WebSocket } from 'ws';
import { createWebSocketServer } from '../src/server';

describe('Serveur WebSocket', () => {
  let wss: WebSocketServer;
  let serverPort: number;

  beforeAll(async () => {
    wss = await createWebSocketServer(0);  // Port 0 = OS choisit le port
    serverPort = (wss.address() as { port: number }).port;
  });

  afterAll(() => {
    wss.close();
  });

  it('devrait authentifier un client avec un token valide', async () => {
    const received: string[] = [];
    const client = new WebSocket(`ws://localhost:${serverPort}`);

    await new Promise<void>((resolve) => client.on('open', resolve));

    client.on('message', (data: Buffer) => {
      received.push(JSON.parse(data.toString()).type);
    });

    client.send(JSON.stringify({ type: 'AUTH', token: 'valid-test-token' }));

    await new Promise<void>((resolve) => setTimeout(resolve, 100));

    expect(received).toContain('AUTH_OK');
    client.close();
  });

  it('devrait diffuser un message à tous les membres d\'une room', async () => {
    const alice = new WebSocket(`ws://localhost:${serverPort}`);
    const bob = new WebSocket(`ws://localhost:${serverPort}`);

    const bobMessages: unknown[] = [];

    await Promise.all([
      new Promise<void>((r) => alice.on('open', r)),
      new Promise<void>((r) => bob.on('open', r)),
    ]);

    bob.on('message', (data: Buffer) => bobMessages.push(JSON.parse(data.toString())));

    // Authentifier et rejoindre la même room
    alice.send(JSON.stringify({ type: 'AUTH', token: 'alice-token' }));
    bob.send(JSON.stringify({ type: 'AUTH', token: 'bob-token' }));

    await new Promise<void>((r) => setTimeout(r, 50));

    alice.send(JSON.stringify({ type: 'JOIN_ROOM', roomId: 'test-room' }));
    bob.send(JSON.stringify({ type: 'JOIN_ROOM', roomId: 'test-room' }));

    await new Promise<void>((r) => setTimeout(r, 50));

    alice.send(JSON.stringify({ type: 'MESSAGE', roomId: 'test-room', content: 'Bonjour Bob' }));

    await new Promise<void>((r) => setTimeout(r, 100));

    const chatMsg = bobMessages.find((m: any) => m.type === 'MESSAGE');
    expect(chatMsg).toBeDefined();
    expect((chatMsg as any).content).toBe('Bonjour Bob');

    alice.close();
    bob.close();
  });
});
```

---

## Configuration Nginx pour WebSocket

```nginx
# /etc/nginx/sites-available/websocket-app
upstream websocket_backend {
    # ip_hash assure que le même client arrive toujours sur la même instance
    # (nécessaire uniquement sans Redis adapter)
    ip_hash;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
    server 127.0.0.1:3003;
}

server {
    listen 443 ssl http2;
    server_name api.mondomaine.fr;

    ssl_certificate     /etc/letsencrypt/live/api.mondomaine.fr/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.mondomaine.fr/privkey.pem;

    location /ws {
        proxy_pass http://websocket_backend;

        # Obligatoire pour l'upgrade WebSocket
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";

        # Transmettre l'IP réelle du client
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;

        # Timeouts étendus pour les connexions WebSocket longue durée
        proxy_read_timeout 3600s;   # 1 heure
        proxy_send_timeout 3600s;
        proxy_connect_timeout 10s;

        # Désactiver le buffering pour les WebSockets
        proxy_buffering off;
    }

    location /api {
        proxy_pass http://websocket_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Résumé des Décisions Architecturales

| Décision | Recommandation |
|----------|----------------|
| Auth au handshake | Utiliser le premier message applicatif, pas le query param (sécurité logs) |
| Compression | Activer `perMessageDeflate` pour JSON verbeux (économie 40-70%) |
| Heartbeat | Ping/pong toutes les 30s côté serveur pour détecter les connexions zombies |
| Reconnexion client | Exponential backoff + jitter ±30% pour éviter le thundering herd |
| Multi-instance | Redis adapter — ne jamais compter sur l'état local d'une instance |
| Choix WS vs SSE | SSE si unidirectionnel (notifications, métriques) — WS si bidirectionnel |
| Long polling | Uniquement comme fallback pour les environnements qui bloquent WS/SSE |
| Rate limiting | Limiter les connexions par IP dans `verifyClient` + `maxPayload` anti-DoS |
