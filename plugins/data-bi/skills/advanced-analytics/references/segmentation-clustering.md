# Segmentation & Clustering — RFM, K-Means, Clustering Hiérarchique & Personas

## Overview

Ce guide couvre les techniques de segmentation client et produit : analyse RFM pour la segmentation comportementale rapide, k-means et variantes pour le clustering non supervise, clustering hierarchique pour l'exploration, et DBSCAN pour les donnees a geometrie complexe. Pour chaque technique, le guide detaille la mise en oeuvre pratique, l'interpretation des segments, la validation de la qualite du clustering, et l'activation metier.

---

## Analyse RFM — Segmentation Comportementale Rapide

### Principe et Calcul

L'analyse RFM (Recency, Frequency, Monetary) est la methode de segmentation client la plus actionnable immediatement. Elle classe les clients selon trois dimensions comportementales :

- **Recency (R)** : quand a eu lieu la derniere interaction / transaction ? Plus recente = meilleure.
- **Frequency (F)** : combien de fois le client a-t-il interagi ? Plus frequent = meilleur.
- **Monetary (M)** : quelle est la valeur totale des transactions ? Plus eleve = meilleur.

```python
import pandas as pd
import numpy as np
from datetime import datetime

def calculate_rfm(transactions_df, customer_id_col, date_col, amount_col,
                  reference_date=None):
    """
    Calcule le tableau RFM a partir d'un historique de transactions.

    Args:
        transactions_df: DataFrame avec colonnes customer_id, date, amount
        reference_date: Date de reference (par defaut = date maximale + 1 jour)
    """
    if reference_date is None:
        reference_date = transactions_df[date_col].max() + pd.Timedelta(days=1)

    rfm = transactions_df.groupby(customer_id_col).agg({
        date_col: lambda x: (reference_date - x.max()).days,  # Recency en jours
        customer_id_col: 'count',                              # Frequency
        amount_col: 'sum'                                      # Monetary
    }).rename(columns={
        date_col: 'recency',
        customer_id_col: 'frequency',
        amount_col: 'monetary'
    })

    return rfm

# Scoring RFM sur 5 niveaux (1 = moins bon, 5 = meilleur)
def rfm_scoring(rfm_df):
    rfm = rfm_df.copy()

    # Recency : score 5 si recent, 1 si ancien (ordre inverse)
    rfm['r_score'] = pd.qcut(rfm['recency'], q=5,
                              labels=[5, 4, 3, 2, 1])

    # Frequency et Monetary : score 5 si eleve, 1 si faible
    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5,
                              labels=[1, 2, 3, 4, 5])
    rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), q=5,
                              labels=[1, 2, 3, 4, 5])

    # Score RFM concatene (ex: "554" = tres recent, tres frequent, tres monetaire)
    rfm['rfm_score'] = (rfm['r_score'].astype(str) +
                        rfm['f_score'].astype(str) +
                        rfm['m_score'].astype(str))

    # Score RFM numerique (pour trier et comparer)
    rfm['rfm_score_num'] = (rfm['r_score'].astype(int) +
                            rfm['f_score'].astype(int) +
                            rfm['m_score'].astype(int))

    return rfm
```

### Segments RFM Metier Recommandes

| Segment | Criteres | Caracteristiques | Actions metier |
|---|---|---|---|
| **Champions** | R=5, F=5, M=4-5 | Achetent recemment, souvent, tres depensiers | Programme de fidelite premium, early access |
| **Loyal Customers** | F=4-5, R=3-5 | Achetent frequemment, fideles | Programme de points, offres exclusives |
| **Potential Loyalists** | R=4-5, F=2-3 | Recents, pas encore frequents | Encourager la 2e et 3e transaction |
| **New Customers** | R=5, F=1 | Tout juste acquis | Sequence d'onboarding, tutoriels |
| **Promising** | R=4, F=1 | Recents mais un seul achat | Offre de decouverte du catalogue |
| **Need Attention** | R=3, F=3, M=3 | Moyens sur tout, risque de glissement | Rappel de valeur produit |
| **About to Sleep** | R=2-3, F=1-2 | Pas achete depuis un moment | Offre de re-engagement |
| **At Risk** | R=2, F=2-4 | Bons clients dans le passe, distants | Offre de retention personnalisee |
| **Can't Lose Them** | R=1, F=5, M=5 | Tres bons clients mais absents depuis longtemps | Appel direct, offre exceptionnelle |
| **Lost** | R=1, F=1-2 | Anciens clients inactifs | Campagne de reactivation ou abandon |

```python
def segment_rfm(row):
    r, f, m = int(row['r_score']), int(row['f_score']), int(row['m_score'])

    if r >= 4 and f >= 4:
        return 'Champions'
    elif f >= 4:
        return 'Loyal Customers'
    elif r >= 4 and f <= 2:
        return 'New Customers' if f == 1 else 'Potential Loyalists'
    elif r >= 3 and f >= 3:
        return 'Need Attention'
    elif r <= 2 and f >= 4:
        return "Can't Lose Them"
    elif r <= 2 and f >= 2:
        return 'At Risk'
    elif r == 1:
        return 'Lost'
    else:
        return 'About to Sleep'

rfm['segment'] = rfm.apply(segment_rfm, axis=1)
```

---

## K-Means — Clustering Generalist

### Principe et Mise en Oeuvre

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# 1. Preparer les features (normalisation obligatoire pour k-means)
features = rfm[['recency', 'frequency', 'monetary']].copy()
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# 2. Determiner le nombre optimal de clusters
# Methode du coude (Elbow Method)
inertias = []
silhouettes = []
K_range = range(2, 11)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(features_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(features_scaled, km.labels_))

# Visualiser
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot(K_range, inertias, 'bo-')
ax1.set_xlabel('Nombre de clusters (k)')
ax1.set_ylabel('Inertie (within-cluster sum of squares)')
ax1.set_title('Methode du Coude')

ax2.plot(K_range, silhouettes, 'ro-')
ax2.set_xlabel('Nombre de clusters (k)')
ax2.set_ylabel('Silhouette Score')
ax2.set_title('Silhouette Score par k')

plt.tight_layout()
plt.savefig('reports/optimal_k.png')

# 3. Entrainer avec le k optimal (ex: k=5)
optimal_k = 5
km = KMeans(n_clusters=optimal_k, random_state=42, n_init=20, max_iter=300)
km.fit(features_scaled)

# 4. Ajouter les labels au DataFrame original
rfm['cluster'] = km.labels_
```

### Validation de la Qualite du Clustering

```python
# Silhouette Score global (plus proche de 1 = meilleur)
sil_score = silhouette_score(features_scaled, km.labels_)
print(f"Silhouette Score : {sil_score:.3f}")
# > 0.5 : bon clustering
# 0.25-0.5 : clustering acceptable
# < 0.25 : clustering de mauvaise qualite

# Davies-Bouldin Index (plus bas = meilleur, 0 = parfait)
from sklearn.metrics import davies_bouldin_score
db_score = davies_bouldin_score(features_scaled, km.labels_)
print(f"Davies-Bouldin Index : {db_score:.3f}")

# Profile des clusters (toujours sur les donnees originales non normalisees)
cluster_profile = rfm.groupby('cluster').agg({
    'recency': ['mean', 'median'],
    'frequency': ['mean', 'median'],
    'monetary': ['mean', 'median', 'sum'],
    'customer_id': 'count'
}).round(1)
cluster_profile.columns = ['_'.join(col) for col in cluster_profile.columns]
cluster_profile['pct_of_total_revenue'] = (
    cluster_profile['monetary_sum'] / cluster_profile['monetary_sum'].sum() * 100
)
print(cluster_profile)
```

### Interpretation et Nommage des Clusters

L'interpretation des clusters est cruciale et doit se faire en collaboration avec les experts metier. Exemple de processus :

1. **Calculer le profil moyen** de chaque cluster sur toutes les features originales
2. **Identifier les dimensions discriminantes** : quelles features different le plus entre clusters ?
3. **Nommer chaque cluster** avec un nom metier explicite (pas "Cluster 0", "Cluster 1")
4. **Valider avec l'equipe metier** : les clusters correspondent-ils a des archétypes connus ?

```python
# Nommage des clusters base sur le profil
cluster_names = {
    0: "Big Spenders — frequents et tres depensiers",
    1: "Dormants a Fort Potentiel — anciens bons clients",
    2: "Nouveaux Actifs — recents et engages",
    3: "Occasionnels Standards — achats rares, montant moyen",
    4: "Inactifs Anciens — peu depensiers, pas recents"
}
rfm['cluster_name'] = rfm['cluster'].map(cluster_names)
```

---

## Clustering Hierarchique

### Quand Utiliser

Le clustering hierarchique est utile pour :
- Explorer la structure des donnees sans hypothese sur le nombre de clusters
- Visualiser les relations entre groupes (dendrogramme)
- Segmenter avec un nombre modere de points (< 50 000 — au-dela, trop lent)
- Valider les resultats de k-means

```python
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.preprocessing import StandardScaler

# Normaliser
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# Construire la matrice de linkage
# methodes : 'ward' (recommandee), 'complete', 'average', 'single'
Z = linkage(X_scaled, method='ward')

# Visualiser le dendrogramme
plt.figure(figsize=(16, 6))
dendrogram(Z, truncate_mode='lastp', p=30,  # Afficher les 30 derniers merges
           leaf_font_size=10, show_contracted=True)
plt.title('Dendrogramme — Clustering Hierarchique (Ward)')
plt.xlabel('Index ou taille du cluster')
plt.ylabel('Distance (inertie)')
plt.axhline(y=15, color='r', linestyle='--', label='Coupure proposee')
plt.legend()
plt.savefig('reports/dendrogram.png')

# Creer les clusters en coupant le dendrogramme
n_clusters = 5
cluster_labels = fcluster(Z, t=n_clusters, criterion='maxclust')
features['cluster_hc'] = cluster_labels
```

---

## DBSCAN — Clustering par Densite

### Quand Utiliser

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) est ideal pour :
- Detecter des clusters de forme arbitraire (pas forcement sphériques)
- Identifier automatiquement les outliers (points de bruit)
- Quand le nombre de clusters est inconnu a priori et les donnees ont des zones denses separees

```python
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Trouver le parametre epsilon optimal (k-distance plot)
k = 4  # Minimum samples recommande = 2 * nb_dimensions
nbrs = NearestNeighbors(n_neighbors=k).fit(X_scaled)
distances, indices = nbrs.kneighbors(X_scaled)
distances = np.sort(distances[:, k-1])

# Visualiser pour trouver le "coude" = bon epsilon
plt.figure(figsize=(8, 4))
plt.plot(distances)
plt.xlabel('Points tries par distance')
plt.ylabel(f'Distance au {k}e voisin')
plt.title('K-Distance Graph — Trouver Epsilon')
plt.axhline(y=0.5, color='r', linestyle='--', label='Epsilon = 0.5')
plt.legend()
plt.savefig('reports/epsilon_selection.png')

# Appliquer DBSCAN
dbscan = DBSCAN(
    eps=0.5,          # Distance maximale pour considerer deux points voisins
    min_samples=10,   # Nombre minimum de points pour former un cluster dense
    metric='euclidean'
)
labels = dbscan.fit_predict(X_scaled)

# -1 = bruit (outlier), 0, 1, 2... = clusters
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = list(labels).count(-1)
print(f"Clusters detectes : {n_clusters}")
print(f"Points de bruit (outliers) : {n_noise} ({n_noise/len(labels)*100:.1f}%)")
```

---

## Personas Data-Driven

### Definition et Processus

Les personas data-driven combinent les insights quantitatifs des clusters avec la richesse qualitative de la connaissance metier pour creer des archétypes actionnables.

**Processus en 4 etapes** :

**Etape 1 — Clustering** : Identifier les groupes homogenes via k-means, RFM ou une combinaison.

**Etape 2 — Profiling quantitatif** : Pour chaque cluster, calculer :
- Metriques demographiques et firmographiques moyennes
- Comportements cles (frequence, produits preferes, canaux)
- KPIs associes (LTV moyen, taux de churn, NPS moyen)
- Taille du segment et evolution tendancielle

**Etape 3 — Enrichissement qualitatif** : Interviewer 3-5 clients representatifs de chaque cluster pour comprendre :
- Leurs motivations et objectifs
- Leurs frustrations et points de friction
- Leur parcours d'achat typique
- Leur attitude vis-a-vis de la marque

**Etape 4 — Formalisation des personas** : Creer une fiche persona pour chaque segment avec un nom, un portrait visuel, et les informations cles.

### Template de Persona Data-Driven

```
NOM : [Nom fictif representatif]
Segment : [Nom du cluster / segment RFM]

PORTRAIT
---------
Taille du segment : X clients (X% de la base)
LTV moyen : X EUR
Taux de retention a 12 mois : X%
NPS moyen : X

COMPORTEMENT TYPIQUE
---------------------
Frequence d'achat : X fois / mois
Produits preferes : [liste]
Canal d'achat prefere : [liste]
Heure d'achat predominante : [periode]
Sensibilite prix : haute / moyenne / faible

MOTIVATIONS
-----------
[3-5 bullet points bases sur les entretiens qualit]

FRUSTRATIONS
------------
[3-5 points de friction identifies]

ACTIONS MARKETING RECOMMANDEES
--------------------------------
[Actions specifiques pour ce segment]

KPIs de SUIVI
--------------
[Metriques a suivre pour ce segment]
```

---

## Stabilite des Segments dans le Temps

### Mesurer la Stabilite

Un probleme courant avec les segmentations est la migration des clients entre segments au fil du temps. Mesurer cette stabilite est essentiel pour l'activation.

```python
# Calculer la matrice de transition entre deux periodes
def segment_transition_matrix(df_t1, df_t2, customer_id_col, segment_col):
    """
    Calcule la matrice de transition de segmentation entre deux periodes.
    Montre quel pourcentage de clients passe d'un segment a l'autre.
    """
    merge = df_t1[[customer_id_col, segment_col]].rename(
        columns={segment_col: 'segment_t1'}
    ).merge(
        df_t2[[customer_id_col, segment_col]].rename(
            columns={segment_col: 'segment_t2'}
        ),
        on=customer_id_col
    )

    transition = pd.crosstab(
        merge['segment_t1'],
        merge['segment_t2'],
        normalize='index'  # Normaliser par ligne (% de chaque segment T1)
    )

    return transition * 100  # En pourcentage

# Population Stability Index (PSI) pour mesurer le drift de la segmentation
def psi(expected_array, actual_array, buckets=10):
    """
    PSI < 0.1 : pas de changement significatif
    0.1 < PSI < 0.25 : changement modere, surveiller
    PSI > 0.25 : changement majeur, re-segmenter
    """
    expected = np.histogram(expected_array, bins=buckets)[0] / len(expected_array)
    actual = np.histogram(actual_array, bins=buckets)[0] / len(actual_array)

    # Eviter la division par zero
    expected = np.where(expected == 0, 0.0001, expected)
    actual = np.where(actual == 0, 0.0001, actual)

    psi_value = np.sum((actual - expected) * np.log(actual / expected))
    return psi_value
```

### Frequence de Re-segmentation

| Type de segmentation | Frequence recommandee | Trigger supplementaire |
|---|---|---|
| **RFM** | Mensuelle | Changement de politique commerciale |
| **K-means comportemental** | Trimestrielle | PSI > 0.2 sur les features principales |
| **Clustering produit** | Semestrielle | Ajout / retrait de categorie produit |
| **Personas** | Annuelle | Etude qualitative, changement de marche |

---

## Activation des Segments

### Integrer les Segments dans les Outils Metier

```python
# Export des segments pour le CRM / MA
segment_export = rfm[['customer_id', 'segment', 'cluster_name', 'rfm_score_num']].copy()
segment_export['refresh_date'] = datetime.today().strftime('%Y-%m-%d')

# Pour Salesforce : upload via API ou fichier CSV
segment_export.to_csv('exports/customer_segments_for_crm.csv', index=False)

# Pour les outils d'email marketing (Mailchimp, Klaviyo, Brevo)
# Creer des listes / audiences par segment
for segment in segment_export['segment'].unique():
    segment_customers = segment_export[segment_export['segment'] == segment]
    segment_customers.to_csv(f'exports/segment_{segment.replace(" ", "_")}.csv', index=False)
    print(f"Segment '{segment}' : {len(segment_customers)} clients exporte")
```

### Tableau de Bord des Segments

| Metrique | Calcul | Frequence |
|---|---|---|
| **Taille de chaque segment** | Nb clients par segment | Mensuel |
| **Evolution mensuelle** | % d'entrees et sorties par segment | Mensuel |
| **Revenue par segment** | CA total et CA moyen par segment | Mensuel |
| **Taux de conversion par segment** | Conversion d'email / offre par segment | Par campagne |
| **PSI des features de clustering** | Stabilite des features cles | Mensuel |
| **Matrice de transition** | Migration entre segments | Trimestriel |
