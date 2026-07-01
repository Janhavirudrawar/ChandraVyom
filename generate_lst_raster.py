import rasterio
from rasterio.windows import Window
import numpy as np
import joblib

# =====================================================
# CONFIGURATION
# =====================================================

MODEL_PATH = "models/uhi_model.pkl"

INPUT_RASTER = "data/Delhi_Prediction_Input1.tif"

OUTPUT_RASTER = "outputs/Predicted_LST.tif"

# Window size
WINDOW_SIZE = 512

# =====================================================
# LOAD TRAINED MODEL
# =====================================================

print("\nLoading trained model...")

model = joblib.load(MODEL_PATH)

print("Model Loaded Successfully!")

# =====================================================
# OPEN INPUT RASTER
# =====================================================

with rasterio.open(INPUT_RASTER) as src:

    profile = src.profile.copy()

    width = src.width
    height = src.height
    bands = src.count

    print("\nRaster Information")
    print("---------------------------")
    print("Width :", width)
    print("Height:", height)
    print("Bands :", bands)

    # Output raster profile
    profile.update(
        dtype=rasterio.float32,
        count=1,
        compress="lzw"
    )

    with rasterio.open(OUTPUT_RASTER, "w", **profile) as dst:

        # =====================================================
        # LOOP OVER WINDOWS
        # =====================================================

        for row in range(0, height, WINDOW_SIZE):

            for col in range(0, width, WINDOW_SIZE):

                window = Window(
                    col_off=col,
                    row_off=row,
                    width=min(WINDOW_SIZE, width-col),
                    height=min(WINDOW_SIZE, height-row)
                )

                # --------------------------------------------
                # Read all bands
                # Shape:
                # (bands, rows, cols)
                # --------------------------------------------

                data = src.read(window=window)

                b, r, c = data.shape

                # Convert into
                # (pixels , bands)

                pixels = data.reshape(b, -1).T

                # --------------------------------------------
                # Handle NaN pixels
                # --------------------------------------------

                valid_mask = np.all(np.isfinite(pixels), axis=1)

                predictions = np.full(
                    pixels.shape[0],
                    np.nan,
                    dtype=np.float32
                )

                if np.any(valid_mask):

                    valid_pixels = pixels[valid_mask]

                    pred = model.predict(valid_pixels)

                    predictions[valid_mask] = pred.astype(np.float32)

                # --------------------------------------------
                # Convert back to image
                # --------------------------------------------

                prediction_image = predictions.reshape(r, c)

                # --------------------------------------------
                # Write window
                # --------------------------------------------

                dst.write(
                    prediction_image,
                    1,
                    window=window
                )

print("\n=====================================")
print("Prediction Completed Successfully!")
print("Output Saved As:")
print(OUTPUT_RASTER)
print("=====================================")