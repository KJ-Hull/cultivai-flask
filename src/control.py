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
 
#import logging

#logging.basicConfig(format='%(levelname)s-%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG,filename='/App/gpio.log')

# Set GPIO mode: GPIO.BCM or GPIO.BOARD
GPIO.setmode(GPIO.BCM) 

# GPIO pins list based on GPIO.BOARD
# gpioList1 = [17,18]
# gpioList2 = [14,15]

# Set mode for each gpio pin

temp_hum_pin = 17
moisture_pin = 22
#GPIO.setup(gpioList2, GPIO.IN)


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
        if measure(pin):
            soil_state = "Wet"
            break
        else:
            soil_state = "Not Wet"
            break
    return soil_state

    



