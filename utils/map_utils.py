

# import folium

# from localtileserver import TileClient
# from localtileserver import get_folium_tile_layer


# def create_map():

#     m = folium.Map(

#         location=[28.61,77.23],

#         zoom_start=10,

#         tiles="CartoDB Positron"

#     )

#     # client = TileClient(
#     #     "rasters/HeatStress_Final_final_tiff.tiff"
#     # )
#     client = TileClient(
#     "rasters/HeatStress_Final_final_tiff.tiff",
#     host="127.0.0.1"
# )

#     layer = get_folium_tile_layer(

#         client,

#         opacity=0.75,

#         name="Heat Stress"

#     )

#     layer.add_to(m)

#     folium.LayerControl().add_to(m)

#     return m

# import folium

# def create_map():

#     m = folium.Map(
#         location=[28.61, 77.23],
#         zoom_start=10,
#         tiles="CartoDB Positron"
#     )

#     folium.raster_layers.ImageOverlay(
#         image="rasters/HeatStress.png",   
#         bounds=[
#             [28.1702262963843459, 76.46349547494253],
#             [29.0051119582669763, 77.6442623396051]
#         ],
#         opacity=0.75,
#         interactive=False,
#         cross_origin=False
#     ).add_to(m)

#     return m

import folium
import rasterio
from rasterio.plot import reshape_as_image

def create_map():

    m = folium.Map(
        location=[28.61,77.23],
        zoom_start=10,
        tiles="CartoDB Positron"
    )

    with rasterio.open("rasters/HeatStress_Final_final_tiff.tiff") as src:

        img = reshape_as_image(src.read())

        bounds = [
            [src.bounds.bottom, src.bounds.left],
            [src.bounds.top, src.bounds.right]
        ]

    folium.raster_layers.ImageOverlay(
        image=img,
        bounds=bounds,
        opacity=0.75,
        interactive=False
    ).add_to(m)

    return m