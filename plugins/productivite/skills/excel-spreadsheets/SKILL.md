---
name: excel-spreadsheets
description: This skill should be used when the user asks about "Excel advanced formulas", "spreadsheet modeling", "Power Query", "Power Pivot", "VBA macros", "Google Sheets", "Apps Script", "pivot tables", "data validation", "conditional formatting", "XLOOKUP", "dynamic arrays", "LAMBDA functions", "Excel dashboards", "financial modeling spreadsheet", "formules Excel avancées", "tableaux croisés dynamiques", "modélisation données", "automatisation Excel", "macros VBA", "Google Sheets avancé", "Power BI connection", "data cleaning spreadsheet", "sparklines", "Power Map", discusses advanced spreadsheet techniques, data modeling, or needs guidance on Excel/Sheets automation, formulas, and professional-grade spreadsheet solutions.
version: 1.0.0
last_updated: 2026-02
---

# Excel & Spreadsheets Avances / Advanced Spreadsheets

## Overview

**FR** — Cette skill couvre les pratiques avancees de travail sur tableurs : formules complexes (XLOOKUP, dynamic arrays, LAMBDA), modelisation de donnees (Power Pivot, DAX), automatisation (VBA, Apps Script), ETL dans le tableur (Power Query, M language), tableaux croises dynamiques avances, construction de dashboards interactifs, et modelisation financiere professionnelle. Le tableur reste L'OUTIL fondamental de traitement de donnees dans toute organisation — de la PME au grand groupe. Maitriser ses capacites avancees, c'est transformer un outil de saisie en veritable plateforme de decision. Les recommandations couvrent Excel (desktop, web, Microsoft 365), Google Sheets, et les fonctionnalites 2024-2026 : Python in Excel, Copilot, dynamic arrays, LAMBDA functions, et l'integration Power BI.

**EN** — This skill covers advanced spreadsheet practices: complex formulas (XLOOKUP, dynamic arrays, LAMBDA), data modeling (Power Pivot, DAX), automation (VBA, Apps Script), in-spreadsheet ETL (Power Query, M language), advanced pivot tables, interactive dashboard construction, and professional financial modeling. The spreadsheet remains THE foundational data processing tool in every organization — from SMBs to large enterprises. Mastering its advanced capabilities transforms a data-entry tool into a genuine decision platform. Recommendations cover Excel (desktop, web, Microsoft 365), Google Sheets, and 2024-2026 features: Python in Excel, Copilot, dynamic arrays, LAMBDA functions, and Power BI integration.

---

## When This Skill Applies

Activate this skill when the user:

- Construit ou optimise des formules avancees (XLOOKUP, FILTER, SORT, UNIQUE, LAMBDA, LET, dynamic arrays)
- Concoit un modele de donnees dans un tableur (couches Input/Calculation/Output, relations entre tables)
- Automatise des taches repetitives avec VBA (Excel) ou Apps Script (Google Sheets)
- Met en place un pipeline ETL avec Power Query (connexion, transformation, chargement)
- Construit des dashboards interactifs dans Excel ou Google Sheets (slicers, graphiques dynamiques, KPIs)
- Developpe un modele financier professionnel (projections, scenarios, sensitivity analysis)
- Implemente des regles de validation de donnees et de controle qualite dans un classeur
- Migre entre Excel et Google Sheets, ou integre un tableur avec Power BI, bases de donnees, ou APIs

---

## Core Principles

### 1. Structure Before Formula
Concevoir l'architecture du classeur avant d'ecrire la premiere formule. Definir les couches (Input, Calculation, Output), les plages nommees, et les tables structurees. Un classeur bien structure rend les formules plus simples, plus lisibles, et plus maintenables. Ne jamais commencer par les formules — commencer par le modele de donnees. / Design the workbook architecture before writing the first formula. Define layers (Input, Calculation, Output), named ranges, and structured tables. A well-structured workbook makes formulas simpler, more readable, and more maintainable.

### 2. Single Source of Truth
Chaque donnee ne doit exister qu'une seule fois dans le classeur. Utiliser des references (formules, liens entre feuilles, XLOOKUP) plutot que la duplication. Si une valeur est copiee-collee a plusieurs endroits, c'est un defaut de conception. Centraliser les parametres dans une feuille dediee "Config" ou "Parametres". / Every data point should exist only once in the workbook. Use references (formulas, cross-sheet links, XLOOKUP) rather than duplication. If a value is copy-pasted in multiple places, it is a design defect.

### 3. Scalability by Design
Construire chaque classeur pour supporter 10x le volume actuel sans modification structurelle. Utiliser des tables structurees (Ctrl+T) qui s'etendent automatiquement. Privilegier les dynamic arrays qui s'adaptent a la taille des donnees. Eviter les references codees en dur (A1:A100) — utiliser des references de table (Table1[Column]) ou des plages nommees dynamiques. / Build every workbook to handle 10x the current volume without structural changes. Use structured tables (Ctrl+T) that expand automatically. Prefer dynamic arrays that adapt to data size.

### 4. Automation of Repetitive Tasks
Si une action est executee plus de 3 fois par semaine, elle doit etre automatisee. Utiliser Power Query pour l'import et la transformation de donnees recurentes. Utiliser VBA ou Apps Script pour les operations complexes (generation de rapports, envoi d'emails, interaction avec d'autres systemes). L'objectif : zero manipulation manuelle de donnees dans les processus recurrents. / If an action is performed more than 3 times per week, it must be automated. Use Power Query for recurring data import and transformation. Use VBA or Apps Script for complex operations.

### 5. Data Validation at Entry
La qualite des donnees se joue a la saisie, pas apres. Implementer des listes deroulantes, des regles de validation, des messages d'erreur clairs, et des formats conditionels pour guider l'utilisateur. Chaque cellule de saisie doit avoir une contrainte explicite (type, plage, format). Un classeur sans validation est un classeur dont les resultats sont infiables. / Data quality is determined at entry, not after. Implement dropdown lists, validation rules, clear error messages, and conditional formatting to guide the user.

### 6. Documentation & Auditability
Chaque classeur professionnel doit inclure : une feuille "Lisez-moi" (objectif, auteur, version, instructions), des commentaires sur les formules complexes, un historique des modifications, et un schema de couleurs coherent (bleu = saisie, vert = formule, gris = reference). Un classeur non documente est un classeur jetable. / Every professional workbook must include: a "ReadMe" sheet (purpose, author, version, instructions), comments on complex formulas, a change log, and a consistent color scheme.

---

## Key Frameworks & Methods

### Data Model Architecture

| Layer | Purpose | Content | Color Convention |
|---|---|---|---|
| **Input** | Saisie et importation des donnees brutes | Donnees source, parametres, hypotheses | Bleu clair (cellules editables) |
| **Calculation** | Logique metier et transformations | Formules, tables intermediaires, lookups | Blanc (ne pas toucher) |
| **Output** | Resultats et presentation | Dashboards, rapports, exports | Vert clair (lecture seule) |
| **Config** | Parametres globaux et references | Listes de validation, constantes, taux | Jaune (parametres) |

### Formula Complexity Matrix

| Niveau | Fonctions | Cas d'usage |
|---|---|---|
| **Basique** | SUM, AVERAGE, COUNT, IF, VLOOKUP | Agregations simples, recherches basiques |
| **Intermediaire** | INDEX/MATCH, SUMIFS, COUNTIFS, TEXT, DATE | Recherches multi-criteres, formatage conditionnel |
| **Avance** | XLOOKUP, FILTER, SORT, UNIQUE, SORTBY | Tableaux dynamiques, tri et filtrage en formule |
| **Expert** | LAMBDA, MAP, REDUCE, SCAN, MAKEARRAY, LET | Fonctions personnalisees, recursivite, abstraction |
| **Power User** | Power Query M, DAX, Python in Excel | ETL, modelisation dimensionnelle, analyse statistique |

### Power Query ETL Pipeline

1. **Connect** — Se connecter aux sources (fichiers, bases de donnees, APIs, web, SharePoint, dossiers)
2. **Clean** — Supprimer les lignes vides, corriger les types, gerer les erreurs et les valeurs manquantes
3. **Transform** — Pivoter/depivoter, fusionner des requetes, ajouter des colonnes calculees, grouper
4. **Shape** — Renommer les colonnes, reordonner, filtrer, appliquer les conventions de nommage
5. **Load** — Charger vers une table structuree, un modele de donnees, ou une connexion seule

### VBA / Apps Script Decision Guide

| Critere | VBA (Excel) | Apps Script (Google Sheets) |
|---|---|---|
| **Environnement** | Desktop Excel (Windows/Mac) | Google Sheets (navigateur) |
| **Execution** | Locale, rapide, acces systeme fichiers | Cloud, latence reseau, acces APIs Google |
| **Declenchement** | Boutons, evenements, raccourcis | Triggers (temps, evenement, menu) |
| **Integration** | COM/OLE, systeme de fichiers, Outlook | Gmail, Drive, Calendar, BigQuery, APIs REST |
| **Collaboration** | Fichier individuel, macros embarquees | Partage natif, scripts lie au fichier ou standalone |
| **Securite** | Macros signees, Trust Center | OAuth, permissions granulaires |
| **Recommandation** | Traitement local rapide, fichiers lourds | Automatisation cloud, collaboration, integration Google |

---

## Decision Guide

### Choosing Formula vs Power Query vs VBA

```
La tache est-elle une transformation de donnees recurrente ?
├── OUI → Les donnees viennent-elles d'une source externe ?
│   ├── OUI → POWER QUERY (ETL automatise, rafraichissable)
│   └── NON → La transformation est-elle complexe (multi-etapes) ?
│       ├── OUI → POWER QUERY (plus lisible que des formules imbriquees)
│       └── NON → FORMULES (dynamic arrays : FILTER, SORT, UNIQUE)
└── NON → La tache implique-t-elle une interaction UI ou systeme ?
    ├── OUI → VBA / APPS SCRIPT (UserForms, fichiers, emails)
    └── NON → La tache est-elle un calcul ponctuel ?
        ├── OUI → FORMULE (XLOOKUP, SUMIFS, LET)
        └── NON → Evaluer si un outil externe est plus adapte
```

### Choosing Excel vs Google Sheets

```
Le classeur necessite-t-il des fonctionnalites avancees ?
├── Power Query / Power Pivot / DAX → EXCEL
├── VBA avec acces systeme de fichiers → EXCEL
├── Fichiers > 100 Mo ou > 1M lignes → EXCEL
├── Integration native Google (Gmail, Drive, BigQuery) → GOOGLE SHEETS
├── Collaboration temps reel multi-utilisateurs → GOOGLE SHEETS
├── Automatisation cloud (triggers, APIs) → GOOGLE SHEETS
└── Usage mixte → EXCEL 365 (cloud + desktop)
```

### Choosing Pivot Table vs Power Pivot

```
Le volume de donnees depasse-t-il 1M de lignes ?
├── OUI → POWER PIVOT (modele de donnees en memoire, compression)
├── NON → Avez-vous besoin de relations entre plusieurs tables ?
│   ├── OUI → POWER PIVOT (star schema, relations DAX)
│   └── NON → Avez-vous besoin de mesures calculees complexes (YTD, rolling) ?
│       ├── OUI → POWER PIVOT (DAX time intelligence)
│       └── NON → TABLEAU CROISE DYNAMIQUE standard
```

---

## Common Patterns & Anti-Patterns

### Patterns (Do)

- **Named Ranges & Structured Tables** : Convertir chaque plage de donnees en table structuree (Ctrl+T). Utiliser des noms significatifs (tbl_Ventes, rng_TauxTVA). Les formules deviennent lisibles : `=SUMIFS(tbl_Ventes[Montant], tbl_Ventes[Region], "Nord")` au lieu de `=SUMIFS($F$2:$F$10000, $C$2:$C$10000, "Nord")`
- **Dynamic Arrays for Self-Sizing Results** : Utiliser FILTER, SORT, UNIQUE, SEQUENCE pour creer des resultats qui s'ajustent automatiquement a la taille des donnees. Eliminer les formules recopiees sur des milliers de lignes
- **Helper Columns for Complex Logic** : Decomposer les formules complexes en colonnes intermediaires nommees explicitement. Une formule de 200 caracteres est un bug en attente. Privilegier 3 colonnes simples a 1 formule imbrique
- **Systematic Error Handling** : Encapsuler les formules critiques avec IFERROR ou IFNA et un message d'erreur explicite. Utiliser LET pour verifier les preconditions avant le calcul principal
- **Input-Calc-Output Separation** : Separer strictement les feuilles de saisie (Input), de calcul (Calc), et de restitution (Output). Proteger les feuilles de calcul. Ne jamais melanger saisie et formules dans la meme cellule
- **Version Control via Change Log** : Maintenir une feuille "Changelog" avec la date, l'auteur, et la description de chaque modification significative. Sauvegarder des versions nommees a chaque jalon

### Anti-Patterns (Avoid)

- **Hardcoded Values in Formulas** : Eviter `=B5*0.20` — utiliser une cellule nommee taux_TVA et ecrire `=B5*taux_TVA`. Les valeurs codees en dur sont invisibles, introuvables, et inchangeables a l'echelle
- **Merged Cells** : Les cellules fusionnees cassent le tri, le filtrage, les tableaux croises dynamiques, les formules de recherche, et Power Query. Utiliser "Center Across Selection" pour l'esthetique sans fusion
- **One Giant Sheet** : Ne jamais placer donnees brutes, calculs, parametres et resultats dans une seule feuille. Cela rend le classeur illisible, fragile et impossible a auditer
- **No Data Validation** : Un classeur de saisie sans listes deroulantes, sans contraintes de type, sans messages d'erreur est un generateur d'erreurs. La validation a la saisie est obligatoire
- **Circular References** : Les references circulaires (meme iteratives) rendent le classeur imprevisible et difficile a deboguer. Restructurer la logique pour les eliminer
- **Volatile Functions Everywhere** : Les fonctions volatiles (INDIRECT, OFFSET, TODAY, NOW, RAND) se recalculent a chaque modification. Utiliser INDEX, XLOOKUP et des plages nommees a la place pour les references dynamiques

---

## Implementation Workflow

### Phase 1 — Audit & Structure (Jour 1-2)
Auditer le classeur existant ou definir les besoins du nouveau classeur. Identifier les sources de donnees, les utilisateurs, les outputs attendus. Definir l'architecture en couches (Input/Calc/Output/Config). Creer le squelette du classeur avec les feuilles nommees, les conventions de couleur, et la feuille ReadMe.

### Phase 2 — Data Model (Jour 3-5)
Importer les donnees sources via Power Query ou connexion directe. Creer les tables structurees avec les types et formats corrects. Definir les relations entre tables (Power Pivot si necessaire). Mettre en place les regles de validation sur toutes les cellules de saisie. Configurer les plages nommees et les listes de reference.

### Phase 3 — Formulas & Logic (Jour 6-10)
Implementer la logique metier couche par couche : d'abord les calculs intermediaires, puis les agregations, enfin les KPIs finaux. Utiliser LET pour la lisibilite, XLOOKUP pour les recherches, dynamic arrays pour les resultats variables. Tester chaque formule avec des cas limites (zero, vide, erreur, valeurs extremes).

### Phase 4 — Automation (Jour 11-13)
Identifier les taches manuelles repetitives et les automatiser. Configurer le rafraichissement automatique de Power Query. Creer les macros VBA ou Apps Script pour la generation de rapports, l'envoi d'alertes, et les operations par lot. Documenter chaque macro (objectif, declenchement, dependances).

### Phase 5 — Dashboards & Delivery (Jour 14-15)
Construire les dashboards de restitution : graphiques dynamiques, slicers, KPIs en cartes. Appliquer les principes de design (hierarchie visuelle, contraste, alignement). Proteger les feuilles sensibles. Tester avec les utilisateurs finaux. Livrer avec documentation et formation.

---

## Modele de maturite

### Niveau 1 — Basique
- Classeurs ad-hoc sans structure, formules simples (SUM, IF, VLOOKUP)
- Donnees copiees-collees manuellement, pas de validation, pas de documentation
- Fichiers individuels non partages, pas de convention de nommage
- **Indicateurs** : taux d'erreur > 10%, temps de production de rapport > 2 heures

### Niveau 2 — Structure
- Tables structurees, plages nommees, separation Input/Output basique
- Formules intermediaires (SUMIFS, INDEX/MATCH), quelques graphiques
- Classeurs partages sur un drive, conventions de nommage en place
- **Indicateurs** : taux d'erreur 3-10%, temps de rapport 30min-2h

### Niveau 3 — Automatise
- Power Query pour l'import de donnees, formules avancees (XLOOKUP, FILTER, LET)
- Tableaux croises dynamiques connectes, dashboards avec slicers
- Macros VBA/Apps Script pour les taches recurrentes, documentation systematique
- **Indicateurs** : taux d'erreur < 3%, temps de rapport < 30 min, rafraichissement automatise

### Niveau 4 — Modele
- Power Pivot avec modele dimensionnel (star schema), mesures DAX
- Power Query enchaine en pipeline ETL complet, parametrise et robuste
- Integration Power BI, classeurs templates reutilisables, gouvernance des versions
- **Indicateurs** : taux d'erreur < 1%, rapport genere en < 5 min, zero saisie manuelle

### Niveau 5 — Predictif
- Python in Excel pour l'analyse statistique et le machine learning
- Copilot pour la generation assistee de formules et l'analyse exploratoire
- Classeurs connectes en temps reel aux sources de donnees, self-service analytics
- **Indicateurs** : taux d'erreur < 0.1%, insights en temps reel, adoption self-service > 80%

---

## Rythme operationnel

| Cadence | Activite | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Quotidien** | Rafraichissement Power Query et verification des alertes | Analyste | Donnees a jour, anomalies signalees |
| **Hebdomadaire** | Revue qualite des classeurs critiques (erreurs, coherence) | Analyste Senior | Rapport de qualite, corrections appliquees |
| **Mensuel** | Audit des classeurs partages (versions, permissions, doublons) | Responsable Data | Registre des classeurs mis a jour |
| **Mensuel** | Optimisation des classeurs lents (formules volatiles, taille) | Power User | Performance amelioree, taille reduite |
| **Trimestriel** | Revue des templates et standards (nouvelles fonctionnalites) | Responsable Data | Templates actualises, guide mis a jour |
| **Trimestriel** | Formation des utilisateurs aux nouvelles fonctions | Formateur | Support de formation, quiz de validation |
| **Annuel** | Migration et archivage des classeurs obsoletes | Responsable Data | Archivage, nettoyage du drive |

---

## State of the Art (2025-2026)

Les tableurs evoluent vers l'intelligence augmentee et la programmabilite :

- **Dynamic Arrays (natif depuis Excel 365)** : FILTER, SORT, UNIQUE, SEQUENCE, SORTBY, RANDARRAY transforment fondamentalement la facon de travailler. Une seule formule remplace des centaines de formules recopiees. C'est le changement le plus important dans Excel depuis les tableaux croises dynamiques.
- **LAMBDA & fonctions nommees** : LAMBDA permet de creer des fonctions personnalisees sans VBA. Combine avec MAP, REDUCE, SCAN et MAKEARRAY, cela transforme Excel en un veritable langage fonctionnel. Les organisations peuvent creer des bibliotheques de fonctions reutilisables.
- **Python in Excel (GA 2024-2025)** : Integration native de Python dans les cellules Excel. Acces a pandas, matplotlib, scikit-learn directement dans le classeur. Execution dans le cloud Azure, pas d'installation locale. Ideal pour l'analyse statistique avancee et la visualisation.
- **Copilot in Excel (2024-2026)** : L'IA generative assiste la creation de formules, l'analyse de donnees, la generation de graphiques, et la mise en forme. Permet aux utilisateurs intermediaires d'acceder a des fonctionnalites avancees via le langage naturel.
- **Google Sheets AI** : Smart Fill et Smart Cleanup pour le nettoyage automatise des donnees. Integration Duet AI pour l'assistance contextuelle. Connecteurs natifs BigQuery pour l'analyse a grande echelle.
- **Connected Spreadsheets** : Les tableurs deviennent des interfaces connectees aux systemes d'entreprise. Power BI connected tables, Google Sheets BigQuery connector, Excel data types lies a des sources externes. Le tableur comme couche de presentation, pas de stockage.

---

## Template actionnable

### Checklist qualite classeur professionnel

| # | Critere | Statut | Commentaire |
|---|---------|--------|-------------|
| 1 | Feuille ReadMe avec objectif, auteur, version, date | ☐ | ___ |
| 2 | Architecture Input/Calc/Output respectee | ☐ | ___ |
| 3 | Toutes les donnees en tables structurees (Ctrl+T) | ☐ | ___ |
| 4 | Zero cellules fusionnees | ☐ | ___ |
| 5 | Plages nommees pour les constantes et parametres | ☐ | ___ |
| 6 | Validation de donnees sur toutes les cellules de saisie | ☐ | ___ |
| 7 | Code couleur coherent (bleu=saisie, blanc=formule, vert=output) | ☐ | ___ |
| 8 | Zero valeurs codees en dur dans les formules | ☐ | ___ |
| 9 | Gestion d'erreur (IFERROR/IFNA) sur les formules critiques | ☐ | ___ |
| 10 | Feuilles protegees (sauf Input) | ☐ | ___ |
| 11 | Power Query parametrise (pas de chemins codes en dur) | ☐ | ___ |
| 12 | Macros documentees (objectif, auteur, declenchement) | ☐ | ___ |
| 13 | Changelog a jour | ☐ | ___ |
| 14 | Taille du fichier < 50 Mo (sinon optimiser) | ☐ | ___ |
| 15 | Test avec cas limites (vide, zero, erreur, volume max) | ☐ | ___ |

---

## Prompts types

- "Aide-moi a concevoir un modele financier professionnel dans Excel avec scenarios et sensitivity analysis"
- "Comment migrer mes formules VLOOKUP vers XLOOKUP et dynamic arrays ?"
- "Propose une architecture Power Query pour consolider 12 fichiers mensuels automatiquement"
- "Ecris une macro VBA pour generer un rapport PDF a partir de mon tableau de bord Excel"
- "Comment construire un dashboard interactif dans Google Sheets avec QUERY et slicers ?"
- "Aide-moi a optimiser un classeur Excel de 200 Mo qui met 30 secondes a se recalculer"
- "Comment utiliser LAMBDA et MAP pour creer des fonctions reutilisables dans Excel 365 ?"
- "Propose un modele de validation de donnees complet pour un formulaire de saisie Excel"

---

## Limites et Red Flags

Ce skill n'est PAS adapte pour :
- Concevoir des dashboards BI professionnels (Power BI, Tableau, Looker) → Utiliser plutot : `data-bi:decision-reporting-governance`
- Construire des pipelines de donnees industriels (Airflow, dbt, Kafka) → Utiliser plutot : `data-bi:data-engineering`
- Developper des applications metier complexes (au-dela du tableur) → Utiliser plutot : `productivite:nocode-apps`
- Gerer la gouvernance et la qualite des donnees a l'echelle de l'entreprise → Utiliser plutot : `data-bi:decision-reporting-governance`
- Realiser des analyses statistiques avancees necessitant R ou Python standalone → Utiliser plutot : `data-bi:data-engineering` ou un skill dedie data science

Signaux d'alerte en cours d'utilisation :
- Un classeur depasse 100 Mo ou 500 000 lignes sans Power Pivot — il faut migrer vers un modele de donnees ou une base de donnees
- Les formules depassent 3 niveaux d'imbrication — decomposer avec LET ou des colonnes helper
- Plusieurs utilisateurs editent le meme classeur et se plaignent de conflits — evaluer Google Sheets ou SharePoint co-authoring
- Un rapport prend plus de 15 minutes a produire manuellement chaque semaine — automatiser avec Power Query + VBA/Apps Script
- Des decisions critiques reposent sur un classeur sans validation ni audit — risque operationnel majeur

---

## Skills connexes

| Skill | Lien |
|---|---|
| Decision Reporting & Governance | `data-bi:decision-reporting-governance` — Dashboards BI, KPIs, gouvernance des donnees |
| Data Engineering | `data-bi:data-engineering` — Pipelines de donnees, ETL industriel, orchestration |
| Data Literacy | `data-bi:data-literacy` — Lecture de donnees, data storytelling, culture data |
| NoCode Apps | `productivite:nocode-apps` — Applications metier sans code |
| AI Copilots Productivite | `productivite:ai-copilots-productivite` — IA generative pour la productivite |
| Automatisation Workflows | `productivite:automatisation-workflows` — Automatisation des processus metier |
| Finance | `entreprise:finance` — Modelisation financiere, budgets, previsions |

---

## Additional Resources

Consult these reference files for deep dives on each topic area:

- **[Formulas & Power Query](./references/formulas-power-query.md)** — XLOOKUP, dynamic arrays (FILTER, SORT, UNIQUE, SEQUENCE), LAMBDA et fonctions nommees (MAP, REDUCE, SCAN, MAKEARRAY), LET pour la lisibilite, Power Query fundamentals et M language, ETL patterns, performance optimization des formules.

- **[VBA & Apps Script](./references/vba-apps-script.md)** — VBA fundamentals (modules, procedures, variables, objets), patterns courants (boucles, fichiers, UserForms), error handling et debugging, Apps Script fundamentals, triggers et automatisation, custom functions, integration APIs, securite et migration entre environnements.

- **[Data Modeling & Dashboards](./references/data-modeling-dashboards.md)** — Architecture de modele de donnees (Input/Calculation/Output), star schema dans Excel (Power Pivot), DAX fundamentals (CALCULATE, SUMX, RELATED, time intelligence), tableaux croises dynamiques avances, dashboards interactifs (slicers, timelines, form controls), conditional formatting, sparklines, Google Sheets dashboards.

- **[Advanced Techniques](./references/advanced-techniques.md)** — Python in Excel (pandas, matplotlib, scikit-learn), Copilot in Excel, Google Sheets AI, performance optimization (modes de calcul, fonctions volatiles), gestion de gros volumes (1M+ lignes), collaboration (co-authoring, version control, protection), connexion Excel-Power BI, validation de donnees, templates reutilisables, formats de fichiers.
