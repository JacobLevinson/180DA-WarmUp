import paho.mqtt.client as mqtt
import json

# Define global variable to store data
imu_data = {}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ece180d/jacob/lab4/imu")


def on_message(client, userdata, msg):
    global imu_data
    try:
        data = json.loads(msg.payload.decode())
        imu_data = {
            "ACC_X": data["ACC_X"],
            "ACC_Y": data["ACC_Y"],
            "ACC_Z": data["ACC_Z"],
            "GYR_X": data["GYR_X"],
            "GYR_Y": data["GYR_Y"],
            "GYR_Z": data["GYR_Z"]
        }
        print("Data stored:", imu_data)
    except Exception as e:
        print("Error processing message:", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_forever()
