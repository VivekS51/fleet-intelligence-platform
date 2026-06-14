SELECT
    ship_id,
    timestamp,
    gps_lat,
    gps_lon,
    engine_rpm,
    coolant_temp,
    fuel_flow_lpm,
    hvac_pressure,
    vibration_mms,
    fault_injected
INTO BlobOutput
FROM IoTHubInput