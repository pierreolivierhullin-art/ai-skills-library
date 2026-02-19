# Vector Search Avancé — pgvector, Qdrant, Weaviate et Stratégies d'Embedding

## Overview

Ce document de référence couvre la recherche vectorielle en production : index pgvector HNSW et IVFFlat avec leurs paramètres fins, comparaison des modèles d'embedding (OpenAI, Cohere, Mistral, open-source), stratégies de chunking pour RAG, Qdrant et Weaviate en détail, FAISS pour le batch offline, reranking deux étapes, et embeddings multimodaux CLIP. Utiliser ce guide comme fondation pour toute décision d'architecture de recherche sémantique.

---

## 1. pgvector — Index Avancés et Tuning

### HNSW vs IVFFlat — Choix d'index

pgvector propose deux famètres d'indexation avec des trade-offs distincts. Choisir en fonction du volume, de la RAM disponible et de l'importance relative de la vitesse vs de la précision :

| Paramètre | HNSW | IVFFlat |
|---|---|---|
| **Vitesse de requête** | Très rapide (O(log n)) | Rapide (O(sqrt(n))) |
| **Précision (recall@10)** | 95-99% | 85-95% |
| **Temps de build** | Lent (proportionnel à m × ef_construction) | Rapide |
| **Consommation RAM** | Haute (graphe en mémoire) | Basse |
| **Dégradation à chaud** | Aucune | Possible si listes mal calibrées |
| **Cas d'usage** | Production, requêtes temps réel | Gros volumes, RAM contrainte |

```sql
-- HNSW — paramètres de production recommandés
-- m : nombre de connexions par nœud (8-64, défaut 16)
-- ef_construction : taille du beam search à la construction (32-400, défaut 64)
CREATE INDEX idx_docs_hnsw
ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 128);

-- Augmenter ef_search à la requête pour améliorer le recall
SET hnsw.ef_search = 100;  -- Défaut : 40, max recommandé : 200

-- IVFFlat — calibrer le nombre de listes sur sqrt(N)
-- Pour 1M vecteurs : lists = 1000, probes = 50
-- Pour 100K vecteurs : lists = 300, probes = 20
CREATE INDEX idx_docs_ivfflat
ON documents USING ivfflat (embedding vector_l2_ops)
WITH (lists = 1000);

SET ivfflat.probes = 50;  -- Nombre de listes à sonder par requête
```

**Règles de calibrage HNSW** :
- `m = 16` est un bon défaut. Augmenter à 32-64 si le recall est insuffisant (coût en RAM).
- `ef_construction = 128` garantit un graphe bien construit. Ne jamais descendre sous 64.
- `ef_search` contrôle le recall à la requête : augmenter de 40 à 100-200 améliore le recall de 2-5% avec +20-50% de latence.
- Reconstruire l'index HNSW après 20%+ d'insertions — le graphe se dégrade par fragmentation.

### Filtrage pré-filter vs post-filter

Le filtrage sur les métadonnées en conjonction avec la recherche vectorielle présente un trade-off critique :

```sql
-- POST-FILTER (défaut pgvector) : recherche vectorielle puis filtre
-- Problème : si le filtre élimine 99% des résultats, le top-k peut être vide
SELECT id, titre, 1 - (embedding <=> $1::vector) AS score
FROM documents
WHERE 1 - (embedding <=> $1::vector) >= 0.7
  AND categorie = 'juridique'          -- Filtre appliqué après le scan vectoriel
ORDER BY embedding <=> $1::vector
LIMIT 10;

-- PRE-FILTER : créer un index partiel par catégorie
-- Avantage : seuls les vecteurs de la catégorie sont scannés
-- Inconvénient : un index par valeur de filtre
CREATE INDEX idx_docs_juridique_hnsw
ON documents USING hnsw (embedding vector_cosine_ops)
WHERE categorie = 'juridique';

-- Utiliser l'index partiel avec la clause WHERE correspondante
SELECT id, titre, 1 - (embedding <=> $1::vector) AS score
FROM documents
WHERE categorie = 'juridique'
ORDER BY embedding <=> $1::vector
LIMIT 10;

-- APPROCHE HYBRIDE recommandée : filtrage sur partition + HNSW partiel
-- Partitionner la table par dimension haute cardinalité (tenant_id, date)
CREATE TABLE documents_2025 PARTITION OF documents
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

**Règle de décision** :
- Sélectivité > 10% → post-filter acceptable.
- Sélectivité < 10% → utiliser un index partiel ou partitionner la table.
- Multi-tenant → partitionner par `tenant_id`, un index HNSW par partition.

### Quantization — Compression des vecteurs

Réduire l'empreinte mémoire et accélérer les calculs via la quantization :

```sql
-- Scalar quantization (SQ) : float32 → int8 (4x moins de RAM)
-- Perte de précision : recall@10 de 98% → 95%
CREATE INDEX idx_docs_hnsw_sq
ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 128, quantization = 'scalar');

-- Binary quantization : float32 → 1 bit par dimension (32x moins de RAM)
-- Requiert une re-vérification sur les vecteurs originaux (rescore)
-- Recommandé uniquement pour les modèles >= 1024 dimensions
CREATE INDEX idx_docs_hnsw_bq
ON documents USING hnsw (embedding bit_hamming_ops)
WITH (m = 16, ef_construction = 128);

-- Matryoshka Representation Learning (MRL) : réduire les dimensions
-- OpenAI text-embedding-3 supporte la réduction dimensionnelle native
SELECT id,
  embedding::vector(512)  -- Tronquer de 1536 → 512 dimensions
FROM documents;
```

| Méthode | Compression | Perte recall | Cas d'usage |
|---|---|---|---|
| **Aucune (float32)** | 1× | 0% | < 1M vecteurs, précision maximale |
| **Scalar (int8)** | 4× | 2-5% | 1-10M vecteurs, production standard |
| **Binary (1 bit)** | 32× | 5-15% | > 10M vecteurs, rescore obligatoire |
| **MRL (dimensions réduites)** | 2-6× | 1-8% | Embeddings OpenAI/Cohere natifs MRL |

### Maintenance de l'index

```sql
-- Vérifier la fragmentation de l'index HNSW
SELECT indexname, pg_size_pretty(pg_relation_size(indexname::regclass))
FROM pg_indexes WHERE tablename = 'documents';

-- Reconstruire après des insertions massives (> 20% du total)
REINDEX INDEX CONCURRENTLY idx_docs_hnsw;

-- Vacuum régulier pour libérer les dead tuples
VACUUM ANALYZE documents;

-- Monitorer le ratio dead_tuples / live_tuples
SELECT n_dead_tup, n_live_tup, last_vacuum
FROM pg_stat_user_tables WHERE relname = 'documents';
```

---

## 2. Modèles d'Embedding — Comparaison 2025-2026

### Tableau comparatif complet

| Modèle | Provider | Dimensions | Max tokens | Multilingue | Prix (1M tokens) | MTEB Score | Cas d'usage |
|---|---|---|---|---|---|---|---|
| **text-embedding-3-large** | OpenAI | 3072 (réductible) | 8191 | Oui | ~$0.13 | 64.6 | Qualité maximale, RAG général |
| **text-embedding-3-small** | OpenAI | 1536 (réductible) | 8191 | Oui | ~$0.02 | 62.3 | Volume élevé, rapport qualité/coût |
| **embed-v3-multilingual** | Cohere | 1024 | 512 | Excellent (100+ langues) | ~$0.10 | 64.0 | RAG multilingue, compression |
| **embed-v3-english** | Cohere | 1024 | 512 | Non | ~$0.10 | 64.5 | Corpus anglophone, légèrement meilleur |
| **mistral-embed** | Mistral | 1024 | 8192 | Oui (EU focus) | ~$0.10 | 55.3 | Conformité données EU, long context |
| **voyage-3-large** | Voyage AI | 1024 | 32000 | Oui | ~$0.18 | 68.3 | Meilleur score MTEB, code + docs longs |
| **BGE-M3** | BAAI (OSS) | 1024 | 8192 | Fort (100 langues) | Gratuit | 66.1 | Self-hosted, données sensibles |
| **nomic-embed-text-v1.5** | Nomic (OSS) | 768 | 8192 | Oui | Gratuit | 62.3 | Self-hosted léger, bonne performance |
| **E5-Mistral-7B** | Microsoft (OSS) | 4096 | 32768 | Oui | Gratuit | 66.6 | Long context self-hosted, top open-source |
| **Jina embeddings v3** | Jina AI | 1024 | 8192 | Oui | ~$0.02 | 65.1 | API ou self-hosted, task-specific |

### Règles de sélection

```
Quel est votre contexte ?
+-- Prototype rapide, budget faible
|   --> text-embedding-3-small (API simple, très bon rapport qualité/coût)
+-- Production RAG général, qualité prioritaire
|   --> text-embedding-3-large avec réduction MRL à 1024 dims
+-- Corpus multilingue (FR/EN/ES/DE/etc.)
|   --> embed-v3-multilingual (Cohere) ou BGE-M3 (self-hosted)
+-- Données sensibles, RGPD, pas d'envoi externe
|   --> BGE-M3 ou nomic-embed-text (self-hosted via Ollama/vLLM)
+-- Documents très longs (> 8K tokens)
|   --> voyage-3-large (32K tokens) ou E5-Mistral-7B (32K tokens)
+-- Code source, documentation technique
|   --> voyage-3-large (excellente performance code) ou text-embedding-3-large
+-- Budget très contraint, > 1 milliard tokens/mois
|   --> nomic-embed-text-v1.5 (self-hosted, gratuit)
```

### Évaluation sur vos données

Ne jamais se fier uniquement aux benchmarks MTEB — évaluer systématiquement sur un échantillon représentatif de vos requêtes et documents réels :

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def évaluer_modèle_embedding(
    modèle,
    requêtes: list[str],
    documents: list[str],
    relevances: list[list[int]],  # 0/1 par (requête, doc)
    k: int = 10
) -> dict:
    """Évaluer recall@k et NDCG@k sur vos données métier."""
    embs_requêtes = modèle.encode(requêtes, normalize_embeddings=True)
    embs_docs = modèle.encode(documents, normalize_embeddings=True)

    scores = cosine_similarity(embs_requêtes, embs_docs)

    recall_k, ndcg_k = [], []
    for i, (row, rels) in enumerate(zip(scores, relevances)):
        top_k = np.argsort(-row)[:k]
        pertinents = set(j for j, r in enumerate(rels) if r == 1)
        # Recall@k
        recall_k.append(len(set(top_k) & pertinents) / max(len(pertinents), 1))
        # NDCG@k
        dcg = sum(rels[j] / np.log2(rang + 2) for rang, j in enumerate(top_k))
        idcg = sum(1 / np.log2(rang + 2) for rang in range(min(k, len(pertinents))))
        ndcg_k.append(dcg / idcg if idcg > 0 else 0)

    return {
        "recall@k": np.mean(recall_k),
        "ndcg@k": np.mean(ndcg_k),
        "k": k
    }
```

---

## 3. Stratégies de Chunking pour RAG

### Comparaison des stratégies

| Stratégie | Taille typique | Overlap | Complexité | Qualité retrieval | Idéal pour |
|---|---|---|---|---|---|
| **Fixed-size** | 512-1000 tokens | 10-20% | Très basse | Baseline | Prototypage rapide |
| **Recursive** | 500-1000 tokens | 10-20% | Basse | Bonne | Texte homogène |
| **Semantic** | 200-1500 tokens | Aucun | Moyenne | Très bonne | Corpus hétérogène |
| **Late chunking** | Variable | Aucun | Moyenne | Excellente | Modèles long-context |
| **Parent-child** | Parent 2000 / Child 400 | Par hiérarchie | Moyenne | Excellente | Besoin de contexte large |
| **Document-aware** | Par section | Optionnel | Haute | Excellente | Docs structurés (MD, HTML) |

### Fixed-size et Recursive Splitting

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Recursive splitting — hiérarchie de séparateurs : \n\n → \n → . → " "
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # tokens (ou caractères selon le tokenizer utilisé)
    chunk_overlap=150,     # ~15% overlap
    separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
    length_function=len,   # Utiliser tiktoken pour un comptage précis
)

# Avec tiktoken pour un découpage en tokens exacts
import tiktoken
enc = tiktoken.encoding_for_model("text-embedding-3-small")

splitter_tokens = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    model_name="text-embedding-3-small",
    chunk_size=500,
    chunk_overlap=50,
)
```

### Semantic Chunking

Détecter automatiquement les frontières sémantiques en comparant la similarité cosinus entre phrases consécutives :

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# breakpoint_threshold_type : "percentile" (défaut), "standard_deviation", "interquartile"
semantic_splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95,  # Découper quand la dissimilarité dépasse le 95e percentile
)

chunks = semantic_splitter.split_text(document_text)
```

### Late Chunking

Encoder le document complet d'abord, puis extraire les embeddings par segment — chaque chunk bénéficie du contexte global :

```python
from transformers import AutoTokenizer, AutoModel
import torch

# Nécessite un modèle supportant les longs contextes (Jina v3, E5-Mistral)
tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-embeddings-v3")
modèle = AutoModel.from_pretrained("jinaai/jina-embeddings-v3", trust_remote_code=True)

def late_chunking(texte: str, positions_chunks: list[tuple[int, int]]) -> list[list[float]]:
    """
    positions_chunks : liste de (start_token, end_token) pour chaque chunk.
    Retourne un embedding par chunk, enrichi du contexte global.
    """
    tokens = tokenizer(texte, return_tensors="pt", truncation=True, max_length=8192)
    with torch.no_grad():
        outputs = modèle(**tokens)
    token_embeddings = outputs.last_hidden_state[0]  # (seq_len, hidden_dim)

    # Mean pooling par chunk sur les token embeddings contextualisés
    chunk_embeddings = []
    for start, end in positions_chunks:
        chunk_emb = token_embeddings[start:end].mean(dim=0)
        chunk_emb = torch.nn.functional.normalize(chunk_emb, dim=0)
        chunk_embeddings.append(chunk_emb.tolist())

    return chunk_embeddings
```

### Parent-Child Chunking

Stocker de petits chunks pour le retrieval (précision) et des grands chunks pour le contexte LLM (qualité) :

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Child splitter : petits chunks pour le retrieval (haute précision)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

# Parent splitter : grands chunks envoyés au LLM avec plus de contexte
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,        # Seuls les child chunks sont indexés vectoriellement
    docstore=InMemoryStore(),       # Les parent chunks sont stockés ici
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)
```

### Arbre de décision — Quelle stratégie choisir

```
Type de corpus ?
+-- Articles de blog, emails, texte homogène
|   --> Recursive splitting (500 tokens, 15% overlap)
+-- Documentation technique avec sections (Markdown, HTML)
|   --> Document-aware (par header) + recursive pour les longues sections
+-- Corpus très hétérogène (mélange types de documents)
|   --> Semantic chunking (95e percentile de dissimilarité)
+-- Modèle long-context disponible (Jina v3, E5-Mistral)
|   --> Late chunking (meilleure qualité d'embedding contextuel)
+-- Requêtes nécessitant du contexte large (synthèse, résumé)
|   --> Parent-child (child 400 tokens retrieval, parent 2000 contexte LLM)
+-- Corpus de contrats, documents juridiques, rapports structurés
|   --> Document-aware (par clauses/articles) + métadonnées enrichies
```

---

## 4. Qdrant — Collections, Filtrage et Sparse Vectors

### Configuration d'une collection

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PayloadSchemaType,
    SparseVectorParams, SparseIndexParams
)

client = QdrantClient(url="http://localhost:6333")

# Créer une collection avec vecteurs denses ET sparse (recherche hybride)
client.create_collection(
    collection_name="documents",
    vectors_config={
        "dense": VectorParams(size=1536, distance=Distance.COSINE),
    },
    sparse_vectors_config={
        "sparse": SparseVectorParams(
            index=SparseIndexParams(on_disk=False)  # En RAM pour la vitesse
        )
    },
    # Paramètres HNSW pour le vecteur dense
    hnsw_config={"m": 16, "ef_construct": 128, "on_disk": False},
    # Quantization scalaire (4× compression mémoire)
    quantization_config={"scalar": {"type": "int8", "quantile": 0.99}},
)

# Créer des index payload pour accélérer le filtrage
client.create_payload_index(
    collection_name="documents",
    field_name="categorie",
    field_schema=PayloadSchemaType.KEYWORD,
)
client.create_payload_index(
    collection_name="documents",
    field_name="date_publication",
    field_schema=PayloadSchemaType.DATETIME,
)
```

### Batch upsert avec vecteurs denses et sparse

```python
from qdrant_client.models import PointStruct, SparseVector
from fastembed import SparseTextEmbedding  # Modèle SPLADE ou BM25

dense_modèle = ...   # Votre modèle d'embedding dense
sparse_modèle = SparseTextEmbedding(model_name="Qdrant/bm25")

def indexer_batch(documents: list[dict], batch_size: int = 100):
    """Indexer des documents avec vecteurs denses et sparse en batch."""
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        textes = [f"{d['titre']} {d['contenu']}" for d in batch]

        # Générer les vecteurs denses et sparse en parallèle
        dense_vecs = dense_modèle.encode(textes, normalize_embeddings=True)
        sparse_vecs = list(sparse_modèle.embed(textes))

        points = [
            PointStruct(
                id=doc["id"],
                vector={
                    "dense": dense_vecs[j].tolist(),
                    "sparse": SparseVector(
                        indices=sparse_vecs[j].indices.tolist(),
                        values=sparse_vecs[j].values.tolist(),
                    ),
                },
                payload={
                    "titre": doc["titre"],
                    "contenu": doc["contenu"],
                    "categorie": doc["categorie"],
                    "date_publication": doc["date_publication"],
                },
            )
            for j, doc in enumerate(batch)
        ]

        client.upsert(collection_name="documents", points=points)
```

### Recherche hybride avec filtrage payload

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue, Prefetch, Query

# Recherche hybride : dense + sparse avec RRF Qdrant natif
def rechercher_hybride(
    requête: str,
    categorie: str | None = None,
    limite: int = 10
) -> list[dict]:
    dense_vec = dense_modèle.encode([requête], normalize_embeddings=True)[0].tolist()
    sparse_vec = list(sparse_modèle.embed([requête]))[0]

    filtre = None
    if categorie:
        filtre = Filter(must=[FieldCondition(key="categorie", match=MatchValue(value=categorie))])

    résultats = client.query_points(
        collection_name="documents",
        prefetch=[
            Prefetch(query=dense_vec, using="dense", limit=50, filter=filtre),
            Prefetch(
                query=SparseVector(
                    indices=sparse_vec.indices.tolist(),
                    values=sparse_vec.values.tolist(),
                ),
                using="sparse",
                limit=50,
                filter=filtre,
            ),
        ],
        query=Query(fusion="rrf"),  # Reciprocal Rank Fusion natif Qdrant
        limit=limite,
    )
    return [{"id": p.id, "payload": p.payload, "score": p.score} for p in résultats.points]
```

---

## 5. Weaviate — Schéma, Hybrid Search et Generative Search

### Configuration du schéma avec modules

```python
import weaviate
from weaviate.classes.config import (
    Configure, Property, DataType, VectorDistances, Tokenization
)

client = weaviate.connect_to_local()

# Créer une collection avec module de vectorisation OpenAI
client.collections.create(
    name="Document",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(
        model="text-embedding-3-small",
        dimensions=1536,
    ),
    generative_config=Configure.Generative.openai(model="gpt-4o"),
    vector_index_config=Configure.VectorIndex.hnsw(
        distance_metric=VectorDistances.COSINE,
        ef_construction=128,
        max_connections=16,
    ),
    properties=[
        Property(name="titre", data_type=DataType.TEXT, tokenization=Tokenization.WORD),
        Property(name="contenu", data_type=DataType.TEXT, tokenization=Tokenization.WORD),
        Property(name="categorie", data_type=DataType.TEXT, tokenization=Tokenization.KEYWORD),
        Property(name="date_publication", data_type=DataType.DATE),
    ],
)
```

### Hybrid Search et Generative Search

```python
from weaviate.classes.query import HybridFusion, MetadataQuery, GenerativeConfig

collection = client.collections.get("Document")

# Recherche hybride BM25 + vector avec pondération configurable
résultats = collection.query.hybrid(
    query="optimisation des performances PostgreSQL",
    alpha=0.6,              # 0 = BM25 pur, 1 = vector pur, 0.6 = 60% vectoriel
    fusion_type=HybridFusion.RELATIVE_SCORE,  # Alternative : RANKED
    filters=None,           # Ajouter des filtres Weaviate si nécessaire
    limit=10,
    return_metadata=MetadataQuery(score=True, explain_score=True),
)

# Generative search — synthèse des résultats par un LLM
réponse = collection.generate.hybrid(
    query="comment optimiser les requêtes lentes dans PostgreSQL ?",
    alpha=0.6,
    single_prompt="Résume cette information en 2 phrases : {contenu}",
    grouped_task="Synthétise les informations suivantes en une réponse structurée avec des recommandations prioritaires.",
    limit=5,
)
print(réponse.generated)  # Réponse LLM basée sur les chunks récupérés
```

---

## 6. FAISS — Indexation Offline et Batch

### Index disponibles et cas d'usage

```python
import faiss
import numpy as np

dimension = 1536

# IndexFlatL2 — recherche exacte, lente mais précision parfaite (baseline)
index_exact = faiss.IndexFlatL2(dimension)
index_exact.add(vecteurs)  # RAM : 4 * N * d bytes

# IndexFlatIP — produit scalaire (cosinus si vecteurs normalisés)
index_ip = faiss.IndexFlatIP(dimension)

# IndexIVFFlat — approximatif, rapide (offline batch)
quantiseur = faiss.IndexFlatL2(dimension)
index_ivf = faiss.IndexIVFFlat(quantiseur, dimension, nlist=1000)
index_ivf.train(vecteurs_train)  # Entraîner avec un sous-ensemble représentatif
index_ivf.add(vecteurs)
index_ivf.nprobe = 50  # Nombre de clusters sondés (recall vs vitesse)

# IndexHNSWFlat — recherche approximative la plus rapide pour petits datasets
index_hnsw = faiss.IndexHNSWFlat(dimension, 32)  # 32 = M
index_hnsw.hnsw.efConstruction = 128
index_hnsw.add(vecteurs)
index_hnsw.hnsw.efSearch = 64

# IndexIVFPQ — compression PQ pour très grands datasets (100M+)
# nlist=1000 clusters, m=32 sous-vecteurs, nbits=8 bits par code
index_pq = faiss.IndexIVFPQ(quantiseur, dimension, 1000, 32, 8)
index_pq.train(vecteurs_train)
index_pq.add(vecteurs)
```

### Sérialisation et usage offline

```python
# Sauvegarder et charger un index FAISS
faiss.write_index(index_hnsw, "index_production.faiss")
index_chargé = faiss.read_index("index_production.faiss")

# Recherche batch optimisée
def recherche_batch(
    requêtes: np.ndarray,
    index: faiss.Index,
    k: int = 10
) -> tuple[np.ndarray, np.ndarray]:
    """Retourne (distances, indices) pour un batch de requêtes."""
    distances, indices = index.search(requêtes.astype(np.float32), k)
    return distances, indices

# GPU (si disponible) — accélération 10-100× pour les gros datasets
if faiss.get_num_gpus() > 0:
    res = faiss.StandardGpuResources()
    index_gpu = faiss.index_cpu_to_gpu(res, 0, index_hnsw)
```

**Quand utiliser FAISS** :
- Traitement offline (pas de mises à jour temps réel).
- Export de vecteurs pour des calculs batch (recommandations, deduplication).
- Prototypage sans serveur (FAISS s'embarque dans le processus Python).
- Pipeline de pre-computing d'index à déployer en lecture seule.

---

## 7. Reranking — Deux Étapes pour un Recall Optimal

### Architecture two-stage retrieval

Le reranking compense la limitation des embeddings (qui encodent un sens global) par un modèle cross-encoder qui compare la requête et chaque document directement :

```
Étape 1 : Retrieval (bi-encoder, rapide)
  Requête → Embedding → ANN search → Top 50-100 candidats

Étape 2 : Reranking (cross-encoder, précis)
  Pour chaque candidat : (Requête, Document) → Score de pertinence
  Top 10 après reranking → Prompt LLM
```

### Cohere Rerank

```python
import cohere

co = cohere.Client(api_key="...")

def reranker_cohere(
    requête: str,
    documents: list[dict],
    top_n: int = 10
) -> list[dict]:
    """Reranker avec Cohere Rerank v3.5 — modèle multilingue."""
    textes = [f"{d['titre']}: {d['contenu'][:500]}" for d in documents]

    résultats = co.rerank(
        query=requête,
        documents=textes,
        model="rerank-v3.5",        # Modèle multilingue, meilleur en 2025-2026
        top_n=top_n,
        return_documents=True,
    )

    return [
        {**documents[r.index], "rerank_score": r.relevance_score}
        for r in résultats.results
    ]
```

### Cross-encoder open-source (self-hosted)

```python
from sentence_transformers import CrossEncoder

# BGE Reranker Large — meilleur cross-encoder open-source en 2025-2026
cross_encoder = CrossEncoder(
    "BAAI/bge-reranker-v2-m3",  # Multilingue, 568M params
    max_length=512,
)

def reranker_local(
    requête: str,
    documents: list[dict],
    top_n: int = 10
) -> list[dict]:
    paires = [(requête, f"{d['titre']}: {d['contenu'][:500]}") for d in documents]
    scores = cross_encoder.predict(paires)

    classés = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )
    return [{"doc": doc, "rerank_score": float(score)} for doc, score in classés[:top_n]]
```

### Impact mesuré du reranking

| Configuration | Recall@10 | NDCG@5 | Latence (ms) |
|---|---|---|---|
| Embedding seul (top 10) | 72% | 0.61 | 25ms |
| Embedding top 50 → Reranker top 10 | 86% | 0.79 | 180ms |
| Embedding top 100 → Reranker top 10 | 89% | 0.82 | 340ms |

---

## 8. Embeddings Multimodaux — CLIP et au-delà

### CLIP pour images et texte

```python
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import requests
from io import BytesIO

modèle = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processeur = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

def encoder_texte(texte: str) -> list[float]:
    """Encoder du texte pour la recherche image-texte."""
    inputs = processeur(text=[texte], return_tensors="pt", padding=True)
    with torch.no_grad():
        embedding = modèle.get_text_features(**inputs)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)  # Normaliser
    return embedding[0].tolist()

def encoder_image(url_image: str) -> list[float]:
    """Encoder une image pour la recherche multimodale."""
    response = requests.get(url_image)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    inputs = processeur(images=image, return_tensors="pt")
    with torch.no_grad():
        embedding = modèle.get_image_features(**inputs)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    return embedding[0].tolist()
```

### Recherche cross-modale dans pgvector

```python
# Table unifiée texte + image avec le même espace vectoriel CLIP
"""
CREATE TABLE contenus (
  id          BIGSERIAL PRIMARY KEY,
  type        TEXT CHECK (type IN ('texte', 'image')),
  contenu     TEXT,           -- Texte ou description de l'image
  url_image   TEXT,           -- Pour les images
  embedding   vector(768),    -- CLIP large = 768 dimensions
  metadata    JSONB
);
CREATE INDEX idx_contenus_hnsw
ON contenus USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 128);
"""

async def recherche_cross_modale(requête_texte: str, k: int = 10):
    """Rechercher des images par description textuelle."""
    embedding_requête = encoder_texte(requête_texte)

    return await db.fetch("""
        SELECT id, type, contenu, url_image,
               1 - (embedding <=> $1::vector) AS score
        FROM contenus
        WHERE type = 'image'
          AND 1 - (embedding <=> $1::vector) >= 0.25
        ORDER BY embedding <=> $1::vector
        LIMIT $2
    """, embedding_requête, k)
```

### Alternatives CLIP pour la production

| Modèle | Dimensions | Forces | Cas d'usage |
|---|---|---|---|
| **CLIP ViT-L/14** | 768 | Standard, bien documenté | Recherche image-texte généraliste |
| **OpenCLIP ViT-H/14** | 1024 | Meilleur recall, open-source | Production self-hosted |
| **SigLIP** (Google) | 1152 | Meilleure performance zéro-shot | Google Cloud, Vertex AI |
| **ImageBind** (Meta) | 1024 | Audio + image + texte + IMU | Recherche multimodale avancée |
| **ALIGN** (Google) | 640 | Entraîné sur très grand corpus | Robustesse aux requêtes bruitées |

---

## 9. Recommandations de Production

### Checklist avant déploiement

```
Architecture
[ ] Index HNSW construit après le chargement complet des données
[ ] ef_search calibré pour le recall cible (tester entre 40 et 200)
[ ] Quantization activée si > 5M vecteurs (scalar int8 par défaut)
[ ] Index partiel ou partitionnement si sélectivité de filtre < 10%
[ ] Vacuum + analyze programmé toutes les heures en production
[ ] Monitoring des dead_tuples pour détecter la fragmentation

Modèle d'embedding
[ ] Évalué sur vos données réelles (pas seulement MTEB)
[ ] Taille de chunk cohérente avec max_tokens du modèle
[ ] Même modèle utilisé à l'indexation ET à la requête (jamais de mixte)
[ ] Version du modèle fixée (pas de mise à jour silencieuse)
[ ] Gestion du re-indexation complète si changement de modèle

Chunking
[ ] Overlap entre 10-20% pour le splitting récursif
[ ] Métadonnées enrichies (source, section, date, langue, chunk_index)
[ ] Taille validée : moyenne et distribution des chunks mesurées
[ ] Chunks vides ou trop courts filtrés (< 50 tokens)

Reranking
[ ] Two-stage si précision critique (top 50 → rerank → top 10)
[ ] Latence du reranker intégrée dans le SLA (ajouter ~150-300ms)
[ ] Fallback sur le classement bi-encoder si le reranker est indisponible
```
