import RPi.GPIO as GPIO
import time
import subprocess
import sys, json
import time

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
        humidity, temperature = measure(pin)
        if temperature is not None and humidity is not None or time.time() > timeout:
            break
        else:
            humidity, temperature = measure(pin)
    temp = round(temperature,2)
    return temp

def get_humid(pin):
    timeout = time.time() + 1  
    while True:
        humidity, temperature = measure(pin)
        if humidity is not None and temperature is not None or time.time() > timeout:
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

def get_temperature(temp_hum_pin):
    temperature = get_temp(temp_hum_pin)
    name = "temperature"
    json_temp = {"variable":name, "value":str(temperature),"device_id":device_id}
    return json.dumps(json_temp)

def get_humidity(temp_hum_pin):
    humidity = get_humid(temp_hum_pin)
    name = "humidity"
    json_humid= {"variable":name, "value":str(humidity),"device_id":device_id}
    return json.dumps(json_humid)

def get_moisture(moisture_pin):
    moisture = get_moist(moisture_pin)
    name = "moisture"
    json_moist= {"variable":name, "value":moisture,"device_id":device_id}
    return json.dumps(json_moist)
    
def get_uv(uv_pin):
    uv = get_uv_light(uv_pin)
    name = "uv"
    json_uv= {"variable":name, "value":uv,"device_id":device_id}
    return json.dumps(json_uv)

    



