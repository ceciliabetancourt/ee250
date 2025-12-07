import paho.mqtt.client as mqtt

# function (or "callback") executed when client receives a connection acknowledgement 
# packet response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    
    # replace user with your USC username in all subscriptions
    client.subscribe("lizarral/cityinfo")
    
    # add the custom callbacks by indicating the topic and the name of the callback handle
    client.message_callback_add("lizarral/cityinfo", on_message_from_cityinfo)
    
def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

# custom message callback
def on_message_from_cityinfo(client, userdata, message):
   global latest_city
   print("Custom callback  - City: "+message.payload.decode())
   latest_city = message.payload.decode()

if __name__ == '__main__':
    # create a client object
    client = mqtt.Client()

    # attach a default callback which we defined above for incoming mqtt messages
    client.on_message = on_message

    # attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect

    # connect to broker
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
    client.loop_start()
