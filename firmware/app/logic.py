def clamp(value, low, high):
    return max(low, min(high, value))


def soil_percent(raw_value, dry_value, wet_value):
    if dry_value == wet_value:
        raise ValueError("dry_value and wet_value must differ")

    span = dry_value - wet_value
    percent = ((dry_value - raw_value) / span) * 100
    return round(clamp(percent, 0, 100), 1)


def needs_water(soil_pct, threshold_pct):
    if soil_pct is None:
        return None
    return soil_pct <= threshold_pct


def build_payload(soil_pct, temperature_c, humidity_pct, light_lux, threshold_pct):
    return {
        "soil_moisture_percent": soil_pct,
        "temperature_c": temperature_c,
        "humidity_percent": humidity_pct,
        "light_lux": light_lux,
        "needs_water": needs_water(soil_pct, threshold_pct),
    }
