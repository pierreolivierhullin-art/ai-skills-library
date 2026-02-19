# Power BI et DAX — Guide Avance

## Vue d'ensemble

Power BI est la plateforme BI de Microsoft combinant un moteur analytique colonnaire (VertiPaq), un langage de formules (DAX) et un service cloud. Maitriser DAX — Data Analysis Expressions — est le facteur differentiant entre un rapport basique et un modele analytique robuste capable de repondre a des questions metier complexes. Ce guide couvre les patterns DAX avances, l'optimisation des performances et la configuration Power BI Service pour des deploiements en production.

---

## 1. CALCULATE et les Modificateurs de Contexte

### 1.1 Fonctionnement de CALCULATE

`CALCULATE` est la fonction la plus puissante de DAX. Elle evalue une expression en modifiant le contexte de filtre courant.

```dax
CALCULATE(<expression>, <filtre1>, <filtre2>, ...)
```

Mecanisme interne :
1. Le contexte de ligne courant est converti en contexte de filtre (transition de contexte)
2. Les filtres passes en argument s'appliquent sur le modele
3. L'expression est evaluee dans ce nouveau contexte

```dax
-- Exemple : CA France independamment du filtre Pays dans le rapport
CA France =
CALCULATE(
    SUM(Ventes[Montant]),
    Pays[Pays] = "France"
)

-- Le filtre "France" remplace tout filtre existant sur la colonne Pays
```

### 1.2 ALL, ALLEXCEPT, ALLSELECTED

`ALL` supprime tous les filtres sur une table ou colonne :

```dax
-- Part de marche : CA pays / CA total
Part Marche =
DIVIDE(
    SUM(Ventes[Montant]),
    CALCULATE(SUM(Ventes[Montant]), ALL(Pays))
)
```

`ALLEXCEPT` supprime tous les filtres SAUF ceux des colonnes specifiees :

```dax
-- CA sur l'annee, en preservant le filtre Pays mais ignorant le mois
CA Annuel =
CALCULATE(
    SUM(Ventes[Montant]),
    ALLEXCEPT(Calendrier, Calendrier[Annee])
)
```

`ALLSELECTED` preserve les filtres appliques par l'utilisateur (slicers) mais ignore les filtres de ligne et de colonne du visuel :

```dax
-- Part de marche relative a la selection de l'utilisateur
Part Marche Selection =
DIVIDE(
    SUM(Ventes[Montant]),
    CALCULATE(SUM(Ventes[Montant]), ALLSELECTED(Pays))
)
```

### 1.3 KEEPFILTERS et REMOVEFILTERS

`KEEPFILTERS` modifie le comportement de CALCULATE pour conserver les filtres existants et appliquer une intersection (au lieu d'un remplacement) :

```dax
-- Sans KEEPFILTERS : affiche toujours le CA France meme si filtre sur Espagne
CA France Simple =
CALCULATE(SUM(Ventes[Montant]), Pays[Pays] = "France")

-- Avec KEEPFILTERS : renvoie vide si le filtre visuel exclut France
CA France Safe =
CALCULATE(
    SUM(Ventes[Montant]),
    KEEPFILTERS(Pays[Pays] = "France")
)
```

`REMOVEFILTERS` (alias de ALL utilise en argument de CALCULATE) supprime explicitement les filtres :

```dax
Total Global =
CALCULATE(
    SUM(Ventes[Montant]),
    REMOVEFILTERS(Calendrier),
    REMOVEFILTERS(Pays)
)
```

---

## 2. Variables DAX — VAR/RETURN

Les variables ameliorent la lisibilite et les performances en evitant les evaluations repetees.

### 2.1 Syntaxe et avantages

```dax
Croissance YoY =
VAR CA_Actuel = SUM(Ventes[Montant])
VAR CA_Precedent =
    CALCULATE(
        SUM(Ventes[Montant]),
        SAMEPERIODLASTYEAR(Calendrier[Date])
    )
VAR Variation = DIVIDE(CA_Actuel - CA_Precedent, CA_Precedent)
RETURN
    IF(
        ISBLANK(CA_Precedent),
        BLANK(),
        Variation
    )
```

Avantages :
- Chaque variable est calculee une seule fois (pas de double evaluation)
- Possibilite d'utiliser la variable dans plusieurs endroits du RETURN
- Le contexte de filtre est capture au moment de la declaration de la variable
- Facilite le debogage : remplacer RETURN par la variable pour isoler

### 2.2 Attention au contexte capture

```dax
-- ATTENTION : le contexte est capture dans la VAR, pas au moment du RETURN
Mauvais Pattern =
VAR Filtre = ALLSELECTED(Produits)
-- Si on utilise Filtre dans RETURN, il reflete le contexte DE DECLARATION
RETURN CALCULATE(SUM(Ventes[Montant]), Filtre)
```

---

## 3. Fonctions Iterator — SUMX, AVERAGEX, MAXX, RANKX

### 3.1 Quand utiliser un iterator vs une agregation simple

| Situation | Recommandation |
|-----------|----------------|
| Colonne existante, simple somme | `SUM(Table[Colonne])` |
| Calcul ligne par ligne puis somme | `SUMX(Table, expression)` |
| Marge = Quantite * Prix - Cout | `SUMX(Ventes, Ventes[Qte] * RELATED(Produits[Prix]) - Ventes[Cout])` |
| Moyenne ponderee | `DIVIDE(SUMX(...), SUMX(...))` |

```dax
-- Marge brute : calcul ligne par ligne obligatoire
Marge Brute =
SUMX(
    Ventes,
    Ventes[Quantite] * (RELATED(Produits[Prix]) - RELATED(Produits[Cout]))
)

-- ATTENTION : SUM(Ventes[Quantite]) * AVERAGE(Produits[Prix]) est INCORRECT
-- Car la moyenne des prix n'est pas ponderee par les volumes
```

### 3.2 RANKX — Classement dynamique

```dax
-- Classement des produits par CA (Dense, du plus grand au plus petit)
Rang Produit =
RANKX(
    ALLSELECTED(Produits[Produit]),
    [CA Total],
    ,
    DESC,
    Dense
)

-- Top N dynamique avec parametre
Est Top N =
VAR N = SELECTEDVALUE(Parametre[N], 10)
RETURN IF([Rang Produit] <= N, 1, 0)
```

### 3.3 AVERAGEX et MAXX

```dax
-- Panier moyen : CA total / nombre de transactions (pas moyenne des montants lignes)
Panier Moyen =
AVERAGEX(
    VALUES(Commandes[CommandeID]),
    CALCULATE(SUM(Ventes[Montant]))
)

-- Maximum du CA journalier sur la periode selectionnee
Pic CA Journalier =
MAXX(
    VALUES(Calendrier[Date]),
    CALCULATE(SUM(Ventes[Montant]))
)
```

---

## 4. Intelligence Temporelle Avancee

Prerequis : la table Calendrier doit etre marquee comme "Table de dates" dans Power BI.

### 4.1 Comparaisons periode sur periode

```dax
-- CA meme periode annee precedente
CA PY =
CALCULATE(
    [CA Total],
    SAMEPERIODLASTYEAR(Calendrier[Date])
)

-- CA mois precedent
CA PM =
CALCULATE(
    [CA Total],
    PREVIOUSMONTH(Calendrier[Date])
)

-- DATEADD : flexible, n'importe quelle granularite
CA -3 Mois =
CALCULATE(
    [CA Total],
    DATEADD(Calendrier[Date], -3, MONTH)
)

-- PARALLELPERIOD : periode complete (vs DATEADD qui decale la selection courante)
CA Trimestre Precedent =
CALCULATE(
    [CA Total],
    PARALLELPERIOD(Calendrier[Date], -1, QUARTER)
)
```

### 4.2 DATESBETWEEN et DATESINPERIOD

```dax
-- CA entre deux dates fixes
CA Periode Fixe =
CALCULATE(
    SUM(Ventes[Montant]),
    DATESBETWEEN(Calendrier[Date], DATE(2024,1,1), DATE(2024,6,30))
)

-- CA sur les 90 derniers jours glissants
CA 90 Jours =
CALCULATE(
    SUM(Ventes[Montant]),
    DATESINPERIOD(
        Calendrier[Date],
        MAX(Calendrier[Date]),
        -90,
        DAY
    )
)

-- YTD (Year-to-Date) avec DATESYTD
CA YTD =
CALCULATE([CA Total], DATESYTD(Calendrier[Date]))

-- YTD exercice fiscal (termine en mars)
CA YTD Fiscal =
CALCULATE([CA Total], DATESYTD(Calendrier[Date], "03-31"))
```

### 4.3 Calculs de croissance robustes

```dax
Croissance YoY % =
VAR CA_N = [CA Total]
VAR CA_N1 = [CA PY]
RETURN
    SWITCH(
        TRUE(),
        ISBLANK(CA_N) && ISBLANK(CA_N1), BLANK(),
        ISBLANK(CA_N1), BLANK(),   -- Pas de base de comparaison
        CA_N1 = 0, BLANK(),         -- Division par zero
        DIVIDE(CA_N - CA_N1, ABS(CA_N1))
    )
```

---

## 5. Filtrage Avance et Patterns SWITCH

### 5.1 FILTER avec CALCULATE

```dax
-- CA des clients dont le segment est Premium OU Gold
CA Premium Gold =
CALCULATE(
    SUM(Ventes[Montant]),
    Clients[Segment] IN {"Premium", "Gold"}
)

-- Equivalent avec FILTER (moins performant sur grandes tables)
CA Premium Gold v2 =
CALCULATE(
    SUM(Ventes[Montant]),
    FILTER(
        ALL(Clients[Segment]),
        Clients[Segment] IN {"Premium", "Gold"}
    )
)
```

### 5.2 SWITCH pattern pour les metriques dynamiques

```dax
-- Metrique selectionnee via un slicer
Metrique Dynamique =
VAR Selection = SELECTEDVALUE(ListeMetriques[Metrique], "CA")
RETURN
    SWITCH(
        Selection,
        "CA",      [CA Total],
        "Marge",   [Marge Brute],
        "Quantite", SUM(Ventes[Quantite]),
        "Panier",  [Panier Moyen],
        BLANK()
    )
```

### 5.3 Segmentation RFM en DAX

```dax
-- Score Recence (1-5, 5 = plus recent)
Score Recence =
VAR Derniere_Date = MAX(Ventes[Date])
VAR Jours_Inactif = DATEDIFF(Derniere_Date, TODAY(), DAY)
RETURN
    SWITCH(
        TRUE(),
        Jours_Inactif <= 30,  5,
        Jours_Inactif <= 60,  4,
        Jours_Inactif <= 90,  3,
        Jours_Inactif <= 180, 2,
        1
    )

-- Score Frequence (1-5)
Score Frequence =
VAR Nb_Commandes = CALCULATE(DISTINCTCOUNT(Ventes[CommandeID]))
RETURN
    SWITCH(
        TRUE(),
        Nb_Commandes >= 20, 5,
        Nb_Commandes >= 10, 4,
        Nb_Commandes >= 5,  3,
        Nb_Commandes >= 2,  2,
        1
    )

-- Segment RFM combine
Segment RFM =
VAR Score = [Score Recence] * 100 + [Score Frequence] * 10 + [Score Monetaire]
RETURN
    SWITCH(
        TRUE(),
        Score >= 444, "Champions",
        Score >= 333, "Loyaux",
        Score >= 311, "A risque",
        Score >= 211, "En danger",
        "Perdus"
    )
```

---

## 6. Parametres What-If

Les parametres what-if permettent des simulations interactives via des slicers.

```dax
-- Creation via l'interface : Modelisation > Nouveau parametre
-- Power BI genere automatiquement :

-- Table de parametre
Taux Croissance = GENERATESERIES(0, 0.5, 0.01)
Taux Croissance[Valeur] -- colonne de valeurs
Taux Croissance Selectionne = SELECTEDVALUE('Taux Croissance'[Taux Croissance], 0.1)

-- Utilisation dans une mesure
CA Projete =
[CA Total] * (1 + [Taux Croissance Selectionne])

-- Simulation du seuil de rentabilite
Marge Apres Remise =
VAR Remise = [Taux Remise Selectionne]
RETURN
    SUMX(
        Ventes,
        Ventes[Quantite] * RELATED(Produits[Prix]) * (1 - Remise)
        - Ventes[Cout]
    )
```

---

## 7. Optimisation des Performances DAX

### 7.1 Regles fondamentales

Preferer les agregations de colonnes aux iterations :

```dax
-- LENT : FILTER(ALL(...)) force un scan de toutes les lignes
CA Segment Lent =
CALCULATE(
    SUM(Ventes[Montant]),
    FILTER(ALL(Clients), Clients[Segment] = "Premium")
)

-- RAPIDE : filtre direct sur la colonne (utilise l'index VertiPaq)
CA Segment Rapide =
CALCULATE(
    SUM(Ventes[Montant]),
    Clients[Segment] = "Premium"
)
```

### 7.2 Utiliser CALCULATETABLE

```dax
-- Creer une table virtuelle filtree pour les iterations
Top Clients =
CALCULATETABLE(
    VALUES(Clients[ClientID]),
    TOPN(100, ALL(Clients[ClientID]), [CA Total], DESC)
)

-- Utiliser dans un SUMX
CA Top 100 =
SUMX(
    Top Clients,
    [CA Total]
)
```

### 7.3 Introduction au VertiPaq Analyzer

VertiPaq Analyzer (outil gratuit de SQLBI) analyse le modele Power BI :
- Taille par table et par colonne
- Cardinalite (valeurs distinctes)
- Taux de compression
- Colonnes avec forte cardinalite a eviter (IDs techniques, timestamps precis)

Bonnes pratiques modele :
- Supprimer les colonnes inutilisees (`Masquer dans les outils clients`)
- Reduire la cardinalite : arrondir les dates/heures, grouper les valeurs rares
- Preferer les relations 1-to-many aux Many-to-many
- Colonnes calculees dans la table de faits : attention a la memoire

```dax
-- MAUVAIS : colonne calculee sur table de faits (materialise en memoire)
-- Dans la table Ventes :
Marge Ligne = Ventes[Quantite] * (RELATED(Produits[Prix]) - RELATED(Produits[Cout]))

-- MIEUX : mesure DAX (calculee a la demande)
Marge Totale = SUMX(Ventes, Ventes[Quantite] * (RELATED(Produits[Prix]) - RELATED(Produits[Cout])))
```

---

## 8. Power BI Service — Workspaces et Apps

### 8.1 Architecture Workspaces

```
Workspace Developpement
    └─ Dataset (source)
    └─ Rapports (draft)
    └─ Dataflows (preparation)

Workspace Production
    └─ Dataset (certifie)
    └─ Rapports (publies)
    └─ App (distribution)
```

Les workspaces de nouvelle generation supportent :
- Roles (Admin, Member, Contributor, Viewer)
- Integration Git (Azure DevOps / GitHub)
- Deployment pipelines (Dev > Test > Prod)

### 8.2 Row-Level Security (RLS) Implementation

RLS cote rapport (Static RLS) :

```dax
-- Dans Power BI Desktop : Modelisation > Gerer les roles
-- Role "Region Nord"
-- Filtre sur la table Regions :
[Region] = "Nord"
```

RLS dynamique (recommande en production) :

```dax
-- La table Acces contient : Email, Region
-- Filtre sur la table Regions dans le role "Utilisateur" :
[Region] IN
    CALCULATETABLE(
        VALUES(Acces[Region]),
        Acces[Email] = USERPRINCIPALNAME()
    )
```

Validation RLS :
```
Power BI Desktop > Modelisation > Afficher en tant que roles
Power BI Service > Dataset > Securite > Tester en tant que
```

### 8.3 Row-Level Security avec USERELATIONSHIP

```dax
-- Quand la RLS filtre via des relations inactives
CA Region Utilisateur =
CALCULATE(
    SUM(Ventes[Montant]),
    USERELATIONSHIP(Ventes[RegionID], Regions[RegionID])
)
```

---

## 9. Incremental Refresh

Configuration pour les grandes tables (>1M lignes) :

```
1. Parametres requis (sensibles a la casse) :
   RangeStart = DateTime — date de debut
   RangeEnd = DateTime — date de fin

2. Dans Power Query, filtrer la table de faits :
   Table.SelectRows(Source, each
     [DateCommande] >= RangeStart and
     [DateCommande] < RangeEnd
   )

3. Modelisation > Incremental Refresh :
   - Stocker les donnees des X dernieres annees
   - Actualiser les donnees des Y derniers mois
   - Detecter les changements de donnees (optionnel)
```

Resultat : seules les periodes recentes sont re-importees, les periodes historiques restent en cache.

---

## 10. Deployment Pipelines

Les pipelines permettent la promotion Developpement > Test > Production :

```
Etape 1 : DEV
    - Iterer rapidement
    - Tester de nouvelles mesures DAX
    - Dataset pointe vers donnees de test

Etape 2 : TEST
    - UAT avec les utilisateurs metier
    - Dataset pointe vers donnees UAT
    - Regles de deploiement : changer la source de donnees automatiquement

Etape 3 : PROD
    - Dataset certifie
    - Gateway de production
    - Actualisation programmee (ex: 6h, 12h, 18h)
```

Regles de deploiement (deployment rules) : permettent de remplacer automatiquement les parametres (URL, serveur, base de donnees) lors de la promotion d'une etape a l'autre, sans modifier le rapport manuellement.

---

## 11. Checklist Production Power BI

### Modele de donnees
- [ ] Schema en etoile ou flocon (eviter les relations Many-to-Many sauf si necessaire)
- [ ] Table de dates marquee comme table de dates
- [ ] Colonnes inutiles masquees ou supprimees
- [ ] Mesures organisees en dossiers d'affichage
- [ ] Description de chaque mesure renseignee

### DAX
- [ ] Pas de FILTER(ALL(...)) remplacable par un filtre direct
- [ ] Mesures avec gestion des BLANK() et division par zero (DIVIDE)
- [ ] Variables pour les expressions repetees
- [ ] Performance testee avec le DAX Studio (plan de requete)

### Securite
- [ ] RLS dynamique configure et teste
- [ ] Roles valides avec comptes de test
- [ ] Donnees sensibles masquees pour les roles concernes

### Service
- [ ] Incremental refresh sur les tables > 1M lignes
- [ ] Actualisation programmee testee
- [ ] App configuree avec l'audience correcte
- [ ] Endorsement (Certifie ou Promu) configure

---

## References et Outils

- **DAX Studio** : outil gratuit d'analyse et de debogage DAX (daxstudio.org)
- **VertiPaq Analyzer** : analyse du modele en memoire (SQLBI)
- **SQLBI.com** : ressource de reference pour DAX avance (Marco Russo, Alberto Ferrari)
- **DAX Formatter** : formater le code DAX (daxformatter.com)
- **Power BI Community** : forum officiel Microsoft
