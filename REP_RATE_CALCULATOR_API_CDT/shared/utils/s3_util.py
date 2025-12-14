import boto3

class S3Util:
    def __init__(self, bucket_name, region='us-east-1'):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3', region_name=region)

    def upload_file_to_s3(self, s3_key, file_content, content_type):
        return self.s3.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=file_content,
            ContentType=content_type
        )
    
    def download_csv_file(self, s3_key):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=s3_key)
        file_content_bytes = response['Body'].read()
        file_content_str = file_content_bytes.decode('utf-8')
        return file_content_str