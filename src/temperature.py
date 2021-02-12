version = "0.1.0"
import RPi.GPIO as GPIO
import subprocess
import sys, json
import time
from request_handling import pin_handling
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


def get_temp(pin):
    while True:
        humidity, temperature = measure(pin)
        if temperature is not None:
            print(temperature)
            break
        else:
            humidity, temperature = measure(pin)
    temp = round(temperature,2)
    return temp

def get_temperature(temp_hum_pin):
    global device_id
    temperature = get_temp(temp_hum_pin)
    name = "temperature"
    output = get_output_num(name)
    json_temp = {"variable":output, output:str(temperature),"device_id":device_id, "value":str(temperature)}
    return json.dumps(json_temp)