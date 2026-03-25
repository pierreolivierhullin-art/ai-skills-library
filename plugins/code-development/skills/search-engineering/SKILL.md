---
name: search-engineering
version: 1.1.0
description: Expert guide for > Invoke this skill proactively whenever search engineering topics arise — even if not explicitly requested. If there is any search engineering dimension in the conversation, this skill applies.
  Search engineering pgvector PostgreSQL vector similarity semantic search embeddings,
  Elasticsearch OpenSearch full-text search relevance scoring BM25 query DSL,
  Algolia InstantSearch faceted navigation typo tolerance,
  hybrid search dense sparse vectors RRF reciprocal rank fusion,
  embedding models OpenAI text-embedding cohere open-source,
  search analytics query understanding autocomplete,
  RAG retrieval augmented generation search layer pipeline
---

# Search Engineering — Recherche Full-Text, Vectorielle et Sémantique

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu intègres une barre de recherche dans une application (full-text, facettée, sémantique)
- Tu veux utiliser pgvector pour de la recherche par similarité vectorielle dans PostgreSQL
- Les résultats de recherche sont peu pertinents et tu dois améliorer le ranking
- Tu construis un pipeline RAG (Retrieval-Augmented Generation) pour un chatbot ou assistant
- Tu veux comparer Elasticsearch, Algolia, Typesense ou une solution interne
- Tu as des besoins de recherche hybride combinant lexical et sémantique

---

## pgvector — Recherche Vectorielle dans PostgreSQL

```sql
-- Activer l'extension pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Table avec embeddings (1536 dimensions pour text-embedding-3-small)
CREATE TABLE documents (
  id          BIGSERIAL PRIMARY KEY,
  titre       TEXT NOT NULL,
  contenu     TEXT NOT NULL,
  embedding   vector(1536),
  metadata    JSONB DEFAULT '{}',
  créé_à      TIMESTAMPTZ DEFAULT NOW()
);

-- Index HNSW — recommandé en production (vitesse > précision vs IVFFlat)
CREATE INDEX idx_documents_hnsw
ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Index IVFFlat — alternative plus économe en RAM
CREATE INDEX idx_documents_ivfflat
ON documents USING ivfflat (embedding vector_l2_ops)
WITH (lists = 100);  -- Règle : sqrt(nombre_lignes)
```

```typescript
import OpenAI from 'openai';

const openai = new OpenAI();

// Générer un embedding
async function générerEmbedding(texte: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: texte,
    dimensions: 1536,
  });
  return response.data[0].embedding;
}

// Indexer un document
async function indexerDocument(
  titre: string,
  contenu: string,
  metadata: Record<string, unknown> = {}
) {
  const embedding = await générerEmbedding(contenu);

  await prisma.$executeRaw`
    INSERT INTO documents (titre, contenu, embedding, metadata)
    VALUES (
      ${titre},
      ${contenu},
      ${JSON.stringify(embedding)}::vector,
      ${JSON.stringify(metadata)}::jsonb
    )
  `;
}

// Recherche par similarité cosinus
async function rechercherSimilaires(
  requête: string,
  limite = 10,
  seuilScore = 0.7
) {
  const queryEmbedding = await générerEmbedding(requête);

  return prisma.$queryRaw<Array<{
    id: number;
    titre: string;
    contenu: string;
    score: number;
  }>>`
    SELECT
      id,
      titre,
      contenu,
      1 - (embedding <=> ${JSON.stringify(queryEmbedding)}::vector) AS score
    FROM documents
    WHERE 1 - (embedding <=> ${JSON.stringify(queryEmbedding)}::vector) >= ${seuilScore}
    ORDER BY embedding <=> ${JSON.stringify(queryEmbedding)}::vector
    LIMIT ${limite}
  `;
}
```

### Recherche Hybride — RRF (Reciprocal Rank Fusion)

```sql
-- Combiner full-text BM25 + similarité vectorielle avec Reciprocal Rank Fusion
WITH
  -- Résultats full-text
  fulltext AS (
    SELECT
      id,
      ts_rank_cd(
        to_tsvector('french', titre || ' ' || contenu),
        plainto_tsquery('french', 'intelligence artificielle')
      ) AS score,
      ROW_NUMBER() OVER (
        ORDER BY ts_rank_cd(
          to_tsvector('french', titre || ' ' || contenu),
          plainto_tsquery('french', 'intelligence artificielle')
        ) DESC
      ) AS rang
    FROM documents
    WHERE to_tsvector('french', titre || ' ' || contenu)
      @@ plainto_tsquery('french', 'intelligence artificielle')
    LIMIT 50
  ),
  -- Résultats vectoriels (embedding de la requête passé en paramètre)
  vectoriel AS (
    SELECT
      id,
      1 - (embedding <=> '[0.1, 0.2, ...]'::vector) AS score,
      ROW_NUMBER() OVER (
        ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
      ) AS rang
    FROM documents
    LIMIT 50
  ),
  -- Fusion RRF : 1/(k + rang) avec k=60 par convention
  rrf AS (
    SELECT
      COALESCE(f.id, v.id) AS id,
      COALESCE(1.0 / (60 + f.rang), 0) +
      COALESCE(1.0 / (60 + v.rang), 0) AS rrf_score
    FROM
      fulltext f
      FULL OUTER JOIN vectoriel v ON f.id = v.id
  )
SELECT d.id, d.titre, r.rrf_score
FROM rrf r
JOIN documents d ON d.id = r.id
ORDER BY rrf_score DESC
LIMIT 10;
```

---

## Elasticsearch / OpenSearch — Recherche Distribuée

```typescript
import { Client } from '@elastic/elasticsearch';

const client = new Client({ node: process.env.ELASTICSEARCH_URL });

// Créer un index avec mappings et analyseur français
await client.indices.create({
  index: 'produits',
  body: {
    settings: {
      analysis: {
        analyzer: {
          analyseur_fr: {
            type: 'custom',
            tokenizer: 'standard',
            filter: ['lowercase', 'elision_fr', 'stop_fr', 'stemmer_fr'],
          },
        },
        filter: {
          elision_fr: {
            type: 'elision',
            articles_case: true,
            articles: ['l', 'm', 't', 'qu', 'n', 's', 'j', 'd', 'c'],
          },
          stop_fr: { type: 'stop', stopwords: '_french_' },
          stemmer_fr: { type: 'stemmer', language: 'light_french' },
        },
      },
    },
    mappings: {
      properties: {
        nom: {
          type: 'text',
          analyzer: 'analyseur_fr',
          fields: { keyword: { type: 'keyword' } },
        },
        description: { type: 'text', analyzer: 'analyseur_fr' },
        prix: { type: 'float' },
        categorie: { type: 'keyword' },
        tags: { type: 'keyword' },
        note_moyenne: { type: 'float' },
        en_stock: { type: 'boolean' },
      },
    },
  },
});

// Requête full-text avec filtres et agrégations
const { hits } = await client.search({
  index: 'produits',
  body: {
    query: {
      bool: {
        must: [
          {
            multi_match: {
              query: 'smartphone 5G',
              fields: ['nom^3', 'description'],   // nom a 3× le poids
              type: 'best_fields',
              fuzziness: 'AUTO',                  // Tolérance aux fautes
              operator: 'and',
            },
          },
        ],
        filter: [
          { range: { prix: { gte: 200, lte: 1000 } } },
          { term: { en_stock: true } },
        ],
        should: [
          { range: { note_moyenne: { gte: 4.0, boost: 1.5 } } },
        ],
      },
    },
    aggs: {
      par_categorie: { terms: { field: 'categorie', size: 10 } },
      plage_prix: {
        range: {
          field: 'prix',
          ranges: [
            { key: '< 200€', to: 200 },
            { key: '200–500€', from: 200, to: 500 },
            { key: '> 500€', from: 500 },
          ],
        },
      },
    },
    highlight: {
      fields: {
        nom: {},
        description: { fragment_size: 150, number_of_fragments: 2 },
      },
      pre_tags: ['<mark>'],
      post_tags: ['</mark>'],
    },
    from: 0,
    size: 20,
  },
});
```

---

## Algolia — Recherche SaaS Clé-en-Main

```typescript
import algoliasearch from 'algoliasearch';
import { liteClient } from 'algoliasearch/lite';
import InstantSearch from 'react-instantsearch';
import { SearchBox, Hits, RefinementList, RangeInput } from 'react-instantsearch';

// Configuration côté serveur (admin)
const client = algoliasearch(
  process.env.ALGOLIA_APP_ID!,
  process.env.ALGOLIA_ADMIN_KEY!
);
const index = client.initIndex('produits');

// Configurer le ranking et les attributs
await index.setSettings({
  searchableAttributes: [
    'unordered(nom)',
    'description',
    'tags',
  ],
  attributesForFaceting: [
    'categorie',
    'marque',
    'filterOnly(prix)',
    'filterOnly(en_stock)',
  ],
  customRanking: ['desc(ventes_30j)', 'desc(note_moyenne)'],
  typoTolerance: 'min',
  removeStopWords: ['fr', 'en'],
  queryLanguages: ['fr'],
  distinct: true,
  attributeForDistinct: 'référence_produit',
});

// Interface React avec InstantSearch
function PageRecherche() {
  const searchClient = liteClient(
    process.env.NEXT_PUBLIC_ALGOLIA_APP_ID!,
    process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_KEY!
  );

  return (
    <InstantSearch indexName="produits" searchClient={searchClient}>
      <SearchBox placeholder="Rechercher un produit..." />
      <RefinementList attribute="categorie" />
      <RangeInput attribute="prix" />
      <Hits hitComponent={({ hit }) => (
        <div>
          <h3>{hit.nom}</h3>
          <p>{hit.description}</p>
          <span>{hit.prix}€</span>
        </div>
      )} />
    </InstantSearch>
  );
}
```

---

## Pipeline RAG — Couche de Recherche pour LLM

```typescript
// Architecture RAG : Retrieve → Augment → Generate
class PipelineRAG {
  constructor(
    private readonly openai: OpenAI,
    private readonly prisma: PrismaClient
  ) {}

  async répondre(question: string): Promise<{ réponse: string; sources: string[] }> {
    // 1. Récupérer les documents pertinents
    const documents = await this.récupérerContexte(question, 5);

    if (documents.length === 0) {
      return {
        réponse: "Je n'ai pas trouvé d'informations pertinentes pour répondre à cette question.",
        sources: [],
      };
    }

    // 2. Construire le prompt avec le contexte
    const contexte = documents
      .map((d, i) => `[Source ${i + 1}: ${d.titre}]\n${d.contenu}`)
      .join('\n\n---\n\n');

    // 3. Générer la réponse
    const réponse = await this.openai.chat.completions.create({
      model: 'claude-sonnet-4-6',
      messages: [
        {
          role: 'system',
          content: `Tu es un assistant expert. Réponds en te basant uniquement sur les sources fournies.
Si la réponse n'est pas dans les sources, dis-le clairement. Cite les sources utilisées.`,
        },
        {
          role: 'user',
          content: `Question : ${question}\n\nSources disponibles :\n${contexte}`,
        },
      ],
      temperature: 0.1,  // Réponses plus déterministes
    });

    return {
      réponse: réponse.choices[0].message.content ?? '',
      sources: documents.map(d => d.titre),
    };
  }

  private async récupérerContexte(question: string, k: number) {
    const embedding = await générerEmbedding(question);

    return prisma.$queryRaw<Array<{ id: number; titre: string; contenu: string; score: number }>>`
      SELECT id, titre, contenu,
        1 - (embedding <=> ${JSON.stringify(embedding)}::vector) AS score
      FROM documents
      WHERE 1 - (embedding <=> ${JSON.stringify(embedding)}::vector) >= 0.65
      ORDER BY embedding <=> ${JSON.stringify(embedding)}::vector
      LIMIT ${k}
    `;
  }
}
```

---

## Métriques et Tuning de Relevance

```
Signaux de ranking à combiner :
├── Score textuel (BM25, TF-IDF) — Pertinence lexicale
├── Score vectoriel (cosinus) — Pertinence sémantique
├── Freshness boost — Contenu récent favorisé
├── Popularité — Clics, conversions, dwell time
└── Personnalisation — Historique et préférences utilisateur

Métriques d'évaluation :
├── NDCG@K  — Normalized Discounted Cumulative Gain
│             Mesure la qualité du ranking (0 → 1, 1 = parfait)
├── MRR     — Mean Reciprocal Rank
│             Position moyenne du premier résultat pertinent
├── P@K / R@K — Précision et rappel parmi les K premiers
└── CTR     — Click-through rate (proxy de satisfaction)

Outils d'évaluation search :
├── Elasticsearch Learning to Rank (LTR plugin)
├── Qdrant / Weaviate — benchmarks vectoriels
├── Arize AI / Ragas — évaluation RAG
└── A/B testing de ranking : Optimizely, GrowthBook
```

---

## Comparatif des Solutions

```
              pgvector      Elasticsearch    Algolia       Typesense
─────────────────────────────────────────────────────────────────────
Vectoriel     ✅ Natif       🔶 Dense vector  ❌             🔶
Full-text     ✅ PostgreSQL   ✅ BM25 avancé   ✅ Propriétaire ✅
Facettes      🔶 Manuel       ✅ Aggregations  ✅ InstantSearch ✅
Typo tolerance ❌            🔶 fuzziness     ✅ Intégrée     ✅
Infrastructure Self-hosted    Self/Cloud      SaaS           Self/Cloud
Coût          0 (PostgreSQL) Moyen           Élevé (SaaS)   Faible
Idéal pour    RAG/AI apps    Gros volumes    E-commerce     App B2B
```

---

## Références

- `references/vector-search.md` — pgvector avancé (quantification, filtrage pré/post), modèles d'embedding comparés (OpenAI vs Cohere vs open-source), Qdrant, Weaviate, FAISS, chunking strategies pour RAG
- `references/elasticsearch.md` — Elasticsearch en profondeur (aggregations, percolator, mapping explosions, snapshot), OpenSearch, Learning to Rank, relevance tuning avancé
- `references/search-ux.md` — Algolia InstantSearch avancé, Typesense, autocomplete, search-as-you-type, analytics de recherche, A/B testing de ranking, query understanding NLP
- `references/case-studies.md` — 4 cas : migration PostgreSQL + pgvector pour RAG, Elasticsearch 50M docs optimisé, Algolia e-commerce avec personnalisation, recherche hybride production

## See Also

- **backend-db** (`code-development/backend-db`) — Database full-text search
- **data-engineering** (`data-bi/data-engineering`) — Data indexing pipelines
