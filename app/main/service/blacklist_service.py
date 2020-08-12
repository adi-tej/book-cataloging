from flask import make_response, jsonify
from app.main import db
from app.main.model.blacklist import BlacklistToken


def save_token(token):
    """ save the token into black list """
    blacklist_token = BlacklistToken(token=token)
    try:
        db.session.add(blacklist_token)
        db.session.commit()
        response_data = {
            'status': 'success',
            'message': 'logout success'
        }
        resp = make_response(jsonify(response_data))
        resp.status_code = 200
        return resp
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': e
        }
        resp = make_response(jsonify(response_data))
        resp.status_code = 200
        return resp
