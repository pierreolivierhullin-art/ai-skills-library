---
name: ai-ethics
description: This skill should be used when the user asks about "AI ethics", "algorithmic bias", "fairness", "explainability", "XAI", "responsible AI", "trustworthy AI", "AI transparency", "bias mitigation", "model cards", "éthique de l'IA", "biais algorithmique", "équité", "explicabilité", "IA responsable", "IA de confiance", "transparence IA", "atténuation des biais", "fiches modèle", "AI audit", "audit algorithmique", "discrimination algorithmique", "AI impact assessment", "étude d'impact IA", "AIDA", "EU AI Act", "AI Act européen", "human-in-the-loop", "HITL", "AI accountability", "responsabilité IA", "data ethics", "éthique des données", "consent management", "fairness metrics", "disparate impact", "AI governance framework", or needs guidance on ethical AI development, bias detection, and responsible AI practices.
version: 1.0.0
---

# AI Ethics, Fairness & Responsible AI

## Overview

Ce skill couvre l'ensemble des disciplines liees a l'ethique de l'intelligence artificielle, a l'equite algorithmique et au developpement responsable de l'IA. Il fournit un cadre structure pour identifier, mesurer et attenuer les biais algorithmiques, assurer la transparence et l'explicabilite des modeles, et mettre en oeuvre les principes d'une IA digne de confiance. L'ethique de l'IA ne se limite pas a un exercice de conformite reglementaire : elle englobe la conception equitable des systemes, la protection des droits fondamentaux, l'evaluation des impacts sociaux et environnementaux, et la mise en place de mecanismes de gouvernance tout au long du cycle de vie des modeles. Appliquer systematiquement les principes decrits ici pour guider chaque decision de conception, d'entrainement, de deploiement et de suivi des systemes d'IA.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Detection et attenuation de biais** : identification de biais dans les donnees d'entrainement, les features, les predictions ou les outcomes d'un modele ; choix et implementation de techniques de debiasing (pre-processing, in-processing, post-processing).
- **Mesure de l'equite algorithmique** : selection et calcul de metriques de fairness (demographic parity, equalized odds, calibration, individual fairness) ; analyse d'impact disparate.
- **Explicabilite et interpretabilite** : generation d'explications pour les predictions d'un modele (SHAP, LIME, attention maps, counterfactual explanations) ; choix entre interpretabilite intrinseque et post-hoc.
- **Documentation et transparence** : redaction de model cards, datasheets for datasets, transparency reports ; conformite a l'article 22 du RGPD (droit a l'explication).
- **Evaluation d'impact algorithmique** : conduite d'une Algorithmic Impact Assessment (AIA), evaluation de l'impact social et environnemental (empreinte carbone, CodeCarbon).
- **Mise en conformite IA de confiance** : application des 7 exigences de l'UE pour une IA digne de confiance, implementation du human-in-the-loop, privacy-preserving AI (federated learning, differential privacy).
- **Audit ethique et gouvernance** : mise en place de comites d'ethique IA, processus d'audit continu, red teaming ethique, consultation des parties prenantes.

## Core Principles

### Principle 1 -- Fairness by Design

Integrer l'equite des la phase de conception, pas comme une correction a posteriori. Definir les groupes proteges et les metriques d'equite avant l'entrainement. Documenter explicitement les compromis entre les differentes definitions de fairness (impossibility theorems de Chouldechova et Kleinberg). Ne jamais supposer qu'un modele est equitable sans mesure quantitative.

### Principle 2 -- Transparency & Explainability First

Privilegier les modeles interpretables pour les decisions a fort impact (credit, sante, justice, recrutement). Quand un modele complexe est necessaire, fournir systematiquement des explications post-hoc adaptees au public cible (data scientists, decideurs metier, personnes concernees). Documenter les limites connues des methodes d'explicabilite utilisees.

### Principle 3 -- Accountability Through Documentation

Documenter chaque etape du cycle de vie du modele : provenance des donnees (datasheets for datasets), choix de conception et compromis (model cards), metriques de performance ventilees par sous-groupes, decisions de deploiement et conditions de retrait. La documentation est le fondement de la responsabilite (accountability).

### Principle 4 -- Human Oversight & Agency

Maintenir un controle humain significatif sur les decisions automatisees a fort impact. Implementer des mecanismes de human-in-the-loop (validation humaine avant action), human-on-the-loop (supervision en continu avec capacite d'intervention), ou human-in-command (gouvernance strategique). Garantir le droit de recours et de contestation pour les personnes affectees.

### Principle 5 -- Proportionality & Do No Harm

Evaluer systematiquement si le recours a l'IA est proportionne au probleme pose. Mesurer les risques de prejudice pour les populations vulnerables. Appliquer le principe de precaution : en cas de doute sur l'impact, ne pas deployer sans etude d'impact approfondie. Considerer l'impact environnemental (energie, eau, emissions carbone) de l'entrainement et de l'inference.

### Principle 6 -- Continuous Monitoring & Iteration

L'equite et la performance d'un modele evoluent dans le temps (data drift, concept drift, societal changes). Mettre en place un monitoring continu des metriques de fairness en production. Definir des seuils d'alerte et des procedures de rollback. Realiser des audits periodiques independants.

## Key Frameworks & Methods

### Bias Taxonomy

| Type de biais | Source | Exemple | Detection |
|---|---|---|---|
| **Selection bias** | Donnees non representatives | Modele de credit entraine uniquement sur des profils urbains | Analyse de couverture demographique |
| **Measurement bias** | Proxy variables, erreurs de mesure | Code postal comme proxy de l'ethnicite | Analyse de correlation features/attributs proteges |
| **Representation bias** | Sous-representation de groupes | Dataset de visages avec 80% de personnes blanches | Distribution statistique par sous-groupe |
| **Historical bias** | Inegalites refletees dans les donnees historiques | Donnees de recrutement refletant des discriminations passees | Analyse causale, consultation d'experts |
| **Aggregation bias** | Traitement uniforme de groupes heterogenes | Modele medical unique pour toutes les populations | Performance ventilee par sous-groupe |
| **Evaluation bias** | Benchmarks non representatifs | Benchmark NLP uniquement en anglais americain | Audit des datasets d'evaluation |

### Fairness Metrics Decision Guide

```
1. Quel est le contexte de decision ?
   +-- Decision binaire (accept/reject) --> Equalized Odds, Predictive Parity
   +-- Score continu (scoring) --> Calibration, AUC par sous-groupe
   +-- Ranking / classement --> Exposure fairness, Attention fairness

2. Quelle definition de l'equite est prioritaire ?
   +-- Egalite des taux de selection --> Demographic Parity (Statistical Parity)
   +-- Egalite des taux d'erreur --> Equalized Odds (FPR et FNR egaux)
   +-- Egalite de la valeur predictive --> Predictive Parity (Calibration)
   +-- Equite individuelle --> Similar individuals, similar outcomes

3. Quel compromis accepter ?
   +-- Theorem d'impossibilite : on ne peut pas satisfaire simultanement
       Demographic Parity + Equalized Odds + Calibration
       (sauf si les taux de base sont identiques entre groupes)
   +-- Documenter explicitement le choix et sa justification
```

### XAI Methods Overview

| Methode | Type | Scope | Avantages | Limites |
|---|---|---|---|---|
| **SHAP** | Post-hoc, model-agnostic | Local & Global | Theorie solide (Shapley values), consistant | Cout computationnel eleve pour les gros modeles |
| **LIME** | Post-hoc, model-agnostic | Local | Intuitif, rapide | Instabilite des explications, sensible au sampling |
| **Attention Maps** | Intrinseque | Local | Natif pour les transformers | Debat sur la fiabilite comme explication causale |
| **Counterfactual** | Post-hoc | Local | Actionnable ("si X avait ete Y...") | Plusieurs counterfactuals possibles, choix non unique |
| **SHAP Interaction** | Post-hoc | Global | Capture les interactions entre features | Complexite O(n^2) |
| **Partial Dependence** | Post-hoc, model-agnostic | Global | Visualisation intuitive | Assume l'independance des features |
| **Integrated Gradients** | Post-hoc, model-specific | Local | Axiomatiquement rigoureux | Necessite un modele differentiable |

### EU Trustworthy AI -- 7 Requirements

Appliquer les 7 exigences du High-Level Expert Group (HLEG) de la Commission europeenne :

1. **Human agency and oversight** : Garantir l'autonomie humaine et le controle significatif.
2. **Technical robustness and safety** : Resister aux attaques adversariales, gerer les erreurs, assurer la fiabilite.
3. **Privacy and data governance** : Proteger les donnees personnelles, assurer la qualite des donnees.
4. **Transparency** : Tracabilite, explicabilite, communication ouverte sur les limites.
5. **Diversity, non-discrimination and fairness** : Eviter les biais injustes, assurer l'accessibilite.
6. **Societal and environmental well-being** : Impact positif sur la societe, durabilite environnementale.
7. **Accountability** : Responsabilite, auditabilite, mecanismes de recours.

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Fairness-aware Training** : Integrer des contraintes d'equite directement dans la fonction de perte du modele (in-processing). Plus efficace que les corrections post-hoc car le modele apprend a etre equitable. Frameworks : Fairlearn, AIF360, Themis-ML.
- **Disaggregated Evaluation** : Toujours evaluer les performances du modele ventilees par sous-groupe (genre, age, ethnicite, etc.) plutot que de se fier uniquement a la performance globale. Un modele peut avoir une accuracy globale de 95% mais 70% pour un sous-groupe specifique.
- **Layered Explainability** : Fournir des explications a plusieurs niveaux de granularite : explication globale du modele (feature importance), explication locale de chaque prediction (SHAP values), explication contrefactuelle actionnable pour l'utilisateur final.
- **Ethics by Design Workshops** : Organiser des ateliers de reflexion ethique en amont de chaque projet IA impliquant des experts metier, des ethiciens, des juristes et des representants des populations affectees.
- **Continuous Fairness Monitoring** : Deployer des dashboards de fairness en production avec alertes automatiques quand les metriques d'equite derivent au-dela des seuils definis.

### Anti-patterns critiques

- **Fairness Washing** : Publier des metriques de fairness sans action corrective reelle. Diagnostiquer via : "Les metriques defavorables ont-elles declenche des modifications du modele ?"
- **Explanation Overconfidence** : Presenter les explications SHAP/LIME comme des verites causales alors qu'elles sont correlationnelles. Toujours communiquer les limites epistemologiques.
- **One-Size-Fits-All Fairness** : Appliquer la meme metrique d'equite a tous les contextes. La definition de fairness doit etre adaptee au domaine et co-construite avec les parties prenantes.
- **Bias Blind Spot** : Ne tester les biais que pour les attributs proteges les plus evidents (genre, ethnicite) en ignorant les intersections (femmes agees issues de minorites) et les biais socio-economiques.
- **Documentation Afterthought** : Rediger les model cards et datasheets apres le deploiement. La documentation doit etre un artefact vivant mis a jour a chaque etape.

## Implementation Workflow

### Phase 1 -- Ethical Framing & Impact Scoping

1. Identifier les populations affectees par le systeme et cartographier les risques de prejudice potentiels.
2. Conduire une evaluation d'impact algorithmique preliminaire (AIA screening).
3. Definir les attributs proteges pertinents et les metriques d'equite cibles avec les parties prenantes.
4. Rediger le datasheet for dataset documentant la provenance, les conditions de collecte et les limites des donnees.
5. Organiser un Ethics by Design Workshop avec les parties prenantes (equipe technique, metier, ethiciens, representants).

### Phase 2 -- Bias Detection & Data Preparation

6. Analyser la distribution des donnees par sous-groupe (representation, label rates, feature distributions).
7. Tester les correlations entre features et attributs proteges (detection de proxies).
8. Appliquer les techniques de debiasing pre-processing si necessaire (reweighting, resampling, relabeling).
9. Documenter toutes les transformations appliquees et leur justification.
10. Valider les donnees preparees avec un second audit independant.

### Phase 3 -- Fair Model Training & Explanation

11. Entrainer le modele avec des contraintes d'equite (in-processing) ou appliquer des corrections post-processing.
12. Evaluer les performances ventilees par sous-groupe sur un jeu de test representatif.
13. Generer les explications globales (feature importance, SHAP summary) et locales (SHAP waterfall, LIME).
14. Rediger la model card incluant : intended use, out-of-scope uses, performance metrics by subgroup, ethical considerations, limitations.
15. Valider les explications avec des utilisateurs non-techniques pour s'assurer de leur comprehensibilite.

### Phase 4 -- Deployment, Monitoring & Audit

16. Deployer avec human-in-the-loop pour les decisions a fort impact (periode probatoire minimum).
17. Mettre en place le monitoring continu des metriques de fairness en production (dashboards, alertes).
18. Definir les seuils de rollback automatique si les metriques derivent.
19. Planifier des audits periodiques independants (trimestriels pour les systemes a haut risque).
20. Maintenir un registre des incidents ethiques et des actions correctives.

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[Bias & Fairness](./references/bias-fairness.md)** : taxonomie complete des biais, metriques de fairness (demographic parity, equalized odds, calibration), techniques de detection, strategies d'attenuation (pre/in/post-processing), fairness-aware ML, analyse d'impact disparate, outils et frameworks.
- **[Explainability & Transparency](./references/explainability-transparency.md)** : methodes XAI (SHAP, LIME, attention maps, counterfactual), interpretabilite intrinseque vs post-hoc, model cards, datasheets for datasets, RGPD article 22, transparency reports, outils et librairies.
- **[Trustworthy AI](./references/trustworthy-ai.md)** : 7 exigences de l'UE pour l'IA de confiance, human oversight, robustesse et securite, privacy-preserving AI (federated learning, differential privacy), frameworks de responsabilite, EU AI Act.
- **[Impact Assessment](./references/impact-assessment.md)** : Algorithmic Impact Assessment, evaluation d'impact social, impact environnemental (empreinte carbone, CodeCarbon), consultation des parties prenantes, monitoring continu et audit, cadres reglementaires.
