from shared.database.db_config import get_db_connection

GET_FILE_UPLOAD_RECORDS = """
    SELECT id, file_name, file_key, status, error_detail, ip, agent
    FROM upload_file
"""

CREATE_FILE_UPLOAD_RECORD = """
    INSERT INTO upload_file (file_name, file_key, status, error_detail, ip, agent)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

UPDATE_FILE_UPLOAD_RECORD = """
    UPDATE upload_file
    SET status = %s, error_detail = %s
    WHERE id = %s
"""

class FileRepository:
    def __init__(self):
        pass

    def get_all(self):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(GET_FILE_UPLOAD_RECORDS)
                    return cursor.fetchall()
        except Exception as err:
            print(f"Error on repository (get_all): {err}")
            raise

    def create_file_record(self, file_data):
        """Crea un nuevo registro de archivo subido"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(CREATE_FILE_UPLOAD_RECORD, (
                        file_data['file_name'],
                        file_data['file_key'],
                        file_data['status'],
                        file_data.get('error_detail'),
                        file_data.get('ip'),
                        file_data.get('agent'),
                    ))
                    conn.commit()
                    # Para MySQL, obtener el último ID insertado
                    cursor.execute("SELECT LAST_INSERT_ID() as id")
                    result = cursor.fetchone()
                    return result['id'] if result else None
        except Exception as err:
            print(f"Error on repository (create_file_record): {err}")
            raise

    def update_dynamic_file_record_by_id(self, record_id: int, update_data: dict) -> int:
        """Actualiza dinámicamente campos de un registro de archivo"""
        if not update_data:
            return 0

        set_clauses = []
        values = []

        for key, value in update_data.items():
            set_clauses.append(f"`{key}` = %s")
            values.append(value)

        set_clause = ", ".join(set_clauses)
        values.append(record_id)
        query = f"UPDATE upload_file SET {set_clause} WHERE id = %s"

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, tuple(values))
                    conn.commit()
                    return cursor.rowcount
        except Exception as err:
            print(f"Error on repository (update_dynamic_file_record): {err}")
            raise

    def update_dynamic_file_record_by_key(self, file_key: str, update_data: dict) -> int:
        """Actualiza dinámicamente campos de un registro de archivo"""
        if not update_data:
            return 0

        set_clauses = []
        values = []

        for key, value in update_data.items():
            set_clauses.append(f"`{key}` = %s")
            values.append(value)

        set_clause = ", ".join(set_clauses)
        values.append(file_key)
        query = f"UPDATE upload_file SET {set_clause} WHERE file_key = %s"

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, tuple(values))
                    conn.commit()
                    return cursor.rowcount
        except Exception as err:
            print(f"Error on repository (update_dynamic_file_record): {err}")
            raise