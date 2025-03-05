from pydantic import BaseModel

class AQIDataResponse(BaseModel):
    city: str
    aqi: float
