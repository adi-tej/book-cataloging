from flask import Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as JWTSerializer
from werkzeug.security import check_password_hash, generate_password_hash
from time import time
from functools import wraps
import json

from app import login_manager, opshop_api, db
from models import User
from http_status import *


# ------------------------- Authentication ---------------------- #
# Spec of user access management
# Step-1: Login, user provide the credentials(email,password) to server
# Step-2: Server will check the email and password, then issue an auth token
# Step-3: Further access with the service user only need to provide auth token
# Step-4: Logout --> frontend revoke the auth token

# --logout
# JWT based user access, for backend there is not necessary to implement logout,
# when user need to logout frontend need to logout user and destroy the token.

# -- Wei Song
# -- 2020/06/19

auth = Blueprint('auth_api', __name__)

login_api = opshop_api.namespace(
    'login',
    description="user authentication process"
)

password_api = opshop_api.namespace(
    'password modification',
    description="user password modification process"
)

user_login_model = auth_api.model(
    'User',
    {
        'register_email': fields.String,
        'password': fields.String
    }
)

@login_manager.user_loader
def load_user(user_id):
    return User.get_user(int(user_id))

@auth.route('/login/')
class UserLogin(Resource):
    @login_api.expect()
    @login_api.doc(
        description="Login with email and password for token"
    )
    def post(self):
        user_info = json.loads(request.data)
        user_email, password = \
            user_info['register_email'].strip(), user_info['password'].strip()

        user = User.query.filter_by(register_email=user_email).first()

        resp = make_response()
        if not user:
            resp.status_code = UNAUTHORIZED
            resp.headers['message'] = 'user not exist'
            return resp
        if not check_password_hash(user.password, password):
            resp.status_code = UNAUTHORIZED
            resp.headers['message'] = 'password incorrect'
            return resp

        token = TOKEN.generate_token(user.user_id, user.register_email, user.user_name)
        resp.headers['API-TOKEN'] = token
        resp.status_code = POST_SUCCESS

        return resp

@auth.route('/password/')
class UserPassword(Resource):
    @token_required
    @password_api.expect()
    @password_api.doc(
        description="Password modification"
    )
    def post(self):
        user_info = json.loads(request.data)
        user_email, password = \
            user_info['register_email'].strip(), user_info['password'].strip()

        user = User.query.filter_by(register_email=user_email).first()
        resp = make_response()
        if not user:
            resp.headers['status'] = UNAUTHORIZED
            resp.headers['message'] = 'user not exist'
            return resp

        user.password = generate_password_hash(password, method='sha256')
        db.session.add(user)
        db.session.commit()

        resp.status_code = POST_SUCCESS
        resp.headers['message'] = 'password update success'

        return resp

class JWToken:
    def __init__(self, my_secret_key, expires):
        self.serializer = JWTSerializer(
            secret_key=my_secret_key,
            expires_in=expires
        )

    def generate_token(self, user_id, user_email, user_name):

        payload = {
            'user_id': user_id,
            'user_email': user_email,
            'user_name': user_name,
            'generate_time': time()
        }

        token = self.serializer.dumps(payload).decode()

    def validate_token(self, token):

        try:
            payload = self.serializer.loads(token.encode())
        except SignatureExpired:
            return 'token expired'
        except BadSignature:
            return 'invalid token'

        return 'valid token'

SECRET_KEY = "LECJEVH@CEGFG$5@%$^LKSH*&IJs8N"
EXPIRES_IN = 60
TOKEN = JWToken(SECRET_KEY, EXPIRES_IN)

def token_required(f):
    @wraps(f)
    def decorate(*args, **kargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({'error': 'Authentication token is missing', 'status': 401})

        result = TOKEN.validate_token(token)
        resp = make_response()
        if result is 'token expired':
            resp.status_code = UNAUTHORIZED
            resp.headers['message'] = 'token expired'
            return resp
        elif result is 'invalid token':
            resp.status_code = UNAUTHORIZED
            resp.headers['message'] = 'invalid token'
            return resp
        else:
            if result is 'valid token':
                return f(*args, **kargs)
            else:
                resp.status_code = UNAUTHORIZED
                resp.headers['message'] = 'unknown token'
                return resp
    return decorate

