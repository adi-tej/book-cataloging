from time import time
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as JWTSerializer, JSONWebSignatureSerializer

from app.main import db
from app.main.model.user import User
from app.main.config import key


def get_all_users():
    return User.query.all()


def get_user(id):
    return User.query.filter_by(id=id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate_token(self, id, email, opshop_id):
        serializer = JWTSerializer(
            secret_key=key,
            expires_in=self.expires_in
        )
        payload = {
            'id': id,
            'email': email,
            'opshop_id': opshop_id,
            'generate_time': time()
        }

        token = self.serializer.dumps(payload)
        return token.decode()

    def validate_token(self, token):
        try:
            payload = self.serializer.loads(token.encode())
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        return payload


EXPIRE = 6000
TOKEN = AuthenticationToken(key, EXPIRE)
