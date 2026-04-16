import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.logic import build_payload, needs_water, soil_percent


class SoilLogicTests(unittest.TestCase):
    def test_soil_percent_maps_midpoint(self):
        self.assertEqual(soil_percent(2300, 3200, 1400), 50.0)

    def test_soil_percent_clamps_high(self):
        self.assertEqual(soil_percent(1000, 3200, 1400), 100)

    def test_soil_percent_clamps_low(self):
        self.assertEqual(soil_percent(4000, 3200, 1400), 0)

    def test_soil_percent_rejects_zero_span(self):
        with self.assertRaises(ValueError):
            soil_percent(2000, 2000, 2000)

    def test_needs_water(self):
        self.assertTrue(needs_water(25, 30))
        self.assertFalse(needs_water(31, 30))

    def test_build_payload(self):
        payload = build_payload(28.5, 21.3, 55.2, 123.4, 30)
        self.assertEqual(payload["soil_moisture_percent"], 28.5)
        self.assertTrue(payload["needs_water"])
        self.assertEqual(payload["light_lux"], 123.4)


if __name__ == "__main__":
    unittest.main()
