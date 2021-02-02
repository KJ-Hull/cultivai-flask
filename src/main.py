import json
import requests
from dotenv import load_dotenv
import os
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
#from aws import check_bucket, create_bucket, s3_aws_init, upload_file, create_json_file 

from control import set_status, get_status, get_temp, get_humid, get_moist, get_uv_light, get_temperature, get_humidity, get_moisture, get_uv, post_schedule
import RPi.GPIO as GPIO
import requests
from datetime import timedelta, datetime
import uuid
import time
from request_handling import post_meas, MQTT_action, payload_handling

temp_hum_pin = 17
moisture_pin = 5
uv_pin = 16
device_id = 'ef720fc0-20ca-4485-92fe-c95c67ee9307'
measurement_id = ""

action_type = ''
received_dev_id = ''
received_variable = ''

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
    action_type, received_dev_id, received_variable, pin = payload_handling(msg.payload)
    MQTT_action(action_type, received_variable, received_dev_id, pin)

def customMasterCallback(client, userdata, msg):
    print("Received Master Action")
    global action_type 
    global received_dev_id
    global received_variable
    action_type, received_dev_id, received_variable, pin = payload_handling(msg.payload)
    MQTT_action(action_type, received_variable, received_dev_id, pin)

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
    rpi_mqtt_client.subscribe(MQTT_TOPIC, 1, customPostCallback)
    rpi_mqtt_client.subscribe('Master', 1, customMasterCallback)
    time.sleep(1)

# s3_aws_init(209, "temp", get_temperature())
   
 
