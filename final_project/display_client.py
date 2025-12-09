import paho.mqtt.client as mqtt
import requests
import json

# definition of global variables
display_color = None
weather_prediction = None
latest_city = None

def on_connect(client, userdata, flags, rc):
    # (1) LIGHT SENSOR -> subscribe to get display color
    client.subscribe("lizarral/displayinfo")
    client.message_callback_add("lizarral/displayinfo", on_message_from_displayinfo)

    # (2) PREDICTED TEMPERATURES -> subscribe to ML prediction data
    client.subscribe("weather/prediction")
    client.message_callback_add("weather/prediction", on_message_from_weather_prediction)

    # (3) CITY INFORMATION -> subscribe to selected city
    client.subscribe("lizarral/cityinfo")
    client.message_callback_add("lizarral/cityinfo", on_message_from_cityinfo)

    print("Connected to broker with result code", rc)

# custom message callbacks
def on_message_from_displayinfo(client, userdata, message):
    global display_color
    print("Custom callback - Display:", message.payload.decode())
    display_color = message.payload.decode()
    http_info_display({'display_color': display_color})

def on_message_from_weather_prediction(client, userdata, message):
    global weather_prediction
    print("Custom callback - Weather Prediction:", message.payload.decode())
    weather_prediction = json.loads(message.payload.decode())
    http_info_weather({'weather_prediction': weather_prediction})

def on_message_from_cityinfo(client, userdata, message):
    global latest_city
    print("Custom callback - City:", message.payload.decode())
    latest_city = message.payload.decode()
    http_info_city({'city': latest_city})

# url used for POST request
url = 'http://127.0.0.1:5000/send_data'

def http_info_weather(weather_prediction):
    return requests.post(url, json=weather_prediction)

def http_info_display(display_color):
    return requests.post(url, json=display_color)

def http_info_city(latest_city):
    return requests.post(url, json=latest_city)

if __name__ == '__main__':
    # create a client object
    client = mqtt.Client()

    # attach the on_connect() callback function
    client.on_connect = on_connect

    # connect to broker
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)

    # begin blocking loop
    client.loop_forever()
