import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
        sensor = PhotoresistorSensor(dark_value=4095, bright_value=1595, adc=FakeLightADC(2845))
        self.assertEqual(sensor.read_lux(), 500.0)


if __name__ == "__main__":
    unittest.main()
