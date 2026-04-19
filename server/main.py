from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

import db
import logic
from config import SOIL_DRY, SOIL_WET, LIGHT_DARK, LIGHT_BRIGHT, WATER_THRESHOLD_PERCENT

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init()
    yield


app = FastAPI(title="Plant Monitor", lifespan=lifespan)


class Reading(BaseModel):
    temperature_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    soil_moisture_raw: Optional[int] = None
    light_raw: Optional[int] = None


@app.post("/readings", status_code=201)
def create_reading(reading: Reading):
    ts = datetime.now(timezone.utc).isoformat()
    soil_pct = logic.soil_percent(reading.soil_moisture_raw, SOIL_DRY, SOIL_WET) if reading.soil_moisture_raw is not None else None
    lux = logic.light_lux(reading.light_raw, LIGHT_DARK, LIGHT_BRIGHT) if reading.light_raw is not None else None
    nw = logic.needs_water(soil_pct, WATER_THRESHOLD_PERCENT)
    db.insert(ts, reading, soil_pct, lux, nw)
    return {"ts": ts}


@app.get("/readings")
def get_readings(limit: int = 100):
    return db.query(limit)


@app.get("/")
def dashboard():
    return FileResponse(STATIC_DIR / "index.html")
