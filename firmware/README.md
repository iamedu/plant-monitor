# Firmware

First version of the Plant Monitor firmware for ESP32 using MicroPython.

## Features
- Reads soil moisture from an analog capacitive sensor
- Reads temperature and humidity from a DHT11
- Reads ambient light from a photoresistor over analog input
- Produces a normalized sensor payload
- Supports threshold-based water-needed detection

## Folder layout
- `app/` core firmware modules
- `tests/` unit tests for logic that can run on desktop Python

## Hardware assumptions
- ESP32
- Capacitive soil moisture sensor on ADC pin 34
- DHT11 data pin on GPIO 4
- Photoresistor on ADC pin 32 via voltage divider

## Build / install

### 1. Flash MicroPython to the ESP32
Example with `esptool.py` and `mpremote` installed:

```bash
brew install esptool
pip3 install mpremote
```

Then erase and flash the board with a current ESP32 MicroPython image.

### 2. Copy firmware files to the board
From the repo root:

```bash
mpremote connect auto fs cp -r firmware/app :
mpremote connect auto fs cp firmware/app/main.py :main.py
```

### 3. Configure pins and calibration
Edit `firmware/app/config.py` before copying if your wiring differs.

The calibration defaults are placeholders:
- `SOIL_DRY = 3200`
- `SOIL_WET = 1400`
- `LIGHT_DARK = 4095`
- `LIGHT_BRIGHT = 1500`

You should recalibrate after wiring your actual sensor.

## Running tests
These tests run on your Mac with desktop Python:

```bash
cd firmware
python3 -m unittest discover -s tests -v
```

## Notes
This first version focuses on sensor logic and clean structure. Network upload, deep sleep, and dashboard integration can come next.
