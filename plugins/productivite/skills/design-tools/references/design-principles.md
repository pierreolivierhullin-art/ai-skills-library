# Principes de Design Visuel — Theorie et Pratique

## Vue d'Ensemble

La difference entre un visuel "amateur" et un visuel "professionnel" n'est souvent pas une question d'outil ou de talent inne — c'est une question de principes appliques. Ce document couvre les fondements theoriques du design visuel que tout professionnel peut apprendre et appliquer : composition, typographie, couleurs, hierarchie et accessibilite.

---

## Les 4 Principes CRAP (Robin Williams)

Robin Williams (auteur de "The Non-Designer's Design Book") a formalise 4 principes fondamentaux applicables par n'importe qui.

### 1. Contrast (Contraste)

**Principe** : si deux elements ne sont pas identiques, les rendre clairement differents. Le contraste cree la hierarchie et guide l'attention.

**Applications** :
- **Couleur** : texte fonce sur fond clair (ou inverse). Ne jamais choisir des couleurs similaires pour des elements distincts.
- **Taille** : le titre doit etre significativement plus grand que le corps de texte (ratio minimum 1.5x, ideal 2x ou plus).
- **Graisse** : meler Regular et Bold pour distinguer les niveaux d'importance.
- **Style** : serif vs sans-serif, rempli vs contour.
- **Forme** : rectangulaire vs rond, horizontal vs vertical.

**Erreur commune** : timidite du contraste — choisir des couleurs legeremet differentes pensant que "ca passe". Aller jusqu'au bout : si vous faites un contraste, rendez-le evident.

**Test du contraste** : floutez mentalement votre design. La hierarchie est-elle toujours lisible ? Les elements importants ressortent-ils ? Si non, augmenter le contraste.

### 2. Repetition (Coherence)

**Principe** : repeter des elements visuels tout au long du design pour creer une unite visuelle. C'est la base du "brand kit".

**Elements a repeter** :
- Meme palette de couleurs (3-5 couleurs maximum)
- Meme paires de polices (2 maximum)
- Meme style d'icones (tout rempli, tout contour, ou tout duotone)
- Meme style de photos (toutes en noir et blanc, ou toutes avec filtre chaud)
- Meme style de formes (tous angles arrondis, ou tous angulaires)
- Meme espacement entre les elements equivalents

**Pourquoi c'est important** : la repetition cree la reconnaissance. Un spectateur qui voit votre 5eme post LinkedIn reconnait immediatement votre marque avant de lire le texte.

**Cas d'usage** : campagne multi-formats. Creer un "mood board" avec les elements repetables, puis les appliquer sur chaque format (post, story, banniere, flyer).

### 3. Alignment (Alignement)

**Principe** : aucun element ne doit etre place "a l'oeil". Chaque element doit etre aligne visuellement avec quelque chose d'autre sur la page.

**Types d'alignement** :
- **Alignement a gauche** : le plus naturel pour la lecture en langues occidentales. Cree une ligne verticale claire a gauche.
- **Alignement centre** : pour les designs symetriques (couvertures, cartes de visite). A eviter pour de longs textes.
- **Alignement a droite** : pour les legendes, dates, numeros — quand le contexte le justifie.
- **Alignement de grille** : utiliser une grille systematique (8, 12 ou 16 colonnes).

**La grille de 8px** : espace toujours les elements par multiples de 8px (8, 16, 24, 32, 48, 64px). Cette discipline cree une harmonie visuelle mathematique.

**Erreur commune** : centrer systematiquement tout le texte parce que "ca parait equilibre". Le centrage est difficile a lire sur plusieurs lignes et cree des blocs irreguliers. Privilegier l'alignement a gauche pour les paragraphes.

### 4. Proximity (Proximite)

**Principe** : les elements lies doivent etre proches les uns des autres. Les elements non lies doivent etre espaces. La proximite cree des groupes logiques.

**Applications** :
- Le titre d'un article doit etre plus proche du debut de l'article que de la fin de l'article precedent.
- L'icone d'un lien doit etre collte au texte du lien.
- Les metriques d'un meme KPI (valeur + label + variation) doivent former un groupe dense, separe des autres KPIs.

**Test de la proximite** : masquez les titres et labels. Est-ce que les groupes d'elements sont encore compréhensibles par leur seule position ? Si oui, la proximite est bien appliquee.

---

## Hierarchie Visuelle

La hierarchie visuelle est l'ordre dans lequel l'oeil parcourt une composition. Un bon design guide l'oeil du plus important vers le moins important.

### Les 7 outils de la hierarchie

**1. Taille** : le plus grand attire l'oeil en premier. Ratio recommande : titre 3-4x plus grand que le corps.

**2. Couleur** : les couleurs saturees attirent avant les couleurs neutres. Une seule couleur vive dans un design de neutres devient automatiquement le point focal.

**3. Contraste** : noir sur blanc attire plus que gris sur blanc. Plus le contraste est eleve, plus l'element ressort.

**4. Position** : dans les cultures occidentales, l'oeil scanne de gauche a droite, de haut en bas. Le coin superieur gauche est "prime real estate".

**5. Espace blanc** : entourer un element d'espace vide lui donne de l'importance. Le texte entoure de "air" parait plus premium.

**6. Alignement** : les elements centres ou isoles attirent plus l'attention que les elements integres dans un bloc.

**7. Repetition contextuelle** : le premier element d'une serie attire l'attention (le premier point d'une liste, le premier item d'un carousel).

### Niveaux de hierarchie

Un design professionnel a 3 niveaux maximum :

| Niveau | Role | Implementation |
|---|---|---|
| **Niveau 1 — Dominant** | L'element principal (un seul) | Taille maximale, couleur d'accent, position prominente |
| **Niveau 2 — Support** | 2-3 elements importants | Taille moyenne, couleur secondaire ou neutre fonce |
| **Niveau 3 — Details** | Tout le reste | Petite taille, gris moyen, position secondaire |

**Erreur commune** : vouloir que tout soit important → rien ne l'est. "Quand tout est gras, rien n'est gras."

---

## Typographie Appliquee

### Anatomie d'une police

- **Serif** : les polices avec des "empattements" (petits traits aux extremites des lettres). Ex : Times New Roman, Georgia, Merriweather. Connotation : tradition, confiance, editorial.
- **Sans-serif** : les polices sans empattements. Ex : Helvetica, Inter, Open Sans. Connotation : modernite, tech, accessibilite.
- **Monospace** : largeur fixe par caractere. Ex : Courier, Fira Code. Usage : code, donnees tabulaires.
- **Display** : polices decoratives pour les titres uniquement. Ex : Lobster, Bebas Neue.

### Regles typographiques fondamentales

**Espacement des lignes (line height)** :
- Corps de texte : 1.4 a 1.6x la taille de police (16px → 22-25px de line height)
- Titres : 1.1 a 1.3x (tighter car moins de lignes)
- Ne jamais utiliser le line height par defaut (1.0) sur le corps de texte → illisible

**Espacement des lettres (letter spacing / tracking)** :
- Corps : 0 (par defaut) — ne jamais agrandir le tracking sur le corps
- Titres : -0.5 a -1% — les grands titres beneficient d'un tracking negatif (plus serres)
- MAJUSCULES et labels : +0.05 a +0.1em — les majuscules respirent mieux espaces

**Longueur de ligne (measure)** :
- Ideal : 60-80 caracteres par ligne pour le confort de lecture
- Maximum : 90-100 caracteres
- Minimum : 45-50 caracteres

**Alignement du texte** :
- Corps de texte : alignement a gauche (jamais justifie sauf avec trait de coupure automatique)
- Titres courts (< 4 mots) : centre ou gauche selon la composition
- Legendes : gauche ou alignees avec l'element qu'elles decrivent

### Paires de polices — Logique de selection

**Principe du contraste typographique** : choisir deux polices suffisamment differentes pour creer un contraste, mais suffisamment harmonieuses pour coexister.

**Combiner serif + sans-serif** : la combinaison classique. Le serif pour les titres cree un ancrage et une personnalite ; le sans-serif pour le corps assure la lisibilite.

**Combiner deux sans-serif** : fonctionne si les polices ont des "personnalites" differentes (une geometrique + une humaniste). Exemple : Montserrat (geometrique, fort) + Open Sans (humaniste, doux).

**Ne jamais combiner** :
- Deux serifs differents (confusion)
- Deux polices similaires (pas de contraste, pas de raison d'etre)
- Des polices "display" decoratives pour le corps de texte

**Ressource** : fontpair.co — paires de Google Fonts validees avec preview en temps reel.

---

## Theorie des Couleurs

### Modeles de couleurs

**RVB (RGB)** : pour les ecrans. Valeurs de 0-255 pour rouge, vert, bleu. Additive : blanc = toutes couleurs au maximum.

**CMJN (CMYK)** : pour l'impression. Cyan, Magenta, Jaune, Noir. Soustractif : blanc = aucune encre.

**HSL (Hue, Saturation, Lightness)** : le plus intuitif pour choisir des couleurs. Teinte (0-360°), Saturation (0-100%), Luminosite (0-100%). Utiliser HSL dans les design tools pour creer des palettes harmonieuses.

**Hex** : notation hexadecimale (#RRGGBB). Standard web. Ex : #0052CC = bleu Atlassian.

### Harmonies de couleurs

**Complementaires** : couleurs opposees sur le cercle chromatique (bleu + orange, rouge + vert). Fort contraste, impact visuel maximum. Usage : CTAs, accents sur fond neutre.

**Analogues** : couleurs voisines sur le cercle (bleu + bleu-vert + vert). Harmonie naturelle, apaisante. Usage : palettes principales de marque.

**Triadiques** : 3 couleurs equidistantes sur le cercle (rouge + jaune + bleu). Dynamique et colore. Difficile a equilibrer.

**Monochromatique** : variations de teinte, saturation et luminosite d'une seule couleur. Elegant, coherent, safe. Ajouter 1 couleur d'accent pour les CTAs.

**Split-complementaire** : une couleur + les deux couleurs adjacentes a son complementaire. Moins tendu que le complementaire pur, plus dynamique que l'analogique.

### Psychologie des couleurs (contexte B2B et Europe)

| Couleur | Connotation principale | Usages typiques |
|---|---|---|
| **Bleu** | Confiance, professionnalisme, tech | Finance, SaaS, consulting, sante |
| **Vert** | Croissance, durabilite, sante | Banque verte, agro, sante, sustainability |
| **Orange** | Energie, chaleur, urgence | CTA, e-commerce, secteur createur |
| **Rouge** | Urgence, danger, passion | Alertes, promotions, secteur foodtech |
| **Violet** | Creativite, premium, innovation | Luxe, tech, bien-etre |
| **Noir** | Luxe, autorite, sophistication | Luxe, mode, premium B2C |
| **Gris** | Neutralite, professionnalisme | Fond, texte secondaire, tous secteurs |
| **Blanc** | Purete, espace, minimalisme | Fond, espace blanc, luxe |
| **Jaune** | Optimisme, energie, avertissement | Secteur constructif, FMCG |

### Construction d'une palette de marque

**Palette minimale viable** :
```
Primaire : votre couleur principale (1 teinte, 5-9 nuances de luminosite)
Secondaire : couleur complementaire ou analogique (1-2 teintes)
Accent : couleur vive pour les CTAs et alerts (souvent complementaire)
Neutrales :
  - Blanc (#FFFFFF ou #F8F9FA pour un blanc chaud)
  - Gris clair (#E5E7EB — fond de sections)
  - Gris moyen (#6B7280 — texte secondaire)
  - Gris fonce (#1F2937 — corps de texte)
  - (Optionnel) Noir (#0D1117 — titres et elements forts)
Semantiques :
  - Success : vert (#10B981 ou similaire)
  - Warning : orange/jaune (#F59E0B)
  - Error : rouge (#EF4444)
  - Info : bleu clair (#3B82F6)
```

**Outil** : coolors.co — generateur interactif avec verrouillage de couleurs. Exporter en CSS, SVG, ou image.

---

## Accessibilite Visuelle

### Contrastes (WCAG 2.1)

**Niveaux de conformite** :
- **AA (minimum requis)** : ratio 4.5:1 pour le texte normal (< 18pt), 3:1 pour le grand texte (≥ 18pt ou gras ≥ 14pt)
- **AAA (optimal)** : ratio 7:1 pour le texte normal, 4.5:1 pour le grand texte

**Outils de verification** :
- contrast.ratio.fyi (verifier deux couleurs)
- WebAIM Contrast Checker (accessible.me)
- Figma Plugins : "Contrast" ou "A11y - Color Contrast Checker"
- Canva : pas d'outil integre — verifier externellement

**Exemples de ratios** :
- Blanc sur noir : 21:1 (maximum)
- Texte gris fonce #333 sur blanc : 12.6:1 (AAA)
- Texte gris moyen #666 sur blanc : 5.7:1 (AA)
- Texte gris clair #999 sur blanc : 2.8:1 (echec AA — a eviter)

### Couleurs et handicaps visuels

**Daltonisme** (8% des hommes, 0.5% des femmes) : principalement confusion rouge/vert.

**Regles** :
1. Ne jamais transmettre une information UNIQUEMENT par la couleur
2. Toujours ajouter une icone, un label ou un pattern en complement
3. Tester le design en simulation daltonisme (Figma : View → Color Blind Simulation / Coblis en ligne)

**Exemple** : un graphique avec des barres "rouge = mauvais, vert = bon" → ajouter des icones (✗ et ✓) ou des labels textuels.

### Lisibilite pour les seniors

- Taille de police minimum 14px pour le corps (16px recommande)
- Contraste eleve (preferez AAA quand possible)
- Eviter les polices decoratives pour le corps de texte
- Eviter le text en italique sur de longs passages

---

## Espace Blanc et Respiration

L'espace blanc (ou espace negatif) est l'absence d'element. Il n'est pas "vide" — il est aussi important que les elements eux-memes.

### Fonctions de l'espace blanc

**Micro-espace blanc** : entre les lettres, les mots, les lignes. Affecte directement la lisibilite.

**Macro-espace blanc** : entre les sections, les blocs de contenu. Affecte la comprehension de la structure.

**Espace blanc actif** : deliberement utilise pour isoler un element et lui donner de l'importance. Un CTA entoure d'espace blanc attire plus l'attention qu'un CTA dans un bloc dense.

### La regle du 8px (spacing system)

Utiliser un systeme d'espacement base sur des multiples de 8 :
- 4px : espacement minimal (entre icone et label)
- 8px : espacement interne d'un composant
- 16px : espacement entre elements dans une section
- 24px : espacement entre composants
- 32px : espacement entre sections legeres
- 48px : espacement entre sections majeures
- 64px : espacements de section sur desktop
- 96px ou + : sections heroiques sur desktop

**Pourquoi des multiples de 8** : divisible en 4, 2, 1 — la plupart des ecrans (iPhone, Android, Mac Retina) ont des densites de pixels qui s'alignent sur ces valeurs.

---

## Composition et Mise en Page

### La regle des tiers

Diviser la composition en 9 zones egales (grille 3x3). Placer les elements cles aux intersections ou le long des lignes de cette grille.

**Application** : pour les photos heroiques, positionner le sujet principal sur une intersection de la grille des tiers plutot qu'exactement au centre. Cree naturellement plus de dynamisme.

### Le nombre d'or (Golden Ratio)

Rapport approximatif de 1.618. Se retrouve dans la nature et est percu comme inheremment harmonieux.

**Application pratique** :
- Sidebar : 38% du layout, contenu principal : 62%
- Titre : si le corps est en 16px, le titre en 26px (16 × 1.618 ≈ 26)
- Canva et Figma ont des fonctionnalites de grilles — utiliser le rapport 5:8 (approximation du nombre d'or)

### Composition en Z et en F

**Composition en Z** : l'oeil suit un "Z" naturellement sur une composition non-texte. Placer les elements cles aux extremites du Z : coin superieur gauche (logo/titre), coin superieur droit (sous-titre ou info), coin inferieur gauche (info secondaire), coin inferieur droit (CTA).

**Composition en F** : pour les pages riches en texte, l'oeil lit les deux premieres lignes en entier, puis scanne verticalement en lisant le debut de chaque ligne. Placer les informations cles a gauche et en debut de ligne.

### Grilles de mise en page

**12 colonnes** : le standard web (Bootstrap, Tailwind). Permet 2 colonnes (6+6), 3 colonnes (4+4+4), asymetrique (8+4), etc.

**8 colonnes** : pour les interfaces de contenu pur (articles, documentations).

**4 colonnes** : pour mobile.

**Dans Canva** : Elements → Grids. Choisir la disposition, puis faire glisser les images dans les cellules.

**Dans Figma** : Frame → Layout grid (panneau droit). Configurer le nombre de colonnes, le gutter et les marges.
