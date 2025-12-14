import json
import io
import csv
from shared.config import Config

class FileUtil:
    @staticmethod
    def csv_reader(content_bytes, delimiter=Config.CSV_DELIMITER):
        file_content_str = content_bytes.decode('utf-8')
        csv_file_in_memory = io.StringIO(file_content_str)
        csv_reader = csv.reader(csv_file_in_memory, delimiter=delimiter)
        return csv_reader

    def extract_client_info(event):
        headers = event.get("headers", {})
        ip_address = headers.get("X-Forwarded-For") or \
                    event.get("requestContext", {}).get("identity", {}).get("sourceIp", "unknown")
        user_agent = headers.get("User-Agent") or headers.get("user-agent") or "unknown"

        return {"ip": ip_address, "user_agent": user_agent}