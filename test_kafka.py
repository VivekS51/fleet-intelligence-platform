from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

future = producer.send(
    "ship-telemetry",
    {"test": "hello"}
)

print(future.get(timeout=30))
print("SUCCESS")