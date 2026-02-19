---
name: agentic-ai
version: 1.0.0
description: >
  Use this skill when the user asks about "AI agents", "agentic AI", "autonomous AI", "multi-agent systems", "LangGraph", "CrewAI", "AutoGen", "agent orchestration", "tool use", "function calling advanced", "ReAct pattern", "plan and execute", "AI workflows autonomous", "agent memory", "agent evaluation", "MCP model context protocol", "agentic RAG", "AI agent safety", discusses building or deploying AI systems that autonomously plan and execute multi-step tasks, or needs guidance on multi-agent architectures and orchestration frameworks.
---

# Agentic AI — Agents Autonomes et Systemes Multi-Agents

## Overview

Les agents IA representent un changement de paradigme par rapport aux LLMs classiques. Un LLM repond a une question ; un agent accomplit une tache de bout en bout, en prenant des decisions, en utilisant des outils, en gerant des erreurs et en s'adaptant aux resultats intermediaires.

En 2025-2026, les agents IA passent des experimentations en laboratoire au deploiement en production. Les frameworks maturent (LangGraph, CrewAI, AutoGen Microsoft), les patterns se stabilisent, et les cas d'usage entreprise se precisent (automatisation de workflows complexes, agents de support, agents de recherche).

---

## Architecture d'un Agent IA

### Composants Fondamentaux

**LLM (Brain)** : le modele de langage au coeur de l'agent. Prend les decisions, genere les plans, interprete les resultats. Choisir un modele avec fort raisonnement pour les agents complexes (Claude Opus 4, GPT-4o, Gemini Ultra).

**Tools (Hands)** : fonctions que l'agent peut appeler. Recherche web, execution de code, acces bases de donnees, APIs externes, gestion de fichiers, envoi d'emails.

**Memory (Storage)** : les agents ont besoin de memoire pour fonctionner sur des taches longues.
- **In-context** : dans la fenetre de contexte (limite)
- **External** : base vectorielle (semantic search), base de donnees (facts), cache (resultats intermediaires)
- **Episodic** : historique des interactions precedentes

**Orchestrator** : gere le flux d'execution, decide quand deleguer a quel agent, gere les erreurs.

**State** : l'etat courant de la tache (ce qui a ete fait, ce qui reste a faire, artefacts produits).

---

## Patterns d'Architecture Agent

### 1. ReAct (Reasoning + Acting)

Le pattern le plus simple et le plus repandu.

**Cycle** : Think → Act → Observe → Repeat

```python
# Pseudo-code ReAct
while not task_complete:
    thought = llm.reason(context, available_tools, history)
    if thought.action:
        result = tools.execute(thought.action)
        history.append(thought, result)
    else:
        final_answer = thought.answer
        break
```

**Usage** : taches avec outils multiples, besoin de raisonnement intermediaire, recherche d'information.

**Limite** : context window peut etre limitee sur les longues taches. Pas de planification a long terme.

### 2. Plan-and-Execute

**Etape 1** : Planifier la tache complete en sous-etapes (plan).
**Etape 2** : Executer chaque sous-etape sequentiellement ou en parallele.
**Etape 3** : Re-planifier si une etape echoue ou si les resultats changent le plan.

**Avantage** : vision globale de la tache, moins de "hallucination de chemin".

**Limit** : le plan initial peut etre sous-optimal. Necessite un mecanisme de re-planification.

### 3. Reflexion (Self-Reflection)

L'agent genere une reponse, puis l'evalue lui-meme et l'ameliore.

```
Draft → Critique → Revise → Critique → Revise → Final
```

**Usage** : generation de documents complexes (rapports, code), taches ou la qualite compte plus que la vitesse.

### 4. Parallel Tool Calling

Executer plusieurs outils simultanement plutôt que sequentiellement.

**Exemple** : pour repondre a "Analyse les 5 principaux concurrents de X", appeler 5 recherches web en parallele plutôt qu'une par une.

**Gain** : 3-5x plus rapide sur les taches avec outils independants.

---

## Frameworks Multi-Agents

### LangGraph (LangChain)

Orchestration basee sur un graphe d'etats. Le plus mature et le plus flexible en 2025.

**Concepts cles** :
- **Nodes** : fonctions qui modifient l'etat
- **Edges** : connexions entre nodes (conditionnelles ou fixes)
- **State** : dictionnaire partage entre tous les nodes
- **Checkpointing** : persistance de l'etat pour les workflows longs

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    current_step: str
    results: dict

def research_node(state: AgentState) -> AgentState:
    # Logique de recherche
    results = web_search(state["messages"][-1])
    return {**state, "results": results}

def synthesize_node(state: AgentState) -> AgentState:
    # Logique de synthese
    summary = llm.summarize(state["results"])
    return {**state, "messages": state["messages"] + [summary]}

def should_continue(state: AgentState) -> str:
    if state["current_step"] == "done":
        return END
    return "research"

# Construction du graphe
graph = StateGraph(AgentState)
graph.add_node("research", research_node)
graph.add_node("synthesize", synthesize_node)
graph.add_edge("research", "synthesize")
graph.add_conditional_edges("synthesize", should_continue)
graph.set_entry_point("research")

app = graph.compile()
```

**Usage** : workflows complexes avec branches conditionnelles, agents de long-running, human-in-the-loop.

### CrewAI

Multi-agent framework oriente "equipes" de specialistes.

**Concepts** :
- **Agent** : role, goal, backstory, tools
- **Task** : description, expected output, agent assigne
- **Crew** : equipe d'agents avec un process (sequential ou hierarchical)

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI",
    backstory="Expert at finding and synthesizing AI research",
    tools=[web_search_tool, arxiv_tool],
    llm="claude-opus-4-6"
)

writer = Agent(
    role="Tech Content Writer",
    goal="Create compelling tech content",
    backstory="Expert at translating complex topics for business audiences",
    llm="claude-sonnet-4-6"
)

research_task = Task(
    description="Research the top 5 AI agent frameworks in 2025",
    agent=researcher,
    expected_output="Structured comparison with pros/cons"
)

writing_task = Task(
    description="Write a 1000-word article based on the research",
    agent=writer,
    expected_output="Blog post in markdown"
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential
)

result = crew.kickoff()
```

**Usage** : taches structurees avec roles distincts, pipelines de contenu, analyse competitive.

### AutoGen (Microsoft)

Framework conversation-centric. Les agents collaborent via un systeme de messages.

**Concepts** :
- **AssistantAgent** : LLM avec tools
- **UserProxyAgent** : peut executer du code, interface humain
- **GroupChat** : plusieurs agents qui conversent

**Usage** : code generation et debugging (excellent), taches avec execution de code, research avec verification.

### Comparaison des Frameworks

| Critere | LangGraph | CrewAI | AutoGen |
|---|---|---|---|
| Flexibilite | Tres haute | Moyenne | Haute |
| Courbe d'apprentissage | Haute | Faible | Moyenne |
| State management | Excellent | Basique | Moyen |
| Human-in-the-loop | Natif | Plugin | Natif |
| Production-ready | Oui | Oui | Oui |
| Use case ideal | Workflows complexes | Equipes de specialistes | Code + recherche |

---

## Model Context Protocol (MCP)

Protocole standard Anthropic pour connecter des outils aux agents de facon unifiee.

**Principe** : les tools/ressources sont exposes via des MCP servers standardises. L'agent (MCP client) peut decouvrir et utiliser n'importe quel MCP server compatible.

**Ecosysteme** : en 2025, des centaines de MCP servers disponibles (GitHub, Slack, Notion, databases, APIs).

**Avantage** : un agent peut etre connecte a tous les systemes de l'entreprise via des MCP servers standards, sans code d'integration custom pour chaque outil.

---

## Evaluation des Agents

### Metriques d'Evaluation

**Task completion rate** : % de taches completees correctement sans intervention humaine.

**Token efficiency** : tokens utilises / qualite du resultat. Les agents peuvent etre tres couteux en tokens.

**Tool call accuracy** : % d'appels d'outils corrects (bon outil, bons arguments).

**Hallucination rate** : % de faits incorrects dans les resultats finaux. Critique pour les agents factuels.

**Latency** : temps moyen pour completer une tache. Les agents multi-steps peuvent etre lents.

### Frameworks d'Evaluation

**LangSmith** (LangChain) : traçage complet des runs d'agents, datasets d'evaluation, comparaison de versions.

**AgentEval** : framework open-source Microsoft pour evaluer les agents sur des benchmarks.

**LLM-as-Judge** : utiliser un LLM puissant pour evaluer les outputs d'un agent sur des criteres definis.

---

## Safety et Guardrails pour les Agents Autonomes

### Risques Specifiques aux Agents

**Action irreversible** : un agent qui supprime des fichiers, envoie des emails ou modifie une base de production peut causer des dommages impossibles a annuler.

**Prompt injection** : un contenu malveillant dans les donnees lues par l'agent peut modifier ses instructions.

**Scope creep** : un agent qui depasse le perimetre de sa tache et effectue des actions non prevues.

**Boucles infinies** : agent bloque dans un cycle de re-planning/retry.

### Guardrails Fondamentaux

**Principe du moindre privilege** : chaque agent n'a acces qu'aux outils strictement necessaires a sa tache.

**Human-in-the-loop** : pour les actions a fort impact (envoi email, ecriture en base, appel API externe), requrir une confirmation humaine.

**Dry-run mode** : executer l'agent en mode simulation avant le mode live. Montrer ce qu'il ferait sans le faire.

**Timeouts et max iterations** : limiter le nombre de steps et le temps d'execution. Stopper proprement si depasse.

**Audit logs** : loguer chaque action de l'agent avec contexte, input, output et timestamp. Indispensable pour le debugging et la conformite.

---

## Use Cases Entreprise

| Use Case | Stack recommandee | Valeur |
|---|---|---|
| Support client niveau 1 | LangGraph + RAG + ticket system | -60% tickets humains |
| Recherche competitive | CrewAI (researcher + analyst + writer) | Rapports en 10 min vs 3h |
| Code review automatise | AutoGen + GitHub MCP | Revue en quelques minutes |
| Data analysis pipeline | LangGraph + code execution | Analyse ad hoc sans datapipeline |
| Onboarding employe | LangGraph + HR systems MCP | Acces autonome aux procedures |
| Monitoring et alerting | Agent reactif sur metriques | Escalade intelligente |

---

## Maturity Model — AI Agents

| Niveau | Caracteristique |
|---|---|
| **1 — Prompt simple** | LLM avec prompt, pas d'outils, pas d'etat |
| **2 — Tool use basique** | LLM + 1-3 tools simples, single-step |
| **3 — Agent autonome** | ReAct multi-steps, memoire basique, 1 use case |
| **4 — Multi-agent** | Plusieurs agents specialises, orchestration, evaluation |
| **5 — Systeme agentique** | Agents en production, monitoring, guardrails, amelioration continue |
