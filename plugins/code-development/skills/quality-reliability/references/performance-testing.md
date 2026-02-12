# Performance Testing / Tests de performance

Reference approfondie sur le load testing, le stress testing, le benchmarking de performance, la performance frontend et les budgets de performance.

Deep-dive reference on load testing, stress testing, performance benchmarking, frontend performance, and performance budgets.

---

## Table of Contents

1. [Load Testing Tools](#load-testing-tools)
2. [Stress Testing & Capacity Planning](#stress-testing--capacity-planning)
3. [Performance Benchmarking](#performance-benchmarking)
4. [Frontend Performance](#frontend-performance)
5. [Database Performance Testing](#database-performance-testing)
6. [Performance Budgets](#performance-budgets)

---

## Load Testing Tools

### k6 (Recommended Standard 2024-2026)

k6 est le framework de reference pour le load testing moderne. Developpe par Grafana Labs, il combine une syntaxe JavaScript accessible, une execution performante en Go, et une integration native avec l'ecosysteme d'observabilite (Prometheus, Grafana, Datadog).

k6 is the reference framework for modern load testing. Developed by Grafana Labs, it combines accessible JavaScript syntax, performant Go execution, and native integration with the observability ecosystem.

**Forces / Strengths:**
- Scripts en JavaScript/TypeScript : accessible pour les developpeurs, versionnable, testable.
- Execution locale haute performance (un seul processus peut generer des milliers de VUs).
- Scenarios avances : ramping VUs, constant arrival rate, externally controlled.
- Extensions natives : support gRPC, WebSocket, SQL, Redis, Kafka.
- Integration CI/CD transparente : seuils (thresholds) et exit codes pour echouer le pipeline.
- k6 Cloud pour le load testing distribue a grande echelle.
- Export natif vers Prometheus, InfluxDB, Datadog, Grafana Cloud.

**Architecture de test recommandee / Recommended test architecture:**

```javascript
// load-tests/checkout-flow.js
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const checkoutErrors = new Rate('checkout_errors');
const checkoutDuration = new Trend('checkout_duration');

export const options = {
  scenarios: {
    // Scenario 1: Normal load - simule le trafic quotidien
    average_load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '3m', target: 50 },   // ramp-up
        { duration: '10m', target: 50 },   // steady state
        { duration: '3m', target: 0 },     // ramp-down
      ],
      gracefulRampDown: '30s',
    },
    // Scenario 2: Peak load - simule les pics (Black Friday)
    peak_load: {
      executor: 'ramping-vus',
      startVUs: 0,
      startTime: '20m',
      stages: [
        { duration: '2m', target: 200 },
        { duration: '5m', target: 200 },
        { duration: '2m', target: 0 },
      ],
    },
    // Scenario 3: Spike test - pic soudain
    spike: {
      executor: 'ramping-vus',
      startVUs: 0,
      startTime: '30m',
      stages: [
        { duration: '10s', target: 500 },
        { duration: '1m', target: 500 },
        { duration: '10s', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1500'],
    http_req_failed: ['rate<0.01'],
    checkout_errors: ['rate<0.02'],
    checkout_duration: ['p(95)<3000'],
  },
};

export default function () {
  const baseUrl = __ENV.BASE_URL || 'https://staging.example.com';
  const token = authenticateUser();

  group('Browse products', () => {
    const catalog = http.get(`${baseUrl}/api/products`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    check(catalog, { 'catalog loaded': (r) => r.status === 200 });
    sleep(Math.random() * 3 + 1); // think time realiste
  });

  group('Add to cart', () => {
    const addResponse = http.post(
      `${baseUrl}/api/cart/items`,
      JSON.stringify({ productId: 'prod_123', quantity: 1 }),
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      }
    );
    check(addResponse, { 'item added': (r) => r.status === 201 });
  });

  group('Checkout', () => {
    const start = Date.now();
    const checkout = http.post(`${baseUrl}/api/checkout`, null, {
      headers: { Authorization: `Bearer ${token}` },
    });
    checkoutDuration.add(Date.now() - start);
    const success = check(checkout, {
      'checkout succeeded': (r) => r.status === 200,
    });
    checkoutErrors.add(!success);
  });

  sleep(Math.random() * 2 + 1);
}

function authenticateUser() {
  const res = http.post(`${__ENV.BASE_URL}/api/auth/login`, JSON.stringify({
    email: `loadtest+${__VU}@example.com`,
    password: 'LoadTest123!',
  }), { headers: { 'Content-Type': 'application/json' } });
  return res.json('token');
}
```

### JMeter

Apache JMeter reste utilise dans les organisations entreprise avec des equipes QA dediees. Son interface graphique facilite la creation de plans de test pour les non-developpeurs.

**Forces:** interface graphique, large ecosysteme de plugins, support de nombreux protocoles (HTTP, JDBC, JMS, SMTP, LDAP), execution distribuee.
**Limites:** gourmand en ressources (JVM), scripts XML difficiles a versionner, courbe d'apprentissage pour les scenarios complexes, interface datee.

**Recommandation / Recommendation:** Utiliser JMeter quand l'equipe QA n'est pas familiere avec le code ou quand des protocoles specifiques (JMS, LDAP) doivent etre testes. Pour les nouveaux projets, preferer k6. / Use JMeter when the QA team is not code-familiar or when specific protocols need testing. For new projects, prefer k6.

### Gatling

Gatling offre un DSL Scala/Java/Kotlin pour ecrire des tests de charge expressifs. Il genere des rapports HTML detailles automatiquement.

**Forces:** DSL expressif, rapports HTML riches, execution performante (Akka/Netty), bon support des scenarios complexes avec pauses et correlations.
**Limites:** DSL Scala peut intimider les equipes non-JVM, moins d'integrations cloud natives que k6.

### Locust

Locust est un framework Python pour le load testing. Ideal pour les equipes Python qui veulent ecrire des scenarios de charge dans leur langage de predilection.

```python
from locust import HttpUser, task, between

class CheckoutUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def browse_products(self):
        self.client.get("/api/products")

    @task(1)
    def checkout(self):
        self.client.post("/api/cart/items",
                        json={"productId": "prod_123", "quantity": 1})
        self.client.post("/api/checkout")
```

### Matrice de decision / Decision Matrix

| Critere / Criterion | k6 | JMeter | Gatling | Locust |
|---|---|---|---|---|
| Langage des scripts | JavaScript | XML/GUI | Scala/Java/Kotlin | Python |
| Performance | Excellente (Go) | Moyenne (JVM) | Bonne (JVM) | Bonne (Python) |
| CI/CD integration | Excellente | Moderee | Bonne | Bonne |
| Rapports | Via Grafana/Cloud | Integres | HTML riches | UI web temps reel |
| Courbe d'apprentissage | Faible | Moyenne | Moyenne-Haute | Faible |
| Cloud/distribue | k6 Cloud | Remote, distribue | Gatling Enterprise | Distribue natif |
| **Recommandation** | **Standard 2025** | Entreprise/legacy | Equipes JVM | Equipes Python |

---

## Stress Testing & Capacity Planning

### Types de tests de performance / Performance Test Types

Distinguer clairement les types de tests de performance et leur objectif :

| Type | Objectif / Purpose | Configuration |
|---|---|---|
| **Load Test** | Valider le comportement sous charge nominale | Charge = trafic normal attendu |
| **Stress Test** | Trouver le point de rupture du systeme | Charge croissante jusqu'a l'echec |
| **Spike Test** | Valider la reaction a un pic soudain | Montee brutale (0 a Nmax en secondes) |
| **Soak Test** (endurance) | Detecter les fuites memoire et la degradation | Charge moderee sur 4-24 heures |
| **Breakpoint Test** | Determiner la capacite maximale | Charge incrementale progressive |
| **Scalability Test** | Valider l'auto-scaling | Charge progressive + monitoring scaling |

### Capacity Planning

Planifier la capacite en suivant cette methodologie :

Plan capacity following this methodology:

1. **Baseline** : mesurer la performance actuelle sous charge normale (latence p50/p95/p99, throughput, utilisation ressources).
2. **Projection** : estimer la croissance du trafic (croissance organique + evenements prevus comme campagnes marketing, lancement produit).
3. **Headroom** : maintenir une marge de 30-50% entre la capacite maximale et la charge projetee.
4. **Validation** : executer des stress tests pour verifier que le headroom prevu est atteignable.
5. **Auto-scaling** : configurer l'auto-scaling (HPA Kubernetes, AWS Auto Scaling) et valider qu'il reagit dans les temps requis.

### Methodologie de stress test / Stress Test Methodology

```
Phase 1: Baseline        — Charge normale pendant 10 min (mesurer les metriques de reference)
Phase 2: Ramp-up         — Augmentation progressive (10% par palier de 5 min)
Phase 3: Breaking point  — Identifier le moment ou les SLOs sont violes
Phase 4: Beyond breaking — Continuer 5 min au-dela du point de rupture
Phase 5: Recovery        — Retour a la charge normale, mesurer le temps de recovery
```

**Criteres de rupture / Breaking point criteria:**
- Latence p99 > 3x la baseline
- Taux d'erreur > 5%
- CPU > 90% soutenu
- Memoire > 85% soutenue
- Queue depth croissante (backlog qui ne se resorbe pas)

---

## Performance Benchmarking

### Metriques cles / Key Metrics

Mesurer systematiquement ces metriques pour chaque benchmark :

| Metrique / Metric | Description | Seuil typique / Typical Threshold |
|---|---|---|
| **Throughput** (req/s) | Nombre de requetes traitees par seconde | Depend du systeme |
| **Latency p50** | Latence mediane | < 100ms (API), < 200ms (page) |
| **Latency p95** | Latence 95e percentile | < 500ms (API), < 1s (page) |
| **Latency p99** | Latence 99e percentile | < 1s (API), < 2s (page) |
| **Error rate** | Pourcentage de requetes en erreur | < 0.1% (cible SRE) |
| **Saturation** | Utilisation des ressources (CPU, RAM, I/O) | < 70% en charge normale |
| **Apdex** | Score de satisfaction (0-1) | > 0.9 |

### Benchmarking en CI/CD

Integrer le benchmarking dans le pipeline CI pour detecter les regressions de performance automatiquement :

```yaml
# GitHub Actions - Performance regression detection
performance-benchmark:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run k6 benchmark
      run: |
        k6 run --out json=results.json load-tests/benchmark.js
    - name: Compare with baseline
      uses: grafana/k6-action@v1
      with:
        filename: load-tests/benchmark.js
        cloud: false
    - name: Assert no regression
      run: |
        # Comparer les resultats avec la baseline stockee
        python scripts/compare-perf.py results.json baseline.json --threshold 10
```

### Microbenchmarking

Pour le benchmarking au niveau du code (fonctions, algorithmes), utiliser des outils specifiques :

- **JavaScript/TypeScript** : `vitest bench`, `tinybench`, Benchmark.js
- **Python** : `pytest-benchmark`, `timeit`
- **Java** : JMH (Java Microbenchmark Harness)
- **Go** : `testing.B` (natif)
- **Rust** : `criterion.rs`

```typescript
// Vitest bench example
import { bench, describe } from 'vitest';

describe('Array sorting', () => {
  const data = Array.from({ length: 10000 }, () => Math.random());

  bench('Array.sort', () => {
    [...data].sort((a, b) => a - b);
  });

  bench('Custom quicksort', () => {
    quicksort([...data]);
  });
});
```

---

## Frontend Performance

### Core Web Vitals (2024-2026)

Les Core Web Vitals sont les metriques de performance frontend definies par Google, impactant directement le SEO et l'experience utilisateur.

Core Web Vitals are Google-defined frontend performance metrics directly impacting SEO and user experience.

| Metrique | Description | Seuil "Good" | Mesure |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | Temps de chargement du plus grand element visible | < 2.5s | Vitesse de chargement percue |
| **INP** (Interaction to Next Paint) | Reactivite aux interactions utilisateur (remplace FID depuis 2024) | < 200ms | Reactivite |
| **CLS** (Cumulative Layout Shift) | Decalages visuels inattendus durant le chargement | < 0.1 | Stabilite visuelle |

### Outils de mesure / Measurement Tools

**Lighthouse:**
- Audit automatise de performance, accessibilite, SEO, bonnes pratiques.
- Integrable en CI via `lighthouse-ci` pour detecter les regressions.
- Score de 0 a 100 par categorie.

```yaml
# lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/', 'http://localhost:3000/products'],
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'first-contentful-paint': ['warn', { maxNumericValue: 1500 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'interactive': ['warn', { maxNumericValue: 3500 }],
      },
    },
    upload: {
      target: 'lhci',
      serverBaseUrl: 'https://lhci.example.com',
    },
  },
};
```

**SpeedCurve:**
- Monitoring de performance synthetique et RUM (Real User Monitoring) continu.
- Comparaison avec les concurrents et suivi de tendance dans le temps.
- Alerting automatique sur la degradation des Core Web Vitals.
- Ideal pour les equipes produit qui veulent un dashboard non-technique.

**Web Vitals library (Google):**
- Mesure des Core Web Vitals directement dans le navigateur de l'utilisateur (RUM).
- Envoi des donnees vers un backend d'analytics pour un monitoring reel.

```typescript
import { onLCP, onINP, onCLS } from 'web-vitals';

function sendToAnalytics(metric) {
  fetch('/api/metrics', {
    method: 'POST',
    body: JSON.stringify({
      name: metric.name,
      value: metric.value,
      rating: metric.rating, // 'good', 'needs-improvement', 'poor'
      delta: metric.delta,
      id: metric.id,
      navigationType: metric.navigationType,
    }),
  });
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

### Strategies d'optimisation frontend / Frontend Optimization Strategies

Appliquer ces techniques pour atteindre les seuils "Good" des Core Web Vitals :

**Pour le LCP :**
- Precharger les ressources critiques (`<link rel="preload">`).
- Optimiser les images (WebP/AVIF, lazy loading, `srcset` pour les tailles responsives).
- Utiliser un CDN avec edge caching.
- Server-Side Rendering (SSR) ou Static Site Generation (SSG) pour le contenu above-the-fold.
- Eliminer les ressources bloquant le rendu (CSS/JS critiques inline, defer le reste).

**Pour le INP :**
- Fractionner les longues taches JavaScript (> 50ms) via `requestIdleCallback` ou `scheduler.yield()`.
- Utiliser les Web Workers pour les calculs lourds hors du thread principal.
- Optimiser les event handlers (debounce, throttle).
- Reduire la taille du DOM (< 1500 noeuds cible).
- Utiliser `content-visibility: auto` pour le contenu hors viewport.

**Pour le CLS :**
- Definir `width` et `height` explicites sur les images et iframes.
- Reserver l'espace pour le contenu dynamique (ads, embeds).
- Eviter les injections de contenu au-dessus du contenu visible.
- Utiliser `font-display: swap` avec des polices web.

---

## Database Performance Testing

### Approche / Approach

Tester la performance de la base de donnees independamment pour identifier les goulots d'etranglement avant qu'ils n'affectent l'application.

Test database performance independently to identify bottlenecks before they affect the application.

**Metriques a mesurer / Metrics to measure:**
- Temps d'execution des requetes (p50, p95, p99).
- Nombre de requetes par seconde.
- Utilisation CPU et I/O de la base de donnees.
- Pool de connexions : utilisation, saturation, temps d'attente.
- Taille des resultats et quantite de donnees transferees.

### Strategies de test / Testing strategies

1. **Query profiling** : activer le slow query log (PostgreSQL: `log_min_duration_statement`, MySQL: `slow_query_log`). Analyser les requetes lentes avec `EXPLAIN ANALYZE`.
2. **Index validation** : verifier que chaque requete critique utilise un index. Scanner les seq scans dans les plans d'execution.
3. **Load testing avec donnees realistes** : tester avec un volume de donnees representatif de la production (anonymisees). Les performances avec 1000 lignes sont non representatives d'un million.
4. **Connection pool stress** : saturer le pool de connexions pour valider le comportement sous contention (timeouts, queuing).
5. **N+1 detection** : utiliser des outils comme `pg_stat_statements`, `bullet` (Rails), ou des middleware custom pour detecter les requetes N+1.

```sql
-- PostgreSQL: identifier les requetes les plus lentes
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Verifier l'utilisation des index
SELECT schemaname, tablename, seq_scan, idx_scan,
       CASE WHEN seq_scan + idx_scan > 0
            THEN round(100.0 * idx_scan / (seq_scan + idx_scan), 1)
            ELSE 0
       END AS idx_scan_pct
FROM pg_stat_user_tables
ORDER BY seq_scan DESC;
```

---

## Performance Budgets

### Definition / Definition

Un budget de performance est un ensemble de limites quantitatives sur les metriques de performance qu'une application ne doit pas depasser. Il transforme la performance d'une preoccupation subjective en une contrainte mesurable et automatisable.

A performance budget is a set of quantitative limits on performance metrics that an application must not exceed. It transforms performance from a subjective concern into a measurable, automatable constraint.

### Categories de budgets / Budget Categories

| Categorie | Metrique | Budget typique |
|---|---|---|
| **Timing** | LCP | < 2.5s |
| **Timing** | INP | < 200ms |
| **Timing** | Time to Interactive | < 3.5s |
| **Taille** | JavaScript total (compresse) | < 200 KB |
| **Taille** | CSS total (compresse) | < 50 KB |
| **Taille** | Images above-the-fold | < 200 KB |
| **Taille** | Page weight totale | < 1 MB |
| **Comptage** | Requetes HTTP (first load) | < 50 |
| **Comptage** | Third-party scripts | < 5 |
| **Score** | Lighthouse Performance | > 90 |
| **Backend** | API response time p95 | < 500ms |
| **Backend** | Throughput minimum | > N req/s |

### Enforcement automatise / Automated Enforcement

Integrer les budgets de performance comme quality gates dans le pipeline CI :

```javascript
// bundlesize.config.js
module.exports = {
  files: [
    { path: 'dist/js/*.js', maxSize: '200 kB', compression: 'gzip' },
    { path: 'dist/css/*.css', maxSize: '50 kB', compression: 'gzip' },
    { path: 'dist/index.html', maxSize: '20 kB' },
  ],
};
```

```yaml
# CI pipeline - Performance budget gate
- name: Check bundle size
  run: npx bundlesize
- name: Lighthouse CI
  run: npx lhci autorun
- name: k6 performance test
  run: k6 run --thresholds load-tests/budget-check.js
```

### Processus de gestion des budgets / Budget Management Process

1. **Etablir la baseline** : mesurer la performance actuelle comme point de depart.
2. **Definir les budgets** : fixer des limites basees sur les objectifs metier et les benchmarks industriels.
3. **Automatiser l'enforcement** : integrer les checks dans la CI. Bloquer les PRs qui depassent les budgets.
4. **Alerter en production** : surveiller les metriques RUM en continu. Alerter quand les budgets sont proches d'etre depasses.
5. **Reviser trimestriellement** : ajuster les budgets en fonction de l'evolution du produit et des standards industriels.

---

## Summary Checklist / Checklist de synthese

- [ ] k6 est l'outil standard pour le load testing, avec des scripts en JavaScript versionnes
- [ ] Chaque type de test de performance (load, stress, spike, soak) est planifie et execute regulierement
- [ ] Le capacity planning integre une marge de 30-50% au-dela de la charge projetee
- [ ] Les Core Web Vitals (LCP, INP, CLS) sont mesures en RUM et en synthethique
- [ ] Lighthouse CI est integre dans le pipeline avec des seuils de performance
- [ ] Les budgets de performance sont definis, automatises et bloquer les PRs en cas de depassement
- [ ] La performance de la base de donnees est monitoree (slow queries, pool saturation, N+1)
- [ ] Les benchmarks de performance sont executes en CI pour detecter les regressions
- [ ] L'auto-scaling est valide par des tests de charge simulant des pics realistes
