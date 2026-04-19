try:
    from .config import SOIL_DRY, SOIL_WET
    from .sensors import SoilMoistureSensor, DHT11Sensor, PhotoresistorSensor
except ImportError:
    from config import SOIL_DRY, SOIL_WET
    from sensors import SoilMoistureSensor, DHT11Sensor, PhotoresistorSensor


def read_all_sensors(include_soil=True):
    soil_sensor = SoilMoistureSensor(SOIL_DRY, SOIL_WET) if include_soil else None
    climate_sensor = DHT11Sensor()
    light_sensor = PhotoresistorSensor()

    soil_raw = soil_sensor.read_raw() if soil_sensor is not None else None
    temperature_c, humidity_pct = climate_sensor.read()
    light_raw = light_sensor.read_raw()

    return {
        "soil_moisture_raw": soil_raw,
        "temperature_c": temperature_c,
        "humidity_percent": humidity_pct,
        "light_raw": light_raw,
    }


def run_loop(interval_s=300):
    import time
    try:
        from .wifi import connect, disconnect
        from .uploader import post_reading
        from .credentials import WIFI_SSID, WIFI_PASSWORD, SERVER_URL
    except ImportError:
        from wifi import connect, disconnect
        from uploader import post_reading
        from credentials import WIFI_SSID, WIFI_PASSWORD, SERVER_URL

    while True:
        payload = read_all_sensors(include_soil=True)
        connect(WIFI_SSID, WIFI_PASSWORD)
        post_reading(SERVER_URL, payload)
        disconnect()
        time.sleep(interval_s)


if __name__ == "__main__":
    print(read_all_sensors())
