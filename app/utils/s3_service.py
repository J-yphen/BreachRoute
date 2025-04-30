import boto3
from flask import current_app, g

def get_s3_client():
    """Returns the S3 client from the app context."""
    if 's3_client' not in g:
        g.s3_client = boto3.client(
            's3',
            endpoint_url=current_app.config['S3_ENDPOINT_URL'],
            aws_access_key_id=current_app.config['S3_ACCESS_KEY'],
            aws_secret_access_key=current_app.config['S3_SECRET_KEY'],
            region_name=current_app.config['S3_REGION']
        )
    return g.s3_client

def upload_file(file_path, object_name):
    """Upload a file to the S3 bucket."""
    s3 = get_s3_client()
    if s3:
        try:
            s3.upload_file(file_path, current_app.config['S3_BUCKET_NAME'], object_name)
            print(f"File {object_name} uploaded successfully.")
        except Exception as e:
            print(f"Error uploading file: {e}")

def delete_file(object_name):
    """Delete a file from the S3 bucket."""
    s3 = get_s3_client()
    if s3:
        try:
            s3.delete_object(Bucket=current_app.config['S3_BUCKET_NAME'], Key=object_name)
            print(f"File {object_name} deleted successfully.")
        except Exception as e:
            print(f"Error deleting file: {e}")

def get_file(object_name):
    """Download a file from S3 and return its content."""
    s3 = get_s3_client()
    if s3:
        try:
            file_content = s3.get_object(Bucket=current_app.config['S3_BUCKET_NAME'], Key=object_name)['Body'].read()
            return file_content
        except Exception as e:
            print(f"Error retrieving file: {e}")
            return None
    else:
        return None