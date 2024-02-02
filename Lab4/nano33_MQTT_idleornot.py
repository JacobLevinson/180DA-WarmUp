import paho.mqtt.client as mqtt
import json

# Define global variables to store data
prev_acc = {"ACC_X": 0, "ACC_Y": 0, "ACC_Z": 0}
threshold = 0.1  # You can adjust this threshold as needed


def is_idle(data):
    global prev_acc
    try:
        delta_x = abs(data["ACC_X"] - prev_acc["ACC_X"])
        delta_y = abs(data["ACC_Y"] - prev_acc["ACC_Y"])
        delta_z = abs(data["ACC_Z"] - prev_acc["ACC_Z"])
        prev_acc = data  # Update previous acceleration values
        if delta_x < threshold and delta_y < threshold and delta_z < threshold:
            return True
        else:
            return False
    except Exception as e:
        print("Error checking acceleration:", e)
        return False


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ece180d/jacob/lab4/imu")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        if is_idle(data):
            print("IDLE")
        else:
            print("NOT IDLE")
    except Exception as e:
        print("Error processing message:", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_forever()
