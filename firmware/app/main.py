try:
    from .config import SOIL_DRY, SOIL_WET, WATER_THRESHOLD_PERCENT
    from .logic import build_payload
    from .sensors import SoilMoistureSensor, DHT22Sensor, BH1750Sensor
except ImportError:
    from config import SOIL_DRY, SOIL_WET, WATER_THRESHOLD_PERCENT
    from logic import build_payload
    from sensors import SoilMoistureSensor, DHT22Sensor, BH1750Sensor


def read_all_sensors():
    soil_sensor = SoilMoistureSensor(SOIL_DRY, SOIL_WET)
    climate_sensor = DHT22Sensor()
    light_sensor = BH1750Sensor()

    soil_pct = soil_sensor.read_percent()
    temperature_c, humidity_pct = climate_sensor.read()
    light_lux = light_sensor.read_lux()

    return build_payload(
        soil_pct=soil_pct,
        temperature_c=temperature_c,
        humidity_pct=humidity_pct,
        light_lux=light_lux,
        threshold_pct=WATER_THRESHOLD_PERCENT,
    )


if __name__ == "__main__":
    print(read_all_sensors())
