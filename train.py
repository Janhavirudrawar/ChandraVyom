import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

from xgboost import XGBRegressor

# ==================================
# LOAD DATASET
# ==================================

df = pd.read_csv("data/Delhi_UHI_Training_Data_Final.csv")

print("Dataset Shape:", df.shape)

# ==================================
# REMOVE UNUSED COLUMNS
# ==================================

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
# TARGET
# ==================================

y = df["LST"]

# ==================================
# TRAIN TEST SPLIT
# ==================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Samples:", len(X_train))
print("Testing Samples :", len(X_test))

# ==================================
# XGBOOST MODEL
# ==================================

model = XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    random_state=42
)

# ==================================
# PHYSICS INFORMED VERSION (OPTIONAL)
# ==================================

# constraints = (
#     -1,   # NDVI
#      1,   # NDBI
#     -1,   # NDWI
#      1,   # AirTemp
#     -1,   # Humidity
#     -1,   # WindSpeed
#     -1,   # Albedo
#      1    # BuildingDensity
# )
#
# model = XGBRegressor(
#     n_estimators=300,
#     max_depth=6,
#     learning_rate=0.05,
#     random_state=42,
#     monotone_constraints=constraints
# )

print("\nTraining Started...")

model.fit(X_train, y_train)

print("Training Completed!")

# ==================================
# PREDICTIONS
# ==================================

preds = model.predict(X_test)

# ==================================
# EVALUATION
# ==================================

r2 = r2_score(y_test, preds)

mae = mean_absolute_error(y_test, preds)

rmse = mean_squared_error(
    y_test,
    preds
) ** 0.5

print("\n===== MODEL PERFORMANCE =====")
print("R² Score :", round(r2, 4))
print("MAE      :", round(mae, 4))
print("RMSE     :", round(rmse, 4))

# ==================================
# FEATURE IMPORTANCE
# ==================================

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\n===== FEATURE IMPORTANCE =====")
print(importance)

importance.to_csv(
    "models/feature_importance.csv",
    index=False
)

# ==================================
# SAVE MODEL
# ==================================

joblib.dump(
    model,
    "models/uhi_model.pkl"
)

print("\nModel Saved Successfully!")

# ==================================
# CREATE PREDICTION CSV
# ==================================

results = pd.DataFrame({
    "Actual_LST": y_test.values,
    "Predicted_LST": preds
})

results["Error"] = (
    results["Actual_LST"]
    - results["Predicted_LST"]
)

results.to_csv(
    "models/predictions.csv",
    index=False
)

print("\nPredictions CSV Saved!")
print(results.head(10))