import paho.mqtt.client as mqtt
import time

counter = 0
subscriber_client_id = "jacob_subscriber"


def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/jacob/test", qos=1)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')


def on_message(client, userdata, message):
    global counter
    received_message = message.payload.decode("utf-8")
    if client._client_id != subscriber_client_id:
        print('Received message on subscriber side:', received_message)
        counter = int(received_message) + 1
        print('Updated counter on subscriber side:', counter)


client = mqtt.Client(client_id=subscriber_client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
