# UX Metrics & Testing -- Mesurer l'Experience Utilisateur

## Overview

Ce document de reference couvre la mesure systematique de l'experience utilisateur : metriques attitudinales (SUS, NPS, CSAT, CES), metriques comportementales (Task Success Rate, Time on Task, Error Rate), frameworks (HEART de Google), evaluation heuristique (Nielsen), accessibilite (WCAG 2.1/2.2), et benchmarking UX. Utiliser ce guide pour concevoir un programme de mesure UX rigoureux, interpreter les resultats et piloter l'amelioration continue.

---

## System Usability Scale (SUS)

Questionnaire standardise de 10 items (Brooke, 1986). Mesure l'utilisabilite percue sur une echelle de 0 a 100. Echelle de Likert 1-5 par item. Items impairs : positifs. Items pairs : negatifs.

| # | Question | Polarite |
|---|----------|----------|
| 1 | Je pense que j'aimerais utiliser ce systeme frequemment | + |
| 2 | J'ai trouve ce systeme inutilement complexe | - |
| 3 | J'ai trouve ce systeme facile a utiliser | + |
| 4 | Je pense que j'aurais besoin de l'aide d'un technicien pour utiliser ce systeme | - |
| 5 | J'ai trouve que les differentes fonctions etaient bien integrees | + |
| 6 | J'ai trouve qu'il y avait trop d'incoherences dans ce systeme | - |
| 7 | Je pense que la plupart des gens apprendraient a utiliser ce systeme tres rapidement | + |
| 8 | J'ai trouve ce systeme tres contraignant a utiliser | - |
| 9 | Je me suis senti(e) tres a l'aise en utilisant ce systeme | + |
| 10 | J'ai du apprendre beaucoup de choses avant de pouvoir utiliser ce systeme | - |

**Calcul** : Items impairs : score = reponse - 1. Items pairs : score = 5 - reponse. Somme x 2.5 = score SUS (0-100).

```
SUS = [(R1-1) + (5-R2) + (R3-1) + (5-R4) + (R5-1) + (5-R6) + (R7-1) + (5-R8) + (R9-1) + (5-R10)] x 2.5
```

**Interpretation** (echelle Sauro) : A+ (84.1-100) excellente | A (80.8-84.0) tres bonne | B (71.4-80.7) bonne | C (62.7-71.3) moyenne | D (51.7-62.6) mediocre | F (< 51.7) inacceptable. Score moyen global : 68.

**Benchmarks par industrie** : Apps mobile grand public 72-78 | SaaS B2B 65-72 | E-commerce 68-75 | Logiciels enterprise 55-65 | Sites gouvernementaux 50-62 | Applications medicales 58-68.

---

## Net Promoter Score (NPS)

**Question** : "Sur une echelle de 0 a 10, quelle est la probabilite que vous recommandiez [Produit] a un collegue ou ami ?"

| Segment | Score | Comportement typique |
|---------|-------|----------------------|
| **Promoteurs** | 9-10 | Fideles, evangelisent, retention > 90% |
| **Passifs** | 7-8 | Satisfaits mais vulnerables aux concurrents |
| **Detracteurs** | 0-6 | Insatisfaits, risque de churn eleve, bouche-a-oreille negatif |

**Calcul** : NPS = % Promoteurs - % Detracteurs. Plage : -100 a +100.

| Industrie | NPS median | Bon | Excellent |
|-----------|-----------|-----|-----------|
| SaaS B2B | 36 | > 40 | > 60 |
| E-commerce | 45 | > 50 | > 70 |
| Services financiers | 28 | > 35 | > 50 |
| Telecom | 15 | > 25 | > 40 |
| Sante | 30 | > 40 | > 55 |

**Questions de suivi** : toujours accompagner d'une question ouverte segmentee. Detracteurs : "Qu'est-ce qui vous a le plus decu ?" Passifs : "Que faudrait-il ameliorer pour que vous nous recommandiez ?" Promoteurs : "Qu'appreciez-vous le plus ?" Analyser par theme et frequence.

---

## Customer Satisfaction Score (CSAT)

**Question** : "Comment evaluez-vous votre satisfaction concernant [interaction specifique] ?" (echelle 1-5 ou 1-7). **Calcul** : CSAT = (reponses 4-5 / total) x 100.

| Moment de mesure | Delai optimal | Canal | Cible |
|------------------|---------------|-------|-------|
| Post-ticket support | < 2h | Email / Widget | > 85% |
| Post-onboarding | J7-J30 | Email | > 80% |
| Post-achat | J1-J3 | Email / SMS | > 80% |
| Post-feature usage | Apres 3e utilisation | In-app | > 75% |

**CSAT vs NPS** : le CSAT mesure la satisfaction transactionnelle (court terme, haute actionabilite). Le NPS mesure la loyaute relationnelle (moyen terme, vue strategique). Utiliser le CSAT pour optimiser les touchpoints, le NPS pour piloter la strategie CX globale.

---

## Customer Effort Score (CES)

**Question** : "[Entreprise] a rendu facile la resolution de mon probleme." (echelle 1-7). **Calcul** : CES = moyenne des reponses.

**Quand utiliser** : post-interaction support, apres processus complexe (onboarding, migration, integration API), apres parcours self-service. Le CES est le meilleur predicteur de fidelite (Dixon, "The Effortless Experience") : 96% des clients a fort effort deviennent infideles vs 9% a faible effort.

| Score CES | Interpretation | Action |
|-----------|----------------|--------|
| 6.0-7.0 | Effort minimal | Documenter et repliquer |
| 5.0-5.9 | Acceptable | Eliminer les micro-frictions |
| 4.0-4.9 | Modere | Analyser les causes, simplifier |
| 3.0-3.9 | Eleve | Revoir le processus en profondeur |
| 1.0-2.9 | Extreme | Intervention immediate, redesign |

---

## Task Success Rate

Le TSR mesure le pourcentage d'utilisateurs completant une tache avec succes. **Succes binaire** : TSR = (taches reussies / tentatives) x 100. **Succes partiel** : 1.0 (complet sans aide) | 0.5 (complet avec difficulte) | 0.0 (echec/abandon).

| Type de tache | TSR moyen | Cible |
|---------------|-----------|-------|
| Navigation simple | 85-90% | > 90% |
| Formulaire | 75-85% | > 85% |
| Transaction | 70-80% | > 80% |
| Configuration | 60-75% | > 75% |
| Workflow multi-etapes | 50-70% | > 70% |

5 utilisateurs identifient ~85% des problemes d'utilisabilite. 15-20 utilisateurs pour des mesures quantitatives fiables.

---

## Time on Task

Mesure le temps necessaire pour completer une tache. Types : temps absolu, temps relatif (A vs B), temps d'expert (ratio novice/expert = courbe d'apprentissage).

**Gestion des outliers** : les donnees suivent une distribution log-normale. Retirer les abandons du calcul. Utiliser la mediane plutot que la moyenne. Exclure les valeurs > 3 ecarts-types. Reporter mediane et moyenne geometrique.

**Comparaison** : Amelioration (%) = [(Temps_ancien - Temps_nouveau) / Temps_ancien] x 100. Test t avec alpha = 0.05. Un gain > 20% est pratiquement significatif.

---

## Error Rate

**Slips (lapsus)** : action correcte mal executee par inattention (clic mauvais bouton, faute de frappe). Cause : interface dense, boutons trop proches. **Mistakes** : plan d'action incorrect par incomprehension (mauvaise option, terminologie ambigue). Cause : architecture confuse, modele mental incompatible.

| Niveau | Severite | Description | Action |
|--------|----------|-------------|--------|
| 0 | Cosmetique | Sans impact fonctionnel | Corriger si possible |
| 1 | Mineure | Ralentit l'utilisateur | Sprint prochain |
| 2 | Majeure | Bloque temporairement | Sprint en cours |
| 3 | Critique | Empeche la completion | Corriger immediatement |
| 4 | Catastrophique | Perte de donnees / securite | Hotfix urgent |

**Calculs** : Error Rate par tache = (erreurs / opportunites d'erreur) x 100. Error Rate par utilisateur = (utilisateurs avec erreur / total utilisateurs) x 100. Error Frequency = total erreurs / total utilisateurs.

---

## HEART Framework (Google)

Developpe par Rodden, Hutchinson et Fu (Google). Cinq dimensions centrees utilisateur, chacune declinee via le processus GSM (Goals, Signals, Metrics).

| Dimension | Description | Goal (exemple SaaS) | Metric |
|-----------|-------------|---------------------|--------|
| **Happiness** | Satisfaction subjective | Produit percu comme facile | SUS > 72, CSAT > 85% |
| **Engagement** | Implication dans le produit | Usage quotidien | DAU/MAU > 40%, > 5 actions/session |
| **Adoption** | Nouveaux utilisateurs/features | Activation des features cles | Taux activation > 60% a J7 |
| **Retention** | Utilisateurs actifs dans le temps | Retention a 90 jours | Retention J90 > 40% |
| **Task success** | Completion des taches | Workflows completes sans erreur | TSR > 85%, Error Rate < 5% |

**Processus GSM** : 1. Goals -- definir l'objectif pour chaque dimension. 2. Signals -- identifier les comportements/attitudes observables. 3. Metrics -- traduire les signaux en metriques mesurables.

---

## Evaluation Heuristique (Nielsen)

### Les 10 heuristiques

1. **Visibilite de l'etat du systeme** : feedback immediat (chargement, confirmation, etat actuel).
2. **Correspondance systeme/monde reel** : terminologie utilisateur, pas jargon technique.
3. **Controle et liberte** : Annuler, Retour, Undo/Redo toujours accessibles.
4. **Coherence et standards** : coherence interne (termes, couleurs) et externe (conventions plateforme).
5. **Prevention des erreurs** : validation en temps reel, confirmations destructrices, valeurs par defaut.
6. **Reconnaissance plutot que rappel** : options visibles, historique, suggestions contextuelles.
7. **Flexibilite et efficacite** : raccourcis clavier, personnalisation, actions en lot.
8. **Design minimaliste** : hierarchie visuelle, progressive disclosure, pas de bruit.
9. **Aide au diagnostic des erreurs** : messages en langage clair, cause + solution, pres du champ.
10. **Aide et documentation** : tooltips, documentation cherchable, tutoriels integres.

### Severite et processus

| Niveau | Severite | Action |
|--------|----------|--------|
| 0 | Pas un probleme | Aucune |
| 1 | Cosmetique | Backlog basse priorite |
| 2 | Mineur | Sprint prochain |
| 3 | Majeur | Sprint en cours, priorite haute |
| 4 | Catastrophe | Bloquant, correction immediate |

**Processus** : 3-5 evaluateurs independants. Evaluation individuelle (heuristique violee, severite 0-4, localisation, recommandation). Consolidation et deduplication. Rapport par severite decroissante. Suivi des severites 3-4 dans le backlog. Utiliser en phase de conception, avant tests utilisateurs, lors d'audits UX, pour evaluer un concurrent.

---

## Accessibility Testing

### WCAG 2.1 / 2.2 -- Quatre principes (POUR)

| Principe | Exemples de criteres |
|----------|---------------------|
| **Perceptible** | Alt text images, sous-titres videos, contraste 4.5:1 minimum |
| **Operable** | Navigation clavier, delais suffisants, pas de clignotement |
| **Understandable** | Langage clair, comportement previsible, aide a la saisie |
| **Robust** | HTML semantique, ARIA roles, compatibilite lecteurs d'ecran |

Niveaux : A (minimum) | AA (standard recommande, obligation legale EU 2025) | AAA (excellence).

### Tests automatises vs manuels

| Aspect | Automatises | Manuels |
|--------|-------------|---------|
| Couverture WCAG | ~30-40% | ~100% |
| Outils | axe, WAVE, Lighthouse, Pa11y | Screen readers, navigation clavier |
| Quand | CI/CD, chaque commit | Releases majeures, audits |

### Screen readers a tester

NVDA (Windows, ~30%) | JAWS (Windows, ~40%) | VoiceOver (macOS/iOS, ~25%) | TalkBack (Android, ~5%). Verifier : elements interactifs annonceables, ordre de lecture logique, ARIA live regions, labels formulaires, en-tetes tableaux, alt text images.

### Problemes les plus courants

Contraste insuffisant (ratio < 4.5:1) | Alt text manquant | Focus non visible | Formulaires sans labels | Navigation clavier impossible | ARIA mal utilise (preferer HTML semantique).

---

## Benchmarking UX

### Competitive Benchmarking

1. Selectionner 3-5 concurrents directs + 1-2 best-in-class hors secteur. 2. Definir 5-8 taches cles. 3. Recruter 10-15 participants par produit. 4. Mesurer TSR, Time on Task, Error Rate, SUS, SEQ (Single Ease Question, 1-7). 5. Comparer dans un tableau.

### Suivi longitudinal et objectifs

Tracker trimestriellement (SUS, NPS) et en continu (metriques comportementales). Une amelioration de +5 SUS ou +10% TSR entre deux vagues est significative.

| Metrique | Baseline | Objectif 6 mois | Objectif 12 mois |
|----------|----------|-----------------|------------------|
| SUS | 65 | 72 | 78 |
| TSR | 75% | 82% | 88% |
| NPS | 25 | 35 | 45 |
| Error Rate | 12% | 8% | 5% |
| CES | 4.5 | 5.2 | 5.8 |

---

## UX Metrics Dashboard

### Metriques et cadence

| Categorie | Metrique | Source | Cadence |
|-----------|---------|--------|---------|
| Attitudinal | SUS | Enquete post-test | Trimestrielle |
| Attitudinal | NPS | Enquete relationnelle | Trimestrielle |
| Attitudinal | CSAT, CES | Post-interaction | Continue |
| Comportemental | TSR, Time on Task | Tests utilisateurs / Analytics | Trimestrielle |
| Comportemental | Error Rate | Analytics / Session replay | Mensuelle |
| Engagement | DAU/MAU, Feature adoption | Product analytics | Hebdo/Mensuelle |
| Retention | J7/J30/J90 | Product analytics | Mensuelle |
| Accessibilite | Lighthouse a11y + Audit WCAG | CI/CD + Audit manuel | Release / Semestrielle |

### Outils

| Outil | Usage | Prix indicatif |
|-------|-------|----------------|
| **Hotjar / Clarity** | Heatmaps, recordings, feedback | 0-100 EUR/mois |
| **Amplitude / Mixpanel** | Product analytics, funnels, retention | 0-2K EUR/mois |
| **Maze / UserTesting** | Tests a distance, metriques UX | 200-2K EUR/mois |
| **axe / Lighthouse** | Tests accessibilite automatises | Gratuit |
| **Qualtrics / Typeform** | Enquetes NPS, CSAT, CES, SUS | 50-500 EUR/mois |

### Reporting aux stakeholders

Executive (C-level) : slide deck 3-5 pages, tendances KPIs cles, trimestriel. Product Management : dashboard interactif, metriques par feature, mensuel. Design/Engineering : rapport detaille, problemes + severite + recommandations, par sprint. Support/CS : tableau operationnel CSAT/CES/themes, hebdomadaire.

---

## State of the Art 2025-2026

### Real-Time UX Monitoring

Le passage de la mesure periodique a la surveillance en temps reel est le shift majeur 2025-2026. Les plateformes (FullStory, Quantum Metric, Glassbox) detectent automatiquement les "frustration signals" : rage clicks, dead clicks, erreurs JS, thrashing, retours arriere repetes. Ces signaux declenchent des alertes automatiques. Les "Digital Experience Scores" (DXS) fournissent un indicateur unique de sante UX actualise en temps reel. Seuil d'alerte : si le DXS chute de > 5% post-release, envisager un rollback.

### AI-Detected Usability Issues

Les LLM multimodaux analysent session recordings et captures d'ecran pour detecter automatiquement des violations d'heuristiques, des problemes d'accessibilite et des patterns de confusion. Capacites 2025-2026 : detection automatique de friction (parcours d'hesitation, abandons), analyse heuristique automatisee contre les 10 heuristiques de Nielsen, clustering de comportements (power users vs utilisateurs en difficulte), synthese automatique des sessions de test (transcription, codage thematique).

### Sentiment Analysis

L'analyse de sentiment sur les feedbacks UX (enquetes, avis, tickets) atteint 88-92% de precision grace aux LLM specialises. Extraction automatique des themes recurrents, du sentiment par theme, de l'urgence percue et des suggestions d'amelioration. La boucle retour passe de semaines (analyse manuelle) a minutes (analyse IA), permettant de quantifier le qualitatif a grande echelle et de prioriser sur des donnees massives.

### Convergence UX Research et Product Analytics

La frontiere quali/quanti s'estompe. Les plateformes 2025-2026 combinent session replays, product analytics, enquetes in-app, tests d'utilisabilite et analyse IA dans un meme outil, passant de l'observation ("les utilisateurs cliquent ici") a la comprehension ("parce qu'ils cherchent X").