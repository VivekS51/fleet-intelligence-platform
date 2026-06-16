from influxdb_client import InfluxDBClient, Point

client = InfluxDBClient(
    url="http://localhost:8086",
    token="fleet-super-secret-token",
    org="fleet-org"
)

write_api = client.write_api()

point = Point("test").field("value", 123)

write_api.write(
    bucket="ship-telemetry",
    org="fleet-org",
    record=point
)

print("SUCCESS")
