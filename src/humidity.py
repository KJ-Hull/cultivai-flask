#humidity version 0.1.0
version = "0.1.1"
import RPi.GPIO as GPIO
import subprocess
import sys, json
from dotenv import load_dotenv
import time
import os
from control import get_output_num

GPIO.setmode(GPIO.BCM)

env_dir = "/home/pi/device_var.env"
load_dotenv(env_dir)
device_id = str(os.getenv("DEVICE_ID"))

def measure(pin):
    return Adafruit_DHT.read(Adafruit_DHT.DHT11, pin)

try:
    import Adafruit_DHT
except:
    install('Adafruit-DHT==1.3.4')
    import Adafruit_DHT


def get_humid(pin): 
    while True:
        time.sleep(1)
        humidity, temperature = measure(pin)
        if humidity is not None:
            print(humidity)
            break
        else:
            humidity, temperature = measure(pin)    
    hum = round(humidity,2)
    return hum

def get_humidity(temp_hum_pin):
    global device_id
    humidity = get_humid(temp_hum_pin)
    name = "humidity"
    output = get_output_num(name)
    json_humid= {"variable":output, output:str(humidity),"device_id":device_id, "value":str(humidity)}
    return json.dumps(json_humid)