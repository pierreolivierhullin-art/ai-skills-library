# Subscription & Billing

Reference approfondie sur la gestion des abonnements Stripe, la facturation recurrente, le metered billing et la recuperation des paiements echoues.

---

## Table of Contents

1. [Subscription Lifecycle](#subscription-lifecycle)
2. [Trial Periods & Grace Periods](#trial-periods--grace-periods)
3. [Proration & Plan Changes](#proration--plan-changes)
4. [Invoice Management](#invoice-management)
5. [Dunning & Failed Payment Recovery](#dunning--failed-payment-recovery)
6. [Usage-Based & Metered Billing](#usage-based--metered-billing)
7. [Stripe Billing Portal](#stripe-billing-portal)
8. [Advanced Billing Patterns](#advanced-billing-patterns)

---

## Subscription Lifecycle

### Etats d'un abonnement

Comprendre les transitions d'etat est fondamental pour gerer correctement les acces et les notifications :

```
incomplete -> active -> past_due -> canceled
                    -> trialing -> active
                    -> paused -> active
                    -> canceled
                    -> unpaid
incomplete_expired (terminal)
```

| Statut | Description | Acces utilisateur | Action requise |
|--------|-------------|-------------------|----------------|
| `incomplete` | Paiement initial en attente (3D Secure, traitement) | Bloque | Attendre le paiement |
| `incomplete_expired` | Paiement initial echoue apres 23h | Bloque | Proposer nouveau paiement |
| `trialing` | Periode d'essai en cours | Accorde | Aucune |
| `active` | Abonnement en cours, paiement a jour | Accorde | Aucune |
| `past_due` | Dernier paiement echoue, retries en cours | Configurable | Dunning automatique |
| `unpaid` | Tous les retries echoues | Bloque | Intervention manuelle |
| `canceled` | Abonnement annule | Bloque (ou grace) | Reactivation possible |
| `paused` | Abonnement mis en pause | Bloque | Reactivation manuelle |

### Creation d'un abonnement

```typescript
// Methode 1 : via Stripe Checkout (recommande pour le onboarding)
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  customer: customerId,
  line_items: [
    {
      price: 'price_pro_monthly',
      quantity: 1,
    },
  ],
  subscription_data: {
    trial_period_days: 14,
    metadata: { plan: 'pro', source: 'website' },
  },
  success_url: 'https://app.example.com/welcome?session_id={CHECKOUT_SESSION_ID}',
  cancel_url: 'https://app.example.com/pricing',
  automatic_tax: { enabled: true },
  allow_promotion_codes: true,
});

// Methode 2 : via l'API directe (quand la methode de paiement est deja sauvegardee)
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: 'price_pro_monthly' }],
  default_payment_method: paymentMethodId,
  trial_period_days: 14,
  payment_behavior: 'default_incomplete', // ne pas activer tant que le paiement n'est pas confirme
  payment_settings: {
    save_default_payment_method: 'on_subscription',
    payment_method_options: {
      card: {
        request_three_d_secure: 'automatic',
      },
    },
  },
  expand: ['latest_invoice.payment_intent'],
  metadata: { plan: 'pro', userId: user.id },
});
```

### Gestion des webhooks d'abonnement

```typescript
async function handleSubscriptionWebhook(event: Stripe.Event): Promise<void> {
  switch (event.type) {
    case 'customer.subscription.created': {
      const subscription = event.data.object as Stripe.Subscription;
      await db.subscriptions.create({
        data: {
          stripeSubscriptionId: subscription.id,
          stripeCustomerId: subscription.customer as string,
          status: subscription.status,
          priceId: subscription.items.data[0].price.id,
          currentPeriodStart: new Date(subscription.current_period_start * 1000),
          currentPeriodEnd: new Date(subscription.current_period_end * 1000),
          trialEnd: subscription.trial_end
            ? new Date(subscription.trial_end * 1000)
            : null,
        },
      });
      break;
    }

    case 'customer.subscription.updated': {
      const subscription = event.data.object as Stripe.Subscription;
      const previousAttributes = event.data.previous_attributes;

      await db.subscriptions.update({
        where: { stripeSubscriptionId: subscription.id },
        data: {
          status: subscription.status,
          priceId: subscription.items.data[0].price.id,
          currentPeriodStart: new Date(subscription.current_period_start * 1000),
          currentPeriodEnd: new Date(subscription.current_period_end * 1000),
          cancelAtPeriodEnd: subscription.cancel_at_period_end,
        },
      });

      // Detecter les changements de plan
      if (previousAttributes?.items) {
        await notifyPlanChange(subscription);
      }

      // Detecter la demande d'annulation
      if (subscription.cancel_at_period_end && !previousAttributes?.cancel_at_period_end) {
        await handleCancellationRequest(subscription);
      }
      break;
    }

    case 'customer.subscription.deleted': {
      const subscription = event.data.object as Stripe.Subscription;
      await db.subscriptions.update({
        where: { stripeSubscriptionId: subscription.id },
        data: { status: 'canceled', canceledAt: new Date() },
      });
      await revokeAccess(subscription.customer as string);
      await sendCancellationConfirmation(subscription);
      break;
    }
  }
}
```

---

## Trial Periods & Grace Periods

### Types de periodes d'essai

**Trial sans methode de paiement** : l'utilisateur s'inscrit sans fournir de carte. A la fin du trial, Stripe passe l'abonnement en `past_due` ou `incomplete` si aucune methode de paiement n'est ajoutee. Ideal pour maximiser les inscriptions, mais taux de conversion plus faible.

```typescript
// Trial sans carte (via Checkout)
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  customer: customerId,
  line_items: [{ price: 'price_pro_monthly' }],
  subscription_data: {
    trial_period_days: 14,
    trial_settings: {
      end_behavior: {
        missing_payment_method: 'cancel', // annuler si pas de carte a la fin
      },
    },
  },
  payment_method_collection: 'if_required', // pas de carte requise pendant le trial
  success_url: 'https://app.example.com/welcome',
  cancel_url: 'https://app.example.com/pricing',
});
```

**Trial avec methode de paiement** : l'utilisateur fournit une carte a l'inscription. A la fin du trial, le premier paiement est automatiquement tente. Meilleur taux de conversion trial-to-paid.

```typescript
// Trial avec carte (via Checkout)
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  customer: customerId,
  line_items: [{ price: 'price_pro_monthly' }],
  subscription_data: {
    trial_period_days: 14,
  },
  payment_method_collection: 'always', // carte requise
  success_url: 'https://app.example.com/welcome',
  cancel_url: 'https://app.example.com/pricing',
});
```

### Grace Period apres annulation

Permettre l'acces jusqu'a la fin de la periode de facturation en cours apres une annulation. Utiliser `cancel_at_period_end` plutot qu'une annulation immediate.

```typescript
// Annulation douce : acces jusqu'a la fin de la periode
await stripe.subscriptions.update(subscriptionId, {
  cancel_at_period_end: true,
});
// Le webhook customer.subscription.updated arrive avec cancel_at_period_end: true
// L'acces reste actif jusqu'a current_period_end
// Le webhook customer.subscription.deleted arrive a la fin de la periode

// Reactivation avant la fin de la periode
await stripe.subscriptions.update(subscriptionId, {
  cancel_at_period_end: false,
});
```

### Trial Extension

Prolonger un trial pour les prospects importants ou les clients en evaluation :

```typescript
// Prolonger le trial de 7 jours supplementaires
const subscription = await stripe.subscriptions.retrieve(subscriptionId);
const newTrialEnd = subscription.trial_end + 7 * 24 * 3600;

await stripe.subscriptions.update(subscriptionId, {
  trial_end: newTrialEnd,
  proration_behavior: 'none',
});
```

### Notifications de fin de trial

Ecouter le webhook `customer.subscription.trial_will_end` (envoye 3 jours avant la fin du trial) pour prevenir le client et l'inciter a mettre a jour sa methode de paiement.

```typescript
case 'customer.subscription.trial_will_end': {
  const subscription = event.data.object as Stripe.Subscription;
  const customer = await stripe.customers.retrieve(subscription.customer as string);
  await sendTrialEndingEmail(customer.email, {
    trialEndDate: new Date(subscription.trial_end * 1000),
    planName: subscription.items.data[0].price.nickname,
    hasPaymentMethod: !!subscription.default_payment_method,
  });
  break;
}
```

---

## Proration & Plan Changes

### Comportements de proration

Stripe offre plusieurs comportements de proration lors d'un changement de plan :

| Comportement | Description | Cas d'usage |
|-------------|-------------|-------------|
| `create_prorations` | Credit pour le temps restant sur l'ancien plan, debit pour le nouveau (defaut) | Changement de plan standard |
| `always_invoice` | Creer et facturer immediatement les prorations | Upgrade avec paiement immediat |
| `none` | Aucune proration, le nouveau prix s'applique au prochain cycle | Plans avec periodes fixes |

### Upgrade de plan

```typescript
// Upgrade : passage de Basic a Pro
const subscription = await stripe.subscriptions.retrieve(subscriptionId);

await stripe.subscriptions.update(subscriptionId, {
  items: [
    {
      id: subscription.items.data[0].id,
      price: 'price_pro_monthly',
    },
  ],
  proration_behavior: 'always_invoice', // facturer immediatement la difference
  payment_behavior: 'pending_if_incomplete',
});

// Stripe calcule automatiquement :
// 1. Credit pour les jours restants sur Basic
// 2. Debit pour les jours restants sur Pro
// 3. Facture et collecte la difference immediatement
```

### Downgrade de plan

```typescript
// Downgrade : passage de Pro a Basic
// Appliquer a la fin de la periode en cours
await stripe.subscriptions.update(subscriptionId, {
  items: [
    {
      id: subscription.items.data[0].id,
      price: 'price_basic_monthly',
    },
  ],
  proration_behavior: 'none', // pas de proration, changement effectif au prochain cycle
});

// Ou appliquer immediatement avec credit
await stripe.subscriptions.update(subscriptionId, {
  items: [
    {
      id: subscription.items.data[0].id,
      price: 'price_basic_monthly',
    },
  ],
  proration_behavior: 'create_prorations', // credit pour le temps restant sur Pro
});
```

### Changement de quantite (per-seat)

```typescript
// Ajouter un siege
const subscription = await stripe.subscriptions.retrieve(subscriptionId);

await stripe.subscriptions.update(subscriptionId, {
  items: [
    {
      id: subscription.items.data[0].id,
      quantity: subscription.items.data[0].quantity + 1,
    },
  ],
  proration_behavior: 'always_invoice', // facturer immediatement le siege supplementaire
});
```

### Preview de proration

Afficher au client le montant qui sera facture avant de confirmer le changement :

```typescript
// Previsualiser la facture de proration
const invoice = await stripe.invoices.createPreview({
  customer: customerId,
  subscription: subscriptionId,
  subscription_items: [
    {
      id: subscription.items.data[0].id,
      price: 'price_pro_monthly',
    },
  ],
  subscription_proration_behavior: 'always_invoice',
  subscription_proration_date: Math.floor(Date.now() / 1000),
});

// Afficher au client
const prorationAmount = invoice.total; // montant en centimes (peut etre negatif pour un credit)
const prorationLines = invoice.lines.data; // lignes detaillees de la proration
```

---

## Invoice Management

### Structure d'une facture

Chaque cycle d'abonnement genere une facture (Invoice). Comprendre les etats d'une facture :

```
draft -> open -> paid
              -> void
              -> uncollectible
              -> past_due (apres echec de paiement)
```

### Factures personnalisees

```typescript
// Ajouter des lignes manuelles a la prochaine facture
await stripe.invoiceItems.create({
  customer: customerId,
  amount: 5000, // 50.00 EUR
  currency: 'eur',
  description: 'Setup fee - one-time charge',
});

// Ces items seront inclus dans la prochaine facture d'abonnement

// Creer une facture ponctuelle (hors abonnement)
const invoice = await stripe.invoices.create({
  customer: customerId,
  collection_method: 'send_invoice', // envoyer par email
  days_until_due: 30, // paiement a 30 jours
  auto_advance: true,
});

await stripe.invoiceItems.create({
  customer: customerId,
  invoice: invoice.id,
  amount: 100000,
  currency: 'eur',
  description: 'Consulting services - January 2025',
});

// Finaliser et envoyer
await stripe.invoices.finalizeInvoice(invoice.id);
await stripe.invoices.sendInvoice(invoice.id);
```

### Numeros de facture personnalises

Configurer un format de numerotation conforme aux exigences legales (obligatoire en France et dans l'UE) :

```typescript
// Configurer le prefix de numerotation dans le Dashboard Stripe
// Settings > Billing > Invoice numbering
// Format : {prefix}-{number} ex: INV-2025-0001

// Ou via l'API lors de la creation
const invoice = await stripe.invoices.create({
  customer: customerId,
  number: 'INV-2025-0042', // numero personnalise
  custom_fields: [
    { name: 'Purchase Order', value: 'PO-2025-1234' },
    { name: 'VAT Number', value: 'FR12345678901' },
  ],
  footer: 'Payment terms: Net 30. Late payment fee: 1.5% per month.',
});
```

### Credit Notes

Emettre des avoir (credit notes) pour les remboursements partiels ou les ajustements :

```typescript
// Creer un avoir sur une facture
const creditNote = await stripe.creditNotes.create({
  invoice: invoiceId,
  lines: [
    {
      type: 'invoice_line_item',
      invoice_line_item: lineItemId,
      quantity: 1, // rembourser une unite
    },
  ],
  reason: 'product_unsatisfactory',
  memo: 'Partial refund for service disruption on January 15th',
});

// Le credit est automatiquement applique au prochain paiement
// ou rembourse sur la methode de paiement originale
```

---

## Dunning & Failed Payment Recovery

### Smart Retries

Stripe Smart Retries utilise le machine learning pour determiner le moment optimal de retenter un paiement echoue. Activer dans le Dashboard : Settings > Billing > Smart Retries.

Configuration recommandee :

| Parametre | Valeur recommandee | Description |
|-----------|-------------------|-------------|
| Smart Retries | Active | ML-optimized retry timing |
| Retry schedule | 3 tentatives sur 7 jours | Nombre et espacement des retries |
| Failed payment emails | Active | Emails automatiques au client |
| Upcoming renewal emails | Active | Email 3 jours avant le renouvellement |

### Revenue Recovery Pipeline

Mettre en place une strategie de recuperation en couches :

```
Paiement echoue (J+0)
  -> Smart Retry #1 (J+1 a J+3, timing ML-optimized)
  -> Email automatique au client (carte expiree, fonds insuffisants)
  -> Smart Retry #2 (J+3 a J+5)
  -> Email de rappel avec lien de mise a jour
  -> Smart Retry #3 (J+5 a J+7)
  -> Notification in-app (banniere dans l'application)
  -> Abonnement passe en past_due -> unpaid -> canceled
```

### Configuration du dunning

```typescript
// Configurer le comportement en cas d'echec via l'API
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: 'price_pro_monthly' }],
  payment_settings: {
    save_default_payment_method: 'on_subscription',
    payment_method_options: {
      card: {
        request_three_d_secure: 'automatic',
      },
    },
  },
  // Configurer dans le Dashboard : Settings > Billing > Manage failed payments
  // Options : mark as unpaid, cancel subscription, leave as past_due
});
```

### Webhooks pour le dunning

```typescript
case 'invoice.payment_failed': {
  const invoice = event.data.object as Stripe.Invoice;
  const subscription = await stripe.subscriptions.retrieve(
    invoice.subscription as string
  );

  // Determiner le nombre de tentatives
  const attemptCount = invoice.attempt_count;
  const nextAttempt = invoice.next_payment_attempt;

  if (attemptCount === 1) {
    // Premiere tentative echouee : email discret
    await sendPaymentFailedEmail(invoice, {
      severity: 'info',
      updatePaymentUrl: `https://app.example.com/billing/update-payment`,
    });
  } else if (attemptCount === 2) {
    // Deuxieme tentative : email plus urgent + notification in-app
    await sendPaymentFailedEmail(invoice, { severity: 'warning' });
    await createInAppNotification(subscription.customer, 'payment_issue');
  } else if (attemptCount >= 3) {
    // Derniere tentative : email urgent avec risque de suspension
    await sendPaymentFailedEmail(invoice, { severity: 'critical' });
    await flagAccountForReview(subscription.customer);
  }
  break;
}

case 'customer.subscription.updated': {
  const subscription = event.data.object as Stripe.Subscription;
  const previousAttributes = event.data.previous_attributes;

  // Detecter le passage en past_due
  if (subscription.status === 'past_due' && previousAttributes?.status === 'active') {
    await restrictFeatures(subscription.customer as string, 'degraded');
    await sendPastDueNotification(subscription);
  }

  // Detecter le passage en unpaid
  if (subscription.status === 'unpaid') {
    await revokeAccess(subscription.customer as string);
    await sendAccountSuspendedNotification(subscription);
  }
  break;
}
```

### Customer Portal pour la mise a jour

Permettre au client de mettre a jour sa methode de paiement via le Stripe Billing Portal :

```typescript
// Generer un lien vers le Customer Portal
const portalSession = await stripe.billingPortal.sessions.create({
  customer: customerId,
  return_url: 'https://app.example.com/settings/billing',
  flow_data: {
    type: 'payment_method_update', // ouvrir directement sur la mise a jour de carte
  },
});

// Rediriger vers portalSession.url
```

---

## Usage-Based & Metered Billing

### Metered Billing (facturation a la consommation)

Creer un prix avec `usage_type: 'metered'` pour facturer selon l'utilisation reelle. Les usage records sont reportes pendant la periode de facturation et agregos a la fin.

```typescript
// Creer un prix metered
const price = await stripe.prices.create({
  product: productId,
  currency: 'eur',
  recurring: {
    interval: 'month',
    usage_type: 'metered',
    aggregate_usage: 'sum', // ou 'max', 'last_during_period', 'last_ever'
  },
  billing_scheme: 'per_unit',
  unit_amount: 10, // 0.10 EUR par unite
});

// Creer l'abonnement metered
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: price.id }],
});
```

### Reporter l'usage

```typescript
// Reporter l'usage (appeler a chaque evenement ou par batch)
await stripe.subscriptionItems.createUsageRecord(
  subscriptionItemId,
  {
    quantity: 150, // 150 appels API
    timestamp: Math.floor(Date.now() / 1000),
    action: 'increment', // ou 'set' pour remplacer la valeur
  },
  {
    idempotencyKey: `usage_${subscriptionItemId}_${timestamp}_${batchId}`,
  }
);
```

Bonnes pratiques pour le reporting d'usage :

- Reporter l'usage en temps reel ou par micro-batches (toutes les heures) pour eviter les pertes en cas de crash.
- Utiliser des cles d'idempotence pour chaque report (prevenir les doubles comptages).
- Stocker l'usage localement avant de le reporter a Stripe (buffer local + queue asynchrone).
- Monitorer les ecarts entre l'usage local et l'usage reporte a Stripe.
- Utiliser `action: 'set'` avec prudence -- `increment` est plus resilient aux retries.

### Tiered Pricing

Configurer des paliers de prix degressifs :

```typescript
// Tiered pricing : prix degressif par tranche
const price = await stripe.prices.create({
  product: productId,
  currency: 'eur',
  recurring: { interval: 'month' },
  billing_scheme: 'tiered',
  tiers_mode: 'graduated', // ou 'volume'
  tiers: [
    { up_to: 100, unit_amount: 50 },     // 0-100 : 0.50 EUR/unite
    { up_to: 1000, unit_amount: 30 },    // 101-1000 : 0.30 EUR/unite
    { up_to: 10000, unit_amount: 15 },   // 1001-10000 : 0.15 EUR/unite
    { up_to: 'inf', unit_amount: 5 },    // 10001+ : 0.05 EUR/unite
  ],
});
```

Difference entre `graduated` et `volume` :
- **graduated** : chaque tranche a son propre prix. Les 100 premieres unites a 0.50 EUR, les 900 suivantes a 0.30 EUR, etc.
- **volume** : le prix de la tranche atteinte s'applique a toutes les unites. 150 unites = 150 * 0.30 EUR (tranche 101-1000).

### Hybrid Billing (fixe + variable)

```typescript
// Abonnement hybride : base fixe + usage variable
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [
    { price: 'price_base_monthly' },    // 49 EUR/mois fixe
    { price: 'price_api_calls_metered' }, // 0.01 EUR par appel API
  ],
});
```

---

## Stripe Billing Portal

### Configuration du portail

Configurer le Customer Portal pour permettre aux clients de gerer leurs abonnements en self-service :

```typescript
// Configurer le portail (une seule fois)
const configuration = await stripe.billingPortal.configurations.create({
  business_profile: {
    headline: 'Manage your subscription',
    privacy_policy_url: 'https://example.com/privacy',
    terms_of_service_url: 'https://example.com/terms',
  },
  features: {
    customer_update: {
      enabled: true,
      allowed_updates: ['email', 'address', 'phone', 'tax_id'],
    },
    invoice_history: { enabled: true },
    payment_method_update: { enabled: true },
    subscription_cancel: {
      enabled: true,
      mode: 'at_period_end', // annulation a la fin de la periode
      proration_behavior: 'none',
      cancellation_reason: {
        enabled: true,
        options: [
          'too_expensive',
          'missing_features',
          'switched_service',
          'unused',
          'customer_service',
          'too_complex',
          'low_quality',
          'other',
        ],
      },
    },
    subscription_update: {
      enabled: true,
      default_allowed_updates: ['price', 'quantity', 'promotion_code'],
      proration_behavior: 'always_invoice',
      products: [
        {
          product: 'prod_basic',
          prices: ['price_basic_monthly', 'price_basic_yearly'],
        },
        {
          product: 'prod_pro',
          prices: ['price_pro_monthly', 'price_pro_yearly'],
        },
        {
          product: 'prod_enterprise',
          prices: ['price_enterprise_monthly', 'price_enterprise_yearly'],
        },
      ],
    },
    subscription_pause: {
      enabled: true, // permettre la mise en pause
    },
  },
});
```

### Generer un lien vers le portail

```typescript
// Generer une session de portail pour un client
app.post('/api/billing/portal', async (req, res) => {
  const { customerId } = req.body;

  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: 'https://app.example.com/settings/billing',
    // Optionnel : ouvrir directement sur une section specifique
    flow_data: {
      type: 'subscription_update',
      subscription_update: {
        subscription: subscriptionId,
      },
    },
  });

  res.json({ url: session.url });
});
```

### Webhooks du portail

Le portail genere les memes webhooks que les operations API. Ecouter les evenements suivants :
- `customer.subscription.updated` : changement de plan ou de quantite
- `customer.subscription.deleted` : annulation
- `payment_method.attached` / `detached` : mise a jour de la methode de paiement
- `customer.updated` : mise a jour des informations client
- `billing_portal.session.created` : ouverture d'une session du portail (tracking)

---

## Advanced Billing Patterns

### Schedule de changement de plan

Planifier un changement de plan a une date future (ex: debut du prochain cycle) :

```typescript
// Creer un schedule de changement
const schedule = await stripe.subscriptionSchedules.create({
  from_subscription: subscriptionId,
});

// Ajouter des phases
await stripe.subscriptionSchedules.update(schedule.id, {
  phases: [
    {
      items: [{ price: 'price_basic_monthly', quantity: 1 }],
      start_date: schedule.phases[0].start_date,
      end_date: schedule.phases[0].end_date,
    },
    {
      items: [{ price: 'price_pro_monthly', quantity: 1 }],
      start_date: schedule.phases[0].end_date, // debut du prochain cycle
      iterations: 1, // optionnel : nombre de cycles
    },
  ],
});
```

### Coupons et promotions

```typescript
// Creer un coupon
const coupon = await stripe.coupons.create({
  percent_off: 20,
  duration: 'repeating',
  duration_in_months: 3, // 20% pendant 3 mois
  max_redemptions: 100,
  redeem_by: Math.floor(new Date('2025-12-31').getTime() / 1000),
  name: 'Holiday Sale 2025',
});

// Creer un code promo (parteable)
const promoCode = await stripe.promotionCodes.create({
  coupon: coupon.id,
  code: 'HOLIDAY20',
  max_redemptions: 50,
  restrictions: {
    first_time_transaction: true, // uniquement pour les nouveaux clients
    minimum_amount: 2000, // minimum 20 EUR
    minimum_amount_currency: 'eur',
  },
});

// Appliquer a un abonnement
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: 'price_pro_monthly' }],
  promotion_code: promoCode.id,
});
```

### Multi-Product Subscriptions

Combiner plusieurs produits dans un seul abonnement :

```typescript
// Abonnement avec base + add-ons
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [
    { price: 'price_pro_monthly' },           // Plan de base
    { price: 'price_extra_storage_monthly' },  // Add-on stockage
    { price: 'price_priority_support_monthly' }, // Add-on support
  ],
});

// Ajouter un add-on plus tard
await stripe.subscriptionItems.create({
  subscription: subscriptionId,
  price: 'price_analytics_addon_monthly',
  proration_behavior: 'always_invoice',
});

// Supprimer un add-on
await stripe.subscriptionItems.del(subscriptionItemId, {
  proration_behavior: 'create_prorations',
});
```

### Pause et reprise

```typescript
// Mettre en pause un abonnement
await stripe.subscriptions.update(subscriptionId, {
  pause_collection: {
    behavior: 'void', // 'void' = pas de facture, 'keep_as_draft' = facture brouillon, 'mark_uncollectible'
    resumes_at: Math.floor(Date.now() / 1000) + 30 * 24 * 3600, // reprise dans 30 jours
  },
});

// Reprendre manuellement
await stripe.subscriptions.update(subscriptionId, {
  pause_collection: '', // supprimer la pause
});
```

---

## Summary Checklist

Verifier ces points sur chaque implementation de billing :

- [ ] Les abonnements sont crees via Checkout ou avec `payment_behavior: 'default_incomplete'`
- [ ] Le webhook `customer.subscription.trial_will_end` declenche une notification 3 jours avant la fin du trial
- [ ] Le cycle de vie complet est gere (trialing, active, past_due, unpaid, canceled)
- [ ] L'annulation est douce (`cancel_at_period_end: true`) avec acces maintenu
- [ ] Les changements de plan gerent la proration correctement
- [ ] Le preview de proration est affiche au client avant confirmation
- [ ] Smart Retries est active pour la recuperation automatique
- [ ] Les emails de dunning sont configures (3 niveaux de severite)
- [ ] Le Customer Portal est deploye pour le self-service
- [ ] Les usage records sont reportes avec des cles d'idempotence
- [ ] Les factures respectent les exigences legales (numerotation, mentions obligatoires)
- [ ] Les Test Clocks sont utilises pour tester les cycles complets
