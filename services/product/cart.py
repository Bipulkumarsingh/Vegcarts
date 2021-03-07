from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.main_logger import set_up_logging
from src.query_base.store_query import CartItem
from src.response import Resp
import json

logger = set_up_logging()
resp = Resp()


class GetCart(Resource):
    @staticmethod
    @jwt_required
    def get():
        try:
            user_id = get_jwt_identity()
            items = CartItem.get_cart(user_id)['data']
            items = json.loads(items[0]['cart_item'])
            return resp.http_200(data=items)
        except Exception as ex:
            logger.exception(ex)
            return resp.http_200(data=[])


class UpdateCart(Resource):
    @staticmethod
    @jwt_required
    def post():
        try:
            user_id = get_jwt_identity()
            data = request.get_json()['data']
            insert_items = CartItem.update_cart(user_id, json.dumps(data))
            logger.info(f"Data inserted: {insert_items}")
            return resp.http_200(data='cart updated')
        except Exception as ex:
            logger.exception(ex)
            return resp.http_500(data="cart not updated")
