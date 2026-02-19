# Case Studies — 4 Implémentations de Search en Production

## Overview

Quatre cas réels d'implémentation de search en production, couvrant les défis concrets, les décisions d'architecture et les résultats mesurés : migration d'une base documentaire vers pgvector + RAG, optimisation d'un index Elasticsearch de 50 millions de produits e-commerce, déploiement Algolia avec personnalisation et A/B testing pour du fashion e-commerce, et construction d'une recherche hybride temps réel pour une application de messagerie. Chaque cas documente les décisions clés, les erreurs évitées et les métriques observées.

---

## Cas 1 — Migration vers pgvector + RAG pour un Chatbot Documentaire

### Contexte

Une plateforme juridique SaaS héberge 50 000 documents PDF (codes, jurisprudences, doctrine) indexés dans Elasticsearch. Le produit offre un moteur de recherche full-text classique depuis 5 ans. L'équipe lance un chatbot d'assistance en langage naturel : les avocats posent des questions complexes comme "Quels sont les délais de prescription applicables en cas de vice caché pour un contrat de vente entre professionnels ?" — des questions auxquelles Elasticsearch répond mal car elles nécessitent une compréhension sémantique des concepts juridiques, pas seulement du matching de mots-clés.

Volume : 50 000 documents, moyenne 12 pages par document, 10 000 questions posées par jour. Budget embedding estimé : 5 €/mois maximum. Contrainte : rester sur PostgreSQL déjà en production (pas de nouveau composant d'infrastructure).

### Problème

L'Elasticsearch existant est efficace pour les recherches mot-clé ("prescription vice caché B2B") mais dégrade fortement pour les questions en langage naturel. Trois problèmes concrets mesurés :

- NDCG@5 de 0.62 sur un jeu d'évaluation de 200 questions juridiques annotées par des experts.
- 22% des questions produisent des résultats hors sujet (documents sur d'autres branches du droit).
- Les questions longues (> 15 mots) sont systématiquement moins bien servies que les requêtes courtes.

L'option Elasticsearch + dense_vector est évaluée mais rejetée : l'équipe veut éviter un deuxième moteur à maintenir. La stack existante est PostgreSQL + pgvector (déjà en production pour une autre feature).

### Solution Architecturale

```
PIPELINE D'INGESTION (offline, run hebdomadaire)

PDF (50K docs)
  → Docling (extraction texte + structure)
  → Chunking document-aware (par article/section juridique)
  → Enrichissement métadonnées (code concerné, juridiction, date, type de document)
  → Embedding text-embedding-3-small (batch OpenAI)
  → pgvector (HNSW) + tsvector (index full-text PostgreSQL)

PIPELINE DE REQUÊTE (online, < 500ms)

Question utilisateur
  → Embedding (text-embedding-3-small, ~30ms)
  → Hybrid search RRF (vector + BM25 PostgreSQL, ~40ms)
  → Reranking Cohere Rerank v3.5 (top 50 → top 10, ~150ms)
  → Assemblage prompt (contexte juridique structuré)
  → Claude claude-sonnet-4-6 (génération réponse, ~800ms streaming)
  → Réponse avec citations des articles pertinents
```

### Stratégie de Chunking

Le chunking document-aware par structure juridique est la décision la plus critique. Les documents juridiques (codes, décisions) ont une structure hiérarchique naturelle (Titre → Chapitre → Article) qui sert de guide de découpage :

```python
import re
from dataclasses import dataclass
from typing import Iterator

@dataclass
class ChunkJuridique:
    texte: str
    article_ref: str       # "Art. L225-14" ou "Attendu que (§3)"
    document_source: str
    type_document: str     # "code", "jurisprudence", "doctrine"
    juridiction: str | None
    date_document: str
    niveau_hierarchique: int  # 1=titre, 2=chapitre, 3=article, 4=alinéa

def chunker_document_juridique(
    texte: str,
    source: str,
    type_doc: str,
    max_tokens: int = 800,
) -> Iterator[ChunkJuridique]:
    """
    Découper un document juridique selon sa structure.
    Priorité : conserver l'intégrité des articles (< 800 tokens).
    Fallback : splitting récursif si un article est trop long.
    """
    # Pattern pour les articles de codes (Art. L123-45 ou Article 1234)
    patron_article = re.compile(
        r"(Article\s+\d+[-\w]*|Art\.\s+[LRD]?\d+[-\w]*)\s*[.—]\s*",
        re.IGNORECASE
    )

    # Pattern pour les attendus de jurisprudence
    patron_attendu = re.compile(
        r"(Attendu que|Vu|Considérant que|Sur le moyen)",
        re.IGNORECASE
    )

    patron = patron_article if type_doc == "code" else patron_attendu
    segments = patron.split(texte)

    buffer = ""
    ref_courante = "Préambule"

    for i, segment in enumerate(segments):
        if patron.match(segment):
            if buffer.strip():
                yield from _chunker_segment(buffer, ref_courante, source, type_doc, max_tokens)
            ref_courante = segment.strip()
            buffer = ""
        else:
            buffer += segment

    if buffer.strip():
        yield from _chunker_segment(buffer, ref_courante, source, type_doc, max_tokens)
```

### Paramètres Index HNSW

Après calibrage sur le dataset de 50 000 documents (650 000 chunks au total après découpage) :

```sql
-- Index HNSW calibré pour 650K vecteurs, recall@10 ≥ 95%
CREATE INDEX idx_chunks_hnsw
ON chunks_juridiques USING hnsw (embedding vector_cosine_ops)
WITH (
  m = 16,             -- 16 connexions par nœud : équilibre performance/RAM
  ef_construction = 128  -- Graphe de qualité, indexation en 4h pour 650K vecteurs
);

-- ef_search = 100 mesuré comme optimal (recall 97%, latence 45ms)
-- ef_search = 40 (défaut) : recall 93%, latence 28ms → inacceptable pour ce cas
ALTER SYSTEM SET hnsw.ef_search = 100;

-- Quantization scalaire (int8) : RAM 6.5 GB → 1.7 GB, recall@10 baisse de 97% → 95%
-- Décision : NE PAS activer (1.7% de recall en moins inacceptable en contexte juridique)
```

### Pipeline de Requête — Hybrid Search RRF

```sql
-- Hybrid search : vector (sémantique) + BM25 (mots-clés exacts) avec RRF
WITH
  vectoriel AS (
    SELECT
      id,
      document_source,
      article_ref,
      texte,
      ROW_NUMBER() OVER (ORDER BY embedding <=> $1::vector) AS rang
    FROM chunks_juridiques
    WHERE type_document = $2   -- Filtre pré-index (index partiel par type)
    ORDER BY embedding <=> $1::vector
    LIMIT 50
  ),
  fulltext AS (
    SELECT
      id,
      ROW_NUMBER() OVER (
        ORDER BY ts_rank_cd(
          to_tsvector('french', texte),
          plainto_tsquery('french', $3)
        ) DESC
      ) AS rang
    FROM chunks_juridiques
    WHERE to_tsvector('french', texte) @@ plainto_tsquery('french', $3)
      AND type_document = $2
    LIMIT 50
  ),
  rrf AS (
    SELECT
      COALESCE(v.id, f.id) AS id,
      COALESCE(1.0 / (60 + v.rang), 0) +
      COALESCE(1.0 / (60 + f.rang), 0) AS score_rrf
    FROM vectoriel v
    FULL OUTER JOIN fulltext f USING (id)
  )
SELECT
  c.id, c.texte, c.article_ref, c.document_source, c.date_document,
  r.score_rrf
FROM rrf r
JOIN chunks_juridiques c ON c.id = r.id
ORDER BY score_rrf DESC
LIMIT 50;  -- 50 candidats pour le reranker
```

### Résultats Mesurés

Évaluation sur le jeu de 200 questions juridiques annotées par 3 experts (consensus de pertinence) :

| Métrique | Elasticsearch (avant) | pgvector hybrid (après) | Amélioration |
|---|---|---|---|
| **NDCG@5** | 0.62 | 0.84 | +35% |
| **Recall@10** | 68% | 91% | +34% |
| **Précision@5** | 51% | 76% | +49% |
| **Questions hors sujet** | 22% | 4% | -82% |
| **Latence P95** | 180ms | 380ms (avec reranking) | +111% |
| **Coût embedding/mois** | — | 43 €/mois | — |

La latence augmente mais reste dans le SLA (< 500ms P95). Le coût de 43 €/mois est largement sous le budget. Le NDCG@5 de 0.84 est suffisant pour que le chatbot soit déployé en production.

### Leçons Apprises

- Le chunking document-aware est la décision la plus impactante — découper par articles juridiques plutôt que par taille fixe améliore le NDCG@5 de 0.71 → 0.84 (vs 0.62 → 0.71 avec le chunking fixe). Le respect de la structure sémantique du document vaut l'investissement en développement.
- Le reranking Cohere justifie son coût et sa latence (+150ms, +$0.002/requête) : sans reranking, NDCG@5 de 0.77 ; avec reranking, 0.84. Le gain de +9% est significatif pour du contenu juridique où la précision prime.
- Rester sur PostgreSQL + pgvector simplifie radicalement les opérations : pas de cluster Elasticsearch à maintenir, les mises à jour de documents sont des UPDATEs SQL standard, les permissions sont gérées par RLS existant.
- text-embedding-3-small à 1536 dimensions performe identiquement à text-embedding-3-large à 3072 dimensions sur ce corpus juridique français (NDCG@5 : 0.84 vs 0.85). L'économie de 6,5× sur le coût d'embedding est justifiée.

---

## Cas 2 — Elasticsearch 50M Produits E-commerce Optimisé

### Contexte

Une marketplace généraliste héberge 50 millions de SKUs répartis sur 3 000 vendeurs. Chaque produit peut avoir jusqu'à 200 attributs dynamiques (taille, couleur, matière, compatibilité, certification, etc.) qui varient selon la catégorie. Exigences : P99 < 500ms pour les recherches facettées, réindexation complète sans downtime, budget infrastructure contraint (pas de cluster Elasticsearch premium).

Stack initiale : Elasticsearch 7.x, 6 nœuds data de 32 GB RAM, index de 50M documents avec mapping dynamique par défaut.

### Problème

Trois problèmes critiques en production depuis 8 mois :

1. **Mapping explosion** : les attributs dynamiques créent plus de 12 000 champs dans le mapping. Chaque nouveau vendeur avec des attributs inédits aggrave la situation. Le mapping dépasse 10 MB et ralentit le bootstrap du cluster.

2. **Requêtes lentes** : P99 de 1200ms sur les recherches avec agrégations de facettes. L'analyse des slow logs révèle que les fielddata sur les attributs dynamiques provoquent des circuit breaker trips réguliers.

3. **Shard hot spots** : un shard concentre 40% du trafic (catégorie Électronique). Les requêtes sur cette catégorie saturent le nœud portant ce shard.

### Solution — Refactoring du Mapping

**Étape 1 : Migrer les attributs dynamiques vers le type `flattened`**

```json
// AVANT : mapping explosion avec attributs dynamiques
{
  "mappings": {
    "properties": {
      "nom": { "type": "text" },
      "attributs_couleur_principale": { "type": "keyword" },
      "attributs_taille_eu": { "type": "keyword" },
      "attributs_compatible_iphone_13": { "type": "boolean" },
      // ... 11 997 autres champs dynamiques générés automatiquement
    }
  }
}

// APRÈS : type flattened pour tous les attributs variables
{
  "mappings": {
    "dynamic": "strict",  // Bloquer tout nouveau champ non déclaré
    "properties": {
      "nom": { "type": "text", "analyzer": "analyseur_fr" },
      "nom_keyword": { "type": "keyword" },
      "description": { "type": "text", "analyzer": "analyseur_fr" },
      "prix_centimes": { "type": "integer" },
      "categorie_id": { "type": "keyword" },
      "vendeur_id": { "type": "keyword" },
      "en_stock": { "type": "boolean" },
      "ventes_30j": { "type": "integer" },
      "note_moyenne": { "type": "half_float" },
      "date_création": { "type": "date" },
      "attributs": {
        "type": "flattened"
        // Tous les attributs dynamiques indexés ici
        // Filtrage : { "term": { "attributs.couleur": "rouge" } }
      }
    }
  }
}
```

**Résultat du refactoring mapping** : 12 000+ champs → 11 champs. Mapping réduit de 10 MB → 8 KB. Bootstrap du cluster : 4 min → 25 secondes.

### Solution — Shard Allocation et Hot Spots

```json
// Allocation explicite des catégories haute-fréquence sur des nœuds dédiés
// Tag les nœuds data avec des attributs personnalisés
// elasticsearch.yml sur les nœuds dédiés :
// node.attr.tier: hot

PUT /produits_electronique/_settings
{
  "index.routing.allocation.require.tier": "hot"
}

// Index template avec shard sizing calibré
PUT /_index_template/template_produits
{
  "index_patterns": ["produits_*"],
  "template": {
    "settings": {
      "number_of_shards": 6,     // 50M docs × 0.5 KB/doc ≈ 25 GB → 6 shards de ~4 GB
      "number_of_replicas": 1,
      "index.refresh_interval": "5s",          // Moins fréquent que le défaut 1s
      "index.max_result_window": 10000,
      "index.codec": "best_compression"        // Économie de 30% espace disque
    }
  }
}
```

### Pipeline d'Indexation Bulk

Le pipeline initial indexait 1 document à la fois via l'API REST. Refactoring vers du bulk streaming avec Kafka :

```python
from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk
from kafka import KafkaConsumer
import json, time

es = Elasticsearch(["http://es-01:9200", "http://es-02:9200"],
                   http_compress=True, request_timeout=30)

def transformer_produit(produit_raw: dict) -> dict:
    """Normaliser un produit avant l'indexation."""
    return {
        "_index": f"produits_{produit_raw['categorie_id'][:8]}",
        "_id": produit_raw["sku"],
        "_source": {
            "nom": produit_raw["nom"],
            "nom_keyword": produit_raw["nom"][:256],
            "description": produit_raw.get("description", "")[:5000],
            "prix_centimes": int(produit_raw["prix"] * 100),
            "categorie_id": produit_raw["categorie_id"],
            "vendeur_id": produit_raw["vendeur_id"],
            "en_stock": produit_raw["quantite_stock"] > 0,
            "ventes_30j": produit_raw.get("ventes_30j", 0),
            "note_moyenne": produit_raw.get("note_moyenne", 0),
            "date_création": produit_raw["created_at"],
            "attributs": produit_raw.get("attributs", {}),  # Tous les attributs dynamiques
        }
    }

consumer = KafkaConsumer(
    "produits_updates",
    bootstrap_servers=["kafka-01:9092"],
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    max_poll_records=5000,
)

buffer = []
BATCH_SIZE = 2000

for message in consumer:
    buffer.append(transformer_produit(message.value))

    if len(buffer) >= BATCH_SIZE:
        succès, erreurs = 0, 0
        for ok, _ in parallel_bulk(es, buffer, thread_count=4, chunk_size=500):
            if ok: succès += 1
            else: erreurs += 1
        print(f"Batch indexé : {succès} OK, {erreurs} erreurs")
        buffer.clear()
```

### Stratégie Zero-Downtime Reindex

La migration du mapping (passage au type `flattened`) nécessite un reindex complet sans interrompre le service :

```python
def reindex_zero_downtime(
    es: Elasticsearch,
    alias: str = "produits",
    nouveau_mapping: dict = NOUVEAU_MAPPING,
) -> str:
    import time

    # 1. Identifier l'index actuel pointé par l'alias
    alias_info = es.indices.get_alias(name=alias)
    index_actuel = list(alias_info.keys())[0]

    # 2. Créer le nouvel index avec le mapping corrigé
    timestamp = int(time.time())
    nouvel_index = f"produits_v2_{timestamp}"
    es.indices.create(index=nouvel_index, body={"mappings": nouveau_mapping, "settings": SETTINGS})

    # 3. Lancer le reindex asynchrone avec throttle (500 docs/s pour ne pas saturer)
    tâche = es.reindex(
        body={"source": {"index": index_actuel, "size": 2000}, "dest": {"index": nouvel_index}},
        wait_for_completion=False,
        requests_per_second=1000,
        slices="auto",  # Paralléliser sur le nombre de shards source
    )

    # 4. Surveiller la progression
    task_id = tâche["task"]
    while True:
        statut = es.tasks.get(task_id=task_id)
        info = statut["task"]["status"]
        print(f"Reindex : {info['created']+info['updated']}/{info['total']} docs "
              f"({info.get('requests_per_second', 0):.0f} docs/s)")
        if statut["completed"]:
            break
        time.sleep(30)

    # 5. Basculer l'alias atomiquement
    es.indices.update_aliases(body={
        "actions": [
            {"remove": {"index": index_actuel, "alias": alias}},
            {"add": {"index": nouvel_index, "alias": alias}},
        ]
    })
    print(f"Alias '{alias}' basculé vers {nouvel_index}")
    return nouvel_index
```

### Résultats Mesurés

| Métrique | Avant optimisation | Après optimisation | Amélioration |
|---|---|---|---|
| **Latence P99 recherche facettée** | 1 200ms | 115ms | -90% |
| **Latence P50 recherche simple** | 120ms | 22ms | -82% |
| **Durée reindex complet (50M docs)** | 2h00 | 18min | -85% |
| **Taille mapping** | 10 MB | 8 KB | -99.9% |
| **Circuit breaker trips/jour** | 12-20 | 0 | -100% |
| **Bootstrap cluster** | 4 min | 25 sec | -90% |
| **RAM fielddata utilisée** | 18 GB | 2.1 GB | -88% |

### Leçons Apprises

- Le type `flattened` est la solution à la mapping explosion pour les attributs produits dynamiques. Passer de 12 000 champs à 1 champ `flattened` n'est pas seulement une optimisation de mapping : c'est une transformation fondamentale de la consommation mémoire (fielddata, segment metadata) qui explique la majorité des gains de performance.
- Le throttle du reindex (`requests_per_second=1000`) est indispensable en production : sans lui, le reindex saturait le cluster et dégradait les P99 de 1200ms à 4000ms pour les utilisateurs. Le reindex avec throttle prend 18 min au lieu de 10 min, mais sans impact utilisateur.
- Les shard hot spots se traitent en amont dans le design de l'index, pas en aval. Partitionner les index par catégorie (produits_electronique, produits_mode, etc.) et allouer les index haute-fréquence sur des nœuds dédiés (`node.attr.tier`) est plus efficace que de chercher à équilibrer la charge après coup.

---

## Cas 3 — Algolia E-commerce avec Personnalisation et A/B Testing

### Contexte

Un site de mode (fashion e-commerce) avec 2 millions de produits actifs, 100 000 sessions par jour, 65% du trafic sur mobile. L'équipe produit identifie un problème de pertinence : le ranking générique ne tient pas compte des tendances, des stocks, ni des préférences individuelles. Taux de clics sur les 3 premiers résultats (CTR@3) : 31%. Taux de zéro-click (l'utilisateur fait une recherche et quitte sans cliquer) : 38%.

Décision : migrer d'un moteur interne Elasticsearch peu maintenu vers Algolia pour bénéficier des fonctionnalités de merchandising et de personnalisation sans développement custom.

### Analyse des Données Avant Migration

```python
import pandas as pd
import numpy as np

# Analyse des recherches sur 30 jours (données analytics exportées)
df = pd.read_csv("recherches_30j.csv")

print("Top 20 requêtes par volume :")
print(df.groupby("query")["session_id"].count().sort_values(ascending=False).head(20))

print("\nRequêtes avec taux zero-click > 50% :")
taux_zero_click = (df[df["position_clic"].isna()]
    .groupby("query")["session_id"].count() /
    df.groupby("query")["session_id"].count()
).sort_values(ascending=False)
print(taux_zero_click[taux_zero_click > 0.5].head(20))

# Distribution des positions de clic
print("\nDistribution des clics par position :")
print(df["position_clic"].value_counts().head(10))
# Résultat : 60% des clics sur position 1, 20% sur position 2, 10% sur position 3
# → Le ranking a un fort impact sur les conversions
```

### Configuration du Ranking Algolia

```javascript
const { algoliasearch } = require("algoliasearch");

const client = algoliasearch(APP_ID, ADMIN_KEY);
const index = client.initIndex("produits");

// Ranking avec signaux business (après analyse des données)
await index.setSettings({
  // Attributs dans l'ordre de priorité textuelle
  searchableAttributes: [
    "unordered(nom)",        // unordered : même importance que le champ ait 1 ou 5 correspondances
    "marque",
    "tags",
    "description",
  ],

  // Custom ranking : après le score textuel, trier par ces critères dans l'ordre
  customRanking: [
    "desc(ventes_7j)",              // Ventes récentes > ventes historiques (mode = saisonnier)
    "desc(score_tendance)",          // Score de tendance calculé quotidiennement
    "asc(jours_rupture_prévue)",    // Proximité de la rupture de stock → urgence
    "desc(note_moyenne)",
  ],

  // Facettes disponibles pour les filtres
  attributesForFaceting: [
    "filterOnly(prix)",
    "categorie",
    "marque",
    "couleur",
    "taille",
    "filterOnly(en_stock)",
    "filterOnly(livraison_express)",
  ],

  // Réduction des doublons (même modèle en différentes couleurs)
  distinct: true,
  attributeForDistinct: "référence_modèle",

  // Paramètres de typo et langue
  queryLanguages: ["fr"],
  removeStopWords: ["fr"],
  typoTolerance: "min",
  minWordSizefor1Typo: 5,
});
```

### Query Rules — Gestion des Campagnes

```javascript
// Règle : mettre en avant la collection capsule pendant les soldes
await index.saveRule({
  objectID: "campagne_soldes_été_2025",
  conditions: [
    { anchoring: "is", pattern: "" },  // Toutes les requêtes
    { context: "page_soldes" },        // Seulement sur la page soldes
  ],
  consequence: {
    filterPromotes: true,
    promote: [
      { objectID: "capsule_été_2025_001", position: 1 },
      { objectID: "capsule_été_2025_002", position: 2 },
    ],
    params: {
      filters: "collection:soldes_été_2025 OR score_remise >= 30",
    },
  },
  validity: [
    { from: 1751328000, until: 1753920000 }  // Du 1er au 31 juillet 2025
  ],
  enabled: true,
  description: "Soldes été 2025 — mise en avant collection capsule + filtrage remises",
});

// Règle : rediriger "nouveautés" vers la page dédiée
await index.saveRule({
  objectID: "redirect_nouveautés",
  conditions: [
    { anchoring: "contains", pattern: "nouveau" },
    { anchoring: "contains", pattern: "nouveauté" },
  ],
  consequence: {
    redirect: { url: "https://example.com/nouveautes" },
  },
});
```

### A/B Test — 3 Variantes de Ranking

```javascript
// Test A/B/C sur 3 stratégies de ranking
// Hypothèse : le ranking orienté stock-urgence améliore les conversions

// Index A : ranking par ventes (contrôle)
await clientA.initIndex("produits_ab_ventes").setSettings({
  customRanking: ["desc(ventes_7j)", "desc(note_moyenne)"],
});

// Index B : ranking par tendance algorithmique
await clientB.initIndex("produits_ab_tendance").setSettings({
  customRanking: ["desc(score_tendance)", "desc(ventes_7j)", "desc(note_moyenne)"],
});

// Index C : ranking avec signal d'urgence stock
await clientC.initIndex("produits_ab_urgence").setSettings({
  customRanking: [
    "desc(ventes_7j)",
    "asc(jours_rupture_prévue)",  // Produits proches rupture en priorité
    "desc(note_moyenne)",
  ],
});

// Créer l'A/B test sur 3 variantes, 33% chacune
const abTest = await client.addABTest({
  name: "Ranking ventes vs tendance vs urgence stock — Juillet 2025",
  variants: [
    { index: "produits_ab_ventes",   trafficPercentage: 34, description: "Contrôle — ventes 7j" },
    { index: "produits_ab_tendance", trafficPercentage: 33, description: "Variante tendance algo" },
    { index: "produits_ab_urgence",  trafficPercentage: 33, description: "Variante urgence stock" },
  ],
  endAt: "2025-08-01T00:00:00.000Z",
});
```

### Personnalisation et Résultats du Test

```javascript
// Résultats de l'A/B test après 14 jours (1,4M sessions par variante)
const résultats = await client.getABTest({ id: abTest.abTestID });

/*
Résultats mesurés :
┌─────────────────────────────────┬──────────┬──────────┬────────────┐
│ Métrique                        │ Contrôle │ Tendance │ Urgence    │
│                                 │ (ventes) │          │ (stock)    │
├─────────────────────────────────┼──────────┼──────────┼────────────┤
│ CTR@3                           │ 31%      │ 38%      │ 33%        │
│ Taux conversion                 │ 3.2%     │ 3.8%     │ 3.5%       │
│ Taux zero-click                 │ 38%      │ 22%      │ 31%        │
│ Valeur panier moyen             │ 89€      │ 91€      │ 96€        │
│ Significativité statistique     │ —        │ 99.7%    │ 95.2%      │
└─────────────────────────────────┴──────────┴──────────┴────────────┘
→ Variante Tendance gagnante : CTR+23%, conversion+19%, zero-click-41%
*/

// Déployer la variante gagnante comme index de production
await client.stopABTest({ id: abTest.abTestID });
// Mettre à jour les settings de l'index de production avec le ranking gagnant
```

### Résultats Consolidés (6 mois post-déploiement)

| Métrique | Avant (Elasticsearch) | Après (Algolia + A/B + Perso) | Évolution |
|---|---|---|---|
| **CTR@3** | 31% | 38% | +23% |
| **Taux de conversion** | 3.2% | 3.4% | +6% |
| **Taux zero-click** | 38% | 22% | -42% |
| **Temps de développement search** | 2 développeurs temps plein | 0.5 développeur | -75% |
| **Latence P95** | 380ms | < 5ms | -99% |
| **Coût infrastructure** | Serveurs ES (~2 000€/mois) | Algolia (~3 500€/mois) | +75% |

Le coût Algolia est plus élevé que l'infrastructure auto-gérée, mais l'économie sur le temps développeur (1.5 développeur × ~70K€/an = 105K€/an d'économie) justifie largement la différence de 18 000€/an de surcoût.

### Leçons Apprises

- Le A/B testing révèle des insights non intuitifs : le ranking par "tendance algorithmique" surpasse le ranking par ventes historiques en mode, car les ventes passées amplifient les biais saisonniers (des produits d'été surclassent des produits pertinents en hiver). Tester avant de déployer une intuition métier.
- La personnalisation Algolia génère peu de gains seule (+2-3% de CTR) — c'est la combinaison ranking de base de qualité + merchandising + personnalisation qui produit les résultats mesurés. Construire dans cet ordre.
- Le taux zero-click est le meilleur signal de qualité du ranking pour l'e-commerce — plus sensible et plus facile à interpréter que le CTR ou la conversion. Un zero-click de 38% signifie que 38% des sessions de recherche finissent sans engagement, ce qui indique un ranking fondamentalement inadapté.

---

## Cas 4 — Recherche Hybride Temps Réel pour une App de Messagerie

### Contexte

Une application de messagerie interne pour les équipes (type Slack) héberge l'historique de conversations de 5 000 entreprises clientes. Les utilisateurs veulent rechercher dans leurs messages avec deux types de requêtes : recherche exacte ("trouver le message où Pierre a mentionné la deadline du projet X") et recherche sémantique ("trouver les discussions sur les problèmes de performance API"). De plus, les messages sont confidentiels — un utilisateur ne peut voir que les messages des canaux auxquels il a accès.

Contraintes : < 50ms P95 pour les résultats, permissions 100% correctes (zéro fuite entre canaux/entreprises), migration sans downtime depuis l'ancienne implémentation ILIKE PostgreSQL.

### Architecture de la Table Messages

```sql
-- Table messages avec full-text et vector dans la même table PostgreSQL
CREATE TABLE messages (
  id              BIGSERIAL PRIMARY KEY,
  channel_id      BIGINT NOT NULL REFERENCES channels(id),
  workspace_id    BIGINT NOT NULL,
  auteur_id       BIGINT NOT NULL REFERENCES users(id),
  contenu         TEXT NOT NULL,
  créé_à          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Full-text search : tsvector pré-calculé (mis à jour par trigger)
  contenu_tsv     TSVECTOR GENERATED ALWAYS AS (
    to_tsvector('french', contenu)
  ) STORED,

  -- Semantic search : embedding généré de manière asynchrone
  contenu_emb     vector(1536),
  emb_généré_à    TIMESTAMPTZ  -- Null si l'embedding n'est pas encore calculé
);

-- Index full-text GIN
CREATE INDEX idx_messages_tsv ON messages USING GIN (contenu_tsv);

-- Index vectoriel HNSW — construit après chargement initial
CREATE INDEX idx_messages_hnsw
ON messages USING hnsw (contenu_emb vector_cosine_ops)
WITH (m = 16, ef_construction = 64);  -- ef_construction réduit : messages courts

-- Index sur les colonnes de filtrage (requêtes fréquentes)
CREATE INDEX idx_messages_channel ON messages (channel_id, créé_à DESC);
CREATE INDEX idx_messages_workspace ON messages (workspace_id, créé_à DESC);

-- Partial index pour le vecteur : ignorer les messages sans embedding
CREATE INDEX idx_messages_hnsw_v2
ON messages USING hnsw (contenu_emb vector_cosine_ops)
WHERE contenu_emb IS NOT NULL;
```

### Row-Level Security — Permissions Correctes à 100%

```sql
-- RLS : chaque utilisateur ne voit que les messages de ses canaux
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Politique : accès uniquement si l'utilisateur est membre du canal
CREATE POLICY messages_par_canal ON messages
  FOR SELECT
  USING (
    channel_id IN (
      SELECT channel_id
      FROM channel_members
      WHERE user_id = current_setting('app.current_user_id')::bigint
        AND accepté_à IS NOT NULL  -- Membre actif seulement
    )
    AND workspace_id = current_setting('app.current_workspace_id')::bigint
  );

-- Fonction utilitaire pour définir le contexte avant chaque requête
CREATE OR REPLACE FUNCTION set_search_context(
  p_user_id BIGINT,
  p_workspace_id BIGINT
) RETURNS VOID AS $$
BEGIN
  PERFORM set_config('app.current_user_id', p_user_id::text, true);
  PERFORM set_config('app.current_workspace_id', p_workspace_id::text, true);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### Requête de Recherche Hybride avec Permissions

```sql
-- Hybrid search avec RLS intégré : l'utilisateur ne voit que ses canaux
-- Les index HNSW et GIN sont utilisés, le filtre RLS s'applique automatiquement
CREATE OR REPLACE FUNCTION rechercher_messages(
  p_requête TEXT,
  p_embedding vector(1536),
  p_limite INT DEFAULT 20,
  p_avant_message_id BIGINT DEFAULT NULL  -- Pour la pagination avec search_after
) RETURNS TABLE (
  id BIGINT,
  channel_id BIGINT,
  auteur_id BIGINT,
  contenu TEXT,
  créé_à TIMESTAMPTZ,
  score_rrf FLOAT,
  extrait TEXT  -- Passage en surbrillance
) AS $$
WITH
  -- Recherche vectorielle (sémantique)
  vectorielle AS (
    SELECT
      m.id,
      ROW_NUMBER() OVER (ORDER BY m.contenu_emb <=> p_embedding) AS rang
    FROM messages m
    WHERE m.contenu_emb IS NOT NULL
      AND (p_avant_message_id IS NULL OR m.id < p_avant_message_id)
    ORDER BY m.contenu_emb <=> p_embedding
    LIMIT 100  -- Le RLS filtre automatiquement sur channel_id
  ),
  -- Recherche full-text (mots-clés exacts, noms propres)
  fulltext AS (
    SELECT
      m.id,
      ROW_NUMBER() OVER (
        ORDER BY ts_rank_cd(m.contenu_tsv, plainto_tsquery('french', p_requête)) DESC
      ) AS rang
    FROM messages m
    WHERE m.contenu_tsv @@ plainto_tsquery('french', p_requête)
      AND (p_avant_message_id IS NULL OR m.id < p_avant_message_id)
    ORDER BY ts_rank_cd(m.contenu_tsv, plainto_tsquery('french', p_requête)) DESC
    LIMIT 100
  ),
  -- Fusion RRF
  fusionnés AS (
    SELECT
      COALESCE(v.id, f.id) AS id,
      COALESCE(1.0 / (60 + v.rang), 0) + COALESCE(1.0 / (60 + f.rang), 0) AS score_rrf
    FROM vectorielle v
    FULL OUTER JOIN fulltext f ON v.id = f.id
  )
SELECT
  m.id, m.channel_id, m.auteur_id, m.contenu, m.créé_à,
  fu.score_rrf,
  ts_headline(
    'french', m.contenu,
    plainto_tsquery('french', p_requête),
    'StartSel=<mark>, StopSel=</mark>, MaxWords=20, MinWords=5'
  ) AS extrait
FROM fusionnés fu
JOIN messages m ON m.id = fu.id
ORDER BY fu.score_rrf DESC
LIMIT p_limite;
$$ LANGUAGE SQL STABLE SECURITY INVOKER;
```

### Indexation Temps Réel avec Queue Asynchrone

Générer les embeddings de manière asynchrone sans bloquer l'écriture des messages :

```typescript
import { Queue, Worker } from "bullmq";
import Redis from "ioredis";
import OpenAI from "openai";
import { Pool } from "pg";

const redis = new Redis({ host: "localhost", port: 6379 });
const embeddingQueue = new Queue("embedding_messages", { connection: redis });
const openai = new OpenAI();
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// Après l'insertion d'un message, enqueuer l'embedding
async function créerMessage(
  channelId: number,
  auteurId: number,
  contenu: string
): Promise<{ id: number }> {
  const { rows } = await pool.query(
    "INSERT INTO messages (channel_id, auteur_id, contenu) VALUES ($1, $2, $3) RETURNING id",
    [channelId, auteurId, contenu]
  );
  const messageId = rows[0].id;

  // Enqueuer l'embedding (délai court pour prioriser les messages récents)
  await embeddingQueue.add(
    "générer_embedding",
    { messageId, contenu },
    { delay: 500, attempts: 3, backoff: { type: "exponential", delay: 2000 } }
  );

  return { id: messageId };
}

// Worker d'embedding (processus séparé, peut scaler horizontalement)
const worker = new Worker(
  "embedding_messages",
  async (job) => {
    const { messageId, contenu } = job.data;

    const response = await openai.embeddings.create({
      model: "text-embedding-3-small",
      input: contenu,
      dimensions: 1536,
    });

    const embedding = response.data[0].embedding;

    await pool.query(
      "UPDATE messages SET contenu_emb = $1::vector, emb_généré_à = NOW() WHERE id = $2",
      [JSON.stringify(embedding), messageId]
    );
  },
  { connection: redis, concurrency: 10 }  // 10 embeddings en parallèle
);
```

### Interface de Recherche — Debounce et Pagination

```typescript
// Pagination avec search_after (curseur) — performant pour les grands datasets
// Évite le OFFSET qui dégrade en O(n) sur les grandes tables

interface RésultatRecherche {
  messages: Message[];
  curseur: number | null;  // ID du dernier message retourné (pour la page suivante)
  total_estimé: number;
}

async function rechercherMessages(
  query: string,
  workspaceId: number,
  userId: number,
  curseur: number | null = null,
  limite: number = 20
): Promise<RésultatRecherche> {
  // Générer l'embedding de la requête
  const { data } = await openai.embeddings.create({
    model: "text-embedding-3-small",
    input: query,
    dimensions: 1536,
  });
  const embedding = data[0].embedding;

  // Définir le contexte RLS
  await pool.query("SELECT set_search_context($1, $2)", [userId, workspaceId]);

  // Exécuter la recherche hybride avec pagination curseur
  const { rows } = await pool.query(
    "SELECT * FROM rechercher_messages($1, $2::vector, $3, $4)",
    [query, JSON.stringify(embedding), limite, curseur]
  );

  return {
    messages: rows,
    curseur: rows.length === limite ? rows[rows.length - 1].id : null,
    total_estimé: rows.length,
  };
}
```

### Migration Sans Downtime depuis ILIKE

```sql
-- Migration en 4 étapes sans downtime

-- Étape 1 : ajouter les nouvelles colonnes sans données
ALTER TABLE messages ADD COLUMN contenu_emb vector(1536);
ALTER TABLE messages ADD COLUMN emb_généré_à TIMESTAMPTZ;

-- Étape 2 : backfill des embeddings (batch par 1000, en tâche de fond)
-- Script Python exécuté en parallèle avec la production

-- Étape 3 : créer les index une fois le backfill terminé
CREATE INDEX CONCURRENTLY idx_messages_hnsw
ON messages USING hnsw (contenu_emb vector_cosine_ops)
WHERE contenu_emb IS NOT NULL;

-- Étape 4 : activer le RLS (non activé au départ pour les performances de migration)
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Pas de changement applicatif requis : la nouvelle fonction SQL coexiste avec l'ancienne
-- La bascule se fait dans l'application, feature flag par workspace
```

### Résultats Mesurés

| Métrique | Avant (ILIKE PostgreSQL) | Après (Hybrid pgvector + RLS) | Amélioration |
|---|---|---|---|
| **Latence P95** | 320ms | 47ms | -85% |
| **Précision sémantique** | N/A (ILIKE = mots exacts) | 82% satisfaction utilisateurs | +∞ |
| **Correctness permissions** | 100% | 100% | Maintenu |
| **Résultats pertinents @10** | 43% (sondage 200 utilisateurs) | 78% | +81% |
| **Messages en queue embedding** | — | < 500ms délai (P95) | — |
| **Temps de migration** | — | 0 downtime | — |

### Leçons Apprises

- Le RLS PostgreSQL est la solution correcte pour les permissions en recherche — plus fiable que le filtrage applicatif (qui peut avoir des bugs), plus performant que le post-filtrage (qui nécessite de récupérer plus de résultats), et automatiquement appliqué sur toutes les requêtes SQL, y compris celles des requêtes hybrides complexes.
- L'indexation asynchrone des embeddings est un pattern de production solide : le message est disponible immédiatement après l'écriture (avec recherche full-text seule), et l'embedding arrive quelques secondes plus tard pour enrichir la recherche sémantique. Les utilisateurs ne perçoivent pas ce délai.
- La pagination par curseur (`search_after` / ID du dernier élément) est critique pour les applications de messagerie : OFFSET devient inacceptable dès 10 000+ messages dans un workspace, car PostgreSQL doit parcourir tous les enregistrements précédents pour chaque page.
- La migration feature-flag par workspace permet un rollout progressif et la correction de bugs sans impacter tous les utilisateurs. Déployer pour les workspaces de test internes d'abord, puis étendre progressivement après validation.
