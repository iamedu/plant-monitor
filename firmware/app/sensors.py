try:
    from .config import LIGHT_ADC_PIN, LIGHT_BRIGHT, LIGHT_DARK, SOIL_ADC_PIN, DHT_PIN
    from .logic import clamp, soil_percent
except ImportError:
    from config import LIGHT_ADC_PIN, LIGHT_BRIGHT, LIGHT_DARK, SOIL_ADC_PIN, DHT_PIN
    from logic import clamp, soil_percent

try:
    from machine import ADC, Pin
    import dht
except ImportError:
    ADC = Pin = None
    dht = None


class SoilMoistureSensor:
    def __init__(self, dry_value, wet_value, adc=None):
        self.dry_value = dry_value
        self.wet_value = wet_value
        if adc is not None:
            self.adc = adc
        elif ADC is not None and Pin is not None:
            self.adc = ADC(Pin(SOIL_ADC_PIN))
            if hasattr(self.adc, "atten"):
                self.adc.atten(ADC.ATTN_11DB)
        else:
            self.adc = None

    def read_raw(self):
        if self.adc is None:
            raise RuntimeError("ADC unavailable")
        return self.adc.read()

    def read_percent(self):
        return soil_percent(self.read_raw(), self.dry_value, self.wet_value)


class DHT11Sensor:
    def __init__(self, sensor=None):
        if sensor is not None:
            self.sensor = sensor
        elif dht is not None and Pin is not None:
            self.sensor = dht.DHT11(Pin(DHT_PIN))
        else:
            self.sensor = None

    def read(self):
        if self.sensor is None:
            raise RuntimeError("DHT11 unavailable")
        self.sensor.measure()
        return self.sensor.temperature(), self.sensor.humidity()


class PhotoresistorSensor:
    def __init__(self, dark_value=LIGHT_DARK, bright_value=LIGHT_BRIGHT, adc=None):
        self.dark_value = dark_value
        self.bright_value = bright_value
        if adc is not None:
            self.adc = adc
        elif ADC is not None and Pin is not None:
            self.adc = ADC(Pin(LIGHT_ADC_PIN))
            if hasattr(self.adc, "atten"):
                self.adc.atten(ADC.ATTN_11DB)
        else:
            self.adc = None

    def read_raw(self):
        if self.adc is None:
            raise RuntimeError("Light ADC unavailable")
        return self.adc.read()

    def read_lux(self):
        raw = self.read_raw()
        span = self.dark_value - self.bright_value
        if span == 0:
            raise ValueError("light calibration values must differ")
        pct = ((self.dark_value - raw) / span) * 100
        pct = round(clamp(pct, 0, 100), 1)
        return round((pct / 100) * 1000, 1)
