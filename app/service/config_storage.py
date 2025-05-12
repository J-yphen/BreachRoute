from flask import current_app

def get_storage_config():
    return {
        "aws": {
            "type": "s3",
            "key": current_app.config['S3_ACCESS_KEY'],
            "secret": current_app.config['S3_SECRET_KEY'],
            "bucket": current_app.config['S3_BUCKET_NAME'],
            "region": current_app.config['S3_REGION']
        },
        "gcp": {
            "type": "google_storage",
            "key": current_app.config['S3_ACCESS_KEY'],
            "secret": current_app.config['S3_SECRET_KEY'],
            "bucket": current_app.config['S3_BUCKET_NAME']
        },
        "azure": {
            "type": "azure_blobs",
            "key": current_app.config['S3_ACCESS_KEY'],
            "secret": current_app.config['S3_SECRET_KEY'],
            "bucket": current_app.config['S3_BUCKET_NAME']
        },
        "digitalocean": {
            "type": "digitalocean_spaces",
            "key": current_app.config['S3_ACCESS_KEY'],
            "secret": current_app.config['S3_SECRET_KEY'],
            "bucket": current_app.config['S3_BUCKET_NAME'],
            "region": current_app.config['S3_REGION']
        },
        "backblaze": {
            "type": "backblaze_b2",
            "key": current_app.config['S3_ACCESS_KEY'],
            "secret": current_app.config['S3_SECRET_KEY'],
            "bucket": current_app.config['S3_BUCKET_NAME']
        }
    }

"""
STORAGE_CONFIG = {
    "aws": {
        "type": "s3",
        "key": os.getenv("AWS_ACCESS_KEY"),
        "secret": os.getenv("AWS_SECRET_KEY"),
        "bucket": "your-aws-bucket",
        "region": "us-east-1"
    },
    "gcp": {
        "type": "google_storage",
        "key": os.getenv("GCP_SERVICE_ACCOUNT_EMAIL"),
        "secret": os.getenv("GCP_PRIVATE_KEY_PATH"),
        "bucket": "your-gcp-bucket"
    },
    "azure": {
        "type": "azure_blobs",
        "key": os.getenv("AZURE_ACCOUNT_NAME"),
        "secret": os.getenv("AZURE_ACCESS_KEY"),
        "bucket": "your-azure-container"
    },
    "digitalocean": {
        "type": "digitalocean_spaces",
        "key": os.getenv("DO_SPACES_KEY"),
        "secret": os.getenv("DO_SPACES_SECRET"),
        "bucket": "your-do-bucket",
        "region": "nyc3"
    },
    "backblaze": {
        "type": "backblaze_b2",
        "key": os.getenv("B2_KEY_ID"),
        "secret": os.getenv("B2_APP_KEY"),
        "bucket": "your-b2-bucket"
    },
    "minio": {
        "type": "minio",
        "key": os.getenv("MINIO_ACCESS_KEY"),
        "secret": os.getenv("MINIO_SECRET_KEY"),
        "bucket": "your-minio-bucket",
        "host": os.getenv("MINIO_HOST", "localhost"),
        "port": int(os.getenv("MINIO_PORT", "9000")),
        "secure": os.getenv("MINIO_SECURE", "false").lower() == "true"
    }
}
"""