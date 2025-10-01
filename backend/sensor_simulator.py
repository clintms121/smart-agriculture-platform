import requests
import random
import time
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Sensor configurations
SENSORS = [
    {"sensor_id": 1, "type": "soil_moisture", "location": "Field A", "min": 10, "max": 80},
    {"sensor_id": 2, "type": "temperature", "location": "Field A", "min": 15, "max": 40},
    {"sensor_id": 3, "type": "humidity", "location": "Field A", "min": 25, "max": 95},
    {"sensor_id": 4, "type": "soil_moisture", "location": "Field B", "min": 10, "max": 80},
    {"sensor_id": 5, "type": "temperature", "location": "Field B", "min": 15, "max": 40},
]


def create_sensors():
    """Initialize sensors in the database (run once)"""
    print("🌱 Creating sensors...")
    for sensor in SENSORS:
        payload = {
            "sensor_type": sensor["type"],
            "location": sensor["location"]
        }
        try:
            response = requests.post(f"{API_BASE_URL}/sensors", json=payload)
            if response.status_code == 200:
                print(f"✅ Created sensor: {sensor['type']} at {sensor['location']}")
            else:
                print(f"⚠️  Sensor might already exist: {response.text}")
        except Exception as e:
            print(f"❌ Error creating sensor: {e}")


def generate_reading(sensor):
    """Generate a realistic sensor reading with occasional anomalies"""
    base_value = random.uniform(sensor["min"], sensor["max"])

    # 10% chance of anomaly (triggers alerts)
    if random.random() < 0.1:
        if sensor["type"] == "soil_moisture":
            return random.uniform(5, 18)  # Low moisture alert
        elif sensor["type"] == "temperature":
            return random.uniform(36, 42)  # High temp alert
        elif sensor["type"] == "humidity":
            return random.uniform(15, 28)  # Low humidity alert

    return round(base_value, 2)


def send_reading(sensor_id, value):
    """Send a reading to the API"""
    payload = {
        "sensor_id": sensor_id,
        "reading_value": value
    }
    try:
        response = requests.post(f"{API_BASE_URL}/readings", json=payload)
        if response.status_code == 200:
            data = response.json()
            alert_status = "🚨 ALERT" if data.get("alert") else "✅"
            print(f"{alert_status} Sensor {sensor_id}: {value} | {datetime.now().strftime('%H:%M:%S')}")
            if data.get("alert"):
                print(f"   └─ {data['alert']['alert_message']}")
        else:
            print(f"❌ Failed to send reading: {response.text}")
    except Exception as e:
        print(f"❌ Error sending reading: {e}")


def simulate_continuous(interval=5):
    """Continuously generate and send sensor data"""
    print(f"\n📡 Starting continuous simulation (every {interval} seconds)...")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            for sensor in SENSORS:
                value = generate_reading(sensor)
                send_reading(sensor["sensor_id"], value)

            print(f"\n⏳ Waiting {interval} seconds...\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n✋ Simulation stopped by user")


def simulate_batch(count=10):
    """Send a batch of readings for testing"""
    print(f"\n📊 Sending {count} readings per sensor...\n")

    for i in range(count):
        print(f"--- Batch {i + 1}/{count} ---")
        for sensor in SENSORS:
            value = generate_reading(sensor)
            send_reading(sensor["sensor_id"], value)
        time.sleep(1)

    print("\n✅ Batch simulation complete!")


def check_api_health():
    """Verify API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print("✅ API is running!")
            return True
        else:
            print("⚠️  API returned unexpected status")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print(f"   Make sure FastAPI is running at {API_BASE_URL}")
        return False


def view_recent_alerts():
    """Fetch and display recent alerts"""
    try:
        response = requests.get(f"{API_BASE_URL}/alerts")
        if response.status_code == 200:
            alerts = response.json()["alerts"]
            if alerts:
                print("\n🚨 Recent Alerts:")
                for alert in alerts[:5]:
                    print(f"  • {alert['alert_message']} ({alert['location']}) - {alert['severity']} severity")
            else:
                print("\n✅ No alerts found")
    except Exception as e:
        print(f"❌ Error fetching alerts: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("🌾 SMART AGRICULTURE - SENSOR SIMULATOR")
    print("=" * 60)

    # Check if API is available
    if not check_api_health():
        exit(1)

    print("\nChoose simulation mode:")
    print("1. Setup - Create sensors (run once)")
    print("2. Batch - Send 10 readings per sensor")
    print("3. Continuous - Stream data every 5 seconds")
    print("4. View recent alerts")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        create_sensors()
    elif choice == "2":
        simulate_batch(count=10)
    elif choice == "3":
        simulate_continuous(interval=5)
    elif choice == "4":
        view_recent_alerts()
    else:
        print("❌ Invalid choice")