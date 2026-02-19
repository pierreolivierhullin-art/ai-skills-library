# Etudes de Cas — Geospatial Analytics en Production

---

## Cas 1 — Retailer : Optimisation de l'implantation de 20 nouveaux magasins

### Contexte

Une chaine de distribution alimentaire (800 magasins en France) souhaitait ouvrir 20 nouveaux points de vente sur 3 ans. La methode historique : etudes de marche manuelles par des consultants, 6 mois par site, 15 000 EUR par dossier. Le management avait une liste intuitive de 35 villes candidates basee sur les remontees terrain.

Objectif de l'equipe data : developper un modele de scoring spatial automatise pour prioriser les zones, reduire le cout d'analyse et augmenter le taux de succes (historiquement 55% des implantations atteignaient les objectifs CA a 3 ans).

### Donnees utilisees

| Source | Description | Format | Actualite |
|---|---|---|---|
| INSEE IRIS | Population, age, CSP, revenus medians par IRIS | Shapefile | 2021 (dernier millésime disponible) |
| INSEE BPE | Base Permanente des Equipements (commerces concurrents) | CSV + geocodage | 2023 |
| OpenStreetMap | Reseau routier, transport en commun, POI | API Overpass | Temps reel |
| DVF (DGFiP) | Transactions immobilieres (prix/m2 locaux commerciaux) | CSV | 2023 |
| Donnees internes | CA, frequentation, zone de chalandise des 800 magasins existants | PostgreSQL | Quotidien |

### Architecture technique

```
PostgreSQL/PostGIS (donnees geospatiales)
     |
Python (GeoPandas + scoring)
     |
Kepler.gl (visualisation direction)
     |
Power BI (reporting mensuel comite)
```

### Algorithme de scoring PostGIS + Python

```python
import geopandas as gpd
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from shapely.strtree import STRtree

engine = create_engine("postgresql+psycopg2://user:pw@db/retail")

# 1. Charger les IRIS avec indicateurs sociodemographiques
iris = gpd.read_postgis("""
    SELECT
        i.code_iris,
        i.nom_iris,
        i.geometry,
        s.population,
        s.pop_15_64,          -- Population active
        s.revenu_median,
        s.taux_proprietaires,
        s.nb_menages,
        s.taille_moy_menage
    FROM iris_geom i
    JOIN iris_stats s ON i.code_iris = s.code_iris
    WHERE s.population > 500   -- Exclure les IRIS industriels ou vides
""", engine, geom_col='geometry')

iris = iris.to_crs("EPSG:2154")
iris['centroide'] = iris.geometry.centroid

# 2. Charger les concurrents depuis la BPE + OSM
concurrents = gpd.read_postgis("""
    SELECT id, nom, categorie, geom
    FROM commerces_concurrents
    WHERE categorie IN ('supermarche', 'hypermarche', 'hard_discount', 'superette')
""", engine, geom_col='geom').to_crs("EPSG:2154")

# 3. Charger les magasins existants (zones d'exclusion : cannibalisation)
propres = gpd.read_postgis("""
    SELECT id, nom, zone_chalandise_geom AS geom
    FROM magasins_reseau
""", engine, geom_col='geom').to_crs("EPSG:2154")

# 4. Calcul des indicateurs par IRIS

# 4a. Densite concurrentielle dans un rayon de 2 km
tree_concurrents = STRtree(concurrents.geometry.tolist())
iris['nb_concurrents_2km'] = iris['centroide'].apply(
    lambda g: len(tree_concurrents.query(g.buffer(2000)))
)

# 4b. Ponderation par surface de vente (hypermarche = poids 3, superette = poids 0.5)
def score_concurrentiel(centroide):
    candidates_idx = tree_concurrents.query(centroide.buffer(2000))
    if not candidates_idx:
        return 0
    candidates = concurrents.iloc[candidates_idx].copy()
    candidates['dist'] = candidates.geometry.distance(centroide)
    # Decroissance avec la distance
    candidates['poids_dist'] = 1 / (1 + candidates['dist'] / 500)
    poids_type = {'hypermarche': 3.0, 'supermarche': 2.0,
                  'hard_discount': 1.5, 'superette': 0.5}
    candidates['poids_type'] = candidates['categorie'].map(poids_type).fillna(1.0)
    return (candidates['poids_dist'] * candidates['poids_type']).sum()

iris['pression_concurrentielle'] = iris['centroide'].apply(score_concurrentiel)

# 4c. Verifier si l'IRIS est dans une zone de chalandise existante (cannibalisation)
tree_propres = STRtree(propres.geometry.tolist())
iris['dans_zone_existante'] = iris['centroide'].apply(
    lambda g: len(tree_propres.query(g)) > 0
)

# 4d. Estimation du CA potentiel (modele base sur les 800 magasins existants)
# CA = f(population, revenu, pression_concurrentielle)
# Coefficients calibres sur le portefeuille existant via regression
COEF_POP = 42.5           # EUR par habitant dans le rayon
COEF_REVENU = 0.008       # Elasticite revenu
COEF_CONCURRENCE = -18000 # Malus par point de pression concurrentielle

iris['ca_potentiel_estime'] = (
    iris['population'] * COEF_POP
    + iris['revenu_median'] * COEF_REVENU * iris['population']
    - iris['pression_concurrentielle'] * COEF_CONCURRENCE
).clip(lower=0)

# 5. Score composite normalise
def normalize(series):
    return (series - series.min()) / (series.max() - series.min() + 1e-9)

iris['score_population']   = normalize(iris['population'])
iris['score_revenu']        = normalize(iris['revenu_median'])
iris['score_concurrence']   = 1 - normalize(iris['pression_concurrentielle'])
iris['score_ca']            = normalize(iris['ca_potentiel_estime'])

POIDS = {
    'score_population': 0.25,
    'score_revenu': 0.20,
    'score_concurrence': 0.30,
    'score_ca': 0.25
}

iris['score_final'] = sum(iris[col] * poids for col, poids in POIDS.items())

# Exclure les zones deja couvertes et filtrer le top 50 pour analyse approfondie
candidats = iris[~iris['dans_zone_existante']].nlargest(50, 'score_final')
print(candidats[['code_iris', 'nom_iris', 'score_final', 'ca_potentiel_estime',
                  'pression_concurrentielle']].head(20))
```

### Carte de chaleur du potentiel

```python
from keplergl import KeplerGl

map_scoring = KeplerGl(height=700)
map_scoring.add_data(data=iris.to_crs("EPSG:4326"), name="Scoring IRIS")
map_scoring.add_data(data=candidats.to_crs("EPSG:4326"), name="Top 50 candidats")
map_scoring.add_data(data=concurrents.to_crs("EPSG:4326"), name="Concurrents")
map_scoring.save_to_html("scoring_implantation.html")
```

### Resultats et ROI

La direction a retenu 20 sites sur les 50 proposes par le modele (les 3 premiers de chaque region), en comparant avec leurs 35 sites intuitifs initiaux.

- **Overlap modele/intuition** : 12 sites en commun
- **8 sites proposes uniquement par le modele** (nouveaux pour la direction)
- **23 sites proposes uniquement par intuition** : scores mediocres, ecarte par le modele

Apres 18 mois :
- 14 des 20 magasins ouverts atteignent leurs objectifs CA (70% vs 55% historique)
- Les 2 sites "modele only" les plus performants : +12% et +18% vs budget
- Cout analyse reduit de 300 000 EUR (20 sites x 15k) a 45 000 EUR (1 mois data engineer)
- **ROI direct : 6x le cout du projet sur la seule reduction des couts d'etude**

### Lecon

Le modele n'elimine pas le jugement humain : l'equipe terrain a identifie 2 contraintes que les donnees ne capturent pas (projet immobilier bloquant, litige foncier). L'approche optimale combine scoring objectif pour prioriser + validation terrain ciiblee sur les finalistes uniquement.

---

## Cas 2 — Logistique : Zones de livraison optimales pour une startup last-mile

### Contexte

Startup de livraison urbaine a Paris (B2B alimentaire), 45 livreurs a velo, 800 adresses clientes actives. Probleme : les zones de livraison assignees historiquement par le cofondateur etaient mal equilibrees. Certains livreurs parcouraient 35 km/jour, d'autres 18 km. Les retards touchaient 22% des livraisons. Objectif : recalibrer les zones pour equilibrer la charge et minimiser les km totaux.

### Donnees

- Adresses clientes geocodees (PostGIS, 800 points WGS84)
- Historique de livraisons (12 mois, 150 000 lignes) : heure, livreur, duree, adresse
- Reseau routier Paris + petite couronne (OSMnx)
- Contraintes operationnelles : chaque livreur doit couvrir sa zone en 6h max

### Approche technique : DBSCAN + Isochrones

```python
import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import openrouteservice
import folium
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://user:pw@db/livraison")

# 1. Charger les adresses clientes
clients = gpd.read_postgis(
    "SELECT id, nom, adresse, geom FROM clients WHERE statut = 'actif'",
    engine, geom_col='geom'
).to_crs("EPSG:2154")

coords = np.array([[g.x, g.y] for g in clients.geometry])

# 2. Clustering DBSCAN sur les coordonnees projetees
# eps en metres : 300m = rayon typique d'un cluster dense Paris
# min_samples : minimum 5 adresses pour constituer un cluster
db = DBSCAN(eps=300, min_samples=5, metric='euclidean', n_jobs=-1)
clients['cluster_id'] = db.fit_predict(coords)

print(f"Clusters trouves: {clients['cluster_id'].nunique() - 1}")  # -1 pour le bruit
print(f"Points bruit (cluster=-1): {(clients['cluster_id'] == -1).sum()}")

# Statistiques par cluster
cluster_stats = clients.groupby('cluster_id').agg(
    nb_adresses=('id', 'count'),
    centroide_x=('geometry', lambda g: g.centroid.x.mean()),
    centroide_y=('geometry', lambda g: g.centroid.y.mean())
).reset_index()
cluster_stats = cluster_stats[cluster_stats['cluster_id'] >= 0]  # Exclure bruit

print(cluster_stats.sort_values('nb_adresses', ascending=False).head(10))

# 3. Regrouper les clusters par zone livreur (target : 45 zones equilibrees)
# Utiliser K-Means sur les centroides de clusters pour creer 45 macro-zones
from sklearn.cluster import KMeans

centroides = cluster_stats[['centroide_x', 'centroide_y']].values
kmeans = KMeans(n_clusters=45, random_state=42, n_init=10)
cluster_stats['zone_livreur'] = kmeans.fit_predict(centroides)

# Propager les zones aux adresses
clients = clients.merge(
    cluster_stats[['cluster_id', 'zone_livreur']],
    on='cluster_id', how='left'
)
# Les points bruit : assigner a la zone la plus proche
bruit_mask = clients['cluster_id'] == -1
if bruit_mask.any():
    from scipy.spatial import cKDTree
    zone_coords = np.array(kmeans.cluster_centers_)
    tree = cKDTree(zone_coords)
    _, idx = tree.query(coords[bruit_mask])
    clients.loc[bruit_mask, 'zone_livreur'] = idx

# 4. Calcul des isochrones par zone (centre de gravite de chaque zone)
ors_client = openrouteservice.Client(key="YOUR_ORS_KEY")

zones_gdf = clients.groupby('zone_livreur').apply(
    lambda g: pd.Series({
        'nb_adresses': len(g),
        'centroide': g.to_crs("EPSG:4326").geometry.unary_union.centroid
    })
).reset_index()

def get_isochrone_zone(row, minutes=180):
    """Calcule l'isochrone de 3h depuis le centroide de la zone."""
    try:
        coords = [[row['centroide'].x, row['centroide'].y]]
        iso = openrouteservice.isochrones.isochrones(
            ors_client, locations=coords,
            profile='cycling-regular',
            range=[minutes * 60],
            range_type='time'
        )
        return iso['features'][0]['geometry']
    except Exception as e:
        print(f"Erreur zone {row['zone_livreur']}: {e}")
        return None

import time
zones_gdf['isochrone_geom'] = zones_gdf.apply(
    lambda r: (time.sleep(1.2), get_isochrone_zone(r))[1], axis=1
)

# 5. Verification : toutes les adresses sont-elles dans leur isochrone?
zones_gdf_geo = gpd.GeoDataFrame(
    zones_gdf,
    geometry=zones_gdf['isochrone_geom'].apply(
        lambda g: __import__('shapely').geometry.shape(g) if g else None
    ),
    crs="EPSG:4326"
)

clients_wgs = clients.to_crs("EPSG:4326")
clients_wgs = clients_wgs.merge(zones_gdf_geo[['zone_livreur', 'geometry']],
                                 on='zone_livreur', suffixes=('', '_zone'))
clients_wgs['dans_isochrone'] = clients_wgs.apply(
    lambda r: r['geometry_zone'].contains(r['geometry']) if r['geometry_zone'] else False,
    axis=1
)
print(f"Adresses dans isochrone: {clients_wgs['dans_isochrone'].mean():.1%}")
```

### Resultats apres 3 mois de deploiement

| Metrique | Avant | Apres | Evolution |
|---|---|---|---|
| Distance moyenne/livreur/jour | 27.4 km | 19.7 km | -28.1% |
| Ecart-type des distances | 6.2 km | 1.8 km | -71% (meilleur equilibre) |
| Taux de livraisons en retard | 22% | 11% | -50% |
| Satisfaction livreurs (NPS interne) | 31 | 58 | +87% |
| Couts carburant + maintenance | 8 400 EUR/mois | 6 050 EUR/mois | -28% |

### Lecon

DBSCAN surpasse K-Means pur pour ce cas car il identifie naturellement les zones denses sans forcer un nombre de clusters predetermine. Le parametre `eps` (rayon) doit etre calibre sur la realite terrain : 300m convient a Paris dense, augmenter a 800m pour les banlieues moins denses. Integrer les contraintes operationnelles (capacite par livreur, horaires) comme contraintes post-clustering plutot que dans le clustering lui-meme.

---

## Cas 3 — Fraude Geographique : Detection en Temps Reel pour une Neobanque

### Contexte

Neobanque europeenne (1,2 million de clients, 8 millions de transactions/mois). L'equipe fraude avait identifie un pattern : des paires de transactions apparemment legitimes, mais geographiquement impossibles (transaction A a Paris, transaction B a Toronto, 7 minutes d'ecart). Le systeme de scoring existant ne capturait pas cet indicateur. Objectif : detecter les transactions "impossible travel" en quasi temps reel et les envoyer au scoring de fraude.

### Pipeline PostGIS temps reel

```sql
-- 1. Table des transactions enrichie avec geometrie
CREATE TABLE transactions (
    id BIGSERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    montant DECIMAL(12,2),
    devise TEXT,
    commercant_id INTEGER,
    geom GEOGRAPHY(POINT, 4326),  -- Position GPS de la transaction
    ip_geom GEOGRAPHY(POINT, 4326), -- Position estimee depuis IP
    created_at TIMESTAMPTZ DEFAULT NOW(),
    statut TEXT DEFAULT 'pending',  -- pending, validated, fraud_suspected
    score_fraude FLOAT
);

CREATE INDEX idx_transactions_client_time ON transactions (client_id, created_at DESC);
CREATE INDEX idx_transactions_geom ON transactions USING GIST (geom);
CREATE INDEX idx_transactions_statut ON transactions (statut) WHERE statut = 'pending';

-- 2. Fonction de detection "impossible travel"
CREATE OR REPLACE FUNCTION detect_impossible_travel(
    p_client_id INTEGER,
    p_transaction_id BIGINT,
    p_geom GEOGRAPHY,
    p_created_at TIMESTAMPTZ,
    p_vitesse_max_kmh FLOAT DEFAULT 900  -- Avion commercial = 900 km/h
)
RETURNS TABLE(
    transaction_precedente_id BIGINT,
    distance_km FLOAT,
    duree_minutes FLOAT,
    vitesse_necessaire_kmh FLOAT,
    est_impossible BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.id AS transaction_precedente_id,
        ST_Distance(p_geom, t.geom) / 1000 AS distance_km,
        EXTRACT(EPOCH FROM (p_created_at - t.created_at)) / 60 AS duree_minutes,
        (ST_Distance(p_geom, t.geom) / 1000)
            / NULLIF(EXTRACT(EPOCH FROM (p_created_at - t.created_at)) / 3600, 0)
            AS vitesse_necessaire_kmh,
        (ST_Distance(p_geom, t.geom) / 1000)
            / NULLIF(EXTRACT(EPOCH FROM (p_created_at - t.created_at)) / 3600, 0)
            > p_vitesse_max_kmh AS est_impossible
    FROM transactions t
    WHERE t.client_id = p_client_id
      AND t.id != p_transaction_id
      AND t.created_at BETWEEN p_created_at - INTERVAL '2 hours'
                            AND p_created_at
      AND t.statut != 'fraud_confirmed'
      AND t.geom IS NOT NULL
    ORDER BY t.created_at DESC
    LIMIT 5;
END;
$$ LANGUAGE plpgsql;

-- 3. Trigger sur INSERT de transaction
CREATE OR REPLACE FUNCTION trigger_fraud_check()
RETURNS TRIGGER AS $$
DECLARE
    v_impossible BOOLEAN;
    v_max_vitesse FLOAT;
    v_result RECORD;
BEGIN
    -- Verifier "impossible travel" vs les 2 dernieres heures
    SELECT est_impossible, vitesse_necessaire_kmh
    INTO v_impossible, v_max_vitesse
    FROM detect_impossible_travel(
        NEW.client_id,
        NEW.id,
        NEW.geom,
        NEW.created_at
    )
    WHERE est_impossible = TRUE
    LIMIT 1;

    IF v_impossible THEN
        -- Mettre a jour le statut et le score
        NEW.statut := 'fraud_suspected';
        NEW.score_fraude := LEAST(1.0, 0.5 + v_max_vitesse / 10000.0);

        -- Inserer dans la table d'alertes
        INSERT INTO fraud_alerts (
            transaction_id, client_id, alert_type,
            details, created_at
        ) VALUES (
            NEW.id, NEW.client_id, 'impossible_travel',
            json_build_object(
                'vitesse_km_h', v_max_vitesse,
                'seuil_km_h', 900
            ),
            NOW()
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_fraud_on_insert
    BEFORE INSERT ON transactions
    FOR EACH ROW EXECUTE FUNCTION trigger_fraud_check();
```

### Window functions pour analyse en batch

```sql
-- Analyse batch journaliere : detecter les patterns impossibles non catches en temps reel
WITH transactions_avec_precedente AS (
    SELECT
        t1.id,
        t1.client_id,
        t1.montant,
        t1.geom,
        t1.created_at,
        t2.id AS id_precedente,
        t2.geom AS geom_precedente,
        t2.created_at AS created_at_precedente,
        ST_Distance(t1.geom, t2.geom) / 1000 AS distance_km,
        EXTRACT(EPOCH FROM (t1.created_at - t2.created_at)) / 60 AS duree_minutes
    FROM transactions t1
    JOIN LATERAL (
        SELECT id, geom, created_at
        FROM transactions t2
        WHERE t2.client_id = t1.client_id
          AND t2.created_at < t1.created_at
          AND t2.created_at > t1.created_at - INTERVAL '4 hours'
          AND t2.geom IS NOT NULL
        ORDER BY t2.created_at DESC
        LIMIT 1
    ) t2 ON TRUE
    WHERE t1.created_at >= NOW() - INTERVAL '24 hours'
      AND t1.geom IS NOT NULL
)
SELECT
    id,
    client_id,
    distance_km,
    duree_minutes,
    ROUND((distance_km / NULLIF(duree_minutes / 60.0, 0))::NUMERIC, 0) AS vitesse_kmh,
    CASE
        WHEN distance_km / NULLIF(duree_minutes / 60.0, 0) > 900 THEN 'IMPOSSIBLE'
        WHEN distance_km / NULLIF(duree_minutes / 60.0, 0) > 200 THEN 'SUSPECT'
        ELSE 'OK'
    END AS verdict
FROM transactions_avec_precedente
WHERE distance_km > 50   -- Ignorer les micro-deplacements
ORDER BY vitesse_kmh DESC NULLS LAST;
```

### Integration API scoring

```python
import psycopg2
import requests
from datetime import datetime

def enrich_fraud_score(transaction_id: int) -> dict:
    """
    Recupere les indicateurs de fraud geo et les envoie
    a l'API de scoring fraude centralisee.
    """
    conn = psycopg2.connect("postgresql://user:pw@db/banking")
    cur = conn.cursor()

    cur.execute("""
        SELECT
            fa.transaction_id,
            fa.client_id,
            fa.details->>'vitesse_km_h' AS vitesse,
            fa.details->>'distance_km' AS distance,
            t.montant,
            t.devise,
            ST_AsGeoJSON(t.geom)::json AS position
        FROM fraud_alerts fa
        JOIN transactions t ON t.id = fa.transaction_id
        WHERE fa.transaction_id = %s
    """, (transaction_id,))

    row = cur.fetchone()
    if not row:
        return {"status": "not_found"}

    payload = {
        "transaction_id": row[0],
        "client_id": row[1],
        "indicators": {
            "impossible_travel": True,
            "vitesse_necessaire_kmh": float(row[2] or 0),
            "distance_km": float(row[3] or 0)
        },
        "transaction": {
            "montant": float(row[4]),
            "devise": row[5],
            "position": row[6]
        }
    }

    response = requests.post(
        "https://scoring.internal/api/v2/fraud/evaluate",
        json=payload,
        headers={"Authorization": "Bearer INTERNAL_API_TOKEN"},
        timeout=2.0
    )
    return response.json()
```

### Resultats en production

- **340 fraudes detectees/mois supplementaires** (vs 0 avant le systeme geo)
- Faux positifs : 4.2% (un client en avion avec carte etrangere)
- Montant moyen fraude detectee : 847 EUR (fraudes a valeur elevee ciblees)
- Latence trigger PostgreSQL : 1.8 ms en moyenne (acceptable pour le temps reel)
- Reduction des pertes fraude : 288 000 EUR/mois (340 x 847)

### Lecon

Le seuil de 900 km/h (vitesse avion) genere trop de faux positifs pour les clients frequemment en voyage d'affaires. L'amelioration suivante : croiser avec le profil client (voyageur frequents identifie par historique IRIS code pays de transaction) et ajuster le seuil dynamiquement. La whitelist des clients "globetrotters" reduit les faux positifs de 4.2% a 1.1%.

---

## Cas 4 — Analyse Sectorielle Immobilier : Modele de Prix au m2 pour une PropTech

### Contexte

Startup PropTech developpant un outil d'aide a la decision pour les agents immobiliers. L'estimation des prix reposait sur une regression lineaire simple (surface, pieces, etage) avec une precision de R2 = 0.61. L'hypothese : integrer les donnees spatiales du voisinage (POI, transports, bruit, revenus IRIS) ameliorerait significativement le modele.

### Donnees utilisees

| Source | Variables extraites | Methode d'integration |
|---|---|---|
| DVF (DGFiP) | Prix de vente, surface, nb pieces, date | CSV via data.gouv.fr, geocodage |
| OpenStreetMap | Commerces, ecoles, transports (points d'interet) | OSMnx, distance au plus proche |
| INSEE IRIS | Revenu median, taux chomage, taux proprietaires | Jointure spatiale (ST_Within) |
| BRUITPARIF | Niveau sonore Lden (bruit total jour-soir-nuit) | Raster, rasterstats zonal mean |
| RATP/IDFM | Acces stations Metro, RER, Bus | GTFS, calcul distance reseau pedestre |

### Pipeline de construction du dataset

```python
import geopandas as gpd
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from shapely.strtree import STRtree
import osmnx as ox
import rasterio
from rasterstats import zonal_stats

engine = create_engine("postgresql+psycopg2://user:pw@db/proptech")

# 1. Charger les transactions DVF Paris (2019-2023)
dvf = gpd.read_postgis("""
    SELECT
        id_mutation,
        valeur_fonciere / surface_reelle_bati AS prix_m2,
        surface_reelle_bati,
        nombre_pieces_principales,
        code_type_local,
        date_mutation,
        geom
    FROM dvf_transactions
    WHERE code_type_local IN ('Appartement', 'Maison')
      AND surface_reelle_bati BETWEEN 15 AND 500
      AND valeur_fonciere / surface_reelle_bati BETWEEN 2000 AND 30000
      AND code_commune LIKE '75%'  -- Paris intramuros
""", engine, geom_col='geom').to_crs("EPSG:2154")

print(f"Transactions: {len(dvf)}, Prix median: {dvf['prix_m2'].median():.0f} EUR/m2")

# 2. Variables IRIS (jointure spatiale)
iris = gpd.read_postgis("""
    SELECT code_iris, revenu_median, taux_chomage, taux_proprio, geometry
    FROM iris_paris
""", engine, geom_col='geometry').to_crs("EPSG:2154")

dvf = dvf.sjoin(iris[['code_iris', 'revenu_median', 'taux_chomage',
                        'taux_proprio', 'geometry']],
                how='left', predicate='within')

# 3. POI OpenStreetMap : distance aux amenities cles
tags_amenities = {
    "amenity": ["school", "university", "hospital", "supermarket"],
    "shop": ["supermarket", "mall"],
    "public_transport": ["station"],
    "railway": ["metro_station", "station"]
}

poi = ox.features_from_place("Paris, France", tags=tags_amenities)
poi = poi[poi.geometry.geom_type == 'Point'].to_crs("EPSG:2154")

# Separer par categorie et calculer la distance au plus proche pour chaque transaction
def dist_nearest(source_gdf, target_gdf, colname):
    tree = STRtree(target_gdf.geometry.tolist())
    dists = []
    for geom in source_gdf.geometry:
        idx = tree.nearest(geom)
        dists.append(geom.distance(target_gdf.geometry.iloc[idx]))
    return pd.Series(dists, index=source_gdf.index, name=colname)

metro_stations = poi[poi.get('railway', '').isin(['metro_station', 'station'])]
ecoles = poi[poi.get('amenity', '').isin(['school', 'university'])]
supermarches = poi[poi.get('amenity', '') == 'supermarket']

dvf['dist_metro_m']       = dist_nearest(dvf, metro_stations, 'dist_metro_m')
dvf['dist_ecole_m']       = dist_nearest(dvf, ecoles, 'dist_ecole_m')
dvf['dist_supermarche_m'] = dist_nearest(dvf, supermarches, 'dist_supermarche_m')

# Nombre de commerces dans un rayon de 300m
tree_commerces = STRtree(supermarches.geometry.tolist())
dvf['nb_commerces_300m'] = dvf.geometry.apply(
    lambda g: len(tree_commerces.query(g.buffer(300)))
)

# 4. Bruit BRUITPARIF (raster)
dvf_wgs = dvf.to_crs("EPSG:4326")
dvf_wgs['geometry_buffer'] = dvf_wgs.geometry.buffer(0.0001)  # ~10m en WGS84

bruit_stats = zonal_stats(
    dvf_wgs.set_geometry('geometry_buffer'),
    "bruitparif_lden_paris.tif",
    stats=['mean'],
    nodata=-9999
)
dvf['bruit_lden_db'] = [s['mean'] if s['mean'] else np.nan for s in bruit_stats]
dvf['bruit_lden_db'].fillna(dvf['bruit_lden_db'].median(), inplace=True)

# 5. Feature engineering
dvf['annee'] = pd.to_datetime(dvf['date_mutation']).dt.year
dvf['log_surface'] = np.log(dvf['surface_reelle_bati'])
dvf['log_dist_metro'] = np.log1p(dvf['dist_metro_m'])
dvf['log_dist_ecole'] = np.log1p(dvf['dist_ecole_m'])
dvf['score_accessibilite'] = (
    -0.4 * dvf['log_dist_metro']
    -0.3 * dvf['log_dist_ecole']
    +0.3 * dvf['nb_commerces_300m'].clip(0, 20) / 20
)

print(dvf[['prix_m2', 'dist_metro_m', 'bruit_lden_db', 'revenu_median']].describe())
```

### Modele de regression spatiale

```python
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import cross_val_score, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import shap

FEATURES = [
    # Transaction
    'log_surface', 'nombre_pieces_principales', 'annee',
    # Accessibilite
    'log_dist_metro', 'log_dist_ecole', 'log1p(dist_supermarche_m)',
    'nb_commerces_300m',
    # Environnement
    'bruit_lden_db',
    # Sociodemographie IRIS
    'revenu_median', 'taux_chomage', 'taux_proprio'
]

# Nettoyage
dvf_clean = dvf[FEATURES + ['prix_m2']].dropna()
X = dvf_clean[FEATURES]
y = np.log(dvf_clean['prix_m2'])  # Log-transformation pour normaliser la distribution

# Gradient Boosting (meilleur sur ce type de donnees)
model = GradientBoostingRegressor(
    n_estimators=500,
    max_depth=5,
    learning_rate=0.05,
    min_samples_leaf=10,
    subsample=0.8,
    random_state=42
)

cv = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring='r2')
print(f"R2 moyen: {scores.mean():.3f} (+/- {scores.std()*2:.3f})")

model.fit(X, y)

# MAE en EUR/m2
dvf_clean['prix_predit'] = np.exp(model.predict(X))
mae = mean_absolute_error(dvf_clean['prix_m2'], dvf_clean['prix_predit'])
print(f"MAE: {mae:.0f} EUR/m2 (soit {mae/dvf_clean['prix_m2'].mean()*100:.1f}%)")

# Importance des variables avec SHAP
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)
shap.summary_plot(shap_values, X, show=False)
# Les variables spatiales (dist_metro, revenu_median, bruit) contribuent ~45% du R2
```

### Carte interactive Kepler.gl pour les commerciaux

```python
from keplergl import KeplerGl
import geopandas as gpd

# Preparer les donnees pour Kepler
dvf_kepler = dvf_clean.copy()
dvf_kepler['latitude'] = dvf.geometry.to_crs("EPSG:4326").y
dvf_kepler['longitude'] = dvf.geometry.to_crs("EPSG:4326").x
dvf_kepler['prix_predit'] = dvf_clean['prix_predit']
dvf_kepler['ecart_marche_pct'] = (
    (dvf_clean['prix_m2'] - dvf_clean['prix_predit'])
    / dvf_clean['prix_predit'] * 100
).round(1)

map_proptech = KeplerGl(height=700, config={
    "version": "v1",
    "config": {
        "visState": {
            "layers": [{
                "type": "heatmap",
                "config": {
                    "dataId": "Transactions DVF",
                    "columns": {"lat": "latitude", "lng": "longitude"},
                    "visConfig": {
                        "radius": 25,
                        "colorRange": {
                            "colors": ["#313695", "#4575b4", "#abd9e9",
                                       "#fee090", "#f46d43", "#a50026"]
                        }
                    }
                }
            }]
        },
        "mapStyle": {"styleType": "light"}
    }
})

map_proptech.add_data(data=dvf_kepler[['latitude', 'longitude', 'prix_m2',
                                        'prix_predit', 'ecart_marche_pct',
                                        'dist_metro_m', 'bruit_lden_db',
                                        'revenu_median']],
                       name="Transactions DVF")
map_proptech.save_to_html("prix_m2_paris_interactif.html")
```

### Resultats et impact metier

| Metrique | Modele classique | Modele spatial | Amelioration |
|---|---|---|---|
| R2 (cross-validation) | 0.61 | 0.82 | +34% |
| MAE (EUR/m2) | 1 240 EUR | 810 EUR | -35% |
| MAPE (%) | 14.2% | 8.8% | -38% |
| Variables importantes (SHAP top 3) | Surface, pieces, etage | Dist. metro, revenu IRIS, bruit | - |

La carte interactive est deployee pour 120 agents commerciaux. L'indicateur "ecart au marche" (prix demande vs prix predit modele) est integre dans le CRM : les biens sous-evalues de plus de 10% sont automatiquement signales comme "opportunites".

### Lecon

Le bruit (BRUITPARIF) est la variable la plus surprenante : chaque decibel supplementaire reduit le prix de 0.8% en moyenne a Paris, avec des effets non-lineaires au dela de 65 dB. La variable la plus importante reste la distance au metro (station de moins de 300m : +7% en moyenne). Le modele spatial surpasse systematiquement la regression classique sur toutes les zones de Paris, mais les gains sont plus importants dans les arrondissements mixtes (10e, 11e, 19e, 20e) ou les indicateurs de voisinage varient fortement sur de courtes distances.
