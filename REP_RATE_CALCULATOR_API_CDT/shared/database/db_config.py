import pymysql
import os
from shared.config import Config
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection():
    """Context manager que crea una conexión MySQL y la cierra al salir."""
    conn = None
    try:
        conn = pymysql.connect(
            host=Config.DB_CONFIG['host'],
            port=Config.DB_CONFIG['port'],
            user=Config.DB_CONFIG['user'],
            password=Config.DB_CONFIG['password'],
            database=Config.DB_CONFIG['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        logger.debug("Conexión MySQL creada")
        yield conn
    except Exception:
        logger.exception("Error de conexión a la BD MySQL")
        raise
    finally:
        if conn is not None:
            conn.close()
            logger.debug("Conexión MySQL cerrada")