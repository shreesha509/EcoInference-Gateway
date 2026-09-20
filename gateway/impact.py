import random

# Power consumption by component (Watts)
GPU_POWER_WATTS = 350.0
CPU_RAM_POWER_WATTS = 150.0
INFERENCE_POWER_WATTS = GPU_POWER_WATTS + CPU_RAM_POWER_WATTS

# Data center efficiency
PUE = 1.3  # Power Usage Effectiveness (1.0 = perfect, typical modern DC: 1.1-1.5)
TOTAL_SYSTEM_POWER_WATTS = INFERENCE_POWER_WATTS * PUE

# Water usage (liters per kWh of IT load)
WUE_LITERS_PER_KWH = 1.2  # Global average for evaporative cooling

# CO2 emissions (kg CO2 per kWh - global grid average)
CO2_KG_PER_KWH = 0.42

# Realistic inference time range (seconds) for image generation models
MIN_INFERENCE_TIME = 5.0
MAX_INFERENCE_TIME = 30.0


def calculate_impact(inference_time_seconds: float) -> dict:
    """
    Estimate total environmental impact of a single inference request.

    Includes GPU + CPU/RAM power, data center cooling overhead (PUE),
    water consumption for cooling, and CO2 emissions.
    """

    energy_joules = TOTAL_SYSTEM_POWER_WATTS * inference_time_seconds
    energy_kwh = energy_joules / 3_600_000

    water_liters = energy_kwh * WUE_LITERS_PER_KWH
    water_ml = water_liters * 1000

    co2_kg = energy_kwh * CO2_KG_PER_KWH
    co2_grams = co2_kg * 1000

    return {
        "inference_time_seconds": round(inference_time_seconds, 1),
        "system_power_watts": round(TOTAL_SYSTEM_POWER_WATTS, 1),
        "pue": PUE,
        "energy_joules": round(energy_joules, 1),
        "energy_kwh": round(energy_kwh, 6),
        "water_ml": round(water_ml, 1),
        "co2_grams": round(co2_grams, 2),
    }


def estimate_inference_time() -> float:
    """
    Simulate a realistic inference time based on typical image
    generation model performance (5-30 seconds).
    """
    return random.uniform(MIN_INFERENCE_TIME, MAX_INFERENCE_TIME)
