from flask import jsonify, make_response
import datetime

from app.main.model.user import User
from app.main.service.user_service import generate_token
from ..service.blacklist_service import save_token
from ..http_status import *
from ..model.blacklist import BlacklistToken
from .. import db

class Auth:
    expire_in = 6000

    @staticmethod
    def login(data):
        user_info = data
        user_email, user_name, password = '', ''
        user = User()
        if user_info['register_email']:
            user_email, password = \
                user_info['register_email'].strip(), user_info['password'].strip()
            user = User.query.filter_by(register_email=user_email).first()
        elif user_info['user_name']:
            user_name, password = \
                user_info['user_name'].strip(), user_info['password'].strip()
            user = User.query.filter_by(user_name=user_name).first()

        if not user:
            resp = make_response(jsonify({'message':'user not exist'}))
            resp.status_code = UNAUTHORIZED
            return resp
        if not User.check_password_hash(user.password, password):
            resp = make_response(jsonify({'message': 'password not right'}))
            resp.status_code = UNAUTHORIZED
            return resp

        token = generate_token(expires_in, user.user_id, user.register_email, user.user_name)
        resp_data = {
            'user_info':user.__dict__.pop('password'),
            'token':token,
        }
        resp = make_response(resp_data)
        resp.status_code = POST_SUCCESS
        return resp

    @staticmethod
    def logout(token):
        black_token = BlacklistToken(token=token, datetime=datetime.datetime.now())
        db.session.add(black_token)
        db.session.commit()
