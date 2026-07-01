
import download_data
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import shap
import streamlit as st
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

from utils.map_utils import create_map
from utils.raster_utils import get_all_values
# Import scenario helper and new recommendation component
from utils.scenario import apply_slider_mitigation, run_batch_optimization
from utils.recommendation import generate_shap_recommendation

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="Urban Heat Intelligence Platform"
)

st.title("🌍 Urban Heat Intelligence Platform")
import os

st.write("Raster folder exists:", os.path.exists("rasters"))

if os.path.exists("rasters"):
    st.write("Contents of rasters folder:")
    st.write(os.listdir("rasters"))
st.markdown("Click anywhere on the map below to analyze local urban heat metrics.")

# ------------------------------------------------------------------
# INITIALIZE & CACHE MODELS/EXPLAINERS
# ------------------------------------------------------------------
@st.cache_resource
def load_ml_components():
    model = joblib.load("models/uhi_model.pkl")
    explainer = shap.TreeExplainer(model)
    return model, explainer

model, explainer = load_ml_components()
geolocator = Nominatim(user_agent="uhi_dashboard")

# ==================================================================
# 1. FULL WIDTH MAP SECTION
# ==================================================================
m = create_map()
output = st_folium(
    m,
    height=500,
    use_container_width=True
)

# ==================================================================
# 2. ANALYSIS & DASHBOARD OUTPUT (BELOW THE MAP)
# ==================================================================
if output and output.get("last_clicked"):
    lat = output["last_clicked"]["lat"]
    lon = output["last_clicked"]["lng"]

    # Reverse geocoding to find address
    try:
        location = geolocator.reverse((lat, lon))
        place = location.address
    except Exception:
        place = "Unknown Location"

    # Fetch environmental parameter values from raster data
    values = get_all_values(lat, lon)

    # Structure features dynamically for model input
    model_input = pd.DataFrame([{
        "NDVI": values.get("NDVI"),
        "NDBI": values.get("NDBI"),
        "NDWI": values.get("NDWI"),
        "AirTemp": values.get("Air Temperature"),
        "Humidity": values.get("Humidity"),
        "WindSpeed": values.get("Wind Speed"),
        "Albedo": values.get("Albedo"),
        "BuildingDensity": values.get("Building Density")
    }])

    # Identify precisely which columns have missing/NaN values
    missing_cols = model_input.columns[model_input.isnull().any()].tolist()

    if missing_cols:
        st.divider()
        st.error("Some raster values are missing at this location.")
        st.warning(f"⚠️ **Missing features:** {', '.join(missing_cols)}")
        
        df_partial = pd.DataFrame({
            "Parameter": list(values.keys()),
            "Value": list(values.values())
        })
        st.subheader("📊 Retrieved Environmental Parameters")
        st.dataframe(df_partial, use_container_width=True, hide_index=True)
        
    else:
        # Predict Land Surface Temperature (LST)
        predicted_lst = model.predict(model_input)[0]

        st.divider()
        
        # --------------------------------------------------------------
        # ROW 1: [Left: Location & LST] | [Right: Parameters Table]
        # --------------------------------------------------------------
        row1_left, row1_right = st.columns([1, 1], gap="large")
        
        with row1_left:
            st.header("📍 Selected Location Analysis")
            st.success(f"**Address:** {place}")
            st.caption(f"**Latitude:** {lat:.6f} | **Longitude:** {lon:.6f}")
            
            st.metric(
                label="🌡️ Predicted Surface Temperature",
                value=f"{predicted_lst:.2f} °C"
            )
            
        with row1_right:
            st.header("📋 Environmental Parameters Reference")
            
            # Prevent duplication by dropping actual LST column from metrics table if it exists
            values.pop("LST", None)

            df = pd.DataFrame({
                "Parameter": list(values.keys()),
                "Value": list(values.values())
            })
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        st.divider()

        # --------------------------------------------------------------
        # ROW 2: [Left: SHAP Text Analysis] | [Right: SHAP Graph Visual]
        # --------------------------------------------------------------
        row2_left, row2_right = st.columns([1, 1], gap="large")
        
        # Calculate local SHAP values
        shap_values = explainer.shap_values(model_input)
        
        # Convert to local lists to map out heating vs cooling factors
        contributions = []
        for feature, shap_val in zip(model_input.columns, shap_values[0]):
            contributions.append((feature, shap_val, model_input[feature].values[0]))
            
        # Sort by absolute impact
        contributions.sort(key=lambda x: abs(x[1]), reverse=True)
        
        with row2_left:
            st.header("🧬 Local SHAP Analysis (Drivers)")
            
            sub_heat, sub_cool = st.columns(2)
            with sub_heat:
                st.markdown("#### 🔥 Top Heating Drivers")
                for feat, val, raw in contributions:
                    if val > 0:
                        st.write(f"• **{feat}**: +{val:.2f}°C *(value: {raw:.2f})*")
                        
            with sub_cool:
                st.markdown("#### ❄️ Top Cooling Factors")
                for feat, val, raw in contributions:
                    if val < 0:
                        st.write(f"• **{feat}**: {val:.2f}°C *(value: {raw:.2f})*")
                        
        with row2_right:
            st.header("📊 Contribution Matrix")
            
            fig, ax = plt.subplots(figsize=(7, 4.5))
            
            features_sorted = [x[0] for x in contributions[::-1]]
            values_sorted = [x[1] for x in contributions[::-1]]
            colors = ['#ff4b4b' if x > 0 else '#0068c9' for x in values_sorted]
            
            ax.barh(features_sorted, values_sorted, color=colors)
            ax.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
            ax.set_xlabel("SHAP Value (Net Impact on LST in °C)")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.tight_layout()
            
            st.pyplot(fig)
            plt.close()




        # ==============================================================
        # ROW 3: SCENARIO INTERVENTIONS & OPTIMIZATION MATRIX WITH SHAP RECOMMENDATIONS
        # ==============================================================
        st.divider()
        st.header("🛠️ Scenario-Based Cooling Intervention Simulator")
        
        # 1. Render the dynamic SHAP recommendation blueprint box
        verdict_text, slider_hints = generate_shap_recommendation(contributions)
        st.info(verdict_text)
        
        if slider_hints != [0, 0, 0]:
            st.caption(f"💡 **AI Target Prescription Hint:** Shift sliders below toward **Tree Cover: {slider_hints[0]}%** | **Water: {slider_hints[1]}%** | **Cool Roofs: {slider_hints[2]}%** to maximize efficiency.")
            
        st.write("")
        
        # Slider Adjustment Controls
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            tree_cover = st.slider("Increase Tree Cover / Vegetation (%)", 0, 50, 0, 5)
        with s_col2:
            water_bodies = st.slider("Expand Surface Water Networks (%)", 0, 20, 0, 2)
        with s_col3:
            cool_roofs = st.slider("Retrofit Cool Roofs / Albedo Impact (%)", 0, 100, 0, 10)
            
        st.write("")
        
        # Split Results Evaluation Display Layout
        row3_left, row3_right = st.columns([1, 1], gap="large")
        
        with row3_left:
            st.subheader("⚙️ Active Sandbox Output")
            
            # Apply matrix changes via utility module
            model_simulated = apply_slider_mitigation(model_input, tree_cover, water_bodies, cool_roofs)
            simulated_pred = model.predict(model_simulated)[0]
            net_cooling = simulated_pred - predicted_lst
            
            st.metric(
                label="Simulated Land Temperature", 
                value=f"{simulated_pred:.2f} °C", 
                delta=f"{net_cooling:.2f} °C",
                delta_color="inverse"
            )
            
            if abs(net_cooling) >= 0.05:
                st.success(f"✨ Custom configuration lowers local surface temperatures by **{abs(net_cooling):.2f}°C**.")
            else:
                st.info("🔼 Use the landscape sliders above to build an intervention configuration strategy.")
                
        with row3_right:
            st.subheader("🏆 Strategy Optimization Ranking")
            
            # Batch calculate predefined framework metrics 
            opt_df = run_batch_optimization(model, model_input)
            st.dataframe(opt_df, use_container_width=True, hide_index=True)
            
            top_strategy = opt_df.iloc[0]["Strategy"]
            top_drop = opt_df.iloc[0]["Reduction (Δ °C)"]
            st.success(f"**Recommendation Summary:** Deploying **{top_strategy}** provides the best localized performance targeting, reducing heat metrics by **{top_drop}°C**.")

else:
    st.info("💡 Click anywhere inside the map domain to trigger the Urban Heat analysis pipeline.")

