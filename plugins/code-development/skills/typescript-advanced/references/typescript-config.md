# Configuration TypeScript — tsconfig, Project References et Compiler API

## Architecture des tsconfigs par environnement

La bonne pratique est de définir un `tsconfig.base.json` partagé et des configs spécialisées par environnement. Cela évite la duplication et garantit la cohérence.

### tsconfig.base.json — configuration racine

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": false,

    // Strict mode complet
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "useUnknownInCatchVariables": true,

    // Qualité du code
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,

    // Interop
    "esModuleInterop": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "resolveJsonModule": true
  }
}
```

### tsconfig.app-node.json — application Node.js

```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "lib": ["ES2022"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.spec.ts"]
}
```

### tsconfig.app-nextjs.json — application Next.js

```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "target": "ES5",
    "lib": ["dom", "dom.iterable", "ES2022"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@lib/*": ["./src/lib/*"],
      "@types/*": ["./src/types/*"]
    },
    // Next.js gère isolatedModules implicitement
    "isolatedModules": true,
    // verbatimModuleSyntax interdit re-export de types sans `export type`
    "verbatimModuleSyntax": false
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### tsconfig.test.json — tests avec Vitest

```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "types": ["vitest/globals"],
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "exactOptionalPropertyTypes": false
  },
  "include": ["src/**/*", "tests/**/*", "vitest.config.ts"],
  "exclude": ["node_modules", "dist"]
}
```

### tsconfig.lib.json — bibliothèque publiée sur npm

```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true,
    "emitDeclarationOnly": false,
    "outDir": "./dist",
    "rootDir": "./src",
    "composite": true,
    "module": "NodeNext",
    "moduleResolution": "NodeNext"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

## Options `strict` — explications détaillées

### strictNullChecks

```typescript
// Sans strictNullChecks — null et undefined assignables partout
let name: string = null; // Autorisé sans strict — dangereux

// Avec strictNullChecks
let nameStrict: string = null; // Erreur !
let nameOptional: string | null = null; // OK

function getUser(id: number): User | null {
  // ...
  return null;
}

const user = getUser(1);
// user.name — Erreur ! user peut être null
if (user !== null) {
  user.name; // OK — TypeScript a réduit le type
}
```

### strictFunctionTypes

```typescript
// Sans strictFunctionTypes — les méthodes sont bivariantes (dangereux)
type Handler = (event: MouseEvent) => void;
const handler: Handler = (e: Event) => {}; // Autorisé mais incorrect

// Avec strictFunctionTypes — contravariante pour les types de fonctions
// Les paramètres doivent être supertypes, pas sous-types
type StringHandler = (s: string) => void;
const numberHandler: StringHandler = (n: number) => {}; // Erreur !
```

### strictBindCallApply

```typescript
function greet(greeting: string, name: string): string {
  return `${greeting}, ${name}!`;
}

// Avec strictBindCallApply — les arguments sont vérifiés
greet.call(null, "Bonjour", "Alice");    // OK
greet.call(null, "Bonjour", 42);         // Erreur — 42 n'est pas string
greet.apply(null, ["Bonjour", "Alice"]); // OK
greet.bind(null, "Bonjour")("Alice");    // OK — type inféré correctement
```

### strictPropertyInitialization

```typescript
class UserService {
  // Avec strictPropertyInitialization
  private db: Database; // Erreur — non initialisé dans le constructeur !

  // Solutions :
  private db2: Database;     // Initialisé dans le constructeur
  private db3!: Database;    // Assertion definite assignment (avec précaution)
  private db4: Database | undefined; // Accepter undefined explicitement

  constructor(db: Database) {
    this.db2 = db; // OK
  }
}
```

### noImplicitAny et noImplicitThis

```typescript
// noImplicitAny — interdit any implicite
function processData(data) { // Erreur — data implicitement any
  return data.toUpperCase();
}

function processDataTyped(data: string) { // OK
  return data.toUpperCase();
}

// noImplicitThis — interdit this de type any
function greet() {
  return this.name; // Erreur — this est implicitement any
}

function greetTyped(this: { name: string }) {
  return this.name; // OK
}
```

## Options de qualité supplémentaires

### noUncheckedIndexedAccess

```typescript
// Sans noUncheckedIndexedAccess
const arr = [1, 2, 3];
const first: number = arr[0]; // Inféré comme number — peut être undefined !

// Avec noUncheckedIndexedAccess
const firstSafe = arr[0]; // Type: number | undefined

// Force à vérifier avant d'utiliser
if (firstSafe !== undefined) {
  const doubled = firstSafe * 2; // OK
}

// Avec les Records aussi
const map: Record<string, string> = {};
const value = map["key"]; // Type: string | undefined (avec noUncheckedIndexedAccess)
```

### exactOptionalPropertyTypes

```typescript
// Sans exactOptionalPropertyTypes
interface Config {
  timeout?: number;
}
const cfg: Config = { timeout: undefined }; // Autorisé

// Avec exactOptionalPropertyTypes
// timeout?: number signifie "absent OU number", PAS "number | undefined"
const cfgStrict: Config = { timeout: undefined }; // Erreur !
const cfgOK: Config = {}; // Correct — propriété absente
const cfgNum: Config = { timeout: 5000 }; // Correct

// Pour accepter undefined explicitement
interface ConfigExplicit {
  timeout?: number | undefined; // Explicite
}
```

### noImplicitOverride et noPropertyAccessFromIndexSignature

```typescript
class Animal {
  move(): void { console.log("Moving"); }
}

class Dog extends Animal {
  // Sans noImplicitOverride — override silencieux risqué
  // Avec noImplicitOverride — doit déclarer override explicitement
  override move(): void { console.log("Running"); } // OK
  // move(): void {} // Erreur sans override keyword !
}

// noPropertyAccessFromIndexSignature
interface StringMap {
  name: string; // Propriété connue
  [key: string]: string; // Index signature
}

const map: StringMap = { name: "Alice" };
map.name;       // OK — propriété connue
map["dynamic"]; // OK — accès par indexation (sans ambiguïté)
// map.dynamic  // Erreur avec noPropertyAccessFromIndexSignature !
```

## Project References — setup monorepo

Les Project References permettent à TypeScript de compiler des projets interdépendants de façon incrémentale.

```
monorepo/
├── packages/
│   ├── types/
│   │   ├── src/
│   │   └── tsconfig.json
│   ├── utils/
│   │   ├── src/
│   │   └── tsconfig.json
│   └── api/
│       ├── src/
│       └── tsconfig.json
└── tsconfig.json
```

### packages/types/tsconfig.json

```json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true,
    "rootDir": "./src",
    "outDir": "./dist"
  },
  "include": ["src/**/*"]
}
```

### packages/api/tsconfig.json — référence types

```json
{
  "compilerOptions": {
    "composite": true,
    "rootDir": "./src",
    "outDir": "./dist"
  },
  "references": [
    { "path": "../types" },
    { "path": "../utils" }
  ],
  "include": ["src/**/*"]
}
```

### tsconfig.json — racine du monorepo

```json
{
  "files": [],
  "references": [
    { "path": "./packages/types" },
    { "path": "./packages/utils" },
    { "path": "./packages/api" }
  ]
}
```

```bash
# Compiler tout le monorepo de façon incrémentale
tsc --build

# Recompiler à partir d'un package spécifique
tsc --build packages/api

# Nettoyer les artifacts
tsc --build --clean
```

## Declaration files `.d.ts` — création et augmentation

### Écrire ses propres déclarations

```typescript
// mon-module.d.ts
declare module "legacy-lib" {
  export interface LegacyConfig {
    host: string;
    port: number;
    debug?: boolean;
  }

  export function connect(config: LegacyConfig): Promise<void>;
  export function disconnect(): void;
  export class LegacyClient {
    constructor(config: LegacyConfig);
    query(sql: string): Promise<unknown[]>;
  }
}

// Variables globales (scripts navigateur)
declare const __APP_VERSION__: string;
declare const __DEV__: boolean;
```

### Augmentation de types de bibliothèques tierces

```typescript
// types/express.d.ts — augmenter Express Request
import "express";

declare module "express" {
  interface Request {
    user?: {
      id: number;
      email: string;
      roles: string[];
    };
    requestId: string;
  }
}

// Usage dans les routes
app.get("/profile", (req, res) => {
  if (!req.user) return res.status(401).json({ error: "Non authentifié" });
  res.json({ userId: req.user.id }); // TypeScript connaît req.user.id
});

// Augmentation globale
declare global {
  interface Array<T> {
    first(): T | undefined;
    last(): T | undefined;
  }
}

Array.prototype.first = function () { return this[0]; };
Array.prototype.last  = function () { return this[this.length - 1]; };
```

### declare namespace

```typescript
// Éviter les conflits de noms dans les grandes bases de code
declare namespace App {
  namespace Events {
    interface UserCreated { userId: number; email: string }
    interface UserDeleted { userId: number }
  }
  namespace Services {
    interface UserService {
      findById(id: number): Promise<unknown>;
    }
  }
}

const event: App.Events.UserCreated = { userId: 1, email: "alice@example.com" };
```

## verbatimModuleSyntax et isolatedModules

### verbatimModuleSyntax (TypeScript 5.0+)

```typescript
// verbatimModuleSyntax enforce l'utilisation de "import type" pour les types purs
// Évite que les bundlers incluent des imports qui ne sont que des types

// Mauvais — sera purgé par TS mais peut tromper les bundlers
import { User } from "./types";
const user: User = {}; // User est seulement un type

// Correct avec verbatimModuleSyntax
import type { User } from "./types"; // Clairement un import de type

// Ou inline
import { type User, UserService } from "./services";
// UserService est une valeur, User est un type — clair pour le bundler
```

### isolatedModules

```typescript
// isolatedModules: true — chaque fichier peut être transpilé indépendamment
// Interdit les fonctionnalités qui nécessitent l'analyse cross-fichiers

// Interdit — les const enums ne peuvent pas être résolus par fichier
const enum Direction { Up, Down } // Erreur avec isolatedModules !

// Autorisé — regular enums
enum DirectionOK { Up, Down } // OK (mais préférer union types)
type DirectionType = "Up" | "Down"; // Meilleure pratique

// Interdit — re-export ambigu (type ou valeur ?)
export { User } from "./user";     // Erreur si User est un type !
export type { User } from "./user"; // OK — explicitement un type
```

## Compiler API — lire et parcourir l'AST

```typescript
import ts from "typescript";

// Lire et typer un fichier TypeScript
function analyzeFile(filePath: string): void {
  const program = ts.createProgram([filePath], {
    target: ts.ScriptTarget.ES2022,
    module: ts.ModuleKind.NodeNext,
  });

  const sourceFile = program.getSourceFile(filePath);
  if (!sourceFile) throw new Error(`Fichier introuvable : ${filePath}`);

  // Parcourir tous les nœuds de l'AST
  function visit(node: ts.Node): void {
    // Trouver tous les console.log
    if (
      ts.isCallExpression(node) &&
      ts.isPropertyAccessExpression(node.expression) &&
      ts.isIdentifier(node.expression.expression) &&
      node.expression.expression.text === "console" &&
      node.expression.name.text === "log"
    ) {
      const { line, character } = sourceFile!.getLineAndCharacterOfPosition(
        node.getStart()
      );
      console.log(`console.log trouvé : ligne ${line + 1}, col ${character + 1}`);
    }

    ts.forEachChild(node, visit);
  }

  visit(sourceFile);
}

// Lister toutes les fonctions exportées d'un fichier
function listExportedFunctions(filePath: string): string[] {
  const program = ts.createProgram([filePath], {});
  const checker = program.getTypeChecker();
  const sourceFile = program.getSourceFile(filePath)!;
  const exports: string[] = [];

  sourceFile.forEachChild((node) => {
    if (
      ts.isFunctionDeclaration(node) &&
      node.name &&
      node.modifiers?.some((m) => m.kind === ts.SyntaxKind.ExportKeyword)
    ) {
      exports.push(node.name.text);
    }
  });

  return exports;
}
```

## ts-morph — manipulation d'AST simplifiée

```typescript
import { Project, SyntaxKind } from "ts-morph";

const project = new Project({
  tsConfigFilePath: "./tsconfig.json",
});

// Générer des types depuis une config JSON
function generateTypesFromJson(configPath: string, outputPath: string): void {
  const config = JSON.parse(require("fs").readFileSync(configPath, "utf-8"));

  function jsonToTypeScript(obj: unknown, name: string, indent = 0): string {
    const pad = "  ".repeat(indent);
    if (typeof obj === "string")  return "string";
    if (typeof obj === "number")  return "number";
    if (typeof obj === "boolean") return "boolean";
    if (obj === null) return "null";
    if (Array.isArray(obj)) {
      const itemType = obj.length > 0 ? jsonToTypeScript(obj[0], name) : "unknown";
      return `${itemType}[]`;
    }
    if (typeof obj === "object") {
      const entries = Object.entries(obj as Record<string, unknown>)
        .map(([k, v]) => `${pad}  ${k}: ${jsonToTypeScript(v, k, indent + 1)};`)
        .join("\n");
      return `{\n${entries}\n${pad}}`;
    }
    return "unknown";
  }

  const typeName = "Config";
  const typeContent = `export interface ${typeName} ${jsonToTypeScript(config, typeName)}`;

  const file = project.createSourceFile(outputPath, typeContent, { overwrite: true });
  file.formatText();
  project.saveSync();
}

// Refactoring automatique — renommer une propriété partout
function renameProperty(
  interfaceName: string,
  oldName: string,
  newName: string
): void {
  const sourceFiles = project.getSourceFiles();

  sourceFiles.forEach((file) => {
    // Renommer dans les interfaces
    file.getInterfaces()
      .filter((i) => i.getName() === interfaceName)
      .forEach((iface) => {
        iface.getProperty(oldName)?.rename(newName);
      });
  });

  project.saveSync();
}
```

## Type checking programmatique en CI

```bash
# tsconfig.ci.json — configuration pour la CI (sans émission)
```

```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "noEmit": true,
    "incremental": false,
    "tsBuildInfoFile": null
  }
}
```

```bash
# Script CI — vérification de types sans compilation
npx tsc --noEmit --project tsconfig.ci.json

# Avec ts-prune pour détecter les exports non utilisés
npx ts-prune --project tsconfig.json | grep -v "(used in module)"

# Script npm package.json
```

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "typecheck:watch": "tsc --noEmit --watch",
    "typecheck:strict": "tsc --noEmit --strict --noUncheckedIndexedAccess",
    "unused-exports": "ts-prune | grep -v 'used in module'"
  }
}
```

## Tableau récapitulatif — options strict

| Option | Défaut (strict: true) | Description |
|---|---|---|
| `strictNullChecks` | activé | null/undefined doivent être explicitement gérés |
| `strictFunctionTypes` | activé | Paramètres contravariant pour types de fonctions |
| `strictBindCallApply` | activé | call/bind/apply vérifient les types des arguments |
| `strictPropertyInitialization` | activé | Les propriétés doivent être initialisées |
| `noImplicitAny` | activé | Interdit le `any` implicite |
| `noImplicitThis` | activé | Interdit `this` sans annotation de type |
| `alwaysStrict` | activé | Émet `"use strict"` dans tous les fichiers |
| `noUncheckedIndexedAccess` | non | Les accès par index renvoient `T \| undefined` |
| `exactOptionalPropertyTypes` | non | Les propriétés optionnelles excluent `undefined` explicite |
| `noImplicitOverride` | non | Requiert le mot-clé `override` |
| `useUnknownInCatchVariables` | activé (TS4.4+) | Les erreurs dans catch sont `unknown`, pas `any` |

## Points clés à retenir

- Séparer les tsconfigs par environnement évite les incohérences entre app, tests et bibliothèques
- `noUncheckedIndexedAccess` et `exactOptionalPropertyTypes` sont les options les plus impactantes non incluses dans `strict`
- Les Project References accélèrent drastiquement la compilation en monorepo grâce à l'incrémental par package
- `verbatimModuleSyntax` force des imports explicites de types, améliore la compatibilité avec les bundlers modernes
- La Compiler API permet d'écrire des linters et des transformers personnalisés directement en TypeScript
