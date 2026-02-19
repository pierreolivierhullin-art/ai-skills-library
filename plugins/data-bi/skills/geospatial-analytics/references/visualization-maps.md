# Visualisation Cartographique — Folium, Plotly et Kepler.gl

## Types de cartes — quand utiliser quoi

| Type | Cas d'usage | Outil recommande | Pieges |
|---|---|---|---|
| Choroplethique | Indicateur agrege par zone (revenus, densite) | Folium, Plotly, Tableau | Effet taille des zones, choisir bonne classification |
| Proportionnelle | Valeur absolue par point (CA par magasin) | Folium CircleMarker, Plotly scatter_mapbox | Surcharge visuelle si trop de points |
| Flux (OD matrix) | Origines-destinations, migrations | Kepler.gl arc layer | Lisibilite si trop de flux |
| Heatmap | Densite de points, concentration incidents | Folium HeatMap, Kepler.gl heatmap | Masque la distribution reelle |
| Cluster | Regroupement de points a differents zooms | Folium MarkerCluster | Perd l'info spatiale precise |
| Isochrone | Zones d'accessibilite depuis un point | Folium Choropleth, Kepler.gl | Necessite calcul prealable |
| Dot density | Distribution spatiale sans agregation | Folium CircleMarker | Performance sur >10k points |

---

## Folium — Cartes interactives avancees

### Configuration de base et tiles

```python
import folium
from folium import plugins
import geopandas as gpd
import json

# Creer une carte de base
m = folium.Map(
    location=[46.2276, 2.2137],  # Centre de la France
    zoom_start=6,
    tiles='CartoDB positron',     # Fond sobre pour les donnees
    # Autres tiles : 'OpenStreetMap', 'CartoDB dark_matter', 'Stamen Toner'
    control_scale=True,           # Echelle en bas a gauche
    prefer_canvas=True            # Performance avec beaucoup de marqueurs
)

# Ajouter plusieurs couches de fond
folium.TileLayer('CartoDB positron', name='Fond clair').add_to(m)
folium.TileLayer('CartoDB dark_matter', name='Fond sombre').add_to(m)
folium.TileLayer('OpenStreetMap', name='OSM').add_to(m)
folium.LayerControl().add_to(m)
```

### GeoJson avec style function

```python
# Style dynamique base sur les attributs des features
communes_geojson = json.loads(communes_gdf.to_json())

def style_function(feature):
    """Colorie les communes selon leur densite de population."""
    densite = feature['properties'].get('densite', 0)
    if densite > 5000:
        color = '#08306b'
    elif densite > 1000:
        color = '#2171b5'
    elif densite > 100:
        color = '#74c476'
    else:
        color = '#f7fcf5'
    return {
        'fillColor': color,
        'color': '#333333',
        'weight': 0.5,
        'fillOpacity': 0.7
    }

def highlight_function(feature):
    """Surbrillance au survol de la souris."""
    return {
        'fillColor': '#ffff00',
        'color': '#000000',
        'weight': 2,
        'fillOpacity': 0.9
    }

geojson_layer = folium.GeoJson(
    communes_geojson,
    name='Communes - Densite',
    style_function=style_function,
    highlight_function=highlight_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['nom', 'population', 'densite'],
        aliases=['Commune:', 'Population:', 'Densite (hab/km2):'],
        localize=True,
        sticky=True
    ),
    popup=folium.GeoJsonPopup(
        fields=['nom', 'code_insee', 'population', 'superficie'],
        aliases=['Commune', 'Code INSEE', 'Population', 'Superficie (km2)']
    )
).add_to(m)
```

### Choropleth avec ColorMap

```python
import branca.colormap as cm

# Creer une colormap continue
colormap = cm.LinearColormap(
    colors=['#ffffcc', '#41b6c4', '#0c2c84'],
    vmin=communes_gdf['revenu_median'].min(),
    vmax=communes_gdf['revenu_median'].max(),
    caption='Revenu median mensuel (EUR)'
)

# Choropleth via folium.Choropleth (plus simple que GeoJson pour les cartes thematiques)
folium.Choropleth(
    geo_data=communes_gdf.__geo_interface__,
    data=communes_gdf,
    columns=['code_insee', 'revenu_median'],
    key_on='feature.properties.code_insee',
    fill_color='YlOrRd',       # Palettes : YlOrRd, BuGn, PuRd, Blues, RdYlGn
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Revenu median mensuel (EUR)',
    nan_fill_color='white',
    name='Revenu median'
).add_to(m)

# ColorMap personnalisee avec etapes
colormap_stepped = cm.StepColormap(
    colors=['#fee5d9', '#fcbba1', '#fb6a4a', '#de2d26', '#a50f15'],
    index=[0, 20000, 35000, 50000, 80000, 150000],
    vmin=0, vmax=150000,
    caption='CA annuel (EUR)'
)
colormap_stepped.add_to(m)
```

### TimestampedGeoJson — Animation temporelle

```python
from folium.plugins import TimestampedGeoJson
import pandas as pd

# Preparer les donnees avec timestamps
df_incidents = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=100, freq='D'),
    'lat': [48.85 + np.random.randn()*0.1 for _ in range(100)],
    'lon': [2.35 + np.random.randn()*0.1 for _ in range(100)],
    'type': np.random.choice(['vol', 'accident', 'fraude'], 100)
})

features = []
for _, row in df_incidents.iterrows():
    features.append({
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [row['lon'], row['lat']]
        },
        'properties': {
            'time': row['date'].strftime('%Y-%m-%dT%H:%M:%S'),
            'style': {'color': 'red' if row['type'] == 'fraude' else 'blue'},
            'icon': 'circle',
            'iconstyle': {
                'fillColor': 'red' if row['type'] == 'fraude' else 'blue',
                'fillOpacity': 0.8,
                'radius': 6
            },
            'popup': f"Type: {row['type']}<br>Date: {row['date'].date()}"
        }
    })

TimestampedGeoJson(
    data={'type': 'FeatureCollection', 'features': features},
    period='P1D',              # Periode : P1D = 1 jour, PT1H = 1 heure
    add_last_point=True,
    auto_play=True,
    loop=True,
    max_speed=10,
    loop_button=True,
    date_options='YYYY-MM-DD',
    time_slider_drag_update=True
).add_to(m)
```

### Plugins Folium utiles

```python
from folium.plugins import (
    HeatMap, MarkerCluster, MiniMap, MeasureControl,
    Fullscreen, DualMap, MousePosition, LocateControl
)

# HeatMap pour densite de points
heat_data = [[row['lat'], row['lon'], row['poids']] for _, row in df.iterrows()]
HeatMap(
    heat_data,
    min_opacity=0.3,
    max_zoom=15,
    radius=15,
    blur=10,
    gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}
).add_to(m)

# MarkerCluster pour >1000 points
cluster = MarkerCluster(name='Magasins').add_to(m)
for _, row in magasins.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        color='blue',
        fill=True,
        popup=f"<b>{row['nom']}</b><br>CA: {row['ca']:,} EUR"
    ).add_to(cluster)

# MiniMap en bas a droite
MiniMap(toggle_display=True, position='bottomright').add_to(m)

# Comparaison deux cartes (DualMap)
dual = DualMap(location=[46.2276, 2.2137], zoom_start=6, layout='horizontal')
folium.TileLayer('CartoDB positron').add_to(dual.m1)
folium.TileLayer('CartoDB dark_matter').add_to(dual.m2)
# Ajouter des layers differents sur m1 et m2

# Plein ecran
Fullscreen(position='topleft').add_to(m)

# Coordonnees de la souris
MousePosition().add_to(m)

# Mesure de distances
MeasureControl(position='bottomleft').add_to(m)

# Sauvegarde
m.save("carte_interactive.html")
```

### Performance Folium avec simplify

```python
# Simplifier les geometries avant injection dans Folium
def prepare_for_folium(gdf, tolerance_m=100):
    """Projette en L93, simplifie, reprojette en WGS84."""
    gdf_l93 = gdf.to_crs("EPSG:2154")
    gdf_simple = gdf_l93.copy()
    gdf_simple['geometry'] = gdf_l93.geometry.simplify(
        tolerance=tolerance_m,
        preserve_topology=True
    )
    return gdf_simple.to_crs("EPSG:4326")

communes_web = prepare_for_folium(communes, tolerance_m=200)
# Reduire de 80% la taille du GeoJSON pour les cartes au niveau national
```

---

## Plotly Maps

### px.choropleth et px.scatter_mapbox

```python
import plotly.express as px
import plotly.graph_objects as go
import json

# Choropleth avec px (GeoJSON externe)
with open('departements.geojson') as f:
    depts_geojson = json.load(f)

fig = px.choropleth(
    df_departements,
    geojson=depts_geojson,
    locations='code_dept',
    featureidkey='properties.code',
    color='chiffre_affaires',
    color_continuous_scale='Blues',
    range_color=(0, df_departements['chiffre_affaires'].quantile(0.95)),
    title='Chiffre d\'affaires par departement 2024',
    labels={'chiffre_affaires': 'CA (MEUR)'},
    hover_data=['nom_dept', 'population']
)
fig.update_geos(
    fitbounds='locations',
    visible=False
)
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

# scatter_mapbox pour des points avec Mapbox
fig_scatter = px.scatter_mapbox(
    df_magasins,
    lat='latitude',
    lon='longitude',
    size='chiffre_affaires',
    color='categorie',
    hover_name='nom_magasin',
    hover_data={'latitude': False, 'longitude': False, 'chiffre_affaires': ':,.0f'},
    color_continuous_scale=px.colors.cyclical.IceFire,
    size_max=25,
    zoom=5,
    mapbox_style='open-street-map',  # Gratuit, ou 'carto-positron', 'carto-darkmatter'
    title='Magasins par CA'
)

# Animation frame pour donnees temporelles
fig_anim = px.scatter_mapbox(
    df_monthly,
    lat='lat', lon='lon',
    size='ventes',
    animation_frame='mois',
    animation_group='magasin_id',
    mapbox_style='carto-positron',
    zoom=4
)
fig_anim.update_layout(updatemenus=[dict(type='buttons', showactive=False)])
```

### go.Scattermapbox pour controle avance

```python
fig = go.Figure()

# Couche 1 : zones de chalandise (polygones)
for _, row in zones_chalandise.iterrows():
    coords = list(row.geometry.exterior.coords)
    lats = [c[1] for c in coords]
    lons = [c[0] for c in coords]
    fig.add_trace(go.Scattermapbox(
        lat=lats, lon=lons,
        mode='lines',
        fill='toself',
        fillcolor='rgba(0, 100, 200, 0.2)',
        line=dict(color='rgba(0, 100, 200, 0.8)', width=2),
        name=f"Zone {row['magasin_nom']}",
        hoverinfo='name'
    ))

# Couche 2 : points magasins
fig.add_trace(go.Scattermapbox(
    lat=magasins['lat'],
    lon=magasins['lon'],
    mode='markers+text',
    marker=go.scattermapbox.Marker(
        size=magasins['ca_normalise'] * 20 + 8,
        color=magasins['score'],
        colorscale='RdYlGn',
        showscale=True,
        colorbar=dict(title='Score')
    ),
    text=magasins['nom'],
    textposition='top right',
    hovertemplate=(
        '<b>%{text}</b><br>'
        'CA: %{customdata[0]:,.0f} EUR<br>'
        'Score: %{marker.color:.2f}<extra></extra>'
    ),
    customdata=magasins[['chiffre_affaires']].values,
    name='Magasins'
))

fig.update_layout(
    mapbox_style='carto-positron',
    mapbox_zoom=9,
    mapbox_center={"lat": 48.8566, "lon": 2.3522},
    margin={"r":0,"t":40,"l":0,"b":0},
    height=700,
    legend=dict(x=0, y=1)
)
fig.show()
fig.write_html("dashboard_magasins.html")
```

---

## Kepler.gl

### Installation et configuration

```bash
pip install keplergl jupyter-widgets
jupyter nbextension install --py --sys-prefix keplergl
jupyter nbextension enable --py --sys-prefix keplergl
```

### Usage Python (Jupyter)

```python
from keplergl import KeplerGl
import geopandas as gpd

# Creer une carte Kepler.gl
map_kepler = KeplerGl(height=600)

# Ajouter des donnees (GeoDataFrame, DataFrame, GeoJSON dict)
map_kepler.add_data(data=magasins_gdf, name="Magasins")
map_kepler.add_data(data=zones_chalandise_gdf, name="Zones de chalandise")
map_kepler.add_data(data=flux_df, name="Flux clients")  # DataFrame avec orig/dest lat/lon

# Afficher en notebook
map_kepler
```

### Configuration JSON pour automatiser Kepler.gl

```python
# Exporter la config depuis l'interface, puis la reutiliser
config = {
    "version": "v1",
    "config": {
        "visState": {
            "layers": [
                {
                    "id": "heatmap_incidents",
                    "type": "heatmap",
                    "config": {
                        "dataId": "Incidents",
                        "label": "Densite des incidents",
                        "color": [255, 153, 31],
                        "columns": {"lat": "latitude", "lng": "longitude"},
                        "isVisible": True,
                        "visConfig": {
                            "opacity": 0.8,
                            "colorRange": {
                                "colors": ["#0d0887", "#7e03a8", "#cb4679",
                                           "#f89540", "#f0f921"]
                            },
                            "radius": 20
                        }
                    }
                },
                {
                    "id": "arc_flux",
                    "type": "arc",
                    "config": {
                        "dataId": "Flux clients",
                        "columns": {
                            "lat0": "lat_origine", "lng0": "lon_origine",
                            "lat1": "lat_destination", "lng1": "lon_destination"
                        },
                        "isVisible": True,
                        "visConfig": {
                            "opacity": 0.4,
                            "strokeWidth": 2,
                            "colorRange": {"colors": ["#00b8d9", "#0052cc"]}
                        }
                    }
                }
            ],
            "filters": [
                {
                    "dataId": "Incidents",
                    "id": "filter_date",
                    "type": "timeRange",
                    "name": ["date"],
                    "enlarged": True   # Afficher le slider temporel
                }
            ]
        },
        "mapState": {
            "latitude": 48.8566,
            "longitude": 2.3522,
            "zoom": 11
        },
        "mapStyle": {
            "styleType": "dark"   # dark, light, muted, satellite
        }
    }
}

map_kepler = KeplerGl(height=600, config=config)
map_kepler.add_data(data=incidents_gdf, name="Incidents")
map_kepler.save_to_html(file_name="kepler_dashboard.html")
```

---

## Power BI Maps

### Azure Maps et Shape Map

```
Configuration Power BI Maps :
1. Azure Maps (premium) :
   - Activer dans Parametres tenant -> Cartes et visuels remplis
   - Bubble map : latitude/longitude + taille par mesure
   - Choropleth : connecter un champ geo (pays, ville, code postal)
   - Heat map layer : active depuis les options du visuel

2. Shape Map (custom boundaries) :
   - Importer un TopoJSON (https://mapshaper.org/ pour convertir shapefile)
   - Matching key : code ISO, code INSEE, ou nom exactement correspondant
   - Couleur par mesure DAX

Mesures DAX utiles pour maps :
   Densite = DIVIDE([Nb incidents], [Surface km2])
   CA par km2 = CALCULATE(SUM(Ventes[CA]), ALLEXCEPT(Communes, Communes[Code]))
               / VALUES(Communes[Surface_km2])

3. ArcGIS Maps for Power BI :
   - Couches supplementaires (demographics Esri, donnees meteo)
   - Infographics cards sur le clic
   - Drive time areas (isochrones integrees)
```

---

## Tableau Maps

```
Types de cartes disponibles dans Tableau :
- Filled Map (choropleth) : zone geographique coloree selon mesure
- Symbol Map : cercles proportionnels sur les localisations
- Density Map : heatmap de concentration
- Proportional Symbol Map : combines formes et couleurs

Configuration :
1. Assigner les roles geodimensionnels (Dimension -> Geographic Role)
   : Country, State, City, ZIP Code, Latitude, Longitude
2. Double-clic sur une dimension geo -> genere automatiquement lat/lon
3. Pages shelf pour animation temporelle

Import fichiers spatiaux dans Tableau :
- Connecter -> Fichier spatial (Shapefile, KML, GeoJSON, TopoJSON)
- Chaque feature devient une ligne, geometrie automatiquement reconnue
- Jointure possible avec autres sources de donnees sur cle commune

Calculs geographiques Tableau :
DISTANCE([Latitude_magasin], [Longitude_magasin],
         [Latitude_client], [Longitude_client], 'km')
MAKELINE([Point_depart], [Point_arrivee])  -- pour flux
BUFFER([Point], [Rayon], 'km')             -- zone tampon
```

---

## Cartes statiques avec Matplotlib et Cartopy

```python
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from matplotlib.colors import BoundaryNorm, ListedColormap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import numpy as np

fig, ax = plt.subplots(
    1, 1,
    figsize=(14, 10),
    subplot_kw={'projection': ccrs.LambertConformal(
        central_longitude=3.0,
        central_latitude=46.5
    )}
)

# Fond cartographique
ax.add_feature(cfeature.LAND, facecolor='#f5f5f0')
ax.add_feature(cfeature.OCEAN, facecolor='#c8d8e4')
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.8)

# Emprise France metropolitaine
ax.set_extent([-5, 10, 41, 52], crs=ccrs.PlateCarree())

# Choropleth avec classification Jenks
import mapclassify
breaks = mapclassify.JenksCaspall(departements['revenu_median'], k=5)
departements['classe'] = breaks.yb

colors = ['#feedde', '#fdbe85', '#fd8d3c', '#e6550d', '#a63603']
cmap = ListedColormap(colors)
norm = BoundaryNorm(boundaries=[0, 1, 2, 3, 4, 5], ncolors=5)

departements.plot(
    ax=ax,
    column='classe',
    cmap=cmap,
    norm=norm,
    transform=ccrs.PlateCarree(),
    edgecolor='white',
    linewidth=0.3
)

# Legende manuelle
patches = [
    mpatches.Patch(color=c, label=f"Classe {i+1}: {breaks.bins[i]:.0f} EUR")
    for i, c in enumerate(colors)
]
ax.legend(handles=patches, loc='lower left', title='Revenu median', fontsize=9)

# Titre et source
ax.set_title('Revenu median par departement — France 2024', fontsize=14, fontweight='bold')
fig.text(0.5, 0.02, 'Sources: INSEE 2024 | Fond: Natural Earth', ha='center', fontsize=8)

plt.tight_layout()
plt.savefig('carte_revenus_france.pdf', dpi=300, bbox_inches='tight')
plt.savefig('carte_revenus_france.png', dpi=150, bbox_inches='tight')
```

---

## Principes cartographiques

### Choix de projection

| Projection | EPSG | Usage | Distorsion |
|---|---|---|---|
| WGS84 (GPS) | 4326 | Stockage, API, web | Surfaces non preservees |
| Mercator Web | 3857 | Fonds de carte web (OSM, Google) | Poles dilates |
| Lambert 93 | 2154 | France, calculs metriques | Minimale sur France |
| UTM Zone 31N | 32631 | France ouest, calculs locaux | Minimale dans la zone |

### Classifications pour choropleth

```python
import mapclassify

valeurs = departements['densite'].values

# Jenks (Natural Breaks) : minimise la variance intra-classe — recommande
jenks = mapclassify.JenksCaspall(valeurs, k=5)

# Quantile : effectifs egaux par classe — peut masquer les extremes
quantile = mapclassify.Quantiles(valeurs, k=5)

# Equal Interval : intervalles reguliers — lisible mais sensible aux outliers
equal = mapclassify.EqualInterval(valeurs, k=5)

# Fisher-Jenks : version optimale de Jenks — meilleure precision
fisher = mapclassify.FisherJenks(valeurs, k=5)

print(f"Jenks breaks: {jenks.bins}")
print(f"Quantile breaks: {quantile.bins}")
```

### Palettes de couleurs

```python
# Sequentielles (bas -> haut) : Blues, Oranges, YlOrRd, BuGn
# Divergentes (negatif -> zero -> positif) : RdYlGn, PuOr, BrBG
# Qualitatives (categories) : Set1, Paired, tab10

# Regles :
# - Sequentielle pour une seule variable positive (population, CA)
# - Divergente pour deviation par rapport a une reference (evolution, delta)
# - Ne jamais utiliser arc-en-ciel (rainbow) : non-intuitif et inaccessible aux daltoniens
# - Tester avec simulateur daltonisme : https://www.color-blindness.com/coblis-color-blindness-simulator/
```

### Bonnes pratiques UX cartographiques

```
Elements obligatoires sur toute carte professionnelle :
1. Titre clair : "Variable | Zone geographique | Periode"
2. Legende complete avec unite et methode de classification
3. Source des donnees + date
4. Echelle graphique (barre d'echelle, pas "echelle approximative")
5. Orientation (fleche Nord si non-standard)
6. Projection utilisee si non-evidente

Interactivite recommandee :
- Tooltip au survol : nom de la zone + valeur exacte + rang
- Clic pour detail : ouvre un panneau lateral avec indicateurs complementaires
- Filtre temporel : slider ou animation
- Zoom coherent : ne pas laisser l'utilisateur zoomer trop loin

Performance web :
- Simplifier les geometries (tolerance 0.001 degres pour niveau national)
- Limiter a 1000 features dans Folium sans clustering
- Utiliser des tuiles vectorielles (Mapbox GL) pour >10k polygones
- Chunking temporel : charger les donnees par tranche a la demande
```
