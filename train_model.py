"""
train_model.py
----------------
MECHGUARD-AI: Mechanical fault diagnosis model trainer.

This script trains a RandomForestClassifier to classify induction motor
faults based on sensor readings. 

NOTE: The dataset used here (data/machine_data.csv) is SYNTHETIC data
created for prototyping purposes. This model is NOT trained on real
industrial sensor data and should not be used for real-world fault
diagnosis decisions without validation on real, labeled industrial data.

Run from the MECHGUARD-AI project root:
    python train_model.py
"""

import os
import json

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# ---------------------------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------------------------
DATA_PATH = os.path.join("data", "machine_data.csv")
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "fault_model.joblib")
FEATURES_PATH = os.path.join(MODEL_DIR, "features.json")

# The six input features used to predict the fault type
FEATURE_COLUMNS = [
    "temperature_c",
    "vibration_mm_s",
    "rpm",
    "load_percent",
    "current_a",
    "operating_hours",
]

TARGET_COLUMN = "fault_type"


def main():
    # -----------------------------------------------------------------------
    # 2. Load the dataset
    # -----------------------------------------------------------------------
    print(f"Loading dataset from: {DATA_PATH}")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Could not find '{DATA_PATH}'. Make sure you're running this "
            "script from the MECHGUARD-AI project root and that the CSV exists."
        )

    df = pd.read_csv(DATA_PATH)
    print(f"Dataset loaded successfully. Shape: {df.shape}")

    # Basic sanity check: make sure all expected columns are present
    missing_cols = [c for c in FEATURE_COLUMNS + [TARGET_COLUMN] if c not in df.columns]
    if missing_cols:
        raise ValueError(f"The following required columns are missing from the CSV: {missing_cols}")

    # -----------------------------------------------------------------------
    # 3. Separate features (X) and target (y)
    # -----------------------------------------------------------------------
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    print("\nClass distribution in full dataset:")
    print(y.value_counts())

    # -----------------------------------------------------------------------
    # 4. Train/test split (stratified so class proportions are preserved)
    # -----------------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples:  {len(X_test)}")

    # -----------------------------------------------------------------------
    # 5. Train the RandomForestClassifier
    # -----------------------------------------------------------------------
    # class_weight="balanced" helps the model give appropriate importance
    # to minority fault classes (useful since fault data is often imbalanced,
    # with NORMAL operation being far more common than fault conditions).
    print("\nTraining RandomForestClassifier...")
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)
    print("Training complete.")

    # -----------------------------------------------------------------------
    # 6. Evaluate the model on the held-out test set
    # -----------------------------------------------------------------------
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred, labels=model.classes_)

    print("\n" + "=" * 60)
    print("MODEL EVALUATION RESULTS")
    print("=" * 60)
    print(f"\nAccuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")

    print("\nClassification Report:")
    print(report)

    print("Confusion Matrix:")
    print(f"Classes (row/col order): {list(model.classes_)}")
    print(conf_matrix)
    print("=" * 60)

    # -----------------------------------------------------------------------
    # 7. Create the models/ folder if it doesn't exist
    # -----------------------------------------------------------------------
    os.makedirs(MODEL_DIR, exist_ok=True)

    # -----------------------------------------------------------------------
    # 8. Save the trained model with joblib
    # -----------------------------------------------------------------------
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to: {MODEL_PATH}")

    # -----------------------------------------------------------------------
    # 9. Save the feature names (so inference scripts know the exact
    #    column order the model expects)
    # -----------------------------------------------------------------------
    with open(FEATURES_PATH, "w") as f:
        json.dump(FEATURE_COLUMNS, f, indent=4)
    print(f"Feature list saved to: {FEATURES_PATH}")

    print("\nDone. MECHGUARD-AI model training finished successfully.")
    print("Reminder: this model was trained on SYNTHETIC data and is a prototype.")


if __name__ == "__main__":
    main()
