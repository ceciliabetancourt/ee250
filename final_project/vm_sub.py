import paho.mqtt.client as mqtt
import threading
import time

# define global variables
latest_city = None
client = None

# (1) mqtt broker functions
def on_connect(client, userdata, flags, rc):
    client.subscribe("lizarral/cityinfo")
    client.message_callback_add("lizarral/cityinfo", on_message_from_cityinfo)
    print("Connected to broker with result code", rc)

def on_message_from_cityinfo(client, userdata, message):
    global latest_city
    latest_city = message.payload.decode()
    print("Custom callback - City:", latest_city)

# (2) defined functions used to avoid race conditions (specifically, the possibility of 
# 'weather_api.py' grabbing 'latest_city' when it's still defined as None
def start_mqtt(background=True): # (AIDED BY CHATGPT)
    # starts the mqtt client
    global client
    if client is not None:
        return client  # already started
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)

    if background:
        thread = threading.Thread(target=client.loop_forever, daemon=True)
        thread.start()
    else:
        client.loop_forever() # blocks
    return client

def wait_for_city(timeout=None, poll_interval=0.1):
    # ensures that the variable 'latest_city' is not grabbed until it's not 
    # None or it times out!
    start = time.time()
    while latest_city is None:
        if timeout is not None and time.time() - start > timeout:
            return None
        time.sleep(poll_interval)
    return latest_city

if __name__ == "__main__":
    start_mqtt(background=False)
    
