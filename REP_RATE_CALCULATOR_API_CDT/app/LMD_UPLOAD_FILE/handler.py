import json
import boto3
import os

def upload_file(event, context):
    node_env = os.environ.get('DEFAULT_ENV', 'dev')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Upload file function in {node_env}',
            'api_key_configured': True,
            'input': event
        })
    }