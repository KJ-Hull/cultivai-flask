import json

from flask import Flask, request, flash, url_for, redirect, \
     render_template, jsonify, Response, send_file

from control import set_status, get_status, get_temp, get_humid
import RPi.GPIO as GPIO

from picamera import PiCamera
from flask_cors import CORS
import requests
from datetime import timedelta, datetime

#camera = PiCamera()

app = Flask(__name__)
content_type_json = {'Content-Type': 'text/css; charset=utf-8'}
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)

temp_hum_pin = 15


lastfile = "static/1.jpg"

server_url = "https://hoog-cluster.herokuapp.com/api/"


@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/status')
def get_stats():
    humidity = get_humid(temp_hum_pin)
    temperature = get_temp(temp_hum_pin)
    
    with open('schedule.json') as f:
            data = json.load(f)
    response = jsonify(
        humidity=humidity,
        temperature=temperature,
        schedule=data,
    )  
    response.headers.add('Access-Control-Allow-Origin', '*')
    #response.body.add(image)
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
    return jsonify(
        temperature=temperature
    )

@app.route('/humidity')
def get_humidity():
    humidity = get_humid(temp_hum_pin)
    return jsonify(
        humidity=humidity
    )


if __name__ == '__main__':
    try:
        # try the production run
        app.run(host='0.0.0.0', port=80)
    except PermissionError:
        # we're probably on the developer's machine
        app.run(host='127.0.0.1', port=5000, debug=False)
        
