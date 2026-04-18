import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.logic import build_payload
from app.sensors import DHT11Sensor, PhotoresistorSensor, SoilMoistureSensor


class FakeADC:
    def __init__(self, value):
        self.value = value

    def read(self):
        return self.value


class FakeDHT:
    def measure(self):
        return None

    def temperature(self):
        return 22.5

    def humidity(self):
        return 48.0


class FakeLightADC:
    def __init__(self, value):
        self.value = value

    def read(self):
        return self.value


class SensorTests(unittest.TestCase):
    def test_soil_sensor_percent(self):
        sensor = SoilMoistureSensor(3200, 1400, adc=FakeADC(2300))
        self.assertEqual(sensor.read_percent(), 50.0)

    def test_dht_sensor_read(self):
        sensor = DHT11Sensor(sensor=FakeDHT())
        self.assertEqual(sensor.read(), (22.5, 48.0))

    def test_photoresistor_read_lux(self):
        sensor = PhotoresistorSensor(dark_value=0, bright_value=2360, adc=FakeLightADC(1180))
        self.assertEqual(sensor.read_lux(), 500.0)

    def test_build_payload_without_soil_sensor(self):
        payload = build_payload(
            soil_pct=None,
            temperature_c=22.5,
            humidity_pct=48.0,
            light_lux=500.0,
            threshold_pct=30,
        )
        self.assertIsNone(payload["soil_moisture_percent"])
        self.assertIsNone(payload["needs_water"])


if __name__ == "__main__":
    unittest.main()
