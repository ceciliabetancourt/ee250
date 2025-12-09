import requests
import pandas as pd
from datetime import datetime, timedelta
import vm_sub

CITY_COORDS = {
    "Los Angeles": (34.0522, -118.2437),
    "Madrid":      (40.4168, -3.7038),
    "London":      (51.5074, -0.1278),
}

def c_to_f(celsius):
    return (celsius * 9/5) + 32

# pull recent weather for model to use
def get_weather_history(latitude, longitude, days=60):
    # use yesterday as end so we only use fully observed days
    days = int(days)
    end = datetime.now() - timedelta(days=1)
    start = end - timedelta(days=days - 1)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
        "daily": "temperature_2m_max",
        "timezone": "America/Los_Angeles",
    }

    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temp": data["daily"]["temperature_2m_max"],
    })

    # convert types
    df["date"] = pd.to_datetime(df["date"])
    df["temp"] = df["temp"].apply(c_to_f)  # store in farhenheit :)

    return df

# function for getting info for weather_prediction.py
def get_weather_history_for_city(city_name, days=60):
    if city_name is None:
        vm_sub.start_mqtt(background=True)
        city_name = vm_sub.wait_for_city(timeout=10)

        if city_name is None:
            raise RuntimeError("Timed out waiting for city from MQTT")
    lat, lon = CITY_COORDS[city_name]
    return get_weather_history(lat, lon, days=days)

if __name__ == "__main__":
    city_name = None
    df_la = get_weather_history_for_city(city_name, days=10)
    print(df_la)
