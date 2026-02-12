# Code Review & Collaboration

Référence approfondie sur le processus de code review, le feedback constructif, la collaboration et les outils modernes d'assistance par IA.

---

## Table of Contents

1. [Code Review Philosophy](#code-review-philosophy)
2. [The Review Process](#the-review-process)
3. [Constructive Feedback](#constructive-feedback)
4. [Review Checklists](#review-checklists)
5. [PR Size Optimization](#pr-size-optimization)
6. [Pair & Mob Programming](#pair--mob-programming)
7. [AI-Assisted Code Review](#ai-assisted-code-review)
8. [Knowledge Sharing Through Reviews](#knowledge-sharing-through-reviews)
9. [Review Metrics & Continuous Improvement](#review-metrics--continuous-improvement)
10. [Trunk-Based Development & Review Flow](#trunk-based-development--review-flow)

---

## Code Review Philosophy

### Objectifs d'une code review

Hiérarchiser les objectifs d'une review (par ordre de priorité) :

1. **Détecter les bugs et erreurs logiques** : trouver ce que les tests automatisés ne captent pas.
2. **Assurer la maintenabilité** : le code sera-t-il compréhensible dans 6 mois par quelqu'un d'autre ?
3. **Partager la connaissance** : chaque review est une opportunité d'apprentissage bidirectionnel.
4. **Maintenir la cohérence** : respecter les conventions et patterns établis de l'équipe.
5. **Améliorer le design** : identifier les opportunités d'amélioration architecturale.

### Ce que la code review n'est PAS

- **Un gatekeeping** : la review n'est pas un outil de contrôle hiérarchique. Tout le monde review, tout le monde est reviewé.
- **Un formatage** : les questions de style et de formatage doivent être traitées par des outils automatiques (Prettier, Black, gofmt), pas par des humains.
- **Un examen** : ne pas utiliser la review pour évaluer la compétence du développeur.
- **Un goulot d'étranglement** : si les reviews bloquent le flux de travail, le processus doit être amélioré.

### La règle d'or

Reviewer le code comme on voudrait que le sien soit reviewé : avec respect, précision et bienveillance.

---

## The Review Process

### Workflow standard

```
Auteur                          Reviewer                        CI/CD
  │                                │                              │
  ├── Crée la PR ─────────────────>│                              │
  │   (description claire,         │                              │
  │    context, test plan)         │                              │
  │                                │                              │
  │                                │<──── Analyses automatiques ──┤
  │                                │      (lint, tests, coverage,  │
  │                                │       security scan, AI review)│
  │                                │                              │
  │                                ├── Review humaine ───>        │
  │                                │   (logique, design,          │
  │                                │    maintenabilité)           │
  │                                │                              │
  │<── Feedback ──────────────────┤                              │
  │                                │                              │
  ├── Adresse les retours ────────>│                              │
  │                                │                              │
  │                                ├── Approve ──────────────────>│
  │                                │                              │
  │<── Merge ──────────────────────┤──── Deploy ─────────────────>│
```

### Rôle de l'auteur de la PR

Avant de demander une review :

1. **Relire son propre code** : faire une self-review en utilisant la vue diff de la PR. Repérer les oublis, les commentaires de debug, les TODO oubliés.
2. **Écrire une description complète** :

```markdown
## What
Implémentation du système de discount codes pour le panier.

## Why
Requis par la feature JIRA-456. Les utilisateurs doivent pouvoir appliquer
des codes promo lors du checkout.

## How
- Ajout du modèle DiscountCode avec validation (expiration, minimum d'achat)
- Nouveau endpoint POST /api/cart/{id}/discount
- Validation via le DiscountValidator (strategy pattern)
- Tests : unitaires sur le validateur, intégration sur l'endpoint

## Test Plan
- [x] Tests unitaires : 12 cas couvrant tous les types de discount
- [x] Test d'intégration : endpoint avec base de données
- [ ] Test manuel : appliquer les codes SUMMER20, FLAT15, EXPIRED01

## Screenshots / Recordings
(si applicable pour les changements UI)

## Notes for Reviewer
Le DiscountValidator utilise le Strategy pattern car nous prévoyons
d'ajouter d'autres types de discount (combo, loyalty) au Q3.
Attention particulière à la gestion des arrondis dans Money.
```

3. **S'assurer que la CI est verte** avant de demander une review humaine.
4. **Tagger les bons reviewers** : au moins un expert du domaine concerné et un membre d'une autre équipe pour le knowledge sharing.

### Rôle du reviewer

1. **Répondre rapidement** : viser un temps de première réponse < 4 heures ouvrées. Le blocage d'une PR est un coût d'opportunité pour l'équipe.
2. **Comprendre le contexte** : lire la description de la PR et le ticket lié avant de regarder le code.
3. **Faire une première passe rapide** : comprendre la structure globale du changement avant de plonger dans les détails.
4. **Distinguer les niveaux de feedback** (voir section suivante).
5. **Approuver quand c'est "suffisamment bon"** : ne pas bloquer pour des améliorations optionnelles. La perfection est l'ennemie du progrès.

---

## Constructive Feedback

### La taxonomie des commentaires de review

Préfixer chaque commentaire avec son niveau pour éviter l'ambiguïté :

| Préfixe | Signification | Bloquant ? |
|---|---|---|
| `[blocker]` | Bug, faille de sécurité, perte de données | Oui |
| `[must-fix]` | Violation d'un standard d'équipe, maintenabilité critique | Oui |
| `[suggestion]` | Amélioration recommandée mais non bloquante | Non |
| `[nitpick]` | Détail cosmétique, préférence personnelle | Non |
| `[question]` | Demande de clarification, compréhension | Non |
| `[praise]` | Quelque chose de bien fait à souligner | Non |

### Formulation du feedback

#### Règles de communication

1. **Commenter le code, pas la personne** :
   - Non : "Tu n'as pas pensé aux edge cases"
   - Oui : `[suggestion] Ce calcul pourrait produire un NaN si quantity est 0. Considérer un guard clause.`

2. **Expliquer le pourquoi, pas juste le quoi** :
   - Non : "Utilise un Map ici"
   - Oui : `[suggestion] Un Map serait plus performant ici car la recherche par clé est O(1) vs O(n) pour le filter sur un Array, et ce code est dans un hot path appelé ~10k fois/requête.`

3. **Proposer une alternative concrète** :
   - Non : "Ce code est confus"
   - Oui : `[suggestion] Ce bloc serait plus lisible en extrayant une méthode :`
     ```typescript
     // plutôt que le inline complexe
     const eligibleUsers = users.filter(u => isEligibleForDiscount(u));
     ```

4. **Poser des questions ouvertes pour comprendre** :
   - `[question] Quelle est la raison de ce choix d'implémentation ? Il y a peut-être un contexte que je ne vois pas.`

5. **Valoriser ce qui est bien fait** :
   - `[praise] Excellent usage du Builder pattern pour les fixtures de test. Ça rend les tests très lisibles.`

### Le modèle "Observation - Impact - Suggestion"

Structurer le feedback en trois parties :

```
[suggestion] Le nom `data` pour cette variable ne révèle pas son contenu.
(Observation)

En lisant ce code dans 6 mois, il faudra remonter au contexte pour comprendre
ce que `data` contient, ce qui ralentit la compréhension.
(Impact)

Renommer en `unpaidInvoices` rendrait le code auto-documenté :
`const unpaidInvoices = await invoiceRepo.findUnpaid(since);`
(Suggestion)
```

### Gérer les désaccords

1. **Appliquer la "two-way door" rule** : si le choix est facilement réversible, accepter la décision de l'auteur. Réserver les escalades pour les décisions irréversibles (choix d'architecture, API publique).
2. **Limiter les allers-retours** : après 2 échanges sur un même point, proposer une discussion en direct (call, pair session) plutôt que de continuer en asynchrone.
3. **Définir un arbitre** : en cas de blocage, le tech lead ou l'architecte tranche.
4. **Documenter la décision** : créer un ADR (Architecture Decision Record) si le débat révèle un choix structurant non documenté.

---

## Review Checklists

### Checklist fonctionnelle

- [ ] Le code implémente correctement les exigences du ticket/story
- [ ] Les edge cases sont gérés (null, vide, limites, overflow)
- [ ] Les erreurs sont gérées proprement (pas de fail silencieux)
- [ ] Les messages d'erreur sont clairs et actionnables
- [ ] Les validations d'entrée sont présentes côté serveur (ne jamais faire confiance au client)

### Checklist design & maintenabilité

- [ ] Le code respecte les principes SOLID
- [ ] Les abstractions sont au bon niveau (ni trop, ni trop peu)
- [ ] Les noms révèlent l'intention (variables, fonctions, classes)
- [ ] Pas de duplication de logique métier
- [ ] La complexité cyclomatique est raisonnable (< 10 par fonction)
- [ ] Le code est cohérent avec les patterns existants du projet
- [ ] Les constantes magiques sont nommées

### Checklist sécurité

- [ ] Pas d'injection possible (SQL, XSS, command injection)
- [ ] Les données sensibles ne sont pas loguées
- [ ] L'authentification et l'autorisation sont vérifiées
- [ ] Les dépendances ajoutées n'ont pas de vulnérabilités connues
- [ ] Les secrets ne sont pas hardcodés

### Checklist performance

- [ ] Pas de requête N+1 vers la base de données
- [ ] Les requêtes BDD utilisent les index appropriés
- [ ] Pas de traitement O(n^2) sur des collections potentiellement grandes
- [ ] Le caching est utilisé quand approprié
- [ ] Les opérations I/O sont asynchrones quand possible

### Checklist testing

- [ ] Des tests couvrent les nouveaux comportements
- [ ] Les tests de non-régression existent pour les bugs corrigés
- [ ] Les tests sont lisibles et suivent le pattern AAA
- [ ] Les tests vérifient le comportement, pas l'implémentation
- [ ] Les edge cases sont testés

### Checklist observabilité

- [ ] Les logs sont présents aux points critiques (pas de sur-logging)
- [ ] Les métriques business et techniques sont émises
- [ ] Les erreurs sont tracées avec le contexte suffisant pour le debug

---

## PR Size Optimization

### Pourquoi la taille compte

Les études (SmartBear, Google Engineering Practices) montrent une corrélation directe entre la taille de la PR et la qualité de la review :

| Taille du diff | Temps de review | Taux de détection de bugs |
|---|---|---|
| < 200 lignes | 15-30 min | Élevé (détection fine) |
| 200-400 lignes | 30-60 min | Bon |
| 400-800 lignes | 60-90 min | Dégradé (fatigue du reviewer) |
| > 800 lignes | 90+ min | Très faible ("LGTM" aveugle) |

**Règle** : viser des PRs de 200-400 lignes de diff. Au-delà de 400 lignes, découper.

### Stratégies de découpage

#### Stacked PRs

Créer une chaîne de PRs dépendantes, chacune reviewable indépendamment :

```
PR 1: Ajouter le modèle DiscountCode et le repository (100 lignes)
  ↓
PR 2: Implémenter le DiscountValidator avec ses tests (150 lignes)
  ↓
PR 3: Ajouter l'endpoint API et les tests d'intégration (200 lignes)
  ↓
PR 4: Intégrer le discount dans le flow de checkout (180 lignes)
```

Outils : `git-branchless`, `graphite`, `ghstack` pour gérer les stacked PRs efficacement.

#### Découpage par type de changement

Séparer dans des PRs distinctes :
- **Refactoring préparatoire** : PR de refactoring pur (aucun changement de comportement) avant la PR de feature.
- **Infrastructure vs logique** : séparer la configuration (migrations, routes) de la logique métier.
- **Tests d'abord** : une PR pour les tests (qui documentent le comportement attendu), puis une PR pour l'implémentation.

#### Le flag "draft" pour les grandes migrations

Pour les changements inévitablement grands (migration de framework, renommage massif), ouvrir une PR draft avec une description expliquant la stratégie, et demander une review de la stratégie avant de finaliser.

---

## Pair & Mob Programming

### Pair Programming

Deux développeurs travaillent sur le même code simultanément. Un pilote (driver) code, un navigateur (navigator) observe, questionne et guide.

#### Quand pratiquer le pair programming

| Situation | Pair recommandé ? |
|---|---|
| Onboarding d'un nouveau membre | Oui (expert + nouveau) |
| Code complexe ou critique | Oui |
| Bug difficile à reproduire | Oui |
| Tâche routinière et bien comprise | Non |
| Exploration / spike | Oui (perspectives croisées) |
| Review asynchrone qui s'éternise | Oui (remplacer par une session pair) |

#### Styles de pair programming

- **Driver-Navigator** : le classique. Le navigator pense à la stratégie pendant que le driver implémente.
- **Ping-Pong** (avec TDD) : A écrit un test, B le fait passer et écrit le test suivant. Excellent pour le TDD.
- **Strong-style** : "Pour qu'une idée passe du cerveau au clavier, elle doit passer par la bouche de quelqu'un d'autre." Le navigateur dicte, le driver implémente.

### Mob Programming

L'équipe entière (3-6 personnes) travaille sur le même code en même temps. Un driver tourne toutes les 10-15 minutes.

#### Quand pratiquer le mob programming

- Décisions architecturales impactantes
- Résolution d'incidents critiques en production
- Développement de conventions et patterns d'équipe
- Formation collective sur un nouveau framework ou pattern

#### Avantages du mob programming

- **Zéro review nécessaire** : le code est reviewé en temps réel par toute l'équipe.
- **Knowledge sharing maximal** : tous les membres comprennent tout le code.
- **Décisions collectives** : les débats de design sont résolus en temps réel.
- **Onboarding accéléré** : les nouveaux apprennent en observant et en participant.

---

## AI-Assisted Code Review

### Outils disponibles (2024-2026)

| Outil | Type | Forces |
|---|---|---|
| GitHub Copilot Code Review | Intégré à GitHub PR | Détection de bugs, suggestions d'amélioration, contexte du repo |
| CodeRabbit | Bot PR autonome | Reviews détaillées, diagrammes de séquence, résumés |
| Sourcery | Refactoring suggestions | Suggestions de refactoring Python/JS, métriques qualité |
| Amazon CodeGuru | AWS-natif | Détection de problèmes de performance et sécurité |
| SonarQube + AI | Analyse statique augmentée | Règles augmentées par ML, détection de patterns complexes |
| Claude / ChatGPT | Review manuelle assistée | Analyse contextuelle profonde, explication de code legacy |

### Stratégie d'intégration de l'IA dans le processus de review

```
Flux optimisé :

1. Auteur pousse la PR
   │
2. CI/CD s'exécute (lint, tests, coverage)
   │
3. Bot IA génère une première review automatique
   │  ├── Résumé du changement
   │  ├── Bugs potentiels détectés
   │  ├── Suggestions de refactoring
   │  ├── Vérification des conventions
   │  └── Score de complexité/risque
   │
4. L'auteur adresse les retours automatiques
   │
5. Le reviewer humain se concentre sur :
   │  ├── La logique métier (que l'IA comprend mal)
   │  ├── Les choix de design et d'architecture
   │  ├── L'adéquation avec la vision technique
   │  └── Le partage de connaissances
   │
6. Merge
```

### Ce que l'IA fait bien

- Détecter les null pointer exceptions, les off-by-one, les race conditions triviales.
- Vérifier la conformité aux conventions de coding style.
- Identifier le code mort et les imports inutilisés.
- Résumer les changements d'une PR volumineuse.
- Suggérer des noms de variables/méthodes plus expressifs.
- Détecter les vulnérabilités de sécurité connues (OWASP patterns).

### Ce que l'IA fait mal (et qui nécessite un humain)

- Comprendre l'intention métier derrière le code.
- Évaluer si le design est cohérent avec la vision architecturale du projet.
- Juger du bon niveau d'abstraction.
- Détecter les problèmes de performance liés au contexte d'exécution spécifique.
- Vérifier que le code résout effectivement le problème du ticket.
- Questionner les exigences elles-mêmes.

### Garde-fous pour l'utilisation de l'IA

1. **Ne jamais remplacer la review humaine** par l'IA seule. L'IA est un filtre de premier niveau, pas un décideur.
2. **Configurer l'IA pour le contexte du projet** : conventions spécifiques, patterns préférés, dépendances interdites.
3. **Valider les suggestions de l'IA** : elle peut halluciner des patterns inexistants ou recommander des bibliothèques obsolètes.
4. **Mesurer le taux de faux positifs** : trop de bruit tue la confiance. Ajuster les seuils de sensibilité.

---

## Knowledge Sharing Through Reviews

### La review comme outil d'apprentissage

Transformer chaque review en opportunité de partage de connaissances :

#### Pour les juniors (reviewés par des seniors)

- Le reviewer explique le "pourquoi" des suggestions, pas juste le "quoi".
- Pointer vers la documentation interne, les ADR, les exemples existants dans le codebase.
- Proposer des pairings pour les changements complexes plutôt que de rewriter dans les commentaires.

#### Pour les seniors (reviewés par des juniors)

- Encourager les questions : "N'hésite pas à demander si quelque chose n'est pas clair."
- Demander explicitement des reviews à des juniors pour les impliquer et les former.
- Expliquer les patterns utilisés dans la description de la PR.

#### Pour le cross-team knowledge

- Inviter un reviewer d'une autre équipe pour les PRs touchant des zones partagées.
- Maintenir un "review rotation" pour que chaque membre de l'équipe review des domaines différents.
- Créer des "review guilds" thématiques (sécurité, performance, accessibilité).

### Documentation émergente des reviews

Extraire les patterns récurrents des reviews pour créer de la documentation :

1. Quand le même feedback apparaît > 3 fois dans des reviews → créer une règle de linter ou un snippet de documentation.
2. Quand un débat de design est tranché dans une review → créer un ADR.
3. Quand un pattern est expliqué dans une review → l'ajouter au wiki/handbook technique de l'équipe.

---

## Review Metrics & Continuous Improvement

### Métriques clés

| Métrique | Cible | Comment mesurer |
|---|---|---|
| Time to first review | < 4h ouvrées | GitHub/GitLab analytics |
| Review cycles (allers-retours) | < 3 cycles | Nombre de re-reviews avant merge |
| PR size (lignes de diff) | 200-400 | PR analytics, repo insights |
| PR lead time (ouverture → merge) | < 24h ouvrées | GitHub/GitLab analytics |
| Review coverage | 100% des PRs | Merge rules / branch protection |
| Escaped defects | Tendance décroissante | Bugs en production liés à du code récent |

### Rétrospective du processus de review

Conduire une rétrospective trimestrielle sur le processus de review :

- Quelles PRs ont pris le plus de temps et pourquoi ?
- Quels types de bugs passent encore malgré les reviews ?
- Le feedback est-il constructif et utile ?
- Les outils automatiques (IA, linters) sont-ils correctement calibrés ?
- Y a-t-il des goulots d'étranglement (certaines personnes taguées sur toutes les PRs) ?

### Anti-patterns de review à surveiller

| Anti-pattern | Symptôme | Solution |
|---|---|---|
| Rubber-stamping | "LGTM" en 30 secondes sur une PR de 500 lignes | Rappeler les objectifs de la review, réduire la taille des PRs |
| Nitpick hell | 30 commentaires cosmétiques, 0 sur la logique | Automatiser le formatage, préfixer les commentaires |
| Gatekeeping | Un seul "architecte" approuve toutes les PRs | Distribuer l'ownership, CODEOWNERS rotatif |
| Review ping-pong | 5+ cycles de review sans convergence | Switch vers une session pair/mob après 2 cycles |
| Stale PRs | PRs ouvertes > 1 semaine | Limiter le WIP, alertes automatiques |

---

## Trunk-Based Development & Review Flow

### Adapter la review au trunk-based development

Dans un workflow trunk-based, les branches vivent moins de 24h. Adapter le processus de review :

1. **PRs courtes et fréquentes** : fusionner 2-3 fois par jour plutôt qu'une PR massive en fin de sprint.
2. **Review rapide obligatoire** : si personne n'a reviewé en 2h, le pair du moment approuve.
3. **Feature flags** : le code peut être mergé dans le trunk même incomplet, tant qu'il est derrière un flag.
4. **Ship/Show/Ask** (Rouan Wilsenach) :
   - **Ship** : changements triviaux (typo, config) → merge direct sans review.
   - **Show** : changements standards → merge puis review asynchrone post-merge.
   - **Ask** : changements complexes ou risqués → review avant merge (PR classique).

### Pre-commit reviews vs Post-commit reviews

| Approche | Avantages | Inconvénients |
|---|---|---|
| Pre-commit (PR classique) | Bugs détectés avant merge, qualité garantie | Bloquant, latence, goulot d'étranglement |
| Post-commit (review après merge) | Non bloquant, vélocité élevée | Bugs en trunk temporairement, rollback nécessaire |
| Hybrid (Ship/Show/Ask) | Adapté au risque, flexible | Nécessite maturité de l'équipe pour bien classifier |

### Automatiser la classification des PRs

```yaml
# Exemple de configuration CODEOWNERS + labeling automatique
# .github/auto-label.yml
labels:
  - label: "review:ship"
    paths:
      - "docs/**"
      - "*.md"
      - ".github/**"
    max_diff_lines: 50

  - label: "review:show"
    paths:
      - "src/**"
    max_diff_lines: 200
    exclude_paths:
      - "src/core/**"
      - "src/auth/**"

  - label: "review:ask"
    paths:
      - "src/core/**"
      - "src/auth/**"
      - "infrastructure/**"
    # Ou si > 400 lignes de diff
    min_diff_lines: 400
```

---

## Summary Checklist

Vérifier ces points pour le processus de code review de l'équipe :

- [ ] Chaque PR a une description complète (What/Why/How/Test Plan)
- [ ] Les PRs font 200-400 lignes de diff maximum
- [ ] Les commentaires de review sont préfixés par leur niveau (blocker/suggestion/nitpick/praise)
- [ ] Le feedback est formulé sur le code, pas sur la personne
- [ ] Le time to first review est < 4h ouvrées
- [ ] Les outils automatiques (linters, IA) filtrent les problèmes mécaniques
- [ ] Le reviewer humain se concentre sur la logique, le design et le partage de connaissances
- [ ] Le pair/mob programming est utilisé comme alternative pour les sujets complexes
- [ ] Les patterns récurrents de review sont transformés en règles automatiques ou documentation
- [ ] Le processus de review est rétrospectif trimestriellement
- [ ] La review est un outil d'apprentissage, pas de gatekeeping
