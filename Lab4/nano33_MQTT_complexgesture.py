import paho.mqtt.client as mqtt
import json
import math

# Define global variable to store data and count consecutive samples
imu_data = {}
consecutive_forward_samples = 0
consecutive_up_samples = 0
consecutive_circular_motion_samples = 0

# Define thresholds for gesture detection in m/s²
THRESHOLD_FORWARD_PUSH = 0.5  # m/s²
THRESHOLD_UPWARD_LIFT = 0.5  # m/s²
THRESHOLD_CIRCULAR_MOTION = 5  # m/s² (Adjust as needed)
CONSECUTIVE_SAMPLE_THRESHOLD = 9  # Number of consecutive samples
CONSECUTIVE_SAMPLE_THRESHOLD_UCM = 25  # Number of consecutive samples
# Define last recorded values for gesture detection
last_acc_x = 0
last_acc_y = 0
last_acc_z = 0


def calculate_magnitude(acc_x, acc_y, acc_z):
    return math.sqrt(acc_x ** 2 + acc_y ** 2)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("ece180d/jacob/lab4/imu")


def on_message(client, userdata, msg):
    global imu_data, last_acc_x, last_acc_y, last_acc_z, consecutive_forward_samples, consecutive_up_samples, consecutive_circular_motion_samples
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

        # Gesture detection
        acc_x = imu_data["ACC_X"]
        acc_y = imu_data["ACC_Y"]
        acc_z = imu_data["ACC_Z"]

        if abs(acc_x - last_acc_x) > THRESHOLD_FORWARD_PUSH:
            consecutive_forward_samples += 1
        else:
            consecutive_forward_samples = 0

        if acc_z - last_acc_z < -THRESHOLD_UPWARD_LIFT:  # Adjusted condition for upward lift
            consecutive_up_samples += 1
        else:
            consecutive_up_samples = 0

        magnitude_xy = math.sqrt(acc_x ** 2 + acc_y ** 2)
        if magnitude_xy > THRESHOLD_CIRCULAR_MOTION:
            consecutive_circular_motion_samples += 1
        else:
            consecutive_circular_motion_samples = 0

        # Check if consecutive samples threshold is reached for any gesture
        if consecutive_forward_samples >= CONSECUTIVE_SAMPLE_THRESHOLD:
            print("Forward push detected")
            consecutive_forward_samples = 0  # Reset counter

        if consecutive_up_samples >= CONSECUTIVE_SAMPLE_THRESHOLD:
            print("Upward lift detected")
            consecutive_up_samples = 0  # Reset counter

        if consecutive_circular_motion_samples >= CONSECUTIVE_SAMPLE_THRESHOLD_UCM:
            print("Circular motion detected")
            consecutive_circular_motion_samples = 0  # Reset counter

        # Update last recorded values
        last_acc_x = acc_x
        last_acc_y = acc_y
        last_acc_z = acc_z

    except Exception as e:
        print("Error processing message:", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_forever()
