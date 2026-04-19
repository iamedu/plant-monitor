def clamp(value, low, high):
    return max(low, min(high, value))


def soil_percent(raw, dry, wet):
    if dry == wet:
        raise ValueError("dry and wet values must differ")
    pct = ((dry - raw) / (dry - wet)) * 100
    return round(clamp(pct, 0, 100), 1)


def light_lux(raw, dark, bright):
    span = dark - bright
    if span == 0:
        raise ValueError("light calibration values must differ")
    pct = ((dark - raw) / span) * 100
    return round((clamp(pct, 0, 100) / 100) * 1000, 1)


def needs_water(soil_pct, threshold):
    if soil_pct is None:
        return None
    return soil_pct <= threshold
