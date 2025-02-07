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

        user = TOKEN.validate_token(token)
        if not user:
            resp = make_response(jsonify({'message': 'Invalid Authorization Token'}))
            resp.status_code = UNAUTHORIZED
            return resp
        return f(*args, user, **kargs)

    return decorate
