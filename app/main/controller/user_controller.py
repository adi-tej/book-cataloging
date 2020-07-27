from flask import request, make_response, jsonify
from flask_restplus import Resource, marshal
import json

from ..util.dto import UserDto
from ..service.user_service import get_a_user, get_all_users
from ..util.decorator import token_required
from ..http_status import *

api = UserDto.api
user_model = UserDto.user

@api.route('/')
class User(Resource):
    @api.doc('retrive a user')
    @api.response(200, 'success', model=user_model)
    @api.response(404, 'not found')
    @api.response(401, 'unauthorized')
    @api.param('user_id', description='take user id as parameter')
    @token_required
    def get(self):
        """ get a user given its identifier"""
        user_id = request.args.get('user_id')
        if user_id:
            user = get_a_user(user_id)
            if not user:
                api.abort(404, 'user not exist')
            else:
                return marshal(user, user_model), GET_SUCCESS
        else:
            api.abort(404, 'user not exist')
