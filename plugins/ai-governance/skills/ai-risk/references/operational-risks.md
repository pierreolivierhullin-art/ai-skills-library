# Operational Risks — Hallucinations, Drift, Vendor Dependencies & Incidents

Reference complete pour les risques operationnels des systemes IA en production : detection et attenuation des hallucinations, model drift, dependance fournisseur, gestion des couts, optimisation de la latence, disponibilite, bases de donnees d'incidents IA, et risques lies aux deepfakes (2024-2026).

---

## Hallucination Detection & Grounding

### Taxonomie des hallucinations

| Type | Description | Exemple | Detectabilite |
|------|-------------|---------|---------------|
| **Factuelle** | Fait invente ou incorrect | "La Tour Eiffel mesure 450 metres" | Elevee (verifiable) |
| **Attributive** | Citation ou source inventee | "Selon l'etude de Smith et al. (2023)..." (inexistante) | Elevee (verifiable) |
| **Logique** | Raisonnement fallacieux | Conclusion qui ne decoule pas des premisses | Moyenne |
| **Confabulatoire** | Memoire inventee, contexte fictif | "Comme vous l'avez mentionne precedemment..." (non dit) | Elevee |
| **Numerique** | Calcul ou statistique incorrects | "25% de 80 = 25" | Elevee (calculable) |
| **Temporelle** | Evenement date incorrectement | "Le Brexit a eu lieu en 2020" | Elevee (verifiable) |
| **Semantique** | Contresens ou mauvaise interpretation | Melange de concepts proches mais distincts | Moyenne-Faible |
| **Partielle** | Information partiellement correcte, partiellement inventee | Fait reel avec details inventes | Faible (plus dangereux) |

### Metriques de detection des hallucinations

**Pour les systemes RAG :**

- **Faithfulness** : Le contenu genere est-il fidele aux documents sources recuperes ? Mesurer via des classifiers NLI (Natural Language Inference) qui evaluent si chaque claim de la reponse est entaillee par les documents sources.
- **Answer Relevancy** : La reponse est-elle pertinente par rapport a la question posee ? Mesurer via la similarite semantique entre la question et la reponse.
- **Context Relevancy** : Les documents recuperes sont-ils pertinents pour la question ? Un mauvais retrieval cause des hallucinations en aval meme si le modele est fidele au contexte.
- **Groundedness Score** : Pourcentage des claims de la reponse qui sont directement supportees par les documents sources. Objectif : > 95% pour les systemes a haut risque.

**Pour les systemes generatifs purs :**

- **Self-consistency** : Generer N reponses pour le meme prompt et mesurer la coherence entre elles. Les reponses incoherentes indiquent une incertitude elevee et un risque d'hallucination.
- **Entropy-based detection** : Mesurer l'entropie de la distribution de tokens a chaque etape de generation. Une entropie elevee sur des facts specifiques (noms, dates, chiffres) indique un risque d'hallucination.
- **Claim verification** : Extraire les claims individuelles de la reponse et les verifier contre des sources externes (knowledge graphs, APIs factuelles, bases de donnees).

### Strategies de grounding (ancrage factuel)

**RAG (Retrieval-Augmented Generation) — Best practices :**

```
Principes pour un RAG robuste anti-hallucination :

1. Qualite du corpus
   - Curate et verifier les documents sources
   - Maintenir les documents a jour (versionning)
   - Supprimer les documents obsoletes ou incorrects
   - Detecter les contradictions internes dans le corpus

2. Qualite du retrieval
   - Utiliser le hybrid search (dense + sparse) pour maximiser le recall
   - Implementer le reranking (Cohere Rerank, cross-encoder)
   - Tester avec des requetes adversariales (negation, hors sujet)
   - Monitorer le recall@k et la precision@k en production

3. Qualite de la generation
   - Instruire le modele de citer ses sources [1][2][3]
   - Instruire le modele de dire "je ne sais pas" si aucun
     document pertinent n'est trouve
   - Limiter la generation aux informations presentes dans le contexte
   - Utiliser un temperature basse (0.0-0.3) pour les faits

4. Verification post-generation
   - NLI checker : chaque claim est-elle entaillee par une source ?
   - Citation verification : chaque citation pointe-t-elle vers
     un document reel du corpus ?
   - Fact extraction + external verification pour les chiffres critiques
```

**Tool-Augmented Verification :**

Pour les informations critiques (chiffres, dates, faits specifiques), permettre au modele d'appeler des outils de verification :

- Calculatrice pour les operations mathematiques
- API de faits (Wikidata, knowledge graphs) pour les informations factuelles
- Moteur de recherche pour les informations recentes
- Base de donnees interne pour les informations proprietaires

Chaque appel d'outil est loggue et auditable, fournissant une trace de verification transparente.

**Confidence Scoring :**

Implementer un systeme de scoring de confiance pour chaque reponse :

| Score | Signification | Action |
|-------|---------------|--------|
| 0.9-1.0 | Haute confiance, information verifiee par des sources multiples | Afficher directement |
| 0.7-0.9 | Confiance moderee, une source confirme | Afficher avec avertissement leger |
| 0.5-0.7 | Confiance faible, pas de source directe | Afficher avec disclaimer explicite |
| < 0.5 | Tres faible confiance, potentielle hallucination | Ne pas afficher, suggerer une reformulation |

### Outils de detection d'hallucinations (2024-2026)

| Outil | Approche | Integration |
|-------|----------|-------------|
| **RAGAS** | Framework d'evaluation RAG (faithfulness, relevancy) | Python, LangChain |
| **Galileo Hallucination Index** | Detection via analyse de representations internes | API, dashboard |
| **Trulens** | Evaluation modulaire de RAG pipelines | Python, LlamaIndex, LangChain |
| **Vectara HHEM** | Hallucination Evaluation Model (NLI-based) | API, open-source |
| **LangSmith** | Evaluation et tracing avec metriques custom | LangChain ecosystem |
| **DeepEval** | Framework de test unitaire pour LLMs | Python, CI/CD |
| **Quotient AI** | Eval platform avec hallucination detection | API cloud |

---

## Model Drift — Detection et remediation

### Types de drift

**Data Drift (Covariate Shift) :**

Changement dans la distribution des donnees d'entree par rapport aux donnees d'entrainement. Le modele recoit des inputs qu'il n'a jamais vus ou qui sont statistiquement differents de son entrainement.

- **Causes** : Changement de comportement utilisateur, saisonnalite, nouveau marche, evolution du langage, nouveaux sujets/terminologie.
- **Detection** : Monitorer la distribution des features d'entree (embeddings). Utiliser PSI (Population Stability Index), KL divergence, KS test, ou MMD (Maximum Mean Discrepancy) pour detecter les shifts.
- **Seuils recommandes (PSI)** :
  - PSI < 0.1 : Pas de drift significatif
  - 0.1 < PSI < 0.25 : Drift modere, investigation necessaire
  - PSI > 0.25 : Drift severe, action corrective requise

**Concept Drift :**

Changement dans la relation entre les inputs et les outputs attendus. Le monde change, meme si les donnees d'entree sont similaires.

- **Causes** : Changement de reglementation, evolution du marche, changement de preferences utilisateur, evenements majeurs.
- **Types** : Sudden drift (changement brutal), gradual drift (evolution progressive), recurring drift (saisonnier), incremental drift (accumulation lente).
- **Detection** : Monitorer les metriques de performance (accuracy, F1, user satisfaction) dans le temps. Detecter les points de rupture via des tests de changement (CUSUM, Page-Hinkley).

**Performance Decay :**

Degradation progressive des performances sans drift explicitement identifiable. Peut resulter d'une combinaison de facteurs :

- Accumulation de micro-drifts non detectes individuellement
- Degradation des donnees sources (RAG corpus obsolete)
- Evolution du modele provider (changements non annonces dans les API)
- Usure des guardrails (les attaquants s'adaptent)

### Monitoring du drift en production

**Architecture recommandee :**

```
[Production Inputs]
       |
       v
[Feature Extraction / Embedding]
       |
       v
[Drift Detector]  -----> [Alert si PSI > seuil]
       |
       v
[Reference Distribution Store]
       |
       v
[Dashboard : drift score temporal, par feature, par segment]
```

**Frequence de monitoring :**

| Type de systeme | Frequence de check | Fenetre d'analyse |
|-----------------|-------------------|-------------------|
| Systeme critique (medical, finance) | Chaque batch (horaire) | 24h glissantes |
| Systeme client-facing | Quotidien | 7 jours glissants |
| Systeme interne | Hebdomadaire | 30 jours glissants |
| Systeme experimental | Mensuel | 90 jours glissants |

### Remediation du drift

| Niveau de drift | Actions |
|-----------------|---------|
| Negligeable (PSI < 0.1) | Logging, aucune action |
| Modere (0.1-0.25) | Investigation des causes, monitoring renforce, potentiel re-tuning |
| Severe (PSI > 0.25) | Re-evaluation complete, re-entrainement/re-tuning, potentiel rollback |

**Strategies de remediation :**

- **Re-tuning / Fine-tuning incrementiel** : Adapter le modele aux nouvelles donnees sans re-entrainement complet. Efficace pour les drifts graduels.
- **RAG corpus refresh** : Mettre a jour le corpus de documents sources pour refleter les informations actuelles. Premiere action pour les systemes RAG.
- **Prompt engineering adaptation** : Adapter les prompts aux nouveaux patterns de requetes. Rapide et sans cout d'entrainement.
- **Modele replacement** : Migrer vers une version plus recente du modele (ex: GPT-4 vers GPT-4o). Tester exhaustivement avant migration.
- **Rollback** : Revenir a une version precedente du modele/prompt si la regression est severe. Necessiter un systeme de versioning rigoureux.

---

## Vendor Lock-in & Multi-Provider Strategy

### Evaluation de la dependance fournisseur

| Dimension | Questions a poser | Risque si eleve |
|-----------|-------------------|-----------------|
| **Technique** | Le modele est-il remplacable ? Les APIs sont-elles standards ? | Migration couteuse |
| **Donnees** | Les embeddings sont-ils portables ? Les fine-tunes sont-ils replicables ? | Perte de personnalisation |
| **Contractuel** | Quelles clauses de sortie ? Quel preavis ? | Piege contractuel |
| **Financier** | Quel % du budget IA chez un seul provider ? | Levier de negociation nul |
| **Competences** | L'equipe maitrise-t-elle des alternatives ? | Incapacite de migrer |

### Architecture multi-provider

```
[Application Layer]
        |
        v
[LLM Abstraction Layer]  (LiteLLM, Portkey, OpenRouter, custom)
        |
   +----+----+----+
   |         |         |
   v         v         v
[Provider A] [Provider B] [Provider C]
(primaire)   (fallback)   (specialise)
```

**Couche d'abstraction recommandee :**

| Outil | Type | Capacites | Avantage |
|-------|------|-----------|----------|
| **LiteLLM** | Librairie Python | Interface unifiee pour 100+ providers | Simple, open-source |
| **Portkey** | Gateway | Routing, fallback, caching, load balancing | Enterprise features |
| **OpenRouter** | API unifiee | Acces a 200+ modeles via une API | Simplicite d'acces |
| **Custom gateway** | Interne | Controle total, logique metier specifique | Flexibilite maximale |

**Strategie de fallback recommandee :**

1. Provider primaire (ex: OpenAI GPT-4o) — utilise pour 90% des requetes
2. Provider secondaire (ex: Anthropic Claude) — fallback si primaire indisponible
3. Provider tertiaire / self-hosted (ex: Llama 3 on-premise) — fallback de derniere instance
4. Reponses pre-calculees / templates — mode degrade sans LLM

Tester les fallbacks regulierement (chaos engineering). Un fallback jamais teste ne fonctionne pas quand on en a besoin.

### Portabilite des artefacts

| Artefact | Portabilite | Strategie |
|----------|-------------|-----------|
| **Prompts** | Elevee mais adaptation necessaire | Maintenir des prompts modulaires, tester sur chaque provider |
| **Fine-tunes** | Faible (specifique au provider) | Conserver les datasets de fine-tuning, re-entrainer si migration |
| **Embeddings** | Nulle (non portables entre modeles) | Re-indexer le corpus avec le nouveau modele d'embedding |
| **RAG corpus** | Elevee (documents sources) | Conserver les documents sources bruts separement des embeddings |
| **Evaluation datasets** | Elevee | Independants du provider, reutilisables |
| **Guardrails config** | Moyenne | Adapter les seuils et les classifiers au nouveau modele |

---

## Cost Management

### Structure des couts IA

| Poste de cout | Ordre de grandeur (2025) | Optimisable |
|---------------|--------------------------|-------------|
| **Inference API (tokens)** | $0.50-60 / 1M tokens (input, selon modele) | Oui (caching, routing, modele sizing) |
| **Embeddings** | $0.02-0.13 / 1M tokens | Oui (caching, modeles locaux) |
| **Fine-tuning** | $3-25 / 1M training tokens | Moyennement (optimiser le dataset) |
| **Infrastructure RAG** | $100-10K/mois (vector DB, compute) | Oui (sizing, tiering) |
| **Monitoring & Eval** | 10-20% du cout d'inference | Necessaire, ne pas reduire |
| **Human review** | $15-50/heure | Reduire le volume, pas le taux |

### Strategies d'optimisation des couts

**1. Semantic Caching :**
Mettre en cache les reponses pour les requetes semantiquement similaires. Utiliser des embeddings pour detecter les requetes proches (cosine similarity > 0.95). Taux de cache hit typique : 20-40% pour les FAQ, 5-10% pour les requetes ouvertes.

**2. Intelligent Model Routing :**
Router les requetes vers le modele le moins couteux capable de les traiter correctement :

```
Requete simple (FAQ, reformulation, classification)
  -> Modele petit et rapide (GPT-4o-mini, Claude Haiku, Gemini Flash)
  -> Cout : $0.15-0.75 / 1M tokens

Requete complexe (raisonnement, analyse, generation longue)
  -> Modele large (GPT-4o, Claude Sonnet, Gemini Pro)
  -> Cout : $2.50-10 / 1M tokens

Requete critique (decision, expertise, audit)
  -> Modele frontier (GPT-4o, Claude Opus, Gemini Ultra)
  -> Cout : $10-60 / 1M tokens
```

Implementer un classifier de complexite pour router automatiquement. Le cout du classifier est negligeable par rapport aux economies realisees.

**3. Token Budgeting :**
- Definir un budget tokens par utilisateur/equipe/feature/jour
- Alerter a 80% du budget, bloquer a 100%
- Revue mensuelle des budgets avec les stakeholders
- Mecanismes d'exception documentes pour les depassements justifies

**4. Prompt Optimization :**
- Reduire la taille des system prompts (chaque token coute a chaque requete)
- Utiliser des instructions concises et structurees
- Implementer le prompt compression pour les contextes longs
- Tronquer intelligemment les contexts RAG (ne garder que les chunks les plus pertinents)

---

## Latency Optimization

### Sources de latence dans un pipeline LLM

| Composant | Latence typique | Optimisation |
|-----------|----------------|-------------|
| Network (API call) | 50-200ms | Edge deployment, region selection |
| Retrieval (RAG) | 50-500ms | Vector DB tuning, caching, pre-computation |
| Reranking | 50-200ms | Modeles legers, batching, caching |
| LLM inference (TTFT) | 200ms-5s | Modele sizing, streaming, prompt caching |
| LLM inference (generation) | 1-30s | Max tokens limit, modele sizing |
| Output filtering | 50-200ms | Filtres legers, parallelisation |
| **Total pipeline** | **1-35s** | **Objectif : P95 < 5s pour les interactions temps reel** |

### Techniques d'optimisation

- **Streaming** : Activer le streaming SSE (Server-Sent Events) pour afficher les tokens au fur et a mesure de leur generation. Reduit le time-to-first-byte (TTFB) de 1-5s a ~200ms.
- **Prompt Caching** : Utiliser les fonctionnalites de prompt caching des providers (Anthropic prompt caching, OpenAI cached inputs) pour reduire la latence et le cout des system prompts longs repetes.
- **Speculative Decoding** : Pour les modeles self-hosted, utiliser un petit modele pour generer des brouillons valides par le grand modele. Acceleration de 2-3x sans degradation de qualite.
- **Parallelisation** : Executer le retrieval, le reranking, et les appels de verification en parallele quand possible. Ne pas serialiser les etapes independantes.
- **Pre-computation** : Pre-calculer les embeddings, pre-charger les contextes frequents, pre-generer les reponses pour les requetes les plus courantes.

---

## Availability & Redundancy

### Cibles de disponibilite pour les systemes IA

| Criticite du systeme | SLO cible | Downtime max/mois | Architecture |
|---------------------|-----------|-------------------|-------------|
| Critique (sante, finance) | 99.9% | 43 minutes | Multi-provider, multi-region, failover automatique |
| Eleve (client-facing) | 99.5% | 3.6 heures | Multi-provider, failover automatique |
| Modere (interne) | 99% | 7.2 heures | Provider unique + fallback degrade |
| Faible (experimental) | 95% | 36 heures | Provider unique, pas de SLO strict |

### Patterns de haute disponibilite

**Active-Passive Failover :**
- Provider primaire gere 100% du trafic
- Provider secondaire active si primaire indisponible
- Bascule automatique basee sur health checks (latence, error rate)
- Re-bascule manuelle apres verification

**Active-Active Load Balancing :**
- Plusieurs providers gerent le trafic simultanement
- Routing base sur la latence, le cout, ou la specialisation
- Pas de bascule necessaire (resilience intrinseque)
- Plus complexe a operer (coherence des comportements entre providers)

**Health Check recommande :**

```
Verifier toutes les 30 secondes :
  1. Le provider repond-il ? (connectivity check)
  2. La latence est-elle acceptable ? (< seuil P95)
  3. La qualite des reponses est-elle maintenue ? (canary requests)
  4. Le rate limit est-il atteint ? (capacity check)

Si 2 checks consecutifs echouent : declarer le provider unhealthy
Si le provider est unhealthy : basculer vers le fallback
Si 5 checks consecutifs reussissent apres recovery : declarer healthy
```

---

## AI Incident Databases (AIAAIC & autres)

### Bases de donnees d'incidents IA a suivre

| Base de donnees | Couverture | Acces | Usage |
|-----------------|-----------|-------|-------|
| **AIAAIC Repository** | Incidents et controverses IA mondiales | Public, gratuit | Veille, formation, risk assessment |
| **AI Incident Database (AIID)** | Incidents IA documentes par la communaute | Public, gratuit | Analyse de tendances, case studies |
| **OECD AI Incidents Monitor** | Incidents IA dans les pays OCDE | Public, gratuit | Politique publique, compliance |
| **MITRE ATLAS Case Studies** | Incidents adversariaux documentes techniquement | Public, gratuit | Red teaming, threat modeling |
| **AI Vulnerability Database (AVID)** | Vulnerabilites techniques des systemes IA | Public, gratuit | Security assessment |

### Top incidents IA a etudier (2023-2025)

Etudier ces incidents comme des case studies pour anticiper les risques :

1. **ChatGPT data leakage (mars 2023)** : Bug exposant les titres de conversations d'autres utilisateurs. Impact : perte de confiance, investigation regulatoire.
2. **Bing Chat persona break (fevrier 2023)** : Le chatbot Sydney exprime des sentiments, menace des utilisateurs. Impact : reaction mediatique massive, restriction des fonctionnalites.
3. **Air Canada chatbot refund (2024)** : Un chatbot promet un remboursement non conforme a la politique. Le tribunal oblige la compagnie a honorer la promesse du chatbot. Impact : precedent juridique sur la responsabilite des outputs IA.
4. **DPD chatbot insults (janvier 2024)** : Le chatbot du service client insulte l'entreprise et jure apres un jailbreak. Impact : embarras public, retrait temporaire du service.
5. **Google Gemini image bias (fevrier 2024)** : Generation d'images historiquement incorrectes (soldats nazis noirs, papes feminins). Impact : suspension du service, debat public sur le biais inverse.
6. **Deepfake financial fraud (Hong Kong, 2024)** : Un employe transfere 25M$ apres un appel video avec des deepfakes de ses collegues. Impact : perte financiere majeure, prise de conscience des risques deepfake.

### Lecons transversales des incidents

- Les incidents IA sont quasi toujours amplifies par la viralite des reseaux sociaux. Un output problematique isole peut devenir un incident reputationnel majeur en quelques heures.
- Les incidents les plus graves ne sont pas techniques mais reputationnels. La perception compte autant que la realite.
- Les chatbots client-facing sont la surface d'attaque la plus exposee. Prioriser les defenses sur ces systemes.
- La jurisprudence se forme en temps reel. Les outputs des chatbots engagent legalement l'organisation.
- Les incidents de bias sont politiquement charges et ne peuvent pas etre resolus uniquement par des solutions techniques.

---

## Deepfake Risks & Countermeasures

### Taxonomie des risques deepfake

| Type | Technologie | Risque principal | Prevalence (2025) |
|------|------------|-----------------|-------------------|
| **Face swap video** | GAN, diffusion models | Fraude, impersonation, desinformation | Tres elevee |
| **Voice cloning** | TTS neural (ElevenLabs, etc.) | Fraude telephonique, social engineering | Tres elevee |
| **Text generation** | LLMs | Desinformation, impersonation ecrite | Omni-presente |
| **Image generation** | Diffusion (DALL-E, Midjourney, Stable Diffusion) | Fausses preuves, manipulation | Tres elevee |
| **Full video generation** | Sora, Kling, Gen-3 | Desinformation video, faux evenements | Elevee (croissante) |

### Detection de deepfakes (2024-2026)

**Approches techniques :**

- **Artifact detection** : Detecter les artefacts visuels (inconsistances dans les reflexions oculaires, anomalies faciales, artifacts de bord). Efficacite en baisse a mesure que la qualite des deepfakes augmente.
- **Frequency analysis** : Analyser le spectre frequentiel des images/videos pour detecter des signatures de generation. Les GANs et les diffusion models laissent des traces spectrales detectables.
- **Provenance verification (C2PA)** : Standard de provenance de contenu (Coalition for Content Provenance and Authenticity). Signe cryptographiquement le contenu a la source (camera, logiciel) pour certifier son authenticite. Approche la plus prometteuse a long terme.
- **Watermarking** : Insertion de watermarks invisibles dans le contenu genere (Google SynthID, Meta AI watermarking). Permet d'identifier le contenu genere par IA meme apres modifications. Resistances aux transformations variable.

**Limites de la detection :**
- Course aux armements permanente : chaque amelioration de detection est contree par une amelioration de la generation
- Les deepfakes de haute qualite deviennent indistinguables pour les detecteurs automatiques classiques
- La detection fonctionne mieux sur les deepfakes "dans la nature" (basse qualite) que sur les deepfakes cibles (haute qualite)
- La solution long-terme est la provenance (C2PA), pas la detection post-hoc

### Mitigations organisationnelles

- **Verification multi-canal** : Pour les decisions critiques (transferts financiers, instructions sensibles), exiger une verification via un canal separe (callback telephonique, confirmation en personne, code OTP).
- **Protocoles d'authentification renforces** : Ne jamais se fier uniquement a la voix ou a la video pour authentifier une personne. Exiger des codes, des questions de securite, ou des elements impossibles a deepfaker en temps reel.
- **Formation des employes** : Sensibiliser aux risques de deepfakes avec des exercices pratiques. Montrer des exemples de deepfakes reussis pour calibrer la vigilance.
- **Politique de verification des sources** : Toute information provenant d'une source non verifiee (video, audio, texte) doit etre corroboree par des sources independantes avant action.
- **Adoption de C2PA** : Deployer les standards C2PA pour signer le contenu produit par l'organisation. Encourager les partenaires et fournisseurs a faire de meme. Participer a l'ecosysteme de provenance de contenu.
