import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

data = {
    "pm25": [30, 60, 90, 120],
    "pm10": [50, 100, 150, 200],
    "no2": [20, 40, 60, 80],
    "aqi": [70, 120, 180, 240]
}

df = pd.DataFrame(data)

X = df[["pm25", "pm10", "no2"]]
y = df["aqi"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, MODEL_PATH)

print("✅ Model trained and saved at:", MODEL_PATH)
