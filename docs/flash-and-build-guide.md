# Plant Monitor Build and Flash Guide

## Current repo state

Repo looks healthy and simple right now.

Update: firmware has now been adapted to your actual kit parts:
- DHT11
- analog photoresistor
- ESP32-S3 flash script added at `scripts/flash.sh`

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
- ESP32-S3
- capacitive soil sensor
- DHT11 from the kit
- photoresistor from the kit
- OLED display planned later

The firmware has now been updated to match that hardware.

## Recommended build order

1. Confirm which ESP32-S3 serial port appears on your Mac
2. Flash MicroPython to the board
3. Copy firmware files to the board
4. Open the serial REPL
5. Test each sensor one by one
6. Calibrate the soil moisture values
7. Only then finalize the build in the enclosure or permanent breadboard layout

## Step 1: connect the board

Plug the ESP32-S3 into your Mac with a USB-C data cable.

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

## Step 3: download MicroPython for ESP32-S3

Use the ESP32-S3 firmware from MicroPython:

- https://micropython.org/download/ESP32-S3/

Download the latest stable `.bin` file.

Example filename:

```bash
ESP32_GENERIC_S3-20250415-v1.24.1.bin
```

Save it somewhere easy, for example:

```bash
~/Downloads/ESP32_GENERIC_S3.bin
```

## Step 4: erase and flash the board

Replace `/dev/cu.usbmodemXXXX` with your actual port.

### Erase flash

```bash
python3 -m esptool --chip esp32s3 --port /dev/cu.usbmodemXXXX erase_flash
```

### Write MicroPython

```bash
python3 -m esptool --chip esp32s3 --port /dev/cu.usbmodemXXXX --baud 460800 write_flash -z 0 ~/Downloads/ESP32_GENERIC_S3.bin
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

After downloading a MicroPython ESP32-S3 binary, you can do the whole process with:

```bash
cd /Users/iamedu/.openclaw/workspace/plant-monitor
./scripts/flash.sh /dev/cu.usbmodemXXXX ~/Downloads/ESP32_GENERIC_S3.bin
```

## Step 6: copy the current firmware

From repo root:

```bash
cd /Users/iamedu/.openclaw/workspace/plant-monitor
```

Copy the app folder:

```bash
mpremote connect /dev/cu.usbmodemXXXX fs cp -r firmware/app :
```

Copy main entrypoint:

```bash
mpremote connect /dev/cu.usbmodemXXXX fs cp firmware/app/main.py :main.py
```

Soft reset the board:

```bash
mpremote connect /dev/cu.usbmodemXXXX reset
```

## Step 7: wiring expectations

Right now the firmware expects:
- `DHT11Sensor`
- `PhotoresistorSensor`

That now matches your actual kit.

## Step 8: recommended wiring plan for your actual kit

### Minimal first successful bring-up
Start with just:
- ESP32-S3
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

Current placeholders in `firmware/app/config.py`:

```python
SOIL_DRY = 3200
SOIL_WET = 1400
```

These are not guaranteed to match your actual sensor.

### Calibration process
1. Read raw soil value in fully dry air
2. Read raw value in fully wet soil or water
3. Update config values

Example target:

```python
SOIL_DRY = <your dry reading>
SOIL_WET = <your wet reading>
```

Then percent calculation becomes meaningful.

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
1. Flash MicroPython to ESP32-S3
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
