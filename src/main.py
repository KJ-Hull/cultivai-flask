import json
import requests
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
measurement_id = ""

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
        measurement_id = uuid.uuid4(),
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
        measurement_id = uuid.uuid4(),
        device_id = device_id,
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
        measurement_id = uuid.uuid4(),
        device_id = device_id,
        name = name,
        moisture=moisture,
        variable=name
    )
    

@app.route('/uv')
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
    

#with app.test_request_context():
   # s3_aws_init(209, "temp", get_temperature())

   

    
try:
    # try the production run
    app.run(host='0.0.0.0', port=80)
except PermissionError:
    # we're probably on the developer's machine
    app.run(host='0.0.0.0', port=8080, debug=False)
        
