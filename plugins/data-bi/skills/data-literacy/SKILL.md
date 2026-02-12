---
name: data-literacy
description: This skill should be used when the user asks about "data visualization", "data storytelling", "dashboard design", "statistical thinking", "data culture", "data democratization", "chart selection", "data presentation", "data literacy", "visualisation de données", "narration par les données", "conception de tableaux de bord", "pensée statistique", "culture data", "culture des données", "démocratisation des données", "choix de graphiques", "présentation de données", "littératie des données", "data-driven culture", "culture data-driven", "bar chart vs line chart", "scatter plot", "box plot", "histogram", "heat map", "choropleth", "infographie", "infographic", "D3.js", "Observable", "Matplotlib", "Plotly", "Apache Superset", "cognitive load", "chart junk", "Tufte", "data ink ratio", "misleading charts", or needs guidance on communicating data insights, building visualizations, and fostering data-driven culture.
version: 1.0.0
---

# Data Literacy — Visualization, Storytelling & Data Culture

## Overview

Ce skill couvre l'ensemble des disciplines liees a la litteratie des donnees : la capacite a lire, comprendre, analyser, communiquer et prendre des decisions fondees sur les donnees. Il ne s'adresse pas uniquement aux analystes ou data scientists — il fournit un cadre complet pour toute personne devant interagir avec des donnees dans un contexte professionnel. Appliquer systematiquement les principes decrits ici pour transformer des donnees brutes en insights actionnables, construire des visualisations efficaces, raconter des histoires convaincantes avec les donnees, et favoriser une culture data-driven a l'echelle de l'organisation. La data literacy est le socle sur lequel repose toute strategie analytique : sans elle, les meilleurs outils et les donnees les plus riches restent inexploites.

This skill covers the full spectrum of data literacy: the ability to read, understand, analyze, communicate, and make decisions based on data. Apply these principles to transform raw data into actionable insights, build effective visualizations, craft compelling data narratives, and foster organization-wide data-driven culture.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- **Conception de visualisations et dashboards** : choix du type de graphique, design de tableaux de bord interactifs, application de principes de perception visuelle, selection des couleurs et mise en forme.
- **Communication d'insights analytiques** : structuration d'un narrative arc avec des donnees, preparation de presentations pour differentes audiences (executive, analyste, operationnel), redaction de syntheses executives.
- **Pensee statistique et esprit critique** : interpretation de resultats d'analyses, identification de biais et sophismes courants (correlation vs causalite, biais du survivant, paradoxe de Simpson), evaluation de la qualite et fiabilite des donnees.
- **Selection et comparaison d'outils de visualisation** : evaluation de Tableau, Power BI, D3.js, Observable, Plotly et autres outils selon les besoins du projet.
- **Programmes de data literacy organisationnelle** : conception de programmes de formation, identification de data champions, mesure de la maturite data culture, strategies de democratisation des donnees.
- **Self-service analytics** : mise en place de plateformes permettant aux utilisateurs metier d'explorer les donnees de maniere autonome, gouvernance du self-service, semantic layers.
- **Recommandations actionnables** : passage de l'analyse a l'action, formulation de recommandations claires, mesure de l'impact des decisions data-driven.

## Core Principles

### Principle 1 — Data-Ink Ratio & Clarity Above All

Appliquer le principe fondamental d'Edward Tufte : maximiser le ratio data-ink, c'est-a-dire la proportion d'encre utilisee pour representer les donnees par rapport a l'encre totale du graphique. Supprimer impitoyablement tout element decoratif qui n'apporte pas d'information : grilles excessives, bordures superflues, effets 3D, cliparts, et tout chartjunk. Chaque pixel doit servir la comprehension. "Above all else, show the data" (Tufte). Stephen Few prolonge ce principe avec le concept de signal-to-noise ratio : chaque element visuel doit amplifier le signal (l'insight) et reduire le bruit (la distraction).

### Principle 2 — Audience-First Design

Ne jamais concevoir une visualisation ou un rapport sans identifier d'abord l'audience cible et son contexte de decision. Un dirigeant a besoin d'un executive summary avec des KPIs et des tendances. Un analyste a besoin de granularite et d'interactivite pour explorer les donnees. Un operationnel a besoin d'alertes et de seuils pour agir immediatement. Adapter le niveau de detail, le vocabulaire, le format et le canal de diffusion a chaque audience. Cole Nussbaumer Knaflic formule ce principe ainsi : "Who is your audience and what do you need them to know or do?"

### Principle 3 — Statistical Rigor Without Jargon

Appliquer la rigueur statistique dans chaque analyse sans imposer le jargon technique a l'audience. Toujours contextualiser les chiffres (comparaisons temporelles, benchmarks, intervalles de confiance), signaler explicitement les limites des donnees (taille d'echantillon, biais de selection, donnees manquantes), et distinguer clairement correlation et causalite. Rendre accessible l'incertitude : utiliser des fourchettes plutot que des chiffres precis quand c'est plus honnete, et privilegier les ordres de grandeur quand la precision est trompeuse.

### Principle 4 — Narrative Arc for Every Analysis

Structurer chaque communication analytique comme un recit avec un arc narratif clair : contexte (pourquoi cette analyse ?), tension (quel probleme ou quelle question ?), analyse (qu'est-ce que les donnees revelent ?), et resolution (quelle action recommander ?). Les donnees seules ne convainquent pas — c'est l'histoire qu'elles racontent qui motive l'action. Un bon data storyteller guide l'audience de la question a l'insight puis a l'action, sans perdre la rigueur analytique en route.

### Principle 5 — Democratization with Governance

Favoriser l'acces aux donnees pour tous les collaborateurs tout en maintenant la gouvernance necessaire. La data literacy ne signifie pas que tout le monde doit devenir data scientist, mais que chacun doit pouvoir poser des questions aux donnees et comprendre les reponses. Mettre en place des semantic layers, des definitions metier partagees (metrics dictionaries), et des niveaux d'acces adaptes. Le self-service analytics sans gouvernance produit du chaos ; la gouvernance sans self-service produit des goulots d'etranglement.

### Principle 6 — Ethical Data Communication

Communiquer les donnees avec integrite. Ne jamais manipuler les axes, tronquer les echelles, ou selectionner les donnees pour soutenir une conclusion predeterminee. Presenter les incertitudes et les limites. Respecter la vie privee et l'anonymisation. Appliquer le principe de charite interpretative : quand les donnees sont ambigues, presenter les interpretations alternatives plutot que de choisir celle qui arrange. La confiance dans les donnees est un actif organisationnel fragile — une seule manipulation la detruit durablement.

## Key Frameworks & Methods

### Data Literacy Competency Framework

| Competence | Niveau 1 — Reader | Niveau 2 — Communicator | Niveau 3 — Analyst | Niveau 4 — Champion |
|---|---|---|---|---|
| **Lecture des donnees** | Lire un graphique simple | Interpreter des tendances | Identifier des anomalies | Evaluer la qualite des sources |
| **Interpretation statistique** | Comprendre une moyenne | Comprendre la variance | Evaluer la significativite | Identifier les biais methodologiques |
| **Visualisation** | Lire un dashboard | Choisir le bon graphique | Concevoir un dashboard | Definir des standards visuels org. |
| **Communication** | Decrire un fait chiffre | Structurer un argument | Construire un narrative arc | Former les autres |
| **Esprit critique** | Poser des questions | Identifier des limites | Challenger les hypotheses | Institutionnaliser la culture critique |

### Chart Selection Decision Matrix

| Objectif de communication | Types recommandes | A eviter |
|---|---|---|
| **Comparaison** entre categories | Bar chart (horizontal pour > 5 cat.), Lollipop chart | Pie chart (> 5 segments), 3D bars |
| **Evolution** dans le temps | Line chart, Area chart (pour volumes), Slope chart | Bar chart pour series longues |
| **Distribution** d'une variable | Histogram, Box plot, Violin plot, Density plot | Pie chart, bar chart sans bins |
| **Correlation** entre variables | Scatter plot, Bubble chart, Heatmap | Line chart (implique causalite) |
| **Composition** d'un tout | Stacked bar (peu de cat.), Treemap, Waterfall | Pie chart (> 5 parts), donut |
| **Geographique** | Choropleth, Bubble map, Hex map | Pie charts sur carte |
| **Flux et relations** | Sankey, Chord diagram, Network graph | Diagrammes trop denses |
| **KPI et statut** | Big number + sparkline, Bullet chart, Gauge | Gauges multiples, 3D meters |

### Tufte's Principles Applied

- **Data-ink ratio** : supprimer tout element graphique non informatif. Eliminer gridlines sauf les plus essentielles, retirer les bordures de legende inutiles, simplifier les axes.
- **Lie factor** : s'assurer que la representation visuelle est proportionnelle aux donnees. Lie Factor = (taille de l'effet visuel) / (taille de l'effet reel). Viser un ratio de 1.0.
- **Small multiples** : utiliser des grilles de petits graphiques identiques pour comparer des patterns entre categories ou periodes. Plus efficace que des graphiques superposes.
- **Sparklines** : integrer des micro-graphiques inline dans les tableaux et textes pour montrer les tendances sans interrompre la lecture.

### Knaflic's Storytelling with Data Method

Appliquer le processus en 6 etapes de Cole Nussbaumer Knaflic :
1. **Understand the context** : identifier l'audience, le message cle, et l'action souhaitee.
2. **Choose an appropriate display** : selectionner le type de graphique adapte a l'objectif (voir matrice ci-dessus).
3. **Eliminate clutter** : supprimer tout element superflu en appliquant les principes Gestalt (proximite, similarite, cloture, continuite).
4. **Focus attention** : utiliser la couleur, la taille et le positionnement de maniere strategique pour guider l'oeil vers l'insight principal.
5. **Think like a designer** : appliquer les principes d'accessibilite, de hierarchie visuelle, et d'affordance.
6. **Tell a story** : structurer la presentation avec un arc narratif clair (contexte, tension, resolution).

## Decision Guide

### Arbre de decision — Quel outil de visualisation choisir ?

```
1. Quel est le profil de l'utilisateur principal ?
   +-- Utilisateur metier non-technique -> Tableau, Power BI, Looker
   +-- Analyste data avec competences SQL -> Tableau, Mode Analytics, Metabase
   +-- Developpeur / data engineer -> D3.js, Observable, Plotly, Vega-Lite
   +-- Data scientist (exploration) -> Python (Matplotlib, Seaborn, Plotly), R (ggplot2)

2. Quel est le contexte de deploiement ?
   +-- Dashboard operationnel temps reel -> Power BI (streaming), Grafana, Superset
   +-- Rapport strategique periodique -> Tableau, Power BI, Google Data Studio
   +-- Visualisation interactive embarquee -> D3.js, Plotly.js, Observable
   +-- Exploration ad hoc -> Jupyter + Plotly, Observable notebooks

3. Quel est l'ecosysteme technologique existant ?
   +-- Stack Microsoft (Azure, SQL Server) -> Power BI
   +-- Stack Google (BigQuery, GCP) -> Looker, Google Data Studio
   +-- Stack AWS (Redshift, Athena) -> QuickSight, Tableau Cloud
   +-- Stack open source -> Metabase, Superset, Redash, Grafana
```

### Guide de decision — Communication selon l'audience

| Audience | Format | Niveau de detail | Longueur | Focus |
|---|---|---|---|---|
| **C-Level / Board** | Executive summary, 1-page | Tres synthetique, KPIs | 5 min de lecture max | Impact business, decisions a prendre |
| **Management intermediaire** | Dashboard + commentaire | Synthetique avec drill-down | 15 min | Tendances, ecarts, actions correctives |
| **Analystes / Experts** | Rapport detaille + data | Granulaire, methodologie | 30-60 min | Methodologie, donnees brutes, limites |
| **Equipes operationnelles** | Alertes, seuils, tableaux | Actionnable, temps reel | Immediat | Que faire maintenant ? Quel seuil est depasse ? |

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Progressive Disclosure** : presenter d'abord le message cle (big number, headline), puis permettre l'exploration progressive vers le detail. Un dashboard efficace raconte son histoire en 5 secondes, puis permet 5 minutes d'exploration.
- **Consistent Visual Grammar** : definir et appliquer un design system pour les visualisations (palette de couleurs, typographie, grille, conventions de nommage). La coherence visuelle reduit la charge cognitive et accelere la comprehension.
- **Annotation-Driven Insights** : annoter les graphiques avec le "so what" — expliquer directement sur le graphique pourquoi un point de donnee est significatif, plutot que de forcer l'audience a deviner.
- **Benchmarking Context** : toujours fournir un point de comparaison (periode precedente, objectif, benchmark sectoriel, moyenne). Un chiffre sans contexte est un chiffre sans sens.
- **Pre-Mortem Data Analysis** : avant de communiquer un insight, se demander : "Quelles objections un sceptique intelligent pourrait-il soulever ?" Adresser proactivement ces objections dans la presentation.

### Anti-patterns critiques

- **Chartjunk & Decoration Overload** : ajouter des elements decoratifs (icones, cliparts, effets 3D, gradients) qui distraient du message. Tufte appelle cela le chartjunk. Chaque element decoratif non informatif est du bruit.
- **Misleading Axes** : tronquer l'axe Y pour exagerer les variations, utiliser des axes doubles avec des echelles incompatibles, ou inverser les axes. Ces pratiques detruisent la confiance.
- **Dashboard Sprawl** : creer des dizaines de dashboards sans hierarchie ni curation, resultant en une fatigue de donnees. Consolider, archiver les dashboards non utilises, et definir des dashboards de reference.
- **Correlation Confusion** : presenter une correlation comme une causalite sans evidence experimentale ou quasi-experimentale. Toujours formuler : "X est associe a Y" plutot que "X cause Y" sauf si un design experimental le justifie.
- **Survivorship Bias in Reporting** : ne rapporter que les succes (clients actifs, projets termines) sans analyser les echecs (churn, projets abandonnes). Le biais du survivant est l'un des plus pernicieux en business analytics.
- **Vanity Metrics** : mesurer des metriques flatteuses mais non actionnables (pages vues sans conversion, nombre de leads sans qualification). Toujours lier les metriques a une decision ou une action.

## Implementation Workflow

### Phase 1 — Assessment & Strategy

1. Evaluer le niveau de data literacy actuel de l'organisation avec le Competency Framework (surveys, interviews, tests pratiques).
2. Identifier les cas d'usage prioritaires ou la data literacy aurait le plus grand impact business.
3. Cartographier les outils de visualisation existants et leur taux d'adoption reel.
4. Definir les personas utilisateurs et leurs besoins specifiques en matiere de donnees.
5. Etablir les standards de visualisation et le design system data (palette, conventions, templates).

### Phase 2 — Foundation & Training

6. Deployer une plateforme de self-service analytics adaptee aux profils utilisateurs identifies.
7. Creer un data dictionary et un metrics glossary partages et accessibles.
8. Concevoir et lancer un programme de formation par niveaux (Reader, Communicator, Analyst, Champion).
9. Identifier et former des data champions dans chaque departement.
10. Produire des templates de dashboards et de presentations conformes aux standards.

### Phase 3 — Activation & Practice

11. Mettre en place des data clinics regulieres (sessions ouvertes de revue de dashboards et analyses).
12. Instaurer des revues de visualisation (viz review) sur le modele des code reviews.
13. Lancer des challenges data internes pour stimuler l'adoption et la creativite.
14. Creer une bibliotheque d'exemples de data storytelling reussis dans l'organisation.
15. Etablir des feedback loops entre producteurs et consommateurs de donnees.

### Phase 4 — Measurement & Scaling

16. Mesurer la maturite data culture avec un modele structure (voir reference data-culture.md).
17. Tracker les metriques d'adoption : nombre d'utilisateurs actifs du self-service, frequence de consultation des dashboards, taux de decisions documentees par les donnees.
18. Evaluer l'impact business : reduction du temps de decision, amelioration des KPIs lies aux initiatives data-driven.
19. Iterer sur le programme de formation en fonction des retours et des lacunes identifiees.
20. Etendre le programme aux nouvelles equipes, filiales et partenaires.


## Skills connexes

| Skill | Lien |
|---|---|
| Decision Reporting | `data-bi:decision-reporting-governance` — Dashboards et reporting BI |
| Data Engineering | `data-bi:data-engineering` — Accès aux données et self-service |
| Product Analytics | `code-development:product-analytics` — Métriques produit et analyse |
| Communication | `entreprise:communication` — Data storytelling et présentation exécutive |
| Marketing | `entreprise:marketing` — Reporting marketing et métriques d'acquisition |

## Additional Resources

Consulter les fichiers de reference suivants pour des guides detailles :

- **[Data Visualization](./references/data-visualization.md)** : best practices de visualisation (Tufte, Few, Knaflic), guide de selection de types de graphiques, theorie des couleurs pour les donnees, design UX de dashboards, visualisations interactives, comparaison d'outils (Tableau, Power BI, D3.js, Observable, Plotly).
- **[Data Storytelling](./references/data-storytelling.md)** : arc narratif (setup, conflit, resolution), communication adaptee a l'audience (executive, analyste, operationnel), syntheses executives, synthese d'insights, presentation de resultats analytiques, recommandations actionnables.
- **[Statistical Thinking](./references/statistical-thinking.md)** : frameworks de data literacy, concepts statistiques pour les non-specialistes, pensee critique avec les donnees, sophismes et erreurs d'interpretation courantes, prise de decision data-driven, bases du test d'hypotheses.
- **[Data Culture](./references/data-culture.md)** : programmes de democratisation des donnees, enablement du self-service analytics, data champions et ambassadeurs, programmes de formation et montee en competences, mesure de la maturite data culture, conduite du changement pour l'adoption data.
