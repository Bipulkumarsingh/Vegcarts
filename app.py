# Predefined Libraries
from os import path
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token

# Service classes
from services.util import Test, PublishMeta
from services.user.user import ResendOtp  # TokenRefresh
from services.user.user import Login, GetAddress, GetUserInfo, UpdateUser, AddAddress, UpdateAddress, DeleteAddress
from services.org.contact import ContactUs, OrderOnPhone, GetReason
from services.user.locality import Locality  # ,City
from services.product.products import ProductList
from services.product.landing import Home
from services.org.about_us import AboutUs
from services.product.cart import GetCart, UpdateCart
from services.product.orders import NewOrder, OrderHistory, CancelOrder

# Supportive imports
from src.response import Resp
from src.query_base.user_query import ValidateCode
from src.main_logger import set_up_logging
from blacklist import BLACKLIST

# from library.image.images import IMAGES_SET

app = Flask(__name__)
CORS(app)
api = Api(app)

resp = Resp()
logger = set_up_logging()

app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]  # allow blacklisting for access and refresh tokens
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.secret_key = "_ra/xo$web!@secret#key_"  # could do app.config['JWT_SECRET_KEY'] if we prefer

jwt = JWTManager(app)

# Flask upload location
app.config['UPLOADED_IMAGES_DEST'] = path.join("static", "images")


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    """
        Using the user_claims_loader, we can specify a method that will be
        called when creating access tokens, and add these claims to the said
        token. This method is passed the identity of whom the token is being
        created for, and must return data that is json serializable.
    """
    user_info = resp.USER_CLAIM
    resp.USER_CLAIM = None
    return {
        "admin": user_info['admin'],
        "name": user_info['name'],
        "user": {
            "id": identity,
            "active": user_info['active'],
            "mobile_no": user_info['mobile_no'],
            "pincode": user_info['pincode']
        }
    }


class ValidateOtp(Resource):
    @staticmethod
    def post():
        data = request.get_json()["data"]
        try:
            mobile_no = data['mobileNo']
            code = data['otp']
            # Getting user information using validate table's code and mobile no.
            valid_user = ValidateCode.validate_user(mobile_no, code)['data']
            logger.info(f"Valid user: {valid_user}")
            if not valid_user:
                return resp.http_401(data="OTP is not valid")
            valid_user = valid_user[0]
            # Deleting otp from validate table
            ValidateCode.delete_code(mobile_no, code)
            # Adding user information to user_claim show that used it for token generation
            resp.USER_CLAIM = valid_user
            access_token = create_access_token(identity=valid_user['user_id'], fresh=True)
            # refresh_token = create_refresh_token(valid_user['user_id'])
            return resp.http_200(data={"userName": valid_user['name'], "mobileNo": valid_user['mobile_no'],
                                       "access-token": access_token})
        except Exception as ex:
            logger.exception(ex)
            return resp.http_500()


api.add_resource(Test, '/')  # Get/Post method
api.add_resource(Locality, '/locality')  # Get method
api.add_resource(ValidateOtp, '/validate')  # Post method for validating OTP
api.add_resource(Login, '/login')  # Post method
api.add_resource(GetAddress, '/get-address')
api.add_resource(AddAddress, '/add-address')
api.add_resource(UpdateAddress, '/update-address')
api.add_resource(DeleteAddress, '/delete-address')
api.add_resource(ContactUs, '/contact-us')  # Post method and token required
api.add_resource(ResendOtp, '/resend-otp')  # Post method
api.add_resource(AboutUs, '/about-us')  # Get method
api.add_resource(OrderOnPhone, '/order-on-phone')  # Post method and token required
api.add_resource(GetUserInfo, '/get-user-info')  # Post method and token required
api.add_resource(UpdateUser, '/update-user')  # Post method and token required
api.add_resource(GetReason, '/get-reasons')  # Get method
api.add_resource(ProductList, "/search-product")
api.add_resource(Home, '/home')
api.add_resource(GetCart, '/get-cart')
api.add_resource(UpdateCart, '/update-cart')
api.add_resource(NewOrder, '/place-order')
api.add_resource(OrderHistory, '/get-orders')
api.add_resource(CancelOrder, '/cancel-order')
api.add_resource(PublishMeta, '/publish-metadata')


if __name__ == '__main__':
    app.run()
