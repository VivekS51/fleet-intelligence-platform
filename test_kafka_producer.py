from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda x: json.dumps(x).encode()
)

producer.send(
    "ship-telemetry",
    {
        "ship_id": "TEST",
        "engine_rpm": 1800,
        "coolant_temp": 80,
        "fuel_flow_lpm": 20,
        "hvac_pressure": 5,
        "vibration_mms": 1,
        "gps_lat": 0,
        "gps_lon": 0,
        "timestamp": "2026-06-27T12:00:00Z"
    }
)

producer.flush()

print("Sent")