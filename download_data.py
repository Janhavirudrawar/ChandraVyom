import os
import zipfile
import gdown

FILE_ID = "1qjKTfCeARm-rbNxn6CTmkyVw4Xk2y5VW"

ZIP_NAME = "rasters.zip"

if not os.path.exists("rasters"):

    print("Downloading rasters...")

    gdown.download(
        f"https://drive.google.com/uc?id={FILE_ID}",
        ZIP_NAME,
        quiet=False
    )

    print("Extracting...")

    with zipfile.ZipFile(ZIP_NAME, "r") as zip_ref:
        zip_ref.extractall(".")

    print("Finished.")