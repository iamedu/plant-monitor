#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime

DEFAULT_SERVER = os.environ.get("PLANT_MONITOR_URL", "http://localhost:8080")


def fetch(server, limit):
    url = f"{server}/readings?limit={limit}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return json.loads(resp.read())
    except urllib.error.URLError as e:
        print(f"Error: could not reach server at {server} ({e.reason})", file=sys.stderr)
        sys.exit(1)


def fmt_val(val, suffix=""):
    return f"{val}{suffix}" if val is not None else "—"


def fmt_water(val):
    if val is None:
        return "—"
    return "YES" if val else "No"


def fmt_ts(ts):
    try:
        return datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts[:19]


def cmd_latest(args):
    data = fetch(args.server, 1)
    if not data:
        print("No readings yet.")
        return
    r = data[0]
    print(
        f"Temp: {fmt_val(r.get('temperature_c'), '°C')}  "
        f"Humidity: {fmt_val(r.get('humidity_percent'), '%')}  "
        f"Soil: {fmt_val(r.get('soil_moisture_percent'), '%')}  "
        f"Light: {fmt_val(r.get('light_lux'), ' lux')}  "
        f"Needs water: {fmt_water(r.get('needs_water'))}"
    )
    print(f"({fmt_ts(r['ts'])})")


def cmd_history(args):
    data = fetch(args.server, args.limit)
    if not data:
        print("No readings yet.")
        return
    if args.json:
        print(json.dumps(data, indent=2))
        return

    header = f"{'TIMESTAMP':<21} {'TEMP':>6} {'HUM':>6} {'SOIL':>6} {'LIGHT':>8}  WATER"
    print(header)
    print("-" * len(header))
    for r in data:
        print(
            f"{fmt_ts(r['ts']):<21}"
            f" {fmt_val(r.get('temperature_c'), '°C'):>6}"
            f" {fmt_val(r.get('humidity_percent'), '%'):>6}"
            f" {fmt_val(r.get('soil_moisture_percent'), '%'):>6}"
            f" {fmt_val(r.get('light_lux'), 'lx'):>8}"
            f"  {fmt_water(r.get('needs_water'))}"
        )


def cmd_stats(args):
    data = fetch(args.server, args.limit)
    if not data:
        print("No readings yet.")
        return

    metrics = [
        ("Temp (°C)",   "temperature_c"),
        ("Humidity %",  "humidity_percent"),
        ("Soil %",      "soil_moisture_percent"),
        ("Light lux",   "light_lux"),
    ]

    print(f"{'':14} {'MIN':>8} {'MAX':>8} {'AVG':>8}  (n={len(data)})")
    print("-" * 44)
    for label, key in metrics:
        vals = [r[key] for r in data if r.get(key) is not None]
        if not vals:
            print(f"{label:<14} {'—':>8} {'—':>8} {'—':>8}")
        else:
            print(
                f"{label:<14}"
                f" {min(vals):>8.1f}"
                f" {max(vals):>8.1f}"
                f" {sum(vals)/len(vals):>8.1f}"
            )


def main():
    parser = argparse.ArgumentParser(prog="cli.py", description="Plant Monitor CLI")
    parser.add_argument("--server", default=DEFAULT_SERVER, help="Server URL (or set PLANT_MONITOR_URL)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("latest", help="Show the most recent reading")

    p_history = sub.add_parser("history", help="Show recent readings")
    p_history.add_argument("--limit", type=int, default=20, help="Number of readings (default 20)")
    p_history.add_argument("--json", action="store_true", help="Output raw JSON")

    p_stats = sub.add_parser("stats", help="Summary statistics")
    p_stats.add_argument("--limit", type=int, default=100, help="Readings to include (default 100)")

    args = parser.parse_args()
    {"latest": cmd_latest, "history": cmd_history, "stats": cmd_stats}[args.command](args)


if __name__ == "__main__":
    main()
