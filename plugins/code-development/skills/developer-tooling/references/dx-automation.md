# DX et Automatisation — Génération de Code, CLI et Terminal

## Plop Templates Avancés

Plop est un micro-générateur qui transforme les tâches répétitives de création de fichiers en commandes interactives reproductibles.

### Configuration complète avec helpers et validations

```javascript
// plopfile.js
import { Plop, run } from "plop";
import { fileURLToPath } from "url";
import path from "path";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default function (plop) {
  // Helpers custom
  plop.setHelper("upperFirst", (str) =>
    str.charAt(0).toUpperCase() + str.slice(1)
  );
  plop.setHelper("featurePath", (name) =>
    `src/features/${plop.getHelper("kebabCase")(name)}`
  );
  plop.setHelper("plural", (word) => {
    const irregular = { person: "people", child: "children" };
    return irregular[word] ?? (word.endsWith("y") ? word.slice(0, -1) + "ies" : word + "s");
  });

  // Générateur de composant React
  plop.setGenerator("component", {
    description: "Crée un composant React avec tests et stories",
    prompts: [
      {
        type: "input",
        name: "name",
        message: "Nom du composant (PascalCase):",
        validate: (value) => {
          if (!value) return "Le nom est obligatoire";
          if (!/^[A-Z][a-zA-Z0-9]*$/.test(value)) {
            return "Le nom doit être en PascalCase (ex: MyButton)";
          }
          if (fs.existsSync(`src/components/${value}`)) {
            return `Le composant ${value} existe déjà`;
          }
          return true;
        },
      },
      {
        type: "list",
        name: "type",
        message: "Type de composant:",
        choices: ["ui", "feature", "layout", "page"],
        default: "ui",
      },
      {
        type: "confirm",
        name: "withTests",
        message: "Inclure les tests Vitest?",
        default: true,
      },
      {
        type: "confirm",
        name: "withStories",
        message: "Inclure les Storybook stories?",
        default: (answers) => answers.type === "ui",
      },
    ],
    actions: (data) => {
      const actions = [
        // Action principale : créer le composant
        {
          type: "add",
          path: "src/components/{{type}}/{{pascalCase name}}/{{pascalCase name}}.tsx",
          templateFile: "plop-templates/component.tsx.hbs",
        },
        // Toujours créer l'index
        {
          type: "add",
          path: "src/components/{{type}}/{{pascalCase name}}/index.ts",
          templateFile: "plop-templates/component-index.ts.hbs",
        },
        // Modifier le barrel file du dossier parent
        {
          type: "append",
          path: "src/components/{{type}}/index.ts",
          pattern: /\/\/ PLOP_EXPORTS/,
          template:
            'export { {{pascalCase name}} } from "./{{pascalCase name}}";',
        },
      ];

      // Actions conditionnelles
      if (data?.withTests) {
        actions.push({
          type: "add",
          path: "src/components/{{type}}/{{pascalCase name}}/{{pascalCase name}}.test.tsx",
          templateFile: "plop-templates/component.test.tsx.hbs",
        });
      }

      if (data?.withStories) {
        actions.push({
          type: "add",
          path: "src/components/{{type}}/{{pascalCase name}}/{{pascalCase name}}.stories.tsx",
          templateFile: "plop-templates/component.stories.tsx.hbs",
        });
      }

      return actions;
    },
  });

  // addMany — créer une arborescence complète
  plop.setGenerator("feature", {
    description: "Crée une feature complète (slice Redux + composants + API)",
    prompts: [
      { type: "input", name: "name", message: "Nom de la feature:" },
    ],
    actions: [
      {
        type: "addMany",
        destination: "src/features/{{kebabCase name}}",
        templateFiles: "plop-templates/feature/**",
        base: "plop-templates/feature",
      },
    ],
  });
}
```

```handlebars
{{! plop-templates/component.tsx.hbs }}
import { type FC } from "react";
import styles from "./{{pascalCase name}}.module.css";

interface {{pascalCase name}}Props {
  className?: string;
}

export const {{pascalCase name}}: FC<{{pascalCase name}}Props> = ({ className }) => {
  return (
    <div className={[styles.root, className].filter(Boolean).join(" ")}>
      {{pascalCase name}}
    </div>
  );
};
```

## Hygen Generators

Hygen offre une approche basée sur des fichiers dans `_templates/`, avec logique en JavaScript via `frontmatter.js`.

```bash
# Initialisation
npx hygen init self
npx hygen generator new my-generator

# Structure des templates
# _templates/
#   component/
#     new/
#       index.js.ejs.t   ← fichier généré
#       index.ejs.t      ← logique frontmatter
```

```javascript
// _templates/service/new/index.js.ejs.t
---
to: src/services/<%= h.inflection.dasherize(name) %>.service.ts
---
import { Injectable } from "@nestjs/common";
import type { <%= h.capitalize(name) %>Repository } from "../repositories";

@Injectable()
export class <%= h.capitalize(name) %>Service {
  constructor(
    private readonly repository: <%= h.capitalize(name) %>Repository
  ) {}

  async findAll() {
    return this.repository.findAll();
  }

  async findById(id: string) {
    return this.repository.findById(id);
  }
}
```

```javascript
// _templates/service/new/prompt.js — logique de frontmatter
module.exports = {
  prompt: ({ prompter, args }) =>
    prompter.prompt([
      {
        type: "input",
        name: "name",
        message: "Nom du service (camelCase):",
        validate: (v) => v.length > 0 || "Obligatoire",
      },
      {
        type: "select",
        name: "withCache",
        message: "Ajouter le cache Redis?",
        choices: ["Oui", "Non"],
      },
    ]),
};
```

## CLI avec Commander.js Avancé

### Architecture d'un CLI professionnel

```typescript
// src/cli/index.ts
import { Command, Option } from "commander";
import { version } from "../../package.json";

const program = new Command();

program
  .name("company-cli")
  .description("CLI interne — génération de code et utilitaires")
  .version(version, "-v, --version")
  .configureHelp({
    sortOptions: true,
    showGlobalOptions: true,
    formatHelp: (cmd, helper) => {
      const help = helper.formatHelp(cmd, helper);
      return `\n${help}\n  Documentation: https://internal.company.com/cli\n`;
    },
  })
  .configureOutput({
    writeErr: (str) => process.stderr.write(`\x1b[31m${str}\x1b[0m`),
  })
  .hook("preAction", (thisCommand) => {
    if (process.env.DEBUG === "cli") {
      console.error("Command:", thisCommand.name());
      console.error("Options:", thisCommand.opts());
    }
  });

// Sous-commande generate
const generate = program.command("generate").alias("g")
  .description("Générer du code à partir de templates");

generate
  .command("service <name>")
  .description("Créer un micro-service Fastify + Prisma + Vitest")
  .addOption(
    new Option("--no-docker", "Omettre la configuration Docker")
  )
  .addOption(
    new Option("-t, --template <type>", "Type de template")
      .choices(["fastify", "express", "nestjs"])
      .default("fastify")
  )
  .action(async (name, options) => {
    const { generateService } = await import("./commands/generate-service.js");
    await generateService(name, options);
  });

// Auto-completion shell
program
  .command("completion")
  .description("Générer le script de completion shell")
  .argument("<shell>", "Shell cible")
  .addArgument(new Argument("[shell]", "Shell").choices(["bash", "zsh", "fish"]))
  .action((shell) => {
    const completions = { bash: "...", zsh: "...", fish: "..." };
    console.log(completions[shell as keyof typeof completions]);
  });

program.parseAsync(process.argv).catch((err) => {
  console.error("\x1b[31mErreur:\x1b[0m", err.message);
  process.exit(1);
});
```

## Ink — React pour le Terminal

### Interface terminal avec composants React

```tsx
// src/cli/ui/ServiceGenerator.tsx
import React, { useState, useEffect } from "react";
import { Box, Text, useApp, useInput } from "ink";
import SelectInput from "ink-select-input";
import TextInput from "ink-text-input";
import Spinner from "ink-spinner";

interface Step {
  label: string;
  status: "pending" | "running" | "done" | "error";
}

interface ServiceGeneratorProps {
  serviceName: string;
  onComplete: (success: boolean) => void;
}

export const ServiceGenerator: React.FC<ServiceGeneratorProps> = ({
  serviceName,
  onComplete,
}) => {
  const { exit } = useApp();
  const [steps, setSteps] = useState<Step[]>([
    { label: "Créer la structure de dossiers", status: "pending" },
    { label: "Générer les fichiers source", status: "pending" },
    { label: "Installer les dépendances", status: "pending" },
    { label: "Initialiser la base de données", status: "pending" },
    { label: "Configurer les tests", status: "pending" },
  ]);
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const runSteps = async () => {
      for (let i = 0; i < steps.length; i++) {
        setSteps((prev) =>
          prev.map((s, idx) =>
            idx === i ? { ...s, status: "running" } : s
          )
        );
        setCurrentStep(i);

        // Simuler le travail réel
        await new Promise((resolve) => setTimeout(resolve, 800));

        setSteps((prev) =>
          prev.map((s, idx) =>
            idx === i ? { ...s, status: "done" } : s
          )
        );
      }
      onComplete(true);
    };

    runSteps().catch(() => onComplete(false));
  }, []);

  return (
    <Box flexDirection="column" paddingY={1}>
      <Box marginBottom={1}>
        <Text bold color="cyan">
          Génération du service:{" "}
        </Text>
        <Text bold color="white">
          {serviceName}
        </Text>
      </Box>

      {steps.map((step, idx) => (
        <Box key={idx} marginLeft={2}>
          <Box width={3}>
            {step.status === "running" && (
              <Text color="yellow">
                <Spinner type="dots" />
              </Text>
            )}
            {step.status === "done" && <Text color="green">✓</Text>}
            {step.status === "error" && <Text color="red">✗</Text>}
            {step.status === "pending" && <Text color="gray">○</Text>}
          </Box>
          <Text
            color={
              step.status === "done"
                ? "green"
                : step.status === "running"
                ? "yellow"
                : step.status === "error"
                ? "red"
                : "gray"
            }
          >
            {step.label}
          </Text>
        </Box>
      ))}

      <Box marginTop={1}>
        <Text color="gray">
          Étape {Math.min(currentStep + 1, steps.length)} / {steps.length}
        </Text>
      </Box>
    </Box>
  );
};
```

```tsx
// Lancement du composant Ink
import { render } from "ink";
import React from "react";
import { ServiceGenerator } from "./ui/ServiceGenerator.js";

render(
  <ServiceGenerator
    serviceName="payment-service"
    onComplete={(success) => process.exit(success ? 0 : 1)}
  />
);
```

## Configuration Terminale Avancée

### zsh et oh-my-zsh pour les développeurs

```bash
# ~/.zshrc — configuration pour les projets Node.js

# NVM avec chargement paresseux (améliore le temps de démarrage du shell)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" --no-use
alias nvm="unset -f nvm; source $NVM_DIR/nvm.sh; nvm"

# Plugins oh-my-zsh utiles
plugins=(git node docker kubectl zsh-autosuggestions zsh-syntax-highlighting)

# Alias de développement
alias t="pnpm test"
alias b="pnpm build"
alias dev="pnpm dev"
alias la="ls -la"
alias ..="cd .."
alias ...="cd ../.."

# Fonction : créer un dossier et s'y déplacer
mkcd() { mkdir -p "$1" && cd "$1"; }

# Fonction : trouver et tuer le processus sur un port
killport() {
  local pid=$(lsof -ti:"$1")
  if [ -n "$pid" ]; then
    kill -9 "$pid"
    echo "Processus $pid tué sur le port $1"
  else
    echo "Aucun processus sur le port $1"
  fi
}

# Fonction : afficher les branches git récentes
recent-branches() {
  git for-each-ref --sort=-committerdate refs/heads/ \
    --format='%(refname:short)' | head -n "${1:-10}"
}

# Auto-switch Node.js version selon .nvmrc
autoload -U add-zsh-hook
load-nvmrc() {
  local nvmrc_path="$(nvm_find_nvmrc)"
  if [ -n "$nvmrc_path" ]; then
    local nvmrc_node_version=$(nvm version "$(cat "${nvmrc_path}")")
    if [ "$nvmrc_node_version" = "N/A" ]; then
      nvm install
    elif [ "$nvmrc_node_version" != "$(nvm version)" ]; then
      nvm use
    fi
  fi
}
add-zsh-hook chpwd load-nvmrc
```

### tmux — Layouts automatiques pour les projets

```bash
# ~/.tmux.conf — configuration optimisée pour le développement
set -g default-terminal "screen-256color"
set -g mouse on
set -g base-index 1
set -g pane-base-index 1

# Raccourcis préfixe modifié (Ctrl+A plus accessible que Ctrl+B)
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# Navigation entre panes avec Alt+flèches
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# Reload config
bind r source-file ~/.tmux.conf \; display "Config rechargée!"

# Barre de statut
set -g status-bg colour235
set -g status-fg colour136
set -g status-left "#[fg=colour28,bold]#S "
set -g status-right "#[fg=colour136]%d %b %H:%M"
```

```yaml
# ~/.config/tmuxinator/myproject.yml
name: myproject
root: ~/projects/my-app

windows:
  - editor:
      layout: main-vertical
      panes:
        - nvim .
        - git log --oneline -20

  - dev:
      layout: even-horizontal
      panes:
        - pnpm dev
        - pnpm --filter=api dev

  - terminal:
      panes:
        - ""
```

```bash
# Lancer le layout du projet
tmuxinator start myproject

# Ou avec tmux-sessionizer (fzf)
tmux-sessionizer ~/projects/my-app
```

## Dotfiles avec Chezmoi

```bash
# Initialisation de Chezmoi
chezmoi init
chezmoi add ~/.zshrc
chezmoi add ~/.gitconfig
chezmoi add ~/.config/nvim/init.lua

# Pousser vers GitHub
chezmoi cd
git add . && git commit -m "feat: initial dotfiles"
git push

# Restaurer sur une nouvelle machine
chezmoi init --apply https://github.com/username/dotfiles.git
```

```
# ~/.local/share/chezmoi/.chezmoitemplates/zshrc.tmpl
# Configuration générée par Chezmoi — NE PAS ÉDITER DIRECTEMENT

{{ if eq .chezmoi.hostname "work-macbook" }}
# Configuration bureau
export CORPORATE_PROXY="http://proxy.company.com:3128"
export npm_config_proxy=$CORPORATE_PROXY
{{ else }}
# Configuration personnelle
alias vpn="sudo openfortivpn vpn.company.com:443"
{{ end }}

# Configuration commune à toutes les machines
export EDITOR="nvim"
export PATH="$HOME/.local/bin:$PATH"
```

```json
// ~/.local/share/chezmoi/.chezmoidata.json
{
  "email": "pierre@company.com",
  "gitHubUsername": "pierreolivier",
  "defaultEditor": "nvim",
  "workMachine": true
}
```

## Git Hooks avec Husky

### Configuration complète des hooks

```bash
# Installation
pnpm add -D husky lint-staged @commitlint/cli @commitlint/config-conventional

# Initialisation
npx husky init
```

```bash
# .husky/pre-commit
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Linting et formatting des fichiers staged
npx lint-staged

# Vérification des types TypeScript (rapide, sans emit)
npx tsc --noEmit --incremental
```

```bash
# .husky/commit-msg
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx --no -- commitlint --edit "$1"
```

```bash
# .husky/pre-push
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Tests avant le push (seulement les fichiers modifiés)
npx nx affected --target=test --base=origin/main
```

```bash
# .husky/prepare-commit-msg
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Ajouter automatiquement le numéro de ticket depuis le nom de branche
BRANCH=$(git symbolic-ref --short HEAD)
TICKET=$(echo "$BRANCH" | grep -oE '[A-Z]+-[0-9]+' | head -1)

if [ -n "$TICKET" ]; then
  COMMIT_FILE="$1"
  CURRENT_MSG=$(cat "$COMMIT_FILE")
  # Ajouter le ticket seulement s'il n'est pas déjà présent
  if ! grep -q "$TICKET" "$COMMIT_FILE"; then
    echo "$CURRENT_MSG ($TICKET)" > "$COMMIT_FILE"
  fi
fi
```

```json
// .lintstagedrc.json
{
  "*.{ts,tsx}": [
    "eslint --fix --max-warnings=0",
    "prettier --write"
  ],
  "*.{js,jsx}": [
    "eslint --fix",
    "prettier --write"
  ],
  "*.{json,yaml,yml,md}": [
    "prettier --write"
  ],
  "*.css": [
    "stylelint --fix",
    "prettier --write"
  ]
}
```

## Commitizen et Conventional Commits

```json
// .czrc
{
  "path": "cz-conventional-changelog"
}
```

```javascript
// commitlint.config.cjs — règles Conventional Commits
module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [
      2,
      "always",
      [
        "feat",     // nouvelle fonctionnalité
        "fix",      // correction de bug
        "docs",     // documentation
        "style",    // formatage (pas de changement de logique)
        "refactor", // refactorisation
        "perf",     // amélioration de performance
        "test",     // ajout ou modification de tests
        "chore",    // maintenance
        "ci",       // intégration continue
        "revert",   // annulation d'un commit
      ],
    ],
    "subject-max-length": [2, "always", 72],
    "body-max-line-length": [2, "always", 100],
    "scope-case": [2, "always", "kebab-case"],
  },
};
```

## Scripts npm et Lifecycle Hooks

```json
// package.json — scripts avancés
{
  "scripts": {
    "preinstall": "npx only-allow pnpm",
    "prepare": "husky",
    "dev": "concurrently --names 'web,api,worker' -c 'cyan,green,yellow' 'pnpm --filter=web dev' 'pnpm --filter=api dev' 'pnpm --filter=worker dev'",
    "build": "turbo run build",
    "build:analyze": "ANALYZE=true pnpm run build",
    "test": "turbo run test",
    "test:watch": "vitest --workspace vitest.workspace.ts",
    "lint": "turbo run lint",
    "type-check": "tsc --noEmit",
    "clean": "turbo run clean && find . -name 'node_modules' -type d -prune -exec rm -rf '{}' +",
    "release": "changeset publish",
    "version": "changeset version && pnpm install --frozen-lockfile=false"
  }
}
```

```bash
# cross-env pour la compatibilité Windows/Mac/Linux
# pnpm add -D cross-env concurrently

"scripts": {
  "build:prod": "cross-env NODE_ENV=production NODE_OPTIONS='--max-old-space-size=4096' turbo run build",
  "test:ci": "cross-env CI=true vitest run --reporter=junit --outputFile=test-results/junit.xml"
}
```

## GitHub Actions Custom Actions

### JavaScript action vs Docker action

```yaml
# .github/actions/notify-slack/action.yml — JavaScript action
name: "Notify Slack"
description: "Envoie une notification Slack avec le résultat du déploiement"
inputs:
  webhook-url:
    description: "URL du webhook Slack"
    required: true
  status:
    description: "Statut du déploiement (success|failure|cancelled)"
    required: true
  environment:
    description: "Environnement déployé"
    required: false
    default: "staging"
outputs:
  message-ts:
    description: "Timestamp du message Slack envoyé"

runs:
  using: "node20"
  main: "dist/index.js"
```

```typescript
// .github/actions/notify-slack/src/index.ts
import * as core from "@actions/core";
import * as github from "@actions/github";

async function run() {
  try {
    const webhookUrl = core.getInput("webhook-url", { required: true });
    const status = core.getInput("status");
    const environment = core.getInput("environment");

    const { context } = github;
    const color = { success: "#36a64f", failure: "#cc0000", cancelled: "#808080" }[status] ?? "#808080";

    const payload = {
      attachments: [
        {
          color,
          title: `Déploiement ${status} — ${environment}`,
          fields: [
            { title: "Repo", value: context.repo.repo, short: true },
            { title: "Branch", value: context.ref.replace("refs/heads/", ""), short: true },
            { title: "Commit", value: context.sha.substring(0, 7), short: true },
            { title: "Auteur", value: context.actor, short: true },
          ],
          footer: `GitHub Actions | ${new Date().toISOString()}`,
        },
      ],
    };

    const response = await fetch(webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = (await response.json()) as { ts: string };
    core.setOutput("message-ts", data.ts);
    core.info("Notification Slack envoyée avec succès");
  } catch (error) {
    core.setFailed(`Erreur lors de l'envoi Slack: ${(error as Error).message}`);
  }
}

run();
```

### Action composite (sans compilation)

```yaml
# .github/actions/setup-project/action.yml — Action composite
name: "Setup Project"
description: "Installe les dépendances avec cache pnpm"
inputs:
  node-version:
    description: "Version de Node.js"
    default: "20"

runs:
  using: "composite"
  steps:
    - uses: pnpm/action-setup@v3
      with:
        version: 9

    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: "pnpm"

    - name: Get pnpm store directory
      shell: bash
      run: echo "STORE_PATH=$(pnpm store path --silent)" >> $GITHUB_ENV

    - uses: actions/cache@v4
      with:
        path: ${{ env.STORE_PATH }}
        key: ${{ runner.os }}-pnpm-${{ hashFiles('**/pnpm-lock.yaml') }}

    - name: Install dependencies
      shell: bash
      run: pnpm install --frozen-lockfile
```

```yaml
# Utilisation dans un workflow
- name: Setup
  uses: ./.github/actions/setup-project
  with:
    node-version: "20"
```
