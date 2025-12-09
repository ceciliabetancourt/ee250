import paho.mqtt.client as mqtt
import time
import sys
import grovepi

# potentiometer connected to analog port A0 as input
potentiometer = 0
grovepi.pinMode(potentiometer,"INPUT")

# light sensor connected to analog port A1 as input
light_sensor = 1
grovepi.pinMode(light_sensor,"INPUT")

# mqtt callback executed when client receives a connection acknowledgement 
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

if __name__ == '__main__':
    # (1) publish to mqtt broker
    # create a client object
    client = mqtt.Client()

    # attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    
    # separate thread to handle incoming, outgoing mqtt messages 
    client.loop_start()

    while True:
        # publish chosen city and color of display :)
        # (2) read light sensor value
        light_sensor_val = grovepi.analogRead(light_sensor)
        print('Light sensor –> ', f"{light_sensor_val}")
        time.sleep(0.2)
        if light_sensor_val < 260: # through experiments, we determined divisions as 0-259, 260-519, >520
            display = 'yellow'
        elif light_sensor_val < 520:
            display = 'blue'
        else: # light_sensor_val >= 520:
            display = 'red'
        client.publish("lizarral/displayinfo", f"{display}")
        time.sleep(1)

        # (3) read potentiometer value
        potentiometer_val = grovepi.analogRead(potentiometer)
        print('Potentiometer –> ', f"{potentiometer_val}")
        time.sleep(0.2)
        if potentiometer_val < 341: # since it's from 0-1023, divisions are 0-341, 342-682, 683-1023
            city = 'Madrid'
        elif potentiometer_val < 682:
            city = 'Los Angeles'
        else: # potentiometer_val >= 682:
            city = 'London'
        client.publish("lizarral/cityinfo", f"{city}")
        time.sleep(1)

