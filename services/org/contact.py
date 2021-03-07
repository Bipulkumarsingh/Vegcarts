from flask_restful import Resource
from flask import request
from src.response import Resp
from src.main_logger import set_up_logging
from src.query_base.org_query import Contact
from src.query_base.store_query import Order
from flask_jwt_extended import jwt_required, get_jwt_identity

resp = Resp()
logger = set_up_logging()


class ContactUs(Resource):
    @staticmethod
    @jwt_required
    def post():
        try:
            user_id = get_jwt_identity()
            data = request.get_json()['data']
            logger.info(f"data: {data}")
            Contact.complain(data['reasonId'], data['comment'], user_id)
            return resp.http_200(data={"message": "we will contact you soon"})
        except Exception as ex:
            logger.exception(ex)
            return resp.http_500(data={"error": "unable to contact customer care !"})


class OrderOnPhone(Resource):
    @staticmethod
    @jwt_required
    def post():
        try:
            locality_id = request.get_json()['data'].get('localityId', -1)
            mobile_no = Order.order_on_phone(locality_id)['data']
            if mobile_no:
                return resp.http_200(data=mobile_no[0])
            return resp.http_200(data={})
        except Exception as ex:
            logger.exception(ex)
            return resp.http_200(data={})


class GetReason(Resource):
    @staticmethod
    def get():
        try:
            reasons = [
                {
                    "id": 1,
                    "reason": "Order related Queries"
                },
                {
                    "id": 2,
                    "reason": "Order related Complaints"
                },
                {
                    "id": 3,
                    "reason": "Issues regarding my online payment"
                },
                {
                    "id": 4,
                    "reason": "General Inquiry - Business, products etc."
                },
                {
                    "id": 5,
                    "reason": "Unable to place order"
                }
            ]
            return resp.http_200(data=reasons)
        except Exception as ex:
            logger.exception(ex)
            return resp.http_200(data=[])
