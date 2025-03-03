import React, { useState } from "react";
import axios from "axios";

function App() {
  const [city, setCity] = useState("");
  const [aqi, setAqi] = useState(null);

  const fetchAQI = async () => {
    if (!city) return;
    try {
      const response = await axios.get(`http://127.0.0.1:8000/aqi/${city}`);
      setAqi(response.data.aqi);
  } catch (error) {
      console.error("Error fetching AQI:", error.response ? error.response.data : error.message);
      setAqi("Error fetching AQI data.");
  }
};
  

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>GeoCloud4AQI</h1>
      <input
        type="text"
        placeholder="Enter City"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        style={{ padding: "8px", marginRight: "10px" }}
      />
      <button onClick={fetchAQI} style={{ padding: "8px" }}>Get AQI</button>
      {aqi && <h2>AQI Level: {aqi}</h2>}
    </div>
  );
}

export default App;

