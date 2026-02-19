# React Email — Templates Avancés, Dark Mode et Client Compatibility

> Référence complète pour créer des templates email en React. Couvre l'architecture de composants, Tailwind dans les emails, le dark mode, la compatibilité cross-client, les contraintes CSS, la typographie, le responsive design et les outils de test.

---

## Architecture de Templates

### Structure de projet recommandée

```
emails/
├── components/           # Composants réutilisables
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── Button.tsx
│   ├── Divider.tsx
│   └── index.ts
├── templates/            # Templates complets
│   ├── EmailBienvenue.tsx
│   ├── EmailConfirmation.tsx
│   ├── EmailMotDePasse.tsx
│   ├── EmailFacture.tsx
│   └── EmailNotification.tsx
├── tokens/               # Design tokens
│   └── theme.ts
└── preview.ts            # Point d'entrée pour le serveur de preview
```

### Design tokens et thème

Définir les design tokens en TypeScript et les utiliser dans tous les composants pour garantir la cohérence visuelle.

```typescript
// emails/tokens/theme.ts
export const theme = {
  colors: {
    primary: '#3B82F6',
    primaryDark: '#1D4ED8',
    text: '#111827',
    textMuted: '#6B7280',
    background: '#F9FAFB',
    surface: '#FFFFFF',
    border: '#E5E7EB',
    danger: '#EF4444',
    success: '#10B981',
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px',
  },
  typography: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    h1: { fontSize: '28px', fontWeight: '700', lineHeight: '36px' },
    h2: { fontSize: '22px', fontWeight: '600', lineHeight: '30px' },
    body: { fontSize: '16px', fontWeight: '400', lineHeight: '26px' },
    small: { fontSize: '13px', fontWeight: '400', lineHeight: '20px' },
  },
  borderRadius: '8px',
  maxWidth: '600px',
} as const;

export type Theme = typeof theme;
```

### Composants réutilisables

```tsx
// emails/components/Header.tsx
import { Img, Section } from '@react-email/components';
import { theme } from '../tokens/theme';

interface HeaderProps {
  logoUrl?: string;
  logoAlt?: string;
  backgroundColor?: string;
}

export function Header({
  logoUrl = 'https://monapp.fr/logo.png',
  logoAlt = 'Mon App',
  backgroundColor = theme.colors.primary,
}: HeaderProps) {
  return (
    <Section
      style={{
        backgroundColor,
        padding: `${theme.spacing.lg} ${theme.spacing.xl}`,
        borderRadius: `${theme.borderRadius} ${theme.borderRadius} 0 0`,
      }}
    >
      <Img
        src={logoUrl}
        alt={logoAlt}
        width={140}
        height={46}
        style={{ display: 'block' }}
      />
    </Section>
  );
}

// emails/components/Button.tsx
import { Button as EmailButton } from '@react-email/components';
import { theme } from '../tokens/theme';

interface ButtonProps {
  href: string;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
}

const variantStyles = {
  primary: { backgroundColor: theme.colors.primary, color: '#FFFFFF' },
  secondary: { backgroundColor: '#FFFFFF', color: theme.colors.primary, border: `2px solid ${theme.colors.primary}` },
  danger: { backgroundColor: theme.colors.danger, color: '#FFFFFF' },
};

export function Button({ href, children, variant = 'primary' }: ButtonProps) {
  return (
    <EmailButton
      href={href}
      style={{
        ...variantStyles[variant],
        borderRadius: theme.borderRadius,
        padding: `${theme.spacing.md} ${theme.spacing.xl}`,
        fontSize: '16px',
        fontWeight: '600',
        textDecoration: 'none',
        display: 'inline-block',
        textAlign: 'center',
        fontFamily: theme.typography.fontFamily,
      }}
    >
      {children}
    </EmailButton>
  );
}

// emails/components/Footer.tsx
import { Hr, Section, Text, Link } from '@react-email/components';
import { theme } from '../tokens/theme';

interface FooterProps {
  unsubscribeUrl?: string;
  companyName?: string;
  address?: string;
}

export function Footer({
  unsubscribeUrl,
  companyName = 'Mon App',
  address = '123 Rue Example, 75001 Paris',
}: FooterProps) {
  return (
    <>
      <Hr style={{ borderColor: theme.colors.border, margin: '0' }} />
      <Section style={{ padding: `${theme.spacing.lg} ${theme.spacing.xl}`, textAlign: 'center' as const }}>
        <Text style={{ ...theme.typography.small, color: theme.colors.textMuted, margin: '0 0 8px' }}>
          &copy; {new Date().getFullYear()} {companyName} &bull; {address}
        </Text>
        {unsubscribeUrl && (
          <Text style={{ ...theme.typography.small, margin: '0' }}>
            <Link href={unsubscribeUrl} style={{ color: theme.colors.textMuted, textDecoration: 'underline' }}>
              Se désabonner
            </Link>
          </Text>
        )}
      </Section>
    </>
  );
}
```

---

## Tailwind dans React Email

### Configuration et limites

```tsx
// Utiliser @react-email/tailwind pour les classes utilitaires
import { Tailwind } from '@react-email/components';

export function EmailAvecTailwind() {
  return (
    <Tailwind
      config={{
        theme: {
          extend: {
            colors: {
              brand: '#3B82F6',
            },
          },
        },
      }}
    >
      <div className="bg-gray-50 font-sans">
        <div className="mx-auto max-w-[600px] bg-white">
          <p className="text-gray-700 text-base leading-7 px-8 py-4">
            Contenu de l'email
          </p>
        </div>
      </div>
    </Tailwind>
  );
}
```

**Limitations de Tailwind dans les emails :**

| Fonctionnalité Tailwind | Support email | Alternative |
|------------------------|--------------|-------------|
| Pseudo-classes (`:hover`, `:focus`) | Non supporté | Inline styles uniquement |
| Media queries responsive (`sm:`, `md:`) | Supporté dans Gmail Web, Apple Mail uniquement | Tables imbriquées + largeurs fixes |
| Dark mode (`dark:`) | Limité | `@media (prefers-color-scheme: dark)` dans `<style>` |
| Animations (`animate-`) | Non supporté | GIF animés |
| Grid (`grid`, `grid-cols-`) | Non supporté | Tables HTML |
| Flexbox (`flex`, `justify-`) | Gmail Web seulement | Tables HTML |
| `gap-` | Non supporté | `cellspacing` ou `margin` |

---

## Dark Mode Email

### Implémentation complète

```tsx
// emails/templates/EmailDarkModeReady.tsx
import { Html, Head, Body, Container } from '@react-email/components';

export function EmailDarkModeReady() {
  return (
    <Html>
      <Head>
        {/* Styles dark mode dans le <head> — supporté par Apple Mail, Gmail App iOS/Android */}
        <style>{`
          @media (prefers-color-scheme: dark) {
            .email-body {
              background-color: #1a1a2e !important;
            }
            .email-container {
              background-color: #16213e !important;
            }
            .email-text {
              color: #e2e8f0 !important;
            }
            .email-text-muted {
              color: #94a3b8 !important;
            }
            .email-border {
              border-color: #334155 !important;
            }
            /* Inverser les logos clairs */
            .logo-light { display: none !important; }
            .logo-dark { display: block !important; }
          }
        `}</style>
      </Head>
      <Body
        className="email-body"
        style={{ backgroundColor: '#F9FAFB', margin: '0', padding: '0' }}
      >
        <Container
          className="email-container"
          style={{
            backgroundColor: '#FFFFFF',
            maxWidth: '600px',
            margin: '0 auto',
          }}
        >
          {/* Logo versioning pour dark/light */}
          <img
            className="logo-light"
            src="https://monapp.fr/logo-dark-text.png"
            alt="Mon App"
            width={140}
            style={{ display: 'block' }}
          />
          <img
            className="logo-dark"
            src="https://monapp.fr/logo-light-text.png"
            alt="Mon App"
            width={140}
            style={{ display: 'none' }}
          />
        </Container>
      </Body>
    </Html>
  );
}
```

### Quirks Outlook dark mode

Outlook 2019 et Windows Mail appliquent automatiquement un mode sombre en inversant les couleurs — ce comportement est non contrôlable par CSS. Stratégies de mitigation :

```html
<!-- Empêcher l'inversion Outlook avec meta tag (Windows Mail) -->
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">

<!-- Conditional comments MSO pour couleurs Outlook spécifiques -->
<!--[if mso]>
<style>
  .email-container { background-color: #FFFFFF !important; }
  td { color: #111827 !important; }
</style>
<![endif]-->
```

---

## Email Client Compatibility Matrix

### Matrice de support des fonctionnalités CSS

| Fonctionnalité | Gmail Web | Gmail iOS | Gmail Android | Outlook 2016/19 | Outlook 365 | Outlook Web | Apple Mail | Yahoo | Samsung |
|----------------|-----------|-----------|---------------|-----------------|-------------|-------------|------------|-------|---------|
| CSS externe | Non | Non | Non | Non | Non | Partiel | Oui | Non | Non |
| `<style>` dans `<head>` | Non | Non | Non | Non | Oui | Oui | Oui | Oui | Oui |
| Inline styles | Oui | Oui | Oui | Oui | Oui | Oui | Oui | Oui | Oui |
| Flexbox | Oui | Non | Non | Non | Non | Oui | Oui | Non | Partiel |
| CSS Grid | Non | Non | Non | Non | Non | Non | Oui | Non | Non |
| Dark mode CSS | Partiel | Oui | Oui | Non | Partiel | Non | Oui | Oui | Oui |
| GIF animés | Oui | Oui | Oui | Non (1ère frame) | Oui | Oui | Oui | Oui | Oui |
| Web fonts | Non | Non | Non | Non | Non | Non | Oui | Non | Non |
| SVG inline | Non | Non | Non | Non | Non | Non | Oui | Non | Non |
| `border-radius` | Oui | Oui | Oui | Non | Oui | Oui | Oui | Oui | Oui |
| `max-width` | Oui | Oui | Oui | Oui | Oui | Oui | Oui | Oui | Oui |

### MSO Conditional Comments pour Outlook

```html
<!-- Commentaires conditionnels MSO — seul Outlook les lit -->

<!--[if mso]>
<!-- Remplacer un div par un tableau pour Outlook -->
<table width="600" cellpadding="0" cellspacing="0" border="0">
  <tr><td>
<![endif]-->
<div style="max-width: 600px; margin: 0 auto;">
  Contenu
</div>
<!--[if mso]>
  </td></tr>
</table>
<![endif]-->

<!--[if !mso]><!-- -->
<!-- Ce bloc est visible pour tout le monde SAUF Outlook -->
<div style="display: flex; gap: 16px;">
  ...
</div>
<!--<![endif]-->
```

---

## CSS en Email

### CSS Reset minimal pour email

```html
<!-- Reset à inclure dans le <head> ou en styles Outlook -->
<style>
  /* Reset box model */
  * { box-sizing: border-box; }

  /* Images responsives */
  img { display: block; max-width: 100%; height: auto; }

  /* Liens */
  a { color: inherit; text-decoration: none; }

  /* Outlook — supprimer les espaces entre cellules */
  table { border-collapse: collapse; }

  /* Prévenir l'agrandissement automatique de police sur iOS */
  body { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
</style>
```

### Propriétés CSS fiables en email

Utiliser uniquement les propriétés avec support universel pour les éléments critiques :

```css
/* FIABLE PARTOUT */
color, background-color, font-family, font-size, font-weight,
font-style, text-align, text-decoration, line-height,
margin, padding, width, height, border, border-radius,
display (block/inline), max-width

/* SUPPORT LIMITÉ — utiliser avec fallback */
border-radius   /* Non supporté Outlook 2016/2019 */
box-shadow      /* Non supporté Outlook */
background-image /* Comportement variable */
text-shadow     /* Non supporté Outlook */
```

---

## Images en Email

### Bonnes pratiques

```tsx
import { Img } from '@react-email/components';

// CORRECT — image hébergée sur CDN public, alt text, dimensions explicites
<Img
  src="https://cdn.monapp.fr/emails/hero-illustration.png"
  alt="Illustration de bienvenue montrant notre interface"
  width={560}
  height={280}
  style={{ display: 'block', margin: '0 auto', maxWidth: '100%' }}
/>

// Pour les images retina (2x) — la largeur affichée reste 280px
<Img
  src="https://cdn.monapp.fr/emails/logo@2x.png"
  alt="Mon App"
  width={140}   // largeur d'affichage (la moitié des pixels réels)
  height={46}
/>
```

**Règles d'hébergement des images :**
- Héberger sur un CDN public accessible sans authentification (CloudFront, Cloudflare R2, imgix)
- Ne jamais utiliser `localhost` ou des URLs de preview dans les emails en production
- Format recommandé : PNG pour les logos/icônes, JPEG pour les photos, GIF pour les animations simples
- Taille maximale recommandée par image : 200 KB
- GIF animés : supportés partout sauf Outlook 2016/2019 (affiche la première frame)

### Graceful degradation sans images

De nombreux clients email bloquent les images par défaut. Concevoir en mobile d'abord, images désactivées ensuite :

```tsx
// Alt text descriptif et informatif — pas juste "image"
<Img
  src="https://cdn.monapp.fr/emails/confirmation-icon.png"
  alt="✓ Votre commande est confirmée"
  width={48}
  height={48}
/>

// Background color de fallback pour les bannières
<Section
  style={{
    backgroundColor: '#3B82F6',  // visible si l'image est bloquée
    backgroundImage: 'url(https://cdn.monapp.fr/emails/banner-bg.jpg)',
    backgroundSize: 'cover',
  }}
>
  <Heading style={{ color: '#FFFFFF' }}>Bienvenue !</Heading>
</Section>
```

---

## Typographie en Email

### System font stack

Les web fonts (Google Fonts, Typekit) ne fonctionnent pas dans la plupart des clients email. Utiliser des font stacks sûres :

```typescript
// Font stacks fiables en email
const fontStacks = {
  // Sans-serif — moderne et lisible
  sansSerif: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',

  // Serif — pour les newsletters éditoriales
  serif: 'Georgia, "Times New Roman", Times, serif',

  // Monospace — pour les codes et tokens
  monospace: 'SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace',
};
```

**Support des web fonts :**
- Apple Mail macOS/iOS : oui (via `@font-face`)
- Gmail Web : non
- Outlook : non (toujours fallback)
- Yahoo : non
- Recommandation : ne pas dépendre des web fonts pour les informations critiques

### Gotchas line-height

```tsx
// CORRECT — toujours spécifier line-height en valeur absolue (px) en email
// Les valeurs relatives (1.5) causent des incohérences entre clients
<Text style={{ fontSize: '16px', lineHeight: '26px' }}>
  Texte bien espacé avec line-height absolu.
</Text>

// INCORRECT — valeur relative problématique dans certains clients
<Text style={{ fontSize: '16px', lineHeight: '1.6' }}>
  Peut s'afficher différemment selon le client.
</Text>
```

---

## Responsive Email

### Approche mobile-first avec tables

```tsx
// Layout en colonnes responsive sans flexbox (compatible Outlook)
// Technique : float + MSO table-based fallback
export function DeuxColonnes({ gauche, droite }: { gauche: React.ReactNode; droite: React.ReactNode }) {
  return (
    <>
      {/* MSO — layout tableau pour Outlook */}
      {'<!--[if mso]>' as any}
      <table width="560" cellPadding={0} cellSpacing={0} border={0}>
        <tr>
          <td width="260" valign="top">{gauche}</td>
          <td width="40" />
          <td width="260" valign="top">{droite}</td>
        </tr>
      </table>
      {'<![endif]-->' as any}

      {/* HTML5 — layout pour les clients modernes */}
      {'<!--[if !mso]><!-->' as any}
      <div style={{ display: 'flex', gap: '40px' }}>
        <div style={{ flex: 1 }}>{gauche}</div>
        <div style={{ flex: 1 }}>{droite}</div>
      </div>
      {'<!--<![endif]-->' as any}
    </>
  );
}
```

### Contraintes responsive email

```css
/* Container max-width — TOUJOURS 600px pour la compatibilité */
.email-container { max-width: 600px; width: 100%; }

/* Sur mobile (< 600px) — passer en colonne unique via media query */
@media (max-width: 600px) {
  .email-container { width: 100% !important; }
  .colonne { width: 100% !important; display: block !important; }
  .masquer-mobile { display: none !important; }
  .padding-mobile { padding: 16px !important; }
}
```

---

## Maizzle — Alternative HTML-First

Maizzle est un framework email HTML-first avec Tailwind, PostHTML et des transformers de compatibilité. Alternative à React Email pour les équipes préférant HTML pur.

```html
<!-- Maizzle template — config/environments.js définit les transformers -->
<extends src="src/layouts/main.html">
  <block name="template">
    <table class="w-full">
      <tr>
        <td class="px-6 py-4 bg-blue-600">
          <img src="{{ asset }}/logo.png" width="140" alt="Mon App">
        </td>
      </tr>
      <tr>
        <td class="px-6 py-6">
          <h1 class="text-2xl font-bold text-gray-900 m-0">
            Bonjour {{ name }} !
          </h1>
        </td>
      </tr>
    </table>
  </block>
</extends>
```

**Comparaison React Email vs Maizzle :**

| Critère | React Email | Maizzle |
|---------|------------|---------|
| Langage | TypeScript/JSX | HTML + Tailwind |
| Composants | Réutilisables (React) | Includes PostHTML |
| Compatibilité | Inline styles auto | Transformers configurables |
| Intégration serveur | Natif Node.js/Next.js | Build séparé |
| Courbe d'apprentissage | Faible (si React connu) | Faible (HTML) |
| Dark mode | Manuelle | Helpers intégrés |

---

## Tests Litmus

Litmus permet de capturer des screenshots d'emails dans 90+ clients et environnements.

```typescript
// Intégration Litmus dans le pipeline CI (via API)
import { LitmusClient } from '@litmus/api-client';

const litmus = new LitmusClient({ apiKey: process.env.LITMUS_API_KEY });

async function testerCompatibilitéEmail(htmlEmail: string): Promise<void> {
  // Lancer les tests dans les clients les plus importants
  const résultat = await litmus.emails.test({
    html: htmlEmail,
    clients: [
      'gmailnew',       // Gmail Web
      'iphone14',       // Apple Mail iOS 16
      'appmail14',      // Apple Mail macOS
      'ol2021',         // Outlook 2021
      'yahoo_new',      // Yahoo Mail Web
      'android_gmail',  // Gmail Android
    ],
  });

  // Générer un rapport
  const rapport = await litmus.emails.getReport(résultat.id);
  console.log(`Tests terminés : ${rapport.summary.passes}/${rapport.summary.total} passés`);

  // Télécharger les screenshots
  for (const client of rapport.clients) {
    if (client.status === 'fail') {
      console.error(`Problème détecté dans ${client.name} : ${client.notes}`);
    }
  }
}
```

**Alternatives à Litmus :**
- **Email on Acid** — prix similaire, moins de clients testés
- **Testi@** — moins cher, focus screenshots
- **Mailjet Previewer** — gratuit mais limité
- **GlockApps** — spécialisé délivrabilité + inbox testing (spam checker)
