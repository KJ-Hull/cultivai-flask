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
from request_handling import post_meas, MQTT_action, payload_handling, dev_publish_init

temp_hum_pin = 17
moisture_pin = 5
uv_pin = 16

measurement_id = ""

action_type = ''
received_dev_id = ''
received_variable = ''

MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_MASTER_TOPIC = "MASTER"
env_dir = "/home/pi/device_var.env"
load_dotenv(env_dir)
device_id = str(os.getenv("DEVICE_ID"))
print(device_id)
MQTT_HOST = os.getenv("THING_HOST")
client_id = "RPI_device"   #This needs to be the device's unique ID
MQTT_TOPIC = device_id + "/Get"
CA_ROOT_CERT_FILE = os.getenv("CA")
THING_CERT_FILE = os.getenv("CERT")
THING_PRIVATE_KEY = os.getenv("PRIV_KEY")
MQTT_ENDPOINT = os.getenv("ENDPOINT")

def customPostCallback(client, userdata, msg):
    global action_type 
    global received_dev_id
    global received_variable
    global device_id
    action_type, received_dev_id, received_variable, pin = payload_handling(msg.payload)
    if received_dev_id == device_id:
        MQTT_action(action_type, received_variable, received_dev_id, pin)
    else:
        print("Action not executed. Device ID mismatch.")

def customMasterCallback(client, userdata, msg):
    print("MASTER ACTION: \n")
    global action_type 
    global received_dev_id
    global received_variable
    action_type, received_dev_id, received_variable, pin = payload_handling(msg.payload)
    attempts = 3
    if received_dev_id == device_id:
        try:
            MQTT_action(action_type, received_variable, received_dev_id, pin)
        except:
            if attempts != 0:
                attempts = attempts - 1
                print("Error in sending occurred, trying again.")
                MQTT_action(action_type, received_variable, received_dev_id, pin)
            else:
                print("Error in sending. Please try again later.")
                os.system("python3 main.py")
                print("Rebooting Device")
                exit()
                
    else:
        print("Action not executed. Device ID mismatch.")

rpi_mqtt_client = AWSIoTMQTTClient(client_id)
rpi_mqtt_client.configureEndpoint(MQTT_HOST, MQTT_PORT)
rpi_mqtt_client.configureCredentials(CA_ROOT_CERT_FILE, THING_PRIVATE_KEY, THING_CERT_FILE)

rpi_mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
rpi_mqtt_client.configureOfflinePublishQueueing(-1)
rpi_mqtt_client.configureDrainingFrequency(2)
rpi_mqtt_client.configureConnectDisconnectTimeout(30)
rpi_mqtt_client.configureMQTTOperationTimeout(30)  

rpi_mqtt_client.connect()
dev_publish_init(rpi_mqtt_client)
attempts_action = 3
attempts_master = 3

while True:
    try:
        rpi_mqtt_client.subscribe(MQTT_TOPIC, 1, customPostCallback)
        print("Subscribed to " + MQTT_TOPIC)
    except:
        if attempts_action != 0:
            print("Error in Subscribing to "+ MQTT_TOPIC +", trying again.")
            rpi_mqtt_client.subscribe(MQTT_TOPIC, 1, customPostCallback)
        else:
            print("Error in subscribing to " + MQTT_TOPIC + ". Please try again later.")
            os.system("python3 main.py")
            print("Rebooting Device")
            attempts_master = 3
            exit()
    try:
        rpi_mqtt_client.subscribe('Master', 1, customMasterCallback)
        print("Subscribed to Master")
    except:
        if attempts_master != 0:
            print("Error in Subscribing to Master, trying again.")
            rpi_mqtt_client.subscribe('Master', 1, customMasterCallback)
        else:
             print("Error in subscribing to Master. Please try again later.")
             os.system("python3 main.py")
             print("Rebooting Device")
             attempts_master = 3
             exit()

# s3_aws_init(209, "temp", get_temperature())
   
 
