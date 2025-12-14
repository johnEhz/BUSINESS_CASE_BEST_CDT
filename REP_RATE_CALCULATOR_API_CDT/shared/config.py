import os
class Config:
    DEFAULT_ENV = os.environ.get('DEFAULT_ENV', 'dev')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'dev-cdt-quota-files')
    MAX_FILE_SIZE_MB = os.environ.get('MAX_FILE_SIZE_MB', '5')
    ALLOWED_FILE_EXTENSIONS = os.environ.get('ALLOWED_FILE_EXTENSIONS', '.csv')
    CSV_DELIMITER = os.environ.get('CSV_DELIMITER', ';')
    DB_CONFIG = {
        'host': os.environ.get('DB_HOST'),
        'port': int(os.environ.get('DB_PORT')),
        'database': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USERNAME'),
        'password': os.environ.get('DB_PASSWORD'),
    }
    FILE_REQUIRED_COLUMNS = ['consecutivo', 'banco', 'minplazo', 'maxplazo', 'minmonto', 'maxmonto', 'tasa', 'fecha']