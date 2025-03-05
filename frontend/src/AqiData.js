import React, { useState, useEffect } from 'react';

const AqiData = () => {
    const [aqiData, setAqiData] = useState([]);
    const [location, setLocation] = useState("Ranchi");

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/aqi-data?location=${location}`)
            .then(response => response.json())
            .then(data => setAqiData(data))
            .catch(error => console.error("Error fetching data:", error));
    }, [location]);

    return (
        <div>
            <h2>AQI Data for {location}</h2>
            <input 
                type="text" 
                value={location} 
                onChange={(e) => setLocation(e.target.value)} 
                placeholder="Enter location"
            />
            <table border="1">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>PM2.5</th>
                        <th>PM10</th>
                        <th>NO2</th>
                        <th>SO2</th>
                        <th>CO</th>
                        <th>O3</th>
                    </tr>
                </thead>
                <tbody>
                    {aqiData.length > 0 ? (
                        aqiData.map((item, index) => (
                            <tr key={index}>
                                <td>{item.timestamp}</td>
                                <td>{item.pm25}</td>
                                <td>{item.pm10}</td>
                                <td>{item.no2}</td>
                                <td>{item.so2}</td>
                                <td>{item.co}</td>
                                <td>{item.o3}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="7">No data available</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default AqiData;
