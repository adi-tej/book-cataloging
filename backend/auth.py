from flask import Blueprint, request, jsonify
from flask_restplus import Api, Resource
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as JWTSerializer
from time import time
from functools import wraps

from app import login_manager
from models import User

auth = Blueprint('auth_api', __name__)

authapi = Api(auth)

# Spec of user access management
# Step-1: Login, user provide the credentials(email,password) to server
# Step-2: Server will check the email and password, then issue an auth token
# Step-3: Further access with the service user only need to provide auth token
# Step-4: Logout --> server revoke the auth token

# Use flask-login to do the user session management.
# It handles the common tasks of logging in, logging out, and remembering
# users' sessions over extended perods of time

@login_manager.user_loader
def load_user(user_id):
    return User.get_user(int(user_id))

@authapi.route('/login/')
class UserLogin(Resource):
    def get(self):
        return "Hello, User"

@authapi.route('/logout/')
class UserLogout(Resource):
    def get(self):
        return "Goodbye, User"

@authapi.route('/password/')
class UserPassword(Resource):
    def post(self):
        return "Change Password"

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
        if result is 'token expired':
            return jsonify({'error': 'token expired', 'status': 401})
        elif result is 'invalid token':
            return jsonify({'error': 'invalid token', 'status': 401})
        else:
            if result is 'valid token':
                return f(*args, **kargs)
            else:
                return jsonify({'error': 'unknown token', 'status': 401})
    return decorate

