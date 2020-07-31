from flask import make_response, jsonify

from app.main import db
from app.main.model.blacklist import BlacklistToken


def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        db.session.add(blacklist_token)
        db.session.commit()
        reponse_data = {
            'status': 'success',
            'message': 'logout success'
        }
        resp = make_response(jsonify(reponse_data))
        resp.status_code = 200
        return resp
    except Exception as e:
        reponse_data = {
            'status': 'fail',
            'message': e
        }
        resp = make_response(jsonify(reponse_data))
        resp.status_code = 200
        return resp
