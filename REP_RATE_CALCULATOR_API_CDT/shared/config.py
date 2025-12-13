import os

class Config:
    DEFAULT_ENV = os.environ.get('DEFAULT_ENV', 'dev')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'dev-cdt-quota-files')
    MAX_FILE_SIZE_MB = os.environ.get('MAX_FILE_SIZE_MB', '5')
    ALLOWED_FILE_EXTENSIONS = os.environ.get('ALLOWED_FILE_EXTENSIONS', '.csv')
    CSV_DELIMITER = os.environ.get('CSV_DELIMITER', ';')
    FILE_REQUIRED_COLUMNS = ['consecutivo', 'banco', 'minplazo', 'maxplazo', 'minmonto', 'maxmonto', 'tasa', 'fecha']