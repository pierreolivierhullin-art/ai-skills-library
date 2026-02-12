---
name: payment-stripe
description: This skill should be used when the user asks about "Stripe integration", "payment processing", "subscription billing", "PCI compliance", "checkout", "webhooks", "Stripe Connect", "payment intents", "recurring payments", "invoicing", "metered billing", "SCA", "3D Secure", "intégration Stripe", "traitement des paiements", "facturation récurrente", "conformité PCI", "paiements récurrents", "facturation", "abonnements", "subscriptions", "pricing page", "page de tarification", "Stripe Elements", "Stripe Checkout", "customer portal", "portail client", "proration", "prorata", "coupons", "promotions", "refunds", "remboursements", "disputes", "litiges", "Stripe Tax", "marketplace payments", "paiements marketplace", "payment links", "Apple Pay", "Google Pay", or needs guidance on payment implementation and monetization.
version: 1.1.0
last_updated: 2026-02
---

# Payment Stripe

## Overview

Ce skill couvre l'ensemble de l'ecosysteme Stripe pour l'implementation de paiements, la facturation recurrente, les places de marche et la conformite reglementaire. Il synthetise les meilleures pratiques 2024-2026 incluant le Payment Element unifie, Stripe Billing v2, Stripe Connect, Stripe Tax, Adaptive Pricing et les embedded components. Utiliser ce skill comme reference systematique pour toute decision touchant aux paiements, a la monetisation et a la gestion financiere dans une application.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- Integration de Stripe Checkout, Payment Links ou Stripe Elements dans une application
- Implementation de Payment Intents ou Setup Intents pour des flux de paiement personnalises
- Mise en place de Stripe Connect pour une place de marche (Standard, Express, Custom)
- Configuration de Stripe Billing pour des abonnements, facturation recurrente ou metered billing
- Gestion des webhooks Stripe (signature verification, idempotency, retry logic)
- Implementation de SCA / 3D Secure 2 pour la conformite europeenne
- Reduction du scope PCI-DSS (tokenisation, Stripe.js, iframes)
- Configuration de Stripe Tax pour le calcul automatique des taxes
- Integration de moyens de paiement varies (cartes, SEPA, Apple Pay, Google Pay, BNPL)
- Gestion du cycle de vie des abonnements (trials, proration, dunning, Smart Retries)
- Revenue recognition et reconciliation comptable
- Implementation d'Adaptive Pricing pour la tarification multi-devises

## Core Principles

### 1. Payment Element First (Element de paiement unifie)

Toujours privilegier le Payment Element unifie plutot que les Elements individuels (Card Element, IBAN Element). Le Payment Element gere automatiquement l'affichage des methodes de paiement pertinentes selon la localisation du client, le montant et la devise. Il prend en charge nativement SCA/3D Secure, les wallets (Apple Pay, Google Pay), SEPA, Klarna, et les nouvelles methodes sans modification de code. Configurer le Payment Element avec `layout: 'accordion'` ou `layout: 'tabs'` selon l'UX souhaitee.

### 2. Server-Side Authority (Autorite cote serveur)

Ne jamais faire confiance au client pour les montants, les devises ou les metadata critiques. Creer systematiquement les Payment Intents, Setup Intents et Checkout Sessions cote serveur. Le client ne recoit que le `client_secret` pour confirmer le paiement. Valider chaque montant cote serveur avant de creer l'intent. Traiter les webhooks comme source de verite pour l'etat des paiements plutot que les retours client-side.

### 3. Webhook-Driven Architecture (Architecture pilotee par webhooks)

Concevoir le systeme autour des webhooks comme source de verite. Ne pas se fier uniquement aux redirections ou aux callbacks client pour confirmer les paiements. Un paiement n'est confirme que lorsque le webhook `payment_intent.succeeded` est recu et traite. Implementer l'idempotence sur chaque handler de webhook. Verifier systematiquement la signature du webhook avec `stripe.webhooks.constructEvent()`. Gerer les retries (Stripe retente jusqu'a 3 jours avec backoff exponentiel).

### 4. PCI Scope Minimization (Minimisation du perimetre PCI)

Reduire le scope PCI au minimum absolu en utilisant exclusivement Stripe.js et les composants d'interface Stripe (Payment Element, Checkout, Payment Links). Ne jamais transmettre, stocker ou journaliser des numeros de carte complets cote serveur. Utiliser la tokenisation pour toutes les operations. Avec Stripe.js et le Payment Element, l'application releve du SAQ-A (niveau le plus simple). Documenter la conformite PCI et maintenir un inventaire des flux de donnees de paiement.

### 5. Idempotent Operations (Operations idempotentes)

Utiliser des cles d'idempotence (`Idempotency-Key` header) pour toutes les operations de creation et de mutation via l'API Stripe. Generer des cles deterministes basees sur le contexte metier (ex: `order_{orderId}_payment`). Cela previent les doubles charges en cas de retry reseau, de timeout ou de redemarrage de processus. Stripe garantit que les requetes avec la meme cle d'idempotence produisent le meme resultat pendant 24 heures.

## Key Frameworks & Methods

### Integration Models

| Modele | Complexite | Personnalisation | Cas d'usage |
|--------|-----------|------------------|-------------|
| Payment Links | Tres faible | Faible | Vente rapide, landing pages, no-code |
| Stripe Checkout (hosted) | Faible | Moyenne | E-commerce standard, SaaS onboarding |
| Stripe Checkout (embedded) | Moyenne | Moyenne-Haute | Checkout integre au site, UX fluide |
| Payment Element (custom) | Haute | Tres haute | Flux personnalises, marketplace |
| Stripe Connect | Tres haute | Totale | Places de marche, platforms multi-vendeurs |

### Subscription Billing Models

| Modele | Description | Cas d'usage |
|--------|-------------|-------------|
| Fixed-price recurring | Montant fixe par periode | SaaS tiers (Basic/Pro/Enterprise) |
| Per-seat pricing | Prix par utilisateur actif | Outils collaboratifs (Slack-like) |
| Metered / usage-based | Facturation a la consommation | API, stockage, compute |
| Tiered pricing | Tranches de prix degressives | Volume discounts |
| Hybrid | Fixe + variable | Base + overage (Twilio-like) |

### Payment Methods Landscape (2024-2026)

| Methode | Regions | Confirmation | Recurrence |
|---------|---------|-------------|------------|
| Cards (Visa, MC, Amex) | Global | Immediate | Oui |
| Apple Pay / Google Pay | Global | Immediate | Oui |
| SEPA Direct Debit | Europe (EUR) | Differee (5-14j) | Oui |
| iDEAL | Pays-Bas | Immediate | Via SEPA mandate |
| Bancontact | Belgique | Immediate | Via SEPA mandate |
| Klarna / Afterpay | EU, US, AU | Immediate | Non |
| Affirm | US | Immediate | Non |
| ACH Direct Debit | US | Differee (4-5j) | Oui |
| BACS Direct Debit | UK | Differee (3-4j) | Oui |
| Link (Stripe) | Global | Immediate | Oui |

## Decision Guide

### Choisir un modele d'integration

```
Vente simple, pas de developpement ?
  -> Payment Links : generer un lien depuis le Dashboard
  -> Ideal pour freelances, associations, MVP rapide

E-commerce ou SaaS standard ?
  -> Stripe Checkout (hosted) : redirection vers la page Stripe
  -> Offre gratuite : gestion des taxes, emails de recus, page de succes
  -> Ajouter mode: 'subscription' pour les abonnements

Checkout integre sans redirection ?
  -> Stripe Checkout (embedded) : composant integre dans la page
  -> Utiliser stripe.initEmbeddedCheckout() avec ui_mode: 'embedded'
  -> Controle du design tout en conservant la conformite PCI

Flux de paiement entierement personnalise ?
  -> Payment Element + Payment Intent cote serveur
  -> Controle total du formulaire, de l'UX et du flux
  -> Gerer manuellement les redirections 3D Secure

Place de marche avec vendeurs tiers ?
  -> Stripe Connect : choisir le type de compte
  -> Standard : vendeurs gerent leur propre dashboard Stripe
  -> Express : onboarding simplifie, dashboard Stripe lite
  -> Custom : controle total, responsabilite totale (KYC, payouts)
```

### Choisir un modele de facturation

```
Prix fixe par mois/an ?
  -> Subscription avec price fixe
  -> Offrir des reduction annuelles (ex: 2 mois offerts)

Tarification par siege ?
  -> Subscription avec quantity dynamique
  -> Mettre a jour subscription.quantity a chaque changement
  -> Gerer la proration automatiquement

Facturation a la consommation ?
  -> Metered billing avec usage records
  -> Reporter l'usage via stripe.subscriptionItems.createUsageRecord()
  -> Facturer en fin de periode (arrears)

Mix fixe + variable ?
  -> Subscription multi-items : un item fixe + un item metered
  -> Le client paie une base + l'overage
```

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Webhook Handler Idempotent** : Stocker l'`event.id` Stripe dans la base de donnees avant de traiter l'evenement. Verifier l'existence avant tout traitement. Utiliser une transaction base de donnees pour garantir l'atomicite entre le marquage "traite" et les effets de bord (envoi d'email, activation de compte).

- **Customer-Centric Model** : Creer un `stripe_customer_id` des l'inscription de l'utilisateur. Stocker ce mapping de facon permanente. Rattacher tous les paiements, abonnements et methodes de paiement a ce customer. Cela permet le Customer Portal, la facturation coherente et l'historique complet.

- **Checkout Session Metadata** : Passer les metadata metier dans la Checkout Session (`metadata: { orderId, userId, plan }`). Recuperer ces metadata dans le webhook pour relier le paiement aux entites metier sans avoir a maintenir un etat intermediaire.

- **Stripe Tax Integration** : Activer Stripe Tax pour le calcul automatique des taxes (TVA, sales tax, GST). Passer `automatic_tax: { enabled: true }` dans les Checkout Sessions et Subscriptions. Cela gere automatiquement les taux par juridiction, les seuils de nexus et les exemptions.

- **Adaptive Pricing** : Activer l'Adaptive Pricing pour afficher automatiquement les prix dans la devise locale du client. Stripe convertit les montants et gere le FX. Cela augmente les taux de conversion de 1.5 a 17.8% selon les marches.

### Anti-patterns a eviter

- **Polling au lieu de webhooks** : Ne pas interroger regulierement l'API Stripe pour verifier l'etat des paiements. Utiliser les webhooks comme mecanisme principal. Le polling genere des couts API, de la latence et des rate limits.

- **Stocker des numeros de carte** : Ne jamais stocker, journaliser ou transmettre des numeros de carte complets. Utiliser exclusivement les tokens et Payment Methods de Stripe. Meme dans les logs de debug, ne jamais enregistrer le `client_secret` d'un Payment Intent.

- **Creer des Payment Intents cote client** : Ne jamais laisser le client definir le montant d'un paiement. Creer le Payment Intent cote serveur avec le montant valide. Le client ne recoit que le `client_secret` pour confirmer.

- **Ignorer les evenements de webhook en echec** : Ne pas ignorer les erreurs dans les handlers de webhook. Retourner un code 5xx pour que Stripe retente. Logger les erreurs avec le contexte complet (event.id, event.type, payload). Mettre en place des alertes sur les webhooks en echec.

- **Hardcoder des prix dans le code** : Ne pas hardcoder les montants ou les price IDs. Utiliser des variables d'environnement ou recuperer les prix depuis l'API Stripe. Cela permet de changer les prix sans deploiement.

## Implementation Workflow

### Phase 1 : Fondations

1. Creer un compte Stripe et configurer les cles API (test + production)
2. Installer le SDK Stripe serveur et Stripe.js cote client
3. Creer un Customer Stripe a chaque inscription utilisateur
4. Configurer les webhooks avec signature verification dans un endpoint dedie
5. Mettre en place le Stripe CLI en local pour le developpement (`stripe listen --forward-to`)

### Phase 2 : Paiements

1. Choisir le modele d'integration (Checkout, Payment Element, Payment Links)
2. Implementer le flux Payment Intent cote serveur -> confirmation cote client
3. Configurer les methodes de paiement acceptees dans le Dashboard ou via l'API
4. Gerer les etats du paiement (requires_payment_method, requires_action, succeeded, failed)
5. Implementer les handlers de webhook pour `payment_intent.succeeded` et `payment_intent.payment_failed`

### Phase 3 : Abonnements

1. Creer les Products et Prices dans Stripe (via Dashboard ou API)
2. Implementer le flux de souscription (Checkout mode subscription ou Subscription API)
3. Gerer le cycle de vie : `customer.subscription.created`, `updated`, `deleted`
4. Configurer les periodes d'essai et la logique de grace period
5. Activer Smart Retries et configurer le dunning (emails de relance automatiques)
6. Deployer le Stripe Customer Portal pour le self-service (changement de plan, annulation)

### Phase 4 : Compliance & Taxes

1. Activer Stripe Tax et configurer les origines fiscales
2. Verifier le niveau SAQ PCI-DSS et documenter la conformite
3. Configurer SCA/3D Secure (automatique avec Payment Element)
4. Mettre en place la gestion des litiges (disputes) et des remboursements
5. Configurer les receipts et invoices automatiques

### Phase 5 : Optimisation & Monitoring

1. Analyser les taux de conversion dans Stripe Dashboard / Sigma
2. Activer Adaptive Pricing pour les marches internationaux
3. Monitorer les webhooks (taux de succes, latence de traitement)
4. Configurer les alertes sur les disputes, les echecs de paiement et les anomalies
5. Implementer Revenue Recognition pour la comptabilite (ASC 606 / IFRS 15)
6. Reconcilier les flux financiers avec le systeme comptable (ERP sync, journal entries)



## State of the Art (2025-2026)

Le paiement en ligne se diversifie et se simplifie :

- **Stripe Billing v2** : Les nouvelles APIs de facturation supportent des modèles complexes (usage-based, hybrid, multi-currency) avec une meilleure gestion du revenue recognition.
- **Embedded payments** : Stripe Connect et les payment facilitation models permettent aux plateformes d'intégrer les paiements nativement.
- **Buy Now Pay Later (BNPL)** : L'intégration de Klarna, Affirm et des solutions BNPL natives de Stripe se démocratise dans les checkouts.
- **Crypto et stablecoins** : Stripe réintègre les paiements en crypto via USDC, ouvrant de nouvelles options pour les paiements internationaux.
- **Revenue automation** : Les outils de revenue recovery (dunning intelligent, smart retries) et de tax compliance (Stripe Tax) automatisent la gestion financière.

## Template actionnable

### Checklist d'intégration Stripe

| Étape | Action | Vérifié |
|---|---|---|
| **Setup** | Compte Stripe créé, clés API configurées | ☐ |
| **Setup** | Webhook endpoint configuré et sécurisé | ☐ |
| **Setup** | Produits et prix créés (test mode) | ☐ |
| **Checkout** | Flow de paiement testé (succès + échec) | ☐ |
| **Checkout** | 3D Secure / SCA géré | ☐ |
| **Webhooks** | Idempotence des handlers vérifiée | ☐ |
| **Webhooks** | Events critiques gérés (payment_intent.succeeded, invoice.paid, customer.subscription.deleted) | ☐ |
| **Billing** | Scénarios d'abonnement testés (upgrade, downgrade, cancel) | ☐ |
| **Billing** | Relance automatique (dunning) configurée | ☐ |
| **Go-live** | Switch vers clés live + tests en production | ☐ |

## Prompts types

- "Comment intégrer Stripe Checkout dans mon app Next.js ?"
- "Aide-moi à implémenter un système d'abonnement avec Stripe"
- "Comment gérer les webhooks Stripe de manière robuste ?"
- "Propose une architecture pour un marketplace avec Stripe Connect"
- "Comment implémenter le metered billing pour un usage-based pricing ?"
- "Aide-moi à gérer les cas d'échec de paiement et les relances"

## Skills connexes

| Skill | Lien |
|---|---|
| Backend & DB | `code-development:backend-db` — APIs, webhooks et persistance des données |
| Auth Security | `code-development:auth-security` — Conformité PCI et sécurité des paiements |
| Finance | `entreprise:finance` — Modèle de monétisation et métriques SaaS |
| Juridique | `entreprise:juridique` — Réglementation des paiements et CGV |
| Product Analytics | `code-development:product-analytics` — Métriques de conversion et funnel |

## Additional Resources

Consulter les fichiers de reference pour un approfondissement detaille :

- **[Stripe Integration](./references/stripe-integration.md)** : Stripe Checkout vs Elements vs Payment Links, Payment Intents & Setup Intents flows, Stripe Connect (Standard/Express/Custom), webhooks best practices (idempotency, retry logic, signature verification), Stripe CLI pour le testing, embedded components, Adaptive Pricing.

- **[Subscription & Billing](./references/subscription-billing.md)** : Cycle de vie des abonnements, periodes d'essai & grace periods, proration & changements de plan, gestion des factures, dunning & recuperation des paiements echoues (Smart Retries), metered/usage-based billing, Stripe Billing Portal, Stripe Revenue Recognition.

- **[PCI Compliance](./references/pci-compliance.md)** : PCI-DSS overview (SAQ levels A/A-EP/D), tokenisation, formulaires de paiement securises, reduction du scope PCI (Stripe.js, iframes), documentation de conformite, SCA/3D Secure 2, types de methodes de paiement (cartes, SEPA, Apple Pay, Google Pay, BNPL).

- **[Revenue & Integration](./references/revenue-integration.md)** : Revenue recognition (ASC 606, IFRS 15), Stripe Tax, integration comptable (journal entries, ERP sync), reporting financier & reconciliation, gestion des remboursements/litiges/chargebacks, multi-devise & FX, Stripe Sigma & Data Pipeline.
