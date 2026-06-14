import json, time, random, math, os
from datetime import datetime, timezone
from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv

load_dotenv()

# --- Ship definitions ---
SHIPS = {
    "MSC-BELLISSIMA": os.getenv("BELLISSIMA_CONN_STR"),
    "MSC-GRANDIOSA":  os.getenv("GRANDIOSA_CONN_STR"),
    "MSC-SEASHORE":   os.getenv("SEASHORE_CONN_STR"),
}

# Base GPS positions (Mediterranean routes)
BASE_POSITIONS = {
    "MSC-BELLISSIMA": (43.2965, 5.3813),   # Marseille
    "MSC-GRANDIOSA":  (40.8518, 14.2681),  # Naples
    "MSC-SEASHORE":   (37.9838, 23.7275),  # Athens
}

def generate_telemetry(ship_id, tick, fault_mode=False):
    lat, lon = BASE_POSITIONS[ship_id]
    # Simulate slow movement
    lat += math.sin(tick * 0.01) * 0.05
    lon += math.cos(tick * 0.01) * 0.05

    # Normal sensor ranges
    engine_rpm    = random.gauss(1800, 30)
    coolant_temp  = random.gauss(78, 1.5)     # normal: ~78°C
    fuel_flow     = random.gauss(12.5, 0.3)   # litres/min
    hvac_pressure = random.gauss(4.2, 0.1)    # bar
    vibration     = random.gauss(0.8, 0.05)   # mm/s

    # Inject fault: coolant overheating + vibration spike
    if fault_mode:
        coolant_temp += random.uniform(15, 25)   # spikes to ~95-103°C
        vibration    += random.uniform(1.0, 2.5) # bearing wear

    return {
        "ship_id":       ship_id,
        "timestamp":     datetime.now(timezone.utc).isoformat(),
        "gps_lat":       round(lat, 6),
        "gps_lon":       round(lon, 6),
        "engine_rpm":    round(engine_rpm, 1),
        "coolant_temp":  round(coolant_temp, 2),
        "fuel_flow_lpm": round(fuel_flow, 3),
        "hvac_pressure": round(hvac_pressure, 3),
        "vibration_mms": round(vibration, 3),
        "fault_injected": fault_mode   # for training labels later
    }

def run_simulator():
    # Connect all ships to IoT Hub
    clients = {}
    for ship_id, conn_str in SHIPS.items():
        clients[ship_id] = IoTHubDeviceClient.create_from_connection_string(conn_str)
        clients[ship_id].connect()
        print(f"Connected: {ship_id}")

    tick = 0
    try:
        while True:
            for ship_id, client in clients.items():
                # 5% chance of fault mode per reading
                fault = random.random() < 0.05
                data = generate_telemetry(ship_id, tick, fault_mode=fault)
                msg  = Message(json.dumps(data))
                msg.content_encoding = "utf-8"
                msg.content_type     = "application/json"
                client.send_message(msg)
                print(f"Sent [{ship_id}] temp={data['coolant_temp']}°C "
                      f"rpm={data['engine_rpm']} fault={fault}")
            tick += 1
            time.sleep(5)   # send every 5 seconds
    except KeyboardInterrupt:
        print("Shutting down simulator...")
    finally:
        for client in clients.values():
            client.disconnect()

if __name__ == "__main__":
    run_simulator()