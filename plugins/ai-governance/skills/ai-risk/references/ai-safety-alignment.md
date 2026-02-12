# AI Safety & Alignment

Reference complete pour la surete et l'alignement des systemes IA : fondamentaux de la safety, Constitutional AI, RLHF/DPO/RLAIF, filtrage et moderation de contenu, prevention des outputs nocifs, reponse aux incidents, kill switches et degradation gracieuse (2024-2026). Couvre le paysage de la recherche en alignement et les approches pratiques pour les systemes en production.

---

## Fondamentaux de la safety IA

### Definitions et distinctions

- **AI Safety** : Discipline visant a s'assurer que les systemes IA se comportent de maniere sure, fiable et benefique. Couvre la prevention des dommages, la robustesse, et le comportement previsible.
- **AI Alignment** : Sous-domaine de la safety visant a s'assurer que les objectifs et le comportement du systeme IA sont alignes avec les intentions et les valeurs humaines. Le modele fait ce que l'on veut qu'il fasse, pas seulement ce qu'on lui a demande litteralement.
- **AI Control** : Capacite a superviser, corriger, et arreter un systeme IA a tout moment. Complementaire a l'alignement : meme un systeme aligne doit etre controlable.

### Le probleme de l'alignement — enjeux fondamentaux

**Specification des objectifs (Outer Alignment) :**
Le defi de specifier correctement ce que l'on veut que le systeme fasse. Les objectifs mal specifies produisent des comportements non desires via le reward hacking (le systeme optimise la metrique sans atteindre l'objectif reel). Exemple classique : un chatbot optimisant la satisfaction utilisateur qui apprend a flatter plutot qu'a donner des reponses utiles.

**Generalisation des objectifs (Inner Alignment) :**
Meme si l'objectif est correctement specifie (outer alignment), le modele peut developper des objectifs internes (mesa-objectives) qui divergent de l'objectif d'entrainement quand le contexte change. Sujet de recherche actif et debattu.

**Scalable oversight :**
Comment superviser un systeme IA dont les capacites depassent celles des superviseurs humains dans certains domaines ? Les approches incluent le debate (deux AIs qui argumentent devant un juge humain), le recursive reward modeling, et les AI-assisted evaluations.

### Principes de safety engineering pour l'IA

1. **Transparency** : Le systeme doit pouvoir expliquer ses decisions et son raisonnement. Implementer le chain-of-thought visible, les citations de sources, et les indicateurs de confiance.
2. **Predictability** : Le comportement du systeme doit etre previsible et coherent. Minimiser les variations de comportement en fonction de la formulation de la requete (sensitivity robustness).
3. **Controllability** : L'operateur humain doit pouvoir superviser, corriger, et arreter le systeme a tout moment. Implementer des kill switches, des limitations de scope, et des mecanismes d'escalade.
4. **Corrigibility** : Le systeme doit accepter les corrections et les modifications de ses objectifs sans resistance. Un systeme qui optimise contre sa propre correction est un signe d'alignement defaillant.
5. **Robustness** : Le systeme doit se comporter correctement meme dans des conditions adversariales, hors distribution, ou avec des inputs inattendus.

---

## Techniques d'alignement — Etat de l'art (2024-2026)

### RLHF (Reinforcement Learning from Human Feedback)

**Processus :**

1. **Supervised Fine-Tuning (SFT)** : Entrainer le modele sur des paires instruction-reponse de haute qualite, curees par des humains. Etablit un comportement de base "assistant utile".
2. **Reward Model Training** : Entrainer un modele de recompense sur des paires de reponses classees par des annotateurs humains. Ce modele apprend a predire les preferences humaines.
3. **PPO Optimization** : Optimiser le modele de langage via Proximal Policy Optimization pour maximiser le score du reward model, avec une penalite KL pour eviter de s'eloigner trop du modele SFT.

**Forces :**
- Methode prouvee a grande echelle (GPT-4, Claude, Gemini)
- Permet de capturer des preferences complexes difficiles a specifier par des regles
- Ameliore significativement la surete et l'utilite par rapport au SFT seul

**Limites :**
- Couteux en annotation humaine (des milliers de comparaisons necessaires)
- Le reward model peut etre "hacke" par le policy model (reward hacking)
- Biais des annotateurs transmis au modele
- Instabilite de l'entrainement PPO (hyperparametres sensibles)
- Les preferences humaines ne sont pas toujours coherentes ou bien calibrees

### DPO (Direct Preference Optimization)

**Principe** : Eliminer le reward model intermediaire en optimisant directement la policy a partir des paires de preferences. Le loss DPO derive analytiquement la solution optimale du probleme RLHF constrained, rendant l'entrainement plus stable et plus simple.

**Formule conceptuelle :**

```
L_DPO = -E[log(sigma(beta * (log(pi(y_w|x)/pi_ref(y_w|x))
                             - log(pi(y_l|x)/pi_ref(y_l|x)))))]

Ou :
  y_w = reponse preferee (winner)
  y_l = reponse rejetee (loser)
  pi  = policy model
  pi_ref = reference model (SFT)
  beta = temperature parameter
```

**Avantages par rapport au RLHF :**
- Pas de reward model a entrainer et maintenir
- Entrainement plus stable (pas de PPO)
- Moins de hyperparametres a tuner
- Plus simple a implementer et a reproduire
- Performances comparables ou superieures au RLHF dans de nombreux benchmarks

**Variantes modernes :**
- **IPO (Identity Preference Optimization)** : Regularisation alternative evitant le overfitting aux preferences
- **KTO (Kahneman-Tversky Optimization)** : Basee sur la theorie des perspectives, utilise des signaux binaires (bon/mauvais) plutot que des paires
- **ORPO (Odds Ratio Preference Optimization)** : Combine SFT et preference alignment en une seule etape
- **SimPO (Simple Preference Optimization)** : Simplification de DPO eliminant le modele de reference

### RLAIF (Reinforcement Learning from AI Feedback)

**Principe** : Remplacer les annotateurs humains par un modele IA "juge" pour generer les labels de preference. Permet un scaling massif de l'annotation a faible cout.

**Processus :**

1. Generer des paires de reponses pour un ensemble de prompts
2. Utiliser un modele IA (souvent plus grand ou specialise) pour evaluer et classer les paires
3. Entrainer le modele cible avec DPO ou RLHF sur ces preferences generees par IA

**Avantages :**
- Scalabilite quasi illimitee (pas de goulot d'etranglement humain)
- Coherence des evaluations (pas de fatigue, de biais d'annotateur)
- Cout reduit de 10-100x par rapport a l'annotation humaine
- Iteration rapide (feedback en minutes, pas en jours/semaines)

**Risques :**
- Amplification des biais du modele juge
- Risque de model collapse si le modele s'entraine sur ses propres preferences
- Manque de jugement nuance sur des cas limites subtils
- Les modeles IA peuvent systematiquement preferer des reponses longues, formelles, ou "safe" au detriment de l'utilite

### Constitutional AI (Anthropic)

**Principe** : Doter le modele d'un ensemble de principes ("constitution") qui guident son comportement. Combiner le RLAIF avec des regles explicites pour reduire le besoin d'annotation humaine tout en maintenant un haut niveau de safety.

**Processus :**

1. **Critique** : Le modele genere une reponse, puis evalue sa propre reponse a la lumiere des principes constitutionnels
2. **Revision** : Le modele revise sa reponse pour mieux respecter les principes
3. **RLAIF** : Les paires (reponse originale, reponse revisee) sont utilisees pour entrainer un preference model

**Principes constitutionnels (exemples) :**
- "Choose the response that is least likely to be harmful or toxic"
- "Choose the response that is most helpful while being honest"
- "Choose the response that most respects the autonomy of the user"
- "If the response contains claims, choose the one that is most accurate and well-supported"

**Avantages :**
- Transparence : les principes sont explicites et auditables
- Scalabilite : le processus est largement automatisable
- Flexibilite : les principes sont modifiables sans re-entrainement complet
- Reduction du RLHF humain : la majorite de l'alignement est fait par RLAIF

---

## Content Filtering & Moderation

### Architecture de moderation multi-couches

```
[User Input]
     |
     v
[Pre-filter: Input Classifier]  ---> [Block + Log] si toxique/injection
     |
     v
[LLM Generation]
     |
     v
[Post-filter: Output Classifier] ---> [Block + Rephrase] si toxique
     |
     v
[PII Scanner] ---> [Redact] si PII detecte
     |
     v
[Domain Compliance Check] ---> [Block + Escalade] si hors scope
     |
     v
[User Output]
```

### Outils de moderation (2024-2026)

| Outil | Type | Capacites | Latence | Cout |
|-------|------|-----------|---------|------|
| **Llama Guard 3** (Meta) | Modele open-source | Classification de safety multi-categorie, customisable | ~100ms | Gratuit (self-hosted) |
| **OpenAI Moderation API** | API cloud | Classification toxicite/violence/sexual/hate | ~50ms | Gratuit |
| **Perspective API** (Google/Jigsaw) | API cloud | Toxicite, insulte, menace, profanite | ~100ms | Gratuit (quota) |
| **Azure AI Content Safety** | API cloud | Classification multi-categorie, severite graduee | ~100ms | Pay-per-use |
| **WildGuard** | Modele open-source | Detection toxicite + refus excessif | ~100ms | Gratuit (self-hosted) |
| **NeMo Guardrails** (NVIDIA) | Framework | Rails programmables, topical/safety/security | Variable | Open-source |
| **Guardrails AI** | Framework | Validators composables, output structure enforcement | Variable | Open-source + cloud |

### Categories de contenu a filtrer

| Categorie | Sous-categories | Severite de filtrage |
|-----------|----------------|---------------------|
| **Violence** | Instructions de violence, menaces, glorification | Strict (blocage systematique) |
| **Contenu sexuel** | Contenu explicite, exploitation, mineurs | Strict (blocage systematique) |
| **Discours haineux** | Discrimination, denigrement de groupes, slurs | Strict |
| **Auto-mutilation** | Suicide, automutilation, encouragement | Strict |
| **Substances illegales** | Fabrication, distribution, consommation | Eleve |
| **Armes** | Fabrication, modification, utilisation illegale | Eleve |
| **Fraude** | Techniques de fraude, phishing, manipulation | Eleve |
| **Vie privee** | Doxing, surveillance, tracking | Eleve |
| **Contenu trompeur** | Desinformation deliberee, impersonation | Modere-Eleve |
| **Contenu protege** | Reproduction substantielle de contenu sous copyright | Modere |

### Gestion du false refusal (sur-filtrage)

Le sur-filtrage est un probleme majeur : un systeme trop defensif refuse des requetes legitimes, degradant l'experience utilisateur et l'utilite du systeme.

**Strategies pour equilibrer safety et utilite :**

- Utiliser des classifiers a severite graduee (pas binaire safe/unsafe) avec des seuils configurables par use case
- Implementer un mecanisme de "soft refusal" : demander des clarifications plutot que bloquer
- Monitorer le taux de false refusal (FRR) comme metrique de qualite au meme titre que le taux de toxicite
- Utiliser XSTest ou des benchmarks similaires pour detecter les exaggerated safety behaviors
- Permettre des overrides manuels pour les utilisateurs verifies dans les contextes a faible risque

---

## Prevention des outputs nocifs

### Harmful Output Prevention Framework

**Niveau 1 — System Prompt Directives :**
Definir clairement dans le system prompt les categories de contenu interdit et le comportement attendu en cas de requete borderline. Les directives doivent etre specifiques (pas de "be helpful and harmless" generique) et priorisees.

**Niveau 2 — Output Classification :**
Classifier chaque output avant livraison. Utiliser un modele specialise (Llama Guard, WildGuard) plutot que le modele generatif lui-meme pour l'auto-evaluation (un modele jailbreake ne peut pas evaluer sa propre compromission).

**Niveau 3 — Structured Output Enforcement :**
Pour les cas a haut risque, forcer des outputs structures (JSON schema, enums, choix multiples) qui limitent mecaniquement la possibilite d'outputs nocifs. Un modele qui remplit un formulaire ne peut pas generer un paragraphe toxique.

**Niveau 4 — Human Review Pipeline :**
Pour les categories de contenu les plus sensibles, router les outputs borderline vers une file de review humaine. Utiliser le confidence score du classifier pour determiner quels outputs necessitent une revue. Objectif : moins de 1% du volume total route vers la revue humaine.

### Grounding et factualite

**Techniques de grounding (ancrage factuel) :**

- **RAG (Retrieval-Augmented Generation)** : Ancrer les reponses dans des documents sources verifies. Obliger le modele a citer ses sources. Verifier que les claims sont supportees par les documents recuperes (faithfulness).
- **Tool-augmented generation** : Permettre au modele d'appeler des outils (calculatrice, API de faits, bases de donnees) pour verifier les informations avant de les inclure dans la reponse.
- **Confidence calibration** : Entrainer ou configurer le modele pour exprimer son incertitude. "Je ne suis pas sur de cette information" est toujours preferable a une hallucination confiante.
- **Abstention** : Configurer le modele pour refuser de repondre quand il n'a pas d'information fiable, plutot que de generer une reponse potentiellement fausse. Preferer "Je ne sais pas" a une hallucination.

---

## Incident Response pour les systemes IA

### AI Incident Response Plan (AIRP)

Adapter le framework NIST Incident Response (SP 800-61) aux specificites des incidents IA :

**Phase 1 — Preparation :**

- Definir les types d'incidents IA : output nocif, data leakage, jailbreak reussi, biais decouvert, hallucination critique, comportement aberrant de l'agent
- Etablir les seuils de severite pour chaque type d'incident
- Designer les roles : AI Incident Commander, AI Security Analyst, Communications Lead
- Preparer les runbooks specifiques a chaque type d'incident
- Tester les procedures via des exercices de simulation (tabletop exercises)

**Phase 2 — Detection & Analyse :**

- Monitoring continu des metriques de risque (cf. risk-taxonomy.md)
- Canaux de signalement pour les utilisateurs et les equipes internes
- Triage automatique base sur la severite et le type d'incident
- Analyse de l'impact : nombre d'utilisateurs affectes, donnees exposees, decisions impactees
- Preservation des evidences : logs, captures d'ecran, inputs/outputs complets

**Phase 3 — Containment & Eradication :**

| Severite | Actions immediates | Timeline |
|----------|-------------------|----------|
| **Critique** | Kill switch global, notification direction, communication publique | < 15 minutes |
| **Elevee** | Desactivation feature flag, analyse root cause, communication interne | < 1 heure |
| **Moderee** | Renforcement filtres, monitoring accru, investigation | < 24 heures |
| **Faible** | Logging, investigation asynchrone, correctif planifie | < 1 semaine |

**Phase 4 — Recovery & Lessons Learned :**

- Restaurer le service avec les corrections appliquees
- Verifier que l'incident est completement resolu (re-testing)
- Conduire un blameless post-mortem dans les 48h suivant la resolution
- Mettre a jour le registre des risques et les defenses
- Partager les lessons learned avec l'equipe et la communaute (si appropriate)

### AI Incident Classification

```
Categorie 1 : Output nocif
  - Sous-categories : contenu violent, discriminatoire, illegal, trompeur
  - Severite : fonction de la diffusion (interne vs public)
  - Actions : blocage output, investigation prompt, renforcement filtres

Categorie 2 : Data leakage
  - Sous-categories : PII leakage, system prompt exposure, training data extraction
  - Severite : fonction du volume et de la sensibilite des donnees
  - Actions : kill switch, notification RGPD si applicable, audit complet

Categorie 3 : Jailbreak / Prompt injection reussi
  - Sous-categories : guardrail bypass, role hijacking, tool abuse
  - Severite : fonction des actions effectuees par le modele compromis
  - Actions : blocage utilisateur, analyse du vecteur, patch des defenses

Categorie 4 : Biais ou discrimination decouverts
  - Sous-categories : biais demographique, discrimination contextuelle
  - Severite : fonction de l'impact et de la visibilite
  - Actions : investigation, correctif, communication transparente

Categorie 5 : Hallucination critique
  - Sous-categories : information medicale fausse, conseil juridique errone, fait invente avec impact
  - Severite : fonction des consequences potentielles de l'hallucination
  - Actions : correction, ajout de disclaimers, renforcement du grounding
```

---

## Kill Switches & Graceful Degradation

### Architecture de kill switch multi-niveaux

```
Niveau 1 : Request-level kill switch
  - Timeout par requete (5-30s selon le use case)
  - Token limit par reponse
  - Declenchement : automatique

Niveau 2 : Session-level kill switch
  - Blocage d'un utilisateur specifique
  - Limite d'actions par session
  - Declenchement : automatique (anomaly detection) ou manuel

Niveau 3 : Feature-level kill switch
  - Feature flag pour desactiver une fonctionnalite IA specifique
  - Fallback vers un comportement non-IA
  - Declenchement : manuel (on-call engineer) en < 5 minutes

Niveau 4 : Model-level kill switch
  - Basculement vers un modele de secours (fallback model)
  - Desactivation d'un provider specifique
  - Declenchement : automatique (circuit breaker) ou manuel

Niveau 5 : System-level kill switch
  - Arret complet de tous les systemes IA
  - Basculement vers des processus manuels/humains
  - Declenchement : AI Incident Commander uniquement
```

**Exigences pour chaque kill switch :**
- Testable : Verifier regulierement que le kill switch fonctionne (chaos engineering)
- Rapide : Activation en moins de 5 minutes pour les niveaux 3+
- Independant : Le kill switch ne doit pas dependre du systeme qu'il arrete
- Documente : Procedure claire, accessible, et connue de l'equipe on-call
- Auditable : Chaque activation est loggee avec le motif, l'auteur, et le timestamp

### Graceful Degradation Patterns

**Pattern 1 — Model Fallback Chain :**

```
Requete utilisateur
  |
  v
[Model principal (ex: GPT-4o)] --> timeout/erreur/indispo
  |                                       |
  v                                       v
[Reponse]                    [Model secondaire (ex: Claude Haiku)]
                                          |
                                timeout/erreur/indispo
                                          |
                                          v
                             [Reponses pre-calculees / templates]
                                          |
                                    indisponible
                                          |
                                          v
                             [Message d'erreur informatif]
                             "Un agent humain va vous repondre."
```

**Pattern 2 — Capability Degradation :**

Reduire progressivement les capacites plutot que de couper completement :

1. Mode complet : generation libre + tool use + RAG
2. Mode restreint : RAG only (pas de generation libre)
3. Mode FAQ : reponses uniquement parmi un set pre-approuve
4. Mode maintenance : message informatif + redirection humaine

**Pattern 3 — Circuit Breaker :**

Implementer le pattern circuit breaker (Hystrix/Resilience4j) adapte aux LLMs :

- **Closed** : fonctionnement normal, compteur d'erreurs actif
- **Open** : trop d'erreurs, toutes les requetes sont rejetees ou redirigees vers le fallback. Timer de recuperation demarre.
- **Half-Open** : apres le timer, quelques requetes test sont envoyees. Si succes, retour en Closed. Si echec, retour en Open.

Seuils recommandes pour les LLMs :
- Ouverture du circuit : > 50% d'erreurs sur une fenetre de 1 minute
- Timer de recuperation : 30 secondes
- Requetes test en half-open : 5 requetes

---

## Paysage de la recherche en alignement (2024-2026)

### Axes de recherche principaux

| Axe | Description | Acteurs cles |
|-----|-------------|-------------|
| **Scalable Oversight** | Comment superviser des modeles plus capables que les humains | Anthropic, OpenAI, DeepMind |
| **Mechanistic Interpretability** | Comprendre les representations internes des modeles neuronaux | Anthropic (circuits), DeepMind, EleutherAI |
| **Debate & IDA** | Deux AIs debattent pour aider un juge humain | OpenAI, CHAI (UC Berkeley) |
| **Process Supervision** | Recompenser le processus de raisonnement, pas seulement le resultat | OpenAI (Let's Verify Step by Step) |
| **Constitutional AI** | Principes explicites guidant le comportement du modele | Anthropic |
| **Cooperative AI** | Systemes IA capables de cooperation multi-agents sure | DeepMind, CHAI |
| **Sleeper Agents** | Detection de comportements latents activables | Anthropic, Redwood Research |
| **Representation Engineering** | Controle du comportement via manipulation des representations internes | Center for AI Safety |
| **AI Control** | Garantir la securite meme si le modele est mal aligne | Redwood Research, ARC Evals |

### Problemes ouverts (2025-2026)

- **Deceptive alignment** : Un modele pourrait-il paraitre aligne pendant l'entrainement tout en poursuivant des objectifs differents en production ? La recherche sur les sleeper agents (Anthropic, 2024) suggere que les backdoors comportementaux sont difficiles a eliminer par fine-tuning standard.
- **Reward hacking a grande echelle** : Les modeles de plus en plus capables trouvent des failles dans les reward models. Les approches actuelles (KL penalty, reward model ensembles) sont des palliatifs. La recherche se concentre sur des reward models plus robustes et le process supervision.
- **Emergent capabilities & risks** : Les capacites emergentes des modeles (raisonnement, planification, deception potentielle) creent des risques imprevisibles. L'evaluation pre-deploiement (ARC Evals, UK AISI Inspect) vise a detecter ces capacites dangereuses avant mise en production.
- **Multi-agent safety** : La securite des systemes multi-agents (agents cooperatifs, hierarchiques, ou competitifs) est largement inexploree. Les risques incluent la collusion entre agents, les cascading failures, et l'emergence de comportements non prevus.
- **Evaluation of evaluations** : Comment savoir si nos evaluations de safety sont elles-memes fiables ? Les benchmarks actuels peuvent etre contamines, gammes, ou insuffisants. La meta-evaluation est un axe de recherche emergent.
