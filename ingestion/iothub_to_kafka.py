import json
import os

from azure.eventhub import EventHubConsumerClient
from kafka import KafkaProducer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EVENTHUB_CONN_STR = os.getenv("IOTHUB_EVENTHUB_CONN_STR")

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("=" * 60)
print("Fleet IoT Hub -> Kafka Bridge Started")
print("=" * 60)
print("Waiting for telemetry from Azure IoT Hub...\n")


def on_event(partition_context, event):
    print("\n================ NEW EVENT ================")

    try:
        # Read raw event body
        body = event.body_as_str()

        print("Raw Event:")
        print(body)

        # Convert JSON
        data = json.loads(body)

        # Send to Kafka
        producer.send("ship-telemetry", value=data)

        # Force send immediately
        producer.flush()

        print(f"✓ Forwarded to Kafka : {data.get('ship_id')}")

        # Update Event Hub checkpoint
        partition_context.update_checkpoint(event)

    except Exception as e:
        print("\n❌ ERROR")
        print(e)


# Create Event Hub consumer
client = EventHubConsumerClient.from_connection_string(
    conn_str=EVENTHUB_CONN_STR,
    consumer_group="$Default"
)

# Start listening
with client:
    client.receive(
        on_event=on_event,
        starting_position="-1"
    )