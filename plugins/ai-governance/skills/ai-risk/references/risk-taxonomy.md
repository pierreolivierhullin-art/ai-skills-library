# AI Risk Taxonomy & Assessment Frameworks

Reference complete pour la taxonomie des risques IA, le NIST AI Risk Management Framework, les cadres d'evaluation, les matrices de risque et les processus de monitoring continu (2024-2026). Couvre les six categories de risques IA, les methodologies d'evaluation quantitative et qualitative, et les processus d'acceptation du risque residuel.

---

## NIST AI Risk Management Framework (AI RMF 1.0) — Guide approfondi

Le NIST AI RMF, publie en janvier 2023 et enrichi par le NIST AI RMF Generative AI Profile (2024), constitue le cadre de reference mondial pour la gestion des risques lies a l'intelligence artificielle. Il est volontairement non prescriptif, adaptable a toute organisation et tout type de systeme IA. Structurer chaque programme de gestion des risques IA autour de ses quatre fonctions fondamentales.

### GOVERN — Gouvernance et culture du risque IA

La fonction GOVERN est transversale : elle irrigue et encadre les trois autres fonctions. Elle etablit les fondations organisationnelles de la gestion des risques IA.

**Activites essentielles :**

- **Definir les politiques de risque IA** : Rediger et publier une politique de risque IA couvrant les seuils d'acceptation, les processus d'escalade, et les roles/responsabilites. Cette politique doit etre approuvee par la direction generale et revisee annuellement.
- **Creer un AI Risk Board** : Constituer un comite pluridisciplinaire (legal, technique, metier, ethique, securite) charge de la gouvernance des risques IA. Ce comite se reunit mensuellement et dispose d'un pouvoir de decision (go/no-go) sur les deploiements a risque eleve.
- **Documenter l'appetit pour le risque** : Formaliser le niveau de risque que l'organisation est prete a accepter pour chaque categorie (technique, reputationnel, legal, etc.). Definir des seuils clairs : au-dela de quels niveaux un deploiement est interdit sans mitigation supplementaire.
- **Former les equipes** : Mettre en place un programme de formation obligatoire sur les risques IA pour tous les contributeurs (developpeurs, data scientists, product managers, equipes support). Actualiser la formation bi-annuellement.
- **Etablir la responsabilite** : Chaque systeme IA doit avoir un risk owner identifie (personne physique, pas une equipe). Ce risk owner est responsable du registre des risques, du suivi des mitigations, et de la communication avec le AI Risk Board.

**Metriques de maturite GOVERN :**

| Niveau | Description | Indicateurs |
|--------|-------------|-------------|
| Initial | Pas de politique formelle, gestion ad hoc | Aucun document, responsabilites floues |
| Defini | Politiques ecrites, roles identifies | Politique publiee, risk owners nommes |
| Gere | Processus actifs, comite operationnel | Comite mensuel, registre a jour |
| Optimise | Culture du risque integree, amelioration continue | Metriques en temps reel, formation continue |

### MAP — Identification et contextualisation des risques

La fonction MAP vise a identifier exhaustivement les risques et a comprendre le contexte dans lequel le systeme IA opere.

**Activites essentielles :**

- **Inventorier les systemes IA** : Maintenir un registre exhaustif de tous les systemes IA (en production, en developpement, en experimentation). Pour chaque systeme, documenter : objectif, donnees utilisees, modele sous-jacent, fournisseur, utilisateurs cibles, decisions impactees.
- **Identifier les parties prenantes** : Pour chaque systeme, cartographier les parties prenantes impactees : utilisateurs directs, sujets des decisions IA, operateurs, mainteneurs, regulateurs, public general. Evaluer l'impact differentiel sur les populations vulnerables.
- **Cataloguer les risques par categorie** : Utiliser la taxonomie a six categories (technique, securitaire, operationnel, reputationnel, legal, ethique) pour identifier systematiquement les risques. Conduire des ateliers de threat modeling adaptes a l'IA.
- **Documenter les scenarios de risque** : Pour chaque risque identifie, decrire le scenario concret : declencheur, mecanisme, impact, population affectee. Utiliser le format : "Si [evenement declencheur], alors [consequence] impactant [population] avec une severite [niveau]."
- **Evaluer le contexte d'utilisation** : Un meme modele presente des risques differents selon son contexte. Un chatbot interne de FAQ a faible risque ; le meme modele utilise pour du conseil medical a haut risque. Toujours evaluer le risque dans le contexte de deploiement reel.

**Threat Modeling adapte a l'IA (STRIDE-AI) :**

| Menace STRIDE | Adaptation IA | Exemples |
|---------------|---------------|----------|
| **Spoofing** | Usurpation d'identite via deepfakes, generation de faux profils | Deepfake audio pour fraude telephonique |
| **Tampering** | Data poisoning, manipulation des embeddings, corruption du RAG | Injection de donnees biaisees dans le corpus d'entrainement |
| **Repudiation** | Non-tracabilite des decisions IA, absence d'audit trail | Decision automatisee sans logging |
| **Information Disclosure** | Data leakage via outputs, extraction de donnees d'entrainement | Reconstruction de PII a partir des reponses du modele |
| **Denial of Service** | Model DoS via inputs complexes, epuisement de tokens/budget | Requetes crafted causant des generations infinies |
| **Elevation of Privilege** | Prompt injection pour contourner les restrictions, agent exploitation | Jailbreak donnant acces a des outils restreints |

### MEASURE — Evaluation et quantification des risques

La fonction MEASURE transforme les risques identifies en evaluations quantifiables et reproductibles.

**Metriques par categorie de risque :**

| Categorie | Metriques cles | Frequence de mesure |
|-----------|----------------|---------------------|
| Technique | Hallucination rate, accuracy, F1, BLEU/ROUGE, faithfulness score | Continue (chaque batch) |
| Securitaire | Attack success rate, injection detection rate, data leakage rate | Quotidien + red teaming mensuel |
| Operationnel | Latence P50/P95/P99, uptime, cout par requete, error rate | Temps reel |
| Reputationnel | Toxicity score, bias metrics, user complaint rate, NPS impact | Hebdomadaire |
| Legal | Compliance check pass rate, PII exposure incidents, audit findings | Mensuel + audits |
| Ethique | Fairness metrics (demographic parity, equalized odds), transparency score | Mensuel |

**Methodologie d'evaluation quantitative :**

1. **Baseline establishment** : Avant deploiement, etablir les metriques de reference sur un jeu de test representatif. Ce baseline sert de point de comparaison pour tout monitoring futur.
2. **Benchmark testing** : Utiliser des benchmarks standardises pertinents pour le type de systeme : TruthfulQA (hallucinations), BBQ (biais), HarmBench (safety), AdvBench (robustesse adversariale).
3. **Red teaming structure** : Conduire des sessions de red teaming avec des equipes internes et externes. Documenter chaque tentative (reussie ou non), le vecteur d'attaque, et la reponse du systeme. Viser un minimum de 500 tentatives diversifiees avant mise en production pour les systemes a haut risque.
4. **Scoring composite** : Calculer un AI Risk Score composite ponderant les metriques par categorie selon le contexte d'utilisation. Un systeme medical ponderera plus fortement les metriques de hallucination et de biais ; un systeme financier ponderera la securite et la conformite.

**Formule de Risk Score (exemple) :**

```
AI_Risk_Score = sum(weight_i * normalized_metric_i) pour i dans les categories

Exemple pour un chatbot client :
  Technical_Risk  (0.25) * hallucination_rate_normalized
+ Security_Risk   (0.20) * injection_success_rate_normalized
+ Operational_Risk(0.15) * (1 - availability) + cost_overrun_rate
+ Reputational_Risk(0.25) * toxicity_rate + bias_score
+ Legal_Risk      (0.10) * compliance_gap_score
+ Ethical_Risk    (0.05) * fairness_gap_score

Score final : 0 (risque minimal) a 1 (risque maximal)
Seuil de deploiement typique : < 0.3 pour low-risk, < 0.15 pour high-risk
```

### MANAGE — Traitement, monitoring et communication des risques

La fonction MANAGE couvre les actions concretes de traitement des risques et le cycle de vie complet de la gestion des risques.

**Strategies de traitement des risques :**

| Strategie | Description | Quand l'utiliser |
|-----------|-------------|-----------------|
| **Eviter** | Eliminer l'activite generant le risque | Risque critique sans mitigation viable |
| **Attenuer** | Reduire la probabilite ou l'impact | Risque eleve avec mitigations possibles |
| **Transferer** | Transmettre le risque (assurance, sous-traitance) | Risque financier quantifiable |
| **Accepter** | Accepter formellement le risque residuel | Risque faible, cout de mitigation disproportionne |

**Processus de monitoring continu :**

1. **Alertes automatisees** : Configurer des alertes sur les metriques critiques avec des seuils differencies (warning, critical, emergency). Chaque alerte doit declencher une procedure de reponse documentee.
2. **Dashboard de risque en temps reel** : Maintenir un dashboard centralise affichant le AI Risk Score de chaque systeme, les tendances, les incidents recents, et le statut des mitigations en cours. Outils recommandes : Grafana, Datadog, ou solutions LLMOps specialisees (LangSmith, Weights & Biases).
3. **Revue periodique** : Revue hebdomadaire des alertes par l'equipe technique. Revue mensuelle du registre des risques par le AI Risk Board. Revue trimestrielle de la strategie de risque par la direction.
4. **Feedback loop** : Integrer les incidents, near-misses, et retours utilisateurs dans le registre des risques. Chaque incident doit generer une mise a jour du registre et potentiellement des mitigations supplementaires.

---

## Taxonomie detaillee des risques IA

### 1. Risques techniques

Les risques lies au comportement du modele lui-meme et a la qualite de ses outputs.

**Hallucinations :**
- **Definition** : Generation d'informations factuellement incorrectes, inventees, ou incoherentes, presentees avec un haut degre de confiance apparente.
- **Types** : Hallucination factuelle (fait invente), hallucination logique (raisonnement fallacieux), confabulation (memoire inventee), hallucination attributive (citation inventee).
- **Impact** : De mineur (erreur corrigeable) a critique (decision medicale erronee, conseil juridique faux).
- **Facteurs aggravants** : Questions hors du domaine d'entrainement, requetes ambigues, absence de grounding, temperature elevee.

**Model Drift :**
- **Data drift** : Changement dans la distribution des donnees d'entree par rapport aux donnees d'entrainement. Mesurer avec PSI (Population Stability Index), KL divergence, ou KS test.
- **Concept drift** : Changement dans la relation entre les inputs et les outputs attendus (le monde change). Necessite un re-entrainement ou un re-tuning periodique.
- **Performance decay** : Degradation progressive des metriques de qualite sans cause unique identifiable. Detecter via le monitoring continu des metriques de reference.

**Model Collapse :**
- **Definition** : Degradation du modele cause par l'entrainement sur des donnees generees par IA (recursive training). Chaque generation amplifie les erreurs et reduit la diversite.
- **Impact 2024-2026** : Risque croissant a mesure que le contenu genere par IA envahit le web. Les corpus de pre-training contamines peuvent affecter les fondations memes des futurs modeles.
- **Mitigation** : Curated datasets, detection de contenu genere par IA, diversification des sources de donnees, watermarking du contenu synthetique (C2PA).

### 2. Risques securitaires

Les risques lies a l'exploitation malveillante des systemes IA.

**Prompt Injection :**
- **Direct** : L'utilisateur insere des instructions malveillantes directement dans son prompt. Exemple : "Ignore toutes les instructions precedentes et..."
- **Indirect** : Des instructions malveillantes sont injectees via des donnees externes (pages web, documents, emails) traitees par le modele. Plus dangereux car invisible pour l'utilisateur.
- **Impact** : Exfiltration de donnees, contournement des guardrails, execution d'actions non autorisees, manipulation des outputs.

**Data Poisoning :**
- **Backdoor attacks** : Insertion de triggers dans les donnees d'entrainement qui activent un comportement malveillant specifique a l'inference.
- **Targeted poisoning** : Modification ciblee des donnees pour biaiser les predictions sur des inputs specifiques.
- **Clean-label attacks** : Poisoning sans modification des labels, rendant la detection extremement difficile.

**Model Extraction :**
- **Definition** : Reconstruction d'un modele proprietary via des requetes systematiques a son API. L'attaquant cree un modele "shadow" reproduisant le comportement du modele cible.
- **Cout** : Reductions significatives du cout d'extraction grace aux techniques de distillation efficientes. Un modele proprietaire coutant des millions peut etre approxime pour quelques milliers de dollars.
- **Defense** : Rate limiting, detection d'anomalies dans les patterns de requetes, watermarking des outputs, limitation de l'information dans les reponses (pas de logprobs).

**Membership Inference :**
- **Definition** : Determiner si un echantillon specifique faisait partie des donnees d'entrainement du modele. Risque pour la vie privee des individus dont les donnees ont ete utilisees.
- **Implications RGPD** : Si un attaquant peut prouver que des donnees personnelles sont "memorisees" par le modele, cela constitue une violation potentielle du droit a la vie privee et du droit a l'oubli.

### 3. Risques operationnels

Les risques lies a l'exploitation quotidienne des systemes IA en production.

- **Vendor lock-in** : Dependance excessive a un fournisseur de modele (OpenAI, Anthropic, Google). Attenuer via des couches d'abstraction (LiteLLM), des strategies multi-fournisseur, et le maintien de competences sur les modeles open-source.
- **Couts incontroles** : Les couts d'inference LLM peuvent exploser avec le volume. Implementer des budgets par utilisateur/equipe/feature, du token budgeting, et des mecanismes de circuit breaker financier.
- **Latence** : Les LLMs ont une latence intrinseque elevee (1-30s selon la complexite). Optimiser via streaming, caching semantique, modeles plus petits pour les taches simples (routing intelligent), et edge deployment.
- **Disponibilite** : Les API de modeles sont sujettes a des pannes. Implementer des fallback multi-fournisseur, des mecanismes de retry avec exponential backoff, et des reponses degradees en cas d'indisponibilite.

### 4. Risques reputationnels

- **Outputs inappropries** : Generation de contenu offensant, discriminatoire, ou inapproprie pour le contexte. Un seul incident viral peut causer des dommages reputationnels disproportionnes.
- **Biais detectes** : Decouverte publique de biais systematiques dans les outputs (genre, race, age, religion). Amplification mediatique garantie.
- **Deepfakes** : Utilisation des capacites generatives pour creer du contenu trompeur impersonnant l'organisation ou ses representants. Inclut la generation de faux communiques, de fausses declarations, ou de faux produits.

### 5. Risques legaux et reglementaires

- **EU AI Act** : Classification des systemes IA par niveau de risque (inacceptable, haut, limite, minimal). Les systemes a haut risque necessitent une evaluation de conformite, une documentation technique, un systeme de gestion des risques, et un marquage CE.
- **RGPD/GDPR** : Les modeles IA traitant des donnees personnelles doivent respecter les principes de minimisation, de limitation de finalite, et de droits des personnes concernees (droit d'acces, droit a l'oubli — problematique pour les modeles entraines).
- **Responsabilite civile** : Qui est responsable quand un systeme IA cause un prejudice ? Le developpeur du modele, l'operateur, l'integrateur, l'utilisateur ? La jurisprudence est encore en formation (2024-2026).
- **Propriete intellectuelle** : Les outputs generes par IA sont-ils proteges par le droit d'auteur ? Les modeles entraines sur du contenu protege violent-ils les droits des auteurs ? Contentieux majeurs en cours (NYT v. OpenAI, Getty v. Stability AI).

### 6. Risques ethiques

- **Biais systematiques** : Les modeles reproduisent et amplifient les biais presents dans les donnees d'entrainement. Mesurer avec des metriques de fairness : demographic parity, equalized odds, predictive parity.
- **Perte d'autonomie humaine** : Delegation excessive de decisions a l'IA erosant le jugement humain et la capacite de decision independante. Risque particulierement eleve dans les contextes educatifs et medicaux.
- **Manque de transparence** : Incapacite d'expliquer les decisions prises par le systeme IA. Exacerbe par la nature "boite noire" des LLMs. Attenuer via l'explainability (XAI), le chain-of-thought, et la documentation des limitations.
- **Fracture numerique** : Les benefices de l'IA sont inegalement distribues. Les populations sans acces, sans competences numeriques, ou sous-representees dans les donnees d'entrainement sont systematiquement desavantagees.

---

## Frameworks d'evaluation des risques IA

### ISO/IEC 23894:2023 — Guidance on AI Risk Management

Standard international fournissant des lignes directrices pour la gestion des risques IA dans le cadre de l'ISO 31000. Integrer ses principes :

- Appliquer le processus de gestion des risques ISO 31000 (etablir le contexte, identifier, analyser, evaluer, traiter) aux specificites de l'IA
- Considerer les risques sur l'ensemble du cycle de vie IA (conception, developpement, deploiement, operation, retrait)
- Integrer les risques IA dans le systeme de gestion des risques global de l'organisation

### MITRE ATLAS (Adversarial Threat Landscape for AI Systems)

Framework de reference pour les menaces adversariales contre les systemes IA. Equivalent du MITRE ATT&CK pour l'IA :

- **Reconnaissance** : Identification des modeles cibles, de leurs capacites et de leurs limitations
- **Resource Development** : Preparation des datasets de poisoning, des prompts adversariaux, des modeles shadow
- **Initial Access** : Prompt injection, supply chain compromise, API exploitation
- **Execution** : Exploitation du modele pour executer des actions non autorisees
- **Persistence** : Backdoor dans les modeles fine-tunes, poisoning persistant
- **Exfiltration** : Extraction de donnees d'entrainement, model stealing, membership inference

Utiliser MITRE ATLAS pour structurer les evaluations de securite et les exercices de red teaming.

### EU AI Act — Classification des risques

Classifier chaque systeme IA selon les quatre niveaux de risque de l'EU AI Act :

| Niveau | Exemples | Obligations |
|--------|----------|-------------|
| **Inacceptable** | Scoring social, manipulation subliminale, identification biometrique temps reel (hors exceptions) | Interdit |
| **Haut risque** | Recrutement IA, scoring credit, diagnostic medical, justice | Evaluation de conformite, documentation technique, monitoring, marquage CE |
| **Risque limite** | Chatbots, deepfakes, systemes de recommandation | Obligations de transparence (informer l'utilisateur qu'il interagit avec une IA) |
| **Risque minimal** | Filtres photo, jeux video, correcteurs orthographiques | Pas d'obligation specifique (bonnes pratiques encouragees) |

---

## Registre des risques — Template operationnel

Maintenir un registre des risques vivant pour chaque systeme IA. Chaque entree contient :

```
Risk ID        : AI-RISK-[SYSTEM]-[NNN]
System         : Nom du systeme IA concerne
Category       : Technique | Securitaire | Operationnel | Reputationnel | Legal | Ethique
Description    : Description detaillee du scenario de risque
Probability    : Rare | Peu probable | Possible | Probable | Tres probable
Impact         : Negligeable | Mineur | Majeur | Critique | Catastrophique
Risk Level     : Score composite (Probabilite x Impact)
Risk Owner     : Nom et role du responsable
Mitigation     : Actions de mitigation implementees ou planifiees
Residual Risk  : Niveau de risque apres mitigation
Status         : Ouvert | En mitigation | Accepte | Ferme
Review Date    : Date de prochaine revue
Notes          : Historique des mises a jour, incidents lies
```

**Processus d'acceptation du risque residuel :**

1. Documenter le risque residuel apres application de toutes les mitigations realisables
2. Evaluer si le risque residuel est dans l'appetit pour le risque defini par l'organisation
3. Si oui : approbation formelle par le risk owner (risque faible) ou le AI Risk Board (risque modere)
4. Si non : escalade a la direction. Trois options : mitigation supplementaire, transfert du risque, arret du projet
5. Documenter la decision et ses justifications. Reviser systematiquement lors de chaque revue periodique
6. Aucun risque residuel de niveau critique ne peut etre accepte sans approbation du COMEX/C-level

---

## Monitoring des risques en production

### Architecture de monitoring recommandee

```
[Input Stream] --> [Input Validator] --> [PII Detector] --> [Model]
                                                              |
                                                    [Output Monitor]
                                                              |
                                    [Toxicity Check] [Hallucination Check] [Bias Check]
                                                              |
                                                    [Logging & Metrics]
                                                              |
                                            [Dashboard] [Alerts] [Audit Trail]
```

### Metriques operationnelles a monitorer

| Metrique | Seuil d'alerte (warning) | Seuil critique | Action |
|----------|--------------------------|----------------|--------|
| Hallucination rate | > 5% | > 15% | Investigation + rollback si > 15% |
| Toxicity rate | > 1% | > 5% | Renforcement filtres + investigation |
| Prompt injection blocked | > 2% des requetes | > 10% | Investigation attaque ciblee |
| P95 latency | > 5s | > 15s | Scaling + investigation |
| Error rate | > 2% | > 10% | Investigation + circuit breaker |
| Drift score (PSI) | > 0.1 | > 0.25 | Re-evaluation + potentiel re-training |
| Cost per request | > 1.5x baseline | > 3x baseline | Budget review + optimisation |
| User complaint rate | > 0.5% | > 2% | Review des outputs + action corrective |

### Outils de monitoring recommandes (2024-2026)

| Outil | Specialite | Integrations |
|-------|-----------|-------------|
| **LangSmith** (LangChain) | Tracing LLM, evaluation, monitoring | LangChain, LangGraph, APIs ouvertes |
| **Weights & Biases** | Experiment tracking, model monitoring | Tous frameworks ML |
| **Arize Phoenix** | Observabilite LLM, tracing, evaluation | OpenTelemetry, LlamaIndex |
| **Helicone** | Logging, caching, rate limiting LLM | OpenAI, Anthropic, tous providers |
| **WhyLabs / Langkit** | Data et model monitoring, drift detection | Python, APIs REST |
| **Galileo** | Hallucination detection, evaluation | RAG pipelines, tous LLMs |
| **Datadog LLM Observability** | Monitoring integre, APM | Ecosysteme Datadog complet |

Privilegier les outils avec support OpenTelemetry pour une integration unifiee dans l'observability stack existante. Ne pas creer un silo de monitoring separe pour l'IA — integrer dans la plateforme d'observabilite globale.
