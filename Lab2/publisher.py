import paho.mqtt.client as mqtt
import numpy as np
import time

counter = 0
publisher_client_id = "jacob_publisher"


def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    # Subscribe to the topic after a successful connection
    client.subscribe("ece180d/jacob/test", qos=1)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')


def on_message(client, userdata, message):
    global counter
    received_message = message.payload.decode("utf-8")
    received_client_id = client._client_id
    if received_client_id != publisher_client_id:
        print('Received message on publisher side:', received_message)
        counter = int(received_message) + 1
        print('Incrementing and updating counter on publisher side:', counter)
        


client = mqtt.Client(client_id=publisher_client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

print('Publishing...')
try:
    while True:
        client.publish("ece180d/jacob/test", str(counter), qos=1)
        print('Publishing:', counter)
        time.sleep(1)

except KeyboardInterrupt:
    pass  # Allow graceful exit on Ctrl+C

client.loop_stop()
client.disconnect()
