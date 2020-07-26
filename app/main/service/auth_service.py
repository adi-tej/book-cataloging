from flask import jsonify, make_response

from app.main.model.user import User
from app.main.service.user_service import TOKEN
from ..service.blacklist_service import save_token
from ..http_status import *
from ..model.blacklist import BlacklistToken
from .. import db

class Auth:

    @staticmethod
    def login(data):
        user_info = data
        user_email, user_name, password = '', '', ''
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
            resp.status_code = NOT_FOUND
            return resp
        if not user.check_password(password):
            resp = make_response(jsonify({'message': 'password not right'}))
            resp.status_code = UNAUTHORIZED
            return resp

        token = TOKEN.generate_token(user.user_id, user.register_email, user.user_name)
        resp_data = {
            'user_info':{
                'user_id':user.user_id,
                'user_name':user.user_name,
                'register_email':user.register_email
            },
            'token':token,
        }
        resp = make_response(resp_data)
        resp.status_code = POST_SUCCESS
        return resp

    @staticmethod
    def logout(token):
        black_token = BlacklistToken(token=token)
        db.session.add(black_token)
        db.session.commit()
