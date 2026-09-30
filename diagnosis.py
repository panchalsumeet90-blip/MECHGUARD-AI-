"""
MECHGUARD-AI
Mechanical Fault Diagnosis Engine

IMPORTANT:
This is a prototype trained on SYNTHETIC data.
It is NOT validated for real industrial fault diagnosis.
"""

import json
import joblib


MODEL_PATH = "models/fault_model.joblib"
FEATURES_PATH = "models/features.json"


MAINTENANCE_ACTIONS = {
    "NORMAL": "No action needed. Continue routine monitoring.",
    "BEARING_FAULT": "Inspect bearings and check for wear or damage.",
    "OVERHEATING": "Check cooling system, airflow, and lubrication.",
    "OVERLOAD": "Check machine load and reduce excessive load if necessary.",
    "MISALIGNMENT": "Check shaft and coupling alignment.",
}


def load_model():
    return joblib.load(MODEL_PATH)


def load_features():
    with open(FEATURES_PATH, "r") as file:
        return json.load(file)


model = load_model()
feature_list = load_features()


def validate_inputs(sensor_values):
    for name, value in sensor_values.items():
        if value < 0:
            raise ValueError(
                f"Invalid input: {name} cannot be negative."
            )


def calculate_health_score(
    temperature_c,
    vibration_mm_s,
    rpm,
    load_percent,
    current_a,
    operating_hours
):
    score = 100

    if temperature_c > 90:
        score -= 30
    elif temperature_c > 75:
        score -= 15
    elif temperature_c > 60:
        score -= 5

    if vibration_mm_s > 7:
        score -= 25
    elif vibration_mm_s > 4:
        score -= 10
    elif vibration_mm_s > 2:
        score -= 5

    if load_percent > 100:
        score -= 25
    elif load_percent > 90:
        score -= 10

    if current_a > 50:
        score -= 15
    elif current_a > 35:
        score -= 5

    if operating_hours > 20000:
        score -= 10
    elif operating_hours > 10000:
        score -= 5

    return max(0, min(100, score))


def get_risk_level(health_score):
    if health_score >= 75:
        return "LOW"
    elif health_score >= 45:
        return "MEDIUM"
    else:
        return "HIGH"


def diagnose_machine(
    temperature_c,
    vibration_mm_s,
    rpm,
    load_percent,
    current_a,
    operating_hours
):
    sensor_values = {
        "temperature_c": temperature_c,
        "vibration_mm_s": vibration_mm_s,
        "rpm": rpm,
        "load_percent": load_percent,
        "current_a": current_a,
        "operating_hours": operating_hours,
    }

    validate_inputs(sensor_values)

    feature_row = [
        [sensor_values[name] for name in feature_list]
    ]

    predicted_fault = model.predict(feature_row)[0]

    probabilities = model.predict_proba(feature_row)[0]

    class_index = list(model.classes_).index(predicted_fault)

    confidence = float(probabilities[class_index])

    health_score = calculate_health_score(
        temperature_c,
        vibration_mm_s,
        rpm,
        load_percent,
        current_a,
        operating_hours
    )

    risk_level = get_risk_level(health_score)

    recommended_action = MAINTENANCE_ACTIONS.get(
        predicted_fault,
        "Manual inspection recommended."
    )

    return {
        "fault_type": predicted_fault,
        "confidence": round(confidence, 4),
        "health_score": health_score,
        "risk_level": risk_level,
        "recommended_action": recommended_action,
    }


if __name__ == "__main__":

    example_reading = {
        "temperature_c": 82.0,
        "vibration_mm_s": 5.2,
        "rpm": 1450,
        "load_percent": 88.0,
        "current_a": 32.5,
        "operating_hours": 12000,
    }

    result = diagnose_machine(**example_reading)

    print("=" * 60)
    print("MECHGUARD-AI DIAGNOSIS")
    print("=" * 60)

    print(f"Predicted Fault : {result['fault_type']}")
    print(f"Confidence      : {result['confidence'] * 100:.2f}%")
    print(f"Health Score    : {result['health_score']}/100")
    print(f"Risk Level      : {result['risk_level']}")
    print(f"Recommendation  : {result['recommended_action']}")

    print("=" * 60)
    print("Prototype trained on synthetic data.")
