# RAG Architecture -- Retrieval-Augmented Generation Patterns & Best Practices

## Introduction

**FR** -- Ce guide de reference couvre l'ensemble des architectures RAG (Retrieval-Augmented Generation), des implementations naives aux systemes avances et modulaires. Il traite en detail les strategies de chunking, les modeles d'embeddings, la recherche vectorielle, la recherche hybride, les techniques avancees (re-ranking, HyDE, self-RAG, CRAG) et les metriques d'evaluation. Le RAG est la technique fondamentale pour ancrer les LLMs dans la connaissance factuelle et a jour. Ce document reflete l'etat de l'art 2024-2026.

**EN** -- This reference guide covers the full spectrum of RAG (Retrieval-Augmented Generation) architectures, from naive implementations to advanced and modular systems. It covers chunking strategies, embedding models, vector search, hybrid search, advanced techniques (re-ranking, HyDE, self-RAG, CRAG), and evaluation metrics in detail. RAG is the foundational technique for grounding LLMs in factual, up-to-date knowledge. This document reflects the 2024-2026 state of the art.

---

## 1. RAG Architecture Patterns

### Naive RAG

The simplest RAG pipeline: chunk documents, embed chunks, store in a vector database, retrieve by similarity, generate with context.

```
Ingestion Pipeline:
Documents -> Chunking -> Embedding -> Vector Store

Query Pipeline:
User Query -> Embedding -> Vector Search (top-k) -> Prompt Assembly -> LLM Generation -> Response
```

**Implementation**:

```python
# Pseudocode -- Naive RAG pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Ingestion
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)
vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())

# Query
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
relevant_docs = retriever.invoke("What is the company's return policy?")

prompt = f"""Answer the question based on the following context.

Context:
{format_docs(relevant_docs)}

Question: What is the company's return policy?

Answer:"""

response = llm.invoke(prompt)
```

**Limitations** / **Limites** :
- Retrieval quality is limited by naive chunking and single-pass vector similarity.
- No handling of multi-hop questions requiring information from multiple documents.
- No query understanding or reformulation.
- Sensitive to chunk size: too small loses context, too large dilutes relevance.

### Advanced RAG

Layer optimization techniques on top of naive RAG to improve retrieval and generation quality:

```
User Query
  -> Query Analysis (classification, decomposition)
  -> Query Transformation (expansion, HyDE, rewriting)
  -> Hybrid Retrieval (dense + sparse search)
  -> Re-ranking (cross-encoder)
  -> Context Compression
  -> Prompt Assembly with citations
  -> LLM Generation
  -> Answer Validation (self-RAG, CRAG)
  -> Response with sources
```

### Modular RAG

A production architecture with pluggable, independently configurable components:

```
                    +-- Query Router (routes to appropriate index/strategy)
                    |
User Query -----> Query Module ---> Retrieval Module ---> Post-Retrieval Module ---> Generation Module
                    |                     |                      |                         |
               - Classification      - Multi-index          - Re-ranking              - Prompt assembly
               - Decomposition       - Dense search         - Compression             - Citation injection
               - HyDE                - Sparse search        - Deduplication           - Answer generation
               - Rewriting           - Hybrid fusion        - Filtering               - Self-verification
                                     - Knowledge graph
```

**FR** -- L'architecture modulaire est la cible pour les systemes de production. Chaque module peut etre evalue, optimise et remplace independamment. Commencer par le RAG naif pour valider le use case, puis ajouter progressivement les modules avances en mesurant l'impact de chaque ajout.

---

## 2. Chunking Strategies

### Fixed-Size Chunking

Split documents into chunks of N tokens/characters with overlap.

```python
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(
    chunk_size=1000,      # characters
    chunk_overlap=200,    # overlap between consecutive chunks
    separator="\n"
)
```

**When to use**: Simple documents with uniform structure. Fast to implement. Baseline strategy. / **Quand l'utiliser** : Documents simples avec une structure uniforme. Rapide a implementer. Strategie de base.

### Recursive Character Splitting

Recursively split on a hierarchy of separators (\n\n, \n, " ", "") to respect natural text boundaries.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)
```

**EN** -- This is the default recommendation for most use cases. It preserves paragraph and sentence boundaries better than fixed-size splitting.

### Semantic Chunking

Split based on semantic similarity between sentences. Group semantically related sentences into chunks.

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",  # or "standard_deviation", "interquartile"
    breakpoint_threshold_amount=95
)
```

**How it works**: Embed each sentence, compute cosine distance between consecutive sentences, split where the distance exceeds a threshold (semantic shift). / **Fonctionnement** : Incorporer chaque phrase, calculer la distance cosinus entre phrases consecutives, couper la ou la distance depasse un seuil (changement semantique).

### Parent-Child (Hierarchical) Chunking

Store both large parent chunks and small child chunks. Retrieve by matching small chunks, but return the parent chunk for context.

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.storage import InMemoryStore

parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=InMemoryStore(),
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)
```

**EN** -- This strategy solves the fundamental tension between retrieval precision (small chunks match better) and generation quality (large chunks provide more context). Use for knowledge bases where context surrounding the matched passage is important.

### Document-Aware Chunking

Respect document structure: split by headers, sections, tables, code blocks.

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "header_1"),
    ("##", "header_2"),
    ("###", "header_3"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
splits = splitter.split_text(markdown_document)
# Each split retains the header hierarchy as metadata
```

For HTML, PDF, and other structured formats, use specialized parsers (Unstructured, LlamaParse, Docling) that extract structure before chunking.

**FR** -- Pour les documents structures (rapports, documentation technique, contrats juridiques), le chunking document-aware est nettement superieur au chunking generique. Utiliser des parseurs specialises (Unstructured, LlamaParse, Docling) pour extraire la structure avant de chunker.

### Chunking Strategy Decision Guide

| Strategy | Best For | Complexity | Quality |
|---|---|---|---|
| Fixed-size | Prototyping, uniform text | Low | Baseline |
| Recursive character | General-purpose text | Low | Good |
| Semantic | Varied topic density | Medium | Better |
| Parent-child | Knowledge bases needing context | Medium | Better |
| Document-aware | Structured documents (HTML, Markdown, PDF) | Medium-High | Best |
| Agentic chunking | Complex multi-format corpora | High | Best |

---

## 3. Embedding Models

### Model Selection Guide (2024-2026)

| Model | Dimensions | Max Tokens | Strengths | Use Case |
|---|---|---|---|---|
| **OpenAI text-embedding-3-large** | 3072 (configurable) | 8191 | High quality, dimension reduction | General-purpose, multilingual |
| **OpenAI text-embedding-3-small** | 1536 (configurable) | 8191 | Cost-efficient | High-volume, cost-sensitive |
| **Cohere embed-v3** | 1024 | 512 | Strong multilingual, compression | Multilingual RAG |
| **Voyage AI voyage-3** | 1024 | 32000 | Long context, code understanding | Code search, long documents |
| **BGE-M3 (BAAI)** | 1024 | 8192 | Open-source, multi-lingual, hybrid | Self-hosted, privacy-sensitive |
| **Jina embeddings v3** | 1024 | 8192 | Open-source, multilingual, task-specific | Self-hosted, flexible |
| **Google Gemini Embedding** | 768 | 2048 | Multimodal (text + image) | Cross-modal search |

### Embedding Best Practices

1. **Match the embedding model to the use case**. Code search needs code-aware embeddings (Voyage). Legal text needs domain-adapted embeddings.
2. **Use asymmetric embeddings** when available. Embed queries differently from documents (Cohere, some models support query vs document prefixes).
3. **Normalize embeddings** for cosine similarity. Most models output normalized vectors, but verify.
4. **Consider dimension reduction**. OpenAI text-embedding-3 supports Matryoshka representations -- reduce dimensions (e.g., 3072 -> 1024) for faster search with minimal quality loss.
5. **Benchmark on your data**. Public benchmarks (MTEB) are useful but your domain may differ significantly. Always evaluate on a representative sample of your actual queries and documents.
6. **Batch embedding requests** for ingestion. Most APIs support batch endpoints that are cheaper and faster.

**FR** -- Ne pas choisir un modele d'embedding sur la seule base des benchmarks publics (MTEB). Evaluer sur un echantillon representatif de vos donnees reelles. La performance varie considerablement selon le domaine, la langue et la longueur des textes.

---

## 4. Vector Databases & Search

### Vector Database Comparison (2024-2026)

| Database | Type | Strengths | Best For |
|---|---|---|---|
| **Pinecone** | Managed cloud | Serverless, auto-scaling, metadata filtering | Production SaaS, no-ops |
| **Weaviate** | Open-source / cloud | Hybrid search built-in, modules, multi-tenancy | Hybrid search, modular |
| **Qdrant** | Open-source / cloud | Rust performance, rich filtering, quantization | High-performance, self-hosted |
| **Chroma** | Open-source | Simple API, embedded mode, great for prototyping | Prototyping, local development |
| **Milvus / Zilliz** | Open-source / cloud | Massive scale, GPU acceleration | Very large datasets |
| **pgvector (PostgreSQL)** | Extension | Use existing Postgres, HNSW/IVFFlat indexes | Teams already on PostgreSQL |
| **Elasticsearch 8+** | Open-source / cloud | Hybrid search (dense + BM25), mature ecosystem | Existing Elasticsearch users |

### Hybrid Search (Dense + Sparse)

Combine dense vector search (semantic similarity) with sparse keyword search (BM25) for superior retrieval.

```python
# Pseudocode -- hybrid search with reciprocal rank fusion
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# Dense retriever (semantic)
dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# Sparse retriever (keyword)
bm25_retriever = BM25Retriever.from_documents(documents, k=10)

# Combine with reciprocal rank fusion
ensemble_retriever = EnsembleRetriever(
    retrievers=[dense_retriever, bm25_retriever],
    weights=[0.6, 0.4]  # Favor dense search, supplement with keyword
)

results = ensemble_retriever.invoke("quarterly revenue growth rate")
```

**EN** -- Hybrid search consistently outperforms pure dense or pure sparse search in benchmarks and production systems. Dense search captures semantic meaning ("revenue growth" matches "income increase"). Sparse search captures exact terms ("Q3 2025", product names, acronyms). The combination covers both.

**FR** -- La recherche hybride surpasse systematiquement la recherche dense pure ou sparse pure. La recherche dense capture le sens semantique. La recherche sparse capture les termes exacts. La combinaison couvre les deux aspects.

### Metadata Filtering

Always store and leverage metadata for filtering:

```python
# Store chunks with rich metadata
vectorstore.add_documents([
    Document(
        page_content="Revenue grew 15% year-over-year...",
        metadata={
            "source": "annual_report_2025.pdf",
            "page": 42,
            "section": "Financial Highlights",
            "year": 2025,
            "document_type": "annual_report",
            "access_level": "public"
        }
    )
])

# Retrieve with metadata filters
results = vectorstore.similarity_search(
    query="revenue growth",
    k=5,
    filter={"year": 2025, "document_type": "annual_report"}
)
```

---

## 5. Advanced RAG Techniques

### Re-Ranking

Use a cross-encoder model to re-score retrieved documents. Cross-encoders jointly encode the query and document, producing much more accurate relevance scores than bi-encoder similarity.

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

# First-stage retrieval: fast, broad (top-20)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

# Second-stage: cross-encoder re-ranking (narrow to top-5)
reranker = CohereRerank(model="rerank-v3.5", top_n=5)
retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=base_retriever
)

results = retriever.invoke("What are the key risk factors?")
```

**Reranking models (2024-2026)**: Cohere Rerank v3.5, Jina Reranker v2, BGE Reranker v2, Voyage Rerank, flashrank (open-source lightweight). / **Modeles de re-ranking (2024-2026)** : Cohere Rerank v3.5, Jina Reranker v2, BGE Reranker v2, Voyage Rerank, flashrank (open-source leger).

**EN** -- Re-ranking is the single highest-impact technique for improving RAG quality. It typically improves retrieval precision by 15-30% with minimal latency overhead (50-100ms). Always implement re-ranking in production RAG systems.

### Query Expansion

Generate multiple variations of the query to improve recall:

```python
# Pseudocode -- multi-query retrieval
expansion_prompt = """Generate 3 alternative versions of this question that might
help retrieve relevant documents. Make each version approach the topic from a
different angle.

Original question: {question}

Alternative questions:"""

alternative_queries = llm.invoke(expansion_prompt)
# Retrieve for each query variant, then deduplicate and merge results
```

### HyDE (Hypothetical Document Embeddings)

Generate a hypothetical answer, embed it, and use that embedding for retrieval. The hypothesis is closer in embedding space to real answers than the original query.

```python
# Step 1: Generate a hypothetical answer
hyde_prompt = """Answer the following question with a detailed, factual response.
It's okay if you're not completely sure -- generate your best answer.

Question: {question}

Answer:"""

hypothetical_answer = llm.invoke(hyde_prompt)

# Step 2: Embed the hypothetical answer (not the original query)
hyde_embedding = embedding_model.embed_query(hypothetical_answer)

# Step 3: Search using the hypothetical answer embedding
results = vectorstore.similarity_search_by_vector(hyde_embedding, k=5)
```

**FR** -- HyDE est particulierement efficace quand les requetes utilisateur sont courtes ou vagues ("comment ca marche ?") et que les documents cibles sont longs et detailles. La reponse hypothetique "parle le meme langage" que les documents, ameliorant la correspondance semantique.

### Self-RAG (Self-Reflective RAG)

The model evaluates its own retrieval and generation at each step, deciding whether to retrieve more, when to use retrieved context, and whether its answer is supported.

```
Step 1: Given the query, decide if retrieval is needed.
  -> If the query can be answered from model knowledge alone, skip retrieval.
  -> If retrieval is needed, proceed to Step 2.

Step 2: Retrieve documents and evaluate relevance.
  -> For each retrieved document, score: RELEVANT / PARTIALLY_RELEVANT / IRRELEVANT
  -> Keep only RELEVANT and PARTIALLY_RELEVANT documents.

Step 3: Generate answer using relevant documents.

Step 4: Self-evaluate the answer:
  -> Is the answer fully supported by the retrieved documents? (SUPPORTED / PARTIALLY_SUPPORTED / NOT_SUPPORTED)
  -> Is the answer useful and complete? (USEFUL / PARTIALLY_USEFUL / NOT_USEFUL)
  -> If NOT_SUPPORTED or NOT_USEFUL, retry with modified query or additional retrieval.
```

### CRAG (Corrective RAG)

Evaluate retrieved documents and take corrective action when retrieval quality is poor:

```
Step 1: Retrieve documents for the query.

Step 2: Evaluate retrieval quality with a lightweight classifier:
  -> CORRECT: Documents are relevant and sufficient -> proceed to generation
  -> AMBIGUOUS: Documents are partially relevant -> refine query and retrieve again
  -> INCORRECT: Documents are irrelevant -> fall back to web search or broader retrieval

Step 3: For CORRECT: use retrieved documents directly.
        For AMBIGUOUS: extract relevant parts, discard irrelevant, supplement with additional retrieval.
        For INCORRECT: perform web search, retrieve from alternative sources, or acknowledge insufficient data.

Step 4: Generate answer with quality-assured context.
```

**EN** -- Self-RAG and CRAG represent the cutting edge of RAG quality assurance (2024-2026). They add 1-2 additional LLM calls per query but significantly improve faithfulness by ensuring the model only uses high-quality retrieved context. Implement for high-stakes applications where hallucination is unacceptable.

### Iterative / Multi-Hop Retrieval

For complex questions requiring information from multiple sources, retrieve iteratively:

```python
# Pseudocode -- iterative retrieval for multi-hop questions
def iterative_rag(question, max_hops=3):
    context = []
    current_query = question

    for hop in range(max_hops):
        # Retrieve for current query
        docs = retriever.invoke(current_query)
        context.extend(docs)

        # Check if we have enough information
        sufficiency_check = llm.invoke(f"""
        Given the question: {question}
        And the collected context: {format_docs(context)}

        Do you have sufficient information to answer the question completely?
        If YES, provide the answer.
        If NO, what specific information is still missing? Formulate a follow-up query.
        """)

        if sufficiency_check.has_answer:
            return sufficiency_check.answer
        else:
            current_query = sufficiency_check.follow_up_query

    # Final attempt with all collected context
    return llm.invoke(f"Answer based on all context: {format_docs(context)}\n\nQuestion: {question}")
```

---

## 6. RAG Evaluation

### Retrieval Metrics

| Metric | What It Measures | Formula | Target |
|---|---|---|---|
| **Precision@k** | Fraction of retrieved docs that are relevant | relevant_in_top_k / k | > 0.7 |
| **Recall@k** | Fraction of all relevant docs that are retrieved | relevant_in_top_k / total_relevant | > 0.8 |
| **MRR (Mean Reciprocal Rank)** | Average rank of the first relevant result | mean(1/rank_of_first_relevant) | > 0.6 |
| **NDCG@k** | Quality of ranking considering position | Discounted cumulative gain, normalized | > 0.7 |
| **Hit Rate** | Fraction of queries with at least one relevant result in top-k | queries_with_hit / total_queries | > 0.9 |

### Generation Metrics (RAGAS Framework)

| Metric | What It Measures | How |
|---|---|---|
| **Faithfulness** | Is the answer supported by the retrieved context? | LLM judges if each claim in the answer is in the context |
| **Answer Relevancy** | Does the answer address the question? | LLM scores relevance of answer to question |
| **Context Relevancy** | Are the retrieved documents relevant to the question? | LLM scores relevance of each retrieved doc |
| **Context Recall** | Does the context contain the information needed for the ground truth answer? | LLM compares context against ground truth |

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset

# Prepare evaluation dataset
eval_data = Dataset.from_dict({
    "question": ["What is the return policy?", ...],
    "answer": [rag_pipeline("What is the return policy?"), ...],
    "contexts": [retrieved_contexts, ...],
    "ground_truth": ["Items can be returned within 30 days...", ...]
})

results = evaluate(
    eval_data,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)
print(results)
# {'faithfulness': 0.87, 'answer_relevancy': 0.91, 'context_precision': 0.78, 'context_recall': 0.83}
```

### End-to-End Evaluation Workflow

1. **Create a golden dataset**: 50-200 (question, ground_truth_answer, relevant_document_ids) triples. Include easy, medium, and hard questions. Include adversarial questions (unanswerable, ambiguous, multi-hop).
2. **Evaluate retrieval independently**: Measure precision@k, recall@k, MRR, NDCG before connecting retrieval to generation.
3. **Evaluate generation with RAGAS**: Measure faithfulness, answer relevancy, context precision, context recall.
4. **Evaluate end-to-end**: Measure overall answer correctness, latency, and cost per query.
5. **A/B test changes**: Never deploy RAG changes without A/B comparison against the current system on the golden dataset.

**FR** -- Evaluer le RAG en deux etapes distinctes : d'abord la qualite de la recherche (metriques de retrieval), puis la qualite de la generation (metriques RAGAS). Cela permet de diagnostiquer precisement si un probleme vient de la recherche ou de la generation. Toujours maintenir un dataset d'evaluation dore et le faire grandir continuellement avec les cas difficiles rencontres en production.

---

## 7. Production RAG Patterns

### Citation and Source Attribution

Always return sources with generated answers:

```python
rag_prompt = """Answer the question based on the provided context. For each claim in your
answer, include a citation in the format [Source N] where N corresponds to the context number.

Context 1 (annual_report_2025.pdf, page 12):
{context_1}

Context 2 (quarterly_update_q3.pdf, page 5):
{context_2}

Question: {question}

Provide your answer with inline citations:"""
```

### Guardrails for RAG

1. **Retrieval threshold**: Do not generate if no retrieved document exceeds a minimum relevance score. Return "I don't have enough information to answer this question" instead.
2. **Source freshness**: Filter out documents older than a configurable threshold for time-sensitive queries.
3. **Access control**: Apply user permissions at retrieval time. Never return documents the user is not authorized to see.
4. **Answer confidence**: Use Self-RAG or a separate classifier to assess answer confidence. Flag low-confidence answers for human review.

### Scaling RAG for Production

- **Index sharding**: Partition large indices by document type, date range, or tenant for faster search.
- **Caching**: Cache frequent query embeddings and results. Use TTL-based invalidation.
- **Async ingestion**: Process new documents asynchronously. Use a queue (SQS, Kafka) for the ingestion pipeline.
- **Monitoring**: Track retrieval latency, relevance scores, and generation quality in production. Alert on degradation.
- **Incremental updates**: Support document addition, update, and deletion without full reindexing.

**EN** -- Production RAG systems must handle document freshness, access control, scalability, and monitoring. Design the ingestion pipeline for incremental updates from day one. Implement comprehensive observability to detect quality regressions before users report them.
