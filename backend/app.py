from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restplus import Api

from book import books
from auth import auth
from order import order
from notifications import notification

# The below ApplicationURL is just an example, after deploying the app to
# AWS, need to config the production environment URL.
# This config is for eBay notifications, from below it can be seen there are
# two kinds of notifications should be received from eBay(ItemSold, ItemListed)
# The domain is configed as "api.sandbox.ebay.com", when it is deployed into the
# production environment, it should be "api.ebay.com" and turn off debug

# -- Wei Song

# --> This part will be configed before the application running <--
# --> This part will be configed before the application running <--
ebay_conn = Connection(config_file="ebay.yaml", domain="api.sandbox.ebay.com", debug=True)
request_data = {
    "ApplicationDeliveryPreferences": {
        "ApplicationEnable": "Enable",
        "ApplicationURL": "http://127.0.0.1/notifications/",
    },

    "UserDeliveryPrederenceArray": [
        {
            "NotificationEnable": {
                "EventEnable": "Enable",
                "EventType": "ItemSold"
            }
        },

        {
            "NotificationEnable": {
                "EventEnable": "Enable",
                "EventType": "ItemListed"
            }
        }
    ],
}

# set notification preferences to ebay...
ebay_conn.execute("SetNotificationPreferences", request_data)

app = Flask(__name__)
app.config['test'] = True
app.config['SECRET_KEY'] = 'Royal Never Give Up'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///....'

db = SQLAlchemy(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(books, url_prefix='/book')
app.register_blueprint(order, url_prefix='/order')
app.register_blueprint(notification, url_prefix='/notification')

opshop_api = Api(
    app=app,
    version='1.0',
    title='Opshop book&ebay Api',
    decorators="This api will try to provide service for opshop mobile app",
    authorizations={
        "TOKEN-BASED":{
            "type": "apiKey",
            "name": "API-TOKEN",
            "in": "header"
        }
    }
)

if __name__ == '__main__':
    app.run()
