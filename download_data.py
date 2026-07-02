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

import os
import zipfile
import shutil
import gdown

FILE_ID = "1qjKTfCeARm-rbNxn6CTmkyVw4Xk2y5VW"
ZIP_NAME = "rasters.zip"

# Check for one raster that MUST exist
required_file = "rasters/Final_NDVI_Delhi.tif"   # <-- change this to the exact filename in your ZIP

if not os.path.exists(required_file):

    print("Downloading rasters...")

    # Remove incomplete rasters folder if it exists
    if os.path.exists("rasters"):
        shutil.rmtree("rasters")

    gdown.download(
        f"https://drive.google.com/uc?id={FILE_ID}",
        ZIP_NAME,
        quiet=False
    )

    print("Extracting...")

    with zipfile.ZipFile(ZIP_NAME, "r") as zip_ref:
        zip_ref.extractall(".")

    os.remove(ZIP_NAME)

    print("Finished.")