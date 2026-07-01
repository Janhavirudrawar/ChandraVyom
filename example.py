import rasterio

with rasterio.open(r"outputs/Predicted_LST.tif") as src:
    print("CRS:", src.crs)
    print("Width:", src.width)
    print("Height:", src.height)
    print("Resolution:", src.res)