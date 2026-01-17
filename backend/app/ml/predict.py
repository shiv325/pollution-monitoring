import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Model file not found. Train the model first.")

model = joblib.load(MODEL_PATH)

def predict_aqi(pm25: float, pm10: float, no2: float):
    prediction = model.predict([[pm25, pm10, no2]])
    return round(float(prediction[0]), 2)
