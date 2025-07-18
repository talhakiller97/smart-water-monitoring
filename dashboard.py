import streamlit as st
import requests
import pandas as pd
import time
import os
import random

st.set_page_config(page_title="Real-Time Water Leakage Detection Dashboard", layout="wide")
st.title("💧 Real-Time Water Leakage Detection with GIS")

# File to log predictions
HISTORY_FILE = "leakage_log.csv"

st.sidebar.header("🔧 Simulation Settings")
simulate_random = st.sidebar.checkbox("🎲 Enable Leak Simulation Mode", value=True)
force_leak = st.sidebar.checkbox("🚨 Force Leak Prediction", value=False)

# Input form
with st.form("leakage_form"):
    st.subheader("Enter Sensor Data (Simulated or Manual)")

    col1, col2 = st.columns(2)
    with col1:
        pressure = st.number_input("Pressure", value=round(random.uniform(10, 50), 2) if simulate_random else 30.0)
        flow = st.number_input("Flow Rate", value=round(random.uniform(100, 160), 2) if simulate_random else 75.0)
        temp = st.number_input("Temperature", value=round(random.uniform(50, 110), 2) if simulate_random else 90.0)
        vib = st.number_input("Vibration", value=round(random.uniform(0.5, 4.0), 2) if simulate_random else 2.0)
    with col2:
        rpm = st.number_input("RPM", value=round(random.uniform(1000, 3000), 2) if simulate_random else 1800.0)
        hours = st.number_input("Operational Hours", value=round(random.uniform(100, 2000), 2) if simulate_random else 500.0)
        lat = st.number_input("Latitude", value=round(random.uniform(25.1, 25.5), 6) if simulate_random else 25.4)
        lon = st.number_input("Longitude", value=round(random.uniform(55.2, 55.5), 6) if simulate_random else 55.3)

    submitted = st.form_submit_button("🚀 Predict Leakage")

if submitted:
    # Prepare payload
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

            # Override prediction if simulation mode is on
            if force_leak:
                result["Leakage_Predicted"] = 1
                result["Leakage_Probability"] = round(random.uniform(0.85, 0.99), 2)

            # Display results
            st.success(f"📍 Location Code: {result['Location_Code']}")
            st.metric("Leakage Probability", result["Leakage_Probability"])

            if result["Leakage_Predicted"] == 1:
                st.error("🚨 Potential Leakage Detected!")
            else:
                st.success("✅ No Leakage Detected")

            # Log the prediction
            log_row = pd.DataFrame([{
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "Latitude": lat,
                "Longitude": lon,
                "Probability": result["Leakage_Probability"],
                "Predicted": result["Leakage_Predicted"],
                "Location_Code": result["Location_Code"]
            }])

            if os.path.exists(HISTORY_FILE):
                log_row.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
            else:
                log_row.to_csv(HISTORY_FILE, index=False)

        else:
            st.error("❌ API Error (status code not 200)")

    except Exception as e:
        st.error(f"⚠️ Failed to connect to API: {e}")

# 🗺️ Map Display Section
st.subheader("🗺️ Real-Time Leak Location Map")

if os.path.exists(HISTORY_FILE):
    history = pd.read_csv(HISTORY_FILE)
    recent = history.sort_values("Timestamp", ascending=False).head(100)

    # Only show predicted leak points
    leak_points = recent[recent["Predicted"] == 1][["Latitude", "Longitude"]].copy()

    # Rename for Streamlit's map API
    leak_points.rename(columns={"Latitude": "latitude", "Longitude": "longitude"}, inplace=True)

    if not leak_points.empty:
        st.map(leak_points)
        st.caption(f"📍 Showing {len(leak_points)} recent leak locations")
    else:
        st.warning("No leak points detected yet. Enable force mode or simulate low pressure + high flow.")

    with st.expander("📄 View Logged Predictions"):
        st.dataframe(recent.reset_index(drop=True))
else:
    st.info("No predictions yet. Submit data above to start logging.")
