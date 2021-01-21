import json
import requests
from dotenv import load_dotenv
import os
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
#from aws import check_bucket, create_bucket, s3_aws_init, upload_file, create_json_file 

from control import set_status, get_status, get_temp, get_humid, get_moist, get_uv_light
import RPi.GPIO as GPIO
import requests
from datetime import timedelta, datetime
from flask import jsonify
import uuid
import time
from request_handling import post_meas

env_dir = "/home/pi/device_var.env"

temp_hum_pin = 17
moisture_pin = 5
uv_pin = 16
device_id = 'ef720fc0-20ca-4485-92fe-c95c67ee9307'
measurement_id = ""

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
    return jsonify(
        #measurement_id = str(uuid.uuid4()),
        variable=name,
        device_id = device_id,
        temperature=str(temperature)
        #name = name,
    )

def get_humidity():
    humidity = get_humid(temp_hum_pin)
    unit = "%"
    name = "humid"
    return jsonify(
        measurement_id = uuid.uuid4(),
        device_id = device_id,
        name = name,
        humidity=humidity,
        unit=unit,
        variable=name
    )

def get_moisture():
    moisture = get_moist(moisture_pin)
    name = "moist"
    return jsonify(
        measurement_id = uuid.uuid4(),
        device_id = device_id,
        name = name,
        moisture=moisture,
        variable=name
    )
    
def get_uv():
    uv = get_uv_light(uv_pin)
    name = uv
    return jsonify(
        measurement_id = uuid.uuid4(),
        device_id = device_id,
        name = name,
        uv=uv,
        variable=name
    )

post_meas(get_temperature())

# s3_aws_init(209, "temp", get_temperature())
   
 
