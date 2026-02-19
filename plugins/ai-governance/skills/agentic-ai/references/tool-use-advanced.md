# Tool Use Avance — MCP, RAG et Execution Securisee

## Model Context Protocol (MCP)

### Definition et Architecture

Le Model Context Protocol (MCP), developpe par Anthropic et ouvert en novembre 2024, est un standard ouvert qui definit comment les LLMs interagissent avec des sources de donnees et des outils externes. Il elimine le besoin d'integrations ad-hoc specifiques a chaque LLM.

Architecture MCP : **Client** (l'application LLM, ex: Claude Desktop, cursor, application custom) — **Server** (un processus qui expose des capacites) — **Transport** (stdio pour local, HTTP+SSE pour remote).

Un MCP server expose trois types de ressources :
- **Tools** : fonctions que le LLM peut appeler (actions avec effets)
- **Resources** : donnees que le LLM peut lire (fichiers, DB, APIs — lecture seule)
- **Prompts** : templates de prompts pre-configures

### Implementation d'un MCP Server

```python
# Installation : pip install mcp
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool, TextContent, Resource, ResourceTemplate,
    ListToolsResult, CallToolResult
)
import mcp.types as types
import json
import sqlite3
from pathlib import Path

# Initialisation du server MCP
app = Server("business-analytics-mcp")

# Connexion database (exemple)
DB_PATH = Path("./analytics.db")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Declare les tools disponibles pour le LLM client."""
    return [
        Tool(
            name="query_sales_data",
            description="""Interroge la base de donnees des ventes.
            Utiliser pour : chiffres de ventes, performances commerciales, trends.
            NE PAS utiliser pour : donnees RH, donnees financieres sensibles.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": "Requete SQL SELECT uniquement (pas de modification)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Nombre max de resultats (defaut: 100, max: 1000)",
                        "default": 100
                    }
                },
                "required": ["sql_query"]
            }
        ),
        Tool(
            name="send_slack_message",
            description="Envoie un message dans un canal Slack specifie. Confirmer avant toute utilisation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {"type": "string", "description": "Nom du canal (ex: #reporting)"},
                    "message": {"type": "string", "description": "Contenu du message Markdown"},
                    "urgency": {"type": "string", "enum": ["low", "normal", "high"]}
                },
                "required": ["channel", "message"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handler d'execution des tools."""

    if name == "query_sales_data":
        sql = arguments["sql_query"]
        limit = arguments.get("limit", 100)

        # Securite : bloquer les requetes de modification
        sql_upper = sql.strip().upper()
        if not sql_upper.startswith("SELECT"):
            return [TextContent(type="text", text="ERREUR: Seules les requetes SELECT sont autorisees")]

        # Injecter le LIMIT de securite
        if "LIMIT" not in sql_upper:
            sql = f"{sql} LIMIT {min(limit, 1000)}"

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.execute(sql)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            result = {"columns": columns, "rows": rows, "count": len(rows)}
            return [TextContent(type="text", text=json.dumps(result, default=str))]
        except Exception as e:
            return [TextContent(type="text", text=f"Erreur SQL: {str(e)}")]
        finally:
            conn.close()

    elif name == "send_slack_message":
        # Integration Slack SDK en production
        channel = arguments["channel"]
        message = arguments["message"]
        # slack_client.chat_postMessage(channel=channel, text=message)
        return [TextContent(type="text", text=f"Message envoye dans {channel}: '{message[:50]}...'")]

    return [TextContent(type="text", text=f"Tool inconnu: {name}")]

@app.list_resources()
async def list_resources() -> list[Resource]:
    """Expose des ressources en lecture seule."""
    return [
        Resource(
            uri="analytics://dashboard/kpis",
            name="KPIs Dashboard",
            description="KPIs business en temps reel",
            mimeType="application/json"
        )
    ]

# Point d'entree du server
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, InitializationOptions(
            server_name="business-analytics-mcp",
            server_version="1.0.0",
            capabilities=app.get_capabilities(notification_options=None, experimental_capabilities=None)
        ))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Exemples de MCP Servers Disponibles

- **filesystem** : lecture/ecriture fichiers locaux avec permissions granulaires
- **database** (PostgreSQL, SQLite, MySQL) : requetes SQL avec protections securite
- **web search** (Brave, Tavily) : recherche web integree
- **git** : operations git (log, diff, blame, status)
- **github/gitlab** : gestion PRs, issues, code review
- **notion/confluence** : acces bases de connaissance
- **slack** : lecture canaux, envoi messages

### Integration avec Claude Desktop

Configuration dans `~/.config/claude/claude_desktop_config.json` :

```json
{
  "mcpServers": {
    "business-analytics": {
      "command": "python",
      "args": ["/path/to/analytics_mcp_server.py"],
      "env": {
        "DB_PATH": "/path/to/analytics.db",
        "LOG_LEVEL": "INFO"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/user/Documents"]
    }
  }
}
```

---

## RAG Avance (Retrieval-Augmented Generation)

### Naive RAG vs Advanced RAG vs Modular RAG

**Naive RAG** : chunk fixe → embed → store → retrieve top-k → generate. Simple mais sous-optimal : chunking arbitraire coupe le sens, retrieval basique manque les documents pertinents, pas de post-processing.

**Advanced RAG** : ajout de pre-retrieval (query transformation) et post-retrieval (reranking, filtrage). Ameliore la precision de 20-40% selon les benchmarks.

**Modular RAG** : architecture flexible ou chaque composant (indexing, routing, retrieval, reranking, generation) est remplacable independamment. Standard pour les systemes production.

### Chunking Strategies

```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    SemanticChunker
)
from langchain_openai import OpenAIEmbeddings

# 1. Fixed-size chunking (baseline — rapide mais grossier)
fixed_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)

# 2. Semantic chunking (regroupe les phrases semantiquement proches)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
semantic_splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="percentile",  # ou "standard_deviation"
    breakpoint_threshold_amount=95           # Seuil de coupure semantique
)

# 3. Hierarchical chunking (parent-child pour contexte multi-echelle)
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_chroma import Chroma

parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)

vectorstore = Chroma(embedding_function=embeddings, collection_name="hierarchical")
docstore = InMemoryStore()

hierarchical_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)
# Recherche sur les chunks enfants (precis) mais retourne les chunks parents (contexte)
```

### Embedding Models — Dimensionnalite et Benchmark MTEB

| Modele | Dim | MTEB Score | Cout / 1M tokens | Cas d'usage |
|--------|-----|------------|------------------|-------------|
| text-embedding-3-small | 1536 | 62.3 | $0.02 | Production standard |
| text-embedding-3-large | 3072 | 64.6 | $0.13 | Haute precision |
| text-embedding-ada-002 | 1536 | 61.0 | $0.10 | Legacy (eviter) |
| Cohere embed-v3 | 1024 | 64.5 | $0.10 | Multilingual |
| BGE-m3 (open source) | 1024 | 64.3 | $0 | Self-hosted |
| E5-mistral-7b | 4096 | 66.6 | $0 | Self-hosted, SOTA |

**MTEB** (Massive Text Embedding Benchmark) : standard de facto pour comparer les modeles d'embedding sur 58 datasets.

### Reranking avec Cross-Encoder

```python
from sentence_transformers import CrossEncoder
from langchain_chroma import Chroma
from typing import List

# Cross-encoder : compare directement query + document (plus precis qu'embedding seul)
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_documents(query: str, documents: list, top_k: int = 5) -> list:
    """Reranke les documents par pertinence avec un cross-encoder."""
    if not documents:
        return []

    # Paires (query, document) pour scoring
    pairs = [[query, doc.page_content] for doc in documents]
    scores = cross_encoder.predict(pairs)

    # Tri par score decroissant
    ranked = sorted(
        zip(scores, documents),
        key=lambda x: x[0],
        reverse=True
    )
    return [doc for score, doc in ranked[:top_k]]

# Integration dans le pipeline RAG
def rag_with_reranking(query: str, vectorstore: Chroma, k_retrieve: int = 20, k_final: int = 5):
    """Retrieve large pool, rerank, return top-k."""
    # Etape 1 : retrieval large (recall maximal)
    initial_docs = vectorstore.similarity_search(query, k=k_retrieve)

    # Etape 2 : reranking (precision maximale)
    reranked_docs = rerank_documents(query, initial_docs, top_k=k_final)

    return reranked_docs
```

### Query Transformation

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 1. HyDE (Hypothetical Document Embeddings)
# Generer une reponse hypothetique, l'embedder pour trouver des documents similaires
def hyde_query(original_query: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Redige un passage de document factuel qui repondrait idealement a cette question. Sois precis et dense en information."),
        ("user", f"Question: {original_query}")
    ])
    chain = prompt | llm
    return chain.invoke({}).content

# 2. Multi-Query : genere plusieurs variantes de la question pour couvrir differents angles
def multi_query(original_query: str, n: int = 4) -> List[str]:
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"Genere {n} reformulations differentes de la question pour maximiser le recall de recherche documentaire. Une reformulation par ligne."),
        ("user", f"Question originale: {original_query}")
    ])
    chain = prompt | llm
    result = chain.invoke({}).content
    queries = [q.strip() for q in result.split("\n") if q.strip()]
    return [original_query] + queries[:n]

# 3. Step-back Prompting : generaliser la question pour trouver le contexte
def stepback_query(original_query: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Genere une question plus generale et conceptuelle qui fournirait le contexte necessaire pour repondre a la question specifique."),
        ("user", f"Question specifique: {original_query}\n\nQuestion generale:")
    ])
    chain = prompt | llm
    return chain.invoke({}).content
```

### Pipeline RAG Complet avec LangChain + ChromaDB

```python
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from sentence_transformers import CrossEncoder
import os

# Configuration
PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "knowledge_base"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-4o", temperature=0)
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Indexation des documents
def index_documents(docs_path: str):
    loader = DirectoryLoader(docs_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIR
    )
    print(f"{len(chunks)} chunks indexes dans ChromaDB")
    return vectorstore

# Chargement d'une collection existante
vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=PERSIST_DIR
)

# Prompt RAG
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """Tu es un assistant expert qui repond aux questions en te basant UNIQUEMENT sur le contexte fourni.
Si l'information n'est pas dans le contexte, dis-le explicitement plutot que d'halluciner.
Cite les sources pertinentes."""),
    ("user", """Contexte documentaire:
{context}

Question: {question}

Reponds de facon precise et cite les elements du contexte utilises.""")
])

def retrieve_and_rerank(query: str, k_retrieve: int = 20, k_final: int = 5) -> str:
    # Multi-query pour meilleur recall
    queries = multi_query(query, n=3)
    all_docs = []
    seen_ids = set()

    for q in queries:
        docs = vectorstore.similarity_search(q, k=k_retrieve // len(queries))
        for doc in docs:
            doc_id = hash(doc.page_content)
            if doc_id not in seen_ids:
                all_docs.append(doc)
                seen_ids.add(doc_id)

    # Reranking
    reranked = rerank_documents(query, all_docs, top_k=k_final)

    # Formatage du contexte
    return "\n\n---\n\n".join([
        f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
        for doc in reranked
    ])

# Pipeline RAG complet
rag_chain = (
    {"context": RunnableLambda(lambda x: retrieve_and_rerank(x["question"])),
     "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke({"question": "Quelles sont les obligations RGPD pour les agents IA ?"})
```

---

## Tool Composition et Chaining

### Tool Chaining Sequential

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
import json

@tool
def fetch_company_data(company_name: str) -> dict:
    """Recupere les donnees de base d'une entreprise (CA, effectifs, secteur)."""
    return {"name": company_name, "revenue_m": 450, "employees": 2300, "sector": "SaaS"}

@tool
def calculate_financial_ratios(revenue_m: float, employees: int) -> dict:
    """Calcule les ratios financiers cles depuis les donnees brutes."""
    return {
        "revenue_per_employee": round(revenue_m * 1000 / employees, 1),
        "efficiency_score": "high" if revenue_m / employees > 150 else "medium"
    }

@tool
def generate_benchmark_report(company_data: dict, ratios: dict) -> str:
    """Genere un rapport de benchmark textuel depuis les donnees et ratios."""
    return f"Rapport: {company_data['name']} — {ratios['revenue_per_employee']}K$/employe ({ratios['efficiency_score']} efficiency)"

# Parallel tool calls : le LLM peut appeler plusieurs tools en une inference
llm_with_tools = ChatOpenAI(model="gpt-4o").bind_tools(
    [fetch_company_data, calculate_financial_ratios, generate_benchmark_report],
    parallel_tool_calls=True  # Permet les appels simultanees
)

# Execution avec gestion des tool calls
def execute_tool_calls(messages):
    tools_map = {
        "fetch_company_data": fetch_company_data,
        "calculate_financial_ratios": calculate_financial_ratios,
        "generate_benchmark_report": generate_benchmark_report
    }
    response = llm_with_tools.invoke(messages)

    while response.tool_calls:
        tool_results = []
        for tc in response.tool_calls:
            tool_func = tools_map[tc["name"]]
            result = tool_func.invoke(tc["args"])
            tool_results.append(ToolMessage(
                content=json.dumps(result) if isinstance(result, dict) else str(result),
                tool_call_id=tc["id"]
            ))
        messages = messages + [response] + tool_results
        response = llm_with_tools.invoke(messages)

    return response.content
```

---

## Sandboxed Code Execution

### E2B Sandbox — Execution Securisee

```python
# pip install e2b-code-interpreter
from e2b_code_interpreter import Sandbox
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import json

@tool
def execute_python_code(code: str) -> str:
    """Execute du code Python dans un sandbox isole et securise.
    Utiliser pour : analyse de donnees, calculs, visualisations, transformations.
    Le sandbox est ephemere — aucune persistance entre les appels."""

    with Sandbox() as sandbox:
        # Upload de fichiers si necessaire
        # sandbox.files.write("/data/dataset.csv", csv_content)

        execution = sandbox.run_code(code)

        results = []

        # Capture des logs stdout
        if execution.logs.stdout:
            results.append("OUTPUT:\n" + "\n".join(execution.logs.stdout))

        # Capture des erreurs
        if execution.logs.stderr:
            results.append("ERRORS:\n" + "\n".join(execution.logs.stderr))

        # Capture des graphiques (base64)
        if execution.results:
            for result in execution.results:
                if result.type == "image/png":
                    results.append(f"[Graphique genere — {len(result.data)} bytes PNG]")
                elif result.type == "text/plain":
                    results.append(f"RESULT: {result.text}")

        return "\n\n".join(results) if results else "Execution completee sans output"

# Agent avec sandbox integration
data_analysis_agent = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools([execute_python_code])

task = """
Analyse ce dataset: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
1. Calcule la moyenne, mediane, ecart-type
2. Identifie le pattern mathematique
3. Genere les 5 valeurs suivantes
"""

result = execute_tool_calls([HumanMessage(content=task)])
```

### Docker Sandbox (Self-Hosted)

```python
import docker
import tempfile
import os

def execute_in_docker(code: str, timeout: int = 30) -> dict:
    """Execute du code Python dans un container Docker isole."""
    client = docker.from_env()

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        script_path = f.name

    try:
        container = client.containers.run(
            image="python:3.12-slim",       # Image minimale et securisee
            command=f"python /code/script.py",
            volumes={script_path: {"bind": "/code/script.py", "mode": "ro"}},
            network_disabled=True,          # Pas d'acces reseau
            mem_limit="256m",               # Limite memoire
            cpu_quota=50000,                # 50% d'un CPU max
            read_only=True,                 # Filesystem read-only
            security_opt=["no-new-privileges"],
            user="nobody",                  # Utilisateur non-root
            detach=False,
            remove=True,
            timeout=timeout
        )
        return {"success": True, "output": container.decode("utf-8")}
    except docker.errors.ContainerError as e:
        return {"success": False, "error": str(e)}
    finally:
        os.unlink(script_path)
```

---

## Structured Outputs — Validation Pydantic

```python
from pydantic import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
from typing import List, Optional
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SecurityAuditResult(BaseModel):
    overall_risk: RiskLevel
    vulnerabilities: List[str] = Field(
        description="Liste des vulnerabilites detectees",
        min_items=0,
        max_items=20
    )
    recommendations: List[str] = Field(
        description="Recommandations d'amelioration priorisees",
        min_items=1
    )
    compliance_score: int = Field(ge=0, le=100, description="Score de conformite 0-100")
    requires_immediate_action: bool

    @validator("recommendations")
    def recommendations_not_empty(cls, v):
        if not v:
            raise ValueError("Au moins une recommandation est requise")
        return v

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def audit_with_retry(code_snippet: str, max_retries: int = 3) -> SecurityAuditResult:
    """Audit avec retry automatique si le parsing echoue."""
    structured_llm = llm.with_structured_output(SecurityAuditResult, method="json_schema")

    for attempt in range(max_retries):
        try:
            result = structured_llm.invoke(
                f"Audite ce code pour les vulnerabilites de securite:\n\n{code_snippet}"
            )
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Parsing echoue (tentative {attempt+1}): {e}. Retry...")
    raise RuntimeError("Impossible d'obtenir un output structure apres retries")
```

---

## Tool Selection et Routing

### Qualite des Descriptions de Tools

La description d'un tool determine si le LLM le selectionnera correctement. Une mauvaise description est la cause numero un des erreurs de tool selection.

**Mauvaise description** : `def get_data(query: str) -> str: """Recupere des donnees."""`

**Bonne description** :
```python
@tool
def query_customer_database(
    customer_id: str,
    fields: list[str] = ["name", "email", "subscription_tier", "created_at"]
) -> dict:
    """Recupere les informations d'un client specifique depuis la CRM.

    UTILISER QUAND : l'utilisateur demande des informations sur UN client specifique
    identifie par son ID.

    NE PAS UTILISER POUR :
    - Lister plusieurs clients (utiliser search_customers)
    - Des statistiques agregees (utiliser get_customer_analytics)
    - La verif d'email (utiliser validate_email)

    EXEMPLES D'INPUTS VALIDES :
    - customer_id: "cust_abc123", fields: ["name", "subscription_tier"]
    - customer_id: "user_xyz789"

    RETOURNE : dict avec les champs demandes, ou KeyError si client introuvable."""
    pass
```

### Routing Layer avec Classification

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Literal

class ToolRoute(BaseModel):
    selected_tool: Literal[
        "query_sales_db",
        "query_hr_db",
        "query_finance_db",
        "web_search",
        "none"
    ]
    confidence: float = Field(ge=0, le=1)
    reasoning: str

router_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def route_to_tool(user_query: str) -> ToolRoute:
    """Determine le tool approprie avant l'appel LLM principal — economise des tokens."""
    prompt = f"""Analyse la requete et selectionne le tool le plus approprie.

TOOLS DISPONIBLES:
- query_sales_db: chiffres de ventes, clients, commandes, revenus
- query_hr_db: employes, salaires, conges, organigramme
- query_finance_db: comptabilite, tresorerie, bilan, P&L
- web_search: informations externes, actualites, concurrents
- none: requete qui ne necessite pas d'acces donnees

REQUETE: {user_query}

Selectionne le tool et explique en une phrase."""

    chain = router_llm.with_structured_output(ToolRoute)
    return chain.invoke(prompt)

# Utilisation dans un agent optimise
route = route_to_tool("Quel est notre chiffre d'affaires du dernier trimestre ?")
print(f"Tool: {route.selected_tool} (confiance: {route.confidence:.0%})")
# Output: Tool: query_sales_db (confiance: 95%)
```

---

## Checklist Tool Use Production

Avant de deployer un systeme avec tools en production, verifier :

- [ ] Chaque tool a une description precise avec cas d'usage et contre-exemples
- [ ] Les tools destructifs (DELETE, email, paiement) ont un mecanisme de confirmation
- [ ] Execution dans sandbox ou environnement isole pour le code dynamique
- [ ] Rate limiting par tool pour eviter les appels abusifs
- [ ] Logging de chaque appel tool (input, output, latence, cout)
- [ ] Timeout configure sur chaque tool (defaut recommande : 30s)
- [ ] Gestion explicite des erreurs : que faire si le tool echoue ?
- [ ] Tests automatises sur les tools avant integration (unit tests)
- [ ] Monitoring en production : taux d'echec par tool, top tools appeles
- [ ] Review reguliere des logs pour detecter les utilisations anormales
