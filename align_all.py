import os
import rasterio
from rasterio.warp import reproject, Resampling

input_folder = "rasters"
output_folder = "aligned"

os.makedirs(output_folder, exist_ok=True)

master = os.path.join(input_folder, "Predicted_LST_Clipped.tif")

with rasterio.open(master) as ref:

    dst_crs = ref.crs
    dst_transform = ref.transform
    dst_width = ref.width
    dst_height = ref.height

    for file in os.listdir(input_folder):

        if not file.endswith(".tif"):
            continue

        if file == "Predicted_LST_Clipped.tif":
            continue

        src_path = os.path.join(input_folder, file)
        out_path = os.path.join(output_folder, file)

        with rasterio.open(src_path) as src:

            kwargs = src.meta.copy()

            kwargs.update({
                "crs": dst_crs,
                "transform": dst_transform,
                "width": dst_width,
                "height": dst_height
            })

            with rasterio.open(out_path, "w", **kwargs) as dst:

                for i in range(1, src.count + 1):

                    reproject(
                        source=rasterio.band(src, i),
                        destination=rasterio.band(dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=dst_transform,
                        dst_crs=dst_crs,
                        resampling=Resampling.bilinear
                    )

        print(file, "Done")