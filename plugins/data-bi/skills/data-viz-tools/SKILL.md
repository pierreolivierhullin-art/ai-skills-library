---
name: data-viz-tools
version: 1.0.0
description: >
  Power BI dashboards, DAX formulas, Tableau calculated fields, Looker LookML,
  data visualization best practices, BI tool implementation, executive dashboards,
  KPI visualization, Power BI Service, Tableau Desktop, data storytelling tools,
  chart selection guide, dashboard design patterns, self-service analytics,
  Metabase, Superset, business intelligence reporting
---

# Data Viz Tools — Power BI, Tableau et Bonnes Pratiques

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu construis ou optimises un dashboard Power BI ou Tableau
- Les formules DAX ou les champs calcules Tableau sont a ecrire ou deboguer
- Tu dois choisir l'outil BI adapte a ton contexte (budget, stack, equipe)
- Les dashboards existants sont lents, confus, ou peu utilises
- Tu mets en place un self-service analytics pour des equipes non-techniques
- Tu conçois l'architecture de rapports pour une organisation

---

## Choisir son Outil BI

| Critere | Power BI | Tableau | Looker | Metabase | Superset |
|---|---|---|---|---|---|
| **Cible** | Orgs Microsoft | Analysts avances | Data teams | PME/startups | Data engineers |
| **Courbe apprentissage** | Moyenne | Elevee | Elevee | Faible | Moyenne |
| **DAX / Calculs** | DAX (puissant) | LOD Expressions | LookML | SQL | SQL/Python |
| **Tarif** | 10 EUR/user/mois | 70 EUR/user/mois | Sur devis | Gratuit OSS | Gratuit OSS |
| **Gouvernance** | Certifie, lineage | Governance limitee | Semantic layer fort | Basique | Basique |
| **Integration Azure/M365** | Natif | Partiel | Non | Non | Non |

**Recommandation par contexte** :
- Orgs Microsoft (Azure, Office 365) : **Power BI**
- Analysts avec besoin de visualisations avancees : **Tableau**
- Data governance centralisee, SQL-first : **Looker**
- PME, equipes techniques auto-suffisantes : **Metabase** (open-source)

---

## Power BI — DAX Fondamentaux

### Measures vs Calculated Columns

```dax
// Calculated Column (compute once, stored in model)
// Utiliser pour : attributs invariants, segmentation statique
// ❌ Calcule sur toutes les lignes au refresh

Categorie Age =
IF(
    Clients[Age] < 25, "18-24",
    IF(Clients[Age] < 35, "25-34",
    IF(Clients[Age] < 45, "35-44", "45+"))
)

// Measure (compute on demand, context-aware)
// Utiliser pour : metriques, aggregations, KPIs
// ✅ Calcule seulement quand necessaire, dans le filtre context actif

CA Total = SUM(Commandes[Montant])

CA Moyen par Commande = DIVIDE([CA Total], COUNTROWS(Commandes), 0)
```

### DAX — Patterns Essentiels

```dax
// ===== CALCULS TEMPORELS =====

// MTD (Month-To-Date)
CA MTD = CALCULATE([CA Total], DATESMTD(Calendrier[Date]))

// YTD (Year-To-Date)
CA YTD = CALCULATE([CA Total], DATESYTD(Calendrier[Date]))

// Meme periode annee precedente
CA Annee Precedente = CALCULATE(
    [CA Total],
    SAMEPERIODLASTYEAR(Calendrier[Date])
)

// Croissance YoY (%)
Croissance YoY =
DIVIDE(
    [CA Total] - [CA Annee Precedente],
    [CA Annee Precedente],
    BLANK()
)

// Rolling 12 mois
CA Rolling 12M = CALCULATE(
    [CA Total],
    DATESINPERIOD(
        Calendrier[Date],
        LASTDATE(Calendrier[Date]),
        -12, MONTH
    )
)


// ===== CONTEXTE ET FILTRES =====

// CALCULATE : modifier le contexte de filtre
CA France = CALCULATE([CA Total], Geographie[Pays] = "France")

// ALL : ignorer tous les filtres
Part de marche % =
DIVIDE(
    [CA Total],
    CALCULATE([CA Total], ALL(Produits)),
    0
)

// ALLEXCEPT : ignorer tous les filtres sauf certaines colonnes
Part par Region =
DIVIDE(
    [CA Total],
    CALCULATE([CA Total], ALLEXCEPT(Geographie, Geographie[Continent]))
)

// SELECTEDVALUE : obtenir la valeur selectionnee (slicer)
Titre Dynamique =
"CA - " & SELECTEDVALUE(Calendrier[Annee], "Toutes annees")


// ===== RANKING ET TOPN =====

// Rang des produits par CA
Rang Produit = RANKX(
    ALL(Produits[Nom]),
    [CA Total],
    ,
    DESC,
    Dense
)

// Top 10 produits
Top 10 Produits = CALCULATE(
    [CA Total],
    TOPN(10, ALL(Produits), [CA Total], DESC)
)
```

### Modele de Donnees — Etoile vs Flocon

```
✅ Schema en etoile (recommande Power BI)

         Calendrier
              |
Produits -- Commandes -- Clients
              |
          Geographie

Regles :
- Tables de faits (Commandes, Ventes) : lignes, FK, mesures numeriques
- Tables de dimensions (Produits, Clients, Calendrier) : attributs descriptifs
- Relations 1-N uniquement (pas de many-to-many direct)
- Une seule table de calendrier, liee a toutes les colonnes date

❌ Flocon de neige (a eviter)
Produits → Sous-categories → Categories
→ Jointures multiples = queries lentes, DAX complexe
```

---

## Tableau — LOD Expressions

Les Level of Detail (LOD) Expressions permettent de calculer a un niveau de granularite different du niveau de la visualisation.

```
// FIXED : calcul independamment du niveau de detail de la vue
{ FIXED [Client ID] : MIN([Date Premiere Commande]) }
// → Date premiere commande par client, meme si la vue est agregee par mois

// INCLUDE : ajouter une dimension au niveau d'agregation
{ INCLUDE [Produit] : SUM([Ventes]) }
// → Ventes par produit ET par les dimensions de la vue

// EXCLUDE : retirer une dimension du niveau d'agregation
{ EXCLUDE [Mois] : SUM([Ventes]) }
// → Total sans la granularite mensuelle (utile pour les parts %)
```

### Exemples Pratiques Tableau

```
// Taux de retention (LOD)
Clients Retenus =
{
  FIXED [Cohorte Mois] :
  COUNTD(
    IF DATEDIFF('month', [Premiere Commande], [Date Commande]) > 0
    THEN [Client ID]
    END
  )
}

// Panier moyen (excluant les remises > 50%)
Panier Moyen Propre =
IF [Remise %] < 0.5
THEN [Montant Commande]
END
// Agregation : AVG([Panier Moyen Propre])

// Croissance MoM
Croissance MoM =
(SUM([Ventes]) - LOOKUP(SUM([Ventes]), -1)) /
ABS(LOOKUP(SUM([Ventes]), -1))
// Parametre de calcul de table : Table Down, mois
```

### Tableau Performance Best Practices

```
Optimiser les extraits (.hyper)
├── Filtrer les donnees irrelevantes avant extraction
├── Agregation : pre-agreeger si possible (hourly → daily)
└── Utiliser les partitions pour les grands extraits

Optimiser les calculs
├── Eviter les LOD FIXED trop larges (toute la base)
├── Utiliser les champs calcules de datasource (pas de vue)
└── Eviter les IF imbriques → utiliser CASE WHEN

Optimiser la vue
├── Reduire le nombre de marques (< 5 000 recommande)
├── Pas de TOP N dans les filtres (utiliser LOD)
└── Desactiver l'animation si beaucoup de donnees
```

---

## Design de Dashboards

### Hierarchie Visuelle

```
Niveau 1 — Alertes (rouge, jaune) : KPIs critiques hors norme
    └── En haut a gauche, taille maximale, couleur forte

Niveau 2 — KPIs Principaux : metriques cles du perimetre
    └── Ligne superieure, KPI cards avec variation vs periode precedente

Niveau 3 — Contexte : graphiques de tendance, distributions
    └── Corps du dashboard, taille standard

Niveau 4 — Details : tableaux, drilldowns
    └── En bas, visible a la demande
```

### Principes de Design (CRAP)

```
Contraste : distinguer les elements importants
├── Texte sur fond : ratio > 4.5:1
├── Couleur cle : 1-2 couleurs d'accent maximum
└── Fond neutre : gris clair ou blanc, pas de gradient

Repetition : coherence visuelle
├── Meme palette couleur dans tout le dashboard
├── Meme typo (une seule famille de police)
└── Meme format de nombre (2 decimales partout ou 0 partout)

Alignement : structure et ordre
├── Grille invisible : tout aligne sur 4 ou 8px
├── Espacement consistant entre les elements
└── Groupes logiques avec separateurs

Proximite : regrouper les elements lies
├── KPIs lies dans le meme cadre
├── Filtres regroupes ensemble (haut ou gauche)
└── Legende pres du graphique qu'elle decrit
```

### Selection du Bon Graphique

| Question business | Graphique recommande |
|---|---|
| Evolution dans le temps | Ligne (1 metrique), Multi-lignes (comparaison) |
| Comparaison de valeurs | Barre horizontale (si long labels), Barre verticale |
| Composition (parties d'un tout) | Barre empilee (% ou valeur), Treemap (si nombreuses categories) |
| Distribution | Histogramme, Box plot |
| Correlation | Scatter plot |
| Geographie | Carte choroplethique, Carte a bulles |
| KPI unique | Big number + sparkline + variation % |

---

## Metabase — Self-Service Rapide

```sql
-- Metabase : questions natives en SQL ou interface graphique
-- Exemple de question native SQL

SELECT
    DATE_TRUNC('month', created_at) AS mois,
    COUNT(*) AS nb_commandes,
    SUM(total_amount) AS ca,
    AVG(total_amount) AS panier_moyen,
    COUNT(DISTINCT customer_id) AS clients_uniques
FROM orders
WHERE
    created_at >= DATE_TRUNC('month', NOW() - INTERVAL '12 months')
    AND status NOT IN ('cancelled', 'refunded')
GROUP BY 1
ORDER BY 1
```

```json
// Metabase API : embedded analytics
// Integrer un dashboard dans une app (iframe avec token signé)
{
  "resource": { "dashboard": 42 },
  "params": { "customer_id": "{{user_id}}" },
  "exp": 1740000000
}
// Signer avec METABASE_SECRET_KEY → URL embedable sans login
```

---

## Gouvernance BI

### Certification et Lineage

```
Power BI — Modele de certification
Promoteur (equipe data) → Certifie (data governance) → Public

Apache Atlas / OpenLineage — Lineage automatique
Source (Postgres) → dbt model → Power BI dataset → Dashboard
→ Impact analysis : si la table source change, quels dashboards sont affectes ?
```

### Checklist Dashboard Production

```
Donnees
├── ✅ Source de verite documentee (quelle table, quelle logique)
├── ✅ Frequence de refresh definie et respectee
└── ✅ Alertes sur les erreurs de refresh

Design
├── ✅ Titre et perimetre clairement indiques
├── ✅ Derniere mise a jour visible
└── ✅ Filtres avec valeurs par defaut pertinentes

Performance
├── ✅ Temps de chargement < 3 secondes
├── ✅ Pas de calculs redondants (measures plutot que columns)
└── ✅ Volume de donnees optimise (pas de SELECT * en temps reel)

Accessibilite
├── ✅ Palette daltonienne compatible
├── ✅ Valeurs numeriques avec unite (EUR, %, k)
└── ✅ Glossaire des metriques accessible
```

---

## References

- `references/power-bi-dax.md` — DAX avance : iterator functions, SUMX, AVERAGEX, variables
- `references/tableau-advanced.md` — LOD avancees, table calculations, set actions, extensions
- `references/dashboard-design.md` — Hierarchie, CRAP, storytelling, charte graphique BI
- `references/case-studies.md` — 4 cas : exec dashboard Power BI, Tableau operations, migration Metabase
