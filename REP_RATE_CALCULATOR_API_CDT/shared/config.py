import os

class Config:
    DEFAULT_ENV = os.environ.get('DEFAULT_ENV', 'dev')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'dev-cdt-quota-files')