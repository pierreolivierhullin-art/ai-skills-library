---
name: prompt-engineering-llmops
description: This skill should be used when the user asks about "prompt engineering", "RAG", "retrieval-augmented generation", "LLM evaluation", "LLMOps", "fine-tuning", "LLM orchestration", "guardrails", "AI agents", "chain-of-thought", "function calling", "tool use", "vector search", "embeddings", "ingénierie de prompts", "génération augmentée par récupération", "évaluation de LLM", "orchestration LLM", "garde-fous", "agents IA", "chaîne de pensée", "appel de fonctions", "recherche vectorielle", "few-shot", "zero-shot", "system prompt", "prompt template", "LangChain", "LlamaIndex", "semantic search", "recherche sémantique", "chunking", "token optimization", "context window", "fenêtre de contexte", "hallucination reduction", "prompt injection defense", "model selection", "choix de modèle", "Claude API", "OpenAI API", "Anthropic", "structured output", "JSON mode", or needs guidance on LLM operations, prompt design, and AI application development.
version: 1.2.0
last_updated: 2026-02
---

# Prompt Engineering & LLMOps — Prompt Design, RAG, Evaluation, Orchestration & Fine-Tuning

## Overview

**FR** -- Cette skill couvre l'ensemble des disciplines de l'ingenierie des prompts et des operations LLM (LLMOps) : conception de prompts avancee, architectures RAG (Retrieval-Augmented Generation), evaluation des LLMs, orchestration d'agents IA, guardrails, fine-tuning et observabilite. Appliquer systematiquement les principes decrits ici pour construire des applications IA robustes, fiables et economiquement viables. Le paysage evolue rapidement (Claude 4.x, GPT-4o, Gemini 2, protocole MCP, agents autonomes) -- ce document reflete l'etat de l'art 2024-2026.

**EN** -- This skill covers the full spectrum of prompt engineering and LLM operations (LLMOps): advanced prompt design, RAG architectures (Retrieval-Augmented Generation), LLM evaluation, AI agent orchestration, guardrails, fine-tuning, and observability. Systematically apply the principles described here to build robust, reliable, and cost-effective AI applications. The landscape evolves rapidly (Claude 4.x, GPT-4o, Gemini 2, MCP protocol, autonomous agents) -- this document reflects the 2024-2026 state of the art.

---

## When This Skill Applies

Activate this skill when the user:

- Designs, optimizes, or debugs prompts for LLMs (system prompts, few-shot, chain-of-thought, structured output)
- Builds or improves a RAG pipeline (chunking, embeddings, vector search, re-ranking, hybrid search)
- Evaluates LLM outputs (hallucination detection, automated eval, benchmarks, red teaming)
- Orchestrates LLM calls with frameworks (LangChain, LlamaIndex, Vercel AI SDK, Semantic Kernel)
- Builds AI agents (tool use, function calling, multi-agent systems, MCP protocol, Claude Code)
- Implements guardrails, safety filters, or prompt injection defenses
- Optimizes LLM costs (caching, model routing, prompt compression, batching)
- Fine-tunes models (LoRA, QLoRA, distillation) or generates synthetic training data
- Sets up LLM observability and monitoring (LangSmith, Langfuse, Helicone)
- Works with multi-modal prompting (vision, audio, documents)

---

## Core Principles

### 1. Prompt as Code -- Version, Test, Iterate
Treat prompts as first-class software artifacts. Store them in version control. Write automated evaluations against golden datasets. Never rely on subjective "feels good" assessment. Track prompt performance metrics (accuracy, latency, cost) across iterations. / Traiter les prompts comme des artefacts logiciels de premiere classe. Les stocker en controle de version. Ecrire des evaluations automatisees sur des datasets de reference. Ne jamais se fier a une evaluation subjective. Suivre les metriques de performance des prompts (precision, latence, cout) a chaque iteration.

### 2. Retrieval Before Generation
Ground LLM outputs in factual, up-to-date context whenever possible. RAG is not optional for knowledge-intensive tasks -- it is the primary defense against hallucination and staleness. Design retrieval quality as carefully as generation quality. / Ancrer les sorties LLM dans un contexte factuel et a jour chaque fois que possible. Le RAG n'est pas optionnel pour les taches a forte intensite de connaissances -- c'est la defense principale contre l'hallucination et l'obsolescence. Concevoir la qualite de la recherche avec autant de soin que la qualite de la generation.

### 3. Evaluate Continuously, Not Once
Build automated evaluation pipelines that run on every prompt change, every model upgrade, and every data refresh. Use multiple evaluation dimensions: faithfulness, relevance, coherence, safety. Human evaluation complements but does not replace automated eval. / Construire des pipelines d'evaluation automatises qui s'executent a chaque changement de prompt, chaque mise a jour de modele et chaque rafraichissement de donnees. Utiliser plusieurs dimensions d'evaluation : fidelite, pertinence, coherence, securite. L'evaluation humaine complete mais ne remplace pas l'evaluation automatisee.

### 4. Defense in Depth for Safety
Never rely on a single safety mechanism. Layer system prompts, input validation, output filtering, guardrail models, and monitoring. Assume adversarial users. Test with red teaming. / Ne jamais compter sur un seul mecanisme de securite. Superposer prompts systeme, validation d'entree, filtrage de sortie, modeles de guardrails et monitoring. Supposer des utilisateurs adversariaux. Tester avec du red teaming.

### 5. Optimize for the Right Model at the Right Cost
Not every task needs the most powerful model. Route simple tasks to small models, complex tasks to large models. Use prompt caching to avoid redundant computation. Measure cost per task, not just cost per token. / Chaque tache ne necessite pas le modele le plus puissant. Router les taches simples vers les petits modeles, les taches complexes vers les grands modeles. Utiliser le cache de prompts pour eviter les calculs redondants. Mesurer le cout par tache, pas seulement le cout par token.

### 6. Agents Are Powerful but Require Guardrails
Agentic AI (tool use, multi-step reasoning, autonomous execution) unlocks transformative capabilities but introduces new failure modes. Constrain agent scope, require human approval for high-stakes actions, log every tool invocation, and set hard limits on iterations and cost. / L'IA agentique (utilisation d'outils, raisonnement multi-etapes, execution autonome) libere des capacites transformatrices mais introduit de nouveaux modes de defaillance. Limiter la portee de l'agent, exiger une approbation humaine pour les actions a haut risque, journaliser chaque invocation d'outil et fixer des limites strictes sur les iterations et le cout.

---

## Key Frameworks & Methods

| Framework / Method | Purpose | FR |
|---|---|---|
| **Prompt Patterns (CoT, ToT, ReAct)** | Structured reasoning techniques for LLMs | Techniques de raisonnement structure pour les LLMs |
| **RAG (Naive, Advanced, Modular)** | Ground generation in retrieved knowledge | Ancrer la generation dans la connaissance recuperee |
| **RAGAS / DeepEval** | Automated RAG and LLM evaluation | Evaluation automatisee des RAG et LLMs |
| **LangChain / LlamaIndex** | LLM orchestration and data frameworks | Frameworks d'orchestration LLM et de donnees |
| **MCP Protocol** | Model Context Protocol for tool integration | Protocole de contexte de modele pour l'integration d'outils |
| **LoRA / QLoRA** | Parameter-efficient fine-tuning | Fine-tuning efficace en parametres |
| **Guardrails AI / NeMo Guardrails** | Safety and compliance enforcement | Application de la securite et de la conformite |
| **LangSmith / Langfuse / Helicone** | LLM observability and tracing | Observabilite et tracing des LLMs |

---

## Decision Guide

### Choosing a Prompt Strategy

```
1. What is the task complexity?
   +-- Simple extraction/classification -> Zero-shot or few-shot prompting
   +-- Multi-step reasoning -> Chain-of-Thought (CoT) or ReAct
   +-- Complex problem-solving -> Tree-of-Thought (ToT) or multi-agent decomposition
   +-- Creative generation -> Persona-based system prompts + temperature tuning

2. Does the task require external knowledge?
   +-- Static, well-known knowledge -> Fine-tuned model or few-shot examples
   +-- Dynamic, domain-specific knowledge -> RAG pipeline
   +-- Real-time data -> RAG + live API tools (function calling / MCP)

3. Does the output need to be structured?
   +-- JSON/XML required -> Structured output mode (JSON mode, tool_use, response_format)
   +-- Free text -> Standard prompting with output format instructions
   +-- Mixed -> Tool use for structured parts, text generation for narrative parts
```

### Choosing a RAG Architecture

- **Naive RAG** -- Simple embed-chunk-retrieve-generate. Use for prototypes, internal tools with clean data, and when latency is critical.
- **Advanced RAG** -- Add re-ranking, query expansion, HyDE, or self-RAG. Use when naive RAG retrieval precision@5 < 70% or faithfulness < 85%, and the data corpus exceeds 10K documents or contains noisy/heterogeneous sources.
- **Modular RAG** -- Pluggable components (routing, multi-index, iterative retrieval). Use for production systems with diverse data sources and complex query patterns.

### Choosing an Orchestration Framework

- **LangChain** -- Largest ecosystem, LCEL for composable chains, strong agent support. Prefer for complex multi-step pipelines with diverse integrations.
- **LlamaIndex** -- Best for data-centric RAG applications. Superior indexing, query engine, and data connector ecosystem.
- **Vercel AI SDK** -- Best for TypeScript/Next.js applications, streaming-first, excellent developer experience.
- **Semantic Kernel** -- Best for .NET/enterprise environments with Microsoft ecosystem integration.
- **Direct API calls** -- Best for simple use cases. Avoid framework overhead when a single API call suffices.

---

## Common Patterns & Anti-Patterns

### Patterns (Do)

- **System Prompt + User Prompt Separation**: Place persistent instructions, persona, constraints, and output format in the system prompt. Place task-specific content in the user prompt. This enables prompt caching and clean separation of concerns.
- **Golden Dataset Evaluation**: Maintain a curated dataset of (input, expected_output) pairs. Run automated evaluation on every prompt change. Track metrics over time.
- **Retrieval-Augmented Everything**: For any task involving factual claims, retrieve supporting evidence. Display citations. Let the user verify.
- **Structured Output Enforcement**: Use JSON mode, tool_use, or schema-constrained decoding to guarantee parseable output. Never rely on regex parsing of free text.
- **Multi-Model Routing**: Route simple queries to small, fast models (Claude Haiku, GPT-4o-mini) and complex queries to capable models (Claude Opus, GPT-4o). Use a classifier or heuristics based on input complexity.
- **Prompt Caching**: Leverage provider-level prompt caching (Anthropic prompt caching, OpenAI cached prompts) for long system prompts and repeated context. Reduces latency and cost by 80-90% on cache hits.

### Anti-Patterns (Avoid)

- **Prompt-and-Pray**: Deploying prompts without systematic evaluation. Every production prompt must have automated tests.
- **RAG Without Evaluation**: Building a RAG pipeline without measuring retrieval precision, recall, and faithfulness. Measure before and after every change.
- **Unbounded Agents**: Letting agents run unlimited iterations with unrestricted tool access. Always set max_iterations, budget limits, and scope constraints.
- **Single-Layer Safety**: Relying only on a system prompt for safety. Attackers bypass system prompts. Layer input filtering, output filtering, and guardrail models.
- **Ignoring Latency**: Optimizing only for quality without measuring latency. Users abandon applications with > 3s time-to-first-token. Measure and optimize the full pipeline.
- **Fine-Tuning Before Prompt Engineering**: Jumping to fine-tuning before exhausting prompt optimization, few-shot examples, and RAG. Fine-tuning is expensive and creates maintenance burden. Use it only when prompting alone is insufficient.

---

## Implementation Workflow

Follow this workflow when building an LLM-powered application:

1. **Define the Task and Success Criteria** -- Specify exactly what the LLM must produce. Define measurable success criteria (accuracy > 95%, latency < 2s, cost < $0.01/request). Create a golden evaluation dataset of at least 50-100 examples.

2. **Design the Prompt** -- Start with zero-shot. Add few-shot examples if accuracy is insufficient. Add chain-of-thought if reasoning is required. Use the system prompt for persistent instructions and persona. Use structured output for parseable results.

3. **Add Retrieval if Needed** -- If the task requires external knowledge, implement RAG. Choose chunking strategy, embedding model, and vector store. Evaluate retrieval quality independently (precision@k, recall@k, MRR) before connecting to generation.

4. **Implement Safety Layers** -- Add input validation (length, content filtering). Add output filtering (PII detection, toxicity check). Implement prompt injection defenses. Set up guardrails for high-risk domains.

5. **Build the Orchestration Pipeline** -- Choose a framework or direct API calls based on complexity. Implement error handling, retries with exponential backoff, and fallback models. Add streaming for user-facing applications.

6. **Evaluate and Iterate** -- Run the evaluation pipeline on the golden dataset. Measure faithfulness (% of claims supported by sources), relevance (% of answers addressing the query), coherence (human rating 1-5), and safety (% of outputs passing content filters). Iterate on prompts, retrieval, and pipeline until success criteria are met. Use A/B testing for production changes.

7. **Deploy with Observability** -- Instrument every LLM call with tracing (LangSmith, Langfuse). Monitor latency (P50, P95, P99), cost per request, error rates (timeouts, 4xx, 5xx), and output quality (hallucination rate, user thumbs-up ratio, faithfulness score). Set up alerts when any metric degrades beyond 10% of the baseline.

8. **Optimize Costs** -- Implement prompt caching. Set up model routing (small model for simple tasks, large model for complex tasks). Compress prompts where possible. Batch requests when latency allows.

9. **Consider Fine-Tuning Only as a Last Resort** -- Fine-tune only si le prompting + RAG plafonnent sous les criteres de succes apres 3+ iterations documentees. Commencer par LoRA/QLoRA (< 1% des parametres entraines). Minimum 1000 exemples d'entrainement (generer des donnees synthetiques si donnees reelles < 500). Evaluer le modele fine-tune sur le meme golden dataset et comparer les metriques point par point.

---

## Modèle de maturité

### Niveau 1 — Exploratoire
- Prompts ad-hoc sans versioning ni structure réutilisable
- Pas d'évaluation systématique des sorties LLM
- Utilisation naïve des modèles sans guardrails ni filtrage
- **Indicateurs** : taux d'hallucination non mesuré, 0% de couverture d'évaluation

### Niveau 2 — Structuré
- Templates de prompts réutilisables avec séparation system/user prompt
- Évaluation manuelle sur des cas de test représentatifs
- RAG basique opérationnel (chunking fixe, embedding standard)
- **Indicateurs** : taux d'hallucination mesuré manuellement, logs d'usage centralisés

### Niveau 3 — Industrialisé
- Prompt versioning en contrôle de source avec historique de performance
- Évaluation automatisée en CI/CD (RAGAS, DeepEval, golden datasets)
- RAG avancé en production (re-ranking, hybrid search, guardrails actifs)
- **Indicateurs** : couverture d'évaluation > 80%, taux d'hallucination < 5%

### Niveau 4 — Optimisé
- Orchestration multi-modèles avec routing intelligent par complexité
- Évaluation continue en production (LLM-as-Judge, A/B testing de prompts)
- Observabilité complète (LangSmith/Langfuse, coût par tâche, latence P95)
- **Indicateurs** : cycle d'itération prompt < 1 jour, coût par tâche optimisé et suivi

### Niveau 5 — Autonome
- Agents autonomes avec tool use et orchestration multi-agents
- Self-improving prompts par feedback loops et évaluation automatique
- Fine-tuning automatisé et coûts optimisés par caching et distillation
- **Indicateurs** : couverture d'évaluation > 95%, coût réduit de 50%+ par distillation

## Rythme opérationnel

| Cadence | Activité | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Hebdomadaire** | Revue des métriques de performance des prompts (accuracy, latence, coût) | Prompt Engineer | Dashboard de performance prompt et alertes |
| **Hebdomadaire** | Triage des erreurs LLM et hallucinations remontées par le monitoring | ML Engineer | Backlog d'améliorations priorisé |
| **Mensuel** | Audit du pipeline d'évaluation (golden datasets, couverture, seuils) | Prompt Engineer + QA | Rapport d'audit eval et mises à jour des datasets |
| **Mensuel** | Revue de sécurité des guardrails et tests de prompt injection | AI Security Lead | Rapport de vulnérabilités et remédiations |
| **Trimestriel** | Revue qualité RAG (retrieval precision, faithfulness, coût par requête) | ML Engineer + Data Engineer | Scorecard RAG et plan d'optimisation |
| **Trimestriel** | Benchmark des modèles et revue de la stratégie de routing multi-modèles | AI Architect | Rapport de benchmark et recommandations de routing |
| **Annuel** | Refresh du stack LLM (nouveaux modèles, frameworks, providers) et roadmap LLMOps | AI Architect + CTO | Roadmap LLMOps et stratégie modèles à 12 mois |

## State of the Art (2025-2026)

L'ingénierie de prompts et les LLMOps se professionnalisent :

- **Agentic workflows** : Les architectures d'agents IA (multi-agents, tool use, planning) remplacent les chaînes de prompts simples pour les tâches complexes.
- **RAG avancé** : Les techniques évoluent (contextual retrieval, reranking, hybrid search, GraphRAG) pour améliorer la qualité des réponses.
- **Structured outputs** : Les LLM supportent nativement la génération de JSON structuré, réduisant le besoin de parsing et améliorant la fiabilité.
- **Evaluation frameworks** : Les frameworks d'évaluation (RAGAS, DeepEval, promptfoo) permettent des tests systématiques de qualité avant déploiement.
- **Fine-tuning efficient** : Les techniques de fine-tuning léger (LoRA, QLoRA, PEFT) rendent la personnalisation des modèles accessible sans infrastructure massive.

## Template actionnable

### Template de system prompt structuré

```text
# Rôle
Tu es un [rôle spécifique] expert en [domaine].

# Contexte
[Description du contexte d'utilisation]

# Instructions
1. [Instruction principale]
2. [Contrainte de format]
3. [Contrainte de ton]

# Format de sortie
[Description du format attendu]

# Exemples
Input: [exemple d'entrée]
Output: [exemple de sortie attendue]

# Garde-fous
- Ne jamais [limite 1]
- Toujours [limite 2]
- Si incertain, [comportement par défaut]
```

## Prompts types

- "Comment concevoir un système RAG performant ?"
- "Aide-moi à optimiser mon prompt pour réduire les hallucinations"
- "Propose une architecture d'agents IA avec function calling"
- "Comment évaluer la qualité des réponses de mon LLM ?"
- "Aide-moi à choisir entre fine-tuning et few-shot prompting"
- "Comment mettre en place des guardrails pour notre chatbot ?"
- "Quelle stratégie de chunking pour mon pipeline RAG ?"

## Limites et Red Flags

Ce skill n'est PAS adapte pour :
- ❌ Definition de la strategie IA d'entreprise, roadmap ou gouvernance organisationnelle → Utiliser plutot : `ai-governance:strategie-ia`
- ❌ Audit de biais algorithmiques, metriques de fairness ou explicabilite ethique → Utiliser plutot : `ai-governance:ai-ethics`
- ❌ Red teaming securitaire, gestion des incidents IA ou conformite reglementaire → Utiliser plutot : `ai-governance:ai-risk`
- ❌ Architecture logicielle generale (microservices, APIs) sans composante LLM → Utiliser plutot : `code-development:architecture`
- ❌ Data engineering pur (pipelines ETL, data lakes) sans lien avec un pipeline RAG ou LLM → Utiliser plutot : `data-bi:data-engineering`

Signaux d'alerte en cours d'utilisation :
- ⚠️ Le prompt est deploye en production sans golden dataset d'evaluation (meme minimal de 50 exemples) — c'est du "Prompt-and-Pray", creer un jeu de test avant tout deploiement
- ⚠️ Le taux d'hallucination n'est pas mesure — mettre en place un scoring de faithfulness (% de claims ancrees dans les sources) avant de deployer un RAG
- ⚠️ Le fine-tuning est envisage alors que le prompt n'a ete itere que 1-2 fois — epuiser d'abord le prompting (few-shot, CoT) et le RAG avant de fine-tuner
- ⚠️ Un agent IA a un acces illimite aux outils sans plafond d'iterations ni budget API — restreindre le scope, plafonner les actions et exiger une approbation humaine pour les actions a fort impact

## Skills connexes

| Skill | Lien |
|---|---|
| Stratégie IA | `ai-governance:strategie-ia` — Stratégie et choix de modèles |
| Architecture | `code-development:architecture` — Architecture des applications LLM |
| Backend & DB | `code-development:backend-db` — Bases vectorielles et APIs |
| AI Risk | `ai-governance:ai-risk` — Guardrails et sécurité des prompts |
| Product Analytics | `code-development:product-analytics` — Métriques et évaluation des LLM |

## Glossaire

| Terme | Définition |
|-------|-----------|
| **RAG (Retrieval-Augmented Generation)** | Architecture combinant recherche documentaire et génération par LLM : les documents pertinents sont récupérés puis injectés dans le contexte pour ancrer la réponse dans des faits vérifiables. |
| **Chain-of-Thought (CoT)** | Technique de prompting incitant le LLM à décomposer son raisonnement en étapes intermédiaires explicites avant de fournir la réponse finale, améliorant la précision sur les tâches complexes. |
| **Tree-of-Thought (ToT)** | Extension du CoT où le modèle explore plusieurs branches de raisonnement en parallèle, évalue chaque chemin et sélectionne le plus prometteur pour résoudre des problèmes complexes. |
| **ReAct** | Pattern combinant raisonnement (Reasoning) et action (Acting) : le LLM alterne entre réflexion sur la tâche et appel à des outils externes pour construire sa réponse de manière itérative. |
| **Few-shot Prompting** | Technique fournissant au LLM quelques exemples (input, output) dans le prompt pour guider le format, le style et la logique de la réponse attendue sans fine-tuning. |
| **Zero-shot Prompting** | Technique demandant au LLM d'effectuer une tâche sans aucun exemple préalable, en s'appuyant uniquement sur les instructions et les connaissances pré-entraînées du modèle. |
| **System Prompt** | Instructions persistantes définissant le rôle, le comportement, les contraintes et le format de sortie du LLM, séparées du prompt utilisateur et appliquées à chaque interaction. |
| **Embedding** | Représentation vectorielle dense d'un texte dans un espace multidimensionnel, capturant le sens sémantique et permettant le calcul de similarité entre documents ou requêtes. |
| **Vector Database** | Base de données spécialisée dans le stockage et la recherche efficace de vecteurs d'embedding via des algorithmes de plus proches voisins (ANN), fondement technique du RAG. |
| **Chunking** | Processus de découpage de documents en segments (chunks) de taille optimale pour l'embedding et la recherche vectorielle, stratégie clé impactant la qualité du RAG. |
| **Re-ranking** | Étape de réordonnancement des résultats de recherche initiaux à l'aide d'un modèle cross-encoder plus précis, améliorant la pertinence des documents fournis au LLM. |
| **HyDE (Hypothetical Document Embeddings)** | Technique RAG avancée où le LLM génère d'abord un document hypothétique répondant à la requête, puis utilise son embedding pour rechercher des documents réels similaires. |
| **CRAG (Corrective RAG)** | Architecture RAG intégrant un évaluateur de pertinence qui vérifie la qualité des documents récupérés et déclenche des stratégies de correction (nouvelle recherche, web search) si nécessaire. |
| **Self-RAG** | Architecture où le LLM décide de manière autonome s'il a besoin de récupérer des informations, évalue la pertinence des documents et vérifie la fidélité de sa propre réponse. |
| **Function Calling** | Capacité d'un LLM à générer des appels de fonctions structurés (nom, paramètres) permettant l'interaction avec des APIs externes, bases de données ou outils logiciels. |
| **Tool Use** | Mécanisme permettant à un LLM d'utiliser des outils externes (calculatrice, recherche web, exécution de code) pour augmenter ses capacités au-delà de la génération de texte. |
| **MCP (Model Context Protocol)** | Protocole standardisé (Anthropic) définissant comment les LLM interagissent avec des outils et sources de données externes via une interface unifiée client-serveur. |
| **Guardrails** | Mécanismes de sécurité (filtres d'entrée/sortie, règles métier, validations) encadrant le comportement d'un LLM pour prévenir les réponses inappropriées, dangereuses ou hors périmètre. |
| **Fine-tuning** | Processus d'adaptation d'un modèle pré-entraîné à une tâche spécifique en le ré-entraînant sur un jeu de données spécialisé, modifiant ses poids pour améliorer ses performances dans un domaine. |
| **LoRA (Low-Rank Adaptation)** | Technique de fine-tuning efficace en paramètres qui gèle les poids du modèle original et n'entraîne que de petites matrices de faible rang, réduisant drastiquement les coûts de calcul et de stockage. |
| **Prompt Caching** | Mécanisme de mise en cache des préfixes de prompts côté fournisseur (Anthropic, OpenAI), évitant le retraitement des instructions système répétitives et réduisant latence et coûts de 80-90%. |
| **Temperature** | Paramètre contrôlant le caractère aléatoire des réponses du LLM : une valeur basse (0-0.3) produit des réponses déterministes et factuelles, une valeur haute (0.7-1.0) favorise la créativité et la diversité. |

## Additional Resources

Consult these reference files for deep dives on each topic area:

- **[Prompt Patterns](./references/prompt-patterns.md)** -- All prompt design patterns (zero-shot, few-shot, CoT, ToT, ReAct, self-consistency), system prompt design, persona engineering, prompt injection prevention, structured output (JSON mode, tool use), multi-modal prompting, prompt templating and version control, prompt optimization techniques, state-of-the-art 2024-2026.

- **[RAG Architecture](./references/rag-architecture.md)** -- RAG patterns (naive, advanced, modular), chunking strategies (fixed-size, semantic, recursive, parent-child, document-aware), embedding models, vector databases, hybrid search (BM25 + dense), advanced RAG techniques (re-ranking, query expansion, HyDE, self-RAG, CRAG, iterative retrieval), RAG evaluation metrics (precision, recall, MRR, NDCG, faithfulness).

- **[LLM Evaluation](./references/llm-evaluation.md)** -- Evaluation frameworks (RAGAS, DeepEval, LangSmith Evaluators, Braintrust), benchmark design, golden dataset creation, human evaluation protocols, automated eval pipelines, hallucination detection, red teaming and adversarial testing, safety evaluation, continuous evaluation in production.

- **[LLMOps & Orchestration](./references/llmops-orchestration.md)** -- Orchestration frameworks (LangChain, LlamaIndex, Semantic Kernel, Vercel AI SDK), agent frameworks and patterns (tool use, multi-agent, CrewAI, AutoGen, Claude Code), MCP protocol, model routing and fallback strategies, cost optimization (caching, compression, batching), observability (LangSmith, Langfuse, Helicone), guardrails (NeMo Guardrails, Guardrails AI), fine-tuning strategies (LoRA, QLoRA, distillation), synthetic data generation.

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.
