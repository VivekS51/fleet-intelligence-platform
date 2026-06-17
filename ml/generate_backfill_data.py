import pandas as pd
import numpy as np
from datetime import datetime, timedelta

SHIPS = ["MSC-BELLISSIMA", "MSC-GRANDIOSA", "MSC-SEASHORE"]
HOURS_OF_HISTORY = 720   # 30 days of hourly data per ship

def generate_ship_history(ship_id, hours):
    rows = []
    start = datetime.now() - timedelta(hours=hours)

    # Simulate occasional "degradation episodes" lasting 4-8 hours
    degradation_active = False
    degradation_remaining = 0
    base_temp = 78.0
    base_vibration = 0.8

    for h in range(hours):
        timestamp = start + timedelta(hours=h)

        # 3% chance to START a degradation episode
        if not degradation_active and np.random.random() < 0.03:
            degradation_active = True
            degradation_remaining = np.random.randint(4, 9)

        if degradation_active:
            # Gradual creep upward over the episode
            progress = 1 - (degradation_remaining / 8)
            temp_drift = progress * 20       # creeps up to +20°C
            vib_drift  = progress * 1.8      # creeps up to +1.8 mm/s
            degradation_remaining -= 1
            if degradation_remaining <= 0:
                degradation_active = False
        else:
            temp_drift = 0
            vib_drift = 0

        avg_temp = base_temp + temp_drift + np.random.normal(0, 1.2)
        max_temp = avg_temp + np.random.uniform(1, 4)
        avg_vib  = base_vibration + vib_drift + np.random.normal(0, 0.05)
        max_vib  = avg_vib + np.random.uniform(0.1, 0.5)

        anomaly = 1 if (max_temp > 90 or max_vib > 2.0) else 0

        rows.append({
            "ship_id": ship_id,
            "hour": timestamp,
            "avg_engine_rpm": np.random.normal(1800, 25),
            "max_engine_rpm": np.random.normal(1850, 30),
            "avg_coolant_temp": round(avg_temp, 2),
            "max_coolant_temp": round(max_temp, 2),
            "stddev_coolant_temp": round(abs(np.random.normal(1, 0.3)), 3),
            "avg_vibration": round(avg_vib, 3),
            "max_vibration": round(max_vib, 3),
            "avg_fuel_flow": round(np.random.normal(12.5, 0.3), 3),
            "avg_hvac_pressure": round(np.random.normal(4.2, 0.1), 3),
            "anomaly_events": 1 if anomaly else 0,
            "anomaly_rate": 1.0 if anomaly else 0.0,
            "label": anomaly
        })
    return rows

def main():
    all_rows = []
    for ship in SHIPS:
        all_rows.extend(generate_ship_history(ship, HOURS_OF_HISTORY))

    df = pd.DataFrame(all_rows)
    df = df.sort_values(["ship_id", "hour"])
    df.to_csv("ml/training_data.csv", index=False)
    print(f"Generated {len(df)} hourly records across {len(SHIPS)} ships")
    print(f"Anomaly rate: {df['label'].mean():.2%}")

if __name__ == "__main__":
    main()