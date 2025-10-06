import React, { useState, useEffect } from 'react';

function App() {
  const [sensors, setSensors] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    // Fetch from your local API
    fetch('http://localhost:8000/sensors')
      .then(res => res.json())
      .then(data => setSensors(data.sensors || []))
      .catch(err => console.error('Error:', err));

    fetch('http://localhost:8000/alerts')
      .then(res => res.json())
      .then(data => setAlerts(data.alerts || []))
      .catch(err => console.error('Error:', err));
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>🌾 Smart Agriculture Dashboard</h1>

      <h2>Sensors</h2>
      <div>
        {sensors.map(sensor => (
          <div key={sensor.sensor_id} style={{
            border: '1px solid #ccc',
            padding: '10px',
            margin: '10px 0'
          }}>
            <strong>{sensor.sensor_type}</strong> - {sensor.location}
          </div>
        ))}
      </div>

      <h2>🚨 Alerts</h2>
      <div>
        {alerts.map(alert => (
          <div key={alert.alert_id} style={{
            border: '2px solid red',
            padding: '10px',
            margin: '10px 0',
            backgroundColor: '#ffe6e6'
          }}>
            <strong>{alert.severity.toUpperCase()}</strong>: {alert.alert_message}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;