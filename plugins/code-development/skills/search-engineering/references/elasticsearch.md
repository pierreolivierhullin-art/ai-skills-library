# Elasticsearch en Profondeur — Agrégations, Performance et Relevance Tuning

## Overview

Ce document de référence couvre Elasticsearch en production : mappings avancés (dynamic templates, nested, join), agrégations complexes avec exemples de code, percolator pour les notifications temps réel, optimisation de performance (shard sizing, bulk indexing, circuit breakers), relevance tuning (function_score, Learning to Rank), cross-cluster search, OpenSearch et ses différences, snapshot/restore, et monitoring opérationnel. Utiliser ce guide pour exploiter Elasticsearch au-delà du full-text basique.

---

## 1. Mappings Avancés

### Dynamic templates

Les dynamic templates permettent de contrôler comment Elasticsearch mappe automatiquement les nouveaux champs selon des patterns de nom ou de type :

```json
PUT /produits
{
  "mappings": {
    "dynamic_templates": [
      {
        "chaînes_en_keyword": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "text",
            "analyzer": "analyseur_fr",
            "fields": {
              "keyword": { "type": "keyword", "ignore_above": 256 },
              "suggest": { "type": "completion" }
            }
          }
        }
      },
      {
        "nombres_flottants": {
          "match_mapping_type": "double",
          "mapping": { "type": "float" }
        }
      },
      {
        "attributs_dynamiques": {
          "path_match": "attributs.*",
          "mapping": { "type": "keyword" }
        }
      }
    ],
    "properties": {
      "nom": {
        "type": "text",
        "analyzer": "analyseur_fr",
        "fields": {
          "keyword": { "type": "keyword" },
          "autocomplete": {
            "type": "search_as_you_type",
            "max_shingle_size": 3
          }
        }
      },
      "prix": { "type": "scaled_float", "scaling_factor": 100 },
      "en_stock": { "type": "boolean" },
      "date_création": { "type": "date", "format": "strict_date_optional_time" }
    }
  }
}
```

### Nested objects vs flattened

Les objets imbriqués (nested) sont indexés comme des documents séparés — nécessaires pour les requêtes sur des tableaux d'objets :

```json
// PROBLÈME : object standard perd la corrélation entre champs d'un même objet
// { "commentaires": [{"auteur": "Alice", "note": 5}, {"auteur": "Bob", "note": 1}] }
// La requête auteur=Alice ET note=5 retournerait le document même si Alice a donné note=1 !

PUT /articles
{
  "mappings": {
    "properties": {
      "titre": { "type": "text" },
      "commentaires": {
        "type": "nested",
        "properties": {
          "auteur": { "type": "keyword" },
          "note": { "type": "byte" },
          "texte": { "type": "text", "analyzer": "analyseur_fr" },
          "date": { "type": "date" }
        }
      }
    }
  }
}
```

```json
// Requête nested — chercher des articles où Alice a donné une note >= 4
{
  "query": {
    "nested": {
      "path": "commentaires",
      "query": {
        "bool": {
          "must": [
            { "term": { "commentaires.auteur": "alice" } },
            { "range": { "commentaires.note": { "gte": 4 } } }
          ]
        }
      },
      "inner_hits": {
        "size": 3,
        "sort": [{ "commentaires.date": "desc" }]
      }
    }
  }
}
```

**Flattened type** — Alternative pour les attributs dynamiques à haute cardinalité :

```json
// Le type flattened indexe tous les sous-champs comme keywords dans un seul champ
// Évite la "mapping explosion" pour les attributs produits dynamiques (couleur, taille, matière, etc.)
PUT /produits
{
  "mappings": {
    "properties": {
      "attributs": { "type": "flattened" }
    }
  }
}

// Insertion — les attributs peuvent être n'importe quels champs string
{ "attributs": { "couleur": "rouge", "taille": "XL", "matière": "coton", "marque": "Zara" } }

// Requête — fonctionne sur n'importe quel sous-champ
{ "query": { "term": { "attributs.couleur": "rouge" } } }
```

### Keyword normalizers

Les normalizers appliquent des transformations au moment de l'indexation pour les champs keyword :

```json
PUT /produits
{
  "settings": {
    "analysis": {
      "normalizer": {
        "normalizer_lowercase": {
          "type": "custom",
          "filter": ["lowercase", "asciifolding"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "categorie": {
        "type": "keyword",
        "normalizer": "normalizer_lowercase"
        // "Électronique" → indexé comme "electronique"
        // Permet les requêtes case-insensitive et sans accents
      }
    }
  }
}
```

### Join queries (parent-child)

La relation parent-child permet de mettre à jour les documents enfants sans réindexer le parent :

```json
PUT /blog
{
  "mappings": {
    "properties": {
      "relation": {
        "type": "join",
        "relations": { "article": "commentaire" }
      },
      "titre": { "type": "text" },
      "contenu": { "type": "text" },
      "auteur": { "type": "keyword" }
    }
  }
}

// Indexer un article parent
PUT /blog/_doc/1
{ "titre": "Guide Elasticsearch", "relation": { "name": "article" } }

// Indexer un commentaire enfant — routing obligatoire sur l'ID parent
PUT /blog/_doc/2?routing=1
{ "auteur": "alice", "texte": "Excellent article !", "relation": { "name": "commentaire", "parent": "1" } }

// Requête has_child — trouver les articles ayant des commentaires d'Alice
GET /blog/_search
{
  "query": {
    "has_child": {
      "type": "commentaire",
      "query": { "term": { "auteur": "alice" } },
      "score_mode": "avg",  // max, sum, min, none
      "inner_hits": {}
    }
  }
}
```

---

## 2. Agrégations — De Basiques à Avancées

### Terms et Date Histogram

```json
GET /commandes/_search
{
  "size": 0,
  "aggs": {
    "par_statut": {
      "terms": { "field": "statut", "size": 10 },
      "aggs": {
        "montant_total": { "sum": { "field": "montant_ttc" } },
        "montant_moyen": { "avg": { "field": "montant_ttc" } }
      }
    },
    "commandes_par_mois": {
      "date_histogram": {
        "field": "date_commande",
        "calendar_interval": "month",
        "format": "yyyy-MM",
        "min_doc_count": 0,
        "extended_bounds": {
          "min": "2025-01-01",
          "max": "2025-12-31"
        }
      },
      "aggs": {
        "ca_mensuel": { "sum": { "field": "montant_ttc" } }
      }
    }
  }
}
```

### Nested aggregations

Agréger sur des champs nested nécessite l'utilisation de l'agrégation `nested` comme wrapper :

```json
GET /articles/_search
{
  "size": 0,
  "aggs": {
    "commentaires_wrapper": {
      "nested": { "path": "commentaires" },
      "aggs": {
        "note_moyenne": { "avg": { "field": "commentaires.note" } },
        "distribution_notes": {
          "terms": { "field": "commentaires.note", "size": 5 },
          "aggs": {
            "retour_parent": {
              "reverse_nested": {},
              "aggs": {
                "titres": { "terms": { "field": "titre.keyword", "size": 3 } }
              }
            }
          }
        }
      }
    }
  }
}
```

### Pipeline aggregations — Moving average et Derivative

```json
GET /métriques_journalières/_search
{
  "size": 0,
  "aggs": {
    "par_jour": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "day"
      },
      "aggs": {
        "visites": { "sum": { "field": "page_views" } },
        "moyenne_mobile_7j": {
          "moving_avg": {
            "buckets_path": "visites",
            "window": 7,
            "model": "simple"   // ewma, holt, holt_winters, linear, simple
          }
        },
        "croissance": {
          "derivative": { "buckets_path": "visites" }
        }
      }
    },
    "total_visites": { "sum_bucket": { "buckets_path": "par_jour>visites" } },
    "top_jour": { "max_bucket": { "buckets_path": "par_jour>visites" } }
  }
}
```

### Top hits — Récupérer des documents dans les agrégations

```json
GET /produits/_search
{
  "size": 0,
  "aggs": {
    "par_categorie": {
      "terms": { "field": "categorie", "size": 5 },
      "aggs": {
        "top_produits": {
          "top_hits": {
            "size": 3,
            "sort": [{ "note_moyenne": "desc" }],
            "_source": { "includes": ["nom", "prix", "note_moyenne"] }
          }
        },
        "prix_moyen": { "avg": { "field": "prix" } }
      }
    }
  }
}
```

---

## 3. Percolator — Indexer des Requêtes

Le percolator inverse le paradigme classique : plutôt que de stocker des documents et chercher avec des requêtes, on indexe les requêtes et on cherche quel document correspond à quelle requête (idéal pour les alertes, les notifications push, la personnalisation temps réel).

### Configuration et indexation des requêtes

```json
// Créer un index percolator
PUT /alertes_produits
{
  "mappings": {
    "properties": {
      "query": { "type": "percolator" },
      "user_id": { "type": "keyword" },
      "type_alerte": { "type": "keyword" },
      "notification_email": { "type": "keyword" }
    }
  }
}

// Indexer les requêtes (les critères d'alerte des utilisateurs)
PUT /alertes_produits/_doc/alerte_1
{
  "user_id": "user_42",
  "type_alerte": "nouveau_produit",
  "notification_email": "alice@example.com",
  "query": {
    "bool": {
      "must": [
        { "term": { "categorie": "electronique" } },
        { "range": { "prix": { "lte": 500 } } }
      ]
    }
  }
}

PUT /alertes_produits/_doc/alerte_2
{
  "user_id": "user_99",
  "type_alerte": "baisse_prix",
  "query": {
    "bool": {
      "must": [
        { "match": { "nom": "iPhone" } },
        { "range": { "prix": { "lte": 800 } } }
      ]
    }
  }
}
```

### Déclencher le percolator sur un nouveau document

```python
import elasticsearch

es = elasticsearch.Elasticsearch(["http://localhost:9200"])

def déclencher_alertes(nouveau_produit: dict) -> list[dict]:
    """Trouver toutes les alertes correspondant à un nouveau produit."""
    résultat = es.search(
        index="alertes_produits",
        body={
            "query": {
                "percolate": {
                    "field": "query",
                    "document": nouveau_produit  # Le document à tester contre les requêtes indexées
                }
            },
            "_source": ["user_id", "type_alerte", "notification_email"]
        }
    )

    alertes_déclenchées = []
    for hit in résultat["hits"]["hits"]:
        alertes_déclenchées.append({
            "alerte_id": hit["_id"],
            "user_id": hit["_source"]["user_id"],
            "email": hit["_source"].get("notification_email"),
            "type": hit["_source"]["type_alerte"],
        })

    return alertes_déclenchées

# Nouveau produit créé → trouver les utilisateurs à notifier
nouveau_produit = {
    "nom": "Samsung Galaxy S25",
    "categorie": "electronique",
    "prix": 449,
    "en_stock": True
}

alertes = déclencher_alertes(nouveau_produit)
# alertes = [{"user_id": "user_42", "email": "alice@example.com", ...}]
```

---

## 4. Performance — Shard Sizing et Indexation

### Shard sizing — La règle des 50 GB

La règle la plus importante : **garder chaque shard entre 10 et 50 GB** pour des performances optimales. Des shards trop petits (overhead de métadonnées JVM), trop grands (lenteur des merges et des recoveries).

```python
def calculer_shards_primaires(
    volume_données_gb: float,
    taille_shard_cible_gb: float = 30,
    facteur_indexation: float = 1.15,  # Overhead des segments non mergés
) -> int:
    """Calculer le nombre optimal de shards primaires."""
    volume_réel = volume_données_gb * facteur_indexation
    return max(1, round(volume_réel / taille_shard_cible_gb))

# Exemples :
# 100 GB de données → 4 shards primaires (4 × 30 GB ≈ 120 GB avec overhead)
# 1 TB de données → 39 shards primaires
# Index de logs time-series → ILM avec rollover à 30 GB
```

### Force merge et refresh interval

```bash
# Désactiver le refresh pendant l'indexation bulk (améliore le débit de 3-5×)
curl -XPUT "localhost:9200/produits/_settings" -H "Content-Type: application/json" -d '
{
  "index": {
    "refresh_interval": "-1",
    "number_of_replicas": 0
  }
}'

# Réactiver après l'indexation
curl -XPUT "localhost:9200/produits/_settings" -H "Content-Type: application/json" -d '
{
  "index": {
    "refresh_interval": "1s",
    "number_of_replicas": 1
  }
}'

# Force merge sur un index en lecture seule (logs anciens, archives)
# Réduit le nombre de segments, améliore les performances de lecture
curl -XPOST "localhost:9200/logs-2025-01/_forcemerge?max_num_segments=1"
```

### Bulk indexing optimisé

```python
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk, parallel_bulk
import json

es = Elasticsearch(
    ["http://localhost:9200"],
    http_compress=True,    # Compression gzip des requêtes
    request_timeout=30,
    max_retries=3,
    retry_on_timeout=True,
)

def générer_actions(documents: list[dict], index_name: str):
    """Générateur d'actions bulk pour les grands volumes."""
    for doc in documents:
        yield {
            "_index": index_name,
            "_id": doc.get("id"),
            "_source": doc,
        }

def indexer_bulk(documents: list[dict], index_name: str, batch_size: int = 1000):
    """Indexation bulk avec parallel_bulk pour maximiser le débit."""
    succès, erreurs = 0, 0

    for ok, info in parallel_bulk(
        es,
        générer_actions(documents, index_name),
        chunk_size=batch_size,
        thread_count=4,        # Parallélisme côté client
        queue_size=8,          # File d'attente de batches en mémoire
        raise_on_error=False,
    ):
        if ok:
            succès += 1
        else:
            erreurs += 1
            print(f"Erreur indexation : {info}")

    return {"succès": succès, "erreurs": erreurs}
```

**Paramètres bulk recommandés** :
- Taille du batch : 5-15 MB par requête bulk (pas en nombre de documents).
- `queue_size = thread_count * 2` pour maximiser l'utilisation des threads.
- Désactiver `refresh_interval` pendant l'indexation initiale.
- `number_of_replicas = 0` pendant l'indexation initiale, réactiver après.
- Utiliser `_id` explicite pour éviter les collisions en cas de retry.

### Circuit breakers

```bash
# Vérifier l'état des circuit breakers
GET /_nodes/stats/breaker

# Configurer le field data circuit breaker (évite les OOM sur les agrégations)
PUT /_cluster/settings
{
  "persistent": {
    "indices.breaker.fielddata.limit": "40%",    # Défaut : 40% heap
    "indices.breaker.request.limit": "60%",      # Défaut : 60% heap
    "indices.breaker.total.limit": "95%"         # Défaut : 95% heap
  }
}

# Si circuit breaker déclenché sur fielddata → vider le cache
POST /_cache/clear?fielddata=true
```

---

## 5. Relevance Tuning — Function Score et Learning to Rank

### function_score — Boost par popularité et fraîcheur

```json
GET /articles/_search
{
  "query": {
    "function_score": {
      "query": {
        "multi_match": {
          "query": "elasticsearch performance",
          "fields": ["titre^3", "contenu"]
        }
      },
      "functions": [
        {
          "filter": { "range": { "date_publication": { "gte": "now-30d" } } },
          "weight": 1.5
        },
        {
          "field_value_factor": {
            "field": "vues_totales",
            "factor": 0.1,
            "modifier": "log1p",  // log(1 + vues) — évite les valeurs extrêmes
            "missing": 1
          }
        },
        {
          "gauss": {
            "date_publication": {
              "origin": "now",
              "scale": "30d",
              "decay": 0.5     // À 30 jours, le score decay vaut 0.5
            }
          }
        }
      ],
      "score_mode": "sum",      // sum, avg, max, min, multiply, first
      "boost_mode": "multiply"  // Multiplie le score BM25 par la function score
    }
  }
}
```

### script_score — Logique de scoring personnalisée

```json
GET /produits/_search
{
  "query": {
    "script_score": {
      "query": {
        "bool": {
          "must": [{ "match": { "nom": "smartphone" } }],
          "filter": [{ "term": { "en_stock": true } }]
        }
      },
      "script": {
        "source": """
          double score = _score;
          double popularité = doc['ventes_30j'].value * 0.001;
          double fraîcheur = Math.max(0, (params.now - doc['date_mise_à_jour'].value.millis) / 86400000.0);
          double fraîcheur_score = Math.exp(-0.05 * fraîcheur);
          double note = doc['note_moyenne'].value;
          return score * (1 + popularité) * fraîcheur_score * (note / 5.0);
        """,
        "params": { "now": 1735689600000 }
      }
    }
  }
}
```

### Learning to Rank (LTR Plugin)

Le plugin LTR d'Elasticsearch (Elasticsearch Learning to Rank) permet d'entraîner un modèle de ranking supervisé à partir de données de clics et de jugements de pertinence :

```python
# Étape 1 : Définir les features (signaux de ranking)
feature_set = {
    "featureset": {
        "name": "ecommerce_features",
        "features": [
            {
                "name": "score_bm25",
                "params": ["keywords"],
                "template": {
                    "match": { "nom": "{{keywords}}" }
                }
            },
            {
                "name": "ventes_30j",
                "params": [],
                "template": {
                    "function_score": {
                        "field_value_factor": { "field": "ventes_30j", "missing": 0 }
                    }
                }
            },
            {
                "name": "note_moyenne",
                "params": [],
                "template": {
                    "function_score": {
                        "field_value_factor": { "field": "note_moyenne", "missing": 3 }
                    }
                }
            }
        ]
    }
}

# Étape 2 : Collecter des jugements de pertinence (grade = 4 = très pertinent)
jugements = [
    {"query_id": 1, "doc_id": "prod_123", "grade": 4},  # Très pertinent
    {"query_id": 1, "doc_id": "prod_456", "grade": 2},  # Pertinent
    {"query_id": 1, "doc_id": "prod_789", "grade": 0},  # Non pertinent
]

# Étape 3 : Entraîner le modèle (LambdaMART via RankLib)
# Le modèle apprend à pondérer les features pour maximiser le NDCG
# Étape 4 : Déployer le modèle dans l'index
# Étape 5 : Utiliser le modèle en production via sltr query
```

---

## 6. Alias et Zero-Downtime Reindexing

### Stratégie d'alias pour les migrations

```python
def réindexer_sans_downtime(
    es: Elasticsearch,
    alias: str,
    ancien_index: str,
    nouveau_mapping: dict
) -> str:
    """Réindexer avec zéro temps d'arrêt via les alias ES."""
    import time

    # 1. Créer le nouvel index avec le nouveau mapping
    nouveau_index = f"{alias}_{int(time.time())}"
    es.indices.create(index=nouveau_index, body=nouveau_mapping)

    # 2. Copier les données avec l'API _reindex (asynchrone pour les grands volumes)
    tâche = es.reindex(
        body={
            "source": {"index": ancien_index, "size": 1000},
            "dest": {"index": nouveau_index},
        },
        wait_for_completion=False,
        requests_per_second=500,  # Throttle pour ne pas saturer le cluster
    )
    task_id = tâche["task"]

    # 3. Attendre la fin du reindex
    while True:
        statut = es.tasks.get(task_id=task_id)
        if statut["completed"]:
            break
        time.sleep(5)

    # 4. Basculer l'alias atomiquement (zéro downtime)
    es.indices.update_aliases(
        body={
            "actions": [
                {"remove": {"index": ancien_index, "alias": alias}},
                {"add": {"index": nouveau_index, "alias": alias}},
            ]
        }
    )

    return nouveau_index

# L'alias "produits" pointe toujours vers l'index actif
# Les applications utilisent l'alias, jamais le nom d'index direct
```

### Index Lifecycle Management (ILM)

```json
// Politique ILM pour les indices de logs time-series
PUT /_ilm/policy/politique_logs
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_primary_shard_size": "30gb",
            "max_age": "1d"
          },
          "set_priority": { "priority": 100 }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": { "number_of_shards": 1 },
          "forcemerge": { "max_num_segments": 1 },
          "set_priority": { "priority": 50 }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "searchable_snapshot": { "snapshot_repository": "snapshots_s3" },
          "set_priority": { "priority": 0 }
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": { "delete": {} }
      }
    }
  }
}
```

---

## 7. Cross-cluster Search

```yaml
# elasticsearch.yml — configurer les clusters distants
cluster.remote:
  cluster_prod:
    seeds: ["prod-es-01:9300", "prod-es-02:9300"]
    transport.ping_schedule: "30s"
  cluster_archive:
    seeds: ["archive-es-01:9300"]
    skip_unavailable: true  # Ne pas échouer si le cluster est indisponible
```

```python
# Requête cross-cluster — syntaxe : cluster:index
résultats = es.search(
    index="cluster_prod:produits,cluster_archive:produits_archive",
    body={
        "query": { "match": { "nom": "smartphone" } },
        "_clusters": {  # Stats par cluster dans la réponse
            "details": True
        }
    }
)
```

---

## 8. OpenSearch — Différences Clés avec Elasticsearch

OpenSearch est le fork open-source d'Elasticsearch (version 7.10, 2021) maintenu par Amazon. Les différences en production :

| Aspect | Elasticsearch | OpenSearch |
|---|---|---|
| **Licence** | SSPL (propriétaire depuis 7.11) | Apache 2.0 (open-source) |
| **k-NN plugin** | Dense vector via `dense_vector` | Plugin k-NN dédié avec HNSW, NMSLIB, FAISS |
| **Neural search** | Limité | Plugin neural search natif (pipeline d'embedding intégré) |
| **Sécurité** | Payant (X-Pack) | Gratuit (OpenSearch Security) |
| **Alerting** | Payant (Watcher) | Gratuit (OpenSearch Alerting) |
| **API** | Standard | Compatible ES 7.x avec extensions |

```json
// OpenSearch — k-NN index avec moteur HNSW
PUT /documents_opensearch
{
  "settings": {
    "index": {
      "knn": true,
      "knn.algo_param.ef_search": 100
    }
  },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 1536,
        "method": {
          "name": "hnsw",
          "engine": "nmslib",
          "space_type": "cosinesimil",
          "parameters": { "m": 16, "ef_construction": 128 }
        }
      }
    }
  }
}

// OpenSearch Neural Search — pipeline d'embedding intégré
PUT /_ingest/pipeline/pipeline_neural
{
  "description": "Pipeline avec embedding automatique",
  "processors": [{
    "text_embedding": {
      "model_id": "<model_id_déployé>",
      "field_map": { "contenu": "contenu_embedding" }
    }
  }]
}
```

---

## 9. Snapshot / Restore — Migrations et Backups

### Configuration du repository

```bash
# Repository S3 (AWS ou compatible MinIO)
PUT /_snapshot/backup_s3
{
  "type": "s3",
  "settings": {
    "bucket": "mon-bucket-es-backups",
    "region": "eu-west-1",
    "base_path": "elasticsearch/",
    "compress": true,
    "chunk_size": "1gb",
    "max_restore_bytes_per_sec": "500mb",
    "max_snapshot_bytes_per_sec": "200mb"
  }
}
```

```python
def créer_snapshot(es: Elasticsearch, repository: str, snapshot_name: str, indices: list[str]):
    """Créer un snapshot et attendre sa complétion."""
    es.snapshot.create(
        repository=repository,
        snapshot=snapshot_name,
        body={
            "indices": ",".join(indices),
            "ignore_unavailable": True,
            "include_global_state": False,
            "metadata": { "créé_par": "backup_automatique", "version": "1.0" }
        },
        wait_for_completion=True,
    )

def restaurer_snapshot(es: Elasticsearch, repository: str, snapshot_name: str, index_source: str, index_dest: str):
    """Restaurer un index avec renommage."""
    es.snapshot.restore(
        repository=repository,
        snapshot=snapshot_name,
        body={
            "indices": index_source,
            "rename_pattern": index_source,
            "rename_replacement": index_dest,
            "index_settings": {
                "index.number_of_replicas": 0  # Restaurer sans réplicas d'abord
            }
        },
        wait_for_completion=True,
    )
```

---

## 10. Monitoring Opérationnel

### APIs de monitoring essentielles

```bash
# Santé du cluster (green / yellow / red)
GET /_cluster/health?level=indices&wait_for_status=green&timeout=30s

# Statistiques des nœuds — RAM, CPU, I/O, JVM
GET /_nodes/stats?filter_path=nodes.*.jvm,nodes.*.os,nodes.*.breakers

# Statistiques des indices
GET /produits/_stats?filter_path=indices.produits.total

# Segments en cours de merge (indicateur de pression d'indexation)
GET /_cat/segments/produits?v=true&s=size:desc

# Requêtes lentes — vérifier le slow log
GET /produits/_settings?filter_path=*.settings.index.search.slowlog

# Tâches en cours (reindex, forcemerge, etc.)
GET /_tasks?detailed=true&actions=indices:data/write/reindex

# Allocation des shards — diagnostiquer les shards non assignés
GET /_cluster/allocation/explain
```

### Métriques à monitorer en production

| Métrique | Seuil d'alerte | Action |
|---|---|---|
| **cluster_status** | yellow > 1h, red immédiat | Vérifier les shards non assignés |
| **jvm.heap_used_percent** | > 75% | Augmenter le heap ou les nœuds |
| **os.cpu.percent** | > 80% (soutenu) | Optimiser les requêtes ou scaler |
| **indices.search.query_time_in_millis** | P99 > 1000ms | Profiler et optimiser les requêtes lentes |
| **indices.indexing.index_failed** | > 0 | Vérifier les erreurs de mapping |
| **breakers.*.tripped** | > 0 | Réduire la charge sur les agrégations |
| **segments.count** | > 300 par shard | Déclencher un forcemerge |

```python
from elasticsearch import Elasticsearch

def vérifier_santé_cluster(es: Elasticsearch) -> dict:
    santé = es.cluster.health()
    stats = es.nodes.stats(metric=["jvm", "os", "breakers"])

    alertes = []
    if santé["status"] == "red":
        alertes.append("CRITIQUE : Cluster RED — des shards primaires sont manquants")
    elif santé["status"] == "yellow":
        alertes.append("AVERTISSEMENT : Cluster YELLOW — des shards réplicas sont manquants")

    for nœud_id, nœud in stats["nodes"].items():
        heap_pct = nœud["jvm"]["mem"]["heap_used_percent"]
        if heap_pct > 75:
            alertes.append(f"AVERTISSEMENT : Nœud {nœud_id} — heap JVM à {heap_pct}%")

    return {"statut": santé["status"], "alertes": alertes}
```
