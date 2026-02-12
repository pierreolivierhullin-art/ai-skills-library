---
name: support-client
description: This skill should be used when the user asks about "customer support strategy", "customer success", "knowledge base management", "NPS improvement", "customer experience", "stratégie support client", "service client", "satisfaction client", "CSAT", "CES", "customer effort score", "help desk", "centre d'aide", "ticketing", "Zendesk", "Intercom", "Freshdesk", "churn prevention", "rétention client", "fidélisation", "customer health score", "onboarding client", "SLA support", "temps de réponse", "first response time", "résolution au premier contact", "FCR", "self-service", "chatbot support", "escalation", "voice of customer", "VoC", discusses help desk operations, churn prevention, or needs guidance on support metrics, CX programs, or customer health scoring.
version: 1.1.0
last_updated: 2026-02
---

# Customer Support & Service Client

## Overview

Ce skill couvre l'ensemble des disciplines liées au support client, au customer success et a l'experience client (CX). Il fournit un cadre operationnel et strategique pour concevoir, structurer et optimiser les operations de support, les bases de connaissances, les programmes de customer success et les dispositifs de mesure de la satisfaction. Le support client moderne ne se limite plus a la resolution reactive de problemes : il englobe l'engagement proactif, le self-service intelligent, l'analyse predictive du churn et l'orchestration omnicanale. Appliquer systematiquement les principes decrits ici pour structurer chaque decision, en privilegiant la resolution au premier contact, l'autonomie client et la valeur a long terme.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Conception ou restructuration d'un service support** : choix des canaux, dimensionnement des equipes, definition des SLA, mise en place des outils (Zendesk, Intercom, Freshdesk, Salesforce Service Cloud).
- **Gestion des tickets et escalades** : conception des workflows de triage, regles d'automatisation, matrices d'escalade, gestion des priorites et des SLA critiques.
- **Construction d'une base de connaissances** : architecture de l'information, taxonomie, redaction d'articles help center, methodologie KCS (Knowledge-Centered Service), optimisation du self-service.
- **Deploiement de chatbots et IA conversationnelle** : design conversationnel, entrainement des modeles, gestion des handoffs humain/bot, mesure de la deflection rate.
- **Mise en place d'un programme Customer Success** : health scoring, segmentation des comptes, playbooks de proactivite, QBR (Quarterly Business Reviews), expansion et upsell.
- **Prevention du churn** : identification des signaux d'alerte, scoring predictif, interventions de retention, analyse des cohortes.
- **Programmes Voice of Customer (VoC)** : deploiement NPS/CSAT/CES, closed-loop feedback, journey mapping, service blueprinting, touchpoint optimization.
- **Analytics et reporting support** : suivi du FCR (First Contact Resolution), AHT (Average Handle Time), ticket volume forecasting, performance par canal et par agent.

## Core Principles

### Principle 1 — Customer Effort Reduction
Reduire l'effort client a chaque interaction. Le Customer Effort Score (CES) est le meilleur predicteur de fidelite. Chaque processus, chaque canal, chaque article de knowledge base doit etre concu pour minimiser les frictions. Viser la resolution en un seul contact (FCR > 80%) et l'acces self-service en moins de 3 clics.

### Principle 2 — Proactive over Reactive
Passer d'un modele reactif (attendre le probleme) a un modele proactif (anticiper et prevenir). Utiliser les donnees produit, les patterns de tickets et le health scoring pour identifier les clients a risque avant qu'ils ne contactent le support. Le support proactif reduit le volume de tickets de 20-30% et augmente la retention de 15-25%.

### Principle 3 — Omnichannel Consistency
Garantir une experience coherente quel que soit le canal (email, chat, telephone, messaging, social media, self-service). Le contexte client doit suivre le parcours entre canaux sans perte d'information. Un client qui passe du chat au telephone ne doit jamais repeter son probleme.

### Principle 4 — Knowledge as a Strategic Asset
Traiter la base de connaissances comme un actif strategique, pas comme un projet ponctuel. Appliquer la methodologie KCS pour creer et maintenir le contenu au fil des interactions. Chaque resolution de ticket est une opportunite d'enrichir la knowledge base. Viser un taux de self-service resolution > 40%.

### Principle 5 — Data-Driven Support Operations
Fonder chaque decision operationnelle sur les donnees. Mesurer systematiquement : CSAT par canal, FCR, AHT, ticket backlog age, agent utilization, deflection rate. Utiliser le forecasting pour anticiper les pics de volume et ajuster le staffing. Ne jamais piloter a l'intuition.

### Principle 6 — Customer Success as Revenue Driver
Le customer success n'est pas un centre de cout — c'est un levier de croissance. Un programme CS mature genere du Net Revenue Retention (NRR) > 110% via l'expansion, l'upsell et la reduction du churn. Aligner les objectifs CS sur les metriques de revenue, pas uniquement sur la satisfaction.

## Key Frameworks & Methods

### Support Maturity Model

| Niveau | Caracteristiques | Metriques cles | Outils |
|---|---|---|---|
| **Level 1 — Reactive** | Email/telephone, pas de SLA formel, KB minimale | Temps de reponse moyen | Boite mail partagee |
| **Level 2 — Structured** | Ticketing, SLA definis, KB basique, 1-2 canaux | CSAT, FCR | Zendesk, Freshdesk |
| **Level 3 — Optimized** | Omnicanal, automatisation, KCS, analytics | CES, deflection rate, NPS | Intercom, Gainsight |
| **Level 4 — Predictive** | IA/ML, health scoring, proactivite, self-service avance | NRR, churn rate, CLV | Plateforme integree + IA |
| **Level 5 — Autonomous** | IA agentique, resolution automatique, hyper-personnalisation | Effort score zero, predictive CSAT | AI-native stack |

### Ticket Triage Framework

Classifier chaque ticket selon deux axes :

**Urgence** (impact sur le client) :
- **P1 — Critical** : service completement indisponible, impact business majeur. SLA reponse : 15 min. SLA resolution : 4h.
- **P2 — High** : fonctionnalite majeure degradee, workaround possible. SLA reponse : 1h. SLA resolution : 8h.
- **P3 — Medium** : probleme impactant mais non bloquant. SLA reponse : 4h. SLA resolution : 24h.
- **P4 — Low** : question, demande d'amelioration, probleme cosmetique. SLA reponse : 24h. SLA resolution : 5 jours.

**Complexite** (effort de resolution) :
- **Tier 1** : resolution immediate, FAQ, procedures standard.
- **Tier 2** : investigation requise, diagnostic technique, configuration.
- **Tier 3** : escalade engineering, bug confirm, custom development.

### Customer Health Score Model

Construire un health score composite (0-100) a partir de signaux ponderes :

| Signal | Poids | Source | Seuil d'alerte |
|---|---|---|---|
| Product usage (DAU/MAU) | 25% | Analytics produit | < 30% du plan |
| Feature adoption | 15% | Product analytics | < 3 features cles |
| Support ticket sentiment | 15% | NLP sur tickets | Sentiment negatif > 40% |
| NPS/CSAT recent | 15% | Enquetes | NPS < 0 ou CSAT < 3/5 |
| Contract/billing health | 15% | CRM/Billing | Retard paiement, downgrade |
| Engagement (logins, API calls) | 10% | Analytics | Baisse > 30% sur 30j |
| Stakeholder relationship | 5% | CS manual input | Changement de champion |

### NPS/CSAT/CES — Quand et comment mesurer

| Metrique | Question type | Quand envoyer | Benchmark |
|---|---|---|---|
| **NPS** | "Recommanderiez-vous..." (0-10) | Trimestriel, post-onboarding | > 50 excellent, > 30 bon |
| **CSAT** | "Satisfaction de cette interaction" (1-5) | Post-ticket, post-chat | > 4.2/5 ou > 85% |
| **CES** | "A ete facile de resoudre..." (1-7) | Post-resolution, post-self-service | > 5.5/7 ou > 75% "facile" |

## Decision Guide

### Arbre de decision : choix de la stack support

```
1. Quel est le volume mensuel de tickets ?
   +-- < 500/mois -> Solution legere (Crisp, HelpScout, Freshdesk Free)
   +-- 500-5000/mois -> Solution intermediaire (Zendesk Suite, Intercom)
   +-- > 5000/mois -> Solution enterprise (Salesforce Service Cloud, Zendesk Enterprise)

2. Quels canaux sont prioritaires ?
   +-- Email + chat principalement -> Intercom, Front, Zendesk
   +-- Telephone important -> Zendesk Talk, Aircall, Five9
   +-- Messaging (WhatsApp, Messenger) -> Intercom, MessageBird, Twilio Flex

3. Faut-il un programme Customer Success ?
   +-- ARR < 2M EUR, < 200 clients -> CS light (CRM + spreadsheet)
   +-- ARR 2-20M EUR -> Gainsight Essentials, Vitally, Planhat
   +-- ARR > 20M EUR -> Gainsight, Totango, ChurnZero
```

### Arbre de decision : self-service vs human support

```
1. La question a-t-elle une reponse standard documentee ?
   +-- Oui -> Self-service (KB article, chatbot, guided flow)
   +-- Non -> Humain

2. Le probleme necessite-t-il un acces au compte client ?
   +-- Non -> Self-service ou communaute
   +-- Oui, lecture seule -> Chatbot avec integration CRM
   +-- Oui, modifications -> Agent humain (Tier 1+)

3. Le client est-il en situation emotionnelle (frustration, urgence) ?
   +-- Oui -> Escalade immediate vers humain avec contexte complet
   +-- Non -> Continuer le parcours self-service
```

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Swarming Model** : remplacer l'escalade hierarchique (Tier 1 -> 2 -> 3) par un modele collaboratif ou les specialistes rejoignent le ticket directement. Reduit le temps de resolution de 40% et elimine les transferts frustrants pour le client.
- **Shift-Left Strategy** : deplacer la resolution vers le self-service et l'automatisation. Investir dans la KB, les chatbots et les guides interactifs pour que 40-60% des requetes soient resolues sans contact humain.
- **Closed-Loop Feedback** : boucler systematiquement sur chaque feedback negatif. Un detracteur NPS recontacte dans les 48h a 50% de chances de devenir promoteur. Documenter chaque boucle de feedback et les actions correctives.
- **Proactive Health Alerts** : configurer des alertes automatiques quand le health score descend sous un seuil. Declencher des playbooks de retention automatises (email personnalise, appel CS, offre).
- **QBR as Value Delivery** : structurer les Quarterly Business Reviews autour de la valeur delivree (ROI, outcomes atteints) et non autour du produit. Presenter 80% valeur / 20% roadmap.

### Anti-patterns critiques

- **Ticket Ping-Pong** : transferer un ticket entre equipes sans resolution. Chaque transfert augmente l'effort client et la frustration. Diagnostiquer via le nombre moyen de reassignations par ticket (cible : < 1.5).
- **Knowledge Base Cemetery** : creer des articles et ne jamais les mettre a jour. Une KB obsolete est pire que pas de KB du tout. Implementer des revues trimestrielles et archiver les articles avec un taux de "Not Helpful" > 30%.
- **Vanity Metrics Obsession** : se focaliser sur le nombre de tickets resolus plutot que sur la qualite de la resolution. Un ticket "resolu" que le client reouvre n'est pas resolu. Mesurer le reopen rate (cible : < 5%).
- **One-Size-Fits-All CS** : appliquer le meme playbook CS a tous les clients. Segmenter par ARR, usage, maturite et potentiel de croissance. Le modele high-touch/low-touch/tech-touch est le minimum.
- **Survey Fatigue** : bombarder les clients d'enquetes. Limiter a 1 enquete NPS par trimestre et 1 CSAT par interaction significative. Toujours agir sur les resultats avant d'envoyer la prochaine enquete.

## Implementation Workflow

### Phase 1 — Foundation & Assessment
1. Auditer l'etat actuel du support : canaux, volume, SLA reels vs cibles, satisfaction.
2. Cartographier le parcours client actuel (customer journey map) avec les points de friction.
3. Definir les personas client et leurs attentes par canal.
4. Benchmarker les metriques vs le secteur (CSAT, FCR, AHT, NPS).
5. Selectionner et configurer la stack d'outils (ticketing, KB, CS platform).

### Phase 2 — Operations Setup
6. Concevoir les workflows de triage et d'escalade.
7. Definir les SLA par priorite et par segment client.
8. Construire la knowledge base initiale (top 50 questions, articles proceduraux).
9. Former les agents sur les outils, les processus et le tone of voice.
10. Mettre en place le reporting operationnel (dashboards quotidiens et hebdomadaires).

### Phase 3 — Optimization & Automation
11. Deployer le self-service : KB publique, chatbot, guided troubleshooting.
12. Automatiser le triage (classification IA, routing automatique, macros).
13. Implementer la methodologie KCS pour l'enrichissement continu de la KB.
14. Lancer les enquetes de satisfaction (NPS trimestriel, CSAT post-interaction).
15. Mettre en place le closed-loop feedback sur les detracteurs.

### Phase 4 — Customer Success & Proactivity
16. Construire le health score et segmenter les comptes.
17. Deployer les playbooks proactifs (onboarding, adoption, retention, expansion).
18. Lancer le programme QBR pour les comptes strategiques.
19. Implementer le churn prediction model et les alertes automatisees.
20. Mesurer le Net Revenue Retention et aligner les objectifs CS sur la croissance.




## Template actionnable

### Matrice de triage des tickets

| Priorité | Critère | SLA réponse | SLA résolution | Exemple |
|---|---|---|---|---|
| **P1 — Critique** | Service indisponible, perte de données | 15 min | 2h | Plateforme down |
| **P2 — Haute** | Fonctionnalité majeure dégradée | 1h | 8h | Paiements échouent |
| **P3 — Moyenne** | Bug non bloquant, contournement possible | 4h | 24h | Export CSV cassé |
| **P4 — Basse** | Question, demande d'amélioration | 24h | 5 jours | Nouvelle fonctionnalité |

## Prompts types

- "Comment structurer un service client multicanal efficace ?"
- "Aide-moi à construire une knowledge base pour réduire les tickets"
- "Propose un plan d'action pour améliorer notre NPS"
- "Comment mettre en place un programme de customer success ?"
- "Quels SLA définir pour notre support client B2B ?"
- "Aide-moi à calculer le customer health score de nos comptes"

## Skills connexes

| Skill | Lien |
|---|---|
| Commercial | `entreprise:commercial` — Rétention client et upsell |
| Communication | `entreprise:communication` — Communication de crise client |
| Product Analytics | `code-development:product-analytics` — Analyse du feedback et NPS |
| Marketing | `entreprise:marketing` — Parcours client et expérience de marque |
| Prompt Engineering | `ai-governance:prompt-engineering-llmops` — Chatbots et support IA |

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[Support Operations](./references/support-operations.md)** : gestion des tickets, support multi-canal, SLA management, matrices d'escalade, outils (Zendesk, Intercom, Freshdesk), modeles de staffing, automatisation, state of the art 2024-2026.
- **[Knowledge Base & Self-Service](./references/knowledge-self-service.md)** : architecture de knowledge base, methodologie KCS, redaction d'articles, optimisation du self-service, chatbots et IA conversationnelle, content analytics, state of the art 2024-2026.
- **[Customer Success](./references/customer-success.md)** : health scoring, engagement proactif, prevention du churn, QBR, expansion et upsell, outils CS (Gainsight, ChurnZero, Totango), modeles de segmentation, state of the art 2024-2026.
- **[CX & Analytics](./references/cx-analytics.md)** : programmes Voice of Customer, mesure NPS/CSAT/CES, journey mapping, service blueprinting, analytics support, forecasting, performance metrics, state of the art 2024-2026.
