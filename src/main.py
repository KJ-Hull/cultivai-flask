import json
#from aws import check_bucket, create_bucket, s3_aws_init, upload_file, create_json_file 

from flask import Flask, request, flash, url_for, redirect, \
     render_template, jsonify, Response, send_file

from control import set_status, get_status, get_temp, get_humid, get_moist, get_uv_light
import RPi.GPIO as GPIO

from flask_cors import CORS
import requests
from datetime import timedelta, datetime

import uuid
import time
import ttn

app_id = "test_kj"
access_key = "ttn-account-v2.ulvfdlPhaPPTiEbQSJ0uelweBFNVlWUARAJca4sipeU"
dev_id = "rpitest"
dev_eui = "00644C3EE7BBCE1E"
app_eui = "70B3D57ED003B7D4"

app = Flask(__name__)
content_type_json = {'Content-Type': 'text/css; charset=utf-8'}
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)

temp_hum_pin = 17
moisture_pin = 5
uv_pin = 16
device_id = 209
measurement_id = uuid.uuid4()

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/status')
def get_stats():
    humidity = get_humid(temp_hum_pin)
    temperature = get_temp(temp_hum_pin)
    moisture = get_moist(moisture_pin)
    uv = get_uv_light(uv_pin)
    response = jsonify(
        humidity=humidity,
        temperature=temperature,
        moisture=moisture,
        uv=uv
    )  
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/schedule', methods = ['POST', 'GET'])
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

@app.route('/temperature')
def get_temperature():
    temperature = get_temp(temp_hum_pin)
    unit = "Celcius"
    name = "temp"
    return jsonify(
        measurement_id =measurement_id,
        device_id = device_id,
        name = name,
        variable=name,
        temperature=temperature
    )
    

@app.route('/humidity')
def get_humidity():
    humidity = get_humid(temp_hum_pin)
    unit = "%"
    name = "humid"
    return jsonify(
        name = name,
        humidity=humidity,
        unit=unit,
        variable=name
    )
    

@app.route('/moisture')
def get_moisture():
    moisture = get_moist(moisture_pin)
    name = "moist"
    return jsonify(
        name = name,
        moisture=moisture,
        variable=name
    )
    

@app.route('/uv')
def get_uv():
    uv = get_uv_light(uv_pin)
    name = uv
    return jsonify(
        name = name,
        uv=uv,
        variable=name
    )
    

#with app.test_request_context():
   # s3_aws_init(209, "temp", get_temperature())


def uplink_callback(msg, client):
  print("Received uplink from ", msg.dev_id)
  print(msg)

updates = {"app_eui":"", "dev_eui":""}
updates["app_eui"] = app_eui
updates["dev_eui"] = dev_eui
app_client = ttn.ApplicationClient(app_id, access_key)
device = app_client.device(dev_id)
app_client.update_device(dev_id, updates)
app_client.register_device(dev_id, device)

handler = ttn.HandlerClient(app_id, access_key)

# using mqtt client
mqtt_client = handler.data()
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.connect()
time.sleep(60)
mqtt_client.close()

# using application manager client
app_client =  handler.application()
my_app = app_client.get()
print(my_app)
my_devices = app_client.devices()
print(my_devices)


if __name__ == '__main__':
    try:
        # try the production run
        app.run(host='0.0.0.0', port=80)
    except PermissionError:
        # we're probably on the developer's machine
        app.run(host='0.0.0.0', port=8080, debug=False)
        
