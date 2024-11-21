from fastapi import FastAPI, Depends, Body
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud, schemas, models
import json

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/availability/")
def get_common_availability(input: schemas.AvailabilityInput = Body(...), db: Session = Depends(get_db)):
    return crud.get_common_availability(db, input)
