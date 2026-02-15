---
name: data-literacy
description: This skill should be used when the user asks about "data visualization", "data storytelling", "dashboard design", "statistical thinking", "data culture", "data democratization", "chart selection", "data presentation", "data literacy", "visualisation de données", "narration par les données", "conception de tableaux de bord", "pensée statistique", "culture data", "culture des données", "démocratisation des données", "choix de graphiques", "présentation de données", "littératie des données", "data-driven culture", "culture data-driven", "bar chart vs line chart", "scatter plot", "box plot", "histogram", "heat map", "choropleth", "infographie", "infographic", "D3.js", "Observable", "Matplotlib", "Plotly", "Apache Superset", "cognitive load", "chart junk", "Tufte", "data ink ratio", "misleading charts", or needs guidance on communicating data insights, building visualizations, and fostering data-driven culture.
version: 1.2.0
last_updated: 2026-02
---

# Data Literacy — Visualization, Storytelling & Data Culture

## Overview

Ce skill couvre les disciplines liees a la litteratie des donnees : la capacite a lire, comprendre, analyser, communiquer et prendre des decisions fondees sur les donnees. Il ne s'adresse pas uniquement aux analystes ou data scientists — il fournit un cadre complet pour toute personne devant interagir avec des donnees dans un contexte professionnel. Appliquer systematiquement les principes decrits ici pour transformer des donnees brutes en insights actionnables, construire des visualisations claires, raconter des histoires convaincantes avec les donnees, et favoriser une culture data-driven a l'echelle de l'organisation. La data literacy est le socle sur lequel repose toute strategie analytique : sans elle, les meilleurs outils et les donnees les plus riches restent inexploites.

This skill covers data literacy: the ability to read, understand, analyze, communicate, and make decisions based on data. Apply these principles to transform raw data into actionable insights, build clear visualizations, craft compelling data narratives, and foster organization-wide data-driven culture.

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

Ne jamais concevoir une visualisation ou un rapport sans identifier d'abord l'audience cible et son contexte de decision. Un dirigeant a besoin d'un executive summary avec 3-5 KPIs, les tendances clés et les decisions a prendre. Un analyste a besoin de granularite et d'interactivite pour explorer les donnees (filtres, drill-down, export SQL). Un operationnel a besoin d'alertes visuelles et de seuils colores (vert/orange/rouge) pour agir en moins de 30 secondes. Adapter le niveau de detail, le vocabulaire, le format et le canal de diffusion a chaque audience. Cole Nussbaumer Knaflic formule ce principe ainsi : "Who is your audience and what do you need them to know or do?"

### Principle 3 — Statistical Rigor Without Jargon

Appliquer la rigueur statistique dans chaque analyse sans imposer le jargon technique a l'audience. Toujours contextualiser les chiffres : ajouter une comparaison temporelle (vs. meme periode N-1), un benchmark (moyenne sectorielle, objectif interne), et un intervalle de confiance quand la precision est incertaine. Signaler explicitement les limites des donnees (taille d'echantillon, biais de selection, donnees manquantes), et distinguer clairement correlation et causalite. Rendre accessible l'incertitude : utiliser des fourchettes plutot que des chiffres precis quand c'est plus honnete, et privilegier les ordres de grandeur quand la precision est trompeuse.

### Principle 4 — Narrative Arc for Every Analysis

Structurer chaque communication analytique comme un recit avec un arc narratif clair : contexte (pourquoi cette analyse ?), tension (quel probleme ou quelle question ?), analyse (qu'est-ce que les donnees revelent ?), et resolution (quelle action recommander ?). Les donnees seules ne convainquent pas — c'est l'histoire qu'elles racontent qui motive l'action. Un bon data storyteller guide l'audience de la question a l'insight puis a l'action, sans perdre la rigueur analytique en route.

### Principle 5 — Democratization with Governance

Favoriser l'acces aux donnees pour tous les collaborateurs tout en maintenant la gouvernance necessaire. La data literacy ne signifie pas que tout le monde doit devenir data scientist, mais que chacun doit pouvoir poser des questions aux donnees et comprendre les reponses. Mettre en place des semantic layers avec des metriques certifiees et documentees, un metrics dictionary accessible a tous (ex: Notion, Confluence, data catalog), et des niveaux d'acces par role (viewer, explorer, analyst). Le self-service analytics sans gouvernance produit du chaos ; la gouvernance sans self-service produit des goulots d'etranglement.

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
4. **Focus attention** : utiliser la couleur, la taille et le positionnement pour guider l'oeil vers l'insight principal — une seule couleur d'accent pour le point cle, gris pour le contexte.
5. **Think like a designer** : appliquer les principes d'accessibilite (contraste WCAG AA minimum), de hierarchie visuelle (titre > sous-titre > annotation > legende), et d'affordance.
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

- **Progressive Disclosure** : presenter d'abord le message cle (big number, headline), puis permettre l'exploration progressive vers le detail. Un dashboard doit raconter son histoire en 5 secondes (le "so what" visible immediatement), puis permettre 5 minutes d'exploration via drill-down et filtres.
- **Consistent Visual Grammar** : definir et appliquer un design system pour les visualisations : palette de 5-7 couleurs maximum (dont 1 couleur d'accent), typographie unique, grille de 12 colonnes, conventions de nommage des metriques. La coherence visuelle reduit la charge cognitive et accelere la comprehension.
- **Annotation-Driven Insights** : annoter les graphiques avec le "so what" — expliquer directement sur le graphique pourquoi un point de donnee est significatif (ex: "Pic du 15 mars : lancement campagne email +45% trafic"), plutot que de forcer l'audience a deviner.
- **Benchmarking Context** : toujours fournir un point de comparaison (periode precedente, objectif, benchmark sectoriel, moyenne). Un chiffre sans contexte est un chiffre sans sens.
- **Pre-Mortem Data Analysis** : avant de communiquer un insight, lister 3 objections qu'un sceptique informé pourrait soulever (ex: "N'est-ce pas un effet de saisonnalité ?", "L'échantillon est-il assez grand ?", "La corrélation implique-t-elle la causalité ?"). Adresser proactivement ces objections dans la presentation.

### Anti-patterns critiques

- **Chartjunk & Decoration Overload** : ajouter des elements decoratifs (icones, cliparts, effets 3D, gradients) qui distraient du message. Tufte appelle cela le chartjunk. Chaque element decoratif non informatif est du bruit.
- **Misleading Axes** : tronquer l'axe Y pour exagerer les variations, utiliser des axes doubles avec des echelles incompatibles, ou inverser les axes. Ces pratiques detruisent la confiance.
- **Dashboard Sprawl** : creer des dizaines de dashboards sans hierarchie ni curation, resultant en une fatigue de donnees. Consolider, archiver les dashboards non utilises, et definir des dashboards de reference.
- **Correlation Confusion** : presenter une correlation comme une causalite sans evidence experimentale ou quasi-experimentale. Toujours formuler : "X est associe a Y" plutot que "X cause Y" sauf si un design experimental le justifie.
- **Survivorship Bias in Reporting** : ne rapporter que les succes (clients actifs, projets termines) sans analyser les echecs (churn, projets abandonnes). Le biais du survivant est l'un des plus pernicieux en business analytics.
- **Vanity Metrics** : mesurer des metriques flatteuses mais non actionnables (pages vues sans conversion, nombre de leads sans qualification). Toujours lier les metriques a une decision ou une action.

## Implementation Workflow

### Phase 1 — Assessment & Strategy

1. Evaluer le niveau de data literacy actuel de l'organisation avec le Competency Framework : faire passer un test pratique de 15 questions couvrant les 5 competences (lecture, statistiques, visualisation, communication, esprit critique), scorer chaque departement sur l'echelle Reader/Communicator/Analyst/Champion.
2. Identifier les 3-5 cas d'usage prioritaires ou la data literacy aurait le plus grand impact business mesurable (ex: reduire le temps de decision du comite de direction de 2h a 30min).
3. Cartographier les outils de visualisation existants et leur taux d'adoption reel (% d'utilisateurs actifs vs. licences payees).
4. Definir les personas utilisateurs et leurs besoins specifiques en matiere de donnees : pour chaque persona, documenter le format prefere, la frequence de consultation, et les 3 questions metier recurrentes.
5. Etablir les standards de visualisation et le design system data : palette de couleurs (5-7 couleurs max), typographie, grille de layout, conventions de nommage des KPIs, templates de dashboards.

### Phase 2 — Foundation & Training

6. Deployer une plateforme de self-service analytics adaptee aux profils utilisateurs identifies.
7. Creer un data dictionary et un metrics glossary partages et accessibles, avec pour chaque metrique : nom, definition, formule de calcul, source, owner, frequence de mise a jour.
8. Concevoir et lancer un programme de formation par niveaux (Reader : 2h, Communicator : 4h, Analyst : 8h, Champion : 16h + mentorat).
9. Identifier et former 1-2 data champions par departement : les former au niveau Analyst minimum et leur donner du temps dedie (10-20% de leur temps).
10. Produire des templates de dashboards et de presentations conformes aux standards definis en phase 1.

### Phase 3 — Activation & Practice

11. Mettre en place des data clinics regulieres (sessions ouvertes de revue de dashboards et analyses) : 1h par semaine, ouvertes a tous.
12. Instaurer des revues de visualisation (viz review) sur le modele des code reviews : chaque nouveau dashboard passe une revue avant publication, verifiee contre la checklist de revue (voir Template actionnable).
13. Lancer des challenges data internes pour stimuler l'adoption et la creativite (ex: "Meilleur dashboard du trimestre", "Insight le plus impactant").
14. Creer une bibliotheque d'exemples de data storytelling reussis dans l'organisation.
15. Etablir des feedback loops entre producteurs et consommateurs de donnees : chaque dashboard a un canal de feedback (Slack, formulaire) et les retours sont traites sous 48h.

### Phase 4 — Measurement & Scaling

16. Mesurer la maturite data culture avec un modele structure (voir reference data-culture.md).
17. Tracker les metriques d'adoption : nombre d'utilisateurs actifs du self-service par semaine, frequence mediane de consultation des dashboards, taux de decisions documentees par les donnees (objectif : > 50% des decisions du comite de direction).
18. Evaluer l'impact business : reduction du temps de decision (en heures), amelioration des KPIs lies aux initiatives data-driven (ex: conversion +X%, churn -Y%).
19. Iterer sur le programme de formation en fonction des retours et des lacunes identifiees.
20. Etendre le programme aux nouvelles equipes, filiales et partenaires.


## Modèle de maturité

### Niveau 1 — Analphabète
- Les collaborateurs ne savent pas lire un graphique ni interpréter des métriques de base
- Aucun programme de formation data, les décisions reposent sur l'intuition ou l'anecdote
- Pas d'outil de self-service analytics, les données sont accessibles uniquement via l'équipe IT
- **Indicateurs** : < 5% de collaborateurs formés aux fondamentaux data, adoption self-service = 0%

### Niveau 2 — Sensibilisé
- Sensibilisation initiale aux données avec des formations ponctuelles pour les managers
- Les collaborateurs peuvent lire des dashboards simples mais ne questionnent pas les données
- Un ou deux outils BI déployés avec une adoption limitée aux équipes analytiques
- **Indicateurs** : 10-25% de collaborateurs formés, adoption self-service < 15%

### Niveau 3 — Autonome
- Programme de formation structuré par niveaux (Reader, Communicator, Analyst) déployé
- Les utilisateurs métier explorent les données de manière autonome via des datasets certifiés
- Data champions identifiés dans chaque département, data clinics régulières en place
- **Indicateurs** : 40-60% de collaborateurs formés, adoption self-service > 40%, qualité des présentations data évaluée

### Niveau 4 — Ambassadeur
- Réseau d'ambassadeurs data actif qui forme et accompagne leurs pairs au quotidien
- Les présentations exécutives appliquent systématiquement les principes de data storytelling
- Self-service analytics mature avec semantic layer, métriques certifiées et gouvernance
- **Indicateurs** : 70-85% de collaborateurs formés, adoption self-service > 65%, data-driven decisions ratio > 60%

### Niveau 5 — Data-driven Culture
- La data literacy est un prérequis pour tous les postes, intégrée dans les parcours d'onboarding
- Chaque décision stratégique est documentée par des données avec traçabilité complète
- Innovation data bottom-up avec des initiatives data portées par les métiers eux-mêmes
- **Indicateurs** : > 90% de collaborateurs formés, adoption self-service > 85%, data-driven decisions ratio > 80%

## Rythme opérationnel

| Cadence | Activité | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Hebdomadaire** | Data tips et micro-learning (newsletter, Slack, intranet) | Data Champion | Contenu de micro-formation publié |
| **Hebdomadaire** | Data clinic ouverte (revue de dashboards et analyses) | Data Analyst + Data Champion | Feedback et améliorations documentés |
| **Mensuel** | Session de formation data literacy (par niveau de compétence) | Data Literacy Lead | Attestation de participation et évaluation |
| **Mensuel** | Revue des métriques d'adoption self-service et d'usage BI | Data Analyst | Rapport d'adoption et recommandations |
| **Trimestriel** | Évaluation de la maturité data culture (survey + métriques) | Data Literacy Lead + RH | Scorecard de maturité et plan d'action |
| **Trimestriel** | Atelier de data storytelling et best practices de visualisation | Data Champion + Communication | Bibliothèque d'exemples mise à jour |
| **Annuel** | Actualisation du plan de formation data literacy et certifications | Data Literacy Lead + RH + CDO | Plan de formation annuel et budget certifications |

## State of the Art (2025-2026)

La data literacy s'accélère avec l'IA et les nouvelles réglementations :

- **Natural language analytics** : Les interfaces en langage naturel (Thoughtspot, Tableau AI) permettent à des non-techniciens de poser des questions aux données directement.
- **Data storytelling assisté par IA** : Les outils génèrent automatiquement des narratifs à partir des données, aidant les analystes à communiquer leurs insights.
- **Mandatory data literacy** : Les programmes de data literacy deviennent obligatoires dans les grandes organisations, souvent liés aux objectifs ESG et de transformation digitale.
- **Visual analytics avancés** : Les techniques de visualisation s'enrichissent (small multiples, sparklines, annotations intelligentes) pour communiquer plus efficacement.
- **Collaborative analytics** : Les notebooks collaboratifs (Observable, Hex, Deepnote) rapprochent l'analyse et la prise de décision en permettant l'exploration partagée.

## Template actionnable

### Checklist de revue de dashboard

| Critère | Vérifié | Commentaire |
|---|---|---|
| **Message clair** — Le "so what" est évident en 5 secondes | ☐ | ___ |
| **Audience** — Adapté au niveau du destinataire | ☐ | ___ |
| **Graphiques** — Types appropriés aux données | ☐ | ___ |
| **Axes** — Échelles cohérentes, non tronquées | ☐ | ___ |
| **Couleurs** — Palette accessible, usage sémantique | ☐ | ___ |
| **Contexte** — Benchmarks ou comparaisons fournis | ☐ | ___ |
| **Annotations** — Insights clés annotés sur les graphiques | ☐ | ___ |
| **Filtres** — Drill-down disponible sans surcharge | ☐ | ___ |
| **Sources** — Données sourcées et datées | ☐ | ___ |
| **Mobile** — Lisible sur petit écran si nécessaire | ☐ | ___ |

## Prompts types

- "Comment choisir le bon type de graphique pour mes données ?"
- "Aide-moi à structurer une présentation data storytelling"
- "Propose un programme de formation data literacy pour nos équipes"
- "Comment éviter les erreurs statistiques courantes dans nos analyses ?"
- "Aide-moi à concevoir un dashboard lisible et actionnable"
- "Quelles bonnes pratiques pour démocratiser l'accès aux données ?"

## Limites et Red Flags

Ce skill n'est PAS adapté pour :
- ❌ Construire les pipelines de données, configurer dbt ou orchestrer des workflows Airflow → Utiliser plutôt : `data-bi:data-engineering`
- ❌ Mettre en place un programme de data governance, un data catalog ou des data contracts → Utiliser plutôt : `data-bi:decision-reporting-governance`
- ❌ Réaliser des analyses statistiques avancées (tests A/B, régressions, séries temporelles, modèles prédictifs) → Utiliser plutôt : un statisticien ou un data scientist
- ❌ Concevoir l'UI/UX d'une application web ou mobile (design system applicatif, composants React) → Utiliser plutôt : `code-development:ui-ux`
- ❌ Rédiger une stratégie de communication corporate ou des supports marketing → Utiliser plutôt : `entreprise:communication` ou `entreprise:marketing`

Signaux d'alerte en cours d'utilisation :
- ⚠️ La présentation contient plus de 10 graphiques sans fil conducteur narratif — signe d'un "data dump" qui ne convaincra personne
- ⚠️ Un graphique utilise plus de 7 couleurs différentes ou des effets 3D — la charge cognitive dépasse la capacité d'interprétation
- ⚠️ Les conclusions sont présentées sans mentionner les limites des données (taille d'échantillon, période couverte, biais potentiels) — signe de surconfiance qui érode la crédibilité
- ⚠️ Le programme de data literacy est conçu uniquement par l'équipe data sans impliquer les RH ni les managers métier — l'adoption sera faible car déconnectée des besoins réels

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

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.
