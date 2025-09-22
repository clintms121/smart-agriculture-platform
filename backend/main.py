#endpoints (defines API routes)
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
form . import models, database

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.get("/sensors")
def read_sensors(db: Session = Depends(get_db)):
    return db.query(models.Sensor).all()