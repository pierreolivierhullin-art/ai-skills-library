# LLMOps & Orchestration -- Frameworks, Agents, Cost Optimization, Observability & Fine-Tuning

## Introduction

**FR** -- Ce guide de reference couvre les operations LLM (LLMOps) et l'orchestration d'applications IA : frameworks d'orchestration (LangChain, LlamaIndex, Semantic Kernel, Vercel AI SDK), frameworks d'agents (tool use, multi-agents, CrewAI, AutoGen, Claude Code), protocole MCP, routage de modeles et fallback, optimisation des couts (caching, compression, batching), observabilite (LangSmith, Langfuse, Helicone), guardrails (NeMo Guardrails, Guardrails AI), strategies de fine-tuning (LoRA, QLoRA, distillation) et generation de donnees synthetiques. Ce document reflete l'etat de l'art 2024-2026.

**EN** -- This reference guide covers LLM operations (LLMOps) and AI application orchestration: orchestration frameworks (LangChain, LlamaIndex, Semantic Kernel, Vercel AI SDK), agent frameworks (tool use, multi-agent, CrewAI, AutoGen, Claude Code), MCP protocol, model routing and fallback, cost optimization (caching, compression, batching), observability (LangSmith, Langfuse, Helicone), guardrails (NeMo Guardrails, Guardrails AI), fine-tuning strategies (LoRA, QLoRA, distillation), and synthetic data generation. This document reflects the 2024-2026 state of the art.

---

## 1. Orchestration Frameworks

### LangChain

LangChain is the most widely adopted LLM orchestration framework, providing composable primitives for building LLM-powered applications.

**Core Concepts (LCEL -- LangChain Expression Language)**:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# LCEL chain -- composable with the pipe operator
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant specializing in {domain}."),
    ("user", "{question}")
])

model = ChatOpenAI(model="gpt-4o")
output_parser = StrOutputParser()

# Compose the chain
chain = prompt | model | output_parser

# Invoke
response = chain.invoke({"domain": "finance", "question": "What is EBITDA?"})

# Stream
async for chunk in chain.astream({"domain": "finance", "question": "What is EBITDA?"}):
    print(chunk, end="")
```

**RAG Chain with LangChain**:

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

# RAG chain composing retrieval and generation
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | ChatPromptTemplate.from_template(
        """Answer based on context:\n\n{context}\n\nQuestion: {question}"""
    )
    | model
    | StrOutputParser()
)

response = rag_chain.invoke("What is the return policy?")
```

**FR** -- LangChain a evolue significativement en 2024-2025. LCEL (LangChain Expression Language) remplace les anciennes Chain classes. Utiliser LCEL pour toute nouvelle implementation. Les anciennes APIs (LLMChain, SequentialChain) sont depreciees.

### LlamaIndex

LlamaIndex excels at data-centric RAG applications with sophisticated indexing and query capabilities.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Configure
Settings.llm = OpenAI(model="gpt-4o")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")

# Load and index documents
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)

# Query engine with re-ranking
from llama_index.core.postprocessor import SentenceTransformerRerank

reranker = SentenceTransformerRerank(model="cross-encoder/ms-marco-MiniLM-L-12-v2", top_n=5)

query_engine = index.as_query_engine(
    similarity_top_k=20,
    node_postprocessors=[reranker],
    response_mode="tree_summarize"
)

response = query_engine.query("What are the key risk factors?")
print(response.response)
print(response.source_nodes)  # Retrieved sources with scores
```

**EN** -- LlamaIndex provides superior data connectors (LlamaHub) for 160+ data sources, advanced query engines (sub-question, router, multi-step), and production-ready indexing with multiple vector store backends. Prefer LlamaIndex when the primary challenge is data ingestion and retrieval quality.

### Vercel AI SDK

The Vercel AI SDK is the leading choice for TypeScript/JavaScript LLM applications, with streaming-first design and React integration.

```typescript
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';
import { generateText, streamText, generateObject } from 'ai';
import { z } from 'zod';

// Simple text generation
const { text } = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Explain quantum computing in simple terms.',
});

// Streaming with React
const result = streamText({
  model: anthropic('claude-sonnet-4-20250514'),
  messages: conversationHistory,
});

// Structured output with Zod schema
const { object } = await generateObject({
  model: openai('gpt-4o'),
  schema: z.object({
    sentiment: z.enum(['positive', 'negative', 'neutral']),
    confidence: z.number().min(0).max(1),
    key_phrases: z.array(z.string()),
  }),
  prompt: `Analyze sentiment: "${userReview}"`,
});

// Tool use
const result = await generateText({
  model: anthropic('claude-sonnet-4-20250514'),
  tools: {
    getWeather: {
      description: 'Get current weather for a city',
      parameters: z.object({ city: z.string() }),
      execute: async ({ city }) => fetchWeather(city),
    },
  },
  prompt: 'What is the weather in Paris?',
});
```

**FR** -- Le Vercel AI SDK est le choix par defaut pour les applications Next.js / React. Il abstrait les differences entre providers (OpenAI, Anthropic, Google, Mistral) derriere une API unifiee. Le support streaming est natif et s'integre directement avec les composants React via le hook `useChat`.

### Semantic Kernel

Microsoft's Semantic Kernel provides LLM orchestration for .NET and Python with enterprise features.

```csharp
// C# -- Semantic Kernel
using Microsoft.SemanticKernel;

var kernel = Kernel.CreateBuilder()
    .AddAzureOpenAIChatCompletion("gpt-4o", endpoint, apiKey)
    .Build();

// Plugin with native function
kernel.Plugins.AddFromType<TimePlugin>();
kernel.Plugins.AddFromType<MathPlugin>();

// Auto-invoke functions (agent-like behavior)
var settings = new OpenAIPromptExecutionSettings {
    ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions
};

var result = await kernel.InvokePromptAsync(
    "What time will it be in 3 hours and 45 minutes?",
    new(settings)
);
```

**EN** -- Semantic Kernel is the natural choice for .NET enterprise environments. It integrates deeply with Azure AI services and provides abstractions that align with Microsoft's AI ecosystem. Use when building on Azure OpenAI Service.

### Framework Comparison Matrix

| Feature | LangChain | LlamaIndex | Vercel AI SDK | Semantic Kernel |
|---|---|---|---|---|
| **Language** | Python, JS | Python, JS | TypeScript | C#, Python, Java |
| **Primary Strength** | Composable chains, agents | Data indexing, RAG | Streaming, React integration | Enterprise, Azure |
| **Learning Curve** | Medium | Medium | Low | Medium |
| **Ecosystem Size** | Very large | Large | Growing | Medium |
| **Streaming** | Good | Good | Excellent (native) | Good |
| **Agent Support** | Strong (LangGraph) | Good (AgentRunner) | Good (tool use) | Good (Auto-invoke) |
| **Best For** | Complex multi-step pipelines | Data-heavy RAG | TypeScript web apps | .NET enterprise |

---

## 2. Agent Frameworks & Patterns

### Tool Use / Function Calling

The foundation of LLM agents: give the model access to external functions.

**Claude Tool Use**:

```python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "search_knowledge_base",
        "description": "Search the company knowledge base for information. Use this when the user asks about company policies, procedures, or products.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"},
                "category": {
                    "type": "string",
                    "enum": ["policies", "products", "procedures", "faq"],
                    "description": "Category to search within"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "create_ticket",
        "description": "Create a support ticket. Use only when the user explicitly requests to create a ticket or when the issue cannot be resolved through the knowledge base.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]}
            },
            "required": ["title", "description", "priority"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's our refund policy for digital products?"}]
)

# Process tool use in the response
for block in response.content:
    if block.type == "tool_use":
        tool_name = block.name
        tool_input = block.input
        # Execute the tool and feed result back
```

**FR** -- Ecrire des descriptions d'outils de haute qualite est aussi important que la conception du prompt. Des descriptions vagues ou ambigues menent a une mauvaise selection d'outils. Inclure des exemples d'utilisation dans la description. Specifier clairement quand utiliser ET quand ne PAS utiliser chaque outil.

### MCP (Model Context Protocol)

MCP standardizes the interface between LLM applications and external tools/data:

```json
// MCP Server definition
{
  "name": "database-mcp-server",
  "version": "1.0.0",
  "description": "Provides read-only access to the analytics database",
  "tools": [
    {
      "name": "query_analytics",
      "description": "Execute a read-only SQL query on the analytics database",
      "inputSchema": {
        "type": "object",
        "properties": {
          "sql": {
            "type": "string",
            "description": "SQL SELECT query (no mutations allowed)"
          }
        },
        "required": ["sql"]
      }
    }
  ],
  "resources": [
    {
      "uri": "analytics://schemas",
      "name": "Database Schema",
      "description": "Complete schema definition of the analytics database",
      "mimeType": "application/json"
    }
  ]
}
```

**EN** -- MCP (Model Context Protocol) is an open standard created by Anthropic for connecting LLMs to tools and data sources. It uses JSON-RPC over stdio or HTTP/SSE transport. MCP servers expose tools (functions the LLM can call), resources (data the LLM can read), and prompts (prompt templates). Claude Code, Claude Desktop, Cursor, and other clients support MCP natively. Prefer MCP for tool integration to achieve interoperability across LLM clients.

### Multi-Agent Frameworks

#### CrewAI

```python
from crewai import Agent, Task, Crew

# Define specialized agents
researcher = Agent(
    role="Senior Research Analyst",
    goal="Conduct thorough research on the given topic",
    backstory="Expert at finding and synthesizing information from multiple sources",
    tools=[search_tool, web_scraper],
    llm="claude-sonnet-4-20250514"
)

writer = Agent(
    role="Technical Writer",
    goal="Write clear, accurate technical content",
    backstory="Experienced technical writer specializing in making complex topics accessible",
    tools=[],
    llm="claude-sonnet-4-20250514"
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Ensure accuracy and completeness of content",
    backstory="Detail-oriented editor who catches errors and ensures factual accuracy",
    tools=[fact_check_tool],
    llm="gpt-4o"
)

# Define tasks
research_task = Task(
    description="Research the latest developments in quantum computing in 2025",
    agent=researcher,
    expected_output="Comprehensive research summary with sources"
)

writing_task = Task(
    description="Write a 1000-word article based on the research findings",
    agent=writer,
    context=[research_task],
    expected_output="Published-quality technical article"
)

review_task = Task(
    description="Review the article for factual accuracy and clarity",
    agent=reviewer,
    context=[writing_task],
    expected_output="Reviewed article with corrections applied"
)

# Execute the crew
crew = Crew(agents=[researcher, writer, reviewer], tasks=[research_task, writing_task, review_task])
result = crew.kickoff()
```

#### Claude Code as Agent Framework

Claude Code represents a production-grade agentic system with computer use and code execution:

```bash
# Claude Code can be invoked as an autonomous coding agent
claude --chat "Refactor the authentication module to use OAuth 2.0 PKCE flow"

# It autonomously:
# 1. Reads the existing codebase
# 2. Plans the refactoring
# 3. Implements changes across multiple files
# 4. Runs tests to validate
# 5. Requests human approval for critical changes
```

**FR** -- Les systemes multi-agents sont puissants mais complexes a debugger et a optimiser. Commencer par un agent unique avec des outils bien definis. N'evoluer vers le multi-agents que lorsque la complexite de la tache le justifie reellement. Le multi-agents multiplie les couts (chaque agent consomme des tokens) et les points de defaillance.

### Agent Safety Patterns

| Pattern | Implementation | Purpose |
|---|---|---|
| **Max iterations** | `max_iterations=10` | Prevent infinite loops |
| **Budget cap** | `max_cost_usd=1.00` per task | Prevent cost overruns |
| **Tool allowlisting** | Explicitly list permitted tools | Prevent unauthorized actions |
| **Human-in-the-loop** | Approval required for writes/deletes | Prevent destructive operations |
| **Scope constraints** | Restrict file paths, URLs, databases | Prevent unauthorized access |
| **Output validation** | Validate tool outputs before continuing | Prevent error cascading |
| **Audit logging** | Log every tool call with input/output | Enable post-hoc investigation |

---

## 3. Model Routing & Fallback

### Intelligent Model Routing

Route requests to different models based on complexity, cost, and latency requirements:

```python
# Pseudocode -- model routing
class ModelRouter:
    def __init__(self):
        self.simple_model = "claude-haiku-3.5"       # Fast, cheap
        self.standard_model = "claude-sonnet-4"       # Balanced
        self.powerful_model = "claude-opus-4"          # Maximum capability

    def route(self, request):
        complexity = self.classify_complexity(request)

        if complexity == "simple":
            # Classification, extraction, simple Q&A
            return self.simple_model
        elif complexity == "standard":
            # Analysis, summarization, code generation
            return self.standard_model
        else:
            # Complex reasoning, multi-step planning, critical decisions
            return self.powerful_model

    def classify_complexity(self, request):
        # Option 1: Rule-based (fast, no extra LLM call)
        if len(request) < 100 and any(kw in request.lower() for kw in ["classify", "extract", "translate"]):
            return "simple"

        # Option 2: Lightweight classifier (small model call)
        classification = self.simple_model.invoke(
            f"Classify this request as simple/standard/complex: {request[:200]}"
        )
        return classification
```

### Fallback Strategy

```python
# Pseudocode -- cascading fallback
async def invoke_with_fallback(prompt, models=None):
    if models is None:
        models = [
            {"provider": "anthropic", "model": "claude-sonnet-4-20250514"},
            {"provider": "openai", "model": "gpt-4o"},
            {"provider": "anthropic", "model": "claude-haiku-3.5"},
        ]

    for model_config in models:
        try:
            response = await call_model(model_config, prompt, timeout=30)
            if response.is_valid():
                return response
        except (TimeoutError, RateLimitError, APIError) as e:
            log.warning(f"Model {model_config['model']} failed: {e}")
            continue

    raise AllModelsFailed("All models in fallback chain failed")
```

**EN** -- Model routing and fallback are essential for production systems. They provide cost optimization (use cheap models when possible), reliability (fallback when primary model is unavailable), and latency optimization (fast models for simple tasks). Implement both routing and fallback for any production LLM application.

---

## 4. Cost Optimization

### Cost Optimization Strategies

| Strategy | Savings | Implementation Effort | Impact on Quality |
|---|---|---|---|
| **Prompt caching** | 80-90% on cached portions | Low | None |
| **Model routing** | 50-70% by using smaller models | Medium | Minimal if well-calibrated |
| **Prompt compression** | 20-40% fewer tokens | Medium | Minimal if well-done |
| **Response caching** | 100% on cache hits | Low | None (exact match) |
| **Batch API** | 50% cost (OpenAI) | Low | Latency increase (24h) |
| **Streaming cancellation** | Variable | Low | None |

### Prompt Caching (Anthropic)

```python
# Anthropic prompt caching -- long system prompts are cached server-side
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": long_system_prompt,  # 5000+ tokens -- cached after first call
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Short user query"}]
)
# First call: full price. Subsequent calls: 90% discount on cached tokens
# Time-to-first-token also reduced significantly
```

### Response Caching

```python
import hashlib
import json

class LLMCache:
    def __init__(self, redis_client, ttl_seconds=3600):
        self.redis = redis_client
        self.ttl = ttl_seconds

    def get_or_create(self, model, messages, **kwargs):
        # Create deterministic cache key
        cache_key = hashlib.sha256(
            json.dumps({"model": model, "messages": messages, **kwargs}, sort_keys=True).encode()
        ).hexdigest()

        # Check cache
        cached = self.redis.get(f"llm:{cache_key}")
        if cached:
            return json.loads(cached)

        # Generate and cache
        response = llm.invoke(model=model, messages=messages, **kwargs)
        self.redis.setex(f"llm:{cache_key}", self.ttl, json.dumps(response))
        return response
```

**FR** -- Le caching de reponses est efficace pour les requetes repetitives (FAQ, requetes communes). Utiliser des TTL adaptes au domaine : court pour les donnees volatiles (minutes), long pour les connaissances stables (heures/jours). Invalider le cache a chaque changement de prompt.

### Prompt Compression

Reduce token count without losing essential information:

```python
# Pseudocode -- LLMLingua-style prompt compression
from llmlingua import PromptCompressor

compressor = PromptCompressor(
    model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
    device_map="cpu"
)

compressed_prompt = compressor.compress_prompt(
    original_prompt,
    rate=0.5,          # Target 50% compression
    force_tokens=["important", "critical"],  # Never remove these tokens
)
# Use compressed_prompt for the LLM call
```

---

## 5. Observability

### LangSmith

LangSmith provides tracing, evaluation, and monitoring for LLM applications:

```python
# Enable LangSmith tracing (set environment variables)
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=ls_...
# LANGCHAIN_PROJECT=my-rag-app

from langsmith import traceable

@traceable(run_type="chain", name="rag_pipeline")
def rag_pipeline(question: str) -> str:
    docs = retrieve(question)         # Traced as a child span
    response = generate(question, docs)  # Traced as a child span
    return response

# Every call is traced with:
# - Input/output of each step
# - Latency per step
# - Token usage and cost
# - Parent-child span relationships
```

### Langfuse

Langfuse is an open-source LLM observability platform:

```python
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

langfuse = Langfuse()

@observe()
def rag_pipeline(question: str) -> str:
    # Retrieval step -- automatically traced
    docs = retrieve(question)

    # Generation step
    langfuse_context.update_current_observation(
        metadata={"num_docs": len(docs), "model": "claude-sonnet-4"}
    )
    response = generate(question, docs)

    # Add evaluation score
    langfuse_context.score_current_trace(
        name="user_satisfaction",
        value=1,  # From user feedback
    )
    return response
```

### Helicone

Helicone provides cost and usage monitoring as a proxy layer:

```python
# Helicone -- proxy-based monitoring (no code changes required)
from openai import OpenAI

client = OpenAI(
    base_url="https://oai.helicone.ai/v1",
    default_headers={
        "Helicone-Auth": "Bearer hlc_...",
        "Helicone-Property-Environment": "production",
        "Helicone-Property-Feature": "rag-pipeline",
    }
)
# All API calls are now monitored through Helicone
# Dashboard shows: cost, latency, token usage, error rates per property
```

### Observability Comparison

| Feature | LangSmith | Langfuse | Helicone |
|---|---|---|---|
| **Deployment** | Cloud only | Open-source / cloud | Cloud / self-host |
| **Tracing** | Deep (LangChain native) | Deep (framework-agnostic) | Request-level |
| **Evaluation** | Built-in evaluators | Score tracking | Basic |
| **Cost Tracking** | Per-trace | Per-trace | Per-request (excellent) |
| **Best For** | LangChain teams | Open-source preference | Cost monitoring |

**FR** -- L'observabilite est non-negociable pour les applications LLM en production. Sans traces, diagnostiquer un probleme de qualite est impossible. Choisir un outil et l'instrumenter des le debut du projet, pas apres le deploiement.

---

## 6. Guardrails

### NeMo Guardrails (NVIDIA)

NeMo Guardrails provides a programmable safety layer for LLM applications:

```python
# config.yml for NeMo Guardrails
models:
  - type: main
    engine: openai
    model: gpt-4o

rails:
  input:
    flows:
      - self check input         # Block prompt injections
      - check jailbreak          # Block jailbreak attempts

  output:
    flows:
      - self check output        # Block harmful outputs
      - check hallucination      # Detect hallucinated content
      - check sensitive data     # Block PII in responses
```

```colang
# Colang -- NeMo Guardrails policy language
define user ask about competitors
  "What do you think about competitor X?"
  "Is competitor Y better than us?"
  "Compare us with Z company"

define flow handle competitor questions
  user ask about competitors
  bot respond with neutral competitor policy
  "I'm designed to help with questions about our products and services.
   For competitor comparisons, I'd recommend checking independent review sites."
```

### Guardrails AI

```python
from guardrails import Guard
from guardrails.hub import ToxicLanguage, DetectPII, RestrictToTopic

# Create a guard with multiple validators
guard = Guard().use_many(
    ToxicLanguage(on_fail="exception"),
    DetectPII(pii_entities=["EMAIL", "PHONE", "SSN"], on_fail="fix"),
    RestrictToTopic(
        valid_topics=["customer support", "product information", "billing"],
        invalid_topics=["politics", "religion", "competitors"],
        on_fail="refrain"
    )
)

# Validate LLM output
result = guard(
    llm_api=openai.chat.completions.create,
    model="gpt-4o",
    messages=[{"role": "user", "content": user_query}],
)

if result.validation_passed:
    return result.validated_output
else:
    return "I'm unable to help with that request."
```

**EN** -- Layer guardrails at both input and output. Input guardrails catch malicious or out-of-scope requests before they reach the LLM. Output guardrails catch harmful, hallucinated, or non-compliant responses before they reach the user. For regulated industries (finance, healthcare, legal), guardrails are not optional.

---

## 7. Fine-Tuning Strategies

### When to Fine-Tune (Decision Framework)

```
1. Have you exhausted prompt engineering?
   +-- NO -> Optimize prompts first (zero-shot, few-shot, CoT, structured output)
   +-- YES -> Proceed to question 2

2. Have you tried RAG?
   +-- NO -> Implement RAG for knowledge-intensive tasks
   +-- YES -> Proceed to question 3

3. What is the goal of fine-tuning?
   +-- Consistent style/tone -> Fine-tune (good candidate)
   +-- Domain-specific knowledge -> RAG is usually better
   +-- Specific output format -> Try structured output APIs first
   +-- Reduce latency -> Fine-tune a smaller model
   +-- Reduce cost -> Fine-tune a smaller model to match larger model quality
   +-- Teach new capabilities -> Fine-tune (good candidate)
```

### LoRA (Low-Rank Adaptation)

LoRA freezes the base model and trains small adapter matrices, reducing trainable parameters by 99%+.

```python
# Pseudocode -- LoRA fine-tuning with PEFT
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer

# Load base model
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# Configure LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                          # Rank (higher = more expressive, more parameters)
    lora_alpha=32,                 # Scaling factor
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # Which layers to adapt
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 6,553,600 || all params: 8,030,261,248 || trainable%: 0.0816

# Train
trainer = Trainer(
    model=model,
    args=TrainingArguments(
        output_dir="./lora-output",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        warmup_steps=100,
        logging_steps=10,
        evaluation_strategy="steps",
        eval_steps=100,
    ),
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)
trainer.train()
```

### QLoRA (Quantized LoRA)

QLoRA combines 4-bit quantization with LoRA, enabling fine-tuning of large models on consumer GPUs:

```python
from transformers import BitsAndBytesConfig
import torch

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

# Load model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-70B-Instruct",
    quantization_config=bnb_config,
    device_map="auto"  # Automatic multi-GPU distribution
)

# Apply LoRA on top of quantized model
# (same LoRA config as above)
model = get_peft_model(model, lora_config)
# Now fine-tuning a 70B model on a single A100 80GB or 2x A100 40GB
```

**FR** -- QLoRA permet le fine-tuning de modeles de 70B parametres sur un seul GPU A100 80GB, contre 8+ A100 en pleine precision. La perte de qualite due a la quantisation 4-bit est generalement minime (< 1% sur les benchmarks). Toujours comparer le modele fine-tune QLoRA contre le modele de base en pleine precision sur votre dataset d'evaluation.

### API-Based Fine-Tuning

Major providers offer fine-tuning as a service:

```python
# OpenAI fine-tuning API
from openai import OpenAI
client = OpenAI()

# Upload training data (JSONL format)
file = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

# Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={
        "n_epochs": 3,
        "learning_rate_multiplier": 1.8,
        "batch_size": "auto"
    }
)

# Training data format (one per line in JSONL)
# {"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

### Knowledge Distillation

Train a smaller, cheaper model to mimic a larger model's behavior:

```python
# Pseudocode -- distillation pipeline
def generate_distillation_dataset(teacher_model, prompts, n=1000):
    """Generate training data by having the teacher model answer prompts."""
    training_data = []
    for prompt in prompts[:n]:
        # Get teacher's response
        teacher_response = teacher_model.invoke(prompt, temperature=0.3)

        training_data.append({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": teacher_response}
            ]
        })
    return training_data

# 1. Generate distillation dataset from GPT-4o / Claude Opus
dataset = generate_distillation_dataset(
    teacher_model=claude_opus,
    prompts=production_prompts
)

# 2. Fine-tune a smaller model on the distillation dataset
# Fine-tune GPT-4o-mini or Llama-3.1-8B on the dataset
# Result: smaller model that performs nearly as well as the teacher for your specific task
```

**EN** -- Distillation is the most cost-effective fine-tuning strategy. Use a powerful teacher model (Claude Opus, GPT-4o) to generate high-quality training data, then fine-tune a cheap student model (GPT-4o-mini, Llama-3.1-8B). This can reduce inference costs by 10-50x while retaining 90%+ of the teacher's quality on your specific task.

---

## 8. Synthetic Data Generation

### Generating Training Data with LLMs

```python
# Pseudocode -- synthetic data generation for fine-tuning
generation_prompt = """Generate a realistic customer support conversation about {topic}.

Requirements:
- The customer message should be natural and varied in style (formal, casual, frustrated, confused)
- The support agent response should be professional, accurate, and helpful
- Include specific details (product names, order numbers, dates) for realism
- The conversation should demonstrate good support practices

Topic: {topic}

Generate the conversation in this JSON format:
{{
    "customer_message": "...",
    "agent_response": "...",
    "category": "...",
    "sentiment": "...",
    "resolution_type": "..."
}}"""

topics = ["refund request", "product malfunction", "shipping delay", "account access", "billing error"]

synthetic_data = []
for topic in topics:
    for i in range(200):  # 200 examples per topic
        result = llm.invoke(generation_prompt.format(topic=topic), temperature=0.9)
        synthetic_data.append(result)

# CRITICAL: Validate synthetic data quality
# 1. Automated checks: JSON validity, required fields, reasonable lengths
# 2. Human review: sample 10-20% and verify quality
# 3. Deduplication: remove near-duplicate examples
# 4. Diversity check: ensure variety in style, complexity, and content
```

### Synthetic Data Quality Checklist

- Verify factual accuracy (especially for domain-specific data)
- Check for diversity in style, complexity, and content
- Remove duplicates and near-duplicates
- Validate JSON/format correctness
- Human review at least 10% of generated data
- Test fine-tuned model against held-out real data (not synthetic)
- Ensure no PII or sensitive information in generated data

**FR** -- Les donnees synthetiques sont un accelerateur puissant mais dangereux. Les LLMs generent des donnees plausibles mais parfois factuellement incorrectes. Toujours valider la qualite avec des humains et evaluer le modele fine-tune sur des donnees reelles, jamais sur des donnees synthetiques. Le biais du modele generateur se propage au modele fine-tune -- diversifier les modeles generateurs et les instructions pour mitiger ce risque.
