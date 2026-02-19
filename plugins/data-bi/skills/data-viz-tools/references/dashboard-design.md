# Design de Dashboards — Principes et Patterns

## Vue d'ensemble

Un dashboard n'est pas une collection de graphiques — c'est un dispositif de communication. La majorite des echecs BI ne sont pas dus a des donnees incorrectes ou a des outils inadaptes, mais a un design qui ne guide pas l'utilisateur vers la decision. Ce guide couvre les fondements psychologiques de la perception visuelle, les regles de composition, les patterns de layout et les anti-patterns a eviter absolument.

---

## 1. Psychologie de la Perception Visuelle

### 1.1 Lois de Gestalt

Les lois de Gestalt decrivent comment le cerveau organise les elements visuels en groupes coherents. Les appliquer en dataviz reduit la charge cognitive.

**Proximite** : les elements proches sont percus comme appartenant au meme groupe.
```
Application : regrouper les KPIs lies (CA, Marge, Volume) dans un meme cadre.
Erreur courante : disperser des metriques liees aux quatre coins du dashboard.
```

**Similitude** : les elements qui se ressemblent (couleur, forme, taille) sont percus comme appartenant au meme groupe.
```
Application : meme couleur pour toutes les metriques du meme type
(ex: bleu pour les revenus, orange pour les couts dans tous les graphiques).
```

**Cloture** : le cerveau complete les formes incompletes.
```
Application : les bordures et encadres ne sont pas toujours necessaires —
la proximite et la similitude suffisent souvent.
Eviter les box avec bordures epaisses sur chaque carte.
```

**Figure/Fond** : on percoit un element principal (figure) sur un fond.
```
Application : utiliser le contraste pour mettre en evidence la metrique principale.
La donnee doit etre la figure, le chrome (bordures, labels, axes) est le fond.
```

**Continuite** : l'oeil suit les lignes et les courbes.
```
Application : aligner les elements sur une grille — l'oeil "circule" naturellement.
Les graphiques en ligne exploitent la continuite pour montrer les tendances.
```

### 1.2 Preattentive Attributes

Les attributs preattentifs sont traites par le cerveau en moins de 250ms, avant que l'attention consciente soit requise. Les utiliser pour guider l'attention instantanement.

| Attribut | Force | Cas d'usage |
|----------|-------|-------------|
| Position | Tres forte | Axe Y pour comparer les valeurs |
| Couleur (teinte) | Forte | Distinguer des categories |
| Couleur (luminosite) | Forte | Montrer une intensite (heatmap) |
| Taille | Forte | Proportionnel a la valeur (bulle, barre) |
| Mouvement | Tres forte | Alertes (avec moderation) |
| Forme | Faible | Distinguer categories (sur scatter) |
| Orientation | Faible | Eviter pour des comparaisons directes |
| Enclosure | Forte | Grouper des elements |

Regle fondamentale : n'utiliser qu'UN seul attribut preattentif pour guider l'attention vers la metrique la plus importante. En utiliser plusieurs simultanement annule leur effet.

---

## 2. Hierarchie de l'Information

### 2.1 Framework What / So What / Now What

Chaque dashboard doit repondre a trois niveaux :

```
WHAT (Quoi se passe-t-il ?)
    -> Les KPIs de surface : CA, taux de conversion, NPS
    -> Visible immediatement, dans les 3 premieres secondes de lecture

SO WHAT (Et alors ?)
    -> Contexte et comparaison : vs objectif, vs mois precedent, vs annee precedente
    -> Tendances : hausse, baisse, stagnation
    -> Segmentation : quels produits, regions, clients

NOW WHAT (Que faire ?)
    -> Anomalies detectees et signalees
    -> Recommandations automatiques (si possible)
    -> Call to action explicite : "Revoir le stock SKU-4421 en region Nord"
```

### 2.2 Principe de la Pyramide Inversee

Comme en journalisme, placer l'information la plus importante en haut et a gauche :

```
[Zone haute : KPIs globaux + alertes critiques]
[Zone milieu : decomposition par dimension principale]
[Zone basse : details et tableaux de donnees brutes]
```

L'utilisateur qui n'a que 30 secondes repart avec l'essentiel. Celui qui a 5 minutes peut creuser.

---

## 3. Choix du Graphique — Reference Complete

### 3.1 Questions Business et Graphiques Recommandes

| Question Business | Graphique Recommande | Alternative |
|-------------------|----------------------|-------------|
| Evolution dans le temps | Graphique en ligne | Barres (si periodes discretes) |
| Comparaison de valeurs | Barres horizontales | Barres verticales |
| Part d'un tout (avec max 5 parts) | Barres empilees 100% | Pie (5 parts max, avec labels) |
| Correlation entre 2 variables | Scatter plot | Heatmap (si trop de points) |
| Distribution d'une variable | Histogramme | Box plot, violin plot |
| Performance vs objectif | Bullet chart | Jauge (avec moderation) |
| Geographie | Carte choropleth | Carte a bulles (valeurs absolues) |
| Classement | Barres triees | Bump chart (classement dans le temps) |
| Hierarchie/Proportion | Treemap | Sunburst (si imbrication visible) |
| Matrice de correlation | Heatmap | Scatter plot matrix |
| Flux entre categories | Sankey | Chord diagram |
| Profil/Spider | Radar chart (max 6-8 axes) | Barres groupees |
| Anomalie dans serie temp. | Ligne + bandes de controle | Barres avec couleur conditionnelle |
| Composition et evolution | Barres empilees | Area chart empile |
| 3 variables quantitatives | Scatter + taille de bulle | Heatmap 2D + couleur |
| KPI unique vs objectif | Bullet chart | Big number + variation |
| Donnees categorielles (freq.) | Barres | Dot plot (si nombreuses categories) |
| Survie/Retention | Courbe de Kaplan-Meier | Heatmap de cohortes |
| Cohortes de retention | Heatmap triangulaire | Lignes par cohorte |
| Funnel/Entonnoir | Funnel chart | Barres horizontales triees |
| Duree / Gantt | Gantt chart | Barres horizontales flottantes |
| Changement entre 2 points | Slope chart | Fleche (dans les slides) |
| Comparaison multi-dimensions | Small multiples | Groupes de barres |
| Volatilite financiere | Chandelier (OHLC) | Ligne avec bandes |
| Relation partie-tout (multi-niveaux) | Sunburst | Treemap icicle |
| Donnees geospatiales ponctuelles | Carte a points | Carte de chaleur (density) |
| Echelles multiples (differentes unites) | Dual axis | Small multiples |
| Top N + reste | Barres avec categorie "Autres" | Treemap |
| Text mining / frequence de mots | Tableau de donnees | Wordcloud (decoratif seulement) |
| Tendance + saisonnalite | STL decomposition | Ligne avec annotations |
| Benchmarking multivariant | Radar | Tableau de scores |
| Reseaux et connexions | Network graph | Matrice d'adjacence |
| Waterfall / cascade | Waterfall chart | Barres flottantes |
| Incertitude / intervalles | Graphique avec barres d'erreur | Ribbon chart |

### 3.2 Regles de Decision Rapide

```
Si la donnee est dans le temps -> Ligne (tendance) ou Barre (comparison)
Si c'est une partie d'un tout -> Barres empilees 100% (jamais pie si >5 parts)
Si c'est une comparaison -> Barres horizontales triees (toujours)
Si c'est une relation -> Scatter plot
Si c'est une distribution -> Histogramme ou box plot
```

---

## 4. Couleur en Dataviz

### 4.1 Trois Types de Palettes

**Palettes sequentielles** : pour des valeurs quantitatives ordonnees (du plus faible au plus eleve).
```
Exemples : Blues, Greens, YlOrRd (jaune-orange-rouge)
Usage : heatmaps, cartes choropleth, intensite de valeur
Regle : une seule teinte, variation de luminosite/saturation
```

**Palettes divergentes** : pour des valeurs avec un point neutre (zero, moyenne, objectif).
```
Exemples : RdBu (rouge-blanc-bleu), PiYG (rose-blanc-vert), RdYlGn
Usage : ecart a l'objectif (negatif/positif), temperature
Regle : deux teintes distinctes, blanc/gris au centre
```

**Palettes categoriques** : pour distinguer des categories sans ordre.
```
Exemples : Tableau 10, ColorBrewer Set2, D3 Category10
Usage : produits, regions, segments
Regle : max 8-10 categories (au-dela, utiliser des nuances ou regrouper)
```

### 4.2 Charte ColorBrewer

ColorBrewer (colorbrewer2.org) est la reference academique pour les palettes de cartes et dataviz. Chaque palette est notee pour :
- Daltonisme (safe or not)
- Impression (print-friendly)
- Ecran (screen-friendly)
- Photocopie (photocopy-friendly)

Palettes ColorBrewer recommandees :

```
Sequentiel :
- Blues (3-9 classes) — safe daltonisme
- YlOrRd (3-8 classes) — forte attire l'attention
- Viridis (externe, perceptuellement uniforme) — recommande pour cartes

Divergent :
- RdBu — tres lisible, bon contraste central
- PiYG — pour les analyses positif/negatif vegetation
- RdYlGn — dangereux pour daltoniens (rouge/vert) — eviter

Categorique :
- Set2 — couleurs pastel, bonnes pour les fonds clairs
- Dark2 — couleurs saturees, pour petits elements (points, lignes)
- Paired — 12 couleurs, pour les paires logiques (actuel/precedent)
```

### 4.3 Daltonisme — Palette Daltonien-Safe

8% des hommes et 0.5% des femmes ont une forme de daltonisme (deuteranopie : confusion rouge-vert la plus courante).

Regles :
```
Eviter : rouge/vert comme seule distinction (tres courante erreur BI)
Preferer : rouge/bleu, orange/violet, jaune/violet
Utiliser la forme ET la couleur conjointement
Tester avec un simulateur : Color Oracle (gratuit, PC/Mac)
```

Palette universelle (accessible daltoniens) :
```
Noir        #000000
Orange      #E69F00
Bleu ciel   #56B4E9
Vert        #009E73
Jaune       #F0E442
Bleu        #0072B2
Orange rouge #D55E00
Rose/Violet #CC79A7
```
(Source : Wong 2011, Nature Methods)

---

## 5. Typographie dans les Dashboards

### 5.1 Regles Fondamentales

```
Une seule famille typographique (deux maximum : une pour les titres, une pour le corps)
Sans-serif pour les ecrans (Inter, Roboto, Lato, Open Sans)
Hierarchie claire via la taille, pas la decoration (eviter gras, italique, souligne excessif)
```

Hierarchie typographique recommandee :

| Element | Taille | Poids | Usage |
|---------|--------|-------|-------|
| Titre de page | 20-24px | Bold | Titre du dashboard |
| Titre de section | 14-16px | Semibold | Titre de graphique |
| Big number KPI | 28-48px | Bold | Metrique principale |
| Label de donnee | 11-12px | Regular | Valeurs sur graphique |
| Annotation | 10-11px | Regular | Notes, legendes |
| Texte de tableau | 11-12px | Regular | Donnees tabulaires |

### 5.2 Regles d'Espacement

```
Marges internes : min 8px entre contenu et bord de carte
Espacement entre cartes : 8-12px
Espacement de section : 16-24px
Line-height : 1.4 a 1.6 pour le texte courant
```

---

## 6. Patterns de Layout

### 6.1 F-Pattern et Z-Pattern de Lecture

Le F-pattern (etudes eyetracking) decrit comment les utilisateurs lisent les dashboards :
- Ligne horizontale en haut (tres regardee)
- Deuxieme passage horizontal moins loin
- Scan vertical a gauche

Le Z-pattern est plus adapte aux dashboards denses :
- Haut gauche > Haut droite > Bas gauche > Bas droite

Application :
```
Haut gauche : KPI le plus important / alerte la plus critique
Haut droit : KPI secondaire
Milieu : graphique principal (tendance temporelle)
Bas : decomposition et details
```

### 6.2 Grille 12 Colonnes

Comme en design web, la grille 12 colonnes offre une flexibilite maximale :

```
Full width (12/12)   : titre, graphique en ligne principal
3/4 + 1/4 (9+3)     : graphique principal + KPI sidebar
1/2 + 1/2 (6+6)     : deux graphiques de meme importance
1/3 + 1/3 + 1/3 (4+4+4) : trois KPIs ou trois petits graphiques
1/4 x 4 (3+3+3+3)   : quatre KPIs de meme niveau
```

### 6.3 Layout Types Recommandes

**Dashboard executif** (une page, vue globale) :
```
[Ligne 1 : 4 KPI cards — CA, Marge, NPS, Conversion] (1/4 x 4)
[Ligne 2 : Tendance CA 12 mois + Carte geographique]  (2/3 + 1/3)
[Ligne 3 : Top produits (barres) + Performance vs plan (bullet)] (1/2 + 1/2)
```

**Dashboard operationnel** (surveillance, alertes) :
```
[Header : status global (vert/orange/rouge) + heure MAJ]
[Ligne 1 : alertes actives (tableau avec couleurs)] (full width)
[Ligne 2 : metriques en temps reel (lignes)] (1/2 + 1/2)
[Ligne 3 : detail par responsable/zone] (full width)
```

**Dashboard self-service** (exploration) :
```
[Header : filtres globaux (dates, region, categorie)]
[Zone principale : graphique large interactif] (2/3)
[Sidebar : decompositions, drill-down] (1/3)
[Footer : tableau de donnees exportable] (full width)
```

---

## 7. Design des KPI Cards

Structure d'une KPI card efficace :

```
+----------------------------------+
| Libelle KPI (12px, gris)         |
|                                  |
|  123 456 EUR   (+8.2%)          |
|  (big number)  (variation)       |
|                                  |
| [sparkline 12 mois]              |
|                                  |
| vs 113 830 EUR il y a 1 an      |
| Objectif : 120 000 EUR (103%)   |
+----------------------------------+
```

Elements obligatoires :
- **Libelle** : court et sans ambiguite ("CA Net HT" plutot que "Chiffre")
- **Valeur principale** : grande, lisible en 1 seconde
- **Variation** : couleur verte/rouge + fleche directionnelle + pourcentage
- **Contexte** : valeur de comparaison (N-1, objectif, benchmark)

Elements optionnels :
- Sparkline : tendance sur les 12 derniers mois (sans axes)
- Icone : si la metrique est tres standard (panier = shopping cart)
- Tooltip : detail du calcul sur survol

Couleur de la variation :
```
Eviter le simple rouge/vert (daltonisme)
Preferer : icone directionnelle + couleur + pourcentage
Pour les metriques inverses (ex: taux de churn, cout) : rouge = hausse
```

---

## 8. Audiences et Types de Dashboards

### 8.1 Executive Dashboard

```
Public : C-level, directeurs
Frequence : hebdomadaire ou mensuel
Objectif : vue globale de la performance vs strategie
Format : une page, max 8 metriques
Granularite : mensuelle ou trimestrielle
Interactivite : minimale (filtres annee/periode uniquement)
Design : epure, chiffres grands, peu de graphiques complexes
```

### 8.2 Operational Dashboard

```
Public : managers, equipes terrain
Frequence : quotidien ou temps reel
Objectif : detecter et reagir aux anomalies
Format : multi-sections, denses
Granularite : jour, heure, ou temps reel
Interactivite : filtres multiples, alertes, drill-down
Design : informatif, dense, alertes visuelles claires
```

### 8.3 Self-Service Dashboard

```
Public : analystes, equipes metier autonomes
Frequence : a la demande
Objectif : exploration libre, ad-hoc analysis
Format : flexible, filtres riches, vues multiples
Granularite : ajustable par l'utilisateur
Interactivite : maximale (cross-filtering, parametres, export)
Design : moins controle, guide par les filtres
```

---

## 9. Mobile Dashboards

### 9.1 Contraintes Mobile

```
Ecran : 375-414px de large (iPhone), 360-412px (Android)
Navigation : doigt (touch targets min 44x44px)
Contexte d'usage : debout, en deplacement, 30 secondes max
Connexion : parfois lente
```

### 9.2 Patterns Mobile

**Progressive disclosure** : montrer les KPIs en premier, le detail sur tap
```
Ecran 1 : 3-4 KPIs empiles verticalement (full width)
Ecran 2 (scroll) : graphique principal simplifie
Ecran 3 (scroll) : tableau de donnees condense
```

**Touch targets** :
```
Boutons et filtres : min 44x44px
Espacement entre elements cliquables : min 8px
Eviter le hover (n'existe pas sur mobile)
```

### 9.3 Simplifications Necessaires

```
Supprimer : legendes complexes, tooltips riches, graphiques denses
Simplifier : 1 metrique par graphique, labels directs sur les barres
Adapter : pie -> big number + top 3, treemap -> liste triee
Conserver : couleurs semantiques, variations, alertes
```

---

## 10. Anti-Patterns a Eviter Absolument

### 10.1 Chartjunk

Le chartjunk (Tufte, 1983) designe tout element visuel qui n'ajoute pas d'information :
```
- Grilles epaisses et nombreuses
- Gradients et ombres portees sur les barres
- Arriere-plans non blancs (gris, texture, image)
- Logos et decorations excessifs
- Icones 3D
```

Solution : maximiser le rapport data/ink (donnee par rapport a l'encre totale du graphique).

### 10.2 Graphiques 3D

Les graphiques 3D distordent systematiquement la perception des valeurs (perspective, occlusion).
```
- Un pie chart 3D : les parts en avant semblent plus grandes
- Un bar chart 3D : la hauteur reelle est difficile a lire
- La 3D n'ajoute jamais d'information, elle en retire
```
Regle absolue : ne jamais utiliser de graphiques 3D dans un dashboard professionnel.

### 10.3 Abus des Pie Charts

Le pie chart ne fonctionne que si :
- Maximum 5 parts
- Les differences sont evidentes (>20%)
- On veut montrer qu'une part domine (>50%)

```
Remplacer par :
- Barres horizontales triees (toujours plus lisible)
- Barres empilees 100% (si comparaison temporelle)
- Treemap (si hierarchie)
```

### 10.4 Double Axe

Le double axe (dual axis) peut tromper car les deux echelles sont arbitraires.
```
Mauvais usage :
- Montrer deux metriques sans lien fort
- Faire sembler une correlation artificielle
- Echelles non alignees sur zero

Bon usage (acceptable) :
- Barres (volume) + ligne (ratio ou %) avec axes clairement libelles
- Le zero des deux axes est aligne si les deux sont des quantites
```

### 10.5 Axe Tronque

Tronquer l'axe Y (ne pas commencer a zero) exagere visuellement les differences.
```
Acceptable :
- Pour les graphiques en ligne montrant une tendance (variation relative)
- Quand la valeur zero n'est pas significative (ex: temperature en degres)

Inacceptable :
- Pour les barres et histogrammes (le zero est implicite dans la hauteur)
- Pour les comparaisons absolues entre categories
```

---

## 11. Template de Charte Graphique BI

### 11.1 Variables CSS / Tokens de Design

```css
/* Palette principale */
--color-primary:     #0F52BA;  /* Bleu corporatif */
--color-secondary:   #E8690A;  /* Orange accent */
--color-neutral:     #6B7280;  /* Gris texte */
--color-background:  #F9FAFB;  /* Fond page */
--color-surface:     #FFFFFF;  /* Fond carte */

/* Semantique */
--color-success:     #059669;  /* Vert : positif */
--color-warning:     #D97706;  /* Orange : attention */
--color-danger:      #DC2626;  /* Rouge : negatif */
--color-info:        #2563EB;  /* Bleu : informatif */

/* Typographie */
--font-family:       'Inter', sans-serif;
--font-size-kpi:     36px;
--font-size-title:   18px;
--font-size-body:    13px;
--font-size-label:   11px;

/* Espacement */
--space-card:        16px;
--space-section:     24px;
--radius-card:       8px;
--shadow-card:       0 1px 3px rgba(0,0,0,0.1);
```

### 11.2 Regles d'Application

```
1. Couleur primaire : titres, elements d'action, filtres actifs
2. Couleur secondaire : accents, call to action, indicateurs cles
3. Gris neutres : labels, axes, legendes, bords
4. Semantique : reserve aux variations (positif = vert, negatif = rouge)
5. Arriere-plan : blanc ou gris tres clair (#F9FAFB) uniquement
6. Aucune couleur "decorative" non porteuse de sens
```

---

## References

- **Edward Tufte** : The Visual Display of Quantitative Information (reference fondatrice)
- **Stephen Few** : Show Me the Numbers, Now You See It (pratique BI)
- **ColorBrewer** : colorbrewer2.org — palettes academiques pour cartes et dataviz
- **Gestalt principles in data visualization** : eagereyes.org
- **Color Oracle** : colororacle.org — simulateur de daltonisme gratuit
- **Datawrapper Academy** : academy.datawrapper.de — guides pratiques accessibles
- **Information is Beautiful** : informationisbeautiful.net — exemples inspiratrices
