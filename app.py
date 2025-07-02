# ✅ app.py (Flask API)
from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model and scaler
model = joblib.load("leakage_model.pkl")
scaler = joblib.load("scaler.pkl")

# Location mapping (Zone, Block, Pipe based on lat/lon ranges for demo)
def map_location(lat, lon):
    if lat > 25.3:
        zone = "Zone_1"
    else:
        zone = "Zone_2"
    if lon > 55.4:
        block = "Block_2"
    else:
        block = "Block_1"
    pipe = "Pipe_1" if lat + lon < 80 else "Pipe_2"
    return f"{zone}_{block}_{pipe}"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = np.array([
        data['Pressure'],
        data['Flow_Rate'],
        data['Temperature'],
        data['Vibration'],
        data['RPM'],
        data['Operational_Hours'],
        data['Pressure'] / (data['Flow_Rate'] + 1e-5),
        data['RPM'] / (data['Operational_Hours'] + 1e-5)
    ]).reshape(1, -1)

    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0, 1]
    location = map_location(data['Latitude'], data['Longitude'])

    return jsonify({
        "Leakage_Predicted": int(prediction),
        "Leakage_Probability": float(round(probability, 3)),
        "Location_Code": location
    })

if __name__ == "__main__":
    app.run(debug=True)
