# Études de Cas — Accessibilité en Production

## Overview

Quatre études de cas réelles couvrant les situations les plus fréquentes en production : audit de conformité RGAA pour un service public, refonte d'un formulaire multi-étapes SaaS, correction d'une modal e-commerce, et construction d'un design system accessible from scratch. Chaque cas documente le contexte initial, les non-conformités trouvées, la solution implémentée avec le code, et les résultats mesurables.

---

## Cas 1 — Audit RGAA d'un Service Public (Administration Française)

### Contexte

**Organisation** : Direction des Systèmes d'Information d'une collectivité territoriale de 400 000 habitants.

**Service audité** : Portail en ligne de démarches administratives — déclarations, demandes de documents, paiements de services municipaux. 8 grandes catégories de formulaires, ~120 pages différentes, ~15 000 sessions mensuelles.

**Obligation légale** : Soumis au RGAA 4.1 depuis septembre 2020 (décret n°2019-768 du 24 juillet 2019). Le service était classifié "non conforme" depuis 2 ans, avec risque de mise en demeure par la DINUM.

**Équipe projet** : 1 chef de projet DSI, 2 développeurs web, 1 expert accessibilité externe (prestataire).

**Durée de l'audit** : 3 semaines pour la phase d'audit, 6 mois pour la mise en conformité.

---

### Méthodologie d'audit RGAA

L'audit RGAA suit un protocole standardisé avec un échantillon représentatif de pages :

```
Échantillon d'audit (15 pages sélectionnées selon la méthode RGAA) :
├── Pages d'entrée : accueil, plan du site, page de contact
├── Pages de processus : formulaire de demande de carte grise (5 étapes)
├── Pages de consultation : liste des services, détail d'un service
├── Pages spécifiques : résultats de recherche, espace personnel
└── Pages obligatoires RGAA : mentions légales, déclaration d'accessibilité

Environnements de test RGAA officiels utilisés :
├── Windows 11 + NVDA 2024.1 + Firefox 125
├── Windows 11 + JAWS 2024 + Edge 124
└── macOS 14 + VoiceOver + Safari 17
```

**Grille d'audit** : 106 critères RGAA 4.1 testés sur chaque page de l'échantillon.

Score initial : **32% de conformité** (conforme = critère réussi sur toutes les pages de l'échantillon)

---

### Non-conformités — Les 47 Problèmes Identifiés

Les non-conformités ont été classées selon leur impact utilisateur :

#### Bloquants (12 non-conformités) — Accès impossible pour certains utilisateurs

```
NC-001 [Critique] Critère 1.1 — 34 images informatives sans attribut alt
  Impact : les utilisateurs de lecteurs d'écran ne peuvent pas comprendre les pictogrammes de statut
  Pages affectées : 8/15 pages de l'échantillon
  Exemple : <img src="statut-en-cours.png"> — aucun alt

NC-002 [Critique] Critère 11.1 — 18 champs de formulaire sans label associé
  Impact : les champs non étiquetés sont illisibles avec un lecteur d'écran
  Pages affectées : formulaires de demande (4 pages)
  Exemple : <input type="text" placeholder="Votre nom"> — placeholder ≠ label

NC-003 [Critique] Critère 10.1 — meta viewport user-scalable=no
  Impact : blocage du zoom — problème majeur pour les malvoyants
  Code problématique :
  <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">

NC-004 [Critique] Critère 4.1 — 5 vidéos sans sous-titres
  Impact : contenu audio inaccessible aux sourds et malentendants
  Pages affectées : page d'accueil, tutoriels d'utilisation

NC-005 [Critique] Critère 12.6 — pas de skip link
  Impact : les utilisateurs clavier traversent 47 liens de navigation avant le contenu
  Mesuré : 47 Tab pour atteindre le premier champ de formulaire

NC-006 [Critique] Critère 7.1 — pièges au focus dans les menus déroulants
  Impact : impossible de quitter les menus au clavier
```

#### Majeurs (21 non-conformités) — Accès très difficile

```
NC-007 Critère 3.1 — contraste insuffisant sur texte primaire
  Ratio mesuré : 3,2:1 (requis : 4,5:1) pour couleur #767676 sur #ffffff
  Pages affectées : toutes les pages (couleur du corps de texte)

NC-008 Critère 3.2 — informations transmises par couleur seule
  Exemples : statuts "En cours" (orange), "Validé" (vert), "Refusé" (rouge)
  sans icône ni texte complémentaire

NC-009 Critère 11.10 — messages d'erreur formulaire non associés aux champs
  Les erreurs apparaissent dans un bandeau en haut de page
  L'utilisateur lecteur d'écran ne sait pas quel champ est en erreur

NC-010 Critère 8.5 — titres de page non descriptifs
  Toutes les pages du formulaire de carte grise ont le même titre :
  <title>Démarches en ligne — Collectivité</title>

NC-011 Critère 6.1 — liens non explicites ("Cliquez ici", "En savoir plus" × 23)
```

#### Mineurs (14 non-conformités) — Gêne ou confusion

```
NC-012 Critère 8.7 — changements de langue non identifiés
  Termes anglais (Dashboard, Login, Reset) sans attribut lang="en"

NC-013 Critère 13.3 — délai de session sans avertissement
  La session expire après 15 minutes sans notification préalable

NC-014 Critère 10.11 — contenu ne passe pas à 320px de large (reflow)
  Les tableaux de données nécessitent un scroll horizontal sur mobile

[...]
```

---

### Plan de Remédiation par Priorité

```
SPRINT 1 — Bloquants critiques (mois 1-2)
Objectif : 0 NC bloquante → conformité partielle déclarée

┌─────────────────────────────────────────────────────────┐
│ NC-003 : Supprimer user-scalable=no                     │ 2h
│ NC-005 : Ajouter skip links sur toutes les pages        │ 1 jour
│ NC-006 : Corriger les pièges au clavier (menus)         │ 3 jours
│ NC-001 : Ajouter les alt manquants (audit images)       │ 5 jours
│ NC-002 : Associer labels aux champs (formulaires)       │ 1 semaine
│ NC-004 : Sous-titrer les 5 vidéos (prestataire externe) │ 2 semaines
└─────────────────────────────────────────────────────────┘
Durée Sprint 1 : 6 semaines, 2 développeurs
```

**Correction NC-002 — Labels manquants (exemple de code avant/après)** :
```html
<!-- ❌ AVANT — placeholder utilisé comme label -->
<div class="form-group">
  <input
    type="text"
    id="nom-demandeur"
    placeholder="Votre nom de famille"
    class="form-control"
  >
</div>

<!-- ✅ APRÈS — label explicite + indication obligatoire -->
<div class="form-group">
  <label for="nom-demandeur">
    Nom de famille
    <span class="obligatoire" aria-label="(champ obligatoire)">*</span>
  </label>
  <input
    type="text"
    id="nom-demandeur"
    name="nom"
    autocomplete="family-name"
    aria-required="true"
    aria-describedby="nom-aide"
    class="form-control"
  >
  <p id="nom-aide" class="form-text">
    Tel qu'il apparaît sur vos documents officiels.
  </p>
</div>
```

**Correction NC-009 — Erreurs associées aux champs** :
```html
<!-- ❌ AVANT — erreurs dans un bandeau global -->
<div class="alert alert-danger" role="alert">
  <p>Le formulaire contient des erreurs. Veuillez les corriger.</p>
</div>

<!-- ✅ APRÈS — erreurs liées aux champs + résumé d'erreurs cliquable -->
<!-- Résumé d'erreurs en haut avec focus automatique -->
<div
  id="resume-erreurs"
  role="alert"
  aria-labelledby="titre-erreurs"
  tabindex="-1"
>
  <h2 id="titre-erreurs">
    Le formulaire contient 3 erreurs. Veuillez les corriger.
  </h2>
  <ul>
    <li><a href="#nom-demandeur">Nom de famille : ce champ est obligatoire</a></li>
    <li><a href="#email">Email : format invalide</a></li>
    <li><a href="#date-naissance">Date de naissance : date dans le futur</a></li>
  </ul>
</div>

<!-- Erreur au niveau du champ -->
<div class="form-group">
  <label for="nom-demandeur">Nom de famille *</label>
  <input
    type="text"
    id="nom-demandeur"
    aria-invalid="true"
    aria-describedby="nom-erreur"
    class="form-control is-invalid"
  >
  <p id="nom-erreur" class="invalid-feedback">
    Ce champ est obligatoire.
  </p>
</div>
```

```typescript
// Gestion du focus après soumission avec erreurs (RGAA 11.10)
function handleSubmit(e: React.FormEvent) {
  e.preventDefault();
  const erreurs = valider(valeurs);

  if (Object.keys(erreurs).length > 0) {
    setErreurs(erreurs);
    // Déplacer le focus vers le résumé d'erreurs
    setTimeout(() => {
      document.getElementById('resume-erreurs')?.focus();
    }, 100);
  } else {
    soumettre(valeurs);
  }
}
```

---

### Résultats après 6 mois

```
Avant audit     → Après Sprint 1  → Après conformité complète
32% conformité  → 61% conformité  → 87% conformité (partiellement conforme)

Non-conformités :
47 NC totales   → 19 NC restantes → 13 NC résiduelles (AAA, médias legacy)

Violations axe (Lighthouse) :
Score 41        → Score 74        → Score 93

Temps d'accomplissement des tâches (test utilisateurs, n=8 avec AT) :
Formulaire carte grise : 24 min → 11 min
Espace personnel : non réalisable → 7 min

Statut légal :
Non conforme → Partiellement conforme (déclaration publiée)
→ Plan pluriannuel pour atteindre la conformité complète en 18 mois
```

**Leçons apprises** :
- 60% des corrections ne nécessitaient aucune refonte — juste des attributs manquants
- Les labels manquants et les alt manquants représentaient à eux seuls 45% du temps de correction
- La formation de l'équipe de 2 jours a réduit les régressions de 70% sur les sprints suivants
- La DINUM a accepté le plan pluriannuel comme preuve de démarche sincère

---

## Cas 2 — Refonte d'un Formulaire Multi-Étapes (SaaS B2B)

### Contexte

**Produit** : SaaS de gestion RH, formulaire d'onboarding d'un nouvel employé — 4 étapes, 35 champs, logique conditionnelle complexe.

**Problème initial** : L'équipe support signalait que 15% des tickets concernaient des problèmes de saisie du formulaire. Un audit interne révèle que le formulaire est inutilisable avec un lecteur d'écran.

**Stack technique** : React 18, React Hook Form, Zod, Tailwind CSS.

---

### Audit initial — État des lieux

```
Test axe (jest-axe) sur le formulaire initial :
──────────────────────────────────────────────
Violations : 23 violations au niveau critical/serious
  ├── 8 × "Form elements must have labels" (impact: critical)
  ├── 5 × "Color-contrast" (impact: serious)
  ├── 4 × "aria-required-attr" (impact: critical)
  ├── 3 × "invalid-aria-prop" (impact: critical)
  └── 3 × "button-name" (impact: critical)

Test manuel clavier :
  ├── ❌ Aucun skip link
  ├── ❌ Indicateur d'étape non annoncé (barre de progression muette)
  ├── ❌ Aucune gestion du focus entre les étapes
  ├── ❌ Messages d'erreur non associés aux champs
  ├── ❌ Select custom inaccessible (div cliquable sans role)
  └── ❌ Date picker : composant tiers non accessible

Test NVDA :
  ├── ❌ Champ "Département" annoncé : "Sélectionner Combo" (pas de label)
  ├── ❌ Erreurs de validation : pas annoncées
  ├── ❌ Passage à l'étape 2 : le focus reste sur le bouton "Suivant" (pas de feedback)
  └── ❌ Champ de date : les 3 selects (jour/mois/année) annoncés sans contexte
```

---

### Solution — Refactorisation Complète

#### Barre de progression accessible

```typescript
// ❌ AVANT — div visuelle sans sémantique
function BarreProgression({ étape, total }: Props) {
  return (
    <div className="progress-bar">
      {Array.from({ length: total }, (_, i) => (
        <div key={i} className={`step ${i < étape ? 'completed' : ''}`}>
          {i + 1}
        </div>
      ))}
    </div>
  );
}

// ✅ APRÈS — sémantique et annonce aux lecteurs d'écran
function BarreProgression({ étape, total, nomÉtape }: Props) {
  return (
    <nav aria-label="Progression du formulaire">
      <ol>
        {étapesFormulaire.map((e, index) => (
          <li
            key={e.id}
            aria-current={index + 1 === étape ? 'step' : undefined}
          >
            <span
              className={`step-indicator ${
                index + 1 < étape ? 'completed' :
                index + 1 === étape ? 'current' : 'upcoming'
              }`}
              aria-hidden="true"
            >
              {index + 1 < étape ? '✓' : index + 1}
            </span>
            <span>{e.label}</span>
          </li>
        ))}
      </ol>

      {/* Annonce de la progression pour les lecteurs d'écran */}
      <div role="status" aria-live="polite" aria-atomic="true" className="sr-only">
        Étape {étape} sur {total} : {nomÉtape}
      </div>
    </nav>
  );
}
```

#### Gestion du focus entre étapes

```typescript
// ✅ Déplacer le focus vers le titre de la nouvelle étape lors du changement
const titreÉtapeRef = useRef<HTMLHeadingElement>(null);

function allerÀÉtapeSuivante() {
  const erreurs = validerÉtape(étapeActuelle, valeurs);
  if (Object.keys(erreurs).length > 0) {
    setErreurs(erreurs);
    // Focus vers le résumé d'erreurs
    setTimeout(() => document.getElementById('erreurs-étape')?.focus(), 50);
    return;
  }

  setÉtapeActuelle(prev => prev + 1);

  // Déplacer le focus vers le titre de la nouvelle étape
  setTimeout(() => {
    titreÉtapeRef.current?.focus();
  }, 100); // Délai pour laisser le temps au rendu
}

// Dans le JSX de chaque étape
<h2
  ref={titreÉtapeRef}
  tabIndex={-1} // Permet le focus programmatique
  id={`titre-étape-${étapeActuelle}`}
>
  {nomÉtapeActuelle}
</h2>
```

#### Sélecteur de département — Composant custom accessible

```typescript
// ❌ AVANT — div non accessible
<div
  className="custom-select"
  onClick={() => setOuvert(!ouvert)}
>
  {valeurSélectionnée || 'Sélectionner'}
</div>

// ✅ APRÈS — Combobox ARIA (cf. aria-patterns.md)
function SélecteurDépartement({ valeur, onChange }: Props) {
  return (
    <div>
      <label htmlFor="département">
        Département
        <span aria-label="(obligatoire)" aria-hidden="false"> *</span>
      </label>
      <select
        id="département"
        name="département"
        value={valeur}
        onChange={e => onChange(e.target.value)}
        required
        aria-required="true"
      >
        <option value="">Sélectionner un département</option>
        {départements.map(d => (
          <option key={d.code} value={d.code}>{d.nom}</option>
        ))}
      </select>
    </div>
  );
  // Note : <select> natif est préférable au combobox custom pour une liste simple
}
```

#### Champ de date accessible

```typescript
// ✅ Date picker natif avec fallback pour les navigateurs incompatibles
function ChampDate({
  id,
  label,
  valeur,
  onChange,
  erreur,
  min,
  max
}: ChampDateProps) {
  const erreurId = `${id}-erreur`;
  const aideId = `${id}-aide`;

  return (
    <div>
      <label htmlFor={id}>{label}</label>

      <input
        type="date"
        id={id}
        name={id}
        value={valeur}
        min={min}
        max={max}
        onChange={e => onChange(e.target.value)}
        aria-invalid={!!erreur}
        aria-describedby={[erreur ? erreurId : null, aideId]
          .filter(Boolean).join(' ')}
        aria-required="true"
      />

      <p id={aideId} className="aide">
        Format : JJ/MM/AAAA
      </p>

      {erreur && (
        <p id={erreurId} role="alert" className="erreur">
          {erreur}
        </p>
      )}
    </div>
  );
}
```

---

### Résultats après refactorisation

```
Violations axe :
23 violations → 0 violations critical/serious, 2 warnings mineurs

Test manuel clavier (protocole 20 points) :
20/20 points conformes (0/20 avant la refactorisation)

Test NVDA+Chrome :
❌ "Sélectionner Combo" → ✅ "Département, liste déroulante, Sélectionner un département"
❌ Erreurs non annoncées → ✅ "Ce champ est obligatoire" annoncé immédiatement
❌ Passage étape sans feedback → ✅ "Étape 2 sur 4 : Informations professionnelles"

Test utilisateurs (n=6, dont 2 utilisateurs de lecteurs d'écran) :
Avant : 2/6 utilisateurs complétaient le formulaire (SR)
Après : 6/6 utilisateurs complétaient le formulaire

Tickets support "problème formulaire" :
-63% de tickets en 3 mois post-déploiement

Temps de complétion moyen :
8 min 30 → 6 min 15 (tous utilisateurs, dont bénéfice pour les utilisateurs typiques)

Score Lighthouse accessibilité : 54 → 97
```

---

## Cas 3 — Modal et Gestion du Focus (E-commerce)

### Contexte

**Produit** : Marketplace B2C, ~2 millions de visiteurs mensuels. Une modal de sélection de taille/couleur est centrale dans le parcours d'achat.

**Rapport de bug** : Un utilisateur VoiceOver signale qu'il ne peut pas utiliser la modal de sélection de variante — rapport relayé sur Twitter et amplifi par la communauté #a11y francophone.

---

### Problèmes identifiés

```
Bug 1 : aria-modal ignoré par VoiceOver iOS
Le contenu hors modal reste accessible via le rotor VoiceOver.
L'utilisateur peut "sortir" de la modal sans la fermer.

Bug 2 : Focus non retourné au déclencheur à la fermeture
Après fermeture, le focus va au haut de la page (body).
L'utilisateur perd sa position dans le catalogue.

Bug 3 : Focus initial dans la modal
Le focus va sur la modal (div), pas sur le premier élément interactif.
NVDA : "Dialogue. Sélectionner la taille de votre produit" puis silence.

Bug 4 : Escape ne ferme pas toujours
Sur mobile avec clavier bluetooth, Escape ne déclenche pas onKeyDown
si un input à l'intérieur est focus.

Bug 5 : Scroll verrouillé mais accessible au lecteur d'écran
Le fond est bloqué au scroll mais VoiceOver iOS peut toujours naviguer
dans le contenu hors modal via les gestes.
```

---

### Solution Complète

```typescript
import { useEffect, useRef, useCallback, useId } from 'react';
import { createPortal } from 'react-dom';

const SÉLECTEURS_FOCUSABLES = [
  'a[href]:not([disabled])',
  'button:not([disabled])',
  'input:not([disabled])',
  'select:not([disabled])',
  'textarea:not([disabled])',
  '[tabindex]:not([tabindex="-1"]):not([disabled])',
].join(', ');

function ModalVariante({
  isOpen,
  onClose,
  produit,
  onAjouterPanier,
}: ModalVarianteProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const déclencheurRef = useRef<HTMLElement | null>(null);
  const titreId = useId();

  // ── Masquage du contenu hors modal pour VoiceOver iOS ──────────────────
  useEffect(() => {
    // Sélectionner tous les éléments frères de la modal dans le body
    const élémentsPrincipaux = Array.from(
      document.body.children
    ).filter(el => !el.contains(modalRef.current));

    if (isOpen) {
      // Mémoriser le déclencheur
      déclencheurRef.current = document.activeElement as HTMLElement;

      // Masquer le reste de la page aux lecteurs d'écran
      élémentsPrincipaux.forEach(el => {
        el.setAttribute('aria-hidden', 'true');
        (el as HTMLElement).setAttribute('data-original-inert', '');
        (el as HTMLElement).inert = true;
      });

      // Bloquer le scroll
      document.body.style.overflow = 'hidden';

      // Déplacer le focus vers le premier élément focusable
      requestAnimationFrame(() => {
        const premier = modalRef.current?.querySelector<HTMLElement>(
          SÉLECTEURS_FOCUSABLES
        );
        premier?.focus();
      });

    } else {
      // Restaurer l'accessibilité du contenu
      élémentsPrincipaux.forEach(el => {
        el.removeAttribute('aria-hidden');
        (el as HTMLElement).inert = false;
      });

      document.body.style.overflow = '';

      // Restaurer le focus au déclencheur
      déclencheurRef.current?.focus();
    }

    return () => {
      élémentsPrincipaux.forEach(el => {
        el.removeAttribute('aria-hidden');
        (el as HTMLElement).inert = false;
      });
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  // ── Focus trap ─────────────────────────────────────────────────────────
  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLDivElement>) => {
    // Escape : fermer la modal
    if (e.key === 'Escape') {
      e.preventDefault();
      e.stopPropagation();
      onClose();
      return;
    }

    if (e.key !== 'Tab') return;

    const focusables = Array.from(
      modalRef.current?.querySelectorAll<HTMLElement>(SÉLECTEURS_FOCUSABLES) ?? []
    ).filter(el => !el.closest('[hidden]') && !el.closest('[inert]'));

    if (focusables.length === 0) {
      e.preventDefault();
      return;
    }

    const premier = focusables[0];
    const dernier = focusables[focusables.length - 1];

    if (e.shiftKey) {
      if (document.activeElement === premier || document.activeElement === modalRef.current) {
        e.preventDefault();
        dernier.focus();
      }
    } else {
      if (document.activeElement === dernier) {
        e.preventDefault();
        premier.focus();
      }
    }
  }, [onClose]);

  if (!isOpen) return null;

  return createPortal(
    <>
      {/* Fond assombri */}
      <div
        className="modal-backdrop"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Modal */}
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titreId}
        className="modal-variante"
        onKeyDown={handleKeyDown}
      >
        {/* En-tête */}
        <div className="modal-header">
          <h2 id={titreId} className="modal-titre">
            Sélectionner une variante — {produit.nom}
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label={`Fermer la sélection de variante pour ${produit.nom}`}
            className="modal-close"
          >
            <svg aria-hidden="true" focusable="false" viewBox="0 0 24 24">
              <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2"/>
            </svg>
          </button>
        </div>

        {/* Corps */}
        <div className="modal-body">
          <SélecteurTaille
            tailles={produit.tailles}
            onChange={/* ... */}
          />
          <SélecteurCouleur
            couleurs={produit.couleurs}
            onChange={/* ... */}
          />
        </div>

        {/* Actions */}
        <div className="modal-footer">
          <button
            type="button"
            onClick={onClose}
            className="btn-secondary"
          >
            Annuler
          </button>
          <button
            type="button"
            onClick={onAjouterPanier}
            className="btn-primary"
          >
            Ajouter au panier
          </button>
        </div>
      </div>
    </>,
    document.body
  );
}
```

---

### Matrice de Tests — 4 Combinaisons Technologies d'Assistance

```
Environnement 1 : NVDA 2024 + Chrome 124 (Windows)
──────────────────────────────────────────────────────
Ouverture modal    : ✅ Annonce "Sélectionner une variante — [produit], Dialogue"
Focus initial      : ✅ Focus sur premier bouton de sélection de taille
Focus trap         : ✅ Tab cycle dans la modal
Escape             : ✅ Ferme la modal, focus revient au bouton "Sélectionner"
VoiceOver hors mod : ✅ Contenu hors modal non accessible (inert)

Environnement 2 : VoiceOver + Safari (macOS 14)
──────────────────────────────────────────────────
Ouverture modal    : ✅ Annonce "Sélectionner une variante — [produit], Dialogue"
Focus initial      : ✅ Focus sur premier élément interactif
Rotor              : ✅ Navigation limitée à la modal
Escape             : ✅ Ferme et retour focus
Geste 2 doigts     : ✅ Scroll limité à la modal

Environnement 3 : VoiceOver iOS + Safari (iPhone)
──────────────────────────────────────────────────
Ouverture modal    : ✅ Annonce correcte (inert sur contenu hors modal)
Navigation gestes  : ✅ Focus limité à la modal
aria-modal seul    : ❌ Sans inert : VoiceOver navigue hors modal
Fermeture (2-tap)  : ✅ Focus retourne au déclencheur

Environnement 4 : TalkBack + Chrome (Android)
──────────────────────────────────────────────
Ouverture modal    : ✅ Annonce correcte
Navigation         : ✅ Gestes limités à la modal
Escape (clavier)   : ✅ Ferme et retour focus
```

**Résultat** : Solution testée conforme sur les 4 combinaisons AT. Déploiement en production avec zéro régression signalée sur les AT.

---

## Cas 4 — Design System Accessible From Scratch (Startup 30 Développeurs)

### Contexte

**Organisation** : Scale-up B2B SaaS, 30 développeurs front-end, 3 équipes produit indépendantes.

**Problème** : Après 3 ans de croissance rapide, le codebase contient 47 implémentations différentes de boutons, 12 patterns de formulaire différents, aucune cohérence d'accessibilité. Score Lighthouse moyen : 58. Décision : refondre avec un design system.

**Contexte légal** : Ambition commerciale vers le secteur public européen — RGAA AA sera requis dans les appels d'offres.

**Timeline** : 8 mois (2 développeurs seniors + 1 designer système).

---

### Stratégie de Construction

#### Phase 1 — Fondations (mois 1-2)

**Design tokens accessibles** :

```typescript
// tokens/colors.ts — Toutes les couleurs validées en contraste
export const colorTokens = {
  // Couleurs de texte
  text: {
    primary: '#1a1a2e',    // ratio: 17,5:1 sur blanc
    secondary: '#4a5568',  // ratio: 7,4:1 sur blanc
    muted: '#718096',      // ratio: 4,6:1 sur blanc — minimum AA
    inverse: '#ffffff',    // ratio: 17,5:1 sur primary
    disabled: '#a0aec0',   // ratio: 2,9:1 — réservé au texte désactivé (exception WCAG)
  },

  // Couleurs de fond
  background: {
    default: '#ffffff',
    subtle: '#f7fafc',
    muted: '#edf2f7',
  },

  // Couleurs sémantiques — toutes validées AA
  semantic: {
    // Erreur : texte foncé sur fond clair pour garantir le contraste
    error: {
      text: '#c53030',          // ratio: 5,9:1 sur blanc
      background: '#fff5f5',    // ratio: 14,2:1 pour errorText sur ce fond
      border: '#fc8181',        // ratio: 3,1:1 composant UI (requis: 3:1)
    },
    success: {
      text: '#276749',          // ratio: 7,1:1 sur blanc
      background: '#f0fff4',
      border: '#68d391',        // ratio: 3,2:1 composant UI
    },
    warning: {
      text: '#7b341e',          // ratio: 8,1:1 sur fond warning-background
      background: '#fffbeb',
      border: '#f6ad55',        // ratio: 3,1:1 composant UI
    },
    info: {
      text: '#1a365d',          // ratio: 12,3:1 sur fond info-background
      background: '#ebf8ff',
      border: '#63b3ed',        // ratio: 3,1:1 composant UI
    },
  },

  // Focus — toujours en contraste 3:1 avec son environnement
  focus: {
    ring: '#005fcc',            // ratio: 7,6:1 sur blanc, 3,2:1 sur noir
  },
} as const;
```

```css
/* tokens/spacing.ts → CSS Custom Properties */
:root {
  /* Touch target minimum 44px selon Apple HIG / WCAG 2.5.8 */
  --touch-target-min: 44px;
  --touch-target-spacing: 8px;  /* Espacement pour cibles <44px */

  /* Focus */
  --focus-ring-width: 3px;
  --focus-ring-offset: 2px;
  --focus-ring-color: #005fcc;

  /* Animation — respectée par prefers-reduced-motion */
  --transition-duration: 200ms;
  --transition-easing: ease-in-out;
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --transition-duration: 0.01ms;
  }
}
```

#### Phase 2 — Composants Core (mois 3-5)

**Checklist d'accessibilité par composant** :

```typescript
// Exemple : Button — composant le plus critique
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  isDisabled?: boolean;
  loadingText?: string; // Texte pour lecteur d'écran pendant le chargement
  type?: 'button' | 'submit' | 'reset'; // Défaut 'button' pour éviter soumission accidentelle
  onClick?: () => void;
  // Pas de 'as' prop — évite les boutons qui sont des divs
}

function Button({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  isDisabled = false,
  loadingText = 'Chargement en cours',
  type = 'button',
  onClick,
}: ButtonProps) {
  return (
    <button
      type={type}
      disabled={isDisabled}
      aria-disabled={isDisabled || isLoading}
      aria-busy={isLoading}
      onClick={!isDisabled && !isLoading ? onClick : undefined}
      className={`btn btn-${variant} btn-${size} ${isLoading ? 'loading' : ''}`}
    >
      {isLoading ? (
        <>
          {/* Spinner visuel masqué aux lecteurs d'écran */}
          <span className="spinner" aria-hidden="true" />
          {/* Texte pour les lecteurs d'écran */}
          <span className="sr-only">{loadingText}</span>
          {/* Masquer le texte du bouton visuellement pendant le chargement */}
          <span aria-hidden="true" className="btn-text-loading">
            {children}
          </span>
        </>
      ) : children}
    </button>
  );
}
```

**Storybook a11y addon — Integration** :

```javascript
// .storybook/main.js
module.exports = {
  addons: [
    '@storybook/addon-a11y',
    // ...
  ],
};

// .storybook/preview.js
export const parameters = {
  a11y: {
    // Niveau de sévérité pour les règles axe
    config: {
      rules: [
        { id: 'color-contrast', enabled: true },
        { id: 'button-name', enabled: true },
      ],
    },
    options: {
      runOnly: {
        type: 'tag',
        values: ['wcag2a', 'wcag2aa', 'wcag21aa'],
      },
    },
  },
};
```

```typescript
// Button.stories.tsx — Stories avec tous les états
const Template: StoryFn<typeof Button> = (args) => <Button {...args} />;

export const Default = Template.bind({});
Default.args = { children: 'Confirmer la commande', variant: 'primary' };

export const Loading = Template.bind({});
Loading.args = {
  children: 'Confirmer la commande',
  isLoading: true,
  loadingText: 'Envoi de votre commande en cours...',
};

export const Disabled = Template.bind({});
Disabled.args = {
  children: 'Confirmer la commande',
  isDisabled: true,
};

// Test automatique axe dans Storybook Play function
Default.play = async ({ canvasElement }) => {
  const canvas = within(canvasElement);
  const button = canvas.getByRole('button');

  // Vérifier les attributs d'accessibilité
  expect(button).toHaveAttribute('type', 'button');
  expect(button).not.toHaveAttribute('aria-disabled', 'true');

  // Test axe
  await expect(canvas.getByRole('button')).toBeAccessible();
};
```

#### Phase 3 — Intégration et Formation (mois 6-7)

**Design review checklist** (intégrée dans le process PR design) :

```markdown
## Checklist A11y — Design Review

### Couleurs et contrastes
- [ ] Tous les textes ont un ratio ≥ 4,5:1 (normal) ou ≥ 3:1 (grand texte)
- [ ] Les composants UI ont un contraste de bordure ≥ 3:1
- [ ] L'information n'est pas transmise par la couleur seule (icône, texte, motif)
- [ ] Les états (hover, focus, active, disabled) sont tous différenciés sans couleur seule

### Cibles interactives
- [ ] Toutes les cibles font au moins 44×44px (ou 24×24px avec espacement compensatoire)
- [ ] Les zones cliquables incluent les labels (label et input formant une grande zone)

### États et feedback
- [ ] L'état de focus est clairement visible sur chaque composant interactif
- [ ] Les états d'erreur incluent un message texte (pas seulement une bordure rouge)
- [ ] Les états de chargement ont un feedback visuel ET textuel

### Structure
- [ ] La hiérarchie de titres est logique dans le composant
- [ ] L'ordre de lecture DOM correspond à l'ordre visuel
```

**Formation équipe** : 2 sessions de 3h (concepts WCAG + pratique avec NVDA), 1 session live sur un composant réel, documentation interne de 40 pages avec exemples.

---

### Résultats — 8 mois après le lancement du design system

```
Adoption :
Mois 1 : 20% du codebase migré
Mois 4 : 65% du codebase migré
Mois 8 : 90% du codebase migré

Score Lighthouse accessibilité :
Avant : 58 (moyenne)
Mois 3 : 74 (composants core migrés)
Mois 6 : 88 (migration avancée)
Mois 8 : 94 (quasi-complet)

Violations axe en CI :
Avant : ~340 violations détectées en audit ponctuel
Mois 8 : 0 violation critical/serious dans le pipeline CI

Régressions d'accessibilité (violations introduites par PR) :
Avant DS : non mesuré (pas de CI a11y)
Mois 3 : 12 régressions bloquées par CI en 1 mois
Mois 8 : 2 régressions bloquées (apprentissage équipe)

Impact sur la vélocité :
Mois 1-3 : -15% vitesse estimée (apprentissage, refactorisation)
Mois 4-6 : -5% (routine installée)
Mois 7-8 : +10% (réutilisation des composants, moins de bugs)

Résultat commercial :
2 appels d'offres secteur public gagnés en mentionnant le score RGAA
1 contrat enterprise signé — l'accessibilité était critère d'évaluation noté
```

**Leçon principale** : Construire l'accessibilité dans les composants de base coûte 2× plus de temps initialement mais divise par 10 le coût de mise en conformité par rapport à un audit tardif. Le ROI est positif dès le 6e mois.
