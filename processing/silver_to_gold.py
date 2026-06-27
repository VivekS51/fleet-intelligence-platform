
import json
import os

from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

blob_service = BlobServiceClient.from_connection_string(CONNECTION_STRING)

silver = blob_service.get_container_client("fleet-silver")
gold = blob_service.get_container_client("fleet-gold")

print("=" * 60)
print("Reading Silver Container...")
print("=" * 60)

processed = 0

for blob in silver.list_blobs():

    try:

        telemetry = json.loads(
            silver.download_blob(blob.name).readall()
        )

        rpm = telemetry["engine_rpm"]
        temp = telemetry["coolant_temp"]
        vibration = telemetry["vibration_mms"]
        fuel = telemetry["fuel_flow_lpm"]

        # Engine Health Score
        health_score = max(
            0,
            100
            - abs(rpm - 1800) / 25
            - abs(temp - 80) * 2
            - vibration * 10
        )

        # Maintenance Risk
        if health_score > 90:
            risk = "LOW"
        elif health_score > 70:
            risk = "MEDIUM"
        else:
            risk = "HIGH"

        telemetry["engine_health_score"] = round(health_score, 2)
        telemetry["maintenance_risk"] = risk

        gold.upload_blob(
            blob.name,
            json.dumps(telemetry, indent=2),
            overwrite=True
        )

        processed += 1

        print(f"✓ {blob.name}")

    except Exception as e:
        print(e)

print("\nFinished")
print(f"Processed : {processed}")
