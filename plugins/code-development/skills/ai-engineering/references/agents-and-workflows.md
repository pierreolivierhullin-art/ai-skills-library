# AI Agents & Workflows — Agent Design, Tool Use, Multi-Agent Orchestration, Memory, Guardrails

## Overview

Ce document de référence couvre la conception et l'implémentation d'agents IA en production : patterns architecturaux (ReAct, Plan-and-Execute, Reflexion), tool use et function calling, orchestration multi-agents, gestion de la mémoire, planification et raisonnement, guardrails de sécurité, évaluation des agents et comparaison des frameworks. Utiliser ce guide pour toute décision de conception d'agent IA.

---

## 1. Agent Architecture Patterns

Un agent IA utilise un LLM comme moteur de raisonnement pour décider dynamiquement quelles actions entreprendre, dans quel ordre, en fonction d'un objectif et des observations obtenues. Contrairement à un pipeline déterministe, l'agent prend des décisions à runtime.

### Pattern 1 — ReAct (Reasoning + Acting)

Le LLM alterne raisonnement explicite et actions concrètes dans une boucle itérative :

```
Entrée utilisateur → THOUGHT → ACTION (appel outil) → OBSERVATION (résultat)
    → THOUGHT → ACTION → OBSERVATION → ... → ANSWER (réponse finale)
```

**Forces** : flexible, adaptatif, raisonnement traçable. **Faiblesses** : peut boucler, coût élevé en tokens sur les tâches longues.

### Pattern 2 — Plan-and-Execute

Le LLM génère un plan complet, puis l'exécute séquentiellement. Le plan peut être révisé si une étape échoue :

```
Entrée → PLANIFICATION (étapes 1-5) → EXÉCUTION SÉQUENTIELLE
    +-- Étape OK → continuer
    +-- Étape ÉCHEC → RE-PLANIFICATION → reprendre
```

**Forces** : plan vérifiable avant exécution. **Faiblesses** : latence initiale, surcoût si le plan est révisé fréquemment.

### Pattern 3 — Reflexion

Le LLM évalue sa propre sortie et itère pour l'améliorer via une boucle d'auto-critique :

```
Entrée → GÉNÉRATION → AUTO-ÉVALUATION
    +-- Score insuffisant → RÉVISION → retour à GÉNÉRATION
    +-- Score suffisant → RÉPONSE FINALE
```

### Pattern 4 — Tool-Use Agent

Pattern minimaliste centré sur la sélection et l'appel d'outils. Le raisonnement est implicite dans le choix de l'outil et de ses paramètres. Boucle : sélection outil → exécution → interprétation → besoin d'un autre outil ? → boucler ou répondre.

### Comparison Table

| Pattern | Complexité | Coût tokens | Traçabilité | Cas d'usage idéal |
|---|---|---|---|---|
| **ReAct** | Moyenne | Moyen-élevé | Excellente | Tâches exploratoires, debugging, recherche |
| **Plan-and-Execute** | Élevée | Élevé | Bonne | Tâches multi-étapes prévisibles, migrations |
| **Reflexion** | Élevée | Très élevé | Excellente | Génération de code, rédaction, analyse complexe |
| **Tool-Use** | Faible | Faible-moyen | Moyenne | Assistants avec outils bien définis |
| **Human-in-the-Loop** | Variable | Variable | Maximale | Actions irréversibles, décisions critiques |

---

## 2. Tool Use & Function Calling

### Bonnes pratiques de définition d'outils

| Principe | Description | Exemple |
|---|---|---|
| **Nom descriptif** | Le nom indique clairement l'action | `search_customers` et non `query1` |
| **Description précise** | Quand et pourquoi utiliser cet outil | "Rechercher des clients par nom, email ou ID" |
| **Paramètres typés** | JSON schema strict avec types et contraintes | `{"name": {"type": "string", "description": "..."}}` |
| **Valeurs par défaut** | Defaults sensibles pour les paramètres optionnels | `limit: 10`, `sort: "created_desc"` |
| **Instructions négatives** | Préciser quand NE PAS utiliser l'outil | "Ne PAS utiliser pour les devis" |
| **Erreurs explicites** | Messages d'erreur clairs et actionnables | "Client ID 123 introuvable. IDs valides : 100-999" |

### Sélection d'outils par le LLM

- **Limiter le nombre d'outils** : au-delà de 15-20, la précision de sélection diminue. Regrouper par catégorie ou utiliser un routing agent.
- **Descriptions mutuellement exclusives** : périmètre clair et non-chevauchant pour chaque outil.
- **Tool routing** : pour 50+ outils, utiliser un premier LLM qui sélectionne la catégorie, puis un second qui choisit l'outil.

### Gestion des erreurs

Chaque appel d'outil doit suivre le flux : validation des paramètres → exécution (avec gestion timeout, autorisation, erreur métier) → post-traitement (troncation des résultats volumineux, formatage pour le LLM). Toujours retourner des erreurs descriptives et actionnables au LLM plutôt que des codes d'erreur bruts.

### Sandboxing et permissions

| Niveau | Description | Implémentation |
|---|---|---|
| **Read-only** | L'outil ne peut que lire des données | Séparer outils de lecture et d'écriture |
| **Confirmation requise** | Validation humaine avant exécution | Flag `requires_confirmation: true` |
| **Scope limité** | Accès restreint à un sous-ensemble | Filtrage par tenant, utilisateur, rôle |
| **Rate limiting** | Limiter les appels par intervalle | Max 10 appels/minute par outil |
| **Sandbox d'exécution** | Environnement isolé | Containers, WebAssembly, E2B, Modal |

---

## 3. Multi-Agent Systems

### Quand utiliser un système multi-agent

```
La tâche nécessite-t-elle des compétences hétérogènes ?
+-- Non → Agent unique suffit
+-- Oui → Séparation des responsabilités requise ?
    +-- Non → Agent unique avec plusieurs outils
    +-- Oui → Sous-tâches indépendantes ?
        +-- Oui → Agents parallèles avec agrégation
        +-- Non → Pipeline d'agents ou orchestrateur (supervisor)
```

### Patterns d'orchestration

**Supervisor** : un agent coordonne des agents spécialisés. Il décide quel agent appeler, dans quel ordre, et agrège les résultats. Le superviseur est un agent dont les "outils" sont les autres agents.

**Hierarchical** : extension du supervisor avec plusieurs niveaux. Un superviseur principal délègue à des superviseurs intermédiaires. Limiter à 2-3 niveaux pour éviter la perte de contexte.

**Swarm / Collaborative** : agents peer-to-peer sans superviseur central. Haute résilience mais debugging difficile.

**Handoff** : un agent transfère le contrôle à un autre selon le contexte (triage → spécialiste). Implémenter un protocole standardisé : raison du transfert, contexte résumé, objectif restant.

| Aspect | Supervisor | Hierarchical | Swarm |
|---|---|---|---|
| **Coordination** | Centralisée | Hiérarchique | Décentralisée |
| **Complexité** | Moyenne | Élevée | Très élevée |
| **Tolérance aux pannes** | Point unique de défaillance | Résilience partielle | Haute résilience |
| **Debugging** | Facile (flux central) | Modéré | Difficile (flux distribué) |

---

## 4. Agent Memory

| Type | Portée | Durée | Implémentation | Analogie humaine |
|---|---|---|---|---|
| **Short-term** | Conversation en cours | Session | Context window du LLM | Mémoire de travail |
| **Working memory** | Tâche en cours | Tâche | Scratchpad, variables d'état | Notes sur un post-it |
| **Long-term** | Cross-sessions | Persistante | Vector store, base de données | Mémoire à long terme |
| **Episodic** | Événements passés | Persistante | Log structuré | Souvenirs d'expériences |
| **Semantic** | Connaissances générales | Persistante | Knowledge graph, embeddings | Connaissances acquises |

### Short-term : context window management

- **Sliding window** : conserver les N derniers messages. Simple mais perd le contexte ancien.
- **Summarization** : résumer les messages anciens en début de contexte. Préserve le contexte clé, coût d'un appel LLM supplémentaire.
- **Token budget** : allouer par catégorie (system prompt 20%, historique 40%, outils 20%, réponse 20%).

### Working Memory : scratchpad

L'agent maintient un état structuré pendant l'exécution : objectif, plan, étape courante, résultats intermédiaires, blockers. Injecter ce scratchpad dans le context window à chaque itération et mettre à jour après chaque action.

### Long-term : vector store

Stocker informations persistantes (résumés de conversations, préférences utilisateur, connaissances acquises) dans un vector store. À chaque fin de session, extraire et embedder les informations clés. Au début de chaque session, retriever les mémoires pertinentes.

### Episodic Memory

Enregistrer les trajectoires complètes (séquence d'actions, résultats, diagnostic, leçons) pour améliorer les performances futures. Retriever les épisodes similaires lors de tâches analogues.

---

## 5. Planning & Reasoning

### Chain-of-Thought (CoT)

Forcer le LLM à expliciter son raisonnement étape par étape. Inclure dans le system prompt : "Avant de choisir une action, raisonne étape par étape : objectif, informations disponibles, informations manquantes, outil approprié, paramètres."

### Tree-of-Thought (ToT)

Explorer plusieurs chemins de raisonnement en parallèle, scorer chaque branche, sélectionner la meilleure et approfondir. Coût multiplicatif (N branches x M profondeur). Réserver aux tâches à haute valeur.

### Step-back Prompting

Avant de résoudre un problème spécifique, formuler le problème de manière plus abstraite, puis appliquer les principes généraux au cas concret.

### Self-Consistency

Générer N réponses indépendantes (temperature > 0), sélectionner la réponse majoritaire. Réduit les erreurs aléatoires.

| Technique | Coût LLM | Amélioration qualité | Cas d'usage |
|---|---|---|---|
| **Chain-of-Thought** | 1x (+ tokens raisonnement) | Significative | Raisonnement logique, mathématiques |
| **Tree-of-Thought** | Nx (N branches) | Forte | Planification, stratégie, puzzles |
| **Step-back** | 2x | Modérée | Problèmes nécessitant une vue d'ensemble |
| **Self-Consistency** | Nx (N échantillons) | Modérée | Classification, extraction |
| **Decomposition** | Variable | Forte | Tâches longues et complexes |

### Decomposition Strategies

- **Fonctionnelle** : découper par fonction (analyser, transformer, valider).
- **Par données** : traiter chaque unité séparément (fichier par fichier).
- **Temporelle** : découper par phase (planifier, exécuter, vérifier).
- **Hiérarchique** : découper récursivement jusqu'aux tâches atomiques.

---

## 6. Guardrails & Safety

### Architecture en couches

```
ENTRÉE → [GUARDRAIL INPUT] → [LLM] → [GUARDRAIL OUTPUT]
    → [GUARDRAIL ACTION] → [EXÉCUTION OUTIL] → [GUARDRAIL RESULT] → RÉPONSE
```

### Input Validation

| Vérification | Description | Implémentation |
|---|---|---|
| **Prompt injection** | Détecter les manipulations du system prompt | Classifier (LLM-as-judge ou modèle dédié) |
| **Longueur maximale** | Limiter la taille de l'input | Truncation avec avertissement |
| **Contenu inapproprié** | Filtrer les inputs dangereux | API de modération |
| **Format attendu** | Valider le format de l'input | Validation regex ou schema |

### Output Validation

| Vérification | Description | Implémentation |
|---|---|---|
| **Format structuré** | Valider le respect du JSON schema | Pydantic, Zod, JSON Schema validation |
| **Hallucination check** | Vérifier les faits contre le contexte | Cross-reference avec sources RAG |
| **PII detection** | Détecter les données personnelles | Regex patterns + NER |
| **Cohérence** | Vérifier la cohérence avec les outputs précédents | Comparaison sémantique |

### Action Validation

- **Allowlist** : seuls les outils explicitement autorisés sont appelables.
- **Confirmation humaine** : validation pour actions destructives (DELETE, envoi email, paiement).
- **Dry-run** : simulation avant exécution réelle.
- **Scope check** : vérifier que l'action reste dans le périmètre autorisé.

### Loop Detection et limites

| Limite | Valeur recommandée | Raison |
|---|---|---|
| **Max iterations** | 15-25 par tâche | Empêcher les boucles infinies |
| **Max tool calls** | 50 par session | Limiter coût et temps |
| **Timeout** | 5-10 min par tâche | Éviter les tâches bloquées |
| **Identical action repeat** | Max 3 consécutives | Détecter les boucles |
| **Max cost** | Seuil en dollars par tâche | Circuit breaker financier |

---

## 7. Agent Evaluation

### Métriques clés

| Métrique | Calcul | Cible |
|---|---|---|
| **Task completion rate** | Tâches réussies / total | > 85% |
| **Tool selection accuracy** | Outils corrects / total appels | > 90% |
| **Tool call efficiency** | Appels réels / appels optimaux | < 1.5x optimal |
| **Cost per task** | Total tokens x prix / tâches | Variable |
| **Latency** | Timestamp fin - début | < 60s (tâches simples) |
| **Error recovery rate** | Récupérations / erreurs | > 70% |
| **Safety violation rate** | Violations / total tâches | < 1% |
| **Human escalation rate** | Escalades / total tâches | 5-15% |

### Framework d'évaluation

```
1. Créer un dataset de test (50-100 tâches représentatives)
   +-- Cas nominaux, edge cases, cas adverses
   +-- Résultats attendus (actions + output final)
2. Définir critères de succès par tâche
   +-- Complétude, exactitude, efficacité, coût
3. Exécuter en batch avec logging détaillé
4. Analyser les trajectoires échouées et itérer
```

### Benchmarking

| Dimension | Métriques | Outil de mesure |
|---|---|---|
| **Qualité** | Task completion, accuracy, F1 | Evals custom, SWE-bench, GAIA |
| **Efficacité** | Steps-to-completion, token efficiency | Logging custom |
| **Coût** | Cost per task, cost per success | Billing API + logging |
| **Sécurité** | Injection resistance, PII leak rate | Red-teaming datasets |
| **Préférence humaine** | Win rate vs baseline | Human eval panels |

---

## 8. Frameworks Comparison

### Comparaison détaillée (2025-2026)

| Feature | LangGraph | CrewAI | AutoGen | Claude Code SDK | Semantic Kernel | Haystack |
|---|---|---|---|---|---|---|
| **Approche** | Graph de workflow | Rôles et équipes | Conversations multi-agents | Agent natif Anthropic | Plugins et planificateur | Pipelines composables |
| **Orchestration** | DAG / cycles | Supervisor | Conversations | Boucle agentique | Planificateur IA | Pipeline linéaire |
| **Multi-agent** | Natif (graph) | Natif (crew) | Natif (groupchat) | Via orchestration externe | Via plugins | Via composants |
| **Memory** | Checkpoints, stores | Natif (short/long) | Natif | Context window | Plugin memory | Document stores |
| **Tool use** | Natif | Natif | Natif | Natif (MCP) | Natif (plugins) | Natif (components) |
| **Human-in-the-loop** | Interrupts, breakpoints | Callback | Terminaison conditionnelle | Natif | Hooks | Optionnel |
| **Langage** | Python | Python | Python / .NET | Python / TypeScript | Python / C# / Java | Python |
| **Cas d'usage idéal** | Workflows complexes avec état | Équipes d'agents rôlés | Agents conversationnels | Coding agents, CLI tools | Enterprise .NET/Java | Pipelines NLP/RAG |

### Arbre de décision

```
Quel est le cas d'usage principal ?
+-- Workflow complexe avec état et cycles → LangGraph
+-- Équipe d'agents avec rôles définis → CrewAI
+-- Agents conversationnels multi-parties → AutoGen
+-- Agent de coding ou CLI tool → Claude Code SDK
+-- Application enterprise .NET/Java → Semantic Kernel
+-- Pipeline NLP/RAG → Haystack
+-- Prototype rapide, flexibilité maximale → API directe (Anthropic/OpenAI SDK)
```

---

## 9. State of the Art (2025-2026)

### Computer Use Agents

Les agents capables d'interagir avec des interfaces graphiques (clic, frappe, navigation) deviennent opérationnels : Anthropic Computer Use, OpenAI Operator, browser-use, LaVague. **Limites** : latence élevée, fragilité face aux changements d'interface. Réserver aux tâches où aucune API n'est disponible.

### Coding Agents

Cas d'usage le plus mature : Claude Code, Cursor, Devin, Codex, Windsurf. Compréhension du code, navigation codebase, édition, exécution de commandes, interaction avec git/tests/linters. **Tendance** : intégration IDE native, résolution d'issues GitHub de bout en bout, extensibilité via MCP.

### Model Context Protocol (MCP)

Protocole standardisé par Anthropic pour connecter LLMs à des sources de données et outils externes via une interface uniforme (resources, tools, prompts). Adopter MCP pour toute nouvelle intégration d'outil.

| Composant MCP | Rôle | Exemple |
|---|---|---|
| **Server** | Expose outils et ressources | PostgreSQL, GitHub, Slack |
| **Client** | Consomme les outils exposés | Claude Code, IDE avec support MCP |
| **Tool** | Action exécutable | `query_database`, `create_issue` |
| **Resource** | Donnée consultable | Schéma de BDD, fichier de config |
| **Prompt** | Template de prompt réutilisable | Prompt d'analyse de code |

### Agent-to-Agent Communication

Protocoles émergents (A2A de Google) pour la communication inter-agents standardisée. Un agent peut déléguer des sous-tâches à un autre sans partager le même runtime. Encore en phase exploratoire.

### Autonomous Agents Safety

Enjeux principaux : **alignment** (l'agent poursuit l'objectif de l'utilisateur), **containment** (limiter les capacités), **monitoring** (observation temps réel), **kill switch** (arrêt immédiat), **audit trail** (traçabilité complète). Pour tout agent en production, implémenter les guardrails de la section 6 comme minimum non négociable.

---

## 10. Checklist de conception d'agent

| Phase | Vérification | Statut |
|---|---|---|
| **Design** | Objectif de l'agent clairement défini | ___ |
| **Design** | Pattern architectural choisi et justifié | ___ |
| **Design** | Liste des outils avec schémas de paramètres | ___ |
| **Design** | Stratégie de mémoire définie (short/long term) | ___ |
| **Safety** | Guardrails input configurés (injection, contenu) | ___ |
| **Safety** | Guardrails output configurés (PII, hallucination) | ___ |
| **Safety** | Guardrails action configurés (confirmation, allowlist) | ___ |
| **Safety** | Limites définies (max iterations, timeout, coût) | ___ |
| **Eval** | Suite d'évaluation créée (50+ cas de test) | ___ |
| **Eval** | Métriques de succès et seuils fixés | ___ |
| **Production** | Observabilité configurée (traces, métriques, coûts) | ___ |
| **Production** | Monitoring, alertes et kill switch en place | ___ |
