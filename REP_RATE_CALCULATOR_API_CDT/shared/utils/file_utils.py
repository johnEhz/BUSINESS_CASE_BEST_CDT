import json
import io
import csv
from shared.config import Config
from decimal import Decimal
from datetime import datetime
class FileUtil:
    @staticmethod
    def csv_reader(content_bytes, delimiter=Config.CSV_DELIMITER):
        file_content_str = content_bytes.decode('utf-8')
        csv_file_in_memory = io.StringIO(file_content_str)
        csv_reader = csv.reader(csv_file_in_memory, delimiter=delimiter)
        return csv_reader
    
    @staticmethod
    def _clean_decimal(value_str):
        if not value_str:
            raise ValueError("Valor numérico vacío.")
        return Decimal(value_str.replace('.', '').replace(',', '.'))

    @staticmethod
    def validate_records_csv(csv_content: str) -> list:
        csv_file_in_memory = io.StringIO(csv_content)
        csv_reader = csv.reader(csv_file_in_memory, delimiter=Config.CSV_DELIMITER)
        expected_columns = len(Config.FILE_REQUIRED_COLUMNS)
        end_db_data = []

        for i, row in enumerate(csv_reader):
            try:
                if i == 0: continue
                row_index = i
                current_row_warnings = []
                db_ready_fields = {}
                try:
                    consecutivo, banco, min_plazo, max_plazo, min_monto_str, max_monto_str, tasa_str, fecha_str = row[:expected_columns]
                except ValueError:
                    current_row_warnings.append({
                        "alert_type": 6,
                        "message": f"Fila {row_index}: Número incorrecto de columnas. Se esperaban {expected_columns}, pero se recibieron {len(row)}."
                    })

                try:
                    db_ready_fields['consecutivo'] = int(consecutivo)
                    db_ready_fields['banco'] = int(banco)
                    db_ready_fields['min_plazo'] = int(min_plazo)
                    db_ready_fields['max_plazo'] = int(max_plazo)
                    db_ready_fields['min_monto'] = FileUtil._clean_decimal(min_monto_str)
                    db_ready_fields['max_monto'] = FileUtil._clean_decimal(max_monto_str)
                    db_ready_fields['tasa'] = Decimal(tasa_str.replace('%', '').replace(',', '.'))
                    db_ready_fields['fecha'] = datetime.strptime(fecha_str, '%d/%m/%Y').date()

                except (ValueError, Exception) as e:
                    current_row_warnings.append({
                        "alert_type": 7,
                        "message": f"Fila {row_index}: Error de formato/conversión: {e}. Datos: {row}"
                    })

                check_non_zero = {
                    'min_monto': db_ready_fields['min_monto'],
                    'max_monto': db_ready_fields['max_monto'],
                    'tasa': db_ready_fields['tasa']
                }

                for field, value in check_non_zero.items():
                    if value <= 0:
                        current_row_warnings.append({
                            "alert_type": 4,
                            "message": f"El campo {field} tiene un valor no positivo: {value}."
                        })
                        
                if db_ready_fields['min_monto'] > db_ready_fields['max_monto']:
                    current_row_warnings.append({
                        "alert_type": 3,
                        "message": f"El monto mínimo ({db_ready_fields['min_monto']}) es mayor que el monto máximo ({db_ready_fields['max_monto']})."
                    })

                if db_ready_fields['min_plazo'] > db_ready_fields['max_plazo']:
                    current_row_warnings.append({
                        "alert_type": 3,
                        "message": f"El plazo mínimo ({db_ready_fields['min_plazo']}) es mayor que el plazo máximo ({db_ready_fields['max_plazo']})."
                    })
                
                has_warnings = bool(current_row_warnings)

                db_ready_fields['has_warnings'] = has_warnings
                db_ready_fields['warnings'] = list(current_row_warnings)

                end_db_data.append(db_ready_fields)
            except Exception as e:
                print(f"Error processing row {i}: {e}")
        return end_db_data