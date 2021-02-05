import requests
from dotenv import load_dotenv
import os
import json
from control import get_humid, get_temperature, get_humidity, get_moisture, get_uv, post_schedule
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

env_dir = "/home/pi/device_var.env"
temp_hum_pin = 17
moisture_pin = 5
uv_pin = 16
device_mqtt_client = ''

def dev_publish_init(mqtt_client):
    global device_mqtt_client
    device_mqtt_client = mqtt_client

def post_meas(meas_json, action_type):
    client = device_mqtt_client
    load_dotenv(env_dir)
    device_id = str(os.getenv("DEVICE_ID"))
    topic = device_id + '/Post/' + action_type
    print(topic)
    data_json = json.loads(meas_json)
    client.publish(topic, json.dumps(data_json), 0)

def payload_handling(payload):
    json_action = json.loads(payload)
    action_type = str(json_action["action_type"])
    print(action_type)
    received_dev_id = str(json_action["device_id"])
    print(received_dev_id)
    received_variable = str(json_action["variable"])
    print(received_variable)
    pin = 17
    if received_variable == "temperature" or received_variable == "humidity":
        pin = 17
    if received_variable == "uv":
        pin = 16
    if received_variable == "moisture":
        pin = 5

    return action_type, received_dev_id, received_variable, pin
    

def MQTT_action(action_type, received_variable, received_dev_id, pin):
    if action_type == "measurement":
        if received_variable == "temperature":
            post_meas(get_temperature(pin), action_type)
            print("Temperature Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "humidity":
            post_meas(get_humidity(pin), action_type)
            print("Humidity Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "moisture":
            post_meas(get_moisture(pin), action_type)
            print("Moisture Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "uv":
            post_meas(get_uv(pin), action_type)
            print("UV Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''



