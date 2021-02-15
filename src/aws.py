version = "0.1.1"

import boto3, botocore
import uuid
import time
import json
import os.path
from os import path
s3_resource = boto3.resource('s3')

bucket_name = 'cultivaisoftware'
file_name = ''


def check_bucket(bucket_name):
    try:
        s3_resource.meta.client.head_bucket(Bucket=bucket_name)
        return True, 0
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 403:
            print("Private Bucket. Forbidden Access!")
            return False, error_code
        elif error_code == 404:
            print("Bucket Does Not Exist!")
            return True, error_code

def download_file(file_name):
    global bucket_name
    status, status_code = check_bucket(bucket_name)
    if status == True and status_code == 0:
        s3 = boto3.resource('s3')
        output = f"/home/pi/downloads/{file_name}"
        s3.Bucket(bucket_name).download_file(file_name)
        dev_state = "Active"
        return dev_state
    else:
        dev_state = "Error"
        return dev_state

def create_bucket(bucket_name, s3_connection):
    error_code = 0
    bucket_response, error_code = check_bucket(bucket_name)
    print(error_code)
    if bucket_response:
        if error_code != 0:
            session = boto3.session.Session()
            current_region = session.region_name
            bucket_response = s3_connection.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                'LocationConstraint': current_region})
            
            return bucket_response
        else:
            print("Bucket already exists")
            return 0


def create_json_file(device_id, name, name_json):
    t = int(time.time())
    file_name = device_id + str(t) + '.json'
    temp_b = json.loads(name_json.data)
    with open(file_name, 'w') as outfile:
        json.dump(temp_b, outfile)

    if path.exists(file_name):
        return True, file_name
    else:
        return False, ""

def upload_file(device_id, name, name_json):
    response, file_name = create_json_file(device_id, name, name_json)
    if response:
        s3_resource.Object(bucket_name, file_name).upload_file(Filename=file_name)
        print('file uploaded')
        return True
    else:
        print('file does not exist')
        return False

def s3_aws_init(device_id, name, name_json):
    bucket_response = create_bucket(bucket_name, s3_resource)

    if bucket_response == 0:
        upload_file(device_id, name, name_json)
    else:
        print("Bucket Created. File will be uploaded for first time.")
        upload_file(device_id, name, name_json)
    
    

    








