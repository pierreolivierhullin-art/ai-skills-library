# ICU Message Format — Pluralisation, Genre Grammatical et Formats Complexes

## Overview

Référence complète sur ICU Message Format pour l'internationalisation avancée. Couvre la syntaxe officielle, la pluralisation par règles CLDR, les ordinaux, le select pour le genre grammatical, les messages imbriqués, i18next-icu, Mozilla Project Fluent et la gestion des langues à morphologie complexe. Appliquer ces patterns pour des traductions correctes dans toutes les langues supportées.

---

## ICU Message Format — Syntaxe Officielle

### Principes fondamentaux

ICU Message Format est la norme internationale pour les messages localisés complexes. Il gère nativement la pluralisation, le genre grammatical, les listes formatées et l'imbrication de ces mécanismes.

```
Syntaxe de base :
{variable}                           — Interpolation simple
{variable, type}                     — Formatage par type
{variable, type, style}              — Formatage avec style personnalisé
{variable, plural, règles}           — Pluralisation
{variable, select, options}          — Sélection conditionnelle (genre, statut)
{variable, selectordinal, règles}    — Nombres ordinaux (1er, 2e, 3e)
```

```json
// Exemples de syntaxe ICU dans les messages
{
  "exemples": {
    "interpolation": "Bonjour, {prenom} {nom} !",
    "date": "Publié le {date, date, long}",
    "nombre": "Total : {montant, number, ::currency/EUR}",
    "plural": "{count, plural, =0 {Aucun article} =1 {1 article} other {# articles}}",
    "select": "{genre, select, masculin {Bienvenu} feminin {Bienvenue} other {Bienvenu(e)}}",
    "ordinal": "{rang, selectordinal, =1 {#er} other {#e}} rang"
  }
}
```

### Syntaxe number skeleton (moderne)

La syntaxe `::` permet des formats de nombres précis et portables, recommandée par rapport aux styles hérités.

```json
{
  "prix": {
    "eur": "Prix : {montant, number, ::currency/EUR}",
    "usd": "Price: {amount, number, ::currency/USD .00}",
    "compact": "Volume : {valeur, number, ::compact-short}",
    "pourcentage": "Taux : {taux, number, ::percent .0}",
    "precision": "Mesure : {valeur, number, ::. @@@}"
  }
}
```

---

## Pluralisation par Règles CLDR

### Classes plurielles par langue

CLDR (Common Locale Data Repository) définit des règles de pluralisation pour chaque langue. Chaque langue appartient à un groupe de règles spécifique.

| Classe | Signification | Exemples de langues |
|---|---|---|
| `zero` | Quantité nulle | Arabe, gallois |
| `one` | Singulier | Français, anglais, espagnol |
| `two` | Duel | Arabe, gallois, slovène |
| `few` | Petit nombre | Russe, polonais, tchèque, arabe |
| `many` | Grand nombre | Polonais, russe, arabe |
| `other` | Défaut (toutes les autres valeurs) | Toutes les langues |

### Règles par langue — tableau des principales

```
Anglais (en) — 2 formes :
  one  : n = 1
  other: tout le reste
  Exemple : "1 item" / "0 items" / "2 items"

Français (fr) — 2 formes :
  one  : n = 0 ou 1  (le zéro est singulier en français !)
  other: tout le reste
  Exemple : "0 article" / "1 article" / "2 articles"

Arabe (ar) — 6 formes :
  zero : n = 0
  one  : n = 1
  two  : n = 2
  few  : n = 3..10
  many : n = 11..99
  other: décimaux et tout le reste
  Exemple : "٠ كتب" / "كتاب" / "كتابان" / "٣ كتب" / "١١ كتابًا"

Russe (ru) — 3 formes :
  one  : n % 10 = 1 AND n % 100 ≠ 11  (1, 21, 31, 41...)
  few  : n % 10 = 2..4 AND n % 100 ≠ 12..14  (2,3,4 / 22,23,24...)
  many : tout le reste (0, 5..20, 25..30...)
  Exemple : "1 файл" / "2 файла" / "5 файлов"

Polonais (pl) — 4 formes :
  one  : n = 1
  few  : n % 10 = 2..4 AND n % 100 ≠ 12..14
  many : n % 10 = 0, ou n % 10 = 5..9, ou n % 100 = 11..14
  other: décimaux
  Exemple : "1 plik" / "2 pliki" / "5 plików"

Japonais (ja), Chinois (zh), Turc (tr) — 1 seule forme :
  other: toutes les quantités
  Exemple : "0個" / "1個" / "100個" (même forme, le nombre change)
```

### Implémentation correcte en JSON

```json
// messages/fr.json — Pluralisation française correcte
{
  "fichiers": {
    "nombre": "{count, plural,\n  =0 {Aucun fichier}\n  =1 {1 fichier}\n  other {# fichiers}\n}",
    "selection": "{count, plural,\n  =0 {Aucun fichier sélectionné}\n  =1 {1 fichier sélectionné}\n  other {# fichiers sélectionnés}\n}",
    "partage": "{count, plural,\n  =1 {{nom} a partagé 1 fichier avec vous}\n  other {{nom} a partagé # fichiers avec vous}\n}"
  },
  "notifications": {
    "nouvelles": "{count, plural,\n  =0 {Aucune notification}\n  =1 {1 nouvelle notification}\n  other {# nouvelles notifications}\n}"
  }
}
```

```json
// messages/ar.json — Pluralisation arabe (6 formes)
{
  "fichiers": {
    "nombre": "{count, plural,\n  =0 {لا ملفات}\n  =1 {ملف واحد}\n  =2 {ملفان}\n  few {# ملفات}\n  many {# ملفًا}\n  other {# ملف}\n}"
  }
}
```

```json
// messages/ru.json — Pluralisation russe (3 formes)
{
  "fichiers": {
    "nombre": "{count, plural,\n  one {# файл}\n  few {# файла}\n  many {# файлов}\n  other {# файла}\n}"
  }
}
```

---

## Ordinaux — Nombres de Rang

### Syntaxe selectordinal

```json
// messages/fr.json — Ordinaux français
{
  "classement": {
    "position": "Vous êtes {rang, selectordinal,\n  =1 {#er}\n  other {#e}\n}",
    "etape": "Étape {num, selectordinal,\n  =1 {#re}\n  other {#e}\n} sur {total}"
  }
}
```

```json
// messages/en.json — Ordinaux anglais (plus complexes)
{
  "classement": {
    "position": "You are {rank, selectordinal,\n  one {#st}\n  two {#nd}\n  few {#rd}\n  other {#th}\n}",
    "exemples": "1st / 2nd / 3rd / 4th / 11th / 21st / 22nd / 23rd / 24th"
  }
}
```

```json
// messages/ru.json — Ordinaux russes
{
  "classement": {
    "position": "{rank, selectordinal,\n  other {#-е}\n} место"
  }
}
```

### Différences clés FR/EN/RU pour les ordinaux

| Nombre | Français | Anglais | Russe |
|---|---|---|---|
| 1 | 1er / 1re | 1st | 1-е |
| 2 | 2e | 2nd | 2-е |
| 3 | 3e | 3rd | 3-е |
| 11 | 11e | 11th (pas 11st!) | 11-е |
| 21 | 21e | 21st | 21-е |
| 22 | 22e | 22nd | 22-е |

---

## Select — Genre Grammatical et Sélection Conditionnelle

### Genre grammatical en français

```json
// messages/fr.json — Genre grammatical
{
  "invitation": {
    "acceptation": "{genre, select,\n  masculin {Il a accepté votre invitation}\n  feminin {Elle a accepté votre invitation}\n  other {La personne a accepté votre invitation}\n}",
    "bienvenue": "Bienvenu{genre, select, feminin {e} other {}} dans l'équipe, {prenom} !",
    "premier": "{genre, select,\n  masculin {{prenom} est le premier à rejoindre}\n  feminin {{prenom} est la première à rejoindre}\n  other {{prenom} est la première personne à rejoindre}\n}"
  },
  "profil": {
    "titre": "{titre, select,\n  M {M.}\n  Mme {Mme}\n  Dr {Dr}\n  Pr {Pr}\n  other {}\n} {nom}"
  }
}
```

### Statuts et états — select pour les valeurs métier

```json
// messages/fr.json — Select pour les statuts
{
  "commande": {
    "statut": "{statut, select,\n  en-attente {En attente de paiement}\n  confirmee {Commande confirmée}\n  en-preparation {En cours de préparation}\n  expediee {Expédiée}\n  livree {Livrée}\n  annulee {Annulée}\n  remboursee {Remboursée}\n  other {Statut inconnu}\n}",
    "action": "{statut, select,\n  en-attente {Payer maintenant}\n  confirmee {Suivre ma commande}\n  expediee {Suivre la livraison}\n  livree {Laisser un avis}\n  other {Contacter le support}\n}"
  }
}
```

---

## Messages Imbriqués — Plurals dans Select et Vice-Versa

### Plurals imbriqués dans select

```json
// messages/fr.json — Genre ET pluriel combinés
{
  "equipe": {
    "membres": "{genre, select,\n  masculin {{count, plural,\n    =0 {Aucun homme dans l'équipe}\n    =1 {1 homme dans l'équipe}\n    other {# hommes dans l'équipe}\n  }}\n  feminin {{count, plural,\n    =0 {Aucune femme dans l'équipe}\n    =1 {1 femme dans l'équipe}\n    other {# femmes dans l'équipe}\n  }}\n  other {{count, plural,\n    =0 {Aucun membre dans l'équipe}\n    =1 {1 membre dans l'équipe}\n    other {# membres dans l'équipe}\n  }}\n}"
  }
}
```

### Dates dans les plurals

```json
// messages/fr.json — Dates combinées avec plurals
{
  "evenement": {
    "duree": "{jours, plural,\n  =0 {Aujourd'hui, {date, date, short}}\n  =1 {Demain, {date, date, short}}\n  other {Dans # jours ({date, date, short})}\n}",
    "anciennete": "{mois, plural,\n  =1 {Ce projet a 1 mois}\n  other {Ce projet a # mois — créé le {dateCreation, date, long}}\n}"
  }
}
```

---

## i18next-icu — ICU Format dans i18next

### Configuration i18next avec le plugin ICU

```typescript
// src/i18n/config.ts — i18next avec ICU message format
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import ICU from 'i18next-icu';

i18n
  .use(ICU)                // Plugin ICU — doit être ajouté avant initReactI18next
  .use(initReactI18next)
  .init({
    resources: {
      fr: {
        translation: {
          'fichiers.nombre': `{count, plural,
            =0 {Aucun fichier}
            =1 {1 fichier}
            other {# fichiers}
          }`,
          'invitation.acceptation': `{genre, select,
            masculin {Il a accepté}
            feminin {Elle a accepté}
            other {Accepté}
          }`,
        },
      },
      en: {
        translation: {
          'fichiers.nombre': `{count, plural,
            one {# file}
            other {# files}
          }`,
        },
      },
    },
    fallbackLng: 'fr',
    interpolation: {
      escapeValue: false,
    },
  });
```

```typescript
// Utilisation dans les composants React
import { useTranslation } from 'react-i18next';

function CompteurFichiers({ count }: { count: number }) {
  const { t } = useTranslation();

  // ICU parse le format automatiquement — pas besoin de logique manuelle
  return <span>{t('fichiers.nombre', { count })}</span>;
}

function MessageAcceptation({ genre }: { genre: 'masculin' | 'feminin' | 'autre' }) {
  const { t } = useTranslation();

  return <p>{t('invitation.acceptation', { genre })}</p>;
}
```

---

## Mozilla Project Fluent — Syntaxe et Avantages

### Syntaxe Fluent

Fluent est une alternative à ICU développée par Mozilla. Sa syntaxe est plus expressive pour les langues à morphologie complexe (finnois, hongrois, turc).

```ftl
# messages/fr.ftl — Syntaxe Fluent
bonjour = Bonjour, { $prenom } !

# Pluralisation Fluent
fichiers =
  { $count ->
    [0] Aucun fichier
    [1] 1 fichier
   *[other] { $count } fichiers
  }

# Select / genre grammatical
bienvenue =
  { $genre ->
    [feminin] Bienvenue, { $prenom } !
   *[other] Bienvenu, { $prenom } !
  }

# Attributs — métadonnées pour un même message
bouton-supprimer =
  .label = Supprimer
  .title = Supprimer ce fichier (irréversible)
  .aria-label = Supprimer le fichier { $nom }

# Termes réutilisables
-nom-app = MonApplication

titre-fenetre = { -nom-app } — Paramètres
```

### Avantages de Fluent pour les langues agglutinantes

```ftl
# Finnois (fi) — langue agglutinante, les déclinaisons changent le suffixe
# "dans le fichier" = "tiedostossa" (locatif), "du fichier" = "tiedostosta" (élative)

fichier-reference =
  { $cas ->
    [locatif] tiedostossa
    [elatif] tiedostosta
    [allatif] tiedostoon
   *[nominatif] tiedosto
  }
```

### Fluent vs ICU — tableau comparatif

| Critère | ICU Message Format | Mozilla Fluent |
|---|---|---|
| **Standardisation** | ISO standard (CLDR) | Standard Mozilla |
| **Syntaxe** | Concise, dans le message | Fichier .ftl séparé |
| **Langues complexes** | Limitée (6 classes plural) | Expressive (cas grammaticaux) |
| **Attributs (aria, title)** | Non | Oui (attributs natifs) |
| **Termes réutilisables** | Non | Oui (-terme) |
| **Support bibliothèques** | Universel (i18next, next-intl) | Limité (fluent.js, Project Fluent) |
| **Quand utiliser** | Applications standard | Langues à morphologie complexe, produits Mozilla |

---

## Variables Complexes — Listes et Conjonctions

### Intl.ListFormat — Listes formatées

```typescript
// Formater des listes avec la conjonction correcte selon la locale
function formaterListe(items: string[], locale: string, type: 'conjunction' | 'disjunction' = 'conjunction'): string {
  const formatteur = new Intl.ListFormat(locale, {
    style: 'long',   // 'long' | 'short' | 'narrow'
    type,            // 'conjunction' (et) | 'disjunction' (ou) | 'unit'
  });
  return formatteur.format(items);
}

// Résultats par locale :
// fr, conjunction : "Alice, Bob et Charlie"
// en, conjunction : "Alice, Bob, and Charlie"  (Oxford comma!)
// fr, disjunction : "Alice, Bob ou Charlie"
// en, disjunction : "Alice, Bob, or Charlie"
// de, conjunction : "Alice, Bob und Charlie"
// ar, conjunction : "Alice وBob وCharlie"
```

```json
// Intégrer Intl.ListFormat dans les messages ICU
// Pré-formater la liste avant de l'injecter dans le message
{
  "partage": {
    "avec": "Partagé avec {liste}",
    "modifie-par": "Modifié par {auteurs}"
  }
}
```

```typescript
// Utilisation combinée — liste + message ICU
import { useTranslations, useFormatter } from 'next-intl';

function InfoPartage({ collaborateurs }: { collaborateurs: string[] }) {
  const t = useTranslations('partage');
  const format = useFormatter();

  // Formater la liste avec Intl.ListFormat via next-intl
  const listeFormatee = format.list(collaborateurs, { type: 'conjunction' });

  return <p>{t('avec', { liste: listeFormatee })}</p>;
}
```

---

## Tests Automatiques des Traductions

### Vérifier les variables non utilisées et clés manquantes

```typescript
// scripts/valider-traductions.ts
import fr from '../messages/fr.json';
import en from '../messages/en.json';
import es from '../messages/es.json';
import ar from '../messages/ar.json';

const locales = { fr, en, es, ar };
const localeReference = 'fr';

// Aplatir les clés imbriquées en notation pointée
function aplatirCles(obj: object, prefixe = ''): Record<string, string> {
  return Object.entries(obj).reduce((acc, [cle, valeur]) => {
    const cleComplete = prefixe ? `${prefixe}.${cle}` : cle;
    if (typeof valeur === 'object' && valeur !== null) {
      Object.assign(acc, aplatirCles(valeur, cleComplete));
    } else {
      acc[cleComplete] = valeur as string;
    }
    return acc;
  }, {} as Record<string, string>);
}

// Extraire les variables ICU d'un message
function extraireVariablesICU(message: string): Set<string> {
  const variables = new Set<string>();
  const regex = /\{(\w+)(?:,\s*\w+(?:,\s*[^}]+)?)?\}/g;
  let match;
  while ((match = regex.exec(message)) !== null) {
    variables.add(match[1]);
  }
  return variables;
}

function validerTraductions() {
  const clesFR = aplatirCles(fr);
  let erreursTotal = 0;

  // Pour chaque locale, vérifier les clés manquantes
  for (const [locale, messages] of Object.entries(locales)) {
    if (locale === localeReference) continue;

    const clesLocale = aplatirCles(messages);
    const clesFRSet = new Set(Object.keys(clesFR));
    const clesLocaleSet = new Set(Object.keys(clesLocale));

    // Clés présentes en FR mais absentes dans cette locale
    const cleManquantes = [...clesFRSet].filter((c) => !clesLocaleSet.has(c));
    if (cleManquantes.length > 0) {
      console.error(`❌ [${locale}] ${cleManquantes.length} clés manquantes :`);
      cleManquantes.forEach((c) => console.error(`   - ${c}`));
      erreursTotal += cleManquantes.length;
    }

    // Vérifier la cohérence des variables ICU
    for (const [cle, messageRef] of Object.entries(clesFR)) {
      const messageLocale = clesLocale[cle];
      if (!messageLocale) continue;

      const variablesRef = extraireVariablesICU(messageRef);
      const variablesLocale = extraireVariablesICU(messageLocale);

      // Variables présentes en FR mais absentes dans la traduction
      for (const variable of variablesRef) {
        if (!variablesLocale.has(variable)) {
          console.error(`❌ [${locale}] Variable manquante dans "${cle}" : {${variable}}`);
          erreursTotal++;
        }
      }
    }
  }

  if (erreursTotal === 0) {
    console.log('✅ Toutes les traductions sont valides');
  } else {
    console.error(`\n❌ ${erreursTotal} erreur(s) de traduction détectée(s)`);
    process.exit(1);
  }
}

validerTraductions();
```

### Intégrer la validation dans la CI

```yaml
# .github/workflows/i18n-validation.yml
name: Validation des traductions

on: [push, pull_request]

jobs:
  valider-traductions:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - name: Valider les clés et variables ICU
        run: npx ts-node scripts/valider-traductions.ts
      - name: Vérifier la couverture de traduction
        run: npx ts-node scripts/couverture-traductions.ts --seuil 98
```

### Test de parsing ICU — détecter les messages malformés

```typescript
// scripts/tester-icu.ts
import { parse } from '@formatjs/icu-messageformat-parser';

function testerMessagesICU(messages: Record<string, string>): void {
  let erreurs = 0;

  for (const [cle, message] of Object.entries(messages)) {
    try {
      parse(message, { captureLocation: true });
    } catch (err) {
      console.error(`❌ Message ICU invalide : "${cle}"`);
      console.error(`   Message : ${message}`);
      console.error(`   Erreur  : ${(err as Error).message}`);
      erreurs++;
    }
  }

  if (erreurs === 0) {
    console.log(`✅ ${Object.keys(messages).length} messages ICU valides`);
  } else {
    process.exit(1);
  }
}
```

---

## Gestion des Langues à Morphologie Complexe

### Arabe — Double (dual) et cas grammaticaux

L'arabe est la seule langue avec 6 classes plurielles CLDR et un duel natif.

```json
// messages/ar.json — Pluralisation arabe complète
{
  "resultat": {
    "recherche": "{count, plural,\n  =0 {لا توجد نتائج}\n  =1 {نتيجة واحدة}\n  =2 {نتيجتان}\n  few {# نتائج}\n  many {# نتيجةً}\n  other {# نتيجة}\n}"
  }
}
```

### Russe — Cas grammaticaux dans les traductions

Le russe a 6 cas grammaticaux. Les outils ICU gèrent cela via `select` sur le cas.

```json
// messages/ru.json — Cas grammaticaux avec select
{
  "profil": {
    "statut": "{cas, select,\n  nominatif {Пользователь}\n  genitif {пользователя}\n  datif {пользователю}\n  accusatif {пользователя}\n  instrumental {пользователем}\n  prepositif {пользователе}\n  other {пользователь}\n}"
  }
}
```

### Polonais — Complexité plurielle unique

Le polonais a 4 classes plurielles avec des règles arithmétiques complexes.

```json
// messages/pl.json — Pluralisation polonaise
{
  "pliki": "{count, plural,\n  =1 {# plik}\n  few {# pliki}\n  many {# plików}\n  other {# pliku}\n}"
}
```

```
Règle polonaise détaillée :
  one  : count = 1                           → "1 plik"
  few  : count % 10 ∈ {2,3,4} ET            → "2 pliki" / "22 pliki"
         count % 100 ∉ {12,13,14}
  many : count % 10 ∈ {0,5..9} OU           → "5 plików" / "11 plików"
         count % 100 ∈ {11..14}
  other: décimaux                             → "1,5 pliku"
```
