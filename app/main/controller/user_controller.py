from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import get_a_user, get_all_users
from ..util.decorator import token_required

api = UserDto.api
user_model = UserDto.user

@api.route('/<user_id>')
@api.param('user_id', 'user unique id')
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('retrive a user')
    @api.marshal_with(user_model)
    @token_required
    def get(self, user_id):
        """ get a user given its identifier"""
        user = get_a_user(user_id)
        if not user:
            api.abort(404)
        else:
            return user
