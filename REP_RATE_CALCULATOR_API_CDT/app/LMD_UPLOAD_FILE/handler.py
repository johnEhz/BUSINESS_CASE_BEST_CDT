import base64
import uuid
import io
import cgi
from shared.database.db_config import get_db_connection
from shared.config import Config
from shared.utils.proxy_util import ProxyUtil
from shared.utils.s3_util import S3Util
from shared.validators.file_validator import FileValidator
from shared.repository.file_repo import FileRepository

s3_util = S3Util(Config.S3_BUCKET_NAME)
file_repo = FileRepository()

def upload_file(event, context):
    file_name = ""
    record_id = None
    try:
        client_info = ProxyUtil.extract_client_info(event)

        body = event['body']
        if isinstance(body, str):
            if event.get("isBase64Encoded", False):
                body = base64.b64decode(body)
            else:
                body = body.encode('utf-8')

        content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')

        if not content_type or 'multipart/form-data' not in content_type:
            return ProxyUtil.create_response(400, {'error': 'Contenido inválido. Se esperaba multipart/form-data.', 'success': False})

        environ = {'REQUEST_METHOD': 'POST'}
        fp = io.BytesIO(body)
        headers = {'content-type': content_type}
        form = cgi.FieldStorage(fp=fp, environ=environ, headers=headers)

        for key in form:
            part = form[key]
            if part.filename:
                filename = part.filename
                file_content = part.file.read()

                record_id = file_repo.create_file_record({
                    "file_name": filename,
                    "file_key": None,
                    "status": 1,
                    "error_detail": None,
                    "ip": client_info['ip'],
                    "agent": client_info['user_agent']
                })

                is_valid, message = FileValidator.is_valid_csv_file(file_content, filename)
                if not is_valid:
                    file_repo.update_dynamic_file_record_by_id(record_id, {
                        "file_name": filename,
                        "status": 2,
                        "error_detail": message
                    })
                    return ProxyUtil.create_response(400, {'error': message, 'success': False})

                s3_key = f"uploads/{uuid.uuid4()}-{filename}"
                s3_util.upload_file_to_s3(
                    s3_key=s3_key,
                    file_content=file_content,
                    content_type=part.type or 'application/octet-stream'
                )
                file_repo.update_dynamic_file_record_by_id(record_id, { "file_name": filename, "file_key": s3_key, "status": 4 })
                return ProxyUtil.create_response(200, {
                    'message': 'Rates file uploaded successfully, is being processed.',
                    'success': True
                })
            
        return ProxyUtil.create_response(400, {'error': 'No se encontró ningún archivo en la solicitud.', 'success': False})
    except Exception as e:
        file_repo.update_dynamic_file_record_by_id(record_id, {
            "file_name": filename,
            "status": 2,
            "error_detail": str(e)
        })
        return ProxyUtil.create_response(500, {'error': str(e), 'success': False})