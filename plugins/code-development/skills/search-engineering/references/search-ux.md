# Search UX — Algolia Avancé, Autocomplete et Analytics de Recherche

## Overview

Ce document de référence couvre la search UX en production : configuration avancée Algolia (query rules, merchandising, A/B testing, personnalisation), Typesense et sa comparaison avec Algolia, autocomplete optimisé avec debounce et états de chargement, search-as-you-type, query understanding (correction orthographique, synonymes, classification), gestion des zéro résultats, analytics de recherche, A/B testing de ranking, et accessibilité ARIA. Utiliser ce guide pour construire des expériences de recherche remarquables.

---

## 1. Algolia — Configuration Avancée

### Query rules — Logique métier sur les résultats

Les query rules permettent d'injecter de la logique métier dans le ranking sans modifier le code applicatif :

```javascript
const { AlgoliaSearchHelper } = require("algoliasearch-helper");
const algoliasearch = require("algoliasearch");

const client = algoliasearch(
  process.env.ALGOLIA_APP_ID,
  process.env.ALGOLIA_ADMIN_KEY
);
const index = client.initIndex("produits");

// Query rule 1 : booster les promotions sur la requête "soldes"
await index.saveRule({
  objectID: "boost_soldes",
  conditions: [
    {
      pattern: "soldes",
      anchoring: "contains",
    },
  ],
  consequence: {
    promote: [
      { objectID: "promo_été_2025", position: 1 },
      { objectID: "promo_hiver_2025", position: 2 },
    ],
    filterPromotes: true,
  },
  description: "Mettre en avant les promotions en cours lors des recherches 'soldes'",
  enabled: true,
});

// Query rule 2 : rediriger vers une page catégorie (sans résultats de recherche)
await index.saveRule({
  objectID: "redirect_iphone",
  conditions: [
    {
      pattern: "iphone",
      anchoring: "is",
    },
  ],
  consequence: {
    redirect: {
      url: "https://exemple.com/marques/apple/iphone",
    },
  },
  description: "Rediriger vers la page Apple iPhone",
});

// Query rule 3 : ajouter un filtre automatique selon le contexte
await index.saveRule({
  objectID: "filtre_contexte_mobile",
  conditions: [
    {
      context: "mobile_app",  // Contexte envoyé depuis l'app mobile
    },
  ],
  consequence: {
    params: {
      filters: "disponible_livraison_rapide:true",
    },
  },
});
```

### Merchandising — Pinning et hiding de produits

```javascript
// Fixer des produits en tête de résultats (ex: meilleures ventes)
await index.saveRule({
  objectID: "merchandising_homepage",
  conditions: [{ pattern: "", anchoring: "is" }],  // Toutes les requêtes vides
  consequence: {
    promote: [
      { objectID: "bestseller_001", position: 1 },
      { objectID: "nouveauté_002", position: 2 },
      { objectID: "exclusivité_003", position: 3 },
    ],
  },
});

// Masquer un produit en rupture de stock des résultats de recherche
await index.saveRule({
  objectID: "hide_rupture_stock",
  conditions: [{ pattern: "", anchoring: "is" }],
  consequence: {
    hide: [{ objectID: "produit_rupture_123" }],
  },
});
```

### A/B Testing Algolia

```javascript
// Créer un A/B test sur deux stratégies de ranking
const { data: abTest } = await client.addABTest({
  name: "Test ranking popularité vs fraîcheur",
  variants: [
    {
      index: "produits",          // Variante A : index de production
      trafficPercentage: 50,
      description: "Ranking actuel — ventes 30 jours"
    },
    {
      index: "produits_fraicheur", // Variante B : index avec boost fraîcheur
      trafficPercentage: 50,
      description: "Ranking avec boost date de mise en ligne"
    },
  ],
  endAt: "2025-04-01T00:00:00.000Z",
});

console.log(`A/B test créé : ID ${abTest.abTestID}`);

// Consulter les résultats
const { data: résultats } = await client.getABTest({ id: abTest.abTestID });
console.log(`Variante A — CTR : ${résultats.variants[0].clickThroughRate}`);
console.log(`Variante B — CTR : ${résultats.variants[1].clickThroughRate}`);
console.log(`Significativité statistique : ${résultats.variants[1].abTestID}`);
```

### Personnalisation — User Tokens et Profils

```javascript
// Envoyer des événements de comportement utilisateur pour la personnalisation
const insightsClient = require("search-insights");

insightsClient("init", {
  appId: process.env.ALGOLIA_APP_ID,
  apiKey: process.env.ALGOLIA_SEARCH_KEY,
  userToken: "user_abc123",  // Identifiant utilisateur (anonyme ou authentifié)
});

// Événement de clic sur un résultat
insightsClient("clickedObjectIDsAfterSearch", {
  eventName: "Produit cliqué",
  index: "produits",
  queryID: queryID,         // Obtenu depuis la réponse de recherche
  objectIDs: ["prod_456"],
  positions: [3],
});

// Événement de conversion (achat)
insightsClient("convertedObjectIDsAfterSearch", {
  eventName: "Produit acheté",
  index: "produits",
  queryID: queryID,
  objectIDs: ["prod_456"],
});

// Requête avec personnalisation activée
const résultats = await index.search("chaussures", {
  userToken: "user_abc123",
  enablePersonalization: true,
  personalizationImpact: 50,  // 0-100 : impact de la personnalisation sur le ranking
});
```

### Algolia Recommend

```javascript
const recommendClient = require("@algolia/recommend");
const client_recommend = recommendClient(
  process.env.ALGOLIA_APP_ID,
  process.env.ALGOLIA_SEARCH_KEY
);

// "Frequently bought together" — produits souvent achetés ensemble
const { results } = await client_recommend.getFrequentlyBoughtTogether({
  requests: [
    {
      indexName: "produits",
      objectID: "prod_123",
      maxRecommendations: 5,
    },
  ],
});

// "Related products" — produits similaires
const { results: similaires } = await client_recommend.getRelatedProducts({
  requests: [
    {
      indexName: "produits",
      objectID: "prod_123",
      maxRecommendations: 8,
      threshold: 20,
    },
  ],
});
```

---

## 2. Typesense — Configuration et Comparaison avec Algolia

### Configuration d'un schéma Typesense

Typesense est open-source, auto-hébergeable et propose une API très proche d'Algolia :

```typescript
import Typesense from "typesense";

const client = new Typesense.Client({
  nodes: [{ host: "localhost", port: 8108, protocol: "http" }],
  apiKey: process.env.TYPESENSE_ADMIN_KEY!,
  connectionTimeoutSeconds: 2,
});

// Schéma strict avec types explicites
await client.collections().create({
  name: "produits",
  fields: [
    { name: "nom", type: "string" },
    { name: "description", type: "string" },
    { name: "prix", type: "float" },
    { name: "categorie", type: "string", facet: true },
    { name: "marque", type: "string", facet: true },
    { name: "note_moyenne", type: "float" },
    { name: "ventes_30j", type: "int32" },
    { name: "en_stock", type: "bool", facet: true },
    { name: "date_création", type: "int64" },  // Unix timestamp
  ],
  default_sorting_field: "ventes_30j",
  enable_nested_fields: true,
});

// Synonymes bidirectionnels
await client.collections("produits").synonyms().upsert("syn_téléphone", {
  synonyms: ["téléphone", "smartphone", "mobile", "portable"],
});

// Synonyme unidirectionnel : "TV" → "télévision, téléviseur"
await client.collections("produits").synonyms().upsert("syn_tv", {
  root: "TV",
  synonyms: ["télévision", "téléviseur"],
});

// Curation — fixer des résultats pour une requête
await client.collections("produits").overrides().upsert("override_iphone", {
  rule: { query: "iphone", match: "exact" },
  includes: [{ id: "apple_iphone_15", position: 1 }],
  excludes: [{ id: "étui_iphone_knockoff" }],
});
```

### Recherche avec filtres et facettes

```typescript
const résultats = await client.collections("produits").documents().search({
  q: "chaussures running",
  query_by: "nom,description",
  query_by_weights: "3,1",              // Pondération des champs
  filter_by: "prix:[50..300] && en_stock:true && categorie:Sport",
  facet_by: "marque,categorie",
  sort_by: "note_moyenne:desc,ventes_30j:desc",
  per_page: 20,
  page: 1,
  typo_tokens_threshold: 1,            // Activer la correction orthographique dès 1 token
  num_typos: 2,                         // Maximum 2 fautes par mot
  highlight_full_fields: "nom",
  snippet_threshold: 100,
});
```

### Comparaison Algolia vs Typesense

| Critère | Algolia | Typesense |
|---|---|---|
| **Hébergement** | SaaS uniquement | Self-hosted ou Typesense Cloud |
| **Licence** | Propriétaire | Apache 2.0 (open-source) |
| **Prix** | Élevé ($1/1000 opérations) | Gratuit self-hosted, ~$0.10/1M opérations cloud |
| **Typo tolerance** | Excellente, configurée automatiquement | Excellente, paramétrable finement |
| **Personnalisation** | Avancée (User Tokens, A/B natif) | Basique (manual ranking rules) |
| **Recherche vectorielle** | Intégrée (Algolia NeuralSearch) | Non native (plugin externe) |
| **A/B testing** | Natif avec stats intégrées | Manuel (via feature flags externes) |
| **Merchandising** | Dashboard UI dédié | API uniquement |
| **Latence** | < 5ms (P99) | < 5ms (P99) sur instances dédiées |
| **Conformité RGPD** | Stockage EU possible | Self-hosted = contrôle total |
| **Idéal pour** | E-commerce, équipes non-techniques, merchandising | Startups, conformité données, budget contraint |

---

## 3. Autocomplete — Implémentation Optimisée

### Debounce et annulation des requêtes précédentes

```typescript
import { useState, useEffect, useRef, useCallback } from "react";

interface SuggestionItem {
  query: string;
  type: "recent" | "popular" | "result";
  objectID?: string;
}

function useAutocomplete(indexName: string, minChars: number = 2) {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState<SuggestionItem[]>([]);
  const [loading, setLoading] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);
  const debounceRef = useRef<NodeJS.Timeout>();

  const rechercher = useCallback(async (valeur: string) => {
    if (valeur.length < minChars) {
      // Afficher les recherches récentes quand la requête est courte
      const récentes = getRecentSearches();
      setSuggestions(récentes.map(q => ({ query: q, type: "recent" })));
      return;
    }

    // Annuler la requête précédente si toujours en cours
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    abortControllerRef.current = new AbortController();
    setLoading(true);

    try {
      const résultats = await index.search(valeur, {
        hitsPerPage: 5,
        attributesToRetrieve: ["objectID", "nom"],
        attributesToHighlight: ["nom"],
        signal: abortControllerRef.current.signal,
      });

      setSuggestions(
        résultats.hits.map(hit => ({
          query: hit.nom as string,
          objectID: hit.objectID,
          type: "result",
        }))
      );
    } catch (err) {
      if ((err as Error).name !== "AbortError") {
        console.error("Erreur autocomplete :", err);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => rechercher(query), 200);  // 200ms debounce
    return () => clearTimeout(debounceRef.current);
  }, [query, rechercher]);

  return { query, setQuery, suggestions, loading };
}
```

### Recherches récentes et requêtes populaires

```typescript
// Gérer l'historique de recherche en localStorage
const CLEF_RÉCENTES = "search_recent";
const MAX_RÉCENTES = 8;

function getRecentSearches(): string[] {
  try {
    return JSON.parse(localStorage.getItem(CLEF_RÉCENTES) || "[]");
  } catch {
    return [];
  }
}

function saveRecentSearch(query: string): void {
  const récentes = getRecentSearches().filter(q => q !== query);
  const mises_à_jour = [query, ...récentes].slice(0, MAX_RÉCENTES);
  localStorage.setItem(CLEF_RÉCENTES, JSON.stringify(mises_à_jour));
}

function removeRecentSearch(query: string): void {
  const filtrées = getRecentSearches().filter(q => q !== query);
  localStorage.setItem(CLEF_RÉCENTES, JSON.stringify(filtrées));
}

// Composant autocomplete avec sections
function Autocomplete({ onSelect }: { onSelect: (q: string) => void }) {
  const { query, setQuery, suggestions, loading } = useAutocomplete("produits");
  const popularQueries = ["smartphone", "ordinateur portable", "casque audio"];

  const sections: { titre: string; items: SuggestionItem[] }[] = [];

  if (query.length < 2) {
    sections.push(
      { titre: "Recherches récentes", items: getRecentSearches().map(q => ({ query: q, type: "recent" })) },
      { titre: "Tendances", items: popularQueries.map(q => ({ query: q, type: "popular" })) }
    );
  } else {
    sections.push({ titre: "Suggestions", items: suggestions });
  }

  return (
    <div role="combobox" aria-expanded={sections.some(s => s.items.length > 0)}>
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Rechercher..."
        aria-autocomplete="list"
        aria-haspopup="listbox"
      />
      {loading && <span aria-live="polite">Chargement...</span>}
      {/* Rendu des sections */}
    </div>
  );
}
```

---

## 4. Search-as-you-type — Implémentation Optimisée

### Elasticsearch search_as_you_type

```typescript
// Utiliser le type search_as_you_type d'Elasticsearch
// Configure automatiquement des analyzers edge_ngram pour les complétions

async function rechercherAsYouType(
  es: Client,
  query: string
): Promise<SearchHit[]> {
  if (query.length < 2) return [];

  const { hits } = await es.search({
    index: "produits",
    body: {
      query: {
        multi_match: {
          query,
          type: "bool_prefix",         // Optimisé pour search-as-you-type
          fields: [
            "nom",
            "nom._2gram",
            "nom._3gram",
            "nom._index_prefix",       // Champ généré automatiquement
          ],
        },
      },
      highlight: {
        fields: { nom: { type: "unified" } },
        pre_tags: ["<strong>"],
        post_tags: ["</strong>"],
      },
      _source: ["nom", "prix", "categorie", "url_image"],
      size: 8,
    },
  });

  return hits.hits;
}
```

### React avec états de chargement et annulation

```tsx
import { useRef, useState, useTransition } from "react";

function SearchAsYouType() {
  const [résultats, setRésultats] = useState<Produit[]>([]);
  const [isPending, startTransition] = useTransition();  // React 18 : non-bloquant
  const abortRef = useRef<AbortController>();

  const handleInput = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const valeur = e.target.value;

    // Annuler la requête précédente
    abortRef.current?.abort();
    abortRef.current = new AbortController();

    if (valeur.length < 2) {
      setRésultats([]);
      return;
    }

    startTransition(async () => {
      try {
        const data = await fetch(
          `/api/search?q=${encodeURIComponent(valeur)}`,
          { signal: abortRef.current!.signal }
        ).then(r => r.json());

        setRésultats(data.hits);
      } catch (err) {
        if ((err as Error).name !== "AbortError") {
          setRésultats([]);
        }
      }
    });
  };

  return (
    <div>
      <input
        type="search"
        onChange={handleInput}
        aria-busy={isPending}
        placeholder="Rechercher un produit..."
      />
      {isPending && <div className="spinner" aria-label="Recherche en cours" />}
      <ul role="listbox">
        {résultats.map(p => (
          <li key={p.id} role="option">
            <img src={p.url_image} alt={p.nom} width={40} />
            <span dangerouslySetInnerHTML={{ __html: p.nom_highlighted }} />
            <span>{p.prix}€</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 5. Query Understanding — NLP pour la Recherche

### Correction orthographique avec seuils

```typescript
// Stratégie de tolérance aux fautes progressive
function configurerTolérance(longueurMot: number): "none" | "1" | "2" {
  if (longueurMot <= 3) return "none";   // "TV" → pas de correction
  if (longueurMot <= 6) return "1";      // "iPhon" → corriger 1 faute
  return "2";                             // "smarthpone" → corriger 2 fautes
}

// Algolia — configurer la tolérance par longueur de mot
await index.setSettings({
  typoTolerance: "min",         // min, true, false (min = au moins 1 résultat correct avant les résultats avec fautes)
  minWordSizefor1Typo: 4,       // Mots de 4+ caractères : 1 faute tolérée
  minWordSizefor2Typos: 8,      // Mots de 8+ caractères : 2 fautes tolérées
  disableTypoToleranceOnAttributes: ["référence_produit", "ean", "sku"],
  disableTypoToleranceOnWords: ["iPhone", "Samsung", "PlayStation"],
});
```

### Synonymes — One-way vs Two-way

```typescript
// Synonymes bidirectionnels (équivalents complets)
await index.saveSynonym("syn_bidir_téléphone", {
  type: "synonym",
  objectID: "syn_bidir_téléphone",
  synonyms: ["téléphone", "smartphone", "mobile"],
});

// Synonymes unidirectionnels (expansion d'une requête vers des termes plus larges)
// "PS5" → trouvera aussi "PlayStation 5" et "console Sony"
// Mais "PlayStation 5" NE trouvera PAS "PS5"
await index.saveSynonym("syn_unidir_ps5", {
  type: "oneWaySynonym",
  objectID: "syn_unidir_ps5",
  input: "ps5",
  synonyms: ["playstation 5", "console sony"],
});

// Substitution avec placeholder (Algolia Placeholder)
// Capturer l'intention "moins de X euros"
await index.saveSynonym("syn_placeholder_prix", {
  type: "altCorrection2",
  objectID: "syn_placeholder_prix",
  word: "pas cher",
  corrections: ["économique", "budget"],
});
```

### Classification de l'intention de requête

```typescript
// Classifier les requêtes pour adapter la stratégie de recherche
async function classifierRequête(query: string): Promise<{
  type: "navigationnelle" | "informationnelle" | "transactionnelle";
  filtres_suggérés?: Record<string, string>;
}> {
  const patterns = {
    navigationnelle: /^(marque|catégorie|page|site)\s/i,
    transactionnelle: /(acheter|commander|prix|promotion|solde|livraison)/i,
    informationnelle: /(comment|qu'est|différence|guide|avis|test|comparatif)/i,
  };

  if (patterns.navigationnelle.test(query)) return { type: "navigationnelle" };
  if (patterns.transactionnelle.test(query)) return {
    type: "transactionnelle",
    filtres_suggérés: { en_stock: "true" },
  };
  if (patterns.informationnelle.test(query)) return { type: "informationnelle" };

  return { type: "transactionnelle" };  // Défaut : intention commerciale
}
```

---

## 6. Gestion des Zéro Résultats

### Stratégies de fallback

```typescript
async function rechercherAvecFallback(
  query: string,
  filtres: Record<string, string>
): Promise<{ résultats: Produit[]; stratégie: string }> {
  // Tentative 1 : recherche complète avec tous les filtres
  let résultats = await index.search(query, { filters: buildFilters(filtres) });
  if (résultats.nbHits > 0) return { résultats: résultats.hits, stratégie: "exact" };

  // Tentative 2 : relâcher les filtres non essentiels (conserver seulement la catégorie)
  const filtres_réduits = { categorie: filtres.categorie };
  résultats = await index.search(query, { filters: buildFilters(filtres_réduits) });
  if (résultats.nbHits > 0) return { résultats: résultats.hits, stratégie: "filtres_réduits" };

  // Tentative 3 : recherche sans filtres
  résultats = await index.search(query);
  if (résultats.nbHits > 0) return { résultats: résultats.hits, stratégie: "sans_filtres" };

  // Tentative 4 : recherche élargie (supprimer les stopwords, utiliser les mots principaux)
  const mots_clés = extraireMots(query);
  résultats = await index.search(mots_clés.join(" "), { queryType: "prefixAll" });
  if (résultats.nbHits > 0) return { résultats: résultats.hits, stratégie: "mots_clés" };

  // Tentative 5 : suggestions alternatives ("Vouliez-vous dire ?")
  const corrections = résultats.queryAfterRemoval || query;
  return { résultats: [], stratégie: "zéro_résultats" };
}

// Composant UI pour les zéro résultats
function ZéroRésultats({ query, corrections }: Props) {
  return (
    <div role="status" aria-live="polite">
      <h2>Aucun résultat pour « {query} »</h2>
      {corrections && (
        <p>
          Vouliez-vous dire{" "}
          <button onClick={() => onSearch(corrections)}>
            <strong>{corrections}</strong>
          </button>{" "}
          ?
        </p>
      )}
      <ul>
        <li>Vérifiez l'orthographe</li>
        <li>Essayez des termes plus généraux</li>
        <li>Réduisez le nombre de filtres actifs</li>
      </ul>
    </div>
  );
}
```

---

## 7. Analytics de Recherche

### Métriques essentielles à collecter

```typescript
interface ÉvénementRecherche {
  query: string;
  timestamp: number;
  user_id?: string;
  session_id: string;
  nb_résultats: number;
  position_clic?: number;     // Position du résultat cliqué (1-indexed)
  objectID_cliqué?: string;
  temps_ms: number;           // Temps de réponse
  filtres_actifs: string[];
  page: number;
}

// Tracker les événements côté client
class SearchAnalytics {
  private sessionId = crypto.randomUUID();

  async trackSearch(params: ÉvénementRecherche): Promise<void> {
    await fetch("/api/analytics/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params),
    });
  }

  trackClic(
    queryID: string,
    objectID: string,
    position: number
  ): void {
    // Algolia Insights
    insightsClient("clickedObjectIDsAfterSearch", {
      eventName: "Résultat cliqué",
      index: "produits",
      queryID,
      objectIDs: [objectID],
      positions: [position],
      userToken: this.sessionId,
    });
  }
}
```

### Dashboard analytics — Requêtes SQL

```sql
-- Top 20 requêtes par volume (7 derniers jours)
SELECT
  query,
  COUNT(*) AS nb_recherches,
  AVG(nb_résultats) AS moy_résultats,
  AVG(CASE WHEN position_clic IS NOT NULL THEN 1.0 ELSE 0.0 END) AS ctr,
  SUM(CASE WHEN nb_résultats = 0 THEN 1 ELSE 0 END) AS nb_zéro_résultats
FROM événements_recherche
WHERE timestamp >= NOW() - INTERVAL '7 days'
GROUP BY query
ORDER BY nb_recherches DESC
LIMIT 20;

-- Requêtes avec 0 résultats (opportunités d'amélioration)
SELECT
  query,
  COUNT(*) AS nb_occurrences,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_du_total
FROM événements_recherche
WHERE timestamp >= NOW() - INTERVAL '7 days'
  AND nb_résultats = 0
GROUP BY query
ORDER BY nb_occurrences DESC
LIMIT 50;

-- Taux de clic par position (pour évaluer la qualité du ranking)
SELECT
  position_clic,
  COUNT(*) AS nb_clics,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_clics
FROM événements_recherche
WHERE timestamp >= NOW() - INTERVAL '30 days'
  AND position_clic IS NOT NULL
GROUP BY position_clic
ORDER BY position_clic;
```

### KPIs de recherche à suivre en production

| Métrique | Définition | Cible | Action si hors cible |
|---|---|---|---|
| **Taux zéro résultats** | % de recherches avec 0 résultat | < 5% | Ajouter synonymes, élargir les fallbacks |
| **CTR moyen** | % de recherches suivies d'un clic | > 40% | Améliorer le ranking, les descriptions |
| **Position moyenne du clic** | Rang moyen du résultat cliqué | < 3 | Retravailler la pertinence et les boosts |
| **Taux d'abandon** | % de recherches sans action suivante | < 30% | Améliorer les suggestions, les facettes |
| **Taux de conversion post-search** | % de sessions de recherche avec achat | Secteur-dépendant | A/B test du ranking, merchandising |
| **Latence P95** | Temps de réponse au 95e percentile | < 200ms | Optimiser les requêtes, le caching |

---

## 8. A/B Testing du Ranking

### Protocole statistique rigoureux

Ne lancer un A/B test de ranking qu'avec une méthodologie statistique solide pour éviter les faux positifs :

```python
from scipy import stats
import numpy as np

def calculer_signification_statistique(
    conversions_A: int,
    visiteurs_A: int,
    conversions_B: int,
    visiteurs_B: int,
    alpha: float = 0.05,
) -> dict:
    """Test de proportion bilatéral pour comparer deux variantes."""
    taux_A = conversions_A / visiteurs_A
    taux_B = conversions_B / visiteurs_B

    # Test Z de proportions
    _, p_value = stats.proportions_ztest(
        count=[conversions_A, conversions_B],
        nobs=[visiteurs_A, visiteurs_B],
        alternative="two-sided",
    )

    # Uplift relatif
    uplift = (taux_B - taux_A) / taux_A * 100

    # Puissance statistique (éviter les tests arrêtés trop tôt)
    effect_size = abs(taux_B - taux_A) / np.sqrt((taux_A + taux_B) / 2)
    power_analysis = stats.norm.cdf(
        abs(stats.norm.ppf(alpha / 2)) - effect_size * np.sqrt(visiteurs_A + visiteurs_B) / 2
    )

    return {
        "taux_A": round(taux_A * 100, 2),
        "taux_B": round(taux_B * 100, 2),
        "uplift_pct": round(uplift, 1),
        "p_value": round(p_value, 4),
        "significatif": p_value < alpha,
        "confiance": round((1 - p_value) * 100, 1),
        "puissance": round(power_analysis * 100, 1),
    }

# Calculer la taille d'échantillon minimale avant de lancer le test
def taille_échantillon_minimale(
    taux_baseline: float = 0.05,  # CTR actuel
    uplift_minimum: float = 0.10,  # Amélioration minimale détectable
    alpha: float = 0.05,
    puissance: float = 0.80,
) -> int:
    from statsmodels.stats.power import NormalIndPower
    effect_size = uplift_minimum * taux_baseline / np.sqrt(taux_baseline * (1 - taux_baseline))
    analysis = NormalIndPower()
    return int(analysis.solve_power(effect_size, power=puissance, alpha=alpha))
```

### Métriques primaires et secondaires d'un A/B test de ranking

```
Métriques PRIMAIRES (décision d'adoption) :
├── CTR position 1-3 (clic sur les 3 premiers résultats)
├── Taux de conversion post-search (achat / ajout au panier)
└── Taux de rebond sur la page de résultats

Métriques SECONDAIRES (signaux complémentaires) :
├── Temps passé sur la page de résultats
├── Profondeur de scroll (proportion des utilisateurs qui scrollent)
├── Taux de reformulation (l'utilisateur modifie sa requête immédiatement)
└── Taux de filtre appliqué (les filtres compensent un mauvais ranking)

Durée minimale recommandée :
├── Trafic élevé (> 10K recherches/jour) : 7 jours minimum
├── Trafic moyen (1K-10K/jour) : 14 jours minimum
├── Trafic faible (< 1K/jour) : 30 jours minimum
└── Toujours inclure au moins 2 cycles hebdomadaires complets (saisonnalité)
```

---

## 9. Accessibilité Search — ARIA et Navigation Clavier

### Combobox ARIA conforme WCAG 2.1

```tsx
import { useState, useRef, useId } from "react";

function SearchCombobox({
  suggestions,
  onSearch,
  onSelect,
}: {
  suggestions: string[];
  onSearch: (q: string) => void;
  onSelect: (item: string) => void;
}) {
  const [ouvert, setOuvert] = useState(false);
  const [indexActif, setIndexActif] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const listeId = useId();

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        setIndexActif(i => Math.min(i + 1, suggestions.length - 1));
        break;
      case "ArrowUp":
        e.preventDefault();
        setIndexActif(i => Math.max(i - 1, -1));
        break;
      case "Enter":
        e.preventDefault();
        if (indexActif >= 0) {
          onSelect(suggestions[indexActif]);
          setOuvert(false);
        } else {
          onSearch(inputRef.current?.value || "");
        }
        break;
      case "Escape":
        setOuvert(false);
        setIndexActif(-1);
        inputRef.current?.focus();
        break;
      case "Home":
        e.preventDefault();
        setIndexActif(0);
        break;
      case "End":
        e.preventDefault();
        setIndexActif(suggestions.length - 1);
        break;
    }
  };

  return (
    <div>
      <label htmlFor="search-input">Rechercher</label>
      <input
        id="search-input"
        ref={inputRef}
        type="search"
        role="combobox"
        aria-expanded={ouvert && suggestions.length > 0}
        aria-autocomplete="list"
        aria-controls={listeId}
        aria-activedescendant={
          indexActif >= 0 ? `option-${indexActif}` : undefined
        }
        onKeyDown={handleKeyDown}
        onChange={e => {
          onSearch(e.target.value);
          setOuvert(true);
          setIndexActif(-1);
        }}
        autoComplete="off"
        spellCheck="false"
      />

      {/* Annonce accessible du nombre de résultats */}
      <div role="status" aria-live="polite" className="sr-only">
        {suggestions.length > 0
          ? `${suggestions.length} suggestion${suggestions.length > 1 ? "s" : ""} disponible${suggestions.length > 1 ? "s" : ""}`
          : "Aucune suggestion"}
      </div>

      <ul
        id={listeId}
        role="listbox"
        aria-label="Suggestions de recherche"
        hidden={!ouvert || suggestions.length === 0}
      >
        {suggestions.map((item, i) => (
          <li
            key={item}
            id={`option-${i}`}
            role="option"
            aria-selected={i === indexActif}
            onClick={() => {
              onSelect(item);
              setOuvert(false);
            }}
            onMouseEnter={() => setIndexActif(i)}
          >
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Support lecteur d'écran — Bonnes pratiques

```tsx
// Annoncer les mises à jour de résultats aux lecteurs d'écran
function RésultatsRecherche({ résultats, query, loading }: Props) {
  return (
    <div>
      {/* Zone d'annonce ARIA live pour les mises à jour */}
      <div role="status" aria-live="polite" aria-atomic="true" className="sr-only">
        {loading
          ? "Recherche en cours..."
          : résultats.length > 0
          ? `${résultats.length} résultat${résultats.length > 1 ? "s" : ""} pour "${query}"`
          : `Aucun résultat pour "${query}"`}
      </div>

      {/* Lien d'évitement pour ignorer la barre de recherche */}
      <a href="#résultats-recherche" className="sr-only focus:not-sr-only">
        Aller aux résultats de recherche
      </a>

      {/* Liste de résultats avec navigation clavier */}
      <ul
        id="résultats-recherche"
        role="list"
        aria-label={`Résultats de recherche pour "${query}"`}
      >
        {résultats.map((produit, index) => (
          <li key={produit.id} role="listitem">
            <a
              href={produit.url}
              aria-label={`${produit.nom} — ${produit.prix}€ — Position ${index + 1} sur ${résultats.length}`}
            >
              <img src={produit.image} alt="" aria-hidden="true" />
              <span>{produit.nom}</span>
              <span aria-label={`Prix : ${produit.prix} euros`}>{produit.prix}€</span>
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Checklist accessibilité search

```
Sémantique ARIA
[ ] role="combobox" sur l'input de recherche avec autocomplete
[ ] role="listbox" sur la liste de suggestions
[ ] role="option" sur chaque suggestion
[ ] aria-expanded reflète l'état du menu de suggestions
[ ] aria-activedescendant pointe vers l'option actuellement mise en évidence
[ ] aria-live="polite" pour les annonces de résultats

Navigation clavier
[ ] Flèche bas/haut naviguent dans les suggestions
[ ] Entrée valide la sélection ou soumet la recherche
[ ] Échap ferme le menu et retourne le focus sur l'input
[ ] Origine/Fin naviguent vers la première/dernière suggestion
[ ] Tab ferme le menu sans perdre le focus

Compatibilité lecteurs d'écran
[ ] Testé avec NVDA + Chrome, VoiceOver + Safari
[ ] Annonces en français (lang="fr" sur le document)
[ ] Descriptions alternatives pour les images des résultats (alt="" si décoratives)
[ ] Contraste de couleur ≥ 4.5:1 pour les textes de résultats
```
