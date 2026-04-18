try:
    from .config import SOIL_DRY, SOIL_WET, WATER_THRESHOLD_PERCENT
    from .logic import build_payload
    from .sensors import SoilMoistureSensor, DHT11Sensor, PhotoresistorSensor
except ImportError:
    from config import SOIL_DRY, SOIL_WET, WATER_THRESHOLD_PERCENT
    from logic import build_payload
    from sensors import SoilMoistureSensor, DHT11Sensor, PhotoresistorSensor


def read_all_sensors():
    soil_sensor = SoilMoistureSensor(SOIL_DRY, SOIL_WET)
    climate_sensor = DHT11Sensor()
    light_sensor = PhotoresistorSensor()

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
