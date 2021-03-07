from src.constants import Constants
from src.main_logger import set_up_logging

constant = Constants()
logger = set_up_logging()


class User:
    def __init__(self):
        pass

    @staticmethod
    def user_exists(mobile_no, pincode):
        query = f"SELECT user_id, name, mobile_no, admin FROM users where mobile_no = {mobile_no} and pincode = {pincode} and active = 1;"
        logger.info(f"User query: {query}")
        return constant.receive_query(query)

    @staticmethod
    def update_user(user_id, name, locality_id):
        query = f"""UPDATE users
                    SET name='{name}', pincode={locality_id}
                    WHERE user_id={user_id};"""
        logger.info(f"update query: {query}")
        return constant.insert_query(query)

    @staticmethod
    def user_info(mobile_no):
        query = f"""
            SELECT
                user_id,
                gu.name,
                mobile_no,
                admin,
                active,
                gu.pincode,
                gl.name AS locality_name,
                gl.helpline_no as helplineNo
            FROM
                users gu
            INNER JOIN locality gl ON
                gu.pincode = gl.pincode
            WHERE
                mobile_no = {mobile_no}
                AND active = 1
        """
        return constant.receive_query(query)

    @staticmethod
    def create_user(user_name, mobile_no, locality, is_admin):
        query = f"INSERT INTO users (name, mobile_no, pincode, admin, active, created_on) VALUES ('{user_name}'," \
                f"  {mobile_no}, {locality}, {is_admin}, 1, CURRENT_TIMESTAMP) ON DUPLICATE KEY UPDATE name = '{user_name}', pincode= {locality}; "
        logger.info(query)
        return constant.insert_query(query)

    @staticmethod
    def add_address(user_id, name, address1, address2, landmark, localityId, mobileNo):
        query = f"""
                INSERT INTO address
                (user_id, name, address1, address2, landmark, pincode, mobile_no)
                VALUES({user_id}, '{name}', '{address1}', '{address2}', '{landmark}', {localityId}, '{mobileNo}');
                """
        return constant.insert_query(query)

    @staticmethod
    def address_list(user_id):
        query = f"SELECT address_id as addressId, name, address1, address2, landmark, pincode as localityId, " \
                f"cast(mobile_no as SIGNED INTEGER) as mobileNo, active FROM address where user_id = {user_id}; "
        return constant.receive_query(query)

    @staticmethod
    def update_address(addressId, name, address1, address2, landmark, localityId, mobileNo, active=1):
        query = f"UPDATE address SET name='{name}', address1='{address1}', address2='{address2}', " \
                f"landmark='{landmark}', pincode={localityId}, mobile_no='{mobileNo}', active={active} WHERE address_id={addressId};"
        return constant.update_query(query)

    @staticmethod
    def delete_address(addressId):
        query = f"UPDATE address SET active=False WHERE address_id={addressId};"
        return constant.update_query(query)


class ValidateCode:
    @staticmethod
    def validate_user(mobile_no, otp):
        query = f"SELECT user_id, name, ur.mobile_no, admin, ur.active, created_on,ur.pincode " \
                f"FROM users ur INNER JOIN validate_code vc on vc.mobile_no = ur.mobile_no where code = {otp} and " \
                f"vc.mobile_no = {mobile_no}; "
        logger.info(query)
        return constant.receive_query(query)

    @staticmethod
    def delete_code(mobile_no, code):
        query = f"DELETE FROM validate_code WHERE mobile_no={mobile_no} and code= {code};"
        return constant.delete_query(query)

    @staticmethod
    def insert_code(mobile_no, code):
        query = f"INSERT INTO validate_code (mobile_no, code, expire_time) VALUES({mobile_no}, {code}, " \
                f"CURRENT_TIMESTAMP) ON DUPLICATE KEY UPDATE code={code};"
        logger.info(f"Insert OTP query: {query}")
        return constant.insert_query(query)


class Location:
    @staticmethod
    def pin_code():
        query = "select pin_code, city_id from locality where city_id in (select city_id " \
                "from cities where is_active=1);"
        return constant.receive_query(query)

    @staticmethod
    def get_city():
        query = f"SELECT city_id, name FROM cities where is_active=1;"
        return constant.receive_query(query)

    @staticmethod
    def get_locality():
        query = "select pincode as id, name from locality where is_active = 1"
        return constant.receive_query(query)
