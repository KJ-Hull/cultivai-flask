#moisture version 0.1.0
version = "0.1.0"
import RPi.GPIO as GPIO
import subprocess
import sys, json
import time
from dotenv import load_dotenv
import os
from request_handling import pin_handling
from control import get_output_num

GPIO.setmode(GPIO.BCM) 
uv_pin = pin_handling("moisture")
GPIO.setup(uv_pin, GPIO.IN)

env_dir = "/home/pi/device_var.env"
load_dotenv(env_dir)
device_id = str(os.getenv("DEVICE_ID"))

def get_moist(pin):
    timeout = time.time() + 1  
    GPIO.setup(5, GPIO.IN)
    while True:
        try:
            moist_pin_state = GPIO.input(pin)
        except:
            GPIO.setup(5, GPIO.IN)
            moist_pin_state = GPIO.input(pin)

        if moist_pin_state is not None:
            if moist_pin_state:
                soil_state = True
                break
            else:
                soil_state = False
                break
    return soil_state

def get_moisture(moisture_pin):
    global device_id
    moisture = get_moist(moisture_pin)
    name = "moisture"
    output = get_output_num(name)
    json_moist= {"variable":output, output:moisture,"device_id":device_id, "value":str(moisture)}
    return json.dumps(json_moist)
