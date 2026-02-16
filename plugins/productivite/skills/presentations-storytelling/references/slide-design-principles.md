# Principes de Design de Slides — Typographie, Couleurs, Layout, Hierarchie Visuelle

## Overview

Ce document de reference couvre les principes fondamentaux du design de slides pour creer des presentations visuellement efficaces et professionnelles. Utiliser ce guide comme fondation pour chaque decision de design, de la selection typographique a l'optimisation des layouts. Un design de slide reussi n'est pas une question d'esthetique decorative : c'est l'application rigoureuse de principes visuels qui servent le message. Chaque choix de couleur, de police, d'espacement et de placement doit etre justifiable par sa contribution a la clarte et a l'impact du contenu.

---

## Typographie pour Slides

### Principes fondamentaux

La typographie est l'element de design le plus critique dans une presentation. Elle represente 80% de la communication visuelle d'une slide. Les regles typographiques pour les slides different significativement de celles du print ou du web :

- **Lisibilite a distance** : le texte doit etre lisible a 3 metres minimum. Corps de texte minimum 18pt, titres minimum 28pt, sous-titres minimum 22pt. En salle de conference large, augmenter de 20-30%.
- **Contraste** : le rapport de contraste minimum entre le texte et le fond doit etre de 4.5:1 (norme WCAG AA). Texte sombre sur fond clair ou texte clair sur fond sombre. Eviter le texte gris moyen sur fond blanc.
- **Espacement** : l'interligne (line-height) doit etre de 1.3 a 1.5 pour le corps de texte en slide. Un interligne trop serre rend la lecture penible a distance.
- **Longueur de ligne** : limiter a 8-10 mots par ligne. Au-dela, l'oeil perd le fil en changeant de ligne, surtout a distance.

### Hierarchie typographique a trois niveaux

Definir exactement 3 niveaux typographiques pour maintenir la clarte :

| Niveau | Role | Taille recommandee | Graisse | Exemple |
|---|---|---|---|---|
| **Niveau 1 — Titre** | Message cle de la slide (action title) | 28-36pt | Bold / Semibold | "Nos revenus ont progresse de 40% au T3" |
| **Niveau 2 — Sous-titre / Label** | Categorie, legende, sous-section | 20-24pt | Medium / Regular | "Revenue par segment, en M EUR" |
| **Niveau 3 — Corps / Annotation** | Detail, source, annotation | 16-20pt | Regular / Light | "Source : rapport annuel 2025, perimetre constant" |

Ne jamais utiliser plus de 3 niveaux sur une meme slide. Si un quatrieme niveau est necessaire, c'est le signe que la slide porte trop d'information.

### Choix et appariement de polices (Font Pairing)

#### Regles de selection

- **Maximum 2 familles de polices** par presentation : une pour les titres, une pour le corps. Utiliser les variantes de graisse (Bold, Regular, Light) pour creer la hierarchie plutot que de multiplier les polices.
- **Privilegier les sans-serif** pour les slides : elles sont plus lisibles a distance et sur ecran. Les serif sont acceptables pour les titres si l'identite de marque l'exige.
- **Eviter les polices decoratives, manuscrites ou condensees** pour le corps de texte. Elles sont acceptables uniquement pour des titres courts et de grande taille.

#### Combinaisons recommandees (2025-2026)

| Usage | Police titre | Police corps | Style |
|---|---|---|---|
| **Corporate moderne** | Inter Bold | Inter Regular | Neutre, professionnel, excellent rendering |
| **Startup tech** | Space Grotesk Bold | DM Sans Regular | Geometrique, contemporain |
| **Executive premium** | Playfair Display Bold | Source Sans 3 Regular | Elegant, serif + sans-serif |
| **Accessible universel** | Atkinson Hyperlegible Bold | Atkinson Hyperlegible Regular | Concu pour la lisibilite maximale |
| **Microsoft ecosystem** | Aptos Display Bold | Aptos Regular | Police par defaut Office 2024+ |
| **Google ecosystem** | Google Sans Bold | Roboto Regular | Natif Google Slides |

#### Polices a eviter

- **Comic Sans** : percu comme non-professionnel dans tout contexte business
- **Papyrus** : associe a l'amateurisme
- **Times New Roman** : connotation "document Word par defaut"
- **Arial** : generique et sans caractere, preferer des alternatives modernes comme Inter ou Roboto
- **Polices condensees** (Arial Narrow, etc.) pour le corps de texte : reduction de lisibilite

### Regles typographiques complementaires

- **Ne jamais utiliser de texte entierement en majuscules** pour plus de 5 mots consecutifs. Les majuscules reduisent la lisibilite de 13-18% car elles suppriment la forme distinctive des mots (ascendantes/descendantes).
- **Italique avec parcimonie** : reserve pour les citations, les termes etrangers ou l'emphase legere. Jamais pour des blocs de texte entiers.
- **Souligne a proscrire** : dans un contexte digital, le souligne est associe aux liens hypertexte. Utiliser le gras ou la couleur pour l'emphase.
- **Alignement a gauche** pour le corps de texte. L'alignement justifie cree des espaces irreguliers difficiles a lire a distance. L'alignement centre est reserve aux titres courts et aux citations.

---

## Theorie des Couleurs pour Presentations

### Construction d'une palette de presentation

Une palette de presentation efficace contient exactement 5 couleurs avec des roles definis :

| Role | Fonction | Exemple |
|---|---|---|
| **Primaire** | Couleur dominante de la marque, utilisee pour les titres et elements d'accent principaux | Bleu fonce (#1A365D) |
| **Secondaire** | Couleur complementaire pour les elements secondaires et les variantes | Bleu moyen (#3182CE) |
| **Accent** | Couleur de contraste pour les call-to-action, les donnees cles, les mises en avant | Orange (#ED8936) ou Vert (#38A169) |
| **Neutre sombre** | Texte principal, bordures | Gris anthracite (#2D3748) |
| **Neutre clair** | Fonds, zones secondaires | Gris tres clair (#F7FAFC) ou blanc (#FFFFFF) |

### Contraste et accessibilite

- **Ratio de contraste minimum** : 4.5:1 pour le texte normal, 3:1 pour le texte large (> 18pt bold). Verifier avec des outils comme WebAIM Contrast Checker ou Stark.
- **Ne pas utiliser la couleur seule pour communiquer l'information** : 8% des hommes sont daltoniens. Toujours combiner couleur + forme (icone, pattern, label textuel). Un graphique en rouge/vert sans annotations est illisible pour 1 personne sur 12.
- **Simuler la vision daltonienne** : utiliser les filtres de simulation (Figma, PowerPoint Accessibility Checker) pour verifier que les distinctions de couleur restent perceptibles.

### Fonds de slide : clair vs sombre

| Critere | Fond clair (blanc/gris) | Fond sombre (bleu fonce/noir) |
|---|---|---|
| **Lisibilite** | Excellente en salle eclairee | Superieure en salle sombre ou projection |
| **Impression** | Optimale (moins d'encre) | A eviter (consommation d'encre) |
| **Perception** | Professionnel, corporate | Premium, moderne, impactant |
| **Fatigue visuelle** | Moindre pour des presentations longues | Peut fatiguer sur des sessions longues |
| **Usage recommande** | Presentations de travail, rapports, formation | Keynotes, pitchs, conferences, demos |

Regle generale : choisir un fond et s'y tenir pour l'ensemble de la presentation. Les transitions entre fond clair et fond sombre sont acceptables uniquement pour marquer un changement de section majeur.

### Codage couleur semantique

Definir un code couleur coherent et le maintenir dans toute la presentation :

- **Vert** : positif, croissance, objectif atteint, validation
- **Rouge** : negatif, decroissance, alerte, rejet
- **Orange / Ambre** : attention, en cours, risque modere
- **Bleu** : neutre, informatif, reference
- **Gris** : contexte, benchmark, historique, desactive

Ne jamais changer la signification d'une couleur en cours de presentation. Si le vert signifie "objectif atteint" sur la slide 5, il doit signifier la meme chose sur la slide 25.

---

## Layout et Systemes de Grille

### Principes de mise en page

La mise en page d'une slide repose sur trois principes fondamentaux :

1. **Alignement** : chaque element doit etre aligne avec au moins un autre element. L'alignement cree de l'ordre visuel et du professionnalisme. Utiliser les guides d'alignement de l'outil (PowerPoint : afficher les guides de dessin, Google Slides : guides personnalises).
2. **Proximite** : les elements lies sont proches, les elements distincts sont espaces. La proximite cree des groupes logiques visuels qui facilitent la comprehension sans avoir besoin de bordures ou de cadres.
3. **Repetition** : les memes elements visuels (couleurs, formes, icones) sont reutilises pour creer la coherence. La repetition permet au regard de trouver rapidement les patterns.

### Grille de 12 colonnes

La grille de 12 colonnes est le systeme le plus flexible pour les slides :

```
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│1│2│3│4│5│6│7│8│9│10│11│12│
└─┴─┴─┴─┴─┴─┴─┴─┴─┴──┴──┴──┘
```

Configurations courantes :
- **Pleine largeur** : 12 colonnes — pour les titres, les images, les declarations
- **2 colonnes egales** : 6+6 — comparaisons, avant/apres, texte + image
- **1/3 + 2/3** : 4+8 — texte court + graphique large, ou sidebar + contenu
- **3 colonnes** : 4+4+4 — trois points cles, trois KPIs, trois options
- **4 colonnes** : 3+3+3+3 — timeline, processus en 4 etapes

### Regle des tiers

Diviser mentalement la slide en 9 zones (3x3). Placer les elements cles sur les intersections des lignes de tiers (les 4 points forts). L'oeil humain est naturellement attire vers ces zones :

```
┌───────────┬───────────┬───────────┐
│           │     ●     │           │
│     ●     │           │     ●     │
│           │           │           │
├───────────┼───────────┼───────────┤
│           │           │           │
│     ●     │           │     ●     │
│           │     ●     │           │
├───────────┼───────────┼───────────┤
│           │           │           │
│     ●     │           │     ●     │
│           │     ●     │           │
└───────────┴───────────┴───────────┘
● = Points forts visuels (intersections)
```

### Safe Zone (Zone de securite)

Toujours maintenir une marge de securite de 5% sur chaque cote de la slide. Les projecteurs, ecrans et cadres video (Zoom, Teams) coupent les bords. Aucun texte ni element important ne doit se trouver dans cette zone. Dans PowerPoint 16:9, cela correspond a environ 60px de marge de chaque cote.

### Layouts de slides les plus efficaces

#### Layout 1 — Titre + Contenu pleine largeur
```
┌────────────────────────────────────┐
│  TITRE AFFIRMATIF COMPLET          │
│                                    │
│  ┌──────────────────────────────┐  │
│  │                              │  │
│  │    Graphique / Image /       │  │
│  │    Contenu principal         │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│  Source : ...                      │
└────────────────────────────────────┘
```

#### Layout 2 — Texte + Visuel (split screen)
```
┌────────────────────────────────────┐
│  TITRE AFFIRMATIF COMPLET          │
│                                    │
│  ┌──────────┐  ┌────────────────┐  │
│  │  Texte   │  │                │  │
│  │  cle     │  │   Image /      │  │
│  │  3-4     │  │   Graphique    │  │
│  │  lignes  │  │                │  │
│  └──────────┘  └────────────────┘  │
│                                    │
└────────────────────────────────────┘
```

#### Layout 3 — Trois colonnes (KPIs, comparaisons)
```
┌────────────────────────────────────┐
│  TITRE AFFIRMATIF COMPLET          │
│                                    │
│  ┌────────┐ ┌────────┐ ┌────────┐  │
│  │ [Icon] │ │ [Icon] │ │ [Icon] │  │
│  │  42%   │ │  €2.3M │ │  +15   │  │
│  │ Label  │ │ Label  │ │ Label  │  │
│  └────────┘ └────────┘ └────────┘  │
│                                    │
└────────────────────────────────────┘
```

---

## Hierarchie Visuelle

### Les 6 leviers de hierarchie

La hierarchie visuelle guide l'oeil du spectateur dans l'ordre souhaite. Six leviers sont disponibles, a combiner :

| Levier | Effet | Application en slide |
|---|---|---|
| **Taille** | Le plus grand attire l'oeil en premier | Titres > sous-titres > corps > annotations |
| **Contraste** | Le plus contraste attire l'oeil | Texte fonce sur fond clair, accent color sur fond neutre |
| **Couleur** | La couleur vive attire l'oeil sur un fond neutre | Couleur d'accent sur un seul element par slide |
| **Position** | Le haut-gauche est lu en premier (en Occident) | Titre en haut, CTA en bas-droite |
| **Espacement** | L'espace autour d'un element l'isole et l'met en valeur | White space genereux autour de la donnee cle |
| **Typographie** | Le gras, l'italique et la taille creent de la hierarchie | Bold pour les mots cles, regular pour le reste |

### Regle du point focal unique

Chaque slide doit avoir un point focal unique — l'element vers lequel l'oeil se dirige en premier. Ce point focal correspond au message cle de la slide. Verifier en plissant les yeux devant la slide : l'element le plus visible doit etre l'element le plus important.

Si deux elements se disputent l'attention, la slide a un probleme de hierarchie. Resoudre en :
- Augmentant la taille/contraste de l'element prioritaire
- Reduisant la taille/intensite de l'element secondaire
- Ajoutant du white space autour de l'element prioritaire

### Pattern de lecture en Z et en F

Sur les slides horizontales (16:9), l'oeil suit naturellement un pattern en Z :

```
1 ──────────────> 2
                  │
                  │
3 <────────────── ┘
│
└──────────────> 4
```

Placer les elements dans cet ordre de priorite : coin superieur gauche (point d'entree), coin superieur droit, coin inferieur gauche, coin inferieur droit (point de sortie / CTA).

Pour les slides avec beaucoup de texte (a eviter, mais parfois necessaire), l'oeil suit un pattern en F : lecture horizontale du titre, puis scanning vertical de la marge gauche.

---

## White Space et Respiration

### Principes du white space

Le white space (ou negative space) est l'espace vide entre les elements. Il n'est pas "gaspille" : il remplit des fonctions essentielles :

- **Separation** : il separe visuellement les groupes d'information sans avoir besoin de bordures ou de lignes
- **Emphase** : il isole et met en valeur les elements importants
- **Lisibilite** : il reduit la charge cognitive et facilite le scanning
- **Sophistication** : les presentations premium ont toujours plus de white space que les presentations amateurs

### Quantification du white space

- **Objectif** : 30 a 40% de chaque slide doit etre vide (ni texte, ni image, ni graphique)
- **Marges interieures** : minimum 10% de la largeur de slide comme padding autour du contenu
- **Espacement entre elements** : au minimum egal a la hauteur du texte le plus proche
- **Separation des sections** : au moins 2x l'espacement normal entre deux blocs logiques

### Test du "squint test"

Plisser les yeux devant la slide terminee. Si la slide apparait comme un bloc uniforme de contenu, il n'y a pas assez de white space. Les elements importants doivent etre visuellement distincts meme a travers les yeux plisses.

---

## Iconographie et Imagerie

### Icones

- **Coherence stylistique** : utiliser un seul jeu d'icones pour toute la presentation (line icons OU filled icons OU duotone, jamais un melange). Les bibliotheques recommandees : Phosphor Icons, Heroicons, Tabler Icons, Lucide.
- **Taille minimum** : 32x32px en slide 16:9 pour rester lisible a distance.
- **Couleur unique** : colorer les icones avec la couleur primaire ou la couleur d'accent. Ne pas utiliser des icones multicolores qui distraient.
- **Fonction, pas decoration** : chaque icone doit servir a illustrer ou identifier un concept. Ne pas ajouter d'icones decoratives qui n'apportent pas d'information.

### Images et photographies

- **Haute resolution** : minimum 1920x1080px pour les images plein ecran en presentation 16:9. Les images pixelisees detruisent la credibilite.
- **Pertinence** : chaque image doit renforcer le message de la slide. Si l'image est generique (poignees de main, ampoule, engrenages), elle n'ajoute pas de valeur. Preferer des photos authentiques, des captures d'ecran produit ou des illustrations sur mesure.
- **Traitement uniforme** : appliquer le meme traitement a toutes les photos (meme filtre, meme ratio, meme style de cadrage). Un traitement incoherent cree un effet de collage amateur.
- **Sources recommandees** : Unsplash, Pexels (gratuites), iStock, Shutterstock (payantes), Midjourney/DALL-E (generation IA pour illustrations conceptuelles).

### Images de fond

- **Overlay** : lorsqu'une image est utilisee en fond de slide, appliquer un overlay semi-transparent (noir 40-60% ou couleur de marque 50-70%) pour garantir la lisibilite du texte superpose.
- **Point focal** : choisir des images dont le point focal ne sera pas masque par le texte. Les images avec des zones vides (ciel, surface unie) sont ideales comme fonds.
- **Pas plus de 20%** des slides : les images de fond plein ecran sont impactantes mais fatigantes si utilisees en exces. Les reserver pour les slides de titre, les transitions et les slides de citation.

---

## Slide Master et Template Design

### Architecture d'un slide master

Un slide master bien concu contient les layouts suivants :

| Layout | Usage | Elements fixes |
|---|---|---|
| **Title Slide** | Premiere slide, ouverture | Logo, titre grande taille, sous-titre, date |
| **Section Divider** | Transition entre sections | Numero de section, titre de section, couleur de fond distinctive |
| **Content — Full Width** | Contenu principal | Titre, zone de contenu pleine largeur, source |
| **Content — Two Column** | Comparaisons, texte + image | Titre, deux zones de contenu equilibrees |
| **Content — Three Column** | KPIs, listes, options | Titre, trois zones egales |
| **Data / Chart** | Visualisation de donnees | Titre, zone de graphique avec espace pour annotation et source |
| **Quote / Testimonial** | Citation, temoignage | Guillemets stylises, texte centre, attribution |
| **Blank** | Slides full-image ou custom | Logo discret et numero de page uniquement |
| **Thank You / CTA** | Derniere slide | Message de cloture, coordonnees, QR code |

### Elements du pied de slide

Le pied de page de chaque slide doit contenir au minimum :
- Le numero de page (pour faciliter les references en Q&A)
- Le logo de l'organisation (discret, en taille reduite)
- Optionnel : le titre de la presentation ou la mention de confidentialite

Ne pas surcharger le pied de page : il ne doit jamais detourner l'attention du contenu principal.

---

## Brand Compliance en Presentations

### Principes de conformite de marque

- **Utiliser exclusivement les couleurs de la palette officielle** : ne pas improviser des variantes ou des nuances non approuvees
- **Respecter les zones de protection du logo** : le logo doit avoir un espace vide minimum autour de lui (generalement egal a la hauteur d'un element du logo)
- **Utiliser les polices de la charte** : si la charte specifie des polices, les utiliser meme si des alternatives semblent plus esthetiques
- **Respecter le tone of voice** : le vocabulaire, le niveau de langue et le style redactionnel doivent etre alignes avec l'identite de marque
- **Versionner les templates** : chaque mise a jour de la charte graphique doit etre repercutee dans les templates de presentation avec un numero de version

### Gestion multi-marque

Pour les organisations avec plusieurs marques ou business units :
- Creer un master template corporate et des sous-templates par marque/BU
- Definir les elements fixes (structure de grille, typographie) et les elements variables (couleurs, logo, visuels)
- Centraliser les templates dans un espace partage (SharePoint, Google Drive, DAM) avec controle de version

---

## Responsive Design pour Presentations

### Adaptation aux formats d'ecran

| Format | Ratio | Usage principal |
|---|---|---|
| **Standard 16:9** | 1920x1080 | Presentations en salle, visio, ecrans modernes |
| **Standard 4:3** | 1024x768 | Projecteurs anciens, compatibilite legacy |
| **Ultrawide 21:9** | 2560x1080 | Ecrans de conference, installations permanentes |
| **Vertical 9:16** | 1080x1920 | Presentations sur mobile, Instagram Stories |
| **Square 1:1** | 1080x1080 | Posts LinkedIn, social media |

Regle : concevoir d'abord en 16:9 (format dominant) puis adapter si necessaire. Verifier que les elements cles ne sont pas coupes lors de la conversion de format.

### Presentations en visioconference

Les presentations en Zoom, Teams ou Meet imposent des contraintes specifiques :
- **Reduire la densite** : l'ecran est plus petit et partage avec la webcam et le chat
- **Augmenter la taille du texte** de 20% par rapport a une presentation en salle
- **Eviter les animations complexes** : le partage d'ecran peut saccader les transitions
- **Prevoir les barres d'outils** : les barres Zoom/Teams couvrent le bas de l'ecran — ne rien placer dans les 10% inferieurs

---

## Print vs Screen Optimization

### Optimisation pour l'ecran (projection)

- Utiliser des couleurs vives et saturees (les projecteurs attenuent les couleurs de 20-30%)
- Eviter les degrades subtils (le banding est visible en projection)
- Tester la presentation sur le projecteur/ecran reel avant l'evenement
- Verifier la resolution (1920x1080 minimum pour un rendu net en Full HD)

### Optimisation pour l'impression (handouts)

- Passer en fond blanc si la presentation utilise un fond sombre (economie d'encre et lisibilite)
- Ajouter des numeros de page visibles
- Verifier que les couleurs sont distinguables en impression noir et blanc
- Creer une version "handout" separee avec davantage de texte et de contexte, car le presentateur ne sera pas la pour commenter
- Utiliser le mode "notes" de PowerPoint/Keynote pour ajouter du contexte sous chaque slide

### Export PDF

- Exporter en PDF/A pour l'archivage long terme
- Verifier l'incorporation des polices (pour eviter les substitutions)
- Optimiser le poids du fichier : compresser les images avant export (cible : < 10 MB pour un deck de 30 slides)
- Supprimer les builds et animations (ils n'apparaissent pas en PDF, ce qui cree des slides vides ou incompletes)
