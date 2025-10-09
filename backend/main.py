from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import data_access

app = FastAPI(title="Smart Agriculture API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SensorCreate(BaseModel):
    sensor_type: str
    location: str


class ReadingCreate(BaseModel):
    sensor_id: int
    reading_value: float


@app.get("/")
def root():
    return {"message": "Smart Agriculture API is running"}


@app.get("/sensors")
def get_all_sensors():
    sensors = data_access.get_sensors()
    return {"sensors": sensors}


@app.get("/sensors/{sensor_id}")
def get_sensor(sensor_id: int):
    sensor = data_access.get_sensor_by_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {"sensor": sensor}


@app.post("/sensors")
def create_sensor(sensor: SensorCreate):
    new_sensor = data_access.add_sensor(sensor.sensor_type, sensor.location)
    return {"message": "Sensor created successfully", "sensor": new_sensor}


@app.post("/readings")
def create_reading(reading: ReadingCreate):
    sensor = data_access.get_sensor_by_id(reading.sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    new_reading = data_access.insert_reading(reading.sensor_id, reading.reading_value)
    alert = data_access.check_for_alert(reading.sensor_id, reading.reading_value)

    return {
        "message": "Reading recorded successfully",
        "reading": new_reading,
        "alert": alert
    }


@app.get("/readings/{sensor_id}")
def get_sensor_readings(sensor_id: int, limit: int = 10):
    sensor = data_access.get_sensor_by_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    readings = data_access.get_readings(sensor_id, limit)
    return {"sensor_id": sensor_id, "readings": readings}


@app.get("/readings")
def get_all_readings(limit: Optional[int] = 50):
    readings = data_access.get_all_readings(limit)
    return {"readings": readings}


@app.get("/alerts")
def get_alerts(limit: int = 20):
    alerts = data_access.get_alerts(limit)
    return {"alerts": alerts}


@app.get("/alerts/active")
def get_active_alerts():
    alerts = data_access.get_active_alerts()
    return {"alerts": alerts}
