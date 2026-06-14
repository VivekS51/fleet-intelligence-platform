import os
import json
import time
import random
import math
import threading
from datetime import datetime, timezone

from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv

load_dotenv()

SHIPS = [
    {
        "shipId": "MSC-BELLISSIMA",
        "connection_string": os.getenv("MSC_BELLISSIMA_CONNECTION_STRING"),
        "base_lat": 1.3521,
        "base_lon": 103.8198
    },
    {
        "shipId": "MSC-GRANDIOSA",
        "connection_string": os.getenv("MSC_GRANDIOSA_CONNECTION_STRING"),
        "base_lat": 1.4000,
        "base_lon": 103.9000
    },
    {
        "shipId": "MSC-SEASHORE",
        "connection_string": os.getenv("MSC_SEASHORE_CONNECTION_STRING"),
        "base_lat": 1.3000,
        "base_lon": 103.7500
    }
]


def generate_telemetry(ship, tick):
    lat = ship["base_lat"] + (math.sin(tick * 0.1) * 0.01)
    lon = ship["base_lon"] + (math.cos(tick * 0.1) * 0.01)

    return {
        "shipId": ship["shipId"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "latitude": round(lat, 6),
        "longitude": round(lon, 6),
        "speed": round(random.uniform(10, 35), 1),
        "fuelLevel": round(random.uniform(30, 100), 1),
        "engineTemp": round(random.uniform(75, 95), 1),
        "heading": random.randint(0, 359),
        "status": random.choice(
            ["sailing", "sailing", "sailing", "anchored"]
        )
    }


def simulate_ship(ship):
    client = IoTHubDeviceClient.create_from_connection_string(
        ship["connection_string"]
    )

    client.connect()

    print(f"Connected: {ship['shipId']}")

    tick = 0

    try:
        while True:
            telemetry = generate_telemetry(ship, tick)

            message = Message(json.dumps(telemetry))
            message.content_type = "application/json"
            message.content_encoding = "utf-8"

            client.send_message(message)

            print(
                f"{ship['shipId']} | "
                f"speed={telemetry['speed']} knots | "
                f"fuel={telemetry['fuelLevel']}% | "
                f"temp={telemetry['engineTemp']}°C"
            )

            tick += 1
            time.sleep(5)

    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()


def main():
    threads = []

    for ship in SHIPS:
        t = threading.Thread(
            target=simulate_ship,
            args=(ship,),
            daemon=True
        )
        threads.append(t)
        t.start()

    print("Fleet simulator started...")
    print("Press Ctrl+C to stop")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()