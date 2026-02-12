---
name: code-excellence
description: This skill should be used when the user asks about "clean code", "code quality", "refactoring", "testing strategy", "TDD", "BDD", "code review", "technical debt", "SOLID principles", "design patterns", "coding standards", "qualité de code", "dette technique", "revue de code", "principes SOLID", "standards de code", "bonnes pratiques", "best practices", "DRY", "KISS", "YAGNI", "code smells", "code coverage", "couverture de tests", "unit testing", "tests unitaires", "integration testing", "tests d'intégration", "mocking", "pair programming", "mob programming", "linting", "static analysis", "analyse statique", "cyclomatic complexity", "software craftsmanship", or needs guidance on software craftsmanship and engineering best practices.
version: 1.1.0
last_updated: 2026-02
---

# Code Excellence

Maîtrise du craft logiciel : clean code, testing, refactoring et revue de code au niveau expert.

## Overview

Appliquer les principes d'excellence du code pour produire un logiciel maintenable, testable et évolutif. Cette skill couvre l'ensemble du cycle de qualité du code : écriture propre, stratégies de test, refactoring méthodique et revue collaborative. Elle intègre les pratiques modernes (2024-2026) incluant le testing par propriétés, le contract testing, la revue assistée par IA et le trunk-based development.

L'excellence du code n'est pas un luxe mais un multiplicateur de vélocité. Un codebase propre réduit le temps de compréhension (qui représente 70% du temps de développement), diminue les bugs en production et accélère l'onboarding des nouveaux développeurs. Adopter ces pratiques transforme la dette technique d'un fardeau invisible en un levier maîtrisé.

## When This Skill Applies

Activer cette skill dans les situations suivantes :

- **Écriture de nouveau code** : appliquer les principes SOLID, DRY, KISS et YAGNI dès la conception pour éviter l'accumulation de dette technique.
- **Définition d'une stratégie de test** : choisir les bons niveaux de test (unitaire, intégration, e2e), adopter TDD/BDD, mettre en place du property-based testing ou du contract testing.
- **Refactoring de code existant** : identifier les code smells, appliquer les techniques de refactoring de manière incrémentale, gérer du legacy code.
- **Revue de code (code review)** : structurer le processus de review, donner du feedback constructif, optimiser la taille des PRs, intégrer des outils d'analyse assistée par IA.
- **Gestion de la dette technique** : identifier, quantifier et prioriser la dette, définir une stratégie de remboursement progressive.
- **Mise en place de standards d'équipe** : définir des coding conventions, des linters, des quality gates et des métriques de qualité.

## Core Principles

### SOLID Principles
Appliquer systématiquement les cinq principes SOLID comme fondation architecturale :
- **S** - Single Responsibility : chaque module, classe ou fonction ne doit avoir qu'une seule raison de changer.
- **O** - Open/Closed : concevoir les entités ouvertes à l'extension mais fermées à la modification.
- **L** - Liskov Substitution : garantir que tout sous-type peut remplacer son type parent sans altérer le comportement.
- **I** - Interface Segregation : préférer plusieurs interfaces spécifiques à une interface généraliste.
- **D** - Dependency Inversion : dépendre d'abstractions, jamais de concrétions.

### DRY, KISS, YAGNI
Appliquer cette triade comme garde-fou permanent :
- **DRY** (Don't Repeat Yourself) : éliminer la duplication de logique, pas simplement de texte. Distinguer la duplication accidentelle (à factoriser) de la duplication délibérée (contextes métier différents).
- **KISS** (Keep It Simple, Stupid) : privilégier la solution la plus simple qui résout le problème. La complexité accidentelle est l'ennemi principal.
- **YAGNI** (You Aren't Gonna Need It) : ne jamais implémenter une fonctionnalité par anticipation. Coder pour le besoin actuel, concevoir pour l'extensibilité.

### Boy Scout Rule & Continuous Improvement
Laisser le code dans un meilleur état qu'à son arrivée. Chaque modification est une opportunité d'amélioration incrémentale : renommer une variable ambiguë, extraire une méthode, ajouter un test manquant.

## Key Frameworks & Methods

### Test Pyramid & Modern Testing
Structurer la stratégie de test selon la pyramide modernisée :
- **Base large : tests unitaires** (70%) -- rapides, isolés, couvrant la logique métier pure.
- **Milieu : tests d'intégration** (20%) -- validant les interactions entre composants, bases de données, APIs.
- **Sommet fin : tests end-to-end** (10%) -- scénarios critiques utilisateur, maintenus au strict minimum.

Compléter avec les approches modernes :
- **Property-based testing** : vérifier des invariants sur des entrées générées aléatoirement (fast-check, Hypothesis, jqwik).
- **Contract testing** (Pact, Spring Cloud Contract) : valider les contrats entre services sans déploiement intégré.
- **Snapshot testing** : capturer les régressions de sortie (UI, API responses), à utiliser avec discernement.
- **Mutation testing** (Stryker, PITest) : évaluer la qualité réelle des tests en injectant des mutations dans le code.

### TDD & BDD
- **TDD** : suivre le cycle Red-Green-Refactor strictement. Écrire le test d'abord, implémenter le minimum pour le faire passer, puis refactorer.
- **BDD** (Behavior-Driven Development) : exprimer les comportements attendus en langage Gherkin (Given/When/Then) pour aligner développeurs, QA et métier.

### Code Review Process
Structurer les revues de code comme un outil d'apprentissage collectif, pas comme un gatekeeping :
- Limiter les PRs à 200-400 lignes de diff pour une revue efficace.
- Utiliser des checklists de revue couvrant : logique, sécurité, performance, lisibilité, tests.
- Intégrer des outils d'analyse assistée par IA (Copilot code review, CodeRabbit, Sourcery) comme premier filtre.
- Pratiquer le pair/mob programming comme alternative synchrone à la review asynchrone.

### Trunk-Based Development
Adopter le trunk-based development pour réduire la friction :
- Travailler sur des branches courtes (< 1 jour) fusionnées fréquemment dans le trunk.
- Utiliser les feature flags pour découpler déploiement et release.
- Combiner avec CI/CD pour valider chaque intégration automatiquement.

## Decision Guide

### Quand appliquer TDD vs test-after ?

| Critère | TDD recommandé | Test-after acceptable |
|---|---|---|
| Logique métier complexe | Oui | Non |
| Prototype/spike exploratoire | Non | Oui |
| Bug fix | Oui (test reproduisant le bug d'abord) | Non |
| Code CRUD simple | Optionnel | Oui |
| Algorithme critique | Oui | Non |

### Quand refactorer vs réécrire ?

| Situation | Refactoring incrémental | Réécriture (Strangler Fig) |
|---|---|---|
| Code avec tests existants | Oui | Non |
| Code sans tests, couplage modéré | Oui (ajouter tests d'abord) | Non |
| Architecture fondamentalement inadaptée | Non | Oui |
| Technologie obsolète sans support | Non | Oui |
| Module isolé < 1000 lignes | Oui | Non |

### Niveau de couverture cible

Ne pas viser 100% de couverture aveuglément. Prioriser :
- **Couverture de la logique métier critique** : 90%+ (calculs, règles, validations).
- **Couverture des chemins d'erreur** : 80%+ (gestion d'exceptions, cas limites).
- **Code d'infrastructure/glue** : 50-70% (tests d'intégration suffisants).
- **Métrique complémentaire** : utiliser le mutation score (Stryker) pour évaluer la pertinence réelle des tests.

## Common Patterns & Anti-Patterns

### Patterns vertueux
- **Arrange-Act-Assert (AAA)** : structurer chaque test en trois phases claires pour maximiser la lisibilité.
- **Builder Pattern pour les tests** : créer des builders de données de test pour éviter les fixtures fragiles.
- **Ports & Adapters** : isoler la logique métier des dépendances externes pour la testabilité.
- **Feature Flags** : découpler le déploiement de la mise en production fonctionnelle.
- **Naming expressif** : nommer les tests `should_[expected]_when_[condition]` pour documenter le comportement.

### Anti-patterns critiques
- **God Class / God Function** : décomposer toute classe > 200 lignes ou fonction > 20 lignes en responsabilités distinctes.
- **Test couplé à l'implémentation** : tester le comportement, jamais les détails d'implémentation (pas de mock excessif).
- **Commentaires compensatoires** : si un commentaire est nécessaire, refactorer le code pour qu'il s'explique lui-même.
- **Primitive Obsession** : encapsuler les concepts métier dans des Value Objects (Email, Money, UserId) plutôt que des types primitifs.
- **Couverture cosmétique** : écrire des tests qui couvrent des lignes sans valider de comportement (assertion absente ou triviale).
- **Feature branch de longue durée** : fusionner au moins quotidiennement ; une branche de plus de 2 jours est un risque de merge conflict et de divergence.

## Implementation Workflow

Suivre ce workflow pour toute initiative d'amélioration de la qualité du code :

### Phase 1 -- Diagnostic (1-2 jours)
1. Exécuter une analyse statique (SonarQube, ESLint, Pylint) pour identifier les hotspots de complexité.
2. Mesurer la couverture de test existante et le mutation score.
3. Identifier les fichiers les plus modifiés (churn) via `git log` : ce sont les cibles prioritaires de refactoring.
4. Cartographier la dette technique existante avec une matrice impact/effort.

### Phase 2 -- Standards & Outillage (1 semaine)
1. Définir les coding standards de l'équipe (linter rules, formatage, conventions de nommage).
2. Configurer les quality gates dans la CI : couverture minimale, complexité cyclomatique maximale, zéro code smell bloquant.
3. Mettre en place une checklist de code review partagée.
4. Intégrer un outil de revue assistée par IA comme filtre de premier niveau.

### Phase 3 -- Amélioration continue (ongoing)
1. Appliquer la Boy Scout Rule sur chaque commit.
2. Planifier des sessions de refactoring dédiées (20% du sprint).
3. Pratiquer le TDD pour toute nouvelle fonctionnalité de logique métier.
4. Conduire des revues de code bienveillantes et formatives.
5. Mesurer et visualiser l'évolution des métriques de qualité mensuellement.

### Phase 4 -- Legacy Modernization (si applicable)
1. Identifier les seams (points de jointure) dans le code legacy pour insérer des tests de caractérisation.
2. Appliquer le pattern Strangler Fig pour remplacer les modules legacy progressivement.
3. Utiliser Branch by Abstraction pour substituer les implémentations sans Big Bang.
4. Documenter les décisions architecturales via des ADR (Architecture Decision Records).



## Template actionnable

### Checklist de code review

| Critère | Vérifié | Commentaire |
|---|---|---|
| **Lisibilité** — Nommage clair, fonctions courtes | ☐ | ___ |
| **SOLID** — Principes respectés | ☐ | ___ |
| **DRY** — Pas de duplication inutile | ☐ | ___ |
| **Tests** — Cas nominaux et edge cases couverts | ☐ | ___ |
| **Error handling** — Erreurs gérées proprement | ☐ | ___ |
| **Sécurité** — Pas d'injection, inputs validés | ☐ | ___ |
| **Performance** — Pas de N+1, requêtes optimisées | ☐ | ___ |
| **Types** — Typage strict, pas de `any` | ☐ | ___ |
| **Documentation** — Logique complexe commentée | ☐ | ___ |
| **Breaking changes** — API rétrocompatible ou migrée | ☐ | ___ |

## Prompts types

- "Comment réduire la dette technique de mon projet ?"
- "Propose une stratégie de tests pour mon application TypeScript"
- "Aide-moi à refactorer ce code en appliquant les principes SOLID"
- "Comment mettre en place un processus de code review efficace ?"
- "Quels design patterns utiliser pour ce cas d'usage ?"
- "Analyse ce code et identifie les code smells"

## Skills connexes

| Skill | Lien |
|---|---|
| Architecture | `code-development:architecture` — Patterns architecturaux et principes de conception |
| Quality Reliability | `code-development:quality-reliability` — Stratégie de tests et automatisation QA |
| Process Engineering | `code-development:process-engineering` — Standards de code et revue de code |
| UI/UX | `code-development:ui-ux` — Qualité du code frontend et composants |
| Monitoring | `code-development:monitoring` — Observabilité et logging dans le code |

## Additional Resources

Consulter les fichiers de référence suivants pour un approfondissement détaillé :

- [Clean Code & Design Principles](./references/clean-code.md) -- Principes SOLID en profondeur, DRY/KISS/YAGNI, conventions de nommage, gestion de la complexité cyclomatique et cognitive, patterns de design appliqués au développement moderne. Inclut des exemples de code concrets.

- [Testing Strategies](./references/testing-strategies.md) -- Pyramide des tests, TDD, BDD (Gherkin/Cucumber), property-based testing, snapshot testing, contract testing (Pact), stratégies de mocking, couverture significative vs 100%. Outils et approches modernes.

- [Refactoring & Technical Debt](./references/refactoring.md) -- Catalogue de refactoring (extract, inline, rename, move), travail avec du legacy code (Michael Feathers), strangler fig pattern, branch by abstraction, modernisation incrémentale. Identification et gestion de la dette technique.

- [Code Review & Collaboration](./references/code-review.md) -- Processus de code review, feedback constructif, checklists de revue, optimisation de la taille des PRs, pair/mob programming, revue assistée par IA, partage de connaissances au travers des revues.

### Ouvrages et références fondamentaux
- Robert C. Martin, *Clean Code* (2008) et *Clean Architecture* (2017)
- Martin Fowler, *Refactoring: Improving the Design of Existing Code* (2nd ed., 2018)
- Michael Feathers, *Working Effectively with Legacy Code* (2004)
- Kent Beck, *Test-Driven Development: By Example* (2002)
- Dave Farley, *Modern Software Engineering* (2021)
- Tidy First? -- Kent Beck (2023)
- Adam Tornhill, *Software Design X-Rays* (2018) et *Your Code as a Crime Scene* (2015)
