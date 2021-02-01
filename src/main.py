import json
import requests
from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
#from aws import check_bucket, create_bucket, s3_aws_init, upload_file, create_json_file 

from control import set_status, get_status, get_temp, get_humid, get_moist, get_uv_light
import RPi.GPIO as GPIO
import requests
from datetime import timedelta, datetime
import uuid
import time
from request_handling import post_meas

temp_hum_pin = 17
moisture_pin = 5
uv_pin = 16
device_id = 'ef720fc0-20ca-4485-92fe-c95c67ee9307'
measurement_id = ""

action_type = ''
received_dev_id = ''
received_variable = ''


def post_schedule():
    if request.method == 'POST':
        req_data = request.get_json()
        with open('schedule.json', 'w') as outfile:
            json.dump(req_data, outfile)

        return jsonify(req_data)
    else:
        with open('schedule.json') as f:
            data = json.load(f)
        return jsonify(data)

def get_temperature():
    temperature = get_temp(temp_hum_pin)
    name = "temperature"
    json_temp = {"variable":name, "value":str(temperature),"device_id":device_id}
    return json.dumps(json_temp)

def get_humidity():
    humidity = get_humid(temp_hum_pin)
    name = "humidity"
    json_humid= {"variable":name, "value":str(humidity),"device_id":device_id}
    return json.dumps(json_humid)

def get_moisture():
    moisture = get_moist(moisture_pin)
    name = "moisture"
    json_moist= {"variable":name, "value":moisture,"device_id":device_id}
    return json.dumps(json_moist)
    
def get_uv():
    uv = get_uv_light(uv_pin)
    name = "uv"
    json_uv= {"variable":name, "value":uv,"device_id":device_id}
    return json.dumps(json_uv)

MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_MASTER_TOPIC = "MASTER"
env_dir = "/home/pi/device_var.env"
load_dotenv(env_dir)

client_id = "RPI_device"
MQTT_TOPIC = os.getenv("GET_TOPIC")
CA_ROOT_CERT_FILE = os.getenv("CA")
THING_CERT_FILE = os.getenv("CERT")
THING_PRIVATE_KEY = os.getenv("PRIV_KEY")
MQTT_ENDPOINT = os.getenv("ENDPOINT")

MQTT_HOST = os.getenv('THING_HOST')
print(MQTT_HOST)

def customPostCallback(client, userdata, msg):
    global action_type 
    global received_dev_id
    global received_variable
    json_action = json.loads(msg.payload)
    action_type = str(json_action["action_type"])
    print(action_type)
    received_dev_id = str(json_action["device_id"])
    print(received_dev_id)
    received_variable = str(json_action["variable"])
    print(received_variable)

def customMasterCallback(client, userdata, msg):
    print("Received Master Action")

rpi_mqtt_client = AWSIoTMQTTClient(client_id)
rpi_mqtt_client.configureEndpoint(MQTT_HOST, MQTT_PORT)
rpi_mqtt_client.configureCredentials(CA_ROOT_CERT_FILE, THING_PRIVATE_KEY, THING_CERT_FILE)

rpi_mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
rpi_mqtt_client.configureOfflinePublishQueueing(-1)
rpi_mqtt_client.configureDrainingFrequency(2)
rpi_mqtt_client.configureConnectDisconnectTimeout(30)
rpi_mqtt_client.configureMQTTOperationTimeout(30)  

rpi_mqtt_client.connect()

while True:
    #rpi_mqtt_client.subscribe(MQTT_TOPIC, 1, customPostCallback)
    rpi_mqtt_client.subscribe('Master', 1, customMasterCallback)
    if action_type == "measurement":
        if received_variable == "temperature":
            post_meas(get_temperature())
            print("Temperature Sent")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "humidity":
            post_meas(get_humidity())
            print("Humidity Sent")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "moisture":
            post_meas(get_moisture())
            print("Moisture Sent")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "uv":
            post_meas(get_uv())
            print("UV Sent")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
    time.sleep(1)

# s3_aws_init(209, "temp", get_temperature())
   
 
