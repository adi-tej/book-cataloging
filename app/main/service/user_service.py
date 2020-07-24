from time import time
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as JWTSerializer

from app.main import db
from app.main.model.user import User

def get_all_users():
    return User.query.all()

def get_a_user(user_id):
    return User.query.filter_by(user_id=user_id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def generate_token(self, expires_in, user_id, user_email, user_name):
    serializer =JWTSerializer(
        secret_key=key,
        expires_in=expires_in
    )
    payload = {
        'user_id': user_id,
        'user_email': user_email,
        'user_name': user_name,
        'generate_time': time()
    }

    token = self.serializer.dumps(payload).decode()
    return token

def validate_token(self, token):
    try:
        payload = self.serializer.loads(token.encode())
    except SignatureExpired:
        return 'token expired'
    except BadSignature:
        return 'invalid token'

    return payload
