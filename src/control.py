import RPi.GPIO as GPIO
import subprocess
import sys, json
import time
from dotenv import load_dotenv
import os

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    import Adafruit_DHT
except:
    install('Adafruit-DHT==1.3.4')
    import Adafruit_DHT
 

# Set GPIO mode: GPIO.BCM or GPIO.BOARD
GPIO.setmode(GPIO.BCM) 

# Set mode for each gpio pin
GPIO.setup(5, GPIO.IN)
GPIO.setup(16, GPIO.IN)
temp_hum_pin = 17
moisture_pin = 5
uv_pin = 16
env_dir = "/home/pi/device_var.env"
load_dotenv(env_dir)
device_id = str(os.getenv("DEVICE_ID"))
def measure(pin):
    return Adafruit_DHT.read(Adafruit_DHT.DHT11, pin)

def set_status(pin,status):
    GPIO.output(pin, status)
    return GPIO.input(pin)

def get_status(pin):
    status = GPIO.input(pin)
    if status == 1:
        return True
    elif status == 0: 
        return False
    
def get_temp(pin):
    timeout = time.time() + 1
    while True:
        time.sleep(1)                                       #Gives time for sensor to be initialised. I think the program is operating too quickly for the sensor and is messing with the sys clock
        humidity, temperature = measure(pin)
        if temperature is not None or time.time() > timeout:
            print(temperature)
            break
        else:
            humidity, temperature = measure(pin)
    temp = round(temperature,2)
    return temp

def get_humid(pin):
    timeout = time.time() + 1  
    while True:
        time.sleep(1)
        humidity, temperature = measure(pin)
        if humidity is not None or time.time() > timeout:
            print(humidity)
            break
        else:
            humidity, temperature = measure(pin)

    hum = round(humidity,2)
    return hum

def get_moist(pin):
    timeout = time.time() + 1  
    while True:
        moist_pin_state = GPIO.input(pin)
        if moist_pin_state is not None:
            if moist_pin_state:
                soil_state = 'WET'
                break
            else:
                soil_state = 'NOT WET'
                break
    return soil_state

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

def get_output_num(variable_name):
    if variable_name == "temperature":
        return "output_1"
    if variable_name == "humidity":
        return "output_2"
    if variable_name == "moisture":
        return "output_3"
    if variable_name == "uv":
        return "output_4"

def get_temperature(temp_hum_pin):
    global device_id
    temperature = get_temp(temp_hum_pin)
    name = "temperature"
    output = get_output_num(name)
    json_temp = {"variable":name, output:str(temperature),"device_id":device_id}
    return json.dumps(json_temp)

def get_humidity(temp_hum_pin):
    global device_id
    humidity = get_humid(temp_hum_pin)
    name = "humidity"
    output = get_output_num(name)
    json_humid= {"variable":name, output:str(humidity),"device_id":device_id}
    return json.dumps(json_humid)

def get_moisture(moisture_pin):
    global device_id
    moisture = get_moist(moisture_pin)
    name = "moisture"
    output = get_output_num(name)
    json_moist= {"variable":name, output:moisture,"device_id":device_id}
    return json.dumps(json_moist)
    
def get_uv(uv_pin):
    global device_id
    uv = get_uv_light(uv_pin)
    name = "uv"
    output = get_output_num(name)
    json_uv= {"variable":name, output:uv,"device_id":device_id}
    return json.dumps(json_uv)

    



