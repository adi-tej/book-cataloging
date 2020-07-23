from functools import wraps
from app.main.service.user_service import validate_token

def token_required(f):
    @wraps(f)
    def decorate(*args, **kargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({'error': 'Authentication token is missing', 'status': 401})

        result = validate_token(token)
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