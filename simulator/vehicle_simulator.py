import os
import json
import time
import random
import math
from datetime import datetime, timezone
from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("IOT_HUB_CONNECTION_STRING")

# Simulated route around Singapore (Southeast Asia - matches our IoT Hub region)
BASE_LAT = 1.3521
BASE_LON = 103.8198

def generate_telemetry(vehicle_id, tick):
    """Generate realistic vehicle telemetry data."""
    # Simulate movement along a route
    lat = BASE_LAT + (math.sin(tick * 0.1) * 0.01)
    lon = BASE_LON + (math.cos(tick * 0.1) * 0.01)

    return {
        "vehicle_id": vehicle_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": {
            "latitude": round(lat, 6),
            "longitude": round(lon, 6)
        },
        "speed_kmh": round(random.uniform(0, 120), 1),
        "engine_temp_c": round(random.uniform(85, 105), 1),
        "fuel_level_pct": round(random.uniform(20, 100), 1),
        "rpm": random.randint(700, 4000),
        "odometer_km": 50000 + tick,
        "status": random.choice(["moving", "moving", "moving", "idle", "stopped"])
    }

def main():
    print(f"Connecting to IoT Hub...")
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    client.connect()
    print(f"Connected! Sending telemetry for fleet-vehicle-001")
    print("Press Ctrl+C to stop\n")

    tick = 0
    try:
        while True:
            telemetry = generate_telemetry("fleet-vehicle-001", tick)
            message = Message(json.dumps(telemetry))
            message.content_type = "application/json"
            message.content_encoding = "utf-8"

            client.send_message(message)
            print(f"[{telemetry['timestamp']}] Sent: speed={telemetry['speed_kmh']} km/h, "
                  f"lat={telemetry['location']['latitude']}, "
                  f"fuel={telemetry['fuel_level_pct']}%")

            tick += 1
            time.sleep(5)  # Send every 5 seconds

    except KeyboardInterrupt:
        print("\nStopping simulator...")
    finally:
        client.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    main()