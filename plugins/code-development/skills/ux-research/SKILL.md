---
name: ux-research
description: >
  Expert guide for UX research, user interviews, usability testing, personas, user journey mapping,
  information architecture, wireframing, prototyping, Jobs-to-be-Done, Google Design Sprint,
  heuristic evaluation (Nielsen), SUS scoring, and UX metrics. Invoke this skill proactively
  whenever the conversation involves understanding users, validating designs, or improving
  user experience — even if framed as 'product research', 'customer feedback', or 'design
  validation'. If user behavior, needs, pain points, or usability are in scope, this skill applies.
version: 1.0.0
last_updated: 2026-03-25
---

# UX Research & User Experience

Expert-level guidance for user research methods, usability testing, UX strategy, information architecture, and evidence-based design decision-making.

## Overview

Ce skill couvre la dimension **UX** de la discipline design : comprendre les utilisateurs, valider les hypothèses, concevoir des parcours efficaces et mesurer la qualité de l'expérience. La recherche utilisateur n'est pas optionnelle — c'est la base de toute décision de design valide.

Un cycle de recherche court (5 participants, tests d'utilisabilité) révèle 85% des problèmes majeurs d'une interface. Sans cette base, les équipes conçoivent pour elles-mêmes, pas pour leurs utilisateurs.

## When This Skill Applies

- **Recherche utilisateur** : planification et conduite d'interviews, surveys, diary studies, contextual inquiry.
- **Tests d'utilisabilité** : modération de sessions de test, analyse des résultats, priorisation des problèmes.
- **Personas & journeys** : création de personas basés sur des données réelles, user journey mapping, service blueprints.
- **Information architecture** : card sorting, tree testing, navigation design, taxonomies.
- **Prototypage & validation** : wireframes low-fidelity, prototypes Figma, guerilla testing.
- **UX metrics** : SUS (System Usability Scale), NPS, UMUX-Lite, task completion rates, error rates.
- **Design sprints** : facilitation de Google Design Sprints, workshops de co-conception.
- **Évaluation heuristique** : audit UX structuré basé sur les 10 heuristiques de Nielsen.

## Core Principles

### Principle 1 — User-Centered Design: Research Before Solutions
Fonder chaque décision de design sur des données utilisateur réelles. Conduire au minimum un cycle de recherche (interviews, tests d'utilisabilité) avant de finaliser toute décision de design significative. Valider chaque itération par des métriques mesurables. La conviction personnelle n'est pas une donnée.

### Principle 2 — Accessibility as a UX Imperative
L'accessibilité est une dimension fondamentale de l'expérience utilisateur, pas une contrainte technique. Inclure des participants avec handicaps dans les sessions de recherche. Un design inaccessible est un mauvais design, indépendamment de son esthétique. L'European Accessibility Act (EAA 2025) renforce cette exigence légalement.

### Principle 3 — Mixed Methods for Robust Insights
Combiner méthodes qualitatives (interviews, observations) et quantitatives (surveys, analytics) pour des insights robustes. Les méthodes qualitatives révèlent le *pourquoi*, les méthodes quantitatives révèlent le *quoi* et le *combien*. Ni l'un ni l'autre seul ne suffit.

### Principle 4 — Continuous Discovery over Episodic Research
La recherche n'est pas un événement ponctuel en début de projet. Intégrer des micro-sessions de validation hebdomadaires dans le rythme produit (continuous discovery). 30 minutes de test par semaine vaut mieux qu'un grand projet de recherche tous les 6 mois.

### Principle 5 — Share Research to Build Organizational Empathy
Les insights de recherche doivent être accessibles à toute l'équipe, pas gardés dans des silos. Créer des artifacts partageables (personas, journey maps, highlight reels) qui construisent l'empathie organisationnelle pour les utilisateurs.

## Key Frameworks & Methods

### UX Research Methods Matrix

| Method | Quand utiliser | Effort | Type de données |
|---|---|---|---|
| **User Interviews** | Discovery, validation | Moyen | Qualitatif |
| **Usability Testing** | Prototype, post-launch | Moyen-Élevé | Quali + Quanti |
| **Surveys** | Validation à grande échelle | Faible | Quantitatif |
| **Card Sorting** | Information architecture | Faible | Qualitatif |
| **Diary Studies** | Comportements long terme | Élevé | Qualitatif |
| **A/B Testing** | Optimisation | Moyen | Quantitatif |
| **Heuristic Evaluation** | Audit rapide | Faible | Expert review |
| **Contextual Inquiry** | Compréhension profonde | Élevé | Qualitatif |
| **Tree Testing** | Navigation validation | Faible | Quantitatif |
| **5-Second Test** | First impressions | Très faible | Qualitatif |
| **Guerilla Testing** | Validation rapide | Très faible | Qualitatif |
| **Session Replay** | Behavior analytics | Faible | Quantitatif |

### Jobs-to-be-Done (JTBD) Framework

Structure un job comme : *"Quand [situation], je veux [motivation], pour [résultat attendu]."*

Les JTBD révèlent les motivations profondes plutôt que les fonctionnalités souhaitées. Un utilisateur n'achète pas une perceuse — il achète un trou dans le mur.

### Les 10 Heuristiques de Nielsen

1. Visibilité du statut système
2. Correspondance entre le système et le monde réel
3. Contrôle et liberté utilisateur
4. Cohérence et standards
5. Prévention des erreurs
6. Reconnaissance plutôt que rappel
7. Flexibilité et efficacité d'utilisation
8. Design esthétique et minimaliste
9. Aide à la reconnaissance, diagnostic et correction des erreurs
10. Aide et documentation

### Google Design Sprint (5 jours)

| Jour | Activité |
|---|---|
| Lundi | Map & Target — comprendre le problème, choisir le défi |
| Mardi | Sketch — générer des solutions individuelles |
| Mercredi | Decide — voter, storyboarder |
| Jeudi | Prototype — construire un prototype testable |
| Vendredi | Test — 5 entretiens utilisateurs avec le prototype |

### UX Metrics Framework

| Métrique | Ce qu'elle mesure | Benchmark |
|---|---|---|
| **SUS (System Usability Scale)** | Utilisabilité globale (0-100) | > 68 = acceptable, > 80 = bon |
| **Task Completion Rate** | % tâches complétées avec succès | Varie par contexte |
| **Time on Task** | Efficience | Comparer avec baseline |
| **Error Rate** | Fréquence d'erreurs utilisateur | < 5% pour tâches critiques |
| **NPS (Net Promoter Score)** | Fidélité et recommandation | > 50 = excellent |
| **UMUX-Lite** | Satisfaction courte (2 items) | Corrélé au SUS |

## Decision Guide

### Quelle méthode de recherche choisir ?

```
1. Stade du projet ?
   |-- Début / Discovery → User interviews + contextual inquiry
   |-- Mi-projet / Design → Usability testing sur prototype (Figma)
   |-- Post-launch / Optimisation → Analytics + A/B testing + session replay

2. Quel budget temps ?
   |-- < 1 jour → Guerilla testing ou heuristic evaluation
   |-- 1-3 jours → Usability testing (5 participants)
   |-- 1-2 semaines → User interviews (8-12 participants)
   +-- 1+ mois → Diary study ou ethnographic research

3. Quantitatif ou qualitatif ?
   |-- Comprendre le POURQUOI → Interviews, usability testing, observations
   |-- Mesurer le COMBIEN → Surveys, analytics, A/B testing
   +-- Les deux → Combinaison: test d'utilisabilité + post-task survey (SUS)
```

### Nombre de participants

- **Tests d'utilisabilité** : 5 participants révèlent 85% des problèmes majeurs (Nielsen's rule)
- **Interviews exploratoires** : 8-12 jusqu'à saturation thématique
- **Surveys quantitatifs** : minimum 100 réponses pour des insights statistiquement valides
- **Guerilla testing** : 3-5 personnes pour validation rapide

## Common Patterns & Anti-Patterns

### Patterns recommandés

- **Continuous Discovery** : sessions de test courtes (30-60 min) hebdomadaires avec de vrais utilisateurs.
- **Research Repository** : centraliser les insights dans un outil partagé (Notion, Dovetail, Airtable).
- **Highlight Reels** : courts clips vidéo des moments-clés des sessions pour construire l'empathie organisationnelle.
- **Research Triangulation** : croiser 3 sources de données différentes avant de tirer des conclusions.
- **Jobs Stories over User Stories** : "Quand [situation], je veux [action], pour [résultat]" plutôt que "En tant qu'utilisateur..."

### Anti-patterns critiques

- **Research as Validation Theater** : conduire une recherche dont le résultat est déjà décidé. La recherche doit pouvoir invalider les hypothèses.
- **Homogeneous Participant Pool** : recruter uniquement ses collègues ou des utilisateurs "faciles". Inclure des personnes avec handicaps, peu expérimentées, et des contextes variés.
- **Insight Graveyard** : accumuler des rapports de recherche jamais lus. Privilégier des formats actionnables et des présentations courtes à l'équipe.
- **Observer Effect Ignored** : ne pas reconnaître que la présence d'un observateur modifie le comportement. Minimiser les biais de modération.
- **Feature Requests ≠ User Needs** : confondre ce que les utilisateurs demandent avec ce dont ils ont besoin. Creuser le "pourquoi" derrière chaque demande.

## Implementation Workflow

### Phase 1 — Research Planning (2-3 jours)
1. Définir les questions de recherche (pas les méthodes — d'abord les questions).
2. Choisir les méthodes adaptées au stade et aux ressources disponibles.
3. Recruter les participants (critères de sélection, screener survey).
4. Préparer le guide d'entretien ou le script de test.

### Phase 2 — Research Execution (1-2 semaines)
5. Conduire les sessions (interviews ou tests d'utilisabilité).
6. Prendre des notes structurées et/ou enregistrer avec consentement.
7. Observer les comportements sans intervenir (sauf si bloqué).
8. Mesurer : task completion, temps, erreurs, SUS post-test.

### Phase 3 — Analysis & Synthesis (2-3 jours)
9. Affinity mapping : regrouper les observations par thèmes.
10. Identifier les patterns récurrents (vu chez ≥ 3 participants = signal fiable).
11. Classer les problèmes par sévérité (impact × fréquence).
12. Formuler des insights actionnables (pas juste des observations).

### Phase 4 — Communication & Action (1 jour)
13. Présenter les insights à l'équipe en < 30 minutes (highlight reel + top 5 findings).
14. Prioriser les problèmes avec l'équipe produit.
15. Définir les actions correctives et les valider lors du prochain cycle de test.
16. Archiver dans le research repository pour référence future.

## Maturity Model

### Niveau 1 — Intuition-Driven
- Décisions de design basées sur les opinions de l'équipe, aucune recherche utilisateur.
- **Indicateurs** : 0 session de test/trimestre, personas imaginaires.

### Niveau 2 — Episodic Research
- Recherche utilisateur ad hoc en début de projet. Quelques interviews par an.
- **Indicateurs** : 1-2 études par an, insights non partagés, aucun repository.

### Niveau 3 — Structured Research
- Méthodes standardisées, templates de guide d'entretien, SUS mesuré systématiquement.
- **Indicateurs** : tests utilisabilité sur chaque feature majeure, SUS > 68.

### Niveau 4 — Continuous Discovery
- Sessions hebdomadaires courtes intégrées au sprint. Research repository à jour.
- Inclusivité : participants avec handicaps, contextes diversifiés.
- **Indicateurs** : ≥ 1 session/semaine, SUS > 75, insights actionnés < 2 sprints.

### Niveau 5 — Research-Led Organization
- La recherche pilote la roadmap produit. Empathie utilisateur partagée dans toute l'organisation.
- UX metrics intégrées aux OKRs produit et business.
- **Indicateurs** : SUS > 80, NPS > 50, task completion > 90% sur parcours critiques.

## Rythme opérationnel recommandé

| Cadence | Activité | Livrable |
|---|---|---|
| **Hebdomadaire** | Mini-test utilisabilité (30-60 min, 3-5 participants) | Top 3 insights + actions |
| **Mensuel** | Session d'usability testing complète (5 participants, parcours critiques) | Rapport usability + recommandations priorisées |
| **Trimestriel** | Revue UX stratégique (parcours utilisateur, pain points, opportunités) | Roadmap UX trimestrielle |
| **Annuel** | Étude longitudinale ou benchmark concurrentiel | Rapport stratégique UX |

## Additional Resources

- **[UX Research](./references/ux-research.md)** — Méthodes détaillées (interviews, usability testing, diary studies), personas et user journeys, JTBD, heuristiques de Nielsen, card sorting, contextual inquiry, Design Sprint.
- **[Études de cas](./references/case-studies.md)** — Cas pratiques illustrant les concepts clés.

## See Also

- **ui-design** (`code-development/ui-design`) — Design systems, composants, CSS architecture (la dimension UI de cette discipline)
- **user-research** (`entreprise/user-research`) — Perspective business de la recherche utilisateur, liée aux décisions produit
- **ux-engineering** (`code-development/ux-engineering`) — Implémentation technique des parcours utilisateur et onboarding
- **customer-analytics** (`data-bi/customer-analytics`) — LTV, cohortes, analytics client quantitatif
- **ab-testing-experimentation** (`data-bi/ab-testing-experimentation`) — Tests A/B statistiquement rigoureux
