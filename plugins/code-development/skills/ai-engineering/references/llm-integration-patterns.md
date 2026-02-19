# LLM Integration Patterns — RAG Architecture, Embeddings, Vector Databases, Prompt Engineering for Developers, Structured Output

## Overview

Ce document de référence couvre les patterns d'intégration LLM en production : architecture RAG complète, modèles d'embeddings, bases vectorielles, stratégies de chunking, prompt engineering pour développeurs, structured output, gestion des context windows, patterns d'API LLM, caching et techniques état de l'art 2025-2026. Utiliser ce guide comme fondation pour toute décision d'intégration LLM.

---

## 1. RAG Architecture Detailed

### Pipeline complet

Le pipeline RAG se décompose en deux flux distincts — ingestion (offline) et requête (online) — avec sept étapes fondamentales :

```
INGESTION PIPELINE (offline / batch)

Documents (PDF, HTML, MD, DB)
  --> Parsing & Extraction (Unstructured, Docling, LlamaParse)
  --> Chunking (stratégie adaptée au type de document)
  --> Enrichissement métadonnées (source, date, section, langue)
  --> Embedding (modèle vectoriel)
  --> Indexation (vector database + index inversé)

QUERY PIPELINE (online / temps réel)

User Query
  --> Query Analysis (classification, détection d'intention)
  --> Query Transformation (expansion, HyDE, décomposition multi-hop)
  --> Retrieval (recherche hybride dense + sparse, metadata filtering)
  --> Re-ranking (cross-encoder, score de pertinence)
  --> Augmentation (assemblage du prompt avec contexte, citations, instructions)
  --> Generation (appel LLM avec contexte récupéré)
  --> Validation (vérification de fidélité, guardrails de sortie)
  --> Response (réponse avec sources et citations)
```

### Architecture diagram

```
+---------------------+     +-------------------+     +------------------+
|   Document Sources  |     |   Ingestion       |     |   Vector Store   |
|                     |     |   Pipeline        |     |                  |
|  - PDF, HTML, MD    +---->+  - Parse          +---->+  - Dense index   |
|  - Base de données  |     |  - Chunk          |     |  - Sparse index  |
|  - API externes     |     |  - Embed          |     |  - Metadata      |
|  - Confluence, etc. |     |  - Enrich metadata|     |  - Filtres       |
+---------------------+     +-------------------+     +--------+---------+
                                                               |
+---------------------+     +-------------------+             |
|   User Interface    |     |   Query Pipeline  |             |
|                     |     |                   |<------------+
|  - Chat             +---->+  - Query analysis |
|  - API              |     |  - Hybrid search  |     +------------------+
|  - Agent            |     |  - Re-ranking     +---->+  LLM Generation  |
+---------------------+     |  - Prompt assembly|     |                  |
                             +-------------------+     |  - Réponse       |
                                                       |  - Citations     |
                                                       |  - Confiance     |
                                                       +------------------+
```

### Component selection guide

| Composant | Options recommandées | Critère de choix |
|---|---|---|
| **Parser** | Unstructured, Docling, LlamaParse | Type de documents, précision d'extraction |
| **Chunking** | Recursive, Semantic, Document-aware | Structure du corpus, variabilité |
| **Embedding** | OpenAI text-embedding-3, Cohere embed-v3, BGE-M3 | Coût, performance multilingue, hébergement |
| **Vector DB** | Pinecone, Qdrant, pgvector, Weaviate | Ops, scaling, fonctionnalités de filtrage |
| **Re-ranker** | Cohere Rerank v3.5, BGE Reranker, Jina Reranker | Latence, précision, coût |
| **LLM** | Claude (Anthropic), GPT-4o (OpenAI), Gemini (Google) | Qualité, context window, coût par token |
| **Observabilité** | Langfuse, Langsmith, Braintrust, Helicone | Traçabilité, évaluation, intégration |

### Recherche hybride (dense + sparse)

Combiner systématiquement la recherche dense (similarité sémantique par vecteurs) et sparse (BM25, mots-clés) pour une couverture optimale :

- **Dense** : capture le sens sémantique ("croissance du chiffre d'affaires" correspond à "augmentation des revenus").
- **Sparse** : capture les termes exacts (noms propres, acronymes, identifiants, dates).
- **Fusion** : utiliser Reciprocal Rank Fusion (RRF) avec pondération ajustable (typiquement 0.6 dense / 0.4 sparse).

### Métriques de qualité RAG

| Métrique | Ce qu'elle mesure | Cible |
|---|---|---|
| **Context Relevance** | Les documents récupérés sont-ils pertinents pour la question ? | > 0.80 |
| **Faithfulness** | La réponse est-elle fidèle au contexte récupéré (pas d'hallucination) ? | > 0.90 |
| **Answer Relevance** | La réponse répond-elle effectivement à la question posée ? | > 0.85 |
| **Context Recall** | Le contexte contient-il l'information nécessaire ? | > 0.80 |
| **Precision@k** | Fraction des top-k documents qui sont pertinents | > 0.70 |
| **Latence end-to-end** | Temps total query-to-response | < 3s (P95) |

---

## 2. Embedding Models & Vector Databases

### Comparaison des modèles d'embeddings (2025-2026)

| Modèle | Provider | Dimensions | Max tokens | Multilingue | Prix (par 1M tokens) | Cas d'usage |
|---|---|---|---|---|---|---|
| **text-embedding-3-large** | OpenAI | 3072 (configurable) | 8191 | Oui | ~$0.13 | Usage général, meilleure qualité |
| **text-embedding-3-small** | OpenAI | 1536 (configurable) | 8191 | Oui | ~$0.02 | Volume élevé, coût réduit |
| **embed-v3** | Cohere | 1024 | 512 | Fort (100+ langues) | ~$0.10 | RAG multilingue, compression |
| **voyage-3-large** | Voyage AI | 1024 | 32000 | Oui | ~$0.18 | Code, documents longs |
| **BGE-M3** | BAAI (open source) | 1024 | 8192 | Fort | Gratuit (self-hosted) | Self-hosted, données sensibles |
| **E5-Mistral-7B** | Microsoft (open source) | 4096 | 32768 | Oui | Gratuit (self-hosted) | Long context, self-hosted |
| **Jina embeddings v3** | Jina AI | 1024 | 8192 | Oui | ~$0.02 | Self-hosted ou API, flexible |
| **Gemini Embedding** | Google | 768 | 2048 | Oui | ~$0.004 | Multimodal, très bas coût |

**Règles de sélection** :

- Choisir **text-embedding-3-large** par défaut pour la meilleure qualité avec API managée.
- Choisir **BGE-M3** ou **E5-Mistral** pour le self-hosting et les données sensibles.
- Utiliser la réduction dimensionnelle Matryoshka (3072 vers 1024 ou 512) pour optimiser le stockage sans perte significative de qualité.
- Toujours évaluer sur un échantillon représentatif de vos données réelles, pas uniquement sur les benchmarks MTEB.

### Comparaison des vector databases (2025-2026)

| Base vectorielle | Type | Filtrage metadata | Recherche hybride | Scaling | Multi-tenancy | Prix |
|---|---|---|---|---|---|---|
| **Pinecone** | Cloud managé | Excellent | Oui (sparse-dense) | Auto-scaling serverless | Namespaces | Pay-per-use, ~$0.08/1M reads |
| **Weaviate** | Open source / cloud | Excellent | Natif (BM25 + vector) | Horizontal sharding | Natif | Self-hosted gratuit, cloud payant |
| **Qdrant** | Open source / cloud | Excellent (payload index) | Via sparse vectors | Sharding + réplication | Collections | Self-hosted gratuit, cloud payant |
| **pgvector** | Extension PostgreSQL | Via SQL standard | Via full-text search + vector | Scaling PostgreSQL | Via schemas | Gratuit (extension) |
| **ChromaDB** | Open source | Basique | Non natif | Limité (single-node) | Non | Gratuit, prototypage |
| **Milvus / Zilliz** | Open source / cloud | Bon | Oui | Massif (GPU, distribué) | Collections | Self-hosted gratuit, cloud payant |

**Arbre de décision** :

```
Quel est votre contexte ?
+-- Prototype / développement local
|   --> ChromaDB (simple, embarqué, zéro config)
+-- Déjà sur PostgreSQL en production
|   --> pgvector (pas de nouveau composant, SQL natif)
+-- Production SaaS, zéro ops souhaité
|   --> Pinecone (serverless, auto-scaling)
+-- Besoin de recherche hybride native
|   --> Weaviate (BM25 + vector intégrés)
+-- Performance maximale, self-hosted
|   --> Qdrant (Rust, filtrage avancé, quantization)
+-- Très grand volume (> 100M vecteurs)
|   --> Milvus / Zilliz (GPU, distribué)
```

---

## 3. Chunking Strategies Deep Dive

### Comparaison détaillée des stratégies

| Stratégie | Description | Taille recommandée | Overlap | Complexité | Qualité |
|---|---|---|---|---|---|
| **Fixed-size** | Découpage à N caractères/tokens fixes | 500-1000 tokens | 10-20% | Très basse | Baseline |
| **Recursive** | Découpage récursif sur hiérarchie de séparateurs (\n\n, \n, ". ") | 500-1000 tokens | 10-20% | Basse | Bonne |
| **Semantic** | Découpage basé sur la similarité sémantique entre phrases | Variable (200-1500 tokens) | Aucun | Moyenne | Très bonne |
| **Document-aware** | Découpage respectant la structure (titres, sections, tableaux) | Variable par section | Optionnel | Moyenne-haute | Excellente |
| **Parent-child** | Petits chunks pour le retrieval, grands chunks pour le contexte | Parent 2000 / Child 400 | Par hiérarchie | Moyenne | Excellente |
| **Agentic** | LLM qui décide des limites de chunks en analysant le contenu | Variable | Décision par LLM | Haute | Meilleure |

### Stratégies d'overlap

L'overlap (chevauchement) entre chunks consécutifs est critique pour éviter de couper des idées au milieu :

- **Overlap fixe** : 10-20% de la taille du chunk (200 caractères d'overlap pour un chunk de 1000). Simple et efficace.
- **Overlap par phrase** : conserver les 1-2 dernières phrases du chunk précédent. Préserve mieux la cohérence.
- **Overlap sémantique** : le chunking sémantique élimine le besoin d'overlap car les frontières sont naturelles.
- **Pas d'overlap** : acceptable uniquement pour les documents très structurés (tableaux, listes de FAQ).

### Enrichissement des métadonnées

Toujours enrichir chaque chunk avec des métadonnées exploitables pour le filtrage et le contexte :

```python
chunk_metadata = {
    "source": "rapport_annuel_2025.pdf",
    "page_numbers": [12, 13],
    "section_title": "Résultats financiers Q3",
    "document_type": "rapport_annuel",
    "date_document": "2025-10-15",
    "langue": "fr",
    "chunk_index": 42,
    "total_chunks": 156,
    "parent_chunk_id": "chunk_parent_7",  # pour parent-child
    "heading_hierarchy": ["Résultats", "Q3 2025", "Chiffre d'affaires"],
    "entities_detected": ["Revenue", "EBITDA", "Q3"]
}
```

### Arbre de décision chunking

```
Quel type de document ?
+-- Texte simple, homogène (articles, emails)
|   --> Recursive character splitting (500-1000 tokens, 20% overlap)
+-- Documentation technique structurée (Markdown, HTML)
|   --> Document-aware (par sections/headers) + recursive pour les longues sections
+-- Corpus multi-format hétérogène
|   --> Semantic chunking (détection automatique des frontières)
+-- Base de connaissances avec besoin de contexte large
|   --> Parent-child (child 400 tokens retrieval, parent 2000 tokens contexte)
+-- Contrats, documents juridiques
|   --> Document-aware (par clauses/articles) + métadonnées enrichies
+-- Budget illimité, qualité maximale
|   --> Agentic chunking (LLM analyse chaque frontière)
```

---

## 4. Prompt Engineering for Developers

### System prompts — Bonnes pratiques

Le system prompt est le levier le plus puissant pour contrôler le comportement d'un LLM. Structurer chaque system prompt avec ces composants :

```
STRUCTURE D'UN SYSTEM PROMPT DE PRODUCTION

1. Rôle et identité : Qui est l'assistant, quel est son domaine d'expertise
2. Objectif : Quelle tâche précise accomplir
3. Contraintes : Ce que l'assistant ne doit PAS faire
4. Format de sortie : Structure exacte attendue (JSON, Markdown, etc.)
5. Exemples : 1-3 exemples input/output (few-shot)
6. Règles de gestion d'erreur : Que faire quand l'information est insuffisante
```

```python
system_prompt = """Tu es un assistant spécialisé en analyse de contrats juridiques français.

OBJECTIF : Extraire les clauses clés d'un contrat et les résumer de manière structurée.

CONTRAINTES :
- Ne jamais inventer d'information absente du contrat
- Si une clause est ambiguë, signaler l'ambiguïté explicitement
- Ne pas fournir de conseil juridique, uniquement de l'extraction factuelle

FORMAT DE SORTIE : JSON strict avec le schéma suivant :
{
  "parties": [{"nom": "...", "rôle": "..."}],
  "date_signature": "YYYY-MM-DD",
  "durée": "...",
  "clauses_clés": [{"type": "...", "résumé": "...", "article_ref": "..."}],
  "points_attention": ["..."]
}

Si une information est absente du contrat, utiliser null pour le champ correspondant."""
```

### Few-shot prompting

Fournir des exemples concrets améliore la qualité de 20-40% sur les tâches de classification et d'extraction. Règles :

- **3-5 exemples** suffisent dans la majorité des cas. Au-delà, les gains sont marginaux.
- **Couvrir les cas limites** : inclure au moins un exemple de cas difficile ou ambigu.
- **Varier les exemples** : ne pas utiliser des exemples trop similaires entre eux.
- **Placer les exemples après les instructions** : le LLM accorde plus d'attention aux instructions qui précèdent les exemples.

### Chain-of-thought (CoT)

Forcer le raisonnement étape par étape pour les tâches complexes :

```python
# CoT explicite
prompt = """Analyse cette situation et raisonne étape par étape avant de conclure.

Étape 1 : Identifier les faits clés
Étape 2 : Identifier les règles applicables
Étape 3 : Appliquer les règles aux faits
Étape 4 : Formuler la conclusion

Situation : {situation}

Raisonnement :"""

# CoT implicite (plus simple, souvent suffisant)
prompt = """Réfléchis étape par étape avant de répondre.

Question : {question}"""
```

Utiliser le CoT pour : calculs, raisonnements logiques, analyses multi-critères, débogage. Ne pas utiliser pour : extraction simple, classification binaire, reformulation.

### Prompt templates et variable injection

Structurer les prompts comme des templates avec variables typées et validées :

```python
from string import Template
from pydantic import BaseModel

class RAGPromptVars(BaseModel):
    question: str
    context: str
    max_words: int = 200
    language: str = "fr"
    citation_style: str = "inline"

RAG_TEMPLATE = Template("""Réponds à la question en te basant UNIQUEMENT sur le contexte fourni.

Contexte :
$context

Question : $question

Instructions :
- Répondre en $language
- Maximum $max_words mots
- Citer les sources avec le style $citation_style : [Source N]
- Si le contexte ne contient pas l'information, répondre "Information non disponible dans les sources fournies."

Réponse :""")

def build_prompt(vars: RAGPromptVars) -> str:
    return RAG_TEMPLATE.substitute(vars.model_dump())
```

### Prompt versioning

Traiter les prompts comme du code — versionnés, testés, déployés :

- **Stocker les prompts dans un fichier dédié** (YAML, JSON) ou un système de gestion (Langfuse, Humanloop, PromptLayer).
- **Versionner chaque modification** avec un changelog (v1.0, v1.1, v2.0).
- **Associer chaque version à ses métriques d'évaluation** pour tracer les régressions.
- **Ne jamais modifier un prompt en production sans A/B test** sur le dataset d'évaluation.

### A/B testing de prompts

```python
# Pseudocode — A/B testing de prompts
import random

PROMPT_VARIANTS = {
    "v1_concise": "Réponds en une phrase courte et précise.",
    "v2_detailed": "Réponds de manière détaillée avec des exemples.",
    "v3_structured": "Réponds avec un format structuré : Résumé, Détails, Conclusion."
}

def select_prompt_variant(user_id: str) -> str:
    # Assignation déterministe par utilisateur pour la cohérence
    variant_index = hash(user_id) % len(PROMPT_VARIANTS)
    variant_key = list(PROMPT_VARIANTS.keys())[variant_index]
    log_experiment("prompt_ab_test", user_id, variant_key)
    return PROMPT_VARIANTS[variant_key]
```

---

## 5. Structured Output Patterns

### JSON mode

Forcer la sortie JSON via les paramètres de l'API. Toujours préférer le JSON mode natif au parsing manuel :

```python
# Anthropic Claude — structured output via tool_use
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[{
        "name": "extract_entities",
        "description": "Extraire les entités d'un texte",
        "input_schema": {
            "type": "object",
            "properties": {
                "personnes": {"type": "array", "items": {"type": "string"}},
                "organisations": {"type": "array", "items": {"type": "string"}},
                "lieux": {"type": "array", "items": {"type": "string"}},
                "dates": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["personnes", "organisations", "lieux", "dates"]
        }
    }],
    tool_choice={"type": "tool", "name": "extract_entities"},
    messages=[{"role": "user", "content": f"Extrais les entités de ce texte : {text}"}]
)

# OpenAI — response_format avec JSON schema
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "entity_extraction",
            "schema": {
                "type": "object",
                "properties": {
                    "personnes": {"type": "array", "items": {"type": "string"}},
                    "organisations": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["personnes", "organisations"]
            }
        }
    },
    messages=[{"role": "user", "content": f"Extrais les entités : {text}"}]
)
```

### Function calling

Utiliser le function calling pour structurer les interactions LLM avec des outils externes :

```python
tools = [
    {
        "name": "search_database",
        "description": "Rechercher dans la base de données produits",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Termes de recherche"},
                "category": {"type": "string", "enum": ["electronics", "clothing", "food"]},
                "max_price": {"type": "number", "description": "Prix maximum en euros"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "create_order",
        "description": "Créer une commande pour un produit",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string"},
                "quantity": {"type": "integer", "minimum": 1},
                "shipping_address": {"type": "string"}
            },
            "required": ["product_id", "quantity", "shipping_address"]
        }
    }
]
```

### Validation Pydantic

Valider systématiquement les sorties LLM avec Pydantic pour garantir la conformité au schéma :

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import json

class AnalyseSentiment(BaseModel):
    sentiment: str = Field(..., pattern="^(positif|négatif|neutre)$")
    score: float = Field(..., ge=0.0, le=1.0)
    aspects: list[str] = Field(..., min_length=1, max_length=10)
    justification: str = Field(..., min_length=10, max_length=500)
    langue_detectee: str = Field(default="fr")

    @field_validator("aspects")
    @classmethod
    def aspects_non_vides(cls, v):
        return [a.strip() for a in v if a.strip()]

def parse_llm_response(raw_response: str) -> AnalyseSentiment:
    try:
        data = json.loads(raw_response)
        return AnalyseSentiment(**data)
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Sortie LLM invalide : {e}")
```

### Retry avec feedback d'erreur

Quand la sortie LLM ne respecte pas le schéma, renvoyer l'erreur de validation au LLM pour correction :

```python
def structured_llm_call(prompt: str, schema: type[BaseModel], max_retries: int = 3) -> BaseModel:
    messages = [{"role": "user", "content": prompt}]

    for attempt in range(max_retries):
        response = llm.invoke(messages)

        try:
            return schema.model_validate_json(response.content)
        except ValidationError as e:
            error_feedback = f"""Ta réponse précédente ne respecte pas le schéma attendu.

Erreurs de validation :
{e.json()}

Corrige ta réponse pour respecter exactement le schéma. Retourne uniquement du JSON valide."""

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": error_feedback})

    raise ValueError(f"Échec après {max_retries} tentatives de validation")
```

### Schema design — Bonnes pratiques

- **Champs obligatoires minimaux** : rendre optionnels les champs que le LLM pourrait ne pas trouver.
- **Enums pour les valeurs contraintes** : utiliser des enums plutôt que des strings libres pour les catégories.
- **Descriptions claires** : chaque champ doit avoir une description pour guider le LLM.
- **Types stricts** : préférer `int` à `number`, `list[str]` à `array`.
- **Valeurs par défaut** : fournir des défauts sensibles pour les champs optionnels.

---

## 6. Context Window Management

### Token counting

Toujours compter les tokens avant d'assembler un prompt pour éviter les dépassements :

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Pour Anthropic Claude, utiliser l'API de comptage
import anthropic
client = anthropic.Anthropic()
token_count = client.count_tokens(text)

# Règle : réserver 20-30% du context window pour la génération
MAX_CONTEXT = 128_000  # Claude Sonnet
RESERVED_FOR_GENERATION = 4_096
MAX_INPUT = MAX_CONTEXT - RESERVED_FOR_GENERATION
```

### Optimisation du context window

| Technique | Réduction tokens | Impact qualité | Complexité |
|---|---|---|---|
| **Résumé des messages anciens** | 70-80% | Légère perte de détail | Basse |
| **Compression de prompt** | 30-50% | Minimale si bien faite | Moyenne |
| **Sélection top-k chunks** | Variable | Dépend du k choisi | Basse |
| **Re-ranking puis top-n** | 50-70% vs top-k large | Améliore la qualité | Moyenne |
| **Extraction d'information ciblée** | 80-90% | Bonne si requête claire | Haute |

### Conversation memory patterns

```
+-- Sliding Window (fenêtre glissante)
|   Garder les N derniers messages. Simple mais perd le contexte ancien.
|   Recommandé : N = 10-20 messages pour les chatbots généraux.
|
+-- Summary Memory (mémoire par résumé)
|   Résumer périodiquement les anciens messages en un paragraphe.
|   Avantage : contexte infini compressé. Risque : perte de détails.
|
+-- RAG-Based Memory (mémoire vectorielle)
|   Stocker chaque message/échange en vector DB. Récupérer les
|   échanges passés pertinents par similarité à la requête courante.
|   Meilleur rappel contextuel mais latence additionnelle.
|
+-- Hybrid (sliding + summary + RAG)
|   Messages récents en fenêtre glissante, historique ancien résumé,
|   échanges pertinents récupérés par RAG. Architecture de production.
```

### Prompt compression

Réduire la taille des prompts sans perdre l'information essentielle :

- **LLMLingua / LongLLMLingua** : compression automatique de prompts par perplexité (réduit 2-5x).
- **Extraction selective** : ne garder que les passages pertinents des chunks récupérés.
- **Résumé hiérarchique** : résumer les chunks longs en conservant les points clés.

---

## 7. LLM API Patterns

### Streaming

Utiliser le streaming pour améliorer la latence perçue (Time-to-First-Token) :

```python
# Anthropic Claude — streaming
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# OpenAI — streaming
from openai import OpenAI

client = OpenAI()
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Retries avec exponential backoff

```python
import time
import random
from typing import Callable, TypeVar

T = TypeVar("T")

def retry_with_backoff(
    fn: Callable[..., T],
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    retryable_errors: tuple = (RateLimitError, APIConnectionError, InternalServerError)
) -> T:
    for attempt in range(max_retries):
        try:
            return fn()
        except retryable_errors as e:
            if attempt == max_retries - 1:
                raise
            delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
            time.sleep(delay)
    raise RuntimeError("Max retries exceeded")
```

### Rate limiting

Implémenter un rate limiter côté client pour respecter les quotas API :

```python
import asyncio
from asyncio import Semaphore

class LLMRateLimiter:
    def __init__(self, requests_per_minute: int = 60, tokens_per_minute: int = 100_000):
        self.rpm_semaphore = Semaphore(requests_per_minute)
        self.tpm_budget = tokens_per_minute
        self.tokens_used = 0
        self.reset_interval = 60  # secondes

    async def acquire(self, estimated_tokens: int):
        await self.rpm_semaphore.acquire()
        while self.tokens_used + estimated_tokens > self.tpm_budget:
            await asyncio.sleep(1)
        self.tokens_used += estimated_tokens

    def release(self):
        self.rpm_semaphore.release()
```

### Fallback chains

Configurer des chaînes de fallback pour la résilience :

```python
MODEL_CHAIN = [
    {"provider": "anthropic", "model": "claude-sonnet-4-20250514", "timeout": 30},
    {"provider": "openai", "model": "gpt-4o", "timeout": 30},
    {"provider": "anthropic", "model": "claude-haiku-4-20250514", "timeout": 15},
]

async def call_with_fallback(prompt: str, chain: list[dict] = MODEL_CHAIN) -> str:
    last_error = None
    for config in chain:
        try:
            return await call_llm(prompt, **config)
        except (TimeoutError, RateLimitError, APIError) as e:
            last_error = e
            log.warning(f"Fallback: {config['model']} failed with {e}")
            continue
    raise last_error
```

### Error handling

| Erreur | Code | Action | Retry ? |
|---|---|---|---|
| **Rate limit** | 429 | Backoff exponentiel, respecter Retry-After header | Oui |
| **Timeout** | 408/timeout | Réduire max_tokens ou passer au modèle suivant | Oui (1-2x) |
| **Server error** | 500/502/503 | Backoff exponentiel | Oui (3-5x) |
| **Auth error** | 401/403 | Vérifier les clés API, ne pas retry | Non |
| **Bad request** | 400 | Corriger le prompt/paramètres | Non |
| **Content filter** | 400 (specific) | Reformuler le prompt, vérifier le contenu | Non |
| **Context overflow** | 400 (specific) | Réduire le prompt, tronquer le contexte | Non (corriger) |

---

## 8. Caching Strategies

### Prompt caching natif

Les providers majeurs offrent désormais du prompt caching côté serveur :

| Provider | Mécanisme | Réduction de coût | Réduction de latence | Conditions |
|---|---|---|---|---|
| **Anthropic** | Cache automatique des longs préfixes | 90% sur les tokens cachés | 85% de latence en moins | Préfixe > 1024 tokens, TTL 5 min |
| **OpenAI** | Automatic prompt caching | 50% sur les tokens cachés | Variable | Préfixe identique, TTL ~1h |
| **Google** | Context caching (explicite) | 75% sur les tokens cachés | Significative | Cache explicite, TTL configurable |

**Stratégie d'optimisation** : placer le contenu statique (system prompt, exemples few-shot, contexte de référence) en début de prompt pour maximiser la correspondance de préfixe. Le contenu dynamique (question utilisateur) doit être en fin de prompt.

```python
# Anthropic — optimisation pour le prompt caching
# Le system prompt long et les exemples sont cachés automatiquement
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": long_system_prompt,  # > 1024 tokens -> caché automatiquement
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{"role": "user", "content": user_question}]  # Partie dynamique
)
# usage.cache_creation_input_tokens, usage.cache_read_input_tokens
```

### Semantic caching

Cacher les réponses par similarité sémantique plutôt que par correspondance exacte :

```python
class SemanticCache:
    def __init__(self, vectorstore, similarity_threshold: float = 0.95):
        self.vectorstore = vectorstore
        self.threshold = similarity_threshold

    def get(self, query: str) -> str | None:
        results = self.vectorstore.similarity_search_with_score(query, k=1)
        if results and results[0][1] >= self.threshold:
            return results[0][0].metadata["response"]
        return None

    def put(self, query: str, response: str):
        self.vectorstore.add_documents([
            Document(
                page_content=query,
                metadata={"response": response, "created_at": datetime.now().isoformat()}
            )
        ])
```

### Cache invalidation

- **TTL-based** : expiration automatique après un délai configurable (1h-24h selon la fraîcheur requise).
- **Event-based** : invalider quand les documents sources sont mis à jour (via webhook ou CDC).
- **Version-based** : invalider quand le modèle ou le prompt change (inclure un hash du prompt dans la clé de cache).

### Impact coût du caching

| Scénario | Sans cache | Avec prompt caching | Avec semantic caching | Économie totale |
|---|---|---|---|---|
| **1M requêtes/mois, $0.003/requête** | $3,000 | $1,500 (50% préfixes identiques) | $900 (40% cache hits sémantiques) | 70% |
| **Support client (FAQ répétitives)** | $5,000 | $3,000 | $500 (90% cache hits) | 90% |
| **RAG analytique (requêtes uniques)** | $2,000 | $1,200 (system prompt caché) | $1,100 (10% cache hits) | 45% |

---

## 9. State of the Art (2025-2026)

### Prefix caching avancé

Les providers étendent le prompt caching au-delà du simple préfixe :

- **Anthropic** : cache automatique multi-segment, TTL prolongé avec réutilisation fréquente.
- **OpenAI** : cached completions avec discount automatique sur les préfixes récurrents.
- **Implication architecturale** : concevoir les prompts avec un long préfixe stable (system prompt + contexte de référence + exemples few-shot) suivi d'un court suffixe dynamique (question utilisateur).

### Model distillation

Utiliser un modèle puissant (Claude Opus, GPT-4o) pour générer des données d'entraînement pour un modèle plus petit et moins coûteux :

```
Pipeline de distillation :
1. Collecter les requêtes de production
2. Générer les réponses de haute qualité avec le modèle teacher (frontier)
3. Filtrer et valider les paires (input, output) de qualité
4. Fine-tuner un modèle student (Claude Haiku, GPT-4o-mini, Llama 3)
5. Évaluer le modèle distillé vs le teacher sur le dataset d'eval
6. Déployer le student si la qualité est suffisante (>95% de la qualité teacher)
```

Gains typiques : 80-90% de réduction de coût avec 95-98% de la qualité sur les tâches bien définies.

### Multimodal RAG

Étendre le RAG au-delà du texte pour indexer et rechercher des images, tableaux, graphiques :

- **Vision-based parsing** : utiliser des modèles multimodaux (GPT-4o, Claude) pour extraire le texte et la sémantique des images et tableaux dans les documents.
- **Multimodal embeddings** : Gemini Embedding, CLIP pour indexer images et texte dans le même espace vectoriel.
- **ColPali / ColQwen** : modèles spécialisés qui indexent directement les images de pages de documents (bypasse l'OCR), état de l'art pour le document retrieval en 2025-2026.

### GraphRAG

Combiner la recherche vectorielle avec un knowledge graph pour capturer les relations entre entités :

```
Documents --> Extraction d'entités et relations (par LLM)
          --> Construction du knowledge graph (Neo4j, Amazon Neptune)
          --> Indexation des communautés (clusters d'entités liées)

Query --> Recherche vectorielle (chunks pertinents)
      --> Recherche dans le graph (entités liées, chemins de relation)
      --> Fusion des résultats (contexte enrichi par les relations)
      --> Génération avec contexte structuré
```

Avantages : meilleure performance sur les questions de synthèse ("Quels sont les liens entre X et Y ?"), requêtes multi-hop, et résumés globaux d'un corpus.

### Contextual retrieval

Technique Anthropic (2024-2025) : enrichir chaque chunk avec un court résumé contextuel généré par LLM avant l'indexation. Le LLM voit le document complet et génère un préfixe de contexte pour chaque chunk :

```python
contextual_prompt = """Voici le document complet :
{full_document}

Voici un chunk spécifique de ce document :
{chunk}

Génère un court contexte (2-3 phrases) situant ce chunk dans le document global.
Ce contexte sera préfixé au chunk pour améliorer la recherche."""

# Résultat : "Ce chunk fait partie du rapport annuel 2025, section Résultats Q3.
# Il détaille la croissance du CA par région. [chunk original]"
```

Impact mesuré : +49% d'amélioration de la précision de retrieval par rapport au chunking sans contexte.

### Late chunking

Technique émergente : encoder le document complet avec un modèle d'embedding long-context, puis extraire les embeddings au niveau du chunk a posteriori. Chaque embedding de chunk bénéficie ainsi du contexte global du document :

```
Approche traditionnelle :
Document --> Chunking --> Embedding de chaque chunk indépendamment

Late chunking :
Document --> Embedding du document complet (modèle long-context)
         --> Extraction des embeddings par segment (token pooling par chunk)
         --> Chaque chunk embedding encode le contexte global
```

Avantage : les embeddings de chunks capturent le contexte inter-chunks sans duplication de tokens. Nécessite un modèle d'embedding supportant les longs contextes (Jina embeddings v3, E5-Mistral).

### Agentic RAG

Les systèmes RAG évoluent vers des architectures agentiques où un agent LLM orchestre dynamiquement le processus de retrieval :

- **Routing dynamique** : l'agent choisit la source de données appropriée (vector DB, SQL, API, web search) en fonction de la requête.
- **Retrieval itératif** : l'agent évalue la suffisance du contexte récupéré et décide de faire des recherches supplémentaires.
- **Query planning** : décomposition automatique des questions complexes en sous-questions indépendantes.
- **Tool use** : l'agent utilise des outils (calculatrice, code interpreter, API) pour compléter le contexte récupéré.
