import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

SEQUENCE_LENGTH = 24

FEATURES = [
    "avg_engine_rpm",
    "max_engine_rpm",
    "avg_coolant_temp",
    "max_coolant_temp",
    "stddev_coolant_temp",
    "avg_vibration",
    "max_vibration",
    "avg_fuel_flow",
    "avg_hvac_pressure"
]

df = pd.read_csv("ml/training_data.csv")

df = df.sort_values(["ship_id", "hour"])

scaler = StandardScaler()

df[FEATURES] = scaler.fit_transform(df[FEATURES])

joblib.dump(scaler, "ml/models/scaler.pkl")

X = []
y = []

for ship_id in df["ship_id"].unique():

    ship_df = df[df["ship_id"] == ship_id]

    values = ship_df[FEATURES].values
    labels = ship_df["label"].values

    for i in range(len(ship_df) - SEQUENCE_LENGTH):

        seq = values[i:i + SEQUENCE_LENGTH]

        target = labels[i + SEQUENCE_LENGTH]

        X.append(seq)
        y.append(target)

X = np.array(X)
y = np.array(y)

np.save("ml/data/X_sequences.npy", X)
np.save("ml/data/y_labels.npy", y)

print("X shape:", X.shape)
print("y shape:", y.shape)
print("Positive labels:", y.sum())