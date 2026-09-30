"""
MECHGUARD-AI Backend
--------------------
Flask API for the MECHGUARD-AI machine fault diagnosis system.

IMPORTANT:
This project is a prototype trained on synthetic data.
It is not validated for real industrial fault diagnosis.
"""

import os
import sys

from flask import Flask, request, jsonify
from flask_cors import CORS


# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

# Find the MECHGUARD-AI project root.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Add the project root to Python's import path.
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# Import the existing diagnosis engine.
from diagnosis import diagnose_machine


# ---------------------------------------------------------
# FLASK APPLICATION
# ---------------------------------------------------------

app = Flask(__name__)

# Allow the frontend to communicate with this backend.
CORS(app)


# ---------------------------------------------------------
# REQUIRED SENSOR INPUTS
# ---------------------------------------------------------

REQUIRED_FIELDS = [
    "temperature_c",
    "vibration_mm_s",
    "rpm",
    "load_percent",
    "current_a",
    "operating_hours",
]


# ---------------------------------------------------------
# HOME / HEALTH CHECK
# ---------------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    """Check whether the MECHGUARD-AI backend is running."""

    return jsonify({
        "status": "ok",
        "message": "MECHGUARD-AI backend is running."
    })


# ---------------------------------------------------------
# MACHINE DIAGNOSIS API
# ---------------------------------------------------------

@app.route("/api/diagnose", methods=["POST"])
def diagnose():
    """
    Receive machine sensor readings and return a diagnosis.
    """

    try:

        # Read JSON data sent by the frontend.
        data = request.get_json(silent=True)

        # Check whether JSON data was received.
        if data is None:
            return jsonify({
                "error": "Invalid or missing JSON body."
            }), 400

        # Check for missing sensor fields.
        missing_fields = [
            field
            for field in REQUIRED_FIELDS
            if field not in data
        ]

        if missing_fields:
            return jsonify({
                "error": (
                    "Missing required field(s): "
                    + ", ".join(missing_fields)
                )
            }), 400

        # Convert sensor values to numbers.
        try:
            temperature_c = float(data["temperature_c"])
            vibration_mm_s = float(data["vibration_mm_s"])
            rpm = float(data["rpm"])
            load_percent = float(data["load_percent"])
            current_a = float(data["current_a"])
            operating_hours = float(data["operating_hours"])

        except (ValueError, TypeError):

            return jsonify({
                "error": "All sensor values must be numeric."
            }), 400

        # Send the sensor readings to our AI diagnosis engine.
        result = diagnose_machine(
            temperature_c=temperature_c,
            vibration_mm_s=vibration_mm_s,
            rpm=rpm,
            load_percent=load_percent,
            current_a=current_a,
            operating_hours=operating_hours
        )

        # Send the diagnosis back as JSON.
        return jsonify(result), 200

    except Exception as error:

        # Handle unexpected errors.
        return jsonify({
            "error": "An unexpected server error occurred.",
            "details": str(error)
        }), 500


# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("MECHGUARD-AI BACKEND")
    print("=" * 60)
    print("Starting Flask server...")
    print("Open http://127.0.0.1:5000 in your browser.")
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )