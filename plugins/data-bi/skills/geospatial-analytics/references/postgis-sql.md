# PostGIS — SQL Spatial Avance

## Introduction et installation

PostGIS est l'extension spatiale de PostgreSQL. Elle transforme une base relationnelle classique en base de donnees geospatiale complete, compatible avec les standards OGC (Open Geospatial Consortium). PostGIS est la reference en production pour stocker, interroger et analyser des donnees geographiques cote serveur.

### Installation

```sql
-- Sur PostgreSQL 15+ avec pgAdmin ou psql
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
CREATE EXTENSION postgis_raster;    -- Pour les donnees raster
CREATE EXTENSION address_standardizer;
CREATE EXTENSION fuzzystrmatch;     -- Prerequis pour tiger_geocoder
CREATE EXTENSION postgis_tiger_geocoder;
CREATE EXTENSION pgrouting;         -- Routing et analyse de reseau

-- Verifier la version installee
SELECT postgis_version();
SELECT postgis_full_version();
-- 3.3.2 USE_GEOS=1 USE_PROJ=1 USE_STATS=1
```

### Configuration initiale recommandee

```sql
-- Augmenter la memoire de travail pour les requetes spatiales
ALTER SYSTEM SET work_mem = '256MB';
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;
-- Reload sans redemarrage
SELECT pg_reload_conf();
```

---

## Types geometriques — GEOMETRY vs GEOGRAPHY

### Difference fondamentale

**GEOMETRY** utilise un systeme de coordonnees cartesiennes planaires. Les calculs sont rapides mais ignorent la courbure de la Terre. Adapte pour des zones locales (ville, region) ou des donnees en projection metrique (Lambert 93 en France, EPSG:2154).

**GEOGRAPHY** travaille sur un ellipsoide (WGS84 par defaut). Les calculs tiennent compte de la courbure terrestre. Les distances sont en metres automatiquement. Plus lent mais precis pour des distances superieures a quelques dizaines de kilometres.

### Regle de decision

| Scenario | Type recommande | Raison |
|---|---|---|
| Donnees France entiere | GEOGRAPHY ou GEOMETRY(EPSG:2154) | Precision acceptable |
| Distance < 50 km | GEOMETRY | Performance |
| Distance > 50 km ou transnationale | GEOGRAPHY | Precision obligatoire |
| Calculs topologiques (within, contains) | GEOMETRY | Fonctions limitees en GEOGRAPHY |
| ST_Distance retournant des metres directement | GEOGRAPHY | Pas de conversion manuelle |

```sql
-- GEOMETRY : stocke en WGS84 mais calcule en degres (MAUVAIS pour distance)
CREATE TABLE points_geometry (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    geom GEOMETRY(POINT, 4326)
);

-- GEOGRAPHY : stocke en WGS84, calcule sur ellipsoide (CORRECT pour distance)
CREATE TABLE points_geography (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    geog GEOGRAPHY(POINT, 4326)
);

-- Demonstration de la difference
INSERT INTO points_geometry VALUES (1, 'Paris', ST_SetSRID(ST_MakePoint(2.3522, 48.8566), 4326));
INSERT INTO points_geometry VALUES (2, 'Lyon', ST_SetSRID(ST_MakePoint(4.8357, 45.7640), 4326));

-- GEOMETRY : retourne des degres, inutilisable directement
SELECT ST_Distance(a.geom, b.geom) AS dist_degres
FROM points_geometry a, points_geometry b
WHERE a.nom = 'Paris' AND b.nom = 'Lyon';
-- Resultat : 2.876... (degres)

-- GEOGRAPHY : retourne des metres, utilisable directement
SELECT ST_Distance(a.geog::GEOGRAPHY, b.geog::GEOGRAPHY) / 1000 AS dist_km
FROM points_geometry a, points_geometry b
WHERE a.nom = 'Paris' AND b.nom = 'Lyon';
-- Resultat : 391.4 km (correct)
```

### Tous les types geometriques

```sql
-- POINT : un emplacement
SELECT ST_AsText(ST_MakePoint(2.3522, 48.8566));  -- POINT(2.3522 48.8566)

-- LINESTRING : une ligne (route, fleuve)
SELECT ST_AsText(ST_MakeLine(ARRAY[
    ST_MakePoint(2.3522, 48.8566),
    ST_MakePoint(2.3488, 48.8534),
    ST_MakePoint(2.3511, 48.8499)
]));

-- POLYGON : une zone fermee
SELECT ST_AsText(ST_MakePolygon(ST_GeomFromText(
    'LINESTRING(0 0, 4 0, 4 4, 0 4, 0 0)'
)));

-- MULTIPOLYGON : plusieurs zones (ex: archipel, commune avec enclave)
SELECT ST_AsText(ST_GeomFromText(
    'MULTIPOLYGON(((0 0, 4 0, 4 4, 0 4, 0 0)),((10 10, 14 10, 14 14, 10 14, 10 10)))'
));

-- GEOMETRYCOLLECTION : melange de types
SELECT ST_AsText(ST_Collect(ARRAY[
    ST_MakePoint(0, 0)::GEOMETRY,
    ST_GeomFromText('LINESTRING(1 1, 2 2)'),
    ST_GeomFromText('POLYGON((5 5, 10 5, 10 10, 5 10, 5 5))')
]));
```

---

## Index spatial GIST — obligatoire en production

### Pourquoi l'index spatial est non-negociable

Sans index GiST, une requete spatiale fait un scan complet de la table. Sur 1 million de points, la difference est de plusieurs ordres de magnitude : 30 secondes vs 2 millisecondes.

```sql
-- Creer l'index GIST (toujours apres insertion bulk des donnees)
CREATE INDEX idx_commerces_geom ON commerces USING GIST (geom);
CREATE INDEX idx_commerces_geog ON commerces USING GIST (geog);

-- Index partiel pour les donnees actives uniquement
CREATE INDEX idx_clients_actifs_geom ON clients USING GIST (geom)
WHERE statut = 'actif';

-- BRIN index pour des donnees ordonnees spatialement (moins efficace mais plus leger)
CREATE INDEX idx_logs_geom_brin ON logs_gps USING BRIN (geom);
```

### EXPLAIN ANALYZE avec et sans index

```sql
-- Requete sans index : TRES LENT
DROP INDEX IF EXISTS idx_commerces_geom;

EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT nom, categorie
FROM commerces
WHERE ST_DWithin(geom::GEOGRAPHY, ST_MakePoint(2.3522, 48.8566)::GEOGRAPHY, 1000);
-- Seq Scan on commerces (cost=0.00..45823.00 rows=333 width=32)
--   (actual time=0.234..28341.123 rows=147 loops=1)
-- Execution Time: 28341.456 ms

-- Recrer l'index
CREATE INDEX idx_commerces_geom ON commerces USING GIST (geom);
ANALYZE commerces;

-- Meme requete avec index : INSTANTANE
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT nom, categorie
FROM commerces
WHERE ST_DWithin(geom::GEOGRAPHY, ST_MakePoint(2.3522, 48.8566)::GEOGRAPHY, 1000);
-- Index Scan using idx_commerces_geom on commerces
--   (cost=0.28..823.45 rows=147 width=32)
--   (actual time=0.082..1.234 rows=147 loops=1)
-- Execution Time: 1.456 ms
```

---

## Fonctions de mesure

```sql
-- ST_Distance : distance entre deux geometries
-- Avec GEOGRAPHY : retourne des metres
SELECT
    c1.nom AS magasin,
    c2.nom AS client,
    ROUND(ST_Distance(c1.geog, c2.geog)::NUMERIC) AS distance_metres
FROM commerces c1, clients c2
WHERE c1.id = 42 AND c2.id = 1337;

-- ST_DWithin : test de proximite avec index (BEAUCOUP plus rapide que ST_Distance < X)
-- Toujours preferer ST_DWithin a ST_Distance < seuil en WHERE
SELECT nom FROM commerces
WHERE ST_DWithin(geog, ST_MakePoint(2.3522, 48.8566)::GEOGRAPHY, 500);
-- Utilise l'index GIST, contrairement a ST_Distance < 500

-- ST_Length : longueur d'une ligne
SELECT
    nom_rue,
    ROUND(ST_Length(geom::GEOGRAPHY)::NUMERIC) AS longueur_metres
FROM rues
ORDER BY longueur_metres DESC
LIMIT 10;

-- ST_Area : surface d'un polygone
SELECT
    nom_quartier,
    ROUND(ST_Area(geom::GEOGRAPHY)::NUMERIC / 1000000, 2) AS surface_km2
FROM quartiers
ORDER BY surface_km2 DESC;

-- ST_Perimeter : perimetre d'un polygone (utile pour compacite)
SELECT
    nom,
    ST_Area(geom::GEOGRAPHY) AS aire,
    ST_Perimeter(geom::GEOGRAPHY) AS perimetre,
    -- Indice de compacite de Miller (1 = cercle parfait)
    4 * PI() * ST_Area(geom::GEOGRAPHY) / POWER(ST_Perimeter(geom::GEOGRAPHY), 2) AS compacite
FROM communes;
```

---

## Fonctions de construction geometrique

```sql
-- ST_Buffer : zone tampon autour d'un point, ligne ou polygone
-- En GEOGRAPHY (metres), en GEOMETRY (unites du SRID)

-- Zone de 500m autour de chaque magasin
SELECT id, nom, ST_Buffer(geog, 500)::GEOMETRY AS zone_achalandise
FROM magasins;

-- Buffer avec quad_segs pour lisser les courbes (defaut 8, augmenter pour rapports)
SELECT ST_Buffer(geom::GEOGRAPHY, 200, 'quad_segs=16')::GEOMETRY AS zone_fine
FROM points_interet;

-- ST_Centroid : centre geometrique d'un polygone
SELECT nom_commune, ST_Centroid(geom) AS centre
FROM communes;
-- Note: ST_PointOnSurface garantit que le point est DANS le polygone (pour les formes concaves)
SELECT nom_commune, ST_PointOnSurface(geom) AS point_interieur
FROM communes;

-- ST_ConvexHull : enveloppe convexe (minimum bounding polygon convex)
SELECT ST_ConvexHull(ST_Collect(geom)) AS hull_magasins
FROM magasins
WHERE region = 'Ile-de-France';

-- ST_Union : fusion de plusieurs geometries en une seule
SELECT ST_Union(geom) AS departement_complet
FROM communes
WHERE code_dept = '75';

-- ST_Difference : soustraction de geometries
SELECT
    z.nom AS zone,
    ST_Difference(z.geom, e.geom) AS zone_sans_exclusion
FROM zones_livraison z
JOIN zones_exclusion e ON ST_Intersects(z.geom, e.geom);

-- ST_Intersection : intersection de deux geometries
SELECT
    a.nom AS zone_a,
    b.nom AS zone_b,
    ST_Intersection(a.geom, b.geom) AS overlap
FROM zones a
JOIN zones b ON a.id < b.id AND ST_Intersects(a.geom, b.geom);

-- ST_Simplify : reduction du nombre de points (pour performance viz)
SELECT nom, ST_Simplify(geom, 0.001) AS geom_simplifiee
FROM communes;
-- Douglas-Peucker preservant la topologie
SELECT nom, ST_SimplifyPreserveTopology(geom, 0.001) AS geom_simplifiee_topo
FROM communes;
```

---

## Fonctions de test topologique

```sql
-- Les fonctions de relation spatiale utilisent toutes l'index GIST si disponible

-- ST_Within : A est entierement dans B
SELECT c.nom AS client, z.nom AS zone
FROM clients c
JOIN zones_livraison z ON ST_Within(c.geom, z.geom);

-- ST_Contains : B contient entierement A (inverse de ST_Within)
SELECT z.nom AS zone, COUNT(c.id) AS nb_clients
FROM zones_livraison z
JOIN clients c ON ST_Contains(z.geom, c.geom)
GROUP BY z.nom;

-- ST_Intersects : les geometries ont au moins un point en commun
-- Plus permissif : True si les zones se touchent ou se chevauchent
SELECT a.nom, b.nom
FROM communes a
JOIN communes b ON a.id < b.id AND ST_Intersects(a.geom, b.geom);

-- ST_Covers : comme ST_Contains mais inclut les points sur la frontiere
SELECT z.nom FROM zones z WHERE ST_Covers(z.geom, ST_MakePoint(2.3522, 48.8566));

-- ST_Overlaps : les geometries se chevauchent partiellement (meme dimension)
SELECT a.nom, b.nom
FROM zones_chalandise a
JOIN zones_chalandise b ON a.id < b.id
WHERE ST_Overlaps(a.geom, b.geom);

-- ST_Touches : les geometries se touchent mais ne se chevauchent pas
SELECT a.nom AS commune_a, b.nom AS commune_b
FROM communes a
JOIN communes b ON ST_Touches(a.geom, b.geom) AND a.id < b.id;

-- ST_Disjoint : les geometries n'ont aucun point en commun
-- ATTENTION : n'utilise pas l'index, preferer NOT ST_Intersects
SELECT c.nom FROM communes c
WHERE NOT ST_Intersects(c.geom, ST_MakePoint(2.3522, 48.8566));
```

---

## Geocodage

### Extension tiger_geocoder (US) et address_standardizer

```sql
-- Standardiser une adresse
SELECT * FROM standardize_address(
    'us_lex', 'us_gaz', 'us_rules',
    '350 Fifth Avenue, New York, NY 10118'
);

-- Geocodage complet (retourne plusieurs candidats avec rating, 0 = parfait)
SELECT g.rating, ST_X(g.geomout) AS lon, ST_Y(g.geomout) AS lat,
       (addy).address || ' ' || (addy).streetname AS adresse_normalisee
FROM geocode('350 Fifth Avenue, New York, NY 10118', 1) AS g;
```

### Integration Nominatim (OpenStreetMap) via API

```sql
-- Creer une fonction wrapper pour l'API Nominatim
CREATE OR REPLACE FUNCTION geocode_nominatim(adresse TEXT)
RETURNS GEOMETRY AS $$
DECLARE
    result JSONB;
    lon FLOAT;
    lat FLOAT;
BEGIN
    -- Utilise http extension (pg_net ou http)
    SELECT content::JSONB INTO result
    FROM http_get(
        'https://nominatim.openstreetmap.org/search?format=json&limit=1&q=' ||
        urlencode(adresse)
    );
    lon := (result->0->>'lon')::FLOAT;
    lat := (result->0->>'lat')::FLOAT;
    RETURN ST_SetSRID(ST_MakePoint(lon, lat), 4326);
END;
$$ LANGUAGE plpgsql;

-- Geocodage batch avec rate limiting (1 req/sec obligatoire Nominatim)
-- Mieux fait cote Python avec geopy, voir reference GeoPandas
```

---

## Clustering spatial SQL

```sql
-- ST_ClusterKMeans : clustering K-Means spatial
-- Retourne un identifiant de cluster pour chaque point
SELECT
    id,
    nom,
    ST_ClusterKMeans(geom, 5) OVER () AS cluster_id
FROM magasins;

-- Calculer les centroides de chaque cluster
WITH clusters AS (
    SELECT
        id, nom, geom,
        ST_ClusterKMeans(geom, 5) OVER () AS cluster_id
    FROM magasins
)
SELECT
    cluster_id,
    COUNT(*) AS nb_magasins,
    ST_Centroid(ST_Collect(geom)) AS centroide_cluster
FROM clusters
GROUP BY cluster_id;

-- ST_ClusterDBSCAN : clustering par densite (DBSCAN)
-- eps = rayon en unites du SRID, minpoints = minimum de points par cluster
SELECT
    id,
    nom,
    ST_ClusterDBSCAN(geom, eps := 0.01, minpoints := 3) OVER () AS cluster_id
    -- cluster_id = NULL signifie "bruit" (outlier)
FROM incidents;

-- Avec GEOGRAPHY (eps en metres)
WITH incidents_proj AS (
    SELECT id, nom,
        ST_Transform(ST_SetSRID(ST_MakePoint(lon, lat), 4326), 2154) AS geom_l93
    FROM incidents
)
SELECT
    id,
    ST_ClusterDBSCAN(geom_l93, eps := 500, minpoints := 5) OVER () AS cluster_id
FROM incidents_proj;
```

---

## Routing avec pgRouting

```sql
-- Prerequis : table des routes avec topologie
CREATE TABLE routes_reseau (
    id SERIAL PRIMARY KEY,
    source INTEGER,
    target INTEGER,
    cost FLOAT,       -- Cout directionnel (distance ou temps)
    reverse_cost FLOAT,
    geom GEOMETRY(LINESTRING, 4326)
);

-- Construire la topologie (cree les colonnes source/target)
SELECT pgr_createTopology('routes_reseau', 0.00001, 'geom', 'id');

-- Plus court chemin Dijkstra entre deux noeuds
SELECT r.id, r.geom, d.cost
FROM pgr_dijkstra(
    'SELECT id, source, target, cost, reverse_cost FROM routes_reseau',
    source := 42,    -- id du noeud source
    target := 1337,  -- id du noeud destination
    directed := true
) d
JOIN routes_reseau r ON r.id = d.edge;

-- A* (plus rapide que Dijkstra pour grands reseaux, necessite heuristique)
SELECT r.id, r.geom
FROM pgr_aStar(
    'SELECT id, source, target, cost, reverse_cost,
            ST_X(ST_StartPoint(geom)) AS x1,
            ST_Y(ST_StartPoint(geom)) AS y1,
            ST_X(ST_EndPoint(geom)) AS x2,
            ST_Y(ST_EndPoint(geom)) AS y2
     FROM routes_reseau',
    source := 42,
    target := 1337,
    directed := true
) d
JOIN routes_reseau r ON r.id = d.edge;

-- Catchment area (isochrone par le reseau)
-- Tous les noeuds atteignables depuis le noeud 42 avec un cout <= 10 minutes
SELECT DISTINCT r.geom
FROM pgr_drivingDistance(
    'SELECT id, source, target, cost FROM routes_reseau',
    start_vid := 42,
    distance := 10.0,
    directed := false
) d
JOIN routes_reseau r ON r.source = d.node OR r.target = d.node;

-- Enveloppe convexe de la zone atteignable
WITH atteignable AS (
    SELECT r.geom
    FROM pgr_drivingDistance(
        'SELECT id, source, target, cost FROM routes_reseau',
        42, 10.0, false
    ) d
    JOIN routes_reseau r ON r.source = d.node OR r.target = d.node
)
SELECT ST_ConvexHull(ST_Collect(geom)) AS isochrone_10min
FROM atteignable;
```

---

## Requetes complexes — Patterns de production

### 10 magasins les plus proches de chaque client

```sql
-- Pattern LATERAL : essentiel pour les top-N par groupe
SELECT
    c.id AS client_id,
    c.nom AS client,
    m.id AS magasin_id,
    m.nom AS magasin,
    ROUND(ST_Distance(c.geog, m.geog)::NUMERIC) AS distance_metres,
    m.rang
FROM clients c
CROSS JOIN LATERAL (
    SELECT
        m.id,
        m.nom,
        m.geog,
        ROW_NUMBER() OVER (ORDER BY ST_Distance(c.geog, m.geog)) AS rang
    FROM magasins m
    ORDER BY c.geog <-> m.geog   -- Operateur KNN : utilise l'index GIST
    LIMIT 10
) m
ORDER BY client_id, rang;

-- Operateur <-> : distance KNN-index (approximatif mais tres rapide)
-- Toujours utiliser <-> dans ORDER BY + LIMIT pour le nearest neighbor
SELECT m.nom, c.geog <-> m.geog AS dist_approx
FROM magasins m
ORDER BY c.geog <-> m.geog
LIMIT 5;
```

### Agregation spatiale par grille

```sql
-- Creer une grille reguliere sur une zone
SELECT
    ST_SnapToGrid(geom, 0.01) AS cellule,  -- Grille de 0.01 degres
    COUNT(*) AS nb_incidents,
    AVG(montant) AS montant_moyen
FROM incidents
GROUP BY ST_SnapToGrid(geom, 0.01)
ORDER BY nb_incidents DESC;
```

### Jointure spatiale optimisee

```sql
-- Pattern recommande : utiliser ST_DWithin plutot que ST_Intersects(ST_Buffer(...), ...)
-- MAUVAIS : cree un buffer materialise pour chaque ligne
SELECT c.nom, z.nom
FROM clients c
JOIN zones z ON ST_Intersects(ST_Buffer(c.geom, 500), z.geom);

-- BON : ST_DWithin utilise l'index nativement
SELECT c.nom, z.nom
FROM clients c
JOIN zones z ON ST_DWithin(c.geog, z.geog, 500);

-- Jointure avec ST_Within + index partiel
SELECT c.nom, dept.nom AS departement
FROM clients c
JOIN departements dept ON ST_Within(c.geom, dept.geom)
WHERE c.statut = 'actif';   -- Index partiel sur statut='actif' + geom
```

### Window functions + spatial

```sql
-- Densite de points par commune avec window function
WITH counts AS (
    SELECT
        d.nom AS commune,
        d.geom,
        COUNT(p.id) AS nb_points,
        ST_Area(d.geom::GEOGRAPHY) / 1000000 AS surface_km2
    FROM decoupages d
    LEFT JOIN points_interet p ON ST_Within(p.geom, d.geom)
    GROUP BY d.nom, d.geom
)
SELECT
    commune,
    nb_points,
    ROUND(surface_km2::NUMERIC, 2) AS surface_km2,
    ROUND((nb_points / NULLIF(surface_km2, 0))::NUMERIC, 1) AS densite_par_km2,
    NTILE(5) OVER (ORDER BY nb_points / NULLIF(surface_km2, 0)) AS quintile_densite
FROM counts
ORDER BY densite_par_km2 DESC;
```

---

## Optimisation des performances

### Materialized views et partitionnement

```sql
-- Vue materialisee pour les agregations spatiales couteuses
CREATE MATERIALIZED VIEW stats_quartiers AS
SELECT
    q.id,
    q.nom,
    q.geom,
    COUNT(c.id) AS nb_clients,
    SUM(c.chiffre_affaires) AS ca_total,
    AVG(c.chiffre_affaires) AS ca_moyen
FROM quartiers q
LEFT JOIN clients c ON ST_Within(c.geom, q.geom)
GROUP BY q.id, q.nom, q.geom;

CREATE INDEX ON stats_quartiers USING GIST (geom);
REFRESH MATERIALIZED VIEW CONCURRENTLY stats_quartiers;

-- Partitionnement par region pour tables volumineuses
CREATE TABLE incidents_partitioned (
    id BIGSERIAL,
    region TEXT,
    geom GEOMETRY(POINT, 4326),
    created_at TIMESTAMPTZ
) PARTITION BY LIST (region);

CREATE TABLE incidents_idf PARTITION OF incidents_partitioned
    FOR VALUES IN ('Ile-de-France');
CREATE TABLE incidents_aura PARTITION OF incidents_partitioned
    FOR VALUES IN ('Auvergne-Rhone-Alpes');

-- Index GIST sur chaque partition
CREATE INDEX ON incidents_idf USING GIST (geom);
CREATE INDEX ON incidents_aura USING GIST (geom);
```

### Checklist de performance PostGIS

- Toujours creer l'index GIST apres le chargement bulk des donnees
- Utiliser `ST_DWithin` au lieu de `ST_Distance < seuil`
- Utiliser l'operateur `<->` pour les requetes nearest-neighbor
- Utiliser `ST_Transform` une seule fois et stocker le resultat
- Preferer `GEOGRAPHY` pour les distances, `GEOMETRY(EPSG:2154)` pour les operations topologiques
- Executer `ANALYZE table` apres chargement de grandes quantites de donnees
- Materialiser les jointures spatiales frequentes
- Verifier `EXPLAIN ANALYZE` pour confirmer l'utilisation des index
