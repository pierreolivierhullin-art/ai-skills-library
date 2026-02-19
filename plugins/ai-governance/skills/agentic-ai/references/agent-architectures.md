# Architectures d'Agents IA — Patterns et Implementation

## Definition d'un Agent IA

Un agent IA est un systeme autonome compose de quatre elements fondamentaux : un LLM comme moteur de raisonnement, un ensemble de tools (fonctions, APIs, bases de donnees), un systeme de memoire pour maintenir le contexte, et une boucle d'action (action loop) qui itere jusqu'a completion de la tache.

La boucle fondamentale : **Observe → Think → Act → Observe**.

```
[User Input] → [LLM Reasoning] → [Tool Selection] → [Tool Execution] → [Observation]
                     ↑                                                        |
                     └────────────────────────────────────────────────────────┘
                                     (repeat until done)
```

Contrairement a un LLM classique (une requete, une reponse), un agent itere : il peut executer 5, 10, ou 50 etapes avant de retourner un resultat final. Cette autonomie est a la fois sa force et son risque principal.

---

## Pattern 1 : ReAct (Reasoning + Acting)

### Principe

ReAct (Yao et al., 2022) entrelace le raisonnement (Thought) et les actions (Action) dans une boucle coherente. Le LLM genere explicitement sa pensee avant chaque action, ce qui rend le comportement interpretable et debuggable.

Structure d'une iteration ReAct :
1. **Thought** : Le LLM exprime son raisonnement
2. **Action** : Le LLM choisit un tool et ses parametres
3. **Observation** : Le resultat du tool est injecte dans le contexte
4. Retour a Thought jusqu'a obtenir la reponse finale

### Implementation Python avec LangChain

```python
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import requests

# Definition des tools
@tool
def search_web(query: str) -> str:
    """Recherche des informations sur le web. Utiliser pour les faits recents."""
    # Integration avec Tavily ou SerpAPI en production
    return f"Resultats de recherche pour: {query}"

@tool
def calculate(expression: str) -> str:
    """Execute un calcul mathematique. Expression Python valide uniquement."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Erreur de calcul: {e}"

@tool
def get_stock_price(ticker: str) -> str:
    """Recupere le prix d'une action boursiere."""
    # Exemple simplifie — utiliser yfinance en production
    prices = {"AAPL": 175.50, "MSFT": 380.20, "GOOGL": 140.10}
    return str(prices.get(ticker.upper(), "Ticker non trouve"))

# Configuration du LLM et de l'agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [search_web, calculate, get_stock_price]

# Prompt ReAct standard depuis LangChain Hub
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,          # Affiche chaque Thought/Action/Observation
    max_iterations=10,     # Protection contre les boucles infinies
    handle_parsing_errors=True  # Gere les erreurs de format LLM
)

result = agent_executor.invoke({
    "input": "Quel est le ratio P/E approximatif d'Apple si son EPS est 6.5?"
})
print(result["output"])
```

### Avantages et Limites

**Avantages** : Simple a implementer, transparent (chaque pensee est visible), bon pour les taches exploratoires, facile a debugger.

**Limites** : Inefficace pour les taches longues (pas de plan d'ensemble), prone aux hallucinations sur les tools disponibles, cout en tokens eleve (chaque thought consomme du contexte).

**Quand utiliser ReAct** : Taches de moins de 5-7 etapes, domaines bien definis avec tools clairs, quand la transparence est prioritaire.

---

## Pattern 2 : Plan-and-Execute

### Principe

Plan-and-Execute separe la planification de l'execution. Un LLM "planner" genere un plan complet en avance, puis un LLM "executor" (souvent plus petit et moins couteux) execute chaque etape. En cas d'erreur ou de resultat inattendu, le planner re-planifie.

Avantage majeur : coherence globale de la tache, meilleure gestion des taches longues et complexes.

### Implementation Python

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
import json

class Plan(BaseModel):
    steps: List[str] = Field(description="Liste ordonnee des etapes a executer")

class StepResult(BaseModel):
    step: str
    result: str
    success: bool

# LLM de planification (modele puissant)
planner_llm = ChatOpenAI(model="gpt-4o", temperature=0)

# LLM d'execution (modele plus rapide/economique)
executor_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def create_plan(task: str, context: str = "") -> Plan:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un planificateur expert. Decompose la tache en etapes atomiques et sequentielles. Sois precis et actionnable."),
        ("user", f"Tache: {task}\nContexte: {context}\n\nCree un plan detaille.")
    ])
    chain = prompt | planner_llm.with_structured_output(Plan)
    return chain.invoke({})

def execute_step(step: str, previous_results: List[StepResult]) -> StepResult:
    context = "\n".join([f"Etape '{r.step}': {r.result}" for r in previous_results])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un executeur. Execute precisement l'etape donnee en utilisant le contexte disponible."),
        ("user", f"Etapes precedentes:\n{context}\n\nEtape a executer: {step}")
    ])
    chain = prompt | executor_llm
    result = chain.invoke({})
    return StepResult(step=step, result=result.content, success=True)

def replan(task: str, original_plan: Plan, results: List[StepResult], error: str) -> Plan:
    """Re-planifie en cas d'erreur ou de deviation."""
    completed = [r.step for r in results if r.success]
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un planificateur. Le plan original a rencontre un probleme. Adapte le plan."),
        ("user", f"Tache originale: {task}\nEtapes completees: {completed}\nErreur: {error}\n\nNouveau plan pour finaliser la tache.")
    ])
    chain = prompt | planner_llm.with_structured_output(Plan)
    return chain.invoke({})

# Execution du workflow Plan-and-Execute
task = "Rediger un rapport sur les tendances IA Q1 2025 avec donnees marche"
plan = create_plan(task)
results = []

for step in plan.steps:
    try:
        result = execute_step(step, results)
        results.append(result)
        print(f"[OK] {step}")
    except Exception as e:
        print(f"[ERREUR] {step}: {e}")
        plan = replan(task, plan, results, str(e))
        break  # Recommencer avec le nouveau plan
```

### Quand utiliser Plan-and-Execute

Ideal pour : taches de plus de 7 etapes, workflows avec dependances claires entre etapes, quand le cout de l'execution doit etre optimise (planner cher, executor bon marche).

---

## Pattern 3 : Reflexion

### Principe

Reflexion (Shinn et al., 2023) ajoute une boucle d'auto-evaluation apres chaque tentative. L'agent produit une reponse, puis un critique (meme LLM ou LLM separe) evalue la qualite et suggere des ameliorations. L'agent itere jusqu'a satisfaction ou limite d'iterations.

### Implementation Python

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional

class Reflection(BaseModel):
    score: int = Field(ge=1, le=10, description="Score de qualite de 1 a 10")
    critique: str = Field(description="Points faibles identifies")
    suggestions: str = Field(description="Ameliorations specifiques a apporter")
    is_satisfactory: bool = Field(description="True si la reponse est acceptable")

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

def generate_response(task: str, previous_attempts: list) -> str:
    history = "\n\n".join([
        f"Tentative {i+1}:\n{a['response']}\nCritique: {a['critique']}"
        for i, a in enumerate(previous_attempts)
    ])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un expert. Produis une reponse de haute qualite. Si des tentatives precedentes existent, ameliore-les."),
        ("user", f"Tache: {task}\n\nHistorique:\n{history}\n\nNouvelle tentative (amelioree):")
    ])
    chain = prompt | llm
    return chain.invoke({}).content

def reflect(task: str, response: str) -> Reflection:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un critique expert. Evalue objectivement la reponse selon : exactitude, completude, clarte, actionabilite."),
        ("user", f"Tache originale: {task}\n\nReponse a evaluer:\n{response}\n\nEvalue et critique cette reponse.")
    ])
    chain = prompt | llm.with_structured_output(Reflection)
    return chain.invoke({})

# Boucle Reflexion
task = "Ecrire une politique de securite IA pour une entreprise financiere"
attempts = []
MAX_ITERATIONS = 3

for iteration in range(MAX_ITERATIONS):
    response = generate_response(task, attempts)
    reflection = reflect(task, response)

    print(f"Iteration {iteration+1} — Score: {reflection.score}/10")
    print(f"Critique: {reflection.critique}")

    attempts.append({
        "response": response,
        "critique": reflection.critique,
        "score": reflection.score
    })

    if reflection.is_satisfactory or reflection.score >= 8:
        print(f"Reponse satisfaisante apres {iteration+1} iteration(s)")
        final_response = response
        break
else:
    # Prendre la meilleure tentative
    best = max(attempts, key=lambda x: x["score"])
    final_response = best["response"]
```

---

## Pattern 4 : Tree of Thoughts (ToT)

### Principe

Tree of Thoughts (Yao et al., 2023) explore parallelement plusieurs chemins de raisonnement sous forme d'arbre. A chaque noeud, plusieurs pensees sont generees et evaluees. Les chemins prometteurs sont approfondis, les autres sont elagues (pruning). Optimal pour les problemes avec multiples solutions valides.

### Implementation Python

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
import asyncio

class ThoughtNode(BaseModel):
    thought: str
    score: float = Field(ge=0.0, le=1.0)
    children: List["ThoughtNode"] = []
    is_solution: bool = False

ThoughtNode.model_rebuild()

llm = ChatOpenAI(model="gpt-4o", temperature=0.8)  # Temperature haute pour diversite

async def generate_thoughts(problem: str, current_path: str, n: int = 3) -> List[str]:
    """Genere n pensees candidates a partir du chemin courant."""
    prompt = f"""Probleme: {problem}

Raisonnement jusqu'ici: {current_path}

Genere {n} etapes de raisonnement DIFFERENTES pour progresser vers la solution.
Format: une etape par ligne, prefixee par '- '"""
    response = await llm.ainvoke(prompt)
    thoughts = [
        line.strip("- ").strip()
        for line in response.content.split("\n")
        if line.strip().startswith("- ")
    ]
    return thoughts[:n]

async def evaluate_thought(problem: str, path: str) -> float:
    """Evalue la promesse d'un chemin de raisonnement (0 = mauvais, 1 = excellent)."""
    prompt = f"""Evalue ce chemin de raisonnement pour resoudre le probleme.
Probleme: {problem}
Chemin: {path}
Reponds UNIQUEMENT avec un score entre 0 et 1 (ex: 0.75)"""
    response = await llm.ainvoke(prompt)
    try:
        return float(response.content.strip())
    except ValueError:
        return 0.5

async def tree_of_thoughts(problem: str, depth: int = 3, branching: int = 3, beam_width: int = 2):
    """Exploration en largeur avec beam search."""
    # Initialisation : beam_width chemins de depart
    current_beam = [""]

    for level in range(depth):
        candidates = []
        for path in current_beam:
            thoughts = await generate_thoughts(problem, path, n=branching)
            for thought in thoughts:
                new_path = f"{path}\nEtape {level+1}: {thought}" if path else f"Etape 1: {thought}"
                score = await evaluate_thought(problem, new_path)
                candidates.append((new_path, score))

        # Garder les beam_width meilleurs chemins (pruning)
        candidates.sort(key=lambda x: x[1], reverse=True)
        current_beam = [path for path, score in candidates[:beam_width]]
        print(f"Niveau {level+1}: {len(candidates)} candidats → {beam_width} retenus")

    # Le meilleur chemin final
    best_path = current_beam[0]
    return best_path

# Utilisation
problem = "Concevoir une strategie de migration vers une architecture microservices pour un monolithe legacy"
result = asyncio.run(tree_of_thoughts(problem, depth=3, branching=3, beam_width=2))
```

**Quand utiliser ToT** : Problemes complexes avec multiples solutions valides (design, strategie), quand l'exploration exhaustive est justifiee par l'importance de la decision. Cout eleve en tokens — reserver aux decisions critiques.

---

## Systemes de Memoire

### Types de Memoire pour Agents

| Type | Description | Implmentation | Duree |
|------|-------------|---------------|-------|
| In-context | Messages dans la fenetre de contexte | Liste de messages | Session |
| External vector store | Embeddings dans une base vectorielle | ChromaDB, Pinecone | Persistante |
| Episodique | Historique d'interactions passees | Structured DB | Persistante |
| Semantique | Faits et connaissances stables | Knowledge graph, VectorDB | Permanente |

### Implementation avec ChromaDB

```python
import chromadb
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from datetime import datetime
import uuid

# Memoire externe persistante
chroma_client = chromadb.PersistentClient(path="./agent_memory")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

class AgentMemory:
    def __init__(self, collection_name: str = "agent_memories"):
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory="./agent_memory"
        )

    def store(self, content: str, metadata: dict = None):
        """Stocke une memoire avec timestamp automatique."""
        doc_id = str(uuid.uuid4())
        meta = {"timestamp": datetime.now().isoformat(), **(metadata or {})}
        self.vectorstore.add_texts(
            texts=[content],
            metadatas=[meta],
            ids=[doc_id]
        )
        return doc_id

    def recall(self, query: str, k: int = 5, filter: dict = None) -> list:
        """Recupere les memoires les plus pertinentes."""
        results = self.vectorstore.similarity_search_with_score(
            query=query, k=k, filter=filter
        )
        return [
            {"content": doc.page_content, "score": score, "metadata": doc.metadata}
            for doc, score in results
            if score < 0.7  # Seuil de pertinence (distance cosine)
        ]

    def forget(self, doc_id: str):
        """Supprime une memoire specifique (RGPD compliance)."""
        self.vectorstore.delete(ids=[doc_id])

# Utilisation dans un agent
memory = AgentMemory(collection_name="support_agent")

# Stockage apres interaction
memory.store(
    content="Client user_123 a eu un probleme de connexion SSO resolu en reinitialisant le token OAuth",
    metadata={"user_id": "user_123", "category": "auth", "resolved": True}
)

# Rappel lors d'une nouvelle interaction
relevant_memories = memory.recall(
    query="probleme de connexion utilisateur",
    k=3,
    filter={"resolved": True}
)
```

---

## Gestion des Erreurs et Resilience

### Retry avec Exponential Backoff

```python
import time
import random
from functools import wraps
from typing import Callable, Any

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple = (Exception,)
):
    """Decorateur pour retry avec backoff exponentiel et jitter."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jitter = random.uniform(0, delay * 0.1)
                    wait_time = delay + jitter
                    print(f"Tentative {attempt+1} echouee: {e}. Retry dans {wait_time:.1f}s")
                    time.sleep(wait_time)
        return wrapper
    return decorator

# Circuit Breaker Pattern
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit ouvert — service indisponible")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                print(f"Circuit ouvert apres {self.failure_count} echecs")
            raise
```

---

## Observabilite des Agents

### Logging Structure de Chaque Step

```python
import json
import time
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional, Any, Dict
from datetime import datetime

@dataclass
class AgentStep:
    step_id: str
    agent_id: str
    task_id: str
    step_type: str          # "thought", "tool_call", "tool_result", "final_answer"
    content: str
    tool_name: Optional[str] = None
    tool_input: Optional[Dict] = None
    tool_output: Optional[Any] = None
    tokens_used: int = 0
    latency_ms: float = 0
    cost_usd: float = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    error: Optional[str] = None

class AgentObservability:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.steps = []
        self.task_start_time = None

    def start_task(self, task_id: str, task_description: str):
        self.task_start_time = time.time()
        self.logger.info(json.dumps({
            "event": "task_started",
            "task_id": task_id,
            "task": task_description,
            "agent_id": self.agent_id
        }))

    def log_step(self, step: AgentStep):
        self.steps.append(step)
        self.logger.info(json.dumps(asdict(step)))

    def end_task(self, task_id: str, success: bool, final_answer: str):
        total_time = (time.time() - self.task_start_time) * 1000
        total_tokens = sum(s.tokens_used for s in self.steps)
        total_cost = sum(s.cost_usd for s in self.steps)

        metrics = {
            "event": "task_completed",
            "task_id": task_id,
            "agent_id": self.agent_id,
            "success": success,
            "total_steps": len(self.steps),
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 6),
            "total_latency_ms": round(total_time, 2),
            "steps_per_task": len(self.steps),
            "cost_per_task_usd": round(total_cost, 6)
        }
        self.logger.info(json.dumps(metrics))
        return metrics
```

---

## Evaluation des Agents

### Benchmarks Automatises et LLM-as-Judge

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from typing import List
import json

class EvaluationResult(BaseModel):
    task_id: str
    score: float = Field(ge=0.0, le=1.0)
    correctness: float = Field(ge=0.0, le=1.0)
    completeness: float = Field(ge=0.0, le=1.0)
    efficiency: float = Field(ge=0.0, le=1.0)
    reasoning: str

eval_llm = ChatOpenAI(model="gpt-4o", temperature=0)

def llm_as_judge(
    task: str,
    agent_response: str,
    reference_answer: str,
    steps_taken: int
) -> EvaluationResult:
    prompt = f"""Tu es un evaluateur expert d'agents IA. Evalue la reponse de l'agent.

TACHE: {task}
REPONSE AGENT: {agent_response}
REPONSE REFERENCE: {reference_answer}
NOMBRE D'ETAPES: {steps_taken}

Evalue selon:
- correctness: exactitude factuelle (0-1)
- completeness: tous les aspects couverts (0-1)
- efficiency: nombre d'etapes minimal (1.0 si optimal, penalite si excessif)
- score: moyenne ponderee globale"""

    chain = eval_llm.with_structured_output(EvaluationResult)
    return chain.invoke(prompt)

# Evaluation en batch sur un benchmark
def run_benchmark(agent_func, test_cases: List[dict]) -> dict:
    results = []
    for case in test_cases:
        start = time.time()
        try:
            response, steps = agent_func(case["task"])
            eval_result = llm_as_judge(
                task=case["task"],
                agent_response=response,
                reference_answer=case["expected"],
                steps_taken=steps
            )
            results.append({
                "task_id": case["id"],
                "score": eval_result.score,
                "success": eval_result.score > 0.7,
                "latency_s": time.time() - start
            })
        except Exception as e:
            results.append({"task_id": case["id"], "score": 0, "success": False, "error": str(e)})

    success_rate = sum(1 for r in results if r["success"]) / len(results)
    avg_score = sum(r["score"] for r in results) / len(results)
    return {"success_rate": success_rate, "avg_score": avg_score, "details": results}
```

---

## Arbre de Decision : Quel Pattern Choisir

```
Tache necessitant un agent ?
├─ NON → LLM simple suffisant (classification, generation, extraction)
└─ OUI
   ├─ Combien d'etapes estimees ?
   │   ├─ < 5 etapes → ReAct (simple, debuggable)
   │   └─ > 5 etapes
   │       ├─ Dependances fortes entre etapes ? → Plan-and-Execute
   │       └─ Tache exploratoire / incertaine → ReAct avec replanning
   │
   ├─ La qualite de sortie est-elle critique ?
   │   └─ OUI → Ajouter Reflexion (post-generation critique)
   │
   ├─ Probleme avec multiples solutions valides ?
   │   └─ OUI → Tree of Thoughts (si budget tokens disponible)
   │
   └─ Plusieurs domaines d'expertise requis ?
       └─ OUI → Multi-agents (voir reference multi-agent-frameworks)
```

### Regles Pratiques

- **Production B2C** : ReAct + guardrails stricts + human-in-the-loop pour actions irreversibles
- **Analyse et recherche** : Plan-and-Execute pour structurer, ReAct pour les sous-taches
- **Generation de contenu critique** : Reflexion obligatoire (au moins 2 iterations)
- **Decisions strategiques** : Tree of Thoughts pour explorer les options
- **Budget limite** : ReAct avec gpt-4o-mini pour l'execution, gpt-4o pour la critique

### Metriques de Performance Cibles

| Metrique | Acceptable | Bon | Excellent |
|----------|-----------|-----|-----------|
| Task success rate | > 60% | > 80% | > 90% |
| Steps per task | < 15 | < 10 | < 7 |
| Cost per task | < $0.10 | < $0.05 | < $0.02 |
| Latency P95 | < 60s | < 30s | < 15s |

Commencer par les benchmarks sur un jeu de test representatif avant de deployer en production. Ne jamais optimiser a l'aveugle — mesurer d'abord.
