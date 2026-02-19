---
name: geospatial-analytics
version: 1.0.0
description: >
  Geospatial analytics, GIS analysis, PostGIS spatial SQL, geopandas Python,
  choropleth maps, spatial clustering, geocoding, catchment area analysis,
  store location optimization, logistics routing, spatial joins, folium maps,
  geographic data visualization, QGIS, H3 Uber hexagons, spatial data science
---

# Geospatial Analytics — Analyse Spatiale et Cartographie

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu analyses des donnees avec une dimension geographique (clients, magasins, livraisons)
- Tu dois optimiser des zones de chalandise ou des zones de livraison
- Tu veux visualiser des metriques business sur une carte
- Tu analyses la concentration geographique (clustering spatial)
- Tu calcules des distances, zones d'accessibilite ou temps de trajet
- Tu integres des donnees externes geographiques (census, POI)

---

## Fondamentaux de la Geodonnee

### Types de Geometries

```python
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
import geopandas as gpd

# Point : une localisation (magasin, client, evenement)
paris = Point(2.3522, 48.8566)  # (longitude, latitude)
client = Point(-0.1276, 51.5074)

# LineString : un itineraire, une route, une frontiere
itineraire = LineString([
    (2.3522, 48.8566),   # Paris
    (2.9000, 43.6047),   # Toulouse
    (3.8767, 43.6119),   # Montpellier
])

# Polygon : une zone (departement, zone de livraison, ZAC)
zone_livraison = Polygon([
    (2.25, 48.80), (2.45, 48.80),
    (2.45, 48.92), (2.25, 48.92),
    (2.25, 48.80),  # Fermer le polygone
])

# Verifications utiles
print(f"Distance Paris-client : {paris.distance(client):.4f} degres")
print(f"Surface zone livraison : {zone_livraison.area:.4f} degres carres")
print(f"Client dans la zone ? {zone_livraison.contains(client)}")
```

### Systemes de Coordonnees (CRS)

```python
import geopandas as gpd

# IMPORTANT : toujours verifier et aligner le CRS
# CRS courants :
# - EPSG:4326 (WGS84) : longitude/latitude decimales → standard GPS/web
# - EPSG:2154 (Lambert 93) : systeme officiel francais → distances en metres
# - EPSG:3857 (Web Mercator) : tiles web (Google Maps, OpenStreetMap)

gdf = gpd.read_file('communes_france.geojson')
print(f"CRS actuel : {gdf.crs}")  # EPSG:4326

# Reprojeter pour calculer des distances en metres
gdf_metres = gdf.to_crs(epsg=2154)
print(f"Surface moyenne commune : {gdf_metres.geometry.area.mean() / 1e6:.1f} km²")

# Toujours reprojeter avant de calculer distances/surfaces
def distance_metres(lat1, lon1, lat2, lon2) -> float:
    """Distance en metres entre deux points GPS."""
    p1 = gpd.GeoDataFrame(geometry=[Point(lon1, lat1)], crs='EPSG:4326')
    p2 = gpd.GeoDataFrame(geometry=[Point(lon2, lat2)], crs='EPSG:4326')
    p1_m = p1.to_crs(epsg=2154)
    p2_m = p2.to_crs(epsg=2154)
    return float(p1_m.geometry.distance(p2_m.geometry.iloc[0]).iloc[0])
```

---

## GeoPandas — Analyse Spatiale Python

### Chargement et Enrichissement

```python
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Charger des donnees tabulaires avec coordonnees
def dataframe_vers_geodataframe(
    df: pd.DataFrame,
    col_lat: str = 'latitude',
    col_lon: str = 'longitude',
    crs: str = 'EPSG:4326',
) -> gpd.GeoDataFrame:
    geometry = [Point(lon, lat) for lat, lon in zip(df[col_lat], df[col_lon])]
    return gpd.GeoDataFrame(df, geometry=geometry, crs=crs)

# Charger les contours departements francais (API geo.gouv.fr)
import requests

def charger_departements() -> gpd.GeoDataFrame:
    url = 'https://geo.api.gouv.fr/departements?fields=nom,code,geometry&format=geojson'
    response = requests.get(url)
    return gpd.read_file(response.text)
```

### Spatial Join

```python
# Joindre des points avec des polygones
# Use case : attribuer chaque client a son departement

clients_gdf = dataframe_vers_geodataframe(df_clients)
departements = charger_departements().to_crs(epsg=4326)

# Spatial join : point in polygon
clients_enrichis = gpd.sjoin(
    clients_gdf,
    departements[['nom', 'code', 'geometry']],
    how='left',
    predicate='within',  # 'intersects', 'contains', 'crosses'
)

# Agregation par departement
stats_dept = clients_enrichis.groupby('code').agg(
    nb_clients=('client_id', 'count'),
    ca_total=('ca_annuel', 'sum'),
    ca_moyen=('ca_annuel', 'mean'),
).reset_index()

# Joindre avec la geographie pour visualiser
carte_dept = departements.merge(stats_dept, on='code')
```

### Analyse de Zone de Chalandise

```python
from shapely.geometry import Point
import geopandas as gpd

def zone_de_chalandise(
    magasin_lat: float, magasin_lon: float,
    rayon_km: float = 5,
) -> gpd.GeoDataFrame:
    """
    Cree une zone de chalandise circulaire (buffer) autour d'un magasin.
    Reprojeter en Lambert 93 pour avoir le rayon en metres.
    """
    magasin_wgs = gpd.GeoDataFrame(
        geometry=[Point(magasin_lon, magasin_lat)],
        crs='EPSG:4326'
    ).to_crs(epsg=2154)

    # Buffer en metres
    buffer = magasin_wgs.buffer(rayon_km * 1000)
    zone = gpd.GeoDataFrame(geometry=buffer, crs='EPSG:2154').to_crs('EPSG:4326')

    return zone

def clients_dans_zone(
    clients_gdf: gpd.GeoDataFrame,
    zone: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Filtre les clients dans la zone de chalandise."""
    return clients_gdf[clients_gdf.geometry.within(zone.geometry.iloc[0])]

# Exemple complet
zone_5km = zone_de_chalandise(48.8566, 2.3522, rayon_km=5)
clients_proches = clients_dans_zone(clients_gdf, zone_5km)
print(f"Clients dans un rayon de 5km : {len(clients_proches)}")
print(f"CA potentiel : {clients_proches['ca_annuel'].sum():,.0f} EUR")
```

---

## PostGIS — SQL Spatial

```sql
-- Activer PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Creer une table avec geometrie
CREATE TABLE magasins (
    id SERIAL PRIMARY KEY,
    nom TEXT NOT NULL,
    ville TEXT,
    localisation GEOGRAPHY(POINT, 4326)  -- GEOGRAPHY = calculs en metres automatiques
);

-- Inserer un point
INSERT INTO magasins (nom, ville, localisation)
VALUES (
    'Magasin Paris Centre',
    'Paris',
    ST_GeogFromText('POINT(2.3522 48.8566)')
);

-- Distance entre deux points (en metres avec GEOGRAPHY)
SELECT
    a.nom AS magasin_1,
    b.nom AS magasin_2,
    ROUND(ST_Distance(a.localisation, b.localisation)::NUMERIC / 1000, 2) AS distance_km
FROM magasins a
CROSS JOIN magasins b
WHERE a.id < b.id
ORDER BY distance_km;

-- Clients dans un rayon de 10km autour d'un magasin
SELECT
    c.id,
    c.nom,
    ROUND(ST_Distance(c.localisation, m.localisation)::NUMERIC / 1000, 2) AS distance_km
FROM clients c
JOIN magasins m ON m.id = 1
WHERE ST_DWithin(c.localisation, m.localisation, 10000)  -- 10 000 metres
ORDER BY distance_km;

-- Aggregation spatiale : CA par departement
SELECT
    d.nom AS departement,
    COUNT(c.id) AS nb_clients,
    SUM(c.ca_annuel) AS ca_total,
    ROUND(AVG(c.ca_annuel)) AS ca_moyen
FROM departements d
JOIN clients c ON ST_Within(c.localisation::geometry, d.geom)
GROUP BY d.id, d.nom
ORDER BY ca_total DESC;
```

---

## H3 — Grille Hexagonale Uber

H3 decoupe le monde en hexagones de taille fixe. Ideal pour les analyses de densite et le clustering.

```python
import h3
import pandas as pd
import geopandas as gpd

def enrichir_avec_h3(df: pd.DataFrame, resolution: int = 9) -> pd.DataFrame:
    """
    Ajoute un index H3 a chaque ligne.
    Resolution 9 = hexagones de ~0.1 km2 (environ 100m de diametre)
    Resolutions courantes : 7 (5km), 8 (0.7km), 9 (0.1km), 10 (0.015km)
    """
    df = df.copy()
    df['h3_index'] = df.apply(
        lambda row: h3.latlng_to_cell(row['latitude'], row['longitude'], resolution),
        axis=1
    )
    return df

def agregation_h3(df_avec_h3: pd.DataFrame, resolution: int = 9) -> gpd.GeoDataFrame:
    """
    Agrege les donnees par hexagone H3 et retourne un GeoDataFrame visualisable.
    """
    from shapely.geometry import Polygon

    stats = df_avec_h3.groupby('h3_index').agg(
        nb_clients=('client_id', 'count'),
        ca_total=('ca_annuel', 'sum'),
    ).reset_index()

    # Convertir les index H3 en polygones
    def h3_vers_polygon(h3_index: str) -> Polygon:
        boundary = h3.cell_to_boundary(h3_index)
        return Polygon([(lng, lat) for lat, lng in boundary])

    stats['geometry'] = stats['h3_index'].apply(h3_vers_polygon)
    return gpd.GeoDataFrame(stats, crs='EPSG:4326')
```

---

## Visualisation avec Folium

```python
import folium
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd

def creer_carte_clients(
    clients_df: pd.DataFrame,
    centre: tuple = (46.2276, 2.2137),  # Centre France
    zoom: int = 6,
) -> folium.Map:
    """Cree une carte interactive avec les clients et leur segmentation."""

    carte = folium.Map(location=centre, zoom_start=zoom, tiles='CartoDB positron')

    # Heatmap de densite
    chaleur = clients_df[['latitude', 'longitude', 'ca_annuel']].values.tolist()
    HeatMap(chaleur, radius=15, name='Densite clients').add_to(carte)

    # Marqueurs clusteres par segment
    segments = {
        'Champions': {'couleur': 'red', 'icone': 'star'},
        'Fideles': {'couleur': 'blue', 'icone': 'user'},
        'A risque': {'couleur': 'orange', 'icone': 'exclamation-sign'},
    }

    for segment, style in segments.items():
        cluster = MarkerCluster(name=f"Clients {segment}")
        clients_seg = clients_df[clients_df['segment_rfm'] == segment]

        for _, client in clients_seg.iterrows():
            folium.Marker(
                location=[client['latitude'], client['longitude']],
                popup=folium.Popup(
                    f"<b>{client['nom']}</b><br>CA : {client['ca_annuel']:,.0f} EUR<br>Segment : {segment}",
                    max_width=200,
                ),
                icon=folium.Icon(color=style['couleur'], icon=style['icone'], prefix='glyphicon'),
            ).add_to(cluster)

        cluster.add_to(carte)

    folium.LayerControl().add_to(carte)
    return carte

# Sauvegarder et afficher
carte = creer_carte_clients(clients_df)
carte.save('clients_carte.html')
```

---

## Clustering Spatial — DBSCAN

```python
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd

def clustering_spatial(
    df: pd.DataFrame,
    eps_km: float = 2.0,     # Rayon maximal d'un cluster (km)
    min_samples: int = 5,     # Minimum de points pour former un cluster
) -> pd.DataFrame:
    """
    DBSCAN geospatial : identifier les zones de concentration.
    Adapte pour les coordonnees GPS en utilisant la distance haversine.
    """
    # Convertir en radians pour la metrique haversine
    coords = np.radians(df[['latitude', 'longitude']].values)
    eps_rad = eps_km / 6371  # Rayon terrestre en km

    clusterer = DBSCAN(
        eps=eps_rad,
        min_samples=min_samples,
        algorithm='ball_tree',
        metric='haversine',
    )

    df = df.copy()
    df['cluster_id'] = clusterer.fit_predict(coords)
    # -1 = bruit (points isoles)

    # Statistiques par cluster
    stats = df[df['cluster_id'] != -1].groupby('cluster_id').agg(
        nb_clients=('client_id', 'count'),
        ca_total=('ca_annuel', 'sum'),
        lat_centre=('latitude', 'mean'),
        lon_centre=('longitude', 'mean'),
    ).reset_index()

    print(f"Clusters identifies : {stats.shape[0]}")
    print(f"Points isoles (bruit) : {(df['cluster_id'] == -1).sum()}")

    return df, stats
```

---

## References

- `references/postgis-sql.md` — Fonctions PostGIS completes, indexation spatiale, optimisation
- `references/geopandas-analysis.md` — Analyse spatiale avancee, overlay, dissolve, buffer, nearest
- `references/visualization-maps.md` — Folium, Plotly Maps, Kepler.gl, Power BI Maps, cartes choroplethes
- `references/case-studies.md` — 4 cas : implantation magasins, zones de livraison, analyse fraude geo
