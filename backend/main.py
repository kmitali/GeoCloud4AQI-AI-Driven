from fastapi import FastAPI
import requests
import os

app = FastAPI()

API_KEY = "dd54d0ecebff369e45f9ff135004c150617233df"  # Replace with your actual API key

@app.get("/")
def home():
    return {"message": "Welcome to GeoCloud4AQI Backend"}

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

# Run the app
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)











