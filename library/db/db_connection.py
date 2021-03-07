from mysql import connector
from src.main_logger import set_up_logging
import json

logger = set_up_logging()


class Database:
    connection = None
    cursor = None

    def __init__(self, config):
        self.config = config

    def __create_connection(self):
        self.connection = connector.connect(**self.config)

    # cursor is private,
    # you can use this to do database operation inside derived class if Inheriting Database class.

    def __create_cursor(self):
        self.cursor = self.connection.cursor(dictionary=True)

    def __execute(self, query):
        try:
            self.__create_connection()
            self.__create_cursor()
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as ex:
            logger.exception(ex)
            return 0
        finally:
            self.cursor.close()
            self.connection.close()

    # Below are public functions to be called for database operation.

    def select(self, query):
        try:
            self.__create_connection()
            self.__create_cursor()
            self.cursor.execute(query)
            query_result = self.cursor.fetchall()
            total_rows = self.cursor.rowcount
            resp = {'data': query_result,
                    "row_count": total_rows,
                    'sqlerror': False
                    }
            return resp
        except Exception as ex:
            return {'data': {},
                    'sqlError': str(ex)
                    }
        finally:
            self.cursor.close()
            self.connection.close()

    def insert(self, query):
        return self.__execute(query)

    def update(self, query):
        return self.__execute(query)

    def delete(self, query):
        return self.__execute(query)
