from flask_restful import Resource
# from src.query_base.user_query import Location
from src.response import Resp
from src.main_logger import set_up_logging
from library.cache.redis_connect import RedisConnector

resp = Resp()
logger = set_up_logging()
redis_connection = RedisConnector()


class Locality(Resource):
    @staticmethod
    def post():
        return resp.http_405(data={"message": "Method not allowed!"})

    @staticmethod
    def get():
        try:
            logger.info("getting data.")
            # locality = Location.get_locality()['data']
            locality = redis_connection.get_metadata('common', key='locality')
            logger.info(f"Locality: {locality}")
            return resp.http_200(data=locality)
        except Exception as ex:
            logger.exception(ex)
            return resp.http_500()
