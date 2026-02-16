# Data Modeling & Dashboards — Power Pivot, Data Models, Interactive Dashboards

## Introduction

**FR** — Ce guide de reference couvre la modelisation de donnees dans les tableurs et la construction de dashboards interactifs professionnels. Il detaille l'architecture de modele de donnees (Input/Calculation/Output), le star schema dans Excel via Power Pivot, les fondamentaux DAX (CALCULATE, SUMX, RELATED, time intelligence), les techniques avancees de tableaux croises dynamiques, les relations et mesures Power Pivot, les principes de design de dashboards, les elements interactifs (slicers, timelines, form controls), le conditional formatting pour la visualisation, les sparklines, et les techniques de dashboard dans Google Sheets. L'objectif est de transformer le tableur en outil de decision visuel, interactif et connecte aux donnees.

**EN** — This reference guide covers data modeling in spreadsheets and the construction of professional interactive dashboards. It details data model architecture (Input/Calculation/Output), star schema in Excel via Power Pivot, DAX fundamentals (CALCULATE, SUMX, RELATED, time intelligence), advanced pivot table techniques, Power Pivot relationships and measures, dashboard design principles, interactive elements (slicers, timelines, form controls), conditional formatting for visualization, sparklines, and Google Sheets dashboard techniques.

---

## 1. Spreadsheet Data Model Architecture

### Le modele Input / Calculation / Output

L'architecture en trois couches est le fondement de tout classeur professionnel. Elle separe les donnees brutes, la logique metier, et la presentation des resultats.

**Layer Input (Donnees) :**
- Contient les donnees brutes importees ou saisies
- Tables structurees (Ctrl+T) avec nommage explicite (`tbl_Ventes`, `tbl_Clients`, `tbl_Produits`)
- Regles de validation sur chaque colonne de saisie
- Convention de couleur : fond bleu clair pour les cellules editables
- Jamais de formule dans cette couche (sauf validation)
- Source unique : chaque donnee n'existe qu'ici

**Layer Calculation (Calculs) :**
- Contient toute la logique metier : formules, lookups, aggregations intermediaires
- Les feuilles de calcul sont protegees (l'utilisateur ne doit pas les modifier)
- Convention de couleur : fond blanc, police noire
- Les formules referencent les tables de la couche Input via des references structurees
- Decomposition en colonnes helper pour la lisibilite

**Layer Output (Restitution) :**
- Contient les dashboards, rapports, et exports
- Graphiques dynamiques, KPIs, tableaux croises dynamiques
- Convention de couleur : fond vert clair ou gris pour les resultats
- Protection complete : aucune modification possible par l'utilisateur
- Mise en page optimisee pour l'impression ou l'export PDF

**Layer Config (Parametres) :**
- Feuille dediee aux constantes, parametres, et listes de reference
- Taux de TVA, taux de change, seuils, categories
- Convention de couleur : fond jaune
- Chaque parametre est une plage nommee pour faciliter l'utilisation dans les formules

### Implementation pratique

```
Classeur: Budget_Annuel_2025.xlsx
├── ReadMe            (documentation, version, instructions)
├── Config            (parametres globaux, taux, seuils)
├── Input_Budget      (saisie du budget par departement)
├── Input_Reel        (import des donnees reelles via Power Query)
├── Calc_Ecarts       (calcul des ecarts budget vs reel)
├── Calc_Previsions   (formules de projection et tendances)
├── Output_Dashboard  (dashboard de synthese avec KPIs)
├── Output_Detail     (rapport detaille par departement)
└── Changelog         (historique des modifications)
```

### Relations entre tables

Meme sans Power Pivot, il est possible de creer un modele relationnel dans Excel :

```
tbl_Clients (1) ←→ (N) tbl_Commandes ←→ (N) tbl_Lignes_Commande → (1) tbl_Produits
     │                       │
     └── ClientID            └── CommandeID, ClientID
                                  LigneID, CommandeID, ProduitID
```

**Avec des formules :**
```
// Dans tbl_Commandes, recuperer le nom du client
=XLOOKUP([@ClientID], tbl_Clients[ClientID], tbl_Clients[Nom])

// Dans tbl_Lignes_Commande, recuperer la categorie du produit
=XLOOKUP([@ProduitID], tbl_Produits[ProduitID], tbl_Produits[Categorie])
```

**Avec Power Pivot :** Les relations sont definies graphiquement dans le Diagram View et exploitees via DAX (voir section suivante).

---

## 2. Star Schema in Excel — Power Pivot

### Qu'est-ce que Power Pivot ?

Power Pivot est un moteur d'analyse de donnees integre a Excel qui permet de :
- Importer des millions de lignes (compression en memoire extreme — 10:1 typiquement)
- Creer des relations entre tables (modele dimensionnel)
- Definir des mesures DAX (calculs dynamiques contextuels)
- Alimenter les tableaux croises dynamiques avec un modele de donnees riche

**Activation :** Fichier → Options → Complements → Complements COM → Microsoft Power Pivot for Excel

### Le Star Schema (schema en etoile)

Le star schema est le modele de donnees recommande pour l'analyse dans Power Pivot :

```
                    tbl_Dim_Temps
                         │
                    (Date → Date)
                         │
tbl_Dim_Clients ←── tbl_Fait_Ventes ──→ tbl_Dim_Produits
  (ClientID)        │  Date          │    (ProduitID)
                    │  ClientID      │
                    │  ProduitID     │
                    │  Montant       │
                    │  Quantite      │
                    │                │
                    └────────────────→ tbl_Dim_Regions
                                        (RegionID)
```

**Tables de faits :**
- Contiennent les evenements metier (ventes, commandes, transactions)
- Colonnes numeriques (montant, quantite, cout) = mesures
- Colonnes d'identification (IDs) = cles etrangeres vers les dimensions
- Granularite la plus fine possible (une ligne = un evenement)

**Tables de dimensions :**
- Contiennent les attributs descriptifs (nom du client, categorie produit, region)
- Hierarchies (Annee → Trimestre → Mois → Jour)
- Peu de lignes (centaines a quelques milliers) comparees aux faits (millions)
- Cle primaire unique

### Creer les relations dans Power Pivot

1. Ouvrir la fenetre Power Pivot (onglet Power Pivot → Manage)
2. Importer ou lier les tables
3. Basculer en Diagram View (icone en bas a droite)
4. Glisser-deposer les colonnes de cle entre les tables pour creer les relations
5. Verifier : la relation va de la cle primaire (1) de la dimension vers la cle etrangere (N) de la table de faits

### Bonnes pratiques du modele

- **Un modele = un star schema** : eviter les schemas flocon (snowflake) sauf necessite
- **Table de dates obligatoire** : creer une table de dates complete (chaque jour de la periode) pour le time intelligence DAX
- **Pas de relations many-to-many** : si necessaire, utiliser une table de pont (bridge table)
- **Nommer les colonnes de facon explicite** : les noms apparaissent dans les champs du tableau croise dynamique
- **Masquer les colonnes techniques** : masquer les IDs et les cles dans la vue utilisateur

---

## 3. DAX Fundamentals

### Qu'est-ce que DAX ?

DAX (Data Analysis Expressions) est le langage de formules de Power Pivot et Power BI. Il permet de creer des mesures calculees qui reagissent dynamiquement au contexte de filtrage (slicers, filtres de tableau croise dynamique, axes de graphiques).

### Mesures vs Colonnes calculees

| Aspect | Mesure (Measure) | Colonne calculee (Calculated Column) |
|---|---|---|
| **Calcul** | A la volee, selon le contexte de filtre | Une fois, lors du rafraichissement |
| **Stockage** | Pas stockee (formule seulement) | Stockee dans le modele (memoire) |
| **Usage** | Valeurs de synthese (KPIs, totaux, moyennes) | Attributs derives (categorisation, concatenation) |
| **Contexte** | Reagit aux slicers et filtres | Valeur fixe par ligne |
| **Recommandation** | Privilegier les mesures | Utiliser avec parcimonie |

### CALCULATE — La fonction la plus importante

CALCULATE modifie le contexte de filtre d'une expression. C'est LA fonction fondamentale de DAX.

```dax
// Syntaxe
CALCULATE(<expression>, <filtre1>, <filtre2>, ...)

// Total des ventes (sans filtre supplementaire)
Total Ventes := SUM(tbl_Fait_Ventes[Montant])

// Ventes de la region Nord uniquement
Ventes Nord := CALCULATE(SUM(tbl_Fait_Ventes[Montant]), tbl_Dim_Regions[Region] = "Nord")

// Ventes de l'annee precedente (time intelligence)
Ventes Annee Precedente := CALCULATE(SUM(tbl_Fait_Ventes[Montant]), SAMEPERIODLASTYEAR(tbl_Dim_Temps[Date]))

// Pourcentage du total (ALL supprime tous les filtres)
Part du Total := DIVIDE(SUM(tbl_Fait_Ventes[Montant]), CALCULATE(SUM(tbl_Fait_Ventes[Montant]), ALL(tbl_Fait_Ventes)))
```

### Fonctions d'iteration — SUMX, AVERAGEX, COUNTX

Les fonctions X iterent sur chaque ligne d'une table et executent une expression :

```dax
// Chiffre d'affaires = somme de (quantite * prix unitaire) pour chaque ligne
CA := SUMX(tbl_Fait_Ventes, tbl_Fait_Ventes[Quantite] * RELATED(tbl_Dim_Produits[Prix_Unitaire]))

// Prix moyen pondere par quantite
Prix Moyen Pondere := DIVIDE(
    SUMX(tbl_Fait_Ventes, tbl_Fait_Ventes[Quantite] * tbl_Fait_Ventes[Prix]),
    SUM(tbl_Fait_Ventes[Quantite])
)

// Nombre de clients ayant achete plus de 3 fois
Clients Fideles := COUNTROWS(
    FILTER(
        SUMMARIZE(tbl_Fait_Ventes, tbl_Dim_Clients[ClientID], "NbAchats", COUNTROWS(tbl_Fait_Ventes)),
        [NbAchats] > 3
    )
)
```

### RELATED — Navigation entre tables

RELATED navigue une relation pour recuperer un attribut d'une table liee :

```dax
// Dans une colonne calculee de tbl_Fait_Ventes, recuperer la categorie du produit
Categorie = RELATED(tbl_Dim_Produits[Categorie])

// Dans une mesure, utiliser RELATED dans un iterateur
CA par Categorie := SUMX(
    tbl_Fait_Ventes,
    tbl_Fait_Ventes[Montant] * IF(RELATED(tbl_Dim_Produits[Categorie]) = "Premium", 1, 0)
)
```

### Time Intelligence — Analyse temporelle

Les fonctions de time intelligence necessitent une table de dates complete (chaque jour de la periode, sans trou).

```dax
// Table de dates (a creer dans Power Pivot ou Power Query)
// Doit contenir : Date, Annee, Trimestre, Mois, NomMois, NumSemaine, JourSemaine

// Year-to-Date (cumul depuis le debut de l'annee)
YTD Ventes := TOTALYTD(SUM(tbl_Fait_Ventes[Montant]), tbl_Dim_Temps[Date])

// Month-to-Date
MTD Ventes := TOTALMTD(SUM(tbl_Fait_Ventes[Montant]), tbl_Dim_Temps[Date])

// Meme periode annee precedente
Ventes N-1 := CALCULATE(SUM(tbl_Fait_Ventes[Montant]), SAMEPERIODLASTYEAR(tbl_Dim_Temps[Date]))

// Croissance annuelle
Croissance % := DIVIDE([Total Ventes] - [Ventes N-1], [Ventes N-1], 0)

// Moyenne mobile 3 mois
Moyenne Mobile 3M := AVERAGEX(
    DATESINPERIOD(tbl_Dim_Temps[Date], MAX(tbl_Dim_Temps[Date]), -3, MONTH),
    CALCULATE(SUM(tbl_Fait_Ventes[Montant]))
)

// Cumul progressif (running total)
Running Total := CALCULATE(
    SUM(tbl_Fait_Ventes[Montant]),
    FILTER(ALL(tbl_Dim_Temps[Date]), tbl_Dim_Temps[Date] <= MAX(tbl_Dim_Temps[Date]))
)
```

### Patrons DAX avances

```dax
// Top N dynamique (ex: Top 5 produits)
Top 5 Produits := CALCULATE(
    SUM(tbl_Fait_Ventes[Montant]),
    TOPN(5, ALL(tbl_Dim_Produits[Nom_Produit]), CALCULATE(SUM(tbl_Fait_Ventes[Montant])), DESC)
)

// Classification ABC
Classification ABC :=
    VAR TotalCA = CALCULATE(SUM(tbl_Fait_Ventes[Montant]), ALL(tbl_Dim_Produits))
    VAR CAProduit = SUM(tbl_Fait_Ventes[Montant])
    VAR Pct = DIVIDE(CAProduit, TotalCA)
    RETURN
        SWITCH(TRUE(),
            Pct >= 0.1, "A",
            Pct >= 0.03, "B",
            "C"
        )

// Nombre de jours depuis la derniere vente (recency)
Jours Depuis Derniere Vente := DATEDIFF(
    MAX(tbl_Fait_Ventes[Date]),
    TODAY(),
    DAY
)
```

---

## 4. Pivot Tables — Advanced Techniques

### Configuration avancee

**Calculer des champs personnalises :**
- Onglet PivotTable Analyze → Fields, Items & Sets → Calculated Field
- Exemple : `=Montant/Quantite` pour le prix moyen

**Groupement de dates :**
- Clic droit sur une date dans le tableau croise → Group
- Options : Annees, Trimestres, Mois, Jours, Heures
- Permet de creer une hierarchie temporelle sans table de dates

**Affichage conditionnel :**
- Clic droit sur une valeur → Show Values As
- % of Grand Total, % of Parent Row, Running Total, Rank

### Techniques de filtrage avancees

```
Top 10 / Bottom 10 :
  PivotTable → Value Filters → Top 10
  Filtrer les N premiers/derniers par valeur

Filtres de valeur :
  Greater than, Between, Contains
  Ex: afficher uniquement les regions avec CA > 100 000

Filtres de date :
  This Quarter, Last Year, Between dates
  Filtrage temporel dynamique sans saisie manuelle
```

### Tableaux croises dynamiques multiples connectes

Creer plusieurs tableaux croises dynamiques a partir du meme modele de donnees et les connecter via des slicers partages :

1. Creer le premier TCD normalement
2. Creer le second TCD : Insert → PivotTable → Use this workbook's Data Model
3. Inserer un slicer : PivotTable Analyze → Insert Slicer
4. Connecter le slicer aux deux TCD : clic droit sur le slicer → Report Connections → cocher les deux TCD

### GetPivotData — Extraction programmable

```
// Extraire une valeur specifique d'un tableau croise dynamique
=GETPIVOTDATA("Montant", $A$3, "Region", "Nord", "Annee", 2025)

// Rendre la formule dynamique avec des references
=GETPIVOTDATA("Montant", $A$3, "Region", E1, "Annee", F1)
```

Astuce : Pour desactiver la generation automatique de GETPIVOTDATA (qui peut etre genante), aller dans PivotTable Analyze → Options → decocher "Generate GetPivotData".

---

## 5. Dashboard Design Principles in Excel

### Les 6 principes du dashboard efficace

**1. Hierarchie visuelle claire**
- Les KPIs les plus importants en haut et en grand
- Les details en dessous, progressivement plus petits
- L'oeil doit naturellement aller du plus important au moins important

**2. Maximum 7 elements visuels par ecran**
- Au-dela de 7 graphiques/tableaux, le dashboard devient illisible
- Regrouper logiquement (KPIs en haut, tendances au milieu, details en bas)
- Utiliser des onglets ou des sections si plus de contenu est necessaire

**3. Contraste et lisibilite**
- Fond blanc ou gris tres clair
- Texte noir ou gris fonce (jamais de texte en couleur vive)
- Les couleurs sont reservees aux donnees, pas a la decoration
- Police unique (Segoe UI, Calibri, ou Arial)

**4. Palette de couleurs limitee**
- 3 couleurs maximum pour les donnees (ex: bleu principal, gris secondaire, orange accent)
- Vert/rouge uniquement pour les indicateurs positif/negatif
- Jamais de couleurs 3D, de degrades, ou d'effets visuels superflus

**5. Interactivite utile**
- Slicers pour les filtres principaux (region, periode, categorie)
- Timelines pour la navigation temporelle
- Tous les elements doivent reagir aux memes filtres

**6. Optimisation pour l'impression/PDF**
- Tester la mise en page en mode apercu avant impression
- Definir la zone d'impression
- S'assurer que le dashboard tient sur une page (Landscape, Fit to 1 page wide)

### Layout type d'un dashboard Excel

```
┌─────────────────────────────────────────────────────┐
│  TITRE DU DASHBOARD              Date: [Slicer]     │
│  Sous-titre / Periode            Region: [Slicer]   │
├──────────┬──────────┬──────────┬────────────────────┤
│  KPI 1   │  KPI 2   │  KPI 3   │  KPI 4            │
│  CA Total│  Marge % │  Nb Cmd  │  Panier Moyen     │
│  125 K   │  32.5%   │  1 250   │  100 EUR          │
│  +12% ↑  │  -2.1% ↓ │  +8% ↑  │  +3% ↑           │
├──────────┴──────────┴──────────┼────────────────────┤
│                                │                     │
│  Graphique tendance CA         │  Repartition par    │
│  (courbe sur 12 mois)         │  categorie (donut)  │
│                                │                     │
├────────────────────────────────┼────────────────────┤
│                                │                     │
│  Top 10 produits (barre horiz) │  Performance par    │
│                                │  region (carte)     │
│                                │                     │
├────────────────────────────────┴────────────────────┤
│  Tableau detail : Top 20 transactions recentes      │
└─────────────────────────────────────────────────────┘
```

### Construction des KPI Cards

Creer des "cartes KPI" dans Excel sans graphique, uniquement avec du formatage :

1. Fusionner les cellules pour creer un bloc (exception a la regle anti-fusion : acceptable dans la couche Output pour la presentation)
2. Formule du KPI : `=SUMIFS(tbl_Ventes[Montant], ...)` en grand (taille 28, gras)
3. Formule de variation : `=[@KPI_actuel]/[@KPI_precedent]-1` en petit (taille 11)
4. Mise en forme conditionnelle : vert si positif, rouge si negatif
5. Bordure subtile et fond blanc

```
// Formule de variation avec fleche
=IF(B2>0, "↑ +" & TEXT(B2, "0.0%"), "↓ " & TEXT(B2, "0.0%"))
```

---

## 6. Interactive Elements

### Slicers (Segments)

Les slicers sont des filtres visuels cliquables connectes aux tableaux croises dynamiques et aux tables structurees.

**Creer un slicer :**
1. Selectionner le tableau croise dynamique
2. Insert → Slicer → Choisir les champs (Region, Categorie, Annee...)
3. Connecter a plusieurs TCD : clic droit → Report Connections

**Mise en forme des slicers :**
- Onglet Slicer → Slicer Styles → choisir un style epure
- Ajuster le nombre de colonnes (ex: 3 colonnes pour les regions)
- Taille et position : aligner avec les autres elements du dashboard

**Slicer sur table structuree (Excel 365) :**
- Selectionner une table structuree
- Insert → Slicer
- Le slicer filtre la table directement (pas besoin de TCD)

### Timelines (Chronologies)

Les timelines sont des slicers specialises pour les dates :

1. Le TCD doit contenir un champ de date
2. Insert → Timeline → Selectionner le champ date
3. Basculer entre Annees, Trimestres, Mois, Jours
4. Selectionner une plage de dates en glissant

### Form Controls (Controles de formulaire)

Les controles de formulaire permettent une interactivite sans VBA :

**Combo Box (liste deroulante) :**
1. Developer → Insert → Combo Box (Form Control)
2. Clic droit → Format Control
3. Input Range : la liste de valeurs
4. Cell Link : la cellule qui recoit la selection (numero d'index)
5. Utiliser INDEX pour convertir l'index en valeur : `=INDEX(liste_regions, cellule_link)`

**Scroll Bar (barre de defilement) :**
1. Developer → Insert → Scroll Bar (Form Control)
2. Format Control : Min, Max, Increment, Cell Link
3. La cellule liee contient la valeur du scroll bar
4. Utiliser cette valeur comme parametre dans les formules (ex: nombre de periodes a afficher)

**Spin Button (bouton +/-) :**
- Meme principe que le scroll bar, increment de 1
- Ideal pour selectionner un mois, une annee, un seuil

**Check Box (case a cocher) :**
- Cell Link contient TRUE/FALSE
- Utiliser dans les formules : `=IF(cellule_check, valeur_si_coche, valeur_si_decoche)`

---

## 7. Conditional Formatting for Data Visualization

### Barres de donnees (Data Bars)

Les barres de donnees transforment les cellules en mini-graphiques a barres :

1. Selectionner la plage de donnees
2. Home → Conditional Formatting → Data Bars
3. Options avancees : Solid Fill, couleur personnalisee, barre negative en rouge

**Bonnes pratiques :**
- Utiliser un fond transparent pour que les valeurs restent lisibles
- Definir le minimum et maximum manuellement pour comparer entre periodes
- Ne jamais utiliser de barres de donnees sur plus de 2-3 colonnes (surcharge visuelle)

### Jeux d'icones (Icon Sets)

| Jeu d'icones | Usage recommande |
|---|---|
| Fleches (3) | Tendance : hausse/stable/baisse |
| Feux tricolores (3) | Statut : bon/attention/critique |
| Drapeaux (3) | Priorite ou conformite |
| Etoiles (5) | Notation ou scoring |
| Barres (4) | Niveau de progression |

**Configuration avancee :**
- Conditional Formatting → Icon Sets → More Rules
- Basculer en "Show icon only" pour masquer les valeurs
- Definir des seuils en valeur absolue ou en percentile

### Echelles de couleurs (Color Scales)

- 2 couleurs : blanc → bleu (intensite proportionnelle a la valeur)
- 3 couleurs : rouge → jaune → vert (divergence autour d'une valeur centrale)
- Ideal pour les heat maps et les matrices de comparaison

**Patron : Heat Map dans Excel**

```
1. Creer un tableau croise dynamique (Lignes: Mois, Colonnes: Categorie, Valeurs: Montant)
2. Selectionner les valeurs
3. Conditional Formatting → Color Scales → Green-Yellow-Red
4. Resultat : une carte thermique qui montre visuellement les zones fortes et faibles
```

### Regles personnalisees

```
// Mettre en rouge les cellules avec ecart > 10%
Conditional Formatting → New Rule → Use a formula
Formule: =ABS(B2-C2)/C2 > 0.1
Format: fond rouge clair, texte rouge fonce

// Mettre en surbrillance la ligne entiere si le statut est "En retard"
Selectionner la plage entiere (ex: A2:F100)
Formule: =$E2="En retard"    ($ sur la colonne E, pas sur la ligne)
Format: fond orange clair

// Alternate row shading (zebra stripes)
Formule: =MOD(ROW(), 2) = 0
Format: fond gris tres clair
```

---

## 8. Sparklines — Mini-Graphiques en Cellule

### Types de sparklines

| Type | Usage | Exemple |
|---|---|---|
| **Line** | Tendance sur une periode | Evolution du CA mensuel |
| **Column** | Comparaison de valeurs discretes | Ventes par mois |
| **Win/Loss** | Resultat binaire (+/-) | Objectif atteint ou non par mois |

### Creation

```
// Dans la cellule G2, inserer un sparkline pour les donnees B2:F2
Insert → Sparklines → Line → Data Range: B2:F2, Location: G2

// Appliquer a toute la colonne
Selectionner G2 → Copier → Coller sur G3:G100
```

### Options de mise en forme

- **High Point / Low Point** : Mettre en evidence le point le plus haut/bas (vert/rouge)
- **First Point / Last Point** : Distinguer le debut et la fin
- **Negative Points** : Colorier les valeurs negatives en rouge
- **Axis** : Afficher l'axe zero pour les donnees avec positif et negatif
- **Min/Max scale** : Meme echelle pour toutes les sparklines (Same for All Sparklines)

### Bonnes pratiques sparklines

- Toujours utiliser la meme echelle pour les sparklines comparables (Custom Min/Max)
- Placer les sparklines dans la colonne immediatement apres les donnees
- Activer High Point et Low Point pour une lecture rapide
- Privilegier le type Line pour les tendances, Column pour les comparaisons

---

## 9. Google Sheets Dashboard Techniques

### QUERY — Le moteur de requete de Google Sheets

La fonction QUERY est l'equivalent d'un mini-SQL dans Google Sheets. Elle est la base de tout dashboard dans cet environnement :

```
// Synthese par region avec filtrage
=QUERY(Donnees!A1:F1000,
    "SELECT B, COUNT(A), SUM(E), AVG(E)
     WHERE D >= date '2025-01-01'
     GROUP BY B
     ORDER BY SUM(E) DESC
     LABEL COUNT(A) 'Nb Ventes', SUM(E) 'Total', AVG(E) 'Moyenne'", 1)

// Top 10 clients
=QUERY(Donnees!A1:F1000,
    "SELECT C, SUM(E)
     GROUP BY C
     ORDER BY SUM(E) DESC
     LIMIT 10
     LABEL SUM(E) 'Chiffre Affaires'", 1)

// Pivot dynamique (equivalent d'un TCD simple)
=QUERY(Donnees!A1:F1000,
    "SELECT B, SUM(E)
     GROUP BY B
     PIVOT D
     LABEL SUM(E) ''", 1)
```

### ARRAYFORMULA — Formules matricielles natives

Dans Google Sheets, ARRAYFORMULA etend une formule a toute une colonne automatiquement :

```
// Appliquer une formule a toute la colonne (au lieu de la recopier)
=ARRAYFORMULA(IF(A2:A<>"", B2:B * C2:C, ""))

// Combinaison QUERY + ARRAYFORMULA pour un KPI dynamique
=QUERY(
    ARRAYFORMULA(IF(Donnees!A2:A<>"",
        {Donnees!A2:A, Donnees!B2:B, Donnees!E2:E * Donnees!F2:F},
        {"","",""})),
    "SELECT Col1, SUM(Col3) GROUP BY Col1", 0)
```

### Types de graphiques recommandes dans Google Sheets

| Type | Quand l'utiliser | Donnees |
|---|---|---|
| **Scorecard** | KPI unique avec variation | 1 valeur + comparaison |
| **Line chart** | Tendance temporelle | Serie temporelle |
| **Column chart** | Comparaison entre categories | Categories + valeurs |
| **Combo chart** | Tendance + comparaison | Barres + ligne |
| **Donut chart** | Repartition (< 6 categories) | Categories + pourcentages |
| **Treemap** | Hierarchie et proportions | Categories imbriquees |
| **Geo chart** | Donnees geographiques | Pays/regions + valeurs |

### Slicers dans Google Sheets

Google Sheets supporte les slicers natifs (depuis 2023) :

1. Selectionner un graphique ou une plage
2. Data → Add a slicer
3. Choisir la colonne de filtrage
4. Le slicer filtre tous les graphiques et tableaux de la feuille

### Dashboard template Google Sheets

```
Structure recommandee :
├── Feuille "Donnees"        (donnees brutes, importees via IMPORTRANGE ou API)
├── Feuille "Calculs"        (QUERY, ARRAYFORMULA, aggregations)
├── Feuille "Dashboard"      (graphiques, KPIs, slicers — feuille protegee)
└── Feuille "Config"         (parametres, listes de validation)
```

**Techniques specifiques Google Sheets :**
- Utiliser `SPARKLINE()` comme fonction (pas comme objet graphique) : `=SPARKLINE(B2:M2, {"charttype","column";"color","#4285f4"})`
- Utiliser `IMAGE()` pour afficher des icones ou logos dans les cellules
- Utiliser Named Ranges pour rendre les QUERY lisibles
- Combiner `IMPORTRANGE` avec `QUERY` pour un dashboard multi-sources

---

## 10. Advanced Dashboard Patterns

### Pattern : Dashboard avec periode de reference dynamique

```
// Cellule de parametre : B1 = "2025-Q1" (selectionne par slicer ou dropdown)

// Extraire annee et trimestre
Annee = LEFT(B1, 4) → 2025
Trimestre = RIGHT(B1, 2) → Q1

// Dates de debut et fin
Date_Debut = DATE(Annee, (Trimestre_Num - 1) * 3 + 1, 1)
Date_Fin = EOMONTH(Date_Debut, 2)

// KPI filtre dynamiquement
CA_Periode = SUMIFS(tbl_Ventes[Montant],
    tbl_Ventes[Date], ">=" & Date_Debut,
    tbl_Ventes[Date], "<=" & Date_Fin)

// Comparaison N-1
CA_N_1 = SUMIFS(tbl_Ventes[Montant],
    tbl_Ventes[Date], ">=" & DATE(Annee-1, MONTH(Date_Debut), 1),
    tbl_Ventes[Date], "<=" & EOMONTH(DATE(Annee-1, MONTH(Date_Debut), 1), 2))

// Variation
Variation = (CA_Periode - CA_N_1) / CA_N_1
```

### Pattern : Graphique dynamique avec OFFSET ou INDEX

Creer un graphique dont la source change selon un parametre (ex: afficher les N derniers mois) :

```
// Plage nommee dynamique pour le graphique
Nom: rng_Chart_Data
Formule: =INDEX(tbl_Ventes[Montant], COUNTA(tbl_Ventes[Montant]) - param_Nb_Mois + 1):INDEX(tbl_Ventes[Montant], COUNTA(tbl_Ventes[Montant]))

// Le graphique source cette plage nommee
// Changer param_Nb_Mois (via scroll bar) met a jour le graphique
```

### Pattern : Alerting visuel automatique

```
// Conditional formatting sur les KPI cards
// Si CA < objectif * 0.9 → fond rouge (alerte)
// Si CA entre objectif * 0.9 et objectif → fond orange (attention)
// Si CA >= objectif → fond vert (OK)

=IF(B2 < C2 * 0.9, "ALERTE",
    IF(B2 < C2, "ATTENTION", "OK"))

// Format conditionnel correspondant :
// "ALERTE" → fond #f8d7da, texte #721c24
// "ATTENTION" → fond #fff3cd, texte #856404
// "OK" → fond #d4edda, texte #155724
```

### Pattern : Mini-dashboard dans une cellule (Google Sheets SPARKLINE)

```
// Sparkline avec options avancees
=SPARKLINE(B2:M2, {
    "charttype", "column";
    "color", "#4285f4";
    "negcolor", "#ea4335";
    "max", MAX(B2:M2) * 1.1;
    "min", 0
})

// Barre de progression
=SPARKLINE({B2, 1-B2}, {
    "charttype", "bar";
    "color1", IF(B2 >= 0.8, "#34a853", IF(B2 >= 0.5, "#fbbc05", "#ea4335"));
    "color2", "#e0e0e0"
})

// Bullet chart (objectif vs reel)
=SPARKLINE({Reel, Objectif - Reel}, {
    "charttype", "bar";
    "color1", "#4285f4";
    "color2", "#e8eaed"
})
```
