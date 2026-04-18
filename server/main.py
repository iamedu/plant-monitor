from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

import db

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init()
    yield


app = FastAPI(title="Plant Monitor", lifespan=lifespan)


class Reading(BaseModel):
    temperature_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    light_lux: Optional[float] = None
    soil_moisture_percent: Optional[float] = None
    needs_water: Optional[bool] = None


@app.post("/readings", status_code=201)
def create_reading(reading: Reading):
    ts = datetime.now(timezone.utc).isoformat()
    db.insert(ts, reading)
    return {"ts": ts}


@app.get("/readings")
def get_readings(limit: int = 100):
    return db.query(limit)


@app.get("/")
def dashboard():
    return FileResponse(STATIC_DIR / "index.html")
