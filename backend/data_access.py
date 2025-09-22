from database import get_connection

def get_sensors():
    #fetch every sensor
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensors;")
    sensors = cur.fetchall()
    cur.close()
    conn.close()
    return sensors

def get_sensor_by_id(sensor_id):
    #fetch a single sensor by its id
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensors WHERE sensor_id = %s;", (sensor_id,))
    sensor = cur.fetchone()
    cur.close()
    conn.close()
    return sensor

def add_sensor(sensor_type: str, location: str):
    #add a new sensor to the sensor table
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
    #fetch the latest N readings for a given sensor
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
    #insert new sensor reading
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sensor_data (sensor_id, reading_value, reading_time)
        VALUES (%s, %s, NOW())
        RETURNING *;
        """,
        (sensor_id, reading_value))
    new_reading = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_reading

def get_all_readings():
    #fetch all sensor readings
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor_data ORDER BY reading_time DESC;")
    readings = cur.fetchall()
    cur.close()
    conn.close()
    return readings

# TESTING #

if __name__ == "__main__":

    #fetch sensors
    print("ALL SENSORS: ", get_sensors())

    #add sensor
    new_sensor = add_sensor("temperature", "test field")
    print("added sensor: ", new_sensor)

    #insert reading
    new_reading = insert_reading(sensor_id=1, reading_value=25.6)
    print("the new reading is: ", new_reading)

    #get reading
    readings = get_readings(sensor_id=1, limit=5)
    print("Latest readings for sensor 1: ", readings)


