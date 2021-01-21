import requests
from dotenv import load_dotenv
import os

env_dir = "/home/pi/device_var.env"

def post_meas(meas_json):
    load_dotenv(env_dir)
    endpoint = os.getenv("ENDPOINT")
    topic = os.getenv("POST_TOPIC")
   
    # Obtain JSON file of temperature and other fields
    data_json = meas_json

    # Create url based on AWS IoT Core HTTPS endpoint doc
    iot_url = 'https://' + endpoint + ':8443/topics/' + topic + '?qos=1'
   
    # Make request
    publish = requests.request('POST',
            iot_url,
            data=data_json,
            cert=[os.getenv("CERT"), os.getenv("PRIV_KEY")])

    # Print results, checking what response code is received
    print("Response status: ", str(publish.status_code))
    if publish.status_code == 200:
        print("Response body:", publish.text)



