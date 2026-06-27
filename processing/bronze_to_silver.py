import json
import os
from dateutil import parser
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Load environment variables
load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Connect to Azure Blob Storage
blob_service = BlobServiceClient.from_connection_string(CONNECTION_STRING)

bronze = blob_service.get_container_client("fleet-bronze")
silver = blob_service.get_container_client("fleet-silver")

print("=" * 60)
print("Reading Bronze Container...")
print("=" * 60)

processed = 0
skipped = 0

# Read every blob in Bronze
for blob in bronze.list_blobs():

    try:
        # Download blob
        blob_data = bronze.download_blob(blob.name).readall()

        # Convert JSON
        telemetry = json.loads(blob_data)

        # Required fields
        required_fields = [
            "ship_id",
            "engine_rpm",
            "coolant_temp",
            "fuel_flow_lpm",
            "hvac_pressure",
            "vibration_mms",
            "gps_lat",
            "gps_lon",
            "timestamp"
        ]

        # Validate required fields
        if not all(field in telemetry for field in required_fields):
            skipped += 1
            print(f"Skipped (missing fields): {blob.name}")
            continue

        # Validate RPM
        if telemetry["engine_rpm"] <= 0:
            skipped += 1
            print(f"Skipped (invalid RPM): {blob.name}")
            continue

        # Validate coolant temperature
        if telemetry["coolant_temp"] < 0 or telemetry["coolant_temp"] > 150:
            skipped += 1
            print(f"Skipped (invalid coolant temperature): {blob.name}")
            continue

        # Validate fuel flow
        if telemetry["fuel_flow_lpm"] < 0:
            skipped += 1
            print(f"Skipped (invalid fuel flow): {blob.name}")
            continue

        # Normalize timestamp
        telemetry["timestamp"] = parser.parse(
            telemetry["timestamp"]
        ).isoformat()

        # Upload cleaned file to Silver
        silver.upload_blob(
            name=blob.name,
            data=json.dumps(telemetry, indent=2),
            overwrite=True
        )

        processed += 1
        print(f"✓ Cleaned: {blob.name}")

    except Exception as e:
        skipped += 1
        print(f"Error processing {blob.name}")
        print(e)

print("\n" + "=" * 60)
print("Bronze → Silver Pipeline Completed")
print("=" * 60)
print(f"Processed : {processed}")
print(f"Skipped   : {skipped}")
print("=" * 60)