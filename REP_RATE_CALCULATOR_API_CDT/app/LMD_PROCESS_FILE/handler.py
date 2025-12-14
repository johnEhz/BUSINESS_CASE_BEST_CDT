"""Lambda processFile: dispara por evento S3 para validar y cargar tasas desde el CSV a la BD, actualizando estados del archivo."""
import io
import csv
import json
from shared.config import Config
from shared.utils.proxy_util import ProxyUtil
from shared.utils.s3_util import S3Util
from shared.utils.file_utils import FileUtil
from shared.repository.file_repo import FileRepository
from shared.repository.rates_repo import RatesReporistory

file_repo = FileRepository()
rates_repo = RatesReporistory()
s3_util = S3Util(Config.S3_BUCKET_NAME)

def process_s3_event(event, context):
    updated_file = None
    try:
        for record in event['Records']:
            s3_info = record['s3']
            object_key = s3_info['object']['key']
            normalized_key = object_key.replace('+', ' ')

            updated_file = file_repo.update_dynamic_file_record_by_key(normalized_key, { "status": 5 })
            if not updated_file:
                raise ValueError(f"No se encontró el registro de archivo para la clave: {object_key}")

            file_content_str = s3_util.download_csv_file(normalized_key)
            csv_data = FileUtil.validate_records_csv(file_content_str)
            rates_repo.update_many_rates(csv_data, updated_file['id'])
            file_repo.update_dynamic_file_record_by_id(updated_file['id'], { "status": 3 })

        return ProxyUtil.create_response(200, {
            'message': 'File processed successfully.',
            'success': True,
        })
    except Exception as e:
        file_repo.update_dynamic_file_record_by_id(updated_file['id'], { "status": 2, "error_detail": str(e) })
        return ProxyUtil.create_response(500, {
            'error': str(e),
            'success': False
        })