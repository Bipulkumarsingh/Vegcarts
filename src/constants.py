from library.db.db_connection import Database
import json


class ConstantsMeta(type):

    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Constants:
    __slots__ = ['db']

    def __init__(self):
        self.db = self.get_config('docker')

    @staticmethod
    def get_config(key):
        with open("src/db_cred.json", 'r') as file:
            return json.load(file)[key]

    def receive_query(self, query):
        try:
            vp = Database(self.db)
            return vp.select(query=query)
        except Exception as e:
            print(e)

    def insert_query(self, query):
        try:
            vp = Database(self.db)
            return vp.insert(query)
        except Exception as e:
            print(e)

    def delete_query(self, query):
        try:
            vp = Database(self.db)
            return vp.delete(query=query)["data"]
        except Exception as e:
            print(e)

    def update_query(self, query):
        try:
            vp = Database(self.db)
            return vp.update(query)
        except Exception as e:
            print(e)
