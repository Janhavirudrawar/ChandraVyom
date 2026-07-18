# 🌍 Urban Heat Intelligence Platform

An AI-powered Decision Support System for Urban Heat Island (UHI) assessment, hotspot identification, explainable AI analysis, and scenario-based cooling intervention planning.

Developed using satellite-derived geospatial datasets, machine learning, SHAP explainability, and ecosystem-based cooling analysis.

---

# 🚀 Features

## 🗺️ Interactive Spatial Dashboard

- Click any location on the map
- Automatically retrieves raster values
- Displays location details
- Predicts Land Surface Temperature (LST)

---

## 🌡️ AI-Based LST Prediction

Predicts Land Surface Temperature using an XGBoost regression model trained on environmental variables.

Input Features:

- NDVI
- NDBI
- NDWI
- Air Temperature
- Humidity
- Wind Speed
- Albedo
- Building Density

Output:

- Predicted Land Surface Temperature

---

## 🧠 Explainable AI (SHAP)

Every prediction is explained using SHAP values.

Displays:

- Top Heating Drivers
- Top Cooling Factors
- Feature Contribution Graph
- Local Feature Importance

---

## 🌿 Nature-Based Cooling Assessment

Integrated ecosystem service indicators derived from InVEST outputs.

Displays:

- Cooling Capacity
- Heat Mitigation
- Air Temperature
- Cooling Potential Classification
- Nature-Based Intervention Recommendations

---

## 🛠️ Scenario Simulator

Users can simulate multiple mitigation strategies.

Adjust:

- Tree Cover
- Water Bodies
- Cool Roof Adoption

The dashboard dynamically predicts:

- Updated LST
- Cooling Improvement
- Best Intervention Strategy

---

# 📂 Project Structure

```
ISRO/

│
├── app.py
├── train.py
├── utils/
│   ├── map_utils.py
│   ├── raster_utils.py
│   ├── scenario.py
│   └── recommendation.py
│
├── rasters/
│   ├── Predicted_LST_Clipped11.tif
│   ├── HeatStress_Final_final_tiff.tiff
│   ├── Final_NDVI_Delhi.tif
│   ├── Final_NDBI_Delhi.tif
│   ├── Final_NDWI_Delhi.tif
│   ├── Final_AirTemp_Delhi.tif
│   ├── Final_Humidity_Delhi.tif
│   ├── Final_WindSpeed_Delhi.tif
│   ├── Final_Albedo_Delhi.tif
│   ├── Final_BuildingDensity_Delhi.tif
│   ├── cc.tif
│   ├── hm.tif
│   └── air_temperature.tif
│
├── models/
│   ├── uhi_model.pkl
│   ├── feature_importance.csv
│   ├── shap_values.csv
│   ├── shap_weights.csv
│   └── predictions.csv
│
├── solweig/
└── README.md
```

---

# ⚙️ Technologies Used

## Programming

- Python

## Machine Learning

- XGBoost
- SHAP

## GIS & Remote Sensing

- Rasterio
- Folium
- LocalTileServer
- GeoPandas
- QGIS

## Dashboard

- Streamlit
- Streamlit-Folium

## Scientific Computing

- NumPy
- Pandas
- Matplotlib

---

# 📊 Workflow

```
Satellite Data
        │
        ▼
Raster Processing
        │
        ▼
Interactive Map
        │
        ▼
Location Selection
        │
        ▼
Raster Value Extraction
        │
        ▼
XGBoost Prediction
        │
        ▼
SHAP Explanation
        │
        ▼
InVEST Cooling Assessment
        │
        ▼
Scenario Simulator
        │
        ▼
Updated Temperature Prediction
        │
        ▼
Decision Support Recommendations
```

---

# 🧪 Machine Learning Model

Model:

- XGBoost Regressor

Target Variable:

- Land Surface Temperature (LST)

Training Features:

- NDVI
- NDBI
- NDWI
- Air Temperature
- Humidity
- Wind Speed
- Albedo
- Building Density

Evaluation Metrics

- R² Score
- MAE
- RMSE

---

# 🌿 Nature-Based Solutions

The dashboard recommends interventions such as:

- Urban Forestry
- Green Roofs
- Water Bodies
- Green Corridors
- Cool Roof Technologies
- Vegetation Expansion

---

# 🖥️ Installation

Clone the repository

```bash
git clone <repository-url>
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
streamlit run app.py
```

---

# 🎯 Future Scope

- Real-time weather integration
- Google Earth Engine connectivity
- SOLWEIG microclimate simulation
- Multi-city support
- Time-series heat forecasting
- Urban planning recommendation engine
- AI chatbot for decision support

---

# 👥 Team
This project has been developed as a GeoAI‑based climate‑tech innovation and is submitted for evaluation under Idea Hackathon 6.0.


---

# 📜 License

This project is intended for academic and research purposes.
