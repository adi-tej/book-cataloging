from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restplus import Api

from book import books
from auth import auth
from order import order

ebay_conn = Connection(config_file="ebay.yaml", domain="api.sandbox.ebay.com", debug=True)
request_data = {
    "ApplicationDeliveryPreferences": {
        "ApplicationEnable": "Enable",
        "ApplicationURL": "http://127.0.0.1/items/notifications/",
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

ebay_conn.execute("SetNotificationPreferences", request_data)

app = Flask(__name__)
# for initial application config we should config from a file,
# because we need config our manager accounts initially...
# we still not have MySQL database, we need AWS account
# ================below is for testing======================
app.config['test'] = True
app.config['SECRET_KEY'] = 'Royal Never Give Up'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///....'

db = SQLAlchemy(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(books, url_prefix='/book')
app.register_blueprint(order, url_prefix='/order')

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
