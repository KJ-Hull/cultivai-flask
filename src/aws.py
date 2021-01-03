import boto3, botocore
import uuid
import time

s3_resource = boto3.resource('s3')

bucket_name = 'cultivai-test-bucket'

def check_bucket(bucket_name, error_code):
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
        return True
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 403:
            print("Private Bucket. Forbidden Access!")
            return True
        elif error_code == 404:
            print("Bucket Does Not Exist!")
            return False

def create_bucket(bucket_name, s3_connection):
    if check_bucket(bucket_name, error_code):
        if error_code != 0:
            session = boto3.session.Session()
            current_region = session.region_name
            bucket_response = s3_connection.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                'LocationConstraint': current_region})
            print(bucket_name, current_region)
            return bucket_name, bucket_response






