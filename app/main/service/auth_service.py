from flask import jsonify, make_response
from app.main.model.user import User
from app.main.service.user_service import TOKEN
from ..http_status import *
from ..model.blacklist import BlacklistToken
from .. import db


class Auth:

    @staticmethod
    def login(data):
        """ for user login, user need to provide email and the password """
        # user_info = data
        user_email, user_name, password = '', '', ''
        # user = User()
        # if user_info['email']:
        email, password = \
            data['email'].strip(), data['password'].strip()
        user = User.query.filter_by(email=email).first()

        if not user:
            resp = make_response(jsonify({'message': 'user does not exist'}))
            resp.status_code = UNAUTHORIZED
            return resp
        if not user.check_password(password):
            resp = make_response(jsonify({'message': 'incorrect password'}))
            resp.status_code = UNAUTHORIZED
            return resp

        # after successfully varify the user backend api will issue token
        token = TOKEN.generate_token(user.id, user.email, user.opshop_id)
        resp_data = {
            'user_info': {
                'user_id': user.id,
                'name': user.name,
                'email': user.email
            },
            'token': token,
        }
        return make_response(resp_data, SUCCESS)
        # resp.status_code = POST_SUCCESS
        # return resp

    @staticmethod
    def logout(token):
        """ logout, add the token to the black list """
        black_token = BlacklistToken(token=token)
        db.session.add(black_token)
        db.session.commit()
