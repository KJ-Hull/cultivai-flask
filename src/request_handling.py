from dotenv import load_dotenv
import os
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from temperature import get_temperature
from humidity import get_humidity
from moisture import get_moisture
from uv import get_uv

env_dir = "/home/pi/device_var.env"
load_dotenv(env_dir)
device_id = str(os.getenv("DEVICE_ID"))
device_mqtt_client = ''

def pin_handling(variable_name):
    if variable_name == "temperature" or variable_name == "humidity":
        pin = 17
        return pin
    if variable_name == "uv":
        pin = 16
        return pin
    if variable_name == "moisture":
        pin = 5
        return pin

def dev_publish_init(mqtt_client):
    global device_mqtt_client
    device_mqtt_client = mqtt_client

def mqtt_meas(meas_json, action_type):
    global device_id
    client = device_mqtt_client
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
    pin = pin_handling(received_variable)
    print(pin)
    return action_type, received_dev_id, received_variable, pin
    

def MQTT_action(action_type, received_variable, received_dev_id, pin):
    if action_type == "measurement":
        if received_variable == "temperature":
            mqtt_meas(get_temperature(pin), action_type)
            print("Temperature Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "humidity":
            mqtt_meas(get_humidity(pin), action_type)
            print("Humidity Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "moisture":
            mqtt_meas(get_moisture(pin), action_type)
            print("Moisture Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "uv":
            mqtt_meas(get_uv(pin), action_type)
            print("UV Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''

    if action_type == "Update":
        print("yes, master")
    #if action_type == "PinState":

    #if action_type == "PortChane":




