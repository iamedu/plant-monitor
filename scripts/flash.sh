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
python3 -m esptool --chip esp32 --port "$PORT" --baud 460800 write_flash -z 0 "$FIRMWARE_BIN"

echo "Copying app files..."
mpremote connect "$PORT" fs cp -r "$ROOT_DIR/firmware/app" :
mpremote connect "$PORT" fs cp "$ROOT_DIR/firmware/app/main.py" :main.py

echo "Resetting board..."
mpremote connect "$PORT" reset

echo "Done. Open a REPL with:"
echo "  mpremote connect $PORT repl"
