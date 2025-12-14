import io
import csv
from shared.config import Config
from shared.utils.proxy_util import ProxyUtil
from shared.utils.s3_util import S3Util
from shared.utils.file_utils import FileUtil
from shared.repository.file_repo import FileRepository

file_repo = FileRepository()
s3_util = S3Util(Config.S3_BUCKET_NAME)

def process_s3_event(event, context):
    try:
        for record in event['Records']:
            s3_info = record['s3']
            object_key = s3_info['object']['key']
            normalized_key = object_key.replace('+', ' ')

            updated = file_repo.update_dynamic_file_record_by_key(normalized_key, { "status": 5 })
            if updated == 0:
                raise ValueError(f"No se encontró el registro de archivo para la clave: {object_key}")
            
            file_content_bytes = s3_util.download_file(normalized_key)
            csv_reader = FileUtil.csv_reader(file_content_bytes)
            print(csv_reader)
        return ProxyUtil.create_response(200, {
            'message': 'File processed successfully.',
            'success': True
        })
    except Exception as e:
        return ProxyUtil.create_response(500, {
            'error': str(e),
            'success': False
        })