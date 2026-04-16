try:
    from .config import BH1750_I2C_ADDR, SOIL_ADC_PIN, DHT_PIN, I2C_SCL_PIN, I2C_SDA_PIN
    from .logic import soil_percent
except ImportError:
    from config import BH1750_I2C_ADDR, SOIL_ADC_PIN, DHT_PIN, I2C_SCL_PIN, I2C_SDA_PIN
    from logic import soil_percent

try:
    from machine import ADC, Pin, I2C
    import dht
except ImportError:
    ADC = Pin = I2C = None
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


class DHT22Sensor:
    def __init__(self, sensor=None):
        if sensor is not None:
            self.sensor = sensor
        elif dht is not None and Pin is not None:
            self.sensor = dht.DHT22(Pin(DHT_PIN))
        else:
            self.sensor = None

    def read(self):
        if self.sensor is None:
            raise RuntimeError("DHT22 unavailable")
        self.sensor.measure()
        return self.sensor.temperature(), self.sensor.humidity()


class BH1750Sensor:
    POWER_ON = b'\x01'
    CONT_H_RES_MODE = b'\x10'

    def __init__(self, i2c=None, address=BH1750_I2C_ADDR):
        self.address = address
        if i2c is not None:
            self.i2c = i2c
        elif I2C is not None and Pin is not None:
            self.i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
        else:
            self.i2c = None

    def read_lux(self):
        if self.i2c is None:
            raise RuntimeError("I2C unavailable")
        self.i2c.writeto(self.address, self.POWER_ON)
        self.i2c.writeto(self.address, self.CONT_H_RES_MODE)
        data = self.i2c.readfrom(self.address, 2)
        raw = (data[0] << 8) | data[1]
        return round(raw / 1.2, 1)
