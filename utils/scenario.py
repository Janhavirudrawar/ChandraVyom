import numpy as np
import pandas as pd

# Define standard macro intervention baseline constants
INTERVENTION_PROFILES = {
    "Urban Greening (Tree Canopy & Parks)": {
        "NDVI": 0.25, "NDBI": -0.15, "NDWI": 0.05, "Albedo": -0.02, "BuildingDensity": -5.0,
        "AirTemp": 0.0, "Humidity": 2.0, "WindSpeed": -0.2
    },
    "Cool Roofs & High-Albedo Surfaces": {
        "NDVI": 0.0, "NDBI": 0.0, "NDWI": 0.0, "Albedo": 0.30, "BuildingDensity": 0.0,
        "AirTemp": 0.0, "Humidity": 0.0, "WindSpeed": 0.0
    },
    "Blue Infrastructure (Retention Basins)": {
        "NDVI": -0.05, "NDBI": -0.10, "NDWI": 0.40, "Albedo": -0.05, "BuildingDensity": -8.0,
        "AirTemp": 0.0, "Humidity": 4.0, "WindSpeed": 0.1
    }
}

def apply_slider_mitigation(base_df, tree_cover, water_bodies, cool_roofs):
    """Applies slider adjustments scaled to your actual multi-feature layout."""
    sim_df = base_df.copy()
    
    # Extract baseline points safely
    ndvi = base_df["NDVI"].values[0]
    ndbi = base_df["NDBI"].values[0]
    ndwi = base_df["NDWI"].values[0]
    albedo = base_df["Albedo"].values[0]
    b_density = base_df["BuildingDensity"].values[0]
    
    # Mathematical scalar transformations
    sim_df["NDVI"] = np.clip(ndvi + (tree_cover / 100) * 0.4, -1.0, 1.0)
    sim_df["NDWI"] = np.clip(ndwi + (water_bodies / 100) * 0.5, -1.0, 1.0)
    sim_df["NDBI"] = np.clip(ndbi - (tree_cover + water_bodies) / 200, -1.0, 1.0)
    sim_df["Albedo"] = np.clip(albedo + (cool_roofs / 100) * 0.35, 0.0, 1.0)
    sim_df["BuildingDensity"] = np.clip(b_density - (tree_cover * 0.2), 0.0, 100.0)
    
    return sim_df

def run_batch_optimization(model, base_df):
    """Evaluates and ranks all preset profiles for your specific architecture."""
    results = []
    base_pred = model.predict(base_df)[0]
    
    for name, profile in INTERVENTION_PROFILES.items():
        sim_df = base_df.copy()
        for col in base_df.columns:
            if col in profile:
                # Direct uniform intensity scaling
                if col == "BuildingDensity":
                    sim_df[col] = np.clip(sim_df[col] + profile[col], 0.0, 100.0)
                elif col in ["AirTemp", "Humidity", "WindSpeed"]:
                    sim_df[col] = sim_df[col] + profile[col]
                else:
                    sim_df[col] = np.clip(sim_df[col] + profile[col], -1.0, 1.0)
                    
        sim_pred = model.predict(sim_df)[0]
        results.append({
            "Strategy": name,
            "Simulated LST (°C)": round(sim_pred, 2),
            "Reduction (Δ °C)": round(base_pred - sim_pred, 2)
        })
        
    return pd.DataFrame(results).sort_values(by="Reduction (Δ °C)", ascending=False)