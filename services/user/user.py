import requests
from flask import request
from flask_restful import Resource
from src.query_base.user_query import User, ValidateCode, Location
from library.otp.otp import generate_otp
from src.response import Resp
from src.main_logger import set_up_logging
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims


resp = Resp()
logger = set_up_logging()


class Login(Resource):
    @staticmethod
    def otp(mobile_no):
        # Generate and send OTP
        otp, expire_time = generate_otp()

        # Sending sms using Fast sms Api
        url = "bulk_sms_url"

        payload = f"sender_id=id_information&values={otp}"
        # response = requests.request("POST", url, data=payload, headers=headers)
        # print(response.text)

        # saving OTP for validation process
        ValidateCode.insert_code(mobile_no, otp)

    def post(self):
        try:
            data = request.get_json()['data']
            # Check existing user
            previous_user = User.user_exists(data['mobileNo'], data['localityId'])
            print("data found")
            if previous_user['data']:
                logger.info(f"This is previous user!: {previous_user['data']}")
                self.otp(data['mobileNo'])
            else:
                logger.info(f"This is creating/updating user.")
                mobile_no = data.get('mobileNo')
                user_name = data.get('userName')
                is_admin = data.get('isAdmin', 0)
                locality = data.get('localityId', -1)
                # Insert or Update user
                created = User.create_user(user_name=user_name, mobile_no=mobile_no, is_admin=is_admin,
                                           locality=locality)
                logger.info(f"New user created!: {created}")
                self.otp(mobile_no)
            return resp.http_200(data="validate otp")
        except Exception as ex:
            logger.exception(ex)
            return resp.http_500(data="user not created")


class GetUserInfo(Resource):
    @staticmethod
    @jwt_required
    def post():
        try:
            claims = get_jwt_claims()
            mobile_no = claims['user']['mobile_no']
            logger.info(f"mobile no: {mobile_no}")
            user = User.user_info(mobile_no)['data']
            logger.info(f"user records: {user}")
            locality = Location.get_locality()['data']
            logger.info(f"location: {locality}")
            if user:
                user = user[0]
                user_info = {
                    "user": {"name": user['name'],
                             "mobileNo": user['mobile_no'],
                             "locality": {"id": user['pincode'], "name": user['locality_name']}
                             },
                    "cart": {},
                    "locality": locality,
                    "helplineNo": user['helplineNo']
                }
                return resp.http_200(data=user_info)
            return resp.http_200(data={"user": {}, "cart": {}})
        except Exception as ex:
            logger.exception(ex)
            return resp.http_500(data="something went wrong!")


class UpdateUser(Resource):
    @staticmethod
    @jwt_required
    def post():
        try:
            user_id = get_jwt_identity()
            data = request.get_json()['data']
            user_updated = User.update_user(user_id, data['name'], data['localityId'])
            logger.info(f"user_updated: {user_updated}")
            return resp.http_200(data="user data updated")
        except Exception as ex:
            logger.exception(ex)
            return resp.http_500(data="User not updated")

class ResendOtp(Resource):

    @staticmethod
    def post():
        try:
            data = request.get_json()["data"]
            mobile_no = data.get('mobileNo')
            otp, expire_time = generate_otp()
            otp = 1234
            ValidateCode.insert_code(mobile_no, otp)
            return resp.http_200(data="OTP is sent to register mobile number.")
        except Exception as ex:
            logger.exception(ex)
            return resp.http_500()


class GetAddress(Resource):
    @staticmethod
    @jwt_required
    def get():
        try:
            user_id = get_jwt_identity()
            address_list = User.address_list(user_id)
            logger.info(f"Address List: {address_list}")
            return resp.http_200(data=address_list['data'])
        except Exception as ex:
            logger.exception(ex)
            return resp.http_200(data=[])


class AddAddress(Resource):
    @staticmethod
    @jwt_required
    def post():
        try:
            data = request.get_json()['data']
            user_id = get_jwt_identity()
            inserted = User.add_address(user_id, **data)
            logger.info(f"address added: {inserted}")
            return resp.http_200(data={"addressId": inserted})
        except Exception as ex:
            logger.exception(ex)
            return resp.http_500(data="something went wrong !")


class UpdateAddress(Resource):
    @staticmethod
    @jwt_required
    def post():
        try:
            data = request.get_json()['data']
            updated = User.update_address(**data)
            logger.info(f"Address updated: {updated}")
            return resp.http_200(data="Address updated")
        except Exception as ex:
            logger.exception(ex)
            return resp.http_500(data="something went wrong")


class DeleteAddress(Resource):
    @staticmethod
    @jwt_required
    def post():
        try:
            data = request.get_json()['data']
            deleted = User.delete_address(**data)
            logger.info(f"Address deleted: {deleted}")
            return resp.http_200(data="Address deleted")
        except Exception as ex:
            logger.exception(ex)
            return resp.http_500(data="Something went wrong")
