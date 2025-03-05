from backend.fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import AQIData  # Import your AQI model
from database import get_db  # Import your database session

router = APIRouter()

@router.get("/aqi/")
def get_aqi_data(db: Session = Depends(get_db)):
    return db.query(AQIData).all()

@router.post("/aqi/")
def add_aqi_data(aqi: AQIData, db: Session = Depends(get_db)):
    db.add(aqi)
    db.commit()
    return {"message": "AQI data added successfully"}

@router.put("/aqi/{aqi_id}")
def update_aqi_data(aqi_id: int, new_data: AQIData, db: Session = Depends(get_db)):
    aqi_record = db.query(AQIData).filter(AQIData.id == aqi_id).first()
    if aqi_record:
        for key, value in new_data.dict().items():
            setattr(aqi_record, key, value)
        db.commit()
        return {"message": "AQI data updated successfully"}
    return {"error": "Record not found"}

@router.delete("/aqi/{aqi_id}")
def delete_aqi_data(aqi_id: int, db: Session = Depends(get_db)):
    aqi_record = db.query(AQIData).filter(AQIData.id == aqi_id).first()
    if aqi_record:
        db.delete(aqi_record)
        db.commit()
        return {"message": "AQI data deleted successfully"}
    return {"error": "Record not found"}
