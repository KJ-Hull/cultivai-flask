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

    



