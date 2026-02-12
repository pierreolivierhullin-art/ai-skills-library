# PCI Compliance & Payment Security

Reference approfondie sur la conformite PCI-DSS, la securisation des paiements, SCA/3D Secure et les methodes de paiement.

---

## Table of Contents

1. [PCI-DSS Overview](#pci-dss-overview)
2. [SAQ Levels & Scope Reduction](#saq-levels--scope-reduction)
3. [Tokenization & Secure Forms](#tokenization--secure-forms)
4. [SCA & 3D Secure 2](#sca--3d-secure-2)
5. [Payment Methods Deep Dive](#payment-methods-deep-dive)
6. [Compliance Documentation](#compliance-documentation)
7. [Security Best Practices](#security-best-practices)

---

## PCI-DSS Overview

### Qu'est-ce que PCI-DSS ?

Le Payment Card Industry Data Security Standard (PCI-DSS) est un ensemble d'exigences de securite pour toute entite qui stocke, traite ou transmet des donnees de cartes de paiement. La version 4.0 (en vigueur depuis mars 2024, pleine conformite requise depuis mars 2025) introduit de nouvelles exigences incluant une approche risk-based, l'authentification multi-facteur etendue et la securisation des scripts JavaScript.

### Les 12 exigences PCI-DSS 4.0

| # | Exigence | Impact developpeur |
|---|----------|-------------------|
| 1 | Installer et maintenir des controles de securite reseau | Firewall, segmentation |
| 2 | Appliquer des configurations securisees a tous les composants | Durcissement des serveurs |
| 3 | Proteger les donnees de comptes stockees | Chiffrement, tokenisation |
| 4 | Proteger les donnees en transit avec un chiffrement fort | TLS 1.2+ partout |
| 5 | Proteger contre les logiciels malveillants | Anti-malware, scanning |
| 6 | Developper et maintenir des systemes securises | SDLC, revue de code, patching |
| 7 | Restreindre l'acces aux donnees de carte par besoin metier | Moindre privilege |
| 8 | Identifier et authentifier les acces aux composants systeme | MFA, password policies |
| 9 | Restreindre l'acces physique aux donnees de carte | N/A pour le cloud |
| 10 | Logger et monitorer tous les acces | Audit trails, SIEM |
| 11 | Tester regulierement les systemes de securite | Pentests, scans vulnerabilites |
| 12 | Supporter la securite avec des politiques organisationnelles | Policies, formation |

### Nouveautes PCI-DSS 4.0

- **Approche personnalisee** : possibilite de definir des controles compensatoires custom justifies par une analyse de risque.
- **Gestion des scripts JavaScript** : obligation de maintenir un inventaire des scripts tiers charges dans les pages de paiement et de monitorer leur integrite (exigence 6.4.3).
- **MFA pour tous les acces a l'environnement de cartes** : pas seulement les acces administratifs.
- **Detection d'attaques automatisee** : systemes de detection d'intrusion (IDS/IPS) avec reponse automatisee.

---

## SAQ Levels & Scope Reduction

### Self-Assessment Questionnaires

Le type de SAQ determine la complexite de la conformite. Avec Stripe, viser le SAQ-A :

| SAQ | Complexite | Conditions | Nombre de controles |
|-----|-----------|------------|---------------------|
| **SAQ-A** | Minimale | Tous les traitements de carte delegues a un prestataire PCI (Stripe). Aucune donnee de carte ne touche les serveurs. | ~20 questions |
| SAQ-A-EP | Moyenne | Le site web sert les pages de paiement mais ne traite pas les donnees de carte. Scripts third-party sur la page. | ~140 questions |
| SAQ-D | Maximale | Le merchant traite, stocke ou transmet des donnees de carte. | ~300+ controles |

### Comment rester en SAQ-A avec Stripe

Respecter ces regles strictement pour maintenir le SAQ-A :

1. **Utiliser exclusivement Stripe.js et le Payment Element** (ou Checkout / Payment Links). Les donnees de carte transitent directement du navigateur vers les serveurs Stripe via un iframe securise, sans toucher les serveurs de l'application.

2. **Ne jamais manipuler de numeros de carte** cote serveur. Les APIs Stripe retournent des PaymentMethod objects avec les 4 derniers chiffres uniquement (`card.last4`). Ne jamais logger, stocker ou transmettre le `client_secret` d'un Payment Intent dans les logs.

3. **Charger Stripe.js depuis le CDN Stripe** (`https://js.stripe.com/v3/`). Ne jamais heberger une copie locale de Stripe.js. Utiliser `@stripe/stripe-js` via npm qui charge dynamiquement depuis le CDN.

4. **Servir les pages de paiement en HTTPS** exclusivement. Configurer HSTS avec preload. Utiliser TLS 1.2 minimum (preferer TLS 1.3).

5. **Inventorier et monitorer les scripts tiers** sur les pages contenant le Payment Element (exigence PCI-DSS 4.0 6.4.3). Utiliser Content Security Policy (CSP) pour restreindre les sources de scripts autorisees.

```html
<!-- CSP recommandee pour les pages avec Stripe -->
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' https://js.stripe.com https://maps.googleapis.com;
  frame-src https://js.stripe.com https://hooks.stripe.com;
  connect-src 'self' https://api.stripe.com;
  img-src 'self' https://*.stripe.com;
  style-src 'self' 'unsafe-inline';
">
```

### Passage au SAQ-A-EP

Si l'application ne peut pas utiliser le Payment Element en iframe (cas rares), le SAQ-A-EP s'applique. Exigences supplementaires :

- Scanner les vulnerabilites trimestriellement avec un ASV (Approved Scanning Vendor)
- Mettre en place un WAF (Web Application Firewall)
- Documenter les flux de donnees de carte
- Former les developpeurs a la securite des applications de paiement

### Diagramme de decision SAQ

```
L'application utilise Payment Links ou Checkout hosted ?
  -> SAQ-A (scope minimal)

L'application utilise le Payment Element ou Embedded Checkout ?
  -> Les donnees de carte passent-elles par les serveurs de l'application ?
    -> Non (iframe Stripe.js) -> SAQ-A
    -> Oui (jamais avec Stripe) -> SAQ-D (a eviter)

L'application utilise l'API Stripe directement avec des numeros de carte ?
  -> SAQ-D (scope maximal, a eviter absolument)
```

---

## Tokenization & Secure Forms

### Fonctionnement de la tokenisation

Stripe tokenise les donnees de carte dans le navigateur. Le flux :

1. Le client saisit ses donnees de carte dans le Payment Element (iframe Stripe)
2. Stripe.js envoie les donnees directement aux serveurs Stripe (pas au serveur de l'application)
3. Stripe cree un PaymentMethod (`pm_xxx`) et le retourne au frontend
4. Le frontend transmet le PaymentMethod ID au backend
5. Le backend utilise le PaymentMethod ID pour creer un Payment Intent ou un Setup Intent

A aucun moment le serveur de l'application ne voit les donnees de carte completes.

### Stripe.js Security Model

```typescript
// Stripe.js charge un iframe securise cross-origin
// Les donnees saisies dans le Payment Element ne sont jamais accessibles
// au JavaScript de la page parente (Same-Origin Policy)

// Initialisation securisee
const stripe = await loadStripe('pk_xxx', {
  // Optionnel : configurer le locale
  locale: 'fr',
  // Optionnel : specifier la version de l'API
  apiVersion: '2024-12-18.acacia',
});

// Le Payment Element est un composant iframe securise
// Aucun acces DOM aux champs de carte depuis le JavaScript parent
const elements = stripe.elements({
  clientSecret,
  loader: 'auto', // ou 'always' pour afficher un skeleton loader
  appearance: {
    theme: 'stripe',
    rules: {
      '.Input': {
        border: '1px solid #e0e0e0',
        borderRadius: '8px',
        padding: '12px',
      },
      '.Input:focus': {
        borderColor: '#0570de',
        boxShadow: '0 0 0 1px #0570de',
      },
      '.Label': {
        fontSize: '14px',
        fontWeight: '500',
      },
    },
  },
});
```

### Protection contre les attaques de scripts

PCI-DSS 4.0 exige de proteger l'integrite des scripts sur les pages de paiement :

```typescript
// Utiliser Subresource Integrity (SRI) pour Stripe.js
// Note : Stripe.js via npm (@stripe/stripe-js) gere automatiquement le chargement
// Pour un chargement manuel, utiliser le CDN officiel

// Content-Security-Policy stricte
// report-uri pour monitorer les violations en production
const cspHeader = [
  "default-src 'self'",
  "script-src 'self' https://js.stripe.com",
  "frame-src https://js.stripe.com https://hooks.stripe.com",
  "connect-src 'self' https://api.stripe.com",
  "report-uri https://csp.example.com/report",
].join('; ');
```

---

## SCA & 3D Secure 2

### Strong Customer Authentication (SCA)

La directive europeenne PSD2 impose le SCA pour les paiements electroniques dans l'EEE (Espace Economique Europeen). Le SCA requiert au moins 2 des 3 facteurs :

| Facteur | Description | Exemples |
|---------|-------------|----------|
| Knowledge | Quelque chose que le client sait | Code PIN, mot de passe |
| Possession | Quelque chose que le client possede | Telephone, carte physique |
| Inherence | Quelque chose que le client est | Empreinte digitale, reconnaissance faciale |

### 3D Secure 2 avec Stripe

Stripe gere automatiquement 3D Secure 2 via le Payment Element. Configurer le comportement :

```typescript
// Configuration automatique (recommandee)
const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000,
  currency: 'eur',
  customer: customerId,
  automatic_payment_methods: { enabled: true },
  // Stripe decide automatiquement quand declencher 3DS
  // base sur le risque, les exemptions et les exigences reglementaires
});

// Configuration manuelle (cas avances)
const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000,
  currency: 'eur',
  payment_method_options: {
    card: {
      request_three_d_secure: 'any', // 'any' = toujours, 'automatic' = selon le risque
    },
  },
});
```

### Exemptions SCA

Certaines transactions peuvent etre exemptees de SCA. Stripe gere automatiquement les demandes d'exemption :

| Exemption | Conditions | Gestion Stripe |
|-----------|-----------|---------------|
| Low-value | Transaction < 30 EUR (cumul < 100 EUR ou 5 transactions) | Automatique |
| Low-risk (TRA) | Taux de fraude du processeur < seuils fixes | Automatique |
| Recurring | Paiements recurrents fixes apres le premier (avec SCA) | Automatique |
| Merchant-initiated | Paiements off-session inities par le merchant | Via `off_session: true` |
| Corporate | Cartes d'entreprise securisees | Detection automatique |

```typescript
// Premier paiement d'un abonnement : SCA requis
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: 'price_xxx' }],
  payment_settings: {
    payment_method_options: {
      card: {
        request_three_d_secure: 'automatic',
      },
    },
  },
});

// Paiements recurrents suivants : exemption automatique (recurring)
// Stripe gere automatiquement l'exemption via le mandat initial

// Paiement off-session : exemption merchant-initiated
const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000,
  currency: 'eur',
  customer: customerId,
  payment_method: savedMethodId,
  off_session: true,
  confirm: true,
  // Si SCA est quand meme requis, Stripe leve une exception
  // Capturer l'erreur et notifier le client
});
```

### Flux 3D Secure cote client

```typescript
// Le Payment Element gere automatiquement le challenge 3DS
// Pour un flux custom avec le CardElement legacy :

const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
  payment_method: {
    card: cardElement,
    billing_details: { name: 'Nom Client' },
  },
});

if (error) {
  if (error.type === 'card_error' || error.type === 'validation_error') {
    // Afficher l'erreur au client
    showError(error.message);
  } else {
    // Erreur serveur inattendue
    showError('An unexpected error occurred.');
  }
} else if (paymentIntent.status === 'requires_action') {
  // 3DS est gere automatiquement par confirmCardPayment
  // Ce cas ne devrait pas se produire avec le Payment Element
} else if (paymentIntent.status === 'succeeded') {
  // Paiement reussi
  showSuccess();
}
```

---

## Payment Methods Deep Dive

### Cards

Methode de paiement la plus universelle. Supporter Visa, Mastercard, American Express au minimum. Ajouter Discover, Diners, JCB, UnionPay selon les marches cibles.

```typescript
// Activer les methodes de paiement automatiquement
const paymentIntent = await stripe.paymentIntents.create({
  amount: 5000,
  currency: 'eur',
  automatic_payment_methods: { enabled: true },
  // Stripe determine automatiquement les methodes pertinentes
  // selon la devise, le montant, la localisation du client
});

// Ou specifier manuellement
const paymentIntent = await stripe.paymentIntents.create({
  amount: 5000,
  currency: 'eur',
  payment_method_types: ['card', 'sepa_debit', 'ideal', 'bancontact'],
});
```

### SEPA Direct Debit

Prelevement bancaire europeen. Paiement differe (5-14 jours ouvrables). Necessite un mandat (consentement du client). Ideal pour les abonnements en zone euro. Frais plus bas que les cartes (generalement 0.35 EUR fixe).

```typescript
// Le Payment Element gere automatiquement SEPA
// Le client saisit son IBAN et signe electroniquement le mandat
// Stripe cree le mandat et le Payment Method automatiquement

// Pour les paiements recurrents via SEPA :
const setupIntent = await stripe.setupIntents.create({
  customer: customerId,
  payment_method_types: ['sepa_debit'],
  mandate_data: {
    customer_acceptance: {
      type: 'online',
      online: {
        ip_address: req.ip,
        user_agent: req.headers['user-agent'],
      },
    },
  },
});
```

Particularites SEPA :
- Le paiement passe en `processing` immediatement (pas de confirmation instantanee)
- Confirmer l'acces uniquement apres le webhook `payment_intent.succeeded` (5-14 jours)
- Gerer le webhook `payment_intent.payment_failed` pour les rejets SEPA
- Les mandats SEPA peuvent etre reutilises pour des paiements recurrents
- Le client peut contester un prelevement SEPA pendant 8 semaines (13 mois si non autorise)

### Apple Pay & Google Pay

Wallets mobiles avec authentification biometrique integree. Le SCA est automatiquement satisfait par l'authentification biometrique du device. Taux de conversion superieur aux cartes classiques.

```typescript
// Le Payment Element inclut automatiquement Apple Pay et Google Pay
// Conditions :
// - Apple Pay : site servi en HTTPS, domaine verifie dans le Dashboard Stripe
// - Google Pay : aucune configuration supplementaire

// Verifier le domaine pour Apple Pay (Dashboard ou API)
await stripe.applePayDomains.create({
  domain_name: 'example.com',
});

// Placer le fichier de verification Apple Pay
// https://example.com/.well-known/apple-developer-merchantid-domain-association
// Le contenu est fourni par Stripe dans le Dashboard

// Pour un bouton Express Checkout Element (Apple Pay / Google Pay / Link)
const expressCheckoutElement = elements.create('expressCheckout', {
  buttonType: {
    applePay: 'buy',
    googlePay: 'buy',
  },
  layout: {
    maxColumns: 3,
    maxRows: 1,
  },
});
expressCheckoutElement.mount('#express-checkout');
```

### Buy Now Pay Later (BNPL)

Paiement fractionne : Klarna, Afterpay/Clearpay, Affirm. Le merchant recoit le paiement integral immediatement. Le client paie en plusieurs fois. Pas de support pour les paiements recurrents.

```typescript
// Activer BNPL dans le Payment Element
const paymentIntent = await stripe.paymentIntents.create({
  amount: 15000, // montants minimums varies selon le provider
  currency: 'eur',
  automatic_payment_methods: { enabled: true },
  // Klarna, Afterpay, Affirm apparaissent automatiquement
  // si le montant et la devise sont eligibles
});

// Montants minimums (approximatifs) :
// Klarna : 1 EUR (Pay in 3/4), 35 EUR (Financing)
// Afterpay : 1 USD/EUR/GBP (varie par region)
// Affirm : 50 USD
```

### Link (Stripe)

Solution d'achat rapide de Stripe. Le client sauvegarde ses informations de paiement et de livraison une seule fois. Les achats suivants se font en un clic avec verification par SMS. Active automatiquement dans le Payment Element.

```typescript
// Link est active par defaut dans le Payment Element
// Desactiver si necessaire :
const paymentElement = elements.create('payment', {
  wallets: {
    link: 'never', // ou 'auto' (defaut)
  },
});
```

---

## Compliance Documentation

### Documents a maintenir

1. **Data Flow Diagram** : cartographier le flux des donnees de paiement dans l'architecture. Identifier chaque point de contact avec les donnees sensibles. Avec Stripe Payment Element, le diagramme montre que les donnees de carte transitent exclusivement entre le navigateur du client et les serveurs Stripe.

2. **SAQ (Self-Assessment Questionnaire)** : remplir le SAQ-A annuellement. Disponible sur le site du PCI Security Standards Council. Stripe fournit un guide pour remplir le SAQ-A avec leur solution.

3. **Attestation of Compliance (AoC)** : document attestant de la conformite. Genere automatiquement avec le SAQ. A fournir aux partenaires, banques et acquireurs sur demande.

4. **Incident Response Plan** : plan de reponse en cas de compromission de donnees de paiement. Definir les roles, les procedures de notification et les mesures correctives.

5. **Inventaire des scripts** (PCI-DSS 4.0, exigence 6.4.3) : maintenir un inventaire a jour de tous les scripts JavaScript charges sur les pages de paiement. Justifier chaque script. Monitorer les modifications non autorisees.

### Checklist annuelle PCI

```
Trimestre :
  [ ] Scanner les vulnerabilites avec un ASV (si SAQ-A-EP ou D)
  [ ] Verifier les certificats TLS et leur validite
  [ ] Auditer les scripts tiers sur les pages de paiement
  [ ] Verifier les logs d'acces aux systemes de paiement

Annuellement :
  [ ] Remplir le SAQ (A, A-EP ou D selon le scope)
  [ ] Signer l'Attestation of Compliance
  [ ] Revoir le Data Flow Diagram
  [ ] Former les developpeurs a la securite des paiements
  [ ] Tester le plan de reponse aux incidents
  [ ] Renouveler les cles API Stripe (rotation)
  [ ] Auditer les permissions d'acces au Dashboard Stripe
```

### Rotation des cles API

Stripe fournit des cles roulantes (rolling keys) pour effectuer des rotations sans interruption :

```typescript
// Processus de rotation des cles API Stripe :
// 1. Generer une nouvelle cle dans Dashboard > Developers > API Keys > Roll key
// 2. Stripe fournit une nouvelle cle qui fonctionne en parallele de l'ancienne
// 3. Deployer la nouvelle cle dans l'application
// 4. Verifier que tout fonctionne avec la nouvelle cle
// 5. Revoquer l'ancienne cle dans le Dashboard

// Stocker les cles dans un secret manager
// JAMAIS dans le code source, les fichiers de configuration ou les variables d'environnement en clair
```

---

## Security Best Practices

### Rate Limiting sur les endpoints de paiement

```typescript
// Appliquer un rate limiting strict sur les endpoints sensibles
import rateLimit from 'express-rate-limit';

const paymentLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // max 10 tentatives de paiement par IP
  message: 'Too many payment attempts. Please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

app.post('/api/create-payment-intent', paymentLimiter, createPaymentIntent);
app.post('/api/create-checkout-session', paymentLimiter, createCheckoutSession);

// Rate limiting plus restrictif sur les webhooks (protection DDoS)
const webhookLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 100, // max 100 webhooks par minute (ajuster selon le volume)
});

app.post('/webhooks/stripe', webhookLimiter, handleWebhook);
```

### Logging securise

```typescript
// Ne JAMAIS logger :
// - Le numero de carte complet
// - Le CVV/CVC
// - Le client_secret d'un Payment Intent
// - Les cles API Stripe (sk_xxx)
// - Le webhook signing secret (whsec_xxx)

// Logger de maniere securisee :
function logPaymentEvent(paymentIntent: Stripe.PaymentIntent): void {
  logger.info('Payment processed', {
    paymentIntentId: paymentIntent.id,
    amount: paymentIntent.amount,
    currency: paymentIntent.currency,
    status: paymentIntent.status,
    customerId: paymentIntent.customer,
    last4: paymentIntent.payment_method_details?.card?.last4,
    // NE PAS inclure : client_secret, raw payment_method data
  });
}
```

### Protection contre la fraude

Stripe Radar fournit une detection de fraude integree. Configurer des regles custom :

```
// Regles Radar recommandees (Dashboard > Radar > Rules)

// Bloquer les cartes prepayees pour les abonnements
Block if :card_funding: = 'prepaid' AND :is_recurring:

// Bloquer les pays a haut risque
Block if :card_country: in ('XX', 'YY') // adapter selon le business

// Requete 3DS pour les montants eleves
Request 3D Secure if :amount_in_eur: > 50000

// Bloquer si le score de risque est eleve
Block if :risk_score: >= 85

// Requete de review si score modere
Review if :risk_score: >= 65 AND :risk_score: < 85
```

### Webhook Endpoint Security

```typescript
// Checklist de securite pour l'endpoint webhook :

// 1. HTTPS uniquement (Stripe refuse d'envoyer des webhooks en HTTP)
// 2. Verification de signature obligatoire
// 3. Le body doit etre lu en mode raw (pas de JSON parsing avant la verification)
// 4. Timeout strict (repondre en < 5 secondes)
// 5. Rate limiting pour proteger contre les abus
// 6. Pas d'exposition de details d'erreur dans la reponse

// Configuration Express.js correcte
app.post('/webhooks/stripe',
  express.raw({ type: 'application/json' }), // raw body AVANT json parsing
  webhookLimiter,
  async (req, res) => {
    try {
      const event = stripe.webhooks.constructEvent(
        req.body,
        req.headers['stripe-signature'],
        process.env.STRIPE_WEBHOOK_SECRET
      );
      await processEvent(event);
      res.json({ received: true });
    } catch (err) {
      if (err.type === 'StripeSignatureVerificationError') {
        res.status(400).send('Invalid signature');
      } else {
        res.status(500).send('Internal error');
      }
    }
  }
);
```

---

## Summary Checklist

Verifier ces points sur chaque implementation de paiement :

- [ ] Le Payment Element (iframe) est utilise -- les donnees de carte ne touchent jamais le serveur
- [ ] Le SAQ-A est maintenu -- aucune donnee de carte n'est stockee, traitee ou transmise
- [ ] Les pages de paiement sont servies exclusivement en HTTPS avec HSTS
- [ ] Content-Security-Policy est configuree pour restreindre les scripts sur les pages de paiement
- [ ] Les scripts tiers sur les pages de paiement sont inventories (PCI-DSS 4.0 6.4.3)
- [ ] SCA/3D Secure est configure en mode automatique
- [ ] Les exemptions SCA sont gerees automatiquement par Stripe
- [ ] Les cles API sont stockees dans un secret manager et rotees regulierement
- [ ] Aucune donnee sensible n'est loggee (numeros de carte, CVV, client_secret, cles API)
- [ ] Rate limiting est applique sur les endpoints de paiement
- [ ] Stripe Radar est configure avec des regles custom adaptees au business
- [ ] Le domaine est verifie pour Apple Pay
- [ ] L'endpoint webhook verifie la signature et lit le body en mode raw
- [ ] Le SAQ est rempli et l'AoC est signee annuellement
- [ ] Le plan de reponse aux incidents couvre les compromissions de paiement
