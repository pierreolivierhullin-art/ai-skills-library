---
name: strategie-ia
description: This skill should be used when the user asks about "AI strategy", "AI maturity", "AI roadmap", "AI governance", "MLOps", "model lifecycle", "AI Center of Excellence", "AI literacy", "build vs buy AI", "AI use case prioritization", "stratégie IA", "maturité IA", "feuille de route IA", "gouvernance IA", "cycle de vie des modèles", "centre d'excellence IA", "acculturation IA", "culture IA", "AI adoption", "adoption de l'IA", "AI transformation", "transformation par l'IA", "AI ROI", "retour sur investissement IA", "AI talent", "compétences IA", "AI operating model", "modèle opérationnel IA", "AI ethics board", "comité éthique IA", "responsible AI governance", "AI portfolio", "AI budget", "make or buy IA", or needs guidance on enterprise AI strategy, model governance, and AI organization.
version: 1.1.0
last_updated: 2026-02
---

# Enterprise AI Strategy & Governance

## Overview

Ce skill couvre l'ensemble des disciplines liées a la strategie IA d'entreprise, de la definition de la vision a l'operationnalisation des modeles en production. Il fournit un cadre de decision structure pour concevoir, deployer et gouverner des initiatives IA a l'echelle, en integrant les dimensions strategiques (maturite, roadmap, ROI), organisationnelles (AI CoE, equipes, literacy), techniques (MLOps, model lifecycle, registre de modeles) et reglementaires (EU AI Act, NIST AI RMF, ISO 42001). Appliquer systematiquement les principes decrits ici pour guider chaque decision relative a l'IA en entreprise, en privilegiant la valeur metier, la gouvernance responsable et l'execution pragmatique. Ce skill integre les evolutions majeures 2024-2026 : strategies GenAI, gouvernance des LLM, agents IA autonomes et responsible scaling.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Definition d'une strategie IA** : evaluation de la maturite IA, construction d'une vision IA alignee sur la strategie d'entreprise, definition des ambitions et du positionnement IA.
- **Construction d'une roadmap IA** : priorisation des cas d'usage (quick wins vs moonshots), sequencement des initiatives, gestion du portefeuille IA.
- **Decisions build vs buy vs partner** : arbitrage entre developpement interne, achat de solutions SaaS IA, partenariats avec des fournisseurs specialises, utilisation d'API de foundation models.
- **Business case et ROI** : construction du business case IA, metriques de valeur, calcul du ROI, gestion des investissements IA.
- **Organisation IA** : mise en place d'un AI Center of Excellence (CoE), structuration des equipes IA, definition des roles (Data Scientist, ML Engineer, AI Engineer, AI PM), montee en competences.
- **AI literacy et culture** : programmes de sensibilisation, formation des metiers, AI champions networks, gestion du changement.
- **MLOps et cycle de vie des modeles** : design du pipeline MLOps, registre de modeles, validation, deploiement, monitoring (data drift, concept drift, performance decay), decommissionnement.
- **Gouvernance des modeles** : model registry, approbation, lineage, audit trail, gouvernance specifique aux LLM et modeles generatifs.
- **Conformite reglementaire IA** : EU AI Act (classification des risques, obligations), NIST AI RMF, ISO 42001, reglementations sectorielles.
- **Strategie GenAI et agents** : adoption des modeles generatifs, gouvernance des LLM, strategies d'agents IA, responsible scaling.

## Core Principles

### Principle 1 — Value-First AI

Partir systematiquement de la valeur metier, jamais de la technologie. Chaque initiative IA doit repondre a un probleme metier clairement identifie avec un impact mesurable. Refuser le "AI washing" : une initiative sans KPI metier clair n'est pas une initiative IA strategique. Evaluer chaque cas d'usage selon trois axes : faisabilite technique, valeur metier et risque. Prioriser les quick wins a fort impact et faible complexite pour construire la credibilite avant d'attaquer les projets transformationnels.

### Principle 2 — Governance by Design

Integrer la gouvernance des la conception, pas comme une couche ajoutee a posteriori. Chaque modele deploye en production doit avoir un owner identifie, un niveau de risque classe, un processus de validation documente et un plan de monitoring. Appliquer le principe de proportionnalite : le niveau de gouvernance doit etre proportionnel au risque du modele (un recommandeur de contenu ne necessite pas le meme niveau de gouvernance qu'un modele de scoring credit). Aligner la gouvernance IA sur les cadres reglementaires applicables (EU AI Act, NIST AI RMF, ISO 42001).

### Principle 3 — Industrialize, Don't Artisanize

Passer du mode artisanal (notebooks, modeles ad hoc, deploiements manuels) au mode industriel (pipelines automatises, CI/CD pour les modeles, monitoring continu). Le taux de modeles deployes en production qui generent effectivement de la valeur est la metrique cle. Un modele non deploye est un cout, pas un actif. Investir dans les fondations MLOps avant de multiplier les cas d'usage.

### Principle 4 — Federated Ownership with Central Standards

Centraliser les standards, les outils et les bonnes pratiques via un AI CoE ou une AI Platform team. Decentraliser l'execution et l'ownership des cas d'usage vers les equipes metier. Le CoE fournit les rails, les metiers conduisent les trains. Ce modele federe permet le passage a l'echelle sans creer de bottleneck organisationnel.

### Principle 5 — Responsible Scaling

Augmenter les capacites IA de maniere responsable. Chaque palier de scaling (du PoC a la production, de quelques modeles a des centaines) necessite un renforcement proportionnel de la gouvernance, du monitoring et des garde-fous. Les modeles generatifs et les agents IA autonomes requierent des mecanismes specifiques : guardrails, human-in-the-loop, evaluation continue, red teaming. Ne jamais sacrifier la gouvernance au profit de la vitesse de deploiement.

### Principle 6 — Continuous Learning Organization

L'IA transforme les metiers et les competences. Investir dans l'AI literacy a tous les niveaux : dirigeants (vision strategique), managers (identification des cas d'usage), experts metier (collaboration avec les equipes IA), equipes techniques (competences MLOps/LLMOps). La formation n'est pas un evenement ponctuel mais un programme continu aligne sur l'evolution de la maturite IA de l'organisation.

## Key Frameworks & Methods

### AI Maturity Model (5 niveaux)

| Niveau | Nom | Caracteristiques | Priorites |
|---|---|---|---|
| **1** | Exploring | Experimentation ad hoc, pas de strategie IA formalisee, competences dispersees | Sensibilisation, premiers PoC, identification des sponsors |
| **2** | Experimenting | Quelques PoC reussis, debut de structuration, premiers data scientists | Premiers deploiements en production, quick wins, constitution du CoE |
| **3** | Formalizing | Strategie IA formalisee, CoE operationnel, pipeline MLOps de base, quelques modeles en production | Scaling des cas d'usage, industrialisation MLOps, AI literacy |
| **4** | Optimizing | Portefeuille IA gere, MLOps mature, gouvernance etablie, culture IA diffusee | Optimisation du ROI, automatisation avancee, GenAI strategy |
| **5** | Transforming | IA comme avantage competitif structurel, innovation continue, agents autonomes | Innovation disruptive, AI-native products, responsible scaling |

### Use Case Prioritization Matrix

Evaluer chaque cas d'usage sur deux axes (scoring 1-5) :

```
        Valeur metier elevee
              |
   STRATEGIC  |  QUICK WINS
   (investir  |  (executer
    long      |   rapidement)
    terme)    |
--------------+---------------
   DEPRIORI-  |  EXPERIMENTS
   TISER      |  (tester et
   (eviter)   |   apprendre)
              |
        Faisabilite elevee
```

- **Quick Wins** (haute valeur, haute faisabilite) : executer en priorite, ROI rapide, construit la credibilite IA.
- **Strategic** (haute valeur, faisabilite moderee) : investir progressivement, necessite des fondations solides.
- **Experiments** (valeur moderee, haute faisabilite) : utile pour apprendre et monter en competences.
- **Deprioritiser** (faible valeur, faible faisabilite) : ne pas investir de ressources.

### Build vs Buy vs Partner Decision Framework

| Critere | Build | Buy (SaaS/API) | Partner |
|---|---|---|---|
| **Avantage competitif** | Fort (IP proprietaire) | Faible (commodite) | Moyen (co-innovation) |
| **Controle** | Total | Limite | Partage |
| **Time to market** | Long (6-18 mois) | Court (1-3 mois) | Moyen (3-9 mois) |
| **Cout initial** | Eleve | Faible | Moyen |
| **Cout recurrent** | Moyen (equipe) | Eleve (licences) | Variable |
| **Competences requises** | Elevees | Faibles | Moyennes |
| **Dependance vendor** | Nulle | Forte | Moderee |

Regle de decision : **Build** pour les capacites IA differenciantes (core domain), **Buy** pour les capacites commoditisees (generic domain), **Partner** pour l'acceleration sur les capacites strategiques mais non-core. Pour les LLM : privilegier les API de foundation models (OpenAI, Anthropic, Mistral) sauf si des contraintes de confidentialite ou de performance imposent un deploiement on-premise.

### ROI Framework pour l'IA

Calculer le ROI IA en integrant :
- **Benefices directs** : reduction de couts (automatisation), augmentation de revenus (personnalisation, conversion), gain de productivite.
- **Benefices indirects** : amelioration de la qualite, reduction des risques, acceleration des decisions.
- **Couts** : infrastructure (compute, storage), equipe (salaires, formation), outils (licences), donnees (acquisition, preparation, labelling), gouvernance et conformite.
- **Time-to-value** : delai entre l'investissement et la generation de valeur. Viser un premier retour mesurable en moins de 6 mois.

## Decision Guide

### Arbre de decision strategique IA

```
1. Quel est le niveau de maturite IA de l'organisation ?
   +-- Niveau 1-2 (Exploring/Experimenting)
   |   +-- Prioriser : AI literacy, premiers PoC, quick wins
   |   +-- Eviter : programmes IA ambitieux sans fondations
   +-- Niveau 3 (Formalizing)
   |   +-- Prioriser : industrialisation MLOps, scaling des cas d'usage, CoE
   |   +-- Eviter : multiplication des PoC sans deploiement
   +-- Niveau 4-5 (Optimizing/Transforming)
       +-- Prioriser : GenAI strategy, agents, AI-native products
       +-- Eviter : sur-centralisation, bureaucratie IA

2. Le cas d'usage est-il un avantage competitif ?
   +-- Oui (core domain) -> Build en interne
   +-- Non (generic domain) -> Buy ou Partner
   +-- Incertain -> Prototyper en Buy, migrer vers Build si strategique

3. Quel est le niveau de risque du modele (EU AI Act) ?
   +-- Risque inacceptable -> Interdit (ne pas developper)
   +-- Haut risque -> Gouvernance renforcee, conformite obligatoire
   +-- Risque limite -> Obligations de transparence
   +-- Risque minimal -> Gouvernance proportionnee

4. Le modele utilise-t-il des donnees personnelles ?
   +-- Oui -> RGPD/GDPR : base legale, PIA, minimisation, droits
   +-- Non -> Verifier les obligations contractuelles et sectorielles

5. S'agit-il d'un LLM/modele generatif ?
   +-- Oui -> Appliquer la gouvernance GenAI specifique
   |   +-- Guardrails, evaluation continue, red teaming
   |   +-- Politique d'usage, filtrage contenu, attribution
   +-- Non -> Pipeline MLOps classique
```

### Choix du modele d'organisation IA

| Critere | Centralise (CoE) | Hub & Spoke | Federe | Embedded |
|---|---|---|---|---|
| Maturite IA | Faible | Moyenne | Elevee | Tres elevee |
| Taille organisation | < 500 | 500-5000 | > 5000 | Variable |
| Coherence | Tres forte | Forte | Moderee | Variable |
| Agilite | Faible | Moyenne | Elevee | Tres elevee |
| Cout de coordination | Faible | Moyen | Eleve | Tres eleve |

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Start Small, Scale Fast** : debuter par 2-3 cas d'usage quick wins, deployer en production, demontrer la valeur, puis scaler. Ne pas lancer 20 PoC simultanes.
- **Data Flywheel** : concevoir les systemes IA pour que leur utilisation genere des donnees qui ameliorent le modele, creant un cercle vertueux (ex : feedback utilisateur comme signal d'entrainement).
- **AI Platform Team** : creer une equipe plateforme IA qui fournit les outils, pipelines et infrastructure partages, permettant aux equipes metier de se concentrer sur la valeur.
- **Model Tiering** : classifier les modeles par niveau de criticite (Tier 1 : business-critical, Tier 2 : important, Tier 3 : experimental) et appliquer une gouvernance proportionnee a chaque tier.
- **LLM Gateway Pattern** : centraliser les appels aux LLM via un gateway unifie qui gere le routage, le rate limiting, le caching semantique, l'observabilite et les guardrails.
- **Human-in-the-Loop by Default** : pour les modeles a haut impact, maintenir un humain dans la boucle de decision jusqu'a ce que la confiance dans le modele soit etablie par des metriques objectives.

### Anti-patterns critiques

- **PoC Graveyard** : accumuler les preuves de concept sans jamais deployer en production. Diagnostiquer via le ratio PoC-to-Production : il doit etre superieur a 30%.
- **Shadow AI** : equipes qui deployent des modeles IA sans gouvernance ni visibilite du CoE. Creer un registre de modeles obligatoire et des processus d'onboarding simples pour eviter le contournement.
- **AI Ivory Tower** : un CoE deconnecte des metiers qui produit des modeles techniquement brillants mais sans adoption. Le CoE doit etre au service des metiers, pas l'inverse.
- **One-Shot Training** : deployer un modele sans plan de re-entrainement ni monitoring de drift. Chaque modele en production doit avoir un pipeline de re-entrainement et des alertes de drift.
- **GenAI FOMO** : adopter les LLM et l'IA generative sans cas d'usage clair, uniquement par peur de manquer le train. Evaluer chaque usage GenAI avec la meme rigueur que tout autre projet IA.
- **Compliance Theater** : cocher des cases reglementaires sans implementer de controles effectifs. La conformite doit etre operationnelle, pas documentaire.

## Implementation Workflow

### Phase 1 — Assessment & Vision (Semaines 1-4)

1. Realiser une evaluation de maturite IA sur les 5 dimensions : strategie, donnees, technologie, organisation, gouvernance.
2. Cartographier les cas d'usage IA existants (y compris le Shadow AI) et leur etat (PoC, production, decommissionne).
3. Identifier les assets strategiques : donnees proprietaires, expertise metier unique, infrastructure existante.
4. Analyser le paysage concurrentiel IA dans le secteur.
5. Definir la vision IA et les ambitions a 3 ans, alignees sur la strategie d'entreprise.

### Phase 2 — Strategy & Roadmap (Semaines 5-10)

6. Prioriser les cas d'usage avec la matrice valeur/faisabilite (viser 3-5 quick wins et 2-3 projets strategiques).
7. Definir le modele d'organisation cible (CoE, hub & spoke, federe) en fonction de la maturite et de la taille.
8. Concevoir l'architecture de la plateforme IA cible (MLOps, data platform, model registry, LLM gateway).
9. Construire le business case consolide avec le ROI projete sur 3 ans.
10. Etablir la roadmap IA sequencee en vagues (Wave 1 : fondations + quick wins, Wave 2 : scaling, Wave 3 : transformation).

### Phase 3 — Foundations & Quick Wins (Mois 3-6)

11. Mettre en place le CoE ou l'equipe plateforme IA (3-5 personnes minimum).
12. Deployer l'infrastructure MLOps de base : model registry, pipeline CI/CD, monitoring.
13. Lancer le programme AI literacy (dirigeants, managers, metiers).
14. Executer les 2-3 premiers quick wins jusqu'au deploiement en production.
15. Etablir le cadre de gouvernance IA : classification des risques, processus de validation, registre de modeles.

### Phase 4 — Scale & Optimize (Mois 6-18)

16. Deployer les cas d'usage strategiques de la Wave 2.
17. Industrialiser les pipelines MLOps : automatisation du re-entrainement, monitoring de drift, A/B testing.
18. Etendre le reseau d'AI Champions dans les metiers.
19. Implementer la conformite reglementaire (EU AI Act, NIST AI RMF) operationnelle.
20. Definir et executer la strategie GenAI : selection des foundation models, governance LLM, agents.

### Phase 5 — Transform & Innovate (Mois 18+)

21. Lancer les initiatives de transformation IA (AI-native products, processus autonomes).
22. Deployer les agents IA autonomes avec les garde-fous et le monitoring appropries.
23. Optimiser le portefeuille IA : decommissionner les modeles sans valeur, scaler les succes.
24. Evoluer vers un modele d'organisation federe mature.
25. Etablir un programme d'innovation IA continue (veille, experimentation, partenariats).

## State of the Art (2025-2026)

La stratégie IA entre dans une phase de maturité opérationnelle :

- **IA générative en production** : Les entreprises passent du POC à la mise en production à grande échelle, avec des challenges de coût, de latence et de gouvernance.
- **AI agents** : Les agents autonomes (multi-step reasoning, tool use) transforment les cas d'usage de l'automatisation des tâches à la prise de décision assistée.
- **Souveraineté et modèles open source** : Les modèles open source (Llama, Mistral) offrent des alternatives aux APIs propriétaires, avec des enjeux de souveraineté des données.
- **AI Center of Excellence 2.0** : Les CoE évoluent vers des structures embedded dans les business units plutôt que centralisées, pour accélérer l'adoption.
- **ROI measurement** : Les frameworks de mesure du ROI de l'IA se structurent, au-delà des métriques techniques vers l'impact business mesurable.

## Template actionnable

### Scorecard de priorisation de use cases IA

| Use case | Impact business (1-5) | Faisabilité technique (1-5) | Données disponibles (1-5) | Risque (1-5, inversé) | Score total | Priorité |
|---|---|---|---|---|---|---|
| ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| ___ | ___ | ___ | ___ | ___ | ___ | ___ |
| ___ | ___ | ___ | ___ | ___ | ___ | ___ |

> Score = Σ critères. Quick win ≥ 16, Projet stratégique 12-15, Exploration 8-11, Reporter < 8.

## Prompts types

- "Comment construire une feuille de route IA pour mon entreprise ?"
- "Aide-moi à évaluer la maturité IA de notre organisation"
- "Build vs buy : comment choisir pour notre cas d'usage IA ?"
- "Propose un framework de priorisation de use cases IA"
- "Comment créer un centre d'excellence IA ?"
- "Aide-moi à construire un business case pour un projet IA"

## Skills connexes

| Skill | Lien |
|---|---|
| Stratégie | `entreprise:strategie` — Intégration de l'IA dans la stratégie corporate |
| IT Systèmes | `entreprise:it-systemes` — Infrastructure et gouvernance IT pour l'IA |
| AI Ethics | `ai-governance:ai-ethics` — IA responsable et cadre éthique |
| Prompt Engineering | `ai-governance:prompt-engineering-llmops` — Implémentation et opérations LLM |
| Risk Management | `entreprise:risk-management` — Gouvernance des risques liés à l'IA |

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[AI Strategy & Roadmap](./references/ai-strategy-roadmap.md)** : modeles de maturite IA detailles, creation de roadmap, priorisation des cas d'usage (quick wins vs moonshots), decisions build vs buy vs partner, frameworks ROI, modeles de CoE IA, programmes d'AI literacy.
- **[Model Governance](./references/model-governance.md)** : cycle de vie MLOps complet, registre de modeles (MLflow, W&B), validation et approbation des modeles, monitoring (data drift, concept drift, performance decay), decommissionnement, gouvernance specifique aux LLM et modeles generatifs.
- **[AI Organization](./references/ai-organization.md)** : structures d'equipes IA (centralise, hub & spoke, embedded, federe), roles (Data Scientist, ML Engineer, AI Engineer, AI PM), upskilling et montee en competences, AI champions, patterns de collaboration entre equipes IA et metiers.
- **[AI Regulatory Frameworks](./references/ai-regulatory-frameworks.md)** : EU AI Act (classification des risques, obligations par niveau), NIST AI RMF (fonctions Govern/Map/Measure/Manage), ISO 42001 (systeme de management de l'IA), reglementations sectorielles, paysage international de la gouvernance IA.

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.
