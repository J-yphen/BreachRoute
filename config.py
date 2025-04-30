import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-fallback-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY', None)
    S3_SECRET_KEY = os.getenv('S3_SECRET_KEY', None)
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', None)
    S3_REGION = os.getenv('S3_REGION', None)
    S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', None)

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}