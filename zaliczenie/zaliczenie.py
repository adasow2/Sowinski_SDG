# %%
import geopandas as gpd
import pandas as pd
from statistics import mean
from shapely import get_num_coordinates
import numpy as np
from pathlib import Path

folder = Path.cwd() / 'dane'

# %%
# stworzenie listy plików
file_list = [file for file in folder.iterdir() if file.suffix == '.shp']
layers = {file.stem[-6:]: gpd.read_file(str(file)) for file in file_list}

# %%
# stworzenie pustego df
summary_df = pd.DataFrame({
    'layer': [],
    'geom_type': [],
    'obj_num': [],
    'mean_area':[],
    'mean_len': [],
    'mean_complex': [],
    'mean_fill': []
})
# %%
def calc_complexity(layer:gpd.GeoDataFrame):
    num_coords = get_num_coordinates(layer.geometry).to_numpy()
    length = layer.length.to_numpy()
    mean_complexity = np.mean(num_coords / length)
    return mean_complexity

def calc_fill(layer: gpd.GeoDataFrame):
    bbx_area = float(layer.dissolve().envelope.area[0])
    np_area = (
        layer.copy()
        .assign(area= lambda x: x.area / bbx_area)
        ['area']
        .to_numpy()
    )
    fill = np.mean(np_area)
    return fill

# %%
for name, layer in layers.items():
    row = {
        'layer': name,
        'geom_type': layer.geom_type[0],
        'obj_num': len(layer),
        'mean_area':pd.NA,
        'mean_len': pd.NA,
        'mean_complex': pd.NA,
        'mean_fill': pd.NA
    }
    match row['geom_type']:
        case 'Polygon':
            row['mean_area'] = mean(layer.area)
            row['mean_fill'] = calc_fill(layer)

        case 'LineString':
            row['mean_len'] = mean(layer.length)
            row['mean_complex'] = calc_complexity(layer)

    summary_df.loc[len(summary_df)] = row

# %%
output = str(folder.parent / 'zaliczenie.csv')
summary_df.to_csv(output)
