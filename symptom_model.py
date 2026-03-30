import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# -----------------------------
# Create models folder if not exists
# -----------------------------
os.makedirs("models", exist_ok=True)

# -----------------------------
# Load dataset (inside dataset folder)
# -----------------------------
data = pd.read_csv("dataset/snakebite_symptoms.csv")

# -----------------------------
# Separate features and target
# -----------------------------
X = data.drop("snake_type", axis=1)
y = data["snake_type"]

# -----------------------------
# Create ML model
# -----------------------------
model = RandomForestClassifier(n_estimators=100)

# -----------------------------
# Train model
# -----------------------------
model.fit(X, y)

# -----------------------------
# Save trained model
# -----------------------------
joblib.dump(model, "models/symptom_model.pkl")

print("Symptom model trained and saved successfully.")