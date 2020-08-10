from flask import request
from flask_restplus import Resource
import json

from app.main.service.auth_service import Auth
from ..util.dto import AuthDto
from ..util.decorator import token_required

api = AuthDto.api
auth_model = AuthDto.user_auth


@api.route('login')
class UserLogin(Resource):
    @api.expect(auth_model, validate=True)
    @api.doc(
        description="Login with email and password for token"
    )
    @api.response(201, 'success')
    @api.response(401, 'unauthorized')
    def post(self):
        user_info = json.loads(request.data)
        return Auth.login(data=user_info)


@api.route('logout')
class UserLogout(Resource):
    @api.doc(description="Logout from user")
    @api.response(201, 'success')
    @api.response(401, 'unauthorized')
    @token_required
    def post(self):
        token = request.headers.get('token')
        return Auth.logout(token)
