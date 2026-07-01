import pandas as pd

def generate_shap_recommendation(contributions):
    """
    Dynamically decodes local feature SHAP contributions to engineer 
    a tailored, physics-informed mitigation recommendation.
    
    Parameters:
    -----------
    contributions : list of tuples
        Expected format: [(feature_name, shap_value, raw_value), ...]
        
    Returns:
    --------
    tuple : (verdict_text, slider_hints)
    """
    # Extract only the features actively driving up the localized microclimate temperature
    heating_drivers = [feat for feat, val, raw in contributions if val > 0]
    
    if not heating_drivers:
        return (
            "🎯 **AI Prescriptive Optimization:** No severe heating anomalies detected at this target coordinate. Local urban indices are thermodynamically stable. Maintain existing canopy density.",
            [0, 0, 0]
        )
    
    # Identify the highest magnitude thermal driver
    top_driver = heating_drivers[0]
    
    if top_driver in ["BuildingDensity", "NDBI"]:
        verdict = (
            f"🎯 **AI Prescriptive Optimization Strategy (High Built Density):** "
            f"The ML infrastructure identifies **{top_driver}** as the primary driver behind surface temperature elevation here. "
            f"The spatial morphology indicates heavy structural artificial heat capture. Prioritize deploying **High-Albedo Cool Roof coatings** "
            f"and light reflective pavements to lower solar radiation absorption."
        )
        hints = [10, 0, 75]  # [Tree Cover, Water Networks, Cool Roofs]
        
    elif top_driver in ["NDVI", "AirTemp"]:
        verdict = (
            f"🎯 **AI Prescriptive Optimization Strategy (Canopy Deficit):** "
            f"The system targets **{top_driver}** as the most critical localized heating factor. "
            f"The coordinate is experiencing suppressed evapotranspiration potential due to low vegetation scaling. Prioritize intensive "
            f"**Urban Greening frameworks**, immediate tree canopy row implementation, and green micro-corridors."
        )
        hints = [45, 0, 15]
        
    elif top_driver in ["NDWI", "Humidity"]:
        verdict = (
            f"🎯 **AI Prescriptive Optimization Strategy (Hydrological Deficit):** "
            f"The engine indicates severe environmental dryness tracking back to **{top_driver}**. "
            f"Introducing targeted **Blue Infrastructure units**—such as stormwater collection ponds, urban bioswales, or public architectural fountains—"
            f"will maximize immediate local cooling via latent heat assimilation."
        )
        hints = [15, 25, 10]
        
    else:
        verdict = "🎯 **AI Prescriptive Optimization Strategy:** Multi-driver thermal spike present. Distribute structural interventions evenly across balancing dimensions."
        hints = [20, 10, 20]
        
    return verdict, hints