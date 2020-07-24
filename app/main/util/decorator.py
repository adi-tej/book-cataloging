from flask import jsonify, make_response

from functools import wraps
from app.main.service.user_service import validate_token

def token_required(f):
    @wraps(f)
    def decorate(*args, **kargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({'error': 'Authentication token is missing', 'status': 401})

        result = validate_token(token)
        if result is 'token expired':
            resp = make_response(jsonify({'message':'token expired'}))
            resp.status_code = UNAUTHORIZED
            return resp
        elif result is 'invalid token':
            resp = make_response(jsonify({'message': 'invalid token'}))
            resp.status_code = UNAUTHORIZED
            return resp
        else:
            return f(*args, **kargs)
    return decorate