import boto3, botocore
import uuid

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

#def create_bucket_name:
#error_code = 0

#if check_bucket(bucket_name, error_code):
 #   if error_code != 0:
 #       create_bucket(bucket_name)


