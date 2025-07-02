# ✅ train_model.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

# Load dataset
df = pd.read_csv("data\location_aware_gis_leakage_dataset.csv")

# Label creation
low_pressure_thresh = df['Pressure'].quantile(0.25)
high_flow_thresh = df['Flow_Rate'].quantile(0.75)
df['Leakage_Flag'] = ((df['Pressure'] < low_pressure_thresh) & (df['Flow_Rate'] > high_flow_thresh)).astype(int)

# Feature engineering
df['Pressure_to_Flow'] = df['Pressure'] / (df['Flow_Rate'] + 1e-5)
df['RPM_to_Age'] = df['RPM'] / (df['Operational_Hours'] + 1e-5)

features = ['Pressure', 'Flow_Rate', 'Temperature', 'Vibration', 'RPM', 'Operational_Hours',
            'Pressure_to_Flow', 'RPM_to_Age']
X = df[features]
y = df['Leakage_Flag']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = XGBClassifier(eval_metric="logloss", random_state=42)
model.fit(X_scaled, y)

# Save model and scaler
joblib.dump(model, "models\leakage_model.pkl")
joblib.dump(scaler, "models\scaler.pkl")
print("✅ Model and scaler saved")
