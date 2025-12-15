"""Lambda getFileUploadHistoryDetail: obtiene los registros de detalle de carga de un archivo específico."""
from shared.utils.proxy_util import ProxyUtil
from shared.repository.file_history_repo import FileHistoryRepository

files_history = FileHistoryRepository()

def lambda_handler(event, context):

    try:
        query_params = event.get('queryStringParameters', {})

        if not query_params:
            return ProxyUtil.create_response(400, {'error': 'Missing query parameters.'})
            
        id_file = query_params.get('id_file')

        if not id_file:
            return ProxyUtil.create_response(400, {'error': 'Missing query parameters.'})
        
        history_detail = files_history.get_upload_history_detail(file_id=int(id_file))
        
        if not history_detail:
            return ProxyUtil.create_response(404, {'error': 'No upload history found for the specified file ID.'})

        return ProxyUtil.create_response(200, {
            "data": history_detail
        })

    except Exception as e:
        return ProxyUtil.create_response(500, {'error': f'Internal server error during processing: {str(e)}'})