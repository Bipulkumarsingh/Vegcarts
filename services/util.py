from flask_restful import Resource
from src.response import Resp
from src.constants import Constants
from src.main_logger import set_up_logging
from library.cache.redis_connect import RedisConnector
from src.query_base.user_query import Location
from src.query_base.store_query import HomeItem
from operator import itemgetter
from src.query_base.store_query import Item

resp = Resp()
logger = set_up_logging()
redis_connector = RedisConnector()


class Test(Resource):
    @staticmethod
    def get():
        return resp.http_405()

    @staticmethod
    def post():
        data = Constants().receive_query("select 1=1;")
        logger.info(f"Database connection test: {data}")
        return resp.http_200()


def home():
    mapping = {
        "slides": [],
        "categories": [],
        "footer": {}
    }
    try:
        elements = HomeItem.get_home_element()['data']
        for item in elements:
            logger.info(item)
            if item['name'] == 'slides':
                mapping['slides'].append({"id": item['id'], "image": item['image'], "order": item['order']})
            if item['name'] == 'footer':
                mapping['footer']['image'] = item['image']
                mapping['footer']['id'] = item['id']
            if item['category_order']:
                try:
                    category_index = list(map(itemgetter('name'), mapping['categories'])).index(item['category'])
                    mapping['categories'][category_index]['subCategories'].append({
                        "name": item['name'],
                        "order": item['order'],
                        "image": item['image'],
                        "search": {"type": "subCategory", "value": item['search_value']}
                    })
                except:
                    mapping['categories'].append({
                        "name": item["category"],
                        "order": item["category_order"],
                        "subCategories": [
                            {
                                "name": item['name'],
                                "order": item['order'],
                                "image": item['image'],
                                "search": {"type": "subCategory", "value": item['search_value']}
                            }
                        ],
                        "numColumns": item['num_columns']
                    })
        return mapping
    except Exception as ex:
        logger.exception(ex)
        return mapping


def product_category():
    sub_category = "pc.name"
    search_value = ['Beans', 'Chilli', 'Exotic', 'Garlic', 'Gourds', 'Leafy', 'Other', 'Potato', 'Root']
    final = {}
    for value in search_value:
        query_clause = f"{sub_category} like '%{value}%'"
        product_list = Item.get_items(query_clause)['data']
        products = []
        for product in product_list:
            try:
                product_index = list(map(itemgetter('name'), products)).index(product['name'])
                products[product_index]["priceList"][product["priceId"]] = {
                    "weight": product["weight"],
                    "unit": product["unit"],
                    "price": product["price"],
                    "inStock": product["inStock"],
                    "actualPrice": product["actualPrice"]
                }
            except ValueError:
                products.append(
                    {
                        "id": product["productId"],
                        "name": product["name"],
                        "image": product["image"].strip(),
                        "categories": [product["category"]],
                        "subCategories": [product["subCategory"]],
                        "priceList": {
                            product["priceId"]: {
                                "weight": product["weight"],
                                "unit": product["unit"],
                                "price": product["price"],
                                "inStock": product["inStock"],
                                "actualPrice": product["actualPrice"]
                            }
                        }
                    }
                )
        final[value] = products
    return final


class PublishMeta(Resource):
    @staticmethod
    def get():
        logger.info("Publish Metadata start.")
        locality = Location.get_locality()['data']
        home_mapping = home()
        redis_connector.set_metadata("common", {"locality": locality, "home": home_mapping})
        product_subcategory = product_category()
        redis_connector.set_metadata("product_subcategory", product_subcategory)
        logger.info("Publish Metadata Finish.")
        return resp.http_200()
