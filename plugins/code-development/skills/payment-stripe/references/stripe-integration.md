# Stripe Integration Patterns

Reference approfondie sur les modeles d'integration Stripe, les flux de paiement, Stripe Connect et les webhooks.

---

## Table of Contents

1. [Checkout vs Elements vs Payment Links](#checkout-vs-elements-vs-payment-links)
2. [Payment Intents & Setup Intents](#payment-intents--setup-intents)
3. [Stripe Connect (Marketplaces)](#stripe-connect-marketplaces)
4. [Webhooks Best Practices](#webhooks-best-practices)
5. [Stripe CLI & Development Workflow](#stripe-cli--development-workflow)
6. [Embedded Components & Stripe Apps](#embedded-components--stripe-apps)
7. [Adaptive Pricing & Multi-Currency](#adaptive-pricing--multi-currency)

---

## Checkout vs Elements vs Payment Links

### Payment Links

Utiliser les Payment Links pour les cas sans developpement. Creer un lien directement depuis le Dashboard Stripe ou via l'API. Le lien redirige vers une page de paiement hebergee par Stripe. Ideal pour les freelances, les associations, les campagnes marketing et les MVP rapides.

Limites : personnalisation reduite, pas de logique metier avancee, pas de controle sur le tunnel de conversion. Ne pas utiliser pour un e-commerce mature ou un SaaS avec onboarding complexe.

```typescript
// Creation d'un Payment Link via l'API
const paymentLink = await stripe.paymentLinks.create({
  line_items: [{ price: 'price_xxx', quantity: 1 }],
  after_completion: {
    type: 'redirect',
    redirect: { url: 'https://example.com/success' },
  },
  automatic_tax: { enabled: true },
  allow_promotion_codes: true,
});
// Partager paymentLink.url par email, SMS, QR code
```

### Stripe Checkout (Hosted)

Utiliser le mode heberge (`mode: 'payment'` ou `mode: 'subscription'`) pour une integration rapide avec un tunnel de conversion optimise par Stripe. La page est hebergee sur le domaine `checkout.stripe.com`. Stripe gere automatiquement les methodes de paiement, les taxes, les reductions, les emails de recus et la conformite SCA.

```typescript
// Cote serveur : creer une Checkout Session
const session = await stripe.checkout.sessions.create({
  mode: 'payment', // ou 'subscription' ou 'setup'
  line_items: [
    {
      price: 'price_xxx',
      quantity: 1,
    },
  ],
  customer: customerId, // rattacher au customer existant
  metadata: { orderId: order.id, userId: user.id },
  success_url: 'https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
  cancel_url: 'https://example.com/cancel',
  automatic_tax: { enabled: true },
  allow_promotion_codes: true,
  billing_address_collection: 'required',
  phone_number_collection: { enabled: true },
  consent_collection: {
    terms_of_service: 'required',
  },
});

// Cote client : rediriger vers Checkout
const stripe = Stripe('pk_xxx');
stripe.redirectToCheckout({ sessionId: session.id });
```

### Stripe Checkout (Embedded)

Utiliser le mode embarque (`ui_mode: 'embedded'`) pour integrer le formulaire de paiement directement dans la page sans redirection. Le composant s'affiche dans un conteneur HTML. Conserver les avantages de Checkout (conformite PCI, methodes de paiement auto, taxes) tout en gardant le controle du design de la page.

```typescript
// Cote serveur : creer une Checkout Session avec ui_mode embedded
const session = await stripe.checkout.sessions.create({
  mode: 'payment',
  ui_mode: 'embedded',
  line_items: [{ price: 'price_xxx', quantity: 1 }],
  return_url: 'https://example.com/return?session_id={CHECKOUT_SESSION_ID}',
  automatic_tax: { enabled: true },
});

// Cote client : initialiser l'Embedded Checkout
const stripe = Stripe('pk_xxx');
const checkout = await stripe.initEmbeddedCheckout({
  clientSecret: session.client_secret,
});
checkout.mount('#checkout-container');

// Demontage propre lors de la navigation
checkout.destroy();
```

### Payment Element (Custom Integration)

Utiliser le Payment Element pour un controle total du formulaire et du flux de paiement. Creer un Payment Intent cote serveur, passer le `client_secret` au client, monter le Payment Element et confirmer le paiement. Gerer manuellement les etats, les redirections 3D Secure et les erreurs.

```typescript
// Cote serveur : creer un Payment Intent
const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000, // montant en centimes
  currency: 'eur',
  customer: customerId,
  automatic_payment_methods: { enabled: true },
  metadata: { orderId: order.id },
}, {
  idempotencyKey: `order_${order.id}_payment`,
});

// Retourner le client_secret au frontend
return { clientSecret: paymentIntent.client_secret };
```

```typescript
// Cote client : monter le Payment Element et confirmer
import { loadStripe } from '@stripe/stripe-js';

const stripe = await loadStripe('pk_xxx');
const elements = stripe.elements({
  clientSecret,
  appearance: {
    theme: 'stripe', // ou 'night', 'flat', ou theme custom
    variables: {
      colorPrimary: '#0570de',
      borderRadius: '8px',
    },
  },
});

const paymentElement = elements.create('payment', {
  layout: 'accordion', // ou 'tabs'
  defaultValues: {
    billingDetails: {
      name: user.name,
      email: user.email,
    },
  },
});
paymentElement.mount('#payment-element');

// Confirmation du paiement
const { error } = await stripe.confirmPayment({
  elements,
  confirmParams: {
    return_url: 'https://example.com/payment/complete',
  },
});

if (error) {
  // Afficher l'erreur au client (error.type, error.message)
  showError(error.message);
}
// Si pas d'erreur, le navigateur redirige vers return_url
```

### Comparaison decision

| Critere | Payment Links | Checkout Hosted | Checkout Embedded | Payment Element |
|---------|--------------|----------------|-------------------|----------------|
| Temps d'integration | Minutes | Heures | Heures | Jours |
| Personnalisation UI | Nulle | Faible | Moyenne | Totale |
| PCI SAQ Level | A | A | A | A |
| SCA/3D Secure | Auto | Auto | Auto | Auto |
| Methodes de paiement | Auto | Auto | Auto | Auto |
| Taxes automatiques | Oui | Oui | Oui | Manuel |
| Coupons/promotions | Oui | Oui | Oui | Manuel |
| Controle du tunnel | Non | Faible | Moyen | Total |
| Adaptable marketplace | Non | Oui (Connect) | Oui (Connect) | Oui (Connect) |

---

## Payment Intents & Setup Intents

### Payment Intent Lifecycle

Le Payment Intent represente l'intention de collecter un paiement. Comprendre son cycle de vie est essentiel :

```
created -> requires_payment_method -> requires_confirmation -> requires_action -> processing -> succeeded
                                                                                            -> requires_capture (si capture manuelle)
                                                                                            -> canceled
                    -> payment_failed (apres echec)
```

Etats cles :

- **requires_payment_method** : l'intent attend qu'une methode de paiement soit attachee. Le client doit soumettre le Payment Element.
- **requires_action** : une action supplementaire est requise (3D Secure, redirection bancaire). Stripe.js gere automatiquement l'affichage du challenge.
- **processing** : le paiement est en cours de traitement (courant pour les virements SEPA, ACH). Attendre le webhook.
- **succeeded** : le paiement est confirme. Declencher la logique metier (activation de commande, envoi de produit).
- **requires_capture** : le paiement est autorise mais non capture. Utiliser pour les reservations ou les pre-autorisations (capture dans 7 jours max).

```typescript
// Capture manuelle (pre-autorisation)
const paymentIntent = await stripe.paymentIntents.create({
  amount: 5000,
  currency: 'eur',
  capture_method: 'manual', // autoriser sans capturer
  customer: customerId,
  automatic_payment_methods: { enabled: true },
});

// Plus tard, capturer le montant final (peut etre inferieur)
await stripe.paymentIntents.capture(paymentIntent.id, {
  amount_to_capture: 4500, // capturer un montant reduit
});
```

### Setup Intent

Le Setup Intent sert a collecter et sauvegarder une methode de paiement sans effectuer de paiement immediat. Utiliser pour :

- Enregistrer une carte pour des paiements futurs (abonnements, paiements recurrents)
- Sauvegarder un mandat SEPA pour des prelevements futurs
- Configurer les wallets (Apple Pay, Google Pay) pour un usage ulterieur

```typescript
// Cote serveur : creer un Setup Intent
const setupIntent = await stripe.setupIntents.create({
  customer: customerId,
  automatic_payment_methods: { enabled: true },
  usage: 'off_session', // pour les paiements futurs sans le client present
});

// Cote client : confirmer le Setup Intent
const { error } = await stripe.confirmSetup({
  elements,
  confirmParams: {
    return_url: 'https://example.com/setup/complete',
  },
});

// Apres confirmation, la PaymentMethod est attachee au Customer
// Utiliser pour creer un abonnement ou un paiement off-session
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: 'price_xxx' }],
  default_payment_method: setupIntent.payment_method,
});
```

### Off-Session Payments

Effectuer des paiements quand le client n'est pas present (renouvellement d'abonnement, factures recurrentes). Necessiter une methode de paiement sauvegardee via un Setup Intent prealable ou un consentement explicite.

```typescript
// Paiement off-session avec une methode sauvegardee
try {
  const paymentIntent = await stripe.paymentIntents.create({
    amount: 1500,
    currency: 'eur',
    customer: customerId,
    payment_method: savedPaymentMethodId,
    off_session: true,
    confirm: true,
  });
  // Paiement reussi
} catch (err) {
  if (err.code === 'authentication_required') {
    // 3D Secure requis : envoyer un email au client pour completer l'authentification
    await notifyCustomerForAuthentication(customerId, err.raw.payment_intent.id);
  }
}
```

---

## Stripe Connect (Marketplaces)

### Types de comptes Connect

| Type | Onboarding | Dashboard | Responsabilite |
|------|-----------|-----------|---------------|
| Standard | Stripe gere | Dashboard Stripe complet | Vendeur responsable |
| Express | Stripe gere (simplifie) | Dashboard Stripe lite | Partage platform/vendeur |
| Custom | Platform gere entierement | Aucun (a construire) | Platform 100% responsable |

### Standard Accounts

Utiliser pour les marketplaces ou les vendeurs sont des entreprises etablies avec leur propre compte Stripe. Onboarding via OAuth. La platform redirige vers Stripe, le vendeur connecte ou cree un compte. Ideal quand les vendeurs ont deja un compte Stripe ou doivent gerer leur propre comptabilite.

```typescript
// Creer un Account Link pour l'onboarding
const accountLink = await stripe.accountLinks.create({
  account: connectedAccountId,
  refresh_url: 'https://platform.com/connect/refresh',
  return_url: 'https://platform.com/connect/complete',
  type: 'account_onboarding',
});
// Rediriger le vendeur vers accountLink.url
```

### Express Accounts

Utiliser pour les marketplaces qui souhaitent un onboarding simplifie. Stripe gere la collecte des informations KYC. Le vendeur a acces a un dashboard Stripe reduit (Express Dashboard) pour voir ses paiements et payouts. La platform peut personnaliser les couleurs et le branding.

```typescript
// Creer un compte Express
const account = await stripe.accounts.create({
  type: 'express',
  country: 'FR',
  email: 'vendor@example.com',
  capabilities: {
    card_payments: { requested: true },
    transfers: { requested: true },
  },
  business_type: 'individual',
  business_profile: {
    mcc: '5734', // Computer software stores
    url: 'https://vendor-website.com',
  },
});
```

### Custom Accounts

Utiliser pour un controle total sur l'experience. La platform gere l'UI d'onboarding, la collecte KYC (via l'API ou les embedded components), et le dashboard vendeur. Responsabilite totale de la platform sur la conformite, les litiges et la communication avec les vendeurs.

Privilegier les embedded onboarding components de Stripe Connect pour reduire la charge de developpement tout en gardant le controle :

```typescript
// Embedded onboarding component (recommande pour Custom accounts)
import { ConnectAccountOnboarding } from '@stripe/react-connect-js';

function VendorOnboarding({ connectedAccountId }) {
  return (
    <ConnectAccountOnboarding
      onExit={() => console.log('Onboarding completed or exited')}
    />
  );
}
```

### Payment Flows avec Connect

Trois modeles de flux de paiement :

**Direct Charges** : le paiement est cree sur le compte du vendeur. La platform prend une commission via `application_fee_amount`. Ideal pour les Standard accounts.

```typescript
const paymentIntent = await stripe.paymentIntents.create({
  amount: 10000,
  currency: 'eur',
  application_fee_amount: 1500, // commission platform de 15%
}, {
  stripeAccount: connectedAccountId, // direct charge sur le compte vendeur
});
```

**Destination Charges** : le paiement est cree sur le compte de la platform, puis transfere au vendeur. La platform controle le flux.

```typescript
const paymentIntent = await stripe.paymentIntents.create({
  amount: 10000,
  currency: 'eur',
  transfer_data: {
    destination: connectedAccountId,
    amount: 8500, // montant transfere au vendeur (platform garde 1500)
  },
});
```

**Separate Charges and Transfers** : le paiement est collecte par la platform, puis les transferts sont effectues manuellement. Utiliser pour les paniers multi-vendeurs ou les paiements differees.

```typescript
// Etape 1 : collecter le paiement
const paymentIntent = await stripe.paymentIntents.create({
  amount: 10000,
  currency: 'eur',
  customer: customerId,
});

// Etape 2 : transferer aux vendeurs (peut etre differe)
const transfer = await stripe.transfers.create({
  amount: 5000,
  currency: 'eur',
  destination: vendorAccountId1,
  transfer_group: `order_${orderId}`,
});

const transfer2 = await stripe.transfers.create({
  amount: 3500,
  currency: 'eur',
  destination: vendorAccountId2,
  transfer_group: `order_${orderId}`,
});
// La platform conserve 1500 (10000 - 5000 - 3500)
```

---

## Webhooks Best Practices

### Signature Verification

Toujours verifier la signature du webhook pour s'assurer que l'evenement provient de Stripe. Ne jamais traiter un webhook sans verification.

```typescript
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

// Express.js example -- utiliser le body brut (raw)
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
  } catch (err) {
    console.error(`Webhook signature verification failed: ${err.message}`);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Traiter l'evenement
  handleWebhookEvent(event)
    .then(() => res.json({ received: true }))
    .catch((err) => {
      console.error(`Webhook handler error: ${err.message}`, { eventId: event.id });
      res.status(500).send('Internal error');
    });
});
```

### Idempotency Pattern

Garantir que le traitement d'un meme evenement plusieurs fois produit le meme resultat. Stripe peut reenvoyer des evenements en cas de timeout ou d'erreur.

```typescript
async function handleWebhookEvent(event: Stripe.Event): Promise<void> {
  // Verifier si l'evenement a deja ete traite
  const existing = await db.stripeEvents.findUnique({
    where: { eventId: event.id },
  });

  if (existing) {
    console.log(`Event ${event.id} already processed, skipping`);
    return;
  }

  // Traiter dans une transaction pour garantir l'atomicite
  await db.$transaction(async (tx) => {
    // Marquer l'evenement comme en cours de traitement
    await tx.stripeEvents.create({
      data: {
        eventId: event.id,
        type: event.type,
        processedAt: new Date(),
      },
    });

    // Dispatcher vers le handler appropriate
    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentSucceeded(tx, event.data.object as Stripe.PaymentIntent);
        break;
      case 'customer.subscription.updated':
        await handleSubscriptionUpdated(tx, event.data.object as Stripe.Subscription);
        break;
      case 'invoice.payment_failed':
        await handleInvoicePaymentFailed(tx, event.data.object as Stripe.Invoice);
        break;
      // ... autres types d'evenements
    }
  });
}
```

### Evenements critiques a ecouter

Configurer les webhooks pour recevoir au minimum ces evenements :

**Paiements :**
- `payment_intent.succeeded` : paiement confirme, declencher la livraison
- `payment_intent.payment_failed` : echec de paiement, notifier le client
- `charge.dispute.created` : litige ouvert, reagir dans les 7 jours

**Abonnements :**
- `customer.subscription.created` : nouvel abonnement actif
- `customer.subscription.updated` : changement de plan, statut, ou periode
- `customer.subscription.deleted` : abonnement annule, revoquer l'acces
- `invoice.payment_succeeded` : renouvellement d'abonnement reussi
- `invoice.payment_failed` : echec de renouvellement, declencher le dunning

**Checkout :**
- `checkout.session.completed` : session completee, traiter la commande
- `checkout.session.expired` : session expiree (apres 24h par defaut)

**Connect :**
- `account.updated` : statut du compte vendeur mis a jour (verification KYC)
- `payout.paid` : virement au vendeur effectue
- `payout.failed` : echec du virement, investiguer

### Retry Logic & Error Handling

Stripe retente les webhooks en echec (code HTTP 4xx/5xx ou timeout) avec un backoff exponentiel sur 3 jours, jusqu'a un maximum de 15 tentatives environ. Concevoir les handlers en consequence :

- Retourner un code 2xx rapidement (dans les 5 secondes). Traiter les operations longues de maniere asynchrone (queue, background job).
- Retourner 200 meme si l'evenement n'est pas pertinent pour l'application (type d'evenement non gere).
- Retourner 5xx uniquement en cas d'erreur transitoire (base de donnees indisponible, service externe down).
- Ne jamais retourner 4xx sauf pour les erreurs de signature (400).

```typescript
// Pattern : traitement asynchrone pour les operations longues
app.post('/webhooks/stripe', async (req, res) => {
  const event = verifyAndParseEvent(req);

  // Repondre rapidement a Stripe
  res.json({ received: true });

  // Traiter en arriere-plan
  await queue.add('stripe-webhook', {
    eventId: event.id,
    type: event.type,
    data: event.data,
  });
});
```

---

## Stripe CLI & Development Workflow

### Installation et configuration

Installer le Stripe CLI pour tester localement les webhooks, declencher des evenements et explorer l'API.

```bash
# Installation (macOS)
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Ecouter les webhooks en local
stripe listen --forward-to localhost:3000/webhooks/stripe

# Le CLI affiche le webhook signing secret (whsec_xxx)
# Utiliser ce secret pour la verification en developpement
```

### Tester les webhooks

```bash
# Declencher un evenement specifique
stripe trigger payment_intent.succeeded

# Declencher un flux complet d'abonnement
stripe trigger customer.subscription.created

# Declencher un evenement avec des donnees custom
stripe trigger invoice.payment_failed --override invoice:billing_reason=subscription_cycle

# Lister les evenements recents
stripe events list --limit 10

# Inspecter un evenement
stripe events retrieve evt_xxx
```

### Fixtures pour le testing

Creer des fixtures JSON pour reproduire des scenarios complexes :

```json
{
  "_meta": { "template_version": 0 },
  "fixtures": [
    {
      "name": "customer",
      "path": "/v1/customers",
      "method": "post",
      "params": {
        "email": "test@example.com",
        "name": "Test Customer"
      }
    },
    {
      "name": "payment_intent",
      "path": "/v1/payment_intents",
      "method": "post",
      "params": {
        "amount": 5000,
        "currency": "eur",
        "customer": "${customer:id}"
      }
    }
  ]
}
```

```bash
# Executer les fixtures
stripe fixtures path/to/fixture.json
```

### Bonnes pratiques de developpement

- Utiliser des cles de test (`sk_test_xxx`) exclusivement en developpement et staging. Ne jamais utiliser des cles de production en local.
- Utiliser les numeros de carte de test Stripe (`4242424242424242` pour succes, `4000000000003220` pour 3D Secure, `4000000000000002` pour declin).
- Configurer des webhook endpoints separes par environnement (dev, staging, production).
- Utiliser le mode test de Stripe pour tester les abonnements avec des periodes de facturation accelerees (test clocks).

### Test Clocks

Utiliser les Test Clocks pour simuler le passage du temps et tester les cycles d'abonnement, les periodes d'essai et les renouvellements sans attendre.

```typescript
// Creer un test clock
const testClock = await stripe.testHelpers.testClocks.create({
  frozen_time: Math.floor(Date.now() / 1000),
  name: 'Subscription lifecycle test',
});

// Creer un customer attache au test clock
const customer = await stripe.customers.create({
  email: 'test@example.com',
  test_clock: testClock.id,
});

// Creer un abonnement avec trial
const subscription = await stripe.subscriptions.create({
  customer: customer.id,
  items: [{ price: 'price_xxx' }],
  trial_period_days: 14,
});

// Avancer le temps de 15 jours (fin du trial)
await stripe.testHelpers.testClocks.advance(testClock.id, {
  frozen_time: Math.floor(Date.now() / 1000) + 15 * 24 * 3600,
});
// Verifier que l'abonnement est passe de 'trialing' a 'active'
```

---

## Embedded Components & Stripe Apps

### Embedded Components (Connect)

Stripe fournit des composants React pre-construits pour les platforms Connect. Utiliser ces composants pour reduire le temps de developpement tout en maintenant la conformite :

```typescript
import { ConnectComponentsProvider } from '@stripe/react-connect-js';
import {
  ConnectPayments,
  ConnectPayouts,
  ConnectAccountOnboarding,
  ConnectAccountManagement,
  ConnectNotificationBanner,
} from '@stripe/react-connect-js';

function VendorDashboard({ connectedAccountId }) {
  return (
    <ConnectComponentsProvider
      connectInstance={stripeConnectInstance}
    >
      <ConnectNotificationBanner />
      <ConnectPayments />
      <ConnectPayouts />
      <ConnectAccountManagement />
    </ConnectComponentsProvider>
  );
}
```

Composants disponibles : `ConnectPayments` (historique des paiements), `ConnectPayouts` (virements), `ConnectAccountOnboarding` (KYC), `ConnectAccountManagement` (parametres du compte), `ConnectNotificationBanner` (alertes de verification), `ConnectBalances` (soldes), `ConnectDocuments` (documents fiscaux).

### Stripe Apps

Creer des extensions Stripe Apps pour ajouter des fonctionnalites custom dans le Dashboard Stripe. Utiliser pour integrer des outils internes, afficher des donnees metier dans le contexte des paiements, ou automatiser des workflows.

```typescript
// stripe-app.json
{
  "id": "com.example.my-app",
  "version": "1.0.0",
  "name": "My Custom App",
  "permissions": [
    { "permission": "customer_read" },
    { "permission": "payment_intent_read" }
  ],
  "ui_extension": {
    "views": [
      {
        "viewport": "stripe.dashboard.customer.detail",
        "component": "CustomerView"
      }
    ]
  }
}
```

---

## Adaptive Pricing & Multi-Currency

### Adaptive Pricing

Activer Adaptive Pricing pour afficher automatiquement les prix dans la devise locale du client. Stripe gere la conversion de devises et le risque de change. Le vendeur recoit le paiement dans sa devise de reglement.

```typescript
// Activer Adaptive Pricing sur Checkout
const session = await stripe.checkout.sessions.create({
  mode: 'payment',
  line_items: [{ price: 'price_xxx', quantity: 1 }],
  // Adaptive Pricing s'active dans le Dashboard Stripe
  // sur chaque Price avec le flag "Adaptive pricing" active
  success_url: 'https://example.com/success',
});
```

Avantages mesures :
- Augmentation des conversions de 1.5% a 17.8% selon les marches
- Reduction des abandons de panier lies a la conversion de devises
- Gestion automatique des taux de change
- Affichage des prix arrondis dans la devise locale (pas de montants a decimales exotiques)

### Multi-Currency Manuel

Pour un controle total des prix par devise, creer des Prices specifiques par devise :

```typescript
// Creer un produit avec des prix multi-devises
const product = await stripe.products.create({
  name: 'Pro Plan',
});

const priceEUR = await stripe.prices.create({
  product: product.id,
  unit_amount: 2900, // 29.00 EUR
  currency: 'eur',
  recurring: { interval: 'month' },
});

const priceUSD = await stripe.prices.create({
  product: product.id,
  unit_amount: 2900, // 29.00 USD
  currency: 'usd',
  recurring: { interval: 'month' },
});

const priceGBP = await stripe.prices.create({
  product: product.id,
  unit_amount: 2500, // 25.00 GBP
  currency: 'gbp',
  recurring: { interval: 'month' },
});

// Selectionner le prix selon la localisation du client
function getPriceForLocale(locale: string): string {
  const priceMap: Record<string, string> = {
    'fr': priceEUR.id,
    'de': priceEUR.id,
    'us': priceUSD.id,
    'gb': priceGBP.id,
  };
  return priceMap[locale] || priceUSD.id; // fallback USD
}
```

### Presentment Currency vs Settlement Currency

Distinguer la devise de presentment (affichee au client) de la devise de settlement (recue par le vendeur). Avec Adaptive Pricing, Stripe convertit automatiquement. Avec multi-currency manuel, gerer le mapping des devises et les taux de change. Stripe applique une commission de conversion FX (generalement 1% au-dessus du taux interbancaire).

---

## Summary Checklist

Verifier ces points sur chaque integration Stripe :

- [ ] Les Payment Intents sont crees exclusivement cote serveur avec montants valides
- [ ] Le Payment Element est utilise plutot que les Elements individuels (Card Element)
- [ ] Les webhooks sont configures avec verification de signature
- [ ] Les handlers de webhook sont idempotents (event.id stocke et verifie)
- [ ] Les cles d'idempotence sont utilisees pour les operations de creation
- [ ] Les cles API sont stockees dans des variables d'environnement securisees
- [ ] Les numeros de carte ne sont jamais stockes, journalises ou transmis cote serveur
- [ ] Le Stripe CLI est utilise pour tester les webhooks en local
- [ ] Les metadata metier sont passees dans les Checkout Sessions et Payment Intents
- [ ] Les Customer IDs sont crees et stockes des l'inscription utilisateur
- [ ] Les erreurs de webhook sont loggees avec le contexte complet
- [ ] Les Test Clocks sont utilises pour tester les cycles d'abonnement
