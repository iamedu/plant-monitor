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
                light_lux REAL,
                soil_moisture_percent REAL,
                needs_water INTEGER
            )
        """)


def insert(ts: str, reading) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT INTO readings
               (ts, temperature_c, humidity_percent, light_lux, soil_moisture_percent, needs_water)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                ts,
                reading.temperature_c,
                reading.humidity_percent,
                reading.light_lux,
                reading.soil_moisture_percent,
                None if reading.needs_water is None else int(reading.needs_water),
            ),
        )


def query(limit: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]
