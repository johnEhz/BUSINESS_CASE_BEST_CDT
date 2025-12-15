"""Lambda getFileUploadHistory: obtiene ultimos 25 registros de carga de archivos."""
from shared.utils.proxy_util import ProxyUtil
from shared.utils.string_utils import StringUtils
from shared.repository.file_history_repo import FileHistoryRepository
from decimal import Decimal
import json

files_history = FileHistoryRepository()

def lambda_handler(event, context):

    try:
        data = files_history.get_recent_uploads(limit=25)
        result = [
            {**record, 'ip': StringUtils.hide_chain(record['ip'], 3) if record.get('ip') else None}
            for record in data
        ]
        return ProxyUtil.create_response(200, {
            "data": result
        })

    except Exception as e:
        return ProxyUtil.create_response(500, {'error': f'Internal server error during processing: {str(e)}'})