

import math
import numpy as np
import rasterio

rasters = {
    "LST": "rasters/Predicted_LST_Clipped11.tif",
    "Heat Stress": "rasters/HeatStress_Final_final_tiff.tiff",
    "NDVI": "rasters/Final_NDVI_Delhi.tif",
    "NDBI": "rasters/Final_NDBI_Delhi.tif",
    "NDWI": "rasters/Final_NDWI_Delhi.tif",
    "Air Temperature": "rasters/Final_AirTemp_Delhi.tif",
    "Humidity": "rasters/Final_Humidity_Delhi.tif",
    "Wind Speed": "rasters/Final_WindSpeed_Delhi.tif",
    "Albedo": "rasters/Final_Albedo_Delhi.tif",
    "Building Density": "rasters/Final_BuildingDensity_Delhi.tif",
    "Cooling Capacity": "rasters/cc.tif",
    "Heat Mitigation": "rasters/hm.tif",
    "Invest Air Temp": "rasters/air_temperature.tif"

}

def read_value(path, lat, lon):
    try:
        with rasterio.open(path) as src:
            # src.index expects (longitude, latitude) for standard EPSG:4326
            row, col = src.index(lon, lat)
            
            # Boundary check
            if row < 0 or col < 0 or row >= src.height or col >= src.width:
                return None
            
            value = src.read(1)[row, col]
            
            # Catch standard Python/Numpy NaN values
            if np.isnan(value) or math.isnan(value):
                return None
                
            # Catch file-defined NoData values
            if src.nodata is not None and value == src.nodata:
                return None
                
            return float(value)
    except Exception:
        return None

def get_all_values(lat, lon):
    values = {}
    for key, path in rasters.items():
        values[key] = read_value(path, lat, lon)
    return values