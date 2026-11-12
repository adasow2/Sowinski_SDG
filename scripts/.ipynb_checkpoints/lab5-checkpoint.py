# %%
from IPython.core.display_functions import display
import geopandas as gpd
from shapely import Point, LineString, Polygon
from pathlib import Path

# %%
"""
1. Stwórz warstwę liniową, która po wyświetleniu będzie zawierała pierwsze 3 drukowane litery Twojego
imienia i pierwsze 3 drukowane litery Twojego nazwiska. Każda literka powinna być osobnym rekordem w GeoDataFrame.
Wyeksportuj te dane i wyświetl w QGIS.

2. Z danych o wyspach stwórz słownik, gdzie kluczem będą nazwy krajów a wartością lista
geometrii wysp do nich przypisanych. Następnie stwórz ranking top 10 krajów które mają największą sumaryczną
powierzchnię wysp w m2

3. Z danych o wyspach stwórz nowy GeoDataFrame zawierający tylko wyspy należące do Japonii.
Przeprowadź dla nich 3 wizualizacje różniące się poziomem uproszczenia geometrii.
Dla każdego poziomu wypisz: ilość krawędzi (linii) oraz ilość wierzchołków (punktów) z których się składa
"""

# %% wczytywanie danych
wyspy = gpd.read_file(r"C:\Users\sowin\Desktop\semsetr_5\sdg\Sowinski_SDG\scripts\data\wyspy\fw2.geojson")

# %% zadanie 1
a1 = LineString([
    (0, 0),
    (4, 10),
    (8, 0),
    (6.2, 4.5),
    (1.8, 4.5)
])

d = LineString([
    (10, 0),
    (10, 10),
    (15, 8),
    (15, 2),
    (10, 0)
])

a2 = LineString([
    (17, 0),
    (21, 10),
    (25, 0),
    (23.2, 4.5),
    (18.8, 4.5)
])
s = LineString([
    (31, 0),
    (34, 4),
    (31, 7),
    (34, 10)
])

o = LineString([
    (40, 0),
    (43, 2.5),
    (43, 7.5),
    (40, 10),
    (37, 7.5),
    (37, 2.5),
    (40, 0)
])

w = LineString([
    (45, 10),
    (48, 0),
    (50, 8),
    (52, 0),
    (55, 10)
])

gdf = gpd.GeoDataFrame(
    {
        "name": ["Linia A", "Linia D", "Linia A2", "Linia S", "Linia O", "Linia W"]
    },
    geometry=[a1, d, a2, s, o, w],
    crs="EPSG:2180"
)
gdf.to_file(r"C:\Users\sowin\Desktop\semsetr_5\sdg\Sowinski_SDG\scripts\imie.gpkg")


# %% zadanie 2
"""
2. Z danych o wyspach stwórz słownik, gdzie kluczem będą nazwy krajów a wartością lista
geometrii wysp do nich przypisanych. Następnie stwórz ranking top 10 krajów które mają największą sumaryczną
powierzchnię wysp w m2
"""

wyspy.to_crs("EPSG:2180", inplace=True)
wyspy_dict = wyspy.groupby('państwo')['geometry'].apply(list).to_dict()
wyspy_dict = {name: gpd.GeoSeries(geoms).area.sum() for name, geoms in wyspy_dict.items()}
top_10 = sorted(wyspy_dict.items(), key=lambda x: x[1], reverse=True)[:10]

for n, v in top_10:
    print(f"{n}: {v} m2")


# %% zadanie 3
"""
3. Z danych o wyspach stwórz nowy GeoDataFrame zawierający tylko wyspy należące do Japonii.
Przeprowadź dla nich 3 wizualizacje różniące się poziomem uproszczenia geometrii.
Dla każdego poziomu wypisz: ilość krawędzi (linii) oraz ilość wierzchołków (punktów) z których się składa
"""

wyspy_jap = wyspy[wyspy['państwo'] == 'Japonia'].to_crs('EPSG:4326')
wyspy_jap.simplify(0.5).plot()


# %%
wyspy.to_crs(epsg=3857, inplace=True)

wyspy['area'] = list(wyspy.geometry.area / 1e6)

# %%
wyspy
