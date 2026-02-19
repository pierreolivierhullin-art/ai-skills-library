---
name: design-tools
version: 1.0.0
description: >
  Use this skill when the user asks about "Figma", "Canva", "Adobe Express", "design for non-designers", "visual design tools", "brand kit", "creating visuals", "presentation design", "social media graphics", "infographic creation", "color palette", "typography for business", "logo creation", "banner design", "marketing visuals", "design templates", "visual hierarchy", "brand consistency", discusses creating professional visual content without a design background, or needs guidance on choosing and using visual design tools for business communication.
---

# Design Tools — Figma, Canva & Creation Visuelle pour Non-Designers

## Overview

La creation visuelle n'est plus l'apanage des designers professionnels. Les outils actuels permettent a tout professionnel de creer des visuels de qualite pour leurs presentations, communications marketing, reseaux sociaux et documents internes — a condition de comprendre quelques principes de base et de choisir l'outil adapte a son usage.

**La democratisation du design** : Canva (2013) puis Figma (acquis par Figma en 2012, devenu standard UX en 2020) ont rendu le design professionnel accessible. Mais l'outil ne remplace pas la culture visuelle : des principes de base (hierarchie, contraste, espace, coherence) font la difference entre un visuel amateur et un visuel professionnel.

**Distinction critique entre les outils** :
- **Figma** : outil professionnel de UI/UX design et de prototypage. Courbe d'apprentissage significative. Indispensable pour les equipes produit et design.
- **Canva** : outil de creation de contenu marketing. Accessible en 10 minutes. Ideal pour les non-designers.
- **Adobe Express** : positionnement similaire a Canva mais avec l'ecosysteme Adobe. Avantage : integration avec Photoshop/Illustrator.
- **Microsoft Designer** : nouvelle entree alimentee par l'IA generative, integree a Microsoft 365.

**Ce que ce skill couvre** :
- Principes fondamentaux du design visuel
- Figma pour les product/project managers et non-designers
- Canva pour la communication marketing et les equipes business
- Creation d'une identite visuelle coherente sans designer
- AI-assisted design (2024-2026)

## Core Principles — Les 4 Piliers du Design (CRAP)

### 1. Contrast (Contraste)
Les elements importants doivent se distinguer clairement des elements secondaires. Le contraste cree la hierarchie visuelle. Il s'applique a : la couleur (clair/fonce), la taille (grand/petit), le style (gras/normal), la forme (rond/angulaire).

**Erreur commune** : trop de couleurs vives, tout au meme niveau — rien ne ressort. Solution : 1-2 couleurs d'accent maximum, le reste en neutre.

### 2. Repetition (Coherence)
Repeter les elements visuels (couleurs, polices, icones, styles) pour creer une coherence. Ce principe est la base du "brand kit". La repetition cree la reconnaissance.

**Regie pratique** : maximum 2 polices (1 pour les titres, 1 pour le corps de texte). Maximum 3-4 couleurs de marque. Toujours le meme style d'icones (tous remplis, tous en contour — pas de mix).

### 3. Alignment (Alignement)
Chaque element doit etre aligne visuellement avec un autre. Eviter les placements "a l'oeil" : utiliser les guides et les grilles. Un alignement rigoureux donne une impression de professionnalisme.

**Erreur commune** : text et images non alignes, marges inconsistantes. Solution : activer les guides dans Canva/Figma, utiliser la grille 12 colonnes.

### 4. Proximity (Proximite)
Les elements lies doivent etre proches. Les elements non lies doivent etre espaces. La proximite cree des groupes logiques qui guident l'oeil.

**Application** : titre + sous-titre proches, puis espace important avant le premier paragraphe. Les metriques d'un meme groupe proches, avec une separation claire d'un autre groupe.

## Typographie pour Non-Designers

### Hierarchie typographique (3 niveaux)
- **H1 - Titre principal** : 32-48px, gras, couleur principale ou neutre fonce
- **H2 - Sous-titre** : 20-28px, semi-gras, couleur secondaire ou gris fonce
- **Corps** : 14-16px, regular, gris fonce (#333333 — pas noir pur #000000)
- **Caption** : 11-12px, gris clair, pour les legendes et metadonnees

### Paires de polices qui fonctionnent

| Titre | Corps | Style |
|---|---|---|
| **Playfair Display** | Source Sans Pro | Elegant, editorial |
| **Montserrat** | Open Sans | Moderne, tech |
| **Merriweather** | Lato | Confiance, finance |
| **Inter** | Inter | Minimaliste, SaaS |
| **Raleway** | Roboto | Dynamic, startup |

**Regle d'or** : 1 serif + 1 sans-serif, ou 2 sans-serif de meme famille. Ne jamais combiner 2 serifs.

## Theorie des Couleurs (Minimum Viable)

### Modele de couleurs d'une marque

**Couleur primaire** : la couleur principale de la marque (ex: bleu #0052CC)
**Couleur secondaire** : complementaire ou analogique (ex: indigo #2D3748)
**Couleur d'accent** : pour les CTAs et elements importants (ex: orange #FF6B35)
**Neutrales** : blanc, noir, gris (#F7F7F7, #333333, #666666)

### Outils de generation de palettes

- **Coolors.co** : generateur avec verrouillage de couleurs
- **Adobe Color** : harmonies (complementaire, triadique, analogique)
- **Huemint** : AI-powered, genere des palettes contextualisees
- **Canva Color Palette Generator** : a partir d'une image

### Accessibilite des couleurs

Respecter un ratio de contraste minimum : 4.5:1 pour le texte normal, 3:1 pour les grands titres (WCAG AA). Tester avec : contrast.ratio.fyi ou l'outil d'accessibilite Figma.

Ne jamais transmettre une information uniquement par la couleur (ex: vert = bon, rouge = mauvais) — ajouter une icone ou un label.

## Figma — Guide du Non-Designer

### Concepts fondamentaux

**Frames** : conteneurs analogues a des "pages" ou "ecrans". Toujours travailler dans une frame (Cmd+A pour selectionner tout, Alt+Cmd+G pour grouper dans une frame).

**Auto Layout** : systeme qui gere automatiquement l'espacement et l'alignement. Indispensable pour les composants reutilisables. Raccourci : Shift+A.

**Components** : elements reutilisables (bouton, carte, icone). Modifier le composant principal met a jour toutes les instances. Cree en appuyant sur Cmd+Alt+K.

**Styles** : couleurs, typographies et effets enregistres et partages. La base du design system. Permet de changer une couleur partout en un clic.

### Workflow pour un non-designer

**1. Commencer par un template** : Figma Community (figma.com/community) offre des milliers de templates gratuits. Chercher : "presentation template", "dashboard wireframe", "mobile app kit".

**2. Brand kit dans Figma** :
```
Fichier: Brand-Kit.fig
├── Colors (styles de couleurs)
│   ├── Primary/Blue-600
│   ├── Secondary/Indigo-700
│   ├── Accent/Orange-500
│   └── Neutral/Gray-xxx (50, 100, 200, 400, 600, 900)
├── Typography (styles de texte)
│   ├── Heading/H1, H2, H3
│   ├── Body/Regular, Small
│   └── Caption
└── Components
    ├── Buttons (Primary, Secondary, Ghost)
    ├── Cards
    └── Icons
```

**3. Raccourcis essentiels Figma**

| Action | Raccourci Mac | Raccourci Windows |
|---|---|---|
| Frame | F | F |
| Auto Layout | Shift+A | Shift+A |
| Component | Cmd+Alt+K | Ctrl+Alt+K |
| Group | Cmd+G | Ctrl+G |
| Duplicate | Cmd+D | Ctrl+D |
| Scale proportionnel | Shift+drag | Shift+drag |
| Align (panel) | Option bar | Option bar |
| Color picker | I | I |

### Figma AI (2024-2026)

- **Make Design** : generer un design a partir d'une description textuelle
- **Rename layers** : nommage automatique des calques avec l'IA
- **Remove background** : suppression d'arriere-plan integree
- **First Draft** : prototypage rapide assiste par IA

## Canva — Guide Pratique

### Organisation d'un espace de travail Canva (Team)

```
Brand Hub
├── Logo (versions : couleur, blanc, noir, icone)
├── Couleurs de marque
├── Polices de marque (telechargees si custom)
└── Kit de templates (partage avec l'equipe)

Dossiers de contenu
├── Social Media
│   ├── LinkedIn (1200x627, 1080x1080)
│   ├── Instagram (1080x1080, Stories 1080x1920)
│   └── Twitter/X (1600x900)
├── Presentations
│   ├── Template interne (16:9)
│   └── Pitch deck clients
└── Print
    ├── Flyers (A4, A5)
    └── Roll-up (85x200cm)
```

### Les fonctionnalites Canva les plus sous-utilisees

**Background Remover** (Pro) : suppression d'arriere-plan en 1 clic sur les photos.

**Magic Resize** : adapter un visuel a tous les formats en 1 clic (LinkedIn post → LinkedIn story → Twitter).

**Brand Kit** (Pro/Team) : sauvegarder couleurs, polices et logos — appliques en 1 clic a n'importe quel template.

**Canva AI (Magic Studio)** :
- **Text to Image** : generer des visuels a partir d'un prompt
- **Magic Write** : rediger du texte directement dans Canva
- **Magic Edit** : modifier une partie d'une image avec un prompt
- **Translate** : traduire automatiquement les textes du design

### Checklist visuel avant publication

- [ ] Toutes les polices appartiennent au brand kit (pas de restes de template)
- [ ] Ratio de contraste texte/fond suffisant (> 4.5:1)
- [ ] Pas de texte sur fond photographie sans overlay semi-transparent
- [ ] Resolution export : JPG 80% pour web, PNG pour transparence, PDF pour print
- [ ] Format verifie selon la plateforme de publication
- [ ] Nom du fichier coherent : AAAA-MM-JJ_type-visuel_sujet.ext

## Decision Guide — Quel Outil pour Quel Usage

| Usage | Outil recommande | Raison |
|---|---|---|
| Post LinkedIn / Instagram | Canva | Templates, Magic Resize, facile |
| Presentation interne | Canva ou PowerPoint | Templates pro, collaboration |
| Pitch deck investisseurs | Figma ou Canva Pro | Design premium, templates investissement |
| Wireframe application | Figma | Standard industrie, prototypage |
| Design system / Composants | Figma | Uniquement outil adapte |
| Flyer / Print | Canva | Export PDF haute resolution |
| Infographie complexe | Canva ou Adobe Illustrator | Templates infographie dans Canva |
| Landing page design | Figma | Handoff dev avec Figma Dev Mode |

## AI-Assisted Design (2024-2026)

- **Midjourney / DALL-E 3 / Ideogram** : generation d'images pour les visuels (photos, illustrations)
- **Adobe Firefly** : integre nativement dans Adobe Express et Photoshop, entraine sur donnees licenciees
- **Canva Magic Studio** : suite AI complete integree a Canva (text to image, edit, translate, write)
- **Figma AI** : generation de designs, renommage de calques, suggestions de composants
- **Gamma.app** : generation de presentations entiere a partir d'un prompt — alternative rapide a Canva pour les presentations

**Workflow AI typique (non-designer)** :
1. Prompt Midjourney pour les images heroiques
2. Canva pour assembler avec les templates et brand kit
3. Magic Resize pour adapter aux formats
4. Export et publication

## Maturity Model — Design Visuel

| Niveau | Caracteristique |
|---|---|
| **1 — Ad hoc** | Word/PPT par defaut, aucune coherence visuelle |
| **2 — Conscient** | Canva utilise, quelques templates, brand inconsistant |
| **3 — Coherent** | Brand kit Canva, templates partages, principes CRAP appliques |
| **4 — Systematique** | Library de composants, Figma pour les projets cles, AI integree |
| **5 — Design-Led** | Design system partage, designers et non-designers collaborent sur Figma |

## Limites

- Canva ne remplace pas un designer pour les projets complexes (identite de marque from scratch, packaging, illustrations sur-mesure)
- Figma a une courbe d'apprentissage significative pour les non-designers — prevoir 20-40h de pratique pour etre autonome
- L'IA generative produit des images avec des artefacts (mains incorrectes, texte illisible) — verifier systematiquement
- Les templates Canva sont utilises par des milliers d'entreprises — personnaliser suffisamment pour sortir du lot
- Le droit d'auteur des images AI est encore non-clarifie dans de nombreuses juridictions — preferer Adobe Firefly (entraine sur donnees licenciees) pour un usage commercial
