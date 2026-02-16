---
name: automatisation-workflows
description: This skill should be used when the user asks about "workflow automation", "N8N", "Power Automate", "Zapier", "Make", "Integromat", "IFTTT", "no-code automation", "API integration", "webhook automation", "automated workflows", "business process automation", "RPA", "trigger action", "automatisation des processus", "flux de travail automatisés", "intégration d'applications", "orchestration de workflows", "automatisation sans code", "connecteurs API", "scheduling automation", "error handling workflows", "multi-step automation", discusses workflow automation platforms, API integrations, or needs guidance on automating business processes without code.
version: 1.0.0
last_updated: 2026-02
---

# Automatisation de Workflows / Workflow Automation

## Overview

Ce skill couvre l'ensemble des pratiques, outils et architectures lies a l'automatisation des workflows et des processus metier. Il fournit un cadre structure pour concevoir, deployer et maintenir des flux automatises a l'aide de plateformes no-code et low-code telles que N8N, Power Automate, Zapier, Make (ex-Integromat) et IFTTT, ainsi que des patterns d'integration API, de gestion des webhooks et d'orchestration de processus. L'automatisation de workflows est LE multiplicateur de productivite : chaque tache repetitive executee manuellement est une candidate a l'automatisation. L'objectif n'est pas d'automatiser pour le plaisir de la technique, mais d'eliminer systematiquement les frictions, les erreurs humaines et les latences dans les processus, en liberant du temps pour les taches a haute valeur ajoutee. Appliquer systematiquement les principes decrits ici pour evaluer chaque opportunite d'automatisation, choisir la plateforme adaptee, concevoir des workflows fiables et les maintenir dans la duree. Integrer les avancees recentes : agents autonomes, creation de workflows en langage naturel, automatisation pilotee par l'IA et architectures event-driven composables.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Integration entre applications** : connecter des outils SaaS (CRM, ERP, messagerie, stockage, facturation) pour synchroniser automatiquement les donnees entre systemes.
- **Automatisation de processus repetitifs** : eliminer les taches manuelles recurrentes (copier-coller entre outils, mise a jour de tableaux, creation de fichiers, envois d'emails).
- **Notifications et alertes** : configurer des alertes conditionnelles basees sur des evenements metier (nouveau lead, paiement recu, seuil depasse, erreur detectee).
- **Synchronisation de donnees** : maintenir la coherence des donnees entre plusieurs systemes en temps reel ou en batch (CRM <-> facturation, RH <-> paie).
- **Generation de rapports automatiques** : agreger des donnees de sources multiples et generer des rapports periodiques sans intervention manuelle.
- **Onboarding et offboarding** : automatiser les flux d'accueil et de depart (creation de comptes, envoi de documents, attribution de licences, revocation d'acces).
- **Lead management et nurturing** : automatiser le routage des leads, le scoring, les sequences de follow-up et la qualification automatique.
- **Document routing et approbations** : automatiser les circuits de validation, la generation de documents et l'archivage structure.
- **Scheduling et orchestration** : planifier des taches recurrentes, orchestrer des sequences multi-etapes et gerer des dependances entre workflows.

## Core Principles

### Principle 1 — Automate the Repetitive First

Prioriser l'automatisation des taches executees frequemment et a faible complexite. Utiliser la matrice frequence x complexite pour identifier les quick wins : les taches executees plus de 5 fois par semaine avec moins de 3 etapes sont les premieres candidates. Ne pas commencer par les processus complexes — construire de la confiance et de l'expertise avec des automatisations simples avant de passer a l'echelle.

### Principle 2 — Start Simple, Then Iterate

Concevoir le premier workflow comme un MVP : une seule integration, un seul trigger, une action principale. Valider le fonctionnement, mesurer le gain, puis enrichir progressivement (ajout de conditions, de branches, de gestion d'erreurs). Un workflow imparfait qui tourne est infiniment plus utile qu'un workflow parfait qui n'existe que sur papier.

### Principle 3 — Error Handling by Design

Ne jamais deployer un workflow sans gestion d'erreurs. Chaque etape doit prevoir ce qui se passe en cas d'echec : retry automatique, notification d'erreur, fallback vers un processus manuel, logging dans un canal dedie. Un workflow sans error handling est une bombe a retardement — il echouera silencieusement et les consequences ne seront decouvertes que trop tard.

### Principle 4 — Idempotency & Reliability

Concevoir chaque workflow pour etre idempotent : son execution multiple avec les memes donnees d'entree doit produire le meme resultat sans effets de bord indesirables. Utiliser des identifiants uniques pour la deduplication, verifier l'existence avant la creation, et utiliser des operations upsert plutot que des inserts aveugles. L'idempotence est la cle de la fiabilite dans un monde ou les webhooks peuvent etre declenches plusieurs fois.

### Principle 5 — Monitor Everything

Chaque workflow en production doit etre monitore : nombre d'executions, taux de succes/echec, duree moyenne, volume de donnees traitees. Configurer des alertes sur les anomalies (echecs repetes, duree anormalement longue, absence d'execution attendue). Sans monitoring, il est impossible de detecter les regressions, d'optimiser les performances et de justifier l'investissement en automatisation.

### Principle 6 — Security & Least Privilege

Appliquer le principe du moindre privilege a chaque connexion et chaque credential. Chaque workflow ne doit acceder qu'aux donnees et actions strictement necessaires a son fonctionnement. Utiliser des comptes de service dedies, des tokens scopes, et des secrets managers. Ne jamais hardcoder des credentials dans les workflows. Auditer regulierement les permissions accordees aux automatisations.

## Key Frameworks & Methods

### Automation Opportunity Matrix

Evaluer chaque tache candidate a l'automatisation selon deux axes : frequence d'execution et complexite de la tache.

| | Complexite faible (1-3 etapes) | Complexite moyenne (4-8 etapes) | Complexite elevee (9+ etapes) |
|---|---|---|---|
| **Haute frequence (quotidien+)** | Automatiser immediatement (Quick Win) | Automatiser en priorite | Automatiser par phases |
| **Frequence moyenne (hebdo)** | Automatiser en sprint 2 | Evaluer ROI avant d'automatiser | Prototype puis decision |
| **Basse frequence (mensuel-)** | Automatiser si trivial | Documenter d'abord, automatiser ensuite | Garder en manuel (ROI insuffisant) |

### Trigger-Action-Condition Model

Tout workflow repose sur le modele TAC :

- **Trigger (Declencheur)** : l'evenement qui demarre le workflow. Types : webhook (temps reel), polling (periodique), schedule (cron), manuel, evenement interne.
- **Condition (Filtre)** : la logique de filtrage qui determine si le workflow doit continuer. Permet d'eviter les executions inutiles et de router vers les bonnes branches.
- **Action (Execution)** : l'operation realisee par le workflow. Types : CRUD sur une API, envoi de notification, transformation de donnees, creation de document, mise a jour de base de donnees.

### Workflow Architecture Patterns

| Pattern | Description | Cas d'usage | Complexite |
|---|---|---|---|
| **Lineaire** | Sequence d'actions executees dans l'ordre | Email -> CRM -> Notification | Faible |
| **Branching (conditionnel)** | Chemins differents selon des conditions | Si montant > 1000 EUR -> approbation manuelle | Moyenne |
| **Parallele** | Actions executees simultanement | Notification Slack + Email + Log simultanes | Moyenne |
| **Boucle (iterateur)** | Repetition d'une action sur une liste | Traiter chaque ligne d'un CSV | Moyenne |
| **Saga** | Sequence avec compensation en cas d'echec | Creation compte + licence + notification avec rollback | Elevee |
| **Event-driven** | Workflows declenches par des evenements | Event bus -> multiple workflows independants | Elevee |

### Platform Selection Framework

| Critere | N8N | Power Automate | Zapier | Make (Integromat) |
|---|---|---|---|---|
| **Modele** | Self-hosted / Cloud | Cloud (Microsoft) | Cloud | Cloud |
| **Prix** | Gratuit (self-hosted) / a partir de 20 EUR/mois | A partir de 15 EUR/user/mois | A partir de 20 USD/mois | A partir de 10 USD/mois |
| **Nombre de connecteurs** | 400+ nodes | 1000+ connecteurs | 7000+ apps | 1500+ modules |
| **Complexite des workflows** | Tres elevee (sub-workflows, code custom) | Elevee (desktop flows, AI Builder) | Moyenne (paths, filters) | Elevee (routers, iterators) |
| **Ecosysteme** | Open-source, communaute | Microsoft 365, Azure | SaaS grand public | SaaS / agences |
| **Courbe d'apprentissage** | Moyenne-elevee | Moyenne | Faible | Moyenne |
| **Self-hosting** | Oui (Docker, K8s) | Non | Non | Non |
| **Ideal pour** | Equipes tech, donnees sensibles | Entreprises Microsoft | PME, non-techniques | Agences, workflows visuels |

## Decision Guide

### Arbre de decision pour le choix de plateforme

```
1. Quel est votre ecosysteme principal ?
   +-- Microsoft 365 / Azure --> Power Automate
   +-- Google Workspace / multi-SaaS --> continuer
       |
       2. Avez-vous des contraintes de souverainete / donnees sensibles ?
          +-- Oui, donnees on-premise ou hebergement controle requis --> N8N (self-hosted)
          +-- Non --> continuer
              |
              3. Quel est le niveau technique de l'equipe ?
                 +-- Non-technique / citizen developers --> Zapier
                 +-- Technique / developpeurs --> N8N Cloud ou Make
                 +-- Mixte --> Make (bon equilibre visuel + puissance)
                     |
                     4. Quel est le budget ?
                        +-- Minimal (< 50 EUR/mois) --> Make ou N8N self-hosted
                        +-- Moyen (50-200 EUR/mois) --> Zapier ou Make
                        +-- Entreprise (200+ EUR/mois) --> Power Automate ou N8N Enterprise
```

### Arbre de decision pour le type de trigger

```
1. L'evenement source offre-t-il des webhooks ?
   +-- Oui --> Utiliser un webhook (temps reel, efficace)
   +-- Non --> continuer
       |
       2. L'evenement source a-t-il une API interrogeable ?
          +-- Oui --> Utiliser le polling avec deduplication
          +-- Non --> continuer
              |
              3. L'evenement est-il periodique / previsible ?
                 +-- Oui --> Utiliser un schedule (cron)
                 +-- Non --> Utiliser un trigger manuel ou un email parser
```

### Quand NE PAS automatiser

- Le processus change frequemment (plus d'une fois par mois) — stabiliser d'abord
- Le volume est trop faible (< 1 fois par mois) et la complexite elevee — le ROI est negatif
- Le processus necessite un jugement humain complexe a chaque etape — automatiser l'acheminement, pas la decision
- Les systemes source n'ont ni API ni webhook — l'automatisation par scraping ou RPA est fragile
- Les donnees sont trop sensibles pour transiter par un tiers cloud — evaluer N8N self-hosted ou une solution on-premise

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Webhook Receiver avec validation** : recevoir un webhook, valider la signature HMAC, parser le payload, router vers le bon traitement. Toujours valider l'authenticite du webhook avant de traiter les donnees.
- **Polling avec deduplication** : interroger une API periodiquement, stocker les IDs deja traites, ne traiter que les nouveaux elements. Utiliser un data store ou une base de donnees pour la deduplication.
- **Retry avec backoff exponentiel** : en cas d'echec d'un appel API, reessayer avec des delais croissants (1s, 2s, 4s, 8s) et un nombre maximum de tentatives. Notifier apres le dernier echec.
- **Data Transformation Pipeline** : recevoir des donnees brutes, les nettoyer, les transformer au format cible, les valider, puis les envoyer. Separer chaque etape de transformation pour faciliter le debug.
- **Approval Workflow** : declencher une demande d'approbation (Slack, email, Teams), attendre la reponse, router selon la decision (approuve -> action, rejete -> notification, timeout -> escalade).
- **Fan-out / Fan-in** : distribuer un traitement sur plusieurs elements en parallele (fan-out), puis agreger les resultats (fan-in). Utile pour le traitement de listes volumineuses.

### Anti-patterns critiques

- **Over-automation** : automatiser des processus qui n'en ont pas besoin, creant de la complexite sans valeur. Chaque workflow ajoute de la dette de maintenance. Automatiser uniquement quand le ROI est clairement positif.
- **No Error Handling** : deployer des workflows sans aucune gestion d'erreurs. Les echecs silencieux provoquent des pertes de donnees, des doublons et une perte de confiance dans l'automatisation.
- **API Rate Limit Ignorance** : ignorer les limites de taux des API, provoquant des blocages et des echecs en cascade. Toujours verifier les rate limits documentees et implementer du throttling.
- **Hardcoded Credentials** : inserer des cles API, tokens ou mots de passe directement dans les configurations de workflow. Utiliser systematiquement les credential stores natifs de la plateforme.
- **Chain of Fragile Steps** : construire des workflows de 20+ etapes sans modularisation. Decomposer en sub-workflows reutilisables et testables independamment.
- **Ignorer les doublons** : ne pas gerer la deduplication dans les workflows declenches par webhook, conduisant a des traitements et des creations en double lors de re-deliveries.

## Implementation Workflow

### Phase 1 — Audit & Opportunity Mapping

1. Inventorier les processus repetitifs de l'equipe ou de l'organisation (interviews, observation, analyse des tickets).
2. Classer chaque processus dans la matrice frequence x complexite.
3. Identifier les 3-5 quick wins : taches a haute frequence et faible complexite.
4. Documenter les systemes impliques, les formats de donnees et les flux d'information actuels.
5. Estimer le temps economise par automatisation pour calculer le ROI previsionnel.

### Phase 2 — Design & Prototype

6. Choisir la plateforme d'automatisation adaptee (cf. Decision Guide).
7. Designer le workflow sur papier ou en diagramme : trigger, conditions, actions, gestion d'erreurs.
8. Identifier les connecteurs necessaires et verifier leur disponibilite sur la plateforme.
9. Prototyper le workflow avec des donnees de test (sandbox, environnement de dev).
10. Valider avec les utilisateurs finaux que le flux automatise produit le resultat attendu.

### Phase 3 — Build & Test

11. Construire le workflow dans la plateforme avec la gestion d'erreurs integree.
12. Tester chaque branche du workflow (succes, echec, cas limites, donnees vides, doublons).
13. Verifier l'idempotence : executer le workflow deux fois avec les memes donnees et valider l'absence de doublons.
14. Tester les limites : volume de donnees, rate limits, timeouts, taille des payloads.
15. Documenter le workflow : objectif, trigger, actions, gestion d'erreurs, contacts responsables.

### Phase 4 — Deploy & Monitor

16. Activer le workflow en production avec un monitoring actif les premiers jours.
17. Configurer les alertes : echecs, duree anormale, absence d'execution attendue.
18. Mettre en place un dashboard de suivi : nombre d'executions, taux de succes, temps moyen.
19. Informer les utilisateurs concernes du lancement et du comportement attendu.
20. Planifier une revue a J+7 et J+30 pour valider le fonctionnement et mesurer le gain reel.

### Phase 5 — Optimize & Scale

21. Analyser les metriques de performance et identifier les optimisations (caching, parallelisation, batching).
22. Refactorer les workflows complexes en sub-workflows modulaires et reutilisables.
23. Etendre l'automatisation aux processus adjacents identifies lors de l'audit.
24. Former les utilisateurs a la creation de workflows simples (citizen automation).
25. Etablir une gouvernance : naming conventions, documentation, revue periodique, ownership.

## Modele de maturite

### Niveau 1 — Manuel

- Les processus sont executes entierement a la main, avec des copier-coller entre applications
- Pas de plateforme d'automatisation en place ; les "automatisations" se limitent a des regles email basiques
- Les erreurs et oublis sont frequents car tout repose sur la memoire et la discipline individuelle
- **Indicateurs** : 0 workflow actif, 100% des processus manuels, erreurs humaines frequentes

### Niveau 2 — Ponctuel

- Quelques workflows simples sont en place (Zapier, IFTTT) pour les taches les plus repetitives
- L'automatisation est portee par des individus, sans strategie ni gouvernance commune
- Pas de gestion d'erreurs structuree ; les echecs sont decouverts au hasard
- **Indicateurs** : 1-10 workflows actifs, gain de temps estime mais non mesure, pas de monitoring

### Niveau 3 — Structure

- Une plateforme principale est choisie et adoptee par l'equipe (N8N, Make, Power Automate)
- Les workflows incluent la gestion d'erreurs, le logging et les notifications d'echec
- Un inventaire des automatisations est maintenu avec des owners et une documentation
- **Indicateurs** : 10-50 workflows actifs, taux de succes > 95%, gain de temps mesure

### Niveau 4 — Optimise

- Les workflows sont modulaires (sub-workflows), versionnes et testes avant deploiement
- Le monitoring est centralise avec des dashboards et des alertes proactives
- Les citizen developers creent des workflows simples en autonomie grace aux templates et a la formation
- **Indicateurs** : 50-200 workflows actifs, taux de succes > 99%, ROI documente par workflow

### Niveau 5 — Intelligent

- L'IA est integree dans les workflows : classification automatique, extraction d'information, prise de decision assistee
- Les workflows se declenchent et s'adaptent dynamiquement en fonction du contexte (event-driven architecture)
- L'orchestration couvre l'ensemble de l'organisation avec une gouvernance centralisee et des analytics d'usage
- **Indicateurs** : 200+ workflows actifs, automatisation pilotee par IA, centre d'excellence automation

## Rythme operationnel

| Cadence | Activite | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Quotidien** | Verification du dashboard de monitoring (echecs, alertes) | Automation Owner | Incidents identifies et traites |
| **Hebdomadaire** | Revue des workflows en echec et des anomalies | Automation Lead | Rapport d'incidents + actions correctives |
| **Mensuel** | Analyse des metriques d'automatisation (executions, taux de succes, gain de temps) | Automation Lead | Dashboard mensuel + ROI |
| **Mensuel** | Identification de nouvelles opportunites d'automatisation | Equipe / Managers | Backlog d'automatisation mis a jour |
| **Trimestriel** | Audit des workflows actifs (pertinence, securite, performance) | Automation Lead + IT | Rapport d'audit + plan de remediation |
| **Trimestriel** | Revue des couts de plateforme et optimisation du plan | Automation Lead + Finance | Analyse cout/benefice + recommandations |
| **Annuel** | Evaluation de la maturite automation et feuille de route | Direction + Automation Lead | Feuille de route N+1 + objectifs |

## State of the Art (2025-2026)

L'automatisation de workflows connait une transformation majeure grace a l'IA et aux architectures composables :

- **AI-powered automation** : les plateformes integrent l'IA generative pour analyser les emails, classifier les documents, extraire les donnees structurees et generer des reponses. N8N propose des nodes AI natifs, Zapier integre des AI actions, et Power Automate dispose d'AI Builder. Les workflows deviennent intelligents et capables de traiter des donnees non structurees.
- **Natural language workflow creation** : la creation de workflows par description en langage naturel devient une realite. Zapier Central, Make AI Assistant et Power Automate Copilot permettent de decrire un workflow en francais ou en anglais et de le generer automatiquement. Cette evolution democratise l'automatisation aupres des non-techniciens.
- **Autonomous agents** : les agents autonomes (AI agents) executent des taches complexes en enchainent plusieurs actions de maniere autonome, avec capacite de raisonnement et d'adaptation. N8N AI Agent node, Zapier Central bots et les agents Power Automate representent l'avant-garde de cette evolution.
- **Event-driven architecture** : l'architecture event-driven remplace progressivement le polling comme modele dominant. Les plateformes adoptent les event buses, les real-time triggers et les architectures pub/sub pour des automatisations plus reactives et plus scalables.
- **Composable automation** : les workflows deviennent des briques composables et reutilisables. Les organisations construisent des bibliotheques de sub-workflows partageables, versionnes et documentes, favorisant la reutilisation et la standardisation.
- **Hyperautomation** : la convergence du no-code, du RPA, de l'IA et du process mining cree une approche holistique de l'automatisation. Le process mining identifie automatiquement les opportunites, les plateformes no-code construisent les workflows, et l'IA optimise leur execution.

## Template actionnable

### Automation Opportunity Assessment

| Processus | Frequence | Temps/execution | Complexite (1-5) | Systemes impliques | Score priorite | Statut |
|---|---|---|---|---|---|---|
| ___ | ___ /semaine | ___ min | ___ | ___ | ___ | A evaluer / En cours / Deploye |
| ___ | ___ /semaine | ___ min | ___ | ___ | ___ | ___ |
| ___ | ___ /semaine | ___ min | ___ | ___ | ___ | ___ |
| ___ | ___ /semaine | ___ min | ___ | ___ | ___ | ___ |
| ___ | ___ /semaine | ___ min | ___ | ___ | ___ | ___ |

**Formule de score priorite** : (Frequence hebdo x Temps en minutes) / Complexite = Score. Plus le score est eleve, plus l'automatisation est prioritaire.

### Workflow Documentation Template

```
Nom du workflow : ___
Owner : ___
Plateforme : ___
Date de creation : ___
Derniere modification : ___

Objectif : ___
Trigger : ___
Frequence d'execution : ___

Etapes :
1. ___
2. ___
3. ___

Gestion d'erreurs :
- En cas d'echec de l'etape ___ : ___
- Notification envoyee a : ___

Systemes connectes : ___
Credentials utilisees : ___

Metriques :
- Executions/jour : ___
- Taux de succes : ___
- Temps moyen : ___
```

## Prompts types

- "Comment automatiser la synchronisation de nos contacts entre HubSpot et Google Sheets ?"
- "Aide-moi a creer un workflow N8N pour traiter les emails entrants et creer des tickets Jira"
- "Quelle plateforme d'automatisation choisir entre Zapier, Make et N8N pour notre equipe ?"
- "Propose un workflow d'onboarding automatise pour les nouveaux collaborateurs"
- "Comment gerer les erreurs et les retry dans mes workflows Make ?"
- "Aide-moi a concevoir un workflow d'approbation multi-niveaux avec Power Automate"

## Limites et Red Flags

Ce skill n'est PAS adapte pour :
- Le developpement d'applications completes avec interface utilisateur --> Utiliser plutot : `productivite:nocode-apps`
- La gestion de projet et le pilotage de programmes --> Utiliser plutot : `entreprise:gestion-de-projets`
- L'architecture logicielle et le design de systemes --> Utiliser plutot : `code-development:architecture`
- Les pipelines de donnees et l'ingenierie de donnees (ETL, data warehouse) --> Utiliser plutot : `data-bi:data-engineering`
- La cybersecurite et l'authentification applicative --> Utiliser plutot : `code-development:auth-security`
- Les pipelines CI/CD et le deploiement logiciel --> Utiliser plutot : `code-development:devops`

Signaux d'alerte en cours d'utilisation :
- Un workflow depasse 20 etapes sans modularisation en sub-workflows — risque de fragilite et difficulte de maintenance
- Le taux d'echec d'un workflow depasse 5% — investiguer la cause racine avant d'ajouter des fonctionnalites
- Des credentials sont hardcodees dans les configurations de workflow — vulnerabilite de securite critique
- Un workflow n'a pas de monitoring ni de notification d'erreur — echecs silencieux garantis
- L'equipe automatise des processus instables qui changent frequemment — stabiliser le processus avant d'automatiser
- Le cout de la plateforme depasse le gain de temps economise — revoir le ROI et optimiser le plan

## Skills connexes

| Skill | Lien |
|---|---|
| No-Code Apps | `productivite:nocode-apps` — Construction d'applications sans code |
| Collaboration Digitale | `productivite:collaboration-digitale` — Outils collaboratifs et communication |
| Email & Gestion du Temps | `productivite:email-gestion-temps` — Productivite email et time management |
| IT Systemes | `entreprise:it-systemes` — Architecture SI et integration |
| Operations | `entreprise:operations` — Excellence operationnelle et processus |
| Data Engineering | `data-bi:data-engineering` — Pipelines de donnees et ETL |

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[N8N & Power Automate](./references/n8n-power-automate.md)** : architecture N8N (self-hosted, fair-code), types de nodes et patterns de workflows, expressions et transformation de donnees, Power Automate fundamentals (cloud flows, desktop flows), connecteurs et fonctionnalites premium, integration M365, comparaison detaillee, patterns avances et deploiement.
- **[Zapier & Make](./references/zapier-make.md)** : architecture Zapier (Zaps, multi-step, paths, filters), Tables et Interfaces, Make scenarios et modules, data mapping et iterateurs, comparaison Zapier vs Make, IFTTT pour les automatisations simples, modeles de pricing et optimisation, patterns avances et migration entre plateformes.
- **[Design Patterns de Workflows](./references/workflow-design-patterns.md)** : patterns d'architecture (sequentiel, parallele, branching, boucle, saga), types de triggers, patterns de gestion d'erreurs (retry, dead letter, circuit breaker), transformation de donnees, idempotence, testing, monitoring, gouvernance et securite.
- **[Integration API & Connecteurs](./references/integration-api.md)** : fondamentaux REST API, methodes HTTP et codes de statut, patterns d'authentification (API key, OAuth 2.0, Bearer token), webhooks et securite, data mapping et transformation, pagination, rate limiting, synchronisation temps reel vs batch, integrations populaires et debugging.
