from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restplus import Api, Namespace
import pymysql
from os import system

# The below ApplicationURL is just an example, after deploying the app to
# AWS, need to config the production environment URL.
# This config is for eBay notifications, from below it can be seen there are
# two kinds of notifications should be received from eBay(ItemSold, ItemListed)
# The domain is configed as "api.sandbox.ebay.com", when it is deployed into the
# production environment, it should be "api.ebay.com" and turn off debug

# -- Wei Song

app = Flask(__name__)
app.config['test'] = True
app.config['SECRET_KEY'] = 'Royal Never Give Up'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ShermanLemon0301@127.0.0.1:3306/shops'

db = SQLAlchemy(app)

opshop_api = Api(
    app,
    description="opshop api -- book scanning, listing, selling, order management..",
    version='1.0',
    title='Opshop Api',
    authorizations={
        "TOKEN-BASED":{
            "type": "apiKey",
            "name": "API-TOKEN",
            "in": "header",
        }
    },
)

from business.book import books, books_api
from business.notifications import notification, notification_api
from authorization.auth import auth, auth_api
from business.order import order, order_api

opshop_api.add_namespace(auth_api, path='/auth')
opshop_api.add_namespace(books_api, path='/book')
opshop_api.add_namespace(order_api, path='/order')
opshop_api.add_namespace(notification_api, path='/notification')

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(books, url_prefix='/book')
app.register_blueprint(order)
app.register_blueprint(notification, url_prefix='/notification')

db.drop_all()
db.create_all()

if __name__ == '__main__':
    app.debug=True
    app.run()
