"""
MECHGUARD-AI
Synthetic Machine Sensor Dataset Generator

This script creates sample induction-motor sensor data
for developing and testing our AI fault-diagnosis system.

IMPORTANT:
This is SYNTHETIC data for a prototype.
It is NOT real industrial sensor data.
"""

import os
import random
import numpy as np
import pandas as pd


# -----------------------------
# SETTINGS
# -----------------------------

RANDOM_SEED = 42
TOTAL_SAMPLES = 12000

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# -----------------------------
# FAULT TYPES
# -----------------------------

FAULT_TYPES = [
    "NORMAL",
    "BEARING_FAULT",
    "OVERHEATING",
    "OVERLOAD",
    "MISALIGNMENT"
]


# -----------------------------
# GENERATE ONE SAMPLE
# -----------------------------

def generate_sample(fault_type):

    # Normal operating conditions
    load = np.random.uniform(20, 90)
    rpm = np.random.normal(1450, 25)
    temperature = 35 + load * 0.45 + np.random.normal(0, 3)
    vibration = np.random.normal(2.0, 0.5)
    current = 2 + load * 0.045 + np.random.normal(0, 0.3)
    operating_hours = np.random.uniform(100, 10000)

    # Bearing fault
    if fault_type == "BEARING_FAULT":
        vibration += np.random.uniform(2.0, 5.0)
        temperature += np.random.uniform(3, 10)
        current += np.random.uniform(0.2, 1.0)

    # Overheating
    elif fault_type == "OVERHEATING":
        temperature += np.random.uniform(25, 45)
        current += np.random.uniform(1, 3)

    # Overload
    elif fault_type == "OVERLOAD":
        load = np.random.uniform(80, 100)
        current += np.random.uniform(2, 5)
        temperature += np.random.uniform(10, 25)
        vibration += np.random.uniform(0.5, 2.0)

    # Misalignment
    elif fault_type == "MISALIGNMENT":
        vibration += np.random.uniform(1.5, 4.0)
        rpm += np.random.normal(-30, 15)
        temperature += np.random.uniform(2, 8)

    return {
        "temperature_c": round(temperature, 2),
        "vibration_mm_s": round(max(vibration, 0.1), 2),
        "rpm": round(max(rpm, 500), 2),
        "load_percent": round(load, 2),
        "current_a": round(max(current, 0.1), 2),
        "operating_hours": round(operating_hours, 2),
        "fault_type": fault_type
    }


# -----------------------------
# CREATE DATASET
# -----------------------------

def main():

    rows = []

    # 40% normal
    # 15% each fault
    normal_samples = int(TOTAL_SAMPLES * 0.40)
    fault_samples = int(TOTAL_SAMPLES * 0.15)

    for _ in range(normal_samples):
        rows.append(generate_sample("NORMAL"))

    for fault in FAULT_TYPES[1:]:
        for _ in range(fault_samples):
            rows.append(generate_sample(fault))

    # Shuffle the dataset
    random.shuffle(rows)

    df = pd.DataFrame(rows)

    # Make sure data folder exists
    os.makedirs("data", exist_ok=True)

    # Save CSV
    output_path = os.path.join("data", "machine_data.csv")
    df.to_csv(output_path, index=False)

    print("=" * 60)
    print("MECHGUARD-AI DATASET CREATED")
    print("=" * 60)

    print(f"\nTotal samples: {len(df)}")
    print(f"Saved to: {output_path}")

    print("\nDataset columns:")
    print(list(df.columns))

    print("\nFault distribution:")
    print(df["fault_type"].value_counts())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDataset generation completed successfully!")


# -----------------------------
# START PROGRAM
# -----------------------------

if __name__ == "__main__":
    main()
