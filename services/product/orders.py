from flask import request
from flask_restful import Resource
from src.main_logger import set_up_logging
from src.response import Resp
from src.query_base.store_query import Order
import uuid
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

logger = set_up_logging()
resp = Resp()


class NewOrder(Resource):
    @staticmethod
    @jwt_required
    def post():
        data = request.get_json()['data']
        # try:
        # Getting user_if from token
        user_id = get_jwt_identity()

        # Generating order id
        order_id = str(uuid.uuid4())

        # placing order
        Order.place_order(order_id, user_id, data['addressId'], data['paymentMethod'], data['orderReceipt'])

        # Order items
        Order.order_item(order_id, data['orderItems'])
        return resp.http_200(data={"message": "Order placed", "orderId": order_id[-12:]})
        # except Exception as ex:
        #     logger.info(ex)
        #     return resp.http_500(data={"error": "order not placed, please try again!"})


class OrderHistory(Resource):

    @staticmethod
    @jwt_required
    def get():
        try:
            # Getting user_if from token
            user_id = get_jwt_identity()
            logger.info(f"User Id: {user_id}")
            history = Order.order_history(user_id)['data']
            logger.info(f"Formatting order history")
            if history:
                orders = {}
                for order in history:
                    if order['order_id'] not in orders:
                        orders[order['order_id']] = {}
                        orders[order['order_id']]['actualOrderId'] = order['actualOrderId']
                        orders[order['order_id']]['orderOn'] = order['order_on'].__str__()
                        orders[order['order_id']]['orderStatus'] = order['status']
                        orders[order['order_id']]['addressId'] = order['address_id']
                        orders[order['order_id']]['paymentMethod'] = order['payment_mode']
                    if 'orderItems' not in orders[order['order_id']]:
                        orders[order['order_id']]['orderItems'] = []
                    orders[order['order_id']]['orderItems'].append({
                        "name": order['product_name'],
                        "quantity": order['quantity'],
                        "price": order['price'],
                        "weight": order['weight'],
                        "measureUnit": order['measure_unit'],
                        "productId": order['product_id'],
                        "itemId": order['item_id']
                    })
                    orders[order['order_id']]['orderReceipt'] = {
                        "subTotal": order['sub_total'],
                        "tax": order['tax'],
                        "deliveryCharge": order['delivery_charge'],
                        "promoCode": order['promo_code'],
                        "discount": order['discount'],
                        "totalPrice": order['total_amount']
                    }

                return resp.http_200(data=orders)
            return resp.http_200(data={})
        except Exception as ex:
            logger.info(ex)
            return resp.http_500(data={"error": "order history not found"})

class CancelOrder(Resource):
    @staticmethod
    @jwt_required
    def post():
        try:
            order_id = request.get_json()['data']['actualOrderId']
            Order.cancel_order(order_id)
            logger.info("Order cancelled")
            return resp.http_200(data="Order cancelled")
        except Exception as ex:
            logger.info(ex)
            return resp.http_500(data={"error": "we not able to cancel this order."})
