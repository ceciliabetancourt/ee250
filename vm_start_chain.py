import paho.mqtt.client as mqtt
import time

# callback function
def on_message(client, userdata, message):
    payload = int(message.payload.decode())
    print(f"Number on {message.topic} is {payload}")
    number_new = payload + 1
    time.sleep(1)
    client.publish("lizarral/ping",str(number_new))

if __name__ == '__main__':
    # get ip address of the broker –in this case, the rpi
    ip_address = '172.20.10.12'
    # create client object
    client = mqtt.Client()
    # attach the on_message() callback function defined above to the mqtt client, connect to broker
    client.on_message = on_message
    client.connect(ip_address, port=1883, keepalive=60)
    # subscribe to 'ping' messages
    client.subscribe("lizarral/pong")
    # start publishing
    number = 0
    time.sleep(1)
    client.publish("lizarral/ping",number)
    print(f"lizarral/ping {number}")
    client.loop_forever()