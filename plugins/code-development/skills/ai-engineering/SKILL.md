---
name: ai-engineering
description: This skill should be used when the user asks about "AI engineering", "LLM integration", "RAG", "retrieval augmented generation", "embeddings", "vector database", "fine-tuning", "prompt engineering for developers", "AI agents", "tool use", "function calling", "multi-agent systems", "LLM API", "model serving", "AI evaluation", "evals", "LLM observability", "AI cost optimization", "ingénierie IA", "intégration LLM", "agents IA", "orchestration IA", "MLOps", "model deployment", "AI pipeline", "semantic search", "recherche sémantique", "chunking strategy", "AI middleware", "structured output", "JSON mode", "streaming LLM", "AI guardrails", "prompt caching", "model routing", "AI gateway", "inference optimization", discusses building AI-powered features, or needs guidance on integrating LLMs into applications, designing AI agents, or managing AI infrastructure.
version: 1.0.0
last_updated: 2026-02
---

# AI Engineering — LLM Integration, Agents & ML Operations

## Overview

Ce skill couvre l'ensemble de l'ingénierie IA appliquée au développement logiciel : intégration de LLMs dans les applications, conception de systèmes RAG, développement d'agents IA, fine-tuning, évaluation, déploiement et optimisation des coûts. Il s'adresse aux développeurs et architectes qui construisent des features IA en production, pas aux data scientists qui entraînent des modèles from scratch. Appliquer systématiquement les principes décrits ici pour structurer chaque décision d'ingénierie IA, en privilégiant la fiabilité (un système IA non évaluable est un système non déployable), l'itération (commencer simple, mesurer, complexifier si nécessaire) et l'optimisation coût/qualité (le modèle le plus cher n'est pas toujours le meilleur choix). L'AI engineering est une discipline d'ingénierie, pas de magie : chaque composant doit être testé, mesuré et monitoré comme n'importe quel autre composant logiciel.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Intégration de LLMs** : appels API (OpenAI, Anthropic, Google, open source), gestion des prompts, structured output, streaming, gestion des erreurs et retries, prompt caching, model routing.
- **Systèmes RAG** : conception de pipelines RAG (ingestion, chunking, embedding, retrieval, generation), choix de vector databases, stratégies de chunking, re-ranking, évaluation de la qualité RAG.
- **Agents IA** : conception d'agents avec tool use/function calling, orchestration multi-agents, planification, mémoire, guardrails, boucles de rétroaction.
- **Fine-tuning et adaptation** : quand fine-tuner vs prompt engineering vs RAG, préparation des datasets, techniques de fine-tuning (LoRA, QLoRA), évaluation post-fine-tuning.
- **Évaluation et qualité** : conception d'evals (automated, human-in-the-loop, LLM-as-judge), métriques de qualité, regression testing, benchmarking.
- **Infrastructure et MLOps** : model serving, scaling d'inférence, monitoring en production, gestion des coûts, CI/CD pour les pipelines IA.
- **Optimisation** : réduction de latence, optimisation des coûts (model routing, caching, batching), gestion des tokens, quantization.

## Core Principles

### Principle 1 — Start Simple, Complexify with Evidence

Ne jamais commencer par l'architecture la plus complexe. La hiérarchie d'implémentation : (1) prompt engineering sur un modèle frontier, (2) few-shot prompting avec exemples, (3) RAG si le contexte externe est nécessaire, (4) fine-tuning si le comportement spécifique ne peut être obtenu autrement, (5) agents si l'autonomie est requise. Chaque niveau de complexité doit être justifié par des mesures montrant que le niveau précédent est insuffisant.

### Principle 2 — Evals Before Everything

Ne jamais déployer un système IA sans suite d'évaluation. Définir les evals avant d'écrire le code : quels cas de test, quelles métriques, quels seuils d'acceptation. Les evals sont l'équivalent des tests unitaires pour l'IA : sans eux, chaque changement de prompt, de modèle ou de pipeline est un pari aveugle. Minimum : 50-100 cas de test couvrant les cas nominaux, les edge cases et les cas adverses.

### Principle 3 — Cost-Aware Engineering

Chaque appel LLM a un coût. Concevoir avec la conscience du coût dès le départ : choisir le modèle approprié par tâche (pas toujours le plus puissant), implémenter le prompt caching, utiliser le batching quand possible, monitorer le coût par requête et par feature. Un système IA qui fonctionne bien mais coûte 10x le budget n'est pas un système viable.

### Principle 4 — Determinism Where Possible

Les LLMs sont intrinsèquement non-déterministes. Maximiser le déterminisme partout où c'est possible : structured output (JSON schema), temperature 0 pour les tâches factuelles, validation de la sortie, retry avec parsing alternatif. Accepter le non-déterminisme uniquement là où il apporte de la valeur (créativité, diversité de réponses).

### Principle 5 — Defense in Depth for AI

Un LLM peut halluciner, être injecté, ou produire du contenu inapproprié. Appliquer la défense en profondeur : validation des entrées (input guardrails), validation des sorties (output guardrails), grounding via RAG ou vérification factuelle, monitoring des anomalies, circuit breaker si la qualité se dégrade. Ne jamais exposer un LLM directement à l'utilisateur sans couche de validation.

### Principle 6 — Observability is Non-Negotiable

Instrumenter chaque appel LLM : prompt envoyé, réponse reçue, latence, tokens consommés, coût, score de qualité si disponible. Utiliser des outils d'observabilité IA (Langfuse, Langsmith, Helicone, Braintrust) pour tracer les pipelines complets. Sans observabilité, le debugging est impossible et l'optimisation est aveugle.

## Key Frameworks & Methods

### LLM Integration Decision Tree

```
1. Quelle est la tâche ?
   +-- Classification, extraction, transformation structurée
   |   --> Prompt engineering + structured output (JSON mode)
   +-- Question-réponse sur des documents spécifiques
   |   --> RAG (retrieval + generation)
   +-- Tâche nécessitant un style/ton/format très spécifique
   |   --> Fine-tuning ou few-shot prompting
   +-- Tâche multi-étapes nécessitant des actions
   |   --> Agent avec tool use
   +-- Tâche conversationnelle avec mémoire
       --> Chat avec context window management
```

### RAG Architecture Components

| Composant | Options | Critères de choix |
|---|---|---|
| **Document Loader** | LangChain, LlamaIndex, Unstructured | Types de documents (PDF, HTML, code) |
| **Chunking** | Fixed-size, recursive, semantic, document-aware | Taille des documents, structure, coût |
| **Embedding Model** | OpenAI text-embedding-3, Cohere embed-v3, open source (BGE, E5) | Qualité, coût, latence, multilingue |
| **Vector DB** | Pinecone, Weaviate, Qdrant, pgvector, ChromaDB | Scale, hosted vs self-hosted, filtering |
| **Retrieval** | Similarity search, MMR, hybrid (dense + sparse), re-ranking | Précision requise, diversité |
| **Re-ranker** | Cohere Rerank, cross-encoder, ColBERT | Qualité vs latence trade-off |
| **Generator** | Claude, GPT-4, Gemini, Llama, Mistral | Qualité, coût, context window |

### Chunking Strategy Comparison

| Stratégie | Taille typique | Forces | Faiblesses | Quand l'utiliser |
|---|---|---|---|---|
| **Fixed-size** | 512-1024 tokens | Simple, prédictible | Coupe le sens | Texte homogène, démarrage rapide |
| **Recursive** | 256-1024 tokens | Respecte la structure | Complexité moyenne | Texte structuré (Markdown, HTML) |
| **Semantic** | Variable | Préserve le sens | Coûteux (embedding) | Documents longs, haute qualité requise |
| **Document-aware** | Variable | Structure native | Spécifique au format | PDF structurés, code, tables |
| **Agentic** | Variable | Adaptatif, contextuel | Complexe, coûteux | Corpus hétérogène, haute exigence |

### Agent Architecture Patterns

```
Pattern 1 — ReAct (Reasoning + Acting)
+-- Le LLM alterne raisonnement et actions
+-- Boucle : Thought → Action → Observation → Thought → ...
+-- Use case : tâches exploratoires, recherche, debugging

Pattern 2 — Plan-and-Execute
+-- Le LLM planifie d'abord, puis exécute séquentiellement
+-- Avantage : plan révisable avant exécution
+-- Use case : tâches complexes multi-étapes

Pattern 3 — Multi-Agent Orchestration
+-- Plusieurs agents spécialisés collaborent
+-- Patterns : supervisor, hierarchical, swarm
+-- Use case : workflows complexes, séparation des responsabilités

Pattern 4 — Human-in-the-Loop
+-- L'agent demande une validation humaine aux étapes critiques
+-- Mandatory pour : actions irréversibles, décisions à fort impact
+-- Use case : workflows business, actions sur des systèmes externes
```

### Model Selection Matrix

| Critère | Frontier (Claude Opus, GPT-4o) | Mid-tier (Claude Sonnet, GPT-4o-mini) | Small (Haiku, Gemini Flash) | Open Source (Llama, Mistral) |
|---|---|---|---|---|
| **Qualité raisonnement** | Excellente | Très bonne | Bonne | Variable |
| **Coût / 1M tokens** | 15-75$ | 3-15$ | 0.25-1$ | Infra only |
| **Latence** | Haute | Moyenne | Faible | Variable (self-hosted) |
| **Context window** | 128K-200K | 128K-200K | 128K-200K | 8K-128K |
| **Idéal pour** | Tâches complexes, coding, analyse | Production générale | Classification, extraction, routing | Privacy, compliance, edge |

### Evaluation Framework

| Type d'eval | Méthode | Quand l'utiliser | Coût |
|---|---|---|---|
| **Exact match** | Output == expected | Extraction structurée, classification | Quasi nul |
| **Fuzzy match** | Similarity score, BLEU, ROUGE | Génération de texte prévisible | Faible |
| **LLM-as-Judge** | Un LLM évalue la qualité de l'output | Tâches ouvertes, qualité subjective | Modéré |
| **Human eval** | Annotateurs humains | Gold standard, calibration initiale | Élevé |
| **A/B testing** | Comparaison en production | Validation à l'échelle | Modéré |
| **Regression testing** | Suite de cas de test automatisés | Chaque changement de prompt/modèle | Faible |

## Decision Guide

### RAG vs Fine-tuning vs Prompt Engineering

```
1. Le modèle doit-il accéder à des données spécifiques/privées ?
   +-- Oui → RAG (les données changent) ou Fine-tuning (patterns stables)
   +-- Non → Prompt engineering suffit probablement

2. Le comportement requis est-il un style/format spécifique ?
   +-- Oui → Fine-tuning (si few-shot insuffisant)
   +-- Non → RAG ou prompt engineering

3. Les données changent-elles fréquemment ?
   +-- Oui → RAG (mise à jour sans re-entraînement)
   +-- Non → Fine-tuning ou prompt engineering

4. Budget et timeline ?
   +-- Contraint → Prompt engineering d'abord
   +-- Flexible → Évaluer RAG puis fine-tuning si nécessaire
```

### Quand utiliser des Agents vs des Pipelines

```
1. La tâche nécessite-t-elle des décisions dynamiques ?
   +-- Non (séquence fixe) → Pipeline déterministe
   +-- Oui → Agent

2. Quel niveau d'autonomie est acceptable ?
   +-- Faible (chaque étape validée) → Pipeline + human-in-the-loop
   +-- Modéré (certaines actions autonomes) → Agent avec guardrails
   +-- Élevé (autonomie complète) → Agent + monitoring renforcé

3. Les outils sont-ils bien définis et limités ?
   +-- Oui (< 10 outils) → Agent simple (ReAct)
   +-- Non (outils dynamiques, contexte variable) → Multi-agent
```

## Common Patterns & Anti-Patterns

### Patterns recommandés

- **Prompt Versioning** : versionner chaque prompt comme du code (git, fichiers séparés). Chaque changement de prompt est associé à un run d'evals. Utiliser un registre de prompts (Langfuse, Braintrust) pour tracer les performances par version.
- **Fallback Chain** : implémenter une chaîne de fallback entre modèles (frontier → mid-tier → small → réponse par défaut). Si le modèle principal échoue ou dépasse le timeout, le suivant prend le relais. Réduit la latence perçue et améliore la disponibilité.
- **Semantic Caching** : cacher les réponses par similarité sémantique du prompt, pas par exact match. Réduit les coûts de 30-60% sur les workloads répétitifs. Outils : GPTCache, Redis avec embeddings.
- **Structured Output Validation** : toujours demander un output structuré (JSON schema, Pydantic model) et valider programmatiquement. Retry avec message d'erreur si la validation échoue. Ne jamais parser du texte libre quand un format structuré est possible.

### Anti-patterns critiques

- **Prompt-and-Pray** : envoyer un prompt non testé en production et espérer que ça marche. Chaque prompt doit être évalué sur une suite de tests avant déploiement.
- **Context Window Stuffing** : mettre le maximum de contexte dans le prompt sans stratégie. Au-delà de ~50% de la fenêtre de contexte, la qualité se dégrade ("lost in the middle"). Utiliser le retrieval pour sélectionner le contexte pertinent.
- **Single Model for Everything** : utiliser le même modèle frontier pour toutes les tâches. La classification simple ne nécessite pas Claude Opus. Router chaque tâche vers le modèle approprié (model routing).
- **No Guardrails in Production** : exposer un LLM sans validation des entrées ni des sorties. Risques : prompt injection, hallucinations servies comme faits, contenu inapproprié, fuite de données.
- **Evaluation Afterthought** : construire tout le système puis réfléchir à l'évaluation. Les evals doivent être conçus en premier, avant le code.

## Implementation Workflow

### Phase 1 — Fondations

1. Définir le use case IA précis et les critères de succès mesurables.
2. Concevoir la suite d'evals : cas de test, métriques, seuils d'acceptation.
3. Prototyper avec du prompt engineering sur un modèle frontier (Claude Sonnet ou GPT-4o).
4. Évaluer le prototype sur la suite d'evals. Si les seuils sont atteints → Phase 3.
5. Si insuffisant → évaluer RAG (besoin de données externes) ou fine-tuning (besoin de comportement spécifique).

### Phase 2 — Pipeline IA

6. Concevoir l'architecture du pipeline (RAG, agent, ou pipeline hybride).
7. Implémenter le pipeline avec instrumentation complète (traces, métriques, coûts).
8. Configurer les guardrails : validation input/output, rate limiting, circuit breaker.
9. Évaluer sur la suite d'evals. Itérer sur les prompts, le retrieval ou le fine-tuning.
10. Optimiser : model routing, caching, batching pour atteindre les cibles de coût et latence.

### Phase 3 — Production

11. Déployer avec feature flag et canary release (5% → 25% → 100%).
12. Configurer le monitoring en production : qualité (LLM-as-judge sampling), latence, coût, erreurs.
13. Mettre en place les alertes : dégradation de qualité, explosion de coûts, taux d'erreur anormal.
14. Implémenter le feedback loop : collecte du feedback utilisateur, intégration dans les evals.
15. Documenter les prompts, l'architecture et les décisions dans un AI Decision Record.

### Phase 4 — Optimisation continue

16. Analyser les patterns d'usage en production (quelles requêtes, quels coûts, quelle qualité).
17. Optimiser le model routing : basculer les tâches simples vers des modèles moins chers.
18. Enrichir la suite d'evals avec les cas de production (edge cases découverts, feedbacks négatifs).
19. Évaluer les nouveaux modèles (chaque release) sur la suite d'evals existante.
20. Itérer : chaque amélioration passe par le cycle evals → changement → evals → déploiement.

## Modèle de maturité

### Niveau 1 — Expérimental
- Les LLMs sont utilisés de manière ad-hoc (playgrounds, scripts ponctuels)
- Pas d'evals, pas de monitoring, pas de gestion des coûts
- Les prompts sont écrits dans le code sans versioning
- **Indicateurs** : pas de suite d'evals, coût IA non suivi, pas d'observabilité

### Niveau 2 — Structuré
- Les appels LLM sont encapsulés dans des services avec gestion d'erreurs
- Une suite d'evals basique existe (50+ cas de test)
- Les prompts sont versionnés et les coûts sont monitorés
- **Indicateurs** : evals passent à chaque PR, coût par feature connu, observabilité basique

### Niveau 3 — Production-Grade
- Architecture RAG ou agent en production avec guardrails complets
- Suite d'evals complète (200+ cas) avec regression testing automatisé
- Model routing et caching implémentés, coûts optimisés
- **Indicateurs** : qualité monitorée en temps réel, coût optimisé de 30%+, fallback chain active

### Niveau 4 — Optimisé
- Experimentation continue (A/B testing de prompts et modèles en production)
- Feedback loop automatisé : feedback utilisateur → evals → amélioration
- Multi-model strategy avec routing intelligent par complexité de tâche
- **Indicateurs** : cycle d'amélioration < 1 semaine, coût/qualité ratio optimal, 95%+ de satisfaction

### Niveau 5 — AI-Native
- L'IA est un composant natif de l'architecture, pas un add-on
- Auto-évaluation et auto-optimisation (evals générés automatiquement, model routing adaptatif)
- Contribution à l'écosystème (modèles custom, datasets d'évaluation partagés)
- **Indicateurs** : > 50% des features utilisent de l'IA, coût IA < 5% du revenu, innovation IA continue

## Rythme opérationnel

| Cadence | Activité | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Continue** | Monitoring qualité + coûts en production | AI Engineer on-call | Dashboard temps réel |
| **Hebdomadaire** | Review des evals et des feedbacks utilisateurs | AI Engineering team | Rapport qualité + actions |
| **Bi-mensuel** | Optimisation prompts et model routing | AI Engineer | Prompts améliorés, coûts réduits |
| **Mensuel** | Évaluation des nouveaux modèles disponibles | AI Tech Lead | Benchmark comparatif |
| **Trimestriel** | Revue d'architecture IA et roadmap technique | AI Tech Lead + CTO | ADR mis à jour + plan |
| **À chaque release modèle** | Run complet de la suite d'evals | AI Engineer | Rapport go/no-go migration |

## State of the Art (2025-2026)

L'AI engineering connaît une maturation rapide avec l'industrialisation des pratiques :

- **AI Gateway & Model Router** : les API gateways spécialisées (Portkey, LiteLLM, Martian) routent automatiquement les requêtes vers le modèle optimal (coût/qualité/latence). Le model routing intelligent devient un pattern standard.
- **Agentic AI Frameworks** : les frameworks d'agents (Claude Code SDK, LangGraph, CrewAI, AutoGen) permettent de construire des systèmes multi-agents orchestrés avec guardrails, mémoire et tool use structuré.
- **Structured Output Native** : les providers supportent nativement le JSON schema contraint (Anthropic, OpenAI), éliminant le parsing fragile. Les structured outputs deviennent le mode par défaut pour toute tâche non-conversationnelle.
- **Eval-Driven Development** : les plateformes d'évaluation (Braintrust, Langfuse, Promptfoo) intègrent les evals dans le CI/CD. Chaque PR qui touche un prompt déclenche automatiquement une suite d'evals.
- **Prompt Caching & Prefix Caching** : Anthropic et OpenAI supportent le caching des préfixes de prompt, réduisant les coûts de 50-90% pour les prompts système longs et les contextes RAG récurrents.

## Template actionnable

### AI Decision Record

| Élément | Description | Votre réponse |
|---|---|---|
| **Use case** | Quelle tâche IA ? | ___ |
| **Approche choisie** | Prompt / RAG / Fine-tuning / Agent ? | ___ |
| **Modèle** | Quel modèle et pourquoi ? | ___ |
| **Evals** | Combien de cas de test, quelles métriques ? | ___ |
| **Coût estimé** | Coût par requête et mensuel projeté ? | ___ |
| **Guardrails** | Quelles validations input/output ? | ___ |
| **Fallback** | Que se passe-t-il si le LLM échoue ? | ___ |
| **Monitoring** | Quelles métriques en production ? | ___ |
| **Critères de succès** | Quels seuils pour considérer le déploiement réussi ? | ___ |

## Prompts types

- "Comment intégrer un LLM dans mon application pour extraire des données structurées ?"
- "Conçois une architecture RAG pour ma base documentaire"
- "Comment évaluer la qualité de mon système RAG ?"
- "Aide-moi à concevoir un agent IA avec tool use pour mon workflow"
- "Comment optimiser les coûts de mon pipeline LLM en production ?"
- "Dois-je fine-tuner ou est-ce que le prompt engineering suffit ?"
- "Comment mettre en place des guardrails pour mon chatbot IA ?"
- "Conçois une suite d'evals pour mon use case IA"

## Limites et Red Flags

Ce skill n'est PAS adapté pour :
- ❌ **Entraînement de modèles from scratch** (pre-training, research ML) → domaine de la recherche ML, pas de l'ingénierie applicative
- ❌ **Stratégie IA d'entreprise** (choix de déploiement, ROI, gouvernance) → Utiliser plutôt : `ai-governance:strategie-ia`
- ❌ **Éthique et biais des modèles** (audits de biais, fairness, AI Act) → Utiliser plutôt : `ai-governance:ai-ethics`
- ❌ **Prompt engineering pour utilisateurs finaux** (rédaction de prompts, techniques de prompting) → Utiliser plutôt : `ai-governance:prompt-engineering-llmops`
- ❌ **Data engineering et pipelines de données** (ETL, data lakes, data quality) → Utiliser plutôt : `data-bi:data-engineering`

Signaux d'alerte en cours d'utilisation :
- ⚠️ Aucune suite d'evals n'existe — le système est non testable, ne pas déployer en production
- ⚠️ Le coût par requête dépasse 0.10$ pour une tâche simple — model routing nécessaire
- ⚠️ Pas de guardrails sur les outputs — risque d'hallucinations et d'injections en production
- ⚠️ Le prompt est dans le code sans versioning — impossible de tracer les régressions

## Skills connexes

| Skill | Lien |
|---|---|
| Architecture | `code-development:architecture` — Design système et patterns d'architecture |
| Backend & DB | `code-development:backend-db` — Bases de données, dont vector stores |
| Monitoring | `code-development:monitoring` — Observabilité et alerting |
| Auth & Security | `code-development:auth-security` — Sécurité des APIs et des données |
| AI Strategy | `ai-governance:strategie-ia` — Stratégie IA d'entreprise |
| Prompt Engineering | `ai-governance:prompt-engineering-llmops` — Prompt engineering et LLMOps |

## Additional Resources

Consulter les fichiers de référence suivants pour des guides détaillés :

- **[LLM Integration Patterns](./references/llm-integration-patterns.md)** : patterns d'intégration LLM, RAG architecture détaillée, embeddings et vector databases, chunking strategies, prompt engineering avancé, structured output, state of the art 2025-2026.
- **[Agents & Workflows](./references/agents-and-workflows.md)** : conception d'agents IA, tool use et function calling, orchestration multi-agents, mémoire et planification, guardrails, patterns d'agentic AI, state of the art 2025-2026.
- **[ML Engineering & Operations](./references/ml-engineering-ops.md)** : fine-tuning (LoRA, QLoRA), model serving, scaling d'inférence, monitoring IA, gestion des coûts, CI/CD pour pipelines IA, state of the art 2025-2026.
- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.
