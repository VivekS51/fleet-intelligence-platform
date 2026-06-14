import json
from datetime import datetime, timezone

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import (
    KafkaSource,
    KafkaOffsetsInitializer,
    KafkaSink,
    KafkaRecordSerializationSchema,
)
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.common import Types

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# ==========================================================
# InfluxDB Configuration
# ==========================================================

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "fleet-super-secret-token"
INFLUX_ORG = "fleet-org"
INFLUX_BUCKET = "ship-telemetry"

influx_client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG,
)

write_api = influx_client.write_api(write_options=SYNCHRONOUS)


# ==========================================================
# Alert Thresholds
# ==========================================================

TEMP_THRESHOLD = 90.0
VIBRATION_THRESHOLD = 2.0


# ==========================================================
# Write telemetry to InfluxDB
# ==========================================================

def write_to_influx(data):
    point = (
        Point("ship_telemetry")
        .tag("ship_id", data["ship_id"])
        .field("engine_rpm", data["engine_rpm"])
        .field("coolant_temp", data["coolant_temp"])
        .field("fuel_flow_lpm", data["fuel_flow_lpm"])
        .field("hvac_pressure", data["hvac_pressure"])
        .field("vibration_mms", data["vibration_mms"])
        .field("gps_lat", data["gps_lat"])
        .field("gps_lon", data["gps_lon"])
        .time(datetime.now(timezone.utc), WritePrecision.NS)
    )

    write_api.write(
        bucket=INFLUX_BUCKET,
        org=INFLUX_ORG,
        record=point,
    )


# ==========================================================
# Alert Logic
# ==========================================================

def check_anomaly(data):
    alerts = []

    if data["coolant_temp"] > TEMP_THRESHOLD:
        alerts.append(
            f"HIGH COOLANT TEMP: {data['coolant_temp']}°C "
            f"(threshold: {TEMP_THRESHOLD}°C)"
        )

    if data["vibration_mms"] > VIBRATION_THRESHOLD:
        alerts.append(
            f"HIGH VIBRATION: {data['vibration_mms']} mm/s "
            f"(threshold: {VIBRATION_THRESHOLD} mm/s)"
        )

    if alerts:
        return {
            "ship_id": data["ship_id"],
            "timestamp": data["timestamp"],
            "severity": "HIGH",
            "alerts": alerts,
        }

    return None


# ==========================================================
# Process Kafka Messages
# ==========================================================

def process_message(raw_json):
    try:
        data = json.loads(raw_json)

        write_to_influx(data)

        alert = check_anomaly(data)

        if alert:
            alert_json = json.dumps(alert)

            print(f"ALERT: {alert_json}")

            return alert_json

        return None

    except Exception as e:
        print(f"Processing Error: {e}")
        return None


# ==========================================================
# Flink Job
# ==========================================================

def run_flink_job():

    env = StreamExecutionEnvironment.get_execution_environment()

    env.set_parallelism(1)

    # Load Kafka JARs
    env.add_jars(
        "file:///C:/Users/DELL/Documents/fleet-intelligence-platform/flink-jars/flink-connector-kafka-3.2.0-1.18.jar",
        "file:///C:/Users/DELL/Documents/fleet-intelligence-platform/flink-jars/kafka-clients-3.5.1.jar"
    )

    kafka_source = (
        KafkaSource.builder()
        .set_bootstrap_servers("localhost:9092")
        .set_topics("ship-telemetry")
        .set_group_id("flink-processor")
        .set_starting_offsets(
            KafkaOffsetsInitializer.latest()
        )
        .set_value_only_deserializer(
            SimpleStringSchema()
        )
        .build()
    )

    stream = env.from_source(
        kafka_source,
        WatermarkStrategy.no_watermarks(),
        "KafkaShipTelemetry"
    )

    alert_stream = (
        stream
        .map(
            process_message,
            output_type=Types.STRING()
        )
        .filter(lambda x: x is not None)
    )

    kafka_sink = (
        KafkaSink.builder()
        .set_bootstrap_servers("localhost:9092")
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()
            .set_topic("ship-alerts")
            .set_value_serialization_schema(
                SimpleStringSchema()
            )
            .build()
        )
        .build()
    )

    alert_stream.sink_to(kafka_sink)

    print("Flink job starting - listening to ship-telemetry...")

    env.execute("FleetAnomalyDetector")


if __name__ == "__main__":
    run_flink_job()