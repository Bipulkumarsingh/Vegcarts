from flask_restful import Resource
from src.main_logger import set_up_logging
from src.response import Resp
from flask_jwt_extended import jwt_required
from library.cache.redis_connect import RedisConnector

logger = set_up_logging()
resp = Resp()
redis_connection = RedisConnector()


class Home(Resource):
    @staticmethod
    @jwt_required
    def get():
        # TODO Landing page { slides: [{image: "", order: ""},{image:"", order:""}],
        #  categories: [{name:"", order:"", subcategories:[{name:"", order:"",image:""}]}], footer:{image:""}}
        mapping = {
            "slides": [],
            "categories": [],
            "footer": {}
        }
        try:
            mapping = redis_connection.get_metadata('common', key='home')
            return resp.http_200(data=mapping)
        except Exception as ex:
            logger.exception(ex)
            return resp.http_200(data=mapping)
