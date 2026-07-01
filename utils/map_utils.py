

import folium

from localtileserver import TileClient
from localtileserver import get_folium_tile_layer


def create_map():

    m = folium.Map(

        location=[28.61,77.23],

        zoom_start=10,

        tiles="CartoDB Positron"

    )

    client = TileClient(
        "rasters/HeatStress_Final_final_tiff.tiff"
    )

    layer = get_folium_tile_layer(

        client,

        opacity=0.75,

        name="Heat Stress"

    )

    layer.add_to(m)

    folium.LayerControl().add_to(m)

    return m