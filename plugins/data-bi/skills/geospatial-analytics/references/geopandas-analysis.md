# GeoPandas — Analyse Spatiale Python

## Installation et environnement

```bash
# Installation recommandee via conda (evite les conflits GDAL)
conda create -n geo python=3.11
conda activate geo
conda install -c conda-forge geopandas fiona shapely pyproj rtree
conda install -c conda-forge osmnx networkx openrouteservice geopy
pip install h3 rasterio rasterstats sqlalchemy geoalchemy2 psycopg2-binary

# Ou via pip avec GDAL preinstalle
pip install geopandas[all]
```

---

## Chargement de donnees geospatiales

### GeoJSON et Shapefile

```python
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

# GeoJSON local ou URL
communes = gpd.read_file("communes.geojson")
communes_url = gpd.read_file(
    "https://data.geopf.fr/telechargement/download/LIMITES_ADMINISTRATIVES_EXPRESS/"
    "LIMITES_ADMINISTRATIVES_EXPRESS_PACK_2024-01-01/"
    "LIMITES_ADMINISTRATIVES_EXPRESS_PACK_2024-01-01.7z"
)

# Shapefile (dossier contenant .shp, .dbf, .shx, .prj)
iris = gpd.read_file("CONTOURS-IRIS_2-1.shp")

# Verification basique
print(f"CRS: {communes.crs}")          # EPSG:4326 ou EPSG:2154
print(f"Colonnes: {communes.columns.tolist()}")
print(f"Nb lignes: {len(communes)}")
print(communes.geometry.geom_type.value_counts())
```

### Chargement depuis WKT et creation de GeoDataFrame

```python
# Depuis un DataFrame pandas avec colonnes WKT
df = pd.read_csv("magasins.csv")
# Colonne 'wkt_geometry' contient "POINT(2.3522 48.8566)"

from shapely import wkt
df['geometry'] = df['wkt_geometry'].apply(wkt.loads)
gdf = gpd.GeoDataFrame(df, geometry='geometry', crs='EPSG:4326')

# Depuis colonnes lat/lon
df = pd.read_csv("clients.csv")
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['longitude'], df['latitude']),
    crs='EPSG:4326'
)
```

### Connexion PostGIS via SQLAlchemy + GeoAlchemy2

```python
from sqlalchemy import create_engine, text
import geopandas as gpd

engine = create_engine(
    "postgresql+psycopg2://user:password@localhost:5432/geodatabase"
)

# Charger depuis PostGIS (respecte les types geometriques)
gdf = gpd.read_postgis(
    "SELECT id, nom, categorie, geom FROM commerces WHERE actif = true",
    con=engine,
    geom_col='geom',
    crs='EPSG:4326'
)

# Ecrire dans PostGIS
gdf.to_postgis(
    name='zones_livraison',
    con=engine,
    if_exists='replace',
    index=False,
    dtype={'geom': 'geometry'}
)
```

### API geo.gouv.fr (donnees officielles France)

```python
import requests
import geopandas as gpd

def get_communes_departement(code_dept: str) -> gpd.GeoDataFrame:
    """Recupere les communes d'un departement via l'API geo.gouv.fr."""
    url = f"https://geo.api.gouv.fr/departements/{code_dept}/communes"
    params = {"format": "geojson", "geometry": "mairie"}
    r = requests.get(url, params=params)
    r.raise_for_status()
    gdf = gpd.GeoDataFrame.from_features(r.json()["features"], crs="EPSG:4326")
    return gdf

# Usage
communes_75 = get_communes_departement("75")
communes_idf = pd.concat([
    get_communes_departement(d) for d in ["75", "77", "78", "91", "92", "93", "94", "95"]
])
```

---

## Operations de base

### Changement de projection

```python
# Toujours verifier et harmoniser les CRS avant toute operation
print(gdf.crs)  # EPSG:4326 (WGS84, degres)

# Projeter en Lambert 93 pour les calculs en metres (France)
gdf_l93 = gdf.to_crs("EPSG:2154")

# Verifier que deux GeoDataFrames ont le meme CRS avant jointure
assert gdf1.crs == gdf2.crs, "CRS differents !"
gdf2 = gdf2.to_crs(gdf1.crs)
```

### Buffer

```python
# Buffer en metres (necessite une projection metrique)
gdf_l93 = magasins.to_crs("EPSG:2154")
zones_500m = gdf_l93.copy()
zones_500m['geometry'] = gdf_l93.geometry.buffer(500)  # 500 metres

# Reprojeter en WGS84 pour affichage/sauvegarde
zones_500m = zones_500m.to_crs("EPSG:4326")

# Buffer avec differentes valeurs selon une colonne
zones = magasins_l93.copy()
zones['geometry'] = magasins_l93.apply(
    lambda row: row.geometry.buffer(row['rayon_zone']),
    axis=1
)
```

### Dissolve par attribut

```python
# Fusionner les communes par departement (equivalent ST_Union groupee)
departements = communes.dissolve(by='code_dept', aggfunc={
    'population': 'sum',
    'superficie': 'sum',
    'nom_commune': 'count'
}).rename(columns={'nom_commune': 'nb_communes'})

# Dissolve sans attribut : tout fusionner en une seule geometrie
france = communes.dissolve()
```

### Simplify pour performance de visualisation

```python
# Douglas-Peucker : tolerance en unites du CRS
# Pour EPSG:2154 (metres) : 100m = simplification legere, 1000m = forte
communes_simple = communes.copy()
communes_simple['geometry'] = communes.geometry.simplify(
    tolerance=100,
    preserve_topology=True  # Evite les trous et auto-intersections
)

print(f"Points avant: {communes.geometry.apply(lambda g: len(g.exterior.coords)).sum()}")
print(f"Points apres: {communes_simple.geometry.apply(lambda g: len(g.exterior.coords)).sum()}")

# Pour GeoJSON web : EPSG:4326 avec tolerance 0.001 degres (~100m)
communes_web = communes.to_crs("EPSG:4326")
communes_web['geometry'] = communes_web.geometry.simplify(0.001, preserve_topology=True)
```

### Convex Hull

```python
# Enveloppe convexe de chaque geometrie
magasins['convex_hull'] = magasins.geometry.convex_hull

# Enveloppe convexe de l'ensemble des points d'une categorie
from shapely.ops import unary_union
hull_supermarches = unary_union(
    magasins[magasins['categorie'] == 'supermarche'].geometry
).convex_hull
```

---

## Overlay operations

```python
# intersection : parties communes entre deux couches
result = gpd.overlay(zones_chalandise, communes, how='intersection')

# union : combine les deux couches, decoupe aux intersections
result = gpd.overlay(gdf1, gdf2, how='union')

# difference : parties de gdf1 qui ne sont pas dans gdf2
zones_hors_exclusion = gpd.overlay(zones_livraison, zones_exclusion, how='difference')

# symmetric_difference : parties de l'un ou l'autre mais pas les deux
result = gpd.overlay(gdf1, gdf2, how='symmetric_difference')

# Exemple concret : zones de chalandise sans chevauchement
# Assigner chaque point de la zone au magasin le plus proche
zones = zones_chalandise.copy()
zones_propres = zones[zones['id_magasin'] == 1].copy()
for i, other in zones[zones['id_magasin'] != 1].iterrows():
    zones_propres['geometry'] = gpd.overlay(
        zones_propres,
        gpd.GeoDataFrame([other], crs=zones.crs),
        how='difference'
    ).geometry
```

---

## Nearest Neighbor Analysis

### Avec STRtree pour performance

```python
from shapely.ops import nearest_points, unary_union
from shapely.strtree import STRtree
import numpy as np

# Methode naive (LENTE sur grandes donnees)
def nearest_naive(points_source, points_target):
    results = []
    for pt in points_source.geometry:
        dists = points_target.geometry.distance(pt)
        results.append(dists.idxmin())
    return results

# Methode avec STRtree (RAPIDE - index spatial en memoire)
def nearest_strtree(clients_gdf, magasins_gdf):
    """
    Retourne pour chaque client l'index du magasin le plus proche.
    Necessite des geometries en projection metrique.
    """
    tree = STRtree(magasins_gdf.geometry.tolist())

    nearest_idx = []
    distances = []

    for client_geom in clients_gdf.geometry:
        # query_nearest retourne l'index dans le STRtree
        idx = tree.nearest(client_geom)
        nearest_idx.append(idx)
        distances.append(client_geom.distance(magasins_gdf.geometry.iloc[idx]))

    clients_result = clients_gdf.copy()
    clients_result['magasin_idx'] = nearest_idx
    clients_result['distance_m'] = distances
    clients_result['magasin_nom'] = magasins_gdf.iloc[nearest_idx]['nom'].values
    return clients_result

# Usage
clients_l93 = clients.to_crs("EPSG:2154")
magasins_l93 = magasins.to_crs("EPSG:2154")
result = nearest_strtree(clients_l93, magasins_l93)
print(result[['nom_client', 'magasin_nom', 'distance_m']].head())

# Top-N voisins avec STRtree
def top_n_neighbors(source_gdf, target_gdf, n=5):
    tree = STRtree(target_gdf.geometry.tolist())
    results = []
    for i, row in source_gdf.iterrows():
        # geom.bounds pour la recherche de candidats
        candidates_idx = tree.query(row.geometry)
        candidates = target_gdf.iloc[candidates_idx].copy()
        candidates['dist'] = candidates.geometry.distance(row.geometry)
        top_n = candidates.nsmallest(n, 'dist')
        for rank, (j, cand) in enumerate(top_n.iterrows(), 1):
            results.append({
                'source_id': row.name,
                'target_id': j,
                'rang': rank,
                'distance_m': cand['dist']
            })
    return pd.DataFrame(results)
```

---

## Geocodage Python

### Geopy avec rate limiting

```python
from geopy.geocoders import Nominatim, GoogleV3
from geopy.extra.rate_limiter import RateLimiter
import time

# Nominatim (OpenStreetMap) — GRATUIT mais 1 requete/seconde max
geolocator = Nominatim(user_agent="mon_projet_analytics_2024")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

adresses = ["10 Rue de la Paix, Paris", "Place Bellecour, Lyon", "Vieux-Port, Marseille"]
locations = [geocode(a) for a in adresses]
coords = [(l.latitude, l.longitude) if l else (None, None) for l in locations]

# Google Maps API — Payant mais plus precis et rapide
geolocator_google = GoogleV3(api_key="YOUR_API_KEY")
geocode_google = RateLimiter(geolocator_google.geocode, min_delay_seconds=0.05)

# Cache intelligent pour eviter les doubles requetes
import functools
import json
from pathlib import Path

class GeocoderWithCache:
    def __init__(self, cache_file="geocode_cache.json"):
        self.cache_file = Path(cache_file)
        self.cache = json.loads(self.cache_file.read_text()) if self.cache_file.exists() else {}
        self.geolocator = Nominatim(user_agent="mon_projet")
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)

    def geocode_address(self, address: str) -> tuple[float, float] | None:
        if address in self.cache:
            return self.cache[address]
        result = self.geocode(address)
        coords = (result.latitude, result.longitude) if result else None
        self.cache[address] = coords
        self.cache_file.write_text(json.dumps(self.cache, ensure_ascii=False))
        return coords

    def geocode_batch(self, addresses: list[str]) -> list[tuple]:
        return [self.geocode_address(a) for a in addresses]
```

---

## Isochrones et zones d'accessibilite

### Openrouteservice API

```python
import openrouteservice
from openrouteservice.isochrones import isochrones
import geopandas as gpd

client = openrouteservice.Client(key="YOUR_ORS_API_KEY")

# Isochrone depuis un point (zone atteignable en X minutes)
coords = [[2.3522, 48.8566]]  # Paris [lon, lat]

iso = isochrones(
    client,
    locations=coords,
    profile='driving-car',      # foot-walking, cycling-regular, driving-car
    range=[300, 600, 900, 1800], # En secondes (5, 10, 15, 30 min)
    range_type='time',          # 'time' ou 'distance'
    smoothing=0.5               # Lissage des contours
)

# Convertir en GeoDataFrame
iso_gdf = gpd.GeoDataFrame.from_features(iso['features'], crs='EPSG:4326')
iso_gdf['minutes'] = iso_gdf['value'] / 60
print(iso_gdf[['minutes', 'geometry']])

# Isochrones en batch pour plusieurs magasins
def batch_isochrones(magasins_gdf, minutes=15, profile='driving-car'):
    """Calcule les isochrones pour une liste de magasins."""
    coords = [[row.geometry.x, row.geometry.y] for _, row in magasins_gdf.iterrows()]
    # Max 5 locations par requete ORS
    all_isos = []
    for i in range(0, len(coords), 5):
        batch = coords[i:i+5]
        iso = isochrones(client, locations=batch, profile=profile,
                         range=[minutes * 60], range_type='time')
        batch_gdf = gpd.GeoDataFrame.from_features(iso['features'], crs='EPSG:4326')
        all_isos.append(batch_gdf)
        time.sleep(1.5)  # Rate limiting
    return pd.concat(all_isos, ignore_index=True)
```

### OSMnx pour le reseau routier

```python
import osmnx as ox
import networkx as nx

# Telecharger le graphe routier d'une zone
G = ox.graph_from_place("Paris, France", network_type="drive")

# Ou depuis un point avec rayon
G = ox.graph_from_point((48.8566, 2.3522), dist=2000, network_type="walk")

# Statistiques du reseau
stats = ox.basic_stats(G)
print(f"Noeuds: {stats['n']}, Aretes: {stats['m']}")
print(f"Longueur totale: {stats['edge_length_total']/1000:.1f} km")

# Plus court chemin entre deux points GPS
origin = (48.8566, 2.3522)      # Paris centre
destination = (48.8738, 2.2950) # Arc de Triomphe

orig_node = ox.nearest_nodes(G, origin[1], origin[0])
dest_node = ox.nearest_nodes(G, destination[1], destination[0])

route = nx.shortest_path(G, orig_node, dest_node, weight='length')
route_length = nx.shortest_path_length(G, orig_node, dest_node, weight='length')
print(f"Distance: {route_length:.0f} metres")

# Visualiser le trajet
fig, ax = ox.plot_graph_route(G, route, route_color='red', figsize=(12, 8))
```

---

## H3 — Indexation hexagonale Uber

```python
import h3
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

# Indexer un point GPS dans une cellule H3
lat, lon = 48.8566, 2.3522
resolution = 8  # 0 (continent) a 15 (maison)
h3_index = h3.latlng_to_cell(lat, lon, resolution)
print(f"H3 index: {h3_index}")  # 8830e1c8c9fffff

# Taille approximative par resolution
# Res 6 : ~36 km2 | Res 7 : ~5 km2 | Res 8 : ~0.7 km2 | Res 9 : ~0.1 km2

# Obtenir le polygone d'une cellule H3
boundary = h3.cell_to_boundary(h3_index)
poly = Polygon([(lon, lat) for lat, lon in boundary])

# Upsampling : decomposer une cellule en sous-cellules plus fines
children = h3.cell_to_children(h3_index, 9)  # Res 8 -> Res 9 (7 cellules)

# Downsampling : remonter au parent
parent = h3.cell_to_parent(h3_index, 7)  # Res 8 -> Res 7

# K-ring : voisins a distance k
neighbors = h3.grid_disk(h3_index, k=2)  # Toutes les cellules a <= 2 pas

# Aggreger des donnees par cellule H3
df = pd.DataFrame({
    'lat': [48.8566, 48.8570, 48.8580, 48.8540],
    'lon': [2.3522, 2.3530, 2.3500, 2.3560],
    'montant': [100, 200, 150, 300]
})

df['h3_r8'] = df.apply(lambda r: h3.latlng_to_cell(r['lat'], r['lon'], 8), axis=1)
h3_agg = df.groupby('h3_r8').agg(
    nb_transactions=('montant', 'count'),
    montant_total=('montant', 'sum')
).reset_index()

# Convertir en GeoDataFrame pour visualisation
def h3_to_geodataframe(df_h3, h3_col='h3_r8'):
    geometries = []
    for h3_idx in df_h3[h3_col]:
        boundary = h3.cell_to_boundary(h3_idx)
        poly = Polygon([(lon, lat) for lat, lon in boundary])
        geometries.append(poly)
    return gpd.GeoDataFrame(df_h3, geometry=geometries, crs='EPSG:4326')

h3_gdf = h3_to_geodataframe(h3_agg)
```

---

## Raster data avec Rasterio

```python
import rasterio
from rasterio.mask import mask
from rasterio.plot import show
import numpy as np

# Ouvrir un fichier raster (DEM, satellite, etc.)
with rasterio.open("mnt_france_25m.tif") as src:
    print(f"CRS: {src.crs}")
    print(f"Dimensions: {src.width}x{src.height}")
    print(f"Nombre de bandes: {src.count}")
    print(f"Emprise: {src.bounds}")

    # Lire la bande 1 (altitude)
    elevation = src.read(1)  # numpy array 2D
    print(f"Altitude min: {elevation.min():.0f}m, max: {elevation.max():.0f}m")
    transform = src.transform

# Decouper le raster par un polygone (masking)
from shapely.geometry import mapping

with rasterio.open("mnt_france_25m.tif") as src:
    shapes = [mapping(zone_polygon)]  # GeoJSON-like dict
    out_image, out_transform = mask(src, shapes, crop=True, nodata=-9999)
    out_meta = src.meta.copy()
    out_meta.update({
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

# Statistiques raster par zone (rasterstats)
from rasterstats import zonal_stats

stats = zonal_stats(
    communes_gdf,          # GeoDataFrame ou chemin vers fichier
    "mnt_france_25m.tif",  # Raster source
    stats=['min', 'max', 'mean', 'std', 'count'],
    nodata=-9999
)
communes_gdf = communes_gdf.join(pd.DataFrame(stats))
print(communes_gdf[['nom', 'mean', 'max']].head())  # Altitude moyenne par commune
```

---

## Pipeline geospatial complet

```python
"""
Pipeline : scoring des zones de chalandise pour implantation de magasins.
Donnees : INSEE IRIS (population), OSM (concurrence), DVF (prix immo)
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from shapely.strtree import STRtree
import osmnx as ox

# 1. Chargement des donnees
engine = create_engine("postgresql+psycopg2://user:pw@localhost/geo")
iris = gpd.read_postgis("SELECT * FROM iris_2023", engine, geom_col='geometry')
iris = iris.to_crs("EPSG:2154")  # Lambert 93

# 2. Telechargement des supermarchés depuis OSM
supermarches = ox.features_from_place(
    "Ile-de-France, France",
    tags={"shop": ["supermarket", "convenience"]}
)
supermarches = supermarches.to_crs("EPSG:2154")
supermarches['geometry'] = supermarches.centroid

# 3. Calcul des indicateurs par IRIS
# 3a. Population par IRIS (deja dans iris)
iris_score = iris[['code_iris', 'population', 'geometry']].copy()

# 3b. Nombre de concurrents dans un rayon de 500m de chaque centroide IRIS
iris_centroids = iris_score.copy()
iris_centroids['geometry'] = iris_score.geometry.centroid

tree = STRtree(supermarches.geometry.tolist())
iris_centroids['nb_concurrents_500m'] = iris_centroids.geometry.apply(
    lambda g: len(tree.query(g.buffer(500)))
)

# 3c. Scoring composite (normalisation Min-Max)
def minmax_normalize(series):
    return (series - series.min()) / (series.max() - series.min())

iris_centroids['score_population'] = minmax_normalize(iris_centroids['population'])
iris_centroids['score_concurrence'] = 1 - minmax_normalize(iris_centroids['nb_concurrents_500m'])
iris_centroids['score_final'] = (
    0.6 * iris_centroids['score_population'] +
    0.4 * iris_centroids['score_concurrence']
)

# 4. Top 20 zones candidates
top_zones = iris_centroids.nlargest(20, 'score_final')
print(top_zones[['code_iris', 'population', 'nb_concurrents_500m', 'score_final']])

# 5. Export
top_zones.to_file("zones_candidates.geojson", driver="GeoJSON")
top_zones.to_postgis("zones_candidates_2024", engine, if_exists='replace')
```

Ce pipeline illustre la chaine complete : ingestion multi-sources, nettoyage CRS, analyse spatiale avec index, scoring metier, et export vers plusieurs formats. Adaptez les poids du scoring selon les criteres metier specifiques de chaque projet.
