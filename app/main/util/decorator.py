from flask import jsonify, make_response, request

from functools import wraps
from app.main.service.user_service import TOKEN
from ..http_status import *


def token_required(f):
    @wraps(f)
    def decorate(*args, **kargs):
        token = request.headers.get('Authorization')
        if not token:
            resp = make_response(jsonify({'error': 'Authentication token is missing'}))
            resp.status_code = UNAUTHORIZED
            return resp

        result = TOKEN.validate_token(token)
        if result == 'token expired':
            resp = make_response(jsonify({'message': 'token expired'}))
            resp.status_code = UNAUTHORIZED
            return resp
        elif result == 'invalid token':
            resp = make_response(jsonify({'message': 'invalid token'}))
            resp.status_code = UNAUTHORIZED
            return resp
        else:
            return f(*args, **kargs)

    return decorate
