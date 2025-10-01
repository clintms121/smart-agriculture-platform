from database import get_connection


def get_sensors():
    """Fetch every sensor"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensors;")
    sensors = cur.fetchall()
    cur.close()
    conn.close()
    return sensors


def get_sensor_by_id(sensor_id):
    """Fetch a single sensor by its id"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensors WHERE sensor_id = %s;", (sensor_id,))
    sensor = cur.fetchone()
    cur.close()
    conn.close()
    return sensor


def add_sensor(sensor_type: str, location: str):
    """Add a new sensor to the sensor table"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO sensors (sensor_type, location, installed_at)
        VALUES (%s, %s, NOW())
        RETURNING *;
        """,
        (sensor_type, location)
    )
    new_sensor = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_sensor


def get_readings(sensor_id: int, limit: int = 10):
    """Fetch the latest N readings for a given sensor"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM sensor_data
        WHERE sensor_id = %s
        ORDER BY reading_time DESC
        LIMIT %s;
        """,
        (sensor_id, limit)
    )
    readings = cur.fetchall()
    cur.close()
    conn.close()
    return readings


def insert_reading(sensor_id: int, reading_value: float):
    """Insert new sensor reading"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO sensor_data (sensor_id, reading_value, reading_time)
        VALUES (%s, %s, NOW())
        RETURNING *;
        """,
        (sensor_id, reading_value)
    )
    new_reading = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_reading


def get_all_readings(limit: int = 50):
    """Fetch all sensor readings"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM sensor_data ORDER BY reading_time DESC LIMIT %s;",
        (limit,)
    )
    readings = cur.fetchall()
    cur.close()
    conn.close()
    return readings


# ALERT FUNCTIONS
def check_for_alert(sensor_id: int, reading_value: float):
    """
    Check if an alert should be triggered based on reading value
    Rules:
    - Soil moisture < 20%: Low moisture alert
    - Temperature > 35°C: High temperature alert
    """
    conn = get_connection()
    cur = conn.cursor()

    # Get sensor type to determine alert logic
    cur.execute("SELECT sensor_type FROM sensors WHERE sensor_id = %s;", (sensor_id,))
    result = cur.fetchone()

    if not result:
        cur.close()
        conn.close()
        return None

    sensor_type = result['sensor_type'].lower()
    alert_triggered = False
    alert_message = None
    severity = None

    # Define alert rules
    if 'moisture' in sensor_type or 'soil' in sensor_type:
        if reading_value < 20:
            alert_triggered = True
            alert_message = f"Low soil moisture detected: {reading_value}%"
            severity = "high"

    elif 'temperature' in sensor_type or 'temp' in sensor_type:
        if reading_value > 35:
            alert_triggered = True
            alert_message = f"High temperature detected: {reading_value}°C"
            severity = "medium"
        elif reading_value < 0:
            alert_triggered = True
            alert_message = f"Freezing temperature detected: {reading_value}°C"
            severity = "high"

    elif 'humidity' in sensor_type:
        if reading_value < 30:
            alert_triggered = True
            alert_message = f"Low humidity detected: {reading_value}%"
            severity = "low"

    # Insert alert if triggered
    if alert_triggered:
        cur.execute(
            """
            INSERT INTO alerts (sensor_id, alert_message, severity, triggered_at, is_resolved)
            VALUES (%s, %s, %s, NOW(), FALSE)
            RETURNING *;
            """,
            (sensor_id, alert_message, severity)
        )
        new_alert = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return new_alert

    cur.close()
    conn.close()
    return None


def get_alerts(limit: int = 20):
    """Fetch recent alerts"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT a.*, s.sensor_type, s.location 
        FROM alerts a
        JOIN sensors s ON a.sensor_id = s.sensor_id
        ORDER BY a.triggered_at DESC
        LIMIT %s;
        """,
        (limit,)
    )
    alerts = cur.fetchall()
    cur.close()
    conn.close()
    return alerts


def get_active_alerts():
    """Fetch only unresolved alerts"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT a.*, s.sensor_type, s.location 
        FROM alerts a
        JOIN sensors s ON a.sensor_id = s.sensor_id
        WHERE a.is_resolved = FALSE
        ORDER BY a.triggered_at DESC;
        """
    )
    alerts = cur.fetchall()
    cur.close()
    conn.close()
    return alerts


def resolve_alert(alert_id: int):
    """Mark an alert as resolved"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE alerts
        SET is_resolved = TRUE, resolved_at = NOW()
        WHERE alert_id = %s
        RETURNING *;
        """,
        (alert_id,)
    )
    updated_alert = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return updated_alert


# TESTING
if __name__ == "__main__":
    # Fetch sensors
    print("ALL SENSORS: ", get_sensors())

    # Add sensor
    new_sensor = add_sensor("soil_moisture", "Field A")
    print("Added sensor: ", new_sensor)

    # Insert reading that triggers alert
    new_reading = insert_reading(sensor_id=1, reading_value=15.5)
    print("New reading: ", new_reading)

    # Check for alert
    alert = check_for_alert(sensor_id=1, reading_value=15.5)
    if alert:
        print("ALERT TRIGGERED: ", alert)

    # Get readings
    readings = get_readings(sensor_id=1, limit=5)
    print("Latest readings for sensor 1: ", readings)

    # Get alerts
    alerts = get_alerts(limit=5)
    print("Recent alerts: ", alerts)