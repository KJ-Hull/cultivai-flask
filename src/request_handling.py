version = "0.1.1"
from dotenv import load_dotenv
import os
import json
from control import pin_handling
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from temperature import get_temperature
from humidity import get_humidity
from moisture import get_moisture
from uv import get_uv

env_dir = "/home/pi/device_var.env"
load_dotenv(env_dir)
device_id = str(os.getenv("DEVICE_ID"))
device_mqtt_client = ''

def dev_publish_init(mqtt_client):
    global device_mqtt_client
    device_mqtt_client = mqtt_client

def status_handling(action_type):
    if action_type == "update":
        active = True
        status = "Updating"
        version = "0.2"
    else:
        active = True
        status = "Active"
        version = "0.1"

    return active, status, version

def mqtt_pub(meas_json, action_type):
    global device_id
    client = device_mqtt_client
    topic = device_id + '/Post/' + action_type
    status_change = device_id + '/Post/status'
    print(status_change)
    print(topic)
    active, status, version = status_handling(action_type)
    status_dict = {"active":active, "status":status, "version":version, "device_id":device_id}
    status_json = json.dumps(status_dict)
    if action_type == "measurement":
        data_json = json.loads(meas_json)
        client.publish(topic, json.dumps(data_json), 0)

    client.publish(status_change, status_json, 0)

def payload_handling(payload):
    json_action = json.loads(payload)
    action_type = str(json_action["action_type"])
    print(action_type)
    received_dev_id = str(json_action["device_id"])
    print(received_dev_id)
    received_variable = str(json_action["variable"])
    print(received_variable)
    pin = pin_handling(received_variable)
    print(pin)
    return action_type, received_dev_id, received_variable, pin
    

def MQTT_action(action_type, received_variable, received_dev_id, pin):
    if action_type == "measurement":
        if received_variable == "temperature":
            mqtt_pub(get_temperature(pin), action_type)
            print("Temperature Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "humidity":
            mqtt_pub(get_humidity(pin), action_type)
            print("Humidity Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "moisture":
            mqtt_pub(get_moisture(pin), action_type)
            print("Moisture Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "uv":
            mqtt_pub(get_uv(pin), action_type)
            print("UV Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''

    if action_type == "update":
        mqtt_pub("", action_type)

    #if action_type == "PinState":

    #if action_type == "PortChange":




