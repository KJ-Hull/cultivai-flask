import requests
from dotenv import load_dotenv
import os
import json
from control import set_status, get_status, get_temp, get_humid, get_moist, get_uv_light, get_temperature, get_humidity, get_moisture, get_uv, post_schedule
env_dir = "/home/pi/device_var.env"

def post_meas(meas_json):
    load_dotenv(env_dir)
    endpoint = os.getenv("ENDPOINT")
    topic = os.getenv("POST_TOPIC")
   
    # Obtain JSON file of temperature and other fields
    data_json = json.loads(meas_json)

    # Create url based on AWS IoT Core HTTPS endpoint doc
    post_url_test = 'http://api.cultiv.ai/api/data/measurement/'
    login_headers = 'Api-Key ' + str(os.environ.get("API_KEY"))
    print(login_headers)
    # Make request
    publish = requests.request('POST',
            post_url_test,
            data=data_json,
            headers = {'Authorization':login_headers})

    # Print results, checking what response code is received
    print("Response status: ", str(publish.status_code))
    if publish.status_code == 200:
        print("Response body:", publish.text)

def MQTT_action(action_type, received_variable, received_dev_id):
    if action_type == "measurement":
        if received_variable == "temperature":
            post_meas(get_temperature())
            print("Temperature Sent")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "humidity":
            post_meas(get_humidity())
            print("Humidity Sent")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "moisture":
            post_meas(get_moisture())
            print("Moisture Sent")
            action_type = ''
            received_variable = ''
            received_dev_id = ''
        if received_variable == "uv":
            post_meas(get_uv())
            print("UV Sent")
            action_type = ''
            received_variable = ''
            received_dev_id = ''



