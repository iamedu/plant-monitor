# Plant Monitor

An ESP32-based plant monitor that reads soil moisture, temperature, humidity, and light every 5 minutes and uploads readings over WiFi to a local web server. A live dashboard shows history charts and flags when a plant needs watering.

## How it works

```
ESP32 (MicroPython)
  └── reads sensors every 5 min (DHT11, photoresistor, soil moisture)
  └── POSTs raw ADC values to Mac server over WiFi

Mac (FastAPI + SQLite, runs as launchd service)
  └── POST /readings  → computes soil%, light lux, needs_water → stores to DB
  └── GET /readings   → returns recent readings as JSON
  └── GET /           → live dashboard (Chart.js)
```

Computation (soil %, light lux, needs_water threshold) happens on the server using calibration constants in `server/config.py`. To recalibrate, edit that file and restart the service — no reflash needed.

## Project layout

```
firmware/
  app/
    config.py       # pin assignments and sensor calibration values
    sensors.py      # hardware drivers (DHT11, photoresistor, soil ADC)
    logic.py        # pure math functions (soil_percent, needs_water, etc.)
    main.py         # read_all_sensors() and run_loop()
    wifi.py         # WiFi connect/disconnect
    uploader.py     # HTTP POST via urequests
    credentials.py  # WiFi SSID/password + server URL (gitignored)
  main.py           # boot entry point — calls run_loop()
  tests/            # desktop unit tests (no hardware required)

server/
  main.py           # FastAPI app (POST /readings, GET /readings, GET /)
  db.py             # SQLite helpers
  logic.py          # computation functions (soil%, light lux, needs_water)
  config.py         # calibration constants (edit here to recalibrate)
  static/
    index.html      # dashboard

docs/
  flash-and-build-guide.md
  wiring-diagram.png
  breadboard-diagram.png
  exact-wiring-map.png

scripts/
  flash.sh          # erase + flash MicroPython + copy firmware in one command
```

## Hardware

- **Board:** ELEGOO ESP32 (ESP32-D0WD-V3)
- **Sensors:** DHT11 (temp/humidity), capacitive soil moisture, photoresistor
- **Pin map:**
  - D4 → DHT11 data
  - D2 → photoresistor (ADC)
  - D15 → soil moisture (ADC)

> **Note:** D2 and D15 are ADC2 pins. ADC2 conflicts with WiFi on the ESP32 — sensors must be read *before* WiFi connects each cycle. See `firmware/app/main.py:run_loop()`. A permanent fix is rewiring to ADC1 pins (GPIO 32–39).

## Quickstart

### 1. Server (Mac)

```bash
cd server
pip3 install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

Or as a boot service (already configured):
```bash
launchctl load ~/Library/LaunchAgents/com.plantmonitor.server.plist
```

Logs: `~/Library/Logs/plant-monitor/server.log`
DB: `server/readings.db`

### 2. Firmware

Copy `firmware/app/credentials.py.example` → `firmware/app/credentials.py` and fill in your WiFi credentials and server URL (`http://<mac-local-ip>:8080/readings`).

Flash the ESP32:
```bash
./scripts/flash.sh /dev/cu.usbserial-0001 path/to/ESP32_GENERIC.bin
```

> Flash requires `--baud 115200 write_flash -z 0x1000` for this board. The script handles this.

### 3. Calibration

Edit `server/config.py`:
```python
SOIL_DRY = 2962   # raw ADC when sensor is in dry soil/air
SOIL_WET = 2485   # raw ADC when sensor is in wet soil/water
LIGHT_DARK = 0
LIGHT_BRIGHT = 2360
WATER_THRESHOLD_PERCENT = 30
```

Restart the server after changes:
```bash
launchctl unload ~/Library/LaunchAgents/com.plantmonitor.server.plist
launchctl load   ~/Library/LaunchAgents/com.plantmonitor.server.plist
```

### 4. Tests

```bash
cd firmware
python3 -m unittest discover -s tests -v
```

## Dashboard

Open `http://localhost:8080/` — shows latest readings and a history chart. Auto-refreshes every 60 seconds.
