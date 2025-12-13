import boto3
import uuid
from requests_toolbelt.multipart import decoder

from shared.config import Config
from shared.proxy_response_helper import ProxyResponseHelper
from shared.utils.s3_util import S3Util

s3_util = S3Util(Config.S3_BUCKET_NAME)

def upload_file(event, context):

    try:
        body = event['body']
        content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')
        if not content_type or 'multipart/form-data' not in content_type:
            return ProxyResponseHelper.create_response(400, {'error': 'Contenido inválido. Se esperaba multipart/form-data.', 'success': False})
    
        form_data = decoder.MultipartDecoder(body, content_type)

        for part in form_data.parts:
            contet_disposition = part.headers.get(b'Content-Disposition', b'').decode()

            if "filename=" in contet_disposition:
                filename = contet_disposition.split("filename=")[-1].replace('"', '')
                s3_key = f"uploads/{uuid.uuid4()}-{filename}"

                s3_util.upload_file_to_s3(
                    s3_key=s3_key,
                    file_content=part.content,
                    content_type=part.headers.get(b'Content-Type', b'application/octet-stream').decode()
                )

                return ProxyResponseHelper.create_response(200,
                {   
                    'message': f'Rates file uploaded successfully.',
                    'success': True
                })
        return ProxyResponseHelper.create_response(400, {'error': 'No se encontró ningún archivo en la solicitud.', 'success': False})
    except Exception as e:
        return ProxyResponseHelper.create_response(500, {'error': str(e), 'success': False})