import paho.mqtt.client as mqtt
import requests
import json

# definition of global variables
display_color = None
weather_prediction = None

def on_connect(client, userdata, flags, rc):
    # (1) LIGHT SENSOR ––> we subscribe to the broker in order to get the light sensor information 
    # (used to determine the background color of the display!)
    client.subscribe("lizarral/displayinfo")
    client.message_callback_add("lizarral/displayinfo", on_message_from_displayinfo)

    # (2) PREDICTED TEMPERATURES ––> in this subsection, we subscribe to the data published by our 
    # ML model
    client.subscribe("lizarral/weather_prediction")
    client.message_callback_add("lizarral/weather_prediction", on_message_from_weather_prediction)
    
    # (3) CITY INFORMATION ––> we subscribe to the corresponding city
    client.subscribe("lizarral/cityinfo")    
    client.message_callback_add("lizarral/cityinfo", on_message_from_cityinfo)

# custom message callbacks
def on_message_from_displayinfo(client, userdata, message):
   global display_color
   print("Custom callback  - Display: "+message.payload.decode())
   display_color = message.payload.decode()

def on_message_from_weather_prediction(client, userdata, message):
   global weather_prediction
   print("Custom callback  - Weather Prediction: "+message.payload.decode())
   weather_prediction = message.payload.decode()

def on_message_from_cityinfo(client, userdata, message):
   global latest_city
   print("Custom callback - City: "+message.payload.decode())
   latest_city = message.payload.decode()

# (2) define the url used to make the POST request
url = 'http://127.0.0.1:5000/send_data'
def http_info_weather(weather_prediction):
    response = requests.post(url, json = weather_prediction)
    return response

def http_info_display(display_color):
    response = requests.post(url, json = display_color)
    return response

def http_info_city(latest_city):
    response = requests.post(url, json = latest_city)
    return response

if __name__ == '__main__':
    # create a client object
    client = mqtt.Client()

    # attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect

    # connect to broker
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
    client.loop_forever()
