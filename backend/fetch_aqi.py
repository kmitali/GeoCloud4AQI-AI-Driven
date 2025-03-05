import requests
import psycopg2
from datetime import datetime

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="geocloud4aqi",
    user="mitali",
    password="Mit@3009",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# OpenWeatherMap API Key
API_KEY = "dd54d0ecebff369e45f9ff135004c150617233df"
LAT, LON = "23.3441", "85.3096"  # Example for Ranchi

# Fetch AQI data
url = f"https://api.waqi.info/feed/geo:{LAT};{LON}/?token={API_KEY}"
response = requests.get(url)
data = response.json()

# Debug: Print API response to check structure
print("API Response:", data)

# Check if response contains 'data' key
if "data" in data and isinstance(data["data"], dict) and "aqi" in data["data"]:
    aqi_value = data["data"]["aqi"]
    timestamp = datetime.now()

# Insert into PostgreSQL
cursor.execute("INSERT INTO aqi_data (location, aqi_value, recorded_at) VALUES (%s, %s, %s)", ("Ranchi", aqi_value, timestamp))
conn.commit()

print(f"AQI for Ranchi: {aqi_value} (Stored in DB)")

# Close connection
cursor.close()
conn.close()
