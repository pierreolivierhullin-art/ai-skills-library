# Critères WCAG 2.1/2.2 AA — Guide de Conformité

## Overview

Référence exhaustive des critères WCAG 2.1 et 2.2 au niveau AA, avec implémentation pratique pour chaque critère. Les WCAG (Web Content Accessibility Guidelines) définissent le standard international d'accessibilité numérique, repris en France par le RGAA (Référentiel Général d'Amélioration de l'Accessibilité). Chaque critère est accompagné de son code de référence, de son niveau (A/AA/AAA) et d'exemples concrets d'implémentation.

---

## Principe 1 — Perceptible

Toute information et composant de l'interface utilisateur doit être présentable aux utilisateurs de manière à ce qu'ils puissent le percevoir.

### 1.1 — Alternatives Textuelles

**Critère 1.1.1 (A)** — Tout contenu non textuel doit avoir une alternative textuelle.

Règles par type d'image :

**Images informatives** — l'alt décrit l'information véhiculée, pas l'aspect visuel :
```html
<!-- ❌ Description visuelle inutile -->
<img src="warning.svg" alt="Triangle jaune avec point d'exclamation">

<!-- ✅ Information véhiculée -->
<img src="warning.svg" alt="Avertissement : votre session expire dans 5 minutes">

<!-- ❌ Alt redondant avec le texte adjacent -->
<img src="logo-apple.png" alt="Logo Apple">
<span>Apple</span>

<!-- ✅ Alt vide quand le texte adjacent suffit -->
<img src="logo-apple.png" alt="">
<span>Apple</span>
```

**Images décoratives** — alt vide, jamais supprimé :
```html
<!-- ✅ Image purement décorative -->
<img src="divider.svg" alt="" role="presentation">

<!-- ❌ Alt absent (le lecteur d'écran lit le nom du fichier) -->
<img src="decorative-wave-bg.png">
```

**Images fonctionnelles** (boutons, liens) — l'alt décrit l'action, pas l'image :
```html
<!-- ✅ Bouton-image : alt = action déclenchée -->
<input type="image" src="search.png" alt="Lancer la recherche">

<!-- ✅ Lien-image : alt = destination -->
<a href="/accueil">
  <img src="logo.png" alt="Page d'accueil MonApp">
</a>
```

**Images complexes** (graphiques, infographies) :
```html
<!-- ✅ Graphique avec alt court + description longue accessible -->
<figure>
  <img
    src="evolution-ca.png"
    alt="Graphique d'évolution du CA 2022–2024"
    aria-describedby="desc-graphique"
  >
  <figcaption id="desc-graphique">
    Le chiffre d'affaires a progressé de 2,1M€ en 2022 à 3,8M€ en 2024,
    soit une croissance de 81%. Pic à 4,1M€ au T3 2023.
  </figcaption>
</figure>
```

**CAPTCHA** — toujours fournir une alternative :
```html
<!-- ✅ CAPTCHA avec alternative audio -->
<div role="group" aria-labelledby="captcha-label">
  <p id="captcha-label">Vérification de sécurité</p>
  <img src="captcha.png" alt="Code de vérification visuel">
  <a href="/captcha-audio">Alternative audio pour malvoyants</a>
</div>
```

---

### 1.2 — Médias Temporels

**Critère 1.2.1 (A)** — Les médias audio et vidéo préenregistrés doivent avoir des alternatives.

**Critère 1.2.2 (A)** — Les vidéos avec audio doivent avoir des sous-titres :
```html
<video controls>
  <source src="presentation.mp4" type="video/mp4">
  <!-- Sous-titres synchronisés en WebVTT -->
  <track
    kind="subtitles"
    src="presentation-fr.vtt"
    srclang="fr"
    label="Français"
    default
  >
  <!-- Audiodescription pour le contenu visuel non perceptible à l'audio -->
  <track
    kind="descriptions"
    src="presentation-ad.vtt"
    srclang="fr"
    label="Audiodescription"
  >
</video>
```

**Format WebVTT minimal** :
```
WEBVTT

00:00:02.000 --> 00:00:06.000
Bonjour et bienvenue dans cette présentation
sur l'accessibilité numérique.

00:00:07.500 --> 00:00:12.000
Nous allons couvrir les quatre principes POUR
définis par les WCAG.
```

**Critère 1.2.3 (A)** — Audiodescription ou alternative media pour vidéo préenregistrée.

**Critère 1.2.4 (AA)** — Sous-titres pour médias en direct (live streaming) — nécessite un service de sous-titrage en temps réel.

**Critère 1.2.5 (AA)** — Audiodescription pour vidéo préenregistrée.

---

### 1.3 — Adaptable

**Critère 1.3.1 (A)** — L'information et la structure doivent pouvoir être déterminées par programme.

Structure sémantique obligatoire — ne jamais utiliser la présentation visuelle pour transmettre la structure :
```html
<!-- ❌ Tableau de mise en page -->
<table>
  <tr>
    <td><b>Nom :</b></td>
    <td>Jean Dupont</td>
  </tr>
</table>

<!-- ✅ Structure sémantique -->
<dl>
  <dt>Nom</dt>
  <dd>Jean Dupont</dd>
</dl>

<!-- ❌ Liste simulée avec des divs -->
<div class="list">
  <div class="item">• Élément 1</div>
  <div class="item">• Élément 2</div>
</div>

<!-- ✅ Liste native -->
<ul>
  <li>Élément 1</li>
  <li>Élément 2</li>
</ul>
```

**Critère 1.3.2 (A)** — La séquence significative est préservée dans le DOM. L'ordre de lecture du DOM doit correspondre à l'ordre visuel logique. Eviter de réordonner visuellement via CSS sans réordonner le DOM.

**Critère 1.3.3 (A)** — Les instructions ne reposent pas uniquement sur les caractéristiques sensorielles (forme, couleur, position) :
```html
<!-- ❌ Référence visuelle uniquement -->
<p>Cliquez sur le bouton vert pour continuer.</p>
<p>Remplissez le formulaire ci-dessous.</p>

<!-- ✅ Instruction compréhensible sans visuel -->
<p>Cliquez sur le bouton "Continuer" pour passer à l'étape suivante.</p>
<p>Remplissez le formulaire "Coordonnées" pour compléter votre commande.</p>
```

**Critère 1.3.4 (AA — WCAG 2.1)** — Orientation : le contenu ne doit pas être restreint à une seule orientation (portrait ou paysage) sauf nécessité absolue :
```css
/* ❌ Bloquer l'orientation via CSS */
@media (orientation: landscape) {
  body { display: none; }
}

/* ✅ Adapter le contenu aux deux orientations */
@media (orientation: landscape) {
  .sidebar { display: none; }
  .main { width: 100%; }
}
```

**Critère 1.3.5 (AA — WCAG 2.1)** — Identifier le but des champs de saisie via `autocomplete` :
```html
<!-- ✅ Attributs autocomplete standardisés -->
<input type="text" autocomplete="given-name" name="prenom">
<input type="text" autocomplete="family-name" name="nom">
<input type="email" autocomplete="email" name="email">
<input type="tel" autocomplete="tel" name="telephone">
<input type="text" autocomplete="street-address" name="adresse">
<input type="text" autocomplete="postal-code" name="codepostal">
<input type="password" autocomplete="current-password" name="mdp">
<input type="text" autocomplete="one-time-code" name="otp">
```

---

### 1.4 — Distinguable

**Critère 1.4.1 (A)** — La couleur n'est pas utilisée comme seul moyen de transmettre l'information :
```html
<!-- ❌ Couleur seule pour l'état du champ -->
<input class="champ-invalide" style="border-color: red">

<!-- ✅ Couleur + icône + texte -->
<div class="champ-wrapper">
  <input aria-invalid="true" aria-describedby="msg-erreur" class="champ-invalide">
  <p id="msg-erreur" class="erreur">
    <svg aria-hidden="true"><use href="#icon-alert"/></svg>
    Ce champ est obligatoire
  </p>
</div>
```

**Critère 1.4.2 (A)** — Contrôle audio : tout audio démarrant automatiquement doit pouvoir être mis en pause.

**Critère 1.4.3 (AA)** — Contraste minimum texte normal : ratio 4,5:1 :
```css
/* Palette accessible — exemples de combinaisons conformes */

/* Texte foncé sur fond clair */
.texte-principal { color: #1a1a2e; background: #ffffff; } /* ratio : 17,5:1 */
.texte-secondaire { color: #4a5568; background: #ffffff; } /* ratio : 7,4:1 */

/* Texte clair sur fond sombre */
.badge-danger { color: #ffffff; background: #c53030; } /* ratio : 6,1:1 */
.badge-info { color: #1a202c; background: #bee3f8; }    /* ratio : 9,2:1 */

/* ❌ Combinaisons non conformes AA */
.gris-moyen { color: #a0aec0; background: #ffffff; }    /* ratio : 2,9:1 */
.jaune-texte { color: #f6e05e; background: #ffffff; }   /* ratio : 1,6:1 */
```

**Critère 1.4.4 (AA)** — Redimensionnement du texte jusqu'à 200% sans perte de contenu ni fonctionnalité :
```css
/* ✅ Unités relatives — respectent les préférences utilisateur */
html { font-size: 100%; }          /* = préférence navigateur (généralement 16px) */
body { font-size: 1rem; }          /* évolue avec les préférences */
h1 { font-size: 2rem; }            /* = 32px si base = 16px */
.nav-link { padding: 0.75em 1em; } /* em : relatif au font-size local */

/* ❌ Unités fixes — bloquent le redimensionnement */
body { font-size: 14px; }
h1 { font-size: 32px; }
.container { height: 400px; }      /* hauteur fixe + overflow: hidden = perte de contenu */
```

**Critère 1.4.5 (AA)** — Les images de texte sont évitées en faveur du texte réel (sauf logos).

**Critère 1.4.10 (AA — WCAG 2.1)** — Reflow : le contenu doit pouvoir être affiché en colonne unique sans scroll horizontal à 320px de large (équivalent 400% de zoom sur écran 1280px) :
```css
/* ✅ Layout responsive qui reflow à 320px */
.container {
  max-width: 1200px;
  width: 100%;
  padding: 0 1rem;
}

/* Éviter les overflow cachés et les largeurs fixes */
.card {
  min-width: 0;          /* Permet le shrink dans flexbox */
  overflow-wrap: break-word;
}

/* Tableaux : permettre le scroll horizontal sur le wrapper, pas sur body */
.table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
table { min-width: 600px; }

/* Tester avec : zoom navigateur 400% sur 1280px de large */
```

**Critère 1.4.11 (AA — WCAG 2.1)** — Contraste des composants d'interface non textuels : ratio 3:1 entre les composants UI et leur environnement :
```css
/* ✅ Bordure d'input visible en contraste 3:1 */
input {
  border: 2px solid #767676; /* ratio 4,6:1 sur fond blanc — conforme */
}

/* ✅ Focus indicator contraste 3:1 */
:focus-visible {
  outline: 3px solid #005fcc; /* ratio 5,9:1 sur fond blanc — conforme */
  outline-offset: 2px;
}

/* ❌ Bordure trop claire */
input {
  border: 1px solid #cccccc; /* ratio 1,6:1 — non conforme */
}
```

**Critère 1.4.12 (AA — WCAG 2.1)** — Espacement du texte : le contenu ne doit pas perdre d'information quand les styles suivants sont appliqués :
```css
/* Styles de test — appliquer via bookmarklet ou DevTools */
* {
  line-height: 1.5 !important;              /* Hauteur de ligne ≥ 1.5× font-size */
  letter-spacing: 0.12em !important;         /* Espacement lettres ≥ 0.12× font-size */
  word-spacing: 0.16em !important;           /* Espacement mots ≥ 0.16× font-size */
}

p { margin-bottom: 2em !important; }        /* Espacement après paragraphe ≥ 2× font-size */

/* ✅ Hauteurs de ligne relatives et flexibles */
.text-container {
  line-height: 1.5;
  overflow: visible;  /* Jamais overflow: hidden sur du texte */
}
```

**Critère 1.4.13 (AA — WCAG 2.1)** — Contenu au survol ou au focus : les popups/tooltips apparaissant au hover/focus doivent être ignorables (Échap), hoverables (la souris peut aller dessus sans fermeture), et persistants (restent visibles tant que le focus est maintenu).

---

## Principe 2 — Opérable

### 2.1 — Accessible au Clavier

**Critère 2.1.1 (A)** — Toutes les fonctionnalités sont accessibles au clavier :
```typescript
// ❌ Gestionnaire souris uniquement
div.addEventListener('click', handleAction);

// ✅ Clavier + souris
div.setAttribute('tabindex', '0');
div.addEventListener('click', handleAction);
div.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    handleAction();
  }
});

// ✅ Mieux : utiliser un élément natif
// <button> gère click + Enter + Space nativement
const button = document.createElement('button');
button.addEventListener('click', handleAction);
```

**Critère 2.1.2 (A)** — Pas de piège au clavier : le focus doit pouvoir entrer ET sortir de chaque composant via le clavier. Exception légitime : les modales (piège intentionnel avec Échap pour sortir).

**Critère 2.1.4 (A — WCAG 2.1)** — Raccourcis clavier à caractère unique : permettre de les désactiver ou remapper.

---

### 2.2 — Délai Suffisant

**Critère 2.2.1 (A)** — Délai ajustable : tout délai peut être désactivé, ajusté (10× minimum) ou prolongé via avertissement :
```typescript
// Avertissement de session avec délai ajustable
function SessionWarning({ minutesLeft, onExtend, onLogout }: Props) {
  return (
    <div role="alertdialog" aria-labelledby="session-titre" aria-modal="true">
      <h2 id="session-titre">Session expire bientôt</h2>
      <p>Votre session expire dans {minutesLeft} minute(s).</p>
      <button onClick={onExtend}>Prolonger ma session (20 minutes)</button>
      <button onClick={onLogout}>Me déconnecter</button>
    </div>
  );
}
```

**Critère 2.2.2 (A)** — Pause, stop, masquer : tout contenu en mouvement démarrant automatiquement pendant plus de 5 secondes doit pouvoir être mis en pause :
```html
<!-- ✅ Carrousel avec bouton pause -->
<div class="carrousel" aria-roledescription="carrousel" aria-label="Promotions du moment">
  <div class="carrousel-contenu" aria-live="off">
    <!-- Slides -->
  </div>
  <button
    aria-label="Mettre en pause la rotation automatique"
    class="pause-btn"
    id="carrousel-pause"
  >
    ⏸ Pause
  </button>
</div>
```

---

### 2.3 — Convulsions

**Critère 2.3.1 (A)** — Pas plus de 3 flashs par seconde. Tester avec le PEAT (Photosensitive Epilepsy Analysis Tool) pour les animations intensives.

```css
/* ✅ Respecter prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* ✅ Animations conditionnelles en JS */
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

if (!prefersReducedMotion) {
  // Lancer l'animation
}
```

---

### 2.4 — Navigable

**Critère 2.4.1 (A)** — Contournement des blocs : un mécanisme de saut doit permettre d'aller au contenu principal :
```html
<!-- Premier élément de la page — visible seulement au focus -->
<a href="#main-content" class="skip-link">Aller au contenu principal</a>
<a href="#search" class="skip-link">Aller à la recherche</a>
<a href="#nav-principale" class="skip-link">Aller à la navigation</a>

<nav id="nav-principale"><!-- ... --></nav>

<main id="main-content" tabindex="-1">
  <!-- tabindex="-1" permet le focus programmatique sans apparaître dans l'ordre Tab -->
</main>
```
```css
.skip-link {
  position: absolute;
  left: 1rem;
  top: -100vh;
  background: #000;
  color: #fff;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  font-weight: bold;
  z-index: 10000;
  border-radius: 0 0 4px 4px;
}
.skip-link:focus {
  top: 0;
}
```

**Critère 2.4.2 (A)** — Page titrée : chaque page a un titre HTML descriptif et unique :
```html
<!-- ✅ Titres descriptifs avec structure : Page — Section — Site -->
<title>Modifier mon profil — Paramètres — MonApp</title>
<title>Récapitulatif de commande #12345 — MonShop</title>
<title>Erreur 404 — Page introuvable — MonSite</title>

<!-- ❌ Titres génériques ou identiques sur toutes les pages -->
<title>MonApp</title>
<title>Page</title>
```

**Critère 2.4.3 (A)** — Ordre du focus : l'ordre de tabulation est logique et correspond au flux de lecture. Eviter les `tabindex` positifs (`tabindex="1"`, `tabindex="2"`) qui cassent l'ordre naturel.

**Critère 2.4.4 (A)** — Objectif du lien (dans son contexte) : le libellé d'un lien doit être compréhensible dans son contexte immédiat :
```html
<!-- ❌ Liens non descriptifs hors contexte -->
<a href="/article/1">Lire la suite</a>
<a href="/article/2">Lire la suite</a>
<a href="/article/3">Lire la suite</a>

<!-- ✅ Libellés uniques et descriptifs -->
<a href="/article/1">Lire l'article : Introduction au WCAG</a>

<!-- ✅ Texte visible court + complément pour SR -->
<a href="/article/1">
  Lire la suite
  <span class="sr-only"> de l'article "Introduction au WCAG"</span>
</a>

<!-- ✅ aria-label pour différencier les liens identiques -->
<a href="/article/1" aria-label="Lire la suite : Introduction au WCAG">
  Lire la suite
</a>
```

**Critère 2.4.5 (AA)** — Plusieurs façons d'accéder au contenu : au moins deux méthodes de navigation (menu, recherche, plan du site, liens entre pages).

**Critère 2.4.6 (AA)** — En-têtes et étiquettes descriptifs : les titres et labels de champs décrivent leur sujet.

**Critère 2.4.7 (AA)** — Focus visible : tout élément interactif doit avoir un indicateur de focus visible :
```css
/* ✅ Focus visible robuste — ne jamais supprimer sans remplacer */
:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 3px;
}

/* Personnaliser par composant si nécessaire */
.btn-primary:focus-visible {
  outline: 3px solid #ffffff;
  outline-offset: 2px;
  box-shadow: 0 0 0 5px #005fcc;
}

/* ❌ À ne jamais faire */
* { outline: none; }
*:focus { outline: 0; }
button:focus { outline: none; }
```

**Critère 2.4.11 (AA — WCAG 2.2)** — Focus non masqué : l'élément qui reçoit le focus n'est pas entièrement masqué par d'autres contenus (headers sticky, bandeaux cookies).

**Critère 2.4.12 (AA — WCAG 2.2)** — Focus non masqué (amélioré) : aucune partie de l'indicateur de focus n'est masquée.

**Critère 2.4.13 (AAA — WCAG 2.2)** — Apparence du focus : critère AAA définissant un minimum de contraste et de taille pour l'indicateur de focus.

---

### 2.5 — Modalités de Saisie (WCAG 2.1)

**Critère 2.5.1 (A)** — Gestes avec le pointeur : toute fonctionnalité nécessitant un geste complexe (swipe, pinch) doit avoir une alternative à pointeur simple :
```typescript
// ✅ Slider avec geste et alternative boutons
function Slider({ value, onChange }: SliderProps) {
  return (
    <div>
      {/* Geste : drag natif HTML5 */}
      <input
        type="range"
        min={0} max={100}
        value={value}
        onChange={e => onChange(Number(e.target.value))}
        aria-label="Valeur du curseur"
      />
      {/* Alternative boutons pour gestes complexes */}
      <button onClick={() => onChange(Math.max(0, value - 10))}>-10</button>
      <button onClick={() => onChange(Math.min(100, value + 10))}>+10</button>
      <output>{value}</output>
    </div>
  );
}
```

**Critère 2.5.3 (A)** — Étiquette dans le nom : pour les composants avec label visible, le nom accessible doit contenir le texte visible :
```html
<!-- ❌ aria-label ne contient pas le texte visible "Rechercher" -->
<button aria-label="Lancer la recherche sur le site">Rechercher</button>

<!-- ✅ Le nom accessible contient le texte visible -->
<button aria-label="Rechercher sur le site">Rechercher</button>
<!-- Ou simplement : -->
<button>Rechercher</button>
```

**Critère 2.5.4 (A)** — Activation par le mouvement : les fonctionnalités déclenchées par agitation ou inclinaison doivent avoir une alternative UI et pouvoir être désactivées.

**Critère 2.5.7 (AA — WCAG 2.2)** — Mouvements de glissement (Dragging Movements) : toute action nécessitant un glissement a une alternative par pointeur simple :
```typescript
// ✅ Drag-and-drop avec alternative clavier
function DraggableList({ items, onReorder }: Props) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={item.id}>
          <span>{item.label}</span>
          {/* Alternative au drag : boutons de déplacement */}
          <button
            onClick={() => onReorder(index, index - 1)}
            disabled={index === 0}
            aria-label={`Déplacer "${item.label}" vers le haut`}
          >↑</button>
          <button
            onClick={() => onReorder(index, index + 1)}
            disabled={index === items.length - 1}
            aria-label={`Déplacer "${item.label}" vers le bas`}
          >↓</button>
        </li>
      ))}
    </ul>
  );
}
```

**Critère 2.5.8 (AA — WCAG 2.2)** — Taille de la cible (Target Size) : la taille minimale des cibles interactives est de 24×24 pixels CSS, avec un espacement qui compense si la cible est plus petite :
```css
/* ✅ Taille minimale 24×24px CSS */
.btn-icone {
  min-width: 44px;    /* Recommandé 44×44 (Apple HIG / Android Material) */
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* ✅ Petit bouton compensé par l'espacement */
.chip {
  min-width: 24px;
  min-height: 24px;
  margin: 10px; /* 10px × 2 + 24px = 44px de zone effective */
}
```

---

## Principe 3 — Compréhensible

### 3.1 — Lisible

**Critère 3.1.1 (A)** — Langue de la page définie dans le HTML :
```html
<!-- ✅ Langue principale définie sur <html> -->
<html lang="fr">

<!-- Pour les variantes régionales -->
<html lang="fr-CA">  <!-- Français canadien -->
<html lang="en-GB">  <!-- Anglais britannique -->
```

**Critère 3.1.2 (AA)** — Langue des parties : les passages dans une autre langue sont identifiés :
```html
<!-- ✅ Changements de langue inline -->
<p>
  Notre slogan : <span lang="en">"Making the web accessible for everyone"</span>.
</p>

<!-- ✅ Termes techniques internationaux (pas nécessairement à taguer) -->
<!-- Exception : noms propres, termes techniques dont la prononciation est identique -->
```

---

### 3.2 — Prévisible

**Critère 3.2.1 (A)** — Pas de changement de contexte lors du focus :
```html
<!-- ❌ Soumettre le formulaire automatiquement à la sélection d'une option -->
<select onchange="this.form.submit()">
  <option value="en">English</option>
  <option value="fr">Français</option>
</select>

<!-- ✅ Bouton de confirmation explicite -->
<form>
  <label for="langue">Langue</label>
  <select id="langue" name="langue">
    <option value="en">English</option>
    <option value="fr">Français</option>
  </select>
  <button type="submit">Appliquer</button>
</form>
```

**Critère 3.2.2 (A)** — Pas de changement de contexte lors de la saisie sans avertissement préalable.

**Critère 3.2.3 (AA)** — Navigation cohérente : les mécanismes de navigation répétés (menus, barres latérales) sont dans le même ordre relatif sur toutes les pages.

**Critère 3.2.4 (AA)** — Identification cohérente : les composants avec la même fonctionnalité sont identifiés de manière cohérente (même aria-label pour le même champ de recherche sur toutes les pages).

---

### 3.3 — Assistance à la Saisie

**Critère 3.3.1 (A)** — Identification des erreurs : les erreurs sont identifiées et décrites en texte :
```typescript
function FormulaireInscription() {
  const [erreurs, setErreurs] = useState<Record<string, string>>({});

  const valider = () => {
    const nouvErreurs: Record<string, string> = {};
    if (!valeurs.email) nouvErreurs.email = 'L\'adresse email est obligatoire';
    else if (!isEmail(valeurs.email)) nouvErreurs.email = 'Format d\'email invalide (exemple@domaine.com)';
    if (!valeurs.mdp) nouvErreurs.mdp = 'Le mot de passe est obligatoire';
    else if (valeurs.mdp.length < 8) nouvErreurs.mdp = 'Le mot de passe doit contenir au moins 8 caractères';
    return nouvErreurs;
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div>
        <label htmlFor="email">Adresse email <span aria-hidden="true">*</span></label>
        <input
          id="email"
          type="email"
          aria-required="true"
          aria-invalid={!!erreurs.email}
          aria-describedby={erreurs.email ? 'email-erreur' : undefined}
        />
        {erreurs.email && (
          <p id="email-erreur" role="alert" className="message-erreur">
            {erreurs.email}
          </p>
        )}
      </div>
    </form>
  );
}
```

**Critère 3.3.2 (A)** — Étiquettes et instructions : les champs de formulaire ont des labels et des instructions claires avant la soumission.

**Critère 3.3.3 (AA)** — Suggestion après erreur : des suggestions de correction sont fournies si possible :
```typescript
// ❌ Erreur sans suggestion
'Format invalide'

// ✅ Erreur avec suggestion
'Format d\'email invalide. Exemple attendu : prenom.nom@entreprise.fr'
'Le code postal doit contenir 5 chiffres. Exemple : 75001'
'Le numéro de téléphone doit être au format +33 6 12 34 56 78'
```

**Critère 3.3.4 (AA)** — Prévention des erreurs (juridique, financier, données) : les soumissions importantes peuvent être vérifiées, corrigées ou annulées :
```typescript
// ✅ Page de récapitulatif avant confirmation définitive
function ÉtapeConfirmation({ commande, onConfirmer, onModifier }: Props) {
  return (
    <section aria-labelledby="titre-recap">
      <h2 id="titre-recap">Récapitulatif de votre commande</h2>
      <dl>
        <dt>Produit</dt><dd>{commande.produit}</dd>
        <dt>Montant</dt><dd>{commande.montant} EUR TTC</dd>
        <dt>Adresse de livraison</dt><dd>{commande.adresse}</dd>
      </dl>
      <p>
        <strong>Action irréversible</strong> : en cliquant sur "Confirmer",
        vous validez définitivement votre commande.
      </p>
      <button onClick={onModifier}>Modifier ma commande</button>
      <button onClick={onConfirmer}>Confirmer et payer</button>
    </section>
  );
}
```

**Critère 3.3.7 (A — WCAG 2.2)** — Saisie redondante : les informations déjà saisies dans une session ne sont pas redemandées sans justification.

**Critère 3.3.8 (AA — WCAG 2.2)** — Authentification accessible : les processus d'authentification ne reposent pas sur des tâches cognitives (puzzles, mémorisation). Exception : CAPTCHA avec alternative audio.

---

## Principe 4 — Robuste

### 4.1 — Compatible

**Critère 4.1.1 (A)** — Analyse syntaxique : le HTML doit être valide (pas d'IDs dupliqués, balises fermées, imbrication correcte). Valider avec le validateur W3C : https://validator.w3.org

**Critère 4.1.2 (A)** — Nom, rôle, valeur : pour tous les composants UI, le nom, le rôle et la valeur doivent être déterminables par programme :
```html
<!-- ✅ Composant custom : rôle + nom + état exposés -->
<div
  role="switch"
  aria-checked="true"
  aria-labelledby="notifications-label"
  tabindex="0"
  id="notif-switch"
>
  <span id="notifications-label">Notifications par email</span>
</div>

<!-- ✅ Barre de progression -->
<div
  role="progressbar"
  aria-valuenow="65"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-label="Téléchargement en cours"
>
  65%
</div>
```

**Critère 4.1.3 (AA — WCAG 2.1)** — Messages de statut : les messages qui n'ont pas le focus doivent pouvoir être perçus par les technologies d'assistance via les rôles ARIA :
```html
<!-- role="status" : polite (ne pas interrompre) -->
<div role="status" aria-live="polite">
  Vos modifications ont été enregistrées.
</div>

<!-- role="alert" : assertive (interruption immédiate) -->
<div role="alert" aria-live="assertive">
  Erreur : impossible de se connecter au serveur.
</div>

<!-- role="log" : historique (chat, logs) -->
<div role="log" aria-live="polite" aria-relevant="additions">
  <!-- Nouveaux messages ajoutés -->
</div>
```

---

## RGAA — Spécificités Françaises

### Contexte légal

Le RGAA (Référentiel Général d'Amélioration de l'Accessibilité) est la déclinaison française des WCAG, rendu obligatoire par la loi pour :
- Les services de l'État et établissements publics (loi du 11 février 2005, décret du 24 juillet 2019)
- Les entreprises dont le chiffre d'affaires dépasse 250M€ en France (depuis 2023)
- Les applications mobiles des administrations publiques

**Sanctions** : jusqu'à 25 000€ d'amende par service non conforme, après mise en demeure par la DINUM.

### Obligations RGAA

```
Déclaration d'accessibilité obligatoire :
├── Page dédiée sur le site (/accessibilite ou /declaration-accessibilite)
├── Statut de conformité (conforme, partiellement conforme, non conforme)
├── Technologies d'assistance testées
├── Liste des non-conformités avec impact
├── Alternatives pour les contenus non accessibles
├── Contact pour signaler un problème d'accessibilité
└── Voies de recours (Défenseur des Droits)

Plan pluriannuel de mise en accessibilité :
├── Calendrier de correction des non-conformités
├── Priorisation par impact utilisateur
└── Budget alloué
```

### Critères RGAA spécifiques

Le RGAA 4.1 comprend 106 critères répartis dans 13 thématiques, quelques différences notables avec WCAG 2.1 :

| RGAA | Différence avec WCAG |
|---|---|
| Thématique 4 (Tableaux) | Critères plus détaillés sur les tableaux de données complexes |
| Thématique 12 (Navigation) | Exige un moteur de recherche OU un plan du site (en plus des menus) |
| Thématique 13 (Consultation) | Précisions sur les documents bureautiques (PDF, DOCX) — PDF/UA requis |
| Tests RGAA | Méthode de tests officiels avec environnements de test définis (NVDA+Firefox, JAWS+Edge) |

### Environnements de test RGAA officiels

```
Desktop (Windows) :
├── NVDA (dernière version) + Firefox (dernière version)
├── JAWS (avant-dernière version majeure) + Edge (dernière version)
└── Navigateur + zoom 200%

Desktop (macOS) :
└── VoiceOver (OS intégré) + Safari (dernière version)

Mobile :
├── iOS : VoiceOver + Safari
└── Android : TalkBack + Chrome
```
