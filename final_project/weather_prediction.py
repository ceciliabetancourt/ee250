import os
import json
from joblib import load
import paho.mqtt.client as mqtt

import vm_sub
from weather_api import get_weather_history_for_city

MODELS_DIR = "models"

CITY_LIST = ["Los Angeles", "Madrid", "London"]

# host, broker port number, and then topic name
BROKER_ADDRESS = "test.mosquitto.org"
BROKER_PORT = 1883
PREDICTION_TOPIC = "weather/prediction"

# convert name for file reading
def name_convert(name: str) -> str:
    return name.lower().replace(" ", "_")

def load_models(models_dir=MODELS_DIR): # (AIDED BY CHATGPT)
    models = {}

    for city in CITY_LIST:
        city_name = name_convert(city)

        model_path = os.path.join(models_dir, f"{city_name}_model.joblib")
        scaler_path = os.path.join(models_dir, f"{city_name}_scaler.joblib")

        model = load(model_path)
        scaler = load(scaler_path)

        models[city] = {"model": model, "scaler": scaler}

    return models

MODELS = load_models()

def build_features_from_weather_df(df, window=7):
    temps = df["temp"].values

    if len(temps) < window:
        raise ValueError(f"Not enough data to build a {window}-day window")

    last_week = temps[-window:]
    X_input = last_week.reshape(1, -1)
    return X_input

def predict_for_city(city_name):
    if city_name not in MODELS:
        raise ValueError(f"No model configured for city: {city_name}")

    df = get_weather_history_for_city(city_name, days=60)  # df must have 'temp' in °F

    X_input = build_features_from_weather_df(df, window=7)

    entry = MODELS[city_name]
    model = entry["model"]
    scaler = entry["scaler"]

    X_scaled = scaler.transform(X_input)

    y_pred = model.predict(X_scaled)
    predicted_temp = float(y_pred[0])

    return predicted_temp

def publish_prediction(city, predicted_temp):
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS, BROKER_PORT, keepalive=60)
    client.loop_start()

    payload = {
        "city": city,
        "predicted_temp_F": predicted_temp,
        "unit": "F"
    }

    client.publish(PREDICTION_TOPIC, json.dumps(payload))
    client.loop_stop()
    client.disconnect()

def main():
    # read the latest city chosen by vm_sub
    vm_sub.start_mqtt(background=True)

    # block until we have a city (or timeout)
    city = vm_sub.wait_for_city(timeout=10)
    if city is None:
        print("No city received from MQTT; exiting.")
        return

    print(f"Latest city from vm_sub: {city}")

    # run ML prediction for this city
    predicted_temp = predict_for_city(city)
    print(f"Predicted temperature for {city}: {predicted_temp:.2f} °F")

    # publish to MQTT!
    publish_prediction(city, predicted_temp)

if __name__ == "__main__":
    main()
    
