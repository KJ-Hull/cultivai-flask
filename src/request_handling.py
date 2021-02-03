import requests
from dotenv import load_dotenv
import os
import json
from control import get_humid, get_temperature, get_humidity, get_moisture, get_uv, post_schedule
env_dir = "/home/pi/device_var.env"
temp_hum_pin = 17
moisture_pin = 5
uv_pin = 16
device_id = str(os.getenv("DEVICE_ID"))
def post_meas(meas_json):
    load_dotenv(env_dir)
    endpoint = os.getenv("ENDPOINT")
    topic = device_id + "/Post"
   
    # Obtain JSON file of temperature and other fields
    data_json = json.loads(meas_json)
    endpoint = str(os.getenv("ENDPOINT"))
    # Create url based on AWS IoT Core HTTPS endpoint doc
    post_url = 'https://'+ endpoint + ':8443/topics/' + topic + '?qos=1'
    # Make request
    publish = requests.request('POST',
            post_url,
            data=data_json, 
            cert=[str(os.getenv("CERT")), str(os.getenv("PRIV_KEY"))])

    # Print results, checking what response code is received
    print("Response status: ", str(publish.status_code))
    if publish.status_code == 200:
        print("Response body:", publish.text)

def payload_handling(payload):
    json_action = json.loads(payload)
    action_type = str(json_action["action_type"])
    print(action_type)
    received_dev_id = str(json_action["device_id"])
    print(received_dev_id)
    received_variable = str(json_action["variable"])
    print(received_variable)
    pin = 17
    if received_variable == "temperature" or received_variable == "humidity":
        pin = 17
    if received_variable == "uv":
        pin = 16
    if received_variable == "moisture":
        pin = 5

    return action_type, received_dev_id, received_variable, pin
    

def MQTT_action(action_type, received_variable, received_dev_id, pin):
    if action_type == "measurement":
        if received_variable == "temperature":
            post_meas(get_temperature(pin))
            print("Temperature Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "humidity":
            post_meas(get_humidity(pin))
            print("Humidity Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "moisture":
            post_meas(get_moisture(pin))
            print("Moisture Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "uv":
            post_meas(get_uv(pin))
            print("UV Sent \n")
            action_type = ''
            received_variable = ''
            received_dev_id = ''



