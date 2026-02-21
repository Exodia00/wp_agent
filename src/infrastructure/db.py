from contextlib import contextmanager

from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool

from config import  get_mysql_config



class MySQLDatabase:

    db_config : dict # Needs to make a call for current_app, wouldn't work before the app is running !
    pool : MySQLConnectionPool

    def __init__(self):
        self.db_config = get_mysql_config()
        self.pool = MySQLConnectionPool(**self.db_config)


    @contextmanager
    def get_cursor(self):
        conn = None
        cursor = None
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            yield cursor
            conn.commit()
        except Error as e:
            if cursor:
                cursor.rollback()
            if conn:
                conn.close()
            raise e # todo: Manage upstream
        finally :
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def execute(self, query, params=None, fetch = True, list_all=True):
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall() if list_all else cursor.fetchone()
                return  cursor # todo : might be used to manage errors
        except Error as e:
            print(e)
            raise
