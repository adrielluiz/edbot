import sys
import time
from paho.mqtt import client as mqtt_client

broker = 'test.mosquitto.org'
port = 1883
topic = "edbotv1_ufu2022/position/set"
topic_test = "edbotv1_ufu2022/position/test_connection"
client_id = f'python-mqtt'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


client = mqtt_client.Client(client_id)
client.on_connect = on_connect
client.connect(broker, port)


def mqtt_publish(motor_id, position):
    msg = "{\"motor\":" + str(motor_id) + ", \"pos\":" + str(position) + "}"
    result = client.publish(topic, msg)
    status = result[0]
    return status


def mqtt_init():
    client.loop_start()
    time.sleep(1)


def mqtt_get_status_conenction():
    client.publish(topic_test, "conencting")
    return client.is_connected()


