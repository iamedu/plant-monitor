# Plant Monitor Build and Flash Guide

## Current repo state

Repo looks healthy and simple right now.

Update: firmware has now been adapted to your actual kit parts:
- DHT11
- analog photoresistor
- ESP32 flash script added at `scripts/flash.sh`

### What is already in place
- MicroPython firmware scaffold exists in `firmware/app/`
- Unit tests pass locally, 9/9 passing
- Wiring diagrams exist:
  - `docs/wiring-diagram.png`
  - `docs/breadboard-diagram.png`
- Main firmware entrypoint exists at `firmware/app/main.py`
- Config is in `firmware/app/config.py`

### Current firmware assumptions
The code is currently written for:
- **Soil sensor** on ADC pin **34**
- **DHT22** on GPIO **4**
- **BH1750 light sensor** on I2C SDA **21** / SCL **22**

### Hardware now matched to your actual kit
From your parts list and memory, your real kit is:
- ESP32
- capacitive soil sensor
- DHT11 from the kit
- photoresistor from the kit
- OLED display planned later

The firmware has now been updated to match that hardware.

### Current tested pin map
- `SOIL_ADC_PIN = 15`
- `DHT_PIN = 4`
- `LIGHT_ADC_PIN = 2`

This pin map keeps all sensor wiring on one side of Edu's ESP32 board.
Note: GPIO 5 was tested and is invalid on Edu's board.

## Recommended build order

1. Confirm which ESP32 serial port appears on your Mac
2. Flash MicroPython to the board
3. Copy firmware files to the board
4. Open the serial REPL
5. Test each sensor one by one
6. Calibrate the soil moisture values
7. Only then finalize the build in the enclosure or permanent breadboard layout

## Step 1: connect the board

Plug the ESP32 into your Mac with a USB data cable.

Then list serial devices:

```bash
ls /dev/tty.*
ls /dev/cu.*
```

You are looking for something like:

```bash
/dev/cu.usbmodemXXXX
```

If nothing new appears:
- try a different cable
- try a different USB port
- make sure it is a data cable, not charge-only

## Step 2: install flashing tools

On your Mac:

```bash
python3 -m pip install --upgrade esptool mpremote
```

If `esptool` is not on PATH, use:

```bash
python3 -m esptool
```

## Step 3: download MicroPython for ESP32

Use the ESP32 generic firmware from MicroPython:

- https://micropython.org/download/ESP32_GENERIC/

Download the latest stable `.bin` file.

Example filename:

```bash
ESP32_GENERIC-20250415-v1.24.1.bin
```

Save it somewhere easy, for example:

```bash
~/Downloads/ESP32_GENERIC.bin
```

## Step 4: erase and flash the board

Replace `/dev/cu.usbmodemXXXX` with your actual port.

### Erase flash

```bash
python3 -m esptool --chip esp32 --port /dev/cu.usbserial-XXXX erase_flash
```

### Write MicroPython

```bash
python3 -m esptool --chip esp32 --port /dev/cu.usbserial-XXXX --baud 115200 write_flash -z 0x1000 ~/Downloads/ESP32_GENERIC.bin
```

If the board does not enter bootloader mode automatically:
- hold **BOOT**
- tap **RESET**
- release **BOOT**
- run the flash command again

## Step 5: verify MicroPython is alive

Open REPL:

```bash
mpremote connect /dev/cu.usbmodemXXXX repl
```

You should see a MicroPython prompt like:

```python
>>>
```

Exit with:

```text
Ctrl-X
```

## One-command flash option

After downloading a MicroPython ESP32 binary, you can do the whole process with:

```bash
cd /Users/iamedu/.openclaw/workspace/plant-monitor
./scripts/flash.sh /dev/cu.usbmodemXXXX ~/Downloads/ESP32_GENERIC.bin
```

## Step 6: copy the current firmware

The flash script handles this automatically. If you need to copy files manually, use a single chained mpremote session (multiple `mpremote connect` calls fail due to the board's raw REPL state):

```bash
APP=firmware/app
mpremote connect /dev/cu.usbserial-XXXX \
  fs mkdir app + \
  fs cp "$APP/__init__.py"    :app/__init__.py + \
  fs cp "$APP/config.py"      :app/config.py + \
  fs cp "$APP/logic.py"       :app/logic.py + \
  fs cp "$APP/main.py"        :app/main.py + \
  fs cp "$APP/sensors.py"     :app/sensors.py + \
  fs cp "$APP/wifi.py"        :app/wifi.py + \
  fs cp "$APP/uploader.py"    :app/uploader.py + \
  fs cp "$APP/credentials.py" :app/credentials.py + \
  fs cp firmware/main.py      :main.py + \
  reset
```

## Step 7: wiring expectations

Right now the firmware expects:
- `DHT11Sensor`
- `PhotoresistorSensor`

That now matches your actual kit.

## Step 8: recommended wiring plan for your actual kit

### Minimal first successful bring-up
Start with just:
- ESP32
- soil moisture sensor
- DHT11

Leave the light sensor and OLED for later.

That gets you to a working first version faster.

### Suggested staged approach

#### Stage A: board only
- flash MicroPython
- verify REPL works

#### Stage B: soil sensor only
- wire soil sensor VCC, GND, analog output
- confirm raw ADC values change in dry vs wet soil

#### Stage C: add DHT11
- wire data pin with correct GPIO
- confirm temperature and humidity reads work

#### Stage D: adapt light sensor code
- wire photoresistor as analog input with voltage divider
- replace BH1750 code path

#### Stage E: add OLED
- after core sensing is stable

## Step 9: soil calibration

Calibration constants live in **`server/config.py`** (not firmware). The ESP32 sends raw ADC values; the server does the conversion. To recalibrate, edit `server/config.py` and restart the server — no reflash needed.

```python
SOIL_DRY = 2962   # raw ADC reading in dry conditions
SOIL_WET = 2485   # raw ADC reading in wet conditions
WATER_THRESHOLD_PERCENT = 30
```

### Calibration process
1. Connect ESP32 via USB and open a REPL: `mpremote connect /dev/cu.usbserial-0001 exec "..."`
2. Read raw ADC with WiFi **off** (ADC2 conflict — see note below):
   ```python
   import machine, network
   network.WLAN(network.STA_IF).active(False)
   adc = machine.ADC(machine.Pin(15))
   adc.atten(machine.ADC.ATTN_11DB)
   print(adc.read())
   ```
3. Read in dry conditions → set `SOIL_DRY`
4. Read in wet conditions → set `SOIL_WET`
5. Edit `server/config.py` and restart the server

### ADC2 / WiFi conflict

GPIO 2 (light) and GPIO 15 (soil) are ADC2 pins. The ESP32's WiFi radio shares ADC2, so readings return 0 when WiFi is active. The firmware reads sensors **before** connecting WiFi each cycle to work around this. A permanent fix is rewiring sensors to ADC1 pins (GPIO 32–39).

## Step 10: useful commands while building

### Run tests locally on Mac

```bash
cd /Users/iamedu/.openclaw/workspace/plant-monitor/firmware
python3 -m unittest discover -s tests -v
```

### List files on board

```bash
mpremote connect /dev/cu.usbmodemXXXX fs ls
```

### Remove and recopy a file

```bash
mpremote connect /dev/cu.usbmodemXXXX fs rm main.py
mpremote connect /dev/cu.usbmodemXXXX fs cp firmware/app/main.py :main.py
```

### Open serial output

```bash
mpremote connect /dev/cu.usbmodemXXXX repl
```

## What I recommend you do next

### Fastest path to first success
1. Flash MicroPython to ESP32
2. Confirm REPL works
3. Run `./scripts/flash.sh ...`
4. Wire soil sensor + DHT11 first
5. Test sensor readings
6. Add photoresistor
7. Calibrate soil and light values

## Bottom line

You **can flash the board now** and the repo now matches your actual parts much more closely.

### Repo status summary
- project structure: good
- tests: passing
- flash path: ready
- hardware-specific code: adapted for DHT11 and photoresistor

Next likely step after flashing is soil and light calibration.
