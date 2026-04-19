try:
    from .config import SOIL_DRY, SOIL_WET, WATER_THRESHOLD_PERCENT
    from .logic import build_payload
    from .sensors import SoilMoistureSensor, DHT11Sensor, PhotoresistorSensor
except ImportError:
    from config import SOIL_DRY, SOIL_WET, WATER_THRESHOLD_PERCENT
    from logic import build_payload
    from sensors import SoilMoistureSensor, DHT11Sensor, PhotoresistorSensor


def read_all_sensors(include_soil=True):
    soil_sensor = SoilMoistureSensor(SOIL_DRY, SOIL_WET) if include_soil else None
    climate_sensor = DHT11Sensor()
    light_sensor = PhotoresistorSensor()

    soil_pct = soil_sensor.read_percent() if soil_sensor is not None else None
    temperature_c, humidity_pct = climate_sensor.read()
    light_lux = light_sensor.read_lux()

    return build_payload(
        soil_pct=soil_pct,
        temperature_c=temperature_c,
        humidity_pct=humidity_pct,
        light_lux=light_lux,
        threshold_pct=WATER_THRESHOLD_PERCENT,
    )


def run_loop(interval_s=300):
    import time
    try:
        from .wifi import connect
        from .uploader import post_reading
        from .credentials import WIFI_SSID, WIFI_PASSWORD, SERVER_URL
    except ImportError:
        from wifi import connect
        from uploader import post_reading
        from credentials import WIFI_SSID, WIFI_PASSWORD, SERVER_URL

    connect(WIFI_SSID, WIFI_PASSWORD)
    while True:
        payload = read_all_sensors(include_soil=True)
        post_reading(SERVER_URL, payload)
        time.sleep(interval_s)


if __name__ == "__main__":
    print(read_all_sensors())
