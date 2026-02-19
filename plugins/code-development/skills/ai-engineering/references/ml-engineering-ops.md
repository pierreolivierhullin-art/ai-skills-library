# ML Engineering & Operations — Fine-tuning, Model Serving, Monitoring, Cost Optimization, CI/CD for AI

## Overview

Ce document de référence couvre l'ingénierie ML opérationnelle : fine-tuning de modèles (LoRA, QLoRA, full), serving d'inférence, optimisation des performances, monitoring en production, gestion des coûts, pipelines d'évaluation, CI/CD pour l'IA, et conformité données/privacy. Utiliser ce guide pour industrialiser chaque composant IA avec la rigueur d'un système logiciel critique.

---

## 1. Fine-tuning Techniques

### Choosing the Right Approach

```
1. Le modèle produit-il la qualité attendue avec du prompt engineering ?
   +-- Oui → Ne pas fine-tuner. Itérer sur les prompts.
   +-- Non → Le problème est-il un manque de données contextuelles ?
       +-- Oui → RAG. Le fine-tuning ne remplace pas le contexte.
       +-- Non → Le problème est-il un style, format ou comportement spécifique ?
           +-- Oui → Fine-tuning. Préparer un dataset d'entraînement.
           +-- Non → Revoir la formulation du problème.
```

### Technique Comparison

| Technique | Paramètres entraînés | GPU requis | Données nécessaires | Coût estimé | Qualité | Cas d'usage |
|---|---|---|---|---|---|---|
| **Full Fine-tuning** | 100% | 4-8x A100/H100 | 10K-100K+ exemples | 500-5000$ | Maximale | Domaine très spécialisé |
| **LoRA** | 0.1-1% | 1x A100 (40GB) | 1K-10K exemples | 50-200$ | Très bonne | Production standard |
| **QLoRA** | 0.1-1% | 1x RTX 4090 (24GB) | 1K-10K exemples | 10-50$ | Bonne | Budget limité, prototypage |
| **Adapter Tuning** | < 0.1% | 1x GPU 16GB | 500-5K exemples | 5-30$ | Correcte | Adaptation légère |
| **Prompt Tuning** | Soft tokens only | 1x GPU 16GB | 100-1K exemples | < 10$ | Variable | Classification rapide |

### Dataset Quality Checklist

| Critère | Seuil minimum | Recommandé | Impact si non respecté |
|---|---|---|---|
| Taille du dataset | 500 exemples | 2000-5000 | Sous-apprentissage, généralisation faible |
| Diversité des cas | 80% couverture | 95%+ | Biais vers les cas surreprésentés |
| Qualité des labels | Validation humaine 10% | 30% | Apprentissage de patterns erronés |
| Format cohérent | 100% valides | + validation auto | Erreurs d'entraînement |
| Déduplication | Pas de doublons exacts | Pas de near-duplicates | Surajustement |

### Hyperparamètres recommandés

| Paramètre | LoRA | Full Fine-tuning | Notes |
|---|---|---|---|
| Learning rate | 1e-4 à 2e-4 | 1e-5 à 5e-5 | Trop élevé = instabilité |
| Batch size effectif | 32-64 | 32-128 | Via gradient accumulation |
| Epochs | 2-4 | 1-3 | Au-delà de 5 = surajustement |
| LoRA rank (r) | 16 (8-64) | N/A | lora_alpha = 2x r |
| Warmup ratio | 0.03-0.1 | 0.03-0.1 | Stabilise le début |
| Weight decay | 0.01-0.1 | 0.01 | Prévient le surajustement |

---

## 2. Model Serving

### Serving Infrastructure Options

| Solution | Type | Scaling | Latence | Coût | Idéal pour |
|---|---|---|---|---|---|
| **vLLM** | Self-hosted | K8s | Très faible | GPU + infra | Production haute perf |
| **TGI** | Self-hosted | Docker/K8s | Faible | GPU + infra | Écosystème HuggingFace |
| **Ollama** | Local | Limité | Faible | CPU/GPU local | Dev, edge, privacy |
| **Together AI** | API managed | Auto | Moyenne | Pay-per-token | Prod sans infra GPU |
| **Replicate** | API managed | Auto | Variable | Pay-per-second | Prototypage, custom |
| **Modal** | Serverless GPU | Auto | Variable | GPU-second | Batch, inférence burst |

### Scaling Strategies

```
1. Volume de requêtes ?
   +-- < 10 req/s → Instance unique + batching continu
   +-- 10-100 req/s → Horizontal scaling (2-4 replicas) + load balancer
   +-- > 100 req/s → Auto-scaling K8s + batching agressif
   +-- Burst irrégulier → Serverless GPU (Modal, Replicate)
```

| Stratégie | Gain throughput | Impact latence | Complexité |
|---|---|---|---|
| **Continuous batching** | 2-5x | Neutre | Faible (natif vLLM/TGI) |
| **Speculative decoding** | 1.5-2.5x | -30 à -50% | Moyenne |
| **Tensor parallelism** | Linéaire (GPUs) | Réduction | Moyenne (multi-GPU) |
| **Prefix caching** | 1.5-3x | TTFT -50 à -80% | Faible |
| **Horizontal scaling** | Linéaire (replicas) | Neutre | Moyenne |

---

## 3. Inference Optimization

### Quantization Techniques

| Technique | Précision | Réduction mémoire | Impact qualité | Vitesse | Quand l'utiliser |
|---|---|---|---|---|---|
| **FP16** | 16-bit | Baseline | Aucun | Baseline | Référence |
| **INT8** | 8-bit | ~50% | < 1% | +20-40% | Production standard |
| **GPTQ** | 4-bit post-training | ~75% | 1-3% | +50-100% | Production optimisée |
| **AWQ** | 4-bit activation-aware | ~75% | < 1% | +50-100% | Meilleur ratio qualité/taille |
| **GGUF** | 2-8 bit flexible | 60-85% | Variable | Variable | CPU, edge, Ollama |
| **FP8** | 8-bit native (H100) | ~50% | Quasi nul | +30-50% | H100/H200 |

### KV Cache & Advanced Optimizations

| Technique | Réduction mémoire | Impact qualité | Support |
|---|---|---|---|
| **PagedAttention** (vLLM) | 60-80% fragmentation éliminée | Aucun | vLLM natif |
| **KV cache quantization** | 50% | Minimal | vLLM, TGI |
| **Grouped-Query Attention** | 4-8x vs MHA | Intégré au modèle | Llama 3, Mistral |
| **Speculative decoding** | N/A (latence) | Aucun (mathématiquement identique) | vLLM, TGI |

Le speculative decoding utilise un modèle draft léger pour proposer N tokens que le modèle principal vérifie en un seul forward pass. Gain : 1.5-2.5x en latence sans perte de qualité. Taux d'acceptation cible : > 70%.

---

## 4. AI Monitoring in Production

### Quality Monitoring

| Méthode | Fréquence | Coût | Fiabilité |
|---|---|---|---|
| **LLM-as-Judge sampling** (5-10% des requêtes) | Continu | Modéré | Bonne |
| **Exact match monitoring** (outputs structurés) | 100% | Quasi nul | Élevée |
| **User feedback** (thumbs up/down, corrections) | Continu | Quasi nul | Variable |
| **Drift detection** (distribution vs baseline) | Quotidien | Faible | Bonne |
| **Golden set regression** (re-run evals prod) | Hebdomadaire | Faible | Élevée |

### Performance Monitoring

| Métrique | Cible | Warning | Critique | Outil |
|---|---|---|---|---|
| **TTFT** | < 500ms | > 1s | > 3s | Langfuse, Helicone |
| **Tokens/s** | > 30 | < 15 | < 5 | Prometheus |
| **Latence P95** | < 3s | > 5s | > 10s | Datadog, Grafana |
| **Taux d'erreur** | < 0.1% | > 1% | > 5% | APM |
| **GPU utilization** | 70-90% | < 40% | > 95% | DCGM |

### Cost Monitoring — Three Levels

```
Niveau 1 — Par requête
+-- Tokens (input + output) x prix/token + coûts annexes (embedding, re-ranking)
+-- Cible : < 0.01$ standard, < 0.10$ complexe

Niveau 2 — Par feature
+-- Coût agrégé de toutes les requêtes d'une feature vs revenu généré
+-- Cible : coût IA < 10% du revenu de la feature

Niveau 3 — Par utilisateur
+-- Coût IA par utilisateur actif, par plan tarifaire
+-- Cible : marge positive sur chaque plan
```

### Alerting Strategy

| Alerte | Trigger | Action | Escalade |
|---|---|---|---|
| **Qualité dégradée** | Score < seuil sur 1h | Investiguer prompts | > 4h → rollback |
| **Latence élevée** | P95 > 2x baseline 15min | Vérifier scaling, GPU | > 30min → scale up |
| **Explosion coûts** | Coût horaire > 2x moyenne | Vérifier trafic vs anomalie | Non justifié → rate limit |
| **Taux d'erreur** | > 1% sur 5min | Vérifier provider, network | > 5% → fallback chain |

---

## 5. Cost Management

### Cost per Token by Provider (2025-2026)

| Provider / Modèle | Input ($/1M tok) | Output ($/1M tok) | Context | Notes |
|---|---|---|---|---|
| **Claude Opus 4** | 15.00 | 75.00 | 200K | Meilleur raisonnement |
| **Claude Sonnet 4** | 3.00 | 15.00 | 200K | Meilleur rapport qualité/prix |
| **Claude Haiku 3.5** | 0.80 | 4.00 | 200K | Classification, extraction |
| **GPT-4o** | 2.50 | 10.00 | 128K | Multimodal natif |
| **GPT-4o-mini** | 0.15 | 0.60 | 128K | Haut volume, tâches simples |
| **Gemini 2.0 Flash** | 0.10 | 0.40 | 1M | Contexte long, coût minimal |
| **Llama 3.1 70B** (Together) | 0.90 | 0.90 | 128K | Open source |
| **Mistral Large** | 2.00 | 6.00 | 128K | Alternatif européen |

*Tarifs indicatifs, vérifier les tarifs actuels sur les sites des providers.*

### Model Routing for Cost Optimization

```
Requête entrante → Classifier la complexité (règles + LLM léger)
   +-- Simple (classification, extraction) → Haiku / GPT-4o-mini / Flash (0.001-0.005$)
   +-- Moyen (résumé, analyse, Q&A) → Sonnet / GPT-4o (0.01-0.05$)
   +-- Complexe (raisonnement, code) → Opus / GPT-4o (0.05-0.50$)
   +-- Fallback → Si échec → modèle supérieur avec retry
```

Impact mesuré : le model routing réduit le coût moyen de 40-70% sans dégradation mesurable de la qualité.

### Caching & Batch Strategies

| Stratégie | Réduction coûts | Complexité | Fraîcheur |
|---|---|---|---|
| **Prompt caching** (natif Anthropic/OpenAI) | 50-90% préfixe | Nulle | Temps réel |
| **Semantic caching** | 30-60% | Moyenne | TTL |
| **Exact match caching** | 20-40% | Faible | TTL |
| **Batch processing** (offline) | 50-70% | Moyenne | Différé |

### ROI Calculation

| Élément | Formule | Exemple |
|---|---|---|
| **Coût IA mensuel** | requêtes/mois x coût/requête | 100K x 0.02$ = 2,000$/mois |
| **Coût infra** | GPUs x prix/h x heures | 4x A100 x 2$/h x 720h = 5,760$ |
| **Valeur générée** | Temps économisé x coût/h + revenu | 500h x 50$ + 10K$ = 35K$ |
| **ROI** | (Valeur - Coût) / Coût x 100 | (35K - 7.7K) / 7.7K = 355% |

---

## 6. Evaluation Pipelines

### Eval Suite Architecture

```
Code change (prompt, config, modèle)
   +-- CI trigger → Load eval dataset (100-500 cas)
   +-- Run inference → Score (exact match, LLM-as-Judge, custom)
   +-- Comparer avec baseline
       +-- Amélioration ou stable → PR approuvée (eval gate pass)
       +-- Régression détectée → PR bloquée, rapport généré
```

### Eval Metrics by Task Type

| Tâche | Métriques | Seuil typique | Scoring |
|---|---|---|---|
| **Classification** | Accuracy, F1 | > 95% | Exact match |
| **Extraction structurée** | Field accuracy, schema compliance | > 98% schema | JSON diff |
| **Résumé** | Faithfulness, coverage | > 4.0/5.0 | LLM-as-Judge |
| **Q&A** | Correctness, groundedness | > 90% correct | LLM-as-Judge + exact |
| **Code generation** | Pass rate, test pass | > 80% pass@1 | Execution-based |

### Eval Tools Comparison

| Outil | Forces | CI | Prix |
|---|---|---|---|
| **Promptfoo** | Open source, CLI-first | Excellente | Gratuit |
| **Braintrust** | UI riche, datasets versionnés | Bonne | Freemium |
| **Langfuse** | Observabilité + evals, open source | Bonne | Gratuit (self-hosted) |
| **Langsmith** | Intégration LangChain | Bonne | Payant |
| **Arize Phoenix** | Open source, tracing + evals | Moyenne | Gratuit |

### Eval Dataset Sources

| Source | Volume | Qualité | Coût |
|---|---|---|---|
| **Expert (manuel)** | 50-200 cas | Excellente | Élevé |
| **Production sampling** | 100-1000+ | Variable | Modéré |
| **Synthétique (LLM)** | 500-5000 | Bonne si validée | Faible |
| **Adversarial** | 50-100 | Critique | Modéré |

---

## 7. AI CI/CD

### Eval Gates in CI

Chaque modification de prompt ou config IA déclenche automatiquement la suite d'évaluation. Configurer un workflow CI (GitHub Actions, GitLab CI) qui : (1) exécute les evals via Promptfoo ou Braintrust, (2) compare les scores avec la baseline, (3) bloque la PR si régression > seuil de tolérance (typiquement 2-5%).

### Model Migration Pipeline

| Étape | Action | Critère de passage |
|---|---|---|
| 1. Benchmark | Run complet evals sur le nouveau modèle | Scores documentés |
| 2. Comparaison | Diff avec le modèle actuel | Pas de régression > 2% |
| 3. Ajustement | Adapter les prompts aux spécificités du modèle | Evals passent après ajustement |
| 4. Shadow mode | Deux modèles en parallèle | Concordance > 95% |
| 5. Canary | 5% trafic nouveau modèle | Métriques stables |
| 6. Rollout | 5% → 25% → 50% → 100% | Monitoring à chaque palier |

### Feature Flags for AI

| Flag | Usage | Granularité |
|---|---|---|
| `ai.model.provider` | Switcher entre providers | Global / par feature |
| `ai.model.version` | Version du modèle | Par feature / segment |
| `ai.feature.enabled` | Activer/désactiver feature IA | Par user, plan, org |
| `ai.routing.strategy` | Stratégie de routing (cost, quality) | Global |
| `ai.guardrails.strict` | Niveau des guardrails | Par environnement |

---

## 8. Data & Privacy

### PII Handling in Prompts

| Type de PII | Risque | Traitement |
|---|---|---|
| **Noms, emails, téléphones** | Identification directe | Pseudonymisation |
| **Adresses** | Localisation | Anonymisation / agrégation |
| **N. sécu, CB** | Très sensible | Ne jamais envoyer. Masquage intégral. |
| **Données médicales** | Sensible (RGPD art. 9) | Anonymisation stricte + consentement |

### GDPR for AI Systems

| Obligation RGPD | Application IA | Implémentation |
|---|---|---|
| **Base légale** (art. 6) | Justifier le traitement par le LLM | Intérêt légitime ou consentement |
| **Minimisation** (art. 5) | Données nécessaires seulement | Filtrage avant appel API |
| **Droit d'effacement** (art. 17) | Supprimer données des logs IA | Pipeline couvrant logs, caches, traces |
| **Transparence** (art. 13-14) | Informer que l'IA est utilisée | Notice CGU, in-app disclosure |
| **AIPD** (art. 35) | Impact pour traitements à risque | Documenter risques et mesures |

### Data Retention

| Donnée | Rétention | Justification |
|---|---|---|
| Prompts et réponses (logs) | 30-90 jours | Debugging, qualité |
| Traces d'observabilité | 90-180 jours | Performance, coûts |
| Eval datasets | Indéfinie (versionnée) | Régression testing |
| Données fine-tuning | Durée du modèle + 1 an | Reproductibilité, audit |

---

## 9. State of the Art (2025-2026)

**Synthetic data for fine-tuning** — La génération de données synthétiques par des LLMs frontier pour entraîner des modèles spécialisés est devenue standard. Datasets synthétiques bien conçus : 80-95% de la qualité humaine à 10% du coût.

**Model merging** — Les techniques TIES, DARE, SLERP permettent de fusionner des modèles fine-tunés sans entraînement additionnel. Prometteuse pour combiner des expertises domaine.

**Mixture of Agents** — Architectures multi-agents (proposer, critiquer, synthétiser) surpassant les modèles uniques sur les tâches complexes. Gains : +10-20% qualité.

**AI cost commoditization** — Le coût d'inférence baisse de 50-70% par an. Implication : ne pas sur-investir en optimisation de coûts, privilégier l'agilité et la qualité.

**Inference-time compute scaling** — Chain-of-thought étendu, best-of-N sampling, self-consistency. Trade-off : plus de tokens = meilleure qualité = coût supérieur. Router les requêtes complexes vers un budget compute élevé.

| Tendance | Maturité | Impact | Action |
|---|---|---|---|
| **Synthetic data** | Production-ready | Coût fine-tuning -90% | Adopter systématiquement |
| **Model merging** | Expérimental-avancé | Simplifie multi-modèles | Explorer cas multi-domaines |
| **Mixture of Agents** | Production (cas ciblés) | Qualité +10-20% | Évaluer haute exigence |
| **Cost commoditization** | Confirmée | ROI optimisations réduit | Privilégier agilité |
| **Inference-time compute** | Production-ready | Levier qualité dynamique | Intégrer au model routing |

---

## Quick Reference — Decision Checklist

```
Fine-tuning : est-ce nécessaire ?
+-- Prompt engineering + few-shot atteignent les seuils ? → Ne pas fine-tuner
+-- Manque de données contextuelles ? → RAG, pas fine-tuning
+-- Style/comportement spécifique ? → Fine-tuner
+-- Budget < 100$ ? → QLoRA | 100-500$ ? → LoRA | > 500$ ? → Full

Serving : comment déployer ?
+-- Privacy/compliance → vLLM ou TGI self-hosted
+-- Volume < 1000 req/jour → API provider
+-- Volume élevé + open source → vLLM sur K8s
+-- Prototypage → Ollama (local) ou Replicate (cloud)

Monitoring : quoi surveiller ?
+-- Qualité → LLM-as-Judge sampling + golden set regression
+-- Performance → TTFT, throughput, P95 latence
+-- Coûts → Par requête, par feature, par utilisateur
+-- Sécurité → PII detection, guardrail triggers, anomalies
```
