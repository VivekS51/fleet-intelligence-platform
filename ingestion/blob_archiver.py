import json
import os
from datetime import datetime

from dotenv import load_dotenv
from kafka import KafkaConsumer
from azure.storage.blob import BlobServiceClient

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "fleet-bronze"

blob_service = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container = blob_service.get_container_client(CONTAINER_NAME)

consumer = KafkaConsumer(
    "ship-telemetry",
    bootstrap_servers="localhost:29092",
    group_id="blob-archiver",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    consumer_timeout_ms=10000,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Listening to Kafka...")

count = 0

for message in consumer:

    count += 1
    print(f"\nMessage #{count}")
    print(message.value)

    data = message.value

    now = datetime.utcnow()

    blob_name = (
        f"{now.year}/"
        f"{now.month:02d}/"
        f"{now.day:02d}/"
        f"{now.strftime('%H%M%S_%f')}.json"
    )

    container.upload_blob(
        blob_name,
        json.dumps(data, indent=2),
        overwrite=True
    )

    print("Uploaded:", blob_name)