# Etudes de Cas — BI Tools en Production

## Vue d'ensemble

Ces quatre etudes de cas documentent des deployments BI reels, couvrant des contextes differents : retailer multi-sites, supply chain industrielle, startup SaaS et equipe data centralisee. Chaque cas detaille le contexte, la justification du choix d'outil, l'implementation technique, les defis d'adoption et les resultats mesures. Les lecons tirees sont directement applicables a d'autres projets similaires.

---

## Cas 1 : Executive Dashboard Power BI — Retailer 50 Magasins

### Contexte

**Secteur** : retail alimentaire, 50 magasins en France
**Taille** : 2 400 employes, CA annuel 180M EUR
**Probleme initial** : chaque directeur de magasin envoyait un fichier Excel le lundi matin. La consolidation prenait 12 heures a l'equipe centrale de reporting. Les donnees etaient souvent discordantes (versions differentes du fichier, erreurs de saisie). Les comites de direction travaillaient sur des donnees a J-7.

**Objectif** : tableau de bord consolide et actualise chaque nuit, accessible aux 50 directeurs et a la direction generale.

### Choix de l'Outil

Power BI a ete retenu pour les raisons suivantes :
- Ecosysteme Microsoft deja en place (Azure SQL, Office 365)
- Licences Power BI Pro incluses dans Microsoft 365 E3 (cout marginal nul)
- Connecteur natif Azure SQL sans configuration supplementaire
- Familiarite de l'equipe IT avec l'environnement Microsoft

Outils evalues et ecartes :
- Tableau : cout de licence significatif (Tableau Creator a 70 EUR/mois/user), necessite une competence DAX equivalente (VizQL)
- Looker : complexite de LookML et necessite un data engineer dedie

### Architecture du Modele de Donnees Etoile

```
                    [DIM_Calendrier]
                          |
[DIM_Magasin] ---- [FAIT_Ventes] ---- [DIM_Produit]
                          |
                    [DIM_Segment]
                          |
                    [DIM_Employe]

Tables de faits :
- FAIT_Ventes : 180M lignes, 4 ans d'historique
  Colonnes : DateID, MagasinID, ProduitID, EmployeID,
             Quantite, MontantHT, MontantTTC, CoutAchat, Remise

- FAIT_Stock : 8M lignes (instantane quotidien)
  Colonnes : DateID, MagasinID, SkuID, QuantiteStock, ValeurStock

Dimensions :
- DIM_Calendrier : 1 461 lignes (4 ans, avec feries, semaines, exercices fiscaux)
- DIM_Magasin : 50 lignes, avec hierarchie Region > Zone > Magasin
- DIM_Produit : 22 000 lignes, avec hierarchie Rayon > Famille > Sous-famille > SKU
```

### KPIs Retenus et Mesures DAX

Comite de direction : 8 KPIs maximum sur la page executif.

```dax
-- CA Net HT (apres remises)
CA Net HT =
SUMX(
    FAIT_Ventes,
    FAIT_Ventes[Quantite] * FAIT_Ventes[MontantHT] * (1 - FAIT_Ventes[Remise])
)

-- Marge Brute %
Marge Brute Pct =
VAR Marge = SUMX(FAIT_Ventes,
    FAIT_Ventes[Quantite] * (FAIT_Ventes[MontantHT] - RELATED(DIM_Produit[CoutAchat]))
)
VAR CA = [CA Net HT]
RETURN DIVIDE(Marge, CA)

-- Panier Moyen (CA / nombre de transactions)
Panier Moyen =
DIVIDE(
    [CA Net HT],
    DISTINCTCOUNT(FAIT_Ventes[TransactionID])
)

-- NPS (calcule separement depuis un systeme de feedback)
NPS Score =
VAR Promoteurs = CALCULATE(COUNTROWS(FAIT_NPS), FAIT_NPS[Score] >= 9)
VAR Detracteurs = CALCULATE(COUNTROWS(FAIT_NPS), FAIT_NPS[Score] <= 6)
VAR Total = COUNTROWS(FAIT_NPS)
RETURN DIVIDE(Promoteurs - Detracteurs, Total) * 100

-- Taux de rupture de stock
Taux Rupture =
DIVIDE(
    CALCULATE(COUNTROWS(FAIT_Stock), FAIT_Stock[QuantiteStock] = 0),
    COUNTROWS(FAIT_Stock)
)

-- CA YoY avec gestion des periodes incompletes
CA YoY Pct =
VAR CA_N = [CA Net HT]
VAR CA_N1 = CALCULATE([CA Net HT], SAMEPERIODLASTYEAR(DIM_Calendrier[Date]))
RETURN
    IF(
        ISBLANK(CA_N1) || CA_N1 = 0,
        BLANK(),
        DIVIDE(CA_N - CA_N1, ABS(CA_N1))
    )
```

### Gouvernance et Adoption

Phase 1 — Pilote (mois 1-2) :
- 5 directeurs de magasin volontaires
- Sessions de 2 heures chacun avec le data analyst
- Feedback : "trop de donnees sur une page", "le filtre de date n'est pas intuitif"
- Iterations : reduction de 24 a 8 KPIs sur la page principale, simplification des filtres

Phase 2 — Deploiement (mois 3-4) :
- Formation en groupe de 10 directeurs (sessions de 3h)
- Support par champion : 2 directeurs "power users" par region designes
- Documentation : guide de 12 pages avec captures d'ecran

Phase 3 — Certification (mois 5-6) :
- Certification interne "Power BI Directeur" (QCM 20 questions)
- Seuls les certifies ont acces en lecture aux datasets

Gouvernance :
- Dataset unique certifie, gere par l'equipe data (3 personnes)
- Aucun directeur ne peut creer de dataset — uniquement des rapports a partir du dataset certifie
- Comite de gouvernance mensuel : demandes de nouvelles metriques, validation des definitions

### Resultats

- **12 heures de reporting manuel elimine par semaine** (equipe centrale)
- **Latence des donnees** : de J-7 a J-1 (actualisation chaque nuit a 5h00)
- **Adoption** : 47/50 directeurs consultent le dashboard au moins 1 fois par semaine (suivi via Power BI Service)
- **Decisions accelerees** : 3 magasins ont detecte des ruptures de stock anormales et reapprovisionne sous 24h (vs 7 jours auparavant)
- **NPS interne** : 8.1/10 (enquete 6 mois post-deploiement)

### Lecons

1. Commencer par 5 KPIs max sur la page principale — les utilisateurs peuvent toujours demander plus, il est difficile de retirer ce qu'on a deja donne
2. Impliquer les directeurs dans le choix des KPIs (co-construction) augmente significativement l'adoption
3. Le dataset certifie unique est critique — les "shadow BI" (datasets personnels) creent rapidement des incoherences
4. La formation initiale de 3 heures est insuffisante — prevoir un suivi a J+30

---

## Cas 2 : Tableau Operational Dashboard — Supply Chain 200 Utilisateurs

### Contexte

**Secteur** : industriel, fabrication d'equipements electroniques
**Taille** : 1 800 employes, 12 sites de production en Europe
**Probleme initial** : les responsables logistique produisaient des rapports Excel quotidiens a partir de l'ERP SAP. Le cycle de decision (detection d'un probleme -> reaction) etait de 48-72 heures. Les ruptures de stock de composants critiques provoquaient des arrets de production coutant en moyenne 80 000 EUR par heure.

**Objectif** : dashboard operationnel en quasi-temps reel (actualisation toutes les 2 heures), alertes automatiques sur les seuils critiques, accessible a 200 utilisateurs (responsables logistique, acheteurs, responsables de site).

### Choix de Tableau

Tableau a ete retenu car :
- L'equipe analytics (6 personnes) avait deja des competences Tableau solides
- Les besoins d'interactivite (drill-down sur un article, comparaison multi-sites) sont mieux servis par Tableau que Power BI pour les utilisateurs analytiques
- La licence Tableau Server (on-premise) permettait de garder les donnees sur les serveurs internes (donnees industrielles sensibles)
- Le connecteur SAP HANA natif Tableau evitait un ETL intermediaire complexe

### Architecture Tableau Server

```
[SAP HANA (source)](on-premise)
    |
    v
[Connexion Tableau via JDBC]
    |
    +---> [Extrait .hyper : 400M lignes]  (actualisation toutes les 2h)
    |
[Tableau Server (on-premise, 2 noeuds)]
    |
    +---> Workbooks : Approvisionnement, Stock, Fournisseurs, Production
    |
    +---> Tableau Bridge (pour futurs besoins cloud)

Infrastructure :
- 2 serveurs Tableau (Active/Active pour la haute disponibilite)
- 32 Go RAM par serveur (moteur in-memory pour les extraits)
- LDAP pour l'authentification (integration Active Directory)
```

### RLS par Region

Chaque responsable logistique ne voit que les articles de son perimetre :

```
Table de permissions (maintenue par les RH/IT) :
Username | Site | Region
jdupont  | Lyon | EMEA-Sud
mmartini | Milan | EMEA-Sud
kmuller  | Berlin | EMEA-Nord

Filtre User dans Tableau Desktop (colonne Site) :
USERNAME() = [Table_Permissions].[Username]

Implementation via "User Filter" Tableau :
1. Ouvrir le classeur dans Tableau Desktop
2. Serveur > Creer un filtre utilisateur
3. Selectionner la dimension Site
4. Assigner les sites a chaque utilisateur
5. Publier sur Tableau Server avec le filtre verrouille
```

### Alertes Automatiques sur Stock

Tableau Server offre des alertes natives sur les extraits :

```
Configuration des alertes :
1. Vue "Stock par Article" avec la mesure [Quantite Stock]
2. Clic droit sur la valeur -> Creer une alerte
3. Condition : [Quantite Stock] < [Seuil Critique]
4. Destinataires : responsable logistique du site + responsable achat
5. Frequence : verification a chaque actualisation (toutes les 2h)

Calcul Tableau pour le seuil dynamique :
// Seuil critique = consommation moyenne * lead time fournisseur * facteur securite
[Consommation Moyenne Journaliere] * [Lead Time Jours] * 1.3

// Statut article (feu rouge/orange/vert)
IF [Quantite Stock] < [Seuil Critique]        THEN "Critique"
ELSEIF [Quantite Stock] < [Seuil Precaution]  THEN "Precaution"
ELSE "OK"
END
```

### Performance Tuning — 400M Lignes

Probleme initial : extraction SAP HANA complete = 6 heures. Inutilisable pour une actualisation bi-horaire.

Solution en 3 etapes :

**Etape 1 : Pre-agregation SAP HANA**
```sql
-- Vue materialisee dans SAP HANA (calcul fait cote serveur)
CREATE VIEW V_STOCK_AGREGE AS
SELECT
    MANDT,
    WERKS AS SITE_CODE,
    MATNR AS ARTICLE_CODE,
    LGORT AS EMPLACEMENT,
    BUDAT AS DATE_MOUVEMENT,
    SUM(MENGE) AS QTE_STOCK,
    MAX(DMBTR) AS VALEUR_STOCK
FROM MSEG
WHERE BUDAT >= ADD_DAYS(CURRENT_DATE, -365)
GROUP BY MANDT, WERKS, MATNR, LGORT, BUDAT;
-- Resultat : 400M lignes -> 12M lignes
```

**Etape 2 : Filtres d'extraction Tableau**
```
Source de donnees > Extrait > Ajouter un filtre
- DATE_MOUVEMENT >= TODAY() - 365 (1 an glissant)
- STATUT_ARTICLE NOT IN ('Obsolete', 'Supprime')
Resultat : 12M -> 4.5M lignes dans l'extrait
```

**Etape 3 : Actualisation incrementale**
```
Tableau Server > Source de donnees > Planification
- Actualisation complete : dimanche 2h00 (index complet)
- Actualisation incrementale : toutes les 2h (nouvelles lignes uniquement)
Critere incremental : DATE_MOUVEMENT > MAX(DATE_MOUVEMENT) de l'extrait existant
Duree extrait complet : 18 min (vs 6h initialement)
Duree extrait incremental : 4 min
```

### Resultats

- **Cycle de decision** : de 48-72h a 4-6h (detection -> action)
- **Alertes stock** : 94% des articles critiques traites avant rupture (vs 61% avant)
- **Arrets de production** : -73% d'arrets lies aux ruptures de composants (annee N vs N-1)
- **ROI calcule** : 2.1M EUR economises (arrets evites) pour 240K EUR de cout projet
- **Adoption** : 187/200 utilisateurs actifs a 3 mois (connexion hebdomadaire minimum)

### Lecons

1. La pre-agregation cote source de donnees est le levier le plus impactant sur les performances — avant d'optimiser Tableau, optimiser la requete source
2. Les alertes natives Tableau Server sont suffisantes pour 80% des cas — ne pas sur-engenierie avec des pipelines d'alertes externes
3. La RLS via User Filter est moins robuste qu'une RLS centrale — migrer vers Row-Level Security Tableau Server si le perimetre grandit
4. Former les 200 utilisateurs en une seule fois est impossible — prevoir des cohortes de 20 et des "relais" par service

---

## Cas 3 : Migration vers Metabase — Startup SaaS, Equipe de 8

### Contexte

**Secteur** : SaaS B2B, plateforme de gestion RH
**Taille** : 45 employes, ARR 3.2M EUR, serie A
**Probleme initial** : pas d'outil BI en place. Les analyses se faisaient via des requetes SQL ad-hoc dans DBeaver ou en exportant vers Excel. L'equipe produit passait 4 heures par semaine a repondre aux demandes de donnees des autres equipes.

**Contexte budget** : budget analytics de 6 000 EUR/an maximum. Tableau (840 EUR/user/an) et Power BI Premium (10-20 EUR/user/mois) etaient hors budget pour l'usage envisage.

### Pourquoi Metabase

Criteres de selection :

| Critere | Metabase | Redash | Apache Superset |
|---------|----------|--------|-----------------|
| Prise en main non-technique | Excellent | Moyen | Difficile |
| SQL-first (pour les devs) | Oui | Oui | Oui |
| Self-service sans SQL | Oui (Question Builder) | Non | Partiel |
| Hosting open-source | Oui | Oui | Oui |
| Embedded analytics | Oui (Metabase Pro) | Non | Oui (complexe) |
| Cout | 500 EUR/mois (Pro) | Gratuit | Gratuit + hosting |
| Communaute | Grande | Moyenne | Croissante |

Metabase retenu pour : prise en main des equipes metier sans SQL, embedded analytics pour les clients (roadmap 6 mois), communaute large.

### Architecture

```
[Production PostgreSQL] (ecriture application)
    |
    v (replication logique, delai ~30 secondes)
    |
[PostgreSQL Read Replica] (lecture seule)
    |
    v
[Metabase Cloud Pro] (heberge par Metabase)
    |
    +---> Collections internes (equipes)
    |         Produit | Finance | Growth | Support
    |
    +---> Embedded Analytics
              Dashboard clients (iframe signe)
```

L'utilisation d'un read replica est critique : les requetes Metabase (souvent des full scans) ne doivent jamais impacter la base de production.

### Collections et Permissions

Structure de permissions Metabase :

```
Collection "Notre Entreprise" (tous les employes, lecture)
    ├── Collection "Produit" (equipe produit, edition)
    │       ├── Dashboard : Product Metrics Weekly
    │       ├── Dashboard : Funnel d'activation
    │       └── Questions sauvegardees : Retention, DAU, Feature adoption
    │
    ├── Collection "Finance" (CFO + comptable, edition)
    │       ├── Dashboard : ARR et MRR
    │       └── Dashboard : Churn et expansion
    │
    ├── Collection "Growth" (marketing + sales, edition)
    │       └── Dashboard : Pipeline et conversions
    │
    └── Collection "Prive" (data team uniquement)
            └── Questions de travail, modeles intermediaires

Groupes :
- Admins : data team (2 personnes)
- Editeurs : leads de chaque equipe (4 personnes)
- Lecteurs : tous les autres employes (39 personnes)
- Clients (externe) : acces uniquement via embedded
```

### Embedded Analytics pour les Clients

Metabase Pro permet d'integrer des dashboards dans l'application cliente via des iframes signees :

```javascript
// Backend Node.js : generation du token signe
const jwt = require('jsonwebtoken');

function getMetabaseEmbedUrl(dashboardId, clientId) {
    const payload = {
        resource: { dashboard: dashboardId },
        params: {
            client_id: clientId  // Filtre RLS par client
        },
        exp: Math.round(Date.now() / 1000) + (10 * 60) // Expire dans 10 min
    };

    const token = jwt.sign(payload, process.env.METABASE_SECRET_KEY);
    const iframeUrl = `${process.env.METABASE_URL}/embed/dashboard/${token}#bordered=false&titled=false`;

    return iframeUrl;
}

// Frontend React : rendu de l'iframe
function ClientDashboard({ clientId }) {
    const [embedUrl, setEmbedUrl] = useState(null);

    useEffect(() => {
        fetch(`/api/analytics/embed-url?clientId=${clientId}`)
            .then(r => r.json())
            .then(data => setEmbedUrl(data.url));
    }, [clientId]);

    return embedUrl
        ? <iframe src={embedUrl} width="100%" height="600px" frameBorder="0" />
        : <LoadingSpinner />;
}
```

Le parametre `client_id` dans le payload JWT est utilise par Metabase pour filtrer automatiquement toutes les questions du dashboard — les clients ne voient que leurs propres donnees.

### Limitations Rencontrees

**Limitation 1 : Pas d'equivalent DAX**
Metabase ne supporte pas les calculs de type "intelligence temporelle" (SAMEPERIODLASTYEAR, YTD dynamique). Tout doit etre fait en SQL.

```sql
-- Workaround : views PostgreSQL pre-calculees
CREATE VIEW v_mrr_yoy AS
SELECT
    DATE_TRUNC('month', date_paiement) AS mois,
    SUM(montant) AS mrr_actuel,
    LAG(SUM(montant), 12) OVER (ORDER BY DATE_TRUNC('month', date_paiement)) AS mrr_n1,
    ROUND(
        (SUM(montant) - LAG(SUM(montant), 12) OVER (ORDER BY DATE_TRUNC('month', date_paiement)))
        / NULLIF(LAG(SUM(montant), 12) OVER (ORDER BY DATE_TRUNC('month', date_paiement)), 0) * 100,
        2
    ) AS croissance_yoy_pct
FROM paiements
WHERE statut = 'reussi'
GROUP BY 1;
-- Metabase interroge cette vue sans SQL visible pour les utilisateurs
```

**Limitation 2 : Pas de modele semantique**
Sans couche semantique, les memes metriques sont parfois definies differemment selon les questions. Solution : modeles SQL (Metabase Models) comme source de reference.

**Limitation 3 : Performance sur requetes complexes**
Les requetes impliquant plusieurs jointures sur des tables > 5M lignes depassaient les timeouts. Solution : tables de pre-agregation quotidiennes via un job Python (dbt ou script cron).

### Resultats

- **Temps de reponse aux demandes de donnees** : de 4h/semaine a 1h/semaine pour le data engineer
- **Autonomie metier** : 60% des questions sont maintenant repondues sans aide du data team (via Question Builder)
- **Embedded analytics** : fonctionnalite lancee en 3 mois, adoptee par 78% des clients actifs
- **Cout total** : 6 000 EUR/an (Metabase Pro) + 200 EUR/an (read replica RDS) vs 15 000-40 000 EUR pour Tableau/Power BI Premium

### Lecons

1. Pour une equipe < 15 personnes avec un budget contraint, Metabase est le meilleur rapport qualite/prix du marche
2. Les Models Metabase (vues SQL abstrayant la complexite) sont essentiels pour maintenir la coherence des metriques
3. L'embedded analytics justifie a elle seule le passage de Metabase Open Source a Metabase Pro
4. Prevoir des views et tables de pre-agregation dans la base de donnees des le depart — le SQL brut dans Metabase ne scale pas

---

## Cas 4 : Looker Semantic Layer — Data Team 5 Personnes, 15 Equipes Metier

### Contexte

**Secteur** : marketplace e-commerce, 350 employes
**Taille** : data team de 5 data analysts, 15 equipes metier avec des besoins analytics tres differents
**Probleme initial** : proliferation de definitions metriques. La meme metrique "taux de conversion" avait 6 definitions differentes selon les equipes (conversion sur visiteurs uniques, sur sessions, sur produits vus, sur ajouts au panier...). Les comites de direction degenereaient en debats sur les chiffres plutot que sur les decisions.

**Objectif** : single source of truth avec une couche semantique centralisee, gouvernance forte, self-service pour les 15 equipes.

### Introduction a LookML

LookML (Looker Modeling Language) est le langage de definition de la couche semantique Looker. Il definit les tables (views), les jointures (explores), les mesures et les dimensions.

```lookml
-- Fichier : views/commandes.view.lkml
view: commandes {
  sql_table_name: analytics.commandes ;;

  dimension: id {
    primary_key: yes
    type: number
    sql: ${TABLE}.commande_id ;;
  }

  dimension_group: created {
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    sql: ${TABLE}.created_at ;;
  }

  dimension: statut {
    type: string
    sql: ${TABLE}.statut ;;
  }

  measure: count {
    type: count
    label: "Nombre de commandes"
  }

  measure: total_revenu {
    type: sum
    sql: ${TABLE}.montant_ttc ;;
    value_format_name: eur
    label: "Revenu TTC"
    description: "Somme du montant TTC de toutes les commandes (hors remboursements)"
  }

  measure: taux_conversion {
    type: number
    sql: ${count} / NULLIF(${sessions.count}, 0) ;;
    value_format_name: percent_2
    label: "Taux de conversion"
    description: "Commandes / Sessions uniques. Toujours mesure sur les sessions avec au moins 1 produit vu."
  }
}
```

La definition de `taux_conversion` est unique et partagee par toutes les equipes — plus de debats sur la definition.

### Views et Explores

Un `explore` definit les jointures possibles entre les views :

```lookml
-- Fichier : models/marketplace.model.lkml
connection: "bigquery_prod"

explore: commandes {
  label: "Ventes et Commandes"

  join: clients {
    type: left_outer
    sql_on: ${commandes.client_id} = ${clients.id} ;;
    relationship: many_to_one
  }

  join: produits {
    type: left_outer
    sql_on: ${commandes.produit_id} = ${produits.id} ;;
    relationship: many_to_one
  }

  join: sessions {
    type: left_outer
    sql_on: ${commandes.session_id} = ${sessions.id} ;;
    relationship: many_to_one
  }
}

explore: stock {
  label: "Inventaire et Stock"
  -- Seules les equipes avec acces "Stock" voient cet explore
  access_filter: {
    field: entrepots.region
    user_attribute: region_acces
  }
}
```

Les utilisateurs metier acced a Looker via l'interface Explore : ils choisissent les dimensions et mesures, Looker genere le SQL optimal et execute la requete sur BigQuery.

### Derived Tables (PDT — Persistent Derived Tables)

Les PDT sont des tables pre-calculees et persistees dans BigQuery, creees et maintenues par Looker :

```lookml
-- Vue calculee : cohortes de retention (calculee 1 fois par jour)
view: retention_cohorte {
  derived_table: {
    sql:
      WITH premier_achat AS (
        SELECT
          client_id,
          DATE_TRUNC(DATE(MIN(created_at)), MONTH) AS mois_cohorte
        FROM commandes
        WHERE statut = 'complete'
        GROUP BY 1
      ),
      activite_mensuelle AS (
        SELECT
          client_id,
          DATE_TRUNC(DATE(created_at), MONTH) AS mois_activite
        FROM commandes
        WHERE statut = 'complete'
        GROUP BY 1, 2
      )
      SELECT
        p.mois_cohorte,
        DATE_DIFF(a.mois_activite, p.mois_cohorte, MONTH) AS periode_index,
        COUNT(DISTINCT a.client_id) AS clients_actifs,
        COUNT(DISTINCT p2.client_id) AS clients_cohorte
      FROM premier_achat p
      JOIN activite_mensuelle a USING (client_id)
      JOIN premier_achat p2 ON p2.mois_cohorte = p.mois_cohorte
      GROUP BY 1, 2
    ;;
    persist_for: "24 hours"
    -- La table est recalculee toutes les 24h automatiquement par Looker
  }

  dimension: mois_cohorte { type: date_month sql: ${TABLE}.mois_cohorte ;; }
  dimension: periode_index { type: number sql: ${TABLE}.periode_index ;; }

  measure: taux_retention {
    type: number
    sql: ${TABLE}.clients_actifs / NULLIF(${TABLE}.clients_cohorte, 0) ;;
    value_format_name: percent_1
  }
}
```

### Content Validator et Gouvernance

Le Content Validator Looker detecte les cassures dans les dashboards et Looks existants apres une modification du modele LookML :

```
Workflow de modification :
1. Data analyst modifie un field dans le LookML (ex: renomme une dimension)
2. Deploiement en production via Git (branch + pull request + review)
3. AVANT de merger : Content Validator
   -> Liste tous les dashboards/Looks qui referencent ce field
   -> Permet de corriger ou de confirmer que la cassure est acceptable
4. Merge et deploiement
5. Notification automatique aux proprietaires des dashboards affectes

Resultat : zero regression silencieuse (la cassure est toujours detectable avant la mise en prod)
```

### Impact Gouvernance — Single Source of Truth

Situation avant Looker :

```
15 equipes, definitions metier :
- Taux de conversion : 6 definitions differentes
- Client actif : 4 definitions (30j, 60j, 90j, "au moins 1 commande")
- Marge : 3 definitions (brute, nette, contribution)
Resultat : comites bloquant sur les chiffres, 30-45 min perdues par comite
```

Situation apres Looker (6 mois post-deploiement) :

```
Chaque metrique : 1 definition, documentee dans Looker
- Description visible par tous les utilisateurs (champ "description" LookML)
- Owner defini (champ "tags")
- Historique de modification (Git)

Metrics Store interne : 47 metriques certifiees, 12 equipes proprietaires
- Chaque equipe est responsable de ses metriques dans LookML
- Le data team valide et merge via pull requests
```

### Mesure de l'Adoption — 6 Mois Post-Deploiement

Looker fournit des donnees d'usage via son API System Activity :

```sql
-- Requete sur les tables Looker System Activity (dans BigQuery)
SELECT
  DATE_TRUNC(DATE(created_at), WEEK) AS semaine,
  COUNT(DISTINCT user_id) AS utilisateurs_actifs,
  COUNT(*) AS queries_executees,
  AVG(runtime) AS temps_moyen_requete_sec,
  COUNTIF(status = 'error') / COUNT(*) AS taux_erreur
FROM system_activity.query
WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 26 WEEK)
GROUP BY 1
ORDER BY 1;
```

Resultats a 6 mois :

| Indicateur | M+1 | M+3 | M+6 |
|------------|-----|-----|-----|
| Utilisateurs actifs hebdo | 23 | 67 | 112 |
| Queries/semaine | 450 | 1 820 | 3 240 |
| % requetes self-service (sans data team) | 34% | 61% | 78% |
| Temps moy. de reponse requete | 8.4s | 5.1s | 3.2s |
| Nb de metriques certifiees | 12 | 35 | 47 |
| Debats sur les definitions en comite | Frequent | Rare | Quasi nul |

### Lecons

1. Le ROI d'un outil semantique se mesure en heures de comite de direction recuperees, pas en requetes executees — quantifier cet impact des le depart pour justifier l'investissement
2. LookML necessite un data engineer dedie au moins a temps partiel — ne pas sous-estimer la courbe d'apprentissage (3-4 semaines avant d'etre autonome)
3. Les PDT sont extremement puissants mais peuvent creer des couts de compute BigQuery significatifs si mal configures — monitorer les couts par PDT
4. La gouvernance Git (pull requests obligatoires) est un facteur cle de succes — elle empeche les modifications non validees en production et cree un historique d'audit
5. Commencer avec les 5-6 metriques les plus disputees — livrer rapidement de la valeur avant d'etendre le modele

---

## Synthese Comparative

| Critere | Power BI | Tableau | Metabase | Looker |
|---------|----------|---------|----------|--------|
| Profil utilisateur | Business + IT | Analytique avance | Dev + business | Data team |
| Modele semantique | DAX (mesures) | Calculs (limites) | Models SQL | LookML (complet) |
| Self-service non-technique | Fort | Moyen | Fort | Moyen |
| Embedded analytics | Oui (Premium) | Oui | Oui (Pro) | Oui |
| Gouvernance | Bonne (certif.) | Bonne (Server) | Basique | Excellente (Git) |
| Ecosysteme | Microsoft | Salesforce | Open source | Google |
| Cout typique | 10-20 EUR/user/mois | 70 EUR/user/mois | 500 EUR/mois fixe | 3 000+ EUR/mois |
| Meilleur pour | Enterprise Microsoft | Analytique profonde | Startup/PME | Data team centralisee |
