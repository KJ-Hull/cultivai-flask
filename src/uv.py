#uv version 0.1.0
version = "0.1.1"
import RPi.GPIO as GPIO
import subprocess
import sys, json
import time
from dotenv import load_dotenv
import os
from control import get_output_num, pin_handling

GPIO.setmode(GPIO.BCM) 
uv_pin = pin_handling("uv")
GPIO.setup(uv_pin, GPIO.IN)

env_dir = "/home/pi/device_var.env"
load_dotenv(env_dir)
device_id = str(os.getenv("DEVICE_ID"))

def get_uv_light(pin):
    timeout = time.time() + 1  
    while True:
        UV_pin_state = GPIO.input(pin)
        if UV_pin_state is not None:
            if UV_pin_state:
                UV_state = 'UV PRESENT'
                break
            else:
                UV_state = 'NO UV PRESENT'
                break
    return UV_state

def get_uv(uv_pin):
    global device_id
    uv = get_uv_light(uv_pin)
    name = "uv"
    output = get_output_num(name)
    json_uv= {"variable":output, output:uv,"device_id":device_id, "value":str(uv)}
    return json.dumps(json_uv)

