import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

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
# FEATURES
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
# SHAP EXPLAINER
# ==================================

explainer = shap.TreeExplainer(model)

print("Calculating SHAP values...")

shap_values = explainer.shap_values(X)

print("Done!")

# ==================================
# GLOBAL SHAP SUMMARY
# ==================================

plt.figure(figsize=(10, 6))

shap.summary_plot(
    shap_values,
    X,
    show=False
)

plt.savefig(
    "models/shap_summary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("SHAP Summary Plot Saved!")

# ==================================
# FEATURE IMPORTANCE BAR PLOT
# ==================================

plt.figure(figsize=(8, 6))

shap.summary_plot(
    shap_values,
    X,
    plot_type="bar",
    show=False
)

plt.savefig(
    "models/shap_importance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("SHAP Importance Plot Saved!")

# ==================================
# SAVE SHAP VALUES
# ==================================

shap_df = pd.DataFrame(
    shap_values,
    columns=X.columns
)

shap_df.to_csv(
    "models/shap_values.csv",
    index=False
)

print("SHAP Values CSV Saved!")

print("\nTop Features (Mean |SHAP|):")

# importance = shap_df.abs().mean().sort_values(ascending=False)

# print(importance)

importance = shap_df.abs().mean().sort_values(ascending=False)

weights = importance / importance.sum()

print("\nNormalized SHAP Weights")
print(weights)

weights.to_csv("models/shap_weights.csv")