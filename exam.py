from PIL import Image
import rasterio
from rasterio.plot import reshape_as_image

with rasterio.open("rasters/HeatStress_Final_final_tiff.tiff") as src:
    img = reshape_as_image(src.read())

Image.fromarray(img).save("rasters/HeatStress.png")

print("Done")