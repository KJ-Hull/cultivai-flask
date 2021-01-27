import json
import requests
from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt
import ssl
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

MQTT_PORT = 8443
MQTT_KEEPALIVE_INTERVAL = 45

env_dir = "/home/pi/device_var.env"
load_dotenv(env_dir)


MQTT_TOPIC = os.getenv("GET_TOPIC")
CA_ROOT_CERT_FILE = os.getenv("CA")
THING_CERT_FILE = os.getenv("CERT")
THING_PRIVATE_KEY = os.getenv("PRIV_KEY")
MQTT_ENDPOINT = os.getenv("ENDPOINT")

MQTT_HOST = 'https://' + MQTT_ENDPOINT + ':8443/topics/' + MQTT_TOPIC + '?qos=1'
print(MQTT_HOST)
def on_connect(mosq, obj, rc):
    mqttc.subscribe(MQTT_TOPIC, 0)

def on_message(mosq, obj, msg):
    json_action = msg.payload
    action_type = json_action["action_type"]
    print(action_type)
    received_dev_id = json_action["device_id"]
    print(received_dev_id)
    received_variable = json_action["variable"]
    print(received_variable)


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed to Topic: " + 
	MQTT_MSG + " with QoS: " + str(granted_qos))

print("hello")
mqttc = mqtt.Client()

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

if action_type == "measurement":
    if received_variable == "temperature":
        post_meas(get_temperature())
    if received_varaible == "humidity":
        post_meas(get_humidity())
    if received_variable == "moisture":
        post_meas(get_moisture())
    if received_variable == "uv":
        post_meas(get_uv())

mqttc.loop_forever()

# s3_aws_init(209, "temp", get_temperature())
   
 
