# grovepi libraries
import sys
sys.path.append('~/Dexter/GrovePi/Software/Python')
import grovepi
# mqtt broker libraries
import paho.mqtt.client as mqtt
import time
from datetime import datetime
import socket

# potentiometer connected to analog port A0 as input
potentiometer = 0
grovepi.pinMode(potentiometer,"INPUT")

# callback executed when client receives a connection acknowledgement 
# packet response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

if __name__ == '__main__':
    # (1) publish to mqtt broker
    # get IP address
    ip_address = 0
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    # create a client object
    client = mqtt.Client()
    
    # attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)

    # separate thread to handle incoming, outgoing mqtt messages 
    client.loop_start()
    time.sleep(1)

    while True:
        # publish chosen city and replace user with your USC username in all subscriptions
        # (2) read potentiometer value
        potentiometer_val = grovepi.analogRead(potentiometer)
        if potentiometer_val < 341: # since it's from 0-1023, divisions are 0-341, 342-682, 683-1023
            city = 'Madrid'
        elif potentiometer_val < 682:
            city = 'Los Angeles'
        else: # potentiometer_val > 682:
            city = 'London'
        client.publish("lizarral/cityinfo", f"{city}")
        time.sleep(4)
