import pandas as pd
import joblib
import shap

# ==================================
# LOAD DATASET
# ==================================

df = pd.read_csv("data/Delhi_UHI_Training_Data_Final.csv")

# Remove unnecessary columns
df = df.drop(
    columns=[
        "system:index",
        ".geo"
    ],
    errors="ignore"
)

# ==================================
# INPUT FEATURES
# ==================================

X = df[
    [
        "NDVI",
        "NDBI",
        "NDWI",
        "AirTemp",
        "Humidity",
        "WindSpeed",
        "Albedo",
        "BuildingDensity"
    ]
]

# ==================================
# LOAD TRAINED MODEL
# ==================================

model = joblib.load("models/uhi_model.pkl")

# ==================================
# CREATE SHAP EXPLAINER
# ==================================

explainer = shap.TreeExplainer(model)

# ==================================
# SELECT PIXEL
# Change this number to test
# different locations
# ==================================

pixel_index = 100

selected_pixel = X.iloc[[pixel_index]]

# ==================================
# PREDICT LST
# ==================================

prediction = model.predict(selected_pixel)[0]

print("\n" + "=" * 60)
print("LOCAL SHAP ANALYSIS")
print("=" * 60)

print(f"\nSelected Pixel Index : {pixel_index}")
print(f"Predicted LST        : {prediction:.2f} °C")

# ==================================
# SHOW INPUT VALUES
# ==================================

print("\nInput Features")
print("-" * 60)

for feature in selected_pixel.columns:
    print(f"{feature:<18}: {selected_pixel.iloc[0][feature]:.4f}")

# ==================================
# CALCULATE SHAP VALUES
# ==================================

shap_values = explainer.shap_values(selected_pixel)

# ==================================
# STORE CONTRIBUTIONS
# ==================================

contributions = []

for feature, value in zip(
    selected_pixel.columns,
    shap_values[0]
):
    contributions.append(
        (feature, value)
    )

# Sort by absolute contribution
contributions.sort(
    key=lambda x: abs(x[1]),
    reverse=True
)

# ==================================
# DISPLAY CONTRIBUTIONS
# ==================================

print("\nFeature Contributions")
print("-" * 60)

for feature, value in contributions:

    if value > 0:
        effect = "Heating ↑"
    else:
        effect = "Cooling ↓"

    print(
        f"{feature:<18}"
        f"{value:>10.3f}    "
        f"{effect}"
    )

# ==================================
# TOP HEATING FACTORS
# ==================================

print("\nTop Heat Drivers")
print("-" * 60)

for feature, value in contributions:

    if value > 0:
        print(f"• {feature:<18} +{value:.3f}")

# ==================================
# TOP COOLING FACTORS
# ==================================

print("\nTop Cooling Factors")
print("-" * 60)

for feature, value in contributions:

    if value < 0:
        print(f"• {feature:<18} {value:.3f}")

print("\n" + "=" * 60)
print("Analysis Complete")
print("=" * 60)