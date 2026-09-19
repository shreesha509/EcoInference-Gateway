GPU_POWER_WATTS = 350.0
WUE_LITERS_PER_KWH = 1.8


def calculate_impact(execution_time_seconds: float) -> dict:
    """
    Estimate GPU energy consumption and associated cooling-water impact.

    Assumptions:
    - GPU power: 350 W
    - WUE: 1.8 L/kWh
    """

    energy_joules = GPU_POWER_WATTS * execution_time_seconds

    energy_kwh = energy_joules / 3_600_000

    water_liters = energy_kwh * WUE_LITERS_PER_KWH

    water_ml = water_liters * 1000

    return {
        "execution_time_seconds": execution_time_seconds,
        "gpu_power_watts": GPU_POWER_WATTS,
        "energy_joules": round(energy_joules, 2),
        "energy_kwh": round(energy_kwh, 6),
        "estimated_water_liters": round(water_liters, 6),
        "estimated_water_ml": round(water_ml, 2),
    }


def calculate_savings(
    standard_execution_time_seconds: float,
    eco_execution_time_seconds: float,
) -> dict:
    """
    Calculate estimated energy and water savings between
    standard and EcoInference execution.
    """

    standard = calculate_impact(standard_execution_time_seconds)
    eco = calculate_impact(eco_execution_time_seconds)

    energy_saved_joules = (
        standard["energy_joules"] - eco["energy_joules"]
    )

    water_saved_ml = (
        standard["estimated_water_ml"]
        - eco["estimated_water_ml"]
    )

    return {
        "standard": standard,
        "eco": eco,
        "energy_saved_joules": round(energy_saved_joules, 2),
        "water_saved_ml": round(water_saved_ml, 2),
    }