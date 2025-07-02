# ✅ dashboard.py (Streamlit UI with Map)
import streamlit as st
import requests
import pandas as pd
import time
import os

# Page setup
st.set_page_config(page_title="Real-Time Water Leakage Detection Dashboard", layout="wide")
st.title("🚰 Real-Time Water Leakage Detection with GIS")

# File to log predictions
HISTORY_FILE = "leakage_log.csv"

# Input form for sensor data
with st.form("leakage_form"):
    st.subheader("🔧 Enter Live Sensor Values")
    col1, col2 = st.columns(2)
    with col1:
        pressure = st.number_input("Pressure", value=30.0)
        flow = st.number_input("Flow Rate", value=75.0)
        temp = st.number_input("Temperature", value=90.0)
        vib = st.number_input("Vibration", value=2.0)
    with col2:
        rpm = st.number_input("RPM", value=1800.0)
        hours = st.number_input("Operational Hours", value=500.0)
        lat = st.number_input("Latitude", value=25.4)
        lon = st.number_input("Longitude", value=55.3)

    submitted = st.form_submit_button("🚀 Predict Leakage")

# If the form is submitted
if submitted:
    payload = {
        "Pressure": pressure,
        "Flow_Rate": flow,
        "Temperature": temp,
        "Vibration": vib,
        "RPM": rpm,
        "Operational_Hours": hours,
        "Latitude": lat,
        "Longitude": lon
    }
    try:
        res = requests.post("http://localhost:5000/predict", json=payload)
        if res.status_code == 200:
            result = res.json()
            st.success(f"✅ Location: {result['Location_Code']}")
            st.metric(label="Leakage Probability", value=result['Leakage_Probability'])

            if result['Leakage_Predicted'] == 1:
                st.error("🚨 Potential Leakage Detected!")
            else:
                st.success("🟢 No Leakage Detected")

            # Log prediction
            log_row = pd.DataFrame([{
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "Latitude": lat,
                "Longitude": lon,
                "Probability": result['Leakage_Probability'],
                "Predicted": result['Leakage_Predicted'],
                "Location_Code": result['Location_Code']
            }])

            if os.path.exists(HISTORY_FILE):
                log_row.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
            else:
                log_row.to_csv(HISTORY_FILE, index=False)

        else:
            st.error("❌ Failed to fetch prediction.")
    except Exception as e:
        st.error(f"⚠️ API Error: {e}")

# 📍 Real-Time Map of Leak Alerts
st.subheader("🗺️ Live Leak Map")
if os.path.exists(HISTORY_FILE):
    history = pd.read_csv(HISTORY_FILE)
    recent = history.sort_values("Timestamp", ascending=False).head(100)
    leak_points = recent[recent["Predicted"] == 1][["Latitude", "Longitude"]]

    if not leak_points.empty:
        # ✅ Rename columns for Streamlit map
        leak_points.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'}, inplace=True)
        st.map(leak_points)
    else:
        st.info("No recent leak alerts to display on the map.")
else:
    st.info("No predictions yet. Submit data above to begin logging.")
