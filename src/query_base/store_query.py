from src.constants import Constants
from src.main_logger import set_up_logging

constant = Constants()
logger = set_up_logging()


class Item:
    def __init__(self):
        pass

    @staticmethod
    def get_items(where_clause):
        # product_image is temporary for testing.  pd.image
        query = f"""
       SELECT
            DISTINCT
            pd.product_description as name,
            'product_image' as image, 
            pt.name as category,
            pv.weight,
            pv.measure_unit as unit,
            pv.price,
            pv.quantity as inStock,
            pv.market_price as actualPrice,
            pc.name as subCategory,
            pv.version_id as priceId,
            pv.product_id as productId
        from
            product_dimension pd
        inner join product_type pt on
            pd.product_key = pt.type_id
        inner join product_version pv on
            pd.product_id = pv.product_id
        inner join product_category pc on
            pd.product_category = pc.category_id
        where {where_clause}
        """
        logger.info(query)
        return constant.receive_query(query)


class Order:
    def __init__(self):
        pass

    @staticmethod
    def place_order(order_id, user_id, address_id, payment_mode, order_receipt):
        query = f"INSERT INTO orders (order_id, user_id, order_on, status, active, address_id, payment_mode, " \
                f"sub_total, tax, delivery_charge, promo_code, discount, total_amount) " \
                f"VALUES('{order_id}', {user_id}, CURRENT_TIMESTAMP, 'Placed', 1, {address_id}, " \
                f"'{payment_mode}', {order_receipt.get('subTotal')}, {order_receipt.get('tax')}," \
                f" {order_receipt.get('deliveryCharge')}, '{order_receipt.get('promoCode')}', " \
                f"{order_receipt.get('discount')}, {order_receipt.get('totalPrice')});"
        logger.info(query)
        return constant.insert_query(query)

    @staticmethod
    def order_item(order_id, order):
        insert = """
        INSERT
            INTO
            order_items (order_id,
            product_id,
            quantity,
            weight,
            product_name,
            measure_unit,
            price)
        VALUES
        """
        value = [
            f"('{order_id}', {item['productId']}, {item['quantity']}, {item['weight']}, '{item['name']}'," \
            f" '{item['measureUnit']}', {item['price']})"
            for item in order]
        query = insert + ','.join(value) + ";"
        logger.info(query)
        out = constant.insert_query(query)
        return out

    @staticmethod
    def order_history(user_id):
        query = f"""
        SELECT
            SUBSTRING(o.order_id, -12) as order_id,
            o.order_id as actualOrderId,
            order_on,
            status,
            address_id,
            payment_mode,
            sub_total,
            tax,
            delivery_charge,
            promo_code,
            discount,
            total_amount,	
            product_id,
            quantity,
            weight,
            product_name,
            measure_unit,
            price,
            oi.id as item_id
        FROM
            orders o
        inner join order_items oi on
            o.order_id = oi.order_id
        where
            user_id = {user_id};
        """
        return constant.receive_query(query)

    @staticmethod
    def order_on_phone(locality_id):
        query = f"""
            select
                order_on_phone as mobileNo
            from
                locality
            where
                pincode = {locality_id}
                and is_active
        """
        return constant.receive_query(query)

    @staticmethod
    def cancel_order(order_id):
        query = f"update orders set status='Cancelled' where order_id='{order_id}';"
        logger.info(query)
        return constant.insert_query(query)


class HomeItem:
    def __init__(self):
        pass

    @staticmethod
    def get_home_element():
        query = """
        SELECT
            concat(gl.id, '') as id,
            gl.name,
            order_no as `order`,
            'image' as image,
            hc.category_order,
            hc.name as category,
            hc.num_columns,
            gl.search_value
        FROM
            landing gl
        LEFT JOIN home_category hc on
            gl.category_id = hc.id
        """
        return constant.receive_query(query)


class CartItem:
    def __init__(self):
        pass

    @staticmethod
    def update_cart(user_id, items):
        query = f"""
        INSERT
            INTO
            cart (user_id,
            cart_item)
        VALUES({user_id},
        '{items}') on
        duplicate key
        update
            cart_item = '{items}';
        """
        return constant.insert_query(query)

    @staticmethod
    def get_cart(user_id):
        query = f"SELECT cart_item FROM cart WHERE user_id = {user_id};"
        return constant.receive_query(query)
