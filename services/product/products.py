from flask_restful import Resource
from flask import request
# from src.query_base.store_query import Item
from src.response import Resp
from src.main_logger import set_up_logging
# from operator import itemgetter
from library.cache.redis_connect import RedisConnector

resp = Resp()
logger = set_up_logging()
redis_connection = RedisConnector()


class ProductList(Resource):
    @staticmethod
    def post():
        try:
            data = request.get_json()['data']
            filter_map = {
                "subCategory": "pc.name",
                "category": "pt.name",
                "specific": "pd.product_description",
                "all": 1,
                "byId": "pv.product_id"
            }
            products = redis_connection.get_metadata('product_subcategory', key=data.get('name'))
            # query_clause = f"{filter_map.get(data.get('type'))} like '%{data.get('name') or data.get('id')}%'"
            # logger.info(f"Query: {query_clause}")
            # product_list = Item.get_items(query_clause)['data']
            # products = []
            # for product in product_list:
            #     try:
            #         product_index = list(map(itemgetter('name'), products)).index(product['name'])
            #         products[product_index]["priceList"][product["priceId"]] = {
            #             "weight": product["weight"],
            #             "unit": product["unit"],
            #             "price": product["price"],
            #             "inStock": product["inStock"],
            #             "actualPrice": product["actualPrice"]
            #         }
            #     except ValueError:
            #         products.append(
            #             {
            #                 "id": product["productId"],
            #                 "name": product["name"],
            #                 "image": product["image"].strip(),
            #                 "categories": [product["category"]],
            #                 "subCategories": [product["subCategory"]],
            #                 "priceList": {
            #                     product["priceId"]: {
            #                         "weight": product["weight"],
            #                         "unit": product["unit"],
            #                         "price": product["price"],
            #                         "inStock": product["inStock"],
            #                         "actualPrice": product["actualPrice"]
            #                     }
            #                 }
            #             }
            #         )
            # if data.get('type') == 'byId' and products:
            #     products = products[0]
            logger.info(f"length: {len(products)}")
            return resp.http_200(data=products)
        except Exception as ex:
            logger.exception(ex)
            return resp.http_200(data=[])
