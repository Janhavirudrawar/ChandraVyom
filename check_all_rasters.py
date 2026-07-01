import os
# import rasterio

folder = r"aligned"   # change if your rasters are elsewhere

print("=" * 110)
print(f"{'FILE':30} {'WIDTH':>8} {'HEIGHT':>8} {'PIXEL SIZE':>18} {'CRS':>25}")
print("=" * 110)

# for file in sorted(os.listdir(folder)):
#     if file.endswith(".tif"):
#         path = os.path.join(folder, file)

#         try:
#             with rasterio.open(path) as src:
#                 print(
#                     f"{file:30}"
#                     f"{src.width:8}"
#                     f"{src.height:8}"
#                     f"{str(src.res):>18}"
#                     f"{str(src.crs):>25}"
#                 )

#         except Exception as e:
#             print(file, e)

import rasterio

with rasterio.open(r"rasters/Predicted_LST_Clipped.tif") as src:
    print("Width:", src.width)
    print("Height:", src.height)
    print("CRS:", src.crs)
    print("Resolution:", src.res)