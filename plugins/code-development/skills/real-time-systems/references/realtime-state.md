# État Temps Réel — CRDT, Présence et Collaboration

## Operational Transform : Pourquoi les CRDTs ont Gagné

Operational Transform (OT) est l'approche historique de la collaboration en temps réel, utilisée par Google Docs (Wave). L'idée : chaque opération (insert, delete) est transformée en tenant compte des opérations concurrentes déjà appliquées pour maintenir la cohérence.

### Le Problème de Convergence d'OT

```
Texte initial : "abc"

Alice : Insère "X" en position 1 → "aXbc"
Bob   : Supprime le caractère en position 2 → "ac"

Sans transformation :
  - Alice voit "aXbc", applique la suppression de Bob en position 2 → "aXc"  ✓
  - Bob voit "ac", applique l'insertion d'Alice en position 1 → "aXc"  ✓

Mais avec 3 utilisateurs simultanés, les transformations deviennent
exponentiellement complexes : O(n²) transformations pour n utilisateurs.
```

OT fonctionne pour 2 utilisateurs mais souffre de :
- Algorithmes de transformation très complexes et difficiles à tester
- Nécessite un serveur central pour séquencer toutes les opérations (pas de P2P)
- Chaque type d'opération (texte, arbre DOM, JSON) nécessite son propre algorithme
- Des bugs de convergence célèbres dans des productions majeures

---

## CRDT : Conflict-free Replicated Data Types

Les CRDTs garantissent mathématiquement la convergence : deux réplicas ayant appliqué le même ensemble d'opérations (dans n'importe quel ordre) aboutiront toujours au même état.

### Propriétés de la Fonction de Fusion

Une structure CRDT doit satisfaire trois propriétés pour être valide :

| Propriété | Définition | Exemple |
|-----------|------------|---------|
| **Associativité** | `merge(merge(a,b),c) = merge(a,merge(b,c))` | L'ordre de traitement par lots ne change rien |
| **Commutativité** | `merge(a,b) = merge(b,a)` | L'ordre de réception ne change rien |
| **Idempotence** | `merge(a,a) = a` | Appliquer deux fois le même message ne cause pas de duplication |

### State-based CRDT (CvRDT) : Counter et G-Set

```typescript
// G-Counter : compteur qui ne peut qu'augmenter
class GCounter {
  private counts: Map<string, number>;

  constructor(private readonly nodeId: string) {
    this.counts = new Map([[nodeId, 0]]);
  }

  increment(amount = 1): void {
    const current = this.counts.get(this.nodeId) ?? 0;
    this.counts.set(this.nodeId, current + amount);
  }

  value(): number {
    let total = 0;
    for (const v of this.counts.values()) total += v;
    return total;
  }

  // Fusion commutative, associative, idempotente
  merge(other: GCounter): GCounter {
    const merged = new GCounter(this.nodeId);
    const allNodes = new Set([...this.counts.keys(), ...other.counts.keys()]);
    for (const node of allNodes) {
      merged.counts.set(node, Math.max(
        this.counts.get(node) ?? 0,
        other.counts.get(node) ?? 0,
      ));
    }
    return merged;
  }

  serialize(): Record<string, number> {
    return Object.fromEntries(this.counts);
  }

  static deserialize(data: Record<string, number>, nodeId: string): GCounter {
    const c = new GCounter(nodeId);
    c.counts = new Map(Object.entries(data));
    return c;
  }
}

// G-Set : ensemble qui ne peut qu'ajouter des éléments
class GSet<T> {
  private items: Set<string>;

  constructor() {
    this.items = new Set();
  }

  add(item: T): void {
    this.items.add(JSON.stringify(item));
  }

  has(item: T): boolean {
    return this.items.has(JSON.stringify(item));
  }

  values(): T[] {
    return [...this.items].map(s => JSON.parse(s) as T);
  }

  merge(other: GSet<T>): GSet<T> {
    const merged = new GSet<T>();
    merged.items = new Set([...this.items, ...other.items]);
    return merged;
  }
}

// OR-Set : permet d'ajouter ET retirer des éléments
class ORSet<T> {
  // Chaque élément est associé à un ensemble d'IDs uniques (tags)
  private added: Map<string, Set<string>> = new Map();
  private removed: Set<string> = new Set();

  add(item: T): void {
    const key = JSON.stringify(item);
    const tag = crypto.randomUUID();
    if (!this.added.has(key)) this.added.set(key, new Set());
    this.added.get(key)!.add(tag);
  }

  remove(item: T): void {
    const key = JSON.stringify(item);
    const tags = this.added.get(key);
    if (tags) tags.forEach(tag => this.removed.add(tag));
  }

  has(item: T): boolean {
    const key = JSON.stringify(item);
    const tags = this.added.get(key);
    if (!tags || tags.size === 0) return false;
    // L'élément est présent si au moins un tag n'a pas été retiré
    return [...tags].some(tag => !this.removed.has(tag));
  }

  merge(other: ORSet<T>): ORSet<T> {
    const merged = new ORSet<T>();
    // Union des éléments ajoutés
    for (const [key, tags] of this.added) {
      merged.added.set(key, new Set(tags));
    }
    for (const [key, tags] of other.added) {
      if (!merged.added.has(key)) merged.added.set(key, new Set());
      tags.forEach(tag => merged.added.get(key)!.add(tag));
    }
    // Union des suppressions
    merged.removed = new Set([...this.removed, ...other.removed]);
    return merged;
  }
}
```

---

## Yjs : Le CRDT de Production pour la Collaboration

Yjs est l'implémentation CRDT la plus mature et la plus utilisée en production. Il implémente un CRDT de séquence (pour le texte) basé sur une structure en arbre avec des identifiants de position uniques.

### Y.Doc, Y.Text, Y.Array, Y.Map

```typescript
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';
import { IndexeddbPersistence } from 'y-indexeddb';

// Document CRDT principal
const ydoc = new Y.Doc();

// Types collaboratifs partagés
const sharedText = ydoc.getText('document-content');
const sharedArray = ydoc.getArray<string>('messages');
const sharedMap = ydoc.getMap<unknown>('metadata');

// Provider WebSocket : synchronise avec le serveur Yjs
const wsProvider = new WebsocketProvider(
  'wss://collaboration.monapp.fr',
  'document-room-123',
  ydoc,
  { connect: true },
);

// Provider IndexedDB : persistance locale (offline first)
const idbProvider = new IndexeddbPersistence('document-room-123', ydoc);

wsProvider.on('status', ({ status }: { status: string }) => {
  console.log('Statut de connexion :', status);
});

// Observer les changements
sharedText.observe((event: Y.YTextEvent) => {
  console.log('Texte modifié :', event.changes);
});

sharedMap.observe((event: Y.YMapEvent<unknown>) => {
  event.changes.keys.forEach((change, key) => {
    if (change.action === 'add') console.log(`Clé ajoutée : ${key}`);
    if (change.action === 'update') console.log(`Clé modifiée : ${key}`);
    if (change.action === 'delete') console.log(`Clé supprimée : ${key}`);
  });
});

// Toutes les modifications sont automatiquement fusionnées
ydoc.transact(() => {
  sharedText.insert(0, 'Premier paragraphe\n');
  sharedMap.set('author', 'Alice');
  sharedMap.set('version', 1);
}, 'init-transaction');
```

### Intégration avec TipTap

```typescript
// Installation : npm install @tiptap/extension-collaboration @tiptap/extension-collaboration-cursor
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Collaboration from '@tiptap/extension-collaboration';
import CollaborationCursor from '@tiptap/extension-collaboration-cursor';
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';

interface CollaborativeEditorProps {
  documentId: string;
  userName: string;
  userColor: string;
}

function CollaborativeEditor({ documentId, userName, userColor }: CollaborativeEditorProps) {
  const ydoc = new Y.Doc();
  const provider = new WebsocketProvider(
    'wss://collab.monapp.fr',
    documentId,
    ydoc,
  );

  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        // Désactiver les extensions d'historique natifs — remplacés par Yjs UndoManager
        history: false,
      }),
      Collaboration.configure({
        document: ydoc,
      }),
      CollaborationCursor.configure({
        provider,
        user: {
          name: userName,
          color: userColor,
        },
      }),
    ],
  });

  return <EditorContent editor={editor} />;
}
```

### Intégration avec CodeMirror 6

```typescript
import { EditorView, basicSetup } from 'codemirror';
import { javascript } from '@codemirror/lang-javascript';
import { yCollab } from 'y-codemirror.next';
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';

const ydoc = new Y.Doc();
const ytext = ydoc.getText('codemirror-content');
const provider = new WebsocketProvider('wss://collab.monapp.fr', 'code-room', ydoc);

const view = new EditorView({
  extensions: [
    basicSetup,
    javascript(),
    yCollab(ytext, provider.awareness, {
      undoManager: new Y.UndoManager(ytext),
    }),
  ],
  parent: document.getElementById('editor')!,
});
```

---

## Awareness : Curseurs, Sélections et Présence

L'Awareness est le mécanisme Yjs pour partager des données éphémères (non persistées) : position du curseur, sélection, nom de l'utilisateur, statut.

```typescript
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';
import { Awareness } from 'y-protocols/awareness';

const ydoc = new Y.Doc();
const provider = new WebsocketProvider('wss://collab.monapp.fr', 'room', ydoc);
const awareness: Awareness = provider.awareness;

// Définir l'état local de présence
awareness.setLocalState({
  user: {
    id: 'user-alice',
    name: 'Alice Martin',
    color: '#4F46E5',
    avatar: 'https://cdn.monapp.fr/avatars/alice.jpg',
  },
  cursor: null,       // Position du curseur dans le document
  selection: null,    // Sélection en cours
  status: 'active',  // 'active' | 'idle' | 'offline'
});

// Mettre à jour la position du curseur
function updateCursor(index: number | null): void {
  awareness.setLocalStateField('cursor', index !== null ? { index } : null);
}

// Observer les changements d'awareness de tous les utilisateurs
awareness.on('change', ({ added, updated, removed }: { added: number[]; updated: number[]; removed: number[] }) => {
  const states = awareness.getStates();

  // Rendre les curseurs distants
  for (const clientId of [...added, ...updated]) {
    if (clientId === awareness.clientID) continue;  // Ignorer soi-même
    const state = states.get(clientId);
    if (state?.cursor) {
      renderRemoteCursor(clientId, state.cursor.index, state.user.color, state.user.name);
    }
  }

  // Retirer les curseurs des utilisateurs déconnectés
  for (const clientId of removed) {
    removeRemoteCursor(clientId);
  }
});

function renderRemoteCursor(_clientId: number, _index: number, _color: string, _name: string): void {
  // Injecter un élément DOM pour afficher le curseur coloré
}

function removeRemoteCursor(_clientId: number): void {
  // Retirer l'élément DOM du curseur
}
```

### Throttling des Curseurs (requestAnimationFrame)

```typescript
// Éviter d'envoyer un événement cursor à chaque frappe — limiter à ~60fps
let pendingCursorUpdate: number | null = null;

function onSelectionChange(index: number): void {
  if (pendingCursorUpdate !== null) {
    cancelAnimationFrame(pendingCursorUpdate);
  }
  pendingCursorUpdate = requestAnimationFrame(() => {
    awareness.setLocalStateField('cursor', { index });
    pendingCursorUpdate = null;
  });
}
```

---

## Automerge : Alternative à Yjs

Automerge propose une approche différente : le document CRDT est un JSON modifiable, avec un historique complet des opérations.

```typescript
import * as Automerge from '@automerge/automerge';

interface Document {
  titre: string;
  contenu: string;
  tags: string[];
  metadata: Record<string, unknown>;
}

// Créer un document
let docAlice = Automerge.init<Document>();

// Modifier le document (toujours via change())
docAlice = Automerge.change(docAlice, 'Initialisation', (doc) => {
  doc.titre = 'Rapport Q1 2026';
  doc.contenu = 'Introduction\n';
  doc.tags = ['rapport', 'Q1'];
  doc.metadata = { version: 1 };
});

// Simuler Bob qui part d'une copie du document
let docBob = Automerge.clone(docAlice);

// Alice et Bob modifient le document simultanément (offline)
docAlice = Automerge.change(docAlice, 'Alice ajoute contenu', (doc) => {
  doc.contenu += 'Section 1 : Contexte\n';
});

docBob = Automerge.change(docBob, 'Bob modifie le titre', (doc) => {
  doc.titre = 'Rapport Q1 2026 — Version Finale';
  doc.tags.push('final');
});

// Fusion des deux versions divergentes — convergence garantie
const mergedAlice = Automerge.merge(docAlice, docBob);
const mergedBob = Automerge.merge(docBob, docAlice);

// Les deux docs sont identiques après fusion
console.log(mergedAlice.titre);    // 'Rapport Q1 2026 — Version Finale'
console.log(mergedAlice.contenu);  // 'Introduction\nSection 1 : Contexte\n'
console.log(Automerge.equals(mergedAlice, mergedBob));  // true

// Sérialisation pour stockage/transmission
const bytes = Automerge.save(mergedAlice);
const loaded = Automerge.load<Document>(bytes);
```

---

## Présence Avancée : Heartbeat et Expiration

```typescript
import { Redis } from 'ioredis';

const redis = new Redis(process.env.REDIS_URL!);

interface PresenceData {
  userId: string;
  status: 'active' | 'idle' | 'offline';
  lastSeen: number;
  metadata?: Record<string, unknown>;
}

const PRESENCE_TTL = 45;         // Secondes avant expiration automatique
const HEARTBEAT_INTERVAL = 20_000; // Renouveler toutes les 20s

class PresenceManager {
  private heartbeatTimer: ReturnType<typeof setInterval> | null = null;

  async setPresence(userId: string, data: Partial<PresenceData>): Promise<void> {
    const key = `presence:${userId}`;
    const presence: PresenceData = {
      userId,
      status: 'active',
      lastSeen: Date.now(),
      ...data,
    };

    // Stocker la présence avec TTL automatique
    await redis.setex(key, PRESENCE_TTL, JSON.stringify(presence));

    // Publier le changement pour les abonnés temps réel
    await redis.publish('presence:changes', JSON.stringify({ type: 'PRESENCE_UPDATE', ...presence }));
  }

  async removePresence(userId: string): Promise<void> {
    await redis.del(`presence:${userId}`);
    await redis.publish('presence:changes', JSON.stringify({
      type: 'PRESENCE_UPDATE',
      userId,
      status: 'offline',
      lastSeen: Date.now(),
    }));
  }

  startHeartbeat(userId: string): void {
    this.heartbeatTimer = setInterval(async () => {
      await this.setPresence(userId, { status: 'active' });
    }, HEARTBEAT_INTERVAL);
  }

  stopHeartbeat(userId: string): void {
    if (this.heartbeatTimer) clearInterval(this.heartbeatTimer);
    this.removePresence(userId).catch(console.error);
  }

  async getPresence(userIds: string[]): Promise<PresenceData[]> {
    if (userIds.length === 0) return [];

    const keys = userIds.map(id => `presence:${id}`);
    const values = await redis.mget(...keys);

    return values
      .map((v, i) => {
        if (!v) {
          return {
            userId: userIds[i],
            status: 'offline' as const,
            lastSeen: 0,
          };
        }
        return JSON.parse(v) as PresenceData;
      });
  }

  async getOnlineUsers(roomId: string): Promise<string[]> {
    // Utiliser un Z-Set trié pour lister les membres d'une room avec leur timestamp
    const members = await redis.zrangebyscore(
      `room:${roomId}:members`,
      Date.now() - PRESENCE_TTL * 1000,
      '+inf',
    );
    return members;
  }
}
```

---

## Undo/Redo Distribué avec Yjs UndoManager

```typescript
import * as Y from 'yjs';

const ydoc = new Y.Doc();
const sharedText = ydoc.getText('content');

// UndoManager : capture uniquement les opérations locales
// Les opérations distantes ne sont pas dans la pile d'undo
const undoManager = new Y.UndoManager(sharedText, {
  captureTimeout: 500,  // Grouper les opérations en moins de 500ms
});

// Effectuer des modifications locales
ydoc.transact(() => {
  sharedText.insert(0, 'Texte initial ');
});

ydoc.transact(() => {
  sharedText.insert(14, 'modifié ');
});

console.log(sharedText.toString());  // 'Texte initial modifié '

// Undo local — ne défait PAS les modifications des autres collaborateurs
undoManager.undo();
console.log(sharedText.toString());  // 'Texte initial '

// Redo
undoManager.redo();
console.log(sharedText.toString());  // 'Texte initial modifié '

// Écouter les événements undo/redo pour mettre à jour l'UI
undoManager.on('stack-cleared', () => {
  updateUndoRedoButtons(undoManager.canUndo(), undoManager.canRedo());
});

undoManager.on('stack-item-added', () => {
  updateUndoRedoButtons(undoManager.canUndo(), undoManager.canRedo());
});

function updateUndoRedoButtons(_canUndo: boolean, _canRedo: boolean): void {
  // Activer/désactiver les boutons Ctrl+Z et Ctrl+Y
}
```

---

## Locking Optimiste : Version et Détection de Conflits

```typescript
// Pour les cas où les CRDTs ne sont pas appropriés (ex : mise à jour d'un champ unique)
// Utiliser le locking optimiste basé sur une version

interface VersionedDocument {
  id: string;
  content: string;
  version: number;
  updatedAt: Date;
  updatedBy: string;
}

// Mise à jour avec détection de conflit
async function updateDocument(
  db: Database,
  documentId: string,
  userId: string,
  content: string,
  expectedVersion: number,
): Promise<{ success: true; doc: VersionedDocument } | { success: false; conflict: VersionedDocument }> {
  // Lire l'état actuel
  const current = await db.findOne<VersionedDocument>({ id: documentId });

  if (current.version !== expectedVersion) {
    // Conflit : quelqu'un d'autre a modifié le document entre-temps
    return { success: false, conflict: current };
  }

  // Mise à jour atomique avec condition sur la version
  const updated = await db.findOneAndUpdate(
    { id: documentId, version: expectedVersion },  // Condition atomique
    {
      $set: { content, updatedAt: new Date(), updatedBy: userId },
      $inc: { version: 1 },
    },
    { returnDocument: 'after' },
  );

  if (!updated) {
    // Race condition : une autre requête a gagné entre la lecture et l'écriture
    const fresh = await db.findOne<VersionedDocument>({ id: documentId });
    return { success: false, conflict: fresh };
  }

  return { success: true, doc: updated };
}

// Côté client : gérer le conflit
async function handleDocumentSave(content: string, localVersion: number): Promise<void> {
  const result = await updateDocument(db, docId, userId, content, localVersion);

  if (result.success) {
    setLocalVersion(result.doc.version);
    showSuccessToast('Document sauvegardé');
  } else {
    // Proposer une interface de résolution de conflit à l'utilisateur
    showConflictDialog({
      myVersion: content,
      theirVersion: result.conflict.content,
      theirAuthor: result.conflict.updatedBy,
      onMerge: (mergedContent) => handleDocumentSave(mergedContent, result.conflict.version),
      onOverwrite: () => handleDocumentSave(content, result.conflict.version),
    });
  }
}

interface Database {
  findOne<T>(query: Record<string, unknown>): Promise<T>;
  findOneAndUpdate(
    filter: Record<string, unknown>,
    update: Record<string, unknown>,
    options: Record<string, unknown>,
  ): Promise<unknown>;
}

declare const db: Database;
declare const docId: string;
declare const userId: string;
function setLocalVersion(_v: number): void { /* update local state */ }
function showSuccessToast(_msg: string): void { /* toast */ }
function showConflictDialog(_opts: unknown): void { /* dialog */ }
```

---

## Persistence de la Collaboration : Snapshots Yjs

```typescript
import * as Y from 'yjs';
import { fromUint8Array, toUint8Array } from 'js-base64';

interface CollaborationSnapshot {
  documentId: string;
  snapshot: string;       // Y.Doc encodé en Base64
  createdAt: Date;
  version: number;
}

// Sauvegarder un snapshot du Y.Doc dans PostgreSQL
async function saveSnapshot(
  db: Database,
  documentId: string,
  ydoc: Y.Doc,
): Promise<void> {
  const state = Y.encodeStateAsUpdate(ydoc);
  const base64 = fromUint8Array(state);

  await db.upsert('collaboration_snapshots', {
    document_id: documentId,
    snapshot: base64,
    created_at: new Date(),
    version: ydoc.clientID,
  });
}

// Restaurer un Y.Doc depuis la base de données
async function loadSnapshot(
  db: Database,
  documentId: string,
): Promise<Y.Doc | null> {
  const row = await db.findOne<CollaborationSnapshot>({
    document_id: documentId,
  });

  if (!row) return null;

  const ydoc = new Y.Doc();
  const state = toUint8Array(row.snapshot);
  Y.applyUpdate(ydoc, state);
  return ydoc;
}

// Avec Hocuspocus (serveur Yjs dédié)
// @hocuspocus/server gère automatiquement les snapshots et la synchronisation
import { Server } from '@hocuspocus/server';
import { Database as HocuspocusDatabase } from '@hocuspocus/extension-database';

const server = Server.configure({
  port: 1234,

  extensions: [
    new HocuspocusDatabase({
      fetch: async ({ documentName }) => {
        // Charger le snapshot depuis PostgreSQL
        const row = await pgClient.query(
          'SELECT snapshot FROM ydoc_snapshots WHERE document_id = $1',
          [documentName],
        );
        if (row.rows.length === 0) return null;
        return toUint8Array(row.rows[0].snapshot);
      },
      store: async ({ documentName, state }) => {
        // Sauvegarder toutes les 30s automatiquement
        await pgClient.query(
          'INSERT INTO ydoc_snapshots (document_id, snapshot) VALUES ($1, $2) ON CONFLICT (document_id) DO UPDATE SET snapshot = $2, updated_at = NOW()',
          [documentName, fromUint8Array(state)],
        );
      },
    }),
  ],
});

await server.listen();

declare const pgClient: { query(sql: string, params?: unknown[]): Promise<{ rows: Array<Record<string, string>> }> };
```

---

## Testing CRDT : Simuler des Modifications Concurrentes

```typescript
import { describe, it, expect } from 'vitest';
import * as Y from 'yjs';

describe('CRDT - Convergence des modifications concurrentes', () => {
  it('devrait converger après des insertions simultanées de texte', () => {
    // Simuler Alice et Bob avec des docs isolés
    const docAlice = new Y.Doc();
    const docBob = new Y.Doc();

    // Synchroniser l'état initial
    const initialState = Y.encodeStateAsUpdate(docAlice);
    Y.applyUpdate(docBob, initialState);

    const textAlice = docAlice.getText('content');
    const textBob = docBob.getText('content');

    // Modifications simultanées (offline)
    textAlice.insert(0, 'Alice');
    textBob.insert(0, 'Bob');

    // Capturer les updates
    const aliceUpdate = Y.encodeStateAsUpdate(docAlice);
    const bobUpdate = Y.encodeStateAsUpdate(docBob);

    // Appliquer les updates croisés
    Y.applyUpdate(docAlice, bobUpdate);
    Y.applyUpdate(docBob, aliceUpdate);

    // Vérifier la convergence — les deux docs doivent être identiques
    expect(textAlice.toString()).toBe(textBob.toString());

    // Le résultat contient les contributions des deux (ordre déterministe)
    expect(textAlice.toString()).toContain('Alice');
    expect(textAlice.toString()).toContain('Bob');
  });

  it('devrait converger avec 3 utilisateurs simultanés', () => {
    const docs = [new Y.Doc(), new Y.Doc(), new Y.Doc()];
    const names = ['Alice', 'Bob', 'Charlie'];

    // Chaque utilisateur insère son nom
    docs.forEach((doc, i) => {
      doc.getText('content').insert(0, names[i]);
    });

    // Échanger tous les updates entre tous les docs
    const updates = docs.map(doc => Y.encodeStateAsUpdate(doc));

    docs.forEach((doc, i) => {
      updates.forEach((update, j) => {
        if (i !== j) Y.applyUpdate(doc, update);
      });
    });

    // Tous les docs doivent avoir le même contenu
    const contents = docs.map(doc => doc.getText('content').toString());
    expect(new Set(contents).size).toBe(1);  // Toutes identiques
    console.log('Résultat convergent :', contents[0]);
  });
});
```

---

## Résumé : Choisir l'Approche de Collaboration

| Scénario | Solution recommandée |
|----------|---------------------|
| Éditeur de texte collaboratif | Yjs + TipTap/CodeMirror + Hocuspocus |
| JSON collaboratif (configuration, settings) | Automerge |
| Compteurs distribués (likes, vues) | G-Counter CRDT ou Redis INCR |
| Présence utilisateurs | Awareness Yjs ou Redis avec TTL |
| Formulaire concurrent simple | Locking optimiste (version field) |
| Undo/Redo local dans un doc partagé | Y.UndoManager |
| Curseurs et sélections | Awareness Yjs (éphémère, non persisté) |
| Implémentation CRDT custom | Éviter — utiliser Yjs ou Automerge |
