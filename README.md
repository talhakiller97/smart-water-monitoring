# 💧 Real-Time Water Leakage Detection with GIS and Machine Learning

This project is an end-to-end machine learning system designed to detect potential water pipeline leakage in real time using sensor data and geographic information. It combines model training, a RESTful API, and a live dashboard with GIS visualization.

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-orange)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

![Screenshot 2025-07-14 124152](https://github.com/user-attachments/assets/f40cb8a2-7f60-43c9-89ae-a3ae2b631592)


---

## 📦 Project Structure

.
├── app.py # Flask API for model inference

├── dashboard.py # Streamlit dashboard for real-time predictions

├── model_training.py # Model training and feature engineering script

├── requirements.txt # Python package dependencies

├── models/ # Saved model and scaler (after training)

│ ├── leakage_model.pkl

│ └── scaler.pkl

├── data/ # Dataset

│ └── location_aware_gis_leakage_dataset.csv

├── leakage_log.csv # Logged predictions (auto-created)

└── README.md # This file

---

## 🔍 Features

- ✅ Leakage Detection using sensor data
- 🌍 GIS-based location mapping
- 📊 Streamlit Dashboard with live map and metrics
- 🧠 XGBoost ML model
- 🧾 CSV-based prediction logging

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/real-time-water-leakage-detection.git
cd real-time-water-leakage-detection
```
2. Install Dependencies
```bash
pip install -r requirements.txt
```
3. Train the Model
```bash
python model_training.py
```
This saves the trained model and scaler (leakage_model.pkl, scaler.pkl).

5. Start the Flask API
```bash
python app.py
```
The API will be live at http://localhost:5000.

7. Launch the Dashboard
In a new terminal/tab:

```bash
streamlit run dashboard.py
```
You’ll get a web interface where you can input sensor values and view predictions on a map.

📡 API Payload Format
Use this format when sending POST requests to /predict:
```json

{
  "Pressure": 30.0,
  "Flow_Rate": 75.0,
  "Temperature": 90.0,
  "Vibration": 2.0,
  "RPM": 1800.0,
  "Operational_Hours": 500.0,
  "Latitude": 25.4,
  "Longitude": 55.3
}
```
🗺️ Dashboard Features
Interactive form for live predictions

Displays probability and binary leak classification

Saves results in leakage_log.csv

Shows recent leak events on a map

📌 Notes

Keep app.py running while using the dashboard.

Ensure location_aware_gis_leakage_dataset.csv is placed in the data/ directory before training.

leakage_log.csv is created automatically.

🧾 License

MIT License — use freely with credit.

Contributions are welcome. Open an issue or submit a pull request to improve the system.
