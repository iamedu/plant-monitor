#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <serial-port> <micropython-bin>"
  echo "Example: $0 /dev/cu.usbserial-0001 ~/Downloads/ESP32_GENERIC.bin"
  exit 1
fi

PORT="$1"
FIRMWARE_BIN="$2"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

python3 -m pip install --quiet --upgrade esptool mpremote

echo "Erasing flash on $PORT..."
python3 -m esptool --chip esp32 --port "$PORT" erase_flash

echo "Flashing MicroPython from $FIRMWARE_BIN..."
python3 -m esptool --chip esp32 --port "$PORT" --baud 115200 write_flash -z 0x1000 "$FIRMWARE_BIN"

echo "Waiting for board to settle..."
sleep 3

echo "Copying app files..."
APP="$ROOT_DIR/firmware/app"
mpremote connect "$PORT" \
  fs mkdir app + \
  fs cp "$APP/__init__.py"    :app/__init__.py + \
  fs cp "$APP/config.py"      :app/config.py + \
  fs cp "$APP/logic.py"       :app/logic.py + \
  fs cp "$APP/main.py"        :app/main.py + \
  fs cp "$APP/sensors.py"     :app/sensors.py + \
  fs cp "$APP/wifi.py"        :app/wifi.py + \
  fs cp "$APP/uploader.py"    :app/uploader.py + \
  fs cp "$APP/credentials.py" :app/credentials.py + \
  fs cp "$ROOT_DIR/firmware/main.py" :main.py + \
  reset

echo "Done. Open a REPL with:"
echo "  mpremote connect $PORT repl"
