import boto3, botocore
import uuid
import time
import json
import os.path
from os import path
s3_resource = boto3.resource('s3')

bucket_name = 'cultivai-test-bucket'

def check_bucket(bucket_name):
    try:
        s3_resource.meta.client.head_bucket(Bucket=bucket_name)
        return True, 0
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 403:
            print("Private Bucket. Forbidden Access!")
            return True, error_code
        elif error_code == 404:
            print("Bucket Does Not Exist!")
            return False, error_code

def create_bucket(bucket_name, s3_connection):
    error_code = 0
    bucket_response, error_code = check_bucket(bucket_name)
    if bucket_response:
        if error_code != 0:
            session = boto3.session.Session()
            current_region = session.region_name
            bucket_response = s3_connection.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                'LocationConstraint': current_region})
            print(bucket_name, current_region)
            return bucket_response
        else:
            print("Bucket already exists")
            return 0

def create_json_file(device_id, name, name_json):
    t = int(time.time())
    file_name = str(t) + '.json'
  
    temp_array = '{"device_id":"device_id", "name":"name", "variable":"name"}'
    
    temp_b = json.loads(name_json.data)
    print(temp_b)
    temp_dict = {**json.loads(temp_array), **temp_b}

    with open(file_name, 'w') as outfile:
        json.dump(temp_dict, outfile)

    if path.exists(file_name):
        return True, file_name
    else:
        return False, ""

def upload_file(device_id, name, name_json):
    file_name = ''
    response, file_name = create_json_file(device_id, name, name_json)
    print(file_name)
    if response:
        s3_resource.Object(bucket_name, file_name_.upload_file(Filename=file_name))
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
        print("Initialisation error. Please try again.")

    
    

    








