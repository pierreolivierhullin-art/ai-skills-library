# Data Visualization — Best Practices, Chart Selection & Tools

## Overview

Ce document de reference couvre les meilleures pratiques de visualisation de donnees, de la theorie de la perception visuelle au design de dashboards en production. Il synthetise les travaux fondamentaux d'Edward Tufte, Stephen Few et Cole Nussbaumer Knaflic, et les applique aux outils et contextes modernes. Utiliser ce guide comme fondation pour toute decision de design visuel impliquant des donnees, en privilegiant la clarte, l'honnetete et l'efficacite communicationnelle.

This reference document covers data visualization best practices, from visual perception theory to production dashboard design. It synthesizes the foundational work of Edward Tufte, Stephen Few, and Cole Nussbaumer Knaflic, applied to modern tools and contexts. Use this guide as the foundation for any visual design decision involving data.

---

## Visualization Theory — The Masters

### Edward Tufte — The Visual Display of Quantitative Information

Tufte est le pere fondateur de la visualisation de donnees moderne. Ses principes fondamentaux, publies a partir de 1983, restent la reference absolue :

**Data-Ink Ratio**
Le ratio data-ink est defini comme la proportion d'encre dans un graphique consacree a la representation non redondante des donnees. Maximiser ce ratio en eliminant :
- Les gridlines excessives — ne conserver que les lignes de reference essentielles, voire les supprimer entierement si les labels de donnees suffisent.
- Les bordures de graphiques — le graphique n'a pas besoin d'une boite pour exister.
- Les fonds colores — utiliser un fond blanc ou tres clair.
- Les legendes redondantes — placer les labels directement sur les donnees quand c'est possible (direct labeling).
- Les effets decoratifs — aucune ombre, aucun gradient, aucun effet 3D.

**Lie Factor**
Le Lie Factor mesure la distorsion entre la representation visuelle et les donnees reelles : `Lie Factor = (taille de l'effet dans le graphique / taille de l'effet dans les donnees)`. Un Lie Factor de 1.0 est ideal. Les distorsions les plus courantes :
- Axes tronques qui exagerent les variations.
- Bulles ou icones dont l'aire ne correspond pas aux valeurs.
- Effets 3D qui deforment les proportions.
- Axes doubles avec echelles disproportionnees.

**Small Multiples**
Plutot que de superposer des series sur un graphique unique (surcharge visuelle), utiliser une grille de petits graphiques identiques, chacun montrant une facette (une categorie, une region, une periode). Les small multiples exploitent la capacite du cerveau a detecter les patterns par comparaison spatiale. Efficaces pour comparer des distributions, des tendances temporelles ou des profils geographiques.

**Sparklines**
Les sparklines sont des micro-graphiques integres dans le flux du texte ou dans les cellules d'un tableau. Elles montrent la tendance generale sans interrompre la lecture. Tufte les decrit comme "data-intense, design-simple, word-sized graphics." Utiliser les sparklines dans les tableaux de KPIs, les rapports emails et les executive summaries.

### Stephen Few — Information Dashboard Design

Few se concentre sur l'efficacite des dashboards et la perception visuelle :

**Pre-attentive Attributes**
Le cerveau traite certains attributs visuels en moins de 500 millisecondes, sans effort conscient. Exploiter ces attributs pour guider l'attention :
- **Couleur (hue)** : l'attribut le plus puissant. Utiliser une couleur d'accent unique pour l'element cle.
- **Intensite (saturation/luminosite)** : des variations d'intensite pour encoder les gradients de valeur.
- **Taille** : plus grand = plus important. Hierarchie visuelle naturelle.
- **Position** : l'attribut le plus precis pour encoder des valeurs quantitatives.
- **Orientation** : utile pour les patterns directionnels.
- **Forme** : la moins efficace pour les donnees quantitatives, a reserver pour les categories.

**Signal vs Noise**
Chaque element d'un dashboard est soit du signal (information utile a la decision) soit du bruit (decoration, redondance, distraction). Few recommande de lister chaque element visuel et de se demander : "Si je le supprime, est-ce que l'audience perd de l'information ?" Si non, le supprimer.

**Dashboard Layout Principles**
- Placer l'information la plus importante en haut a gauche (lecture en Z ou en F).
- Grouper les metriques liees spatialement (principe de proximite Gestalt).
- Limiter a 5-7 visualisations par ecran (charge cognitive).
- Utiliser une grille coherente pour l'alignement.
- Fournir un titre descriptif et une date de derniere mise a jour visible.

### Cole Nussbaumer Knaflic — Storytelling with Data

Knaflic apporte la dimension narrative et la methodologie pratique :

**Le processus en 6 etapes (detaille)**

1. **Understand the context** : avant de toucher un outil, repondre a trois questions — Qui est l'audience ? Qu'a-t-elle besoin de savoir ? Quelle action doit-elle entreprendre ? Documenter ces reponses dans un "Big Idea" statement : "En raison de [contexte], nous devrions [action] pour obtenir [resultat]."

2. **Choose an appropriate visual display** : le type de graphique doit correspondre a l'objectif analytique (comparaison, tendance, distribution, composition, relation). Ne pas choisir un type de graphique parce qu'il est esthetique — le choisir parce qu'il est efficace.

3. **Eliminate clutter** : appliquer les principes Gestalt pour identifier et supprimer l'encombrement visuel. Les principes Gestalt cles en data viz :
   - **Proximite** : les elements proches sont percus comme un groupe.
   - **Similarite** : les elements de meme couleur/forme sont percus comme relies.
   - **Enclosure** : les elements entoures d'un cadre forment un groupe (utiliser avec parcimonie).
   - **Connexion** : les elements relies par une ligne sont percus comme connectes.
   - **Continuite** : l'oeil suit naturellement les lignes et courbes.
   - **Cloture** : le cerveau complete les formes incompletes (permettre de simplifier).

4. **Focus attention** : utiliser la couleur strategiquement — une couleur neutre (gris) pour le contexte, une couleur d'accent pour l'insight principal. Jamais plus de 2-3 couleurs distinctes dans un graphique. Ajouter des annotations textuelles pour pointer le "so what".

5. **Think like a designer** : hierarchiser l'information visuellement. Utiliser la taille, le contraste et la position pour creer un chemin de lecture naturel. Appliquer les principes d'accessibilite (daltonisme, contraste).

6. **Tell a story** : structurer avec un debut (contexte et pourquoi), un milieu (les donnees et ce qu'elles revelent), et une fin (la recommandation et le call-to-action).

---

## Chart Type Selection — Comprehensive Guide

### Comparison Charts

**Bar Chart (Horizontal)**
- Usage : comparer des valeurs entre categories, surtout quand les labels sont longs.
- Best practice : trier par valeur (pas alphabetiquement) sauf si l'ordre a une signification (jours de la semaine, stades d'un funnel). Commencer l'axe a zero. Utiliser une seule couleur, avec une couleur d'accent pour la categorie a mettre en avant.
- Variante : lollipop chart — plus epure pour les longues listes de categories.

**Bar Chart (Vertical / Column)**
- Usage : comparer des valeurs entre categories (< 7 categories) ou montrer une evolution avec des periodes discretes.
- Best practice : espacement entre les barres = 50% de la largeur des barres. Eviter les barres trop etroites ou trop larges.

**Grouped Bar Chart**
- Usage : comparer des sous-categories au sein de chaque categorie. Limiter a 2-3 sous-groupes maximum.
- Alternative : preferer les small multiples si le nombre de sous-groupes depasse 3.

**Bullet Chart (Stephen Few)**
- Usage : afficher une performance par rapport a un objectif et des seuils. Remplacement optimal des jauges circulaires.
- Structure : barre principale (valeur reelle), marque de reference (objectif), bandes de fond (seuils qualitatifs : mauvais, acceptable, bon).

### Time Series Charts

**Line Chart**
- Usage : montrer l'evolution d'une ou plusieurs variables dans le temps. Le graphique le plus commun et le plus efficace pour les tendances.
- Best practice : limiter a 4-5 lignes maximum. Au-dela, utiliser des small multiples. Utiliser des lignes epaisses pour les series principales, fines pour le contexte. Ajouter des labels directs en fin de ligne plutot qu'une legende separee.

**Area Chart**
- Usage : montrer l'evolution de volumes ou d'une composition dans le temps. Efficace pour visualiser la magnitude.
- Best practice : utiliser des area charts empiles uniquement si la composition est le message principal. Utiliser la transparence pour les chevauchements.

**Slope Chart**
- Usage : comparer deux points dans le temps en montrant la direction et l'amplitude du changement. Tres efficace pour les classements avant/apres.
- Best practice : ideal pour 5-15 elements. Utiliser la couleur pour distinguer les hausses, baisses et stabilites.

### Distribution Charts

**Histogram**
- Usage : montrer la distribution de frequence d'une variable continue. Essentiel pour comprendre la forme d'une distribution (normale, bimodale, asymetrique).
- Best practice : le choix du nombre de bins est critique — trop peu masque les details, trop beaucoup cree du bruit. Utiliser la regle de Sturges ou de Freedman-Diaconis pour un point de depart, puis ajuster visuellement.

**Box Plot (Boite a moustaches)**
- Usage : comparer les distributions entre categories. Montre la mediane, les quartiles, et les outliers.
- Best practice : ajouter les points individuels (jitter) pour les petits echantillons. Completer par un violin plot pour montrer la forme de la distribution.

**Violin Plot**
- Usage : comme le box plot, mais montre la forme complete de la distribution. Plus informatif que le box plot pour les distributions multimodales.

### Correlation Charts

**Scatter Plot**
- Usage : explorer la relation entre deux variables continues. Identifier les correlations, clusters, et outliers.
- Best practice : ajouter une ligne de tendance (regression) si la correlation est le message principal. Annoter les outliers significatifs. Utiliser la taille et la couleur comme troisieme et quatrieme dimensions (bubble chart).

**Heatmap**
- Usage : montrer les patterns dans une matrice de donnees (correlation, frequence par heure/jour, performance croisee).
- Best practice : utiliser une echelle de couleurs sequentielle pour les valeurs unidirectionnelles, divergente pour les valeurs avec un point milieu significatif (ex : ecart a un objectif).

### Composition Charts

**Stacked Bar Chart**
- Usage : montrer la composition d'un tout et comparer entre categories. Limiter a 3-5 segments maximum.
- Best practice : placer la categorie la plus importante en bas (baseline commune). Les stacked bars 100% sont utiles pour comparer les proportions.

**Treemap**
- Usage : montrer la composition hierarchique avec de nombreuses categories. Efficace pour les donnees part-of-whole avec 2 niveaux de hierarchie.
- Best practice : utiliser la couleur pour encoder une seconde dimension (performance, categorie). Ajouter des labels de pourcentage dans les rectangles.

**Waterfall Chart**
- Usage : montrer comment une valeur initiale est affectee par des augmentations et diminutions successives pour arriver a une valeur finale. Ideal pour les analyses financieres (passage du CA au resultat net).

### Geographic Charts

**Choropleth Map**
- Usage : montrer la distribution d'une variable par zone geographique en colorant les zones.
- Attention : les grandes zones visuelles (Russie, Canada) dominent visuellement meme si leur valeur est faible. Utiliser des taux (per capita) plutot que des valeurs absolues. Envisager un cartogramme pour corriger le biais de surface.

**Bubble Map**
- Usage : placer des bulles proportionnelles sur une carte. Evite le biais de surface du choropleth.

---

## Color Theory for Data Visualization

### Types de palettes

**Sequentielle (quantitative, unidirectionnelle)**
- Usage : donnees ordonnees allant d'un minimum a un maximum (temperature, densite, chiffre d'affaires).
- Principe : une seule teinte avec variation de luminosite (clair = faible, fonce = eleve) ou une progression entre deux teintes proches.
- Exemples : bleu clair vers bleu fonce, beige vers marron.

**Divergente (quantitative, bidirectionnelle)**
- Usage : donnees avec un point central significatif et des extremes dans deux directions (ecart a un objectif, sentiment positif/negatif, correlation).
- Principe : deux teintes contrastees aux extremes, avec un point neutre (blanc ou gris clair) au centre.
- Exemples : rouge-blanc-bleu, orange-blanc-violet.

**Categorielle (qualitative)**
- Usage : distinguer des categories sans ordre inherent (segments de marche, regions, types de produits).
- Principe : teintes distinctes avec une luminosite similaire. Maximum 7-8 couleurs distinctes — au-dela, utiliser d'autres encodages (forme, position).
- Exemples : palettes Tableau 10, ColorBrewer qualitative, palette Okabe-Ito.

### Accessibilite et daltonisme

Environ 8% des hommes et 0.5% des femmes sont daltoniens. Concevoir en consequence :
- **Ne jamais encoder l'information uniquement par la couleur** : ajouter des formes, des patterns, des labels directs ou des textures.
- **Eviter la combinaison rouge-vert** : utiliser plutot bleu-orange ou bleu-rouge.
- **Tester avec des simulateurs** : Coblis, Color Oracle, Viz Palette (Susie Lu).
- **Utiliser des palettes daltonien-safe** : palette Okabe-Ito, palettes ColorBrewer annotees comme "colorblind safe".
- **Maintenir un contraste suffisant** : ratio de contraste minimum 4.5:1 pour le texte (WCAG AA), 3:1 pour les elements graphiques.

### Regles pratiques pour la couleur

- **Couleur grise par defaut** : utiliser le gris comme couleur de base pour toutes les donnees de contexte. Reserver la couleur pour l'insight principal (accent unique).
- **Une seule couleur d'accent** : dans une presentation, un seul element doit attirer l'attention. Utiliser une couleur vive pour cet element, gris pour tout le reste.
- **Coherence organisationnelle** : definir une palette data officielle alignee avec la charte graphique de l'organisation, mais optimisee pour la lisibilite des donnees (pas pour l'esthetique du branding).
- **Eviter les couleurs pures saturees** : les couleurs tres saturees (rouge pur, bleu pur) fatiguent visuellement. Utiliser des versions legerement desaturees.
- **Respecter les conventions culturelles** : rouge = negatif/danger, vert = positif/succes dans le contexte occidental. Ne pas inverser ces associations sauf raison forte.

---

## Dashboard UX Design

### Architecture d'information d'un dashboard

**Hierarchie en 3 niveaux (Overview, Detail, Exception)**

Niveau 1 — Overview (ecran principal) :
- Big numbers (5-7 KPIs cles) avec sparklines de tendance et indicateurs de direction (fleches, couleurs).
- Un ou deux graphiques synthetiques montrant les tendances principales.
- Comparaison avec la periode precedente et l'objectif.
- Temps de comprehension cible : < 5 secondes pour le message principal.

Niveau 2 — Detail (drill-down) :
- Graphiques detailles par dimension (temps, categorie, geographie).
- Filtres interactifs pour l'exploration (date range, segments, produits).
- Tableaux de donnees avec tri et recherche.
- Temps d'exploration cible : 5-15 minutes.

Niveau 3 — Exception (alertes et anomalies) :
- Mise en evidence automatique des anomalies et deviations significatives.
- Seuils visuels (rouge/jaune/vert) pour l'action immediate.
- Lien vers les donnees brutes pour l'investigation.

### Layout et grille

- **Grille 12 colonnes** : standard pour la responsivite. Les widgets occupent 4, 6, 8 ou 12 colonnes.
- **Lecture en Z ou en F** : l'information la plus importante en haut a gauche.
- **Above the fold** : les KPIs et messages cles doivent etre visibles sans scroll.
- **Espacement coherent** : utiliser un systeme de spacing uniforme (8px base grid).
- **Titre et contexte** : chaque dashboard a un titre descriptif, une date de derniere mise a jour, et une breve description de son objet.

### Interactivite

**Filtrage**
- Filtres globaux en haut du dashboard (date range, segment, region).
- Filtres contextuels par graphique (click-to-filter, cross-filtering).
- Etat des filtres toujours visible et reinitialisation facile.

**Drill-down**
- Permettre le passage du resume au detail par clic sur un element de graphique.
- Maintenir le contexte lors du drill-down (breadcrumb, back navigation).
- Afficher la profondeur de drill-down disponible visuellement.

**Tooltips**
- Fournir les valeurs exactes au survol (hover).
- Inclure le contexte (pourcentage, rang, comparaison).
- Garder les tooltips concis (< 5 lignes d'information).

### Performance et temps de chargement

- Un dashboard doit se charger en moins de 3 secondes. Au-dela, l'adoption chute drastiquement.
- Precomputer les aggregations cles (materialized views, extracts).
- Limiter le nombre de requetes simultanees par page (lazy loading pour les widgets below the fold).
- Cacher les resultats avec une politique d'invalidation adaptee a la fraicheur requise des donnees.

---

## Interactive Visualizations

### Principes d'interactivite efficace

**Overview first, zoom and filter, then details-on-demand** (mantra de Ben Shneiderman). Cette sequence constitue la reference pour toute visualisation interactive :
1. Montrer la vue d'ensemble pour donner le contexte general.
2. Permettre de zoomer et filtrer pour se concentrer sur un sous-ensemble.
3. Fournir les details a la demande (tooltip, panel, drill-down).

**Linked Views**
Relier plusieurs visualisations de sorte qu'une interaction dans l'une (selection, filtre, survol) se propage aux autres. Cela permet l'exploration multidimensionnelle sans complexifier un graphique unique. Technique native dans Tableau (actions), Power BI (cross-filtering), Observable (viewof), et D3.js (dispatch).

**Animated Transitions**
Utiliser les animations pour montrer les transformations de donnees (changement de filtre, re-tri, changement d'echelle). Les transitions aident le cerveau a comprendre comment les donnees se reorganisent. Duree recommandee : 300-500ms. Au-dela, les transitions deviennent une source de friction.

**Responsive Design**
Concevoir les visualisations pour fonctionner sur differentes tailles d'ecran. Strategies :
- Desktop : interactions riches (hover, drag, zoom).
- Tablette : interactions tactiles (tap, pinch-to-zoom).
- Mobile : simplifier (big numbers, sparklines, listes scrollables). Ne pas tenter de reproduire un dashboard desktop sur mobile — creer une experience adaptee.

---

## Tools Comparison — In-Depth

### Tableau

**Forces** : reference du marche pour l'exploration visuelle. Drag-and-drop intuitif, calculated fields puissants, large communaute (Tableau Public). Capacites VizQL uniques pour le querying visuel. Excellente gestion des large datasets via Hyper engine.
**Limites** : cout eleve (Tableau Creator ~75$/mois par utilisateur), courbe d'apprentissage pour les features avancees (LOD expressions, table calculations). Personnalisation CSS/visuelle limitee. Moins adapte pour les visualisations non-standard.
**Ideal pour** : equipes analytics avec besoin d'exploration ad hoc, organisations avec budget BI significatif, creation de dashboards interactifs complexes.

### Power BI

**Forces** : integration native avec l'ecosysteme Microsoft (Azure, Excel, Teams, SharePoint). Cout competitif (Power BI Pro ~10$/mois par utilisateur). DAX powerful pour les calculs complexes. Bonne gouvernance avec les espaces de travail et les certifications de datasets.
**Limites** : performance variable sur les grands volumes sans Premium capacity. Visualisations custom moins flexibles que Tableau. Dependance a l'ecosysteme Microsoft.
**Ideal pour** : organisations Microsoft-first, equipes avec des analystes familiers d'Excel, scenarios de reporting a grande echelle avec gouvernance.

### D3.js

**Forces** : flexibilite totale — aucune limite sur le type de visualisation. Rendu SVG/Canvas pour des performances maximales. Standard du web pour les visualisations sur mesure. Controle pixel-perfect.
**Limites** : courbe d'apprentissage abrupte (JavaScript + SVG + data joins). Pas de dashboard engine integre. Temps de developpement eleve pour des visualisations basiques. Pas d'interactivite "gratuite" — tout doit etre code.
**Ideal pour** : developpeurs web creant des visualisations interactives embarquees, newsrooms (data journalism), projets necessitant des visualisations non-standard.

### Observable (Observable Framework / Observable Plot)

**Forces** : notebooks reactifs pour le prototypage rapide de visualisations. Observable Plot offre une grammaire de graphiques haut-niveau (successeur spirituel de ggplot2 pour le web). Framework pour deployer des applications data en production. Integration native avec D3.js.
**Limites** : ecosysteme plus jeune, communaute plus petite que D3 ou Tableau. Modele de deploiement specifique (Observable Cloud ou self-hosted via Framework). Moins adapte pour les dashboards entreprise lourds.
**Ideal pour** : data scientists et developpeurs cherchant un prototypage rapide, equipes voulant publier des analyses interactives, transition entre exploration et production.

### Plotly (Plotly.js / Dash / Plotly pour Python et R)

**Forces** : graphiques interactifs out-of-the-box (zoom, hover, export). API disponible en Python, R, Julia et JavaScript. Dash permet de construire des applications analytiques completes en Python. Bonne integration avec les notebooks Jupyter.
**Limites** : esthetique par defaut moins soignee que Tableau ou D3. Performances limitees sur les tres grands datasets cote client. Dash necessite une infrastructure serveur pour le deploiement.
**Ideal pour** : data scientists voulant des visualisations interactives depuis Python/R, equipes construisant des applications analytiques internes, transition notebook-to-app.

### Metabase / Apache Superset

**Forces** : open source, self-hosted, cout zero (hors infrastructure). Interface simple pour les utilisateurs non-techniques. SQL natif pour les analystes. Configuration rapide.
**Limites** : visualisations moins sophistiquees que Tableau/Power BI. Interactivite limitee. Moins de gouvernance enterprise out-of-the-box.
**Ideal pour** : startups et PME, equipes techniques voulant un outil BI leger, complement a un stack data open source.

### Grafana

**Forces** : reference pour le monitoring et les dashboards operationnels temps reel. Support natif de Prometheus, InfluxDB, Elasticsearch et dizaines d'autres data sources. Alerting integre.
**Limites** : concu pour les metriques de monitoring, pas pour l'analyse business. Visualisations limitees pour les analyses exploratoires.
**Ideal pour** : equipes DevOps/SRE, dashboards operationnels temps reel, monitoring d'infrastructure et d'applications.

### Matrice de comparaison synthetique

| Critere | Tableau | Power BI | D3.js | Observable | Plotly/Dash | Metabase |
|---|---|---|---|---|---|---|
| **Facilite d'utilisation** | Haute | Haute | Faible | Moyenne | Moyenne | Haute |
| **Flexibilite visuelle** | Haute | Moyenne | Totale | Haute | Moyenne | Faible |
| **Interactivite** | Haute | Haute | Totale | Haute | Haute | Faible |
| **Cout** | Eleve | Moyen | Gratuit | Gratuit/Moyen | Gratuit/Moyen | Gratuit |
| **Governance enterprise** | Haute | Haute | N/A | Faible | Faible | Faible |
| **Courbe d'apprentissage** | Moyenne | Moyenne | Abrupte | Moyenne | Moyenne | Faible |
| **Embed/Integration web** | Moyenne | Moyenne | Totale | Haute | Haute | Moyenne |
| **Exploration ad hoc** | Excellente | Bonne | Faible | Bonne | Bonne | Bonne |
| **Temps reel** | Moyen | Bon | Bon | Bon | Bon | Faible |
