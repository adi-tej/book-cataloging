from flask_restplus import Api
from flask import Blueprint

# The below ApplicationURL is just an example, after deploying the app to
# AWS, need to config the production environment URL.
# This config is for eBay notifications, from below it can be seen there are
# two kinds of notifications should be received from eBay(ItemSold, ItemListed)
# The domain is configed as "api.sandbox.ebay.com", when it is deployed into the
# production environment, it should be "api.ebay.com" and turn off debug

# -- Wei Song

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.order_controller import api as order_ns
from .main.controller.book_controller import api as book_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Opshop flask restplus api',
          version='1.1',
          description='opshop opshop',
          authorizations={
              "TOKEN-BASED": {
                  "type": "apiKey",
                  "name": "API-TOKEN",
                  "in": "header"
              }
          }
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/')
api.add_namespace(order_ns, path='/order')
api.add_namespace(book_ns, path='/book')
