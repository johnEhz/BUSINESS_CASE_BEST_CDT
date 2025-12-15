from shared.database.db_config import get_db_connection

GET_FILE_UPLOAD_HISTORY = """
    SELECT 
        f.id, f.file_name, f.status, f.error_detail, f.ip, f.agent, f.created_at, count(r.id) as warnings,
        CASE 
            WHEN r.id  IS NOT NULL THEN 1
            ELSE 0
        END AS has_warnings
    FROM upload_file f
    LEFT JOIN rate_alert r ON f.id  = r.id_file
    GROUP BY f.id
    ORDER BY f.created_at DESC
    LIMIT %s
"""

GET_FILE_UPLOAD_HISTORY_DETAIL = """
    SELECT ra.rate_consecutive, rad.id_alert_type, rad.message, rad.created_at 
    FROM rate_alert ra
    JOIN rate_alert_detail rad ON ra.id = rad.id_rate_alert
    WHERE ra.id_file = %s
"""

class FileHistoryRepository:
    def __init__(self):
        pass

    def get_recent_uploads(self, limit=20):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(GET_FILE_UPLOAD_HISTORY, (limit,))
                    return cursor.fetchall()
        except Exception as err:
            print(f"Error on repository (get_recent_uploads): {err}")
            raise

    def get_upload_history_detail(self, file_id: int):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(GET_FILE_UPLOAD_HISTORY_DETAIL, (file_id,))
                    return cursor.fetchall()
        except Exception as err:
            print(f"Error on repository (get_upload_history_detail): {err}")
            raise