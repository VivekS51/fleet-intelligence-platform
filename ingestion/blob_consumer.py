import os
import json
from datetime import datetime

from kafka import KafkaConsumer
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")

blob_service = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service.get_container_client(container_name)

consumer = KafkaConsumer(
    "ship-telemetry",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Listening to Kafka...")

for msg in consumer:
    data = msg.value

    now = datetime.utcnow()

    blob_name = (
        f"{now.year}/"
        f"{now.month:02d}/"
        f"{now.day:02d}/"
        f"telemetry_{now.strftime('%H%M%S%f')}.json"
    )

    container_client.upload_blob(
        name=blob_name,
        data=json.dumps(data),
        overwrite=True
    )

    print(f"Uploaded {blob_name}")