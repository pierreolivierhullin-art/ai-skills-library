# Tableau Desktop — LOD Avancees et Optimisation

## Vue d'ensemble

Tableau Desktop est reconnu pour sa richesse analytique : les LOD Expressions (Level of Detail), les Table Calculations et les actions dynamiques permettent de construire des analyses sophistiquees sans code SQL. Ce guide couvre les patterns avances de Tableau, l'optimisation des performances et les choix d'architecture pour des deploiements en production sur Tableau Cloud ou Tableau Server.

---

## 1. LOD Expressions — Level of Detail

Les LOD Expressions permettent de controler le niveau de granularite d'un calcul, independamment de la granularite du visuel courant.

### 1.1 FIXED — Granularite Independante

`FIXED` calcule a un niveau de granularite fixe, independamment des dimensions dans la vue.

```tableau
// CA par client (toujours au niveau client, meme si la vue est au niveau commande)
{ FIXED [Client ID] : SUM([Montant]) }

// Part du client dans son segment
{ FIXED [Client ID] : SUM([Montant]) }
/
{ FIXED [Segment] : SUM([Montant]) }

// Date du premier achat par client (cohorte)
{ FIXED [Client ID] : MIN([Date Commande]) }
```

Comportement vis-a-vis des filtres :
- Les filtres de `Contexte` s'appliquent avant FIXED
- Les filtres normaux (non-contexte) s'appliquent APRES FIXED
- Pour qu'un filtre influence un calcul FIXED, le mettre en filtre de contexte (clic droit > Ajouter au contexte)

### 1.2 INCLUDE — Dimension Supplementaire

`INCLUDE` ajoute une dimension au niveau de detail courant de la vue.

```tableau
// Moyenne du CA par commande, affichee au niveau client
// Sans INCLUDE, AVG([Montant]) moyenne sur les lignes de la vue
// Avec INCLUDE, on descend au niveau de la commande avant de faire la moyenne

{ INCLUDE [Commande ID] : SUM([Montant]) }
// Ce calcul, place dans la vue au niveau client, donnera :
// AVG({ INCLUDE [Commande ID] : SUM([Montant]) })
// = panier moyen reel par client

// Nombre moyen de produits par commande, affiche par categorie
AVG({ INCLUDE [Commande ID] : COUNTD([Produit ID]) })
```

### 1.3 EXCLUDE — Dimension Exclue

`EXCLUDE` retire une dimension du contexte de la vue.

```tableau
// Contribution du sous-total categorie dans le visuel produit x categorie
// Sans EXCLUDE : calcul au niveau produit + categorie
// Avec EXCLUDE : calcul au niveau categorie uniquement

{ EXCLUDE [Produit] : SUM([Montant]) }
// Utilise ensuite comme denominateur pour le % de contribution produit

SUM([Montant]) / { EXCLUDE [Produit] : SUM([Montant]) }
```

### 1.4 LOD Imbriquees (Nested LOD)

```tableau
// Moyenne du CA de premier achat par cohorte mensuelle
// Etape 1 : date du premier achat par client
{ FIXED [Client ID] : MIN([Date Commande]) }

// Etape 2 : CA du mois du premier achat par client
{ FIXED [Client ID] :
    SUM(
        IF DATETRUNC('month', [Date Commande]) =
           DATETRUNC('month', { FIXED [Client ID] : MIN([Date Commande]) })
        THEN [Montant]
        END
    )
}

// Etape 3 : Moyenne du CA du premier mois par cohorte (date acquisition)
AVG(
    { FIXED [Client ID] :
        SUM(
            IF DATETRUNC('month', [Date Commande]) =
               DATETRUNC('month', { FIXED [Client ID] : MIN([Date Commande]) })
            THEN [Montant]
            END
        )
    }
)
```

### 1.5 Table-Scoped vs Datasource-Scoped

- **Datasource-scoped** (defaut) : le LOD s'applique a l'ensemble de la source de donnees
- **Table-scoped** : syntaxe `{ : SUM([Montant]) }` (sans dimension et sans mot-cle) — calcule sur la table entiere de la vue

```tableau
// Grand total absolu (datasource-scoped)
{ FIXED : SUM([Montant]) }

// Identique dans ce contexte mais semantiquement different :
// Table-scoped tient compte des filtres d'extraction
```

---

## 2. Table Calculations Avancees

Les table calculations s'appliquent APRES l'agregation, sur les resultats deja calcules dans la vue.

### 2.1 Fonctions de Base

```tableau
// Somme courante du CA
RUNNING_SUM(SUM([Montant]))

// Moyenne mobile sur 3 periodes
WINDOW_AVG(SUM([Montant]), -2, 0)
// -2 = 2 periodes en arriere, 0 = periode courante

// Somme sur une fenetre
WINDOW_SUM(SUM([Montant]), FIRST(), LAST())
// Equivalent au total de la partition

// Valeur de la periode precedente
LOOKUP(SUM([Montant]), -1)

// Position dans la partition
INDEX()

// Distance depuis le debut/fin
FIRST()   // Renvoie 0 pour la premiere ligne, -1 pour l'avant-derniere, etc.
LAST()    // Renvoie 0 pour la derniere ligne
```

### 2.2 Partition vs Addressing

Chaque table calculation doit definir :
- **Partition** : le regroupement sur lequel la calculation repart a zero
- **Addressing** : la direction dans laquelle la calculation avance

```
Exemple : vue avec Annee en colonnes, Categorie en lignes

- Addressing = Table (horizontalement) :
  RUNNING_SUM calcule le cumul sur chaque ligne (par categorie, travers les annees)

- Addressing = Table (verticalement) :
  RUNNING_SUM calcule le cumul sur chaque colonne (par annee, travers les categories)

- Addressing = Panneau (horizontalement) :
  RUNNING_SUM repart a zero pour chaque colonne
```

Recommandation : utiliser `Calcul utilisant > Avance` pour controler explicitement la partition et l'addressing, eviter `Table (horizontalement)` qui change de comportement quand la structure de la vue change.

### 2.3 Patterns Avances

```tableau
// Croissance YoY avec LOOKUP
(SUM([Montant]) - LOOKUP(SUM([Montant]), -1))
/ ABS(LOOKUP(SUM([Montant]), -1))

// Rang par partition (ex: classement par categorie)
RANK_UNIQUE(SUM([Montant]), 'desc')

// Pourcentage du total de la partition
SUM([Montant]) / TOTAL(SUM([Montant]))

// Cumulatif en % du total
RUNNING_SUM(SUM([Montant])) / TOTAL(SUM([Montant]))
// Useful pour les courbes de Pareto (80/20)
```

---

## 3. Set Actions — Selection Dynamique

Les Set Actions connectent les selections utilisateur dans la vue a des Sets, permettant des interactions complexes.

### 3.1 Highlight + Filter

```
Cas d'usage : l'utilisateur clique sur un pays dans une carte ->
les graphiques associes se filtrent sur ce pays

Configuration :
1. Creer un Set "Pays Selectionnes" (sur la dimension Pays)
2. Dashboard > Actions > Ajouter une action > Modifier le set
3. Source : Carte | Target : Set "Pays Selectionnes"
4. Running : Hovering ou Selecting
5. Clearing : Garder les membres du set / Retirer tous les membres

Utilisation du Set dans les autres feuilles :
- Filtrer sur "Dans le set" = affiche uniquement la selection
- Couleur sur "Dans le set" = highlight avec gris pour hors-selection
```

### 3.2 Comparaison Dynamique avec un Set

```tableau
// Visualisation : comparer un pays selectionne au reste du monde
IF [Pays Selectionnes]  // le set
THEN "Selection"
ELSE "Reste du monde"
END

// CA du pays selectionne vs total
SUM(IF [Pays Selectionnes] THEN [Montant] END)
/
SUM([Montant])
```

### 3.3 Pattern : Audience Dynamique pour Retargeting

```
Objectif : selectionner des clients dans un tableau ->
exporter la liste pour campagne marketing

1. Set "Clients Cibles" sur la dimension Client ID
2. Set Action : selection dans le tableau -> modifie le Set
3. Feuille separee affichant les details des clients "Dans le set"
4. Bouton download sur le dashboard
```

---

## 4. Parameter Actions — Interactivite Avancee

Les Parameter Actions lient la selection utilisateur a un parametre, ouvrant des possibilites avancees.

### 4.1 Reference Lines Dynamiques

```
Parametre "Seuil Alerte" (float, defaut 10000)
Ligne de reference sur le parametre

Parameter Action :
- Source : Graphique CA
- Cible : Parametre "Seuil Alerte"
- Field : SUM([Montant])
- Quand vide : Garder la valeur actuelle

Resultat : cliquer sur une barre fixe le seuil a la valeur de cette barre
```

### 4.2 Viz in Viz (Drill-through)

```
Parametre "Dimension Selectionnee" (string)
Parametre "Valeur Selectionnee" (string)

Parameter Action sur un graphique haute-level :
- Passe la dimension et la valeur cliquee aux parametres

Vue de detail utilise ces parametres :
IF [Pays] = [Valeur Selectionnee] THEN [Montant] END

Dashboard avec 2 feuilles :
- Vue globale (carte ou treemap)
- Vue detail (aparait/se filtre selon la selection)
```

### 4.3 Toggle de Metriques

```tableau
// Parametre "Metrique" avec valeurs : CA | Marge | Quantite | Clients
// Champ calcule "Valeur Selectionnee" :
CASE [Metrique]
WHEN "CA"       THEN SUM([Montant])
WHEN "Marge"    THEN SUM([Marge Brute])
WHEN "Quantite" THEN SUM([Quantite])
WHEN "Clients"  THEN COUNTD([Client ID])
END

// Ce champ s'utilise dans n'importe quel visuel
// Parameter Action sur les boutons du dashboard met a jour [Metrique]
```

---

## 5. Analyses de Cohortes avec LOD

### 5.1 Retention par Cohorte

```tableau
// Etape 1 : mois de premiere commande (cohorte)
Mois Cohorte = { FIXED [Client ID] : MIN(DATETRUNC('month', [Date])) }

// Etape 2 : index de periode (0 = mois acquisition, 1 = mois suivant, etc.)
Periode Index =
DATEDIFF('month', [Mois Cohorte], DATETRUNC('month', [Date]))

// Etape 3 : nombre de clients actifs par cohorte et periode
// Dimension en lignes : MONTH([Mois Cohorte])
// Dimension en colonnes : [Periode Index]
// Mesure : COUNTD([Client ID])

// Etape 4 : taux de retention = clients periode N / clients periode 0
// Table calculation : SUM / LOOKUP(SUM, FIRST())
COUNTD([Client ID]) / LOOKUP(COUNTD([Client ID]), FIRST())
// Addressing : table (horizontalement)
// Couleur : avec palette divergente (rouge = faible, vert = eleve)
```

### 5.2 Courbe de Valeur par Cohorte

```tableau
// CA cumule par cohorte depuis l'acquisition
RUNNING_SUM(SUM([Montant]))
// Partition : Mois Cohorte
// Addressing : Periode Index

// Normalise par le nombre de clients de la cohorte
RUNNING_SUM(SUM([Montant]))
/ { FIXED DATETRUNC('month', [Mois Cohorte]) :
    COUNTD([Client ID]) }
```

---

## 6. Graphiques Avances

### 6.1 Dual Axis

```
Cas d'usage : CA (barres) + Taux de croissance (ligne)

Procedure :
1. Placer SUM([Montant]) sur Lignes
2. Placer [Croissance YoY] sur Lignes (second champ)
3. Clic droit sur le second axe > Axe double
4. Clic droit > Synchroniser les axes (si echelles comparables)
5. Changer le type de marque : barres pour CA, ligne pour croissance
6. Adapter les couleurs pour distinguer les series
```

### 6.2 Bump Chart (Classement dans le temps)

```tableau
// Rang dynamique par periode
RANK_UNIQUE(SUM([Montant]), 'desc')
// Partition : Produit (ou Categorie)
// Addressing : Date (Mois)

// L'axe Y est inverse (Rang 1 en haut)
// Type de marque : Ligne + Cercle
// Label : INDEX() ou [Produit]
```

---

## 7. Tableau Extensions API

Les extensions permettent d'integrer des visualisations personnalisees (D3.js, Plotly) ou des fonctionnalites tierces (ML, formulaires) dans un dashboard Tableau.

```javascript
// Structure d'une extension Tableau
// Fichier .trex (manifest XML) + fichier HTML/JS

// Connexion au dashboard
tableau.extensions.initializeAsync().then(() => {
    const dashboard = tableau.extensions.dashboardContent.dashboard;

    // Ecouter les changements de selection
    dashboard.worksheets.forEach(sheet => {
        sheet.addEventListener(
            tableau.TableauEventType.MarkSelectionChanged,
            handleMarkSelection
        );
    });
});

// Recuperer les donnees d'une feuille
async function getData(worksheetName) {
    const sheet = dashboard.worksheets.find(w => w.name === worksheetName);
    const data = await sheet.getSummaryDataAsync();
    return data.data; // Array de DataValue
}
```

Extensions disponibles sur Tableau Exchange :
- **Analytics Extension** : connecter Tableau a Python/R pour le scoring ML en temps reel
- **Einstein Discovery** : predictions directement dans la vue
- **Writeback** : saisie de donnees directement dans Tableau

---

## 8. Optimisation des Performances

### 8.1 Extrait vs Connexion Directe (Live)

| Critere | Extrait | Live |
|---------|---------|------|
| Performances | Excellent (in-memory) | Dependant de la BDD |
| Fraicheur | Rafraichissement programme | Temps reel |
| Volume max | Limite RAM Tableau Server | Illimite (push vers BDD) |
| Recommande pour | Rapports < 200M lignes | Tableaux de bord operationnels |

Configuration de l'extrait :
```
Source de donnees > Extraire
- Filtres d'extraction : reduire le volume (ex: 2 derniers ans)
- Agregation : pre-aggreger si possible
- Masquer les champs inutilises avant extraction
```

### 8.2 Aggregation Pre-Tableau

Pour les grandes tables (>100M lignes), pre-aggreger en base de donnees :

```sql
-- Vue materialisee ou table de pre-agregation
CREATE MATERIALIZED VIEW vente_mensuelle AS
SELECT
    DATE_TRUNC('month', date_commande) AS mois,
    region_id,
    categorie_id,
    SUM(montant) AS ca_total,
    COUNT(DISTINCT commande_id) AS nb_commandes,
    COUNT(DISTINCT client_id) AS nb_clients
FROM ventes
GROUP BY 1, 2, 3;
```

### 8.3 Ordre des Filtres et Filtres de Contexte

L'ordre d'execution des filtres dans Tableau (du plus au moins prioritaire) :

```
1. Filtres d'extraction (Extract Filters)
2. Filtres de source de donnees (Data Source Filters)
3. Filtres de contexte (Context Filters) <- FIXED LOD calcule apres
4. Filtres de dimensions
5. Filtres de mesures
6. Filtres Table Calculation
```

Transformer un filtre tres selectif en filtre de contexte :
- Clic droit sur le filtre > Ajouter au contexte
- L'icone devient grise
- Tableau cree une sous-requete temporaire, reduisant le volume pour tous les autres calculs

### 8.4 Performance Recorder

```
Aide > Parametres et performance > Demarrer l'enregistrement des performances
Interagir avec le tableau de bord
Aide > Parametres et performance > Arreter l'enregistrement

Analyse :
- Executing Query : temps de requete BDD (probleme cote source)
- Geocoding : geolocalisation lente (eviter si non necessaire)
- Rendering : probleme de rendu (trop de marques)

Recommandation :
- < 5 000 marques pour les vues en scatter plot
- < 100 000 marques pour les barres/lignes
- Filtrer agressivement avant d'afficher
```

---

## 9. Tableau Prep Builder — Principes

Tableau Prep est l'outil de preparation des donnees de l'ecosysteme Tableau.

### 9.1 Design d'un Flow

```
Structure typique d'un flow Prep :

[Input: CSV/BDD/API]
    -> [Etape Nettoyage]
        - Renommer les colonnes
        - Changer les types (date, number, string)
        - Filtrer les lignes invalides
        - Remplacer les valeurs nulles
    -> [Etape Transformation]
        - Pivots (colonnes -> lignes ou inverse)
        - Split de colonnes (ex: "Nom Prenom" -> deux colonnes)
        - Calculs (new fields)
    -> [Jointure]
        - Join ou Union avec une autre source
    -> [Agregation]
        - Reduire la granularite avant Tableau Desktop
    -> [Output: Extrait .hyper ou publication Tableau Server]
```

### 9.2 Etapes de Nettoyage Courantes

```
Profil de colonne :
- Distribution des valeurs (barres)
- Detection automatique des valeurs aberrantes
- Mise en forme des erreurs (chiffres dans colonnes texte)

Cleaning steps :
- Group and Replace : normaliser les valeurs ("FR", "France", "france" -> "France")
  Utiliser la correspondance phonetique ou la correspondance orthographique
- Filter : exclure les lignes (critere sur champs)
- Rename : standardiser les noms de champs
- Split : extraire des sous-chaines (code postal, domaine email)
```

---

## 10. Tableau Cloud vs Tableau Server

| Critere | Tableau Cloud | Tableau Server |
|---------|---------------|----------------|
| Infrastructure | Geree par Tableau/Salesforce | Auto-hebergee |
| Maintenance | Aucune (patches auto) | Equipe IT requise |
| Cout | Par utilisateur/mois | Licence serveur + infrastructure |
| Personnalisation | Limitee | Complete |
| Connectivite reseau prive | Bridge (agent local) | Direct |
| Conformite donnees sensibles | A verifier par region | Controle total |
| SAML/SSO | Oui | Oui |
| Embedded Analytics | Oui (Connected Apps) | Oui (Trusted Authentication) |

Recommandation :
- **PME / startups** : Tableau Cloud (pas de gestion serveur)
- **Grands comptes avec donnees sensibles** : Tableau Server on-premise ou cloud prive
- **Donnees sur reseau interne** : Tableau Cloud + Tableau Bridge (agent de connectivite)

---

## 11. Checklist Tableau Production

### Modelisation
- [ ] Extraits configures avec filtres d'extraction (volume reduit)
- [ ] Champs inutilises masques avant extraction
- [ ] Types de donnees corrects (dates, mesures, dimensions)
- [ ] Hierarchies definies (Annee > Trimestre > Mois > Semaine > Jour)

### Calculs
- [ ] LOD FIXED avec filtres de contexte si necessaire
- [ ] Table Calculations avec partition et addressing explicites
- [ ] Calculs testes avec des valeurs limites (null, zero, dates extremes)

### Performance
- [ ] Performance Recorder execute sur les vues cles
- [ ] Filtres tres selectifs convertis en filtres de contexte
- [ ] Marques < 5 000 pour les scatter plots
- [ ] Pre-agregation BDD pour les sources > 50M lignes

### Securite et Gouvernance
- [ ] RLS configure (User Filter ou Row Level Security Tableau Server)
- [ ] Permissions de projet et de classeur verifiees
- [ ] Rafraichissement des extraits programme et monitore

---

## References

- **Tableau Help** : help.tableau.com (documentation officielle)
- **Tableau Community** : community.tableau.com (forum et galeries)
- **LOD Reference** : tableau.com/about/blog/LOD-expressions
- **Bora Beran** : blog de reference pour LOD avancees
- **Andy Cotgreave** : The Big Book of Dashboards (design Tableau)
