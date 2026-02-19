# Figma — Guide Essentiel pour Non-Designers

## Vue d'Ensemble

Figma est devenu le standard de l'industrie pour le design UI/UX et le prototypage. Initialement reserve aux designers, il est desormais utilise par les product managers, developpeurs et meme des profils metier pour collaborer sur les projets produit. Ce guide couvre l'essentiel pour etre operationnel en Figma sans formation design formelle.

---

## Interface et Navigation

### Structure d'un fichier Figma

```
Projet Figma
├── Page 1 — Wireframes
├── Page 2 — Design Final
├── Page 3 — Prototype
└── Page 4 — Design System
```

**Panneau gauche — Layers** : arborescence de tous les elements. Organiser les layers avec des noms explicites (pas "Rectangle 42"). Convention recommandee :
- Frames : kebab-case en majuscules (ex: `HOME-DESKTOP`, `CARD-PRODUCT`)
- Components : PascalCase (ex: `ButtonPrimary`, `InputField`)
- Layers basiques : snake_case descriptif (ex: `hero_background`, `cta_text`)

**Panneau droit — Properties** : proprietes de l'element selectionne (taille, couleur, typographie, effets).

**Toolbar centrale** : outils principaux

| Icone | Outil | Raccourci | Usage |
|---|---|---|---|
| Fleche | Selection | V | Selectionner et deplacer |
| Cadre | Frame | F | Creer un conteneur |
| Rectangle | Forme | R | Dessiner des rectangles |
| Crayon | Pen | P | Dessiner des formes vectorielles |
| T | Text | T | Ajouter du texte |
| Main | Hand | H | Naviguer dans le canvas |
| Loupe | Zoom | Z | Zoomer/dezoomer |

---

## Concepts Fondamentaux

### Frames vs Groupes — La Difference Cle

**Groupe** (Cmd+G) : conteneur simple sans proprietes propres. Les elements a l'interieur conservent leurs positions absolues. Utiliser pour : grouper temporairement des elements.

**Frame** (F ou Cmd+Alt+G) : conteneur avec des proprietes propres (couleur de fond, coins arrondis, padding, auto layout, contraintes). Utiliser pour : ecrans, cartes, sections de page, composants.

**Regle pratique** : preferer les Frames aux Groupes dans 95% des cas. Les Frames permettent les contraintes de redimensionnement et l'Auto Layout.

### Auto Layout — Le Systeme Essentiel

Auto Layout transforme une Frame en un conteneur flexible qui gere automatiquement l'espacement et l'alignement de ses enfants.

**Activer** : selectionner une Frame → Shift+A (ou bouton "+" dans la section Auto Layout du panneau droit)

**Configuration** :
```
Direction : Horizontal | Vertical | Wrap
Spacing between items : espacement entre elements
Padding : Top, Right, Bottom, Left
Alignment : Start | Center | End | Space between
```

**Pourquoi Auto Layout est indispensable** :
- Ajouter un element recalcule l'espacement automatiquement
- Redimensionner un bouton ajuste le padding automatiquement
- Base de tous les composants reutilisables

**Exemple pratique — Bouton auto layout** :
```
Frame (Auto Layout Horizontal)
├── Icon (optionnel, 16x16)
└── Label "Envoyer"
Padding : 12px vertical, 20px horizontal
Gap : 8px
```

### Contraintes de Redimensionnement

Les contraintes definissent le comportement d'un element quand son parent est redimensionne.

**Types de contraintes** :
- **Left / Right / Top / Bottom** : ancre a ce bord
- **Left and Right** : s'etire horizontalement
- **Center** : reste centre
- **Scale** : se redimensionne proportionnellement

**Usage typique** :
- Navigation bar : contrainte "Left and Right" + "Top" → s'etire avec la page
- Bouton CTA : contrainte "Center" → reste centre
- Sidebar : contrainte "Top and Bottom" + "Left" → s'etire en hauteur

---

## Components et Design System

### Creer un Component

**1. Creer le composant de base** :
Dessiner l'element, le selectionner → Cmd+Alt+K (ou clic droit → Create component)

**2. Nommer le component** (convention recommandee) :
```
Category/ComponentName/Variant
Ex:
Button/Primary/Default
Button/Primary/Hover
Button/Primary/Disabled
Input/Text/Default
Input/Text/Error
Card/Product/Default
```

**3. Variants** (depuis Figma 2021) :
Plusieurs etats d'un meme composant geres ensemble. Le designer (ou vous) peut passer de "Default" a "Hover" a "Disabled" en 1 clic dans les proprietes.

### Utiliser les Components

**Instance** : copie d'un composant master. Modifier le master met a jour toutes les instances. Mais chaque instance peut etre personnalisee (texte, couleur) sans affecter le master.

**Detach** (Cmd+Alt+B) : detache une instance du composant master → devient un groupe editable normal. Utiliser uniquement si vous avez besoin de modifier la structure, pas juste le contenu.

### Styles Partagees

**Couleurs** : creer dans le panneau droit → Style → "+" → nommer (ex: `Primary/Blue-600`, `Neutral/Gray-400`)

**Typographie** : idem pour les styles de texte. Definir : police, taille, graisse, hauteur de ligne, espacement des lettres.

**Effets** : ombres, flous. Creer une fois, reutiliser partout.

**Avantage** : si la couleur primaire change (#0052CC → #003F99), changer le style met a jour tous les elements en 1 clic.

---

## Workflow pour un Non-Designer

### Etape 1 — Partir d'un Template

**Figma Community** (figma.com/community) : rechercher des templates gratuits.

Termes de recherche utiles :
- `wireframe kit` : structure de basse fidelite
- `UI kit` : composants complets (boutons, formulaires, navigation)
- `presentation template` : slides professionnels
- `dashboard template` : tableaux de bord
- `mobile app design` : design mobile complet

**Templates recommandes (gratuits)** :
- **Material Design 3** : composants Google, tres complets
- **Untitled UI** : design system propre, 7000+ composants
- **Primer** : design system GitHub, excellent pour les outils internes

### Etape 2 — Creer son Brand Kit

Fichier dedie `Brand-Kit.fig` avec :

```
Page 1 — Colors
├── Palette primaire (5-9 nuances)
├── Palette secondaire
├── Couleurs semantiques (Success, Warning, Error, Info)
└── Neutrales (Gray 50 → Gray 900)

Page 2 — Typography
├── Heading H1 → H6 avec styles
├── Body Regular / Medium
├── Caption / Label / Overline
└── Code / Mono (si applicable)

Page 3 — Components Base
├── Boutons (Primary, Secondary, Ghost, Danger)
├── Inputs (Text, Select, Checkbox, Radio)
├── Cards
├── Badges / Tags
└── Alerts

Page 4 — Icons
└── Jeu d'icones coherent (Heroicons, Lucide, Material Icons)
```

### Etape 3 — Prototypage

**Connecter les ecrans** : onglet "Prototype" (panneau droit) → selectionner un element → tirer le lien vers l'ecran de destination.

**Interactions disponibles** :
- On click / On hover / On drag
- Navigate to / Open overlay / Scroll to
- Animations : Instant, Dissolve, Smart Animate, Push, Slide

**Smart Animate** : Figma anime automatiquement les elements communs entre deux ecrans si leurs noms de layers correspondent. Creer des animations fluides sans code.

**Partager le prototype** : Share → Get link → "Prototype" → le destinataire peut tester sans compte Figma.

---

## Collaboration et Handoff

### Commentaires

Cmd+/ → "Comment" ou touche C. Cliquer sur l'element a commenter. Les commentaires sont visibles par tous les collaborateurs. Utiliser @mention pour notifier quelqu'un.

**Workflow revue de design** :
1. Designer partage le lien "View only"
2. Parties prenantes ajoutent des commentaires directement sur le design
3. Designer resout les commentaires et notifie
4. Evite les aller-retours par email avec des screenshots

### Figma Dev Mode

Pour les developpeurs : activer le Dev Mode (toggle en haut a droite) pour :
- Voir les specifications precises (px, couleurs en hex/rgba, typographie)
- Copier le CSS/Swift/Kotlin directement
- Voir les assets a exporter
- Comparer le design et l'implementation (Compare mode)

**Export des assets** :
- Selectionner un element → panneau droit → "Export"
- Formats : PNG (1x, 2x, 3x), SVG, PDF
- SVG recommande pour les icones (vectoriel, scalable)
- PNG 2x pour les illustrations et photos

---

## Figma AI (2025-2026)

### Make Design

Generer un design complet a partir d'une description textuelle.

```
Prompt example :
"Create a SaaS dashboard for a project management tool.
Include a sidebar navigation, a header with user avatar,
and a main content area with task cards and a progress chart.
Use a clean, minimal style with blue accent colors."
```

Figma genere une structure de frames et composants que vous pouvez ensuite modifier.

### Rename Layers

Selectionner plusieurs layers → clic droit → "Rename with AI". Figma analyse le contenu et nomme les layers de facon descriptive automatiquement.

**Avant** : `Rectangle 47`, `Text 3`, `Group 12`
**Apres** : `card_background`, `product_title`, `price_badge`

### Remove Background

Selectionner une image → panneau droit → "Remove background". Suppression automatique sans Photoshop.

### First Draft

Generer un premier brouillon de design a partir d'une description de page ou de feature. Utile pour le POC rapide avant d'impliquer un designer.

---

## Raccourcis Essentiels

### Navigation

| Action | Mac | Windows |
|---|---|---|
| Zoom in/out | Cmd + / - | Ctrl + / - |
| Fit to screen | Shift+1 | Shift+1 |
| Fit selection | Shift+2 | Shift+2 |
| Pan | Space + drag | Space + drag |
| Zoom 100% | Cmd+0 | Ctrl+0 |

### Selection et Edition

| Action | Mac | Windows |
|---|---|---|
| Selectionner tout | Cmd+A | Ctrl+A |
| Selectionner enfants | Enter | Enter |
| Remonter d'un niveau | Escape | Escape |
| Dupliquer | Cmd+D | Ctrl+D |
| Copier/Coller | Cmd+C/V | Ctrl+C/V |
| Copier proprietes | Cmd+Alt+C | Ctrl+Alt+C |
| Coller proprietes | Cmd+Alt+V | Ctrl+Alt+V |
| Grouper | Cmd+G | Ctrl+G |
| Ungrouper | Cmd+Shift+G | Ctrl+Shift+G |

### Creation

| Action | Mac | Windows |
|---|---|---|
| Frame | F | F |
| Rectangle | R | R |
| Cercle | O | O |
| Ligne | L | L |
| Texte | T | T |
| Pen | P | P |
| Image | Cmd+Shift+K | Ctrl+Shift+K |

### Organisation

| Action | Mac | Windows |
|---|---|---|
| Auto Layout | Shift+A | Shift+A |
| Component | Cmd+Alt+K | Ctrl+Alt+K |
| Align left | Alt+A | Alt+A |
| Align right | Alt+D | Alt+D |
| Align top | Alt+W | Alt+W |
| Align bottom | Alt+S | Alt+S |
| Distribute horizontal | Alt+Shift+H | Alt+Shift+H |

---

## Erreurs Courantes et Solutions

### "Je ne trouve pas comment modifier le texte d'un composant"

Le texte est protege si vous avez selectionne une propriete de component en lecture seule. **Solution** : double-cliquer pour entrer dans le composant, ou selectionner l'instance (pas le master) et editer le texte directement dans l'instance.

### "Mon element ne s'aligne pas correctement"

Verifier si vous etes dans un Auto Layout. Si oui, l'alignement est controle par le container. **Solution** : modifier les proprietes du container Auto Layout (alignment, spacing), pas l'element lui-meme.

### "Le prototype ne s'anime pas correctement"

Smart Animate requiert que les layers aient le MEME NOM dans les deux ecrans. **Solution** : verifier que les layers des deux frames ont des noms identiques.

### "Mes exportations sont floues"

Exporter en resolution insuffisante. **Solution** : exporter en PNG 2x ou 3x pour les ecrans retina, ou en SVG pour les icones et illustrations vectorielles.

### "Le fichier est lent"

Trop d'images lourdes ou de composants complexes. **Solutions** :
- Utiliser "Flatten" (Cmd+E) pour simplifier les vecteurs complexes
- Reduire la resolution des images importees (max 1440px de large pour les hero images)
- Fermer les pages inutilisees
