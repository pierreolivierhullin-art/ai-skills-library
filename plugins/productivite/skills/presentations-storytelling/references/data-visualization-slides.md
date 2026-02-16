# Data Visualization en Slides — Graphiques, Tableaux, Infographies & Impact Visuel

## Overview

Ce document de reference couvre les principes et les bonnes pratiques de data visualization specifiquement dans le contexte des presentations. La visualisation de donnees en slide est fondamentalement differente de celle d'un dashboard interactif : en presentation, le graphique doit communiquer un message unique, etre lisible a distance et s'integrer dans un arc narratif. Utiliser ce guide pour choisir le bon type de graphique, le designer avec rigueur et l'annoter de maniere a transformer une donnee brute en argument convaincant. Chaque graphique dans une presentation doit repondre a la question : "Qu'est-ce que je veux que l'audience retienne de cette donnee ?"

---

## Guide de Selection de Graphiques

### Matrice de decision : quel graphique pour quel message ?

| Message a communiquer | Type de graphique recommande | Alternative |
|---|---|---|
| **Comparaison entre categories** | Bar chart horizontal | Column chart (si < 6 categories) |
| **Evolution dans le temps** | Line chart | Area chart (pour montrer le volume) |
| **Composition / Repartition** | Stacked bar chart | Treemap, Waffle chart |
| **Part de marche / Proportion** | Waffle chart (100 carres) | Donut chart (maximum 4 segments) |
| **Correlation entre variables** | Scatter plot | Bubble chart (3e variable en taille) |
| **Distribution** | Histogram | Box plot (pour audiences techniques) |
| **Classement / Ranking** | Bar chart horizontal ordonne | Lollipop chart |
| **Flux / Processus** | Sankey diagram | Flow chart |
| **Geographie** | Carte choropleth | Bubble map |
| **Ecart objectif/realise** | Bullet chart | Gauge (pour un KPI unique) |
| **KPI unique** | Big Number display | Delta / variation |

### Arbre de decision rapide

```
Quelle est la nature de vos donnees ?
├── Categorielle (pays, produits, segments)
│   ├── Peu de categories (< 6) → Bar chart horizontal
│   ├── Beaucoup de categories (> 6) → Bar chart horizontal trie, ou top 5 + "Autres"
│   └── Proportion d'un tout → Waffle chart ou stacked bar
├── Temporelle (mois, trimestres, annees)
│   ├── Une seule serie → Line chart
│   ├── 2-4 series → Line chart multi-series
│   └── Composition dans le temps → Stacked area chart
├── Numerique continue (2 variables)
│   └── Correlation → Scatter plot
└── Un seul chiffre cle
    └── Big Number display avec contexte (delta, trend)
```

---

## Bonnes Pratiques par Type de Graphique

### Bar Chart / Column Chart

Le bar chart est le graphique le plus polyvalent et le plus lisible. Le privilegier par defaut.

**Regles :**
- **Horizontal pour les comparaisons** : les labels sont plus lisibles et les barres s'allongent naturellement de gauche a droite
- **Ordonner par valeur** (du plus grand au plus petit) sauf si l'ordre a un sens inherent (chronologique, alphabetique obligatoire)
- **Commencer l'axe a zero** : ne jamais tronquer l'axe Y d'un bar chart — cela deforme visuellement les proportions et trompe l'audience
- **Colorer une seule barre** (la barre cle) avec la couleur d'accent et laisser les autres en gris neutre pour guider l'attention
- **Largeur des barres** : la largeur doit etre superieure a l'espace entre les barres (ratio 2:1 recommande)
- **Labels directs** : afficher la valeur directement au bout de la barre plutot que de forcer la lecture de l'axe
- **Maximum 8-10 barres** par graphique. Au-dela, regrouper en categories ou ne montrer que le top 5 + "Autres"

**Anti-patterns :**
- Effet 3D sur les barres (deforme la lecture des valeurs)
- Barres avec des patterns/textures differentes (preferer la couleur)
- Doubles axes Y (une echelle a gauche, une a droite) qui confondent la lecture

### Line Chart

Le line chart est le choix naturel pour les donnees temporelles.

**Regles :**
- **Maximum 4 lignes** sur un meme graphique. Au-dela, les lignes se croisent et deviennent illisibles. Creer des graphiques separes ou utiliser le small multiples pattern.
- **Epaisseur de ligne** : 2-3px pour la ligne principale, 1-1.5px pour les lignes secondaires ou de reference
- **Annoter les points cles** directement sur la courbe : pic, creux, point d'inflexion, evenement marquant
- **Ligne de reference** (benchmark, objectif, moyenne) en pointille gris pour donner du contexte
- **Eviter les lignes lissees** si les donnees sont irregulieres — la lissage peut masquer des variations significatives
- **Labels de serie en fin de ligne** plutot que dans une legende separee (elimine l'aller-retour visuel)

**Anti-patterns :**
- Axe Y ne commencant pas a zero (sauf si le range est explicitement justifie et annote)
- Trop de points de donnees sans lissage (la courbe devient un zigzag illisible)
- Couleurs trop proches pour des series differentes (indistinguables en projection)

### Pie Chart et Alternatives

Le pie chart est le graphique le plus controverse en data visualization. L'oeil humain est mauvais pour estimer les angles — un bar chart est presque toujours superieur.

**Si vous devez utiliser un pie chart :**
- **Maximum 4 segments** (au-dela, les petits segments deviennent illisibles)
- **Ordonner les segments** du plus grand au plus petit, en commencant a 12h
- **Afficher les pourcentages** directement sur ou a cote de chaque segment
- **Ne jamais utiliser d'effet 3D** (deforme completement la perception des proportions)
- **Preferer le donut chart** (anneau) au pie chart classique : le centre vide peut afficher le total ou le label principal

**Alternatives superieures au pie chart :**

| Alternative | Avantage | Usage ideal |
|---|---|---|
| **Waffle chart** (100 carres) | Lecture precise des proportions | Part de marche, sondages, adoption |
| **Stacked bar chart** (1 barre horizontale) | Comparaison de composition entre categories | Evolution de la composition dans le temps |
| **Treemap** | Affichage de hierarchies et proportions | Budget, repartition par categorie et sous-categorie |
| **Bar chart horizontal** | Comparaison precise des valeurs | Tout contexte ou la precision compte |

### Scatter Plot

Le scatter plot montre la relation entre deux variables numeriques.

**Regles :**
- **Ajouter une ligne de tendance** si la correlation est le message (preciser le R-carre si pertinent)
- **Annoter les outliers** : les points aberrants sont souvent les plus interessants pour l'audience
- **Utiliser la taille des points** (bubble chart) pour ajouter une troisieme dimension
- **Utiliser la couleur** pour categoriser (maximum 4-5 categories)
- **Quadrants** : si pertinent, diviser en 4 quadrants avec des lignes de reference pour creer des categories interpretables (ex : matrice BCG, matrice effort/impact)

---

## Design de Tableaux en Slides

### Principes fondamentaux

Les tableaux dans les slides doivent etre radicalement plus simples que les tableaux dans les documents ou les spreadsheets. "Less is more" est la regle absolue.

### Regles de design

- **Maximum 5 colonnes et 7 lignes** visibles sur une slide. Au-dela, la lisibilite chute drastiquement a distance.
- **Supprimer les bordures** : utiliser l'alternance de fond (zebra striping) ou l'espacement pour separer les lignes, pas des grilles lourdes.
- **Aligner les nombres a droite** et les textes a gauche. Ne jamais centrer les nombres (les unites et les virgules ne s'alignent plus).
- **Mettre en gras la colonne ou la ligne cle** pour guider l'attention.
- **Colorer les cellules cles** plutot que l'ensemble du tableau. Une cellule verte ou rouge attire l'oeil immediatement.
- **Arrondir les nombres** : en slide, "2.3M EUR" est preferable a "2,347,891 EUR". La precision excessive ne sert pas la comprehension.
- **Titre du tableau = action title** : "Notre marge progresse sur tous les segments" plutot que "Tableau des marges par segment".

### Tableau minimaliste vs tableau classique

**Tableau classique (a eviter en slide) :**
```
┌──────────┬────────┬────────┬────────┐
│ Segment  │ 2023   │ 2024   │ 2025   │
├──────────┼────────┼────────┼────────┤
│ Europe   │ 12.3M  │ 14.1M  │ 16.8M  │
├──────────┼────────┼────────┼────────┤
│ USA      │  8.7M  │ 10.2M  │ 13.1M  │
├──────────┼────────┼────────┼────────┤
│ APAC     │  3.2M  │  4.5M  │  6.7M  │
└──────────┴────────┴────────┴────────┘
```

**Tableau minimaliste (recommande en slide) :**
```
Segment     2023    2024    2025
─────────────────────────────────
Europe     12.3M   14.1M   16.8M ↑
USA         8.7M   10.2M   13.1M ↑
APAC        3.2M    4.5M    6.7M ↑↑
```

Supprimer les bordures verticales. Utiliser une seule ligne horizontale sous l'en-tete. Ajouter des indicateurs visuels (fleches, couleurs) pour les tendances.

---

## KPI et Metric Display Patterns

### Big Number Display

Le pattern le plus impactant pour communiquer un chiffre unique :

```
┌────────────────────────────────────┐
│  Titre : "Notre NPS a double       │
│           en 12 mois"              │
│                                    │
│          67                        │  ← Chiffre en 72pt+
│       points NPS                   │  ← Unite en 24pt
│                                    │
│     vs. 34 il y a 12 mois (+97%)  │  ← Contexte en 18pt
│     Benchmark secteur : 45         │  ← Reference en 16pt
└────────────────────────────────────┘
```

**Regles :**
- Le chiffre cle en tres grande taille (60-96pt) au centre de la slide
- L'unite ou le label en taille plus petite juste en dessous
- Le contexte (variation, periode, benchmark) en taille encore plus petite
- Une seule couleur d'accent sur le chiffre, le reste en couleur neutre
- Maximum 1 Big Number par slide pour un impact maximal

### Dashboard Slide (Multiple KPIs)

Quand plusieurs KPIs doivent etre presentes ensemble :

```
┌────────────────────────────────────┐
│  Performance Q3 2025               │
│                                    │
│  ┌────────┐ ┌────────┐ ┌────────┐  │
│  │ €2.3M  │ │  67    │ │  42%   │  │
│  │Revenue │ │  NPS   │ │Marge   │  │
│  │ +15% ▲ │ │ +12 ▲  │ │ +3pp ▲ │  │
│  └────────┘ └────────┘ └────────┘  │
│                                    │
│  ┌────────┐ ┌────────┐ ┌────────┐  │
│  │  245   │ │ 94.2%  │ │  18    │  │
│  │Clients │ │Uptime  │ │ jours  │  │
│  │ +22% ▲ │ │ =      │ │DSO -5▼ │  │
│  └────────┘ └────────┘ └────────┘  │
└────────────────────────────────────┘
```

**Regles :**
- Maximum 6 KPIs par slide (grille 3x2 ou 2x3)
- Chaque KPI avec : valeur, label, variation (avec fleche et couleur)
- Code couleur semantique constant : vert = positif, rouge = negatif, gris = stable
- Aucun graphique dans les cartes KPI — uniquement le chiffre et la variation
- Le titre de la slide resume le message global ("Tous nos KPIs sont en progres au T3")

### Delta / Variation Display

Pour montrer un changement ou un ecart :

```
34 → 67
NPS score, +97% en 12 mois
```

Ou avec un before/after visuel :

```
┌───────────────────────────────────────┐
│  Avant (Q1 2024)    Apres (Q1 2025)   │
│                                       │
│     34                   67           │
│   points NPS          points NPS      │
│                                       │
│           ──── +97% ────→             │
└───────────────────────────────────────┘
```

### Gauge / Speedometer

Utile pour un KPI unique avec un objectif defini :

- **Utiliser avec parcimonie** : un gauge prend beaucoup de place pour peu d'information
- Definir clairement les zones (rouge/orange/vert) avec des seuils explicites
- Afficher la valeur actuelle ET l'objectif en chiffres (ne pas forcer la lecture du gauge seul)
- Alternative plus efficace : un bullet chart (bar chart horizontal avec marqueur d'objectif)

---

## Before/After Visualization

### Pattern de comparaison temporelle

Le before/after est un pattern narratif puissant pour montrer l'impact d'une action :

```
┌────────────────────────────────────┐
│  Impact de la refonte du processus  │
│                                    │
│  AVANT           →       APRES     │
│  ┌──────────┐        ┌──────────┐  │
│  │ 12 jours │        │  3 jours │  │
│  │ delai     │        │ delai    │  │
│  │ moyen    │        │ moyen    │  │
│  └──────────┘        └──────────┘  │
│                                    │
│       -75% de temps de traitement  │
└────────────────────────────────────┘
```

**Regles :**
- Placer "Avant" a gauche et "Apres" a droite (sens naturel de lecture)
- Utiliser la meme echelle et le meme format pour les deux etats
- Afficher le delta en grand entre ou sous les deux etats
- Utiliser la couleur pour renforcer : gris/rouge pour "Avant", couleur d'accent/vert pour "Apres"

---

## Process et Flow Diagrams

### Principes de design de diagrammes de flux

Les diagrammes de processus doivent etre simples et directionnels en slide :

- **Direction gauche-droite** pour les processus lineaires (sens de lecture)
- **Direction haut-bas** pour les hierarchies et les arbres de decision
- **Maximum 5-7 etapes** visibles sur une slide. Au-dela, decomposer en sous-processus sur des slides separees
- **Formes simples** : rectangles arrondis pour les etapes, losanges pour les decisions, fleches pour les connexions
- **Couleur par categorie** : utiliser la couleur pour distinguer les acteurs, les phases ou les types d'action
- **Numerotation explicite** des etapes pour faciliter la reference en discussion

### Types de diagrammes de processus

| Type | Usage | Forme |
|---|---|---|
| **Processus lineaire** | Workflow sequentiel, etapes ordonnees | Fleches horizontales, chevrons |
| **Swimlane** | Processus multi-acteurs avec responsabilites | Lignes horizontales par acteur |
| **Cycle** | Processus iteratif, boucle d'amelioration | Cercle avec etapes |
| **Funnel** | Processus de conversion/filtrage | Entonnoir avec volumes |
| **Arbre de decision** | Parcours avec choix | Branches avec losanges |
| **Gantt simplifie** | Timeline de projet | Barres horizontales sur axe temporel |

### Funnel Diagram

Le funnel est un classique des presentations marketing et commerciales :

```
┌──────────────────────────────────┐  10,000 visiteurs
│                                  │
└──────────┐              ┌────────┘
           │              │          2,500 leads (25%)
           └──────┐  ┌────┘
                  │  │               500 MQLs (20%)
                  └──┘
                  │  │               100 deals (20%)
                  └──┘
                   ▼                 35 clients (35%)
```

**Regles du funnel :**
- Afficher les volumes absolus ET les taux de conversion entre chaque etape
- Colorer les etapes en degrade (du plus clair au plus fonce, ou inversement)
- Annoter le taux de conversion le plus faible (point de friction) avec un callout
- Ne pas depasser 5-6 niveaux dans le funnel

---

## Comparison Layouts

### Layouts de comparaison

| Pattern | Usage | Structure |
|---|---|---|
| **Deux colonnes** | Comparer 2 options, avant/apres | 50/50 split vertical |
| **Tableau comparatif** | Comparer 3+ options sur des criteres | Colonnes = options, lignes = criteres |
| **Harvey balls** | Evaluer des options sur une echelle qualitative | Cercles remplis (vide, quart, demi, trois-quarts, plein) |
| **Matrice 2x2** | Positionner des elements sur 2 axes | Quadrants avec labels |
| **Radar / Spider chart** | Comparer des profils multi-criteres | Polygones superposes |

### Matrice 2x2

La matrice 2x2 est un outil de positionnement visuel puissant :

```
              Axe Y ↑
                    │
     Quadrant 2     │    Quadrant 1
     (opportunite)  │    (priorite)
                    │
    ────────────────┼────────────────→ Axe X
                    │
     Quadrant 3     │    Quadrant 4
     (basse prio)   │    (risque)
                    │
```

**Regles :**
- Nommer chaque axe avec clarte (pas de jargon)
- Nommer chaque quadrant avec un label actionnable
- Placer les elements (projets, produits, marches) comme des points ou des bulles
- Utiliser la taille des bulles pour ajouter une dimension (ex : CA, nombre de clients)
- Le quadrant prioritaire doit etre visuellement le plus mis en avant (couleur d'accent)

---

## Annotation et Callout Techniques

### Principes d'annotation

L'annotation est ce qui transforme un graphique descriptif en graphique argumentatif. Sans annotation, le graphique laisse l'audience interpreter seule — et elle peut interpreter differemment de votre intention.

### Types d'annotations

| Type | Usage | Implementation |
|---|---|---|
| **Callout de donnee** | Pointer une valeur specifique | Fleche + etiquette avec la valeur et le contexte |
| **Zone de highlight** | Mettre en evidence une periode ou une zone | Rectangle semi-transparent colore sur la zone |
| **Ligne de reference** | Ajouter un benchmark ou un objectif | Ligne horizontale en pointille avec label |
| **Note de source** | Citer l'origine des donnees | Texte en petit en bas de la slide |
| **Insight textuel** | Formuler le takeaway en une phrase | Encart ou texte en gras sous ou a cote du graphique |

### Regles d'annotation

- **Annoter l'essentiel, pas tout** : 1 a 3 annotations par graphique maximum. Trop d'annotations recreent la surcharge.
- **Utiliser la couleur d'accent** pour les annotations afin qu'elles se distinguent du graphique
- **La fleche pointe vers la donnee**, pas depuis la donnee. L'oeil suit la fleche dans le sens de la pointe.
- **Le texte d'annotation est une phrase courte** (5-10 mots), pas un paragraphe
- **Toujours inclure la source** des donnees en petit en bas de la slide (credibilite et tracabilite)

---

## Couleur et Codage pour les Donnees

### Codage couleur semantique

Maintenir un codage couleur coherent dans toute la presentation :

| Couleur | Signification | Usage |
|---|---|---|
| **Vert** (#38A169) | Positif, en progres, objectif atteint | KPIs en hausse, validation |
| **Rouge** (#E53E3E) | Negatif, en recul, alerte | KPIs en baisse, risques |
| **Orange** (#ED8936) | Attention, modere, en cours | Elements a surveiller |
| **Bleu** (#3182CE) | Neutre, informatif | Donnees de reference, benchmarks |
| **Gris** (#A0AEC0) | Contexte, secondaire | Donnees historiques, comparaisons |
| **Couleur d'accent** | Point cle, highlight | La donnee que l'audience doit retenir |

### Codage par intensite

Utiliser des variations d'intensite (clair a fonce) d'une meme couleur pour representer une progression :

- **Clair** : valeur faible ou ancienne
- **Moyen** : valeur intermediaire ou de reference
- **Fonce** : valeur forte ou recente

Ce pattern est plus accessible que le codage multi-couleur pour les personnes daltoniennes.

### Mise en contraste (highlight)

Pour attirer l'attention sur une donnee specifique dans un graphique :
- Colorer la barre/ligne/point cle avec la couleur d'accent
- Laisser toutes les autres barres/lignes/points en gris neutre
- L'oeil ira immediatement vers l'element colore

Ce pattern "gris + accent" est le plus efficace pour le data storytelling car il combine la vue d'ensemble (contexte en gris) avec le focus (highlight en couleur).

---

## Accessibilite en Data Visualization

### Principes d'accessibilite

- **Ne pas reposer sur la couleur seule** pour distinguer les series de donnees. Ajouter des patterns (pointilles, hachures), des labels directs ou des formes differentes.
- **Contraste minimum 3:1** entre les elements de donnees adjacents
- **Labels directs** sur les graphiques plutot que des legendes separees (reduit la charge cognitive pour tous les utilisateurs)
- **Taille de texte minimum 14pt** pour les annotations et labels de graphiques
- **Description alternative** : dans les speaker notes ou le texte de la slide, decrire brievement ce que montre le graphique pour les personnes qui ne peuvent pas le voir (partage par email, lecture d'ecran)

### Palette daltonien-friendly

Eviter le couple rouge/vert (indistinguable pour 8% des hommes). Alternatives :
- **Bleu / Orange** : distinguable par tous les types de daltonisme
- **Bleu / Rouge** : bon contraste, mais verifier le type deuteranopie
- **Violet / Jaune-orange** : excellent contraste universel
- Utiliser un simulateur de daltonisme (Color Oracle, Coblis) pour verifier chaque graphique

### Test de lisibilite a distance

Avant de finaliser une slide de donnees :
1. Afficher la slide en mode diaporama
2. Se placer a 3 metres de l'ecran
3. Verifier que le message principal est lisible (titre + annotation)
4. Verifier que les valeurs cles sont distinguables
5. Verifier que les couleurs sont differenciables
