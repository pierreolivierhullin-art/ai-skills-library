# Case Studies — 4 Systèmes Email en Production

> Quatre études de cas détaillées couvrant des problèmes réels : migration d'ESP avec amélioration de la délivrabilité, architecture haute volumétrie, déploiement DMARC p=reject sans interruption de service, et système de templates multi-marque. Chaque cas inclut le contexte, le problème, la solution technique, le process et les résultats mesurés.

---

## Cas 1 : Migration vers Resend avec 99.8% de Délivrabilité

### Contexte

FormFlux, SaaS B2B de gestion de formulaires, envoie 50 000 emails par mois : confirmations d'inscription, notifications de soumission, exports et alertes. L'équipe technique (5 développeurs, 1 designer, 1 PM) utilise SendGrid depuis le lancement. L'application Next.js s'appuie sur le SDK SendGrid Node.js avec des templates MJML compilés manuellement. Les emails sont envoyés depuis un domaine partagé SendGrid par défaut — FormFlux n'a jamais configuré de domaine d'envoi dédié. Le taux d'ouverture plafonne à 18% contre un benchmark SaaS B2B de 30-40%, et les clients signalent régulièrement des emails manquants. L'équipe growth lance un audit de délivrabilité lors de la préparation d'une campagne de réactivation.

### Problème

L'audit révèle quatre problèmes structurels.

**Domaine partagé avec mauvaise réputation :** FormFlux envoie depuis `noreply@forms.sendgrid.net`, un sous-domaine SendGrid partagé entre des milliers d'expéditeurs. Un seul acteur malveillant sur ce pool peut dégrader la réputation de tout le monde. Google Postmaster Tools indique une réputation de domaine "Low" — les emails arrivent directement dans le dossier spam pour 38% des destinataires Gmail.

**Absence de DMARC :** Aucun enregistrement SPF sur le domaine `formflux.io`, et DMARC non configuré. Les emails de phishing usurpant le domaine FormFlux circulent sans être bloqués, ce qui aggrave la réputation du domaine.

**Templates non responsifs :** Les templates MJML compilés datent de 2021. Sur mobile (67% des ouvertures), les CTAs sont inaccessibles — boutons trop petits, texte tronqué. Le taux de clic mobile est de 0.8% contre 4.2% sur desktop.

**Spam rate élevé :** Le taux de spam mesuré via Google Postmaster Tools atteint 6.7%, bien au-dessus du seuil critique de 0.30%. L'absence de liste de suppression correctement maintenue permet d'envoyer à des adresses ayant signalé des spams sur le domaine partagé — les plaintes s'accumulent.

### Solution

L'équipe opte pour une migration vers Resend pour trois raisons : SDK TypeScript moderne avec support natif de React Email, domaine d'envoi dédié inclus dès le plan gratuit, et interface de gestion des événements (bounces, plaintes) simplifiée.

**Semaine 1-2 : Infrastructure DNS**

Configurer le domaine d'envoi dédié `mail.formflux.io` avec les trois enregistrements d'authentification :

```dns
; SPF — autoriser uniquement les serveurs Resend
mail.formflux.io. IN TXT "v=spf1 include:_spf.resend.com -all"

; DKIM — délégation CNAME vers Resend (rotation automatique des clés)
resend._domainkey.mail.formflux.io. IN CNAME resend._domainkey.resend.com.

; DMARC — commencer par p=none pour surveiller sans impact
_dmarc.formflux.io. IN TXT "v=DMARC1; p=none; rua=mailto:dmarc@formflux.io; ruf=mailto:dmarc-ruf@formflux.io"
```

**Semaine 2-3 : Refonte des templates avec React Email**

Remplacer les 8 templates MJML par des composants React Email avec des design tokens partagés. Les templates sont mobile-first avec des CTAs de 48px de hauteur minimum et un inline style system compatible Outlook.

```typescript
// Avant : MJML compilé, inline HTML statique
// Après : React Email avec composants réutilisables
import { EmailBienvenue } from './templates/EmailBienvenue';

await resend.emails.send({
  from: 'FormFlux <notifications@mail.formflux.io>',
  to: [user.email],
  subject: 'Votre formulaire est prêt',
  react: EmailBienvenue({ prénom: user.prénom, lienFormulaire: form.url }),
});
```

**Semaine 3-4 : Warm-up progressif**

Le domaine `mail.formflux.io` étant nouveau, un warm-up sur 4 semaines est indispensable. Segmenter la liste par engagement : d'abord les utilisateurs ayant ouvert un email dans les 30 derniers jours, puis 60j, puis 90j.

| Semaine | Volume/jour | Segment ciblé |
|---------|------------|---------------|
| 1 | 50-200 | Actifs 30j (plus hauts taux d'ouverture) |
| 2 | 500-1000 | Actifs 60j |
| 3 | 2000-5000 | Actifs 90j |
| 4 | Volume nominal | Liste complète avec suppressions propres |

Configurer des alertes dans Google Postmaster Tools : si le spam rate dépasse 0.05%, geler les envois et analyser.

**Semaine 5-6 : DMARC p=reject**

Après 2 semaines de rapports DMARC en mode `p=none`, tous les expéditeurs légitimes apparaissent dans les rapports. La progression :
- Semaine 5 : `p=quarantine; pct=25`
- Fin semaine 5 : `p=quarantine; pct=100`
- Semaine 6 : `p=reject; pct=100`

### Résultats

| Métrique | Avant migration | Après migration |
|----------|----------------|-----------------|
| Inbox rate Gmail | 61.3% | 99.8% |
| Spam rate | 6.7% | 0.1% |
| Taux d'ouverture | 18.2% | 34.7% |
| Taux de clic mobile | 0.8% | 3.9% |
| Hard bounces | 3.2% | 0.3% |
| Phishing détecté (DMARC) | Non mesuré | 847 tentatives bloquées/mois |

### Leçons apprises

Ne jamais envoyer depuis un domaine partagé ESP en production — le coût d'un domaine dédié est nul (Resend l'inclut), mais l'impact sur la délivrabilité est massif. Le DMARC `p=none` doit être activé dès le premier email envoyé, même si le passage à `p=reject` prend des semaines. Les rapports collectés pendant cette phase sont précieux pour identifier tous les expéditeurs légitimes avant de durcir la politique.

---

## Cas 2 : Système de Notifications 1M Emails/Jour avec BullMQ

### Contexte

ThreadSpace, plateforme de collaboration pour les équipes produit, génère des notifications en temps réel : mentions dans les commentaires, assignations de tâches, digests d'activité, alertes de délais. L'application (Node.js/Fastify + React) compte 80 000 utilisateurs actifs avec une croissance de 15% par mois. Au pic (14h-17h Europe), 50 000 événements par heure génèrent des notifications.

Au lancement, l'envoi est synchrone : `await resend.emails.send(...)` dans le handler HTTP. Le système tient jusqu'à 5 000 utilisateurs actifs, puis se dégrade.

### Problème

Avec la croissance, l'envoi synchrone provoque trois types d'incidents récurrents.

**Timeouts HTTP :** L'API Resend répond en 200-800ms. Sur les endpoints qui génèrent plusieurs notifications (mention de 5 personnes dans un commentaire), le handler HTTP prend 1-4 secondes — au-delà du timeout Nginx de 3 secondes, provoquant des erreurs 504.

**Absence de retry :** Si Resend retourne une erreur 429 (rate limit) ou 5xx, l'email est silencieusement perdu. Pas de retry, pas de monitoring, pas d'alerte. Des utilisateurs signalent ne jamais recevoir leurs notifications — impossible à diagnostiquer.

**Spam des notifications :** Un utilisateur mentionné 20 fois en 5 minutes reçoit 20 emails séparés. Le taux de désabonnement des notifications atteint 34% en 6 mois — les utilisateurs préfèrent ne plus recevoir d'emails que d'être submergés.

### Solution

Refonte complète de l'infrastructure d'envoi avec BullMQ, Redis Cluster et une stratégie de digests.

**Architecture des queues par priorité :**

```typescript
// Trois queues avec priorités distinctes
const QUEUES = {
  // Priorité 1 — critique : réinitialisation mot de passe, confirmation email
  transactionnel: new Queue('notif:transactionnel', {
    connection: redis,
    defaultJobOptions: { attempts: 7, backoff: { type: 'exponential', delay: 2000 }, priority: 1 },
  }),

  // Priorité 5 — important : mentions directes, assignations
  immédiat: new Queue('notif:immédiat', {
    connection: redis,
    defaultJobOptions: { attempts: 5, backoff: { type: 'exponential', delay: 5000 }, priority: 5 },
  }),

  // Priorité 10 — non-critique : digest d'activité, résumés
  digest: new Queue('notif:digest', {
    connection: redis,
    defaultJobOptions: { attempts: 3, backoff: { type: 'exponential', delay: 30000 }, priority: 10 },
  }),
};
```

**Batching des notifications en digest 5 minutes :**

Au lieu d'envoyer immédiatement chaque notification, regrouper les notifications d'un même utilisateur sur une fenêtre glissante de 5 minutes. Si 3 mentions arrivent en 4 minutes, un seul email résume les 3.

```typescript
async function créerNotification(userId: string, événement: Événement): Promise<void> {
  // Enregistrer l'événement
  await db.notifications.créer({ userId, ...événement });

  // Vérifier si un job digest est déjà planifié pour cet utilisateur
  const jobId = `digest:${userId}`;
  const jobExistant = await QUEUES.digest.getJob(jobId);

  if (!jobExistant) {
    // Premier événement — planifier l'envoi dans 5 minutes
    await QUEUES.digest.add(
      'envoyer-digest',
      { userId },
      {
        jobId,
        delay: 5 * 60 * 1000, // 5 minutes
      }
    );
  }
  // Si un job existe déjà, il enverra toutes les notifications accumulées
}

// Worker digest — envoie toutes les notifications non lues
const digestWorker = new Worker('notif:digest', async (job) => {
  const { userId } = job.data;

  const notifications = await db.notifications.trouverNonEnvoyées(userId);
  if (notifications.length === 0) return;

  await resend.emails.send({
    to: [user.email],
    subject: `${notifications.length} nouvelle(s) notification(s) sur ThreadSpace`,
    react: DigestEmail({ notifications }),
  });

  await db.notifications.marquerEnvoyées(notifications.map(n => n.id));
});
```

**Rate limiting vers Resend (100 req/s) :**

```typescript
import { RateLimiterRedis } from 'rate-limiter-flexible';

const limiter = new RateLimiterRedis({
  storeClient: redis,
  keyPrefix: 'rl:resend',
  points: 100,       // 100 appels
  duration: 1,       // par seconde
  blockDuration: 2,  // bloquer 2s si dépassement
});

// Dans le worker
async function envoyerAvecRateLimit(données: EmailData): Promise<void> {
  try {
    await limiter.consume('resend_api');
    await resend.emails.send(données);
  } catch (rateLimitError) {
    // Remettre en queue après 2s
    throw new Error('Rate limit ESP — retry automatique');
  }
}
```

**Circuit breaker si taux d'erreur > 5% :**

```typescript
let erreursConsécutives = 0;
const SEUIL_CIRCUIT = 5;
let circuitOuvert = false;

emailWorker.on('failed', (job, error) => {
  if (error.message.includes('429') || error.message.includes('5')) {
    erreursConsécutives++;
    if (erreursConsécutives >= SEUIL_CIRCUIT && !circuitOuvert) {
      circuitOuvert = true;
      // Pause de 30 secondes avant de ré-essayer
      setTimeout(() => {
        circuitOuvert = false;
        erreursConsécutives = 0;
      }, 30000);
    }
  }
});
```

### Résultats

| Métrique | Avant | Après |
|----------|-------|-------|
| Emails perdus | Non mesuré (~500/jour) | 0 (Outbox pattern) |
| Timeouts API | 45/heure au pic | 0 |
| P50 delivery time | N/A (synchrone) | 8 secondes |
| P99 delivery time | N/A | 28 secondes |
| Désabonnements notifications | 34% en 6 mois | 8% en 6 mois |
| Coût serveur (CPU/mémoire) | 100% (baseline) | 40% (−60%) |
| Emails en attente au pic | N/A | < 200 (traités en < 2s) |

### Leçons apprises

Le batching des notifications est la fonctionnalité qui a eu le plus d'impact sur la satisfaction utilisateur — réduire le désabonnement de 34% à 8% démontre que les utilisateurs veulent être informés, mais pas submergés. La fenêtre de 5 minutes est un bon équilibre entre réactivité et agrégation. Une fenêtre plus longue (30 minutes) réduit encore plus les emails mais diminue la satisfaction pour les mentions urgentes.

---

## Cas 3 : DMARC p=reject en 6 Semaines sans Casser le Trafic Légitime

### Contexte

IndustrialAI, entreprise de conseil en automatisation industrielle (250 personnes), détecte en septembre 2024 des campagnes de phishing utilisant son domaine `industrialai.eu`. Des clients reçoivent de faux emails de factures demandant des virements bancaires urgents — le domaine est identique à celui d'IndustrialAI. La DSI identifie 3 incidents de fraude avérée et une tentative bloquée par la banque d'un client. L'enjeu dépasse la technique : responsabilité légale, réputation commerciale, et conformité NIS2.

**Complexité de la situation :** IndustrialAI utilise 12 services qui envoient des emails au nom du domaine `industrialai.eu` : Salesforce (CRM), HubSpot (marketing), Workday (RH), ServiceNow (tickets), une application interne Python/SMTP, des alertes Datadog, des notifications GitHub, des rapports automatisés depuis SAP, et 4 agences externes qui envoient des newsletters pour le compte d'IndustrialAI. Passer à `p=reject` sans inventaire complet couperait des centaines d'emails légitimes par jour.

### Problème

La transition `p=none → p=reject` sans précaution coupe tous les emails dont le SPF ou DKIM n'est pas correctement configuré. Dans une organisation de 250 personnes avec 12 expéditeurs, l'inventaire initial est incomplet et les équipes métier ignorent souvent quels services envoient des emails en leur nom.

### Solution

Six semaines de travail structuré avec une équipe pluridisciplinaire : DSI, équipes marketing, RH, finance et les équipes IT de chaque filiale.

**Semaine 1-2 : Inventaire par les rapports DMARC**

Activer DMARC `p=none` avec reporting vers un outil spécialisé (dmarcian) et attendre 72h pour collecter les premiers rapports.

```dns
_dmarc.industrialai.eu. IN TXT "v=DMARC1; p=none; rua=mailto:dmarc@industrialai.eu; ruf=mailto:dmarc-ruf@industrialai.eu; ri=3600"
```

Les rapports agrégés reçus (200 000 entrées en 48h) révèlent 23 sources IP distinctes envoyant des emails avec le domaine `industrialai.eu` :
- 8 sont connues et légitimes (Salesforce, HubSpot, etc.)
- 9 sont des services inconnus de la DSI (outils marketing d'agences, outils RH de filiales)
- 6 sont clairement malveillantes (IPs russes et chinoises — les campagnes de phishing)

**Semaine 3-4 : Authentication de tous les expéditeurs légitimes**

Pour chaque expéditeur légitime découvert, configurer SPF et DKIM :

```dns
; SPF fusionné — tous les ESPs légitimes
industrialai.eu. IN TXT "v=spf1
  include:_spf.salesforce.com
  include:_spf.hubspot.com
  include:workday.com
  include:servicenow.com
  include:_spf.mailchimp.com
  ip4:185.24.76.0/24
  -all"

; DKIM pour chaque service
salesforce._domainkey.industrialai.eu. IN CNAME ...
hubspot1._domainkey.industrialai.eu. IN CNAME ...
; ... etc.
```

Pour les 9 services inconnus découverts, contacter les équipes responsables et soit :
- Configurer DKIM/SPF si l'outil est légitime et approuvé
- Migrer vers un service approuvé
- Interdire l'utilisation si non justifié

Deux services utilisaient un sous-domaine non configuré (`newsletter.industrialai.eu`). Solution : créer les enregistrements SPF/DKIM sur ce sous-domaine, et configurer une politique DMARC séparée plus permissive pendant la transition.

```dns
; Sous-domaine newsletters — progression indépendante
_dmarc.newsletter.industrialai.eu. IN TXT "v=DMARC1; p=none; rua=mailto:dmarc-newsletter@industrialai.eu"
```

**Semaine 5 : Quarantaine progressive**

```dns
; Lundi semaine 5 : quarantaine 10%
_dmarc.industrialai.eu. IN TXT "v=DMARC1; p=quarantine; pct=10; rua=mailto:dmarc@industrialai.eu"

; Jeudi semaine 5 : quarantaine 50%
_dmarc.industrialai.eu. IN TXT "v=DMARC1; p=quarantine; pct=50; rua=mailto:dmarc@industrialai.eu"

; Lundi semaine 6 : quarantaine 100%
_dmarc.industrialai.eu. IN TXT "v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarc@industrialai.eu"
```

À chaque étape, surveiller pendant 48h les rapports DMARC et les signalements d'emails manquants. Aucun email légitime ne sera bloqué si tous les expéditeurs légitimes ont été correctement configurés à l'étape précédente.

**Semaine 6 : p=reject**

```dns
_dmarc.industrialai.eu. IN TXT "v=DMARC1; p=reject; pct=100; rua=mailto:dmarc@industrialai.eu; ruf=mailto:dmarc-ruf@industrialai.eu; fo=1"
```

### Résultats

| Métrique | Avant | Après |
|----------|-------|-------|
| Emails de phishing avec domaine IndustrialAI | 3 incidents/mois | 0 depuis le déploiement |
| Emails légitimes perdus | 0 | 0 |
| Expéditeurs inconnus découverts | N/A | 9 (dont 2 interdits) |
| Rapports d'abus clients | ~15/mois | −70% (< 5/mois) |
| Durée totale | 6 semaines | — |
| Équipes impliquées | 8 | — |

### Leçons apprises

La phase d'inventaire est la plus critique et la plus sous-estimée. Sans les rapports DMARC `p=none`, IndustrialAI n'aurait jamais identifié les 9 services "fantômes" qui envoyaient des emails en leur nom — dont deux non approuvés par la DSI. Le passage direct à `p=reject` aurait coupé des dizaines d'emails légitimes quotidiennement.

Impliquer les équipes métier dès la phase d'inventaire est indispensable. La DSI seule ne peut pas identifier tous les services utilisés par le marketing, les RH et les agences externes. Un email interne demandant à chaque département de lister leurs outils d'envoi accélère considérablement le processus.

---

## Cas 4 : Système de Templates Multi-Marque (White-Label)

### Contexte

LocalReach, plateforme SaaS de communication locale pour les réseaux de franchises et collectivités, permet à ses clients (franchiseurs, réseaux de revendeurs, associations) d'envoyer des emails à leurs propres utilisateurs finaux. Chaque client LocalReach est un "tenant" avec son propre logo, sa charte graphique, son domaine d'envoi et ses listes de contacts. La plateforme compte 500 tenants actifs, de 50 à 50 000 abonnés chacun, pour un total de 2 millions d'emails par mois.

**Contraintes techniques complexes :**
- 500 configurations de branding différentes (logo, couleurs primaires/secondaires, police)
- 500 domaines d'envoi distincts, chacun avec ses propres SPF/DKIM
- Réputation d'envoi individuelle par tenant (un tenant avec un mauvais taux de spam ne doit pas pénaliser les autres)
- Onboarding d'un nouveau tenant en moins de 10 minutes
- SLA de 99.9% de disponibilité de l'envoi

### Problème

L'architecture initiale utilise un domaine partagé `mail.localreach.fr` pour tous les tenants. Trois problèmes émergent rapidement.

**Contamination de réputation :** Un tenant avec une liste de mauvaise qualité génère des plaintes qui dégradent la réputation de `mail.localreach.fr` pour tous les autres tenants. En 2023, un tenant (réseau de 120 agences immobilières) envoie une campagne non consentie — le spam rate de tout le domaine monte à 2.3%, affectant les 499 autres tenants.

**Branding insuffisant :** Les clients franchisor veulent que leurs franchisés reçoivent des emails qui ressemblent à 100% à la marque principale. Avec un domaine partagé, le `From:` affiche `notifications@mail.localreach.fr` — les franchisés ne reconnaissent pas l'expéditeur et le taux d'ouverture est faible.

**Scalabilité de la configuration :** L'ajout d'un nouveau tenant nécessite une intervention manuelle (configuration DNS, vérification DKIM) qui prend 30 à 120 minutes selon la compétence de l'équipe support.

### Solution

Refonte de l'architecture d'envoi autour de l'isolation totale par tenant.

**Schéma de données multi-tenant :**

```sql
-- Configuration complète par tenant
CREATE TABLE tenant_email_configs (
  tenant_id      UUID PRIMARY KEY REFERENCES tenants(id),
  domain         TEXT NOT NULL UNIQUE,     -- ex: mail.franchise-dupont.fr
  from_name      TEXT NOT NULL,            -- ex: Franchise Dupont
  from_email     TEXT NOT NULL,            -- ex: notifications@mail.franchise-dupont.fr
  reply_to       TEXT,
  -- Statut d'authentification
  dkim_verified  BOOLEAN NOT NULL DEFAULT false,
  spf_verified   BOOLEAN NOT NULL DEFAULT false,
  dmarc_verified BOOLEAN NOT NULL DEFAULT false,
  -- Réputation
  reputation_score SMALLINT NOT NULL DEFAULT 100 CHECK (reputation_score BETWEEN 0 AND 100),
  suspended      BOOLEAN NOT NULL DEFAULT false,
  suspended_reason TEXT,
  -- Branding tokens
  brand_config   JSONB NOT NULL DEFAULT '{}',
  -- Métadonnées
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  verified_at    TIMESTAMPTZ
);

-- Design tokens par tenant
-- Structure brand_config :
-- {
--   "colors": { "primary": "#E63946", "secondary": "#457B9D", "text": "#1D3557", "background": "#F1FAEE" },
--   "typography": { "fontFamily": "Arial, sans-serif", "fontSize": "16px" },
--   "logo": { "url": "https://cdn.localreach.fr/logos/franchise-dupont.png", "width": 160, "height": 52, "alt": "Franchise Dupont" },
--   "footer": { "address": "123 Rue de la République, 69001 Lyon", "phone": "04 72 XX XX XX", "website": "https://franchise-dupont.fr" }
-- }
```

**Génération automatique de la configuration DNS lors de l'onboarding :**

```typescript
// services/tenant-onboarding.service.ts
async function configurerNouveauTenant(tenantId: string, domaine: string): Promise<TenantDNSConfig> {
  // 1. Générer les instructions DNS via l'API Resend
  const domaineResend = await resend.domains.create({
    name: domaine,
  });

  // Resend retourne les enregistrements DNS à créer
  const enregistrementsDNS = domaineResend.records;
  // [
  //   { type: 'TXT', name: 'resend._domainkey', value: 'p=MIIBIjAN...' },
  //   { type: 'TXT', name: 'send', value: 'v=spf1 include:_spf.resend.com ~all' },
  //   { type: 'MX', name: 'bounce', value: 'feedback-smtp.resend.com', priority: 10 }
  // ]

  // 2. Sauvegarder la configuration
  await db.tenantEmailConfigs.créer({
    tenantId,
    domain: domaine,
    fromName: (await db.tenants.findById(tenantId)).name,
    fromEmail: `notifications@${domaine}`,
    resendDomainId: domaineResend.id,
  });

  // 3. Retourner les instructions DNS pour affichage dans l'UI d'onboarding
  return {
    tenantId,
    domaine,
    enregistrementsDNS,
    instructions: générerInstructionsDNS(enregistrementsDNS),
    webhookVérification: `/api/tenants/${tenantId}/verify-dns`,
  };
}

// Vérification automatique via polling (pas d'intervention humaine)
async function vérifierDNSTenant(tenantId: string): Promise<VerificationResult> {
  const config = await db.tenantEmailConfigs.findByTenantId(tenantId);

  const résultat = await resend.domains.verify(config.resendDomainId);

  if (résultat.status === 'verified') {
    await db.tenantEmailConfigs.update(tenantId, {
      dkimVerified: true,
      spfVerified: true,
      verifiedAt: new Date(),
    });
    return { succès: true, message: 'Domaine vérifié et prêt pour l\'envoi' };
  }

  return {
    succès: false,
    enregistrementsPendants: résultat.records.filter(r => !r.verified),
  };
}
```

**Rendu des templates avec theming par tenant :**

```typescript
// services/template-renderer.service.ts
import { render } from '@react-email/render';

async function rendreEmailPourTenant<T extends object>(
  tenantId: string,
  templateNom: string,
  données: T
): Promise<{ html: string; text: string }> {
  // Charger la configuration de branding du tenant
  const config = await db.tenantEmailConfigs.findByTenantId(tenantId);
  const brandConfig = config.brandConfig as TenantBrandConfig;

  // Créer un thème à partir des tokens du tenant
  const theme: EmailTheme = {
    colors: {
      primary: brandConfig.colors.primary ?? '#3B82F6',
      secondary: brandConfig.colors.secondary ?? '#6366F1',
      text: brandConfig.colors.text ?? '#111827',
      background: brandConfig.colors.background ?? '#F9FAFB',
    },
    logo: brandConfig.logo,
    footer: brandConfig.footer,
    typography: brandConfig.typography ?? { fontFamily: 'Arial, sans-serif' },
  };

  // Importer dynamiquement le template
  const { default: Template } = await import(`../email-templates/${templateNom}`);

  const html = render(<Template theme={theme} {...données} />);
  const text = render(<Template theme={theme} {...données} />, { plainText: true });

  return { html, text };
}

// Envoi avec isolation de réputation par tenant
async function envoyerEmailTenant(
  tenantId: string,
  destinataire: string,
  template: string,
  données: object
): Promise<void> {
  const config = await db.tenantEmailConfigs.findByTenantId(tenantId);

  // Vérifier que le tenant n'est pas suspendu
  if (config.suspended) {
    throw new Error(`Tenant ${tenantId} suspendu : ${config.suspendedReason}`);
  }

  // Vérifier la liste de suppression du tenant (isolée par tenant)
  const estSupprimé = await db.tenantSuppressions.existe(tenantId, destinataire);
  if (estSupprimé) return;

  const { html, text } = await rendreEmailPourTenant(tenantId, template, données);

  // Envoyer depuis le domaine du tenant — réputation isolée
  await resend.emails.send({
    from: `${config.fromName} <${config.fromEmail}>`,
    to: [destinataire],
    html,
    text,
    // Tag tenant pour le filtering dans les webhooks
    tags: [
      { name: 'tenant_id', value: tenantId },
      { name: 'template', value: template },
    ],
  });
}
```

**Monitoring de la réputation par tenant et suspension automatique :**

```typescript
// jobs/tenant-reputation-monitor.ts (cron toutes les heures)
async function surveillerRéputationTenants(): Promise<void> {
  const tenants = await db.tenantEmailConfigs.findActifs();

  for (const tenant of tenants) {
    // Calculer les métriques des dernières 24h
    const métriques = await db.emailStats.calculerPourTenant(tenant.tenantId, '24h');

    const scoreRéputation = calculerScore(métriques);

    await db.tenantEmailConfigs.updateScore(tenant.tenantId, scoreRéputation);

    // Suspension automatique si les seuils sont dépassés
    if (métriques.spamRate > 0.5 || métriques.bounceRate > 5 || scoreRéputation < 30) {
      await suspendTenant(tenant.tenantId, {
        raison: `Score de réputation critique : spam ${métriques.spamRate}%, bounce ${métriques.bounceRate}%`,
        métriques,
      });

      await notifierAdminLocalReach(tenant.tenantId, métriques);
    }
  }
}

function calculerScore(métriques: EmailMetrics): number {
  let score = 100;
  score -= métriques.spamRate * 40;        // Chaque 1% de spam = −40 points
  score -= métriques.bounceRate * 5;        // Chaque 1% de bounce = −5 points
  score -= métriques.plaintes * 10;         // Chaque plainte = −10 points
  score += métriques.openRate * 0.5;        // Chaque 1% d'ouverture = +0.5 points
  return Math.max(0, Math.min(100, score));
}
```

### Résultats

| Métrique | Avant refonte | Après refonte |
|----------|--------------|---------------|
| Durée onboarding nouveau tenant | 30-120 min (manuel) | < 10 min (automatique) |
| Contamination réputation cross-tenant | Oui (incident 2023) | Non — isolation totale |
| Tenants avec branding distinct | 0 | 500 (100%) |
| SLA disponibilité envoi | 99.2% | 99.94% |
| Tenants suspendus automatiquement | N/A | 3 depuis 6 mois (abus détectés) |
| Satisfaction clients (NPS) | 42 | 71 |

### Leçons apprises

L'isolation de réputation par tenant est la feature qui a eu le plus d'impact commercial. Les clients enterprise refusaient la plateforme partagée par crainte de la contamination de réputation — la garantie d'un domaine dédié a débloqué 12 contrats enterprise en 6 mois. Le coût opérationnel est négligeable (domaines dédiés gratuits avec Resend, configuration automatisée).

La suspension automatique des tenants abusifs est indispensable dès le premier jour sur une plateforme multi-tenant. Sans elle, un seul client malveillant peut compromettre la réputation de toute la plateforme. La clé est de définir des seuils précis (spam rate > 0.5%, pas 5%) et d'alerter l'équipe support simultanément pour investiguer avant de suspendre définitivement.

L'onboarding DNS en moins de 10 minutes est possible uniquement parce que Resend expose une API complète de gestion des domaines. Vérifier que l'ESP choisi pour une architecture multi-tenant supporte la gestion programmatique des domaines — certains ESPs nécessitent encore une intervention humaine pour la configuration DKIM.
