import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.sensors import BH1750Sensor, DHT22Sensor, SoilMoistureSensor


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


class FakeI2C:
    def __init__(self, raw_bytes):
        self.raw_bytes = raw_bytes
        self.writes = []

    def writeto(self, address, data):
        self.writes.append((address, data))

    def readfrom(self, address, count):
        return self.raw_bytes


class SensorTests(unittest.TestCase):
    def test_soil_sensor_percent(self):
        sensor = SoilMoistureSensor(3200, 1400, adc=FakeADC(2300))
        self.assertEqual(sensor.read_percent(), 50.0)

    def test_dht_sensor_read(self):
        sensor = DHT22Sensor(sensor=FakeDHT())
        self.assertEqual(sensor.read(), (22.5, 48.0))

    def test_bh1750_read_lux(self):
        fake_i2c = FakeI2C(bytes([0x01, 0x2C]))
        sensor = BH1750Sensor(i2c=fake_i2c)
        self.assertEqual(sensor.read_lux(), 250.0)
        self.assertEqual(len(fake_i2c.writes), 2)


if __name__ == "__main__":
    unittest.main()
