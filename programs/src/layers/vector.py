from . import state
import geopandas as gpd
from dataclasses import dataclass

@dataclass
class VectorLayer:
    name:str
    crs:str
    geometry: str
    df:gpd.GeoDataFrame

    @staticmethod
    def load_vector(path:str):
        gdf = gpd.read_file(path)
        layer_name = path.split('/')[-1]
        vec = VectorLayer(
            name=layer_name,
            crs=gdf.crs.to_string(),
            geometry=gdf.geom_type.iloc[0],
            df=gdf
        )
        state.active_layers[f"{state.layers_id}"] = vec
        state.layers_id += 1
        print(*state.active_layers.keys(), sep='\n')
