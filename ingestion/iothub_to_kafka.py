import json
import os
from azure.eventhub import EventHubConsumerClient
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

EVENTHUB_CONN_STR = os.getenv("IOTHUB_EVENTHUB_CONN_STR")

producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def on_event(partition_context, event):
    try:
        data = json.loads(event.body_as_str())
        producer.send("ship-telemetry", value=data)
        print(f"Forwarded: {data.get('ship_id')}")
        partition_context.update_checkpoint(event)
    except Exception as e:
        print("Error:", e)

client = EventHubConsumerClient.from_connection_string(
    conn_str=EVENTHUB_CONN_STR,
    consumer_group="$Default"
)

print("Listening to IoT Hub and forwarding to Kafka...")

with client:
    client.receive(
        on_event=on_event,
        starting_position="-1"
    )