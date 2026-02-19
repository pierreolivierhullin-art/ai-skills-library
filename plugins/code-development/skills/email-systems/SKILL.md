---
name: email-systems
version: 1.0.0
description: >
  Transactional email infrastructure Resend Postmark SendGrid AWS SES,
  email deliverability SPF DKIM DMARC authentication DNS records,
  React Email templates responsive email HTML CSS rendering,
  email testing Mailtrap Mailhog email preview,
  bounce handling complaint management suppression list,
  queue workers retry mechanisms dead letter queue email,
  webhook events email tracking open click unsubscribe,
  bulk email sending rate limits warm-up sender reputation
---

# Email Systems — Infrastructure d'Email Transactionnel

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu intègres l'envoi d'email dans une application (confirmation, réinitialisation, notifications)
- Les emails finissent dans le dossier spam et tu dois améliorer la délivrabilité
- Tu veux créer des templates d'email en React (React Email)
- Tu dois gérer les rebonds, plaintes et désabonnements correctement
- Tu choisis entre Resend, Postmark, SendGrid ou AWS SES
- Tu mets en place une architecture de file d'attente pour l'envoi asynchrone

---

## Resend — L'API Email Moderne

```typescript
import { Resend } from 'resend';
import { render } from '@react-email/render';
import { EmailBienvenue } from './templates/EmailBienvenue';

const resend = new Resend(process.env.RESEND_API_KEY);

// Envoi simple
await resend.emails.send({
  from: 'Mon App <noreply@monapp.fr>',
  to: ['utilisateur@exemple.fr'],
  subject: 'Bienvenue sur Mon App',
  react: EmailBienvenue({ prénom: 'Pierre', token: 'abc123' }),
  // Optionnel
  reply_to: 'support@monapp.fr',
  tags: [{ name: 'type', value: 'bienvenue' }],
});

// Envoi avec pièce jointe
await resend.emails.send({
  from: 'Facturation <facturation@monapp.fr>',
  to: [user.email],
  subject: `Facture ${facture.référence}`,
  react: EmailFacture({ facture }),
  attachments: [
    {
      filename: `facture-${facture.référence}.pdf`,
      content: pdfBuffer,
      content_type: 'application/pdf',
    },
  ],
});
```

### Webhooks Resend — Traiter les Événements

```typescript
// app/api/webhooks/email/route.ts
import { Webhook } from 'svix';
import { headers } from 'next/headers';

const WEBHOOK_SECRET = process.env.RESEND_WEBHOOK_SECRET!;

export async function POST(req: Request) {
  const headersList = headers();
  const svixId = headersList.get('svix-id');
  const svixTimestamp = headersList.get('svix-timestamp');
  const svixSignature = headersList.get('svix-signature');

  const payload = await req.text();

  // Vérifier la signature
  const wh = new Webhook(WEBHOOK_SECRET);
  let event: ResendWebhookEvent;

  try {
    event = wh.verify(payload, {
      'svix-id': svixId!,
      'svix-timestamp': svixTimestamp!,
      'svix-signature': svixSignature!,
    }) as ResendWebhookEvent;
  } catch {
    return Response.json({ error: 'Invalid signature' }, { status: 400 });
  }

  switch (event.type) {
    case 'email.delivered':
      await db.emails.updateStatus(event.data.email_id, 'LIVRÉ');
      break;

    case 'email.bounced':
      // Rebond permanent → désactiver l'adresse
      if (event.data.bounce.type === 'hard') {
        await db.utilisateurs.supprimerEmail(event.data.to[0]);
        await db.suppressionList.ajouter(event.data.to[0], 'HARD_BOUNCE');
      }
      break;

    case 'email.complained':
      // Plainte spam → désabonner immédiatement
      await db.suppressionList.ajouter(event.data.to[0], 'PLAINTE_SPAM');
      await db.utilisateurs.désabonnerMarketing(event.data.to[0]);
      break;

    case 'email.clicked':
      await db.tracking.enregistrerClic(event.data.email_id, event.data.click.link);
      break;
  }

  return Response.json({ reçu: true });
}
```

---

## React Email — Templates Réactifs

```typescript
// emails/templates/EmailBienvenue.tsx
import {
  Html, Head, Body, Container, Section,
  Heading, Text, Button, Link, Hr, Img,
  Preview, Tailwind,
} from '@react-email/components';

interface EmailBienvenueProps {
  prénom: string;
  token: string;
  urlBase?: string;
}

export function EmailBienvenue({
  prénom,
  token,
  urlBase = 'https://monapp.fr',
}: EmailBienvenueProps) {
  const urlConfirmation = `${urlBase}/auth/confirmer?token=${token}`;

  return (
    <Html>
      <Head />
      <Preview>Bienvenue {prénom} — Confirmez votre adresse email</Preview>
      <Tailwind>
        <Body className="bg-gray-50 font-sans">
          <Container className="mx-auto my-10 max-w-[600px] bg-white rounded-lg shadow-sm">
            {/* En-tête */}
            <Section className="px-8 py-6 bg-blue-600 rounded-t-lg">
              <Img
                src={`${urlBase}/logo-blanc.png`}
                alt="Mon App"
                width={120}
                height={40}
              />
            </Section>

            {/* Corps */}
            <Section className="px-8 py-6">
              <Heading className="text-2xl font-bold text-gray-900 mb-4">
                Bienvenue, {prénom} !
              </Heading>
              <Text className="text-gray-600 mb-6">
                Merci de vous être inscrit sur Mon App. Pour finaliser
                votre compte, confirmez votre adresse email en cliquant
                sur le bouton ci-dessous.
              </Text>
              <Button
                href={urlConfirmation}
                className="bg-blue-600 text-white rounded-md px-6 py-3 text-base font-medium no-underline block text-center"
              >
                Confirmer mon adresse email
              </Button>
              <Text className="text-sm text-gray-500 mt-4">
                Ce lien expire dans 24h. Si vous n&apos;avez pas créé de
                compte, ignorez cet email.
              </Text>
            </Section>

            <Hr className="border-gray-200" />

            {/* Pied de page */}
            <Section className="px-8 py-4 text-center">
              <Text className="text-xs text-gray-400">
                © 2025 Mon App • 123 Rue Example, Paris 75001
              </Text>
              <Text className="text-xs">
                <Link href={`${urlBase}/désabonnement?token=${token}`}
                  className="text-gray-400 underline">
                  Se désabonner
                </Link>
              </Text>
            </Section>
          </Container>
        </Body>
      </Tailwind>
    </Html>
  );
}
```

```typescript
// emails/preview.tsx — Serveur de preview local
// Lancer : npx email dev --dir ./emails/templates
// Accéder à : http://localhost:3000

// Générer le HTML pour l'envoi
import { render } from '@react-email/render';
import { EmailBienvenue } from './templates/EmailBienvenue';

const html = render(
  <EmailBienvenue prénom="Pierre" token="abc123" />,
  { pretty: true }
);
const texte = render(
  <EmailBienvenue prénom="Pierre" token="abc123" />,
  { plainText: true }
);
```

---

## Délivrabilité — SPF, DKIM, DMARC

```
Configuration DNS pour votre domaine (monapp.fr) :

1. SPF (Sender Policy Framework)
   Type: TXT
   Hôte: @
   Valeur: "v=spf1 include:_spf.resend.com include:_spf.sendgrid.net ~all"
   TTL: 3600
   → Autorise les serveurs Resend/SendGrid à envoyer depuis votre domaine

2. DKIM (DomainKeys Identified Mail)
   Type: CNAME (Resend génère automatiquement)
   Hôte: resend._domainkey.monapp.fr
   Valeur: resend._domainkey.resend.com
   → Signe cryptographiquement les emails sortants

3. DMARC (Domain-based Message Authentication)
   Type: TXT
   Hôte: _dmarc.monapp.fr
   Valeur: "v=DMARC1; p=quarantine; rua=mailto:dmarc@monapp.fr; pct=100; adkim=s; aspf=s"
   TTL: 3600
   → Politique d'action si SPF/DKIM échoue

Progression recommandée DMARC :
Phase 1 : p=none    (surveillance seulement, aucun impact)
Phase 2 : p=quarantine; pct=10  (quarantaine pour 10% des emails)
Phase 3 : p=quarantine; pct=100 (quarantaine pour tout)
Phase 4 : p=reject  (rejeter complètement les emails non authentifiés)
```

---

## File d'Attente — Envoi Asynchrone avec BullMQ

```typescript
// queues/email.queue.ts
import { Queue, Worker, Job } from 'bullmq';
import { redis } from '../lib/redis';

// Définition de la queue
export const emailQueue = new Queue('email', {
  connection: redis,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 5000,  // 5s, 25s, 125s
    },
    removeOnComplete: { age: 86400 },  // Garder 24h
    removeOnFail: { age: 604800 },     // Garder 7 jours les échecs
  },
});

// Typage des jobs
interface JobEmailTransactionnel {
  destinataire: string;
  type: 'BIENVENUE' | 'CONFIRMATION' | 'RÉINITIALISATION' | 'FACTURE';
  données: Record<string, unknown>;
}

// Ajouter à la queue
export async function planifierEmail(data: JobEmailTransactionnel) {
  return emailQueue.add('envoyer', data, {
    // Délai avant l'envoi (ex: email de suivi 24h après)
    delay: data.type === 'SUIVI' ? 24 * 60 * 60 * 1000 : 0,
    // Priorité (1 = urgent)
    priority: data.type === 'RÉINITIALISATION' ? 1 : 10,
  });
}

// Worker — traiter les jobs
export const emailWorker = new Worker<JobEmailTransactionnel>(
  'email',
  async (job: Job<JobEmailTransactionnel>) => {
    const { destinataire, type, données } = job.data;

    // Vérifier la liste de suppression
    const supprimé = await db.suppressionList.existe(destinataire);
    if (supprimé) {
      console.log(`Email ignoré pour ${destinataire} (liste de suppression)`);
      return;
    }

    switch (type) {
      case 'BIENVENUE':
        await resend.emails.send({
          from: 'Mon App <noreply@monapp.fr>',
          to: [destinataire],
          subject: 'Bienvenue !',
          react: EmailBienvenue(données as EmailBienvenueProps),
        });
        break;
      // ... autres types
    }

    // Enregistrer dans l'historique
    await db.emails.créer({
      destinataire,
      type,
      statut: 'ENVOYÉ',
      jobId: job.id,
    });
  },
  {
    connection: redis,
    concurrency: 10,  // 10 emails en parallèle maximum
  }
);

// Gérer les erreurs
emailWorker.on('failed', async (job, err) => {
  console.error(`Job ${job?.id} échoué après ${job?.attemptsMade} tentatives:`, err);
  if (job && job.attemptsMade >= (job.opts.attempts ?? 3)) {
    // Déplacer vers dead-letter queue
    await db.emails.marquerÉchec(job.id!, err.message);
  }
});
```

---

## Tests — Mailtrap et Intercepteurs

```typescript
// tests/setup.ts — Intercepter les emails en développement
import nodemailer from 'nodemailer';

// Mailtrap (service de test) — capte les emails sans les envoyer
const transporter = nodemailer.createTransport({
  host: 'sandbox.smtp.mailtrap.io',
  port: 2525,
  auth: {
    user: process.env.MAILTRAP_USER,
    pass: process.env.MAILTRAP_PASS,
  },
});

// Vitest — mock de l'envoi d'email
vi.mock('../lib/email', () => ({
  planifierEmail: vi.fn().mockResolvedValue({ id: 'mock-id' }),
  envoyerEmail: vi.fn().mockResolvedValue({ id: 'mock-id' }),
}));

// Test d'intégration — vérifier le contenu du template
import { render } from '@react-email/render';
import { EmailBienvenue } from '../emails/templates/EmailBienvenue';

describe('EmailBienvenue', () => {
  it('inclut le lien de confirmation', () => {
    const html = render(
      <EmailBienvenue prénom="Alice" token="test-token-123" />,
      { pretty: false }
    );

    expect(html).toContain('test-token-123');
    expect(html).toContain('Confirmer mon adresse email');
    expect(html).not.toContain('undefined');
  });

  it('inclut un lien de désabonnement', () => {
    const html = render(
      <EmailBienvenue prénom="Alice" token="test-token-123" />
    );
    expect(html).toContain('désabonnement');
  });
});
```

---

## Comparatif des Prestataires

```
                Resend       Postmark     SendGrid      AWS SES
────────────────────────────────────────────────────────────────
DX / API        ⭐⭐⭐⭐⭐    ⭐⭐⭐⭐      ⭐⭐⭐         ⭐⭐⭐
Délivrabilité   ⭐⭐⭐⭐⭐    ⭐⭐⭐⭐⭐    ⭐⭐⭐⭐        ⭐⭐⭐⭐
React Email     ✅ Natif      🔶 Partiel    🔶             ❌
Webhook events  ✅ Svix       ✅            ✅             ✅ (SNS)
Analytics       ✅ Dashboard  ✅ Excellent  ✅             ❌ minimal
Prix 100K/mois  ~$20         ~$74         ~$15           ~$10
Idéal pour      Startups     SaaS B2B      Volume élevé  AWS shops
SDK TypeScript  ✅ Excellent  ✅ Bon        🔶 Verbose     🔶
```

---

## Références

- `references/deliverability.md` — SPF/DKIM/DMARC en profondeur, Google Postmaster Tools, Microsoft SNDS, réputation d'IP, warm-up plan d'envoi, listes de blocage, feedback loops
- `references/react-email.md` — React Email templates avancés (composants réutilisables, dark mode, client rendering matrix), Maizzle, MJML comparé, tests Litmus
- `references/queue-architecture.md` — BullMQ configuration avancée, rate limiting par destinataire, dead-letter queue, dashboard Bull Board, gestion des bounces et suppressions, RGPD compliance
- `references/case-studies.md` — 4 cas : migration vers Resend avec 99.8% délivrabilité, système de notifications 1M emails/jour, DMARC p=reject en 6 semaines, template system multi-marque
