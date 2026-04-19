import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "readings.db"


def init():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                temperature_c REAL,
                humidity_percent REAL,
                soil_moisture_raw INTEGER,
                soil_moisture_percent REAL,
                light_raw INTEGER,
                light_lux REAL,
                needs_water INTEGER
            )
        """)


def insert(ts: str, reading, soil_pct, light_lux, needs_water) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT INTO readings
               (ts, temperature_c, humidity_percent, soil_moisture_raw,
                soil_moisture_percent, light_raw, light_lux, needs_water)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                ts,
                reading.temperature_c,
                reading.humidity_percent,
                reading.soil_moisture_raw,
                soil_pct,
                reading.light_raw,
                light_lux,
                None if needs_water is None else int(needs_water),
            ),
        )


def query(limit: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]
