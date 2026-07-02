# import os
# import zipfile
# import gdown

# FILE_ID = "1qjKTfCeARm-rbNxn6CTmkyVw4Xk2y5VW"

# ZIP_NAME = "rasters.zip"

# if not os.path.exists("rasters"):

#     print("Downloading rasters...")

#     gdown.download(
#         f"https://drive.google.com/uc?id={FILE_ID}",
#         ZIP_NAME,
#         quiet=False
#     )

#     print("Extracting...")

#     with zipfile.ZipFile(ZIP_NAME, "r") as zip_ref:
#         zip_ref.extractall(".")

#     print("Finished.")

# import os
# import zipfile
# import shutil
# import gdown

# FILE_ID = "1qjKTfCeARm-rbNxn6CTmkyVw4Xk2y5VW"
# ZIP_NAME = "rasters.zip"

# # Check for one raster that MUST exist
# required_file = "rasters/Final_NDVI_Delhi.tif"   # <-- change this to the exact filename in your ZIP

# if not os.path.exists(required_file):

#     print("Downloading rasters...")

#     # Remove incomplete rasters folder if it exists
#     if os.path.exists("rasters"):
#         shutil.rmtree("rasters")

#     gdown.download(
#         f"https://drive.google.com/uc?id={FILE_ID}",
#         ZIP_NAME,
#         quiet=False
#     )

#     print("Extracting...")

#     with zipfile.ZipFile(ZIP_NAME, "r") as zip_ref:
#         zip_ref.extractall(".")

#     os.remove(ZIP_NAME)

#     print("Finished.")

# import os
# import zipfile
# import shutil
# import gdown

# FILE_ID = "1qjKTfCeARm-rbNxn6CTmkyVw4Xk2y5VW"
# ZIP_NAME = "rasters.zip"

# # Delete existing rasters folder
# if os.path.exists("rasters"):
#     shutil.rmtree("rasters")

# print("Downloading rasters...")

# gdown.download(
#     f"https://drive.google.com/uc?id={FILE_ID}",
#     ZIP_NAME,
#     quiet=False
# )

# print("Extracting rasters...")

# with zipfile.ZipFile(ZIP_NAME, "r") as zip_ref:
#     zip_ref.extractall(".")

# print("Files after extraction:")

# for root, dirs, files in os.walk("."):
#     print(root)
#     for file in files:
#         print("   ", file)

# os.remove(ZIP_NAME)

# print("Finished.")

# import os
# import zipfile
# import shutil
# import gdown

# FILE_ID = "1be8RqoukXlXdoleB7EN-9dWok60U2GnS"
# ZIP_NAME = "rasters.zip"

# if os.path.exists("rasters"):
#     shutil.rmtree("rasters")

# print("Downloading rasters...")

# gdown.download(
#     id=FILE_ID,
#     output=ZIP_NAME,
#     fuzzy=True
# )

# print("Extracting rasters...")

# with zipfile.ZipFile(ZIP_NAME, "r") as zip_ref:
#     zip_ref.extractall(".")

# os.remove(ZIP_NAME)

# print("Finished.")

import os
import gdown

# Create the rasters directory if it doesn't exist
if not os.path.exists("rasters"):
    os.makedirs("rasters")

# Map your local filenames EXACTLY to their Google Drive File IDs from your WinRAR screenshot
RASTER_DOWNLOADS = {
    "hm.tif": "1m-4CDQc2D7ZtYHBfpa1RCtQacjuol-0h",
    "cc.tif": "13ia8KvlMVXWfA5ohA7hmptsge6AHziqn",
    "T_air.tif": "1BQ8tzy593JdAXbBVC24khj0Inz-ofL5Y",
    "Final_Albedo_Delhi.tif": "1d8mRZQZk2lYrqTPP3RIYNMi5xQQ-N7MU",
    "Final_Humidity_Delhi.tif": "1jutkST2GYW0XbdUDiiEdtGRHlSuOCnyv",
    "Final_WindSpeed_Delhi.tif": "1sDEDwAi3lW5HYGdEkiKuzQhIjyfuLsGM",
    "Final_AirTemp_Delhi.tif": "1DFH3_dBNR_TDUNiWuFs1lxVYqGQrPamd",
    "Final_NDVI_Delhi.tif": "1cTPdQlVbMAfFri9V9xtASA9voSHGU3DC",
    "Final_NDBI_Delhi.tif": "1tM6ihoRkMrB7las6Hkuxe35KZ71iCpNB",
    "Final_NDWI_Delhi.tif": "10CEZwQGyBu4bMKkI66fxVm-2voih7x-2",
    "HeatStress_Final_final_tiff.tiff": "1r_esrZcNijUoSkSruPkxESeoO_dXLisW",
    "Final_BuildingDensity_Delhi.tif": "1x61OqfrivMdmzgutbGfpsTjxnxbue_a0",
    
    # Your PNG file from the screenshot
    "HeatStress.png": "1iBZ1Q3XO6OKleKPpZpLlNs2aYrwHxr75"
}

print("Checking for missing geospatial data layers...")

for filename, file_id in RASTER_DOWNLOADS.items():
    destination_path = os.path.join("rasters", filename)
    
    # Download the file ONLY if it doesn't exist locally
    if not os.path.exists(destination_path):
        print(f"Downloading missing layer: {filename}...")
        url = f"https://drive.google.com/uc?id={file_id}"
        try:
            gdown.download(url, destination_path, quiet=True)
        except Exception as e:
            print(f"Failed to download {filename}: {e}")

print("All asset layers are up to date.")