from shared.config import Config
import csv
from io import StringIO

class FileValidator:
    @staticmethod
    def is_valid_csv_file(file_content: bytes, file_name: str, ) -> (bool, str):
        allowed_extensions = [ext.strip().lower() for ext in Config.ALLOWED_FILE_EXTENSIONS.split(',')]

        if not any(file_name.lower().endswith(ext) for ext in allowed_extensions):
            return False, f"Invalid file extension. Allowed extensions are: {', '.join(allowed_extensions)}"

        if len(file_content) == 0:
            return False, "File is empty."

        if len(file_content) > int(Config.MAX_FILE_SIZE_MB) * 1024 * 1024:
            return False, f"File size exceeds the maximum limit of {Config.MAX_FILE_SIZE_MB} MB."
        
        try:
            decoded_content = file_content.decode('utf-8')
        except UnicodeDecodeError:
            return False, "El archivo no se puede decodificar como UTF-8."
        
        reader = csv.DictReader(StringIO(decoded_content), delimiter=Config.CSV_DELIMITER)
        file_columns = reader.fieldnames

        if not file_columns:
            return False, "File has no columns."

        for column in Config.FILE_REQUIRED_COLUMNS:
            if column not in file_columns:
                return False, f"Missing required column: {column}"

        return True, "File is valid."