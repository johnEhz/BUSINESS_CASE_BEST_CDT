from shared.database.db_config import get_db_connection
from typing import List, Dict, Tuple, Any

INSERT_QUERY = """
    INSERT INTO rates (id_file, consecutive, id_bank, min_term, max_term, min_amount, max_amount, quota, last_update)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

INSERT_RATE_WARNING_QUERY = """
    INSERT INTO rate_alert (id_rate, id_file, rate_consecutive)
    VALUES (%s, %s, %s)
"""

INSERT_RATE_WARNING_DETAIL= """
    INSERT INTO rate_alert_detail (id_rate_alert, id_alert_type, message)
    VALUES (%s, %s, %s)
"""

GET_RATES_BY_TERM_AND_AMOUNT_QUERY = """
    SELECT consecutive, id_bank, quota, min_term, max_term, min_amount, max_amount, last_update
    FROM rates
    WHERE %s BETWEEN min_term AND max_term
    AND %s BETWEEN min_amount AND max_amount
"""

DELETE_RATES_QUERY = """
    DELETE FROM rates
"""

DELETE_RATES_ALERT_QUERY = """
    DELETE FROM rate_alert
"""

DELETE_RATE_ALERT_DETAIL_QUERY = """
    DELETE FROM rate_alert_detail
"""

class RatesReporistory:
    def __init__(self):
        pass

    def update_many_rates(self, rates_data: list[Dict[str, Any]], file_id: int) -> None:
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:  
                    cursor.execute(DELETE_RATES_QUERY)
                    cursor.execute(DELETE_RATES_ALERT_QUERY)  
                    cursor.execute(DELETE_RATE_ALERT_DETAIL_QUERY)  
                    for rate in rates_data:
                        if not rate.get('has_warnings'):
                            cursor.execute(INSERT_QUERY, (
                                file_id,
                                rate['consecutivo'],
                                rate['banco'],
                                rate['min_plazo'],
                                rate['max_plazo'],
                                rate['min_monto'],
                                rate['max_monto'],
                                rate['tasa'],
                                rate['fecha']
                            ))                  

                        if rate['has_warnings']:
                            cursor.execute(INSERT_RATE_WARNING_QUERY, (
                                None,
                                file_id,
                                rate['consecutivo']
                            ))

                            for warning in rate['warnings']:
                                cursor.execute(INSERT_RATE_WARNING_DETAIL, (
                                    cursor.lastrowid,
                                    warning['alert_type'],
                                    warning['message'],
                                )) 
                    conn.commit()
                
        except Exception as err:
            conn.rollback()
            print(f"Error on repository (insert_many_rates): {err}")
            raise

    def get_rates_by_terms_and_amount(self, term_in_days: int, amount: float) -> List[Dict[str, Any]]:
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(GET_RATES_BY_TERM_AND_AMOUNT_QUERY, (term_in_days, amount))
                    results = cursor.fetchall()
                    return results
        except Exception as err:
            print(f"Error on repository (get_rates_by_terms_and_amount): {err}")
            raise