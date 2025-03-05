from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database import SessionLocal
from models import AQIData
from fastapi import FastAPI, Depends
from typing import List
from schemas import AQIDataResponse
from fastapi.middleware.cors import CORSMiddleware
import models
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "Connected to PostgreSQL!"}        

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "dd54d0ecebff369e45f9ff135004c150617233df"  # Replace with your actual API key
DATABASE_URL = "postgresql+psycopg2://mitali:Mit@3009@localhost:5432/geocloud4aqi"
engine = create_engine(DATABASE_URL)
@app.get("/")
def home():
    return {"message": "Welcome to GeoCloud4AQI Backend"}

@app.get("/aqi", response_model=List[AQIDataResponse])
def get_aqi_data(db: Session = Depends(get_db)):
    """Fetch all AQI records from the database."""
    return db.query(AQIData).all()

@app.post("/aqi", response_model=AQIDataResponse)
def add_aqi_data(aqi_data: AQIDataResponse, db: Session = Depends(get_db)):
    """Insert a new AQI record into the database."""
    new_aqi = AQIData(**aqi_data.dict())
    db.add(new_aqi)
    db.commit()
    db.refresh(new_aqi)
    return new_aqi

@app.get("/aqi", response_model=List[AQIDataResponse])
def get_aqi_data(
    city: str = None, 
    date: str = None, 
    db: Session = Depends(get_db)
):
    """Fetch AQI data with optional filters."""
    query = db.query(AQIData)
    
    if city:
        query = query.filter(AQIData.city == city)
    
    if date:
        query = query.filter(AQIData.date == date)
    
    return query.all()



@app.get("/aqi-data")
async def get_aqi_data(location: str, db: Session = Depends(get_db)):
    print(f"Querying data for location: {location}")
    result = db.query(AQIData).filter(AQIData.location == location).all()
    print(f"Result: {result}")
    return result


@app.get("/aqi/{location}")
def get_aqi(location: str, db: Session = Depends(get_db)):
    aqi_record = db.query(AQIData).filter(AQIData.location == location).order_by(AQIData.timestamp.desc()).first()
    if not aqi_record:
        return {"error": "No data found"}
    return {"location": aqi_record.location, "aqi": aqi_record.aqi, "timestamp": aqi_record.timestamp}


@app.get("/get_aqi/{city}")
async def get_aqi(city: str):
    url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "status" in data and data["status"] == "ok":
            aqi = data["data"]["aqi"]
            return {"city": city, "aqi": aqi}
        return {"error": "No AQI data available"}

    return {"error": "Invalid city or API issue"}

@app.delete("/aqi/{aqi_id}", response_model=dict)
def delete_aqi_data(aqi_id: int, db: Session = Depends(get_db)):
    """Delete AQI data by ID."""
    aqi_entry = db.query(AQIData).filter(AQIData.id == aqi_id).first()

    if not aqi_entry:
        raise HTTPException(status_code=404, detail="AQI record not found")

    db.delete(aqi_entry)
    db.commit()

    return {"message": f"AQI record with ID {aqi_id} deleted successfully"}


# Run the app
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)











