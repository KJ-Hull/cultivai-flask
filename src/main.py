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
import ttn

app_id = "test_kj"
access_key = "ttn-account-v2.ulvfdlPhaPPTiEbQSJ0uelweBFNVlWUARAJca4sipeU"
dev_id = "rpitest"
dev_eui = "00644C3EE7BBCE1E"
app_eui = "70B3D57ED003B7D4"
app_key = "800F0166400FB6365775915807094349"
endpoint_test = "https://94c16c2f5bccf564bc36432a5d11708c.m.pipedream.net"
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
with app.test_request_context():
    key = "Key.{}".format(access_key)
    endpoint = "https://console.thethingsnetwork.org/applications/test_kj/devices/register"
    params = {"lorawan_device": {
               "dev_id": "rpitest_2", 
               "dev_eui": "00E8B71CFD8A33DB", 
               "app_key": "916BE91922789D1402F9125BB8258CAB", 
               "app_eui": "70B3D57ED003B7D4",
               "app_id": "test_kj", 
               "activation_constraints": "local", 
               "uses32_bit_f_cnt": True}, 
             "app_id": "test_kj", 
             "dev_id": "rpitest_2",
             "end_device":"{}"}
    #params["lorawan_device":"dev_id"] = dev_id
    #params["lorawan_device":"dev_eui"] = dev_eui
    #params["lorawan_device":"app_key"] = app_key
    #params["lorawan_device":"app_eui"] = app_eui
    #params["lorawan_device":"app_id"] = app_id
    #params["app_id"] = app_id
    #params["dev_id"] = dev_id
    print(params)
    params_json = json.dumps(params)

    response = requests.post(endpoint,headers={'Authorization': key}, data = params_json)


    response_test = get_temperature()
    test = requests.post(endpoint_test, response_test.data)
    
    print(test)

    def uplink_callback(msg, client):
      print("Received uplink from ", msg.dev_id)
      print(msg)

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
        
