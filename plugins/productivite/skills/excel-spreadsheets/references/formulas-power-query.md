# Formulas Avancees & Power Query — XLOOKUP, Dynamic Arrays, LAMBDA, Power Query ETL

## Introduction

**FR** — Ce guide de reference couvre les formules avancees d'Excel et Google Sheets ainsi que Power Query. Il detaille les dynamic arrays (FILTER, SORT, UNIQUE, SEQUENCE, SORTBY), les fonctions de recherche modernes (XLOOKUP, XMATCH), les fonctions LAMBDA et leur ecosysteme (MAP, REDUCE, SCAN, MAKEARRAY), la fonction LET pour la lisibilite, et Power Query comme outil ETL integre au tableur. Chaque section inclut des patrons d'implementation, des exemples concrets, et des recommandations de performance. L'objectif est de transformer l'approche "une formule par cellule recopiee sur 10 000 lignes" en une approche "une formule dynamique qui s'adapte automatiquement".

**EN** — This reference guide covers advanced Excel and Google Sheets formulas and Power Query. It details dynamic arrays (FILTER, SORT, UNIQUE, SEQUENCE, SORTBY), modern lookup functions (XLOOKUP, XMATCH), LAMBDA functions and their ecosystem (MAP, REDUCE, SCAN, MAKEARRAY), the LET function for readability, and Power Query as a built-in ETL tool. Each section includes implementation patterns, concrete examples, and performance recommendations.

---

## 1. Modern Lookup Functions — XLOOKUP & XMATCH

### XLOOKUP — The Universal Lookup

XLOOKUP remplace VLOOKUP, HLOOKUP, INDEX/MATCH, et LOOKUP en une seule fonction unifiee. Disponible dans Excel 365, Excel 2021+, et Google Sheets.

**Syntaxe :**
```
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])
```

**Parametres cles :**
- `if_not_found` : Valeur retournee si aucune correspondance (remplace IFERROR autour de VLOOKUP)
- `match_mode` : 0 = exact (defaut), -1 = exact ou inferieur, 1 = exact ou superieur, 2 = wildcard
- `search_mode` : 1 = premier au dernier (defaut), -1 = dernier au premier, 2 = recherche binaire ascendante, -2 = recherche binaire descendante

**Patrons courants :**

```
// Recherche basique avec gestion d'erreur integree
=XLOOKUP(A2, tbl_Produits[Code], tbl_Produits[Prix], "Non trouve")

// Recherche sur plusieurs colonnes (retour d'une plage)
=XLOOKUP(A2, tbl_Employes[ID], tbl_Employes[Nom]:tbl_Employes[Service])

// Recherche inversee (de droite a gauche — impossible avec VLOOKUP)
=XLOOKUP(A2, tbl_Ventes[Montant], tbl_Ventes[Client])

// Derniere occurrence (search_mode = -1)
=XLOOKUP(A2, tbl_Transactions[Client], tbl_Transactions[Date], , 0, -1)

// Recherche approximative (ex: tranches de prix)
=XLOOKUP(B2, tbl_Tranches[Seuil], tbl_Tranches[Taux], , -1)
```

**XLOOKUP imbrique pour recherche bidimensionnelle :**
```
=XLOOKUP(B1, B3:F3, XLOOKUP(A4, A4:A10, B4:F10))
```
Ce patron remplace l'ancienne combinaison INDEX/MATCH/MATCH pour les recherches a deux dimensions.

### XMATCH — Position Lookup

XMATCH retourne la position d'une valeur dans une plage. Il remplace MATCH avec des capacites supplementaires (wildcard, recherche binaire, derniere occurrence).

```
=XMATCH(lookup_value, lookup_array, [match_mode], [search_mode])
```

**Usage typique :** XMATCH est rarement utilise seul. Il sert principalement dans des formules combinees (INDEX+XMATCH) ou pour des validations de presence.

```
// Verifier si une valeur existe dans une liste
=IF(ISNA(XMATCH(A2, tbl_Ref[Code])), "Absent", "Present")

// Position de la derniere occurrence
=XMATCH(A2, tbl_Data[Category], 0, -1)
```

---

## 2. Dynamic Arrays — The Paradigm Shift

Les dynamic arrays sont le changement le plus fondamental dans Excel depuis l'introduction des tableaux croises dynamiques. Une seule formule dans une seule cellule produit un resultat qui "deborde" (spill) sur plusieurs cellules automatiquement.

### FILTER — Filtrage dynamique

```
=FILTER(array, include, [if_empty])
```

**Patrons courants :**

```
// Filtrer les ventes de la region Nord
=FILTER(tbl_Ventes, tbl_Ventes[Region]="Nord", "Aucune vente")

// Filtre multi-criteres (ET logique — multiplier les conditions)
=FILTER(tbl_Ventes, (tbl_Ventes[Region]="Nord") * (tbl_Ventes[Montant]>1000))

// Filtre multi-criteres (OU logique — additionner les conditions)
=FILTER(tbl_Ventes, (tbl_Ventes[Region]="Nord") + (tbl_Ventes[Region]="Sud"))

// Retourner uniquement certaines colonnes
=FILTER(CHOOSECOLS(tbl_Ventes, 1, 3, 5), tbl_Ventes[Region]="Nord")
```

### SORT & SORTBY — Tri dynamique

```
=SORT(array, [sort_index], [sort_order], [by_col])
=SORTBY(array, by_array1, [sort_order1], [by_array2], [sort_order2], ...)
```

**Patrons courants :**

```
// Trier les ventes par montant decroissant
=SORT(tbl_Ventes, 4, -1)

// Tri multi-criteres avec SORTBY
=SORTBY(tbl_Ventes, tbl_Ventes[Region], 1, tbl_Ventes[Montant], -1)

// Combiner FILTER + SORT : Top ventes Nord triees par montant
=SORT(FILTER(tbl_Ventes, tbl_Ventes[Region]="Nord"), 4, -1)
```

### UNIQUE — Deduplication dynamique

```
=UNIQUE(array, [by_col], [exactly_once])
```

**Patrons courants :**

```
// Liste des regions distinctes
=UNIQUE(tbl_Ventes[Region])

// Valeurs apparaissant exactement une fois (exactly_once = TRUE)
=UNIQUE(tbl_Ventes[Client], , TRUE)

// Liste triee des regions distinctes
=SORT(UNIQUE(tbl_Ventes[Region]))

// Combiner pour creer un resume dynamique
=LET(
    regions, SORT(UNIQUE(tbl_Ventes[Region])),
    totaux, SUMIFS(tbl_Ventes[Montant], tbl_Ventes[Region], regions),
    HSTACK(regions, totaux)
)
```

### SEQUENCE — Generation de series

```
=SEQUENCE(rows, [columns], [start], [step])
```

**Patrons courants :**

```
// Generer les numeros 1 a 100
=SEQUENCE(100)

// Generer une grille 5x5 commencant a 0
=SEQUENCE(5, 5, 0, 1)

// Generer des dates (premier de chaque mois de 2025)
=DATE(2025, SEQUENCE(12), 1)

// Matrice d'heures pour un planning
=TEXT(TIME(SEQUENCE(24, 1, 8), 0, 0), "HH:MM")
```

### RANDARRAY — Donnees aleatoires structurees

```
=RANDARRAY([rows], [columns], [min], [max], [whole_number])
```

Utile pour la generation de donnees de test et les simulations Monte Carlo dans le tableur.

### Combinaison de Dynamic Arrays — Patrons avances

Le veritable pouvoir des dynamic arrays emerge quand on les combine :

```
// Top 10 clients par chiffre d'affaires
=LET(
    clients, UNIQUE(tbl_Ventes[Client]),
    ca, SUMIFS(tbl_Ventes[Montant], tbl_Ventes[Client], clients),
    combined, HSTACK(clients, ca),
    sorted, SORT(combined, 2, -1),
    top10, TAKE(sorted, 10),
    top10
)

// Tableau de synthese dynamique complet
=LET(
    regions, SORT(UNIQUE(tbl_Ventes[Region])),
    nb, COUNTIFS(tbl_Ventes[Region], regions),
    total, SUMIFS(tbl_Ventes[Montant], tbl_Ventes[Region], regions),
    moyenne, total / nb,
    HSTACK(regions, nb, total, moyenne)
)
```

### Spill Reference (#)

L'operateur `#` reference l'ensemble du resultat deborde d'une formule dynamique :

```
// Si A1 contient =UNIQUE(tbl_Ventes[Region])
// Alors A1# reference toutes les valeurs retournees
=COUNTA(A1#)  // Nombre de regions distinctes
=SORT(A1#)    // Trier le resultat
```

---

## 3. LAMBDA & Custom Functions

### LAMBDA — Fonctions personnalisees sans VBA

LAMBDA permet de creer des fonctions reutilisables directement dans le Name Manager (Gestionnaire de noms). C'est une revolution pour les power users : les formules complexes deviennent des fonctions nommees, testables et partagees.

**Syntaxe :**
```
=LAMBDA([parameter1], [parameter2], ..., calculation)
```

**Creation d'une fonction nommee :**
1. Ouvrir le Gestionnaire de noms (Ctrl+F3)
2. Creer un nouveau nom (ex: `TVA_TTC`)
3. Dans "Refers to" : `=LAMBDA(montant_ht, taux, montant_ht * (1 + taux))`
4. Utilisation : `=TVA_TTC(B2, C2)`

**Exemples de LAMBDA utiles :**

```
// Conversion temperature
CELSIUS_TO_FAHRENHEIT = LAMBDA(c, c * 9/5 + 32)

// Calcul de marge
MARGE = LAMBDA(prix_vente, cout, (prix_vente - cout) / prix_vente)

// Arrondi bancaire (au 0.05 le plus proche)
ARRONDI_BANCAIRE = LAMBDA(montant, MROUND(montant, 0.05))

// Formule de scoring personnalisee
SCORE_CLIENT = LAMBDA(ca, anciennete, nb_commandes,
    LET(
        score_ca, IF(ca > 100000, 3, IF(ca > 50000, 2, 1)),
        score_anc, IF(anciennete > 5, 3, IF(anciennete > 2, 2, 1)),
        score_cmd, IF(nb_commandes > 50, 3, IF(nb_commandes > 20, 2, 1)),
        (score_ca * 0.5) + (score_anc * 0.3) + (score_cmd * 0.2)
    )
)
```

### MAP — Appliquer une fonction a chaque element

```
=MAP(array, LAMBDA(element, transformation))
```

```
// Appliquer un taux de TVA a chaque montant
=MAP(tbl_Ventes[Montant_HT], LAMBDA(m, m * 1.20))

// Categoriser chaque montant
=MAP(tbl_Ventes[Montant], LAMBDA(m, IF(m > 10000, "Gros", IF(m > 1000, "Moyen", "Petit"))))

// Extraire le domaine de chaque email
=MAP(tbl_Contacts[Email], LAMBDA(e, MID(e, FIND("@", e) + 1, 100)))
```

### REDUCE — Aggregation personnalisee

```
=REDUCE(initial_value, array, LAMBDA(accumulator, element, operation))
```

```
// Produit de tous les elements (equivalent de PRODUCT mais personnalisable)
=REDUCE(1, A1:A10, LAMBDA(acc, val, acc * val))

// Concatenation avec separateur
=REDUCE("", tbl_Data[Nom], LAMBDA(acc, val, acc & IF(acc="", "", ", ") & val))

// Somme conditionnelle personnalisee (elements > 100 uniquement)
=REDUCE(0, A1:A20, LAMBDA(acc, val, acc + IF(val > 100, val, 0)))
```

### SCAN — REDUCE avec historique

SCAN fonctionne comme REDUCE mais retourne toutes les valeurs intermediaires (pas seulement le resultat final). Ideal pour les cumuls.

```
// Cumul progressif (running total)
=SCAN(0, tbl_Ventes[Montant], LAMBDA(acc, val, acc + val))

// Maximum progressif (running max)
=SCAN(0, tbl_Data[Valeur], LAMBDA(acc, val, MAX(acc, val)))
```

### MAKEARRAY — Generation de matrices

```
=MAKEARRAY(rows, cols, LAMBDA(row, col, calculation))
```

```
// Table de multiplication
=MAKEARRAY(10, 10, LAMBDA(r, c, r * c))

// Matrice d'identite
=MAKEARRAY(5, 5, LAMBDA(r, c, IF(r = c, 1, 0)))

// Planning horaire avec etiquettes
=MAKEARRAY(24, 7, LAMBDA(h, j,
    IF(AND(h >= 9, h <= 17), "Ouvre", "Ferme")
))
```

### BYCOL & BYROW — Aggregation par dimension

```
// Somme par colonne
=BYCOL(B2:F10, LAMBDA(col, SUM(col)))

// Maximum par ligne
=BYROW(B2:F10, LAMBDA(row, MAX(row)))

// Coefficient de variation par colonne
=BYCOL(B2:F100, LAMBDA(col, STDEV(col) / AVERAGE(col)))
```

---

## 4. LET — Readable Formulas

### Syntaxe et principe

LET permet de definir des variables intermediaires dans une formule, rendant les formules complexes lisibles et performantes (chaque variable n'est calculee qu'une fois).

```
=LET(
    name1, value1,
    name2, value2,
    ...,
    calculation
)
```

### Patrons d'utilisation

```
// Calcul de remise progressive (sans LET : illisible)
// Avec LET : clair et maintenable
=LET(
    montant, B2,
    seuil1, 1000,
    seuil2, 5000,
    seuil3, 10000,
    taux1, 0.05,
    taux2, 0.10,
    taux3, 0.15,
    remise, IF(montant >= seuil3, taux3, IF(montant >= seuil2, taux2, IF(montant >= seuil1, taux1, 0))),
    montant * (1 - remise)
)

// Validation complexe avec messages
=LET(
    val, A2,
    is_num, ISNUMBER(val),
    is_positive, val > 0,
    is_in_range, AND(val >= 1, val <= 100),
    IF(NOT(is_num), "Erreur: pas un nombre",
        IF(NOT(is_positive), "Erreur: valeur negative",
            IF(NOT(is_in_range), "Erreur: hors plage 1-100",
                "OK")))
)

// Performance : eviter les calculs repetes
=LET(
    filtered, FILTER(tbl_Ventes[Montant], tbl_Ventes[Region] = "Nord"),
    total, SUM(filtered),
    count, COUNTA(filtered),
    avg, total / count,
    median, MEDIAN(filtered),
    HSTACK(total, count, avg, median)
)
```

### Bonnes pratiques LET

- Nommer les variables de facon explicite (pas `x`, `y`, mais `montant_ht`, `taux_remise`)
- Decomposer les calculs complexes en etapes logiques (validation, calcul intermediaire, resultat)
- Utiliser LET pour eviter de recalculer la meme sous-expression plusieurs fois (performance)
- Combiner LET avec LAMBDA pour creer des fonctions nommees lisibles

---

## 5. Power Query Fundamentals

### Qu'est-ce que Power Query ?

Power Query est un moteur ETL integre a Excel et Power BI. Il permet de se connecter a des centaines de sources de donnees, de transformer les donnees via une interface graphique ou le langage M, et de charger les resultats dans des tables Excel ou un modele de donnees. Chaque transformation est enregistree comme une etape reproductible et rafraichissable.

**Avantages cles :**
- Les transformations sont enregistrees et rejouables (pas de copier-coller)
- Le rafraichissement est automatique (planifie ou a la demande)
- Interface graphique + langage M pour les operations complexes
- Gestion native des erreurs, des types, et des valeurs manquantes
- Fusion (merge) et ajout (append) de requetes multiples

### Sources de donnees supportees

| Source | Exemples |
|---|---|
| **Fichiers** | Excel, CSV, JSON, XML, PDF, texte, Parquet |
| **Bases de donnees** | SQL Server, PostgreSQL, MySQL, Oracle, Access |
| **Cloud** | SharePoint, OneDrive, Azure, Dataverse, Salesforce |
| **Web** | Pages HTML, APIs REST, OData |
| **Dossiers** | Consolidation automatique de tous les fichiers d'un dossier |
| **Autres** | Active Directory, Exchange, SAP, ODBC/OLEDB |

### Langage M — Fondamentaux

Le langage M (Power Query Formula Language) est un langage fonctionnel qui sous-tend toutes les transformations Power Query. Chaque requete est une expression M.

**Structure d'une requete M :**

```m
let
    // Etape 1 : Connexion a la source
    Source = Excel.Workbook(File.Contents("C:\Data\Ventes.xlsx"), null, true),

    // Etape 2 : Navigation vers la table
    Ventes_Table = Source{[Item="Ventes",Kind="Table"]}[Data],

    // Etape 3 : Typage des colonnes
    TypedColumns = Table.TransformColumnTypes(Ventes_Table, {
        {"Date", type date},
        {"Montant", type number},
        {"Region", type text}
    }),

    // Etape 4 : Filtrage
    FilteredRows = Table.SelectRows(TypedColumns, each [Montant] > 0),

    // Etape 5 : Ajout d'une colonne calculee
    AddedColumn = Table.AddColumn(FilteredRows, "Annee", each Date.Year([Date]), Int64.Type),

    // Etape 6 : Groupement
    Grouped = Table.Group(AddedColumn, {"Region", "Annee"}, {
        {"Total", each List.Sum([Montant]), type number},
        {"Nombre", each Table.RowCount(_), Int64.Type}
    })
in
    Grouped
```

**Fonctions M courantes :**

| Fonction | Usage |
|---|---|
| `Table.SelectRows` | Filtrer des lignes selon une condition |
| `Table.AddColumn` | Ajouter une colonne calculee |
| `Table.TransformColumnTypes` | Definir les types de donnees |
| `Table.Group` | Grouper et agreger |
| `Table.NestedJoin` | Jointure entre tables (merge) |
| `Table.Combine` | Union de tables (append) |
| `Table.Pivot` | Pivoter des lignes en colonnes |
| `Table.Unpivot` | Depivoter des colonnes en lignes |
| `Table.ReplaceValue` | Remplacer des valeurs |
| `Table.RemoveColumns` | Supprimer des colonnes |
| `Text.Trim`, `Text.Clean` | Nettoyer du texte |
| `Date.Year`, `Date.Month` | Extraire des composants de date |

---

## 6. Power Query ETL Patterns

### Pattern 1 — Consolidation de fichiers multiples

Consolider automatiquement tous les fichiers d'un dossier (ex: 12 fichiers mensuels CSV) :

```m
let
    // Pointer vers le dossier
    Source = Folder.Files("C:\Data\Ventes_Mensuelles"),

    // Filtrer les fichiers CSV uniquement
    FilteredFiles = Table.SelectRows(Source, each [Extension] = ".csv"),

    // Extraire le contenu de chaque fichier
    AddContent = Table.AddColumn(FilteredFiles, "Tables", each
        Csv.Document([Content], [Delimiter=";", Encoding=65001, QuoteStyle=QuoteStyle.None])
    ),

    // Combiner toutes les tables
    Combined = Table.Combine(AddContent[Tables]),

    // Ajouter la source (nom du fichier)
    AddSource = Table.AddColumn(Combined, "Fichier_Source", each [Name], type text),

    // Typer les colonnes
    Typed = Table.TransformColumnTypes(AddSource, {
        {"Date", type date},
        {"Montant", type number}
    })
in
    Typed
```

### Pattern 2 — Merge (jointure) de tables

```m
let
    // Charger la table des ventes
    Ventes = Excel.CurrentWorkbook(){[Name="tbl_Ventes"]}[Content],

    // Charger la table des produits
    Produits = Excel.CurrentWorkbook(){[Name="tbl_Produits"]}[Content],

    // Jointure gauche sur le code produit
    Merged = Table.NestedJoin(Ventes, {"Code_Produit"}, Produits, {"Code"}, "Produit_Detail", JoinKind.LeftOuter),

    // Expandre les colonnes necessaires
    Expanded = Table.ExpandTableColumn(Merged, "Produit_Detail", {"Categorie", "Prix_Unitaire"})
in
    Expanded
```

### Pattern 3 — Depivotage (Unpivot)

Transformer des donnees en colonnes (format "large") en donnees en lignes (format "long") — essentiel pour l'analyse :

```m
let
    Source = Excel.CurrentWorkbook(){[Name="Budget"]}[Content],

    // Colonnes de mois (Jan, Fev, Mar...) -> lignes
    Unpivoted = Table.UnpivotOtherColumns(Source, {"Departement", "Poste"}, "Mois", "Montant"),

    // Typer
    Typed = Table.TransformColumnTypes(Unpivoted, {{"Montant", type number}})
in
    Typed
```

### Pattern 4 — Parametres dynamiques

Utiliser des parametres pour rendre les requetes flexibles :

```m
let
    // Lire le parametre depuis une cellule Excel nommee
    Annee_Filtre = Excel.CurrentWorkbook(){[Name="param_Annee"]}[Content]{0}[Column1],

    Source = Sql.Database("serveur", "base_ventes"),
    Ventes = Source{[Schema="dbo", Item="Ventes"]}[Data],

    // Filtrer selon le parametre
    Filtered = Table.SelectRows(Ventes, each Date.Year([Date_Vente]) = Annee_Filtre)
in
    Filtered
```

### Pattern 5 — Custom Functions en M

Creer des fonctions reutilisables dans Power Query :

```m
// Fonction de nettoyage de texte (a creer comme requete separee nommee "fn_CleanText")
(input as text) as text =>
let
    trimmed = Text.Trim(input),
    cleaned = Text.Clean(trimmed),
    proper = Text.Proper(cleaned),
    result = Text.Replace(proper, "  ", " ")
in
    result

// Utilisation dans une autre requete :
// Table.TransformColumns(Source, {{"Nom", fn_CleanText, type text}})
```

---

## 7. Advanced Power Query Techniques

### Error Handling in Power Query

```m
// Remplacer les erreurs par des valeurs par defaut
let
    Source = ...,
    ReplaceErrors = Table.ReplaceErrorValues(Source, {
        {"Montant", 0},
        {"Date", null},
        {"Code", "INCONNU"}
    }),

    // Ou capturer les erreurs dans une colonne separee
    AddErrorFlag = Table.AddColumn(Source, "Has_Error", each
        try [Montant] otherwise "ERREUR", type text
    )
in
    ReplaceErrors
```

### Incremental Refresh Pattern

Pour les grandes sources de donnees, ne charger que les donnees nouvelles ou modifiees :

```m
let
    // Parametre : derniere date chargee
    LastLoad = Excel.CurrentWorkbook(){[Name="param_LastLoad"]}[Content]{0}[Column1],

    Source = Sql.Database("serveur", "base"),
    Ventes = Source{[Schema="dbo", Item="Ventes"]}[Data],

    // Ne charger que les nouvelles donnees
    Incremental = Table.SelectRows(Ventes, each [Date_Modification] > LastLoad)
in
    Incremental
```

### Performance Optimization

**Regles de performance Power Query :**

1. **Filtrer le plus tot possible** — Appliquer les filtres avant les transformations lourdes. Les filtres sont "pushes" vers la source pour les bases de donnees (query folding)
2. **Selectionner uniquement les colonnes necessaires** — `Table.SelectColumns` en debut de requete reduit le volume de donnees traite
3. **Verifier le query folding** — Clic droit sur la derniere etape "foldable" → "View Native Query". Si la requete native est disponible, les transformations sont executees cote serveur
4. **Eviter les colonnes ajoutees avant le filtrage** — Les colonnes ajoutees cassent le query folding dans certains cas
5. **Utiliser `Table.Buffer`** — Pour les tables utilisees dans plusieurs jointures, la mise en cache evite les recalculs
6. **Desactiver le chargement des requetes intermediaires** — Les requetes helper doivent etre en "Connection Only" (ne pas charger vers une feuille)

---

## 8. Formula Performance Optimization

### Fonctions volatiles a eviter

Les fonctions volatiles se recalculent a chaque modification du classeur, meme si leurs arguments n'ont pas change :

| Volatile (eviter) | Alternative non-volatile |
|---|---|
| `INDIRECT` | `INDEX` avec des plages nommees |
| `OFFSET` | `INDEX` pour les references dynamiques |
| `TODAY()` | Cellule de parametre avec la date, rafraichie par macro |
| `NOW()` | Idem |
| `RAND()` / `RANDBETWEEN()` | `RANDARRAY` (semi-volatile, recalcul controle) |
| `INFO` | Eviter si possible |

### Strategies de performance pour les formules

1. **Utiliser des tables structurees** — Les references de table (`tbl[Col]`) sont optimisees par le moteur de calcul d'Excel
2. **Privilegier XLOOKUP a VLOOKUP** — XLOOKUP supporte la recherche binaire (parametre search_mode) pour les grandes plages triees
3. **Remplacer les SUMPRODUCT complexes par SUMIFS** — SUMIFS est nativement optimise et plus rapide que SUMPRODUCT pour les conditions multiples
4. **Eviter les formules matricielles legacy (Ctrl+Shift+Enter)** — Les remplacer par des dynamic arrays natifs
5. **Limiter le nombre de formules inter-feuilles** — Les references entre feuilles sont plus lentes que les references intra-feuille. Consolider les donnees avec Power Query plutot qu'avec des formules de liaison
6. **Utiliser le mode de calcul Manuel** — Pour les classeurs lourds (> 100 000 formules), passer en calcul manuel et utiliser F9 pour recalculer a la demande
7. **Profiler avec le Evaluate Formula** — Utiliser Formules → Evaluer la formule pour identifier les etapes lentes d'une formule complexe

### Benchmark de performance

| Technique | 10K lignes | 100K lignes | 1M lignes |
|---|---|---|---|
| VLOOKUP | 0.2s | 2s | 20s+ |
| INDEX/MATCH | 0.15s | 1.5s | 15s |
| XLOOKUP | 0.1s | 0.8s | 8s |
| XLOOKUP (binary) | 0.05s | 0.1s | 0.5s |
| Power Query lookup | 0.5s (chargement) | 1s | 3s |

Note : les temps sont indicatifs et dependent du materiel. L'avantage de Power Query est que le lookup est fait une seule fois au chargement, pas a chaque recalcul.

---

## 9. Google Sheets Specifics

### Fonctions exclusives a Google Sheets

| Fonction | Usage |
|---|---|
| `QUERY` | Mini-SQL dans le tableur (GROUP BY, WHERE, PIVOT, ORDER BY) |
| `IMPORTRANGE` | Importer des donnees d'un autre classeur Google Sheets |
| `IMPORTDATA` | Importer un CSV depuis une URL |
| `IMPORTHTML` | Importer des tableaux ou listes depuis une page web |
| `IMPORTXML` | Importer des donnees XML avec XPath |
| `GOOGLEFINANCE` | Donnees financieres en temps reel |
| `IMAGE` | Afficher une image dans une cellule |
| `SPARKLINE` | Mini-graphique dans une cellule |

### QUERY — Le SQL de Google Sheets

```
=QUERY(data, query, [headers])
```

```
// Somme par region
=QUERY(A1:D100, "SELECT B, SUM(D) WHERE C > 1000 GROUP BY B ORDER BY SUM(D) DESC LABEL SUM(D) 'Total'")

// Filtrage avec condition texte
=QUERY(tbl_Ventes, "SELECT * WHERE B CONTAINS 'Paris' AND D > 5000")

// Pivot dynamique
=QUERY(A1:D100, "SELECT A, SUM(D) PIVOT B")

// Top N
=QUERY(A1:D100, "SELECT B, SUM(D) GROUP BY B ORDER BY SUM(D) DESC LIMIT 10")
```

### Differences cles avec Excel

| Aspect | Excel 365 | Google Sheets |
|---|---|---|
| **Dynamic arrays** | FILTER, SORT, UNIQUE natifs | FILTER, SORT, UNIQUE disponibles |
| **LAMBDA** | Disponible | Disponible (depuis 2022) |
| **XLOOKUP** | Natif | Disponible (depuis 2023) |
| **ETL** | Power Query (complet) | Connected Sheets / BigQuery (limite) |
| **Macros** | VBA (puissant, local) | Apps Script (cloud, APIs Google) |
| **Pivot** | Tableau croise dynamique avance + Power Pivot | Pivot basique, QUERY pour l'avance |
| **Performance** | Excellente (local, jusqu'a 1M+ lignes) | Limitee (5M cellules max) |
| **Collaboration** | Co-authoring (SharePoint) | Natif, temps reel |

---

## 10. Formula Patterns Library

### Patron : Recherche avec fallback

```
=LET(
    result1, XLOOKUP(A2, tbl_Primary[Key], tbl_Primary[Value]),
    result2, XLOOKUP(A2, tbl_Secondary[Key], tbl_Secondary[Value]),
    IF(NOT(ISNA(result1)), result1, IF(NOT(ISNA(result2)), result2, "Non trouve"))
)
```

### Patron : Extraction de texte structuree

```
// Extraire le code postal d'une adresse (format francais : 5 chiffres)
=LET(
    addr, A2,
    pos, AGGREGATE(15, 6, FIND({0,1,2,3,4,5,6,7,8,9}, addr & "0123456789", ROW($1:$100)), 1),
    MID(addr, pos, 5)
)

// Alternative avec XLOOKUP sur un pattern
=TEXTAFTER(TEXTBEFORE(A2, " ", -1), " ", -1)
```

### Patron : Calcul de jours ouvrables avec jours feries

```
=LET(
    debut, B2,
    fin, C2,
    feries, tbl_Feries[Date],
    NETWORKDAYS(debut, fin, feries)
)
```

### Patron : Categorisation dynamique avec table de reference

```
=LET(
    valeur, B2,
    seuils, tbl_Categories[Seuil_Min],
    categories, tbl_Categories[Categorie],
    XLOOKUP(valeur, seuils, categories, "Non classe", -1)
)
```

### Patron : Calcul de cumul annuel (Year-to-Date)

```
=LET(
    date_ref, B2,
    debut_annee, DATE(YEAR(date_ref), 1, 1),
    SUMIFS(tbl_Ventes[Montant],
        tbl_Ventes[Date], ">=" & debut_annee,
        tbl_Ventes[Date], "<=" & date_ref)
)
```

### Patron : Variance et ecart par rapport a la moyenne

```
=LET(
    valeur, B2,
    moyenne, AVERAGE(tbl_Data[Valeur]),
    ecart_type, STDEV(tbl_Data[Valeur]),
    z_score, (valeur - moyenne) / ecart_type,
    IF(ABS(z_score) > 2, "Anomalie", "Normal")
)
```
