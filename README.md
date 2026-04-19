# Plant Monitor

A simple ESP32-based plant monitor that tracks soil moisture, temperature, humidity, and light.

## Current Status

### Working now
- ESP32 board identified and working
- MicroPython successfully flashed
- Firmware loads on device
- DHT11 wired and returning readings
- Photoresistor wired and returning readings
- Soil moisture sensor wired and calibrated
- WiFi upload working, ESP32 POSTs readings to Mac server every 5 minutes
- FastAPI server running on Mac as a launchd service (starts on boot)
- SQLite database persisting all readings
- Live dashboard with Chart.js history charts at `http://localhost:8080/`
- Supabase mirroring working from Mac server
- SwiftUI iPhone app MVP built in the same repo and installed locally

### Current hardware setup
- **Board:** ELEGOO ESP32 starter kit board (ESP32, not ESP32-S3)
- **Power:** USB to ESP32, sensors powered from **3V3** and **GND**
- **One-side pin layout:**
  - **D15** → soil moisture sensor signal
  - **D4** → DHT11 data
  - **D2** → photoresistor junction

### Current calibration
- **SOIL_DRY = 2962**
- **SOIL_WET = 2485**
- **LIGHT_DARK = 0**
- **LIGHT_BRIGHT = 2360**
- **WATER_THRESHOLD_PERCENT = 30**

### Current architecture

```text
ESP32 (MicroPython)
  └── reads DHT11 + photoresistor + soil sensor every 5 min
  └── POSTs JSON to local Mac server

Mac server (FastAPI, launchd)
  └── stores readings in SQLite
  └── computes calibrated values
  └── serves dashboard/API
  └── mirrors readings to Supabase

iPhone app (SwiftUI)
  └── reads recent history from Supabase
```

## iPhone App

The repo now includes a SwiftUI app MVP:
- latest reading card
- recent history list
- watering status badge
- pull to refresh
- custom plant app icon

Files live under:
- `ios/PlantMonitorApp/`
- `PlantMonitor.xcodeproj`
- `project.yml`

Secrets stay local only:
- real config: `ios/PlantMonitorApp/SupabaseConfig.json` (gitignored)
- example config: `ios/PlantMonitorApp/SupabaseConfig.example.json`

## Supabase

Optional cloud mirroring is wired into the Mac server.

Safe committed files:
- `server/supabase_client.py`
- `server/supabase_local.example.json`
- `server/supabase_schema.sql`

Local-only file:
- `server/supabase_local.json` (gitignored)

## Notes for next dev session
- Board serial port used successfully: `/dev/cu.usbserial-0001`
- MicroPython firmware used: `ESP32_GENERIC-20260406-v1.28.0.bin`
- Flash must use offset `0x1000` and baud `115200`
- GPIO 5 was tested and is invalid on this board for this use
- ADC2/WiFi conflict on ESP32 was handled by disconnecting WiFi after each POST
- Supabase project is working for mirrored cloud reads
- App icon is now set explicitly through the asset catalog

## Next Steps
1. Improve iPhone app UI and add charts
2. Add watering alert flow (likely BlueBubbles group notification)
3. Prepare app for TestFlight if desired
4. Add OLED support on device
5. Consider multiple plants / multi-device support
