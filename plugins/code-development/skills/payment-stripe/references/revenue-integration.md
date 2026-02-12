# Revenue & Financial Integration

Reference approfondie sur la revenue recognition, Stripe Tax, l'integration comptable, la reconciliation et la gestion des litiges.

---

## Table of Contents

1. [Revenue Recognition (ASC 606 / IFRS 15)](#revenue-recognition-asc-606--ifrs-15)
2. [Stripe Tax](#stripe-tax)
3. [Accounting Integration](#accounting-integration)
4. [Financial Reporting & Reconciliation](#financial-reporting--reconciliation)
5. [Refunds, Disputes & Chargebacks](#refunds-disputes--chargebacks)
6. [Multi-Currency & FX](#multi-currency--fx)
7. [Stripe Sigma & Data Pipeline](#stripe-sigma--data-pipeline)

---

## Revenue Recognition (ASC 606 / IFRS 15)

### Principes fondamentaux

La reconnaissance du revenu suit un modele en 5 etapes, identique entre ASC 606 (US GAAP) et IFRS 15 (normes internationales) :

| Etape | Description | Application SaaS |
|-------|-------------|-----------------|
| 1 | Identifier le contrat | Abonnement actif avec conditions acceptees |
| 2 | Identifier les obligations de performance | Acces logiciel, support, formation |
| 3 | Determiner le prix de la transaction | Montant de l'abonnement (net de taxes et remises) |
| 4 | Allouer le prix aux obligations | Repartir entre les differentes obligations |
| 5 | Reconnaitre le revenu quand l'obligation est satisfaite | Au fur et a mesure de la livraison du service |

### Application aux modeles SaaS

**Abonnement mensuel (30 EUR/mois)** :
- Obligation de performance : acces continu au logiciel pendant 1 mois.
- Le revenu est reconnu lineairement sur la periode d'abonnement.
- Le 15 janvier, la facture du mois de janvier est emise. Le revenu reconnaissable au 31 janvier = 30 EUR complet.
- En comptabilite d'engagement : le paiement cree une dette (deferred revenue), reconnue lineairement.

**Abonnement annuel (300 EUR/an, paye d'avance)** :
- Le client paie 300 EUR le 1er janvier.
- Le revenu reconnu au 31 janvier = 300/12 = 25 EUR.
- Les 275 EUR restants = deferred revenue (produit constate d'avance).
- Chaque mois suivant, 25 EUR migrent de deferred revenue vers recognized revenue.

**Abonnement avec trial gratuit (14 jours)** :
- Aucun revenu pendant le trial (pas de contrepartie financiere).
- Le revenu debute au premier jour de l'abonnement paye.
- Si le trial est offert avec une obligation d'achat, analyser si le trial constitue une obligation distincte.

### Stripe Revenue Recognition

Stripe Revenue Recognition automatise la generation des ecritures comptables conformes ASC 606/IFRS 15 :

```
Fonctionnalites :
- Waterfall chart de reconnaissance du revenu
- Deferred revenue tracking automatique
- Gestion des refunds et disputes dans la reconnaissance
- Export des ecritures vers les systemes comptables
- Support multi-devises avec conversion au taux historique
- Gestion des changements de plan et prorations
```

Configurer dans Dashboard > Revenue Recognition :
- Definir les regles de reconnaissance par produit
- Configurer les periodes comptables (mensuel, trimestriel)
- Exporter les rapports ou connecter a l'ERP

### Ecritures de base

```
# Paiement d'un abonnement annuel de 300 EUR (1er janvier)

Journal Entry - 1er janvier :
  Debit  : Cash / Accounts Receivable     300.00 EUR
  Credit : Deferred Revenue                300.00 EUR

Journal Entry - 31 janvier (reconnaissance mensuelle) :
  Debit  : Deferred Revenue                 25.00 EUR
  Credit : Subscription Revenue             25.00 EUR

# Repete chaque mois jusqu'au 31 decembre

---

# Remboursement partiel de 100 EUR le 15 mars (3 mois ecoulees)

# Revenu deja reconnu : 3 x 25 = 75 EUR
# Deferred revenue restant : 225 EUR
# Remboursement 100 EUR : d'abord reduire le deferred, puis le recognized si necessaire

Journal Entry - 15 mars :
  Debit  : Deferred Revenue                100.00 EUR
  Credit : Cash / Refund Liability         100.00 EUR

# Ajuster les ecritures futures : nouveau montant mensuel = (300 - 100) / 9 mois restants = 22.22 EUR
```

### Cas complexes

**Upgrade mid-cycle** : si un client passe de Basic (30 EUR/mois) a Pro (50 EUR/mois) le 15 du mois :
- Credit proportionnel pour Basic : 30 * 15/30 = 15 EUR
- Debit proportionnel pour Pro : 50 * 15/30 = 25 EUR
- Le client paie la difference : 10 EUR
- Revenue recognition : 15 EUR Basic (1-15) + 25 EUR Pro (15-30)

**Coupons et remises** : les remises reduisent le prix de la transaction (etape 3). Le revenu est reconnu sur le montant net apres remise, pas le montant brut.

**Periodes d'essai gratuites** : aucun revenu pendant la periode d'essai. Si le trial est suivi d'un abonnement annuel, la reconnaissance commence au premier jour paye.

---

## Stripe Tax

### Configuration

Stripe Tax calcule automatiquement les taxes (TVA, sales tax, GST) pour les transactions dans plus de 50 pays. Activer dans Dashboard > Settings > Tax.

```typescript
// Activer Stripe Tax sur une Checkout Session
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  line_items: [{ price: 'price_pro_monthly', quantity: 1 }],
  automatic_tax: { enabled: true },
  customer: customerId,
  customer_update: {
    address: 'auto', // mettre a jour l'adresse du customer automatiquement
  },
  success_url: 'https://app.example.com/success',
  cancel_url: 'https://app.example.com/pricing',
});

// Activer Stripe Tax sur un abonnement via l'API
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: 'price_pro_monthly' }],
  automatic_tax: { enabled: true },
});
```

### Tax Registration (Immatriculations fiscales)

Declarer les immatriculations fiscales dans chaque juridiction ou l'entreprise a un nexus :

```typescript
// Ajouter une immatriculation TVA (via Dashboard ou API)
const registration = await stripe.tax.registrations.create({
  country: 'FR',
  country_options: {
    fr: {
      type: 'standard', // TVA standard francaise
    },
  },
  active_from: 'now',
});

// Ajouter une immatriculation pour les US (sales tax)
const usRegistration = await stripe.tax.registrations.create({
  country: 'US',
  state: 'CA', // Californie
  country_options: {
    us: {
      state: 'CA',
      type: 'state_sales_tax',
    },
  },
  active_from: 'now',
});
```

### Tax IDs (Numeros de TVA client)

Collecter et verifier les numeros de TVA des clients B2B :

```typescript
// Ajouter un numero de TVA au customer
const taxId = await stripe.customers.createTaxId(customerId, {
  type: 'eu_vat', // ou 'gb_vat', 'us_ein', 'au_abn', etc.
  value: 'FR12345678901',
});

// Stripe verifie automatiquement la validite du numero via VIES
// Le statut est mis a jour via webhook : customer.tax_id.updated

// Si le client est B2B dans un autre pays UE avec TVA valide :
// -> Reverse charge : TVA a 0% (autoliquidation)
// Stripe gere automatiquement cette logique
```

### Tax Codes (Categories de produit)

Assigner le bon code fiscal a chaque produit pour un calcul correct des taxes :

```typescript
// Configurer le tax code du produit
const product = await stripe.products.create({
  name: 'Pro Plan',
  tax_code: 'txcd_10103001', // Software as a Service (SaaS)
});

// Tax codes courants pour le SaaS :
// txcd_10103001 : SaaS - business use
// txcd_10103000 : SaaS - personal use
// txcd_10201000 : Infrastructure as a Service (IaaS)
// txcd_10301000 : Platform as a Service (PaaS)
// txcd_10502000 : Cloud-based electronic services
```

### Taux de TVA par pays (exemples)

| Pays | Taux standard | Taux reduit | Applicable au SaaS |
|------|--------------|-------------|---------------------|
| France | 20% | 10% / 5.5% | 20% |
| Allemagne | 19% | 7% | 19% |
| Royaume-Uni | 20% | 5% | 20% |
| Etats-Unis | Variable (0-10.25%) | N/A | Selon l'etat |
| Canada | 5% GST + PST variable | N/A | 5-15% selon la province |
| Australie | 10% GST | N/A | 10% |
| Japon | 10% JCT | 8% | 10% |

---

## Accounting Integration

### Journal Entries Pattern

Modeliser les ecritures comptables pour chaque type de transaction Stripe :

```
# PAIEMENT PAR CARTE (charge immediatement capturee)
# Montant brut: 100.00 EUR, Frais Stripe: 2.90 EUR, TVA: 20.00 EUR

Debit  : Stripe Receivable          100.00 EUR
Credit : Revenue                      80.00 EUR
Credit : VAT Collected                20.00 EUR

# A la reception du payout Stripe (J+2 a J+7)
Debit  : Bank Account                97.10 EUR
Debit  : Payment Processing Fees      2.90 EUR
Credit : Stripe Receivable           100.00 EUR

---

# ABONNEMENT MENSUEL (50 EUR/mois, paye le 1er du mois)

# Emission de la facture (J+0)
Debit  : Accounts Receivable         60.00 EUR  (50 + 10 TVA)
Credit : Deferred Revenue            50.00 EUR
Credit : VAT Collected               10.00 EUR

# Paiement recu
Debit  : Stripe Receivable           60.00 EUR
Credit : Accounts Receivable         60.00 EUR

# Reconnaissance lineaire (chaque jour ou fin de mois)
Debit  : Deferred Revenue            50.00 EUR
Credit : Subscription Revenue        50.00 EUR

---

# REMBOURSEMENT COMPLET (charge originale de 100 EUR)

Debit  : Revenue                     80.00 EUR
Debit  : VAT Collected               20.00 EUR
Credit : Stripe Receivable          100.00 EUR

# Note : les frais Stripe ne sont PAS rembourses
# Perte nette = frais Stripe de la charge originale (2.90 EUR)

---

# LITIGE / CHARGEBACK (charge originale de 100 EUR)

# A l'ouverture du litige
Debit  : Dispute Receivable         100.00 EUR
Debit  : Chargeback Fee               15.00 EUR  (frais de litige Stripe)
Credit : Stripe Receivable           115.00 EUR

# Si le litige est gagne
Debit  : Stripe Receivable          100.00 EUR
Credit : Dispute Receivable          100.00 EUR
# Note : les frais de litige ne sont pas rembourses (sauf UK/EU)

# Si le litige est perdu
Debit  : Bad Debt Expense           100.00 EUR
Credit : Dispute Receivable          100.00 EUR
```

### ERP Sync Patterns

Trois approches pour synchroniser Stripe avec un ERP (Sage, SAP, Netsuite, Xero, QuickBooks) :

**Approche 1 : Webhook-driven (temps reel)**

```typescript
// Synchroniser chaque evenement Stripe avec l'ERP en temps reel
async function syncToERP(event: Stripe.Event): Promise<void> {
  switch (event.type) {
    case 'invoice.paid': {
      const invoice = event.data.object as Stripe.Invoice;
      await erpClient.createInvoice({
        externalId: invoice.id,
        customerId: mapStripeToERPCustomer(invoice.customer as string),
        amount: invoice.amount_paid / 100,
        currency: invoice.currency.toUpperCase(),
        lineItems: invoice.lines.data.map(line => ({
          description: line.description,
          amount: line.amount / 100,
          taxAmount: line.tax_amounts?.[0]?.amount / 100 || 0,
        })),
        paidAt: new Date(invoice.status_transitions.paid_at * 1000),
      });
      break;
    }

    case 'charge.refunded': {
      const charge = event.data.object as Stripe.Charge;
      await erpClient.createCreditNote({
        relatedInvoiceId: charge.invoice as string,
        amount: charge.amount_refunded / 100,
        reason: charge.refunds.data[0]?.reason || 'requested_by_customer',
      });
      break;
    }

    case 'payout.paid': {
      const payout = event.data.object as Stripe.Payout;
      await erpClient.createBankDeposit({
        externalId: payout.id,
        amount: payout.amount / 100,
        arrivalDate: new Date(payout.arrival_date * 1000),
        bankAccount: payout.destination as string,
      });
      break;
    }
  }
}
```

**Approche 2 : Batch reconciliation (quotidien)**

```typescript
// Reconcilier quotidiennement les transactions Stripe avec l'ERP
async function dailyReconciliation(date: Date): Promise<ReconciliationReport> {
  const startOfDay = Math.floor(new Date(date.setHours(0, 0, 0, 0)).getTime() / 1000);
  const endOfDay = Math.floor(new Date(date.setHours(23, 59, 59, 999)).getTime() / 1000);

  // Recuperer toutes les charges du jour
  const charges = await stripe.charges.list({
    created: { gte: startOfDay, lte: endOfDay },
    limit: 100,
  });

  // Recuperer tous les remboursements du jour
  const refunds = await stripe.refunds.list({
    created: { gte: startOfDay, lte: endOfDay },
    limit: 100,
  });

  // Recuperer les payouts du jour
  const payouts = await stripe.payouts.list({
    arrival_date: { gte: startOfDay, lte: endOfDay },
    limit: 100,
  });

  // Comparer avec les ecritures ERP et identifier les ecarts
  const report = await compareWithERP(charges, refunds, payouts);
  return report;
}
```

**Approche 3 : Stripe Data Pipeline (pour les gros volumes)**

Utiliser Stripe Data Pipeline pour exporter les donnees vers un data warehouse (Snowflake, BigQuery, Redshift) et reconcilier via SQL.

---

## Financial Reporting & Reconciliation

### Reconciliation des payouts

Un payout Stripe contient l'agregat de plusieurs transactions (charges, refunds, fees, adjustments). Reconcilier au niveau du payout :

```typescript
// Lister les transactions d'un payout
const balanceTransactions = await stripe.balanceTransactions.list({
  payout: payoutId,
  limit: 100,
});

// Chaque balance transaction contient :
// - amount : montant brut
// - fee : frais Stripe
// - net : montant net (amount - fee)
// - type : 'charge', 'refund', 'adjustment', 'stripe_fee', etc.
// - source : ID de la charge/refund liee

let totalGross = 0;
let totalFees = 0;
let totalNet = 0;

for (const txn of balanceTransactions.data) {
  totalGross += txn.amount;
  totalFees += txn.fee;
  totalNet += txn.net;
}

// totalNet doit etre egal au montant du payout
// Si ecart : investiguer les adjustments et les disputes
```

### Balance Reports

Stripe fournit des rapports de balance detailles :

```typescript
// Generer un rapport de balance
const report = await stripe.reporting.reportRuns.create({
  report_type: 'balance_change_from_activity.itemized.3',
  parameters: {
    interval_start: Math.floor(new Date('2025-01-01').getTime() / 1000),
    interval_end: Math.floor(new Date('2025-02-01').getTime() / 1000),
    currency: 'eur',
  },
});

// Le rapport est genere de maniere asynchrone
// Recuperer le resultat via le webhook reporting.report_run.succeeded
// Ou par polling : stripe.reporting.reportRuns.retrieve(report.id)
```

### KPIs financiers a monitorer

| KPI | Calcul | Cible |
|-----|--------|-------|
| MRR (Monthly Recurring Revenue) | Somme des abonnements actifs * montant mensuel | Croissance |
| ARR (Annual Recurring Revenue) | MRR * 12 | Reference investisseurs |
| Churn Rate | Abonnements perdus / total abonnements | < 5% / mois |
| Net Revenue Retention | (MRR debut + expansion - contraction - churn) / MRR debut | > 100% |
| ARPU (Average Revenue Per User) | MRR / nombre d'abonnements actifs | Croissance |
| LTV (Lifetime Value) | ARPU / churn rate mensuel | > 3x CAC |
| Dispute Rate | Disputes / total charges | < 0.5% |
| Refund Rate | Montant rembourse / montant facture | < 5% |
| Recovery Rate | Paiements recuperes par dunning / paiements echoues | > 60% |

---

## Refunds, Disputes & Chargebacks

### Refunds (Remboursements)

```typescript
// Remboursement complet
const refund = await stripe.refunds.create({
  payment_intent: paymentIntentId,
  reason: 'requested_by_customer', // ou 'duplicate', 'fraudulent'
});

// Remboursement partiel
const partialRefund = await stripe.refunds.create({
  payment_intent: paymentIntentId,
  amount: 500, // rembourser 5.00 EUR sur un paiement de 20.00 EUR
  reason: 'requested_by_customer',
  metadata: { reason_detail: 'Unused days after cancellation' },
});

// Remboursement sur un abonnement (credit note)
const creditNote = await stripe.creditNotes.create({
  invoice: invoiceId,
  amount: 1000, // credit de 10.00 EUR
  reason: 'product_unsatisfactory',
  credit_amount: 1000, // appliquer comme credit sur la prochaine facture
  // OU
  refund_amount: 1000, // rembourser sur la methode de paiement
});
```

Impact financier des remboursements :
- Stripe rembourse le montant au client mais ne rembourse **pas** les frais de traitement (depuis 2023).
- Perte = frais de traitement de la charge originale.
- Pour les remboursements SEPA : delai de 5-10 jours ouvrables.
- Pour les remboursements carte : 5-10 jours pour apparaitre sur le releve du client.

### Disputes (Litiges)

Un dispute (chargeback) est initie par le client aupres de sa banque. Stripe notifie via le webhook `charge.dispute.created`. Reagir dans les 7-21 jours selon le type de dispute.

```typescript
// Ecouter les webhooks de litige
case 'charge.dispute.created': {
  const dispute = event.data.object as Stripe.Dispute;

  // Logger le litige avec le contexte complet
  logger.warn('Dispute created', {
    disputeId: dispute.id,
    chargeId: dispute.charge,
    amount: dispute.amount,
    reason: dispute.reason, // 'fraudulent', 'duplicate', 'product_not_received', etc.
    status: dispute.status,
    evidenceDueBy: new Date(dispute.evidence_details.due_by * 1000),
  });

  // Notifier l'equipe
  await notifyDisputeTeam(dispute);

  // Creer un ticket pour le suivi
  await createDisputeTicket(dispute);
  break;
}

case 'charge.dispute.updated': {
  const dispute = event.data.object as Stripe.Dispute;
  if (dispute.status === 'won') {
    await handleDisputeWon(dispute);
  } else if (dispute.status === 'lost') {
    await handleDisputeLost(dispute);
  }
  break;
}
```

### Soumission de preuves

```typescript
// Soumettre des preuves pour contester un litige
await stripe.disputes.update(disputeId, {
  evidence: {
    // Preuves generales
    customer_name: 'Jean Dupont',
    customer_email_address: 'jean@example.com',
    customer_purchase_ip: '203.0.113.42',

    // Preuves specifiques au type de litige
    product_description: 'SaaS subscription - Pro Plan (monthly)',
    service_date: '2025-01-01',

    // Preuves d'utilisation du service
    access_activity_log: 'Customer logged in 47 times in January 2025. Last login: Jan 28.',

    // Preuves de livraison
    shipping_tracking_number: 'N/A - digital service',

    // Politique de remboursement
    refund_policy: 'Full refund available within 30 days. Customer did not request refund.',
    refund_policy_disclosure: 'Displayed during checkout and in Terms of Service.',

    // Communication avec le client
    customer_communication: 'fileId_xxx', // upload d'un fichier PDF

    // Confirmation de la commande
    receipt: 'fileId_yyy', // upload du recu

    // Pour les abonnements : preuve de consentement
    uncategorized_text: 'Subscription created on Dec 15, 2024. Customer agreed to Terms of Service. No cancellation request received.',
  },
  submit: true, // soumettre les preuves (pas de modification possible apres)
});
```

### Prevention des litiges

- Utiliser un descripteur de facturation clair (`statement_descriptor`) : le client doit reconnaitre l'achat sur son releve bancaire. Configurer dans Dashboard > Settings > Public business information.
- Envoyer des recus automatiques pour chaque paiement.
- Rembourser proactivement les clients mecontents avant qu'ils n'ouvrent un litige (un remboursement coute 0 EUR, un litige coute 15 EUR de frais + temps de gestion).
- Monitorer le taux de dispute (seuil d'alerte : 0.5% des charges). Au-dessus de 0.75%, les reseaux de cartes peuvent sanctionner.
- Activer Stripe Radar pour bloquer les paiements frauduleux en amont.

---

## Multi-Currency & FX

### Gestion multi-devises

Stripe supporte plus de 135 devises de presentment. Comprendre les concepts :

- **Presentment currency** : devise affichee au client (EUR, USD, GBP)
- **Settlement currency** : devise dans laquelle les payouts sont effectues (configuree par compte Stripe)
- **FX rate** : taux de change applique par Stripe (taux interbancaire + marge)

```typescript
// Creer un paiement dans une devise specifique
const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000, // 20.00 dans la devise specifiee
  currency: 'gbp', // livre sterling
  customer: customerId,
  automatic_payment_methods: { enabled: true },
});

// Si le compte Stripe est en EUR et le paiement en GBP :
// - Le client paie 20.00 GBP
// - Stripe convertit en EUR au taux du jour
// - Le payout est effectue en EUR
// - Les frais de conversion FX s'appliquent (generalement 1%)
```

### Multi-Currency Payouts

Configurer des comptes bancaires dans plusieurs devises pour eviter la conversion FX :

```typescript
// Ajouter un compte bancaire en GBP pour recevoir les payouts en GBP
const bankAccount = await stripe.accounts.createExternalAccount(accountId, {
  external_account: {
    object: 'bank_account',
    country: 'GB',
    currency: 'gbp',
    account_number: '00012345',
    routing_number: '108800',
  },
});

// Les payouts en GBP seront effectues sur ce compte
// sans conversion FX (economie de la marge de conversion)
```

### Devises zero-decimal

Certaines devises n'ont pas de decimales (JPY, KRW, VND). Adapter les montants en consequence :

```typescript
// Devises avec decimales (la plupart)
const eurPayment = { amount: 2000, currency: 'eur' }; // 20.00 EUR

// Devises zero-decimal
const jpyPayment = { amount: 2000, currency: 'jpy' }; // 2000 JPY (pas 20.00)

// Helper pour gerer les conversions
function toStripeAmount(amount: number, currency: string): number {
  const zeroDecimalCurrencies = [
    'bif', 'clp', 'djf', 'gnf', 'jpy', 'kmf', 'krw', 'mga',
    'pyg', 'rwf', 'ugx', 'vnd', 'vuv', 'xaf', 'xof', 'xpf',
  ];
  if (zeroDecimalCurrencies.includes(currency.toLowerCase())) {
    return Math.round(amount);
  }
  return Math.round(amount * 100);
}

function fromStripeAmount(amount: number, currency: string): number {
  const zeroDecimalCurrencies = [
    'bif', 'clp', 'djf', 'gnf', 'jpy', 'kmf', 'krw', 'mga',
    'pyg', 'rwf', 'ugx', 'vnd', 'vuv', 'xaf', 'xof', 'xpf',
  ];
  if (zeroDecimalCurrencies.includes(currency.toLowerCase())) {
    return amount;
  }
  return amount / 100;
}
```

---

## Stripe Sigma & Data Pipeline

### Stripe Sigma

Stripe Sigma permet d'executer des requetes SQL directement sur les donnees Stripe. Utiliser pour le reporting custom, l'analyse financiere et la reconciliation.

```sql
-- MRR actuel par produit
SELECT
  p.name AS product_name,
  SUM(
    CASE
      WHEN si.price_recurring_interval = 'month' THEN si.price_unit_amount
      WHEN si.price_recurring_interval = 'year' THEN si.price_unit_amount / 12
    END
  ) / 100.0 AS mrr_eur
FROM subscriptions s
JOIN subscription_items si ON si.subscription_id = s.id
JOIN prices pr ON pr.id = si.price_id
JOIN products p ON p.id = pr.product_id
WHERE s.status = 'active'
  AND s.livemode = true
GROUP BY p.name
ORDER BY mrr_eur DESC;

-- Taux de churn mensuel
SELECT
  DATE_TRUNC('month', s.canceled_at) AS month,
  COUNT(*) AS churned_subscriptions,
  (SELECT COUNT(*) FROM subscriptions WHERE status = 'active') AS total_active,
  ROUND(COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM subscriptions WHERE status = 'active'), 0), 2) AS churn_rate_pct
FROM subscriptions s
WHERE s.status = 'canceled'
  AND s.canceled_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '6 months')
GROUP BY DATE_TRUNC('month', s.canceled_at)
ORDER BY month DESC;

-- Revenue par region (top 10 pays)
SELECT
  c.address_country AS country,
  COUNT(DISTINCT ch.customer_id) AS customers,
  SUM(ch.amount) / 100.0 AS total_revenue,
  AVG(ch.amount) / 100.0 AS avg_transaction
FROM charges ch
JOIN customers c ON c.id = ch.customer_id
WHERE ch.status = 'succeeded'
  AND ch.created >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
  AND ch.livemode = true
GROUP BY c.address_country
ORDER BY total_revenue DESC
LIMIT 10;

-- Analyse des disputes
SELECT
  d.reason,
  COUNT(*) AS dispute_count,
  SUM(d.amount) / 100.0 AS total_disputed,
  SUM(CASE WHEN d.status = 'won' THEN 1 ELSE 0 END) AS won,
  SUM(CASE WHEN d.status = 'lost' THEN 1 ELSE 0 END) AS lost,
  ROUND(SUM(CASE WHEN d.status = 'won' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS win_rate_pct
FROM disputes d
WHERE d.created >= DATE_TRUNC('year', CURRENT_DATE)
GROUP BY d.reason
ORDER BY dispute_count DESC;
```

### Stripe Data Pipeline

Exporter automatiquement les donnees Stripe vers un data warehouse pour l'analyse avancee :

```
Configuration :
1. Dashboard > Settings > Data Pipeline
2. Selectionner la destination (Snowflake, Amazon Redshift, ou un bucket S3/GCS)
3. Configurer la frequence de sync (toutes les heures ou quotidien)
4. Selectionner les tables a exporter (charges, customers, subscriptions, invoices, etc.)

Avantages :
- Donnees brutes completes (pas d'aggregation)
- Jointure avec les donnees internes (CRM, product analytics)
- Requetes SQL avancees sans impact sur l'API Stripe
- Historique complet des transactions
- Support des outils BI (Looker, Tableau, Metabase, dbt)
```

### Integration avec dbt (Data Build Tool)

```yaml
# models/stripe/mrr.sql (dbt model)
# Calcul du MRR avec gestion des upgrades/downgrades

WITH active_subscriptions AS (
  SELECT
    s.id AS subscription_id,
    s.customer_id,
    si.price_id,
    p.unit_amount,
    p.recurring_interval,
    CASE
      WHEN p.recurring_interval = 'month' THEN p.unit_amount
      WHEN p.recurring_interval = 'year' THEN p.unit_amount / 12
    END AS monthly_amount,
    s.current_period_start,
    s.current_period_end
  FROM {{ source('stripe', 'subscriptions') }} s
  JOIN {{ source('stripe', 'subscription_items') }} si ON si.subscription_id = s.id
  JOIN {{ source('stripe', 'prices') }} p ON p.id = si.price_id
  WHERE s.status = 'active'
)

SELECT
  DATE_TRUNC('month', CURRENT_DATE) AS month,
  COUNT(DISTINCT customer_id) AS active_customers,
  SUM(monthly_amount) / 100.0 AS mrr,
  SUM(monthly_amount) / 100.0 * 12 AS arr
FROM active_subscriptions
```

---

## Summary Checklist

Verifier ces points sur chaque integration financiere :

- [ ] La revenue recognition respecte ASC 606/IFRS 15 (reconnaissance lineaire pour les abonnements)
- [ ] Le deferred revenue est correctement suivi pour les paiements d'avance
- [ ] Stripe Tax est active avec les immatriculations fiscales correctes
- [ ] Les codes fiscaux des produits sont correctement assignes (txcd_xxx)
- [ ] Les numeros de TVA des clients B2B sont collectes et verifies
- [ ] Les ecritures comptables couvrent : charges, refunds, disputes, payouts, fees
- [ ] La reconciliation des payouts est effectuee regulierement
- [ ] Les descripteurs de facturation sont clairs pour le client
- [ ] Le processus de gestion des litiges est documente et teste
- [ ] Les preuves de litige sont preparees en avance (logs d'acces, recus, CGV)
- [ ] Le taux de dispute est monitore avec alerte a 0.5%
- [ ] Les devises zero-decimal sont correctement gerees
- [ ] Les KPIs financiers sont calcules et suivis (MRR, churn, NRR, dispute rate)
- [ ] Les rapports Sigma ou Data Pipeline sont configures pour le reporting
